import math
import random
import pygame
from dataclasses import dataclass, field


@dataclass
class Gemstone:
    uid: str
    gem_type: str
    rarity: str           # common / uncommon / rare / epic / legendary
    size: str             # small / medium / large / exceptional
    state: str            # rough / cut
    cut: str              # raw / tumbled / cabochon / brilliant / step / cushion / pear
    clarity: str          # FL / VVS / VS / SI / I1 / I2
    color_saturation: float  # 0.0 – 1.0
    optical_effect: str   # none / chatoyancy / asterism / color_change / fluorescence / adularescence
    inclusion: str        # none / color_zoning / phantom_crystal / garden / rutile_needles / silk / trapped_fluid / fingerprint / rainbow
    crystal_system: str   # cubic / hexagonal / trigonal / orthorhombic / amorphous
    primary_color: tuple
    secondary_color: tuple
    depth_found: int
    seed: int
    biome: str
    upgrades: list = field(default_factory=list)


# ---------------------------------------------------------------------------
# Gem type definitions
# ---------------------------------------------------------------------------

GEM_TYPES = {
    "amber": {
        "min_depth": 8,
        "crystal_system": "amorphous",
        "rarity_pool": ["common", "common", "common", "uncommon"],
        "color_pool": [
            ((210, 138, 28),  (255, 200, 75)),
            ((185, 112, 18),  (230, 168, 55)),
            ((235, 165, 45),  (255, 218, 110)),
        ],
        "available_cuts": ["tumbled", "cabochon"],
        "optical_effect_pool": {"none": 0.80, "fluorescence": 0.20},
        "inclusion_pool": {"none": 0.45, "color_zoning": 0.25, "trapped_fluid": 0.20, "phantom_crystal": 0.10},
        "biome_affinity": [],
    },
    "garnet": {
        "min_depth": 22,
        "crystal_system": "cubic",
        "rarity_pool": ["common", "uncommon", "uncommon", "rare"],
        "color_pool": [
            ((168, 28,  35),  (220, 65,  70)),
            ((145, 20,  28),  (195, 50,  55)),
            ((185, 42,  55),  (235, 85,  90)),
        ],
        "available_cuts": ["tumbled", "brilliant", "cushion"],
        "optical_effect_pool": {"none": 0.82, "asterism": 0.12, "fluorescence": 0.06},
        "inclusion_pool": {"none": 0.55, "color_zoning": 0.20, "fingerprint": 0.15, "rutile_needles": 0.10},
        "biome_affinity": [],
    },
    "spinel": {
        "min_depth": 38,
        "crystal_system": "cubic",
        "rarity_pool": ["uncommon", "uncommon", "rare", "epic"],
        "color_pool": [
            ((210, 48,  80),  (245, 120, 145)),
            ((155, 48, 175),  (205, 115, 225)),
            ((45,  88, 185),  (105, 150, 235)),
            ((28,  28,  32),  (80,  80,  88)),
        ],
        "available_cuts": ["brilliant", "cushion", "tumbled"],
        "optical_effect_pool": {"none": 0.78, "fluorescence": 0.22},
        "inclusion_pool": {"none": 0.60, "fingerprint": 0.20, "color_zoning": 0.12, "phantom_crystal": 0.08},
        "biome_affinity": [],
    },
    "peridot": {
        "min_depth": 52,
        "crystal_system": "orthorhombic",
        "rarity_pool": ["uncommon", "rare", "rare", "epic"],
        "color_pool": [
            ((125, 195, 52),  (195, 240, 110)),
            ((100, 170, 38),  (168, 218, 88)),
            ((145, 215, 68),  (215, 255, 135)),
        ],
        "available_cuts": ["step", "cushion", "tumbled"],
        "optical_effect_pool": {"none": 0.90, "fluorescence": 0.10},
        "inclusion_pool": {"none": 0.55, "color_zoning": 0.22, "fingerprint": 0.15, "phantom_crystal": 0.08},
        "biome_affinity": ["igneous"],
    },
    "tourmaline": {
        "min_depth": 65,
        "crystal_system": "trigonal",
        "rarity_pool": ["rare", "rare", "uncommon", "epic"],
        "color_pool": [
            ((218, 72, 128),  (78, 168, 105)),
            ((195, 55, 108),  (55, 145, 88)),
            ((235, 98, 155),  (98, 192, 128)),
        ],
        "available_cuts": ["brilliant", "cushion", "cabochon", "pear"],
        "optical_effect_pool": {"none": 0.72, "chatoyancy": 0.20, "fluorescence": 0.08},
        "inclusion_pool": {"none": 0.50, "color_zoning": 0.25, "rutile_needles": 0.15, "silk": 0.10},
        "biome_affinity": [],
    },
    "alexandrite": {
        "min_depth": 85,
        "crystal_system": "orthorhombic",
        "rarity_pool": ["epic", "rare", "epic", "legendary"],
        "color_pool": [
            ((48, 158, 88),   (188, 52,  88)),
            ((38, 138, 72),   (168, 42,  72)),
        ],
        "available_cuts": ["brilliant", "cushion", "step"],
        "optical_effect_pool": {"color_change": 1.0},
        "inclusion_pool": {"none": 0.65, "fingerprint": 0.20, "color_zoning": 0.10, "phantom_crystal": 0.05},
        "biome_affinity": [],
    },
    "emerald": {
        "min_depth": 100,
        "crystal_system": "hexagonal",
        "rarity_pool": ["rare", "epic", "rare", "legendary"],
        "color_pool": [
            ((28, 148, 78),   (72, 205, 128)),
            ((22, 128, 65),   (58, 182, 108)),
            ((35, 165, 88),   (85, 225, 148)),
        ],
        "available_cuts": ["step", "cushion", "cabochon"],
        "optical_effect_pool": {"none": 0.88, "adularescence": 0.12},
        "inclusion_pool": {"none": 0.25, "garden": 0.40, "fingerprint": 0.20, "rainbow": 0.15},
        "biome_affinity": ["sedimentary"],
    },
    "ruby": {
        "min_depth": 118,
        "crystal_system": "trigonal",
        "rarity_pool": ["epic", "rare", "epic", "legendary"],
        "color_pool": [
            ((198, 28,  48),  (245, 88, 105)),
            ((178, 18,  38),  (225, 68,  85)),
            ((215, 42,  65),  (255, 108, 128)),
        ],
        "available_cuts": ["brilliant", "cushion", "cabochon", "pear"],
        "optical_effect_pool": {"none": 0.62, "asterism": 0.22, "fluorescence": 0.16},
        "inclusion_pool": {"none": 0.35, "silk": 0.35, "rutile_needles": 0.20, "fingerprint": 0.10},
        "biome_affinity": ["ferrous"],
    },
    "sapphire": {
        "min_depth": 135,
        "crystal_system": "trigonal",
        "rarity_pool": ["epic", "rare", "epic", "legendary"],
        "color_pool": [
            ((28,  72, 188),  (75, 138, 245)),
            ((22,  55, 165),  (58, 118, 222)),
            ((38,  92, 205),  (95, 158, 255)),
        ],
        "available_cuts": ["brilliant", "cushion", "cabochon", "step"],
        "optical_effect_pool": {"none": 0.60, "asterism": 0.25, "fluorescence": 0.15},
        "inclusion_pool": {"none": 0.38, "silk": 0.32, "rutile_needles": 0.20, "fingerprint": 0.10},
        "biome_affinity": ["crystal"],
    },
    "padparadscha": {
        "min_depth": 158,
        "crystal_system": "trigonal",
        "rarity_pool": ["legendary", "epic", "epic", "legendary"],
        "color_pool": [
            ((238, 118, 85),  (255, 175, 138)),
            ((225, 102, 72),  (248, 158, 118)),
        ],
        "available_cuts": ["brilliant", "cushion", "pear"],
        "optical_effect_pool": {"none": 0.55, "asterism": 0.30, "fluorescence": 0.15},
        "inclusion_pool": {"none": 0.45, "silk": 0.30, "fingerprint": 0.15, "rainbow": 0.10},
        "biome_affinity": [],
    },
    "diamond": {
        "min_depth": 172,
        "crystal_system": "cubic",
        "rarity_pool": ["epic", "legendary", "epic", "legendary"],
        "color_pool": [
            ((240, 245, 252), (200, 220, 245)),
            ((245, 240, 235), (215, 200, 185)),
            ((238, 252, 240), (195, 235, 200)),
        ],
        "available_cuts": ["brilliant", "cushion", "step", "pear"],
        "optical_effect_pool": {"none": 0.55, "fluorescence": 0.45},
        "inclusion_pool": {"none": 0.70, "fingerprint": 0.18, "phantom_crystal": 0.08, "trapped_fluid": 0.04},
        "biome_affinity": ["void"],
    },
    "red_beryl": {
        "min_depth": 190,
        "crystal_system": "hexagonal",
        "rarity_pool": ["legendary", "legendary", "epic", "legendary"],
        "color_pool": [
            ((198, 35,  58),  (245, 88, 108)),
            ((178, 22,  45),  (228, 68,  90)),
        ],
        "available_cuts": ["step", "brilliant", "cushion"],
        "optical_effect_pool": {"none": 0.60, "adularescence": 0.28, "fluorescence": 0.12},
        "inclusion_pool": {"none": 0.30, "garden": 0.35, "fingerprint": 0.25, "rainbow": 0.10},
        "biome_affinity": [],
    },
    "jet": {
        "min_depth": 8,
        "crystal_system": "amorphous",
        "rarity_pool": ["common", "common", "common", "uncommon"],
        "color_pool": [
            ((22, 20, 25),   (52, 48, 58)),
            ((28, 25, 30),   (62, 56, 68)),
        ],
        "available_cuts": ["tumbled", "cabochon"],
        "optical_effect_pool": {"none": 0.85, "fluorescence": 0.15},
        "inclusion_pool": {"none": 0.55, "color_zoning": 0.25, "trapped_fluid": 0.20},
        "biome_affinity": [],
    },
    "obsidian": {
        "min_depth": 10,
        "crystal_system": "amorphous",
        "rarity_pool": ["common", "common", "uncommon", "uncommon"],
        "color_pool": [
            ((28, 25, 32),   (75, 65, 88)),
            ((35, 28, 38),   (85, 72, 95)),
            ((22, 22, 28),   (68, 60, 80)),
        ],
        "available_cuts": ["tumbled", "cabochon"],
        "optical_effect_pool": {"none": 0.68, "adularescence": 0.20, "fluorescence": 0.12},
        "inclusion_pool": {"none": 0.60, "color_zoning": 0.22, "trapped_fluid": 0.12, "rainbow": 0.06},
        "biome_affinity": ["igneous"],
    },
    "rose_quartz": {
        "min_depth": 12,
        "crystal_system": "trigonal",
        "rarity_pool": ["common", "common", "common", "uncommon"],
        "color_pool": [
            ((225, 185, 195), (248, 218, 228)),
            ((215, 172, 185), (242, 208, 218)),
            ((235, 198, 208), (255, 228, 238)),
        ],
        "available_cuts": ["tumbled", "cabochon", "cushion"],
        "optical_effect_pool": {"none": 0.80, "adularescence": 0.12, "asterism": 0.08},
        "inclusion_pool": {"none": 0.55, "color_zoning": 0.28, "rutile_needles": 0.12, "fingerprint": 0.05},
        "biome_affinity": [],
    },
    "amethyst": {
        "min_depth": 18,
        "crystal_system": "trigonal",
        "rarity_pool": ["common", "uncommon", "uncommon", "rare"],
        "color_pool": [
            ((148, 88, 198),  (192, 138, 238)),
            ((128, 72, 178),  (172, 118, 218)),
            ((165, 105, 215), (208, 158, 252)),
        ],
        "available_cuts": ["tumbled", "brilliant", "cushion", "step"],
        "optical_effect_pool": {"none": 0.82, "fluorescence": 0.18},
        "inclusion_pool": {"none": 0.55, "color_zoning": 0.28, "phantom_crystal": 0.12, "fingerprint": 0.05},
        "biome_affinity": [],
    },
    "citrine": {
        "min_depth": 25,
        "crystal_system": "trigonal",
        "rarity_pool": ["common", "uncommon", "uncommon", "rare"],
        "color_pool": [
            ((215, 168, 48),  (252, 208, 92)),
            ((198, 148, 35),  (238, 188, 72)),
            ((232, 185, 62),  (255, 222, 108)),
        ],
        "available_cuts": ["tumbled", "brilliant", "cushion", "step"],
        "optical_effect_pool": {"none": 0.88, "fluorescence": 0.12},
        "inclusion_pool": {"none": 0.52, "color_zoning": 0.28, "phantom_crystal": 0.12, "fingerprint": 0.08},
        "biome_affinity": [],
    },
    "turquoise": {
        "min_depth": 28,
        "crystal_system": "orthorhombic",
        "rarity_pool": ["common", "uncommon", "uncommon", "rare"],
        "color_pool": [
            ((68, 178, 168),  (118, 218, 208)),
            ((52, 158, 148),  (98, 198, 188)),
            ((82, 195, 185),  (135, 232, 222)),
        ],
        "available_cuts": ["tumbled", "cabochon"],
        "optical_effect_pool": {"none": 0.92, "fluorescence": 0.08},
        "inclusion_pool": {"none": 0.42, "garden": 0.32, "color_zoning": 0.18, "fingerprint": 0.08},
        "biome_affinity": [],
    },
    "malachite": {
        "min_depth": 32,
        "crystal_system": "orthorhombic",
        "rarity_pool": ["common", "uncommon", "uncommon", "rare"],
        "color_pool": [
            ((28, 138, 68),   (72, 195, 108)),
            ((22, 118, 55),   (58, 172, 90)),
            ((35, 155, 78),   (85, 215, 125)),
        ],
        "available_cuts": ["tumbled", "cabochon"],
        "optical_effect_pool": {"none": 0.85, "chatoyancy": 0.15},
        "inclusion_pool": {"color_zoning": 0.60, "none": 0.22, "garden": 0.10, "rainbow": 0.08},
        "biome_affinity": [],
    },
    "moonstone": {
        "min_depth": 42,
        "crystal_system": "orthorhombic",
        "rarity_pool": ["uncommon", "uncommon", "rare", "rare"],
        "color_pool": [
            ((215, 225, 238), (185, 205, 228)),
            ((205, 218, 235), (175, 198, 222)),
            ((225, 232, 245), (198, 218, 238)),
        ],
        "available_cuts": ["cabochon", "tumbled"],
        "optical_effect_pool": {"adularescence": 0.75, "none": 0.18, "chatoyancy": 0.07},
        "inclusion_pool": {"none": 0.55, "color_zoning": 0.28, "rainbow": 0.12, "fingerprint": 0.05},
        "biome_affinity": [],
    },
    "labradorite": {
        "min_depth": 48,
        "crystal_system": "orthorhombic",
        "rarity_pool": ["uncommon", "rare", "rare", "epic"],
        "color_pool": [
            ((88, 95, 108),   (148, 168, 195)),
            ((78, 85, 98),    (138, 158, 185)),
            ((98, 105, 118),  (158, 178, 205)),
        ],
        "available_cuts": ["cabochon", "tumbled"],
        "optical_effect_pool": {"adularescence": 0.55, "color_change": 0.30, "none": 0.15},
        "inclusion_pool": {"none": 0.50, "color_zoning": 0.30, "rainbow": 0.15, "phantom_crystal": 0.05},
        "biome_affinity": [],
    },
    "topaz": {
        "min_depth": 55,
        "crystal_system": "orthorhombic",
        "rarity_pool": ["uncommon", "rare", "rare", "epic"],
        "color_pool": [
            ((228, 148, 52),  (255, 195, 95)),
            ((68, 145, 218),  (118, 192, 255)),
            ((215, 148, 185), (252, 195, 225)),
            ((235, 215, 155), (255, 242, 195)),
        ],
        "available_cuts": ["brilliant", "step", "cushion", "pear"],
        "optical_effect_pool": {"none": 0.78, "fluorescence": 0.22},
        "inclusion_pool": {"none": 0.60, "fingerprint": 0.20, "color_zoning": 0.12, "phantom_crystal": 0.08},
        "biome_affinity": [],
    },
    "rhodonite": {
        "min_depth": 58,
        "crystal_system": "orthorhombic",
        "rarity_pool": ["uncommon", "uncommon", "rare", "rare"],
        "color_pool": [
            ((195, 85, 108),  (238, 132, 152)),
            ((178, 72, 95),   (222, 118, 138)),
            ((208, 98, 122),  (248, 148, 168)),
        ],
        "available_cuts": ["tumbled", "cabochon", "cushion"],
        "optical_effect_pool": {"none": 0.92, "chatoyancy": 0.08},
        "inclusion_pool": {"color_zoning": 0.55, "garden": 0.25, "none": 0.12, "fingerprint": 0.08},
        "biome_affinity": [],
    },
    "iolite": {
        "min_depth": 62,
        "crystal_system": "orthorhombic",
        "rarity_pool": ["uncommon", "rare", "rare", "epic"],
        "color_pool": [
            ((88, 92, 188),   (138, 148, 228)),
            ((72, 78, 172),   (122, 132, 212)),
            ((105, 108, 205), (155, 165, 245)),
        ],
        "available_cuts": ["step", "brilliant", "cushion"],
        "optical_effect_pool": {"none": 0.65, "color_change": 0.35},
        "inclusion_pool": {"none": 0.55, "fingerprint": 0.22, "color_zoning": 0.15, "silk": 0.08},
        "biome_affinity": [],
    },
    "opal": {
        "min_depth": 72,
        "crystal_system": "amorphous",
        "rarity_pool": ["rare", "rare", "epic", "epic"],
        "color_pool": [
            ((238, 238, 242), (215, 225, 238)),
            ((38, 38, 42),    (65, 65, 72)),
            ((225, 185, 145), (248, 215, 178)),
        ],
        "available_cuts": ["cabochon", "tumbled"],
        "optical_effect_pool": {"adularescence": 0.70, "color_change": 0.30},
        "inclusion_pool": {"rainbow": 0.60, "none": 0.25, "color_zoning": 0.15},
        "biome_affinity": [],
    },
    "lapis_lazuli": {
        "min_depth": 78,
        "crystal_system": "cubic",
        "rarity_pool": ["uncommon", "rare", "rare", "epic"],
        "color_pool": [
            ((28, 55, 155),   (48, 88, 198)),
            ((22, 45, 138),   (38, 72, 178)),
            ((35, 68, 172),   (58, 105, 215)),
        ],
        "available_cuts": ["tumbled", "cabochon", "step"],
        "optical_effect_pool": {"none": 0.75, "fluorescence": 0.25},
        "inclusion_pool": {"garden": 0.45, "color_zoning": 0.28, "none": 0.18, "fingerprint": 0.09},
        "biome_affinity": [],
    },
    "tanzanite": {
        "min_depth": 105,
        "crystal_system": "orthorhombic",
        "rarity_pool": ["rare", "rare", "epic", "epic"],
        "color_pool": [
            ((88, 72, 195),   (148, 125, 238)),
            ((72, 58, 175),   (132, 108, 218)),
            ((105, 88, 215),  (165, 145, 252)),
        ],
        "available_cuts": ["brilliant", "step", "cushion", "pear"],
        "optical_effect_pool": {"none": 0.55, "color_change": 0.32, "fluorescence": 0.13},
        "inclusion_pool": {"none": 0.55, "fingerprint": 0.22, "color_zoning": 0.15, "silk": 0.08},
        "biome_affinity": [],
    },
    "tsavorite": {
        "min_depth": 112,
        "crystal_system": "cubic",
        "rarity_pool": ["rare", "epic", "rare", "legendary"],
        "color_pool": [
            ((28, 165, 78),   (72, 218, 128)),
            ((22, 148, 65),   (58, 198, 108)),
            ((35, 182, 88),   (85, 232, 145)),
        ],
        "available_cuts": ["brilliant", "cushion", "step"],
        "optical_effect_pool": {"none": 0.82, "fluorescence": 0.18},
        "inclusion_pool": {"none": 0.58, "fingerprint": 0.22, "phantom_crystal": 0.12, "color_zoning": 0.08},
        "biome_affinity": [],
    },
    "kunzite": {
        "min_depth": 118,
        "crystal_system": "orthorhombic",
        "rarity_pool": ["rare", "rare", "epic", "epic"],
        "color_pool": [
            ((215, 148, 198), (252, 192, 238)),
            ((198, 132, 182), (238, 175, 222)),
            ((228, 162, 212), (255, 208, 248)),
        ],
        "available_cuts": ["brilliant", "step", "cushion", "pear"],
        "optical_effect_pool": {"none": 0.55, "fluorescence": 0.32, "color_change": 0.13},
        "inclusion_pool": {"none": 0.62, "fingerprint": 0.22, "color_zoning": 0.16},
        "biome_affinity": [],
    },
    "morganite": {
        "min_depth": 125,
        "crystal_system": "hexagonal",
        "rarity_pool": ["rare", "epic", "epic", "legendary"],
        "color_pool": [
            ((235, 168, 155), (255, 208, 198)),
            ((222, 152, 138), (248, 192, 178)),
            ((248, 185, 172), (255, 222, 212)),
        ],
        "available_cuts": ["brilliant", "step", "cushion", "pear"],
        "optical_effect_pool": {"none": 0.68, "fluorescence": 0.22, "adularescence": 0.10},
        "inclusion_pool": {"none": 0.65, "fingerprint": 0.22, "phantom_crystal": 0.10, "color_zoning": 0.03},
        "biome_affinity": [],
    },
    "zircon": {
        "min_depth": 132,
        "crystal_system": "tetragonal",
        "rarity_pool": ["rare", "epic", "rare", "epic"],
        "color_pool": [
            ((125, 168, 225), (188, 215, 252)),
            ((215, 125, 52),  (252, 175, 95)),
            ((232, 228, 225), (255, 252, 248)),
        ],
        "available_cuts": ["brilliant", "step", "cushion", "pear"],
        "optical_effect_pool": {"none": 0.62, "fluorescence": 0.28, "adularescence": 0.10},
        "inclusion_pool": {"none": 0.62, "fingerprint": 0.22, "phantom_crystal": 0.10, "rainbow": 0.06},
        "biome_affinity": [],
    },
    "sphene": {
        "min_depth": 142,
        "crystal_system": "orthorhombic",
        "rarity_pool": ["rare", "epic", "epic", "legendary"],
        "color_pool": [
            ((195, 185, 45),  (238, 228, 88)),
            ((148, 188, 42),  (195, 232, 88)),
            ((215, 145, 38),  (252, 195, 82)),
        ],
        "available_cuts": ["brilliant", "cushion", "step"],
        "optical_effect_pool": {"none": 0.55, "fluorescence": 0.45},
        "inclusion_pool": {"none": 0.58, "fingerprint": 0.25, "color_zoning": 0.12, "phantom_crystal": 0.05},
        "biome_affinity": [],
    },
    "paraiba": {
        "min_depth": 148,
        "crystal_system": "trigonal",
        "rarity_pool": ["epic", "epic", "legendary", "legendary"],
        "color_pool": [
            ((28, 198, 215),  (88, 245, 242)),
            ((22, 178, 195),  (72, 228, 222)),
            ((35, 215, 232),  (98, 255, 252)),
        ],
        "available_cuts": ["brilliant", "cushion", "pear", "step"],
        "optical_effect_pool": {"none": 0.55, "fluorescence": 0.32, "color_change": 0.13},
        "inclusion_pool": {"none": 0.52, "fingerprint": 0.25, "silk": 0.15, "color_zoning": 0.08},
        "biome_affinity": [],
    },
    "taafeite": {
        "min_depth": 162,
        "crystal_system": "hexagonal",
        "rarity_pool": ["legendary", "epic", "legendary", "legendary"],
        "color_pool": [
            ((195, 128, 178), (238, 172, 218)),
            ((178, 112, 162), (222, 155, 202)),
            ((212, 142, 192), (252, 188, 232)),
        ],
        "available_cuts": ["brilliant", "cushion", "step"],
        "optical_effect_pool": {"none": 0.60, "fluorescence": 0.25, "color_change": 0.15},
        "inclusion_pool": {"none": 0.65, "fingerprint": 0.22, "phantom_crystal": 0.13},
        "biome_affinity": [],
    },
    "grandidierite": {
        "min_depth": 175,
        "crystal_system": "orthorhombic",
        "rarity_pool": ["legendary", "epic", "legendary", "legendary"],
        "color_pool": [
            ((52, 168, 168),  (98, 218, 212)),
            ((42, 152, 152),  (85, 202, 195)),
            ((62, 185, 182),  (112, 232, 228)),
        ],
        "available_cuts": ["step", "cushion", "brilliant"],
        "optical_effect_pool": {"none": 0.50, "color_change": 0.32, "fluorescence": 0.18},
        "inclusion_pool": {"none": 0.58, "fingerprint": 0.22, "silk": 0.12, "color_zoning": 0.08},
        "biome_affinity": [],
    },
    "painite": {
        "min_depth": 183,
        "crystal_system": "hexagonal",
        "rarity_pool": ["legendary", "legendary", "epic", "legendary"],
        "color_pool": [
            ((155, 68, 45),   (208, 112, 80)),
            ((138, 55, 35),   (188, 95, 65)),
            ((172, 82, 55),   (225, 128, 95)),
        ],
        "available_cuts": ["step", "brilliant", "cushion"],
        "optical_effect_pool": {"none": 0.52, "fluorescence": 0.32, "color_change": 0.16},
        "inclusion_pool": {"none": 0.60, "phantom_crystal": 0.22, "fingerprint": 0.12, "color_zoning": 0.06},
        "biome_affinity": [],
    },
    "jeremejevite": {
        "min_depth": 196,
        "crystal_system": "orthorhombic",
        "rarity_pool": ["legendary", "legendary", "legendary", "epic"],
        "color_pool": [
            ((165, 205, 238), (208, 235, 255)),
            ((188, 218, 248), (225, 245, 255)),
            ((215, 228, 242), (242, 248, 255)),
        ],
        "available_cuts": ["brilliant", "step", "cushion"],
        "optical_effect_pool": {"none": 0.55, "fluorescence": 0.30, "chatoyancy": 0.15},
        "inclusion_pool": {"none": 0.62, "fingerprint": 0.22, "phantom_crystal": 0.10, "trapped_fluid": 0.06},
        "biome_affinity": [],
    },
}

