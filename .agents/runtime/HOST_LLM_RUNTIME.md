---
name: HOST_LLM_RUNTIME
version: 3.0.0
status: FOUNDATIONAL
---

# Host LLM Runtime Specification v3.0

## Core Concept

**Host LLM** = The AI assistant the user is currently chatting with.

Examples:
- Antigravity
- Claude Code
- Cursor
- Gemini CLI
- GitHub Copilot
- ChatGPT
- Codex

**Host LLM IS the Runtime.** There is NO backend, NO API, NO provider layer.

```
User
  ↓
Host LLM (AI)
  ↓
Reads: Skill Contracts, Policies, Rules, Knowledge
  ↓
Executes: State Machine (11 Phases)
  ↓
Uses: Local Tools (Python scripts, Git, LaTeX compiler)
  ↓
Output: PDF, JSON, LaTeX, Reports
```

## No Backend Architecture

**Forbidden in v3.0:**
- ❌ Gemini API calls
- ❌ OpenAI API calls
- ❌ Claude API calls
- ❌ Any LLM backend layer
- ❌ Model provider abstraction
- ❌ Agent spawning other agents via API
- ❌ llm_backend.py, provider.py, model_router.py
- ❌ Any Python code that initiates LLM calls

**The entire backend IS the Host LLM.**

## State Machine Model

Host LLM MUST operate as a deterministic state machine with 11 phases:

```
Phase 0: BOOT
  ├─ Load Runtime Policy
  ├─ Load Repository Policy
  ├─ Load Global Rules
  ├─ Load Terminology
  ├─ Load README
  ├─ Load Skill Contracts
  └─ Build Execution Context

Phase 1: REPOSITORY AUDIT
  ├─ Understand folder structure
  ├─ Understand skill purposes
  ├─ Understand policy purposes
  ├─ Identify Source of Truth
  └─ Checkpoint: PASS or FAIL

Phase 2: EXECUTION PLAN
  ├─ Define Current Goal
  ├─ List Required Skills
  ├─ List Required Tools
  ├─ List Required Policies
  ├─ Define Expected Outputs
  ├─ Define Files to Modify
  ├─ Define Forbidden Files
  ├─ Define Risk
  └─ Define Rollback Strategy

Phase 3: WAIT USER APPROVAL
  ├─ Show Execution Plan
  ├─ Wait for Proceed
  └─ If rejected: Go to Phase 2

Phase 4: EXECUTION
  ├─ For each action:
  │  ├─ Gather Evidence
  │  ├─ Draw Conclusion
  │  └─ Execute Action
  ├─ Forbidden: Reactive decisions
  ├─ Forbidden: I think..., Maybe..., Actually...
  └─ Required: Evidence → Conclusion → Action

Phase 5: SELF VERIFICATION
  ├─ Check output correctness
  ├─ Check Skill Contract compliance
  ├─ Check Policy compliance
  ├─ Check Golden Template integrity
  ├─ Check Order Preservation
  └─ Checkpoint: PASS or FAIL

Phase 6: REGRESSION TEST
  ├─ If modified: crawler → run crawler tests
  ├─ If modified: parser → run parser tests
  ├─ If modified: translator → run translator tests
  ├─ If modified: latex → run latex tests
  ├─ If modified: compiler → run compiler tests
  ├─ If modified: queue → run queue tests
  └─ Checkpoint: ALL PASS or FAIL

Phase 7: REPOSITORY CLEANUP
  ├─ Remove debug files
  ├─ Remove one-time scripts
  ├─ Remove duplicate files
  ├─ Move temp files to /scratch
  └─ Remove /scratch after completion

Phase 8: FINAL AUDIT
  ├─ Repository Audit: PASS
  ├─ Skill Audit: PASS
  ├─ Policy Audit: PASS
  ├─ Template Audit: PASS
  ├─ Language Audit: PASS
  ├─ Encoding Audit: PASS
  └─ Checkpoint: ALL PASS or FAIL

Phase 9: COMMIT
  ├─ Only if Phase 8 PASS
  └─ Create descriptive commit message

Phase 10: TAG (if release)
  ├─ Only if all phases PASS
  └─ Create annotated tag

Phase 11: PUSH
  ├─ Push branch
  └─ Push tag
```

## Key Rules for Host LLM

### Rule 1: Repository First
Always follow this hierarchy:
```
Repository Structure
  ↓
Policy (Mandatory Rules)
  ↓
Skill (How to Execute)
  ↓
Rule (Best Practices)
  ↓
Knowledge (Reference)
  ↓
Current Task
```

