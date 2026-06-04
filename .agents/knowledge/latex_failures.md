# LATEX FAILURES KNOWLEDGE BASE

## 1. Constraintbox Undefined
**BUG:** Lỗi biên dịch `! LaTeX Error: Environment constraintbox undefined.` hoặc `! LaTeX Error: Environment codebg undefined.`
**ROOT CAUSE:** Template synchronization fail. File python tạo latex không đồng bộ với các macro được định nghĩa trong `template.tex`, hoặc subagent (LLM) đã tự ảo tưởng (hallucinate) ra các hàm và môi trường chưa từng được khai báo.
**FIX:** Ép buộc các subagent chỉ sử dụng đúng các lệnh từ Golden Template. Tạo bộ lọc regex dọn dẹp các lệnh không hợp lệ trước khi compile.
**PREVENTION RULE:**
- Output không bao giờ được sử dụng các macro / environment chưa được định nghĩa trong `template.tex`.
- Bất kỳ environment lạ nào phải bị xóa bỏ hoặc replace tự động về dạng text chuẩn trong pipeline trước khi biên dịch.

## 2. Fake PDF Success
**BUG:** Script python báo "Compilation successful!" mặc dù lệnh `pdflatex` báo lỗi và văn bản xuất ra không có thật.
**ROOT CAUSE:** Script chỉ đơn thuần kiểm tra sự tồn tại của file `output.pdf`. Nếu có một file PDF sót lại từ lần chạy cũ, nó sẽ lầm tưởng đó là kết quả của lần chạy này.
**FIX:** Xóa bỏ file PDF đích trước khi chạy lệnh biên dịch. Bắt buộc kiểm tra `res.returncode == 0`.
**PREVENTION RULE:**
- TRƯỚC KHI COMPILE: Bắt buộc phải xóa artifact cũ.
- SAU KHI COMPILE: Bắt buộc kiểm tra return code của trình biên dịch. Chỉ khi `returncode == 0` mới được kết luận PASS.

## 3. TOC Empty (Table of Contents rỗng)
**BUG:** LaTeX biên dịch ra PDF nhưng phần Mục lục (Table of Contents) không có một bài toán nào (trống).
**ROOT CAUSE:** LaTeX sử dụng kiến trúc hai bước để sinh mục lục: bước 1 tạo `.toc`, bước 2 chèn `.toc`. Việc chỉ chạy `pdflatex` 1 lần (Single pass) khiến TOC không bao giờ được nhúng vào PDF. Lỗi phụ: Dùng `\section*{...}` thay vì có cơ chế `\addcontentsline`.
**FIX:** Chạy `pdflatex` 2 lần. Cập nhật `\problem` macro để nhúng `\addcontentsline`.
**PREVENTION RULE:**
- LUÔN LUÔN compile 2 pass (`pdflatex` chạy 2 lần liên tiếp) khi có sử dụng `\tableofcontents`.

## 4. Template Bypass
**BUG:** File `output.tex` chứa một trang bìa khác biệt hoàn toàn với `template.tex`, thiếu thông tin logo, mất màu sắc.
**ROOT CAUSE:** Lỗi do người lập trình (hoặc script tự động) hardcode thẳng toàn bộ phần Header (chứa `\title`, `\maketitle`) trong file Python, "bypass" (bỏ qua) hoàn toàn nội dung chuẩn nằm trong file `template.tex`.
**FIX:** Sửa kịch bản Python để đọc nguyên gốc file `template.tex` và sử dụng nó làm vỏ bọc cho file đầu ra.
**PREVENTION RULE:**
- Tuyệt đối không hardcode layout, title, hay header/footer trong Python.
- Nguồn chân lý duy nhất (Single Source Of Truth): `.agents/skills/cp-latex/template.tex`. Bắt buộc phải load template này và điền nội dung vào vị trí Placeholder.
