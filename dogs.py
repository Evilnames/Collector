import random
from constants import BLOCK_SIZE, GRAVITY, MAX_FALL, PLAYER_W, PLAYER_H, HOTBAR_SIZE
from animals import Animal, _expressed_categorical

DOG_MOVE_SPEED    = 1.3
DOG_FLEE_SPEED    = 2.8
DOG_FLEE_RADIUS   = 6     # blocks — wild dogs flee from player
KENNEL_SEARCH_RADIUS = 6  # blocks from dog to look for KENNEL_BLOCK

# Categorical gene dominance orders
DOG_COAT_PATTERN_ORDER   = ["solid", "spotted", "merle", "brindle", "saddle", "ticked"]
DOG_COAT_LENGTH_ORDER    = ["short", "medium", "long"]
DOG_COAT_TYPE_ORDER      = ["smooth", "wavy", "curly", "wire"]
DOG_EAR_TYPE_ORDER       = ["erect", "semi-erect", "floppy"]
DOG_TAIL_TYPE_ORDER      = ["long", "curled", "short", "bob"]
DOG_EYE_COLOR_ORDER      = ["brown", "amber", "blue", "heterochromia"]
DOG_SIZE_CLASS_ORDER     = ["medium", "large", "small", "giant", "toy"]

# Color genetics ─────────────────────────────────────────────────────────────
# Dominance: black > brown > red > yellow > cream  (index 0 = dominant)
BASE_COLOR_ORDER    = ["black", "brown", "red", "yellow", "cream"]
# Dilute is fully recessive — both alleles must be "dilute" to express
DILUTE_ORDER        = ["full", "dilute"]
# White spotting — more white = more recessive
WHITE_SPOTTING_ORDER = ["solid", "irish", "piebald", "extreme_white"]

# Named color descriptions shown in the view panel
COLOR_NAMES = {
    ("black",  "full"):   "Jet Black",
    ("black",  "dilute"): "Blue/Slate",
    ("brown",  "full"):   "Chocolate",
    ("brown",  "dilute"): "Lilac",
    ("red",    "full"):   "Red/Mahogany",
    ("red",    "dilute"): "Apricot",
    ("yellow", "full"):   "Golden",
    ("yellow", "dilute"): "Pale Gold",
    ("cream",  "full"):   "Cream",
    ("cream",  "dilute"): "Platinum",
}

# RGB values for each base_color × dilute combination
COLOR_RGB = {
    ("black",  "full"):   (28,  22,  18),
    ("black",  "dilute"): (95,  100, 115),
    ("brown",  "full"):   (110,  58,  24),
    ("brown",  "dilute"): (175, 148, 165),
    ("red",    "full"):   (190,  75,  30),
    ("red",    "dilute"): (215, 155, 105),
    ("yellow", "full"):   (205, 168,  55),
    ("yellow", "dilute"): (228, 212, 158),
    ("cream",  "full"):   (235, 222, 192),
    ("cream",  "dilute"): (248, 243, 232),
}

DOG_EYE_COLORS = {
    "brown":         (100, 60, 20),
    "amber":         (180, 120, 30),
    "blue":          (80, 130, 200),
    "heterochromia": (140, 90, 30),
}

# Per-breed color gene weights
# base_color_weights: parallel to BASE_COLOR_ORDER [black, brown, red, yellow, cream]
# dilute_carrier_prob: per-allele chance of carrying dilute (0.0–1.0)
# white_spotting_weights: parallel to WHITE_SPOTTING_ORDER [solid, irish, piebald, extreme_white]
_BREED_COLOR_GENES = {
    "Border Collie":      {"base": [65, 20,  8,  5,  2], "dilute": 0.10, "spotting": [10, 60, 25,  5]},
    "Husky":              {"base": [50,  5,  5, 15, 25], "dilute": 0.30, "spotting": [ 5, 30, 55, 10]},
    "Greyhound":          {"base": [30, 10, 25, 25, 10], "dilute": 0.20, "spotting": [50, 35, 15,  0]},
    "Bloodhound":         {"base": [20, 55, 20,  5,  0], "dilute": 0.08, "spotting": [70, 15, 10,  5]},
    "German Shepherd":    {"base": [60, 30,  8,  2,  0], "dilute": 0.05, "spotting": [80, 15,  5,  0]},
    "Labrador":           {"base": [30, 30,  5, 30,  5], "dilute": 0.25, "spotting": [90,  8,  2,  0]},
    "Dalmatian":          {"base": [90,  5,  3,  2,  0], "dilute": 0.10, "spotting": [ 0,  0, 20, 80]},
    "Beagle":             {"base": [25, 40, 25,  8,  2], "dilute": 0.10, "spotting": [10, 55, 30,  5]},
    "Poodle":             {"base": [30, 20, 15, 20, 15], "dilute": 0.35, "spotting": [85, 10,  5,  0]},
    "Bulldog":            {"base": [10, 20, 40, 20, 10], "dilute": 0.20, "spotting": [20, 30, 40, 10]},
    "Malamute":           {"base": [50,  5,  5, 15, 25], "dilute": 0.15, "spotting": [10, 25, 55, 10]},
    "Vizsla":             {"base": [ 5, 15, 70,  8,  2], "dilute": 0.20, "spotting": [75, 20,  5,  0]},
    "Australian Shepherd":{"base": [40, 25, 20, 10,  5], "dilute": 0.20, "spotting": [ 5, 25, 55, 15]},
    "Dachshund":          {"base": [20, 50, 20,  5,  5], "dilute": 0.15, "spotting": [60, 15, 20,  5]},
    "Setter":             {"base": [ 5,  5, 80,  8,  2], "dilute": 0.10, "spotting": [60, 35,  5,  0]},
    # New breeds
    "Akita":              {"base": [40, 15, 30, 10,  5], "dilute": 0.08, "spotting": [55, 35, 10,  0]},
    "Rottweiler":         {"base": [80, 15,  3,  2,  0], "dilute": 0.05, "spotting": [85, 12,  3,  0]},
    "Samoyed":            {"base": [ 5,  0,  5, 20, 70], "dilute": 0.55, "spotting": [ 5, 10, 20, 65]},
    "Shiba Inu":          {"base": [15,  5, 55, 20,  5], "dilute": 0.12, "spotting": [30, 55, 15,  0]},
    "Great Pyrenees":     {"base": [ 5,  0,  5, 20, 70], "dilute": 0.40, "spotting": [ 0,  5, 10, 85]},
    "Weimaraner":         {"base": [85,  8,  3,  2,  2], "dilute": 0.85, "spotting": [90,  8,  2,  0]},
    "Doberman":           {"base": [75, 20,  3,  2,  0], "dilute": 0.18, "spotting": [90,  8,  2,  0]},
    "Chow Chow":          {"base": [ 5,  5, 50, 25, 15], "dilute": 0.12, "spotting": [95,  4,  1,  0]},
    "Jack Russell":       {"base": [30, 25, 25, 15,  5], "dilute": 0.15, "spotting": [ 0, 20, 45, 35]},
    "Rhodesian Ridgeback":{"base": [ 5,  5, 70, 18,  2], "dilute": 0.08, "spotting": [90,  8,  2,  0]},
    "Cane Corso":         {"base": [55, 20, 10, 10,  5], "dilute": 0.15, "spotting": [75, 18,  7,  0]},
    "Bernese Mountain Dog":{"base":[75, 15,  5,  4,  1], "dilute": 0.05, "spotting": [ 0, 10, 80, 10]},
    "Whippet":            {"base": [25, 15, 25, 20, 15], "dilute": 0.22, "spotting": [25, 40, 30,  5]},
    "Basenji":            {"base": [ 5, 10, 55, 25,  5], "dilute": 0.06, "spotting": [50, 40, 10,  0]},
    "Saint Bernard":      {"base": [10, 10, 55, 20,  5], "dilute": 0.08, "spotting": [ 0, 15, 70, 15]},
}

