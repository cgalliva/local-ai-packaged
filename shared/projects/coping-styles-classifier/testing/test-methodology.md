# Testing Methodology for Classification Prompts

## Overview
We will test 4 different prompt approaches against 5 known-diagnosis statements to determine which performs best.

---

## Prompts to Test

1. **prompt-comprehensive.md** - Full descriptions + keywords + examples + differentiations
2. **prompt-keywords-only.md** - Pure keyword matching
3. **prompt-semantic-only.md** - Lived experience descriptions only
4. **prompt-embodiment-only.md** - Energetic/coding language from curriculum

---

## Testing Process

### Phase 1: Individual Prompt Testing
For each prompt, run all 5 test cases and record:
- Classifications returned
- Confidence scores
- Time to generate (if measurable)
- Token usage (if measurable)

### Phase 2: Scoring
Use the scoring system from test-dataset.md:
- Calculate score for each test case (0-10 points)
- Average across all 5 cases
- Note specific strengths/weaknesses

### Phase 3: Analysis
For each prompt, analyze:
- **Precision**: % of known diagnoses correctly identified
- **Recall**: % of total diagnoses found
- **False Positive Rate**: % of incorrect additions
- **Differentiation Success**: Did it correctly distinguish:
  - INDULGED vs FRUSTRATED?
  - FLOATY vs INDULGED?
  - OMNIPOTENT vs FRUSTRATED?
  - PREMATURE vs INDULGED?

### Phase 4: Qualitative Analysis
- Which prompt best captures the "soul" of each style?
- Which handles ambiguous cases best?
- Which provides most useful explanations?

---

## Hypotheses

### Expected Performance

**prompt-comprehensive.md**
- **Pros**: Most context, worked examples, differentiations
- **Cons**: Longest, might over-fit to examples
- **Predicted Score**: 8-9/10

**prompt-keywords-only.md**
- **Pros**: Fast, clear matching criteria
- **Cons**: Might miss subtle semantic patterns
- **Predicted Score**: 6-7/10

**prompt-semantic-only.md**
- **Pros**: Rich lived experience, captures essence
- **Cons**: Requires more inference, less structured
- **Predicted Score**: 7-8/10

**prompt-embodiment-only.md**
- **Pros**: Captures energetic patterns, uses "soul" language
- **Cons**: Most abstract, might be hardest to apply consistently
- **Predicted Score**: 6-8/10 (high variance)

---

## Specific Test Scenarios

### Test Case 5: The INDULGED Differentiator
**Critical test**: Does each prompt correctly identify "too adulty" as INDULGED?

**What we're testing**: 
- Does keywords-only miss it (no "adulting" in keyword list)?
- Does semantic-only catch the "if something's hard, I take easy road" pattern?
- Does comprehensive use the worked example effectively?
- Does embodiment catch the "resist responsibility" energy?

**Expected Results**:
- comprehensive: ✓ Should catch it (has similar example)
- keywords-only: ? Might miss specific language
- semantic-only: ✓ Should catch pattern
- embodiment-only: ✓ Should catch energy

### Test Case 3: The Neutral Reporter (DISCONNECTED)
**Critical test**: Can prompts identify DISCONNECTED when person reports facts without emotion?

**What we're testing**:
- Can they detect the pattern of "reporting without affect"?
- Do they over-diagnose CONSTRICTED (controlled) vs DISCONNECTED?

### Test Case 2: The Seven-Way Split
**Critical test**: Can prompts handle complex co-occurring styles?

**What we're testing**:
- Do they correctly rank intensity (Frictive should be highest)
- Do they limit to reasonable number (≤5)?
- Do they avoid kitchen-sink approach?

---

## Data Collection Format

```markdown
## Test Results: [Prompt Name]

### Test Case 1
**Returned**: [Style 1 (0.XX), Style 2 (0.XX), ...]
**Score**: X/10
**Notes**: [observations]

### Test Case 2
**Returned**: [...]
**Score**: X/10
**Notes**: [observations]

[... cases 3-5 ...]

### Overall
**Average Score**: X.X/10
**Precision**: XX%
**Recall**: XX%
**False Positive Rate**: XX%

**Strengths**:
- [bullet points]

**Weaknesses**:
- [bullet points]

**Differentiations**:
- INDULGED vs FRUSTRATED: ✓/✗
- FLOATY vs INDULGED: ✓/✗
- etc.
```

---

## How to Run Tests

### Option 1: Manual Testing
1. Copy prompt content to LLM interface
2. Submit each test case statement
3. Record results in format above
4. Calculate scores

### Option 2: Automated Testing (If API Available)
```python
# Pseudocode
for prompt in [comprehensive, keywords, semantic, embodiment]:
    results = []
    for test_case in test_dataset:
        response = llm.classify(prompt, test_case.statement)
        score = evaluate(response, test_case.known_diagnosis)
        results.append(score)
    
    print(f"{prompt.name}: Average {mean(results)}/10")
```

### Option 3: n8n Workflow
Could create an n8n workflow that:
1. Reads test cases from JSON
2. Runs each through LLM with different prompts
3. Stores results in database
4. Generates comparison report

---

## Success Criteria

### Minimum Viable Performance
- Average score ≥ 7.0/10
- Precision ≥ 70%
- Recall ≥ 60%
- All critical differentiations correct

### Optimal Performance
- Average score ≥ 8.5/10
- Precision ≥ 85%
- Recall ≥ 75%
- Confidence scores well-calibrated

---

## Next Steps After Testing

1. **Identify winner**: Which prompt performs best overall?
2. **Hybrid approach**: Can we combine strengths?
   - Example: Use keywords for pre-filter, comprehensive for final classification
3. **Refinement**: Update winning prompt based on failures
4. **Expand dataset**: Add more test cases for weak areas
5. **Production deployment**: Integrate best approach into system

---

## Questions for User

1. Do you have API access for automated testing?
2. Would you like me to manually test all 4 prompts right now?
3. Should we create an n8n workflow for ongoing testing?
4. Do you have additional test cases with known diagnoses?

