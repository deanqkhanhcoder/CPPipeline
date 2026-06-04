# REPOSITORY POLICY

Những quy định dưới đây là BẮT BUỘC, đóng vai trò như Guardrails bảo vệ tính toàn vẹn của Repository. Bất kỳ sự vi phạm nào cũng sẽ khiến PR/Commit bị reject.

## 1. Root sạch (Clean Root Directory)
Thư mục gốc (Root directory) phải luôn ở trạng thái sạch sẽ. CHỈ CÓ THỂ chứa:
- `README.md`
- `LICENSE`
- `requirements.txt`
- `.gitignore`
- Các thư mục chính (`.agents`, `archive`, `cache`, `outputs`, `reports`, `tools`).
Tuyệt đối KHÔNG LƯU các file debug, log rác, json rác, script nháp ở root. Mọi thứ phải được phân loại vào `cache/debug/` hoặc `reports/`.

## 2. Template là nguồn chân lý duy nhất (Single Source Of Truth)
File `.agents/skills/cp-latex/template.tex` là quy chuẩn duy nhất cho toàn bộ kết xuất PDF.
- Bất kỳ file tài liệu LaTeX nào được sinh ra cũng phải tuân thủ nghiêm ngặt, đọc và kế thừa toàn bộ cấu trúc (Title, Header, Footer) từ file template này.
- Nghiêm cấm mọi hành vi bypass, hardcode cấu trúc LaTeX trong các script Python.

## 3. Tool không được sinh layout (Logic Separation)
Các script/tools (ví dụ: `combine_latex.py`, `compile_latex.py`) có nhiệm vụ là cầu nối (glue code), phục vụ xử lý chuỗi và quản lý tiến trình.
- Tool KHÔNG ĐƯỢC PHÉP tự quyết định và sinh ra layout, design, hay font chữ mới.

## 4. Tool chỉ I/O
Các công cụ tự động hóa, script Python chỉ đảm nhiệm vai trò Input/Output (I/O).
- Gửi Request, Nhận Response, Đọc file, Ghi file, Bắn Log, Execute Lệnh hệ thống.
- Tuyệt đối không nhúng LLM logic phức tạp vào trong tool code.

## 5. LLM chịu trách nhiệm logic (LLM Responsibility)
- Khả năng đọc hiểu ngữ nghĩa, phân tách cấu trúc, dịch thuật và lý luận toán học hoàn toàn là trách nhiệm của mô hình Ngôn ngữ Lớn (LLM).
- Tool chỉ là cánh tay nối dài để LLM thao tác với đĩa và mạng. Mọi quyết định xử lý text phức tạp phải được prompt engineering thông qua LLM thay vì sử dụng regex hardcode chằng chịt.
