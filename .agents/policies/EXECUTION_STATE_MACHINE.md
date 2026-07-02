---
name: EXECUTION_STATE_MACHINE
version: 3.0.0
status: POLICY_MANDATORY
---

# Chính sách Execution State Machine v3.0

## Tổng quan

Policy này định nghĩa 11 phases bắt buộc mà Host LLM PHẢI tuân thủ cho BẤT KỲ operation nào trên CPPipeline repository.

**Không phase nào có thể bỏ qua.**
**Không phase nào có thể thực thi không theo thứ tự.**
**Không phase nào có thể kết hợp lại.**

## Phase 0: BOOT

**Thời gian:** Ngay khi task bắt đầu  
**Checkpoint:** BẮT BUỘC

### Actions:
1. Load `.agents/runtime/HOST_LLM_RUNTIME.md`
2. Load `.agents/policies/repository_policy.md`
3. Load `.agents/policies/EXECUTION_STATE_MACHINE.md` (file này)
4. Load `.agents/policies/terminology.md`
5. Load `README.md`
6. Load `.agents/skills/cp-pipeline/SKILL.md`
7. Load tất cả dependent skills
8. Build execution context

### Checkpoint:
- ✅ Tất cả files load thành công
- ✅ Không conflict trong policies
- ✅ Repository version được xác định
- ✅ Execution context ready

**Nếu FAIL:** STOP, report file nào fail

**Nếu PASS:** → Phase 1

---

## Phase 1: REPOSITORY AUDIT

**Thời gian:** 5-10 phút  
**Checkpoint:** BẮT BUỘC

### Yêu cầu:

Host LLM PHẢI hiểu:
- ✅ Repository folder structure (.agents/, tools/, cache/, outputs/)
- ✅ Skill purposes (skill nào làm gì)
- ✅ Policy purposes (policy nào enforce gì)
- ✅ Tool purposes (script Python nào làm gì)
- ✅ Golden Template location và immutability rules
- ✅ Source of Truth cho mỗi component
- ✅ File organization và naming conventions
- ✅ Encoding standards (UTF-8 cho tất cả text files)
- ✅ Forbidden architectures và patterns

### Audit Checklist:

```
□ Tất cả 13 skills tồn tại
□ Tất cả policies load đúng
□ Golden Template tìm thấy ở .agents/templates/template.tex
□ README mô tả Host LLM Runtime đúng
□ Không có llm_backend.py hoặc provider.py
□ Không có API wrapper code
□ Terminology dictionary accessible
□ Queue structure hiểu được
□ Cache structure hiểu được
□ Build process hiểu được
□ Compile process hiểu được
```

### Checkpoint:
- ✅ Host LLM trả lời: "Tôi hiểu repository này"
- ✅ Tất cả 13 skills có thể locate và describe
- ✅ Tất cả policies có thể cite đúng
- ✅ Source of Truth được xác định cho mỗi component

**Nếu FAIL:** STOP, xác định cái gì thiếu hoặc hiểu sai

**Nếu PASS:** → Phase 2

---

## Phase 2: EXECUTION PLAN

**Thời gian:** 5-15 phút  
**Checkpoint:** BẮT BUỘC

### Yêu cầu:

Host LLM PHẢI tạo written Execution Plan chứa:

```
EXECUTION PLAN
==============

Mục tiêu hiện tại:
[Chúng ta đang cố gắng làm gì?]

Required Skills:
- [Skill A]: cho [mục đích]
- [Skill B]: cho [mục đích]

Required Tools:
- [Tool 1]: cho [mục đích]
- [Tool 2]: cho [mục đích]

Required Policies:
- [Policy 1]: govern [gì]
- [Policy 2]: govern [gì]

Expected Outputs:
- [Output 1]: location, format
- [Output 2]: location, format

Files to Modify:
- [File 1]: reason, expected changes
- [File 2]: reason, expected changes

Files Forbidden to Modify:
- [File 1]: vì [reason từ policy]
- [File 2]: vì [reason từ policy]

Risk Assessment:
- Low/Medium/High
- Nếu breaking change, gì mitigate?

Rollback Strategy:
- Nếu có gì fail, chúng ta rollback sao?
- Recovery steps là gì?
```

### Checkpoint:
- ✅ Plan được viết (không chỉ trong mind)
- ✅ Tất cả required skills được xác định
- ✅ Tất cả required tools được xác định
- ✅ Tất cả required policies được reference
- ✅ Outputs được define rõ ràng
- ✅ Forbidden files được list rõ ràng
- ✅ Risk được assess
- ✅ Rollback strategy được define

