# MULTI-AGENT ARCHITECTURE AUDIT REPORT (Phase 1)

Báo cáo đánh giá hiện trạng hệ thống Agent/Skill và đề xuất mô hình phân tách Multi-Agent.

## 1. Hiện trạng các Skill hiện tại

### Skill: `cavecrew`
- **Đường dẫn**: `.agents\skills\cavecrew\SKILL.md`
- **Kích thước**: 91 dòng (4080 bytes)
- **Định nghĩa Input/Output**: Không
- **Siêu dữ liệu Version/Owner**: Không
- **Trạng thái**: Tốt, nhiệm vụ đơn lẻ.

### Skill: `caveman`
- **Đường dẫn**: `.agents\skills\caveman\SKILL.md`
- **Kích thước**: 86 dòng (5026 bytes)
- **Định nghĩa Input/Output**: Không
- **Siêu dữ liệu Version/Owner**: Không
- **Trạng thái**: Tốt, nhiệm vụ đơn lẻ.

### Skill: `caveman-commit`
- **Đường dẫn**: `.agents\skills\caveman-commit\SKILL.md`
- **Kích thước**: 74 dòng (2745 bytes)
- **Định nghĩa Input/Output**: Không
- **Siêu dữ liệu Version/Owner**: Không
- **Trạng thái**: Tốt, nhiệm vụ đơn lẻ.

### Skill: `caveman-compress`
- **Đường dẫn**: `.agents\skills\caveman-compress\SKILL.md`
- **Kích thước**: 120 dòng (4706 bytes)
- **Định nghĩa Input/Output**: Không
- **Siêu dữ liệu Version/Owner**: Không
- **Vấn đề phát hiện**:
  - ⚠️ Kích thước quá lớn (> 100 dòng)

### Skill: `caveman-help`
- **Đường dẫn**: `.agents\skills\caveman-help\SKILL.md`
- **Kích thước**: 72 dòng (2467 bytes)
- **Định nghĩa Input/Output**: Không
- **Siêu dữ liệu Version/Owner**: Không
- **Trạng thái**: Tốt, nhiệm vụ đơn lẻ.

### Skill: `caveman-stats`
- **Đường dẫn**: `.agents\skills\caveman-stats\SKILL.md`
- **Kích thước**: 19 dòng (782 bytes)
- **Định nghĩa Input/Output**: Không
- **Siêu dữ liệu Version/Owner**: Không
- **Trạng thái**: Tốt, nhiệm vụ đơn lẻ.

### Skill: `cp-crawler`
- **Đường dẫn**: `.agents\skills\cp-crawler\SKILL.md`
- **Kích thước**: 51 dòng (3029 bytes)
- **Định nghĩa Input/Output**: Không
- **Siêu dữ liệu Version/Owner**: Không
- **Trạng thái**: Tốt, nhiệm vụ đơn lẻ.

### Skill: `cp-parser`
- **Đường dẫn**: `.agents\skills\cp-parser\SKILL.md`
- **Kích thước**: 66 dòng (3948 bytes)
- **Định nghĩa Input/Output**: Có
- **Siêu dữ liệu Version/Owner**: Không
- **Trạng thái**: Tốt, nhiệm vụ đơn lẻ.

### Skill: `cp-pipeline`
- **Đường dẫn**: `.agents\skills\cp-pipeline\SKILL.md`
- **Kích thước**: 264 dòng (16069 bytes)
- **Định nghĩa Input/Output**: Có
- **Siêu dữ liệu Version/Owner**: Không
- **Vấn đề phát hiện**:
  - ⚠️ Kích thước quá lớn (> 100 dòng)
  - ⚠️ Orchestrator thô sơ, chưa hỗ trợ song song thực sự và trừu tượng hóa model

### Skill: `editorial-agent`
- **Đường dẫn**: `.agents\skills\editorial-agent\SKILL.md`
- **Kích thước**: 55 dòng (2179 bytes)
- **Định nghĩa Input/Output**: Có
- **Siêu dữ liệu Version/Owner**: Có
- **Trạng thái**: Tốt, nhiệm vụ đơn lẻ.

