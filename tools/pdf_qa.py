"""PDF QA gate for CP Pipeline. No mutation, no repair."""
from __future__ import annotations
import argparse, subprocess, sys
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Finding:
    error_class: str
    message: str
    def line(self) -> str: return f"{self.error_class}: {self.message}"

TEXT_BANS = (
    ("FORMATTER", "```", "raw Markdown code fence remains"),
    ("PARSER", "<div", "raw HTML remains"),
    ("PARSER", "<span", "raw HTML remains"),
    ("PARSER", "</", "raw HTML closing tag remains"),
    ("FORMATTER", "```mermaid", "raw Mermaid remains"),
    ("FORMATTER", "<svg", "raw SVG remains"),
    ("PARSER", "DescriptionDescription", "UI chrome remains"),
    ("PARSER", "TopicsCompanies", "UI chrome remains"),
    ("LATEX", "Undefined control sequence", "LaTeX error text visible"),
)
LOG_BANS = (
    ("COMPILE", "Fatal error occurred", "fatal compile error"),
    ("COMPILE", "Emergency stop", "compile emergency stop"),
    ("LATEX", "Undefined control sequence", "undefined control sequence"),
    ("LATEX", "LaTeX Error", "LaTeX error"),
    ("LATEX", "Missing $ inserted", "math mode error"),
)

def pdf_to_text(pdf: Path) -> str:
    try:
        res = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
    except FileNotFoundError:
        raise SystemExit("PDF: pdftotext not found; cannot audit PDF text")
    if res.returncode != 0:
        raise SystemExit(f"PDF: pdftotext failed: {res.stderr.strip()}")
    return res.stdout

def audit_text(text: str) -> list[Finding]:
    findings: list[Finding] = []
    for error_class, token, message in TEXT_BANS:
        if token in text: findings.append(Finding(error_class, f"{message}: {token}"))
    if "Table of Contents" in text and "M?c l?c" not in text:
        findings.append(Finding("PDF", "TOC title appears inconsistent"))
    return findings

def audit_log(log_text: str, max_overfull: int) -> list[Finding]:
    findings: list[Finding] = []
    for error_class, token, message in LOG_BANS:
        if token in log_text: findings.append(Finding(error_class, f"{message}: {token}"))
    overfull = log_text.count("Overfull \hbox") + log_text.count("Overfull \vbox")
    if overfull > max_overfull:
        findings.append(Finding("PDF", f"too many overfull boxes: {overfull} > {max_overfull}"))
    return findings

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit compiled PDF and LaTeX log before archive.")
    parser.add_argument("pdf", nargs="?")
    parser.add_argument("--text-file")
    parser.add_argument("--log", default="cache/debug/compile_error.log")
    parser.add_argument("--max-overfull", type=int, default=20)
    args = parser.parse_args(argv)
    if args.text_file:
        text = Path(args.text_file).read_text(encoding="utf-8", errors="replace")
    else:
        if not args.pdf:
            print("PDF: missing PDF path", file=sys.stderr); return 1
        pdf = Path(args.pdf)
        if not pdf.exists() or pdf.stat().st_size == 0:
            print(f"PDF: missing or empty PDF: {pdf}", file=sys.stderr); return 1
        text = pdf_to_text(pdf)
    log_path = Path(args.log)
    findings = audit_text(text) + audit_log(log_path.read_text(encoding="utf-8", errors="replace") if log_path.exists() else "", args.max_overfull)
    if findings:
        for finding in findings: print(finding.line(), file=sys.stderr)
        return 1
    print("PASS: PDF QA")
    return 0
if __name__ == "__main__": raise SystemExit(main())
