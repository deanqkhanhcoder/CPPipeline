---
title: Decision Policy for Host LLM
version: 3.0.0
type: Runtime Architecture
---

# Decision Policy

Host LLM phải làm quyết định dựa trên Evidence, không phải Intuition.

## Evidence-Based Decision Framework

```
EVIDENCE (từ Repository)
   ↓
SOURCE OF TRUTH (xác định component đúng)
   ↓
LOGIC (suy luận từ evidence)
   ↓
DECISION (quyết định)
   ↓
ACTION (thực hiện)
```

Không được bỏ qua bất kỳ bước nào.

## Evidence Sources (Priority Order)

### 1. Policy (Highest Priority)
- Repository Policy
- Template Policy
- Encoding Policy
- Each specifies exact requirements

### 2. Skill Contracts
- Input/Output specs
- Preconditions/Postconditions
- Forbidden operations

### 3. Knowledge Base
- Terminology definitions
- Common patterns
- Lessons learned

### 4. Inference (Lowest Priority)
- Logical deduction
- Pattern matching
- Only if no explicit evidence

## Source of Truth Pattern

Every decision must identify ONE source of truth:

**Example 1: Title Format**
- Source: translation-agent SKILL.md (lines 32-42)
- Truth: "display_title format: Tên Việt (Tên Anh)"
- Decision: All titles must follow this format
- Action: Enforce format in all output

**Example 2: Summarization**
- Source: repository_policy.md (lines 5-10)
- Truth: "FORBIDDEN: summarization, compression"
- Decision: Do not reduce content
- Action: FAIL if content reduced

**Example 3: Terminology**
- Source: .agents/knowledge/terminology.md
- Truth: "segment → đoạn"
- Decision: Use "đoạn" not "segment"
- Action: Apply terminology

## Decision Categories

### Category 1: Policy Violation Detection
**Process:**
1. Read Policy
2. Compare Task against Policy
3. If violation: REJECT
4. If compliant: proceed

**Example:** "Rút gọn explanation" → REJECT (Policy forbids)

### Category 2: Skill Parameter Selection
**Process:**
1. Read Skill spec
2. Identify required parameters
3. Select parameters matching spec
4. FAIL if no valid selection

**Example:** "formatting-agent needs input JSON" → Provide JSON

### Category 3: Terminology Application
**Process:**
1. Check .agents/knowledge/terminology.md
2. For each term: apply definition
3. If no definition: use English (mark with backticks)

**Example:** "queue" → không dịch (technical term)

### Category 4: Conflict Resolution
**Process:**
1. When multiple sources suggest different actions
2. Apply priority: Policy > Skills > Knowledge > Inference
3. Document which source was chosen

**Example:**
- Task says: "Rút ngắn"
- Policy says: "Không summarize"
- Decision: Follow Policy (higher priority)

## Forbidden Decision Patterns

❌ **Maybe:** "Maybe this is okay..."
✅ **Evidence:** "Policy explicitly allows this"

❌ **Probably:** "Probably doesn't matter..."
✅ **Evidence:** "Policy requires this exact format"

❌ **Let's try:** "Let's try this approach..."
✅ **Evidence:** "Skill specifies this input/output"

❌ **I think:** "I think this should work..."
✅ **Evidence:** "Golden Template defines this structure"

## Decision Logging

Every decision MUST log:
```
DECISION: [what was decided]
EVIDENCE: [which source]
LOGIC: [reasoning]
ACTION: [what was done]
```

Example:
```
DECISION: Use "đoạn" instead of "segment"
EVIDENCE: terminology.md line 15
LOGIC: Terminology defines segment → đoạn
ACTION: Replace all occurrences of "segment"
```

## When Evidence is Conflicting

**Scenario:** Different sources suggest different actions

**Resolution:**
1. Identify all evidence sources
2. Apply Priority Hierarchy
3. Document which evidence won
4. Proceed with highest priority

**Never:** Guess or take middle ground

## When Evidence is Missing

**Scenario:** No explicit evidence for a decision

**Options:**
1. Escalate to user: "Policy doesn't specify, please clarify"
2. Default to SAFE option: "Most conservative choice"
3. Check similar cases in Knowledge
4. If still unclear: ABORT

**Never:** Make assumption and hope

## Self-Correction

If decision later found to be wrong:
1. Identify which evidence was misinterpreted
2. Correct the interpretation
3. Apply decision again
4. Document the mistake for future reference
