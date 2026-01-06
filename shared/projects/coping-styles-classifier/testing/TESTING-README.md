# Running Classification Tests with Ollama

## Overview

This test suite evaluates the 4 different classification prompts against 5 real-world test cases using multiple LLM models via Ollama.

**Key Features**:
- ✅ Tests in isolation (each LLM call has no prior context)
- ✅ Strips examples from prompts to prevent contamination
- ✅ Tests multiple models for comparison
- ✅ Automated scoring and comprehensive reporting

## Prerequisites

### 1. Install Ollama

```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Or download from: https://ollama.ai
```

### 2. Pull Models (Optional - script will prompt)

The script will test these models (strongest open-source options):

```bash
# Recommended models (pick at least 2-3):
ollama pull qwen2.5:32b          # Excellent reasoning, fast
ollama pull llama3.1:70b         # Meta's flagship, very capable
ollama pull mistral-large:123b   # Strong general purpose (large!)
ollama pull deepseek-r1:70b      # Good at analysis
```

**Note**: 70b+ models require significant RAM (32GB+). For testing on smaller machines, use:

```bash
ollama pull qwen2.5:14b          # Smaller but still capable
ollama pull llama3.1:8b          # Fast, good baseline
ollama pull mistral:7b           # Lightweight option
```

## Running the Tests

```bash
cd coping-styles
python3 run_ollama_tests.py
```

The script will:
1. ✅ Check Ollama is running
2. 📋 List available models and prompt to pull missing ones
3. 🧪 Run all test combinations (can take 30-60 minutes)
4. 💾 Save results as JSON and generate markdown report

## What Gets Tested

- **4 Prompts**:
  - `prompt-comprehensive.md` (full descriptions + keywords + examples)
  - `prompt-keywords-only.md` (keyword matching only)
  - `prompt-semantic-only.md` (lived experience descriptions)
  - `prompt-embodiment-only.md` (energetic/symbolic patterns)

- **5 Test Cases**:
  - Real statements with known diagnoses
  - Expected top 3 styles for each

- **Multiple Models**:
  - Tests same prompt across different LLMs
  - Reveals which models understand the framework best

## Scoring System

Each test case gets scored 0-10:

- **10 points**: All top 3 correct + high precision
- **7 points**: 2+ top 3 correct + good coverage
- **4 points**: Some matches but weak ranking
- **0 points**: Poor or no matches

**Metrics Tracked**:
- Precision (avoid false positives)
- Recall (capture all relevant styles)
- Top-3 accuracy (ranking quality)

## Output Files

After running, you'll get:

1. **`test-results-TIMESTAMP.json`**: Raw data
   - All responses from all models
   - Scores and metrics for each combination
   - Parseable for further analysis

2. **`test-report-TIMESTAMP.md`**: Human-readable report
   - Rankings by prompt
   - Rankings by model
   - Detailed breakdown
   - Recommendations

## Interpreting Results

### Prompt Performance

- **≥ 8.5/10**: Excellent, production-ready
- **7.0-8.4**: Good, may need minor refinement
- **5.0-6.9**: Needs work
- **< 5.0**: Rethink approach

### Model Consistency

- If ALL models score low: Prompt needs improvement
- If SOME models score high: Model selection matters
- If scores vary widely: Prompt may be ambiguous

## Important: Test Contamination Prevention

The script **automatically strips example classifications** from prompts before testing. This ensures:

- No memorization of test cases
- Fair comparison across prompts
- Valid assessment of actual understanding

## Troubleshooting

### Ollama Not Found
```bash
# Check Ollama is installed
ollama --version

# Start Ollama service (if needed)
ollama serve
```

### Model Download Fails
```bash
# Check available models
ollama list

# Manually pull
ollama pull MODEL_NAME
```

### Script Hangs
- Some 70b+ models are slow (2-5 min per test)
- Check Ollama logs: `ollama logs`
- Try smaller models first

### Parse Errors
- If models return non-JSON, script will mark as error
- Check `test-results-*.json` for raw responses
- Some models need prompt tuning

## Next Steps After Testing

1. **Review the report** - Which prompt performed best?
2. **Check model consistency** - Do results hold across models?
3. **Analyze failures** - Which test cases were hardest?
4. **Refine prompts** - Use insights to improve weak areas
5. **Re-test** - Iterate until performance threshold met

## Questions?

- Test methodology documented in `test-methodology.md`
- Test cases defined in `test-dataset.md`
- Prompts in `prompt-*.md` files

