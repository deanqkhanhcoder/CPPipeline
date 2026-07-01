import os
import re
import sys
from pathlib import Path

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

def normalize_latex_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Merge lines that were incorrectly wrapped (single newlines not followed by a blank line or command)
        # Actually, LaTeX does this automatically. But let's fix spacing around punctuation.
        content = re.sub(r'\s+([.,!?:;])', r'\1', content) # Remove space before punctuation
        content = re.sub(r'([.,!?:;])(?=[a-zA-Záàảãạăắằẳẵặâấầẩẫậđéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ])', r'\1 ', content) # Ensure space after punctuation (ignoring numbers)
        
        # 2. Fix inline bullet points that are joined together: " - step 1 - step 2"
        # We find occurrences of " - " or " * " inside text and break them into newlines
        content = re.sub(r'(?<=\w)\s+[-*•]\s+(?=\w)', r'\n- ', content)
        
        # 3. List Normalization: Convert markdown lists to itemize if they missed Phase 6
        # Find consecutive lines starting with - or * and wrap them
        def list_replacer(match):
            items = match.group(0).strip().split('\n')
            latex_items = []
            for item in items:
                clean_item = re.sub(r'^[-*•]\s*', '', item.strip())
                latex_items.append(f"  \\item {clean_item}")
            return "\\begin{itemize}\n" + "\n".join(latex_items) + "\n\\end{itemize}\n"
            
        content = re.sub(r'(?:^|\n)([-*•]\s+[^\n]+(?:\n[-*•]\s+[^\n]+)*)', list_replacer, content)

        # 4. Remove residual markdown headers like "### " or "**"
        content = re.sub(r'^#{1,6}\s*(.*?)$', r'\\textbf{\1}', content, flags=re.MULTILINE)
        content = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', content)
        content = re.sub(r'\*(.*?)\*', r'\\textit{\1}', content)

        # 5. Fix multiple consecutive blank lines
        content = re.sub(r'\n{3,}', r'\n\n', content)

        # 6. Ensure Example / Constraint boxes don't have trailing/leading massive whitespace
        content = re.sub(r'\\begin{inputbox}\s+', r'\\begin{inputbox}\n', content)
        content = re.sub(r'\s+\\end{inputbox}', r'\n\\end{inputbox}', content)
        content = re.sub(r'\\begin{outputbox}\s+', r'\\begin{outputbox}\n', content)
        content = re.sub(r'\s+\\end{outputbox}', r'\n\\end{outputbox}', content)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[Normalizer] Normalized {file_path.name}")
        return True
    except Exception as e:
        print(f"[Normalizer] Error processing {file_path.name}: {e}", file=sys.stderr)
        return False

def main():
    build_dir = Path(__file__).resolve().parents[1] / "cache" / "build"
    if not build_dir.exists():
        print("[Normalizer] No build directory found.")
        return
        
    tex_files = list(build_dir.glob("*.tex"))
    for tf in tex_files:
        # Don't normalize output.tex itself directly since we normalize build fragments
        if tf.name != "output.tex":
            normalize_latex_file(tf)

if __name__ == "__main__":
    main()
