---
name: cp-pipeline
description: Skill điều phối toàn diện Hệ thống Dịch thuật và Tạo tài liệu Competitive Programming (End-to-End Orchestrator). Tự động kích hoạt khi người dùng cung cấp URL bài toán CP để dịch thuật và xuất file PDF.
---

# CP Pipeline Orchestrator

## Tổng quan

`cp-pipeline` là Skill cốt lõi đóng vai trò "Nhạc trưởng" (Orchestrator) điều phối toàn bộ Hệ thống Dịch thuật Competitive Programming. Thay vì tự mình thực hiện các tác vụ phân tích, dịch thuật hay xử lý file, Skill này tự động hóa quy trình gọi tuần tự các bộ kỹ năng chuyên biệt khác, giám sát luồng dữ liệu đầu vào/đầu ra, và xử lý rủi ro xuyên suốt chu trình. Mục đích cao nhất là chuyển đổi tự động một URL bài toán (từ các nguồn như Codeforces, CSES, USACO...) thành một tài liệu PDF tiếng Việt chuẩn mực ICPC/HSG.

## Kiến trúc

**Crawler** → **Parser** → **Translator** → **LaTeX** → **PDF Compiler**

## PDF Handling (LLM-First)
Hệ thống nay hỗ trợ đọc hiểu đề bài dạng PDF (IOI, APIO, CEOI...). Toàn bộ quy trình diễn ra theo chuẩn LLM-First:
1. **Content Detection**: Crawler tự nhận diện URL PDF, tải về `cache/pdf/`.
2. **Image Fallback**: PDF được convert sang ảnh (`cache/pdf_images/`) làm fallback nếu font lỗi.
3. **LLM Parsing**: Nghiêm cấm Python parse/OCR. LLM trực tiếp sử dụng tool `view_file` để nạp PDF/Ảnh và suy luận thành JSON.

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

## Quy trình Tiêu Chuẩn

Khi người dùng thực thi lệnh:
`/cp-pipeline <url>`

Agent sẽ tự động chạy không ngừng nghỉ theo 5 giai đoạn sau:

### STEP 1: Enqueue URLs
*   **Thực thi:** Gọi lệnh enqueue vào hàng đợi (vd: `python tools/crawler_manager.py enqueue <url>`).
*   **Mục tiêu:** Ghi nhận URL cần xử lý vào `cache/queue/index.json`.

### STEP 2: Crawler Manager
*   **Thực thi:** Gọi `python tools/crawler_manager.py process`.
*   **Mục tiêu:** Crawl tuần tự các bài trong queue, tuân thủ nghiêm ngặt **Single Browser Policy** (Chỉ mở 1 phiên làm việc để không dính lỗi Profile Lock).
*   **Expected Output:** Lưu file thô vào `cache/problemset/<id>.json`.

### STEP 3: Verify Cache
*   **Thực thi:** Pipeline đọc queue state để xác nhận job `done` hay `failed`.
*   **Mục tiêu:** Quyết định xem có nên spawn subagents cho các bước tiếp theo hay không. Nếu `failed` thì bỏ qua bài đó, không đập sập toàn pipeline.

### STEP 4: Spawn Parse Agents
*   **Thực thi:** Gọi `cp-parser` trên các file JSON hợp lệ trong `cache/problemset/`.
*   **Expected Output:** `cache/clean/<id>.json` (hoặc `problem_normalized.json`).

### STEP 5: Spawn Translate Agents
*   **Thực thi:** Khởi chạy `cp-translator`.
*   **Expected Output:** Dữ liệu ngôn ngữ đích.

### STEP 6: Spawn LaTeX Agents
*   **Thực thi:** Khởi chạy `cp-latex`.
*   **Expected Output:** Mã nguồn file tex từng bài tại `cache/build/<problem_id>.tex`.

### STEP 7: Combine
*   **Thực thi:** Chạy `python tools/combine_latex.py`.
*   **Expected Output:** Gộp tất cả thành file tổng `outputs/output.tex`.

### STEP 8: Compile
*   **Thực thi:** Gọi `python tools/compile_latex.py outputs/output.tex`.
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
*   **User Order > Completion Order:** Bắt buộc Orchestrator phải đảm bảo các file JSON đầu ra của các subagent (Parser, Translator) đều kế thừa và bảo toàn trường `order_index`. File PDF cuối cùng phải phản ánh đúng 100% thứ tự URL đầu vào của người dùng, không phụ thuộc vào thứ tự hoàn thành của các worker song song.

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

