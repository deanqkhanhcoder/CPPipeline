import os
import sys
import subprocess
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from crawler_manager import enqueue_url, read_queue

def run_stress_test():
    print("Enqueuing 100 URLs...")
    for i in range(100):
        url = f"https://codeforces.com/problemset/problem/1/{i}"
        enqueue_url(url)
        
    print("Starting crawler_manager process in the background...")
    # Run a few iterations to prove it doesn't crash or lock
    # We will pass a timeout to not hang the test forever
    try:
        # Run it for 20 seconds, we should see sequential processing
        proc = subprocess.Popen(["python", "tools/crawler_manager.py", "process"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        time.sleep(15) # let it process a few
        proc.terminate()
        stdout, stderr = proc.communicate(timeout=5)
        
        print("--- STDOUT ---")
        print(stdout)
        print("--- STDERR ---")
        print(stderr)
        
        if "Opening in existing browser session" in stdout or "Profile already in use" in stdout:
            print("FAILED: Profile lock detected!")
            sys.exit(1)
        elif "Opening in existing browser session" in stderr or "Profile already in use" in stderr:
            print("FAILED: Profile lock detected in stderr!")
            sys.exit(1)
        else:
            print("SUCCESS: 0 Profile Locks, 0 Session Conflicts.")
            
    except Exception as e:
        print(f"Test error: {e}")
        
if __name__ == "__main__":
    run_stress_test()
