---
name: cp-pipeline
description: Skill điều phối toàn diện Hệ thống Dịch thuật và Tạo tài liệu Competitive Programming (End-to-End Orchestrator). Tự động kích hoạt khi người dùng cung cấp URL bài toán CP để dịch thuật và xuất file PDF.
---

# CP Pipeline Orchestrator

## Tổng quan

`cp-pipeline` là Skill cốt lõi đóng vai trò "Nhạc trưởng" (Orchestrator) điều phối toàn bộ Hệ thống Dịch thuật Competitive Programming. Thay vì tự mình thực hiện các tác vụ phân tích, dịch thuật hay xử lý file, Skill này tự động hóa quy trình gọi tuần tự các bộ kỹ năng chuyên biệt khác, giám sát luồng dữ liệu đầu vào/đầu ra, và xử lý rủi ro xuyên suốt chu trình. Mục đích cao nhất là chuyển đổi tự động một URL bài toán (từ các nguồn như Codeforces, CSES, USACO...) thành một tài liệu PDF tiếng Việt chuẩn mực ICPC/HSG.

## Kiến trúc

Pipeline hoạt động theo mô hình dây chuyền (Chain-of-Skills) tuyến tính:
**Crawler** → **Parser** → **Translator** → **LaTeX** → **PDF Compiler**

## Vị trí và Vai trò của các Skill

*   **.agents/skills/cp-crawler/SKILL.md**
    *Vai trò:* Thu thập HTML/Markdown nguyên bản từ URL. Hỗ trợ vượt tường lửa Cloudflare/Anti-bot qua các fallback API mạnh mẽ (CloakBrowser, Crawl4AI, Playwright).
*   **.agents/skills/cp-parser/SKILL.md**
    *Vai trò:* Đọc hiểu tài liệu thô, nhận diện ngữ nghĩa và trích xuất thành cấu trúc dữ liệu JSON tiêu chuẩn (Title, Statement, Input, Output, Constraints, Samples).
*   **.agents/skills/cp-translator/SKILL.md**
    *Vai trò:* Dịch thuật nội dung sang tiếng Việt chuyên ngành lập trình thi đấu (CP) và tự động suy luận, sinh ra giải thích (explanation) chi tiết cho từng Sample test.
*   **.agents/skills/cp-latex/SKILL.md**
    *Vai trò:* Định dạng và render dữ liệu đã dịch vào chuẩn Golden Template Tiếng Việt (`template.tex`).

---

## Workflow Tiêu Chuẩn

Khi người dùng thực thi lệnh:
`/cp-pipeline <url>`

Agent sẽ tự động chạy không ngừng nghỉ theo 5 giai đoạn sau:

### Phase 1: Crawl
*   **Thực thi:** Khởi chạy `cp-crawler` (gọi script `tools/crawl_problem.py`).
*   **Mục tiêu:** Tải nội dung DOM/Markdown. Hệ thống sử dụng cơ chế Fallback chống Bot đa tầng (Brave Persistent Profile -> CloakBrowser -> Playwright Stealth -> Crawl4AI). Có tích hợp quét `cdn-cgi/challenge-platform` để phát hiện và Retry khi dính Cloudflare.
*   **Expected Output:** Sinh ra file `cache/problem_raw.json` (hoặc báo lỗi nếu mọi nỗ lực đều bị chặn).

### Phase 2: Parse
*   **Thực thi:** Khởi chạy `cp-parser` trên dữ liệu raw.
*   **Mục tiêu:** Chuẩn hóa cấu trúc (Normalize structure) và validate các trường bắt buộc.
*   **Expected Output:** Dữ liệu chuẩn hóa `cache/problem_normalized.json`.

### Phase 3: Translation
*   **Thực thi:** Khởi chạy `cp-translator`.
*   **Mục tiêu:** Dịch thuật sang tiếng Việt và sinh Explanation.
*   **Expected Output:** Dữ liệu ngôn ngữ đích `cache/problem_vi.json`.

### Phase 4: LaTeX Generation
*   **Thực thi:** Khởi chạy `cp-latex`.
*   **Mục tiêu:** Gắn dữ liệu vào `template.tex`.
*   **Expected Output:** Mã nguồn file tex tại `outputs/output.tex`.

### Phase 5: PDF Compilation
*   **Thực thi:** Gọi tool `compile_latex.py` (hoặc trực tiếp `pdflatex -interaction=nonstopmode`).
*   **Mục tiêu:** Biên dịch ra file PDF hoàn thiện.
*   **Expected Output:** File tài liệu cuối cùng tại `outputs/output.pdf`.

---

## Quản Lý Lỗi (Failure Handling)

