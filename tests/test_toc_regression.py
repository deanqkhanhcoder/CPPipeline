import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    print("Running TOC Regression Test...")
    
    template_path = ROOT / ".agents" / "templates" / "template.tex"
    output_dir = ROOT / "outputs"
    output_dir.mkdir(exist_ok=True)
    output_tex = output_dir / "output.tex"
    
    # 1. Read template
    template_content = template_path.read_text(encoding="utf-8")
    
    # 2. Insert exactly 3 problems
    problems = """
\\problem{Test Problem 1}{Source 1}
This is problem 1.
\\problem{Test Problem 2}{Source 2}
This is problem 2.
\\problem{Test Problem 3}{Source 3}
This is problem 3.
"""
    
    # Replace the content block
    content = template_content.replace("% CONTENT_START\n% CONTENT_END", f"% CONTENT_START\n{problems}\n% CONTENT_END")
    content = content.replace("[[PROBLEM_COUNT]]", "3")
    
    # 3. Write to outputs/output.tex
    output_tex.write_text(content, encoding="utf-8")
    
    # 4. Compile LaTeX
    print("Compiling LaTeX...")
    res = subprocess.run([sys.executable, "tools/compile_latex.py", "outputs/output.tex"], cwd=str(ROOT), capture_output=True, text=True)
    
    if res.returncode != 0:
        print("FAIL: Compilation failed!")
        print(res.stdout)
        print(res.stderr)
        return 1
        
    print("Compilation passed. Running validate_toc.py...")
    
    # 5. Run validate_toc.py
    res2 = subprocess.run([sys.executable, "tools/validate_toc.py"], cwd=str(ROOT), capture_output=True, text=True)
    
    if res2.returncode != 0:
        print("FAIL: TOC Validation failed!")
        print(res2.stdout)
        return 1
        
    if "problem_count = 3, toc_count = 3" not in res2.stdout:
        print("FAIL: TOC count was not exactly 3 as expected.")
        print(res2.stdout)
        return 1
        
    print("PASS: Regression test successful. TOC contains exactly 3 entries matching 3 problems.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
