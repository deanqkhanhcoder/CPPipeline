# CPPipeline

Hệ thống dịch thuật tự động Competitive Programming (CP) với kiến trúc LLM-First Orchestration. 
Nhiệm vụ của dự án là lấy dữ liệu từ bất kỳ Online Judge nào (Codeforces, CSES, USACO...), tự động phân tích ngữ nghĩa, dịch sang Tiếng Việt chuẩn ICPC/HSG, tự động sinh giải thích chi tiết cho từng Test Case, và cuối cùng biên dịch ra một tài liệu PDF bằng LaTeX có chất lượng xuất bản.

## Architecture
Hệ thống sử dụng mô hình **Chain-of-Skills** dựa trên sức mạnh của AI (Gemini Agent):
- **cp-pipeline (Orchestrator)**: "Nhạc trưởng" điều phối luồng dữ liệu tự động.
- **cp-crawler**: Module thu thập dữ liệu thô. Sử dụng 4 tầng Fallback (CloakBrowser → Crawl4AI → Playwright → Requests) để xuyên thủng các hàng rào chống Bot như Cloudflare.
- **cp-parser**: Module AI phân tích cấu trúc DOM/Markdown để trích xuất Title, Statement, Input/Output, và Samples mà không phụ thuộc vào Regex tĩnh.
- **cp-translator**: Module AI dịch thuật và sinh tư duy logic. Đảm bảo bảo toàn 100% công thức Toán Học (Mathematics) và tự động chạy tay thuật toán để giải thích ví dụ.
- **cp-latex**: Module AI render dữ liệu vào "Golden Template", tạo ra file `.tex` chuẩn tiếng Việt.
- **PDF Compiler**: Tool gọi tự động `pdflatex` để xuất bản PDF.

## Workflow
Dây chuyền xử lý dữ liệu hoạt động không ngừng nghỉ theo 5 Phase:
1. **Phase 1 (Crawl)**: Tải DOM nguyên bản → `problem_raw.json`
2. **Phase 2 (Parse)**: Nhận diện cấu trúc → `problem_normalized.json`
3. **Phase 3 (Translate)**: Dịch thuật & giải thích → `problem_vi.json`
4. **Phase 4 (LaTeX)**: Gắn vào template → `outputs/output.tex`
5. **Phase 5 (Compile)**: Biên dịch LaTeX → `outputs/output.pdf`

## Directory Structure
```text
CPPipeline/
├── .agents/
│   └── skills/           # Chứa não bộ AI và luật chơi cho từng skill
│       ├── cp-pipeline/  # Orchestrator
│       ├── cp-crawler/
│       ├── cp-parser/
│       ├── cp-translator/
│       └── cp-latex/
├── cache/                # Chứa các file trung gian (Raw/Parsed/Translated JSON)
├── outputs/              # Chứa sản phẩm cuối cùng (output.tex, output.pdf)
├── reports/              # Chứa các báo cáo Audit, Lỗi, và Validation
├── tools/                # Chứa Python Scripts (Crawl I/O, Compile PDF)
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE
```

## Quick Start
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

## One Command Workflow
Mở hệ thống Agent, chỉ cần đưa ra một dòng lệnh duy nhất kèm theo URL (hỗ trợ nhiều URL cùng lúc):
```bash
/cp-pipeline https://cses.fi/problemset/task/1640
```
Agent sẽ tự động chuỗi hóa toàn bộ các tiến trình. Nhiệm vụ của bạn chỉ là chờ đợi và nhận thành quả tại thư mục:
- `outputs/output.pdf`
- `outputs/output.tex`
