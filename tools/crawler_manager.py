import os
import json
import time
import sys
import hashlib
from datetime import datetime

# Make sure we can import crawl_problem
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from crawl_problem import crawl_problem

QUEUE_DIR = "cache/queue"
QUEUE_FILE = os.path.join(QUEUE_DIR, "index.json")

def init_queue():
    os.makedirs(QUEUE_DIR, exist_ok=True)
    if not os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "pending": [],
                "running": [],
                "done": [],
                "failed": []
            }, f, indent=2)

def read_queue():
    init_queue()
    with open(QUEUE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def write_queue(q):
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(q, f, indent=2)

def get_job_id(url):
    return hashlib.md5(url.encode()).hexdigest()[:8]

def enqueue_url(url):
    q = read_queue()
    job_id = get_job_id(url)
    
    # Check if already exists anywhere
    for category in ["pending", "running", "done", "failed"]:
        for job in q[category]:
            if job["url"] == url:
                if category in ["failed", "pending"]:
                    # Move to pending if failed
                    q[category].remove(job)
                    break
                else:
                    return job_id # Already running or done
                    
    job = {
        "id": job_id,
        "url": url,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "html_path": None,
        "error": None,
        "retry_count": 0
    }
    q["pending"].append(job)
    write_queue(q)
    return job_id

def process_queue():
    while True:
        q = read_queue()
        if not q["pending"]:
            break
            
        job = q["pending"].pop(0)
        job["status"] = "running"
        job["updated_at"] = datetime.now().isoformat()
        q["running"].append(job)
        write_queue(q)
        
        url = job["url"]
        print(f"[Crawler Manager] Processing {url}...")
        
        # Single Browser Policy is enforced because this is a single-threaded daemon
        try:
            result = crawl_problem(url)
            
            # Reload queue in case it was modified
            q = read_queue()
            
            # Find and remove from running
            for j in q["running"]:
                if j["id"] == job["id"]:
                    q["running"].remove(j)
                    break
                    
            if result and not result.get("html", "").startswith("Error:"):
                job["status"] = "done"
                job["updated_at"] = datetime.now().isoformat()
                job["html_path"] = f"cache/problemset/{job['id']}.json" # It actually saves by problem_id in crawl_problem
                job["error"] = None
                q["done"].append(job)
                print(f"[Crawler Manager] Success: {url}")
            else:
                job["status"] = "failed"
                job["updated_at"] = datetime.now().isoformat()
                job["error"] = result.get("html", "Unknown error") if result else "Crawl failed"
                job["retry_count"] = job.get("retry_count", 0) + 1
                q["failed"].append(job)
                print(f"[Crawler Manager] Failed: {url}")
                
            write_queue(q)
        except Exception as e:
            print(f"[Crawler Manager] Exception during crawl: {e}", file=sys.stderr)
            q = read_queue()
            for j in q["running"]:
                if j["id"] == job["id"]:
                    q["running"].remove(j)
                    break
            job["status"] = "failed"
            job["updated_at"] = datetime.now().isoformat()
            job["error"] = str(e)
            job["retry_count"] = job.get("retry_count", 0) + 1
            q["failed"].append(job)
            write_queue(q)
            
if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "enqueue":
            for url in sys.argv[2:]:
                enqueue_url(url)
            print("URLs enqueued.")
        elif sys.argv[1] == "process":
            process_queue()
            print("Queue processing finished.")
    else:
        print("Usage: python crawler_manager.py enqueue <url1> <url2>... | process")
