# Logic & Automation System — Implementation Plan

## Context

Adds a circuit-style automation layer to CollectorBlocks. Players place wires on a dedicated third grid layer (invisible by default, toggled visible with a hotkey), connect them to switches and logic gates, and drive output blocks (doors, dam, pump, iron gate) to open/close automatically. Logic gates: AND, OR, NOT, and a toggle latch (stateful flip-flop).

This is infrastructure, not a collectible system — no encyclopedia, no codex, no biome profiles.

---

## New Files

| File | Purpose |
|------|---------|
| `logic.py` | Signal propagation engine (BFS + gate evaluation) |
| `Render/logic_blocks.py` | Renderer draw functions for all new blocks |

---

## Files Modified

`blocks.py`, `items.py`, `world.py`, `player.py`, `renderer.py`, `save_manager.py`, `main.py`, `crafting.py`

---

## Block IDs  (next free was 1072 → after this: 1085)

```python
SWITCH_BLOCK_OFF      = 1072   # lever — player toggles with E
SWITCH_BLOCK_ON       = 1073
LATCH_BLOCK_OFF       = 1074   # toggle flip-flop — player toggles with E
LATCH_BLOCK_ON        = 1075
AND_GATE_BLOCK        = 1076   # visual powered state read from logic_state
OR_GATE_BLOCK         = 1077
NOT_GATE_BLOCK        = 1078
DAM_BLOCK_CLOSED      = 1079   # water barrier — opaque, solid when closed
DAM_BLOCK_OPEN        = 1080   # passable gap when open
PUMP_BLOCK_OFF        = 1081
PUMP_BLOCK_ON         = 1082
IRON_GATE_BLOCK_CLOSED = 1083  # 1-tall controllable gate (≠ impassable GATE_MID)
IRON_GATE_BLOCK_OPEN   = 1084
```

Helper sets to add in `blocks.py`:
```python
LOGIC_SOURCE_BLOCKS = {SWITCH_BLOCK_ON, LATCH_BLOCK_ON}
LOGIC_GATE_BLOCKS   = {AND_GATE_BLOCK, OR_GATE_BLOCK, NOT_GATE_BLOCK}
LOGIC_OUTPUT_PAIRS  = {
    DAM_BLOCK_CLOSED: DAM_BLOCK_OPEN,   DAM_BLOCK_OPEN: DAM_BLOCK_CLOSED,
    PUMP_BLOCK_OFF:   PUMP_BLOCK_ON,    PUMP_BLOCK_ON:  PUMP_BLOCK_OFF,
    IRON_GATE_BLOCK_CLOSED: IRON_GATE_BLOCK_OPEN,
    IRON_GATE_BLOCK_OPEN:   IRON_GATE_BLOCK_CLOSED,
    # merge with existing _DOOR_PAIRS from player.py
}
LOGIC_OUTPUT_BLOCKS = set(LOGIC_OUTPUT_PAIRS)   # any block that logic can drive
```

---

## Step 1 — `logic.py`  (new file)

```python
from blocks import (LOGIC_SOURCE_BLOCKS, LOGIC_GATE_BLOCKS,
                    AND_GATE_BLOCK, OR_GATE_BLOCK, NOT_GATE_BLOCK,
                    LOGIC_OUTPUT_BLOCKS, LOGIC_OUTPUT_PAIRS)

_DIRS = [(0, -1), (0, 1), (-1, 0), (1, 0)]   # N S W E

def evaluate_full_network(world) -> set:
    """
    Re-evaluate the entire wire network from scratch.
    Returns the new set of powered (bx, by) wire/gate tiles.
    Stores result on world.powered_wires; also applies output block states.
    """
```

**Algorithm (three phases):**

**Phase 1 — Forward propagation**
- Seed queue: every tile where `world.get_block(bx,by)` is in `LOGIC_SOURCE_BLOCKS`
- BFS through wire tiles (`world.get_wire(nx,ny) == 1`) and through AND/OR gate tiles
  - AND gate: add to powered set only if ALL non-output neighbor wire tiles are powered
  - OR gate: add to powered set if ANY neighbor wire tile is powered
  - Gate output direction is stored in `world.logic_state[(bx,by)]["facing"]`
  - Stop BFS at NOT gate inputs and at output blocks (they are terminals)

