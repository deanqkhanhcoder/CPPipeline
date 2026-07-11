import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from pdf_qa import audit_text, audit_log

def test_pdf_text_passes():
    assert audit_text("B?i to?n h?p l?\nD? li?u v?o\n") == []

def test_pdf_rejects_markdown():
    assert any(f.error_class == "FORMATTER" for f in audit_text("```"))

def test_pdf_rejects_html():
    assert any(f.error_class == "PARSER" for f in audit_text("<div>"))

def test_pdf_rejects_mermaid_svg():
    findings = audit_text("```mermaid\n<svg")
    assert {f.error_class for f in findings} == {"FORMATTER"}

def test_pdf_rejects_ui_chrome():
    assert any(f.error_class == "PARSER" for f in audit_text("TopicsCompanies"))

def test_pdf_rejects_undefined_control_sequence():
    assert any(f.error_class == "LATEX" for f in audit_log("Undefined control sequence", 20))

def test_pdf_rejects_too_many_overfull():
    assert any(f.error_class == "PDF" for f in audit_log("Overfull \\hbox\n" * 21, 20))

if __name__ == "__main__":
    test_pdf_text_passes()
    test_pdf_rejects_markdown()
    test_pdf_rejects_html()
    test_pdf_rejects_mermaid_svg()
    test_pdf_rejects_ui_chrome()
    test_pdf_rejects_undefined_control_sequence()
    test_pdf_rejects_too_many_overfull()
    print("PASS")
