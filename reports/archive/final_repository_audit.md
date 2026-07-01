# FINAL REPOSITORY AUDIT REPORT

## 1. Repository Walkthrough
- **Dead files:** `tools/test_playwright.py` (Script thử nghiệm tạm thời).
- **Unused files:** Không phát hiện file thừa đáng kể, ngoại trừ `outputs/.keep` không thực sự cần thiết nếu đã quản lý vòng đời đúng cách.
- **Duplicated logic:** Không có trùng lặp lớn, nhưng `combine_latex.py` đang nằm ở thư mục gốc (root) thay vì `tools/`, vi phạm quy hoạch Repository Policy (điều 1).
- **Temporary artifacts:** Phát hiện `compile_error.log` vứt ngổn ngang ở thư mục gốc sau khi chạy compile. Mặc dù bị ignore trong `.gitignore`, nhưng điều này vi phạm luật Root Pollution.
- **Legacy code:** Không phát hiện mã nguồn quá cũ.

## 2. Skill Consistency Audit (Skill Drift)
Các Skill đang chạy khá ổn định theo quy định mới, nhưng có hiện tượng Skill Drift nhẹ:
- **cp-latex:** Khẳng định "Compiler mặc định là latexmk -pdf", nhưng thực tế pipeline trong `compile_latex.py` đang sử dụng `pdflatex` chay với cờ `-interaction=nonstopmode`. 
- **cp-pipeline:** Khẳng định output sinh ra "Mã nguồn file tex tại outputs/output.tex", nhưng thực tế subagent sinh các file tex vào `cache/build/` trước khi `combine_latex.py` gộp lại.

## 3. Source of Truth Audit
- **VERDICT:** PASS.
- Chỉ tồn tại duy nhất một file `.agents/skills/cp-latex/template.tex`. Không có bất kỳ phiên bản sao lưu, giả mạo hay phân mảnh nào của template.

## 4. Output Contract Audit
- **VERDICT:** MINOR ISSUES.
- Thư mục `outputs/` ngoài `output.tex` và `output.pdf` còn tồn tại các file phụ trợ sinh ra bởi pdflatex (`output.aux`, `output.log`, `output.out`, `output.toc`). Dù không vi phạm nghiêm trọng (không rớt lại `problem_xxx.json` hay `p1.tex`), việc không dọn dẹp các artifact này làm output thiếu sạch sẽ tuyệt đối.

## 5. Cache Policy Audit
- **VERDICT:** PASS.
- Phân tách `cache/problemset` (crawled data), `cache/debug` (lỗi HTML), `cache/build` (intermediate tex), `cache/clean` (parsed/vi JSON) hoạt động chính xác và rất hiệu quả. Đề xuất: Cần định kỳ xóa `cache/debug` nếu dung lượng phình to.

## 6. Archive Audit
- **VERDICT:** PASS.
- Có lưu đủ lịch sử theo ngày (`archive/2026-06-04/`).
- File được đánh số thứ tự tuần tự (`output_001.pdf`, `output_002.pdf`) nên không bị ghi đè hay trùng.
- `index.json` đồng bộ và được code (trong `compile_latex.py` hàm `archive_files`) chủ động cập nhật dữ liệu metadata.

## 7. Compile Pipeline Audit
- **VERDICT:** PASS.
- Đã xác minh `tools/compile_latex.py` gọi `pdflatex` 2 pass liên tiếp.
- Check return code (`if res.returncode == 0`) được thực thi nghiêm ngặt.
- Có lệnh `os.remove(pdf_path)` xóa file PDF cũ trước khi compile, chấm dứt hoàn toàn rủi ro Fake Success.

## 8. Crawler Audit
- **VERDICT:** PASS.
- Chuỗi fallback (Brave -> CloakBrowser -> Playwright Stealth -> Crawl4AI) được phân tầng qua if-not logic rõ ràng.
- Vòng lặp `for attempt in range(retries)` hoạt động.
- Regex detect Cloudflare đã có bước xác nhận `.problem-statement` tồn tại hay chưa, chống False Positive hiệu quả.
- Debug snapshot ghi đúng vào `cache/debug`.

## 9. GitHub Readiness
- **VERDICT:** FAIL (Minor).
- File `.gitignore` đã chặn đúng các runtime artifacts (`.aux`, `.log`, `.toc`, `cache/*`, `outputs/*`).
- TUY NHIÊN, script `combine_latex.py` nằm ở root chưa được đưa vào thư mục `tools/` sẽ dễ gây lộn xộn. Script rác `test_playwright.py` cũng vô tình được commit.

## 10. Dependency Audit
- **VERDICT:** PASS.
- Mọi dependency (`playwright`, `requests`, `crawl4ai`, `cloakbrowser`) được liệt kê trong `requirements.txt` và được hướng dẫn sử dụng trong `README.md`.

## 11. Security Audit
- **VERDICT:** CRITICAL FAIL.
- **Tồn tại Hardcoded Profile/Path trong `tools/crawl_problem.py`:**
  - `BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"`
  - `USER_DATA = r"C:\Users\toanpq\AppData\Local\BraveSoftware\Brave-Browser\User Data"`
- Việc hardcode user `toanpq` khiến mã nguồn này chỉ chạy được trên máy cá nhân của tác giả, hoàn toàn mất tính khả chuyển (portability) và sẵn sàng sản xuất (production readiness). Vi phạm nghiêm trọng tiêu chuẩn bảo mật và OSS.

---

## FINAL SCORE

- **Kiến trúc:** 85/100 (Cấu trúc Chain-of-Skills xuất sắc, trừ điểm vị trí file `combine_latex.py`).
- **Maintainability:** 80/100 (Guardrails tốt nhưng vẫn để xảy ra skill drift nhẹ).
- **Reliability:** 95/100 (Compiler/Crawler bắt lỗi quá tốt).
- **Repository Hygiene:** 75/100 (Vẫn còn rác `.log` ở root, rác `.aux` ở outputs).
- **Production Readiness:** 0/100 (Bị triệt tiêu hoàn toàn bởi lỗi hardcoded User Path).

### Tổng điểm (Trung bình): 67 / 100

## VERDICT
**NEEDS WORK**

### Recommendations:
1. **Critical:** Thay thế biến `USER_DATA` và `BRAVE_PATH` trong crawler bằng tham số môi trường (`.env`) hoặc dùng `os.path.expanduser("~")`.
2. **Major:** Di chuyển `combine_latex.py` vào `tools/` và dọn `test_playwright.py`.
3. **Minor:** Xóa `compile_error.log` ở root ngay khi xử lý xong hoặc đưa nó vào `reports/`.
4. **Minor:** Thêm lệnh tự động clean `.aux`, `.log`, `.out` sau khi LaTeX compile thành công.
