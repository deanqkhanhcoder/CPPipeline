---
name: HOST_LLM_RUNTIME
version: 3.0.0
status: NỀN_TẢNG
---

# Đặc tả Host LLM Runtime v3.0

## Khái niệm cốt lõi

**Host LLM** = Trợ lý AI mà người dùng hiện đang chat.

Ví dụ:
- Antigravity
- Claude Code
- Cursor
- Gemini CLI
- GitHub Copilot
- ChatGPT
- Codex

**Host LLM CHÍNH LÀ RUNTIME.** Không có backend, không có API, không có tầng provider.

```
Người dùng
  ↓
Host LLM (AI)
  ↓
Đọc: Skill Contracts, Policies, Rules, Knowledge
  ↓
Thực thi: State Machine (11 Phases)
  ↓
Sử dụng: Local Tools (Python scripts, Git, LaTeX compiler)
  ↓
Output: PDF, JSON, LaTeX, Reports
```

## Kiến trúc cấm (Forbidden Architecture)

**Cấm trong v3.0:**
- ❌ Gọi Gemini API
- ❌ Gọi OpenAI API
- ❌ Gọi Claude API
- ❌ Bất kỳ tầng backend LLM nào
- ❌ Abstraction layer provider model
- ❌ Agent spawning agent qua API
- ❌ llm_backend.py, provider.py, model_router.py
- ❌ Bất kỳ Python code nào khởi tạo LLM calls

**Toàn bộ backend LÀ Host LLM.**

## Mô hình State Machine

Host LLM PHẢI hoạt động như state machine xác định với 11 phases:

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
  ├─ Hiểu folder structure
  ├─ Hiểu skill purposes
  ├─ Hiểu policy purposes
  ├─ Xác định Source of Truth
  └─ Checkpoint: PASS hoặc FAIL

Phase 2: EXECUTION PLAN
  ├─ Định nghĩa Current Goal
  ├─ Liệt kê Required Skills
  ├─ Liệt kê Required Tools
  ├─ Liệt kê Required Policies
  ├─ Định nghĩa Expected Outputs
  ├─ Định nghĩa Files to Modify
  ├─ Định nghĩa Forbidden Files
  ├─ Định nghĩa Risk
  └─ Định nghĩa Rollback Strategy

Phase 3: WAIT USER APPROVAL
  ├─ Hiển thị Execution Plan
  ├─ Chờ Proceed
  └─ Nếu từ chối: Quay về Phase 2

Phase 4: EXECUTION
  ├─ Với mỗi action:
  │  ├─ Thu thập Evidence
  │  ├─ Rút ra Conclusion
  │  └─ Thực thi Action
  ├─ Cấm: Reactive decisions
  ├─ Cấm: I think..., Maybe..., Actually...
  └─ Yêu cầu: Evidence → Conclusion → Action

Phase 5: SELF VERIFICATION
  ├─ Kiểm tra output correctness
  ├─ Kiểm tra Skill Contract compliance
  ├─ Kiểm tra Policy compliance
  ├─ Kiểm tra Golden Template integrity
  ├─ Kiểm tra Order Preservation
  └─ Checkpoint: PASS hoặc FAIL

Phase 6: REGRESSION TEST
  ├─ Nếu sửa: crawler → chạy crawler tests
  ├─ Nếu sửa: parser → chạy parser tests
  ├─ Nếu sửa: translator → chạy translator tests
  ├─ Nếu sửa: latex → chạy latex tests
  ├─ Nếu sửa: compiler → chạy compiler tests
  ├─ Nếu sửa: queue → chạy queue tests
  └─ Checkpoint: ALL PASS hoặc FAIL

Phase 7: REPOSITORY CLEANUP
  ├─ Xóa debug files
  ├─ Xóa one-time scripts
  ├─ Xóa duplicate files
  └─ Di chuyển temp files sang /scratch

Phase 8: FINAL AUDIT
  ├─ Repository Audit: PASS
  ├─ Skill Audit: PASS
  ├─ Policy Audit: PASS
  ├─ Template Audit: PASS
  ├─ Language Audit: PASS
  ├─ Encoding Audit: PASS
  └─ Checkpoint: ALL PASS hoặc FAIL

Phase 9: COMMIT
  ├─ Chỉ nếu Phase 8 PASS
  └─ Tạo descriptive commit message

Phase 10: TAG (nếu release)
  ├─ Chỉ nếu all phases PASS
  └─ Tạo annotated tag

Phase 11: PUSH
  ├─ Push branch
  └─ Push tag
