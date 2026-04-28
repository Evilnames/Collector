import math
import random
import hashlib
import pygame
from dataclasses import dataclass


@dataclass
class Seashell:
    uid: str
    species: str
    rarity: str
    depth_zone: str   # "tidal" | "reef"
    color: tuple
    pattern: str
    size_cm: float
    biome_found: str
    seed: int


# ---------------------------------------------------------------------------
# Species definitions
# ---------------------------------------------------------------------------

SHELL_TYPES = {
    # ── Tidal (7 species) ──────────────────────────────────────────────────
    "cowrie": {
        "depth_zone":  "tidal",
        "rarity_pool": ["common", "common", "uncommon"],
        "color_pool":  [(235, 210, 180), (220, 180, 140), (200, 165, 120)],
        "patterns":    ["spotted", "banded", "solid"],
        "size_range":  (1.5, 4.0),
        "shape":       "oval",
    },
    "cone": {
        "depth_zone":  "tidal",
        "rarity_pool": ["common", "uncommon"],
        "color_pool":  [(210, 185, 150), (195, 160, 115), (225, 200, 165)],
        "patterns":    ["spotted", "banded", "spotted"],
        "size_range":  (2.0, 6.0),
        "shape":       "cone",
    },
    "scallop": {
        "depth_zone":  "tidal",
        "rarity_pool": ["common", "common", "uncommon"],
        "color_pool":  [(230, 140, 100), (215, 120, 80), (245, 160, 120)],
        "patterns":    ["ribbed", "solid", "ribbed"],
        "size_range":  (3.0, 8.0),
        "shape":       "fan",
    },
    "clam": {
        "depth_zone":  "tidal",
        "rarity_pool": ["common"],
        "color_pool":  [(220, 215, 205), (200, 195, 185), (235, 228, 220)],
        "patterns":    ["solid", "banded", "solid"],
        "size_range":  (2.0, 7.0),
        "shape":       "oval",
    },
    "periwinkle": {
        "depth_zone":  "tidal",
        "rarity_pool": ["common"],
        "color_pool":  [(120, 125, 140), (100, 105, 120), (135, 140, 155)],
        "patterns":    ["solid", "spiral", "solid"],
        "size_range":  (0.8, 2.5),
        "shape":       "spiral",
    },
    "limpet": {
        "depth_zone":  "tidal",
        "rarity_pool": ["common", "uncommon"],
        "color_pool":  [(180, 170, 145), (160, 148, 125), (195, 185, 160)],
        "patterns":    ["ribbed", "solid", "ribbed"],
        "size_range":  (1.5, 5.0),
        "shape":       "cone",
    },
    "whelk": {
        "depth_zone":  "tidal",
        "rarity_pool": ["uncommon"],
        "color_pool":  [(200, 175, 140), (185, 158, 125), (215, 190, 155)],
        "patterns":    ["spiral", "ribbed", "spiral"],
        "size_range":  (3.0, 9.0),
        "shape":       "spiral",
    },
    # ── Reef (8 species) ───────────────────────────────────────────────────
    "oyster": {
        "depth_zone":  "reef",
        "rarity_pool": ["common", "uncommon"],
        "color_pool":  [(145, 140, 130), (125, 120, 110), (160, 155, 145)],
        "patterns":    ["layered", "solid", "layered"],
        "size_range":  (5.0, 15.0),
        "shape":       "oval",
    },
    "abalone": {
        "depth_zone":  "reef",
        "rarity_pool": ["uncommon", "rare"],
        "color_pool":  [(120, 195, 185), (100, 175, 165), (140, 210, 200)],
        "patterns":    ["iridescent", "spiral", "iridescent"],
        "size_range":  (6.0, 18.0),
        "shape":       "oval",
    },
    "murex": {
        "depth_zone":  "reef",
        "rarity_pool": ["uncommon", "rare"],
        "color_pool":  [(195, 160, 140), (175, 140, 120), (210, 178, 158)],
        "patterns":    ["spined", "ribbed", "spined"],
        "size_range":  (4.0, 12.0),
        "shape":       "spiral",
    },
    "nautilus": {
        "depth_zone":  "reef",
        "rarity_pool": ["rare", "epic"],
        "color_pool":  [(240, 230, 215), (220, 210, 195), (255, 245, 230)],
        "patterns":    ["banded", "spiral", "banded"],
        "size_range":  (8.0, 20.0),
        "shape":       "coiled",
    },
    "triton": {
        "depth_zone":  "reef",
        "rarity_pool": ["rare"],
        "color_pool":  [(210, 175, 130), (190, 155, 112), (225, 190, 148)],
        "patterns":    ["spiral", "ribbed", "spiral"],
        "size_range":  (10.0, 25.0),
        "shape":       "spiral",
    },
    "volute": {
        "depth_zone":  "reef",
        "rarity_pool": ["rare", "epic"],
        "color_pool":  [(225, 145, 80), (205, 125, 65), (240, 165, 100)],
        "patterns":    ["spotted", "banded", "spotted"],
        "size_range":  (5.0, 15.0),
        "shape":       "oval",
    },
    "turritella": {
        "depth_zone":  "reef",
        "rarity_pool": ["uncommon"],
        "color_pool":  [(160, 140, 110), (142, 122, 95), (175, 155, 125)],
        "patterns":    ["spiral", "ribbed", "spiral"],
        "size_range":  (3.0, 8.0),
        "shape":       "cone",
    },
    "marginella": {
        "depth_zone":  "reef",
        "rarity_pool": ["rare", "epic"],
        "color_pool":  [(240, 200, 180), (220, 180, 160), (255, 218, 198)],
        "patterns":    ["spotted", "solid", "spotted"],
        "size_range":  (1.0, 3.0),
        "shape":       "oval",
    },
    # ── Tidal additions ───────────────────────────────────────────────────────
    "sundial": {
        "depth_zone":  "tidal",
        "rarity_pool": ["uncommon", "rare", "rare"],
        "color_pool":  [(210, 195, 155), (195, 178, 135), (225, 210, 170)],
        "patterns":    ["spiral", "ribbed", "spiral"],
        "size_range":  (2.0, 6.0),
        "shape":       "spiral",
    },
    "top_shell": {
        "depth_zone":  "tidal",
        "rarity_pool": ["common", "uncommon"],
        "color_pool":  [(80, 160, 140), (100, 180, 155), (60, 145, 125)],
        "patterns":    ["spiral", "banded", "solid"],
        "size_range":  (1.5, 4.5),
        "shape":       "cone",
    },
    "nerite": {
        "depth_zone":  "tidal",
        "rarity_pool": ["common"],
        "color_pool":  [(40, 40, 40), (55, 50, 45), (30, 30, 35)],
        "patterns":    ["banded", "solid", "spotted"],
        "size_range":  (0.8, 2.0),
        "shape":       "oval",
    },
    "tellin": {
        "depth_zone":  "tidal",
        "rarity_pool": ["common", "uncommon"],
        "color_pool":  [(245, 195, 195), (230, 175, 175), (255, 210, 210)],
        "patterns":    ["solid", "banded", "layered"],
        "size_range":  (2.0, 6.0),
        "shape":       "oval",
    },
    "auger": {
        "depth_zone":  "tidal",
        "rarity_pool": ["uncommon"],
        "color_pool":  [(175, 140, 105), (158, 125, 92), (190, 155, 120)],
        "patterns":    ["spiral", "ribbed", "spotted"],
        "size_range":  (3.0, 7.0),
        "shape":       "cone",
    },
    "cockle": {
        "depth_zone":  "tidal",
        "rarity_pool": ["common", "common", "uncommon"],
        "color_pool":  [(215, 185, 110), (200, 168, 95), (228, 198, 125)],
        "patterns":    ["ribbed", "solid", "ribbed"],
        "size_range":  (2.0, 5.5),
        "shape":       "fan",
    },
    "moon_snail": {
        "depth_zone":  "tidal",
        "rarity_pool": ["uncommon"],
        "color_pool":  [(195, 180, 155), (170, 158, 140), (145, 165, 185)],
        "patterns":    ["banded", "solid", "coiled"],
        "size_range":  (3.0, 8.0),
        "shape":       "coiled",
    },
    "olive": {
        "depth_zone":  "tidal",
        "rarity_pool": ["uncommon", "rare"],
        "color_pool":  [(110, 130, 80), (95, 115, 68), (125, 145, 95)],
        "patterns":    ["banded", "spiral", "solid"],
        "size_range":  (2.0, 5.5),
        "shape":       "oval",
    },
    "bubble_shell": {
        "depth_zone":  "tidal",
        "rarity_pool": ["uncommon"],
        "color_pool":  [(240, 238, 232), (225, 222, 215), (252, 248, 244)],
        "patterns":    ["solid", "banded", "iridescent"],
        "size_range":  (0.5, 2.0),
        "shape":       "oval",
    },
    "horn_shell": {
        "depth_zone":  "tidal",
        "rarity_pool": ["common"],
        "color_pool":  [(80, 65, 50), (95, 78, 62), (65, 52, 40)],
        "patterns":    ["solid", "ribbed", "spiral"],
        "size_range":  (2.0, 6.0),
        "shape":       "cone",
    },
    "ark_shell": {
        "depth_zone":  "tidal",
        "rarity_pool": ["common"],
        "color_pool":  [(165, 155, 135), (148, 138, 120), (178, 168, 148)],
        "patterns":    ["ribbed", "solid", "ribbed"],
        "size_range":  (3.0, 8.0),
        "shape":       "fan",
    },
    "jingle_shell": {
        "depth_zone":  "tidal",
        "rarity_pool": ["uncommon"],
        "color_pool":  [(220, 185, 80), (205, 168, 65), (235, 200, 95)],
        "patterns":    ["iridescent", "solid", "ribbed"],
        "size_range":  (1.5, 4.0),
        "shape":       "fan",
    },
    "blue_mussel": {
        "depth_zone":  "tidal",
        "rarity_pool": ["common"],
        "color_pool":  [(60, 70, 110), (45, 55, 95), (75, 85, 125)],
        "patterns":    ["solid", "banded", "layered"],
        "size_range":  (3.0, 7.0),
        "shape":       "oval",
    },
    "coquina": {
        "depth_zone":  "tidal",
        "rarity_pool": ["common"],
        "color_pool":  [(215, 130, 90), (180, 200, 100), (140, 170, 215)],
        "patterns":    ["banded", "ribbed", "solid"],
        "size_range":  (0.5, 1.5),
        "shape":       "fan",
    },
    "keyhole_limpet": {
        "depth_zone":  "tidal",
        "rarity_pool": ["common", "uncommon"],
        "color_pool":  [(155, 150, 140), (138, 133, 123), (168, 163, 153)],
        "patterns":    ["ribbed", "solid", "layered"],
        "size_range":  (2.0, 6.0),
        "shape":       "cone",
    },
    "slipper_shell": {
        "depth_zone":  "tidal",
        "rarity_pool": ["common"],
        "color_pool":  [(225, 210, 180), (210, 195, 165), (240, 225, 195)],
        "patterns":    ["layered", "solid", "layered"],
        "size_range":  (1.5, 5.0),
        "shape":       "cone",
    },
    "nutmeg": {
        "depth_zone":  "tidal",
        "rarity_pool": ["uncommon"],
        "color_pool":  [(200, 170, 125), (185, 155, 110), (215, 185, 140)],
        "patterns":    ["spotted", "ribbed", "spotted"],
        "size_range":  (1.5, 4.0),
        "shape":       "cone",
    },
    "pelican_foot": {
        "depth_zone":  "tidal",
        "rarity_pool": ["rare"],
        "color_pool":  [(210, 180, 145), (195, 165, 132), (225, 195, 160)],
        "patterns":    ["ribbed", "spiral", "solid"],
        "size_range":  (2.5, 5.5),
        "shape":       "spiral",
    },
    "dove_shell": {
        "depth_zone":  "tidal",
        "rarity_pool": ["common"],
        "color_pool":  [(235, 220, 200), (215, 195, 175), (250, 235, 215)],
        "patterns":    ["solid", "spotted", "banded"],
        "size_range":  (0.5, 1.5),
        "shape":       "oval",
    },
    "turban": {
        "depth_zone":  "tidal",
        "rarity_pool": ["uncommon"],
        "color_pool":  [(55, 90, 65), (70, 110, 80), (40, 75, 55)],
        "patterns":    ["spiral", "solid", "ribbed"],
        "size_range":  (2.0, 6.0),
        "shape":       "coiled",
    },
    "cerith": {
        "depth_zone":  "tidal",
        "rarity_pool": ["common"],
        "color_pool":  [(105, 85, 65), (88, 70, 52), (120, 100, 78)],
        "patterns":    ["spiral", "ribbed", "spotted"],
        "size_range":  (1.0, 4.0),
        "shape":       "cone",
    },
    "violet_snail": {
        "depth_zone":  "tidal",
        "rarity_pool": ["rare"],
        "color_pool":  [(130, 80, 185), (115, 65, 168), (145, 95, 200)],
        "patterns":    ["solid", "banded", "spiral"],
        "size_range":  (1.5, 4.0),
        "shape":       "spiral",
    },
    "nassa": {
        "depth_zone":  "tidal",
        "rarity_pool": ["common"],
        "color_pool":  [(150, 130, 100), (135, 115, 88), (165, 145, 115)],
        "patterns":    ["ribbed", "spotted", "banded"],
        "size_range":  (1.0, 3.0),
        "shape":       "spiral",
    },
    "carrier_shell": {
        "depth_zone":  "tidal",
        "rarity_pool": ["uncommon"],
        "color_pool":  [(175, 165, 140), (158, 148, 125), (190, 180, 155)],
        "patterns":    ["solid", "ribbed", "layered"],
        "size_range":  (4.0, 10.0),
        "shape":       "spiral",
    },
    "angel_wing": {
        "depth_zone":  "tidal",
        "rarity_pool": ["rare"],
        "color_pool":  [(248, 245, 240), (235, 232, 226), (255, 252, 248)],
        "patterns":    ["ribbed", "solid", "ribbed"],
        "size_range":  (8.0, 18.0),
        "shape":       "fan",
    },
    # ── Reef additions ────────────────────────────────────────────────────────
    "tiger_cowrie": {
        "depth_zone":  "reef",
        "rarity_pool": ["uncommon", "rare"],
        "color_pool":  [(210, 195, 165), (190, 175, 145), (225, 210, 180)],
        "patterns":    ["spotted", "banded", "spotted"],
        "size_range":  (6.0, 12.0),
        "shape":       "oval",
    },
    "map_cowrie": {
        "depth_zone":  "reef",
        "rarity_pool": ["uncommon", "rare"],
        "color_pool":  [(185, 155, 120), (168, 138, 105), (200, 170, 135)],
        "patterns":    ["banded", "spotted", "banded"],
        "size_range":  (5.0, 10.0),
        "shape":       "oval",
    },
    "miter": {
        "depth_zone":  "reef",
        "rarity_pool": ["uncommon", "rare"],
        "color_pool":  [(195, 85, 55), (175, 68, 42), (212, 102, 70)],
        "patterns":    ["spiral", "spotted", "ribbed"],
        "size_range":  (3.0, 8.0),
        "shape":       "cone",
    },
    "harp": {
        "depth_zone":  "reef",
        "rarity_pool": ["rare"],
        "color_pool":  [(225, 140, 75), (205, 122, 60), (240, 158, 90)],
        "patterns":    ["ribbed", "banded", "ribbed"],
        "size_range":  (5.0, 12.0),
        "shape":       "oval",
    },
    "helmet": {
        "depth_zone":  "reef",
        "rarity_pool": ["rare"],
        "color_pool":  [(190, 162, 120), (170, 144, 104), (205, 178, 136)],
        "patterns":    ["banded", "solid", "layered"],
        "size_range":  (8.0, 20.0),
        "shape":       "coiled",
    },
    "tun": {
        "depth_zone":  "reef",
        "rarity_pool": ["uncommon", "rare"],
        "color_pool":  [(200, 178, 145), (182, 160, 128), (215, 193, 160)],
        "patterns":    ["banded", "ribbed", "solid"],
        "size_range":  (7.0, 18.0),
        "shape":       "coiled",
    },
    "fig_shell": {
        "depth_zone":  "reef",
        "rarity_pool": ["uncommon"],
        "color_pool":  [(195, 160, 105), (178, 144, 90), (210, 175, 120)],
        "patterns":    ["ribbed", "banded", "spiral"],
        "size_range":  (5.0, 12.0),
        "shape":       "coiled",
    },
    "flamingo_tongue": {
        "depth_zone":  "reef",
        "rarity_pool": ["uncommon", "rare"],
        "color_pool":  [(240, 215, 185), (225, 198, 170), (252, 228, 200)],
        "patterns":    ["spotted", "banded", "spotted"],
        "size_range":  (2.0, 4.5),
        "shape":       "oval",
    },
    "textile_cone": {
        "depth_zone":  "reef",
        "rarity_pool": ["rare"],
        "color_pool":  [(210, 185, 150), (192, 168, 133), (225, 200, 165)],
        "patterns":    ["spotted", "banded", "spotted"],
        "size_range":  (5.0, 12.0),
        "shape":       "cone",
    },
    "geography_cone": {
        "depth_zone":  "reef",
        "rarity_pool": ["rare", "epic"],
        "color_pool":  [(215, 180, 140), (198, 163, 125), (228, 195, 155)],
        "patterns":    ["spotted", "banded", "spotted"],
        "size_range":  (8.0, 15.0),
        "shape":       "cone",
    },
    "golden_cowrie": {
        "depth_zone":  "reef",
        "rarity_pool": ["epic"],
        "color_pool":  [(215, 170, 60), (195, 150, 45), (230, 188, 78)],
        "patterns":    ["solid", "iridescent", "solid"],
        "size_range":  (8.0, 15.0),
        "shape":       "oval",
    },
    "imperial_volute": {
        "depth_zone":  "reef",
        "rarity_pool": ["rare", "epic"],
        "color_pool":  [(220, 155, 80), (200, 138, 65), (235, 172, 95)],
        "patterns":    ["spotted", "banded", "spotted"],
        "size_range":  (12.0, 30.0),
        "shape":       "oval",
    },
    "junonia": {
        "depth_zone":  "reef",
        "rarity_pool": ["rare"],
        "color_pool":  [(240, 230, 215), (222, 212, 198), (252, 242, 228)],
        "patterns":    ["spotted", "banded", "spotted"],
        "size_range":  (6.0, 14.0),
        "shape":       "oval",
    },
    "spider_conch": {
        "depth_zone":  "reef",
        "rarity_pool": ["rare"],
        "color_pool":  [(205, 180, 145), (188, 163, 130), (220, 195, 160)],
        "patterns":    ["ribbed", "solid", "spined"],
        "size_range":  (8.0, 18.0),
        "shape":       "fan",
    },
    "frog_shell": {
        "depth_zone":  "reef",
        "rarity_pool": ["uncommon", "rare"],
        "color_pool":  [(155, 125, 90), (138, 110, 78), (170, 140, 105)],
        "patterns":    ["ribbed", "spiral", "spotted"],
        "size_range":  (4.0, 10.0),
        "shape":       "spiral",
    },
    "lightning_whelk": {
        "depth_zone":  "reef",
        "rarity_pool": ["rare"],
        "color_pool":  [(210, 195, 168), (192, 178, 152), (225, 210, 182)],
        "patterns":    ["banded", "spiral", "banded"],
        "size_range":  (10.0, 28.0),
        "shape":       "spiral",
    },
    "venus_comb": {
        "depth_zone":  "reef",
        "rarity_pool": ["rare"],
        "color_pool":  [(225, 210, 185), (208, 192, 168), (240, 225, 200)],
        "patterns":    ["spined", "ribbed", "spined"],
        "size_range":  (6.0, 14.0),
        "shape":       "spiral",
    },
    "slit_shell": {
        "depth_zone":  "reef",
        "rarity_pool": ["rare", "epic"],
        "color_pool":  [(200, 170, 135), (180, 152, 118), (215, 185, 150)],
        "patterns":    ["coiled", "banded", "coiled"],
        "size_range":  (4.0, 10.0),
        "shape":       "coiled",
    },
    "glory_cone": {
        "depth_zone":  "reef",
        "rarity_pool": ["rare", "epic"],
        "color_pool":  [(225, 185, 140), (205, 165, 122), (240, 200, 155)],
        "patterns":    ["spotted", "banded", "spotted"],
        "size_range":  (6.0, 12.0),
        "shape":       "cone",
    },
    "chestnut_cowrie": {
        "depth_zone":  "reef",
        "rarity_pool": ["uncommon"],
        "color_pool":  [(130, 90, 55), (112, 75, 42), (148, 105, 68)],
        "patterns":    ["solid", "banded", "spotted"],
        "size_range":  (3.0, 6.0),
        "shape":       "oval",
    },
    "baler_shell": {
        "depth_zone":  "reef",
        "rarity_pool": ["rare"],
        "color_pool":  [(210, 175, 130), (192, 158, 115), (225, 190, 145)],
        "patterns":    ["banded", "spotted", "solid"],
        "size_range":  (15.0, 35.0),
        "shape":       "oval",
    },
    "royal_volute": {
        "depth_zone":  "reef",
        "rarity_pool": ["epic"],
        "color_pool":  [(180, 100, 145), (160, 82, 128), (195, 118, 160)],
        "patterns":    ["spotted", "banded", "spotted"],
        "size_range":  (10.0, 22.0),
        "shape":       "oval",
    },
    "money_cowrie": {
        "depth_zone":  "reef",
        "rarity_pool": ["uncommon"],
        "color_pool":  [(220, 205, 140), (205, 190, 125), (235, 220, 155)],
        "patterns":    ["solid", "banded", "solid"],
        "size_range":  (2.0, 4.0),
        "shape":       "oval",
    },
    "giant_clam": {
        "depth_zone":  "reef",
        "rarity_pool": ["rare", "epic"],
        "color_pool":  [(120, 180, 195), (100, 160, 175), (140, 200, 215)],
        "patterns":    ["ribbed", "iridescent", "ribbed"],
        "size_range":  (30.0, 120.0),
        "shape":       "fan",
    },
    "humpback_cowrie": {
        "depth_zone":  "reef",
        "rarity_pool": ["uncommon", "rare"],
        "color_pool":  [(100, 80, 60), (82, 65, 48), (118, 95, 72)],
        "patterns":    ["solid", "spotted", "banded"],
        "size_range":  (4.0, 8.0),
        "shape":       "oval",
    },
}

