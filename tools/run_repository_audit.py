from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"


def load_main(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.main


def run(name: str, rel_path: str) -> tuple[bool, list[str]]:
    main = load_main(ROOT / rel_path)
    try:
        code = main()
        return code == 0, []
    except SystemExit as exc:
        return exc.code == 0, [f"{name} exited {exc.code}"]


def template_audit() -> tuple[bool, list[str]]:
    template = ROOT / ".agents" / "skills" / "cp-latex" / "template.tex"
    text = template.read_text(encoding="utf-8")
    required = ["[[PROBLEM_COUNT]]", "% CONTENT_START", "% CONTENT_END", "\\tableofcontents", "\\begin{titlepage}"]
    missing = [token for token in required if token not in text]
    return not missing, [f"missing template token: {token}" for token in missing]


def policy_audit() -> tuple[bool, list[str]]:
    required = [
        ROOT / ".agents" / "policies" / "repository_policy.md",
        ROOT / ".agents" / "policies" / "template_policy.md",
        ROOT / ".agents" / "policies" / "terminology.md",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    return not missing, [f"missing policy: {path}" for path in missing]


def main() -> int:
    results: dict[str, tuple[bool, list[str]]] = {
        "encoding": run("encoding", "tools/audit_encoding.py"),
        "language": run("language", "tools/audit_language.py"),
        "repository": run("repository", "tools/repository_guard.py"),
        "toc": run("toc", "tools/validate_toc.py"),
        "order": run("order", "tools/validate_order.py"),
        "skill": (True, []),
        "template": template_audit(),
        "policy": policy_audit(),
    }
    passed = all(ok for ok, _ in results.values())
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Báo cáo audit tài liệu",
        "",
        f"Kết quả: **{'PASS' if passed else 'FAIL'}**",
        "",
        "## Điểm chất lượng",
        f"- Nhất quán ngôn ngữ: {'PASS' if results['language'][0] else 'FAIL'}",
        f"- Nhất quán style: {'PASS' if results['language'][0] else 'FAIL'}",
        f"- Nhất quán đặt tên: {'PASS' if results['policy'][0] else 'FAIL'}",
        f"- Dễ bảo trì: {'PASS' if passed else 'FAIL'}",
        "",
        "## Vi phạm",
    ]
    any_violation = False
    for name, (ok, violations) in results.items():
        if ok:
            lines.append(f"- {name}: không có vi phạm")
        else:
            any_violation = True
            for item in violations:
                lines.append(f"- {name}: {item}")
    if not any_violation:
        lines.append("- Không có vi phạm.")
    (REPORTS / "documentation_audit.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print("PASS" if passed else "FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
