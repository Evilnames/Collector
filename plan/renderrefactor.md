# Codebase Split Plan

## Goal
Break the largest, most-modified files into focused modules. Each chunk is a single session's work. Stop at any boundary — every chunk ships independently.

## Most-modified files (by commit count)
| File | Lines | Commits |
|------|-------|---------|
| renderer.py | 19,859 | 28 |
| player.py | 2,329 | 27 |
| main.py | 1,702 | 25 |
| world.py | 3,066 | 24 |
| crafting.py | 2,725 | 24 |
| save_manager.py | 2,332 | 23 |
| items.py | 2,316 | 23 |
| blocks.py | 2,906 | 21 |
| cities.py | 8,710 | 15 |

---

## Pattern A — Standalone functions (renderer, world helpers, crafting data)
Extract method bodies to module-level functions. Thin wrapper stays in the original class.

```python
# Render/npcs.py
def draw_npc_soldier(screen, sx, sy, npc): ...

# renderer.py — wrapper stays, body moves out
def _draw_npc_soldier(self, sx, sy, npc):
    from Render.npcs import draw_npc_soldier
    draw_npc_soldier(self.screen, sx, sy, npc)
```

## Pattern B — Mixin classes (save_manager, player)
Split class methods into mixin classes that are inherited.

```python
# save_collections.py
class SaveCollectionsMixin:
    def _save_rocks(self, con, player): ...
    def _save_wildflowers(self, con, player): ...

# save_manager.py
from save_collections import SaveCollectionsMixin
class SaveManager(SaveCollectionsMixin): ...
```

## Pattern C — Data modules (items, blocks, crafting)
Split the data dict/list definitions into category files. Import and merge in the main file.

```python
# items_food.py
FOOD_ITEMS = { "bread": {...}, "soup": {...} }

# items.py
from items_food import FOOD_ITEMS
ITEMS = { **FOOD_ITEMS, **MATERIAL_ITEMS, ... }
```

---

# FILE: renderer.py (19,859 lines)

Already has `Render/birds.py`, `Render/insects.py`, `Render/dogs.py`, `Render/lights.py`. All new modules follow Pattern A.

## Group A — NPCs (target: `Render/npcs.py`, ~1,800 lines total)

### [x] A1 — Service NPCs (~210 lines, 17504–17715)
- `_draw_npc_quest`, `_draw_npc_trade`, `_draw_npc_herbalist`, `_draw_npc_jeweler`
- `_draw_npc_royal_curator`, `_draw_npc_royal_florist`, `_draw_npc_royal_jeweler`
- `_draw_npc_royal_paleontologist`, `_draw_npc_royal_angler`
- `_draw_npc_merchant`, `_draw_npc_outpost_keeper`
- **Test:** Visit a city, open shops, talk to quest/royal NPCs.

### [x] A2 — Workers & Leader (~565 lines, 17716–18282) - worker.py
- `_draw_npc_soldier` (17716–17832)
- `_draw_npc_chef`, `_draw_npc_monk` (17832–17873)
- `_draw_npc_leader` (17873–18217 — 344 lines, do not split)
- `_draw_npc_farmer`, `_draw_npc_villager`, `_draw_npc_child` (18217–18282)
- **Test:** Walk city streets, verify soldier, chef, monk, leader, farmer, villager, child.

### [x] A3 — Guard System & Weapons (~328 lines, 18283–18610) - guardsystem.py
- `_draw_npc_guard`, all `_guard_*` helpers, all `_draw_weapon_*`, `_draw_shield`
- Move all together — these call each other.
- **Test:** Walk city walls, verify guards with equipment, helmets, weapons.

### [x] A4 — Social NPCs (~187 lines, 18611–18797) - socialnpc.py
- `_draw_npc_elder`, `_draw_npc_beggar`, `_draw_npc_noble`, `_draw_npc_pilgrim`
- `_draw_npc_drunkard`, `_draw_npc_blacksmith`, `_draw_npc_innkeeper`, `_draw_npc_scholar`
- **Test:** Find elder, beggar, noble, inn — verify render.

