---
title: Rollback Policy for Host LLM
version: 3.0.0
type: Ki?n tr?c Runtime
---

# Rollback Policy

Khi bất kỳ Phase nào FAIL, Host LLM phải biết cách rollback an toàn.

## Rollback Triggers

Rollback được kích hoạt khi:

1. **Policy Violation** - Output vi phạm repository policy
2. **Semantic Loss** - Data bị mất hoặc rút gọn
3. **Validation Failure** - Output không pass QA checks
4. **Format Error** - Output không match template
5. **Dependency Failure** - Required skill thất bại
6. **Timeout** - Phase vượt quá time limit
7. **Exception** - Runtime error xảy ra

## Rollback Strategy by Phase

### Phase 1 Failure (CRAWL)
**Trigger:** HTML download failed or empty

**Rollback Steps:**
1. Delete `cache/problemset/<id>.json` (incomplete)
2. Remove entry from `cache/queue/index.json`
3. Log error: why crawl failed
4. Retry with fallback crawler (if available)
5. If all retries exhausted: ABORT task

**Restore Point:** Before this phase started

### Phase 2 Failure (PARSE)
**Trigger:** Parsing produced invalid structure

**Rollback Steps:**
1. Delete `cache/normalized/<id>.json`
2. Keep `cache/problemset/<id>.json` (reuse for retry)
3. Adjust parser parameters
4. Retry Phase 2
5. If retry fails: ABORT

**Restore Point:** Keep raw HTML, redo parsing

### Phase 3-7 Failures (TRANSLATION, FORMATTING, LATEX, VERIFICATION, QA)
**Trigger:** Any validation check fails

**Rollback Steps:**
1. Delete output file(s) from current phase
2. Keep outputs from previous phases
3. Diagnose failure reason
4. Either:
   - Adjust parameters and retry, OR
   - Skip to next problem in queue, OR
   - ABORT and report error to user

**Restore Point:** Before current phase started

### Phase 8 Failure (COMBINE & COMPILE)
**Trigger:** LaTeX compilation failed

**Rollback Steps:**
1. Keep individual .tex files (may be reusable)
2. Delete `outputs/output.pdf` and `outputs/output.tex`
3. Diagnose LaTeX errors
4. Either:
   - Fix LaTeX and recompile, OR
   - Adjust Golden Template and retry, OR
   - ABORT

**Restore Point:** Keep individual files, redo combine/compile

## Rollback Data Management

### Safe to Delete:
- `cache/build/*.tex` (can regenerate)
- `outputs/output.pdf` (can regenerate)
- `outputs/output.tex` (can regenerate)
- Temporary processing files

### Must Preserve:
- `cache/problemset/<id>.json` (original raw content)
- `cache/normalized/<id>.json` (parsed structure)
- `cache/queue/index.json` (metadata)
- `archive/` (completed work)

### Must NOT Delete:
- `.agents/` (repository policies and skills)
- `tools/` (compilation tools)
- `reports/` (audit logs)

## Rollback Error Handling

When rollback itself fails:
1. Log detailed error
2. Stop processing
3. Report to user: "Cannot recover from this error"
4. Provide manual recovery instructions

## Maximum Rollback Attempts

```
Phase 1: Max 3 crawl attempts (different fallbacks)
Phase 2: Max 2 parse attempts (adjust parameters)
Phase 3-7: Max 1 attempt (validation failed, skip or abort)
Phase 8: Max 2 compile attempts (adjust LaTeX)
```

After max attempts: ABORT task, report failure.

## Rollback Logging

Every rollback must log:
```
ROLLBACK TRIGGER: [which check failed]
PHASE: [which phase]
DATA PRESERVED: [what was kept]
DATA DELETED: [what was cleaned up]
NEXT ACTION: [retry, skip, or abort]
REASON: [why this action]
```

## User Communication

When rollback happens:
1. **Info:** Explain what went wrong
2. **Action:** Explain what will be done
3. **Recovery:** Offer recovery options if applicable

Example:
```
Semantic fidelity check FAILED: Sample explanation missing.
Deleting generated LaTeX, rolling back to Phase 3.
Retrying Phase 3 with mandatory explanation enforcement.
```

## No Data Loss Guarantee

Rollback should NEVER result in data loss:
- Original content always preserved
- Intermediate results can be redone
- Only temporary outputs deleted
- User can always inspect cache/

## V3.1 Root-Cause Rollback

Rollback never means patching generated outputs.

If Fragment QA fails:
1. keep upstream JSON,
2. delete/reject only bad fragment if needed,
3. classify the layer,
4. regenerate from that layer,
5. rerun Fragment QA.

If Compile fails:
1. keep `outputs/output.tex` for diagnosis,
2. read compile log/status,
3. classify COMPILE or LATEX,
4. fix template/latex-agent/fragment source as appropriate,
5. regenerate; do not archive.

If PDF QA fails:
1. do not patch PDF,
2. classify the source layer,
3. regenerate from the source-of-truth layer,
4. rerun compile and PDF QA.
