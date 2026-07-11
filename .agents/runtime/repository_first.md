---
title: Repository First Principle
version: 3.0.0
type: Ki?n tr?c Runtime
---

# Repository First Principle

Host LLM phải luôn ưu tiên Repository trước mọi quyết định khác.

## Priority Hierarchy - Skill-First Design

```
Level 0: SKILL (Entry Point)
  ↓ "Load these dependencies:"
Level 1: SKILL BOOTSTRAP (declares Runtime)
  ↓ "Load Runtime Framework"
Level 2: REPOSITORY POLICY
  ↓
Level 3: GLOBAL RULES
  ↓
Level 4: SKILL CONTRACTS
  ↓
Level 5: KNOWLEDGE BASE (lazy-loaded)
  ↓
Level 6: USER TASK
```

**Execution Flow**:
1. User invokes Skill: `/cp-pipeline`
2. Host LLM reads: `cp-pipeline/SKILL.md`
3. SKILL.md says: "Load Runtime Framework"
4. Host LLM loads declared dependencies
5. Runtime bootstraps and takes over
6. Runtime follows Policy > Rules > Skills hierarchy

Host LLM **PHẢI** tuân theo hierarchy này. Không được bỏ qua hoặc đảo thứ tự.

## Level 1: Repository Policy

**Source:** `.agents/policies/repository_policy.md`

**Contains:**
- Forbidden patterns
- Required patterns
- Encoding standards
- Template requirements
- Data integrity rules

**When Task conflicts with Policy:** REJECT TASK

**Example:**
- Task: "Rút gọn explanation"
- Policy: "Không được summarize"
- Result: REJECT - Policy wins

---

## Level 2: Global Rules

**Source:** `.agents/rules/`

**Contains:**
- Language consistency rules
- Formatting rules
- Naming conventions
- Quy tr?nh rules

**When Task conflicts with Rules:** MODIFY TASK to comply

**Example:**
- Task: "Viết Vietnamese with English mixed"
- Rule: "Tiếng Việt 100%"
- Result: ENFORCE rule

---

## Level 3: Skill Contracts

**Source:** `.agents/skills/*/SKILL.md`

**Contains:**
- Input/Output specifications
- Preconditions/Postconditions
- Forbidden operations
- Validation rules

**When Task conflicts with Skill:** ADJUST PARAMETERS

**Example:**
- Skill formatting-agent: "Không được bỏ sample"
- Task: "Loại bỏ sample dài"
- Result: REJECT - Skill forbids it

---

## Level 4: Knowledge Base

**Source:** `.agents/knowledge/`

**Contains:**
- Terminology dictionary
- CP problem templates
- Common patterns
- Lessons learned

**When Task unclear:** CONSULT KNOWLEDGE

**Example:**
- Task: "Dịch 'segment'"
- Knowledge: Contains "segment → đoạn"
- Result: USE definition from knowledge

---

## Level 5: User Task

**Source:** User input

**Contains:**
- URLs to process
- Processing parameters
- Output requirements

**Constraints:** Task must NOT violate Levels 1-4

**Example:**
- User: "/cp-pipeline https://cses.fi/..."
- Policy forbids: certain operations
- Rule requires: certain format
- Result: APPLY all constraints before execution

---

## Implementation Rules

### Rule 1: Read Before Execute

**Before** accepting any task, Host LLM MUST:
1. Read `.agents/policies/repository_policy.md`
2. Read `.agents/rules/`
3. Read relevant `.agents/skills/*/SKILL.md`
4. Scan `.agents/knowledge/`

**Only then:** Proceed with task

### Rule 2: Conflict Resolution

When conflict arises:
```
Policy > Rules > Skills > Knowledge > Task
```

Higher level ALWAYS wins.

### Rule 3: No Workarounds

CẤM:
- Skip Policy because Task is urgent
- Ignore Rule because "seems okay"
- Bypass Skill contract because "it's faster"
- Guess from knowledge instead of reading

### Rule 4: Evidence Trail

Every decision must have evidence:
- "I followed Policy X because of rule Y"
- "I rejected this because Skill Z forbids it"
- "I modified input based on Knowledge K"

### Rule 5: Escalation

If Task violates Repository:
1. DO NOT execute task
2. EXPLAIN which level was violated
3. PROPOSE modification to task
4. WAIT for user confirmation

---

## Common Mistakes to Avoid

❌ **Mistake 1:** Execute task before reading Policy
✅ **Correct:** Read Policy first, then execute

❌ **Mistake 2:** Interpret Skill loosely
✅ **Correct:** Apply Skill strictly as written

❌ **Mistake 3:** Create tool when Skill exists
✅ **Correct:** Use existing Skill abstraction

❌ **Mistake 4:** Guess from knowledge
✅ **Correct:** Read knowledge explicitly

❌ **Mistake 5:** Modify Policy to fit Task
✅ **Correct:** Modify Task to fit Policy

---

## Repository as Single Source of Truth

Repository contains ALL decisions:
- What is allowed? → Policy
- How should it work? → Skills
- What terminology to use? → Knowledge
- How to format? → Rules

Host LLM is **Executor**, not **Decider**.

Decisions are made by Repository, not by Host LLM's reasoning.
