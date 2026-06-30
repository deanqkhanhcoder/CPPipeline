# Hướng dẫn Khắc phục Lỗi LaTeX trong Competitive Programming Pipeline

Tài liệu này tổng hợp các lỗi LaTeX thường gặp, nguyên nhân, cách phát hiện và cách sửa đổi vĩnh viễn để tránh lỗi tái diễn.

## 1. TOC Empty Despite Successful Compile (Mục lục rỗng mặc dù PDF biên dịch thành công)

### Triệu chứng (Symptom)
- File PDF được biên dịch ra hoàn chỉnh, không có lỗi cú pháp LaTeX (`returncode == 0` từ `pdflatex`).
- Tuy nhiên, trang Mục lục (Table of Contents) hoàn toàn trống rỗng hoặc chỉ hiển thị tiêu đề mục lục mà không có danh sách các bài toán.

### Nguyên nhân (Root Cause)
- Macro `\problem{title}{source}` (hoặc macro tương tự dùng để vẽ tiêu đề bài toán) chỉ hiển thị giao diện đồ họa (e.g. `mdframed` box) mà không tạo ra các chỉ dẫn sinh TOC cho LaTeX (như `\addcontentsline` hoặc `\section` / `\subsection` / `\section*`).
- LaTeX không thể tự suy luận để đưa nội dung của `\problem` vào file `.toc`.

### Cách phát hiện (Detection Method)
- File `.toc` sinh ra sau compilation (e.g. `output.toc`) không chứa bất kỳ dòng `\contentsline` nào mô tả bài toán, hoặc chỉ chứa metadata Babel.
- Sử dụng script kiểm định tự động `tools/validate_toc.py` để so sánh số lượng `\problem{` trong `.tex` với số lượng `\contentsline` trong `.toc`.

### Cách sửa vĩnh viễn (Permanent Remedy)
- Định nghĩa macro `\problem` là **Single Source of Truth** cho việc tạo TOC.
- Cập nhật macro `\problem` trong `template.tex` để nó tự động gọi `\addcontentsline{toc}{section}{#1}` trước khi vẽ khung:
  ```latex
  \newcommand{\problem}[2]{%
    \addcontentsline{toc}{section}{#1}%
    \begin{mdframed}[...
    ]
    ...
    \end{mdframed}
  }
  ```
- Luôn kiểm soát chặt chẽ bằng cách giữ lại file `.toc` trong `cache/build/` để kiểm tra số lượng khớp trước khi hoàn tất build pipeline.
