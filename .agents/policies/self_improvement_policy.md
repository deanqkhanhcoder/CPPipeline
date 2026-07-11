---
type: Policy
description: Chính sách tự tiến hóa và cải tiến liên tục sau mỗi lỗi (Self-Improvement & Continuous Improvement Policy).
---

# Chính Sách Tự Tiến Hóa (Self-Improvement Policy)

Hệ thống CP Pipeline được thiết kế theo mô hình **Self-Improving** và **Root-Cause Driven**. Host LLM không chỉ có nhiệm vụ sửa lỗi tạm thời khi phát hiện bug, mà bắt buộc phải thực hiện quy trình tự tiến hóa để ngăn lỗi tái diễn vĩnh viễn.

## 1. Vòng lặp Root Cause (Root Cause Loop)
Mọi lỗi phát sinh trong quá trình thực thi (từ crawl, parse, dịch thuật đến compile LaTeX) phải tuyệt đối tuân thủ chu trình 11 bước:
1. **Detect**: Phát hiện lỗi qua Quality Gates (Fragment QA, Compile rc != 0, PDF QA).
2. **Classify**: Phân loại lỗi chính xác theo 9 lớp trong `.agents/policies/error_taxonomy.md`. Cấm dùng `Unknown/Misc/Other`.
3. **Root Cause**: Truy tìm nguyên nhân gốc tại tầng sinh ra lỗi (Parser, Formatter, LaTeX Agent...).
4. **Fix tầng gốc**: Chỉ sửa code/skill/template tại tầng sinh lỗi. Cấm vá lỗi ngọn (`output.tex`, `output.pdf`, `fix_output*.py`).
5. **Regression Test**: Chạy bộ kiểm định để đảm bảo không vỡ tính năng hiện tại.
6. **Knowledge Update**: Cập nhật bài học mới vào `.agents/knowledge/root_causes.md`.
7. **Skill Update**: Bổ sung quy tắc ngăn ngừa vào `SKILL.md` của tầng tương ứng.
8. **Policy Update**: Cập nhật chính sách guardrail nếu cần thiết.
9. **Runtime Update**: Cập nhật State Machine hoặc kiểm duyệt Runtime nếu có lỗ hổng luồng.
10. **Documentation Update**: Đồng bộ tài liệu và báo cáo.
11. **Acceptance Test**: Chạy lại toàn bộ kiểm định nghiệm thu.

## 2. Vòng lặp phản hồi Kiến thức (Knowledge Feedback Loop)
Sau mỗi lỗi thực tế, Host LLM bắt buộc trả lời chuỗi kiểm định tự đánh giá:
- Lỗi này có cần cập nhật **Skill** không? (Nếu Có -> Cập nhật; Nếu Không -> Ghi rõ lý do tại sao Skill hiện tại đã đủ).
- Lỗi này có cần cập nhật **Runtime** không?
- Lỗi này có cần cập nhật **Policy** không?
- Lỗi này có cần cập nhật **Knowledge** không?
- Lỗi này có cần cập nhật **Test** không?
- Lỗi này có cần cập nhật **Documentation** không?

## 3. Tiêu chí Đánh giá (Fail Condition)
Nếu một lỗi có khả năng tái diễn trong tương lai mà Host LLM chỉ sửa code tạm thời, không cập nhật hệ thống (Skill, Policy, Test, Knowledge) theo chu trình trên -> **FAIL**.
