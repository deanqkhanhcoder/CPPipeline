---
name: EXECUTION_STATE_MACHINE
version: 3.0.0
status: MANDATORY_POLICY
---

# Execution State Machine Policy v3.0

## Overview

This policy defines 11 mandatory phases that Host LLM MUST follow for ANY operation on CPPipeline repository.

**No phase can be skipped.**
**No phase can be executed out of order.**
**No phase can be combined.**

## Phase 0: BOOT

**Duration:** Immediate on task start  
**Checkpoint:** MANDATORY

### Actions:
1. Load `.agents/runtime/HOST_LLM_RUNTIME.md`
2. Load `.agents/policies/repository_policy.md`
3. Load `.agents/policies/EXECUTION_STATE_MACHINE.md` (this file)
4. Load `.agents/policies/terminology.md`
5. Load `README.md`
6. Load `.agents/skills/cp-pipeline/SKILL.md`
7. Load all dependent skills
8. Build execution context (see HOST_LLM_RUNTIME.md)

### Checkpoint:
- ✅ All files loaded successfully
- ✅ No conflicts in policies
- ✅ Repository version identified
- ✅ Execution context ready

**If FAIL:** STOP, report which file failed to load

**If PASS:** → Phase 1

---

## Phase 1: REPOSITORY AUDIT

**Duration:** 5-10 minutes  
**Checkpoint:** MANDATORY

### Requirements:

Host LLM MUST understand:
- ✅ Repository folder structure (.agents/, tools/, cache/, outputs/)
- ✅ Skill purposes (what each skill does)
- ✅ Policy purposes (what each policy enforces)
- ✅ Tool purposes (what each Python script does)
- ✅ Golden Template location and immutability rules
- ✅ Source of Truth for each component
- ✅ File organization and naming conventions
- ✅ Encoding standards (UTF-8 for all text files)
- ✅ Forbidden architectures and patterns

### Audit Checklist:

```
□ All 13 skills exist
□ All policies loaded correctly
□ Golden Template found at .agents/templates/template.tex
□ README describes Host LLM Runtime correctly
□ No llm_backend.py or provider.py exists
□ No API wrapper code exists
□ Terminology dictionary accessible
□ Queue structure understood
□ Cache structure understood
□ Build process understood
□ Compile process understood
```

### Checkpoint:
- ✅ Host LLM answers: "I understand this repository"
- ✅ All 13 skills can be located and described
- ✅ All policies can be cited correctly
- ✅ Source of Truth identified for each component

**If FAIL:** STOP, identify what's missing or misunderstood

**If PASS:** → Phase 2

---

## Phase 2: EXECUTION PLAN

**Duration:** 5-15 minutes  
**Checkpoint:** MANDATORY

### Requirements:

Host LLM MUST create written Execution Plan containing:

```
EXECUTION PLAN
==============

Current Goal:
[What are we trying to accomplish?]

Required Skills:
- [Skill A]: for [purpose]
- [Skill B]: for [purpose]

Required Tools:
- [Tool 1]: for [purpose]
- [Tool 2]: for [purpose]

Required Policies:
- [Policy 1]: governs [what]
- [Policy 2]: governs [what]

Expected Outputs:
- [Output 1]: location, format
- [Output 2]: location, format

Files to Modify:
- [File 1]: reason, expected changes
- [File 2]: reason, expected changes

Files Forbidden to Modify:
- [File 1]: because [reason from policy]
- [File 2]: because [reason from policy]

Risk Assessment:
- Low/Medium/High
- If breaking change, what mitigates it?

Rollback Strategy:
- If something fails, how do we rollback?
- What are the recovery steps?
```

### Checkpoint:
- ✅ Plan is written (not just in mind)
- ✅ All required skills identified
- ✅ All required tools identified
- ✅ All required policies referenced
- ✅ Outputs clearly defined
- ✅ Forbidden files explicitly listed
- ✅ Risk assessed
- ✅ Rollback strategy defined

**If FAIL:** STOP, refine plan

**If PASS:** → Phase 3 (if major operation) or → Phase 4 (if minor operation)

---

## Phase 3: WAIT USER APPROVAL

