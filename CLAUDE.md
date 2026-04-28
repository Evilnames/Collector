# Project Guidelines

## File Size & Structure
Keep all files small. Break logic into focused functions that compose upward — small helpers roll up into mid-level functions, which roll up into top-level systems. If a file is getting long, split it.

## Readability
Write systems that are easy to read and follow at a glance. Prefer clear naming and flat, obvious control flow over clever abstractions. A new reader should be able to understand any system quickly.

## Data Definitions
Keep data that needs to be modified in clearly defined, easy-to-find structures (dicts, lists, constants). Data should be easy to mutate — avoid scattering configuration or values across logic. Centralize definitions so changes require editing one place.

---

## Architecture Map

### Entry Points
- **main.py** — Game loop, settings, input dispatch. `INSECT_DROP_TABLE` lives here.
- **constants.py** — All global engine numbers: `BLOCK_SIZE`, `WORLD_H`, `SURFACE_Y`, `CHUNK_W`, physics, `CITY_SPACING`.

### Block & Item Registries
- **blocks.py** — Block ID constants (0–999+) + `BLOCKS` dict (master metadata). Block sets: `YOUNG_CROP_BLOCKS`, `MATURE_CROP_BLOCKS`, `EQUIPMENT_BLOCKS`, `BUSH_BLOCKS`, `ALL_LOGS`, etc. Door/crop stage pairs.
- **items.py** — `ITEMS` dict (900+ items). Imports block IDs for recipe inputs.

### World & Terrain
- **world.py** — `World` class: chunks, entities, time-of-day. `_CROP_MATURE_MAP` (young→mature), ocean/island generation constants.
- **biomes.py** — `BIOMES` dict (biome → generation rules). `BIOME_ORE_MULTIPLIERS`, `BIODOME_TYPES`.
- **soil.py** — Soil moisture/fertility simulation.

### Player
- **player.py** — `Player` class: position, inventory, mining, equipment. `_BG_DISALLOWED`, `_DOOR_PAIRS`.

### Collectible Type Systems
Each system follows the same pattern: a typed class + a `*_TYPES` registry dict + a generator class.
- **fish.py** — `Fish` class, `FISH_TYPES` dict (40+ species), `FISH_BIOME_GROUPS`.
- **rocks.py** — `Rock` class, `ROCK_TYPES` dict (25+ types), `ROCK_BIOME_AFFINITY`.
- **gemstones.py** — `Gemstone` class, `GEM_TYPES` dict (22+ types with depth/cuts/optical effects).
- **fossils.py** — `Fossil` class, `FOSSIL_TYPES` dict (age tiers, depth, patterns).
- **wildflowers.py** — `Wildflower` class, flower type/color/rarity pools.
- **insects.py** — `Insect` base class + 40+ subclasses, `ALL_INSECT_SPECIES`.
- **birds.py** — `Bird` base class + 30+ subclasses, `ALL_SPECIES`. Flocking/perching behavior.

### Processed Collectible Systems
Each has a class, biome flavor profiles, and processing stage constants.
- **wine.py** — `Grape` class, `BIOME_GRAPE_PROFILES`, `CRUSH_STYLES`, `YEASTS`, `VESSELS`.
- **coffee.py** — `CoffeeBean` class, `BIOME_FLAVOR_PROFILES`, `PROCESSING_METHODS`, `ROAST_COLORS`, `GRIND_SIZES`.
- **beer.py** — `Beer` class, `BIOME_BEER_PROFILES`, `MASH_TYPES`, `HOP_ADDITIONS`, `YEAST_TYPES`, `BEER_TYPE_DESCS`, `BEER_BUFFS`.
- **tea.py** — `TeaLeaf` class, `BIOME_TEA_PROFILES`, `WITHER_METHODS`, `OXIDATION_ZONES`, `TEA_TYPE_BUFFS`, `HERBAL_ADDITIVES`.
- **spirits.py** — `BIOME_SPIRIT_PROFILES`, `BIOME_DISPLAY_NAMES`.
- **cheese.py** — `Cheese` class with aging, milk source, texture/flavor/aroma.
- **pottery.py** — `PotteryPiece` class, `CLAY_BIOME_PROFILES`, `_TEXTURE_NOTE_POOLS`, `_CODEX_BIOMES`.
- **salt.py** — `SaltCrystal` class, salt types, biome origins.
- **textiles.py** — `Textile` class, pattern/dye/weave generation.
- **jewelry.py** — `Jewelry` class, material + gemstone components.
- **weapons.py** — `Weapon` class, `WEAPON_TYPES`, `PART_TEMPLATES`, `ASSEMBLY_HANDLES`.
- **sculpture.py** — `Sculpture` class, style/material generation.
- **tapestry.py** — `Tapestry` class, pattern/color/weave generation.

