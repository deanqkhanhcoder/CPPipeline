import os
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def clean_url(url_str: str) -> str:
    url_str = url_str.strip()
    # Remove \url{...}
    m = re.match(r"\\url\s*\{(.*?)\}", url_str)
    if m:
        url_str = m.group(1)
    return url_str.strip()

def main() -> int:
    output_tex = ROOT / "outputs" / "output.tex"
    queue_file = ROOT / "cache" / "queue" / "index.json"
    
    if not output_tex.exists():
        print("PASS: outputs/output.tex does not exist yet. Skip order validation.")
        return 0
        
    if not queue_file.exists():
        print("PASS: cache/queue/index.json does not exist. Skip order validation.")
        return 0
        
    # 1. Read queue and get expected URL order
    try:
        with open(queue_file, "r", encoding="utf-8") as f:
            q = json.load(f)
    except Exception as e:
        print(f"FAIL: Failed to read queue: {e}")
        return 1
        
    all_jobs = []
    for cat in ["pending", "running", "done", "failed"]:
        for job in q.get(cat, []):
            all_jobs.append(job)
            
    # Sort by order_index
    all_jobs.sort(key=lambda x: x.get("order_index", 0))
    expected_urls = [job["url"] for job in all_jobs if "url" in job]
    
    if not expected_urls:
        print("PASS: Queue is empty.")
        return 0
        
    # 2. Read output.tex and find problem URLs
    content = output_tex.read_text(encoding="utf-8", errors="replace")
    
    # Match \problem{Title}{URL}
    # We capture the second group (source)
    problems = re.findall(r"\\problem\s*\{.*?\}\s*\{(.*?)\}", content)
    actual_urls = [clean_url(p) for p in problems]
    
    print(f"Expected URL order (from queue): {expected_urls}")
    print(f"Actual URL order (from PDF): {actual_urls}")
    
    # 3. Check if actual_urls is a subsequence of expected_urls
    # (since some enqueued URLs might have failed/skipped)
    it = iter(expected_urls)
    is_subsequence = all(any(clean_url(x).lower() in clean_url(y).lower() or clean_url(y).lower() in clean_url(x).lower() for y in it) for x in actual_urls)
    
    if not is_subsequence:
        print("FAIL: Actual PDF problem order does not match enqueued URL order.")
        return 1
        
    print("PASS: PDF problem order is correct.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
