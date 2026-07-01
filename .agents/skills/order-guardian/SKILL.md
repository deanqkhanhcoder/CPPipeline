---
name: order-guardian
description: Bảo đảm thứ tự hiển thị của các bài toán trong PDF luôn khớp 100% với URL đầu vào.
version: 2.0.0
owner: QA-team
dependencies:
  - cp-pipeline
compatible_pipeline: 2.x
---

# Order Guardian Contract

## 1. Responsibility
Đối chiếu thứ tự các bài toán từ: URL đầu vào -> Queue -> PDF -> TOC -> Metadata. Đảm bảo chúng khớp nhau hoàn toàn 100% dựa trên chỉ số `order_index`.

## 2. Input Schema
Metadata của Queue (`cache/queue/index.json`) và Danh sách các file `.tex` được sắp xếp trong `cache/build/`.

## 3. Output Schema
Boolean (True/False) khẳng định tính nhất quán của thứ tự bài toán.

## 4. Forbidden Rules
- CẤM để xảy ra hiện tượng lệch thứ tự hiển thị của bất kỳ bài toán nào.

## 5. Failure Mode & Retry Policy
Nếu phát hiện lệch thứ tự, lập tức dừng pipeline (FAIL), ném lỗi yêu cầu sắp xếp lại.
