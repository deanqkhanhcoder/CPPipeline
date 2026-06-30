# LaTeX Layout Fix Report

## Bug Description

`inputbox` và `outputbox` bị dư khoảng trắng rất lớn phía dưới khi chứa `lstlisting`.

## Root Cause Analysis

### Thành phần sinh khoảng trắng (theo thứ tự từ ngoài vào)

| Layer | Property | Giá trị | Tác động |
|-------|----------|---------|---------|
| `mdframed` (inputbox) | `innertopmargin` | 4pt | Padding trên |
| `mdframed` (inputbox) | `innerbottommargin` | 4pt | Padding dưới |
| `lstlisting` | `aboveskip` | 6pt | Spacing trên bên trong mdframed |
| `lstlisting` | `belowskip` | 6pt | Spacing dưới bên trong mdframed |
| List environment | `\topsep` + `\partopsep` | ~10-12pt | **Ẩn** — LaTeX tự thêm vì lstlisting là list env |

### Kết quả cộng gộp

Total whitespace = innerbottommargin(4) + belowskip(6) + topsep(~6) + partopsep(~4) = ~20pt (~7mm dư)

### Tại sao `lstlisting` gây ra `\topsep`?

`lstlisting` trong LaTeX được implement dưới dạng một **list environment** (trivlist). Mọi list env đều tự thêm `\topsep + \partopsep` ở đầu và cuối. Khi đặt trong `mdframed`, spacing này chồng lên padding của frame.

## Final Patch (Đã áp dụng)

Tạo environment `samplecode` riêng biệt, chỉ dùng cho Input/Output samples:

```latex
\lstnewenvironment{samplecode}{%
  \lstset{
    backgroundcolor=\color{white},
    frame=none,        % Không frame — inputbox đã có frame rồi
    aboveskip=0pt,     % Triệt tiêu spacing trên
    belowskip=0pt,     % Triệt tiêu spacing dưới
    xleftmargin=0pt,
    xrightmargin=0pt,
    framesep=0pt,
  }%
}{}
```

**Usage đúng trong body LaTeX:**
```latex
\begin{inputbox}
\begin{samplecode}
3 2
1 2 3
\end{samplecode}
\end{inputbox}
```

## Verification

Compile test thành công: `Compilation successful using pdflatex.`

## Luật chống đứt gãy

**Đã ghi vào `cp-latex/SKILL.md` Rule 4:**
> Khi viết ví dụ đầu vào/đầu ra trong inputbox/outputbox, phải dùng `samplecode` thay vì `lstlisting`.
