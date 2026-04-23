Ready for review
Select text to add comments on the plan
Coffee Bean Mini-Game — Implementation Plan
Context
Add a deep, multi-layered coffee system. The player finds and grows coffee in specific biomes, roasts it via a timing-based mini-game, blends different regional origins together, brews the blend using one of five methods, and drinks the result for a temporary buff. Flavor profiles are procedurally generated from origin biome × roast level × brew method, giving 35+ discoverable codex entries.

Architecture Overview
Coffee Bush (biome-specific) 
  → harvest → CoffeeBean object (state="raw", origin biome encoded)
  → Roaster mini-game → CoffeeBean (state="roasted", roast_level, roast_quality, flavor_notes set)
  → Blend Station → CoffeeBean (state="blended", merged flavor profile, component uids)
  → Brew Station + method → drinkable item (drip_coffee / espresso / etc.) → player buff
CoffeeBean objects are stored in player.coffee_beans (never the item inventory), identical pattern to Gemstone objects.

New File: coffee.py
CoffeeBean dataclass:

uid: str
origin_biome: str        # biodome string where cherry was harvested
variety: str             # "arabica" | "robusta" | "liberica"
state: str               # "raw" | "roasted" | "blended"
roast_level: str         # "green" | "light" | "medium" | "dark" | "charred"
roast_quality: float     # 0.0–1.0, set by mini-game performance
acidity: float           # 0.0–1.0 base attributes
body: float
sweetness: float
earthiness: float
brightness: float
flavor_notes: list       # ["chocolate", "citrus", ...] 2–4 strings
seed: int
blend_components: list   # [] for single-origin, [uid1, uid2] for blends
BIOME_FLAVOR_PROFILES dict — maps biodome → (acidity, body, sweetness, earthiness, brightness, variety):

Biome	acidity	body	sweetness	earthiness	brightness	variety
tropical	0.75	0.55	0.80	0.25	0.85	arabica
jungle	0.60	0.70	0.65	0.55	0.60	arabica
savanna	0.40	0.85	0.45	0.80	0.30	robusta
wetland	0.30	0.90	0.35	0.90	0.20	robusta
arid_steppe	0.55	0.65	0.50	0.70	0.40	liberica
canyon	0.50	0.75	0.40	0.85	0.35	liberica
beach	0.85	0.40	0.90	0.10	0.95	arabica
generate_flavor_notes(bean) — selects 2–4 strings from threshold-gated pools:

acidity > 0.6 → ["citrus", "lemon zest", "bright cherry", "green apple"]
body > 0.7 → ["dark chocolate", "molasses", "walnut", "heavy cream"]
sweetness > 0.7 → ["caramel", "honey", "ripe berry", "brown sugar"]
earthiness > 0.6 → ["cedar", "tobacco", "forest floor", "dried herb"]
brightness > 0.7 → ["floral", "jasmine", "bergamot", "stone fruit"]
Roast modulation: dark adds "smoky"/"roasted grain"; light adds "grassy"/"tea-like"; charred replaces all with ["ash", "bitter carbon"]
CoffeeGenerator class — seeded from world.seed, generate(biodome) creates a raw CoffeeBean with attributes from BIOME_FLAVOR_PROFILES + random.gauss(0, 0.08) noise.

COFFEE_TYPE_ORDER — list of all 35 "biome_roast" strings for the codex.

ROAST_LEVEL_DESCS, ROAST_COLORS — display helpers for UI.

blocks.py Changes
Add after BIRD_BATH_BLOCK = 210:

COFFEE_BUSH           = 211
COFFEE_CROP_YOUNG     = 212
COFFEE_CROP_MATURE    = 213   # special: mine → CoffeeBean object + coffee_seed drop
ROASTER_BLOCK         = 214
BLEND_STATION_BLOCK   = 215
BREW_STATION_BLOCK    = 216
Add to set constants:

COFFEE_BUSH → BUSH_BLOCKS
COFFEE_CROP_YOUNG → YOUNG_CROP_BLOCKS
COFFEE_CROP_MATURE → MATURE_CROP_BLOCKS, PERENNIAL_CROP_MATURE, MATURE_TO_YOUNG_CROP
ROASTER_BLOCK, BLEND_STATION_BLOCK, BREW_STATION_BLOCK → EQUIPMENT_BLOCKS
Add BLOCKS entries:

