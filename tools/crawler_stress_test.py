import os
import time
import subprocess
import json
import concurrent.futures

# Generate 100 URLs across different OJs
urls = []
# Codeforces (20 URLs)
for i in range(1, 21):
    urls.append(f"https://codeforces.com/problemset/problem/{1500+i}/A")
# AtCoder (20 URLs)
for i in range(1, 21):
    urls.append(f"https://atcoder.jp/contests/abc{200+i}/tasks/abc{200+i}_a")
# CSES (20 URLs)
for i in range(1, 21):
    urls.append(f"https://cses.fi/problemset/task/{1067+i}")
# USACO (15 URLs)
for i in range(1, 16):
    urls.append(f"http://www.usaco.org/index.php?page=viewproblem2&cpid={700+i}")
# Luogu (15 URLs)
for i in range(1, 16):
    urls.append(f"https://www.luogu.com.cn/problem/P{1000+i}")
# HDU (5 URLs)
for i in range(1, 6):
    urls.append(f"https://acm.hdu.edu.cn/showproblem.php?pid={1000+i}")
# Kattis (5 URLs)
kattis_problems = ["hello", "different", "r2", "carrots", "autori"]
for p in kattis_problems:
    urls.append(f"https://open.kattis.com/problems/{p}")

total_urls = len(urls)
print(f"Starting Stress Test on {total_urls} URLs...")

results = {
    "total": total_urls,
    "success": 0,
    "failure": 0,
    "runtimes": [],
    "failures": []
}

def crawl_url(url):
    start_time = time.time()
    try:
        # Run crawler
        # The crawler outputs JSON to stdout
        process = subprocess.run(
            ["python", "tools/crawl_problem.py", url],
            capture_output=True,
            text=True,
            timeout=30
        )
        runtime = time.time() - start_time
        
        if process.returncode == 0 and process.stdout.strip().startswith("{"):
            try:
                data = json.loads(process.stdout)
                if "html" in data and "markdown" in data:
                    return {"url": url, "success": True, "runtime": runtime}
            except:
                pass
        
        # Failure case
        err_msg = process.stderr.strip() if process.stderr else "Invalid output or Timeout"
        return {"url": url, "success": False, "runtime": runtime, "error": err_msg}
    except Exception as e:
        return {"url": url, "success": False, "runtime": time.time() - start_time, "error": str(e)}

# We run with max_workers=5 to avoid DDOSing OJs and getting rate limited heavily immediately,
# but enough to test concurrency.
start_total = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futures = {executor.submit(crawl_url, url): url for url in urls}
    for future in concurrent.futures.as_completed(futures):
        res = future.result()
        if res["success"]:
            results["success"] += 1
            print(f"[OK] {res['url']} ({res['runtime']:.2f}s)")
        else:
            results["failure"] += 1
            results["failures"].append({"url": res["url"], "error": res["error"]})
            print(f"[FAIL] {res['url']} - {res['error']}")
        results["runtimes"].append(res["runtime"])

total_time = time.time() - start_total
results["total_time"] = total_time
results["average_runtime"] = sum(results["runtimes"]) / len(results["runtimes"]) if results["runtimes"] else 0

os.makedirs("reports", exist_ok=True)
with open("reports/stress_test_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("\n--- STRESS TEST COMPLETE ---")
print(f"Success: {results['success']}/{results['total']}")
print(f"Failure: {results['failure']}/{results['total']}")
print(f"Avg Runtime: {results['average_runtime']:.2f}s")
print("Detailed results saved to reports/stress_test_results.json")