# Tidal first (common→uncommon→rare), then reef (uncommon→rare→epic)
SHELL_TYPE_ORDER = [
    # Tidal — common
    "clam", "periwinkle", "scallop", "limpet", "cone",
    "cockle", "horn_shell", "ark_shell", "blue_mussel", "coquina",
    "cerith", "slipper_shell", "dove_shell", "nassa", "nerite", "tellin",
    # Tidal — uncommon
    "cowrie", "whelk", "top_shell", "auger", "moon_snail",
    "bubble_shell", "keyhole_limpet", "nutmeg", "turban", "jingle_shell",
    "carrier_shell", "olive",
    # Tidal — rare
    "sundial", "pelican_foot", "violet_snail", "angel_wing",
    # Reef — uncommon
    "oyster", "turritella", "money_cowrie", "chestnut_cowrie",
    "fig_shell", "flamingo_tongue", "tun", "frog_shell", "humpback_cowrie",
    # Reef — uncommon/rare
    "abalone", "murex", "marginella", "map_cowrie", "miter",
    "harp", "helmet", "tiger_cowrie", "lightning_whelk", "spider_conch",
    "imperial_volute", "baler_shell", "junonia",
    # Reef — rare/epic
    "textile_cone", "volute", "triton", "golden_cowrie",
    "venus_comb", "slit_shell", "glory_cone", "royal_volute",
    "geography_cone", "giant_clam", "nautilus",
]

