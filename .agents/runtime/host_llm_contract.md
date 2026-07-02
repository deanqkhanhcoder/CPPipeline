---
title: Host LLM Runtime Specification
version: 3.0.0
type: Architecture
---

# Host LLM Runtime Contract

## Definition

**Host LLM** là AI mà người dùng đang chat với. Nó chính là Runtime duy nhất của CPPipeline.

Ví dụ về Host LLM:
- Antigravity
- Gemini CLI
- Claude Code
- Cursor
- Codex
- Copilot Agent
- ChatGPT

## Principle: Skill-First Bootstrap

Host LLM knows ONLY about Skills it's asked to invoke:
- User: `/cp-pipeline`
- Host LLM: Finds `cp-pipeline/SKILL.md`
- SKILL.md: "First, load `.agents/runtime/runtime.md`"
- Host LLM: Loads runtime as instructed
- Runtime: Takes over and orchestrates execution

**Host LLM does NOT**:
- Scan `.agents/runtime/` on its own
- Discover Runtime before reading Skill
- Assume where Runtime is located

**Host LLM DOES**:
- Read Skill.md (given by user command)
- Follow Skill's bootstrap instructions
- Load dependencies declared by Skill
- Delegate execution to Runtime

Không được:
- Thực hiện task trước khi đọc Policy
- Sửa code trước khi kiểm tra Skill
- Tự suy diễn trước khi kiểm tra Knowledge

## Principle: Evidence First

Mọi quyết định phải theo:
```
Evidence (từ Repository) 
   ↓
Source of Truth (chỉ định một thành phần đúng)
   ↓
Conclusion (suy luận logic)
   ↓
Action (thực hiện)
```

Cấm suy luận "maybe", "probably", "let's try".

## Principle: No Reactive Coding

Cấm:
- Tạo tool mới nếu repository đã có abstraction
- Duplicate pipeline, parser, translator, latex generator
- Vá tầng trên khi tầng dưới mới là Source of Truth

Nếu cần sửa: **sửa đúng abstraction**.

## Principle: Self-Verification

Sau mỗi bước, Host LLM tự hỏi:
- Output đúng chưa?
- Có vi phạm Policy không?
- Có mất dữ liệu không?
- Có rút gọn quá mức không?
- Có vi phạm Golden Template không?

Nếu "Có" → FAIL, không kết thúc.

## Skill Dependencies

Mỗi Skill phải khai báo:
```
- Dependencies (Skill cần load trước)
- Required Policy
- Required Knowledge
- Required Terminology
```

Host LLM tự resolve dependency graph.

## Execution Guarantee

Bất kỳ Host LLM nào (Gemini, Claude, Cursor, Copilot) đều phải:
1. Hiểu ngay cách Runtime hoạt động
2. Thực hiện cùng một quy trình
3. Sinh cùng kết quả
4. Không phụ thuộc vào "cách suy nghĩ" riêng
