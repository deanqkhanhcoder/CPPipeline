import os
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    output_tex = ROOT / "outputs" / "output.tex"
    output_toc = ROOT / "cache" / "debug" / "output.toc"
    
    if not output_tex.exists():
        print("PASS: outputs/output.tex does not exist yet. Skip TOC validation.")
        return 0
        
    content = output_tex.read_text(encoding="utf-8", errors="replace")
    problem_count = len(re.findall(r"\\problem\s*\{", content))
    
    if not output_toc.exists():
        if problem_count > 0:
            print(f"FAIL: output.toc is missing but problem_count = {problem_count}.")
            return 1
        print("PASS: Both output.toc missing and problem_count is 0.")
        return 0
        
    toc_content = output_toc.read_text(encoding="utf-8", errors="replace")
    toc_count = len(re.findall(r"\\contentsline\s*\{", toc_content))
    
    print(f"Validation: problem_count = {problem_count}, toc_count = {toc_count}")
    
    if problem_count != toc_count:
        print("FAIL: TOC count does not match problem count.")
        return 1
        
    if problem_count > 0 and toc_count == 0:
        print("FAIL: Pipeline guardrail triggered. toc_count == 0 and problem_count > 0.")
        return 1
        
    print("PASS: TOC is perfectly aligned with problems.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
