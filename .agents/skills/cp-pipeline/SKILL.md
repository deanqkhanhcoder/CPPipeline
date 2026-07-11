---
name: cp-pipeline
description: Skill điều phối toàn diện Hệ thống Dịch thuật và Tạo tài liệu Competitive Programming (End-to-End Orchestrator). Tự động kích hoạt khi người dùng cung cấp URL bài toán CP để dịch thuật và xuất file PDF.
---

## Declarative Dependencies
- **Runtime**: `.agents/runtime/runtime.md`
- **Policies**: `.agents/policies/repository_policy.md`, `.agents/policies/template_policy.md`, `.agents/policies/error_taxonomy.md`, `.agents/policies/self_improvement_policy.md`
- **Knowledge**: `.agents/knowledge/root_causes.md`, `.agents/knowledge/pipeline_failures.md`
- **Required Skills**: `.agents/skills/cp-crawler/SKILL.md`, `.agents/skills/cp-parser/SKILL.md`, `.agents/skills/translation-agent/SKILL.md`, `.agents/skills/formatting-agent/SKILL.md`, `.agents/skills/latex-agent/SKILL.md`, `.agents/skills/fragment-qa/SKILL.md`, `.agents/skills/latex-guardian/SKILL.md`, `.agents/skills/qa-agent/SKILL.md`
- **Optional Skills**: `.agents/skills/editorial-agent/SKILL.md`, `.agents/skills/terminology-agent/SKILL.md`, `.agents/skills/sample-explainer/SKILL.md`, `.agents/skills/semantic-fidelity-reviewer/SKILL.md`, `.agents/skills/order-guardian/SKILL.md`
- **Optional Knowledge**: `.agents/knowledge/crawler_failures.md`, `.agents/knowledge/latex_failures.md`, `.agents/knowledge/pdf_statement_handling.md`, `.agents/knowledge/repository_failures.md`

# CP Pipeline Orchestrator

## Runtime
Host LLM đang thực thi Skill này. Skill không gọi bất kỳ LLM nào khác. Skill chỉ hướng dẫn Host LLM cách suy luận, điều phối Tool và thực thi Quy tr?nh.

## Runtime Bootstrap (Entry Point)

**Khi Skill này được Host Runtime kích hoạt**:

Việc đầu tiên Host LLM phải làm là:

1. **Load Runtime Framework**
   - Read: `.agents/runtime/runtime.md`
   - Runtime sẽ hướng dẫn các bước tiếp theo

2. **Runtime Dependencies** (Host LLM sẽ resolve):
   - `.agents/runtime/runtime.md` (index and overview)
   - `.agents/runtime/host_llm_contract.md` (runtime principles)
   - `.agents/runtime/execution_state_machine.md` (12-state machine)
   - `.agents/runtime/phase_definition.md` (what each phase does)
   - `.agents/runtime/repository_first.md` (decision priority)
   - `.agents/runtime/decision_policy.md` (evidence-based decisions)
   - `.agents/runtime/rollback_policy.md` (error recovery)
   - `.agents/runtime/verification_policy.md` (output verification)

3. **Runtime Will Guide**:
   - Which policies to load (.agents/policies/)
   - Which knowledge to load on-demand (.agents/knowledge/)
   - Which dependency skills to resolve
   - When to plan execution
   - When to execute phases
   - When to verify output

**This Skill is NOT the Executor.** This Skill is the **Bootstrap Point**. Runtime is the **Execution Engine**.

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
    *Vai trò:* Thu thập HTML/Markdown nguyên bản từ URL. Hỗ trợ vượt tường lửa Cloudflare/Anti-bot qua các cơ chế fallback mạnh mẽ (CloakBrowser, Crawl4AI, Playwright).
*   **.agents/skills/cp-parser/SKILL.md**
    *Vai trò:* Đọc hiểu tài liệu thô, nhận diện ngữ nghĩa và trích xuất thành cấu trúc dữ liệu JSON tiêu chuẩn (Title, Statement, Input, Output, Constraints, Samples).
*   **.agents/skills/translation-agent/SKILL.md**
    *Vai trò:* Dịch thuật nội dung ngữ nghĩa chính xác sang tiếng Việt và bảo toàn công thức toán học.
