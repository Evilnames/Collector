# Living Oceans

Ocean biomes currently generate as completely featureless voids — the same `WATER` block (ID 25) fills from `SURFACE_Y=45` all the way to `WORLD_H=225` (180 blocks deep), with a flat sand floor and no creatures, plants, or visual differentiation. This plan layers the ocean into four distinct depth zones, each with unique visuals, creatures, and collectibles. Progression is gated behind diving gear and a new research column.

---

## Depth Zone Definitions

Based on `SURFACE_Y = 45`:

| Zone | Y range | Depth | Access |
|------|---------|-------|--------|
| Tidal | 45–60 | 0–15 | Free |
| Reef | 60–95 | 15–50 | Diving Helmet |
| Twilight | 95–155 | 50–110 | Full Suit + Oxygen Tank |
| Deep | 155–225 | 110–180 | Advanced Gear + Research |

---

## Phase 1 — Depth Zone Helper

**File:** world.py

Add a module-level function `get_ocean_depth_zone(y: int) -> str` returning `"tidal"`, `"reef"`, `"twilight"`, or `"deep"` based on y relative to `SURFACE_Y`. Imported by player.py, fish.py, and the renderer.

---

## Phase 2 — New Ocean Blocks

**File:** blocks.py (new constants at 1262+, entries in `BLOCKS` dict)

| Constant | ID | Purpose |
|---|---|---|
| `CORAL_FRAGMENT_BLOCK` | 1262 | Player-placed seed for coral gardening |
| `CORAL_GROWING` | 1263 | Stage 1 growth (intermediate) |
| `CORAL_FULL` | 1264 | Mature harvested coral |
| `KELP_BLOCK` | 1265 | Tall underwater plant (tidal/reef) |
| `SEASHELL_BLOCK` | 1266 | Collectible shell node on ocean floor |
| `SEA_ANEMONE` | 1267 | Decorative reef block |
| `BIOLUME_DEEP_BLOCK` | 1268 | Deep-zone glowing organism — add to `LIGHT_EMITTERS` (color `(30, 210, 195)`) |
| `OCEAN_ROCK` | 1269 | Encrusted rock for twilight/deep floors |

Drop tables: `CORAL_FULL` drops `"coral_fragment"` items; `SEASHELL_BLOCK` triggers shell generation; `BIOLUME_DEEP_BLOCK` drops `"glowing_spore"`.

---

## Phase 3 — Visual Depth Differentiation

**Files:** Render/worldScene/scene.py (~line 321), Render/surface/biome.py

Extend the water rendering conditional to call `get_ocean_depth_zone(by)` when inside an ocean biome and pick a zone color:

- Tidal: `(40, 120, 200)` — bright clear blue
- Reef: `(25, 90, 170)` — rich blue
- Twilight: `(15, 55, 120)` — dark blue
- Deep: `(8, 20, 70)` — near-black with cyan biolume shimmer

Draw a semi-transparent dark overlay rect (alpha 0–140 proportional to depth) over the player's viewport when submerged below the tidal zone.

---

## Phase 4 — Ocean World Generation

**File:** world.py — extend `_fill_chunk()` (~line 822)

Add `_spawn_ocean_floor_decor(chunk, y, biome)` called after placing WATER blocks at ocean floor:

- **Tidal floor** (y 58–60): sand bottom; scatter `SEASHELL_BLOCK` (10%), `KELP_BLOCK` (8%)
- **Reef floor** (y 90–95): sand/gravel; scatter `CORAL_FULL` (15%), `SEA_ANEMONE` (10%), `KELP_BLOCK` (12%), `SEASHELL_BLOCK` (6%)
- **Twilight floor** (y 148–155): gravel/stone; sparse `OCEAN_ROCK` (8%), rare `KELP_BLOCK` (3%)
- **Deep floor** (y 220–225): bare stone; `BIOLUME_DEEP_BLOCK` clusters (12%), `OCEAN_ROCK` (10%)

---

## Phase 5 — Seashell Collectible System

**New file:** seashells.py (follows rocks.py pattern exactly)

```python
@dataclass
class Seashell:
    uid: str
    species: str
    rarity: str
    depth_zone: str       # "tidal" | "reef"
    color: tuple
    pattern: str
    size_cm: float
    biome_found: str
    seed: int

SHELL_TYPES = {
    # Tidal (7 species)
    "cowrie":     { "depth_zone": "tidal", "rarity_pool": ["common","common","uncommon"], ... },
    "cone":       { "depth_zone": "tidal", "rarity_pool": ["common","uncommon"], ... },
    "scallop":    { "depth_zone": "tidal", "rarity_pool": ["common","common","uncommon"], ... },
    "clam":       { "depth_zone": "tidal", "rarity_pool": ["common"], ... },
    "periwinkle": { "depth_zone": "tidal", "rarity_pool": ["common"], ... },
    "limpet":     { "depth_zone": "tidal", "rarity_pool": ["common","uncommon"], ... },
    "whelk":      { "depth_zone": "tidal", "rarity_pool": ["uncommon"], ... },
    # Reef (8 species)
    "oyster":     { "depth_zone": "reef",  "rarity_pool": ["common","uncommon"], ... },
    "abalone":    { "depth_zone": "reef",  "rarity_pool": ["uncommon","rare"], ... },
    "murex":      { "depth_zone": "reef",  "rarity_pool": ["uncommon","rare"], ... },
    "nautilus":   { "depth_zone": "reef",  "rarity_pool": ["rare","epic"], ... },
    "triton":     { "depth_zone": "reef",  "rarity_pool": ["rare"], ... },
    "volute":     { "depth_zone": "reef",  "rarity_pool": ["rare","epic"], ... },
    "turritella": { "depth_zone": "reef",  "rarity_pool": ["uncommon"], ... },
    "marginella": { "depth_zone": "reef",  "rarity_pool": ["rare","epic"], ... },
}
SHELL_TYPE_ORDER = [...]   # tidal first, then reef, common→legendary
```

