# Keywords Test: With vs Without Shared Keywords

## Test Configuration

**Test Date**: January 6, 2026  
**Format**: Pure keyword lists (IN/OUT), no descriptions, no examples, no antidotes

**Two Prompts Tested:**
1. **Keywords-Only**: Core keywords only
2. **Keywords + Shared**: Core + shared/overlapping keywords

---

## 🚨 SURPRISING RESULT: Model-Specific Impact!

| Model | Keywords-Only | + Shared Keywords | Change |
|-------|--------------|-------------------|---------|
| **qwen3:8b** | 4.28/10 | **6.52/10** | **+52% ✅ IMPROVEMENT!** |
| **qwen3-coder:30b** | 3.30/10 | 4.77/10 | +45% ⚠️ improved |
| **gpt-oss:120b** | 2.84/10 | 4.44/10 | +56% ⚠️ improved |

### Key Finding: More Keywords HELPED (When Used Without Other Context)

Surprisingly, adding shared/overlapping keywords **improved performance across ALL models** when using keywords-only prompts!

**This contradicts our earlier finding** that adding more keywords to comprehensive prompts hurt performance.

---

## Why This Happened: Context Matters

### Earlier Test (Comprehensive Prompts):
```
Comprehensive (descriptions + examples + core keywords): 6.60-6.80/10
+ Adding exhaustive keywords: 5.40-6.60/10 ❌ WORSE (-18%)
```
**Problem**: Information overload when descriptions already provide context

### This Test (Keywords-Only Prompts):
```
Keywords-only (core): 2.84-4.28/10
+ Adding shared keywords: 4.44-6.52/10 ✅ BETTER (+45-56%)
```
**Benefit**: More data points help when that's ALL the model has

---

## Test-by-Test Analysis

### Test 1: Complex Relational (Consumed/Obsessed)
**Known**: OMNIPOTENT, FLOATY

| Model | Core Only | + Shared | Analysis |
|-------|-----------|----------|----------|
| qwen3:8b | 6.0/10 (OMNIPOTENT) | 0.0/10 (wrong) | **Worse!** More keywords confused it |
| qwen3-coder | 6.0/10 (OMNIPOTENT) | 6.0/10 (OMNIPOTENT) | Same |
| gpt-oss:120b | 0.0/10 (nothing) | 0.0/10 (DEPRIVED) | Still struggling |

---

### Test 2: Anxious New Relationship (Multi-style)
**Known**: OMNIPOTENT, SYMBIOTIC, FRICTIVE, DEPRIVED, FLOATY, FLIGHTY (6 styles!)

| Model | Core Only | + Shared | Found |
|-------|-----------|----------|-------|
| qwen3:8b | 5.4/10 (3/6) | 4.6/10 (4/6) | Actually found more but ranking off |
| qwen3-coder | 3.8/10 (2/6) | 3.8/10 (2/6) | Same |
| gpt-oss:120b | 1.5/10 (1/6) | 1.5/10 (1/6) | Still struggling |

---

### Test 3: Dealership Story (Pattern-Based) ⭐ BREAKTHROUGH
**Known**: DISCONNECTED

| Model | Core Only | + Shared | Analysis |
|-------|-----------|----------|----------|
| qwen3:8b | 0.0/10 (nothing) | **10.0/10 ✅** | **SOLVED IT!** |
| qwen3-coder | 0.0/10 (4 wrong) | **10.0/10 ✅** | **SOLVED IT!** |
| gpt-oss:120b | 0.0/10 (FRICTIVE) | **10.0/10 ✅** | **SOLVED IT!** |

**ALL THREE MODELS** went from complete failure → perfect score!

**Why?** Adding shared keywords like "distant," "doesn't care," "doesn't listen" gave enough clues to detect the DISCONNECTED pattern in factual reporting style.

---

### Test 4: Future-Focused Rumination
**Known**: FLOATY, OMNIPOTENT

