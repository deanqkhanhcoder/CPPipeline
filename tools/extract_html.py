"""
extract_html.py — Token Optimization Tool

PURPOSE:
  Extract only the .problem-statement div from raw HTML stored in
  cache/problemset/<id>.json, and save a clean, minimal JSON to
  cache/normalized/<id>.json.

PHILOSOPHY (LLM-First):
  - Python ONLY extracts the HTML fragment using BeautifulSoup
  - Python does NOT parse, translate, or analyze content
  - All semantic understanding is done by Gemini

ARCHITECTURE: ALLOWLIST DOM EXTRACTION
  Instead of a blocklist (remove bad tags), we use an allowlist (keep only
  content tags). This is the only architecture that can guarantee
  forbidden_dom_violations = 0.

RESULT:
  Before: 100-270 KB raw HTML (99% waste: CSS, JS, navigation)
  After:  1-5 KB clean text+math fragment (problem-statement only)
  Token reduction: ~99%
"""

import os
import json
import sys
from datetime import datetime

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stdin.encoding.lower() != 'utf-8':
    sys.stdin.reconfigure(encoding='utf-8')

# BeautifulSoup for structural HTML extraction (NOT content parsing)
try:
    from bs4 import BeautifulSoup, NavigableString, Tag, Comment
except ImportError:
    print("ERROR: beautifulsoup4 not installed. Run: pip install beautifulsoup4", file=sys.stderr)
    sys.exit(1)

PROBLEMSET_DIR = "cache/problemset"
NORMALIZED_DIR = "cache/normalized"

# ──────────────────────────────────────────────────────────────────────────────
# ALLOWLIST: only these tags are allowed to remain in the output.
# Anything not in this list is UNWRAPPED (children kept) or REMOVED (no children).
# ──────────────────────────────────────────────────────────────────────────────
ALLOWED_TAGS = {
    # Text structure
    "p", "br", "hr",
    # Headings
    "h1", "h2", "h3", "h4", "h5", "h6",
    # Containers (structural only — kept because they carry semantic classes)
    "div", "span",
    # Lists
    "ul", "ol", "li",
    # Preformatted / code
    "pre", "code",
    # Emphasis
    "b", "i", "em", "strong", "sup", "sub",
    # Tables (for sample I/O)
    "table", "thead", "tbody", "tfoot", "tr", "th", "td",
    # Math (native MathML — kept verbatim)
    "math", "mi", "mo", "mn", "ms", "mtext", "mrow",
    "mfrac", "msqrt", "mroot", "mstyle", "merror",
    "mpadded", "mphantom", "mfenced", "menclose",
    "msub", "msup", "msubsup", "munder", "mover",
    "munderover", "mmultiscripts", "annotation", "semantics",
}

# ──────────────────────────────────────────────────────────────────────────────
# FORBIDDEN (always removed, children too):
# These are noise/chrome that must NEVER reach downstream LLMs.
# ──────────────────────────────────────────────────────────────────────────────
FORBIDDEN_TAGS = {
    "script", "style", "noscript", "iframe", "object", "embed",
    "form", "input", "button", "select", "textarea",
    "nav", "header", "footer", "aside", "menu", "menuitem",
    "canvas", "video", "audio", "source", "track",
    "svg", "img",  # images stripped (LLM sees text only; PDF images handled separately)
}

# ──────────────────────────────────────────────────────────────────────────────
# FORBIDDEN CLASSES: nodes with these classes are removed entirely (content too).
# Covers Codeforces UI chrome that lives inside .problem-statement.
# ──────────────────────────────────────────────────────────────────────────────
FORBIDDEN_CLASSES = {
    "input-output-copier",
    "MathJax_Preview",   # duplicate rendered math — the script tag has the real LaTeX
    "MathJax",
    "mjx-chtml",
    "MathJax_CHTML",
    "MathJax_SVG",
    "MathJax_MathML",
    "mathjax",
}

# ──────────────────────────────────────────────────────────────────────────────
# ALLOWED ATTRIBUTES per tag.
# All other attributes (id, style, data-*, title, onclick, ...) are stripped.
# ──────────────────────────────────────────────────────────────────────────────
ALLOWED_ATTRS: dict[str, set[str]] = {
    # semantic classes are essential for LLM to understand structure
    "div": {"class"},
    "span": {"class"},
    "pre": {"class"},
    "code": {"class"},
    "table": {"class"},
    "td": {"class"},
    "th": {"class"},
    # math attributes needed for correct rendering by LLM parsers
    "math": {"xmlns", "display"},
    "annotation": {"encoding"},
}

# Mathml tags inherit all standard MathML attributes
_MATHML_ATTRS = {"mathvariant", "mathsize", "mathcolor", "mathbackground",
                 "displaystyle", "scriptlevel", "accent", "accentunder",
                 "open", "close", "separators", "stretchy", "symmetric",
                 "maxsize", "minsize", "largeop", "movablelimits",
                 "lspace", "rspace", "fence", "notation", "width", "height",
                 "rowspan", "columnspan", "rowalign", "columnalign", "align",
                 "columnlines", "rowlines", "frame", "columnwidth", "equalrows",
                 "equalcolumns", "side", "minlabelspacing", "numalign",
                 "denomalign", "bevelled", "subscriptshift", "superscriptshift",
                 "position", "shift", "location", "edge"}
