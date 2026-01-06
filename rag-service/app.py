#!/usr/bin/env python3
"""
RAG Retrieval Service - Retrieves relevant chunks from Supabase + Neo4j
Generation happens in n8n, not here!
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os

from llama_index.core import VectorStoreIndex, PropertyGraphIndex, Settings
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.vector_stores.supabase import SupabaseVectorStore
from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore

# Setup logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(title="RAG Retrieval Service", version="2.0.0")

# Configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "qwen3-embedding:8b")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# Global retrievers - loaded on startup
vector_retriever = None
graph_retriever = None

@app.on_event("startup")
async def startup_event():
    """Load the vector and graph stores on startup"""
    global vector_retriever, graph_retriever
    
    logger.info("🚀 Starting up RAG Retrieval Service...")
    logger.info(f"📊 Supabase URL: {SUPABASE_URL}")
    logger.info(f"📊 Neo4j URI: {NEO4J_URI}")
    
    # Configure embedding model
    Settings.embed_model = OllamaEmbedding(
        model_name=EMBEDDING_MODEL,
        base_url=OLLAMA_HOST,
    )
    
    try:
        # Load vector store (Supabase)
        logger.info("📚 Connecting to Supabase vector store...")
        
        # Connect directly to Supabase postgres DB
        postgres_password = "FGVUMISvP1NtSWJdKNtFkQBzl3aOsK8CW2ZDbNL-lb4"
        
        vector_store = SupabaseVectorStore(
            postgres_connection_string=f"postgresql://postgres:{postgres_password}@db:5432/postgres",
            collection_name="book_chunks",
            dimension=4096,  # qwen3-embedding:8b actual dimension
        )
        
        vector_index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store,
            embed_model=Settings.embed_model,
        )
        
        vector_retriever = vector_index.as_retriever(
            similarity_top_k=10,  # Retrieve more for n8n to filter
        )
        
        logger.info("✅ Vector store loaded successfully!")
        
    except Exception as e:
        logger.error(f"❌ Failed to load vector store: {e}")
        logger.warning("   Vector retrieval will not be available")
    
    try:
        # Load graph store (Neo4j)
        logger.info("📚 Connecting to Neo4j graph store...")
        logger.info("   ⚠️  Graph retrieval disabled - requires LLM configuration")
        logger.info("   Using vector-only retrieval for now")
        # TODO: Implement graph retrieval without OpenAI dependency
        
    except Exception as e:
        logger.error(f"❌ Failed to load graph store: {e}")
        logger.warning("   Graph retrieval will not be available")


# Request/Response models
class RetrievalRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5
    use_graph: Optional[bool] = True
    use_vector: Optional[bool] = True

class IngestRequest(BaseModel):
    file_path: str  # Path to file in mounted volume

class RetrievalResponse(BaseModel):
    query: str
    chunks: List[Dict[str, Any]]
    total_chunks: int
    retrieval_method: str

class IngestResponse(BaseModel):
    status: str
    chunks_created: int
    message: str


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    vector_ready = vector_retriever is not None
    graph_ready = graph_retriever is not None
    
    return {
        "status": "healthy" if (vector_ready or graph_ready) else "degraded",
        "vector_store": "connected" if vector_ready else "unavailable",
        "graph_store": "connected" if graph_ready else "unavailable",
        "embedding_model": EMBEDDING_MODEL,
        "ollama_host": OLLAMA_HOST,
        "supabase_url": SUPABASE_URL,
        "neo4j_uri": NEO4J_URI,
        "message": "Ready for retrieval! Generation happens in n8n."
    }


@app.post("/retrieve", response_model=RetrievalResponse)
async def retrieve_chunks(request: RetrievalRequest):
    """
    Retrieve relevant chunks from Supabase (vector) and/or Neo4j (graph)
    No generation - just return the raw chunks for n8n to process
    """
    if not vector_retriever and not graph_retriever:
        raise HTTPException(
            status_code=503, 
            detail="No retrieval stores available. Run ingestion first."
        )
    
    try:
        logger.info(f"🔍 Retrieving for query: {request.query}")
        
        all_chunks = []
        methods_used = []
        
        # Vector retrieval from Supabase
        if request.use_vector and vector_retriever:
            logger.info("   → Using vector retrieval (Supabase)")
            vector_nodes = vector_retriever.retrieve(request.query)
            
            for node in vector_nodes[:request.top_k]:
                all_chunks.append({
                    "text": node.text,
                    "score": float(node.score) if hasattr(node, 'score') else None,
                    "metadata": node.metadata if hasattr(node, 'metadata') else {},
                    "source": "vector",
                    "node_id": node.node_id if hasattr(node, 'node_id') else None,
                })
            
            methods_used.append("vector")
            logger.info(f"   ✓ Retrieved {len(vector_nodes)} chunks from vector store")
        
        # Graph retrieval from Neo4j
        if request.use_graph and graph_retriever:
            logger.info("   → Using graph retrieval (Neo4j)")
            try:
                graph_nodes = graph_retriever.retrieve(request.query)
                
                for node in graph_nodes[:request.top_k]:
                    all_chunks.append({
                        "text": node.text,
                        "score": float(node.score) if hasattr(node, 'score') else None,
                        "metadata": node.metadata if hasattr(node, 'metadata') else {},
                        "source": "graph",
                        "node_id": node.node_id if hasattr(node, 'node_id') else None,
                    })
                
                methods_used.append("graph")
                logger.info(f"   ✓ Retrieved {len(graph_nodes)} chunks from graph store")
                
            except Exception as e:
                logger.warning(f"   ⚠ Graph retrieval failed: {e}")
        
        # Deduplicate by node_id if available
        seen_ids = set()
        unique_chunks = []
        for chunk in all_chunks:
            node_id = chunk.get('node_id')
            if node_id and node_id not in seen_ids:
                seen_ids.add(node_id)
                unique_chunks.append(chunk)
            elif not node_id:
                unique_chunks.append(chunk)
        
        # Sort by score (highest first)
        unique_chunks.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        # Limit to top_k
        final_chunks = unique_chunks[:request.top_k]
        
        logger.info(f"✅ Returning {len(final_chunks)} unique chunks")
        
        return RetrievalResponse(
            query=request.query,
            chunks=final_chunks,
            total_chunks=len(final_chunks),
            retrieval_method=" + ".join(methods_used) if methods_used else "none"
        )
        
    except Exception as e:
        logger.error(f"❌ Retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ingest", response_model=IngestResponse)
async def ingest_document(request: IngestRequest):
    """
    Ingest a document from the shared volume into Supabase
    """
    import re
    from llama_index.core import Document
    from llama_index.core.node_parser import SemanticSplitterNodeParser
    
    try:
        logger.info(f"📥 Starting ingestion of: {request.file_path}")
        
        # Load file from shared volume
        file_full_path = f"/data/shared/books/{request.file_path}"
        if not os.path.exists(file_full_path):
            raise HTTPException(status_code=404, detail=f"File not found: {request.file_path}")
        
        with open(file_full_path, 'r', encoding='utf-8') as f:
            book_text = f.read()
        
        # Extract metadata
        title_match = re.search(r'^\*\*([^\*]+?)\*\*', book_text, re.MULTILINE)
        author_match = re.search(r'^\*\*by ([^\*]+?)\*\*', book_text, re.MULTILINE)
        
        book_title = title_match.group(1).strip() if title_match else "Unknown Title"
        book_author = author_match.group(1).strip() if author_match else "Unknown Author"
        
        logger.info(f"   Book: {book_title} by {book_author}")
        
        # Create document
        document = Document(
            text=book_text,
            metadata={
                "book_title": book_title,
                "book_author": book_author,
                "file_path": request.file_path,
                "source": "api_ingest"
            }
        )
        
        # Semantic chunking
        logger.info("   Creating semantic chunks...")
        logger.info(f"   Embed model: {Settings.embed_model}")
        
        if Settings.embed_model is None:
            raise HTTPException(status_code=500, detail="Embedding model not initialized. Service may still be starting up.")
        
        splitter = SemanticSplitterNodeParser(
            embed_model=Settings.embed_model,
            breakpoint_percentile_threshold=95,
            buffer_size=1,
        )
        nodes = splitter.get_nodes_from_documents([document])
        logger.info(f"   ✓ Created {len(nodes)} chunks")
        
        # Store in Supabase
        logger.info("   Storing in Supabase...")
        postgres_password = "FGVUMISvP1NtSWJdKNtFkQBzl3aOsK8CW2ZDbNL-lb4"
        
        vector_store = SupabaseVectorStore(
            postgres_connection_string=f"postgresql://postgres:{postgres_password}@db:5432/postgres",
            collection_name="book_chunks",
            dimension=4096,
        )
        
        # Add nodes directly to vector store (bypass index creation)
        logger.info(f"   Adding {len(nodes)} nodes to vector store...")
        from llama_index.core.storage.storage_context import StorageContext
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        
        index = VectorStoreIndex(
            nodes,
            storage_context=storage_context,
            embed_model=Settings.embed_model,
            show_progress=False,
        )
        
        logger.info(f"✅ Ingestion complete: {len(nodes)} chunks stored")
        
        return IngestResponse(
            status="success",
            chunks_created=len(nodes),
            message=f"Successfully ingested '{book_title}' with {len(nodes)} chunks"
        )
        
    except Exception as e:
        logger.error(f"❌ Ingestion failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