**Nếu FAIL:** STOP, refine plan

**Nếu PASS:** → Phase 3 (nếu major operation) hoặc → Phase 4 (nếu minor operation)

---

## Phase 3: WAIT USER APPROVAL

**Thời gian:** Phụ thuộc user  
**Checkpoint:** CONDITIONAL (chỉ cho large operations)

### Khi yêu cầu:

Major operations:
- ✅ Skill refactor
- ✅ Policy change
- ✅ Template modification
- ✅ Schema change
- ✅ Deleting/renaming files
- ✅ Creating new agents/skills
- ✅ Generating large outputs (>100 files)

### Khi KHÔNG yêu cầu:

Minor operations:
- ✅ Fixing typos
- ✅ Adding documentation
- ✅ Updating single field values
- ✅ Translating content
- ✅ Running existing tools mà không modify

### Action:

1. Display Execution Plan cho user
2. Request: "Plan này có đúng không? Type: Proceed"
3. Chờ explicit "Proceed" hoặc similar confirmation

### Checkpoint:
- ✅ User approved plan
- ✅ User confirmed goal alignment

**Nếu REJECTED:** → Quay về Phase 2 (refine plan)

**Nếu APPROVED:** → Phase 4

**Nếu SKIPPED (minor op):** → Phase 4

---

## Phase 4: EXECUTION

**Thời gian:** Phụ thuộc complexity  
**Checkpoint:** PER ACTION

### Bắt buộc Pattern cho mỗi Action:

```
Evidence:
[Tôi đọc file X và tìm thấy Y]
[Policy nói Z]

Conclusion:
[Do đó, tôi cần làm A]
[Vì B yêu cầu C]

Action:
[Thực thi A]
[Result: D]
```

### CẤM Trong Execution:
- ❌ "Tôi nghĩ chúng ta nên..."
- ❌ "Có thể chúng ta có thể..."
- ❌ "Thực ra, để tôi thử..."
- ❌ "Chờ, tôi nhận ra..."
- ❌ "Để tôi tạo helper script..."
- ❌ Reactive decision-making
- ❌ Guessing mà không evidence

### YÊU CẦU Trong Execution:
- ✅ Evidence từ repository/policy
- ✅ Clear conclusion được derive logically
- ✅ Deliberate action
- ✅ Result verification

### Checkpoint (per action):
- ✅ Evidence gathered
- ✅ Conclusion stated
- ✅ Action completed
- ✅ Result verified

**Nếu action FAIL:** → Determine: Rollback hay Fix & Retry

**Sau khi tất cả actions PASS:** → Phase 5

---

## Phase 5: SELF VERIFICATION

**Thời gian:** 5-10 phút  
**Checkpoint:** BẮT BUỘC

### Host LLM PHẢI Hỏi và Trả lời:

```
□ Outputs có khớp expected format? YES / NO
□ Mỗi output có respect Skill Contracts? YES / NO
□ Tất cả Policies vẫn được follow? YES / NO
□ Golden Template không bị thay? YES / NO
□ Order Preservation vẫn còn đúng? YES / NO
□ Có errors mới? YES / NO
□ Encoding standards được maintain? YES / NO
□ Tất cả files ở correct locations? YES / NO
```

### Nếu BẤT KỲ Answer là "NO":
→ Identify issue và fix trước khi move forward

### Nếu TẤT CẢ Answers là "YES":
→ Phase 6

---

## Phase 6: REGRESSION TEST

**Thời gian:** 10-30 phút  
**Checkpoint:** CONDITIONAL

### Chỉ yêu cầu nếu Modified:

```
Modified crawler.py?
  → Run: python tools/crawler_manager.py test
  → Expected: All tests pass

Modified parser?
  → Run: python tools/parser.py test
  → Expected: All tests pass

Modified translator workflow?
  → Run: sample translation on known input
  → Expected: Output khớp previous baseline

Modified latex generation?
  → Run: pdflatex compile
  → Expected: PDF generates không errors

Modified queue system?
  → Run: queue integrity check
  → Expected: All jobs properly queued
```

### Checkpoint:
- ✅ Nếu modified components có tests, tests PASS
- ✅ Không regression observed
- ✅ Output quality maintained

**Nếu ANY test FAIL:** → STOP, fix issue, re-run Phase 6

**Nếu ALL tests PASS:** → Phase 7

---

## Phase 7: REPOSITORY CLEANUP

**Thời gian:** 5 phút  
**Checkpoint:** BẮT BUỘC

