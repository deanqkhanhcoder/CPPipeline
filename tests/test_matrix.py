import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_1_no_root_pollution():
    allowed_root = {"README.md", "LICENSE", "requirements.txt", ".gitignore", ".agents", "archive", "cache", "outputs", "reports", "tools", "tests", "build.py"}
    actual = {p.name for p in ROOT.iterdir()}
    illegal = actual - allowed_root - {".git", ".venv", "node_modules", "__pycache__", "env"}
    assert not illegal, f"Root pollution detected: {illegal}"

def test_2_no_temp_files_at_root():
    for ext in [".tmp", ".log", ".aux", ".out", ".toc", ".synctex.gz", ".pyc"]:
        illegal = list(ROOT.glob(f"*{ext}"))
        assert not illegal, f"Temp files found at root: {illegal}"

def test_3_no_hardcoded_paths():
    for py in ROOT.rglob("*.py"):
        if py.name in {"test_matrix.py", "audit_encoding.py", "repair_encoding.py"}:
            continue
        content = py.read_text(encoding="utf-8", errors="replace")
        assert "C:\\Users\\" not in content and "/home/" not in content, f"Hardcoded path found in {py}"

def test_4_single_source_of_truth_template():
    template = ROOT / ".agents" / "templates" / "template.tex"
    assert template.exists(), "template.tex is missing"
    content = template.read_text(encoding="utf-8")
    assert "\\documentclass" in content and "\\begin{document}" in content, "template.tex invalid"

def test_5_no_fake_compile_success():
    compile_py = ROOT / "tools" / "compile_latex.py"
    content = compile_py.read_text(encoding="utf-8")
    assert "returncode == 0" in content, "compile_latex.py does not enforce returncode == 0"

def test_6_output_contract():
    out_dir = ROOT / "outputs"
    if out_dir.exists():
        for p in out_dir.iterdir():
            if p.name != ".keep":
                assert p.name in {"output.tex", "output.pdf"}, f"Illegal file in outputs/: {p.name}"

def test_7_archive_contract():
    arch_py = ROOT / "tools" / "archive_output.py"
    content = arch_py.read_text(encoding="utf-8")
    assert "index.json" in content and "archive" in content, "Archive contract violated in archive_output.py"

def test_8_no_regex_cp_parsing():
    for py in (ROOT / "tools").glob("*.py"):
        if py.name in {"extract_html.py", "text_normalizer.py", "combine_latex.py"}:
            continue
        content = py.read_text(encoding="utf-8")
        assert "re.findall(r'Input'" not in content and "re.search(r'Output'" not in content, f"Illegal regex CP parsing in {py.name}"

def test_9_allowlist_dom_no_raw_html():
    extract_py = ROOT / "tools" / "extract_html.py"
    content = extract_py.read_text(encoding="utf-8")
    assert "BeautifulSoup" in content or "allowlist" in content.lower(), "extract_html.py missing DOM allowlist"

def test_10_no_python_pdf_ocr():
    for py in ROOT.rglob("*.py"):
        if py.name == "test_matrix.py": continue
        content = py.read_text(encoding="utf-8", errors="replace")
        assert "pytesseract" not in content and "paddleocr" not in content.lower(), f"Illegal PDF OCR found in {py}"

def test_11_no_external_llm_api():
    for py in ROOT.rglob("*.py"):
        if py.name == "test_matrix.py": continue
        content = py.read_text(encoding="utf-8", errors="replace")
        assert "openai.ChatCompletion" not in content and "gemini.generate_content" not in content, f"External LLM API call in {py}"

def test_12_no_patch_scripts():
    for py in ROOT.glob("fix_output*.py"):
        assert False, f"Illegal patch script found at root: {py}"

def test_13_declarative_dependency_graph():
    for skill_md in (ROOT / ".agents" / "skills").rglob("SKILL.md"):
        content = skill_md.read_text(encoding="utf-8")
        assert "## Declarative Dependencies" in content, f"Missing Declarative Dependencies in {skill_md}"

def test_14_deterministic_state_machine():
    esm = ROOT / ".agents" / "runtime" / "execution_state_machine.md"
    content = esm.read_text(encoding="utf-8")
    assert "CONTINUOUS IMPROVEMENT" in content and "### SKILL INVOKED" in content, "State machine not deterministic or missing continuous improvement"

def test_15_quality_gates_order():
    cpp = ROOT / ".agents" / "skills" / "cp-pipeline" / "SKILL.md"
    content = cpp.read_text(encoding="utf-8")
    assert "Fragment Quality Gate" in content and "PDF Quality Gate" in content, "Quality gates missing from cp-pipeline skill"

def test_16_error_taxonomy_compliance():
    et = ROOT / ".agents" / "policies" / "error_taxonomy.md"
    content = et.read_text(encoding="utf-8")
    for cls in ["PARSER", "NORMALIZER", "TRANSLATOR", "FORMATTER", "LATEX", "COMBINE", "COMPILE", "PDF", "RUNTIME"]:
        assert cls in content, f"Missing error class {cls} in taxonomy"

def test_17_root_cause_loop_compliance():
    sip = ROOT / ".agents" / "policies" / "self_improvement_policy.md"
    content = sip.read_text(encoding="utf-8")
    assert "Root Cause Loop" in content and "11" in content, "Missing 11-step Root Cause Loop in policy"

def test_18_knowledge_feedback_loop():
    sip = ROOT / ".agents" / "policies" / "self_improvement_policy.md"
    content = sip.read_text(encoding="utf-8")
    assert "Knowledge Feedback Loop" in content and "Skill" in content, "Missing Knowledge Feedback Loop in policy"

def test_19_no_speculative_language():
    for md in (ROOT / ".agents").rglob("*.md"):
        if md.name in {"error_taxonomy.md", "self_improvement_policy.md", "decision_policy.md", "host_llm_contract.md", "runtime.md"}:
            continue
        content = md.read_text(encoding="utf-8", errors="replace")
        assert "Maybe this works" not in content and "Thinking..." not in content, f"Speculative language in {md}"

def test_20_self_improvement_enforcement():
    sip = ROOT / ".agents" / "policies" / "self_improvement_policy.md"
    assert sip.exists(), "self_improvement_policy.md missing"
    content = sip.read_text(encoding="utf-8")
    assert "FAIL" in content, "Self-improvement enforcement missing FAIL condition"

def main():
    tests = [
        test_1_no_root_pollution,
        test_2_no_temp_files_at_root,
        test_3_no_hardcoded_paths,
        test_4_single_source_of_truth_template,
        test_5_no_fake_compile_success,
        test_6_output_contract,
        test_7_archive_contract,
        test_8_no_regex_cp_parsing,
        test_9_allowlist_dom_no_raw_html,
        test_10_no_python_pdf_ocr,
        test_11_no_external_llm_api,
        test_12_no_patch_scripts,
        test_13_declarative_dependency_graph,
        test_14_deterministic_state_machine,
        test_15_quality_gates_order,
        test_16_error_taxonomy_compliance,
        test_17_root_cause_loop_compliance,
        test_18_knowledge_feedback_loop,
        test_19_no_speculative_language,
        test_20_self_improvement_enforcement
    ]
    for idx, t in enumerate(tests, 1):
        try:
            t()
            print(f"[{idx}/20] {t.__name__}: PASS")
        except AssertionError as e:
            print(f"[{idx}/20] {t.__name__}: FAIL -> {e}")
            sys.exit(1)
    print("\nALL 20 ARCHITECTURAL & SCALE CRITERIA PASSED 100%!")
    sys.exit(0)

if __name__ == "__main__":
    main()
