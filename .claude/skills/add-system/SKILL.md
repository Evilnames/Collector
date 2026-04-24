---
name: add-system
description: Complete guide for adding a brand-new collectible system to CollectorBlocks (like coffee or wine). Covers every file that must be touched: data module, blocks, items, world harvesting, player tracking, save/load, UI mixin, collections tab, encyclopedia, and input wiring.
---

# Add a New Collectible System

Use coffee and wine as the two reference implementations throughout. Every step below has a direct parallel in one or both of them.

---

## Overview — files you will touch

| File | What you add |
|------|-------------|
| `newsystem.py` | Dataclass, biome profiles, processing tables, generator, helper functions |
| `blocks.py` | Bush / Young / Mature block IDs and block definitions |
| `items.py` | Seed, raw harvest, station placer, all output variants |
| `player.py` | Collection list, discovered set, generator instance, mining hook |
| `save_manager.py` | DB table schema, save method, load query |
| `crafting.py` | Research locks for station items |
| `UI/newsystem.py` | UI mixin — all drawing and click handlers |
| `UI/__init__.py` | Import mixin, add to UI class inheritance |
| `UI/collections.py` | Filter button, encyclopedia tab, codex drawing function |
| `UI/handlers.py` | Route block clicks to your mixin's handlers |
| `main.py` | Wire keyboard / mouse input for mini-games |

---

## Step 1 — Core data module (`newsystem.py`)

Create `newsystem.py` at the project root. Structure it exactly like `coffee.py` or `wine.py`.

**Required pieces:**

```python
from dataclasses import dataclass, field

@dataclass
class NewItem:
    uid: str
    origin_biome: str       # biome harvested in ("blend" for blends)
    variety: str            # cultivar / variant key
    state: str              # "raw" | "processed" | "finished"
    # ... your system's core float attributes (0.0–1.0) ...
    flavor_notes: list
    seed: int
    blend_components: list = field(default_factory=list)

# Base attributes per biome — every harvestable biome gets an entry
BIOME_PROFILES = {
    "tropical": {"attr_a": 0.80, "attr_b": 0.40, ..., "variety": "variety_key"},
    ...
}

# Processing step tables (modifiers applied at each stage)
PROCESSING_OPTIONS = {
    "option_key": {"label": "Label", "desc": "...", "attr_a": +0.10, ...},
    ...
}

# Output descriptions and display colors
OUTPUT_DESCS   = {"output_key": "Output Name — description"}
OUTPUT_COLORS  = {"output_key": (r, g, b)}

# Buff effects
BUFF_DESCS = {"buff_key": "Effect description (+X%)"}

# Codex display order — defines grid layout
_CODEX_BIOMES  = list(BIOME_PROFILES.keys())
TYPE_ORDER     = [f"{biome}_{output}" for biome in _CODEX_BIOMES for output in OUTPUT_DESCS]

BIOME_DISPLAY_NAMES = {"tropical": "Tropical", ..., "blend": "Blend"}

class NewSystemGenerator:
    def __init__(self, world_seed: int):
        self._world_seed = world_seed
        self._counter    = 0

    def generate(self, biodome: str) -> "NewItem":
        self._counter += 1
        seed = (self._world_seed * 31 + self._counter * 7919) & 0xFFFFFFFF
        uid  = hashlib.md5(f"newsystem_{seed}_{self._counter}".encode()).hexdigest()[:12]
        profile = BIOME_PROFILES.get(biodome, list(BIOME_PROFILES.values())[0])
        # jitter each attribute, build and return the dataclass instance
        ...
```

---

## Step 2 — Blocks (`blocks.py`)

Add three block IDs and their definitions — bush (decorative), young crop (growing), mature crop (harvestable).

```python
# Block ID constants (pick the next available integers)
NEWSYSTEM_BUSH          = 250
NEWSYSTEM_CROP_YOUNG    = 251
NEWSYSTEM_CROP_MATURE   = 252
```

Add entries to the `BLOCKS` dict following the same pattern as `COFFEE_BUSH` etc.:

```python
NEWSYSTEM_BUSH:       {"name": "New System Bush",   "hardness": 1, "color": (...), "drop": "newsystem_seed", "drop_chance": 0.3},
NEWSYSTEM_CROP_YOUNG: {"name": "New System (Young)", "hardness": 1, "color": (...), "drop": None},
NEWSYSTEM_CROP_MATURE: {"name": "New System (Mature)", "hardness": 1, "color": (...), "drop": "newsystem_seed", "drop_chance": 1.0},
```

