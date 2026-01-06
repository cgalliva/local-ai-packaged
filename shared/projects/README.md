# Projects Directory

This directory contains active development and testing projects that use the source data in `shared/data/`.

## Current Projects

### Coping Styles Classifier
- **Location**: `coping-styles-classifier/`
- **Purpose**: LLM-based classification of coping mechanisms from user input
- **Status**: Active testing and prompt optimization
- **Source Data**: Uses `../data/word-clusters.md` as reference taxonomy

**Project Structure:**
```
coping-styles-classifier/
├── 2026-01-01-comprehensive-baseline/  # Initial experiments
│   ├── prompts/
│   ├── results/
│   └── analysis/
├── 2026-01-02-keywords-experiments/    # Keyword-focused iteration
│   ├── prompts/
│   ├── results/
│   └── analysis/
└── testing/                             # Testing infrastructure
    ├── test_prompts.py
    ├── test-dataset.md
    └── TESTING-README.md
```

## Future Projects

Potential additions:
- Session transcript analysis
- Multi-modal classification
- LLM fine-tuning experiments
- RAG optimization tests

## Access from Services

All files accessible at:
- **Docker services**: `/data/shared/projects/`
- **n8n workflows**: `/data/shared/projects/`
- **Local development**: `./shared/projects/`
