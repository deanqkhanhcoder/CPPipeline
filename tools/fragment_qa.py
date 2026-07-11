"""Fragment QA gate for CP Pipeline. No mutation, no repair."""
from __future__ import annotations
import argparse, re, sys
from dataclasses import dataclass
from pathlib import Path

ERROR_CLASSES = {"PARSER","NORMALIZER","TRANSLATOR","FORMATTER","LATEX","COMBINE","COMPILE","PDF","RUNTIME"}
BANNED_TOKENS = (
    ("LATEX", r"\documentclass", "fragment contains document preamble"),
    ("LATEX", r"\usepackage", "fragment contains package declaration"),
    ("LATEX", r"\begin{titlepage}", "fragment contains title page"),
    ("LATEX", r"\end{titlepage}", "fragment contains title page"),
    ("LATEX", r"\tableofcontents", "fragment contains TOC"),
    ("LATEX", r"\pagestyle", "fragment changes page style"),
    ("LATEX", r"\fancyhead", "fragment changes header"),
    ("LATEX", r"\fancyfoot", "fragment changes footer"),
    ("LATEX", r"\fancyhf", "fragment changes header/footer"),
    ("LATEX", r"\hypersetup", "fragment changes hyperref"),
    ("LATEX", r"\definecolor", "fragment defines template color"),
    ("LATEX", r"\newcommand", "fragment defines macro"),
    ("LATEX", r"\def\end", "fragment contains unsafe TeX definition"),
    ("LATEX", r"\begin{constraintbox}", "obsolete macro/environment"),
    ("LATEX", r"\end{constraintbox}", "obsolete macro/environment"),
    ("LATEX", r"\begin{examplebox}", "obsolete macro/environment"),
    ("LATEX", r"\end{examplebox}", "obsolete macro/environment"),
    ("LATEX", r"\begin{codebg}", "obsolete macro/environment"),
    ("LATEX", r"\end{codebg}", "obsolete macro/environment"),
    ("LATEX", r"\begin{exmp}", "obsolete macro/environment"),
    ("LATEX", r"\end{exmp}", "obsolete macro/environment"),
    ("LATEX", r"\begin{samplebox}", "obsolete macro/environment"),
    ("LATEX", r"\end{samplebox}", "obsolete macro/environment"),
    ("LATEX", r"\begin{inputbox}", "obsolete macro/environment"),
    ("LATEX", r"\end{inputbox}", "obsolete macro/environment"),
    ("LATEX", r"\begin{outputbox}", "obsolete macro/environment"),
    ("LATEX", r"\end{outputbox}", "obsolete macro/environment"),
    ("FORMATTER", "```", "raw Markdown fence"),
    ("FORMATTER", "```mermaid", "raw Mermaid fence"),
    ("PARSER", "<div", "raw HTML tag"),
    ("PARSER", "<span", "raw HTML tag"),
    ("PARSER", "</", "raw HTML closing tag"),
    ("PARSER", "DescriptionDescription", "UI chrome leak"),
    ("PARSER", "TopicsCompanies", "UI chrome leak"),
    ("LATEX", "[backgroundcolor=", "raw tcolorbox option leak"),
    ("LATEX", "{backgroundcolor=", "raw tcolorbox option leak"),
    ("FORMATTER", "---\n", "raw YAML marker"),
    ("FORMATTER", "{\"", "raw JSON marker"),
)
REQUIRED_MACROS = (r"\problem", r"\inputformat", r"\outputformat")

@dataclass(frozen=True)
class Finding:
    error_class: str
    path: str
    message: str
    def line(self) -> str: return f"{self.error_class}: {self.path}: {self.message}"

def validate_content(content: str, path: str = "<memory>", require_sections: bool = True) -> list[Finding]:
    findings: list[Finding] = []
    for error_class, token, message in BANNED_TOKENS:
        if token in content:
            findings.append(Finding(error_class, path, f"{message}: {token}"))
    if not re.search(r"\\problem\s*\{", content):
        findings.append(Finding("LATEX", path, "missing \problem macro"))
    for title in re.findall(r"\\problem\s*\{(.*?)\}\s*\{", content, flags=re.DOTALL):
        if "\\" in title or "\n" in title:
            findings.append(Finding("LATEX", path, "invalid \problem title contains command or newline"))
        if not title.strip():
            findings.append(Finding("LATEX", path, "empty \problem title"))
    commands = set(re.findall(r"\\([A-Za-z]+)", content))
    obsolete = commands & {"constraintbox","examplebox","codebg","exmp","samplebox","inputbox","outputbox"}
    if obsolete:
        findings.append(Finding("LATEX", path, f"obsolete/hallucinated macro(s): {', '.join(sorted(obsolete))}"))
    if require_sections:
        for macro in REQUIRED_MACROS:
            if macro not in content:
                findings.append(Finding("LATEX", path, f"missing required macro {macro}"))
        if r"\example" not in content:
            findings.append(Finding("FORMATTER", path, "missing sample block \example"))
        if r"\explanation" not in content:
            findings.append(Finding("FORMATTER", path, "missing sample explanation \explanation"))
    return findings

def iter_tex_files(target: Path) -> list[Path]:
    return [target] if target.is_file() else sorted(target.glob("*.tex"))

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate LaTeX fragments before combine.")
    parser.add_argument("target", nargs="?", default="cache/build")
    parser.add_argument("--no-require-sections", action="store_true")
    args = parser.parse_args(argv)
    target = Path(args.target)
    if not target.exists():
        print(f"PARSER: {target}: path does not exist", file=sys.stderr); return 1
    findings: list[Finding] = []
    files = iter_tex_files(target)
    if not files:
        print(f"COMBINE: {target}: no .tex fragments found", file=sys.stderr); return 1
    for path in files:
        findings.extend(validate_content(path.read_text(encoding="utf-8", errors="replace"), str(path), not args.no_require_sections))
    if findings:
        for finding in findings: print(finding.line(), file=sys.stderr)
        return 1
    print(f"PASS: fragment QA checked {len(files)} file(s)")
    return 0
if __name__ == "__main__": raise SystemExit(main())
