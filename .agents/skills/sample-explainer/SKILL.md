---
name: sample-explainer
description: Tạo explanation cho mọi Sample. Nếu website có sẵn thì dịch, nếu không có thì tự sinh bằng suy luận từ đề bài và dữ liệu mẫu.
version: 2.1.0
compatible_pipeline: 2.x
---

# Sample Explainer Contract

## Runtime
Host LLM đang thực thi Skill này. Skill không gọi bất kỳ LLM nào khác. Skill hướng dẫn Host LLM cách tạo explanation cho Sample.

## 1. Responsibility

Đảm bảo **MỌI SAMPLE** đều có **Explanation** đầy đủ.

### Nếu website có Explanation:
- Giữ nguyên.
- Dịch trung thực.
- Không sửa.
- Không rút gọn.

### Nếu website KHÔNG có Explanation:
- Host LLM phải tự sinh bằng suy luận từ:
  - Statement (đề bài)
  - Input Format (định dạng đầu vào)
  - Output Format (định dạng đầu ra)
  - Constraints (ràng buộc)
  - Sample Input (dữ liệu mẫu)
  - Sample Output (kết quả mẫu)

## 2. Explanation Requirements

Explanation phải đủ chi tiết để:

> **Một học sinh mới đọc đề có thể hiểu ngay sample.**

Không được chỉ viết:
- "Kết quả là 5."
- "The answer is obvious."
- "Output matches input."

Phải viết:
- Ban đầu có gì.
- Các bước thực hiện.
- Sau mỗi bước có gì.
- Kết quả cuối cùng là gì và tại sao.

## 3. Explanation Format

```markdown
### Giải thích

Ban đầu: [mô tả trạng thái khởi đầu]

Bước 1: [mô tả thao tác]
→ Kết quả: [trạng thái sau bước 1]

Bước 2: [mô tả thao tác]
→ Kết quả: [trạng thái sau bước 2]

...

Do đó: [kết luận logic]

Kết quả cuối cùng là: [output và lý do]
```

## 4. Độ Chi Tiết

- Nếu sample có **5 dòng dữ liệu** → giải thích đầy đủ từng dòng.
- Nếu có **nhiều bước** → mỗi bước đều phải mô tả.
- Nếu có **nhiều test case** → mỗi test đều có explanation riêng.

## 5. When Cannot Reason

Nếu:
- Sample quá lớn (> 100 dòng)
- Không đủ dữ kiện để suy luận chính xác

→ Host LLM phải ghi rõ:

```
**Lưu ý:** Không thể suy luận chính xác toàn bộ quá trình từ dữ liệu mẫu do [lý do].
Dưới đây là phân tích một phần dựa trên thông tin có sẵn:
[giải thích được đến đâu thì giải thích]
```

## 6. Forbidden Rules

- CẤM bịa input.
- CẤM bịa output.
- CẤM bịa thuật toán.
- CẤM bịa dữ kiện.
- CẤM bịa quy tắc.
- CẤM để trống explanation (trừ khi ghi rõ "không đủ thông tin").
- CẤM viết editorial thuật toán — chỉ giải thích sample, không giải thích cách giải bài.

Chỉ được suy luận từ:
- Đề bài
- Sample Input
- Sample Output
- Logic hiển nhiên từ đề

## 7. Input Schema

```json
{
  "statement": "...",
  "input": "...",
  "output": "...",
  "constraints": "...",
  "samples": [
    {
      "input": "...",
      "output": "...",
      "explanation": "..." // có thể rỗng nếu website không có
    }
  ]
}
```

## 8. Output Schema

```json
{
  "statement": "...",
  "input": "...",
  "output": "...",
  "constraints": "...",
  "samples": [
    {
      "input": "...",
      "output": "...",
      "explanation": "..." // BẮT BUỘC phải có nội dung
    }
  ]
}
```

## 9. Example - Website Có Explanation

**Input (English):**
```
Sample 1:
Input: 3 5
Output: 8
Explanation: 3 + 5 = 8
```

**Output (Vietnamese):**
```
Mẫu 1:
Đầu vào: 3 5
Đầu ra: 8
Giải thích: 3 + 5 = 8
```

## 10. Example - Website KHÔNG Có Explanation

**Input (đề bài: "Tính tổng hai số"):**
```
Sample 1:
Input: 3 5
Output: 8
Explanation: (trống)
```

**Output (Host LLM tự sinh):**
```
Mẫu 1:
Đầu vào: 3 5
Đầu ra: 8

Giải thích:
Ban đầu có hai số: 3 và 5.
Theo đề bài, ta cần tính tổng của chúng.
3 + 5 = 8
Do đó, kết quả đầu ra là 8.
```

## 11. Anti-Regression

Pipeline FAIL nếu:
- Bất kỳ sample nào không có explanation (trừ khi ghi rõ "không đủ thông tin").
- Explanation chỉ có 1 câu ngắn không giải thích gì.
- Explanation bị bỏ qua trong quá trình dịch.

## 12. Failure Mode & Retry Policy

Nếu Host LLM không thể sinh explanation hợp lý sau 2 lần thử:
- Ghi rõ: "Không thể suy luận chính xác..."
- Giải thích được đến đâu thì giải thích.
- KHÔNG được để trống hoàn toàn.
