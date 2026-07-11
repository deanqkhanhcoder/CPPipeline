# B?o c?o Hardening Ki?n tr?c CP Pipeline V3.1

**M?c ti?u**: Lo?i b? tri?t ?? nguy?n nh?n ki?n tr?c sinh ra c?c script v? l?i ki?u `fix_output*.py`.
**Nguy?n t?c**: Kh?ng patch `outputs/output.tex`, kh?ng patch `outputs/output.pdf`, kh?ng s?a tri?u ch?ng ? t?ng h? ngu?n.

## I. Bug & Root Cause Map

```text
Crawler -> Parser -> Normalizer -> Translator -> Formatter -> LaTeX Agent -> Fragment QA -> Combine -> Compile -> PDF QA -> Archive
```

| T?n Bug | T?ng sinh l?i (Layer) | Tri?u ch?ng | Kh?ng ???c v? ? ??u | ???c s?a ? ??u |
|---|---|---|---|---|
| `DescriptionDescription` / `TopicsCompanies` | PARSER | UI chrome c?a trang OJ l?t v?o n?i dung ?? b?i v? PDF. | `outputs/output.tex`, `outputs/output.pdf`, `combine_latex.py` | `extract_html.py`, `cp-parser` (t? ch?i fallback body ch?a marker UI). |
| Raw Markdown fence (```` ``` ````, ```` ```mermaid ````) | FORMATTER | Kh?i code markdown ho?c diagram th? xu?t hi?n tr?n t?i li?u LaTeX/PDF. | `compile_latex.py`, PDF | `formatting-agent`, converter diagram th??ng ngu?n. |
| Raw HTML tag (`<div`, `<span`, `</`) | PARSER | Th? HTML th? s?t l?i sau b??c parse. | `combine_latex.py`, `output.tex` | `extract_html.py`, `cp-parser`. |
| Undefined control sequence | LATEX | L?i compile do macro l? ho?c macro kh?ng c? trong template. | Script v? regex, PDF | `latex-agent` (ch? d?ng macro trong allowlist), `template.tex`. |
| Invalid problem title | LATEX | T?n b?i trong problem ch?a xu?ng d?ng ho?c l?nh LaTeX. | `combine_latex.py` | `latex-agent` (s? d?ng chu?n `display_title`). |
| Obsolete macros | LATEX | Subagent d?ng l?nh c?: `inputbox`, `outputbox`, `constraintbox`, v.v. | Script v? l?i sau compile | `latex-agent`, `latex-guardian`. |
| False compile success | COMPILE | `compile_latex.py` b?o th?nh c?ng ch? v? file PDF c? c?n t?n t?i d? `pdflatex` tr? v? m? l?i. | Host LLM report | `compile_latex.py` (b?t bu?c `returncode == 0` cho c? 2 pass). |

## II. Ph?n t?ch tr?ch nhi?m (Separation of Concerns)

- **`combine_latex.py`**: Ch? ??c fragment t? `cache/build/`, g?i `fragment_qa.py` ?? ki?m duy?t, s?p x?p theo `order_index`, gh?p v?o template v? ghi ra `outputs/output.tex`. B? ho?n to?n c?c ?o?n code regex repair, d?n d?p markdown hay s?a latex th?.
- **`compile_latex.py`**: Ch? ch?y `pdflatex` 2 pass, qu?n l? compile log (`cache/debug/compile_error.log`), ghi status code v? tr? v? non-zero n?u fail. B? ho?n to?n vi?c archive file hay parse metadata ra kh?i tool n?y.
- **`archive_output.py`** [NEW]: Tool chuy?n bi?t ch? ch?y khi t?i li?u ?? v??t qua PDF QA; ch?u tr?ch nhi?m copy sang `archive/` v? ghi metadata v?o `index.json`.
- **`fragment_qa.py`** [NEW]: Gate ki?m duy?t ??c l?p t?ng file fragment `.tex` tr??c khi combine.
- **`pdf_qa.py`** [NEW]: Gate ki?m duy?t text c?a file `.pdf` th?nh ph?m v? log compile tr??c khi archive.

## III. C?c c?ng ki?m duy?t m?i (Quality Gates)

### 1. Fragment QA (`fragment-qa`)
- **V? tr?**: ??ng sau `latex-agent` / `latex-guardian` v? tr??c `combine_latex.py`.
- **Lu?t**: Ki?m tra c? ph?p c? b?n, macro b?t bu?c (`\problem`, `\inputformat`, `\outputformat`, `\example`, `\explanation`), c?m macro l?i th?i, c?m th? HTML/Markdown/Mermaid th?, c?m UI chrome.
- **X? l? khi FAIL**: T? ch?i fragment, x?c ??nh t?ng g?y l?i (Parser, Formatter hay LaTeX) v? bu?c Host LLM t?i t?o l?i t? ??ng t?ng ??. Kh?ng bao gi? combine fragment l?i.

### 2. PDF QA (`pdf_qa.py`)
- **V? tr?**: ??ng sau `compile_latex.py` v? tr??c `archive_output.py`.
- **Lu?t**: Qu?t text c?a PDF (qua `pdftotext`) v? compile log ?? ??m b?o kh?ng s?t markdown fence, HTML, UI chrome, kh?ng c? l?i `Undefined control sequence`, v? s? l??ng `Overfull \hbox` kh?ng v??t ng??ng (< 20).
- **X? l? khi FAIL**: Ch?n archive, y?u c?u s?a t? source-of-truth th??ng ngu?n.

