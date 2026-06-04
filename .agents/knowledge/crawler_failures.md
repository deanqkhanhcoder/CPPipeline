# CRAWLER FAILURES KNOWLEDGE BASE

## 1. Cloudflare False Positive
**BUG:** Crawler báo lỗi "Cloudflare detected" và dừng crawl dù trang web vẫn hiển thị đề bài bình thường (đặc biệt trên Codeforces).
**ROOT CAUSE:** Codeforces thường chèn các keyword như `cdn-cgi`, `__CF` vào trang web (ví dụ ở các script tĩnh hoặc cookie set) ngay cả trên page hợp lệ (page không bị block).
**FIX:** Chuyển chiến lược phát hiện Cloudflare từ việc chỉ dựa vào keyword văn bản sang việc kiểm tra nội dung thực tế của trang.
**PREVENTION RULE:** 
- KHÔNG BAO GIỜ kết luận Cloudflare chặn CHỈ BẰNG TỪ KHÓA (`__CF`, `Just a moment`).
- LUÔN PHẢI KIỂM TRA sự tồn tại của class chứa nội dung bài toán (ví dụ: `.problem-statement` đối với Codeforces) trước khi đưa ra quyết định Fail. Nếu có nội dung bài toán, đó là crawl thành công.

## 2. Brave Session Lock
**BUG:** Quá trình crawl bằng Playwright + CloakBrowser/Brave bị treo (hang) hoặc crash.
**ROOT CAUSE:** Trình duyệt Brave đang được mở bởi người dùng (User-Data-Dir bị khóa bởi tiến trình khác). Playwright không thể ghi đè session.
**FIX:** Thêm cơ chế catch exception khi khởi tạo Browser Context và in ra lỗi tường minh.
**PREVENTION RULE:** 
- Bắt buộc phải detect lỗi "Browser in use" / "Profile locked". 
- Báo rõ nguyên nhân cho người dùng thay vì retry vô nghĩa. Yêu cầu người dùng đóng trình duyệt trước khi tiếp tục.

## 3. Crawl4AI Failure
**BUG:** Pipeline crash toàn bộ do Crawl4AI ném exception.
**ROOT CAUSE:** Thư viện Crawl4AI hoặc API thay đổi liên tục, gây lỗi import hoặc lỗi runtime.
**FIX:** Thêm cơ chế try-catch bọc quanh Crawl4AI và tự động fallback sang crawler khác (như Playwright nguyên thủy).
**PREVENTION RULE:**
- Crawl4AI không được phép là single point of failure. Nếu Crawl4AI fail, hệ thống PHẢI tự động fallback sang crawler dự phòng.
- KHÔNG BAO GIỜ để crash cả pipeline chỉ vì một công cụ crawl gặp lỗi.

## 4. BRAVE PROFILE CONTENTION
**BUG:** Trình duyệt Brave bị lock liên tục. Playwright báo lỗi "Opening in existing browser session" hoặc "Profile already in use".
**ROOT CAUSE:** Multi-agent crawling. Pipeline spawn nhiều subagent, các subagent này đồng loạt gọi script `crawl_problem.py`, tạo ra tình trạng cạnh tranh tài nguyên (N agents -> N browsers -> N truy cập profile).
**SOLUTION:** Crawler Queue + Single Browser Policy.
**PREVENTION RULE:** 
- KHÔNG BAO GIỜ cho phép subagent gọi độc lập script crawl. Mọi quá trình tải HTML phải được xử lý qua hàng đợi tập trung (`crawler_manager.py`).
- Tại mọi thời điểm, chỉ cho phép 1 instance browser hoạt động.
