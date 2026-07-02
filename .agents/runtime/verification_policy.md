---
title: Verification Policy for Host LLM
version: 3.0.0
type: Runtime Architecture
---

# Verification Policy

Host LLM phải tự verify output sau mỗi phase và trước khi kết thúc.

## Verification Levels

### Level 1: Output Format Check
**When:** After every phase  
**Questions:**
- Output file exists? ✓
- Output file size > 0? ✓
- Output format matches spec? ✓

**Failure Action:** Rollback phase

### Level 2: Policy Compliance Check
**When:** After phases that produce content (3-8)  
**Questions:**
- Output violates policy? ✓
- Output violates rules? ✓
- Output uses correct terminology? ✓

**Failure Action:** REJECT output, rollback phase

### Level 3: Semantic Integrity Check
**When:** After translation phases (3, 4)  
**Questions:**
- No information lost? ✓
- No over-compression? ✓
- All samples present? ✓
- All explanations present? ✓

**Failure Action:** Rollback phase

### Level 4: Template Compliance Check
**When:** After Phase 5 (LaTeX generation)  
**Questions:**
- LaTeX uses Golden Template? ✓
- display_title correct format? ✓
- Order index preserved? ✓
- Escaping valid? ✓

**Failure Action:** Rollback phase

### Level 5: Quality Score Check
**When:** After Phase 7 (QA)  
**Questions:**
- Statement quality >= 4.0? ✓
- Explanation quality >= 4.0? ✓
- Formatting quality >= 4.0? ✓
- Readability quality >= 4.0? ✓
- Semantic fidelity >= 4.0? ✓

**Failure Action:** REJECT, rollback phases 3-7

### Level 6: Consistency Check
**When:** Final check before output  
**Questions:**
- All problems in same directory? ✓
- All problems same format? ✓
- Order preserved? ✓
- PDF compiles? ✓

**Failure Action:** Rollback phase 8

## Verification Checklist by Phase

### Phase 1 (CRAWL)
```
[ ] Raw HTML file exists
[ ] File size > 1KB
[ ] UTF-8 encoding valid
[ ] File readable by parser
```

### Phase 2 (PARSE)
```
[ ] JSON structure valid
[ ] All required fields present
[ ] title, statement, input, output, constraints, samples exist
[ ] Samples count > 0
[ ] No HTML pollution in text
```

### Phase 3 (TRANSLATE)
```
[ ] display_title format correct: "Việt (Anh)"
[ ] Math formulas preserved
[ ] No information lost (compare to Phase 2)
[ ] Explanation for all samples
[ ] Terminology consistent
```

### Phase 4 (FORMATTING)
```
[ ] I/O format separated
[ ] Samples preserved (same count as Phase 2)
[ ] Explanation preserved for all samples
[ ] display_title unchanged
[ ] JSON structure valid
```

### Phase 5 (LATEX)
```
[ ] LaTeX file exists
[ ] LaTeX syntax valid
[ ] display_title used (not title or translated_title)
[ ] Order index in comment
[ ] Template structure followed
[ ] Escaping correct
```

### Phase 6 (SEMANTIC FIDELITY)
```
[ ] Comparison completed
[ ] No information lost
[ ] Sample count matches
[ ] Explanation present for all
[ ] PASS verdict obtained
```

### Phase 7 (QA)
```
[ ] Quality scored 1.0-5.0
[ ] All dimensions scored
[ ] No dimension < 4.0
[ ] PASS verdict obtained
[ ] No policy violations noted
```

### Phase 8 (COMPILE)
```
[ ] PDF generated
[ ] PDF file valid
[ ] PDF readable (not corrupted)
[ ] Page count correct
[ ] Order preserved in PDF
```

## Self-Verification Questions

After completing execution, Host LLM must answer:

1. **Data Integrity**
   - Did I lose any original information? NO ✓
   - Did I over-compress any explanation? NO ✓
   - Are all samples present? YES ✓

2. **Policy Compliance**
   - Did I violate any policy? NO ✓
   - Did I follow all rules? YES ✓
   - Did I use correct terminology? YES ✓

3. **Format Correctness**
   - Did I use display_title everywhere? YES ✓
   - Did I follow Golden Template? YES ✓
   - Did I preserve order? YES ✓

4. **Quality Standards**
   - Are all quality scores >= 4.0? YES ✓
   - Did QA agent approve? YES ✓
   - Is output production-ready? YES ✓

## Verification Failure Modes

### Failure Mode 1: Format Invalid
**Detection:** Output doesn't match spec  
**Action:** Rollback, retry phase, log error

### Failure Mode 2: Policy Violation
**Detection:** Output violates policy  
**Action:** Rollback, escalate to user, offer correction

### Failure Mode 3: Data Loss
**Detection:** Semantic fidelity check fails  
**Action:** Rollback, retry with preservation mandate

### Failure Mode 4: Quality Below Threshold
**Detection:** Quality score < 4.0  
**Action:** Rollback phases, retry with quality enforcement

### Failure Mode 5: Consistency Broken
**Detection:** Output inconsistent with previous outputs  
**Action:** Rollback, rebuild all affected files

## Verification Logging

Every verification check must log:
```
VERIFICATION: [what was checked]
RESULT: [PASS / FAIL]
EVIDENCE: [which test was performed]
ACTION: [what happens next]
```

Example:
```
VERIFICATION: display_title format
RESULT: FAIL - found "Handshake" instead of "Bắt tay (Handshake)"
EVIDENCE: qa-agent validation
ACTION: Rollback Phase 3, retry with display_title enforcement
```
