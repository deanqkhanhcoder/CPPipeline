---
name: cp-parser
description: Hướng dẫn Gemini cách parse raw HTML/Markdown thành Structured JSON.
---
## Nhiệm vụ
Gemini phải đọc nội dung raw HTML/Markdown từ công cụ crawl và tự suy luận để xuất ra cấu trúc JSON chuẩn. KHÔNG dùng Python script.

## Hướng dẫn nhận diện
- **Statement (Đề bài)**: Nhận diện nội dung mô tả cốt truyện và yêu cầu thuật toán.
- **Input/Output (Dữ liệu vào/ra)**: Nhận diện định dạng dữ liệu vào và dữ liệu ra.
- **Constraints (Ràng buộc)**: Giới hạn thời gian, bộ nhớ, giới hạn biến số (N, M, v.v.).
- **Samples (Ví dụ)**: Trích xuất các test case mẫu. Bắt buộc tạo trường `input`, `output`, `explanation`.

## Output
JSON với schema: name, source, statement, input, output, constraints, notes, samples.