SHELL_RARITY_COLORS = {
    "common":    (140, 160, 140),
    "uncommon":  (80,  180, 220),
    "rare":      (130, 90,  230),
    "epic":      (220, 160, 30),
    "legendary": (230, 80,  80),
}

SHELL_RARITY_LABEL = {
    "common":    "Common",
    "uncommon":  "Uncommon",
    "rare":      "Rare",
    "epic":      "Epic",
    "legendary": "Legendary",
}

SHELL_TYPE_DESCRIPTIONS = {
    # Originals
    "cowrie":          "A smooth oval shell with a toothed opening, prized across cultures as currency and ornament.",
    "cone":            "A conical shell with bold patterns, home to a venomous hunter lurking in reef sand.",
    "scallop":         "A fan-shaped bivalve with radiating ribs, often found tumbling in the shallows.",
    "clam":            "A sturdy bivalve with a smooth oval shell, common on sandy tidal flats.",
    "periwinkle":      "A small spiral gastropod with a thick shell, grazing algae in tidal pools.",
    "limpet":          "A conical shell that clings fiercely to intertidal rocks against the surge.",
    "whelk":           "A large spiral gastropod with a channeled suture and rough outer surface.",
    "oyster":          "A rough bivalve with an iridescent interior, sometimes concealing a pearl.",
    "abalone":         "A flattened spiral with a row of holes along the edge and a stunning iridescent lining.",
    "murex":           "A spiny or ribbed gastropod whose purple dye once colored royal robes.",
    "nautilus":        "A living fossil, coiling its chambered shell in perfect logarithmic proportion.",
    "triton":          "A large predatory snail with a heavily ribbed, trumpet-like shell.",
    "volute":          "An elegant oval gastropod with vivid bands and a smooth, porcelain-like surface.",
    "turritella":      "A long, tightly coiled gastropod with a sharp apex and fine spiral ribs.",
    "marginella":      "A tiny, polished oval shell with a thickened outer lip, gleaming like porcelain.",
    # Tidal additions
    "sundial":         "A flat, disc-like shell with radiating ribs that spiral outward like the face of a sundial.",
    "top_shell":       "A brightly colored conical snail that grazes algae from rocks, its shell catching the light like a polished jewel.",
    "nerite":          "A stout oval snail with a thick shell and bold black-and-white patterns, common in rocky tidal pools.",
    "tellin":          "A thin, elegant bivalve with delicate pastel hues, half-buried in clean sandy flats.",
    "auger":           "A long, tapering shell that bores through sand to ambush buried bivalves.",
    "cockle":          "A round ribbed bivalve named for its heart-shaped cross-section, common in tidal estuaries.",
    "moon_snail":      "A large, globe-shaped snail that ploughs through sand on an oversized muscular foot, drilling prey with acid.",
    "olive":           "A smooth, polished shell in muted olive tones, shaped like the fruit it takes its name from.",
    "bubble_shell":    "An extraordinarily thin shell, almost translucent, that barely contains its soft-bodied inhabitant.",
    "horn_shell":      "A slender, darkly colored gastropod common in mudflats, grazing detritus and algae.",
    "ark_shell":       "A heavy ribbed bivalve with a straight hinge line lined with dozens of tiny teeth.",
    "jingle_shell":    "A thin, translucent bivalve with a golden sheen that chimes softly when gathered in a pile.",
    "blue_mussel":     "An elongated bivalve cloaked in deep blue-black, clustering on pier pilings and wave-swept rocks.",
    "coquina":         "A tiny, jewel-like bivalve with wings of color, burrowing with the surge of each wave.",
    "keyhole_limpet":  "A flattened cone with a keyhole-shaped opening at its apex for water circulation.",
    "slipper_shell":   "A cup-shaped limpet that stacks atop others in chains, changing sex as it ages.",
    "nutmeg":          "A small, beautifully patterned cone with brown spots on a cream background, resembling grated nutmeg.",
    "pelican_foot":    "An unusual spiral shell whose outer lip extends into claw-like projections, like a bird's foot.",
    "dove_shell":      "A tiny, smooth-lipped shell barely larger than a grain of rice, with porcelain-like markings.",
    "turban":          "A thick, heavy coiled shell with a flat, pearlescent base, prized by hermit crabs as a home.",
    "cerith":          "A small, elongated, tightly coiled gastropod common in seagrass beds and sandy shallows.",
    "violet_snail":    "A fragile spiral shell of vivid violet, drifting at the ocean's surface beneath a raft of bubbles.",
    "nassa":           "A small ribbed mud snail that scavenges exposed flats in dense feeding aggregations.",
    "carrier_shell":   "A snail that cements pebbles, shells, and coral fragments onto its own shell as camouflage.",
    "angel_wing":      "A delicate elongated bivalve of pure white, named for the feathered appearance of its fine ribs.",
    # Reef additions
    "tiger_cowrie":    "One of the largest cowries, glossy white with bold black spots that vanish beneath its fleshy mantle.",
    "map_cowrie":      "A large cowrie whose intricate brown-and-cream pattern resembles an ancient cartographic chart.",
    "miter":           "A slender, brightly colored reef gastropod named for the tall peaked hat worn by a bishop.",
    "harp":            "An oval shell with bold longitudinal ribs that create a harp-like silhouette against vivid coloration.",
    "helmet":          "A massive, heavy-walled gastropod with a wide flared lip, once carved into cameo jewelry.",
    "tun":             "A large, thin-walled globose shell with wide spiral ribs, housing an enormous soft-bodied predator.",
    "fig_shell":       "A graceful, pear-shaped gastropod with fine spiral ribs, often found hunting sea cucumbers.",
    "flamingo_tongue": "A small oval cowrie-like shell with a pure white exterior hidden beneath a vivid patterned mantle in life.",
    "textile_cone":    "A cone shell bearing an intricate net-like pattern that inspired fractal mathematicians for generations.",
    "geography_cone":  "The world's most dangerous cone shell, its map-like markings concealing a potent venomous harpoon.",
    "golden_cowrie":   "A rare and prized cowrie of lustrous golden-orange, treasured by Pacific Islander chiefs as a symbol of rank.",
    "imperial_volute": "A large, ornately patterned volute from tropical reefs, long coveted by shell collectors worldwide.",
    "junonia":         "A spotted white volute found in deep offshore waters, considered a lucky find on a Gulf Coast beach.",
    "spider_conch":    "A large conch with elongated projections along the outer lip that resemble a spider's legs.",
    "frog_shell":      "A squat, heavily sculptured spiral with irregular knobs and ribs, resembling a crouched frog.",
    "lightning_whelk": "A large left-handed spiral that opens counterclockwise, unusual among gastropods.",
    "venus_comb":      "A spectacular murex whose outer lip sprouts a row of long, delicate spines like the teeth of a comb.",
    "slit_shell":      "An ancient gastropod lineage with a slit along each whorl, once thought extinct until living specimens were found.",
    "glory_cone":      "A large, elegant cone regarded by many collectors as the most beautiful shell in the world.",
    "chestnut_cowrie": "A small, smooth oval cowrie in warm chestnut tones, common on California kelp reefs.",
    "baler_shell":     "One of the largest living gastropods, its capacious shell historically used by Pacific islanders to bail canoes.",
    "royal_volute":    "A richly colored volute in regal pink and mauve, one of the most sought-after shells by conchologists.",
    "money_cowrie":    "A small yellow-backed cowrie used as currency across Africa and Asia for thousands of years.",
    "giant_clam":      "The world's largest bivalve, its ridged shell sheltering a brilliant iridescent mantle in tropical reef lagoons.",
    "humpback_cowrie": "A deep brown cowrie with a distinctly humped profile, found in crevices of Indo-Pacific reefs.",
}