### Host LLM PHẢI Hỏi:

```
□ Có debug files? YES / NO → Xóa
□ Có one-time scripts? YES / NO → Xóa hoặc move /scratch
□ Có duplicate files? YES / NO → Xóa
□ Có misplaced files? YES / NO → Move to correct location
□ /scratch bị polluted? YES / NO → Clean up
□ Có temporary outputs? YES / NO → Xóa
```

### Required Locations cho Temporary Files:
- `scratch/` - One-time scripts, debug files
- `/tmp` - Temporary outputs during processing

### Post-Cleanup:
- ✅ Xóa tất cả temporary files
- ✅ Clean `/scratch` directory
- ✅ Remove debug artifacts

### Checkpoint:
- ✅ Repository is clean
- ✅ Không debug files remain
- ✅ Không artifacts remain

**Sau cleanup:** → Phase 8

---

## Phase 8: FINAL AUDIT

**Thời gian:** 10-15 phút  
**Checkpoint:** BẮT BUỘC - TẤT CẢ PHẢI PASS

### Chạy Tất cả Audits:

1. **Repository Audit** - Same as Phase 1
   - Tất cả skills vẫn accessible
   - Tất cả policies vẫn enforced
   - Không violations mới

2. **Skill Audit** - All skills function correctly
   - Skills load mà không errors
   - Skills understand inputs
   - Skills produce expected outputs

3. **Policy Audit** - All policies vẫn enforced
   - Không policy violations detected
   - Forbidden patterns không introduced
   - Required patterns maintained

4. **Template Audit** - Golden Template unchanged
   - template.tex file signature khớp baseline
   - Không macros modified
   - Không structure altered

5. **Language Audit** - All text properly Vietnamese/bilingual
   - Titles ở format: "Tiếng Việt (English)"
   - Terminology consistent
   - Không English-only content ở chỗ yêu cầu Vietnamese

6. **Encoding Audit** - All files UTF-8
   - Không encoding errors
   - Special characters preserved
   - Không mojibake present

### Checkpoint:
```
Repository Audit: PASS / FAIL
Skill Audit: PASS / FAIL
Policy Audit: PASS / FAIL
Template Audit: PASS / FAIL
Language Audit: PASS / FAIL
Encoding Audit: PASS / FAIL

FINAL RESULT: ALL PASS hoặc STOP
```

**Nếu ANY FAIL:** → STOP, DO NOT COMMIT

**Nếu ALL PASS:** → Phase 9

---

## Phase 9: COMMIT

**Thời gian:** 2 phút  
**Checkpoint:** CONDITIONAL

### Chỉ Execute nếu:
- ✅ Phase 8: ALL audits PASS
- ✅ Không uncommitted changes (hoặc chỉ new files)

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

**Sau commit:** → Phase 10 (nếu release) hoặc → Phase 11 (nếu push)

---

## Phase 10: TAG (Release Only)

**Thời gian:** 1 phút  
**Checkpoint:** CONDITIONAL

### Chỉ Execute cho Release:

```
git tag -a v3.0 -m "CPPipeline v3.0 - Host LLM Runtime State Machine"
```

### Checkpoint:
- ✅ Tag created
- ✅ Tag message descriptive

**Sau tag:** → Phase 11

---

## Phase 11: PUSH

**Thời gian:** 2 phút  
**Checkpoint:** FINAL

### Actions:
```
git push origin master
git push origin v3.0  (nếu release)
```

### Checkpoint:
- ✅ Branch pushed
- ✅ Tag pushed (nếu applicable)
- ✅ Remote synchronized

**Sau push:** → COMPLETE

---

## Hậu quả Vi phạm

Nếu Host LLM vi phạm bất kỳ phase rule nào:

- ❌ Bỏ qua phase → Repository enters inconsistent state
- ❌ Execute out of order → Data corruption risk
- ❌ Make reactive decisions → Unpredictable behavior
- ❌ Modify forbidden files → Policy violation
- ❌ Commit mà không audit → Broken state propagates
- ❌ Không follow evidence→conclusion→action → Logical errors

**Result:** Repository trở nên unmaintainable, yêu cầu recovery.

## Success Criteria

Sau khi TẤT CẢ 11 phases hoàn thành thành công:

✅ Changes production-ready
✅ Không regressions
✅ Tất cả policies enforced
✅ Tất cả contracts satisfied
✅ Tất cả audits pass
✅ Repository clean
✅ Commit meaningful
✅ Tag descriptive
✅ Push complete
