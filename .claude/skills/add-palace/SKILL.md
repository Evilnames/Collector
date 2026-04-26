---
name: add-palace
description: Step-by-step guide for adding a new palace type to CollectorBlocks. Covers PALACE_TYPES registration, NPC offset, placement function, and world.py dispatch.
---

# Add a New Palace Type

Palace types are listed in [cities.py](../../../cities.py) and each has a dedicated placement function. The placement function uses modular piece helpers (`_piece_*`) and block-drawing helpers (`_castle_set`, `_castle_bg`, etc.) to assemble the structure, then spawns NPCs with `_palace_npc_at`.

---

## Step 1 — Register the palace name

Find `PALACE_TYPES` in [cities.py](../../../cities.py) and add the new style name:

```python
PALACE_TYPES = [
    "castle", "mediterranean", "east_asian", "south_asian",
    "italian", "moorish", "middle_eastern",
    "norse", "gothic", "african", "byzantine", "tibetan",
    "japanese", "chinese",
    "ottoman",   # ← add here
]
```

---

## Step 2 — Add the NPC guard offset

Find `PALACE_NPC_OFFSET` in [cities.py](../../../cities.py) and set the x-offset (in blocks) from `left_x` where guards should be placed. Typical range is 31–53:

```python
PALACE_NPC_OFFSET = {
    ...
    "ottoman": 42,
}
```

---

## Step 3 — Implement the placement function

Add a new function `_place_ottoman_palace(world, left_x, sy)` near the other `_place_*_palace` functions. The function receives:
- `world` — the world object (use `world.set_block`, `world.get_block`, etc.)
- `left_x` — leftmost block x of the palace footprint
- `sy` — the surface y at the palace centre

Structure it as a sequence of piece calls followed by NPC spawning:

```python
def _place_ottoman_palace(world, left_x, sy):
    rng = _palace_rng(world, left_x)

    # Clear and level terrain
    _palace_clear_terrain(world, left_x, sy, half_w=50)

    # Assemble pieces left → right
    cx = left_x
    cx += _piece_moat(world, cx, sy)
    cx += _piece_gatehouse(world, cx, sy)
    cx += _piece_grand_hall(world, cx, sy)
    cx += _piece_keep(world, cx, sy)
    cx += _piece_chapel(world, cx, sy)   # use as a prayer hall

    # Pick a block palette
    wall  = BLOCK.SANDSTONE
    roof  = BLOCK.TERRACOTTA_BLUE
    floor = BLOCK.MARBLE_TILE

    # Place decorative dome manually if needed
    mid = left_x + 25
    for dy in range(6):
        w = 6 - dy
        _castle_set(world, mid - w, sy - 8 - dy, mid + w, sy - 8 - dy, wall)
    _castle_bg(world, mid - 2, sy - 14, mid + 2, sy - 14, roof)

    # Spawn NPCs
    _palace_npc_at(world, left_x + 4,  sy, GuardNPC)
    _palace_npc_at(world, left_x + 8,  sy, TradeNPC)
    _palace_npc_at(world, left_x + 14, sy, LeaderNPC)
    _palace_npc_at(world, left_x + 20, sy, RoyalJewelerNPC)
    _palace_npc_at(world, left_x + PALACE_NPC_OFFSET["ottoman"], sy, GuardNPC)
```

### Block-drawing helpers

| Helper | What it does |
|--------|-------------|
| `_castle_set(world, x1, y1, x2, y2, block)` | Fill a rectangle with foreground blocks |
| `_castle_bg(world, x1, y1, x2, y2, block)` | Fill a rectangle with background blocks |
| `_castle_fill_bg(world, x1, y1, x2, y2, block)` | Alias for bg fill (solid interior) |
| `_castle_door(world, x, y)` | Place a 2×2 walkable archway |

### Piece helpers and their widths

| Piece function | Width constant | Description |
|----------------|---------------|-------------|
| `_piece_moat(world, cx, sy)` | `_CW_MOAT = 4` | Drawbridge approach |
| `_piece_round_tower(world, cx, sy)` | `_CW_ROUND_TOW = 6` | Conical-roof tower |
| `_piece_square_tower(world, cx, sy)` | `_CW_SQ_TOW = 8` | Battlement tower |
| `_piece_gatehouse(world, cx, sy)` | `_CW_GATEHOUSE = 7` | Portcullis entry |
| `_piece_great_hall(world, cx, sy)` | `_CW_GREAT_HALL = 13` | Throne hall |
| `_piece_grand_hall(world, cx, sy)` | `_CW_GRAND_HALL = 15` | Larger throne hall |
| `_piece_keep(world, cx, sy)` | `_CW_KEEP = 10` | Central keep |
| `_piece_palace_keep(world, cx, sy)` | `_CW_PAL_KEEP = 12` | Grand central keep |
| `_piece_chapel(world, cx, sy)` | `_CW_CHAPEL = 9` | Gothic chapel |
| `_piece_barracks(world, cx, sy)` | `_CW_BARRACKS = 11` | Military wing |

### NPC types valid in palaces

`TradeNPC`, `LeaderNPC`, `RoyalCuratorNPC`, `RoyalFloristNPC`, `RoyalJewelerNPC`, `GuardNPC`, `ScholarNPC`

---

## Step 4 — Wire into the dispatch

Find the palace selection block in [cities.py](../../../cities.py) (search for `PALACE_TYPES` usage or `_place_castle_palace`) and add the new dispatch case:

```python
if palace_type == "ottoman":
    _place_ottoman_palace(world, left_x, sy)
```

If dispatch is a dict mapping strings to functions, add:

```python
_PALACE_DISPATCH = {
    ...
    "ottoman": _place_ottoman_palace,
}
```

---

## Verification checklist

- [ ] `"ottoman"` appears in `PALACE_TYPES`
- [ ] `PALACE_NPC_OFFSET["ottoman"]` is set
- [ ] `_place_ottoman_palace` is implemented and reachable
- [ ] Dispatch wired so the function is called when `palace_type == "ottoman"`
- [ ] Generate a capital city in the matching biome — palace should render with no errors
- [ ] All expected NPCs (guard, leader, trader) spawn inside the palace
