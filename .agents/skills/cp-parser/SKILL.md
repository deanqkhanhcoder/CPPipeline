---
name: cp-parser
description: Hướng dẫn Gemini cách parse raw HTML/Markdown thành Structured JSON.
---
## Nhiệm vụ
Gemini phải đọc nội dung HTML fragment từ `cache/normalized/<id>.json` (trường `content`) và tự suy luận để xuất ra cấu trúc JSON chuẩn. KHÔNG dùng Python script.

**QUAN TRỌNG**: Đọc `cache/normalized/<id>.json`, KHÔNG đọc `cache/problemset/<id>.json`. File normalized đã được extract chỉ còn phần `.problem-statement` (~5-50KB thay vì 100-270KB raw HTML). Đọc raw sẽ lãng phí 97% token.

## Hướng dẫn nhận diện (PDF Quality - Phase 5)
- **Statement (Đề bài)**: Nhận diện nội dung mô tả cốt truyện và yêu cầu thuật toán.
- **Input/Output (Dữ liệu vào/ra)**: Nhận diện định dạng dữ liệu vào và dữ liệu ra. Bắt buộc tách biệt rõ ràng, không được trộn lẫn hoặc viết liền nhau.
- **Constraints (Ràng buộc)**: Giới hạn thời gian, bộ nhớ, giới hạn biến số (N, M, v.v.).
- **Samples (Ví dụ)**: Trích xuất các test case mẫu. Bắt buộc tạo trường `input`, `output`, `explanation`. Các ví dụ phải được cấu trúc độc lập trong block code, không được dính liền với nội dung văn bản.

## Output
JSON với schema: name, source, statement, input, output, constraints, notes, samples, order_index.
- **Chú ý:** Trường `order_index` là bắt buộc để duy trì thứ tự bài toán trong PDF đầu ra.

## Xử lý PDF Statement (LLM-First)
Nếu bài toán được cung cấp dưới dạng PDF:
- **Direct PDF Reading (Ưu tiên):** Sử dụng tool `view_file` để đọc trực tiếp nội dung văn bản từ file PDF (lưu tại `cache/pdf/`).
- **Image Fallback:** Nếu PDF chỉ chứa ảnh hoặc văn bản bị lỗi font (toán học không hiển thị đúng), Gemini phải sử dụng tool `view_file` để nạp các file ảnh chụp PDF (lưu tại `cache/pdf_images/`).
- **Nghiêm cấm OCR bằng Python:** Mọi quá trình trích xuất, nhận diện ký tự, phân tích hình học trang PDF PHẢI do Gemini tự thực hiện bằng Computer Vision. Không được dùng bất kỳ tool/script Python nào để trích xuất text.

## Bài học kinh nghiệm
1. LLM đôi khi sinh thiếu trường bắt buộc (như `samples` bị rỗng) nếu HTML quá phức tạp.
2. Dữ liệu toán học có thể bị làm hỏng nếu Parser không giữ nguyên định dạng MathJax/LaTeX.

## Luật chống đứt gãy
- **Rule 1**: Bắt buộc giữ nguyên vẹn 100% công thức toán học (`$$`, `\(\)`).
- **Rule 2**: Nếu không tìm thấy I/O hoặc Samples, phải gán bằng mảng rỗng `[]` hoặc báo cáo lỗi, không được điền dữ liệu ảo giác.
- **Rule 3**: BẮT BUỘC giữ nguyên vẹn trường `order_index` từ JSON đầu vào sang JSON đầu ra. Tuyệt đối không được bỏ qua hoặc làm thay đổi giá trị này.

## Token Optimization Rules
- PHẢI đọc từ `cache/normalized/<id>.json` field `content` (html fragment đã được extract)
- KHÔNG ĐƯỢC đọc `cache/problemset/<id>.json` (raw HTML - quá lớn, lãng phí token)
- Nếu `cache/normalized/<id>.json` chưa tồn tại, yêu cầu orchestrator chạy: `python tools/extract_html.py <id>`

## Lỗi đã biết
- Parser bị lừa bởi các trang web có cấu trúc lạ không theo chuẩn Codeforces/CSES.
- Thất bại trong việc trích xuất bảng Sample Input/Output nếu nó sử dụng cấu trúc `div` lồng nhau phức tạp thay vì `pre` hoặc `table`.
- Parser đọc raw HTML 100KB+ từ cache/problemset → token overflow, chi phí tăng 100x.
