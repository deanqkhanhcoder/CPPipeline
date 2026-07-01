import os
import re
import sys
from pathlib import Path

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / ".agents" / "skills"
REPORTS_DIR = ROOT / "reports"

def audit_skills():
    if not SKILLS_DIR.exists():
        print(f"[Skill Audit] Error: {SKILLS_DIR} does not exist.", file=sys.stderr)
        return False
        
    skills = [d for d in SKILLS_DIR.iterdir() if d.is_dir()]
    report_lines = [
        "# MULTI-AGENT ARCHITECTURE AUDIT REPORT (Phase 1)",
        "",
        "Báo cáo đánh giá hiện trạng hệ thống Agent/Skill và đề xuất mô hình phân tách Multi-Agent.",
        "",
        "## 1. Hiện trạng các Skill hiện tại",
        ""
    ]
    
    total_skills = 0
    overlaps = []
    monolithic_skills = []
    vague_skills = []
    
    for skill_path in skills:
        skill_file = skill_path / "SKILL.md"
        if not skill_file.exists():
            continue
            
        total_skills += 1
        content = skill_file.read_text(encoding="utf-8")
        
        # Count lines & size
        lines = content.split('\n')
        line_count = len(lines)
        size_bytes = len(content)
        
        # Analyze Frontmatter Versioning
        has_version = "version:" in content or "Version:" in content
        has_owner = "owner:" in content or "Owner:" in content
        has_contract = "Input" in content and "Output" in content
        
        report_lines.append(f"### Skill: `{skill_path.name}`")
        report_lines.append(f"- **Đường dẫn**: `{skill_file.relative_to(ROOT)}`")
        report_lines.append(f"- **Kích thước**: {line_count} dòng ({size_bytes} bytes)")
        report_lines.append(f"- **Định nghĩa Input/Output**: {'Có' if has_contract else 'Không'}")
        report_lines.append(f"- **Siêu dữ liệu Version/Owner**: {'Có' if has_version else 'Không'}")
        
        # Heuristics for monolithic or vague skills
        reasons = []
        if line_count > 100:
            reasons.append("Kích thước quá lớn (> 100 dòng)")
        if skill_path.name == "cp-translator":
            reasons.append("Đảm nhận quá nhiều trách nhiệm (Dịch, Viết lại văn phong, Kiểm tra thuật ngữ, Tạo giải thích)")
            monolithic_skills.append(skill_path.name)
        if skill_path.name == "cp-latex":
            reasons.append("Đảm nhận cả sinh mã LaTeX và kiểm duyệt/validate lỗi compiler")
            monolithic_skills.append(skill_path.name)
        if skill_path.name == "cp-pipeline":
            reasons.append("Orchestrator thô sơ, chưa hỗ trợ song song thực sự và trừu tượng hóa model")
            monolithic_skills.append(skill_path.name)
            
        if reasons:
            report_lines.append("- **Vấn đề phát hiện**:")
            for r in reasons:
                report_lines.append(f"  - ⚠️ {r}")
        else:
            report_lines.append("- **Trạng thái**: Tốt, nhiệm vụ đơn lẻ.")
            
        report_lines.append("")
        
    # Phase 2 & 3 Redesign Proposals
    report_lines.extend([
        "## 2. Đề xuất Kiến trúc Multi-Agent mới (V2)",
        "",
        "Để giải quyết các vấn đề trên và đáp ứng 15 Phase yêu cầu, hệ thống sẽ được phân tách thành các Agent đơn nhiệm chuyên biệt sau:",
        "",
        "### A. Nhóm Dịch thuật & Biên tập (Translation & Editorial)",
        "1. **`translation-agent`**: Dịch thô đề bài từ tiếng Anh sang tiếng Việt, bảo toàn công thức toán học.",
        "2. **`editorial-agent`**: Cải thiện cấu trúc đoạn văn, reflow câu chữ, chia đoạn logic (< 12 dòng), tạo văn phong tự nhiên chuẩn Sách HSG.",
        "3. **`terminology-agent`**: So khớp và chuẩn hóa thuật ngữ tiếng Việt theo từ điển `terminology.md`.",
        "",
        "### B. Nhóm Sinh mã & Bảo vệ LaTeX (LaTeX & Guardians)",
        "1. **`latex-agent`**: Sinh mã `.tex` tương thích với Golden Template.",
        "2. **`latex-guardian`**: Kiểm soát cú pháp LaTeX thô, đảm bảo escape chính xác các ký tự đặc biệt, kiểm tra math/table/list environments.",
        "3. **`order-guardian`**: Đối chiếu thứ tự bài toán từ URL gốc -> Queue -> PDF -> TOC -> Metadata.",
        "",
        "### C. Nhóm Kiểm duyệt & Đánh giá (QA & Output Validator)",
        "1. **`qa-agent` / `output-validator`**: Chấm điểm chất lượng 5 tiêu chí (Statement, Explanation, Formatting, Readability, Conversion). Chặn build nếu điểm trung bình < 4.0.",
        "",
        "## 3. Bản Hợp đồng của Agent (Agent Contract Specification)",
        "Mỗi Agent mới sẽ bắt buộc phải tuân thủ schema:",
        "- **Input**: Kiểu dữ liệu và trường bắt buộc nhận vào.",
        "- **Output**: Kiểu dữ liệu trả ra.",
        "- **Responsibility**: Trách nhiệm duy nhất.",
        "- **Forbidden**: Các hành vi bị cấm.",
        "- **Failure Mode & Retry Policy**: Cách thức ứng phó khi gặp sự cố.",
        ""
    ])
    
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_file = REPORTS_DIR / "multi_agent_audit.md"
    report_file.write_text("\n".join(report_lines) + "\n", encoding="utf-8", newline="\n")
    print(f"[Skill Audit] Created audit report at {report_file}")
    return True

if __name__ == "__main__":
    audit_skills()
