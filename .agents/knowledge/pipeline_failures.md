# PIPELINE FAILURES KNOWLEDGE BASE

## 1. Gemini báo PASS dù compile fail
**BUG:** Đặc vụ báo cáo quá trình chạy hoàn tất thành công (PASS) nhưng khi kiểm tra thì file log lại báo `Fatal error occurred, no output PDF file produced!`.
**ROOT CAUSE:** Đặc vụ chỉ kiểm tra hời hợt sự tồn tại của file trên ổ đĩa, hoặc tin tưởng hoàn toàn vào log output stdout mà không kiểm tra return code.
**FIX:** Yêu cầu đặc vụ / script bắt buộc phải verify return code và parse nội dung file log lỗi trước khi kết luận.
**PREVENTION RULE:**
- KHÔNG BAO GIỜ được tin tưởng việc chỉ có file PDF tồn tại đồng nghĩa với thành công.
- PHẢI check returncode của lệnh biên dịch.
- PHẢI đọc file log (`compile_error.log`) để xác nhận không có `LaTeX Error` hay `Fatal Error`.

## 2. Subagent Hallucinate Macro
**BUG:** Các file `.tex` được sinh ra chứa các lệnh như `\exmp`, `\inputformat`, `\begin{exmpIn}` dù chúng không hề có mặt trong tài liệu gốc. Gây sập hệ thống biên dịch.
**ROOT CAUSE:** LLM có thiên hướng "tự bịa" ra các macro dựa trên dữ liệu training cũ của nó về Competitive Programming LaTeX, thay vì tuân thủ nghiêm ngặt Prompt Template.
**FIX:** Siết chặt prompt (System Instruction / Skill MD) và dọn dẹp (sanitize) output bằng script.
**PREVENTION RULE:**
- CHỈ ĐƯỢC PHÉP dùng các macro đã tồn tại một cách rõ ràng trong `template.tex`.
- Pipeline (Python script) phải đóng vai trò gatekeeper để gỡ bỏ mọi macro ảo giác trước khi đưa cho LaTeX compiler.