GEM_TYPE_ORDER = [
    "amber", "jet", "obsidian", "rose_quartz", "amethyst",
    "garnet", "citrine", "turquoise", "malachite", "spinel",
    "moonstone", "labradorite", "peridot", "topaz", "rhodonite",
    "iolite", "tourmaline", "opal", "lapis_lazuli", "alexandrite",
    "emerald", "tanzanite", "tsavorite", "ruby", "kunzite",
    "morganite", "zircon", "sapphire", "sphene", "paraiba",
    "padparadscha", "taafeite", "diamond", "grandidierite",
    "painite", "red_beryl", "jeremejevite",
]

GEM_SIZES = ["small", "medium", "large", "exceptional"]

RARITY_COLORS = {
    "common":    (150, 148, 145),
    "uncommon":  (80,  175, 90),
    "rare":      (70,  130, 220),
    "epic":      (170, 80,  230),
    "legendary": (230, 160, 40),
}

_CLARITY_POOL_BY_RARITY = {
    "common":    ["I2", "I1", "I1", "SI"],
    "uncommon":  ["I1", "SI", "SI", "VS"],
    "rare":      ["SI", "VS", "VS", "VVS"],
    "epic":      ["VS", "VVS", "VVS", "FL"],
    "legendary": ["VVS", "FL", "VVS", "FL"],
}