### Crafting
- **crafting.py** — All station recipe dicts: `BAKERY_RECIPES` (140+), plus cuisine-specific recipes (Chinese, Italian, Middle Eastern, Spanish). Recipe shape: `{name, ingredients: {item→count}, output_id, output_count}`.
- **herbalism.py** — Herb drying recipes, herbal tea additions.

### City & NPC Systems
- **cities.py** — Quest system. `RARITY_ORDER`, `RARITY_REWARD`, `QUEST_SPECIALS`, `DIFFICULTY_RARITY`, `TRADE_TABLE`.
- **towns.py** — Town generation, biome-to-region-group mapping, NPC pools.
- **outposts.py** — `OUTPOST_TYPES` dict (wine_estate, herb_monastery, tea_house, etc. with eligible biomes, sells/buys/needs). `OUTPOST_SPAWN_CHANCE=0.20`.
- **tea_house.py** — Visitor system. `TEA_ITEM_IDS`, `_ARCHETYPE_PREFS`, `_ARCHETYPE_NAMES`, `_ARCHETYPE_PALETTE`.
- **player_cities.py** — Player-built town system.
- **npc_dynasty.py / npc_identity.py / npc_preferences.py** — NPC generation, lineage, personality.
- **heraldry.py** — Town coat-of-arms generation.

### Animals
- **animals.py** — `CHICKEN_BREED_PROFILES`, `GOAT_BREED_PROFILES`, `HORSE_BREED_PROFILES`, `SHEEP_BREED_PROFILES`. Genetics: coat, plumage, markings, `MUTATION_TYPES`.
- **hunting.py** — Animal slaughter → meat/hide drops.

### World Devices
- **automations.py** — `FarmBot`, `Backhoe` classes. `AUTOMATION_DEFS`, `FARM_BOT_TYPES`.
- **elevators.py** — `ElevatorCar` class.
- **minecarts.py** — `Minecart` class, track following.
- **logic.py** — Wire/gate system.

### Progression
- **research.py** — `ResearchTree` class. Depth gates: `GATE_MID` (~40), `GATE_DEEP` (~100), `GATE_CORE` (~160).
- **achievements.py** — Achievement tracking.

### Persistence
- **save_manager.py** — `SaveManager` class, SQLite. `SAVE_VERSION`. Tables: chunks, player, all collectible types, towns, outposts, farm_bots, backhoes, research, achievements, etc.

### Rendering
- **renderer.py** — Main renderer. Imports block render modules and entity renderers.
- **Render/blockRenderHandler.py** — Block texture cache.
- **Render/blocks_terrain.py / blocks_crafting.py / blocks_structures.py / blocks_wood.py / blocks_decor.py** — Draw functions split by block category.
- **Render/birds.py** — Bird sprites, 30+ species with flight/perch states.
- **Render/insects.py** — Insect wing/body animation.
- **Render/largeAnimal.py / farmanimal.py / forestAnimal.py / wetlandAnimal.py** — Animal rendering with genetics.
- **Render/dogs.py** — Dog breed visualization.
- **Render/Guardsystem.py / Servicenpcs.py / Socialnpcs.py / Workernpcs.py** — NPC rendering by role.
- **Render/hud.py** — Health, hotbar, minimap.
- **Render/lights.py** — Torch/light glow rendering.
- **Render/vehicles.py** — Minecart rendering.
- **Render/logic_blocks.py** — Wire/gate visualization.
- **Render/worldScene/scene.py** — World map scene.

### UI
- **UI/handlers.py** — Input and button routing.
- **UI/panels.py** — Inventory, pause, main menu panels.
- **UI/collections.py** — Collection tabs (rocks, fish, insects, birds, gems, etc.).
- **UI/crafting.py** — Crafting station interfaces.
- **UI/minigames.py** — Mini-games: grape crushing, coffee roasting, tea oxidation, gem cutting.
- **UI/hud.py** — In-game HUD rendering.
- **UI/tea_house.py** — Tea house service UI.
- **UI/reputation_screen.py** — Reputation/standing UI.
- **UI/arena.py / racing.py** — Arena and racing minigame UIs.
- System-specific UIs (one file each): wine, beer, coffee, tea, cheese, textiles, pottery, jewelry, sculpture, tapestry, herbalism, city_block_menu, town_menu, landmark_menu, outpost_menu, hire_panel, job_panel.
- **UI/help.py** — Codex/help system.

### Cross-System
- **crossover.py** — Cross-system interactions: pairing buffs, pollination, aging modifiers.
- **dropped_item.py** — `DroppedItem` entity class.
- **item_icons.py** — Icon asset definitions.
- **landmarks.py / landmark_buildings.py** — Landmark generation.