## Group B — Wild Animals (target: `Render/wild_animals.py`, ~552 lines)

### [x] B1 — Forest & plains (~246 lines, 16777–17023) - forestAnimal.py
- `_draw_deer`, `_draw_boar`, `_draw_rabbit`, `_draw_turkey`, `_draw_wolf`, `_draw_bear`
- **Test:** Walk forest/plains biomes.

### [x] B2 — Wetland & mountain (~306 lines, 17023–17329) - wetlandAnimal.py
- `_draw_duck`, `_draw_elk`, `_draw_bison`, `_draw_fox`, `_draw_moose`, `_draw_bighorn`
- `_draw_pheasant_animal`, `_draw_warthog`, `_draw_musk_ox`, `_draw_crocodile`, `_draw_goose`, `_draw_hare`
- **Test:** Visit swamp/savanna/mountain biomes.

## Group C — Livestock (target: `Render/livestock.py`, ~588 lines)

### [x ] C1 — Farm animals (~253 lines, 18798–19051) - farmanimal.py
- `_draw_sheep`, `_draw_goat`, `_draw_cow`, `_draw_chicken`
- **Test:** Visit a farm.

### [x ] C2 — Large animals (~335 lines, 19052–19386) - largeAnimal.py
- `_draw_horse`, `_draw_dog`, `_draw_snow_leopard`, `_draw_mountain_lion`, `_draw_tiger`
- **Test:** Visit stables, find big cats.

## [x ] - Group D — Vehicles (target: `Render/vehicles.py`, ~174 lines, 17330–17503)
- `draw_arrows`, `draw_automations`, `draw_farm_bots`
- `draw_backhoes`, `_draw_backhoe`, `_fmt_fuel_time`
- `draw_elevator_cars`, `draw_minecarts`
- **Test:** Ride minecart, use backhoe, run elevator.

## Group E — HUD & Overlays (target: `Render/hud.py`, ~450 lines)

### [ ] E1 — Indicators (~80 lines, 19387–19436) - Render/Hud/indicator.py
- `draw_mining_indicator`, `draw_place_indicator`
- **Test:** Mine a block, place a block.

### [ ] E2 — Float texts & dropped items (~60 lines, 19438–19462 + 19821–19838) - Render/Hud/floatText.py
- `add_float_text`, `tick_float_texts`, `draw_float_texts`, `draw_dropped_items`
- **Test:** Break a block, pick up an item.

### [ ] E3 — Weather & world overlays (~80 lines, 19463–19524) - Render/Hud/weather.py
- `draw_farm_sense`, `draw_water_overlay`, `draw_rain`
- **Test:** Wade in water, trigger rain.

### [ ] E4 — Lighting & minimap (~225 lines, 19525–19820) - Render/Hud/lighting.py
- `_build_block_gradient`, `draw_lighting`
- `_build_mm_color_table`, `_rebuild_minimap`, `draw_minimap`
- **Test:** Check minimap, go underground at night.

## Group F — World Scene (target: `Render/world_scene.py`, ~450 lines)
Do after Groups A–E so callees are already extracted.

### [ ] F1 — Display objects (~330 lines, 16465–16628) - Render/worldScene/art.py
- `_draw_pottery_displays`, `_draw_sculpture_at`, `_draw_all_sculptures`
- `_draw_tapestry_at`, `_draw_all_tapestries`, `_draw_garden_blocks`, `_draw_wildflower_displays`
- **Test:** Visit cities/interiors with pottery, sculptures, tapestries.

### [ ] F2 — Core draw loop (~120 lines, 16201–16464 + 16629–16776) - Render/worldScene/player.py
- `draw_world`, `draw_player`, `draw_entities`
- **Test:** Full overworld + underground + city playthrough.