_CLARITY_RANK = {"I2": 0, "I1": 1, "SI": 2, "VS": 3, "VVS": 4, "FL": 5}

_GEM_DEPTH_BANDS = [
    (0,   40,  "shallow"),
    (40,  100, "mid"),
    (100, 160, "deep"),
    (160, 999, "abyss"),
]

_GEM_RARITY_WEIGHTS = {
    "shallow": {"common": 6, "uncommon": 3, "rare": 1},
    "mid":     {"common": 3, "uncommon": 4, "rare": 3, "epic": 1},
    "deep":    {"uncommon": 2, "rare": 4, "epic": 3, "legendary": 1},
    "abyss":   {"rare": 2, "epic": 4, "legendary": 4},
}

GEM_TYPE_DESCRIPTIONS = {
    "amber":        "Ancient tree resin, millions of years preserved in stone. May hold trapped time itself.",
    "jet":          "Compressed ancient wood, black as coal but warm to the touch. Polishes to a mirror finish.",
    "obsidian":     "Volcanic glass that fractures to an edge sharper than surgical steel. Some shimmer with hidden rainbows.",
    "rose_quartz":  "The stone of gentle light. Rarely perfect, always beautiful. Some hide a six-rayed star inside.",
    "amethyst":     "Purple quartz prized by royalty for millennia. The deepest specimens rival the finest amethysts of antiquity.",
    "garnet":       "Deep red crystals of almandine, born in metamorphic rock under vast pressure.",
    "citrine":      "Sunny quartz of yellow to amber. Once sold as topaz by unscrupulous traders due to its warmth.",
    "turquoise":    "Formed where copper and phosphate meet. The sky-blue of ancient Egypt, Persia, and the American Southwest.",
    "malachite":    "Vivid green copper carbonate with concentric banding as unique as a fingerprint.",
    "spinel":       "Mistaken for ruby and sapphire for centuries. Comes in fiery reds, purples, and blues.",
    "moonstone":    "A feldspar that billows with adularescence — a glowing light that seems to float within the stone.",
    "labradorite":  "Dark grey rock until the light catches it. Then: an explosion of spectral colour called labradorescence.",
    "peridot":      "Forged in volcanic fire and sometimes fallen from the sky inside meteorites.",
    "topaz":        "Comes in imperial orange, sky blue, champagne, and pink. The finest are 'precious topaz', not mere blue.",
    "rhodonite":    "Rose-pink manganese silicate laced with black veins — the earth's own brushwork.",
    "iolite":       "The 'Viking compass' — its intense pleochroism shifts violet-blue to pale gold as you rotate it.",
    "tourmaline":   "The 'rainbow gem' — a single crystal that shifts from pink to green tip-to-tip.",
    "opal":         "A mosaic of silica spheres that diffracts light into every colour. No two are alike.",
    "lapis_lazuli": "Royal blue with golden pyrite stars. Ground to pigment for paintings for five thousand years.",
    "alexandrite":  "A colour-change miracle: emerald green by daylight, ruby red by lamp. Extraordinarily rare.",
    "emerald":      "The finest green beryl, prized since antiquity. Its garden inclusions are called 'jardin'.",
    "tanzanite":    "Found only near Mount Kilimanjaro. Trichroic: blue, violet, and burgundy depending on the angle.",
    "tsavorite":    "The vivid green garnet from Kenya. More brilliant than emerald and, pound for pound, rarer.",
    "ruby":         "The king of gems. Stars of light sleep inside the finest rubies.",
    "kunzite":      "Pale pink spodumene with an intense violet flash when rotated. Glows under UV light.",
    "morganite":    "Peachy-pink beryl named for financier J.P. Morgan. The warmth of a sunrise, held in the hand.",
    "zircon":       "Not cubic zirconia — a natural gem older than the moon with extraordinary fire and brilliance.",
    "sapphire":     "Corundum in every colour but red. The star sapphire is one of nature's wonders.",
    "sphene":       "Titanite: its dispersion exceeds even diamond, splitting light into spectral fire.",
    "paraiba":      "Copper-bearing tourmaline that glows neon blue-green under any light. Among the most valuable gems per carat.",
    "padparadscha":  "The rarest sapphire: a lotus-blossom pink-orange found in only a handful of places.",
    "taafeite":     "Initially mistaken for spinel, it was identified as a new mineral in 1945. Extraordinarily scarce.",
    "diamond":      "The hardest natural substance. Some glow an eerie blue under certain light.",
    "grandidierite": "A blue-green trichroic gem from Madagascar. Transparent examples are vanishingly rare.",
    "painite":      "Once the rarest mineral on Earth. Only a handful of specimens existed until the early 2000s.",
    "red_beryl":    "Rarer than diamond. Called 'red emerald' by collectors who seek it obsessively.",
    "jeremejevite":  "An aluminium borate of icy blue. Museum-quality specimens are measured in the dozens worldwide.",
}

