# Báo cáo Khắc phục Nóng Mã hóa (Encoding Hotfix Report)

## Tóm tắt Sự cố
Hệ thống phát hiện tình trạng hỏng mã hóa tiếng Việt (mojibake) nghiêm trọng trên diện rộng, ảnh hưởng trực tiếp đến các file mã nguồn, file cấu hình và tài liệu của repository (hiện tượng các ký tự tiếng Việt bị thay thế bằng dấu `?`, ví dụ: `H?p ??ng l?i`).

## Nguyên nhân Cốt lõi (Root Cause Hypothesis)
Nguyên nhân gốc rễ là do môi trường thực thi (Python trên hệ điều hành Windows) sử dụng mã hóa mặc định là `cp1252` thay vì `utf-8` khi gọi các hàm I/O như `open()` hoặc `Path.write_text()`. Việc thiếu tham số `encoding="utf-8"` tường minh trong các script đã khiến tiếng Việt bị đọc và ghi sai định dạng, dẫn đến hỏng file vĩnh viễn trên ổ cứng.

## Kết quả Quét và Khôi phục
Hệ thống đã tiến hành quét toàn bộ repository và sử dụng thư mục sao lưu `d:\CPPipeline_recovery` để tự động phục hồi.

### 1. Số lượng File Bị Hỏng (Corrupted Files Found): 17
1. `README.md`
2. `.agents/policies/template_policy.md`
3. `.agents/policies/terminology.md`
4. `.agents/skills/cp-crawler/SKILL.md`
5. `.agents/skills/cp-latex/SKILL.md`
6. `.agents/skills/cp-parser/SKILL.md`
7. `.agents/skills/cp-pipeline/SKILL.md`
8. `.agents/skills/cp-translator/SKILL.md`
9. `.agents/skills/pdfmaker/scripts/translate_md.py`
10. `archive/index.json`
11. `archive/2026-06-04/output_001.tex`
12. `reports/crawler_queue_migration.md`
13. `reports/documentation_audit.md`
14. `reports/encoding_audit.md`
15. `reports/final_repository_audit.md`
16. `tools/audit_encoding.py`
17. `tools/run_repository_audit.py`

*(Lưu ý: Một số file như `audit_encoding.py` hoặc các báo cáo audit có thể chứa dấu `?` một cách hợp lệ dưới dạng mã Regex hoặc trích dẫn lỗi, nhưng vẫn được đưa vào diện nghi ngờ do chứa pattern giống mojibake).*

### 2. Số lượng File Phục hồi Thành công (Recovered Files): 11
Các file đã được tự động copy từ `CPPipeline_recovery` sang, đảm bảo mã hóa UTF-8 hoàn chỉnh:
- `README.md`
- `.agents/skills/cp-crawler/SKILL.md`
- `.agents/skills/cp-latex/SKILL.md`
- `.agents/skills/cp-parser/SKILL.md`
- `.agents/skills/cp-pipeline/SKILL.md`
- `.agents/skills/cp-translator/SKILL.md`
- `archive/index.json`
- `archive/2026-06-04/output_001.tex`
- `reports/crawler_queue_migration.md`
- `reports/final_repository_audit.md`
- `tools/run_repository_audit.py` (File này sau đó được khôi phục thủ công bằng mã nguồn chính xác để tương thích với repository hiện tại).

### 3. Số lượng File Không thể Phục hồi (Unrecoverable Files): 6
Các file này không tồn tại trong thư mục backup `CPPipeline_recovery`. Để tuân thủ nghiêm ngặt nguyên tắc **"Không tự bịa ra văn bản tiếng Việt"**, các file này được giữ nguyên trạng thái chưa phục hồi:
- `.agents/policies/template_policy.md`
- `.agents/policies/terminology.md`
- `.agents/skills/pdfmaker/scripts/translate_md.py`
- `reports/documentation_audit.md`
- `reports/encoding_audit.md`
- `tools/audit_encoding.py` (Script Python này vẫn hoạt động bình thường, các dấu `?` thực chất là Regex hợp lệ).

## Biện pháp Ngăn chặn (Preventive Measures)
Hệ thống đã quét toàn bộ các file Python trong repository (bao gồm cả thư mục `.agents/skills/`) và tự động chèn thêm tham số `encoding="utf-8"` vào tất cả các lệnh gọi `open()`, `read_text()`, và `write_text()`. 
Các script được vá bao gồm:
- `.agents\skills\caveman-compress\scripts\benchmark.py`
- `.agents\skills\caveman-compress\scripts\compress.py`
- `.agents\skills\caveman-compress\scripts\detect.py`
- `.agents\skills\caveman-compress\scripts\validate.py`
- `.agents\skills\pdfmaker\pdfmaker\config\settings.py`
- `.agents\skills\pdfmaker\pdfmaker\converter\datalab.py`
- `tools\crawl_problem.py`

## Rủi ro Còn lại (Remaining Risks)
- Các file không thể phục hồi (`.agents/policies/*.md`) đang chứa tiếng Việt bị lỗi, có thể gây khó hiểu cho con người hoặc Agent khác khi đọc.
- Bất kỳ công cụ external nào hoặc Agent tương lai sử dụng lệnh hệ thống của Windows (như `echo` hoặc shell tools không hỗ trợ UTF-8 native) để đọc/ghi file vẫn có nguy cơ gây hỏng mã hóa nếu không cấu hình ép kiểu về `utf-8`.
