---
name: terminology-agent
description: Kiểm soát sự nhất quán của các thuật ngữ chuyên ngành Competitive Programming theo từ điển.
version: 2.0.0
owner: terminology-team
dependencies:
  - editorial-agent
compatible_pipeline: 2.x
---

## Declarative Dependencies
- **Runtime**: `.agents/runtime/runtime.md`
- **Policies**: `.agents/policies/repository_policy.md`, `.agents/policies/terminology.md`, `.agents/policies/error_taxonomy.md`
- **Knowledge**: `.agents/knowledge/root_causes.md`
- **Required Skills**: None
- **Optional Skills**: None
- **Optional Knowledge**: None

# Terminology Agent Contract

## Runtime
Host LLM đang thực thi Skill này. Skill không gọi bất kỳ LLM nào khác. Skill chỉ hướng dẫn Host LLM cách chuẩn hóa thuật ngữ theo từ điển CP.

## 1. Responsibility
Đối chiếu bản dịch với danh sách từ điển thuật ngữ chuyên ngành lập trình thi đấu trong `.agents/policies/terminology.md`. Sửa các từ dịch sai/lệch (e.g. sửa `subsegment` thành `đoạn con liên tiếp`, `constraints` thành `ràng buộc`).

## 2. Input Schema
JSON văn bản tiếng Việt sau khi đã biên tập.

## 3. Output Schema
JSON tiếng Việt với các thuật ngữ được chuẩn hóa hoàn toàn 100%.

## 4. Forbidden Rules
- CẤM bỏ qua từ điển thuật ngữ.
- CẤM dịch các biến, tên hàm, tên class sang tiếng Việt.

## 5. Failure Mode & Retry Policy
Quét và thay thế bằng regex nếu LLM không thể match hết.

## V3.1 Root-Cause Hardening

If any bug appears:
1. classify it using `.agents/policies/error_taxonomy.md`,
2. fix the producing layer only,
3. regenerate downstream artifacts,
4. verify with the matching gate.

Never patch `outputs/output.tex`, patch `outputs/output.pdf`, create `fix_output*.py`, regex-repair generated artifacts, or move a defect to another layer.
