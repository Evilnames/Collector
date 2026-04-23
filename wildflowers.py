import math
import random
import pygame
from dataclasses import dataclass, field


@dataclass
class Wildflower:
    uid: str
    flower_type: str
    rarity: str
    bloom_stage: str       # "bud" | "open" | "full"
    primary_color: tuple
    secondary_color: tuple
    center_color: tuple
    petal_pattern: str     # "simple" | "daisy" | "trumpet" | "cluster"
    petal_count: int
    fragrance: float       # 0.0–1.0
    vibrancy: float        # 0.0–1.0
    specials: list
    biodome_found: str
    seed: int


# ---------------------------------------------------------------------------
# Flower type definitions
# ---------------------------------------------------------------------------

WILDFLOWER_TYPES = {
    "daisy": {
        "rarity_pool": ["common", "common", "common", "uncommon"],
        "color_pool": [((255, 255, 255), (240, 235, 210)), ((245, 240, 220), (255, 250, 230))],
        "center_colors": [(255, 210, 50), (240, 195, 30)],
        "patterns": ["daisy", "daisy", "simple"],
        "petal_counts": [10, 12, 14],
        "preferred_biodomes": ["temperate", "savanna"],
    },
    "buttercup": {
        "rarity_pool": ["common", "common", "uncommon"],
        "color_pool": [((255, 215, 0), (255, 240, 80)), ((245, 200, 20), (255, 230, 60))],
        "center_colors": [(180, 155, 0), (200, 170, 10)],
        "patterns": ["simple", "simple"],
        "petal_counts": [5, 6],
        "preferred_biodomes": ["temperate"],
    },
    "clover": {
        "rarity_pool": ["common", "common", "common"],
        "color_pool": [((210, 115, 175), (255, 175, 220)), ((195, 100, 160), (240, 160, 210))],
        "center_colors": [(165, 75, 135), (180, 85, 150)],
        "patterns": ["cluster", "cluster"],
        "petal_counts": [4],
        "preferred_biodomes": ["temperate", "boreal"],
    },
    "cornflower": {
        "rarity_pool": ["common", "uncommon"],
        "color_pool": [((65, 115, 215), (95, 155, 255)), ((50, 95, 200), (80, 135, 245))],
        "center_colors": [(35, 70, 170), (45, 80, 185)],
        "patterns": ["daisy", "simple"],
        "petal_counts": [8, 10],
        "preferred_biodomes": ["temperate", "savanna"],
    },
    "fireweed": {
        "rarity_pool": ["common", "common", "uncommon"],
        "color_pool": [((215, 75, 145), (255, 135, 195)), ((200, 60, 130), (245, 120, 180))],
        "center_colors": [(170, 35, 105), (185, 45, 115)],
        "patterns": ["cluster", "simple"],
        "petal_counts": [4],
        "preferred_biodomes": ["boreal"],
    },
    "lupine": {
        "rarity_pool": ["common", "uncommon", "rare"],
        "color_pool": [((115, 65, 215), (175, 125, 255)), ((55, 95, 205), (95, 145, 250))],
        "center_colors": [(75, 35, 175), (45, 75, 170)],
        "patterns": ["cluster", "cluster"],
        "petal_counts": [5, 6],
        "preferred_biodomes": ["boreal"],
    },
    "arctic_poppy": {
        "rarity_pool": ["uncommon", "uncommon", "rare"],
        "color_pool": [((255, 195, 45), (255, 235, 100)), ((250, 155, 25), (255, 215, 75))],
        "center_colors": [(195, 145, 15), (210, 160, 20)],
        "patterns": ["simple", "trumpet"],
        "petal_counts": [4, 6],
        "preferred_biodomes": ["boreal"],
    },
    "bluebell": {
        "rarity_pool": ["common", "common", "uncommon"],
        "color_pool": [((95, 135, 215), (155, 195, 255)), ((80, 115, 200), (140, 175, 245))],
        "center_colors": [(60, 90, 180), (70, 100, 195)],
        "patterns": ["trumpet", "cluster"],
        "petal_counts": [5, 6],
        "preferred_biodomes": ["birch_forest"],
    },
    "wood_anemone": {
        "rarity_pool": ["common", "uncommon", "rare"],
        "color_pool": [((255, 252, 252), (225, 225, 255)), ((240, 235, 255), (220, 215, 250))],
        "center_colors": [(215, 195, 45), (225, 205, 55)],
        "patterns": ["simple", "daisy"],
        "petal_counts": [5, 6, 7],
        "preferred_biodomes": ["birch_forest"],
    },
    "trillium": {
        "rarity_pool": ["uncommon", "uncommon", "rare", "epic"],
        "color_pool": [((255, 252, 252), (255, 215, 235)), ((235, 175, 215), (255, 205, 235))],
        "center_colors": [(255, 215, 195), (250, 205, 185)],
        "patterns": ["simple"],
        "petal_counts": [3],
        "preferred_biodomes": ["birch_forest"],
    },
    "orchid": {
        "rarity_pool": ["uncommon", "rare", "rare", "epic"],
        "color_pool": [((195, 95, 250), (235, 155, 255)), ((250, 145, 195), (255, 195, 235))],
        "center_colors": [(255, 215, 175), (250, 205, 160)],
        "patterns": ["trumpet", "simple"],
        "petal_counts": [5, 6],
        "preferred_biodomes": ["jungle"],
    },
    "heliconia": {
        "rarity_pool": ["uncommon", "rare", "epic"],
        "color_pool": [((250, 75, 45), (255, 195, 0)), ((255, 115, 0), (255, 215, 45))],
        "center_colors": [(255, 250, 45), (250, 240, 35)],
        "patterns": ["trumpet", "simple"],
        "petal_counts": [4, 5],
        "preferred_biodomes": ["jungle", "tropical"],
    },
    "passion_flower": {
        "rarity_pool": ["rare", "rare", "epic", "legendary"],
        "color_pool": [((195, 75, 250), (255, 195, 255)), ((95, 45, 195), (195, 145, 250))],
        "center_colors": [(255, 255, 195), (250, 250, 180)],
        "patterns": ["daisy", "cluster"],
        "petal_counts": [10, 12],
        "preferred_biodomes": ["jungle"],
    },
    "iris": {
        "rarity_pool": ["common", "uncommon", "rare"],
        "color_pool": [((115, 75, 195), (175, 145, 250)), ((65, 95, 195), (135, 165, 250))],
        "center_colors": [(255, 235, 145), (250, 225, 130)],
        "patterns": ["trumpet", "simple"],
        "petal_counts": [6],
        "preferred_biodomes": ["wetland"],
    },
    "marsh_marigold": {
        "rarity_pool": ["common", "common", "uncommon"],
        "color_pool": [((255, 205, 0), (255, 235, 75)), ((245, 190, 15), (255, 225, 60))],
        "center_colors": [(195, 155, 0), (205, 165, 10)],
        "patterns": ["simple"],
        "petal_counts": [5, 6],
        "preferred_biodomes": ["wetland"],
    },
    "water_lily": {
        "rarity_pool": ["uncommon", "rare", "epic"],
        "color_pool": [((255, 195, 215), (255, 235, 250)), ((255, 252, 252), (215, 235, 255))],
        "center_colors": [(255, 215, 95), (250, 205, 80)],
        "patterns": ["simple", "daisy"],
        "petal_counts": [8, 12, 16],
        "preferred_biodomes": ["wetland"],
    },
    "redwood_violet": {
        "rarity_pool": ["uncommon", "rare", "epic"],
        "color_pool": [((155, 75, 195), (215, 145, 250)), ((140, 60, 180), (200, 130, 240))],
        "center_colors": [(255, 195, 95), (250, 185, 80)],
        "patterns": ["simple"],
        "petal_counts": [5],
        "preferred_biodomes": ["redwood"],
    },
    "bleeding_heart": {
        "rarity_pool": ["rare", "rare", "epic", "legendary"],
        "color_pool": [((215, 55, 115), (255, 135, 175)), ((200, 40, 100), (250, 120, 160))],
        "center_colors": [(255, 215, 215), (255, 205, 205)],
        "patterns": ["trumpet"],
        "petal_counts": [2, 4],
        "preferred_biodomes": ["redwood"],
    },
    "hibiscus": {
        "rarity_pool": ["uncommon", "rare", "epic"],
        "color_pool": [((255, 45, 95), (255, 175, 95)), ((255, 115, 0), (255, 235, 75))],
        "center_colors": [(255, 255, 145), (250, 250, 130)],
        "patterns": ["trumpet", "simple"],
        "petal_counts": [5],
        "preferred_biodomes": ["tropical"],
    },
    "plumeria": {
        "rarity_pool": ["rare", "epic", "legendary"],
        "color_pool": [((255, 235, 175), (255, 195, 95)), ((255, 175, 195), (255, 235, 235))],
        "center_colors": [(255, 215, 95), (250, 205, 80)],
        "patterns": ["simple"],
        "petal_counts": [5],
        "preferred_biodomes": ["tropical"],
    },
    "sunflower": {
        "rarity_pool": ["common", "common", "uncommon"],
        "color_pool": [((255, 195, 0), (255, 235, 75)), ((245, 180, 15), (255, 225, 60))],
        "center_colors": [(95, 55, 15), (80, 45, 10)],
        "patterns": ["daisy"],
        "petal_counts": [14, 16, 18],
        "preferred_biodomes": ["savanna"],
    },
    "marigold": {
        "rarity_pool": ["common", "uncommon"],
        "color_pool": [((255, 135, 0), (255, 195, 45)), ((255, 95, 0), (255, 165, 45))],
        "center_colors": [(195, 75, 0), (180, 65, 0)],
        "patterns": ["daisy", "cluster"],
        "petal_counts": [10, 12],
        "preferred_biodomes": ["savanna", "temperate"],
    },
    "desert_rose": {
        "rarity_pool": ["uncommon", "rare", "epic", "legendary"],
        "color_pool": [((215, 95, 135), (255, 175, 195)), ((195, 75, 95), (250, 155, 175))],
        "center_colors": [(255, 215, 215), (250, 205, 205)],
        "patterns": ["simple", "trumpet"],
        "petal_counts": [5, 6],
        "preferred_biodomes": ["wasteland"],
    },
    "sand_lily": {
        "rarity_pool": ["rare", "epic", "legendary"],
        "color_pool": [((255, 235, 195), (255, 250, 235)), ((235, 215, 175), (255, 245, 225))],
        "center_colors": [(215, 175, 95), (205, 165, 80)],
        "patterns": ["simple"],
        "petal_counts": [6],
        "preferred_biodomes": ["wasteland"],
    },
    "glowcap_bloom": {
        "rarity_pool": ["uncommon", "rare", "epic"],
        "color_pool": [((95, 250, 175), (195, 255, 235)), ((75, 215, 145), (175, 250, 215))],
        "center_colors": [(255, 255, 145), (250, 255, 130)],
        "patterns": ["cluster"],
        "petal_counts": [6, 8],
        "preferred_biodomes": ["fungal"],
    },
    "mycelium_lily": {
        "rarity_pool": ["rare", "epic", "legendary"],
        "color_pool": [((195, 95, 250), (235, 175, 255)), ((155, 45, 215), (215, 145, 250))],
        "center_colors": [(255, 195, 95), (250, 185, 80)],
        "patterns": ["trumpet", "cluster"],
        "petal_counts": [4, 6],
        "preferred_biodomes": ["fungal"],
    },

    # ---- 25 new types ----

    # temperate / birch_forest
    "foxglove": {
        "rarity_pool": ["uncommon", "uncommon", "rare"],
        "color_pool": [((220, 80, 200), (255, 160, 240)), ((200, 50, 180), (245, 130, 225))],
        "center_colors": [(255, 230, 240), (250, 220, 235)],
        "patterns": ["cluster", "trumpet"],
        "petal_counts": [4, 5],
        "preferred_biodomes": ["temperate", "birch_forest"],
    },
    "lavender": {
        "rarity_pool": ["common", "common", "uncommon"],
        "color_pool": [((175, 140, 230), (210, 180, 255)), ((155, 120, 210), (195, 165, 245))],
        "center_colors": [(145, 100, 200), (160, 115, 215)],
        "patterns": ["cluster", "cluster"],
        "petal_counts": [5, 6],
        "preferred_biodomes": ["temperate", "savanna"],
    },
    "poppy": {
        "rarity_pool": ["common", "uncommon", "rare"],
        "color_pool": [((240, 50, 45), (255, 135, 110)), ((235, 30, 25), (255, 110, 90))],
        "center_colors": [(25, 20, 20), (30, 25, 25)],
        "patterns": ["simple", "simple"],
        "petal_counts": [4, 6],
        "preferred_biodomes": ["temperate", "boreal"],
    },
    "cowslip": {
        "rarity_pool": ["common", "common", "uncommon"],
        "color_pool": [((255, 195, 30), (255, 230, 100)), ((245, 180, 15), (255, 220, 80))],
        "center_colors": [(200, 140, 0), (210, 150, 10)],
        "patterns": ["cluster", "simple"],
        "petal_counts": [5],
        "preferred_biodomes": ["temperate"],
    },

    # boreal
    "edelweiss": {
        "rarity_pool": ["rare", "rare", "epic", "legendary"],
        "color_pool": [((250, 248, 248), (230, 225, 225)), ((245, 242, 240), (220, 215, 215))],
        "center_colors": [(255, 230, 100), (250, 220, 80)],
        "patterns": ["daisy", "simple"],
        "petal_counts": [6, 8],
        "preferred_biodomes": ["boreal"],
    },
    "cloudberry_flower": {
        "rarity_pool": ["uncommon", "rare"],
        "color_pool": [((255, 252, 248), (240, 230, 220)), ((250, 245, 240), (235, 225, 215))],
        "center_colors": [(255, 210, 60), (250, 200, 50)],
        "patterns": ["simple"],
        "petal_counts": [5],
        "preferred_biodomes": ["boreal"],
    },
    "willow_herb": {
        "rarity_pool": ["common", "uncommon"],
        "color_pool": [((225, 100, 185), (255, 165, 230)), ((210, 80, 170), (245, 148, 218))],
        "center_colors": [(190, 55, 150), (200, 65, 160)],
        "patterns": ["cluster", "simple"],
        "petal_counts": [4],
        "preferred_biodomes": ["boreal"],
    },

    # birch_forest
    "lily_of_valley": {
        "rarity_pool": ["uncommon", "rare", "epic"],
        "color_pool": [((252, 252, 252), (235, 235, 250)), ((248, 248, 248), (230, 230, 245))],
        "center_colors": [(240, 240, 240), (235, 235, 235)],
        "patterns": ["cluster", "trumpet"],
        "petal_counts": [4, 5],
        "preferred_biodomes": ["birch_forest"],
    },
    "spring_beauty": {
        "rarity_pool": ["common", "uncommon", "rare"],
        "color_pool": [((250, 225, 240), (255, 245, 250)), ((230, 195, 220), (250, 225, 242))],
        "center_colors": [(255, 200, 200), (250, 190, 190)],
        "patterns": ["simple"],
        "petal_counts": [5],
        "preferred_biodomes": ["birch_forest"],
    },
    "wild_rose": {
        "rarity_pool": ["uncommon", "rare", "epic"],
        "color_pool": [((250, 160, 185), (255, 205, 225)), ((240, 130, 160), (255, 185, 210))],
        "center_colors": [(255, 215, 80), (250, 205, 65)],
        "patterns": ["simple", "daisy"],
        "petal_counts": [5],
        "preferred_biodomes": ["birch_forest", "temperate"],
    },

    # jungle
    "bromeliad": {
        "rarity_pool": ["uncommon", "rare", "epic"],
        "color_pool": [((255, 80, 80), (255, 200, 50)), ((255, 55, 55), (255, 185, 30))],
        "center_colors": [(255, 240, 80), (255, 230, 60)],
        "patterns": ["trumpet", "simple"],
        "petal_counts": [3, 4],
        "preferred_biodomes": ["jungle"],
    },
    "anthurium": {
        "rarity_pool": ["uncommon", "rare", "epic"],
        "color_pool": [((240, 50, 50), (255, 120, 120)), ((255, 80, 80), (255, 150, 150))],
        "center_colors": [(255, 230, 100), (250, 220, 80)],
        "patterns": ["simple", "trumpet"],
        "petal_counts": [1, 2],
        "preferred_biodomes": ["jungle", "tropical"],
    },
    "giant_lotus": {
        "rarity_pool": ["rare", "epic", "legendary"],
        "color_pool": [((255, 215, 235), (255, 240, 250)), ((255, 185, 215), (255, 225, 245))],
        "center_colors": [(255, 235, 120), (250, 225, 100)],
        "patterns": ["daisy", "simple"],
        "petal_counts": [12, 16, 20],
        "preferred_biodomes": ["jungle", "wetland"],
    },

    # wetland
    "cattail_bloom": {
        "rarity_pool": ["common", "common", "uncommon"],
        "color_pool": [((120, 85, 50), (160, 120, 80)), ((105, 70, 40), (145, 105, 65))],
        "center_colors": [(85, 55, 25), (95, 65, 35)],
        "patterns": ["cluster"],
        "petal_counts": [4, 5],
        "preferred_biodomes": ["wetland"],
    },
    "pickerel_weed": {
        "rarity_pool": ["common", "uncommon"],
        "color_pool": [((90, 100, 225), (140, 155, 255)), ((75, 85, 210), (120, 135, 245))],
        "center_colors": [(220, 235, 255), (210, 225, 250)],
        "patterns": ["cluster", "simple"],
        "petal_counts": [5, 6],
        "preferred_biodomes": ["wetland"],
    },
    "lotus": {
        "rarity_pool": ["rare", "epic", "legendary"],
        "color_pool": [((255, 175, 205), (255, 230, 245)), ((255, 145, 185), (255, 215, 240))],
        "center_colors": [(255, 230, 80), (250, 220, 65)],
        "patterns": ["daisy", "simple"],
        "petal_counts": [10, 14, 18],
        "preferred_biodomes": ["wetland"],
    },

    # redwood
    "redwood_sorrel": {
        "rarity_pool": ["common", "uncommon", "rare"],
        "color_pool": [((250, 230, 235), (255, 248, 250)), ((240, 215, 225), (250, 238, 244))],
        "center_colors": [(255, 210, 180), (250, 200, 170)],
        "patterns": ["simple"],
        "petal_counts": [5],
        "preferred_biodomes": ["redwood"],
    },
    "fairy_slipper": {
        "rarity_pool": ["rare", "epic", "legendary"],
        "color_pool": [((215, 100, 185), (255, 170, 230)), ((195, 75, 165), (245, 150, 215))],
        "center_colors": [(255, 240, 200), (250, 230, 185)],
        "patterns": ["trumpet"],
        "petal_counts": [3, 5],
        "preferred_biodomes": ["redwood"],
    },

    # tropical
    "bird_of_paradise": {
        "rarity_pool": ["rare", "epic", "legendary"],
        "color_pool": [((255, 140, 0), (0, 100, 200)), ((255, 160, 20), (20, 120, 220))],
        "center_colors": [(255, 255, 255), (240, 245, 255)],
        "patterns": ["trumpet", "simple"],
        "petal_counts": [3, 4],
        "preferred_biodomes": ["tropical", "jungle"],
    },
    "torch_ginger": {
        "rarity_pool": ["uncommon", "rare", "epic"],
        "color_pool": [((230, 40, 60), (255, 140, 100)), ((215, 25, 45), (245, 120, 80))],
        "center_colors": [(255, 200, 80), (250, 190, 65)],
        "patterns": ["cluster", "trumpet"],
        "petal_counts": [5, 6],
        "preferred_biodomes": ["tropical"],
    },
    "frangipani": {
        "rarity_pool": ["rare", "epic", "legendary"],
        "color_pool": [((255, 245, 210), (255, 210, 100)), ((255, 230, 185), (255, 195, 80))],
        "center_colors": [(255, 200, 50), (250, 190, 40)],
        "patterns": ["simple"],
        "petal_counts": [5],
        "preferred_biodomes": ["tropical"],
    },

    # savanna
    "acacia_blossom": {
        "rarity_pool": ["common", "uncommon", "rare"],
        "color_pool": [((255, 215, 60), (255, 240, 140)), ((245, 200, 40), (255, 230, 120))],
        "center_colors": [(200, 155, 10), (210, 165, 20)],
        "patterns": ["cluster", "daisy"],
        "petal_counts": [6, 8],
        "preferred_biodomes": ["savanna"],
    },
    "king_protea": {
        "rarity_pool": ["rare", "epic", "legendary"],
        "color_pool": [((215, 90, 120), (255, 175, 200)), ((195, 65, 100), (245, 155, 180))],
        "center_colors": [(255, 240, 230), (250, 235, 225)],
        "patterns": ["daisy"],
        "petal_counts": [16, 20, 24],
        "preferred_biodomes": ["savanna"],
    },

    # wasteland
    "prickly_pear_bloom": {
        "rarity_pool": ["uncommon", "rare", "epic"],
        "color_pool": [((255, 210, 60), (255, 245, 130)), ((255, 155, 45), (255, 215, 110))],
        "center_colors": [(230, 165, 20), (240, 175, 30)],
        "patterns": ["simple", "daisy"],
        "petal_counts": [6, 8],
        "preferred_biodomes": ["wasteland"],
    },
    "dune_poppy": {
        "rarity_pool": ["rare", "epic", "legendary"],
        "color_pool": [((255, 240, 195), (255, 255, 230)), ((245, 225, 175), (255, 248, 220))],
        "center_colors": [(210, 185, 100), (220, 195, 110)],
        "patterns": ["simple"],
        "petal_counts": [4, 6],
        "preferred_biodomes": ["wasteland"],
    },
    "ghost_plant_bloom": {
        "rarity_pool": ["epic", "legendary"],
        "color_pool": [((235, 240, 255), (210, 220, 250)), ((225, 232, 252), (200, 212, 245))],
        "center_colors": [(240, 245, 255), (232, 238, 252)],
        "patterns": ["simple", "trumpet"],
        "petal_counts": [5],
        "preferred_biodomes": ["wasteland"],
    },

    # fungal
    "inkwell_cap": {
        "rarity_pool": ["uncommon", "rare", "epic"],
        "color_pool": [((30, 20, 50), (130, 80, 220)), ((20, 15, 40), (110, 65, 200))],
        "center_colors": [(200, 160, 255), (185, 145, 245)],
        "patterns": ["simple", "trumpet"],
        "petal_counts": [5, 6],
        "preferred_biodomes": ["fungal"],
    },
    "twilight_bell": {
        "rarity_pool": ["rare", "epic", "legendary"],
        "color_pool": [((55, 30, 120), (180, 120, 255)), ((40, 20, 105), (165, 100, 245))],
        "center_colors": [(220, 200, 255), (210, 190, 250)],
        "patterns": ["trumpet", "cluster"],
        "petal_counts": [4, 5],
        "preferred_biodomes": ["fungal"],
    },

    # ---- 25 more types ----

    # temperate
    "forget_me_not": {
        "rarity_pool": ["common", "common", "uncommon"],
        "color_pool": [((120, 165, 240), (175, 210, 255)), ((100, 145, 225), (155, 195, 250))],
        "center_colors": [(255, 240, 100), (250, 230, 80)],
        "patterns": ["daisy", "cluster"],
        "petal_counts": [5],
        "preferred_biodomes": ["temperate"],
    },
    "sweet_pea": {
        "rarity_pool": ["common", "uncommon", "rare"],
        "color_pool": [((230, 160, 215), (255, 210, 245)), ((200, 130, 190), (245, 190, 235))],
        "center_colors": [(255, 220, 240), (250, 210, 232)],
        "patterns": ["cluster", "trumpet"],
        "petal_counts": [4, 5],
        "preferred_biodomes": ["temperate"],
    },
    "snapdragon": {
        "rarity_pool": ["uncommon", "rare"],
        "color_pool": [((255, 120, 40), (255, 210, 80)), ((230, 60, 60), (255, 160, 60))],
        "center_colors": [(255, 240, 160), (250, 230, 140)],
        "patterns": ["trumpet", "cluster"],
        "petal_counts": [3, 4],
        "preferred_biodomes": ["temperate"],
    },

    # boreal
    "mountain_avens": {
        "rarity_pool": ["uncommon", "rare", "epic"],
        "color_pool": [((252, 250, 248), (235, 232, 228)), ((248, 245, 240), (228, 224, 220))],
        "center_colors": [(255, 220, 60), (248, 210, 45)],
        "patterns": ["daisy"],
        "petal_counts": [8],
        "preferred_biodomes": ["boreal"],
    },
    "larch_bloom": {
        "rarity_pool": ["common", "uncommon"],
        "color_pool": [((230, 170, 205), (255, 210, 240)), ((215, 150, 190), (245, 195, 228))],
        "center_colors": [(200, 125, 170), (210, 135, 180)],
        "patterns": ["cluster"],
        "petal_counts": [4, 5],
        "preferred_biodomes": ["boreal"],
    },
    "bunchberry": {
        "rarity_pool": ["common", "common", "uncommon"],
        "color_pool": [((252, 252, 252), (230, 235, 225)), ((245, 248, 240), (220, 228, 215))],
        "center_colors": [(200, 210, 150), (190, 200, 140)],
        "patterns": ["simple"],
        "petal_counts": [4],
        "preferred_biodomes": ["boreal"],
    },

    # birch_forest
    "hepatica": {
        "rarity_pool": ["uncommon", "rare"],
        "color_pool": [((130, 110, 215), (185, 170, 255)), ((100, 80, 195), (158, 143, 245))],
        "center_colors": [(255, 250, 220), (248, 242, 210)],
        "patterns": ["simple", "daisy"],
        "petal_counts": [6, 7],
        "preferred_biodomes": ["birch_forest"],
    },
    "wood_violet": {
        "rarity_pool": ["common", "common", "uncommon"],
        "color_pool": [((145, 95, 200), (195, 155, 245)), ((120, 70, 180), (172, 132, 228))],
        "center_colors": [(255, 240, 120), (248, 232, 100)],
        "patterns": ["simple"],
        "petal_counts": [5],
        "preferred_biodomes": ["birch_forest"],
    },

    # jungle
    "jungle_jasmine": {
        "rarity_pool": ["uncommon", "rare"],
        "color_pool": [((252, 250, 235), (255, 255, 248)), ((240, 235, 215), (250, 248, 235))],
        "center_colors": [(255, 230, 80), (248, 220, 65)],
        "patterns": ["daisy", "simple"],
        "petal_counts": [5, 6],
        "preferred_biodomes": ["jungle"],
    },
    "pitcher_plant_flower": {
        "rarity_pool": ["rare", "epic", "legendary"],
        "color_pool": [((180, 30, 30), (60, 140, 60)), ((155, 20, 20), (45, 120, 45))],
        "center_colors": [(220, 200, 60), (210, 190, 45)],
        "patterns": ["trumpet"],
        "petal_counts": [3, 4],
        "preferred_biodomes": ["jungle"],
    },

    # wetland
    "bogbean": {
        "rarity_pool": ["common", "uncommon"],
        "color_pool": [((252, 240, 248), (255, 250, 252)), ((240, 222, 238), (250, 242, 248))],
        "center_colors": [(230, 230, 240), (222, 222, 234)],
        "patterns": ["daisy", "simple"],
        "petal_counts": [5],
        "preferred_biodomes": ["wetland"],
    },
    "swamp_rose": {
        "rarity_pool": ["uncommon", "rare", "epic"],
        "color_pool": [((235, 140, 165), (255, 195, 215)), ((218, 115, 145), (248, 175, 200))],
        "center_colors": [(255, 215, 70), (248, 205, 55)],
        "patterns": ["simple", "daisy"],
        "petal_counts": [5],
        "preferred_biodomes": ["wetland"],
    },

    # redwood
    "calypso_orchid": {
        "rarity_pool": ["rare", "epic", "legendary"],
        "color_pool": [((225, 110, 195), (255, 175, 235)), ((205, 80, 175), (245, 150, 220))],
        "center_colors": [(255, 235, 145), (250, 225, 130)],
        "patterns": ["trumpet"],
        "petal_counts": [5],
        "preferred_biodomes": ["redwood"],
    },
    "ghost_orchid": {
        "rarity_pool": ["epic", "legendary"],
        "color_pool": [((245, 248, 252), (215, 228, 245)), ((238, 242, 250), (205, 220, 240))],
        "center_colors": [(248, 248, 252), (240, 242, 248)],
        "patterns": ["trumpet", "simple"],
        "petal_counts": [4, 5],
        "preferred_biodomes": ["redwood"],
    },

    # tropical
    "ylang_ylang": {
        "rarity_pool": ["uncommon", "rare"],
        "color_pool": [((215, 210, 80), (255, 250, 150)), ((195, 190, 55), (245, 238, 128))],
        "center_colors": [(175, 165, 30), (185, 175, 40)],
        "patterns": ["daisy", "simple"],
        "petal_counts": [6],
        "preferred_biodomes": ["tropical"],
    },
    "bougainvillea": {
        "rarity_pool": ["common", "uncommon"],
        "color_pool": [((240, 60, 180), (255, 140, 225)), ((215, 35, 155), (248, 115, 210))],
        "center_colors": [(255, 255, 255), (250, 248, 245)],
        "patterns": ["cluster"],
        "petal_counts": [3, 4],
        "preferred_biodomes": ["tropical"],
    },
    "rafflesia": {
        "rarity_pool": ["epic", "legendary"],
        "color_pool": [((180, 35, 35), (255, 200, 180)), ((155, 20, 20), (240, 175, 155))],
        "center_colors": [(80, 20, 20), (90, 25, 25)],
        "patterns": ["daisy"],
        "petal_counts": [5],
        "preferred_biodomes": ["tropical", "jungle"],
    },

    # savanna
    "lion_tooth": {
        "rarity_pool": ["common", "common", "uncommon"],
        "color_pool": [((255, 205, 10), (255, 240, 90)), ((245, 190, 0), (255, 230, 70))],
        "center_colors": [(195, 145, 0), (205, 155, 10)],
        "patterns": ["daisy"],
        "petal_counts": [14, 18, 22],
        "preferred_biodomes": ["savanna", "temperate"],
    },
    "red_hot_poker": {
        "rarity_pool": ["uncommon", "rare", "epic"],
        "color_pool": [((255, 60, 20), (255, 195, 30)), ((240, 40, 10), (248, 180, 15))],
        "center_colors": [(255, 240, 60), (248, 228, 45)],
        "patterns": ["cluster", "trumpet"],
        "petal_counts": [5, 6],
        "preferred_biodomes": ["savanna"],
    },

    # wasteland
    "barrel_cactus_bloom": {
        "rarity_pool": ["uncommon", "rare", "epic"],
        "color_pool": [((255, 195, 30), (255, 240, 100)), ((255, 130, 20), (255, 205, 75))],
        "center_colors": [(215, 155, 10), (225, 165, 20)],
        "patterns": ["simple", "daisy"],
        "petal_counts": [8, 10],
        "preferred_biodomes": ["wasteland"],
    },
    "straw_flower": {
        "rarity_pool": ["uncommon", "rare", "epic"],
        "color_pool": [((240, 155, 30), (255, 215, 80)), ((210, 50, 50), (255, 135, 90))],
        "center_colors": [(255, 235, 80), (248, 225, 65)],
        "patterns": ["daisy"],
        "petal_counts": [12, 16],
        "preferred_biodomes": ["wasteland"],
    },
    "tumblegrass_flower": {
        "rarity_pool": ["common", "uncommon"],
        "color_pool": [((245, 242, 230), (255, 250, 240)), ((232, 228, 215), (248, 244, 232))],
        "center_colors": [(215, 205, 165), (205, 195, 155)],
        "patterns": ["cluster", "simple"],
        "petal_counts": [4, 5],
        "preferred_biodomes": ["wasteland"],
    },

    # fungal
    "spore_lily": {
        "rarity_pool": ["rare", "epic"],
        "color_pool": [((60, 220, 215), (160, 255, 252)), ((40, 195, 190), (138, 245, 240))],
        "center_colors": [(220, 255, 252), (210, 248, 245)],
        "patterns": ["simple", "trumpet"],
        "petal_counts": [6],
        "preferred_biodomes": ["fungal"],
    },
    "nether_belle": {
        "rarity_pool": ["epic", "legendary"],
        "color_pool": [((85, 10, 15), (210, 50, 70)), ((70, 5, 10), (190, 35, 55))],
        "center_colors": [(255, 40, 55), (248, 30, 45)],
        "patterns": ["trumpet"],
        "petal_counts": [4, 5],
        "preferred_biodomes": ["fungal"],
    },
    "cave_daisy": {
        "rarity_pool": ["uncommon", "rare"],
        "color_pool": [((215, 218, 225), (240, 242, 248)), ((198, 202, 212), (228, 232, 240))],
        "center_colors": [(180, 185, 195), (172, 178, 188)],
        "patterns": ["daisy", "simple"],
        "petal_counts": [10, 12],
        "preferred_biodomes": ["fungal"],
    },

    # ---- 25 more types ----

    # temperate
    "chamomile": {
        "rarity_pool": ["common", "common", "common", "uncommon"],
        "color_pool": [((252, 250, 235), (255, 255, 245)), ((240, 238, 220), (250, 248, 235))],
        "center_colors": [(255, 220, 50), (248, 210, 38)],
        "patterns": ["daisy", "daisy"],
        "petal_counts": [14, 18],
        "preferred_biodomes": ["temperate"],
    },
    "ox_eye_daisy": {
        "rarity_pool": ["common", "common", "uncommon"],
        "color_pool": [((252, 252, 252), (230, 240, 230)), ((242, 245, 242), (220, 232, 220))],
        "center_colors": [(255, 215, 35), (248, 205, 25)],
        "patterns": ["daisy"],
        "petal_counts": [16, 20, 24],
        "preferred_biodomes": ["temperate"],
    },

    # boreal
    "alpine_aster": {
        "rarity_pool": ["uncommon", "rare", "epic"],
        "color_pool": [((140, 100, 220), (195, 160, 255)), ((110, 75, 200), (170, 135, 245))],
        "center_colors": [(255, 220, 55), (248, 210, 42)],
        "patterns": ["daisy", "simple"],
        "petal_counts": [12, 16],
        "preferred_biodomes": ["boreal"],
    },
    "moss_campion": {
        "rarity_pool": ["uncommon", "rare"],
        "color_pool": [((230, 105, 175), (255, 165, 215)), ((215, 85, 158), (245, 148, 202))],
        "center_colors": [(255, 235, 200), (248, 225, 188)],
        "patterns": ["simple"],
        "petal_counts": [5],
        "preferred_biodomes": ["boreal"],
    },
    "dwarf_fireweed": {
        "rarity_pool": ["common", "common", "uncommon"],
        "color_pool": [((220, 90, 155), (255, 155, 205)), ((205, 70, 138), (242, 135, 190))],
        "center_colors": [(180, 50, 115), (192, 60, 125)],
        "patterns": ["cluster", "simple"],
        "petal_counts": [4],
        "preferred_biodomes": ["boreal"],
    },

    # birch_forest
    "wood_sorrel": {
        "rarity_pool": ["common", "common", "uncommon"],
        "color_pool": [((252, 245, 252), (235, 225, 250)), ((245, 235, 248), (225, 212, 242))],
        "center_colors": [(255, 235, 155), (248, 225, 140)],
        "patterns": ["simple"],
        "petal_counts": [5],
        "preferred_biodomes": ["birch_forest"],
    },
    "jack_in_pulpit": {
        "rarity_pool": ["rare", "epic", "legendary"],
        "color_pool": [((75, 130, 55), (155, 210, 130)), ((55, 110, 40), (135, 192, 112))],
        "center_colors": [(95, 75, 30), (108, 85, 38)],
        "patterns": ["trumpet"],
        "petal_counts": [1],
        "preferred_biodomes": ["birch_forest"],
    },

    # jungle
    "jungle_lily": {
        "rarity_pool": ["uncommon", "rare", "epic"],
        "color_pool": [((255, 85, 30), (255, 200, 60)), ((240, 60, 20), (255, 180, 40))],
        "center_colors": [(255, 245, 90), (248, 235, 75)],
        "patterns": ["trumpet", "simple"],
        "petal_counts": [6],
        "preferred_biodomes": ["jungle"],
    },
    "cannonball_flower": {
        "rarity_pool": ["rare", "epic", "legendary"],
        "color_pool": [((215, 55, 80), (255, 175, 55)), ((195, 40, 65), (245, 158, 40))],
        "center_colors": [(255, 255, 180), (248, 248, 165)],
        "patterns": ["cluster"],
        "petal_counts": [6, 8],
        "preferred_biodomes": ["jungle"],
    },
    "torch_lily": {
        "rarity_pool": ["uncommon", "rare", "epic"],
        "color_pool": [((255, 65, 25), (255, 195, 45)), ((235, 45, 10), (248, 178, 28))],
        "center_colors": [(255, 240, 70), (248, 230, 55)],
        "patterns": ["cluster", "trumpet"],
        "petal_counts": [5, 6],
        "preferred_biodomes": ["jungle"],
    },

    # wetland
    "arrowhead_bloom": {
        "rarity_pool": ["common", "common", "uncommon"],
        "color_pool": [((252, 252, 252), (230, 238, 255)), ((240, 242, 252), (218, 228, 248))],
        "center_colors": [(255, 220, 200), (248, 210, 188)],
        "patterns": ["simple"],
        "petal_counts": [3],
        "preferred_biodomes": ["wetland"],
    },
    "frog_bit": {
        "rarity_pool": ["uncommon", "rare"],
        "color_pool": [((250, 248, 252), (235, 232, 248)), ((242, 240, 248), (225, 222, 240))],
        "center_colors": [(230, 215, 255), (220, 205, 248)],
        "patterns": ["simple"],
        "petal_counts": [3],
        "preferred_biodomes": ["wetland"],
    },

    # redwood
    "redwood_lily": {
        "rarity_pool": ["uncommon", "rare", "epic"],
        "color_pool": [((235, 115, 40), (255, 195, 100)), ((218, 95, 25), (245, 178, 82))],
        "center_colors": [(195, 75, 15), (208, 88, 22)],
        "patterns": ["trumpet", "simple"],
        "petal_counts": [6],
        "preferred_biodomes": ["redwood"],
    },
    "twinflower": {
        "rarity_pool": ["rare", "epic"],
        "color_pool": [((240, 185, 220), (255, 220, 245)), ((225, 162, 202), (245, 205, 235))],
        "center_colors": [(255, 230, 240), (248, 222, 232)],
        "patterns": ["trumpet"],
        "petal_counts": [5],
        "preferred_biodomes": ["redwood"],
    },
    "vanilla_leaf_bloom": {
        "rarity_pool": ["uncommon", "rare"],
        "color_pool": [((252, 250, 248), (235, 232, 228)), ((245, 242, 238), (225, 222, 218))],
        "center_colors": [(240, 235, 215), (232, 226, 205)],
        "patterns": ["cluster"],
        "petal_counts": [4, 5],
        "preferred_biodomes": ["redwood"],
    },

    # tropical
    "glory_lily": {
        "rarity_pool": ["rare", "epic", "legendary"],
        "color_pool": [((240, 40, 35), (255, 215, 30)), ((220, 20, 15), (248, 198, 15))],
        "center_colors": [(255, 245, 100), (248, 235, 85)],
        "patterns": ["daisy", "simple"],
        "petal_counts": [6],
        "preferred_biodomes": ["tropical"],
    },
    "monstera_bloom": {
        "rarity_pool": ["rare", "epic"],
        "color_pool": [((252, 248, 230), (255, 255, 245)), ((240, 235, 215), (250, 248, 232))],
        "center_colors": [(195, 215, 165), (182, 202, 152)],
        "patterns": ["trumpet"],
        "petal_counts": [1, 2],
        "preferred_biodomes": ["tropical"],
    },

    # savanna
    "flame_lily": {
        "rarity_pool": ["uncommon", "rare", "epic"],
        "color_pool": [((240, 50, 25), (255, 195, 35)), ((225, 30, 10), (248, 178, 20))],
        "center_colors": [(255, 235, 75), (248, 225, 60)],
        "patterns": ["daisy", "simple"],
        "petal_counts": [6],
        "preferred_biodomes": ["savanna"],
    },
    "blue_sage": {
        "rarity_pool": ["common", "common", "uncommon"],
        "color_pool": [((95, 130, 225), (155, 190, 255)), ((80, 112, 210), (138, 172, 245))],
        "center_colors": [(205, 218, 255), (195, 208, 248)],
        "patterns": ["cluster", "simple"],
        "petal_counts": [4, 5],
        "preferred_biodomes": ["savanna"],
    },
    "carpet_daisy": {
        "rarity_pool": ["common", "common", "common", "uncommon"],
        "color_pool": [((255, 220, 55), (255, 245, 130)), ((245, 205, 38), (255, 235, 112))],
        "center_colors": [(185, 140, 10), (198, 152, 18)],
        "patterns": ["daisy"],
        "petal_counts": [10, 12],
        "preferred_biodomes": ["savanna"],
    },

    # wasteland
    "brittlebush_bloom": {
        "rarity_pool": ["uncommon", "rare"],
        "color_pool": [((255, 200, 25), (255, 238, 100)), ((240, 182, 10), (248, 224, 82))],
        "center_colors": [(200, 148, 5), (212, 160, 12)],
        "patterns": ["daisy", "simple"],
        "petal_counts": [8, 10],
        "preferred_biodomes": ["wasteland"],
    },
    "sagebrush_flower": {
        "rarity_pool": ["common", "common", "uncommon"],
        "color_pool": [((155, 162, 185), (195, 202, 225)), ((138, 145, 168), (178, 185, 210))],
        "center_colors": [(215, 220, 235), (205, 210, 228)],
        "patterns": ["cluster"],
        "petal_counts": [3, 4],
        "preferred_biodomes": ["wasteland"],
    },

    # fungal
    "phantom_bloom": {
        "rarity_pool": ["epic", "legendary"],
        "color_pool": [((215, 228, 252), (235, 245, 255)), ((200, 215, 245), (222, 235, 252))],
        "center_colors": [(255, 255, 255), (248, 250, 255)],
        "patterns": ["simple", "daisy"],
        "petal_counts": [8, 10],
        "preferred_biodomes": ["fungal"],
    },
    "void_petal": {
        "rarity_pool": ["rare", "epic"],
        "color_pool": [((25, 10, 55), (105, 55, 175)), ((15, 5, 45), (88, 42, 158))],
        "center_colors": [(185, 100, 255), (172, 88, 245)],
        "patterns": ["daisy", "simple"],
        "petal_counts": [6, 8],
        "preferred_biodomes": ["fungal"],
    },
    "crystal_bloom": {
        "rarity_pool": ["rare", "epic", "legendary"],
        "color_pool": [((210, 240, 255), (240, 252, 255)), ((195, 228, 250), (228, 245, 252))],
        "center_colors": [(255, 255, 255), (245, 250, 255)],
        "patterns": ["simple", "daisy", "trumpet"],
        "petal_counts": [6, 8, 12],
        "preferred_biodomes": ["fungal"],
    },

    # ---- 25 more types ----

    # temperate
    "meadowsweet": {
        "rarity_pool": ["common", "common", "uncommon"],
        "color_pool": [((252, 248, 230), (255, 253, 242)), ((240, 235, 215), (250, 246, 230))],
        "center_colors": [(255, 228, 80), (248, 218, 65)],
        "patterns": ["cluster", "cluster"],
        "petal_counts": [5, 6],
        "preferred_biodomes": ["temperate"],
    },
    "vetch_flower": {
        "rarity_pool": ["common", "common", "uncommon"],
        "color_pool": [((125, 80, 200), (185, 145, 245)), ((100, 55, 180), (162, 122, 228))],
        "center_colors": [(215, 195, 255), (205, 182, 248)],
        "patterns": ["cluster", "simple"],
        "petal_counts": [4, 5],
        "preferred_biodomes": ["temperate"],
    },

    # boreal
    "saxifrage": {
        "rarity_pool": ["uncommon", "rare", "epic"],
        "color_pool": [((252, 250, 248), (232, 228, 222)), ((245, 242, 238), (220, 215, 208))],
        "center_colors": [(255, 215, 90), (248, 205, 75)],
        "patterns": ["daisy", "simple"],
        "petal_counts": [5],
        "preferred_biodomes": ["boreal"],
    },
    "crowberry_flower": {
        "rarity_pool": ["rare", "epic"],
        "color_pool": [((160, 35, 70), (215, 85, 125)), ((142, 22, 55), (198, 68, 110))],
        "center_colors": [(235, 175, 200), (225, 162, 188)],
        "patterns": ["simple"],
        "petal_counts": [4, 5],
        "preferred_biodomes": ["boreal"],
    },

    # birch_forest
    "wild_strawberry_flower": {
        "rarity_pool": ["common", "common", "uncommon"],
        "color_pool": [((252, 252, 252), (235, 245, 235)), ((240, 245, 240), (220, 235, 220))],
        "center_colors": [(255, 218, 60), (248, 208, 45)],
        "patterns": ["simple"],
        "petal_counts": [5],
        "preferred_biodomes": ["birch_forest"],
    },
    "wood_cranesbill": {
        "rarity_pool": ["common", "uncommon", "rare"],
        "color_pool": [((145, 105, 210), (200, 165, 250)), ((120, 80, 192), (178, 142, 238))],
        "center_colors": [(255, 240, 200), (248, 230, 185)],
        "patterns": ["simple", "daisy"],
        "petal_counts": [5],
        "preferred_biodomes": ["birch_forest"],
    },
    "ramsons": {
        "rarity_pool": ["common", "common", "uncommon"],
        "color_pool": [((248, 252, 248), (225, 240, 225)), ((238, 245, 238), (212, 230, 212))],
        "center_colors": [(220, 240, 220), (208, 230, 208)],
        "patterns": ["cluster"],
        "petal_counts": [6],
        "preferred_biodomes": ["birch_forest"],
    },

    # jungle
    "vanilla_orchid": {
        "rarity_pool": ["rare", "epic", "legendary"],
        "color_pool": [((215, 228, 195), (245, 252, 230)), ((198, 215, 178), (232, 245, 215))],
        "center_colors": [(255, 245, 195), (248, 235, 178)],
        "patterns": ["trumpet", "simple"],
        "petal_counts": [5, 6],
        "preferred_biodomes": ["jungle"],
    },
    "flame_of_forest": {
        "rarity_pool": ["rare", "epic", "legendary"],
        "color_pool": [((255, 65, 15), (255, 175, 35)), ((240, 45, 5), (248, 158, 20))],
        "center_colors": [(255, 240, 80), (248, 228, 65)],
        "patterns": ["trumpet", "cluster"],
        "petal_counts": [5, 6],
        "preferred_biodomes": ["jungle"],
    },

    # wetland
    "water_crowfoot": {
        "rarity_pool": ["common", "common", "uncommon"],
        "color_pool": [((252, 252, 252), (228, 238, 252)), ((240, 242, 252), (215, 228, 248))],
        "center_colors": [(255, 222, 65), (248, 212, 50)],
        "patterns": ["simple", "daisy"],
        "petal_counts": [5],
        "preferred_biodomes": ["wetland"],
    },
    "yellow_flag": {
        "rarity_pool": ["uncommon", "rare", "epic"],
        "color_pool": [((255, 215, 30), (255, 248, 120)), ((242, 198, 15), (248, 235, 102))],
        "center_colors": [(195, 158, 5), (208, 170, 12)],
        "patterns": ["trumpet", "simple"],
        "petal_counts": [6],
        "preferred_biodomes": ["wetland"],
    },
    "marsh_cinquefoil": {
        "rarity_pool": ["uncommon", "rare"],
        "color_pool": [((145, 40, 95), (205, 100, 158)), ((128, 25, 78), (188, 82, 142))],
        "center_colors": [(225, 165, 200), (215, 152, 188)],
        "patterns": ["simple"],
        "petal_counts": [5],
        "preferred_biodomes": ["wetland"],
    },

    # redwood
    "inside_out_flower": {
        "rarity_pool": ["uncommon", "rare", "epic"],
        "color_pool": [((252, 248, 252), (230, 222, 248)), ((242, 238, 248), (218, 210, 240))],
        "center_colors": [(255, 235, 175), (248, 225, 160)],
        "patterns": ["daisy", "simple"],
        "petal_counts": [6, 8],
        "preferred_biodomes": ["redwood"],
    },
    "toadshade": {
        "rarity_pool": ["rare", "epic", "legendary"],
        "color_pool": [((105, 30, 35), (185, 75, 85)), ((88, 18, 22), (168, 58, 68))],
        "center_colors": [(255, 195, 185), (248, 182, 172)],
        "patterns": ["simple"],
        "petal_counts": [3],
        "preferred_biodomes": ["redwood"],
    },

    # tropical
    "sea_hibiscus": {
        "rarity_pool": ["uncommon", "rare", "epic"],
        "color_pool": [((255, 220, 55), (255, 145, 35)), ((248, 205, 35), (240, 125, 18))],
        "center_colors": [(185, 55, 15), (198, 68, 22)],
        "patterns": ["trumpet", "simple"],
        "petal_counts": [5],
        "preferred_biodomes": ["tropical"],
    },
    "jungle_crown": {
        "rarity_pool": ["rare", "epic", "legendary"],
        "color_pool": [((195, 65, 210), (255, 155, 255)), ((175, 45, 190), (245, 135, 245))],
        "center_colors": [(255, 255, 200), (248, 248, 185)],
        "patterns": ["daisy", "cluster"],
        "petal_counts": [8, 10],
        "preferred_biodomes": ["tropical"],
    },
    "tropical_snowball": {
        "rarity_pool": ["rare", "epic"],
        "color_pool": [((252, 252, 252), (235, 242, 255)), ((240, 245, 255), (220, 232, 252))],
        "center_colors": [(215, 228, 255), (205, 218, 248)],
        "patterns": ["cluster"],
        "petal_counts": [6, 8],
        "preferred_biodomes": ["tropical"],
    },

    # savanna
    "fire_wheel": {
        "rarity_pool": ["uncommon", "rare", "epic"],
        "color_pool": [((220, 30, 20), (255, 205, 30)), ((205, 15, 10), (248, 188, 15))],
        "center_colors": [(105, 15, 10), (118, 22, 15)],
        "patterns": ["daisy"],
        "petal_counts": [14, 18],
        "preferred_biodomes": ["savanna"],
    },
    "buffalo_thorn_flower": {
        "rarity_pool": ["common", "uncommon"],
        "color_pool": [((252, 245, 215), (255, 252, 235)), ((238, 230, 195), (250, 245, 220))],
        "center_colors": [(210, 188, 95), (222, 200, 108)],
        "patterns": ["cluster", "simple"],
        "petal_counts": [4, 5],
        "preferred_biodomes": ["savanna"],
    },
    "protea_pink": {
        "rarity_pool": ["rare", "epic", "legendary"],
        "color_pool": [((240, 155, 175), (255, 210, 225)), ((222, 132, 155), (248, 195, 212))],
        "center_colors": [(255, 245, 235), (248, 238, 228)],
        "patterns": ["daisy"],
        "petal_counts": [18, 22, 28],
        "preferred_biodomes": ["savanna"],
    },

    # wasteland
    "night_blooming_cereus": {
        "rarity_pool": ["epic", "legendary"],
        "color_pool": [((252, 252, 248), (230, 240, 255)), ((240, 242, 248), (215, 228, 252))],
        "center_colors": [(255, 248, 215), (248, 240, 200)],
        "patterns": ["daisy", "simple"],
        "petal_counts": [12, 16, 20],
        "preferred_biodomes": ["wasteland"],
    },
    "sand_verbena": {
        "rarity_pool": ["uncommon", "rare"],
        "color_pool": [((225, 90, 170), (255, 165, 220)), ((208, 68, 152), (245, 145, 205))],
        "center_colors": [(255, 225, 240), (248, 215, 232)],
        "patterns": ["cluster"],
        "petal_counts": [5, 6],
        "preferred_biodomes": ["wasteland"],
    },
    "sacred_datura": {
        "rarity_pool": ["rare", "epic", "legendary"],
        "color_pool": [((252, 250, 248), (225, 218, 255)), ((240, 238, 248), (210, 205, 248))],
        "center_colors": [(245, 240, 255), (235, 230, 250)],
        "patterns": ["trumpet"],
        "petal_counts": [5],
        "preferred_biodomes": ["wasteland"],
    },

    # fungal
    "echo_blossom": {
        "rarity_pool": ["epic", "legendary"],
        "color_pool": [((195, 175, 245), (230, 215, 255)), ((178, 158, 232), (215, 198, 248))],
        "center_colors": [(255, 252, 255), (248, 245, 252)],
        "patterns": ["simple", "daisy"],
        "petal_counts": [8, 10, 12],
        "preferred_biodomes": ["fungal"],
    },
    "deep_lung_bloom": {
        "rarity_pool": ["rare", "epic"],
        "color_pool": [((200, 55, 55), (255, 135, 105)), ((178, 35, 35), (240, 115, 88))],
        "center_colors": [(255, 215, 195), (248, 202, 182)],
        "patterns": ["cluster", "trumpet"],
        "petal_counts": [4, 5],
        "preferred_biodomes": ["fungal"],
    },

    # ---- 25 more types ----

    # temperate
    "red_clover": {
        "rarity_pool": ["common", "common", "common", "uncommon"],
        "color_pool": [((210, 75, 130), (255, 150, 185)), ((192, 55, 112), (242, 130, 168))],
        "center_colors": [(175, 40, 95), (188, 52, 108)],
        "patterns": ["cluster"],
        "petal_counts": [4, 5],
        "preferred_biodomes": ["temperate"],
    },
    "yarrow": {
        "rarity_pool": ["common", "common", "uncommon"],
        "color_pool": [((252, 250, 240), (255, 252, 248)), ((238, 235, 220), (250, 248, 235))],
        "center_colors": [(248, 238, 195), (240, 228, 182)],
        "patterns": ["cluster"],
        "petal_counts": [5, 6],
        "preferred_biodomes": ["temperate"],
    },
    "selfheal": {
        "rarity_pool": ["common", "uncommon"],
        "color_pool": [((105, 80, 195), (165, 140, 240)), ((85, 60, 178), (148, 122, 228))],
        "center_colors": [(195, 175, 248), (182, 162, 238)],
        "patterns": ["cluster", "simple"],
        "petal_counts": [4, 5],
        "preferred_biodomes": ["temperate"],
    },

    # boreal
    "purple_saxifrage": {
        "rarity_pool": ["uncommon", "rare", "epic"],
        "color_pool": [((165, 60, 195), (218, 128, 245)), ((145, 42, 175), (200, 108, 230))],
        "center_colors": [(255, 228, 180), (248, 218, 165)],
        "patterns": ["simple"],
        "petal_counts": [5],
        "preferred_biodomes": ["boreal"],
    },
    "glacier_pink": {
        "rarity_pool": ["rare", "epic"],
        "color_pool": [((245, 185, 210), (255, 225, 240)), ((230, 165, 195), (248, 210, 228))],
        "center_colors": [(255, 240, 248), (248, 232, 240)],
        "patterns": ["simple", "daisy"],
        "petal_counts": [5, 6],
        "preferred_biodomes": ["boreal"],
    },

    # birch_forest
    "moschatel": {
        "rarity_pool": ["uncommon", "rare"],
        "color_pool": [((165, 195, 125), (210, 230, 175)), ((148, 178, 108), (195, 215, 158))],
        "center_colors": [(225, 238, 185), (215, 228, 172)],
        "patterns": ["cluster"],
        "petal_counts": [5],
        "preferred_biodomes": ["birch_forest"],
    },
    "early_purple_orchid": {
        "rarity_pool": ["rare", "epic", "legendary"],
        "color_pool": [((148, 42, 185), (215, 115, 248)), ((128, 25, 165), (198, 95, 232))],
        "center_colors": [(255, 225, 215), (248, 215, 202)],
        "patterns": ["trumpet", "simple"],
        "petal_counts": [5, 6],
        "preferred_biodomes": ["birch_forest"],
    },

    # jungle
    "moon_flower": {
        "rarity_pool": ["rare", "epic", "legendary"],
        "color_pool": [((252, 252, 252), (225, 235, 255)), ((240, 242, 255), (210, 225, 252))],
        "center_colors": [(255, 250, 215), (248, 242, 200)],
        "patterns": ["trumpet"],
        "petal_counts": [5],
        "preferred_biodomes": ["jungle"],
    },
    "amazon_lily": {
        "rarity_pool": ["rare", "epic", "legendary"],
        "color_pool": [((252, 252, 252), (215, 205, 255)), ((240, 235, 255), (198, 188, 248))],
        "center_colors": [(185, 160, 255), (172, 148, 245)],
        "patterns": ["simple", "daisy"],
        "petal_counts": [6],
        "preferred_biodomes": ["jungle"],
    },
    "jungle_magnolia": {
        "rarity_pool": ["epic", "legendary"],
        "color_pool": [((255, 248, 235), (255, 252, 248)), ((242, 232, 215), (250, 245, 235))],
        "center_colors": [(195, 165, 95), (208, 178, 108)],
        "patterns": ["simple", "trumpet"],
        "petal_counts": [6, 9, 12],
        "preferred_biodomes": ["jungle"],
    },

    # wetland
    "flowering_rush": {
        "rarity_pool": ["uncommon", "rare", "epic"],
        "color_pool": [((230, 130, 165), (255, 190, 215)), ((215, 110, 148), (245, 172, 200))],
        "center_colors": [(255, 215, 230), (248, 205, 220)],
        "patterns": ["cluster", "simple"],
        "petal_counts": [3],
        "preferred_biodomes": ["wetland"],
    },
    "purple_loosestrife": {
        "rarity_pool": ["common", "uncommon", "rare"],
        "color_pool": [((175, 55, 185), (228, 125, 238)), ((158, 38, 168), (212, 105, 222))],
        "center_colors": [(245, 205, 255), (235, 192, 248)],
        "patterns": ["cluster"],
        "petal_counts": [5, 6],
        "preferred_biodomes": ["wetland"],
    },

    # redwood
    "leopard_lily": {
        "rarity_pool": ["uncommon", "rare", "epic"],
        "color_pool": [((245, 130, 35), (255, 200, 90)), ((228, 112, 18), (248, 182, 72))],
        "center_colors": [(95, 35, 10), (108, 45, 15)],
        "patterns": ["trumpet", "simple"],
        "petal_counts": [6],
        "preferred_biodomes": ["redwood"],
    },
    "fringe_cups": {
        "rarity_pool": ["uncommon", "rare"],
        "color_pool": [((248, 215, 225), (255, 240, 248)), ((235, 195, 210), (250, 228, 240))],
        "center_colors": [(255, 228, 235), (248, 218, 225)],
        "patterns": ["cluster", "trumpet"],
        "petal_counts": [5],
        "preferred_biodomes": ["redwood"],
    },
    "goats_beard": {
        "rarity_pool": ["common", "uncommon"],
        "color_pool": [((252, 252, 252), (235, 240, 235)), ((240, 245, 240), (220, 228, 220))],
        "center_colors": [(225, 232, 220), (215, 222, 210)],
        "patterns": ["daisy"],
        "petal_counts": [20, 28, 36],
        "preferred_biodomes": ["redwood"],
    },

    # tropical
    "wax_plant": {
        "rarity_pool": ["uncommon", "rare"],
        "color_pool": [((255, 205, 215), (255, 235, 245)), ((242, 185, 198), (250, 222, 235))],
        "center_colors": [(255, 215, 228), (248, 205, 218)],
        "patterns": ["cluster"],
        "petal_counts": [5],
        "preferred_biodomes": ["tropical"],
    },
    "pentas": {
        "rarity_pool": ["uncommon", "rare"],
        "color_pool": [((225, 45, 75), (255, 135, 155)), ((195, 180, 235), (235, 220, 255))],
        "center_colors": [(255, 245, 245), (248, 235, 235)],
        "patterns": ["cluster"],
        "petal_counts": [5],
        "preferred_biodomes": ["tropical"],
    },

    # savanna
    "cape_daisy": {
        "rarity_pool": ["common", "common", "uncommon"],
        "color_pool": [((252, 248, 252), (235, 225, 255)), ((240, 230, 248), (222, 210, 245))],
        "center_colors": [(45, 28, 58), (55, 35, 68)],
        "patterns": ["daisy"],
        "petal_counts": [12, 14],
        "preferred_biodomes": ["savanna"],
    },
    "veld_lily": {
        "rarity_pool": ["uncommon", "rare", "epic"],
        "color_pool": [((252, 248, 232), (255, 252, 245)), ((238, 232, 212), (250, 245, 230))],
        "center_colors": [(195, 175, 95), (208, 188, 108)],
        "patterns": ["simple", "trumpet"],
        "petal_counts": [6],
        "preferred_biodomes": ["savanna"],
    },
    "rooi_els_flower": {
        "rarity_pool": ["uncommon", "rare"],
        "color_pool": [((215, 95, 120), (255, 165, 185)), ((198, 75, 102), (245, 148, 168))],
        "center_colors": [(255, 215, 225), (248, 205, 215)],
        "patterns": ["cluster", "simple"],
        "petal_counts": [4, 5],
        "preferred_biodomes": ["savanna"],
    },

    # wasteland
    "ocotillo_bloom": {
        "rarity_pool": ["uncommon", "rare", "epic"],
        "color_pool": [((255, 65, 25), (255, 170, 50)), ((240, 45, 10), (248, 152, 32))],
        "center_colors": [(255, 235, 80), (248, 225, 65)],
        "patterns": ["cluster", "trumpet"],
        "petal_counts": [4, 5],
        "preferred_biodomes": ["wasteland"],
    },
    "globe_mallow": {
        "rarity_pool": ["common", "common", "uncommon"],
        "color_pool": [((245, 135, 75), (255, 198, 135)), ((228, 115, 55), (248, 178, 112))],
        "center_colors": [(215, 98, 42), (228, 112, 55)],
        "patterns": ["simple", "trumpet"],
        "petal_counts": [5],
        "preferred_biodomes": ["wasteland"],
    },
    "desert_chicory": {
        "rarity_pool": ["uncommon", "rare"],
        "color_pool": [((252, 252, 252), (225, 240, 255)), ((238, 242, 252), (210, 228, 250))],
        "center_colors": [(210, 228, 255), (198, 215, 248)],
        "patterns": ["daisy"],
        "petal_counts": [14, 18],
        "preferred_biodomes": ["wasteland"],
    },

    # fungal
    "star_cap_flower": {
        "rarity_pool": ["rare", "epic"],
        "color_pool": [((55, 235, 185), (155, 255, 228)), ((38, 215, 165), (135, 245, 210))],
        "center_colors": [(255, 252, 195), (248, 245, 182)],
        "patterns": ["daisy"],
        "petal_counts": [6, 8],
        "preferred_biodomes": ["fungal"],
    },
    "biolume_bell": {
        "rarity_pool": ["epic", "legendary"],
        "color_pool": [((45, 215, 228), (135, 252, 255)), ((28, 195, 210), (115, 240, 248))],
        "center_colors": [(215, 252, 255), (200, 242, 248)],
        "patterns": ["trumpet"],
        "petal_counts": [4, 5],
        "preferred_biodomes": ["fungal"],
    },

    # ---- New biome flowers (desert, tundra, swamp, beach, canyon + all new biomes) ----

    # swamp
    "swamp_rose_mallow": {
        "rarity_pool": ["common", "uncommon", "uncommon"],
        "color_pool": [((255, 185, 210), (255, 230, 245)), ((240, 155, 190), (250, 215, 238))],
        "center_colors": [(215, 80, 120), (225, 95, 135)],
        "patterns": ["trumpet", "simple"],
        "petal_counts": [5],
        "preferred_biodomes": ["swamp"],
    },
    "blue_flag_iris": {
        "rarity_pool": ["common", "uncommon", "rare"],
        "color_pool": [((75, 80, 210), (135, 140, 255)), ((55, 65, 195), (110, 120, 245))],
        "center_colors": [(240, 235, 200), (230, 225, 185)],
        "patterns": ["trumpet", "simple"],
        "petal_counts": [6],
        "preferred_biodomes": ["swamp", "wetland"],
    },
    "swamp_candles": {
        "rarity_pool": ["uncommon", "uncommon", "rare"],
        "color_pool": [((255, 215, 30), (255, 250, 120)), ((242, 200, 15), (250, 238, 100))],
        "center_colors": [(195, 155, 10), (208, 168, 20)],
        "patterns": ["cluster"],
        "petal_counts": [5, 6],
        "preferred_biodomes": ["swamp"],
    },
    "cardinal_flower": {
        "rarity_pool": ["rare", "rare", "epic", "legendary"],
        "color_pool": [((215, 25, 25), (255, 95, 75)), ((200, 15, 15), (245, 78, 58))],
        "center_colors": [(255, 230, 100), (248, 220, 85)],
        "patterns": ["cluster", "trumpet"],
        "petal_counts": [5],
        "preferred_biodomes": ["swamp"],
    },
    "great_blue_lobelia": {
        "rarity_pool": ["uncommon", "rare", "epic"],
        "color_pool": [((60, 90, 215), (110, 145, 255)), ((45, 72, 198), (90, 125, 242))],
        "center_colors": [(220, 238, 255), (208, 228, 250)],
        "patterns": ["cluster", "simple"],
        "petal_counts": [5],
        "preferred_biodomes": ["swamp", "wetland"],
    },

    # tundra
    "mountain_dryas": {
        "rarity_pool": ["uncommon", "uncommon", "rare"],
        "color_pool": [((252, 250, 240), (235, 232, 220)), ((245, 242, 228), (225, 222, 208))],
        "center_colors": [(255, 220, 55), (248, 210, 42)],
        "patterns": ["daisy"],
        "petal_counts": [8],
        "preferred_biodomes": ["tundra", "boreal"],
    },
    "tundra_cotton": {
        "rarity_pool": ["common", "common", "uncommon"],
        "color_pool": [((252, 252, 252), (232, 238, 248)), ((242, 245, 252), (218, 228, 248))],
        "center_colors": [(245, 248, 255), (235, 240, 252)],
        "patterns": ["cluster"],
        "petal_counts": [6, 8],
        "preferred_biodomes": ["tundra"],
    },
    "arctic_bell": {
        "rarity_pool": ["rare", "epic", "legendary"],
        "color_pool": [((165, 195, 235), (210, 230, 255)), ((145, 178, 220), (195, 218, 252))],
        "center_colors": [(225, 240, 255), (215, 232, 252)],
        "patterns": ["trumpet"],
        "petal_counts": [5],
        "preferred_biodomes": ["tundra"],
    },

    # desert
    "saguaro_bloom": {
        "rarity_pool": ["uncommon", "rare", "epic"],
        "color_pool": [((252, 252, 248), (232, 240, 220)), ((240, 245, 230), (215, 228, 205))],
        "center_colors": [(255, 235, 90), (248, 225, 75)],
        "patterns": ["simple", "daisy"],
        "petal_counts": [8, 10],
        "preferred_biodomes": ["desert"],
    },
    "desert_marigold_bloom": {
        "rarity_pool": ["common", "common", "uncommon"],
        "color_pool": [((255, 205, 30), (255, 242, 110)), ((242, 188, 15), (248, 230, 92))],
        "center_colors": [(185, 148, 10), (198, 162, 18)],
        "patterns": ["daisy"],
        "petal_counts": [12, 14],
        "preferred_biodomes": ["desert"],
    },
    "desert_primrose": {
        "rarity_pool": ["uncommon", "rare", "epic", "legendary"],
        "color_pool": [((252, 250, 235), (255, 255, 248)), ((238, 235, 215), (252, 250, 235))],
        "center_colors": [(255, 232, 80), (248, 222, 65)],
        "patterns": ["simple", "trumpet"],
        "petal_counts": [4, 5],
        "preferred_biodomes": ["desert"],
    },

    # beach
    "sea_rocket": {
        "rarity_pool": ["common", "common", "uncommon"],
        "color_pool": [((185, 155, 215), (225, 200, 245)), ((165, 135, 198), (208, 182, 232))],
        "center_colors": [(235, 225, 248), (225, 215, 240)],
        "patterns": ["simple", "cluster"],
        "petal_counts": [4],
        "preferred_biodomes": ["beach"],
    },
    "beach_morning_glory": {
        "rarity_pool": ["common", "uncommon", "rare"],
        "color_pool": [((210, 100, 175), (255, 175, 230)), ((185, 75, 150), (245, 148, 210))],
        "center_colors": [(255, 245, 225), (248, 235, 210)],
        "patterns": ["trumpet"],
        "petal_counts": [5],
        "preferred_biodomes": ["beach"],
    },
    "sea_campion": {
        "rarity_pool": ["common", "common", "uncommon"],
        "color_pool": [((252, 252, 252), (225, 238, 248)), ((240, 244, 252), (210, 226, 244))],
        "center_colors": [(255, 248, 240), (248, 240, 232)],
        "patterns": ["simple"],
        "petal_counts": [5],
        "preferred_biodomes": ["beach"],
    },

    # canyon
    "canyon_columbine": {
        "rarity_pool": ["uncommon", "rare", "epic"],
        "color_pool": [((215, 40, 40), (255, 205, 60)), ((195, 25, 25), (248, 188, 42))],
        "center_colors": [(255, 242, 100), (248, 232, 85)],
        "patterns": ["trumpet"],
        "petal_counts": [5],
        "preferred_biodomes": ["canyon"],
    },
    "cliff_penstemon": {
        "rarity_pool": ["uncommon", "uncommon", "rare"],
        "color_pool": [((195, 55, 140), (248, 135, 205)), ((175, 38, 120), (235, 112, 188))],
        "center_colors": [(255, 225, 245), (248, 215, 235)],
        "patterns": ["trumpet", "cluster"],
        "petal_counts": [5],
        "preferred_biodomes": ["canyon"],
    },
    "rock_cress": {
        "rarity_pool": ["common", "common", "uncommon"],
        "color_pool": [((215, 185, 235), (245, 225, 255)), ((195, 162, 218), (230, 205, 248))],
        "center_colors": [(255, 248, 255), (248, 240, 252)],
        "patterns": ["cluster", "simple"],
        "petal_counts": [4],
        "preferred_biodomes": ["canyon"],
    },
}