If mature blocks should auto-register as harvestable, add `NEWSYSTEM_CROP_MATURE` to `MATURE_CROP_BLOCKS`.

---

## Step 3 — Items (`items.py`)

Add all items the system needs. Follow the coffee/wine pattern for naming and fields.

```python
# Planting
"newsystem_seed":   {"name": "New System Seed", "place_block": NEWSYSTEM_CROP_YOUNG},

# Raw harvest (may be edible)
"newsystem_raw":    {"name": "New System Harvest", "edible": True, "hunger_restore": 4},

# Station placer
"newsystem_station_item": {"name": "New System Station", "place_block": NEWSYSTEM_STATION_BLOCK},

# Processed outputs — base / fine / superior tiers for each output type
"newsystem_output_a":          {"edible": True, "newsystem_buff": "buff_key", "newsystem_buff_duration": 90.0},
"newsystem_output_a_fine":     {"edible": True, "newsystem_buff": "buff_key", "newsystem_buff_duration": 112.0},
"newsystem_output_a_superior": {"edible": True, "newsystem_buff": "buff_key", "newsystem_buff_duration": 135.0},
```

---

## Step 4 — Player tracking (`player.py`)

**Add fields in `__init__`:**

```python
from newsystem import NewSystemGenerator

# in Player.__init__:
self.newsystem_items        = []
self.discovered_newsystem   = set()        # "biome_outputkey" strings
self._newsystem_gen         = NewSystemGenerator(world.seed)
self.newsystem_buffs        = {}           # {buff_name: {"duration": float}}
```

**Add the mining hook in `finish_mine()`**, alongside the coffee/wine blocks:

```python
elif block_id == NEWSYSTEM_CROP_MATURE:
    biodome = self.world.get_biodome(bx)
    item    = self._newsystem_gen.generate(biodome)
    self.newsystem_items.append(item)
    self._add_item("newsystem_seed")
    self.pending_notifications.append(("NewSystem", "New System Harvest", None))
```

**Add to `apply_save()`:**

```python
self.newsystem_items      = [NewItem(**x) for x in d.get("newsystem_items", [])]
self.discovered_newsystem = set(d.get("discovered_newsystem", []))
```

---

## Step 5 — Save/load (`save_manager.py`)

**Create the table** in the table-creation block:

```python
CREATE TABLE IF NOT EXISTS newsystem_items (
    uid TEXT PRIMARY KEY,
    origin_biome TEXT, variety TEXT, state TEXT,
    attr_a REAL, attr_b REAL, ...,
    flavor_notes TEXT, seed INT,
    blend_components TEXT
)
```

**Add a save method** near `_save_coffee_beans`:

```python
def _save_newsystem_items(self, con, player):
    con.execute("DELETE FROM newsystem_items")
    for x in player.newsystem_items:
        con.execute("INSERT OR REPLACE INTO newsystem_items VALUES (?,?,?,?,?,?,?,?,?)", (
            x.uid, x.origin_biome, x.variety, x.state,
            x.attr_a, x.attr_b, ...,
            json.dumps(x.flavor_notes), x.seed,
            json.dumps(x.blend_components),
        ))
```

Call it from `save()`:

```python
self._save_newsystem_items(con, player)
```

**Add the load query** alongside the coffee/wine queries:

```python
newsystem_data = [dict(r) for r in con.execute("SELECT * FROM newsystem_items")]
# parse flavor_notes / blend_components from JSON strings back to lists
return {
    ...
    "newsystem_items":      newsystem_data,
    "discovered_newsystem": list({
        f"{x['origin_biome']}_{x['state']}" for x in newsystem_data
    }),
}
```

---

## Step 6 — Research lock (`crafting.py`)

If the station requires research to unlock, add it to the research-locked items dict:

```python
"newsystem_station_item": "newsystem_basics",
```

Add the corresponding research node to `research.py` if the research tree is expanding.

---

## Step 7 — UI mixin (`UI/newsystem.py`)

Create `UI/newsystem.py` with a `NewSystemMixin` class. Model it after `UI/coffee.py` or `UI/wine.py`.

**Required methods:**

```python
class NewSystemMixin:
    # ── Drawing ──────────────────────────────────────────────────────────
    def _draw_newsystem_station(self, surface, player): ...
    # One method per processing stage (draw the panel + mini-game visuals)

    # ── Click handlers ───────────────────────────────────────────────────
    def _handle_newsystem_station_click(self, pos, player): ...

    # ── Key handlers (if mini-game uses keyboard) ─────────────────────
    def handle_newsystem_keydown(self, key, player): ...
    def handle_newsystem_keys(self, keys, dt, player): ...
```

