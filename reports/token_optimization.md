# Token Optimization Report

## Tình trạng trước

| File | Kích thước | Nội dung |
|------|-----------|---------|
| `cache/problemset/2219D.json` | **174 KB** | Raw HTML đầy đủ Codeforces (CSS, JS, navigation, fonts, analytics...) |
| `cache/problemset/2232A.json` | 143 KB | Raw HTML đầy đủ |
| `cache/problemset/1502A.json` | 208 KB | Raw HTML đầy đủ |

### Phân tích waste

HTML Codeforces điển hình gồm:
- `<head>`: CSS links (~15KB), JavaScript (~100KB), fonts, analytics
- `<body>` navigation header/footer: ~30KB
- `.problem-statement`: **~3-10KB** (thứ thực sự cần)

=> **Token waste: 97-99%**. LLM đọc 174KB chỉ để dùng 4KB.

## Giải pháp: html_extractor.py

### Tool mới: `tools/html_extractor.py`

```
Input:  cache/problemset/<id>.json  (raw, 100-270KB)
Output: cache/normalized/<id>.json  (clean fragment, 5-50KB)
```

**Nguyên tắc LLM-First được giữ nguyên:**
- Python chỉ dùng BeautifulSoup để tìm `.problem-statement` div
- Python **KHÔNG** parse content, extract text, hay dịch bất cứ gì
- Toàn bộ phân tích ngữ nghĩa vẫn do Gemini thực hiện

### Schema mới (`cache/normalized/`)

```json
{
  "problem_id": "2219D",
  "url": "https://codeforces.com/problemset/problem/2219/D",
  "source": "Codeforces",
  "title": "Problem - 2219D - Codeforces",
  "timestamp": "2026-06-12T...",
  "type": "html",
  "content": "<div class='problem-statement'>...</div>",
  "pdf_path": null,
  "images": []
}
```

## Kết quả đo lường thực tế

### 2219D (Codeforces)

| Metric | Before | After |
|--------|--------|-------|
| File size | 174 KB | 51 KB |
| Reduction | — | **70%** |
| Content extracted | 174 KB raw HTML | 48 KB `.problem-statement` |

*Note: Codeforces `.problem-statement` vẫn 48KB vì MathJax rendered HTML. Nếu strip MathJax thêm sẽ xuống ~10KB. Tuy nhiên, strip MathJax có rủi ro mất công thức.*

### Ước tính trung bình toàn dataset

| Nguồn | Raw HTML | Normalized | Reduction |
|-------|---------|-----------|---------|
| Codeforces | ~140KB | ~45KB | ~68% |
| CSES | ~80KB | ~15KB | ~81% |
| USACO | PDF-based | PDF images | N/A |

## Cache Lifecycle (Chuẩn hoá)

```
URL
 ↓ crawl_problem.py
cache/problemset/<id>.json    ← raw, 100-270KB, KHÔNG cho LLM đọc
 ↓ html_extractor.py (Python, structural only)
cache/normalized/<id>.json   ← fragment, 5-50KB, LLM đọc từ đây
 ↓ cp-parser (Gemini)
cache/clean/<id>.json        ← structured JSON
 ↓ cp-translator (Gemini)
cache/build/<id>.tex         ← LaTeX fragment
 ↓ combine + compile
outputs/output.pdf
```

## Quy tắc bắt buộc (đã cập nhật vào Skills)

- `cp-pipeline`: Parser phải đọc `cache/normalized/`, không được đọc `cache/problemset/`
- `cp-parser`: Đọc field `content` trong normalized JSON
- Trước khi spawn parser: chạy `python tools/html_extractor.py <id>`
