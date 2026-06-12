"""
html_extractor.py — Token Optimization Tool

PURPOSE:
  Extract only the .problem-statement div from raw HTML stored in
  cache/problemset/<id>.json, and save a clean, minimal JSON to
  cache/normalized/<id>.json.

PHILOSOPHY (LLM-First):
  - Python ONLY extracts the HTML fragment using BeautifulSoup
  - Python does NOT parse, translate, or analyze content
  - All semantic understanding is done by Gemini

RESULT:
  Before: 100-270 KB raw HTML (99% waste: CSS, JS, navigation)
  After:  3-8 KB clean HTML fragment (problem-statement only)
  Token reduction: ~97%
"""

import os
import sys
import json
from datetime import datetime

# BeautifulSoup for structured HTML extraction (NOT content parsing)
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: beautifulsoup4 not installed. Run: pip install beautifulsoup4", file=sys.stderr)
    sys.exit(1)

PROBLEMSET_DIR = "cache/problemset"
NORMALIZED_DIR = "cache/normalized"


def extract_problem_statement(html: str) -> str:
    """Extract the .problem-statement div from full Codeforces HTML.
    
    This is ONLY structural extraction - not content parsing.
    Returns the HTML fragment, or empty string if not found.
    """
    soup = BeautifulSoup(html, "html.parser")
    
    # Try Codeforces .problem-statement
    ps = soup.find(class_="problem-statement")
    if ps:
        return str(ps)
    
    # Try generic .statement or #problem
    for selector in [".statement", "#problem-statement", ".problem", ".task"]:
        el = soup.select_one(selector)
        if el:
            return str(el)
    
    # Fallback: return body content
    body = soup.find("body")
    if body:
        return str(body)
    
    return html  # No extraction possible, return as-is


def extract_one(problem_id: str) -> dict | None:
    """Extract and normalize one problem from cache/problemset/ to cache/normalized/."""
    src_path = os.path.join(PROBLEMSET_DIR, f"{problem_id}.json")
    dst_path = os.path.join(NORMALIZED_DIR, f"{problem_id}.json")
    
    if not os.path.exists(src_path):
        print(f"[Extractor] NOT FOUND: {src_path}", file=sys.stderr)
        return None
    
    # Already normalized
    if os.path.exists(dst_path):
        with open(dst_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["_cached"] = True
        return data
    
    with open(src_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    
    content_type = raw.get("type", "html")
    
    if content_type == "pdf":
        # PDF: no HTML extraction needed, pass through
        normalized = {
            "problem_id": raw.get("problem_id", problem_id),
            "url": raw.get("url", ""),
            "source": raw.get("source", "Unknown"),
            "title": raw.get("title", ""),
            "timestamp": raw.get("timestamp", datetime.now().isoformat()),
            "type": "pdf",
            "content": raw.get("html", ""),  # Just the description
            "pdf_path": raw.get("pdf_path", None),
            "images": raw.get("images", []),
        }
    else:
        # HTML: extract problem-statement fragment only
        raw_html = raw.get("html", "")
        
        if raw_html.startswith("Error:"):
            print(f"[Extractor] SKIP {problem_id}: crawl error", file=sys.stderr)
            return None
        
        before_size = len(raw_html.encode("utf-8"))
        extracted = extract_problem_statement(raw_html)
        after_size = len(extracted.encode("utf-8"))
        
        reduction = ((before_size - after_size) / before_size * 100) if before_size > 0 else 0
        print(f"[Extractor] {problem_id}: {before_size//1024}KB → {after_size//1024}KB ({reduction:.0f}% reduction)", file=sys.stderr)
        
        normalized = {
            "problem_id": raw.get("problem_id", problem_id),
            "url": raw.get("url", ""),
            "source": raw.get("source", "Unknown"),
            "title": raw.get("title", ""),
            "timestamp": raw.get("timestamp", datetime.now().isoformat()),
            "type": "html",
            "content": extracted,
            "pdf_path": None,
            "images": [],
        }
    
    os.makedirs(NORMALIZED_DIR, exist_ok=True)
    with open(dst_path, "w", encoding="utf-8") as f:
        json.dump(normalized, f, ensure_ascii=False, indent=2)
    
    normalized["_cached"] = False
    return normalized


def extract_all():
    """Extract all problems in cache/problemset/ to cache/normalized/."""
    os.makedirs(NORMALIZED_DIR, exist_ok=True)
    
    files = [f for f in os.listdir(PROBLEMSET_DIR) if f.endswith(".json") and f != "index.json"]
    print(f"[Extractor] Found {len(files)} problems to process")
    
    success = 0
    skip = 0
    for fname in files:
        pid = fname[:-5]  # strip .json
        result = extract_one(pid)
        if result:
            success += 1
        else:
            skip += 1
    
    print(f"[Extractor] Done: {success} extracted, {skip} skipped")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "all":
            extract_all()
        else:
            # Extract specific problem ID
            result = extract_one(sys.argv[1])
            if result:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(f"Failed to extract {sys.argv[1]}", file=sys.stderr)
                sys.exit(1)
    else:
        print("Usage: python html_extractor.py <problem_id> | all")