SHELL_PATTERN_DESCS = {
    "spotted":    "Scattered spots on a pale base",
    "banded":     "Concentric or spiral color bands",
    "solid":      "Single even base color",
    "ribbed":     "Raised radial or spiral ribs",
    "spiral":     "Spiraling lines along whorls",
    "layered":    "Growth layers visible on surface",
    "iridescent": "Shifting rainbow inner lining",
    "spined":     "Branching spine processes",
    "coiled":     "Tightly coiled chambered form",
}


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------

class SeashellGenerator:
    def __init__(self, world_seed: int):
        self._world_seed = world_seed

    def generate(self, bx: int, by: int, biome: str) -> "Seashell":
        from world import get_ocean_depth_zone
        shell_seed = hash((self._world_seed, bx, by)) & 0xFFFFFFFF
        rng = random.Random(shell_seed)

        zone = get_ocean_depth_zone(by)
        if zone not in ("tidal", "reef"):
            zone = "tidal"

        eligible = [s for s, d in SHELL_TYPES.items() if d["depth_zone"] == zone]
        if not eligible:
            eligible = ["cowrie"]

        species = rng.choice(eligible)
        sdef = SHELL_TYPES[species]

        rarity  = rng.choice(sdef["rarity_pool"])
        color   = rng.choice(sdef["color_pool"])
        pattern = rng.choice(sdef["patterns"])
        size_cm = round(rng.uniform(*sdef["size_range"]), 1)

        uid = hashlib.md5(f"shell_{shell_seed}_{bx}_{by}".encode()).hexdigest()[:12]

        return Seashell(
            uid=uid,
            species=species,
            rarity=rarity,
            depth_zone=zone,
            color=color,
            pattern=pattern,
            size_cm=size_cm,
            biome_found=biome,
            seed=shell_seed,
        )


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