## Bài học kinh nghiệm
1. **Gemini báo PASS dù compile fail**: LLM có xu hướng tự tin thái quá, báo cáo thành công chỉ vì thấy file có mặt trên đĩa (hoặc do file PDF cũ chưa bị xoá).
2. **Subagent hallucinate macro**: Không thể tin tưởng hoàn toàn vào LLM trong việc sinh ra LaTeX macro chuẩn. Chúng thường tự bịa thêm các lệnh lạ.
3. **Queue Backup**: Hàng đợi (`cache/queue/index.json`) có thể bị kẹt jobs cũ sau crash/restart. Nếu crawler mở URL lạ, kiểm tra ngay queue. Dùng `python tools/crawler_manager.py flush` để dọn dẹp.

## Luật chống đứt gãy
- **Rule 1**: BẮT BUỘC CHÉO KIỂM TRA (cross-verify). Không bao giờ tin tưởng mù quáng vào kết quả sinh file. Phải kiểm tra Return Code và Log file.
- **Rule 2**: Phải tự động xóa artifact cũ trước khi khởi động quy trình compile (clean state).
- **Rule 3**: Cấm việc subagent tự sáng tạo macro. Pipeline ở bước LaTeX phải có cơ chế validate/sanitize output LaTeX.
- **Rule 4**: CẤM SUBAGENT CRAWL ĐỘC LẬP. Child agents are forbidden from calling `crawl_problem.py`. Mọi quá trình crawl phải thông qua `crawler_manager.py` theo kiến trúc Queue.

## Repository Hygiene Rules (ENFORCED)
- **Root Directory**: Chỉ được phép: `README.md`, `LICENSE`, `requirements.txt`, `.gitignore`, `build.py`. Tuyệt đối CẤM tạo file `.html`, `.txt`, `.json`, `.md`, `.log`, `.aux`, `.py` tại root.
- **cache/problemset/**: Chỉ chứa `.json` files (raw cache). Không được tạo `.html`, `.txt`, `.md` tại đây.
- **cache/normalized/**: Chứa `.json` normalized (html fragment extracted). Không được chứa HTML files.
- **cache/build/**: Chỉ chứa `.tex` và `.pdf` cho từng bài. KHÔNG được chứa `.aux`, `.log`, `.toc`, `.out`, `.py`, `.txt` rác.
- **outputs/**: Chỉ được chứa `output.tex` và `output.pdf`. `.aux`, `.log`, `.toc`, `.out` phải được xóa tự động sau compile.
- **archive/**: Chỉ lưu `.pdf` và `.tex`. Không lưu `.aux`, `.log`, `.toc`, `.out`, `.synctex.gz`.

## Token Optimization Rules (ENFORCED)
- **Parser PHẢI đọc `cache/normalized/<id>.json`** (html fragment ~5-50KB), KHÔNG được đọc `cache/problemset/<id>.json` (raw HTML 100-270KB).
- Trước khi spawn Parser agent: bắt buộc chạy `python tools/extract_html.py <id>` để extract fragment vào `cache/normalized/`.
- Nếu `cache/normalized/<id>.json` đã tồn tại: skip extraction (lazy).
- **NGHIÊM CẤM** truyền raw HTML 100KB+ cho LLM. Đây là lãng phí token 97%.

## Cache Lifecycle Rules
```
URL → cache/problemset/<id>.json  (raw, full HTML, 100-270KB)
      ↓ html_extractor.py
      cache/normalized/<id>.json  (clean fragment, 5-50KB)
      ↓ LLM Parser
      cache/clean/<id>.json       (structured JSON)
      ↓ LLM Translator
      cache/build/<id>.tex        (LaTeX fragment)
      ↓ combine + compile
      outputs/output.tex + output.pdf
      ↓ archive
      archive/<date>/output_NNN.pdf
```
Mỗi bước chỉ đọc stage trước của nó. Không bao giờ skip stage.

## Lỗi đã biết
- Pipeline báo SUCCESS nhưng không có PDF (Fake Success).
- Root directory bị ô nhiễm (Root Pollution) do quá trình debug.
- Lỗi LaTeX không được catch và report chính xác cho user.
- Parser đọc raw HTML (100KB+) thay vì normalized fragment → token waste 97%.