GEM_CLARITY_DESCS = {
    "FL":  "Flawless — no inclusions visible even under 10x magnification.",
    "VVS": "Very Very Slightly Included — minute inclusions, difficult to see.",
    "VS":  "Very Slightly Included — minor inclusions, not visible to the naked eye.",
    "SI":  "Slightly Included — inclusions visible under magnification.",
    "I1":  "Included — inclusions visible to the naked eye, may affect brilliance.",
    "I2":  "Heavily Included — obvious inclusions that reduce transparency.",
}

GEM_INCLUSION_DESCS = {
    "none":          "Eye-clean — no significant inclusions.",
    "color_zoning":  "Distinct bands of different color saturation within the crystal.",
    "phantom_crystal": "A ghostly earlier growth stage preserved inside, like a gem within a gem.",
    "garden":        "Moss-like inclusions called 'jardin' — the fingerprint of the earth.",
    "rutile_needles": "Fine golden needles that can create a star or cat's eye effect when cut correctly.",
    "silk":          "Fine needles of rutile, classic in ruby and sapphire — the source of star stones.",
    "trapped_fluid": "A microscopic bubble of ancient liquid, sealed inside for eons.",
    "fingerprint":   "Negative crystal inclusions in a fingerprint pattern, frozen in time.",
    "rainbow":       "A thin film that scatters light into spectral colors.",
}