WILDFLOWER_TYPE_ORDER = sorted(WILDFLOWER_TYPES.keys())

WILDFLOWER_BIODOME_AFFINITY = {
    "temperate":    {"daisy", "buttercup", "clover", "cornflower", "marigold",
                     "foxglove", "lavender", "poppy", "cowslip", "wild_rose",
                     "forget_me_not", "sweet_pea", "snapdragon",
                     "chamomile", "ox_eye_daisy",
                     "meadowsweet", "vetch_flower",
                     "red_clover", "yarrow", "selfheal"},
    "boreal":       {"fireweed", "lupine", "arctic_poppy", "clover",
                     "edelweiss", "cloudberry_flower", "willow_herb", "poppy",
                     "mountain_avens", "larch_bloom", "bunchberry",
                     "alpine_aster", "moss_campion", "dwarf_fireweed",
                     "saxifrage", "crowberry_flower",
                     "purple_saxifrage", "glacier_pink", "mountain_dryas"},
    "birch_forest": {"bluebell", "wood_anemone", "trillium",
                     "foxglove", "lily_of_valley", "spring_beauty", "wild_rose",
                     "hepatica", "wood_violet",
                     "wood_sorrel", "jack_in_pulpit",
                     "wild_strawberry_flower", "wood_cranesbill", "ramsons",
                     "moschatel", "early_purple_orchid"},
    "jungle":       {"orchid", "heliconia", "passion_flower",
                     "bromeliad", "anthurium", "giant_lotus", "bird_of_paradise",
                     "jungle_jasmine", "pitcher_plant_flower", "rafflesia",
                     "jungle_lily", "cannonball_flower", "torch_lily",
                     "vanilla_orchid", "flame_of_forest",
                     "moon_flower", "amazon_lily", "jungle_magnolia"},
    "wetland":      {"iris", "marsh_marigold", "water_lily",
                     "cattail_bloom", "pickerel_weed", "lotus", "giant_lotus",
                     "bogbean", "swamp_rose",
                     "arrowhead_bloom", "frog_bit",
                     "water_crowfoot", "yellow_flag", "marsh_cinquefoil",
                     "flowering_rush", "purple_loosestrife",
                     "blue_flag_iris", "great_blue_lobelia"},
    "redwood":      {"redwood_violet", "bleeding_heart",
                     "redwood_sorrel", "fairy_slipper", "lily_of_valley",
                     "calypso_orchid", "ghost_orchid",
                     "redwood_lily", "twinflower", "vanilla_leaf_bloom",
                     "inside_out_flower", "toadshade",
                     "leopard_lily", "fringe_cups", "goats_beard"},
    "tropical":     {"hibiscus", "plumeria", "heliconia",
                     "bird_of_paradise", "torch_ginger", "frangipani", "anthurium",
                     "ylang_ylang", "bougainvillea", "rafflesia",
                     "glory_lily", "monstera_bloom",
                     "sea_hibiscus", "jungle_crown", "tropical_snowball",
                     "wax_plant", "pentas"},
    "savanna":      {"sunflower", "marigold", "cornflower", "daisy",
                     "lavender", "acacia_blossom", "king_protea",
                     "lion_tooth", "red_hot_poker",
                     "flame_lily", "blue_sage", "carpet_daisy",
                     "fire_wheel", "buffalo_thorn_flower", "protea_pink",
                     "cape_daisy", "veld_lily", "rooi_els_flower"},
    "wasteland":    {"desert_rose", "sand_lily",
                     "prickly_pear_bloom", "dune_poppy", "ghost_plant_bloom",
                     "barrel_cactus_bloom", "straw_flower", "tumblegrass_flower",
                     "brittlebush_bloom", "sagebrush_flower",
                     "night_blooming_cereus", "sand_verbena", "sacred_datura",
                     "ocotillo_bloom", "globe_mallow", "desert_chicory"},
    "fungal":       {"glowcap_bloom", "mycelium_lily",
                     "inkwell_cap", "twilight_bell",
                     "spore_lily", "nether_belle", "cave_daisy",
                     "phantom_bloom", "void_petal", "crystal_bloom",
                     "echo_blossom", "deep_lung_bloom",
                     "star_cap_flower", "biolume_bell"},
    "alpine_mountain": {"edelweiss", "mountain_avens", "arctic_poppy", "lupine",
                        "moss_campion", "alpine_aster", "purple_saxifrage", "glacier_pink",
                        "saxifrage", "dwarf_fireweed", "mountain_dryas", "arctic_bell"},
    "rocky_mountain":  {"edelweiss", "mountain_avens", "arctic_poppy", "bluebell",
                        "poppy", "fireweed", "lupine", "wild_rose", "redwood_violet",
                        "canyon_columbine", "cliff_penstemon", "rock_cress"},
    "rolling_hills":   {"daisy", "buttercup", "clover", "cornflower", "marigold",
                        "lavender", "poppy", "cowslip", "wild_rose", "foxglove",
                        "lion_tooth", "chamomile", "ox_eye_daisy", "meadowsweet"},
    "steep_hills":     {"daisy", "bluebell", "fireweed", "foxglove", "poppy",
                        "wild_rose", "cornflower", "wood_anemone", "lavender",
                        "chamomile", "forget_me_not", "sweet_pea"},
    "steppe":          {"sunflower", "marigold", "cornflower", "lavender",
                        "lion_tooth", "blue_sage", "carpet_daisy", "acacia_blossom",
                        "red_clover", "yarrow", "sagebrush_flower"},
    "arid_steppe":     {"desert_rose", "sand_lily", "prickly_pear_bloom",
                        "tumblegrass_flower", "sagebrush_flower", "brittlebush_bloom",
                        "sunflower", "marigold", "globe_mallow"},
    "desert":          {"saguaro_bloom", "desert_marigold_bloom", "desert_primrose",
                        "desert_rose", "dune_poppy", "ghost_plant_bloom",
                        "prickly_pear_bloom", "ocotillo_bloom", "sacred_datura",
                        "sand_verbena", "barrel_cactus_bloom"},
    "tundra":          {"mountain_dryas", "tundra_cotton", "arctic_bell",
                        "arctic_poppy", "edelweiss", "mountain_avens",
                        "moss_campion", "purple_saxifrage", "glacier_pink"},
    "swamp":           {"swamp_rose_mallow", "blue_flag_iris", "swamp_candles",
                        "cardinal_flower", "great_blue_lobelia",
                        "iris", "marsh_marigold", "cattail_bloom", "swamp_rose",
                        "bogbean", "purple_loosestrife", "lotus"},
    "beach":           {"sea_rocket", "beach_morning_glory", "sea_campion",
                        "daisy", "clover", "poppy", "cornflower"},
    "canyon":          {"canyon_columbine", "cliff_penstemon", "rock_cress",
                        "poppy", "desert_rose", "marigold", "cornflower", "foxglove"},
}

