import re
import shutil
import subprocess
import sys
from pathlib import Path

GOOD = r"""% order_index: {i}
\problem{{B?i {i} (Problem {i})}}{{Fixture}}
N?i dung.
\inputformat
M?t d?ng.
\outputformat
M?t d?ng.
\constraints
$1 \le n \le 10$.
\endconstraints
\example
\begin{{lstlisting}}
1
\end{{lstlisting}}
\explanation
H?p l?.
"""

def test_100_fragments_validate():
    import tempfile
    tmp_path = Path(tempfile.mkdtemp())
    for i in range(100):
        (tmp_path / f"{i:03}.tex").write_text(GOOD.format(i=i), encoding="utf-8")
    res = subprocess.run([sys.executable, "tools/fragment_qa.py", str(tmp_path)], capture_output=True, text=True)
    assert res.returncode == 0, res.stderr

if __name__ == "__main__":
    test_100_fragments_validate()
    print("PASS")
