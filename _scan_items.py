"""Find items defined in ITEMS that the player likely cannot obtain.

items.py uses string keys (e.g. "dirt_clump"). For each key, count occurrences
across the codebase outside items.py itself. Items with very few external
references are likely orphans — defined but never produced as a recipe output,
drop, NPC sell, or anything else.
"""
import ast, re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent
SKIP_DIRS = {"__pycache__", ".git", ".claude", "memory"}

_OUT = []
items_py = ROOT / "items.py"
text = items_py.read_text(encoding="utf-8")

# Parse the ITEMS dict and pull out string keys
tree = ast.parse(text)
keys = []  # ordered list of (key, display_name)
display = {}

for node in ast.walk(tree):
    if isinstance(node, ast.Assign):
        for tgt in node.targets:
            if isinstance(tgt, ast.Name) and tgt.id == "ITEMS" and isinstance(node.value, ast.Dict):
                for k, v in zip(node.value.keys, node.value.values):
                    if isinstance(k, ast.Constant) and isinstance(k.value, str):
                        key = k.value
                        keys.append(key)
                        # try to find name
                        if isinstance(v, ast.Dict):
                            for sk, sv in zip(v.keys, v.values):
                                if isinstance(sk, ast.Constant) and sk.value == "name" \
                                        and isinstance(sv, ast.Constant):
                                    display[key] = sv.value

_OUT.append(f"Parsed {len(keys)} item keys from ITEMS dict.\n")

# Now count occurrences of each string key as a quoted literal in all other .py files
py_files = [p for p in ROOT.rglob("*.py")
            if not any(part in SKIP_DIRS for part in p.parts)
            and p.name != "items.py"
            and not p.name.startswith("_scan_")
            and not p.name.startswith("test_")]

# Build one big regex matching any of the keys as a quoted string: "key" or 'key'
# To stay performant, batch.
counts = defaultdict(int)
locations = defaultdict(set)
key_set = set(keys)

# Use a single regex of quoted strings, then look up
QUOTED = re.compile(r"""['"]([a-z][a-z0-9_\-]*)['"]""")
# Detect dynamic key construction: f"prefix_{...}..." — captures the literal prefix.
FSTRING_PREFIX = re.compile(r"""f['"]([a-z][a-z0-9_]+_)\{""")

dynamic_prefixes = set()
for p in py_files:
    try:
        body = p.read_text(encoding="utf-8")
    except Exception:
        continue
    for m in QUOTED.finditer(body):
        k = m.group(1)
        if k in key_set:
            counts[k] += 1
            locations[k].add(p.relative_to(ROOT).as_posix())
    for m in FSTRING_PREFIX.finditer(body):
        dynamic_prefixes.add((m.group(1), p.relative_to(ROOT).as_posix()))

# Any item key starting with a dynamic prefix is considered "produced".
for k in keys:
    for prefix, loc in dynamic_prefixes:
        if k.startswith(prefix):
            counts[k] = max(counts[k], 1)  # at least one ref
            locations[k].add(f"{loc} (f-string)")
            break

orphans = sorted(k for k in keys if counts[k] == 0)
suspicious = sorted((k for k in keys if counts[k] == 1), key=lambda k: counts[k])

_OUT.append(f"== ORPHAN ITEMS (key never referenced outside items.py): {len(orphans)} ==")
for k in orphans:
    _OUT.append(f"  {k!r:32s}  \"{display.get(k, '?')}\"")

_OUT.append(f"\n== ONLY-1-REFERENCE ITEMS: {len(suspicious)} ==")
for k in suspicious:
    loc = next(iter(locations[k]))
    _OUT.append(f"  {k!r:32s}  in {loc:40s}  \"{display.get(k, '?')}\"")

import sys
out_path = Path(sys.argv[1]) if len(sys.argv) > 1 else None
text_out = "\n".join(str(x) for x in _OUT)
if out_path:
    out_path.write_text(text_out, encoding="utf-8")
else:
    print(text_out)
