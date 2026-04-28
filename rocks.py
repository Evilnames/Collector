import math
import random
import pygame
from dataclasses import dataclass, field


@dataclass
class Rock:
    uid: str
    base_type: str
    rarity: str
    size: str
    primary_color: tuple
    secondary_color: tuple
    pattern: str
    pattern_density: float
    hardness: float
    luster: float
    purity: float
    specials: list
    depth_found: int
    seed: int
    upgrades: list = field(default_factory=list)


# ---------------------------------------------------------------------------
# Rock type definitions
# ---------------------------------------------------------------------------

ROCK_TYPES = {
    "granite": {
        "min_depth": 6,
        "rarity_pool": ["common", "common", "common", "uncommon"],
        "color_pool": [((150, 140, 135), (180, 160, 155)), ((160, 130, 130), (190, 150, 145))],
        "patterns": ["banded", "solid", "banded"],
    },
    "coal_gem": {
        "min_depth": 10,
        "rarity_pool": ["common", "common", "common", "uncommon"],
        "color_pool": [((28, 25, 28), (200, 200, 200)), ((35, 30, 35), (180, 180, 180))],
        "patterns": ["speckled", "speckled", "solid"],
    },
    "quartz": {
        "min_depth": 20,
        "rarity_pool": ["uncommon", "uncommon", "common", "rare"],
        "color_pool": [((230, 225, 220), (200, 160, 170)), ((240, 235, 230), (210, 170, 180))],
        "patterns": ["veined", "solid", "veined"],
    },
    "pyrite": {
        "min_depth": 30,
        "rarity_pool": ["uncommon", "uncommon", "common", "rare"],
        "color_pool": [((200, 175, 50), (60, 55, 40)), ((210, 185, 60), (50, 45, 30))],
        "patterns": ["spotted", "spotted", "banded"],
    },
    "amethyst": {
        "min_depth": 50,
        "rarity_pool": ["rare", "rare", "uncommon", "epic"],
        "color_pool": [((140, 70, 200), (180, 120, 240)), ((120, 50, 180), (160, 100, 220))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "citrine": {
        "min_depth": 60,
        "rarity_pool": ["rare", "rare", "uncommon", "epic"],
        "color_pool": [((230, 160, 30), (255, 210, 80)), ((210, 140, 20), (240, 190, 60))],
        "patterns": ["veined", "solid", "spotted"],
    },
    "malachite": {
        "min_depth": 80,
        "rarity_pool": ["rare", "rare", "uncommon", "epic"],
        "color_pool": [((40, 160, 80), (20, 100, 50)), ((50, 175, 90), (25, 110, 55))],
        "patterns": ["banded", "veined", "banded"],
    },
    "bloodstone": {
        "min_depth": 120,
        "rarity_pool": ["epic", "rare", "rare", "legendary"],
        "color_pool": [((30, 90, 50), (180, 30, 30)), ((25, 80, 45), (160, 25, 25))],
        "patterns": ["spotted", "spotted", "veined"],
    },
    "moonstone": {
        "min_depth": 150,
        "rarity_pool": ["epic", "epic", "rare", "legendary"],
        "color_pool": [((180, 200, 230), (220, 230, 255)), ((160, 185, 220), (210, 225, 250))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "voidite": {
        "min_depth": 180,
        "rarity_pool": ["legendary", "epic", "epic", "legendary"],
        "color_pool": [((30, 10, 50), (100, 40, 180)), ((20, 5, 40), (80, 30, 160))],
        "patterns": ["speckled", "speckled", "spotted"],
    },
    # --- New types ---
    "flint": {
        "min_depth": 5,
        "rarity_pool": ["common", "common", "common", "uncommon"],
        "color_pool": [((70, 70, 75), (120, 120, 130)), ((60, 65, 70), (110, 115, 125))],
        "patterns": ["speckled", "solid", "speckled"],
    },
    "limestone": {
        "min_depth": 8,
        "rarity_pool": ["common", "common", "common", "uncommon"],
        "color_pool": [((215, 205, 185), (180, 170, 150)), ((225, 215, 195), (190, 180, 160))],
        "patterns": ["banded", "banded", "solid"],
    },
    "sandstone": {
        "min_depth": 10,
        "rarity_pool": ["common", "common", "uncommon", "common"],
        "color_pool": [((200, 160, 100), (180, 140, 80)), ((210, 170, 110), (190, 150, 90))],
        "patterns": ["banded", "spotted", "banded"],
    },
    "jasper": {
        "min_depth": 35,
        "rarity_pool": ["uncommon", "uncommon", "common", "rare"],
        "color_pool": [((190, 70, 40), (220, 110, 60)), ((170, 55, 30), (200, 90, 50))],
        "patterns": ["spotted", "veined", "spotted"],
    },
    "onyx": {
        "min_depth": 40,
        "rarity_pool": ["uncommon", "rare", "uncommon", "rare"],
        "color_pool": [((20, 20, 22), (200, 200, 210)), ((15, 15, 18), (180, 185, 195))],
        "patterns": ["banded", "veined", "banded"],
    },
    "obsidian_chunk": {
        "min_depth": 45,
        "rarity_pool": ["uncommon", "uncommon", "rare", "uncommon"],
        "color_pool": [((28, 10, 40), (80, 40, 120)), ((20, 8, 32), (70, 30, 110))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "jade": {
        "min_depth": 65,
        "rarity_pool": ["rare", "uncommon", "rare", "epic"],
        "color_pool": [((50, 155, 90), (30, 100, 60)), ((60, 170, 100), (35, 115, 65))],
        "patterns": ["veined", "banded", "veined"],
    },
    "tiger_eye": {
        "min_depth": 70,
        "rarity_pool": ["rare", "uncommon", "rare", "rare"],
        "color_pool": [((180, 130, 40), (100, 65, 15)), ((195, 145, 50), (115, 75, 20))],
        "patterns": ["banded", "banded", "veined"],
    },
    "carnelian": {
        "min_depth": 85,
        "rarity_pool": ["rare", "rare", "uncommon", "epic"],
        "color_pool": [((210, 80, 30), (240, 140, 65)), ((195, 65, 20), (225, 120, 50))],
        "patterns": ["solid", "spotted", "solid"],
    },
    "labradorite": {
        "min_depth": 110,
        "rarity_pool": ["epic", "rare", "rare", "epic"],
        "color_pool": [((80, 110, 160), (40, 165, 205)), ((70, 100, 150), (35, 150, 190))],
        "patterns": ["veined", "speckled", "veined"],
    },
    "azurite": {
        "min_depth": 125,
        "rarity_pool": ["epic", "rare", "rare", "legendary"],
        "color_pool": [((30, 60, 185), (65, 115, 225)), ((25, 50, 165), (52, 98, 208))],
        "patterns": ["spotted", "veined", "spotted"],
    },
    "rhodonite": {
        "min_depth": 135,
        "rarity_pool": ["epic", "epic", "rare", "legendary"],
        "color_pool": [((210, 100, 150), (40, 30, 40)), ((195, 85, 135), (30, 25, 35))],
        "patterns": ["veined", "spotted", "veined"],
    },
    "celestite": {
        "min_depth": 155,
        "rarity_pool": ["epic", "epic", "rare", "legendary"],
        "color_pool": [((160, 200, 240), (205, 228, 255)), ((145, 185, 225), (188, 212, 248))],
        "patterns": ["speckled", "solid", "speckled"],
    },
    "meteorite": {
        "min_depth": 165,
        "rarity_pool": ["epic", "rare", "epic", "legendary"],
        "color_pool": [((60, 58, 55), (200, 195, 185)), ((50, 48, 46), (185, 180, 170))],
        "patterns": ["spotted", "speckled", "spotted"],
    },
    "void_crystal": {
        "min_depth": 185,
        "rarity_pool": ["legendary", "epic", "legendary", "legendary"],
        "color_pool": [((15, 5, 35), (60, 20, 120)), ((10, 3, 28), (50, 15, 100))],
        "patterns": ["solid", "speckled", "solid"],
    },
    # --- Batch 3 ---
    "slate": {
        "min_depth": 7,
        "rarity_pool": ["common", "common", "common", "uncommon"],
        "color_pool": [((80, 90, 100), (55, 65, 78)), ((72, 82, 94), (50, 60, 72))],
        "patterns": ["banded", "solid", "banded"],
    },
    "chalk": {
        "min_depth": 9,
        "rarity_pool": ["common", "common", "common", "uncommon"],
        "color_pool": [((240, 238, 230), (200, 195, 185)), ((245, 242, 234), (210, 205, 195))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "basalt": {
        "min_depth": 12,
        "rarity_pool": ["common", "common", "common", "uncommon"],
        "color_pool": [((45, 45, 48), (70, 70, 76)), ((40, 40, 44), (62, 62, 68))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "dolomite": {
        "min_depth": 15,
        "rarity_pool": ["common", "common", "uncommon", "common"],
        "color_pool": [((190, 188, 182), (155, 150, 144)), ((200, 198, 192), (165, 160, 154))],
        "patterns": ["banded", "veined", "banded"],
    },
    "chert": {
        "min_depth": 22,
        "rarity_pool": ["common", "uncommon", "common", "uncommon"],
        "color_pool": [((130, 90, 60), (90, 58, 38)), ((142, 100, 68), (100, 66, 44))],
        "patterns": ["speckled", "solid", "speckled"],
    },
    "serpentine": {
        "min_depth": 28,
        "rarity_pool": ["uncommon", "common", "uncommon", "rare"],
        "color_pool": [((60, 130, 80), (30, 80, 50)), ((70, 145, 90), (35, 90, 58))],
        "patterns": ["veined", "spotted", "veined"],
    },
    "gypsum": {
        "min_depth": 32,
        "rarity_pool": ["uncommon", "common", "uncommon", "rare"],
        "color_pool": [((235, 220, 215), (200, 178, 172)), ((240, 228, 222), (212, 188, 182))],
        "patterns": ["solid", "banded", "solid"],
    },
    "tourmaline": {
        "min_depth": 55,
        "rarity_pool": ["rare", "uncommon", "rare", "epic"],
        "color_pool": [((20, 80, 50), (220, 120, 160)), ((15, 70, 44), (208, 108, 148))],
        "patterns": ["banded", "veined", "banded"],
    },
    "garnet": {
        "min_depth": 58,
        "rarity_pool": ["rare", "uncommon", "rare", "epic"],
        "color_pool": [((150, 28, 40), (190, 60, 70)), ((138, 22, 34), (178, 50, 62))],
        "patterns": ["spotted", "solid", "spotted"],
    },
    "lapis_lazuli": {
        "min_depth": 62,
        "rarity_pool": ["rare", "rare", "uncommon", "epic"],
        "color_pool": [((30, 58, 162), (198, 164, 28)), ((24, 50, 148), (184, 150, 22))],
        "patterns": ["speckled", "spotted", "speckled"],
    },
    "sodalite": {
        "min_depth": 68,
        "rarity_pool": ["rare", "uncommon", "rare", "rare"],
        "color_pool": [((68, 100, 175), (220, 218, 215)), ((62, 90, 162), (208, 205, 202))],
        "patterns": ["spotted", "veined", "spotted"],
    },
    "fluorite": {
        "min_depth": 75,
        "rarity_pool": ["rare", "rare", "uncommon", "epic"],
        "color_pool": [((130, 58, 200), (58, 180, 120)), ((118, 48, 188), (48, 166, 108))],
        "patterns": ["banded", "solid", "banded"],
    },
    "hematite": {
        "min_depth": 78,
        "rarity_pool": ["rare", "uncommon", "rare", "epic"],
        "color_pool": [((100, 52, 52), (158, 78, 78)), ((88, 44, 44), (145, 66, 66))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "aventurine": {
        "min_depth": 82,
        "rarity_pool": ["rare", "rare", "uncommon", "epic"],
        "color_pool": [((50, 150, 90), (178, 154, 58)), ((44, 138, 80), (165, 142, 50))],
        "patterns": ["speckled", "spotted", "speckled"],
    },
    "spinel": {
        "min_depth": 105,
        "rarity_pool": ["epic", "rare", "rare", "legendary"],
        "color_pool": [((200, 48, 100), (240, 98, 140)), ((184, 38, 88), (226, 86, 126))],
        "patterns": ["solid", "spotted", "solid"],
    },
    "alexandrite": {
        "min_depth": 115,
        "rarity_pool": ["epic", "rare", "epic", "legendary"],
        "color_pool": [((38, 158, 78), (118, 38, 158)), ((32, 146, 68), (106, 30, 146))],
        "patterns": ["solid", "veined", "solid"],
    },
    "iolite": {
        "min_depth": 118,
        "rarity_pool": ["epic", "rare", "rare", "legendary"],
        "color_pool": [((78, 78, 200), (128, 98, 230)), ((68, 68, 185), (118, 88, 218))],
        "patterns": ["speckled", "solid", "speckled"],
    },
    "peridot": {
        "min_depth": 130,
        "rarity_pool": ["epic", "epic", "rare", "legendary"],
        "color_pool": [((140, 190, 58), (98, 148, 28)), ((128, 176, 50), (88, 136, 22))],
        "patterns": ["spotted", "veined", "spotted"],
    },
    "tanzanite": {
        "min_depth": 140,
        "rarity_pool": ["epic", "epic", "rare", "legendary"],
        "color_pool": [((58, 78, 210), (118, 58, 200)), ((50, 68, 196), (108, 50, 188))],
        "patterns": ["veined", "solid", "veined"],
    },
    "zircon": {
        "min_depth": 145,
        "rarity_pool": ["epic", "epic", "rare", "legendary"],
        "color_pool": [((178, 144, 58), (78, 108, 200)), ((166, 132, 50), (68, 98, 188))],
        "patterns": ["spotted", "speckled", "spotted"],
    },
    "moldavite": {
        "min_depth": 162,
        "rarity_pool": ["epic", "rare", "epic", "legendary"],
        "color_pool": [((28, 110, 48), (58, 168, 78)), ((22, 98, 42), (50, 155, 68))],
        "patterns": ["veined", "solid", "veined"],
    },
    "painite": {
        "min_depth": 168,
        "rarity_pool": ["legendary", "epic", "epic", "legendary"],
        "color_pool": [((188, 78, 18), (228, 118, 48)), ((175, 66, 12), (215, 106, 40))],
        "patterns": ["solid", "spotted", "solid"],
    },
    "taaffeite": {
        "min_depth": 175,
        "rarity_pool": ["legendary", "epic", "legendary", "legendary"],
        "color_pool": [((200, 148, 210), (158, 108, 178)), ((188, 136, 198), (148, 98, 166))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "aurora_stone": {
        "min_depth": 188,
        "rarity_pool": ["legendary", "legendary", "epic", "legendary"],
        "color_pool": [((38, 210, 178), (218, 178, 58)), ((32, 195, 165), (205, 165, 50))],
        "patterns": ["speckled", "veined", "speckled"],
    },
    "shadow_crystal": {
        "min_depth": 195,
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((12, 12, 18), (158, 158, 178)), ((8, 8, 14), (145, 145, 165))],
        "patterns": ["veined", "speckled", "veined"],
    },
    # --- Batch 4 ---
    "pumice": {
        "min_depth": 13,
        "rarity_pool": ["common", "common", "common", "uncommon"],
        "color_pool": [((210, 205, 198), (175, 168, 160)), ((218, 212, 205), (183, 176, 168))],
        "patterns": ["speckled", "solid", "speckled"],
    },
    "travertine": {
        "min_depth": 17,
        "rarity_pool": ["common", "common", "uncommon", "common"],
        "color_pool": [((228, 215, 188), (195, 178, 148)), ((235, 222, 196), (202, 185, 155))],
        "patterns": ["banded", "veined", "banded"],
    },
    "mudstone": {
        "min_depth": 19,
        "rarity_pool": ["common", "common", "common", "uncommon"],
        "color_pool": [((105, 92, 78), (75, 65, 54)), ((112, 99, 84), (82, 72, 60))],
        "patterns": ["solid", "banded", "solid"],
    },
    "agate": {
        "min_depth": 26,
        "rarity_pool": ["uncommon", "common", "uncommon", "rare"],
        "color_pool": [((210, 130, 60), (230, 200, 150)), ((180, 100, 40), (210, 175, 130))],
        "patterns": ["banded", "banded", "veined"],
    },
    "chalcedony": {
        "min_depth": 38,
        "rarity_pool": ["uncommon", "uncommon", "common", "rare"],
        "color_pool": [((180, 198, 220), (220, 228, 240)), ((168, 186, 208), (208, 218, 232))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "conglomerate": {
        "min_depth": 44,
        "rarity_pool": ["uncommon", "common", "uncommon", "uncommon"],
        "color_pool": [((160, 130, 100), (100, 78, 58)), ((148, 118, 90), (90, 68, 48))],
        "patterns": ["spotted", "spotted", "speckled"],
    },
    "prehnite": {
        "min_depth": 48,
        "rarity_pool": ["uncommon", "uncommon", "rare", "rare"],
        "color_pool": [((168, 210, 148), (120, 172, 100)), ((155, 198, 136), (110, 160, 90))],
        "patterns": ["veined", "solid", "veined"],
    },
    "sugilite": {
        "min_depth": 52,
        "rarity_pool": ["rare", "uncommon", "rare", "epic"],
        "color_pool": [((165, 48, 198), (208, 118, 238)), ((148, 38, 178), (195, 105, 225))],
        "patterns": ["solid", "spotted", "solid"],
    },
    "kyanite": {
        "min_depth": 56,
        "rarity_pool": ["rare", "uncommon", "rare", "epic"],
        "color_pool": [((58, 108, 200), (148, 185, 238)), ((48, 96, 185), (135, 172, 225))],
        "patterns": ["veined", "banded", "veined"],
    },
    "chrysocolla": {
        "min_depth": 67,
        "rarity_pool": ["rare", "uncommon", "rare", "epic"],
        "color_pool": [((42, 162, 165), (28, 118, 128)), ((36, 148, 152), (22, 106, 116))],
        "patterns": ["veined", "spotted", "veined"],
    },
    "rhodochrosite": {
        "min_depth": 73,
        "rarity_pool": ["rare", "rare", "uncommon", "epic"],
        "color_pool": [((228, 108, 138), (255, 168, 188)), ((215, 96, 125), (242, 155, 175))],
        "patterns": ["banded", "veined", "banded"],
    },
    "lepidolite": {
        "min_depth": 77,
        "rarity_pool": ["rare", "rare", "uncommon", "epic"],
        "color_pool": [((188, 148, 218), (145, 108, 178)), ((175, 136, 205), (132, 96, 165))],
        "patterns": ["speckled", "solid", "speckled"],
    },
    "calcite": {
        "min_depth": 88,
        "rarity_pool": ["rare", "uncommon", "rare", "rare"],
        "color_pool": [((238, 235, 225), (195, 190, 178)), ((245, 242, 232), (205, 200, 188))],
        "patterns": ["solid", "veined", "solid"],
    },
    "aragonite": {
        "min_depth": 92,
        "rarity_pool": ["rare", "rare", "uncommon", "epic"],
        "color_pool": [((210, 158, 68), (168, 118, 38)), ((198, 145, 58), (155, 106, 28))],
        "patterns": ["spotted", "veined", "spotted"],
    },
    "variscite": {
        "min_depth": 96,
        "rarity_pool": ["rare", "rare", "epic", "epic"],
        "color_pool": [((148, 200, 148), (88, 148, 100)), ((136, 188, 136), (78, 136, 90))],
        "patterns": ["veined", "spotted", "veined"],
    },
    "kunzite": {
        "min_depth": 108,
        "rarity_pool": ["epic", "rare", "rare", "legendary"],
        "color_pool": [((228, 168, 215), (188, 128, 178)), ((215, 155, 202), (175, 116, 165))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "aquamarine": {
        "min_depth": 113,
        "rarity_pool": ["epic", "rare", "rare", "legendary"],
        "color_pool": [((128, 210, 218), (78, 168, 185)), ((115, 196, 205), (66, 155, 172))],
        "patterns": ["solid", "veined", "solid"],
    },
    "heliodor": {
        "min_depth": 122,
        "rarity_pool": ["epic", "rare", "epic", "legendary"],
        "color_pool": [((228, 205, 68), (188, 162, 28)), ((215, 192, 58), (175, 150, 18))],
        "patterns": ["veined", "solid", "veined"],
    },
    "benitoite": {
        "min_depth": 128,
        "rarity_pool": ["epic", "epic", "rare", "legendary"],
        "color_pool": [((38, 78, 228), (88, 128, 255)), ((28, 66, 215), (76, 116, 242))],
        "patterns": ["speckled", "solid", "speckled"],
    },
    "demantoid": {
        "min_depth": 138,
        "rarity_pool": ["epic", "epic", "rare", "legendary"],
        "color_pool": [((38, 188, 88), (88, 238, 138)), ((28, 175, 76), (76, 225, 125))],
        "patterns": ["spotted", "speckled", "spotted"],
    },
    "chrysoberyl": {
        "min_depth": 153,
        "rarity_pool": ["epic", "epic", "rare", "legendary"],
        "color_pool": [((188, 205, 68), (140, 162, 28)), ((175, 192, 58), (128, 150, 18))],
        "patterns": ["spotted", "veined", "spotted"],
    },
    "grandidierite": {
        "min_depth": 163,
        "rarity_pool": ["legendary", "epic", "epic", "legendary"],
        "color_pool": [((38, 165, 158), (88, 215, 205)), ((28, 152, 145), (76, 202, 192))],
        "patterns": ["veined", "solid", "veined"],
    },
    "musgravite": {
        "min_depth": 172,
        "rarity_pool": ["legendary", "epic", "legendary", "legendary"],
        "color_pool": [((128, 118, 158), (88, 78, 118)), ((115, 105, 145), (78, 68, 106))],
        "patterns": ["speckled", "solid", "speckled"],
    },
    "serendibite": {
        "min_depth": 183,
        "rarity_pool": ["legendary", "legendary", "epic", "legendary"],
        "color_pool": [((18, 22, 58), (58, 68, 128)), ((12, 16, 48), (48, 58, 115))],
        "patterns": ["solid", "veined", "solid"],
    },
    "void_amber": {
        "min_depth": 198,
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((100, 60, 8), (220, 80, 180)), ((88, 50, 5), (205, 68, 165))],
        "patterns": ["spotted", "speckled", "spotted"],
    },
    # --- Batch 5 ---
    "shale": {
        "min_depth": 11,
        "rarity_pool": ["common", "common", "common", "uncommon"],
        "color_pool": [((95, 92, 100), (65, 62, 70)), ((105, 102, 110), (75, 72, 80))],
        "patterns": ["banded", "banded", "solid"],
    },
    "rhyolite": {
        "min_depth": 14,
        "rarity_pool": ["common", "common", "common", "uncommon"],
        "color_pool": [((210, 195, 185), (170, 150, 145)), ((220, 205, 195), (180, 160, 155))],
        "patterns": ["spotted", "banded", "spotted"],
    },
    "andesite": {
        "min_depth": 16,
        "rarity_pool": ["common", "common", "common", "uncommon"],
        "color_pool": [((120, 118, 125), (85, 82, 88)), ((130, 128, 135), (95, 92, 98))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "tuff": {
        "min_depth": 18,
        "rarity_pool": ["common", "common", "uncommon", "common"],
        "color_pool": [((185, 178, 170), (145, 138, 130)), ((195, 188, 180), (155, 148, 140))],
        "patterns": ["speckled", "solid", "speckled"],
    },
    "perlite": {
        "min_depth": 21,
        "rarity_pool": ["common", "uncommon", "common", "uncommon"],
        "color_pool": [((225, 222, 218), (188, 185, 180)), ((232, 229, 225), (195, 192, 187))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "quartzite": {
        "min_depth": 24,
        "rarity_pool": ["uncommon", "common", "uncommon", "rare"],
        "color_pool": [((235, 230, 225), (195, 188, 182)), ((228, 222, 218), (188, 180, 175))],
        "patterns": ["banded", "solid", "veined"],
    },
    "phlogopite": {
        "min_depth": 34,
        "rarity_pool": ["uncommon", "common", "uncommon", "rare"],
        "color_pool": [((155, 128, 80), (110, 88, 52)), ((168, 140, 90), (122, 99, 62))],
        "patterns": ["speckled", "banded", "speckled"],
    },
    "zoisite": {
        "min_depth": 42,
        "rarity_pool": ["uncommon", "uncommon", "common", "rare"],
        "color_pool": [((210, 155, 175), (155, 108, 128)), ((198, 142, 162), (143, 96, 116))],
        "patterns": ["veined", "spotted", "veined"],
    },
    "epidote": {
        "min_depth": 46,
        "rarity_pool": ["uncommon", "uncommon", "rare", "rare"],
        "color_pool": [((100, 130, 70), (70, 100, 45)), ((112, 142, 80), (80, 112, 55))],
        "patterns": ["spotted", "veined", "spotted"],
    },
    "enstatite": {
        "min_depth": 54,
        "rarity_pool": ["rare", "uncommon", "rare", "epic"],
        "color_pool": [((148, 128, 98), (108, 90, 68)), ((158, 138, 108), (118, 100, 78))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "diopside": {
        "min_depth": 64,
        "rarity_pool": ["rare", "uncommon", "rare", "epic"],
        "color_pool": [((48, 138, 88), (28, 98, 58)), ((55, 150, 98), (35, 108, 66))],
        "patterns": ["veined", "solid", "veined"],
    },
    "sphene": {
        "min_depth": 72,
        "rarity_pool": ["rare", "rare", "uncommon", "epic"],
        "color_pool": [((198, 168, 48), (148, 118, 18)), ((210, 180, 58), (160, 130, 28))],
        "patterns": ["spotted", "veined", "spotted"],
    },
    "andalusite": {
        "min_depth": 76,
        "rarity_pool": ["rare", "rare", "uncommon", "epic"],
        "color_pool": [((168, 118, 95), (128, 78, 58)), ((180, 130, 105), (140, 90, 68))],
        "patterns": ["veined", "banded", "veined"],
    },
    "staurolite": {
        "min_depth": 83,
        "rarity_pool": ["rare", "rare", "uncommon", "epic"],
        "color_pool": [((138, 98, 58), (98, 68, 32)), ((150, 110, 68), (108, 78, 42))],
        "patterns": ["spotted", "solid", "spotted"],
    },
    "topaz": {
        "min_depth": 90,
        "rarity_pool": ["rare", "rare", "uncommon", "epic"],
        "color_pool": [((168, 215, 235), (128, 175, 200)), ((188, 228, 245), (148, 192, 215))],
        "patterns": ["solid", "veined", "solid"],
    },
    "dumortierite": {
        "min_depth": 94,
        "rarity_pool": ["rare", "rare", "epic", "epic"],
        "color_pool": [((68, 78, 198), (108, 118, 228)), ((58, 68, 185), (98, 108, 215))],
        "patterns": ["veined", "spotted", "veined"],
    },
    "kornerupine": {
        "min_depth": 98,
        "rarity_pool": ["epic", "rare", "rare", "legendary"],
        "color_pool": [((98, 138, 88), (68, 108, 58)), ((108, 150, 98), (78, 118, 68))],
        "patterns": ["speckled", "veined", "speckled"],
    },
    "jeremejevite": {
        "min_depth": 102,
        "rarity_pool": ["epic", "rare", "rare", "legendary"],
        "color_pool": [((195, 215, 240), (148, 170, 205)), ((208, 228, 252), (162, 185, 218))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "poudretteite": {
        "min_depth": 106,
        "rarity_pool": ["epic", "rare", "epic", "legendary"],
        "color_pool": [((238, 185, 215), (198, 145, 175)), ((225, 172, 202), (185, 132, 162))],
        "patterns": ["solid", "spotted", "solid"],
    },
    "hauyne": {
        "min_depth": 111,
        "rarity_pool": ["epic", "rare", "rare", "legendary"],
        "color_pool": [((38, 108, 218), (88, 158, 248)), ((28, 96, 205), (76, 145, 235))],
        "patterns": ["speckled", "solid", "speckled"],
    },
    "sinhalite": {
        "min_depth": 117,
        "rarity_pool": ["epic", "rare", "epic", "legendary"],
        "color_pool": [((198, 155, 68), (158, 115, 38)), ((210, 168, 78), (168, 125, 48))],
        "patterns": ["spotted", "veined", "spotted"],
    },
    "clinohumite": {
        "min_depth": 126,
        "rarity_pool": ["epic", "epic", "rare", "legendary"],
        "color_pool": [((228, 128, 38), (188, 88, 18)), ((240, 140, 48), (200, 100, 28))],
        "patterns": ["veined", "solid", "veined"],
    },
    "pargasite": {
        "min_depth": 132,
        "rarity_pool": ["epic", "epic", "rare", "legendary"],
        "color_pool": [((38, 118, 68), (22, 78, 42)), ((48, 130, 78), (28, 88, 50))],
        "patterns": ["solid", "veined", "solid"],
    },
    "hibonite": {
        "min_depth": 142,
        "rarity_pool": ["legendary", "epic", "epic", "legendary"],
        "color_pool": [((88, 78, 68), (138, 118, 98)), ((98, 88, 78), (148, 128, 108))],
        "patterns": ["speckled", "solid", "speckled"],
    },
    "fingerite": {
        "min_depth": 200,
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((158, 28, 8), (255, 88, 18)), ((140, 20, 5), (240, 75, 10))],
        "patterns": ["veined", "spotted", "veined"],
    },
    # --- Batch 6 ---
    "siltstone": {
        "min_depth": 23,
        "rarity_pool": ["common", "common", "common", "uncommon"],
        "color_pool": [((155, 145, 130), (118, 108, 95)), ((165, 155, 140), (128, 118, 105))],
        "patterns": ["banded", "solid", "banded"],
    },
    "wollastonite": {
        "min_depth": 27,
        "rarity_pool": ["uncommon", "common", "uncommon", "rare"],
        "color_pool": [((235, 232, 228), (195, 190, 184)), ((242, 239, 235), (202, 197, 191))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "barite": {
        "min_depth": 29,
        "rarity_pool": ["uncommon", "common", "uncommon", "rare"],
        "color_pool": [((210, 215, 228), (168, 172, 185)), ((218, 222, 235), (175, 179, 192))],
        "patterns": ["banded", "solid", "banded"],
    },
    "brookite": {
        "min_depth": 31,
        "rarity_pool": ["uncommon", "uncommon", "common", "rare"],
        "color_pool": [((175, 115, 48), (135, 78, 22)), ((188, 128, 58), (148, 90, 32))],
        "patterns": ["spotted", "solid", "spotted"],
    },
    "realgar": {
        "min_depth": 33,
        "rarity_pool": ["uncommon", "uncommon", "rare", "rare"],
        "color_pool": [((218, 88, 28), (255, 148, 48)), ((205, 75, 18), (242, 135, 38))],
        "patterns": ["solid", "spotted", "solid"],
    },
    "stilbite": {
        "min_depth": 36,
        "rarity_pool": ["uncommon", "uncommon", "common", "rare"],
        "color_pool": [((235, 195, 168), (200, 155, 128)), ((245, 205, 178), (210, 165, 138))],
        "patterns": ["speckled", "solid", "speckled"],
    },
    "anorthite": {
        "min_depth": 37,
        "rarity_pool": ["uncommon", "common", "uncommon", "uncommon"],
        "color_pool": [((228, 225, 218), (188, 184, 176)), ((235, 232, 225), (196, 192, 184))],
        "patterns": ["solid", "banded", "solid"],
    },
    "beryl": {
        "min_depth": 39,
        "rarity_pool": ["rare", "uncommon", "rare", "epic"],
        "color_pool": [((148, 195, 178), (98, 148, 130)), ((160, 208, 190), (110, 162, 145))],
        "patterns": ["veined", "solid", "veined"],
    },
    "axinite": {
        "min_depth": 41,
        "rarity_pool": ["uncommon", "uncommon", "rare", "rare"],
        "color_pool": [((140, 108, 88), (108, 72, 58)), ((152, 120, 98), (118, 83, 68))],
        "patterns": ["spotted", "veined", "spotted"],
    },
    "smithsonite": {
        "min_depth": 43,
        "rarity_pool": ["rare", "uncommon", "rare", "epic"],
        "color_pool": [((118, 195, 195), (78, 155, 158)), ((128, 208, 208), (88, 168, 172))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "apophyllite": {
        "min_depth": 47,
        "rarity_pool": ["uncommon", "uncommon", "rare", "rare"],
        "color_pool": [((198, 228, 205), (155, 185, 162)), ((208, 238, 215), (162, 195, 170))],
        "patterns": ["solid", "veined", "solid"],
    },
    "vesuvianite": {
        "min_depth": 51,
        "rarity_pool": ["rare", "uncommon", "rare", "epic"],
        "color_pool": [((68, 148, 88), (108, 165, 48)), ((78, 162, 98), (118, 178, 58))],
        "patterns": ["veined", "spotted", "veined"],
    },
    "dioptase": {
        "min_depth": 53,
        "rarity_pool": ["rare", "rare", "uncommon", "epic"],
        "color_pool": [((18, 148, 88), (58, 198, 128)), ((12, 135, 78), (48, 185, 118))],
        "patterns": ["spotted", "speckled", "spotted"],
    },
    "spessartine": {
        "min_depth": 57,
        "rarity_pool": ["rare", "uncommon", "rare", "epic"],
        "color_pool": [((218, 108, 38), (178, 68, 18)), ((230, 120, 48), (190, 80, 28))],
        "patterns": ["solid", "spotted", "solid"],
    },
    "hiddenite": {
        "min_depth": 59,
        "rarity_pool": ["rare", "rare", "uncommon", "epic"],
        "color_pool": [((78, 178, 108), (48, 138, 78)), ((88, 192, 118), (55, 150, 88))],
        "patterns": ["veined", "solid", "veined"],
    },
    "cuprite": {
        "min_depth": 61,
        "rarity_pool": ["rare", "uncommon", "rare", "epic"],
        "color_pool": [((178, 38, 28), (128, 18, 12)), ((192, 48, 38), (142, 28, 22))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "gaspeite": {
        "min_depth": 63,
        "rarity_pool": ["rare", "uncommon", "rare", "rare"],
        "color_pool": [((128, 200, 88), (88, 158, 48)), ((140, 215, 98), (98, 172, 58))],
        "patterns": ["spotted", "veined", "spotted"],
    },
    "pyromorphite": {
        "min_depth": 66,
        "rarity_pool": ["rare", "rare", "uncommon", "epic"],
        "color_pool": [((58, 178, 78), (18, 138, 38)), ((68, 192, 88), (28, 152, 48))],
        "patterns": ["speckled", "spotted", "speckled"],
    },
    "sphalerite": {
        "min_depth": 69,
        "rarity_pool": ["rare", "uncommon", "rare", "epic"],
        "color_pool": [((168, 128, 48), (48, 38, 28)), ((180, 140, 58), (58, 48, 38))],
        "patterns": ["spotted", "solid", "spotted"],
    },
    "herderite": {
        "min_depth": 71,
        "rarity_pool": ["rare", "rare", "uncommon", "epic"],
        "color_pool": [((195, 175, 228), (155, 135, 188)), ((208, 188, 240), (165, 145, 200))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "scorodite": {
        "min_depth": 74,
        "rarity_pool": ["rare", "rare", "uncommon", "epic"],
        "color_pool": [((118, 178, 138), (78, 138, 98)), ((128, 190, 148), (88, 150, 108))],
        "patterns": ["veined", "spotted", "veined"],
    },
    "larimar": {
        "min_depth": 79,
        "rarity_pool": ["rare", "uncommon", "rare", "epic"],
        "color_pool": [((88, 175, 215), (48, 135, 178)), ((98, 188, 228), (58, 148, 192))],
        "patterns": ["veined", "speckled", "veined"],
    },
    "neptunite": {
        "min_depth": 81,
        "rarity_pool": ["rare", "rare", "uncommon", "epic"],
        "color_pool": [((22, 15, 12), (148, 38, 18)), ((18, 10, 8), (135, 28, 12))],
        "patterns": ["speckled", "solid", "speckled"],
    },
    "legrandite": {
        "min_depth": 84,
        "rarity_pool": ["rare", "rare", "epic", "epic"],
        "color_pool": [((228, 205, 38), (188, 165, 18)), ((240, 218, 48), (200, 178, 28))],
        "patterns": ["spotted", "veined", "spotted"],
    },
    "phosphosiderite": {
        "min_depth": 86,
        "rarity_pool": ["rare", "rare", "uncommon", "epic"],
        "color_pool": [((178, 118, 188), (138, 78, 148)), ((190, 130, 200), (148, 90, 160))],
        "patterns": ["solid", "speckled", "solid"],
    },
    # --- Batch 7 ---
    "phyllite": {
        "min_depth": 25,
        "rarity_pool": ["common", "common", "common", "uncommon"],
        "color_pool": [((148, 152, 158), (108, 112, 118)), ((155, 159, 165), (115, 119, 125))],
        "patterns": ["banded", "solid", "banded"],
    },
    "cerussite": {
        "min_depth": 87,
        "rarity_pool": ["rare", "uncommon", "rare", "rare"],
        "color_pool": [((245, 242, 238), (200, 196, 190)), ((250, 248, 244), (210, 206, 200))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "mimetite": {
        "min_depth": 89,
        "rarity_pool": ["rare", "uncommon", "rare", "epic"],
        "color_pool": [((218, 175, 38), (178, 135, 18)), ((230, 188, 48), (190, 148, 28))],
        "patterns": ["spotted", "solid", "spotted"],
    },
    "adamite": {
        "min_depth": 91,
        "rarity_pool": ["rare", "rare", "uncommon", "epic"],
        "color_pool": [((178, 208, 48), (138, 168, 18)), ((188, 220, 58), (148, 180, 28))],
        "patterns": ["speckled", "spotted", "speckled"],
    },
    "wavellite": {
        "min_depth": 93,
        "rarity_pool": ["rare", "rare", "uncommon", "epic"],
        "color_pool": [((148, 198, 148), (108, 158, 108)), ((158, 210, 158), (118, 170, 118))],
        "patterns": ["spotted", "veined", "spotted"],
    },
    "turquoise": {
        "min_depth": 95,
        "rarity_pool": ["rare", "rare", "uncommon", "epic"],
        "color_pool": [((68, 178, 188), (28, 138, 150)), ((78, 192, 202), (38, 150, 165))],
        "patterns": ["veined", "spotted", "veined"],
    },
    "chrysoprase": {
        "min_depth": 97,
        "rarity_pool": ["rare", "uncommon", "rare", "epic"],
        "color_pool": [((108, 195, 108), (68, 155, 68)), ((118, 208, 118), (78, 168, 78))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "eudialyte": {
        "min_depth": 99,
        "rarity_pool": ["epic", "rare", "rare", "legendary"],
        "color_pool": [((188, 58, 78), (148, 28, 48)), ((202, 68, 88), (160, 38, 58))],
        "patterns": ["spotted", "veined", "spotted"],
    },
    "clinozoisite": {
        "min_depth": 101,
        "rarity_pool": ["rare", "rare", "uncommon", "epic"],
        "color_pool": [((215, 168, 178), (175, 128, 138)), ((225, 178, 188), (185, 138, 148))],
        "patterns": ["veined", "solid", "veined"],
    },
    "anatase": {
        "min_depth": 103,
        "rarity_pool": ["epic", "rare", "rare", "legendary"],
        "color_pool": [((28, 38, 108), (68, 78, 148)), ((18, 28, 95), (58, 68, 138))],
        "patterns": ["speckled", "solid", "speckled"],
    },
    "scapolite": {
        "min_depth": 107,
        "rarity_pool": ["rare", "rare", "epic", "epic"],
        "color_pool": [((218, 185, 88), (178, 145, 58)), ((205, 172, 78), (165, 132, 48))],
        "patterns": ["solid", "veined", "solid"],
    },
    "danburite": {
        "min_depth": 109,
        "rarity_pool": ["rare", "rare", "uncommon", "epic"],
        "color_pool": [((238, 225, 175), (198, 185, 135)), ((248, 235, 188), (208, 195, 148))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "hackmanite": {
        "min_depth": 112,
        "rarity_pool": ["epic", "rare", "rare", "legendary"],
        "color_pool": [((228, 178, 218), (188, 138, 178)), ((240, 190, 230), (200, 150, 190))],
        "patterns": ["speckled", "solid", "speckled"],
    },
    "datolite": {
        "min_depth": 114,
        "rarity_pool": ["rare", "rare", "uncommon", "epic"],
        "color_pool": [((188, 218, 195), (148, 178, 155)), ((198, 228, 205), (158, 188, 165))],
        "patterns": ["solid", "spotted", "solid"],
    },
    "phenakite": {
        "min_depth": 116,
        "rarity_pool": ["epic", "rare", "epic", "legendary"],
        "color_pool": [((242, 240, 238), (205, 202, 198)), ((248, 246, 244), (212, 209, 205))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "columbite": {
        "min_depth": 119,
        "rarity_pool": ["epic", "rare", "rare", "legendary"],
        "color_pool": [((28, 22, 20), (78, 62, 55)), ((22, 16, 14), (68, 52, 45))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "willemite": {
        "min_depth": 121,
        "rarity_pool": ["epic", "rare", "epic", "legendary"],
        "color_pool": [((68, 158, 78), (28, 118, 38)), ((78, 172, 88), (38, 130, 48))],
        "patterns": ["speckled", "spotted", "speckled"],
    },
    "ekanite": {
        "min_depth": 123,
        "rarity_pool": ["legendary", "epic", "epic", "legendary"],
        "color_pool": [((38, 128, 78), (18, 88, 48)), ((48, 142, 88), (28, 100, 58))],
        "patterns": ["veined", "solid", "veined"],
    },
    "annabergite": {
        "min_depth": 124,
        "rarity_pool": ["epic", "rare", "rare", "legendary"],
        "color_pool": [((148, 195, 148), (108, 158, 108)), ((158, 208, 158), (118, 170, 118))],
        "patterns": ["speckled", "veined", "speckled"],
    },
    "leucite": {
        "min_depth": 127,
        "rarity_pool": ["epic", "rare", "rare", "legendary"],
        "color_pool": [((232, 228, 222), (192, 188, 182)), ((240, 236, 230), (200, 196, 190))],
        "patterns": ["solid", "spotted", "solid"],
    },
    "cavansite": {
        "min_depth": 129,
        "rarity_pool": ["epic", "epic", "rare", "legendary"],
        "color_pool": [((28, 118, 198), (68, 158, 238)), ((18, 106, 185), (58, 145, 225))],
        "patterns": ["spotted", "speckled", "spotted"],
    },
    "clinoatacamite": {
        "min_depth": 131,
        "rarity_pool": ["epic", "epic", "rare", "legendary"],
        "color_pool": [((28, 108, 78), (18, 78, 52)), ((38, 120, 88), (28, 88, 62))],
        "patterns": ["veined", "spotted", "veined"],
    },
    "ettringite": {
        "min_depth": 133,
        "rarity_pool": ["legendary", "epic", "epic", "legendary"],
        "color_pool": [((238, 228, 48), (198, 188, 18)), ((248, 238, 58), (208, 198, 28))],
        "patterns": ["speckled", "solid", "speckled"],
    },
    "rhodizite": {
        "min_depth": 136,
        "rarity_pool": ["legendary", "epic", "legendary", "legendary"],
        "color_pool": [((240, 235, 215), (200, 194, 172)), ((248, 244, 225), (210, 204, 182))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "natrolite": {
        "min_depth": 139,
        "rarity_pool": ["epic", "rare", "rare", "legendary"],
        "color_pool": [((238, 236, 232), (198, 195, 190)), ((245, 243, 239), (205, 202, 197))],
        "patterns": ["solid", "banded", "solid"],
    },
    # --- Batch 8 ---
    "okenite": {
        "min_depth": 49,
        "rarity_pool": ["uncommon", "uncommon", "common", "rare"],
        "color_pool": [((242, 240, 236), (205, 202, 198)), ((248, 246, 242), (215, 212, 208))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "cassiterite": {
        "min_depth": 100,
        "rarity_pool": ["rare", "uncommon", "rare", "epic"],
        "color_pool": [((68, 48, 28), (38, 28, 18)), ((80, 58, 35), (48, 35, 22))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "tephroite": {
        "min_depth": 104,
        "rarity_pool": ["rare", "rare", "uncommon", "epic"],
        "color_pool": [((168, 155, 175), (128, 115, 135)), ((178, 165, 185), (138, 125, 145))],
        "patterns": ["spotted", "solid", "spotted"],
    },
    "rosasite": {
        "min_depth": 134,
        "rarity_pool": ["epic", "rare", "rare", "legendary"],
        "color_pool": [((58, 158, 195), (28, 118, 158)), ((68, 170, 208), (38, 130, 170))],
        "patterns": ["veined", "spotted", "veined"],
    },
    "narsarsukite": {
        "min_depth": 137,
        "rarity_pool": ["epic", "rare", "epic", "legendary"],
        "color_pool": [((208, 178, 68), (168, 138, 38)), ((220, 190, 78), (178, 148, 48))],
        "patterns": ["solid", "veined", "solid"],
    },
    "monazite": {
        "min_depth": 141,
        "rarity_pool": ["epic", "epic", "rare", "legendary"],
        "color_pool": [((195, 158, 58), (155, 118, 28)), ((208, 170, 68), (165, 128, 38))],
        "patterns": ["spotted", "solid", "spotted"],
    },
    "scheelite": {
        "min_depth": 143,
        "rarity_pool": ["epic", "epic", "rare", "legendary"],
        "color_pool": [((235, 228, 175), (195, 188, 135)), ((245, 238, 185), (205, 198, 145))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "barytocalcite": {
        "min_depth": 146,
        "rarity_pool": ["epic", "rare", "rare", "legendary"],
        "color_pool": [((240, 238, 232), (205, 202, 195)), ((248, 245, 239), (212, 208, 202))],
        "patterns": ["solid", "veined", "solid"],
    },
    "vivianite": {
        "min_depth": 148,
        "rarity_pool": ["epic", "epic", "rare", "legendary"],
        "color_pool": [((28, 48, 138), (68, 88, 188)), ((18, 38, 125), (58, 78, 175))],
        "patterns": ["veined", "spotted", "veined"],
    },
    "mottramite": {
        "min_depth": 149,
        "rarity_pool": ["epic", "rare", "epic", "legendary"],
        "color_pool": [((58, 78, 28), (28, 48, 12)), ((68, 90, 38), (38, 58, 20))],
        "patterns": ["spotted", "veined", "spotted"],
    },
    "jadeite": {
        "min_depth": 151,
        "rarity_pool": ["legendary", "epic", "epic", "legendary"],
        "color_pool": [((28, 138, 68), (18, 98, 48)), ((38, 152, 78), (25, 110, 58))],
        "patterns": ["veined", "solid", "veined"],
    },
    "glaucophane": {
        "min_depth": 152,
        "rarity_pool": ["legendary", "epic", "epic", "legendary"],
        "color_pool": [((68, 88, 148), (38, 58, 118)), ((78, 98, 160), (48, 68, 130))],
        "patterns": ["banded", "veined", "banded"],
    },
    "lawsonite": {
        "min_depth": 154,
        "rarity_pool": ["legendary", "epic", "legendary", "legendary"],
        "color_pool": [((148, 178, 218), (108, 138, 178)), ((158, 188, 228), (118, 148, 188))],
        "patterns": ["veined", "solid", "veined"],
    },
    "omphacite": {
        "min_depth": 156,
        "rarity_pool": ["legendary", "legendary", "epic", "legendary"],
        "color_pool": [((28, 88, 48), (18, 58, 28)), ((38, 100, 58), (25, 68, 38))],
        "patterns": ["solid", "veined", "solid"],
    },
    "gahnite": {
        "min_depth": 157,
        "rarity_pool": ["epic", "epic", "rare", "legendary"],
        "color_pool": [((28, 68, 88), (18, 48, 68)), ((38, 78, 98), (25, 55, 78))],
        "patterns": ["speckled", "solid", "speckled"],
    },
    "thomsonite": {
        "min_depth": 158,
        "rarity_pool": ["epic", "rare", "rare", "legendary"],
        "color_pool": [((232, 208, 198), (195, 165, 155)), ((240, 218, 208), (205, 175, 165))],
        "patterns": ["spotted", "veined", "spotted"],
    },
    "fergusonite": {
        "min_depth": 159,
        "rarity_pool": ["legendary", "epic", "legendary", "legendary"],
        "color_pool": [((22, 18, 15), (68, 55, 45)), ((16, 12, 10), (58, 45, 35))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "synchysite": {
        "min_depth": 160,
        "rarity_pool": ["legendary", "epic", "legendary", "legendary"],
        "color_pool": [((228, 218, 158), (188, 178, 118)), ((238, 228, 168), (198, 188, 128))],
        "patterns": ["spotted", "solid", "spotted"],
    },
    "samarskite": {
        "min_depth": 161,
        "rarity_pool": ["legendary", "legendary", "epic", "legendary"],
        "color_pool": [((18, 12, 10), (58, 42, 35)), ((12, 8, 6), (48, 35, 28))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "loparite": {
        "min_depth": 164,
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((15, 12, 18), (55, 45, 65)), ((10, 8, 14), (45, 35, 55))],
        "patterns": ["speckled", "solid", "speckled"],
    },
    "tantalite": {
        "min_depth": 166,
        "rarity_pool": ["legendary", "legendary", "epic", "legendary"],
        "color_pool": [((20, 15, 10), (60, 48, 35)), ((14, 10, 6), (50, 38, 28))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "polycrase": {
        "min_depth": 167,
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((25, 18, 22), (75, 55, 68)), ((18, 12, 16), (62, 45, 58))],
        "patterns": ["speckled", "spotted", "speckled"],
    },
    "pyrochlore": {
        "min_depth": 169,
        "rarity_pool": ["legendary", "legendary", "epic", "legendary"],
        "color_pool": [((88, 68, 28), (48, 35, 8)), ((100, 78, 38), (58, 45, 15))],
        "patterns": ["spotted", "solid", "spotted"],
    },
    "betafite": {
        "min_depth": 170,
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((12, 8, 15), (48, 35, 58)), ((8, 5, 10), (38, 28, 48))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "priorite": {
        "min_depth": 171,
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((35, 25, 15), (90, 65, 40)), ((28, 18, 10), (78, 55, 32))],
        "patterns": ["speckled", "veined", "speckled"],
    },
    # --- Batch 9 ---
    "strengite": {
        "min_depth": 144,
        "rarity_pool": ["epic", "epic", "rare", "legendary"],
        "color_pool": [((218, 158, 188), (178, 118, 148)), ((228, 168, 198), (188, 128, 158))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "plumbogummite": {
        "min_depth": 147,
        "rarity_pool": ["epic", "rare", "rare", "legendary"],
        "color_pool": [((195, 195, 168), (158, 158, 128)), ((205, 205, 178), (168, 168, 138))],
        "patterns": ["spotted", "veined", "spotted"],
    },
    "chevkinite": {
        "min_depth": 173,
        "rarity_pool": ["legendary", "legendary", "epic", "legendary"],
        "color_pool": [((18, 12, 8), (78, 42, 22)), ((12, 8, 5), (65, 35, 18))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "allanite": {
        "min_depth": 174,
        "rarity_pool": ["legendary", "epic", "legendary", "legendary"],
        "color_pool": [((45, 30, 18), (88, 62, 38)), ((35, 22, 12), (75, 52, 30))],
        "patterns": ["speckled", "solid", "speckled"],
    },
    "scorzalite": {
        "min_depth": 176,
        "rarity_pool": ["legendary", "legendary", "epic", "legendary"],
        "color_pool": [((38, 48, 148), (68, 78, 188)), ((28, 38, 135), (58, 68, 175))],
        "patterns": ["veined", "solid", "veined"],
    },
    "lazulite": {
        "min_depth": 177,
        "rarity_pool": ["legendary", "legendary", "epic", "legendary"],
        "color_pool": [((58, 108, 188), (28, 68, 148)), ((68, 118, 200), (38, 78, 160))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "tugtupite": {
        "min_depth": 178,
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((218, 48, 78), (178, 18, 48)), ((228, 58, 88), (188, 28, 58))],
        "patterns": ["solid", "spotted", "solid"],
    },
    "elbaite": {
        "min_depth": 179,
        "rarity_pool": ["legendary", "legendary", "epic", "legendary"],
        "color_pool": [((218, 88, 148), (48, 168, 98)), ((195, 68, 128), (38, 148, 78))],
        "patterns": ["banded", "veined", "banded"],
    },
    "bixbite": {
        "min_depth": 181,
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((188, 28, 48), (148, 8, 28)), ((200, 38, 58), (158, 18, 38))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "pezzottaite": {
        "min_depth": 182,
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((218, 88, 138), (178, 48, 98)), ((228, 98, 148), (188, 58, 108))],
        "patterns": ["solid", "veined", "solid"],
    },
    "tsavorite": {
        "min_depth": 184,
        "rarity_pool": ["legendary", "legendary", "epic", "legendary"],
        "color_pool": [((18, 148, 58), (8, 108, 38)), ((28, 162, 68), (15, 120, 48))],
        "patterns": ["solid", "spotted", "solid"],
    },
    "hessonite": {
        "min_depth": 186,
        "rarity_pool": ["legendary", "epic", "legendary", "legendary"],
        "color_pool": [((198, 138, 48), (158, 98, 18)), ((210, 150, 58), (168, 108, 28))],
        "patterns": ["spotted", "solid", "spotted"],
    },
    "rhodolite": {
        "min_depth": 187,
        "rarity_pool": ["legendary", "legendary", "epic", "legendary"],
        "color_pool": [((188, 58, 118), (148, 28, 88)), ((200, 68, 128), (158, 38, 98))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "uvarovite": {
        "min_depth": 189,
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((8, 138, 48), (3, 98, 28)), ((15, 152, 58), (8, 110, 38))],
        "patterns": ["speckled", "spotted", "speckled"],
    },
    "malaya": {
        "min_depth": 190,
        "rarity_pool": ["legendary", "legendary", "epic", "legendary"],
        "color_pool": [((218, 118, 68), (178, 78, 38)), ((228, 128, 78), (188, 88, 48))],
        "patterns": ["solid", "veined", "solid"],
    },
    "pyrope": {
        "min_depth": 191,
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((158, 18, 28), (118, 5, 12)), ((170, 28, 38), (128, 12, 20))],
        "patterns": ["solid", "spotted", "solid"],
    },
    "grossular": {
        "min_depth": 192,
        "rarity_pool": ["legendary", "epic", "legendary", "legendary"],
        "color_pool": [((178, 195, 88), (138, 155, 58)), ((188, 208, 98), (148, 165, 68))],
        "patterns": ["spotted", "solid", "spotted"],
    },
    "schorl": {
        "min_depth": 193,
        "rarity_pool": ["legendary", "epic", "legendary", "legendary"],
        "color_pool": [((12, 10, 12), (45, 38, 45)), ((8, 6, 8), (35, 28, 35))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "dravite": {
        "min_depth": 194,
        "rarity_pool": ["legendary", "legendary", "epic", "legendary"],
        "color_pool": [((108, 78, 38), (68, 48, 18)), ((120, 88, 48), (78, 58, 28))],
        "patterns": ["speckled", "solid", "speckled"],
    },
    "uvite": {
        "min_depth": 196,
        "rarity_pool": ["legendary", "legendary", "epic", "legendary"],
        "color_pool": [((78, 108, 58), (48, 78, 28)), ((88, 120, 68), (58, 88, 38))],
        "patterns": ["veined", "spotted", "veined"],
    },
    "liddicoatite": {
        "min_depth": 197,
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((148, 58, 128), (48, 128, 88)), ((160, 68, 138), (58, 138, 98))],
        "patterns": ["banded", "veined", "banded"],
    },
    "polylithionite": {
        "min_depth": 199,
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((195, 178, 218), (155, 138, 178)), ((205, 188, 228), (165, 148, 188))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "riftstone": {
        "min_depth": 201,
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((88, 18, 48), (138, 28, 78)), ((75, 12, 38), (125, 20, 68))],
        "patterns": ["veined", "speckled", "veined"],
    },
    "abyssalite": {
        "min_depth": 202,
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((8, 8, 48), (28, 28, 108)), ((5, 5, 38), (20, 20, 95))],
        "patterns": ["speckled", "veined", "speckled"],
    },
    "cosmite": {
        "min_depth": 203,
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((158, 28, 218), (218, 208, 255)), ((145, 18, 205), (205, 195, 245))],
        "patterns": ["solid", "speckled", "solid"],
    },
    # --- Batch 10 ---
    "wulfenite": {
        "min_depth": 204,
        "rarity_pool": ["legendary", "legendary", "epic", "legendary"],
        "color_pool": [((235, 140, 30), (255, 200, 80)), ((215, 120, 20), (245, 180, 60))],
        "patterns": ["solid", "spotted", "solid"],
    },
    "crocoite": {
        "min_depth": 205,
        "rarity_pool": ["legendary", "legendary", "epic", "legendary"],
        "color_pool": [((220, 80, 30), (255, 140, 60)), ((200, 65, 25), (240, 120, 45))],
        "patterns": ["veined", "spotted", "veined"],
    },
    "vanadinite": {
        "min_depth": 206,
        "rarity_pool": ["legendary", "legendary", "epic", "legendary"],
        "color_pool": [((200, 50, 20), (240, 120, 40)), ((185, 40, 15), (225, 100, 30))],
        "patterns": ["solid", "spotted", "solid"],
    },
    "torbernite": {
        "min_depth": 207,
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((40, 160, 60), (100, 220, 100)), ((30, 140, 50), (80, 200, 80))],
        "patterns": ["banded", "solid", "banded"],
    },
    "autunite": {
        "min_depth": 208,
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((200, 220, 40), (240, 255, 80)), ((180, 200, 30), (220, 240, 60))],
        "patterns": ["banded", "speckled", "banded"],
    },
    "carnotite": {
        "min_depth": 209,
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((230, 220, 30), (255, 245, 80)), ((210, 200, 20), (240, 225, 60))],
        "patterns": ["speckled", "solid", "speckled"],
    },
    "stibnite": {
        "min_depth": 210,
        "rarity_pool": ["legendary", "legendary", "epic", "legendary"],
        "color_pool": [((160, 160, 165), (120, 120, 130)), ((150, 150, 155), (110, 110, 120))],
        "patterns": ["banded", "solid", "banded"],
    },
    "cobaltite": {
        "min_depth": 211,
        "rarity_pool": ["legendary", "legendary", "epic", "legendary"],
        "color_pool": [((200, 180, 190), (140, 100, 120)), ((185, 165, 175), (125, 90, 110))],
        "patterns": ["spotted", "solid", "spotted"],
    },
    "skutterudite": {
        "min_depth": 212,
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((210, 210, 215), (180, 180, 190)), ((195, 195, 200), (165, 165, 175))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "sperrylite": {
        "min_depth": 213,
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((220, 220, 220), (200, 200, 205)), ((205, 205, 205), (185, 185, 190))],
        "patterns": ["solid", "solid", "spotted"],
    },
    "bismuthinite": {
        "min_depth": 214,
        "rarity_pool": ["legendary", "legendary", "epic", "legendary"],
        "color_pool": [((150, 145, 150), (180, 170, 185)), ((140, 135, 140), (165, 155, 170))],
        "patterns": ["banded", "veined", "banded"],
    },
    "descloizite": {
        "min_depth": 215,
        "rarity_pool": ["legendary", "legendary", "epic", "legendary"],
        "color_pool": [((100, 90, 40), (140, 130, 60)), ((90, 80, 30), (130, 115, 50))],
        "patterns": ["speckled", "solid", "speckled"],
    },
    "miargyrite": {
        "min_depth": 216,
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((120, 40, 40), (180, 80, 80)), ((105, 30, 30), (165, 65, 65))],
        "patterns": ["veined", "spotted", "veined"],
    },
    "stephanite": {
        "min_depth": 217,
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((40, 38, 42), (80, 75, 85)), ((30, 28, 32), (70, 65, 75))],
        "patterns": ["solid", "solid", "speckled"],
    },
    "polybasite": {
        "min_depth": 218,
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((35, 30, 35), (100, 40, 40)), ((25, 20, 25), (85, 30, 30))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "pyrargyrite": {
        "min_depth": 219,
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((160, 20, 30), (210, 50, 60)), ((140, 15, 25), (190, 35, 45))],
        "patterns": ["solid", "veined", "solid"],
    },
    "proustite": {
        "min_depth": 220,
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((200, 30, 30), (240, 70, 60)), ((180, 20, 20), (220, 55, 45))],
        "patterns": ["solid", "spotted", "solid"],
    },
    "argentite": {
        "min_depth": 221,
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((180, 180, 185), (160, 160, 165)), ((165, 165, 170), (145, 145, 150))],
        "patterns": ["solid", "solid", "banded"],
    },
    "acanthite": {
        "min_depth": 222,
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((120, 120, 125), (80, 78, 82)), ((110, 108, 112), (70, 68, 72))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "sylvanite": {
        "min_depth": 223,
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((200, 190, 140), (160, 155, 120)), ((185, 175, 125), (145, 140, 105))],
        "patterns": ["veined", "solid", "veined"],
    },
    "calaverite": {
        "min_depth": 224,
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((210, 185, 60), (240, 220, 100)), ((195, 170, 45), (225, 205, 85))],
        "patterns": ["spotted", "solid", "spotted"],
    },
    "petzite": {
        "min_depth": 225,
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((120, 115, 90), (160, 150, 120)), ((110, 105, 80), (145, 135, 105))],
        "patterns": ["solid", "banded", "solid"],
    },
    "hessite": {
        "min_depth": 226,
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((150, 148, 152), (130, 128, 135)), ((138, 136, 140), (118, 116, 122))],
        "patterns": ["solid", "solid", "veined"],
    },
    "krennerite": {
        "min_depth": 227,
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((220, 200, 120), (240, 230, 170)), ((205, 185, 105), (225, 215, 155))],
        "patterns": ["spotted", "veined", "spotted"],
    },
    "electrum": {
        "min_depth": 228,
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((230, 215, 130), (255, 240, 170)), ((215, 200, 115), (240, 225, 155))],
        "patterns": ["solid", "spotted", "veined"],
    },
    # --- Arctic ---
    "ice_crystal": {
        "min_depth": 5,
        "rarity_pool": ["rare", "rare", "uncommon", "epic"],
        "color_pool": [((185, 225, 248), (215, 240, 255)), ((172, 210, 238), (202, 228, 250))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "permafrost_amber": {
        "min_depth": 80,
        "rarity_pool": ["rare", "epic", "epic", "legendary"],
        "color_pool": [((195, 168, 98), (228, 205, 138)), ((182, 155, 85), (215, 192, 125))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "cryolite": {
        "min_depth": 120,
        "rarity_pool": ["epic", "epic", "rare", "legendary"],
        "color_pool": [((235, 242, 255), (210, 225, 248)), ((225, 232, 248), (198, 215, 238))],
        "patterns": ["solid", "solid", "speckled"],
    },
    # --- Alpine / Mountain rocks ---
    "mica_schist": {
        "min_depth": 5,
        "rarity_pool": ["common", "common", "uncommon", "rare"],
        "color_pool": [((158, 152, 142), (188, 180, 168)), ((145, 150, 158), (172, 175, 182))],
        "patterns": ["banded", "banded", "speckled"],
    },
    "hornfels": {
        "min_depth": 12,
        "rarity_pool": ["uncommon", "uncommon", "rare", "rare"],
        "color_pool": [((65, 60, 68), (88, 82, 92)), ((55, 52, 60), (78, 74, 82))],
        "patterns": ["solid", "speckled", "solid"],
    },
    "gneiss": {
        "min_depth": 18,
        "rarity_pool": ["common", "uncommon", "uncommon", "rare"],
        "color_pool": [((172, 162, 155), (125, 118, 112)), ((162, 152, 145), (115, 108, 102))],
        "patterns": ["banded", "banded", "veined"],
    },
}

ROCK_BIOME_AFFINITY = {
    "igneous":     {"basalt", "pumice", "rhyolite", "andesite", "tuff", "perlite", "obsidian_chunk",
                    "hauyne", "clinohumite", "fingerite", "granite", "coal_gem", "larimar"},
    "sedimentary": {"limestone", "sandstone", "chalk", "shale", "dolomite", "chert", "travertine",
                    "mudstone", "siltstone", "flint", "wollastonite", "barite", "conglomerate",
                    "slate", "gypsum"},
    "crystal":     {"quartz", "amethyst", "citrine", "fluorite", "celestite", "void_crystal",
                    "aquamarine", "benitoite", "tanzanite", "kyanite", "calcite", "apophyllite",
                    "chalcedony", "tourmaline", "topaz", "zircon", "benitoite"},
    "ferrous":     {"pyrite", "hematite", "jasper", "onyx", "garnet", "malachite", "serpentine",
                    "spinel", "alexandrite", "bloodstone", "labradorite", "staurolite", "rhodonite",
                    "aventurine", "sphalerite", "cuprite", "neptunite"},
    "void":        {"voidite", "void_crystal", "shadow_crystal", "serendibite", "void_amber",
                    "azurite", "iolite", "moldavite", "painite", "taaffeite", "musgravite",
                    "neptunite"},
    "tundra":      {"ice_crystal", "cryolite", "permafrost_amber", "quartzite",
                    "quartz", "fluorite", "calcite", "celestite", "moonstone", "topaz"},
    "alpine_mountain": {"mica_schist", "hornfels", "gneiss", "quartzite", "quartz", "fluorite"},
    "rocky_mountain":  {"mica_schist", "hornfels", "gneiss", "quartzite", "granite", "basalt"},
    "rolling_hills":   {"limestone", "flint", "chalk", "sandstone", "conglomerate", "gneiss"},
    "steep_hills":     {"shale", "slate", "flint", "limestone", "dolomite", "hornfels"},
}

ROCK_TYPE_ORDER = sorted(ROCK_TYPES.keys(), key=lambda t: ROCK_TYPES[t]["min_depth"])

ROCK_TYPE_DESCRIPTIONS = {
    "flint":          "A fine-grained sedimentary rock prized since prehistory for its sharp edge.",
    "granite":        "A coarse-grained igneous rock, the backbone of the shallow earth.",
    "limestone":      "Sedimentary rock rich in calcium carbonate, pale and layered.",
    "coal_gem":       "Carbonized organic matter compressed into dark, lustrous form.",
    "sandstone":      "Compressed grains of ancient sand, warm-toned and banded.",
    "quartz":         "Silicon dioxide crystals, prized for their clarity and veined beauty.",
    "pyrite":         "Fool's gold — golden metallic luster in iron sulfide formations.",
    "jasper":         "An opaque red-orange chalcedony, patterned by iron-rich deposits.",
    "onyx":           "A banded chalcedony with striking black-and-white contrast.",
    "obsidian_chunk": "Volcanic glass formed when lava cools rapidly, deeply black.",
    "amethyst":       "Purple quartz of striking beauty, formed in volcanic cavities.",
    "citrine":        "Yellow to orange quartz, warmed by trace iron in its depths.",
    "jade":           "A nephrite stone of deep green, veined with ancient complexity.",
    "tiger_eye":      "A chatoyant gemstone of golden-brown silk, banded like an iris.",
    "malachite":      "Banded green copper carbonate, layered by ancient mineral flows.",
    "carnelian":      "A warm red-orange chalcedony, translucent and deeply colored.",
    "bloodstone":     "Dark green jasper spotted with blood-red iron oxide inclusions.",
    "labradorite":    "A feldspar that flashes iridescent blues when the light catches.",
    "azurite":        "A deep blue copper carbonate, vivid as a midnight sky.",
    "rhodonite":      "Pink manganese silicate veined with black oxide inclusions.",
    "moonstone":      "Feldspar with adularescence — a floating inner glow like moonlight.",
    "celestite":      "Pale blue strontium sulfate crystals, ethereally delicate.",
    "meteorite":      "Extraterrestrial iron-nickel, scarred by an ancient journey through space.",
    "voidite":        "A mineral of unknown origin, pulsing with void energy.",
    "void_crystal":   "Pure crystallized void-energy. Its interior seems to swallow light.",
    "slate":          "A fine-grained metamorphic rock that cleaves into flat layers.",
    "chalk":          "A soft white limestone formed from ancient marine microfossils.",
    "basalt":         "Dense volcanic rock, the dark floor of oceans and lava fields.",
    "dolomite":       "A calcium-magnesium carbonate, pale and layered by time.",
    "chert":          "A hard, fine-grained silica rock with a waxy, conchoidal fracture.",
    "serpentine":     "A mottled green metamorphic rock, cool and smooth to the touch.",
    "gypsum":         "Soft calcium sulfate, sometimes forming translucent selenite blades.",
    "tourmaline":     "A complex boron silicate with striking multicolor banding.",
    "garnet":         "A deep wine-red silicate prized since antiquity for its luster.",
    "lapis_lazuli":   "A royal blue rock speckled with golden pyrite, used as pigment by masters.",
    "sodalite":       "A blue tectosilicate flecked with white calcite veins.",
    "fluorite":       "Calcium fluoride in vivid purple and green, often fluorescent.",
    "hematite":       "Iron oxide with a metallic luster, leaving a blood-red streak.",
    "aventurine":     "A quartz variety spangled with reflective mineral flakes.",
    "spinel":         "A magnesium aluminate often mistaken for ruby — prized in its own right.",
    "alexandrite":    "A chromium-rich chrysoberyl that shifts between green and violet.",
    "iolite":         "A pleochroic blue-violet cordierite, the 'water sapphire' of old.",
    "peridot":        "Olive-green olivine, formed deep in the mantle and brought up by volcanism.",
    "tanzanite":      "A blue-violet zoisite found in only one place in the natural world.",
    "zircon":         "One of the oldest minerals on earth, in golden to vivid blue forms.",
    "moldavite":      "A glassy tektite formed by meteorite impact, bottle-green and rare.",
    "painite":        "Once the rarest mineral known, a deep orange-red borate crystal.",
    "taaffeite":      "A mauve beryllium spinel so rare it was found in a cut gem first.",
    "aurora_stone":   "A deep-earth mineral that stores the spectrum of ancient light.",
    "shadow_crystal": "A void-adjacent lattice that bends light around its edges.",
    "pumice":         "A frothy volcanic glass so porous it floats on water.",
    "travertine":     "A banded limestone deposited by mineral springs over millennia.",
    "mudstone":       "Compacted clay and silt, a quiet record of ancient lake beds.",
    "agate":          "A chalcedony with concentric color bands formed in ancient voids.",
    "chalcedony":     "A microcrystalline quartz with a milky blue translucence.",
    "conglomerate":   "Rounded pebbles cemented together by time and pressure.",
    "prehnite":       "A pale apple-green phyllosilicate, once used to predict the future.",
    "sugilite":       "A deep purple cyclosilicate, one of the rarer gem minerals.",
    "kyanite":        "A blue aluminosilicate that grows as long bladed crystals.",
    "chrysocolla":    "A hydrated copper silicate, blue-green as a tropical shallows.",
    "rhodochrosite":  "Rosy manganese carbonate, banded pink and white like a heartbeat.",
    "lepidolite":     "A lilac lithium mica that shimmers with reflected light.",
    "calcite":        "The most common carbonate mineral, often perfectly transparent.",
    "aragonite":      "A warm orange-brown carbonate polymorph of calcite.",
    "variscite":      "A pale green hydrated aluminum phosphate, soft and waxy.",
    "kunzite":        "A pastel pink spodumene, named for a gemologist who loved pink.",
    "aquamarine":     "A pale blue-green beryl, the color of a clear winter sea.",
    "heliodor":       "A golden yellow beryl named for the sun, bright and warm.",
    "benitoite":      "A deep blue barium titanium silicate, fluorescent under UV light.",
    "demantoid":      "A brilliant green andradite garnet with unmistakable fire.",
    "chrysoberyl":    "A yellow-green beryllium aluminate, harder than most gems.",
    "grandidierite":  "A blue-green boron silicate of exceptional rarity.",
    "musgravite":     "A grey-violet beryllium oxide, among the rarest minerals found.",
    "serendibite":    "A dark borosilicate of boron, named for the island of Sri Lanka.",
    "void_amber":     "Ancient resin from before the void rift, trapping impossible light.",
    "shale":          "A fissile mudrock that splits into thin layers, dark and ancient.",
    "rhyolite":       "A fine-grained volcanic rock, pale and speckled, cousin to granite.",
    "andesite":       "An intermediate volcanic rock, grey and dense, named for the Andes.",
    "tuff":           "Compacted volcanic ash from ancient eruptions, soft and porous.",
    "perlite":        "Volcanic glass with a pearly sheen that expands dramatically in heat.",
    "quartzite":      "Metamorphic quartz fused under heat and pressure, harder than sandstone.",
    "phlogopite":     "A brown magnesium mica that peels into thin, golden-bronze sheets.",
    "zoisite":        "A calcium silicate ranging from grey to vivid pink in a single vein.",
    "epidote":        "A yellow-green silicate, common in metamorphic rock assemblages.",
    "enstatite":      "A pyroxene mineral found in igneous rocks and stony meteorites alike.",
    "diopside":       "A calcium magnesium pyroxene, chrome-green in its finest gem forms.",
    "sphene":         "A titanite with extraordinary fire and adamantine luster, golden-hued.",
    "andalusite":     "An orthosilicate formed at low pressure, revealing a cross in cross-section.",
    "staurolite":     "An iron silicate famous for its natural cruciform twin crystals.",
    "topaz":          "A silicate of aluminum and fluorine, prized in blue and imperial golden forms.",
    "dumortierite":   "A dense blue silicate easily mistaken for lapis at first glance.",
    "kornerupine":    "A borosilicate with green-brown pleochroism, found in metamorphic depths.",
    "jeremejevite":   "A colorless to pale-blue aluminum borate of extraordinary rarity.",
    "poudretteite":   "A pink borosilicate so rare only a handful of faceted stones exist.",
    "hauyne":         "A vivid blue sodalite-group mineral erupted from volcanic vents.",
    "sinhalite":      "A honey-brown borosilicate from ancient seabeds, long confused with topaz.",
    "clinohumite":    "A deep orange titanium silicate found in marble and carbonatite flows.",
    "pargasite":      "A dark green calcic amphibole forged in metamorphic and igneous heat.",
    "hibonite":       "A rare calcium aluminate oxide found in carbonatite and pristine meteorites.",
    "fingerite":      "A mineral so deep it should not exist — named for the void's own reach.",
    "siltstone":      "A fine sedimentary rock between mudstone and sandstone, pale and compact.",
    "wollastonite":   "A white calcium silicate common in metamorphic contact zones.",
    "barite":         "A heavy barium sulfate, pale blue-grey and unexpectedly dense in hand.",
    "brookite":       "A brown-orange titanium oxide polymorph, rarer than rutile or anatase.",
    "realgar":        "A vivid orange arsenic sulfide, used as pigment since antiquity.",
    "stilbite":       "A peach-coloured zeolite that grows in sheaf-like crystal fans.",
    "anorthite":      "A calcium-rich feldspar, pale and common in deep igneous terranes.",
    "beryl":          "The parent mineral of emerald and aquamarine, pale green in raw form.",
    "axinite":        "A brown-violet manganese silicate with sharp wedge-shaped crystals.",
    "smithsonite":    "A blue-green zinc carbonate that mimics turquoise in its finest forms.",
    "apophyllite":    "A pale green phyllosilicate that grows in translucent pyramid clusters.",
    "vesuvianite":    "A green calcium silicate from contact metamorphic aureoles, named for Vesuvius.",
    "dioptase":       "A vivid emerald-green copper cyclosilicate, too soft to wear, too bright to ignore.",
    "spessartine":    "An orange-red manganese garnet with a warm inner fire.",
    "hiddenite":      "An emerald-green spodumene of great rarity, found in only a few localities.",
    "cuprite":        "A deep red copper oxide with an almost metallic, gem-like luster.",
    "gaspeite":       "A bright apple-green nickel carbonate, named for its discovery in Gaspé.",
    "pyromorphite":   "A vivid green lead phosphate that grows in barrel-shaped hexagonal prisms.",
    "sphalerite":     "A honey to jet-black zinc sulfide with a resinous, almost liquid luster.",
    "herderite":      "A pale lilac beryllium phosphate prized by collectors for its delicacy.",
    "scorodite":      "A pale green iron arsenate that forms on oxidizing arsenic ore deposits.",
    "larimar":        "A sky-blue volcanic pectolite found in a single sea-cliff deposit.",
    "neptunite":      "A black titanium silicate shot through with deep red internal reflections.",
    "legrandite":     "A bright canary-yellow zinc arsenate, one of the most vivid yellows in nature.",
    "phosphosiderite": "A rose-violet iron phosphate, sometimes mistaken for amethyst at a glance.",
    "phyllite":        "A fine-grained metamorphic rock with a silky sheen from aligned mica crystals.",
    "cerussite":       "A white lead carbonate with a brilliant, almost diamond-like adamantine luster.",
    "mimetite":        "A yellow-orange lead arsenate chloride that mimics pyromorphite in habit.",
    "adamite":         "A vivid yellow-green zinc arsenate that glows brilliantly under UV light.",
    "wavellite":       "A pale green aluminium phosphate that grows in radial star-burst clusters.",
    "turquoise":       "The iconic blue-green copper aluminium phosphate, veined with earthy matrix.",
    "chrysoprase":     "Apple-green chalcedony coloured by nickel, the finest of the chalcedonies.",
    "eudialyte":       "A red-pink zirconium cyclosilicate found in alkaline igneous complexes.",
    "clinozoisite":    "A pale pink calcium silicate, the manganese-free twin of epidote.",
    "anatase":         "A deep blue-black titanium oxide polymorph with an almost metallic luster.",
    "scapolite":       "A yellow to violet calcium silicate found in metamorphic terranes.",
    "danburite":       "A pale golden borosilicate with a diamond-like luster and gentle warmth.",
    "hackmanite":      "A tenebrescent pink sodalite that shifts color when exposed to light.",
    "datolite":        "A pale green borosilicate sometimes found filling cavities in basalt flows.",
    "phenakite":       "A colorless beryllium silicate of gem clarity, harder than most quartz.",
    "columbite":       "A black iron-niobium oxide, the primary ore of the element niobium.",
    "willemite":       "A green zinc silicate that fluoresces brilliant green under ultraviolet light.",
    "ekanite":         "A translucent green thorium silicate so radioactive it eventually becomes amorphous.",
    "annabergite":     "A pale green nickel arsenate, the nickel analogue of vivianite.",
    "leucite":         "A white potassium silicate from volcanic flows, with a trapezohedral form.",
    "cavansite":       "A vivid cobalt-blue calcium vanadium silicate found in basalt vesicles.",
    "clinoatacamite":  "A dark emerald-green copper chloride hydroxide on oxidized copper deposits.",
    "ettringite":      "A bright lemon-yellow calcium sulfoaluminate, delicate and alkaline-formed.",
    "rhodizite":       "A rare pale borate found in granitic pegmatites across the world.",
    "natrolite":       "A white zeolite that grows in slender parallel needles from volcanic cavities.",
    "okenite":         "A white silicate that grows as soft, cotton-like tufts in basalt cavities.",
    "cassiterite":     "A dark brown tin oxide, the principal ore of tin since the Bronze Age.",
    "tephroite":       "A grey-lavender manganese olivine from skarn and metamorphic iron deposits.",
    "rosasite":        "A sky-blue copper-zinc carbonate that coats oxidized copper deposits in vivid colour.",
    "narsarsukite":    "A honey-yellow titanium silicate from rare alkaline igneous complexes.",
    "monazite":        "A yellow-brown rare earth phosphate that concentrates thorium in its lattice.",
    "scheelite":       "A pale yellow calcium tungstate that glows brilliant blue-white under UV light.",
    "barytocalcite":   "A white translucent barium calcium carbonate found in hydrothermal veins.",
    "vivianite":       "An iron phosphate that transforms from colorless to deep indigo blue on exposure to air.",
    "mottramite":      "A dark olive-green lead copper vanadate from oxidized ore deposits.",
    "jadeite":         "True pyroxene jade — in 'imperial' form, the most prized green stone in the world.",
    "glaucophane":     "A steel-blue sodium amphibole, the signature mineral of blueschist metamorphism.",
    "lawsonite":       "A pale blue calcium silicate formed in subducted ocean crust under extreme pressure.",
    "omphacite":       "A deep green sodium-calcium pyroxene from eclogite, born at mantle depths.",
    "gahnite":         "A dark blue-green zinc spinel found in metamorphic zinc ore deposits.",
    "thomsonite":      "A cream and pink zeolite prized for its concentric, agate-like banded patterns.",
    "fergusonite":     "A black rare earth niobate that stores yttrium, erbium, and other lanthanides.",
    "synchysite":      "A pale yellow rare earth fluorocarbonate from carbonatite and pegmatite veins.",
    "samarskite":      "A velvet-black complex niobate-tantalate storing multiple rare earth elements.",
    "loparite":        "A black perovskite-type titanate from ultra-rare alkaline igneous complexes.",
    "tantalite":       "A heavy jet-black tantalum-niobium oxide, mined for electronics at great depth.",
    "polycrase":       "A black uranium-niobate-titanate whose lattice is shattered by its own radioactivity.",
    "pyrochlore":      "A honey-brown to black niobate that concentrates niobium in carbonatite deposits.",
    "betafite":        "A deep black uranium pyrochlore, one of the most radioactive minerals found.",
    "priorite":        "A black-brown rare earth titanate from granitic pegmatites at extreme depth.",
    "strengite":       "A pale rose-pink iron phosphate from weathered iron ore deposits, delicate and rare.",
    "plumbogummite":   "A pale grey-yellow lead aluminium phosphate coating oxidized galena surfaces.",
    "chevkinite":      "A black titanium rare earth silicate from alkaline igneous and pegmatite settings.",
    "allanite":        "A dark brown-black rare earth epidote that concentrates cerium and lanthanum.",
    "scorzalite":      "A deep indigo-blue iron magnesium phosphate from granitic pegmatites.",
    "lazulite":        "A sky-blue magnesium aluminium phosphate found in quartz veins and schist.",
    "tugtupite":       "A vivid red beryllium silicate that bleaches in sunlight and darkens in dark.",
    "elbaite":         "A multicolour lithium tourmaline, the most gem-prized of the tourmaline species.",
    "bixbite":         "Red beryl — rarer than diamonds by a factor of thousands, vivid as molten crimson.",
    "pezzottaite":     "A raspberry-pink cesium beryl not recognized as its own species until 2003.",
    "tsavorite":       "A chrome-green grossular garnet from East Africa, rivalling emerald in colour.",
    "hessonite":       "A honey-orange grossular garnet with a distinctive treacly internal texture.",
    "rhodolite":       "A rose-violet pyrope-almandine garnet with exceptional clarity and colour depth.",
    "uvarovite":       "A vivid emerald-green chromium garnet that grows only in tiny drusy crystals.",
    "malaya":          "An orange-pink pyrope-spessartine garnet, named for its rejection from known groups.",
    "pyrope":          "A deep blood-red magnesium garnet, named for its fire — from the Greek for fire.",
    "grossular":       "A pale green to yellow calcium aluminium garnet, named for the gooseberry.",
    "schorl":          "The most common tourmaline species — jet-black iron tourmaline, found worldwide.",
    "dravite":         "A dark brown magnesium tourmaline, named for the Drava river region.",
    "uvite":           "A brown-green calcium magnesium tourmaline, named for Uva Province in Sri Lanka.",
    "liddicoatite":    "A triangular calcium tourmaline with spectacular concentric colour-zone cross-sections.",
    "polylithionite":  "A pale lilac lithium mica from granitic pegmatites, crystallographic sister to lepidolite.",
    "riftstone":       "A void-adjacent crystalline silicate found along deep rift fractures — faintly warm.",
    "abyssalite":      "A blue-black mineral found only at the deepest excavation points — origin unclear.",
    "cosmite":         "A shimmering violet-white crystal that does not appear in any geological survey.",
    "wulfenite":       "A vivid orange lead molybdate that grows as wafer-thin tabular crystals.",
    "crocoite":        "A stunning orange-red lead chromate, its prismatic crystals fragile as glass.",
    "vanadinite":      "A bright red-orange lead vanadate forming hexagonal barrel-shaped prisms.",
    "torbernite":      "A radioactive green uranium phosphate — beautiful and quietly lethal.",
    "autunite":        "A vivid yellow-green uranium phosphate that fluoresces intensely under UV light.",
    "carnotite":       "A canary-yellow uranium vanadate dusting ancient sandstone — richly radioactive.",
    "stibnite":        "A silvery antimony sulfide that forms long, striated metallic blades.",
    "cobaltite":       "A silver-pink cobalt arsenide with a pale rose tint that hints at its cobalt core.",
    "skutterudite":    "A silver-white cobalt arsenide from hydrothermal veins — remarkably pure.",
    "sperrylite":      "A platinum arsenide and one of the rarest platinum minerals found in nature.",
    "bismuthinite":    "A grey bismuth sulfide with faint iridescent tarnish on cleavage surfaces.",
    "descloizite":     "A heavy olive-brown lead zinc vanadate, crystallizing in wedge-shaped prisms.",
    "miargyrite":      "A dark red silver antimony sulfide — one of the 'ruby silvers' of old miners.",
    "stephanite":      "A brittle black silver antimony sulfide, the richest of the silver ores.",
    "polybasite":      "A black silver antimony sulfosalt with a dark red internal reflection.",
    "pyrargyrite":     "Deep ruby silver — a vivid dark red silver antimony sulfide of high purity.",
    "proustite":       "Light ruby silver — a brilliant crimson silver arsenosulfide, glassy and rare.",
    "argentite":       "A silvery grey silver sulfide ore, the primary source of silver at depth.",
    "acanthite":       "The stable low-temperature form of silver sulfide, lead-grey to silver-black.",
    "sylvanite":       "A pale gold-grey gold silver telluride with a writing-like crystal habit.",
    "calaverite":      "A gold telluride — one of the few minerals in which gold bonds to another element.",
    "petzite":         "A dark grey silver gold telluride, found in epithermal gold-silver deposits.",
    "hessite":         "A lead-grey silver telluride from volcanic hydrothermal veins at extreme depth.",
    "krennerite":      "A gold-white gold silver telluride, twinned in complex herringbone forms.",
    "electrum":        "A natural alloy of gold and silver found in the deepest hydrothermal veins.",
    "ice_crystal":     "A pale blue water-ice crystal that forms in permafrost cracks, preserved by perpetual cold.",
    "permafrost_amber": "Ancient amber trapped for millennia in frozen ground, its warm tones contrasting the ice around it.",
    "cryolite":        "A near-colourless sodium aluminium fluoride found only in the coldest deep rock — once mistaken for ice.",
    "mica_schist":     "A glittering metamorphic rock split into silvery-grey leaves by heat and mountain pressure.",
    "hornfels":        "A dense, dark metamorphic rock baked at the edge of igneous intrusions, hard as flint.",
    "gneiss":          "A coarse, banded rock formed deep in mountain roots where heat and pressure reshape stone into layered ribbons.",
}

RARITY_WEIGHTS = {
    # (min_depth, max_depth): {rarity: weight}
    "band_surface": {"common": 90, "uncommon": 10, "rare": 0, "epic": 0, "legendary": 0},
    "band_shallow": {"common": 70, "uncommon": 25, "rare": 5, "epic": 0, "legendary": 0},
    "band_mid":     {"common": 40, "uncommon": 40, "rare": 15, "epic": 5, "legendary": 0},
    "band_deep":    {"common": 20, "uncommon": 30, "rare": 30, "epic": 15, "legendary": 5},
    "band_core":    {"common": 10, "uncommon": 20, "rare": 30, "epic": 25, "legendary": 15},
}

RARITY_PROPS = {
    "common":    {"hardness": (1, 4),    "luster": (0.0, 0.4), "purity": (0.1, 0.4), "specials": (0, 0)},
    "uncommon":  {"hardness": (2, 6),    "luster": (0.2, 0.6), "purity": (0.3, 0.6), "specials": (0, 1)},
    "rare":      {"hardness": (3, 7),    "luster": (0.4, 0.8), "purity": (0.5, 0.8), "specials": (1, 2)},
    "epic":      {"hardness": (4, 9),    "luster": (0.6, 0.9), "purity": (0.7, 0.9), "specials": (2, 3)},
    "legendary": {"hardness": (6, 10),   "luster": (0.8, 1.0), "purity": (0.9, 1.0), "specials": (3, 4)},
}

ALL_SPECIALS = ["luminous", "magnetic", "crystalline", "resonant", "voidtouched", "dense", "hollow", "fused"]

SIZES = ["pebble", "chunk", "boulder"]
SIZE_MULT = {"pebble": 1, "chunk": 2, "boulder": 4}


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------

def _depth_band(depth):
    if depth < 20:
        return "band_surface"
    if depth < 50:
        return "band_shallow"
    if depth < 100:
        return "band_mid"
    if depth < 160:
        return "band_deep"
    return "band_core"


def _weighted_choice(rng, weights_dict):
    keys = list(weights_dict.keys())
    weights = [weights_dict[k] for k in keys]
    total = sum(weights)
    r = rng.random() * total
    acc = 0
    for k, w in zip(keys, weights):
        acc += w
        if r < acc:
            return k
    return keys[-1]


class RockGenerator:
    def __init__(self, world_seed):
        self._world_seed = world_seed

    def generate(self, bx, by, depth, biome=None, biodome=None):
        rock_seed = hash((self._world_seed, bx, by)) & 0xFFFFFFFF
        rng = random.Random(rock_seed)

        # Pick eligible types for this depth
        eligible = [t for t, d in ROCK_TYPES.items() if d["min_depth"] <= depth]
        if not eligible:
            eligible = ["granite"]

        band = _depth_band(depth)
        rarity = _weighted_choice(rng, RARITY_WEIGHTS[band])

        # Prefer types whose rarity_pool matches (soft preference)
        preferred = [t for t in eligible if rarity in ROCK_TYPES[t]["rarity_pool"]]
        type_pool = preferred if preferred else eligible

        # Biome bias — prefer types matching geological biome or ecological biodome
        affinity = ROCK_BIOME_AFFINITY.get(biome, set()) | ROCK_BIOME_AFFINITY.get(biodome, set())
        if affinity:
            biome_preferred = [t for t in type_pool if t in affinity]
            if biome_preferred:
                type_pool = biome_preferred

        base_type = rng.choice(type_pool)

        tdef = ROCK_TYPES[base_type]
        colors = rng.choice(tdef["color_pool"])
        primary_color = colors[0]
        secondary_color = colors[1]
        pattern = rng.choice(tdef["patterns"])
        pattern_density = rng.uniform(0.3, 1.0)

        size = rng.choice(SIZES)
        props = RARITY_PROPS[rarity]
        hardness = rng.uniform(*props["hardness"])
        luster = rng.uniform(*props["luster"])
        purity = rng.uniform(*props["purity"])

        n_specials_min, n_specials_max = props["specials"]
        n_specials = rng.randint(n_specials_min, n_specials_max)
        specials = rng.sample(ALL_SPECIALS, min(n_specials, len(ALL_SPECIALS)))

        uid = f"{rock_seed:08x}_{bx}_{by}"

        return Rock(
            uid=uid,
            base_type=base_type,
            rarity=rarity,
            size=size,
            primary_color=primary_color,
            secondary_color=secondary_color,
            pattern=pattern,
            pattern_density=pattern_density,
            hardness=round(hardness, 1),
            luster=round(luster, 2),
            purity=round(purity, 2),
            specials=specials,
            depth_found=depth,
            seed=rock_seed,
        )


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

_surf_cache = {}
_codex_preview_cache = {}


def render_codex_preview(type_key, cell_size=48):
    cache_key = (type_key, cell_size)
    if cache_key in _codex_preview_cache:
        return _codex_preview_cache[cache_key]
    tdef = ROCK_TYPES.get(type_key)
    if tdef is None:
        s = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
        _codex_preview_cache[cache_key] = s
        return s
    colors = tdef["color_pool"][0]
    preview = Rock(
        uid=f"__codex_{type_key}__",
        base_type=type_key,
        rarity="common",
        size="chunk",
        primary_color=colors[0],
        secondary_color=colors[1],
        pattern=tdef["patterns"][0],
        pattern_density=0.6,
        hardness=5.0,
        luster=0.5,
        purity=0.5,
        specials=[],
        depth_found=0,
        seed=hash(type_key) & 0xFFFFFFFF,
    )
    surf = render_rock(preview, cell_size)
    _codex_preview_cache[cache_key] = surf
    return surf


def render_rock(rock, cell_size=48):
    if rock.uid in _surf_cache:
        return _surf_cache[rock.uid]

    rng = random.Random(rock.seed)
    surf = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
    surf.fill((0, 0, 0, 0))

    cx, cy = cell_size // 2, cell_size // 2
    r = cell_size // 2 - 3

    # Build irregular silhouette polygon
    n_pts = 12
    angles = [i * 2 * math.pi / n_pts for i in range(n_pts)]
    jitter = r * 0.22
    pts = []
    for a in angles:
        dist = r + rng.uniform(-jitter, jitter)
        pts.append((cx + dist * math.cos(a), cy + dist * math.sin(a)))

    # Fill silhouette mask
    mask_surf = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
    pygame.draw.polygon(mask_surf, (255, 255, 255, 255), pts)

    # Base color layer
    base_surf = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
    base_surf.fill((0, 0, 0, 0))
    pygame.draw.polygon(base_surf, rock.primary_color + (255,), pts)

    # Pattern overlay
    pat_surf = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
    sc = rock.secondary_color
    density = rock.pattern_density

    if rock.pattern == "spotted":
        n = int(3 + density * 8)
        for _ in range(n):
            px = rng.randint(cx - r + 4, cx + r - 4)
            py = rng.randint(cy - r + 4, cy + r - 4)
            pr = rng.randint(2, max(3, int(r * 0.2)))
            pygame.draw.circle(pat_surf, sc + (200,), (px, py), pr)

    elif rock.pattern == "veined":
        n_veins = rng.randint(2, 4)
        for _ in range(n_veins):
            x0 = rng.randint(4, cell_size - 4)
            y0 = rng.randint(4, cell_size - 4)
            pts_v = [(x0, y0)]
            for _ in range(rng.randint(3, 6)):
                x0 += rng.randint(-8, 8)
                y0 += rng.randint(-8, 8)
                x0 = max(2, min(cell_size - 2, x0))
                y0 = max(2, min(cell_size - 2, y0))
                pts_v.append((x0, y0))
            if len(pts_v) >= 2:
                pygame.draw.lines(pat_surf, sc + (180,), False, pts_v, 2)

    elif rock.pattern == "banded":
        n_bands = rng.randint(3, 6)
        band_h = cell_size // n_bands
        for i in range(n_bands):
            if i % 2 == 0:
                y0 = i * band_h
                pygame.draw.rect(pat_surf, sc + (160,), (0, y0, cell_size, band_h))

    elif rock.pattern == "speckled":
        n = int(20 + density * 60)
        for _ in range(n):
            px = rng.randint(0, cell_size - 1)
            py = rng.randint(0, cell_size - 1)
            pat_surf.set_at((px, py), sc + (220,))

    # Composite: base then pattern, clipped by mask
    combined = base_surf.copy()
    combined.blit(pat_surf, (0, 0))

    # Apply mask
    combined.blit(mask_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    surf.blit(combined, (0, 0))

    # Edge darkening for 3D effect
    edge_surf = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
    for dist_step in range(1, 5):
        alpha = 60 - dist_step * 12
        if alpha <= 0:
            break
        shrunk = [(
            cx + (px - cx) * (1 - dist_step * 0.05),
            cy + (py - cy) * (1 - dist_step * 0.05),
        ) for px, py in pts]
        pygame.draw.polygon(edge_surf, (0, 0, 0, 0), shrunk)
    # Draw thick dark outline
    pygame.draw.polygon(edge_surf, (0, 0, 0, 120), pts, 3)
    surf.blit(edge_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    # Redraw to not multiply base away entirely
    surf.blit(combined, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

    # Re-apply mask after compositing to keep clean edges
    final = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
    pygame.draw.polygon(final, rock.primary_color + (255,), pts)
    final.blit(pat_surf, (0, 0))
    # Darken edges
    for i in range(3):
        alpha = 80 - i * 25
        pygame.draw.polygon(final, (0, 0, 0, alpha), pts, 3 - i)
    surf = final

    # Sparkles for rare+
    rarities = ["common", "uncommon", "rare", "epic", "legendary"]
    rarity_idx = rarities.index(rock.rarity)
    if rarity_idx >= 2:
        n_sparks = (rarity_idx - 1) * 4
        for _ in range(n_sparks):
            px = rng.randint(4, cell_size - 4)
            py = rng.randint(4, cell_size - 4)
            brightness = rng.randint(200, 255)
            surf.set_at((px, py), (brightness, brightness, brightness, 255))
            if cell_size > 32:
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = px + dx, py + dy
                    if 0 <= nx < cell_size and 0 <= ny < cell_size:
                        surf.set_at((nx, ny), (brightness, brightness, brightness, 120))

    _surf_cache[rock.uid] = surf
    return surf


# ---------------------------------------------------------------------------
# Rarity colors (for UI borders)
# ---------------------------------------------------------------------------

RARITY_COLORS = {
    "common":    (140, 140, 140),
    "uncommon":  (50, 180, 50),
    "rare":      (60, 100, 220),
    "epic":      (150, 50, 220),
    "legendary": (240, 180, 0),
}


# ---------------------------------------------------------------------------
# Refinery equipment logic
# ---------------------------------------------------------------------------

def _size_mult(rock):
    base = SIZE_MULT[rock.size]
    if "dense" in rock.specials:
        base = max(1, base - 1)
    return base


def _effective_luster(rock):
    l = rock.luster
    if "hollow" in rock.specials:
        l = max(0.0, l - 0.3)
    return l


def _effective_purity(rock):
    p = rock.purity
    if "dense" in rock.specials:
        p = min(1.0, p + 0.3)
    return p


def _base_output_count(rock, formula_val):
    count = max(1, math.ceil(formula_val))
    if "hollow" in rock.specials:
        count += 2
    return count


# Gem type → item_id mapping
GEM_ITEMS = {
    "quartz":    "quartz_gem",
    "amethyst":  "amethyst_gem",
    "citrine":   "citrine_gem",
}


def _tumbler_can_use(rock):
    return "magnetic" not in rock.specials and "polished" not in rock.upgrades


def _tumbler_refine(rock):
    rock.luster = min(1.0, rock.luster + 0.25)
    rock.upgrades.append("polished")
    return []


def _crusher_can_use(rock):
    return True


def _crusher_refine(rock):
    purity = _effective_purity(rock)
    sm = _size_mult(rock)
    count = _base_output_count(rock, sm * math.ceil(purity * 3))
    if "magnetic" in rock.specials:
        count += 2
    return [("rock_dust", count)]


def _gem_cutter_can_use(rock):
    return "crystalline" in rock.specials


def _gem_cutter_refine(rock):
    purity = _effective_purity(rock)
    gem_item = GEM_ITEMS.get(rock.base_type, "quartz_gem")
    base_count = _base_output_count(rock, purity * 4)
    multiplier = 1.0
    if "polished" in rock.upgrades:
        multiplier *= 1.5
    if "fired" in rock.upgrades:
        multiplier *= 2.0
    return [(gem_item, max(1, round(base_count * multiplier)))]


def _kiln_can_use(rock):
    return "fired" not in rock.upgrades


def _kiln_refine(rock):
    rock.purity = min(1.0, rock.purity + 0.25)
    rock.upgrades.append("fired")
    return []


def _resonance_can_use(rock):
    return True


def _resonance_refine(rock):
    outputs = []
    if "voidtouched" in rock.specials:
        count = 2 if "fired" in rock.upgrades else 1
        outputs.append(("void_essence", count))
    if not outputs:
        outputs.append(("rock_dust", 1))
    return outputs


# Maps block_id → (name, description, can_use_fn, refine_fn)
# Block IDs are imported lazily to avoid circular import
def build_refinery_equipment():
    from blocks import TUMBLER_BLOCK, CRUSHER_BLOCK, GEM_CUTTER_BLOCK, KILN_BLOCK, RESONANCE_BLOCK
    return {
        TUMBLER_BLOCK: {
            "name": "Rock Tumbler",
            "description": "Polishes the rock, raising Luster +0.25. Cannot re-polish. Rock stays in collection.",
            "can_use": _tumbler_can_use,
            "refine": _tumbler_refine,
            "upgrade_preview": lambda rock: f"Luster: {rock.luster:.2f}  \u2192  {min(1.0, rock.luster + 0.25):.2f}",
        },
        CRUSHER_BLOCK: {
            "name": "Stone Crusher",
            "description": "Crushes rocks into raw dust. Magnetic rocks yield bonus material.",
            "can_use": _crusher_can_use,
            "refine": _crusher_refine,
        },
        GEM_CUTTER_BLOCK: {
            "name": "Gem Cutter",
            "description": "Cuts crystalline rocks into gems. Polished \u00d71.5, Fired \u00d72.0 (stackable).",
            "can_use": _gem_cutter_can_use,
            "refine": _gem_cutter_refine,
        },
        KILN_BLOCK: {
            "name": "Alchemical Kiln",
            "description": "Fires the rock, raising Purity +0.25. Cannot re-fire. Rock stays in collection.",
            "can_use": _kiln_can_use,
            "refine": _kiln_refine,
            "upgrade_preview": lambda rock: f"Purity: {rock.purity:.2f}  \u2192  {min(1.0, rock.purity + 0.25):.2f}",
        },
        RESONANCE_BLOCK: {
            "name": "Resonance Chamber",
            "description": "Extracts void essence from voidtouched rocks. Fired rocks yield double.",
            "can_use": _resonance_can_use,
            "refine": _resonance_refine,
        },
    }


REFINERY_EQUIPMENT = None  # initialized lazily after pygame/blocks are loaded


def get_refinery_equipment():
    global REFINERY_EQUIPMENT
    if REFINERY_EQUIPMENT is None:
        REFINERY_EQUIPMENT = build_refinery_equipment()
    return REFINERY_EQUIPMENT
