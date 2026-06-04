# CP Translation System

## 1. Mục tiêu dự án
Hệ thống xử lý tự động Competitive Programming.
Mục tiêu thu thập các bài toán từ mọi nền tảng (Online Judges), tự động hiểu, dịch sát nghĩa theo ngữ cảnh ICPC/HSG, sinh giải thích tư duy logic từng bước và xuất bản định dạng LaTeX PDF cực kỳ chuyên nghiệp.

## 2. Kiến trúc LLM-First
Thay vì dùng logic tĩnh của Python để bóc tách DOM và tự dịch, hệ thống này đưa toàn bộ gánh nặng tư duy cho AI:
- **Python / Tool**: Chỉ có nhiệm vụ "chân tay" như tải HTML gốc qua Crawler đa lớp (Crawl4AI, Playwright, v.v) và gọi LaTeX Compiler (`latexmk`).
- **LLM (Gemini)**: Đọc HTML thô, hiểu cấu trúc bài, xuất ra JSON tiêu chuẩn, dịch sang tiếng Việt chuẩn CP, viết Explanation, và sinh mã LaTeX.

## 3. Cách cài đặt
```bash
git clone https://github.com/your-username/cp-translation.git
cd cp-translation
pip install -r requirements.txt
playwright install chromium
```
Yêu cầu hệ thống: Có sẵn LaTeX (MiKTeX/TeX Live) với `latexmk`.

## 4. Cách dùng
Khởi động Agent với Antigravity IDE, cung cấp lệnh:
```text
/cp-pipeline Hãy dịch bài toán: <URL>
```
Đầu ra sẽ xuất hiện tại `outputs/output.pdf`.

## 5. Workflow
1. Agent gọi `tools/crawl_problem.py` lấy HTML.
2. Agent đọc HTML sinh `problem_parsed.json`.
3. Agent tự dịch và giải thích sinh `problem_vi.json`.
4. Agent dựa vào `template.tex` để sinh mã LaTeX tại `outputs/output.tex`.
5. Agent gọi `tools/compile_latex.py` xuất ra PDF cuối cùng.

## 6. Ví dụ với Codeforces
Ví dụ với bài "Books" (279B), hệ thống dễ dàng phân tách logic tổng dồn $O(N)$ thay vì phải dịch word-by-word.

## 7. Ví dụ với CSES
CSES có cấu trúc nhẹ, hệ thống sẽ fallback xuống Requests/Playwright nếu cần, lấy cực nhanh và sinh file chuẩn HSG.

## 8. Ví dụ với USACO
USACO thường kể những câu chuyện dài về Nông dân John. LLM sẽ dịch mượt mà câu chuyện này, tránh dịch thô cứng, đồng thời lấy đúng bộ test samples.

## One Command Workflow

```bash
/cp-pipeline https://cses.fi/problemset/task/1640
```

Pipeline:
Crawler
→ Parser
→ Translator
→ LaTeX
→ PDF

Artifacts:
outputs/output.pdf
outputs/output.tex
