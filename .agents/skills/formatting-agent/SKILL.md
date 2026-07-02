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

**BắT BUỘC: Mọi sample phải có Explanation đầy đủ.**

## 2. Input Schema
JSON có chứa trường `input`, `output`, `samples` và `explanation`.

## 3. Output Schema
JSON với các trường I/O được định dạng mạch lạc, tách biệt từng mục con.

## 4. Forbidden Rules
- CẤM để `input` và `output` dính trên cùng một dòng.
- CẤM làm hỏng nội dung code của sample testcases.
- CẤM bỏ bất kỳ sample nào — số sample đầu ra phải bằng số sample đầu vào.
- CẤM bỏ explanation của bất kỳ sample nào.
- CẤM gộp nội dung giữa các sample khác nhau.
- CẤM để trống trường `explanation` — nếu thiếu, FAIL và yêu cầu `sample-explainer` bổ sung.
- CẤM thay đổi `display_title` — phải giữ nguyên vẹn từ `translation-agent`.

## 5. Failure Mode & Retry Policy
Nếu format lỗi, chạy lại bước `tools/text_normalizer.py`.
