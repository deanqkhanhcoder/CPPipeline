---
name: cp-translator
description: Hướng dẫn Gemini cách dịch và sinh explanation cho Problem JSON.
---
## Nhiệm vụ
Gemini đọc cấu trúc parsed JSON và thực hiện dịch thuật toàn bộ sang tiếng Việt, đồng thời tự suy luận explanation nếu đề thiếu.

## Yêu cầu dịch
- Dịch sát nghĩa, chuẩn văn phong ICPC/HSG.
- Chuẩn hóa các thuật ngữ: graph, tree, query, edge, node, array, v.v.

## Yêu cầu sinh Explanation (Bao gồm cả PDF)
- KHÔNG tạo câu chung chung kiểu "Kết quả hợp lệ".
- Phải đọc kĩ sample input và output (dù lấy từ văn bản HTML hay ảnh chụp PDF của đề IOI/APIO), chạy tay thuật toán hoặc suy luận logic để chứng minh vì sao sinh ra output đó.
- Giải thích chi tiết, từng bước dễ hiểu.

## Lessons Learned
1. Đôi khi bản dịch tự động bị thay đổi logic của bài toán nếu LLM cố gắng "viết lại cho hay" thay vì giữ nguyên toán học cốt lõi.
2. Sinh giải thích sai lầm (hallucinate) nếu thuật toán của bài toán quá phức tạp mà LLM không suy luận đúng.

## Anti Regression Rules
- **Rule 1**: BẢO TOÀN LOGIC (Preserve meaning). Tuyệt đối không được thay đổi ý nghĩa thuật toán, điều kiện kiểm tra, hay ràng buộc số học của bài toán.
- **Rule 2**: Nếu việc tự sinh giải thích (explanation) vượt quá khả năng suy luận logic chắc chắn, hãy bỏ trống trường explanation thay vì sinh ra một lý thuyết sai lệch gây nhầm lẫn.

## Known Failure Modes
- Dịch sai cụm từ chuyên môn (ví dụ `subsegment` dịch thành `mảng con` thay vì `đoạn con liên tiếp`).
- Làm mất dấu ngoặc, công thức toán học nội tuyến (inline math `$...$`) khi dịch.