**Duration:** Depends on user  
**Checkpoint:** CONDITIONAL (only for large operations)

### When Required:

Major operations only:
- ✅ Skill refactor
- ✅ Policy change
- ✅ Template modification
- ✅ Schema change
- ✅ Deleting/renaming files
- ✅ Creating new agents/skills
- ✅ Generating large outputs (>100 files)

### When NOT Required:

Minor operations:
- ✅ Fixing typos
- ✅ Adding documentation
- ✅ Updating single field values
- ✅ Translating content
- ✅ Running existing tools without modification

### Action:

1. Display Execution Plan to user
2. Request: "Does this plan look correct? Type: Proceed"
3. Wait for explicit "Proceed" or similar confirmation

### Checkpoint:
- ✅ User approved plan
- ✅ User confirmed goal alignment

**If REJECTED:** → Back to Phase 2 (refine plan)

**If APPROVED:** → Phase 4

**If SKIPPED (minor op):** → Phase 4

---

## Phase 4: EXECUTION

**Duration:** Depends on complexity  
**Checkpoint:** PER ACTION

### Mandatory Pattern for Each Action:

```
Evidence:
[I read file X and found Y]
[The policy says Z]

Conclusion:
[Therefore, I need to do A]
[Because B requires C]

Action:
[Execute A]
[Result: D]
```

### Forbidden During Execution:
- ❌ "I think we should..."
- ❌ "Maybe we could..."
- ❌ "Actually, let me try..."
- ❌ "Wait, I realized..."
- ❌ "Let me create a helper script..."
- ❌ Reactive decision-making
- ❌ Guessing without evidence

### Required During Execution:
- ✅ Evidence from repository/policy
- ✅ Clear conclusion logically derived
- ✅ Deliberate action
- ✅ Verification of result

### Checkpoint (per action):
- ✅ Evidence gathered
- ✅ Conclusion stated
- ✅ Action completed
- ✅ Result verified

**If any action FAILS:** → Determine: Rollback or Fix & Retry

**After all actions PASS:** → Phase 5

---

## Phase 5: SELF VERIFICATION

**Duration:** 5-10 minutes  
**Checkpoint:** MANDATORY

### Host LLM MUST Ask and Answer:

```
□ Do outputs match the expected format? YES / NO
□ Does each output respect Skill Contracts? YES / NO
□ Are all Policies still being followed? YES / NO
□ Is Golden Template unchanged? YES / NO
□ Is Order Preservation intact? YES / NO
□ Are there any new errors? YES / NO
□ Are encoding standards maintained? YES / NO
□ Are all files in correct locations? YES / NO
```

### If ANY Answer is "NO":
→ Identify issue and fix before moving forward

### If ALL Answers are "YES":
→ Phase 6

---

## Phase 6: REGRESSION TEST

**Duration:** 10-30 minutes  
**Checkpoint:** CONDITIONAL

### Only Required If Modified:

```
Modified crawler.py?
  → Run: python tools/crawler_manager.py test
  → Expected: All tests pass

Modified parser?
  → Run: python tools/parser.py test
  → Expected: All tests pass

Modified translator workflow?
  → Run: sample translation on known input
  → Expected: Output matches previous baseline

Modified latex generation?
  → Run: pdflatex compile
  → Expected: PDF generates without errors

Modified queue system?
  → Run: queue integrity check
  → Expected: All jobs properly queued
```

### Checkpoint:
- ✅ If modified components have tests, tests PASS
- ✅ No regression observed
- ✅ Output quality maintained

**If ANY test FAILS:** → STOP, fix issue, re-run Phase 6

**If ALL tests PASS:** → Phase 7

---

## Phase 7: REPOSITORY CLEANUP

**Duration:** 5 minutes  
**Checkpoint:** MANDATORY

### Host LLM MUST Ask:

```
□ Are there debug files? YES / NO → Delete
□ Are there one-time scripts? YES / NO → Delete or move to /scratch
□ Are there duplicate files? YES / NO → Delete
□ Are there misplaced files? YES / NO → Move to correct location
□ Is /scratch polluted? YES / NO → Clean up
□ Are there temporary outputs? YES / NO → Delete
```