COFFEE_BUSH: hardness 0.5, color (60,100,40), drop coffee_seed
COFFEE_CROP_YOUNG: hardness 0.5, color (75,140,60), drop coffee_seed
COFFEE_CROP_MATURE: hardness 0.5, color (160,45,30), drop None (object-generating, handled in player._mine_block)
Equipment blocks: hardness 1.5, drops corresponding _item
items.py Changes
Add:

coffee_seed — place_block: COFFEE_CROP_YOUNG
coffee_cherry — edible, hunger_restore 4, color (170,40,30)
roaster_item, blend_station_item, brew_station_item — place_block their respective blocks
15 brew output items (3 quality tiers × 5 methods):
Base IDs: drip_coffee, espresso, pour_over, cold_brew, french_press
Fine tier: drip_coffee_fine, etc. (90s duration boost)
Superior: drip_coffee_superior, etc. (150% duration)
Each has: edible: True, hunger_restore: 6–10, coffee_buff: "focus" (etc.), coffee_buff_duration: float
world.py Changes
Import new block constants
Add COFFEE_BUSH to _BIOME_BUSHES for: tropical, jungle, savanna, wetland, arid_steppe, canyon, beach
Add COFFEE_CROP_YOUNG: COFFEE_CROP_MATURE to the crop maturation mapping in update_crops()
player.py Changes
Import CoffeeBean, CoffeeGenerator from coffee; import COFFEE_CROP_MATURE from blocks
__init__: add self.coffee_beans = [], self.discovered_coffee_origins = set(), self._coffee_gen = CoffeeGenerator(world.seed), self.active_buffs = {}
apply_save(): reconstruct coffee_beans and discovered_coffee_origins
_mine_block(): when block is COFFEE_CROP_MATURE, call _coffee_gen.generate(current_biodome), append to self.coffee_beans, also drop 1 coffee_seed into inventory
try_eat(): if item_data.get("coffee_buff"), store in self.active_buffs[buff_type] = {"duration": ..., "intensity": ...}
update(dt): tick active_buffs durations; if "endurance" active, reduce hunger drain by 40%
Apply "rush" buff (+25% move speed) in handle_input()
Apply "focus" buff (mining speed ×0.8) in block-break timing
Apply "strength" buff (+1 effective pick_power) when checking ore hardness
Apply "clarity" buff (+50% item pickup radius) in item collection range check
Roasting Mini-Game (ui.py)
State variables to add to UI.__init__:

self._roast_phase           = "select_bean"  # "select_bean" | "roasting" | "result"
self._roast_bean_idx        = None
self._roast_time            = 0.0
self._roast_total_time      = 30.0
self._roast_temp            = 0.0       # 0.0–1.0 drum temperature
self._roast_temp_vel        = 0.0       # rate of change
self._roast_heat_held       = False     # is player holding heat button?
self._roast_time_in_band    = 0.0       # seconds in [0.30, 0.80] band
self._roast_first_crack_hit = False
self._roast_second_crack_hit= False
self._roast_penalties       = 0
self._roast_event_flash     = None      # ("FIRST CRACK!", color, timer)
self._roast_stop_btn        = None
self._roast_select_rects    = {}
Phases:

"select_bean" — list of player.coffee_beans where state == "raw". Click a bean to start roasting. Shows origin biome, expected flavor profile preview.

"roasting" — the core mini-game:

Vertical temperature bar with colored zones: green [0.40–0.65], yellow [0.65–0.80], red [0.80–1.0]
Horizontal time bar showing progress across 30 seconds
Landmark markers at t=10 (first crack zone start), t=14 (end), t=22 (second crack)
Player holds SPACE (or mouse button on "HEAT" button) to increase temp: _roast_temp_vel += 0.025/frame; releases to cool: _roast_temp_vel -= 0.012/frame
At t=10: yellow flash "FIRST CRACK!" event; at t=22: red flash "SECOND CRACK!" event
Each second past t=22 with temp > 0.80 = +1 penalty
Player presses ENTER (or clicks "STOP") to end roast; roast_level determined by current temp at stop time
timing_score = time spent in [0.40, 0.65] during [t=10, t=14] / 4.0 seconds
temp_control_score = _roast_time_in_band / _roast_total_time
roast_quality = clamp(timing_score * 0.6 + temp_control_score * 0.4 - penalties * 0.15, 0.0, 1.0)
"result" — shows roast level, flavor notes, quality stars (1–5), roast description. DONE button returns to "select_bean". Bean state set to "roasted", discovered_coffee_origins.add(f"{biome}_{roast_level}").

