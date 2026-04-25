#!/usr/bin/env python3
"""
new_block.py — Scaffold a new block in CollectorBlocks.

Usage:
    python generator/new_block.py decorative "Marble Tile"  "200,195,185"
    python generator/new_block.py equipment  "Salt Kiln"    "140,120,100"
    python generator/new_block.py ore        "Tin Ore"      "180,170,160"

Options:
    --hardness N    Mining hardness (default: 1 for decorative/equipment, 4 for ore)
    --drop ID       Drop item ID. Use "none" for no drop.
                    Ore default: <name>_chunk. Decorative/equipment default: <name> item.
    --comment TEXT  Short comment appended to the ID constant line.
    --dry-run       Print what would be written without touching files.

Writes:
    blocks.py   — ID constant, BLOCKS entry, set membership
    items.py    — item entry + extends blocks import
    crafting.py — ARTISAN_RECIPES placeholder (decorative/equipment only)

Prints remaining manual steps at the end.
"""

import argparse
import re
import sys
from pathlib import Path

ROOT        = Path(__file__).parent.parent
BLOCKS_PY   = ROOT / "blocks.py"
ITEMS_PY    = ROOT / "items.py"
CRAFTING_PY = ROOT / "crafting.py"

IMPORT_INDENT = " " * 20   # indentation used in items.py "from blocks import (...)"
SET_INDENT    = " " * 20   # indentation used in EQUIPMENT_BLOCKS / RESOURCE_BLOCKS


# ── Name helpers ───────────────────────────────────────────────────────────────

def to_const(name: str) -> str:
    """'Marble Tile' → 'MARBLE_TILE'"""
    return re.sub(r"\W+", "_", name.strip()).upper().strip("_")

def to_id(name: str) -> str:
    """'Marble Tile' → 'marble_tile'"""
    return re.sub(r"\W+", "_", name.strip()).lower().strip("_")

def fmt_color(c: tuple) -> str:
    return f"({c[0]:3d}, {c[1]:3d}, {c[2]:3d})"

def parse_color(s: str) -> tuple:
    parts = [int(x.strip()) for x in s.split(",")]
    if len(parts) != 3:
        raise ValueError(f"color must be R,G,B — got {s!r}")
    return tuple(parts)


# ── Brace / bracket matching ───────────────────────────────────────────────────

def _find_matching(text: str, open_pos: int, open_ch: str, close_ch: str) -> int:
    """Return index of the character that closes the brace/bracket at open_pos."""
    if text[open_pos] != open_ch:
        raise ValueError(f"Expected {open_ch!r} at position {open_pos}, got {text[open_pos]!r}")
    depth = 0
    for i in range(open_pos, len(text)):
        if text[i] == open_ch:
            depth += 1
        elif text[i] == close_ch:
            depth -= 1
            if depth == 0:
                return i
    raise ValueError(f"No matching {close_ch!r} for {open_ch!r} at position {open_pos}")

def _dict_close(text: str, dict_name: str) -> int:
    """Return index of the '}' that closes 'NAME = {' at module level."""
    m = re.search(rf"^{re.escape(dict_name)} *= *\{{", text, re.MULTILINE)
    if not m:
        raise ValueError(f"Cannot find '{dict_name} = {{' in file")
    brace_pos = m.end() - 1
    return _find_matching(text, brace_pos, "{", "}")

def _list_close(text: str, list_name: str) -> int:
    """Return index of the ']' that closes 'NAME = [' at module level."""
    m = re.search(rf"^{re.escape(list_name)} *= *\[", text, re.MULTILINE)
    if not m:
        raise ValueError(f"Cannot find '{list_name} = [' in file")
    bracket_pos = m.end() - 1
    return _find_matching(text, bracket_pos, "[", "]")

