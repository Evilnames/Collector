import math
import random
import pygame
from dataclasses import dataclass, field


@dataclass
class Fossil:
    uid: str
    fossil_type: str
    rarity: str          # common / uncommon / rare / epic / legendary
    size: str            # fragment / small / medium / large / complete
    primary_color: tuple
    secondary_color: tuple
    pattern: str         # smooth / ridged / spiral / fractured
    pattern_density: float
    age: str             # paleozoic / mesozoic / cenozoic
    clarity: float       # 0.0 – 1.0 (how clearly preserved)
    detail: float        # 0.0 – 1.0 (preservation quality)
    specials: list
    depth_found: int
    seed: int
    upgrades: list = field(default_factory=list)
    prepared: bool = False


# ---------------------------------------------------------------------------
# Fossil type definitions
# ---------------------------------------------------------------------------

FOSSIL_TYPES = {
    # --- Paleozoic (depth 50–100) ---
    "trilobite": {
        "min_depth": 50,
        "age": "paleozoic",
        "rarity_pool": ["common", "common", "uncommon", "uncommon"],
        "color_pool": [((175, 160, 135), (120, 105, 85)), ((155, 145, 120), (95, 85, 65))],
        "patterns": ["ridged", "ridged", "smooth"],
        "specials_pool": ["complete", "mineralized", "impression"],
    },
    "brachiopod": {
        "min_depth": 55,
        "age": "paleozoic",
        "rarity_pool": ["common", "common", "common", "uncommon"],
        "color_pool": [((180, 165, 140), (140, 120, 95)), ((165, 150, 125), (110, 95, 72))],
        "patterns": ["ridged", "smooth", "smooth"],
        "specials_pool": ["impression", "complete"],
    },
    "crinoid": {
        "min_depth": 60,
        "age": "paleozoic",
        "rarity_pool": ["common", "uncommon", "uncommon", "rare"],
        "color_pool": [((160, 150, 130), (100, 90, 75)), ((190, 175, 155), (130, 115, 95))],
        "patterns": ["smooth", "fractured", "ridged"],
        "specials_pool": ["impression", "mineralized"],
    },
    "nautiloid": {
        "min_depth": 65,
        "age": "paleozoic",
        "rarity_pool": ["uncommon", "uncommon", "rare", "rare"],
        "color_pool": [((200, 185, 150), (145, 125, 90)), ((215, 195, 165), (155, 135, 100))],
        "patterns": ["spiral", "spiral", "smooth"],
        "specials_pool": ["complete", "mineralized", "opalized"],
    },
    "graptolite": {
        "min_depth": 70,
        "age": "paleozoic",
        "rarity_pool": ["uncommon", "rare", "rare", "epic"],
        "color_pool": [((90, 85, 80), (55, 50, 45)), ((105, 95, 88), (65, 58, 52))],
        "patterns": ["fractured", "smooth", "ridged"],
        "specials_pool": ["carbonized", "impression"],
    },
    "coral_colony": {
        "min_depth": 75,
        "age": "paleozoic",
        "rarity_pool": ["uncommon", "rare", "rare", "epic"],
        "color_pool": [((200, 170, 130), (150, 120, 85)), ((185, 160, 120), (135, 110, 78))],
        "patterns": ["ridged", "fractured", "smooth"],
        "specials_pool": ["mineralized", "complete"],
    },
    # --- Mesozoic (depth 100–150) ---
    "ammonite": {
        "min_depth": 100,
        "age": "mesozoic",
        "rarity_pool": ["uncommon", "rare", "rare", "epic"],
        "color_pool": [((200, 175, 110), (155, 130, 75)), ((215, 190, 130), (165, 140, 90))],
        "patterns": ["spiral", "spiral", "ridged"],
        "specials_pool": ["complete", "opalized", "mineralized"],
    },
    "belemnite": {
        "min_depth": 105,
        "age": "mesozoic",
        "rarity_pool": ["uncommon", "uncommon", "rare", "rare"],
        "color_pool": [((155, 145, 125), (105, 95, 78)), ((170, 155, 132), (115, 105, 85))],
        "patterns": ["smooth", "ridged", "smooth"],
        "specials_pool": ["mineralized", "impression"],
    },
    "ichthyosaur_tooth": {
        "min_depth": 110,
        "age": "mesozoic",
        "rarity_pool": ["rare", "rare", "epic", "legendary"],
        "color_pool": [((235, 225, 200), (170, 158, 130)), ((220, 210, 185), (160, 148, 122))],
        "patterns": ["smooth", "smooth", "fractured"],
        "specials_pool": ["complete", "mineralized", "amber_trace"],
    },
    "fern_frond": {
        "min_depth": 115,
        "age": "mesozoic",
        "rarity_pool": ["rare", "rare", "epic", "epic"],
        "color_pool": [((85, 95, 70), (50, 65, 40)), ((95, 108, 78), (58, 72, 46))],
        "patterns": ["fractured", "smooth", "ridged"],
        "specials_pool": ["carbonized", "impression", "complete"],
    },
    "pine_cone_fossil": {
        "min_depth": 120,
        "age": "mesozoic",
        "rarity_pool": ["rare", "epic", "epic", "legendary"],
        "color_pool": [((145, 110, 72), (100, 75, 48)), ((160, 125, 85), (110, 85, 56))],
        "patterns": ["ridged", "ridged", "fractured"],
        "specials_pool": ["carbonized", "complete", "mineralized"],
    },
    "sea_lily": {
        "min_depth": 125,
        "age": "mesozoic",
        "rarity_pool": ["rare", "epic", "epic", "legendary"],
        "color_pool": [((175, 155, 120), (125, 105, 78)), ((190, 170, 138), (138, 118, 88))],
        "patterns": ["spiral", "smooth", "ridged"],
        "specials_pool": ["complete", "opalized"],
    },
    # --- Cenozoic (depth 150+) ---
    "sabertooth": {
        "min_depth": 150,
        "age": "cenozoic",
        "rarity_pool": ["rare", "epic", "epic", "legendary"],
        "color_pool": [((240, 228, 200), (180, 165, 135)), ((228, 218, 192), (168, 155, 125))],
        "patterns": ["smooth", "fractured", "smooth"],
        "specials_pool": ["complete", "mineralized", "amber_trace"],
    },
    "mammoth_molar": {
        "min_depth": 155,
        "age": "cenozoic",
        "rarity_pool": ["rare", "rare", "epic", "legendary"],
        "color_pool": [((210, 195, 165), (152, 138, 110)), ((222, 208, 178), (162, 148, 118))],
        "patterns": ["ridged", "ridged", "smooth"],
        "specials_pool": ["mineralized", "complete"],
    },
    "ancient_bird": {
        "min_depth": 160,
        "age": "cenozoic",
        "rarity_pool": ["epic", "epic", "legendary", "legendary"],
        "color_pool": [((100, 90, 78), (65, 58, 48)), ((115, 105, 90), (75, 68, 56))],
        "patterns": ["fractured", "smooth", "ridged"],
        "specials_pool": ["carbonized", "complete", "impression"],
    },
    "giant_insect": {
        "min_depth": 165,
        "age": "cenozoic",
        "rarity_pool": ["epic", "epic", "legendary", "legendary"],
        "color_pool": [((195, 155, 65), (145, 112, 42)), ((210, 170, 78), (158, 125, 52))],
        "patterns": ["smooth", "ridged", "fractured"],
        "specials_pool": ["amber_trace", "complete"],
    },
    "seed_pod": {
        "min_depth": 155,
        "age": "cenozoic",
        "rarity_pool": ["rare", "rare", "epic", "epic"],
        "color_pool": [((158, 130, 92), (110, 88, 60)), ((172, 145, 105), (120, 98, 68))],
        "patterns": ["ridged", "smooth", "fractured"],
        "specials_pool": ["carbonized", "mineralized"],
    },
    "whale_bone": {
        "min_depth": 160,
        "age": "cenozoic",
        "rarity_pool": ["epic", "legendary", "legendary", "legendary"],
        "color_pool": [((232, 222, 200), (175, 162, 140)), ((242, 232, 212), (185, 172, 148))],
        "patterns": ["smooth", "fractured", "smooth"],
        "specials_pool": ["mineralized", "complete", "impression"],
    },
    # --- Additional Paleozoic ---
    "eurypterid": {
        "min_depth": 58,
        "age": "paleozoic",
        "rarity_pool": ["common", "uncommon", "uncommon", "rare"],
        "color_pool": [((155, 140, 110), (100, 88, 68)), ((170, 152, 125), (110, 97, 76))],
        "patterns": ["ridged", "smooth", "fractured"],
        "specials_pool": ["impression", "mineralized", "complete"],
    },
    "placoderm_scale": {
        "min_depth": 62,
        "age": "paleozoic",
        "rarity_pool": ["common", "uncommon", "rare", "rare"],
        "color_pool": [((120, 140, 115), (80, 95, 75)), ((135, 155, 130), (90, 108, 85))],
        "patterns": ["ridged", "ridged", "smooth"],
        "specials_pool": ["mineralized", "impression"],
    },
    "orthoceras": {
        "min_depth": 68,
        "age": "paleozoic",
        "rarity_pool": ["uncommon", "uncommon", "rare", "epic"],
        "color_pool": [((185, 170, 145), (125, 112, 88)), ((200, 185, 160), (138, 125, 98))],
        "patterns": ["ridged", "smooth", "smooth"],
        "specials_pool": ["mineralized", "complete", "opalized"],
    },
    "rugose_coral": {
        "min_depth": 72,
        "age": "paleozoic",
        "rarity_pool": ["common", "common", "uncommon", "rare"],
        "color_pool": [((190, 155, 115), (138, 108, 78)), ((178, 145, 108), (125, 98, 70))],
        "patterns": ["ridged", "fractured", "smooth"],
        "specials_pool": ["mineralized", "complete"],
    },
    "spiriferid": {
        "min_depth": 76,
        "age": "paleozoic",
        "rarity_pool": ["uncommon", "rare", "rare", "epic"],
        "color_pool": [((200, 185, 155), (148, 132, 105)), ((188, 175, 148), (138, 122, 97))],
        "patterns": ["spiral", "ridged", "smooth"],
        "specials_pool": ["complete", "impression", "mineralized"],
    },
    "bryozoan": {
        "min_depth": 80,
        "age": "paleozoic",
        "rarity_pool": ["common", "uncommon", "uncommon", "rare"],
        "color_pool": [((168, 158, 138), (112, 105, 88)), ((182, 170, 150), (125, 115, 96))],
        "patterns": ["fractured", "ridged", "smooth"],
        "specials_pool": ["impression", "mineralized"],
    },
    "blastoid": {
        "min_depth": 85,
        "age": "paleozoic",
        "rarity_pool": ["uncommon", "rare", "rare", "epic"],
        "color_pool": [((195, 175, 140), (142, 122, 92)), ((210, 190, 158), (155, 135, 105))],
        "patterns": ["ridged", "spiral", "smooth"],
        "specials_pool": ["complete", "mineralized", "opalized"],
    },
    "shark_tooth_paleozoic": {
        "min_depth": 88,
        "age": "paleozoic",
        "rarity_pool": ["uncommon", "rare", "rare", "epic"],
        "color_pool": [((225, 215, 192), (162, 152, 130)), ((238, 228, 205), (172, 162, 138))],
        "patterns": ["smooth", "smooth", "fractured"],
        "specials_pool": ["complete", "mineralized"],
    },
    "ostracod_cluster": {
        "min_depth": 90,
        "age": "paleozoic",
        "rarity_pool": ["common", "common", "uncommon", "rare"],
        "color_pool": [((148, 138, 118), (98, 90, 75)), ((162, 150, 130), (108, 100, 84))],
        "patterns": ["smooth", "fractured", "ridged"],
        "specials_pool": ["impression", "carbonized"],
    },
    # --- Additional Mesozoic ---
    "mosasaur_scale": {
        "min_depth": 108,
        "age": "mesozoic",
        "rarity_pool": ["uncommon", "rare", "rare", "epic"],
        "color_pool": [((112, 138, 118), (72, 90, 78)), ((125, 152, 132), (82, 102, 88))],
        "patterns": ["ridged", "ridged", "smooth"],
        "specials_pool": ["impression", "mineralized", "carbonized"],
    },
    "pterosaur_bone": {
        "min_depth": 112,
        "age": "mesozoic",
        "rarity_pool": ["rare", "rare", "epic", "legendary"],
        "color_pool": [((228, 218, 195), (165, 155, 132)), ((242, 232, 208), (178, 168, 145))],
        "patterns": ["smooth", "fractured", "smooth"],
        "specials_pool": ["complete", "mineralized", "impression"],
    },
    "dinosaur_egg_fragment": {
        "min_depth": 118,
        "age": "mesozoic",
        "rarity_pool": ["rare", "epic", "epic", "legendary"],
        "color_pool": [((215, 195, 155), (158, 138, 105)), ((228, 208, 168), (168, 148, 115))],
        "patterns": ["smooth", "fractured", "ridged"],
        "specials_pool": ["complete", "mineralized", "impression"],
    },
    "cycad_frond": {
        "min_depth": 122,
        "age": "mesozoic",
        "rarity_pool": ["rare", "rare", "epic", "epic"],
        "color_pool": [((92, 115, 75), (58, 75, 48)), ((105, 128, 88), (68, 88, 55))],
        "patterns": ["ridged", "fractured", "smooth"],
        "specials_pool": ["carbonized", "impression", "complete"],
    },
    "plesiosaur_vertebra": {
        "min_depth": 128,
        "age": "mesozoic",
        "rarity_pool": ["epic", "epic", "legendary", "legendary"],
        "color_pool": [((235, 222, 198), (172, 162, 138)), ((248, 235, 212), (185, 175, 150))],
        "patterns": ["smooth", "ridged", "fractured"],
        "specials_pool": ["complete", "mineralized", "impression"],
    },
    "crocodilian_tooth": {
        "min_depth": 132,
        "age": "mesozoic",
        "rarity_pool": ["rare", "rare", "epic", "legendary"],
        "color_pool": [((232, 222, 200), (168, 158, 136)), ((245, 235, 212), (180, 170, 148))],
        "patterns": ["smooth", "smooth", "fractured"],
        "specials_pool": ["complete", "mineralized"],
    },
    "shark_tooth_mesozoic": {
        "min_depth": 136,
        "age": "mesozoic",
        "rarity_pool": ["rare", "epic", "epic", "legendary"],
        "color_pool": [((52, 48, 42), (32, 28, 24)), ((65, 60, 54), (42, 38, 32))],
        "patterns": ["smooth", "fractured", "smooth"],
        "specials_pool": ["complete", "mineralized", "opalized"],
    },
    "insect_wing": {
        "min_depth": 140,
        "age": "mesozoic",
        "rarity_pool": ["rare", "epic", "epic", "legendary"],
        "color_pool": [((88, 105, 72), (55, 68, 44)), ((78, 92, 62), (48, 60, 38))],
        "patterns": ["smooth", "fractured", "ridged"],
        "specials_pool": ["carbonized", "impression", "amber_trace"],
    },
    "sauropod_scale": {
        "min_depth": 144,
        "age": "mesozoic",
        "rarity_pool": ["epic", "epic", "legendary", "legendary"],
        "color_pool": [((145, 130, 102), (100, 88, 68)), ((158, 142, 115), (112, 98, 78))],
        "patterns": ["ridged", "fractured", "smooth"],
        "specials_pool": ["impression", "mineralized", "complete"],
    },
    # --- Additional Cenozoic ---
    "cave_bear_claw": {
        "min_depth": 152,
        "age": "cenozoic",
        "rarity_pool": ["rare", "epic", "epic", "legendary"],
        "color_pool": [((235, 225, 200), (175, 165, 138)), ((248, 238, 212), (188, 178, 150))],
        "patterns": ["smooth", "fractured", "smooth"],
        "specials_pool": ["complete", "mineralized"],
    },
    "pollen_deposit": {
        "min_depth": 154,
        "age": "cenozoic",
        "rarity_pool": ["rare", "rare", "epic", "epic"],
        "color_pool": [((210, 185, 85), (155, 130, 52)), ((225, 200, 98), (168, 142, 62))],
        "patterns": ["smooth", "smooth", "fractured"],
        "specials_pool": ["amber_trace", "carbonized", "complete"],
    },
    "glyptodon_plate": {
        "min_depth": 158,
        "age": "cenozoic",
        "rarity_pool": ["rare", "rare", "epic", "legendary"],
        "color_pool": [((168, 148, 115), (115, 98, 72)), ((182, 162, 128), (128, 110, 84))],
        "patterns": ["ridged", "fractured", "ridged"],
        "specials_pool": ["complete", "mineralized", "impression"],
    },
    "terror_bird_bone": {
        "min_depth": 162,
        "age": "cenozoic",
        "rarity_pool": ["epic", "epic", "legendary", "legendary"],
        "color_pool": [((118, 108, 92), (78, 70, 58)), ((132, 122, 105), (88, 80, 67))],
        "patterns": ["smooth", "fractured", "ridged"],
        "specials_pool": ["complete", "mineralized", "impression"],
    },
    "giant_sloth_claw": {
        "min_depth": 168,
        "age": "cenozoic",
        "rarity_pool": ["epic", "legendary", "legendary", "legendary"],
        "color_pool": [((198, 178, 145), (142, 122, 94)), ((212, 192, 158), (155, 135, 108))],
        "patterns": ["smooth", "fractured", "smooth"],
        "specials_pool": ["complete", "mineralized"],
    },
    "dire_wolf_tooth": {
        "min_depth": 172,
        "age": "cenozoic",
        "rarity_pool": ["epic", "legendary", "legendary", "legendary"],
        "color_pool": [((245, 235, 215), (185, 175, 152)), ((232, 222, 202), (172, 162, 140))],
        "patterns": ["smooth", "smooth", "fractured"],
        "specials_pool": ["complete", "mineralized", "opalized"],
    },
    "elephant_ancestor_tusk": {
        "min_depth": 176,
        "age": "cenozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((245, 238, 220), (188, 180, 162)), ((255, 248, 232), (200, 192, 175))],
        "patterns": ["smooth", "ridged", "smooth"],
        "specials_pool": ["complete", "mineralized", "impression"],
    },
    # --- Deep Paleozoic / Cambrian ---
    "stromatolite": {
        "min_depth": 50,
        "age": "paleozoic",
        "rarity_pool": ["common", "common", "common", "uncommon"],
        "color_pool": [((155, 165, 170), (105, 115, 120)), ((138, 148, 155), (92, 100, 108))],
        "patterns": ["ridged", "smooth", "fractured"],
        "specials_pool": ["mineralized", "impression"],
    },
    "conodont": {
        "min_depth": 52,
        "age": "paleozoic",
        "rarity_pool": ["common", "uncommon", "rare", "rare"],
        "color_pool": [((55, 50, 45), (35, 30, 25)), ((72, 65, 58), (48, 42, 36))],
        "patterns": ["smooth", "smooth", "fractured"],
        "specials_pool": ["carbonized", "mineralized"],
    },
    "tabulate_coral": {
        "min_depth": 56,
        "age": "paleozoic",
        "rarity_pool": ["common", "common", "uncommon", "rare"],
        "color_pool": [((185, 175, 155), (130, 120, 100)), ((198, 188, 168), (142, 132, 112))],
        "patterns": ["ridged", "fractured", "smooth"],
        "specials_pool": ["mineralized", "complete"],
    },
    "lingulid": {
        "min_depth": 57,
        "age": "paleozoic",
        "rarity_pool": ["common", "uncommon", "uncommon", "rare"],
        "color_pool": [((175, 175, 140), (118, 118, 92)), ((162, 162, 128), (108, 108, 84))],
        "patterns": ["smooth", "ridged", "smooth"],
        "specials_pool": ["impression", "mineralized", "complete"],
    },
    "cephalaspis_shield": {
        "min_depth": 63,
        "age": "paleozoic",
        "rarity_pool": ["uncommon", "rare", "rare", "epic"],
        "color_pool": [((148, 138, 118), (98, 90, 75)), ((162, 152, 132), (110, 100, 85))],
        "patterns": ["smooth", "ridged", "fractured"],
        "specials_pool": ["complete", "mineralized", "impression"],
    },
    "scolecodont": {
        "min_depth": 78,
        "age": "paleozoic",
        "rarity_pool": ["uncommon", "rare", "rare", "epic"],
        "color_pool": [((48, 44, 38), (28, 25, 20)), ((62, 56, 50), (38, 34, 28))],
        "patterns": ["smooth", "fractured", "smooth"],
        "specials_pool": ["carbonized", "impression"],
    },
    "acanthodian_spine": {
        "min_depth": 82,
        "age": "paleozoic",
        "rarity_pool": ["uncommon", "rare", "rare", "epic"],
        "color_pool": [((228, 218, 198), (165, 155, 135)), ((242, 232, 212), (178, 168, 148))],
        "patterns": ["smooth", "ridged", "smooth"],
        "specials_pool": ["mineralized", "complete"],
    },
    "xiphosuran": {
        "min_depth": 86,
        "age": "paleozoic",
        "rarity_pool": ["uncommon", "uncommon", "rare", "epic"],
        "color_pool": [((108, 115, 88), (70, 76, 56)), ((122, 130, 100), (80, 88, 65))],
        "patterns": ["ridged", "smooth", "fractured"],
        "specials_pool": ["impression", "complete", "mineralized"],
    },
    "calamite_stem": {
        "min_depth": 91,
        "age": "paleozoic",
        "rarity_pool": ["uncommon", "rare", "rare", "epic"],
        "color_pool": [((140, 148, 128), (90, 98, 82)), ((155, 162, 142), (102, 110, 94))],
        "patterns": ["ridged", "ridged", "smooth"],
        "specials_pool": ["carbonized", "impression", "mineralized"],
    },
    "fusulinid": {
        "min_depth": 92,
        "age": "paleozoic",
        "rarity_pool": ["common", "uncommon", "rare", "rare"],
        "color_pool": [((215, 205, 182), (158, 148, 126)), ((228, 218, 196), (170, 160, 138))],
        "patterns": ["smooth", "ridged", "smooth"],
        "specials_pool": ["mineralized", "complete"],
    },
    "lepidodendron_bark": {
        "min_depth": 93,
        "age": "paleozoic",
        "rarity_pool": ["rare", "rare", "epic", "epic"],
        "color_pool": [((118, 128, 108), (75, 82, 68)), ((132, 142, 122), (85, 94, 78))],
        "patterns": ["ridged", "fractured", "ridged"],
        "specials_pool": ["impression", "carbonized", "complete"],
    },
    "archaeocyathid": {
        "min_depth": 95,
        "age": "paleozoic",
        "rarity_pool": ["uncommon", "rare", "epic", "epic"],
        "color_pool": [((192, 178, 152), (138, 125, 105)), ((205, 192, 165), (150, 138, 118))],
        "patterns": ["ridged", "fractured", "smooth"],
        "specials_pool": ["mineralized", "complete"],
    },
    "diplocaulus_skull": {
        "min_depth": 96,
        "age": "paleozoic",
        "rarity_pool": ["rare", "epic", "epic", "legendary"],
        "color_pool": [((128, 108, 88), (85, 70, 55)), ((142, 122, 102), (96, 82, 65))],
        "patterns": ["smooth", "fractured", "smooth"],
        "specials_pool": ["complete", "mineralized", "impression"],
    },
    "dimetrodon_spine": {
        "min_depth": 97,
        "age": "paleozoic",
        "rarity_pool": ["rare", "epic", "epic", "legendary"],
        "color_pool": [((238, 228, 205), (175, 165, 142)), ((252, 242, 218), (188, 178, 155))],
        "patterns": ["smooth", "ridged", "smooth"],
        "specials_pool": ["complete", "mineralized"],
    },
    "hallucigenia": {
        "min_depth": 98,
        "age": "paleozoic",
        "rarity_pool": ["epic", "epic", "legendary", "legendary"],
        "color_pool": [((65, 58, 50), (40, 35, 28)), ((78, 70, 62), (50, 45, 38))],
        "patterns": ["smooth", "fractured", "smooth"],
        "specials_pool": ["carbonized", "impression", "complete"],
    },
    "lystrosaurus_tooth": {
        "min_depth": 99,
        "age": "paleozoic",
        "rarity_pool": ["rare", "rare", "epic", "legendary"],
        "color_pool": [((232, 222, 200), (170, 160, 138)), ((245, 235, 212), (182, 172, 150))],
        "patterns": ["smooth", "fractured", "smooth"],
        "specials_pool": ["complete", "mineralized"],
    },
    # --- More Mesozoic ---
    "nothosaur_tooth": {
        "min_depth": 100,
        "age": "mesozoic",
        "rarity_pool": ["uncommon", "rare", "rare", "epic"],
        "color_pool": [((225, 215, 192), (162, 152, 130)), ((238, 228, 205), (175, 165, 142))],
        "patterns": ["smooth", "smooth", "fractured"],
        "specials_pool": ["complete", "mineralized"],
    },
    "ginkgo_leaf": {
        "min_depth": 102,
        "age": "mesozoic",
        "rarity_pool": ["uncommon", "rare", "rare", "epic"],
        "color_pool": [((98, 118, 78), (62, 78, 48)), ((112, 132, 92), (72, 90, 58))],
        "patterns": ["smooth", "fractured", "ridged"],
        "specials_pool": ["impression", "carbonized", "complete"],
    },
    "echinoid": {
        "min_depth": 104,
        "age": "mesozoic",
        "rarity_pool": ["uncommon", "uncommon", "rare", "epic"],
        "color_pool": [((225, 218, 198), (165, 158, 138)), ((238, 232, 212), (178, 172, 152))],
        "patterns": ["ridged", "smooth", "ridged"],
        "specials_pool": ["complete", "mineralized", "opalized"],
    },
    "theropod_claw": {
        "min_depth": 113,
        "age": "mesozoic",
        "rarity_pool": ["rare", "rare", "epic", "legendary"],
        "color_pool": [((235, 225, 202), (172, 162, 140)), ((248, 238, 215), (185, 175, 152))],
        "patterns": ["smooth", "smooth", "fractured"],
        "specials_pool": ["complete", "mineralized", "amber_trace"],
    },
    "coprolite": {
        "min_depth": 117,
        "age": "mesozoic",
        "rarity_pool": ["uncommon", "rare", "rare", "epic"],
        "color_pool": [((108, 98, 82), (68, 62, 50)), ((122, 112, 95), (80, 72, 60))],
        "patterns": ["smooth", "fractured", "smooth"],
        "specials_pool": ["mineralized", "complete"],
    },
    "amber_chunk": {
        "min_depth": 119,
        "age": "mesozoic",
        "rarity_pool": ["rare", "epic", "epic", "legendary"],
        "color_pool": [((215, 165, 55), (160, 118, 35)), ((228, 180, 70), (172, 132, 48))],
        "patterns": ["smooth", "smooth", "fractured"],
        "specials_pool": ["amber_trace", "complete", "impression"],
    },
    "hadrosaur_tooth": {
        "min_depth": 123,
        "age": "mesozoic",
        "rarity_pool": ["rare", "rare", "epic", "epic"],
        "color_pool": [((238, 228, 205), (175, 165, 142)), ((225, 215, 192), (162, 152, 130))],
        "patterns": ["ridged", "ridged", "smooth"],
        "specials_pool": ["complete", "mineralized"],
    },
    "ankylosaur_scute": {
        "min_depth": 127,
        "age": "mesozoic",
        "rarity_pool": ["rare", "epic", "epic", "legendary"],
        "color_pool": [((105, 95, 78), (65, 58, 47)), ((118, 108, 92), (75, 68, 56))],
        "patterns": ["ridged", "fractured", "ridged"],
        "specials_pool": ["mineralized", "complete", "impression"],
    },
    "stegosaur_plate": {
        "min_depth": 131,
        "age": "mesozoic",
        "rarity_pool": ["epic", "epic", "legendary", "legendary"],
        "color_pool": [((195, 175, 138), (140, 122, 95)), ((208, 188, 152), (152, 135, 108))],
        "patterns": ["smooth", "ridged", "fractured"],
        "specials_pool": ["complete", "mineralized", "impression"],
    },
    "wood_opal": {
        "min_depth": 133,
        "age": "mesozoic",
        "rarity_pool": ["epic", "epic", "legendary", "legendary"],
        "color_pool": [((148, 185, 198), (98, 128, 142)), ((162, 200, 215), (112, 142, 158))],
        "patterns": ["ridged", "smooth", "ridged"],
        "specials_pool": ["opalized", "complete", "mineralized"],
    },
    "spinosaur_tooth": {
        "min_depth": 135,
        "age": "mesozoic",
        "rarity_pool": ["epic", "epic", "legendary", "legendary"],
        "color_pool": [((238, 225, 198), (175, 162, 135)), ((252, 238, 212), (188, 175, 148))],
        "patterns": ["smooth", "ridged", "smooth"],
        "specials_pool": ["complete", "mineralized", "opalized"],
    },
    "ichthyosaur_vertebra": {
        "min_depth": 137,
        "age": "mesozoic",
        "rarity_pool": ["epic", "legendary", "legendary", "legendary"],
        "color_pool": [((222, 212, 188), (160, 150, 128)), ((235, 225, 202), (172, 162, 140))],
        "patterns": ["smooth", "ridged", "smooth"],
        "specials_pool": ["complete", "mineralized", "impression"],
    },
    "triceratops_horn_core": {
        "min_depth": 139,
        "age": "mesozoic",
        "rarity_pool": ["epic", "legendary", "legendary", "legendary"],
        "color_pool": [((210, 195, 165), (150, 138, 112)), ((225, 210, 180), (162, 150, 125))],
        "patterns": ["smooth", "ridged", "smooth"],
        "specials_pool": ["complete", "mineralized"],
    },
    "cretaceous_fish": {
        "min_depth": 143,
        "age": "mesozoic",
        "rarity_pool": ["epic", "legendary", "legendary", "legendary"],
        "color_pool": [((72, 68, 58), (45, 42, 35)), ((85, 80, 70), (55, 52, 44))],
        "patterns": ["fractured", "smooth", "ridged"],
        "specials_pool": ["impression", "complete", "carbonized"],
    },
    "giant_ammonite_fragment": {
        "min_depth": 145,
        "age": "mesozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((205, 182, 118), (152, 132, 80)), ((218, 195, 132), (162, 142, 92))],
        "patterns": ["spiral", "ridged", "spiral"],
        "specials_pool": ["opalized", "complete", "mineralized"],
    },
    "titanosaur_bone": {
        "min_depth": 147,
        "age": "mesozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((232, 225, 205), (172, 165, 145)), ((245, 238, 218), (185, 178, 158))],
        "patterns": ["smooth", "fractured", "smooth"],
        "specials_pool": ["complete", "mineralized", "impression"],
    },
    "archaeopteryx_feather": {
        "min_depth": 149,
        "age": "mesozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((62, 58, 50), (38, 35, 30)), ((75, 70, 62), (48, 45, 40))],
        "patterns": ["smooth", "fractured", "ridged"],
        "specials_pool": ["impression", "carbonized", "complete"],
    },
    # --- More Cenozoic ---
    "auroch_horn_core": {
        "min_depth": 153,
        "age": "cenozoic",
        "rarity_pool": ["rare", "epic", "epic", "legendary"],
        "color_pool": [((62, 52, 38), (38, 32, 22)), ((75, 65, 50), (48, 40, 30))],
        "patterns": ["smooth", "ridged", "smooth"],
        "specials_pool": ["complete", "mineralized"],
    },
    "hyena_tooth_giant": {
        "min_depth": 156,
        "age": "cenozoic",
        "rarity_pool": ["rare", "epic", "epic", "legendary"],
        "color_pool": [((238, 228, 205), (175, 165, 142)), ((252, 242, 218), (188, 178, 155))],
        "patterns": ["smooth", "smooth", "fractured"],
        "specials_pool": ["complete", "mineralized"],
    },
    "deinotherium_molar": {
        "min_depth": 158,
        "age": "cenozoic",
        "rarity_pool": ["rare", "epic", "legendary", "legendary"],
        "color_pool": [((205, 192, 168), (148, 138, 118)), ((218, 205, 182), (160, 150, 130))],
        "patterns": ["ridged", "ridged", "smooth"],
        "specials_pool": ["mineralized", "complete", "impression"],
    },
    "merychippus_tooth": {
        "min_depth": 160,
        "age": "cenozoic",
        "rarity_pool": ["epic", "epic", "legendary", "legendary"],
        "color_pool": [((235, 225, 205), (172, 162, 142)), ((248, 238, 218), (185, 175, 155))],
        "patterns": ["ridged", "smooth", "ridged"],
        "specials_pool": ["complete", "mineralized"],
    },
    "gastornis_bone": {
        "min_depth": 162,
        "age": "cenozoic",
        "rarity_pool": ["epic", "epic", "legendary", "legendary"],
        "color_pool": [((155, 145, 125), (105, 98, 82)), ((168, 158, 138), (115, 108, 92))],
        "patterns": ["smooth", "fractured", "smooth"],
        "specials_pool": ["complete", "mineralized", "impression"],
    },
    "entelodont_jaw": {
        "min_depth": 163,
        "age": "cenozoic",
        "rarity_pool": ["epic", "legendary", "legendary", "legendary"],
        "color_pool": [((88, 78, 62), (55, 48, 38)), ((102, 92, 75), (65, 58, 46))],
        "patterns": ["smooth", "fractured", "ridged"],
        "specials_pool": ["complete", "mineralized"],
    },
    "toxodon_rib": {
        "min_depth": 164,
        "age": "cenozoic",
        "rarity_pool": ["epic", "legendary", "legendary", "legendary"],
        "color_pool": [((225, 215, 195), (162, 155, 138)), ((238, 228, 208), (175, 168, 150))],
        "patterns": ["smooth", "ridged", "smooth"],
        "specials_pool": ["complete", "mineralized", "impression"],
    },
    "smilodon_scapula": {
        "min_depth": 167,
        "age": "cenozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((242, 232, 212), (180, 170, 150)), ((255, 245, 225), (192, 182, 162))],
        "patterns": ["smooth", "fractured", "smooth"],
        "specials_pool": ["complete", "mineralized"],
    },
    "giant_beaver_incisor": {
        "min_depth": 169,
        "age": "cenozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((195, 115, 45), (142, 82, 28)), ((210, 130, 58), (155, 95, 38))],
        "patterns": ["ridged", "smooth", "ridged"],
        "specials_pool": ["complete", "mineralized"],
    },
    "short_faced_bear_claw": {
        "min_depth": 170,
        "age": "cenozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((238, 228, 210), (178, 168, 150)), ((252, 242, 224), (192, 182, 164))],
        "patterns": ["smooth", "fractured", "smooth"],
        "specials_pool": ["complete", "mineralized"],
    },
    "megaloceros_antler": {
        "min_depth": 174,
        "age": "cenozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((115, 98, 72), (75, 62, 45)), ((128, 112, 85), (85, 72, 55))],
        "patterns": ["smooth", "ridged", "fractured"],
        "specials_pool": ["complete", "mineralized", "impression"],
    },
    "basilosaurus_tooth": {
        "min_depth": 176,
        "age": "cenozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((242, 232, 212), (180, 170, 150)), ((228, 218, 198), (168, 158, 138))],
        "patterns": ["smooth", "smooth", "fractured"],
        "specials_pool": ["complete", "mineralized", "opalized"],
    },
    "woolly_rhino_tooth": {
        "min_depth": 178,
        "age": "cenozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((205, 195, 175), (148, 140, 122)), ((218, 208, 188), (160, 152, 135))],
        "patterns": ["ridged", "ridged", "smooth"],
        "specials_pool": ["complete", "mineralized"],
    },
    "andrewsarchus_molar": {
        "min_depth": 180,
        "age": "cenozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((92, 82, 68), (58, 52, 42)), ((105, 95, 80), (68, 62, 52))],
        "patterns": ["ridged", "smooth", "fractured"],
        "specials_pool": ["complete", "mineralized"],
    },
    "uintatherium_horn": {
        "min_depth": 182,
        "age": "cenozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((88, 80, 68), (55, 50, 42)), ((102, 94, 80), (65, 60, 50))],
        "patterns": ["smooth", "ridged", "smooth"],
        "specials_pool": ["complete", "mineralized", "impression"],
    },
    "pakicetus_bone": {
        "min_depth": 184,
        "age": "cenozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((225, 215, 195), (165, 155, 138)), ((238, 228, 208), (178, 168, 150))],
        "patterns": ["smooth", "fractured", "smooth"],
        "specials_pool": ["complete", "mineralized"],
    },
    "paraceratherium_vertebra": {
        "min_depth": 186,
        "age": "cenozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((245, 238, 220), (185, 178, 162)), ((232, 225, 208), (172, 165, 150))],
        "patterns": ["smooth", "ridged", "smooth"],
        "specials_pool": ["complete", "mineralized", "impression"],
    },
    # --- Cambrian / Deep Paleozoic ---
    "marrella": {
        "min_depth": 51,
        "age": "paleozoic",
        "rarity_pool": ["uncommon", "rare", "epic", "legendary"],
        "color_pool": [((55, 52, 48), (32, 30, 26)), ((68, 65, 60), (42, 40, 36))],
        "patterns": ["smooth", "fractured", "smooth"],
        "specials_pool": ["carbonized", "impression", "complete"],
    },
    "radiolarian_chert": {
        "min_depth": 53,
        "age": "paleozoic",
        "rarity_pool": ["common", "uncommon", "rare", "rare"],
        "color_pool": [((158, 168, 178), (108, 118, 128)), ((145, 155, 168), (98, 108, 120))],
        "patterns": ["fractured", "smooth", "ridged"],
        "specials_pool": ["mineralized", "impression"],
    },
    "tentaculite": {
        "min_depth": 77,
        "age": "paleozoic",
        "rarity_pool": ["common", "uncommon", "uncommon", "rare"],
        "color_pool": [((210, 200, 178), (152, 142, 122)), ((222, 212, 192), (162, 152, 134))],
        "patterns": ["ridged", "smooth", "ridged"],
        "specials_pool": ["mineralized", "impression"],
    },
    "bothriolepis": {
        "min_depth": 73,
        "age": "paleozoic",
        "rarity_pool": ["uncommon", "rare", "rare", "epic"],
        "color_pool": [((98, 92, 80), (62, 58, 50)), ((112, 106, 94), (72, 68, 60))],
        "patterns": ["ridged", "fractured", "smooth"],
        "specials_pool": ["impression", "mineralized", "complete"],
    },
    "dunkleosteus_plate": {
        "min_depth": 81,
        "age": "paleozoic",
        "rarity_pool": ["rare", "rare", "epic", "legendary"],
        "color_pool": [((72, 68, 60), (45, 42, 36)), ((85, 80, 72), (55, 52, 46))],
        "patterns": ["smooth", "fractured", "ridged"],
        "specials_pool": ["complete", "mineralized", "impression"],
    },
    "coelacanth_scale": {
        "min_depth": 84,
        "age": "paleozoic",
        "rarity_pool": ["uncommon", "rare", "rare", "epic"],
        "color_pool": [((105, 118, 102), (68, 78, 66)), ((118, 132, 115), (78, 90, 76))],
        "patterns": ["ridged", "smooth", "ridged"],
        "specials_pool": ["mineralized", "complete"],
    },
    "carboniferous_millipede": {
        "min_depth": 89,
        "age": "paleozoic",
        "rarity_pool": ["rare", "rare", "epic", "epic"],
        "color_pool": [((72, 68, 58), (45, 42, 36)), ((85, 80, 70), (55, 52, 44))],
        "patterns": ["ridged", "smooth", "fractured"],
        "specials_pool": ["carbonized", "impression", "complete"],
    },
    "seed_fern_frond": {
        "min_depth": 90,
        "age": "paleozoic",
        "rarity_pool": ["uncommon", "rare", "rare", "epic"],
        "color_pool": [((88, 102, 72), (55, 65, 44)), ((100, 115, 84), (64, 75, 52))],
        "patterns": ["fractured", "ridged", "smooth"],
        "specials_pool": ["carbonized", "impression"],
    },
    "lycopsid_cone": {
        "min_depth": 92,
        "age": "paleozoic",
        "rarity_pool": ["uncommon", "rare", "epic", "epic"],
        "color_pool": [((110, 120, 98), (70, 78, 62)), ((122, 135, 110), (80, 90, 72))],
        "patterns": ["ridged", "fractured", "smooth"],
        "specials_pool": ["carbonized", "impression", "mineralized"],
    },
    "ichthyostega_limb": {
        "min_depth": 94,
        "age": "paleozoic",
        "rarity_pool": ["epic", "epic", "legendary", "legendary"],
        "color_pool": [((135, 118, 95), (90, 78, 62)), ((148, 132, 108), (100, 88, 72))],
        "patterns": ["smooth", "fractured", "smooth"],
        "specials_pool": ["complete", "mineralized", "impression"],
    },
    "wiwaxia": {
        "min_depth": 95,
        "age": "paleozoic",
        "rarity_pool": ["epic", "epic", "legendary", "legendary"],
        "color_pool": [((62, 58, 52), (38, 35, 30)), ((75, 70, 64), (48, 45, 40))],
        "patterns": ["ridged", "smooth", "fractured"],
        "specials_pool": ["impression", "carbonized", "complete"],
    },
    "mesosaurus_rib": {
        "min_depth": 96,
        "age": "paleozoic",
        "rarity_pool": ["rare", "epic", "legendary", "legendary"],
        "color_pool": [((225, 215, 195), (162, 155, 138)), ((238, 228, 208), (175, 168, 150))],
        "patterns": ["smooth", "ridged", "smooth"],
        "specials_pool": ["complete", "mineralized"],
    },
    "pikaia": {
        "min_depth": 97,
        "age": "paleozoic",
        "rarity_pool": ["epic", "legendary", "legendary", "legendary"],
        "color_pool": [((58, 55, 48), (35, 33, 28)), ((70, 66, 60), (44, 42, 37))],
        "patterns": ["smooth", "fractured", "smooth"],
        "specials_pool": ["carbonized", "impression", "complete"],
    },
    "opabinia": {
        "min_depth": 98,
        "age": "paleozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((52, 48, 42), (32, 29, 25)), ((65, 60, 54), (42, 39, 34))],
        "patterns": ["smooth", "fractured", "smooth"],
        "specials_pool": ["carbonized", "impression", "complete"],
    },
    "anomalocaris_appendage": {
        "min_depth": 99,
        "age": "paleozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((48, 44, 38), (28, 26, 22)), ((60, 56, 50), (38, 36, 32))],
        "patterns": ["ridged", "fractured", "smooth"],
        "specials_pool": ["carbonized", "complete", "impression"],
    },
    # --- More Mesozoic ---
    "coral_reef_cretaceous": {
        "min_depth": 103,
        "age": "mesozoic",
        "rarity_pool": ["common", "uncommon", "rare", "rare"],
        "color_pool": [((195, 182, 158), (140, 128, 108)), ((208, 195, 172), (152, 140, 120))],
        "patterns": ["ridged", "fractured", "smooth"],
        "specials_pool": ["mineralized", "complete"],
    },
    "dinosaur_footprint": {
        "min_depth": 106,
        "age": "mesozoic",
        "rarity_pool": ["uncommon", "rare", "rare", "epic"],
        "color_pool": [((158, 148, 130), (108, 100, 86)), ((172, 162, 142), (118, 110, 96))],
        "patterns": ["smooth", "fractured", "smooth"],
        "specials_pool": ["impression", "complete"],
    },
    "nautilus_mesozoic": {
        "min_depth": 107,
        "age": "mesozoic",
        "rarity_pool": ["uncommon", "rare", "rare", "epic"],
        "color_pool": [((205, 188, 155), (148, 132, 105)), ((218, 202, 170), (160, 145, 118))],
        "patterns": ["spiral", "smooth", "spiral"],
        "specials_pool": ["complete", "opalized", "mineralized"],
    },
    "shark_fin_spine_mesozoic": {
        "min_depth": 109,
        "age": "mesozoic",
        "rarity_pool": ["uncommon", "rare", "epic", "epic"],
        "color_pool": [((215, 205, 185), (155, 148, 128)), ((228, 218, 198), (168, 160, 140))],
        "patterns": ["ridged", "smooth", "ridged"],
        "specials_pool": ["mineralized", "complete"],
    },
    "pachyrhizodus_tooth": {
        "min_depth": 116,
        "age": "mesozoic",
        "rarity_pool": ["rare", "rare", "epic", "epic"],
        "color_pool": [((228, 218, 198), (165, 158, 138)), ((242, 232, 212), (178, 172, 152))],
        "patterns": ["smooth", "smooth", "fractured"],
        "specials_pool": ["complete", "mineralized"],
    },
    "sea_turtle_scute": {
        "min_depth": 119,
        "age": "mesozoic",
        "rarity_pool": ["rare", "epic", "epic", "legendary"],
        "color_pool": [((85, 100, 75), (52, 65, 46)), ((98, 115, 88), (62, 76, 56))],
        "patterns": ["ridged", "fractured", "smooth"],
        "specials_pool": ["mineralized", "complete", "impression"],
    },
    "turtle_shell_fragment": {
        "min_depth": 121,
        "age": "mesozoic",
        "rarity_pool": ["rare", "epic", "epic", "legendary"],
        "color_pool": [((105, 92, 72), (68, 60, 46)), ((118, 105, 84), (78, 70, 56))],
        "patterns": ["ridged", "smooth", "fractured"],
        "specials_pool": ["mineralized", "complete"],
    },
    "ornithomimid_bone": {
        "min_depth": 124,
        "age": "mesozoic",
        "rarity_pool": ["rare", "epic", "epic", "legendary"],
        "color_pool": [((232, 222, 202), (170, 162, 142)), ((245, 235, 215), (182, 174, 155))],
        "patterns": ["smooth", "fractured", "smooth"],
        "specials_pool": ["complete", "mineralized"],
    },
    "nodosaur_spike": {
        "min_depth": 126,
        "age": "mesozoic",
        "rarity_pool": ["epic", "epic", "legendary", "legendary"],
        "color_pool": [((115, 102, 82), (75, 66, 52)), ((128, 115, 95), (85, 76, 62))],
        "patterns": ["smooth", "ridged", "smooth"],
        "specials_pool": ["complete", "mineralized", "impression"],
    },
    "plesiosaur_jaw_fragment": {
        "min_depth": 129,
        "age": "mesozoic",
        "rarity_pool": ["epic", "epic", "legendary", "legendary"],
        "color_pool": [((228, 218, 198), (165, 158, 138)), ((242, 232, 212), (178, 172, 152))],
        "patterns": ["smooth", "fractured", "ridged"],
        "specials_pool": ["complete", "mineralized", "impression"],
    },
    "microraptor_impression": {
        "min_depth": 130,
        "age": "mesozoic",
        "rarity_pool": ["epic", "legendary", "legendary", "legendary"],
        "color_pool": [((58, 55, 48), (35, 33, 28)), ((70, 66, 60), (44, 42, 36))],
        "patterns": ["smooth", "fractured", "smooth"],
        "specials_pool": ["impression", "carbonized", "complete"],
    },
    "pachycephalosaur_dome": {
        "min_depth": 132,
        "age": "mesozoic",
        "rarity_pool": ["epic", "legendary", "legendary", "legendary"],
        "color_pool": [((225, 215, 195), (162, 155, 138)), ((238, 228, 208), (175, 168, 150))],
        "patterns": ["smooth", "smooth", "fractured"],
        "specials_pool": ["complete", "mineralized"],
    },
    "allosaurus_tooth": {
        "min_depth": 134,
        "age": "mesozoic",
        "rarity_pool": ["epic", "legendary", "legendary", "legendary"],
        "color_pool": [((235, 225, 202), (172, 165, 142)), ((248, 238, 215), (185, 178, 155))],
        "patterns": ["smooth", "ridged", "smooth"],
        "specials_pool": ["complete", "mineralized", "opalized"],
    },
    "baryonyx_claw": {
        "min_depth": 135,
        "age": "mesozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((82, 75, 65), (52, 48, 40)), ((95, 88, 78), (62, 58, 50))],
        "patterns": ["smooth", "fractured", "smooth"],
        "specials_pool": ["complete", "mineralized"],
    },
    "velociraptor_tooth": {
        "min_depth": 138,
        "age": "mesozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((242, 232, 212), (180, 172, 152)), ((255, 245, 225), (192, 185, 165))],
        "patterns": ["smooth", "smooth", "fractured"],
        "specials_pool": ["complete", "mineralized", "amber_trace"],
    },
    "ankylosaurus_tail_club": {
        "min_depth": 139,
        "age": "mesozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((105, 95, 78), (68, 62, 50)), ((118, 108, 92), (78, 72, 60))],
        "patterns": ["smooth", "ridged", "fractured"],
        "specials_pool": ["complete", "mineralized", "impression"],
    },
    "ceratopsian_frill": {
        "min_depth": 141,
        "age": "mesozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((222, 212, 190), (160, 152, 132)), ((235, 225, 204), (172, 165, 145))],
        "patterns": ["smooth", "fractured", "ridged"],
        "specials_pool": ["complete", "mineralized", "impression"],
    },
    "rebbachisaurus_spine": {
        "min_depth": 143,
        "age": "mesozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((235, 228, 208), (174, 168, 150)), ((248, 242, 222), (188, 182, 164))],
        "patterns": ["smooth", "ridged", "smooth"],
        "specials_pool": ["complete", "mineralized"],
    },
    # --- More Cenozoic ---
    "giant_tortoise_scute": {
        "min_depth": 152,
        "age": "cenozoic",
        "rarity_pool": ["rare", "epic", "epic", "legendary"],
        "color_pool": [((88, 78, 62), (55, 48, 38)), ((102, 92, 75), (65, 58, 47))],
        "patterns": ["ridged", "fractured", "smooth"],
        "specials_pool": ["complete", "mineralized"],
    },
    "macrauchenia_vertebra": {
        "min_depth": 155,
        "age": "cenozoic",
        "rarity_pool": ["rare", "epic", "legendary", "legendary"],
        "color_pool": [((228, 218, 198), (168, 160, 140)), ((242, 232, 212), (180, 172, 152))],
        "patterns": ["smooth", "ridged", "smooth"],
        "specials_pool": ["complete", "mineralized"],
    },
    "thylacosmilus_fang": {
        "min_depth": 157,
        "age": "cenozoic",
        "rarity_pool": ["epic", "epic", "legendary", "legendary"],
        "color_pool": [((248, 238, 218), (185, 178, 158)), ((235, 225, 205), (175, 168, 148))],
        "patterns": ["smooth", "smooth", "fractured"],
        "specials_pool": ["complete", "mineralized"],
    },
    "giant_penguin_bone": {
        "min_depth": 159,
        "age": "cenozoic",
        "rarity_pool": ["epic", "epic", "legendary", "legendary"],
        "color_pool": [((218, 208, 188), (158, 150, 132)), ((232, 222, 202), (170, 162, 145))],
        "patterns": ["smooth", "fractured", "smooth"],
        "specials_pool": ["complete", "mineralized", "impression"],
    },
    "palaeotherium_tooth": {
        "min_depth": 161,
        "age": "cenozoic",
        "rarity_pool": ["epic", "legendary", "legendary", "legendary"],
        "color_pool": [((238, 228, 208), (175, 168, 148)), ((225, 215, 195), (165, 158, 138))],
        "patterns": ["ridged", "smooth", "ridged"],
        "specials_pool": ["complete", "mineralized"],
    },
    "megalodon_tooth": {
        "min_depth": 163,
        "age": "cenozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((62, 58, 52), (38, 35, 30)), ((75, 70, 64), (48, 45, 40))],
        "patterns": ["smooth", "smooth", "fractured"],
        "specials_pool": ["complete", "mineralized", "opalized"],
    },
    "chalicothere_claw": {
        "min_depth": 165,
        "age": "cenozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((72, 62, 50), (45, 38, 30)), ((85, 75, 62), (55, 48, 38))],
        "patterns": ["smooth", "ridged", "smooth"],
        "specials_pool": ["complete", "mineralized"],
    },
    "procoptodon_claw": {
        "min_depth": 167,
        "age": "cenozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((232, 222, 202), (172, 162, 142)), ((245, 235, 215), (185, 175, 155))],
        "patterns": ["smooth", "fractured", "smooth"],
        "specials_pool": ["complete", "mineralized"],
    },
    "embolotherium_horn": {
        "min_depth": 171,
        "age": "cenozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((80, 72, 62), (50, 45, 38)), ((92, 84, 74), (60, 55, 48))],
        "patterns": ["smooth", "ridged", "smooth"],
        "specials_pool": ["complete", "mineralized", "impression"],
    },
    "hyracotherium_molar": {
        "min_depth": 173,
        "age": "cenozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((238, 228, 208), (178, 168, 148)), ((252, 242, 222), (190, 180, 160))],
        "patterns": ["ridged", "smooth", "ridged"],
        "specials_pool": ["complete", "mineralized"],
    },
    "mesonyx_jaw": {
        "min_depth": 175,
        "age": "cenozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((105, 95, 78), (68, 62, 50)), ((118, 108, 92), (78, 72, 60))],
        "patterns": ["smooth", "fractured", "ridged"],
        "specials_pool": ["complete", "mineralized"],
    },
    "arsinoitherium_horn": {
        "min_depth": 177,
        "age": "cenozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((68, 62, 55), (42, 38, 33)), ((80, 74, 66), (52, 48, 42))],
        "patterns": ["smooth", "ridged", "smooth"],
        "specials_pool": ["complete", "mineralized", "impression"],
    },
    "sivatherium_ossicone": {
        "min_depth": 179,
        "age": "cenozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((92, 80, 62), (58, 50, 38)), ((105, 94, 75), (68, 60, 48))],
        "patterns": ["smooth", "ridged", "fractured"],
        "specials_pool": ["complete", "mineralized"],
    },
    "diprotodon_molar": {
        "min_depth": 181,
        "age": "cenozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((215, 205, 185), (155, 148, 130)), ((228, 218, 198), (168, 160, 142))],
        "patterns": ["ridged", "ridged", "smooth"],
        "specials_pool": ["complete", "mineralized"],
    },
    "thylacoleo_tooth": {
        "min_depth": 183,
        "age": "cenozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((245, 235, 215), (185, 178, 158)), ((232, 222, 202), (175, 168, 148))],
        "patterns": ["smooth", "fractured", "smooth"],
        "specials_pool": ["complete", "mineralized", "opalized"],
    },
    "josephoartigasia_incisor": {
        "min_depth": 185,
        "age": "cenozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((188, 108, 42), (138, 78, 26)), ((202, 122, 55), (150, 90, 35))],
        "patterns": ["ridged", "smooth", "ridged"],
        "specials_pool": ["complete", "mineralized"],
    },
    "stegodon_molar": {
        "min_depth": 187,
        "age": "cenozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((210, 200, 180), (152, 144, 126)), ((222, 212, 192), (162, 155, 138))],
        "patterns": ["ridged", "ridged", "smooth"],
        "specials_pool": ["complete", "mineralized", "impression"],
    },
    # --- More Paleozoic ---
    "pentamerus": {
        "min_depth": 59,
        "age": "paleozoic",
        "rarity_pool": ["common", "uncommon", "uncommon", "rare"],
        "color_pool": [((182, 168, 145), (130, 118, 98)), ((168, 155, 132), (118, 105, 85))],
        "patterns": ["ridged", "smooth", "smooth"],
        "specials_pool": ["impression", "mineralized", "complete"],
    },
    "cameroceras_fragment": {
        "min_depth": 66,
        "age": "paleozoic",
        "rarity_pool": ["uncommon", "rare", "rare", "epic"],
        "color_pool": [((195, 182, 158), (140, 128, 108)), ((210, 195, 172), (152, 140, 118))],
        "patterns": ["ridged", "smooth", "spiral"],
        "specials_pool": ["complete", "mineralized", "opalized"],
    },
    "phacops_eye": {
        "min_depth": 69,
        "age": "paleozoic",
        "rarity_pool": ["uncommon", "rare", "epic", "epic"],
        "color_pool": [((85, 78, 68), (52, 48, 40)), ((100, 92, 80), (62, 58, 50))],
        "patterns": ["ridged", "fractured", "smooth"],
        "specials_pool": ["impression", "mineralized", "complete"],
    },
    "receptaculites": {
        "min_depth": 74,
        "age": "paleozoic",
        "rarity_pool": ["uncommon", "rare", "rare", "epic"],
        "color_pool": [((168, 175, 152), (115, 122, 102)), ((182, 190, 165), (128, 135, 115))],
        "patterns": ["ridged", "fractured", "smooth"],
        "specials_pool": ["mineralized", "complete"],
    },
    "sigillaria_bark": {
        "min_depth": 91,
        "age": "paleozoic",
        "rarity_pool": ["uncommon", "rare", "rare", "epic"],
        "color_pool": [((108, 118, 95), (68, 76, 58)), ((122, 132, 108), (78, 88, 68))],
        "patterns": ["ridged", "ridged", "fractured"],
        "specials_pool": ["impression", "carbonized", "complete"],
    },
    "proterogyrinus_vertebra": {
        "min_depth": 95,
        "age": "paleozoic",
        "rarity_pool": ["rare", "epic", "epic", "legendary"],
        "color_pool": [((132, 118, 98), (88, 76, 62)), ((145, 132, 110), (98, 88, 72))],
        "patterns": ["smooth", "fractured", "smooth"],
        "specials_pool": ["complete", "mineralized", "impression"],
    },
    # --- More Mesozoic ---
    "tethyan_coral": {
        "min_depth": 105,
        "age": "mesozoic",
        "rarity_pool": ["common", "uncommon", "rare", "rare"],
        "color_pool": [((198, 185, 158), (142, 130, 108)), ((212, 198, 172), (155, 142, 120))],
        "patterns": ["ridged", "fractured", "smooth"],
        "specials_pool": ["mineralized", "complete"],
    },
    "hybodus_spine": {
        "min_depth": 114,
        "age": "mesozoic",
        "rarity_pool": ["uncommon", "rare", "epic", "epic"],
        "color_pool": [((228, 218, 198), (165, 158, 138)), ((242, 232, 212), (178, 172, 152))],
        "patterns": ["ridged", "smooth", "ridged"],
        "specials_pool": ["mineralized", "complete"],
    },
    "pachycormid_scale": {
        "min_depth": 117,
        "age": "mesozoic",
        "rarity_pool": ["uncommon", "rare", "rare", "epic"],
        "color_pool": [((118, 138, 112), (78, 92, 74)), ((132, 152, 126), (88, 105, 84))],
        "patterns": ["ridged", "ridged", "smooth"],
        "specials_pool": ["impression", "mineralized", "complete"],
    },
    "rhamphorhynchus_bone": {
        "min_depth": 121,
        "age": "mesozoic",
        "rarity_pool": ["rare", "epic", "epic", "legendary"],
        "color_pool": [((235, 225, 202), (172, 165, 142)), ((248, 238, 215), (185, 178, 155))],
        "patterns": ["smooth", "fractured", "smooth"],
        "specials_pool": ["complete", "mineralized", "impression"],
    },
    "kentrosaurus_spike": {
        "min_depth": 128,
        "age": "mesozoic",
        "rarity_pool": ["rare", "epic", "epic", "legendary"],
        "color_pool": [((188, 172, 142), (135, 122, 98)), ((202, 185, 155), (148, 135, 110))],
        "patterns": ["smooth", "ridged", "fractured"],
        "specials_pool": ["complete", "mineralized"],
    },
    "abelisaurid_tooth": {
        "min_depth": 136,
        "age": "mesozoic",
        "rarity_pool": ["epic", "epic", "legendary", "legendary"],
        "color_pool": [((242, 232, 210), (180, 172, 150)), ((228, 218, 198), (168, 160, 140))],
        "patterns": ["smooth", "smooth", "fractured"],
        "specials_pool": ["complete", "mineralized", "opalized"],
    },
    "leedsichthys_scale": {
        "min_depth": 142,
        "age": "mesozoic",
        "rarity_pool": ["epic", "epic", "legendary", "legendary"],
        "color_pool": [((75, 72, 62), (46, 44, 38)), ((88, 84, 75), (56, 54, 48))],
        "patterns": ["ridged", "fractured", "smooth"],
        "specials_pool": ["mineralized", "complete", "impression"],
    },
    "iguanodon_thumb": {
        "min_depth": 140,
        "age": "mesozoic",
        "rarity_pool": ["epic", "legendary", "legendary", "legendary"],
        "color_pool": [((88, 80, 68), (55, 50, 42)), ((102, 92, 80), (65, 60, 50))],
        "patterns": ["smooth", "ridged", "smooth"],
        "specials_pool": ["complete", "mineralized"],
    },
    "tapejara_crest_fragment": {
        "min_depth": 145,
        "age": "mesozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((198, 88, 72), (142, 62, 50)), ((215, 102, 85), (155, 75, 62))],
        "patterns": ["smooth", "fractured", "smooth"],
        "specials_pool": ["complete", "mineralized", "impression"],
    },
    "giraffatitan_rib": {
        "min_depth": 148,
        "age": "mesozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((238, 228, 210), (178, 170, 152)), ((252, 242, 225), (192, 184, 166))],
        "patterns": ["smooth", "ridged", "fractured"],
        "specials_pool": ["complete", "mineralized"],
    },
    # --- More Cenozoic ---
    "synthetoceras_horn": {
        "min_depth": 156,
        "age": "cenozoic",
        "rarity_pool": ["rare", "epic", "epic", "legendary"],
        "color_pool": [((78, 68, 56), (48, 42, 34)), ((92, 82, 68), (58, 52, 42))],
        "patterns": ["smooth", "ridged", "smooth"],
        "specials_pool": ["complete", "mineralized"],
    },
    "amphicyon_jaw": {
        "min_depth": 160,
        "age": "cenozoic",
        "rarity_pool": ["epic", "epic", "legendary", "legendary"],
        "color_pool": [((82, 72, 60), (52, 45, 36)), ((95, 85, 72), (60, 54, 45))],
        "patterns": ["smooth", "fractured", "ridged"],
        "specials_pool": ["complete", "mineralized"],
    },
    "amebelodon_tusk_fragment": {
        "min_depth": 162,
        "age": "cenozoic",
        "rarity_pool": ["epic", "legendary", "legendary", "legendary"],
        "color_pool": [((242, 235, 218), (182, 175, 160)), ((228, 222, 205), (170, 164, 148))],
        "patterns": ["smooth", "ridged", "smooth"],
        "specials_pool": ["complete", "mineralized", "impression"],
    },
    "apidium_molar": {
        "min_depth": 165,
        "age": "cenozoic",
        "rarity_pool": ["epic", "legendary", "legendary", "legendary"],
        "color_pool": [((248, 238, 218), (185, 178, 158)), ((235, 225, 205), (175, 168, 148))],
        "patterns": ["ridged", "smooth", "ridged"],
        "specials_pool": ["complete", "mineralized"],
    },
    "pezosiren_rib": {
        "min_depth": 171,
        "age": "cenozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((235, 228, 210), (175, 170, 152)), ((222, 215, 198), (165, 158, 142))],
        "patterns": ["smooth", "ridged", "smooth"],
        "specials_pool": ["complete", "mineralized"],
    },
    "homotherium_fang": {
        "min_depth": 174,
        "age": "cenozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((248, 240, 222), (188, 182, 165)), ((235, 228, 210), (178, 172, 155))],
        "patterns": ["smooth", "smooth", "fractured"],
        "specials_pool": ["complete", "mineralized", "opalized"],
    },
    "doedicurus_scute": {
        "min_depth": 176,
        "age": "cenozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((162, 142, 112), (112, 98, 75)), ((175, 155, 125), (125, 110, 86))],
        "patterns": ["ridged", "fractured", "ridged"],
        "specials_pool": ["complete", "mineralized", "impression"],
    },
    "zygorhiza_tooth": {
        "min_depth": 179,
        "age": "cenozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((235, 225, 205), (175, 165, 145)), ((248, 238, 218), (188, 178, 158))],
        "patterns": ["smooth", "fractured", "smooth"],
        "specials_pool": ["complete", "mineralized"],
    },
    "elasmotherium_horn_core": {
        "min_depth": 182,
        "age": "cenozoic",
        "rarity_pool": ["legendary", "legendary", "legendary", "legendary"],
        "color_pool": [((62, 55, 48), (38, 34, 28)), ((75, 68, 60), (48, 44, 37))],
        "patterns": ["ridged", "ridged", "smooth"],
        "specials_pool": ["complete", "mineralized", "impression"],
    },
}