## IV. Error Taxonomy & Root Cause Database

- ?? chu?n h?a ph?n lo?i l?i trong `.agents/policies/error_taxonomy.md` v?i 9 l?p duy nh?t:
  `PARSER`, `NORMALIZER`, `TRANSLATOR`, `FORMATTER`, `LATEX`, `COMBINE`, `COMPILE`, `PDF`, `RUNTIME`.
- C?m ho?n to?n vi?c s? d?ng `Unknown`, `Misc`, `Other`.
- Th?m c? s? d? li?u nguy?n nh?n g?c t?i `.agents/knowledge/root_causes.md`.

## V. C?p nh?t Skill & Policy

- ?? th?m lu?t **V3.1 Root-Cause Hardening** v?o to?n b? c?c skill c?t l?i (`cp-pipeline`, `cp-parser`, `translation-agent`, `formatting-agent`, `latex-agent`, `latex-guardian`, `qa-agent`, `sample-explainer`, `semantic-fidelity-reviewer`, `editorial-agent`, `terminology-agent`).
- C?p nh?t `runtime.md`, `phase_definition.md`, `verification_policy.md`, `rollback_policy.md`, `repository_policy.md`, `template_policy.md` ?? ??ng b? workflow 12 phase m?i.

## VI. K?t qu? Test Suite (Verification & Regression)

?? t?o v? ch?y b? test t? ??ng x?c minh ki?n tr?c m?i:

1. **`test_fragment_qa.py`** -> PASS: Ki?m ch?ng Fragment QA block ch?nh x?c c?c fragment ch?a UI chrome (`DescriptionDescription`), th? HTML, Markdown fence, v? macro c? (`\begin{inputbox}`).
2. **`test_pdf_qa.py`** -> PASS: Ki?m ch?ng PDF QA ph?t hi?n ch?nh x?c c?c marker r?c v? l?i log compilation.
3. **`test_compile_archive_split.py`** -> PASS: Ki?m ch?ng khi compile th?t b?i (nh?n TeX l?i), h? th?ng tr? v? m? l?i v? tuy?t ??i kh?ng t?o hay ghi ?? file trong th? m?c `archive/`.
4. **`test_pipeline_gates.py`** -> PASS: Ki?m ch?ng kh? n?ng scale khi validate 100 fragment chu?n ng?u nhi?n trong pipeline.
5. **Syntax Check** -> PASS: T?t c? c?c c?ng c? `fragment_qa.py`, `pdf_qa.py`, `archive_output.py`, `combine_latex.py`, `compile_latex.py` ??u pass `py_compile`.

*L?u ? r?i ro h?i quy (Regression Risk)*:
- C?c fragment c? trong `cache/build/` sinh ra t? c?c version tr??c n?u ch?a ???c regenerate s? b? Fragment QA t? ch?i do ch?a macro c? ho?c UI chrome. ??y l? h?nh vi ??ng theo thi?t k? (fail-fast) ?? ng?n t?i li?u b?n l?t v?o b?n in.
- Ki?m to?n repository (`run_repository_audit.py`) cho th?y m?i tr??ng hi?n t?i c? drift v? ng?n ng? (c?c ti?u ?? ti?ng Anh trong file docs h? th?ng) v? l?ch s? l??ng TOC/URL do cache l?ch s? ch?a ???c clean tay, ??ng v?i khuy?n c?o c?n regenerate tr?n v?n cache khi th?c hi?n release ch?nh th?c.

## VII. Ki?n tr?c m?i & Nh?ng ?i?m c?n c?n c?i thi?n

### S? ?? lu?ng th?c thi V3.1:
```text
[Crawl] -> [Parse/Extract] -> [Translate] -> [Format] -> [LaTeX Agent]
                                                                |
                                                          (Fragment QA) --[FAIL]--> Reject & Regenerate from Source
                                                                |
                                                             [PASS]
                                                                v
                                                            [Combine]
                                                                v
                                                            [Compile] (pdflatex rc == 0)
                                                                |
                                                             (PDF QA) ----[FAIL]--> Reject & Regenerate from Source
                                                                |
                                                             [PASS]
                                                                v
                                                            [Archive]
```

### ?i?m c?n c?i thi?n ti?p theo:
1. **Upstream Diagram Converter**: X?y d?ng m?t module pre-processor chuy?n bi?t ?? t? ??ng chuy?n ??i m? Mermaid/SVG th? sang TikZ ho?c ?nh bitmap tr??c khi truy?n v?o t?ng `formatting-agent`.
2. **Site-specific Extractors**: M? r?ng c?c rule b?c t?ch ri?ng cho T-V/LeetCode/AtCoder trong `extract_html.py` ?? kh?ng ph?i d?a v?o fallback body, tri?t ti?u r?i ro r? r? UI chrome t? g?c.
3. **Cache Invalidation Automation**: Th?m c? ch? t? ??ng ??nh d?u stale/invalid cho to?n b? `cache/build/` m?i khi `template_hash.txt` ho?c macro contract c? s? thay ??i.