BIODOME_RARITY_WEIGHTS = {
    "temperate":    {"common": 70, "uncommon": 25, "rare": 5,  "epic": 0,  "legendary": 0},
    "savanna":      {"common": 70, "uncommon": 25, "rare": 5,  "epic": 0,  "legendary": 0},
    "boreal":       {"common": 60, "uncommon": 30, "rare": 8,  "epic": 2,  "legendary": 0},
    "birch_forest": {"common": 60, "uncommon": 30, "rare": 8,  "epic": 2,  "legendary": 0},
    "wetland":      {"common": 55, "uncommon": 30, "rare": 12, "epic": 3,  "legendary": 0},
    "redwood":      {"common": 50, "uncommon": 30, "rare": 15, "epic": 4,  "legendary": 1},
    "jungle":       {"common": 40, "uncommon": 35, "rare": 18, "epic": 6,  "legendary": 1},
    "tropical":     {"common": 35, "uncommon": 35, "rare": 20, "epic": 8,  "legendary": 2},
    "wasteland":    {"common": 30, "uncommon": 25, "rare": 25, "epic": 15, "legendary": 5},
    "fungal":       {"common": 45, "uncommon": 30, "rare": 18, "epic": 5,  "legendary": 2},
    "alpine_mountain": {"common": 20, "uncommon": 35, "rare": 30, "epic": 12, "legendary": 3},
    "rocky_mountain":  {"common": 30, "uncommon": 35, "rare": 25, "epic": 8,  "legendary": 2},
    "rolling_hills":   {"common": 65, "uncommon": 28, "rare": 7,  "epic": 0,  "legendary": 0},
    "steep_hills":     {"common": 60, "uncommon": 28, "rare": 10, "epic": 2,  "legendary": 0},
    "steppe":          {"common": 60, "uncommon": 30, "rare": 8,  "epic": 2,  "legendary": 0},
    "arid_steppe":     {"common": 40, "uncommon": 30, "rare": 20, "epic": 8,  "legendary": 2},
    "desert":          {"common": 20, "uncommon": 30, "rare": 30, "epic": 15, "legendary": 5},
    "tundra":          {"common": 45, "uncommon": 35, "rare": 15, "epic": 4,  "legendary": 1},
    "swamp":           {"common": 50, "uncommon": 30, "rare": 15, "epic": 4,  "legendary": 1},
    "beach":           {"common": 65, "uncommon": 28, "rare": 7,  "epic": 0,  "legendary": 0},
    "canyon":          {"common": 30, "uncommon": 35, "rare": 25, "epic": 8,  "legendary": 2},
}

