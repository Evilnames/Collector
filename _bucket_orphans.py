"""Bucket the orphan list by common prefix for the cleanup report."""
import re
from pathlib import Path
from collections import defaultdict

raw = Path("planning/_items_raw.txt").read_text(encoding="utf-8")

orphans = []
suspicious = []
mode = None
for line in raw.splitlines():
    if "ORPHAN ITEMS" in line:
        mode = "orphan"; continue
    if "ONLY-1-REFERENCE" in line:
        mode = "susp"; continue
    m = re.match(r"\s+'([^']+)'\s+(?:in\s+\S+\s+)?\"([^\"]+)\"", line)
    if not m: continue
    key, name = m.group(1), m.group(2)
    if mode == "orphan":
        orphans.append((key, name))
    elif mode == "susp":
        suspicious.append((key, name))

def bucket(items):
    b = defaultdict(list)
    for k, n in items:
        prefix = k.split("_", 1)[0]
        b[prefix].append((k, n))
    return b

ob = bucket(orphans)
sb = bucket(suspicious)

out = []
out.append(f"# Orphan items by prefix ({len(orphans)} total)\n")
for prefix, lst in sorted(ob.items(), key=lambda kv: -len(kv[1])):
    out.append(f"\n## `{prefix}_*` — {len(lst)} item(s)\n")
    for k, n in sorted(lst):
        out.append(f"- `{k}` — {n}")

out.append(f"\n\n# Only-one-reference items by prefix ({len(suspicious)} total)\n")
for prefix, lst in sorted(sb.items(), key=lambda kv: -len(kv[1])):
    out.append(f"\n## `{prefix}_*` — {len(lst)} item(s)")
    if len(lst) > 25:
        out.append(f"(showing first 25)")
        lst = sorted(lst)[:25]
    for k, n in sorted(lst):
        out.append(f"- `{k}` — {n}")

Path("planning/_orphan_buckets.md").write_text("\n".join(out), encoding="utf-8")
print(f"Wrote {len(out)} lines to planning/_orphan_buckets.md")
print(f"Orphan prefix counts: {sorted([(p, len(l)) for p,l in ob.items()], key=lambda x:-x[1])[:15]}")
