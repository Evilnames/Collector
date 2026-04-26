---
name: add-city
description: Step-by-step guide for adding a new city size or layout variant to CollectorBlocks. Covers CITY_CONFIGS entry, building/NPC lists, growth slots, and difficulty mapping.
---

# Add a New City Size or Layout Variant

City layouts are data-driven entries in `CITY_CONFIGS` in [cities.py](../../../cities.py). Each entry defines the physical footprint, building slots, NPC types, ambient population, and growth stages. No new classes are needed for a new layout — only a new config dict and a mapping update.

---

## Step 1 — Add an entry to `CITY_CONFIGS`

Find `CITY_CONFIGS` in [cities.py](../../../cities.py). Add a new key (the size/variant name) with the full config structure. Use `"medium"` as a reference template:

```python
CITY_CONFIGS["grand"] = {
    # Half-width in blocks from the city centre. Total width = half_w * 2.
    "half_w": 56,

    # Each tuple: (x_offset_from_left, width_range, height_range, building_variant_list)
    # x_offset is relative to left edge of city footprint.
    # width_range: (min_w, max_w) in blocks
    # height_range: (min_h, max_h) in blocks
    # building_variant_list: list of style strings (see Building Styles below)
    "buildings": [
        (2,  (5, 7),  (4, 6),  ["house", "two_story"]),
        (10, (6, 8),  (5, 7),  ["smithy"]),
        (18, (7, 9),  (5, 8),  ["inn"]),
        (28, (8, 10), (6, 9),  ["market_stall", "pavilion"]),
        (38, (6, 8),  (5, 7),  ["apothecary"]),
        (46, (5, 7),  (4, 6),  ["library"]),
        (54, (6, 8),  (5, 7),  ["shrine"]),
        (62, (7, 9),  (5, 8),  ["restaurant"]),
        (70, (5, 7),  (4, 6),  ["house", "two_story"]),
        (78, (6, 8),  (5, 7),  ["tower"]),
        (86, (5, 7),  (4, 6),  ["house", "three_story"]),
    ],

    # NPC type string for each building slot — must be same length as "buildings".
    # Valid values: "quest_rock", "merchant", "innkeeper", "blacksmith",
    #               "scholar", "shrine_keeper", "restaurant", "jewelry_merchant",
    #               "trade" — see NPC dispatch in _build_single_city()
    "npc_types": [
        "quest_rock", "blacksmith", "innkeeper", "merchant",
        "apothecary", "scholar", "shrine_keeper", "restaurant",
        "quest_wildflower", "trade", "jewelry_merchant",
    ],

    # Garden plots: list of (x_offset, half_width) pairs
    "gardens": [(22, 3), (50, 3)],

    # Town squares: list of (x_offset, half_width) pairs
    "squares": [(36, 5)],

    # Growth slot lists — buildings that unlock as the town tiers up.
    # Each entry mirrors the format of a "buildings" tuple.
    "growth_slots_tier1": [
        (94, (5, 7), (4, 6), ["house", "two_story"]),
    ],
    "growth_slots_tier2": [
        (102, (6, 8), (5, 7), ["market_stall"]),
    ],
    "growth_slots_tier3": [
        (110, (7, 9), (6, 8), ["three_story", "pavilion"]),
    ],

    # Farm strips: list of (x_offset, half_width) pairs outside the walls
    "farms": [(-12, 4), (108, 4)],

    # Ambient NPCs that roam the streets: list of (x_offset, npc_type_string)
    # Valid types: "villager", "child", "farmer", "guard"
    "ambient_npcs": [
        (15, "villager"), (30, "child"), (45, "guard"),
        (60, "villager"), (75, "farmer"), (90, "guard"),
    ],
}
```

---

## Step 2 — Map the new size to a difficulty

Find `_SIZE_BY_DIFFICULTY` in [cities.py](../../../cities.py) and add the new size at the appropriate difficulty tier. Difficulty is 0–3 (0 = easiest/smallest, 3 = hardest/largest):

```python
_SIZE_BY_DIFFICULTY = {
    0: "small",
    1: "medium",
    2: "large",
    3: "grand",   # ← new
}
```

If you want the new size to appear only for capital cities or special conditions, leave `_SIZE_BY_DIFFICULTY` unchanged and instead pass the size string directly when calling `_build_single_city`.

---

## Reference

### Building styles

| Style | Description |
|-------|-------------|
| `"house"` | Standard 1-storey house |
| `"two_story"` | 2-storey residence |
| `"three_story"` | 3-storey residence |
| `"longhouse"` | Wide single-storey hall |
| `"tower"` | Narrow tall tower |
| `"ruin"` | Collapsed structure (ambient) |
| `"market_stall"` | Open-fronted market booth |
| `"well"` | Decorative well (no NPC) |
| `"inn"` | Inn with sign |
| `"smithy"` | Forge with chimney |
| `"apothecary"` | Herbalist shop |
| `"library"` | Scholar's library |
| `"restaurant"` | Cuisine-specific eatery |
| `"pavilion"` | Open gazebo |
| `"shrine"` | Religious shrine |

Biome-specific variants (`"desert_house"`, `"east_asian_tower"`, etc.) are auto-selected inside `_build_single_city` based on the chunk biome — you do not need to list them explicitly.

### NPC type strings → NPC classes

| String | Class spawned |
|--------|--------------|
| `"quest_rock"` | `RockQuestNPC` |
| `"quest_wildflower"` | `WildflowerQuestNPC` |
| `"quest_gem"` | `GemQuestNPC` |
| `"merchant"` | `MerchantNPC` |
| `"trade"` | `TradeNPC` |
| `"blacksmith"` | `BlacksmithNPC` |
| `"innkeeper"` | `InnkeeperNPC` |
| `"scholar"` | `ScholarNPC` |
| `"shrine_keeper"` | `ShrineKeeperNPC` |
| `"restaurant"` | `RestaurantNPC` |
| `"jewelry_merchant"` | `JewelryMerchantNPC` |

To use a new NPC type, add the string here and add a matching dispatch case in `_build_single_city`.

---

## Verification checklist

- [ ] `len(npc_types) == len(buildings)` for the new config
- [ ] All NPC type strings have a dispatch case in `_build_single_city`
- [ ] `_SIZE_BY_DIFFICULTY` updated if the size should appear in generation
- [ ] Generate a world and find a city of the new size — all buildings and NPCs should spawn without errors
- [ ] Growth buildings unlock correctly as the town tiers up over days
