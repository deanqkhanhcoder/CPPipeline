---
name: cp-pipeline
description: End-to-end Competitive Programming Translation Pipeline. Use when the user provides one or more Competitive Programming problem URLs and wants a complete Vietnamese translation, explanation generation, LaTeX document generation, and PDF compilation.
---

# CP Pipeline

When invoked with:

/cp-pipeline <url>

Execute the following chain strictly:

1. Run cp-crawler
   * Fetch statement
   * Extract title
   * Extract limits
   * Extract samples

2. Run cp-parser
   * Normalize structure
   * Validate fields

3. Run cp-translator
   * Translate statement to Vietnamese
   * Preserve math notation
   * Preserve examples

4. Run cp-latex
   * Render template.tex
   * Generate output.tex

5. Compile
   * pdflatex output.tex (hoặc latexmk -pdf)

6. Save outputs
   * outputs/output.tex
   * outputs/output.pdf

Return:
* PDF path
* Summary
* Errors if any

Do not stop between phases.
Continue automatically until PDF is generated or a fatal error occurs.
