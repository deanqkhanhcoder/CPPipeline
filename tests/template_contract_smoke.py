from pathlib import Path
import hashlib
import importlib.util
import shutil

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / ".agents" / "skills" / "cp-latex" / "template.tex"
HASH = ROOT / ".agents" / "metadata" / "template_hash.txt"
COMBINE = ROOT / "tools" / "combine_latex.py"


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def write_case(count: int):
    build = ROOT / "cache" / "build"
    if build.exists():
        shutil.rmtree(build)
    build.mkdir(parents=True, exist_ok=True)
    for i in range(count):
        (build / f"case_{i:03d}.tex").write_text(
            f"\problem{{P{i}}}{{Codeforces}}\inputformat x\outputformat y\constraints z\endconstraints\example e\explanation t",
            encoding="utf-8",
        )


def main():
    expected = HASH.read_text(encoding="utf-8").strip().split()[0]
    actual = hashlib.sha256(TEMPLATE.read_bytes()).hexdigest()
    assert actual == expected
    mod = load_module(COMBINE)
    for count in (1, 10, 100):
        write_case(count)
        mod.main()
        out = (ROOT / "outputs" / "output.tex").read_text(encoding="utf-8")
        template = TEMPLATE.read_text(encoding="utf-8")
        assert "% CONTENT_START" in template and "% CONTENT_END" in template and "[[PROBLEM_COUNT]] Bài toán" in template
        assert "% CONTENT_START" in out and "% CONTENT_END" in out
        assert out.count("\problem{") == count
        assert f"{count} Bài toán" in out
        assert "[[PROBLEM_COUNT]]" not in out
        assert "... Bài toán" not in out
        assert "\documentclass" not in out.split("% CONTENT_START", 1)[1]
    print("ok")


if __name__ == "__main__":
    main()
