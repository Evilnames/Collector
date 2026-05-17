"""Find Python modules in this repo that are never reached from main.py."""
import ast, os, sys
from pathlib import Path

ROOT = Path(__file__).parent
SKIP_DIRS = {"__pycache__", ".git", ".claude", "memory"}

def all_modules():
    mods = {}
    for p in ROOT.rglob("*.py"):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        rel = p.relative_to(ROOT).with_suffix("")
        parts = rel.parts
        # __init__.py represents the package itself
        if parts[-1] == "__init__":
            parts = parts[:-1]
            if not parts:
                continue
        modname = ".".join(parts)
        mods[modname] = p
    return mods

def imports_of(path):
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except Exception:
        return set()
    # package path of this file (e.g. UI/panels.py -> ("UI",))
    rel = path.relative_to(ROOT).with_suffix("")
    pkg_parts = rel.parts[:-1] if rel.parts[-1] != "__init__" else rel.parts[:-1]
    out = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                out.add(n.name.split(".")[0])
                out.add(n.name)
        elif isinstance(node, ast.ImportFrom):
            if node.level:  # relative import
                base = list(pkg_parts[: len(pkg_parts) - (node.level - 1)] if node.level > 1 else pkg_parts)
                if node.module:
                    base.append(node.module)
                if base:
                    out.add(".".join(base))
                    out.add(base[0])
                # named symbols may themselves be submodules
                for n in node.names:
                    if base:
                        out.add(".".join(base + [n.name]))
            elif node.module:
                out.add(node.module.split(".")[0])
                out.add(node.module)
                for n in node.names:
                    out.add(f"{node.module}.{n.name}")
    return out

def main():
    mods = all_modules()
    # Build name -> path lookup (try both full dotted and leaf basename)
    name_to_path = {}
    for modname, p in mods.items():
        name_to_path[modname] = p
        leaf = modname.split(".")[-1]
        name_to_path.setdefault(leaf, p)

    # BFS from main
    start = ROOT / "main.py"
    reached = set()
    stack = [start]
    while stack:
        cur = stack.pop()
        if cur in reached:
            continue
        reached.add(cur)
        for imp in imports_of(cur):
            tgt = name_to_path.get(imp)
            if tgt and tgt not in reached:
                stack.append(tgt)

    all_paths = set(mods.values())
    orphans = sorted(all_paths - reached, key=lambda p: str(p))
    print(f"Reached from main.py: {len(reached)}")
    print(f"Total .py files:      {len(all_paths)}")
    print(f"ORPHANS ({len(orphans)}):")
    for p in orphans:
        print(f"  {p.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
