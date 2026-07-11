# ROOT CAUSE REPORT — CP Pipeline V3

**Scope**: LaTeX/PDF pipeline root-cause audit.  
**Rule**: `outputs/output.tex` / `outputs/output.pdf` were not patched.  
**Verdict**: ❌ **NOT Release Candidate**.

## Executive Summary

Repeated `fix_output*.py` exists because invalid intermediate artifacts were allowed through multiple layers:

1. Parser fallback used whole `<body>` for unsupported pages.
2. LaTeX agent contract referenced old/nonexistent template macros.
3. Guardian policy allowed regex recovery instead of failing at source layer.
4. Combine layer lacked strict gates for UI chrome/raw formats/title pollution.
5. Compile layer treated "PDF exists" as success even when `pdflatex` returned nonzero.

Correct architecture: fail fast at the layer that produced the defect, then regenerate.

## 1. Template Bugs

### T1 — Missing support packages

Root Cause → `template.tex` lacked theorem/image/TikZ/longtable/float/caption support.  
Affected Layer → Golden template.  
Correct Fix → Added `amsthm`, `caption`, `float`, `graphicx`, `longtable`, `microtype`, `needspace`, `ragged2e`, `tikz`; updated template hash.  
Regression Risk → Medium; covered by `tests/test_template.tex`.

### T2 — Raw Mermaid/SVG boundary undefined

Root Cause → Pipeline did not define whether raw Mermaid/SVG may enter LaTeX.  
Affected Layer → Template + latex-agent + combine.  
Correct Fix → Raw Mermaid/SVG unsupported; upstream must convert to TikZ/image. Combine rejects raw Mermaid/HTML-like markers.  
Regression Risk → Low.

## 2. Generator Bugs

### G1 — LaTeX Agent used obsolete macros

Root Cause → `latex-agent/SKILL.md` referenced `inputbox`, `outputbox`, `constraintbox`, `samplecode`; current template uses `\inputformat`, `\outputformat`, `\constraints ... \endconstraints`, `\example`, `\explanation`.  
Affected Layer → LaTeX generator contract.  
Correct Fix → Updated contract to current macro allowlist and forbid hallucinated legacy macros.  
Regression Risk → High until old cache/build files are regenerated.

### G2 — Invalid `\problem{...}` title arguments

Root Cause → Some fragments put environments/newlines inside `\problem{title}{source}`.  
Affected Layer → latex-agent title generation + combine validation.  
Correct Fix → Combine rejects titles containing LaTeX commands or newlines.  
Regression Risk → Medium; historical fragments fail until regenerated.

## 3. Translator Bugs

No direct translator-specific bug was proven. Observed failures are structural: parser contamination and generator/template contract drift.

## 4. Markdown Bugs

Root Cause → Markdown fences/Mermaid blocks could leak into fragments.  
Affected Layer → latex-guardian + combine.  
Correct Fix → Combine rejects markdown fences, raw Mermaid, raw HTML, raw JSON/YAML-like markers.  
Regression Risk → Low.

## 5. Parser Bugs

### P1 — Unsupported LeetCode fallback poisoned content

Root Cause → `extract_html.py` fell back to whole `<body>` when selectors failed; LeetCode UI chrome survived: `DescriptionDescription`, `EditorialEditorial`, `TopicsCompanies`.  
Affected Layer → Parser/extractor.  
Correct Fix → Fallback body with known UI markers now fails extraction instead of poisoning downstream input.  
Regression Risk → Medium; unsupported sites fail earlier until explicit selectors/support are added.

## 6. Combine Bugs

Root Cause → `combine_latex.py` accepted polluted fragments and invalid titles.  
Affected Layer → Combine.  
Correct Fix → Added gates for raw markdown, Mermaid, HTML, UI pollution, tcolorbox option leaks, JSON/YAML-like leaks, invalid `\problem` titles.  
Regression Risk → Medium; old cache fails sooner.

