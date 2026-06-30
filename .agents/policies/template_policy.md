# Chính sách template

## Bất biến
- `.agents/skills/cp-latex/template.tex` là Single Source Of Truth.
- Chỉ được chèn body giữa `% CONTENT_START` và `% CONTENT_END`.
- Không được rewrite, tối ưu, beautify, hay sinh lại template.
- Không được thêm package, màu, font, title page, TOC, header, footer, hoặc macro mới ngoài thay đổi giao diện có chủ đích.
- Mỗi build phải kiểm tra hash trong `.agents/metadata/template_hash.txt` trước khi tạo `outputs/output.tex`.
- Hash lệch -> fail build.

## Vùng động duy nhất
- `[[PROBLEM_COUNT]]` trên title page.
- Phải thay bằng số `\problem` thực tế có trong PDF cuối.
- Nếu `[[PROBLEM_COUNT]]` hoặc hardcoded count label còn sót lại -> fail build.
