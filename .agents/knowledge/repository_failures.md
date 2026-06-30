# REPOSITORY FAILURES KNOWLEDGE BASE

## 1. Root Pollution
**BUG:** Thư mục gốc (Root directory) chứa đầy rác như `temp.txt`, `verify_output.log`, `crawl_test.py`.
**ROOT CAUSE:** Việc debug được thực hiện một cách cẩu thả, tạo file test tại bất kỳ vị trí nào và không dọn dẹp sau khi làm xong.
**FIX:** Chuyển toàn bộ các file tạm bợ vào thư mục cache hoặc debug chuyên biệt.
**PREVENTION RULE:**
- KHÔNG BAO GIỜ lưu file debug ở thư mục Root.
- Thư mục gốc CHỈ CHỨA các file cốt lõi: `README.md`, `LICENSE`, `requirements.txt`, `.gitignore` và các thư mục chính của dự án.

## 2. Intermediate Tex Pollution
**BUG:** Hàng chục file `.tex` đơn lẻ (tương ứng với mỗi bài toán) nằm vương vãi chung với file kết quả cuối cùng.
**ROOT CAUSE:** Việc lưu file đầu ra của quá trình translate/parse chung một thư mục gây lộn xộn.
**FIX:** Cách ly file trung gian.
**PREVENTION RULE:**
- Mọi file `.tex` trung gian từ các bài toán riêng lẻ PHẢI ĐƯỢC CHỨA TRONG `cache/build/`.
- Thư mục `outputs/` CHỈ CHỨA DUY NHẤT file `output.tex` và `output.pdf` cuối cùng.

## 3. Runtime Logs Pollution
**BUG:** Log hệ thống, log biên dịch, log lỗi xuất hiện rải rác.
**ROOT CAUSE:** Chạy file không kiểm soát thư mục làm việc của output.
**FIX:** Phân luồng dữ liệu log.
**PREVENTION RULE:**
- Mọi báo cáo, báo cáo lỗi (run audit) PHẢI ĐƯỢC CHỨA TRONG `reports/`.
- Log lỗi biên dịch tạm thời (`compile_error.log`) có thể lưu ở root tạm thời nhưng sau đó nên được dọn dẹp hoặc dời đi.
