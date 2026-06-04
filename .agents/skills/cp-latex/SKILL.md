---
name: cp-latex
description: Hướng dẫn Gemini tạo mã LaTeX chuẩn từ JSON theo Golden Template.
---
## Nhiệm vụ
Gemini tự viết toàn bộ nội dung file `.tex` dựa trên dữ liệu đã dịch, TUÂN THỦ CHÍNH XÁC Golden Template.

## LATEX QUALITY RULES
1. Output phải GIỐNG PHONG CÁCH Template chuẩn (`template.tex`).
2. Dùng `mdframed` nhất quán: `\problem` box, `inputbox`, `outputbox`, `constraintbox`.
3. Dùng `\titlepage` đầy đủ với styling như template.
4. Dùng `\tableofcontents` đầy đủ và `\newpage`.
5. Section phải có màu `sectioncolor`. Dùng gói `titlesec` để styling.
6. Header/Footer phải đẹp, sử dụng gói `fancyhdr`.
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
Tuyệt đối KHÔNG DÙNG `\usepackage{fontspec}` và `\setmainfont`. Compiler mặc định là `latexmk -pdf`.

## Validation
Trước khi lưu file, kiểm tra:
1. Có statement chưa? 2. Có input chưa? 3. Có output chưa? 4. Có constraints chưa? 5. Có sample chưa? 6. Có explanation chưa? 7. Có định nghĩa đủ các macro, mdframed và màu sắc chưa?
Nếu thiếu -> FAIL.
