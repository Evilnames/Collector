# Static-analysis cleanup — status report

Generated 2026-05-16. Updated after batches 1–3.
Full per-item dumps live in `planning/_items_raw.txt` and `planning/_orphan_buckets.md`.

## Progress

| Metric | Start | After B1 | After B2 | After B3 | Status |
|---|---|---|---|---|---|
| Orphan items in `ITEMS` | 455 | 423 | 289 | **35** | 30 are scanner false-positives, 5 are tiny vestigial materials |
| Vulture findings (80%) | 27 | 7 | 7 | 7 | Unused locals remain — possibly incomplete features |
| Unreachable UI panels | 1 | 0 | 0 | 0 | Done |
| Module orphans | 14 | 14 | 14 | 14 | All expected (tests, dev scripts) |

## Batch 1 — Mechanical cleanup

- Deleted 32 vestigial weapon-tier items (`iron_*`/`gold_*`/`steel_*` parts) from an abandoned tier-system superseded by `player.smithed_parts` dicts.
- Removed dead `npc_inspect_open` flag from [UI/__init__.py](UI/__init__.py).
- Fixed `if False else …` ternary bug in [Render/blocks_structures.py:5727](Render/blocks_structures.py#L5727).
- Swept 20 unused imports/locals across UI modules, `cities.py`, `worldgen/plan.py`.

## Batch 2 — Scanner improvements + coffee fix

- **Real bug found:** [coffee.py:322](coffee.py#L322) — `BREW_METHODS` key was `"drip"` but every consumer expects `"drip_coffee"`. Renamed; this wires up 11 drip-coffee variants (base + tiered + 6 herb-combos) that had been producing keys nothing recognized.
- Upgraded the orphan scanner to detect dynamic key construction via f-strings — eliminated 134 false positives across cheese/beer/wine/spirits/mead/coffee/charcuterie/salt aging & brewing systems.

## Batch 3 — Knightly Order rank rewards + Royal Curator dynasty drops

The big one. Wired ~250 chapter-house / order / dynasty narrative items end-to-end.

- Added `UNIVERSAL_RANK_REWARDS` + `TRADITION_RANK_REWARDS` in [knightly_orders.py](knightly_orders.py). Player ranking up (Squire → Knight-Errant → Banneret → Marshal → Grandmaster) is granted a curated bundle of items — induction gear → chapter livery → marshal insignia → founder relics + royal regalia.
- Tradition-flavored extras layered on top: Templar gets blessing oils & rosary, Hospitaller gets pilgrim robe & lily standard, Cavalier gets royal court items, Samurai/Ghazi/Rajput/Horde get their cultural weapon parts (yari, ban-pou, rumh, kund, shamshir, dao).
- `grant_rank_rewards()` called from [UI/chapter_house.py:_ch_complete_trial](UI/chapter_house.py) — fires when a trial is passed. UI message lists first 3 items granted.
- Wired ~120 royal **dynasty heirlooms** as drops from `RoyalCuratorNPC` quest completions. Each completion grants 3 dynasty items, prioritized toward items the player owns fewest of — over repeated completions the player fills the dynasty collection naturally.

## Batch 3 results

Closed 254 orphans across batches 2+3 (289 → 35).

## What remains (35 items)

### 30 scanner false positives — already functionally wired
After the [coffee.py:322](coffee.py#L322) `drip_coffee` fix, these are produced dynamically by `get_brew_output_id` via `f"{method}{tier}_{herb}"`:
- `cold_brew_dried_*` (6) — chamomile, garlic, ginger, lavender, mint, rosemary
- `drip_coffee_dried_*` (6)
- `espresso_dried_*` (6)
- `french_press_dried_*` (6)
- `pour_over_dried_*` (6)

The orphan scanner can't see them because their f-string has no literal prefix (`f"{method}_..."` starts with a `{}` placeholder). They are reachable in-game by brewing the corresponding method with a dried herb additive.

### 5 truly vestigial materials — small loose ends
| Item | Status |
|---|---|
| `jute_seed` | Defined but no `jute_crop` block to plant. `jute_fiber` works in [player.py:3162](player.py#L3162). Either add a jute crop block or delete the seed. |
| `kumis_flask` | Defined as edible but never crafted or sold. Cultural drink fixture; either wire to nomad outpost recipe or delete. |
| `seal_rivalry_token` | Order rivalry token — needs a rivalry-event drop hook, or move into a Grandmaster reward. |
| `soot` | Documented in [manuscripts.py:3](manuscripts.py#L3) as an ink ingredient but no recipe actually consumes it. Wire into ink recipes or delete. |
| `throne_ash` | Pyre/forge byproduct with no producer or consumer. Delete unless intended for a planned mechanic. |

## Module orphans (unchanged, all expected)

```
DataWork\export_birds.py
DataWork\extract_birds.py
DataWork\extract_species.py
Render\surface\__init__.py        (empty)
Render\worldScene\__init__.py     (empty)
generator\add_bauhaus_blocks.py
generator\batch_victorian.py
generator\new_block.py
test_crafting.py
test_logic.py
test_save_manager.py
test_water_sim.py
tools\update_food_nutrition.py
_scan_orphans.py
```

## Remaining vulture findings (7)

Unused locals — investigate as potential incomplete features:
- [UI/crafting.py:546](UI/crafting.py#L546) `selected_attr`
- [UI/herbalism.py:298](UI/herbalism.py#L298) `inv_scroll`
- [UI/hire_panel.py:160](UI/hire_panel.py#L160) `threshold_warn`
- [UI/worldgen_screen.py:229](UI/worldgen_screen.py#L229) `alpha_progress`
- [wine.py:305](wine.py#L305) `avg_pressure`
- [worldgen/history/sim.py:538](worldgen/history/sim.py#L538) `rebel_label`

Plus `DataWork/export_birds.py:6` unused `inspect` import (dev script, skip).

## Batch 4 — Quartermaster shop + incomplete-feature sweep

### Quartermaster shop tab (chapter house)

Added a togglable "Quartermaster" tab next to the existing Quest Board in the chapter house panel. The shop:
- Stocks items by rank tier (1..4); player can browse stock from any rank up to their effective rank.
- 112 items priced from 6g (squire trinkets) to 500g (founder relics).
- Click-to-buy with affordability check; gold deducted, item added to inventory.
- Mousewheel scrolling wired in [main.py:1787](main.py#L1787) MOUSEWHEEL dispatch.
- Tables `QUARTERMASTER_OFFERS` + helpers `quartermaster_offers_for_rank`, `quartermaster_buy` live in [knightly_orders.py](knightly_orders.py).
- UI helpers `_draw_tab_btn`, `_draw_quest_board`, `_draw_quartermaster` in [UI/chapter_house.py](UI/chapter_house.py).

This gives players a gold-based path to acquire chapter house content they missed on rank-up or want duplicates of.

### Incomplete features wired up (former vulture findings)

All 6 unused parameters were real incomplete features. Each is now functional:

| Where | What it does now |
|---|---|
| [UI/hire_panel.py:160](UI/hire_panel.py#L160) `upkeep_row` | `threshold_warn` produces a dim-gray "low concern" color tier between green (OK) and yellow (warning) |
| [UI/worldgen_screen.py:229](UI/worldgen_screen.py#L229) `_draw_kingdom_flags` | `alpha_progress` now animates flagpoles growing from base & flag fading in via alpha-blended surface |
| [worldgen/history/events.py:48](worldgen/history/events.py#L48) `text_kingdom_split` | Chronicle entries mention the rebel faction ("led by the Inner branch of House X") via passed `rebel_label` |
| [wine.py:305](wine.py#L305) `apply_press_result` | `avg_pressure` shapes extraction: gentle press favors aromatics, firm press extracts tannin + body |
| [UI/herbalism.py:297](UI/herbalism.py#L297) `_draw_station_ui` | `inv_scroll` paginates the herb grid (substrate for future scroll wheel) |
| [UI/crafting.py:545](UI/crafting.py#L545) `_draw_cooking_station` | Cleaned: `selected_attr` was vestigial param, removed from signature + 14 call sites |

**Vulture findings: 27 → 1** (remaining one is `inspect` import in `DataWork/export_birds.py`, a dev script — skip).

## Outstanding future work

1. **Live dynasty events** *(biggest remaining gap)* — currently dynasty items drop from RoyalCuratorNPC quest completions + the Quartermaster shop. A more immersive integration would tie them to live runtime events (coronation, royal marriage, death, succession, abdication) using existing chronicle data. Requires building a live-event scheduler that fires near the player's date, surfaces a notification, and grants thematically-tied dynasty items. Substantial standalone feature (~2-4 hrs).
2. **5 tiny vestigial materials** — `jute_seed`, `kumis_flask`, `seal_rivalry_token`, `soot`, `throne_ash`. Each is a one-line decision (wire or delete).
3. **30 coffee-herb scanner false positives** — items like `drip_coffee_dried_mint`. Confirmed functionally wired after the [coffee.py:322](coffee.py#L322) fix; scanner just can't see f-strings that start with `{var}` instead of a literal prefix. Cosmetic — `_scan_items.py` could be taught to handle this pattern.

