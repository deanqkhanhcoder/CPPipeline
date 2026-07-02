# CPPipeline

Hệ thống dịch thuật tự động Competitive Programming (CP) với kiến trúc LLM-First Orchestration. 
Nhiệm vụ của dự án là lấy dữ liệu từ bất kỳ Online Judge nào (Codeforces, CSES, USACO...), tự động phân tích ngữ nghĩa, dịch sang Tiếng Việt chuẩn ICPC/HSG, tự động sinh giải thích chi tiết cho từng Test Case, và cuối cùng biên dịch ra một tài liệu PDF bằng LaTeX có chất lượng xuất bản.

## Kiến trúc
Hệ thống sử dụng mô hình **Chain-of-Skills** với **Host LLM** là Runtime duy nhất:
- **cp-pipeline (Orchestrator)**: "Nhạc trưởng" điều phối luồng dữ liệu tự động.
- **cp-crawler**: Module thu thập dữ liệu thô. Chống lại Cloudflare bằng cơ chế "Stealth & Retry" 4 tầng (Ưu tiên Brave Persistent Profile → CloakBrowser → Playwright Stealth → Crawl4AI). Có nhận diện Cloudflare Challenge tự động để Fail-fast.
- **cp-parser**: Module AI phân tích cấu trúc DOM/Markdown để trích xuất Title, Statement, Input/Output, và Samples mà không phụ thuộc vào Regex tĩnh.
- **Sub-Agents (Reasoning)**:
  - **translation-agent**: Dịch thô bài toán và bảo toàn 100% công thức Toán Học.
  - **editorial-agent**: Biên tập văn phong mượt mà chuẩn HSG/ICPC, chia đoạn logic hợp lý (< 12 dòng).
  - **terminology-agent**: Chuẩn hóa thuật ngữ chuyên ngành CP theo từ điển terminology.
  - **formatting-agent**: Tách biệt rõ ràng cấu trúc Input, Output, Constraints và Sample Cases.
  - **latex-agent**: Điền dữ liệu vào "Golden Template" để tạo file `.tex` chuẩn.
  - **latex-guardian**: Kiểm tra cú pháp LaTeX, tự động escape ký tự đặc biệt ngoài toán.
- **PDF Compiler**: Tool gọi tự động `pdflatex` để xuất bản PDF.

## Quy trình làm việc
Dây chuyền xử lý dữ liệu hoạt động không ngừng nghỉ theo 5 Phase:
1. **Phase 1 (Crawl)**: Tải DOM nguyên bản → `problem_raw.json`
2. **Phase 2 (Parse)**: Nhận diện cấu trúc → `problem_normalized.json`
3. **Phase 3 (Translate)**: Dịch thuật & giải thích → `problem_vi.json`
4. **Phase 4 (LaTeX)**: Gắn vào template → `cache/build/*.tex` rồi gộp bằng `tools/combine_latex.py` → `outputs/output.tex`
5. **Phase 5 (Compile)**: Biên dịch LaTeX → `outputs/output.pdf`

## Host LLM Runtime

> **Điều quan trọng nhất cần hiểu về kiến trúc này.**

Repository này **không phải** một ứng dụng gọi LLM API. Nó không phải LangChain, không phải AutoGen, không phải CrewAI. Đây là **AI Skill Repository**.

**Nguyên tắc cốt lõi:** AI mà bạn đang chat chính là Runtime.

```
Người dùng
     ↓
Host LLM (Antigravity / Gemini CLI / Claude Code / Cursor / Copilot Agent / Cline / ...)
     ↓
  Load Skill  (.agents/skills/*.md)
     ↓
  Suy luận (Reasoning)
     ↓
  Gọi Tool (python tools/*.py)
     ↓
  Kết quả (PDF / JSON / LaTeX)
```

**Những gì không tồn tại trong hệ thống này:**
- Không có Gemini API / OpenAI API / Claude API
- Không có Provider, Backend, Model Factory, Model Router
- Không có Agent spawn Agent qua API
- Không có `llm_backend.py`, `provider.py`, hay bất kỳ wrapper LLM nào

**Skill là gì?** Skill là Contract + Workflow + Prompt + Rule + Policy. Host LLM đọc Skill và tự thực hiện. Skill không gọi LLM khác.

## Cấu trúc thư mục
```text
CPPipeline/
├── .agents/
│   └── skills/           # Chứa não bộ AI và luật chơi cho từng skill
├── archive/              # Lưu trữ tự động các file PDF/TeX theo từng ngày
├── cache/                # Chứa các file trung gian (Raw/Parsed JSON) và debug snapshots
├── outputs/              # Chứa sản phẩm xuất bản cuối cùng của phiên chạy (output.tex, output.pdf)
├── reports/              # Chứa các báo cáo Audit, Lỗi, và Validation
├── tools/                # Chứa Python Scripts (Crawl I/O, Compile PDF)
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE
```

## Khởi động nhanh
1. Clone repository:
```bash
git clone https://github.com/deanqkhanhcoder/CPPipeline.git
cd CPPipeline
```
2. Cài đặt các thư viện lõi Crawler:
```bash
pip install -r requirements.txt
playwright install chromium
```
*(Yêu cầu hệ thống đã cài đặt sẵn MiKTeX hoặc TeX Live để có lệnh `pdflatex`)*