FORBIDDEN: Task → Code → Policy

### Rule 2: Source of Truth
Always identify and locate Source of Truth before modification.

Examples:
- Template changes → Must update `.agents/templates/template.tex`
- Terminology → Must update `.agents/policies/terminology.md`
- Title format → Must update `translation-agent` Skill Contract
- Queue structure → Must update `crawler_manager.py`

### Rule 3: Evidence → Conclusion → Action
Every decision MUST follow this pattern:

```
Evidence: "I read file X and found Y"
Conclusion: "Therefore, I need to do Z"
Action: "Execute Z"
```

Forbidden: "I think we should...", "Maybe we could...", "Actually, let me try..."

### Rule 4: No Reactive Coding
FORBIDDEN:
- Writing a new tool to fix a failing workflow
- Creating batch_parser.py because parser is slow
- Creating helper.py for one-time use
- Duplicating pipeline code to work around bug

REQUIRED:
- Fix the root cause (the abstraction layer)
- If feature missing, extend abstraction
- Don't patch on top

### Rule 5: Scratch Policy
Temporary files MUST go to `/scratch` or `/temp`:
- One-time scripts
- Debug files
- Test outputs
- Intermediate data

After use, MUST delete. Never commit to main repo.

### Rule 6: No Early Execution
FORBIDDEN to execute before:
- ❌ Audit complete
- ❌ Plan approved by user
- ❌ Verification step passed
- ❌ Final audit passed

### Rule 7: Self Verification
After each phase, Host LLM MUST ask:
- "Did output match expected?"
- "Does Skill Contract still apply?"
- "Did I violate any Policy?"
- "Is Golden Template unchanged?"
- "Is Order Preservation intact?"

If ANY answer is "No" → Go back, fix, re-verify.

## Execution Context

When Host LLM boots, it MUST build execution context:

```
{
  "repository_root": "d:\\CP crawl",
  "current_branch": "master",
  "current_commit": "ac0c03e",
  "repository_version": "v2.1",
  "target_version": "v3.0",
  "skills_available": [
    "cp-pipeline",
    "cp-crawler",
    "cp-parser",
    "translation-agent",
    "sample-explainer",
    "editorial-agent",
    "terminology-agent",
    "formatting-agent",
    "latex-agent",
    "latex-guardian",
    "semantic-fidelity-reviewer",
    "order-guardian",
    "qa-agent"
  ],
  "policies": [
    "repository_policy",
    "template_policy",
    "terminology_policy",
    "execution_state_machine"
  ],
  "golden_template": ".agents/templates/template.tex",
  "source_of_truth": {
    "titles": "translation-agent/output",
    "terminology": ".agents/policies/terminology.md",
    "template": ".agents/templates/template.tex",
    "order": "cache/queue/index.json"
  },
  "current_goal": null,
  "approved_plan": null,
  "current_phase": 0
}
```

## Phase Transitions

Host LLM MUST NOT skip phases:

```
Phase 0 → Phase 1 (MANDATORY)
Phase 1 FAIL → STOP
Phase 1 PASS → Phase 2 (MANDATORY)
Phase 2 → Phase 3 (MANDATORY for large ops)
Phase 3 REJECTED → Back to Phase 2
Phase 3 APPROVED → Phase 4 (MANDATORY)
Phase 4 ERROR → Stop or Rollback (defined in plan)
Phase 4 SUCCESS → Phase 5 (MANDATORY)
Phase 5 FAIL → Stop or Fix then Phase 5 again
Phase 5 PASS → Phase 6 (if applicable, else Phase 7)
Phase 6 FAIL → STOP, Fix issue
Phase 6 PASS → Phase 7 (MANDATORY)
Phase 7 → Phase 8 (MANDATORY)
Phase 8 FAIL → STOP, Do NOT commit
Phase 8 PASS → Phase 9 (MANDATORY for release)
Phase 9 → Phase 10 (if release)
Phase 10 → Phase 11 (MANDATORY)
```

## Success Criteria for v3.0

After v3.0 upgrade, ALL Host LLMs must:

✅ Follow the 11-phase state machine deterministically
✅ Never execute before audit and plan approval
✅ Never make reactive decisions (try-error-guess)
✅ Always identify Source of Truth before modifying
✅ Always gather evidence before conclusions
✅ Always self-verify after changes
✅ Always respect Skill Contracts and Policies
✅ Never create unnecessary tools or files
✅ Always cleanup artifacts
✅ Always pass final audit before committing

If ANY Host LLM violates these rules → Repository fails to load properly.
