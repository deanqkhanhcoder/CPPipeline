import argparse
import subprocess
import os
import sys
import shutil
import json
import re
from datetime import datetime

def parse_tex_metadata(tex_file):
    try:
        with open(tex_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Count number of problems
            problems = re.findall(r'\\problem\{.*?\}\{(.*?)\}', content)
            sources = list(set([p.split()[0] for p in problems if p])) if problems else []
            return len(problems), sources
    except Exception:
        return 0, []

def archive_files(tex_file, pdf_file, hits=0, misses=0):
    archive_dir = "archive"
    date_str = datetime.now().strftime("%Y-%m-%d")
    target_dir = os.path.join(archive_dir, date_str)
    os.makedirs(target_dir, exist_ok=True)
    
    existing_pdfs = [f for f in os.listdir(target_dir) if f.startswith("output_") and f.endswith(".pdf")]
    seq_num = len(existing_pdfs) + 1
    
    new_tex_name = f"output_{seq_num:03d}.tex"
    new_pdf_name = f"output_{seq_num:03d}.pdf"
    
    target_tex = os.path.join(target_dir, new_tex_name)
    target_pdf = os.path.join(target_dir, new_pdf_name)
    
    shutil.copy2(tex_file, target_tex)
    shutil.copy2(pdf_file, target_pdf)
    
    index_file = os.path.join(archive_dir, "index.json")
    if os.path.exists(index_file):
        with open(index_file, "r", encoding="utf-8") as f:
            try:
                index_data = json.load(f)
            except json.JSONDecodeError:
                index_data = []
    else:
        index_data = []
        
    prob_count, sources = parse_tex_metadata(tex_file)
    
    metadata = {
        "timestamp": datetime.now().isoformat(),
        "problem_count": prob_count,
        "sources": sources,
        "cache_hits": hits,
        "cache_misses": misses,
        "pdf_file": f"{date_str}/{new_pdf_name}",
        "tex_file": f"{date_str}/{new_tex_name}"
    }
    index_data.append(metadata)
    
    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)
        
    print(f"Archived to {target_pdf}")

def compile_latex(tex_file: str, hits=0, misses=0):
    print(f"Compiling {tex_file}...")
    pdf_name = tex_file.replace(".tex", ".pdf")
    
    engine = "pdflatex"
    cmd = [engine, "-interaction=nonstopmode", tex_file]
    print(f"Trying engine: {' '.join(cmd)}")
    try:
        cwd = os.path.dirname(tex_file) or "."
        basename = os.path.basename(tex_file)
        cmd_with_base = [engine, "-interaction=nonstopmode", basename]
        
        pdf_basename = basename.replace(".tex", ".pdf")
        pdf_path = os.path.join(cwd, pdf_basename)
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
            
        res = subprocess.run(cmd_with_base, cwd=cwd, capture_output=True, text=True, timeout=60)
        
        if res.returncode == 0 and os.path.exists(pdf_path):
            # Run second time for TOC
            print(f"Running {engine} a second time for Table of Contents...")
            res2 = subprocess.run(cmd_with_base, cwd=cwd, capture_output=True, text=True, timeout=60)
            if res2.returncode == 0:
                print(f"Compilation successful using {engine}.")
                archive_files(tex_file, pdf_path, hits, misses)
                return
            else:
                print(f"{engine} (pass 2) failed with return code {res2.returncode}.")
                res = res2 # pass error to logging
        else:
            print(f"{engine} failed with return code {res.returncode}.")
            
        with open("compile_error.log", "w", encoding="utf-8") as f:
            f.write(res.stdout + "\n" + res.stderr)
        print("Check compile_error.log for details.")
    except Exception as e:
        print(f"{engine} execution failed: {e}")
            
    print("Compilation failed.")
    sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("tex_file", help="Path to .tex file")
    parser.add_argument("--hits", type=int, default=0, help="Number of cache hits")
    parser.add_argument("--misses", type=int, default=0, help="Number of cache misses")
    args = parser.parse_args()
    compile_latex(args.tex_file, args.hits, args.misses)
