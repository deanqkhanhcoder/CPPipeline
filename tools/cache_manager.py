import os
import json
import hashlib
import sys
from datetime import datetime

CACHE_DIR = "cache/problemset"
INDEX_FILE = os.path.join(CACHE_DIR, "index.json")

def _init_cache():
    os.makedirs(CACHE_DIR, exist_ok=True)
    if not os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

def get_problem_id(url):
    if "codeforces.com" in url:
        parts = url.split('/')
        if "contest" in parts and "problem" in parts:
            c_idx = parts.index("contest")
            p_idx = parts.index("problem")
            return f"{parts[c_idx+1]}{parts[p_idx+1]}"
        elif "problemset" in parts and "problem" in parts:
            p_idx = parts.index("problem")
            return f"{parts[p_idx+1]}{parts[p_idx+2]}"
    elif "cses.fi" in url:
        return url.split('/')[-1]
    elif "usaco.org" in url:
        if "cpid=" in url:
            return url.split('cpid=')[-1]
        else:
            basename = url.split('/')[-1]
            if basename.lower().endswith('.pdf'):
                return basename[:-4]
            return basename if basename else hashlib.md5(url.encode()).hexdigest()[:8]
    return hashlib.md5(url.encode()).hexdigest()[:8]

def get_source(url):
    if "codeforces" in url.lower(): return "Codeforces"
    if "cses" in url.lower(): return "CSES"
    if "usaco" in url.lower(): return "USACO"
    return "Unknown"

def lookup_cache(url):
    _init_cache()
    pid = get_problem_id(url)
    cache_path = os.path.join(CACHE_DIR, f"{pid}.json")
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                data["_cached"] = True
                return data
        except Exception:
            pass
    return None

def save_cache(url, title, html="", markdown="", content_type="html", pdf_path=None, images=None, order_index=0):
    _init_cache()
    pid = get_problem_id(url)
    source = get_source(url)
    cache_path = os.path.join(CACHE_DIR, f"{pid}.json")
    
    data = {
        "url": url,
        "source": source,
        "problem_id": pid,
        "order_index": order_index,
        "title": title,
        "timestamp": datetime.now().isoformat(),
        "type": content_type,
        "html": html,
        "text": markdown,
        "markdown": markdown,
        "pdf_path": pdf_path,
        "images": images or [],
        "_cached": True
    }
    
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        index_data = json.load(f)
        
    index_data = [item for item in index_data if item["problem_id"] != pid]
    
    index_data.append({
        "problem_id": pid,
        "source": source,
        "title": title,
        "url": url,
        "cached_at": data["timestamp"]
    })
    
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)
        
    print(f"[Cache] Saved to {pid}.json", file=sys.stderr)

def print_stats():
    _init_cache()
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        index_data = json.load(f)
        
    cf_count = sum(1 for x in index_data if x["source"] == "Codeforces")
    cses_count = sum(1 for x in index_data if x["source"] == "CSES")
    usaco_count = sum(1 for x in index_data if x["source"] == "USACO")
    
    print("=== CACHE STATS ===")
    print(f"Total Cached Problems: {len(index_data)}")
    print(f"Codeforces: {cf_count}")
    print(f"CSES: {cses_count}")
    print(f"USACO: {usaco_count}")

if __name__ == "__main__":
    print_stats()