## Group G — Surface Builders (target: `Render/surface_builders.py`, ~600 lines)

### [ ] G1 — Terrain variants (~190 lines, 15924–16148) - Render/surface/terrain.py
- `_build_log_variants`, `_build_leaf_variants`, `_build_fruit_cluster_variants`
- `_build_grass_variants`, `_build_dirt_variants`, `_build_sand_variants`, `_build_snow_variants`
- **Test:** Walk overworld — logs, leaves, grass, dirt, sand, snow all show variants.

### [ ] G2 — Resource & biome surfaces (~85 lines, 15803–15924) - Render/surface/biome.py
- `_build_water_surfs`, `_build_resource_hint_surfs`
- `_build_biome_resource_hint_surfs`, `_build_biome_stone_surfs`
- **Test:** Check water, resource icons on minimap.

### [ ] G3 — Flags & sky (~80 lines, 15838–15924 + 16158–16200) - - Render/surface/flags.py
- `_get_town_flag_surf`, `_get_outpost_flag_surf`
- `_build_sky_surf`, `_build_night_sky_surf`, `_sky_night_alpha`
- **Test:** Visit town/outpost flag, watch day/night sky.

### [ ] G4 — Background surfaces & camera (~110 lines) - - Render/surface/surfaceAndCamera.py
- `_build_bg_darken_surf`, `_build_bg_block_surfs`, `_build_cave_wall_surf`
- `_build_tilled_soil_surfs`, `update_camera`
- **Test:** Enter cave, look at tilled soil.

## [x] Group H — Block Surfaces (the monster, ~15,200 lines, 558–15788)
`_build_block_surfs` replaced by `Render/blockRenderHandler.py` dispatcher + 6 category files. Shared helpers + mushroom renderer in `Render/block_helpers.py`. renderer.py shrank from 16,674 → 938 lines.

### [x] H1 — Terrain blocks → `Render/blocks_terrain.py` (372 lines)
Cave terrain, ores, deposits, sapling, mushrooms.

### [x] H2 — Wood & structural → `Render/blocks_wood.py` (808 lines)
Ladder, fences, all door variants, stairs, chest, bird blocks, wood/stone panels.

### [x] H3 — Crops & flora → `Render/blocks_crops.py` (2,160 lines)
All food crops, herb bushes, wildflowers, desert plants, coffee, grapes, flax, cotton.

### [x] H4 — Crafting stations → `Render/blocks_crafting.py` (1,023 lines)
All processing stations: bakery, wok, kilns, pottery wheel, forge, spinning wheel, loom, etc.

### [x] H5 — Decorative & containers → `Render/blocks_decor.py` (6,043 lines)
Garden ornamentals, tapestries, wetland plants, alpine furnishings, Greek artifacts, lighting, flags.

### [x] H6 — Structures & palace → `Render/blocks_structures.py` (6,791 lines)
Stone/brick tiles, cathedral glass, Moorish arch, Renaissance palace, Asian/cultural architecture, MCM blocks.

---

# FILE: cities.py (8,710 lines)

## Group I — Quests (~355 lines)

### I1 — Quest builders (~355 lines, 178–532)
All `_build_*_quest` and `*_quest_display`/`*_quest_hint` functions → `cities_quests.py`
- `_build_wf_quest`, `wf_quest_display`, `wf_quest_hint`
- `_build_gem_quest`, `gem_quest_display`, `gem_quest_hint`
- `_build_quest`, `_build_prestige_*`, `_build_royal_*`
- `fossil_quest_display`, `fish_quest_display`, `quest_display`, `quest_hint`
- **Test:** Accept a quest from any NPC type, verify quest text displays.

## Group J — NPC Classes (~1,600 lines)

### J1 — Base & ambient NPCs (~280 lines, 533–808)
`NPC`, `AmbientNPC`, `FarmerNPC`, `VillagerNPC`, `ChildNPC`, `GuardNPC`, `ElderNPC`, `BeggarNPC` → `cities_npc_base.py`
- **Test:** Walk city, all ambient NPCs move and exist.

