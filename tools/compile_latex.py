import argparse
import subprocess
import os
import sys

def compile_latex(tex_file: str):
    print(f"Compiling {tex_file}...")
    pdf_name = tex_file.replace(".tex", ".pdf")
    
    engine = "latexmk -pdf"
    cmd = engine.split() + ["-interaction=nonstopmode", tex_file]
    print(f"Trying engine: {' '.join(cmd)}")
    try:
        cwd = os.path.dirname(tex_file) or "."
        basename = os.path.basename(tex_file)
        cmd_with_base = engine.split() + ["-interaction=nonstopmode", basename]
        res = subprocess.run(cmd_with_base, cwd=cwd, capture_output=True, text=True, timeout=60)
        
        pdf_basename = basename.replace(".tex", ".pdf")
        if os.path.exists(os.path.join(cwd, pdf_basename)):
            print(f"Compilation successful using {engine}.")
            return
        else:
            print(f"{engine} failed with return code {res.returncode}.")
    except Exception as e:
        print(f"{engine} execution failed: {e}")
            
    print("Compilation failed.")
    sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("tex_file", help="Path to .tex file")
    args = parser.parse_args()
    compile_latex(args.tex_file)
