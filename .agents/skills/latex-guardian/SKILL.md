---
name: latex-guardian
description: Người bảo vệ cú pháp LaTeX, kiểm duyệt bảo đảm tài liệu sạch lỗi biên dịch.
version: 2.0.0
owner: security-team
dependencies:
  - latex-agent
compatible_pipeline: 2.x
---

## Declarative Dependencies
- **Runtime**: `.agents/runtime/runtime.md`
- **Policies**: `.agents/policies/repository_policy.md`, `.agents/policies/template_policy.md`, `.agents/policies/error_taxonomy.md`
- **Knowledge**: `.agents/knowledge/latex_failures.md`, `.agents/knowledge/root_causes.md`
- **Required Skills**: None
- **Optional Skills**: None
- **Optional Knowledge**: None

# LaTeX Guardian Contract

## Runtime
Host LLM đang thực thi Skill này. Skill không gọi bất kỳ LLM nào khác. Skill chỉ hướng dẫn Host LLM cách kiểm tra và escape cú pháp LaTeX.

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
Nếu phát hiện lỗi cú pháp:
1. Xác định lỗi thuộc parser / formatting-agent / latex-agent / template / combine.
2. FAIL build nếu không thể sửa ở tầng sinh lỗi.
3. Tuyệt đối KHÔNG sinh script `fix_output*.py` hoặc regex patch lên `outputs/output.tex`.

## V3.1 Root-Cause Hardening

If any bug appears:
1. classify it using `.agents/policies/error_taxonomy.md`,
2. fix the producing layer only,
3. regenerate downstream artifacts,
4. verify with the matching gate.

Never patch `outputs/output.tex`, patch `outputs/output.pdf`, create `fix_output*.py`, regex-repair generated artifacts, or move a defect to another layer.