*   **.agents/skills/editorial-agent/SKILL.md**
    *Vai trò:* Biên tập văn phong tự nhiên chuẩn HSG, tự động chia đoạn hợp lý (< 12 dòng).
*   **.agents/skills/terminology-agent/SKILL.md**
    *Vai trò:* Chuẩn hóa thuật ngữ lập trình thi đấu (CP) theo từ điển `terminology.md`.
*   **.agents/skills/formatting-agent/SKILL.md**
    *Vai trò:* Chuẩn hóa cấu trúc I/O và Sample Cases.
*   **.agents/skills/latex-agent/SKILL.md**
    *Vai trò:* Chuyển đổi cấu trúc JSON sang mã nguồn LaTeX.
*   **.agents/skills/latex-guardian/SKILL.md**
    *Vai trò:* Kiểm soát cú pháp LaTeX thô, escape ký tự đặc biệt, kiểm tra math/list environments.
*   **.agents/skills/order-guardian/SKILL.md**
    *Vai trò:* Đối chiếu thứ tự bài toán từ URL gốc -> Queue -> PDF -> TOC -> Metadata.
*   **.agents/skills/qa-agent/SKILL.md**
    *Vai trò:* Chấm điểm chất lượng toàn diện của tài liệu đầu ra qua hệ thống 5 sao (Aspect Score >= 4.0).

## Unified Bilingual Title Policy

**Format chuẩn duy nhất:** Tên tiếng Việt (Tên tiếng Anh)

Mọi nơi trong pipeline (JSON, LaTeX, PDF, TOC, Bookmark, Header, Footer, Archive, Metadata) đều phải dùng `display_title` với format:

- **Đúng:** "Bắt tay (Handshake)", "A. Dưa hấu (Watermelon)", "E. Ba số (Three Numbers)"
- **Sai:** "Handshake", "Bắt tay", "Handshake (Bắt tay)", "BẮT TAY"

**Source of Truth:** Chỉ tồn tại duy nhất `display_title` được tạo bởi `translation-agent`. Mọi skill downstream không được tự dịch, tự format, hoặc đảo thứ tự.

**Anti-Regression:** Pipeline FAIL nếu phát hiện title không đúng format, hoặc TOC/bookmark/header/footer không dùng `display_title`.

---

## Quy trình Tiêu Chuẩn (Declarative Orchestration)

Khi người dùng thực thi lệnh:
`/cp-pipeline <url>`

Host LLM (Gemini CLI, Antigravity, Claude Code, Cursor...) sẽ trực tiếp làm runtime điều phối theo các bước:

### STEP 1: Enqueue URLs
*   **Thực thi:** Host LLM chạy lệnh `python tools/crawler_manager.py enqueue <url>`.
*   **Mục tiêu:** Thêm URL vào `cache/queue/index.json`.

### STEP 2: Crawler Engine
*   **Thực thi:** Host LLM chạy lệnh `python tools/crawler_manager.py run` (hoặc `process`).
*   **Mục tiêu:** Tải HTML thô về `cache/problemset/<id>.json`.

### STEP 3: Verify Cache & Extract Fragment
*   **Thực thi:** Host LLM chạy `python tools/extract_html.py <id>` để lọc chrome DOM và sinh fragment chính vào `cache/normalized/<id>.json`.

### STEP 4: Parse Content
*   **Thực thi:** Host LLM nạp `.agents/skills/cp-parser/SKILL.md` để tự chuyển đổi fragment thô thành JSON cấu trúc chuẩn.

### STEP 5: Apply Reasoning Skills
*   **Thực thi:** Host LLM lần lượt (hoặc song song bằng subagents) áp dụng các Skill Contracts lên JSON cấu trúc để sinh ra mã nguồn LaTeX:
    1. `translation-agent` (Dịch thô toàn bộ đề bài, giữ nguyên toán học)
    2. `sample-explainer` (Sinh explanation cho mọi sample nếu thiếu)
    3. `editorial-agent` (Biên tập văn phong, chia đoạn logic)
    4. `terminology-agent` (Chuẩn hóa thuật ngữ CP)
    5. `formatting-agent` (Tách biệt I/O format)
    6. `latex-agent` (Chuyển đổi sang mã LaTeX chuẩn template)
    7. `latex-guardian` (Escape ký tự đặc biệt, kiểm tra cú pháp)
    8. `semantic-fidelity-reviewer` (So sánh đề gốc vs bản dịch, FAIL nếu mất thông tin)
