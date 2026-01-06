# RAG System Documentation

## Overview

State-of-the-art Retrieval-Augmented Generation (RAG) system for semantic search and question-answering over a large book corpus.

**Architecture**: Supabase (pgvector) for vector storage + FastAPI retrieval service + n8n for agent workflows

## Key Features

✅ **Semantic Chunking**: Intelligent text splitting using LlamaIndex  
✅ **High-dimensional Embeddings**: 4096-dimensional vectors via `qwen3-embedding:8b` (Ollama)  
✅ **Automatic Metadata Extraction**: Book title, author extracted from content  
✅ **Optimized for Single Large Document**: 107,000+ words, semantically chunked  
✅ **Retrieval-Only Service**: Designed to be called by n8n agent for generation  

## Quick Start

### 1. Start Services

```bash
docker compose up -d
```

### 2. Ingest Book

```bash
# Place your book in: shared/books/your-book.md
# Then run from project root:
python3 rag-service/run_ingestion.py
```

This will:
- Load the book from `shared/books/`
- Extract metadata automatically
- Create semantic chunks using LlamaIndex
- Generate 4096-dimensional embeddings via Ollama
- Store in Supabase pgvector

### 3. Query via n8n

Import workflow: `n8n/workflows/rag-retrieval-generation.json`

**Workflow steps**:
1. User sends query
2. Call `/retrieve` endpoint → get relevant chunks
3. Call Ollama `qwen3:30b` with chunks + query → generate answer

## API Endpoints

### Health Check
```bash
GET http://localhost/rag/health
```

Returns service status and chunk count.

### Retrieve
```bash
POST http://localhost/rag/retrieve
{
  "query": "your question here",
  "top_k": 5
}
```

Returns relevant chunks with metadata and similarity scores.

### Ingest
```bash
POST http://localhost/rag/ingest
{
  "file_path": "your-book.md"
}
```

Triggers semantic chunking and ingestion (long-running).

## Architecture

```
┌─────────────┐
│   n8n       │ ← User interacts here
│   Agent     │
└──────┬──────┘
       │
       ├─→ /retrieve (RAG Service)
       │   └─→ Supabase pgvector (4096-dim vectors)
       │
       └─→ Ollama qwen3:30b (Generation)
```

## Technical Stack

- **Embeddings**: Ollama `qwen3-embedding:8b` (4096 dimensions, runs natively)
- **Vector DB**: Supabase with pgvector extension
- **Chunking**: LlamaIndex SemanticSplitterNodeParser
- **API**: FastAPI (retrieval-only)
- **Orchestration**: Docker Compose
- **Workflows**: n8n (retrieval + generation)

## Future Enhancements (Optional)

### Graph Database Integration
Currently **NOT implemented** - vector-only retrieval is sufficient for single-document use case.

**Would add value if**:
- Expanding to multiple books/sources
- Need multi-hop reasoning across chapters
- Require explicit entity relationship tracking
- Want explainable retrieval paths

**To implement**: Uncomment Neo4j sections in `docker-compose.yml` and `app.py`

## Configuration

Key environment variables in `docker-compose.yml`:

```yaml
OLLAMA_HOST: http://host.docker.internal:11434  # Native Ollama
EMBEDDING_MODEL: qwen3-embedding:8b
LLM_MODEL: qwen3:30b
SUPABASE_URL: http://kong:8000
```

## Project Structure

```
sc-ai-demo/
├── docker-compose.yml          # Service orchestration
├── rag-service/
│   ├── app.py                  # FastAPI retrieval service
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile
│   ├── run_ingestion.py        # Helper script for ingestion
│   └── RAG-SYSTEM.md          # This documentation
├── n8n/workflows/
│   └── rag-retrieval-generation.json  # Working workflow
└── shared/books/
    └── SOURCE CODE full manuscript 2025.docx.md  # Your book
```

## Troubleshooting

### Check Service Health
```bash
curl http://localhost/rag/health
```

### Check Chunk Count
Healthy system should show `chunks_in_db > 0`

### Reingest Book
If chunks are lost:
1. Drop table: `DROP TABLE vecs.book_chunks;`
2. Restart RAG service: `docker restart sc-ai-rag-service`
3. Run ingestion: `python3 rag-service/run_ingestion.py`

## Performance

- **Ingestion**: ~30-45 minutes for 107K word book (semantic chunking + embeddings)
- **Retrieval**: <1 second for top-5 chunks
- **Accuracy**: SOTA for single-document RAG with semantic chunking + high-dimensional embeddings

## Development Notes

- Ollama runs **natively** (not in Docker) - ensure it's running before starting services
- Embedding dimension is **4096** (verified via Ollama API)
- Supabase accessed directly via `db:5432` (not Kong proxy for internal connections)
- RAG service **only does retrieval** - generation happens in n8n