### J2 — Quest-giver NPCs (~700 lines, 809–~1500)
Rock quest NPC, wildflower quest NPC, gem quest NPC, fossil NPC, fish NPC, prestige variants → `cities_npc_quest.py`
- **Test:** Accept quests, complete them, verify reward logic.

### J3 — Shop & service NPCs (~500 lines, ~1500–~2000)
Trade NPC, merchant, herbalist, jeweler, all royal service NPCs, outpost keeper → `cities_npc_shops.py`
- **Test:** Buy/sell from all shop types.

## Group K — City Builder (~3,100 lines)

### [ ] K1 — Building configs & helpers (~600 lines)
`CITY_CONFIGS`, building lists, NPC slot definitions, placement helpers that don't fit a palace → `cities_configs.py`
- **Test:** Generate a new world, cities spawn with correct building types.

### [ ] K2 — City layout & blocks (~1,200 lines)
`_build_single_city` + road/wall/floor placement → `cities_builder.py`
- **Test:** Cities have correct roads, walls, floors in all biomes.

### [ ] K3 — City population (~600 lines)
NPC spawning within a city, shop stock assignment, guard patrol routes → `cities_population.py`
- **Test:** Cities have correct NPC types and counts.

### [ ] K4 — Castle & outpost (~300 lines, 5158–5324)
`_castle_templates`, `_place_castle`, `_place_castle_garden`, `_palace_clear_terrain`, `_palace_npc_at`, `_populate_castle` → `cities_castle.py`
- **Test:** Find a castle, verify structure and NPCs.

## Group L — Palaces (~3,400 lines)
One palace file per session. Each palace is self-contained with its own inner helpers.

### [ ] L1 — Mediterranean & Gothic (~650 lines, 5325–5694 + 6500–6814)
`_place_mediterranean_palace`, `_place_gothic_palace` → `cities_palaces_european.py`

### [ ] L2 — Norse, Byzantine, French Baroque (~640 lines, 6384–6500 + 6814–6972 + 8223–8367)
`_place_norse_hall`, `_place_byzantine_palace`, `_place_french_baroque_palace` → append to `cities_palaces_european.py`

### [ ] L3 — East Asian (~500 lines, 5525–5694 + 7165–7327)
`_place_east_asian_palace`, `_place_japanese_palace` → `cities_palaces_asian.py`

### [ ] L4 — Chinese palaces (~900 lines, 7327–7945)
`_place_chinese_palace`, `_place_tang_palace`, `_place_song_palace`, `_place_han_palace` → append to `cities_palaces_asian.py`

### [ ] L5 — South & Central Asian (~800 lines, 5694–5861 + 6972–7165)
`_place_south_asian_palace`, `_place_tibetan_palace` → `cities_palaces_south_asian.py`

### [ ] L6 — Middle Eastern & Moorish (~500 lines, 6039–6384 + 8508–8651)
`_place_moorish_palace`, `_place_middle_eastern_palace`, `_place_persian_palace` → `cities_palaces_middle_east.py`

### [ ] L7 — African & Mesoamerican (~620 lines, 6657–6814 + 7945–8223 + 8367–8508)
`_place_african_palace`, `_place_east_african_palace`, `_place_mesoamerican_palace`, `_place_incan_palace` → `cities_palaces_other.py`

**Test for each L chunk:** Generate world, find a city with that palace type, verify it renders and populates.

---

# FILE: world.py (3,066 lines)

Pattern A — move method bodies to module-level functions, pass `world` (self) explicitly.

## [ ] Group M — Cave Generation (~350 lines, 1083–1416) → `world_caves.py`
- `_gen_caves`, `_biome_cave_params`, `_circle_offsets`, `_carve_network`
- `_cave_ca_smooth`, `_mark_cracked_ceilings`, `_place_natural_columns`, `_try_place_column`
- `_place_speleothems`, `_carve_chimneys`, `_carve_geodes`, `_place_cave_flora`
- `_place_gravel`, `_place_cave_mushrooms`
- **Test:** Generate world, go underground — caves exist and look correct.

