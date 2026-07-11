import os
import json
import subprocess
import sys
import shutil
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    print("Running Order Preservation Regression Test...")
    
    # Setup directories
    queue_dir = ROOT / "cache" / "queue"
    queue_dir.mkdir(parents=True, exist_ok=True)
    build_dir = ROOT / "cache" / "build"
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Enqueue A, B, C, D in order
    q = {
        "pending": [],
        "running": [],
        "done": [
            {"id": "A", "url": "URL_A", "order_index": 0, "status": "done"},
            {"id": "B", "url": "URL_B", "order_index": 1, "status": "done"},
            {"id": "C", "url": "URL_C", "order_index": 2, "status": "done"},
            {"id": "D", "url": "URL_D", "order_index": 3, "status": "done"}
        ],
        "failed": []
    }
    
    with open(queue_dir / "index.json", "w", encoding="utf-8") as f:
        json.dump(q, f, indent=2)
        
    print("Enqueued URLs: URL_A (0), URL_B (1), URL_C (2), URL_D (3)")
    
    # 2. Mock completion out of order (B, D, C, A)
    # We name files in reverse alphabetical order so that string sort would fail
    # A -> Z_A.tex (0)
    # B -> Y_B.tex (1)
    # C -> X_C.tex (2)
    # D -> W_D.tex (3)
    
    completion_order = [
        ("Y_B.tex", 1, "B", "URL_B", 1),
        ("W_D.tex", 3, "D", "URL_D", 2),
        ("X_C.tex", 2, "C", "URL_C", 5),
        ("Z_A.tex", 0, "A", "URL_A", 10),
    ]
    
    for filename, order_idx, title, url, delay in completion_order:
        time.sleep(0.1) # Simulate delay
        content = f"% order_index: {order_idx}\n\\problem{{{title}}}{{{url}}}\n\\inputformat\nInput format for {title}.\n\\outputformat\nOutput format for {title}.\n\\example\nExample for {title}.\n\\explanation\nExplanation for {title}.\n"
        (build_dir / filename).write_text(content, encoding="utf-8")
        print(f"Mock completion: {title} (Delay {delay}s, File: {filename})")
        
    # 3. Combine LaTeX
    print("Combining LaTeX...")
    res = subprocess.run([sys.executable, "tools/combine_latex.py"], cwd=str(ROOT), capture_output=True, text=True)
    if res.returncode != 0:
        print("FAIL: combine_latex.py failed!")
        print(res.stderr)
        return 1
        
    # 4. Check outputs/output.tex
    output_tex = ROOT / "outputs" / "output.tex"
    content = output_tex.read_text(encoding="utf-8")
    
    # 5. Run validate_order.py
    print("Validating order...")
    res2 = subprocess.run([sys.executable, "tools/validate_order.py"], cwd=str(ROOT), capture_output=True, text=True)
    if res2.returncode != 0:
        print("FAIL: validate_order.py failed!")
        print(res2.stdout)
        print(res2.stderr)
        return 1
        
    if "PASS" not in res2.stdout:
        print("FAIL: Validation did not output PASS.")
        return 1
        
    print("STRESS TEST PASS: Order successfully preserved despite parallel reordering!")
    
    # Cleanup to avoid failing validate_toc.py
    if output_tex.exists():
        output_tex.unlink()
    if (ROOT / "cache" / "queue" / "index.json").exists():
        (ROOT / "cache" / "queue" / "index.json").unlink()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
