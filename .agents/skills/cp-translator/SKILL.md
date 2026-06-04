---
name: cp-translator
description: Hướng dẫn Gemini cách dịch và sinh explanation cho Problem JSON.
---
## Nhiệm vụ
Gemini đọc cấu trúc parsed JSON và thực hiện dịch thuật toàn bộ sang tiếng Việt, đồng thời tự suy luận explanation nếu đề thiếu.

## Yêu cầu dịch
- Dịch sát nghĩa, chuẩn văn phong ICPC/HSG.
- Chuẩn hóa các thuật ngữ: graph, tree, query, edge, node, array, v.v.

## Yêu cầu sinh Explanation
- KHÔNG tạo câu chung chung kiểu "Kết quả hợp lệ".
- Phải đọc kĩ sample input và output, chạy tay thuật toán hoặc suy luận logic để chứng minh vì sao sinh ra output đó.
- Giải thích chi tiết, từng bước dễ hiểu.
