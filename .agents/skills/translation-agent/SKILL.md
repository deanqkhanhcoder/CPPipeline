---
name: translation-agent
description: Dịch thuật ngữ nghĩa chính xác từ tiếng Anh sang tiếng Việt, bảo toàn 100% toán học.
version: 2.0.0
owner: translation-team
dependencies:
  - cp-parser
compatible_pipeline: 2.x
---

# Translation Agent Contract

## 1. Responsibility
Dịch thô toàn bộ nội dung của đề bài toán Competitive Programming sang tiếng Việt, giữ nguyên vẹn 100% công thức toán học (`$...$`, `$$...$$`).

## 2. Input Schema
JSON chứa các trường: `statement`, `input`, `output`, `constraints`, `notes`, `samples`, `order_index`.

## 3. Output Schema
JSON tương tự Input nhưng nội dung text đã được dịch sang tiếng Việt.

## 4. Forbidden Rules
- CẤM thay đổi hoặc làm mất công thức toán học.
- CẤM dịch word-by-word (e.g. không dịch "You are given..." thành "Bạn được cho...").
- CẤM tự ý format bằng dấu gạch ngang hoặc xuống dòng thủ công.

## 5. Failure Mode & Retry Policy
Nếu bản dịch không đạt yêu cầu (ví dụ mất định dạng toán học), Host LLM phải tự phát hiện lỗi và sinh lại (Self-Correct). Thử lại tối đa 3 lần trước khi đánh dấu FAIL.

## 6. Self Improving
Lỗi dịch sai thuật ngữ hoặc mất toán sẽ được log vào `.agents/knowledge/quality_failures.md` để rút kinh nghiệm.
