import argparse
import subprocess
import os
import sys
import shutil
import json

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stdin.encoding.lower() != 'utf-8':
    sys.stdin.reconfigure(encoding='utf-8')

import re
import hashlib
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = ROOT / ".agents" / "skills" / "cp-latex" / "template.tex"
HASH_PATH = ROOT / ".agents" / "metadata" / "template_hash.txt"


def verify_template_hash() -> None:
    expected = HASH_PATH.read_text(encoding="utf-8").strip().split()[0]
    actual = hashlib.sha256(TEMPLATE_PATH.read_bytes()).hexdigest()
    if actual != expected:
        raise SystemExit(f"FAIL: template hash mismatch: {actual} != {expected}")


def parse_tex_metadata(tex_file):
    try:
        with open(tex_file, 'r', encoding='utf-8') as f:
            content = f.read()
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
    verify_template_hash()
    print(f"Compiling {tex_file}...")
    engine = "pdflatex"
    cwd = os.path.dirname(tex_file) or "."
    basename = os.path.basename(tex_file)
    cmd_with_base = [engine, "-interaction=nonstopmode", basename]
    pdf_basename = basename.replace(".tex", ".pdf")
    pdf_path = os.path.join(cwd, pdf_basename)
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    try:
        res = subprocess.run(cmd_with_base, cwd=cwd, capture_output=True, timeout=60, encoding='utf-8', errors='strict')
        if res.returncode == 0:
            # Pass 2
            res2 = subprocess.run(cmd_with_base, cwd=cwd, capture_output=True, timeout=60, encoding='utf-8', errors='strict')
            if res2.returncode == 0:
                print(f"Compilation successful using {engine}.")
                archive_files(tex_file, pdf_path, hits, misses)
                return
            print(f"{engine} (pass 2) failed with return code {res2.returncode}.")
            res = res2
        else:
            print(f"{engine} failed with return code {res.returncode}.")
        stdout = res.stdout or ''
        stderr = res.stderr or ''
        log_dir = os.path.join(ROOT, "cache", "debug")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "compile_error.log")
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(stdout + "\n" + stderr)
        print(f"Check {log_path} for details.")
    except Exception as e:
        print(f"{engine} execution failed: {e}")
    finally:
        base_no_ext = os.path.splitext(tex_file)[0]
        build_dir = os.path.join(ROOT, "cache", "build")
        os.makedirs(build_dir, exist_ok=True)
        for ext in [".aux", ".out", ".toc", ".log", ".synctex.gz"]:
            for candidate in [base_no_ext + ext, os.path.join(cwd, os.path.splitext(basename)[0] + ext)]:
                if os.path.exists(candidate):
                    try:
                        target = os.path.join(build_dir, os.path.basename(candidate))
                        if os.path.exists(target):
                            os.remove(target)
                        shutil.move(candidate, target)
                    except Exception as e:
                        print(f"Warning: could not move {candidate}: {e}")
                    break
    print("Compilation failed.")
    sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("tex_file", help="Path to .tex file")
    parser.add_argument("--hits", type=int, default=0, help="Number of cache hits")
    parser.add_argument("--misses", type=int, default=0, help="Number of cache misses")
    args = parser.parse_args()
    compile_latex(args.tex_file, args.hits, args.misses)
