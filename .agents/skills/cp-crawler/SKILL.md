---
name: cp-crawler
description: Skill chuyên biệt làm nhiệm vụ lấy dữ liệu HTML/Markdown từ các trang web CP (Codeforces, CSES, USACO...).
---

# CP Crawler

## Tính Năng & Kiến Trúc
Đây là cỗ máy tải dữ liệu mạnh mẽ được thiết kế với cơ chế ưu tiên fallback nhiều lớp để vượt qua Cloudflare và các lớp bảo vệ chống Bot:

1. **Brave Persistent Profile**: Ưu tiên 1. Tái sử dụng Profile và Cookie thật của trình duyệt Brave đang có trên máy để bypass Cloudflare tự nhiên nhất. Yêu cầu Brave phải đóng trước khi chạy pipeline.
2. **CloakBrowser**: Ưu tiên 2. Trình duyệt chuyên trị chống Bot, ngụy trang vân tay (fingerprint) bằng C++.
3. **Playwright Stealth**: Ưu tiên 3. Trình duyệt Playwright có nhúng script vô hiệu hóa webdriver.
4. **Crawl4AI**: Ưu tiên 4. Trình duyệt bất đồng bộ tốc độ cao.

## Cơ chế Retry & Failure Detection
Mỗi fallback đều được tích hợp:
- **Cloudflare Detection**: Quét HTML để tìm chuỗi `cdn-cgi/challenge-platform`, `Just a moment` hoặc `__CF$cv$params`. Nếu dính, tự động fail ngay lập tức, không sinh JSON giả.
- **Vòng lặp Retry**: Nếu bị chặn, crawler sẽ đợi vài giây và retry (2-3 lần) trước khi bỏ cuộc để chuyển sang fallback tiếp theo.

## Scripts
Thực thi crawl:
`python tools/crawl_problem.py <URL>`
