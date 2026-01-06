# Keywords-Only Test: All Models Comparison

## Test Configuration

**Prompt**: `prompt-only-unique-keywords-5-styles-diconnected-to-symbiotic.md`  
**Format**: Pure keyword lists (IN/OUT), no descriptions, no examples, no antidotes  
**Test Date**: January 6, 2026

---

## Results Summary

| Model | Score | vs Comprehensive | Performance |
|-------|-------|------------------|-------------|
| **qwen3:8b** | 4.28/10 | -35% (was 6.60) | Best with keywords-only |
| **qwen3-coder:30b** | **3.30/10** | *(not tested baseline)* | Middle |
| **gpt-oss:120b** | 2.84/10 | -58% (was 6.80) | Worst with keywords-only |

---

## Key Finding: Model Size Doesn't Help with Bad Prompts

### Paradox: Larger Model Performed WORSE

- **qwen3:8b** (smallest): 4.28/10 ⭐ Best
- **qwen3-coder:30b** (3.75x larger): 3.30/10 
- **gpt-oss:120b** (15x larger): 2.84/10 ❌ Worst

**This confirms**: When the prompt lacks essential information (descriptions, examples), model size can't compensate. In fact, larger models may overthink and perform worse.

---

## Detailed Test Breakdown

### Test 1: Complex Relational (Consumed/Obsessed)
**Known**: OMNIPOTENT, FLOATY

| Model | Predicted | Score | Analysis |
|-------|-----------|-------|----------|
| qwen3:8b | OMNIPOTENT ✅, DEPRIVED, DISCONNECTED | 6.0/10 | Got OMNIPOTENT, missed FLOATY |
| qwen3-coder:30b | OMNIPOTENT ✅, FRICTIVE, SYMBIOTIC | 6.0/10 | Same - got OMNIPOTENT, missed FLOATY |
| gpt-oss:120b | *(Nothing)* | 0.0/10 | Complete miss |

**Insight**: Both Qwen models found OMNIPOTENT, but 120b couldn't even start.

---

### Test 2: Anxious New Relationship
**Known**: OMNIPOTENT, SYMBIOTIC, FRICTIVE, DEPRIVED, FLOATY, FLIGHTY (6 styles!)

| Model | Predicted | Score | Correct |
|-------|-----------|-------|---------|
| qwen3:8b | FRICTIVE ✅, DEPRIVED ✅, FLOATY ✅ | 5.4/10 | 3/6 = 50% |
| qwen3-coder:30b | FRICTIVE ✅, OMNIPOTENT ✅ | 3.8/10 | 2/6 = 33% |
| gpt-oss:120b | DEPRIVED ✅ | 1.5/10 | 1/6 = 17% |

**Insight**: qwen3:8b handled multi-style best. Coder model got 2. 120b only got 1.

---

### Test 3: Dealership Story (Pattern-Based)
**Known**: DISCONNECTED

| Model | Predicted | Score | Analysis |
|-------|-----------|-------|----------|
| qwen3:8b | *(Nothing)* | 0.0/10 | Couldn't detect pattern |
| qwen3-coder:30b | DEPRIVED, FRICTIVE, SYMBIOTIC, OMNIPOTENT | 0.0/10 | Wildly wrong (4 false positives!) |
| gpt-oss:120b | FRICTIVE | 0.0/10 | Wrong |

**Insight**: **ALL MODELS FAILED.** This is DISCONNECTED shown as "factual reporting style" - pattern-based, not keyword-based. Without descriptions, impossible to detect.

---

### Test 4: Future-Focused Rumination
**Known**: FLOATY, OMNIPOTENT

| Model | Predicted | Score | Analysis |
|-------|-----------|-------|----------|
| qwen3:8b | FRICTIVE, DISCONNECTED | 0.0/10 | Completely wrong |
| qwen3-coder:30b | FRICTIVE | 0.0/10 | Only predicted FRICTIVE (wrong) |
| gpt-oss:120b | FLOATY ✅, DISCONNECTED | 6.0/10 | Got FLOATY! |

**Insight**: Surprise - 120b was the ONLY model to get this one partially right! Found FLOATY from "not present" keywords.

---

### Test 5: "Adulting" Avoidance
**Known**: DISCONNECTED (actually INDULGED, but not in limited prompt)