| Model | Core Only | + Shared | Analysis |
|-------|-----------|----------|----------|
| qwen3:8b | 0.0/10 (wrong) | **8.0/10** ✅ | Got both! |
| qwen3-coder | 0.0/10 (FRICTIVE) | 4.0/10 | Got FLOATY |
| gpt-oss:120b | 6.0/10 (FLOATY) | 4.0/10 | Got FLOATY |

---

### Test 5: "Adulting" Avoidance
**Known**: DISCONNECTED

| Model | Core Only | + Shared | Analysis |
|-------|-----------|----------|----------|
| qwen3:8b | 10.0/10 ✅ | **10.0/10** ✅ | Still perfect |
| qwen3-coder | 6.7/10 | 0.0/10 ❌ | **Worse!** Predicted FRICTIVE |
| gpt-oss:120b | 6.7/10 | 6.7/10 | Same |

---

## Key Insights

### 1. **The "Information Sweet Spot" Hypothesis**

```
Too Little Info (core keywords only):
  ├─ 2.84-4.28/10 ❌ Not enough to disambiguate
  
Sweet Spot (core + shared keywords):
  ├─ 4.44-6.52/10 ⚠️ Better, but still limited
  
Too Much Info (comprehensive + exhaustive keywords):
  ├─ 5.40-6.60/10 ⚠️ Information overload
  
Optimal (comprehensive + core keywords only):
  └─ 6.60-6.80/10 ✅ Best balance
```

### 2. **Test 3 Breakthrough: Pattern Detection**

**The biggest win**: ALL models solved Test 3 (Dealership story) when shared keywords were added.

**Before** (core only): 0/3 models correct  
**After** (+ shared): 3/3 models correct ✅

This pattern-based case (DISCONNECTED shown as emotional disconnection in factual reporting) became detectable when "doesn't care," "doesn't listen," "distant" were added.

**Lesson**: Shared keywords can reveal patterns that core keywords alone miss.

### 3. **Model-Specific Behavior**

**qwen3:8b** (Largest improvement: +52%)
- Benefited most from additional keywords
- Willing to use overlap clues
- Better at aggregating multiple weak signals

**qwen3-coder:30b** (+45%)
- Moderate improvement
- Still conservative in predictions
- Benefits from more data but doesn't maximize it

**gpt-oss:120b** (+56%)
- Second largest improvement
- Was refusing to guess with limited data
- More keywords gave it confidence to respond

---

## Why This Differs from Earlier Findings

### Comprehensive Prompt Test (descriptions + examples):
**Adding MORE keywords = -18% to -35% performance**

**Why it hurt:**
- Models already had rich context from descriptions
- Extra keywords created noise and confusion
- "Too many cooks in the kitchen"
- Overlapping keywords without context = ambiguity

### Keywords-Only Test:
**Adding MORE keywords = +45% to +56% performance**

**Why it helped:**
- Keywords were THE ONLY information available
- More keywords = more clues to work with
- Overlapping keywords revealed cross-style patterns
- "Any port in a storm" - models used whatever they had

---

## The Comprehensive Comparison

### All Approaches Ranked:

| Approach | qwen3:8b | gpt-oss:120b | Average | Rank |
|----------|----------|--------------|---------|------|
| **Comprehensive** | 6.60 | 6.80 | **6.70** | 🥇 **Best** |
| **Keywords + Shared** | 6.52 | 4.44 | **5.48** | 🥈 |
| **Comprehensive + MORE** | 5.40 | 6.60 | **6.00** | 🥉 |
| **Keywords-Only (core)** | 4.28 | 2.84 | **3.56** | 4th |

**Clear winner**: Comprehensive prompt (descriptions + examples + core keywords)

---

## Practical Implications

### 1. **For Keywords-Only Approaches**

If you MUST use keywords-only (no descriptions/examples):
- ✅ **DO** include shared/overlapping keywords
- ✅ **DO** add as many relevant keywords as possible
- ⚠️ Performance ceiling: ~6.5/10 (still significantly worse than comprehensive)

### 2. **For Comprehensive Approaches**

