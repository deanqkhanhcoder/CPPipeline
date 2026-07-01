---
name: latex-guardian
description: Người bảo vệ cú pháp LaTeX, kiểm duyệt bảo đảm tài liệu sạch lỗi biên dịch.
version: 2.0.0
owner: security-team
dependencies:
  - latex-agent
compatible_pipeline: 2.x
---

# LaTeX Guardian Contract

## 1. Responsibility
Kiểm soát cú pháp LaTeX thô, đảm bảo escape chính xác các ký tự đặc biệt như `%`, `&`, `_`, `{`, `}` bên ngoài các môi trường math/code, kiểm tra các thẻ môi trường đã đóng đủ chưa (math/table/list environments).

## 2. Input Schema
Chuỗi mã nguồn `.tex` sinh ra từ `latex-agent`.

## 3. Output Schema
Chuỗi mã nguồn LaTeX đã được làm sạch và hợp lệ 100% (hoặc FAIL nếu lỗi quá nặng).

## 4. Forbidden Rules
- CẤM bỏ sót bất kỳ ký tự đặc biệt nào chưa được escape.
- CẤM để lại markdown chưa chuyển đổi trong file LaTeX.

## 5. Failure Mode & Retry Policy
Nếu phát hiện lỗi cú pháp, tự động áp dụng regex escape để tự phục hồi. Nếu không thể sửa được, ném Exception dừng build.