**State variables** belong in `UI/__init__`'s `__init__` (see next step), not in the mixin itself.

**When processing completes**, call:
```python
player._add_item("newsystem_output_a")           # give the output item
player.discovered_newsystem.add(f"{biome}_{output_key}")  # mark discovered
```

---

## Step 8 — Register the mixin (`UI/__init__.py`)

```python
from .newsystem import NewSystemMixin

class UI(
    ...,
    CoffeeMixin,
    WineMixin,
    NewSystemMixin,   # add here
):
    def __init__(self, ...):
        ...
        # Add your mixin's state variables here, alongside coffee/wine state:
        self.newsystem_phase          = "idle"   # or whatever states your mini-game needs
        self.newsystem_selected_item  = None
        self.newsystem_scroll         = 0
```

---

## Step 9 — Collections & encyclopedia (`UI/collections.py`)

**A — Filter button**

Find the filter definitions block (near the `"COFFEE"`, `"WINE"` entries) and add:

```python
("NEWSYSTEM", theme_color),
```

Add your theme color to `FILTER_THEME`:

```python
"NEWSYSTEM": (r, g, b),
```

**B — Encyclopedia tab**

Find `enc_defs` (the list that drives the tabs across the top of the encyclopedia). Add an entry:

```python
enc_defs = [
    ...,
    ("NewSystem", len(player.discovered_newsystem), total_count, theme_color),
]
```

Add your theme to `ENC_THEME`:

```python
ENC_THEME["newsystem"] = (r, g, b)
```

Increment the `_encyclopedia_cat` range to include the new tab index.

**C — Codex drawing function**

Add `_draw_newsystem_codex(self, player, gy0=58)`. Use `_draw_coffee_codex` or `_draw_wine_codex` as the template — they both:

1. Build a biome × output grid from `TYPE_ORDER`
2. Check `player.discovered_newsystem` to decide which cells are revealed
3. Show quality stars for discovered entries
4. Render a detail panel for the selected entry

Wire it into the encyclopedia tab dispatcher alongside the existing cases.

---

## Step 10 — Block click routing (`UI/handlers.py`)

Find `handle_refinery_click` (the method that dispatches to coffee/wine handlers based on the active block ID). Add your station block:

```python
if self.refinery_block_id == NEWSYSTEM_STATION_BLOCK:
    self._handle_newsystem_station_click(pos, player)
```

Import `NEWSYSTEM_STATION_BLOCK` from `blocks.py` at the top of the file.

---

## Step 11 — Input wiring (`main.py`)

Search for how coffee/wine keyboard input is routed (look for `handle_roaster_keydown`, `handle_grape_press_keys`, etc.). Mirror the same pattern for your system:

```python
# In the keydown handler:
if ui.active_panel == "newsystem_station":
    ui.handle_newsystem_keydown(event.key, player)

# In the held-key handler (called each frame):
if ui.active_panel == "newsystem_station":
    ui.handle_newsystem_keys(keys, dt, player)

# Mousewheel, if your UI scrolls:
if ui.active_panel == "newsystem_station":
    ui.newsystem_scroll += event.y * SCROLL_SPEED
```

---

## Sequence summary

Follow this order to avoid forward-reference issues:

1. `newsystem.py` — data structures and generator
2. `blocks.py` — block IDs and definitions
3. `items.py` — all items
4. `player.py` — fields, mining hook, apply_save
5. `save_manager.py` — table, save method, load query
6. `crafting.py` — research lock
7. `UI/newsystem.py` — mixin with drawing + handlers
8. `UI/__init__.py` — import mixin, add state vars
9. `UI/collections.py` — filter, encyclopedia tab, codex
10. `UI/handlers.py` — block click routing
11. `main.py` — keyboard/mouse input

## Verification checklist

- [ ] Harvest the plant in-game — item appears in player inventory
- [ ] Save and reload — inventory survives
- [ ] Process through each station stage — output item is granted
- [ ] `discovered_newsystem` set updates after first completion
- [ ] Encyclopedia tab shows correct discovered / total count
- [ ] Codex grid shows discovered cells; detail panel renders correctly
- [ ] Collection filter button shows only this system's items
- [ ] Buffs apply when output item is consumed