_shell_surf_cache = {}
_shell_codex_cache = {}


def _darken(color, amount=40):
    return tuple(max(0, c - amount) for c in color)


def _lighten(color, amount=40):
    return tuple(min(255, c + amount) for c in color)


def render_seashell(shell: "Seashell", cell_size: int = 48) -> pygame.Surface:
    cache_key = (shell.uid, cell_size)
    if cache_key in _shell_surf_cache:
        return _shell_surf_cache[cache_key]

    rng = random.Random(shell.seed)
    surf = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
    surf.fill((0, 0, 0, 0))

    shape = SHELL_TYPES.get(shell.species, {}).get("shape", "oval")
    c = shell.color
    dark = _darken(c)
    light = _lighten(c)
    cx = cy = cell_size // 2
    r = cell_size // 2 - 4

    if shape == "oval":
        pygame.draw.ellipse(surf, c, (cx - r, cy - int(r * 0.7), r * 2, int(r * 1.4)))
        pygame.draw.ellipse(surf, dark, (cx - r, cy - int(r * 0.7), r * 2, int(r * 1.4)), 2)
        if shell.pattern in ("spotted", "banded"):
            for _ in range(5 if shell.pattern == "spotted" else 0):
                sx = cx + rng.randint(-r + 4, r - 4)
                sy = cy + rng.randint(-int(r * 0.5), int(r * 0.5))
                pygame.draw.circle(surf, dark, (sx, sy), rng.randint(2, 4))
            if shell.pattern == "banded":
                for bi in range(3):
                    bx2 = cx - r + 6 + bi * (r * 2 - 12) // 3
                    pygame.draw.line(surf, dark, (bx2, cy - int(r * 0.6)), (bx2, cy + int(r * 0.6)), 2)
        if shell.pattern == "iridescent":
            shine = pygame.Surface((r, int(r * 0.8)), pygame.SRCALPHA)
            shine.fill((120, 200, 195, 60))
            surf.blit(shine, (cx - r // 2, cy - int(r * 0.3)))

    elif shape == "cone":
        pts = [(cx, cy - r), (cx + r, cy + r), (cx - r, cy + r)]
        pygame.draw.polygon(surf, c, pts)
        pygame.draw.polygon(surf, dark, pts, 2)
        if shell.pattern in ("spotted", "banded"):
            for i in range(3):
                y = cy - r + (r * 2 * (i + 1) // 4)
                w = r * 2 * (i + 1) // 4
                pygame.draw.line(surf, dark, (cx - w // 2, y), (cx + w // 2, y), 1)

    elif shape == "spiral":
        t = 0.0
        pts = []
        while t < 4 * math.pi:
            ri = (r * 0.1 + r * 0.9 * t / (4 * math.pi))
            px = int(cx + ri * math.cos(t))
            py = int(cy + ri * math.sin(t))
            pts.append((px, py))
            t += 0.25
        if len(pts) >= 2:
            pygame.draw.lines(surf, dark, False, pts, 3)
            pygame.draw.lines(surf, c, False, pts, 2)

    elif shape == "fan":
        for i in range(7):
            angle = math.pi + i * math.pi / 6
            ex = int(cx + r * math.cos(angle))
            ey = int(cy + r * math.sin(angle))
            pygame.draw.line(surf, dark if i % 2 == 0 else c, (cx, cy + r // 2), (ex, ey), 2)
        pygame.draw.circle(surf, c, (cx, cy + r // 2), r // 3)
        pygame.draw.circle(surf, dark, (cx, cy + r // 2), r // 3, 1)

    elif shape == "coiled":
        for ring in range(4, 0, -1):
            ri = r * ring // 4
            col = c if ring % 2 == 0 else dark
            pygame.draw.circle(surf, col, (cx, cy), ri)
        pygame.draw.circle(surf, dark, (cx, cy), r, 2)
        if shell.pattern == "banded":
            pygame.draw.line(surf, dark, (cx - r, cy), (cx + r, cy), 2)

    _shell_surf_cache[cache_key] = surf
    return surf


def render_shell_codex_preview(species: str, cell_size: int = 48) -> pygame.Surface:
    cache_key = (species, cell_size)
    if cache_key in _shell_codex_cache:
        return _shell_codex_cache[cache_key]

    sdef = SHELL_TYPES.get(species)
    if sdef is None:
        s = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
        _shell_codex_cache[cache_key] = s
        return s

    preview = Seashell(
        uid=f"__codex_{species}__",
        species=species,
        rarity="common",
        depth_zone=sdef["depth_zone"],
        color=sdef["color_pool"][0],
        pattern=sdef["patterns"][0],
        size_cm=round((sdef["size_range"][0] + sdef["size_range"][1]) / 2, 1),
        biome_found="ocean",
        seed=hash(species) & 0xFFFFFFFF,
    )
    surf = render_seashell(preview, cell_size)
    _shell_codex_cache[cache_key] = surf
    return surf
