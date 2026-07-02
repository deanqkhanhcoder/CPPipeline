---
title: Host LLM Runtime Framework v3.0
version: 3.0.0
type: Architecture
---

# Host LLM Runtime Framework v3.0

**CPPipeline** không phải một ứng dụng. Nó là một **Runtime Framework** cho AI.

## Architecture: Skill-First Design

```
User: /cp-pipeline
  ↓
Host Runtime finds: cp-pipeline/SKILL.md
  ↓
SKILL.md Bootstrap Section: "Load Runtime"
  ↓
Host Runtime loads: .agents/runtime/runtime.md
  ↓
Runtime takes over execution
  ↓
Runtime orchestrates all phases
```

**Key Point**: Skill is the **Entry Point**. Runtime is the **Execution Engine**.

Host Runtime does NOT scan `.agents/runtime/` on its own.
Skill TELLS Host Runtime to load Runtime Framework.

## Runtime Architecture Layers

### Layer 1: Specification Files (.agents/runtime/)

```
host_llm_contract.md
  → Defines what Host LLM is
  → Principles and execution guarantee

execution_state_machine.md
  → Defines HOW Host LLM executes
  → 12 states that MUST be followed in order
  → No skipping, no regressions

phase_definition.md
  → Defines WHAT each phase does
  → Input/Output specs for each phase
  → Preconditions/Postconditions

repository_first.md
  → Defines PRIORITY of decisions
  → Policy > Rules > Skills > Knowledge > Task
  → No deviations allowed

decision_policy.md
  → Defines HOW to make decisions
  → Evidence-based, not intuition-based
  → Source of truth for each decision

rollback_policy.md
  → Defines WHAT to do when phase fails
  → How to safely restore to previous state
  → Data preservation guarantees

verification_policy.md
  → Defines HOW to verify output
  → Checklists for each phase
  → Self-verification questions
```

### Layer 2: Policies (.agents/policies/)

```
repository_policy.md
  → Forbidden patterns
  → Required patterns
  → System constraints

template_policy.md
  → Template structure requirements
  → Golden Template rules

encoding_policy.md
  → UTF-8 requirements
  → Encoding specifications
```

### Layer 3: Skills (.agents/skills/)

```
cp-pipeline
  → Orchestrator (loads and coordinates skills)
  
cp-crawler
  → Downloads HTML/Markdown from URL
  
cp-parser
  → Parses structure to JSON
  
translation-agent
  → Translates to Vietnamese
  
sample-explainer
  → Creates explanations for samples
  
editorial-agent
  → Improves Vietnamese prose
  
terminology-agent
  → Applies terminology dictionary
  
formatting-agent
  → Normalizes structure
  
latex-agent
  → Generates LaTeX code
  
latex-guardian
  → Validates LaTeX syntax
  
semantic-fidelity-reviewer
  → Verifies no information loss
  
qa-agent
  → Scores quality (1.0-5.0)
  
order-guardian
  → Preserves problem order
```

### Layer 4: Knowledge Base (.agents/knowledge/)

```
Terminology dictionary
Common patterns
Lessons learned
Quality standards
```

## Execution Flow

```
1. BOOT
2. LOAD RUNTIME (this framework)
3. LOAD GLOBAL POLICIES
4. LOAD TERMINOLOGY
5. LOAD KNOWLEDGE
6. LOAD cp-pipeline
7. LOAD REQUIRED SKILLS
8. AUDIT INPUT
9. BUILD EXECUTION PLAN
10. WAIT USER APPROVAL (if needed)
11. EXECUTION (Phase 1-8)
12. SELF VERIFICATION
13. OUTPUT
```

## Key Principles

### Principle 1: Repository First
Policy always wins over Task. Skills always win over guess.

### Principle 2: Evidence Based
Every decision must have evidence from Repository. No "maybe" or "probably".

### Principle 3: State Machine
Follow execution flow exactly. No jumping states. No regressions.

### Principle 4: Self Verification
Verify output after every phase. FAIL if quality < 4.0.

### Principle 5: No Reactive Coding
Don't create tools when Skills exist. Don't bypass abstractions.

## Success Criterion

After reading this framework, ANY AI Host should:

1. ✅ Understand what Host LLM is
2. ✅ Know the execution state machine
3. ✅ Know what each phase does
4. ✅ Know priority of decisions
5. ✅ Know how to make evidence-based decisions
6. ✅ Know how to rollback safely
7. ✅ Know how to verify output

Result: **All AI Hosts execute identically**

No Gemini-specific behavior. No Claude-specific behavior. Just pure **Runtime Framework**.

## Files to Read in Order

1. **host_llm_contract.md** - What is Host LLM?
2. **execution_state_machine.md** - How to execute?
3. **phase_definition.md** - What does each phase do?
4. **repository_first.md** - What's the priority?
5. **decision_policy.md** - How to decide?
6. **rollback_policy.md** - How to recover?
7. **verification_policy.md** - How to verify?

Then: Read the Skills. Read the Policies. Execute accordingly.

## Integration with Existing Architecture

This runtime framework **does NOT change** any Skills or Policies.

It **adds clarity** on:
- HOW Host LLM should use Skills
- WHEN to use which Policy
- WHAT order to execute
- HOW to make decisions
- HOW to recover from failure

The framework is **non-invasive** and **additive**.