BLOOM_STAGES = ["bud", "open", "full"]

FLOWER_RARITY_PROPS = {
    "common":    {"fragrance": (0.0, 0.4), "vibrancy": (0.1, 0.5), "specials": (0, 0)},
    "uncommon":  {"fragrance": (0.2, 0.6), "vibrancy": (0.3, 0.65), "specials": (0, 1)},
    "rare":      {"fragrance": (0.4, 0.8), "vibrancy": (0.5, 0.8), "specials": (1, 2)},
    "epic":      {"fragrance": (0.6, 0.9), "vibrancy": (0.7, 0.9), "specials": (2, 3)},
    "legendary": {"fragrance": (0.8, 1.0), "vibrancy": (0.9, 1.0), "specials": (3, 4)},
}

FLOWER_SPECIALS = [
    "luminous", "nocturnal", "aromatic", "medicinal",
    "toxic", "frost_resistant", "giant", "miniature",
]


def _weighted_choice(rng, weights: dict) -> str:
    total = sum(weights.values())
    r = rng.uniform(0, total)
    cumulative = 0
    for key, weight in weights.items():
        cumulative += weight
        if r <= cumulative:
            return key
    return list(weights.keys())[-1]


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------

class WildflowerGenerator:
    def __init__(self, world_seed: int):
        self._world_seed = world_seed

    def generate(self, bx: int, by: int, biodome: str = "temperate") -> Wildflower:
        flower_seed = hash((self._world_seed, bx, by)) & 0xFFFFFFFF
        rng = random.Random(flower_seed)

        weights = BIODOME_RARITY_WEIGHTS.get(biodome, BIODOME_RARITY_WEIGHTS["temperate"])
        rarity = _weighted_choice(rng, weights)

        affinity = WILDFLOWER_BIODOME_AFFINITY.get(biodome, set())
        type_pool = [t for t in affinity if rarity in WILDFLOWER_TYPES[t]["rarity_pool"]]
        if not type_pool:
            type_pool = list(affinity) if affinity else list(WILDFLOWER_TYPES.keys())

        flower_type = rng.choice(sorted(type_pool))
        tdef = WILDFLOWER_TYPES[flower_type]

        colors = rng.choice(tdef["color_pool"])
        center_color = rng.choice(tdef["center_colors"])
        pattern = rng.choice(tdef["patterns"])
        petal_count = rng.choice(tdef["petal_counts"])
        bloom_stage = rng.choice(BLOOM_STAGES)
        props = FLOWER_RARITY_PROPS[rarity]
        fragrance = rng.uniform(*props["fragrance"])
        vibrancy = rng.uniform(*props["vibrancy"])
        n_specials = rng.randint(*props["specials"])
        specials = rng.sample(FLOWER_SPECIALS, min(n_specials, len(FLOWER_SPECIALS)))

        uid = f"flower_{bx}_{by}_{flower_seed}"
        return Wildflower(
            uid=uid,
            flower_type=flower_type,
            rarity=rarity,
            bloom_stage=bloom_stage,
            primary_color=colors[0],
            secondary_color=colors[1],
            center_color=center_color,
            petal_pattern=pattern,
            petal_count=petal_count,
            fragrance=fragrance,
            vibrancy=vibrancy,
            specials=specials,
            biodome_found=biodome,
            seed=flower_seed,
        )


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

