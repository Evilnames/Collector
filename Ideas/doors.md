# Palace Doors

## Problem

Palaces don't actually place door *blocks* today. `_castle_door()` in
[cities.py:4190-4196](../cities.py#L4190-L4196) just carves a 2×2 archway:
foreground → AIR, background → `CASTLE_GATE_ARCH`. There are 21 palace types,
113 `_castle_door()` call sites in cities.py, and zero placed door blocks.

Door *blocks* exist as a system — toggle on click, 2-tall pairing — but only 7
styles, mostly Middle Eastern: `WOOD_DOOR`, `IRON_DOOR`, `COBALT_DOOR`,
`CRIMSON_CEDAR_DOOR`, `TEAL_DOOR`, `SAFFRON_DOOR`, plus single-state
`CHALET_DOOR`. Most palace types have no thematically appropriate door.

## Proposal — 8 new door types

Each new door is a closed/open pair = 16 new block IDs. **Next free ID = 1155**
(highest in use is `PICKERELWEED_BLOCK = 1154`). Reserve 1155–1170.

| New door (IDs)                          | Palace types                                    | Look                                                 |
|-----------------------------------------|-------------------------------------------------|------------------------------------------------------|
| `STUDDED_OAK_DOOR` 1155/1156            | castle, gothic, norse                           | Heavy oak planks, iron studs, strap hinges           |
| `VERMILION_DOOR` 1157/1158              | chinese, tang_imperial, song_palace, han_palace | Red lacquer + brass stud grid (classic Chinese gate) |
| `SHOJI_DOOR` 1159/1160                  | japanese, east_asian                            | Wood lattice + translucent rice paper                |
| `GILDED_DOOR` 1161/1162                 | french_baroque, italian                         | White panels with gold trim and rosette              |
| `BRONZE_DOOR` 1163/1164                 | byzantine                                       | Engraved bronze with cross icon                      |
| `SWAHILI_DOOR` 1165/1166                | east_african                                    | Carved frame with brass spikes (Zanzibar style)      |
| `SANDALWOOD_DOOR` 1167/1168             | south_asian, african                            | Densely carved teak with floral motifs               |
| `STONE_SLAB_DOOR` 1169/1170             | incan, mesoamerican                             | Trapezoidal stone slab with glyphs                   |

Re-use existing doors:

- mediterranean → `WOOD_DOOR`
- moorish, persian → `COBALT_DOOR`
- middle_eastern → `SAFFRON_DOOR` / `CRIMSON_CEDAR_DOOR`
- tibetan → `CRIMSON_CEDAR_DOOR`

## Implementation strategy

### 1. blocks.py
- Add 16 ID constants (1155–1170) in a new `# --- Palace doors ---` section.
- Add 16 `BLOCKS` dict entries (closed + "(Open)" suffix), `hardness=2`, color, drop=item id. Mirror the COBALT/CRIMSON_CEDAR/TEAL pattern at lines 2086–2091.
- Add all 8 *_OPEN ids to `OPEN_DOORS` set at line 1246.

### 2. items.py
- Add 8 new `place_block` items (one per door style) in the door section at lines 916–920.
- Add the 8 new `*_DOOR_CLOSED` ids to the imports at line 68.

### 3. crafting.py
- Add 8 Artisan Bench recipes alphabetically (recipes are sorted). Sample ingredient costs:
  - `Studded Oak Door` — lumber 2, iron_chunk 1
  - `Vermilion Door` — lumber 2, ruby 1, gold_nugget 1
  - `Shoji Door` — lumber 2, crystal_shard 1
  - `Gilded Door` — lumber 2, gold_nugget 2
  - `Bronze Door` — iron_chunk 2, gold_nugget 1
  - `Swahili Door` — lumber 2, gold_nugget 1, iron_chunk 1
  - `Sandalwood Door` — lumber 2, dirt_clump 1, ruby 1
  - `Stone Slab Door` — stone_chip 3, granite_slab 1

### 4. renderer.py
- Add 16 ids to imports (line 115–118 area).
- Add 16 `if bid == X_DOOR_CLOSED/OPEN` drawing blocks after line 2139, mirroring SAFFRON_DOOR's 32×32 pattern. Open variant = 8px-wide hinge sliver.
- Add 8 *_DOOR_OPEN ids to the door-with-bg list at lines 16125–16127 (so the archway shows behind the open door).
- Add 16 ids to TERRAIN_IDS at line 19315 area, and again at line 19429 (two minimap lists).

### 5. player.py
- Add 16 ids to import list (line 5–9).
- Add 16 ids to `_BG_DISALLOWED` set at lines 87–90.
- Add 8 `(closed, opened)` tuples to the toggle list at line 1260 — they auto-pair with adjacent door for 2-tall behavior.

### 6. cities.py — wire into palace placement
- Update `_castle_door(world, bx, sy, door_block=None)`:
  - Keep current archway carve (AIR fg, CASTLE_GATE_ARCH bg).
  - If `door_block` given, write the closed door block to fg at sy-1 and sy-2 (so it sits inside the archway).
- Update each `_place_*_palace()` function: define a local `_DOOR = X_DOOR_CLOSED` near the top, pass to its `_castle_door()` calls.
- Shared piece helpers (`_piece_gatehouse`, `_piece_grand_hall`, `_build_round_tower`, etc.) take an optional `door_block` parameter, threaded through from the palace function.
- Tower archways and outer-wall walkthroughs **stay bare** (no door block) — they're not entrances, they're passes. Only the main palace-piece entrances get doors.

## Sequencing

Suggested order — each step compiles independently:

1. blocks.py constants + BLOCKS + OPEN_DOORS
2. items.py items
3. crafting.py recipes
4. renderer.py imports + drawing + bg-list + minimap
5. player.py imports + _BG_DISALLOWED + toggle
6. cities.py `_castle_door()` signature + per-palace wiring (do 1–2 palace types first to validate the approach, then the rest)

After each step, run `python -c "import main"` to catch import errors early.

## Open questions

- Should towers/secondary passes also get doors, or stay open archways? *(Current plan: stay open.)*
- Should castle gardens (`_place_castle_garden`) get doors too? *(Current plan: no — it's a garden.)*
- Crafting ingredients above are guesses — match against existing door costs (cobalt=2 lumber+1 crystal+1 gold; saffron=2 lumber+2 gold) before locking in.