If using descriptions + examples:
- ✅ **DO** use core keywords (top 10-15 per style)
- ❌ **DON'T** add exhaustive keyword lists
- ❌ **DON'T** include detailed cross-references
- Focus on quality over quantity

### 3. **The Goldilocks Principle**

```
Too Little: Core keywords alone (3.5/10)
├─ Not enough information to classify accurately

Too Much: Comprehensive + exhaustive keywords (5.4-6.6/10)
├─ Information overload creates confusion

Just Right: Comprehensive + core keywords (6.6-6.8/10)
└─ Optimal balance of context and precision
```

---

## Unexpected Finding: qwen3:8b Outperforms 120B

**With Keywords + Shared:**
- qwen3:8b: 6.52/10 🥇
- qwen3-coder:30b: 4.77/10
- gpt-oss:120b: 4.44/10 (worst!)

**Why smaller model wins:**
- Smaller models aggregate keywords more aggressively
- Less overthinking with limited information
- More willing to use partial matches
- "Simple heuristics work when data is limited"

**Large models need context** to perform optimally. With keywords-only, they're handicapped.

---

## Test 3 Success Story

**The Dealership Story** was the litmus test for pattern recognition.

**With Core Keywords Only:**
- All 3 models: **0/3 correct** ❌

**With Shared Keywords Added:**
- All 3 models: **3/3 correct** ✅

**What changed?**

Added keywords that capture emotional disconnection:
- "doesn't care"
- "doesn't listen"  
- "distant"
- "doesn't hear"
- "unreachable"

These weren't in the statement directly, but their absence (factual reporting without emotional expression) became detectable as a pattern when models knew these were DISCONNECTED indicators.

---

## Recommendations

### 1. **Primary Path: Use Comprehensive Prompts**

Don't settle for 6.5/10 when 6.8/10 is achievable:
- Descriptions + Examples + Core Keywords = **Best performance**
- Keywords alone (even with shared) = **Significant accuracy loss**

### 2. **If Limited to Keywords-Only**

Maximize performance by:
- ✅ Include shared/overlapping keywords
- ✅ Use qwen3:8b (best performer at 6.52/10)
- ✅ Add as many relevant keywords as possible
- ⚠️ Accept ~35% accuracy ceiling vs. comprehensive

### 3. **For Production Systems**

**Don't use keywords-only.** The 6.5 vs 6.8 might seem small, but:
- 6.5/10 = 65% accuracy (1 in 3 misclassifications)
- 6.8/10 = 68% accuracy (borderline acceptable)
- With 30+ examples: estimated 8-8.5/10 (85% accuracy)

---

## Final Verdict

### Main Finding: Context-Dependent Keyword Impact

**Keywords hurt when**: Used with comprehensive prompts (creates noise)  
**Keywords help when**: Used alone (provides needed data)

### Optimal Strategy:

```
1. Start with comprehensive prompt (descriptions + examples)
2. Use CORE keywords only (top 10-15 per style)
3. Don't add exhaustive keyword lists or detailed cross-refs
4. Focus on collecting 30-50 diagnosed examples ← Biggest ROI
```

### Never Use:

```
❌ Keywords-only (core or shared) - 35% worse than comprehensive
❌ Comprehensive + exhaustive keywords - 18% worse than optimal
```

---

## The Complete Picture

```
Performance Hierarchy:

6.80 ┤                        ● Comprehensive (optimal)
     │
6.52 ┤                    ● Keywords + Shared (qwen3:8b)
     │
6.00 ┤               ● Comprehensive + MORE keywords
     │
4.77 ┤          ● Keywords + Shared (coder)
     │
4.44 ┤         ● Keywords + Shared (120b)
     │
4.28 ┤     ● Keywords-only core (qwen3:8b)
     │
3.30 ┤  ● Keywords-only core (coder)
     │
2.84 ┤ ● Keywords-only core (120b)
     │
     └────────────────────────────────────
      Keywords-Only  vs  Comprehensive
```

**Conclusion**: Comprehensive prompts win decisively. Keywords alone (even enhanced) remain significantly inferior.