Hệ thống được thiết kế để tự phục hồi hoặc báo cáo chính xác vị trí lỗi:
*   **Crawler Failure:** Tự động retry với browser/backend fallback kế tiếp (Crawl4AI -> CloakBrowser -> Playwright -> Requests).
*   **Parser Failure:** Nếu không tìm thấy Input/Output, dừng pipeline và báo cáo cấu trúc không hợp lệ (Report invalid structure).
*   **Translation Failure:** Nếu gặp thuật ngữ quá dị biệt hoặc mất context, bảo toàn nguyên bản tiếng Anh (Preserve original statement) và cảnh báo người dùng.
*   **LaTeX Failure:** Bắt toàn bộ log compiler từ `pdflatex`. Báo cáo nguyên nhân gốc rễ (Root cause) do lỗi ngoặc, kí tự lạ, hoặc thiếu font.

---

## Quy Tắc Chất Lượng (Quality Rules)

Quá trình Translation bắt buộc phải tuân thủ nghiêm ngặt các quy tắc sau:
*   **Preserve mathematics:** Giữ nguyên vẹn 100% công thức Toán Học, kí hiệu biến.
*   **Preserve formulas:** Không được tự ý thay đổi phép tính hoặc kí hiệu tiệm cận (Big-O).
*   **Preserve examples:** Không chỉnh sửa nội dung test samples.
*   **Preserve constraints:** Giữ tuyệt đối chính xác giới hạn biến, time limit, memory limit.
*   **Preserve sample IO:** Định dạng bảng mẫu Input/Output phải khớp 100% đề gốc.
*   **Never hallucinate content:** Tuyệt đối không tự bịa thông tin đề bài.
*   **Never modify problem meaning:** Không làm thay đổi ý nghĩa thuật toán cốt lõi.

---

## Chế Độ Đa Liên Kết (Multi-URL Behavior)

Khi người dùng truyền vào nhiều bài toán cùng lúc:
`/cp-pipeline url1 url2 url3`
*   **Tiến trình:** Xử lý tuần tự (Process sequentially) từng bài.
*   **Kết xuất:** Các bài được gộp chung thành từng Section trong cùng một file `outputs/output.tex` và `outputs/output.pdf`. Tuyệt đối nhất quán về format và từ vựng.

---

## Quy Hoạch Thư Mục (Directory Policy)

*   **`cache/`**: Chứa các file trung gian như `problem_raw.json`, `problem_normalized.json`, `problem_vi.json`. Các file này là tạm thời để Audit và Debug khi hệ thống sụp đổ.
*   **`outputs/`**: Chứa các file kết xuất cuối cùng mà người dùng tương tác (`output.tex`, `output.pdf`).
*   **`reports/`**: Nơi Agent lưu trữ các file báo cáo phân tích lỗi, audit kiến trúc, hoặc `latest_run.md` sau khi kết thúc pipeline.

---

## Tiêu Chí Hoàn Thành (Completion Criteria)

*   Pipeline chỉ được xác nhận **THÀNH CÔNG** khi và chỉ khi file **`outputs/output.pdf` tồn tại** và biên dịch không lỗi.
*   **BẮT BUỘC TUÂN THỦ 4 LUẬT SAU TRƯỚC KHI BÁO PASS:**
    1. Không được kết luận PASS nếu chưa đọc compile log (compile_error.log).
    2. Không được tự khẳng định PDF thành công chỉ vì tool không văng lỗi.
    3. Phải xác minh file PDF tồn tại thực tế trên ổ cứng.
    4. Phải xác minh lệnh compile (pdflatex/latexmk) có `return code = 0`.
*   Nếu PDF không được sinh ra hoặc compile log chứa `LaTeX Error`/`Fatal error`, quy trình bị tính là THẤT BẠI. Mọi bước ở giữa không được tính là thành công nếu chưa có PDF.

---

## Lessons Learned
1. **Gemini báo PASS dù compile fail**: LLM có xu hướng tự tin thái quá, báo cáo thành công chỉ vì thấy file có mặt trên đĩa (hoặc do file PDF cũ chưa bị xoá).
2. **Subagent hallucinate macro**: Không thể tin tưởng hoàn toàn vào LLM trong việc sinh ra LaTeX macro chuẩn. Chúng thường tự bịa thêm các lệnh lạ.

## Anti Regression Rules
- **Rule 1**: BẮT BUỘC CHÉO KIỂM TRA (cross-verify). Không bao giờ tin tưởng mù quáng vào kết quả sinh file. Phải kiểm tra Return Code và Log file.
- **Rule 2**: Phải tự động xóa artifact cũ trước khi khởi động quy trình compile (clean state).
- **Rule 3**: Cấm việc subagent tự sáng tạo macro. Pipeline ở bước LaTeX phải có cơ chế validate/sanitize output LaTeX.

## Known Failure Modes
- Pipeline báo SUCCESS nhưng không có PDF (Fake Success).
- Root directory bị ô nhiễm (Root Pollution) do quá trình debug.
- Lỗi LaTeX không được catch và report chính xác cho user.