_flower_surf_cache: dict = {}
_flower_preview_cache: dict = {}


def render_wildflower(flower: Wildflower, cell_size: int = 48) -> pygame.Surface:
    cache_key = (flower.uid, cell_size)
    if cache_key in _flower_surf_cache:
        return _flower_surf_cache[cache_key]

    surf = _build_flower_surface(
        seed=flower.seed,
        primary_color=flower.primary_color,
        secondary_color=flower.secondary_color,
        center_color=flower.center_color,
        petal_pattern=flower.petal_pattern,
        petal_count=flower.petal_count,
        bloom_stage=flower.bloom_stage,
        cell_size=cell_size,
    )
    _flower_surf_cache[cache_key] = surf
    return surf


def get_flower_preview(type_key: str, cell_size: int = 48) -> pygame.Surface:
    cache_key = (type_key, cell_size)
    if cache_key in _flower_preview_cache:
        return _flower_preview_cache[cache_key]

    tdef = WILDFLOWER_TYPES[type_key]
    colors = tdef["color_pool"][0]
    center_color = tdef["center_colors"][0]
    pattern = tdef["patterns"][0]
    petal_count = tdef["petal_counts"][0]

    surf = _build_flower_surface(
        seed=hash(type_key) & 0xFFFFFFFF,
        primary_color=colors[0],
        secondary_color=colors[1],
        center_color=center_color,
        petal_pattern=pattern,
        petal_count=petal_count,
        bloom_stage="full",
        cell_size=cell_size,
    )
    _flower_preview_cache[cache_key] = surf
    return surf


