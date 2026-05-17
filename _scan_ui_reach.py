"""Find UI *_open flags that are never set to True anywhere (= unreachable screens)."""
import re
from pathlib import Path

ROOT = Path(__file__).parent
SKIP_DIRS = {"__pycache__", ".git", ".claude", "memory"}

# 1. Collect every "self.<name>_open = False" declaration (defines the flag exists)
DECL = re.compile(r"self\.([A-Za-z_][A-Za-z0-9_]*_open)\s*=\s*False")
OPEN_RE = re.compile(r"\.([A-Za-z_][A-Za-z0-9_]*_open)\s*=\s*(True\b|not\s)")
READ_RE = re.compile(r"\.([A-Za-z_][A-Za-z0-9_]*_open)\b")

flags = set()
opens = {}   # flag -> list of (file, line)
reads = {}   # flag -> list of (file, line)

for p in ROOT.rglob("*.py"):
    if any(part in SKIP_DIRS for part in p.parts):
        continue
    try:
        text = p.read_text(encoding="utf-8")
    except Exception:
        continue
    for m in DECL.finditer(text):
        flags.add(m.group(1))
    for i, line in enumerate(text.splitlines(), 1):
        for m in OPEN_RE.finditer(line):
            opens.setdefault(m.group(1), []).append((p.relative_to(ROOT), i, line.strip()))
        for m in READ_RE.finditer(line):
            reads.setdefault(m.group(1), []).append((p.relative_to(ROOT), i))

print(f"Total *_open flags declared: {len(flags)}\n")

never_set = sorted(f for f in flags if f not in opens)
print(f"UNREACHABLE ({len(never_set)} flags never set to True):")
for f in never_set:
    # Show whether anything even reads it
    n_reads = len(reads.get(f, []))
    print(f"  {f}   (read in {n_reads} place(s))")
