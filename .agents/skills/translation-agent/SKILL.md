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

## Runtime
Host LLM đang thực thi Skill này. Skill không gọi bất kỳ LLM nào khác. Skill chỉ hướng dẫn Host LLM cách dịch thuật và bảo toàn toán học.

## 1. Responsibility
Dịch **toàn bộ** nội dung đề bài Competitive Programming sang tiếng Việt, giữ nguyên vẹn 100% công thức toán học (`$...$`, `$$...$$`).

**Nguyên tắc cốt lõi: SEMANTICALLY LOSSLESS.**
Mọi thông tin có trong đề gốc phải còn tồn tại trong bản dịch. Đây là bản dịch — không phải tóm tắt, không phải blog, không phải tài liệu học.

- Nếu đề có 5 đoạn → bản dịch phải có đủ nội dung của 5 đoạn.
- Nếu đề có 3 ví dụ → bản dịch phải có đủ 3 ví dụ.
- Nếu đề có 8 bullet trong explanation → bản dịch phải có đủ 8 bullet.
- Nếu LLM nghĩ "câu này không quan trọng" → **vẫn phải dịch**.

**BẮT BUỘC: MỌI SAMPLE phải có Explanation.**
- Nếu đề gốc có explanation → dịch trung thực, không rút gọn.
- Nếu đề gốc KHÔNG có explanation → chuyển sang `sample-explainer` để tự sinh.

## 2. Input Schema
JSON chứa các trường: `statement`, `input`, `output`, `constraints`, `notes`, `samples`, `order_index`.

## 3. Output Schema
JSON tương tự Input nhưng nội dung text đã được dịch sang tiếng Việt.

## 4. Forbidden Rules
- CẤM thay đổi hoặc làm mất công thức toán học.
- CẤM dịch word-by-word (e.g. không dịch "You are given..." thành "Bạn được cho...").
- CẤM tự ý format bằng dấu gạch ngang hoặc xuống dòng thủ công.
- CẤM summarize, shorten, simplify bằng cách cắt nội dung.
- CẤM bỏ bất kỳ ví dụ (sample) nào.
- CẤM bỏ bất kỳ explanation nào.
- CẤM bỏ bất kỳ ghi chú (notes), warning, observation nào.
- CẤM gộp nhiều đoạn thành một nếu làm mất thông tin.
- CẤM tự diễn giải ngắn hơn — "tự nhiên" ≠ "ngắn".

## 5. Self-Review
Sau khi dịch xong, tự hỏi: **"Nếu mình chỉ có bản dịch này để giải bài, mình có bị thiếu bất kỳ thông tin nào so với đề gốc không?"** Nếu "Có" → dịch lại phần bị thiếu.

## 6. Failure Mode & Retry Policy
Nếu bản dịch không đạt yêu cầu (mất định dạng toán học, mất thông tin), Host LLM phải tự phát hiện lỗi và sinh lại (Self-Correct). Thử lại tối đa 3 lần trước khi đánh dấu FAIL.

## 7. Self Improving
Lỗi dịch sai thuật ngữ hoặc mất toán sẽ được log vào `.agents/knowledge/quality_failures.md` để rút kinh nghiệm.