## Group N — Tree Generation (~450 lines, 1801–2265) → `world_trees.py`

### [ ] N1 — Tree helpers & first batch (~250 lines, 1801–2066)
- `_place_canopy`, `_scatter_fruit_clusters`, `_add_branch_stubs`, `_add_root_flare`, `_place_trunk`
- `_grow_oak`, `_grow_pine`, `_grow_birch`, `_grow_jungle`, `_grow_willow`, `_grow_redwood`
- `_grow_palm`, `_grow_acacia`, `_grow_dead`, `_grow_mushroom`, `_grow_maple`, `_grow_cherry`
- `_grow_cypress`, `_grow_baobab`
- **Test:** New world has forests — oak, pine, birch, palm etc. all appear.

### [ ] N2 — Remaining tree types (~200 lines, 2066–2265)
- `_grow_mangrove`, `_grow_spruce`, `_grow_ginkgo`, `_grow_banyan`
- `_grow_pear`, `_grow_fig`, `_grow_citrus`, `_grow_apple`, `_grow_pomegranate`
- `_dispatch_grow`, `_grow_tree`
- **Test:** Visit mangrove swamp, spruce forest, fruit tree groves.

## Group O — Animal Spawning (~480 lines, 2612–3078) → `world_spawning.py`

### O1 — Land & dog spawning (~300 lines, 2612–2970)
- `_spawn_animals`, `_spawn_dogs_for_chunk`, `_spawn_huntable_animals`
- `_spawn_animals_for_chunk`
- **Test:** New world has deer, wolves, boars, dogs near outposts.

### O2 — Bird & insect spawning (~180 lines, 2970–3078)
- `_spawn_birds`, `_spawn_birds_for_chunk`
- `_spawn_insects_for_chunk`, `_spawn_garden_insects_in_chunk`, `_add_garden_insects`
- `spawn_insects_near_garden`, `_spawn_insects`
- **Test:** Birds appear in trees, insects appear near gardens.

## Group P — World Updates (~430 lines) → `world_updates.py`

### P1 — Plant updates (~270 lines, 2266–2612)
- `update_saplings`, `update_crops`, `update_fruit_trees`, `update_soil`
- `update_leaves`, `update_compost_bins`
- **Test:** Plant a crop, wait for it to grow.

### P2 — World tick (~160 lines, 1668–1793 + 2427–2481)
- `update_time`, `_tick_light_traps`, `update_water`, `_drain_unsustained_water`
- `_has_sky_view`, `_adjacent_to_water`, `_update_rain`, `update_trade_blocks`
- **Test:** Watch day/night cycle, pour water and let it flow.

---

# FILE: crafting.py (2,725 lines)
Pattern C — data modules. All dicts imported and merged in the main `crafting.py`.

## Group Q — Cooking Recipes (~700 lines) → `crafting_cooking.py`
- Bakery, Wok, Steamer, Noodle Pot recipes (lines 1–253)
- **Test:** Open bakery station, all recipes visible and craftable.

## Group R — Grill, Clay & Desert (~450 lines) → `crafting_stations_a.py`
- BBQ Grill, Clay Pot, Desert Forge recipes (lines 254–455)
- **Test:** Open BBQ and clay pot, all recipes available.

## Group S — Industrial & Artisan (~1,400 lines) → `crafting_stations_b.py`
- Glass Kiln, Smithing Forge, Artisan Bench, all remaining station recipes (lines 456–2680)
- **Test:** Open forge and artisan bench, all recipes available.

## Group T — Core Logic (~100 lines, 2681–end)
Keep `match_recipe`, `craft_costs`, `can_craft`, `is_research_locked`, `can_craft_with_research` in `crafting.py`. Not worth moving — it's already small.