*   **Mục tiêu:** Lưu kết quả LaTeX cuối cùng vào `cache/build/<problem_id>.tex` kèm comment `% order_index: <index>`.

### STEP 6: Verify Order
*   **Thực thi:** Host LLM chạy `python tools/validate_order.py`.
*   **Mục tiêu:** Xác minh thứ tự bài viết trong `cache/build/` khớp hoàn toàn với queue.

### STEP 7: Text Normalization
*   **Thực thi:** Host LLM chạy `python tools/text_normalizer.py`.
*   **Mục tiêu:** Định dạng lại khoảng trắng, dấu câu và danh sách LaTeX.

### STEP 8: Fragment Quality Gate (Fragment QA)
*   **Th?c thi:** Host LLM ch?y `python tools/fragment_qa.py`.
*   **M?c ti?u:** Ki?m duy?t ??c l?p t?ng file fragment `.tex` trong `cache/build/`. N?u FAIL, t? ch?i fragment v? bu?c Host LLM t?i t?o t? t?ng g?c (Parser/Formatter/LaTeX). Tuy?t ??i kh?ng combine fragment l?i.

### STEP 9: Combine & Compile
*   **Th?c thi:** Host LLM ch?y `python tools/combine_latex.py` ?? g?p t?i li?u th?nh `outputs/output.tex`, sau ?? ch?y `python tools/compile_latex.py outputs/output.tex` ?? bi?n d?ch ra `outputs/output.pdf`.
*   **M?c ti?u:** B?t bu?c Return Code c?a c? 2 pass compile ph?i b?ng 0 (`rc == 0`). N?u FAIL, x?c ??nh TeX error v? quay v? s?a t?ng LaTeX/Template th??ng ngu?n.

### STEP 10: PDF Quality Gate & Archive (PDF QA)
*   **Th?c thi:** Host LLM ch?y `python tools/pdf_qa.py` ?? ki?m duy?t text c?a file PDF v? compile log. N?u PASS, ch?y `python tools/archive_output.py` ?? l?u tr? sang `archive/` v? ghi nh?n metadata. N?u FAIL, ch?n archive v? kh?i ??ng v?ng l?p Root Cause.

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
*   **BẮT BUỘC TUÂN THỦ 5 LUẬT SAU TRƯỚC KHI BÁO PASS:**
    1. Không được kết luận PASS nếu chưa đọc compile log (compile_error.log).
    2. Không được tự khẳng định PDF thành công chỉ vì tool không văng lỗi.
    3. Phải xác minh file PDF tồn tại thực tế trên ổ cứng.
    4. Phải xác minh lệnh compile (pdflatex/latexmk) có `return code = 0`.
    5. Phải đảm bảo tất cả các file LaTeX trong `cache/build/` đều đã vượt qua bước kiểm duyệt chất lượng `audit_quality.py` mà không bị văng lỗi hoặc cảnh báo vi phạm.
*   Nếu PDF không được sinh ra hoặc compile log chứa `LaTeX Error`/`Fatal error`, quy trình bị tính là THẤT BẠI. Mọi bước ở giữa không được tính là thành công nếu chưa có PDF.

---

## Bài học kinh nghiệm
1. **Host LLM báo PASS dù compile fail**: LLM có xu hướng tự tin thái quá, báo cáo thành công chỉ vì thấy file có mặt trên đĩa (hoặc do file PDF cũ chưa bị xoá).
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

## V3.1 Root-Cause Hardening

If any bug appears:
1. classify it using `.agents/policies/error_taxonomy.md`,
2. fix the producing layer only,
3. regenerate downstream artifacts,
4. verify with the matching gate.

Never patch `outputs/output.tex`, patch `outputs/output.pdf`, create `fix_output*.py`, regex-repair generated artifacts, or move a defect to another layer.