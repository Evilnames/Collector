import random
import uuid
import pygame
from constants import BLOCK_SIZE, GRAVITY, JUMP_FORCE, MAX_FALL, PLAYER_W, PLAYER_H, MINE_REACH, HOTBAR_SIZE
from blocks import LADDER, WOOD_FENCE, IRON_FENCE, WATER

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

    def update(self, dt):
        if self.dead:
            return

        # Breeding cooldown
        self._breed_cooldown -= dt
        if (self._breed_cooldown <= 0
                and self.on_ground
                and not self.being_harvested
                and not self.no_breed):
            same = [e for e in self.world.entities
                    if type(e) is type(self) and not e.dead]
            if len(same) < 500:
                for other in same:
                    if other is self or other._breed_cooldown > 0 or other.no_breed:
                        continue
                    dx = (self.x + self.W / 2 - other.x - other.W / 2) / BLOCK_SIZE
                    dy = (self.y + self.H / 2 - other.y - other.H / 2) / BLOCK_SIZE
                    if (dx * dx + dy * dy) ** 0.5 <= 3.0:
                        self._breed(other, self.world)
                        break

        # Tamed: follow player instead of wandering
        if self.tamed:
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

        # Normal wander
        self._wander_timer -= dt
        if self._wander_timer <= 0:
            self._wander_timer = random.uniform(1.5, 5.0)
            self._wander_dir = random.choice([-1, -1, 0, 0, 0, 1, 1])

        self.vx = self._wander_dir * ANIMAL_MOVE_SPEED
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


class Sheep(Animal):
    ANIMAL_W = 24
    ANIMAL_H = 18
    HARVEST_TIME = 1.5
    REGROW_TIME  = 30.0
    MILK_REFILL_TIME = 25.0
    MEAT_DROP = ("raw_mutton", 2)
    PREFERRED_FOODS = ("wheat", "carrot")

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "sheep")
        self.has_wool = True
        self._regrow_timer = 0.0
        self._milk_refill_timer = 0.0

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
                count = max(1, round(weight))
                if mut == "giant":
                    count += 1
                drops = [("wool", count)]
                if mut == "golden":
                    drops.append(("golden_wool", 1))
                return drops
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
                count = max(1, round(prod))
                if mut == "giant":
                    count += 1
                drops = [("sheep_milk", count)]
                if mut == "golden":
                    drops.append(("golden_milk", 1))
                return drops
        else:
            self.reset_harvest()
        return None


class Goat(Animal):
    ANIMAL_W = 22
    ANIMAL_H = 18
    HARVEST_TOOL = "bucket"
    HARVEST_TIME = 1.5
    REFILL_TIME  = 25.0
    MEAT_DROP    = ("raw_mutton", 1)
    PREFERRED_FOODS = ("wheat", "carrot")

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "goat")
        self._refill_timer = 0.0

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
            count = max(1, round(volume))
            if mut == "giant":
                count += 1
            drops = [("goat_milk", count)]
            if mut == "golden":
                drops.append(("golden_milk", 1))
            return drops
        return None


class Cow(Animal):
    ANIMAL_W = 30
    ANIMAL_H = 20
    HARVEST_TOOL = "bucket"
    HARVEST_TIME = 1.5
    REFILL_TIME = 20.0
    MEAT_DROP = ("raw_beef", 2)
    PREFERRED_FOODS = ("wheat", "apple")

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "cow")
        self.has_milk = True
        self._refill_timer = 0.0

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

        count = max(1, round(volume * hits / 4))
        if mut == "giant":
            count += 1
        drops = [("milk", count)]
        if mut == "golden":
            drops.append(("golden_milk", 1))

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


class Chicken(Animal):
    ANIMAL_W = 18
    ANIMAL_H = 16
    HARVEST_TOOL = None  # collected empty-handed
    HARVEST_TIME = 1.0
    REFILL_TIME = 30.0
    MEAT_DROP = ("raw_chicken", 1)
    PREFERRED_FOODS = ("corn", "pea")

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "chicken")
        self._refill_timer = 0.0

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
            count = max(1, round(prod))
            if mut == "giant":
                count += 1
            drops = [("egg", count)]
            if mut == "golden":
                drops.append(("golden_egg", 1))
            return drops
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
        if player is not None:
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


WOLF_BIOMES  = {"boreal", "tundra", "birch_forest", "redwood", "alpine_mountain"}
BEAR_BIOMES  = {"boreal", "redwood", "alpine_mountain", "rocky_mountain"}
DUCK_BIOMES  = {"wetland", "swamp", "temperate"}
ELK_BIOMES   = {"boreal", "tundra", "alpine_mountain", "rocky_mountain"}
BISON_BIOMES = {"steppe", "savanna", "arid_steppe", "rolling_hills"}
FOX_BIOMES   = {"temperate", "boreal", "rolling_hills", "birch_forest"}


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


MOOSE_BIOMES    = {"boreal", "wetland", "steep_hills", "redwood"}
BIGHORN_BIOMES  = {"rocky_mountain", "alpine_mountain", "canyon", "steep_hills"}
PHEASANT_BIOMES = {"temperate", "birch_forest", "rolling_hills", "boreal"}
WARTHOG_BIOMES  = {"savanna", "arid_steppe", "steppe", "wasteland"}
MUSK_OX_BIOMES  = {"tundra", "alpine_mountain"}
CROC_BIOMES     = {"swamp", "wetland", "jungle", "tropical"}
GOOSE_BIOMES    = {"wetland", "temperate", "swamp"}
HARE_BIOMES     = {"steppe", "tundra", "arid_steppe", "wasteland"}
