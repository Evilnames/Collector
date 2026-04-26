# Towns, Regions, Needs & Growth

## Context

Towns today are procedurally placed via `cities.generate_cities` / `_build_single_city` but they are *just geometry* — no identity, no state, no relationship to one another. The player walks through them and can talk to merchant/quest NPCs but the towns themselves are scenery.

This idea adds:
- A persistent **Town** identity with name, biome, tier, needs, reputation, and remembered "grown" buildings
- **Regions** that group every 3 consecutive towns; the biggest town in each region is the capital and houses a **palace/castle** with a **LeaderNPC**
- A new **Town Flag** block placed in every town (square or center) — interacting opens a Town Menu UI
- Generic-category **needs** ("200 food", "100 wood") that scale with tier; satisfying them awards gold + per-town and per-region reputation
- **Daily growth ticks**: needs satisfied → growth_progress accumulates → tier up → new buildings physically appear in the world (live, in-place)

## Locked design decisions

| | |
|---|---|
| Categories (v1) | **Core 4**: food, wood, stone, metal |
| Growth visualization | **Live in-place new buildings** at pre-allocated growth slots |
| Region size / capital | **3 towns/region, biggest tier = capital** (locked at world gen) |
| Reputation | **Per-town and per-region** (region rep = sum of member-town rep, surfaced separately in leader dialog) |

## Architecture

### New module: `towns.py`

Holds the `Town` and `Region` classes, the in-memory registries, day-tick logic, and supply logic. Mirrors how `cities.py` is the home for city geometry — `towns.py` is the home for town *state*.

```
class Town:
    town_id: int                    # stable, derived from generation slot index
    region_id: int
    is_capital: bool
    center_bx: int                  # canonical world-x of the town center (= city_bx)
    half_w: int                     # current footprint, may grow with tier
    biome: str
    name: str
    leader_name: str | None         # only on capitals
    tier: int                       # 0=hamlet 1=village 2=town 3=city
    reputation: int
    needs: dict[str, dict]          # {"food": {"required": 200, "supplied": 50}, ...}
    growth_progress: float          # 0..1; resets on tier up
    grown_buildings: list[tuple]    # [(offset, variant, width, height, palette_id), ...]
                                    # appended to as the town grows; replayed on chunk regen
    founded_day: int

class Region:
    region_id: int
    name: str
    capital_town_id: int
    member_town_ids: list[int]
    leader_color: tuple             # heraldic flag color, propagated to flags + castle banners
    reputation: int                 # sum/avg of member town rep
```

Module-level: `TOWNS: dict[int, Town] = {}`, `REGIONS: dict[int, Region] = {}` populated by `init_towns(world)`.

### New module: `town_needs.py`

Pure data + helpers. Keeps `items.py` untouched and centralizes need definitions in one place.

```
TOWN_CATEGORIES = {
    "food":  ["wheat", "carrot", "tomato", "corn", "pumpkin", "apple",
              "potato", "onion", "cabbage", "beet", "leek", "broccoli",
              "rice", "bok_choy", "ginger", "mushroom", "chickpea",
              "lentil", "sweet_potato", "watermelon", "pomegranate",
              "cactus_fruit", "date_palm_fruit",
              # cooked dishes
              "steamed_bun", "bread", "noodles", ...],
    "wood":  ["oak_log", "birch_log", ..., "walnut_plank", "teak_plank", ...],
    "stone": ["stone", "cobblestone", "limestone", "marble_block", ...],
    "metal": ["iron_ingot", "copper_ingot", "gold_ingot", "tin_ingot", ...],
}

CATEGORY_DISPLAY     = {"food": "Food", "wood": "Wood", ...}
CATEGORY_COLOR       = {"food": (200,180,60), "wood": (140,90,50), ...}
GOLD_PER_UNIT        = {"food": 1, "wood": 2, "stone": 3, "metal": 8}
REP_PER_NEED_FILLED  = 10        # awarded once when a category fully satisfied

# Built once at import:
ITEM_TO_CATEGORY: dict[str, str] = {item: cat for cat, items in TOWN_CATEGORIES.items() for item in items}
```

### New module: `UI/town_menu.py`