# Per-breed data: biomes, size, gene ranges, ability carrier chances,
# coat colour palette, coat_pattern_weights, ear/tail/coat defaults.
BREED_PROFILES = {
    "Border Collie": {
        "biomes": {"temperate", "rolling_hills", "birch_forest"},
        "size_class": "medium",
        "genes": {
            "speed_gene":       (0.9, 1.2),
            "endurance_gene":   (0.9, 1.2),
            "agility_gene":     (1.1, 1.3),
            "strength_gene":    (0.7, 1.0),
            "nose_gene":        (0.8, 1.1),
            "alertness_gene":   (0.9, 1.2),
            "loyalty_gene":     (0.7, 1.0),
            "playfulness_gene": (0.5, 0.9),
            "stubbornness_gene":(0.2, 0.5),
            "prey_drive_gene":  (0.7, 1.0),
        },
        "abilities": {"herding": 0.60},
        "coat_colors": [(80, 60, 40), (220, 215, 200), (30, 28, 28)],
        "coat_pattern_weights": [30, 35, 0, 0, 25, 10],
        "ear_type": "semi-erect",
        "tail_type": "long",
        "coat_length": "medium",
        "coat_type_weights": [0, 60, 40, 0],
    },
    "Husky": {
        "biomes": {"tundra", "boreal", "alpine_mountain"},
        "size_class": "large",
        "genes": {
            "speed_gene":       (1.0, 1.3),
            "endurance_gene":   (1.1, 1.3),
            "agility_gene":     (0.9, 1.1),
            "strength_gene":    (0.9, 1.2),
            "nose_gene":        (0.8, 1.1),
            "alertness_gene":   (0.9, 1.2),
            "loyalty_gene":     (0.5, 0.8),
            "playfulness_gene": (0.7, 1.0),
            "stubbornness_gene":(0.5, 0.8),
            "prey_drive_gene":  (0.6, 0.9),
        },
        "abilities": {},
        "coat_colors": [(200, 195, 190), (80, 75, 70), (240, 238, 235)],
        "coat_pattern_weights": [20, 40, 0, 0, 40, 0],
        "ear_type": "erect",
        "tail_type": "curled",
        "coat_length": "medium",
        "coat_type_weights": [60, 40, 0, 0],
    },
    "Greyhound": {
        "biomes": {"savanna", "steppe", "arid_steppe", "beach", "tropical"},
        "size_class": "large",
        "genes": {
            "speed_gene":       (1.2, 1.3),
            "endurance_gene":   (0.7, 0.9),
            "agility_gene":     (1.0, 1.2),
            "strength_gene":    (0.7, 0.9),
            "nose_gene":        (0.7, 0.9),
            "alertness_gene":   (0.8, 1.0),
            "loyalty_gene":     (0.5, 0.8),
            "playfulness_gene": (0.4, 0.7),
            "stubbornness_gene":(0.3, 0.6),
            "prey_drive_gene":  (0.8, 1.0),
        },
        "abilities": {},
        "coat_colors": [(200, 190, 175), (80, 75, 68), (165, 155, 140)],
        "coat_pattern_weights": [70, 10, 0, 20, 0, 0],
        "ear_type": "floppy",
        "tail_type": "long",
        "coat_length": "short",
        "coat_type_weights": [100, 0, 0, 0],
    },
    "Bloodhound": {
        "biomes": {"wetland", "jungle", "swamp"},
        "size_class": "large",
        "genes": {
            "speed_gene":       (0.7, 1.0),
            "endurance_gene":   (0.9, 1.2),
            "agility_gene":     (0.7, 0.9),
            "strength_gene":    (0.9, 1.2),
            "nose_gene":        (1.2, 1.3),
            "alertness_gene":   (0.7, 1.0),
            "loyalty_gene":     (0.7, 1.0),
            "playfulness_gene": (0.3, 0.6),
            "stubbornness_gene":(0.5, 0.8),
            "prey_drive_gene":  (0.9, 1.1),
        },
        "abilities": {"tracking": 0.70},
        "coat_colors": [(140, 80, 40), (100, 55, 25), (185, 115, 65)],
        "coat_pattern_weights": [50, 0, 0, 0, 50, 0],
        "ear_type": "floppy",
        "tail_type": "long",
        "coat_length": "short",
        "coat_type_weights": [100, 0, 0, 0],
    },
    "German Shepherd": {
        "biomes": {"temperate", "rolling_hills"},
        "size_class": "large",
        "genes": {
            "speed_gene":       (0.9, 1.2),
            "endurance_gene":   (1.0, 1.2),
            "agility_gene":     (1.0, 1.2),
            "strength_gene":    (1.0, 1.2),
            "nose_gene":        (0.9, 1.2),
            "alertness_gene":   (1.0, 1.3),
            "loyalty_gene":     (0.8, 1.0),
            "playfulness_gene": (0.5, 0.8),
            "stubbornness_gene":(0.2, 0.5),
            "prey_drive_gene":  (0.7, 1.0),
        },
        "abilities": {"guard": 0.60},
        "coat_colors": [(60, 40, 20), (180, 150, 80), (30, 25, 18)],
        "coat_pattern_weights": [0, 0, 0, 0, 70, 30],
        "ear_type": "erect",
        "tail_type": "long",
        "coat_length": "medium",
        "coat_type_weights": [80, 20, 0, 0],
    },
    "Labrador": {
        "biomes": {"beach", "wetland", "temperate"},
        "size_class": "large",
        "genes": {
            "speed_gene":       (0.9, 1.2),
            "endurance_gene":   (1.0, 1.2),
            "agility_gene":     (0.9, 1.1),
            "strength_gene":    (1.0, 1.2),
            "nose_gene":        (0.9, 1.2),
            "alertness_gene":   (0.8, 1.1),
            "loyalty_gene":     (0.8, 1.0),
            "playfulness_gene": (0.8, 1.0),
            "stubbornness_gene":(0.1, 0.4),
            "prey_drive_gene":  (0.5, 0.8),
        },
        "abilities": {"retrieve": 0.70},
        "coat_colors": [(220, 195, 150), (50, 40, 30), (210, 205, 195)],
        "coat_pattern_weights": [100, 0, 0, 0, 0, 0],
        "ear_type": "floppy",
        "tail_type": "long",
        "coat_length": "short",
        "coat_type_weights": [100, 0, 0, 0],
    },
    "Dalmatian": {
        "biomes": {"temperate", "rocky_mountain", "beach"},
        "size_class": "large",
        "genes": {
            "speed_gene":       (1.0, 1.2),
            "endurance_gene":   (1.1, 1.3),
            "agility_gene":     (1.0, 1.2),
            "strength_gene":    (0.8, 1.1),
            "nose_gene":        (0.8, 1.0),
            "alertness_gene":   (0.9, 1.1),
            "loyalty_gene":     (0.6, 0.9),
            "playfulness_gene": (0.7, 1.0),
            "stubbornness_gene":(0.4, 0.7),
            "prey_drive_gene":  (0.5, 0.8),
        },
        "abilities": {},
        "coat_colors": [(235, 232, 225), (235, 232, 225)],
        "coat_pattern_weights": [0, 100, 0, 0, 0, 0],
        "ear_type": "floppy",
        "tail_type": "long",
        "coat_length": "short",
        "coat_type_weights": [100, 0, 0, 0],
    },
    "Beagle": {
        "biomes": {"boreal", "temperate", "birch_forest"},
        "size_class": "small",
        "genes": {
            "speed_gene":       (0.8, 1.1),
            "endurance_gene":   (0.9, 1.1),
            "agility_gene":     (0.8, 1.0),
            "strength_gene":    (0.7, 0.9),
            "nose_gene":        (1.1, 1.3),
            "alertness_gene":   (0.9, 1.2),
            "loyalty_gene":     (0.7, 1.0),
            "playfulness_gene": (0.7, 1.0),
            "stubbornness_gene":(0.4, 0.7),
            "prey_drive_gene":  (0.8, 1.1),
        },
        "abilities": {"tracking": 0.50},
        "coat_colors": [(180, 155, 100), (80, 55, 30), (220, 215, 200)],
        "coat_pattern_weights": [0, 0, 0, 0, 80, 20],
        "ear_type": "floppy",
        "tail_type": "long",
        "coat_length": "short",
        "coat_type_weights": [100, 0, 0, 0],
    },
    "Poodle": {
        "biomes": {"temperate", "birch_forest"},
        "size_class": "medium",
        "genes": {
            "speed_gene":       (0.8, 1.1),
            "endurance_gene":   (0.9, 1.1),
            "agility_gene":     (1.0, 1.2),
            "strength_gene":    (0.7, 0.9),
            "nose_gene":        (0.8, 1.1),
            "alertness_gene":   (0.9, 1.2),
            "loyalty_gene":     (0.7, 1.0),
            "playfulness_gene": (0.8, 1.0),
            "stubbornness_gene":(0.0, 0.3),
            "prey_drive_gene":  (0.3, 0.6),
        },
        "abilities": {},
        "coat_colors": [(235, 230, 220), (80, 70, 60), (200, 185, 155)],
        "coat_pattern_weights": [100, 0, 0, 0, 0, 0],
        "ear_type": "floppy",
        "tail_type": "curled",
        "coat_length": "long",
        "coat_type_weights": [0, 0, 100, 0],
    },
    "Bulldog": {
        "biomes": {"temperate", "canyon"},
        "size_class": "medium",
        "genes": {
            "speed_gene":       (0.7, 0.9),
            "endurance_gene":   (0.8, 1.0),
            "agility_gene":     (0.7, 0.9),
            "strength_gene":    (1.1, 1.3),
            "nose_gene":        (0.7, 1.0),
            "alertness_gene":   (0.8, 1.1),
            "loyalty_gene":     (0.8, 1.0),
            "playfulness_gene": (0.4, 0.7),
            "stubbornness_gene":(0.6, 0.9),
            "prey_drive_gene":  (0.4, 0.7),
        },
        "abilities": {"guard": 0.40},
        "coat_colors": [(190, 160, 120), (160, 130, 95), (80, 65, 45)],
        "coat_pattern_weights": [50, 30, 0, 20, 0, 0],
        "ear_type": "semi-erect",
        "tail_type": "short",
        "coat_length": "short",
        "coat_type_weights": [100, 0, 0, 0],
    },
    "Malamute": {
        "biomes": {"tundra", "alpine_mountain"},
        "size_class": "large",
        "genes": {
            "speed_gene":       (0.9, 1.1),
            "endurance_gene":   (1.1, 1.3),
            "agility_gene":     (0.8, 1.0),
            "strength_gene":    (1.1, 1.3),
            "nose_gene":        (0.8, 1.1),
            "alertness_gene":   (0.9, 1.1),
            "loyalty_gene":     (0.7, 0.9),
            "playfulness_gene": (0.5, 0.8),
            "stubbornness_gene":(0.6, 0.9),
            "prey_drive_gene":  (0.6, 0.9),
        },
        "abilities": {},
        "coat_colors": [(215, 210, 200), (55, 50, 45), (185, 175, 160)],
        "coat_pattern_weights": [20, 0, 0, 0, 80, 0],
        "ear_type": "erect",
        "tail_type": "curled",
        "coat_length": "long",
        "coat_type_weights": [60, 40, 0, 0],
    },
    "Vizsla": {
        "biomes": {"steppe", "savanna", "rolling_hills"},
        "size_class": "medium",
        "genes": {
            "speed_gene":       (1.0, 1.3),
            "endurance_gene":   (1.0, 1.2),
            "agility_gene":     (1.0, 1.2),
            "strength_gene":    (0.8, 1.1),
            "nose_gene":        (1.0, 1.2),
            "alertness_gene":   (1.0, 1.2),
            "loyalty_gene":     (0.8, 1.0),
            "playfulness_gene": (0.7, 1.0),
            "stubbornness_gene":(0.2, 0.5),
            "prey_drive_gene":  (0.8, 1.1),
        },
        "abilities": {"retrieve": 0.50},
        "coat_colors": [(200, 130, 65), (180, 115, 55), (215, 150, 80)],
        "coat_pattern_weights": [100, 0, 0, 0, 0, 0],
        "ear_type": "floppy",
        "tail_type": "short",
        "coat_length": "short",
        "coat_type_weights": [100, 0, 0, 0],
    },
    "Australian Shepherd": {
        "biomes": {"rolling_hills", "steppe", "temperate", "wetland", "swamp"},
        "size_class": "medium",
        "genes": {
            "speed_gene":       (1.0, 1.2),
            "endurance_gene":   (1.0, 1.2),
            "agility_gene":     (1.1, 1.3),
            "strength_gene":    (0.8, 1.1),
            "nose_gene":        (0.9, 1.2),
            "alertness_gene":   (1.0, 1.2),
            "loyalty_gene":     (0.8, 1.0),
            "playfulness_gene": (0.6, 0.9),
            "stubbornness_gene":(0.2, 0.5),
            "prey_drive_gene":  (0.8, 1.0),
        },
        "abilities": {"herding": 0.55},
        "coat_colors": [(80, 95, 115), (200, 195, 180), (50, 60, 70)],
        "coat_pattern_weights": [10, 15, 60, 0, 0, 15],
        "ear_type": "semi-erect",
        "tail_type": "bob",
        "coat_length": "medium",
        "coat_type_weights": [20, 80, 0, 0],
    },
    "Dachshund": {
        "biomes": {"boreal", "birch_forest", "fungal", "swamp"},
        "size_class": "small",
        "genes": {
            "speed_gene":       (0.7, 0.9),
            "endurance_gene":   (0.8, 1.1),
            "agility_gene":     (0.7, 0.9),
            "strength_gene":    (0.7, 0.9),
            "nose_gene":        (1.0, 1.3),
            "alertness_gene":   (1.0, 1.2),
            "loyalty_gene":     (0.7, 1.0),
            "playfulness_gene": (0.6, 0.9),
            "stubbornness_gene":(0.6, 0.9),
            "prey_drive_gene":  (0.9, 1.2),
        },
        "abilities": {"tracking": 0.40},
        "coat_colors": [(120, 70, 30), (60, 35, 15), (190, 160, 100)],
        "coat_pattern_weights": [60, 0, 0, 40, 0, 0],
        "ear_type": "floppy",
        "tail_type": "long",
        "coat_length": "short",
        "coat_type_weights": [60, 20, 20, 0],
    },
    "Setter": {
        "biomes": {"temperate", "boreal", "redwood"},
        "size_class": "large",
        "genes": {
            "speed_gene":       (1.0, 1.2),
            "endurance_gene":   (1.0, 1.2),
            "agility_gene":     (1.0, 1.2),
            "strength_gene":    (0.8, 1.1),
            "nose_gene":        (1.0, 1.2),
            "alertness_gene":   (0.9, 1.2),
            "loyalty_gene":     (0.8, 1.0),
            "playfulness_gene": (0.7, 1.0),
            "stubbornness_gene":(0.3, 0.6),
            "prey_drive_gene":  (0.7, 1.0),
        },
        "abilities": {"retrieve": 0.45, "tracking": 0.30},
        "coat_colors": [(190, 90, 40), (210, 110, 55), (170, 75, 30)],
        "coat_pattern_weights": [100, 0, 0, 0, 0, 0],
        "ear_type": "floppy",
        "tail_type": "long",
        "coat_length": "long",
        "coat_type_weights": [0, 80, 20, 0],
    },
    "Akita": {
        "biomes": {"boreal", "alpine_mountain", "rocky_mountain", "redwood"},
        "size_class": "large",
        "genes": {
            "speed_gene":        (0.9, 1.2),
            "endurance_gene":    (1.0, 1.2),
            "agility_gene":      (0.9, 1.1),
            "strength_gene":     (1.1, 1.3),
            "nose_gene":         (0.8, 1.1),
            "alertness_gene":    (1.0, 1.3),
            "loyalty_gene":      (0.8, 1.0),
            "playfulness_gene":  (0.4, 0.7),
            "stubbornness_gene": (0.5, 0.8),
            "prey_drive_gene":   (0.7, 1.0),
        },
        "abilities": {"guard": 0.55},
        "coat_colors": [(220, 200, 160), (28, 22, 18), (190, 75, 30)],
        "coat_pattern_weights": [55, 0, 0, 0, 40, 5],
        "ear_type": "erect",
        "tail_type": "curled",
        "coat_length": "short",
        "coat_type_weights": [80, 20, 0, 0],
    },
    "Rottweiler": {
        "biomes": {"temperate", "canyon", "wasteland", "swamp"},
        "size_class": "large",
        "genes": {
            "speed_gene":        (0.8, 1.1),
            "endurance_gene":    (0.9, 1.2),
            "agility_gene":      (0.8, 1.0),
            "strength_gene":     (1.1, 1.3),
            "nose_gene":         (0.8, 1.1),
            "alertness_gene":    (1.0, 1.3),
            "loyalty_gene":      (0.8, 1.0),
            "playfulness_gene":  (0.4, 0.7),
            "stubbornness_gene": (0.4, 0.7),
            "prey_drive_gene":   (0.7, 1.0),
        },
        "abilities": {"guard": 0.65},
        "coat_colors": [(28, 22, 18), (40, 28, 12)],
        "coat_pattern_weights": [0, 0, 0, 0, 90, 10],
        "ear_type": "floppy",
        "tail_type": "short",
        "coat_length": "short",
        "coat_type_weights": [100, 0, 0, 0],
    },
    "Samoyed": {
        "biomes": {"tundra", "alpine_mountain"},
        "size_class": "large",
        "genes": {
            "speed_gene":        (0.9, 1.2),
            "endurance_gene":    (1.1, 1.3),
            "agility_gene":      (0.9, 1.1),
            "strength_gene":     (0.9, 1.2),
            "nose_gene":         (0.8, 1.1),
            "alertness_gene":    (0.8, 1.1),
            "loyalty_gene":      (0.7, 1.0),
            "playfulness_gene":  (0.7, 1.0),
            "stubbornness_gene": (0.4, 0.7),
            "prey_drive_gene":   (0.5, 0.8),
        },
        "abilities": {},
        "coat_colors": [(235, 222, 192), (248, 243, 232)],
        "coat_pattern_weights": [100, 0, 0, 0, 0, 0],
        "ear_type": "erect",
        "tail_type": "curled",
        "coat_length": "long",
        "coat_type_weights": [40, 60, 0, 0],
    },
    "Shiba Inu": {
        "biomes": {"boreal", "birch_forest", "temperate", "fungal"},
        "size_class": "small",
        "genes": {
            "speed_gene":        (0.9, 1.2),
            "endurance_gene":    (0.9, 1.1),
            "agility_gene":      (1.0, 1.2),
            "strength_gene":     (0.7, 1.0),
            "nose_gene":         (0.8, 1.1),
            "alertness_gene":    (1.0, 1.3),
            "loyalty_gene":      (0.6, 0.9),
            "playfulness_gene":  (0.5, 0.8),
            "stubbornness_gene": (0.6, 0.9),
            "prey_drive_gene":   (0.7, 1.0),
        },
        "abilities": {"guard": 0.30},
        "coat_colors": [(190, 75, 30), (205, 168, 55), (28, 22, 18)],
        "coat_pattern_weights": [30, 0, 0, 0, 60, 10],
        "ear_type": "erect",
        "tail_type": "curled",
        "coat_length": "short",
        "coat_type_weights": [80, 20, 0, 0],
    },
    "Great Pyrenees": {
        "biomes": {"alpine_mountain", "rocky_mountain", "tundra", "redwood"},
        "size_class": "giant",
        "genes": {
            "speed_gene":        (0.8, 1.0),
            "endurance_gene":    (1.0, 1.2),
            "agility_gene":      (0.7, 0.9),
            "strength_gene":     (1.1, 1.3),
            "nose_gene":         (0.8, 1.1),
            "alertness_gene":    (1.0, 1.2),
            "loyalty_gene":      (0.8, 1.0),
            "playfulness_gene":  (0.4, 0.7),
            "stubbornness_gene": (0.4, 0.7),
            "prey_drive_gene":   (0.5, 0.8),
        },
        "abilities": {"guard": 0.60},
        "coat_colors": [(235, 222, 192), (248, 243, 232)],
        "coat_pattern_weights": [80, 0, 0, 0, 20, 0],
        "ear_type": "floppy",
        "tail_type": "long",
        "coat_length": "long",
        "coat_type_weights": [40, 60, 0, 0],
    },
    "Weimaraner": {
        "biomes": {"temperate", "steppe", "rolling_hills"},
        "size_class": "large",
        "genes": {
            "speed_gene":        (1.1, 1.3),
            "endurance_gene":    (1.0, 1.2),
            "agility_gene":      (1.0, 1.2),
            "strength_gene":     (0.9, 1.1),
            "nose_gene":         (1.1, 1.3),
            "alertness_gene":    (1.0, 1.2),
            "loyalty_gene":      (0.8, 1.0),
            "playfulness_gene":  (0.6, 0.9),
            "stubbornness_gene": (0.3, 0.6),
            "prey_drive_gene":   (0.9, 1.2),
        },
        "abilities": {"tracking": 0.45, "retrieve": 0.35},
        "coat_colors": [(95, 100, 115), (110, 115, 125)],
        "coat_pattern_weights": [100, 0, 0, 0, 0, 0],
        "ear_type": "floppy",
        "tail_type": "short",
        "coat_length": "short",
        "coat_type_weights": [100, 0, 0, 0],
    },
    "Doberman": {
        "biomes": {"temperate", "wasteland", "canyon"},
        "size_class": "large",
        "genes": {
            "speed_gene":        (1.1, 1.3),
            "endurance_gene":    (1.0, 1.2),
            "agility_gene":      (1.0, 1.2),
            "strength_gene":     (1.0, 1.2),
            "nose_gene":         (0.8, 1.1),
            "alertness_gene":    (1.1, 1.3),
            "loyalty_gene":      (0.8, 1.0),
            "playfulness_gene":  (0.4, 0.7),
            "stubbornness_gene": (0.3, 0.6),
            "prey_drive_gene":   (0.7, 1.0),
        },
        "abilities": {"guard": 0.65},
        "coat_colors": [(28, 22, 18), (110, 58, 24)],
        "coat_pattern_weights": [0, 0, 0, 0, 90, 10],
        "ear_type": "erect",
        "tail_type": "short",
        "coat_length": "short",
        "coat_type_weights": [100, 0, 0, 0],
    },
    "Chow Chow": {
        "biomes": {"boreal", "alpine_mountain", "fungal"},
        "size_class": "medium",
        "genes": {
            "speed_gene":        (0.8, 1.0),
            "endurance_gene":    (0.9, 1.1),
            "agility_gene":      (0.7, 0.9),
            "strength_gene":     (0.9, 1.2),
            "nose_gene":         (0.7, 1.0),
            "alertness_gene":    (0.9, 1.2),
            "loyalty_gene":      (0.7, 1.0),
            "playfulness_gene":  (0.3, 0.6),
            "stubbornness_gene": (0.7, 1.0),
            "prey_drive_gene":   (0.5, 0.8),
        },
        "abilities": {"guard": 0.35},
        "coat_colors": [(190, 75, 30), (235, 222, 192), (28, 22, 18)],
        "coat_pattern_weights": [100, 0, 0, 0, 0, 0],
        "ear_type": "erect",
        "tail_type": "curled",
        "coat_length": "long",
        "coat_type_weights": [0, 0, 100, 0],
    },
    "Jack Russell": {
        "biomes": {"temperate", "rolling_hills", "birch_forest"},
        "size_class": "small",
        "genes": {
            "speed_gene":        (1.0, 1.2),
            "endurance_gene":    (0.9, 1.1),
            "agility_gene":      (1.1, 1.3),
            "strength_gene":     (0.7, 0.9),
            "nose_gene":         (0.9, 1.2),
            "alertness_gene":    (1.0, 1.2),
            "loyalty_gene":      (0.6, 0.9),
            "playfulness_gene":  (0.8, 1.0),
            "stubbornness_gene": (0.5, 0.8),
            "prey_drive_gene":   (0.9, 1.2),
        },
        "abilities": {"tracking": 0.35},
        "coat_colors": [(248, 243, 232), (235, 222, 192)],
        "coat_pattern_weights": [0, 30, 0, 0, 50, 20],
        "ear_type": "semi-erect",
        "tail_type": "short",
        "coat_length": "short",
        "coat_type_weights": [80, 20, 0, 0],
    },
    "Rhodesian Ridgeback": {
        "biomes": {"savanna", "tropical", "wasteland", "arid_steppe"},
        "size_class": "large",
        "genes": {
            "speed_gene":        (1.1, 1.3),
            "endurance_gene":    (1.0, 1.2),
            "agility_gene":      (1.0, 1.2),
            "strength_gene":     (1.0, 1.2),
            "nose_gene":         (1.0, 1.2),
            "alertness_gene":    (1.0, 1.2),
            "loyalty_gene":      (0.7, 1.0),
            "playfulness_gene":  (0.5, 0.8),
            "stubbornness_gene": (0.4, 0.7),
            "prey_drive_gene":   (0.9, 1.2),
        },
        "abilities": {"tracking": 0.40, "guard": 0.30},
        "coat_colors": [(190, 75, 30), (205, 168, 55)],
        "coat_pattern_weights": [100, 0, 0, 0, 0, 0],
        "ear_type": "floppy",
        "tail_type": "long",
        "coat_length": "short",
        "coat_type_weights": [100, 0, 0, 0],
    },
    "Cane Corso": {
        "biomes": {"canyon", "temperate", "wasteland"},
        "size_class": "giant",
        "genes": {
            "speed_gene":        (0.8, 1.1),
            "endurance_gene":    (0.9, 1.2),
            "agility_gene":      (0.8, 1.0),
            "strength_gene":     (1.2, 1.3),
            "nose_gene":         (0.8, 1.1),
            "alertness_gene":    (1.0, 1.2),
            "loyalty_gene":      (0.8, 1.0),
            "playfulness_gene":  (0.3, 0.6),
            "stubbornness_gene": (0.4, 0.7),
            "prey_drive_gene":   (0.7, 1.0),
        },
        "abilities": {"guard": 0.60},
        "coat_colors": [(28, 22, 18), (95, 100, 115), (110, 58, 24)],
        "coat_pattern_weights": [50, 0, 0, 35, 15, 0],
        "ear_type": "floppy",
        "tail_type": "short",
        "coat_length": "short",
        "coat_type_weights": [100, 0, 0, 0],
    },
    "Bernese Mountain Dog": {
        "biomes": {"alpine_mountain", "rocky_mountain", "boreal", "redwood"},
        "size_class": "large",
        "genes": {
            "speed_gene":        (0.8, 1.1),
            "endurance_gene":    (1.0, 1.2),
            "agility_gene":      (0.8, 1.0),
            "strength_gene":     (1.0, 1.2),
            "nose_gene":         (0.8, 1.1),
            "alertness_gene":    (0.8, 1.1),
            "loyalty_gene":      (0.9, 1.0),
            "playfulness_gene":  (0.6, 0.9),
            "stubbornness_gene": (0.2, 0.5),
            "prey_drive_gene":   (0.5, 0.8),
        },
        "abilities": {"retrieve": 0.30},
        "coat_colors": [(28, 22, 18), (110, 58, 24)],
        "coat_pattern_weights": [0, 0, 0, 0, 80, 20],
        "ear_type": "floppy",
        "tail_type": "long",
        "coat_length": "long",
        "coat_type_weights": [60, 40, 0, 0],
    },
    "Whippet": {
        "biomes": {"steppe", "arid_steppe", "savanna"},
        "size_class": "medium",
        "genes": {
            "speed_gene":        (1.2, 1.3),
            "endurance_gene":    (0.8, 1.0),
            "agility_gene":      (1.1, 1.3),
            "strength_gene":     (0.7, 0.9),
            "nose_gene":         (0.7, 1.0),
            "alertness_gene":    (0.9, 1.1),
            "loyalty_gene":      (0.7, 1.0),
            "playfulness_gene":  (0.6, 0.9),
            "stubbornness_gene": (0.3, 0.6),
            "prey_drive_gene":   (0.8, 1.1),
        },
        "abilities": {},
        "coat_colors": [(28, 22, 18), (190, 75, 30), (95, 100, 115), (235, 222, 192)],
        "coat_pattern_weights": [20, 15, 10, 30, 15, 10],
        "ear_type": "semi-erect",
        "tail_type": "long",
        "coat_length": "short",
        "coat_type_weights": [100, 0, 0, 0],
    },
    "Basenji": {
        "biomes": {"jungle", "tropical", "savanna", "arid_steppe", "beach"},
        "size_class": "small",
        "genes": {
            "speed_gene":        (1.0, 1.2),
            "endurance_gene":    (0.9, 1.1),
            "agility_gene":      (1.0, 1.2),
            "strength_gene":     (0.7, 0.9),
            "nose_gene":         (1.1, 1.3),
            "alertness_gene":    (1.0, 1.2),
            "loyalty_gene":      (0.5, 0.8),
            "playfulness_gene":  (0.5, 0.8),
            "stubbornness_gene": (0.6, 0.9),
            "prey_drive_gene":   (0.9, 1.2),
        },
        "abilities": {"tracking": 0.50},
        "coat_colors": [(190, 75, 30), (205, 168, 55), (28, 22, 18)],
        "coat_pattern_weights": [30, 5, 0, 0, 30, 35],
        "ear_type": "erect",
        "tail_type": "curled",
        "coat_length": "short",
        "coat_type_weights": [100, 0, 0, 0],
    },
    "Saint Bernard": {
        "biomes": {"alpine_mountain", "tundra", "boreal"},
        "size_class": "giant",
        "genes": {
            "speed_gene":        (0.7, 0.9),
            "endurance_gene":    (1.1, 1.3),
            "agility_gene":      (0.7, 0.9),
            "strength_gene":     (1.2, 1.3),
            "nose_gene":         (0.9, 1.2),
            "alertness_gene":    (0.8, 1.1),
            "loyalty_gene":      (0.9, 1.0),
            "playfulness_gene":  (0.5, 0.8),
            "stubbornness_gene": (0.2, 0.5),
            "prey_drive_gene":   (0.4, 0.7),
        },
        "abilities": {"tracking": 0.35},
        "coat_colors": [(190, 75, 30), (205, 168, 55)],
        "coat_pattern_weights": [0, 0, 0, 0, 70, 30],
        "ear_type": "floppy",
        "tail_type": "long",
        "coat_length": "long",
        "coat_type_weights": [50, 50, 0, 0],
    },
}

