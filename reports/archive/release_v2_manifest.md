# Release Manifest - CPPipeline v2.0

Bản phát hành chính thức v2.0 của CPPipeline - Hệ thống dịch thuật tự động Competitive Programming.

---

## 📌 Thông tin Phiên bản (Release Details)

- **Phiên bản (Version):** `v2.0`
- **Nhánh (Branch):** `master`
- **Nhãn phát hành (Tag):** `v2.0`
- **Ngày phát hành (Release Date):** 2026-07-01
- **Môi trường đề xuất:** Mọi AI Host hỗ trợ đặc tả `.agents/` (Antigravity, Cursor, Claude Code, Cline, Roo Code, etc.)

---

## 🏆 Kết quả Audit & Test (Validation Results)

- **Repository Guard Audit:** **PASS** (Đồng bộ UTF-8, dọn sạch tệp rác, không chứa file debug/temporary).
- **TOC & Order Preservation:** **PASS** (TOC khớp 100% với số bài, thứ tự các bài trong PDF trùng khớp hoàn toàn thứ tự URL đầu vào).
- **Stress Test (55 URLs đồng thời):** **PASS** (Không xảy ra deadlock, không starvation, không mất job, bảo toàn thứ tự).
- **Template Contract Smoke Test:** **PASS**
- **TOC Regression Test:** **PASS**
- **Order Preservation Regression Test:** **PASS**

---

## 🔄 Các thay đổi lớn & Phá vỡ tương thích (Breaking Changes)

- **Orchestration Shift:** Loại bỏ hoàn toàn lớp code Python trung gian (`tools/llm_backend.py`, `tools/agent_framework.py`, `tools/pipeline_v2.py`) gọi API ngoài. Thay thế bằng cơ chế đặc tả declarative Host LLM trong `.agents/skills/cp-pipeline/SKILL.md`.
- **Modular AI Skills:** Thay thế 2 skill gộp cũ (`cp-translator`, `cp-latex`) bằng bộ 6 sub-agents chuyên môn hóa cao (`translation-agent`, `editorial-agent`, `terminology-agent`, `formatting-agent`, `latex-agent`, `latex-guardian`).
- **Template Isolation:** Di chuyển file quy chuẩn `template.tex` từ skill folder `cp-latex/` cũ sang một thư mục độc lập `.agents/templates/template.tex` nhằm đảm bảo tính toàn vẹn kiến trúc.

---

## ⚠️ Giới hạn Đã biết (Known Limitations)

- **Trình duyệt Brave:** Yêu cầu đóng trình duyệt Brave trên máy cục bộ trước khi chạy để tránh xung đột session cookie khi crawl Codeforces/CSES chống bot.

---

## 🗺️ Lộ trình Tương lai (Future Roadmap)

- Tích hợp thêm các bộ parser tự động cho các Online Judge nội địa khác.
- Tự động hóa việc phân chia tiểu nhiệm vụ (sub-tasks) để xử lý lượng đề lớn cực nhanh.
- Cơ chế cache PDF ở cấp độ trang (page-level preview caching).
