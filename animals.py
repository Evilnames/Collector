import random
import uuid
import pygame
from constants import BLOCK_SIZE, GRAVITY, JUMP_FORCE, MAX_FALL, PLAYER_W, PLAYER_H, MINE_REACH, HOTBAR_SIZE
from blocks import LADDER, WOOD_FENCE, IRON_FENCE, WATER, GRASS, DIRT, FEED_TROUGH_BLOCK, SALT_LICK_BLOCK

ANIMAL_MOVE_SPEED = 1.2
ANIMAL_CLIMB_SPEED = 1.5

MUTATION_TYPES = ["albino", "giant", "miniature", "golden"]

# Dominance order — index 0 = dominant, higher index = more recessive
COAT_PATTERN_ORDER  = ["solid", "dappled", "spotted", "blanket"]
LEG_MARKING_ORDER   = ["none", "socks", "stockings"]
WOOL_COLOR_ORDER    = ["white", "grey", "brown", "black"]
MANE_COLOR_ORDER    = ["match", "flaxen", "silver", "dark"]
FACE_MARKING_ORDER  = ["none", "star", "blaze", "stripe"]
HIDE_ORDER          = ["solid", "spotted", "belted", "piebald"]
GOAT_COLOR_ORDER    = ["tan", "white", "brown", "black"]
GOAT_PATTERN_ORDER  = ["solid", "chamoisee", "broken", "sundgau"]
GOAT_HORN_ORDER     = ["curved", "straight", "scurred", "polled"]
GOAT_EAR_ORDER      = ["upright", "drooping", "gopher"]
GOAT_BEARD_ORDER    = ["small", "full", "none"]
PLUMAGE_ORDER          = ["white", "yellow", "brown", "black"]
CHICKEN_PATTERN_ORDER  = ["solid", "barred", "laced", "speckled"]
CHICKEN_COMB_ORDER     = ["single", "rose", "pea", "walnut"]
CHICKEN_LEG_ORDER      = ["yellow", "white", "dark", "feathered"]

# lay_rate_gene:        divides into REFILL_TIME — higher = lays more often
# constitution_gene:    sets starting health (0.7–1.3)
# feather_density_gene: coat fluffiness — visual + display (0.0–1.0)
CHICKEN_BREED_PROFILES = {
    # ── High production ───────────────────────────────────────────────────
    "Leghorn": {
        "biomes": {"temperate", "rolling_hills", "savanna"},
        "genes": {"lay_rate_gene": (1.2, 1.5), "constitution_gene": (0.8, 1.1), "feather_density_gene": (0.0, 0.2)},
        "plumage_weights": [70, 5, 20, 5], "pattern_weights": [90, 5, 5, 0],
        "comb_weights": [85, 10, 5, 0], "leg_weights": [85, 10, 5, 0],
        "egg_tint": (245, 235, 200),
    },
    "Australorp": {
        "biomes": {"temperate", "rolling_hills"},
        "genes": {"lay_rate_gene": (1.1, 1.4), "constitution_gene": (0.9, 1.2), "feather_density_gene": (0.0, 0.2)},
        "plumage_weights": [0, 0, 5, 95], "pattern_weights": [90, 0, 10, 0],
        "comb_weights": [85, 10, 5, 0], "leg_weights": [15, 5, 75, 5],
        "egg_tint": (245, 235, 200),
    },
    # ── Dual-purpose ──────────────────────────────────────────────────────
    "Rhode Island Red": {
        "biomes": {"temperate", "rolling_hills"},
        "genes": {"lay_rate_gene": (1.0, 1.3), "constitution_gene": (0.9, 1.2), "feather_density_gene": (0.0, 0.2)},
        "plumage_weights": [5, 15, 70, 10], "pattern_weights": [88, 5, 7, 0],
        "comb_weights": [85, 10, 5, 0], "leg_weights": [80, 5, 15, 0],
        "egg_tint": (245, 228, 200),
    },
    "Plymouth Rock": {
        "biomes": {"temperate", "rolling_hills", "birch_forest"},
        "genes": {"lay_rate_gene": (0.9, 1.2), "constitution_gene": (0.9, 1.2), "feather_density_gene": (0.0, 0.2)},
        "plumage_weights": [10, 5, 50, 35], "pattern_weights": [5, 80, 10, 5],
        "comb_weights": [85, 10, 5, 0], "leg_weights": [85, 10, 5, 0],
        "egg_tint": (245, 230, 200),
    },
    "Sussex": {
        "biomes": {"temperate", "rolling_hills"},
        "genes": {"lay_rate_gene": (0.9, 1.2), "constitution_gene": (0.9, 1.2), "feather_density_gene": (0.1, 0.3)},
        "plumage_weights": [60, 10, 20, 10], "pattern_weights": [40, 10, 20, 30],
        "comb_weights": [85, 10, 5, 0], "leg_weights": [20, 70, 10, 0],
        "egg_tint": (245, 232, 205),
    },
    "Wyandotte": {
        "biomes": {"boreal", "temperate", "birch_forest"},
        "genes": {"lay_rate_gene": (0.9, 1.2), "constitution_gene": (1.0, 1.3), "feather_density_gene": (0.1, 0.3)},
        "plumage_weights": [20, 30, 30, 20], "pattern_weights": [20, 20, 55, 5],
        "comb_weights": [5, 85, 10, 0], "leg_weights": [75, 20, 5, 0],
        "egg_tint": (245, 230, 200),
    },
    "Orpington": {
        "biomes": {"temperate", "boreal"},
        "genes": {"lay_rate_gene": (0.9, 1.2), "constitution_gene": (0.9, 1.2), "feather_density_gene": (0.5, 0.8)},
        "plumage_weights": [20, 35, 35, 10], "pattern_weights": [90, 0, 10, 0],
        "comb_weights": [85, 10, 5, 0], "leg_weights": [20, 75, 5, 0],
        "egg_tint": (245, 232, 205),
    },
    # ── Cold-hardy ────────────────────────────────────────────────────────
    "Brahma": {
        "biomes": {"boreal", "tundra"},
        "genes": {"lay_rate_gene": (0.8, 1.1), "constitution_gene": (1.0, 1.3), "feather_density_gene": (0.4, 0.7)},
        "plumage_weights": [20, 20, 30, 30], "pattern_weights": [30, 20, 45, 5],
        "comb_weights": [5, 10, 80, 5], "leg_weights": [10, 10, 10, 70],
        "egg_tint": (245, 232, 205),
    },
    # ── Ornamental ────────────────────────────────────────────────────────
    "Silkie": {
        "biomes": {"temperate", "rolling_hills"},
        "genes": {"lay_rate_gene": (0.6, 0.9), "constitution_gene": (0.7, 1.0), "feather_density_gene": (0.8, 1.0)},
        "plumage_weights": [30, 30, 20, 20], "pattern_weights": [95, 0, 5, 0],
        "comb_weights": [5, 10, 10, 75], "leg_weights": [10, 10, 10, 70],
        "egg_tint": (245, 232, 210),
    },
    "Barbu d'Uccle": {
        "biomes": {"temperate", "rolling_hills"},
        "genes": {"lay_rate_gene": (0.7, 1.0), "constitution_gene": (0.7, 1.0), "feather_density_gene": (0.5, 0.8)},
        "plumage_weights": [25, 25, 30, 20], "pattern_weights": [40, 10, 20, 30],
        "comb_weights": [85, 10, 5, 0], "leg_weights": [10, 10, 10, 70],
        "egg_tint": (245, 232, 205),
    },
    # ── Tropical / gamefowl ───────────────────────────────────────────────
    "Malay": {
        "biomes": {"tropical", "savanna"},
        "genes": {"lay_rate_gene": (0.6, 0.9), "constitution_gene": (1.0, 1.3), "feather_density_gene": (0.0, 0.1)},
        "plumage_weights": [5, 15, 40, 40], "pattern_weights": [85, 0, 5, 10],
        "comb_weights": [5, 10, 10, 75], "leg_weights": [70, 10, 20, 0],
        "egg_tint": (245, 228, 198),
    },
    # ── Heritage / special ────────────────────────────────────────────────
    "Araucana": {
        "biomes": {"rolling_hills", "arid_steppe"},
        "genes": {"lay_rate_gene": (0.9, 1.2), "constitution_gene": (0.9, 1.2), "feather_density_gene": (0.2, 0.4)},
        "plumage_weights": [20, 20, 35, 25], "pattern_weights": [70, 10, 15, 5],
        "comb_weights": [5, 10, 80, 5], "leg_weights": [30, 20, 45, 5],
        "egg_tint": (195, 220, 205),   # blue-green eggs
    },
}

CHICKEN_BIOME_MAP: dict = {}
for _chk_breed, _chk_profile in CHICKEN_BREED_PROFILES.items():
    for _chk_biome in _chk_profile["biomes"]:
        CHICKEN_BIOME_MAP.setdefault(_chk_biome, []).append(_chk_breed)
BIRTH_ORDER              = ["single", "twin"]    # twin fully recessive

# milk_volume_gene:  bottles per milking — round() gives count (0.5–2.5)
# milk_richness_gene: quality stat (0.7–1.3)
# refill_rate_gene:  divides into REFILL_TIME — higher = refills faster
# constitution_gene: hardiness → starting health on spawn (0.7–1.3)
# fiber_gene:        fleece density for Angora/Cashmere — visual + future shearing (0.0–1.0)
GOAT_BREED_PROFILES = {
    # ── Dairy leaders ─────────────────────────────────────────────────────
    "Nubian": {
        "biomes": {"temperate", "savanna", "tropical"},
        "genes": {
            "milk_volume_gene":   (1.5, 2.2), "milk_richness_gene": (1.0, 1.3),
            "refill_rate_gene":   (1.0, 1.4), "constitution_gene":  (0.8, 1.1),
            "fiber_gene": (0.0, 0.1),
        },
        "coat_color_weights": [35, 20, 30, 15], "pattern_weights": [60, 10, 25, 5],
        "horn_weights": [70, 10, 10, 10], "ear_weights": [0, 100, 0], "beard_weights": [40, 30, 30],
    },
    "Saanen": {
        "biomes": {"temperate", "rolling_hills"},
        "genes": {
            "milk_volume_gene":   (2.0, 2.5), "milk_richness_gene": (0.9, 1.1),
            "refill_rate_gene":   (1.1, 1.5), "constitution_gene":  (0.9, 1.2),
            "fiber_gene": (0.0, 0.1),
        },
        "coat_color_weights": [5, 90, 4, 1], "pattern_weights": [90, 5, 5, 0],
        "horn_weights": [60, 15, 5, 20], "ear_weights": [90, 5, 5], "beard_weights": [50, 20, 30],
    },
    "Alpine": {
        "biomes": {"temperate", "rolling_hills", "alpine_mountain"},
        "genes": {
            "milk_volume_gene":   (1.5, 2.0), "milk_richness_gene": (0.9, 1.2),
            "refill_rate_gene":   (1.0, 1.3), "constitution_gene":  (0.9, 1.2),
            "fiber_gene": (0.0, 0.1),
        },
        "coat_color_weights": [20, 15, 40, 25], "pattern_weights": [30, 40, 25, 5],
        "horn_weights": [20, 60, 10, 10], "ear_weights": [90, 5, 5], "beard_weights": [50, 30, 20],
    },
    "Toggenburg": {
        "biomes": {"boreal", "alpine_mountain"},
        "genes": {
            "milk_volume_gene":   (1.5, 2.0), "milk_richness_gene": (0.9, 1.1),
            "refill_rate_gene":   (1.0, 1.3), "constitution_gene":  (1.0, 1.3),
            "fiber_gene": (0.0, 0.1),
        },
        "coat_color_weights": [15, 10, 65, 10], "pattern_weights": [20, 60, 10, 10],
        "horn_weights": [10, 70, 10, 10], "ear_weights": [90, 5, 5], "beard_weights": [60, 20, 20],
    },
    "Oberhasli": {
        "biomes": {"alpine_mountain", "boreal"},
        "genes": {
            "milk_volume_gene":   (1.3, 1.9), "milk_richness_gene": (1.0, 1.2),
            "refill_rate_gene":   (1.0, 1.3), "constitution_gene":  (0.9, 1.2),
            "fiber_gene": (0.0, 0.1),
        },
        "coat_color_weights": [20, 5, 65, 10], "pattern_weights": [10, 80, 5, 5],
        "horn_weights": [10, 70, 10, 10], "ear_weights": [90, 5, 5], "beard_weights": [50, 30, 20],
    },
    "Nigerian Dwarf": {
        "biomes": {"temperate", "rolling_hills"},
        "genes": {
            "milk_volume_gene":   (0.8, 1.3), "milk_richness_gene": (1.1, 1.3),
            "refill_rate_gene":   (1.0, 1.4), "constitution_gene":  (0.8, 1.1),
            "fiber_gene": (0.0, 0.1),
        },
        "coat_color_weights": [35, 25, 25, 15], "pattern_weights": [45, 20, 30, 5],
        "horn_weights": [60, 15, 10, 15], "ear_weights": [90, 5, 5], "beard_weights": [45, 25, 30],
    },
    "LaMancha": {
        "biomes": {"temperate", "rolling_hills"},
        "genes": {
            "milk_volume_gene":   (1.5, 2.0), "milk_richness_gene": (1.0, 1.2),
            "refill_rate_gene":   (1.0, 1.4), "constitution_gene":  (0.9, 1.2),
            "fiber_gene": (0.0, 0.1),
        },
        "coat_color_weights": [30, 20, 30, 20], "pattern_weights": [50, 15, 30, 5],
        "horn_weights": [50, 20, 10, 20], "ear_weights": [0, 0, 100], "beard_weights": [40, 30, 30],
    },
    # ── Meat breeds ───────────────────────────────────────────────────────
    "Boer": {
        "biomes": {"arid_steppe", "savanna", "desert"},
        "genes": {
            "milk_volume_gene":   (0.6, 1.0), "milk_richness_gene": (0.7, 0.9),
            "refill_rate_gene":   (0.8, 1.1), "constitution_gene":  (1.0, 1.3),
            "fiber_gene": (0.0, 0.1),
        },
        "coat_color_weights": [10, 60, 25, 5], "pattern_weights": [20, 0, 70, 10],
        "horn_weights": [70, 15, 10, 5], "ear_weights": [10, 85, 5], "beard_weights": [50, 20, 30],
    },
    "Kiko": {
        "biomes": {"savanna", "tropical", "arid_steppe"},
        "genes": {
            "milk_volume_gene":   (0.6, 1.0), "milk_richness_gene": (0.7, 0.9),
            "refill_rate_gene":   (0.9, 1.2), "constitution_gene":  (1.0, 1.3),
            "fiber_gene": (0.0, 0.1),
        },
        "coat_color_weights": [20, 50, 25, 5], "pattern_weights": [65, 10, 20, 5],
        "horn_weights": [60, 25, 10, 5], "ear_weights": [80, 15, 5], "beard_weights": [50, 20, 30],
    },
    "Myotonic": {
        "biomes": {"temperate", "rolling_hills"},
        "genes": {
            "milk_volume_gene":   (0.7, 1.2), "milk_richness_gene": (0.8, 1.0),
            "refill_rate_gene":   (0.8, 1.1), "constitution_gene":  (0.8, 1.1),
            "fiber_gene": (0.0, 0.15),
        },
        "coat_color_weights": [25, 25, 30, 20], "pattern_weights": [50, 10, 35, 5],
        "horn_weights": [50, 25, 15, 10], "ear_weights": [85, 10, 5], "beard_weights": [40, 25, 35],
    },
    # ── Fiber breeds ──────────────────────────────────────────────────────
    "Angora": {
        "biomes": {"temperate", "birch_forest", "rolling_hills"},
        "genes": {
            "milk_volume_gene":   (0.5, 0.9), "milk_richness_gene": (0.7, 1.0),
            "refill_rate_gene":   (0.8, 1.1), "constitution_gene":  (0.8, 1.1),
            "fiber_gene": (0.7, 1.0),
        },
        "coat_color_weights": [10, 80, 8, 2], "pattern_weights": [90, 5, 5, 0],
        "horn_weights": [15, 65, 10, 10], "ear_weights": [85, 10, 5], "beard_weights": [30, 50, 20],
    },
    "Cashmere": {
        "biomes": {"tundra", "alpine_mountain", "boreal"},
        "genes": {
            "milk_volume_gene":   (0.5, 0.9), "milk_richness_gene": (0.8, 1.1),
            "refill_rate_gene":   (0.8, 1.2), "constitution_gene":  (1.0, 1.3),
            "fiber_gene": (0.6, 1.0),
        },
        "coat_color_weights": [30, 30, 25, 15], "pattern_weights": [85, 8, 5, 2],
        "horn_weights": [70, 15, 10, 5], "ear_weights": [85, 10, 5], "beard_weights": [35, 45, 20],
    },
}

GOAT_BIOME_MAP: dict = {}
for _goat_breed, _goat_profile in GOAT_BREED_PROFILES.items():
    for _goat_biome in _goat_profile["biomes"]:
        GOAT_BIOME_MAP.setdefault(_goat_biome, []).append(_goat_breed)
SHEEP_WOOL_PATTERN_ORDER = ["solid", "spotted", "badgerface", "piebald"]
SHEEP_FACE_WOOL_ORDER    = ["open", "covered"]   # open = bare face, covered = wool-covered face
SHEEP_HORN_ORDER         = ["none", "single_curved", "double_curved", "spiral"]
SHEEP_EAR_ORDER          = ["upright", "drooping"]
SHEEP_TAIL_ORDER         = ["normal", "fat_tailed", "stub"]

