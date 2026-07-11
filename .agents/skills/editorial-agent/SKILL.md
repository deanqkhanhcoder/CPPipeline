---
name: editorial-agent
description: Biên tập câu chữ, cải thiện cấu trúc đoạn văn bản và tối ưu tính dễ đọc của bản dịch.
version: 2.0.0
owner: editorial-team
dependencies:
  - translation-agent
compatible_pipeline: 2.x
---

## Declarative Dependencies
- **Runtime**: `.agents/runtime/runtime.md`
- **Policies**: `.agents/policies/repository_policy.md`, `.agents/policies/terminology.md`, `.agents/policies/error_taxonomy.md`
- **Knowledge**: `.agents/knowledge/root_causes.md`
- **Required Skills**: None
- **Optional Skills**: None
- **Optional Knowledge**: None

# Editorial Agent Contract

## Runtime
Host LLM đang thực thi Skill này. Skill không gọi bất kỳ LLM nào khác. Skill chỉ hướng dẫn Host LLM cách biên tập văn phong và chia đoạn.

## 1. Responsibility
Cải thiện văn phong dịch thuật, chia tách các khối văn bản quá dài (> 12 dòng) thành các paragraph logic nhỏ hơn. Tách biệt rõ ràng phần mở đầu truyện, mô tả thuật toán, quy tắc trò chơi, và mục tiêu bài toán.

**Giới hạn cứng:** Biên tập chỉ được phép thay đổi cách diễn đạt, cấu trúc câu, chia đoạn. Không được xóa bất kỳ thông tin nào. "Biên tập" ≠ "Rút ngắn".

## 2. Input Schema
JSON chứa bản dịch tiếng Việt từ `translation-agent`.

## 3. Output Schema
JSON tương tự Input nhưng văn phong mượt mà, cấu trúc đoạn rõ ràng, dễ hiểu như sách HSG.

## 4. Forbidden Rules
- CẤM làm thay đổi ý nghĩa thuật toán gốc.
- CẤM tạo các đoạn văn dài quá 12 dòng.
- CẤM chèn thêm thông tin giả định hoặc hallucinate.
- CẤM xóa hoặc gộp bullet points nếu làm giảm số lượng.
- CẤM bỏ bất kỳ notes, warning, explanation, observation nào dù ngắn.
- CẤM summarize — nếu đoạn gốc có 5 ý, biên tập xong vẫn phải có 5 ý.

## 5. Failure Mode & Retry Policy
Nếu văn phong không được cải thiện tốt hoặc lỗi xử lý, rollback về bản dịch thô ban đầu. Không retry.

## V3.1 Root-Cause Hardening

If any bug appears:
1. classify it using `.agents/policies/error_taxonomy.md`,
2. fix the producing layer only,
3. regenerate downstream artifacts,
4. verify with the matching gate.

Never patch `outputs/output.tex`, patch `outputs/output.pdf`, create `fix_output*.py`, regex-repair generated artifacts, or move a defect to another layer.
