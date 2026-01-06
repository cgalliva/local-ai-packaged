# Limited Style Test Report

**Prompt File**: prompt-keywords-with-cross-refs.md

**Timestamp**: 2026-01-06T09:40:27.272780

**Available Styles**: CHARMING, DEPRIVED, DISCONNECTED, ELUSIVE, FLIGHTY, FLOATY, FRICTIVE, INDISPENSABLE, MASKED, OMNIPOTENT, PURSUING, SCAVENGING, STIFF, STOCKPILING, SYMBIOTIC, WOUNDED

---

## Summary

| Model | Avg Score | Grade |
|-------|-----------|-------|
| qwen3:8b | 4.34/10 | ❌ Poor |
| qwen3-coder:30b-a3b-q8_0 | 5.92/10 | ⚠️ Fair |
| gpt-oss:120b | 2.75/10 | ❌ Poor |

---

## Detailed Results

### qwen3:8b

#### Test 1 - Score: 4.0/10

**Full Original Diagnosis**: OMNIPOTENT, FRUSTRATED, PREMATURE, CONSTRICTED, FLOATY

**Available for Grading**: OMNIPOTENT, FLOATY

**Model Predicted**: DISCONNECTED, DEPRIVED, OMNIPOTENT, SYMBIOTIC, FRICTIVE

---

#### Test 2 - Score: 7.7/10

**Full Original Diagnosis**: OMNIPOTENT, SYMBIOTIC, FRICTIVE, DEPRIVED, FLOATY, FLIGHTY, CONSTRICTED

**Available for Grading**: OMNIPOTENT, SYMBIOTIC, FRICTIVE, DEPRIVED, FLOATY, FLIGHTY

**Model Predicted**: OMNIPOTENT, DEPRIVED, FLOATY, SYMBIOTIC, FRICTIVE

---

#### Test 3 - Score: 10.0/10

**Full Original Diagnosis**: DISCONNECTED, FRUSTRATED, SACRIFICING

**Available for Grading**: DISCONNECTED

**Model Predicted**: DISCONNECTED

---

#### Test 4 - Score: 0.0/10

**Full Original Diagnosis**: FRUSTRATED, FLOATY, CONSTRICTED, PREMATURE, OMNIPOTENT

**Available for Grading**: FLOATY, OMNIPOTENT

**Model Predicted**: None

---

#### Test 5 - Score: 0.0/10

**Full Original Diagnosis**: INDULGED, FRUSTRATED, DISCONNECTED

**Available for Grading**: DISCONNECTED

**Model Predicted**: None

---

### qwen3-coder:30b-a3b-q8_0

#### Test 1 - Score: 6.0/10

**Full Original Diagnosis**: OMNIPOTENT, FRUSTRATED, PREMATURE, CONSTRICTED, FLOATY

**Available for Grading**: OMNIPOTENT, FLOATY

**Model Predicted**: OMNIPOTENT, FRICTIVE, DEPRIVED, SYMBIOTIC, WOUNDED

---

#### Test 2 - Score: 6.9/10

**Full Original Diagnosis**: OMNIPOTENT, SYMBIOTIC, FRICTIVE, DEPRIVED, FLOATY, FLIGHTY, CONSTRICTED

**Available for Grading**: OMNIPOTENT, SYMBIOTIC, FRICTIVE, DEPRIVED, FLOATY, FLIGHTY

**Model Predicted**: FRICTIVE, FLOATY, DEPRIVED, DISCONNECTED, OMNIPOTENT

---

#### Test 3 - Score: 6.7/10

**Full Original Diagnosis**: DISCONNECTED, FRUSTRATED, SACRIFICING

**Available for Grading**: DISCONNECTED

**Model Predicted**: DEPRIVED, FRICTIVE, OMNIPOTENT, DISCONNECTED, STIFF

---

#### Test 4 - Score: 10.0/10

**Full Original Diagnosis**: FRUSTRATED, FLOATY, CONSTRICTED, PREMATURE, OMNIPOTENT

**Available for Grading**: FLOATY, OMNIPOTENT

**Model Predicted**: FLOATY, DISCONNECTED, OMNIPOTENT

---

#### Test 5 - Score: 0.0/10

**Full Original Diagnosis**: INDULGED, FRUSTRATED, DISCONNECTED

**Available for Grading**: DISCONNECTED

**Model Predicted**: OMNIPOTENT, STIFF

---

### gpt-oss:120b

#### Test 1 - Score: 0.0/10

**Full Original Diagnosis**: OMNIPOTENT, FRUSTRATED, PREMATURE, CONSTRICTED, FLOATY

**Available for Grading**: OMNIPOTENT, FLOATY

**Model Predicted**: SYMBIOTIC, STIFF, MASKED, DEPRIVED, WOUNDED

---

#### Test 2 - Score: 3.1/10

**Full Original Diagnosis**: OMNIPOTENT, SYMBIOTIC, FRICTIVE, DEPRIVED, FLOATY, FLIGHTY, CONSTRICTED

**Available for Grading**: OMNIPOTENT, SYMBIOTIC, FRICTIVE, DEPRIVED, FLOATY, FLIGHTY

**Model Predicted**: MASKED, DEPRIVED, DISCONNECTED, FLOATY

---

#### Test 3 - Score: 6.7/10

**Full Original Diagnosis**: DISCONNECTED, FRUSTRATED, SACRIFICING

**Available for Grading**: DISCONNECTED

**Model Predicted**: DEPRIVED, DISCONNECTED

---

#### Test 4 - Score: 4.0/10

**Full Original Diagnosis**: FRUSTRATED, FLOATY, CONSTRICTED, PREMATURE, OMNIPOTENT

**Available for Grading**: FLOATY, OMNIPOTENT

**Model Predicted**: DISCONNECTED, FLOATY

---

#### Test 5 - Score: 0.0/10

**Full Original Diagnosis**: INDULGED, FRUSTRATED, DISCONNECTED

**Available for Grading**: DISCONNECTED

**Model Predicted**: DEPRIVED

---