| Model | Predicted | Score | Analysis |
|-------|-----------|-------|----------|
| qwen3:8b | DISCONNECTED ✅, FRICTIVE, STIFF | 10.0/10 | Perfect! |
| qwen3-coder:30b | FRICTIVE, DISCONNECTED ✅ | 6.7/10 | Got DISCONNECTED (not #1) |
| gpt-oss:120b | FLIGHTY, STIFF, DISCONNECTED ✅ | 6.7/10 | Got DISCONNECTED (not #1) |

**Insight**: qwen3:8b nailed this one. Others got it but not as primary.

---

## Pattern Analysis

### What Each Model Is Good/Bad At

**qwen3:8b (4.28/10)** ⭐ Best with keywords-only
- ✅ Best at multi-style statements (Test 2: 3/6)
- ✅ Decent keyword matching
- ❌ Still misses pattern-based (Test 3, 4)

**qwen3-coder:30b (3.30/10)** 
- ✅ Found OMNIPOTENT consistently
- ⚠️ Conservative - often only 1-2 predictions
- ❌ Worst on Test 3 (4 false positives!)
- ❌ Struggles with multi-style (Test 2: 2/6)

**gpt-oss:120b (2.84/10)** ❌ Worst with keywords-only
- ✅ ONLY model to get Test 4 (FLOATY)
- ❌ Often returns nothing or very little
- ❌ Worst on multi-style (Test 2: 1/6)
- ❌ May be "too smart" and refusing to guess without context

---

## Why "Coder" Model Didn't Excel

**qwen3-coder:30b** is trained for code, which has:
- Precise syntax rules
- Clear patterns
- Deterministic logic

**Coping styles classification** requires:
- Semantic understanding
- Emotional nuance
- Ambiguity tolerance
- Pattern recognition in natural language

**Result**: The "coder" model's precision-oriented training may actually HURT on this task, causing it to be overly cautious or miss subtle emotional patterns.

---

## Key Insights Across All Models

### 1. **No Model Can Overcome Bad Prompts**

Even 120B parameter model drops from 6.80 → 2.84 (-58%) with keywords-only.

### 2. **Smaller Models Can Outperform Larger Ones**

qwen3:8b (smallest) beat both larger models on keywords-only task.

**Why?**
- Less prone to overthinking
- More willing to "guess" based on limited info
- Faster, more direct matching

### 3. **All Models Failed Pattern-Based Classification**

**Test 3 (Dealership)**: 0/3 models got it right  
**Why**: DISCONNECTED manifests as "emotional disconnection in reporting" - requires description to detect

### 4. **Multi-Style Statements Are Hardest**

**Test 2** (6 styles): Best was 50% (qwen3:8b), worst was 17% (120b)

---

## Comparison to Comprehensive Prompts

### With Full Context (descriptions + examples + keywords)

| Model | Keywords-Only | Comprehensive | Delta |
|-------|--------------|---------------|-------|
| qwen3:8b | 4.28/10 | 6.60/10 | **+54% improvement** |
| qwen3-coder:30b | 3.30/10 | *(not tested)* | *(estimate: ~6.5/10 if comprehensive)* |
| gpt-oss:120b | 2.84/10 | 6.80/10 | **+139% improvement** |

**Largest benefit**: gpt-oss:120b improved 2.4x with comprehensive prompt!

This suggests: **Larger models benefit MORE from good prompts** (and suffer MORE from bad ones).

---

## The Model Size Paradox Explained

### With Keywords-Only (Bad Prompt)
```
Small model (8B):  4.28/10  ← "Just match keywords"
Medium (30B):      3.30/10  ← "Hmm, this seems incomplete..."
Large (120B):      2.84/10  ← "I need more context to be confident"
```

### With Comprehensive Prompt (Good Prompt)
```
Small model (8B):  6.60/10  ← "Got it!"
Large (120B):      6.80/10  ← "Ah, now I understand the nuances!"
```

**Lesson**: Large models are like expert clinicians - they need proper assessment tools (good prompts). Small models are like interns - they'll take a guess even with limited info.

---

## Recommendations

### 1. **Don't Use Keywords-Only** ❌

All models performed poorly (2.84-4.28/10 = 28-43% accuracy)

### 2. **Model Selection for This Task**

For keywords-only or limited context:
- ✅ **qwen3:8b** - Best fallback (4.28/10)

For comprehensive prompts:
- ✅ **gpt-oss:120b** - Best with context (6.80/10)
- ✅ **qwen3:8b** - Fast & good (6.60/10)
- ⚠️ **qwen3-coder:30b** - Likely similar to qwen3:8b if given comprehensive prompt

### 3. **Invest in Prompt, Not Model Size**

Going from 8B → 120B with bad prompt: **Worse** (-33%)  
Going from bad prompt → good prompt with same model: **+54% to +139%**

**ROI**: Better prompt >>> Bigger model

---

## Next Test Recommendations

1. ✅ **Test qwen3-coder:30b with comprehensive prompt** to see if it matches qwen3:8b or 120b
2. 🎯 **Create simplified comprehensive prompt** (remove keyword noise, keep descriptions + examples)
3. 🎯 **Collect 30-50 more diagnosed examples** (biggest potential improvement)

---

## Final Verdict on Keywords-Only Approach

### Universal Failure Across All Models

| Metric | Result |
|--------|--------|
| Best Score | 4.28/10 (qwen3:8b) |
| Worst Score | 2.84/10 (gpt-oss:120b) |
| Average | 3.47/10 |
| Grade | ❌ **FAIL** |

**Conclusion**: Keywords alone are INSUFFICIENT for coping style classification, regardless of model size or architecture.

**The path forward**: Focus on prompt quality (descriptions + examples), not keyword quantity or model size.