## Quy trình xử lý một lệnh
Mở hệ thống Agent, chỉ cần đưa ra một dòng lệnh duy nhất kèm theo URL (hỗ trợ nhiều URL cùng lúc):
```bash
/cp-pipeline https://cses.fi/problemset/task/1640
```
Agent sẽ tự động chuỗi hóa toàn bộ các tiến trình. Nhiệm vụ của bạn chỉ là chờ đợi và nhận thành quả tại thư mục:
- `outputs/output.pdf`
- `outputs/output.tex`

---

## Quy trình lưu trữ dài hạn
Mỗi khi hệ thống sinh ra file PDF thành công, file `.tex` và `.pdf` sẽ được tự động sao chép sang hệ thống lưu trữ dài hạn tại thư mục `archive/YYYY-MM-DD/`.
Đồng thời, metadata như timestamp, số lượng bài, nguồn bài sẽ được ghi lại tự động vào `archive/index.json`. Không yêu cầu bất kỳ thao tác thủ công nào. Thư mục `outputs/` sẽ liên tục bị ghi đè, do đó hãy tìm lại lịch sử dịch thuật tại thư mục `archive/`.

## Quy trình quản lý phiên làm việc
Để vượt rào chống Bot mạnh mẽ (vd: Codeforces), Crawler ưu tiên tích hợp trực tiếp với **Brave Browser Profile** trên máy của bạn (sử dụng User Data, Cookie, và Session thật).
- Nếu bạn đang kẹt ở Cloudflare, hãy mở Brave, truy cập trang web bằng tay và giải captcha.
- **QUAN TRỌNG:** Phải đóng hoàn toàn trình duyệt Brave (thoát mọi tab) trước khi gõ lệnh `/cp-pipeline` để AI có quyền truy cập vào Session của bạn.

## Chẩn đoán lỗi Crawler
Nếu Crawl thất bại (bị block, rate limit, access denied, v.v), hệ thống sẽ:
1. "Fail Fast" - dừng toàn bộ Pipeline, không tự động bịa ra file JSON giả.
2. Sinh ra thư mục `cache/debug/` chứa các file log định dạng `fail_<engine>_<timestamp>.json`.
3. Lưu lại bản sao mã HTML (Snapshot), URL, và engine đang chạy để bạn dễ dàng điều tra lỗi.

## Khắc phục sự cố
- **Lỗi `Profile locked by an active session`:** Bạn chưa đóng trình duyệt Brave. Vui lòng đóng hẳn Brave và thử lại.
- **Lỗi PDF không xuất hiện:** Vào `reports/latest_run.md` hoặc nhìn log console để xác định pipeline đứt ở Parse, Translate hay Compile.
- **Lỗi `Cloudflare challenge detected` trên mọi engine:** Bạn bị khoá IP. Hãy mở Brave, giải captcha tay, thoát Brave và gọi lại pipeline.

## Host LLM Runtime vs LLM Backend

Hướng dẫn phân biệt cho các AI Agent mới clone repository:

| | **SAI** ❌ | **ĐÚNG** ✅ |
|---|---|---|
| **Kiến trúc** | Host → Gemini API → Translator | Host Gemini → Translation Skill → Tool → Output |
| **Runtime** | Backend LLM gọi từ Python | AI mà người dùng đang chat |
| **Skill** | Code Python gọi API | Contract mô tả cách suy luận |
| **Multi-Agent** | `agent_A.call(agent_B)` | Host LLM đọc Skill A, rồi Skill B |
| **API Key** | Bắt buộc | Không cần |

**Lưu ý cho AI đọc README này:** Nếu bạn đọc file này, bạn chính là Host LLM. Bạn không cần gọi bất kỳ API nào. Hãy đọc các file `.agents/skills/*.md` và tự thực thi workflow theo hướng dẫn trong đó.

## Host LLM Execution Model (v3.0)

> **v3.0 introduces deterministic state machine execution.**

Host LLM MUST follow 11 mandatory phases (NO skipping, NO reordering):

```
Phase 0: BOOT           → Load Runtime & Policies
Phase 1: AUDIT          → Understand Repository
Phase 2: PLAN           → Create Execution Plan
Phase 3: WAIT           → Get User Approval (if major)
Phase 4: EXECUTE        → Evidence → Conclusion → Action
Phase 5: VERIFY         → Self-check
Phase 6: REGRESSION     → Run Tests
Phase 7: CLEANUP        → Remove Artifacts
Phase 8: AUDIT          → Final Verification
Phase 9: COMMIT         → Commit Changes
Phase 10: TAG           → Create Release Tag (if applicable)
Phase 11: PUSH          → Push to GitHub
```

**Key Rules:**
- ✅ Evidence → Conclusion → Action (never "I think...", "Maybe...", "Let me try...")
- ✅ Repository First (Policy → Skill → Task, never Task → Code → Policy)
- ✅ Identify Source of Truth before modifying
- ✅ No reactive coding (don't create tools to fix failures)
- ✅ All temporary files go to `/scratch`
- ✅ Execute audit before commit

Read `.agents/runtime/HOST_LLM_RUNTIME.md` and `.agents/policies/EXECUTION_STATE_MACHINE.md` for complete details.