# fleece_weight_gene:  raw float — round() gives wool bundle count (0.5–3.5)
# wool_fineness_gene:  quality stat for display / future items (0.7–1.3)
# wool_length_gene:    staple length — drives visual puff + small yield modifier (0.0–1.0)
# regrow_rate_gene:    divides into REGROW_TIME — higher = fleece grows back faster
# milk_yield_gene:     sheep milk bottles per bucket — round() gives count (0.5–1.8)
# constitution_gene:   hardiness — sets starting health on spawn (0.7–1.3 → 2–4 hp)
SHEEP_BREED_PROFILES = {
    # ── Premium wool ─────────────────────────────────────────────────────
    "Merino": {
        "biomes": {"temperate", "rolling_hills", "savanna"},
        "genes": {
            "fleece_weight_gene": (2.0, 3.0), "wool_fineness_gene": (1.1, 1.3),
            "wool_length_gene":   (0.3, 0.6),  "regrow_rate_gene":   (0.8, 1.1),
            "milk_yield_gene":    (0.5, 0.8),  "constitution_gene":  (0.8, 1.1),
        },
        "wool_color_weights": [80, 15, 4, 1], "pattern_weights": [92, 4, 4, 0],
        "face_wool_weights": [20, 80], "horn_weights": [75, 20, 5, 0],
        "ear_weights": [20, 80], "tail_weights": [95, 0, 5], "dark_face": False,
    },
    "Rambouillet": {
        "biomes": {"alpine_mountain", "temperate", "boreal"},
        "genes": {
            "fleece_weight_gene": (2.0, 2.8), "wool_fineness_gene": (1.0, 1.3),
            "wool_length_gene":   (0.3, 0.5),  "regrow_rate_gene":   (0.9, 1.2),
            "milk_yield_gene":    (0.6, 0.9),  "constitution_gene":  (0.9, 1.2),
        },
        "wool_color_weights": [85, 12, 2, 1], "pattern_weights": [95, 2, 3, 0],
        "face_wool_weights": [30, 70], "horn_weights": [60, 30, 10, 0],
        "ear_weights": [30, 70], "tail_weights": [95, 0, 5], "dark_face": False,
    },
    # ── Long / coarse wool ───────────────────────────────────────────────
    "Lincoln": {
        "biomes": {"temperate", "birch_forest", "rolling_hills"},
        "genes": {
            "fleece_weight_gene": (1.5, 2.5), "wool_fineness_gene": (0.7, 0.9),
            "wool_length_gene":   (0.7, 1.0),  "regrow_rate_gene":   (0.6, 0.9),
            "milk_yield_gene":    (0.5, 0.8),  "constitution_gene":  (0.9, 1.2),
        },
        "wool_color_weights": [60, 30, 8, 2], "pattern_weights": [90, 5, 5, 0],
        "face_wool_weights": [85, 15], "horn_weights": [70, 25, 5, 0],
        "ear_weights": [85, 15], "tail_weights": [92, 0, 8], "dark_face": False,
    },
    # ── Medium / dual-purpose ─────────────────────────────────────────────
    "Corriedale": {
        "biomes": {"temperate", "rolling_hills"},
        "genes": {
            "fleece_weight_gene": (1.5, 2.2), "wool_fineness_gene": (0.9, 1.1),
            "wool_length_gene":   (0.4, 0.7),  "regrow_rate_gene":   (0.9, 1.2),
            "milk_yield_gene":    (0.7, 1.0),  "constitution_gene":  (0.9, 1.2),
        },
        "wool_color_weights": [70, 20, 8, 2], "pattern_weights": [88, 7, 5, 0],
        "face_wool_weights": [80, 20], "horn_weights": [65, 25, 10, 0],
        "ear_weights": [80, 20], "tail_weights": [92, 0, 8], "dark_face": False,
    },
    "Icelandic": {
        "biomes": {"tundra", "alpine_mountain"},
        "genes": {
            "fleece_weight_gene": (1.8, 2.8), "wool_fineness_gene": (0.9, 1.2),
            "wool_length_gene":   (0.5, 0.8),  "regrow_rate_gene":   (1.0, 1.4),
            "milk_yield_gene":    (1.0, 1.5),  "constitution_gene":  (1.0, 1.3),
        },
        "wool_color_weights": [45, 25, 20, 10], "pattern_weights": [65, 15, 15, 5],
        "face_wool_weights": [70, 30], "horn_weights": [55, 35, 10, 0],
        "ear_weights": [85, 15], "tail_weights": [92, 0, 8], "dark_face": False,
    },
    "Churro": {
        "biomes": {"arid_steppe", "steppe"},
        "genes": {
            "fleece_weight_gene": (1.2, 2.0), "wool_fineness_gene": (0.8, 1.1),
            "wool_length_gene":   (0.5, 0.8),  "regrow_rate_gene":   (1.0, 1.4),
            "milk_yield_gene":    (0.7, 1.1),  "constitution_gene":  (0.9, 1.2),
        },
        "wool_color_weights": [55, 20, 20, 5], "pattern_weights": [75, 10, 15, 0],
        "face_wool_weights": [80, 20], "horn_weights": [20, 35, 40, 5],
        "ear_weights": [75, 25], "tail_weights": [88, 5, 7], "dark_face": False,
    },
    # ── Meat breeds ───────────────────────────────────────────────────────
    "Suffolk": {
        "biomes": {"temperate", "savanna", "rolling_hills"},
        "genes": {
            "fleece_weight_gene": (0.8, 1.5), "wool_fineness_gene": (0.8, 1.0),
            "wool_length_gene":   (0.1, 0.3),  "regrow_rate_gene":   (1.0, 1.4),
            "milk_yield_gene":    (0.6, 1.0),  "constitution_gene":  (0.9, 1.2),
        },
        "wool_color_weights": [90, 8, 2, 0], "pattern_weights": [95, 2, 3, 0],
        "face_wool_weights": [100, 0], "horn_weights": [100, 0, 0, 0],
        "ear_weights": [90, 10], "tail_weights": [92, 0, 8], "dark_face": True,
    },
    "Dorper": {
        "biomes": {"arid_steppe", "desert", "savanna"},
        "genes": {
            "fleece_weight_gene": (0.5, 1.0),  "wool_fineness_gene": (0.7, 0.9),
            "wool_length_gene":   (0.0, 0.2),   "regrow_rate_gene":   (1.2, 1.8),
            "milk_yield_gene":    (0.5, 0.8),   "constitution_gene":  (1.0, 1.3),
        },
        "wool_color_weights": [70, 5, 5, 20], "pattern_weights": [65, 10, 10, 15],
        "face_wool_weights": [100, 0], "horn_weights": [55, 30, 15, 0],
        "ear_weights": [85, 15], "tail_weights": [90, 0, 10], "dark_face": True,
    },
    # ── Primitive / heritage ──────────────────────────────────────────────
    "Soay": {
        "biomes": {"boreal", "tundra", "alpine_mountain"},
        "genes": {
            "fleece_weight_gene": (0.8, 1.3), "wool_fineness_gene": (0.8, 1.1),
            "wool_length_gene":   (0.2, 0.5),  "regrow_rate_gene":   (0.9, 1.3),
            "milk_yield_gene":    (0.5, 0.8),  "constitution_gene":  (1.0, 1.3),
        },
        "wool_color_weights": [5, 15, 65, 15], "pattern_weights": [50, 20, 30, 0],
        "face_wool_weights": [90, 10], "horn_weights": [20, 50, 30, 0],
        "ear_weights": [90, 10], "tail_weights": [90, 0, 10], "dark_face": False,
    },
    "Karakul": {
        "biomes": {"arid_steppe", "desert"},
        "genes": {
            "fleece_weight_gene": (0.8, 1.4), "wool_fineness_gene": (0.8, 1.1),
            "wool_length_gene":   (0.3, 0.6),  "regrow_rate_gene":   (0.9, 1.2),
            "milk_yield_gene":    (0.6, 1.0),  "constitution_gene":  (1.0, 1.3),
        },
        "wool_color_weights": [5, 35, 20, 40], "pattern_weights": [80, 5, 10, 5],
        "face_wool_weights": [90, 10], "horn_weights": [30, 35, 30, 5],
        "ear_weights": [25, 75], "tail_weights": [10, 85, 5], "dark_face": False,
    },
    "Hebridean": {
        "biomes": {"boreal", "tundra"},
        "genes": {
            "fleece_weight_gene": (0.7, 1.2), "wool_fineness_gene": (0.8, 1.1),
            "wool_length_gene":   (0.3, 0.6),  "regrow_rate_gene":   (0.9, 1.3),
            "milk_yield_gene":    (0.5, 0.8),  "constitution_gene":  (1.0, 1.3),
        },
        "wool_color_weights": [0, 10, 10, 80], "pattern_weights": [70, 15, 10, 5],
        "face_wool_weights": [85, 15], "horn_weights": [5, 25, 50, 20],
        "ear_weights": [90, 10], "tail_weights": [92, 0, 8], "dark_face": False,
    },
    "Jacob": {
        "biomes": {"temperate", "rolling_hills", "birch_forest"},
        "genes": {
            "fleece_weight_gene": (1.0, 1.8), "wool_fineness_gene": (0.9, 1.2),
            "wool_length_gene":   (0.4, 0.7),  "regrow_rate_gene":   (0.9, 1.3),
            "milk_yield_gene":    (0.7, 1.1),  "constitution_gene":  (0.9, 1.2),
        },
        "wool_color_weights": [40, 15, 20, 25], "pattern_weights": [10, 60, 10, 20],
        "face_wool_weights": [80, 20], "horn_weights": [5, 15, 50, 30],
        "ear_weights": [85, 15], "tail_weights": [92, 0, 8], "dark_face": False,
    },
}

SHEEP_BIOME_MAP: dict = {}
for _sheep_breed, _sheep_profile in SHEEP_BREED_PROFILES.items():
    for _sheep_biome in _sheep_profile["biomes"]:
        SHEEP_BIOME_MAP.setdefault(_sheep_biome, []).append(_sheep_breed)

LLAMA_COLOR_ORDER   = ["white", "fawn", "brown", "black", "grey"]
LLAMA_PATTERN_ORDER = ["solid", "tipped", "spotted", "appaloosa"]
LLAMA_EAR_ORDER     = ["banana", "upright", "short"]

# Llama / camelid breeds — highland & arid steppe fiber animals.
# fleece_weight_gene:  raw float — round() gives wool bundle count (0.5–3.5)
# fiber_fineness_gene: quality stat for display / future premium recipes (0.7–1.5)
# fiber_length_gene:   staple length — drives visual fluff + yield modifier (0.0–1.0)
# regrow_rate_gene:    divides into REGROW_TIME — higher = regrows wool faster
# constitution_gene:   sets starting health (0.7–1.3)
LLAMA_BREED_PROFILES = {
    # ── Classic pack llama ───────────────────────────────────────────────
    "Classic Llama": {
        "biomes": {"rocky_mountain", "alpine_mountain", "arid_steppe", "canyon", "red_rock", "steppe"},
        "genes": {
            "fleece_weight_gene": (1.5, 2.6), "fiber_fineness_gene": (0.8, 1.0),
            "fiber_length_gene":  (0.4, 0.7), "regrow_rate_gene":    (0.9, 1.2),
            "constitution_gene":  (1.0, 1.3),
        },
        "color_weights":   [30, 30, 25, 10, 5],
        "pattern_weights": [60, 20, 15, 5],
        "ear_weights":     [80, 15, 5],
    },
    # ── Heavy-fleece wooly llama (Ccara/Tampuli) ─────────────────────────
    "Wooly Llama": {
        "biomes": {"alpine_mountain", "rocky_mountain"},
        "genes": {
            "fleece_weight_gene": (2.2, 3.4), "fiber_fineness_gene": (0.9, 1.1),
            "fiber_length_gene":  (0.6, 1.0), "regrow_rate_gene":    (0.7, 1.0),
            "constitution_gene":  (0.9, 1.2),
        },
        "color_weights":   [40, 20, 25, 10, 5],
        "pattern_weights": [70, 15, 10, 5],
        "ear_weights":     [85, 10, 5],
    },
    # ── Huacaya alpaca — dense crimped fleece ────────────────────────────
    "Huacaya Alpaca": {
        "biomes": {"alpine_mountain", "rocky_mountain", "arid_steppe"},
        "genes": {
            "fleece_weight_gene": (1.0, 1.8), "fiber_fineness_gene": (1.2, 1.5),
            "fiber_length_gene":  (0.5, 0.8), "regrow_rate_gene":    (0.9, 1.2),
            "constitution_gene":  (0.8, 1.1),
        },
        "color_weights":   [35, 30, 20, 10, 5],
        "pattern_weights": [80, 10, 5, 5],
        "ear_weights":     [10, 80, 10],
    },
    # ── Suri alpaca — long, silky locks ──────────────────────────────────
    "Suri Alpaca": {
        "biomes": {"alpine_mountain", "rocky_mountain"},
        "genes": {
            "fleece_weight_gene": (0.9, 1.6), "fiber_fineness_gene": (1.2, 1.5),
            "fiber_length_gene":  (0.8, 1.0), "regrow_rate_gene":    (0.8, 1.1),
            "constitution_gene":  (0.7, 1.0),
        },
        "color_weights":   [40, 25, 20, 10, 5],
        "pattern_weights": [85, 8, 5, 2],
        "ear_weights":     [15, 75, 10],
    },
    # ── Guanaco — wild lean camelid ──────────────────────────────────────
    "Guanaco": {
        "biomes": {"arid_steppe", "canyon", "red_rock", "rocky_mountain", "steppe"},
        "genes": {
            "fleece_weight_gene": (0.7, 1.3), "fiber_fineness_gene": (1.0, 1.3),
            "fiber_length_gene":  (0.2, 0.5), "regrow_rate_gene":    (1.0, 1.4),
            "constitution_gene":  (1.0, 1.3),
        },
        "color_weights":   [0, 75, 20, 0, 5],
        "pattern_weights": [85, 10, 5, 0],
        "ear_weights":     [5, 90, 5],
    },
}

LLAMA_BIOME_MAP: dict = {}
for _llama_breed, _llama_profile in LLAMA_BREED_PROFILES.items():
    for _llama_biome in _llama_profile["biomes"]:
        LLAMA_BIOME_MAP.setdefault(_llama_biome, []).append(_llama_breed)

YAK_COLOR_ORDER   = ["black", "brown", "white", "piebald", "golden"]
YAK_HORN_ORDER    = ["wide", "curved", "short", "polled"]
YAK_SKIRT_ORDER   = ["full", "medium", "short"]   # the long body hair "skirt"

# Yak — high-altitude bovid. Shaggy fiber + rich milk + heavy meat.
# milk_volume_gene:   bottles per milking (0.8–2.5)
# milk_richness_gene: quality multiplier (1.0–1.6) — yak milk is famously rich
# fleece_weight_gene: wool bundle count per shear (0.6–2.4)
# fiber_length_gene:  staple length, drives visual skirt + yield modifier (0.3–1.0)
# regrow_rate_gene:   divides into REGROW_TIME (0.5–1.5)
# constitution_gene:  starting health multiplier (0.8–1.4)
YAK_BREED_PROFILES = {
    # ── Domestic yak — balanced milk + wool ─────────────────────────────
    "Domestic Yak": {
        "biomes": {"alpine_mountain", "rocky_mountain", "tundra"},
        "genes": {
            "milk_volume_gene":   (1.0, 1.8), "milk_richness_gene":  (1.1, 1.4),
            "fleece_weight_gene": (1.2, 2.0), "fiber_length_gene":   (0.5, 0.9),
            "regrow_rate_gene":   (0.8, 1.2), "constitution_gene":   (1.0, 1.3),
        },
        "color_weights": [55, 25, 10,  8, 2],
        "horn_weights":  [40, 35, 20,  5],
        "skirt_weights": [55, 35, 10],
    },
    # ── Wild yak — bigger, more meat, less tame milk ────────────────────
    "Wild Yak": {
        "biomes": {"alpine_mountain", "tundra"},
        "genes": {
            "milk_volume_gene":   (0.6, 1.2), "milk_richness_gene":  (1.0, 1.3),
            "fleece_weight_gene": (1.8, 2.6), "fiber_length_gene":   (0.7, 1.0),
            "regrow_rate_gene":   (0.6, 0.9), "constitution_gene":   (1.2, 1.4),
        },
        "color_weights": [75, 15,  5,  5, 0],
        "horn_weights":  [70, 20, 10,  0],
        "skirt_weights": [80, 18,  2],
    },
    # ── Dzo (yak/cow hybrid) — lowland-friendly, lighter coat ───────────
    "Dzo": {
        "biomes": {"rocky_mountain", "boreal", "alpine_mountain"},
        "genes": {
            "milk_volume_gene":   (1.4, 2.4), "milk_richness_gene":  (1.0, 1.3),
            "fleece_weight_gene": (0.7, 1.4), "fiber_length_gene":   (0.3, 0.6),
            "regrow_rate_gene":   (0.9, 1.3), "constitution_gene":   (0.9, 1.2),
        },
        "color_weights": [30, 40, 15, 12, 3],
        "horn_weights":  [25, 45, 25,  5],
        "skirt_weights": [15, 55, 30],
    },
}

YAK_BIOME_MAP: dict = {}
for _yak_breed, _yak_profile in YAK_BREED_PROFILES.items():
    for _yak_biome in _yak_profile["biomes"]:
        YAK_BIOME_MAP.setdefault(_yak_biome, []).append(_yak_breed)

# horn_length_gene: 0.0 = polled, 1.0 = maximum Longhorn spread
# hair_length_gene: 0.0 = bare, 1.0 = maximum shaggy (Yak/Highland)
# milk_volume_gene: expected bottles per milking — round() gives actual count (1-3+)
# milk_richness_gene: quality multiplier used for display and future cream/butter items
# refill_rate_gene: divides into REFILL_TIME — higher = refills faster
COW_BREED_PROFILES = {
    # ── Dairy leaders ─────────────────────────────────────────────────────
    "Holstein": {
        "biomes": {"temperate", "rolling_hills", "birch_forest"},
        "genes": {
            "milk_volume_gene":   (2.0, 3.0), "milk_richness_gene": (1.0, 1.2),
            "refill_rate_gene":   (1.1, 1.5), "beef_quality_gene":  (0.7, 1.0),
            "horn_length_gene":   (0.0, 0.05), "hair_length_gene":  (0.0, 0.15),
        },
        "coat_colors": [(220, 218, 215), (235, 232, 228)],
        "hide_weights": [10, 20, 10, 60],
    },
    "Jersey": {
        "biomes": {"temperate", "rolling_hills"},
        "genes": {
            "milk_volume_gene":   (1.3, 2.0), "milk_richness_gene": (1.1, 1.3),
            "refill_rate_gene":   (1.0, 1.4), "beef_quality_gene":  (0.6, 0.9),
            "horn_length_gene":   (0.05, 0.25), "hair_length_gene": (0.0, 0.15),
        },
        "coat_colors": [(190, 155, 95), (175, 140, 80), (205, 168, 108)],
        "hide_weights": [60, 30, 10, 0],
    },
    "Brown Swiss": {
        "biomes": {"boreal", "alpine_mountain", "temperate"},
        "genes": {
            "milk_volume_gene":   (1.8, 2.8), "milk_richness_gene": (0.9, 1.2),
            "refill_rate_gene":   (1.0, 1.4), "beef_quality_gene":  (0.8, 1.1),
            "horn_length_gene":   (0.15, 0.45), "hair_length_gene": (0.1, 0.3),
        },
        "coat_colors": [(145, 120, 100), (160, 135, 110), (130, 108, 90)],
        "hide_weights": [75, 20, 5, 0],
    },
    "Guernsey": {
        "biomes": {"temperate", "rolling_hills"},
        "genes": {
            "milk_volume_gene":   (1.5, 2.3), "milk_richness_gene": (1.1, 1.3),
            "refill_rate_gene":   (1.0, 1.4), "beef_quality_gene":  (0.7, 1.0),
            "horn_length_gene":   (0.05, 0.3), "hair_length_gene":  (0.0, 0.15),
        },
        "coat_colors": [(210, 165, 85), (195, 150, 70), (225, 180, 100)],
        "hide_weights": [20, 30, 10, 40],
    },
    # ── Dual-purpose ──────────────────────────────────────────────────────
    "Simmental": {
        "biomes": {"temperate", "rolling_hills", "birch_forest"},
        "genes": {
            "milk_volume_gene":   (1.3, 2.0), "milk_richness_gene": (0.9, 1.1),
            "refill_rate_gene":   (0.9, 1.2), "beef_quality_gene":  (0.9, 1.2),
            "horn_length_gene":   (0.15, 0.45), "hair_length_gene": (0.0, 0.2),
        },
        "coat_colors": [(195, 130, 55), (180, 115, 45), (210, 145, 65)],
        "hide_weights": [20, 10, 20, 50],
    },
    "Dexter": {
        "biomes": {"temperate", "birch_forest", "boreal"},
        "genes": {
            "milk_volume_gene":   (1.0, 1.8), "milk_richness_gene": (0.9, 1.2),
            "refill_rate_gene":   (0.9, 1.3), "beef_quality_gene":  (0.9, 1.2),
            "horn_length_gene":   (0.1, 0.4),  "hair_length_gene":  (0.0, 0.25),
        },
        "coat_colors": [(50, 35, 22), (65, 45, 28), (28, 18, 12)],
        "hide_weights": [85, 10, 5, 0],
    },
    # ── Beef / range ──────────────────────────────────────────────────────
    "Angus": {
        "biomes": {"temperate", "boreal", "rolling_hills", "birch_forest"},
        "genes": {
            "milk_volume_gene":   (0.7, 1.2), "milk_richness_gene": (0.7, 1.0),
            "refill_rate_gene":   (0.7, 1.0), "beef_quality_gene":  (1.1, 1.3),
            "horn_length_gene":   (0.0, 0.05), "hair_length_gene":  (0.0, 0.15),
        },
        "coat_colors": [(30, 22, 18), (40, 30, 24)],
        "hide_weights": [100, 0, 0, 0],
    },
    "Hereford": {
        "biomes": {"temperate", "rolling_hills", "savanna"},
        "genes": {
            "milk_volume_gene":   (0.8, 1.5), "milk_richness_gene": (0.8, 1.1),
            "refill_rate_gene":   (0.8, 1.1), "beef_quality_gene":  (0.9, 1.2),
            "horn_length_gene":   (0.2, 0.5),  "hair_length_gene":  (0.0, 0.2),
        },
        "coat_colors": [(175, 75, 35), (160, 65, 30), (185, 85, 40)],
        "hide_weights": [30, 0, 30, 40],
    },
    "Longhorn": {
        "biomes": {"arid_steppe", "savanna", "steppe", "desert"},
        "genes": {
            "milk_volume_gene":   (0.6, 1.1), "milk_richness_gene": (0.7, 1.0),
            "refill_rate_gene":   (0.7, 1.0), "beef_quality_gene":  (0.8, 1.1),
            "horn_length_gene":   (0.75, 1.0), "hair_length_gene":  (0.0, 0.15),
        },
        "coat_colors": [(170, 115, 60), (145, 95, 45), (110, 75, 35)],
        "hide_weights": [50, 30, 0, 20],
    },
    "Zebu": {
        "biomes": {"tropical", "desert"},
        "genes": {
            "milk_volume_gene":   (0.6, 1.0), "milk_richness_gene": (0.7, 1.0),
            "refill_rate_gene":   (0.7, 1.0), "beef_quality_gene":  (0.8, 1.1),
            "horn_length_gene":   (0.2, 0.5),  "hair_length_gene":  (0.0, 0.15),
        },
        "coat_colors": [(185, 178, 170), (200, 193, 185), (165, 158, 150)],
        "hide_weights": [85, 10, 5, 0],
    },
    # ── Cold/mountain ─────────────────────────────────────────────────────
    "Highland": {
        "biomes": {"boreal", "tundra", "alpine_mountain"},
        "genes": {
            "milk_volume_gene":   (0.7, 1.2), "milk_richness_gene": (0.8, 1.1),
            "refill_rate_gene":   (0.7, 1.0), "beef_quality_gene":  (0.9, 1.2),
            "horn_length_gene":   (0.2, 0.55), "hair_length_gene":  (0.7, 1.0),
        },
        "coat_colors": [(185, 100, 45), (155, 80, 35), (210, 170, 100)],
        "hide_weights": [80, 10, 10, 0],
    },
    "Brahman": {
        "biomes": {"tropical", "savanna", "desert"},
        "genes": {
            "milk_volume_gene":   (0.6, 1.1), "milk_richness_gene": (0.7, 1.0),
            "refill_rate_gene":   (0.7, 1.0), "beef_quality_gene":  (0.8, 1.1),
            "horn_length_gene":   (0.2, 0.55), "hair_length_gene":  (0.0, 0.2),
        },
        "coat_colors": [(200, 195, 190), (175, 170, 165), (220, 215, 210)],
        "hide_weights": [85, 10, 5, 0],
    },
    "Yak": {
        "biomes": {"tundra", "alpine_mountain"},
        "genes": {
            "milk_volume_gene":   (1.0, 1.8), "milk_richness_gene": (1.0, 1.2),
            "refill_rate_gene":   (0.9, 1.2), "beef_quality_gene":  (0.8, 1.1),
            "horn_length_gene":   (0.3, 0.65), "hair_length_gene":  (0.75, 1.0),
        },
        "coat_colors": [(30, 22, 16), (45, 32, 22), (20, 15, 10)],
        "hide_weights": [90, 5, 5, 0],
    },
}

