import os
import re
import sys
from pathlib import Path

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

def audit_latex_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        scores = {
            "Statement": 5.0,
            "Explanation": 5.0,
            "Formatting": 5.0,
            "Markdown Conversion": 5.0,
            "Readability": 5.0
        }
        
        failures = []

        # ================= PHASE 9: ANTI REGRESSION =================
        
        # 1. Bullet points joined into paragraph or multiple bullets on the same line
        # Checking for raw bullet markdown on lines that don't start with list markers
        for line_num, line in enumerate(content.split('\n'), 1):
            if re.search(r'\w+.*?\s+[-*•]\s+\w+', line):
                failures.append(f"Line {line_num}: Bullet point joined inline within paragraph: '{line.strip()}'")
            if len(re.findall(r'[-*•]\s+', line)) > 1:
                failures.append(f"Line {line_num}: Multiple bullet points found on the same line: '{line.strip()}'")
                
        # 2. Markdown remaining
        # Check for remaining bold/italic markdown (** or *) that is not escaped or part of LaTeX syntax
        # We allow * for multiplication in formulas (inside $...$), so we only check outside math mode
        text_outside_math = re.sub(r'\$.*?\$', '', content)
        if '**' in text_outside_math:
            failures.append("Remaining bold markdown '**' found outside math mode.")
            scores["Markdown Conversion"] -= 2.0
        if '#' in text_outside_math and not re.search(r'\\#', text_outside_math):
            failures.append("Remaining raw '#' header/symbol found outside math mode.")
            scores["Markdown Conversion"] -= 1.0

        # 3. Enumerate lost (raw 1. / 2. inside text instead of enumerate env)
        if re.search(r'(?:\n|^)\s*\d+\.\s+\w+', content) and '\\begin{enumerate}' not in content:
            failures.append("Raw numbered lists found without using \\begin{enumerate}.")
            scores["Formatting"] -= 1.5

        # 4. Explanation longer than 8 lines but only 1 paragraph
        explanation_blocks = re.findall(r'\\explanation\s*(.*?)(?=\\problem|\\end{document}|$)', content, re.DOTALL)
        for exp in explanation_blocks:
            lines = [l.strip() for l in exp.strip().split('\n') if l.strip()]
            paragraphs = exp.strip().split('\n\n')
            if len(lines) > 8 and len(paragraphs) == 1:
                failures.append("Explanation block is longer than 8 lines but has only 1 paragraph.")
                scores["Explanation"] -= 2.0

        # ================= PHASE 10: QUALITY SCORE =================
        
        # Deduct Formatting if lstlisting is used inside inputbox/outputbox (violating Rule 4)
        if re.search(r'\\begin{(?:input|output)box}\s*\\begin{lstlisting}', content):
            failures.append("Banned environment lstlisting used inside inputbox/outputbox (must use samplecode).")
            scores["Formatting"] -= 2.0
            
        # Deduct Formatting if undefined LaTeX commands are used
        banned_macros = ["\\vspace", "\\\\", "\\noindent", "\\bigskip"]
        for bm in banned_macros:
            if bm in content:
                # We only flag if not inside headers/footers of template
                failures.append(f"Banned manual formatting macro '{bm}' used.")
                scores["Formatting"] -= 1.0

        # Readability check
        # Check if any paragraph outside math/code blocks exceeds 8/12 lines
        paragraphs = content.split('\n\n')
        for p in paragraphs:
            if '\\begin{samplecode}' in p or '\\begin{lstlisting}' in p:
                continue
            lines = [l for l in p.strip().split('\n') if l.strip()]
            if len(lines) > 12:
                scores["Readability"] -= 1.5
                failures.append(f"Paragraph too long (> 12 lines, {len(lines)} lines). Build FAIL.")
            elif len(lines) > 8:
                scores["Readability"] -= 0.5
                failures.append(f"Paragraph slightly long (> 8 lines, {len(lines)} lines). Warning.")

        # Final score calculation
        min_allowed_score = 4.0
        failed_audit = False
        
        print(f"\n--- Quality Audit for {file_path.name} ---")
        for aspect, score in scores.items():
            stars = "★" * int(score) + "☆" * (5 - int(score))
            print(f"{aspect:<20}: {stars} ({score:.1f}/5.0)")
            if score < min_allowed_score:
                failed_audit = True

        if failures:
            print("\nAudit Flags/Violations:", file=sys.stderr)
            for fail_msg in failures:
                print(f"- {fail_msg}", file=sys.stderr)

        if failed_audit:
            print(f"\n[Audit] FAIL: Quality score for {file_path.name} is below threshold ({min_allowed_score}).", file=sys.stderr)
            return False
            
        print(f"[Audit] PASS: {file_path.name} matches quality guidelines.")
        return True
    except Exception as e:
        print(f"[Audit] Exception: {e}", file=sys.stderr)
        return False

def main():
    build_dir = Path(__file__).resolve().parents[1] / "cache" / "build"
    if not build_dir.exists():
        print("[Audit] No build directory found.")
        return
        
    tex_files = list(build_dir.glob("*.tex"))
    success = True
    for tf in tex_files:
        if tf.name != "output.tex":
            if not audit_latex_file(tf):
                success = False
                
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