**Phase 2 — NOT gate evaluation**
- For every NOT_GATE_BLOCK tracked in `world.logic_state`:
  - Input side (opposite of facing) wire tile: if NOT powered → NOT gate is powered
  - Add NOT gate output-side wire tile to a second BFS queue and propagate

**Phase 3 — Apply outputs**
- For every tile in `LOGIC_OUTPUT_BLOCKS`: if any adjacent wire tile is in `powered_wires` → set to open/on variant; else → set to closed/off variant
- Door pairs: reuse existing door-toggle logic

Store result: `world.powered_wires = powered_wires` (a `set` of `(bx,by)` tuples).

**Gate facing** is captured at placement time (`player.direction` → stored in `world.logic_state`).

**Latch rising-edge detection:** `world.logic_state[(bx,by)]["prev_input"]` tracks last input state; latch toggles only when input transitions False→True.

**Loop protection:** `max_iterations=8` outer loop guards against circular NOT chains.

---

## Step 2 — `blocks.py`

- Add the 13 block ID constants (see above)
- Add BLOCKS entries for all 13; gates/switches are `hardness: 2`, drops = their item form
- Dam/pump/iron-gate pairs: open variants have `hardness: 2`, `color: None` (renderer handles)
- Add all helper sets listed above
- Add `SWITCH_BLOCK_OFF` and `LATCH_BLOCK_OFF` to `EQUIPMENT_BLOCKS` so they are solid

---

## Step 3 — `items.py`

```python
"wire":                {"name": "Wire",         "color": (180,180,220), "wire_layer": True},
"switch_item":         {"name": "Switch",        "place_block": SWITCH_BLOCK_OFF},
"latch_item":          {"name": "Toggle Latch",  "place_block": LATCH_BLOCK_OFF},
"and_gate_item":       {"name": "AND Gate",      "place_block": AND_GATE_BLOCK},
"or_gate_item":        {"name": "OR Gate",       "place_block": OR_GATE_BLOCK},
"not_gate_item":       {"name": "NOT Gate",      "place_block": NOT_GATE_BLOCK},
"dam_item":            {"name": "Dam",           "place_block": DAM_BLOCK_CLOSED},
"pump_item":           {"name": "Pump",          "place_block": PUMP_BLOCK_OFF},
"iron_gate_item":      {"name": "Iron Gate",     "place_block": IRON_GATE_BLOCK_CLOSED},
```

`"wire_layer": True` is a sentinel that `player.py` checks to route placement to `world.set_wire()` instead of `world.set_block()`.

---

## Step 4 — `world.py`

**New fields on `World.__init__`:**
```python
self._wire_chunks   = {}        # chunk_x → 2D list[y][lx], uint8 (0=empty, 1=wire)
self.logic_state    = {}        # (bx,by) → {"facing": str, "latch_state": bool, "prev_input": bool}
self.powered_wires  = set()     # (bx,by) of currently-powered wire/gate tiles
self.wire_mode      = False     # True = wire layer visible
```

**New methods** (mirror `get_bg_block` / `set_bg_block` pattern):
```python
def get_wire(self, x, y) -> int: ...
def set_wire(self, x, y, val: int): ...   # marks dirty chunk for save
def toggle_wire_mode(self): self.wire_mode = not self.wire_mode
```

Wire chunks use the same chunk-key scheme as `_bg_chunks`.

---

## Step 5 — `player.py`

**Wire placement** — in the block-placement code (where `item.get("place_block")` is handled):
```python
if item.get("wire_layer"):
    self.world.set_wire(bx, by, 0 if self.world.get_wire(bx,by) else 1)
    logic.evaluate_full_network(self.world)
    return
```

**Gate placement** — after `set_block()` for any gate/switch/latch:
```python
if new_bid in LOGIC_GATE_BLOCKS | {SWITCH_BLOCK_OFF, LATCH_BLOCK_OFF}:
    self.world.logic_state[(bx,by)] = {"facing": self.direction, "latch_state": False, "prev_input": False}
    logic.evaluate_full_network(self.world)
```

