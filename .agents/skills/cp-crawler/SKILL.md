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

## Lessons Learned
1. **Cloudflare False Positive**: Keyword detection (như `__CF`) không đáng tin cậy vì các file script của Cloudflare có thể được nhúng vào các page hợp lệ.
2. **Brave Session Lock**: Nếu người dùng đang mở trình duyệt, Playwright không thể ghi đè session và sẽ bị treo/crash.
3. **Crawl4AI Instability**: Thư viện này thường xuyên thay đổi API gây sập toàn hệ thống nếu không có cơ chế bắt lỗi.

## Anti Regression Rules
- **Rule 1**: LUÔN KIỂM TRA sự tồn tại của class bài toán (ví dụ `.problem-statement`) TRƯỚC KHI kết luận Cloudflare chặn bằng keyword.
- **Rule 2**: Phải bắt exception khi khởi tạo Browser Context và in ra thông báo lỗi yêu cầu đóng trình duyệt thay vì retry vô nghĩa.
- **Rule 3**: Mọi crawler module (đặc biệt là Crawl4AI) PHẢI được bọc trong `try-catch` và tự động fallback. Pipeline không được crash vì một crawler hỏng.
- **Rule 4**: CẤM SUBAGENT CRAWL ĐỘC LẬP. Child agents are forbidden from calling `crawl_problem.py`. Mọi quá trình crawl phải được điều phối thông qua Queue bởi `crawler_manager.py`.

## Known Failure Modes
- Playwright bị TimeoutError do Brave đang mở (Session locked).
- Trả về mã HTML giả chứa `Just a moment` nếu bypass thất bại toàn diện.
- API thay đổi ở thư viện Crawl4AI/Playwright làm gãy code khởi tạo trình duyệt.
