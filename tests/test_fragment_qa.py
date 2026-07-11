import tempfile
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from fragment_qa import validate_content

GOOD = r"""% order_index: 1
\problem{T?ng hai s? (Two Sum)}{CSES}
N?i dung.
\inputformat
M?t d?ng.
\outputformat
M?t d?ng.
\constraints
$1 \le n \le 10$.
\endconstraints
\example
\begin{lstlisting}
1 2
\end{lstlisting}
\explanation
V? d? h?p l?.
"""

def assert_class(text, klass):
    findings = validate_content(text, "x.tex")
    assert any(f.error_class == klass for f in findings), [f.line() for f in findings]

def test_good_fragment_passes():
    assert validate_content(GOOD, "good.tex") == []

def test_parser_pollution_fails():
    assert_class(GOOD + "DescriptionDescription", "PARSER")

def test_markdown_fails():
    assert_class(GOOD + "```", "FORMATTER")

def test_html_fails():
    assert_class(GOOD + "<div>", "PARSER")

def test_mermaid_fails():
    assert_class(GOOD + "```mermaid", "FORMATTER")

def test_obsolete_macro_fails():
    assert_class(GOOD + r"\begin{inputbox}", "LATEX")

def test_invalid_title_fails():
    bad = GOOD.replace(r"\problem{T?ng hai s? (Two Sum)}", r"\problem{\begin{itemize}Bad}")
    assert_class(bad, "LATEX")

if __name__ == "__main__":
    test_good_fragment_passes()
    test_parser_pollution_fails()
    test_markdown_fails()
    test_html_fails()
    test_mermaid_fails()
    test_obsolete_macro_fails()
    test_invalid_title_fails()
    print("PASS")
