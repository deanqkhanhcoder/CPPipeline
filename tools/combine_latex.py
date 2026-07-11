from pathlib import Path
import hashlib
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))
from fragment_qa import validate_content
TEMPLATE_PATH = ROOT / ".agents" / "templates" / "template.tex"
HASH_PATH = ROOT / ".agents" / "metadata" / "template_hash.txt"
BUILD_DIR = ROOT / "cache" / "build"
OUTPUT_PATH = ROOT / "outputs" / "output.tex"
START = "% CONTENT_START"
END = "% CONTENT_END"
COUNT_PLACEHOLDER = "[[PROBLEM_COUNT]]"


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def verify_template_hash() -> None:
    expected = HASH_PATH.read_text(encoding="utf-8").strip().split()[0]
    actual = hashlib.sha256(TEMPLATE_PATH.read_bytes()).hexdigest()
    if actual != expected:
        fail(f"template hash mismatch: {actual} != {expected}")


def read_template() -> tuple[str, str]:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    if COUNT_PLACEHOLDER not in template:
        fail("missing [[PROBLEM_COUNT]] placeholder in template")
    if template.count(START) != 1 or template.count(END) != 1:
        fail("template markers must appear exactly once")
    before, rest = template.split(START, 1)
    _, after = rest.split(END, 1)
    return before + START + "\n", END + after


def validate_body(path: Path, content: str) -> int:
    findings = validate_content(content, str(path), require_sections=True)
    if findings:
        fail(findings[0].line())
    return len(re.findall(r"\\problem\s*\{", content))


def main() -> None:
    verify_template_hash()
    header, footer = read_template()
    files = list(BUILD_DIR.glob("*.tex"))
    file_contents = []
    for file_path in files:
        content = file_path.read_text(encoding="utf-8")
        m = re.search(r"%\s*order_index:\s*(\d+)", content, re.IGNORECASE)
        order_idx = int(m.group(1)) if m else 999999
        file_contents.append((order_idx, file_path.name, file_path, content))

    file_contents.sort()
    body = []
    problem_count = 0
    for order_idx, name, file_path, content in file_contents:
        problem_count += validate_body(file_path, content)
        body.append(content.rstrip() + "\n\\newpage\n")
    output = header + "\n".join(body) + footer
    output = output.replace(COUNT_PLACEHOLDER, str(problem_count))
    if COUNT_PLACEHOLDER in output:
        fail("problem count placeholder leaked into final output")
    if "... Bài toán" in output:
        fail("hardcoded title-page count leaked into final output")
    final_count = len(re.findall(r"\\problem\s*\{", output))
    if final_count != problem_count:
        fail(f"problem count mismatch: title={problem_count}, body={final_count}")
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(output, encoding="utf-8", newline="\n")
    print(f"Created {OUTPUT_PATH}")


if __name__ == "__main__":
    main()