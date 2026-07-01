---
name: latex-agent
description: Chuyển đổi dữ liệu JSON thành mã nguồn LaTeX theo Golden Template.
version: 2.0.0
owner: latex-team
dependencies:
  - formatting-agent
compatible_pipeline: 2.x
---

# LaTeX Agent Contract

## Runtime
Host LLM đang thực thi Skill này. Skill không gọi bất kỳ LLM nào khác. Skill chỉ hướng dẫn Host LLM cách điền dữ liệu JSON vào Golden Template để sinh mã LaTeX.

## 1. Responsibility
Sinh mã nguồn `.tex` từ JSON. Điền các trường nội dung tương ứng vào các macro của `template.tex` như `\problem{...}`, `\begin{inputbox}`, `\begin{outputbox}`, `\begin{constraintbox}`, `\begin{samplecode}`.

## 2. Input Schema
JSON dữ liệu bài toán cuối cùng đã qua bước formatting.

## 3. Output Schema
String chứa mã nguồn `.tex` nguyên bản.

## 4. Forbidden Rules
- CẤM sinh thêm macro layout tự động như `\vspace`, `\\`, `\noindent`.
- CẤM dùng `\begin{lstlisting}` bên trong inputbox/outputbox.
- CẤM thay đổi cấu trúc của Golden Template.

## 5. Failure Mode & Retry Policy
Nếu text bị sai mã hóa, tự động sửa lỗi mojibake qua tool.