`SeashellGenerator.generate(bx, by, biome)` instantiates a `Seashell`. Breaking `SEASHELL_BLOCK` calls the generator and drops the result as a `DroppedItem`.

Requires: save_manager.py (`seashells` table, matching fossils pattern), UI/collections.py (Seashells tab), UI/help.py (codex entries).

---

## Phase 6 — Ocean Fish Expansion

**File:** fish.py

1. Add `ocean_zone: str = ""` field to `Fish` dataclass (empty = non-ocean fish, no breakage).

2. Add ~20 new species with `"biome_affinity": ["ocean"]` and a new `"ocean_zone"` key:
   - **Reef (10):** clownfish, moorish_idol, lionfish, parrotfish_reef, grouper, blue_tang, damselfish, wrasse, hawksbill_companion, sergeant_major
   - **Twilight (6):** lanternfish, flashlight_fish, oarfish, leafy_sea_dragon, banded_sea_krait, coelacanth
   - **Deep (4):** anglerfish, gulper_eel, barreleye, fangtooth

3. Add to `FISH_BIOME_GROUPS`: `("Ocean Reef", [...])`, `("Ocean Twilight", [...])`, `("Ocean Deep", [...])`.

4. `FishGenerator.generate()` — add optional `ocean_zone: str = ""` param; filter to matching ocean species when set.

5. player.py fishing: detect `_fishing_biome == "ocean"`, compute `ocean_zone = get_ocean_depth_zone(int(self.y))`, pass to generator.

---



## Phase 8 — Diving Gear & Research

**File:** items.py — four new equipment items:

| Key | Slot | Unlocks | Crafted from |
|---|---|---|---|
| `"diving_helmet"` | head | reef zone | 4 glass + 2 iron + 1 leather |
| `"diving_suit"` | body | — (needed with tank) | 6 leather + 3 iron |
| `"oxygen_tank"` | offhand | twilight zone (with suit) | 5 iron + 1 copper |
| `"advanced_diving_gear"` | head | deep zone | helmet + suit + tank |

**File:** research.py — column 22 `"Marine Biology"`:
- Row 0: `"ocean_fishing"` — unlocks ocean biome fishing
- Row 1: `"coral_gardening"` — unlocks coral fragment placement
- Row 2: `"deep_diving"` — unlocks twilight zone (requires full gear)
- Row 3: `"abyss_access"` — unlocks deep zone

**File:** player.py — `_get_accessible_ocean_zone(self) -> str` checks gear + research, returns max accessible zone. Show HUD message `"Need [item] to dive deeper"` when below limit.

---

## Phase 9 — Rendering

**Files:** Render/worldScene/scene.py, new Render/ocean.py

Draw functions for new blocks:
- `draw_coral_fragment` — small pink/orange nub
- `draw_coral_growing` — branching mid-size coral
- `draw_coral_full` — large vivid branching coral with polyp dots
- `draw_kelp` — tall dark-green stalk with wavy leaves
- `draw_sea_anemone` — circular tentacle fan (bright orange/purple)
- `draw_biolume_deep` — dark dome with cyan inner glow (reuse BIOLUME style)
- `draw_ocean_rock` — grey boulder with barnacle dots
- `draw_seashell_block` — small shell silhouette (cone/cowrie in tidal, nautilus/abalone in reef)

Underwater darkness overlay: after main block render loop, if player y > SURFACE_Y + 5 and biome is ocean, blit `(0, 0, 20)` rect at alpha proportional to depth (max ~140 at deep zone).

---

## Files to Touch

| File | Changes |
|---|---|
| blocks.py | 8 new block IDs (1262–1269), BLOCKS entries, LIGHT_EMITTERS update |
| items.py | 4 diving gear items, `"coral_fragment"` item |
| world.py | `get_ocean_depth_zone()`, `_spawn_ocean_floor_decor()`, `_coral_growth` dict + tick |
| fish.py | `ocean_zone` dataclass field, 20 new ocean species, 3 new FISH_BIOME_GROUPS |
| player.py | `_get_accessible_ocean_zone()`, fishing depth detection, zone boundary enforcement |
| research.py | Column 22 "Marine Biology" (4 rows) |
| save_manager.py | `seashells` table, `coral_growth` table |
| Render/worldScene/scene.py | Zone water tinting, underwater darkness overlay |
| UI/collections.py | Seashells codex tab |
| **New:** seashells.py | `Seashell` dataclass, `SHELL_TYPES` (15 species), `SeashellGenerator` |
| **New:** Render/ocean.py | Draw functions for all 8 new ocean blocks |

---

## Verification

1. Find ocean biome, wade in — verify tidal water is brighter than surrounding land water
2. Swim to reef depth without gear — confirm HUD message "Need diving_helmet to go deeper"
3. Craft + equip diving_helmet — find new reef fish (clownfish, blue_tang) and seashells
4. Break a `SEASHELL_BLOCK` — verify shell appears in collections codex
5. Place `CORAL_FRAGMENT_BLOCK` in reef zone — wait for 3-stage growth; harvest → drops fragments + chance pearl
6. Craft full diving suit + oxygen tank — verify twilight access; catch lanternfish, coelacanth
7. Complete `"abyss_access"` research + advanced gear — see biolume glow; catch anglerfish
8. Save and reload — seashells collection and coral growth state persist