# Reverse index: biome -> list of breeds that naturally spawn there
DOG_BIOME_MAP: dict = {}
for _breed_name, _profile in BREED_PROFILES.items():
    for _biome in _profile["biomes"]:
        DOG_BIOME_MAP.setdefault(_biome, []).append(_breed_name)


def derive_coat_color(base_color, dilute_expressed):
    """Return the RGB tuple for a given base_color + dilute combination."""
    key = (base_color, "dilute" if dilute_expressed else "full")
    return COLOR_RGB.get(key, COLOR_RGB[("yellow", "full")])


def expressed_color_name(base_color, dilute_expressed):
    """Return the human-readable color name."""
    key = (base_color, "dilute" if dilute_expressed else "full")
    return COLOR_NAMES.get(key, base_color.title())


def _pick_categorical(order, weights):
    """Pick a random categorical value using weights parallel to order."""
    opts = [o for o, w in zip(order, weights) if w > 0]
    wts  = [w for w in weights if w > 0]
    if not opts:
        return order[0]
    return random.choices(opts, weights=wts)[0]


class Dog(Animal):
    ANIMAL_W = 28
    ANIMAL_H = 18
    PREFERRED_FOODS = ("bone", "raw_meat", "dog_treat", "carrot")
    MEAT_DROP = (None, 0)  # dogs cannot be hunted

    def __init__(self, x, y, world, breed=None):
        super().__init__(x, y, world, "dog")

        self._breed_cooldown = 9999.0  # only breed via kennel
        self.stay_mode = False
        self._flee_timer = 0.0
        self._tracking_hint = False
        self._tracking_hint_timer = 0.0

        bx = int(float(x) // BLOCK_SIZE)
        biodome = world.biodome_at(bx) if world is not None else "temperate"

        if breed is None:
            eligible = DOG_BIOME_MAP.get(biodome, list(BREED_PROFILES.keys()))
            breed = random.choice(eligible) if eligible else "Labrador"

        profile = BREED_PROFILES.get(breed, BREED_PROFILES["Labrador"])

        self.traits["breed"]          = breed
        self.traits["generation"]     = 1
        self.traits["collar_applied"] = False
        self.traits["dog_name"]       = None
        self.traits["size_class"]     = profile["size_class"]
        self.traits["ear_type"]       = profile.get("ear_type", "floppy")
        self.traits["tail_type"]      = profile.get("tail_type", "long")
        self.traits["coat_length"]    = profile.get("coat_length", "short")
        self.traits["coat_color"]     = (160, 100, 50)  # placeholder; overwritten by genotype
        self.traits["base_color"]     = "yellow"        # placeholder; overwritten by genotype
        self.traits["dilute_expressed"] = False
        self.traits["dilute_carrier"]   = False
        self.traits["white_spotting"]   = "solid"
        self.traits["eye_color"]      = random.choices(
            ["brown", "amber", "blue", "heterochromia"], weights=[55, 30, 12, 3]
        )[0]

        self._init_dog_genotype(profile)

    def _init_dog_genotype(self, profile):
        genes = profile["genes"]
        for gene_key, (lo, hi) in genes.items():
            self.genotype[gene_key] = [
                round(random.uniform(lo, hi), 3),
                round(random.uniform(lo, hi), 3),
            ]

        # Categorical visual genes
        ctw = profile.get("coat_type_weights", [100, 0, 0, 0])
        cpw = profile.get("coat_pattern_weights", [100, 0, 0, 0, 0, 0])
        for gene_key, order, weights in [
            ("coat_pattern_gene", DOG_COAT_PATTERN_ORDER, cpw),
            ("coat_type_gene",    DOG_COAT_TYPE_ORDER,    ctw),
        ]:
            val = _pick_categorical(order, weights)
            self.genotype[gene_key] = [val, val]

        ear_val  = profile.get("ear_type", "floppy")
        tail_val = profile.get("tail_type", "long")
        len_val  = profile.get("coat_length", "short")
        self.genotype["ear_type_gene"]  = [ear_val, ear_val]
        self.genotype["tail_type_gene"] = [tail_val, tail_val]
        self.genotype["coat_length_gene"] = [len_val, len_val]
        self.genotype["eye_color_gene"] = [
            random.choices(["brown","amber","blue","heterochromia"], weights=[55,30,12,3])[0],
            random.choices(["brown","amber","blue","heterochromia"], weights=[55,30,12,3])[0],
        ]
        self.genotype["size_class_gene"] = [
            profile["size_class"], profile["size_class"]
        ]

        # Color genetics
        cg = _BREED_COLOR_GENES.get(self.traits.get("breed", "Labrador"), _BREED_COLOR_GENES.get("Labrador",
            {"base": [20,20,20,20,20], "dilute": 0.15, "spotting": [60,20,15,5]}))
        base_a = random.choices(BASE_COLOR_ORDER, weights=cg["base"])[0]
        base_b = random.choices(BASE_COLOR_ORDER, weights=cg["base"])[0]
        self.genotype["base_color_gene"] = [base_a, base_b]
        dp = cg["dilute"]
        self.genotype["dilute_gene"] = [
            "dilute" if random.random() < dp else "full",
            "dilute" if random.random() < dp else "full",
        ]
        sw = cg["spotting"]
        spot_a = random.choices(WHITE_SPOTTING_ORDER, weights=sw)[0]
        spot_b = random.choices(WHITE_SPOTTING_ORDER, weights=sw)[0]
        self.genotype["white_spotting_gene"] = [spot_a, spot_b]

        # Recessive ability genes
        ability_probs = profile.get("abilities", {})
        for ability in ("tracking", "herding", "guard", "retrieve"):
            prob = ability_probs.get(ability, 0.05)
            self.genotype[f"{ability}_gene"] = [
                ability if random.random() < prob else None,
                ability if random.random() < prob else None,
            ]

        self._apply_genotype_to_traits()

    def _apply_genotype_to_traits(self):
        super()._apply_genotype_to_traits()

        # Float performance / temperament genes
        float_genes = [
            ("speed_gene",        "speed",        0.7, 1.3),
            ("endurance_gene",    "endurance",     0.7, 1.3),
            ("agility_gene",      "agility",       0.7, 1.3),
            ("strength_gene",     "strength",      0.7, 1.3),
            ("nose_gene",         "nose",          0.7, 1.3),
            ("alertness_gene",    "alertness",     0.7, 1.3),
            ("loyalty_gene",      "loyalty",       0.0, 1.0),
            ("playfulness_gene",  "playfulness",   0.0, 1.0),
            ("stubbornness_gene", "stubbornness",  0.0, 1.0),
            ("prey_drive_gene",   "prey_drive",    0.0, 1.0),
        ]
        for gene_key, trait_key, lo, hi in float_genes:
            if gene_key in self.genotype:
                avg = sum(self.genotype[gene_key]) / 2
                self.traits[trait_key] = round(max(lo, min(hi, avg)), 3)

        # Categorical visual genes
        cat_genes = [
            ("coat_pattern_gene", "coat_pattern", DOG_COAT_PATTERN_ORDER),
            ("coat_length_gene",  "coat_length",  DOG_COAT_LENGTH_ORDER),
            ("coat_type_gene",    "coat_type",    DOG_COAT_TYPE_ORDER),
            ("ear_type_gene",     "ear_type",     DOG_EAR_TYPE_ORDER),
            ("tail_type_gene",    "tail_type",    DOG_TAIL_TYPE_ORDER),
            ("eye_color_gene",    "eye_color",    DOG_EYE_COLOR_ORDER),
            ("size_class_gene",   "size_class",   DOG_SIZE_CLASS_ORDER),
        ]
        for gene_key, trait_key, order in cat_genes:
            if gene_key in self.genotype:
                self.traits[trait_key] = _expressed_categorical(
                    self.genotype[gene_key], order
                )

        # Recessive ability expression (both alleles must match)
        for ability in ("tracking", "herding", "guard", "retrieve"):
            a, b = self.genotype.get(f"{ability}_gene", [None, None])
            self.traits[f"has_{ability}"] = (a == ability and b == ability)

        # Dominant color genetics
        if "base_color_gene" in self.genotype:
            base = _expressed_categorical(self.genotype["base_color_gene"], BASE_COLOR_ORDER)
            self.traits["base_color"] = base
        if "dilute_gene" in self.genotype:
            a, b = self.genotype["dilute_gene"]
            dilute_expressed = (a == "dilute" and b == "dilute")
            self.traits["dilute_expressed"] = dilute_expressed
            self.traits["dilute_carrier"]   = (a == "dilute" or b == "dilute")
        if "white_spotting_gene" in self.genotype:
            self.traits["white_spotting"] = _expressed_categorical(
                self.genotype["white_spotting_gene"], WHITE_SPOTTING_ORDER
            )
        # Derive coat_color RGB from genetics when both genes are present
        if "base_color" in self.traits and "dilute_expressed" in self.traits:
            self.traits["coat_color"] = derive_coat_color(
                self.traits["base_color"], self.traits["dilute_expressed"]
            )

    def _synthesize_genotype_from_traits(self):
        super()._synthesize_genotype_from_traits()
        float_genes = [
            ("speed_gene",        "speed",        0.7, 1.3),
            ("endurance_gene",    "endurance",     0.7, 1.3),
            ("agility_gene",      "agility",       0.7, 1.3),
            ("strength_gene",     "strength",      0.7, 1.3),
            ("nose_gene",         "nose",          0.7, 1.3),
            ("alertness_gene",    "alertness",     0.7, 1.3),
            ("loyalty_gene",      "loyalty",       0.0, 1.0),
            ("playfulness_gene",  "playfulness",   0.0, 1.0),
            ("stubbornness_gene", "stubbornness",  0.0, 1.0),
            ("prey_drive_gene",   "prey_drive",    0.0, 1.0),
        ]
        for gene_key, trait_key, lo, hi in float_genes:
            v = self.traits.get(trait_key, (lo + hi) / 2)
            noise = random.uniform(-0.04, 0.04)
            self.genotype[gene_key] = [
                round(max(lo, min(hi, v + noise)), 3),
                round(max(lo, min(hi, v - noise)), 3),
            ]
        for gene_key, trait_key in [
            ("coat_pattern_gene", "coat_pattern"),
            ("coat_length_gene",  "coat_length"),
            ("coat_type_gene",    "coat_type"),
            ("ear_type_gene",     "ear_type"),
            ("tail_type_gene",    "tail_type"),
            ("eye_color_gene",    "eye_color"),
            ("size_class_gene",   "size_class"),
        ]:
            v = self.traits.get(trait_key, "")
            if v:
                self.genotype[gene_key] = [v, v]
        for ability in ("tracking", "herding", "guard", "retrieve"):
            has = self.traits.get(f"has_{ability}", False)
            self.genotype[f"{ability}_gene"] = [ability, ability] if has else [None, None]
        # Color genes — synthesize from saved traits or default to closest named color
        base = self.traits.get("base_color", "yellow")
        if base not in BASE_COLOR_ORDER:
            base = "yellow"
        self.genotype["base_color_gene"] = [base, base]
        dilute = self.traits.get("dilute_expressed", False)
        self.genotype["dilute_gene"] = ["dilute", "dilute"] if dilute else ["full", "full"]
        spot = self.traits.get("white_spotting", "solid")
        if spot not in WHITE_SPOTTING_ORDER:
            spot = "solid"
        self.genotype["white_spotting_gene"] = [spot, spot]

    # ------------------------------------------------------------------
    # Non-killable
    # ------------------------------------------------------------------

    def try_harvest(self, player, dt):
        self._flee_timer = max(self._flee_timer, 3.0)
        self.reset_harvest()
        return None

    def _try_harvest_resource(self, player, dt):
        return None

    # ------------------------------------------------------------------
    # Taming
    # ------------------------------------------------------------------

    def try_feed(self, player):
        if self.tamed:
            return False
        item_id = player.hotbar[player.selected_slot]
        if not item_id:
            return False

        progress_gain = 0
        if item_id == "dog_treat":
            if player.inventory.get("dog_treat", 0) <= 0:
                return False
            player.inventory["dog_treat"] -= 1
            if player.inventory["dog_treat"] <= 0:
                del player.inventory["dog_treat"]
                for i in range(HOTBAR_SIZE):
                    if player.hotbar[i] == "dog_treat":
                        player.hotbar[i] = None
                        break
            progress_gain = 2
        elif item_id in self.PREFERRED_FOODS:
            if player.inventory.get(item_id, 0) <= 0:
                return False
            player.inventory[item_id] -= 1
            if player.inventory[item_id] <= 0:
                del player.inventory[item_id]
                for i in range(HOTBAR_SIZE):
                    if player.hotbar[i] == item_id:
                        player.hotbar[i] = None
                        break
            progress_gain = 1
        else:
            return False

        self.tame_progress += progress_gain

        stubbornness = self.traits.get("stubbornness", 0.5)
        threshold = int(5 + stubbornness * 7)
        threshold -= getattr(player, "dog_whisperer_bonus", 0)
        threshold = max(1, threshold)

        if self.tame_progress >= threshold:
            # Consume one collar from inventory
            if player.inventory.get("dog_collar", 0) <= 0:
                # No collar — progress stalls at threshold - 1
                self.tame_progress = threshold - 1
                player.pending_notifications.append(
                    ("Dogs", "Need a Dog Collar to complete taming!", None)
                )
                return True
            player.inventory["dog_collar"] -= 1
            if player.inventory["dog_collar"] <= 0:
                del player.inventory["dog_collar"]
                for i in range(HOTBAR_SIZE):
                    if player.hotbar[i] == "dog_collar":
                        player.hotbar[i] = None
                        break
            self.tamed = True
            self.traits["collar_applied"] = True
            player.dogs_tamed = getattr(player, "dogs_tamed", 0) + 1
            breed = self.traits.get("breed", "Mixed")
            disc = getattr(player, "discovered_dog_breeds", set())
            disc.add(breed)
            player.discovered_dog_breeds = disc
            spd = self.traits.get("speed", 1.0)
            nose = self.traits.get("nose", 1.0)
            records = getattr(player, "dog_records", {})
            if spd > records.get("best_speed", 0.0):
                records["best_speed"] = spd
            if nose > records.get("best_nose", 0.0):
                records["best_nose"] = nose
            player.dog_records = records
        return True

    # ------------------------------------------------------------------
    # Breeding — only via kennel UI
    # ------------------------------------------------------------------

    def _breed(self, other, world):
        self._breed_cooldown = 9999.0

    def breed_with(self, other, world, player):
        """Player-triggered breeding at a kennel. Returns offspring or None."""
        if self.no_breed or other.no_breed:
            return None
        if not (self.tamed and other.tamed):
            return None
        if not (self._kennel_nearby(world) or other._kennel_nearby(world)):
            return None

        ox = (self.x + other.x) / 2
        oy = (self.y + other.y) / 2
        # Create offspring without breed argument — we'll set it manually
        offspring = Dog(ox, oy, world, breed=self.traits.get("breed", "Mixed"))

        # Mendelian allele inheritance
        offspring._inherit_genotype(self, other)

        # Coat color is derived from the inherited base_color/dilute/white_spotting genes
        # (already applied by _inherit_genotype → _apply_genotype_to_traits above)

        # Breed purity
        breed_a = self.traits.get("breed", "Mixed")
        breed_b = other.traits.get("breed", "Mixed")
        if breed_a == breed_b and "Mixed" not in breed_a:
            offspring.traits["breed"] = breed_a
            # pure_breed_bonus: +0.05 on characteristic stat
            if getattr(player, "pure_breed_bonus", False):
                _boost_pure_breed(offspring, breed_a)
        else:
            a_short = breed_a.split()[0]
            b_short = breed_b.split()[0]
            mixed_name = f"Mixed ({a_short}/{b_short})"
            offspring.traits["breed"] = mixed_name[:24]

        # Generation
        gen_a = self.traits.get("generation", 1)
        gen_b = other.traits.get("generation", 1)
        offspring.traits["generation"] = max(gen_a, gen_b) + 1

        # Ability genes with advanced_genetics bonus
        ability_bonus = getattr(player, "dog_ability_chance", 0.0)
        for ability in ("tracking", "herding", "guard", "retrieve"):
            gene = f"{ability}_gene"
            a_alleles = self.genotype.get(gene, [None, None])
            b_alleles = other.genotype.get(gene, [None, None])
            child_a = random.choice(a_alleles)
            child_b = random.choice(b_alleles)
            if ability_bonus > 0 and (child_a == ability or child_b == ability):
                if random.random() < ability_bonus:
                    child_a = ability
            offspring.genotype[gene] = [child_a, child_b]

        offspring.traits["collar_applied"] = True
        offspring.parent_a_uid = self.uid
        offspring.parent_b_uid = other.uid
        offspring.tamed = True
        offspring._breed_cooldown = 9999.0

        self._breed_cooldown  = 1200.0
        other._breed_cooldown = 1200.0
        world.entities.append(offspring)

        if player:
            player.dogs_bred = getattr(player, "dogs_bred", 0) + 1
            spd = offspring.traits.get("speed", 1.0)
            nose = offspring.traits.get("nose", 1.0)
            records = getattr(player, "dog_records", {})
            if spd > records.get("best_speed", 0.0):
                records["best_speed"] = spd
            if nose > records.get("best_nose", 0.0):
                records["best_nose"] = nose
            player.dog_records = records
            breed = offspring.traits.get("breed", "Mixed")
            disc = getattr(player, "discovered_dog_breeds", set())
            disc.add(breed)
            player.discovered_dog_breeds = disc

        return offspring

    def _kennel_nearby(self, world):
        from blocks import KENNEL_BLOCK
        cx = int((self.x + self.W / 2) // BLOCK_SIZE)
        cy = int((self.y + self.H / 2) // BLOCK_SIZE)
        for dx in range(-KENNEL_SEARCH_RADIUS, KENNEL_SEARCH_RADIUS + 1):
            for dy in range(-KENNEL_SEARCH_RADIUS, KENNEL_SEARCH_RADIUS + 1):
                if world.get_block(cx + dx, cy + dy) == KENNEL_BLOCK:
                    return True
        return False

    def in_range_stay_toggle(self, player, radius=8):
        """True if player is within radius blocks."""
        acx = (self.x + self.W / 2) / BLOCK_SIZE
        acy = (self.y + self.H / 2) / BLOCK_SIZE
        pcx = (player.x + PLAYER_W / 2) / BLOCK_SIZE
        pcy = (player.y + PLAYER_H / 2) / BLOCK_SIZE
        return ((acx - pcx) ** 2 + (acy - pcy) ** 2) ** 0.5 <= radius

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------

    def update(self, dt):
        if self.dead:
            return

        # Keep breed cooldown from auto-triggering base class breed
        if self._breed_cooldown < 9999.0:
            self._breed_cooldown -= dt
            if self._breed_cooldown < 0:
                self._breed_cooldown = 0.0
        else:
            # Suppress base class auto-breeding entirely
            pass

        # Flee when harmed
        if self._flee_timer > 0:
            self._flee_timer -= dt
            self.vx = self.facing * DOG_FLEE_SPEED
            self.vy = min(self.vy + GRAVITY, MAX_FALL)
            self._move_x(self.vx)
            self._move_y(self.vy)
            return

        # Wild dog flees from player
        if not self.tamed:
            player = getattr(self.world, '_player_ref', None)
            if player is not None:
                pdx = (player.x + PLAYER_W / 2) - (self.x + self.W / 2)
                pdy = (player.y + PLAYER_H / 2) - (self.y + self.H / 2)
                dist = ((pdx / BLOCK_SIZE) ** 2 + (pdy / BLOCK_SIZE) ** 2) ** 0.5
                if dist < DOG_FLEE_RADIUS:
                    self.vx = (-1 if pdx > 0 else 1) * DOG_FLEE_SPEED
                    self.facing = 1 if self.vx > 0 else -1
                    self.vy = min(self.vy + GRAVITY, MAX_FALL)
                    self._move_x(self.vx)
                    self._move_y(self.vy)
                    return

        # Stay mode: sit still
        if self.stay_mode and self.tamed:
            self.vx = 0.0
            self.vy = min(self.vy + GRAVITY, MAX_FALL)
            self._move_y(self.vy)
            # Tracking hint check while staying
            self._update_tracking_hint(dt)
            return

        # Tamed: follow player with loyalty-scaled follow distance
        if self.tamed:
            player = getattr(self.world, '_player_ref', None)
            if player is not None:
                pdx = (player.x + PLAYER_W / 2) - (self.x + self.W / 2)
                pdy = (player.y + PLAYER_H / 2) - (self.y + self.H / 2)
                dist = ((pdx / BLOCK_SIZE) ** 2 + (pdy / BLOCK_SIZE) ** 2) ** 0.5
                loyalty = self.traits.get("loyalty", 0.5)
                follow_dist = 2.0 + (1.0 - loyalty) * 3.0
                if dist > follow_dist:
                    self.vx = DOG_MOVE_SPEED * (1 if pdx > 0 else -1)
                    self.facing = 1 if self.vx > 0 else -1
                else:
                    self.vx = 0.0
                if self._in_water():
                    self.vy = min(self.vy + GRAVITY * 0.2, 2.5)
                    self.vx *= 0.8
                else:
                    self.vy = min(self.vy + GRAVITY, MAX_FALL)
                self._move_x(self.vx)
                self._move_y(self.vy)
                self._update_tracking_hint(dt)
                return

        # Wander
        self._wander_timer -= dt
        if self._wander_timer <= 0:
            self._wander_timer = random.uniform(1.5, 5.0)
            self._wander_dir = random.choice([-1, -1, 0, 0, 0, 1, 1])

        self.vx = self._wander_dir * DOG_MOVE_SPEED
        if self.vx != 0:
            self.facing = 1 if self.vx > 0 else -1

        if self._in_water():
            self.vy = min(self.vy + GRAVITY * 0.2, 2.5)
            self.vx *= 0.8
        else:
            self.vy = min(self.vy + GRAVITY, MAX_FALL)
        self._move_x(self.vx)
        self._move_y(self.vy)

    def _update_tracking_hint(self, dt):
        if not self.traits.get("has_tracking", False):
            return
        self._tracking_hint_timer -= dt
        if self._tracking_hint_timer > 0:
            return
        self._tracking_hint_timer = 5.0
        # Check for ore blocks nearby
        if self.world is None:
            return
        cx = int((self.x + self.W / 2) // BLOCK_SIZE)
        cy = int((self.y + self.H / 2) // BLOCK_SIZE)
        from blocks import RESOURCE_BLOCKS as ORE_BLOCKS
        for ddx in range(-3, 4):
            for ddy in range(-3, 4):
                bid = self.world.get_block(cx + ddx, cy + ddy)
                if bid in ORE_BLOCKS:
                    self._tracking_hint = True
                    return


_PACK_VISUAL_GENES = {
    "base_color_gene", "dilute_gene", "white_spotting_gene",
    "coat_pattern_gene", "coat_type_gene", "coat_length_gene",
}

def _blend_to_pack_template(dog, alpha):
    """Shift a pack member's float genes ~60% toward the alpha's and copy visual genes for family resemblance."""
    for gene_key, a_vals in alpha.genotype.items():
        if gene_key not in dog.genotype:
            continue
        d_vals = dog.genotype[gene_key]
        if gene_key in _PACK_VISUAL_GENES:
            dog.genotype[gene_key] = list(a_vals)
        elif isinstance(d_vals[0], float):
            dog.genotype[gene_key] = [
                round(0.6 * a + 0.4 * d, 3)
                for a, d in zip(a_vals, d_vals)
            ]
    dog._apply_genotype_to_traits()


def _boost_pure_breed(offspring, breed):
    """Apply +0.05 to a breed's most characteristic float trait."""
    char_trait = {
        "Border Collie":      "agility",
        "Husky":              "endurance",
        "Greyhound":          "speed",
        "Bloodhound":         "nose",
        "German Shepherd":    "alertness",
        "Labrador":           "playfulness",
        "Dalmatian":          "endurance",
        "Beagle":             "nose",
        "Poodle":             "agility",
        "Bulldog":            "strength",
        "Malamute":           "strength",
        "Vizsla":             "speed",
        "Australian Shepherd":"agility",
        "Dachshund":          "nose",
        "Setter":             "speed",
        "Akita":              "strength",
        "Rottweiler":         "strength",
        "Samoyed":            "endurance",
        "Shiba Inu":          "alertness",
        "Great Pyrenees":     "strength",
        "Weimaraner":         "nose",
        "Doberman":           "speed",
        "Chow Chow":          "alertness",
        "Jack Russell":       "agility",
        "Rhodesian Ridgeback":"speed",
        "Cane Corso":         "strength",
        "Bernese Mountain Dog":"loyalty",
        "Whippet":            "speed",
        "Basenji":            "nose",
        "Saint Bernard":      "endurance",
    }.get(breed)
    if char_trait and char_trait in offspring.traits:
        offspring.traits[char_trait] = round(
            min(1.3, offspring.traits[char_trait] + 0.05), 3
        )
