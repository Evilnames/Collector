import math
import random

from blocks import (STONE, BEDROCK, HOUSE_WALL, HOUSE_ROOF, AIR, LADDER,
                    TILLED_SOIL, WELL_BLOCK,
                    WHEAT_CROP_YOUNG, WHEAT_CROP_MATURE,
                    CARROT_CROP_YOUNG, CARROT_CROP_MATURE,
                    POTATO_CROP_YOUNG, POTATO_CROP_MATURE,
                    CABBAGE_CROP_YOUNG, CABBAGE_CROP_MATURE,
                    LEEK_CROP_YOUNG, LEEK_CROP_MATURE,
                    BEET_CROP_YOUNG, BEET_CROP_MATURE,
                    TURNIP_CROP_YOUNG, TURNIP_CROP_MATURE,
                    ONION_CROP_YOUNG, ONION_CROP_MATURE,
                    GARLIC_CROP_YOUNG, GARLIC_CROP_MATURE,
                    EGGPLANT_CROP_YOUNG, EGGPLANT_CROP_MATURE,
                    CHILI_CROP_YOUNG, CHILI_CROP_MATURE,
                    RICE_CROP_YOUNG, RICE_CROP_MATURE,
                    BOK_CHOY_CROP_YOUNG, BOK_CHOY_CROP_MATURE,
                    SWEET_POTATO_CROP_YOUNG, SWEET_POTATO_CROP_MATURE,
                    CELERY_CROP_YOUNG, CELERY_CROP_MATURE,
                    HOUSE_WALL_STONE, HOUSE_ROOF_STONE,
                    HOUSE_WALL_BRICK, HOUSE_ROOF_BRICK,
                    HOUSE_WALL_DARK,  HOUSE_ROOF_DARK,
                    RESTAURANT_WALL, RESTAURANT_AWNING,
                    SANDSTONE_BLOCK, POLISHED_MARBLE,
                    WHITEWASHED_WALL, MONASTERY_ROOF, MANI_STONE, PRAYER_FLAG_BLOCK,
                    WOOD_DOOR_CLOSED, WOOD_DOOR_OPEN, ALL_LOGS, ALL_LEAVES, BUSH_BLOCKS, SAPLING,
                    PINE_PLANK_WALL, SLATE_SHINGLE,
                    GRANITE_ASHLAR, ROUGH_STONE_WALL, ALPINE_PLASTER,
                    WHITE_PLASTER_WALL, ADOBE_BRICK, SPANISH_ROOF_TILE,
                    AFRICAN_MUD_BRICK, TERRACOTTA_ROOF_TILE,
                    COBBLESTONE, LIMESTONE_BLOCK,
                    FLOWER_BOX, GERANIUM_BOX, CARVED_SHUTTER, HANGING_BASKET,
                    WROUGHT_IRON_GRILLE, HAY_BALE, FIREWOOD_STACK,
                    TEXTILE_RUG_NATURAL, TEXTILE_RUG_GOLDEN, TEXTILE_RUG_CRIMSON,
                    TEXTILE_RUG_ROSE, TEXTILE_RUG_COBALT, TEXTILE_RUG_VIOLET,
                    TEXTILE_RUG_VERDANT, TEXTILE_RUG_AMBER, TEXTILE_RUG_IVORY,
                    TEXTILE_TAPESTRY_NATURAL, TEXTILE_TAPESTRY_GOLDEN,
                    TEXTILE_TAPESTRY_CRIMSON, TEXTILE_TAPESTRY_ROSE,
                    TEXTILE_TAPESTRY_COBALT, TEXTILE_TAPESTRY_VIOLET,
                    TEXTILE_TAPESTRY_VERDANT, TEXTILE_TAPESTRY_AMBER,
                    TEXTILE_TAPESTRY_IVORY,
                    LAVENDER_BED, ROSE_BED, TULIP_BED, COTTAGE_GARDEN_BED,
                    SUNFLOWER_BED, DAHLIA_BED, IRIS_BED, POPPY_BED,
                    MARIGOLD_BED, FOXGLOVE_PATCH, ALLIUM_PATCH, PEONY_BUSH,
                    HYDRANGEA_BUSH, RHODODENDRON_BUSH, FLOWERING_SHRUB,
                    HOLLY_SHRUB, BOXWOOD_BALL, FERN_CLUMP, BAMBOO_CLUMP,
                    TOPIARY_PEACOCK, TOPIARY_BEAR, TOPIARY_RABBIT,
                    TOPIARY_SWAN, TOPIARY_FOX, TOPIARY_HEDGEHOG,
                    TOPIARY_OWL, TOPIARY_SNAIL, TOPIARY_MUSHROOM,
                    TOPIARY_ARCH, ORNAMENTAL_GRASS, CHAMOMILE_LAWN,
                    CLOVER_LAWN, MOSS_PATCH, BARK_MULCH,
                    BIRD_TABLE, GARDEN_GNOME, BEE_SKEP, GARDEN_DOVECOTE,
                    GARDEN_WHEELBARROW, RAIN_BARREL, COMPOST_HEAP,
                    POTTING_TABLE, GARDEN_TOAD_HOUSE, STONE_FROG,
                    STONE_HEDGEHOG, GARDEN_CLOCK, GARDEN_OBELISK_METAL,
                    STONE_TROUGH_PLANTER, COLD_FRAME, TRELLIS_ARCH,
                    GARDEN_SWING, WICKER_FENCE, BUBBLE_FOUNTAIN,
                    SHELL_FOUNTAIN, MILLSTONE_FOUNTAIN, CHERUB_FOUNTAIN,
                    LION_HEAD_FOUNTAIN, MOSAIC_FOUNTAIN, KOI_POOL,
                    LILY_PAD_POND, KNOT_GARDEN, SWEET_PEA_TRELLIS,
                    WISTERIA_PILLAR, STANDARD_ROSE, AGAPANTHUS_PATCH,
                    BLEEDING_HEART_PATCH, ASTILBE_PATCH,
                    MARBLE_STATUE, MARBLE_PLINTH, GARDEN_OBELISK,
                    GARDEN_COLUMN, GARDEN_LANTERN, MARBLE_BIRDBATH,
                    GARDEN_TABLE, GARDEN_ROCK, HERRINGBONE_GARDEN,
                    INLAID_MARBLE, MARBLE_MEDALLION_REN, GARDEN_STAR_TILE,
                    HERMES_STELE, VICTORY_STELE, GREEK_STONE_BENCH,
                    DORIC_CAPITAL, TRIPOD_BRAZIER, VOTIVE_TABLET,
                    SYMPOSIUM_TABLE, LAUREL_WREATH_MOUNT, BRAZIER,
                    CARVED_BENCH, STONE_BASIN, WALL_SCONCE, STAR_LAMP,
                    TORCH, ARCH_STONE, GARDEN_GATE, LOW_GARDEN_WALL,
                    LANTERN_ORB, CHANDELIER, CANDELABRA, OLIVE_BRANCH,
                    PHILOSOPHERS_SCROLL, GREEK_THEATRE_MASK,
                    ROUND_TOWER_WALL, CURTAIN_WALL, GREAT_HALL_FLOOR,
                    CRENELLATION, HERALDIC_PANEL, CASTLE_FIREPLACE,
                    MACHICOLATION, PORTCULLIS_BLOCK, DRAWBRIDGE_CHAIN,
                    DRAWBRIDGE_PLANK, CASTLE_GATE_ARCH, WALL_WALK_FLOOR,
                    DUNGEON_WALL, DUNGEON_GRATE, MOAT_STONE,
                    MURDER_HOLE, CORBEL_COURSE, TOWER_CAP,
                    GARDEROBE_CHUTE, CHAPEL_STONE, GOTHIC_TRACERY,
                    ROSE_WINDOW, LANCET_WINDOW, GARGOYLE_BLOCK,
                    PALACE_FLOOR_TILE, PALACE_PORTAL, PALAZZO_BALCONY,
                    IRON_DOOR_CLOSED, BRONZE_SHIELD_MOUNT,
                    TOWN_FLAG_BLOCK, STAIRS_RIGHT, STAIRS_LEFT,
                    PAGODA_EAVE, TORII_PANEL, TATAMI_PAVING, JAPANESE_SHOJI,
                    PINE_TOPIARY_JP, JAPANESE_MAPLE, SHISHI_ODOSHI, RED_ARCH_BRIDGE,
                    TORO_LANTERN, YUKIMI_LANTERN, BAMBOO_FENCE_JP, STONE_LANTERN,
                    WAVE_CERAMIC, GLAZED_ROOF_TILE, MOON_GATE, CERAMIC_PLANTER,
                    LACQUER_PANEL, PAPER_LANTERN, DRAGON_TILE, BAMBOO_SCREEN,
                    CRIMSON_BRICK, JADE_PANEL, GOLDEN_CEILING, CERAMIC_SEAT,
                    IMPERIAL_PAVING, TOPIARY_DRAGON,
                    ROMAN_MOSAIC, ROMAN_ARCH_REN,
                    GREEK_KEY, GREEK_AMPHORA,
                    MUGHAL_ARCH, MUGHAL_JALI,
                    ANDALUSIAN_FOUNTAIN, PORTUGUESE_BENCH,
                    SPANISH_PATIO_FLOOR, MUDEJAR_STAR_TILE, MUDEJAR_BRICK,
                    COBALT_DOOR_CLOSED, CRIMSON_CEDAR_DOOR_CLOSED, SAFFRON_DOOR_CLOSED,
                    STUDDED_OAK_DOOR_CLOSED, VERMILION_DOOR_CLOSED, SHOJI_DOOR_CLOSED,
                    GILDED_DOOR_CLOSED, BRONZE_DOOR_CLOSED, SWAHILI_DOOR_CLOSED,
                    SANDALWOOD_DOOR_CLOSED, STONE_SLAB_DOOR_CLOSED,
                    BED, CHEST_BLOCK, BAKERY_BLOCK, STABLE_BLOCK, STORAGE_PITHOS,
                    TAPESTRY_BLOCK, WOVEN_TEXTILE, OAK_PANEL)
from constants import (BLOCK_SIZE, PLAYER_W, PLAYER_H, CITY_SPACING, CITY_COUNT,
                       NPC_INTERACT_RANGE, CHUNK_W, GRAVITY, MAX_FALL, SURFACE_Y)
from rocks import ROCK_TYPES


RARITY_ORDER  = ["common", "uncommon", "rare", "epic", "legendary"]
RARITY_REWARD = {
    "common":    5,
    "uncommon":  12,
    "rare":      25,
    "epic":      60,
    "legendary": 150,
}

QUEST_SPECIALS = ["luminous", "magnetic", "crystalline", "resonant", "voidtouched"]
SPECIAL_REWARD = {
    "luminous":    20,
    "magnetic":    18,
    "crystalline": 25,
    "resonant":    32,
    "voidtouched": 50,
}

DIFFICULTY_RARITY = {
    0: ["common", "uncommon"],
    1: ["common", "uncommon", "rare"],
    2: ["uncommon", "rare", "epic", "legendary"],
}

DIFFICULTY_KINDS = {
    0: ["single", "single", "single", "quantity"],
    1: ["single", "single", "any_rarity", "quantity"],
    2: ["single", "any_rarity", "quantity", "special"],
}

TRADE_TABLE = [
    ("lumber",        5,  3),
    ("iron_chunk",    3,  4),
    ("coal",          8,  3),
    ("gold_nugget",   1,  8),
    ("wool",          3,  5),
    ("crystal_shard", 1, 15),
    ("ruby",          1, 25),
    ("stone_chip",   10,  2),
    ("obsidian_slab", 1, 20),
    ("dirt_clump",   15,  1),
    ("milk",          2,  4),
]

# ---------------------------------------------------------------------------
# Wildflower quest data
# ---------------------------------------------------------------------------

_WF_RARITY_REWARD = {
    "common":    6,
    "uncommon":  15,
    "rare":      35,
    "epic":      80,
    "legendary": 200,
}

_WF_QUEST_POOL = {
    0: ["daisy", "buttercup", "clover", "poppy", "lavender", "chamomile", "forget_me_not"],
    1: ["lupine", "foxglove", "iris", "orchid", "sunflower", "bleeding_heart", "sweet_pea", "snapdragon"],
    2: ["edelweiss", "ghost_orchid", "crystal_bloom", "void_petal", "phantom_bloom", "biolume_bell"],
}

_WF_KINDS_BY_DIFF = {
    0: ["wf_single", "wf_single", "wf_quantity"],
    1: ["wf_single", "wf_rarity", "wf_quantity"],
    2: ["wf_rarity", "wf_rarity", "wf_quantity"],
}


def _build_wf_quest(rng, difficulty):
    kind = rng.choice(_WF_KINDS_BY_DIFF[difficulty])
    allowed = DIFFICULTY_RARITY[difficulty]

    if kind == "wf_single":
        flower_type = rng.choice(_WF_QUEST_POOL[difficulty])
        reward = int(_WF_RARITY_REWARD["common"] * (1 + difficulty))
        return {"kind": "wf_single", "flower_type": flower_type, "reward": reward}

    elif kind == "wf_quantity":
        pool = _WF_QUEST_POOL[min(difficulty, 1)]
        flower_type = rng.choice(pool)
        count = rng.randint(2, 3)
        reward = int(_WF_RARITY_REWARD["common"] * count * (1 + difficulty * 0.5))
        return {"kind": "wf_quantity", "flower_type": flower_type, "count": count, "reward": reward}

    else:  # wf_rarity
        upper = allowed[max(0, len(allowed) // 2):]
        min_rarity = rng.choice(upper)
        reward = int(_WF_RARITY_REWARD[min_rarity] * 1.4)
        return {"kind": "wf_rarity", "min_rarity": min_rarity, "reward": reward}


def wf_quest_display(quest):
    if quest["kind"] == "wf_single":
        return quest["flower_type"].replace("_", " ").title()
    elif quest["kind"] == "wf_quantity":
        return f"{quest['count']}x {quest['flower_type'].replace('_', ' ').title()}"
    elif quest["kind"] == "wf_rarity":
        from UI import RARITY_LABEL
        label = RARITY_LABEL.get(quest["min_rarity"], quest["min_rarity"])
        return f"Any {label}+ wildflower"
    return "Unknown quest"


def wf_quest_hint(quest):
    if quest["kind"] == "wf_single":
        return "Found at the surface in various biomes"
    elif quest["kind"] == "wf_quantity":
        return "Any rarity accepted"
    elif quest["kind"] == "wf_rarity":
        idx = RARITY_ORDER.index(quest["min_rarity"])
        above = " / ".join(r.title() for r in RARITY_ORDER[idx:])
        return f"Accepted: {above}"
    return ""


# ---------------------------------------------------------------------------
# Gem quest data
# ---------------------------------------------------------------------------

_GEM_RARITY_REWARD = {
    "common":    10,
    "uncommon":  25,
    "rare":      60,
    "epic":      140,
    "legendary": 350,
}

_GEM_QUEST_POOL = {
    0: ["amber", "garnet", "rose_quartz", "jet"],
    1: ["spinel", "peridot", "tourmaline", "obsidian"],
    2: ["alexandrite", "emerald", "ruby", "sapphire", "diamond"],
}

_GEM_KINDS_BY_DIFF = {
    0: ["gem_type", "gem_type", "gem_rarity"],
    1: ["gem_type", "gem_rarity", "gem_cut"],
    2: ["gem_rarity", "gem_cut", "gem_cut"],
}


def _build_gem_quest(rng, difficulty):
    kind = rng.choice(_GEM_KINDS_BY_DIFF[difficulty])
    allowed = DIFFICULTY_RARITY[difficulty]

    if kind == "gem_type":
        gem_type = rng.choice(_GEM_QUEST_POOL[difficulty])
        reward = int(_GEM_RARITY_REWARD["common"] * (1 + difficulty * 0.8))
        return {"kind": "gem_type", "gem_type": gem_type, "reward": reward}

    elif kind == "gem_cut":
        gem_type = rng.choice(_GEM_QUEST_POOL[min(difficulty, 1)])
        reward = int(_GEM_RARITY_REWARD["uncommon"] * (1 + difficulty * 0.6))
        return {"kind": "gem_cut", "gem_type": gem_type, "reward": reward}

    else:  # gem_rarity
        upper = allowed[max(0, len(allowed) // 2):]
        min_rarity = rng.choice(upper)
        reward = int(_GEM_RARITY_REWARD[min_rarity] * 1.3)
        return {"kind": "gem_rarity", "min_rarity": min_rarity, "reward": reward}


def gem_quest_display(quest):
    if quest["kind"] == "gem_type":
        return f"Any {quest['gem_type'].replace('_', ' ').title()}"
    elif quest["kind"] == "gem_cut":
        return f"Cut {quest['gem_type'].replace('_', ' ').title()}"
    elif quest["kind"] == "gem_rarity":
        from UI import RARITY_LABEL
        label = RARITY_LABEL.get(quest["min_rarity"], quest["min_rarity"])
        return f"Any {label}+ gemstone"
    elif quest["kind"] == "gem_royal":
        return f"Legendary Cut {quest['gem_type'].replace('_', ' ').title()}"
    return "Unknown quest"


def gem_quest_hint(quest):
    if quest["kind"] == "gem_type":
        return "Any rarity, rough or cut accepted"
    elif quest["kind"] == "gem_cut":
        return "Must be cut (use the Gem Cutter)"
    elif quest["kind"] == "gem_rarity":
        idx = RARITY_ORDER.index(quest["min_rarity"])
        above = " / ".join(r.title() for r in RARITY_ORDER[idx:])
        return f"Accepted: {above}"
    elif quest["kind"] == "gem_royal":
        return "Must be legendary quality and cut (use the Gem Cutter)"
    return ""


# ---------------------------------------------------------------------------
# Rock quest helpers (unchanged)
# ---------------------------------------------------------------------------

def _quest_candidates(rng, difficulty):
    allowed = set(DIFFICULTY_RARITY[difficulty])
    max_depth = 40 + difficulty * 50
    candidates = [
        k for k, v in ROCK_TYPES.items()
        if v["min_depth"] <= max_depth and any(r in allowed for r in v["rarity_pool"])
    ]
    return candidates if candidates else list(ROCK_TYPES.keys())


def _build_quest(rng, difficulty):
    kind = rng.choice(DIFFICULTY_KINDS[difficulty])
    allowed = DIFFICULTY_RARITY[difficulty]

    if kind == "single":
        candidates = _quest_candidates(rng, difficulty)
        rock_type = rng.choice(candidates)
        pool = [r for r in ROCK_TYPES[rock_type]["rarity_pool"] if r in allowed]
        rarity = rng.choice(pool) if pool else rng.choice(allowed)
        base_reward = RARITY_REWARD[rarity]
        reward = int(base_reward * (1 + difficulty * 0.3))
        return {"kind": "single", "rock_type": rock_type, "rarity": rarity, "reward": reward}

    elif kind == "any_rarity":
        upper = allowed[max(0, len(allowed) // 2):]
        min_rarity = rng.choice(upper)
        reward = int(RARITY_REWARD[min_rarity] * 1.5)
        return {"kind": "any_rarity", "min_rarity": min_rarity, "reward": reward}

    elif kind == "quantity":
        count = 2 if difficulty == 0 else rng.randint(2, 3)
        candidates = _quest_candidates(rng, difficulty)
        rock_type = rng.choice(candidates)
        reward = int(RARITY_REWARD["common"] * count * (1 + difficulty * 0.5))
        return {"kind": "quantity", "rock_type": rock_type, "count": count, "reward": reward}

    else:  # special
        special = rng.choice(QUEST_SPECIALS)
        reward = int(SPECIAL_REWARD[special] * (1 + difficulty * 0.4))
        return {"kind": "special", "special": special, "reward": reward}


_PRESTIGE_SPECIALS = ["resonant", "voidtouched"]

ROYAL_QUEST_REP    = 500
_ROYAL_SPECIALS    = ["voidtouched", "crystalline", "resonant"]
_ROYAL_FLOWER_POOL = ["ghost_orchid", "void_petal", "phantom_bloom", "crystal_bloom", "biolume_bell"]
_ROYAL_GEM_POOL    = ["diamond", "alexandrite", "emerald", "ruby", "sapphire"]
_ROYAL_FOSSIL_SPECIALS = ["opalized", "complete"]
_FOSSIL_SPECIAL_REWARD = {"opalized": 80, "complete": 60, "carbonized": 40, "mineralized": 30}
_FOSSIL_RARITY_REWARD  = {
    "common": 8, "uncommon": 20, "rare": 48, "epic": 115, "legendary": 280,
}
_FISH_RARITY_REWARD = {
    "common": 6, "uncommon": 15, "rare": 35, "epic": 80, "legendary": 200,
}


def _build_prestige_rock_quest(rng, difficulty):
    if difficulty == 0:
        upper = ["rare", "epic"]
        min_rarity = rng.choice(upper)
        reward = int(RARITY_REWARD[min_rarity] * 2.5)
        return {"kind": "any_rarity", "min_rarity": min_rarity, "reward": reward, "min_rep": 150}
    elif difficulty == 1:
        special = rng.choice(_PRESTIGE_SPECIALS)
        reward = int(SPECIAL_REWARD[special] * 3.5)
        return {"kind": "special", "special": special, "reward": reward, "min_rep": 250}
    else:
        candidates = [k for k, v in ROCK_TYPES.items() if "legendary" in v.get("rarity_pool", [])]
        rock_type = rng.choice(candidates) if candidates else rng.choice(list(ROCK_TYPES.keys()))
        reward = int(RARITY_REWARD["legendary"] * 4.0)
        return {"kind": "single", "rock_type": rock_type, "rarity": "legendary", "reward": reward, "min_rep": 400}


def _build_prestige_wf_quest(rng, difficulty):
    if difficulty == 0:
        min_rarity = "rare"
        reward = int(_WF_RARITY_REWARD[min_rarity] * 2.5)
        return {"kind": "wf_rarity", "min_rarity": min_rarity, "reward": reward, "min_rep": 150}
    elif difficulty == 1:
        min_rarity = "epic"
        reward = int(_WF_RARITY_REWARD[min_rarity] * 3.0)
        return {"kind": "wf_rarity", "min_rarity": min_rarity, "reward": reward, "min_rep": 250}
    else:
        flower_type = rng.choice(_WF_QUEST_POOL[2])
        reward = int(_WF_RARITY_REWARD["legendary"] * 4.0)
        return {"kind": "wf_single", "flower_type": flower_type, "reward": reward, "min_rep": 400}


def _build_prestige_gem_quest(rng, difficulty):
    if difficulty == 0:
        gem_type = rng.choice(_GEM_QUEST_POOL[0])
        reward = int(_GEM_RARITY_REWARD["uncommon"] * 2.5)
        return {"kind": "gem_cut", "gem_type": gem_type, "reward": reward, "min_rep": 150}
    elif difficulty == 1:
        upper = ["rare", "epic"]
        min_rarity = rng.choice(upper)
        reward = int(_GEM_RARITY_REWARD[min_rarity] * 3.0)
        return {"kind": "gem_rarity", "min_rarity": min_rarity, "reward": reward, "min_rep": 250}
    else:
        reward = int(_GEM_RARITY_REWARD["legendary"] * 3.5)
        return {"kind": "gem_rarity", "min_rarity": "legendary", "reward": reward, "min_rep": 400}


def _build_royal_rock_quest(rng):
    if rng.random() < 0.4:
        special = rng.choice(_ROYAL_SPECIALS)
        reward = int(SPECIAL_REWARD[special] * 10)
        return {"kind": "special", "special": special, "reward": reward, "min_rep": ROYAL_QUEST_REP}
    candidates = [k for k, v in ROCK_TYPES.items() if "legendary" in v.get("rarity_pool", [])]
    rock_type = rng.choice(candidates) if candidates else rng.choice(list(ROCK_TYPES.keys()))
    reward = int(RARITY_REWARD["legendary"] * 5)
    return {"kind": "single", "rock_type": rock_type, "rarity": "legendary", "reward": reward,
            "min_rep": ROYAL_QUEST_REP}


def _build_royal_wf_quest(rng):
    if rng.random() < 0.6:
        flower_type = rng.choice(_ROYAL_FLOWER_POOL)
        reward = int(_WF_RARITY_REWARD["legendary"] * 5)
        return {"kind": "wf_single", "flower_type": flower_type, "reward": reward, "min_rep": ROYAL_QUEST_REP}
    reward = int(_WF_RARITY_REWARD["legendary"] * 4)
    return {"kind": "wf_rarity", "min_rarity": "legendary", "reward": reward, "min_rep": ROYAL_QUEST_REP}


def _build_royal_gem_quest(rng):
    gem_type = rng.choice(_ROYAL_GEM_POOL)
    reward = int(_GEM_RARITY_REWARD["legendary"] * 5)
    return {"kind": "gem_royal", "gem_type": gem_type, "reward": reward, "min_rep": ROYAL_QUEST_REP}


def _build_royal_fossil_quest(rng):
    if rng.random() < 0.35:
        special = rng.choice(_ROYAL_FOSSIL_SPECIALS)
        reward = int(_FOSSIL_SPECIAL_REWARD[special] * 10)
        return {"kind": "fossil_special", "special": special, "reward": reward, "min_rep": ROYAL_QUEST_REP}
    from fossils import FOSSIL_TYPES
    candidates = [k for k, v in FOSSIL_TYPES.items() if "legendary" in v.get("rarity_pool", [])]
    fossil_type = rng.choice(candidates) if candidates else rng.choice(list(FOSSIL_TYPES.keys()))
    reward = int(_FOSSIL_RARITY_REWARD["legendary"] * 5)
    return {"kind": "fossil_single", "fossil_type": fossil_type, "rarity": "legendary",
            "reward": reward, "min_rep": ROYAL_QUEST_REP}


def _build_royal_fish_quest(rng):
    from fish import FISH_TYPES
    candidates = [k for k, v in FISH_TYPES.items() if "legendary" in v.get("rarity_pool", [])]
    species = rng.choice(candidates) if candidates else rng.choice(list(FISH_TYPES.keys()))
    reward = int(_FISH_RARITY_REWARD["legendary"] * 5)
    return {"kind": "fish_single", "species": species, "rarity": "legendary",
            "reward": reward, "min_rep": ROYAL_QUEST_REP}


def fossil_quest_display(quest):
    if quest["kind"] == "fossil_single":
        from UI import RARITY_LABEL
        label = RARITY_LABEL.get(quest["rarity"], quest["rarity"])
        return f"{label} {quest['fossil_type'].replace('_', ' ').title()}"
    elif quest["kind"] == "fossil_special":
        return f"Any {quest['special'].title()} Fossil"
    return "Unknown quest"


def fossil_quest_hint(quest):
    if quest["kind"] == "fossil_single":
        from fossils import FOSSIL_TYPES
        depth = FOSSIL_TYPES.get(quest["fossil_type"], {}).get("min_depth", "?")
        age   = FOSSIL_TYPES.get(quest["fossil_type"], {}).get("age", "")
        return f"Found from depth {depth} m  ({age.title()} era)"
    elif quest["kind"] == "fossil_special":
        return "Special properties occur rarely on any fossil"
    return ""


def fish_quest_display(quest):
    if quest["kind"] == "fish_single":
        return f"Legendary {quest['species'].replace('_', ' ').title()}"
    return "Unknown quest"


def fish_quest_hint(quest):
    if quest["kind"] == "fish_single":
        from fish import FISH_TYPES
        info    = FISH_TYPES.get(quest["species"], {})
        habitat = info.get("habitat", "river")
        biomes  = info.get("biome_affinity", [])
        if biomes:
            bio_str = ", ".join(b.replace("_", " ") for b in biomes[:3])
            return f"Found in {habitat}s — {bio_str}"
        return f"Found in {habitat}s worldwide"
    return ""


def quest_display(quest):
    if quest["kind"] == "single":
        from UI import RARITY_LABEL
        label = RARITY_LABEL.get(quest["rarity"], quest["rarity"])
        return f"{label} {quest['rock_type'].replace('_', ' ').title()}"
    elif quest["kind"] == "any_rarity":
        from UI import RARITY_LABEL
        label = RARITY_LABEL.get(quest["min_rarity"], quest["min_rarity"])
        return f"Any {label}+ rock"
    elif quest["kind"] == "quantity":
        return f"{quest['count']}x {quest['rock_type'].replace('_', ' ').title()} (any rarity)"
    elif quest["kind"] == "special":
        return f"Any {quest['special'].title()} rock"
    return "Unknown quest"


def quest_hint(quest):
    if quest["kind"] == "single":
        depth = ROCK_TYPES[quest["rock_type"]]["min_depth"]
        return f"Found from depth {depth} m"
    elif quest["kind"] == "any_rarity":
        idx = RARITY_ORDER.index(quest["min_rarity"])
        above = " / ".join(r.title() for r in RARITY_ORDER[idx:])
        return f"Accepted: {above}"
    elif quest["kind"] == "quantity":
        depth = ROCK_TYPES[quest["rock_type"]]["min_depth"]
        return f"Found from depth {depth} m"
    elif quest["kind"] == "special":
        return "Special properties appear randomly on any rock"
    return ""


# ---------------------------------------------------------------------------
# NPC base class
# ---------------------------------------------------------------------------

class NPC:
    NPC_W = 20
    NPC_H = 28

    def __init__(self, x, y, world, npc_id):
        self.x = float(x)
        self.y = float(y)
        self.vy = 0.0
        self.on_ground = False
        self.world = world
        self.animal_id = npc_id
        self._bob_timer = 0.0
        self._bob_offset = 0.0
        # Identity / relationship fields — populated by _setup_identity() after spawn
        self.npc_uid     = None
        self.town_id     = None
        self.identity    = None   # dict: first_name, family_name, gender, display_name, blurb
        self.preferences = None   # dict from npc_preferences.derive_preferences
        self.family_id    = None
        self.family_role  = "singleton"
        self.spouse_uid   = None
        self.parent_uids  = []
        self.sibling_uids = []

    def _setup_identity(self, town_id: int, npc_index: int, world_seed: int):
        """Called once after spawn to assign stable name, lineage, and preferences."""
        import npc_identity
        import npc_preferences
        self.town_id  = town_id
        self.npc_uid  = f"{town_id}_{npc_index}"
        self.identity = npc_identity.generate_identity(
            self.npc_uid, town_id,
            getattr(self, "display_name", self.animal_id),
            world_seed,
        )
        self.preferences = npc_preferences.derive_preferences(self.npc_uid, world_seed)

    def _beloved_price_mult(self, player) -> float:
        """Return 0.90 if player has a beloved discount in this NPC's town, else 1.0."""
        if player is None:
            return 1.0
        tid = getattr(self, "town_id", None) or self._nearest_town_id()
        if tid in getattr(player, "merchant_beloved_towns", set()):
            return 0.90
        return 1.0

    def _dynasty_price_mult(self, player) -> float:
        """Return discount multiplier from dynasty favor (5% at Favored, 10% at Champion)."""
        if player is None:
            return 1.0
        from towns import TOWNS
        tid   = getattr(self, "town_id", None) or self._nearest_town_id()
        town  = TOWNS.get(tid)
        if town is None:
            return 1.0
        rid  = getattr(town, "region_id", None)
        mult = 1.0
        if rid in getattr(player, "favored_dynasty_regions",  set()):
            mult *= 0.95
        if rid in getattr(player, "champion_dynasty_regions", set()):
            mult *= 0.95
        return mult

    @property
    def rect(self):
        import pygame
        return pygame.Rect(int(self.x), int(self.y), self.NPC_W, self.NPC_H)

    def _collides(self):
        left  = int(self.x // BLOCK_SIZE)
        right = int((self.x + self.NPC_W - 1) // BLOCK_SIZE)
        top   = int(self.y // BLOCK_SIZE)
        bot   = int((self.y + self.NPC_H - 1) // BLOCK_SIZE)
        for bx in range(left, right + 1):
            for by in range(top, bot + 1):
                if self.world.is_solid(bx, by):
                    return True
        return False

    def update(self, dt):
        # Stationary NPCs respect gravity — they fall until they hit the ground
        # so they never end up floating after the building under them is removed.
        self.vy = min(self.vy + GRAVITY, MAX_FALL)
        self.y += self.vy
        if self._collides():
            self.y -= self.vy
            self.vy = 0.0
            self.on_ground = True
        else:
            self.on_ground = False

    def reset_harvest(self):
        pass

    def try_harvest(self, player, dt):
        return None

    def in_range(self, player):
        px = (player.x + PLAYER_W / 2) / BLOCK_SIZE
        py = (player.y + PLAYER_H / 2) / BLOCK_SIZE
        ex = (self.x + self.NPC_W / 2) / BLOCK_SIZE
        ey = (self.y + self.NPC_H / 2) / BLOCK_SIZE
        return ((px - ex) ** 2 + (py - ey) ** 2) ** 0.5 <= NPC_INTERACT_RANGE

    def _nearest_town_id(self):
        centers = getattr(self.world, "town_centers", [])
        if not centers:
            return None
        return min(range(len(centers)), key=lambda i: abs(centers[i] - round(self.x / BLOCK_SIZE)))

    def _town_rep(self):
        from towns import TOWNS
        tid = self._nearest_town_id()
        return TOWNS[tid].reputation if tid is not None and tid in TOWNS else 0

    def _town_tier(self):
        from towns import TOWNS
        tid = self._nearest_town_id()
        return TOWNS[tid].tier if tid is not None and tid in TOWNS else 0


# ---------------------------------------------------------------------------
# Ambient NPCs — non-interactive residents that walk and go home at night
# ---------------------------------------------------------------------------

class AmbientNPC(NPC):
    """Base class for city residents: farmers, villagers, children, guards.

    Walks a patrol range around patrol_cx, pauses occasionally, reverses at
    the edges.  is_ambient=True tells main.py to skip the E-key panel.
    """
    is_ambient = True

    def __init__(self, x, y, world, npc_id, patrol_half=48, biodome="temperate"):
        super().__init__(x, y, world, npc_id)
        self.patrol_cx   = float(x)
        self.patrol_half = float(patrol_half)
        self.facing      = 1       # 1 = right, -1 = left
        self._walk_speed = 28.0    # px/sec
        self._pause_max  = 3.5     # max idle seconds
        self._state      = "walk"
        self._state_timer = random.uniform(1.0, 4.0)
        style = _CLOTHING_STYLE_BY_BIODOME.get(biodome, "temperate")
        self.clothing = _CLOTHING_PALETTES.get(style, _CLOTHING_DEFAULT)
        # Ensure spawn is not inside solid terrain
        self._snap_to_surface()

    def _snap_to_surface(self):
        """Eject upward block-by-block until the NPC is no longer inside terrain."""
        for _ in range(60):
            if not self._collides():
                break
            self.y -= BLOCK_SIZE

    def update(self, dt):
        # Gravity
        self.vy = min(self.vy + GRAVITY, MAX_FALL)
        self.y += self.vy
        if self._collides():
            self.y -= self.vy
            self.vy = 0.0
            self.on_ground = True
        else:
            self.on_ground = False

        # Bob animation
        self._bob_timer += dt
        self._bob_offset = math.sin(self._bob_timer * 2.2) * 1.5

        # Walk / pause state machine
        self._state_timer -= dt
        if self._state == "pause":
            if self._state_timer <= 0:
                self._state = "walk"
                self._state_timer = random.uniform(2.0, 6.0)
        else:
            if self._walk_speed > 0:
                old_x = self.x
                self.x += self._walk_speed * dt * self.facing
                lo = self.patrol_cx - self.patrol_half
                hi = self.patrol_cx + self.patrol_half - self.NPC_W
                if self.x <= lo or self.x >= hi:
                    # Hit patrol boundary — clamp and turn around
                    self.x = max(lo, min(hi, self.x))
                    self.facing *= -1
                elif self._collides():
                    # Hit a wall — revert and turn around
                    self.x = old_x
                    self.facing *= -1
            if self._state_timer <= 0:
                self._state = "pause"
                self._state_timer = random.uniform(1.0, self._pause_max)


class FarmerNPC(AmbientNPC):
    def __init__(self, x, y, world, patrol_half=56, biodome="temperate"):
        super().__init__(x, y, world, "npc_farmer", patrol_half, biodome)
        self._walk_speed = 22.0
        self._pause_max  = 5.0   # lingers near crops

    def update(self, dt):
        from world import DAY_DURATION
        tod = getattr(self.world, 'time_of_day', 0.0)
        if tod >= DAY_DURATION:
            self._walk_speed = 0.0
            dx = self.patrol_cx - self.x
            if abs(dx) > 4:
                self.x += dx * min(1.0, dt * 2.0)
        else:
            self._walk_speed = 22.0
        super().update(dt)


class VillagerNPC(AmbientNPC):
    def __init__(self, x, y, world, patrol_half=60, biodome="temperate"):
        super().__init__(x, y, world, "npc_villager", patrol_half, biodome)

    def update(self, dt):
        from world import DAY_DURATION
        tod = getattr(self.world, 'time_of_day', 0.0)
        if tod >= DAY_DURATION:
            self._walk_speed = 0.0
            dx = self.patrol_cx - self.x
            if abs(dx) > 4:
                self.x += dx * min(1.0, dt * 2.0)
        else:
            self._walk_speed = 28.0
        super().update(dt)


class ChildNPC(AmbientNPC):
    NPC_W = 14
    NPC_H = 20

    def __init__(self, x, y, world, patrol_half=80, biodome="temperate"):
        super().__init__(x, y, world, "npc_child", patrol_half, biodome)
        self._walk_speed = 48.0
        self._pause_max  = 1.5


_GUARD_KIT_POOL = (["spearman"] * 5 + ["swordsman"] * 5
                   + ["halberdier"] * 3 + ["crossbowman"] * 3
                   + ["axeman"] * 3 + ["macer"] * 3
                   + ["archer"] * 3 + ["pikeman"] * 2
                   + ["lancer"] * 2 + ["watchman"] * 3
                   + ["captain"] * 1)
_GUARD_HELMETS  = ["pot", "pot", "kettle", "sallet", "plumed", "coif", "horned"]
_GUARD_EMBLEMS  = ["none", "none", "none", "cross", "star", "circle", "chevron"]
_GUARD_BEARDS   = ["none", "none", "short", "full", "mustache"]
_GUARD_CAPES    = ["none", "none", "none", "none", "trim", "dark", "trim"]
_GUARD_FINISHES = ["steel", "steel", "bronze", "blackened", "burnished"]
_GUARD_TABARDS  = ["solid", "solid", "vertical_split", "quartered", "horizontal_band"]
_GUARD_SKINS    = [(245, 215, 175), (230, 195, 155), (200, 160, 120),
                   (160, 120,  85), (115,  80,  55)]
_GUARD_SHIELD_COLORS = [(140,  35,  35), (40,  60, 130), (35, 110,  60),
                       (180, 145,  35), (45,  45,  55), (140, 100,  35)]
_GUARD_BOOTS    = [(60, 45, 30), (80, 55, 30), (40, 35, 30), (95, 75, 50)]


class GuardNPC(AmbientNPC):
    def __init__(self, x, y, world, patrol_half=40, biodome="temperate", kit=None):
        super().__init__(x, y, world, "npc_guard", patrol_half, biodome)
        self._walk_speed = 20.0
        self._pause_max  = 2.0
        self.kit = kit or random.choice(_GUARD_KIT_POOL)
        if self.kit == "captain":
            self.helmet, self.cape = "plumed", "trim"
        elif self.kit in ("crossbowman", "archer", "watchman"):
            self.helmet = random.choice(["kettle", "coif", "pot"])
            self.cape   = "none"
        else:
            self.helmet = random.choice(_GUARD_HELMETS)
            self.cape   = random.choice(_GUARD_CAPES)
        self.beard          = random.choice(_GUARD_BEARDS)
        self.emblem         = random.choice(_GUARD_EMBLEMS)
        self.tint           = random.randint(-18, 22)
        self.weapon_variant = random.randint(0, 2)
        self.helmet_finish  = random.choice(_GUARD_FINISHES)
        self.tabard         = random.choice(_GUARD_TABARDS)
        self.skin_tone      = random.choice(_GUARD_SKINS)
        self.shield_color   = random.choice(_GUARD_SHIELD_COLORS)
        self.boots          = random.choice(_GUARD_BOOTS)
        self.sash           = random.random() < 0.15


class ElderNPC(AmbientNPC):
    def __init__(self, x, y, world, patrol_half=32, biodome="temperate"):
        super().__init__(x, y, world, "npc_elder", patrol_half, biodome)
        self._walk_speed = 14.0
        self._pause_max  = 5.0


class BeggarNPC(AmbientNPC):
    def __init__(self, x, y, world, patrol_half=20, biodome="temperate"):
        super().__init__(x, y, world, "npc_beggar", patrol_half, biodome)
        self._walk_speed = 10.0
        self._pause_max  = 7.0


class NobleNPC(AmbientNPC):
    def __init__(self, x, y, world, patrol_half=44, biodome="temperate"):
        super().__init__(x, y, world, "npc_noble", patrol_half, biodome)
        self._walk_speed = 22.0
        self._pause_max  = 2.5


class RoyalSpouseNPC(AmbientNPC):
    def __init__(self, x, y, world, patrol_half=24, biodome="temperate",
                 leader_color=(160, 40, 80), palace_type="castle"):
        super().__init__(x, y, world, "npc_royal_spouse", patrol_half, biodome)
        self._walk_speed  = 16.0
        self._pause_max   = 4.0
        self.leader_color = leader_color
        self.palace_type  = palace_type


class RoyalChildNPC(AmbientNPC):
    def __init__(self, x, y, world, patrol_half=18, biodome="temperate",
                 leader_color=(160, 40, 80), palace_type="castle"):
        super().__init__(x, y, world, "npc_royal_child", patrol_half, biodome)
        self._walk_speed  = 26.0
        self._pause_max   = 1.5
        self.leader_color = leader_color
        self.palace_type  = palace_type


class PilgrimNPC(AmbientNPC):
    def __init__(self, x, y, world, patrol_half=64, biodome="temperate"):
        super().__init__(x, y, world, "npc_pilgrim", patrol_half, biodome)
        self._walk_speed = 24.0
        self._pause_max  = 3.0


class DrunkardNPC(AmbientNPC):
    def __init__(self, x, y, world, patrol_half=24, biodome="temperate"):
        super().__init__(x, y, world, "npc_drunkard", patrol_half, biodome)
        self._walk_speed = 16.0
        self._pause_max  = 4.5


# ---------------------------------------------------------------------------
# NPC types
# ---------------------------------------------------------------------------

class RockQuestNPC(NPC):
    def __init__(self, x, y, world, rng, difficulty=0, biodome="temperate"):
        super().__init__(x, y, world, "npc_quest")
        self.clothing = _npc_clothing(biodome)
        self._rng = rng
        self.difficulty = difficulty
        self._streak = 0
        self.quests = [_build_quest(rng, difficulty), _build_prestige_rock_quest(rng, difficulty)]

    def find_matching_rocks(self, player, quest):
        if quest["kind"] == "single":
            return [i for i, r in enumerate(player.rocks)
                    if r.base_type == quest["rock_type"] and r.rarity == quest["rarity"]]
        elif quest["kind"] == "any_rarity":
            min_idx = RARITY_ORDER.index(quest["min_rarity"])
            return [i for i, r in enumerate(player.rocks)
                    if RARITY_ORDER.index(r.rarity) >= min_idx]
        elif quest["kind"] == "quantity":
            return [i for i, r in enumerate(player.rocks)
                    if r.base_type == quest["rock_type"]]
        elif quest["kind"] == "special":
            return [i for i, r in enumerate(player.rocks)
                    if quest["special"] in r.specials]
        return []

    def can_complete(self, player, quest_idx):
        quest = self.quests[quest_idx]
        if self._town_rep() < quest.get("min_rep", 0):
            return False
        needed = quest.get("count", 1)
        return len(self.find_matching_rocks(player, quest)) >= needed

    def complete_quest(self, player, quest_idx=0):
        quest = self.quests[quest_idx]
        needed = quest.get("count", 1)
        matching = self.find_matching_rocks(player, quest)
        if len(matching) < needed or self._town_rep() < quest.get("min_rep", 0):
            return False
        for i in sorted(matching[:needed], reverse=True):
            player.rocks.pop(i)
        self._streak += 1
        streak_mult = 1.0 + min(self._streak - 1, 2) * 0.25
        player.money += int(quest["reward"] * streak_mult * getattr(player, "blessing_mult", 1.0))
        builder = _build_prestige_rock_quest if quest_idx == 1 else _build_quest
        self.quests[quest_idx] = builder(self._rng, self.difficulty)
        return True


class RoyalCuratorNPC(RockQuestNPC):
    """Royal vault curator — collects legendary rocks and rare specials for the king."""
    def __init__(self, x, y, world, rng, biodome="temperate"):
        NPC.__init__(self, x, y, world, "npc_royal_curator")
        self.clothing  = _npc_clothing(biodome)
        self._rng      = rng
        self.difficulty = 2
        self._streak   = 0
        self.quests    = [_build_royal_rock_quest(rng), _build_royal_rock_quest(rng)]

    def complete_quest(self, player, quest_idx=0):
        quest   = self.quests[quest_idx]
        needed  = quest.get("count", 1)
        matching = self.find_matching_rocks(player, quest)
        if len(matching) < needed or self._town_rep() < quest.get("min_rep", 0):
            return False
        for i in sorted(matching[:needed], reverse=True):
            player.rocks.pop(i)
        player.money += int(quest["reward"] * getattr(player, "blessing_mult", 1.0))
        self.quests[quest_idx] = _build_royal_rock_quest(self._rng)
        return True


class WildflowerQuestNPC(NPC):
    def __init__(self, x, y, world, rng, difficulty=0, biodome="temperate"):
        super().__init__(x, y, world, "npc_herbalist")
        self.clothing = _npc_clothing(biodome)
        self._rng = rng
        self.difficulty = difficulty
        self._streak = 0
        self.quests = [_build_wf_quest(rng, difficulty), _build_prestige_wf_quest(rng, difficulty)]

    def find_matching_flowers(self, player, quest):
        if quest["kind"] == "wf_single":
            return [i for i, f in enumerate(player.wildflowers)
                    if f.flower_type == quest["flower_type"]]
        elif quest["kind"] == "wf_quantity":
            return [i for i, f in enumerate(player.wildflowers)
                    if f.flower_type == quest["flower_type"]]
        elif quest["kind"] == "wf_rarity":
            min_idx = RARITY_ORDER.index(quest["min_rarity"])
            return [i for i, f in enumerate(player.wildflowers)
                    if RARITY_ORDER.index(f.rarity) >= min_idx]
        return []

    def can_complete(self, player, quest_idx):
        quest = self.quests[quest_idx]
        if self._town_rep() < quest.get("min_rep", 0):
            return False
        needed = quest.get("count", 1)
        return len(self.find_matching_flowers(player, quest)) >= needed

    def complete_quest(self, player, quest_idx=0):
        quest = self.quests[quest_idx]
        needed = quest.get("count", 1)
        matching = self.find_matching_flowers(player, quest)
        if len(matching) < needed or self._town_rep() < quest.get("min_rep", 0):
            return False
        for i in sorted(matching[:needed], reverse=True):
            player.wildflowers.pop(i)
        self._streak += 1
        streak_mult = 1.0 + min(self._streak - 1, 2) * 0.25
        player.money += int(quest["reward"] * streak_mult * getattr(player, "blessing_mult", 1.0))
        builder = _build_prestige_wf_quest if quest_idx == 1 else _build_wf_quest
        self.quests[quest_idx] = builder(self._rng, self.difficulty)
        return True


class RoyalFloristNPC(WildflowerQuestNPC):
    """Royal garden keeper — seeks legendary flowers for the king's collection."""
    def __init__(self, x, y, world, rng, biodome="temperate"):
        NPC.__init__(self, x, y, world, "npc_royal_florist")
        self.clothing  = _npc_clothing(biodome)
        self._rng      = rng
        self.difficulty = 2
        self._streak   = 0
        self.quests    = [_build_royal_wf_quest(rng), _build_royal_wf_quest(rng)]

    def complete_quest(self, player, quest_idx=0):
        quest   = self.quests[quest_idx]
        needed  = quest.get("count", 1)
        matching = self.find_matching_flowers(player, quest)
        if len(matching) < needed or self._town_rep() < quest.get("min_rep", 0):
            return False
        for i in sorted(matching[:needed], reverse=True):
            player.wildflowers.pop(i)
        player.money += int(quest["reward"] * getattr(player, "blessing_mult", 1.0))
        self.quests[quest_idx] = _build_royal_wf_quest(self._rng)
        return True


class GemQuestNPC(NPC):
    def __init__(self, x, y, world, rng, difficulty=0, biodome="temperate"):
        super().__init__(x, y, world, "npc_jeweler")
        self.clothing = _npc_clothing(biodome)
        self._rng = rng
        self.difficulty = difficulty
        self._streak = 0
        self.quests = [_build_gem_quest(rng, difficulty), _build_prestige_gem_quest(rng, difficulty)]

    def find_matching_gems(self, player, quest):
        gems = getattr(player, "gems", [])
        if quest["kind"] == "gem_type":
            return [i for i, g in enumerate(gems)
                    if g.gem_type == quest["gem_type"]]
        elif quest["kind"] == "gem_cut":
            return [i for i, g in enumerate(gems)
                    if g.gem_type == quest["gem_type"] and g.state == "cut"]
        elif quest["kind"] == "gem_rarity":
            min_idx = RARITY_ORDER.index(quest["min_rarity"])
            return [i for i, g in enumerate(gems)
                    if RARITY_ORDER.index(g.rarity) >= min_idx]
        elif quest["kind"] == "gem_royal":
            return [i for i, g in enumerate(gems)
                    if g.gem_type == quest["gem_type"] and g.state == "cut"
                    and g.rarity == "legendary"]
        return []

    def can_complete(self, player, quest_idx):
        quest = self.quests[quest_idx]
        if self._town_rep() < quest.get("min_rep", 0):
            return False
        needed = quest.get("count", 1)
        return len(self.find_matching_gems(player, quest)) >= needed

    def complete_quest(self, player, quest_idx=0):
        quest = self.quests[quest_idx]
        needed = quest.get("count", 1)
        matching = self.find_matching_gems(player, quest)
        if len(matching) < needed or self._town_rep() < quest.get("min_rep", 0):
            return False
        for i in sorted(matching[:needed], reverse=True):
            player.gems.pop(i)
        self._streak += 1
        streak_mult = 1.0 + min(self._streak - 1, 2) * 0.25
        player.money += int(quest["reward"] * streak_mult * getattr(player, "blessing_mult", 1.0))
        builder = _build_prestige_gem_quest if quest_idx == 1 else _build_gem_quest
        self.quests[quest_idx] = builder(self._rng, self.difficulty)
        return True


class RoyalJewelerNPC(GemQuestNPC):
    """Crown jeweler — seeks legendary cut gems for the royal treasury."""
    def __init__(self, x, y, world, rng, biodome="temperate"):
        NPC.__init__(self, x, y, world, "npc_royal_jeweler")
        self.clothing  = _npc_clothing(biodome)
        self._rng      = rng
        self.difficulty = 2
        self._streak   = 0
        self.quests    = [_build_royal_gem_quest(rng), _build_royal_gem_quest(rng)]

    def complete_quest(self, player, quest_idx=0):
        quest   = self.quests[quest_idx]
        needed  = quest.get("count", 1)
        matching = self.find_matching_gems(player, quest)
        if len(matching) < needed or self._town_rep() < quest.get("min_rep", 0):
            return False
        for i in sorted(matching[:needed], reverse=True):
            player.gems.pop(i)
        player.money += int(quest["reward"] * getattr(player, "blessing_mult", 1.0))
        self.quests[quest_idx] = _build_royal_gem_quest(self._rng)
        return True


class RoyalPaleontologistNPC(NPC):
    """Royal paleontologist — seeks legendary fossils for the king's museum."""
    def __init__(self, x, y, world, rng, biodome="temperate"):
        super().__init__(x, y, world, "npc_royal_paleontologist")
        self.clothing = _npc_clothing(biodome)
        self._rng     = rng
        self.quests   = [_build_royal_fossil_quest(rng), _build_royal_fossil_quest(rng)]

    def find_matching_fossils(self, player, quest):
        fossils = getattr(player, "fossils", [])
        if quest["kind"] == "fossil_single":
            return [i for i, f in enumerate(fossils)
                    if f.fossil_type == quest["fossil_type"] and f.rarity == quest["rarity"]]
        elif quest["kind"] == "fossil_special":
            return [i for i, f in enumerate(fossils)
                    if quest["special"] in getattr(f, "specials", [])]
        return []

    def can_complete(self, player, quest_idx):
        quest = self.quests[quest_idx]
        if self._town_rep() < quest.get("min_rep", 0):
            return False
        return len(self.find_matching_fossils(player, quest)) >= quest.get("count", 1)

    def complete_quest(self, player, quest_idx=0):
        quest    = self.quests[quest_idx]
        needed   = quest.get("count", 1)
        matching = self.find_matching_fossils(player, quest)
        if len(matching) < needed or self._town_rep() < quest.get("min_rep", 0):
            return False
        for i in sorted(matching[:needed], reverse=True):
            player.fossils.pop(i)
        player.money += int(quest["reward"] * getattr(player, "blessing_mult", 1.0))
        self.quests[quest_idx] = _build_royal_fossil_quest(self._rng)
        return True


class RoyalAnglerNPC(NPC):
    """Royal angler — seeks legendary fish for the king's banquet."""
    def __init__(self, x, y, world, rng, biodome="temperate"):
        super().__init__(x, y, world, "npc_royal_angler")
        self.clothing = _npc_clothing(biodome)
        self._rng     = rng
        self.quests   = [_build_royal_fish_quest(rng), _build_royal_fish_quest(rng)]

    def find_matching_fish(self, player, quest):
        fish_list = getattr(player, "fish_caught", [])
        if quest["kind"] == "fish_single":
            return [i for i, f in enumerate(fish_list)
                    if f.species == quest["species"] and f.rarity == quest["rarity"]]
        return []

    def can_complete(self, player, quest_idx):
        quest = self.quests[quest_idx]
        if self._town_rep() < quest.get("min_rep", 0):
            return False
        return len(self.find_matching_fish(player, quest)) >= quest.get("count", 1)

    def complete_quest(self, player, quest_idx=0):
        quest    = self.quests[quest_idx]
        needed   = quest.get("count", 1)
        matching = self.find_matching_fish(player, quest)
        if len(matching) < needed or self._town_rep() < quest.get("min_rep", 0):
            return False
        for i in sorted(matching[:needed], reverse=True):
            player.fish_caught.pop(i)
        player.money += int(quest["reward"] * getattr(player, "blessing_mult", 1.0))
        self.quests[quest_idx] = _build_royal_fish_quest(self._rng)
        return True


class TradeNPC(NPC):
    def __init__(self, x, y, world, rng, biodome="temperate"):
        super().__init__(x, y, world, "npc_trade")
        self.clothing = _npc_clothing(biodome)
        n = rng.randint(3, 4)
        self.trades = rng.sample(TRADE_TABLE, n)

    def boosted_gold(self, trade_idx):
        _, _, receive_gold = self.trades[trade_idx]
        return max(1, round(receive_gold * _rep_buy_bonus(self._town_rep())))

    def rep_bonus_pct(self):
        return round((_rep_buy_bonus(self._town_rep()) - 1.0) * 100)

    def can_trade(self, trade_idx, player):
        item_id, give_count, _ = self.trades[trade_idx]
        return player.inventory.get(item_id, 0) >= give_count

    def execute_trade(self, trade_idx, player):
        if not self.can_trade(trade_idx, player):
            return False
        item_id, give_count, _ = self.trades[trade_idx]
        player.inventory[item_id] -= give_count
        if player.inventory[item_id] <= 0:
            del player.inventory[item_id]
            for i in range(len(player.hotbar)):
                if player.hotbar[i] == item_id:
                    player.hotbar[i] = None
        player.money += self.boosted_gold(trade_idx)
        return True


# ---------------------------------------------------------------------------
# Merchant / Restaurant / Shrine data
# ---------------------------------------------------------------------------

MERCHANT_SHOP_TABLE = [
    # (item_id, gold_cost, display_name, barter_item, barter_qty)
    ("iron_chunk",     8,  "Iron Chunk",    "lumber",       5),
    ("coal",          12,  "Coal",          "stone_chip",   7),
    ("lumber",        10,  "Lumber",        "stone_chip",   6),
    ("wool",          15,  "Wool",          "lumber",       9),
    ("crystal_shard", 40,  "Crystal Shard", "iron_chunk",   8),
    ("stone_chip",     5,  "Stone Chip",    "dirt_clump",  10),
    ("obsidian_slab", 50,  "Obsidian Slab", "coal",        10),
    ("ruby",          70,  "Ruby",          "spirits",      4),
    ("milk",          18,  "Milk",          "wool",         4),
    ("tempered_iron", 60,  "Tempered Iron", "iron_chunk",  10),
]

COFFEE_SHOP_TABLE = [
    # (item_id, gold_cost, display_name, barter_item, barter_qty)
    ("coffee_seed",          12, "Coffee Seed",          "lumber",        3),
    ("coffee_cherry",         8, "Coffee Cherry",        "dirt_clump",    6),
    ("drip_coffee",          20, "Drip Coffee",          "wheat",         5),
    ("espresso",             25, "Espresso",            "coffee_cherry", 10),
    ("pour_over",            30, "Pour Over",           "coffee_cherry", 12),
    ("cold_brew",            35, "Cold Brew",           "coffee_cherry", 15),
    ("french_press",         32, "French Press",        "coffee_cherry", 14),
    ("roaster_item",        150, "Coffee Roaster",      "iron_chunk",    15),
]

WINE_SHOP_TABLE = [
    # (item_id, gold_cost, display_name, barter_item, barter_qty)
    ("red_wine",             25, "Red Wine",             "apple",        10),
    ("white_wine",           25, "White Wine",           "apple",        10),
    ("rose_wine",            30, "Rosé Wine",            "strawberry",   15),
    ("sparkling_wine",       45, "Sparkling Wine",       "bread",         5),
    ("wine_amphora",         60, "Wine Amphora",         "clay",         20),
    ("wine_cellar_item",    200, "Wine Cellar",          "lumber",       40),
]

BEER_SHOP_TABLE = [
    # (item_id, gold_cost, display_name, barter_item, barter_qty)
    ("hop_seed",              8, "Hop Seed",             "lumber",        3),
    ("hop_cluster",           6, "Hop Cluster",          "dirt_clump",    6),
    ("brew_kettle_item",    180, "Brew Kettle",           "iron_chunk",   18),
    ("ferm_vessel_item",    200, "Ferm. Vessel",          "iron_chunk",   20),
    ("taproom_item",        220, "Taproom",               "iron_chunk",   22),
    ("ale",                  20, "Ale",                   "wheat",         6),
    ("lager",                18, "Lager",                 "wheat",         5),
    ("stout",                22, "Stout",                 "coal",          4),
    ("ipa",                  25, "IPA",                   "wheat",         7),
    ("wheat_beer",           20, "Wheat Beer",            "wheat",         6),
    ("saison",               24, "Saison",                "wheat",         7),
    ("porter",               22, "Porter",                "coal",          4),
    ("amber_ale",            20, "Amber Ale",             "wheat",         6),
    ("pilsner",              18, "Pilsner",               "wheat",         5),
    ("brown_ale",            20, "Brown Ale",             "wheat",         6),
    ("sour",                 24, "Sour",                  "mushroom",      4),
    ("barleywine",           28, "Barleywine",            "wheat",         8),
]

# Prices BeerMerchantNPC / TavernkeeperNPC pay when buying beers from the player.
TAVERN_BUY_TABLE = {
    "ale": 16,            "lager": 14,          "stout": 18,
    "ipa": 20,            "wheat_beer": 16,     "saison": 19,
    "porter": 18,         "amber_ale": 16,      "pilsner": 14,
    "brown_ale": 16,      "sour": 19,           "barleywine": 22,
    "ale_fine": 36,       "lager_fine": 33,     "stout_fine": 40,
    "ipa_fine": 46,       "wheat_beer_fine": 36,"saison_fine": 43,
    "porter_fine": 40,    "amber_ale_fine": 36, "pilsner_fine": 33,
    "brown_ale_fine": 36, "sour_fine": 43,      "barleywine_fine": 50,
    "ale_reserve": 70,    "lager_reserve": 62,  "stout_reserve": 78,
    "ipa_reserve": 88,    "wheat_beer_reserve": 70, "saison_reserve": 82,
    "porter_reserve": 78, "amber_ale_reserve": 70,  "pilsner_reserve": 62,
    "brown_ale_reserve": 70, "sour_reserve": 82, "barleywine_reserve": 92,
}

TAVERN_MENU = [
    # (item_id, gold_cost)
    ("bread",          8),
    ("cooked_beef",   16),
    ("cooked_chicken",13),
    ("cheese",         9),
    ("ale",           12),
    ("lager",         11),
    ("stout",         14),
    ("ipa",           15),
]


# Items unlocked in merchant shops as the host town grows in tier.

MERCHANT_TIER_TABLE = {
    2: [
        ("rare_mushroom",    40, "Rare Mushroom",    "lumber",        22),
        ("red_wine_fine",    45, "Fine Red Wine",    "spirits",        3),
        ("herbs",            20, "Mixed Herbs",      "wool",           5),
    ],
    3: [
        ("gold_nugget",      35, "Gold Nugget",      "crystal_shard",  2),
        ("red_wine_reserve", 65, "Reserve Wine",     "spirits",        5),
        ("fossil_fragment",  55, "Fossil Fragment",  "iron_chunk",     9),
    ],
}

BLACKSMITH_SHOP_TABLE = [
    # (item_id, gold_cost, display_name, barter_item, barter_qty)
    ("stone_pickaxe",     12, "Stone Pickaxe",    "stone_chip",  6),
    ("iron_pickaxe",      35, "Iron Pickaxe",     "iron_chunk",  8),
    ("stone_axe",         14, "Stone Axe",        "lumber",      5),
    ("iron_axe",          40, "Iron Axe",         "iron_chunk",  8),
    ("hoe",               18, "Hoe",              "lumber",      6),
    ("tempered_iron",     55, "Tempered Iron",    "iron_chunk",  10),
    ("tempered_pickaxe",  90, "Tempered Pickaxe", "tempered_iron", 4),
    ("tempered_axe",      95, "Tempered Axe",     "tempered_iron", 4),
]

INN_MENU = [
    # (item_id, gold_cost)
    ("bread",         8),
    ("beef_stew",    22),
    ("cooked_beef",  16),
    ("cooked_chicken", 14),
    ("cheese",       10),
    ("cooked_egg",    9),
    ("noodle_soup",  18),
]

SCHOLAR_SHOP_TABLE = [
    # (item_id, gold_cost, display_name, barter_item, barter_qty)
    ("philosophers_scroll", 30, "Philosophers Scroll", "iron_chunk",  5),
    ("votive_tablet",       25, "Votive Tablet",       "stone_chip",  8),
    ("olive_branch",        20, "Olive Branch",        "lumber",      4),
    ("greek_theatre_mask",  40, "Theatre Mask",        "wool",        4),
]

CUISINE_MENUS = {
    "Noodle Shop": [
        ("beef_noodle_soup",    18),
        ("chicken_noodle_soup", 15),
        ("noodle_soup",         12),
        ("ramen",               20),
        ("chili_noodles",       16),
    ],
    "BBQ Stall": [
        ("mutton_skewer",       14),
        ("bbq_beef_ribs",       22),
        ("grilled_corn",         8),
        ("stuffed_pepper",      16),
        ("grilled_mushroom",    12),
        ("eggplant_skewer",     13),
    ],
    "Dim Sum House": [
        ("steamed_bun",          8),
        ("veggie_dumplings",    14),
        ("chicken_bun",         15),
        ("crystal_rolls",       13),
        ("rice_noodle_roll",    10),
    ],
    "Bakery": [
        ("bread",                8),
        ("corn_bread",          10),
        ("pumpkin_pie",         20),
        ("apple_pie",           18),
        ("carrot_cake",         22),
        ("cheese_bread",        14),
    ],
    "Stew House": [
        ("beef_stew",           22),
        ("mutton_hotpot",       20),
        ("chicken_mushroom_pot", 18),
        ("hot_pot_broth",       15),
        ("braised_chicken",     17),
    ],
    "Tapas Bar": [
        ("patatas_bravas",      12),
        ("croquetas",           14),
        ("gambas_al_ajillo",    18),
        ("tortilla_espanola",   16),
        ("pimientos_padron",    10),
        ("pan_tostado",          8),
        ("chorizo",             13),
        ("espetos",             15),
    ],
    "Mezze Restaurant": [
        ("hummus",              10),
        ("baba_ghanoush",       12),
        ("falafel",             13),
        ("shawarma",            20),
        ("tabbouleh",           11),
        ("kibbeh",              15),
        ("fattoush",            12),
        ("manakish",            14),
        ("kofte",               16),
        ("labneh",               9),
    ],
    "Trattoria": [
        ("bruschetta",          10),
        ("minestrone",          14),
        ("spaghetti_pomodoro",  16),
        ("pesto_gnocchi",       17),
        ("ossobuco",            24),
        ("ribollita",           15),
        ("bistecca",            22),
        ("cacio_e_pepe",        16),
        ("zuppa_di_pesce",      18),
        ("polenta",             11),
    ],
    "Spanish Bodega": [
        ("pan_tostado",          8),
        ("empanada",            14),
        ("patatas_bravas",      12),
        ("tortilla_espanola",   16),
        ("croquetas",           14),
        ("paella",              22),
        ("cocido_madrileno",    20),
        ("rabo_de_toro",        22),
        ("fabada",              18),
        ("churros",              9),
    ],
    "Japanese Izakaya": [
        ("edamame",              8),
        ("miso_soup",           10),
        ("onigiri",             12),
        ("gyoza",               13),
        ("yakitori",            14),
        ("tempura",             18),
        ("soba",                15),
        ("udon",                15),
        ("teriyaki_chicken",    19),
        ("tonkatsu",            20),
        ("matcha_cake",         12),
    ],
    "Greek Taverna": [
        ("tzatziki",             9),
        ("horiatiki",           11),
        ("spanakopita",         14),
        ("dolmades",            13),
        ("keftedes",            15),
        ("saganaki",            14),
        ("souvlaki",            17),
        ("moussaka",            20),
        ("kleftiko",            23),
        ("pastitsio",           19),
        ("loukoumades",         11),
    ],
    "Roman Thermopolium": [
        ("puls",                 8),
        ("flatbread",            8),
        ("olive",                6),
        ("isicia",              14),
        ("patina",              15),
        ("garum_fish",          16),
        ("pullum_numidicum",    19),
        ("libum",               11),
        ("dulcia",              10),
    ],
    "Indian Dhaba": [
        ("naan",                 9),
        ("raita",                8),
        ("samosa",              12),
        ("aloo_gobi",           15),
        ("chana_masala",        17),
        ("dal_makhani",         17),
        ("paneer_tikka",        17),
        ("tandoori_chicken",    21),
        ("butter_chicken",      21),
        ("biryani",             23),
        ("kheer",               12),
    ],
}

RELIGION_BY_BIOME = {
    "alpine_mountain": ("Himalayan Monastery",  "dzong"),
    "rocky_mountain":  ("Mountain Monastery",   "temple"),
    "temperate":       ("Forest Chapel",        "chapel"),
    "boreal":          ("Forest Chapel",        "chapel"),
    "birch_forest":    ("Woodland Shrine",      "chapel"),
    "redwood":         ("Grove Sanctuary",      "chapel"),
    "desert":          ("Desert Sanctum",       "desert_shrine"),
    "arid_steppe":     ("Desert Sanctum",       "desert_shrine"),
    "savanna":         ("Savanna Altar",        "desert_shrine"),
    "jungle":          ("Jungle Altar",         "jungle_shrine"),
    "tropical":        ("Tropical Shrine",      "jungle_shrine"),
    "wetland":         ("Swamp Oracle",         "jungle_shrine"),
    "tundra":          ("Standing Stones",      "standing_stones"),
    "steppe":          ("Ancestor Circle",      "standing_stones"),
    "canyon":          ("Cave Sanctum",         "temple"),
    "mediterranean":   ("Temple Precinct",      "classical"),
    "east_asian":      ("Shinto Shrine",        "shinto"),
    "south_asian":     ("Hindu Mandir",         "mandir"),
}

SHRINE_FLAVOR = {
    "dzong":           "Prayer flags snap in the mountain wind.\nThe whitewashed walls glow against dark peaks.\nBells toll somewhere above the clouds.",
    "temple":          "Incense drifts through stone archways.\nMonks chant in quiet reverence.",
    "chapel":          "Sunlight filters through the canopy above.\nA small bell hangs in the doorway.\nThe wood is worn smooth by many hands.",
    "desert_shrine":   "Carved stone glows in the desert heat.\nOld prayers are scratched into the walls.\nA clay bowl holds the remains of an offering.",
    "jungle_shrine":   "Moss clings to ancient carvings.\nThe air hums with the sound of insects.\nSomething watches from between the stones.",
    "standing_stones": "Weathered stones stand in a silent row.\nNames are carved in a forgotten tongue.\nThe ground between them never grows grass.",
    "shinto":          "A red gate frames the path ahead.\nStone lanterns flicker in the still air.\nSomewhere, a wind chime answers the breeze.",
    "mandir":          "Carved figures cover every surface of the shrine.\nThe scent of marigold and incense fills the air.\nA bell sounds once, then fades into silence.",
    "classical":       "White columns rise into clear sky.\nOlive branches hang above the entrance.\nA slow-burning flame marks the sacred threshold.",
}


REP_RANKS = [
    (1000, "Champion", (220, 180,  40)),
    ( 500, "Honored",  (160, 210,  90)),
    ( 200, "Trusted",  ( 90, 200, 160)),
    (  50, "Familiar", (130, 175, 130)),
    (   0, "Stranger", (145, 140, 140)),
]


def rep_rank(rep):
    for threshold, name, color in REP_RANKS:
        if rep >= threshold:
            return name, color
    return "Stranger", (145, 140, 140)


def _rep_discount(rep, npc=None):
    """Reputation discount multiplier for purchases.

    Optional `npc` lets the caller pick up two region-level modifiers:
    - Mercantile leader buff: once the local town's reputation crosses 200,
      a Mercantile region stacks an extra 10% off.
    - Diplomatic anchor: shops in regions allied to the player's anchor region
      grant 10% off; rival regions add 10%.
    """
    if   rep >= 1000: base = 0.60
    elif rep >=  500: base = 0.70
    elif rep >=  200: base = 0.80
    elif rep >=   50: base = 0.90
    else:             base = 1.0
    if npc is not None:
        from towns import TOWNS, REGIONS, anchor_region_id, relation_between
        tid = npc._nearest_town_id()
        if tid is not None and tid in TOWNS:
            town   = TOWNS[tid]
            region = REGIONS.get(town.region_id)
            if region and region.agenda == "mercantile" and town.reputation >= 200:
                base *= 0.90
            anchor = anchor_region_id()
            if anchor is not None and region is not None and anchor != region.region_id:
                rel = relation_between(anchor, region.region_id)
                if   rel == "allied": base *= 0.90
                elif rel == "rival":  base *= 1.10
    return base


def _region_for_npc(npc):
    """Return the Region the npc is currently in, or None."""
    from towns import TOWNS, REGIONS
    tid = npc._nearest_town_id()
    if tid is None or tid not in TOWNS:
        return None
    return REGIONS.get(TOWNS[tid].region_id)


def _item_price_tags(item_id) -> set:
    """Best-effort tag set used to score an item against a region's specialty.

    Combines town_needs categories (food / wood / stone / metal / weapons /
    wine / coffee / spirits / pottery / tea / herbs) with the contract tag
    overrides — covers most items the player can buy or sell.
    """
    from town_needs import ITEM_TO_CATEGORY
    tags = set()
    cat = ITEM_TO_CATEGORY.get(item_id)
    if cat:
        tags.add(cat)
    tags.update(_CONTRACT_TAGS.get(item_id, ()))
    return tags


def _specialty_price_mult(npc, item_id) -> float:
    """Region specialty multiplier: −15% on local exports, +15% on imports.

    Returns 1.0 if the item is neither tagged as an export nor an import for
    the local region (most decorative or unique items).
    """
    region = _region_for_npc(npc)
    if region is None:
        return 1.0
    from towns import region_specialty
    spec = region_specialty(region)
    item_tags = _item_price_tags(item_id)
    if item_tags & set(spec.get("exports", ())):
        return 0.85
    if item_tags & set(spec.get("imports", ())):
        return 1.15
    return 1.0


def specialty_price_label(npc, item_id) -> str:
    """A short tag a shop UI can render next to a price ('export' / 'import')."""
    mult = _specialty_price_mult(npc, item_id)
    if mult < 1.0:
        return "export"
    if mult > 1.0:
        return "import"
    return ""


def _shop_size_bonus(npc, agenda_match: str) -> int:
    """+1 to a shop's sample size when the npc's region matches `agenda_match`.

    Used by Blacksmith / Merchant / Scholar to widen their inventory in
    regions whose leader prefers their goods.
    """
    region = _region_for_npc(npc)
    return 1 if (region and region.agenda == agenda_match) else 0


def _wealth_stock_bonus(npc) -> int:
    """Region wealth modifier on shop stock count: rich +1, poor -1, modest 0."""
    region = _region_for_npc(npc)
    if region is None:
        return 0
    if region.wealth == "rich": return  1
    if region.wealth == "poor": return -1
    return 0


def _rep_buy_bonus(rep):
    if rep >= 1000: return 1.50
    if rep >= 500:  return 1.40
    if rep >= 200:  return 1.25
    if rep >= 50:   return 1.10
    return 1.0


class MerchantNPC(NPC):
    def __init__(self, x, y, world, rng, biodome="temperate"):
        super().__init__(x, y, world, "npc_merchant")
        self.clothing = _npc_clothing(biodome)
        tier = self._town_tier()
        pool = list(MERCHANT_SHOP_TABLE)
        for t in range(2, tier + 1):
            pool.extend(MERCHANT_TIER_TABLE.get(t, []))
        # Mercantile leaders lean on their trade connections — even a tier-1
        # town gets the rare tier-3 items pooled in.
        region = _region_for_npc(self)
        if region and region.agenda == "mercantile":
            pool.extend(MERCHANT_TIER_TABLE.get(3, []))
        n = (rng.randint(3, 4)
             + (1 if tier >= 2 else 0)
             + _shop_size_bonus(self, "mercantile")
             + _wealth_stock_bonus(self))
        n = max(1, n)
        self.shop = rng.sample(pool, min(n, len(pool)))

    def discounted_cost(self, idx, player=None):
        _, cost, *_ = self.shop[idx]
        item_id = self.shop[idx][0]
        return max(1, round(cost
                            * _rep_discount(self._town_rep(), self)
                            * _specialty_price_mult(self, item_id)
                            * self._beloved_price_mult(player)
                            * self._dynasty_price_mult(player)))

    def rep_discount_pct(self):
        return round((1.0 - _rep_discount(self._town_rep(), self)) * 100)

    def can_buy(self, idx, player):
        return player.money >= self.discounted_cost(idx, player)

    def execute_purchase(self, idx, player):
        if not self.can_buy(idx, player):
            return False
        item_id = self.shop[idx][0]
        player.money -= self.discounted_cost(idx, player)
        player._add_item(item_id)
        return True

    def can_barter(self, idx, player):
        *_, barter_item, barter_qty = self.shop[idx]
        return player.inventory.get(barter_item, 0) >= barter_qty

    def execute_barter(self, idx, player):
        if not self.can_barter(idx, player):
            return False
        item_id, _, _, barter_item, barter_qty = self.shop[idx]
        player.inventory[barter_item] = player.inventory.get(barter_item, 0) - barter_qty
        if player.inventory[barter_item] <= 0:
            del player.inventory[barter_item]
            for i in range(len(player.hotbar)):
                if player.hotbar[i] == barter_item:
                    player.hotbar[i] = None
        player._add_item(item_id)
        return True


class CoffeeMerchantNPC(MerchantNPC):
    def __init__(self, x, y, world, rng, biodome="temperate"):
        super().__init__(x, y, world, rng, biodome)
        self.clothing = _npc_clothing(biodome)
        self.clothing["body"] = (101, 67, 33) # Coffee brown
        n = rng.randint(4, 5)
        self.shop = rng.sample(COFFEE_SHOP_TABLE, min(n, len(COFFEE_SHOP_TABLE)))


class WineMerchantNPC(MerchantNPC):
    def __init__(self, x, y, world, rng, biodome="temperate"):
        super().__init__(x, y, world, rng, biodome)
        self.clothing = _npc_clothing(biodome)
        self.clothing["body"] = (114, 47, 55) # Wine red
        n = rng.randint(4, 5)
        self.shop = rng.sample(WINE_SHOP_TABLE, min(n, len(WINE_SHOP_TABLE)))


class BeerMerchantNPC(MerchantNPC):
    """Sells brewing supplies and beers; also buys fine/reserve beers from the player."""
    def __init__(self, x, y, world, rng, biodome="temperate"):
        super().__init__(x, y, world, rng, biodome)
        self.clothing = _npc_clothing(biodome)
        self.clothing["body"] = (180, 140, 60)  # Golden ale amber
        self.display_name = "Beer Merchant"
        n = rng.randint(5, 7)
        self.shop = rng.sample(BEER_SHOP_TABLE, min(n, len(BEER_SHOP_TABLE)))

    def beer_buy_price(self, item_id):
        base = TAVERN_BUY_TABLE.get(item_id, 0)
        return max(1, round(base * _rep_buy_bonus(self._town_rep())))

    def can_sell_beer(self, item_id, player):
        return TAVERN_BUY_TABLE.get(item_id, 0) > 0 and player.inventory.get(item_id, 0) > 0

    def sell_beer(self, item_id, player):
        if not self.can_sell_beer(item_id, player):
            return 0
        price = self.beer_buy_price(item_id)
        player.inventory[item_id] -= 1
        if player.inventory[item_id] <= 0:
            del player.inventory[item_id]
            for i in range(len(player.hotbar)):
                if player.hotbar[i] == item_id:
                    player.hotbar[i] = None
        player.money += price
        return price


class DoctorNPC(NPC):
    def __init__(self, x, y, world, biodome="temperate"):
        super().__init__(x, y, world, "npc_doctor")
        self.clothing = _npc_clothing(biodome)
        self.clothing["body"] = (245, 245, 245) # White coat
        self.heal_cost = 50

    def _is_free(self, player):
        tid = getattr(self, "town_id", None) or self._nearest_town_id()
        return tid in getattr(player, "doctor_beloved_towns", set())

    def can_heal(self, player):
        if self._is_free(player):
            return player.health < player.MAX_HEALTH
        return player.money >= self.heal_cost and player.health < player.MAX_HEALTH

    def execute_heal(self, player):
        if self.can_heal(player):
            if not self._is_free(player):
                player.money -= self.heal_cost
            player.health = player.MAX_HEALTH
            return True
        return False


class MusicianNPC(NPC):
    def __init__(self, x, y, world, biodome="temperate"):
        super().__init__(x, y, world, "npc_musician")
        self.clothing = _npc_clothing(biodome)


class TownCrierNPC(NPC):
    def __init__(self, x, y, world, biodome="temperate"):
        super().__init__(x, y, world, "npc_crier")
        self.clothing = _npc_clothing(biodome)
        self.clothing["body"] = (180, 40, 40) # Royal red herald


class RestaurantNPC(NPC):

    def __init__(self, x, y, world, rng, biodome="temperate"):
        super().__init__(x, y, world, "npc_chef")
        self.clothing = _npc_clothing(biodome)
        pool = _CUISINE_POOL_BY_BIOME.get(biodome, list(CUISINE_MENUS.keys()))
        self.cuisine = rng.choice(pool)
        self.menu = CUISINE_MENUS[self.cuisine]

    def discounted_cost(self, idx, player=None):
        item_id, cost = self.menu[idx]
        return max(1, round(cost
                            * _rep_discount(self._town_rep(), self)
                            * _specialty_price_mult(self, item_id)
                            * self._beloved_price_mult(player)
                            * self._dynasty_price_mult(player)))

    def rep_discount_pct(self):
        return round((1.0 - _rep_discount(self._town_rep(), self)) * 100)

    def can_buy(self, idx, player):
        return player.money >= self.discounted_cost(idx, player)

    def execute_purchase(self, idx, player):
        if not self.can_buy(idx, player):
            return False
        item_id, _ = self.menu[idx]
        player.money -= self.discounted_cost(idx, player)
        player._add_item(item_id)
        return True


class ShrineKeeperNPC(NPC):
    def __init__(self, x, y, world, rng, difficulty=0, biodome="temperate"):
        super().__init__(x, y, world, "npc_monk")
        self.clothing = _npc_clothing(biodome)
        display_name, style = RELIGION_BY_BIOME.get(biodome, ("Forest Chapel", "chapel"))
        self.religion_name = display_name
        self.religion_style = style
        self.flavor = SHRINE_FLAVOR.get(style, SHRINE_FLAVOR["chapel"])
        self.blessing_cost = 10 + difficulty * 10

    def discounted_cost(self):
        return max(1, round(self.blessing_cost * _rep_discount(self._town_rep(), self)))

    def rep_discount_pct(self):
        return round((1.0 - _rep_discount(self._town_rep(), self)) * 100)

    def _blessing_duration(self):
        rep = self._town_rep()
        if   rep >= 1000: base = 360.0
        elif rep >=  500: base = 300.0
        elif rep >=  200: base = 240.0
        else:             base = 180.0
        # Pious leaders extend their shrine's blessings once their region's
        # standing is earned — adds ~25% on top.
        region = _region_for_npc(self)
        if region and region.agenda == "pious" and rep >= 200:
            base += 60.0
        return base

    def can_bless(self, player):
        return player.money >= self.discounted_cost()

    def give_blessing(self, player):
        if not self.can_bless(player):
            return False
        player.money -= self.discounted_cost()
        player.blessing_timer = self._blessing_duration()
        player.blessing_mult = 1.25
        return True


class JewelryMerchantNPC(NPC):
    """Buys custom jewelry pieces from the player."""
    def __init__(self, x, y, world, rng, biodome="temperate"):
        super().__init__(x, y, world, "npc_merchant")
        self.clothing = _npc_clothing(biodome)
        self.display_name = "Jewelry Merchant"

    def appraise(self, jewelry, player):
        from jewelry import calculate_value
        return calculate_value(jewelry, player, master_jeweler=getattr(player, "master_jeweler", False))

    def sell_piece(self, jewelry_uid, player):
        piece = next((j for j in player.jewelry if j.uid == jewelry_uid), None)
        if piece is None:
            return 0
        value = self.appraise(piece, player)
        player.jewelry.remove(piece)
        player.money += value
        return value


class BlacksmithNPC(NPC):
    def __init__(self, x, y, world, rng, biodome="temperate"):
        super().__init__(x, y, world, "npc_blacksmith")
        self.clothing = _npc_clothing(biodome)
        n = max(1, rng.randint(3, 4) + _shop_size_bonus(self, "martial") + _wealth_stock_bonus(self))
        self.shop = rng.sample(BLACKSMITH_SHOP_TABLE,
                               min(n, len(BLACKSMITH_SHOP_TABLE)))

    def discounted_cost(self, idx, player=None):
        _, cost, *_ = self.shop[idx]
        item_id = self.shop[idx][0]
        return max(1, round(cost
                            * _rep_discount(self._town_rep(), self)
                            * _specialty_price_mult(self, item_id)
                            * self._beloved_price_mult(player)
                            * self._dynasty_price_mult(player)))

    def rep_discount_pct(self):
        return round((1.0 - _rep_discount(self._town_rep(), self)) * 100)

    def can_buy(self, idx, player):
        return player.money >= self.discounted_cost(idx, player)

    def execute_purchase(self, idx, player):
        if not self.can_buy(idx, player):
            return False
        item_id = self.shop[idx][0]
        player.money -= self.discounted_cost(idx, player)
        player._add_item(item_id)
        return True

    def can_barter(self, idx, player):
        *_, barter_item, barter_qty = self.shop[idx]
        return player.inventory.get(barter_item, 0) >= barter_qty

    def execute_barter(self, idx, player):
        if not self.can_barter(idx, player):
            return False
        item_id, _, _, barter_item, barter_qty = self.shop[idx]
        player.inventory[barter_item] = player.inventory.get(barter_item, 0) - barter_qty
        if player.inventory[barter_item] <= 0:
            del player.inventory[barter_item]
            for i in range(len(player.hotbar)):
                if player.hotbar[i] == barter_item:
                    player.hotbar[i] = None
        player._add_item(item_id)
        return True


class InnkeeperNPC(NPC):
    def __init__(self, x, y, world, rng, difficulty=0, biodome="temperate"):
        super().__init__(x, y, world, "npc_innkeeper")
        self.clothing = _npc_clothing(biodome)
        self.rest_cost = 15 + difficulty * 10
        self.menu = INN_MENU

    def discounted_cost(self, idx=None, player=None):
        if idx is None:
            return max(1, round(self.rest_cost
                                * _rep_discount(self._town_rep(), self)
                                * self._beloved_price_mult(player)
                            * self._dynasty_price_mult(player)))
        item_id, cost = self.menu[idx]
        return max(1, round(cost
                            * _rep_discount(self._town_rep(), self)
                            * _specialty_price_mult(self, item_id)
                            * self._beloved_price_mult(player)
                            * self._dynasty_price_mult(player)))

    def rep_discount_pct(self):
        return round((1.0 - _rep_discount(self._town_rep(), self)) * 100)

    def can_buy(self, idx, player):
        return player.money >= self.discounted_cost(idx, player)

    def execute_purchase(self, idx, player):
        if not self.can_buy(idx, player):
            return False
        item_id, _ = self.menu[idx]
        player.money -= self.discounted_cost(idx, player)
        player._add_item(item_id)
        return True

    def can_rest(self, player):
        return player.money >= self.discounted_cost(None, player)

    def give_rest(self, player):
        if not self.can_rest(player):
            return False
        player.money -= self.discounted_cost(None, player)
        if getattr(player, "inn_beloved", False):
            player.health = player.MAX_HEALTH
            player.blessing_timer = 480.0
            player.blessing_mult  = 1.20
        else:
            player.blessing_timer = 240.0
            player.blessing_mult  = 1.15
        return True


class TavernkeeperNPC(InnkeeperNPC):
    """Runs a tavern — serves food and beer, buys quality beer from the player."""
    def __init__(self, x, y, world, rng, difficulty=0, biodome="temperate"):
        super().__init__(x, y, world, rng, difficulty, biodome)
        self.clothing["body"] = (120, 75, 35)  # Tavern brown
        self.display_name = "Tavernkeeper"
        self.menu = TAVERN_MENU

    def beer_buy_price(self, item_id):
        base = TAVERN_BUY_TABLE.get(item_id, 0)
        return max(1, round(base * _rep_buy_bonus(self._town_rep())))

    def can_sell_beer(self, item_id, player):
        return TAVERN_BUY_TABLE.get(item_id, 0) > 0 and player.inventory.get(item_id, 0) > 0

    def sell_beer(self, item_id, player):
        if not self.can_sell_beer(item_id, player):
            return 0
        price = self.beer_buy_price(item_id)
        player.inventory[item_id] -= 1
        if player.inventory[item_id] <= 0:
            del player.inventory[item_id]
            for i in range(len(player.hotbar)):
                if player.hotbar[i] == item_id:
                    player.hotbar[i] = None
        player.money += price
        return price


class ScholarNPC(NPC):
    def __init__(self, x, y, world, rng, biodome="temperate"):
        super().__init__(x, y, world, "npc_scholar")
        self.clothing = _npc_clothing(biodome)
        n = max(1, rng.randint(2, 3) + _shop_size_bonus(self, "scholarly") + _wealth_stock_bonus(self))
        self.shop = rng.sample(SCHOLAR_SHOP_TABLE,
                               min(n, len(SCHOLAR_SHOP_TABLE)))

    def discounted_cost(self, idx, player=None):
        _, cost, *_ = self.shop[idx]
        item_id = self.shop[idx][0]
        return max(1, round(cost
                            * _rep_discount(self._town_rep(), self)
                            * _specialty_price_mult(self, item_id)
                            * self._beloved_price_mult(player)
                            * self._dynasty_price_mult(player)))

    def rep_discount_pct(self):
        return round((1.0 - _rep_discount(self._town_rep(), self)) * 100)

    def can_buy(self, idx, player):
        return player.money >= self.discounted_cost(idx, player)

    def execute_purchase(self, idx, player):
        if not self.can_buy(idx, player):
            return False
        item_id = self.shop[idx][0]
        player.money -= self.discounted_cost(idx, player)
        player._add_item(item_id)
        return True

    def can_barter(self, idx, player):
        *_, barter_item, barter_qty = self.shop[idx]
        return player.inventory.get(barter_item, 0) >= barter_qty

    def execute_barter(self, idx, player):
        if not self.can_barter(idx, player):
            return False
        item_id, _, _, barter_item, barter_qty = self.shop[idx]
        player.inventory[barter_item] = player.inventory.get(barter_item, 0) - barter_qty
        if player.inventory[barter_item] <= 0:
            del player.inventory[barter_item]
            for i in range(len(player.hotbar)):
                if player.hotbar[i] == barter_item:
                    player.hotbar[i] = None
        player._add_item(item_id)
        return True


LEADER_CONTRACT_TABLE = [
    # (item_id, give_count, reward_gold, display_name, min_rep, rep_bonus_per_town)
    ("lumber",        30,  150, "Timber Supply",     0,   2),
    ("wool",          20,  180, "Wool Bales",        50,  2),
    ("iron_chunk",    25,  220, "Iron Shipment",    100,  3),
    ("herbs",         15,  280, "Medicinal Herbs",  150,  3),
    ("pottery",       12,  300, "Fine Pottery",     200,  4),
    ("coffee",         8,  380, "Coffee Reserve",   250,  4),
    ("tea",           10,  340, "Tea Consignment",  250,  4),
    ("red_wine",       8,  360, "Regional Wine",    200,  5),
    ("ale",            8,  300, "Craft Beer Cask",  150,  4),
    ("spirits",        6,  450, "Premium Spirits",  300,  5),
    ("tempered_iron",  5,  500, "Forged Steel",     400,  6),
    ("crystal_shard",  3,  600, "Crystal Cache",    500,  8),
]

# Tag each contract item so we can weight the random pick by agenda + imports.
# Tags are intentionally broad — they match LEADER_AGENDAS["tags"] and
# BIOME_GROUP_SPECIALTIES export/import vocabulary in towns.py.
_CONTRACT_TAGS: dict[str, tuple] = {
    "lumber":        ("wood",),
    "wool":          ("textiles",),
    "iron_chunk":    ("metal",),
    "herbs":         ("herbs",),
    "pottery":       ("pottery",),
    "coffee":        ("coffee",),
    "tea":           ("tea",),
    "red_wine":      ("wine",),
    "ale":           ("beer",),
    "spirits":       ("spirits",),
    "tempered_iron": ("metal", "weapons"),
    "crystal_shard": ("gems",),
}


def _pick_contract_for_region(rng, region):
    """Pick a contract for `region`, weighted by leader agenda + region imports.
    Adds a smuggling premium when the chosen item happens to be a rival
    region's signature export.

    Returns None if the player's diplomatic anchor is rival to this region and
    a 50% refusal roll fires — surfaces as an empty contract slot in the UI.
    """
    if region is not None:
        from towns import anchor_region_id, relation_between
        anchor = anchor_region_id()
        if (anchor is not None and anchor != region.region_id
                and relation_between(anchor, region.region_id) == "rival"
                and rng.random() < 0.5):
            return None

    pool = LEADER_CONTRACT_TABLE
    preferred: set = set()
    if region is not None:
        from towns import LEADER_AGENDAS, BIOME_GROUP_SPECIALTIES
        preferred.update(LEADER_AGENDAS.get(region.agenda, {}).get("tags", ()))
        preferred.update(BIOME_GROUP_SPECIALTIES.get(region.biome_group, {}).get("imports", ()))

    if preferred:
        weighted = []
        for entry in pool:
            tags = set(_CONTRACT_TAGS.get(entry[0], ()))
            weighted.extend([entry] * (4 if tags & preferred else 1))
        chosen = rng.choice(weighted)
    else:
        chosen = rng.choice(pool)

    contract = list(chosen)

    # Wealth multiplier on reward — rich regions pay more, poor pay less.
    if region is not None:
        if   region.wealth == "rich": contract[2] = int(contract[2] * 1.25)
        elif region.wealth == "poor": contract[2] = int(contract[2] * 0.80)

    # Danger premium — wild regions pay a hazard bonus on top of any other modifiers.
    if region is not None and region.danger == "wild":
        contract[2] = int(contract[2] * 1.20)
        contract[3] = f"☠ {contract[3]}"   # ☠ marks wild-region hazard pay

    # Rival-export smuggling premium: if the contract item is an export of any
    # region this leader rivals, the reward gets +50% and the name is marked.
    if region is not None and region.relations:
        from towns import REGIONS, BIOME_GROUP_SPECIALTIES
        item_tags = set(_CONTRACT_TAGS.get(contract[0], ()))
        for rid, rel in region.relations.items():
            if rel != "rival":
                continue
            rival = REGIONS.get(rid)
            if rival is None:
                continue
            rival_exports = set(BIOME_GROUP_SPECIALTIES.get(rival.biome_group, {}).get("exports", ()))
            if item_tags & rival_exports:
                contract[2] = int(contract[2] * 1.5)
                contract[3] = f"⚔ {contract[3]}"   # ⚔ marks smuggling premium
                break

    return contract


class LeaderNPC(NPC):
    """Region leader who resides in a capital town's castle."""
    def __init__(self, x, y, world, region_id: int, region_name: str,
                 leader_name: str, leader_color: tuple, palace_type: str = "castle"):
        super().__init__(x, y, world, "npc_leader")
        self.region_id   = region_id
        self.region_name = region_name
        self.leader_name = leader_name
        self.leader_color = leader_color
        self.palace_type  = palace_type
        self.display_name = leader_name
        import random as _rnd
        self._rng = _rnd.Random(int(x) ^ (getattr(world, "seed", 0) * 0x9E3779B9))
        self.contracts = [self._new_contract(), self._new_contract()]

    def _new_contract(self):
        from towns import REGIONS
        return _pick_contract_for_region(self._rng, REGIONS.get(self.region_id))

    def can_fulfill(self, idx, player):
        contract = self.contracts[idx]
        if contract is None:
            return False
        item_id, give_count, _, _, min_rep, _ = contract
        return (self._town_rep() >= min_rep and
                player.inventory.get(item_id, 0) >= give_count)

    def execute_contract(self, idx, player):
        if not self.can_fulfill(idx, player):
            return False
        item_id, give_count, reward_gold, _, _, rep_bonus = self.contracts[idx]
        player.inventory[item_id] = player.inventory.get(item_id, 0) - give_count
        if player.inventory[item_id] <= 0:
            del player.inventory[item_id]
            for i in range(len(player.hotbar)):
                if player.hotbar[i] == item_id:
                    player.hotbar[i] = None
        player.money += reward_gold
        from towns import TOWNS, REGIONS, _cascade_rep
        region = REGIONS.get(self.region_id)
        if region:
            for tid in region.member_town_ids:
                town = TOWNS.get(tid)
                if town:
                    town.reputation += rep_bonus
            # Allies/rivals feel the ripple — allies +¼, rivals -1/10.
            _cascade_rep(self.region_id, rep_bonus)
        self.contracts[idx] = self._new_contract()
        return True

    def regional_rep(self):
        from towns import TOWNS, REGIONS
        region = REGIONS.get(self.region_id)
        if region is None:
            return 0
        return sum(TOWNS[tid].reputation for tid in region.member_town_ids if tid in TOWNS)


class LandmarkNPC(NPC):
    """Stands at a capital's landmark; fires a one-per-day agenda-keyed effect."""
    def __init__(self, x, y, world, region_id: int, landmark_name: str, tagline: str):
        super().__init__(x, y, world, "npc_landmark")
        self.region_id     = region_id
        self.landmark_name = landmark_name
        self.tagline       = tagline
        self.display_name  = landmark_name

    def trigger(self, player) -> tuple[bool, str, str]:
        """Run the landmark's agenda effect for the player. Returns (ok, title, detail)."""
        from landmarks import apply_effect
        from towns import REGIONS
        region = REGIONS.get(self.region_id)
        return apply_effect(player, region, getattr(self.world, "day_count", 0))


# ---------------------------------------------------------------------------
# City generation
# ---------------------------------------------------------------------------

_DESERT_BIOMES    = {"desert", "arid_steppe"}
_ARABIA_BIOMES    = {"savanna"}
_ARABIA_PALETTE   = (SANDSTONE_BLOCK, ADOBE_BRICK)
_ARABIA_SWAP      = {"house": "tent", "two_story": "tent", "three_story": "tent",
                     "longhouse": "caravanserai", "inn": "caravanserai"}
_DESERT_PALETTE   = (SANDSTONE_BLOCK, POLISHED_MARBLE)
_DOME_SWAP        = {"house": "dome", "two_story": "dome", "three_story": "dome",
                     "longhouse": "dome"}

_HIMALAYAN_BIOMES  = {"alpine_mountain", "tundra"}
_HIMALAYAN_PALETTE = (WHITEWASHED_WALL, MONASTERY_ROOF)
_HIMALAYAN_SWAP    = {"house": "himalayan", "two_story": "himalayan",
                      "three_story": "himalayan", "longhouse": "himalayan"}

_MEDITERRANEAN_BIOMES  = {"mediterranean"}
_MEDITERRANEAN_PALETTES = [
    (WHITE_PLASTER_WALL, SPANISH_ROOF_TILE),
    (LIMESTONE_BLOCK,    HOUSE_ROOF_STONE),
    (ADOBE_BRICK,        SPANISH_ROOF_TILE),
]

_EAST_ASIAN_BIOMES  = {"east_asian"}
_EAST_ASIAN_PALETTE = (PINE_PLANK_WALL, SLATE_SHINGLE)
_EAST_ASIAN_SWAP    = {"shrine": "temple"}

_SOUTH_ASIAN_BIOMES  = {"south_asian"}
_SOUTH_ASIAN_PALETTES = [
    (LIMESTONE_BLOCK, TERRACOTTA_ROOF_TILE),
    (ADOBE_BRICK,     TERRACOTTA_ROOF_TILE),
]

# Restaurant wall/awning blocks keyed by culture style
_RESTAURANT_STYLES = {
    "default":       (RESTAURANT_WALL,    RESTAURANT_AWNING),
    "mediterranean": (WHITE_PLASTER_WALL, SPANISH_ROOF_TILE),
    "east_asian":    (PINE_PLANK_WALL,    PAGODA_EAVE),
    "south_asian":   (LIMESTONE_BLOCK,    TERRACOTTA_ROOF_TILE),
    "desert":        (SANDSTONE_BLOCK,    POLISHED_MARBLE),
}
_RESTAURANT_STYLE_BY_BIOME = {
    "mediterranean": "mediterranean",
    "east_asian":    "east_asian",
    "south_asian":   "south_asian",
    "desert":        "desert",
    "arid_steppe":   "desert",
    "savanna":       "desert",
}

# Cuisine pools weighted by biome — fallback is all menus
_CUISINE_POOL_BY_BIOME: dict[str, list[str]] = {
    "mediterranean": ["Trattoria", "Spanish Bodega", "Tapas Bar", "Greek Taverna"],
    "east_asian":    ["Japanese Izakaya", "Noodle Shop", "Dim Sum House"],
    "south_asian":   ["Indian Dhaba"],
    "desert":        ["Mezze Restaurant"],
    "arid_steppe":   ["Mezze Restaurant"],
    "savanna":       ["Mezze Restaurant", "Mezze Restaurant", "BBQ Stall"],
    "alpine_mountain": ["Stew House", "Bakery"],
    "tundra":        ["Stew House", "Bakery"],
    "jungle":        ["BBQ Stall", "Stew House"],
    "tropical":      ["BBQ Stall", "Noodle Shop"],
}

# Building style palettes: (wall_block, roof_block)
BUILDING_PALETTES = [
    (HOUSE_WALL,         HOUSE_ROOF),         # warm wood
    (HOUSE_WALL_STONE,   HOUSE_ROOF_STONE),   # grey stone
    (HOUSE_WALL_BRICK,   HOUSE_ROOF_BRICK),   # red brick
    (HOUSE_WALL_DARK,    HOUSE_ROOF_DARK),    # dark timber
    (PINE_PLANK_WALL,    SLATE_SHINGLE),      # alpine pine
    (GRANITE_ASHLAR,     SLATE_SHINGLE),      # grey ashlar
    (ALPINE_PLASTER,     HOUSE_ROOF_DARK),    # whitewash + dark timber
    (HOUSE_WALL_BRICK,   SLATE_SHINGLE),      # english brick + slate
    (LIMESTONE_BLOCK,    HOUSE_ROOF_STONE),   # pale stone
    (ROUGH_STONE_WALL,   HOUSE_ROOF),         # rough stone + wood
    (COBBLESTONE,        HOUSE_ROOF_DARK),    # cobble + dark timber
    (WHITE_PLASTER_WALL, SPANISH_ROOF_TILE),  # mediterranean white + tile
    (ADOBE_BRICK,        SPANISH_ROOF_TILE),  # spanish adobe
    (AFRICAN_MUD_BRICK,  TERRACOTTA_ROOF_TILE), # west african banco
    (LIMESTONE_BLOCK,    TERRACOTTA_ROOF_TILE), # mediterranean stone + tile
    (HOUSE_WALL_DARK,    SLATE_SHINGLE),      # dark tudor + slate
    (ALPINE_PLASTER,     SLATE_SHINGLE),      # alpine whitewash + slate
]

# ---------------------------------------------------------------------------
# City wall styles
# Each entry: (base_block, top_block, height, has_crenellations).
# Wood/adobe styles set has_crenellations=False and reuse the base block as
# the flat top so the wall reads as a palisade rather than a battlement.
# ---------------------------------------------------------------------------

_DEFAULT_WALL_STYLES = [
    (HOUSE_WALL_DARK,  HOUSE_WALL_DARK,  5, False),  # dark timber palisade
    (PINE_PLANK_WALL,  PINE_PLANK_WALL,  5, False),  # pine plank palisade
    (ROUGH_STONE_WALL, CRENELLATION,     6, True),   # rough stone rampart
    (GRANITE_ASHLAR,   CRENELLATION,     7, True),   # ashlar fortification
    (LIMESTONE_BLOCK,  CRENELLATION,     7, True),   # limestone wall
    (HOUSE_WALL_BRICK, CRENELLATION,     6, True),   # red brick wall
    (CURTAIN_WALL,     CRENELLATION,     8, True),   # heavy curtain wall
    (COBBLESTONE,      CRENELLATION,     6, True),   # cobble wall
]

_DESERT_WALL_STYLES = [
    (ADOBE_BRICK,        ADOBE_BRICK,       5, False),
    (SANDSTONE_BLOCK,    CRENELLATION,      6, True),
    (AFRICAN_MUD_BRICK,  AFRICAN_MUD_BRICK, 5, False),
]

_HIMALAYAN_WALL_STYLES = [
    (WHITEWASHED_WALL, WHITEWASHED_WALL, 5, False),
    (GRANITE_ASHLAR,   CRENELLATION,     6, True),
]

_EAST_ASIAN_WALL_STYLES = [
    (PINE_PLANK_WALL, PINE_PLANK_WALL, 5, False),
    (CRIMSON_BRICK,   CRENELLATION,    6, True),
]

_MEDITERRANEAN_WALL_STYLES = [
    (LIMESTONE_BLOCK,    CRENELLATION,        6, True),
    (WHITE_PLASTER_WALL, WHITE_PLASTER_WALL,  5, False),
]

_SOUTH_ASIAN_WALL_STYLES = [
    (LIMESTONE_BLOCK, CRENELLATION, 6, True),
    (ADOBE_BRICK,     ADOBE_BRICK,  5, False),
]

# Biome → wall pool (falls back to defaults).
_WALL_STYLE_POOLS: dict[str, list] = {}
for _b in _DESERT_BIOMES:        _WALL_STYLE_POOLS[_b] = _DESERT_WALL_STYLES
for _b in _ARABIA_BIOMES:        _WALL_STYLE_POOLS[_b] = _DESERT_WALL_STYLES
for _b in _HIMALAYAN_BIOMES:     _WALL_STYLE_POOLS[_b] = _HIMALAYAN_WALL_STYLES
for _b in _EAST_ASIAN_BIOMES:    _WALL_STYLE_POOLS[_b] = _EAST_ASIAN_WALL_STYLES
for _b in _MEDITERRANEAN_BIOMES: _WALL_STYLE_POOLS[_b] = _MEDITERRANEAN_WALL_STYLES
for _b in _SOUTH_ASIAN_BIOMES:   _WALL_STYLE_POOLS[_b] = _SOUTH_ASIAN_WALL_STYLES

# Per-size chance of having a wall at all. Capitals/garrisons always walled,
# small towns rarely so — leaves room for plenty of "open" cities.
_WALL_CHANCE_BY_SIZE = {
    "small":         0.20,
    "medium":        0.50,
    "large":         0.75,
    "metropolitan":  1.00,
    "military":      1.00,
    "oasis":         0.40,
    "bedouin_camp":  0.00,
}

# Rug colour pool — each house picks one for its floor.
_INTERIOR_RUGS = (
    TEXTILE_RUG_NATURAL, TEXTILE_RUG_GOLDEN, TEXTILE_RUG_CRIMSON,
    TEXTILE_RUG_ROSE,    TEXTILE_RUG_COBALT, TEXTILE_RUG_VIOLET,
    TEXTILE_RUG_VERDANT, TEXTILE_RUG_AMBER,  TEXTILE_RUG_IVORY,
)

# Tapestry colour pool — each house picks one for its back wall.
_INTERIOR_TAPESTRIES = (
    TEXTILE_TAPESTRY_NATURAL, TEXTILE_TAPESTRY_GOLDEN, TEXTILE_TAPESTRY_CRIMSON,
    TEXTILE_TAPESTRY_ROSE,    TEXTILE_TAPESTRY_COBALT, TEXTILE_TAPESTRY_VIOLET,
    TEXTILE_TAPESTRY_VERDANT, TEXTILE_TAPESTRY_AMBER,  TEXTILE_TAPESTRY_IVORY,
)

# Window-box flora pool — drops onto facades just under windows.
_FACADE_FLOWER_BOXES = (FLOWER_BOX, GERANIUM_BOX)

# ---------------------------------------------------------------------------
# Military NPCs
# ---------------------------------------------------------------------------

# Appraisal base prices per weapon type (gold)
_WEAPON_ARMORER_BASE = {"dagger": 20, "sword": 35, "spear": 30, "axe": 40,
                        "mace": 45, "halberd": 55, "glaive": 48,
                        "rapier": 32, "trident": 42, "scythe": 60}
_WEAPON_MATERIAL_MULT = {"iron": 1.0, "gold": 1.6, "steel": 2.0}


class WeaponArmorerNPC(NPC):
    """Buys crafted Weapon objects from the player, paying based on quality + material."""

    def __init__(self, x, y, world, rng, biodome="temperate"):
        super().__init__(x, y, world, "npc_weapon_armorer")
        self.clothing     = _npc_clothing(biodome)
        self.display_name = "Weapon Armorer"

    def appraise(self, weapon, player) -> int:
        from weapons import quality_tier as _qt
        base      = _WEAPON_ARMORER_BASE.get(weapon.weapon_type, 25)
        mat_mult  = _WEAPON_MATERIAL_MULT.get(weapon.material, 1.0)
        q_mult    = 0.5 + weapon.quality * 1.5
        rep_bonus = _rep_buy_bonus(self._town_rep())
        return max(1, round(base * mat_mult * q_mult * rep_bonus))

    def sell_weapon(self, weapon_uid, player) -> int:
        weapon = next((w for w in player.crafted_weapons if w.uid == weapon_uid), None)
        if weapon is None:
            return 0
        value = self.appraise(weapon, player)
        player.crafted_weapons.remove(weapon)
        if player.equipped_weapon_uid == weapon_uid:
            player.equipped_weapon_uid = None
        player.money += value
        return value


# Items the Quartermaster buys from the player
QUARTERMASTER_BUY_TABLE = [
    ("wood_arrow",      5,  2),
    ("bone_arrow",      5,  3),
    ("flint_arrow",     4,  4),
    ("iron_arrow",      4,  6),
    ("barbed_arrow",    3,  9),
    ("broadhead_arrow", 3, 12),
    ("poison_arrow",    3, 11),
    ("gold_arrow",      2, 18),
    ("wood_bow",        1, 12),
    ("recurve_bow",     1, 22),
    ("composite_bow",   1, 36),
    ("longbow",         1, 44),
    ("crossbow",        1, 52),
]


class QuartermasterNPC(NPC):
    """Buys bow and arrow inventory items in bulk from the player."""

    def __init__(self, x, y, world, rng, biodome="temperate"):
        super().__init__(x, y, world, "npc_quartermaster")
        self.clothing     = _npc_clothing(biodome)
        self.display_name = "Quartermaster"
        n            = rng.randint(4, 6)
        self.trades  = rng.sample(QUARTERMASTER_BUY_TABLE, k=n)

    def boosted_gold(self, idx):
        _, _, gold = self.trades[idx]
        return max(1, round(gold * _rep_buy_bonus(self._town_rep())))

    def rep_bonus_pct(self):
        return round((_rep_buy_bonus(self._town_rep()) - 1.0) * 100)

    def can_trade(self, idx, player):
        item_id, give_count, _ = self.trades[idx]
        return player.inventory.get(item_id, 0) >= give_count

    def execute_trade(self, idx, player) -> bool:
        if not self.can_trade(idx, player):
            return False
        item_id, give_count, _ = self.trades[idx]
        player.inventory[item_id] = player.inventory.get(item_id, 0) - give_count
        if player.inventory[item_id] <= 0:
            del player.inventory[item_id]
            for i in range(len(player.hotbar)):
                if player.hotbar[i] == item_id:
                    player.hotbar[i] = None
        player.money += self.boosted_gold(idx)
        return True


_TIER_ORDER = ["Poor", "Standard", "Fine", "Masterwork"]


def _build_garrison_quest(rng, difficulty):
    count     = rng.randint(1, 1 + min(difficulty, 2))
    min_tier  = _TIER_ORDER[min(difficulty, 2)]
    wtype     = rng.choice(["dagger", "sword", "spear", "axe", "mace", "halberd", "glaive",
                            "rapier", "trident", "scythe", None])
    reward    = (35 + difficulty * 20) * count
    return {"count": count, "min_tier": min_tier, "weapon_type": wtype, "reward": reward}


class GarrisonCommanderNPC(NPC):
    """Quest giver: deliver N crafted weapons of minimum quality tier."""

    def __init__(self, x, y, world, rng, difficulty=1, biodome="temperate"):
        super().__init__(x, y, world, "npc_garrison_commander")
        self.clothing     = _npc_clothing(biodome)
        self.display_name = "Garrison Commander"
        self._rng         = rng
        self.difficulty   = difficulty
        self.quests       = [
            _build_garrison_quest(rng, difficulty),
            _build_garrison_quest(rng, difficulty + 1),
        ]

    def matching_weapons(self, player, quest):
        from weapons import quality_tier as _qt
        min_idx = _TIER_ORDER.index(quest["min_tier"])
        return [
            i for i, w in enumerate(player.crafted_weapons)
            if _TIER_ORDER.index(_qt(w.quality)) >= min_idx
            and (quest["weapon_type"] is None or w.weapon_type == quest["weapon_type"])
        ]

    def can_complete(self, player, qi):
        q = self.quests[qi]
        return len(self.matching_weapons(player, q)) >= q["count"]

    def complete_quest(self, player, qi) -> bool:
        quest    = self.quests[qi]
        matching = self.matching_weapons(player, quest)
        if len(matching) < quest["count"]:
            return False
        for idx in sorted(matching[:quest["count"]], reverse=True):
            player.crafted_weapons.pop(idx)
        if player.equipped_weapon_uid not in {w.uid for w in player.crafted_weapons}:
            player.equipped_weapon_uid = None
        player.money += round(quest["reward"] * getattr(player, "blessing_mult", 1.0))
        self.quests[qi] = _build_garrison_quest(self._rng, self.difficulty + qi)
        return True


# Frontier biomes that may produce military towns
_FRONTIER_BIOMES = {"steppe", "wasteland", "rocky_mountain", "canyon", "arid_steppe"}

# Building slot format: (offset_from_cx, (min_w, max_w), (min_h, max_h), variants)
# variants is a list sampled uniformly; repeat entries to weight them.
# Use (offset, None, None, None) for an outdoor NPC slot with no building.
# Variants: "house", "two_story", "tower", "longhouse", "ruin", "restaurant", "shrine"
#
# npc_types entries map positionally to buildings. An entry may be:
#   - a string ("scholar")           — always that NPC
#   - a list (["scholar", "villager"]) — sampled per-city; repeat to weight
#   - "villager" / "child" / "guard"  — ambient resident (no shop/quest)
#   - "none" or None                  — leave the slot empty
CITY_CONFIGS = {
    "small": {
        "half_w": 16,
        "buildings": [
            (-15, (4, 6), (3, 5), ["house", "house", "two_story", "three_story", "tower",
                                    "ruin", "market_stall", "well", "inn", "smithy", "vignette"]),
            ( -3, (4, 5), (3, 4), ["restaurant", "restaurant", "apothecary"]),
            (  5, (4, 6), (3, 5), ["house", "house", "two_story", "three_story", "longhouse",
                                    "ruin", "market_stall", "well", "inn", "vignette"]),
        ],
        "npc_types": ["quest_rock", "restaurant_npc", "innkeeper"],
        # (center_offset, half_w) — small garden plots tucked between buildings.
        "gardens": [(-9, 2), (10, 2)],
        "squares": [],
        # Growth slots per tier: (offset, w_range, h_range, variants)
        "growth_slots_tier1": [( 12, (4, 5), (3, 4), ["two_story", "house"]),
                               (-12, (4, 5), (3, 4), ["house", "two_story"])],
        "growth_slots_tier2": [( 14, (5, 6), (4, 5), ["tower"]),
                               (-14, (4, 5), (3, 4), ["longhouse"])],
        "growth_slots_tier3": [( 16, (6, 7), (5, 6), ["tower"]),
                               (-16, (5, 6), (4, 5), ["two_story"])],
        # (center_offset, half_w) — farm fields outside the main footprint
        "farms": [(-24, 6), (24, 6)],
        # (offset, npc_type) — ambient residents at street level. npc_type may
        # be a list (sampled) or include "none" so head-count varies.
        "ambient_npcs": [(-6, ["villager", "villager", "none"]),
                         (8,  ["child", "child", "none"]),
                         (-12, ["villager", "elder", "none"]),
                         (12, ["child", "villager", "none"]),
                         (3,  ["elder", "none", "none"]),
                         (-3, ["pilgrim", "none", "none", "none"])],
    },
    "medium": {
        "half_w": 26,
        "buildings": [
            (-25, (4, 6), (3, 5), ["house", "two_story", "three_story", "tower", "ruin",
                                    "longhouse", "pavilion", "inn"]),
            (-17, (4, 6), (3, 4), ["smithy", "smithy", "smithy", "house", "two_story",
                                    "longhouse", "ruin", "market_stall", "barn"]),
            ( -8, (4, 5), (3, 4), ["inn", "inn", "restaurant", "apothecary"]),
            ( -2, None,   None,   None),    # outdoor NPC — stands in the town square
            (  5, (4, 6), (3, 4), ["house", "house", "two_story", "three_story", "ruin",
                                    "tower", "market_stall", "well", "vignette"]),
            ( 13, (4, 6), (3, 5), ["library", "library", "house", "two_story", "tower",
                                    "longhouse", "ruin", "pavilion", "apothecary", "coffee_shop"]),
            ( 19, (6, 7), (5, 7), ["shrine"]),
        ],
        "npc_types": ["quest_rock", "blacksmith", "innkeeper", "merchant",
                      ["quest_gem", "quest_gem", "villager"],
                      ["scholar", "villager", "villager", "coffee_merchant", "beer_merchant"],
                      "shrine_npc"],
        "gardens": [(-21, 2), (-12, 2), (16, 2)],
        # (center_offset, half_w) — paved plaza with a centre sculpture.
        "squares": [(0, 4)],
        "growth_slots_tier1": [( 22, (4, 6), (3, 4), ["house", "two_story"]),
                               (-22, (4, 6), (3, 4), ["house", "longhouse"])],
        "growth_slots_tier2": [( 24, (5, 7), (4, 5), ["tower", "two_story", "three_story"]),
                               (-24, (5, 6), (4, 5), ["tower", "two_story", "three_story"])],
        "growth_slots_tier3": [( 26, (6, 8), (5, 6), ["tower", "three_story"]),
                               (-26, (5, 7), (4, 6), ["longhouse", "three_story"])],
        "farms": [(-36, 7), (36, 7)],
        "ambient_npcs": [(-12, ["villager", "villager", "elder", "none"]),
                         (-6,  ["child", "child", "none"]),
                         (9,   ["villager", "villager", "drunkard", "musician"]),
                         (15,  ["child", "child", "villager", "none"]),
                         (-18, ["guard", "none"]),
                         (20,  ["guard", "guard", "none"]),
                         (-22, ["villager", "pilgrim", "none"]),
                         (22,  ["villager", "child", "none", "none"]),
                         (3,   ["elder", "pilgrim", "none", "none"]),
                         (-15, ["beggar", "none", "none", "none"]),
                         (6,   ["drunkard", "none", "none"])],
    },
    "large": {
        "half_w": 36,
        "buildings": [
            (-35, (5, 7), (4, 5), ["house", "two_story", "three_story", "tower", "longhouse",
                                    "pavilion", "inn", "inn", "hospital"]),
            (-27, (4, 6), (3, 5), ["smithy", "smithy", "smithy", "house", "ruin", "tower",
                                    "two_story", "market_stall", "wine_shop"]),
            (-19, (4, 5), (3, 4), ["house", "house", "two_story", "three_story", "ruin",
                                    "longhouse", "pavilion", "apothecary", "coffee_shop"]),
            ( -8, None,   None,   None),    # outdoor NPC — left square
            ( -2, (4, 5), (3, 4), ["house", "two_story", "three_story", "ruin", "tower",
                                    "longhouse", "market_stall"]),
            (  5, (4, 5), (3, 4), ["inn", "inn", "inn", "restaurant"]),
            ( 11, None,   None,   None),    # outdoor NPC — right square
            ( 18, (4, 6), (3, 5), ["library", "library", "house", "tower", "ruin",
                                    "two_story", "market_stall", "apothecary", "barn", "vignette"]),
            ( 26, (7, 9), (5, 7), ["shrine"]),
        ],
        "npc_types": [["quest_rock", "doctor"], "blacksmith",
                      ["quest_wildflower", "quest_wildflower", "villager", "wine_merchant"],
                      "merchant",
                      ["quest_gem", "quest_gem", "villager", "coffee_merchant"],
                      ["innkeeper", "innkeeper", "tavern"],
                      ["trade", "merchant", "villager", "beer_merchant"],
                      ["scholar", "scholar", "villager"],
                      "shrine_npc",
                      ["jewelry_merchant", "villager", "villager"]],
        "gardens": [(-31, 2), (-23, 2), (22, 2)],
        "squares": [(-10, 4), (13, 4)],
        "growth_slots_tier1": [( 32, (4, 6), (3, 4), ["house", "two_story"]),
                               (-32, (4, 6), (3, 4), ["house", "longhouse"])],
        "growth_slots_tier2": [( 34, (5, 7), (4, 5), ["tower", "two_story", "three_story"]),
                               (-34, (5, 7), (4, 5), ["tower", "longhouse", "three_story"])],
        "growth_slots_tier3": [( 36, (6, 8), (5, 6), ["tower", "three_story"]),
                               (-36, (5, 7), (4, 6), ["tower", "three_story"])],
        "farms": [(-48, 8), (48, 8)],
        "ambient_npcs": [(-30, ["villager", "villager", "elder", "none"]),
                         (-14, ["child", "child", "none"]),
                         (0,   ["villager", "noble", "villager", "none", "town_crier"]),
                         (8,   ["child", "child", "villager", "none"]),
                         (22,  ["villager", "drunkard", "villager", "musician"]),
                         (28,  ["guard", "guard", "none"]),
                         (-22, ["villager", "pilgrim", "none"]),
                         (-36, ["guard", "none", "none"]),
                         (15,  ["child", "elder", "none"]),
                         (35,  ["villager", "child", "none", "none"]),
                         (-3,  ["beggar", "none", "none", "none"]),
                         (3,   ["pilgrim", "elder", "none", "none"]),
                         (-25, ["noble", "none", "none"]),
                         (12,  ["drunkard", "none", "none"])],
    },
    # Tier-3 metropolis (capital after max growth)
    "metropolitan": {
        "half_w": 55,
        "buildings": [
            (-50, (6, 8), (5, 7), ["three_story", "tower", "library", "barn", "hospital"]),
            (-42, (5, 7), (4, 6), ["house", "two_story", "inn", "barn", "wine_shop"]),
            (-34, (4, 6), (3, 5), ["smithy", "smithy", "apothecary", "barn", "coffee_shop"]),
            (-26, (5, 7), (4, 6), ["library", "library", "house"]),
            (-18, None,   None,   None),    # Outdoor scholar
            (-12, (7, 9), (5, 8), ["shrine"]),
            ( -2, (4, 6), (3, 5), ["restaurant", "restaurant", "inn", "barn"]),
            (  6, None,   None,   None),    # Outdoor merchant
            ( 14, (5, 7), (4, 6), ["house", "two_story", "three_story", "jewelry_store"]),
            ( 22, (6, 8), (5, 7), ["tower", "library", "longhouse", "barn"]),
            ( 30, (4, 6), (3, 5), ["smithy", "apothecary", "jewelry_store", "house", "vignette"]),
            ( 38, None,   None,   None),    # Outdoor noble
            ( 46, (7, 10), (6, 9), ["shrine", "shrine"]),
        ],
        "npc_types": [["scholar", "doctor"], ["innkeeper", "tavern"], "blacksmith", "scholar",
                      "scholar", "shrine_npc", "restaurant_npc", ["merchant", "beer_merchant"],
                      "villager", ["scholar", "library_npc", "villager", "wine_merchant"], "jewelry_merchant",
                      "noble", "shrine_npc"],
        "gardens": [(-46, 3), (-22, 2), (10, 2), (34, 3)],
        "squares": [(-30, 5), (0, 6), (26, 5)],
        "growth_slots_tier1": [( 50, (4, 6), (3, 4), ["house", "two_story"]),
                               (-50, (4, 6), (3, 4), ["house", "longhouse"])],
        "growth_slots_tier2": [( 52, (5, 7), (4, 5), ["tower", "two_story", "three_story"]),
                               (-52, (5, 7), (4, 5), ["tower", "longhouse", "three_story"])],
        "growth_slots_tier3": [( 54, (6, 8), (5, 6), ["tower", "three_story"]),
                               (-54, (5, 7), (4, 6), ["tower", "three_story"])],
        "farms": [(-70, 10), (70, 10)],
        "ambient_npcs": [(-45, ["villager", "noble", "guard", "town_crier"]),
                         (-25, ["child", "villager", "none", "musician"]),
                         (0,   ["noble", "noble", "guard", "none", "town_crier"]),
                         (15,  ["child", "child", "none", "musician"]),
                         (35,  ["villager", "drunkard", "beggar", "musician"]),
                         (45,  ["guard", "guard", "guard"]),
                         (-10, ["scholar", "villager", "none"]),
                         (25,  ["noble", "none", "none"]),
                         (-35, ["beggar", "none", "none"]),
                         (10,  ["pilgrim", "elder", "none"])],
    },
    # Military garrison — spawns biome-driven in frontier biomes (steppe/wasteland/etc.)
    "military": {
        "half_w": 30,
        "buildings": [
            (-29, (6, 8), (5, 6), ["smithy"]),
            (-20, (5, 6), (4, 5), ["smithy", "two_story"]),
            (-11, (4, 5), (3, 4), ["market_stall", "house"]),
            ( -3, None,   None,   None),
            (  4, (4, 5), (3, 4), ["inn", "restaurant"]),
            ( 10, None,   None,   None),
            ( 17, (5, 7), (4, 6), ["shrine", "tower"]),
        ],
        "npc_types": ["weapon_armorer", "blacksmith", "quest_rock",
                      "garrison_commander", "innkeeper", "quartermaster", "shrine_npc"],
        "gardens": [],
        "squares": [(-5, 4), (8, 4)],
        "growth_slots_tier1": [( 24, (4, 5), (3, 4), ["tower", "smithy"])],
        "growth_slots_tier2": [(-26, (4, 6), (3, 5), ["smithy", "tower"])],
        "growth_slots_tier3": [( 27, (5, 7), (4, 6), ["tower"])],
        "farms":   [(-40, 6), (40, 6)],
        "ambient_npcs": [(-25, "guard"),
                         (-7,  ["guard", "guard", "drunkard", "none"]),
                         (0,   "guard"),
                         (7,   ["guard", "none"]),
                         (20,  "guard"),
                         (-15, ["guard", "drunkard", "none"]),
                         (15,  ["guard", "elder", "none"]),
                         (12,  ["drunkard", "none", "none"])],
    },
}

CITY_CONFIGS["oasis"] = {
    "half_w": 22,
    "buildings": [
        (-21, (5, 7), (3, 4), ["tent", "tent", "market_stall"]),
        (-13, (4, 5), (3, 4), ["tent", "market_stall"]),
        ( -4, (5, 6), (4, 5), ["caravanserai"]),
        (  5, None,   None,   None),          # outdoor merchant in the well square
        ( 11, (4, 5), (3, 4), ["tent", "tent", "well"]),
        ( 16, (6, 8), (5, 6), ["shrine"]),
    ],
    "npc_types": ["quest_rock", "merchant", "innkeeper",
                  "trade", "quest_gem", "shrine_npc"],
    "gardens":  [(-17, 2), (8, 2)],
    "squares":  [(3, 3)],
    "growth_slots_tier1": [( 20, (4, 5), (3, 4), ["tent", "market_stall"]),
                            (-19, (4, 5), (3, 4), ["tent"])],
    "growth_slots_tier2": [( 22, (5, 6), (4, 5), ["caravanserai"]),
                            (-21, (5, 7), (4, 5), ["tent", "tent"])],
    "growth_slots_tier3": [( 24, (6, 7), (5, 6), ["caravanserai"]),
                            (-23, (4, 6), (3, 4), ["tent", "market_stall"])],
    "farms":    [(-32, 5), (32, 5)],
    "ambient_npcs": [(-16, ["villager", "villager", "elder", "none"]),
                     (-9,  ["child", "child", "none"]),
                     (7,   ["villager", "pilgrim", "villager"]),
                     (14,  ["child", "child", "none"]),
                     (-20, ["guard", "none"]),
                     (19,  ["guard", "guard", "none"]),
                     (0,   ["villager", "child", "pilgrim", "none"]),
                     (-12, ["villager", "elder", "none"]),
                     (3,   ["pilgrim", "none", "none"]),
                     (-3,  ["beggar", "none", "none", "none"])],
}

CITY_CONFIGS["bedouin_camp"] = {
    "half_w": 13,
    "buildings": [
        (-12, (5, 7), (3, 4), ["tent", "tent"]),
        ( -3, (4, 5), (3, 4), ["market_stall", "tent"]),
        (  5, (5, 7), (3, 4), ["tent", "tent"]),
    ],
    "npc_types": ["quest_rock", "trade", "restaurant_npc"],
    "gardens":  [(-7, 2), (9, 2)],
    "squares":  [],
    "growth_slots_tier1": [( 11, (4, 5), (3, 4), ["tent"]),
                            (-11, (4, 5), (3, 4), ["tent"])],
    "growth_slots_tier2": [( 13, (5, 7), (4, 5), ["caravanserai"]),
                            (-13, (4, 5), (3, 4), ["market_stall"])],
    "growth_slots_tier3": [( 15, (5, 7), (4, 5), ["tent", "tent"]),
                            (-15, (5, 6), (4, 5), ["tent"])],
    "farms":    [(-20, 4), (20, 4)],
    "ambient_npcs": [(-8,  ["villager", "villager", "elder", "none"]),
                     (2,   ["child", "none"]),
                     (10,  ["villager", "pilgrim", "villager"]),
                     (-14, ["villager", "elder", "none"]),
                     (14,  ["child", "child", "none"]),
                     (6,   ["child", "none", "none"]),
                     (-2,  ["elder", "pilgrim", "none", "none"])],
}

_SIZE_BY_DIFFICULTY = {
    0: ["small", "small", "medium"],
    1: ["small", "medium", "large"],
    2: ["medium", "large", "metropolitan"],
}

# Biome overrides for city layout — bypasses difficulty-based selection.
_SIZE_BY_BIOME = {
    "savanna": ["bedouin_camp", "oasis", "oasis"],
}

_PLANT_BLOCKS = ALL_LOGS | ALL_LEAVES | BUSH_BLOCKS | {SAPLING}


# ---------------------------------------------------------------------------
# City gardens
# ---------------------------------------------------------------------------

# Each theme is a sequence of decorative garden blocks placed along the
# sy-1 row in front of buildings. Themes are chosen per-garden based on
# biome and a random pick.
GARDEN_THEMES = {
    "flower_meadow": (LAVENDER_BED, ROSE_BED, TULIP_BED, MARIGOLD_BED,
                      IRIS_BED, POPPY_BED, DAHLIA_BED, SUNFLOWER_BED),
    "cottage":       (COTTAGE_GARDEN_BED, BEE_SKEP, FOXGLOVE_PATCH,
                      ALLIUM_PATCH, COTTAGE_GARDEN_BED, FLOWERING_SHRUB,
                      PEONY_BUSH, HYDRANGEA_BUSH),
    "formal":        (BOXWOOD_BALL, TOPIARY_RABBIT, BOXWOOD_BALL,
                      TOPIARY_PEACOCK, BOXWOOD_BALL, TOPIARY_BEAR,
                      BOXWOOD_BALL, TOPIARY_SWAN),
    "topiary_zoo":   (TOPIARY_FOX, TOPIARY_OWL, TOPIARY_HEDGEHOG,
                      TOPIARY_SNAIL, TOPIARY_MUSHROOM, TOPIARY_ARCH,
                      TOPIARY_RABBIT, TOPIARY_PEACOCK),
    "fountain_plaza":(HOLLY_SHRUB, FLOWERING_SHRUB, BUBBLE_FOUNTAIN,
                      FLOWERING_SHRUB, HOLLY_SHRUB, RHODODENDRON_BUSH,
                      SHELL_FOUNTAIN, BOXWOOD_BALL),
    "kitchen":       (COMPOST_HEAP, COLD_FRAME, POTTING_TABLE,
                      RAIN_BARREL, BEE_SKEP, GARDEN_WHEELBARROW,
                      STONE_TROUGH_PLANTER, BIRD_TABLE),
    "ornament":      (GARDEN_GNOME, STONE_FROG, STONE_HEDGEHOG,
                      GARDEN_TOAD_HOUSE, BIRD_TABLE, GARDEN_DOVECOTE,
                      GARDEN_OBELISK_METAL, GARDEN_CLOCK),
    "fern_grove":    (FERN_CLUMP, BAMBOO_CLUMP, ORNAMENTAL_GRASS,
                      FERN_CLUMP, BAMBOO_CLUMP, MOSS_PATCH,
                      LILY_PAD_POND, FERN_CLUMP),
    "english_park":  (STANDARD_ROSE, BOXWOOD_BALL, AGAPANTHUS_PATCH,
                      ASTILBE_PATCH, BLEEDING_HEART_PATCH, STANDARD_ROSE,
                      KNOT_GARDEN, RHODODENDRON_BUSH),
    "wisteria_walk": (WISTERIA_PILLAR, SWEET_PEA_TRELLIS, TRELLIS_ARCH,
                      WISTERIA_PILLAR, FLOWERING_SHRUB, SWEET_PEA_TRELLIS,
                      WISTERIA_PILLAR, GARDEN_SWING),
    "alpine_yard":   (HAY_BALE, FIREWOOD_STACK, RAIN_BARREL,
                      COMPOST_HEAP, FLOWER_BOX, FERN_CLUMP,
                      WICKER_FENCE, GARDEN_WHEELBARROW),
    "monastic":      (HOLLY_SHRUB, BOXWOOD_BALL, KNOT_GARDEN,
                      LAVENDER_BED, ROSE_BED, BOXWOOD_BALL,
                      MARIGOLD_BED, BOXWOOD_BALL),
    "pondside":      (LILY_PAD_POND, KOI_POOL, FERN_CLUMP,
                      LILY_PAD_POND, BAMBOO_CLUMP, FERN_CLUMP,
                      KOI_POOL, MOSS_PATCH),
    "japanese_garden": (PINE_TOPIARY_JP, KOI_POOL, SHISHI_ODOSHI,
                        JAPANESE_MAPLE, BAMBOO_CLUMP, MOSS_PATCH,
                        RED_ARCH_BRIDGE, FERN_CLUMP),
    "mediterranean_patio": (STANDARD_ROSE, ROSE_BED, LAVENDER_BED,
                            AGAPANTHUS_PATCH, ORNAMENTAL_GRASS,
                            PORTUGUESE_BENCH, BUBBLE_FOUNTAIN, FLOWERING_SHRUB),
    "south_asian_garden": (MARIGOLD_BED, SUNFLOWER_BED, KOI_POOL,
                           ORNAMENTAL_GRASS, FERN_CLUMP, LILY_PAD_POND,
                           BAMBOO_CLUMP, FLOWERING_SHRUB),
}

# Lawn ground covers used to fill gaps between accent blocks.
_LAWN_BLOCKS = (CHAMOMILE_LAWN, CLOVER_LAWN, MOSS_PATCH, BARK_MULCH)

# Biome-flavoured garden theme bias. Falls back to "any" if not listed.
_GARDEN_THEMES_BY_BIOME = {
    "temperate":      ["flower_meadow", "cottage", "formal", "ornament",
                       "english_park", "wisteria_walk"],
    "boreal":         ["fern_grove", "cottage", "ornament", "alpine_yard"],
    "birch_forest":   ["cottage", "flower_meadow", "fern_grove", "english_park"],
    "redwood":        ["fern_grove", "ornament", "formal", "pondside"],
    "tropical":       ["fern_grove", "topiary_zoo", "fountain_plaza", "wisteria_walk"],
    "jungle":         ["fern_grove", "topiary_zoo", "pondside"],
    "savanna":        ["topiary_zoo", "ornament", "formal"],
    "wetland":        ["fern_grove", "cottage", "pondside"],
    "tundra":         ["formal", "ornament", "alpine_yard"],
    "steppe":         ["formal", "ornament", "cottage", "monastic"],
    "alpine_mountain":["fountain_plaza", "formal", "alpine_yard", "monastic"],
    "rocky_mountain": ["formal", "ornament", "alpine_yard"],
    "canyon":         ["ornament", "formal", "monastic"],
    "desert":         ["fountain_plaza", "ornament", "monastic"],
    "arid_steppe":    ["fountain_plaza", "ornament", "monastic"],
    "mediterranean":  ["mediterranean_patio", "flower_meadow", "formal",
                       "wisteria_walk", "cottage"],
    "east_asian":     ["japanese_garden", "pondside", "fern_grove",
                       "monastic"],
    "south_asian":    ["south_asian_garden", "flower_meadow", "fountain_plaza",
                       "topiary_zoo"],
}

_FOUNTAIN_BLOCKS = (BUBBLE_FOUNTAIN, SHELL_FOUNTAIN, MILLSTONE_FOUNTAIN,
                    CHERUB_FOUNTAIN, MOSAIC_FOUNTAIN, LION_HEAD_FOUNTAIN)

# ---------------------------------------------------------------------------
# Clothing palettes — keyed by cultural style, used by ambient NPC renderer
# ---------------------------------------------------------------------------
# Keys: body, leg, skin, trim (belt/collar), hat (farmer), armor/plate (guard)

_CLOTHING_PALETTES = {
    "temperate": {
        "body": (90, 115, 75), "leg": (90, 70, 45), "skin": (255, 215, 160),
        "trim": (110, 75, 35), "hat": (200, 175, 80),
        "armor": (55, 55, 75), "plate": (155, 160, 165),
    },
    "desert": {
        # Light flowing robes, warm skin, deep blue trim
        "body": (238, 232, 210), "leg": (230, 225, 200), "skin": (205, 160, 105),
        "trim": (50, 90, 160), "hat": (245, 238, 215),
        "armor": (200, 175, 100), "plate": (230, 200, 130),
    },
    "alpine": {
        # Heavy wool in deep burgundy, fair skin
        "body": (105, 40, 40), "leg": (75, 60, 50), "skin": (245, 205, 160),
        "trim": (165, 120, 70), "hat": (130, 60, 40),
        "armor": (50, 45, 55), "plate": (130, 135, 145),
    },
    "mediterranean": {
        # Terra cotta and ochre with olive skin
        "body": (185, 90, 50), "leg": (215, 200, 155), "skin": (220, 180, 125),
        "trim": (30, 25, 20), "hat": (215, 185, 100),
        "armor": (80, 50, 30), "plate": (195, 165, 100),
    },
    "east_asian": {
        # Crimson and ink-black hanfu with gold trim, warm-fair skin
        "body": (170, 40, 40), "leg": (30, 25, 30), "skin": (245, 205, 165),
        "trim": (210, 170, 50), "hat": (25, 20, 25),
        "armor": (40, 35, 50), "plate": (180, 145, 55),
    },
    "south_asian": {
        # Saffron and coral with warm brown skin
        "body": (215, 115, 35), "leg": (225, 215, 185), "skin": (180, 135, 85),
        "trim": (200, 175, 40), "hat": (235, 190, 80),
        "armor": (140, 85, 30), "plate": (210, 175, 80),
    },
    "jungle": {
        # Deep greens and earthy cotton, dark skin
        "body": (65, 145, 85), "leg": (100, 75, 45), "skin": (165, 115, 70),
        "trim": (190, 155, 50), "hat": (170, 140, 50),
        "armor": (45, 75, 45), "plate": (90, 130, 80),
    },
    "boreal": {
        # Dark forest green and navy, pale skin
        "body": (50, 80, 65), "leg": (55, 55, 70), "skin": (250, 215, 175),
        "trim": (100, 80, 55), "hat": (70, 100, 70),
        "armor": (45, 50, 60), "plate": (120, 130, 140),
    },
    "steppe": {
        # Rust orange and deep gold, medium warm skin
        "body": (175, 95, 40), "leg": (140, 100, 50), "skin": (200, 158, 100),
        "trim": (130, 35, 30), "hat": (195, 150, 55),
        "armor": (100, 65, 30), "plate": (175, 140, 70),
    },
    "coastal": {
        # Faded blues and sandy cream, tanned skin
        "body": (90, 130, 165), "leg": (210, 195, 160), "skin": (215, 175, 120),
        "trim": (50, 80, 110), "hat": (200, 180, 120),
        "armor": (55, 75, 95), "plate": (140, 160, 180),
    },
}
_CLOTHING_DEFAULT = _CLOTHING_PALETTES["temperate"]

# Maps biodome string → clothing style key
_CLOTHING_STYLE_BY_BIODOME = {
    "temperate": "temperate", "birch_forest": "temperate", "redwood": "temperate",
    "boreal": "boreal",
    "alpine_mountain": "alpine", "tundra": "alpine", "rocky_mountain": "alpine",
    "desert": "desert", "savanna": "desert", "arid_steppe": "desert",
    "canyon": "east_asian",
    "rolling_hills": "mediterranean", "steep_hills": "desert",
    "mediterranean": "mediterranean",
    "east_asian": "east_asian",
    "south_asian": "south_asian",
    "jungle": "jungle", "tropical": "jungle",
    "wetland": "boreal", "swamp": "boreal",
    "steppe": "steppe", "wasteland": "steppe",
    "beach": "coastal",
}

def _npc_clothing(biodome):
    style = _CLOTHING_STYLE_BY_BIODOME.get(biodome, "temperate")
    return _CLOTHING_PALETTES.get(style, _CLOTHING_DEFAULT)



# ---------------------------------------------------------------------------
# Farm data
# ---------------------------------------------------------------------------

# Maps biodome strings to a simplified group key for farm crop selection.
_BIOME_GROUP_SIMPLE = {
    "temperate": "temperate", "boreal": "boreal", "birch_forest": "temperate",
    "redwood": "temperate",   "jungle": "jungle",  "tropical": "jungle",
    "wetland": "wetland",     "swamp": "wetland",  "desert": "desert",
    "arid_steppe": "desert",  "savanna": "desert", "alpine_mountain": "alpine",
    "tundra": "alpine",       "rocky_mountain": "alpine", "steppe": "steppe",
    "wasteland": "steppe",    "canyon": "steppe",  "beach": "coastal",
    "mediterranean": "temperate", "east_asian": "temperate", "south_asian": "jungle",
}

# Crops that appear in city farm fields, by biome group.
FARM_CROPS_BY_BIOME = {
    "temperate": [WHEAT_CROP_YOUNG, CARROT_CROP_YOUNG, POTATO_CROP_YOUNG,
                  CABBAGE_CROP_YOUNG, LEEK_CROP_YOUNG, BEET_CROP_YOUNG],
    "boreal":    [WHEAT_CROP_YOUNG, POTATO_CROP_YOUNG, TURNIP_CROP_YOUNG,
                  BEET_CROP_YOUNG, LEEK_CROP_YOUNG],
    "desert":    [ONION_CROP_YOUNG, GARLIC_CROP_YOUNG, EGGPLANT_CROP_YOUNG,
                  CHILI_CROP_YOUNG],
    "alpine":    [TURNIP_CROP_YOUNG, POTATO_CROP_YOUNG, BEET_CROP_YOUNG,
                  WHEAT_CROP_YOUNG],
    "jungle":    [RICE_CROP_YOUNG, BOK_CHOY_CROP_YOUNG, CHILI_CROP_YOUNG,
                  SWEET_POTATO_CROP_YOUNG],
    "wetland":   [RICE_CROP_YOUNG, LEEK_CROP_YOUNG, CELERY_CROP_YOUNG],
    "steppe":    [WHEAT_CROP_YOUNG, ONION_CROP_YOUNG, POTATO_CROP_YOUNG],
    "coastal":   [CABBAGE_CROP_YOUNG, ONION_CROP_YOUNG, LEEK_CROP_YOUNG],
}
_FARM_CROPS_DEFAULT = [WHEAT_CROP_YOUNG, CARROT_CROP_YOUNG, POTATO_CROP_YOUNG]

# Maps young crop block → its mature variant for visual variety in pre-grown fields.
_YOUNG_TO_MATURE = {
    WHEAT_CROP_YOUNG:        WHEAT_CROP_MATURE,
    CARROT_CROP_YOUNG:       CARROT_CROP_MATURE,
    POTATO_CROP_YOUNG:       POTATO_CROP_MATURE,
    CABBAGE_CROP_YOUNG:      CABBAGE_CROP_MATURE,
    LEEK_CROP_YOUNG:         LEEK_CROP_MATURE,
    BEET_CROP_YOUNG:         BEET_CROP_MATURE,
    TURNIP_CROP_YOUNG:       TURNIP_CROP_MATURE,
    ONION_CROP_YOUNG:        ONION_CROP_MATURE,
    GARLIC_CROP_YOUNG:       GARLIC_CROP_MATURE,
    EGGPLANT_CROP_YOUNG:     EGGPLANT_CROP_MATURE,
    CHILI_CROP_YOUNG:        CHILI_CROP_MATURE,
    RICE_CROP_YOUNG:         RICE_CROP_MATURE,
    BOK_CHOY_CROP_YOUNG:     BOK_CHOY_CROP_MATURE,
    SWEET_POTATO_CROP_YOUNG: SWEET_POTATO_CROP_MATURE,
    CELERY_CROP_YOUNG:       CELERY_CROP_MATURE,
}


def _place_garden_plot(world, rng, center_bx, sy, biodome, half_w=3):
    """Paint a small garden along the row above the city floor.

    All accent blocks are placed as background blocks so the player can
    still walk through the city street — the garden reads visually but
    never obstructs movement.
    """
    pool = _GARDEN_THEMES_BY_BIOME.get(biodome, list(GARDEN_THEMES.keys()))
    theme_name = rng.choice(pool)
    blocks = GARDEN_THEMES[theme_name]

    plot_y = sy - 1
    fence_y = sy - 2
    if not (0 <= plot_y < world.height):
        return

    for wx in range(center_bx - half_w, center_bx + half_w + 1):
        if world.get_block(wx, plot_y) != AIR:
            continue
        # 65% accent block from the theme, 35% lawn cover
        if rng.random() < 0.65:
            world.set_bg_block(wx, plot_y, rng.choice(blocks))
        else:
            world.set_bg_block(wx, plot_y, rng.choice(_LAWN_BLOCKS))

    # Fountain centerpiece on plaza-style themes.
    if theme_name == "fountain_plaza" and 0 <= plot_y < world.height:
        world.set_bg_block(center_bx, plot_y, rng.choice(_FOUNTAIN_BLOCKS))

    # A few low wicker-fence segments behind the plot for visual framing.
    if 0 <= fence_y < world.height:
        for wx in (center_bx - half_w, center_bx + half_w):
            if world.get_block(wx, fence_y) == AIR:
                world.set_bg_block(wx, fence_y, WICKER_FENCE)


def _place_farm_plot(world, rng, center_bx, biodome, half_w=7):
    """Place a strip of tilled soil with crops outside the city footprint.

    Each column uses its own terrain surface so the farm follows the landscape
    rather than floating when the ground outside the city is uneven.

    A well is placed as a background block at the centre column.
    Wicker fence posts frame the outer edges.
    Crops are chosen by biome group so farm contents match the landscape.
    """
    biome_group = _BIOME_GROUP_SIMPLE.get(biodome, "temperate")
    crops = FARM_CROPS_BY_BIOME.get(biome_group, _FARM_CROPS_DEFAULT)

    for bx in range(center_bx - half_w, center_bx + half_w + 1):
        col_sy = world.surface_y_at(bx)
        soil_y = col_sy - 1
        crop_y = col_sy - 2
        if not (0 <= soil_y < world.height):
            continue
        if world.get_block(bx, soil_y) != AIR:
            continue
        world.set_block(bx, soil_y, TILLED_SOIL)
        if 0 <= crop_y < world.height and world.get_block(bx, crop_y) == AIR:
            chosen = rng.choice(crops)
            if rng.random() < 0.5:
                chosen = _YOUNG_TO_MATURE.get(chosen, chosen)
            world.set_block(bx, crop_y, chosen)

    # Central well as a background landmark
    well_y = world.surface_y_at(center_bx) - 1
    if 0 <= well_y < world.height:
        world.set_bg_block(center_bx, well_y, WELL_BLOCK)

    # Fence corner posts
    for bx in (center_bx - half_w, center_bx + half_w):
        fence_y = world.surface_y_at(bx) - 3
        if 0 <= fence_y < world.height and world.get_block(bx, fence_y) == AIR:
            world.set_bg_block(bx, fence_y, WICKER_FENCE)


# ---------------------------------------------------------------------------
# Town squares
# ---------------------------------------------------------------------------

# Each theme is:
#   "monument" — list of bg blocks placed bottom-up at the centre column
#                (e.g. plinth on row sy-1, statue on row sy-2)
#   "flank"    — bg block flanking the monument, 2 rows out on each side
#   "edge"     — bg block at the outer edges of the plaza
#   "paving"   — solid block that replaces the city stone floor across the plaza
SQUARE_THEMES = {
    "civic_marble": {
        "monument": [MARBLE_PLINTH, MARBLE_STATUE],
        "flank":    GREEK_STONE_BENCH,
        "edge":     TRIPOD_BRAZIER,
        "paving":   INLAID_MARBLE,
    },
    "obelisk_court": {
        "monument": [MARBLE_PLINTH, GARDEN_OBELISK],
        "flank":    GARDEN_LANTERN,
        "edge":     GARDEN_COLUMN,
        "paving":   HERRINGBONE_GARDEN,
    },
    "victory_plaza": {
        "monument": [MARBLE_PLINTH, VICTORY_STELE],
        "flank":    LAUREL_WREATH_MOUNT,
        "edge":     CARVED_BENCH,
        "paving":   GARDEN_STAR_TILE,
    },
    "scholar_court": {
        "monument": [MARBLE_PLINTH, HERMES_STELE],
        "flank":    STONE_BASIN,
        "edge":     DORIC_CAPITAL,
        "paving":   INLAID_MARBLE,
    },
    "fountain_square": {
        "monument": [MOSAIC_FOUNTAIN],
        "flank":    GREEK_STONE_BENCH,
        "edge":     BRAZIER,
        "paving":   HERRINGBONE_GARDEN,
    },
    "cherub_court": {
        "monument": [CHERUB_FOUNTAIN],
        "flank":    CARVED_BENCH,
        "edge":     GARDEN_LANTERN,
        "paving":   MARBLE_MEDALLION_REN,
    },
    "birdbath_garden": {
        "monument": [MARBLE_BIRDBATH],
        "flank":    FERN_CLUMP,
        "edge":     STONE_TROUGH_PLANTER,
        "paving":   CHAMOMILE_LAWN,
    },
    "lion_plaza": {
        "monument": [LION_HEAD_FOUNTAIN],
        "flank":    GREEK_STONE_BENCH,
        "edge":     STAR_LAMP,
        "paving":   GARDEN_STAR_TILE,
    },
    "scholar_rock": {
        "monument": [GARDEN_ROCK],
        "flank":    BAMBOO_CLUMP,
        "edge":     GARDEN_LANTERN,
        "paving":   HERRINGBONE_GARDEN,
    },
    "agora_forum": {
        "monument": [MARBLE_PLINTH, DORIC_CAPITAL],
        "flank":    SYMPOSIUM_TABLE,
        "edge":     PHILOSOPHERS_SCROLL,
        "paving":   INLAID_MARBLE,
    },
    "festival_square": {
        "monument": [BRAZIER, CHANDELIER],
        "flank":    CANDELABRA,
        "edge":     STAR_LAMP,
        "paving":   GARDEN_STAR_TILE,
    },
    "olive_grove": {
        "monument": [STONE_BASIN, OLIVE_BRANCH],
        "flank":    SYMPOSIUM_TABLE,
        "edge":     GREEK_STONE_BENCH,
        "paving":   HERRINGBONE_GARDEN,
    },
    "theatre_court": {
        "monument": [MARBLE_PLINTH, GREEK_THEATRE_MASK],
        "flank":    GREEK_STONE_BENCH,
        "edge":     LAUREL_WREATH_MOUNT,
        "paving":   GARDEN_STAR_TILE,
    },
    "lantern_court": {
        "monument": [GARDEN_LANTERN, LANTERN_ORB],
        "flank":    GREEK_STONE_BENCH,
        "edge":     STAR_LAMP,
        "paving":   MARBLE_MEDALLION_REN,
    },
    "garden_pavilion": {
        "monument": [GARDEN_TABLE, MARBLE_BIRDBATH],
        "flank":    CARVED_BENCH,
        "edge":     GARDEN_LANTERN,
        "paving":   CHAMOMILE_LAWN,
    },
    "torii_plaza": {
        "monument": [TORII_PANEL, TORII_PANEL],
        "flank":    PINE_TOPIARY_JP,
        "edge":     SHISHI_ODOSHI,
        "paving":   TATAMI_PAVING,
    },
    "zen_court": {
        "monument": [GARDEN_ROCK, GARDEN_LANTERN],
        "flank":    PINE_TOPIARY_JP,
        "edge":     BAMBOO_CLUMP,
        "paving":   MOSS_PATCH,
    },
    "roman_forum": {
        "monument": [ROMAN_ARCH_REN, MARBLE_STATUE],
        "flank":    ROMAN_ARCH_REN,
        "edge":     MARBLE_PLINTH,
        "paving":   ROMAN_MOSAIC,
    },
    "greek_agora": {
        "monument": [MARBLE_PLINTH, GREEK_AMPHORA],
        "flank":    GREEK_STONE_BENCH,
        "edge":     VOTIVE_TABLET,
        "paving":   INLAID_MARBLE,
    },
    "mughal_court": {
        "monument": [MUGHAL_ARCH],
        "flank":    ORNAMENTAL_GRASS,
        "edge":     MARIGOLD_BED,
        "paving":   MUDEJAR_STAR_TILE,
    },
    "spanish_plaza": {
        "monument": [ANDALUSIAN_FOUNTAIN],
        "flank":    PORTUGUESE_BENCH,
        "edge":     ORNAMENTAL_GRASS,
        "paving":   SPANISH_PATIO_FLOOR,
    },
}

_SQUARE_THEMES_BY_BIOME = {
    "temperate":      ["civic_marble", "fountain_square", "victory_plaza",
                       "birdbath_garden", "garden_pavilion", "lantern_court"],
    "boreal":         ["civic_marble", "fountain_square", "scholar_court",
                       "lantern_court"],
    "birch_forest":   ["birdbath_garden", "fountain_square", "civic_marble",
                       "garden_pavilion"],
    "redwood":        ["scholar_court", "civic_marble", "birdbath_garden",
                       "garden_pavilion"],
    "tropical":       ["fountain_square", "lion_plaza", "scholar_rock",
                       "lantern_court"],
    "jungle":         ["scholar_rock", "lion_plaza", "fountain_square"],
    "savanna":        ["lion_plaza", "obelisk_court", "victory_plaza",
                       "agora_forum"],
    "wetland":        ["birdbath_garden", "scholar_rock", "lantern_court"],
    "tundra":         ["civic_marble", "victory_plaza", "festival_square"],
    "steppe":         ["obelisk_court", "victory_plaza", "agora_forum"],
    "alpine_mountain":["civic_marble", "scholar_court", "festival_square"],
    "rocky_mountain": ["civic_marble", "obelisk_court", "agora_forum"],
    "canyon":         ["obelisk_court", "lion_plaza", "theatre_court"],
    "desert":         ["obelisk_court", "lion_plaza", "fountain_square",
                       "olive_grove"],
    "arid_steppe":    ["obelisk_court", "lion_plaza", "olive_grove",
                       "theatre_court"],
    "mediterranean":  ["spanish_plaza", "greek_agora", "roman_forum",
                       "civic_marble", "fountain_square"],
    "east_asian":     ["torii_plaza", "zen_court", "scholar_rock",
                       "lantern_court"],
    "south_asian":    ["mughal_court", "lion_plaza", "fountain_square",
                       "festival_square"],
}


def _place_town_square(world, rng, center_bx, sy, biodome, half_w=4):
    """Carve out a paved town square with a central sculpture.

    Paving replaces the city floor (still solid, so the player walks on it).
    The monument, benches, lanterns, and other ornamentation are placed as
    background blocks so the entire plaza stays walkable.
    """
    pool = _SQUARE_THEMES_BY_BIOME.get(biodome, list(SQUARE_THEMES.keys()))
    theme_name = rng.choice(pool)
    theme = SQUARE_THEMES[theme_name]

    # Pave the floor row across the square.
    paving = theme["paving"]
    for wx in range(center_bx - half_w, center_bx + half_w + 1):
        if world.get_block(wx, sy) == STONE:
            world.set_block(wx, sy, paving)

    # Central sculpture (monument) — stacked bottom-up from sy-1.
    monument = theme["monument"]
    for i, blk in enumerate(monument):
        my = sy - 1 - i
        if 0 <= my < world.height and world.get_block(center_bx, my) == AIR:
            world.set_bg_block(center_bx, my, blk)

    # Flanking decoration two columns out on each side.
    flank = theme["flank"]
    flank_y = sy - 1
    for dx in (-2, 2):
        wx = center_bx + dx
        if 0 <= flank_y < world.height and world.get_block(wx, flank_y) == AIR:
            world.set_bg_block(wx, flank_y, flank)

    # Edge ornaments on the outer corners.
    edge = theme["edge"]
    edge_y = sy - 1
    for wx in (center_bx - half_w, center_bx + half_w):
        if 0 <= edge_y < world.height and world.get_block(wx, edge_y) == AIR:
            world.set_bg_block(wx, edge_y, edge)

    # Town flag — placed in background at square center, one block above the ground.
    flag_y = sy - 1
    if 0 <= flag_y < world.height:
        world.set_bg_block(center_bx, flag_y, TOWN_FLAG_BLOCK)


# ---------------------------------------------------------------------------
# Streets, streetlamps, gateposts, pavilions, wells
# ---------------------------------------------------------------------------

# Pool of paving blocks chosen per-city for the main street.
_STREET_PAVINGS = (COBBLESTONE, HERRINGBONE_GARDEN, GARDEN_STAR_TILE,
                   INLAID_MARBLE)

# Pool of streetlamp blocks placed periodically along the street.
_STREETLAMP_BLOCKS = (GARDEN_LANTERN, TORCH, WALL_SCONCE,
                      LANTERN_ORB, STAR_LAMP, BRAZIER)


def _pave_main_street(world, rng, lo_x, hi_x, sy):
    """Replace the bare-stone city floor with a chosen paving block.

    Skips bedrock and any non-stone block, so building floors, rugs, and
    square paving aren't overwritten.
    """
    paving = rng.choice(_STREET_PAVINGS)
    if not (0 <= sy < world.height):
        return
    for bx in range(lo_x, hi_x + 1):
        if world.get_block(bx, sy) == STONE:
            world.set_block(bx, sy, paving)


def _place_streetlamps(world, rng, lo_x, hi_x, sy, spacing=6):
    """Sprinkle bg-block streetlamps along the city street.

    Each lamp sits above the floor as a background block so it renders
    against the sky without blocking the player. Lamps are skipped over
    columns that are inside a roofed building — we test several rows of
    headroom to distinguish open street from interior.
    """
    lamp = rng.choice(_STREETLAMP_BLOCKS)
    lamp_y = sy - 2
    if not (0 <= lamp_y < world.height):
        return
    for bx in range(lo_x, hi_x + 1, spacing):
        # All four rows above the floor must be open air — guarantees we're
        # outdoors and not standing under a building roof.
        if all(world.get_block(bx, sy - dy) == AIR for dy in (1, 2, 3, 4, 5)):
            world.set_bg_block(bx, lamp_y, lamp)


def _place_gateposts(world, rng, lo_x, hi_x, sy):
    """Tall stone posts at the two ends of the city marking the entrance.

    Each post is 4 rows of stacked masonry topped with an ornamental cap.
    Posts are real solid blocks so they read as a clear threshold; the
    gap between post and city body is wide enough to walk through.
    """
    cap = rng.choice((GARDEN_OBELISK, ARCH_STONE, DORIC_CAPITAL,
                      LAUREL_WREATH_MOUNT, GARDEN_LANTERN))
    base_block = rng.choice((HOUSE_WALL_STONE, GRANITE_ASHLAR, LIMESTONE_BLOCK,
                             COBBLESTONE))
    for bx in (lo_x, hi_x):
        for dy in range(1, 5):
            wy = sy - dy
            if 0 <= wy < world.height and world.get_block(bx, wy) == AIR:
                world.set_bg_block(bx, wy, base_block)
        cap_y = sy - 5
        if 0 <= cap_y < world.height and world.get_block(bx, cap_y) == AIR:
            world.set_bg_block(bx, cap_y, cap)


def _pick_wall_style(rng, biodome, city_size):
    """Return a (base, cap, height, has_crenel) style, or None for an open city."""
    chance = _WALL_CHANCE_BY_SIZE.get(city_size, 0.3)
    if rng.random() > chance:
        return None
    pool = _WALL_STYLE_POOLS.get(biodome, _DEFAULT_WALL_STYLES)
    return rng.choice(pool)


def _place_city_walls(world, rng, lo_x, hi_x, sy, biodome, city_size):
    """Build foreground gate towers with optional crenellations and a bg
    wall section flanking each gate so the city reads as enclosed.

    Open cities (style is None) fall back to the simpler bg gateposts.
    The 2-tall gate gap (sy-1, sy-2) at each gate column is left clear so
    the player can walk through; the wall starts at sy-3 and rises to sy-h.
    """
    style = _pick_wall_style(rng, biodome, city_size)
    if style is None:
        _place_gateposts(world, rng, lo_x, hi_x, sy)
        return

    base, cap, height, has_crenel = style

    # Foreground gate columns at the city edges.
    for gate_x in (lo_x, hi_x):
        for dy in range(3, height + 1):
            wy = sy - dy
            if 0 <= wy < world.height and world.get_block(gate_x, wy) == AIR:
                world.set_block(gate_x, wy, base)
        if has_crenel:
            crenel_y = sy - height - 1
            if 0 <= crenel_y < world.height and world.get_block(gate_x, crenel_y) == AIR:
                world.set_block(gate_x, crenel_y, cap)

    # Background wall continuation: 2 columns flanking each gate outward,
    # giving the impression the wall extends beyond the gate towers.
    for outward, gate_x in ((-1, lo_x), (+1, hi_x)):
        for step in range(1, 3):
            bx = gate_x + outward * step
            for dy in range(3, height + 1):
                wy = sy - dy
                if 0 <= wy < world.height and world.get_block(bx, wy) == AIR:
                    world.set_bg_block(bx, wy, base)
            if has_crenel:
                top_y = sy - height - 1
                if 0 <= top_y < world.height and world.get_block(bx, top_y) == AIR:
                    world.set_bg_block(bx, top_y, cap)


def _place_pavilion(world, left_x, sy, width, wall_height,
                    wall_block=GARDEN_COLUMN, roof_block=HOUSE_ROOF_STONE):
    """Open-sided garden pavilion: columns at each corner, peaked roof, hollow inside."""
    h = max(3, wall_height)
    # Corner columns — stop one row short so the player can walk in at street level.
    for wy in range(sy - h, sy - 1):
        if 0 <= wy < world.height:
            world.set_block(left_x, wy, wall_block)
            world.set_block(left_x + width - 1, wy, wall_block)

    # Capitals just above each column.
    cap_y = sy - h
    if 0 <= cap_y < world.height:
        world.set_block(left_x, cap_y, DORIC_CAPITAL)
        world.set_block(left_x + width - 1, cap_y, DORIC_CAPITAL)

    # Lintel running across the top.
    lintel_y = cap_y - 1
    if 0 <= lintel_y < world.height:
        for rx in range(left_x, left_x + width):
            world.set_block(rx, lintel_y, ARCH_STONE)

    # Peaked roof over the lintel.
    half = max(1, width // 2)
    for row in range(half + 1):
        row_y = lintel_y - 1 - row
        if not (0 <= row_y < world.height):
            break
        for rx in range(left_x + row, left_x + width - row):
            if 0 <= rx < world.width:
                world.set_block(rx, row_y, roof_block)

    # A bench inside, as bg, so the pavilion reads as a sit-down spot.
    bench_y = sy - 1
    if 0 <= bench_y < world.height:
        for wx in range(left_x + 1, left_x + width - 1):
            if world.get_block(wx, bench_y) == AIR:
                world.set_bg_block(wx, bench_y, GREEK_STONE_BENCH)


def _place_well(world, left_x, sy, width, wall_height):
    """Stone well: low walls around a shaft with a peaked wood canopy on posts."""
    if width < 3:
        width = 3
    # Low stone wellhead around the centre column (centre stays open).
    # Edges are bg so the player can walk up to the well without collision.
    well_y = sy - 1
    if 0 <= well_y < world.height:
        world.set_bg_block(left_x, well_y, COBBLESTONE)
        world.set_bg_block(left_x + width - 1, well_y, COBBLESTONE)
        for wx in range(left_x + 1, left_x + width - 1):
            if world.get_block(wx, well_y) == AIR:
                world.set_bg_block(wx, well_y, COBBLESTONE)

    # Two timber posts holding up the canopy.
    post_h = max(2, wall_height - 1)
    for dy in range(1, post_h + 1):
        wy = sy - 1 - dy
        if 0 <= wy < world.height:
            world.set_block(left_x, wy, HOUSE_WALL_DARK)
            world.set_block(left_x + width - 1, wy, HOUSE_WALL_DARK)

    # Peaked canopy.
    canopy_y = sy - 1 - post_h - 1
    if 0 <= canopy_y < world.height:
        for rx in range(left_x - 1, left_x + width + 1):
            world.set_block(rx, canopy_y, HOUSE_ROOF)
    peak_y = canopy_y - 1
    if 0 <= peak_y < world.height:
        for rx in range(left_x, left_x + width):
            world.set_block(rx, peak_y, HOUSE_ROOF)

    # Bucket dangling under the canopy as a bg block.
    bucket_y = canopy_y + 1
    bucket_x = left_x + width // 2
    if 0 <= bucket_y < world.height and world.get_block(bucket_x, bucket_y) == AIR:
        world.set_bg_block(bucket_x, bucket_y, RAIN_BARREL)


def _decorate_interior(world, rng, left_x, sy, width, npc_col):
    """Add rugs, tapestries, and functional furniture (beds, chests) to the interior.
    The rug becomes the floor block (still solid, so the NPC stands on it).
    The tapestry and furniture are placed as background blocks.
    """
    if width < 4:
        return
    rug_block = rng.choice(_INTERIOR_RUGS)
    if 0 <= sy < world.height:
        for wx in range(left_x + 1, left_x + width - 1):
            if world.get_block(wx, sy) == STONE:
                world.set_block(wx, sy, rug_block)

    tapestry_block = rng.choice(_INTERIOR_TAPESTRIES)
    tap_x = left_x + width - 2
    if tap_x == npc_col:
        tap_x = left_x + 2
    tap_y = sy - 3
    if 0 <= tap_y < world.height and world.get_block(tap_x, tap_y) == AIR:
        world.set_bg_block(tap_x, tap_y, tapestry_block)

    # Add furniture if there's enough room
    if width >= 5:
        # Pick a side that isn't the NPC's side
        furn_x = left_x + 1 if npc_col > left_x + width // 2 else left_x + width - 2
        pool = [BED, CHEST_BLOCK, SYMPOSIUM_TABLE, STORAGE_PITHOS, BAKERY_BLOCK]
        _set_bg_furniture(world, furn_x, sy - 1, rng.choice(pool))


def _decorate_facade(world, rng, left_x, sy, width, wall_height, wall_block):
    """Add a carved shutter window and a flower box ledge to the front facade."""
    # Carve one of the upper-mid wall blocks into a shuttered window on each side wall.
    win_y = sy - wall_height + 2
    if 0 <= win_y < world.height:
        for bx in (left_x, left_x + width - 1):
            if world.get_block(bx, win_y) == wall_block:
                world.set_block(bx, win_y, CARVED_SHUTTER)

    # Flower-box ledge as a background block adjacent to each side wall — purely visual.
    box_block = rng.choice(_FACADE_FLOWER_BOXES)
    ledge_y = win_y + 1
    if 0 <= ledge_y < world.height:
        for bx, dx in ((left_x, -1), (left_x + width - 1, 1)):
            adj = bx + dx
            if world.get_block(adj, ledge_y) == AIR:
                world.set_bg_block(adj, ledge_y, box_block)

    # Hanging basket as a bg block hanging just under the eaves — outside the door arch.
    basket_y = sy - wall_height
    for bx in (left_x - 1, left_x + width):
        if 0 <= basket_y < world.height and world.get_block(bx, basket_y) == AIR:
            world.set_bg_block(bx, basket_y, HANGING_BASKET)


def _place_tower(world, left_x, sy, width, wall_height,
                 wall_block=HOUSE_WALL_STONE, roof_block=HOUSE_ROOF_STONE):
    """Tall narrow building with crenelated battlements and an iron-grille window."""
    tower_h = wall_height + 3
    for wy in range(sy - tower_h, sy):
        for wx in range(left_x, left_x + width):
            if not (0 <= wy < world.height):
                continue
            is_left  = (wx == left_x)
            is_right = (wx == left_x + width - 1)
            # 4-row opening so players approaching from terrain up to 3 blocks
            # above the city floor can still walk through without hitting solid wall.
            is_door  = (wy >= sy - 4) and (is_left or is_right)
            if is_door:
                world.set_block(wx, wy, WOOD_DOOR_OPEN)
            elif is_left or is_right:
                world.set_block(wx, wy, wall_block)
            else:
                world.set_block(wx, wy, AIR)
                world.set_bg_block(wx, wy, wall_block)

    # Iron-grille window mid-tower
    win_y = sy - tower_h + 2
    win_x = left_x + width // 2
    if 0 <= win_y < world.height:
        world.set_block(win_x, win_y, WROUGHT_IRON_GRILLE)

    # Crenelated battlements: alternating wall and air across the top.
    crown_y = sy - tower_h
    if 0 <= crown_y < world.height:
        for i, wx in enumerate(range(left_x - 1, left_x + width + 1)):
            if i % 2 == 0:
                world.set_block(wx, crown_y, roof_block)
    # Solid roof slab one row down so the inside is sealed.
    slab_y = crown_y + 1
    if 0 <= slab_y < world.height:
        for wx in range(left_x, left_x + width):
            world.set_block(wx, slab_y, roof_block)


def _place_longhouse(world, left_x, sy, width, wall_height,
                     wall_block=HOUSE_WALL, roof_block=HOUSE_ROOF, rng=None):
    """Wide, low building with a stretched flat roof and shutter accents."""
    h = max(3, wall_height - 1)
    _place_house(world, left_x, sy, width, h, wall_block, roof_block, rng)
    # Shutter pairs as bg accents along the long facade — visual only,
    # so they never block the inside of the longhouse.
    shutter_y = sy - h + 1
    if 0 <= shutter_y < world.height:
        for wx in range(left_x + 2, left_x + width - 2, 2):
            if world.get_block(wx, shutter_y) == AIR:
                world.set_bg_block(wx, shutter_y, CARVED_SHUTTER)


def _place_market_stall(world, rng, left_x, sy, width, wall_height):
    """Open-front market stall: two timber posts, a striped awning, a counter.

    The NPC inside is fully visible — the stall is just visual framing.
    """
    h = max(2, min(3, wall_height - 1))
    awning_block = rng.choice(_INTERIOR_TAPESTRIES)

    # Side posts — stop one row short of the ground so the player can walk in freely.
    for wy in range(sy - h, sy - 1):
        if 0 <= wy < world.height:
            world.set_block(left_x, wy, HOUSE_WALL_DARK)
            world.set_block(left_x + width - 1, wy, HOUSE_WALL_DARK)

    # Striped awning across the top, with overhang.
    awning_y = sy - h
    if 0 <= awning_y < world.height:
        for wx in range(left_x - 1, left_x + width + 1):
            world.set_block(wx, awning_y, awning_block)

    # Pendant valance dangling under the awning — bg only so it doesn't block entry.
    valance_y = awning_y + 1
    if 0 <= valance_y < world.height:
        for wx in range(left_x + 1, left_x + width - 1):
            if world.get_block(wx, valance_y) == AIR:
                world.set_bg_block(wx, valance_y, awning_block)

    # Counter / table along the front, also bg so the player can step in.
    counter_y = sy - 1
    counter_block = rng.choice((GARDEN_TABLE, SYMPOSIUM_TABLE))
    if 0 <= counter_y < world.height:
        for wx in range(left_x + 1, left_x + width - 1):
            if world.get_block(wx, counter_y) == AIR:
                world.set_bg_block(wx, counter_y, counter_block)


def _place_ruin(world, left_x, sy, width, wall_height):
    """Partial walls of weathered cobblestone — looks abandoned, no door, no roof.

    Loose rubble inside the footprint is placed as background so the player
    can walk through what's left of the building.
    """
    for wy in range(sy - wall_height, sy):
        for wx in range(left_x, left_x + width):
            if not (0 <= wy < world.height):
                continue
            is_left  = (wx == left_x)
            is_right = (wx == left_x + width - 1)
            # Top half of the side walls is broken away; bottom 2 rows are also
            # open so the player can walk through without being blocked.
            broken_top  = wy < sy - wall_height + 2
            broken_base = wy >= sy - 2
            if (is_left or is_right) and not broken_top and not broken_base:
                world.set_block(wx, wy, COBBLESTONE)
            else:
                world.set_block(wx, wy, AIR)
                world.set_bg_block(wx, wy, COBBLESTONE)
    # Scattered rubble — bg only so the ruin stays walkable.
    for wx in (left_x + 1, left_x + width // 2, left_x + width - 2):
        floor_y = sy - 1
        if 0 <= floor_y < world.height and world.get_block(wx, floor_y) == AIR:
            world.set_bg_block(wx, floor_y, COBBLESTONE)


def _place_inn(world, left_x, sy, width, wall_height, rng):
    """Dark-timber two-story tavern: lantern sign outside, brazier and benches inside."""
    floor2_h = rng.randint(2, 3)
    _place_house_two_story(world, left_x, sy, width, wall_height, floor2_h,
                           HOUSE_WALL_DARK, SLATE_SHINGLE)
    mid = left_x + width // 2
    for wx in range(left_x + 1, left_x + width - 1):
        if 0 <= sy < world.height and world.get_block(wx, sy) == STONE:
            world.set_block(wx, sy, rng.choice(_INTERIOR_RUGS))
    if 0 <= sy - 1 < world.height:
        world.set_bg_block(mid,                     sy - 1, BRAZIER)
        world.set_bg_block(left_x + 1,              sy - 1, CARVED_BENCH)
        world.set_bg_block(left_x + width - 2,      sy - 1, CARVED_BENCH)
    sign_y = sy - wall_height
    if 0 <= sign_y < world.height:
        world.set_bg_block(left_x - 1, sign_y, GARDEN_LANTERN)


def _place_smithy(world, left_x, sy, width, wall_height,
                  wall_block=ROUGH_STONE_WALL):
    """Open-front stone forge: solid back wall, stub side walls, brazier and iron racks."""
    rx = left_x + width - 1
    for wy in range(sy - wall_height, sy):
        if 0 <= wy < world.height:
            world.set_block(rx, wy, wall_block)
            world.set_bg_block(rx, wy, wall_block)
    stub_h = max(2, wall_height // 2)
    for wy in range(sy - stub_h, sy):
        if not (0 <= wy < world.height):
            continue
        world.set_block(left_x, wy, WOOD_DOOR_OPEN if wy >= sy - 2 else wall_block)
    for wy in range(sy - wall_height, sy):
        for wx in range(left_x, left_x + width):
            if 0 <= wy < world.height and world.get_block(wx, wy) == AIR:
                world.set_bg_block(wx, wy, wall_block)
    for wx in range(left_x, left_x + width):
        if 0 <= sy < world.height and world.get_block(wx, sy) not in (AIR, BEDROCK):
            world.set_block(wx, sy, COBBLESTONE)
    mid = left_x + width // 2
    if 0 <= sy - 1 < world.height:
        world.set_bg_block(mid,                     sy - 1, BRAZIER)
        world.set_bg_block(left_x + 1,              sy - 1, WROUGHT_IRON_GRILLE)
        world.set_bg_block(left_x + width - 2,      sy - 1, WROUGHT_IRON_GRILLE)
    if 0 <= sy - 3 < world.height:
        world.set_bg_block(mid, sy - 3, WALL_SCONCE)


def _place_apothecary(world, left_x, sy, width, wall_height, rng):
    """Whitewashed herb shop: plaster walls, flower boxes everywhere, botanical interior."""
    _place_house(world, left_x, sy, width, wall_height, ALPINE_PLASTER, HOUSE_ROOF_DARK)
    box_y = sy - 3
    if 0 <= box_y < world.height:
        for bx in range(left_x - 1, left_x + width + 1, 2):
            if world.get_block(bx, box_y) == AIR:
                world.set_bg_block(bx, box_y, rng.choice((FLOWER_BOX, GERANIUM_BOX)))
    basket_y = sy - wall_height
    if 0 <= basket_y < world.height:
        for bx in (left_x - 1, left_x + width):
            if world.get_block(bx, basket_y) == AIR:
                world.set_bg_block(bx, basket_y, HANGING_BASKET)
    if 0 <= sy - 1 < world.height:
        world.set_bg_block(left_x + 1,              sy - 1, LAVENDER_BED)
        world.set_bg_block(left_x + width - 2,      sy - 1, ROSE_BED)
        world.set_bg_block(left_x + width // 2,     sy - 1, MARIGOLD_BED)
    if 0 <= sy - wall_height + 2 < world.height:
        world.set_bg_block(left_x + width // 2,     sy - wall_height + 2, WALL_SCONCE)


def _place_hospital(world, left_x, sy, width, wall_height, rng):
    """Clean, stone medical facility: white stone walls, multiple beds, orderly interior."""
    _place_house(world, left_x, sy, width, wall_height, HOUSE_WALL_STONE, HOUSE_ROOF_STONE)
    # Interior: hospital beds and medical supplies
    for bx in range(left_x + 1, left_x + width - 1, 3):
        if 0 <= sy - 1 < world.height:
             world.set_bg_block(bx, sy - 1, BED)
             if bx + 1 < left_x + width - 1:
                  world.set_bg_block(bx + 1, sy - 1, AIR) # Clear space next to bed

    # Sconces for light
    if 0 <= sy - wall_height + 2 < world.height:
        world.set_bg_block(left_x + 1, sy - wall_height + 2, WALL_SCONCE)
        world.set_bg_block(left_x + width - 2, sy - wall_height + 2, WALL_SCONCE)


def _place_coffee_shop(world, left_x, sy, width, wall_height, rng):
    """Coffee shop: warm wood paneling, counter, and aromatic vibe."""
    _place_house(world, left_x, sy, width, wall_height, PINE_PLANK_WALL, HOUSE_ROOF_DARK)
    if 0 <= sy - 2 < world.height:
        world.set_bg_block(left_x + 1, sy - 2, STORAGE_PITHOS)
        world.set_bg_block(left_x + width - 2, sy - 2, STONE_BASIN)


def _place_wine_shop(world, left_x, sy, width, wall_height, rng):
    """Wine shop: elegant stone/wood, amphorae on display."""
    _place_house(world, left_x, sy, width, wall_height, HOUSE_WALL_BRICK, HOUSE_ROOF_DARK)
    if 0 <= sy - 1 < world.height:
        world.set_bg_block(left_x + 1, sy - 1, GREEK_AMPHORA)
        world.set_bg_block(left_x + width - 2, sy - 1, GREEK_AMPHORA)


def _set_bg_furniture(world, bx, by, bid):
    """Set a background furniture block if in-bounds and empty."""
    if 0 <= by < world.height and world.get_block(bx, by) == AIR:
        world.set_bg_block(bx, by, bid)


def _build_modular_building(world, rng, left_x, sy, width, wall_height, 
                             wall_block=HOUSE_WALL, roof_block=HOUSE_ROOF, building_type="house"):
    """Assembles a building from modular pieces (rooms/units) 'pushed' together.
    Each unit is 3-5 blocks wide and contains specific interior details.
    """
    # 1. Determine pieces based on building type and width
    pieces = []
    remaining_w = width
    while remaining_w > 0:
        pw = rng.randint(3, 5)
        if remaining_w - pw < 3: # don't leave a tiny sliver
            pw = remaining_w
        pieces.append(pw)
        remaining_w -= pw
    
    # 2. Select themes for each piece
    themes = []
    if building_type == "barn":
        themes = ["stalls"] * len(pieces)
    elif building_type == "shop":
        themes = ["entry"] + ["display"] * (len(pieces)-1)
    else: # house
        # Mix of entry, living, sleeping, kitchen
        pool = ["living", "sleeping", "kitchen"]
        themes = ["entry"] + [rng.choice(pool) for _ in range(max(0, len(pieces)-1))]
    
    # 3. Build each piece
    current_x = left_x
    for i, pw in enumerate(pieces):
        is_left_edge = (i == 0)
        is_right_edge = (i == len(pieces) - 1)
        theme = themes[i]
        
        # Room core: walls and floor/ceiling
        for wy in range(sy - wall_height, sy):
            for wx in range(current_x, current_x + pw):
                if not (0 <= wy < world.height): continue
                
                is_ceiling = (wy == sy - wall_height)
                # Internal walls are replaced with a background supporting block
                is_wall = (is_left_edge and wx == current_x) or (is_right_edge and wx == current_x + pw - 1)
                is_door = (wy >= sy - 2) and is_wall
                
                if is_door:
                    world.set_block(wx, wy, WOOD_DOOR_OPEN)
                elif is_wall or is_ceiling:
                    world.set_block(wx, wy, wall_block)
                else:
                    world.set_block(wx, wy, AIR)
                    world.set_bg_block(wx, wy, wall_block)
        
        # Interior decorations
        mid_x = current_x + pw // 2
        floor_y = sy - 1
        
        if theme == "sleeping":
            _set_bg_furniture(world, mid_x, floor_y, BED)
            if pw > 3:
                _set_bg_furniture(world, current_x + 1, floor_y, CHEST_BLOCK)
        elif theme == "living":
            _set_bg_furniture(world, mid_x, floor_y, SYMPOSIUM_TABLE)
            _set_bg_furniture(world, mid_x, floor_y - 2, WALL_SCONCE)
        elif theme == "kitchen":
            _set_bg_furniture(world, current_x + 1, floor_y, BAKERY_BLOCK)
            _set_bg_furniture(world, current_x + 1, floor_y - 2, RAIN_BARREL)
        elif theme == "stalls":
            _set_bg_furniture(world, mid_x, floor_y, STABLE_BLOCK)
            _set_bg_furniture(world, mid_x + 1, floor_y, HAY_BALE)
        elif theme == "display":
            _set_bg_furniture(world, mid_x, floor_y, STORAGE_PITHOS)
            _set_bg_furniture(world, current_x + 1, floor_y - 1, HERALDIC_PANEL)
            
        current_x += pw

    # 4. Roof applied over everything
    roof_y = sy - wall_height - 1
    for rx in range(left_x - 1, left_x + width + 1):
        if 0 <= roof_y < world.height:
            world.set_block(rx, roof_y, roof_block)
    peak_y = roof_y - 1
    for rx in range(left_x, left_x + width):
        if 0 <= peak_y < world.height:
            world.set_block(rx, peak_y, roof_block)


def _place_house(world, left_x, sy, width, wall_height,
                 wall_block=HOUSE_WALL, roof_block=HOUSE_ROOF, rng=None):
    """Hollow enterable house with modular internal details."""
    if rng is None:
        rng = random.Random(left_x ^ sy)
    _build_modular_building(world, rng, left_x, sy, width, wall_height, wall_block, roof_block, "house")


def _place_barn(world, left_x, sy, width, wall_height, rng):
    """Modular barn with animal stalls and hay storage."""
    _build_modular_building(world, rng, left_x, sy, width, wall_height, HOUSE_WALL_DARK, HOUSE_ROOF_DARK, "barn")


def _place_house_two_story(world, left_x, sy, width, floor1_h, floor2_h,
                            wall_block=HOUSE_WALL, roof_block=HOUSE_ROOF, rng=None):
    """Two-story building. Ground floor has doors on both sides; upper floor via ladder."""
    if rng is None: rng = random.Random(left_x ^ sy)
    ladder_col = left_x + width - 2  # one column from right wall

    # Ground floor
    for wy in range(sy - floor1_h, sy):
        for wx in range(left_x, left_x + width):
            if not (0 <= wy < world.height):
                continue
            is_ceiling    = (wy == sy - floor1_h)
            is_left_side  = (wx == left_x)
            is_right_side = (wx == left_x + width - 1)
            is_door_row   = (wy >= sy - 2)
            is_left_door  = is_left_side  and is_door_row
            is_right_door = is_right_side and is_door_row
            is_ladder_pos = (wx == ladder_col)
            is_hole       = (is_ceiling and is_ladder_pos)

            if is_left_door or is_right_door:
                world.set_block(wx, wy, WOOD_DOOR_OPEN)
            elif is_hole:
                # Opening in ceiling for ladder passthrough
                world.set_block(wx, wy, LADDER)
                world.set_bg_block(wx, wy, wall_block)
            elif is_ceiling or is_left_side or is_right_side:
                world.set_block(wx, wy, wall_block)
            elif is_ladder_pos:
                world.set_block(wx, wy, LADDER)
                world.set_bg_block(wx, wy, wall_block)
            else:
                world.set_block(wx, wy, AIR)
                world.set_bg_block(wx, wy, wall_block)

    # Upper floor
    for wy in range(sy - floor1_h - floor2_h, sy - floor1_h):
        for wx in range(left_x, left_x + width):
            if not (0 <= wy < world.height):
                continue
            is_top        = (wy == sy - floor1_h - floor2_h)
            is_left_side  = (wx == left_x)
            is_right_side = (wx == left_x + width - 1)

            if is_top or is_left_side or is_right_side:
                world.set_block(wx, wy, wall_block)
            elif wx == ladder_col:
                world.set_block(wx, wy, LADDER)
                world.set_bg_block(wx, wy, wall_block)
            else:
                world.set_block(wx, wy, AIR)
                world.set_bg_block(wx, wy, wall_block)

    # Upper floor furniture
    _set_bg_furniture(world, left_x + 2, sy - floor1_h - 1, BED)
    if width > 5:
        _set_bg_furniture(world, left_x + 3, sy - floor1_h - 1, CHEST_BLOCK)

    # Flat roof overhang
    roof_y = sy - floor1_h - floor2_h - 1
    for rx in range(left_x - 1, left_x + width + 1):
        if 0 <= roof_y < world.height:
            world.set_block(rx, roof_y, roof_block)

    # Peaked ridge
    peak_y = roof_y - 1
    for rx in range(left_x, left_x + width):
        if 0 <= peak_y < world.height:
            world.set_block(rx, peak_y, roof_block)


def _place_house_three_story(world, rng, left_x, sy, width, floor1_h, floor2_h, floor3_h,
                              wall_block=HOUSE_WALL, roof_block=HOUSE_ROOF):
    """Three-story building. Ground floor has doors; upper floors via shared ladder column."""
    ladder_col = left_x + width - 2

    def _floor(top_y, bot_y, has_ceiling_hole, has_doors):
        """Place one floor's walls, ceiling, and interior."""
        for wy in range(top_y, bot_y):
            for wx in range(left_x, left_x + width):
                if not (0 <= wy < world.height):
                    continue
                is_ceil  = (wy == top_y)
                is_left  = (wx == left_x)
                is_right = (wx == left_x + width - 1)
                is_door  = has_doors and (wy >= bot_y - 2) and (is_left or is_right)
                is_hole  = has_ceiling_hole and is_ceil and (wx == ladder_col)
                if is_door:
                    world.set_block(wx, wy, WOOD_DOOR_OPEN)
                elif is_hole:
                    world.set_block(wx, wy, LADDER)
                    world.set_bg_block(wx, wy, wall_block)
                elif is_ceil or is_left or is_right:
                    world.set_block(wx, wy, wall_block)
                elif wx == ladder_col:
                    world.set_block(wx, wy, LADDER)
                    world.set_bg_block(wx, wy, wall_block)
                else:
                    world.set_block(wx, wy, AIR)
                    world.set_bg_block(wx, wy, wall_block)

    floor2_top = sy - floor1_h
    floor3_top = sy - floor1_h - floor2_h
    roof_top   = sy - floor1_h - floor2_h - floor3_h

    _floor(floor2_top, sy,        has_ceiling_hole=True,  has_doors=True)
    _floor(floor3_top, floor2_top, has_ceiling_hole=True,  has_doors=False)
    _floor(roof_top,   floor3_top, has_ceiling_hole=False, has_doors=False)

    # Decorate floors 2 and 3 (floor 1 is handled by _build_single_city)
    _decorate_interior(world, rng, left_x, floor2_top, width, left_x + 1)
    _decorate_interior(world, rng, left_x, floor3_top, width, left_x + 1)

    # Flat overhang + peaked ridge
    roof_y = roof_top - 1
    for rx in range(left_x - 1, left_x + width + 1):
        if 0 <= roof_y < world.height:
            world.set_block(rx, roof_y, roof_block)
    peak_y = roof_y - 1
    for rx in range(left_x, left_x + width):
        if 0 <= peak_y < world.height:
            world.set_block(rx, peak_y, roof_block)


def _place_library(world, left_x, sy, width, wall_height, rng,
                   wall_block=HOUSE_WALL_STONE, roof_block=HOUSE_ROOF_STONE):
    """Stone library: arched window, reading tables, scroll racks, lantern sconce."""
    _place_house(world, left_x, sy, width, wall_height, wall_block, roof_block, rng)

    # Lancet window on the facade mid-height
    win_y = sy - wall_height // 2
    if 0 <= win_y < world.height:
        world.set_bg_block(left_x + width // 2, win_y, LANCET_WINDOW)

    # Interior furnishings as background blocks
    if 0 <= sy - 1 < world.height:
        world.set_bg_block(left_x + 1,          sy - 1, SYMPOSIUM_TABLE)
        world.set_bg_block(left_x + width - 2,  sy - 1, SYMPOSIUM_TABLE)
        world.set_bg_block(left_x + width // 2, sy - 1, PHILOSOPHERS_SCROLL)
    if 0 <= sy - 3 < world.height:
        world.set_bg_block(left_x + 1,           sy - 3, WALL_SCONCE)
        world.set_bg_block(left_x + width - 2,   sy - 3, VOTIVE_TABLET)


def _place_restaurant(world, left_x, sy, width, wall_height, style="default"):
    """Restaurant: hollow interior, doors on both sides, flat cultural awning."""
    wall_block, awning_block = _RESTAURANT_STYLES.get(style, _RESTAURANT_STYLES["default"])
    for wy in range(sy - wall_height, sy):
        for wx in range(left_x, left_x + width):
            if not (0 <= wy < world.height):
                continue
            is_top        = (wy == sy - wall_height)
            is_left_side  = (wx == left_x)
            is_right_side = (wx == left_x + width - 1)
            is_door_row   = (wy >= sy - 2)
            is_left_door  = is_left_side  and is_door_row
            is_right_door = is_right_side and is_door_row

            if is_left_door or is_right_door:
                world.set_block(wx, wy, WOOD_DOOR_OPEN)
            elif is_top or is_left_side or is_right_side:
                world.set_block(wx, wy, wall_block)
            else:
                world.set_block(wx, wy, AIR)
                world.set_bg_block(wx, wy, wall_block)

    # Flat awning overhang (wider than normal, no peak — distinctive canopy look)
    awning_y = sy - wall_height - 1
    for rx in range(left_x - 2, left_x + width + 2):
        if 0 <= awning_y < world.height:
            world.set_block(rx, awning_y, awning_block)


def _place_temple(world, left_x, sy, width, wall_height):
    """Wide stone temple with a 3-tier pagoda-style roof."""
    # Walls and hollow interior
    for wy in range(sy - wall_height, sy):
        for wx in range(left_x, left_x + width):
            if not (0 <= wy < world.height):
                continue
            is_top        = (wy == sy - wall_height)
            is_left_side  = (wx == left_x)
            is_right_side = (wx == left_x + width - 1)
            is_door_row   = (wy >= sy - 2)
            # Wide double-door entrance on both sides
            is_left_door  = is_left_side  and is_door_row
            is_right_door = is_right_side and is_door_row
            is_left_door2  = (wx == left_x + 1) and is_door_row
            is_right_door2 = (wx == left_x + width - 2) and is_door_row

            if is_left_door or is_right_door or is_left_door2 or is_right_door2:
                world.set_block(wx, wy, WOOD_DOOR_OPEN)
            elif is_top or is_left_side or is_right_side:
                world.set_block(wx, wy, HOUSE_WALL_STONE)
            else:
                world.set_block(wx, wy, AIR)
                world.set_bg_block(wx, wy, HOUSE_WALL_STONE)

    # 3-tier pagoda roof — each tier narrows by 1 block per side and adds 1 row
    base_y = sy - wall_height - 1
    for tier in range(3):
        tier_y = base_y - tier * 2
        shrink = tier
        for rx in range(left_x - 1 + shrink, left_x + width + 1 - shrink):
            if 0 <= tier_y < world.height:
                world.set_block(rx, tier_y, HOUSE_ROOF_STONE)
        peak_y = tier_y - 1
        for rx in range(left_x + shrink, left_x + width - shrink):
            if 0 <= peak_y < world.height:
                world.set_block(rx, peak_y, HOUSE_ROOF_STONE)


def _place_dome_house(world, left_x, sy, width, wall_height,
                      wall_block=SANDSTONE_BLOCK, dome_block=POLISHED_MARBLE):
    """Desert dome building: sandstone box walls topped with a white marble semicircle."""
    center_x = left_x + width // 2

    for wy in range(sy - wall_height, sy):
        for wx in range(left_x, left_x + width):
            if not (0 <= wy < world.height):
                continue
            is_left       = (wx == left_x)
            is_right      = (wx == left_x + width - 1)
            is_door_row   = (wy >= sy - 2)
            is_left_door  = is_left  and is_door_row
            is_right_door = is_right and is_door_row

            if is_left_door or is_right_door:
                world.set_block(wx, wy, WOOD_DOOR_OPEN)
            elif is_left or is_right:
                world.set_block(wx, wy, wall_block)
            else:
                world.set_block(wx, wy, AIR)
                world.set_bg_block(wx, wy, wall_block)

    # Semicircular dome — radius = half of building width
    radius = width // 2
    dome_base_y = sy - wall_height - 1
    for row in range(radius + 1):
        half_w = int((radius * radius - row * row) ** 0.5)
        row_y  = dome_base_y - row
        if not (0 <= row_y < world.height):
            break
        for dx in range(-half_w, half_w + 1):
            rx = center_x + dx
            if 0 <= rx < world.width:
                world.set_block(rx, row_y, dome_block)


def _place_bedouin_tent(world, left_x, sy, width, wall_height, rng):
    """Bedouin goat-hair tent: two corner poles, sagging fabric canopy, open sides."""
    fabric   = rng.choice((HOUSE_WALL_DARK, TEXTILE_TAPESTRY_NATURAL,
                            TEXTILE_TAPESTRY_CRIMSON, TEXTILE_TAPESTRY_AMBER))
    h        = max(3, min(4, wall_height))
    center_x = left_x + width // 2

    # Corner support poles
    for wy in range(sy - h, sy):
        if 0 <= wy < world.height:
            world.set_block(left_x,             wy, HOUSE_WALL_DARK)
            world.set_block(left_x + width - 1, wy, HOUSE_WALL_DARK)

    # Canopy: edges sit at pole-top height, centre sags one row down
    for wx in range(left_x - 1, left_x + width + 1):
        sag = 1 if abs(wx - center_x) < width // 3 else 0
        ry  = sy - h + sag
        if 0 <= ry < world.height and 0 <= wx < world.width:
            world.set_block(wx, ry, fabric)

    # Back curtain — bg only so the front stays open to the player
    for wy in range(sy - h + 1, sy):
        if 0 <= wy < world.height:
            world.set_bg_block(left_x + width - 1, wy, fabric)

    # Ground rug
    rug = rng.choice((TEXTILE_RUG_NATURAL, TEXTILE_RUG_GOLDEN, TEXTILE_RUG_CRIMSON,
                      TEXTILE_RUG_AMBER,   TEXTILE_RUG_IVORY))
    for wx in range(left_x + 1, left_x + width - 1):
        if 0 <= sy < world.height:
            world.set_block(wx, sy, rug)


def _place_caravanserai(world, left_x, sy, width, wall_height):
    """Caravanserai: thick sandstone walls, crenellated parapet, central arched gate."""
    h        = min(8, max(5, wall_height + 2))
    wall     = SANDSTONE_BLOCK
    center_x = left_x + width // 2
    gate_w   = max(2, width // 5)

    # Perimeter walls with open interior
    for wy in range(sy - h, sy):
        for wx in range(left_x, left_x + width):
            if not (0 <= wy < world.height):
                continue
            is_edge = (wx == left_x) or (wx == left_x + width - 1)
            in_gate = abs(wx - center_x) <= gate_w and wy >= sy - 3
            if in_gate:
                pass                                 # gate arch stays AIR
            elif is_edge:
                world.set_block(wx, wy, wall)
            else:
                world.set_block(wx, wy, AIR)
                world.set_bg_block(wx, wy, wall)

    # Gate lintel spanning the arch opening
    lintel_y = sy - 4
    for wx in range(center_x - gate_w - 1, center_x + gate_w + 2):
        if 0 <= lintel_y < world.height and 0 <= wx < world.width:
            world.set_block(wx, lintel_y, wall)

    # Crenellated parapet — alternating merlons above the wall top
    parapet_y = sy - h - 1
    for wx in range(left_x, left_x + width):
        if (wx - left_x) % 2 == 0 and 0 <= parapet_y < world.height:
            world.set_block(wx, parapet_y, wall)


def _place_chapel(world, left_x, sy, width, wall_height):
    """Wood chapel with a single center door and a tall triangular gabled roof."""
    center = left_x + width // 2
    for wy in range(sy - wall_height, sy):
        for wx in range(left_x, left_x + width):
            if not (0 <= wy < world.height):
                continue
            is_top        = (wy == sy - wall_height)
            is_left_side  = (wx == left_x)
            is_right_side = (wx == left_x + width - 1)
            is_door_row   = (wy >= sy - 2)
            is_left_door  = is_left_side  and is_door_row
            is_right_door = is_right_side and is_door_row
            is_center_door = (wx == center) and is_door_row

            if is_left_door or is_right_door or is_center_door:
                world.set_block(wx, wy, WOOD_DOOR_OPEN)
            elif is_top or is_left_side or is_right_side:
                world.set_block(wx, wy, HOUSE_WALL)
            else:
                world.set_block(wx, wy, AIR)
                world.set_bg_block(wx, wy, HOUSE_WALL)

    # Tall triangular gabled roof — each row narrows by 1 per side until 1 block wide
    base_y = sy - wall_height - 1
    half = width // 2 + 1
    for row in range(half):
        row_y = base_y - row
        if not (0 <= row_y < world.height):
            break
        for rx in range(left_x - 1 + row, left_x + width + 1 - row):
            if 0 <= rx < world.width:
                world.set_block(rx, row_y, HOUSE_ROOF)

    # Bell tower: one column above the roof peak, in background so it doesn't block movement
    peak_y = base_y - half
    for by in range(peak_y - 2, peak_y):
        if 0 <= by < world.height:
            world.set_bg_block(center, by, HOUSE_WALL)


def _place_desert_shrine(world, left_x, sy, width, wall_height):
    """Open-sided shrine with stone columns and a wide flat overhanging roof."""
    col_positions = {left_x, left_x + width // 2, left_x + width - 1}
    for wy in range(sy - wall_height, sy):
        for wx in range(left_x, left_x + width):
            if not (0 <= wy < world.height):
                continue
            if wx in col_positions:
                # Ground row is bg so the player can walk through the column bases.
                if wy == sy - 1:
                    world.set_bg_block(wx, wy, HOUSE_WALL_BRICK)
                else:
                    world.set_block(wx, wy, HOUSE_WALL_BRICK)
            else:
                world.set_block(wx, wy, AIR)
                world.set_bg_block(wx, wy, HOUSE_WALL_STONE)

    # Double-layer flat roof with wide overhang
    for roof_y, overhang in ((sy - wall_height - 1, 1), (sy - wall_height - 2, 2)):
        if 0 <= roof_y < world.height:
            for rx in range(left_x - overhang, left_x + width + overhang):
                if 0 <= rx < world.width:
                    world.set_block(rx, roof_y, HOUSE_WALL_STONE)


def _place_jungle_shrine(world, left_x, sy, width, wall_height):
    """Solid stone stepped pyramid narrowing toward a single capstone."""
    steps = min(wall_height, (width // 2) + 1)
    for step in range(steps):
        step_y = sy - step - 1
        if not (0 <= step_y < world.height):
            break
        for wx in range(left_x + step, left_x + width - step):
            if 0 <= wx < world.width:
                # Base row is bg so the player can walk up to the shrine NPC.
                if step_y == sy - 1:
                    world.set_bg_block(wx, step_y, HOUSE_WALL_STONE)
                else:
                    world.set_block(wx, step_y, HOUSE_WALL_STONE)

    # Capstone above pyramid tip
    cap_y = sy - steps - 1
    mid   = left_x + width // 2
    if 0 <= cap_y < world.height:
        world.set_block(mid, cap_y, HOUSE_ROOF_STONE)


def _place_standing_stones(world, left_x, sy, width, wall_height):
    """Three tall stone pillars — shorter at edges, tallest at center."""
    positions = [left_x, left_x + width // 2, left_x + width - 1]
    heights   = [wall_height - 1, wall_height + 1, wall_height - 1]
    for sx, h in zip(positions, heights):
        if not (0 <= sx < world.width):
            continue
        for wy in range(sy - h, sy):
            if 0 <= wy < world.height:
                # Ground row is bg so the player can walk up to the shrine NPC.
                if wy == sy - 1:
                    world.set_bg_block(sx, wy, HOUSE_WALL_STONE)
                else:
                    world.set_block(sx, wy, HOUSE_WALL_STONE)
        # Flat capstone block
        cap_y = sy - h - 1
        if 0 <= cap_y < world.height:
            world.set_block(sx, cap_y, HOUSE_ROOF_STONE)


def _place_himalayan_house(world, left_x, sy, width, wall_height):
    """Himalayan building: MANI_STONE base, whitewashed walls, flat roof + prayer flags."""
    stone_rows = min(2, wall_height - 2)

    for wy in range(sy - wall_height, sy):
        for wx in range(left_x, left_x + width):
            if not (0 <= wy < world.height):
                continue
            is_top        = (wy == sy - wall_height)
            is_left_side  = (wx == left_x)
            is_right_side = (wx == left_x + width - 1)
            is_door_row   = (wy >= sy - 2)
            is_left_door  = is_left_side  and is_door_row
            is_right_door = is_right_side and is_door_row
            is_stone_base = (wy >= sy - stone_rows)

            use_block = MANI_STONE if is_stone_base else WHITEWASHED_WALL

            if is_left_door or is_right_door:
                world.set_block(wx, wy, WOOD_DOOR_OPEN)
            elif is_top or is_left_side or is_right_side:
                world.set_block(wx, wy, use_block)
            else:
                world.set_block(wx, wy, AIR)
                world.set_bg_block(wx, wy, use_block)

    # Flat roof with slight overhang — characteristic Himalayan silhouette
    roof_y = sy - wall_height - 1
    for rx in range(left_x - 1, left_x + width + 1):
        if 0 <= roof_y < world.height and abs(rx) < world.width:
            world.set_block(rx, roof_y, MONASTERY_ROOF)

    # Prayer flags along the roof ridge
    flag_y = roof_y - 1
    for fx in range(left_x, left_x + width, 2):
        if 0 <= flag_y < world.height and abs(fx) < world.width:
            world.set_block(fx, flag_y, PRAYER_FLAG_BLOCK)


def _place_dzong(world, left_x, sy, width, wall_height):
    """Himalayan fortress-monastery (Dzong): battered stone base, white upper walls, tiered roof."""
    stone_split = wall_height * 2 // 3  # lower portion in MANI_STONE

    for wy in range(sy - wall_height, sy):
        for wx in range(left_x, left_x + width):
            if not (0 <= wy < world.height):
                continue
            is_stone_half = (wy >= sy - stone_split)
            wall_blk      = MANI_STONE if is_stone_half else WHITEWASHED_WALL
            is_left_wall  = (wx <= left_x + 1)
            is_right_wall = (wx >= left_x + width - 2)
            is_top        = (wy == sy - wall_height)
            is_door_row   = (wy >= sy - 2)
            # Wide double-door entrance on both sides
            is_left_door  = is_door_row and wx == left_x
            is_left_door2 = is_door_row and wx == left_x + 1
            is_right_door  = is_door_row and wx == left_x + width - 1
            is_right_door2 = is_door_row and wx == left_x + width - 2

            if is_left_door or is_left_door2 or is_right_door or is_right_door2:
                world.set_block(wx, wy, WOOD_DOOR_OPEN)
            elif is_top or is_left_wall or is_right_wall:
                world.set_block(wx, wy, wall_blk)
            else:
                world.set_block(wx, wy, AIR)
                world.set_bg_block(wx, wy, wall_blk)

    # 3-tier monastery roof — each tier slightly narrower
    base_y = sy - wall_height - 1
    for tier in range(3):
        tier_y = base_y - tier * 2
        shrink = tier
        for rx in range(left_x - 1 + shrink, left_x + width + 1 - shrink):
            if 0 <= tier_y < world.height and abs(rx) < world.width:
                world.set_block(rx, tier_y, MONASTERY_ROOF)
        fill_y = tier_y + 1
        for rx in range(left_x + shrink, left_x + width - shrink):
            if 0 <= fill_y < world.height and abs(rx) < world.width:
                world.set_block(rx, fill_y, MONASTERY_ROOF)

    # Prayer flags strung across the top
    flag_y = base_y - 7
    for fx in range(left_x, left_x + width):
        if 0 <= flag_y < world.height and abs(fx) < world.width:
            world.set_block(fx, flag_y, PRAYER_FLAG_BLOCK)


def _place_bridge(world, lx, rx, by):
    """Wooden plank bridge connecting two buildings."""
    for x in range(lx, rx):
        if 0 <= by < world.height:
            world.set_block(x, by, OAK_PANEL)
            world.set_bg_block(x, by, LADDER) # railing-like look


def _place_vignette(world, rng, left_x, sy, width, height, theme=None):
    """Small atmospheric scene: laundry, stalled carts, or construction."""
    if theme is None:
        theme = rng.choice(["laundry", "cart", "scaffold", "firewood"])
    
    if theme == "laundry":
        # Two posts with a clothesline
        for wy in range(sy - 3, sy):
            if 0 <= wy < world.height:
                world.set_block(left_x, wy, HOUSE_WALL_DARK)
                world.set_block(left_x + width - 1, wy, HOUSE_WALL_DARK)
        line_y = sy - 3
        if 0 <= line_y < world.height:
            for wx in range(left_x + 1, left_x + width - 1):
                world.set_bg_block(wx, line_y, WOVEN_TEXTILE)
                
    elif theme == "cart":
        # A supply cart (bg blocks) and some barrels
        mid_x = left_x + width // 2
        for wx in range(left_x, left_x + width):
            if 0 <= sy - 1 < world.height:
                world.set_bg_block(wx, sy - 1, HOUSE_WALL_DARK) # cart body
        if 0 <= sy - 1 < world.height:
            world.set_bg_block(left_x, sy - 1, COBBLESTONE) # wheel
            world.set_bg_block(left_x + width - 1, sy - 1, COBBLESTONE) # wheel
            _set_bg_furniture(world, mid_x, sy - 1, STORAGE_PITHOS)
            _set_bg_furniture(world, mid_x - 1, sy - 1, RAIN_BARREL)

    elif theme == "scaffold":
        # Construction site: ladder and some planks
        for wy in range(sy - height, sy):
            if 0 <= wy < world.height:
                world.set_block(left_x, wy, LADDER)
        for wx in range(left_x, left_x + width):
            if 0 <= sy - height // 2 < world.height:
                world.set_block(wx, sy - height // 2, HOUSE_WALL)
        _set_bg_furniture(world, left_x + 1, sy - 1, FIREWOOD_STACK)

    elif theme == "firewood":
        # Large stack of wood for the winter
        for wx in range(left_x, left_x + width):
            for wy in range(sy - 2, sy):
                _set_bg_furniture(world, wx, wy, FIREWOOD_STACK)


def _place_shrine_for_biome(world, left_x, sy, width, wall_height, biodome):
    _, style = RELIGION_BY_BIOME.get(biodome, ("Forest Chapel", "chapel"))
    if style == "dzong":
        _place_dzong(world, left_x, sy, width, wall_height)
    elif style == "chapel":
        _place_chapel(world, left_x, sy, width, wall_height)
    elif style == "desert_shrine":
        _place_desert_shrine(world, left_x, sy, width, wall_height)
    elif style == "jungle_shrine":
        _place_jungle_shrine(world, left_x, sy, width, wall_height)
    elif style == "standing_stones":
        _place_standing_stones(world, left_x, sy, width, wall_height)
    else:
        _place_temple(world, left_x, sy, width, wall_height)


_TRAVERSAL_THRESHOLD = 3   # height diff (blocks) below which no stairs are needed
_TRAVERSAL_MAX_STEPS = 25  # cap so extreme terrain doesn't create absurd staircases


def _ensure_city_traversal(world, city_bx, half_w, sy):
    """Guarantee the player can enter and exit the city on each side.

    Per-side logic:
      - City elevated above terrain → build a rising stone-supported ramp toward the city.
      - City below terrain (mountain wall) → carve a descending ramp through the hillside.
    Stair block direction is chosen so the ascending direction always uses a stair trigger.
    """
    def _side(edge_x, outward):
        # Sample the first terrain column outside the city edge.
        terrain_sy = world.surface_y_at(edge_x + outward)
        diff = terrain_sy - sy      # positive = terrain lower; negative = terrain higher
        if abs(diff) <= _TRAVERSAL_THRESHOLD:
            return
        steps = min(abs(diff), _TRAVERSAL_MAX_STEPS)

        far_x = edge_x + outward * (steps + 2)
        chunk_lo = min(edge_x, far_x) // CHUNK_W - 1
        chunk_hi = max(edge_x, far_x) // CHUNK_W + 1
        for c in range(chunk_lo, chunk_hi + 1):
            world.load_chunk(c)

        if diff > 0:
            # City is elevated: build a ramp rising toward the city.
            # Ascending direction = toward city, so use stair that triggers movement toward city.
            # Left side (outward=-1): player moves right toward city → STAIRS_RIGHT.
            # Right side (outward=+1): player moves left toward city → STAIRS_LEFT.
            stair_block = STAIRS_RIGHT if outward == -1 else STAIRS_LEFT
            for i in range(steps):
                sx      = edge_x + outward * (1 + i)
                stair_y = sy + i        # descends (y grows) as we step away from city
                world.set_block(sx, stair_y, stair_block)
                for h in range(1, 3):
                    if world.get_block(sx, stair_y - h) not in (AIR, BEDROCK):
                        world.set_block(sx, stair_y - h, AIR)
                for fill_y in range(stair_y + 1, terrain_sy + 1):
                    if world.get_block(sx, fill_y) == AIR:
                        world.set_block(sx, fill_y, STONE)
        else:
            # City is below terrain: carve a ramp through the hillside.
            # Ascending direction = away from city, so use stair that triggers movement away.
            # Left side (outward=-1): player exits left → STAIRS_LEFT.
            # Right side (outward=+1): player exits right → STAIRS_RIGHT.
            stair_block = STAIRS_LEFT if outward == -1 else STAIRS_RIGHT
            for i in range(steps):
                sx      = edge_x + outward * (1 + i)
                # Start at sy-1 (player row when at city floor) so the first stair fires.
                # Ascending outward; i=steps-1 lands at terrain_sy (mountain surface, cleared below).
                stair_y = sy - 1 - i
                world.set_block(sx, stair_y, stair_block)
                for h in range(1, 3):
                    if world.get_block(sx, stair_y - h) not in (AIR, BEDROCK):
                        world.set_block(sx, stair_y - h, AIR)
                # No fill needed — mountain stone below is already solid.

    _side(city_bx - half_w, -1)   # left exit
    _side(city_bx + half_w, +1)   # right exit


def _build_single_city(world, rng, city_bx, difficulty):
    sy = world.surface_y_at(city_bx)
    biodome = world.biodome_at(city_bx)
    # town_id is the index this city will occupy in world.town_centers (appended after return)
    _current_town_id = len(getattr(world, "town_centers", []))
    _entities_before = len(world.entities)
    if biodome in _SIZE_BY_BIOME:
        city_size = rng.choice(_SIZE_BY_BIOME[biodome])
    else:
        city_size = rng.choice(_SIZE_BY_DIFFICULTY[difficulty])
    # Frontier biomes have a 30% chance to spawn as a military garrison instead
    if biodome in _FRONTIER_BIOMES and city_size in ("medium", "large") and rng.random() < 0.30:
        city_size = "military"
    cfg = CITY_CONFIGS[city_size]
    half_w = cfg["half_w"]

    is_arabia        = biodome in _ARABIA_BIOMES
    is_desert        = biodome in _DESERT_BIOMES
    is_himalayan     = biodome in _HIMALAYAN_BIOMES
    is_mediterranean = biodome in _MEDITERRANEAN_BIOMES
    is_east_asian    = biodome in _EAST_ASIAN_BIOMES
    is_south_asian   = biodome in _SOUTH_ASIAN_BIOMES
    restaurant_style = _RESTAURANT_STYLE_BY_BIOME.get(biodome, "default")

    buildings_list = list(cfg["buildings"])
    npc_types_list = list(cfg["npc_types"])
    # Ensure npc_types_list is at least as long as buildings_list
    while len(npc_types_list) < len(buildings_list):
        npc_types_list.append("villager")

    # Separate slots into buildings and outdoor NPCs
    b_indices = [i for i, b in enumerate(buildings_list) if b[1] is not None]
    o_indices = [i for i, b in enumerate(buildings_list) if b[1] is None]

    # Build pools from the config data
    b_pool = []
    for i, nt in enumerate(npc_types_list):
        if i < len(buildings_list) and i in b_indices:
            b_pool.append((buildings_list[i][3], nt))
        elif i >= len(buildings_list):
            b_pool.append((["house", "two_story", "tower"], nt))
    b_pool.append((["house", "two_story", "three_story", "tower"], "villager"))
    b_pool.append((["house", "two_story", "three_story"], "villager"))

    o_pool = [npc_types_list[i] for i in o_indices]
    o_pool.append("villager")
    o_pool.append("none")

    # 1. Collect all layout items
    layout_items = []
    for _ in b_indices:
        v_pool, n_type = rng.choice(b_pool)
        w_range = (4, 6) # Default
        h_range = (3, 5) # Default
        # Try to find matching ranges from the config to stay somewhat balanced
        if buildings_list:
            match = rng.choice(buildings_list)
            if match[1]: w_range, h_range = match[1], match[2]
        
        layout_items.append({
            "type": "building",
            "variants": v_pool,
            "npc_type": n_type,
            "w_range": w_range,
            "h_range": h_range,
            "width": rng.randint(*w_range)
        })

    for _ in o_indices:
        layout_items.append({
            "type": "outdoor",
            "npc_type": rng.choice(o_pool),
            "width": 1
        })

    for _, half in cfg.get("squares", ()):
        layout_items.append({
            "type": "square",
            "half": half,
            "width": half * 2 + 1
        })

    for _, half in cfg.get("gardens", ()):
        layout_items.append({
            "type": "garden",
            "half": half,
            "width": half * 2 + 1
        })

    # Shuffle the items to create a unique town layout every time
    rng.shuffle(layout_items)

    # 2. Pack items and calculate the actual width needed
    total_width = 0
    gaps = []
    for i in range(len(layout_items)):
        gap = rng.randint(1, 2) if i < len(layout_items) - 1 else 0
        gaps.append(gap)
        total_width += layout_items[i]["width"] + gap

    half_w = (total_width // 2) + 1

    world.city_zones.append((city_bx - half_w, city_bx + half_w))

    # Pre-load every chunk the city footprint + farm strips touch
    chunk_lo = (city_bx - half_w - 20) // CHUNK_W
    chunk_hi = (city_bx + half_w + 20) // CHUNK_W
    for c_idx in range(chunk_lo, chunk_hi + 1):
        world.load_chunk(c_idx)

    for bx in range(city_bx - half_w - 2, city_bx + half_w + 3):
        for by in range(max(0, sy - 35), sy):
            if world.get_block(bx, by) in _PLANT_BLOCKS:
                world.set_block(bx, by, AIR)

    # Flatten terrain across the city footprint to sy
    for bx in range(city_bx - half_w, city_bx + half_w + 1):
        col_sy = world.surface_y_at(bx)
        # Hill: remove blocks above city floor
        for by in range(col_sy, sy):
            blk = world.get_block(bx, by)
            if blk not in (AIR, BEDROCK):
                world.set_block(bx, by, AIR)
        # Valley: fill gaps below city floor with stone
        for by in range(sy, col_sy + 1):
            if world.get_block(bx, by) == AIR:
                world.set_block(bx, by, STONE)

    for bx in range(city_bx - half_w, city_bx + half_w + 1):
        if world.get_block(bx, sy) != BEDROCK:
            world.set_block(bx, sy, STONE)

    # 3. Place items sequentially
    current_x = city_bx - half_w + 1
    prev_right_x = None
    prev_height = None

    for i, item in enumerate(layout_items):
        left_x = current_x
        width  = item["width"]
        
        if item["type"] == "building":
            height  = rng.randint(*item["h_range"])
            variants = item["variants"]
            npc_type = item["npc_type"]
            
            # Palette selection
            if is_arabia:
                wall_block, roof_block = _ARABIA_PALETTE
                if variants: variants = [_ARABIA_SWAP.get(v, v) for v in variants]
            elif is_desert:
                wall_block, roof_block = _DESERT_PALETTE
                if variants: variants = [_DOME_SWAP.get(v, v) for v in variants]
            elif is_himalayan:
                wall_block, roof_block = _HIMALAYAN_PALETTE
                if variants: variants = [_HIMALAYAN_SWAP.get(v, v) for v in variants]
            elif is_mediterranean:
                wall_block, roof_block = rng.choice(_MEDITERRANEAN_PALETTES)
            elif is_east_asian:
                wall_block, roof_block = _EAST_ASIAN_PALETTE
                if variants: variants = [_EAST_ASIAN_SWAP.get(v, v) for v in variants]
            elif is_south_asian:
                wall_block, roof_block = rng.choice(_SOUTH_ASIAN_PALETTES)
            else:
                wall_block, roof_block = rng.choice(BUILDING_PALETTES)

            variant = rng.choice(variants) if variants else "house"

            if variant == "tent":
                _place_bedouin_tent(world, left_x, sy, width, height, rng)
            elif variant == "caravanserai":
                _place_caravanserai(world, left_x, sy, width, height)
            elif variant == "dome":
                _place_dome_house(world, left_x, sy, width, height, wall_block)
            elif variant == "himalayan":
                _place_himalayan_house(world, left_x, sy, width, height)
            elif variant == "two_story":
                floor2_h = rng.randint(2, 3)
                _place_house_two_story(world, left_x, sy, width, height, floor2_h,
                                       wall_block, roof_block, rng)
            elif variant == "three_story":
                floor2_h = rng.randint(2, 3)
                floor3_h = rng.randint(2, 3)
                _place_house_three_story(world, rng, left_x, sy, width, height,
                                         floor2_h, floor3_h, wall_block, roof_block)
            elif variant == "restaurant":
                _place_restaurant(world, left_x, sy, width, height, restaurant_style)
            elif variant == "shrine":
                _place_shrine_for_biome(world, left_x, sy, width, height, biodome)
            elif variant == "tower":
                _place_tower(world, left_x, sy, width, height, wall_block, roof_block)
            elif variant == "longhouse":
                _place_longhouse(world, left_x, sy, width, height, wall_block, roof_block, rng)
            elif variant == "ruin":
                _place_ruin(world, left_x, sy, width, height)
            elif variant == "market_stall":
                _place_market_stall(world, rng, left_x, sy, width, height)
            elif variant == "pavilion":
                _place_pavilion(world, left_x, sy, width, height, GARDEN_COLUMN, roof_block)
            elif variant == "well":
                _place_well(world, left_x, sy, width, height)
            elif variant == "inn":
                _place_inn(world, left_x, sy, width, height, rng)
            elif variant == "smithy":
                _place_smithy(world, left_x, sy, width, height, wall_block)
            elif variant == "apothecary":
                _place_apothecary(world, left_x, sy, width, height, rng)
            elif variant == "library":
                _place_library(world, left_x, sy, width, height, rng, wall_block, roof_block)
            elif variant == "barn":
                _place_barn(world, left_x, sy, width, height, rng)
            elif variant == "vignette":
                _place_vignette(world, rng, left_x, sy, width, height)
            elif variant == "hospital":
                _place_hospital(world, left_x, sy, width, height, rng)
            elif variant == "coffee_shop":
                _place_coffee_shop(world, left_x, sy, width, height, rng)
            elif variant == "wine_shop":
                _place_wine_shop(world, left_x, sy, width, height, rng)
            else:
                _place_house(world, left_x, sy, width, height, wall_block, roof_block, rng)

            # Bridge logic: occasionally connect buildings with roof bridges or clotheslines
            if prev_right_x is not None and prev_height is not None:
                gap = left_x - prev_right_x
                if 1 <= gap <= 3 and rng.random() < 0.5:
                    # Determine bridge height
                    low_h = min(height, prev_height)
                    if low_h >= 4:
                        bridge_y = sy - low_h + 1
                        _place_bridge(world, prev_right_x, left_x, bridge_y)
                    elif gap <= 2:
                        # Low-level clothesline
                        for bx in range(prev_right_x, left_x):
                            if 0 <= sy - 3 < world.height:
                                world.set_bg_block(bx, sy - 3, rng.choice([TAPESTRY_BLOCK, WOVEN_TEXTILE]))

            prev_right_x = left_x + width
            prev_height = height

            npc_bx = left_x + 1
            if variant in ("house", "two_story", "three_story", "longhouse", "tower"):
                _decorate_interior(world, rng, left_x, sy, width, npc_bx)
                _decorate_facade(world, rng, left_x, sy, width, height, wall_block)

        elif item["type"] == "square":
            _place_town_square(world, rng, left_x + item["half"], sy, biodome, item["half"])
            npc_bx, npc_type = left_x + item["half"], "none"
        elif item["type"] == "garden":
            _place_garden_plot(world, rng, left_x + item["half"], sy, biodome, item["half"])
            npc_bx, npc_type = left_x + item["half"], "none"
        else: # Outdoor
            npc_bx, npc_type = left_x, item["npc_type"]

        # Place the NPC assigned to this plot/building
        if isinstance(npc_type, (list, tuple)):
            npc_type = rng.choice(npc_type)

        if npc_type not in (None, "none"):
            npc_px = npc_bx * BLOCK_SIZE + (BLOCK_SIZE - NPC.NPC_W) // 2
            npc_py = (sy - 2) * BLOCK_SIZE
            if npc_type == "villager":
                world.entities.append(VillagerNPC(npc_px, npc_py, world, biodome=biodome))
            elif npc_type == "child":
                world.entities.append(ChildNPC(npc_px, npc_py, world, biodome=biodome))
            elif npc_type == "guard":
                world.entities.append(GuardNPC(npc_px, npc_py, world, biodome=biodome))
            elif npc_type == "elder":
                world.entities.append(ElderNPC(npc_px, npc_py, world, biodome=biodome))
            elif npc_type == "beggar":
                world.entities.append(BeggarNPC(npc_px, npc_py, world, biodome=biodome))
            elif npc_type == "noble":
                world.entities.append(NobleNPC(npc_px, npc_py, world, biodome=biodome))
            elif npc_type == "pilgrim":
                world.entities.append(PilgrimNPC(npc_px, npc_py, world, biodome=biodome))
            elif npc_type == "drunkard":
                world.entities.append(DrunkardNPC(npc_px, npc_py, world, biodome=biodome))
            elif npc_type == "quest_rock":
                world.entities.append(RockQuestNPC(npc_px, npc_py, world, rng, difficulty, biodome))
            elif npc_type == "trade":
                world.entities.append(TradeNPC(npc_px, npc_py, world, rng, biodome))
            elif npc_type == "quest_wildflower":
                world.entities.append(WildflowerQuestNPC(npc_px, npc_py, world, rng, difficulty, biodome))
            elif npc_type == "quest_gem":
                world.entities.append(GemQuestNPC(npc_px, npc_py, world, rng, difficulty, biodome))
            elif npc_type == "merchant":
                world.entities.append(MerchantNPC(npc_px, npc_py, world, rng, biodome))
            elif npc_type == "restaurant_npc":
                world.entities.append(RestaurantNPC(npc_px, npc_py, world, rng, biodome))
            elif npc_type == "shrine_npc":
                world.entities.append(ShrineKeeperNPC(npc_px, npc_py, world, rng, difficulty, biodome))
            elif npc_type == "jewelry_merchant":
                world.entities.append(JewelryMerchantNPC(npc_px, npc_py, world, rng, biodome))
            elif npc_type == "blacksmith":
                world.entities.append(BlacksmithNPC(npc_px, npc_py, world, rng, biodome))
            elif npc_type == "innkeeper":
                world.entities.append(InnkeeperNPC(npc_px, npc_py, world, rng, difficulty, biodome))
            elif npc_type == "scholar":
                world.entities.append(ScholarNPC(npc_px, npc_py, world, rng, biodome))
            elif npc_type == "weapon_armorer":
                world.entities.append(WeaponArmorerNPC(npc_px, npc_py, world, rng, biodome))
            elif npc_type == "quartermaster":
                world.entities.append(QuartermasterNPC(npc_px, npc_py, world, rng, biodome))
            elif npc_type == "garrison_commander":
                world.entities.append(GarrisonCommanderNPC(npc_px, npc_py, world, rng, difficulty, biodome))
            elif npc_type == "doctor":
                world.entities.append(DoctorNPC(npc_px, npc_py, world, biodome=biodome))
            elif npc_type == "coffee_merchant":
                world.entities.append(CoffeeMerchantNPC(npc_px, npc_py, world, rng, biodome=biodome))
            elif npc_type == "wine_merchant":
                world.entities.append(WineMerchantNPC(npc_px, npc_py, world, rng, biodome=biodome))
            elif npc_type == "beer_merchant":
                world.entities.append(BeerMerchantNPC(npc_px, npc_py, world, rng, biodome=biodome))
            elif npc_type == "tavern":
                world.entities.append(TavernkeeperNPC(npc_px, npc_py, world, rng, difficulty, biodome=biodome))
            elif npc_type == "musician":
                world.entities.append(MusicianNPC(npc_px, npc_py, world, biodome=biodome))
            elif npc_type == "town_crier":
                world.entities.append(TownCrierNPC(npc_px, npc_py, world, biodome=biodome))

        current_x += width + gaps[i]

    # Every city gets a flag at the city center.
    flag_y = sy - 1
    if 0 <= flag_y < world.height:
        world.set_bg_block(city_bx, flag_y, TOWN_FLAG_BLOCK)

    # 4. Final dynamic elements
    _ambient_npc_cls = {"villager": VillagerNPC, "child": ChildNPC, "guard": GuardNPC,
                        "elder": ElderNPC, "beggar": BeggarNPC, "noble": NobleNPC,
                        "pilgrim": PilgrimNPC, "drunkard": DrunkardNPC,
                        "musician": MusicianNPC, "town_crier": TownCrierNPC}
    
    # Ambient NPCs now roam randomly between the city walls
    for _, npc_type in cfg.get("ambient_npcs", ()):
        if isinstance(npc_type, (list, tuple)):
            npc_type = rng.choice(npc_type)
        cls = _ambient_npc_cls.get(npc_type)
        if cls is None: continue
        nx = (city_bx + rng.randint(-half_w + 1, half_w - 1)) * BLOCK_SIZE + (BLOCK_SIZE - NPC.NPC_W) // 2
        ny = (sy - 2) * BLOCK_SIZE
        world.entities.append(cls(nx, ny, world, biodome=biodome))

    # Restore old_half_w for farm offsets if needed, or just let farms be relative to new half_w
    # To keep the "Same thing" logic, let's use the new half_w for farm gap calculation.
    # The farm loop below already uses `half_w` (which I've updated).


    # Cobbled main street + lamps + entry gateposts wrap up the city.
    _pave_main_street(world, rng, city_bx - half_w, city_bx + half_w, sy)
    _place_streetlamps(world, rng, city_bx - half_w + 2,
                       city_bx + half_w - 2, sy)
    _place_city_walls(world, rng, city_bx - half_w, city_bx + half_w, sy,
                      biodome, city_size)
    _ensure_city_traversal(world, city_bx, half_w, sy)

    # Assign identity, preferences, and family links to all NPCs spawned for this city
    import npc_identity
    city_npcs = world.entities[_entities_before:]
    for idx, npc in enumerate(city_npcs):
        if hasattr(npc, "_setup_identity"):
            npc._setup_identity(_current_town_id, idx, world.seed)
    npc_identity.assign_families(
        [n for n in city_npcs if hasattr(n, "family_id")],
        _current_town_id,
        world.seed,
    )

    return city_size


def _castle_set(world, bx, by, bid):
    """Set a foreground block only if in-bounds."""
    if 0 <= by < world.height:
        world.set_block(bx, by, bid)


def _castle_bg(world, bx, by, bid):
    """Set a background block only if in-bounds."""
    if 0 <= by < world.height:
        world.set_bg_block(bx, by, bid)


def _castle_fill_bg(world, lx, rx, top_y, bot_y, bid):
    """Flood-fill a rectangle with background blocks."""
    for bx in range(lx, rx + 1):
        for by in range(top_y, bot_y + 1):
            if 0 <= by < world.height:
                world.set_bg_block(bx, by, bid)


def _castle_door(world, bx, sy, door_block=None):
    """Carve a 2-wide × 2-tall walkable archway at bx and bx+1."""
    for col in (bx, bx + 1):
        _castle_set(world, col, sy - 1, door_block if door_block else AIR)
        _castle_set(world, col, sy - 2, door_block if door_block else AIR)
        _castle_bg(world, col, sy - 1, CASTLE_GATE_ARCH)
        _castle_bg(world, col, sy - 2, CASTLE_GATE_ARCH)


def _build_round_tower(world, lx: int, sy: int, w: int, h: int, door_block=None):
    """A fully detailed corner tower: solid round-tower walls, mid-floor, corbels,
    machicolations, crenellations, conical cap, arrow slit, garderobe chute."""
    # Foundation
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy, CURTAIN_WALL)
    # Full-height outer walls
    for by in range(sy - h, sy):
        _castle_set(world, lx,      by, ROUND_TOWER_WALL)
        _castle_set(world, lx + w,  by, ROUND_TOWER_WALL)
    # Full interior background fill
    _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, ROUND_TOWER_WALL)
    # Door openings on both sides so players can flow through
    _castle_door(world, lx,         sy)   # left entrance
    _castle_door(world, lx + w - 1, sy)   # right exit
    # Mid-level interior floor
    mid_floor = sy - h // 2
    for bx in range(lx + 1, lx + w):
        _castle_set(world, bx, mid_floor, WALL_WALK_FLOOR)
    # Arrow slit + sconce on mid level
    tmid = lx + w // 2
    _castle_bg(world, tmid, mid_floor - 2, DUNGEON_GRATE)
    _castle_bg(world, tmid, mid_floor - 1, WALL_SCONCE)
    # Garderobe chute jutting from lower outer wall
    _castle_bg(world, lx,     sy - 4, GARDEROBE_CHUTE)
    # Corbel course just below parapet
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy - h + 1, CORBEL_COURSE)
    # Machicolations at parapet level
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy - h, MACHICOLATION)
    # Crenellations (alternating merlons)
    for bx in range(lx, lx + w + 1):
        if (bx - lx) % 2 == 0:
            _castle_set(world, bx, sy - h - 1, CRENELLATION)
    # Conical tower cap — pyramid of TOWER_CAP blocks
    for i, span in enumerate(range(w // 2 + 1, 0, -1)):
        cap_y = sy - h - 2 - i
        for bx in range(tmid - span + 1, tmid + span):
            _castle_set(world, bx, cap_y, TOWER_CAP)
    # Wall sconce inside at ground level
    _castle_bg(world, tmid, sy - 2, BRAZIER)


# ── Castle piece dimensions ────────────────────────────────────────────────
_CW_MOAT      = 4   # moat approach
_CW_ROUND_TOW = 6   # round tower
_CW_SQ_TOW    = 8   # square tower
_CW_GATEHOUSE = 7   # gatehouse
_CW_GREAT_HALL= 13  # great hall
_CW_GRAND_HALL= 15  # wide grand hall
_CW_KEEP      = 10  # standard keep
_CW_PAL_KEEP  = 12  # palace keep (wider)
_CW_CHAPEL    = 9   # chapel wing
_CW_BARRACKS  = 11  # barracks wing

_CH_ROUND_TOW = 17  # round tower height
_CH_SQ_TOW    = 14  # square tower height
_CH_WALL      = 11  # standard hall/wall height
_CH_KEEP      = 11  # keep height
_CH_PAL_KEEP  = 26  # palace keep height
_CH_CHAPEL    = 14  # chapel height


def _piece_moat(world, lx, sy, door_block=None):
    """Moat approach — drawbridge planks over damp stone flanks."""
    for bx in range(lx, lx + _CW_MOAT):
        _castle_set(world, bx, sy,     DRAWBRIDGE_PLANK)
        _castle_bg(world,  bx, sy,     DRAWBRIDGE_CHAIN)
        _castle_bg(world,  bx, sy - 1, MOAT_STONE)
        _castle_bg(world,  bx, sy - 2, MOAT_STONE)
    return _CW_MOAT


def _piece_round_tower(world, lx, sy, door_block=None):
    """Round tower with conical cap and gargoyle corners."""
    _build_round_tower(world, lx, sy, _CW_ROUND_TOW, _CH_ROUND_TOW)
    _castle_bg(world, lx,                sy - _CH_ROUND_TOW - 1, GARGOYLE_BLOCK)
    _castle_bg(world, lx + _CW_ROUND_TOW, sy - _CH_ROUND_TOW - 1, GARGOYLE_BLOCK)
    return _CW_ROUND_TOW


def _piece_square_tower(world, lx, sy, door_block=None):
    """Square keep-tower: flat battlements, arrow slits, two interior floors."""
    w, h = _CW_SQ_TOW, _CH_SQ_TOW
    cx = lx + w // 2
    _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, CURTAIN_WALL)
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy, CURTAIN_WALL)
    for by in range(sy - h, sy):
        _castle_set(world, lx,     by, CURTAIN_WALL)
        _castle_set(world, lx + w, by, CURTAIN_WALL)
    _castle_door(world, lx,         sy)
    _castle_door(world, lx + w - 1, sy)
    mid = sy - h // 2
    for bx in range(lx + 1, lx + w):
        _castle_set(world, bx, mid, WALL_WALK_FLOOR)
    _castle_bg(world, lx,     mid - 2, DUNGEON_GRATE)
    _castle_bg(world, lx + w, mid - 2, DUNGEON_GRATE)
    _castle_bg(world, cx, mid - 1, WALL_SCONCE)
    _castle_bg(world, cx, sy  - 3, BRAZIER)
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy - h + 1, CORBEL_COURSE)
        _castle_set(world, bx, sy - h,     MACHICOLATION)
        if (bx - lx) % 2 == 0:
            _castle_set(world, bx, sy - h - 1, CRENELLATION)
    _castle_bg(world, lx,     sy - h - 1, GARGOYLE_BLOCK)
    _castle_bg(world, lx + w, sy - h - 1, GARGOYLE_BLOCK)
    return w


def _piece_gatehouse(world, lx, sy, door_block=None):
    """Gatehouse with portcullis, murder holes, and battlements."""
    w, h = _CW_GATEHOUSE, _CH_WALL
    cx = lx + w // 2
    _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, CURTAIN_WALL)
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy, CURTAIN_WALL)
    for by in range(sy - h, sy):
        _castle_set(world, lx,     by, CURTAIN_WALL)
        _castle_set(world, lx + w, by, CURTAIN_WALL)
    for by in range(sy - 3, sy):
        _castle_bg(world, cx,     by, CASTLE_GATE_ARCH)
        _castle_bg(world, cx - 1, by, CASTLE_GATE_ARCH)
    _castle_bg(world, cx,     sy - 4, PORTCULLIS_BLOCK)
    _castle_bg(world, cx - 1, sy - 4, PORTCULLIS_BLOCK)
    _castle_bg(world, lx + 1,     sy - 2, DRAWBRIDGE_CHAIN)
    _castle_bg(world, lx + w - 1, sy - 2, DRAWBRIDGE_CHAIN)
    _castle_bg(world, lx + 1,     sy - 4, DRAWBRIDGE_CHAIN)
    _castle_bg(world, lx + w - 1, sy - 4, DRAWBRIDGE_CHAIN)
    for bx in range(lx + 1, lx + w):
        _castle_set(world, bx, sy - 5, MURDER_HOLE)
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy - h + 1, CORBEL_COURSE)
        _castle_set(world, bx, sy - h,     MACHICOLATION)
        _castle_set(world, bx, sy - h - 1, CRENELLATION)
    return w


def _piece_great_hall(world, lx, sy, door_block=None):
    """Great hall with central fireplace, chandeliers, and heraldic panels."""
    w, h = _CW_GREAT_HALL, _CH_WALL
    cx = lx + w // 2
    _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, CURTAIN_WALL)
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy, GREAT_HALL_FLOOR)
    for by in range(sy - h, sy):
        _castle_set(world, lx, by, CURTAIN_WALL)
    for bx in range(lx + 1, lx + w):
        _castle_set(world, bx, sy - h + 1, WALL_WALK_FLOOR)
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy - h,     CURTAIN_WALL)
        _castle_set(world, bx, sy - h - 1, CORBEL_COURSE)
        if bx % 2 == 0:
            _castle_set(world, bx, sy - h - 2, CRENELLATION)
        else:
            _castle_set(world, bx, sy - h - 2, MACHICOLATION)
    _castle_bg(world, cx, sy - 1, CASTLE_FIREPLACE)
    _castle_bg(world, cx, sy - 2, CASTLE_FIREPLACE)
    _castle_bg(world, cx, sy - 3, HERALDIC_PANEL)
    _castle_bg(world, cx, sy - 4, HERALDIC_PANEL)
    _castle_bg(world, cx - 2, sy - 1, HERALDIC_PANEL)
    _castle_bg(world, cx + 2, sy - 1, HERALDIC_PANEL)
    _castle_bg(world, cx - 3, sy - 2, BRONZE_SHIELD_MOUNT)
    _castle_bg(world, cx + 3, sy - 2, BRONZE_SHIELD_MOUNT)
    _castle_bg(world, cx - 4, sy - h + 2, CHANDELIER)
    _castle_bg(world, cx,     sy - h + 2, CHANDELIER)
    _castle_bg(world, cx + 4, sy - h + 2, CHANDELIER)
    _castle_bg(world, lx + 2,     sy - 5, WALL_SCONCE)
    _castle_bg(world, lx + w - 2, sy - 5, WALL_SCONCE)
    _castle_bg(world, cx - 5, sy - 1, CANDELABRA)
    _castle_bg(world, cx + 5, sy - 1, CANDELABRA)
    _castle_bg(world, lx + 1,     sy - 1, VICTORY_STELE)
    _castle_bg(world, lx + w - 1, sy - 1, VICTORY_STELE)
    _castle_bg(world, lx + 3,     sy - 2, PHILOSOPHERS_SCROLL)
    _castle_bg(world, lx + w - 3, sy - 2, PHILOSOPHERS_SCROLL)
    for bx in range(lx + 2, lx + w, 3):
        _castle_bg(world, bx, sy - h + 2, CORBEL_COURSE)
    return w


def _piece_grand_hall(world, lx, sy, door_block=None):
    """Wide grand hall with twin fireplaces and extra opulence."""
    w, h = _CW_GRAND_HALL, _CH_WALL
    t1 = lx + w // 3
    t2 = lx + 2 * w // 3
    cx = lx + w // 2
    _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, CURTAIN_WALL)
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy, GREAT_HALL_FLOOR)
    for by in range(sy - h, sy):
        _castle_set(world, lx, by, CURTAIN_WALL)
    for bx in range(lx + 1, lx + w):
        _castle_set(world, bx, sy - h + 1, WALL_WALK_FLOOR)
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy - h,     CURTAIN_WALL)
        _castle_set(world, bx, sy - h - 1, CORBEL_COURSE)
        if bx % 2 == 0:
            _castle_set(world, bx, sy - h - 2, CRENELLATION)
        else:
            _castle_set(world, bx, sy - h - 2, MACHICOLATION)
    for fc in (t1, t2):
        _castle_bg(world, fc, sy - 1, CASTLE_FIREPLACE)
        _castle_bg(world, fc, sy - 2, CASTLE_FIREPLACE)
        _castle_bg(world, fc, sy - 3, HERALDIC_PANEL)
        _castle_bg(world, fc, sy - 4, HERALDIC_PANEL)
    _castle_bg(world, cx, sy - 1, HERALDIC_PANEL)
    _castle_bg(world, cx, sy - 2, HERALDIC_PANEL)
    _castle_bg(world, t1 - 2, sy - 2, BRONZE_SHIELD_MOUNT)
    _castle_bg(world, t2 + 2, sy - 2, BRONZE_SHIELD_MOUNT)
    _castle_bg(world, cx - 1, sy - 1, BRONZE_SHIELD_MOUNT)
    _castle_bg(world, cx + 1, sy - 1, BRONZE_SHIELD_MOUNT)
    for ch_x in (lx + 2, t1 + 1, t2 - 1, lx + w - 2):
        _castle_bg(world, ch_x, sy - h + 2, CHANDELIER)
    _castle_bg(world, t1 - 1, sy - 1, CANDELABRA)
    _castle_bg(world, t2 + 1, sy - 1, CANDELABRA)
    _castle_bg(world, lx + 2,     sy - 5, WALL_SCONCE)
    _castle_bg(world, lx + w - 2, sy - 5, WALL_SCONCE)
    _castle_bg(world, lx + 1,     sy - 1, VICTORY_STELE)
    _castle_bg(world, lx + w - 1, sy - 1, VICTORY_STELE)
    _castle_bg(world, lx + 4,     sy - 2, PHILOSOPHERS_SCROLL)
    _castle_bg(world, lx + w - 4, sy - 2, PHILOSOPHERS_SCROLL)
    return w


def _piece_keep(world, lx, sy, door_block=None):
    """Central keep — throne room, mezzanine, tallest structure."""
    w, h = _CW_KEEP, _CH_KEEP
    cx  = lx + w // 2
    mez = sy - h // 2
    _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, ROUND_TOWER_WALL)
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy, CURTAIN_WALL)
    for bx in range(lx + 1, lx + w):
        _castle_set(world, bx, sy, PALACE_FLOOR_TILE)
    for by in range(sy - h, sy):
        _castle_set(world, lx,     by, ROUND_TOWER_WALL)
        _castle_set(world, lx + w, by, ROUND_TOWER_WALL)
    for by in range(sy - h + 1, sy):
        _castle_bg(world, lx + 1,     by, CURTAIN_WALL)
        _castle_bg(world, lx + w - 1, by, CURTAIN_WALL)
    for bx in range(lx + 1, lx + w):
        _castle_set(world, bx, mez, GREAT_HALL_FLOOR)
    for col in (cx - 1, cx):
        _castle_set(world, col, sy - 1, door_block if door_block else AIR)
        _castle_set(world, col, sy - 2, door_block if door_block else AIR)
        _castle_bg(world,  col, sy - 1, PALACE_PORTAL)
    _castle_bg(world, cx, sy - 3, HERALDIC_PANEL)
    _castle_bg(world, cx, sy - 4, HERALDIC_PANEL)
    _castle_bg(world, cx, sy - 5, HERALDIC_PANEL)
    _castle_bg(world, cx - 1, sy - 3, CASTLE_FIREPLACE)
    _castle_bg(world, cx + 1, sy - 3, CASTLE_FIREPLACE)
    _castle_bg(world, cx - 2, sy - 1, CANDELABRA)
    _castle_bg(world, cx + 2, sy - 1, CANDELABRA)
    _castle_bg(world, cx - 3, sy - 1, BRONZE_SHIELD_MOUNT)
    _castle_bg(world, cx + 3, sy - 1, BRONZE_SHIELD_MOUNT)
    _castle_bg(world, cx - 2, sy - _CH_WALL + 1, CHANDELIER)
    _castle_bg(world, cx + 2, sy - _CH_WALL + 1, CHANDELIER)
    _castle_bg(world, cx - 1, mez - 2, LANTERN_ORB)
    _castle_bg(world, cx + 1, mez - 2, LANTERN_ORB)
    _castle_bg(world, cx,     mez - 3, HERALDIC_PANEL)
    _castle_bg(world, lx + 2,     sy - 6, WALL_SCONCE)
    _castle_bg(world, lx + w - 2, sy - 6, WALL_SCONCE)
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy - h + 1, CORBEL_COURSE)
        _castle_set(world, bx, sy - h,     MACHICOLATION)
        _castle_set(world, bx, sy - h - 1, CRENELLATION)
    _castle_bg(world, lx,     sy - h - 1, GARGOYLE_BLOCK)
    _castle_bg(world, lx + w, sy - h - 1, GARGOYLE_BLOCK)
    _castle_set(world, lx,     sy - _CH_WALL - 1, PALAZZO_BALCONY)
    _castle_set(world, lx + w, sy - _CH_WALL - 1, PALAZZO_BALCONY)
    _castle_bg(world, cx, sy - h + 3, STAR_LAMP)
    _castle_bg(world, cx, mez - 4,    HERALDIC_PANEL)
    return w


def _piece_palace_keep(world, lx, sy, door_block=None):
    """Grand palace keep — wider, taller, three-level throne complex."""
    w, h   = _CW_PAL_KEEP, _CH_PAL_KEEP
    cx     = lx + w // 2
    low_mez = sy - h // 3
    hi_mez  = sy - 2 * h // 3
    _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, ROUND_TOWER_WALL)
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy, CURTAIN_WALL)
    for bx in range(lx + 1, lx + w):
        _castle_set(world, bx, sy, PALACE_FLOOR_TILE)
    for by in range(sy - h, sy):
        _castle_set(world, lx,     by, ROUND_TOWER_WALL)
        _castle_set(world, lx + w, by, ROUND_TOWER_WALL)
    for by in range(sy - h + 1, sy):
        _castle_bg(world, lx + 1,     by, CURTAIN_WALL)
        _castle_bg(world, lx + w - 1, by, CURTAIN_WALL)
    for bx in range(lx + 1, lx + w):
        _castle_set(world, bx, low_mez, GREAT_HALL_FLOOR)
        _castle_set(world, bx, hi_mez,  WALL_WALK_FLOOR)
    for col in (cx - 1, cx, cx + 1):
        _castle_set(world, col, sy - 1, door_block if door_block else AIR)
        _castle_set(world, col, sy - 2, door_block if door_block else AIR)
        _castle_bg(world,  col, sy - 1, PALACE_PORTAL)
    _castle_bg(world, cx, sy - 3, HERALDIC_PANEL)
    _castle_bg(world, cx, sy - 4, HERALDIC_PANEL)
    _castle_bg(world, cx, sy - 5, HERALDIC_PANEL)
    _castle_bg(world, cx, sy - 6, HERALDIC_PANEL)
    _castle_bg(world, cx - 2, sy - 3, CASTLE_FIREPLACE)
    _castle_bg(world, cx + 2, sy - 3, CASTLE_FIREPLACE)
    _castle_bg(world, cx - 3, sy - 1, CANDELABRA)
    _castle_bg(world, cx + 3, sy - 1, CANDELABRA)
    _castle_bg(world, cx - 4, sy - 1, BRONZE_SHIELD_MOUNT)
    _castle_bg(world, cx + 4, sy - 1, BRONZE_SHIELD_MOUNT)
    _castle_bg(world, cx - 1, low_mez - 2, LANTERN_ORB)
    _castle_bg(world, cx + 1, low_mez - 2, LANTERN_ORB)
    _castle_bg(world, cx,     low_mez - 3, HERALDIC_PANEL)
    _castle_bg(world, cx - 3, low_mez - 1, CHANDELIER)
    _castle_bg(world, cx + 3, low_mez - 1, CHANDELIER)
    _castle_bg(world, cx, hi_mez - 2, STAR_LAMP)
    _castle_bg(world, cx, hi_mez - 3, HERALDIC_PANEL)
    _castle_bg(world, lx + 2,     sy - 7,       WALL_SCONCE)
    _castle_bg(world, lx + w - 2, sy - 7,       WALL_SCONCE)
    _castle_bg(world, lx + 2,     low_mez - 4,  WALL_SCONCE)
    _castle_bg(world, lx + w - 2, low_mez - 4,  WALL_SCONCE)
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy - h + 1, CORBEL_COURSE)
        _castle_set(world, bx, sy - h,     MACHICOLATION)
        _castle_set(world, bx, sy - h - 1, CRENELLATION)
    _castle_bg(world, lx,     sy - h - 1, GARGOYLE_BLOCK)
    _castle_bg(world, lx + w, sy - h - 1, GARGOYLE_BLOCK)
    _castle_set(world, lx,     sy - _CH_WALL - 1, PALAZZO_BALCONY)
    _castle_set(world, lx + w, sy - _CH_WALL - 1, PALAZZO_BALCONY)
    return w


def _piece_chapel(world, lx, sy, door_block=None):
    """Gothic chapel wing with tracery, lancet windows, and rose window."""
    w, h = _CW_CHAPEL, _CH_CHAPEL
    cx = lx + w // 2
    _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, CHAPEL_STONE)
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy, GREAT_HALL_FLOOR)
    for by in range(sy - h, sy):
        _castle_set(world, lx,     by, CHAPEL_STONE)
        _castle_set(world, lx + w, by, CHAPEL_STONE)
    for by in range(sy - h + 2, sy - 2):
        _castle_bg(world, cx - 1, by, GOTHIC_TRACERY)
        _castle_bg(world, cx + 1, by, GOTHIC_TRACERY)
        _castle_bg(world, cx,     by, CHAPEL_STONE)
    _castle_bg(world, cx,     sy - h + 1, ROSE_WINDOW)
    _castle_bg(world, cx - 1, sy - h + 2, GOTHIC_TRACERY)
    _castle_bg(world, cx + 1, sy - h + 2, GOTHIC_TRACERY)
    for by in range(sy - 5, sy - 2):
        _castle_bg(world, lx + 2,     by, LANCET_WINDOW)
        _castle_bg(world, lx + w - 2, by, LANCET_WINDOW)
    _castle_bg(world, cx,     sy - 1, CHAPEL_STONE)
    _castle_bg(world, cx,     sy - 2, CHAPEL_STONE)
    _castle_bg(world, cx - 2, sy - 1, CANDELABRA)
    _castle_bg(world, cx + 2, sy - 1, CANDELABRA)
    _castle_bg(world, cx - 3, sy - 3, WALL_SCONCE)
    _castle_bg(world, cx + 3, sy - 3, WALL_SCONCE)
    _castle_bg(world, cx,     sy - h + 4, CHANDELIER)
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy - h, CHAPEL_STONE)
        if (bx - lx) % 2 == 0:
            _castle_set(world, bx, sy - h - 1, CRENELLATION)
        else:
            _castle_bg(world, bx, sy - h - 1, GOTHIC_TRACERY)
    return w


def _piece_barracks(world, lx, sy, door_block=None):
    """Military barracks wing — rough stone, weapon racks, soldier quarters."""
    w, h = _CW_BARRACKS, _CH_WALL
    cx = lx + w // 2
    _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, DUNGEON_WALL)
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy, CURTAIN_WALL)
    for by in range(sy - h, sy):
        _castle_set(world, lx,     by, CURTAIN_WALL)
        _castle_set(world, lx + w, by, CURTAIN_WALL)
    for bx in range(lx + 1, lx + w):
        _castle_set(world, bx, sy - h + 1, WALL_WALK_FLOOR)
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy - h,     CURTAIN_WALL)
        _castle_set(world, bx, sy - h - 1, CORBEL_COURSE)
        if bx % 2 == 0:
            _castle_set(world, bx, sy - h - 2, CRENELLATION)
        else:
            _castle_set(world, bx, sy - h - 2, MACHICOLATION)
    for off in range(1, w, 2):
        _castle_bg(world, lx + off, sy - 2, BRONZE_SHIELD_MOUNT)
    _castle_bg(world, cx - 2, sy - 1, DUNGEON_GRATE)
    _castle_bg(world, cx + 2, sy - 1, DUNGEON_GRATE)
    _castle_bg(world, cx,     sy - 1, VICTORY_STELE)
    _castle_bg(world, lx + 2,     sy - 5, WALL_SCONCE)
    _castle_bg(world, lx + w - 2, sy - 5, WALL_SCONCE)
    _castle_bg(world, cx - 4, sy - 1, BRAZIER)
    _castle_bg(world, cx + 4, sy - 1, BRAZIER)
    return w


# Piece width lookup (defined after all piece functions)
_PIECE_W = None  # lazy-initialised on first _place_castle call


def _get_piece_w():
    global _PIECE_W
    if _PIECE_W is None:
        _PIECE_W = {
            _piece_moat:         _CW_MOAT,
            _piece_round_tower:  _CW_ROUND_TOW,
            _piece_square_tower: _CW_SQ_TOW,
            _piece_gatehouse:    _CW_GATEHOUSE,
            _piece_great_hall:   _CW_GREAT_HALL,
            _piece_grand_hall:   _CW_GRAND_HALL,
            _piece_keep:         _CW_KEEP,
            _piece_palace_keep:  _CW_PAL_KEEP,
            _piece_chapel:       _CW_CHAPEL,
            _piece_barracks:     _CW_BARRACKS,
        }
    return _PIECE_W


# Castle layout templates — each is a sequence of piece functions
def _castle_templates():
    return [
        # 0 — Classic fortress (original layout)
        [_piece_moat, _piece_round_tower, _piece_gatehouse, _piece_great_hall,
         _piece_keep, _piece_chapel, _piece_round_tower, _piece_moat],
        # 1 — Grand palace: enter through hall, no gatehouse, palace keep
        [_piece_moat, _piece_square_tower, _piece_grand_hall,
         _piece_palace_keep, _piece_chapel, _piece_square_tower, _piece_moat],
        # 2 — War citadel: barracks flanking the keep, military feel
        [_piece_moat, _piece_round_tower, _piece_gatehouse, _piece_barracks,
         _piece_keep, _piece_barracks, _piece_round_tower, _piece_moat],
        # 3 — Manor keep: grand hall west, palace keep east, no chapel
        [_piece_moat, _piece_square_tower, _piece_gatehouse, _piece_grand_hall,
         _piece_palace_keep, _piece_round_tower, _piece_moat],
    ]


def _place_castle(world, left_x: int, sy: int):
    """Assemble a castle from modular pieces — 4 different layouts."""
    _DOOR = STUDDED_OAK_DOOR_CLOSED
    rng     = random.Random(left_x ^ (world.seed * 0x9E3779B9) ^ 0xC4571E)
    pieces  = rng.choice(_castle_templates())
    pw      = _get_piece_w()
    total_w = sum(pw[p] for p in pieces)
    for cx in range((left_x - 4) // CHUNK_W,
                    (left_x + total_w + 4) // CHUNK_W + 1):
        world.load_chunk(cx)
    max_h = _CH_PAL_KEEP + 6
    for bx in range(left_x - 2, left_x + total_w + 3):
        for by in range(sy - max_h, sy):
            if world.get_block(bx, by) not in (AIR, BEDROCK):
                world.set_block(bx, by, AIR)
    for bx in range(left_x, left_x + total_w + 1):
        col_sy = world.surface_y_at(bx)
        for by in range(col_sy, sy):
            if world.get_block(bx, by) not in (AIR, BEDROCK):
                world.set_block(bx, by, AIR)
        for by in range(sy, col_sy + 1):
            if world.get_block(bx, by) == AIR:
                world.set_block(bx, by, STONE)
    sections = []
    x = left_x
    for piece_fn in pieces:
        sections.append((piece_fn, x))
        x += piece_fn(world, x, sy, door_block=_DOOR)
    for i in range(1, len(sections)):
        prev_fn, _  = sections[i - 1]
        this_fn, lx = sections[i]
        if prev_fn is _piece_moat and this_fn is not _piece_moat:
            _castle_door(world, lx, sy, door_block=_DOOR)
        elif prev_fn is not _piece_moat and this_fn is _piece_moat:
            _castle_door(world, lx, sy, door_block=_DOOR)
        elif prev_fn is not _piece_moat:
            _castle_door(world, lx - 1, sy, door_block=_DOOR)
    return total_w


_CASTLE_GARDEN_THEMES = ("formal", "topiary_zoo", "fountain_plaza", "english_park", "monastic")


def _place_castle_garden(world, left_x: int, sy: int, rng: random.Random, biodome: str):
    """Walled pleasure garden to the right of a castle — paved court, topiary, fountain."""
    W = 12

    # Flatten and pave the garden plot
    for bx in range(left_x, left_x + W):
        col_sy = world.surface_y_at(bx)
        for by in range(col_sy, sy):
            if world.get_block(bx, by) not in (AIR, BEDROCK):
                world.set_block(bx, by, AIR)
        for by in range(sy, col_sy + 1):
            if world.get_block(bx, by) == AIR:
                world.set_block(bx, by, STONE)
        _castle_set(world, bx, sy, STONE)

    # Low crenellated garden wall on the outer sides
    for side_x in (left_x, left_x + W - 1):
        _castle_set(world, side_x, sy - 1, CURTAIN_WALL)
        _castle_set(world, side_x, sy - 2, CRENELLATION)

    # Pick a castle-appropriate garden theme, biased toward the biome's own pool
    biome_pool = _GARDEN_THEMES_BY_BIOME.get(biodome, [])
    themed = [t for t in biome_pool if t in _CASTLE_GARDEN_THEMES]
    theme_name = rng.choice(themed if themed else list(_CASTLE_GARDEN_THEMES))
    blocks = GARDEN_THEMES[theme_name]

    # Fountain centrepiece
    cx = left_x + W // 2
    _castle_bg(world, cx, sy - 1, rng.choice(_FOUNTAIN_BLOCKS))

    # Garden decoration across the inner row — bg only so the court stays walkable
    inner = list(range(left_x + 1, left_x + W - 1))
    inner.remove(cx)
    for i, bx in enumerate(inner):
        _castle_bg(world, bx, sy - 1, blocks[i % len(blocks)])


def _palace_clear_terrain(world, left_x: int, sy: int, total_w: int, max_h: int):
    """Shared terrain prep for all cultural palaces."""
    for cx in range((left_x - 2) // CHUNK_W, (left_x + total_w + 4) // CHUNK_W + 1):
        world.load_chunk(cx)
    for bx in range(left_x - 1, left_x + total_w + 2):
        for by in range(sy - max_h, sy):
            if world.get_block(bx, by) not in (AIR, BEDROCK):
                world.set_block(bx, by, AIR)
    for bx in range(left_x, left_x + total_w + 1):
        col_sy = world.surface_y_at(bx)
        for by in range(col_sy, sy):
            if world.get_block(bx, by) not in (AIR, BEDROCK):
                world.set_block(bx, by, AIR)
        for by in range(sy, col_sy + 1):
            if world.get_block(bx, by) == AIR:
                world.set_block(bx, by, STONE)


def _palace_npc_at(world, bx, sy, npc_cls, *args, **kwargs):
    """Spawn an NPC centred on block bx, standing on floor row sy."""
    px = bx * BLOCK_SIZE + (BLOCK_SIZE - NPC.NPC_W) // 2
    py = (sy - 2) * BLOCK_SIZE
    world.entities.append(npc_cls(px, py, world, *args, **kwargs))


# Block-offset from palace left_x to throne centre — used by _place_capital_structures.
PALACE_NPC_OFFSET = {
    "castle":           35,   # moat + round_tower + gatehouse + great_hall + half-keep
    "mediterranean":    45,   # 8 garden + 12 stoa + 14 wing + 11 half-basilica
    "east_asian":       46,   # 10 garden + 14 reception + 12 pavilion + 10 half-keep
    "south_asian":      44,   # 8 garden + 10 gate + 14 court + 12 half-diwan
    "italian":          46,   # 8 garden + 12 loggia + 16 cortile + 10 half-sala
    "moorish":          53,   # 8 garden + 8 tower + 12 gallery + 14 patio + 9 half-throne
    "middle_eastern":   42,   # 8 garden + 10 gate + 14 hall + 11 half-iwan
    "norse":            31,   # 8 yard + 12 lodge + 11 half-hall
    "gothic":           38,   # 8 garden + 8 tower + 12 nave + 10 half-choir
    "african":          41,   # 8 garden + 10 encl + 14 court + 9 half-throne
    "byzantine":        43,   # 8 garden + 10 port + 14 naos + 11 half-throne
    "tibetan":          44,   # 8 yard + 12 wing + 14 court + 10 half-tower
    "japanese":         42,   # 10 zen + 10 yagura + 14 shoin + 8 half-tenshu
    "chinese":          49,   # 10 pailou + 16 outer + 12 wing + 11 half-throne
    "tang_imperial":    48,   # 10 terrace + 12 drum + 14 col + 12 half-hanyuan
    "song_palace":      45,   # 12 garden + 10 moon + 14 pavilion + 9 half-hall
    "han_palace":       44,   # 10 platform + 12 watch + 12 ante + 10 half-throne
    "east_african":     41,   # 8 garden + 10 gate + 12 court + 11 half-throne
    "mesoamerican":     42,   # 8 plaza + 10 gate + 14 court + 10 half-pyramid
    "french_baroque":   47,   # 10 garden + 14 wing + 12 salon + 11 half-throne
    "incan":            40,   # 8 terrace + 10 gate + 12 hall + 10 half-throne
    "persian":          43,   # 8 garden + 10 portal + 14 apadana + 11 half-throne
}

PALACE_TYPES = [
    "castle", "mediterranean", "east_asian", "south_asian",
    "italian", "moorish", "middle_eastern",
    "norse", "gothic", "african", "byzantine", "tibetan",
    "japanese", "chinese", "tang_imperial", "song_palace", "han_palace",
    "east_african", "mesoamerican", "french_baroque", "incan", "persian",
]


def _populate_castle(world, left_x: int, sy: int, rng: random.Random):
    """Spawn royal court staff inside a medieval castle."""
    _palace_npc_at(world, left_x + 12, sy, TradeNPC, rng)
    _palace_npc_at(world, left_x + 22, sy, RoyalCuratorNPC, rng)
    _palace_npc_at(world, left_x + 30, sy, RoyalFloristNPC, rng)
    _palace_npc_at(world, left_x + 38, sy, RoyalJewelerNPC, rng)
    _palace_npc_at(world, left_x + 44, sy, RoyalPaleontologistNPC, rng)
    _palace_npc_at(world, left_x + 50, sy, RoyalAnglerNPC, rng)


def _place_mediterranean_palace(world, left_x: int, sy: int):
    """Grand forum complex — outer gardens, market stoa, temple wing, domed basilica,
    treasury, banquet hall.  Staff: court trader, oracle, quartermaster, palace chef.
    """
    _DOOR = WOOD_DOOR_CLOSED
    rng = random.Random(left_x ^ (world.seed * 0x1B4C3A7) ^ 0xA3D5E1)
    variant = rng.randint(0, 1)   # 0 = forum/republic  1 = acropolis/empire

    # Variant 1 uses slightly larger proportions for an imposing imperial feel
    W_GARD = 8
    W_STOA = 12 + variant * 2;  H_STOA = 7
    W_WING = 14;                 H_WING = 7 + variant
    W_HALL = 22;                 H_HALL = 9 + variant
    total_w = W_GARD + W_STOA + W_WING + W_HALL + W_WING + W_STOA + W_GARD
    _palace_clear_terrain(world, left_x, sy, total_w, H_HALL + 14)

    # --- shared room builder ---
    def _med_room(lx, w, h):
        _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, LIMESTONE_BLOCK)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy, ROMAN_MOSAIC)
        for by in range(sy - h, sy):
            _castle_set(world, lx,      by, LIMESTONE_BLOCK)
            _castle_set(world, lx + w,  by, LIMESTONE_BLOCK)
        _castle_door(world, lx, sy, door_block=_DOOR)
        _castle_door(world, lx + w - 2, sy, door_block=_DOOR)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy - h,     POLISHED_MARBLE)
            _castle_set(world, bx, sy - h - 1, POLISHED_MARBLE)
        for bx in range(lx + 1, lx + w, 3):
            _castle_bg(world, bx, sy - 5, ROMAN_ARCH_REN)

    def _med_cols(lx, w, n=2):
        step = max(3, w // (n + 1))
        for i in range(1, n + 1):
            cx = lx + i * step
            for by in range(sy - 10, sy):
                _castle_bg(world, cx, by, GARDEN_COLUMN)
            _castle_bg(world, cx, sy - 11, DORIC_CAPITAL)

    x = left_x

    # ── outer garden (left) ─────────────────────────────────────────────────
    for bx in range(x, x + W_GARD):
        _castle_set(world, bx, sy, INLAID_MARBLE)
    for bx in range(x, x + W_GARD, 2):
        _castle_bg(world, bx, sy - 1, GARDEN_COLUMN)
        _castle_bg(world, bx, sy - 2, GARDEN_COLUMN)
        _castle_bg(world, bx, sy - 3, DORIC_CAPITAL)
    _castle_bg(world, x + 1, sy - 1, LAVENDER_BED)
    _castle_bg(world, x + 3, sy - 1, ROSE_BED)
    _castle_bg(world, x + 5, sy - 1, LAVENDER_BED)
    _castle_bg(world, x + W_GARD // 2, sy - 2, MARBLE_PLINTH)
    _castle_bg(world, x + W_GARD // 2, sy - 1, MARBLE_STATUE)
    x += W_GARD

    # ── guards at palace entrance (always) ──────────────────────────────────
    _palace_npc_at(world, left_x + 1,          sy, GuardNPC, biodome="mediterranean")
    _palace_npc_at(world, left_x + total_w - 2, sy, GuardNPC, biodome="mediterranean")

    # ── left outer stoa ──────────────────────────────────────────────────────
    _med_room(x, W_STOA, H_STOA)
    _med_cols(x, W_STOA, n=2)
    _castle_bg(world, x + W_STOA // 2,     sy - 1, SYMPOSIUM_TABLE)
    _castle_bg(world, x + 2,               sy - 1, CARVED_BENCH)
    _castle_bg(world, x + W_STOA - 2,      sy - 1, CARVED_BENCH)
    _castle_bg(world, x + W_STOA // 2,     sy - H_STOA + 2, WALL_SCONCE)
    # Variant 0: court trader — Variant 1: wildflower scholar (court naturalist)
    if variant == 0:
        _castle_bg(world, x + 1,           sy - 2, OLIVE_BRANCH)
        _castle_bg(world, x + W_STOA - 1,  sy - 2, OLIVE_BRANCH)
        _palace_npc_at(world, x + W_STOA // 2, sy, TradeNPC, rng)
    else:
        _castle_bg(world, x + 1,           sy - 2, LAVENDER_BED)
        _castle_bg(world, x + W_STOA - 1,  sy - 2, ROSE_BED)
        _palace_npc_at(world, x + W_STOA // 2, sy, WildflowerQuestNPC, rng, 1,
                       "mediterranean")
    x += W_STOA

    # ── left inner wing ──────────────────────────────────────────────────────
    _med_room(x, W_WING, H_WING)
    _med_cols(x, W_WING, n=2)
    _castle_bg(world, x + W_WING // 2,     sy - H_WING + 3, CHANDELIER)
    # Variant 0: oracle — Variant 1: court jeweler
    if variant == 0:
        _castle_bg(world, x + W_WING // 2, sy - 1, MARBLE_PLINTH)
        _castle_bg(world, x + W_WING // 2, sy - 2, VOTIVE_TABLET)
        _castle_bg(world, x + 2,           sy - 1, TRIPOD_BRAZIER)
        _castle_bg(world, x + W_WING - 2,  sy - 1, TRIPOD_BRAZIER)
        _castle_bg(world, x + 3,           sy - 3, PHILOSOPHERS_SCROLL)
        _castle_bg(world, x + W_WING - 3,  sy - 3, PHILOSOPHERS_SCROLL)
        _palace_npc_at(world, x + W_WING // 2, sy, ShrineKeeperNPC, rng,
                       biodome="mediterranean")
    else:
        _castle_bg(world, x + W_WING // 2, sy - 1, HERMES_STELE)
        _castle_bg(world, x + W_WING // 2, sy - 2, MARBLE_PLINTH)
        _castle_bg(world, x + 2,           sy - 1, GREEK_STONE_BENCH)
        _castle_bg(world, x + W_WING - 2,  sy - 1, GREEK_STONE_BENCH)
        _castle_bg(world, x + 3,           sy - 3, VOTIVE_TABLET)
        _castle_bg(world, x + W_WING - 3,  sy - 3, VOTIVE_TABLET)
        _palace_npc_at(world, x + W_WING // 2, sy, JewelryMerchantNPC, rng)
    x += W_WING

    # ── central basilica — Leader throne (spawned by caller) ─────────────────
    cx_hall = x + W_HALL // 2
    _castle_fill_bg(world, x, x + W_HALL, sy - H_HALL, sy - 1, LIMESTONE_BLOCK)
    for bx in range(x, x + W_HALL + 1):
        _castle_set(world, bx, sy, INLAID_MARBLE)
    for by in range(sy - H_HALL, sy):
        _castle_set(world, x,          by, LIMESTONE_BLOCK)
        _castle_set(world, x + W_HALL, by, LIMESTONE_BLOCK)
    _castle_door(world, x, sy, door_block=_DOOR)
    _castle_door(world, x + W_HALL - 2, sy, door_block=_DOOR)
    # Nave — four column pairs forming a processional aisle
    for col_x in (x + 4, x + 8, x + W_HALL - 8, x + W_HALL - 4):
        for by in range(sy - H_HALL + 4, sy):
            _castle_bg(world, col_x, by, GARDEN_COLUMN)
        _castle_bg(world, col_x, sy - H_HALL + 3, DORIC_CAPITAL)
    # Arch band across the upper wall
    for bx in range(x + 1, x + W_HALL, 2):
        _castle_bg(world, bx, sy - 9, ROMAN_ARCH_REN)
    # Double marble cornice
    for bx in range(x, x + W_HALL + 1):
        _castle_set(world, bx, sy - H_HALL,     POLISHED_MARBLE)
        _castle_set(world, bx, sy - H_HALL - 1, POLISHED_MARBLE)
    # Full dome
    for row in range(1, W_HALL // 2 + 1):
        dome_y = sy - H_HALL - 1 - row
        if not (0 <= dome_y < world.height):
            break
        for bx in range(x + row, x + W_HALL + 1 - row):
            _castle_set(world, bx, dome_y, POLISHED_MARBLE)
    # Throne dais and lighting
    _castle_bg(world, cx_hall,     sy - 1, MARBLE_PLINTH)
    _castle_bg(world, cx_hall,     sy - 2, HERMES_STELE)
    _castle_bg(world, cx_hall - 4, sy - 1, TRIPOD_BRAZIER)
    _castle_bg(world, cx_hall + 4, sy - 1, TRIPOD_BRAZIER)
    _castle_bg(world, cx_hall - 7, sy - 1, LAUREL_WREATH_MOUNT)
    _castle_bg(world, cx_hall + 7, sy - 1, LAUREL_WREATH_MOUNT)
    _castle_bg(world, cx_hall,     sy - H_HALL + 4, CHANDELIER)
    _castle_bg(world, cx_hall - 3, sy - H_HALL + 6, CANDELABRA)
    _castle_bg(world, cx_hall + 3, sy - H_HALL + 6, CANDELABRA)
    x += W_HALL

    # ── right inner wing ─────────────────────────────────────────────────────
    _med_room(x, W_WING, H_WING)
    _med_cols(x, W_WING, n=2)
    _castle_bg(world, x + W_WING // 2,     sy - H_WING + 3, CHANDELIER)
    # Variant 0: treasury/quartermaster — Variant 1: gem scholar
    if variant == 0:
        _castle_bg(world, x + W_WING // 2, sy - 1, HERMES_STELE)
        _castle_bg(world, x + W_WING // 2, sy - 2, MARBLE_PLINTH)
        _castle_bg(world, x + 2,           sy - 2, WALL_SCONCE)
        _castle_bg(world, x + W_WING - 2,  sy - 2, WALL_SCONCE)
        _castle_bg(world, x + 3,           sy - 1, CARVED_BENCH)
        _castle_bg(world, x + W_WING - 3,  sy - 1, CARVED_BENCH)
        _palace_npc_at(world, x + W_WING // 2, sy, MerchantNPC, rng)
    else:
        _castle_bg(world, x + W_WING // 2, sy - 1, MARBLE_PLINTH)
        _castle_bg(world, x + W_WING // 2, sy - 2, VICTORY_STELE)
        _castle_bg(world, x + 2,           sy - 1, TRIPOD_BRAZIER)
        _castle_bg(world, x + W_WING - 2,  sy - 1, TRIPOD_BRAZIER)
        _castle_bg(world, x + 3,           sy - 3, PHILOSOPHERS_SCROLL)
        _castle_bg(world, x + W_WING - 3,  sy - 3, PHILOSOPHERS_SCROLL)
        _palace_npc_at(world, x + W_WING // 2, sy, GemQuestNPC, rng, 1,
                       "mediterranean")
    x += W_WING

    # ── right outer stoa ─────────────────────────────────────────────────────
    _med_room(x, W_STOA, H_STOA)
    _med_cols(x, W_STOA, n=2)
    _castle_bg(world, x + W_STOA // 2,     sy - 1, SYMPOSIUM_TABLE)
    _castle_bg(world, x + 2,               sy - 1, GREEK_STONE_BENCH)
    _castle_bg(world, x + W_STOA - 2,      sy - 1, GREEK_STONE_BENCH)
    _castle_bg(world, x + W_STOA // 2,     sy - H_STOA + 2, CHANDELIER)
    # Variant 0: palace chef — Variant 1: court merchant
    if variant == 0:
        _castle_bg(world, x + 1,           sy - 2, LAUREL_WREATH_MOUNT)
        _castle_bg(world, x + W_STOA - 1,  sy - 2, LAUREL_WREATH_MOUNT)
        _palace_npc_at(world, x + W_STOA // 2, sy, RestaurantNPC, rng, "mediterranean")
    else:
        _castle_bg(world, x + 1,           sy - 2, OLIVE_BRANCH)
        _castle_bg(world, x + W_STOA - 1,  sy - 2, OLIVE_BRANCH)
        _palace_npc_at(world, x + W_STOA // 2, sy, TradeNPC, rng)
    x += W_STOA

    # ── outer garden (right) ─────────────────────────────────────────────────
    for bx in range(x, x + W_GARD):
        _castle_set(world, bx, sy, INLAID_MARBLE)
    for bx in range(x, x + W_GARD, 2):
        _castle_bg(world, bx, sy - 1, GARDEN_COLUMN)
        _castle_bg(world, bx, sy - 2, GARDEN_COLUMN)
        _castle_bg(world, bx, sy - 3, DORIC_CAPITAL)
    _castle_bg(world, x + 1, sy - 1, ROSE_BED)
    _castle_bg(world, x + 3, sy - 1, LAVENDER_BED)
    _castle_bg(world, x + 5, sy - 1, ROSE_BED)
    _castle_bg(world, x + W_GARD // 2, sy - 2, MARBLE_PLINTH)
    _castle_bg(world, x + W_GARD // 2, sy - 1, MARBLE_BIRDBATH)


def _place_east_asian_palace(world, left_x: int, sy: int):
    """Imperial compound — garden approaches, shinto reception courts, pavilion wings,
    central 4-tier pagoda keep.  Staff: shrine priest, court steward, palace chef, trader.
    """
    _DOOR = SHOJI_DOOR_CLOSED
    rng = random.Random(left_x ^ (world.seed * 0x7E3C1F9) ^ 0xD4E7B2)
    variant = rng.randint(0, 1)   # 0 = shogunate  1 = imperial court

    W_GARD = 10   # outer garden + torii approach
    W_RCRT = 14;  H_RCRT = 12   # reception court
    W_PAV  = 12;  H_PAV  = 7    # inner pavilion
    W_KEEP = 20;  H_KEEP = 9    # central pagoda keep
    total_w = W_GARD + W_RCRT + W_PAV + W_KEEP + W_PAV + W_RCRT + W_GARD
    _palace_clear_terrain(world, left_x, sy, total_w, H_KEEP + 16)

    # --- shared builders ---
    def _ea_room(lx, w, h, tiers=2):
        _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, PINE_PLANK_WALL)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy, TATAMI_PAVING)
        for by in range(sy - h, sy):
            _castle_set(world, lx,      by, PINE_PLANK_WALL)
            _castle_set(world, lx + w,  by, PINE_PLANK_WALL)
        _castle_door(world, lx, sy, door_block=_DOOR)
        _castle_door(world, lx + w - 2, sy, door_block=_DOOR)
        for bx in range(lx + 1, lx + w, 2):
            _castle_bg(world, bx, sy - 4, JAPANESE_SHOJI)
            _castle_bg(world, bx, sy - 5, JAPANESE_SHOJI)
        for tier in range(tiers):
            base_y = sy - h - 1 - tier * 2
            for bx in range(lx - 1 + tier, lx + w + 2 - tier):
                _castle_set(world, bx, base_y, PAGODA_EAVE)
            for bx in range(lx + tier, lx + w + 1 - tier):
                _castle_set(world, bx, base_y - 1, PINE_PLANK_WALL)

    def _torii(ax, w):
        for bx in range(ax, ax + w):
            _castle_set(world, bx, sy, TATAMI_PAVING)
        mid = ax + w // 2
        for post in (mid, mid + 2):
            for row in range(1, 4):
                _castle_set(world, post, sy - row, TORII_PANEL)
        for bx in range(mid - 1, mid + 4):
            _castle_set(world, bx, sy - 4, TORII_PANEL)
            _castle_set(world, bx, sy - 5, TORII_PANEL)
        _castle_bg(world, ax + 1,      sy - 1, PINE_TOPIARY_JP)
        _castle_bg(world, ax + 2,      sy - 1, JAPANESE_MAPLE)
        _castle_bg(world, ax + w - 2,  sy - 1, JAPANESE_MAPLE)
        _castle_bg(world, ax + w - 1,  sy - 1, PINE_TOPIARY_JP)
        _castle_bg(world, ax + w // 2, sy - 1, KOI_POOL)

    x = left_x

    # ── guards at compound entrance ──────────────────────────────────────────
    _palace_npc_at(world, left_x + 1,           sy, GuardNPC, biodome="east_asian")
    _palace_npc_at(world, left_x + total_w - 2, sy, GuardNPC, biodome="east_asian")

    # ── outer garden + torii (left) ──────────────────────────────────────────
    _torii(x, W_GARD)
    x += W_GARD

    # ── left reception court ─────────────────────────────────────────────────
    _ea_room(x, W_RCRT, H_RCRT, tiers=2)
    _castle_bg(world, x + 2,               sy - 1, PINE_TOPIARY_JP)
    _castle_bg(world, x + W_RCRT - 2,      sy - 1, PINE_TOPIARY_JP)
    _castle_bg(world, x + W_RCRT // 2,     sy - H_RCRT + 3, CHANDELIER)
    _castle_bg(world, x + 1,               sy - 3, BAMBOO_CLUMP)
    _castle_bg(world, x + W_RCRT - 1,      sy - 3, BAMBOO_CLUMP)
    # Variant 0: shinto priest — Variant 1: wildflower scholar (court botanist)
    if variant == 0:
        _castle_bg(world, x + W_RCRT // 2, sy - 1, STONE_BASIN)
        _palace_npc_at(world, x + W_RCRT // 2, sy, ShrineKeeperNPC, rng,
                       biodome="east_asian")
    else:
        _castle_bg(world, x + W_RCRT // 2, sy - 1, KOI_POOL)
        _palace_npc_at(world, x + W_RCRT // 2, sy, WildflowerQuestNPC, rng, 1,
                       "east_asian")
    x += W_RCRT

    # ── left inner pavilion ──────────────────────────────────────────────────
    _ea_room(x, W_PAV, H_PAV, tiers=2)
    _castle_bg(world, x + 2,              sy - 1, BAMBOO_CLUMP)
    _castle_bg(world, x + W_PAV - 2,      sy - 1, BAMBOO_CLUMP)
    _castle_bg(world, x + W_PAV // 2,     sy - H_PAV + 3, STAR_LAMP)
    # Variant 0: court steward — Variant 1: gem scholar
    if variant == 0:
        _castle_bg(world, x + W_PAV // 2, sy - 1, GARDEN_LANTERN)
        _palace_npc_at(world, x + W_PAV // 2, sy, MerchantNPC, rng)
    else:
        _castle_bg(world, x + W_PAV // 2, sy - 1, STAR_LAMP)
        _palace_npc_at(world, x + W_PAV // 2, sy, GemQuestNPC, rng, 1, "east_asian")
    x += W_PAV

    # ── central pagoda keep — Leader throne (spawned by caller) ──────────────
    cx_keep = x + W_KEEP // 2
    _castle_fill_bg(world, x, x + W_KEEP, sy - H_KEEP, sy - 1, PINE_PLANK_WALL)
    for bx in range(x, x + W_KEEP + 1):
        _castle_set(world, bx, sy, TATAMI_PAVING)
    for by in range(sy - H_KEEP, sy):
        _castle_set(world, x,          by, PINE_PLANK_WALL)
        _castle_set(world, x + W_KEEP, by, PINE_PLANK_WALL)
    _castle_door(world, x, sy, door_block=_DOOR)
    _castle_door(world, x + W_KEEP - 2, sy, door_block=_DOOR)
    # Mid-floor gallery
    mid_floor = sy - H_KEEP // 2
    for bx in range(x + 1, x + W_KEEP):
        _castle_set(world, bx, mid_floor, TATAMI_PAVING)
    # Upper-level shoji screens
    for bx in range(x + 1, x + W_KEEP, 2):
        _castle_bg(world, bx, sy - 6, JAPANESE_SHOJI)
        _castle_bg(world, bx, sy - 7, JAPANESE_SHOJI)
    for bx in range(x + 1, x + W_KEEP, 2):
        _castle_bg(world, bx, mid_floor - 2, JAPANESE_SHOJI)
        _castle_bg(world, bx, mid_floor - 3, JAPANESE_SHOJI)
    # Interior wooden columns
    for col_x in (x + 4, x + W_KEEP - 4):
        for by in range(sy - H_KEEP + 4, sy):
            _castle_bg(world, col_x, by, PINE_PLANK_WALL)
        _castle_bg(world, col_x, sy - H_KEEP + 3, GARDEN_LANTERN)
    # Throne and lighting
    _castle_bg(world, cx_keep,     sy - 1, CARVED_BENCH)
    _castle_bg(world, cx_keep - 4, sy - 1, STAR_LAMP)
    _castle_bg(world, cx_keep + 4, sy - 1, STAR_LAMP)
    _castle_bg(world, cx_keep - 6, sy - 1, BAMBOO_CLUMP)
    _castle_bg(world, cx_keep + 6, sy - 1, BAMBOO_CLUMP)
    _castle_bg(world, cx_keep,     sy - H_KEEP + 4, CHANDELIER)
    # 4-tier pagoda roof
    for tier in range(4):
        base_y = sy - H_KEEP - 1 - tier * 2
        for bx in range(x - 1 + tier, x + W_KEEP + 2 - tier):
            _castle_set(world, bx, base_y, PAGODA_EAVE)
        for bx in range(x + tier, x + W_KEEP + 1 - tier):
            _castle_set(world, bx, base_y - 1, PINE_PLANK_WALL)
    x += W_KEEP

    # ── right inner pavilion ─────────────────────────────────────────────────
    _ea_room(x, W_PAV, H_PAV, tiers=2)
    _castle_bg(world, x + 2,              sy - 1, BAMBOO_CLUMP)
    _castle_bg(world, x + W_PAV - 2,      sy - 1, BAMBOO_CLUMP)
    _castle_bg(world, x + W_PAV // 2,     sy - H_PAV + 3, STAR_LAMP)
    # Variant 0: palace chef — Variant 1: court jeweler
    if variant == 0:
        _castle_bg(world, x + W_PAV // 2, sy - 1, GARDEN_LANTERN)
        _palace_npc_at(world, x + W_PAV // 2, sy, RestaurantNPC, rng, "east_asian")
    else:
        _castle_bg(world, x + W_PAV // 2, sy - 1, STONE_BASIN)
        _palace_npc_at(world, x + W_PAV // 2, sy, JewelryMerchantNPC, rng)
    x += W_PAV

    # ── right reception court ────────────────────────────────────────────────
    _ea_room(x, W_RCRT, H_RCRT, tiers=2)
    _castle_bg(world, x + 2,               sy - 1, JAPANESE_MAPLE)
    _castle_bg(world, x + W_RCRT - 2,      sy - 1, JAPANESE_MAPLE)
    _castle_bg(world, x + W_RCRT // 2,     sy - H_RCRT + 3, CHANDELIER)
    _castle_bg(world, x + 1,               sy - 3, PINE_TOPIARY_JP)
    _castle_bg(world, x + W_RCRT - 1,      sy - 3, PINE_TOPIARY_JP)
    # Variant 0: court trader — Variant 1: court merchant
    if variant == 0:
        _castle_bg(world, x + W_RCRT // 2, sy - 1, SHISHI_ODOSHI)
        _palace_npc_at(world, x + W_RCRT // 2, sy, TradeNPC, rng)
    else:
        _castle_bg(world, x + W_RCRT // 2, sy - 1, KOI_POOL)
        _palace_npc_at(world, x + W_RCRT // 2, sy, MerchantNPC, rng)
    x += W_RCRT

    # ── outer garden + torii (right) ─────────────────────────────────────────
    _torii(x, W_GARD)


def _place_south_asian_palace(world, left_x: int, sy: int):
    """Ornate Mughal imperial complex — peacock gardens, soaring gate towers, jali courts,
    massive central Diwan-i-Khas.  Staff: vizier, court pandit, quartermaster, palace chef.
    """
    _DOOR = SANDALWOOD_DOOR_CLOSED
    rng = random.Random(left_x ^ (world.seed * 0xC3E5A91) ^ 0xF2B6D3)
    variant = rng.randint(0, 1)   # 0 = sultanate  1 = maharaja court

    W_GARD = 8
    W_GATE = 10;  H_GATE = 7
    W_CORT = 14;  H_CORT = 7
    W_DIWAN= 24;  H_DIWAN= 10
    total_w = W_GARD + W_GATE + W_CORT + W_DIWAN + W_CORT + W_GATE + W_GARD
    _palace_clear_terrain(world, left_x, sy, total_w, H_DIWAN + 16)

    # --- shared builders ---
    def _sa_room(lx, w, h, fountain=False):
        _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, LIMESTONE_BLOCK)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy, MUDEJAR_STAR_TILE)
        for by in range(sy - h, sy):
            _castle_set(world, lx,      by, LIMESTONE_BLOCK)
            _castle_set(world, lx + w,  by, LIMESTONE_BLOCK)
        _castle_door(world, lx, sy, door_block=_DOOR)
        _castle_door(world, lx + w - 2, sy, door_block=_DOOR)
        for bx in range(lx + 1, lx + w, 2):
            _castle_bg(world, bx, sy - 4, MUGHAL_JALI)
            _castle_bg(world, bx, sy - 5, MUGHAL_JALI)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy - h, TERRACOTTA_ROOF_TILE)
        if fountain:
            _castle_bg(world, lx + w // 2, sy - 1, ANDALUSIAN_FOUNTAIN)

    def _gate_tower(gx):
        _castle_fill_bg(world, gx, gx + W_GATE, sy - H_GATE, sy - 1, LIMESTONE_BLOCK)
        for bx in range(gx, gx + W_GATE + 1):
            _castle_set(world, bx, sy, MUDEJAR_STAR_TILE)
        for by in range(sy - H_GATE, sy):
            _castle_set(world, gx,          by, LIMESTONE_BLOCK)
            _castle_set(world, gx + W_GATE, by, LIMESTONE_BLOCK)
        # Central Mughal arch passage
        _castle_door(world, gx + W_GATE // 2 - 1, sy, door_block=_DOOR)
        for by in range(sy - 6, sy):
            _castle_bg(world, gx + W_GATE // 2,     by, MUGHAL_ARCH)
            _castle_bg(world, gx + W_GATE // 2 - 1, by, MUGHAL_ARCH)
        # Upper jali screens
        for bx in range(gx + 1, gx + W_GATE, 2):
            _castle_bg(world, bx, sy - 8, MUGHAL_JALI)
            _castle_bg(world, bx, sy - 9, MUGHAL_JALI)
        # Stepped terracotta parapet
        for bx in range(gx, gx + W_GATE + 1):
            _castle_set(world, bx, sy - H_GATE, TERRACOTTA_ROOF_TILE)
            if (bx - gx) % 2 == 0:
                _castle_set(world, bx, sy - H_GATE - 1, TERRACOTTA_ROOF_TILE)
        # Corner flower decoration
        _castle_bg(world, gx + 1,          sy - H_GATE + 2, MARIGOLD_BED)
        _castle_bg(world, gx + W_GATE - 1, sy - H_GATE + 2, MARIGOLD_BED)

    x = left_x

    # ── guards at compound entrance ──────────────────────────────────────────
    _palace_npc_at(world, left_x + 1,           sy, GuardNPC, biodome="south_asian")
    _palace_npc_at(world, left_x + total_w - 2, sy, GuardNPC, biodome="south_asian")

    # ── outer peacock garden (left) ──────────────────────────────────────────
    for bx in range(x, x + W_GARD):
        _castle_set(world, bx, sy, MUDEJAR_STAR_TILE)
    _castle_bg(world, x + 1, sy - 1, TOPIARY_PEACOCK)
    _castle_bg(world, x + 3, sy - 1, MARIGOLD_BED)
    _castle_bg(world, x + 5, sy - 1, SUNFLOWER_BED)
    _castle_bg(world, x + W_GARD // 2, sy - 1, ANDALUSIAN_FOUNTAIN)
    x += W_GARD

    # ── left gate tower ───────────────────────────────────────────────────────
    _gate_tower(x)
    x += W_GATE

    # ── left jali court ───────────────────────────────────────────────────────
    _sa_room(x, W_CORT, H_CORT, fountain=True)
    _castle_bg(world, x + W_CORT // 2,     sy - H_CORT + 3, CHANDELIER)
    _castle_bg(world, x + W_CORT // 2 - 3, sy - 2, MUGHAL_JALI)
    _castle_bg(world, x + W_CORT // 2 + 3, sy - 2, MUGHAL_JALI)
    if variant == 0:   # sultanate: vizier in left court
        _castle_bg(world, x + 2,           sy - 1, MARIGOLD_BED)
        _castle_bg(world, x + W_CORT - 2,  sy - 1, MARIGOLD_BED)
        _palace_npc_at(world, x + W_CORT // 2, sy, TradeNPC, rng)
    else:              # maharaja court: wildflower scholar
        _castle_bg(world, x + 2,           sy - 1, SUNFLOWER_BED)
        _castle_bg(world, x + W_CORT - 2,  sy - 1, ROSE_BED)
        _palace_npc_at(world, x + W_CORT // 2, sy, WildflowerQuestNPC, rng, 1,
                       "south_asian")
    x += W_CORT

    # ── central Diwan-i-Khas — Leader throne (spawned by caller) ────────────
    cx_diwan = x + W_DIWAN // 2
    _castle_fill_bg(world, x, x + W_DIWAN, sy - H_DIWAN, sy - 1, LIMESTONE_BLOCK)
    for bx in range(x, x + W_DIWAN + 1):
        _castle_set(world, bx, sy, MUDEJAR_STAR_TILE)
    for by in range(sy - H_DIWAN, sy):
        _castle_set(world, x,          by, LIMESTONE_BLOCK)
        _castle_set(world, x + W_DIWAN, by, LIMESTONE_BLOCK)
    _castle_door(world, x, sy, door_block=_DOOR)
    _castle_door(world, x + W_DIWAN - 2, sy, door_block=_DOOR)
    # Four Mughal arch columns forming the audience hall
    for col_x in (x + 4, x + 8, x + W_DIWAN - 8, x + W_DIWAN - 4):
        for by in range(sy - 8, sy):
            _castle_bg(world, col_x, by, MUGHAL_ARCH)
    # Upper jali screen band
    for bx in range(x + 1, x + W_DIWAN, 2):
        _castle_bg(world, bx, sy - 10, MUGHAL_JALI)
        _castle_bg(world, bx, sy - 11, MUGHAL_JALI)
    # Stepped terracotta roof
    for bx in range(x, x + W_DIWAN + 1):
        _castle_set(world, bx, sy - H_DIWAN, TERRACOTTA_ROOF_TILE)
    for step in range(1, 7):
        step_y = sy - H_DIWAN - step
        if not (0 <= step_y < world.height):
            break
        for bx in range(x + step * 2, x + W_DIWAN + 1 - step * 2):
            _castle_set(world, bx, step_y, TERRACOTTA_ROOF_TILE)
    # Throne dais
    _castle_bg(world, cx_diwan,     sy - 1, MARBLE_PLINTH)
    _castle_bg(world, cx_diwan,     sy - 2, VICTORY_STELE)
    _castle_bg(world, cx_diwan - 4, sy - 1, STAR_LAMP)
    _castle_bg(world, cx_diwan + 4, sy - 1, STAR_LAMP)
    _castle_bg(world, cx_diwan - 7, sy - 1, MARIGOLD_BED)
    _castle_bg(world, cx_diwan + 7, sy - 1, MARIGOLD_BED)
    _castle_bg(world, cx_diwan - 9, sy - 1, TOPIARY_PEACOCK)
    _castle_bg(world, cx_diwan + 9, sy - 1, TOPIARY_PEACOCK)
    _castle_bg(world, cx_diwan,     sy - H_DIWAN + 5, CHANDELIER)
    _castle_bg(world, cx_diwan - 3, sy - H_DIWAN + 7, CANDELABRA)
    _castle_bg(world, cx_diwan + 3, sy - H_DIWAN + 7, CANDELABRA)
    x += W_DIWAN

    # ── right jali court ─────────────────────────────────────────────────────
    _sa_room(x, W_CORT, H_CORT, fountain=True)
    _castle_bg(world, x + W_CORT // 2,     sy - H_CORT + 3, CHANDELIER)
    _castle_bg(world, x + W_CORT // 2 - 3, sy - 2, MUGHAL_JALI)
    _castle_bg(world, x + W_CORT // 2 + 3, sy - 2, MUGHAL_JALI)
    if variant == 0:   # sultanate: court pandit
        _castle_bg(world, x + 2,           sy - 1, SUNFLOWER_BED)
        _castle_bg(world, x + W_CORT - 2,  sy - 1, SUNFLOWER_BED)
        _palace_npc_at(world, x + W_CORT // 2, sy, ShrineKeeperNPC, rng,
                       biodome="south_asian")
    else:              # maharaja court: gem scholar
        _castle_bg(world, x + 2,           sy - 1, MARIGOLD_BED)
        _castle_bg(world, x + W_CORT - 2,  sy - 1, MARIGOLD_BED)
        _palace_npc_at(world, x + W_CORT // 2, sy, GemQuestNPC, rng, 1, "south_asian")
    x += W_CORT

    # ── right gate tower — quartermaster (variant 0) or jeweler (variant 1) ──
    _gate_tower(x)
    if variant == 0:
        _palace_npc_at(world, x + W_GATE // 2, sy, MerchantNPC, rng)
    else:
        _palace_npc_at(world, x + W_GATE // 2, sy, JewelryMerchantNPC, rng)
    x += W_GATE

    # ── outer peacock garden (right) ─────────────────────────────────────────
    for bx in range(x, x + W_GARD):
        _castle_set(world, bx, sy, MUDEJAR_STAR_TILE)
    _castle_bg(world, x + 1,          sy - 1, SUNFLOWER_BED)
    _castle_bg(world, x + 3,          sy - 1, MARIGOLD_BED)
    _castle_bg(world, x + 5,          sy - 1, TOPIARY_PEACOCK)
    _castle_bg(world, x + W_GARD // 2, sy - 1, ANDALUSIAN_FOUNTAIN)


def _place_italian_palazzo(world, left_x: int, sy: int):
    """Renaissance Italian palazzo — outer gardens, loggia wings, cortile courtyards,
    grand sala grande with piano nobile.  Staff: consul, court naturalist, merchant, scholar.
    """
    _DOOR = GILDED_DOOR_CLOSED
    rng = random.Random(left_x ^ (world.seed * 0x5A3F2B1) ^ 0xC0FFEE)
    variant = rng.randint(0, 1)   # 0 = republic  1 = duchy

    W_GARD = 8
    W_LOG  = 12;  H_LOG  = 7
    W_CORT = 16;  H_CORT = 7
    W_SALA = 20;  H_SALA = 9
    total_w = W_GARD + W_LOG + W_CORT + W_SALA + W_CORT + W_LOG + W_GARD
    _palace_clear_terrain(world, left_x, sy, total_w, H_SALA + 14)

    def _pal_room(lx, w, h):
        _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, LIMESTONE_BLOCK)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy, ROMAN_MOSAIC)
        for by in range(sy - h, sy):
            _castle_set(world, lx,      by, LIMESTONE_BLOCK)
            _castle_set(world, lx + w,  by, LIMESTONE_BLOCK)
        _castle_door(world, lx, sy, door_block=_DOOR)
        _castle_door(world, lx + w - 2, sy, door_block=_DOOR)
        # Ground-floor arcade
        for bx in range(lx + 1, lx + w, 3):
            _castle_bg(world, bx, sy - 4, ROMAN_ARCH_REN)
            _castle_bg(world, bx, sy - 5, ROMAN_ARCH_REN)
        # Piano nobile floor + balcony rail
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy - h + 1, POLISHED_MARBLE)
        for bx in range(lx + 1, lx + w, 2):
            _castle_bg(world, bx, sy - h,     PALAZZO_BALCONY)
        # Cornice
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy - h - 1, POLISHED_MARBLE)

    x = left_x

    _palace_npc_at(world, left_x + 1,           sy, GuardNPC)
    _palace_npc_at(world, left_x + total_w - 2, sy, GuardNPC)

    # ── outer garden (left) ──────────────────────────────────────────────────
    for bx in range(x, x + W_GARD):
        _castle_set(world, bx, sy, INLAID_MARBLE)
    _castle_bg(world, x + 1,           sy - 1, ROSE_BED)
    _castle_bg(world, x + 3,           sy - 1, LAVENDER_BED)
    _castle_bg(world, x + 5,           sy - 1, STANDARD_ROSE)
    _castle_bg(world, x + W_GARD // 2, sy - 2, MARBLE_PLINTH)
    _castle_bg(world, x + W_GARD // 2, sy - 1, MARBLE_STATUE)
    x += W_GARD

    # ── left loggia ──────────────────────────────────────────────────────────
    _pal_room(x, W_LOG, H_LOG)
    _castle_bg(world, x + W_LOG // 2,  sy - H_LOG + 2, CHANDELIER)
    _castle_bg(world, x + 2,           sy - 1, GARDEN_COLUMN)
    _castle_bg(world, x + W_LOG - 2,   sy - 1, GARDEN_COLUMN)
    if variant == 0:
        _castle_bg(world, x + W_LOG // 2, sy - 1, SYMPOSIUM_TABLE)
        _palace_npc_at(world, x + W_LOG // 2, sy, TradeNPC, rng)
    else:
        _castle_bg(world, x + W_LOG // 2, sy - 1, CARVED_BENCH)
        _palace_npc_at(world, x + W_LOG // 2, sy, GemQuestNPC, rng, 1)
    x += W_LOG

    # ── left cortile — open courtyard with fountain ──────────────────────────
    for bx in range(x, x + W_CORT + 1):
        _castle_set(world, bx, sy, POLISHED_MARBLE)
    _castle_fill_bg(world, x, x + W_CORT, sy - H_CORT, sy - 1, LIMESTONE_BLOCK)
    for by in range(sy - H_CORT, sy):
        _castle_set(world, x,          by, LIMESTONE_BLOCK)
        _castle_set(world, x + W_CORT, by, LIMESTONE_BLOCK)
    _castle_door(world, x, sy, door_block=_DOOR)
    _castle_door(world, x + W_CORT - 2, sy, door_block=_DOOR)
    for bx in range(x + 1, x + W_CORT, 3):
        _castle_bg(world, bx, sy - 5, ROMAN_ARCH_REN)
    _castle_bg(world, x + W_CORT // 2,     sy - 1, rng.choice(_FOUNTAIN_BLOCKS))
    _castle_bg(world, x + 2,               sy - 1, BOXWOOD_BALL)
    _castle_bg(world, x + W_CORT - 2,      sy - 1, BOXWOOD_BALL)
    _castle_bg(world, x + W_CORT // 2,     sy - H_CORT + 3, CHANDELIER)
    for bx in range(x, x + W_CORT + 1):
        _castle_set(world, bx, sy - H_CORT + 1, POLISHED_MARBLE)
    for bx in range(x + 1, x + W_CORT, 2):
        _castle_bg(world, bx, sy - H_CORT, PALAZZO_BALCONY)
    for bx in range(x, x + W_CORT + 1):
        _castle_set(world, bx, sy - H_CORT - 1, POLISHED_MARBLE)
    if variant == 0:
        _palace_npc_at(world, x + W_CORT // 2, sy, WildflowerQuestNPC, rng, 1)
    else:
        _palace_npc_at(world, x + W_CORT // 2, sy, MerchantNPC, rng)
    x += W_CORT

    # ── sala grande — Leader throne (spawned by caller) ──────────────────────
    cx = x + W_SALA // 2
    _castle_fill_bg(world, x, x + W_SALA, sy - H_SALA, sy - 1, LIMESTONE_BLOCK)
    for bx in range(x, x + W_SALA + 1):
        _castle_set(world, bx, sy, POLISHED_MARBLE)
    for by in range(sy - H_SALA, sy):
        _castle_set(world, x,          by, LIMESTONE_BLOCK)
        _castle_set(world, x + W_SALA, by, LIMESTONE_BLOCK)
    _castle_door(world, x, sy, door_block=_DOOR)
    _castle_door(world, x + W_SALA - 2, sy, door_block=_DOOR)
    for bx in range(x + 1, x + W_SALA, 3):
        _castle_bg(world, bx, sy - 5, ROMAN_ARCH_REN)
        _castle_bg(world, bx, sy - 6, ROMAN_ARCH_REN)
    for col_x in (x + 4, x + W_SALA - 4):
        for by in range(sy - H_SALA + 4, sy):
            _castle_bg(world, col_x, by, GARDEN_COLUMN)
        _castle_bg(world, col_x, sy - H_SALA + 3, DORIC_CAPITAL)
    mid = sy - H_SALA // 2
    for bx in range(x + 1, x + W_SALA):
        _castle_set(world, bx, mid, POLISHED_MARBLE)
    for bx in range(x, x + W_SALA + 1):
        _castle_set(world, bx, sy - H_SALA + 1, POLISHED_MARBLE)
    for bx in range(x + 1, x + W_SALA, 2):
        _castle_bg(world, bx, sy - H_SALA, PALAZZO_BALCONY)
    for bx in range(x, x + W_SALA + 1):
        _castle_set(world, bx, sy - H_SALA - 1, POLISHED_MARBLE)
    _castle_bg(world, cx,     sy - 1, CARVED_BENCH)
    _castle_bg(world, cx - 2, sy - 1, MARBLE_PLINTH)
    _castle_bg(world, cx + 2, sy - 1, MARBLE_PLINTH)
    _castle_bg(world, cx - 2, sy - 2, MARBLE_STATUE)
    _castle_bg(world, cx + 2, sy - 2, MARBLE_STATUE)
    _castle_bg(world, cx - 5, sy - 1, CANDELABRA)
    _castle_bg(world, cx + 5, sy - 1, CANDELABRA)
    _castle_bg(world, cx,     sy - H_SALA + 4, CHANDELIER)
    x += W_SALA

    # ── right cortile ────────────────────────────────────────────────────────
    for bx in range(x, x + W_CORT + 1):
        _castle_set(world, bx, sy, POLISHED_MARBLE)
    _castle_fill_bg(world, x, x + W_CORT, sy - H_CORT, sy - 1, LIMESTONE_BLOCK)
    for by in range(sy - H_CORT, sy):
        _castle_set(world, x,          by, LIMESTONE_BLOCK)
        _castle_set(world, x + W_CORT, by, LIMESTONE_BLOCK)
    _castle_door(world, x, sy, door_block=_DOOR)
    _castle_door(world, x + W_CORT - 2, sy, door_block=_DOOR)
    for bx in range(x + 1, x + W_CORT, 3):
        _castle_bg(world, bx, sy - 5, ROMAN_ARCH_REN)
    _castle_bg(world, x + W_CORT // 2,  sy - 1, rng.choice(_FOUNTAIN_BLOCKS))
    _castle_bg(world, x + 2,            sy - 1, TOPIARY_PEACOCK)
    _castle_bg(world, x + W_CORT - 2,   sy - 1, TOPIARY_RABBIT)
    _castle_bg(world, x + W_CORT // 2,  sy - H_CORT + 3, CHANDELIER)
    for bx in range(x, x + W_CORT + 1):
        _castle_set(world, bx, sy - H_CORT + 1, POLISHED_MARBLE)
    for bx in range(x + 1, x + W_CORT, 2):
        _castle_bg(world, bx, sy - H_CORT, PALAZZO_BALCONY)
    for bx in range(x, x + W_CORT + 1):
        _castle_set(world, bx, sy - H_CORT - 1, POLISHED_MARBLE)
    if variant == 0:
        _palace_npc_at(world, x + W_CORT // 2, sy, RestaurantNPC, rng)
    else:
        _palace_npc_at(world, x + W_CORT // 2, sy, ScholarNPC, rng)
    x += W_CORT

    # ── right loggia ─────────────────────────────────────────────────────────
    _pal_room(x, W_LOG, H_LOG)
    _castle_bg(world, x + W_LOG // 2,  sy - H_LOG + 2, CHANDELIER)
    _castle_bg(world, x + 2,           sy - 1, GARDEN_COLUMN)
    _castle_bg(world, x + W_LOG - 2,   sy - 1, GARDEN_COLUMN)
    if variant == 0:
        _castle_bg(world, x + W_LOG // 2, sy - 1, GREEK_STONE_BENCH)
        _palace_npc_at(world, x + W_LOG // 2, sy, BlacksmithNPC, rng)
    else:
        _castle_bg(world, x + W_LOG // 2, sy - 1, MARBLE_BIRDBATH)
        _palace_npc_at(world, x + W_LOG // 2, sy, JewelryMerchantNPC, rng)
    x += W_LOG

    # ── outer garden (right) ─────────────────────────────────────────────────
    for bx in range(x, x + W_GARD):
        _castle_set(world, bx, sy, INLAID_MARBLE)
    _castle_bg(world, x + 1,           sy - 1, LAVENDER_BED)
    _castle_bg(world, x + 3,           sy - 1, ROSE_BED)
    _castle_bg(world, x + 5,           sy - 1, AGAPANTHUS_PATCH)
    _castle_bg(world, x + W_GARD // 2, sy - 2, MARBLE_PLINTH)
    _castle_bg(world, x + W_GARD // 2, sy - 1, MARBLE_BIRDBATH)


def _place_moorish_palace(world, left_x: int, sy: int):
    """Andalusian Moorish palace — Alhambra-inspired patio gardens, arched galleries,
    mudejar throne hall.  Staff: court scribe, jeweler, quartermaster, palace chef.
    """
    _DOOR = COBALT_DOOR_CLOSED
    rng = random.Random(left_x ^ (world.seed * 0x8B4CF21) ^ 0xAB5EED)
    variant = rng.randint(0, 1)   # 0 = Nasrid sultanate  1 = Almohad caliphate

    W_GARD  = 8
    W_TOWER = 8;   H_TOWER = 8
    W_GAL   = 12;  H_GAL   = 7
    W_PATIO = 14;  H_PATIO = 7
    W_THRONE= 18;  H_THRONE= 8
    total_w = W_GARD + W_TOWER + W_GAL + W_PATIO + W_THRONE + W_PATIO + W_GAL + W_TOWER + W_GARD
    _palace_clear_terrain(world, left_x, sy, total_w, H_THRONE + 14)

    def _moor_room(lx, w, h):
        _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, WHITEWASHED_WALL)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy, SPANISH_PATIO_FLOOR)
        for by in range(sy - h, sy):
            _castle_set(world, lx,      by, WHITEWASHED_WALL)
            _castle_set(world, lx + w,  by, WHITEWASHED_WALL)
        _castle_door(world, lx, sy, door_block=_DOOR)
        _castle_door(world, lx + w - 2, sy, door_block=_DOOR)
        for bx in range(lx + 1, lx + w, 2):
            _castle_bg(world, bx, sy - 4, MUGHAL_JALI)
            _castle_bg(world, bx, sy - 5, MUGHAL_JALI)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy - h, MUDEJAR_BRICK)
            if (bx - lx) % 2 == 0:
                _castle_set(world, bx, sy - h - 1, MUDEJAR_BRICK)

    def _watch_tower(tx):
        _castle_fill_bg(world, tx, tx + W_TOWER, sy - H_TOWER, sy - 1, MUDEJAR_BRICK)
        for bx in range(tx, tx + W_TOWER + 1):
            _castle_set(world, bx, sy, MUDEJAR_STAR_TILE)
        for by in range(sy - H_TOWER, sy):
            _castle_set(world, tx,           by, MUDEJAR_BRICK)
            _castle_set(world, tx + W_TOWER, by, MUDEJAR_BRICK)
        _castle_door(world, tx + W_TOWER // 2 - 1, sy, door_block=_DOOR)
        for by in range(sy - 6, sy):
            _castle_bg(world, tx + W_TOWER // 2,     by, MUGHAL_ARCH)
            _castle_bg(world, tx + W_TOWER // 2 - 1, by, MUGHAL_ARCH)
        for bx in range(tx + 1, tx + W_TOWER, 2):
            _castle_bg(world, bx, sy - 9,  MUGHAL_JALI)
            _castle_bg(world, bx, sy - 10, MUGHAL_JALI)
        for bx in range(tx, tx + W_TOWER + 1):
            _castle_set(world, bx, sy - H_TOWER, MUDEJAR_BRICK)
            if (bx - tx) % 2 == 0:
                _castle_set(world, bx, sy - H_TOWER - 1, MUDEJAR_BRICK)

    x = left_x

    _palace_npc_at(world, left_x + 1,           sy, GuardNPC)
    _palace_npc_at(world, left_x + total_w - 2, sy, GuardNPC)

    # ── entry garden (left) ──────────────────────────────────────────────────
    for bx in range(x, x + W_GARD):
        _castle_set(world, bx, sy, MUDEJAR_STAR_TILE)
    _castle_bg(world, x + 1,           sy - 1, ROSE_BED)
    _castle_bg(world, x + 3,           sy - 1, LAVENDER_BED)
    _castle_bg(world, x + 5,           sy - 1, ROSE_BED)
    _castle_bg(world, x + W_GARD // 2, sy - 1, ANDALUSIAN_FOUNTAIN)
    x += W_GARD

    # ── left watch tower ─────────────────────────────────────────────────────
    _watch_tower(x)
    x += W_TOWER

    # ── left gallery ─────────────────────────────────────────────────────────
    _moor_room(x, W_GAL, H_GAL)
    _castle_bg(world, x + W_GAL // 2,  sy - H_GAL + 2, CHANDELIER)
    _castle_bg(world, x + 2,           sy - 1, PORTUGUESE_BENCH)
    _castle_bg(world, x + W_GAL - 2,   sy - 1, PORTUGUESE_BENCH)
    if variant == 0:
        _castle_bg(world, x + W_GAL // 2, sy - 1, STONE_BASIN)
        _palace_npc_at(world, x + W_GAL // 2, sy, TradeNPC, rng)
    else:
        _castle_bg(world, x + W_GAL // 2, sy - 1, ANDALUSIAN_FOUNTAIN)
        _palace_npc_at(world, x + W_GAL // 2, sy, ScholarNPC, rng)
    x += W_GAL

    # ── left patio (Court of the Myrtles) ────────────────────────────────────
    for bx in range(x, x + W_PATIO + 1):
        _castle_set(world, bx, sy, SPANISH_PATIO_FLOOR)
    _castle_fill_bg(world, x, x + W_PATIO, sy - H_PATIO, sy - 1, WHITEWASHED_WALL)
    for by in range(sy - H_PATIO, sy):
        _castle_set(world, x,           by, WHITEWASHED_WALL)
        _castle_set(world, x + W_PATIO, by, WHITEWASHED_WALL)
    _castle_door(world, x, sy, door_block=_DOOR)
    _castle_door(world, x + W_PATIO - 2, sy, door_block=_DOOR)
    _castle_bg(world, x + W_PATIO // 2,     sy - 1, ANDALUSIAN_FOUNTAIN)
    _castle_bg(world, x + 2,               sy - 1, LAVENDER_BED)
    _castle_bg(world, x + W_PATIO - 2,     sy - 1, LAVENDER_BED)
    for bx in range(x + 1, x + W_PATIO, 2):
        _castle_bg(world, bx, sy - 6, MUGHAL_JALI)
    _castle_bg(world, x + W_PATIO // 2,    sy - H_PATIO + 3, CHANDELIER)
    for bx in range(x, x + W_PATIO + 1):
        _castle_set(world, bx, sy - H_PATIO, MUDEJAR_BRICK)
    if variant == 0:
        _palace_npc_at(world, x + W_PATIO // 2, sy, WildflowerQuestNPC, rng, 1)
    else:
        _palace_npc_at(world, x + W_PATIO // 2, sy, ShrineKeeperNPC, rng)
    x += W_PATIO

    # ── throne hall (Comares) — Leader throne (spawned by caller) ────────────
    cx = x + W_THRONE // 2
    _castle_fill_bg(world, x, x + W_THRONE, sy - H_THRONE, sy - 1, WHITEWASHED_WALL)
    for bx in range(x, x + W_THRONE + 1):
        _castle_set(world, bx, sy, MUDEJAR_STAR_TILE)
    for by in range(sy - H_THRONE, sy):
        _castle_set(world, x,           by, MUDEJAR_BRICK)
        _castle_set(world, x + W_THRONE,by, MUDEJAR_BRICK)
    _castle_door(world, x, sy, door_block=_DOOR)
    _castle_door(world, x + W_THRONE - 2, sy, door_block=_DOOR)
    for col_x in (x + 4, x + W_THRONE - 4):
        for by in range(sy - 8, sy):
            _castle_bg(world, col_x, by, MUGHAL_ARCH)
    for bx in range(x + 1, x + W_THRONE, 2):
        _castle_bg(world, bx, sy - 10, MUGHAL_JALI)
        _castle_bg(world, bx, sy - 11, MUGHAL_JALI)
    mid = sy - H_THRONE // 2
    for bx in range(x + 1, x + W_THRONE):
        _castle_set(world, bx, mid, SPANISH_PATIO_FLOOR)
    for bx in range(x, x + W_THRONE + 1):
        _castle_set(world, bx, sy - H_THRONE, MUDEJAR_BRICK)
        if (bx - x) % 2 == 0:
            _castle_set(world, bx, sy - H_THRONE - 1, MUDEJAR_BRICK)
    _castle_bg(world, cx,     sy - 1, MARBLE_PLINTH)
    _castle_bg(world, cx,     sy - 2, VICTORY_STELE)
    _castle_bg(world, cx - 4, sy - 1, STAR_LAMP)
    _castle_bg(world, cx + 4, sy - 1, STAR_LAMP)
    _castle_bg(world, cx - 6, sy - 1, ROSE_BED)
    _castle_bg(world, cx + 6, sy - 1, ROSE_BED)
    _castle_bg(world, cx,     sy - H_THRONE + 4, CHANDELIER)
    _castle_bg(world, cx - 3, sy - H_THRONE + 6, CANDELABRA)
    _castle_bg(world, cx + 3, sy - H_THRONE + 6, CANDELABRA)
    x += W_THRONE

    # ── right patio ──────────────────────────────────────────────────────────
    for bx in range(x, x + W_PATIO + 1):
        _castle_set(world, bx, sy, SPANISH_PATIO_FLOOR)
    _castle_fill_bg(world, x, x + W_PATIO, sy - H_PATIO, sy - 1, WHITEWASHED_WALL)
    for by in range(sy - H_PATIO, sy):
        _castle_set(world, x,           by, WHITEWASHED_WALL)
        _castle_set(world, x + W_PATIO, by, WHITEWASHED_WALL)
    _castle_door(world, x, sy, door_block=_DOOR)
    _castle_door(world, x + W_PATIO - 2, sy, door_block=_DOOR)
    _castle_bg(world, x + W_PATIO // 2,     sy - 1, ANDALUSIAN_FOUNTAIN)
    _castle_bg(world, x + 2,               sy - 1, MARIGOLD_BED)
    _castle_bg(world, x + W_PATIO - 2,     sy - 1, MARIGOLD_BED)
    for bx in range(x + 1, x + W_PATIO, 2):
        _castle_bg(world, bx, sy - 6, MUGHAL_JALI)
    _castle_bg(world, x + W_PATIO // 2,    sy - H_PATIO + 3, CHANDELIER)
    for bx in range(x, x + W_PATIO + 1):
        _castle_set(world, bx, sy - H_PATIO, MUDEJAR_BRICK)
    if variant == 0:
        _palace_npc_at(world, x + W_PATIO // 2, sy, JewelryMerchantNPC, rng)
    else:
        _palace_npc_at(world, x + W_PATIO // 2, sy, MerchantNPC, rng)
    x += W_PATIO

    # ── right gallery ────────────────────────────────────────────────────────
    _moor_room(x, W_GAL, H_GAL)
    _castle_bg(world, x + W_GAL // 2,  sy - H_GAL + 2, CHANDELIER)
    _castle_bg(world, x + 2,           sy - 1, PORTUGUESE_BENCH)
    _castle_bg(world, x + W_GAL - 2,   sy - 1, PORTUGUESE_BENCH)
    if variant == 0:
        _castle_bg(world, x + W_GAL // 2, sy - 1, STONE_BASIN)
        _palace_npc_at(world, x + W_GAL // 2, sy, RestaurantNPC, rng)
    else:
        _castle_bg(world, x + W_GAL // 2, sy - 1, CARVED_BENCH)
        _palace_npc_at(world, x + W_GAL // 2, sy, GemQuestNPC, rng, 1)
    x += W_GAL

    # ── right watch tower ────────────────────────────────────────────────────
    _watch_tower(x)
    x += W_TOWER

    # ── exit garden (right) ──────────────────────────────────────────────────
    for bx in range(x, x + W_GARD):
        _castle_set(world, bx, sy, MUDEJAR_STAR_TILE)
    _castle_bg(world, x + 1,           sy - 1, LAVENDER_BED)
    _castle_bg(world, x + 3,           sy - 1, ROSE_BED)
    _castle_bg(world, x + 5,           sy - 1, LAVENDER_BED)
    _castle_bg(world, x + W_GARD // 2, sy - 1, ANDALUSIAN_FOUNTAIN)


def _place_middle_eastern_palace(world, left_x: int, sy: int):
    """Arabian/Persian palace — date-palm entry gardens, vaulted gate towers, divan halls,
    grand throne iwan.  Staff: vizier, court scholar, gem trader, palace steward.
    """
    _DOOR = SAFFRON_DOOR_CLOSED
    rng = random.Random(left_x ^ (world.seed * 0x6D2E4B8) ^ 0xF4B1A3)
    variant = rng.randint(0, 1)   # 0 = Abbasid  1 = Ottoman

    W_GARD = 8
    W_GATE = 10;  H_GATE = 7
    W_HALL = 14;  H_HALL = 7
    W_IWAN = 22;  H_IWAN = 9
    total_w = W_GARD + W_GATE + W_HALL + W_IWAN + W_HALL + W_GATE + W_GARD
    _palace_clear_terrain(world, left_x, sy, total_w, H_IWAN + 14)

    def _me_room(lx, w, h):
        _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, SANDSTONE_BLOCK)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy, PALACE_FLOOR_TILE)
        for by in range(sy - h, sy):
            _castle_set(world, lx,      by, SANDSTONE_BLOCK)
            _castle_set(world, lx + w,  by, SANDSTONE_BLOCK)
        _castle_door(world, lx, sy, door_block=_DOOR)
        _castle_door(world, lx + w - 2, sy, door_block=_DOOR)
        for bx in range(lx + 1, lx + w, 2):
            _castle_bg(world, bx, sy - 4, MUGHAL_JALI)
            _castle_bg(world, bx, sy - 5, MUGHAL_JALI)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy - h, SANDSTONE_BLOCK)

    def _gate_tower(gx):
        _castle_fill_bg(world, gx, gx + W_GATE, sy - H_GATE, sy - 1, SANDSTONE_BLOCK)
        for bx in range(gx, gx + W_GATE + 1):
            _castle_set(world, bx, sy, PALACE_FLOOR_TILE)
        for by in range(sy - H_GATE, sy):
            _castle_set(world, gx,          by, SANDSTONE_BLOCK)
            _castle_set(world, gx + W_GATE, by, SANDSTONE_BLOCK)
        _castle_door(world, gx + W_GATE // 2 - 1, sy, door_block=_DOOR)
        for by in range(sy - 7, sy):
            _castle_bg(world, gx + W_GATE // 2,     by, MUGHAL_ARCH)
            _castle_bg(world, gx + W_GATE // 2 - 1, by, MUGHAL_ARCH)
        for bx in range(gx + 1, gx + W_GATE, 2):
            _castle_bg(world, bx, sy - 9,  MUGHAL_JALI)
            _castle_bg(world, bx, sy - 10, MUGHAL_JALI)
        for bx in range(gx, gx + W_GATE + 1):
            _castle_set(world, bx, sy - H_GATE, SANDSTONE_BLOCK)
            if (bx - gx) % 2 == 0:
                _castle_set(world, bx, sy - H_GATE - 1, SANDSTONE_BLOCK)
        _castle_bg(world, gx + 1,          sy - H_GATE + 2, STAR_LAMP)
        _castle_bg(world, gx + W_GATE - 1, sy - H_GATE + 2, STAR_LAMP)

    x = left_x

    _palace_npc_at(world, left_x + 1,           sy, GuardNPC)
    _palace_npc_at(world, left_x + total_w - 2, sy, GuardNPC)

    # ── entry garden (left) ──────────────────────────────────────────────────
    for bx in range(x, x + W_GARD):
        _castle_set(world, bx, sy, PALACE_FLOOR_TILE)
    _castle_bg(world, x + 1,           sy - 1, MARIGOLD_BED)
    _castle_bg(world, x + 3,           sy - 1, ROSE_BED)
    _castle_bg(world, x + 5,           sy - 1, MARIGOLD_BED)
    _castle_bg(world, x + W_GARD // 2, sy - 1, rng.choice(_FOUNTAIN_BLOCKS))
    x += W_GARD

    # ── left gate tower ──────────────────────────────────────────────────────
    _gate_tower(x)
    x += W_GATE

    # ── left divan hall ──────────────────────────────────────────────────────
    _me_room(x, W_HALL, H_HALL)
    _castle_bg(world, x + W_HALL // 2,  sy - H_HALL + 3, CHANDELIER)
    _castle_bg(world, x + 2,            sy - 1, STONE_BASIN)
    _castle_bg(world, x + W_HALL - 2,   sy - 1, STONE_BASIN)
    for bx in range(x + 1, x + W_HALL, 3):
        _castle_bg(world, bx, sy - 7, MUGHAL_ARCH)
    if variant == 0:
        _castle_bg(world, x + W_HALL // 2, sy - 1, CARVED_BENCH)
        _palace_npc_at(world, x + W_HALL // 2, sy, ScholarNPC, rng)
    else:
        _castle_bg(world, x + W_HALL // 2, sy - 1, MARBLE_PLINTH)
        _palace_npc_at(world, x + W_HALL // 2, sy, TradeNPC, rng)
    x += W_HALL

    # ── grand throne iwan — Leader throne (spawned by caller) ────────────────
    cx = x + W_IWAN // 2
    _castle_fill_bg(world, x, x + W_IWAN, sy - H_IWAN, sy - 1, SANDSTONE_BLOCK)
    for bx in range(x, x + W_IWAN + 1):
        _castle_set(world, bx, sy, PALACE_FLOOR_TILE)
    for by in range(sy - H_IWAN, sy):
        _castle_set(world, x,          by, SANDSTONE_BLOCK)
        _castle_set(world, x + W_IWAN, by, SANDSTONE_BLOCK)
    _castle_door(world, x, sy, door_block=_DOOR)
    _castle_door(world, x + W_IWAN - 2, sy, door_block=_DOOR)
    for col_x in (x + 4, x + 8, x + W_IWAN - 8, x + W_IWAN - 4):
        for by in range(sy - 8, sy):
            _castle_bg(world, col_x, by, MUGHAL_ARCH)
    for bx in range(x + 1, x + W_IWAN, 2):
        _castle_bg(world, bx, sy - 10, MUGHAL_JALI)
        _castle_bg(world, bx, sy - 11, MUGHAL_JALI)
    mid = sy - H_IWAN // 2
    for bx in range(x + 1, x + W_IWAN):
        _castle_set(world, bx, mid, PALACE_FLOOR_TILE)
    for bx in range(x, x + W_IWAN + 1):
        _castle_set(world, bx, sy - H_IWAN, SANDSTONE_BLOCK)
    for step in range(1, 6):
        step_y = sy - H_IWAN - step
        if not (0 <= step_y < world.height):
            break
        for bx in range(x + step * 2, x + W_IWAN + 1 - step * 2):
            _castle_set(world, bx, step_y, SANDSTONE_BLOCK)
    _castle_bg(world, cx,     sy - 1, MARBLE_PLINTH)
    _castle_bg(world, cx,     sy - 2, VICTORY_STELE)
    _castle_bg(world, cx - 4, sy - 1, STAR_LAMP)
    _castle_bg(world, cx + 4, sy - 1, STAR_LAMP)
    _castle_bg(world, cx - 7, sy - 1, MARIGOLD_BED)
    _castle_bg(world, cx + 7, sy - 1, MARIGOLD_BED)
    _castle_bg(world, cx - 9, sy - 1, ROSE_BED)
    _castle_bg(world, cx + 9, sy - 1, ROSE_BED)
    _castle_bg(world, cx,     sy - H_IWAN + 4, CHANDELIER)
    _castle_bg(world, cx - 3, sy - H_IWAN + 6, CANDELABRA)
    _castle_bg(world, cx + 3, sy - H_IWAN + 6, CANDELABRA)
    x += W_IWAN

    # ── right divan hall ─────────────────────────────────────────────────────
    _me_room(x, W_HALL, H_HALL)
    _castle_bg(world, x + W_HALL // 2,  sy - H_HALL + 3, CHANDELIER)
    _castle_bg(world, x + 2,            sy - 1, MARIGOLD_BED)
    _castle_bg(world, x + W_HALL - 2,   sy - 1, MARIGOLD_BED)
    for bx in range(x + 1, x + W_HALL, 3):
        _castle_bg(world, bx, sy - 7, MUGHAL_ARCH)
    if variant == 0:
        _castle_bg(world, x + W_HALL // 2, sy - 1, STONE_BASIN)
        _palace_npc_at(world, x + W_HALL // 2, sy, GemQuestNPC, rng, 1)
    else:
        _castle_bg(world, x + W_HALL // 2, sy - 1, CARVED_BENCH)
        _palace_npc_at(world, x + W_HALL // 2, sy, MerchantNPC, rng)
    x += W_HALL

    # ── right gate tower ─────────────────────────────────────────────────────
    _gate_tower(x)
    if variant == 0:
        _palace_npc_at(world, x + W_GATE // 2, sy, JewelryMerchantNPC, rng)
    else:
        _palace_npc_at(world, x + W_GATE // 2, sy, RestaurantNPC, rng)
    x += W_GATE

    # ── exit garden (right) ──────────────────────────────────────────────────
    for bx in range(x, x + W_GARD):
        _castle_set(world, bx, sy, PALACE_FLOOR_TILE)
    _castle_bg(world, x + 1,           sy - 1, ROSE_BED)
    _castle_bg(world, x + 3,           sy - 1, MARIGOLD_BED)
    _castle_bg(world, x + 5,           sy - 1, ROSE_BED)
    _castle_bg(world, x + W_GARD // 2, sy - 1, rng.choice(_FOUNTAIN_BLOCKS))


def _place_norse_hall(world, left_x: int, sy: int):
    """Viking mead hall complex — entry yards, side longhouses, great central hall.
    Staff: blacksmith, merchant, trade envoy, shrine keeper, gem quest giver.
    """
    _DOOR = STUDDED_OAK_DOOR_CLOSED
    rng = random.Random(left_x ^ (world.seed * 0x3A7F1E5) ^ 0xD1CE4B)
    variant = rng.randint(0, 1)   # 0 = chieftain hall  1 = jarls court

    W_YARD  = 8
    W_LODGE = 12;  H_LODGE = 7
    W_HALL  = 22;  H_HALL  = 8
    total_w = W_YARD + W_LODGE + W_HALL + W_LODGE + W_YARD
    _palace_clear_terrain(world, left_x, sy, total_w, H_HALL + 12)

    def _longhouse(lx, w, h):
        _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, HOUSE_WALL_DARK)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy, COBBLESTONE)
        for by in range(sy - h, sy):
            _castle_set(world, lx,      by, HOUSE_WALL_DARK)
            _castle_set(world, lx + w,  by, HOUSE_WALL_DARK)
        _castle_door(world, lx, sy, door_block=_DOOR)
        _castle_door(world, lx + w - 2, sy, door_block=_DOOR)
        for bx in range(lx + 1, lx + w, 2):
            _castle_bg(world, bx, sy - 4, HERALDIC_PANEL)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy - h, HOUSE_ROOF_DARK)
        _castle_bg(world, lx + 1,      sy - 1, BRONZE_SHIELD_MOUNT)
        _castle_bg(world, lx + w - 1,  sy - 1, BRONZE_SHIELD_MOUNT)

    x = left_x

    # ── guards at compound entrance ──────────────────────────────────────────
    _palace_npc_at(world, left_x + 1,           sy, GuardNPC, biodome="alpine")
    _palace_npc_at(world, left_x + total_w - 2, sy, GuardNPC, biodome="alpine")

    # ── entry yard (left) ────────────────────────────────────────────────────
    for bx in range(x, x + W_YARD):
        _castle_set(world, bx, sy, COBBLESTONE)
    _castle_bg(world, x + 1, sy - 1, FIREWOOD_STACK)
    _castle_bg(world, x + 3, sy - 1, HAY_BALE)
    _castle_bg(world, x + 5, sy - 1, FIREWOOD_STACK)
    x += W_YARD

    # ── left longhouse ───────────────────────────────────────────────────────
    _longhouse(x, W_LODGE, H_LODGE)
    _castle_bg(world, x + W_LODGE // 2, sy - H_LODGE + 3, CHANDELIER)
    _castle_bg(world, x + 2,            sy - 1, HERALDIC_PANEL)
    _castle_bg(world, x + W_LODGE - 2,  sy - 1, HERALDIC_PANEL)
    if variant == 0:
        _castle_bg(world, x + W_LODGE // 2, sy - 1, BRAZIER)
        _palace_npc_at(world, x + W_LODGE // 2, sy, BlacksmithNPC, rng)
    else:
        _castle_bg(world, x + W_LODGE // 2, sy - 1, HAY_BALE)
        _palace_npc_at(world, x + W_LODGE // 2, sy, MerchantNPC, rng)
    x += W_LODGE

    # ── great mead hall — Leader throne (spawned by caller) ──────────────────
    cx = x + W_HALL // 2
    _castle_fill_bg(world, x, x + W_HALL, sy - H_HALL, sy - 1, HERALDIC_PANEL)
    for bx in range(x, x + W_HALL + 1):
        _castle_set(world, bx, sy, COBBLESTONE)
    for by in range(sy - H_HALL, sy):
        _castle_set(world, x,          by, ROUGH_STONE_WALL)
        _castle_set(world, x + W_HALL, by, ROUGH_STONE_WALL)
    _castle_door(world, x, sy, door_block=_DOOR)
    _castle_door(world, x + W_HALL - 2, sy, door_block=_DOOR)
    # Interior timber columns
    for col_x in (x + 4, x + W_HALL - 4):
        for by in range(sy - H_HALL + 3, sy):
            _castle_bg(world, col_x, by, PINE_PLANK_WALL)
    # Mid-floor gallery
    mid = sy - H_HALL // 2
    for bx in range(x + 1, x + W_HALL):
        _castle_set(world, bx, mid, PINE_PLANK_WALL)
    # Fire pits and shields
    _castle_bg(world, cx - 6, sy - 1, BRAZIER)
    _castle_bg(world, cx + 6, sy - 1, BRAZIER)
    _castle_bg(world, cx - 2, sy - 1, BRONZE_SHIELD_MOUNT)
    _castle_bg(world, cx + 2, sy - 1, BRONZE_SHIELD_MOUNT)
    # Throne
    _castle_bg(world, cx, sy - 1, CARVED_BENCH)
    _castle_bg(world, cx, sy - 2, HERALDIC_PANEL)
    # Roof
    for bx in range(x, x + W_HALL + 1):
        _castle_set(world, bx, sy - H_HALL, HOUSE_ROOF_DARK)
    _castle_bg(world, cx, sy - H_HALL + 4, CHANDELIER)
    x += W_HALL

    # ── right longhouse ──────────────────────────────────────────────────────
    _longhouse(x, W_LODGE, H_LODGE)
    _castle_bg(world, x + W_LODGE // 2, sy - H_LODGE + 3, CHANDELIER)
    _castle_bg(world, x + 2,            sy - 1, HERALDIC_PANEL)
    _castle_bg(world, x + W_LODGE - 2,  sy - 1, HERALDIC_PANEL)
    if variant == 0:
        _castle_bg(world, x + W_LODGE // 2, sy - 1, BRAZIER)
        _palace_npc_at(world, x + W_LODGE // 2, sy, TradeNPC, rng)
    else:
        _castle_bg(world, x + W_LODGE // 2, sy - 1, FIREWOOD_STACK)
        _palace_npc_at(world, x + W_LODGE // 2, sy, ShrineKeeperNPC, rng,
                       biodome="boreal")
    x += W_LODGE

    # ── exit yard (right) ────────────────────────────────────────────────────
    for bx in range(x, x + W_YARD):
        _castle_set(world, bx, sy, COBBLESTONE)
    _castle_bg(world, x + 1, sy - 1, HAY_BALE)
    _castle_bg(world, x + 3, sy - 1, FIREWOOD_STACK)
    _castle_bg(world, x + 5, sy - 1, HAY_BALE)
    # Variant NPCs on right side
    if variant == 0:
        _palace_npc_at(world, x + W_YARD // 2, sy, MerchantNPC, rng)
    else:
        _palace_npc_at(world, x + W_YARD // 2, sy, GemQuestNPC, rng, 1, "boreal")


def _place_gothic_palace(world, left_x: int, sy: int):
    """Gothic cathedral-palace — gargoyle entry approach, flanking towers, nave wings,
    central choir throne room with rose window.  Staff: shrine keeper, scholar, trade envoy.
    """
    _DOOR = STUDDED_OAK_DOOR_CLOSED
    rng = random.Random(left_x ^ (world.seed * 0x2C9E8F3) ^ 0xB0A3C6)
    variant = rng.randint(0, 1)   # 0 = episcopal  1 = royal chapel

    W_GARD  = 8
    W_TOWER = 8;   H_TOWER = 8
    W_NAVE  = 12;  H_NAVE  = 7
    W_CHOIR = 20;  H_CHOIR = 9
    total_w = W_GARD + W_TOWER + W_NAVE + W_CHOIR + W_NAVE + W_TOWER + W_GARD
    _palace_clear_terrain(world, left_x, sy, total_w, H_CHOIR + 14)

    def _gothic_room(lx, w, h):
        _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, CHAPEL_STONE)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy, COBBLESTONE)
        for by in range(sy - h, sy):
            _castle_set(world, lx,      by, CHAPEL_STONE)
            _castle_set(world, lx + w,  by, CHAPEL_STONE)
        _castle_door(world, lx, sy, door_block=_DOOR)
        _castle_door(world, lx + w - 2, sy, door_block=_DOOR)
        for bx in range(lx + 1, lx + w, 2):
            _castle_bg(world, bx, sy - 5, LANCET_WINDOW)
            _castle_bg(world, bx, sy - 6, LANCET_WINDOW)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy - h, CHAPEL_STONE)
        _castle_bg(world, lx + 1,      sy - h + 2, GARGOYLE_BLOCK)
        _castle_bg(world, lx + w - 1,  sy - h + 2, GARGOYLE_BLOCK)

    def _flanking_tower(tx):
        _castle_fill_bg(world, tx, tx + W_TOWER, sy - H_TOWER, sy - 1, CHAPEL_STONE)
        for bx in range(tx, tx + W_TOWER + 1):
            _castle_set(world, bx, sy, COBBLESTONE)
        for by in range(sy - H_TOWER, sy):
            _castle_set(world, tx,           by, CHAPEL_STONE)
            _castle_set(world, tx + W_TOWER, by, CHAPEL_STONE)
        _castle_door(world, tx + W_TOWER // 2 - 1, sy, door_block=_DOOR)
        for bx in range(tx + 1, tx + W_TOWER, 2):
            _castle_bg(world, bx, sy - 8,  LANCET_WINDOW)
            _castle_bg(world, bx, sy - 9,  LANCET_WINDOW)
        _castle_bg(world, tx + W_TOWER // 2, sy - H_TOWER + 2, GOTHIC_TRACERY)
        for bx in range(tx, tx + W_TOWER + 1):
            _castle_set(world, bx, sy - H_TOWER, CHAPEL_STONE)
            if (bx - tx) % 2 == 0:
                _castle_set(world, bx, sy - H_TOWER - 1, CHAPEL_STONE)
        _castle_bg(world, tx + 1,          sy - H_TOWER + 2, GARGOYLE_BLOCK)
        _castle_bg(world, tx + W_TOWER - 1, sy - H_TOWER + 2, GARGOYLE_BLOCK)

    x = left_x

    # ── guards at compound entrance ──────────────────────────────────────────
    _palace_npc_at(world, left_x + 1,           sy, GuardNPC)
    _palace_npc_at(world, left_x + total_w - 2, sy, GuardNPC)

    # ── entry approach (left) ────────────────────────────────────────────────
    for bx in range(x, x + W_GARD):
        _castle_set(world, bx, sy, COBBLESTONE)
    _castle_bg(world, x + 1, sy - 1, GARGOYLE_BLOCK)
    _castle_bg(world, x + 3, sy - 1, BOXWOOD_BALL)
    _castle_bg(world, x + 5, sy - 1, BOXWOOD_BALL)
    _castle_bg(world, x + W_GARD - 1, sy - 1, GARGOYLE_BLOCK)
    x += W_GARD

    # ── left flanking tower ──────────────────────────────────────────────────
    _flanking_tower(x)
    x += W_TOWER

    # ── left nave ────────────────────────────────────────────────────────────
    _gothic_room(x, W_NAVE, H_NAVE)
    _castle_bg(world, x + W_NAVE // 2, sy - H_NAVE + 3, CHANDELIER)
    _castle_bg(world, x + 2,           sy - 1, CANDELABRA)
    _castle_bg(world, x + W_NAVE - 2,  sy - 1, CANDELABRA)
    if variant == 0:
        _castle_bg(world, x + W_NAVE // 2, sy - 1, STONE_BASIN)
        _palace_npc_at(world, x + W_NAVE // 2, sy, ShrineKeeperNPC, rng,
                       biodome="temperate")
    else:
        _castle_bg(world, x + W_NAVE // 2, sy - 1, CARVED_BENCH)
        _palace_npc_at(world, x + W_NAVE // 2, sy, WildflowerQuestNPC, rng, 1,
                       "temperate")
    x += W_NAVE

    # ── central choir/throne — Leader throne (spawned by caller) ─────────────
    cx = x + W_CHOIR // 2
    _castle_fill_bg(world, x, x + W_CHOIR, sy - H_CHOIR, sy - 1, CHAPEL_STONE)
    for bx in range(x, x + W_CHOIR + 1):
        _castle_set(world, bx, sy, COBBLESTONE)
    for by in range(sy - H_CHOIR, sy):
        _castle_set(world, x,           by, CHAPEL_STONE)
        _castle_set(world, x + W_CHOIR, by, CHAPEL_STONE)
    _castle_door(world, x, sy, door_block=_DOOR)
    _castle_door(world, x + W_CHOIR - 2, sy, door_block=_DOOR)
    # Interior columns
    for col_x in (x + 4, x + W_CHOIR - 4):
        for by in range(sy - H_CHOIR + 4, sy):
            _castle_bg(world, col_x, by, CHAPEL_STONE)
        _castle_bg(world, col_x, sy - H_CHOIR + 3, GARGOYLE_BLOCK)
    # Lancet windows in rows
    for bx in range(x + 1, x + W_CHOIR, 2):
        _castle_bg(world, bx, sy - 7, LANCET_WINDOW)
        _castle_bg(world, bx, sy - 8, LANCET_WINDOW)
    # Rose window + tracery centrepiece
    _castle_bg(world, cx, sy - H_CHOIR + 3, ROSE_WINDOW)
    _castle_bg(world, cx - 1, sy - H_CHOIR + 3, GOTHIC_TRACERY)
    _castle_bg(world, cx + 1, sy - H_CHOIR + 3, GOTHIC_TRACERY)
    # Mid-floor gallery
    mid = sy - H_CHOIR // 2
    for bx in range(x + 1, x + W_CHOIR):
        _castle_set(world, bx, mid, COBBLESTONE)
    # Throne dais
    _castle_bg(world, cx,     sy - 1, CARVED_BENCH)
    _castle_bg(world, cx - 1, sy - 1, MARBLE_PLINTH)
    _castle_bg(world, cx + 1, sy - 1, MARBLE_PLINTH)
    _castle_bg(world, cx - 4, sy - 1, CANDELABRA)
    _castle_bg(world, cx + 4, sy - 1, CANDELABRA)
    _castle_bg(world, cx - 3, sy - H_CHOIR + 6, CHANDELIER)
    _castle_bg(world, cx + 3, sy - H_CHOIR + 6, CHANDELIER)
    # Stepped crenellated top
    for bx in range(x, x + W_CHOIR + 1):
        _castle_set(world, bx, sy - H_CHOIR, CHAPEL_STONE)
        if (bx - x) % 2 == 0:
            _castle_set(world, bx, sy - H_CHOIR - 1, CHAPEL_STONE)
    x += W_CHOIR

    # ── right nave ───────────────────────────────────────────────────────────
    _gothic_room(x, W_NAVE, H_NAVE)
    _castle_bg(world, x + W_NAVE // 2, sy - H_NAVE + 3, CHANDELIER)
    _castle_bg(world, x + 2,           sy - 1, CANDELABRA)
    _castle_bg(world, x + W_NAVE - 2,  sy - 1, CANDELABRA)
    if variant == 0:
        _castle_bg(world, x + W_NAVE // 2, sy - 1, MARBLE_PLINTH)
        _palace_npc_at(world, x + W_NAVE // 2, sy, ScholarNPC, rng, "temperate")
    else:
        _castle_bg(world, x + W_NAVE // 2, sy - 1, STONE_BASIN)
        _palace_npc_at(world, x + W_NAVE // 2, sy, GemQuestNPC, rng, 1, "temperate")
    x += W_NAVE

    # ── right flanking tower ─────────────────────────────────────────────────
    _flanking_tower(x)
    if variant == 0:
        _palace_npc_at(world, x + W_TOWER // 2, sy, MerchantNPC, rng)
    else:
        _palace_npc_at(world, x + W_TOWER // 2, sy, TradeNPC, rng)
    x += W_TOWER

    # ── exit approach (right) ────────────────────────────────────────────────
    for bx in range(x, x + W_GARD):
        _castle_set(world, bx, sy, COBBLESTONE)
    _castle_bg(world, x + 1, sy - 1, GARGOYLE_BLOCK)
    _castle_bg(world, x + 3, sy - 1, BOXWOOD_BALL)
    _castle_bg(world, x + 5, sy - 1, BOXWOOD_BALL)
    _castle_bg(world, x + W_GARD - 1, sy - 1, GARGOYLE_BLOCK)


def _place_african_palace(world, left_x: int, sy: int):
    """Sub-Saharan royal compound — Great Zimbabwe / West African style.
    Entry gardens, outer enclosure walls, inner court, elevated throne hall.
    Staff: trade envoy, wildflower quest, shrine keeper, gem quest, jeweler.
    """
    _DOOR = SANDALWOOD_DOOR_CLOSED
    rng = random.Random(left_x ^ (world.seed * 0x9F2D1C4) ^ 0xE3A5B7)
    variant = rng.randint(0, 1)   # 0 = Great Zimbabwe  1 = West African court

    W_GARD   = 8
    W_ENCL   = 10;  H_ENCL   = 7
    W_COURT  = 14;  H_COURT  = 7
    W_THRONE = 18;  H_THRONE = 8
    total_w = W_GARD + W_ENCL + W_COURT + W_THRONE + W_COURT + W_ENCL + W_GARD
    _palace_clear_terrain(world, left_x, sy, total_w, H_THRONE + 12)

    def _enclosure(ex, w, h):
        _castle_fill_bg(world, ex, ex + w, sy - h, sy - 1, AFRICAN_MUD_BRICK)
        for bx in range(ex, ex + w + 1):
            _castle_set(world, bx, sy, SANDSTONE_BLOCK)
        for by in range(sy - h, sy):
            _castle_set(world, ex,      by, AFRICAN_MUD_BRICK)
            _castle_set(world, ex + w,  by, AFRICAN_MUD_BRICK)
        _castle_door(world, ex + w // 2 - 1, sy, door_block=_DOOR)
        # Stepped terracotta parapet
        for bx in range(ex, ex + w + 1):
            _castle_set(world, bx, sy - h, TERRACOTTA_ROOF_TILE)
            if (bx - ex) % 2 == 0:
                _castle_set(world, bx, sy - h - 1, TERRACOTTA_ROOF_TILE)
        _castle_bg(world, ex + 2,      sy - 1, MARIGOLD_BED)
        _castle_bg(world, ex + w - 2,  sy - 1, MARIGOLD_BED)

    x = left_x

    # ── guards at compound entrance ──────────────────────────────────────────
    _palace_npc_at(world, left_x + 1,           sy, GuardNPC, biodome="savanna")
    _palace_npc_at(world, left_x + total_w - 2, sy, GuardNPC, biodome="savanna")

    # ── entry garden (left) ──────────────────────────────────────────────────
    for bx in range(x, x + W_GARD):
        _castle_set(world, bx, sy, SANDSTONE_BLOCK)
    _castle_bg(world, x + 1,           sy - 1, SUNFLOWER_BED)
    _castle_bg(world, x + 3,           sy - 1, MARIGOLD_BED)
    _castle_bg(world, x + 5,           sy - 1, TOPIARY_PEACOCK)
    _castle_bg(world, x + W_GARD // 2, sy - 1, rng.choice(_FOUNTAIN_BLOCKS))
    x += W_GARD

    # ── left outer enclosure ─────────────────────────────────────────────────
    _enclosure(x, W_ENCL, H_ENCL)
    _castle_bg(world, x + W_ENCL // 2, sy - H_ENCL + 3, CHANDELIER)
    if variant == 0:
        _castle_bg(world, x + W_ENCL // 2, sy - 1, CARVED_BENCH)
        _palace_npc_at(world, x + W_ENCL // 2, sy, TradeNPC, rng)
    else:
        _castle_bg(world, x + W_ENCL // 2, sy - 1, STONE_BASIN)
        _palace_npc_at(world, x + W_ENCL // 2, sy, MerchantNPC, rng)
    x += W_ENCL

    # ── left inner court ─────────────────────────────────────────────────────
    _castle_fill_bg(world, x, x + W_COURT, sy - H_COURT, sy - 1, AFRICAN_MUD_BRICK)
    for bx in range(x, x + W_COURT + 1):
        _castle_set(world, bx, sy, SANDSTONE_BLOCK)
    for by in range(sy - H_COURT, sy):
        _castle_set(world, x,           by, AFRICAN_MUD_BRICK)
        _castle_set(world, x + W_COURT, by, AFRICAN_MUD_BRICK)
    _castle_door(world, x, sy, door_block=_DOOR)
    _castle_door(world, x + W_COURT - 2, sy, door_block=_DOOR)
    for bx in range(x, x + W_COURT + 1):
        _castle_set(world, bx, sy - H_COURT, TERRACOTTA_ROOF_TILE)
    _castle_bg(world, x + W_COURT // 2,     sy - 1, rng.choice(_FOUNTAIN_BLOCKS))
    _castle_bg(world, x + 2,               sy - 1, SUNFLOWER_BED)
    _castle_bg(world, x + W_COURT - 2,     sy - 1, SUNFLOWER_BED)
    _castle_bg(world, x + W_COURT // 2,    sy - H_COURT + 3, CHANDELIER)
    if variant == 0:
        _palace_npc_at(world, x + W_COURT // 2, sy, WildflowerQuestNPC, rng, 1,
                       "savanna")
    else:
        _palace_npc_at(world, x + W_COURT // 2, sy, GemQuestNPC, rng, 1, "savanna")
    x += W_COURT

    # ── throne hall — Leader throne (spawned by caller) ───────────────────────
    cx = x + W_THRONE // 2
    _castle_fill_bg(world, x, x + W_THRONE, sy - H_THRONE, sy - 1, AFRICAN_MUD_BRICK)
    for bx in range(x, x + W_THRONE + 1):
        _castle_set(world, bx, sy, SANDSTONE_BLOCK)
    for by in range(sy - H_THRONE, sy):
        _castle_set(world, x,            by, AFRICAN_MUD_BRICK)
        _castle_set(world, x + W_THRONE, by, AFRICAN_MUD_BRICK)
    _castle_door(world, x, sy, door_block=_DOOR)
    _castle_door(world, x + W_THRONE - 2, sy, door_block=_DOOR)
    # Interior mud-brick columns
    for col_x in (x + 3, x + W_THRONE - 3):
        for by in range(sy - H_THRONE + 3, sy):
            _castle_bg(world, col_x, by, AFRICAN_MUD_BRICK)
    # Stepped pyramid parapet
    for step in range(1, 5):
        step_y = sy - H_THRONE - step
        if not (0 <= step_y < world.height):
            break
        for bx in range(x + step * 2, x + W_THRONE + 1 - step * 2):
            _castle_set(world, bx, step_y, TERRACOTTA_ROOF_TILE)
    for bx in range(x, x + W_THRONE + 1):
        _castle_set(world, bx, sy - H_THRONE, TERRACOTTA_ROOF_TILE)
    # Throne dais
    _castle_bg(world, cx,     sy - 1, CARVED_BENCH)
    _castle_bg(world, cx - 3, sy - 1, SUNFLOWER_BED)
    _castle_bg(world, cx + 3, sy - 1, SUNFLOWER_BED)
    _castle_bg(world, cx - 5, sy - 1, STAR_LAMP)
    _castle_bg(world, cx + 5, sy - 1, STAR_LAMP)
    _castle_bg(world, cx,     sy - H_THRONE + 4, CHANDELIER)
    _castle_bg(world, cx - 3, sy - H_THRONE + 6, CANDELABRA)
    _castle_bg(world, cx + 3, sy - H_THRONE + 6, CANDELABRA)
    x += W_THRONE

    # ── right inner court ────────────────────────────────────────────────────
    _castle_fill_bg(world, x, x + W_COURT, sy - H_COURT, sy - 1, AFRICAN_MUD_BRICK)
    for bx in range(x, x + W_COURT + 1):
        _castle_set(world, bx, sy, SANDSTONE_BLOCK)
    for by in range(sy - H_COURT, sy):
        _castle_set(world, x,           by, AFRICAN_MUD_BRICK)
        _castle_set(world, x + W_COURT, by, AFRICAN_MUD_BRICK)
    _castle_door(world, x, sy, door_block=_DOOR)
    _castle_door(world, x + W_COURT - 2, sy, door_block=_DOOR)
    for bx in range(x, x + W_COURT + 1):
        _castle_set(world, bx, sy - H_COURT, TERRACOTTA_ROOF_TILE)
    _castle_bg(world, x + W_COURT // 2,     sy - 1, rng.choice(_FOUNTAIN_BLOCKS))
    _castle_bg(world, x + 2,               sy - 1, MARIGOLD_BED)
    _castle_bg(world, x + W_COURT - 2,     sy - 1, MARIGOLD_BED)
    _castle_bg(world, x + W_COURT // 2,    sy - H_COURT + 3, CHANDELIER)
    if variant == 0:
        _palace_npc_at(world, x + W_COURT // 2, sy, ShrineKeeperNPC, rng,
                       biodome="savanna")
    else:
        _palace_npc_at(world, x + W_COURT // 2, sy, JewelryMerchantNPC, rng)
    x += W_COURT

    # ── right outer enclosure ────────────────────────────────────────────────
    _enclosure(x, W_ENCL, H_ENCL)
    _castle_bg(world, x + W_ENCL // 2, sy - H_ENCL + 3, CHANDELIER)
    if variant == 0:
        _castle_bg(world, x + W_ENCL // 2, sy - 1, MARIGOLD_BED)
        _palace_npc_at(world, x + W_ENCL // 2, sy, GemQuestNPC, rng, 1, "savanna")
    else:
        _castle_bg(world, x + W_ENCL // 2, sy - 1, SUNFLOWER_BED)
        _palace_npc_at(world, x + W_ENCL // 2, sy, WildflowerQuestNPC, rng, 1,
                       "savanna")
    x += W_ENCL

    # ── exit garden (right) ──────────────────────────────────────────────────
    for bx in range(x, x + W_GARD):
        _castle_set(world, bx, sy, SANDSTONE_BLOCK)
    _castle_bg(world, x + 1,           sy - 1, TOPIARY_PEACOCK)
    _castle_bg(world, x + 3,           sy - 1, SUNFLOWER_BED)
    _castle_bg(world, x + 5,           sy - 1, MARIGOLD_BED)
    _castle_bg(world, x + W_GARD // 2, sy - 1, rng.choice(_FOUNTAIN_BLOCKS))


def _place_byzantine_palace(world, left_x: int, sy: int):
    """Byzantine Imperial palace — chrysotriklinos throne room, portico wings,
    naos halls, Greek key friezes.  Staff: scholar, trade envoy, gem quest, jeweler.
    """
    _DOOR = BRONZE_DOOR_CLOSED
    rng = random.Random(left_x ^ (world.seed * 0x4E8F2A1) ^ 0xC9D7B5)
    variant = rng.randint(0, 1)   # 0 = Macedonian dynasty  1 = Komnenian era

    W_GARD   = 8
    W_PORT   = 10;  H_PORT   = 7
    W_NAOS   = 14;  H_NAOS   = 7
    W_THRONE = 22;  H_THRONE = 9
    total_w = W_GARD + W_PORT + W_NAOS + W_THRONE + W_NAOS + W_PORT + W_GARD
    _palace_clear_terrain(world, left_x, sy, total_w, H_THRONE + 14)

    def _byz_room(lx, w, h):
        _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, LIMESTONE_BLOCK)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy, ROMAN_MOSAIC)
        for by in range(sy - h, sy):
            _castle_set(world, lx,      by, LIMESTONE_BLOCK)
            _castle_set(world, lx + w,  by, LIMESTONE_BLOCK)
        _castle_door(world, lx, sy, door_block=_DOOR)
        _castle_door(world, lx + w - 2, sy, door_block=_DOOR)
        # Greek key frieze near top
        for bx in range(lx + 1, lx + w, 2):
            _castle_bg(world, bx, sy - h + 2, GREEK_KEY)
        # Palace portal over doorways
        for by in range(sy - 5, sy):
            _castle_bg(world, lx + 1, by, PALACE_PORTAL)
            _castle_bg(world, lx + w - 1, by, PALACE_PORTAL)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy - h, LIMESTONE_BLOCK)

    x = left_x

    # ── guards at compound entrance ──────────────────────────────────────────
    _palace_npc_at(world, left_x + 1,           sy, GuardNPC, biodome="mediterranean")
    _palace_npc_at(world, left_x + total_w - 2, sy, GuardNPC, biodome="mediterranean")

    # ── approach garden (left) ───────────────────────────────────────────────
    for bx in range(x, x + W_GARD):
        _castle_set(world, bx, sy, COBBLESTONE)
    _castle_bg(world, x + 1,           sy - 1, GREEK_AMPHORA)
    _castle_bg(world, x + 3,           sy - 1, MARBLE_STATUE)
    _castle_bg(world, x + 4,           sy - 2, MARBLE_PLINTH)
    _castle_bg(world, x + 5,           sy - 1, GREEK_AMPHORA)
    x += W_GARD

    # ── left portico ─────────────────────────────────────────────────────────
    _byz_room(x, W_PORT, H_PORT)
    _castle_bg(world, x + W_PORT // 2, sy - H_PORT + 3, CHANDELIER)
    _castle_bg(world, x + 2,           sy - 1, GREEK_AMPHORA)
    _castle_bg(world, x + W_PORT - 2,  sy - 1, GREEK_AMPHORA)
    if variant == 0:
        _castle_bg(world, x + W_PORT // 2, sy - 1, STONE_BASIN)
        _palace_npc_at(world, x + W_PORT // 2, sy, ScholarNPC, rng, "mediterranean")
    else:
        _castle_bg(world, x + W_PORT // 2, sy - 1, CANDELABRA)
        _palace_npc_at(world, x + W_PORT // 2, sy, WildflowerQuestNPC, rng, 1,
                       "mediterranean")
    x += W_PORT

    # ── left naos hall ───────────────────────────────────────────────────────
    _byz_room(x, W_NAOS, H_NAOS)
    _castle_bg(world, x + W_NAOS // 2, sy - H_NAOS + 3, CHANDELIER)
    _castle_bg(world, x + 2,           sy - 1, GREEK_AMPHORA)
    _castle_bg(world, x + W_NAOS - 2,  sy - 1, GREEK_AMPHORA)
    for bx in range(x + 1, x + W_NAOS, 2):
        _castle_bg(world, bx, sy - H_NAOS + 2, GREEK_KEY)
    if variant == 0:
        _castle_bg(world, x + W_NAOS // 2, sy - 1, CARVED_BENCH)
        _palace_npc_at(world, x + W_NAOS // 2, sy, TradeNPC, rng)
    else:
        _castle_bg(world, x + W_NAOS // 2, sy - 1, CANDELABRA)
        _palace_npc_at(world, x + W_NAOS // 2, sy, JewelryMerchantNPC, rng)
    x += W_NAOS

    # ── chrysotriklinos throne room — Leader throne (spawned by caller) ───────
    cx = x + W_THRONE // 2
    _castle_fill_bg(world, x, x + W_THRONE, sy - H_THRONE, sy - 1, LIMESTONE_BLOCK)
    for bx in range(x, x + W_THRONE + 1):
        _castle_set(world, bx, sy, ROMAN_MOSAIC)
    for by in range(sy - H_THRONE, sy):
        _castle_set(world, x,            by, LIMESTONE_BLOCK)
        _castle_set(world, x + W_THRONE, by, LIMESTONE_BLOCK)
    _castle_door(world, x, sy, door_block=_DOOR)
    _castle_door(world, x + W_THRONE - 2, sy, door_block=_DOOR)
    # Interior limestone columns
    for col_x in (x + 4, x + W_THRONE - 4):
        for by in range(sy - H_THRONE + 4, sy):
            _castle_bg(world, col_x, by, LIMESTONE_BLOCK)
    # Greek key band
    for bx in range(x + 1, x + W_THRONE, 2):
        _castle_bg(world, bx, sy - H_THRONE + 2, GREEK_KEY)
    # Stepped dome (limestone)
    for step in range(1, 7):
        step_y = sy - H_THRONE - step
        if not (0 <= step_y < world.height):
            break
        for bx in range(x + step * 2, x + W_THRONE + 1 - step * 2):
            _castle_set(world, bx, step_y, LIMESTONE_BLOCK)
    for bx in range(x, x + W_THRONE + 1):
        _castle_set(world, bx, sy - H_THRONE, LIMESTONE_BLOCK)
    # Mid-floor gallery
    mid = sy - H_THRONE // 2
    for bx in range(x + 1, x + W_THRONE):
        _castle_set(world, bx, mid, ROMAN_MOSAIC)
    # Throne dais
    _castle_bg(world, cx,     sy - 1, MARBLE_PLINTH)
    _castle_bg(world, cx,     sy - 2, VICTORY_STELE)
    _castle_bg(world, cx - 2, sy - 1, GREEK_AMPHORA)
    _castle_bg(world, cx + 2, sy - 1, GREEK_AMPHORA)
    _castle_bg(world, cx - 4, sy - 1, CANDELABRA)
    _castle_bg(world, cx + 4, sy - 1, CANDELABRA)
    _castle_bg(world, cx,     sy - H_THRONE + 4, CHANDELIER)
    _castle_bg(world, cx - 3, sy - H_THRONE + 6, CANDELABRA)
    _castle_bg(world, cx + 3, sy - H_THRONE + 6, CANDELABRA)
    x += W_THRONE

    # ── right naos hall ──────────────────────────────────────────────────────
    _byz_room(x, W_NAOS, H_NAOS)
    _castle_bg(world, x + W_NAOS // 2, sy - H_NAOS + 3, CHANDELIER)
    _castle_bg(world, x + 2,           sy - 1, GREEK_AMPHORA)
    _castle_bg(world, x + W_NAOS - 2,  sy - 1, GREEK_AMPHORA)
    for bx in range(x + 1, x + W_NAOS, 2):
        _castle_bg(world, bx, sy - H_NAOS + 2, GREEK_KEY)
    if variant == 0:
        _castle_bg(world, x + W_NAOS // 2, sy - 1, MARBLE_PLINTH)
        _palace_npc_at(world, x + W_NAOS // 2, sy, GemQuestNPC, rng, 1,
                       "mediterranean")
    else:
        _castle_bg(world, x + W_NAOS // 2, sy - 1, STONE_BASIN)
        _palace_npc_at(world, x + W_NAOS // 2, sy, MerchantNPC, rng)
    x += W_NAOS

    # ── right portico ────────────────────────────────────────────────────────
    _byz_room(x, W_PORT, H_PORT)
    _castle_bg(world, x + W_PORT // 2, sy - H_PORT + 3, CHANDELIER)
    _castle_bg(world, x + 2,           sy - 1, GREEK_AMPHORA)
    _castle_bg(world, x + W_PORT - 2,  sy - 1, GREEK_AMPHORA)
    if variant == 0:
        _castle_bg(world, x + W_PORT // 2, sy - 1, CANDELABRA)
        _palace_npc_at(world, x + W_PORT // 2, sy, JewelryMerchantNPC, rng)
    else:
        _castle_bg(world, x + W_PORT // 2, sy - 1, CARVED_BENCH)
        _palace_npc_at(world, x + W_PORT // 2, sy, TradeNPC, rng)
    x += W_PORT

    # ── approach garden (right) ──────────────────────────────────────────────
    for bx in range(x, x + W_GARD):
        _castle_set(world, bx, sy, COBBLESTONE)
    _castle_bg(world, x + 1,           sy - 1, GREEK_AMPHORA)
    _castle_bg(world, x + 3,           sy - 1, MARBLE_PLINTH)
    _castle_bg(world, x + 3,           sy - 2, MARBLE_STATUE)
    _castle_bg(world, x + 5,           sy - 1, GREEK_AMPHORA)


def _place_tibetan_palace(world, left_x: int, sy: int):
    """Tibetan Potala-style palace-fortress — monastery yards, whitewashed wings,
    inner court, soaring central tower.  Staff: shrine keeper, wildflower quest, scholar.
    """
    _DOOR = CRIMSON_CEDAR_DOOR_CLOSED
    rng = random.Random(left_x ^ (world.seed * 0xB6E3C2A) ^ 0x4F8D19)
    variant = rng.randint(0, 1)   # 0 = Gelug monastery  1 = Bon royal court

    W_YARD  = 8
    W_WING  = 12;  H_WING  = 7
    W_COURT = 14;  H_COURT = 7
    W_TOWER = 20;  H_TOWER = 11
    total_w = W_YARD + W_WING + W_COURT + W_TOWER + W_COURT + W_WING + W_YARD
    _palace_clear_terrain(world, left_x, sy, total_w, H_TOWER + 14)

    def _tibet_room(lx, w, h):
        _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, WHITEWASHED_WALL)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy, GRANITE_ASHLAR)
        for by in range(sy - h, sy):
            _castle_set(world, lx,      by, WHITEWASHED_WALL)
            _castle_set(world, lx + w,  by, WHITEWASHED_WALL)
        _castle_door(world, lx, sy, door_block=_DOOR)
        _castle_door(world, lx + w - 2, sy, door_block=_DOOR)
        for bx in range(lx + 1, lx + w, 2):
            _castle_bg(world, bx, sy - 4, MANI_STONE)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy - h, MONASTERY_ROOF)
        # Prayer flags above roofline
        _castle_bg(world, lx + 2,     sy - h - 1, PRAYER_FLAG_BLOCK)
        _castle_bg(world, lx + w - 2, sy - h - 1, PRAYER_FLAG_BLOCK)

    x = left_x

    # ── guards at compound entrance ──────────────────────────────────────────
    _palace_npc_at(world, left_x + 1,           sy, GuardNPC, biodome="alpine_mountain")
    _palace_npc_at(world, left_x + total_w - 2, sy, GuardNPC, biodome="alpine_mountain")

    # ── monastery yard (left) ────────────────────────────────────────────────
    for bx in range(x, x + W_YARD):
        _castle_set(world, bx, sy, GRANITE_ASHLAR)
    _castle_bg(world, x + 1, sy - 1, MANI_STONE)
    _castle_bg(world, x + 3, sy - 1, MANI_STONE)
    # Tall prayer flag poles
    for py in range(1, 5):
        _castle_bg(world, x + 5, sy - py, PRAYER_FLAG_BLOCK)
    _castle_bg(world, x + W_YARD - 1, sy - 1, MANI_STONE)
    x += W_YARD

    # ── left wing ───────────────────────────────────────────────────────────
    _tibet_room(x, W_WING, H_WING)
    _castle_bg(world, x + W_WING // 2, sy - H_WING + 3, CHANDELIER)
    _castle_bg(world, x + 2,           sy - 1, MANI_STONE)
    _castle_bg(world, x + W_WING - 2,  sy - 1, MANI_STONE)
    if variant == 0:
        _castle_bg(world, x + W_WING // 2, sy - 1, STONE_BASIN)
        _palace_npc_at(world, x + W_WING // 2, sy, ShrineKeeperNPC, rng,
                       biodome="alpine_mountain")
    else:
        _castle_bg(world, x + W_WING // 2, sy - 1, CARVED_BENCH)
        _palace_npc_at(world, x + W_WING // 2, sy, ScholarNPC, rng,
                       "alpine_mountain")
    x += W_WING

    # ── left inner court ─────────────────────────────────────────────────────
    _castle_fill_bg(world, x, x + W_COURT, sy - H_COURT, sy - 1, WHITEWASHED_WALL)
    for bx in range(x, x + W_COURT + 1):
        _castle_set(world, bx, sy, GRANITE_ASHLAR)
    for by in range(sy - H_COURT, sy):
        _castle_set(world, x,            by, WHITEWASHED_WALL)
        _castle_set(world, x + W_COURT,  by, WHITEWASHED_WALL)
    _castle_door(world, x, sy, door_block=_DOOR)
    _castle_door(world, x + W_COURT - 2, sy, door_block=_DOOR)
    for bx in range(x, x + W_COURT + 1):
        _castle_set(world, bx, sy - H_COURT, MONASTERY_ROOF)
    for bx in range(x + 1, x + W_COURT, 2):
        _castle_bg(world, bx, sy - 4, MANI_STONE)
    # Center prayer flag pole
    for py in range(1, 5):
        _castle_bg(world, x + W_COURT // 2, sy - H_COURT - py, PRAYER_FLAG_BLOCK)
    _castle_bg(world, x + W_COURT // 2,     sy - 1, rng.choice(_FOUNTAIN_BLOCKS))
    _castle_bg(world, x + 2,               sy - 1, MANI_STONE)
    _castle_bg(world, x + W_COURT - 2,     sy - 1, MANI_STONE)
    _castle_bg(world, x + W_COURT // 2,    sy - H_COURT + 3, STAR_LAMP)
    if variant == 0:
        _palace_npc_at(world, x + W_COURT // 2, sy, WildflowerQuestNPC, rng, 1,
                       "alpine_mountain")
    else:
        _palace_npc_at(world, x + W_COURT // 2, sy, GemQuestNPC, rng, 1,
                       "alpine_mountain")
    x += W_COURT

    # ── central Potala tower — Leader throne (spawned by caller) ─────────────
    cx = x + W_TOWER // 2
    _castle_fill_bg(world, x, x + W_TOWER, sy - H_TOWER, sy - 1, MANI_STONE)
    for bx in range(x, x + W_TOWER + 1):
        _castle_set(world, bx, sy, GRANITE_ASHLAR)
    # Stone base (lower 3 rows)
    for by in range(sy - 3, sy):
        _castle_set(world, x,            by, GRANITE_ASHLAR)
        _castle_set(world, x + W_TOWER,  by, GRANITE_ASHLAR)
    for by in range(sy - H_TOWER, sy - 3):
        _castle_set(world, x,            by, WHITEWASHED_WALL)
        _castle_set(world, x + W_TOWER,  by, WHITEWASHED_WALL)
    _castle_door(world, x, sy, door_block=_DOOR)
    _castle_door(world, x + W_TOWER - 2, sy, door_block=_DOOR)
    # Interior columns
    for col_x in (x + 4, x + W_TOWER - 4):
        for by in range(sy - H_TOWER + 4, sy):
            _castle_bg(world, col_x, by, WHITEWASHED_WALL)
    # Mid-floor gallery
    mid = sy - H_TOWER // 2
    for bx in range(x + 1, x + W_TOWER):
        _castle_set(world, bx, mid, GRANITE_ASHLAR)
    # Mani stone bg walls
    for bx in range(x + 1, x + W_TOWER, 3):
        _castle_bg(world, bx, sy - 6, MANI_STONE)
        _castle_bg(world, bx, sy - 7, MANI_STONE)
    # Stepped monastery roof
    for bx in range(x, x + W_TOWER + 1):
        _castle_set(world, bx, sy - H_TOWER, MONASTERY_ROOF)
    for step in range(1, 6):
        step_y = sy - H_TOWER - step
        if not (0 <= step_y < world.height):
            break
        for bx in range(x + step * 2, x + W_TOWER + 1 - step * 2):
            _castle_set(world, bx, step_y, MONASTERY_ROOF)
    # Prayer flags above tower
    for py in range(1, 5):
        _castle_bg(world, x + 2,          sy - H_TOWER - py, PRAYER_FLAG_BLOCK)
        _castle_bg(world, x + W_TOWER - 2, sy - H_TOWER - py, PRAYER_FLAG_BLOCK)
    # Throne dais
    _castle_bg(world, cx,     sy - 1, MARBLE_PLINTH)
    _castle_bg(world, cx,     sy - 2, CARVED_BENCH)
    _castle_bg(world, cx - 4, sy - 1, STAR_LAMP)
    _castle_bg(world, cx + 4, sy - 1, STAR_LAMP)
    _castle_bg(world, cx - 6, sy - 1, MANI_STONE)
    _castle_bg(world, cx + 6, sy - 1, MANI_STONE)
    _castle_bg(world, cx,     sy - H_TOWER + 5, CHANDELIER)
    _castle_bg(world, cx - 3, sy - H_TOWER + 7, STAR_LAMP)
    _castle_bg(world, cx + 3, sy - H_TOWER + 7, STAR_LAMP)
    x += W_TOWER

    # ── right inner court ────────────────────────────────────────────────────
    _castle_fill_bg(world, x, x + W_COURT, sy - H_COURT, sy - 1, WHITEWASHED_WALL)
    for bx in range(x, x + W_COURT + 1):
        _castle_set(world, bx, sy, GRANITE_ASHLAR)
    for by in range(sy - H_COURT, sy):
        _castle_set(world, x,            by, WHITEWASHED_WALL)
        _castle_set(world, x + W_COURT,  by, WHITEWASHED_WALL)
    _castle_door(world, x, sy, door_block=_DOOR)
    _castle_door(world, x + W_COURT - 2, sy, door_block=_DOOR)
    for bx in range(x, x + W_COURT + 1):
        _castle_set(world, bx, sy - H_COURT, MONASTERY_ROOF)
    for bx in range(x + 1, x + W_COURT, 2):
        _castle_bg(world, bx, sy - 4, MANI_STONE)
    for py in range(1, 5):
        _castle_bg(world, x + W_COURT // 2, sy - H_COURT - py, PRAYER_FLAG_BLOCK)
    _castle_bg(world, x + W_COURT // 2,     sy - 1, rng.choice(_FOUNTAIN_BLOCKS))
    _castle_bg(world, x + 2,               sy - 1, MANI_STONE)
    _castle_bg(world, x + W_COURT - 2,     sy - 1, MANI_STONE)
    _castle_bg(world, x + W_COURT // 2,    sy - H_COURT + 3, STAR_LAMP)
    if variant == 0:
        _palace_npc_at(world, x + W_COURT // 2, sy, MerchantNPC, rng)
    else:
        _palace_npc_at(world, x + W_COURT // 2, sy, TradeNPC, rng)
    x += W_COURT

    # ── right wing ───────────────────────────────────────────────────────────
    _tibet_room(x, W_WING, H_WING)
    _castle_bg(world, x + W_WING // 2, sy - H_WING + 3, CHANDELIER)
    _castle_bg(world, x + 2,           sy - 1, MANI_STONE)
    _castle_bg(world, x + W_WING - 2,  sy - 1, MANI_STONE)
    if variant == 0:
        _castle_bg(world, x + W_WING // 2, sy - 1, CARVED_BENCH)
        _palace_npc_at(world, x + W_WING // 2, sy, WildflowerQuestNPC, rng, 1,
                       "alpine_mountain")
    else:
        _castle_bg(world, x + W_WING // 2, sy - 1, STONE_BASIN)
        _palace_npc_at(world, x + W_WING // 2, sy, GemQuestNPC, rng, 1,
                       "alpine_mountain")
    x += W_WING

    # ── monastery yard (right) ───────────────────────────────────────────────
    for bx in range(x, x + W_YARD):
        _castle_set(world, bx, sy, GRANITE_ASHLAR)
    _castle_bg(world, x + 1,           sy - 1, MANI_STONE)
    for py in range(1, 5):
        _castle_bg(world, x + 3, sy - py, PRAYER_FLAG_BLOCK)
    _castle_bg(world, x + 5,           sy - 1, MANI_STONE)
    _castle_bg(world, x + W_YARD - 1,  sy - 1, MANI_STONE)


def _place_japanese_palace(world, left_x: int, sy: int):
    """Feudal shiro compound — zen garden approach, flanking yagura towers, shoin halls,
    five-tier tenshu keep.  Staff: shrine keeper, court steward, palace chef, gem scholar.
    """
    _DOOR = SHOJI_DOOR_CLOSED
    rng = random.Random(left_x ^ (world.seed * 0x5A3C1D7) ^ 0xE2F9B4)
    variant = rng.randint(0, 1)   # 0 = shogunate fortress  1 = daimyo castle

    W_ZEN   = 10                      # zen garden approach
    W_YAG   = 10;  H_YAG  = 7        # flanking yagura corner tower
    W_SHOIN = 14;  H_SHOIN = 7        # shoin reception hall
    W_KEEP  = 16;  H_KEEP  = 10       # central tenshu keep
    total_w = W_ZEN + W_YAG + W_SHOIN + W_KEEP + W_SHOIN + W_YAG + W_ZEN
    _palace_clear_terrain(world, left_x, sy, total_w, H_KEEP + 14)

    def _shoin_room(lx, w, h):
        _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, PINE_PLANK_WALL)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy, TATAMI_PAVING)
        for by in range(sy - h, sy):
            _castle_set(world, lx,       by, PINE_PLANK_WALL)
            _castle_set(world, lx + w,   by, PINE_PLANK_WALL)
        _castle_door(world, lx, sy, door_block=_DOOR)
        _castle_door(world, lx + w - 2, sy, door_block=_DOOR)
        for bx in range(lx + 1, lx + w, 2):
            _castle_bg(world, bx, sy - 3, JAPANESE_SHOJI)
            _castle_bg(world, bx, sy - 4, JAPANESE_SHOJI)
        for tier in range(2):
            base_y = sy - h - 1 - tier * 2
            for bx in range(lx - 1 + tier, lx + w + 2 - tier):
                _castle_set(world, bx, base_y, PAGODA_EAVE)
            for bx in range(lx + tier, lx + w + 1 - tier):
                _castle_set(world, bx, base_y - 1, PINE_PLANK_WALL)

    def _yagura_tower(lx, w, h):
        _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, PINE_PLANK_WALL)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy, GRANITE_ASHLAR)
        for by in range(sy - h, sy):
            _castle_set(world, lx,       by, PINE_PLANK_WALL)
            _castle_set(world, lx + w,   by, PINE_PLANK_WALL)
        for bx in range(lx + 1, lx + w, 2):
            _castle_bg(world, bx, sy - 5, JAPANESE_SHOJI)
        for tier in range(3):
            base_y = sy - h - 1 - tier * 2
            for bx in range(lx - 1 + tier, lx + w + 2 - tier):
                _castle_set(world, bx, base_y, PAGODA_EAVE)
            for bx in range(lx + tier, lx + w + 1 - tier):
                _castle_set(world, bx, base_y - 1, PINE_PLANK_WALL)

    def _zen_garden(lx, w):
        for bx in range(lx, lx + w):
            _castle_set(world, bx, sy, TATAMI_PAVING)
        _castle_bg(world, lx + 1,      sy - 1, TORO_LANTERN)
        _castle_bg(world, lx + 2,      sy - 1, PINE_TOPIARY_JP)
        _castle_bg(world, lx + 4,      sy - 1, KOI_POOL)
        _castle_bg(world, lx + w - 2,  sy - 1, PINE_TOPIARY_JP)
        _castle_bg(world, lx + w - 1,  sy - 1, YUKIMI_LANTERN)

    x = left_x

    # ── guards ───────────────────────────────────────────────────────────────
    _palace_npc_at(world, left_x + 1,           sy, GuardNPC, biodome="east_asian")
    _palace_npc_at(world, left_x + total_w - 2, sy, GuardNPC, biodome="east_asian")

    # ── zen garden (left) ────────────────────────────────────────────────────
    _zen_garden(x, W_ZEN)
    _castle_bg(world, x + W_ZEN // 2, sy - 1, RED_ARCH_BRIDGE)
    x += W_ZEN

    # ── left yagura tower ────────────────────────────────────────────────────
    _yagura_tower(x, W_YAG, H_YAG)
    _castle_bg(world, x + W_YAG // 2, sy - H_YAG + 4, STAR_LAMP)
    if variant == 0:
        _castle_bg(world, x + W_YAG // 2, sy - 1, STONE_BASIN)
        _palace_npc_at(world, x + W_YAG // 2, sy, ShrineKeeperNPC, rng,
                       biodome="east_asian")
    else:
        _castle_bg(world, x + W_YAG // 2, sy - 1, STONE_LANTERN)
        _palace_npc_at(world, x + W_YAG // 2, sy, GuardNPC, biodome="east_asian")
    x += W_YAG

    # ── left shoin hall ──────────────────────────────────────────────────────
    _shoin_room(x, W_SHOIN, H_SHOIN)
    _castle_bg(world, x + 2,               sy - 1, BAMBOO_CLUMP)
    _castle_bg(world, x + W_SHOIN - 2,     sy - 1, BAMBOO_CLUMP)
    _castle_bg(world, x + W_SHOIN // 2,    sy - H_SHOIN + 3, CHANDELIER)
    if variant == 0:
        _castle_bg(world, x + W_SHOIN // 2, sy - 1, STONE_BASIN)
        _palace_npc_at(world, x + W_SHOIN // 2, sy, ShrineKeeperNPC, rng,
                       biodome="east_asian")
    else:
        _castle_bg(world, x + W_SHOIN // 2, sy - 1, GARDEN_LANTERN)
        _palace_npc_at(world, x + W_SHOIN // 2, sy, MerchantNPC, rng)
    x += W_SHOIN

    # ── central tenshu keep ──────────────────────────────────────────────────
    cx_keep = x + W_KEEP // 2
    for bx in range(x, x + W_KEEP + 1):
        _castle_set(world, bx, sy, GRANITE_ASHLAR)
    _castle_fill_bg(world, x, x + W_KEEP, sy - H_KEEP, sy - 1, PINE_PLANK_WALL)
    for by in range(sy - H_KEEP, sy):
        _castle_set(world, x,          by, PINE_PLANK_WALL)
        _castle_set(world, x + W_KEEP, by, PINE_PLANK_WALL)
    _castle_door(world, x, sy, door_block=_DOOR)
    _castle_door(world, x + W_KEEP - 2, sy, door_block=_DOOR)
    mid_floor = sy - H_KEEP // 2
    for bx in range(x + 1, x + W_KEEP):
        _castle_set(world, bx, mid_floor, TATAMI_PAVING)
    for bx in range(x + 1, x + W_KEEP, 2):
        _castle_bg(world, bx, sy - 5, JAPANESE_SHOJI)
        _castle_bg(world, bx, sy - 6, JAPANESE_SHOJI)
    for bx in range(x + 1, x + W_KEEP, 2):
        _castle_bg(world, bx, mid_floor - 2, JAPANESE_SHOJI)
        _castle_bg(world, bx, mid_floor - 3, JAPANESE_SHOJI)
    for col_x in (x + 3, x + W_KEEP - 3):
        for by in range(sy - H_KEEP + 4, sy):
            _castle_bg(world, col_x, by, PINE_PLANK_WALL)
        _castle_bg(world, col_x, sy - H_KEEP + 3, TORO_LANTERN)
    _castle_bg(world, cx_keep,     sy - 1, CARVED_BENCH)
    _castle_bg(world, cx_keep - 4, sy - 1, STAR_LAMP)
    _castle_bg(world, cx_keep + 4, sy - 1, STAR_LAMP)
    _castle_bg(world, cx_keep - 6, sy - 1, BAMBOO_CLUMP)
    _castle_bg(world, cx_keep + 6, sy - 1, BAMBOO_CLUMP)
    _castle_bg(world, cx_keep,     sy - H_KEEP + 4, CHANDELIER)
    for tier in range(5):
        base_y = sy - H_KEEP - 1 - tier * 2
        for bx in range(x - 1 + tier, x + W_KEEP + 2 - tier):
            _castle_set(world, bx, base_y, PAGODA_EAVE)
        for bx in range(x + tier, x + W_KEEP + 1 - tier):
            _castle_set(world, bx, base_y - 1, PINE_PLANK_WALL)
    x += W_KEEP

    # ── right shoin hall ─────────────────────────────────────────────────────
    _shoin_room(x, W_SHOIN, H_SHOIN)
    _castle_bg(world, x + 2,               sy - 1, JAPANESE_MAPLE)
    _castle_bg(world, x + W_SHOIN - 2,     sy - 1, JAPANESE_MAPLE)
    _castle_bg(world, x + W_SHOIN // 2,    sy - H_SHOIN + 3, CHANDELIER)
    if variant == 0:
        _castle_bg(world, x + W_SHOIN // 2, sy - 1, SHISHI_ODOSHI)
        _palace_npc_at(world, x + W_SHOIN // 2, sy, RestaurantNPC, rng, "east_asian")
    else:
        _castle_bg(world, x + W_SHOIN // 2, sy - 1, STONE_LANTERN)
        _palace_npc_at(world, x + W_SHOIN // 2, sy, GemQuestNPC, rng, 1, "east_asian")
    x += W_SHOIN

    # ── right yagura tower ───────────────────────────────────────────────────
    _yagura_tower(x, W_YAG, H_YAG)
    _castle_bg(world, x + W_YAG // 2, sy - H_YAG + 4, STAR_LAMP)
    if variant == 0:
        _castle_bg(world, x + W_YAG // 2, sy - 1, STONE_LANTERN)
        _palace_npc_at(world, x + W_YAG // 2, sy, TradeNPC, rng)
    else:
        _castle_bg(world, x + W_YAG // 2, sy - 1, STONE_BASIN)
        _palace_npc_at(world, x + W_YAG // 2, sy, MerchantNPC, rng)
    x += W_YAG

    # ── zen garden (right) ───────────────────────────────────────────────────
    _zen_garden(x, W_ZEN)
    _castle_bg(world, x + W_ZEN // 2, sy - 1, RED_ARCH_BRIDGE)


def _place_chinese_palace(world, left_x: int, sy: int):
    """Imperial Gugong compound — ceremonial pailou gates, formal outer courts, gallery wings,
    grand Taihe throne hall.  Staff: court scholar, steward, gem merchant, palace chef.
    """
    _DOOR = VERMILION_DOOR_CLOSED
    rng = random.Random(left_x ^ (world.seed * 0x8D2E4F1) ^ 0xA3C7B9)
    variant = rng.randint(0, 1)   # 0 = Ming dynasty  1 = Qing dynasty

    W_GATE   = 10                        # ceremonial pailou gate approach
    W_OUTER  = 16;  H_OUTER  = 7        # outer ceremonial court
    W_WING   = 12;  H_WING   = 7        # side gallery wing
    W_THRONE = 22;  H_THRONE = 8        # central Taihe throne hall
    total_w  = W_GATE + W_OUTER + W_WING + W_THRONE + W_WING + W_OUTER + W_GATE
    _palace_clear_terrain(world, left_x, sy, total_w, H_THRONE + 14)

    def _chin_room(lx, w, h):
        _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, CRIMSON_BRICK)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy, IMPERIAL_PAVING)
        for by in range(sy - h, sy):
            _castle_set(world, lx,       by, CRIMSON_BRICK)
            _castle_set(world, lx + w,   by, CRIMSON_BRICK)
        _castle_door(world, lx, sy, door_block=_DOOR)
        _castle_door(world, lx + w - 2, sy, door_block=_DOOR)
        for bx in range(lx + 1, lx + w, 2):
            _castle_bg(world, bx, sy - 3, LACQUER_PANEL)
            _castle_bg(world, bx, sy - 4, LACQUER_PANEL)
        for tier in range(2):
            base_y = sy - h - 1 - tier * 2
            for bx in range(lx - 1 + tier, lx + w + 2 - tier):
                _castle_set(world, bx, base_y, GLAZED_ROOF_TILE)
            for bx in range(lx + tier, lx + w + 1 - tier):
                _castle_set(world, bx, base_y - 1, CRIMSON_BRICK)

    def _pailou(lx, w):
        for bx in range(lx, lx + w):
            _castle_set(world, bx, sy, IMPERIAL_PAVING)
        mid = lx + w // 2
        for post in (mid - 1, mid + 2):
            for row in range(1, 5):
                _castle_set(world, post, sy - row, CRIMSON_BRICK)
            _castle_set(world, post, sy - 5, DRAGON_TILE)
        for bx in range(mid - 2, mid + 4):
            _castle_set(world, bx, sy - 5, GLAZED_ROOF_TILE)
            _castle_set(world, bx, sy - 6, GLAZED_ROOF_TILE)
        _castle_bg(world, lx + 1,      sy - 1, TOPIARY_DRAGON)
        _castle_bg(world, lx + 2,      sy - 1, CERAMIC_PLANTER)
        _castle_bg(world, lx + w - 2,  sy - 1, CERAMIC_PLANTER)
        _castle_bg(world, lx + w - 1,  sy - 1, TOPIARY_DRAGON)
        _castle_bg(world, lx + w // 2, sy - 1, PAPER_LANTERN)

    x = left_x

    # ── guards ───────────────────────────────────────────────────────────────
    _palace_npc_at(world, left_x + 1,           sy, GuardNPC, biodome="east_asian")
    _palace_npc_at(world, left_x + total_w - 2, sy, GuardNPC, biodome="east_asian")

    # ── pailou gate (left) ───────────────────────────────────────────────────
    _pailou(x, W_GATE)
    x += W_GATE

    # ── left outer court ─────────────────────────────────────────────────────
    _chin_room(x, W_OUTER, H_OUTER)
    _castle_bg(world, x + 2,              sy - 1, TOPIARY_DRAGON)
    _castle_bg(world, x + W_OUTER - 2,    sy - 1, CERAMIC_PLANTER)
    _castle_bg(world, x + W_OUTER // 2,   sy - H_OUTER + 3, CHANDELIER)
    _castle_bg(world, x + 1,              sy - 3, DRAGON_TILE)
    _castle_bg(world, x + W_OUTER - 1,    sy - 3, DRAGON_TILE)
    if variant == 0:
        _castle_bg(world, x + W_OUTER // 2, sy - 1, KOI_POOL)
        _palace_npc_at(world, x + W_OUTER // 2, sy, WildflowerQuestNPC, rng, 1,
                       "east_asian")
    else:
        _castle_bg(world, x + W_OUTER // 2, sy - 1, MOON_GATE)
        _palace_npc_at(world, x + W_OUTER // 2, sy, ShrineKeeperNPC, rng,
                       biodome="east_asian")
    x += W_OUTER

    # ── left gallery wing ────────────────────────────────────────────────────
    _chin_room(x, W_WING, H_WING)
    _castle_bg(world, x + 2,            sy - 1, BAMBOO_CLUMP)
    _castle_bg(world, x + W_WING - 2,   sy - 1, BAMBOO_CLUMP)
    _castle_bg(world, x + W_WING // 2,  sy - H_WING + 3, STAR_LAMP)
    if variant == 0:
        _castle_bg(world, x + W_WING // 2, sy - 1, PAPER_LANTERN)
        _palace_npc_at(world, x + W_WING // 2, sy, MerchantNPC, rng)
    else:
        _castle_bg(world, x + W_WING // 2, sy - 1, JADE_PANEL)
        _palace_npc_at(world, x + W_WING // 2, sy, GemQuestNPC, rng, 1, "east_asian")
    x += W_WING

    # ── central Taihe throne hall ────────────────────────────────────────────
    cx_throne = x + W_THRONE // 2
    _castle_fill_bg(world, x, x + W_THRONE, sy - H_THRONE, sy - 1, CRIMSON_BRICK)
    for bx in range(x, x + W_THRONE + 1):
        _castle_set(world, bx, sy, IMPERIAL_PAVING)
    for by in range(sy - H_THRONE, sy):
        _castle_set(world, x,             by, CRIMSON_BRICK)
        _castle_set(world, x + W_THRONE,  by, CRIMSON_BRICK)
    _castle_door(world, x, sy, door_block=_DOOR)
    _castle_door(world, x + W_THRONE - 2, sy, door_block=_DOOR)
    for bx in range(x + 1, x + W_THRONE, 2):
        _castle_bg(world, bx, sy - 4, LACQUER_PANEL)
        _castle_bg(world, bx, sy - 5, LACQUER_PANEL)
    for bx in range(x + 1, x + W_THRONE, 4):
        _castle_bg(world, bx, sy - H_THRONE + 2, DRAGON_TILE)
    for col_x in (x + 4, x + W_THRONE - 4):
        for by in range(sy - H_THRONE + 3, sy):
            _castle_bg(world, col_x, by, CRIMSON_BRICK)
        _castle_bg(world, col_x, sy - H_THRONE + 2, PAPER_LANTERN)
    _castle_bg(world, cx_throne,     sy - 1, CARVED_BENCH)
    _castle_bg(world, cx_throne - 4, sy - 1, PAPER_LANTERN)
    _castle_bg(world, cx_throne + 4, sy - 1, PAPER_LANTERN)
    _castle_bg(world, cx_throne - 6, sy - 1, TOPIARY_DRAGON)
    _castle_bg(world, cx_throne + 6, sy - 1, TOPIARY_DRAGON)
    for gx in range(cx_throne - 2, cx_throne + 3):
        _castle_bg(world, gx, sy - H_THRONE + 4, GOLDEN_CEILING)
    for tier in range(3):
        base_y = sy - H_THRONE - 1 - tier * 2
        for bx in range(x - 1 + tier, x + W_THRONE + 2 - tier):
            _castle_set(world, bx, base_y, GLAZED_ROOF_TILE)
        for bx in range(x + tier, x + W_THRONE + 1 - tier):
            _castle_set(world, bx, base_y - 1, CRIMSON_BRICK)
    x += W_THRONE

    # ── right gallery wing ───────────────────────────────────────────────────
    _chin_room(x, W_WING, H_WING)
    _castle_bg(world, x + 2,            sy - 1, CERAMIC_PLANTER)
    _castle_bg(world, x + W_WING - 2,   sy - 1, CERAMIC_PLANTER)
    _castle_bg(world, x + W_WING // 2,  sy - H_WING + 3, STAR_LAMP)
    if variant == 0:
        _castle_bg(world, x + W_WING // 2, sy - 1, CERAMIC_SEAT)
        _palace_npc_at(world, x + W_WING // 2, sy, RestaurantNPC, rng, "east_asian")
    else:
        _castle_bg(world, x + W_WING // 2, sy - 1, KOI_POOL)
        _palace_npc_at(world, x + W_WING // 2, sy, JewelryMerchantNPC, rng)
    x += W_WING

    # ── right outer court ────────────────────────────────────────────────────
    _chin_room(x, W_OUTER, H_OUTER)
    _castle_bg(world, x + 2,              sy - 1, TOPIARY_DRAGON)
    _castle_bg(world, x + W_OUTER - 2,    sy - 1, CERAMIC_PLANTER)
    _castle_bg(world, x + W_OUTER // 2,   sy - H_OUTER + 3, CHANDELIER)
    _castle_bg(world, x + 1,              sy - 3, DRAGON_TILE)
    _castle_bg(world, x + W_OUTER - 1,    sy - 3, DRAGON_TILE)
    if variant == 0:
        _castle_bg(world, x + W_OUTER // 2, sy - 1, MOON_GATE)
        _palace_npc_at(world, x + W_OUTER // 2, sy, TradeNPC, rng)
    else:
        _castle_bg(world, x + W_OUTER // 2, sy - 1, KOI_POOL)
        _palace_npc_at(world, x + W_OUTER // 2, sy, MerchantNPC, rng)
    x += W_OUTER

    # ── pailou gate (right) ──────────────────────────────────────────────────
    _pailou(x, W_GATE)


def _place_tang_palace(world, left_x: int, sy: int):
    """Tang dynasty Daming Palace — granite terrace approaches, broad drum towers,
    open colonnade courts, four-eave Hanyuan great hall.
    Staff: court poet, shrine keeper, palace chef, gem merchant.
    """
    _DOOR = VERMILION_DOOR_CLOSED
    rng = random.Random(left_x ^ (world.seed * 0x6B1C3A9) ^ 0xD8E4F2)
    variant = rng.randint(0, 1)   # 0 = early Tang  1 = late Tang

    W_TERR = 10                       # granite terrace approach
    W_DRUM = 12;  H_DRUM = 7         # drum tower
    W_COL  = 14;  H_COL  = 7         # open colonnade court
    W_HANY = 24;  H_HANY = 7         # Hanyuan Hall
    total_w = W_TERR + W_DRUM + W_COL + W_HANY + W_COL + W_DRUM + W_TERR
    _palace_clear_terrain(world, left_x, sy, total_w, H_DRUM + 12)

    def _terrace(lx, w):
        for bx in range(lx, lx + w):
            _castle_set(world, bx, sy, GRANITE_ASHLAR)
        for bx in range(lx + 1, lx + w - 1):
            _castle_set(world, bx, sy - 1, GRANITE_ASHLAR)
        _castle_bg(world, lx + 1,      sy - 2, TOPIARY_DRAGON)
        _castle_bg(world, lx + w - 1,  sy - 2, TOPIARY_DRAGON)
        _castle_bg(world, lx + w // 2, sy - 2, PAPER_LANTERN)

    def _drum_tower(lx, w, h):
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy, GRANITE_ASHLAR)
        _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, CRIMSON_BRICK)
        for by in range(sy - h, sy):
            _castle_set(world, lx,       by, CRIMSON_BRICK)
            _castle_set(world, lx + w,   by, CRIMSON_BRICK)
        for bx in range(lx + 2, lx + w - 1, 3):
            _castle_bg(world, bx, sy - 3, LACQUER_PANEL)
            _castle_bg(world, bx, sy - 4, LACQUER_PANEL)
        _castle_bg(world, lx + w // 2, sy - h + 3, STAR_LAMP)
        for tier in range(4):
            base_y = sy - h - 1 - tier * 2
            for bx in range(lx - 1 + tier, lx + w + 2 - tier):
                _castle_set(world, bx, base_y, GLAZED_ROOF_TILE)
            for bx in range(lx + tier, lx + w + 1 - tier):
                _castle_set(world, bx, base_y - 1, CRIMSON_BRICK)

    def _colonnade(lx, w, h):
        _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, CRIMSON_BRICK)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy, IMPERIAL_PAVING)
        for by in range(sy - h, sy):
            _castle_set(world, lx,       by, CRIMSON_BRICK)
            _castle_set(world, lx + w,   by, CRIMSON_BRICK)
        _castle_door(world, lx, sy, door_block=_DOOR)
        _castle_door(world, lx + w - 2, sy, door_block=_DOOR)
        for col in range(lx + 3, lx + w - 2, 4):
            for by in range(sy - h + 2, sy):
                _castle_bg(world, col, by, CRIMSON_BRICK)
            _castle_bg(world, col, sy - h + 1, DRAGON_TILE)
        for tier in range(2):
            base_y = sy - h - 1 - tier * 2
            for bx in range(lx - 1 + tier, lx + w + 2 - tier):
                _castle_set(world, bx, base_y, GLAZED_ROOF_TILE)
            for bx in range(lx + tier, lx + w + 1 - tier):
                _castle_set(world, bx, base_y - 1, CRIMSON_BRICK)

    x = left_x

    # ── guards ───────────────────────────────────────────────────────────────
    _palace_npc_at(world, left_x + 1,           sy, GuardNPC, biodome="east_asian")
    _palace_npc_at(world, left_x + total_w - 2, sy, GuardNPC, biodome="east_asian")

    # ── left granite terrace ──────────────────────────────────────────────────
    _terrace(x, W_TERR)
    x += W_TERR

    # ── left drum tower ───────────────────────────────────────────────────────
    _drum_tower(x, W_DRUM, H_DRUM)
    if variant == 0:
        _castle_bg(world, x + W_DRUM // 2, sy - 1, STONE_BASIN)
        _palace_npc_at(world, x + W_DRUM // 2, sy, ShrineKeeperNPC, rng,
                       biodome="east_asian")
    else:
        _castle_bg(world, x + W_DRUM // 2, sy - 1, PAPER_LANTERN)
        _palace_npc_at(world, x + W_DRUM // 2, sy, GuardNPC, biodome="east_asian")
    x += W_DRUM

    # ── left colonnade court ──────────────────────────────────────────────────
    _colonnade(x, W_COL, H_COL)
    _castle_bg(world, x + W_COL // 2, sy - H_COL + 3, CHANDELIER)
    if variant == 0:
        _castle_bg(world, x + W_COL // 2, sy - 1, KOI_POOL)
        _palace_npc_at(world, x + W_COL // 2, sy, WildflowerQuestNPC, rng, 1,
                       "east_asian")
    else:
        _castle_bg(world, x + W_COL // 2, sy - 1, CERAMIC_PLANTER)
        _palace_npc_at(world, x + W_COL // 2, sy, MerchantNPC, rng)
    x += W_COL

    # ── Hanyuan Hall (central throne) ─────────────────────────────────────────
    cx = x + W_HANY // 2
    for bx in range(x, x + W_HANY + 1):
        _castle_set(world, bx, sy, GRANITE_ASHLAR)
    _castle_fill_bg(world, x, x + W_HANY, sy - H_HANY, sy - 1, CRIMSON_BRICK)
    for by in range(sy - H_HANY, sy):
        _castle_set(world, x,           by, CRIMSON_BRICK)
        _castle_set(world, x + W_HANY,  by, CRIMSON_BRICK)
    _castle_door(world, x, sy, door_block=_DOOR)
    _castle_door(world, x + W_HANY - 2, sy, door_block=_DOOR)
    for col_x in (x + 5, cx - 4, cx + 4, x + W_HANY - 5):
        for by in range(sy - H_HANY + 3, sy):
            _castle_bg(world, col_x, by, CRIMSON_BRICK)
        _castle_bg(world, col_x, sy - H_HANY + 2, DRAGON_TILE)
    for bx in range(x + 1, x + W_HANY, 3):
        _castle_bg(world, bx, sy - 3, LACQUER_PANEL)
        _castle_bg(world, bx, sy - 4, LACQUER_PANEL)
    _castle_bg(world, cx,     sy - 1, CARVED_BENCH)
    _castle_bg(world, cx - 5, sy - 1, PAPER_LANTERN)
    _castle_bg(world, cx + 5, sy - 1, PAPER_LANTERN)
    _castle_bg(world, cx - 8, sy - 1, TOPIARY_DRAGON)
    _castle_bg(world, cx + 8, sy - 1, TOPIARY_DRAGON)
    for gx in range(cx - 3, cx + 4):
        _castle_bg(world, gx, sy - H_HANY + 4, GOLDEN_CEILING)
    for tier in range(4):
        base_y = sy - H_HANY - 1 - tier * 2
        for bx in range(x - 1 + tier, x + W_HANY + 2 - tier):
            _castle_set(world, bx, base_y, GLAZED_ROOF_TILE)
        for bx in range(x + tier, x + W_HANY + 1 - tier):
            _castle_set(world, bx, base_y - 1, CRIMSON_BRICK)
    x += W_HANY

    # ── right colonnade court ─────────────────────────────────────────────────
    _colonnade(x, W_COL, H_COL)
    _castle_bg(world, x + W_COL // 2, sy - H_COL + 3, CHANDELIER)
    if variant == 0:
        _castle_bg(world, x + W_COL // 2, sy - 1, PAPER_LANTERN)
        _palace_npc_at(world, x + W_COL // 2, sy, RestaurantNPC, rng, "east_asian")
    else:
        _castle_bg(world, x + W_COL // 2, sy - 1, JADE_PANEL)
        _palace_npc_at(world, x + W_COL // 2, sy, GemQuestNPC, rng, 1, "east_asian")
    x += W_COL

    # ── right drum tower ──────────────────────────────────────────────────────
    _drum_tower(x, W_DRUM, H_DRUM)
    if variant == 0:
        _castle_bg(world, x + W_DRUM // 2, sy - 1, PAPER_LANTERN)
        _palace_npc_at(world, x + W_DRUM // 2, sy, TradeNPC, rng)
    else:
        _castle_bg(world, x + W_DRUM // 2, sy - 1, STONE_BASIN)
        _palace_npc_at(world, x + W_DRUM // 2, sy, MerchantNPC, rng)
    x += W_DRUM

    # ── right granite terrace ─────────────────────────────────────────────────
    _terrace(x, W_TERR)


def _place_song_palace(world, left_x: int, sy: int):
    """Song dynasty Lin'an Palace — scholar water gardens, moon gate courts,
    bamboo screen pavilions, refined two-eave Chuigong reception hall.
    Staff: court painter, garden scholar, gem appraiser, palace chef.
    """
    _DOOR = VERMILION_DOOR_CLOSED
    rng = random.Random(left_x ^ (world.seed * 0x4E9A2C7) ^ 0xB5D3F8)
    variant = rng.randint(0, 1)   # 0 = Northern Song  1 = Southern Song

    W_GARDEN = 12                      # scholar water garden approach
    W_MOON   = 10;  H_MOON  = 7       # moon gate court
    W_PAV    = 14;  H_PAV   = 7       # scholar pavilion
    W_HALL   = 18;  H_HALL  = 7       # main Chuigong reception hall
    total_w  = W_GARDEN + W_MOON + W_PAV + W_HALL + W_PAV + W_MOON + W_GARDEN
    _palace_clear_terrain(world, left_x, sy, total_w, H_HALL + 12)

    def _water_garden(lx, w):
        for bx in range(lx, lx + w):
            _castle_set(world, bx, sy, WAVE_CERAMIC)
        _castle_bg(world, lx + 1,      sy - 1, KOI_POOL)
        _castle_bg(world, lx + 3,      sy - 1, BAMBOO_CLUMP)
        _castle_bg(world, lx + w - 3,  sy - 1, BAMBOO_CLUMP)
        _castle_bg(world, lx + w - 1,  sy - 1, CERAMIC_PLANTER)

    def _moon_court(lx, w, h):
        _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, PINE_PLANK_WALL)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy, WAVE_CERAMIC)
        for by in range(sy - h, sy):
            _castle_set(world, lx,       by, PINE_PLANK_WALL)
            _castle_set(world, lx + w,   by, PINE_PLANK_WALL)
        _castle_door(world, lx, sy, door_block=_DOOR)
        _castle_door(world, lx + w - 2, sy, door_block=_DOOR)
        _castle_bg(world, lx + w // 2, sy - 4, MOON_GATE)
        _castle_bg(world, lx + w // 2, sy - 5, MOON_GATE)
        for bx in range(lx + 1, lx + w, 2):
            _castle_bg(world, bx, sy - 2, BAMBOO_SCREEN)
        for tier in range(2):
            base_y = sy - h - 1 - tier * 2
            for bx in range(lx - 1 + tier, lx + w + 2 - tier):
                _castle_set(world, bx, base_y, GLAZED_ROOF_TILE)
            for bx in range(lx + tier, lx + w + 1 - tier):
                _castle_set(world, bx, base_y - 1, PINE_PLANK_WALL)

    def _scholar_pavilion(lx, w, h):
        _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, PINE_PLANK_WALL)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy, WAVE_CERAMIC)
        for by in range(sy - h, sy):
            _castle_set(world, lx,       by, PINE_PLANK_WALL)
            _castle_set(world, lx + w,   by, PINE_PLANK_WALL)
        _castle_door(world, lx, sy, door_block=_DOOR)
        _castle_door(world, lx + w - 2, sy, door_block=_DOOR)
        for bx in range(lx + 1, lx + w, 2):
            _castle_bg(world, bx, sy - 3, BAMBOO_SCREEN)
            _castle_bg(world, bx, sy - 4, BAMBOO_SCREEN)
        for tier in range(2):
            base_y = sy - h - 1 - tier * 2
            for bx in range(lx - 1 + tier, lx + w + 2 - tier):
                _castle_set(world, bx, base_y, GLAZED_ROOF_TILE)
            for bx in range(lx + tier, lx + w + 1 - tier):
                _castle_set(world, bx, base_y - 1, PINE_PLANK_WALL)

    x = left_x

    # ── guards ───────────────────────────────────────────────────────────────
    _palace_npc_at(world, left_x + 1,           sy, GuardNPC, biodome="east_asian")
    _palace_npc_at(world, left_x + total_w - 2, sy, GuardNPC, biodome="east_asian")

    # ── left water garden ─────────────────────────────────────────────────────
    _water_garden(x, W_GARDEN)
    x += W_GARDEN

    # ── left moon gate court ──────────────────────────────────────────────────
    _moon_court(x, W_MOON, H_MOON)
    _castle_bg(world, x + W_MOON // 2, sy - H_MOON + 3, STAR_LAMP)
    if variant == 0:
        _castle_bg(world, x + W_MOON // 2, sy - 1, CERAMIC_SEAT)
        _palace_npc_at(world, x + W_MOON // 2, sy, WildflowerQuestNPC, rng, 1,
                       "east_asian")
    else:
        _castle_bg(world, x + W_MOON // 2, sy - 1, KOI_POOL)
        _palace_npc_at(world, x + W_MOON // 2, sy, ShrineKeeperNPC, rng,
                       biodome="east_asian")
    x += W_MOON

    # ── left scholar pavilion ─────────────────────────────────────────────────
    _scholar_pavilion(x, W_PAV, H_PAV)
    _castle_bg(world, x + 2,            sy - 1, BAMBOO_CLUMP)
    _castle_bg(world, x + W_PAV - 2,    sy - 1, BAMBOO_CLUMP)
    _castle_bg(world, x + W_PAV // 2,   sy - H_PAV + 3, CHANDELIER)
    if variant == 0:
        _castle_bg(world, x + W_PAV // 2, sy - 1, JADE_PANEL)
        _palace_npc_at(world, x + W_PAV // 2, sy, MerchantNPC, rng)
    else:
        _castle_bg(world, x + W_PAV // 2, sy - 1, CERAMIC_PLANTER)
        _palace_npc_at(world, x + W_PAV // 2, sy, GemQuestNPC, rng, 1, "east_asian")
    x += W_PAV

    # ── Chuigong Hall (central throne) ────────────────────────────────────────
    cx = x + W_HALL // 2
    _castle_fill_bg(world, x, x + W_HALL, sy - H_HALL, sy - 1, PINE_PLANK_WALL)
    for bx in range(x, x + W_HALL + 1):
        _castle_set(world, bx, sy, WAVE_CERAMIC)
    for by in range(sy - H_HALL, sy):
        _castle_set(world, x,          by, PINE_PLANK_WALL)
        _castle_set(world, x + W_HALL, by, PINE_PLANK_WALL)
    _castle_door(world, x, sy, door_block=_DOOR)
    _castle_door(world, x + W_HALL - 2, sy, door_block=_DOOR)
    for bx in range(x + 1, x + W_HALL, 2):
        _castle_bg(world, bx, sy - 3, BAMBOO_SCREEN)
        _castle_bg(world, bx, sy - 4, BAMBOO_SCREEN)
    for bx in range(x + 2, x + W_HALL, 5):
        _castle_bg(world, bx, sy - H_HALL + 2, DRAGON_TILE)
    for col_x in (x + 3, x + W_HALL - 3):
        for by in range(sy - H_HALL + 3, sy):
            _castle_bg(world, col_x, by, PINE_PLANK_WALL)
        _castle_bg(world, col_x, sy - H_HALL + 2, PAPER_LANTERN)
    _castle_bg(world, cx,     sy - 1, CARVED_BENCH)
    _castle_bg(world, cx - 3, sy - 1, PAPER_LANTERN)
    _castle_bg(world, cx + 3, sy - 1, PAPER_LANTERN)
    _castle_bg(world, cx - 5, sy - 1, CERAMIC_PLANTER)
    _castle_bg(world, cx + 5, sy - 1, CERAMIC_PLANTER)
    for gx in range(cx - 2, cx + 3):
        _castle_bg(world, gx, sy - H_HALL + 4, GOLDEN_CEILING)
    for tier in range(2):
        base_y = sy - H_HALL - 1 - tier * 2
        for bx in range(x - 1 + tier, x + W_HALL + 2 - tier):
            _castle_set(world, bx, base_y, GLAZED_ROOF_TILE)
        for bx in range(x + tier, x + W_HALL + 1 - tier):
            _castle_set(world, bx, base_y - 1, PINE_PLANK_WALL)
    x += W_HALL

    # ── right scholar pavilion ────────────────────────────────────────────────
    _scholar_pavilion(x, W_PAV, H_PAV)
    _castle_bg(world, x + 2,            sy - 1, CERAMIC_SEAT)
    _castle_bg(world, x + W_PAV - 2,    sy - 1, CERAMIC_SEAT)
    _castle_bg(world, x + W_PAV // 2,   sy - H_PAV + 3, CHANDELIER)
    if variant == 0:
        _castle_bg(world, x + W_PAV // 2, sy - 1, MOON_GATE)
        _palace_npc_at(world, x + W_PAV // 2, sy, RestaurantNPC, rng, "east_asian")
    else:
        _castle_bg(world, x + W_PAV // 2, sy - 1, KOI_POOL)
        _palace_npc_at(world, x + W_PAV // 2, sy, JewelryMerchantNPC, rng)
    x += W_PAV

    # ── right moon gate court ─────────────────────────────────────────────────
    _moon_court(x, W_MOON, H_MOON)
    _castle_bg(world, x + W_MOON // 2, sy - H_MOON + 3, STAR_LAMP)
    if variant == 0:
        _castle_bg(world, x + W_MOON // 2, sy - 1, KOI_POOL)
        _palace_npc_at(world, x + W_MOON // 2, sy, TradeNPC, rng)
    else:
        _castle_bg(world, x + W_MOON // 2, sy - 1, CERAMIC_PLANTER)
        _palace_npc_at(world, x + W_MOON // 2, sy, MerchantNPC, rng)
    x += W_MOON

    # ── right water garden ────────────────────────────────────────────────────
    _water_garden(x, W_GARDEN)


def _place_han_palace(world, left_x: int, sy: int):
    """Han dynasty Weiyang Palace — earthen terrace platforms, stone watchtowers,
    jade-accented ante-halls, austere throne platform.
    Staff: court official, imperial archivist, stone carver, trade minister.
    """
    _DOOR = VERMILION_DOOR_CLOSED
    rng = random.Random(left_x ^ (world.seed * 0x3F7B5D2) ^ 0xC9A1E6)
    variant = rng.randint(0, 1)   # 0 = Western Han  1 = Eastern Han

    W_PLAT   = 10                       # earthen terrace platform approach
    W_WATCH  = 12;  H_WATCH  = 8       # stone watchtower
    W_ANTE   = 12;  H_ANTE   = 7       # ante-hall
    W_THRONE = 20;  H_THRONE = 7       # central Jiaofang throne platform
    total_w  = W_PLAT + W_WATCH + W_ANTE + W_THRONE + W_ANTE + W_WATCH + W_PLAT
    _palace_clear_terrain(world, left_x, sy, total_w, H_WATCH + 12)

    def _platform(lx, w):
        for bx in range(lx, lx + w):
            _castle_set(world, bx, sy, GRANITE_ASHLAR)
        for bx in range(lx + 1, lx + w - 1):
            _castle_set(world, bx, sy - 1, LIMESTONE_BLOCK)
        _castle_bg(world, lx + 2,      sy - 2, STAR_LAMP)
        _castle_bg(world, lx + w - 2,  sy - 2, STAR_LAMP)

    def _watchtower(lx, w, h):
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy, GRANITE_ASHLAR)
        _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, LIMESTONE_BLOCK)
        for by in range(sy - h, sy):
            _castle_set(world, lx,       by, LIMESTONE_BLOCK)
            _castle_set(world, lx + w,   by, LIMESTONE_BLOCK)
        for by in range(sy - h + 3, sy - 2, 4):
            _castle_bg(world, lx + w // 2, by, JADE_PANEL)
        _castle_bg(world, lx + w // 2, sy - h + 3, GARDEN_LANTERN)
        for tier in range(2):
            base_y = sy - h - 1 - tier * 2
            for bx in range(lx - 1 + tier, lx + w + 2 - tier):
                _castle_set(world, bx, base_y, GLAZED_ROOF_TILE)
            for bx in range(lx + tier, lx + w + 1 - tier):
                _castle_set(world, bx, base_y - 1, LIMESTONE_BLOCK)

    def _ante_hall(lx, w, h):
        _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, LIMESTONE_BLOCK)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy, GRANITE_ASHLAR)
        for by in range(sy - h, sy):
            _castle_set(world, lx,       by, LIMESTONE_BLOCK)
            _castle_set(world, lx + w,   by, LIMESTONE_BLOCK)
        _castle_door(world, lx, sy, door_block=_DOOR)
        _castle_door(world, lx + w - 2, sy, door_block=_DOOR)
        for bx in range(lx + 1, lx + w, 2):
            _castle_bg(world, bx, sy - 3, JADE_PANEL)
        for tier in range(2):
            base_y = sy - h - 1 - tier * 2
            for bx in range(lx - 1 + tier, lx + w + 2 - tier):
                _castle_set(world, bx, base_y, GLAZED_ROOF_TILE)
            for bx in range(lx + tier, lx + w + 1 - tier):
                _castle_set(world, bx, base_y - 1, LIMESTONE_BLOCK)

    x = left_x

    # ── guards ───────────────────────────────────────────────────────────────
    _palace_npc_at(world, left_x + 1,           sy, GuardNPC, biodome="east_asian")
    _palace_npc_at(world, left_x + total_w - 2, sy, GuardNPC, biodome="east_asian")

    # ── left terrace platform ─────────────────────────────────────────────────
    _platform(x, W_PLAT)
    x += W_PLAT

    # ── left watchtower ───────────────────────────────────────────────────────
    _watchtower(x, W_WATCH, H_WATCH)
    if variant == 0:
        _castle_bg(world, x + W_WATCH // 2, sy - 1, STONE_BASIN)
        _palace_npc_at(world, x + W_WATCH // 2, sy, GuardNPC, biodome="east_asian")
    else:
        _castle_bg(world, x + W_WATCH // 2, sy - 1, STAR_LAMP)
        _palace_npc_at(world, x + W_WATCH // 2, sy, ShrineKeeperNPC, rng,
                       biodome="east_asian")
    x += W_WATCH

    # ── left ante-hall ────────────────────────────────────────────────────────
    _ante_hall(x, W_ANTE, H_ANTE)
    _castle_bg(world, x + W_ANTE // 2, sy - H_ANTE + 3, STAR_LAMP)
    if variant == 0:
        _castle_bg(world, x + W_ANTE // 2, sy - 1, GARDEN_LANTERN)
        _palace_npc_at(world, x + W_ANTE // 2, sy, MerchantNPC, rng)
    else:
        _castle_bg(world, x + W_ANTE // 2, sy - 1, STONE_BASIN)
        _palace_npc_at(world, x + W_ANTE // 2, sy, TradeNPC, rng)
    x += W_ANTE

    # ── central Jiaofang throne platform ──────────────────────────────────────
    cx = x + W_THRONE // 2
    for bx in range(x, x + W_THRONE + 1):
        _castle_set(world, bx, sy, GRANITE_ASHLAR)
    _castle_fill_bg(world, x, x + W_THRONE, sy - H_THRONE, sy - 1, LIMESTONE_BLOCK)
    for by in range(sy - H_THRONE, sy):
        _castle_set(world, x,             by, LIMESTONE_BLOCK)
        _castle_set(world, x + W_THRONE,  by, LIMESTONE_BLOCK)
    _castle_door(world, x, sy, door_block=_DOOR)
    _castle_door(world, x + W_THRONE - 2, sy, door_block=_DOOR)
    for col_x in (x + 4, x + W_THRONE - 4):
        for by in range(sy - H_THRONE + 3, sy):
            _castle_bg(world, col_x, by, LIMESTONE_BLOCK)
        _castle_bg(world, col_x, sy - H_THRONE + 2, GARDEN_LANTERN)
    for bx in range(x + 1, x + W_THRONE, 4):
        _castle_bg(world, bx, sy - H_THRONE + 2, JADE_PANEL)
    _castle_bg(world, cx,     sy - 1, CARVED_BENCH)
    _castle_bg(world, cx - 4, sy - 1, STAR_LAMP)
    _castle_bg(world, cx + 4, sy - 1, STAR_LAMP)
    _castle_bg(world, cx - 7, sy - 1, STONE_BASIN)
    _castle_bg(world, cx + 7, sy - 1, STONE_BASIN)
    _castle_bg(world, cx,     sy - H_THRONE + 4, CHANDELIER)
    for tier in range(3):
        base_y = sy - H_THRONE - 1 - tier * 2
        for bx in range(x - 1 + tier, x + W_THRONE + 2 - tier):
            _castle_set(world, bx, base_y, GLAZED_ROOF_TILE)
        for bx in range(x + tier, x + W_THRONE + 1 - tier):
            _castle_set(world, bx, base_y - 1, LIMESTONE_BLOCK)
    x += W_THRONE

    # ── right ante-hall ───────────────────────────────────────────────────────
    _ante_hall(x, W_ANTE, H_ANTE)
    _castle_bg(world, x + W_ANTE // 2, sy - H_ANTE + 3, STAR_LAMP)
    if variant == 0:
        _castle_bg(world, x + W_ANTE // 2, sy - 1, STONE_BASIN)
        _palace_npc_at(world, x + W_ANTE // 2, sy, GemQuestNPC, rng, 1, "east_asian")
    else:
        _castle_bg(world, x + W_ANTE // 2, sy - 1, GARDEN_LANTERN)
        _palace_npc_at(world, x + W_ANTE // 2, sy, WildflowerQuestNPC, rng, 1,
                       "east_asian")
    x += W_ANTE

    # ── right watchtower ──────────────────────────────────────────────────────
    _watchtower(x, W_WATCH, H_WATCH)
    if variant == 0:
        _castle_bg(world, x + W_WATCH // 2, sy - 1, STAR_LAMP)
        _palace_npc_at(world, x + W_WATCH // 2, sy, TradeNPC, rng)
    else:
        _castle_bg(world, x + W_WATCH // 2, sy - 1, STONE_BASIN)
        _palace_npc_at(world, x + W_WATCH // 2, sy, MerchantNPC, rng)
    x += W_WATCH

    # ── right terrace platform ────────────────────────────────────────────────
    _platform(x, W_PLAT)


def _place_east_african_palace(world, left_x: int, sy: int):
    """Aksumite / East African palace — obelisk forecourt, carved granite gate towers,
    stepped throne hall.  Staff: trade envoy, gem quest, shrine keeper, jeweler.
    """
    _DOOR = SWAHILI_DOOR_CLOSED
    rng = random.Random(left_x ^ (world.seed * 0x7C3D2E1) ^ 0xF5A4B8)
    variant = rng.randint(0, 1)   # 0 = Aksumite  1 = Swahili Coast

    W_GARD   = 8
    W_GATE   = 10;  H_GATE   = 7
    W_COURT  = 12;  H_COURT  = 7
    W_THRONE = 22;  H_THRONE = 8
    total_w = W_GARD + W_GATE + W_COURT + W_THRONE + W_COURT + W_GATE + W_GARD
    _palace_clear_terrain(world, left_x, sy, total_w, H_THRONE + 12)

    def _stone_room(lx, w, h):
        _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, GRANITE_ASHLAR)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy, SANDSTONE_BLOCK)
        for by in range(sy - h, sy):
            _castle_set(world, lx,      by, GRANITE_ASHLAR)
            _castle_set(world, lx + w,  by, GRANITE_ASHLAR)
        _castle_door(world, lx, sy, door_block=_DOOR)
        _castle_door(world, lx + w - 2, sy, door_block=_DOOR)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy - h, GRANITE_ASHLAR)
            if (bx - lx) % 2 == 0:
                _castle_set(world, bx, sy - h - 1, SANDSTONE_BLOCK)

    x = left_x

    # ── guards ───────────────────────────────────────────────────────────────
    _palace_npc_at(world, left_x + 1,           sy, GuardNPC, biodome="savanna")
    _palace_npc_at(world, left_x + total_w - 2, sy, GuardNPC, biodome="savanna")

    # ── entry forecourt (left) ───────────────────────────────────────────────
    for bx in range(x, x + W_GARD):
        _castle_set(world, bx, sy, SANDSTONE_BLOCK)
    _castle_bg(world, x + 1,           sy - 1, MARIGOLD_BED)
    _castle_bg(world, x + 3,           sy - 1, VICTORY_STELE)
    _castle_bg(world, x + 5,           sy - 1, SUNFLOWER_BED)
    _castle_bg(world, x + W_GARD // 2, sy - 1, rng.choice(_FOUNTAIN_BLOCKS))
    x += W_GARD

    # ── left gate tower ──────────────────────────────────────────────────────
    _stone_room(x, W_GATE, H_GATE)
    for step in range(1, 5):
        span = max(0, 2 - step // 2)
        peak_y = sy - H_GATE - step
        if 0 <= peak_y < world.height:
            for bx in range(x + W_GATE // 2 - span, x + W_GATE // 2 + span + 1):
                _castle_set(world, bx, peak_y, SANDSTONE_BLOCK)
    _castle_bg(world, x + W_GATE // 2, sy - H_GATE + 3, CHANDELIER)
    if variant == 0:
        _castle_bg(world, x + W_GATE // 2, sy - 1, HERMES_STELE)
        _palace_npc_at(world, x + W_GATE // 2, sy, TradeNPC, rng)
    else:
        _castle_bg(world, x + W_GATE // 2, sy - 1, STONE_BASIN)
        _palace_npc_at(world, x + W_GATE // 2, sy, MerchantNPC, rng)
    x += W_GATE

    # ── left inner court ─────────────────────────────────────────────────────
    _stone_room(x, W_COURT, H_COURT)
    _castle_bg(world, x + W_COURT // 2, sy - H_COURT + 3, CHANDELIER)
    _castle_bg(world, x + 2,            sy - 1, MARIGOLD_BED)
    _castle_bg(world, x + W_COURT - 2,  sy - 1, MARIGOLD_BED)
    _castle_bg(world, x + W_COURT // 2, sy - 1, rng.choice(_FOUNTAIN_BLOCKS))
    if variant == 0:
        _palace_npc_at(world, x + W_COURT // 2, sy, GemQuestNPC, rng, 1, "savanna")
    else:
        _palace_npc_at(world, x + W_COURT // 2, sy, WildflowerQuestNPC, rng, 1, "savanna")
    x += W_COURT

    # ── granite throne hall ──────────────────────────────────────────────────
    cx = x + W_THRONE // 2
    _castle_fill_bg(world, x, x + W_THRONE, sy - H_THRONE, sy - 1, GRANITE_ASHLAR)
    for bx in range(x, x + W_THRONE + 1):
        _castle_set(world, bx, sy, SANDSTONE_BLOCK)
    for by in range(sy - H_THRONE, sy):
        _castle_set(world, x,             by, GRANITE_ASHLAR)
        _castle_set(world, x + W_THRONE,  by, GRANITE_ASHLAR)
    _castle_door(world, x, sy, door_block=_DOOR)
    _castle_door(world, x + W_THRONE - 2, sy, door_block=_DOOR)
    for col_x in (x + 4, x + W_THRONE - 4):
        for by in range(sy - H_THRONE + 3, sy):
            _castle_bg(world, col_x, by, GRANITE_ASHLAR)
        _castle_bg(world, col_x, sy - H_THRONE + 2, STAR_LAMP)
    for step in range(1, 5):
        step_y = sy - H_THRONE - step
        if not (0 <= step_y < world.height):
            break
        for bx in range(x + step * 2, x + W_THRONE + 1 - step * 2):
            _castle_set(world, bx, step_y, SANDSTONE_BLOCK)
    for bx in range(x, x + W_THRONE + 1):
        _castle_set(world, bx, sy - H_THRONE, GRANITE_ASHLAR)
    _castle_bg(world, cx,     sy - 1, CARVED_BENCH)
    _castle_bg(world, cx - 4, sy - 1, VICTORY_STELE)
    _castle_bg(world, cx + 4, sy - 1, VICTORY_STELE)
    _castle_bg(world, cx - 6, sy - 1, BRAZIER)
    _castle_bg(world, cx + 6, sy - 1, BRAZIER)
    _castle_bg(world, cx,     sy - H_THRONE + 4, CHANDELIER)
    x += W_THRONE

    # ── right inner court ────────────────────────────────────────────────────
    _stone_room(x, W_COURT, H_COURT)
    _castle_bg(world, x + W_COURT // 2, sy - H_COURT + 3, CHANDELIER)
    _castle_bg(world, x + 2,            sy - 1, SUNFLOWER_BED)
    _castle_bg(world, x + W_COURT - 2,  sy - 1, SUNFLOWER_BED)
    _castle_bg(world, x + W_COURT // 2, sy - 1, rng.choice(_FOUNTAIN_BLOCKS))
    if variant == 0:
        _palace_npc_at(world, x + W_COURT // 2, sy, ShrineKeeperNPC, rng,
                       biodome="savanna")
    else:
        _palace_npc_at(world, x + W_COURT // 2, sy, GemQuestNPC, rng, 1, "savanna")
    x += W_COURT

    # ── right gate tower ─────────────────────────────────────────────────────
    _stone_room(x, W_GATE, H_GATE)
    for step in range(1, 5):
        span = max(0, 2 - step // 2)
        peak_y = sy - H_GATE - step
        if 0 <= peak_y < world.height:
            for bx in range(x + W_GATE // 2 - span, x + W_GATE // 2 + span + 1):
                _castle_set(world, bx, peak_y, SANDSTONE_BLOCK)
    _castle_bg(world, x + W_GATE // 2, sy - H_GATE + 3, CHANDELIER)
    if variant == 0:
        _castle_bg(world, x + W_GATE // 2, sy - 1, STONE_BASIN)
        _palace_npc_at(world, x + W_GATE // 2, sy, JewelryMerchantNPC, rng)
    else:
        _castle_bg(world, x + W_GATE // 2, sy - 1, HERMES_STELE)
        _palace_npc_at(world, x + W_GATE // 2, sy, TradeNPC, rng)
    x += W_GATE

    # ── exit forecourt (right) ───────────────────────────────────────────────
    for bx in range(x, x + W_GARD):
        _castle_set(world, bx, sy, SANDSTONE_BLOCK)
    _castle_bg(world, x + 1,           sy - 1, SUNFLOWER_BED)
    _castle_bg(world, x + 3,           sy - 1, VICTORY_STELE)
    _castle_bg(world, x + 5,           sy - 1, MARIGOLD_BED)
    _castle_bg(world, x + W_GARD // 2, sy - 1, rng.choice(_FOUNTAIN_BLOCKS))


def _place_mesoamerican_palace(world, left_x: int, sy: int):
    """Mesoamerican palace — Aztec / Maya stepped temple pyramid, offering courts,
    colonnaded halls.  Staff: trade envoy, gem quest, wildflower quest, shrine keeper.
    """
    _DOOR = STONE_SLAB_DOOR_CLOSED
    rng = random.Random(left_x ^ (world.seed * 0x6B2F4E7) ^ 0xD4C3B2)
    variant = rng.randint(0, 1)   # 0 = Aztec  1 = Maya

    W_PLAZA  = 8
    W_GATE   = 10;  H_GATE   = 7
    W_COURT  = 14;  H_COURT  = 7
    W_PYRAM  = 20;  H_PYRAM  = 8
    total_w = W_PLAZA + W_GATE + W_COURT + W_PYRAM + W_COURT + W_GATE + W_PLAZA
    _palace_clear_terrain(world, left_x, sy, total_w, H_PYRAM + 14)

    def _temple_room(lx, w, h):
        _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, SANDSTONE_BLOCK)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy, LIMESTONE_BLOCK)
        for by in range(sy - h, sy):
            _castle_set(world, lx,      by, SANDSTONE_BLOCK)
            _castle_set(world, lx + w,  by, SANDSTONE_BLOCK)
        _castle_door(world, lx, sy, door_block=_DOOR)
        _castle_door(world, lx + w - 2, sy, door_block=_DOOR)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy - h,     SANDSTONE_BLOCK)
            _castle_set(world, bx, sy - h - 1, TERRACOTTA_ROOF_TILE)

    x = left_x

    # ── guards ───────────────────────────────────────────────────────────────
    _palace_npc_at(world, left_x + 1,           sy, GuardNPC, biodome="jungle")
    _palace_npc_at(world, left_x + total_w - 2, sy, GuardNPC, biodome="jungle")

    # ── entry plaza (left) ───────────────────────────────────────────────────
    for bx in range(x, x + W_PLAZA):
        _castle_set(world, bx, sy, LIMESTONE_BLOCK)
    _castle_bg(world, x + 1,            sy - 1, MARIGOLD_BED)
    _castle_bg(world, x + 3,            sy - 1, SUNFLOWER_BED)
    _castle_bg(world, x + W_PLAZA // 2, sy - 1, BRAZIER)
    x += W_PLAZA

    # ── left gate temple ─────────────────────────────────────────────────────
    _temple_room(x, W_GATE, H_GATE)
    _castle_bg(world, x + W_GATE // 2, sy - H_GATE + 3, CHANDELIER)
    _castle_bg(world, x + 2,           sy - 1, BRAZIER)
    _castle_bg(world, x + W_GATE - 2,  sy - 1, BRAZIER)
    if variant == 0:
        _castle_bg(world, x + W_GATE // 2, sy - 1, STONE_BASIN)
        _palace_npc_at(world, x + W_GATE // 2, sy, TradeNPC, rng)
    else:
        _castle_bg(world, x + W_GATE // 2, sy - 1, CARVED_BENCH)
        _palace_npc_at(world, x + W_GATE // 2, sy, MerchantNPC, rng)
    x += W_GATE

    # ── left offering court ───────────────────────────────────────────────────
    _temple_room(x, W_COURT, H_COURT)
    _castle_bg(world, x + W_COURT // 2, sy - H_COURT + 3, STAR_LAMP)
    _castle_bg(world, x + 2,            sy - 1, MARIGOLD_BED)
    _castle_bg(world, x + W_COURT - 2,  sy - 1, MARIGOLD_BED)
    _castle_bg(world, x + W_COURT // 2, sy - 1, rng.choice(_FOUNTAIN_BLOCKS))
    if variant == 0:
        _palace_npc_at(world, x + W_COURT // 2, sy, GemQuestNPC, rng, 1, "jungle")
    else:
        _palace_npc_at(world, x + W_COURT // 2, sy, WildflowerQuestNPC, rng, 1,
                       "jungle")
    x += W_COURT

    # ── central stepped pyramid throne complex ────────────────────────────────
    cx = x + W_PYRAM // 2
    _castle_fill_bg(world, x, x + W_PYRAM, sy - H_PYRAM, sy - 1, SANDSTONE_BLOCK)
    for bx in range(x, x + W_PYRAM + 1):
        _castle_set(world, bx, sy, LIMESTONE_BLOCK)
    for by in range(sy - H_PYRAM, sy):
        _castle_set(world, x,            by, SANDSTONE_BLOCK)
        _castle_set(world, x + W_PYRAM,  by, SANDSTONE_BLOCK)
    _castle_door(world, x, sy, door_block=_DOOR)
    _castle_door(world, x + W_PYRAM - 2, sy, door_block=_DOOR)
    for col_x in (x + 4, x + W_PYRAM - 4):
        for by in range(sy - H_PYRAM + 3, sy):
            _castle_bg(world, col_x, by, SANDSTONE_BLOCK)
        _castle_bg(world, col_x, sy - H_PYRAM + 2, BRAZIER)
    for tier in range(1, 6):
        tier_y = sy - H_PYRAM - 1 - (tier - 1) * 2
        if not (0 <= tier_y < world.height):
            break
        for bx in range(x + tier * 2, x + W_PYRAM + 1 - tier * 2):
            _castle_set(world, bx, tier_y, SANDSTONE_BLOCK)
        tier_top = tier_y - 1
        if 0 <= tier_top < world.height:
            for bx in range(x + tier * 2, x + W_PYRAM + 1 - tier * 2):
                _castle_set(world, bx, tier_top, TERRACOTTA_ROOF_TILE)
    for bx in range(x, x + W_PYRAM + 1):
        _castle_set(world, bx, sy - H_PYRAM, SANDSTONE_BLOCK)
    _castle_bg(world, cx,     sy - 1, CARVED_BENCH)
    _castle_bg(world, cx - 4, sy - 1, BRAZIER)
    _castle_bg(world, cx + 4, sy - 1, BRAZIER)
    _castle_bg(world, cx - 6, sy - 1, MARIGOLD_BED)
    _castle_bg(world, cx + 6, sy - 1, MARIGOLD_BED)
    _castle_bg(world, cx,     sy - H_PYRAM + 4, CHANDELIER)
    x += W_PYRAM

    # ── right offering court ──────────────────────────────────────────────────
    _temple_room(x, W_COURT, H_COURT)
    _castle_bg(world, x + W_COURT // 2, sy - H_COURT + 3, STAR_LAMP)
    _castle_bg(world, x + 2,            sy - 1, SUNFLOWER_BED)
    _castle_bg(world, x + W_COURT - 2,  sy - 1, SUNFLOWER_BED)
    _castle_bg(world, x + W_COURT // 2, sy - 1, rng.choice(_FOUNTAIN_BLOCKS))
    if variant == 0:
        _palace_npc_at(world, x + W_COURT // 2, sy, ShrineKeeperNPC, rng,
                       biodome="jungle")
    else:
        _palace_npc_at(world, x + W_COURT // 2, sy, GemQuestNPC, rng, 1, "jungle")
    x += W_COURT

    # ── right gate temple ─────────────────────────────────────────────────────
    _temple_room(x, W_GATE, H_GATE)
    _castle_bg(world, x + W_GATE // 2, sy - H_GATE + 3, CHANDELIER)
    _castle_bg(world, x + 2,           sy - 1, BRAZIER)
    _castle_bg(world, x + W_GATE - 2,  sy - 1, BRAZIER)
    if variant == 0:
        _castle_bg(world, x + W_GATE // 2, sy - 1, CARVED_BENCH)
        _palace_npc_at(world, x + W_GATE // 2, sy, JewelryMerchantNPC, rng)
    else:
        _castle_bg(world, x + W_GATE // 2, sy - 1, STONE_BASIN)
        _palace_npc_at(world, x + W_GATE // 2, sy, TradeNPC, rng)
    x += W_GATE

    # ── exit plaza (right) ───────────────────────────────────────────────────
    for bx in range(x, x + W_PLAZA):
        _castle_set(world, bx, sy, LIMESTONE_BLOCK)
    _castle_bg(world, x + 1,            sy - 1, SUNFLOWER_BED)
    _castle_bg(world, x + 3,            sy - 1, MARIGOLD_BED)
    _castle_bg(world, x + W_PLAZA // 2, sy - 1, BRAZIER)


def _place_french_baroque_palace(world, left_x: int, sy: int):
    """French baroque palace — Versailles-inspired formal gardens, mirrored wings,
    grand salon, gilded throne chamber.  Staff: florist, jeweler, chef, curator.
    """
    _DOOR = GILDED_DOOR_CLOSED
    rng = random.Random(left_x ^ (world.seed * 0x2A5D7F3) ^ 0xE8C6B4)
    variant = rng.randint(0, 1)   # 0 = Versailles  1 = Fontainebleau

    W_GARD   = 10
    W_WING   = 14;  H_WING   = 7
    W_SALON  = 12;  H_SALON  = 7
    W_THRONE = 22;  H_THRONE = 9
    total_w = W_GARD + W_WING + W_SALON + W_THRONE + W_SALON + W_WING + W_GARD
    _palace_clear_terrain(world, left_x, sy, total_w, H_THRONE + 14)

    def _baroque_room(lx, w, h):
        _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, LIMESTONE_BLOCK)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy, PALACE_FLOOR_TILE)
        for by in range(sy - h, sy):
            _castle_set(world, lx,      by, LIMESTONE_BLOCK)
            _castle_set(world, lx + w,  by, LIMESTONE_BLOCK)
        _castle_door(world, lx, sy, door_block=_DOOR)
        _castle_door(world, lx + w - 2, sy, door_block=_DOOR)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy - h,     POLISHED_MARBLE)
            _castle_set(world, bx, sy - h - 1, POLISHED_MARBLE)
        for bx in range(lx + 2, lx + w - 1, 3):
            for by in range(sy - h + 2, sy - 2):
                _castle_bg(world, bx, by, PALACE_PORTAL)

    x = left_x

    # ── guards ───────────────────────────────────────────────────────────────
    _palace_npc_at(world, left_x + 1,           sy, GuardNPC, biodome="mediterranean")
    _palace_npc_at(world, left_x + total_w - 2, sy, GuardNPC, biodome="mediterranean")

    # ── formal garden (left) ─────────────────────────────────────────────────
    for bx in range(x, x + W_GARD):
        _castle_set(world, bx, sy, PALACE_FLOOR_TILE)
    _castle_bg(world, x + 1,           sy - 1, TOPIARY_PEACOCK)
    _castle_bg(world, x + 2,           sy - 1, KNOT_GARDEN)
    _castle_bg(world, x + 4,           sy - 1, TOPIARY_SWAN)
    _castle_bg(world, x + 5,           sy - 1, ROSE_BED)
    _castle_bg(world, x + 7,           sy - 1, BOXWOOD_BALL)
    _castle_bg(world, x + W_GARD // 2, sy - 1,
               rng.choice((CHERUB_FOUNTAIN, MOSAIC_FOUNTAIN, SHELL_FOUNTAIN)))
    x += W_GARD

    # ── left gallery wing ────────────────────────────────────────────────────
    _baroque_room(x, W_WING, H_WING)
    _castle_bg(world, x + W_WING // 2, sy - H_WING + 3, CHANDELIER)
    _castle_bg(world, x + 2,           sy - 1, MARBLE_STATUE)
    _castle_bg(world, x + W_WING - 2,  sy - 1, MARBLE_PLINTH)
    if variant == 0:
        _castle_bg(world, x + W_WING // 2, sy - 1, LAVENDER_BED)
        _palace_npc_at(world, x + W_WING // 2, sy, RoyalFloristNPC, rng)
    else:
        _castle_bg(world, x + W_WING // 2, sy - 1, GARDEN_TABLE)
        _palace_npc_at(world, x + W_WING // 2, sy, RoyalCuratorNPC, rng)
    x += W_WING

    # ── left salon ───────────────────────────────────────────────────────────
    _baroque_room(x, W_SALON, H_SALON)
    _castle_bg(world, x + W_SALON // 2, sy - H_SALON + 3, CHANDELIER)
    _castle_bg(world, x + 2,            sy - 1, WISTERIA_PILLAR)
    _castle_bg(world, x + W_SALON - 2,  sy - 1, WISTERIA_PILLAR)
    _castle_bg(world, x + W_SALON // 2, sy - 1, MARBLE_BIRDBATH)
    if variant == 0:
        _palace_npc_at(world, x + W_SALON // 2, sy, RoyalJewelerNPC, rng)
    else:
        _palace_npc_at(world, x + W_SALON // 2, sy, JewelryMerchantNPC, rng)
    x += W_SALON

    # ── grand throne chamber ─────────────────────────────────────────────────
    cx = x + W_THRONE // 2
    _castle_fill_bg(world, x, x + W_THRONE, sy - H_THRONE, sy - 1, LIMESTONE_BLOCK)
    for bx in range(x, x + W_THRONE + 1):
        _castle_set(world, bx, sy, PALACE_FLOOR_TILE)
    for by in range(sy - H_THRONE, sy):
        _castle_set(world, x,             by, LIMESTONE_BLOCK)
        _castle_set(world, x + W_THRONE,  by, LIMESTONE_BLOCK)
    _castle_door(world, x, sy, door_block=_DOOR)
    _castle_door(world, x + W_THRONE - 2, sy, door_block=_DOOR)
    for bx in range(x + 2, x + W_THRONE - 1, 3):
        for by in range(sy - H_THRONE + 2, sy - 2):
            _castle_bg(world, bx, by, PALACE_PORTAL)
    for col_x in (x + 4, x + W_THRONE - 4):
        for by in range(sy - H_THRONE + 3, sy):
            _castle_bg(world, col_x, by, LIMESTONE_BLOCK)
        _castle_bg(world, col_x, sy - H_THRONE + 2, MARBLE_PLINTH)
    for gx in range(cx - 3, cx + 4):
        _castle_bg(world, gx, sy - H_THRONE + 4, GOLDEN_CEILING)
    for bx in range(x, x + W_THRONE + 1):
        _castle_set(world, bx, sy - H_THRONE,     POLISHED_MARBLE)
        _castle_set(world, bx, sy - H_THRONE - 1, POLISHED_MARBLE)
    _castle_bg(world, cx,     sy - 1, CARVED_BENCH)
    _castle_bg(world, cx - 4, sy - 1, CANDELABRA)
    _castle_bg(world, cx + 4, sy - 1, CANDELABRA)
    _castle_bg(world, cx - 6, sy - 1, MARBLE_STATUE)
    _castle_bg(world, cx + 6, sy - 1, MARBLE_STATUE)
    _castle_bg(world, cx,     sy - H_THRONE + 4, CHANDELIER)
    _castle_bg(world, cx - 5, sy - H_THRONE + 6, CHANDELIER)
    _castle_bg(world, cx + 5, sy - H_THRONE + 6, CHANDELIER)
    x += W_THRONE

    # ── right salon ──────────────────────────────────────────────────────────
    _baroque_room(x, W_SALON, H_SALON)
    _castle_bg(world, x + W_SALON // 2, sy - H_SALON + 3, CHANDELIER)
    _castle_bg(world, x + 2,            sy - 1, WISTERIA_PILLAR)
    _castle_bg(world, x + W_SALON - 2,  sy - 1, WISTERIA_PILLAR)
    _castle_bg(world, x + W_SALON // 2, sy - 1, MARBLE_BIRDBATH)
    if variant == 0:
        _palace_npc_at(world, x + W_SALON // 2, sy, RestaurantNPC, rng,
                       "mediterranean")
    else:
        _palace_npc_at(world, x + W_SALON // 2, sy, TradeNPC, rng)
    x += W_SALON

    # ── right gallery wing ───────────────────────────────────────────────────
    _baroque_room(x, W_WING, H_WING)
    _castle_bg(world, x + W_WING // 2, sy - H_WING + 3, CHANDELIER)
    _castle_bg(world, x + 2,           sy - 1, MARBLE_PLINTH)
    _castle_bg(world, x + W_WING - 2,  sy - 1, MARBLE_STATUE)
    if variant == 0:
        _castle_bg(world, x + W_WING // 2, sy - 1, ROSE_BED)
        _palace_npc_at(world, x + W_WING // 2, sy, MerchantNPC, rng)
    else:
        _castle_bg(world, x + W_WING // 2, sy - 1, LAVENDER_BED)
        _palace_npc_at(world, x + W_WING // 2, sy, RoyalFloristNPC, rng)
    x += W_WING

    # ── formal garden (right) ────────────────────────────────────────────────
    for bx in range(x, x + W_GARD):
        _castle_set(world, bx, sy, PALACE_FLOOR_TILE)
    _castle_bg(world, x + 1,           sy - 1, BOXWOOD_BALL)
    _castle_bg(world, x + 2,           sy - 1, ROSE_BED)
    _castle_bg(world, x + 4,           sy - 1, TOPIARY_SWAN)
    _castle_bg(world, x + 5,           sy - 1, KNOT_GARDEN)
    _castle_bg(world, x + 7,           sy - 1, TOPIARY_PEACOCK)
    _castle_bg(world, x + W_GARD // 2, sy - 1,
               rng.choice((CHERUB_FOUNTAIN, MOSAIC_FOUNTAIN, SHELL_FOUNTAIN)))


def _place_incan_palace(world, left_x: int, sy: int):
    """Incan palace — Andean precision-cut ashlar stonework, terraced approach,
    solar throne hall.  Staff: gem quest, shrine keeper, trade envoy, jeweler.
    """
    _DOOR = STONE_SLAB_DOOR_CLOSED
    rng = random.Random(left_x ^ (world.seed * 0x4E9F1A7) ^ 0xB3C7D5)
    variant = rng.randint(0, 1)   # 0 = Cusco imperial  1 = highland fortress

    W_TERR   = 8
    W_GATE   = 10;  H_GATE   = 7
    W_HALL   = 12;  H_HALL   = 7
    W_THRONE = 20;  H_THRONE = 8
    total_w = W_TERR + W_GATE + W_HALL + W_THRONE + W_HALL + W_GATE + W_TERR
    _palace_clear_terrain(world, left_x, sy, total_w, H_THRONE + 12)

    def _inca_room(lx, w, h):
        _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, ROUGH_STONE_WALL)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy, GRANITE_ASHLAR)
        for by in range(sy - h, sy):
            _castle_set(world, lx,      by, GRANITE_ASHLAR)
            _castle_set(world, lx + w,  by, GRANITE_ASHLAR)
        _castle_door(world, lx, sy, door_block=_DOOR)
        _castle_door(world, lx + w - 2, sy, door_block=_DOOR)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy - h, GRANITE_ASHLAR)

    x = left_x

    # ── guards ───────────────────────────────────────────────────────────────
    _palace_npc_at(world, left_x + 1,           sy, GuardNPC, biodome="mountain")
    _palace_npc_at(world, left_x + total_w - 2, sy, GuardNPC, biodome="mountain")

    # ── left terrace approach ────────────────────────────────────────────────
    for bx in range(x, x + W_TERR):
        _castle_set(world, bx, sy, GRANITE_ASHLAR)
    for bx in range(x + 1, x + W_TERR - 1):
        _castle_set(world, bx, sy - 1, ROUGH_STONE_WALL)
    for bx in range(x + 3, x + W_TERR - 3):
        _castle_set(world, bx, sy - 2, ROUGH_STONE_WALL)
    _castle_bg(world, x + 2,           sy - 3, SUNFLOWER_BED)
    _castle_bg(world, x + W_TERR - 2,  sy - 3, MARIGOLD_BED)
    _castle_bg(world, x + W_TERR // 2, sy - 1, BRAZIER)
    x += W_TERR

    # ── left gateway ─────────────────────────────────────────────────────────
    _inca_room(x, W_GATE, H_GATE)
    _castle_bg(world, x + W_GATE // 2, sy - H_GATE + 3, STAR_LAMP)
    _castle_bg(world, x + 2,           sy - 1, STONE_BASIN)
    _castle_bg(world, x + W_GATE - 2,  sy - 1, STONE_BASIN)
    if variant == 0:
        _castle_bg(world, x + W_GATE // 2, sy - 1, BRAZIER)
        _palace_npc_at(world, x + W_GATE // 2, sy, GemQuestNPC, rng, 1, "mountain")
    else:
        _castle_bg(world, x + W_GATE // 2, sy - 1, GARDEN_OBELISK)
        _palace_npc_at(world, x + W_GATE // 2, sy, ShrineKeeperNPC, rng,
                       biodome="mountain")
    x += W_GATE

    # ── left hall ────────────────────────────────────────────────────────────
    _inca_room(x, W_HALL, H_HALL)
    _castle_bg(world, x + W_HALL // 2, sy - H_HALL + 3, STAR_LAMP)
    _castle_bg(world, x + 2,           sy - 1, MARIGOLD_BED)
    _castle_bg(world, x + W_HALL - 2,  sy - 1, SUNFLOWER_BED)
    _castle_bg(world, x + W_HALL // 2, sy - 1, rng.choice(_FOUNTAIN_BLOCKS))
    if variant == 0:
        _palace_npc_at(world, x + W_HALL // 2, sy, TradeNPC, rng)
    else:
        _palace_npc_at(world, x + W_HALL // 2, sy, MerchantNPC, rng)
    x += W_HALL

    # ── solar throne hall ─────────────────────────────────────────────────────
    cx = x + W_THRONE // 2
    _castle_fill_bg(world, x, x + W_THRONE, sy - H_THRONE, sy - 1, ROUGH_STONE_WALL)
    for bx in range(x, x + W_THRONE + 1):
        _castle_set(world, bx, sy, GRANITE_ASHLAR)
    for by in range(sy - H_THRONE, sy):
        _castle_set(world, x,             by, GRANITE_ASHLAR)
        _castle_set(world, x + W_THRONE,  by, GRANITE_ASHLAR)
    _castle_door(world, x, sy, door_block=_DOOR)
    _castle_door(world, x + W_THRONE - 2, sy, door_block=_DOOR)
    for col_x in (x + 4, x + W_THRONE - 4):
        for by in range(sy - H_THRONE + 3, sy):
            _castle_bg(world, col_x, by, GRANITE_ASHLAR)
        _castle_bg(world, col_x, sy - H_THRONE + 2, STAR_LAMP)
    for bx in range(x, x + W_THRONE + 1):
        _castle_set(world, bx, sy - H_THRONE, GRANITE_ASHLAR)
    for step in range(1, 4):
        step_y = sy - H_THRONE - step
        if not (0 <= step_y < world.height):
            break
        for bx in range(x + step * 2, x + W_THRONE + 1 - step * 2):
            _castle_set(world, bx, step_y, ROUGH_STONE_WALL)
    for niche_x in range(x + 2, x + W_THRONE - 1, 4):
        _castle_bg(world, niche_x, sy - H_THRONE + 4, BRAZIER)
    _castle_bg(world, cx,     sy - 1, CARVED_BENCH)
    _castle_bg(world, cx - 4, sy - 1, BRAZIER)
    _castle_bg(world, cx + 4, sy - 1, BRAZIER)
    _castle_bg(world, cx - 6, sy - 1, STONE_BASIN)
    _castle_bg(world, cx + 6, sy - 1, STONE_BASIN)
    _castle_bg(world, cx,     sy - H_THRONE + 4, CHANDELIER)
    x += W_THRONE

    # ── right hall ────────────────────────────────────────────────────────────
    _inca_room(x, W_HALL, H_HALL)
    _castle_bg(world, x + W_HALL // 2, sy - H_HALL + 3, STAR_LAMP)
    _castle_bg(world, x + 2,           sy - 1, SUNFLOWER_BED)
    _castle_bg(world, x + W_HALL - 2,  sy - 1, MARIGOLD_BED)
    _castle_bg(world, x + W_HALL // 2, sy - 1, rng.choice(_FOUNTAIN_BLOCKS))
    if variant == 0:
        _palace_npc_at(world, x + W_HALL // 2, sy, JewelryMerchantNPC, rng)
    else:
        _palace_npc_at(world, x + W_HALL // 2, sy, TradeNPC, rng)
    x += W_HALL

    # ── right gateway ─────────────────────────────────────────────────────────
    _inca_room(x, W_GATE, H_GATE)
    _castle_bg(world, x + W_GATE // 2, sy - H_GATE + 3, STAR_LAMP)
    _castle_bg(world, x + 2,           sy - 1, STONE_BASIN)
    _castle_bg(world, x + W_GATE - 2,  sy - 1, STONE_BASIN)
    if variant == 0:
        _castle_bg(world, x + W_GATE // 2, sy - 1, GARDEN_OBELISK)
        _palace_npc_at(world, x + W_GATE // 2, sy, ShrineKeeperNPC, rng,
                       biodome="mountain")
    else:
        _castle_bg(world, x + W_GATE // 2, sy - 1, BRAZIER)
        _palace_npc_at(world, x + W_GATE // 2, sy, GemQuestNPC, rng, 1, "mountain")
    x += W_GATE

    # ── right terrace approach ────────────────────────────────────────────────
    for bx in range(x, x + W_TERR):
        _castle_set(world, bx, sy, GRANITE_ASHLAR)
    for bx in range(x + 1, x + W_TERR - 1):
        _castle_set(world, bx, sy - 1, ROUGH_STONE_WALL)
    for bx in range(x + 3, x + W_TERR - 3):
        _castle_set(world, bx, sy - 2, ROUGH_STONE_WALL)
    _castle_bg(world, x + 2,           sy - 3, MARIGOLD_BED)
    _castle_bg(world, x + W_TERR - 2,  sy - 3, SUNFLOWER_BED)
    _castle_bg(world, x + W_TERR // 2, sy - 1, BRAZIER)


def _place_persian_palace(world, left_x: int, sy: int):
    """Achaemenid Persian palace — Persepolis-style lamassu gates, hypostyle apadana halls,
    columned audience chamber.  Staff: scholar, gem quest, trade envoy, jeweler.
    """
    rng = random.Random(left_x ^ (world.seed * 0x5B3E8A4) ^ 0xF7D2C6)
    variant = rng.randint(0, 1)   # 0 = Darius/Persepolis  1 = Susa/Achaemenid

    W_GARD   = 8
    W_PORT   = 10;  H_PORT   = 7
    W_APAD   = 14;  H_APAD   = 7
    W_THRONE = 22;  H_THRONE = 8
    total_w = W_GARD + W_PORT + W_APAD + W_THRONE + W_APAD + W_PORT + W_GARD
    _palace_clear_terrain(world, left_x, sy, total_w, H_THRONE + 14)

    def _persian_room(lx, w, h):
        _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, SANDSTONE_BLOCK)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy, POLISHED_MARBLE)
        for by in range(sy - h, sy):
            _castle_set(world, lx,      by, SANDSTONE_BLOCK)
            _castle_set(world, lx + w,  by, SANDSTONE_BLOCK)
        _castle_door(world, lx, sy)
        _castle_door(world, lx + w - 2, sy)
        for bx in range(lx + 2, lx + w, 3):
            _castle_bg(world, bx, sy - h + 2, MUGHAL_ARCH)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy - h,     POLISHED_MARBLE)
            _castle_set(world, bx, sy - h - 1, SANDSTONE_BLOCK)

    x = left_x

    # ── guards ───────────────────────────────────────────────────────────────
    _palace_npc_at(world, left_x + 1,           sy, GuardNPC, biodome="desert")
    _palace_npc_at(world, left_x + total_w - 2, sy, GuardNPC, biodome="desert")

    # ── approach garden (left) ───────────────────────────────────────────────
    for bx in range(x, x + W_GARD):
        _castle_set(world, bx, sy, POLISHED_MARBLE)
    _castle_bg(world, x + 1,           sy - 1, GARDEN_OBELISK)
    _castle_bg(world, x + 3,           sy - 1, ROSE_BED)
    _castle_bg(world, x + 5,           sy - 1, GARDEN_OBELISK)
    _castle_bg(world, x + W_GARD // 2, sy - 1, rng.choice(_FOUNTAIN_BLOCKS))
    x += W_GARD

    # ── left lamassu gate portal ─────────────────────────────────────────────
    _persian_room(x, W_PORT, H_PORT)
    for col_x in (x + 2, x + W_PORT - 2):
        for by in range(sy - H_PORT + 2, sy):
            _castle_bg(world, col_x, by, SANDSTONE_BLOCK)
        _castle_bg(world, col_x, sy - H_PORT + 1, MUGHAL_ARCH)
    _castle_bg(world, x + W_PORT // 2, sy - H_PORT + 3, CHANDELIER)
    if variant == 0:
        _castle_bg(world, x + W_PORT // 2, sy - 1, CARVED_BENCH)
        _palace_npc_at(world, x + W_PORT // 2, sy, ScholarNPC, rng)
    else:
        _castle_bg(world, x + W_PORT // 2, sy - 1, STONE_BASIN)
        _palace_npc_at(world, x + W_PORT // 2, sy, TradeNPC, rng)
    x += W_PORT

    # ── left apadana hypostyle hall ──────────────────────────────────────────
    _persian_room(x, W_APAD, H_APAD)
    for col_x in range(x + 3, x + W_APAD - 2, 3):
        for by in range(sy - H_APAD + 3, sy):
            _castle_bg(world, col_x, by, SANDSTONE_BLOCK)
        _castle_bg(world, col_x, sy - H_APAD + 2, STAR_LAMP)
    _castle_bg(world, x + W_APAD // 2, sy - H_APAD + 3, CHANDELIER)
    if variant == 0:
        _castle_bg(world, x + W_APAD // 2, sy - 1, TEXTILE_RUG_GOLDEN)
        _palace_npc_at(world, x + W_APAD // 2, sy, GemQuestNPC, rng, 1, "desert")
    else:
        _castle_bg(world, x + W_APAD // 2, sy - 1, STONE_BASIN)
        _palace_npc_at(world, x + W_APAD // 2, sy, WildflowerQuestNPC, rng, 1,
                       "desert")
    x += W_APAD

    # ── royal audience chamber ────────────────────────────────────────────────
    cx = x + W_THRONE // 2
    _castle_fill_bg(world, x, x + W_THRONE, sy - H_THRONE, sy - 1, SANDSTONE_BLOCK)
    for bx in range(x, x + W_THRONE + 1):
        _castle_set(world, bx, sy, POLISHED_MARBLE)
    for by in range(sy - H_THRONE, sy):
        _castle_set(world, x,             by, SANDSTONE_BLOCK)
        _castle_set(world, x + W_THRONE,  by, SANDSTONE_BLOCK)
    _castle_door(world, x, sy)
    _castle_door(world, x + W_THRONE - 2, sy)
    for col_x in range(x + 4, x + W_THRONE - 3, 4):
        for by in range(sy - H_THRONE + 3, sy):
            _castle_bg(world, col_x, by, SANDSTONE_BLOCK)
        _castle_bg(world, col_x, sy - H_THRONE + 2, MUGHAL_ARCH)
    for bx in range(x + 1, x + W_THRONE, 2):
        _castle_bg(world, bx, sy - H_THRONE + 2, MUGHAL_JALI)
    for bx in range(x, x + W_THRONE + 1):
        _castle_set(world, bx, sy - H_THRONE,     POLISHED_MARBLE)
        _castle_set(world, bx, sy - H_THRONE - 1, SANDSTONE_BLOCK)
    _castle_bg(world, cx,     sy - 1, CARVED_BENCH)
    _castle_bg(world, cx - 4, sy - 1, STAR_LAMP)
    _castle_bg(world, cx + 4, sy - 1, STAR_LAMP)
    _castle_bg(world, cx - 7, sy - 1, CANDELABRA)
    _castle_bg(world, cx + 7, sy - 1, CANDELABRA)
    _castle_bg(world, cx,     sy - H_THRONE + 4, CHANDELIER)
    _castle_bg(world, cx - 4, sy - H_THRONE + 6, CHANDELIER)
    _castle_bg(world, cx + 4, sy - H_THRONE + 6, CHANDELIER)
    x += W_THRONE

    # ── right apadana hypostyle hall ─────────────────────────────────────────
    _persian_room(x, W_APAD, H_APAD)
    for col_x in range(x + 3, x + W_APAD - 2, 3):
        for by in range(sy - H_APAD + 3, sy):
            _castle_bg(world, col_x, by, SANDSTONE_BLOCK)
        _castle_bg(world, col_x, sy - H_APAD + 2, STAR_LAMP)
    _castle_bg(world, x + W_APAD // 2, sy - H_APAD + 3, CHANDELIER)
    if variant == 0:
        _castle_bg(world, x + W_APAD // 2, sy - 1, STONE_BASIN)
        _palace_npc_at(world, x + W_APAD // 2, sy, JewelryMerchantNPC, rng)
    else:
        _castle_bg(world, x + W_APAD // 2, sy - 1, TEXTILE_RUG_GOLDEN)
        _palace_npc_at(world, x + W_APAD // 2, sy, GemQuestNPC, rng, 1, "desert")
    x += W_APAD

    # ── right lamassu gate portal ─────────────────────────────────────────────
    _persian_room(x, W_PORT, H_PORT)
    for col_x in (x + 2, x + W_PORT - 2):
        for by in range(sy - H_PORT + 2, sy):
            _castle_bg(world, col_x, by, SANDSTONE_BLOCK)
        _castle_bg(world, col_x, sy - H_PORT + 1, MUGHAL_ARCH)
    _castle_bg(world, x + W_PORT // 2, sy - H_PORT + 3, CHANDELIER)
    if variant == 0:
        _castle_bg(world, x + W_PORT // 2, sy - 1, STONE_BASIN)
        _palace_npc_at(world, x + W_PORT // 2, sy, MerchantNPC, rng)
    else:
        _castle_bg(world, x + W_PORT // 2, sy - 1, CARVED_BENCH)
        _palace_npc_at(world, x + W_PORT // 2, sy, ScholarNPC, rng)
    x += W_PORT

    # ── exit garden (right) ──────────────────────────────────────────────────
    for bx in range(x, x + W_GARD):
        _castle_set(world, bx, sy, POLISHED_MARBLE)
    _castle_bg(world, x + 1,           sy - 1, GARDEN_OBELISK)
    _castle_bg(world, x + 3,           sy - 1, ROSE_BED)
    _castle_bg(world, x + 5,           sy - 1, GARDEN_OBELISK)
    _castle_bg(world, x + W_GARD // 2, sy - 1, rng.choice(_FOUNTAIN_BLOCKS))


def _city_slot_metadata(slot_x: int) -> dict:
    """Return deterministic region identity for the city slot at slot_x.

    slot_x must be the true slot center (n * CITY_SPACING + CITY_SPACING // 2),
    not the jittered city_bx.
    """
    slot_index = slot_x // CITY_SPACING      # floor div handles negatives correctly
    region_id  = slot_index // 3
    is_capital = (slot_index % 3 == 1)       # Python % is non-negative, works for negatives
    return {"slot_index": slot_index, "region_id": region_id, "is_capital": is_capital}


def generate_cities(world, seed):
    rng = random.Random(seed + 77777)
    placed = 0
    x = -(CITY_COUNT // 2) * CITY_SPACING + CITY_SPACING // 2
    world.city_zones = []
    world.town_centers = []
    world.city_sizes = []
    world.city_slot_xs = []

    while placed < CITY_COUNT:
        slot_x = x
        jitter = rng.randint(-6, 6)
        city_bx = slot_x + jitter
        difficulty = min(placed // 2, 2)
        city_size = _build_single_city(world, rng, city_bx, difficulty)
        world.town_centers.append(city_bx)
        world.city_sizes.append(city_size)
        world.city_slot_xs.append(slot_x)
        placed += 1
        x += CITY_SPACING

    import npc_identity
    npc_identity.assign_ruling_dynasties(world, seed)


def generate_city_for_chunk(world, seed, cx):
    """Build a city in newly-generated chunk cx if a city slot falls there."""
    from constants import CHUNK_W
    base_x = cx * CHUNK_W
    half = CITY_SPACING // 2
    slot_x = None
    for bx in range(base_x, base_x + CHUNK_W):
        if ((bx % CITY_SPACING) + CITY_SPACING) % CITY_SPACING == half:
            slot_x = bx
            break
    if slot_x is None:
        return
    meta = _city_slot_metadata(slot_x)
    rng = random.Random(seed + slot_x * 9001 + 33333)
    jitter = rng.randint(-6, 6)
    city_bx = slot_x + jitter
    if any(lo - 10 <= city_bx <= hi + 10 for lo, hi in world.city_zones):
        return
    city_size = _build_single_city(world, rng, city_bx, 2)
    world.town_centers.append(city_bx)
    world.city_sizes.append(city_size)
    world.city_slot_xs.append(slot_x)
    from towns import register_new_town
    import npc_identity
    register_new_town(world, city_bx, city_size,
                      region_id=meta["region_id"],
                      is_capital=meta["is_capital"])
    npc_identity.assign_ruling_dynasties(world, seed)