`TownMenuMixin` — added to the `UI` inheritance tuple in `UI/__init__.py`. Mirrors the existing mixin pattern (cheese.py, jewelry.py, pottery.py).

- `_draw_town_menu(self, player)` — modal panel showing town name, biome, tier badge, growth bar, region label (with "★ Capital" if the leader town), reputation bar, list of active needs
- Each need row: category name + icon swatch, supplied/required progress bar, `+1 / +10 / +ALL` supply buttons, gold/rep preview
- `_handle_town_menu_click` — routes button clicks through `towns.supply_need(town, player, category, amount)`
- ESC and E close the menu (wired via `UI/handlers.py`)

### Day tick: `world.py`

Add `self.day_count = 0` in `__init__`. Modify `update_time` (currently around line 1525):

```
def update_time(self, dt):
    prev = self.time_of_day
    self.time_of_day = (self.time_of_day + dt) % CYCLE_DURATION
    if self.time_of_day < prev:
        self.day_count += 1
        from towns import advance_day
        advance_day(self)
```

`advance_day(world)` iterates `TOWNS.values()`. For each town, if all current needs are satisfied, `growth_progress += 1.0 / DAYS_PER_TIER` (with `DAYS_PER_TIER = 5`). When `>= 1.0`, increment tier, reset progress, generate new needs scaled to new tier, **and call `_grow_town_buildings(town, world)`** which appends new entries to `town.grown_buildings` and immediately spawns them in the world.

## File-by-file changes

### New files

- **`towns.py`** — Town/Region classes; `TOWNS`/`REGIONS` registries; `init_towns(world)`; `assign_initial_needs(town)`; `supply_need(town, player, category, amount)`; `advance_day(world)`; `_grow_town_buildings(town, world)`; `get_town_for_block(world, bx, by)`; `serialize_all() / deserialize_all(rows)` for save_manager.
- **`town_needs.py`** — `TOWN_CATEGORIES`, lookups, reward constants.
- **`UI/town_menu.py`** — `TownMenuMixin` class with draw/click handlers.

### Modified files

- **`blocks.py`** — Add `TOWN_FLAG_BLOCK = 1072` constant + `BLOCKS[TOWN_FLAG_BLOCK]` entry (non-mineable, no drop). Next free ID is 1072.
- **`items.py`** — No changes. (Categories live in `town_needs.py`.) Optional cheat-only "town_flag" placement item.
- **`renderer.py`** — Add `_draw_town_flag(...)`: a pole + a colored pennant tinted by `region.leader_color`. Wire into the block draw dispatch for `TOWN_FLAG_BLOCK`.
- **`cities.py`**:
  - Add a 4th tier `"city"` to `CITY_CONFIGS` (for tier-3 metropolis).
  - Add **growth slot** lists per tier in each `CITY_CONFIGS` entry: `"growth_slots_tier1"`, `"growth_slots_tier2"`, `"growth_slots_tier3"` — tuples of `(offset, w_range, h_range, variants)` extending the footprint outward. Pre-allocated positions only used when a town grows.
  - Add `castle` building variant + `_place_castle(world, left_x, sy, width, height)` using `ROUND_TOWER_WALL`, `CURTAIN_WALL`, `GREAT_HALL_FLOOR`, `CRENELLATION`, `HERALDIC_PANEL`. Spawns a `LeaderNPC` inside.
  - New `LeaderNPC(NPC)` class with `region_id`, `region_name`, `leader_name`, `dialog_lines`. Renders with a distinct outfit color.
  - Modify `_build_single_city` (currently around line 1835) to accept the town record (or look it up). Replays `town.grown_buildings` after base buildings. If `town.is_capital`, also place the castle (at the leftmost or rightmost edge of the footprint).
  - In `_place_town_square` (currently around line 954), place a `TOWN_FLAG_BLOCK` (foreground) at `(center_bx, sy - 1)`. For small towns with no square, also place a flag in `_build_single_city` at city center — every town must have a flag.
- **`world.py`**:
  - `__init__`: `self.day_count = 0`, `self.town_centers: list[tuple] = []` (filled as cities are built).
  - `update_time`: wrap-detect → day tick.
  - After `generate_cities(self, self.seed)` (init + load paths), call `towns.init_towns(self)`.
  - In the chunk-streaming city build path (`generate_city_for_chunk`), record the town center too — but for v1, only `generate_cities`-built cities get town identities (chunk-streamed cities are flagless and ignored by `towns.py`). Documented limitation.