COW_BIOME_MAP: dict = {}
for _cow_breed, _cow_profile in COW_BREED_PROFILES.items():
    for _cow_biome in _cow_profile["biomes"]:
        COW_BIOME_MAP.setdefault(_cow_biome, []).append(_cow_breed)


def _expressed_categorical(allele_pair, order):
    """Return whichever allele is more dominant (lowest index in order list)."""
    a, b = allele_pair
    ai = order.index(a) if a in order else len(order)
    bi = order.index(b) if b in order else len(order)
    return order[min(ai, bi)]


class Animal:
    def __init__(self, x, y, world, animal_id):
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.world = world
        self.on_ground = False
        self.facing = 1  # 1=right, -1=left
        self.animal_id = animal_id
        self._wander_timer = random.uniform(0.5, 3.0)
        self._wander_dir = random.choice([-1, 0, 0, 1])
        self._harvest_time = 0.0
        self.being_harvested = False

        # Genetics
        self.uid = str(uuid.uuid4())
        self.parent_a_uid = None
        self.parent_b_uid = None
        self.no_breed = False
        self.genotype = {}
        self.traits = {
            "color_shift": (
                random.uniform(-0.20, 0.20),
                random.uniform(-0.20, 0.20),
                random.uniform(-0.20, 0.20),
            ),
            "size": random.uniform(0.87, 1.13),
            "productivity": random.uniform(0.80, 1.20),
            "mutation": None,
            "sex": random.choice(["female", "male"]),
        }
        self._init_base_genotype()

        # Health / death
        self.health = 3
        self.dead = False
        self._kill_timer = 0.0

        # Breeding
        self._breed_cooldown = random.uniform(300.0, 900.0)

        # Taming
        self.tamed = False
        self.tame_progress = 0

        # Grazing — 1.0 = full belly, 0.0 = starving. Multiplies wool/milk/egg yields.
        self.fullness = 1.0
        # Hydration — separate stat, decays faster than fullness. Yields are min(fullness, hydration).
        self.hydration = 1.0
        # Rolling care average — EMA of min(fullness, hydration). High score → premium yields.
        self.care_score = 1.0
        # Buffs (in seconds remaining)
        self.salt_buff_timer = 0.0
        # Pen-recognition score (0.0 → 1.0); recomputed periodically by `_kept_tick`.
        self.kept_score = 0.0
        self._pen_check_timer = random.uniform(0.0, 10.0)
        # Sleeping state — true at night for tamed animals; halves need decay & blocks wander.
        self._sleeping = False

    # Subclasses define these as class attributes
    ANIMAL_W = 0
    ANIMAL_H = 0
    PREFERRED_FOODS = ()
    MEAT_DROP = ("raw_mutton", 1)

    @property
    def W(self):
        mut = self.traits.get("mutation")
        if mut == "giant":
            s = 1.4
        elif mut == "miniature":
            s = 0.6
        else:
            s = self.traits.get("size", 1.0)
        return int(self.ANIMAL_W * s)

    @property
    def H(self):
        mut = self.traits.get("mutation")
        if mut == "giant":
            s = 1.4
        elif mut == "miniature":
            s = 0.6
        else:
            s = self.traits.get("size", 1.0)
        return int(self.ANIMAL_H * s)

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.W, self.H)

    def _has_jump_clearance(self):
        left  = int(self.x // BLOCK_SIZE)
        right = int((self.x + self.W - 1) // BLOCK_SIZE)
        top   = int(self.y // BLOCK_SIZE)
        for bx in range(left, right + 1):
            if self.world.is_solid(bx, top - 1):
                return False
        return True

    def _move_x(self, dx):
        self.x += dx
        if self._collides():
            hit_fence = self._collides_with_fence()
            self.x -= dx
            self.vx = 0.0
            if self.on_ground and not hit_fence and self._has_jump_clearance():
                self.vy = JUMP_FORCE
            else:
                self._wander_dir = -self._wander_dir

    def _move_y(self, dy):
        self.y += dy
        if self._collides() or (dy > 0 and self._feet_in_water()):
            self.y -= dy
            self.vy = 0.0
            if dy > 0:
                self.on_ground = True
        else:
            if dy > 0:
                self.on_ground = False

    def _collides(self):
        left  = int(self.x // BLOCK_SIZE)
        right = int((self.x + self.W - 1) // BLOCK_SIZE)
        top   = int(self.y // BLOCK_SIZE)
        bot   = int((self.y + self.H - 1) // BLOCK_SIZE)
        for bx in range(left, right + 1):
            for by in range(top, bot + 1):
                if self.world.is_solid(bx, by):
                    return True
        return False

    def _collides_with_fence(self):
        left  = int(self.x // BLOCK_SIZE)
        right = int((self.x + self.W - 1) // BLOCK_SIZE)
        top   = int(self.y // BLOCK_SIZE)
        bot   = int((self.y + self.H - 1) // BLOCK_SIZE)
        for bx in range(left, right + 1):
            for by in range(top, bot + 1):
                bid = self.world.get_block(bx, by)
                if bid in (WOOD_FENCE, IRON_FENCE):
                    return True
        return False

    def _fence_in_direction(self, direction):
        self.x += direction
        result = self._collides_with_fence()
        self.x -= direction
        return result

    def _near_fence(self, radius=4):
        cx = int((self.x + self.W / 2) // BLOCK_SIZE)
        cy = int((self.y + self.H / 2) // BLOCK_SIZE)
        for bx in range(cx - radius, cx + radius + 1):
            for by in range(cy - radius, cy + radius + 1):
                bid = self.world.get_block(bx, by)
                if bid in (WOOD_FENCE, IRON_FENCE):
                    return True
        return False

    def _in_ladder(self):
        left  = int(self.x // BLOCK_SIZE)
        right = int((self.x + self.W - 1) // BLOCK_SIZE)
        top   = int(self.y // BLOCK_SIZE)
        bot   = int((self.y + self.H - 1) // BLOCK_SIZE)
        for bx in range(left, right + 1):
            for by in range(top, bot + 1):
                if self.world.get_block(bx, by) == LADDER:
                    return True
        return False

    def _feet_in_water(self):
        left = int(self.x // BLOCK_SIZE)
        right = int((self.x + self.W - 1) // BLOCK_SIZE)
        bot = int((self.y + self.H - 1) // BLOCK_SIZE)
        for bx in range(left, right + 1):
            if self.world.get_block(bx, bot) == WATER:
                return True
        return False

    def _in_water(self):
        left  = int(self.x // BLOCK_SIZE)
        right = int((self.x + self.W - 1) // BLOCK_SIZE)
        top   = int(self.y // BLOCK_SIZE)
        bot   = int((self.y + self.H - 1) // BLOCK_SIZE)
        for bx in range(left, right + 1):
            for by in range(top, bot + 1):
                if self.world.get_block(bx, by) == WATER:
                    return True
        return False

    def _unstuck(self):
        if not self._collides():
            return
        by = int(self.y // BLOCK_SIZE)
        for dy in range(1, self.world.height):
            ty = by - dy
            if ty < 0:
                break
            test_y = ty * BLOCK_SIZE
            old_y, self.y = self.y, float(test_y)
            if not self._collides():
                self.vy = 0.0
                self.on_ground = False
                return
            self.y = old_y

    def update(self, dt):
        if self.dead:
            return

        self._unstuck()
        self._graze_tick(dt)
        self._kept_tick(dt)

        # Breeding cooldown — well-fed animals tick faster, starved animals stall
        breed_speed = 0.0 if self._is_starving() else (0.5 + 1.0 * min(self.fullness, self.hydration))
        self._breed_cooldown -= dt * breed_speed
        if (self._breed_cooldown <= 0
                and self.on_ground
                and not self.being_harvested
                and not self.no_breed
                and self._can_breed()):
            same = [e for e in self.world.entities
                    if type(e) is type(self) and not e.dead]
            if len(same) < 500:
                for other in same:
                    if (other is self or other._breed_cooldown > 0
                            or other.no_breed or not other._can_breed()):
                        continue
                    dx = (self.x + self.W / 2 - other.x - other.W / 2) / BLOCK_SIZE
                    dy = (self.y + self.H / 2 - other.y - other.H / 2) / BLOCK_SIZE
                    if (dx * dx + dy * dy) ** 0.5 <= 3.0:
                        self._breed(other, self.world)
                        break

        # Tamed: follow player instead of wandering (not when penned in a fence)
        if self.tamed and not self._near_fence():
            player = getattr(self.world, '_player_ref', None)
            if player is not None:
                pdx = (player.x + PLAYER_W / 2) - (self.x + self.W / 2)
                pdy = (player.y + PLAYER_H / 2) - (self.y + self.H / 2)
                dist = ((pdx / BLOCK_SIZE) ** 2 + (pdy / BLOCK_SIZE) ** 2) ** 0.5
                if dist > 2.5:
                    desired_dir = 1 if pdx > 0 else -1
                    if self._fence_in_direction(desired_dir):
                        self.vx = 0.0
                    else:
                        self.vx = ANIMAL_MOVE_SPEED * desired_dir
                else:
                    self.vx = 0.0
                if self.vx != 0:
                    self.facing = 1 if self.vx > 0 else -1
                if self._in_ladder():
                    if self.vx != 0:
                        self.vy = -ANIMAL_CLIMB_SPEED
                    else:
                        self.vy = 0
                elif self._in_water():
                    self.vy = min(self.vy + GRAVITY * 0.2, 2.5)
                    self.vx *= 0.8
                else:
                    self.vy = min(self.vy + GRAVITY, MAX_FALL)
                self._move_x(self.vx)
                self._move_y(self.vy)
                return  # skip wander

        # Normal wander — sleeping/starving animals stand still
        self._wander_timer -= dt
        if self._wander_timer <= 0:
            self._wander_timer = random.uniform(1.5, 5.0)
            if self._is_starving() or self._sleeping:
                self._wander_dir = 0   # plant feet
            else:
                self._wander_dir = random.choice([-1, -1, 0, 0, 0, 1, 1])

        if self._sleeping:
            speed_mult = 0.0
        elif self._is_starving():
            speed_mult = 0.4
        else:
            speed_mult = 1.0
        self.vx = self._wander_dir * ANIMAL_MOVE_SPEED * speed_mult
        if self.vx != 0:
            self.facing = 1 if self.vx > 0 else -1

        if self._in_ladder():
            if self.vx != 0:
                self.vy = -ANIMAL_CLIMB_SPEED
            else:
                self.vy = 0
        elif self._in_water():
            self.vy = min(self.vy + GRAVITY * 0.2, 2.5)
            self.vx *= 0.8
        else:
            self.vy = min(self.vy + GRAVITY, MAX_FALL)
        self._move_x(self.vx)
        self._move_y(self.vy)

    def _breed(self, other, world):
        if self.traits.get("sex") == other.traits.get("sex"):
            return
        cls = type(self)
        offspring = cls((self.x + other.x) / 2, (self.y + other.y) / 2, world)

        # Inherit allele-based genotype from both parents
        offspring._inherit_genotype(self, other)

        # color_shift stays blended (not allele-based)
        cs_a = self.traits["color_shift"]
        cs_b = other.traits["color_shift"]
        offspring.traits["color_shift"] = tuple(
            max(-0.25, min(0.25, (cs_a[i] + cs_b[i]) / 2 + random.uniform(-0.03, 0.03)))
            for i in range(3)
        )
        if offspring.traits.get("mutation") == "albino":
            offspring.traits["color_shift"] = (
                random.uniform(0.20, 0.25),
                random.uniform(0.20, 0.25),
                random.uniform(0.20, 0.25),
            )

        offspring.parent_a_uid = self.uid
        offspring.parent_b_uid = other.uid
        offspring.tamed = self.tamed and other.tamed
        offspring._breed_cooldown = 300.0 if offspring.traits.get("mutation") == "miniature" else 600.0
        self._breed_cooldown = 600.0
        other._breed_cooldown = 600.0
        world.entities.append(offspring)

        # Remove the most distant un-tamed animal of this type so the
        # population doesn't grow unboundedly and crowded areas stay playable.
        player = getattr(world, '_player_ref', None)
        if player is not None:
            pcx = player.x + PLAYER_W / 2
            pcy = player.y + PLAYER_H / 2
            candidates = [
                e for e in world.entities
                if type(e) is type(self) and not e.dead and not e.tamed
                and e is not offspring
            ]
            if candidates:
                farthest = max(
                    candidates,
                    key=lambda e: (e.x + e.W / 2 - pcx) ** 2 + (e.y + e.H / 2 - pcy) ** 2
                )
                farthest.dead = True

    # ------------------------------------------------------------------
    # Genetics helpers
    # ------------------------------------------------------------------

    def _init_base_genotype(self):
        """Set up base allele pairs from current trait values."""
        v = self.traits["size"]
        self.genotype["size_gene"] = [
            round(random.uniform(max(0.7, v - 0.1), min(1.3, v + 0.1)), 3),
            round(random.uniform(max(0.7, v - 0.1), min(1.3, v + 0.1)), 3),
        ]
        p = self.traits["productivity"]
        self.genotype["productivity_gene"] = [
            round(random.uniform(max(0.6, p - 0.15), min(1.4, p + 0.15)), 3),
            round(random.uniform(max(0.6, p - 0.15), min(1.4, p + 0.15)), 3),
        ]
        # Mutation gene: wild animals are rarely carriers (~5%)
        self.genotype["mutation"] = [None, None]
        if random.random() < 0.05:
            self.genotype["mutation"] = [None, random.choice(MUTATION_TYPES)]

    def _inherit_genotype(self, parent_a, parent_b):
        """Mendelian inheritance: pick one allele from each parent per gene."""
        for gene in parent_a.genotype:
            if gene not in parent_b.genotype:
                continue
            self.genotype[gene] = [
                random.choice(parent_a.genotype[gene]),
                random.choice(parent_b.genotype[gene]),
            ]
        # 3% chance one mutation allele spontaneously mutates
        if "mutation" in self.genotype and random.random() < 0.03:
            self.genotype["mutation"][random.randint(0, 1)] = random.choice(MUTATION_TYPES)
        self._apply_genotype_to_traits()

    def _apply_genotype_to_traits(self):
        """Sync expressed traits from genotype (phenotype computation)."""
        if "size_gene" in self.genotype:
            avg = (self.genotype["size_gene"][0] + self.genotype["size_gene"][1]) / 2
            self.traits["size"] = round(max(0.85, min(1.15, avg)), 3)
        if "productivity_gene" in self.genotype:
            avg = (self.genotype["productivity_gene"][0] + self.genotype["productivity_gene"][1]) / 2
            self.traits["productivity"] = round(max(0.7, min(1.3, avg)), 3)
        if "mutation" in self.genotype:
            a, b = self.genotype["mutation"]
            # Mutation only expresses when homozygous (both alleles match)
            self.traits["mutation"] = a if (a == b and a is not None) else None
        if self.traits.get("mutation") == "albino":
            self.traits["color_shift"] = (
                random.uniform(0.20, 0.25),
                random.uniform(0.20, 0.25),
                random.uniform(0.20, 0.25),
            )

    def _synthesize_genotype_from_traits(self):
        """Build genotype from saved traits — used when loading pre-genetics saves."""
        v = self.traits.get("size", 1.0)
        noise = random.uniform(-0.04, 0.04)
        self.genotype["size_gene"] = [round(max(0.7, v + noise), 3), round(max(0.7, v - noise), 3)]
        v = self.traits.get("productivity", 1.0)
        noise = random.uniform(-0.06, 0.06)
        self.genotype["productivity_gene"] = [round(max(0.6, v + noise), 3), round(max(0.6, v - noise), 3)]
        mut = self.traits.get("mutation")
        self.genotype["mutation"] = [mut, mut] if mut else [None, None]

    def in_range(self, player):
        acx = (self.x + self.W / 2) / BLOCK_SIZE
        acy = (self.y + self.H / 2) / BLOCK_SIZE
        pcx = (player.x + PLAYER_W / 2) / BLOCK_SIZE
        pcy = (player.y + PLAYER_H / 2) / BLOCK_SIZE
        return ((acx - pcx) ** 2 + (acy - pcy) ** 2) ** 0.5 <= MINE_REACH

    def try_harvest(self, player, dt):
        if self.dead:
            self.reset_harvest()
            return None
        tool = player.hotbar[player.selected_slot]
        if tool == "hunting_knife":
            self._kill_timer += dt
            self.being_harvested = True
            if self._kill_timer >= 0.5:
                self._kill_timer = 0.0
                self.health -= 1
                if self.health <= 0:
                    self.dead = True
                    self.reset_harvest()
                    item_id, base_count = self.MEAT_DROP
                    count = base_count + (1 if self.traits.get("mutation") == "giant" else 0)
                    return [(item_id, count)]
            return None
        return self._try_harvest_resource(player, dt)

    def _try_harvest_resource(self, player, dt):
        raise NotImplementedError

    def try_feed(self, player):
        if self.tamed:
            return False
        item_id = player.hotbar[player.selected_slot]
        if not item_id or item_id not in self.PREFERRED_FOODS:
            return False
        if player.inventory.get(item_id, 0) <= 0:
            return False
        player.inventory[item_id] -= 1
        if player.inventory[item_id] <= 0:
            del player.inventory[item_id]
            for i in range(HOTBAR_SIZE):
                if player.hotbar[i] == item_id:
                    player.hotbar[i] = None
                    break
        threshold = 2 if self.traits.get("mutation") == "albino" else 3
        self.tame_progress += 1
        if self.tame_progress >= threshold:
            self.tamed = True
        return True

    def reset_harvest(self):
        self._harvest_time = 0.0
        self._kill_timer = 0.0
        self.being_harvested = False

    # ── Grazing & Hydration ────────────────────────────────────────────────
    # Decay: ~21 minutes full → empty if no food source available.
    _FULLNESS_DECAY = 0.0008
    _HYDRATION_DECAY = 0.0012    # animals get thirsty faster than hungry
    _GRASS_GRAZE_RATE = 0.05
    _TROUGH_GRAZE_RATE = 0.10
    _WATER_DRINK_RATE = 0.20
    _GRASS_DEPLETE_CHANCE = 0.005  # per second while grazing — scales with trampling

    # Subclasses override to mark biomes they evolved for.
    NATIVE_BIOMES: set = set()

    # Per-biome grazing-quality multiplier (applied to grass graze rate & yield bonus).
    BIOME_PASTURE_QUALITY = {
        "temperate":       1.00,
        "rolling_hills":   1.10,
        "birch_forest":    0.85,
        "savanna":         0.90,
        "tropical":        0.85,
        "boreal":          0.70,
        "alpine_mountain": 0.80,
        "tundra":          0.55,
        "arid_steppe":     0.65,
        "desert":          0.30,
    }

    def _foot_block_xy(self):
        cx = int((self.x + self.W / 2) // BLOCK_SIZE)
        fy = int((self.y + self.H) // BLOCK_SIZE)  # one row below feet
        return cx, fy

    def _trough_nearby(self, radius=2):
        cx = int((self.x + self.W / 2) // BLOCK_SIZE)
        cy = int((self.y + self.H / 2) // BLOCK_SIZE)
        for bx in range(cx - radius, cx + radius + 1):
            for by in range(cy - radius, cy + radius + 1):
                if self.world.get_block(bx, by) == FEED_TROUGH_BLOCK:
                    return (bx, by)
        return None

    def _water_nearby(self, radius=2):
        """Return True if a water block or horse trough is within drinking range."""
        from blocks import HORSE_TROUGH_BLOCK as _HT
        cx = int((self.x + self.W / 2) // BLOCK_SIZE)
        cy = int((self.y + self.H / 2) // BLOCK_SIZE)
        for bx in range(cx - radius, cx + radius + 1):
            for by in range(cy - radius, cy + radius + 1):
                bid = self.world.get_block(bx, by)
                if bid == WATER or bid == _HT:
                    return True
        return False

    def _pasture_quality(self):
        """Multiplier for grazing speed and yield from current biome + native-species bonus."""
        if self.world is None:
            return 1.0
        bx = int((self.x + self.W / 2) // BLOCK_SIZE)
        biodome = self.world.biodome_at(bx) if hasattr(self.world, "biodome_at") else "temperate"
        base = self.BIOME_PASTURE_QUALITY.get(biodome, 0.70)
        if self.NATIVE_BIOMES and biodome in self.NATIVE_BIOMES:
            base += 0.25
        return base

    def _trampling_factor(self):
        """Multiplier for grass-deplete chance — scales with same-tile herd density."""
        if self.world is None:
            return 1.0
        bx, by = self._foot_block_xy()
        # Count nearby herd entities sharing the same grass tile column
        count = 0
        for e in self.world.entities:
            if e is self or not isinstance(e, Animal) or e.dead:
                continue
            ebx = int((e.x + e.W / 2) // BLOCK_SIZE)
            eby = int((e.y + e.H) // BLOCK_SIZE)
            if ebx == bx and abs(eby - by) <= 1:
                count += 1
        # 1 neighbor = 2×, 2 = 3×, etc. (linear)
        return 1.0 + count

    def _is_sleeping_now(self):
        """Tamed animals sleep at night. Untamed wild animals keep wandering."""
        if not self.tamed or self.world is None:
            return False
        from constants import DAY_DURATION
        tod = getattr(self.world, "time_of_day", 0.0)
        return tod >= DAY_DURATION

    def _grazing_blocked_by_weather(self):
        """Heavy rain stops grazing — animals huddle."""
        if self.world is None:
            return False
        return bool(getattr(self.world, "_rain_active", False))

    def _salt_lick_nearby(self, radius=2):
        cx = int((self.x + self.W / 2) // BLOCK_SIZE)
        cy = int((self.y + self.H / 2) // BLOCK_SIZE)
        for bx in range(cx - radius, cx + radius + 1):
            for by in range(cy - radius, cy + radius + 1):
                if self.world.get_block(bx, by) == SALT_LICK_BLOCK:
                    return True
        return False

    def _graze_tick(self, dt):
        # Sleeping animals decay needs at half rate.
        self._sleeping = self._is_sleeping_now()
        decay_mult = 0.5 if self._sleeping else 1.0
        self.fullness  = max(0.0, self.fullness  - self._FULLNESS_DECAY  * dt * decay_mult)
        self.hydration = max(0.0, self.hydration - self._HYDRATION_DECAY * dt * decay_mult)

        # Care score — slow exponential moving average of (min needs). Drives premium yields.
        target = min(self.fullness, self.hydration)
        # Time constant ~ 60s: care_score follows but lags behind real needs.
        alpha = min(1.0, dt / 60.0)
        self.care_score = self.care_score * (1.0 - alpha) + target * alpha

        # Salt buff decay
        if self.salt_buff_timer > 0:
            self.salt_buff_timer = max(0.0, self.salt_buff_timer - dt)

        if self.world is None:
            return

        # Salt lick: visiting refreshes a 5-minute productivity buff
        if self.salt_buff_timer < 60.0 and self._salt_lick_nearby():
            self.salt_buff_timer = 300.0

        # ── Drinking ──
        if self.hydration < 0.95 and self._water_nearby():
            self.hydration = min(1.0, self.hydration + self._WATER_DRINK_RATE * dt)
        # ── Feeding ──
        if self.fullness >= 0.95 or self._sleeping:
            return
        # Trough first (faster refill, ranged) — works even in rain (covered feed)
        trough_pos = self._trough_nearby()
        if trough_pos is not None:
            data = getattr(self.world, "feed_trough_data", {}).get(trough_pos)
            if data and data.get("contents", 0) > 0:
                gain = self._TROUGH_GRAZE_RATE * dt
                self.fullness = min(1.0, self.fullness + gain)
                data["progress"] = data.get("progress", 0.0) + gain
                # One unit of trough food = 0.25 fullness; bale = 4 units = 1.0 fullness
                while data["progress"] >= 0.25 and data["contents"] > 0:
                    data["progress"] -= 0.25
                    data["contents"] -= 1
                return
        # Open-pasture grazing is suppressed by heavy rain.
        if self._grazing_blocked_by_weather():
            return
        # Grass under feet — scaled by pasture quality & trampled by density
        if not self.on_ground:
            return
        bx, by = self._foot_block_xy()
        if self.world.get_block(bx, by) == GRASS:
            q = self._pasture_quality()
            self.fullness = min(1.0, self.fullness + self._GRASS_GRAZE_RATE * q * dt)
            # Roll base depletion first; only pay the O(N) trampling scan if it hits.
            if random.random() < self._GRASS_DEPLETE_CHANCE * dt:
                trample = self._trampling_factor()
                # Solo = always deplete; each additional same-tile animal adds a coin flip.
                if trample == 1 or random.random() < min(1.0, 0.5 + (trample - 1) * 0.25):
                    self.world.set_block(bx, by, DIRT)

    # ── Pen recognition ──
    # Periodically check if this animal is in a serviceable pen:
    # - both sides bounded by a fence within reasonable distance
    # - a feed trough within range
    # - water (open WATER tile or HORSE_TROUGH) within range
    # All three present → kept_score creeps toward 1.0, otherwise toward 0.0.
    _PEN_CHECK_INTERVAL = 10.0
    _PEN_FENCE_RANGE    = 14   # blocks left/right
    _PEN_AMENITY_RANGE  = 8    # blocks for trough/water

    def _has_fence_in_direction(self, direction, max_dist):
        from blocks import WOOD_FENCE as _WF, IRON_FENCE as _IF
        cx = int((self.x + self.W / 2) // BLOCK_SIZE)
        cy = int((self.y + self.H / 2) // BLOCK_SIZE)
        for d in range(1, max_dist + 1):
            bid = self.world.get_block(cx + direction * d, cy)
            if bid in (_WF, _IF):
                return True
        return False

    def _amenity_nearby(self, block_ids, radius):
        cx = int((self.x + self.W / 2) // BLOCK_SIZE)
        cy = int((self.y + self.H / 2) // BLOCK_SIZE)
        for bx in range(cx - radius, cx + radius + 1):
            for by in range(cy - radius, cy + radius + 1):
                if self.world.get_block(bx, by) in block_ids:
                    return True
        return False

    def _kept_tick(self, dt):
        if self.world is None:
            return
        self._pen_check_timer -= dt
        if self._pen_check_timer > 0:
            return
        self._pen_check_timer = self._PEN_CHECK_INTERVAL
        from blocks import HORSE_TROUGH_BLOCK as _HT
        fenced = (self._has_fence_in_direction(-1, self._PEN_FENCE_RANGE)
                  and self._has_fence_in_direction(1, self._PEN_FENCE_RANGE))
        has_food = self._amenity_nearby({FEED_TROUGH_BLOCK}, self._PEN_AMENITY_RANGE)
        has_water = self._amenity_nearby({WATER, _HT}, self._PEN_AMENITY_RANGE)
        target = 1.0 if (fenced and has_food and has_water) else 0.0
        # Drift toward target at ~0.05 per interval (gentle: ~3 minutes to fully gain/lose)
        rate = 0.05
        if target > self.kept_score:
            self.kept_score = min(1.0, self.kept_score + rate)
        else:
            self.kept_score = max(0.0, self.kept_score - rate)

    def _yield_mult(self):
        # Limiting factor: whichever stat is lower. Native-biome forage gives a small bonus.
        need = min(self.fullness, self.hydration)
        base = 0.4 + 0.9 * need
        if need > 0.7 and self.NATIVE_BIOMES:
            if self.world is not None:
                bx = int((self.x + self.W / 2) // BLOCK_SIZE)
                if self.world.biodome_at(bx) in self.NATIVE_BIOMES:
                    base *= 1.10
        # Salt-lick buff: +10% productivity while timer is active
        if self.salt_buff_timer > 0:
            base *= 1.10
        # Kept-pen buff: smooth +0..10% based on kept_score
        if self.kept_score > 0:
            base *= 1.0 + 0.10 * self.kept_score
        return base

    def _premium_drop(self, base_id):
        """Return the premium variant if care_score is consistently high.
        Premium = additional 1 of the variant on top of the standard drop."""
        if self.care_score < 0.85:
            return None
        # care_score caps at 1.0 — chance scales from 0% at 0.85 to ~60% at 1.0
        chance = (self.care_score - 0.85) / 0.15 * 0.6
        if random.random() >= chance:
            return None
        return {
            "wool":       "premium_wool",
            "sheep_milk": "premium_milk",
            "milk":       "premium_milk",
            "goat_milk":  "premium_milk",
            "egg":        "premium_egg",
        }.get(base_id)

    def _finalize_drops(self, drops, base_id):
        """Append a premium-variant bonus drop if the animal has been kept exceptionally well."""
        if drops:
            prem = self._premium_drop(base_id)
            if prem:
                drops.append((prem, 1))
        return drops or None

    def _can_breed(self):
        """Breeding gate — both needs must be reasonably met."""
        return self.fullness > 0.45 and self.hydration > 0.45

    def _is_starving(self):
        return self.fullness < 0.25 or self.hydration < 0.25


class Sheep(Animal):
    ANIMAL_W = 24
    ANIMAL_H = 18
    HARVEST_TIME = 1.5
    REGROW_TIME  = 30.0
    MILK_REFILL_TIME = 25.0
    MANURE_TIMER = 90.0
    _MANURE_ITEM = "sheep_droppings"
    MEAT_DROP = ("raw_mutton", 2)
    PREFERRED_FOODS = ("wheat", "carrot")
    NATIVE_BIOMES = {"temperate", "rolling_hills", "alpine_mountain", "boreal"}

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "sheep")
        self.has_wool = True
        self._regrow_timer = 0.0
        self._milk_refill_timer = 0.0
        self.has_manure = False
        self._manure_timer = self.MANURE_TIMER

        bx = int(float(x) // BLOCK_SIZE)
        biodome = world.biodome_at(bx) if world is not None else "temperate"
        eligible = SHEEP_BIOME_MAP.get(biodome, list(SHEEP_BREED_PROFILES.keys()))
        breed = random.choice(eligible) if eligible else "Merino"
        self.traits["breed"] = breed

        # Only females produce milk
        self.has_milk = (self.traits["sex"] == "female")

        profile = SHEEP_BREED_PROFILES.get(breed, SHEEP_BREED_PROFILES["Merino"])
        self._init_sheep_genotype(profile)

    def _init_sheep_genotype(self, profile=None):
        if profile is None:
            breed = self.traits.get("breed", "Merino")
            profile = SHEEP_BREED_PROFILES.get(breed, SHEEP_BREED_PROFILES["Merino"])

        for gene_key, (lo, hi) in profile["genes"].items():
            self.genotype[gene_key] = [
                round(random.uniform(lo, hi), 3),
                round(random.uniform(lo, hi), 3),
            ]

        wcw = profile["wool_color_weights"]
        self.genotype["wool_color_gene"] = [
            random.choices(WOOL_COLOR_ORDER, weights=wcw)[0],
            random.choices(WOOL_COLOR_ORDER, weights=wcw)[0],
        ]
        pw = profile["pattern_weights"]
        self.genotype["wool_pattern_gene"] = [
            random.choices(SHEEP_WOOL_PATTERN_ORDER, weights=pw)[0],
            random.choices(SHEEP_WOOL_PATTERN_ORDER, weights=pw)[0],
        ]
        fw = profile["face_wool_weights"]
        self.genotype["face_wool_gene"] = [
            random.choices(SHEEP_FACE_WOOL_ORDER, weights=fw)[0],
            random.choices(SHEEP_FACE_WOOL_ORDER, weights=fw)[0],
        ]
        hw = profile["horn_weights"]
        self.genotype["horn_type_gene"] = [
            random.choices(SHEEP_HORN_ORDER, weights=hw)[0],
            random.choices(SHEEP_HORN_ORDER, weights=hw)[0],
        ]
        ew = profile["ear_weights"]
        self.genotype["ear_type_gene"] = [
            random.choices(SHEEP_EAR_ORDER, weights=ew)[0],
            random.choices(SHEEP_EAR_ORDER, weights=ew)[0],
        ]
        tw = profile["tail_weights"]
        self.genotype["tail_type_gene"] = [
            random.choices(SHEEP_TAIL_ORDER, weights=tw)[0],
            random.choices(SHEEP_TAIL_ORDER, weights=tw)[0],
        ]
        self.genotype["birth_gene"] = [
            "single",
            "twin" if random.random() < 0.08 else "single",
        ]
        self._apply_genotype_to_traits()
        self.traits["dark_face"] = profile.get("dark_face", False)
        # Constitution sets starting health (2–4 hp range)
        self.health = max(2, round(self.traits.get("constitution", 1.0) * 3))

    def _apply_genotype_to_traits(self):
        super()._apply_genotype_to_traits()
        for gene, trait, lo, hi in [
            ("fleece_weight_gene", "fleece_weight", 0.5, 3.5),
            ("wool_fineness_gene", "wool_fineness", 0.7, 1.3),
            ("wool_length_gene",   "wool_length",   0.0, 1.0),
            ("regrow_rate_gene",   "regrow_rate",   0.5, 2.0),
            ("milk_yield_gene",    "milk_yield",    0.5, 1.8),
            ("constitution_gene",  "constitution",  0.7, 1.3),
            ("fleece_gene",        "fleece",        0.7, 1.3),
        ]:
            if gene in self.genotype:
                avg = sum(self.genotype[gene]) / 2
                self.traits[trait] = round(max(lo, min(hi, avg)), 3)
        for gene, trait, order in [
            ("wool_color_gene",   "wool_color",   WOOL_COLOR_ORDER),
            ("wool_pattern_gene", "wool_pattern", SHEEP_WOOL_PATTERN_ORDER),
            ("face_wool_gene",    "face_wool",    SHEEP_FACE_WOOL_ORDER),
            ("horn_type_gene",    "horn_type",    SHEEP_HORN_ORDER),
            ("ear_type_gene",     "ear_type",     SHEEP_EAR_ORDER),
            ("tail_type_gene",    "tail_type",    SHEEP_TAIL_ORDER),
            ("birth_gene",        "birth",        BIRTH_ORDER),
        ]:
            if gene in self.genotype:
                self.traits[trait] = _expressed_categorical(self.genotype[gene], order)

    def _synthesize_genotype_from_traits(self):
        super()._synthesize_genotype_from_traits()
        for gene, trait, lo, hi in [
            ("fleece_weight_gene", "fleece_weight", 0.5, 3.5),
            ("wool_fineness_gene", "wool_fineness", 0.7, 1.3),
            ("wool_length_gene",   "wool_length",   0.0, 1.0),
            ("regrow_rate_gene",   "regrow_rate",   0.5, 2.0),
            ("milk_yield_gene",    "milk_yield",    0.5, 1.8),
            ("constitution_gene",  "constitution",  0.7, 1.3),
        ]:
            v = self.traits.get(trait, (lo + hi) / 2)
            n = random.uniform(-0.03, 0.03)
            self.genotype[gene] = [round(max(lo, min(hi, v + n)), 3), round(max(lo, min(hi, v - n)), 3)]
        self.genotype["wool_color_gene"]   = [self.traits.get("wool_color", "white")] * 2
        self.genotype["wool_pattern_gene"] = [self.traits.get("wool_pattern", "solid")] * 2
        self.genotype["face_wool_gene"]    = [self.traits.get("face_wool", "open")] * 2
        self.genotype["horn_type_gene"]    = [self.traits.get("horn_type", "none")] * 2
        self.genotype["ear_type_gene"]     = [self.traits.get("ear_type", "upright")] * 2
        self.genotype["tail_type_gene"]    = [self.traits.get("tail_type", "normal")] * 2
        self.genotype["birth_gene"]        = [self.traits.get("birth", "single")] * 2

    def _breed(self, other, world):
        super()._breed(other, world)
        # Twin gene: when expressed, 60% chance of a second lamb
        offspring = next(
            (e for e in reversed(world.entities)
             if getattr(e, 'parent_a_uid', None) == self.uid and not e.dead),
            None
        )
        if offspring and offspring.traits.get("birth") == "twin" and random.random() < 0.6:
            twin = Sheep((self.x + other.x) / 2, (self.y + other.y) / 2, world)
            twin._inherit_genotype(self, other)
            cs_a = self.traits["color_shift"]
            cs_b = other.traits["color_shift"]
            twin.traits["color_shift"] = tuple(
                max(-0.25, min(0.25, (cs_a[i] + cs_b[i]) / 2 + random.uniform(-0.03, 0.03)))
                for i in range(3)
            )
            twin.parent_a_uid = self.uid
            twin.parent_b_uid = other.uid
            twin.tamed = self.tamed and other.tamed
            twin._breed_cooldown = 600.0
            world.entities.append(twin)

    def update(self, dt):
        super().update(dt)
        if self.dead:
            return
        if not self.has_wool:
            self._regrow_timer -= dt
            if self._regrow_timer <= 0:
                self.has_wool = True
        if self.traits.get("sex", "female") == "female" and not self.has_milk:
            self._milk_refill_timer -= dt
            if self._milk_refill_timer <= 0:
                self.has_milk = True
        if not self.has_manure:
            self._manure_timer -= dt
            if self._manure_timer <= 0:
                self.has_manure = True

    def collect_manure(self):
        if not self.has_manure:
            return None
        self.has_manure = False
        self._manure_timer = self.MANURE_TIMER
        return [(self._MANURE_ITEM, 1)]

    def _try_harvest_resource(self, player, dt):
        tool = player.hotbar[player.selected_slot]
        if tool == "shears":
            if not self.has_wool:
                self.reset_harvest()
                return None
            self._harvest_time += dt
            self.being_harvested = True
            if self._harvest_time >= self.HARVEST_TIME:
                self.reset_harvest()
                self.has_wool = False
                regrow_rate = self.traits.get("regrow_rate", 1.0)
                self._regrow_timer = self.REGROW_TIME / max(0.3, regrow_rate)
                weight = self.traits.get("fleece_weight",
                         self.traits.get("fleece",
                         self.traits.get("productivity", 1.0)))
                mut   = self.traits.get("mutation")
                count = max(0, round(weight * self._yield_mult()))
                if mut == "giant":
                    count += 1
                drops = [("wool", count)] if count > 0 else []
                if mut == "golden":
                    drops.append(("golden_wool", 1))
                return self._finalize_drops(drops, "wool")
        elif tool == "bucket":
            if not self.has_milk:
                self.reset_harvest()
                return None
            self._harvest_time += dt
            self.being_harvested = True
            if self._harvest_time >= self.HARVEST_TIME:
                self.reset_harvest()
                self.has_milk = False
                self._milk_refill_timer = self.MILK_REFILL_TIME
                prod = self.traits.get("milk_yield",
                       self.traits.get("productivity", 1.0))
                mut  = self.traits.get("mutation")
                count = max(0, round(prod * self._yield_mult()))
                if mut == "giant":
                    count += 1
                drops = [("sheep_milk", count)] if count > 0 else []
                if mut == "golden":
                    drops.append(("golden_milk", 1))
                return self._finalize_drops(drops, "sheep_milk")
        else:
            self.reset_harvest()
        return None


class Llama(Animal):
    ANIMAL_W = 26
    ANIMAL_H = 28
    HARVEST_TIME = 1.8
    REGROW_TIME  = 45.0
    MANURE_TIMER = 110.0
    _MANURE_ITEM = "sheep_droppings"
    MEAT_DROP = ("raw_mutton", 2)
    PREFERRED_FOODS = ("wheat", "carrot", "apple")
    NATIVE_BIOMES = {"alpine_mountain", "arid_steppe", "rolling_hills"}

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "llama")
        self.has_wool = True
        self._regrow_timer = 0.0
        self.has_manure = False
        self._manure_timer = self.MANURE_TIMER

        bx = int(float(x) // BLOCK_SIZE)
        biodome = world.biodome_at(bx) if world is not None else "rocky_mountain"
        eligible = LLAMA_BIOME_MAP.get(biodome, list(LLAMA_BREED_PROFILES.keys()))
        breed = random.choice(eligible) if eligible else "Classic Llama"
        self.traits["breed"] = breed

        profile = LLAMA_BREED_PROFILES.get(breed, LLAMA_BREED_PROFILES["Classic Llama"])
        self._init_llama_genotype(profile)

    def _init_llama_genotype(self, profile=None):
        if profile is None:
            breed = self.traits.get("breed", "Classic Llama")
            profile = LLAMA_BREED_PROFILES.get(breed, LLAMA_BREED_PROFILES["Classic Llama"])

        for gene_key, (lo, hi) in profile["genes"].items():
            self.genotype[gene_key] = [
                round(random.uniform(lo, hi), 3),
                round(random.uniform(lo, hi), 3),
            ]

        cw = profile["color_weights"]
        self.genotype["coat_color_gene"] = [
            random.choices(LLAMA_COLOR_ORDER, weights=cw)[0],
            random.choices(LLAMA_COLOR_ORDER, weights=cw)[0],
        ]
        pw = profile["pattern_weights"]
        self.genotype["coat_pattern_gene"] = [
            random.choices(LLAMA_PATTERN_ORDER, weights=pw)[0],
            random.choices(LLAMA_PATTERN_ORDER, weights=pw)[0],
        ]
        ew = profile["ear_weights"]
        self.genotype["ear_type_gene"] = [
            random.choices(LLAMA_EAR_ORDER, weights=ew)[0],
            random.choices(LLAMA_EAR_ORDER, weights=ew)[0],
        ]
        self.genotype["birth_gene"] = ["single", "single"]
        self._apply_genotype_to_traits()
        self.health = max(2, round(self.traits.get("constitution", 1.0) * 3))

    def _apply_genotype_to_traits(self):
        super()._apply_genotype_to_traits()
        for gene, trait, lo, hi in [
            ("fleece_weight_gene",  "fleece_weight",  0.5, 3.5),
            ("fiber_fineness_gene", "fiber_fineness", 0.7, 1.5),
            ("fiber_length_gene",   "fiber_length",   0.0, 1.0),
            ("regrow_rate_gene",    "regrow_rate",    0.5, 2.0),
            ("constitution_gene",   "constitution",   0.7, 1.3),
        ]:
            if gene in self.genotype:
                avg = sum(self.genotype[gene]) / 2
                self.traits[trait] = round(max(lo, min(hi, avg)), 3)
        for gene, trait, order in [
            ("coat_color_gene",   "coat_color",   LLAMA_COLOR_ORDER),
            ("coat_pattern_gene", "coat_pattern", LLAMA_PATTERN_ORDER),
            ("ear_type_gene",     "ear_type",     LLAMA_EAR_ORDER),
            ("birth_gene",        "birth",        BIRTH_ORDER),
        ]:
            if gene in self.genotype:
                self.traits[trait] = _expressed_categorical(self.genotype[gene], order)

    def _synthesize_genotype_from_traits(self):
        super()._synthesize_genotype_from_traits()
        for gene, trait, lo, hi in [
            ("fleece_weight_gene",  "fleece_weight",  0.5, 3.5),
            ("fiber_fineness_gene", "fiber_fineness", 0.7, 1.5),
            ("fiber_length_gene",   "fiber_length",   0.0, 1.0),
            ("regrow_rate_gene",    "regrow_rate",    0.5, 2.0),
            ("constitution_gene",   "constitution",   0.7, 1.3),
        ]:
            v = self.traits.get(trait, (lo + hi) / 2)
            n = random.uniform(-0.03, 0.03)
            self.genotype[gene] = [round(max(lo, min(hi, v + n)), 3), round(max(lo, min(hi, v - n)), 3)]
        self.genotype["coat_color_gene"]   = [self.traits.get("coat_color", "fawn")] * 2
        self.genotype["coat_pattern_gene"] = [self.traits.get("coat_pattern", "solid")] * 2
        self.genotype["ear_type_gene"]     = [self.traits.get("ear_type", "banana")] * 2
        self.genotype["birth_gene"]        = [self.traits.get("birth", "single")] * 2

    def update(self, dt):
        super().update(dt)
        if self.dead:
            return
        if not self.has_wool:
            self._regrow_timer -= dt
            if self._regrow_timer <= 0:
                self.has_wool = True
        if not self.has_manure:
            self._manure_timer -= dt
            if self._manure_timer <= 0:
                self.has_manure = True

    def collect_manure(self):
        if not self.has_manure:
            return None
        self.has_manure = False
        self._manure_timer = self.MANURE_TIMER
        return [(self._MANURE_ITEM, 1)]

    def try_feed(self, player):
        was_tamed = self.tamed
        ok = super().try_feed(player)
        if ok and not was_tamed and self.tamed:
            _record_llama_tame(self, player)
        return ok

    def _breed(self, other, world):
        was_count = len(world.entities)
        super()._breed(other, world)
        player = getattr(world, "_player_ref", None)
        if player is None or len(world.entities) <= was_count:
            return
        offspring = world.entities[-1]
        if isinstance(offspring, Llama) and self.tamed and other.tamed:
            player.llamas_bred = getattr(player, "llamas_bred", 0) + 1
            _record_llama_stats(offspring, player)

    def _try_harvest_resource(self, player, dt):
        tool = player.hotbar[player.selected_slot]
        if tool != "shears":
            self.reset_harvest()
            return None
        if not self.has_wool:
            self.reset_harvest()
            return None
        self._harvest_time += dt
        self.being_harvested = True
        if self._harvest_time >= self.HARVEST_TIME:
            self.reset_harvest()
            self.has_wool = False
            regrow_rate = self.traits.get("regrow_rate", 1.0)
            self._regrow_timer = self.REGROW_TIME / max(0.3, regrow_rate)
            weight   = self.traits.get("fleece_weight", 1.5)
            fineness = self.traits.get("fiber_fineness", 1.0)
            length   = self.traits.get("fiber_length", 0.5)
            mut = self.traits.get("mutation")
            count = max(0, round(weight * (0.8 + 0.4 * length) * self._yield_mult()))
            if mut == "giant":
                count += 1
            if fineness >= 1.25 and random.random() < (fineness - 1.0):
                count += 1
            drops = [("wool", count)] if count > 0 else []
            if mut == "golden":
                drops.append(("golden_wool", 1))
            return self._finalize_drops(drops, "wool")
        return None


def _record_llama_stats(llama, player):
    records = getattr(player, "llama_records", {})
    fw = llama.traits.get("fleece_weight", 0.0)
    ff = llama.traits.get("fiber_fineness", 0.0)
    if fw > records.get("best_fleece", 0.0):
        records["best_fleece"] = fw
    if ff > records.get("best_fineness", 0.0):
        records["best_fineness"] = ff
    player.llama_records = records


def _record_llama_tame(llama, player):
    player.llamas_tamed = getattr(player, "llamas_tamed", 0) + 1
    breed = llama.traits.get("breed", "Classic Llama")
    breeds = getattr(player, "discovered_llama_breeds", set())
    breeds.add(breed)
    player.discovered_llama_breeds = breeds
    biodome = llama.world.biodome_at(int(llama.x // BLOCK_SIZE)) if llama.world else "rocky_mountain"
    biomes = getattr(player, "discovered_llama_biomes", set())
    biomes.add(biodome)
    player.discovered_llama_biomes = biomes
    _record_llama_stats(llama, player)


class Yak(Animal):
    ANIMAL_W = 34
    ANIMAL_H = 26
    HARVEST_TIME = 1.8
    REGROW_TIME      = 60.0
    MILK_REFILL_TIME = 30.0
    MANURE_TIMER     = 100.0
    _MANURE_ITEM = "cow_manure"
    MEAT_DROP = ("raw_beef", 3)
    NATIVE_BIOMES = {"tundra", "alpine_mountain", "boreal"}
    PREFERRED_FOODS = ("wheat", "carrot", "apple")

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "yak")
        self.has_wool = True
        self._regrow_timer = 0.0
        self._milk_refill_timer = 0.0
        self.has_manure = False
        self._manure_timer = self.MANURE_TIMER

        bx = int(float(x) // BLOCK_SIZE)
        biodome = world.biodome_at(bx) if world is not None else "alpine_mountain"
        eligible = YAK_BIOME_MAP.get(biodome, list(YAK_BREED_PROFILES.keys()))
        breed = random.choice(eligible) if eligible else "Domestic Yak"
        self.traits["breed"] = breed

        # Only females produce milk
        self.has_milk = (self.traits["sex"] == "female")

        profile = YAK_BREED_PROFILES.get(breed, YAK_BREED_PROFILES["Domestic Yak"])
        self._init_yak_genotype(profile)

    def _init_yak_genotype(self, profile=None):
        if profile is None:
            breed = self.traits.get("breed", "Domestic Yak")
            profile = YAK_BREED_PROFILES.get(breed, YAK_BREED_PROFILES["Domestic Yak"])

        for gene_key, (lo, hi) in profile["genes"].items():
            self.genotype[gene_key] = [
                round(random.uniform(lo, hi), 3),
                round(random.uniform(lo, hi), 3),
            ]

        cw = profile["color_weights"]
        self.genotype["coat_color_gene"] = [
            random.choices(YAK_COLOR_ORDER, weights=cw)[0],
            random.choices(YAK_COLOR_ORDER, weights=cw)[0],
        ]
        hw = profile["horn_weights"]
        self.genotype["horn_type_gene"] = [
            random.choices(YAK_HORN_ORDER, weights=hw)[0],
            random.choices(YAK_HORN_ORDER, weights=hw)[0],
        ]
        sw = profile["skirt_weights"]
        self.genotype["skirt_length_gene"] = [
            random.choices(YAK_SKIRT_ORDER, weights=sw)[0],
            random.choices(YAK_SKIRT_ORDER, weights=sw)[0],
        ]
        self._apply_genotype_to_traits()
        self.health = max(3, round(self.traits.get("constitution", 1.0) * 4))

    def _apply_genotype_to_traits(self):
        super()._apply_genotype_to_traits()
        for gene, trait, lo, hi in [
            ("milk_volume_gene",   "milk_volume",   0.5, 2.5),
            ("milk_richness_gene", "milk_richness", 0.9, 1.6),
            ("fleece_weight_gene", "fleece_weight", 0.5, 3.0),
            ("fiber_length_gene",  "fiber_length",  0.0, 1.0),
            ("regrow_rate_gene",   "regrow_rate",   0.5, 2.0),
            ("constitution_gene",  "constitution",  0.7, 1.5),
        ]:
            if gene in self.genotype:
                avg = sum(self.genotype[gene]) / 2
                self.traits[trait] = round(max(lo, min(hi, avg)), 3)
        for gene, trait, order in [
            ("coat_color_gene",    "coat_color",   YAK_COLOR_ORDER),
            ("horn_type_gene",     "horn_type",    YAK_HORN_ORDER),
            ("skirt_length_gene",  "skirt_length", YAK_SKIRT_ORDER),
        ]:
            if gene in self.genotype:
                self.traits[trait] = _expressed_categorical(self.genotype[gene], order)

    def _synthesize_genotype_from_traits(self):
        super()._synthesize_genotype_from_traits()
        for gene, trait, lo, hi in [
            ("milk_volume_gene",   "milk_volume",   0.5, 2.5),
            ("milk_richness_gene", "milk_richness", 0.9, 1.6),
            ("fleece_weight_gene", "fleece_weight", 0.5, 3.0),
            ("fiber_length_gene",  "fiber_length",  0.0, 1.0),
            ("regrow_rate_gene",   "regrow_rate",   0.5, 2.0),
            ("constitution_gene",  "constitution",  0.7, 1.5),
        ]:
            v = self.traits.get(trait, (lo + hi) / 2)
            n = random.uniform(-0.03, 0.03)
            self.genotype[gene] = [round(max(lo, min(hi, v + n)), 3), round(max(lo, min(hi, v - n)), 3)]
        self.genotype["coat_color_gene"]   = [self.traits.get("coat_color", "black")] * 2
        self.genotype["horn_type_gene"]    = [self.traits.get("horn_type", "wide")] * 2
        self.genotype["skirt_length_gene"] = [self.traits.get("skirt_length", "full")] * 2

    def update(self, dt):
        super().update(dt)
        if self.dead:
            return
        if not self.has_wool:
            self._regrow_timer -= dt
            if self._regrow_timer <= 0:
                self.has_wool = True
        if self.traits.get("sex", "female") == "female" and not self.has_milk:
            self._milk_refill_timer -= dt
            if self._milk_refill_timer <= 0:
                self.has_milk = True
        if not self.has_manure:
            self._manure_timer -= dt
            if self._manure_timer <= 0:
                self.has_manure = True

    def collect_manure(self):
        if not self.has_manure:
            return None
        self.has_manure = False
        self._manure_timer = self.MANURE_TIMER
        return [(self._MANURE_ITEM, 1)]

    def try_feed(self, player):
        was_tamed = self.tamed
        ok = super().try_feed(player)
        if ok and not was_tamed and self.tamed:
            _record_yak_tame(self, player)
        return ok

    def _breed(self, other, world):
        was_count = len(world.entities)
        super()._breed(other, world)
        player = getattr(world, "_player_ref", None)
        if player is None or len(world.entities) <= was_count:
            return
        offspring = world.entities[-1]
        if isinstance(offspring, Yak) and self.tamed and other.tamed:
            player.yaks_bred = getattr(player, "yaks_bred", 0) + 1
            _record_yak_stats(offspring, player)

    def _try_harvest_resource(self, player, dt):
        tool = player.hotbar[player.selected_slot]
        if tool == "shears":
            if not self.has_wool:
                self.reset_harvest()
                return None
            self._harvest_time += dt
            self.being_harvested = True
            if self._harvest_time >= self.HARVEST_TIME:
                self.reset_harvest()
                self.has_wool = False
                regrow_rate = self.traits.get("regrow_rate", 1.0)
                self._regrow_timer = self.REGROW_TIME / max(0.3, regrow_rate)
                weight = self.traits.get("fleece_weight", 1.5)
                length = self.traits.get("fiber_length", 0.6)
                mut = self.traits.get("mutation")
                count = max(0, round(weight * (0.9 + 0.5 * length) * self._yield_mult()))
                if mut == "giant":
                    count += 1
                drops = [("wool", count)] if count > 0 else []
                if mut == "golden":
                    drops.append(("golden_wool", 1))
                return self._finalize_drops(drops, "wool")
        elif tool == "bucket":
            if not self.has_milk:
                self.reset_harvest()
                return None
            self._harvest_time += dt
            self.being_harvested = True
            if self._harvest_time >= self.HARVEST_TIME:
                self.reset_harvest()
                self.has_milk = False
                self._milk_refill_timer = self.MILK_REFILL_TIME
                volume = self.traits.get("milk_volume", 1.2)
                richness = self.traits.get("milk_richness", 1.2)
                mut = self.traits.get("mutation")
                count = max(0, round(volume * richness * self._yield_mult()))
                if mut == "giant":
                    count += 1
                drops = [("milk", count)] if count > 0 else []
                if mut == "golden":
                    drops.append(("golden_milk", 1))
                return self._finalize_drops(drops, "milk")
        else:
            self.reset_harvest()
        return None


def _record_yak_stats(yak, player):
    records = getattr(player, "yak_records", {})
    fw = yak.traits.get("fleece_weight", 0.0)
    mv = yak.traits.get("milk_volume", 0.0)
    mr = yak.traits.get("milk_richness", 0.0)
    if fw > records.get("best_fleece", 0.0):
        records["best_fleece"] = fw
    if mv > records.get("best_milk", 0.0):
        records["best_milk"] = mv
    if mr > records.get("best_richness", 0.0):
        records["best_richness"] = mr
    player.yak_records = records


def _record_yak_tame(yak, player):
    player.yaks_tamed = getattr(player, "yaks_tamed", 0) + 1
    breed = yak.traits.get("breed", "Domestic Yak")
    breeds = getattr(player, "discovered_yak_breeds", set())
    breeds.add(breed)
    player.discovered_yak_breeds = breeds
    biodome = yak.world.biodome_at(int(yak.x // BLOCK_SIZE)) if yak.world else "alpine_mountain"
    biomes = getattr(player, "discovered_yak_biomes", set())
    biomes.add(biodome)
    player.discovered_yak_biomes = biomes
    _record_yak_stats(yak, player)


# ── Pig orderings ────────────────────────────────────────────────────
PIG_COLOR_ORDER   = ["pink", "black", "red", "white", "spotted", "blonde"]
PIG_PATTERN_ORDER = ["solid", "belted", "spotted", "piebald"]
PIG_EAR_ORDER     = ["upright", "lop", "semi_lop"]
PIG_SNOUT_ORDER   = ["short", "medium", "long"]


# Pig — omnivorous farm animal. Meat + manure + lard from fat.
# meat_yield_gene:  pork count multiplier (0.7–1.5)
# fat_gene:         extra lard chance + visual girth (0.5–1.5)
# growth_rate_gene: speeds breeding cooldown (0.7–1.3)
# litter_size_gene: extra offspring per breed when high (0.8–1.6)
# constitution_gene: starting health multiplier (0.7–1.4)
PIG_BREED_PROFILES = {
    # ── Berkshire — black, white socks/snout, premium meat ─────────────
    "Berkshire": {
        "biomes": {"temperate", "birch_forest", "rolling_hills"},
        "genes": {
            "meat_yield_gene":  (1.0, 1.3), "fat_gene":         (0.9, 1.3),
            "growth_rate_gene": (0.8, 1.1), "litter_size_gene": (0.9, 1.2),
            "constitution_gene":(0.9, 1.2),
        },
        "color_weights":   [ 0, 80,  0,  0,  5, 15],
        "pattern_weights": [25,  0, 15, 60],
        "ear_weights":     [70, 10, 20],
        "snout_weights":   [40, 50, 10],
    },
    # ── Tamworth — long ginger forager, narrow body ─────────────────────
    "Tamworth": {
        "biomes": {"birch_forest", "boreal", "temperate"},
        "genes": {
            "meat_yield_gene":  (0.8, 1.1), "fat_gene":         (0.5, 0.9),
            "growth_rate_gene": (0.9, 1.2), "litter_size_gene": (1.0, 1.4),
            "constitution_gene":(1.0, 1.3),
        },
        "color_weights":   [ 0,  0, 85,  0,  5, 10],
        "pattern_weights": [90,  0,  5,  5],
        "ear_weights":     [85,  5, 10],
        "snout_weights":   [10, 35, 55],
    },
    # ── Large White — pink, big, productive lowland breed ───────────────
    "Large White": {
        "biomes": {"temperate", "rolling_hills", "savanna"},
        "genes": {
            "meat_yield_gene":  (1.1, 1.5), "fat_gene":         (0.7, 1.1),
            "growth_rate_gene": (1.0, 1.3), "litter_size_gene": (1.1, 1.6),
            "constitution_gene":(0.9, 1.2),
        },
        "color_weights":   [70,  0,  0, 25,  3,  2],
        "pattern_weights": [92,  0,  4,  4],
        "ear_weights":     [80, 10, 10],
        "snout_weights":   [25, 60, 15],
    },
    # ── Duroc — red, fast-growing meat hog ──────────────────────────────
    "Duroc": {
        "biomes": {"temperate", "savanna", "rolling_hills"},
        "genes": {
            "meat_yield_gene":  (1.1, 1.4), "fat_gene":         (0.8, 1.2),
            "growth_rate_gene": (1.1, 1.3), "litter_size_gene": (1.0, 1.3),
            "constitution_gene":(1.0, 1.2),
        },
        "color_weights":   [ 0,  5, 80,  0,  5, 10],
        "pattern_weights": [88,  0,  6,  6],
        "ear_weights":     [10, 65, 25],
        "snout_weights":   [30, 60, 10],
    },
    # ── Hampshire — black with white belt ───────────────────────────────
    "Hampshire": {
        "biomes": {"rolling_hills", "temperate", "birch_forest"},
        "genes": {
            "meat_yield_gene":  (1.0, 1.3), "fat_gene":         (0.7, 1.0),
            "growth_rate_gene": (1.0, 1.2), "litter_size_gene": (0.9, 1.2),
            "constitution_gene":(1.0, 1.2),
        },
        "color_weights":   [ 0, 75,  0,  0,  5, 20],
        "pattern_weights": [ 5, 85,  5,  5],
        "ear_weights":     [80, 10, 10],
        "snout_weights":   [30, 55, 15],
    },
    # ── Mangalitsa — shaggy curly-coated lard pig, cold-hardy ──────────
    "Mangalitsa": {
        "biomes": {"alpine_mountain", "boreal", "tundra"},
        "genes": {
            "meat_yield_gene":  (0.8, 1.1), "fat_gene":         (1.2, 1.5),
            "growth_rate_gene": (0.7, 0.9), "litter_size_gene": (0.8, 1.1),
            "constitution_gene":(1.1, 1.4),
        },
        "color_weights":   [ 5, 10,  5, 10,  5, 65],
        "pattern_weights": [80,  0, 10, 10],
        "ear_weights":     [25, 55, 20],
        "snout_weights":   [15, 55, 30],
    },
    # ── Gloucestershire Old Spots — white orchard pig with black spots ─
    "Gloucestershire Old Spots": {
        "biomes": {"temperate", "rolling_hills", "birch_forest"},
        "genes": {
            "meat_yield_gene":  (0.9, 1.2), "fat_gene":         (1.0, 1.3),
            "growth_rate_gene": (0.8, 1.0), "litter_size_gene": (1.0, 1.3),
            "constitution_gene":(1.0, 1.3),
        },
        "color_weights":   [10,  0,  0, 50, 40,  0],
        "pattern_weights": [10,  0, 80, 10],
        "ear_weights":     [ 0, 75, 25],
        "snout_weights":   [20, 60, 20],
    },
    # ── Kunekune — small, friendly grazer, very tame ────────────────────
    "Kunekune": {
        "biomes": {"temperate", "rolling_hills", "savanna"},
        "genes": {
            "meat_yield_gene":  (0.6, 0.9), "fat_gene":         (1.1, 1.4),
            "growth_rate_gene": (0.7, 0.9), "litter_size_gene": (0.8, 1.1),
            "constitution_gene":(1.1, 1.3),
        },
        "color_weights":   [20, 25, 10, 15, 25,  5],
        "pattern_weights": [40,  5, 25, 30],
        "ear_weights":     [40, 25, 35],
        "snout_weights":   [80, 18,  2],
    },
    # ── Iberian — black premium ham pig, oak-fed savanna forager ───────
    "Iberian": {
        "biomes": {"savanna", "temperate", "rolling_hills"},
        "genes": {
            "meat_yield_gene":  (1.0, 1.3), "fat_gene":         (1.3, 1.5),
            "growth_rate_gene": (0.7, 0.9), "litter_size_gene": (0.8, 1.0),
            "constitution_gene":(1.1, 1.3),
        },
        "color_weights":   [ 0, 85,  3,  0,  2, 10],
        "pattern_weights": [88,  0,  6,  6],
        "ear_weights":     [10, 70, 20],
        "snout_weights":   [ 5, 35, 60],
    },
    # ── Vietnamese Pot-Belly — miniature, black, low-slung ──────────────
    "Vietnamese Pot-Belly": {
        "biomes": {"temperate", "savanna", "rolling_hills"},
        "genes": {
            "meat_yield_gene":  (0.5, 0.8), "fat_gene":         (1.2, 1.5),
            "growth_rate_gene": (0.9, 1.1), "litter_size_gene": (1.0, 1.3),
            "constitution_gene":(1.0, 1.2),
        },
        "color_weights":   [ 5, 75,  0,  5, 10,  5],
        "pattern_weights": [70,  0, 15, 15],
        "ear_weights":     [80,  5, 15],
        "snout_weights":   [85, 12,  3],
    },
    # ── Meishan — wrinkled Chinese breed, enormous litters ──────────────
    "Meishan": {
        "biomes": {"temperate", "rolling_hills", "savanna"},
        "genes": {
            "meat_yield_gene":  (0.8, 1.1), "fat_gene":         (1.1, 1.4),
            "growth_rate_gene": (0.8, 1.0), "litter_size_gene": (1.4, 1.7),
            "constitution_gene":(1.0, 1.2),
        },
        "color_weights":   [ 5, 80,  0,  3,  7,  5],
        "pattern_weights": [85,  0,  8,  7],
        "ear_weights":     [ 5, 85, 10],
        "snout_weights":   [30, 55, 15],
    },
    # ── Pietrain — lean spotted European meat hog ───────────────────────
    "Pietrain": {
        "biomes": {"temperate", "rolling_hills", "birch_forest"},
        "genes": {
            "meat_yield_gene":  (1.2, 1.5), "fat_gene":         (0.5, 0.8),
            "growth_rate_gene": (1.0, 1.2), "litter_size_gene": (1.0, 1.3),
            "constitution_gene":(0.9, 1.1),
        },
        "color_weights":   [25,  5,  0, 35, 35,  0],
        "pattern_weights": [ 5,  0, 80, 15],
        "ear_weights":     [70, 15, 15],
        "snout_weights":   [30, 60, 10],
    },
    # ── Hereford — red body, white face & socks (US heritage) ───────────
    "Hereford": {
        "biomes": {"rolling_hills", "temperate", "savanna"},
        "genes": {
            "meat_yield_gene":  (1.0, 1.3), "fat_gene":         (0.9, 1.2),
            "growth_rate_gene": (0.9, 1.1), "litter_size_gene": (1.0, 1.3),
            "constitution_gene":(1.0, 1.3),
        },
        "color_weights":   [ 5,  0, 70,  5, 15,  5],
        "pattern_weights": [ 5, 10, 10, 75],
        "ear_weights":     [25, 55, 20],
        "snout_weights":   [25, 60, 15],
    },
    # ── Large Black — all-black lop-eared forager (British) ─────────────
    "Large Black": {
        "biomes": {"birch_forest", "boreal", "temperate", "rolling_hills"},
        "genes": {
            "meat_yield_gene":  (1.0, 1.3), "fat_gene":         (1.0, 1.3),
            "growth_rate_gene": (0.8, 1.0), "litter_size_gene": (1.1, 1.4),
            "constitution_gene":(1.1, 1.3),
        },
        "color_weights":   [ 0, 90,  0,  0,  3,  7],
        "pattern_weights": [92,  0,  4,  4],
        "ear_weights":     [ 0, 90, 10],
        "snout_weights":   [15, 55, 30],
    },
    # ── Red Wattle — large calm red pig with neck wattles ───────────────
    "Red Wattle": {
        "biomes": {"savanna", "temperate", "rolling_hills"},
        "genes": {
            "meat_yield_gene":  (1.1, 1.4), "fat_gene":         (0.8, 1.1),
            "growth_rate_gene": (1.0, 1.2), "litter_size_gene": (1.1, 1.4),
            "constitution_gene":(1.0, 1.2),
        },
        "color_weights":   [ 0,  3, 88,  0,  4,  5],
        "pattern_weights": [90,  0,  5,  5],
        "ear_weights":     [25, 40, 35],
        "snout_weights":   [20, 60, 20],
    },
    # ── Oxford Sandy & Black — sandy blonde with black blotches ─────────
    "Oxford Sandy & Black": {
        "biomes": {"temperate", "rolling_hills", "birch_forest"},
        "genes": {
            "meat_yield_gene":  (0.9, 1.2), "fat_gene":         (0.9, 1.2),
            "growth_rate_gene": (0.8, 1.0), "litter_size_gene": (1.0, 1.3),
            "constitution_gene":(1.0, 1.2),
        },
        "color_weights":   [ 5,  5,  5,  0,  5, 80],
        "pattern_weights": [ 5,  0, 20, 75],
        "ear_weights":     [20, 50, 30],
        "snout_weights":   [25, 60, 15],
    },
    # ── Saddleback — British belted heritage breed ──────────────────────
    "Saddleback": {
        "biomes": {"temperate", "rolling_hills", "birch_forest"},
        "genes": {
            "meat_yield_gene":  (1.0, 1.3), "fat_gene":         (0.9, 1.2),
            "growth_rate_gene": (0.9, 1.1), "litter_size_gene": (1.1, 1.4),
            "constitution_gene":(1.0, 1.3),
        },
        "color_weights":   [ 0, 80,  0,  0,  5, 15],
        "pattern_weights": [ 5, 88,  4,  3],
        "ear_weights":     [ 5, 80, 15],
        "snout_weights":   [20, 60, 20],
    },
    # ── Ossabaw Island — small feral hardy pig, variable colors ─────────
    "Ossabaw Island": {
        "biomes": {"savanna", "birch_forest", "boreal", "temperate"},
        "genes": {
            "meat_yield_gene":  (0.6, 0.9), "fat_gene":         (1.2, 1.5),
            "growth_rate_gene": (0.7, 0.9), "litter_size_gene": (0.9, 1.2),
            "constitution_gene":(1.2, 1.4),
        },
        "color_weights":   [10, 30, 15,  5, 25, 15],
        "pattern_weights": [35,  5, 30, 30],
        "ear_weights":     [55, 20, 25],
        "snout_weights":   [10, 40, 50],
    },
}

PIG_BIOME_MAP: dict = {}
for _pig_breed, _pig_profile in PIG_BREED_PROFILES.items():
    for _pig_biome in _pig_profile["biomes"]:
        PIG_BIOME_MAP.setdefault(_pig_biome, []).append(_pig_breed)


class Goat(Animal):
    ANIMAL_W = 22
    ANIMAL_H = 18
    HARVEST_TOOL = "bucket"
    HARVEST_TIME = 1.5
    REFILL_TIME  = 25.0
    MANURE_TIMER = 90.0
    _MANURE_ITEM = "goat_droppings"
    MEAT_DROP    = ("raw_mutton", 1)
    NATIVE_BIOMES = {"alpine_mountain", "tundra", "arid_steppe", "savanna", "rolling_hills"}
    PREFERRED_FOODS = ("wheat", "carrot")

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "goat")
        self._refill_timer = 0.0
        self.has_manure = False
        self._manure_timer = self.MANURE_TIMER

        bx = int(float(x) // BLOCK_SIZE)
        biodome = world.biodome_at(bx) if world is not None else "temperate"
        eligible = GOAT_BIOME_MAP.get(biodome, list(GOAT_BREED_PROFILES.keys()))
        breed = random.choice(eligible) if eligible else "Alpine"
        self.traits["breed"] = breed

        self.has_milk = (self.traits["sex"] == "female")

        profile = GOAT_BREED_PROFILES.get(breed, GOAT_BREED_PROFILES["Alpine"])
        self._init_goat_genotype(profile)

    def _init_goat_genotype(self, profile=None):
        if profile is None:
            breed = self.traits.get("breed", "Alpine")
            profile = GOAT_BREED_PROFILES.get(breed, GOAT_BREED_PROFILES["Alpine"])

        for gene_key, (lo, hi) in profile["genes"].items():
            self.genotype[gene_key] = [
                round(random.uniform(lo, hi), 3),
                round(random.uniform(lo, hi), 3),
            ]

        ccw = profile["coat_color_weights"]
        self.genotype["coat_color_gene"] = [
            random.choices(GOAT_COLOR_ORDER, weights=ccw)[0],
            random.choices(GOAT_COLOR_ORDER, weights=ccw)[0],
        ]
        for key, order, wkey in [
            ("coat_pattern_gene", GOAT_PATTERN_ORDER, "pattern_weights"),
            ("horn_type_gene",    GOAT_HORN_ORDER,    "horn_weights"),
            ("ear_type_gene",     GOAT_EAR_ORDER,     "ear_weights"),
            ("beard_gene",        GOAT_BEARD_ORDER,   "beard_weights"),
        ]:
            w = profile[wkey]
            self.genotype[key] = [
                random.choices(order, weights=w)[0],
                random.choices(order, weights=w)[0],
            ]

        self._apply_genotype_to_traits()
        self.health = max(2, round(self.traits.get("constitution", 1.0) * 3))

    def _apply_genotype_to_traits(self):
        super()._apply_genotype_to_traits()
        for gene, trait, lo, hi in [
            ("milk_volume_gene",   "milk_volume",   0.5, 2.5),
            ("milk_richness_gene", "milk_richness", 0.7, 1.3),
            ("refill_rate_gene",   "refill_rate",   0.5, 2.0),
            ("constitution_gene",  "constitution",  0.7, 1.3),
            ("fiber_gene",         "fiber",         0.0, 1.0),
        ]:
            if gene in self.genotype:
                avg = sum(self.genotype[gene]) / 2
                self.traits[trait] = round(max(lo, min(hi, avg)), 3)
        for gene, trait, order in [
            ("coat_color_gene",   "coat_color",   GOAT_COLOR_ORDER),
            ("coat_pattern_gene", "coat_pattern", GOAT_PATTERN_ORDER),
            ("horn_type_gene",    "horn_type",    GOAT_HORN_ORDER),
            ("ear_type_gene",     "ear_type",     GOAT_EAR_ORDER),
            ("beard_gene",        "beard",        GOAT_BEARD_ORDER),
        ]:
            if gene in self.genotype:
                self.traits[trait] = _expressed_categorical(self.genotype[gene], order)

    def _synthesize_genotype_from_traits(self):
        super()._synthesize_genotype_from_traits()
        for gene, trait, lo, hi in [
            ("milk_volume_gene",   "milk_volume",   0.5, 2.5),
            ("milk_richness_gene", "milk_richness", 0.7, 1.3),
            ("refill_rate_gene",   "refill_rate",   0.5, 2.0),
            ("constitution_gene",  "constitution",  0.7, 1.3),
            ("fiber_gene",         "fiber",         0.0, 1.0),
        ]:
            v = self.traits.get(trait, (lo + hi) / 2)
            n = random.uniform(-0.03, 0.03)
            self.genotype[gene] = [round(max(lo, min(hi, v + n)), 3), round(max(lo, min(hi, v - n)), 3)]
        self.genotype["coat_color_gene"]   = [self.traits.get("coat_color", "tan")] * 2
        self.genotype["coat_pattern_gene"] = [self.traits.get("coat_pattern", "solid")] * 2
        self.genotype["horn_type_gene"]    = [self.traits.get("horn_type", "curved")] * 2
        self.genotype["ear_type_gene"]     = [self.traits.get("ear_type", "upright")] * 2
        self.genotype["beard_gene"]        = [self.traits.get("beard", "small")] * 2

    def update(self, dt):
        super().update(dt)
        if self.dead:
            return
        if self.traits.get("sex", "female") == "female" and not self.has_milk:
            self._refill_timer -= dt
            if self._refill_timer <= 0:
                self.has_milk = True
        if not self.has_manure:
            self._manure_timer -= dt
            if self._manure_timer <= 0:
                self.has_manure = True

    def collect_manure(self):
        if not self.has_manure:
            return None
        self.has_manure = False
        self._manure_timer = self.MANURE_TIMER
        return [(self._MANURE_ITEM, 1)]

    def _try_harvest_resource(self, player, dt):
        if not self.has_milk:
            self.reset_harvest()
            return None
        tool = player.hotbar[player.selected_slot]
        if tool != self.HARVEST_TOOL:
            self.reset_harvest()
            return None
        self._harvest_time += dt
        self.being_harvested = True
        if self._harvest_time >= self.HARVEST_TIME:
            self.reset_harvest()
            self.has_milk = False
            refill_rate = self.traits.get("refill_rate", 1.0)
            self._refill_timer = self.REFILL_TIME / max(0.3, refill_rate)
            volume = self.traits.get("milk_volume",
                     self.traits.get("milk_richness",
                     self.traits.get("productivity", 1.0)))
            mut   = self.traits.get("mutation")
            count = max(0, round(volume * self._yield_mult()))
            if mut == "giant":
                count += 1
            drops = [("goat_milk", count)] if count > 0 else []
            if mut == "golden":
                drops.append(("golden_milk", 1))
            return self._finalize_drops(drops, "goat_milk")
        return None


class Cow(Animal):
    ANIMAL_W = 30
    ANIMAL_H = 20
    HARVEST_TOOL = "bucket"
    HARVEST_TIME = 1.5
    REFILL_TIME  = 20.0
    MANURE_TIMER = 90.0
    _MANURE_ITEM = "cow_manure"
    MEAT_DROP = ("raw_beef", 2)
    NATIVE_BIOMES = {"temperate", "rolling_hills", "savanna"}
    PREFERRED_FOODS = ("wheat", "apple")

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "cow")
        self.has_milk = True
        self._refill_timer = 0.0
        self.has_manure = False
        self._manure_timer = self.MANURE_TIMER

        bx = int(float(x) // BLOCK_SIZE)
        biodome = world.biodome_at(bx) if world is not None else "temperate"
        eligible = COW_BIOME_MAP.get(biodome, list(COW_BREED_PROFILES.keys()))
        breed = random.choice(eligible) if eligible else "Holstein"
        self.traits["breed"] = breed

        profile = COW_BREED_PROFILES.get(breed, COW_BREED_PROFILES["Holstein"])
        self._init_cow_genotype(profile)

        # Only females produce milk
        self.has_milk = (self.traits["sex"] == "female")
        self._milking = None   # mini-game state dict while active

    def _init_cow_genotype(self, profile=None):
        if profile is None:
            breed = self.traits.get("breed", "Holstein")
            profile = COW_BREED_PROFILES.get(breed, COW_BREED_PROFILES["Holstein"])

        for gene_key, (lo, hi) in profile["genes"].items():
            self.genotype[gene_key] = [
                round(random.uniform(lo, hi), 3),
                round(random.uniform(lo, hi), 3),
            ]

        hw = profile["hide_weights"]
        self.genotype["hide_gene"] = [
            random.choices(HIDE_ORDER, weights=hw)[0],
            random.choices(HIDE_ORDER, weights=hw)[0],
        ]
        self._apply_genotype_to_traits()
        self.traits["coat_color"] = random.choice(profile["coat_colors"])

    def _apply_genotype_to_traits(self):
        super()._apply_genotype_to_traits()
        for gene, trait, lo, hi in [
            ("milk_volume_gene",   "milk_volume",   0.5, 3.5),
            ("milk_richness_gene", "milk_richness", 0.7, 1.3),
            ("refill_rate_gene",   "refill_rate",   0.5, 2.0),
            ("beef_quality_gene",  "beef_quality",  0.7, 1.3),
            ("horn_length_gene",   "horn_length",   0.0, 1.0),
            ("hair_length_gene",   "hair_length",   0.0, 1.0),
        ]:
            if gene in self.genotype:
                avg = sum(self.genotype[gene]) / 2
                self.traits[trait] = round(max(lo, min(hi, avg)), 3)
        if "hide_gene" in self.genotype:
            self.traits["hide"] = _expressed_categorical(self.genotype["hide_gene"], HIDE_ORDER)

    def _synthesize_genotype_from_traits(self):
        super()._synthesize_genotype_from_traits()
        for gene, trait, lo, hi in [
            ("milk_volume_gene",   "milk_volume",   0.5, 3.5),
            ("milk_richness_gene", "milk_richness", 0.7, 1.3),
            ("refill_rate_gene",   "refill_rate",   0.5, 2.0),
            ("beef_quality_gene",  "beef_quality",  0.7, 1.3),
            ("horn_length_gene",   "horn_length",   0.0, 1.0),
            ("hair_length_gene",   "hair_length",   0.0, 1.0),
        ]:
            v = self.traits.get(trait, (lo + hi) / 2)
            n = random.uniform(-0.03, 0.03)
            self.genotype[gene] = [round(max(lo, min(hi, v + n)), 3), round(max(lo, min(hi, v - n)), 3)]
        self.genotype["hide_gene"] = [self.traits.get("hide", "solid")] * 2

    # ------------------------------------------------------------------
    # Milking mini-game
    # ------------------------------------------------------------------

    def start_milking(self, player):
        volume = self.traits.get("milk_volume", 1.0)
        # Faster-refilling breeds have a slightly tighter pull window
        window = max(0.7, 1.8 - self.traits.get("refill_rate", 1.0) * 0.25)
        self._milking = {
            "teat":   0,       # which of 4 teats is currently extended
            "timer":  0.0,     # time current teat has been open
            "window": window,  # seconds before teat retracts (= miss)
            "phase":  "open",  # "open" | "hit" | "miss"
            "flash":  0.0,     # brief feedback timer
            "hits":   0,
            "player": player,
            "volume": volume,
        }
        self.being_harvested = True

    def handle_milking_press(self):
        m = self._milking
        if m is None or m["phase"] != "open":
            return
        m["phase"] = "hit"
        m["flash"] = 0.28
        m["hits"] += 1

    def _advance_milking_teat(self):
        m = self._milking
        if m["teat"] >= 3:
            self._finish_milking()
        else:
            m["teat"] += 1
            m["timer"] = 0.0
            m["phase"] = "open"

    def _finish_milking(self):
        m = self._milking
        self._milking = None
        self.being_harvested = False
        self.has_milk = False
        refill_rate = self.traits.get("refill_rate", 1.0)
        self._refill_timer = self.REFILL_TIME / max(0.3, refill_rate)

        hits   = m["hits"]
        volume = m["volume"]
        mut    = self.traits.get("mutation")

        if hits == 0:
            return

        count = max(0, round(volume * hits / 4 * self._yield_mult()))
        if mut == "giant":
            count += 1
        drops = [("milk", count)] if count > 0 else []
        if mut == "golden":
            drops.append(("golden_milk", 1))
        prem = self._premium_drop("milk") if drops else None
        if prem:
            drops.append((prem, 1))
        if not drops:
            return

        player = m["player"]
        player._consume_tool_use()
        for item_id, qty in drops:
            for _ in range(qty):
                player._add_item(item_id)
        if hasattr(player, "_on_milk_harvested"):
            player._on_milk_harvested(self, drops)

    def update(self, dt):
        super().update(dt)
        if self.dead:
            return
        # Advance milking mini-game
        m = self._milking
        if m is not None:
            if m["phase"] in ("hit", "miss"):
                m["flash"] -= dt
                if m["flash"] <= 0:
                    self._advance_milking_teat()
            else:  # "open"
                m["timer"] += dt
                if m["timer"] >= m["window"]:
                    m["phase"] = "miss"
                    m["flash"] = 0.28
        if self.traits.get("sex", "female") == "female" and not self.has_milk:
            self._refill_timer -= dt
            if self._refill_timer <= 0:
                self.has_milk = True
        if not self.has_manure:
            self._manure_timer -= dt
            if self._manure_timer <= 0:
                self.has_manure = True

    def collect_manure(self):
        if not self.has_manure:
            return None
        self.has_manure = False
        self._manure_timer = self.MANURE_TIMER
        return [(self._MANURE_ITEM, 1)]

    def _try_harvest_resource(self, player, dt):
        # Mini-game already running — held mouse does nothing; SPACE drives input
        if self._milking is not None:
            return None
        if not self.has_milk:
            self.reset_harvest()
            return None
        tool = player.hotbar[player.selected_slot]
        if tool != self.HARVEST_TOOL:
            self.reset_harvest()
            return None
        # Click with bucket starts the mini-game
        self.start_milking(player)
        return None


class Pig(Animal):
    ANIMAL_W = 26
    ANIMAL_H = 16
    HARVEST_TIME = 1.0
    MANURE_TIMER = 75.0
    _MANURE_ITEM = "pig_manure"
    MEAT_DROP = ("raw_pork", 3)
    NATIVE_BIOMES = {"temperate", "rolling_hills", "birch_forest", "savanna", "boreal"}
    PREFERRED_FOODS = ("apple", "carrot", "potato", "wheat", "corn", "acorn")

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "pig")
        self.has_manure = False
        self._manure_timer = self.MANURE_TIMER

        bx = int(float(x) // BLOCK_SIZE)
        biodome = world.biodome_at(bx) if world is not None else "temperate"
        eligible = PIG_BIOME_MAP.get(biodome, list(PIG_BREED_PROFILES.keys()))
        breed = random.choice(eligible) if eligible else "Large White"
        self.traits["breed"] = breed

        profile = PIG_BREED_PROFILES.get(breed, PIG_BREED_PROFILES["Large White"])
        self._init_pig_genotype(profile)

    def _init_pig_genotype(self, profile=None):
        if profile is None:
            breed = self.traits.get("breed", "Large White")
            profile = PIG_BREED_PROFILES.get(breed, PIG_BREED_PROFILES["Large White"])

        for gene_key, (lo, hi) in profile["genes"].items():
            self.genotype[gene_key] = [
                round(random.uniform(lo, hi), 3),
                round(random.uniform(lo, hi), 3),
            ]

        cw = profile["color_weights"]
        self.genotype["coat_color_gene"] = [
            random.choices(PIG_COLOR_ORDER, weights=cw)[0],
            random.choices(PIG_COLOR_ORDER, weights=cw)[0],
        ]
        pw = profile["pattern_weights"]
        self.genotype["coat_pattern_gene"] = [
            random.choices(PIG_PATTERN_ORDER, weights=pw)[0],
            random.choices(PIG_PATTERN_ORDER, weights=pw)[0],
        ]
        ew = profile["ear_weights"]
        self.genotype["ear_type_gene"] = [
            random.choices(PIG_EAR_ORDER, weights=ew)[0],
            random.choices(PIG_EAR_ORDER, weights=ew)[0],
        ]
        sw = profile["snout_weights"]
        self.genotype["snout_length_gene"] = [
            random.choices(PIG_SNOUT_ORDER, weights=sw)[0],
            random.choices(PIG_SNOUT_ORDER, weights=sw)[0],
        ]
        self._apply_genotype_to_traits()
        self.health = max(3, round(self.traits.get("constitution", 1.0) * 4))

    def _apply_genotype_to_traits(self):
        super()._apply_genotype_to_traits()
        for gene, trait, lo, hi in [
            ("meat_yield_gene",   "meat_yield",   0.6, 1.6),
            ("fat_gene",          "fat",          0.4, 1.6),
            ("growth_rate_gene",  "growth_rate",  0.6, 1.4),
            ("litter_size_gene",  "litter_size",  0.7, 1.7),
            ("constitution_gene", "constitution", 0.7, 1.5),
        ]:
            if gene in self.genotype:
                avg = sum(self.genotype[gene]) / 2
                self.traits[trait] = round(max(lo, min(hi, avg)), 3)
        for gene, trait, order in [
            ("coat_color_gene",    "coat_color",    PIG_COLOR_ORDER),
            ("coat_pattern_gene",  "coat_pattern",  PIG_PATTERN_ORDER),
            ("ear_type_gene",      "ear_type",      PIG_EAR_ORDER),
            ("snout_length_gene",  "snout_length",  PIG_SNOUT_ORDER),
        ]:
            if gene in self.genotype:
                self.traits[trait] = _expressed_categorical(self.genotype[gene], order)

    def _synthesize_genotype_from_traits(self):
        super()._synthesize_genotype_from_traits()
        for gene, trait, lo, hi in [
            ("meat_yield_gene",   "meat_yield",   0.6, 1.6),
            ("fat_gene",          "fat",          0.4, 1.6),
            ("growth_rate_gene",  "growth_rate",  0.6, 1.4),
            ("litter_size_gene",  "litter_size",  0.7, 1.7),
            ("constitution_gene", "constitution", 0.7, 1.5),
        ]:
            v = self.traits.get(trait, (lo + hi) / 2)
            n = random.uniform(-0.03, 0.03)
            self.genotype[gene] = [round(max(lo, min(hi, v + n)), 3), round(max(lo, min(hi, v - n)), 3)]
        self.genotype["coat_color_gene"]    = [self.traits.get("coat_color", "pink")] * 2
        self.genotype["coat_pattern_gene"]  = [self.traits.get("coat_pattern", "solid")] * 2
        self.genotype["ear_type_gene"]      = [self.traits.get("ear_type", "upright")] * 2
        self.genotype["snout_length_gene"]  = [self.traits.get("snout_length", "medium")] * 2

    def update(self, dt):
        super().update(dt)
        if self.dead:
            return
        if not self.has_manure:
            self._manure_timer -= dt
            if self._manure_timer <= 0:
                self.has_manure = True

    def collect_manure(self):
        if not self.has_manure:
            return None
        self.has_manure = False
        self._manure_timer = self.MANURE_TIMER
        return [(self._MANURE_ITEM, 1)]

    def try_feed(self, player):
        was_tamed = self.tamed
        ok = super().try_feed(player)
        if ok and not was_tamed and self.tamed:
            _record_pig_tame(self, player)
        return ok

    def _breed(self, other, world):
        was_count = len(world.entities)
        super()._breed(other, world)
        player = getattr(world, "_player_ref", None)
        if player is None or len(world.entities) <= was_count:
            return
        offspring = world.entities[-1]
        if not isinstance(offspring, Pig) or not (self.tamed and other.tamed):
            return
        player.pigs_bred = getattr(player, "pigs_bred", 0) + 1
        _record_pig_stats(offspring, player)
        # Litter size — extra piglets when both parents have strong litter_size trait
        avg_litter = (self.traits.get("litter_size", 1.0) + other.traits.get("litter_size", 1.0)) / 2
        extras = 0
        if avg_litter >= 1.3 and random.random() < (avg_litter - 1.2):
            extras = 1
        if avg_litter >= 1.5 and random.random() < (avg_litter - 1.4):
            extras = 2
        for _ in range(extras):
            piglet = Pig(offspring.x + random.uniform(-8, 8),
                         offspring.y, world)
            piglet.parent_a_uid = self.uid
            piglet.parent_b_uid = other.uid
            world.entities.append(piglet)
            player.pigs_bred += 1

    def try_harvest(self, player, dt):
        # Override base meat drop to scale with meat_yield_gene + fat bonus
        if self.dead:
            self.reset_harvest()
            return None
        tool = player.hotbar[player.selected_slot]
        if tool != "hunting_knife":
            return None
        self._kill_timer += dt
        self.being_harvested = True
        if self._kill_timer < 0.5:
            return None
        self._kill_timer = 0.0
        self.health -= 1
        if self.health > 0:
            return None
        self.dead = True
        self.reset_harvest()
        item_id, base = self.MEAT_DROP
        meat = max(1, round(base * self.traits.get("meat_yield", 1.0) * self._yield_mult()))
        if self.traits.get("mutation") == "giant":
            meat += 1
        drops = [(item_id, meat)]
        fat = self.traits.get("fat", 1.0)
        lard = int(fat) if fat >= 1.0 else 0
        if fat - int(fat) > 0 and random.random() < (fat - int(fat)):
            lard += 1
        if lard > 0:
            drops.append(("lard", lard))
        if self.traits.get("mutation") == "golden":
            drops.append(("golden_pork", 1))
        # Stash breed quality for charcuterie — one entry per meat/lard unit dropped.
        raw_q = ((self.traits.get("meat_yield", 1.0) - 0.6) * 0.5
                 + (self.traits.get("fat", 1.0) - 0.5) * 0.5)
        quality = max(0.0, min(1.0, raw_q))
        q = getattr(player, "pork_quality_queue", None)
        if q is not None:
            for _ in range(meat + lard):
                q.append(quality)
        return drops


def _record_pig_stats(pig, player):
    records = getattr(player, "pig_records", {})
    my = pig.traits.get("meat_yield", 0.0)
    ft = pig.traits.get("fat", 0.0)
    ls = pig.traits.get("litter_size", 0.0)
    if my > records.get("best_meat", 0.0):
        records["best_meat"] = my
    if ft > records.get("best_fat", 0.0):
        records["best_fat"] = ft
    if ls > records.get("best_litter", 0.0):
        records["best_litter"] = ls
    player.pig_records = records


def _record_pig_tame(pig, player):
    player.pigs_tamed = getattr(player, "pigs_tamed", 0) + 1
    breed = pig.traits.get("breed", "Large White")
    breeds = getattr(player, "discovered_pig_breeds", set())
    breeds.add(breed)
    player.discovered_pig_breeds = breeds
    biodome = pig.world.biodome_at(int(pig.x // BLOCK_SIZE)) if pig.world else "temperate"
    biomes = getattr(player, "discovered_pig_biomes", set())
    biomes.add(biodome)
    player.discovered_pig_biomes = biomes
    _record_pig_stats(pig, player)


class Chicken(Animal):
    ANIMAL_W = 18
    ANIMAL_H = 16
    HARVEST_TOOL = None  # collected empty-handed
    HARVEST_TIME = 1.0
    REFILL_TIME  = 30.0
    MANURE_TIMER = 90.0
    _MANURE_ITEM = "chicken_droppings"
    MEAT_DROP = ("raw_chicken", 1)
    NATIVE_BIOMES = {"temperate", "rolling_hills", "tropical", "savanna"}
    PREFERRED_FOODS = ("corn", "pea")

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "chicken")
        self._refill_timer = 0.0
        self.has_manure = False
        self._manure_timer = self.MANURE_TIMER

        bx = int(float(x) // BLOCK_SIZE)
        biodome = world.biodome_at(bx) if world is not None else "temperate"
        eligible = CHICKEN_BIOME_MAP.get(biodome, list(CHICKEN_BREED_PROFILES.keys()))
        breed = random.choice(eligible) if eligible else "Leghorn"
        self.traits["breed"] = breed

        # Only hens lay eggs
        self.has_egg = (self.traits["sex"] == "female")

        profile = CHICKEN_BREED_PROFILES.get(breed, CHICKEN_BREED_PROFILES["Leghorn"])
        self._init_chicken_genotype(profile)

    def _init_chicken_genotype(self, profile=None):
        if profile is None:
            breed = self.traits.get("breed", "Leghorn")
            profile = CHICKEN_BREED_PROFILES.get(breed, CHICKEN_BREED_PROFILES["Leghorn"])

        for gene_key, (lo, hi) in profile["genes"].items():
            self.genotype[gene_key] = [
                round(random.uniform(lo, hi), 3),
                round(random.uniform(lo, hi), 3),
            ]

        pw = profile["plumage_weights"]
        self.genotype["plumage_gene"] = [
            random.choices(PLUMAGE_ORDER, weights=pw)[0],
            random.choices(PLUMAGE_ORDER, weights=pw)[0],
        ]
        for key, order, wkey in [
            ("pattern_gene",  CHICKEN_PATTERN_ORDER, "pattern_weights"),
            ("comb_type_gene", CHICKEN_COMB_ORDER,   "comb_weights"),
            ("leg_type_gene",  CHICKEN_LEG_ORDER,    "leg_weights"),
        ]:
            w = profile[wkey]
            self.genotype[key] = [
                random.choices(order, weights=w)[0],
                random.choices(order, weights=w)[0],
            ]

        self._apply_genotype_to_traits()
        self.traits["egg_tint"] = profile.get("egg_tint", (245, 235, 200))
        self.health = max(2, round(self.traits.get("constitution", 1.0) * 3))

    def _apply_genotype_to_traits(self):
        super()._apply_genotype_to_traits()
        for gene, trait, lo, hi in [
            ("lay_rate_gene",        "lay_rate",        0.5, 2.0),
            ("constitution_gene",    "constitution",    0.7, 1.3),
            ("feather_density_gene", "feather_density", 0.0, 1.0),
        ]:
            if gene in self.genotype:
                avg = sum(self.genotype[gene]) / 2
                self.traits[trait] = round(max(lo, min(hi, avg)), 3)
        for gene, trait, order in [
            ("plumage_gene",  "plumage",   PLUMAGE_ORDER),
            ("pattern_gene",  "pattern",   CHICKEN_PATTERN_ORDER),
            ("comb_type_gene","comb_type", CHICKEN_COMB_ORDER),
            ("leg_type_gene", "leg_type",  CHICKEN_LEG_ORDER),
        ]:
            if gene in self.genotype:
                self.traits[trait] = _expressed_categorical(self.genotype[gene], order)

    def _synthesize_genotype_from_traits(self):
        super()._synthesize_genotype_from_traits()
        for gene, trait, lo, hi in [
            ("lay_rate_gene",        "lay_rate",        0.5, 2.0),
            ("constitution_gene",    "constitution",    0.7, 1.3),
            ("feather_density_gene", "feather_density", 0.0, 1.0),
        ]:
            v = self.traits.get(trait, (lo + hi) / 2)
            n = random.uniform(-0.03, 0.03)
            self.genotype[gene] = [round(max(lo, min(hi, v + n)), 3), round(max(lo, min(hi, v - n)), 3)]
        self.genotype["plumage_gene"]   = [self.traits.get("plumage", "white")] * 2
        self.genotype["pattern_gene"]   = [self.traits.get("pattern", "solid")] * 2
        self.genotype["comb_type_gene"] = [self.traits.get("comb_type", "single")] * 2
        self.genotype["leg_type_gene"]  = [self.traits.get("leg_type", "yellow")] * 2

    def update(self, dt):
        super().update(dt)
        if self.dead:
            return
        if self.traits.get("sex", "female") == "female" and not self.has_egg:
            self._refill_timer -= dt
            if self._refill_timer <= 0:
                self.has_egg = True
        if not self.has_manure:
            self._manure_timer -= dt
            if self._manure_timer <= 0:
                self.has_manure = True

    def collect_manure(self):
        if not self.has_manure:
            return None
        self.has_manure = False
        self._manure_timer = self.MANURE_TIMER
        return [(self._MANURE_ITEM, 1)]

    def _try_harvest_resource(self, player, dt):
        if not self.has_egg:
            self.reset_harvest()
            return None
        self._harvest_time += dt
        self.being_harvested = True
        if self._harvest_time >= self.HARVEST_TIME:
            self.reset_harvest()
            self.has_egg = False
            lay_rate = self.traits.get("lay_rate", 1.0)
            self._refill_timer = max(5.0, self.REFILL_TIME / lay_rate)
            prod  = self.traits.get("productivity", 1.0)
            mut   = self.traits.get("mutation")
            count = max(0, round(prod * self._yield_mult()))
            if mut == "giant":
                count += 1
            drops = [("egg", count)] if count > 0 else []
            if mut == "golden":
                drops.append(("golden_egg", 1))
            return self._finalize_drops(drops, "egg")
        return None


BIG_CAT_FLEE_RADIUS = 7   # blocks
BIG_CAT_FLEE_SPEED  = 2.6


class BigCat(Animal):
    """Base class for rare, unhuntable big cats that flee from the player."""
    ANIMAL_W = 36
    ANIMAL_H = 20
    PREFERRED_FOODS = ()
    MEAT_DROP = (None, 0)

    def __init__(self, x, y, world, animal_id):
        super().__init__(x, y, world, animal_id)

    def try_harvest(self, player, dt):
        self.reset_harvest()
        return None

    def _try_harvest_resource(self, player, dt):
        return None

    def _breed(self, other, world):
        pass

    def update(self, dt):
        if self.dead:
            return

        player = getattr(self.world, '_player_ref', None)
        if player is not None and not self._near_fence():
            pdx = (player.x + PLAYER_W / 2) - (self.x + self.W / 2)
            pdy = (player.y + PLAYER_H / 2) - (self.y + self.H / 2)
            dist = ((pdx / BLOCK_SIZE) ** 2 + (pdy / BLOCK_SIZE) ** 2) ** 0.5
            if dist < BIG_CAT_FLEE_RADIUS:
                flee_dir = -1 if pdx > 0 else 1
                self.vx = flee_dir * BIG_CAT_FLEE_SPEED
                self.facing = 1 if self.vx > 0 else -1
                self.vy = min(self.vy + GRAVITY, MAX_FALL)
                self._move_x(self.vx)
                self._move_y(self.vy)
                return

        self._wander_timer -= dt
        if self._wander_timer <= 0:
            self._wander_timer = random.uniform(2.0, 8.0)
            self._wander_dir = random.choice([-1, -1, 0, 0, 0, 1, 1])

        self.vx = self._wander_dir * ANIMAL_MOVE_SPEED
        if self.vx != 0:
            self.facing = 1 if self.vx > 0 else -1

        self.vy = min(self.vy + GRAVITY, MAX_FALL)
        self._move_x(self.vx)
        self._move_y(self.vy)


class SnowLeopard(BigCat):
    ANIMAL_W = 36
    ANIMAL_H = 20

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "snow_leopard")


class MountainLion(BigCat):
    ANIMAL_W = 38
    ANIMAL_H = 22

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "mountain_lion")


class Tiger(BigCat):
    ANIMAL_W = 44
    ANIMAL_H = 24

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "tiger")


# ---------------------------------------------------------------------------
# Huntable wildlife — flee from player, killed by arrows
# ---------------------------------------------------------------------------

HUNTABLE_FLEE_RADIUS = 9    # blocks
HUNTABLE_FLEE_SPEED  = 2.2


class HuntableAnimal(Animal):
    """Prey animal: flees the player and can only be killed by arrows."""

    TROPHY_STATS = {}  # subclasses override: {stat_key: (min, max, "unit")}

    def __init__(self, x, y, world, animal_id):
        super().__init__(x, y, world, animal_id)
        self._stunned_timer = 0.0
        self._barbed_timer  = 0.0
        self.stats = {
            k: round(random.uniform(lo, hi), 1)
            for k, (lo, hi, _) in self.TROPHY_STATS.items()
        }

    def try_harvest(self, player, dt):
        self.reset_harvest()
        return None

    def _try_harvest_resource(self, player, dt):
        return None

    def _breed(self, other, world):
        pass

    def update(self, dt):
        if self.dead:
            return
        if self._stunned_timer > 0:
            self._stunned_timer -= dt
            self.vx = 0
            self.vy = min(self.vy + GRAVITY, MAX_FALL)
            self._move_y(self.vy)
            return
        player = getattr(self.world, '_player_ref', None)
        if self._barbed_timer > 0:
            self._barbed_timer -= dt
        if player is not None:
            pdx = (player.x + PLAYER_W / 2) - (self.x + self.W / 2)
            pdy = (player.y + PLAYER_H / 2) - (self.y + self.H / 2)
            dist = ((pdx / BLOCK_SIZE) ** 2 + (pdy / BLOCK_SIZE) ** 2) ** 0.5
            if dist < HUNTABLE_FLEE_RADIUS:
                flee_dir = -1 if pdx > 0 else 1
                flee_speed = HUNTABLE_FLEE_SPEED * (0.4 if self._barbed_timer > 0 else 1.0)
                self.vx = flee_dir * flee_speed
                self.facing = 1 if self.vx > 0 else -1
                self.vy = min(self.vy + GRAVITY, MAX_FALL)
                self._move_x(self.vx)
                self._move_y(self.vy)
                return
        self._wander_timer -= dt
        if self._wander_timer <= 0:
            self._wander_timer = random.uniform(2.0, 6.0)
            self._wander_dir = random.choice([-1, -1, 0, 0, 1, 1])
        self.vx = self._wander_dir * ANIMAL_MOVE_SPEED
        if self.vx != 0:
            self.facing = 1 if self.vx > 0 else -1
        self.vy = min(self.vy + GRAVITY, MAX_FALL)
        self._move_x(self.vx)
        self._move_y(self.vy)

    def on_arrow_hit(self, damage=1, poison=False, barb=False):
        """Deal arrow damage. Returns drop list when dead, else None."""
        self.health -= damage
        if poison:
            self._stunned_timer = 3.0
        if barb:
            self._barbed_timer = 5.0
        if self.health <= 0:
            self.dead = True
            return list(self.MEAT_DROP)
        return None


class Deer(HuntableAnimal):
    ANIMAL_W = 28
    ANIMAL_H = 22
    MEAT_DROP = [("raw_venison", 2), ("deer_hide", 1), ("bone", 1)]
    TROPHY_STATS = {"antler_spread": (24, 62, "in")}

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "deer")
        self.health = 3


class Boar(HuntableAnimal):
    ANIMAL_W = 26
    ANIMAL_H = 18
    MEAT_DROP = [("raw_boar_meat", 2), ("bone", 1)]
    TROPHY_STATS = {"tusk_length": (3.0, 10.0, "in")}

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "boar")
        self.health = 3


class Rabbit(HuntableAnimal):
    ANIMAL_W = 14
    ANIMAL_H = 12
    MEAT_DROP = [("raw_rabbit", 1), ("rabbit_pelt", 1)]
    TROPHY_STATS = {"weight": (2.0, 6.0, "lbs")}

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "rabbit")
        self.health = 1


class Turkey(HuntableAnimal):
    ANIMAL_W = 20
    ANIMAL_H = 18
    MEAT_DROP = [("raw_turkey", 2), ("feather", 2)]
    TROPHY_STATS = {"beard_length": (4.0, 14.0, "in")}

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "turkey")
        self.health = 2


DEER_BIOMES   = {"temperate", "boreal", "birch_forest", "rolling_hills", "redwood"}
BOAR_BIOMES   = {"temperate", "jungle", "swamp", "boreal", "redwood"}
RABBIT_BIOMES = {"temperate", "boreal", "tundra", "steppe", "rolling_hills", "steep_hills"}
TURKEY_BIOMES = {"temperate", "boreal", "birch_forest", "rolling_hills"}


class Wolf(HuntableAnimal):
    ANIMAL_W = 26
    ANIMAL_H = 18
    MEAT_DROP = [("wolf_pelt", 1), ("bone", 1)]
    TROPHY_STATS = {"weight": (60, 180, "lbs")}

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "wolf")
        self.health = 2


class Bear(HuntableAnimal):
    ANIMAL_W = 34
    ANIMAL_H = 26
    MEAT_DROP = [("raw_bear_meat", 3), ("bear_pelt", 1), ("bone", 2)]
    TROPHY_STATS = {"weight": (200, 800, "lbs")}

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "bear")
        self.health = 4


class Duck(HuntableAnimal):
    ANIMAL_W = 16
    ANIMAL_H = 12
    MEAT_DROP = [("raw_duck", 1), ("feather", 2)]
    TROPHY_STATS = {"weight": (1.0, 4.0, "lbs")}

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "duck")
        self.health = 1


class Elk(HuntableAnimal):
    ANIMAL_W = 32
    ANIMAL_H = 26
    MEAT_DROP = [("raw_venison", 3), ("elk_antler", 1), ("bone", 1)]
    TROPHY_STATS = {"antler_spread": (30, 74, "in")}

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "elk")
        self.health = 3


class Bison(HuntableAnimal):
    ANIMAL_W = 36
    ANIMAL_H = 24
    MEAT_DROP = [("raw_bison_meat", 3), ("bison_hide", 1), ("bone", 1)]
    TROPHY_STATS = {"weight": (800, 2200, "lbs")}

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "bison")
        self.health = 3


class Fox(HuntableAnimal):
    ANIMAL_W = 20
    ANIMAL_H = 14
    MEAT_DROP = [("fox_pelt", 1), ("bone", 1)]
    TROPHY_STATS = {"weight": (8, 24, "lbs")}

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "fox")
        self.health = 1


class ArcticFox(HuntableAnimal):
    ANIMAL_W = 20
    ANIMAL_H = 14
    MEAT_DROP = [("arctic_fox_pelt", 1), ("bone", 1)]
    TROPHY_STATS = {"weight": (6, 20, "lbs")}

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "arctic_fox")
        self.health = 1


WOLF_BIOMES       = {"boreal", "tundra", "birch_forest", "redwood", "alpine_mountain"}
BEAR_BIOMES       = {"boreal", "redwood", "alpine_mountain", "rocky_mountain"}
DUCK_BIOMES       = {"wetland", "swamp", "temperate"}
ELK_BIOMES        = {"boreal", "tundra", "alpine_mountain", "rocky_mountain"}
BISON_BIOMES      = {"steppe", "savanna", "arid_steppe", "rolling_hills"}
FOX_BIOMES        = {"temperate", "boreal", "rolling_hills", "birch_forest"}
ARCTIC_FOX_BIOMES = {"tundra", "alpine_mountain", "frozen_tundra"}


class Moose(HuntableAnimal):
    ANIMAL_W = 36
    ANIMAL_H = 30
    MEAT_DROP = [("raw_venison", 4), ("moose_antler", 1), ("bone", 2)]
    TROPHY_STATS = {"antler_span": (36, 84, "in")}

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "moose")
        self.health = 4


class Bighorn(HuntableAnimal):
    ANIMAL_W = 24
    ANIMAL_H = 20
    MEAT_DROP = [("raw_mutton", 2), ("bighorn_horn", 1), ("bone", 1)]
    TROPHY_STATS = {"horn_score": (100, 220, "pts")}

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "bighorn")
        self.health = 2


class Pheasant(HuntableAnimal):
    ANIMAL_W = 18
    ANIMAL_H = 14
    MEAT_DROP = [("raw_pheasant", 1), ("feather", 3)]
    TROPHY_STATS = {"tail_length": (12, 36, "in")}

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "pheasant")
        self.health = 1


class Warthog(HuntableAnimal):
    ANIMAL_W = 24
    ANIMAL_H = 16
    MEAT_DROP = [("raw_boar_meat", 2), ("warthog_tusk", 1), ("bone", 1)]
    TROPHY_STATS = {"tusk_length": (4.0, 14.0, "in")}

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "warthog")
        self.health = 2


class MuskOx(HuntableAnimal):
    ANIMAL_W = 32
    ANIMAL_H = 22
    MEAT_DROP = [("raw_bison_meat", 3), ("musk_ox_hide", 1), ("bone", 1)]
    TROPHY_STATS = {"horn_spread": (20, 36, "in")}

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "musk_ox")
        self.health = 3


class Crocodile(HuntableAnimal):
    ANIMAL_W = 40
    ANIMAL_H = 14
    MEAT_DROP = [("raw_crocodile", 2), ("croc_hide", 1), ("bone", 1)]
    TROPHY_STATS = {"length": (5.0, 14.0, "ft")}

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "crocodile")
        self.health = 3


class Goose(HuntableAnimal):
    ANIMAL_W = 18
    ANIMAL_H = 16
    MEAT_DROP = [("raw_goose", 1), ("feather", 2)]
    TROPHY_STATS = {"weight": (5.0, 12.0, "lbs")}

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "goose")
        self.health = 1


class Hare(HuntableAnimal):
    ANIMAL_W = 16
    ANIMAL_H = 14
    MEAT_DROP = [("raw_rabbit", 1), ("rabbit_pelt", 1)]
    TROPHY_STATS = {"weight": (3.0, 8.0, "lbs")}
    # Hares flee faster than rabbits
    def update(self, dt):
        if self.dead:
            return
        player = getattr(self.world, '_player_ref', None)
        if player is not None:
            pdx = (player.x + PLAYER_W / 2) - (self.x + self.W / 2)
            pdy = (player.y + PLAYER_H / 2) - (self.y + self.H / 2)
            dist = ((pdx / BLOCK_SIZE) ** 2 + (pdy / BLOCK_SIZE) ** 2) ** 0.5
            if dist < HUNTABLE_FLEE_RADIUS + 3:
                flee_dir = -1 if pdx > 0 else 1
                self.vx = flee_dir * (HUNTABLE_FLEE_SPEED + 1.2)
                self.facing = 1 if self.vx > 0 else -1
                self.vy = min(self.vy + GRAVITY, MAX_FALL)
                self._move_x(self.vx)
                self._move_y(self.vy)
                return
        self._wander_timer -= dt
        if self._wander_timer <= 0:
            self._wander_timer = random.uniform(1.0, 4.0)
            self._wander_dir = random.choice([-1, -1, 0, 1, 1])
        self.vx = self._wander_dir * (ANIMAL_MOVE_SPEED + 0.5)
        if self.vx != 0:
            self.facing = 1 if self.vx > 0 else -1
        self.vy = min(self.vy + GRAVITY, MAX_FALL)
        self._move_x(self.vx)
        self._move_y(self.vy)

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "hare")
        self.health = 1


class Caribou(HuntableAnimal):
    ANIMAL_W = 30
    ANIMAL_H = 24
    MEAT_DROP = [("raw_venison", 3), ("caribou_hide", 1), ("caribou_antler", 1), ("bone", 1)]
    TROPHY_STATS = {"antler_spread": (28, 70, "in")}

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "caribou")
        self.health = 3


class Antelope(HuntableAnimal):
    ANIMAL_W = 24
    ANIMAL_H = 20
    MEAT_DROP = [("raw_venison", 2), ("antelope_hide", 1), ("antelope_horn", 1)]
    TROPHY_STATS = {"horn_length": (8, 26, "in")}

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "antelope")
        self.health = 2


class Ibex(HuntableAnimal):
    ANIMAL_W = 22
    ANIMAL_H = 20
    MEAT_DROP = [("raw_mutton", 2), ("ibex_horn", 1), ("bone", 1)]
    TROPHY_STATS = {"horn_curl": (16, 50, "in")}

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "ibex")
        self.health = 2


class Lynx(HuntableAnimal):
    ANIMAL_W = 22
    ANIMAL_H = 16
    MEAT_DROP = [("lynx_pelt", 1), ("bone", 1)]
    TROPHY_STATS = {"weight": (15, 50, "lbs")}

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "lynx")
        self.health = 2


class Coyote(HuntableAnimal):
    ANIMAL_W = 22
    ANIMAL_H = 16
    MEAT_DROP = [("coyote_pelt", 1), ("bone", 1)]
    TROPHY_STATS = {"weight": (20, 50, "lbs")}

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "coyote")
        self.health = 1


class Beaver(HuntableAnimal):
    ANIMAL_W = 20
    ANIMAL_H = 14
    MEAT_DROP = [("raw_beaver", 1), ("beaver_pelt", 1), ("beaver_tail", 1)]
    TROPHY_STATS = {"weight": (30, 70, "lbs")}

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "beaver")
        self.health = 1


CARIBOU_BIOMES  = {"tundra", "boreal", "alpine_mountain", "frozen_tundra"}
ANTELOPE_BIOMES = {"savanna", "steppe", "arid_steppe", "rolling_hills"}
IBEX_BIOMES     = {"alpine_mountain", "rocky_mountain", "canyon", "steep_hills"}
LYNX_BIOMES     = {"boreal", "birch_forest", "alpine_mountain", "redwood"}
COYOTE_BIOMES   = {"steppe", "arid_steppe", "savanna", "temperate", "wasteland"}
BEAVER_BIOMES   = {"wetland", "swamp", "temperate", "boreal"}


MOOSE_BIOMES    = {"boreal", "wetland", "steep_hills", "redwood"}
BIGHORN_BIOMES  = {"rocky_mountain", "alpine_mountain", "canyon", "red_rock", "steep_hills"}
PHEASANT_BIOMES = {"temperate", "birch_forest", "rolling_hills", "boreal"}
WARTHOG_BIOMES  = {"savanna", "arid_steppe", "steppe", "wasteland"}
MUSK_OX_BIOMES  = {"tundra", "alpine_mountain"}
CROC_BIOMES     = {"swamp", "wetland", "jungle", "tropical"}
GOOSE_BIOMES    = {"wetland", "temperate", "swamp"}
HARE_BIOMES     = {"steppe", "tundra", "arid_steppe", "wasteland"}


class Capybara(Animal):
    """Passive, unhuntable rodent — wanders near wetlands and rivers."""
    ANIMAL_W = 34
    ANIMAL_H = 18
    PREFERRED_FOODS = ()
    MEAT_DROP = (None, 0)

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "capybara")
        self.no_breed = True

    def try_harvest(self, _player, _dt):
        self.reset_harvest()
        return None

    def _try_harvest_resource(self, _player, _dt):
        return None

    def _breed(self, other, world):
        pass

    def update(self, dt):
        if self.dead:
            return
        self._wander_timer -= dt
        if self._wander_timer <= 0:
            self._wander_timer = random.uniform(2.0, 10.0)
            self._wander_dir = random.choice([-1, -1, 0, 0, 0, 0, 1, 1])
        self.vx = self._wander_dir * ANIMAL_MOVE_SPEED * 0.75
        if self.vx != 0:
            self.facing = 1 if self.vx > 0 else -1
        self.vy = min(self.vy + GRAVITY, MAX_FALL)
        self._move_x(self.vx)
        self._move_y(self.vy)


CAPYBARA_BIOMES = {"wetland", "swamp", "tropical", "jungle", "river"}
