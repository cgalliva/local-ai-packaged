# Source Data Directory

This directory contains all raw source materials that may be used for RAG ingestion, training, or prompt development.

## Current Sources

**Book:**
- `SOURCE CODE full manuscript 2025.docx.md` (107,027 words)
- Status: Ingested into RAG system

**Reference Taxonomy:**
- `word-clusters.md` - Coping styles classification framework
- Status: Available for RAG ingestion or prompt reference

**Training Examples:**
- `coping-styles-examples.jsonl` - Prompt/classification pairs for LLM training
- Format: JSON Lines (one example per line)
- Status: Collaborative, version-controlled training data

## How It Works

1. **Automatic Processing**: Place your data file (`.txt` or `.md`) here
2. **Auto-Metadata Extraction**: Title and author extracted from content
3. **Semantic Chunking**: RAG service handles intelligent text splitting
4. **Zero Configuration**: No manual metadata files needed

## Adding New Sources

```bash
# 1. Place file in this directory
cp your-file.md shared/data/

# 2. Run ingestion (edit run_ingestion.py to change file_path)
python3 rag-service/run_ingestion.py
```

The RAG service will automatically:
- ✅ Extract metadata from content
- ✅ Create semantic chunks
- ✅ Generate 4096-dimensional embeddings
- ✅ Store in Supabase pgvector

## Supported Formats

- **Markdown (`.md`)** - Recommended (preserves structure)
- **Plain text (`.txt`)** - Also works perfectly

## Working with Training Examples

**JSONL Format (coping-styles-examples.jsonl):**
```jsonl
{"prompt": "User's problem statement...", "coping_styles": ["Style1", "Style2"], "raw_diagnosis": "Style1, Style2", "metadata": {"source": "...", "validated": false}}
```

**Adding new examples:**
```bash
# Just append a new line to the file
echo '{"prompt": "New example...", "coping_styles": ["Frustrated"], ...}' >> shared/data/coping-styles-examples.jsonl

# Commit changes
git add shared/data/coping-styles-examples.jsonl
git commit -m "Add new training example"
```

**Reading in Python:**
```python
import jsonlines
with jsonlines.open('shared/data/coping-styles-examples.jsonl') as reader:
    for example in reader:
        print(example['prompt'], example['coping_styles'])
```

## Future Sources

Planned additions:
- Session transcripts
- Additional classification examples
- Coding session examples
- Audio transcripts

## Access from Services

All files accessible at:
- **Docker services**: `/data/shared/data/`
- **n8n workflows**: `/data/shared/data/`
- **Local development**: `./shared/data/`
