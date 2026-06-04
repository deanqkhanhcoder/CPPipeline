# PDF STATEMENT HANDLING

Tài liệu này quy định cách hệ thống CP Pipeline xử lý các bài toán ở định dạng PDF (đặc biệt là đề thi Olympiad như IOI, APIO, CEOI...).

## HTML Workflow vs PDF Workflow

**HTML Workflow:**
1. Crawler tải mã HTML/Markdown từ Codeforces, CSES.
2. Lưu vào `cache/problemset/<id>.json`.
3. LLM (Parser) đọc văn bản text thuần túy để phân tách cấu trúc.

**PDF Workflow:**
1. Crawler phát hiện URL là PDF (dựa trên đuôi `.pdf` hoặc Content-Type).
2. Tải trực tiếp file PDF vào `cache/pdf/<id>.pdf`.
3. Sử dụng `PyMuPDF` để tự động render từng trang PDF thành ảnh chất lượng cao lưu tại `cache/pdf_images/<id>_page_<N>.png`.
4. Crawler lưu JSON meta-data vào `cache/problemset/<id>.json` chỉ định rõ `type="pdf"` cùng đường dẫn `pdf_path` và mảng `images`.

## Chế Độ Đọc PDF (LLM-First)

Hệ thống hoạt động theo triết lý **LLM-First**. Nghiêm cấm hoàn toàn việc sử dụng Python để bóc tách văn bản, OCR (Tesseract, PaddleOCR), hoặc parse nội dung. 

- **Direct PDF Reading:** Gemini sử dụng `view_file` nạp trực tiếp file `.pdf` từ `cache/pdf/`. Gemini có khả năng tự động đọc hiểu PDF.
- **Image Fallback:** Nếu file PDF dạng scan, hoặc lỗi font toán học, Gemini sử dụng `view_file` nạp danh sách ảnh từ `cache/pdf_images/` để đọc và phân tích bằng Computer Vision.

## Yêu Cầu Đối Với LLM
- Khả năng tự luận: LLM phải tự trích xuất Title, Statement, Input, Output, Constraints, Samples.
- Khả năng giải thích (Explanation): Nếu PDF chứa dữ liệu mẫu, LLM phải đọc hiểu dữ liệu trên ảnh và tự suy luận cách giải thích từng bước (Step-by-step logic) giống như đối xử với HTML.

## Known Failure Modes
1. **Toán học biến dạng (Math Deformation):** File PDF chứa font toán học đặc biệt, nếu parse bằng text thuần túy sẽ bị mất ký hiệu. -> Giải pháp: Dùng Image Fallback.
2. **Nhiều bài toán trong một file PDF:** Đề Olympiad thường gộp chung 3 bài trong 1 file. LLM có thể bị nhầm lẫn giữa các bài. -> Tránh truyền URL gộp, hoặc prompt LLM bóc tách từng bài (Cần logic parser phức tạp hơn ở tương lai).
3. **Quá giới hạn kích thước:** File PDF quá lớn vượt qua token limit của Model. -> Fallback sang chia nhỏ ảnh hoặc chỉ nạp text mỏng.
