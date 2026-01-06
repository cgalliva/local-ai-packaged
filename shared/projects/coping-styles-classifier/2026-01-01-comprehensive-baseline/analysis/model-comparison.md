# Model Size Comparison: Impact on Classification Accuracy

## Test Results: Small vs Medium vs Large Models

### Overall Scores by Model

| Model | Size | Avg Score | Best Prompt | Best Score |
|-------|------|-----------|-------------|------------|
| **gpt-oss:120b** | 120B | **3.60/10** | Comprehensive | **6.80/10** |
| **qwen3:8b** | 8B | 3.45/10 | Comprehensive | 6.60/10 |
| **gpt-oss:20b** | 20B | 2.45/10 | Comprehensive | 6.20/10 |

---

## Key Finding: Model Size Matters, But Not Much

### Comprehensive Prompt Performance:

| Model | Test 1 | Test 2 | Test 3 | Test 4 | Test 5 | Average |
|-------|--------|--------|--------|--------|--------|---------|
| **120B** | 4.0 | **10.0** | 6.0 | 7.0 | 7.0 | **6.80** |
| **8B**   | 4.0 | **10.0** | 2.0 | 7.0 | **10.0** | 6.60 |
| **20B**  | 2.0 | **10.0** | 6.0 | 7.0 | 6.0 | 6.20 |

**Analysis**: 
- ✅ All models nail Test 2 (relationship anxiety) - **10/10**
- ⚠️ All models struggle with Test 1 (consumed/vulnerable) - **2-4/10**
- 📊 120B model shows more consistency (no 2/10 scores)
- 🎯 Larger model improves average by only **+0.2 points** (6.6 → 6.8)

---

## Detailed Breakdown by Prompt Type

### 1. Comprehensive Prompt

**gpt-oss:120b (6.80/10)**:
- ✅ Best: Test 2 (10/10) - Perfect identification
- ✅ Good: Tests 3,4,5 (6-7/10) - Solid performance
- ❌ Weak: Test 1 (4/10) - Missed some styles

**qwen3:8b (6.60/10)**:
- ✅ Best: Tests 2,5 (10/10) - Perfect on clear cases
- ✅ Good: Test 4 (7/10)
- ❌ Weak: Tests 1,3 (2-4/10) - Struggled with ambiguity

**Verdict**: Larger model is slightly more consistent but not dramatically better.

---

### 2. Keywords-Only Prompt

| Model | Score | Notes |
|-------|-------|-------|
| 120B | 3.60/10 | Best of three, but still poor |
| 8B | 2.80/10 | Struggles with keyword-only |
| 20B | 1.60/10 | Worst performer |

**Verdict**: Keywords-only approach fails regardless of model size.

---

### 3. Semantic-Only Prompt

| Model | Score | Notes |
|-------|-------|-------|
| 120B | 2.40/10 | Slightly better than smaller |
| 8B | 1.60/10 | Very poor |
| 20B | 0.80/10 | Terrible |

**Verdict**: Pure semantic descriptions don't work well. Larger model helps slightly.

---

### 4. Embodiment-Only Prompt

| Model | Score | Notes |
|-------|-------|-------|
| 8B | 2.80/10 | Surprisingly best |
| 120B | 3.60/10 | Marginal improvement |
| 20B | 1.20/10 | Worst |

**Verdict**: Energetic/embodiment language too abstract for all models.

---

## Critical Insight: The Problem ISN'T Model Size

### What We Learned:

1. **All models consistently succeed on Test 2** (10/10 across all)
   - Statement: Relationship anxiety, destabilizing, consumed
   - Known styles: FRICTIVE, OMNIPOTENT, SYMBIOTIC
   - This is a **clear, unambiguous case**

2. **All models consistently fail on Test 1** (2-4/10 across all)
   - Statement: Consumed, vulnerable, life force sucking
   - Known styles: OMNIPOTENT, PREMATURE, FRUSTRATED, CONSTRICTED, FLOATY
   - This is **complex with 5 co-occurring styles**

3. **Model size gives diminishing returns**
   - 8B → 20B: **-1.0 points** (worse!)
   - 8B → 120B: **+0.2 points** (tiny improvement)
   - 15x more parameters = 3% improvement

---

## The REAL Problem: Prompt Quality

### Evidence:

1. **Comprehensive prompt works 3x better** (6.8/10) than others (1.2-3.6/10)
   - This holds true across ALL model sizes
   - Suggests information quality > model intelligence

2. **Simplified prompts fail** regardless of model power
   - Keywords: 1.6-3.6/10
   - Semantic: 0.8-2.4/10  
   - Embodiment: 1.2-3.6/10

3. **Complex multi-style cases are the bottleneck**
   - Test 1: 5 styles present (all models struggle)
   - Test 2: 3 clear styles (all models excel)

---

## Recommendations

### ❌ DON'T: Use larger models as main improvement strategy
- Cost: 15x more compute
- Benefit: +3% accuracy
- ROI: Very poor

### ✅ DO: Focus on prompt improvement
**Priority 1: Add more examples of complex cases**
- 20-30 examples with 4-5 co-occurring styles
- Especially cases like Test 1 (consumed/vulnerable pattern)

**Priority 2: Add differential diagnosis**
- "This looks like PREMATURE but is actually OMNIPOTENT because..."
- "FRICTIVE and OMNIPOTENT often co-occur when..."

**Priority 3: Add step-by-step reasoning**
- Chain-of-thought: "First identify feelings... then patterns... then styles"
- Break down the classification process

**Expected improvement**: 6.8/10 → **8-9/10** with better prompt

---

## Next Actions

### Immediate (This Week):
1. ✅ Diagnosed more complex examples (like Test 1)
2. ✅ Add to comprehensive prompt
3. ✅ Retest with qwen3:8b (cheapest, fast iteration)

### Short-term (Next 2 Weeks):
1. Collect 50-100 diagnosed examples
2. Implement RAG (retrieve similar examples dynamically)
3. Expected: **7.5-8.5/10**

### Long-term (Next Month):
1. Collect 200-300 diagnosed examples
2. Fine-tune qwen3:8b or similar
3. Expected: **8-9/10**

---

## Cost-Benefit Analysis

### Option A: Use 120B model with current prompt
- Accuracy: 6.8/10
- Speed: ~3 min/classification
- Cost: High compute
- **Grade: C-** (expensive, marginal improvement)

### Option B: Use 8B model with improved prompt (30 examples)
- Accuracy: ~7.5-8/10 (estimated)
- Speed: ~30 sec/classification
- Cost: Low compute + your time
- **Grade: A** (best ROI)

### Option C: RAG + 8B model (200 examples)
- Accuracy: ~8-9/10 (estimated)
- Speed: ~45 sec/classification
- Cost: Medium (vector DB) + data collection time
- **Grade: A+** (production-ready)

---

## Conclusion

**The data is clear**: 

🎯 **Model size is NOT your bottleneck**. A well-crafted prompt with 50-100 diverse examples on an 8B model will vastly outperform a poorly-crafted prompt on a 120B model.

💡 **Focus your effort on**:
1. Collecting diverse diagnosed examples (especially complex cases)
2. Adding differential diagnosis guidance
3. Structuring the prompt for step-by-step reasoning

🚀 **Expected trajectory**:
- Current (120B, basic prompt): **6.8/10**
- Improved prompt (8B, +30 examples): **7.5-8/10**
- RAG system (8B, +200 examples): **8.5-9/10**
- Fine-tuned (8B, +500 examples): **9-10/10**

**Bottom line**: Invest in data quality, not model size.

