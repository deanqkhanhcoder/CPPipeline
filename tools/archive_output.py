"""Archive passed CP Pipeline outputs. Archive-only."""
from __future__ import annotations
import argparse, json, re, shutil
from datetime import datetime
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def parse_tex_metadata(tex_file: Path) -> tuple[int, list[str]]:
    content = tex_file.read_text(encoding="utf-8", errors="replace")
    problems = re.findall(r"\\problem\{.*?\}\{(.*?)\}", content)
    return len(problems), sorted({p.split()[0] for p in problems if p.split()})

def archive(tex_file: Path, pdf_file: Path, hits: int = 0, misses: int = 0) -> Path:
    if not tex_file.exists() or not pdf_file.exists():
        raise SystemExit("RUNTIME: cannot archive missing tex/pdf")
    archive_dir = ROOT / "archive"
    date_str = datetime.now().strftime("%Y-%m-%d")
    target_dir = archive_dir / date_str
    target_dir.mkdir(parents=True, exist_ok=True)
    seq_num = len(list(target_dir.glob("output_*.pdf"))) + 1
    target_tex = target_dir / f"output_{seq_num:03d}.tex"
    target_pdf = target_dir / f"output_{seq_num:03d}.pdf"
    shutil.copy2(tex_file, target_tex); shutil.copy2(pdf_file, target_pdf)
    index_file = archive_dir / "index.json"
    if index_file.exists():
        try: index_data = json.loads(index_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError: index_data = []
    else: index_data = []
    prob_count, sources = parse_tex_metadata(tex_file)
    index_data.append({"timestamp": datetime.now().isoformat(), "problem_count": prob_count, "sources": sources, "cache_hits": hits, "cache_misses": misses, "pdf_file": f"{date_str}/{target_pdf.name}", "tex_file": f"{date_str}/{target_tex.name}"})
    index_file.write_text(json.dumps(index_data, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    return target_pdf

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Archive output.tex/output.pdf after QA PASS.")
    parser.add_argument("tex", nargs="?", default="outputs/output.tex")
    parser.add_argument("pdf", nargs="?", default="outputs/output.pdf")
    parser.add_argument("--hits", type=int, default=0); parser.add_argument("--misses", type=int, default=0)
    args = parser.parse_args(argv)
    print(f"Archived to {archive(Path(args.tex), Path(args.pdf), args.hits, args.misses)}")
    return 0
if __name__ == "__main__": raise SystemExit(main())
