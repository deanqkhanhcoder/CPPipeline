# Root Cause Database

## DescriptionDescription / TopicsCompanies
Layer: PARSER
Symptom: Online judge UI chrome leaks into statement/PDF.
Do not fix in: output.tex, output.pdf, combine, compile.
Fix in: extractor/parser selector support, fail-fast fallback rejection.
Verification: parser output and fragment QA contain no UI marker.
Regression risk: unsupported sites fail earlier.

## Raw Markdown fence
Layer: FORMATTER
Symptom: ``` or ```mermaid appears in fragment/PDF.
Do not fix in: output.tex, PDF, compile.
Fix in: formatter or upstream Mermaid converter.
Verification: fragment QA/PDF QA reject raw fence.
Regression risk: low.

## Raw HTML tag
Layer: PARSER
Symptom: <div, <span, closing HTML tags leak downstream.
Do not fix in: latex-agent, combine, output.tex.
Fix in: extract_html.py or cp-parser.
Verification: parser output + fragment QA.
Regression risk: medium for new OJ layouts.

## Raw Mermaid/SVG
Layer: FORMATTER
Symptom: Mermaid/SVG source appears in LaTeX/PDF.
Do not fix in: compile/PDF.
Fix in: upstream converter to TikZ/image or reject unsupported graph.
Verification: fragment QA/PDF QA reject raw graph source.
Regression risk: medium until converter exists.

## Undefined control sequence
Layer: LATEX
Symptom: pdflatex reports undefined macro.
Do not fix in: PDF/output patch scripts.
Fix in: latex-agent macro allowlist or golden template if macro is intentional.
Verification: fragment QA + compile rc=0.
Regression risk: high when skill contract drifts.

## Invalid problem title
Layer: LATEX
Symptom: \problem title contains command/newline/environment.
Do not fix in: combine/output.tex.
Fix in: latex-agent title generation from display_title.
Verification: fragment QA rejects invalid title.
Regression risk: medium.

## Obsolete macros
Layer: LATEX
Symptom: inputbox/outputbox/constraintbox/samplebox/etc. appear.
Do not fix in: combine/output.tex.
Fix in: latex-agent and latex-guardian contracts.
Verification: fragment QA rejects obsolete macros.
Regression risk: medium until old cache regenerated.

## False compile success
Layer: COMPILE
Symptom: stale/partial PDF exists while pdflatex failed.
Do not fix in: archive or Host report.
Fix in: compile_latex.py rc/status checks.
Verification: compile test with broken TeX must not archive.
Regression risk: low.

## Missing sample/explanation
Layer: FORMATTER
Symptom: sample or explanation absent in fragment/PDF.
Do not fix in: PDF QA or output patch.
Fix in: sample-explainer/formatting-agent.
Verification: fragment QA and semantic QA.
Regression risk: medium.

## TOC/title mismatch
Layer: LATEX
Symptom: title/TOC/bookmark not using display_title.
Do not fix in: PDF.
Fix in: translation-agent display_title then latex-agent propagation.
Verification: order guardian + PDF QA spot checks.
Regression risk: medium.

## Asymptotic Notation Alteration
Layer: TRANSLATOR
Symptom: Big-O or asymptotic notations like O(N log N) or \Theta(V+E) lose math formatting or get mistranslated during English-to-Vietnamese conversion.
Do not fix in: output.tex, output.pdf, combine_latex.py, regex replace scripts.
Fix in: translation-agent (enforce strict preservation of mathematical environments and asymptotic symbols).
Verification: semantic-fidelity-reviewer confirms 100% math and asymptotic notation fidelity.
Regression risk: None (improves mathematical accuracy).
