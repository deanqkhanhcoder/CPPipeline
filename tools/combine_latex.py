import os
import re

files = [f for f in os.listdir(os.path.join("cache", "build")) if f.endswith(".tex")]

template_path = os.path.join(".agents", "skills", "cp-latex", "template.tex")
with open(template_path, "r", encoding="utf-8") as tf:
    template = tf.read()

parts = template.split(r"% TODO: Nội dung bài toán được sinh từ LLM sẽ nằm tại đây")
if len(parts) == 2:
    header = parts[0]
    footer = parts[1]
else:
    print("Error: Could not split template.tex")
    exit(1)

with open("outputs/output.tex", "w", encoding="utf-8") as out:
    out.write(header)
    for f in files:
        file_path = os.path.join("cache", "build", f)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as pf:
                content = pf.read()
                
                # Cleanup hallucinated macros
                content = content.replace(r"\begin{codebg}", "")
                content = content.replace(r"\end{codebg}", "")
                content = content.replace(r"\begin{example}", "")
                content = content.replace(r"\end{example}", "")
                content = content.replace(r"\begin{exmp}", "")
                content = content.replace(r"\end{exmp}", "")
                content = content.replace(r"\begin{exmpIn}", r"\begin{inputbox}")
                content = content.replace(r"\end{exmpIn}", r"\end{inputbox}")
                content = content.replace(r"\begin{exmpOut}", r"\begin{outputbox}")
                content = content.replace(r"\end{exmpOut}", r"\end{outputbox}")
                
                content = content.replace(r"\example", r"\section*{Ví dụ}")
                
                content = re.sub(r"\\exmpin\{([^}]+)\}", r"\\begin{inputbox}\1\\end{inputbox}", content)
                content = re.sub(r"\\exmpout\{([^}]+)\}", r"\\begin{outputbox}\1\\end{outputbox}", content)
                content = re.sub(r"\\exmpinput\{([^}]+)\}", r"\\begin{inputbox}\1\\end{inputbox}", content)
                content = re.sub(r"\\exmpoutput\{([^}]+)\}", r"\\begin{outputbox}\1\\end{outputbox}", content)
                
                # Remove \exmp{...}{...} by falling back to separate boxes
                content = re.sub(r"\\exmp\{([^}]+)\}\{([^}]+)\}", r"\\begin{inputbox}\1\\end{inputbox}\\begin{outputbox}\2\\end{outputbox}", content)
                
                content = content.replace(r"\inputformat", r"\section*{Dữ liệu vào}")
                content = content.replace(r"\outputformat", r"\section*{Dữ liệu ra}")
                content = content.replace(r"\constraints", r"\section*{Giới hạn}")
                
                out.write(content)
                out.write("\n\\newpage\n")
        else:
            out.write(f"\n\\section*{{Lỗi: Thiếu file {f}}}\n")
    out.write(footer)

print("Created output.tex")
