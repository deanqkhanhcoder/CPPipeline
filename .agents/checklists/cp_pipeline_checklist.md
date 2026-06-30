# CP Pipeline Pre-flight Checklist

Hệ thống chỉ được phép báo cáo PASS (Thành công) khi và chỉ khi TẤT CẢ các mục dưới đây được đánh dấu hoàn thành:

- [ ] **Crawl Success**: Nội dung DOM hợp lệ được lấy về, không dính Cloudflare/Access Denied.
- [ ] **Parser Success**: Trích xuất thành công JSON chứa đủ Title, Statement, Input, Output, Constraints, Samples.
- [ ] **Translation Success**: Dịch sang tiếng Việt hoàn tất, giữ nguyên công thức toán học và test cases.
- [ ] **Explanation Generated**: Đã sinh giải thích (explanation) rõ ràng cho ít nhất một Sample test.
- [ ] **Template Loaded**: Nạp thành công `template.tex` làm cấu trúc Header/Footer gốc (Single Source Of Truth).
- [ ] **TOC Generated**: Có danh sách các bài toán (problems) xuất hiện trong Table of Contents (click được).
- [ ] **pdflatex Pass 1**: Trình biên dịch chạy thành công lần 1 (sinh file `.toc`).
- [ ] **pdflatex Pass 2**: Trình biên dịch chạy thành công lần 2 (nhúng `.toc` vào văn bản).
- [ ] **Return Code = 0**: Cả hai lần chạy lệnh biên dịch đều trả về Exit Code 0 (Không có lỗi Fatal/Undefined).
- [ ] **PDF Exists**: File `outputs/output.pdf` đã thực sự được sinh ra mới trên ổ đĩa cứng.
- [ ] **Archive Updated**: Kết quả được lưu trữ an toàn vào thư mục `archive/` cùng với siêu dữ liệu (`index.json`).

Nếu bất kỳ điều kiện nào bị bỏ trống, toàn bộ tiến trình PHẢI được đánh giá là THẤT BẠI.
