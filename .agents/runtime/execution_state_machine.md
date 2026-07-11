---
title: Host LLM Execution State Machine
version: 3.0.0
type: Ki?n tr?c Runtime
---

# Host LLM Execution State Machine

**Context**: This state machine executes AFTER Skill (e.g., `/cp-pipeline`) is invoked by Host Runtime.

The Skill bootstraps Runtime, then Runtime follows this state machine.

Host LLM phải hoạt động theo State Machine dưới đây. Mỗi state phải hoàn tất trước khi chuyển state tiếp theo.

## State Diagram

```
┌──────────────────────────┐
│   SKILL INVOKED          │
│   (User: /cp-pipeline)   │
│   cp-pipeline/SKILL.md   │
└──────┬───────────────────┘
       │ Bootstrap Runtime
       ↓
┌─────────────────────────┐
│  LOAD RUNTIME           │
│  - Load runtime.md      │
│  - Load all runtime/    │
└──────┬──────────────────┘
       │
       ↓
┌─────────────────────────┐
│  LOAD GLOBAL POLICIES   │
│  - repository_policy.md │
│  - template_policy.md   │
│  - encoding_policy.md   │
└──────┬──────────────────┘
       │
       ↓
┌─────────────────────────┐
│  LOAD TERMINOLOGY       │
│  - terminology.md       │
│  - Build cache          │
└──────┬──────────────────┘
       │
       ↓
┌─────────────────────────┐
│  RESOLVE SKILLS         │
│  - Read cp-pipeline deps│
│  - Load in order        │
│  - Verify no cycles     │
└──────┬──────────────────┘
       │
       ↓
┌─────────────────────────┐
│  AUDIT INPUT            │
│  - Validate user input  │
│  - Check against Policy │
└──────┬──────────────────┘
       │
       ↓
┌─────────────────────────┐
│  BUILD EXECUTION PLAN   │
│  - Goal, skills, outputs│
│  - Data flow map        │
└──────┬──────────────────┘
       │
       ↓
┌─────────────────────────┐
│  EXECUTION              │
│  - Run phases 1-8       │
│  - Knowledge: lazy load │
│  - Rollback on error    │
└──────┬──────────────────┘
       │
       ↓
┌─────────────────────────┐
│  SELF VERIFICATION      │
│  - Verify each output   │
│  - Policy compliance    │
│  - Semantic fidelity    │
└──────┬──────────────────┘
       │
       ↓
┌──────────────┐
│   OUTPUT     │
└──────────────┘
```

> **Knowledge Loading**: KHÔNG load toàn bộ knowledge upfront.
> Knowledge được lazy-load on-demand trong EXECUTION:
> - Crawler error → `crawler_failures.md`
> - LaTeX error → `latex_failures.md`
> - PDF input → `pdf_statement_handling.md`

## State Specifications

### SKILL INVOKED
**Trigger:** User types `/cp-pipeline <url>`
**Action:** Host Runtime finds `cp-pipeline/SKILL.md`. Reads Bootstrap section. Follows dependency list.
**Next State:** LOAD RUNTIME
**Failure:** N/A (starting point)

### LOAD RUNTIME
**Duration:** 1-2 seconds
**Action:** Load all `.agents/runtime/*.md` files as declared by Skill's Runtime Dependencies
**Validation:** All runtime files must be readable
**Next State:** LOAD GLOBAL POLICIES
**Failure:** HALT - runtime not found

### LOAD GLOBAL POLICIES
**Duration:** 1-2 seconds  
**Action:** Load all `.agents/policies/*.md` files  
**Files**: `repository_policy.md`, `template_policy.md`, `terminology.md`  
**Note**: Encoding rules are embedded in `repository_policy.md` (UTF-8 requirement)  
**Validation:** All policy files must be readable  
**Next State:** LOAD TERMINOLOGY  
**Failure:** HALT - policies missing