GEM_OPTICAL_DESCS = {
    "none":         "",
    "chatoyancy":   "Cat's Eye — a band of reflected light glides across the dome of a cabochon.",
    "asterism":     "Star Stone — a 6-rayed star of light moves across the gem's surface.",
    "color_change": "Colour Change — green in daylight, red under incandescent light.",
    "fluorescence": "Fluorescence — glows a ghostly colour under certain underground light sources.",
    "adularescence": "Adularescence — a billowing glow moves beneath the surface like moonlight on water.",
}

GEM_CUT_DESCS = {
    "raw":      "Unprocessed — still encased in its host matrix.",
    "tumbled":  "Tumbled — smoothed and polished, no facets. Shows colour beautifully.",
    "cabochon": "Cabochon — a polished dome that reveals chatoyancy and asterism.",
    "brilliant": "Brilliant — round cut with 57 facets, maximises fire and brilliance.",
    "step":     "Step Cut — rectangular facets in parallel steps, emphasises clarity and colour.",
    "cushion":  "Cushion Cut — rounded corners, larger facets, classic antique feel.",
    "pear":     "Pear Cut — a teardrop silhouette combining brilliance and elegance.",
}

# Cuts that activate optical effects
_CUT_ACTIVATES_OPTICAL = {
    "chatoyancy": {"cabochon"},
    "asterism":   {"cabochon"},
    "color_change": {"brilliant", "cushion", "step", "pear"},
    "fluorescence": {"brilliant", "cushion", "step", "cabochon", "pear", "tumbled"},
    "adularescence": {"cabochon", "tumbled"},
}

_FAULT_COUNTS = {
    "common": 3, "uncommon": 3, "rare": 4, "epic": 4, "legendary": 5,
}

# ---------------------------------------------------------------------------
# Surface cache
# ---------------------------------------------------------------------------

_gem_surf_cache: dict = {}


def invalidate_gem_cache(uid):
    keys = [k for k in _gem_surf_cache if isinstance(k, tuple) and k[0] == uid]
    for k in keys:
        del _gem_surf_cache[k]


# ---------------------------------------------------------------------------
# Rendering helpers
# ---------------------------------------------------------------------------

def _clamp_color(c):
    return tuple(max(0, min(255, int(v))) for v in c)


def _lerp_color(a, b, t):
    return _clamp_color((a[0] + (b[0] - a[0]) * t,
                         a[1] + (b[1] - a[1]) * t,
                         a[2] + (b[2] - a[2]) * t))


def _brighten(c, amt):
    return _clamp_color((c[0] + amt, c[1] + amt, c[2] + amt))


def _darken(c, amt):
    return _clamp_color((c[0] - amt, c[1] - amt, c[2] - amt))


def _saturate(c, sat):
    """Scale colour saturation around grey."""
    grey = (c[0] * 0.299 + c[1] * 0.587 + c[2] * 0.114)
    return _clamp_color((grey + (c[0] - grey) * sat,
                         grey + (c[1] - grey) * sat,
                         grey + (c[2] - grey) * sat))


# ---------------------------------------------------------------------------
# Rough gem rendering
# ---------------------------------------------------------------------------

