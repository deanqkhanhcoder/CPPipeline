---
title: Host LLM Execution State Machine
version: 3.0.0
type: Runtime Architecture
---

# Host LLM Execution State Machine

Host LLM phải hoạt động theo State Machine dưới đây. Mỗi state phải hoàn tất trước khi chuyển state tiếp theo.

## State Diagram

```
┌──────────────┐
│    BOOT      │
└──────┬───────┘
       │
       ↓
┌─────────────────────────┐
│  LOAD RUNTIME           │
│  - Load host_llm_contract.md
│  - Verify runtime principles
└──────┬──────────────────┘
       │
       ↓
┌─────────────────────────┐
│  LOAD GLOBAL POLICIES   │
│  - Load repository_policy.md
│  - Load template_policy.md
│  - Load encoding_policy.md
└──────┬──────────────────┘
       │
       ↓
┌─────────────────────────┐
│  LOAD TERMINOLOGY       │
│  - Load terminology.md
│  - Build terminology cache
└──────┬──────────────────┘
       │
       ↓
┌─────────────────────────┐
│  LOAD KNOWLEDGE         │
│  - Load .agents/knowledge/*
│  - Build context cache
└──────┬──────────────────┘
       │
       ↓
┌─────────────────────────┐
│  LOAD cp-pipeline       │
│  - Parse SKILL.md
│  - Identify dependencies
└──────┬──────────────────┘
       │
       ↓
┌─────────────────────────┐
│  LOAD REQUIRED SKILLS   │
│  - Resolve dependency graph
│  - Load in dependency order
│  - Verify no circular deps
└──────┬──────────────────┘
       │
       ↓
┌─────────────────────────┐
│  AUDIT INPUT            │
│  - Validate user input
│  - Validate URLs (if any)
│  - Check input against Policy
└──────┬──────────────────┘
       │
       ↓
┌─────────────────────────┐
│  BUILD EXECUTION PLAN   │
│  - Determine goal
│  - List required skills
│  - Map data flow
│  - Identify outputs
│  - List validation steps
└──────┬──────────────────┘
       │
       ↓
┌─────────────────────────┐
│  WAIT USER APPROVAL     │
│  (nếu plan phức tạp)
│  - Show plan to user
│  - Wait for approval
│  - Handle rejection
└──────┬──────────────────┘
       │
       ↓
┌─────────────────────────┐
│  EXECUTION              │
│  - Execute each skill
│  - Monitor outputs
│  - Catch errors
│  - Apply rollback (if needed)
└──────┬──────────────────┘
       │
       ↓
┌─────────────────────────┐
│  SELF VERIFICATION      │
│  - Verify each output
│  - Check policy compliance
│  - Validate data integrity
│  - Semantic fidelity check
└──────┬──────────────────┘
       │
       ↓
┌──────────────┐
│   OUTPUT     │
└──────────────┘
```

## State Specifications

### BOOT
**Duration:** Instant  
**Action:** Initialize state machine  
**Validation:** None  
**Next State:** LOAD RUNTIME

### LOAD RUNTIME
**Duration:** 1-2 seconds  
**Action:** Read `.agents/runtime/host_llm_contract.md`, verify this state machine  
**Validation:** Contract must be valid  
**Next State:** LOAD GLOBAL POLICIES  
**Failure:** HALT - runtime misconfigured

### LOAD GLOBAL POLICIES
**Duration:** 1-2 seconds  
**Action:** Load all `.agents/policies/*.md` files  
**Validation:** All policies must be readable  
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
