# Chính sách template

## Bất biến
- `.agents/templates/template.tex` là Single Source Of Truth.
- Chỉ được chèn body giữa `% CONTENT_START` và `% CONTENT_END`.
- Không được rewrite, tối ưu, beautify, hay sinh lại template.
- Không được thêm package, màu, font, title page, TOC, header, footer, hoặc macro mới ngoài thay đổi giao diện có chủ đích.
- Mỗi build phải kiểm tra hash trong `.agents/metadata/template_hash.txt` trước khi tạo `outputs/output.tex`.
- Hash lệch -> fail build.

## Vùng động duy nhất
- `[[PROBLEM_COUNT]]` trên title page.
- Phải thay bằng số `\problem` thực tế có trong PDF cuối.
- Nếu `[[PROBLEM_COUNT]]` hoặc hardcoded count label còn sót lại -> fail build.

## V3.1 Fragment Contract

Allowed fragment macros are the golden-template macros only: `\problem`, `\inputformat`, `\outputformat`, `\constraints`, `\example`, `\explanation`, plus standard LaTeX list/math/text macros supported by the template.

Obsolete fragment macros are forbidden: `inputbox`, `outputbox`, `constraintbox`, `examplebox`, `samplebox`, `codebg`, `exmp`.

Raw Markdown, HTML, Mermaid, SVG, JSON/YAML markers, and UI chrome must not enter LaTeX fragments.