for _t in {"mi", "mo", "mn", "ms", "mtext", "mrow", "mfrac", "msqrt",
           "mroot", "mstyle", "merror", "mpadded", "mphantom", "mfenced",
           "menclose", "msub", "msup", "msubsup", "munder", "mover",
           "munderover", "mmultiscripts", "semantics", "annotation"}:
    ALLOWED_ATTRS[_t] = _MATHML_ATTRS


def _has_forbidden_class(tag: Tag) -> bool:
    """True if any of tag's classes are forbidden."""
    classes = tag.get("class", [])
    if isinstance(classes, str):
        classes = classes.split()
    return bool(set(classes) & FORBIDDEN_CLASSES)


def _clean_node(node) -> str:
    """
    Recursively walk a BS4 node and return a clean HTML string.
    - Comments → removed
    - NavigableString → kept as-is (actual text)
    - Tag in FORBIDDEN_TAGS or with FORBIDDEN_CLASSES → removed entirely
    - Tag NOT in ALLOWED_TAGS → unwrapped (recurse into children, keep text)
    - Tag in ALLOWED_TAGS → recurse children, rebuild with allowed attrs only
    """
    if isinstance(node, Comment):
        return ""
    if isinstance(node, NavigableString):
        return str(node)

    if not isinstance(node, Tag):
        return ""

    tag_name = node.name.lower() if node.name else ""

    # Hard-remove forbidden tags (and all their children)
    if tag_name in FORBIDDEN_TAGS:
        return ""

    # Hard-remove forbidden class nodes
    if _has_forbidden_class(node):
        return ""

    # Recurse into children first
    inner = "".join(_clean_node(child) for child in node.children)

    # If tag is allowed, rebuild it with clean attributes
    if tag_name in ALLOWED_TAGS:
        allowed = ALLOWED_ATTRS.get(tag_name, set())
        attrs_out = []
        for k, v in node.attrs.items():
            if k in allowed:
                if isinstance(v, list):
                    v = " ".join(v)
                attrs_out.append(f'{k}="{v}"')
        attr_str = (" " + " ".join(attrs_out)) if attrs_out else ""
        # Self-closing if no inner content and tag is typically void
        if not inner.strip() and tag_name in {"br", "hr"}:
            return f"<{tag_name}{attr_str}/>"
        return f"<{tag_name}{attr_str}>{inner}</{tag_name}>"

    # Not in allowed tags → unwrap (keep children's text, drop the wrapper tag)
    return inner


def extract_problem_statement(html: str) -> str:
    """
    Locate the problem statement root node, then apply the Allowlist DOM Walker.

    Strategy (tried in order):
    1. Codeforces  → .problem-statement
    2. CSES        → #task-statement, .task-statement
    3. USACO       → .problem-text, .problem-statement
    4. Generic     → #problem-statement, .statement, .problem, .task
    5. Fallback    → <body>

    Returns a clean, minimal HTML string with only allowed content.
    """
    soup = BeautifulSoup(html, "html.parser")

    root = None

    # Ordered selector search
    selectors = [
        # Codeforces
        ".problem-statement",
        # CSES
        "#task-statement", ".task-statement",
        # USACO
        ".problem-text", "#problem-text",
        # Generic
        "#problem-statement", ".statement", ".problem", ".task",
    ]
    for sel in selectors:
        el = soup.select_one(sel)
        if el:
            root = el
            break

    # Absolute fallback
    if root is None:
        root = soup.find("body") or soup

    # Apply allowlist walker
    cleaned = _clean_node(root)

    # Collapse excess whitespace (preserve newlines inside <pre>)
    import re
    cleaned = re.sub(r"[ \t]+", " ", cleaned)      # multiple spaces → one
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)   # 3+ newlines → 2
    return cleaned.strip()


def extract_one(problem_id: str, force: bool = False) -> dict | None:
    """Extract and normalize one problem from cache/problemset/ to cache/normalized/."""
    src_path = os.path.join(PROBLEMSET_DIR, f"{problem_id}.json")
    dst_path = os.path.join(NORMALIZED_DIR, f"{problem_id}.json")

    if not os.path.exists(src_path):
        print(f"[Extractor] NOT FOUND: {src_path}", file=sys.stderr)
        return None

    # Already normalized (skip unless forced)
    if os.path.exists(dst_path) and not force:
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
            "order_index": raw.get("order_index", 0),
            "timestamp": raw.get("timestamp", datetime.now().isoformat()),
            "type": "pdf",
            "content": raw.get("html", ""),
            "pdf_path": raw.get("pdf_path", None),
            "images": raw.get("images", []),
        }
    else:
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
            "order_index": raw.get("order_index", 0),
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


def extract_all(force: bool = False):
    """Extract all problems in cache/problemset/ to cache/normalized/."""
    os.makedirs(NORMALIZED_DIR, exist_ok=True)

    files = [f for f in os.listdir(PROBLEMSET_DIR) if f.endswith(".json") and f != "index.json"]
    print(f"[Extractor] Found {len(files)} problems to process")

    success = 0
    skip = 0
    for fname in files:
        pid = fname[:-5]
        result = extract_one(pid, force=force)
        if result:
            success += 1
        else:
            skip += 1

    print(f"[Extractor] Done: {success} extracted, {skip} skipped")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    force = "--force" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    if args:
        if args[0] == "all":
            extract_all(force=force)
        else:
            result = extract_one(args[0], force=force)
            if result:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(f"Failed to extract {args[0]}", file=sys.stderr)
                sys.exit(1)
    else:
        print("Usage: python extract_html.py <problem_id|all> [--force]")
