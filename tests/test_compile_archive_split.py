import subprocess
import sys
from pathlib import Path

def test_compile_error_does_not_archive():
    import tempfile
    tmp_path = Path(tempfile.mkdtemp())
    before = set(Path("archive").rglob("output_*.pdf")) if Path("archive").exists() else set()
    bad = tmp_path / "bad.tex"
    bad.write_text(r"\documentclass{article}\begin{document}\undefinedmacro\end{document}", encoding="utf-8")
    res = subprocess.run([sys.executable, "tools/compile_latex.py", str(bad)], capture_output=True, text=True)
    after = set(Path("archive").rglob("output_*.pdf")) if Path("archive").exists() else set()
    assert res.returncode != 0
    assert before == after

if __name__ == "__main__":
    test_compile_error_does_not_archive()
    print("PASS")
