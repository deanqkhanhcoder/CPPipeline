---
name: qa-agent
description: Đánh giá chất lượng toàn diện của tài liệu đầu ra thông qua 5 tiêu chí cốt lõi.
version: 2.0.0
owner: QA-team
dependencies:
  - latex-guardian
compatible_pipeline: 2.x
---

# QA Agent Contract

## Runtime
Host LLM đang thực thi Skill này. Skill không gọi bất kỳ LLM nào khác. Skill chỉ hướng dẫn Host LLM cách chấm điểm và đánh giá chất lượng tài liệu LaTeX.

## 1. Responsibility
Chấm điểm chất lượng (từ 1.0 đến 5.0) trên **6 phương diện**: Statement, Explanation, Formatting, Markdown Conversion, Readability, **Semantic Fidelity**.

`Semantic Fidelity` = không mất thông tin so với đề gốc. Điểm 1.0 nếu bản dịch mất bất kỳ sample/explanation/notes/warning nào.

**KIỂM TRA BẮT BUỘC: Mọi sample phải có Explanation.**
Nếu bất kỳ sample nào thiếu explanation → điểm Explanation = 1.0 → FAIL.

**KIỂM TRA BẮT BUỘC: display_title phải đúng format.**
Format chuẩn: **Tên tiếng Việt (Tên tiếng Anh)**
- Ví dụ đúng: "Bắt tay (Handshake)", "A. Dưa hấu (Watermelon)"
- Sai: "Handshake", "Bắt tay", "Handshake (Bắt tay)", "BẮT TAY"
Nếu sai format → điểm Statement = 1.0 → FAIL. 

## 2. Input Schema
Đường dẫn đến file LaTeX cần đánh giá.

## 3. Output Schema
Báo cáo điểm số cụ thể kèm theo danh sách các vi phạm nếu có.

## 4. Forbidden Rules
- CẤM bỏ qua bước chấm điểm.
- CẤM cho PASS nếu điểm trung bình hoặc điểm bất kỳ hạng mục nào dưới 4.0.
- CẤM cho PASS nếu `Semantic Fidelity` < 4.0 (tức là có mất thông tin so với đề gốc).
- CẤM cho PASS nếu bất kỳ sample nào thiếu explanation (trừ khi ghi rõ "không đủ thông tin để suy luận").
- CẤM cho PASS nếu `display_title` không đúng format "Tên tiếng Việt (Tên tiếng Anh)".
- CẤM cho PASS nếu TOC, bookmark, header, footer không dùng `display_title`.

## v3.0: Phase Awareness
Skill này là cuối cùng của PHASE 5 (VERIFY) trong State Machine.
- Host LLM phải thực hiện toàn bộ 6 audits: Repository, Skill, Policy, Template, Language, Encoding
- Nếu ANY FAIL → STOP, không commit (Phase 9 bị block)
- Nếu ALL PASS → Proceed to Phase 6 (Regression) nếu có modified components
- Không được "assume pass" - phải explicit PASS mọi tiêu chí

## 5. Failure Mode & Retry Policy
Nếu chất lượng không đạt, chặn đứng quá trình combine và kết xuất PDF.