def _build_flower_surface(
    seed, primary_color, secondary_color, center_color,
    petal_pattern, petal_count, bloom_stage, cell_size
) -> pygame.Surface:
    rng = random.Random(seed)
    surf = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
    surf.fill((0, 0, 0, 0))

    cx = cell_size // 2
    stem_top_y = int(cell_size * 0.32)
    stem_bot_y = cell_size - 2
    stem_w = max(1, cell_size // 22)

    stem_g = 130 + rng.randint(-20, 20)
    stem_color = (40 + rng.randint(-10, 10), stem_g, 35 + rng.randint(-10, 10), 210)

    # Slight stem lean
    lean = rng.randint(-2, 2)
    pygame.draw.line(surf, stem_color, (cx + lean, stem_top_y), (cx, stem_bot_y), stem_w)

    # Small leaves on stem
    leaf_y = int(stem_top_y + (stem_bot_y - stem_top_y) * 0.55)
    leaf_col = (50 + rng.randint(-10, 10), 140 + rng.randint(-20, 20), 40 + rng.randint(-10, 10), 200)
    pygame.draw.line(surf, leaf_col, (cx + lean // 2, leaf_y), (cx + lean // 2 + rng.randint(4, 7), leaf_y - rng.randint(2, 4)), 1)
    pygame.draw.line(surf, leaf_col, (cx + lean // 2, leaf_y + 3), (cx + lean // 2 - rng.randint(4, 7), leaf_y + 3 - rng.randint(2, 4)), 1)

    bloom_scale = {"bud": 0.30, "open": 0.65, "full": 1.0}[bloom_stage]
    max_r = int(cell_size * 0.30)
    petal_r = max(2, int(max_r * bloom_scale))
    petal_col = primary_color + (230,)
    sec_col = secondary_color + (180,)

    hx = cx + lean
    hy = stem_top_y

    if petal_pattern == "simple":
        _draw_simple_petals(surf, hx, hy, petal_r, petal_count, petal_col, sec_col, rng)
    elif petal_pattern == "daisy":
        _draw_daisy_petals(surf, hx, hy, petal_r, petal_count, petal_col, sec_col, rng)
    elif petal_pattern == "trumpet":
        _draw_trumpet_petals(surf, hx, hy, petal_r, petal_count, petal_col, sec_col, rng)
    elif petal_pattern == "cluster":
        _draw_cluster_petals(surf, hx, hy, petal_r, petal_count, petal_col, sec_col, rng)

    # Center
    center_r = max(2, cell_size // 11)
    pygame.draw.circle(surf, center_color + (255,), (hx, hy), center_r)
    # Center highlight
    pygame.draw.circle(surf, (255, 255, 255, 100), (hx - 1, hy - 1), max(1, center_r // 3))

    _flower_surf_cache[id(surf)] = surf  # just to avoid gc; actual caching is by caller
    return surf


def _draw_simple_petals(surf, cx, cy, r, n, col, sec_col, rng):
    offset_r = int(r * 0.65)
    petal_radius = max(2, int(r * 0.52))
    for i in range(n):
        angle = i * 2 * math.pi / n + rng.uniform(-0.08, 0.08)
        px = cx + int(offset_r * math.cos(angle))
        py = cy + int(offset_r * math.sin(angle))
        pygame.draw.circle(surf, col, (px, py), petal_radius)
        # subtle secondary colour vein
        if r > 6:
            vx = cx + int((offset_r * 0.35) * math.cos(angle))
            vy = cy + int((offset_r * 0.35) * math.sin(angle))
            pygame.draw.line(surf, sec_col, (cx, cy), (vx, vy), 1)


def _draw_daisy_petals(surf, cx, cy, r, n, col, sec_col, rng):
    petal_w = max(2, int(r * 0.28))
    for i in range(n):
        angle = i * 2 * math.pi / n
        ex = cx + int(r * math.cos(angle))
        ey = cy + int(r * math.sin(angle))
        pygame.draw.line(surf, col, (cx, cy), (ex, ey), petal_w)
        # tip circle
        pygame.draw.circle(surf, sec_col, (ex, ey), max(1, petal_w - 1))


def _draw_trumpet_petals(surf, cx, cy, r, n, col, sec_col, rng):
    mid_r = int(r * 0.5)
    tip_r = max(2, int(r * 0.38))
    inner_w = max(2, int(r * 0.22))
    for i in range(n):
        angle = i * 2 * math.pi / n + rng.uniform(-0.05, 0.05)
        mx = cx + int(mid_r * math.cos(angle))
        my = cy + int(mid_r * math.sin(angle))
        tx = cx + int(r * math.cos(angle))
        ty = cy + int(r * math.sin(angle))
        pygame.draw.line(surf, col, (cx, cy), (mx, my), inner_w)
        pygame.draw.circle(surf, col, (tx, ty), tip_r)
        pygame.draw.circle(surf, sec_col, (tx, ty), max(1, tip_r - 1))


def _draw_cluster_petals(surf, cx, cy, r, n, col, sec_col, rng):
    n_clusters = rng.randint(3, 5)
    cluster_r = max(2, int(r * 0.48))
    dist = int(r * 0.52)
    sub_petal_r = max(1, int(cluster_r * 0.42))
    sub_n = min(n, 6)
    for i in range(n_clusters):
        angle = i * 2 * math.pi / n_clusters + rng.uniform(-0.15, 0.15)
        scx = cx + int(dist * math.cos(angle))
        scy = cy + int(dist * math.sin(angle))
        for j in range(sub_n):
            sa = j * 2 * math.pi / sub_n
            spx = scx + int(cluster_r * math.cos(sa))
            spy = scy + int(cluster_r * math.sin(sa))
            pygame.draw.circle(surf, col, (spx, spy), sub_petal_r)
        pygame.draw.circle(surf, sec_col, (scx, scy), max(1, sub_petal_r))
