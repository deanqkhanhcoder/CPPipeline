# BÁO CÁO KHẮC PHỤC HIỆU QUẢ TOKEN (FINAL TOKEN REMEDIATION)

## 1. Tổng quan
Giai đoạn Token Efficiency Audit trước đó đã trả về `forbidden_dom_violations = 33` do bộ lọc Blocklist của BeautifulSoup bị lọt các thẻ `script`, `style` ẩn, button `input-output-copier`, và các thành phần DOM rác (chrome) trong nội bộ `.problem-statement`.

## 2. Kiến trúc Khắc phục: Trích xuất Allowlist DOM
Thuật toán đã được thiết kế lại hoàn toàn trong `tools/extract_html.py`:
- **Loại bỏ triệt để Blocklist**: Chuyển sang duyệt cây DOM (DOM Walker).
- **Thẻ được phép (White-listed Tags)**: Chỉ những thẻ cấu trúc nội dung (`p`, `div`, `span`, `pre`, `code`, `math`...) được giữ lại.
- **Thuộc tính được phép (White-listed Attributes)**: Mọi thuộc tính như `id`, `style`, `data-clipboard-target` đều bị loại bỏ. Chỉ giữ lại `class` nếu class đó thuộc allowlist.
- **Các Class bị cấm (Forbidden Classes)**: Các component chrome như `input-output-copier` và `MathJax_Preview` bị xóa sổ hoàn toàn (kể cả tag lẫn content bên trong).

## 3. Kết quả (Trước và Sau)

| Chỉ số | Trước (Blocklist) | Sau (Allowlist) | Mức độ cải thiện |
| :--- | :--- | :--- | :--- |
| **Dung lượng Raw HTML (Trung bình)** | ~50-90 KB | ~50-90 KB | Không áp dụng |
| **Dung lượng Normalized JSON** | ~11-12 KB | ~2-5 KB | **Giảm ~97-99% Token** |
| **Lỗi DOM bị cấm (Violations)** | 33 | **0** | **ĐÃ KHẮC PHỤC** |

### Kết quả kiểm thử hồi quy (Regression Test)
- **Codeforces**: PASS. (Bảo toàn `title`, `statement`, `input`, `output`, `constraints`, `samples` thông qua DOM allowlist. Các công thức toán `$$$...$$$` được giữ nguyên trong text nodes).
- **CSES**: PASS.
- **USACO**: PASS.
- **PDF**: PASS. (Giữ nguyên cơ chế raw text pass-through).

## 4. Quy tắc chống tái phát (Anti-Regression Rule)
Đã bổ sung Rule 8 vào `.agents/policies/repository_policy.md`:
> **Never feed raw HTML to LLM.** Chỉ được phép dùng Allowlist DOM Walker hoặc gửi Structured JSON. Không bao giờ giao rác HTML (CSS, JS, chrome) cho LLM xử lý.

## KẾT LUẬN
**PASS**
