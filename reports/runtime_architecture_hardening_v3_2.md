# Báo Cáo Hardening Kiến Trúc CP Pipeline V3.2 (Self-Improving & Root-Cause Driven)

**Trạng thái**: Hoàn tất 100% (All 12 Phases Verified)
**Ngày**: 2026-07-06

---

## 1. Tóm Tắt Kiến Trúc V3.2

CP Pipeline V3.2 là đợt nâng cấp toàn diện biến hệ thống thành một môi trường **Deterministic**, **Declarative**, **Repository-First**, và **Self-Improving**. Toàn bộ 12 giai đoạn cải tiến kiến trúc đã được thực thi và nghiệm thu thành công.

### Các Nguyên Tắc Vàng Được Khóa Chặt (Locked Guardrails):
1. **No Output Patching**: Tuyệt đối cấm mọi hành vi sửa chữa triệu chứng ở hạ nguồn (`outputs/output.tex`, `outputs/output.pdf`, `fix_output*.py`).
2. **Root-Cause Loop**: Mọi bug phải tuân thủ quy trình 11 bước tìm và sửa từ tầng gốc theo 9 phân loại tiêu chuẩn trong `.agents/policies/error_taxonomy.md` (`PARSER`, `NORMALIZER`, `TRANSLATOR`, `FORMATTER`, `LATEX`, `COMBINE`, `COMPILE`, `PDF`, `RUNTIME`). Cấm dùng `Misc`/`Unknown`.
3. **Declarative Dependencies**: Tất cả 20 Skills đều khai báo tường minh các phụ thuộc tại phần đầu file `SKILL.md` (`Runtime`, `Policies`, `Knowledge`, `Required Skills`, `Optional Skills`).
4. **Deterministic State Machine**: Quy trình điều phối của Host LLM hoạt động theo cỗ máy trạng thái 13 bước, kết thúc bằng `CONTINUOUS IMPROVEMENT` và `FINISH`.

---

## 2. Bảng Kiểm Định Sức Khỏe Kiến Trúc (V3.2 Test Matrix)

Hệ thống đã được kiểm thử với `tests/test_matrix.py` bao phủ trọn vẹn 20 tiêu chí kiến trúc và quy mô:

| # | Tiêu Chí Kiểm Định (Architectural Criteria) | Tool / Test | Kết Quả |
|---|---|---|---|
| 1 | No Root Pollution | `test_1_no_root_pollution` | **PASS** |
| 2 | No Temp Files at Root | `test_2_no_temp_files_at_root` | **PASS** |
| 3 | No Hardcoded Paths | `test_3_no_hardcoded_paths` | **PASS** |
| 4 | Single Source of Truth Template | `test_4_single_source_of_truth_template` | **PASS** |
| 5 | No Fake Compile Success | `test_5_no_fake_compile_success` | **PASS** |
| 6 | Output Contract | `test_6_output_contract` | **PASS** |
| 7 | Archive Contract | `test_7_archive_contract` | **PASS** |
| 8 | No Regex CP Parsing | `test_8_no_regex_cp_parsing` | **PASS** |
| 9 | Allowlist DOM & No Raw HTML | `test_9_allowlist_dom_no_raw_html` | **PASS** |
| 10 | No Python PDF OCR | `test_10_no_python_pdf_ocr` | **PASS** |
| 11 | Forbidden Architecture (No External LLM API) | `test_11_no_external_llm_api` | **PASS** |
| 12 | No Patch Scripts | `test_12_no_patch_scripts` | **PASS** |
| 13 | Declarative Dependency Graph | `test_13_declarative_dependency_graph` | **PASS** |
| 14 | Deterministic State Machine | `test_14_deterministic_state_machine` | **PASS** |
| 15 | Quality Gates Order | `test_15_quality_gates_order` | **PASS** |
| 16 | Error Taxonomy Compliance | `test_16_error_taxonomy_compliance` | **PASS** |
| 17 | Root Cause Loop Compliance | `test_17_root_cause_loop_compliance` | **PASS** |
| 18 | Knowledge Feedback Loop | `test_18_knowledge_feedback_loop` | **PASS** |
| 19 | No Speculative Language | `test_19_no_speculative_language` | **PASS** |
| 20 | Self-Improvement Enforcement | `test_20_self_improvement_enforcement` | **PASS** |

---

## 3. Nghiệm Thu Tự Tiến Hóa (Continuous Improvement Acceptance)

Đã thiết lập kịch bản kiểm chứng `tests/test_root_cause_loop_simulation.py` mô phỏng lỗi dịch thuật ký hiệu tiệm cận toán học ($O(N \log N)$). Kết quả chứng minh:
- Lỗi được phát hiện ngay tại cổng kiểm duyệt, phân loại chính xác là `TRANSLATOR` error.
- Hệ thống từ chối mọi nỗ lực vá lỗi ở hạ nguồn, buộc quay về tầng `translation-agent` để bổ sung luật bảo toàn toán học.
- Bài học được tự động ghi nhận vào `.agents/knowledge/root_causes.md` ("Asymptotic Notation Alteration").
- Toàn bộ 10 test scripts trong regression suite đều đạt `returncode == 0`.

---

## 4. Danh Sách Công Việc Đã Thực Hiện
1. **Hợp nhất Chính sách**: Hợp nhất `repository_cleanliness.md` vào `repository_policy.md`, xóa bỏ file thừa và `cp_pipeline_checklist.md` lỗi thời.
2. **Chuẩn hóa Ngôn ngữ**: Dọn dẹp English drift trong toàn bộ `README.md`, `cp-pipeline/SKILL.md`, `fragment-qa/SKILL.md` và `.agents/runtime/*.md`.
3. **Thêm Đồ thị Phụ thuộc**: Cập nhật `## Declarative Dependencies` cho toàn bộ 20 Skills trong repository.
4. **Chính sách Tự Cải tiến**: Ban hành `.agents/policies/self_improvement_policy.md` quy định bắt buộc 11 bước Root Cause Loop và Knowledge Feedback Loop.
5. **Cập nhật State Machine**: Đưa `CONTINUOUS IMPROVEMENT` thành State 12 chính thức trong cỗ máy trạng thái điều phối của Host LLM.
6. **Làm sạch Output Compiler**: Thêm cơ chế tự động dọn dẹp và di chuyển file aux (`*.aux`, `*.log`, `*.out`, `*.toc`) về `cache/debug/` sau compile, giữ cho `outputs/` sạch tuyệt đối.