- **`save_manager.py`**:
  - Add tables in `_create_tables`:
    ```
    CREATE TABLE IF NOT EXISTS towns (
        town_id INTEGER PRIMARY KEY, region_id INTEGER,
        is_capital INTEGER, center_bx INTEGER, half_w INTEGER,
        biome TEXT, name TEXT, leader_name TEXT,
        tier INTEGER, reputation INTEGER, growth_progress REAL,
        founded_day INTEGER, needs_json TEXT, grown_buildings_json TEXT
    );
    CREATE TABLE IF NOT EXISTS regions (
        region_id INTEGER PRIMARY KEY, name TEXT,
        capital_town_id INTEGER, leader_color TEXT, reputation INTEGER
    );
    ```
  - Add `day_count INTEGER` column to existing `world_meta` table (handle via existing `_maybe_migrate` around line 107).
  - Wire `_save_towns / _load_towns / _save_regions / _load_regions` into `save()` / `load()` calls.
- **`main.py`** — Add a new branch in the E-key dispatch (around line 935, before the equipment branch):
  ```
  nearby_flag = player.get_nearby_town_flag()
  if nearby_flag is not None:
      from towns import get_town_for_block
      town = get_town_for_block(world, *nearby_flag)
      if ui.town_menu_open and ui.active_town is town:
          ui.close_town_menu()
      else:
          _close_all_ui(); ui.open_town_menu(town)
      continue
  ```
  Also add `ui.town_menu_open = False; ui.active_town = None` to `_close_all_ui` (currently around line 457).
- **`player.py`** — Add `get_nearby_town_flag(self)` (mirrors `get_nearby_chest`). Add helpers `count_items_in_category(category)` and `remove_items_in_category(category, count_needed)` for clean supply logic.
- **`UI/__init__.py`** — Import `TownMenuMixin`, add to inheritance, init `self.town_menu_open = False; self.active_town = None; self._town_menu_rects = {}`. Add `open_town_menu/close_town_menu` methods. Dispatch in `draw()`.
- **`UI/handlers.py`** — ESC + E close handling for `town_menu_open`. Click routing to `_handle_town_menu_click`.
- **`UI/panels.py`** — In `_draw_npc_panel`, add `elif isinstance(npc, LeaderNPC):` branch + `_draw_leader_content(player, npc, ...)` method showing region overview, member town list with per-town rep, region rep total, and flavor dialog.

## Reused functions / patterns

- NPC interaction toggle pattern: `main.py` ~line 850 — copy verbatim for flag block.
- Chest `get_nearby_chest` traversal: `player.py` — copy structure for `get_nearby_town_flag`.
- TradeNPC supply pattern: `cities.py` ~line 438 — adapt for `supply_need` (decrement inventory, credit money, but iterate by category).
- UI mixin pattern: existing `UI/cheese.py`, `UI/pottery.py` — template for `UI/town_menu.py`.
- Save migration hook: existing `_maybe_migrate` at `save_manager.py` ~line 107 — add `day_count` column there.
- Castle blocks already imported in `renderer.py` — `ROUND_TOWER_WALL`, `CURTAIN_WALL`, `GREAT_HALL_FLOOR`, `CRENELLATION`, `HERALDIC_PANEL`.

## Implementation order