---

# FILE: save_manager.py (2,332 lines)
Pattern B — mixin classes.

## Group U — Schema (~490 lines, 285–774) → `save_schema.py`
Move `_create_tables` (huge SQL schema) into `class SaveSchemaMixin`.
- **Test:** New game creates database with all expected tables.

## Group V — Collection saves (~650 lines, 1065–1800) → `save_collections.py`
Move all `_save_rocks`, `_save_wildflowers`, `_save_fossils`, `_save_gems`, `_save_fish`, `_save_coffee_beans`, `_save_wine_grapes`, `_save_spirits`, `_save_tea_leaves`, `_save_textiles`, `_save_cheese_wheels`, `_save_jewelry`, `_save_sculptures`, `_save_tapestries`, `_save_pottery_pieces`, `_save_salt_crystals`, `_save_crafted_weapons`, `_save_bird_observations` into `class SaveCollectionsMixin`.
- **Test:** Save game, reload — all collections intact.

## Group W — Achievement & migration (~130 lines, 823–933)
Move `_merge_global_collection`, `_check_and_save_achievements`, `load_achievements`, `_maybe_migrate` into `class SaveAchievementsMixin`.
- **Test:** Earn an achievement, reload — achievement persists.

---

# Progress Tracker
## renderer.py
- [ x] A1 — Service NPCs
- [x ] A2 — Workers & Leader
- [x ] A3 — Guard System & Weapons
- [x ] A4 — Social NPCs
- [x ] B1 — Wild Animals: forest & plains
- [x ] B2 — Wild Animals: wetland & mountain
- [x] C1 — Livestock: farm animals
- [x] C2 — Livestock: large animals & big cats
- [x] D1 — Vehicles & Machines
- [x] E1 — HUD: Indicators
- [x] E2 — HUD: Float texts & dropped items
- [x] E3 — HUD: Weather & overlays
- [x] E4 — HUD: Lighting & minimap
- [x] F1 — World scene: display objects
- [x] F2 — World scene: core draw loop
- [x] G1 — Surface builders: terrain variants
- [x] G2 — Surface builders: resource & biome
- [x] G3 — Surface builders: flags & sky
- [x] G4 — Surface builders: background & camera
- [x] H1 — Block surfs: terrain
- [x] H2 — Block surfs: wood & structural
- [x] H3 — Block surfs: crops & flora
- [x] H4 — Block surfs: crafting stations
- [x] H5 — Block surfs: decorative & containers
- [x] H6 — Block surfs: structures & palace

## cities.py
- [ ] I1 — Quest builders
- [ ] J1 — Base & ambient NPCs
- [ ] J2 — Quest-giver NPCs
- [ ] J3 — Shop & service NPCs
- [ ] K1 — City configs & helpers
- [ ] K2 — City layout & blocks
- [ ] K3 — City population
- [ ] K4 — Castle & outpost
- [ ] L1 — Palaces: Mediterranean & Gothic
- [ ] L2 — Palaces: Norse, Byzantine, Baroque
- [ ] L3 — Palaces: East Asian
- [ ] L4 — Palaces: Chinese
- [ ] L5 — Palaces: South & Central Asian
- [ ] L6 — Palaces: Middle Eastern & Moorish
- [ ] L7 — Palaces: African & Mesoamerican

## world.py
- [ ] M — Cave generation
- [ ] N1 — Trees: helpers & first batch
- [ ] N2 — Trees: remaining types
- [ ] O1 — Spawning: land animals
- [ ] O2 — Spawning: birds & insects
- [ ] P1 — Updates: plant growth
- [ ] P2 — Updates: world tick

## crafting.py
- [ ] Q — Cooking recipes
- [ ] R — Grill, clay & desert
- [ ] S — Industrial & artisan

## save_manager.py
- [ ] U — Schema
- [ ] V — Collection saves
- [ ] W — Achievements & migration
