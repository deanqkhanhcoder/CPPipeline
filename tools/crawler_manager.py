import os
import json
import time
import sys
import hashlib
import signal
from datetime import datetime

# Make sure we can import crawl_problem
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from crawl_problem import crawl_problem
from cache_manager import get_problem_id, normalize_url

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
    temp_file = QUEUE_FILE + ".tmp"
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(q, f, indent=2)
    os.replace(temp_file, QUEUE_FILE)

def get_job_id(url):
    norm_url = normalize_url(url)
    return hashlib.md5(norm_url.encode()).hexdigest()[:8]

def enqueue_url(url):
    url = normalize_url(url)
    q = read_queue()
    job_id = get_job_id(url)
    
    # Check if already exists anywhere
    for category in ["pending", "running", "done", "failed"]:
        for job in q[category]:
            if job["url"] == url:
                if category == "failed":
                    # Move from failed to pending, preserving original order_index
                    q["failed"].remove(job)
                    job["status"] = "pending"
                    job["updated_at"] = datetime.now().isoformat()
                    job["retry_count"] = job.get("retry_count", 0)
                    q["pending"].append(job)
                    write_queue(q)
                    return job_id
                else:
                    # If already in pending, running, or done, do nothing
                    return job_id
                    
    order_index = sum(len(q[c]) for c in ["pending", "running", "done", "failed"])
                    
    job = {
        "id": job_id,
        "url": url,
        "order_index": order_index,
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

LOCK_FILE = os.path.join(QUEUE_DIR, "crawler.lock")

def pid_exists(pid):
    if pid <= 0:
        return False
    if sys.platform == "win32":
        import subprocess
        try:
            out = subprocess.check_output(f'tasklist /FI "PID eq {pid}"', shell=True).decode()
            return str(pid) in out
        except Exception:
            return False
    else:
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        else:
            return True

def acquire_lock():
    if os.path.exists(LOCK_FILE):
        try:
            with open(LOCK_FILE, "r") as f:
                pid = int(f.read().strip())
            if pid_exists(pid):
                print(f"[Crawler Manager] Process with PID {pid} is already running. Exiting.", file=sys.stderr)
                return False
        except Exception:
            pass
    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))
    return True

def release_lock():
    if os.path.exists(LOCK_FILE):
        try:
            os.remove(LOCK_FILE)
        except Exception:
            pass

def self_heal_queue():
    q = read_queue()
    if q.get("running"):
        print(f"[Crawler Manager] Self-healing: Moving {len(q['running'])} running jobs back to pending.")
        for job in q["running"]:
            job["status"] = "pending"
            job["updated_at"] = datetime.now().isoformat()
            q["pending"].insert(0, job)
        q["running"] = []
        write_queue(q)

def handle_sigint(signum, frame):
    print("\n[Crawler Manager] SIGINT received. Shutting down gracefully...", file=sys.stderr)
    q = read_queue()
    if q.get("running"):
        for job in q["running"]:
            job["status"] = "pending"
            job["updated_at"] = datetime.now().isoformat()
            q["pending"].insert(0, job)
        q["running"] = []
        write_queue(q)
    try:
        from crawl_problem import PersistentBrowserManager
        PersistentBrowserManager.get_instance().close()
    except Exception:
        pass
    release_lock()
    print("[Crawler Manager] Graceful shutdown complete. Exiting.", file=sys.stderr)
    sys.exit(0)

def process_queue():
    if not acquire_lock():
        return
        
    signal.signal(signal.SIGINT, handle_sigint)
        
    try:
        self_heal_queue()
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
            start_time = time.time()
            try:
                result = crawl_problem(url, order_index=job.get("order_index", 0))
                duration_ms = int((time.time() - start_time) * 1000)
                
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
                    job["html_path"] = f"cache/problemset/{get_problem_id(url)}.json" # Synchronized naming
                    job["error"] = None
                    job["engine_used"] = result.get("engine_used", "Unknown")
                    job["duration_ms"] = duration_ms
                    job["html_length"] = len(result.get("html", ""))
                    q["done"].append(job)
                    print(f"[Crawler Manager] Success: {url} (Engine: {job['engine_used']}, Time: {duration_ms}ms, Size: {job['html_length']} chars)")
                else:
                    job["status"] = "failed"
                    job["updated_at"] = datetime.now().isoformat()
                    job["error"] = result.get("html", "Unknown error") if result else "Crawl failed"
                    job["retry_count"] = job.get("retry_count", 0) + 1
                    job["engine_used"] = result.get("engine_used", "Unknown") if result else "None"
                    job["duration_ms"] = duration_ms
                    job["html_length"] = len(result.get("html", "")) if result else 0
                    q["failed"].append(job)
                    print(f"[Crawler Manager] Failed: {url} (Time: {duration_ms}ms)")
                    
                write_queue(q)
            except Exception as e:
                duration_ms = int((time.time() - start_time) * 1000)
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
                job["engine_used"] = "Exception"
                job["duration_ms"] = duration_ms
                job["html_length"] = 0
                q["failed"].append(job)
                write_queue(q)
    finally:
        try:
            from crawl_problem import PersistentBrowserManager
            PersistentBrowserManager.get_instance().close()
        except Exception:
            pass
        release_lock()
            
if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "enqueue":
            for url in sys.argv[2:]:
                enqueue_url(url)
            print("URLs enqueued.")
        elif sys.argv[1] == "process":
            process_queue()
            print("Queue processing finished.")
        elif sys.argv[1] == "flush":
            init_queue()
            with open(QUEUE_FILE, "w", encoding="utf-8") as f:
                json.dump({
                    "pending": [],
                    "running": [],
                    "done": [],
                    "failed": []
                }, f, indent=2)
            print("Queue flushed successfully. All stale jobs removed.")
    else:
        print("Usage: python crawler_manager.py enqueue <url1> <url2>... | process | flush")
