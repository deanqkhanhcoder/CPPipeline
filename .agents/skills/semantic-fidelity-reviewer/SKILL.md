---
name: semantic-fidelity-reviewer
description: Kiểm tra tính toàn vẹn ngữ nghĩa (Semantic Fidelity) của bản dịch. So sánh đề gốc với bản dịch để phát hiện bất kỳ thông tin nào bị mất, bị rút gọn, hoặc bị bỏ sót.
version: 2.1.0
compatible_pipeline: 2.x
---

## Declarative Dependencies
- **Runtime**: `.agents/runtime/runtime.md`
- **Policies**: `.agents/policies/repository_policy.md`, `.agents/policies/error_taxonomy.md`
- **Knowledge**: `.agents/knowledge/root_causes.md`
- **Required Skills**: None
- **Optional Skills**: None
- **Optional Knowledge**: None

# Semantic Fidelity Reviewer Contract

## Runtime
Host LLM đang thực thi Skill này. Skill không gọi bất kỳ LLM nào khác. Skill hướng dẫn Host LLM cách so sánh ngữ nghĩa giữa đề gốc và bản dịch.

## 1. Responsibility

So sánh **đề gốc (Original)** với **bản dịch (Translation)** và xác nhận không có thông tin nào bị mất.

Repository này tạo **bản dịch**, không phải tóm tắt, không phải blog, không phải tài liệu học. Mọi thông tin trong đề gốc phải còn tồn tại trong bản dịch.

## 2. Fidelity Checklist

Kiểm tra từng mục. FAIL ngay nếu bất kỳ mục nào bị thiếu hoặc bị rút gọn mất thông tin:

```
□ Title (Tiêu đề)
□ Story / Context (Cốt truyện / Bối cảnh — nếu có)
□ Problem Statement (Mô tả bài toán — đầy đủ từng câu)
□ Input Format (Định dạng đầu vào — đầy đủ)
□ Output Format (Định dạng đầu ra — đầy đủ)
□ Constraints (Ràng buộc — mọi dòng, mọi biến)
□ Notes (Ghi chú)
□ Warning (Cảnh báo — nếu có)
□ Observations (Nhận xét — nếu có)
□ Editorial Hint (Gợi ý thuật toán — nếu có)
□ Every paragraph (Mọi đoạn văn)
□ Every bullet point (Mọi bullet — số lượng phải khớp)
□ Every numbered step (Mọi bước có đánh số — số lượng phải khớp)
□ Every Sample (Mọi ví dụ mẫu — số lượng phải khớp)
□ Every Sample Explanation (Mọi giải thích ví dụ)
□ Every formula / math expression (Mọi công thức)
□ Every table (Mọi bảng)
□ Every image description (Mọi mô tả hình — nếu có)
□ Every footnote (Mọi chú thích — nếu có)
```

## 3. Anti-Regression Rules

Bản dịch **tự động FAIL** nếu vi phạm bất kỳ điều nào sau:

- Số lượng Sample trong bản dịch < số lượng Sample trong đề gốc
- Số lượng bullet trong một đoạn giảm so với đề gốc
- Số lượng bước (numbered steps) giảm so với đề gốc
- Explanation ngắn hơn vì bị bỏ ý
- Notes biến mất
- Warning biến mất
- Edge case biến mất
- Số đoạn văn giảm do summarize

## 4. Self-Review Question

Sau khi review, Host LLM phải tự hỏi:

> **"Nếu mình chỉ có bản dịch này để giải bài, mình có bị thiếu bất kỳ thông tin nào so với đề gốc không?"**

- Nếu **"Có"** → **FAIL**. Phải yêu cầu dịch lại phần bị thiếu.
- Nếu **"Không"** → **PASS**.

## 5. Output Schema

```json
{
  "status": "PASS | FAIL",
  "missing_elements": ["danh sách các phần bị thiếu — rỗng nếu PASS"],
  "verdict": "Mô tả ngắn lý do PASS hoặc FAIL"
}
```

## 6. Forbidden Rules

- CẤM PASS nếu có bất kỳ thông tin nào bị thiếu, dù nhỏ.
- CẤM bỏ qua các phần "tưởng là không quan trọng" (ghi chú, warning, edge case).
- CẤM so sánh độ dài văn bản — phải so sánh nội dung ngữ nghĩa.

## 7. Failure Mode & Retry Policy

Nếu FAIL:
1. Trả về danh sách `missing_elements`.
2. Yêu cầu `translation-agent` bổ sung lại phần bị thiếu.
3. Chạy lại review. Tối đa 2 lần retry trước khi đánh dấu pipeline FAIL.

## V3.1 Root-Cause Hardening

If any bug appears:
1. classify it using `.agents/policies/error_taxonomy.md`,
2. fix the producing layer only,
3. regenerate downstream artifacts,
4. verify with the matching gate.

Never patch `outputs/output.tex`, patch `outputs/output.pdf`, create `fix_output*.py`, regex-repair generated artifacts, or move a defect to another layer.