FOSSIL_TYPE_ORDER = sorted(FOSSIL_TYPES.keys(), key=lambda t: FOSSIL_TYPES[t]["min_depth"])

FOSSIL_SIZES = ["fragment", "small", "medium", "large", "complete"]

FOSSIL_RARITY_WEIGHTS = {
    "shallow": {"common": 60, "uncommon": 30, "rare": 8, "epic": 1, "legendary": 1},
    "mid":     {"common": 30, "uncommon": 40, "rare": 20, "epic": 8, "legendary": 2},
    "deep":    {"common": 10, "uncommon": 25, "rare": 35, "epic": 22, "legendary": 8},
}

FOSSIL_RARITY_PROPS = {
    "common":    {"clarity": (0.10, 0.45), "detail": (0.10, 0.45), "specials": (0, 0)},
    "uncommon":  {"clarity": (0.25, 0.60), "detail": (0.25, 0.60), "specials": (0, 1)},
    "rare":      {"clarity": (0.40, 0.75), "detail": (0.40, 0.75), "specials": (0, 1)},
    "epic":      {"clarity": (0.55, 0.88), "detail": (0.55, 0.88), "specials": (1, 2)},
    "legendary": {"clarity": (0.72, 1.00), "detail": (0.72, 1.00), "specials": (2, 3)},
}

