# Crawler Documentation Audit

## 1. Phiên bản đang cài
Dựa trên môi trường hiện tại:
- `crawl4ai`: >= 0.1.0 (nhưng thực tế là >=0.8)
- `cloakbrowser`: >= 0.1.0
- `playwright`: >= 1.40.0

## 2. API Chính Thức Hiện Tại
### Crawl4AI
- **Module**: `crawl4ai`
- **Class chính**: `AsyncWebCrawler`
- **Phương thức**: Dùng `async with AsyncWebCrawler() as crawler: await crawler.arun(url)`
- Trả về đối tượng `result` với thuộc tính `result.markdown` và `result.html`.

### CloakBrowser
- **Module**: `cloakbrowser`
- **Hàm chính**: `launch` (sync) hoặc `launch_async` (async)
- **Phương thức**: Trả về `browser` chuẩn tương thích 100% Playwright (`browser.new_page()`, `page.goto()`, `page.content()`).

## 3. Những Lỗi Sai Trong Code Cũ
- **Lỗi 1 (Crawl4AI)**: Code cũ gọi `from crawl4ai import WebCrawler` và `crawler.run()`. Đây là syntax từ version rất cũ hoặc tự suy diễn. API hiện tại bắt buộc dùng Async (`AsyncWebCrawler` và `arun()`).
- **Lỗi 2 (CloakBrowser)**: Code cũ gọi `from cloakbrowser import CloakBrowser` và `b = CloakBrowser()`. Đây là class tự chế. Hàm chuẩn là `from cloakbrowser import launch`.
=> Đây là nguyên nhân trực tiếp dẫn tới việc cả 2 thư viện mạnh nhất đều bị sập ngay từ bước Import ở lần chạy trước.
