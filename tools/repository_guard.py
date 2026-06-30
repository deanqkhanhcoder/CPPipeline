from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_ROOT_FILES = {".gitignore", "README.md", "LICENSE", "requirements.txt", "build.py"}
ALLOWED_ROOT_DIRS = {".agents", "archive", "cache", "outputs", "reports", "tools", "tests", ".git"}
FORBIDDEN_EXT = {".txt", ".html", ".md", ".log", ".aux", ".out", ".toc", ".tmp"}


def main() -> int:
    violations: list[str] = []
    for path in ROOT.iterdir():
        if path.name in ALLOWED_ROOT_FILES or path.name in ALLOWED_ROOT_DIRS:
            continue
        if path.is_dir():
            violations.append(f"root unexpected directory: {path.name}")
        elif path.suffix.lower() in FORBIDDEN_EXT:
            violations.append(f"root forbidden file: {path.name}")
        elif path.is_file():
            violations.append(f"root unexpected file: {path.name}")
    if violations:
        print("\n".join(violations))
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
