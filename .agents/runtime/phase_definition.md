---
title: CP Pipeline Phase Definitions
version: 3.0.0
type: Runtime Architecture
---

# Phase Definitions for Host LLM

Mỗi phase định nghĩa một bước rõ ràng trong pipeline. Host LLM phải tuân theo từng phase.

## PHASE 1: CRAWL

**Responsibility:** Download raw HTML/Markdown từ URL

**Skill:** cp-crawler

**Input:**
- URL (hoặc danh sách URLs)

**Output:**
- `cache/problemset/<id>.json` (raw HTML/content)
- `cache/queue/index.json` (updated with problem metadata)

**Preconditions:**
- URL phải hợp lệ
- Network phải khả dụng
- Crawler không được overload

**Postconditions:**
- File phải tồn tại trên disk
- File phải có content
- Không được empty

**Dependencies:**
- Policy: repository_policy.md
- Policy: encoding_policy.md

**Self-Validation:**
- File exists? ✓
- File size > 0? ✓
- UTF-8 encoding valid? ✓
- JSON structure valid (if .json)? ✓

---

## PHASE 2: PARSE

**Responsibility:** Extract structured data từ raw content

**Skill:** cp-parser

**Input:**
- `cache/problemset/<id>.json` (raw content)

**Output:**
- `cache/normalized/<id>.json` (structured problem JSON)

**Preconditions:**
- Input file must exist
- Content must be readable

**Postconditions:**
- Output must have: title, statement, input, output, constraints, samples
- All required fields must be non-empty
- No HTML tags in text (except in code blocks)

**Dependencies:**
- Policy: repository_policy.md
- Knowledge: structure definitions

**Self-Validation:**
- All required fields present? ✓
- No HTML pollution? ✓
- Samples count > 0? ✓
- Constraints present? ✓

---

## PHASE 3: TRANSLATE

**Responsibility:** Dịch toàn bộ nội dung sang tiếng Việt

**Skill:** translation-agent

**Input:**
- `cache/normalized/<id>.json`

**Output:**
- JSON with fields: `title`, `translated_title`, `display_title`, `statement`, `input`, `output`, `constraints`, `samples` (with explanations)

**Preconditions:**
- Input file must exist
- Statement must be in English

**Postconditions:**
- All text translated to Vietnamese
- `display_title` format: "Tên Việt (Tên Anh)"
- Math formulas preserved 100%
- No summarization

**Dependencies:**
- Policy: repository_policy.md
- Knowledge: terminology.md
- Skill: sample-explainer

**Self-Validation:**
- display_title format correct? ✓
- Math preserved? ✓
- No info lost? ✓
- Explanation for all samples? ✓

---

## PHASE 4: FORMATTING

**Responsibility:** Chuẩn hóa cấu trúc dữ liệu

**Skill:** formatting-agent

**Input:**
- Translated JSON from Phase 3

**Output:**
- Formatted JSON with clean structure

**Preconditions:**
- Input fields must exist

**Postconditions:**
- I/O format clear and separated
- Samples fully separated
- Explanation preserved for all samples

**Dependencies:**
- Policy: repository_policy.md

**Self-Validation:**
- Samples count unchanged? ✓
- Explanation preserved? ✓
- Structure valid? ✓

---

## PHASE 5: LATEX GENERATION

**Responsibility:** Generate LaTeX mã nguồn

**Skills:**
- latex-agent
- latex-guardian

**Input:**
- Formatted JSON from Phase 4

**Output:**
- `cache/build/<id>.tex` (valid LaTeX code)

**Preconditions:**
- Input JSON valid
- Golden Template accessible

**Postconditions:**
- File valid LaTeX syntax
- No escape errors
- Using display_title correctly
- Order index preserved in comment

**Dependencies:**
- Policy: template_policy.md
- Resource: template.tex

**Self-Validation:**
- LaTeX syntax valid? ✓
- display_title used? ✓
- Escaping correct? ✓
- Order index present? ✓

---

## PHASE 6: SEMANTIC VERIFICATION

**Responsibility:** Verify no information loss

**Skill:** semantic-fidelity-reviewer

**Input:**
- Original problem JSON
- Translated/formatted JSON

**Output:**
- PASS / FAIL verdict

**Preconditions:**
- Both input files exist

**Postconditions:**
- All original information present in translation
- No summarization or compression

**Dependencies:**
- Policy: repository_policy.md

**Self-Validation:**
- Sample count matches? ✓
- Explanation for all samples? ✓
- No info lost? ✓

---

## PHASE 7: QUALITY ASSURANCE

**Responsibility:** Final quality check

**Skill:** qa-agent

**Input:**
- Generated LaTeX from Phase 5
- Formatted JSON from Phase 4

**Output:**
- Quality score (1.0-5.0)
- PASS / FAIL decision

**Preconditions:**
- Input files exist

**Postconditions:**
- All dimensions scored >= 4.0
- No issues found

**Dependencies:**
- Policy: repository_policy.md

**Self-Validation:**
- All scores >= 4.0? ✓
- No policy violations? ✓

---

## PHASE 8: COMBINE & COMPILE

**Responsibility:** Combine LaTeX files and compile to PDF

**Tools:** combine_latex.py, compile_latex.py

**Input:**
- `cache/build/*.tex` (all problem files)

**Output:**
- `outputs/output.pdf`
- `outputs/output.tex`

**Preconditions:**
- All .tex files valid
- pdflatex available

**Postconditions:**
- PDF file exists
- PDF is valid and readable
- Order preserved

**Dependencies:**
- Policy: template_policy.md

**Self-Validation:**
- PDF generated? ✓
- File readable? ✓
- Pages correct? ✓

---

## Phase Execution Rules

1. **Sequential:** Phases phải tuần tự, không được nhảy
2. **Validation:** Mỗi phase kết thúc phải validate output
3. **Rollback:** Nếu phase FAIL, trigger rollback (xem rollback_policy.md)
4. **Logging:** Mỗi phase phải log input/output
5. **Idempotency:** Chạy lại phase phải sinh kết quả giống nhau