FOSSIL_SPECIALS = ["mineralized", "complete", "impression", "opalized", "carbonized", "amber_trace"]

FOSSIL_SPECIAL_DESCS = {
    "mineralized": "Replaced by minerals — enhanced clarity",
    "complete":    "Unusually whole specimen",
    "impression":  "Perfect matrix impression preserved",
    "opalized":    "Rare opal replacement — exceptional value",
    "carbonized":  "Carbon film perfectly captures soft tissue",
    "amber_trace": "Amber inclusions visible in the matrix",
}

FOSSIL_AGE_COLORS = {
    "paleozoic": (180, 160, 120),
    "mesozoic":  (160, 190, 140),
    "cenozoic":  (200, 170, 130),
}

FOSSIL_TYPE_DESCRIPTIONS = {
    "trilobite":         "An ancient arthropod with a segmented shell, common in Paleozoic seas.",
    "brachiopod":        "A shelled marine invertebrate that filtered nutrients from the sea floor.",
    "crinoid":           "A sea lily that anchored to the ocean floor and waved feathery arms.",
    "nautiloid":         "An ancestor of modern nautiluses, with a chambered coiled shell.",
    "graptolite":        "A colonial organism whose carbon traces appear as fine lines in shale.",
    "coral_colony":      "A reef-building organism that formed dense limestone masses.",
    "ammonite":          "An extinct cephalopod with a distinctive spiral shell.",
    "belemnite":         "A squid-like creature whose hard internal shell is commonly fossilized.",
    "ichthyosaur_tooth": "A tooth from a dolphin-shaped marine reptile of the Mesozoic seas.",
    "fern_frond":        "A plant impression showing the delicate fronds of an ancient fern.",
    "pine_cone_fossil":  "A mineralized cone from an early coniferous tree.",
    "sea_lily":          "A crinoid-like echinoderm with feathery feeding arms.",
    "sabertooth":        "A fang from Smilodon, the iconic saber-toothed predator.",
    "mammoth_molar":     "A ridged molar from a woolly mammoth, built for grinding tough grass.",
    "ancient_bird":      "Delicate bones or a feather impression from a Cenozoic bird.",
    "giant_insect":      "An insect preserved in amber or compressed shale from a warmer era.",
    "seed_pod":          "A mineralized seed pod from an early flowering plant.",
    "whale_bone":             "A fragment from a prehistoric whale that walked on four legs.",
    "eurypterid":             "A fearsome sea scorpion that prowled shallow Paleozoic seas.",
    "placoderm_scale":        "A bony scale from an armored fish of the Devonian oceans.",
    "orthoceras":             "A straight-shelled nautiloid that swam upright in Silurian seas.",
    "rugose_coral":           "A solitary horn-shaped coral from Paleozoic reef communities.",
    "spiriferid":             "A brachiopod with delicate spiral internal supports for feeding.",
    "bryozoan":               "A colonial filter feeder that built lacy mat-like colonies on the sea floor.",
    "blastoid":               "A star-shaped echinoderm that anchored to ancient sea floors.",
    "shark_tooth_paleozoic":  "A tooth from an early cartilaginous fish that prowled Paleozoic seas.",
    "ostracod_cluster":       "A cluster of tiny bivalved crustaceans preserved together in matrix.",
    "mosasaur_scale":         "A scale from a mosasaur, a giant marine lizard of the Cretaceous seas.",
    "pterosaur_bone":         "A hollow, lightweight bone from the wing of a flying pterosaur.",
    "dinosaur_egg_fragment":  "A curved eggshell fragment from a nesting dinosaur's clutch.",
    "cycad_frond":            "A frond impression from a cycad, the palm-like dominant plant of the Mesozoic.",
    "plesiosaur_vertebra":    "A neck vertebra from a long-necked plesiosaur that hunted fish.",
    "crocodilian_tooth":      "A conical tooth from an ancient crocodilian predator.",
    "shark_tooth_mesozoic":   "A serrated tooth from a large Cretaceous shark.",
    "insect_wing":            "A delicate wing venation impression from a Mesozoic insect.",
    "sauropod_scale":         "A skin scale impression from a massive sauropod dinosaur.",
    "cave_bear_claw":         "A curved claw from Ursus spelaeus, the giant Pleistocene cave bear.",
    "pollen_deposit":         "Ancient pollen grains preserved in amber or compressed shale.",
    "glyptodon_plate":        "An armored scute from a giant Ice Age relative of the armadillo.",
    "terror_bird_bone":       "A bone from Phorusrhacidae, a giant flightless predatory bird.",
    "giant_sloth_claw":       "A massive claw from Megatherium, a ground sloth as large as an elephant.",
    "dire_wolf_tooth":        "A molar from Canis dirus, the formidable Ice Age dire wolf.",
    "elephant_ancestor_tusk":    "A tusk fragment from an early proboscidean ancestor of modern elephants.",
    "stromatolite":              "A layered dome of ancient cyanobacteria, among the oldest fossils on Earth.",
    "conodont":                  "Tiny tooth-like elements from an eel-shaped early vertebrate.",
    "tabulate_coral":            "A colonial coral forming honeycomb or chain patterns in Paleozoic limestone.",
    "lingulid":                  "An inarticulate brachiopod virtually unchanged for 500 million years.",
    "cephalaspis_shield":        "The bony head shield of a jawless Devonian fish.",
    "scolecodont":               "The fossilized jaw of an ancient polychaete worm.",
    "acanthodian_spine":         "A defensive fin spine from an acanthodian, one of the first jawed fishes.",
    "xiphosuran":                "An ancient horseshoe crab relative, a design unchanged to the present day.",
    "calamite_stem":             "A ribbed stem section from a giant Carboniferous horsetail tree.",
    "fusulinid":                 "A rice-grain shaped foraminifera common in late Paleozoic rock.",
    "lepidodendron_bark":        "Bark showing the diamond leaf scars of a Carboniferous club moss tree.",
    "archaeocyathid":            "A sponge-like organism that built Cambrian reefs before going extinct.",
    "diplocaulus_skull":         "The distinctive boomerang-shaped skull of a Permian amphibian.",
    "dimetrodon_spine":          "A dorsal spine from the iconic sail-backed Permian predator.",
    "hallucigenia":              "A bizarre Cambrian worm bristling with spines, once described upside-down.",
    "lystrosaurus_tooth":        "A tooth from the pig-sized survivor that repopulated Earth after the Permian extinction.",
    "nothosaur_tooth":           "A needle-sharp tooth from a Triassic marine reptile.",
    "ginkgo_leaf":               "A fan-shaped leaf from the ancient ginkgo, a true living fossil.",
    "echinoid":                  "A sea urchin test, often found perfectly preserved in chalk.",
    "theropod_claw":             "A sickle-shaped killing claw from a theropod dinosaur.",
    "coprolite":                 "Fossilized dinosaur droppings that preserve clues about ancient diets.",
    "amber_chunk":               "A chunk of fossilized tree resin trapping ancient inclusions.",
    "hadrosaur_tooth":           "A fragment of the complex grinding tooth battery of a duck-billed dinosaur.",
    "ankylosaur_scute":          "An armored bony scute from the back of an ankylosaur.",
    "stegosaur_plate":           "A bony dorsal plate from a Stegosaurus, whose function is still debated.",
    "wood_opal":                 "Ancient wood replaced by opal, producing stunning iridescent colors.",
    "spinosaur_tooth":           "A conical tooth from Spinosaurus, the largest known predatory dinosaur.",
    "ichthyosaur_vertebra":      "A disc-shaped vertebra from a dolphin-like Mesozoic marine reptile.",
    "triceratops_horn_core":     "The bony core of a Triceratops horn, fused directly to the skull.",
    "cretaceous_fish":           "A small fish preserved whole in fine-grained Cretaceous sediment.",
    "giant_ammonite_fragment":   "A slab from an ammonite that grew to over two metres across.",
    "titanosaur_bone":           "An air-filled bone from a titanosaur, one of the largest animals ever.",
    "archaeopteryx_feather":     "A feather impression from Archaeopteryx, the first known bird.",
    "auroch_horn_core":          "A horn core from Bos primigenius, the wild ancestor of all cattle.",
    "hyena_tooth_giant":         "A tooth from Pachycrocuta, a spotted hyena as large as a modern lion.",
    "deinotherium_molar":        "A molar from Deinotherium, an elephant relative with downward-curving tusks.",
    "merychippus_tooth":         "A high-crowned tooth from a three-toed Miocene horse ancestor.",
    "gastornis_bone":            "A bone from Gastornis, a giant flightless bird that dominated the Eocene.",
    "entelodont_jaw":            "A jaw fragment from an entelodont, the fearsome Eocene 'hell pig'.",
    "toxodon_rib":               "A rib from Toxodon, a hippo-sized South American ungulate.",
    "smilodon_scapula":          "A shoulder blade from Smilodon fatalis, the famous saber-toothed cat.",
    "giant_beaver_incisor":      "A massive orange incisor from Castoroides, a beaver the size of a black bear.",
    "short_faced_bear_claw":     "A claw from Arctodus sinus, the largest bear-like predator to ever live.",
    "megaloceros_antler":        "A fragment from the enormous antler of the Irish elk, spanning 3.7 metres.",
    "basilosaurus_tooth":        "A tooth from Basilosaurus, a serpentine early whale up to 18 metres long.",
    "woolly_rhino_tooth":        "A ridged molar from Coelodonta antiquitatis, the woolly rhinoceros.",
    "andrewsarchus_molar":       "A molar from Andrewsarchus, possibly the largest terrestrial mammal predator.",
    "uintatherium_horn":         "A bony horn from Uintatherium, a rhinoceros-sized Eocene herbivore.",
    "pakicetus_bone":            "A bone from Pakicetus, a dog-sized land animal that was an ancestor of all whales.",
    "paraceratherium_vertebra":   "A vertebra from Paraceratherium, the largest land mammal that ever lived.",
    "marrella":                   "A lacy Cambrian arthropod and the most common fossil from the Burgess Shale.",
    "radiolarian_chert":          "A flint-like rock packed with the silica skeletons of microscopic radiolarians.",
    "tentaculite":                "A tiny conical organism of uncertain classification, abundant in Silurian seas.",
    "bothriolepis":               "An antiarch placoderm with jointed pectoral fins, found in Devonian freshwater lakes.",
    "dunkleosteus_plate":         "A bony plate from Dunkleosteus, a 6-metre armoured fish with blade-like bone jaws.",
    "coelacanth_scale":           "A scale from a coelacanth, a lobe-finned fish once thought extinct for 65 million years.",
    "carboniferous_millipede":    "An impression of Arthropleura, a millipede that grew up to 2.5 metres long.",
    "seed_fern_frond":            "A frond from a Carboniferous seed fern, an early plant that reproduced by seeds.",
    "lycopsid_cone":              "A reproductive cone from a lycopsid tree that towered 30 metres in coal swamp forests.",
    "ichthyostega_limb":          "A limb bone from Ichthyostega, one of the first vertebrates to walk on land.",
    "wiwaxia":                    "A Cambrian slug-like creature covered in overlapping sclerites and defensive spines.",
    "mesosaurus_rib":             "A rib from Mesosaurus, one of the first reptiles to return to a fully aquatic life.",
    "pikaia":                     "The earliest known chordate, resembling a tiny fish with a primitive notochord.",
    "opabinia":                   "A bizarre 5-eyed Cambrian predator with a nozzle-tipped frontal proboscis.",
    "anomalocaris_appendage":     "A grasping frontal appendage from Anomalocaris, apex predator of the Cambrian.",
    "coral_reef_cretaceous":      "A section of Cretaceous reef coral, precursor to modern tropical reef ecosystems.",
    "dinosaur_footprint":         "A three-toed dinosaur track preserved in ancient riverbank mudstone.",
    "nautilus_mesozoic":          "A nautilus shell from the Mesozoic, nearly identical to species alive today.",
    "shark_fin_spine_mesozoic":   "A fin spine from a hybodont shark, the dominant shark group of the Mesozoic.",
    "pachyrhizodus_tooth":        "A crushing tooth from Pachyrhizodus, a large bony fish of the Cretaceous seas.",
    "sea_turtle_scute":           "A bony scute from an ancient sea turtle's shell.",
    "turtle_shell_fragment":      "A fragment from the shell of a freshwater turtle from Mesozoic river systems.",
    "ornithomimid_bone":          "A gracile limb bone from an ostrich-mimic dinosaur that may have been feathered.",
    "nodosaur_spike":             "A lateral defensive spike from a nodosaurid ankylosaur.",
    "plesiosaur_jaw_fragment":    "A jaw fragment from a plesiosaur, lined with needle-sharp fish-catching teeth.",
    "microraptor_impression":     "An impression of Microraptor, the famous four-winged feathered dinosaur.",
    "pachycephalosaur_dome":      "The massive fused skull dome of a pachycephalosaur, possibly used in combat.",
    "allosaurus_tooth":           "A serrated tooth from Allosaurus, the dominant predator of the Jurassic period.",
    "baryonyx_claw":              "The enormous curved thumb claw of Baryonyx, a spinosaurid fish hunter.",
    "velociraptor_tooth":         "A small serrated tooth from Velociraptor, far smaller than pop culture suggests.",
    "ankylosaurus_tail_club":     "A fragment from the massive bony tail club of Ankylosaurus.",
    "ceratopsian_frill":          "A piece of the elaborate bony neck frill of a ceratopsian dinosaur.",
    "rebbachisaurus_spine":       "A tall neural spine from Rebbachisaurus, a diplodocid sauropod of Africa.",
    "giant_tortoise_scute":       "A scute from a giant Pleistocene tortoise that could reach over 2 metres long.",
    "macrauchenia_vertebra":      "A vertebra from Macrauchenia, the bizarre long-necked camel-like South American ungulate.",
    "thylacosmilus_fang":         "A sabre-tooth fang from Thylacosmilus, a marsupial that convergently mimicked Smilodon.",
    "giant_penguin_bone":         "A bone from an ancient penguin that stood as tall as a human adult.",
    "palaeotherium_tooth":        "A tooth from Palaeotherium, a tapir-like mammal from the Eocene of Europe.",
    "megalodon_tooth":            "A massive serrated tooth from Otodus megalodon, a shark estimated up to 20 metres long.",
    "chalicothere_claw":          "A hoof-claw from a chalicothere, a horse-relative that walked on its knuckles.",
    "procoptodon_claw":           "A claw from Procoptodon goliah, the largest kangaroo that ever lived.",
    "embolotherium_horn":         "A bony nasal boss from Embolotherium, a massive Eocene brontothere of Asia.",
    "hyracotherium_molar":        "A molar from Hyracotherium, the fox-sized ancestor of all modern horses.",
    "mesonyx_jaw":                "A jaw from Mesonyx, a wolf-like hoofed predator of the Eocene epoch.",
    "arsinoitherium_horn":        "A paired horn core from Arsinoitherium, a rhino-like mammal of Eocene Africa.",
    "sivatherium_ossicone":       "An ossicone from Sivatherium, the largest giraffe to have ever lived.",
    "diprotodon_molar":           "A molar from Diprotodon, a wombat-like marsupial the size of a hippopotamus.",
    "thylacoleo_tooth":           "A carnassial tooth from Thylacoleo carnifex, the marsupial lion of Ice Age Australia.",
    "josephoartigasia_incisor":   "A massive incisor from Josephoartigasia monesi, the largest known rodent.",
    "stegodon_molar":             "A ridged molar from Stegodon, a widespread elephant relative of Asia and Africa.",
    "pentamerus":                 "A clustered Silurian brachiopod whose pentagonal cross-section is immediately recognizable.",
    "cameroceras_fragment":       "A fragment from Cameroceras, a straight-shelled nautiloid that may have reached 9 metres in length.",
    "phacops_eye":                "The compound eye of Phacops, a trilobite famous for its large spherical lenses.",
    "receptaculites":             "A sunflower-shaped Silurian organism of debated affinity, possibly an alga or sponge.",
    "sigillaria_bark":            "Bark bearing the oval leaf cushions of Sigillaria, a Carboniferous scale tree up to 30 metres tall.",
    "proterogyrinus_vertebra":    "A vertebra from a crocodile-like amphibian that was among the top predators of the Carboniferous.",
    "tethyan_coral":              "A colony coral from the ancient Tethys Sea, ancestor of modern tropical reef ecosystems.",
    "hybodus_spine":              "A dorsal fin spine from Hybodus, the most successful shark of the entire Mesozoic era.",
    "pachycormid_scale":          "A large scale from a pachycormid, a group of giant ray-finned fishes that fed by filter-feeding.",
    "rhamphorhynchus_bone":       "A hollow wing bone from Rhamphorhynchus, a long-tailed pterosaur of the Jurassic.",
    "kentrosaurus_spike":         "A paired tail spike from Kentrosaurus, an African stegosaur even more heavily armed than Stegosaurus.",
    "abelisaurid_tooth":          "A stubby, thick-rooted tooth from an abelisaurid theropod, dominant predators of Gondwana.",
    "leedsichthys_scale":         "A scale from Leedsichthys problematicus, possibly the largest bony fish ever to have lived.",
    "iguanodon_thumb":            "The conical thumb spike of Iguanodon, once mistakenly reconstructed as a nose horn.",
    "tapejara_crest_fragment":    "A fragment of the vivid sail-like head crest of Tapejara, a Cretaceous Brazilian pterosaur.",
    "giraffatitan_rib":           "A massive rib from Giraffatitan, the African brachiosaurid whose shoulder height exceeded 6 metres.",
    "synthetoceras_horn":         "The unique Y-shaped nasal horn of Synthetoceras, a Miocene deer-like North American ungulate.",
    "amphicyon_jaw":              "A jaw from Amphicyon, the 'bear-dog' that blended wolf agility with bear-like bulk.",
    "amebelodon_tusk_fragment":   "A shovel-shaped tusk fragment from Amebelodon, a proboscidean that used its tusks to dig up plants.",
    "apidium_molar":              "A molar from Apidium, a small Oligocene primate and an early anthropoid ancestor.",
    "pezosiren_rib":              "A dense rib from Pezosiren, a four-legged ancestor of modern manatees and dugongs.",
    "homotherium_fang":           "A flattened, serrated fang from Homotherium, the scimitar-toothed cat that ranged across four continents.",
    "doedicurus_scute":           "An armored scute from Doedicurus, a glyptodont that swung a spiked bony tail club in defense.",
    "zygorhiza_tooth":            "A tooth from Zygorhiza, an early Eocene whale still retaining hind limbs vestigially.",
    "elasmotherium_horn_core":    "The horn core of Elasmotherium, a giant Pleistocene rhino whose single horn may have exceeded 1.5 metres.",
}


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------