### Skill: `formatting-agent`
- **Đường dẫn**: `.agents\skills\formatting-agent\SKILL.md`
- **Kích thước**: 56 dòng (2074 bytes)
- **Định nghĩa Input/Output**: Có
- **Siêu dữ liệu Version/Owner**: Có
- **Trạng thái**: Tốt, nhiệm vụ đơn lẻ.

### Skill: `fragment-qa`
- **Đường dẫn**: `.agents\skills\fragment-qa\SKILL.md`
- **Kích thước**: 43 dòng (1249 bytes)
- **Định nghĩa Input/Output**: Có
- **Siêu dữ liệu Version/Owner**: Không
- **Trạng thái**: Tốt, nhiệm vụ đơn lẻ.

### Skill: `latex-agent`
- **Đường dẫn**: `.agents\skills\latex-agent\SKILL.md`
- **Kích thước**: 75 dòng (2919 bytes)
- **Định nghĩa Input/Output**: Có
- **Siêu dữ liệu Version/Owner**: Có
- **Trạng thái**: Tốt, nhiệm vụ đơn lẻ.

### Skill: `latex-guardian`
- **Đường dẫn**: `.agents\skills\latex-guardian\SKILL.md`
- **Kích thước**: 52 dòng (1970 bytes)
- **Định nghĩa Input/Output**: Có
- **Siêu dữ liệu Version/Owner**: Có
- **Trạng thái**: Tốt, nhiệm vụ đơn lẻ.

### Skill: `order-guardian`
- **Đường dẫn**: `.agents\skills\order-guardian\SKILL.md`
- **Kích thước**: 38 dòng (1309 bytes)
- **Định nghĩa Input/Output**: Có
- **Siêu dữ liệu Version/Owner**: Có
- **Trạng thái**: Tốt, nhiệm vụ đơn lẻ.

### Skill: `qa-agent`
- **Đường dẫn**: `.agents\skills\qa-agent\SKILL.md`
- **Kích thước**: 64 dòng (2512 bytes)
- **Định nghĩa Input/Output**: Có
- **Siêu dữ liệu Version/Owner**: Có
- **Trạng thái**: Tốt, nhiệm vụ đơn lẻ.

### Skill: `sample-explainer`
- **Đường dẫn**: `.agents\skills\sample-explainer\SKILL.md`
- **Kích thước**: 213 dòng (4499 bytes)
- **Định nghĩa Input/Output**: Có
- **Siêu dữ liệu Version/Owner**: Có
- **Vấn đề phát hiện**:
  - ⚠️ Kích thước quá lớn (> 100 dòng)

### Skill: `semantic-fidelity-reviewer`
- **Đường dẫn**: `.agents\skills\semantic-fidelity-reviewer\SKILL.md`
- **Kích thước**: 107 dòng (3627 bytes)
- **Định nghĩa Input/Output**: Có
- **Siêu dữ liệu Version/Owner**: Có
- **Vấn đề phát hiện**:
  - ⚠️ Kích thước quá lớn (> 100 dòng)

### Skill: `terminology-agent`
- **Đường dẫn**: `.agents\skills\terminology-agent\SKILL.md`
- **Kích thước**: 49 dòng (1740 bytes)
- **Định nghĩa Input/Output**: Có
- **Siêu dữ liệu Version/Owner**: Có
- **Trạng thái**: Tốt, nhiệm vụ đơn lẻ.

### Skill: `translation-agent`
- **Đường dẫn**: `.agents\skills\translation-agent\SKILL.md`
- **Kích thước**: 91 dòng (4003 bytes)
- **Định nghĩa Input/Output**: Có
- **Siêu dữ liệu Version/Owner**: Có
- **Trạng thái**: Tốt, nhiệm vụ đơn lẻ.

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

