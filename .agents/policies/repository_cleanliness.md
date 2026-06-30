# Chính sách vệ sinh Repository (Repository Cleanliness Policy)

Để duy trì trạng thái repository sạch sẽ, tối giản và dễ hiểu, tất cả các agent (đặc biệt là agent phụ trách crawl/compile) phải tuân thủ nghiêm ngặt các quy định sau:

1. **Không tạo file temp ở root**: Tuyệt đối không lưu bất kỳ file tạm (temporary files) nào tại thư mục gốc của repository.
2. **Không tạo file debug ở root**: Không lưu các file xuất ra phục vụ mục đích debug (e.g. `check_log.txt`, `env.txt`) tại root.
3. **Không tạo file test output ở root**: Mọi output từ quá trình test hoặc chạy thử nghiệm không được nằm ở root.
4. **Quy định về Scratch Files**: Mọi scratch file (file nháp, file lưu dữ liệu tạm thời) phải được chuyển vào thư mục `cache/temp/`.
5. **Quy định về Compile Artifacts**: Mọi compile artifact sinh ra từ quá trình biên dịch LaTeX (e.g. `*.aux`, `*.log`, `*.out`, `*.toc`, `*.synctex.gz`) phải được lưu tại thư mục `cache/build/` hoặc tự động xóa sau khi compile. Không để lại artifacts ở `outputs/` hoặc root.
6. **Quy định về Reports**: Mọi báo cáo (reports) phải được lưu trữ trong thư mục `reports/`.
7. **Quy định về Logs**: Mọi log (bao gồm log lỗi biên dịch như `compile_error.log`) phải được lưu vào thư mục `cache/debug/`.