### LOAD TERMINOLOGY
**Duration:** 1 second  
**Action:** Load `.agents/policies/terminology.md`  
**Validation:** Terminology dict must be valid  
**Next State:** LOAD KNOWLEDGE  
**Failure:** HALT - terminology invalid

### LOAD KNOWLEDGE
**Duration:** 2-3 seconds  
**Action:** Load all `.agents/knowledge/*.md` files  
**Validation:** Knowledge base must be readable  
**Next State:** LOAD cp-pipeline  
**Failure:** WARN - some knowledge missing, continue

### LOAD cp-pipeline
**Duration:** 1 second  
**Action:** Parse `.agents/skills/cp-pipeline/SKILL.md`  
**Validation:** Must be valid SKILL.md format  
**Next State:** LOAD REQUIRED SKILLS  
**Failure:** HALT - orchestrator not found

### LOAD REQUIRED SKILLS
**Duration:** 3-5 seconds  
**Action:** Resolve dependency graph, load skills in order  
**Validation:** No circular dependencies, all skills exist  
**Next State:** AUDIT INPUT  
**Failure:** HALT - missing dependency

### AUDIT INPUT
**Duration:** 2-3 seconds  
**Action:** Validate user input against policies  
**Validation:** Input must pass policy checks  
**Next State:** BUILD EXECUTION PLAN  
**Failure:** REJECT - input invalid

### BUILD EXECUTION PLAN
**Duration:** 5-10 seconds  
**Action:** Create detailed plan before execution  
**Plan must include:**
- Goal
- Required skills (in order)
- Expected outputs
- Files to read
- Files to write
- Validation steps

**Next State:** WAIT USER APPROVAL (if complex) or EXECUTION  
**Failure:** REJECT - plan infeasible

### WAIT USER APPROVAL
**Duration:** User-dependent  
**Action:** Show plan, wait for confirmation  
**Validation:** User must approve  
**Next State:** EXECUTION  
**Failure:** ABORT - user rejected

### EXECUTION
**Duration:** Skill-dependent  
**Action:** Execute each skill in order  
**Validation:** Monitor outputs continuously  
**Next State:** SELF VERIFICATION  
**Failure:** ROLLBACK or ABORT

### SELF VERIFICATION
**Duration:** 10-20 seconds  
**Action:** Verify all outputs against policies  
**Checks:**
- Output format correct
- No policy violations
- No data loss
- No over-compression
- Golden template compliance
- Semantic fidelity maintained

**Next State:** OUTPUT  
**Failure:** REJECT - quality check failed

### OUTPUT
**Next State:** CONTINUOUS IMPROVEMENT

### CONTINUOUS IMPROVEMENT
**Purpose:** Th?c hi?n V?ng l?p Root Cause (11 b??c) v? V?ng l?p ph?n h?i Ki?n th?c (Knowledge Feedback Loop). C?p nh?t Skill, Knowledge, Policy, Test n?u ph?t hi?n l? h?ng theo `.agents/policies/self_improvement_policy.md`.
**Next State:** FINISH

### FINISH
**Purpose:** Ho?n t?t to?n b? quy tr?nh ?i?u ph?i v? t? c?i ti?n, tr? quy?n ?i?u khi?n v? cho ng??i d?ng.
**Duration:** Instant  
**Action:** Return results to user  
**Validation:** None (already verified)

## Rules

1. **No State Skipping:** Không được bỏ qua state nào
2. **No State Regression:** Không được quay lại state trước
3. **State Idempotency:** Mỗi state phải idempotent (chạy nhiều lần cùng kết quả)
4. **Clear Failure Modes:** Mỗi state phải có rõ ràng cách xử lý failure
5. **Timeout Protection:** Mỗi state phải có timeout (tránh vô hạn)

## Transition Rules

- Chỉ chuyển state khi điều kiện SATISFIED
- Mỗi transition phải ghi log
- Failure chỉ phép HALT, ABORT, REJECT, ROLLBACK
- Không có "optional" states - tất cả bắt buộc
