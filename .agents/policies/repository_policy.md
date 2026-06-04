# REPOSITORY POLICY

Những quy định dưới đây là BẮT BUỘC, đóng vai trò như Guardrails bảo vệ tính toàn vẹn của Repository. Bất kỳ sự vi phạm nào cũng sẽ khiến PR/Commit bị reject.

## 1. NO ROOT POLLUTION (Root sạch)
Thư mục gốc (Root directory) phải luôn ở trạng thái sạch sẽ. CHỈ CÓ THỂ chứa:
- `README.md`
- `LICENSE`
- `requirements.txt`
- `.gitignore`
- Các thư mục chính (`.agents`, `archive`, `cache`, `outputs`, `reports`, `tools`).
Tuyệt đối KHÔNG LƯU các file debug, log rác (`compile_error.log`), json rác, script nháp ở root. Mọi thứ phải được phân loại vào `cache/debug/` hoặc `reports/`.

## 2. NO HARDCODED USER PATHS
Tuyệt đối CẤM hardcode tên người dùng (username), đường dẫn hệ thống cố định (như `C:\Users\toanpq\...`, `C:\Program Files\...`) vào bất kỳ script nào (vd: crawler). Phải sử dụng biến môi trường (Environment Variables) hoặc cơ chế tự động khám phá (Auto Discovery qua `os.environ`, `sys.platform`, `os.path.expanduser`) để đảm bảo tính khả chuyển (Portability) trên mọi OS: Windows, Linux, MacOS.

## 3. Template là nguồn chân lý duy nhất (Single Source Of Truth)
File `.agents/skills/cp-latex/template.tex` là quy chuẩn duy nhất cho toàn bộ kết xuất PDF.
- Bất kỳ file tài liệu LaTeX nào được sinh ra cũng phải tuân thủ nghiêm ngặt, đọc và kế thừa toàn bộ cấu trúc (Title, Header, Footer) từ file template này.
- Nghiêm cấm mọi hành vi bypass, hardcode cấu trúc LaTeX trong các script Python.

## 4. NO FAKE SUCCESS (Xác thực Biên dịch)
Quá trình biên dịch (Compile Pipeline) tuyệt đối không được báo PASS nếu thất bại.
- Bắt buộc kiểm tra `return code == 0`.
- Bắt buộc phải tự động xoá file PDF cũ trước khi chạy lệnh biên dịch mới để tránh trình trạng nhận diện nhầm file cũ thành công.

## 5. OUTPUT CONTRACT
Thư mục `outputs/` là khu vực xuất bản cuối cùng. Nó CHỈ ĐƯỢC PHÉP chứa các thành phẩm hoàn thiện.
- Các file trung gian (Intermediate files) phải nằm ở `cache/build/`.
- Sau khi LaTeX biên dịch thành công, tool biên dịch phải TỰ ĐỘNG DỌN DẸP (cleanup) các file phụ trợ sinh ra trong quá trình chạy (`*.aux`, `*.out`, `*.toc`, `*.log`).
- Cuối cùng chỉ giữ lại duy nhất: `outputs/output.tex` và `outputs/output.pdf`.

## 6. ARCHIVE CONTRACT
Lịch sử kết xuất phải được lưu giữ vĩnh viễn và có trật tự.
- Bắt buộc lưu vào `archive/<YYYY-MM-DD>/output_<seq>.pdf`.
- Phải cập nhật metadata đồng bộ vào `archive/index.json`.

## 7. Logic Separation & Tool Duty
Các script/tools (`tools/combine_latex.py`, `tools/compile_latex.py`) có nhiệm vụ là cầu nối (glue code), chỉ đảm nhiệm vai trò Input/Output (I/O).
- Gửi Request, Nhận Response, Đọc file, Ghi file, Bắn Log, Execute Lệnh hệ thống.
- Tool KHÔNG ĐƯỢC PHÉP tự quyết định và sinh ra layout, design, hay font chữ mới.
- Khả năng đọc hiểu ngữ nghĩa, phân tách cấu trúc, dịch thuật hoàn toàn là trách nhiệm của mô hình Ngôn ngữ Lớn (LLM). Mọi quyết định xử lý text phức tạp phải được prompt engineering thông qua LLM thay vì sử dụng regex hardcode chằng chịt.

## 8. NO PYTHON PDF PARSING / OCR (LLM-FIRST PDF)
Tuyệt đối NGHIÊM CẤM việc sử dụng Python để parse, OCR (như Tesseract, PaddleOCR), hoặc dùng Regex để trích xuất nội dung từ các file PDF đề bài. Các script chỉ được phép tải PDF hoặc chuyển đổi định dạng (PDF sang ảnh PNG làm fallback). Gemini phải là thực thể duy nhất chịu trách nhiệm đọc hiểu, suy luận, và phân tích cấu trúc statement từ PDF.
