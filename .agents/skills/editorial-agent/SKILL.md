---
name: editorial-agent
description: Biên tập câu chữ, cải thiện cấu trúc đoạn văn bản và tối ưu tính dễ đọc của bản dịch.
version: 2.0.0
owner: editorial-team
dependencies:
  - translation-agent
compatible_pipeline: 2.x
---

# Editorial Agent Contract

## Runtime
Host LLM đang thực thi Skill này. Skill không gọi bất kỳ LLM nào khác. Skill chỉ hướng dẫn Host LLM cách biên tập văn phong và chia đoạn.

## 1. Responsibility
Cải thiện văn phong dịch thuật, chia tách các khối văn bản quá dài (> 12 dòng) thành các paragraph logic nhỏ hơn. Tách biệt rõ ràng phần mở đầu truyện, mô tả thuật toán, quy tắc trò chơi, và mục tiêu bài toán.

## 2. Input Schema
JSON chứa bản dịch tiếng Việt từ `translation-agent`.

## 3. Output Schema
JSON tương tự Input nhưng văn phong mượt mà, cấu trúc đoạn rõ ràng, dễ hiểu như sách HSG.

## 4. Forbidden Rules
- CẤM làm thay đổi ý nghĩa thuật toán gốc.
- CẤM tạo các đoạn văn dài quá 12 dòng.
- CẤM chèn thêm thông tin giả định hoặc hallucinate.

## 5. Failure Mode & Retry Policy
Nếu văn phong không được cải thiện tốt hoặc lỗi xử lý, rollback về bản dịch thô ban đầu. Không retry.
