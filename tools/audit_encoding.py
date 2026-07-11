import os
import re
import sys
from pathlib import Path

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stdin.encoding.lower() != 'utf-8':
    sys.stdin.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]

# Excluded paths
EXCLUDE_DIRS = {".git", "__pycache__", "node_modules", ".venv", "env", "cache", "archive", "reports"}
EXCLUDE_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".gif", ".ico", ".bin", ".keep", ".zip", ".tar", ".gz"}
# We audit source files and output files, but exclude binary caches and the tools themselves
EXCLUDE_FILES = {"template_hash.txt", "audit_encoding.py", "repair_encoding.py", "encoding_audit.md", "repository_cleanup_audit.md"}

# Regex patterns
# 1. Question mark adjacent to a letter but not part of a URL or standard punctuation.
CORRUPTED_VIETNAMESE = re.compile(r"(?<!https)(?<!http)(?<![:/.=])\b([a-zA-Z]+\?[a-zA-Z]*|[a-zA-Z]*\?[a-zA-Z]+)\b(?!=)")
# 2. Three or more consecutive question marks (e.g. ???c or placeholder ???)
TRIPLE_QUESTION = re.compile(r"\?\?\?")
# 3. Unicode replacement character (indicating decoding fallback happened somewhere)
REPLACEMENT_CHAR = re.compile(r"\ufffd")
# 4. Common Mojibake patterns (e.g., Ã followed by a byte, typical of double-encoded UTF-8 in cp1252)
# e.g., Ã¡, Ã¢, Ã£, Ã², Ã³, Ã´, Ã¹, Ãº, Ä‘
MOJIBAKE = re.compile(r"Ã[¡¢£¤¥¦§¨©ª«®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ]")

def audit_file(path: Path) -> list[str]:
    violations = []
    
    # Read as raw bytes to check if it's valid UTF-8
    try:
        content_bytes = path.read_bytes()
    except Exception as e:
        return [f"Failed to read file bytes: {e}"]
        
    try:
        content = content_bytes.decode("utf-8")
    except UnicodeDecodeError as e:
        violations.append(f"Invalid UTF-8 encoding: {e}")
        # Try to decode with replacement to run other checks
        content = content_bytes.decode("utf-8", errors="replace")
        
    # Check for replacement characters
    if REPLACEMENT_CHAR.search(content):
        violations.append("Contains Unicode replacement character (\\ufffd)")
        
    # Check for corrupted Vietnamese (literal ? adjacent to letters)
    is_generated_tex = path.suffix.lower() == '.tex' and path.name != 'template.tex'
    
    corrupted_matches = list(CORRUPTED_VIETNAMESE.finditer(content))
    if corrupted_matches and is_generated_tex:
        # Show some context
        for match in corrupted_matches[:3]:
            start = max(0, match.start() - 15)
            end = min(len(content), match.end() + 15)
            context = content[start:end].replace("\n", " ")
            violations.append(f"Corrupted Vietnamese: '{context.strip()}'")
            
    # Check for '???'
    if TRIPLE_QUESTION.search(content):
        # Allow it if it's explicitly part of a comment/code pattern we don't care about,
        # but in this repository it's almost always a sign of corruption (e.g., ???c).
        # Let's flag it.
        triple_matches = list(TRIPLE_QUESTION.finditer(content))
        for match in triple_matches[:3]:
            start = max(0, match.start() - 15)
            end = min(len(content), match.end() + 15)
            context = content[start:end].replace("\n", " ")
            violations.append(f"Contains '???': '{context.strip()}'")

    # Check for mojibake
    mojibake_matches = list(MOJIBAKE.finditer(content))
    if mojibake_matches:
        for match in mojibake_matches[:3]:
            start = max(0, match.start() - 15)
            end = min(len(content), match.end() + 15)
            context = content[start:end].replace("\n", " ")
            violations.append(f"Mojibake detected: '{context.strip()}'")

    return violations

def main() -> int:
    all_violations = {}
    
    for root, dirs, files in os.walk(ROOT):
        # Exclude directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            file_path = Path(root) / file
            
            # Skip by extension
            if file_path.suffix.lower() in EXCLUDE_EXTENSIONS:
                continue
            # Skip by file name
            if file_path.name in EXCLUDE_FILES:
                continue
                
            # Skip if file is inside .agents/skills but not a code/text file we audit,
            # actually we should audit markdown and tex in skills too.
            # Let's audit all .py, .tex, .json, .md, .txt
            if file_path.suffix.lower() not in {".py", ".tex", ".json", ".md", ".txt"}:
                continue
                
            rel_path = file_path.relative_to(ROOT)
            violations = audit_file(file_path)
            if violations:
                all_violations[str(rel_path)] = violations
                
    if all_violations:
        print("=== ENCODING AUDIT FAILURE ===")
        for path, violations in all_violations.items():
            print(f"\nFile: {path}")
            for v in violations:
                print(f"  - {v}")
        return 1
        
    print("Encoding audit passed. All files are valid UTF-8 and clean.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
