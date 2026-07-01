---
name: formatting-agent
description: Tách biệt rõ ràng cấu trúc các phần Input, Output, Constraints và Sample Cases.
version: 2.0.0
owner: formatting-team
dependencies:
  - terminology-agent
compatible_pipeline: 2.x
---

# Formatting Agent Contract

## Runtime
Host LLM đang thực thi Skill này. Skill không gọi bất kỳ LLM nào khác. Skill chỉ hướng dẫn Host LLM cách chuẩn hóa cấu trúc I/O và Sample Cases.

## 1. Responsibility
Chuẩn hóa cấu trúc và cách trình bày của các phần dữ liệu đầu vào (Input), đầu ra (Output) và các ví dụ (Samples). Đảm bảo chúng nằm trong khối độc lập và không dính vào nhau.

## 2. Input Schema
JSON có chứa trường `input`, `output`, `samples` và `explanation`.

## 3. Output Schema
JSON với các trường I/O được định dạng mạch lạc, tách biệt từng mục con.

## 4. Forbidden Rules
- CẤM để `input` và `output` dính trên cùng một dòng.
- CẤM làm hỏng nội dung code của sample testcases.

## 5. Failure Mode & Retry Policy
Nếu format lỗi, chạy lại bước `tools/text_normalizer.py`.