**Switch / latch interaction** — in the E-key handler (near `_try_open_door`):
```python
if bid == SWITCH_BLOCK_OFF:
    self.world.set_block(bx, by, SWITCH_BLOCK_ON);  logic.evaluate_full_network(self.world)
elif bid == SWITCH_BLOCK_ON:
    self.world.set_block(bx, by, SWITCH_BLOCK_OFF); logic.evaluate_full_network(self.world)
elif bid in (LATCH_BLOCK_OFF, LATCH_BLOCK_ON):
    new = LATCH_BLOCK_ON if bid == LATCH_BLOCK_OFF else LATCH_BLOCK_OFF
    self.world.set_block(bx, by, new);              logic.evaluate_full_network(self.world)
```

---

## Step 6 — `renderer.py`

**Wire layer rendering** — add a pass in the tile-drawing loop (after foreground, before entities), gated on `world.wire_mode`:
```python
if world.wire_mode:
    for visible tile (bx, by):
        if world.get_wire(bx, by):
            draw_wire_tile(surface, bx, by, world)    # in Render/logic_blocks.py
```

`draw_wire_tile` infers shape (straight / corner / cross / T) from 4 neighbors' wire values. Powered wires: bright cyan. Unpowered: dim grey-blue.

**Logic block draw functions in `Render/logic_blocks.py`:**
- `draw_switch_off / draw_switch_on` — lever sprite
- `draw_latch_off / draw_latch_on` — flip-flop symbol
- `draw_and_gate / draw_or_gate / draw_not_gate` — gate shapes with facing arrow; tint cyan when in `world.powered_wires`
- `draw_dam_closed / draw_dam_open` — stone barrier vs open gap
- `draw_pump_off / draw_pump_on` — pump housing; piston crank when ON
- `draw_iron_gate_closed / draw_iron_gate_open` — vertical bars vs open

Import these in `renderer.py` and add to the block-draw dispatch (same pattern as existing `Render/blocks_*.py`).

---

## Step 7 — `save_manager.py`

**Wire chunks** — same compress+pack format as regular chunks:
```sql
CREATE TABLE IF NOT EXISTS wire_chunks (chunk_x INTEGER PRIMARY KEY, data BLOB)
```
Save in `_save_wire_chunks(con, world)`, load in `_load_wire_chunks(con)`.

**Logic state** — new JSON column `logic_state` in `world_meta`:
```python
# save:  json.dumps({f"{bx},{by}": v for (bx,by),v in world.logic_state.items()})
# load:  {tuple(map(int,k.split(","))): v for k,v in parsed.items()}
```

**Powered wires** — do NOT save; always re-derive by calling `logic.evaluate_full_network(world)` after load completes.

---

## Step 8 — `crafting.py`

Add recipes at the existing **Workbench** station (no new research lock):

| Output | Ingredients |
|--------|-------------|
| Wire ×16 | 2 iron + 1 copper |
| Switch | 2 iron + 1 wire |
| Toggle Latch | 3 iron + 2 wire |
| AND Gate | 2 copper + 2 wire |
| OR Gate | 2 copper + 1 wire |
| NOT Gate | 2 copper + 1 iron + 1 wire |
| Dam | 6 stone + 2 iron |
| Pump | 4 iron + 2 copper + 2 wire |
| Iron Gate | 6 iron |

---

## Step 9 — `main.py`

**Wire mode toggle** — add to key-event block:
```python
if event.key == pygame.K_BACKQUOTE:    # ` key
    world.toggle_wire_mode()
```

No new panel/UI overlay needed; wire mode is purely a visual layer toggle on the world renderer.

---

## Verification

1. Place a **switch** and a **door** — connect with wires — press E on switch → door opens/closes
2. Place a **NOT gate** between switch and door — door open by default, closes on switch ON
3. Two switches → **AND gate** → pump — pump only activates when both switches are ON
4. Save and reload — wire layout, logic_state, and switch positions survive
5. Toggle wire mode off (`\``) — wires invisible, game plays normally
6. Toggle wire mode on — wire tiles visible, powered wires glow cyan
7. Place a **latch** — tap E twice — confirm it stays ON after first tap, OFF after second
8. Mine a gate block — drops its item — place again, signal still propagates

---

## Block ID update

After this system: **next free block ID = 1085**
