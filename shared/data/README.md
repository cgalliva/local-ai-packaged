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
{
  "prompt": "User's problem statement...",
  "coping_styles": ["Style1", "Style2"],
  "code": "category_name",
  "raw_diagnosis": "Professional diagnosis text (optional, to be added)",
  "metadata": {
    "source": "...",
    "validated": false,
    "date_added": "2026-01-06",
    "note": "Additional context"
  }
}
```

**Fields:**
- `prompt` - The user's problem statement (required)
- `coping_styles` - Array of identified coping styles (required)
- `code` - Category/grouping code for the example (optional but recommended)
- `raw_diagnosis` - Professional diagnosis text (optional, add after review)
- `metadata` - Source, validation status, notes

**Adding new examples:**
```bash
# Interactive helper script (recommended)
cd shared/projects/coping-styles-classifier
python add_example.py

# Or non-interactive
python add_example.py --prompt "User statement..." --styles "Frustrated,Disconnected" --code "work_stress"

# Then commit
git add ../../data/coping-styles-examples.jsonl
git commit -m "Add new training example: work_stress"
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