def _fossil_depth_band(depth):
    if depth < 100:
        return "shallow"
    elif depth < 150:
        return "mid"
    return "deep"


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


_SIZE_TO_GRID_N = {"fragment": 4, "small": 5, "medium": 6, "large": 7, "complete": 8}


def generate_prep_grid(fossil):
    """Return (grid, n) where grid is a list-of-lists of cell dicts.

    Cell dict keys:
      type         – "hard" | "soft" | "fragile"
      hits_brush   – brush clicks needed to clear
      chisel_damage – integrity damage if chisel used
    """
    n = _SIZE_TO_GRID_N.get(fossil.size, 5)
    rng = random.Random(fossil.seed ^ 0xBEEF0F)
    cx = (n - 1) / 2.0
    cy = (n - 1) / 2.0
    max_d = math.sqrt(cx * cx + cy * cy) or 1.0
    grid = []
    for row in range(n):
        row_cells = []
        for col in range(n):
            dx = col - cx
            dy = row - cy
            d = math.sqrt(dx * dx + dy * dy) / max_d
            d += rng.uniform(-0.12, 0.12)
            if d < 0.35:
                row_cells.append({"type": "fragile", "hits_brush": 2, "chisel_damage": 20})
            elif d < 0.65:
                row_cells.append({"type": "soft",    "hits_brush": 1, "chisel_damage": 8})
            else:
                row_cells.append({"type": "hard",    "hits_brush": 3, "chisel_damage": 0})
        grid.append(row_cells)
    return grid, n


