---
name: cp-latex
description: Hướng dẫn Gemini tạo mã LaTeX chuẩn từ JSON theo Golden Template.
---
## Nhiệm vụ
Gemini tự viết toàn bộ nội dung file `.tex` dựa trên dữ liệu đã dịch, TUÂN THỦ CHÍNH XÁC Golden Template.

## LATEX QUALITY RULES (GOLDEN TEMPLATE LOCK)
LUẬT MỚI: Template duy nhất là `.agents/skills/cp-latex/template.tex` - Single Source Of Truth.
Mọi `\titlepage`, `\tableofcontents`, header, footer, và macro ĐỀU PHẢI ĐƯỢC LẤY TỪ ĐÂY.
KHÔNG ĐƯỢC tự sinh hay hardcode trong Python script.
1. Output phải GIỐNG PHONG CÁCH Template chuẩn (`template.tex`).
2. Dùng `mdframed` nhất quán: `\problem` box, `inputbox`, `outputbox`, `constraintbox`.
3. KHÔNG ĐƯỢC PHÂN BIỆT nguồn gốc dữ liệu là HTML hay PDF. Dù bài toán được crawl từ file PDF của Olympiad hay từ trang HTML Codeforces, file LaTeX output cuối cùng phải hoàn toàn giống nhau về mặt định dạng, không được thêm bớt macro nào khác ngoài Template.
4. KHÔNG tự sáng tạo layout mới. KHÔNG đơn giản hóa. Học thuộc từng macro và sử dụng chính xác.
7. Explanation phải mang tính giảng dạy, phân tích. Bắt đầu bằng macro `\explanation`.
8. Constraints phải chuẩn hóa trong `constraintbox` hoặc `itemize` dưới macro `\constraints`.
9. Listings phải có background màu xám (`codebg`), viền đơn `rulecolor`. Khai báo `\lstset` chuẩn.
10. KHÔNG tự sáng tạo layout mới. KHÔNG đơn giản hóa. Học thuộc từng macro và sử dụng chính xác.

## Đặc tả Font Tiếng Việt BẮT BUỘC
BẮT BUỘC khai báo:
```latex
\usepackage[utf8]{inputenc}
\usepackage[T5]{fontenc}
\usepackage[vietnamese]{babel}
```
Tuyệt đối KHÔNG DÙNG `\usepackage{fontspec}` và `\setmainfont`. Compiler mặc định là `pdflatex` (2 pass).

## Validation (STRICT LATEX CONTRACT)
Tuyệt đối KHÔNG ĐƯỢC hallucinate các macro như `\exmp`, `\exmpin`, `\exmpout`, `\inputformat`, `\outputformat`, `\begin{exmpIn}`, v.v.
Chỉ được sử dụng chính xác các macro đã được định nghĩa trong Golden Template:
- Dùng `\section*{Dữ liệu vào}` thay vì `\inputformat`
- Dùng `\section*{Dữ liệu ra}` thay vì `\outputformat`
- Dùng `\begin{example} \begin{inputbox} ... \end{inputbox} \begin{outputbox} ... \end{outputbox} \end{example}` cho các ví dụ.
- Dùng `\begin{constraintbox} ... \end{constraintbox}` cho giới hạn.

Trước khi lưu file và báo PASS, BẮT BUỘC kiểm tra:
1. Có statement chưa? 2. Có input chưa? 3. Có output chưa? 4. Có constraints chưa? 5. Có sample chưa? 6. Có explanation chưa?
Nếu thiếu -> FAIL.

Khi kết luận thành công ở bước biên dịch (Compile), PHẢI kiểm tra log `compile_error.log`.
Nếu log chứa: `LaTeX Error`, `Fatal Error`, `Undefined` => FAIL. Không được báo PASS.

## Lessons Learned
1. **constraintbox undefined**: Lỗi sinh ra khi output sử dụng một environment hoặc macro chưa bao giờ được định nghĩa trong `template.tex`.
2. **Template Bypass**: Lỗi sinh ra khi python script (combine) không dùng template.tex mà tự hardcode LaTeX header.
3. **TOC Empty**: Lỗi do trình biên dịch pdflatex chỉ được gọi 1 lần (single pass). Mục lục yêu cầu 2 lần chạy.

## Anti Regression Rules
- **Rule 1**: Output TUYỆT ĐỐI KHÔNG ĐƯỢC sử dụng environment/macro lạ.
- **Rule 2**: LUÔN COMPILE 2 pass khi dùng `\tableofcontents` để sinh mục lục động.
- **Rule 3**: Single Source Of Truth duy nhất là `template.tex`. Không tự sinh hay hardcode header/footer ở file khác.

## Known Failure Modes
- Hallucination các lệnh `\exmp`, `\codebg`, `\example` gây vỡ layout và Too deeply nested.
- Quên chèn `\addcontentsline` khiến TOC bị rỗng.
