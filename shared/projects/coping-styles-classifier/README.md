# Coping Styles Classification Project

## Structure

```
shared/
├── data/                                           # Source materials
│   ├── word-clusters.md                            # Keyword taxonomy (source of truth)
│   └── SOURCE CODE full manuscript 2025.docx.md   # Book manuscript
│
└── projects/
    └── coping-styles-classifier/
        ├── 2026-01-01-comprehensive-baseline/      # First experiment: Full prompts
        │   ├── prompts/                            # All comprehensive prompt variations
        │   ├── results/                            # Test outputs (JSON, logs, reports)
        │   └── analysis/                           # Insights & comparisons
        │
        ├── 2026-01-02-keywords-experiments/        # Second experiment: Keywords-only
        │   ├── prompts/                            # Keyword-only variations
        │   ├── results/                            # Test outputs
        │   └── analysis/                           # What we learned about keywords
        │
        └── testing/                                # Reusable test infrastructure
            ├── run_ollama_tests.py                 # Main test runner (all styles)
            ├── run_limited_style_test.py           # Limited style test runner
            ├── test-dataset.md                     # Test cases with diagnoses
            └── test-methodology.md                 # Testing approach
```

## Naming Convention

Experiments use format: `YYYY-MM-NN-description`
- `YYYY-MM` = Year-Month
- `NN` = Sequence number (01, 02, 03...)
- `description` = What was tested

This allows multiple experiments per month while maintaining chronological order.

## Running Tests

### Full Test Suite (All 12 Styles)

Test one or more prompts with multiple models:

```bash
cd testing

# Test single prompt
python3 run_ollama_tests.py \
  ../2026-01-01-comprehensive-baseline/prompts/prompt-comprehensive.md \
  -o ../2026-01-01-comprehensive-baseline/results/

# Test multiple prompts
python3 run_ollama_tests.py \
  ../2026-01-01-comprehensive-baseline/prompts/*.md \
  -o ../2026-01-01-comprehensive-baseline/results/
```

### Limited Style Test (Subset of Styles)

For prompts with only a few styles defined:

```bash
cd testing

python3 run_limited_style_test.py \
  ../2026-01-02-keywords-experiments/prompts/prompt-keywords-with-shared.md \
  -o ../2026-01-02-keywords-experiments/results/
```

### Options

Both scripts support:
- `-o, --output`: Specify output directory for results (default: current directory)
- Multiple prompt files can be tested in sequence

## Source Data

- **Book Manuscript**: `shared/data/SOURCE CODE full manuscript 2025.docx.md`
- **Word Clusters**: `shared/data/word-clusters.md`

## Notes

- Experiments are time-boxed by available data (5 examples now, 30+ later)
- Old experiments stay as historical record, not for comparison
- When data improves significantly, start a new experiment folder

