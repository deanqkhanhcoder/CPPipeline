---
name: latex-agent
description: Chuyển đổi dữ liệu JSON thành mã nguồn LaTeX theo Golden Template.
version: 2.0.0
owner: latex-team
dependencies:
  - formatting-agent
compatible_pipeline: 2.x
---

## Declarative Dependencies
- **Runtime**: `.agents/runtime/runtime.md`
- **Policies**: `.agents/policies/repository_policy.md`, `.agents/policies/template_policy.md`, `.agents/policies/error_taxonomy.md`
- **Knowledge**: `.agents/knowledge/latex_failures.md`, `.agents/knowledge/root_causes.md`
- **Required Skills**: `.agents/skills/latex-guardian/SKILL.md`
- **Optional Skills**: None
- **Optional Knowledge**: None

# LaTeX Agent Contract

## Runtime
Host LLM đang thực thi Skill này. Skill không gọi bất kỳ LLM nào khác. Skill chỉ hướng dẫn Host LLM cách điền dữ liệu JSON vào Golden Template để sinh mã LaTeX.

## 1. Responsibility
Sinh mã nguồn `.tex` fragment từ JSON. Fragment chỉ là phần thân bài toán, KHÔNG chứa `\documentclass`, `\usepackage`, title page, hoặc `\tableofcontents`.

Macro được phép từ `template.tex`:
- `\problem{display_title}{source}`
- `\inputformat`
- `\outputformat`
- `\constraints ... \endconstraints`
- `\example`
- `\explanation`

Mọi macro/environment khác phải là LaTeX chuẩn đã có package trong `template.tex` (`itemize`, `enumerate`, `tabularx`, `longtable`, `lstlisting`, math).

**BẮT BUỘC: Sử dụng `display_title` làm tiêu đề.**
Mọi nơi cần tiêu đề (\section, \problem, bookmark, TOC, header, footer) đều phải lấy từ `display_title`.

Không được:
- Tự dịch `title`
- Tự format lại
- Tỹ đảo thứ tự
- Dùng `translated_title` thay vì `display_title`
- Dùng `title` thay vì `display_title`

## 2. Input Schema
JSON dữ liệu bài toán cuối cùng đã qua bước formatting.

## 3. Output Schema
String chứa mã nguồn `.tex` nguyên bản.

## 4. Forbidden Rules
- CẤM sinh thêm macro layout tự động như `\vspace`, `\\`, `\noindent`.
- CẤM sinh macro/environment không có trong `template.tex` như `inputbox`, `outputbox`, `constraintbox`, `samplebox`, `examplebox`, `codebg`, `exmp`.
- CẤM đặt list/table/code/math hoặc newline bên trong đối số `\problem{...}{...}`.
- CẤM thay đổi cấu trúc của Golden Template.
- CẤM tự dịch hoặc format lại `title` — chỉ dùng `display_title`.
- CẤM dùng `title` hoặc `translated_title` trong bất kỳ macro nào — phải dùng `display_title`.
- CẤM truyền raw Markdown, HTML, Mermaid, JSON, YAML vào LaTeX.
- Nếu cần sửa `outputs/output.tex`, STOP: sửa generator/formatting/parser rồi regenerate.

## 5. Failure Mode & Retry Policy
Nếu text bị sai mã hóa, tự động sửa lỗi mojibake qua tool.

## V3.1 Root-Cause Hardening

If any bug appears:
1. classify it using `.agents/policies/error_taxonomy.md`,
2. fix the producing layer only,
3. regenerate downstream artifacts,
4. verify with the matching gate.

Never patch `outputs/output.tex`, patch `outputs/output.pdf`, create `fix_output*.py`, regex-repair generated artifacts, or move a defect to another layer.
