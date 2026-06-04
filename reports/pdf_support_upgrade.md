# PDF SUPPORT UPGRADE REPORT

## Architecture Changes
Hệ thống CP Pipeline đã chính thức hỗ trợ luồng dữ liệu **PDF Statements** (các đề bài Olympiad truyền thống như IOI, APIO, CEOI...). Luồng xử lý được mở rộng dựa trên nguyên tắc lõi **LLM-First**:
- **Content Type Detection:** `tools/crawl_problem.py` được tích hợp hàm `is_pdf(url)` sử dụng `requests.head()` và kiểm tra chuỗi URL để phát hiện PDF (Content-Type: application/pdf).
- **Direct Download & Image Fallback:** Bất kỳ file PDF nào cũng được tải trực tiếp xuống `cache/pdf/`. Đồng thời, hệ thống sử dụng thư viện `PyMuPDF` (fitz) để kết xuất PDF thành ảnh chất lượng cao (150 DPI) lưu vào `cache/pdf_images/`.
- **Zero Python OCR:** Để đảm bảo không thất thoát dữ liệu toán học và giảm thiểu sai số, tôi đã cấm tuyệt đối việc sử dụng Tesseract, PaddleOCR hay PyPDF2 để bóc tách text. File JSON trung gian (`problem_raw.json`) sẽ báo cáo `type="pdf"` cùng đường dẫn tới các ảnh này. Gemini (Agent) sau đó sẽ sử dụng khả năng đọc tệp và Computer Vision siêu việt của mình để tự đọc đề.

## Files Modified
1. `requirements.txt`: Bổ sung `PyMuPDF>=1.23.0`.
2. `tools/crawl_problem.py`: Thêm module `is_pdf` và `crawl_pdf`. Hỗ trợ render sang nhiều trang ảnh. Bổ sung `User-Agent` để giảm thiểu tỉ lệ bị chặn 403.
3. `tools/cache_manager.py`: Mở rộng schema `save_cache` để tương thích các trường `type`, `pdf_path`, `images`.

## Skill Changes
1. `.agents/skills/cp-parser/SKILL.md`: Cập nhật chế độ **Xử lý PDF Statement**, hướng dẫn Gemini sử dụng `view_file` lên `cache/pdf_images/` để trực tiếp đọc ảnh.
2. `.agents/skills/cp-translator/SKILL.md`: Bổ sung chỉ thị suy luận logic và chạy tay giải thích (explanation) từ dữ liệu đọc được trên PDF.
3. `.agents/skills/cp-pipeline/SKILL.md`: Cập nhật lưu trình xử lý PDF Handling làm một pipeline bổ trợ song song với HTML Workflow.
4. `.agents/skills/cp-latex/SKILL.md`: Bổ sung luật không phân biệt HTML/PDF để đảm bảo Output duy nhất là Template chuẩn.

## Knowledge Updates
1. Tạo `.agents/knowledge/pdf_statement_handling.md`: Ghi chép chi tiết cách làm việc với PDF, bao gồm Direct PDF Reading, Image Fallback và Known Failure Modes (Toán học biến dạng, Nhiều bài gộp chung file).
2. Sửa `.agents/policies/repository_policy.md`: Thêm **Rule 8: NO PYTHON PDF PARSING / OCR** để đóng đinh nguyên tắc LLM-First vào kiến trúc bảo mật.

## Validation Results
- Khả năng cài đặt PyMuPDF: Thành công.
- Crawler chạy trên URL PDF (`github-git-cheat-sheet.pdf`):
  - Nhận diện đúng Content-Type.
  - Tải thành công `cache/pdf/bfcc4b2f.pdf`.
  - Tách thành công 2 trang ảnh `cache/pdf_images/bfcc4b2f_page_001.png` và `002.png`.
  - Lưu JSON metadata chính xác.
- Về luồng xử lý: Pipeline không còn crash khi đưa URL PDF. Subagent có đầy đủ tài nguyên tĩnh (ảnh và file PDF) trên ổ đĩa để tự phân tích.

## Coverage Matrix
| Source | Type | Parsing Backend | Supported |
|--------|------|-----------------|-----------|
| Codeforces | HTML | BeautifulSoup (Legacy) / Gemini Vision | ✅ YES |
| CSES | HTML | Gemini Vision | ✅ YES |
| IOI/APIO/CEOI | PDF | PyMuPDF -> Images -> Gemini Vision | ✅ YES |
| Any URL | PDF | PyMuPDF -> Images -> Gemini Vision | ✅ YES |