def apply_preparation_result(fossil, damage_pct):
    """Reduce clarity and detail based on accumulated damage percentage (0–100)."""
    if damage_pct <= 0:
        return
    if damage_pct <= 25:
        reduction = 0.10 * (damage_pct / 25)
    elif damage_pct <= 50:
        reduction = 0.10 + 0.15 * ((damage_pct - 25) / 25)
    elif damage_pct <= 75:
        reduction = 0.25 + 0.15 * ((damage_pct - 50) / 25)
    else:
        reduction = 0.40 + 0.20 * ((damage_pct - 75) / 25)
    fossil.clarity = max(0.05, round(fossil.clarity - reduction, 2))
    fossil.detail  = max(0.05, round(fossil.detail  - reduction, 2))


class FossilGenerator:
    def __init__(self, world_seed):
        self._world_seed = world_seed

    def generate(self, bx, by, depth, biome=None):
        fossil_seed = hash((self._world_seed, bx, by, 0xF055117)) & 0xFFFFFFFF
        rng = random.Random(fossil_seed)

        eligible = [t for t, d in FOSSIL_TYPES.items() if d["min_depth"] <= depth]
        if not eligible:
            eligible = ["trilobite"]

        band = _fossil_depth_band(depth)
        rarity = _weighted_choice(rng, FOSSIL_RARITY_WEIGHTS[band])

        preferred = [t for t in eligible if rarity in FOSSIL_TYPES[t]["rarity_pool"]]
        type_pool = preferred if preferred else eligible

        fossil_type = rng.choice(type_pool)
        tdef = FOSSIL_TYPES[fossil_type]

        colors = rng.choice(tdef["color_pool"])
        primary_color = colors[0]
        secondary_color = colors[1]
        pattern = rng.choice(tdef["patterns"])
        pattern_density = rng.uniform(0.3, 1.0)

        size = rng.choice(FOSSIL_SIZES)
        props = FOSSIL_RARITY_PROPS[rarity]
        clarity = round(rng.uniform(*props["clarity"]), 2)
        detail = round(rng.uniform(*props["detail"]), 2)

        n_specials_min, n_specials_max = props["specials"]
        n_specials = rng.randint(n_specials_min, n_specials_max)
        specials_pool = tdef.get("specials_pool", FOSSIL_SPECIALS)
        specials = rng.sample(specials_pool, min(n_specials, len(specials_pool)))

        uid = f"fossil_{fossil_seed:08x}_{bx}_{by}"

        return Fossil(
            uid=uid,
            fossil_type=fossil_type,
            rarity=rarity,
            size=size,
            primary_color=primary_color,
            secondary_color=secondary_color,
            pattern=pattern,
            pattern_density=pattern_density,
            age=tdef["age"],
            clarity=clarity,
            detail=detail,
            specials=specials,
            depth_found=depth,
            seed=fossil_seed,
        )


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

