"""
token_efficiency_audit.py — Validate that extracted HTML contains NO forbidden DOM nodes.
"""

import os
import json
import sys

# Try loading beautifulsoup
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: beautifulsoup4 not installed.", file=sys.stderr)
    sys.exit(1)

NORMALIZED_DIR = "cache/normalized"

FORBIDDEN_TAGS = {
    "script", "style", "noscript", "iframe", "object", "embed",
    "form", "input", "button", "select", "textarea",
    "nav", "header", "footer", "aside", "menu", "menuitem",
    "canvas", "video", "audio", "source", "track",
    "svg", "img",
}

FORBIDDEN_CLASSES = {
    "input-output-copier",
    "MathJax_Preview",
    "MathJax",
    "mjx-chtml",
    "MathJax_CHTML",
    "MathJax_SVG",
    "MathJax_MathML",
    "mathjax",
    "hidden",
    "ads",
    "copy-button",
}

def audit_file(filepath: str) -> list[str]:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    if data.get("type") != "html":
        return []
    
    html = data.get("content", "")
    soup = BeautifulSoup(html, "html.parser")
    
    violations = []
    
    # 1. Check for forbidden tags
    for tag in soup.find_all(True):
        if tag.name.lower() in FORBIDDEN_TAGS:
            violations.append(f"Forbidden tag: <{tag.name}>")
            
        classes = tag.get("class", [])
        if isinstance(classes, str):
            classes = classes.split()
            
        for c in classes:
            if c in FORBIDDEN_CLASSES:
                violations.append(f"Forbidden class: {c}")
                
        # 2. Check for leftover inline styles or onclick
        if tag.has_attr("style"):
            violations.append(f"Forbidden attribute 'style' on <{tag.name}>")
        if tag.has_attr("id"):
            violations.append(f"Forbidden attribute 'id' on <{tag.name}>")
            
    return violations

def main():
    if not os.path.exists(NORMALIZED_DIR):
        print(f"Directory {NORMALIZED_DIR} not found.")
        return 1
        
    files = [f for f in os.listdir(NORMALIZED_DIR) if f.endswith(".json")]
    
    total_files = len(files)
    total_violations = 0
    
    for f in files:
        filepath = os.path.join(NORMALIZED_DIR, f)
        v = audit_file(filepath)
        if v:
            print(f"FAIL {f}:")
            for viol in set(v):
                print(f"  - {viol}")
            total_violations += len(v)
            
    print(f"\nAudit complete. Checked {total_files} files.")
    print(f"forbidden_dom_violations = {total_violations}")
    
    if total_violations > 0:
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
