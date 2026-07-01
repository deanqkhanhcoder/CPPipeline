# MULTI-AGENT ARCHITECTURE AUDIT REPORT (Phase 1)

Báo cáo đánh giá hiện trạng hệ thống Agent/Skill và đề xuất mô hình phân tách Multi-Agent.

## 1. Hiện trạng các Skill hiện tại

### Skill: `cavecrew`
- **Đường dẫn**: `.agents\skills\cavecrew\SKILL.md`
- **Kích thước**: 83 dòng (3901 bytes)
- **Định nghĩa Input/Output**: Không
- **Siêu dữ liệu Version/Owner**: Không
- **Trạng thái**: Tốt, nhiệm vụ đơn lẻ.

### Skill: `caveman`
- **Đường dẫn**: `.agents\skills\caveman\SKILL.md`
- **Kích thước**: 78 dòng (4847 bytes)
- **Định nghĩa Input/Output**: Không
- **Siêu dữ liệu Version/Owner**: Không
- **Trạng thái**: Tốt, nhiệm vụ đơn lẻ.

### Skill: `caveman-commit`
- **Đường dẫn**: `.agents\skills\caveman-commit\SKILL.md`
- **Kích thước**: 66 dòng (2566 bytes)
- **Định nghĩa Input/Output**: Không
- **Siêu dữ liệu Version/Owner**: Không
- **Trạng thái**: Tốt, nhiệm vụ đơn lẻ.

### Skill: `caveman-compress`
- **Đường dẫn**: `.agents\skills\caveman-compress\SKILL.md`
- **Kích thước**: 112 dòng (4527 bytes)
- **Định nghĩa Input/Output**: Không
- **Siêu dữ liệu Version/Owner**: Không
- **Vấn đề phát hiện**:
  - ⚠️ Kích thước quá lớn (> 100 dòng)

### Skill: `caveman-help`
- **Đường dẫn**: `.agents\skills\caveman-help\SKILL.md`
- **Kích thước**: 64 dòng (2288 bytes)
- **Định nghĩa Input/Output**: Không
- **Siêu dữ liệu Version/Owner**: Không
- **Trạng thái**: Tốt, nhiệm vụ đơn lẻ.

### Skill: `caveman-stats`
- **Đường dẫn**: `.agents\skills\caveman-stats\SKILL.md`
- **Kích thước**: 11 dòng (603 bytes)
- **Định nghĩa Input/Output**: Không
- **Siêu dữ liệu Version/Owner**: Không
- **Trạng thái**: Tốt, nhiệm vụ đơn lẻ.

### Skill: `cp-crawler`
- **Đường dẫn**: `.agents\skills\cp-crawler\SKILL.md`
- **Kích thước**: 40 dòng (2531 bytes)
- **Định nghĩa Input/Output**: Không
- **Siêu dữ liệu Version/Owner**: Không
- **Trạng thái**: Tốt, nhiệm vụ đơn lẻ.

### Skill: `cp-latex`
- **Đường dẫn**: `.agents\skills\cp-latex\SKILL.md`
- **Kích thước**: 64 dòng (5000 bytes)
- **Định nghĩa Input/Output**: Không
- **Siêu dữ liệu Version/Owner**: Không
- **Vấn đề phát hiện**:
  - ⚠️ Đảm nhận cả sinh mã LaTeX và kiểm duyệt/validate lỗi compiler

### Skill: `cp-parser`
- **Đường dẫn**: `.agents\skills\cp-parser\SKILL.md`
- **Kích thước**: 44 dòng (3141 bytes)
- **Định nghĩa Input/Output**: Có
- **Siêu dữ liệu Version/Owner**: Không
- **Trạng thái**: Tốt, nhiệm vụ đơn lẻ.

### Skill: `cp-pipeline`
- **Đường dẫn**: `.agents\skills\cp-pipeline\SKILL.md`
- **Kích thước**: 185 dòng (11006 bytes)
- **Định nghĩa Input/Output**: Có
- **Siêu dữ liệu Version/Owner**: Không
- **Vấn đề phát hiện**:
  - ⚠️ Kích thước quá lớn (> 100 dòng)
  - ⚠️ Orchestrator thô sơ, chưa hỗ trợ song song thực sự và trừu tượng hóa model

### Skill: `cp-translator`
- **Đường dẫn**: `.agents\skills\cp-translator\SKILL.md`
- **Kích thước**: 30 dòng (2140 bytes)
- **Định nghĩa Input/Output**: Không
- **Siêu dữ liệu Version/Owner**: Không
- **Vấn đề phát hiện**:
  - ⚠️ Đảm nhận quá nhiều trách nhiệm (Dịch, Viết lại văn phong, Kiểm tra thuật ngữ, Tạo giải thích)

## 2. Đề xuất Kiến trúc Multi-Agent mới (V2)

Để giải quyết các vấn đề trên và đáp ứng 15 Phase yêu cầu, hệ thống sẽ được phân tách thành các Agent đơn nhiệm chuyên biệt sau:

### A. Nhóm Dịch thuật & Biên tập (Translation & Editorial)
1. **`translation-agent`**: Dịch thô đề bài từ tiếng Anh sang tiếng Việt, bảo toàn công thức toán học.
2. **`editorial-agent`**: Cải thiện cấu trúc đoạn văn, reflow câu chữ, chia đoạn logic (< 12 dòng), tạo văn phong tự nhiên chuẩn Sách HSG.
3. **`terminology-agent`**: So khớp và chuẩn hóa thuật ngữ tiếng Việt theo từ điển `terminology.md`.

### B. Nhóm Sinh mã & Bảo vệ LaTeX (LaTeX & Guardians)
1. **`latex-agent`**: Sinh mã `.tex` tương thích với Golden Template.
2. **`latex-guardian`**: Kiểm soát cú pháp LaTeX thô, đảm bảo escape chính xác các ký tự đặc biệt, kiểm tra math/table/list environments.
3. **`order-guardian`**: Đối chiếu thứ tự bài toán từ URL gốc -> Queue -> PDF -> TOC -> Metadata.

### C. Nhóm Kiểm duyệt & Đánh giá (QA & Output Validator)
1. **`qa-agent` / `output-validator`**: Chấm điểm chất lượng 5 tiêu chí (Statement, Explanation, Formatting, Readability, Conversion). Chặn build nếu điểm trung bình < 4.0.

## 3. Bản Hợp đồng của Agent (Agent Contract Specification)
Mỗi Agent mới sẽ bắt buộc phải tuân thủ schema:
- **Input**: Kiểu dữ liệu và trường bắt buộc nhận vào.
- **Output**: Kiểu dữ liệu trả ra.
- **Responsibility**: Trách nhiệm duy nhất.
- **Forbidden**: Các hành vi bị cấm.
- **Failure Mode & Retry Policy**: Cách thức ứng phó khi gặp sự cố.