_fossil_surf_cache = {}
_fossil_codex_cache = {}


def render_fossil(fossil, cell_size=48):
    cache_key = (fossil.uid, cell_size)
    if cache_key in _fossil_surf_cache:
        return _fossil_surf_cache[cache_key]

    rng = random.Random(fossil.seed)
    cx, cy = cell_size // 2, cell_size // 2
    rx = cell_size // 2 - 4
    ry = max(6, cell_size // 3 - 2)

    n_pts = 14
    jitter_amt = min(rx, ry) * 0.14
    pts = []
    for i in range(n_pts):
        a = i * 2 * math.pi / n_pts
        dx = rx + rng.uniform(-jitter_amt, jitter_amt)
        dy = ry + rng.uniform(-jitter_amt, jitter_amt)
        pts.append((cx + dx * math.cos(a), cy + dy * math.sin(a)))

    pc = fossil.primary_color
    sc = fossil.secondary_color
    density = fossil.pattern_density

    final = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
    pygame.draw.polygon(final, pc + (255,), pts)

    pat_surf = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)

    if fossil.pattern == "ridged":
        n_lines = int(3 + density * 6)
        for i in range(n_lines + 1):
            t = i / max(1, n_lines)
            ly = int(cy - ry + t * ry * 2)
            if 0 <= ly < cell_size:
                pygame.draw.line(pat_surf, sc + (175,), (cx - rx, ly), (cx + rx, ly), 1)

    elif fossil.pattern == "spiral":
        n_pts_s = 80
        n_revs = 2.0 + density * 2.0
        for i in range(n_pts_s - 1):
            t0 = i / n_pts_s
            t1 = (i + 1) / n_pts_s
            r0 = t0 * min(rx, ry) * 0.9
            r1 = t1 * min(rx, ry) * 0.9
            a0 = t0 * n_revs * 2 * math.pi
            a1 = t1 * n_revs * 2 * math.pi
            x0 = int(cx + r0 * math.cos(a0))
            y0 = int(cy + r0 * math.sin(a0) * ry / max(rx, 1))
            x1 = int(cx + r1 * math.cos(a1))
            y1 = int(cy + r1 * math.sin(a1) * ry / max(rx, 1))
            if (0 <= x0 < cell_size and 0 <= y0 < cell_size and
                    0 <= x1 < cell_size and 0 <= y1 < cell_size):
                pygame.draw.line(pat_surf, sc + (200,), (x0, y0), (x1, y1), 1)

    elif fossil.pattern == "fractured":
        n_cracks = int(2 + density * 3)
        for _ in range(n_cracks):
            px0 = rng.randint(cx - rx + 3, cx + rx - 3)
            py0 = rng.randint(cy - ry + 2, cy + ry - 2)
            crack = [(px0, py0)]
            for _ in range(rng.randint(2, 4)):
                px0 += rng.randint(-9, 9)
                py0 += rng.randint(-5, 5)
                crack.append((px0, py0))
            if len(crack) >= 2:
                pygame.draw.lines(pat_surf, sc + (195,), False, crack, 1)

    elif fossil.pattern == "smooth":
        n = int(6 + density * 16)
        for _ in range(n):
            px = rng.randint(cx - rx + 2, cx + rx - 2)
            py = rng.randint(cy - ry + 1, cy + ry - 1)
            if 0 <= px < cell_size and 0 <= py < cell_size:
                pat_surf.set_at((px, py), sc + (130,))

    final.blit(pat_surf, (0, 0))

    # Edge darkening inside the polygon boundary
    for i in range(3):
        alpha = 72 - i * 22
        pygame.draw.polygon(final, (0, 0, 0, alpha), pts, 3 - i)

    surf = final

    # Rarity sparkles
    rarities = ["common", "uncommon", "rare", "epic", "legendary"]
    rarity_idx = rarities.index(fossil.rarity)
    if rarity_idx >= 2:
        n_sparks = (rarity_idx - 1) * 3
        for _ in range(n_sparks):
            px = rng.randint(cx - rx + 2, cx + rx - 2)
            py = rng.randint(cy - ry + 1, cy + ry - 1)
            if 0 <= px < cell_size and 0 <= py < cell_size:
                brightness = rng.randint(200, 255)
                surf.set_at((px, py), (brightness, brightness, brightness, 255))

    _fossil_surf_cache[cache_key] = surf
    return surf


def render_fossil_codex_preview(type_key, cell_size=48):
    cache_key = (type_key, cell_size)
    if cache_key in _fossil_codex_cache:
        return _fossil_codex_cache[cache_key]
    tdef = FOSSIL_TYPES.get(type_key)
    if tdef is None:
        s = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
        _fossil_codex_cache[cache_key] = s
        return s
    colors = tdef["color_pool"][0]
    preview = Fossil(
        uid=f"__codex_fossil_{type_key}_{cell_size}__",
        fossil_type=type_key,
        rarity="common",
        size="medium",
        primary_color=colors[0],
        secondary_color=colors[1],
        pattern=tdef["patterns"][0],
        pattern_density=0.6,
        age=tdef["age"],
        clarity=0.5,
        detail=0.5,
        specials=[],
        depth_found=0,
        seed=hash(("fossil_codex", type_key, cell_size)) & 0xFFFFFFFF,
    )
    surf = render_fossil(preview, cell_size)
    _fossil_codex_cache[cache_key] = surf
    return surf
