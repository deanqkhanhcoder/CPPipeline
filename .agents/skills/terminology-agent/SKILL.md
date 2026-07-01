---
name: terminology-agent
description: Kiểm soát sự nhất quán của các thuật ngữ chuyên ngành Competitive Programming theo từ điển.
version: 2.0.0
owner: terminology-team
dependencies:
  - editorial-agent
compatible_pipeline: 2.x
---

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
