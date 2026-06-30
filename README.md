# CPPipeline

Hệ thống dịch thuật tự động Competitive Programming (CP) với kiến trúc LLM-First Orchestration. 
Nhiệm vụ của dự án là lấy dữ liệu từ bất kỳ Online Judge nào (Codeforces, CSES, USACO...), tự động phân tích ngữ nghĩa, dịch sang Tiếng Việt chuẩn ICPC/HSG, tự động sinh giải thích chi tiết cho từng Test Case, và cuối cùng biên dịch ra một tài liệu PDF bằng LaTeX có chất lượng xuất bản.

## Kiến trúc
Hệ thống sử dụng mô hình **Chain-of-Skills** dựa trên sức mạnh của AI (Gemini Agent):
- **cp-pipeline (Orchestrator)**: "Nhạc trưởng" điều phối luồng dữ liệu tự động.
- **cp-crawler**: Module thu thập dữ liệu thô. Chống lại Cloudflare bằng cơ chế "Stealth & Retry" 4 tầng (Ưu tiên Brave Persistent Profile → CloakBrowser → Playwright Stealth → Crawl4AI). Có nhận diện Cloudflare Challenge tự động để Fail-fast.
- **cp-parser**: Module AI phân tích cấu trúc DOM/Markdown để trích xuất Title, Statement, Input/Output, và Samples mà không phụ thuộc vào Regex tĩnh.
- **cp-translator**: Module AI dịch thuật và sinh tư duy logic. Đảm bảo bảo toàn 100% công thức Toán Học (Mathematics) và tự động chạy tay thuật toán để giải thích ví dụ.
- **cp-latex**: Module AI render dữ liệu vào "Golden Template", tạo ra file `.tex` chuẩn tiếng Việt.
- **PDF Compiler**: Tool gọi tự động `pdflatex` để xuất bản PDF.

## Quy trình làm việc
Dây chuyền xử lý dữ liệu hoạt động không ngừng nghỉ theo 5 Phase:
1. **Phase 1 (Crawl)**: Tải DOM nguyên bản → `problem_raw.json`
2. **Phase 2 (Parse)**: Nhận diện cấu trúc → `problem_normalized.json`
3. **Phase 3 (Translate)**: Dịch thuật & giải thích → `problem_vi.json`
4. **Phase 4 (LaTeX)**: Gắn vào template → `cache/build/*.tex` rồi gộp bằng `tools/combine_latex.py` → `outputs/output.tex`
5. **Phase 5 (Compile)**: Biên dịch LaTeX → `outputs/output.pdf`

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