## 7. Compile Bugs

Root Cause → `compile_latex.py` reported success if PDF existed, ignoring nonzero `pdflatex` return code.  
Affected Layer → Compile.  
Correct Fix → Success now requires pass1 rc=0, pass2 rc=0, and PDF exists.  
Regression Risk → Low; false success removed.

## 8. PDF Rendering Bugs

Current `outputs/output.pdf` text audit found:

| Marker | Found |
|---|---:|
| `[backgroundcolor=...]` | No |
| `DescriptionDescription` | Yes |
| `TopicsCompanies` | Yes |
| raw HTML `<div` | No |
| raw markdown fence | No |
| raw `\problem` macro | No |

Root Cause → PDF was generated from polluted cache/build content before parser/combine gates.  
Correct Fix → Do not patch PDF. Regenerate after bad cache entries are regenerated from corrected upstream layers.

## 9. Bugs Fixed

| Layer | File | Fix |
|---|---|---|
| Template | `.agents/templates/template.tex` | Added required packages + theorem support |
| Template hash | `.agents/metadata/template_hash.txt` | Updated hash |
| Parser | `tools/extract_html.py` | Reject fallback UI-chrome body |
| LaTeX Agent | `.agents/skills/latex-agent/SKILL.md` | Align macro contract |
| Guardian | `.agents/skills/latex-guardian/SKILL.md` | Remove regex patch policy |
| Combine | `tools/combine_latex.py` | Add raw/pollution/title validation |
| Compile | `tools/compile_latex.py` | Require pdflatex rc=0 |
| Test | `tests/test_template.tex` | Add template stress test |

## 10. Remaining Issues

| Priority | Issue | Required Fix |
|---|---|---|
| 🔴 High | `cache/build/` contains invalid historical fragments | Regenerate cache/build |
| 🔴 High | Current PDF contains LeetCode UI pollution | Regenerate after cache cleanup |
| 🔴 High | 17/35 standalone build fragments fail | Root-cause each or discard/regenerate |
| 🟡 Medium | Raw SVG/Mermaid unsupported | Add upstream converter if required |
| 🟡 Medium | Old fragments may use obsolete macro contracts | Regenerate after updated latex-agent contract |

## 11. Regression Risk

| Area | Risk | Mitigation |
|---|---|---|
| Parser support | Unsupported pages fail earlier | Add site-specific extractor support |
| Build cache | Historical bad files fail validation | Clean/regenerate cache/build |
| Compile | More builds fail due nonzero pdflatex | Desired; prevents false release |
| Template packages | Slightly larger dependency surface | Covered by stress test |
| Combine gates | Possible false positives | Tune with real examples |

## 12. Verification Results

- `tests/test_template.tex`: pdflatex pass1/pass2 PASS.
- `tools/combine_latex.py`: correctly FAILS on `830f3dfa.tex` with `DescriptionDescription`.
- `extract_html.py`: test rejects fallback body with UI chrome.
- Current PDF text audit: FAIL due `DescriptionDescription`, `TopicsCompanies`.
- Build directory test: 35 files checked, 17 standalone failures.
- Combine scale test on current cache: 2/5/20 combine pass but compile fail; 100 combine fail due validation gate.

## 13. Architecture Improvement Proposal

Pipeline should be:

```text
crawl → extract → normalize → translate → format → latex fragment
  ↓
validate fragment independently
  ↓
combine
  ↓
compile with rc==0
  ↓
pdf text audit
  ↓
archive
```

Rules:
- Never repair generated `outputs/output.tex`.
- Every `fix_output*.py` need is architecture failure.
- Store root-cause classification before regeneration.

## Final Verdict

❌ **Repository is NOT Release Candidate.**

No unresolved root-cause class remains for the observed `fix_output*.py` pattern: it was caused by parser fallback contamination + generator/template contract drift + weak combine/compile gates.
