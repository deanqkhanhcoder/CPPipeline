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

## Lessons Learned
1. LLM đôi khi sinh thiếu trường bắt buộc (như `samples` bị rỗng) nếu HTML quá phức tạp.
2. Dữ liệu toán học có thể bị làm hỏng nếu Parser không giữ nguyên định dạng MathJax/LaTeX.

## Anti Regression Rules
- **Rule 1**: Bắt buộc giữ nguyên vẹn 100% công thức toán học (`$$`, `\(\)`).
- **Rule 2**: Nếu không tìm thấy I/O hoặc Samples, phải gán bằng mảng rỗng `[]` hoặc báo cáo lỗi, không được điền dữ liệu ảo giác.

## Known Failure Modes
- Parser bị lừa bởi các trang web có cấu trúc lạ không theo chuẩn Codeforces/CSES.
- Thất bại trong việc trích xuất bảng Sample Input/Output nếu nó sử dụng cấu trúc `div` lồng nhau phức tạp thay vì `pre` hoặc `table`.