1. **`town_needs.py`** — categories + reverse lookup. Pure data.
2. **player.py helpers** — `count_items_in_category`, `remove_items_in_category`. Unit-test by hand at the cheat console.
3. **`world.day_count` + day-tick hook** — print on wrap to confirm.
4. **`towns.py`** — Town/Region classes, `init_towns`, name pools, initial needs. Verify in console: print `TOWNS` after world load.
5. **save_manager schema** — add tables + migration. Save → reload → confirm towns persist.
6. **`TOWN_FLAG_BLOCK`** — block ID, BLOCKS entry, renderer draw, placement in `_place_town_square` and small-town fallback.
7. **player.get_nearby_town_flag + main.py E-key branch** — opens placeholder menu.
8. **`UI/town_menu.py`** — needs panel, supply buttons. End-to-end test: deliver wheat, food need decrements, money/rep increase.
9. **Day-tick growth** — `advance_day`, growth_progress, tier-up. Toast on tier-up.
10. **Growth slots** — define per-tier slot lists in `CITY_CONFIGS`. `_grow_town_buildings` picks the next slot, spawns building immediately, appends to `town.grown_buildings`. On chunk regen, `_build_single_city` replays the list.
11. **Region grouping** — `init_towns` groups consecutive 3, picks biggest-tier as capital (ties → first), generates region names + leader colors.
12. **Castle + LeaderNPC** — capital towns get a castle building placed at the footprint edge; LeaderNPC spawns inside.
13. **Leader dialog** — branch in `_draw_npc_panel` showing region status, member town reps, flavor lines.
14. **Polish** — name pools per biome, balance the gold/rep numbers, tune `DAYS_PER_TIER`.

## Risks & edge cases

- **Existing saves**: no `towns`/`regions` rows → `init_towns` creates fresh state on first load. `day_count` defaults to 0. Safe.
- **Town with no square** (small towns have `"squares": []`): handled by the small-town fallback in step 6 — flag goes at city center.
- **Chunk-streamed cities** (`generate_city_for_chunk`): fully supported. They receive a town record, region membership (lazily created), flag block, and are growth-eligible. Region assignment is slot-index-based: `region_id = (slot_x // CITY_SPACING) // 3`, capital when `slot_index % 3 == 1`.
- **Capital changes when a non-capital town grows**: capital is **locked at world generation**, not re-evaluated on tier-up. Otherwise the LeaderNPC would teleport between towns. This is a deliberate simplification.
- **Live in-place growth touching player-edited blocks**: `_grow_town_buildings` should check that the target growth slot is mostly empty/natural before placing — if blocked (player built there), skip silently and try the next slot. Failing that, defer until next chunk regen.
- **Day length**: `CYCLE_DURATION = 960s` (16 min real-time per day). With `DAYS_PER_TIER = 5`, tiering up takes ~80 min real-time of fully satisfied needs. Tunable.
- **Item duplication via category overlap**: Each item is in exactly one category in `TOWN_CATEGORIES`. Reverse map is unambiguous.
- **Region rep computation**: cheap — `sum(TOWNS[tid].reputation for tid in region.member_town_ids)`. Compute on read, don't persist separately.
- **LeaderNPC regen on load**: NPCs aren't persisted, but identity is `region_id`. On regen, `_place_castle` creates a fresh `LeaderNPC(region_id=...)` and pulls `leader_name` / dialog from `REGIONS[region_id]`. Identity preserved.

## Verification

End-to-end smoke test:
1. New world → walk to nearest town, find flag in square (or city center for small).
2. E on flag → Town Menu opens. Confirm name, biome, tier 0, region label, 2-4 needs listed (food/wood/stone/metal mix).
3. Stack wheat in inventory, click `+ALL` on the food need. Need decrements; gold and town reputation go up.
4. Walk to capital town of the region → find castle structure. Find LeaderNPC inside. E to talk → dialog shows region overview with member town reps.
5. Satisfy ALL needs of a town. Wait through 5 in-game days (5 wraps of `time_of_day`). Confirm tier-up toast and a new building appears at the next growth slot.
6. Save → reload. Confirm tier, reputation, supplied progress, grown_buildings all persist. Walk back to the town, confirm the grown building is still there.
7. Place a chest inside the city. Trigger another tier-up. Confirm the chest is not destroyed (growth slot scan skipped occupied tiles).

## Critical files to modify

- `cities.py` — CITY_CONFIGS, _build_single_city, _place_town_square, new `castle` variant, `LeaderNPC` class
- `world.py` — day_count, update_time, init_towns hook, town_centers
- `save_manager.py` — towns/regions tables, day_count column, save/load wiring
- `main.py` — E-key flag branch, _close_all_ui
- `player.py` — get_nearby_town_flag, category inventory helpers
- `blocks.py` — TOWN_FLAG_BLOCK
- `renderer.py` — _draw_town_flag, castle draw helpers
- `UI/__init__.py` — TownMenuMixin wiring
- `UI/panels.py` — leader dialog branch
- `UI/handlers.py` — town_menu close + click routing