def _set_close(text: str, set_name: str) -> int:
    """Return index of the '}' that closes 'SET_NAME = {' at module level."""
    m = re.search(rf"^{re.escape(set_name)}\b[^{{]*\{{", text, re.MULTILINE | re.DOTALL)
    if not m:
        raise ValueError(f"Cannot find set {set_name!r} in file")
    brace_pos = m.end() - 1
    return _find_matching(text, brace_pos, "{", "}")

def _import_close(text: str) -> int:
    """Return index of the ')' that closes 'from blocks import ('."""
    m = re.search(r"^from blocks import \(", text, re.MULTILINE)
    if not m:
        return -1
    paren_pos = m.end() - 1
    return _find_matching(text, paren_pos, "(", ")")


# ── blocks.py mutations ────────────────────────────────────────────────────────

def next_block_id(text: str) -> int:
    ids = [int(v) for v in re.findall(r"^[A-Z][A-Z_0-9]* *= *(\d+)", text, re.MULTILINE)]
    if not ids:
        raise ValueError("No block ID constants found in blocks.py")
    return max(ids) + 1

def insert_id_constant(text: str, const: str, bid: int, comment: str) -> str:
    pos = text.find("\nBLOCKS = {")
    if pos == -1:
        raise ValueError("blocks.py: cannot find 'BLOCKS = {'")
    line = f"\n{const:<28} = {bid}  # {comment}"
    return text[:pos] + line + text[pos:]

def insert_blocks_entry(text: str, const: str, name: str, hardness, color: tuple, drop) -> str:
    drop_s = f'"{drop}"' if drop else "None"
    pad    = max(1, 26 - len(const))
    entry  = f'    {const}:{" " * pad}{{"name": "{name}", "hardness": {hardness}, "color": {fmt_color(color)}, "drop": {drop_s}}},\n'
    close  = _dict_close(text, "BLOCKS")
    return text[:close] + entry + text[close:]

def append_to_set(text: str, set_name: str, const: str) -> str:
    close = _set_close(text, set_name)
    return text[:close] + f",\n{SET_INDENT}{const}" + text[close:]


# ── items.py mutations ─────────────────────────────────────────────────────────

def insert_item(text: str, item_id: str, name: str, color: tuple, place_block) -> str:
    pb    = place_block if place_block else "None"
    pad   = max(1, 26 - len(item_id) - 2)   # -2 for surrounding quotes
    entry = f'    "{item_id}":{" " * pad}{{"name": "{name}", "color": {fmt_color(color)}, "place_block": {pb}}},\n'
    close = _dict_close(text, "ITEMS")
    text  = text[:close] + entry + text[close:]
    if place_block and place_block != "None":
        text = _extend_blocks_import(text, place_block)
    return text

def _extend_blocks_import(text: str, const: str) -> str:
    close = _import_close(text)
    if close == -1:
        return text   # no import block — skip silently
    return text[:close] + f",\n{IMPORT_INDENT}{const}" + text[close:]


# ── crafting.py mutations ──────────────────────────────────────────────────────