### Required Locations for Temporary Files:
- `scratch/` - One-time scripts, debug files
- `/tmp` - Temporary outputs during processing

### Post-Cleanup:
- ✅ Delete all temporary files
- ✅ Clean `/scratch` directory
- ✅ Remove debug artifacts

### Checkpoint:
- ✅ Repository is clean
- ✅ No debug files remain
- ✅ No artifacts remain

**After cleanup:** → Phase 8

---

## Phase 8: FINAL AUDIT

**Duration:** 10-15 minutes  
**Checkpoint:** MANDATORY - ALL MUST PASS

### Run All Audits:

1. **Repository Audit** - Same as Phase 1
   - All skills still accessible
   - All policies still enforced
   - No new violations introduced

2. **Skill Audit** - All skills function correctly
   - Skills load without errors
   - Skills understand inputs
   - Skills produce expected outputs

3. **Policy Audit** - All policies still enforced
   - No policy violations detected
   - Forbidden patterns not introduced
   - Required patterns maintained

4. **Template Audit** - Golden Template unchanged
   - template.tex file signature matches baseline
   - No macros modified
   - No structure altered

5. **Language Audit** - All text properly Vietnamese/bilingual
   - Titles in format: "Tiếng Việt (English)"
   - Terminology consistent
   - No English-only content where Vietnamese required

6. **Encoding Audit** - All files UTF-8
   - No encoding errors
   - Special characters preserved
   - No mojibake present

### Checkpoint:
```
Repository Audit: PASS / FAIL
Skill Audit: PASS / FAIL
Policy Audit: PASS / FAIL
Template Audit: PASS / FAIL
Language Audit: PASS / FAIL
Encoding Audit: PASS / FAIL

FINAL RESULT: ALL PASS or STOP
```

**If ANY FAIL:** → STOP, DO NOT COMMIT

**If ALL PASS:** → Phase 9

---

## Phase 9: COMMIT

**Duration:** 2 minutes  
**Checkpoint:** CONDITIONAL

### Only Execute If:
- ✅ Phase 8: ALL audits PASS
- ✅ No uncommitted changes exist (or only new files to commit)

### Action:
```
git add -A
git commit -m "[descriptive message]"
```

### Commit Message Format:
```
[type]: [description]

- What was changed
- Why it was changed
- Related phase/goal

Example:
feat: add Host LLM Runtime state machine for v3.0
- Created HOST_LLM_RUNTIME.md specification
- Defined 11-phase execution model
- Updated all skills with runtime phase contracts
```

### Checkpoint:
- ✅ Commit created
- ✅ Commit message descriptive
- ✅ All changes included

**After commit:** → Phase 10 (if release) or → Phase 11 (if push)

---

## Phase 10: TAG (Release Only)

**Duration:** 1 minute  
**Checkpoint:** CONDITIONAL

### Only Execute For Release:

```
git tag -a v3.0 -m "CPPipeline v3.0 - Host LLM Runtime State Machine"
```

### Checkpoint:
- ✅ Tag created
- ✅ Tag message descriptive

**After tag:** → Phase 11

---

## Phase 11: PUSH

**Duration:** 2 minutes  
**Checkpoint:** FINAL

### Actions:
```
git push origin master
git push origin v3.0  (if release)
```

### Checkpoint:
- ✅ Branch pushed
- ✅ Tag pushed (if applicable)
- ✅ Remote synchronized

**After push:** → COMPLETE

---

## Violation Consequences

If Host LLM violates any phase rule:

- ❌ Skips phase → Repository enters inconsistent state
- ❌ Executes out of order → Data corruption risk
- ❌ Makes reactive decisions → Unpredictable behavior
- ❌ Modifies forbidden files → Policy violation
- ❌ Commits without audit → Broken state propagates
- ❌ Doesn't follow evidence→conclusion→action → Logical errors

**Result:** Repository becomes unmaintainable, requires recovery.

## Success Criteria

After ALL 11 phases complete successfully:

✅ Changes are production-ready
✅ No regressions introduced
✅ All policies enforced
✅ All contracts satisfied
✅ All audits pass
✅ Repository is clean
✅ Commit is meaningful
✅ Tag is descriptive
✅ Push is complete