def render_rough_gem(gem, cell_size=48):
    cache_key = ("rough", gem.uid, cell_size)
    if cache_key in _gem_surf_cache:
        return _gem_surf_cache[cache_key]

    rng = random.Random(gem.seed ^ 0xA7B3C1)
    surf = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
    surf.fill((0, 0, 0, 0))

    cx, cy = cell_size // 2, cell_size // 2
    r = cell_size // 2 - 3

    # Matrix (host rock) colour — dull brown-grey
    matrix_col = (92, 82, 72)
    matrix_dark = (68, 60, 52)

    # Build lumpy irregular silhouette
    n_pts = 14
    angles = [i * 2 * math.pi / n_pts for i in range(n_pts)]
    jitter = r * 0.28
    pts = []
    for a in angles:
        dist = r + rng.uniform(-jitter, jitter)
        pts.append((cx + dist * math.cos(a), cy + dist * math.sin(a)))

    # Fill matrix shape
    pygame.draw.polygon(surf, matrix_col + (255,), pts)

    # Darker matrix texture (banding)
    for _ in range(rng.randint(3, 6)):
        px = rng.randint(cx - r + 4, cx + r - 4)
        py = rng.randint(cy - r + 4, cy + r - 4)
        pr = rng.randint(2, max(3, r // 3))
        pygame.draw.circle(surf, matrix_dark + (180,), (px, py), pr)

    # Crystal windows — small bright patches of the actual gem colour peeking through
    pc = gem.primary_color
    sc = gem.secondary_color
    # Desaturate slightly for the rough preview but keep recognisable
    rough_pc = _lerp_color(pc, matrix_col, 0.15)
    rough_sc = _lerp_color(sc, matrix_col, 0.10)

    n_windows = rng.randint(2, 5)
    for _ in range(n_windows):
        angle = rng.uniform(0, 2 * math.pi)
        dist = rng.uniform(r * 0.2, r * 0.72)
        wx = int(cx + dist * math.cos(angle))
        wy = int(cy + dist * math.sin(angle))
        wr = rng.randint(2, max(3, r // 4))
        win_col = rng.choice([rough_pc, rough_sc])
        pygame.draw.circle(surf, win_col + (220,), (wx, wy), wr)
        # Bright tip
        pygame.draw.circle(surf, _brighten(win_col, 40) + (200,), (wx, wy), max(1, wr // 2))

    # Outline
    pygame.draw.polygon(surf, matrix_dark + (255,), pts, 1)

    # "?" overlay on very center — this gem is a mystery
    font_size = max(10, cell_size // 4)
    try:
        font = pygame.font.SysFont("Arial", font_size, bold=True)
        q = font.render("?", True, (200, 190, 170, 200))
        surf.blit(q, (cx - q.get_width() // 2, cy - q.get_height() // 2))
    except Exception:
        pass

    _gem_surf_cache[cache_key] = surf
    return surf


# ---------------------------------------------------------------------------
# Cut gem rendering
# ---------------------------------------------------------------------------

def render_gem(gem, cell_size=48):
    cache_key = ("cut", gem.uid, cell_size)
    if cache_key in _gem_surf_cache:
        return _gem_surf_cache[cache_key]

    rng = random.Random(gem.seed ^ 0x3F9A21)
    surf = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
    surf.fill((0, 0, 0, 0))

    # Apply colour saturation
    pc = _saturate(gem.primary_color, 0.6 + gem.color_saturation * 0.8)
    sc = _saturate(gem.secondary_color, 0.6 + gem.color_saturation * 0.8)

    cut = gem.cut
    cx, cy = cell_size // 2, cell_size // 2
    r = cell_size // 2 - 3

    if cut == "tumbled":
        _render_tumbled(surf, cx, cy, r, pc, sc, rng, gem)
    elif cut == "cabochon":
        _render_cabochon(surf, cx, cy, r, pc, sc, rng, gem)
    elif cut == "brilliant":
        _render_brilliant(surf, cx, cy, r, pc, sc, rng, gem)
    elif cut == "step":
        _render_step(surf, cx, cy, r, pc, sc, rng, gem)
    elif cut == "cushion":
        _render_cushion(surf, cx, cy, r, pc, sc, rng, gem)
    elif cut == "pear":
        _render_pear(surf, cx, cy, r, pc, sc, rng, gem)
    else:
        _render_tumbled(surf, cx, cy, r, pc, sc, rng, gem)

    # Optical effect overlays
    _render_optical_overlay(surf, cx, cy, r, gem, rng)

    _gem_surf_cache[cache_key] = surf
    return surf


def _render_tumbled(surf, cx, cy, r, pc, sc, rng, gem):
    n_pts = 14
    jitter = r * 0.14
    pts = []
    for i in range(n_pts):
        a = i * 2 * math.pi / n_pts
        dist = r + rng.uniform(-jitter, jitter)
        pts.append((cx + dist * math.cos(a), cy + dist * math.sin(a)))

    pygame.draw.polygon(surf, pc + (255,), pts)

    # Subtle secondary colour sheen
    mid = _lerp_color(pc, sc, 0.35)
    sheen_pts = [(cx + (p[0] - cx) * 0.6, cy + (p[1] - cy) * 0.6) for p in pts]
    pygame.draw.polygon(surf, mid + (120,), sheen_pts)

    # Highlight arc
    hl = _brighten(pc, 70)
    pygame.draw.ellipse(surf, hl + (160,),
                        (cx - r // 3, cy - r // 2, r // 2, r // 3))

    pygame.draw.polygon(surf, _darken(pc, 40) + (220,), pts, 1)


def _render_cabochon(surf, cx, cy, r, pc, sc, rng, gem):
    pygame.draw.ellipse(surf, pc + (255,), (cx - r, cy - int(r * 0.72), r * 2, int(r * 1.44)))

    # Dome centre glow
    inner = _brighten(pc, 50)
    pygame.draw.ellipse(surf, inner + (140,),
                        (cx - r // 2, cy - int(r * 0.38), r, int(r * 0.76)))

    # Secondary colour depth shadow at bottom
    shadow = _lerp_color(sc, (0, 0, 0), 0.4)
    pygame.draw.ellipse(surf, shadow + (100,),
                        (cx - r // 2, cy + int(r * 0.12), r, int(r * 0.52)))

    # Highlight
    hl = _brighten(pc, 90)
    pygame.draw.ellipse(surf, hl + (180,),
                        (cx - r // 4, cy - int(r * 0.52), r // 2, int(r * 0.32)))

    pygame.draw.ellipse(surf, _darken(pc, 45) + (220,),
                        (cx - r, cy - int(r * 0.72), r * 2, int(r * 1.44)), 1)


def _render_brilliant(surf, cx, cy, r, pc, sc, rng, gem):
    # Outer circle fill
    pygame.draw.circle(surf, pc + (255,), (cx, cy), r)

    # Table (flat center)
    table_r = int(r * 0.5)
    table_col = _lerp_color(pc, (255, 255, 255), 0.28)
    pygame.draw.circle(surf, table_col + (230,), (cx, cy), table_r)

    # Girdle facets — thin triangular wedges around the circumference
    n_facets = 16
    for i in range(n_facets):
        a0 = i * 2 * math.pi / n_facets
        a1 = (i + 0.5) * 2 * math.pi / n_facets
        a2 = (i + 1) * 2 * math.pi / n_facets
        mid_a = (a0 + a2) / 2
        brightness = int(40 * math.sin(mid_a - math.pi / 4))
        facet_col = _lerp_color(pc, sc, (i % 2) * 0.4)
        facet_col = _brighten(facet_col, brightness)
        tip = (cx + int(table_r * math.cos(a1)), cy + int(table_r * math.sin(a1)))
        rim0 = (cx + int(r * math.cos(a0)), cy + int(r * math.sin(a0)))
        rim2 = (cx + int(r * math.cos(a2)), cy + int(r * math.sin(a2)))
        pygame.draw.polygon(surf, facet_col + (210,), [tip, rim0, rim2])

    # Star facets from table edge
    for i in range(8):
        a = i * math.pi / 4
        x0 = cx + int(table_r * math.cos(a))
        y0 = cy + int(table_r * math.sin(a))
        x1 = cx + int(r * math.cos(a + math.pi / 8))
        y1 = cy + int(r * math.sin(a + math.pi / 8))
        pygame.draw.line(surf, _darken(pc, 30) + (140,), (x0, y0), (x1, y1), 1)

    # Outline
    pygame.draw.circle(surf, _darken(pc, 50) + (220,), (cx, cy), r, 1)

    # Centre sparkle
    sp = _brighten(pc, 100)
    pygame.draw.circle(surf, sp + (255,), (cx, cy), max(2, r // 8))


def _render_step(surf, cx, cy, r, pc, sc, rng, gem):
    # Octagonal step-cut (emerald cut)
    bevel = int(r * 0.28)
    half = r
    # Octagon points (bevelled rectangle)
    pts = [
        (cx - half + bevel, cy - half),
        (cx + half - bevel, cy - half),
        (cx + half, cy - half + bevel),
        (cx + half, cy + half - bevel),
        (cx + half - bevel, cy + half),
        (cx - half + bevel, cy + half),
        (cx - half, cy + half - bevel),
        (cx - half, cy - half + bevel),
    ]
    pygame.draw.polygon(surf, pc + (255,), pts)

    # Step facets — concentric inner rectangles
    for step in range(1, 4):
        factor = 1.0 - step * 0.22
        inner_pts = [
            (cx + (p[0] - cx) * factor, cy + (p[1] - cy) * factor)
            for p in pts
        ]
        step_col = _lerp_color(pc, sc, step * 0.18)
        step_col = _brighten(step_col, 18 - step * 8)
        pygame.draw.polygon(surf, step_col + (180,), inner_pts, 1)

    # Table highlight
    table_pts = [(cx + (p[0] - cx) * 0.45, cy + (p[1] - cy) * 0.45) for p in pts]
    table_col = _lerp_color(pc, (255, 255, 255), 0.32)
    pygame.draw.polygon(surf, table_col + (200,), table_pts)

    # Outline
    pygame.draw.polygon(surf, _darken(pc, 45) + (220,), pts, 1)


def _render_cushion(surf, cx, cy, r, pc, sc, rng, gem):
    # Rounded square with larger facets
    n = 20
    pts = []
    corner_r = int(r * 0.35)
    sq = r - corner_r
    corners = [(-sq, -sq), (sq, -sq), (sq, sq), (-sq, sq)]
    for i, (ox, oy) in enumerate(corners):
        a_start = i * math.pi / 2 + math.pi * 1.25
        for j in range(n // 4 + 1):
            a = a_start + j * (math.pi / 2) / (n // 4)
            pts.append((cx + ox + corner_r * math.cos(a),
                        cy + oy + corner_r * math.sin(a)))

    pygame.draw.polygon(surf, pc + (255,), pts)

    # Main facets — 4 kite shapes pointing inward
    for i in range(4):
        a = i * math.pi / 2 + math.pi / 4
        tip = (cx + int(r * 0.55 * math.cos(a)), cy + int(r * 0.55 * math.sin(a)))
        edge0 = (cx + int(r * math.cos(a - math.pi / 4)),
                 cy + int(r * math.sin(a - math.pi / 4)))
        edge1 = (cx + int(r * math.cos(a + math.pi / 4)),
                 cy + int(r * math.sin(a + math.pi / 4)))
        f_col = _lerp_color(pc, sc, 0.3 + (i % 2) * 0.2)
        f_col = _brighten(f_col, 15 - i * 5)
        pygame.draw.polygon(surf, f_col + (190,), [(cx, cy), tip, edge0])
        pygame.draw.polygon(surf, f_col + (150,), [(cx, cy), tip, edge1])

    # Table
    table_r = int(r * 0.42)
    table_col = _lerp_color(pc, (255, 255, 255), 0.30)
    pygame.draw.circle(surf, table_col + (190,), (cx, cy), table_r)

    pygame.draw.polygon(surf, _darken(pc, 40) + (210,), pts, 1)


def _render_pear(surf, cx, cy, r, pc, sc, rng, gem):
    # Teardrop / pear shape
    n = 40
    pts = []
    for i in range(n):
        t = i / n
        a = t * 2 * math.pi - math.pi / 2
        if a < math.pi / 2:
            # Top rounded lobe
            dist = r * 0.62
        else:
            # Bottom pointed end
            progress = (a - math.pi / 2) / math.pi
            dist = r * (0.62 + progress * 0.48)
        pts.append((cx + dist * math.cos(a), cy + dist * math.sin(a)))

    # Better pear: ellipse top + triangle point at bottom
    top_pts = []
    n_top = 24
    for i in range(n_top):
        a = i * math.pi / (n_top - 1) - math.pi
        x = cx + r * 0.72 * math.cos(a)
        y = cy - int(r * 0.18) + int(r * 0.78) * math.sin(a)
        top_pts.append((x, y))
    tip = (cx, cy + int(r * 0.88))
    pts = top_pts + [tip]

    pygame.draw.polygon(surf, pc + (255,), pts)

    # Facets
    n_f = 8
    for i in range(n_f):
        t = i / n_f
        a = t * math.pi * 2 - math.pi / 2
        fx = cx + int(r * 0.5 * math.cos(a))
        fy = cy - int(r * 0.18) + int(r * 0.45 * math.sin(a))
        pygame.draw.line(surf, _lerp_color(pc, sc, 0.3) + (140,),
                         (cx, cy - int(r * 0.18)), (fx, fy), 1)

    # Highlight
    hl = _brighten(pc, 80)
    pygame.draw.ellipse(surf, hl + (160,),
                        (cx - r // 4, cy - int(r * 0.6), r // 2, int(r * 0.32)))

    pygame.draw.polygon(surf, _darken(pc, 40) + (210,), pts, 1)


def _render_optical_overlay(surf, cx, cy, r, gem, rng):
    effect = gem.optical_effect
    cut = gem.cut

    # Only show the effect if the right cut was chosen
    if effect in _CUT_ACTIVATES_OPTICAL:
        if cut not in _CUT_ACTIVATES_OPTICAL[effect]:
            return

    if effect == "asterism":
        # 6-ray star from centre
        star_col = (255, 255, 220, 200)
        for i in range(6):
            a = i * math.pi / 3
            x1 = cx + int(r * 0.88 * math.cos(a))
            y1 = cy + int(r * 0.88 * math.sin(a))
            pygame.draw.line(surf, star_col, (cx, cy), (x1, y1), 2)
            # Glow
            pygame.draw.line(surf, (255, 255, 200, 80), (cx, cy), (x1, y1), 4)

    elif effect == "chatoyancy":
        # Horizontal band of light
        band_y = cy
        band_w = int(r * 1.85)
        band_h = max(2, r // 5)
        eye = pygame.Surface((band_w, band_h * 3), pygame.SRCALPHA)
        for dy in range(-band_h, band_h + 1):
            alpha = int(160 * (1 - abs(dy) / (band_h + 1)))
            pygame.draw.line(eye, (255, 255, 200, alpha),
                             (0, band_h + dy), (band_w, band_h + dy), 1)
        surf.blit(eye, (cx - band_w // 2, band_y - band_h))

    elif effect == "color_change":
        # Split color hint: left half gets secondary colour tint
        overlay = pygame.Surface((r, r * 2), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 0))
        sc_tint = gem.secondary_color + (55,)
        overlay.fill(sc_tint)
        surf.blit(overlay, (cx - r, cy - r))

    elif effect == "fluorescence":
        # Inner glow ring
        glow_col = _brighten(gem.primary_color, 60) + (60,)
        for gr in range(r // 3, r - 2, 2):
            pygame.draw.circle(surf, glow_col, (cx, cy), gr, 1)

    elif effect == "adularescence":
        # Billowing glow (static: soft central bloom)
        for gr in range(r // 4, r, 3):
            alpha = int(80 * (1 - gr / r))
            col = _brighten(gem.primary_color, 60) + (alpha,)
            pygame.draw.circle(surf, col, (cx, cy - r // 6), gr, 2)


# ---------------------------------------------------------------------------
# Codex preview rendering (no specific gem instance)
# ---------------------------------------------------------------------------

def render_gem_codex_preview(type_key, cell_size=48):
    cache_key = ("codex", type_key, cell_size)
    if cache_key in _gem_surf_cache:
        return _gem_surf_cache[cache_key]

    tdef = GEM_TYPES[type_key]
    rng = random.Random(hash(type_key) & 0xFFFFFFFF)
    colors = rng.choice(tdef["color_pool"])
    pc, sc = colors[0], colors[1]
    pc = _saturate(pc, 1.1)

    surf = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
    surf.fill((0, 0, 0, 0))

    cx, cy = cell_size // 2, cell_size // 2
    r = cell_size // 2 - 3

    # Render a representative cut
    cut = tdef["available_cuts"][0]
    dummy_gem = type("DummyGem", (), {
        "primary_color": pc, "secondary_color": sc,
        "color_saturation": 0.85, "optical_effect": "none",
        "cut": cut,
    })()

    if cut == "brilliant":
        _render_brilliant(surf, cx, cy, r, pc, sc, rng, dummy_gem)
    elif cut == "step":
        _render_step(surf, cx, cy, r, pc, sc, rng, dummy_gem)
    elif cut == "cabochon":
        _render_cabochon(surf, cx, cy, r, pc, sc, rng, dummy_gem)
    elif cut == "cushion":
        _render_cushion(surf, cx, cy, r, pc, sc, rng, dummy_gem)
    elif cut == "pear":
        _render_pear(surf, cx, cy, r, pc, sc, rng, dummy_gem)
    else:
        _render_tumbled(surf, cx, cy, r, pc, sc, rng, dummy_gem)

    # Silhouette if not yet discovered — handled by caller
    _gem_surf_cache[cache_key] = surf
    return surf


# ---------------------------------------------------------------------------
# Fault-line generation for the cracking mini-game
# ---------------------------------------------------------------------------

def get_fault_points(gem, area_size=160):
    """Return deterministic list of (x, y) fault points for the gem's mini-game."""
    rng = random.Random(gem.seed ^ 0xFA1708)
    n = _FAULT_COUNTS[gem.rarity]
    cx, cy = area_size // 2, area_size // 2
    margin = int(area_size * 0.22)
    pts = []
    for i in range(n):
        angle = i * 2 * math.pi / n + rng.uniform(-0.4, 0.4)
        dist = rng.uniform(area_size * 0.18, area_size * 0.38)
        x = int(cx + dist * math.cos(angle))
        y = int(cy + dist * math.sin(angle))
        x = max(margin, min(area_size - margin, x))
        y = max(margin, min(area_size - margin, y))
        pts.append((x, y))
    return pts


# ---------------------------------------------------------------------------
# Clarity after mini-game
# ---------------------------------------------------------------------------

def apply_cracking_result(gem, mistakes):
    """Lower clarity grade based on mistake count. Mutates gem in-place."""
    grades = ["I2", "I1", "SI", "VS", "VVS", "FL"]
    cur = grades.index(gem.clarity) if gem.clarity in grades else 2
    cur = max(0, cur - mistakes)
    gem.clarity = grades[cur]


def resolve_optical_effect(gem):
    """Return True if the chosen cut activates the gem's optical effect."""
    if gem.optical_effect == "none":
        return False
    needed = _CUT_ACTIVATES_OPTICAL.get(gem.optical_effect, set())
    return gem.cut in needed


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------

class GemGenerator:
    def __init__(self, world_seed):
        self._world_seed = world_seed

    def generate(self, bx, by, depth, biome=None):
        gem_seed = hash((self._world_seed, bx, by, 0x6E534F1)) & 0xFFFFFFFF
        rng = random.Random(gem_seed)

        # Depth band → rarity
        band = "shallow"
        for lo, hi, name in _GEM_DEPTH_BANDS:
            if lo <= depth < hi:
                band = name
                break

        weights = _GEM_RARITY_WEIGHTS[band]
        rarity = random.Random(gem_seed ^ 0x1234).choices(
            list(weights.keys()), weights=list(weights.values())
        )[0]

        # Eligible gem types for depth + biome
        eligible = [
            t for t, d in GEM_TYPES.items()
            if d["min_depth"] <= depth
        ]
        if not eligible:
            eligible = ["amber"]

        # Prefer types matching rarity and biome
        preferred = [t for t in eligible if rarity in GEM_TYPES[t]["rarity_pool"]]
        if biome:
            biome_pref = [t for t in preferred
                          if not GEM_TYPES[t]["biome_affinity"] or biome.lower() in GEM_TYPES[t]["biome_affinity"]]
            if biome_pref:
                preferred = biome_pref

        type_pool = preferred if preferred else eligible
        gem_type = rng.choice(type_pool)
        tdef = GEM_TYPES[gem_type]

        colors = rng.choice(tdef["color_pool"])
        pc, sc = colors[0], colors[1]

        size = rng.choice(GEM_SIZES)
        clarity = rng.choice(_CLARITY_POOL_BY_RARITY[rarity])

        color_saturation = round(rng.uniform(0.55, 1.0), 2)

        # Optical effect (hidden until cracked)
        opt_pool = tdef["optical_effect_pool"]
        optical_effect = rng.choices(list(opt_pool.keys()), weights=list(opt_pool.values()))[0]

        # Inclusion (hidden until cracked)
        inc_pool = tdef["inclusion_pool"]
        inclusion = rng.choices(list(inc_pool.keys()), weights=list(inc_pool.values()))[0]

        # If inclusion is silk/rutile and no asterism optical, give a chance to upgrade
        if inclusion in ("silk", "rutile_needles") and optical_effect == "none":
            if gem_type in ("ruby", "sapphire", "padparadscha", "garnet"):
                if rng.random() < 0.45:
                    optical_effect = "asterism"
            elif gem_type == "tourmaline":
                if rng.random() < 0.35:
                    optical_effect = "chatoyancy"

        uid = f"gem_{gem_seed:08x}_{bx}_{by}"

        return Gemstone(
            uid=uid,
            gem_type=gem_type,
            rarity=rarity,
            size=size,
            state="rough",
            cut="raw",
            clarity=clarity,
            color_saturation=color_saturation,
            optical_effect=optical_effect,
            inclusion=inclusion,
            crystal_system=tdef["crystal_system"],
            primary_color=pc,
            secondary_color=sc,
            depth_found=depth,
            seed=gem_seed,
            biome=biome or "",
        )
