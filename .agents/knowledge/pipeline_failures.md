# Hướng dẫn Khắc phục Lỗi Pipeline trong Competitive Programming Pipeline

Tài liệu này ghi nhận các lỗi kiến trúc cấp pipeline, nguyên nhân, cách khắc phục và phòng ngừa.

## 1. Parallel Completion Reordering Bug (Lỗi Xáo trộn Thứ tự do Hoàn thành Song song)

### Triệu chứng (Symptom)
- Người dùng gửi danh sách các URL bài toán theo thứ tự mong muốn: A, B, C, D.
- Tuy nhiên, file PDF cuối cùng và trang Mục lục (TOC) hiển thị theo thứ tự bị xáo trộn, ví dụ: B, D, A, C.

### Nguyên nhân (Root Cause)
- Pipeline sử dụng queue, crawler workers, translator workers, và subagents để xử lý song song.
- Do tốc độ mạng, cấu trúc trang web khác nhau hoặc độ phức tạp của bài toán, thời gian xử lý của mỗi bài toán là khác nhau. Các worker hoàn thành và ghi file ra thư mục `cache/build/` theo thứ tự ngẫu nhiên dựa trên thời điểm hoàn thành (Completion Order).
- Script gộp file `tools/combine_latex.py` trước đây chỉ đọc các file trong thư mục `cache/build/` và sắp xếp theo tên file (alphabetical) hoặc thời gian ghi file (timestamp), dẫn đến thứ tự hiển thị bị đảo lộn, không khớp với thứ tự gửi URL ban đầu (Input Order).

### Cách sửa vĩnh viễn (Permanent Remedy)
1. **Thiết lập Order Index ngay từ đầu:**
   Ngay khi URL được đưa vào queue qua `tools/crawler_manager.py`, gán cứng một trường `order_index` tăng dần (e.g. A -> 0, B -> 1, C -> 2, D -> 3).
2. **Lan truyền Order Index xuyên suốt:**
   Trường `order_index` này phải được lưu trong:
   - Metadata của queue (`cache/queue/index.json`)
   - Cache của crawler (`cache/problemset/{pid}.json`)
   - File JSON đã trích xuất (`cache/normalized/{pid}.json`)
   - Kết quả dịch và cuối cùng là ghi dưới dạng comment trong file LaTeX: `% order_index: <N>` ở đầu file `.tex` trong `cache/build/`.
3. **Merge dựa trên Order Index:**
   Cập nhật `tools/combine_latex.py` để quét comment `% order_index: (\d+)` trong mỗi file `.tex` thuộc `cache/build/`. Thực hiện sắp xếp mảng file theo chỉ số này trước khi tiến hành merge vào `outputs/output.tex`.
4. **Kiểm tra tự động (Validator):**
   Sử dụng script `tools/validate_order.py` để so sánh thứ tự URL trong queue với thứ tự xuất hiện của các bài toán trong file `.tex` đầu ra để phát hiện lỗi lệch thứ tự ngay khi build.

## 2. Root Pollution Bug
- **Bug**: Agent thường tuỳ tiện tạo file nháp như `a.txt`, `test.html`, `draft.md` hoặc sinh log `compile.log` ngay tại thư mục root.
- **Root Cause**: Thiếu ranh giới nghiêm ngặt về khu vực làm việc (Workspace boundaries).
- **Fix**: Áp dụng luật `ROOT = READ ONLY` (trừ một số file chuẩn). Mọi hoạt động sinh runtime artifact PHẢI diễn ra trong `cache/`, `reports/`, hoặc `outputs/`. Đã thực thi qua `tools/repository_guard.py`.

## 3. Token Waste Bug (HTML Bloat)
- **Bug**: Việc chuyển toàn bộ Raw HTML (lên tới 200KB+) cho LLM xử lý gây tốn kém token khổng lồ và tăng tỷ lệ hallucination do dính code CSS/JS rác.
- **Fix**: Pipeline BẮT BUỘC phải đi qua bước Normalization (dùng BeautifulSoup tách độc lập `.problem-statement`). LLM chỉ được phép đọc `cache/normalized/` (kích thước ~1-3KB, giảm ~95-98% token lãng phí).

## 4. PDF Extraction Timeout / Filename Bug
- **Bug**: Cố tải file PDF nhưng lưu cache bằng đường dẫn URL chứa ký tự đặc biệt, gây `OSError: [Errno 22] Invalid argument`.
- **Fix**: Logic bóc tách `get_problem_id` phải cẩn thận với URL không có query parameter, cần sanitize kỹ tên file trước khi tạo đường dẫn cache.

## 5. TOC (Mục lục) Empty Bug
- **Bug**: Cấu trúc `main.toc` hoàn toàn rỗng.
- **Fix**: `\problem` macro BẮT BUỘC phải chứa lệnh `\addcontentsline{toc}{section}{#1}` bên trong file LaTeX Template gốc (không được bypass template).