def insert_artisan_recipe(text: str, item_id: str, name: str) -> str:
    entry = (
        f'    {{"name": "{name}", '
        f'"ingredients": {{"stone_chip": 2}}, '
        f'"output_id": "{item_id}", "output_count": 2}},\n'
    )
    close = _list_close(text, "ARTISAN_RECIPES")
    return text[:close] + entry + text[close:]


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="Scaffold a new block in CollectorBlocks")
    ap.add_argument("type",    choices=["decorative", "equipment", "ore"])
    ap.add_argument("name",    help='Display name e.g. "Marble Tile"')
    ap.add_argument("color",   help="RGB as R,G,B e.g. 200,195,185")
    ap.add_argument("--hardness", type=float, default=None)
    ap.add_argument("--drop",     default=None,
                    help="Drop item ID. 'none' = no drop. Ore default: <name>_chunk.")
    ap.add_argument("--comment",  default=None)
    ap.add_argument("--dry-run",  action="store_true")
    args = ap.parse_args()

    color   = parse_color(args.color)
    btype   = args.type
    name    = args.name
    comment = args.comment or name.lower()

    # Derive identifiers
    base = to_const(name)
    if btype == "equipment" and not base.endswith("_BLOCK"):
        const = base + "_BLOCK"
    elif btype == "ore" and not (base.endswith("_ORE") or base.endswith("_DEPOSIT")):
        const = base + "_ORE"
    else:
        const = base

    item_id  = to_id(name)
    hardness = args.hardness if args.hardness is not None else (4 if btype == "ore" else 1)

    if args.drop == "none":
        drop = None
    elif args.drop:
        drop = args.drop
    elif btype == "ore":
        drop = item_id + "_chunk"
    else:
        drop = item_id   # decorative/equipment drop their own item

    # ── Read files ─────────────────────────────────────────────────────────────
    blocks_text   = BLOCKS_PY.read_text()
    items_text    = ITEMS_PY.read_text()
    crafting_text = CRAFTING_PY.read_text()

    bid = next_block_id(blocks_text)

    print(f"\n  name       : {name}")
    print(f"  type       : {btype}")
    print(f"  constant   : {const} = {bid}")
    print(f"  item_id    : {item_id}")
    print(f"  color      : {color}")
    print(f"  hardness   : {hardness}")
    print(f"  drop       : {drop or '(none)'}\n")

    # ── Apply mutations ────────────────────────────────────────────────────────
    try:
        # blocks.py
        blocks_text = insert_id_constant(blocks_text, const, bid, comment)
        blocks_text = insert_blocks_entry(blocks_text, const, name, hardness, color, drop)
        if btype == "equipment":
            blocks_text = append_to_set(blocks_text, "EQUIPMENT_BLOCKS", const)
        elif btype == "ore":
            blocks_text = append_to_set(blocks_text, "RESOURCE_BLOCKS", const)

        # items.py
        if btype in ("decorative", "equipment"):
            items_text = insert_item(items_text, item_id, name, color, const)
        else:
            # ore: add the drop chunk item (not placeable)
            if drop:
                drop_name  = drop.replace("_", " ").title()
                items_text = insert_item(items_text, drop, drop_name, color, None)

        # crafting.py
        if btype in ("decorative", "equipment"):
            crafting_text = insert_artisan_recipe(crafting_text, item_id, name)

    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    # ── Write or dry-run ───────────────────────────────────────────────────────
    if args.dry_run:
        print("Dry run — nothing written.\n")
        _preview("blocks.py",   BLOCKS_PY.read_text(),   blocks_text)
        _preview("items.py",    ITEMS_PY.read_text(),     items_text)
        if btype in ("decorative", "equipment"):
            _preview("crafting.py", CRAFTING_PY.read_text(), crafting_text)
    else:
        BLOCKS_PY.write_text(blocks_text)
        ITEMS_PY.write_text(items_text)
        CRAFTING_PY.write_text(crafting_text)
        print("  Written: blocks.py")
        print("  Written: items.py")
        if btype in ("decorative", "equipment"):
            print("  Written: crafting.py")

    # ── Remaining manual steps ─────────────────────────────────────────────────
    print("\nStill needs manual work:")
    print(f"  renderer.py   — draw {const} in _build_block_surfs()")
    if btype == "equipment":
        print(f"  main.py       — wire UI in handle_block_interact() for {const}")
    if btype == "ore":
        print(f"  world.py      — add spawn condition in _pick_block() for {const}")
        if drop:
            print(f"  items.py      — review '{drop}' entry (color/name auto-set from block)")
    if btype in ("decorative", "equipment"):
        print(f"  crafting.py   — update placeholder ingredients in ARTISAN_RECIPES for \"{name}\"")
    print()


def _preview(label: str, original: str, modified: str) -> None:
    orig_lines = set(original.splitlines())
    new_lines  = [l for l in modified.splitlines() if l not in orig_lines and l.strip()]
    if new_lines:
        print(f"--- {label} ---")
        for l in new_lines:
            print(f"  + {l}")
        print()


if __name__ == "__main__":
    main()