```

## Quy tắc chính cho Host LLM

### Quy tắc 1: Repository First
Luôn tuân thủ hierarchy này:
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

CẤM: Task → Code → Policy

### Quy tắc 2: Source of Truth
Luôn xác định và định vị Source of Truth trước khi sửa đổi.

Ví dụ:
- Template changes → Phải cập nhật `.agents/templates/template.tex`
- Terminology → Phải cập nhật `.agents/policies/terminology.md`
- Title format → Phải cập nhật `translation-agent` Skill Contract
- Queue structure → Phải cập nhật `crawler_manager.py`

### Quy tắc 3: Evidence → Conclusion → Action
Mọi quyết định PHẢI tuân thủ pattern này:

```
Evidence: "Tôi đọc file X và tìm thấy Y"
Conclusion: "Do đó, tôi cần làm Z"
Action: "Thực thi Z"
```

CẤM: "Tôi nghĩ chúng ta nên...", "Có thể chúng ta có thể...", "Thực ra, hãy thử..."

### Quy tắc 4: Không Reactive Coding
CẤM:
- Viết tool mới để fix failing workflow
- Tạo batch_parser.py vì parser chậm
- Tạo helper.py cho one-time use
- Duplicate pipeline code để work around bug

YÊU CẦU:
- Fix root cause (abstraction layer)
- Nếu feature thiếu, extend abstraction
- Không patch trên top

### Quy tắc 5: Scratch Policy
Temporary files PHẢI vào `/scratch` hoặc `/temp`:
- One-time scripts
- Debug files
- Test outputs
- Intermediate data

Sau khi sử dụng, PHẢI xóa. Không commit vào main repo.

### Quy tắc 6: Không Execute trước
CẤM execute trước khi:
- ❌ Audit complete
- ❌ Plan approved bởi user
- ❌ Verification step passed
- ❌ Final audit passed

### Quy tắc 7: Self Verification
Sau mỗi phase, Host LLM PHẢI hỏi:
- "Output có khớp expected không?"
- "Skill Contract vẫn còn áp dụng không?"
- "Tôi có vi phạm Policy không?"
- "Golden Template có bị thay đổi không?"
- "Order Preservation vẫn còn đúng không?"

Nếu BẤT KỲ câu trả lời là "Không" → Quay lại, fix, re-verify.

## Execution Context

Khi Host LLM boot, nó PHẢI xây dựng execution context:

```json
{
  "repository_root": "d:\\CP crawl",
  "current_branch": "master",
  "current_commit": "29c2876",
  "repository_version": "v2.1",
  "target_version": "v3.0",
  "skills_available": [
    "cp-pipeline", "cp-crawler", "cp-parser",
    "translation-agent", "sample-explainer",
    "editorial-agent", "terminology-agent",
    "formatting-agent", "latex-agent",
    "latex-guardian", "semantic-fidelity-reviewer",
    "order-guardian", "qa-agent"
  ],
  "policies": [
    "repository_policy", "template_policy",
    "terminology_policy", "execution_state_machine"
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

Host LLM KHÔNG ĐƯỢC bỏ qua phases:

```
Phase 0 → Phase 1 (BẮT BUỘC)
Phase 1 FAIL → STOP
Phase 1 PASS → Phase 2 (BẮT BUỘC)
Phase 2 → Phase 3 (BẮT BUỘC cho major ops)
Phase 3 REJECTED → Quay về Phase 2
Phase 3 APPROVED → Phase 4 (BẮT BUỘC)
Phase 4 ERROR → Stop hoặc Rollback
Phase 4 SUCCESS → Phase 5 (BẮT BUỘC)
Phase 5 FAIL → Stop hoặc Fix rồi Phase 5 lại
Phase 5 PASS → Phase 6 (nếu applicable, else Phase 7)
Phase 6 FAIL → STOP, Fix issue
Phase 6 PASS → Phase 7 (BẮT BUỘC)
Phase 7 → Phase 8 (BẮT BUỘC)
Phase 8 FAIL → STOP, DO NOT commit
Phase 8 PASS → Phase 9 (BẮT BUỘC for release)
Phase 9 → Phase 10 (nếu release)
Phase 10 → Phase 11 (BẮT BUỘC)
```

## Tiêu chí thành công cho v3.0

Sau v3.0 upgrade, TẤT CẢ Host LLMs phải:

✅ Tuân thủ 11-phase state machine deterministically
✅ KHÔNG bao giờ execute trước audit và plan approval
✅ KHÔNG bao giờ make reactive decisions (try-error-guess)
✅ Luôn xác định Source of Truth trước khi sửa đổi
✅ Luôn thu thập evidence trước conclusions
✅ Luôn self-verify sau changes
✅ Luôn respect Skill Contracts và Policies
✅ KHÔNG bao giờ tạo unnecessary tools hoặc files
✅ Luôn cleanup artifacts
✅ Luôn pass final audit trước khi committing

Nếu BẤT KỲ Host LLM vi phạm rules này → Repository fails to load properly.
