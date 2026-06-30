from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_FILES = [*ROOT.glob("README.md"), *ROOT.glob("reports/**/*.md"), *ROOT.glob(".agents/**/*.md")]
EN_DRIFT = re.compile(
    r"\b(Final Report|Known Failure Modes|Lessons Learned|Anti Regression Rules|Quick Start|Architecture|Workflow|Directory Structure|One Command Workflow|Session Workflow|Crawler Diagnostics|Troubleshooting|problem statement|sample input|sample output|Crawler Queue|Queue Manager)\b"
)
MIXED_SENTENCE = re.compile(r"[À-ỹ].*\b(If|Then|Else|Known Failure Modes|Lessons Learned|Final Report)\b|\b(If|Then|Else)\b.*[À-ỹ]")
FORBIDDEN = ["Bắt đầu crawl problem statement", "If Cloudflare detected", "... Bài toán"]
EXEMPT_DIRS = ("/caveman", "/pdfmaker", "/cavecrew")


def is_exempt(path: Path) -> bool:
    text = str(path).replace("\\", "/")
    return any(part in text for part in EXEMPT_DIRS) or path.name in {"documentation_audit.md", "terminology.md"}


def strip_code(line: str) -> str:
    return re.sub(r"`[^`]*`", "", line)


def audit_file(path: Path) -> list[str]:
    if is_exempt(path):
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    violations: list[str] = []
    in_fence = False
    for idx, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or line.strip().startswith("---"):
            continue
        plain = strip_code(line)
        if EN_DRIFT.search(plain):
            violations.append(f"{path}:{idx}: English heading/term drift")
        if MIXED_SENTENCE.search(plain):
            violations.append(f"{path}:{idx}: mixed language sentence")
    for phrase in FORBIDDEN:
        if phrase in text:
            violations.append(f"{path}: forbidden phrase {phrase}")
    return violations


def main() -> int:
    violations: list[str] = []
    for path in TEXT_FILES:
        violations.extend(audit_file(path))
    if violations:
        print("\n".join(violations))
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
