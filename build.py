import sys
with open('cache/build/2fd58e15.tex', 'r', encoding='utf-8') as f:
    content = f.read()

problem_text = r"""\problem{D. Max Median}{Codeforces}

Bạn được cho một mảng $a$ có độ dài $n$. Hãy tìm một mảng con $a[l..r]$ có độ dài ít nhất $k$ với phần tử trung vị lớn nhất.

Phần tử trung vị trong một mảng độ dài $n$ là phần tử nằm ở vị trí thứ $\lfloor \frac{n + 1}{2} \rfloor$ sau khi ta sắp xếp các phần tử theo thứ tự không giảm. Ví dụ: $median([1, 2, 3, 4]) = 2$, $median([3, 2, 1]) = 2$, $median([2, 1, 2, 1]) = 1$.

Mảng con $a[l..r]$ là một phần liên tiếp của mảng $a$, tức là dãy $a_l, a_{l+1}, \ldots, a_r$ với $1 \leq l \leq r \leq n$, và độ dài của nó là $r - l + 1$.

\inputformat
Dòng đầu tiên chứa hai số nguyên $n$ và $k$ ($1 \leq k \leq n \leq 2 \cdot 10^5$).

Dòng thứ hai chứa $n$ số nguyên $a_1, a_2, \ldots, a_n$ ($1 \leq a_i \leq n$).

\outputformat
In ra một số nguyên $m$ — phần tử trung vị lớn nhất bạn có thể đạt được.

\constraints
\begin{constraintbox}
\begin{itemize}[leftmargin=*]
    \item $1 \leq k \leq n \leq 2 \cdot 10^5$
    \item $1 \leq a_i \leq n$
\end{itemize}
\end{constraintbox}

\example
\textbf{Sample 1}
\begin{inputbox}
\begin{verbatim}
5 3
1 2 3 2 1
\end{verbatim}
\end{inputbox}
\begin{outputbox}
\begin{verbatim}
2
\end{verbatim}
\end{outputbox}

\textbf{Sample 2}
\begin{inputbox}
\begin{verbatim}
4 2
1 2 3 4
\end{verbatim}
\end{inputbox}
\begin{outputbox}
\begin{verbatim}
3
\end{verbatim}
\end{outputbox}

\explanation
Trong ví dụ đầu tiên, tất cả các mảng con có thể là $[1..3]$, $[1..4]$, $[1..5]$, $[2..4]$, $[2..5]$ và $[3..5]$. Trung vị của tất cả chúng đều là $2$, vì vậy trung vị lớn nhất có thể đạt được cũng là $2$.

Trong ví dụ thứ hai, $median([3..4]) = 3$.
"""

with open('.agents/skills/cp-latex/template.tex', 'r', encoding='utf-8') as f:
    template = f.read()

template = template.replace('% TODO: Nội dung bài toán được sinh từ LLM sẽ nằm tại đây', problem_text)

with open('cache/build/2fd58e15.tex', 'w', encoding='utf-8') as f:
    f.write(template)