Blend Station (ui.py)
Phases: "select_slots" → "result"

Shows 3 slots (2 required, 3rd optional) populated from player.coffee_beans where state == "roasted"
Each slot shows: origin biome name, roast level, 3 top flavor notes
"BLEND" button generates blended bean with weighted-average attributes, union of flavor notes (max 5), origin_biome = "blend", blend_components = [uid1, uid2, ...]
Input beans are consumed; blended bean appended to player.coffee_beans
Brew Station (ui.py)
Left: scrollable list of player.coffee_beans where state in ("roasted", "blended")
Right: 5 brew method buttons with description and amplification preview
"BREW" button: consumes bean, applies method amplification to select quality tier, adds output item to player inventory
Method amplification table:

Method	Amplifies	Output	Buff
drip	sweetness×1.3, brightness×1.2	drip_coffee	focus: mining +20%, 90s
espresso	body×1.5, acidity×1.3	espresso	rush: speed +25%, 45s
pour_over	acidity×1.4, brightness×1.4	pour_over	clarity: collect radius +50%, 60s
cold_brew	sweetness×1.4, body×1.2	cold_brew	endurance: hunger drain -40%, 120s
french_press	body×1.6, earthiness×1.4	french_press	strength: pick_power +1, 75s
Quality tier: roast_quality < 0.4 → base; 0.4–0.7 → _fine (+25% duration); > 0.7 → _superior (+50% duration).

Collection UI (ui.py)
Encyclopedia (Tab 1): Add category index 7 "COFFEE". Sub-filter = 7 biome buttons. Grid of 5 roast levels per biome. Locked = grayed bean. Unlocked shows: variety, flavor notes, best quality score for that origin+roast.

Collection (Tab 0): Add "coffee" filter. Displays coffee beans as a procedural brown-circle icon with roast level text.

Buff HUD: Small row of colored icons at bottom-right of screen showing active buff name + countdown timer.

save_manager.py Changes
New table:

CREATE TABLE IF NOT EXISTS coffee_beans (
    uid              TEXT PRIMARY KEY,
    origin_biome     TEXT,
    variety          TEXT,
    state            TEXT,
    roast_level      TEXT,
    roast_quality    REAL,
    acidity          REAL, body REAL, sweetness REAL, earthiness REAL, brightness REAL,
    flavor_notes     TEXT,  -- JSON list
    seed             INTEGER,
    blend_components TEXT   -- JSON list of uids
);
Add _save_coffee_beans(con, player) — DELETE + INSERT OR REPLACE pattern identical to _save_gems. Add _load_coffee_beans(con) in _load_player(). Add "coffee_beans" to new_game() delete list. Save/load discovered_coffee_origins as JSON list on the player table row (add column via ALTER TABLE fallback like other new columns).

crafting.py Changes
Add three shaped-grid crafting recipes to RECIPES for the equipment items (roaster_item, blend_station_item, brew_station_item) using wood, stone, iron ore combinations.

item_icons.py Changes
Add rendering functions for coffee_seed (small brown oval), coffee_cherry (red round food), and one shared render function for all brew output items (dark liquid in a cup shape). Wire into the _ICONS dispatch dict.

Implementation Sequence
blocks.py — new constants + set membership
items.py — new item definitions
coffee.py — new file: dataclass, generator, flavor system
player.py — storage, generation hook, buff system
save_manager.py — table + save/load
world.py — biome bush entries + crop maturation
crafting.py — equipment recipes
ui.py — roaster mini-game, blend station, brew station, collection tab, buff HUD
item_icons.py — coffee icons
Verification
Start game, find a tropical/jungle/savanna biome → confirm COFFEE_BUSH appears on surface
Break bush → get coffee_seed; plant seed → young crop grows to mature
Break mature crop → CoffeeBean object added to player.coffee_beans, coffee_seed added to inventory
Place roaster_item → open roaster UI → select raw bean → roasting phase: hold SPACE to heat, check temp bar responds, first crack event fires at t=10, STOP at medium temp → result shows flavor notes + quality stars
Roast 2 beans from different biomes → open blend station → fill both slots → BLEND → blended bean appears with merged notes
Open brew station → select blended bean → choose espresso → confirm espresso (or tiered variant) added to inventory
Eat espresso → rush buff activates, movement speed visibly increases, buff HUD shows countdown
Open collection tab → Coffee filter shows beans; encyclopedia Coffee tab shows discovered entries
Save and reload → all coffee beans, discovered origins, active buffs restore correctly