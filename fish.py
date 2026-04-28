import math
import random
import pygame
from dataclasses import dataclass


@dataclass
class Fish:
    uid: str
    species: str
    rarity: str
    weight_kg: float
    length_cm: int
    pattern: str
    primary_color: tuple
    secondary_color: tuple
    habitat: str
    biome_found: str
    seed: int
    ocean_zone: str = ""


# ---------------------------------------------------------------------------
# Fish type definitions
# biome_affinity: list of biodomes where this fish can appear.
#   Empty list means the fish can appear in ANY fishing biome.
# Fishing biomes (those with surface water): temperate, boreal, birch_forest,
#   wetland, swamp, rolling_hills, jungle, tundra, tropical.
# ---------------------------------------------------------------------------

FISH_TYPES = {

    # ------------------------------------------------------------------
    # Universal
    # ------------------------------------------------------------------
    "minnow": {
        "name": "Minnow",
        "rarity_pool": ["common", "common", "common", "uncommon"],
        "habitat": "river",
        "biome_affinity": [],   # any biome
        "weight_range": (0.03, 0.25),
        "length_range": (4, 12),
        "pattern_pool": ["striped", "plain", "spotted"],
        "colors": [
            ((160, 190, 210), (110, 145, 175)),
            ((175, 205, 185), (130, 160, 140)),
        ],
        "description": "A tiny freshwater fish. Found almost everywhere there is clean water.",
        "tension": 0.4,
    },

    # ------------------------------------------------------------------
    # Temperate (temperate, rolling_hills, birch_forest)
    # ------------------------------------------------------------------
    "perch": {
        "name": "Perch",
        "rarity_pool": ["common", "common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "birch_forest", "boreal"],
        "weight_range": (0.20, 1.50),
        "length_range": (15, 30),
        "pattern_pool": ["striped", "banded"],
        "colors": [
            ((200, 165, 80), (70, 125, 55)),
            ((215, 180, 90), (60, 110, 45)),
        ],
        "description": "A spiny-finned lake fish with vivid green and gold stripes.",
    },
    "bass": {
        "name": "Bass",
        "rarity_pool": ["common", "uncommon", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "birch_forest"],
        "weight_range": (0.50, 4.00),
        "length_range": (25, 55),
        "pattern_pool": ["plain", "mottled"],
        "colors": [
            ((95, 140, 75), (55, 95, 45)),
            ((110, 155, 90), (65, 105, 55)),
        ],
        "description": "A bold and scrappy lake predator. Puts up a strong fight.",
        "tension": 1.8,
    },
    "carp": {
        "name": "Carp",
        "rarity_pool": ["uncommon", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "birch_forest", "wetland"],
        "weight_range": (1.00, 10.00),
        "length_range": (30, 80),
        "pattern_pool": ["plain", "scaled"],
        "colors": [
            ((180, 140, 80), (130, 100, 55)),
            ((195, 155, 90), (145, 112, 65)),
        ],
        "description": "A large, hardy lake fish. Wary and difficult to fool.",
        "tension": 1.4,
    },
    "bluegill": {
        "name": "Bluegill",
        "rarity_pool": ["uncommon", "uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "birch_forest"],
        "weight_range": (0.10, 0.80),
        "length_range": (10, 25),
        "pattern_pool": ["banded", "striped"],
        "colors": [
            ((75, 125, 200), (165, 125, 50)),
            ((65, 115, 190), (150, 115, 45)),
        ],
        "description": "A small sunfish with brilliant blue cheek markings.",
    },
    "walleye": {
        "name": "Walleye",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "birch_forest", "boreal"],
        "weight_range": (0.50, 5.00),
        "length_range": (30, 65),
        "pattern_pool": ["mottled", "striped"],
        "colors": [
            ((205, 180, 105), (100, 90, 65)),
            ((190, 165, 95), (90, 80, 58)),
        ],
        "description": "A prized lake fish with glassy, light-reflecting eyes.",
    },
    "golden_koi": {
        "name": "Golden Koi",
        "rarity_pool": ["legendary"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "birch_forest", "rolling_hills"],
        "weight_range": (1.00, 8.00),
        "length_range": (30, 70),
        "pattern_pool": ["scaled", "spotted"],
        "colors": [
            ((255, 210, 40), (255, 140, 20)),
            ((245, 200, 30), (240, 125, 15)),
        ],
        "description": "A legendary ornamental fish of mythical beauty. Said to bring fortune.",
    },
    "crappie": {
        "name": "Crappie",
        "rarity_pool": ["common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "birch_forest"],
        "weight_range": (0.15, 1.00),
        "length_range": (12, 28),
        "pattern_pool": ["spotted", "mottled"],
        "colors": [
            ((180, 180, 180), (45, 50, 55)),
            ((165, 170, 175), (38, 42, 48)),
        ],
        "description": "A popular panfish with bold black speckles on a silver body.",
    },
    "sunfish": {
        "name": "Sunfish",
        "rarity_pool": ["common", "common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "birch_forest", "wetland"],
        "weight_range": (0.05, 0.60),
        "length_range": (8, 22),
        "pattern_pool": ["plain", "spotted"],
        "colors": [
            ((220, 130, 50), (60, 110, 185)),
            ((210, 120, 42), (50, 100, 170)),
        ],
        "description": "A brilliantly colored little lake fish. Feisty on the hook.",
    },
    "channel_catfish": {
        "name": "Channel Catfish",
        "rarity_pool": ["uncommon", "uncommon", "rare"],
        "habitat": "river",
        "biome_affinity": ["temperate", "rolling_hills", "wetland"],
        "weight_range": (0.80, 7.00),
        "length_range": (30, 75),
        "pattern_pool": ["plain", "spotted"],
        "colors": [
            ((100, 110, 130), (65, 72, 88)),
            ((90, 100, 120), (58, 65, 80)),
        ],
        "description": "A river-dwelling catfish with a forked tail. Common in warm rivers.",
    },
    "smallmouth_bass": {
        "name": "Smallmouth Bass",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "birch_forest", "rolling_hills"],
        "weight_range": (0.40, 3.50),
        "length_range": (20, 50),
        "pattern_pool": ["striped", "mottled"],
        "colors": [
            ((175, 140, 70), (90, 120, 55)),
            ((160, 128, 60), (80, 110, 48)),
        ],
        "description": "A bronze-colored bass that prefers clear, rocky lakes and streams.",
    },
    "yellow_perch": {
        "name": "Yellow Perch",
        "rarity_pool": ["common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "birch_forest", "boreal"],
        "weight_range": (0.15, 1.20),
        "length_range": (14, 32),
        "pattern_pool": ["striped", "banded"],
        "colors": [
            ((220, 195, 60), (42, 42, 46)),
            ((205, 180, 52), (36, 36, 40)),
        ],
        "description": "A vibrant yellow fish with bold dark vertical bars.",
    },
    "muskie": {
        "name": "Muskie",
        "rarity_pool": ["rare", "epic"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "birch_forest", "boreal"],
        "weight_range": (2.00, 18.00),
        "length_range": (55, 140),
        "pattern_pool": ["mottled", "striped"],
        "colors": [
            ((120, 145, 65), (200, 180, 90)),
            ((110, 135, 58), (185, 165, 80)),
        ],
        "description": "The muskellunge — a fearsome apex predator of northern lakes.",
    },
    "roach": {
        "name": "Roach",
        "rarity_pool": ["common", "common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "boreal", "birch_forest", "wetland"],
        "weight_range": (0.10, 1.00),
        "length_range": (10, 25),
        "pattern_pool": ["plain", "scaled"],
        "colors": [
            ((185, 190, 200), (200, 80, 60)),
            ((175, 180, 192), (185, 72, 52)),
        ],
        "description": "A widespread silver fish with striking red fins.",
    },
    "rudd": {
        "name": "Rudd",
        "rarity_pool": ["common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "wetland", "rolling_hills"],
        "weight_range": (0.15, 1.20),
        "length_range": (12, 28),
        "pattern_pool": ["plain", "striped"],
        "colors": [
            ((195, 165, 80), (200, 82, 52)),
            ((182, 152, 72), (185, 74, 46)),
        ],
        "description": "A golden-flanked lake fish with vivid orange-red fins.",
    },
    "tench": {
        "name": "Tench",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "wetland", "swamp", "rolling_hills"],
        "weight_range": (0.50, 4.00),
        "length_range": (25, 55),
        "pattern_pool": ["plain", "mottled"],
        "colors": [
            ((70, 90, 55), (150, 135, 60)),
            ((62, 82, 48), (138, 124, 52)),
        ],
        "description": "A deep-bodied, olive-green fish known as the 'doctor fish' of ponds.",
    },

    # ------------------------------------------------------------------
    # Cold biomes (boreal, tundra)
    # ------------------------------------------------------------------
    "trout": {
        "name": "Trout",
        "rarity_pool": ["uncommon", "uncommon", "rare"],
        "habitat": "river",
        "biome_affinity": ["boreal", "tundra"],
        "weight_range": (0.30, 3.00),
        "length_range": (20, 60),
        "pattern_pool": ["spotted", "striped"],
        "colors": [
            ((160, 100, 80), (220, 185, 105)),
            ((140, 90, 70), (200, 165, 90)),
        ],
        "description": "An agile river fish prized for its spotted markings and flavor.",
        "tension": 1.2,
    },
    "salmon": {
        "name": "Salmon",
        "rarity_pool": ["rare", "rare", "epic"],
        "habitat": "river",
        "biome_affinity": ["boreal", "tundra"],
        "weight_range": (2.00, 12.00),
        "length_range": (50, 100),
        "pattern_pool": ["spotted", "plain"],
        "colors": [
            ((230, 120, 80), (160, 100, 70)),
            ((220, 110, 70), (150, 90, 60)),
        ],
        "description": "A powerful migratory river fish with striking pink flesh.",
        "tension": 1.6,
    },
    "pike": {
        "name": "Pike",
        "rarity_pool": ["rare", "epic"],
        "habitat": "lake",
        "biome_affinity": ["boreal", "tundra", "temperate", "rolling_hills"],
        "weight_range": (1.00, 15.00),
        "length_range": (40, 130),
        "pattern_pool": ["mottled", "spotted"],
        "colors": [
            ((75, 125, 65), (185, 170, 85)),
            ((65, 115, 55), (170, 155, 75)),
        ],
        "description": "A fierce lake ambush predator with excellent camouflage.",
        "tension": 2.2,
    },
    "sturgeon": {
        "name": "Sturgeon",
        "rarity_pool": ["epic", "epic", "legendary"],
        "habitat": "river",
        "biome_affinity": ["boreal", "temperate", "rolling_hills"],
        "weight_range": (5.00, 50.00),
        "length_range": (80, 200),
        "pattern_pool": ["plated", "plain"],
        "colors": [
            ((80, 80, 92), (50, 50, 62)),
            ((92, 90, 105), (60, 58, 72)),
        ],
        "description": "An ancient armored river giant. Extremely rare and massive.",
    },
    "arctic_char": {
        "name": "Arctic Char",
        "rarity_pool": ["uncommon", "uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["boreal", "tundra"],
        "weight_range": (0.30, 4.50),
        "length_range": (25, 65),
        "pattern_pool": ["spotted", "plain"],
        "colors": [
            ((230, 110, 60), (180, 195, 212)),
            ((215, 100, 52), (165, 180, 198)),
        ],
        "description": "A cold-water char with brilliant orange flanks and silver back.",
    },
    "lake_whitefish": {
        "name": "Lake Whitefish",
        "rarity_pool": ["common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["boreal", "tundra"],
        "weight_range": (0.50, 4.00),
        "length_range": (28, 55),
        "pattern_pool": ["plain", "scaled"],
        "colors": [
            ((200, 205, 210), (150, 158, 165)),
            ((190, 196, 202), (140, 148, 156)),
        ],
        "description": "A deep-water cold lake fish with delicate silver scales.",
    },
    "burbot": {
        "name": "Burbot",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["boreal", "tundra"],
        "weight_range": (0.40, 5.00),
        "length_range": (30, 80),
        "pattern_pool": ["mottled", "spotted"],
        "colors": [
            ((110, 90, 60), (75, 60, 40)),
            ((120, 100, 70), (82, 68, 46)),
        ],
        "description": "An eel-like cod relative. The only freshwater member of the cod family.",
    },
    "brook_trout": {
        "name": "Brook Trout",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "river",
        "biome_affinity": ["boreal", "birch_forest"],
        "weight_range": (0.10, 2.50),
        "length_range": (15, 50),
        "pattern_pool": ["spotted", "striped"],
        "colors": [
            ((80, 100, 60), (220, 120, 50)),
            ((70, 90, 52), (205, 110, 45)),
        ],
        "description": "A spectacularly patterned cold stream trout with red-and-blue spots.",
    },
    "steelhead": {
        "name": "Steelhead",
        "rarity_pool": ["rare", "epic"],
        "habitat": "river",
        "biome_affinity": ["boreal", "tundra"],
        "weight_range": (2.00, 10.00),
        "length_range": (50, 100),
        "pattern_pool": ["spotted", "plain"],
        "colors": [
            ((190, 200, 215), (215, 120, 110)),
            ((175, 185, 200), (200, 110, 100)),
        ],
        "description": "The sea-run rainbow trout. Chrome bright and ferociously strong.",
        "tension": 2.0,
    },

    # ------------------------------------------------------------------
    # Jungle / Tropical (jungle, tropical)
    # ------------------------------------------------------------------
    "piranha": {
        "name": "Piranha",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "river",
        "biome_affinity": ["jungle", "tropical"],
        "weight_range": (0.20, 1.50),
        "length_range": (15, 35),
        "pattern_pool": ["plain", "spotted"],
        "colors": [
            ((170, 175, 175), (200, 60, 55)),
            ((155, 160, 160), (185, 52, 48)),
        ],
        "description": "A razor-toothed jungle fish. Dangerous in groups. Beautiful up close.",
    },
    "arapaima": {
        "name": "Arapaima",
        "rarity_pool": ["epic", "legendary"],
        "habitat": "river",
        "biome_affinity": ["jungle", "tropical"],
        "weight_range": (20.00, 120.00),
        "length_range": (100, 250),
        "pattern_pool": ["scaled", "plated"],
        "colors": [
            ((55, 90, 60), (180, 150, 50)),
            ((48, 80, 52), (165, 138, 44)),
        ],
        "description": "One of the largest freshwater fish in the world. Ancient and breathtaking.",
    },
    "electric_eel": {
        "name": "Electric Eel",
        "rarity_pool": ["rare", "epic"],
        "habitat": "river",
        "biome_affinity": ["jungle", "wetland"],
        "weight_range": (1.50, 10.00),
        "length_range": (80, 180),
        "pattern_pool": ["striped", "plain"],
        "colors": [
            ((55, 50, 35), (190, 175, 30)),
            ((48, 44, 30), (175, 160, 25)),
        ],
        "description": "Generates up to 600 volts. Handle with extreme caution.",
    },
    "tilapia": {
        "name": "Tilapia",
        "rarity_pool": ["common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["tropical", "jungle"],
        "weight_range": (0.30, 3.00),
        "length_range": (18, 40),
        "pattern_pool": ["striped", "plain"],
        "colors": [
            ((150, 155, 165), (100, 110, 125)),
            ((140, 145, 156), (92, 102, 116)),
        ],
        "description": "A hardy tropical lake fish. Thrives in warm, shallow waters.",
    },
    "cichlid": {
        "name": "Cichlid",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["tropical", "jungle"],
        "weight_range": (0.15, 1.80),
        "length_range": (12, 35),
        "pattern_pool": ["banded", "striped"],
        "colors": [
            ((50, 120, 220), (220, 100, 40)),
            ((42, 110, 205), (205, 90, 35)),
        ],
        "description": "A brilliantly colored tropical fish. Males display vivid breeding colors.",
    },
    "tambaqui": {
        "name": "Tambaqui",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "river",
        "biome_affinity": ["jungle", "tropical"],
        "weight_range": (1.00, 14.00),
        "length_range": (40, 90),
        "pattern_pool": ["plain", "mottled"],
        "colors": [
            ((60, 60, 50), (180, 80, 60)),
            ((52, 52, 44), (165, 72, 52)),
        ],
        "description": "A large fruit-eating river fish of the deep jungle. Has powerful jaw teeth.",
    },
    "catfish": {
        "name": "Catfish",
        "rarity_pool": ["common", "uncommon"],
        "habitat": "river",
        "biome_affinity": ["wetland", "swamp", "jungle", "tropical"],
        "weight_range": (1.00, 8.00),
        "length_range": (30, 70),
        "pattern_pool": ["plain", "mottled"],
        "colors": [
            ((90, 80, 70), (55, 50, 45)),
            ((110, 95, 80), (70, 60, 55)),
        ],
        "description": "A whiskered bottom-dweller of muddy rivers and warm swamps.",
    },

    # ------------------------------------------------------------------
    # Wetland / Swamp (wetland, swamp)
    # ------------------------------------------------------------------
    "gar": {
        "name": "Gar",
        "rarity_pool": ["rare", "epic"],
        "habitat": "river",
        "biome_affinity": ["wetland", "swamp"],
        "weight_range": (1.00, 10.00),
        "length_range": (55, 150),
        "pattern_pool": ["striped", "mottled"],
        "colors": [
            ((120, 140, 80), (185, 195, 180)),
            ((110, 128, 72), (170, 180, 165)),
        ],
        "description": "An armored living fossil with a long, needle-like snout.",
    },
    "bowfin": {
        "name": "Bowfin",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["wetland", "swamp"],
        "weight_range": (0.50, 4.50),
        "length_range": (35, 70),
        "pattern_pool": ["mottled", "striped"],
        "colors": [
            ((65, 75, 45), (160, 155, 60)),
            ((58, 68, 40), (148, 142, 52)),
        ],
        "description": "A primitive, air-breathing fish that thrives in stagnant swamps.",
    },
    "mudskipper": {
        "name": "Mudskipper",
        "rarity_pool": ["common", "uncommon"],
        "habitat": "river",
        "biome_affinity": ["wetland", "swamp"],
        "weight_range": (0.05, 0.40),
        "length_range": (8, 25),
        "pattern_pool": ["spotted", "mottled"],
        "colors": [
            ((130, 115, 90), (90, 85, 70)),
            ((120, 106, 82), (82, 78, 62)),
        ],
        "description": "An amphibious fish that can walk on land using its fins.",
    },
    "snakehead": {
        "name": "Snakehead",
        "rarity_pool": ["rare", "epic"],
        "habitat": "river",
        "biome_affinity": ["wetland", "swamp", "jungle"],
        "weight_range": (0.50, 6.00),
        "length_range": (35, 85),
        "pattern_pool": ["mottled", "spotted"],
        "colors": [
            ((60, 70, 55), (110, 115, 85)),
            ((52, 62, 48), (100, 106, 78)),
        ],
        "description": "A fierce air-breathing predator. Can survive out of water for days.",
        "tension": 2.1,
    },
    "alligator_gar": {
        "name": "Alligator Gar",
        "rarity_pool": ["epic", "legendary"],
        "habitat": "river",
        "biome_affinity": ["wetland", "swamp"],
        "weight_range": (15.00, 80.00),
        "length_range": (120, 300),
        "pattern_pool": ["plated", "mottled"],
        "colors": [
            ((95, 100, 60), (140, 125, 75)),
            ((88, 92, 54), (128, 116, 68)),
        ],
        "description": "A massive armored predator. One of the largest freshwater fish in North America.",
    },

    # ------------------------------------------------------------------
    # Universal (additional)
    # ------------------------------------------------------------------
    "dace": {
        "name": "Dace",
        "rarity_pool": ["common", "common", "uncommon"],
        "habitat": "river",
        "biome_affinity": [],
        "weight_range": (0.02, 0.18),
        "length_range": (4, 14),
        "pattern_pool": ["plain", "striped", "spotted"],
        "colors": [
            ((195, 205, 215), (140, 155, 170)),
            ((185, 195, 205), (130, 145, 160)),
        ],
        "description": "A small, darting silver fish found in almost any clean stream.",
    },
    "stone_loach": {
        "name": "Stone Loach",
        "rarity_pool": ["common", "uncommon"],
        "habitat": "river",
        "biome_affinity": [],
        "weight_range": (0.01, 0.10),
        "length_range": (5, 14),
        "pattern_pool": ["mottled", "spotted"],
        "colors": [
            ((120, 100, 70), (80, 65, 45)),
            ((130, 110, 78), (88, 72, 50)),
        ],
        "description": "A whisker-bearing bottom-dweller that hides beneath pebbles in fast currents.",
    },

    # ------------------------------------------------------------------
    # Temperate (additional)
    # ------------------------------------------------------------------
    "brown_trout": {
        "name": "Brown Trout",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "river",
        "biome_affinity": ["temperate", "birch_forest", "boreal"],
        "weight_range": (0.30, 5.00),
        "length_range": (22, 70),
        "pattern_pool": ["spotted", "mottled"],
        "colors": [
            ((185, 145, 75), (200, 80, 40)),
            ((170, 132, 65), (185, 72, 35)),
        ],
        "description": "A wily river trout with vivid red and black spots on golden flanks.",
    },
    "chub": {
        "name": "Chub",
        "rarity_pool": ["common", "uncommon"],
        "habitat": "river",
        "biome_affinity": ["temperate", "rolling_hills", "birch_forest"],
        "weight_range": (0.10, 2.00),
        "length_range": (12, 40),
        "pattern_pool": ["plain", "scaled"],
        "colors": [
            ((140, 155, 120), (195, 185, 160)),
            ((128, 142, 110), (180, 170, 148)),
        ],
        "description": "A chunky olive-silver river fish with a large head and wide mouth.",
    },
    "bream": {
        "name": "Bream",
        "rarity_pool": ["common", "common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "wetland"],
        "weight_range": (0.20, 4.00),
        "length_range": (18, 55),
        "pattern_pool": ["plain", "scaled"],
        "colors": [
            ((200, 195, 170), (120, 140, 80)),
            ((188, 182, 158), (110, 128, 72)),
        ],
        "description": "A deep-bodied bronze-silver lake fish. Patient anglers are often rewarded.",
    },
    "pumpkinseed": {
        "name": "Pumpkinseed",
        "rarity_pool": ["uncommon", "uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "birch_forest"],
        "weight_range": (0.05, 0.50),
        "length_range": (8, 22),
        "pattern_pool": ["spotted", "banded"],
        "colors": [
            ((220, 140, 50), (50, 160, 200)),
            ((205, 128, 44), (42, 148, 185)),
        ],
        "description": "A jewel-like sunfish blazing with orange and turquoise. Tiny but stunning.",
    },
    "white_bass": {
        "name": "White Bass",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills"],
        "weight_range": (0.30, 2.50),
        "length_range": (20, 45),
        "pattern_pool": ["striped", "plain"],
        "colors": [
            ((210, 215, 215), (55, 55, 58)),
            ((198, 204, 204), (48, 48, 52)),
        ],
        "description": "A schooling silver lake fish with bold dark horizontal stripes.",
    },
    "rock_bass": {
        "name": "Rock Bass",
        "rarity_pool": ["common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "birch_forest"],
        "weight_range": (0.10, 0.90),
        "length_range": (12, 28),
        "pattern_pool": ["mottled", "spotted"],
        "colors": [
            ((155, 125, 70), (80, 70, 55)),
            ((142, 115, 62), (70, 62, 48)),
        ],
        "description": "A bronze-mottled panfish with red eyes and a bold personality.",
    },

    # ------------------------------------------------------------------
    # Cold biomes (additional)
    # ------------------------------------------------------------------
    "grayling": {
        "name": "Arctic Grayling",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "river",
        "biome_affinity": ["boreal", "tundra"],
        "weight_range": (0.20, 2.00),
        "length_range": (20, 48),
        "pattern_pool": ["spotted", "plain"],
        "colors": [
            ((185, 185, 205), (120, 100, 185)),
            ((175, 175, 195), (110, 90, 172)),
        ],
        "description": "Known for its enormous iridescent dorsal fin. A prize of arctic rivers.",
    },
    "cisco": {
        "name": "Cisco",
        "rarity_pool": ["common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["boreal", "tundra"],
        "weight_range": (0.15, 1.50),
        "length_range": (18, 40),
        "pattern_pool": ["plain", "scaled"],
        "colors": [
            ((190, 200, 215), (120, 140, 165)),
            ((180, 190, 206), (110, 130, 155)),
        ],
        "description": "A slender, silvery cold-lake fish that schools in open water.",
    },
    "golden_trout": {
        "name": "Golden Trout",
        "rarity_pool": ["rare", "epic"],
        "habitat": "river",
        "biome_affinity": ["tundra"],
        "weight_range": (0.10, 1.50),
        "length_range": (15, 40),
        "pattern_pool": ["spotted", "striped"],
        "colors": [
            ((245, 185, 45), (210, 90, 40)),
            ((235, 172, 38), (198, 82, 35)),
        ],
        "description": "Found only in the coldest mountain streams. Blazingly colorful.",
    },
    "dolly_varden": {
        "name": "Dolly Varden",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "river",
        "biome_affinity": ["boreal", "tundra"],
        "weight_range": (0.20, 4.00),
        "length_range": (22, 65),
        "pattern_pool": ["spotted", "plain"],
        "colors": [
            ((90, 120, 75), (225, 100, 90)),
            ((80, 110, 65), (210, 90, 82)),
        ],
        "description": "A char with vivid pink-red spots on olive flanks. Named after a Dickens character.",
    },
    "round_whitefish": {
        "name": "Round Whitefish",
        "rarity_pool": ["common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["boreal", "tundra"],
        "weight_range": (0.20, 1.40),
        "length_range": (18, 38),
        "pattern_pool": ["plain", "scaled"],
        "colors": [
            ((185, 175, 155), (130, 125, 108)),
            ((175, 165, 145), (120, 115, 100)),
        ],
        "description": "A small, cylindrical whitefish that hugs the cold lake bottom.",
    },

    # ------------------------------------------------------------------
    # Jungle / Tropical (additional)
    # ------------------------------------------------------------------
    "peacock_bass": {
        "name": "Peacock Bass",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["tropical", "jungle"],
        "weight_range": (0.50, 6.00),
        "length_range": (25, 65),
        "pattern_pool": ["banded", "spotted"],
        "colors": [
            ((60, 140, 70), (215, 140, 40)),
            ((52, 128, 62), (200, 128, 35)),
        ],
        "description": "A fierce tropical predator bearing a vivid eyespot on its tail.",
        "tension": 1.9,
    },
    "payara": {
        "name": "Payara",
        "rarity_pool": ["rare", "epic"],
        "habitat": "river",
        "biome_affinity": ["jungle"],
        "weight_range": (1.00, 9.00),
        "length_range": (40, 90),
        "pattern_pool": ["plain", "striped"],
        "colors": [
            ((190, 195, 205), (45, 48, 55)),
            ((178, 184, 195), (38, 42, 48)),
        ],
        "description": "The 'Vampire Fish' — silver and fierce, with two enormous downward-pointing fangs.",
        "tension": 2.4,
    },
    "redtail_catfish": {
        "name": "Redtail Catfish",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "river",
        "biome_affinity": ["jungle", "tropical"],
        "weight_range": (2.00, 20.00),
        "length_range": (45, 120),
        "pattern_pool": ["plain", "spotted"],
        "colors": [
            ((35, 35, 40), (210, 55, 45)),
            ((42, 42, 48), (195, 48, 38)),
        ],
        "description": "A striking catfish with a jet-black body and a brilliant scarlet tail.",
    },
    "discus": {
        "name": "Discus",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["tropical", "jungle"],
        "weight_range": (0.15, 0.80),
        "length_range": (12, 24),
        "pattern_pool": ["striped", "banded"],
        "colors": [
            ((50, 120, 210), (225, 110, 45)),
            ((42, 110, 198), (210, 100, 38)),
        ],
        "description": "A disc-shaped fish of extraordinary color. The 'king of the aquarium'.",
    },
    "pacu": {
        "name": "Pacu",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "river",
        "biome_affinity": ["jungle", "tropical"],
        "weight_range": (1.50, 18.00),
        "length_range": (35, 90),
        "pattern_pool": ["plain", "mottled"],
        "colors": [
            ((55, 58, 45), (195, 85, 50)),
            ((48, 50, 38), (180, 75, 44)),
        ],
        "description": "A piranha relative with flat human-like teeth for crushing seeds and nuts.",
    },
    "oscar": {
        "name": "Oscar",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["tropical", "jungle"],
        "weight_range": (0.30, 1.80),
        "length_range": (18, 36),
        "pattern_pool": ["mottled", "spotted"],
        "colors": [
            ((35, 35, 30), (215, 95, 40)),
            ((42, 42, 36), (200, 86, 34)),
        ],
        "description": "A bold, intelligent cichlid with vivid tiger-orange patches on black.",
    },

    # ------------------------------------------------------------------
    # Wetland / Swamp (additional)
    # ------------------------------------------------------------------
    "pickerel": {
        "name": "Chain Pickerel",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["wetland", "swamp"],
        "weight_range": (0.30, 2.50),
        "length_range": (28, 65),
        "pattern_pool": ["mottled", "spotted"],
        "colors": [
            ((55, 120, 60), (195, 175, 80)),
            ((48, 110, 52), (180, 162, 72)),
        ],
        "description": "A slender swamp predator with intricate chain-link markings of green and gold.",
    },
    "warmouth": {
        "name": "Warmouth",
        "rarity_pool": ["common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["wetland", "swamp"],
        "weight_range": (0.10, 0.70),
        "length_range": (10, 25),
        "pattern_pool": ["mottled", "striped"],
        "colors": [
            ((100, 115, 70), (155, 130, 80)),
            ((90, 105, 62), (142, 120, 72)),
        ],
        "description": "A chunky, wide-mouthed sunfish that lurks among swamp roots.",
    },
    "flier": {
        "name": "Flier",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["wetland", "swamp"],
        "weight_range": (0.05, 0.40),
        "length_range": (8, 20),
        "pattern_pool": ["spotted", "plain"],
        "colors": [
            ((100, 165, 95), (190, 195, 185)),
            ((90, 152, 85), (175, 180, 170)),
        ],
        "description": "A small, disc-shaped sunfish of cypress swamps. Uncommon and underappreciated.",
    },
    "walking_catfish": {
        "name": "Walking Catfish",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "river",
        "biome_affinity": ["wetland", "swamp", "jungle"],
        "weight_range": (0.20, 1.50),
        "length_range": (20, 45),
        "pattern_pool": ["spotted", "mottled"],
        "colors": [
            ((95, 100, 75), (55, 58, 45)),
            ((105, 110, 82), (62, 65, 50)),
        ],
        "description": "Uses its pectoral fins to 'walk' overland between pools during droughts.",
    },
    "longnose_gar": {
        "name": "Longnose Gar",
        "rarity_pool": ["rare", "epic"],
        "habitat": "river",
        "biome_affinity": ["wetland", "swamp", "temperate"],
        "weight_range": (0.80, 7.00),
        "length_range": (60, 120),
        "pattern_pool": ["striped", "mottled"],
        "colors": [
            ((110, 130, 75), (180, 170, 120)),
            ((100, 120, 68), (165, 158, 110)),
        ],
        "description": "A slender, needle-snouted living fossil. Lurks motionless before striking.",
    },
    "grass_carp": {
        "name": "Grass Carp",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["wetland", "swamp", "temperate"],
        "weight_range": (2.00, 20.00),
        "length_range": (45, 110),
        "pattern_pool": ["plain", "scaled"],
        "colors": [
            ((105, 140, 80), (175, 180, 160)),
            ((95, 128, 72), (160, 165, 148)),
        ],
        "description": "A large, torpedo-shaped plant eater. Extremely cautious and difficult to hook.",
    },

    # ------------------------------------------------------------------
    # US Freshwater Lakes
    # ------------------------------------------------------------------
    "lake_trout": {
        "name": "Lake Trout",
        "rarity_pool": ["uncommon", "uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["boreal", "tundra"],
        "weight_range": (1.00, 12.00),
        "length_range": (35, 100),
        "pattern_pool": ["spotted", "mottled"],
        "colors": [
            ((90, 115, 75), (210, 205, 185)),
            ((80, 105, 65), (195, 190, 170)),
        ],
        "description": "A deep cold-lake predator. The largest of the chars, caught through ice and deep trolling.",
    },
    "flathead_catfish": {
        "name": "Flathead Catfish",
        "rarity_pool": ["uncommon", "uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "wetland"],
        "weight_range": (2.00, 30.00),
        "length_range": (45, 120),
        "pattern_pool": ["mottled", "plain"],
        "colors": [
            ((155, 125, 75), (90, 75, 50)),
            ((140, 112, 65), (80, 66, 44)),
        ],
        "description": "A massive, flat-headed ambush predator. Feeds almost exclusively on live prey.",
    },
    "blue_catfish": {
        "name": "Blue Catfish",
        "rarity_pool": ["uncommon", "rare", "epic"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills"],
        "weight_range": (2.00, 45.00),
        "length_range": (50, 140),
        "pattern_pool": ["plain", "mottled"],
        "colors": [
            ((110, 130, 165), (70, 88, 115)),
            ((100, 120, 155), (62, 80, 106)),
        ],
        "description": "The largest catfish in North America. Giants exceed 100 lbs in large river lakes.",
    },
    "yellow_bullhead": {
        "name": "Yellow Bullhead",
        "rarity_pool": ["common", "common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "wetland", "swamp"],
        "weight_range": (0.10, 1.50),
        "length_range": (15, 38),
        "pattern_pool": ["plain", "mottled"],
        "colors": [
            ((200, 165, 70), (130, 105, 45)),
            ((185, 152, 62), (118, 95, 40)),
        ],
        "description": "A small, whiskered catfish with pale chin barbels. A common lake-bottom resident.",
    },
    "brown_bullhead": {
        "name": "Brown Bullhead",
        "rarity_pool": ["common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "wetland"],
        "weight_range": (0.10, 1.80),
        "length_range": (16, 42),
        "pattern_pool": ["mottled", "plain"],
        "colors": [
            ((125, 95, 65), (80, 62, 42)),
            ((115, 88, 58), (72, 55, 38)),
        ],
        "description": "A chunky brown catfish with dark chin barbels and a square tail. Fond of weedy coves.",
    },
    "freshwater_drum": {
        "name": "Freshwater Drum",
        "rarity_pool": ["uncommon", "uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "wetland"],
        "weight_range": (0.50, 12.00),
        "length_range": (28, 80),
        "pattern_pool": ["scaled", "plain"],
        "colors": [
            ((175, 185, 195), (95, 108, 120)),
            ((162, 172, 182), (85, 98, 110)),
        ],
        "description": "The only freshwater drum in North America. Makes a loud rumbling noise with its swim bladder.",
    },
    "sauger": {
        "name": "Sauger",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "boreal"],
        "weight_range": (0.30, 3.00),
        "length_range": (25, 55),
        "pattern_pool": ["mottled", "spotted"],
        "colors": [
            ((155, 130, 75), (85, 90, 65)),
            ((142, 118, 68), (75, 82, 58)),
        ],
        "description": "A smaller walleye cousin with distinctive dark saddle blotches. Prefers turbid lakes.",
    },
    "tiger_muskie": {
        "name": "Tiger Muskie",
        "rarity_pool": ["epic", "legendary"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "boreal", "birch_forest"],
        "weight_range": (3.00, 22.00),
        "length_range": (65, 145),
        "pattern_pool": ["striped", "banded"],
        "colors": [
            ((95, 145, 70), (220, 195, 80)),
            ((85, 132, 62), (205, 180, 72)),
        ],
        "description": "A rare hybrid of muskellunge and northern pike. Grows fast and strikes ferociously.",
    },
    "spotted_bass": {
        "name": "Spotted Bass",
        "rarity_pool": ["uncommon", "uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills"],
        "weight_range": (0.30, 2.50),
        "length_range": (22, 50),
        "pattern_pool": ["spotted", "mottled"],
        "colors": [
            ((85, 130, 70), (50, 80, 42)),
            ((75, 118, 62), (44, 72, 36)),
        ],
        "description": "A bass species with a row of small spots along the lower flank. Prefers rocky points.",
    },
    "striped_bass": {
        "name": "Striped Bass",
        "rarity_pool": ["rare", "rare", "epic"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills"],
        "weight_range": (1.00, 25.00),
        "length_range": (40, 120),
        "pattern_pool": ["striped", "plain"],
        "colors": [
            ((200, 205, 210), (40, 42, 46)),
            ((188, 194, 200), (34, 36, 40)),
        ],
        "description": "A powerhouse reservoir predator. Landlocked stripers run in massive schools and hit hard.",
        "tension": 1.8,
    },
    "yellow_bass": {
        "name": "Yellow Bass",
        "rarity_pool": ["common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills"],
        "weight_range": (0.15, 0.90),
        "length_range": (15, 32),
        "pattern_pool": ["striped", "banded"],
        "colors": [
            ((210, 185, 55), (42, 45, 48)),
            ((198, 172, 48), (36, 38, 42)),
        ],
        "description": "A compact, scrappy schooling fish with bold dark horizontal stripes on a golden body.",
    },
    "redear_sunfish": {
        "name": "Redear Sunfish",
        "rarity_pool": ["uncommon", "uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "wetland"],
        "weight_range": (0.10, 1.80),
        "length_range": (12, 34),
        "pattern_pool": ["plain", "spotted"],
        "colors": [
            ((140, 165, 90), (210, 70, 55)),
            ((128, 152, 80), (195, 62, 48)),
        ],
        "description": "The 'shellcracker' — named for its ability to crush snail shells with powerful throat teeth.",
    },
    "green_sunfish": {
        "name": "Green Sunfish",
        "rarity_pool": ["common", "common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "birch_forest", "wetland"],
        "weight_range": (0.05, 0.50),
        "length_range": (8, 26),
        "pattern_pool": ["banded", "plain"],
        "colors": [
            ((60, 110, 80), (200, 180, 50)),
            ((52, 100, 72), (185, 165, 44)),
        ],
        "description": "A bold, tolerant sunfish with teal-blue streaks on its cheeks. Thrives in degraded water.",
    },
    "longear_sunfish": {
        "name": "Longear Sunfish",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills"],
        "weight_range": (0.04, 0.35),
        "length_range": (8, 22),
        "pattern_pool": ["spotted", "banded"],
        "colors": [
            ((220, 115, 45), (45, 130, 205)),
            ((205, 105, 38), (38, 118, 190)),
        ],
        "description": "Blazingly colorful with a dramatically long gill flap. One of the most vivid freshwater fish.",
    },
    "redbreast_sunfish": {
        "name": "Redbreast Sunfish",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills"],
        "weight_range": (0.05, 0.50),
        "length_range": (10, 26),
        "pattern_pool": ["plain", "spotted"],
        "colors": [
            ((185, 145, 65), (215, 90, 40)),
            ((172, 132, 58), (200, 82, 35)),
        ],
        "description": "A sunfish of Atlantic-slope streams with a vivid reddish-orange belly.",
    },
    "white_crappie": {
        "name": "White Crappie",
        "rarity_pool": ["common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "wetland"],
        "weight_range": (0.15, 1.50),
        "length_range": (14, 38),
        "pattern_pool": ["banded", "spotted"],
        "colors": [
            ((195, 198, 195), (40, 48, 42)),
            ((180, 184, 180), (34, 42, 36)),
        ],
        "description": "A lighter, more silvery crappie with vertical bars. Prefers turbid, warmer lakes than its cousin.",
    },
    "bigmouth_buffalo": {
        "name": "Bigmouth Buffalo",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "wetland"],
        "weight_range": (2.00, 22.00),
        "length_range": (45, 100),
        "pattern_pool": ["scaled", "plain"],
        "colors": [
            ((90, 105, 70), (145, 138, 90)),
            ((80, 95, 62), (132, 126, 82)),
        ],
        "description": "A large, hump-backed sucker with an upturned mouth. Can live over 100 years.",
    },
    "white_sucker": {
        "name": "White Sucker",
        "rarity_pool": ["common", "common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "boreal"],
        "weight_range": (0.30, 3.00),
        "length_range": (25, 58),
        "pattern_pool": ["plain", "scaled"],
        "colors": [
            ((195, 188, 175), (130, 125, 112)),
            ((182, 176, 162), (118, 114, 102)),
        ],
        "description": "An adaptable, bottom-feeding sucker that spawns in shallow streams in spring.",
    },
    "golden_shiner": {
        "name": "Golden Shiner",
        "rarity_pool": ["common", "common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "birch_forest"],
        "weight_range": (0.02, 0.25),
        "length_range": (6, 20),
        "pattern_pool": ["plain", "scaled"],
        "colors": [
            ((205, 185, 80), (145, 130, 55)),
            ((190, 170, 70), (132, 118, 48)),
        ],
        "description": "A deep-bodied golden minnow. The most popular live bait fish in the US.",
    },
    "gizzard_shad": {
        "name": "Gizzard Shad",
        "rarity_pool": ["common", "common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "wetland"],
        "weight_range": (0.05, 0.60),
        "length_range": (12, 38),
        "pattern_pool": ["plain", "scaled"],
        "colors": [
            ((185, 195, 210), (90, 115, 145)),
            ((172, 182, 198), (80, 105, 135)),
        ],
        "description": "A silvery-blue filter-feeder that schools in enormous shimmering clouds near the surface.",
    },
    "paddlefish": {
        "name": "Paddlefish",
        "rarity_pool": ["epic", "epic", "legendary"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "wetland"],
        "weight_range": (5.00, 60.00),
        "length_range": (80, 200),
        "pattern_pool": ["plain", "plated"],
        "colors": [
            ((85, 98, 125), (55, 65, 85)),
            ((95, 108, 138), (62, 72, 95)),
        ],
        "description": "A prehistoric filter-feeder with a paddle-shaped rostrum. Has no scales and no equal.",
    },
    "spotted_gar": {
        "name": "Spotted Gar",
        "rarity_pool": ["rare", "epic"],
        "habitat": "lake",
        "biome_affinity": ["wetland", "swamp", "temperate"],
        "weight_range": (0.50, 4.50),
        "length_range": (45, 90),
        "pattern_pool": ["spotted", "mottled"],
        "colors": [
            ((105, 128, 72), (175, 175, 160)),
            ((95, 116, 64), (160, 160, 146)),
        ],
        "description": "A smaller gar distinguished by spots on its head and snout as well as its body.",
    },
    "white_perch": {
        "name": "White Perch",
        "rarity_pool": ["common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills"],
        "weight_range": (0.10, 0.90),
        "length_range": (15, 32),
        "pattern_pool": ["plain", "striped"],
        "colors": [
            ((198, 200, 205), (115, 125, 138)),
            ((185, 188, 194), (105, 115, 128)),
        ],
        "description": "A schooling silver perch that invades new lakes aggressively. Excellent on the table.",
    },
    "american_eel": {
        "name": "American Eel",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "wetland", "swamp"],
        "weight_range": (0.20, 4.50),
        "length_range": (30, 105),
        "pattern_pool": ["plain", "mottled"],
        "colors": [
            ((70, 80, 60), (125, 138, 100)),
            ((62, 72, 52), (112, 124, 90)),
        ],
        "description": "A snake-like fish that migrates thousands of miles to spawn in the Sargasso Sea.",
    },
    "goldeye": {
        "name": "Goldeye",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "boreal"],
        "weight_range": (0.10, 0.80),
        "length_range": (18, 36),
        "pattern_pool": ["plain", "scaled"],
        "colors": [
            ((195, 195, 205), (200, 165, 45)),
            ((182, 182, 194), (185, 152, 38)),
        ],
        "description": "Named for its large, glinting golden eye. A prized smoked fish of the Canadian prairies.",
    },

    # ------------------------------------------------------------------
    # US Freshwater Lakes (batch 2)
    # ------------------------------------------------------------------
    "black_bullhead": {
        "name": "Black Bullhead",
        "rarity_pool": ["common", "common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "wetland", "swamp"],
        "weight_range": (0.10, 1.20),
        "length_range": (14, 32),
        "pattern_pool": ["plain", "mottled"],
        "colors": [
            ((55, 55, 48), (175, 168, 120)),
            ((65, 62, 55), (188, 180, 130)),
        ],
        "description": "The darkest of the bullheads. Thrives in warm, turbid ponds where other fish struggle.",
    },
    "sunshine_bass": {
        "name": "Sunshine Bass",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills"],
        "weight_range": (0.50, 8.00),
        "length_range": (28, 65),
        "pattern_pool": ["striped", "plain"],
        "colors": [
            ((205, 208, 215), (38, 40, 45)),
            ((192, 196, 204), (32, 34, 40)),
        ],
        "description": "A hybrid of striped and white bass. Grows faster than either parent and hits like a freight train.",
    },
    "saugeye": {
        "name": "Saugeye",
        "rarity_pool": ["rare", "epic"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills"],
        "weight_range": (0.40, 4.50),
        "length_range": (28, 62),
        "pattern_pool": ["mottled", "spotted"],
        "colors": [
            ((175, 148, 80), (88, 95, 68)),
            ((160, 135, 72), (78, 85, 60)),
        ],
        "description": "A walleye × sauger hybrid stocked in turbid reservoirs. Inherits the best of both parents.",
    },
    "mooneye": {
        "name": "Mooneye",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "boreal"],
        "weight_range": (0.15, 0.90),
        "length_range": (18, 40),
        "pattern_pool": ["plain", "scaled"],
        "colors": [
            ((192, 198, 210), (155, 162, 178)),
            ((180, 186, 198), (142, 150, 165)),
        ],
        "description": "A close relative of the goldeye with a large silver eye. Leaps acrobatically when hooked.",
    },
    "emerald_shiner": {
        "name": "Emerald Shiner",
        "rarity_pool": ["common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "boreal"],
        "weight_range": (0.005, 0.04),
        "length_range": (5, 12),
        "pattern_pool": ["plain", "scaled"],
        "colors": [
            ((175, 210, 175), (120, 188, 145)),
            ((165, 200, 165), (110, 175, 135)),
        ],
        "description": "A slender, sparkling minnow with a vivid emerald-green lateral stripe. Vast schools in open water.",
    },
    "fathead_minnow": {
        "name": "Fathead Minnow",
        "rarity_pool": ["common", "common", "common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": [],
        "weight_range": (0.005, 0.05),
        "length_range": (4, 10),
        "pattern_pool": ["plain", "banded"],
        "colors": [
            ((148, 130, 95), (88, 78, 58)),
            ((40, 38, 32), (155, 138, 100)),
        ],
        "description": "The most abundant minnow in North America. Breeding males turn jet-black with a spongy pad on their snout.",
    },
    "rainbow_darter": {
        "name": "Rainbow Darter",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills"],
        "weight_range": (0.005, 0.025),
        "length_range": (4, 8),
        "pattern_pool": ["banded", "striped"],
        "colors": [
            ((45, 115, 200), (225, 118, 35)),
            ((38, 105, 185), (210, 108, 30)),
        ],
        "description": "A jewel-sized bottom fish with electric-blue and orange banding. Males are among the most vivid US fish.",
    },
    "logperch": {
        "name": "Logperch",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills"],
        "weight_range": (0.01, 0.09),
        "length_range": (8, 18),
        "pattern_pool": ["banded", "striped"],
        "colors": [
            ((185, 172, 120), (55, 58, 48)),
            ((172, 160, 110), (48, 50, 42)),
        ],
        "description": "The largest darter. Flips pebbles with its pig-like snout to find the insects hiding beneath.",
    },
    "quillback": {
        "name": "Quillback",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "wetland"],
        "weight_range": (0.30, 4.00),
        "length_range": (25, 60),
        "pattern_pool": ["scaled", "plain"],
        "colors": [
            ((155, 145, 90), (100, 120, 65)),
            ((142, 132, 80), (90, 108, 58)),
        ],
        "description": "A deep-bodied carpsucker with a long, quill-like first dorsal ray. Rooting along silty bottoms.",
    },
    "shorthead_redhorse": {
        "name": "Shorthead Redhorse",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "boreal"],
        "weight_range": (0.30, 3.00),
        "length_range": (25, 55),
        "pattern_pool": ["plain", "scaled"],
        "colors": [
            ((185, 170, 120), (215, 85, 45)),
            ((172, 158, 110), (200, 75, 38)),
        ],
        "description": "A sucker with brilliant red-orange fins. Spawns in river rapids in spring.",
    },
    "northern_hogsucker": {
        "name": "Northern Hogsucker",
        "rarity_pool": ["common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills"],
        "weight_range": (0.15, 2.00),
        "length_range": (20, 50),
        "pattern_pool": ["banded", "mottled"],
        "colors": [
            ((155, 138, 85), (62, 58, 42)),
            ((142, 126, 75), (55, 52, 38)),
        ],
        "description": "Has a large, shovel-like head and distinctive dark saddles. Constantly roots through gravel for insect larvae.",
    },
    "smallmouth_buffalo": {
        "name": "Smallmouth Buffalo",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "wetland"],
        "weight_range": (1.00, 15.00),
        "length_range": (35, 85),
        "pattern_pool": ["scaled", "plain"],
        "colors": [
            ((70, 88, 58), (120, 118, 82)),
            ((62, 80, 52), (110, 108, 74)),
        ],
        "description": "A smaller, more slender buffalo than its bigmouth cousin. A bottom-filter feeder of still waters.",
    },
    "threadfin_shad": {
        "name": "Threadfin Shad",
        "rarity_pool": ["common", "common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "wetland"],
        "weight_range": (0.01, 0.06),
        "length_range": (6, 18),
        "pattern_pool": ["plain", "scaled"],
        "colors": [
            ((195, 205, 218), (195, 185, 55)),
            ((182, 192, 206), (180, 170, 48)),
        ],
        "description": "A delicate silver shad with a yellow-tipped tail. Named for the thread-like extension on its dorsal fin.",
    },
    "redfin_pickerel": {
        "name": "Redfin Pickerel",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["wetland", "swamp"],
        "weight_range": (0.05, 0.55),
        "length_range": (15, 40),
        "pattern_pool": ["mottled", "striped"],
        "colors": [
            ((65, 120, 58), (195, 178, 70)),
            ((58, 108, 52), (180, 165, 62)),
        ],
        "description": "The smallest pickerel. Lurks in dense aquatic vegetation with vivid red-orange fins.",
    },
    "pirate_perch": {
        "name": "Pirate Perch",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["wetland", "swamp"],
        "weight_range": (0.03, 0.18),
        "length_range": (8, 18),
        "pattern_pool": ["plain", "mottled"],
        "colors": [
            ((75, 58, 88), (48, 38, 60)),
            ((88, 68, 100), (55, 44, 72)),
        ],
        "description": "A bizarre little predator whose anus migrates to just behind its head as it matures. Unique among US fish.",
    },
    "alewife": {
        "name": "Alewife",
        "rarity_pool": ["common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["boreal", "temperate"],
        "weight_range": (0.03, 0.25),
        "length_range": (10, 25),
        "pattern_pool": ["plain", "scaled"],
        "colors": [
            ((155, 175, 205), (88, 112, 148)),
            ((142, 162, 192), (78, 102, 135)),
        ],
        "description": "A landlocked herring that exploded in the Great Lakes. An essential forage fish for salmon and trout.",
    },
    "rainbow_smelt": {
        "name": "Rainbow Smelt",
        "rarity_pool": ["common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["boreal", "tundra"],
        "weight_range": (0.02, 0.15),
        "length_range": (10, 25),
        "pattern_pool": ["plain", "scaled"],
        "colors": [
            ((175, 205, 195), (115, 148, 165)),
            ((162, 192, 182), (105, 135, 152)),
        ],
        "description": "A translucent cold-water fish with a faint iridescent stripe. Runs into streams by the millions in spring.",
    },
    "trout_perch": {
        "name": "Trout-Perch",
        "rarity_pool": ["common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["boreal", "temperate"],
        "weight_range": (0.02, 0.12),
        "length_range": (8, 18),
        "pattern_pool": ["spotted", "plain"],
        "colors": [
            ((185, 178, 148), (95, 105, 75)),
            ((172, 165, 136), (85, 95, 68)),
        ],
        "description": "A relict species that bridges trout and perch. Found in deep cold lakes, seldom seen by anglers.",
    },
    "ruffe": {
        "name": "Ruffe",
        "rarity_pool": ["common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["boreal", "temperate"],
        "weight_range": (0.02, 0.20),
        "length_range": (8, 22),
        "pattern_pool": ["spotted", "mottled"],
        "colors": [
            ((145, 128, 80), (78, 82, 55)),
            ((132, 116, 72), (68, 72, 48)),
        ],
        "description": "An invasive Eurasian perch now established in the Great Lakes. Spiny, prolific, and hard to eradicate.",
    },
    "round_goby": {
        "name": "Round Goby",
        "rarity_pool": ["common", "common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["boreal", "temperate"],
        "weight_range": (0.01, 0.15),
        "length_range": (7, 25),
        "pattern_pool": ["mottled", "spotted"],
        "colors": [
            ((118, 112, 98), (58, 55, 48)),
            ((105, 100, 86), (50, 48, 42)),
        ],
        "description": "An invasive bottom-dweller from the Black Sea. Spreads through ballast water. Uses a suction disc to cling to rocks.",
    },

    # ------------------------------------------------------------------
    # US Freshwater Lakes (batch 3)
    # ------------------------------------------------------------------
    "cutthroat_trout": {
        "name": "Cutthroat Trout",
        "rarity_pool": ["uncommon", "uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["boreal", "tundra"],
        "weight_range": (0.20, 4.50),
        "length_range": (20, 65),
        "pattern_pool": ["spotted", "plain"],
        "colors": [
            ((145, 155, 110), (215, 75, 55)),
            ((132, 142, 100), (200, 65, 48)),
        ],
        "description": "Named for the vivid red-orange slash marks under its jaw. A prize of western mountain lakes.",
    },
    "kokanee": {
        "name": "Kokanee",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["boreal", "tundra"],
        "weight_range": (0.30, 3.00),
        "length_range": (25, 55),
        "pattern_pool": ["plain", "spotted"],
        "colors": [
            ((170, 192, 210), (95, 118, 145)),
            ((210, 60, 55),   (80, 42, 38)),
        ],
        "description": "The landlocked sockeye salmon. Silver and sleek in the lake; blood-red at spawning time.",
    },
    "splake": {
        "name": "Splake",
        "rarity_pool": ["rare", "epic"],
        "habitat": "lake",
        "biome_affinity": ["boreal", "tundra"],
        "weight_range": (0.50, 6.00),
        "length_range": (30, 72),
        "pattern_pool": ["spotted", "mottled"],
        "colors": [
            ((85, 108, 72), (215, 138, 65)),
            ((75, 98, 62), (200, 125, 58)),
        ],
        "description": "A lake trout × brook trout hybrid. Combines both parents' hardiness in one hard-hitting fish.",
    },
    "tiger_trout": {
        "name": "Tiger Trout",
        "rarity_pool": ["epic", "legendary"],
        "habitat": "lake",
        "biome_affinity": ["boreal", "birch_forest"],
        "weight_range": (0.20, 3.50),
        "length_range": (20, 58),
        "pattern_pool": ["mottled", "striped"],
        "colors": [
            ((175, 135, 55), (42, 38, 28)),
            ((162, 124, 48), (35, 32, 22)),
        ],
        "description": "A brown × brook trout hybrid with wild, marble-like vermiculate markings. Almost never found naturally.",
    },
    "bull_trout": {
        "name": "Bull Trout",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["boreal", "tundra"],
        "weight_range": (0.30, 7.00),
        "length_range": (25, 72),
        "pattern_pool": ["spotted", "plain"],
        "colors": [
            ((80, 108, 72), (230, 195, 80)),
            ((70, 98, 62), (215, 180, 70)),
        ],
        "description": "A char of icy mountain lakes. Requires the coldest, cleanest water — its presence signals pristine habitat.",
    },
    "coho_salmon": {
        "name": "Coho Salmon",
        "rarity_pool": ["rare", "rare", "epic"],
        "habitat": "lake",
        "biome_affinity": ["boreal", "tundra"],
        "weight_range": (1.50, 9.00),
        "length_range": (45, 90),
        "pattern_pool": ["spotted", "plain"],
        "colors": [
            ((185, 198, 212), (42, 44, 48)),
            ((195, 65, 55),   (80, 38, 34)),
        ],
        "description": "A Pacific salmon stocked throughout the Great Lakes. Chrome bright one season, crimson the next.",
    },
    "longnose_sucker": {
        "name": "Longnose Sucker",
        "rarity_pool": ["common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["boreal", "tundra"],
        "weight_range": (0.30, 3.50),
        "length_range": (25, 62),
        "pattern_pool": ["plain", "scaled"],
        "colors": [
            ((95, 105, 80), (195, 165, 100)),
            ((85, 95, 72), (180, 152, 90)),
        ],
        "description": "A cold-water sucker with a distinctly long snout. Abundant in northern lakes and glacial streams.",
    },
    "bluntnose_minnow": {
        "name": "Bluntnose Minnow",
        "rarity_pool": ["common", "common", "common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": [],
        "weight_range": (0.005, 0.04),
        "length_range": (5, 10),
        "pattern_pool": ["plain", "striped"],
        "colors": [
            ((162, 165, 148), (88, 92, 72)),
            ((148, 152, 135), (78, 82, 62)),
        ],
        "description": "Possibly the most abundant minnow in the eastern US. A blunt snout and a dark lateral stripe.",
    },
    "spottail_shiner": {
        "name": "Spottail Shiner",
        "rarity_pool": ["common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "boreal"],
        "weight_range": (0.005, 0.04),
        "length_range": (5, 12),
        "pattern_pool": ["plain", "scaled"],
        "colors": [
            ((192, 198, 205), (30, 30, 32)),
            ((180, 186, 194), (25, 25, 28)),
        ],
        "description": "A slender silver shiner with a distinctive black spot at the base of its tail. Schools in open lake water.",
    },
    "hornyhead_chub": {
        "name": "Hornyhead Chub",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills"],
        "weight_range": (0.05, 0.30),
        "length_range": (10, 25),
        "pattern_pool": ["plain", "spotted"],
        "colors": [
            ((165, 148, 88), (218, 115, 55)),
            ((152, 136, 78), (205, 105, 48)),
        ],
        "description": "Breeding males sprout a crown of tubercles and flush orange on the cheeks. Builds pebble nests.",
    },
    "fallfish": {
        "name": "Fallfish",
        "rarity_pool": ["common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "birch_forest"],
        "weight_range": (0.10, 1.00),
        "length_range": (15, 45),
        "pattern_pool": ["plain", "scaled"],
        "colors": [
            ((185, 182, 162), (110, 118, 90)),
            ((172, 170, 150), (100, 108, 82)),
        ],
        "description": "The largest native minnow in the eastern US. Builds boulder nests up to a meter tall.",
    },
    "mosquitofish": {
        "name": "Mosquitofish",
        "rarity_pool": ["common", "common", "common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "wetland", "swamp"],
        "weight_range": (0.001, 0.012),
        "length_range": (2, 6),
        "pattern_pool": ["plain", "spotted"],
        "colors": [
            ((128, 125, 105), (88, 85, 70)),
            ((115, 112, 95), (78, 75, 62)),
        ],
        "description": "A live-bearing minnow that can eat its weight in mosquito larvae daily. Introduced worldwide.",
    },
    "johnny_darter": {
        "name": "Johnny Darter",
        "rarity_pool": ["common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "boreal"],
        "weight_range": (0.003, 0.015),
        "length_range": (4, 7),
        "pattern_pool": ["mottled", "spotted"],
        "colors": [
            ((175, 158, 108), (55, 52, 38)),
            ((162, 145, 98), (48, 45, 32)),
        ],
        "description": "A tiny darter covered in W-shaped zigzag marks. Scoots across the bottom in short dashes.",
    },
    "iowa_darter": {
        "name": "Iowa Darter",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "wetland"],
        "weight_range": (0.003, 0.020),
        "length_range": (4, 8),
        "pattern_pool": ["banded", "spotted"],
        "colors": [
            ((65, 118, 188), (215, 105, 42)),
            ((55, 108, 175), (200, 95, 36)),
        ],
        "description": "A small, prairie-lake darter with blue and orange breeding colors. Clings to aquatic vegetation.",
    },
    "orangethroat_darter": {
        "name": "Orangethroat Darter",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills"],
        "weight_range": (0.003, 0.020),
        "length_range": (4, 8),
        "pattern_pool": ["banded", "striped"],
        "colors": [
            ((52, 125, 172), (225, 112, 38)),
            ((44, 112, 158), (210, 102, 32)),
        ],
        "description": "The male blazes blue-green with a vivid orange throat in breeding season. A tiny jewel of riffle habitat.",
    },
    "least_darter": {
        "name": "Least Darter",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "wetland"],
        "weight_range": (0.001, 0.006),
        "length_range": (2, 5),
        "pattern_pool": ["spotted", "plain"],
        "colors": [
            ((105, 148, 105), (55, 80, 55)),
            ((95, 135, 95), (48, 72, 48)),
        ],
        "description": "The world's smallest perch — barely the length of a thumbnail. Darts among aquatic mosses.",
    },
    "crystal_darter": {
        "name": "Crystal Darter",
        "rarity_pool": ["rare", "epic"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills"],
        "weight_range": (0.005, 0.028),
        "length_range": (6, 12),
        "pattern_pool": ["plain", "spotted"],
        "colors": [
            ((205, 210, 215), (48, 50, 42)),
            ((192, 198, 204), (40, 42, 36)),
        ],
        "description": "A nearly transparent sand-dwelling darter. Four dark saddle bands are visible through its translucent body.",
    },
    "blue_sucker": {
        "name": "Blue Sucker",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "wetland"],
        "weight_range": (1.00, 6.50),
        "length_range": (45, 90),
        "pattern_pool": ["plain", "scaled"],
        "colors": [
            ((88, 108, 142), (55, 70, 95)),
            ((78, 98, 130), (48, 62, 85)),
        ],
        "description": "A streamlined slate-blue sucker built for fast current. Declining across much of its range.",
    },
    "dollar_sunfish": {
        "name": "Dollar Sunfish",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["wetland", "swamp"],
        "weight_range": (0.02, 0.15),
        "length_range": (6, 14),
        "pattern_pool": ["spotted", "plain"],
        "colors": [
            ((55, 118, 88), (192, 185, 52)),
            ((48, 108, 78), (178, 172, 45)),
        ],
        "description": "A tiny, coin-shaped sunfish of cypress swamps with iridescent blue-green spots on an olive body.",
    },
    "spotted_bullhead": {
        "name": "Spotted Bullhead",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["wetland", "swamp"],
        "weight_range": (0.15, 1.50),
        "length_range": (18, 40),
        "pattern_pool": ["spotted", "plain"],
        "colors": [
            ((55, 48, 38), (218, 215, 205)),
            ((62, 55, 44), (205, 200, 190)),
        ],
        "description": "A rarely seen catfish with bold white spots on a dark body. Restricted to a few southeastern rivers.",
    },

    # ------------------------------------------------------------------
    # Universal (new)
    # ------------------------------------------------------------------
    "gudgeon": {
        "name": "Gudgeon",
        "rarity_pool": ["common", "common", "common", "uncommon"],
        "habitat": "river",
        "biome_affinity": [],
        "weight_range": (0.01, 0.08),
        "length_range": (5, 12),
        "pattern_pool": ["mottled", "plain", "spotted"],
        "colors": [
            ((145, 125, 90), (80, 68, 45)),
            ((160, 138, 100), (90, 78, 52)),
        ],
        "description": "A small, bottom-hugging river fish with sensory barbels. Found in clear, gravelly streams worldwide.",
    },
    "bleak": {
        "name": "Bleak",
        "rarity_pool": ["common", "common", "uncommon"],
        "habitat": "river",
        "biome_affinity": [],
        "weight_range": (0.01, 0.06),
        "length_range": (6, 15),
        "pattern_pool": ["plain", "striped"],
        "colors": [
            ((210, 220, 225), (145, 165, 180)),
            ((200, 215, 220), (135, 158, 172)),
        ],
        "description": "A slender, silver-flanked surface fish that darts in glittering shoals near the water's edge.",
    },
    "mottled_sculpin": {
        "name": "Mottled Sculpin",
        "rarity_pool": ["uncommon", "uncommon", "rare"],
        "habitat": "river",
        "biome_affinity": [],
        "weight_range": (0.02, 0.18),
        "length_range": (5, 18),
        "pattern_pool": ["mottled", "plain"],
        "colors": [
            ((110, 90, 65), (68, 52, 35)),
            ((125, 105, 78), (78, 62, 42)),
        ],
        "description": "A spiny, broad-headed river fish that clings to stream bottoms. Master of camouflage against gravel.",
    },

    # ------------------------------------------------------------------
    # Temperate (new)
    # ------------------------------------------------------------------
    "creek_chub": {
        "name": "Creek Chub",
        "rarity_pool": ["common", "common", "uncommon"],
        "habitat": "river",
        "biome_affinity": ["temperate", "rolling_hills", "birch_forest"],
        "weight_range": (0.05, 0.50),
        "length_range": (8, 28),
        "pattern_pool": ["plain", "spotted"],
        "colors": [
            ((140, 118, 85), (85, 68, 45)),
            ((152, 130, 95), (95, 78, 52)),
        ],
        "description": "A stout-bodied creek fish that builds pebble mound nests. Males develop bright breeding colors in spring.",
    },
    "river_carpsucker": {
        "name": "River Carpsucker",
        "rarity_pool": ["uncommon", "uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills"],
        "weight_range": (0.8, 3.5),
        "length_range": (30, 58),
        "pattern_pool": ["plain", "scaled"],
        "colors": [
            ((175, 155, 105), (115, 98, 65)),
            ((188, 168, 118), (125, 108, 75)),
        ],
        "description": "A deep-bodied sucker that cruises river shallows in loose schools. Silvery-bronze with subtly scaled flanks.",
    },
    "spotted_sucker": {
        "name": "Spotted Sucker",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "river",
        "biome_affinity": ["temperate", "rolling_hills", "birch_forest"],
        "weight_range": (0.5, 2.5),
        "length_range": (25, 50),
        "pattern_pool": ["spotted", "plain"],
        "colors": [
            ((155, 132, 95), (38, 42, 32)),
            ((168, 145, 108), (42, 46, 36)),
        ],
        "description": "A trim sucker with neat rows of dark spots along each scale row. Prefers clear, sand-bottomed rivers.",
    },
    "warpaint_shiner": {
        "name": "Warpaint Shiner",
        "rarity_pool": ["uncommon", "rare", "rare"],
        "habitat": "river",
        "biome_affinity": ["temperate", "rolling_hills", "birch_forest"],
        "weight_range": (0.03, 0.18),
        "length_range": (8, 18),
        "pattern_pool": ["striped", "plain"],
        "colors": [
            ((215, 185, 60), (200, 80, 40)),
            ((205, 175, 50), (190, 70, 35)),
        ],
        "description": "A vivid shiner with a crimson blotch behind the eye and golden flanks. One of the most colorful native minnows.",
    },

    # ------------------------------------------------------------------
    # Cold / Boreal (new)
    # ------------------------------------------------------------------
    "pink_salmon": {
        "name": "Pink Salmon",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "river",
        "biome_affinity": ["boreal", "tundra"],
        "weight_range": (1.5, 5.5),
        "length_range": (45, 68),
        "pattern_pool": ["plain", "scaled"],
        "colors": [
            ((195, 165, 150), (115, 88, 80)),
            ((185, 155, 140), (105, 80, 72)),
            ((155, 130, 120), (90, 65, 58)),
        ],
        "description": "The smallest Pacific salmon, arriving in enormous spawning runs. Males grow a distinctive humped back.",
    },
    "chum_salmon": {
        "name": "Chum Salmon",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "river",
        "biome_affinity": ["boreal", "tundra"],
        "weight_range": (3.0, 11.0),
        "length_range": (55, 90),
        "pattern_pool": ["striped", "mottled"],
        "colors": [
            ((125, 148, 105), (180, 100, 80)),
            ((118, 138, 98), (168, 90, 72)),
        ],
        "description": "A powerful ocean salmon with bold calico markings in its spawning colors. Also called the dog salmon.",
        "tension": 1.7,
    },
    "lake_sculpin": {
        "name": "Lake Sculpin",
        "rarity_pool": ["uncommon", "uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["boreal", "tundra"],
        "weight_range": (0.04, 0.35),
        "length_range": (8, 22),
        "pattern_pool": ["mottled", "plain"],
        "colors": [
            ((88, 95, 108), (52, 58, 68)),
            ((78, 85, 98), (45, 50, 60)),
        ],
        "description": "A deep-water sculpin of cold northern lakes. Spends most of its life hugging the muddy lake floor.",
    },
    "ninespine_stickleback": {
        "name": "Ninespine Stickleback",
        "rarity_pool": ["common", "common", "uncommon"],
        "habitat": "river",
        "biome_affinity": ["boreal", "tundra", "temperate"],
        "weight_range": (0.003, 0.015),
        "length_range": (4, 9),
        "pattern_pool": ["plain", "striped"],
        "colors": [
            ((155, 168, 148), (95, 108, 88)),
            ((145, 158, 138), (88, 100, 80)),
        ],
        "description": "A tiny armored fish with up to nine sharp dorsal spines. Males build elaborate bubble nests and guard eggs.",
    },

    # ------------------------------------------------------------------
    # Jungle / Tropical (new)
    # ------------------------------------------------------------------
    "arowana": {
        "name": "Silver Arowana",
        "rarity_pool": ["rare", "rare", "epic"],
        "habitat": "river",
        "biome_affinity": ["jungle", "tropical"],
        "weight_range": (3.0, 6.0),
        "length_range": (55, 90),
        "pattern_pool": ["plain", "scaled"],
        "colors": [
            ((210, 225, 230), (145, 168, 185)),
            ((220, 232, 238), (155, 178, 195)),
        ],
        "description": "A surface-hunting predator with enormous mirror-like scales. Leaps from the water to snatch insects and small birds.",
    },
    "goliath_tigerfish": {
        "name": "Goliath Tigerfish",
        "rarity_pool": ["epic", "epic", "legendary"],
        "habitat": "river",
        "biome_affinity": ["jungle", "tropical"],
        "weight_range": (25.0, 70.0),
        "length_range": (105, 180),
        "pattern_pool": ["striped", "plain"],
        "colors": [
            ((195, 188, 152), (38, 38, 32)),
            ((185, 178, 142), (32, 32, 28)),
        ],
        "description": "One of Africa's most feared river predators. Razor teeth and raw power make it a legendary catch.",
    },
    "bichir": {
        "name": "Bichir",
        "rarity_pool": ["rare", "epic"],
        "habitat": "river",
        "biome_affinity": ["jungle", "tropical"],
        "weight_range": (0.8, 4.0),
        "length_range": (35, 75),
        "pattern_pool": ["plated", "mottled"],
        "colors": [
            ((72, 82, 55), (42, 48, 32)),
            ((80, 90, 62), (48, 55, 38)),
        ],
        "description": "An ancient fish with bony armor plates and a series of finlets along its back. Breathes air with a primitive lung.",
    },
    "giant_gourami": {
        "name": "Giant Gourami",
        "rarity_pool": ["rare", "rare", "epic"],
        "habitat": "lake",
        "biome_affinity": ["tropical", "jungle"],
        "weight_range": (2.0, 9.0),
        "length_range": (45, 75),
        "pattern_pool": ["plain", "spotted"],
        "colors": [
            ((210, 148, 62), (160, 105, 38)),
            ((195, 138, 55), (148, 95, 32)),
            ((165, 115, 45), (120, 80, 28)),
        ],
        "description": "The largest of the gouramis, with a rounded body and long trailing ventral feelers. Tends massive bubble nests.",
    },
    "rivulus": {
        "name": "Rivulus",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "river",
        "biome_affinity": ["jungle", "tropical"],
        "weight_range": (0.003, 0.012),
        "length_range": (3, 7),
        "pattern_pool": ["plain", "spotted"],
        "colors": [
            ((155, 95, 42), (38, 68, 38)),
            ((168, 108, 52), (42, 75, 42)),
            ((85, 128, 72), (38, 68, 38)),
        ],
        "description": "A jewel-colored killifish of jungle streams. Can survive drought by entering dormancy buried in moist soil.",
    },

    # ------------------------------------------------------------------
    # Pacific / Polynesian
    # ------------------------------------------------------------------
    "mahi_mahi": {
        "name": "Mahi-Mahi",
        "rarity_pool": ["rare", "epic"],
        "habitat": "river",
        "biome_affinity": ["pacific_island", "beach", "tropical"],
        "weight_range": (2.0, 20.0),
        "length_range": (50, 130),
        "pattern_pool": ["spotted", "banded"],
        "colors": [
            ((40, 180, 160), (210, 175, 40)),
            ((35, 165, 148), (195, 160, 35)),
            ((50, 195, 175), (225, 190, 50)),
        ],
        "description": "A blazing fast pelagic fish of warm Pacific waters. Its vivid blue-green and gold flanks fade quickly after being caught.",
    },
    "parrotfish": {
        "name": "Parrotfish",
        "rarity_pool": ["uncommon", "uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["pacific_island", "beach"],
        "weight_range": (0.5, 4.5),
        "length_range": (25, 65),
        "pattern_pool": ["scaled", "mottled"],
        "colors": [
            ((80, 190, 145), (200, 100, 160)),
            ((65, 175, 130), (185, 85, 145)),
            ((100, 200, 160), (215, 120, 175)),
        ],
        "description": "A reef fish that crunches coral with a beak-like jaw. Sleeps in a mucous cocoon and produces the white sand of tropical beaches.",
    },
    "triggerfish": {
        "name": "Triggerfish",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["pacific_island", "beach"],
        "weight_range": (0.3, 3.0),
        "length_range": (20, 45),
        "pattern_pool": ["spotted", "plain"],
        "colors": [
            ((50, 80, 160), (240, 195, 40)),
            ((40, 65, 145), (225, 180, 35)),
            ((85, 120, 185), (255, 215, 60)),
        ],
        "description": "Hawaii's state fish — the humuhumunukunukuapua'a. Wedges itself into coral crevices by locking its dorsal spine.",
    },
    "flying_fish": {
        "name": "Flying Fish",
        "rarity_pool": ["common", "common", "uncommon"],
        "habitat": "river",
        "biome_affinity": ["pacific_island", "ocean", "beach"],
        "weight_range": (0.1, 0.6),
        "length_range": (18, 35),
        "pattern_pool": ["plain", "banded"],
        "colors": [
            ((55, 90, 155), (215, 230, 245)),
            ((45, 78, 140), (200, 218, 238)),
        ],
        "description": "A remarkable open-ocean fish that glides above the surface on wing-like pectoral fins. Polynesian navigators once tracked their flight to find islands.",
    },
    "yellowfin_tuna": {
        "name": "Yellowfin Tuna",
        "rarity_pool": ["rare", "epic"],
        "habitat": "river",
        "biome_affinity": ["pacific_island", "ocean", "tropical"],
        "weight_range": (5.0, 60.0),
        "length_range": (70, 180),
        "pattern_pool": ["plain", "striped"],
        "colors": [
            ((28, 55, 100), (220, 190, 30)),
            ((22, 45, 88), (210, 178, 25)),
        ],
        "description": "The ahi of Hawaiian fishermen. A powerful open-water predator whose brilliant yellow fins and blazing speed made it a prized catch for outrigger canoe crews.",
        "tension": 2.3,
    },

    # ------------------------------------------------------------------
    # Wetland / Swamp (new)
    # ------------------------------------------------------------------
    "chain_pickerel": {
        "name": "Chain Pickerel",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["wetland", "swamp"],
        "weight_range": (0.4, 2.5),
        "length_range": (28, 55),
        "pattern_pool": ["striped", "mottled"],
        "colors": [
            ((88, 120, 65), (215, 195, 85)),
            ((80, 110, 58), (200, 180, 75)),
        ],
        "description": "A sleek, chain-patterned ambush predator that lurks among lily pads. Strikes with explosive speed.",
    },
    "golden_topminnow": {
        "name": "Golden Topminnow",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "river",
        "biome_affinity": ["wetland", "swamp"],
        "weight_range": (0.005, 0.025),
        "length_range": (4, 9),
        "pattern_pool": ["plain", "spotted"],
        "colors": [
            ((220, 185, 45), (155, 125, 25)),
            ((208, 175, 38), (145, 115, 20)),
        ],
        "description": "A brilliant golden surface fish that skims the still edges of bayous and oxbows for floating insects.",
    },
    "cypress_darter": {
        "name": "Cypress Darter",
        "rarity_pool": ["rare", "epic"],
        "habitat": "river",
        "biome_affinity": ["wetland", "swamp"],
        "weight_range": (0.003, 0.014),
        "length_range": (3, 6),
        "pattern_pool": ["plain", "spotted"],
        "colors": [
            ((72, 118, 82), (188, 145, 55)),
            ((65, 108, 75), (175, 135, 48)),
        ],
        "description": "A tiny jewel of the cypress swamps, with vivid green and amber markings. Rarely seen among the dark water roots.",
    },
    "swamp_eel": {
        "name": "Swamp Eel",
        "rarity_pool": ["rare", "epic"],
        "habitat": "river",
        "biome_affinity": ["wetland", "swamp"],
        "weight_range": (0.3, 1.8),
        "length_range": (40, 100),
        "pattern_pool": ["plain", "mottled"],
        "colors": [
            ((95, 108, 62), (55, 65, 35)),
            ((88, 98, 55), (48, 58, 30)),
        ],
        "description": "A scaleless, serpentine fish that breathes air and slithers through swamp mud. Thrives where true eels cannot.",
    },

    # ------------------------------------------------------------------
    # Japan / East Asia
    # ------------------------------------------------------------------
    "ayu": {
        "name": "Ayu",
        "rarity_pool": ["common", "common", "uncommon"],
        "habitat": "river",
        "biome_affinity": ["temperate", "boreal", "birch_forest"],
        "weight_range": (0.08, 0.30),
        "length_range": (15, 30),
        "pattern_pool": ["plain", "striped"],
        "colors": [
            ((195, 210, 195), (165, 155, 80)),
            ((185, 200, 185), (155, 145, 70)),
        ],
        "description": "Japan's iconic sweetfish. Migrates from sea to river each year and is prized for its subtle watermelon fragrance.",
    },
    "oikawa": {
        "name": "Oikawa",
        "rarity_pool": ["common", "uncommon", "rare"],
        "habitat": "river",
        "biome_affinity": ["temperate", "rolling_hills", "birch_forest"],
        "weight_range": (0.03, 0.18),
        "length_range": (8, 20),
        "pattern_pool": ["plain", "striped"],
        "colors": [
            ((210, 215, 225), (200, 85, 35)),
            ((195, 205, 215), (185, 75, 28)),
            ((185, 125, 65), (215, 90, 35)),
        ],
        "description": "A pale river chub whose males blaze into vivid red-orange during the spring breeding season.",
    },
    "tanago": {
        "name": "Tanago",
        "rarity_pool": ["uncommon", "rare", "epic"],
        "habitat": "river",
        "biome_affinity": ["temperate", "wetland"],
        "weight_range": (0.005, 0.025),
        "length_range": (4, 9),
        "pattern_pool": ["plain", "scaled"],
        "colors": [
            ((95, 175, 185), (210, 130, 155)),
            ((85, 162, 172), (198, 120, 142)),
            ((105, 188, 195), (220, 145, 168)),
        ],
        "description": "A jewel-bright bitterling that lays its eggs inside living freshwater mussels. One of Japan's most beautiful small fish.",
    },
    "medaka": {
        "name": "Medaka",
        "rarity_pool": ["common", "common", "common", "uncommon"],
        "habitat": "river",
        "biome_affinity": ["temperate", "rolling_hills", "wetland"],
        "weight_range": (0.001, 0.005),
        "length_range": (2, 4),
        "pattern_pool": ["plain", "spotted"],
        "colors": [
            ((235, 195, 120), (195, 158, 88)),
            ((225, 185, 110), (185, 148, 78)),
        ],
        "description": "A tiny golden killifish of rice paddies and sun-warmed ditches. A symbol of Japan's rural waterways.",
    },
    "gibuna": {
        "name": "Gibuna",
        "rarity_pool": ["common", "common", "uncommon"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "rolling_hills", "birch_forest"],
        "weight_range": (0.1, 0.9),
        "length_range": (15, 32),
        "pattern_pool": ["plain", "scaled"],
        "colors": [
            ((205, 185, 115), (152, 135, 82)),
            ((215, 195, 125), (162, 145, 90)),
        ],
        "description": "Japan's common crucian carp. Familiar in ponds and slow rivers, it has coexisted with people for centuries.",
    },
    "higai": {
        "name": "Higai",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "river",
        "biome_affinity": ["temperate", "rolling_hills"],
        "weight_range": (0.02, 0.15),
        "length_range": (8, 20),
        "pattern_pool": ["plain", "banded"],
        "colors": [
            ((155, 165, 115), (105, 112, 72)),
            ((145, 155, 108), (98, 105, 68)),
        ],
        "description": "A sleek golden-green cyprinid with an elegant profile. Found only in clear, well-oxygenated Japanese rivers.",
    },
    "striped_loach": {
        "name": "Striped Loach",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "river",
        "biome_affinity": ["temperate", "rolling_hills"],
        "weight_range": (0.005, 0.020),
        "length_range": (6, 12),
        "pattern_pool": ["striped", "plain"],
        "colors": [
            ((200, 178, 118), (48, 42, 32)),
            ((188, 168, 108), (42, 36, 28)),
        ],
        "description": "A small sand-dwelling loach with crisp parallel stripes. Burrows into clean gravel when disturbed.",
    },
    "dojou": {
        "name": "Dojou",
        "rarity_pool": ["common", "uncommon"],
        "habitat": "river",
        "biome_affinity": ["temperate", "wetland", "swamp"],
        "weight_range": (0.01, 0.08),
        "length_range": (8, 20),
        "pattern_pool": ["mottled", "plain"],
        "colors": [
            ((145, 118, 80), (98, 78, 50)),
            ((135, 108, 72), (88, 70, 45)),
        ],
        "description": "A whiskered pond loach that can breathe air and sense approaching storms. A beloved figure in Japanese folk culture.",
    },
    "namazu": {
        "name": "Namazu",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "wetland", "swamp"],
        "weight_range": (1.0, 7.0),
        "length_range": (40, 80),
        "pattern_pool": ["mottled", "plain"],
        "colors": [
            ((65, 80, 55), (195, 195, 172)),
            ((58, 72, 48), (185, 185, 162)),
        ],
        "description": "The Japanese catfish of legend. Said to thrash beneath the earth and cause earthquakes. Lurks in deep, muddy lake beds.",
    },
    "gigi": {
        "name": "Gigi",
        "rarity_pool": ["uncommon", "rare"],
        "habitat": "river",
        "biome_affinity": ["temperate", "wetland"],
        "weight_range": (0.05, 0.40),
        "length_range": (12, 30),
        "pattern_pool": ["plain", "mottled"],
        "colors": [
            ((72, 78, 88), (42, 45, 52)),
            ((65, 70, 80), (38, 40, 48)),
        ],
        "description": "A secretive torrent catfish that hides under boulders in fast, clear Japanese rivers. Rarely seen in daylight.",
    },
    "yamame": {
        "name": "Yamame",
        "rarity_pool": ["uncommon", "rare", "rare"],
        "habitat": "river",
        "biome_affinity": ["boreal", "temperate"],
        "weight_range": (0.2, 1.5),
        "length_range": (20, 45),
        "pattern_pool": ["spotted", "plain"],
        "colors": [
            ((168, 185, 152), (195, 95, 85)),
            ((155, 175, 140), (185, 88, 78)),
        ],
        "description": "Japan's beloved landlocked cherry salmon. Parr marks adorn its flanks year-round — a jewel of mountain rivers.",
    },
    "amago": {
        "name": "Amago",
        "rarity_pool": ["rare", "rare", "epic"],
        "habitat": "river",
        "biome_affinity": ["boreal", "temperate"],
        "weight_range": (0.15, 1.2),
        "length_range": (18, 40),
        "pattern_pool": ["spotted", "plain"],
        "colors": [
            ((145, 168, 118), (195, 55, 45)),
            ((135, 158, 108), (185, 48, 38)),
            ((155, 175, 128), (205, 62, 52)),
        ],
        "description": "A close cousin of the Yamame with brilliant crimson spots. Endemic to the clear rivers of western Japan.",
    },
    "iwana": {
        "name": "Iwana",
        "rarity_pool": ["uncommon", "rare", "rare"],
        "habitat": "river",
        "biome_affinity": ["boreal", "tundra"],
        "weight_range": (0.3, 3.0),
        "length_range": (25, 60),
        "pattern_pool": ["spotted", "mottled"],
        "colors": [
            ((58, 78, 62), (225, 222, 215)),
            ((52, 70, 55), (215, 212, 205)),
            ((65, 85, 68), (232, 228, 220)),
        ],
        "description": "Japan's native char of cold headwater streams. Its ghostly white spots glow against a dark body in crystal water.",
    },
    "ugui": {
        "name": "Ugui",
        "rarity_pool": ["common", "common", "uncommon"],
        "habitat": "river",
        "biome_affinity": ["boreal", "temperate", "rolling_hills"],
        "weight_range": (0.05, 0.8),
        "length_range": (15, 35),
        "pattern_pool": ["plain", "striped"],
        "colors": [
            ((185, 195, 205), (195, 118, 108)),
            ((178, 188, 198), (185, 108, 98)),
        ],
        "description": "Japan's most common river fish, found from Okinawa to Hokkaido. Spawning males flash a vivid pinkish-red lateral stripe.",
    },
    "itou": {
        "name": "Itou",
        "rarity_pool": ["epic", "epic", "legendary"],
        "habitat": "river",
        "biome_affinity": ["boreal", "tundra"],
        "weight_range": (15.0, 60.0),
        "length_range": (100, 180),
        "pattern_pool": ["spotted", "mottled"],
        "colors": [
            ((78, 108, 72), (165, 88, 55)),
            ((70, 98, 65), (155, 80, 48)),
        ],
        "description": "Japan's largest salmonid and rarest freshwater fish. A ghost of Hokkaido's wild rivers, it may live over fifty years.",
    },
    "sakura_masu": {
        "name": "Sakura Masu",
        "rarity_pool": ["rare", "rare", "epic"],
        "habitat": "river",
        "biome_affinity": ["boreal", "tundra"],
        "weight_range": (1.5, 7.0),
        "length_range": (45, 75),
        "pattern_pool": ["plain", "spotted"],
        "colors": [
            ((205, 195, 210), (195, 115, 135)),
            ((215, 205, 218), (205, 125, 148)),
            ((188, 162, 178), (175, 95, 118)),
        ],
        "description": "The cherry salmon in its sea-run form. Returns to cold northern rivers flushed with the soft pink hues of spring blossoms.",
    },
    "shishamo": {
        "name": "Shishamo",
        "rarity_pool": ["common", "common", "uncommon"],
        "habitat": "river",
        "biome_affinity": ["boreal", "tundra"],
        "weight_range": (0.02, 0.08),
        "length_range": (10, 18),
        "pattern_pool": ["plain", "striped"],
        "colors": [
            ((195, 208, 200), (132, 148, 138)),
            ((185, 198, 192), (122, 138, 128)),
        ],
        "description": "A small silver smelt that runs into cold Hokkaido rivers to spawn. Beloved whole-grilled in Japanese cuisine.",
    },
    "aburahaya": {
        "name": "Aburahaya",
        "rarity_pool": ["common", "uncommon", "uncommon"],
        "habitat": "river",
        "biome_affinity": ["boreal", "temperate"],
        "weight_range": (0.02, 0.12),
        "length_range": (8, 18),
        "pattern_pool": ["plain", "mottled"],
        "colors": [
            ((138, 125, 88), (82, 72, 48)),
            ((148, 135, 95), (90, 80, 55)),
        ],
        "description": "A small, fat-bellied minnow of mountain streams. Adaptable and hardy, it thrives in fast, cold water.",
    },
    "japanese_eel": {
        "name": "Japanese Eel",
        "rarity_pool": ["rare", "rare", "epic", "legendary"],
        "habitat": "river",
        "biome_affinity": ["temperate", "wetland"],
        "weight_range": (0.5, 2.5),
        "length_range": (40, 90),
        "pattern_pool": ["plain", "mottled"],
        "colors": [
            ((62, 78, 52), (195, 188, 125)),
            ((55, 70, 45), (185, 178, 115)),
        ],
        "description": "The unagi of Japanese cuisine. Spawns deep in the Pacific and returns to rivers to grow for decades. Now critically rare.",
    },
    "biwamasu": {
        "name": "Biwamasu",
        "rarity_pool": ["rare", "rare", "epic"],
        "habitat": "lake",
        "biome_affinity": ["temperate", "boreal"],
        "weight_range": (0.8, 3.5),
        "length_range": (35, 60),
        "pattern_pool": ["spotted", "plain"],
        "colors": [
            ((195, 185, 215), (88, 62, 108)),
            ((185, 175, 205), (78, 55, 98)),
            ((175, 165, 195), (68, 48, 88)),
        ],
        "description": "A landlocked salmon found only in Lake Biwa, Japan's oldest and largest lake. Its violet-silver sheen is unmistakable.",
    },

    # ------------------------------------------------------------------
    # Ocean — Reef zone (y 60–95)
    # ------------------------------------------------------------------
    "clownfish": {
        "name": "Clownfish",
        "rarity_pool": ["uncommon", "uncommon", "rare"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "reef",
        "weight_range": (0.05, 0.25),
        "length_range": (6, 14),
        "pattern_pool": ["banded", "striped"],
        "colors": [
            ((230, 100, 30), (250, 250, 250)),
            ((215, 85, 20),  (240, 240, 240)),
        ],
        "description": "A bold orange fish that shelters among sea anemone tentacles. Immune to their sting.",
    },
    "moorish_idol": {
        "name": "Moorish Idol",
        "rarity_pool": ["uncommon", "rare", "rare"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "reef",
        "weight_range": (0.10, 0.40),
        "length_range": (12, 22),
        "pattern_pool": ["banded", "striped"],
        "colors": [
            ((230, 200, 50), (30, 30, 30)),
            ((240, 210, 60), (40, 40, 40)),
        ],
        "description": "A striking disc-shaped fish with dramatic black, white, and yellow bands and an elongated dorsal spine.",
    },
    "lionfish": {
        "name": "Lionfish",
        "rarity_pool": ["uncommon", "rare", "rare", "epic"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "reef",
        "weight_range": (0.20, 1.20),
        "length_range": (15, 38),
        "pattern_pool": ["striped", "banded"],
        "colors": [
            ((200, 50, 50),  (245, 240, 220)),
            ((180, 40, 40),  (235, 225, 200)),
            ((210, 80, 110), (240, 230, 210)),
        ],
        "description": "A venomous ambush predator with fan-like spines. Beautiful and dangerous in equal measure.",
    },
    "parrotfish_reef": {
        "name": "Reef Parrotfish",
        "rarity_pool": ["uncommon", "uncommon", "rare"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "reef",
        "weight_range": (0.40, 4.00),
        "length_range": (25, 65),
        "pattern_pool": ["mottled", "plain"],
        "colors": [
            ((50, 180, 140),  (210, 90, 130)),
            ((60, 190, 155),  (190, 80, 115)),
            ((80, 160, 200),  (200, 110, 60)),
        ],
        "description": "A vivid reef fish that bites off chunks of coral and excretes white sand. Responsible for much of the beach you walk on.",
    },
    "grouper": {
        "name": "Grouper",
        "rarity_pool": ["common", "common", "uncommon", "rare"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "reef",
        "weight_range": (0.80, 12.0),
        "length_range": (30, 90),
        "pattern_pool": ["mottled", "spotted", "plain"],
        "colors": [
            ((130, 95, 60),  (80, 55, 35)),
            ((115, 85, 55),  (70, 48, 30)),
            ((145, 110, 70), (90, 62, 40)),
        ],
        "description": "A powerful reef ambush predator. Can swallow prey nearly its own size. Highly prized as food fish.",
    },
    "blue_tang": {
        "name": "Blue Tang",
        "rarity_pool": ["uncommon", "uncommon", "rare"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "reef",
        "weight_range": (0.15, 0.60),
        "length_range": (15, 31),
        "pattern_pool": ["plain", "spotted"],
        "colors": [
            ((40, 100, 210),  (230, 180, 30)),
            ((50, 115, 225),  (240, 190, 40)),
        ],
        "description": "A vivid electric-blue surgeonfish with a sharp spine near the tail. Grazes algae off reef surfaces.",
    },
    "damselfish": {
        "name": "Damselfish",
        "rarity_pool": ["common", "common", "uncommon"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "reef",
        "weight_range": (0.04, 0.18),
        "length_range": (5, 12),
        "pattern_pool": ["plain", "spotted"],
        "colors": [
            ((70, 120, 200), (230, 190, 60)),
            ((60, 100, 185), (215, 175, 50)),
            ((90, 140, 210), (220, 180, 55)),
        ],
        "description": "A feisty little reef fish that aggressively guards patches of algae it farms on the coral surface.",
    },
    "wrasse": {
        "name": "Wrasse",
        "rarity_pool": ["uncommon", "uncommon", "rare"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "reef",
        "weight_range": (0.10, 2.50),
        "length_range": (10, 50),
        "pattern_pool": ["striped", "spotted", "plain"],
        "colors": [
            ((130, 70, 170), (60, 150, 100)),
            ((100, 60, 145), (70, 160, 110)),
            ((155, 80, 190), (50, 140, 90)),
        ],
        "description": "A diverse family of slender, often brilliantly colored reef fish. Many act as dedicated parasite cleaners for larger species.",
    },
    "hawksbill_companion": {
        "name": "Remora",
        "rarity_pool": ["rare", "rare", "epic"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "reef",
        "weight_range": (0.20, 1.00),
        "length_range": (20, 45),
        "pattern_pool": ["plain", "striped"],
        "colors": [
            ((90, 140, 80),  (110, 75, 40)),
            ((80, 125, 70),  (100, 65, 35)),
        ],
        "description": "A sleek fish with a suction disc on its head. Hitches rides on sea turtles and sharks, feeding on scraps.",
    },
    "sergeant_major": {
        "name": "Sergeant Major",
        "rarity_pool": ["common", "common", "uncommon"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "reef",
        "weight_range": (0.08, 0.30),
        "length_range": (9, 18),
        "pattern_pool": ["banded", "striped"],
        "colors": [
            ((220, 200, 50), (40, 40, 40)),
            ((210, 190, 45), (35, 35, 35)),
        ],
        "description": "A boldly striped damselfish named for its rank-like bars. Forms dense schools around reef edges.",
    },

    # ------------------------------------------------------------------
    # Ocean — Twilight zone (y 95–155)
    # ------------------------------------------------------------------
    "lanternfish": {
        "name": "Lanternfish",
        "rarity_pool": ["common", "common", "uncommon"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "twilight",
        "weight_range": (0.01, 0.07),
        "length_range": (3, 10),
        "pattern_pool": ["plain", "spotted"],
        "colors": [
            ((170, 180, 195), (80, 90, 110)),
            ((155, 165, 180), (70, 80, 100)),
        ],
        "description": "A tiny deep-water fish with rows of photophores along its belly. Billions migrate vertically each night — the largest mass movement on Earth.",
    },
    "flashlight_fish": {
        "name": "Flashlight Fish",
        "rarity_pool": ["uncommon", "rare", "rare"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "twilight",
        "weight_range": (0.05, 0.20),
        "length_range": (8, 14),
        "pattern_pool": ["plain", "mottled"],
        "colors": [
            ((30, 80, 100),  (140, 230, 220)),
            ((25, 70, 88),   (120, 215, 205)),
        ],
        "description": "Carries a light-producing organ beneath each eye. Blinks by rotating the organ inward to hide it. Uses the light to hunt and communicate.",
    },
    "oarfish": {
        "name": "Oarfish",
        "rarity_pool": ["rare", "epic", "epic", "legendary"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "twilight",
        "weight_range": (100.0, 270.0),
        "length_range": (300, 1100),
        "pattern_pool": ["plain", "striped"],
        "colors": [
            ((200, 205, 215), (200, 60, 80)),
            ((190, 195, 210), (185, 50, 70)),
        ],
        "description": "The world's longest bony fish. A silvery ribbon up to 11 metres long with a vivid crimson dorsal fin. The origin of many sea-serpent legends.",
        "tension": 3.5,
    },
    "leafy_sea_dragon": {
        "name": "Leafy Sea Dragon",
        "rarity_pool": ["epic", "epic", "legendary"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "twilight",
        "weight_range": (0.08, 0.18),
        "length_range": (20, 35),
        "pattern_pool": ["mottled", "plain"],
        "colors": [
            ((100, 155, 90),  (170, 110, 60)),
            ((110, 165, 100), (160, 100, 55)),
        ],
        "description": "An elaborate pipefish relative draped in leaf-like appendages for camouflage. Males carry the eggs. A living work of art.",
    },
    "banded_sea_krait": {
        "name": "Banded Sea Krait",
        "rarity_pool": ["rare", "rare", "epic"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "twilight",
        "weight_range": (0.30, 0.90),
        "length_range": (80, 150),
        "pattern_pool": ["banded", "striped"],
        "colors": [
            ((170, 190, 210), (35, 35, 40)),
            ((160, 180, 200), (30, 30, 38)),
        ],
        "description": "A venomous sea snake with striking black and blue-grey bands. Breathes air but hunts eels in reef crevices.",
    },
    "coelacanth": {
        "name": "Coelacanth",
        "rarity_pool": ["epic", "epic", "legendary"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "twilight",
        "weight_range": (40.0, 90.0),
        "length_range": (120, 195),
        "pattern_pool": ["spotted", "mottled"],
        "colors": [
            ((50, 70, 150),  (180, 185, 200)),
            ((45, 65, 140),  (170, 175, 190)),
        ],
        "description": "A 'living fossil' believed extinct for 65 million years until rediscovered in 1938. Swims with paired lobed fins that foreshadow the limbs of land animals.",
        "tension": 2.8,
    },

    # ------------------------------------------------------------------
    # Ocean — Deep zone (y 155+)
    # ------------------------------------------------------------------
    "anglerfish": {
        "name": "Anglerfish",
        "rarity_pool": ["rare", "rare", "epic"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "deep",
        "weight_range": (0.50, 5.00),
        "length_range": (10, 40),
        "pattern_pool": ["plain", "mottled"],
        "colors": [
            ((60, 40, 35),  (100, 230, 210)),
            ((50, 35, 30),  (90, 220, 200)),
        ],
        "description": "Uses a bioluminescent lure to attract prey in absolute darkness. The male is a parasitic nub fused to the female's body.",
    },
    "gulper_eel": {
        "name": "Gulper Eel",
        "rarity_pool": ["rare", "epic", "epic"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "deep",
        "weight_range": (0.20, 2.00),
        "length_range": (60, 200),
        "pattern_pool": ["plain", "striped"],
        "colors": [
            ((40, 40, 50),  (80, 50, 100)),
            ((35, 35, 45),  (70, 42, 88)),
        ],
        "description": "Its enormous hinged jaw can engulf prey much larger than itself. Whip-like tail tip glows to lure prey into the abyss.",
        "tension": 2.0,
    },
    "barreleye": {
        "name": "Barreleye",
        "rarity_pool": ["epic", "epic", "legendary"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "deep",
        "weight_range": (0.05, 0.25),
        "length_range": (10, 18),
        "pattern_pool": ["plain", "spotted"],
        "colors": [
            ((140, 160, 170), (60, 210, 140)),
            ((130, 150, 162), (55, 200, 130)),
        ],
        "description": "Has a transparent fluid-filled head and tubular green eyes that can rotate to look straight up through its own skull.",
    },
    "fangtooth": {
        "name": "Fangtooth",
        "rarity_pool": ["rare", "rare", "epic"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "deep",
        "weight_range": (0.08, 0.35),
        "length_range": (8, 18),
        "pattern_pool": ["plain", "mottled"],
        "colors": [
            ((45, 42, 48), (120, 30, 30)),
            ((40, 38, 44), (110, 25, 25)),
        ],
        "description": "Pound for pound, the most fearsome teeth of any fish. Its fangs are so long they fit into sheaths beside its brain when the jaw closes.",
        "tension": 1.8,
    },

    # ------------------------------------------------------------------
    # Ocean — Reef zone (additional)
    # ------------------------------------------------------------------
    "butterflyfish": {
        "name": "Butterflyfish",
        "rarity_pool": ["uncommon", "uncommon", "rare"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "reef",
        "weight_range": (0.05, 0.30),
        "length_range": (8, 22),
        "pattern_pool": ["banded", "spotted"],
        "colors": [
            ((230, 210, 50),  (245, 245, 245)),
            ((220, 190, 40),  (240, 240, 240)),
            ((210, 170, 30),  (60, 60, 60)),
        ],
        "description": "A flattened disc-shaped reef fish with vivid patterns. Pairs mate for life and patrol the same coral head together.",
    },
    "ocean_angelfish": {
        "name": "Angelfish",
        "rarity_pool": ["uncommon", "rare", "rare"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "reef",
        "weight_range": (0.20, 1.80),
        "length_range": (18, 45),
        "pattern_pool": ["striped", "banded"],
        "colors": [
            ((50, 90, 190),   (220, 175, 40)),
            ((60, 100, 205),  (235, 185, 50)),
            ((80, 60, 170),   (210, 170, 40)),
        ],
        "description": "Tall and slow-moving, with sweeping fins and vivid bands. A reef sentinel that fearlessly approaches divers.",
    },
    "trumpetfish": {
        "name": "Trumpetfish",
        "rarity_pool": ["uncommon", "uncommon", "rare"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "reef",
        "weight_range": (0.15, 0.70),
        "length_range": (40, 90),
        "pattern_pool": ["plain", "striped"],
        "colors": [
            ((160, 150, 100), (120, 110, 65)),
            ((195, 170, 55),  (145, 120, 35)),
            ((100, 140, 115), (65, 100, 80)),
        ],
        "description": "A slender ambush predator that drifts vertically among coral branches, disguised as a stem. Strikes with a vacuum-pump mouth.",
    },
    "barracuda": {
        "name": "Barracuda",
        "rarity_pool": ["uncommon", "rare", "rare", "epic"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "reef",
        "weight_range": (1.00, 10.0),
        "length_range": (60, 180),
        "pattern_pool": ["plain", "striped"],
        "colors": [
            ((180, 185, 195), (70, 75, 90)),
            ((170, 175, 185), (60, 65, 80)),
        ],
        "description": "A torpedo-shaped apex predator with a mouthful of dagger teeth. Hunts by explosive bursts of speed, not stealth.",
        "tension": 2.5,
    },
    "moray_eel": {
        "name": "Moray Eel",
        "rarity_pool": ["uncommon", "rare", "rare"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "reef",
        "weight_range": (0.50, 8.00),
        "length_range": (50, 180),
        "pattern_pool": ["spotted", "mottled"],
        "colors": [
            ((80, 120, 60),  (200, 185, 120)),
            ((60, 90, 45),   (185, 170, 105)),
            ((140, 120, 50), (195, 180, 110)),
        ],
        "description": "A muscular, snake-like predator that lurks in coral crevices. Has a second set of jaws in its throat that reaches forward to grip prey.",
        "tension": 1.8,
    },
    "goatfish": {
        "name": "Goatfish",
        "rarity_pool": ["common", "common", "uncommon"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "reef",
        "weight_range": (0.10, 0.80),
        "length_range": (15, 35),
        "pattern_pool": ["plain", "striped"],
        "colors": [
            ((200, 80, 60),  (240, 235, 225)),
            ((185, 65, 50),  (235, 228, 215)),
            ((215, 100, 80), (245, 240, 230)),
        ],
        "description": "Roots through sandy reef floors with two chin barbels to flush out hidden worms and crustaceans. Named for its resemblance to a goat's beard.",
    },
    "humphead_wrasse": {
        "name": "Humphead Wrasse",
        "rarity_pool": ["rare", "rare", "epic", "legendary"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "reef",
        "weight_range": (5.0, 30.0),
        "length_range": (80, 230),
        "pattern_pool": ["mottled", "plain"],
        "colors": [
            ((60, 140, 130),  (40, 95, 88)),
            ((70, 155, 145),  (50, 105, 98)),
        ],
        "description": "The largest of all wrasse — a massive blue-green giant with a distinctive hump on its forehead. Can live over 30 years. Now critically endangered.",
        "tension": 2.0,
    },
    "rabbitfish": {
        "name": "Rabbitfish",
        "rarity_pool": ["common", "common", "uncommon"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "reef",
        "weight_range": (0.20, 1.20),
        "length_range": (20, 42),
        "pattern_pool": ["spotted", "mottled"],
        "colors": [
            ((170, 155, 85), (130, 115, 55)),
            ((180, 165, 95), (140, 125, 65)),
            ((155, 140, 75), (115, 100, 48)),
        ],
        "description": "A reef grazer with a blunt snout and venomous dorsal spines. Travels in tight schools that strip algae from coral in synchronized sweeps.",
    },
    "sohal_surgeonfish": {
        "name": "Sohal Surgeonfish",
        "rarity_pool": ["uncommon", "rare", "rare"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "reef",
        "weight_range": (0.20, 0.90),
        "length_range": (20, 40),
        "pattern_pool": ["striped", "plain"],
        "colors": [
            ((50, 110, 200), (220, 120, 40)),
            ((45, 100, 190), (210, 110, 35)),
        ],
        "description": "An electric-blue surgeonfish with a vivid orange streak along its flank. Fiercely territorial on Red Sea reefs; will charge fish twice its size.",
    },
    "scorpionfish": {
        "name": "Scorpionfish",
        "rarity_pool": ["uncommon", "uncommon", "rare"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "reef",
        "weight_range": (0.30, 2.50),
        "length_range": (20, 55),
        "pattern_pool": ["mottled", "spotted"],
        "colors": [
            ((160, 70, 50),  (110, 85, 65)),
            ((140, 55, 40),  (95, 72, 55)),
            ((175, 100, 70), (125, 95, 70)),
        ],
        "description": "A master of camouflage that blends perfectly with coral rubble. Its dorsal spines deliver a venom so potent it can cause temporary paralysis.",
    },

    # ------------------------------------------------------------------
    # Ocean — Twilight zone (additional)
    # ------------------------------------------------------------------
    "hatchetfish": {
        "name": "Marine Hatchetfish",
        "rarity_pool": ["common", "common", "uncommon"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "twilight",
        "weight_range": (0.005, 0.04),
        "length_range": (3, 8),
        "pattern_pool": ["plain", "spotted"],
        "colors": [
            ((195, 200, 210), (50, 55, 75)),
            ((185, 190, 200), (45, 50, 70)),
        ],
        "description": "Paper-thin and intensely silvery, with a row of photophores along its belly that match downwelling light — making it invisible from below.",
    },
    "viperfish": {
        "name": "Pacific Viperfish",
        "rarity_pool": ["uncommon", "rare", "rare"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "twilight",
        "weight_range": (0.10, 0.35),
        "length_range": (20, 35),
        "pattern_pool": ["plain", "striped"],
        "colors": [
            ((55, 55, 70), (180, 220, 215)),
            ((48, 50, 65), (165, 205, 200)),
        ],
        "description": "Has fangs so long they can never fully close its mouth. Lures prey with a photophore on the tip of its elongated first dorsal ray.",
    },
    "ribbonfish_ocean": {
        "name": "Ribbonfish",
        "rarity_pool": ["uncommon", "uncommon", "rare"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "twilight",
        "weight_range": (0.50, 4.00),
        "length_range": (60, 200),
        "pattern_pool": ["plain", "striped"],
        "colors": [
            ((205, 210, 220), (150, 155, 170)),
            ((195, 200, 212), (140, 145, 160)),
        ],
        "description": "A flattened silver ribbon of a fish that swims vertically through the mesopelagic zone. Relative of the oarfish but far less rare.",
    },
    "rattail": {
        "name": "Rattail",
        "rarity_pool": ["common", "common", "uncommon"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "twilight",
        "weight_range": (0.20, 1.50),
        "length_range": (30, 80),
        "pattern_pool": ["plain", "mottled"],
        "colors": [
            ((130, 125, 140), (90, 85, 100)),
            ((120, 115, 130), (82, 78, 92)),
        ],
        "description": "Also called a grenadier — a heavy-headed fish with a body that tapers to a whip-like tail. The most abundant deep-water fish family on Earth.",
    },
    "ghost_shark": {
        "name": "Ghost Shark",
        "rarity_pool": ["rare", "rare", "epic"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "twilight",
        "weight_range": (1.00, 5.00),
        "length_range": (60, 120),
        "pattern_pool": ["plain", "spotted"],
        "colors": [
            ((215, 215, 220), (160, 160, 170)),
            ((205, 205, 212), (150, 150, 162)),
        ],
        "description": "Not a true shark but a chimera — a ghostly cartilaginous fish with a venomous spine and iridescent skin that shimmers like mother-of-pearl.",
    },
    "black_dragonfish": {
        "name": "Black Dragonfish",
        "rarity_pool": ["rare", "rare", "epic"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "twilight",
        "weight_range": (0.02, 0.12),
        "length_range": (15, 40),
        "pattern_pool": ["plain", "striped"],
        "colors": [
            ((30, 30, 38),  (120, 210, 190)),
            ((25, 25, 32),  (100, 195, 175)),
        ],
        "description": "Iridescent black scales absorb nearly all light. The female — ten times larger than the male — hunts with a glowing chin barbel in absolute darkness.",
    },
    "stoplight_loosejaw": {
        "name": "Stoplight Loosejaw",
        "rarity_pool": ["uncommon", "rare", "rare"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "twilight",
        "weight_range": (0.02, 0.08),
        "length_range": (12, 28),
        "pattern_pool": ["plain", "mottled"],
        "colors": [
            ((120, 30, 30), (60, 200, 80)),
            ((110, 25, 25), (50, 185, 70)),
        ],
        "description": "Emits both red and green bioluminescence — a unique trick since most deep-sea creatures are blind to red light. Its open-frame jaw can fold flat.",
    },
    "sabertooth_fish": {
        "name": "Sabertooth Fish",
        "rarity_pool": ["uncommon", "rare", "rare"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "twilight",
        "weight_range": (0.08, 0.40),
        "length_range": (15, 35),
        "pattern_pool": ["plain", "mottled"],
        "colors": [
            ((65, 70, 90),  (190, 200, 215)),
            ((58, 62, 82),  (178, 188, 205)),
        ],
        "description": "Transparent, recurved fangs grip prey without puncturing the skull — they fold back when the mouth closes. Ambushes with a burst of speed.",
    },
    "frilled_shark": {
        "name": "Frilled Shark",
        "rarity_pool": ["rare", "epic", "epic"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "twilight",
        "weight_range": (80.0, 200.0),
        "length_range": (130, 200),
        "pattern_pool": ["plain", "mottled"],
        "colors": [
            ((100, 95, 110), (155, 150, 165)),
            ((92, 88, 102),  (145, 140, 155)),
        ],
        "description": "An ancient shark lineage unchanged for 80 million years. Six frilled gill slits and a serpentine body make it look more like an eel than a shark.",
        "tension": 2.5,
    },

    # ------------------------------------------------------------------
    # Ocean — Deep zone (additional)
    # ------------------------------------------------------------------
    "blobfish": {
        "name": "Blobfish",
        "rarity_pool": ["common", "uncommon", "uncommon"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "deep",
        "weight_range": (2.00, 5.00),
        "length_range": (25, 35),
        "pattern_pool": ["plain", "mottled"],
        "colors": [
            ((215, 175, 170), (180, 140, 135)),
            ((205, 165, 160), (170, 130, 125)),
        ],
        "description": "At crushing deep-sea pressure, it is an unremarkable fish. Hauled to the surface, its flesh decompresses into an infamous gelatinous blob.",
    },
    "pelican_eel": {
        "name": "Pelican Eel",
        "rarity_pool": ["rare", "epic", "epic"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "deep",
        "weight_range": (0.10, 0.60),
        "length_range": (60, 100),
        "pattern_pool": ["plain", "striped"],
        "colors": [
            ((45, 42, 55),  (190, 80, 60)),
            ((38, 36, 48),  (175, 70, 52)),
        ],
        "description": "Its enormous hinged mouth pouch — larger than its entire body — inflates like a net to engulf schools of prey. A glowing pink tail tip serves as a lure.",
        "tension": 1.6,
    },
    "footballfish": {
        "name": "Football Fish",
        "rarity_pool": ["epic", "epic", "legendary"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "deep",
        "weight_range": (1.00, 6.00),
        "length_range": (15, 60),
        "pattern_pool": ["plain", "spotted"],
        "colors": [
            ((65, 45, 40),  (220, 210, 100)),
            ((58, 40, 36),  (210, 198, 90)),
        ],
        "description": "A round anglerfish with an elaborate bioluminescent lure on a long stalk. One of the rarest sights in the deep — fewer than 30 have ever been collected.",
    },
    "black_swallower": {
        "name": "Black Swallower",
        "rarity_pool": ["rare", "rare", "epic"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "deep",
        "weight_range": (0.02, 0.15),
        "length_range": (10, 25),
        "pattern_pool": ["plain", "mottled"],
        "colors": [
            ((35, 38, 45), (70, 65, 80)),
            ((30, 33, 40), (62, 58, 72)),
        ],
        "description": "A tiny fish capable of swallowing prey ten times its own mass. Its stomach can expand to many times its body size — sometimes with fatal results.",
    },
    "tripod_fish": {
        "name": "Tripod Fish",
        "rarity_pool": ["rare", "epic", "legendary"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "deep",
        "weight_range": (0.10, 0.30),
        "length_range": (30, 45),
        "pattern_pool": ["plain", "mottled"],
        "colors": [
            ((105, 100, 115), (160, 155, 170)),
            ((98, 93, 108),   (150, 145, 162)),
        ],
        "description": "Stands motionless on three elongated fin rays on the abyssal floor, facing the current with pectoral fins spread to funnel drifting food into its mouth.",
    },
    "spookfish": {
        "name": "Spookfish",
        "rarity_pool": ["epic", "epic", "legendary"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "deep",
        "weight_range": (0.01, 0.05),
        "length_range": (4, 9),
        "pattern_pool": ["plain", "spotted"],
        "colors": [
            ((145, 155, 165), (80, 130, 160)),
            ((135, 145, 155), (70, 120, 150)),
        ],
        "description": "The only vertebrate known to use mirrors — not lenses — to focus light in its eyes. Four tube-eyes point up, down, forward, and sideways simultaneously.",
    },

    # ------------------------------------------------------------------
    # Ocean — Reef zone (additional 2)
    # ------------------------------------------------------------------
    "pufferfish": {
        "name": "Pufferfish",
        "rarity_pool": ["uncommon", "uncommon", "rare"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "reef",
        "weight_range": (0.30, 2.50),
        "length_range": (20, 60),
        "pattern_pool": ["spotted", "plain"],
        "colors": [
            ((150, 155, 90),  (220, 205, 120)),
            ((130, 140, 75),  (200, 190, 105)),
            ((160, 145, 80),  (225, 210, 128)),
        ],
        "description": "When threatened, gulps water to inflate into a spiky ball three times its resting size. Its organs contain tetrodotoxin — one of the most potent toxins known.",
    },
    "boxfish": {
        "name": "Boxfish",
        "rarity_pool": ["common", "uncommon", "uncommon"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "reef",
        "weight_range": (0.10, 0.80),
        "length_range": (10, 30),
        "pattern_pool": ["spotted", "plain"],
        "colors": [
            ((220, 185, 40), (30, 30, 30)),
            ((200, 165, 30), (25, 25, 25)),
            ((90, 145, 190), (30, 30, 30)),
        ],
        "description": "Encased in a rigid bony box, it swims by fluttering its small fins like a helicopter. When stressed it releases a toxin that kills everything in a tank — including itself.",
    },
    "needlefish": {
        "name": "Needlefish",
        "rarity_pool": ["common", "common", "uncommon"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "reef",
        "weight_range": (0.10, 1.20),
        "length_range": (30, 90),
        "pattern_pool": ["plain", "striped"],
        "colors": [
            ((170, 195, 185), (120, 150, 140)),
            ((160, 185, 175), (110, 142, 132)),
        ],
        "description": "A slender surface predator with a beak full of needle-like teeth. Leaps from the water when startled — its bony bill can impale and has killed swimmers.",
    },
    "achilles_tang": {
        "name": "Achilles Tang",
        "rarity_pool": ["rare", "rare", "epic"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "reef",
        "weight_range": (0.10, 0.50),
        "length_range": (15, 30),
        "pattern_pool": ["plain", "spotted"],
        "colors": [
            ((35, 35, 40),  (220, 110, 40)),
            ((30, 30, 36),  (210, 100, 35)),
        ],
        "description": "Jet-black with a vivid teardrop of orange framing its tail spine — named for the mythological warrior's fatal heel. A prized and difficult reef fish.",
    },
    "hawkfish": {
        "name": "Hawkfish",
        "rarity_pool": ["uncommon", "uncommon", "rare"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "reef",
        "weight_range": (0.05, 0.35),
        "length_range": (8, 25),
        "pattern_pool": ["spotted", "mottled"],
        "colors": [
            ((180, 85, 50),  (230, 210, 180)),
            ((165, 72, 42),  (220, 200, 170)),
            ((155, 65, 38),  (210, 190, 160)),
        ],
        "description": "Perches motionless on coral heads, gripping with thickened pectoral fins, then dives like a hawk onto passing shrimps and small fish.",
    },
    "filefish": {
        "name": "Filefish",
        "rarity_pool": ["common", "common", "uncommon"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "reef",
        "weight_range": (0.10, 2.00),
        "length_range": (15, 60),
        "pattern_pool": ["mottled", "spotted", "plain"],
        "colors": [
            ((140, 130, 100), (100, 90, 65)),
            ((130, 120, 90),  (92, 82, 58)),
            ((155, 140, 108), (108, 98, 72)),
        ],
        "description": "Skin as rough as sandpaper, a retractable locking dorsal spine, and a tiny mouth specialized for nipping coral polyps. Can rapidly shift colour to match its background.",
    },
    "coral_grouper": {
        "name": "Coral Grouper",
        "rarity_pool": ["rare", "rare", "epic"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "reef",
        "weight_range": (0.50, 8.00),
        "length_range": (35, 100),
        "pattern_pool": ["spotted", "plain"],
        "colors": [
            ((200, 45, 45),  (80, 160, 230)),
            ((185, 38, 38),  (70, 148, 218)),
        ],
        "description": "Scarlet body blazing with electric-blue spots. Hunts cooperatively with moray eels — one drives prey into the open, the other cuts off escape into crevices.",
    },
    "blacktip_reef_shark": {
        "name": "Blacktip Reef Shark",
        "rarity_pool": ["rare", "epic", "epic", "legendary"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "reef",
        "weight_range": (10.0, 30.0),
        "length_range": (120, 200),
        "pattern_pool": ["plain", "striped"],
        "colors": [
            ((140, 140, 150), (30, 30, 35)),
            ((130, 130, 140), (25, 25, 30)),
        ],
        "description": "The iconic shallow-reef shark — grey above, white below, each fin tipped with black. Timid but fast; often the first shark a diver will ever encounter.",
        "tension": 3.0,
    },
    "spotted_drum": {
        "name": "Spotted Drum",
        "rarity_pool": ["uncommon", "rare", "rare"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "reef",
        "weight_range": (0.20, 1.00),
        "length_range": (20, 40),
        "pattern_pool": ["spotted", "striped"],
        "colors": [
            ((35, 35, 38),  (245, 245, 240)),
            ((30, 30, 34),  (240, 240, 235)),
        ],
        "description": "A strikingly patterned reef fish with a dramatically elongated first dorsal fin. Juveniles swim in tight spirals around coral heads. Makes a loud drumming sound.",
    },
    "tilefish": {
        "name": "Tilefish",
        "rarity_pool": ["uncommon", "uncommon", "rare"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "reef",
        "weight_range": (0.50, 10.0),
        "length_range": (40, 120),
        "pattern_pool": ["spotted", "plain"],
        "colors": [
            ((60, 130, 170),  (220, 180, 50)),
            ((55, 120, 158),  (210, 168, 44)),
            ((70, 140, 180),  (230, 190, 58)),
        ],
        "description": "Excavates elaborate burrow systems in sandy reef edges that shelter dozens of other species. Its vivid blue-green and gold colouring makes it unmistakable.",
    },

    # ------------------------------------------------------------------
    # Ocean — Twilight zone (additional 2)
    # ------------------------------------------------------------------
    "swordfish": {
        "name": "Swordfish",
        "rarity_pool": ["epic", "epic", "legendary"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "twilight",
        "weight_range": (50.0, 250.0),
        "length_range": (200, 450),
        "pattern_pool": ["plain", "striped"],
        "colors": [
            ((65, 80, 120),  (185, 188, 200)),
            ((58, 72, 110),  (175, 178, 192)),
        ],
        "description": "Uses its flat, elongated bill to slash through schools of fish at high speed, then circles back to eat the stunned. One of the fastest fish in the ocean.",
        "tension": 4.0,
    },
    "opah": {
        "name": "Opah",
        "rarity_pool": ["rare", "rare", "epic"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "twilight",
        "weight_range": (15.0, 80.0),
        "length_range": (100, 200),
        "pattern_pool": ["spotted", "plain"],
        "colors": [
            ((195, 55, 55),  (195, 195, 205)),
            ((185, 48, 48),  (185, 185, 195)),
        ],
        "description": "A warm-blooded fish — a rare trait among fish — giving it a speed advantage in cold mesopelagic water. Its vivid crimson and silver makes it look like a dropped Christmas ornament.",
    },
    "escolar": {
        "name": "Escolar",
        "rarity_pool": ["uncommon", "rare", "rare"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "twilight",
        "weight_range": (5.0, 25.0),
        "length_range": (100, 200),
        "pattern_pool": ["plain", "mottled"],
        "colors": [
            ((70, 65, 60),  (50, 45, 42)),
            ((65, 60, 55),  (44, 40, 37)),
        ],
        "description": "Dark and powerfully built, with flesh so rich in wax esters it cannot be fully digested. Some countries ban it entirely. Sold under names like 'white tuna.'",
    },
    "alfonsino": {
        "name": "Alfonsino",
        "rarity_pool": ["uncommon", "uncommon", "rare"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "twilight",
        "weight_range": (0.50, 3.00),
        "length_range": (30, 70),
        "pattern_pool": ["plain", "scaled"],
        "colors": [
            ((200, 55, 40),  (150, 35, 25)),
            ((188, 48, 35),  (140, 30, 22)),
        ],
        "description": "A deep-red snapper-like fish with outsized eyes adapted to the twilight zone. Highly prized in Japanese cuisine as kinmedai; often lives 50+ years.",
    },
    "longnose_lancetfish": {
        "name": "Longnose Lancetfish",
        "rarity_pool": ["uncommon", "rare", "rare"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "twilight",
        "weight_range": (2.00, 20.0),
        "length_range": (100, 215),
        "pattern_pool": ["plain", "striped"],
        "colors": [
            ((175, 178, 190), (35, 38, 55)),
            ((165, 168, 182), (30, 33, 50)),
        ],
        "description": "A spectacular mesopelagic predator with a sail-like dorsal fin, dagger-like fang teeth, and a gelatinous body that leaves it practically weightless in water.",
        "tension": 2.2,
    },
    "pineconefish": {
        "name": "Pineconefish",
        "rarity_pool": ["uncommon", "rare", "rare"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "twilight",
        "weight_range": (0.05, 0.40),
        "length_range": (8, 18),
        "pattern_pool": ["scaled", "plain"],
        "colors": [
            ((190, 160, 80), (60, 190, 80)),
            ((178, 148, 72), (52, 178, 72)),
        ],
        "description": "Armored in large interlocking scales like a pinecone, with bioluminescent organs on its lower jaw that host symbiotic glowing bacteria. Navigates reef caves in darkness.",
    },
    "orange_roughy": {
        "name": "Orange Roughy",
        "rarity_pool": ["rare", "rare", "epic"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "twilight",
        "weight_range": (1.50, 7.00),
        "length_range": (50, 75),
        "pattern_pool": ["plain", "scaled"],
        "colors": [
            ((215, 90, 45),  (160, 55, 28)),
            ((200, 82, 40),  (148, 50, 25)),
        ],
        "description": "Can live over 200 years — fish caught today may have hatched before Napoleon. Deep-sea trawling has devastated populations that took centuries to build.",
    },
    "slickhead": {
        "name": "Slickhead",
        "rarity_pool": ["common", "common", "uncommon"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "twilight",
        "weight_range": (0.10, 1.00),
        "length_range": (20, 50),
        "pattern_pool": ["plain", "mottled"],
        "colors": [
            ((120, 118, 135), (85, 82, 98)),
            ((112, 110, 126), (78, 76, 90)),
        ],
        "description": "A smooth-skinned, large-eyed mesopelagic fish with no scales on its head — giving it an oddly bald appearance. One of the most abundant mid-water fish families.",
    },
    "dealfish": {
        "name": "Dealfish",
        "rarity_pool": ["rare", "epic", "epic"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "twilight",
        "weight_range": (3.0, 30.0),
        "length_range": (100, 350),
        "pattern_pool": ["plain", "striped"],
        "colors": [
            ((195, 200, 210), (200, 40, 55)),
            ((188, 192, 202), (188, 35, 50)),
        ],
        "description": "A giant flattened silver fish with a vivid red dorsal fin running its entire length. A relative of the oarfish, rarely seen alive. Its stranded body inspired coastal omens of catastrophe.",
    },

    # ------------------------------------------------------------------
    # Ocean — Deep zone (additional 3)
    # ------------------------------------------------------------------
    "snipe_eel": {
        "name": "Snipe Eel",
        "rarity_pool": ["uncommon", "rare", "rare"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "deep",
        "weight_range": (0.05, 0.30),
        "length_range": (60, 150),
        "pattern_pool": ["plain", "striped"],
        "colors": [
            ((80, 85, 100),  (130, 135, 150)),
            ((72, 78, 92),   (122, 128, 142)),
        ],
        "description": "An impossibly slender eel with a beak that curves outward at the tip — so long the jaws cannot close. Drifts near-vertical in the abyss, trailing behind like a thread.",
    },
    "whalefish": {
        "name": "Whalefish",
        "rarity_pool": ["rare", "epic", "legendary"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "deep",
        "weight_range": (0.005, 0.02),
        "length_range": (3, 8),
        "pattern_pool": ["plain", "mottled"],
        "colors": [
            ((95, 88, 105),  (145, 138, 158)),
            ((88, 82, 98),   (136, 130, 148)),
        ],
        "description": "One of the strangest deep-sea fish: scaleless, with a huge gaping mouth, no teeth, and a lateral-line system so sensitive it hunts by detecting water pressure waves from copepods.",
    },
    "coffinfish": {
        "name": "Coffinfish",
        "rarity_pool": ["rare", "rare", "epic"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "deep",
        "weight_range": (0.10, 0.50),
        "length_range": (15, 25),
        "pattern_pool": ["plain", "mottled"],
        "colors": [
            ((190, 155, 145), (140, 108, 100)),
            ((178, 144, 134), (130, 100, 92)),
        ],
        "description": "A batfish that walks along the seafloor on stumpy pectoral fins. Can inflate itself with water like a pufferfish. Named for its flattened coffin-like shape.",
    },
    "telescope_fish": {
        "name": "Telescope Fish",
        "rarity_pool": ["epic", "epic", "legendary"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "deep",
        "weight_range": (0.02, 0.15),
        "length_range": (8, 20),
        "pattern_pool": ["plain", "spotted"],
        "colors": [
            ((50, 52, 68),  (30, 38, 55)),
            ((44, 46, 62),  (26, 33, 50)),
        ],
        "description": "Cylindrical and jet-dark, with huge forward-pointing eyes like telescopes. Has a transparent head through which its tubular eyes can be seen rotating to track bioluminescent prey.",
    },
    "medusafish": {
        "name": "Medusafish",
        "rarity_pool": ["uncommon", "rare", "rare"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "deep",
        "weight_range": (0.05, 0.50),
        "length_range": (10, 30),
        "pattern_pool": ["plain", "spotted"],
        "colors": [
            ((175, 185, 195), (120, 135, 150)),
            ((165, 175, 185), (112, 126, 140)),
        ],
        "description": "Juveniles shelter inside the stinging tentacles of jellyfish and siphonophores, acquiring immunity and a moving fortress. Adults descend into the deep, abandoning their host forever.",
    },
    "abyssal_grenadier": {
        "name": "Abyssal Grenadier",
        "rarity_pool": ["uncommon", "uncommon", "rare"],
        "habitat": "ocean",
        "biome_affinity": ["ocean"],
        "ocean_zone": "deep",
        "weight_range": (1.00, 6.00),
        "length_range": (60, 120),
        "pattern_pool": ["plain", "mottled"],
        "colors": [
            ((155, 148, 162), (110, 104, 118)),
            ((145, 138, 152), (102, 96, 110)),
        ],
        "description": "A deep-sea grenadier found at the very bottom of the ocean trenches. Feeds on organic particles raining down from above — the 'marine snow' of the abyss.",
    },
}

# Order for display in the fish codex (roughly by biome group, then rarity)
FISH_TYPE_ORDER = [
    # Universal
    "minnow", "dace", "stone_loach", "fathead_minnow", "bluntnose_minnow",
    "gudgeon", "bleak", "mottled_sculpin",
    # Temperate
    "perch", "yellow_perch", "bass", "smallmouth_bass", "white_bass", "striped_bass",
    "spotted_bass", "yellow_bass", "sunshine_bass", "white_perch",
    "bluegill", "sunfish", "pumpkinseed", "rock_bass", "redear_sunfish",
    "green_sunfish", "longear_sunfish", "redbreast_sunfish",
    "crappie", "white_crappie", "walleye", "sauger", "saugeye",
    "carp", "tench", "roach", "rudd", "chub", "bream",
    "bigmouth_buffalo", "smallmouth_buffalo", "white_sucker", "northern_hogsucker",
    "quillback", "shorthead_redhorse", "blue_sucker",
    "golden_shiner", "emerald_shiner", "spottail_shiner", "gizzard_shad", "threadfin_shad",
    "hornyhead_chub", "fallfish", "mosquitofish",
    "channel_catfish", "yellow_bullhead", "brown_bullhead", "black_bullhead",
    "freshwater_drum", "mooneye",
    "johnny_darter", "iowa_darter", "orangethroat_darter", "least_darter", "crystal_darter",
    "rainbow_darter", "logperch",
    "american_eel", "muskie", "tiger_muskie", "golden_koi",
    "creek_chub", "river_carpsucker", "spotted_sucker", "warpaint_shiner",
    # Cold
    "trout", "brown_trout", "brook_trout", "lake_trout", "arctic_char", "dolly_varden",
    "cutthroat_trout", "bull_trout", "splake", "tiger_trout",
    "grayling", "golden_trout",
    "kokanee", "coho_salmon", "salmon", "steelhead",
    "cisco", "lake_whitefish", "round_whitefish", "longnose_sucker", "burbot", "goldeye",
    "alewife", "rainbow_smelt", "trout_perch", "ruffe", "round_goby",
    "pike", "sturgeon",
    "pink_salmon", "chum_salmon", "lake_sculpin", "ninespine_stickleback",
    # Jungle/Tropical
    "tilapia", "cichlid", "discus", "oscar", "peacock_bass",
    "piranha", "tambaqui", "pacu", "catfish",
    "redtail_catfish", "electric_eel", "payara", "arapaima",
    "arowana", "goliath_tigerfish", "bichir", "giant_gourami", "rivulus",
    # Pacific
    "mahi_mahi", "parrotfish", "triggerfish", "flying_fish", "yellowfin_tuna",
    # Wetland/Swamp
    "warmouth", "flier", "dollar_sunfish", "pirate_perch", "mudskipper", "bowfin",
    "walking_catfish", "pickerel", "redfin_pickerel", "spotted_gar", "snakehead",
    "longnose_gar", "grass_carp", "flathead_catfish", "blue_catfish",
    "spotted_bullhead", "paddlefish", "gar", "alligator_gar",
    "chain_pickerel", "golden_topminnow", "cypress_darter", "swamp_eel",
    # Japan / East Asia
    "ayu", "oikawa", "tanago", "medaka", "gibuna", "higai",
    "striped_loach", "dojou", "namazu", "gigi",
    "yamame", "amago", "iwana", "ugui", "itou",
    "sakura_masu", "shishamo", "aburahaya", "japanese_eel", "biwamasu",
    # Ocean Reef
    "clownfish", "moorish_idol", "lionfish", "parrotfish_reef", "grouper",
    "blue_tang", "damselfish", "wrasse", "hawksbill_companion", "sergeant_major",
    "butterflyfish", "ocean_angelfish", "trumpetfish", "barracuda", "moray_eel",
    "goatfish", "humphead_wrasse", "rabbitfish", "sohal_surgeonfish", "scorpionfish",
    "pufferfish", "boxfish", "needlefish", "achilles_tang", "hawkfish",
    "filefish", "coral_grouper", "blacktip_reef_shark", "spotted_drum", "tilefish",
    # Ocean Twilight
    "lanternfish", "flashlight_fish", "oarfish", "leafy_sea_dragon",
    "banded_sea_krait", "coelacanth",
    "hatchetfish", "viperfish", "ribbonfish_ocean", "rattail", "ghost_shark",
    "black_dragonfish", "stoplight_loosejaw", "sabertooth_fish", "frilled_shark",
    "swordfish", "opah", "escolar", "alfonsino", "longnose_lancetfish",
    "pineconefish", "orange_roughy", "slickhead", "dealfish",
    # Ocean Deep
    "anglerfish", "gulper_eel", "barreleye", "fangtooth",
    "blobfish", "pelican_eel", "footballfish", "black_swallower", "tripod_fish", "spookfish",
    "snipe_eel", "whalefish", "coffinfish", "telescope_fish", "medusafish", "abyssal_grenadier",
]

FISH_RARITY_COLORS = {
    "common":    (160, 160, 180),
    "uncommon":  (80, 200, 120),
    "rare":      (80, 140, 220),
    "epic":      (160, 80, 220),
    "legendary": (255, 180, 0),
}

RARITY_LABEL = {
    "common": "Common", "uncommon": "Uncommon", "rare": "Rare",
    "epic": "Epic", "legendary": "Legendary",
}

# Biome group labels used in the fish codex header rows
FISH_BIOME_GROUPS = [
    ("Universal",       ["minnow", "dace", "stone_loach", "fathead_minnow", "bluntnose_minnow",
                         "gudgeon", "bleak", "mottled_sculpin"]),
    ("Temperate",       ["perch", "yellow_perch", "bass", "smallmouth_bass", "white_bass", "striped_bass",
                         "spotted_bass", "yellow_bass", "sunshine_bass", "white_perch",
                         "bluegill", "sunfish", "pumpkinseed", "rock_bass", "redear_sunfish",
                         "green_sunfish", "longear_sunfish", "redbreast_sunfish",
                         "crappie", "white_crappie", "walleye", "sauger", "saugeye",
                         "carp", "tench", "roach", "rudd", "chub", "bream",
                         "bigmouth_buffalo", "smallmouth_buffalo", "white_sucker", "northern_hogsucker",
                         "quillback", "shorthead_redhorse", "blue_sucker",
                         "golden_shiner", "emerald_shiner", "spottail_shiner", "gizzard_shad", "threadfin_shad",
                         "hornyhead_chub", "fallfish", "mosquitofish",
                         "channel_catfish", "yellow_bullhead", "brown_bullhead", "black_bullhead",
                         "freshwater_drum", "mooneye",
                         "johnny_darter", "iowa_darter", "orangethroat_darter", "least_darter",
                         "crystal_darter", "rainbow_darter", "logperch",
                         "american_eel", "muskie", "tiger_muskie", "golden_koi",
                         "creek_chub", "river_carpsucker", "spotted_sucker", "warpaint_shiner"]),
    ("Cold / Boreal",   ["trout", "brown_trout", "brook_trout", "lake_trout", "arctic_char", "dolly_varden",
                         "cutthroat_trout", "bull_trout", "splake", "tiger_trout",
                         "grayling", "golden_trout",
                         "kokanee", "coho_salmon", "salmon", "steelhead",
                         "cisco", "lake_whitefish", "round_whitefish", "longnose_sucker", "burbot", "goldeye",
                         "alewife", "rainbow_smelt", "trout_perch", "ruffe", "round_goby",
                         "pike", "sturgeon",
                         "pink_salmon", "chum_salmon", "lake_sculpin", "ninespine_stickleback"]),
    ("Jungle / Tropical", ["tilapia", "cichlid", "discus", "oscar", "peacock_bass",
                            "piranha", "tambaqui", "pacu", "catfish",
                            "redtail_catfish", "electric_eel", "payara", "arapaima",
                            "arowana", "goliath_tigerfish", "bichir", "giant_gourami", "rivulus"]),
    ("Pacific",         ["mahi_mahi", "parrotfish", "triggerfish", "flying_fish", "yellowfin_tuna"]),
    ("Wetland / Swamp", ["warmouth", "flier", "dollar_sunfish", "pirate_perch", "mudskipper", "bowfin",
                         "walking_catfish", "pickerel", "redfin_pickerel", "spotted_gar", "snakehead",
                         "longnose_gar", "grass_carp", "flathead_catfish", "blue_catfish",
                         "spotted_bullhead", "paddlefish", "gar", "alligator_gar",
                         "chain_pickerel", "golden_topminnow", "cypress_darter", "swamp_eel"]),
    ("Japan / East Asia", ["ayu", "oikawa", "tanago", "medaka", "gibuna", "higai",
                            "striped_loach", "dojou", "namazu", "gigi",
                            "yamame", "amago", "iwana", "ugui", "itou",
                            "sakura_masu", "shishamo", "aburahaya", "japanese_eel", "biwamasu"]),
    ("Ocean Reef",       ["clownfish", "moorish_idol", "lionfish", "parrotfish_reef", "grouper",
                          "blue_tang", "damselfish", "wrasse", "hawksbill_companion", "sergeant_major",
                          "butterflyfish", "ocean_angelfish", "trumpetfish", "barracuda", "moray_eel",
                          "goatfish", "humphead_wrasse", "rabbitfish", "sohal_surgeonfish", "scorpionfish",
                          "pufferfish", "boxfish", "needlefish", "achilles_tang", "hawkfish",
                          "filefish", "coral_grouper", "blacktip_reef_shark", "spotted_drum", "tilefish"]),
    ("Ocean Twilight",   ["lanternfish", "flashlight_fish", "oarfish", "leafy_sea_dragon",
                          "banded_sea_krait", "coelacanth",
                          "hatchetfish", "viperfish", "ribbonfish_ocean", "rattail", "ghost_shark",
                          "black_dragonfish", "stoplight_loosejaw", "sabertooth_fish", "frilled_shark",
                          "swordfish", "opah", "escolar", "alfonsino", "longnose_lancetfish",
                          "pineconefish", "orange_roughy", "slickhead", "dealfish"]),
    ("Ocean Deep",       ["anglerfish", "gulper_eel", "barreleye", "fangtooth",
                          "blobfish", "pelican_eel", "footballfish", "black_swallower",
                          "tripod_fish", "spookfish",
                          "snipe_eel", "whalefish", "coffinfish", "telescope_fish",
                          "medusafish", "abyssal_grenadier"]),
]

# Maps bait item_id → set of fish species that prefer it.
# Fish absent from every set are "universal" — catchable without bait or with any bait.
BAIT_AFFINITIES = {
    "worm_bait": {
        "minnow", "dace", "chub", "roach", "bream", "gudgeon",
        "loach", "stone_loach", "barbel", "nase", "spined_loach",
        "ruffe", "tench", "crucian_carp", "carp", "common_carp",
        "white_bream", "silver_bream", "bronze_bream",
        "bullhead", "river_bullhead", "stone_loach",
    },
    "insect_bait": {
        "trout", "rainbow_trout", "brown_trout", "brook_trout", "lake_trout",
        "grayling", "arctic_grayling", "bleak", "asp", "ide", "rudd",
        "arapaima", "piranha", "red_piranha", "discus", "tiger_fish",
        "arowana", "silver_arowana", "peacock_bass", "oscar",
        "tigerfish", "african_tigerfish",
    },
    "grain_bait": {
        "mirror_carp", "grass_carp", "bighead_carp", "silver_carp",
        "crucian_carp", "leather_carp", "koi",
        "tench", "bream", "white_bream", "silver_bream",
        "ide", "chub", "roach", "rudd",
    },
    "berry_bait": {
        "perch", "yellow_perch", "pumpkinseed", "bluegill", "sunfish",
        "bowfin", "mudfish", "weatherfish", "longnose_gar", "spotted_gar",
        "crappie", "black_crappie", "white_crappie",
        "rock_bass", "warmouth",
    },
    "meat_bait": {
        "pike", "northern_pike", "walleye", "zander", "pikeperch",
        "largemouth_bass", "smallmouth_bass", "striped_bass", "spotted_bass",
        "muskie", "tiger_muskie", "muskellunge",
        "taimen", "huchen", "wels_catfish", "flathead_catfish",
        "channel_catfish", "blue_catfish", "electric_eel",
        "alligator_gar", "gar", "snakehead",
    },
    # Cross-system baits — biased toward rare/legendary ornamental species.
    "floral_bait": {
        "golden_koi", "koi", "mirror_carp", "discus", "arowana",
        "silver_arowana", "peacock_bass", "ayu", "tanago", "medaka",
        "biwamasu", "japanese_eel",
    },
    "spiced_bait": {
        "arapaima", "tigerfish", "african_tigerfish", "snakehead",
        "wels_catfish", "muskie", "amago", "yamame", "iwana", "itou",
        "sakura_masu",
    },
    "aromatic_bait": {
        "trout", "rainbow_trout", "brown_trout", "brook_trout",
        "lake_trout", "grayling", "arctic_grayling", "yamame", "amago",
        "iwana", "ayu", "biwamasu",
    },
    "honeyed_bait": {
        "golden_koi", "koi", "mirror_carp", "leather_carp",
        "crucian_carp", "tench", "rudd", "ide",
        "ayu", "oikawa", "ugui", "gibuna",
    },
}

# Pre-computed set for O(1) lookup — fish in this set require specific bait
_ALL_BAIT_FISH = {s for lst in BAIT_AFFINITIES.values() for s in lst}

# Weight toward rarer rarity pools
_RARITY_WEIGHT = {
    "common": 40, "uncommon": 25, "rare": 10, "epic": 4, "legendary": 1
}

# time_pref: "night" | "dawn_dusk" | "day" — fish that bite more at specific times of day.
# dawn_dusk = first or last 60s of the 480s day cycle.
_FISH_TIME_PREF = {
    "eel":           "night",
    "bowfin":        "night",
    "bullhead":      "night",
    "burbot":        "night",
    "wels_catfish":  "night",
    "tench":         "night",
    "snakehead":     "night",
    "ayu":           "dawn_dusk",
    "trout":         "dawn_dusk",
    "grayling":      "dawn_dusk",
    "arctic_grayling": "dawn_dusk",
    "brown_trout":   "dawn_dusk",
    "rainbow_trout": "dawn_dusk",
    "walleye":       "dawn_dusk",
    "golden_koi":    "dawn_dusk",
    "arapaima":      "day",
    "tigerfish":     "day",
    "piranha":       "day",
}

# season_pref: "winter" | "summer" — bonus chance in that season (day_count % 40).
# winter = day_count % 40 >= 30; summer = day_count % 40 in [10, 20).
_FISH_SEASON_PREF = {
    "burbot":            "winter",
    "arctic_grayling":   "winter",
    "arctic_char":       "winter",
    "lake_trout":        "winter",
    "whitefish":         "winter",
    "arapaima":          "summer",
    "peacock_bass":      "summer",
    "tigerfish":         "summer",
    "piranha":           "summer",
    "discus":            "summer",
}


class FishGenerator:
    def __init__(self, world_seed):
        self._world_seed = world_seed
        self._counter = 0

    def generate(self, bx, by, biome, bait=None, time_of_day=0.0, day_count=0, is_hotspot=False, ocean_zone=""):
        self._counter += 1
        seed = (self._world_seed * 31337 + bx * 7919 + by * 4481 + self._counter) & 0x7FFFFFFF
        rng = random.Random(seed)

        bait_preferred = BAIT_AFFINITIES.get(bait, set()) if bait else set()

        # Determine current time category and season for preference bonuses.
        _DAY_DUR = 480.0
        _DAWN_DUSK_WINDOW = 60.0
        is_night = time_of_day >= _DAY_DUR
        is_dawn_dusk = not is_night and (time_of_day < _DAWN_DUSK_WINDOW or time_of_day > _DAY_DUR - _DAWN_DUSK_WINDOW)
        is_day = not is_night and not is_dawn_dusk
        season_phase = day_count % 40
        is_summer = 10 <= season_phase < 20
        is_winter = season_phase >= 30

        def _time_multiplier(species):
            pref = _FISH_TIME_PREF.get(species)
            if pref is None:
                return 1
            if pref == "night" and is_night:
                return 3
            if pref == "dawn_dusk" and is_dawn_dusk:
                return 3
            if pref == "day" and is_day:
                return 3
            return 1  # no time penalty — available all day, just less common

        def _season_multiplier(species):
            pref = _FISH_SEASON_PREF.get(species)
            if pref is None:
                return 1
            if pref == "summer" and is_summer:
                return 3
            if pref == "winter" and is_winter:
                return 3
            return 1

        # Build weighted species list filtered by biome and bait preference.
        # Without bait only universal fish (not in _ALL_BAIT_FISH) are eligible.
        # With bait, preferred fish get full weight; universal fish get 1/3 weight;
        # fish that prefer a different bait are excluded entirely.
        eligible = []
        for species, fdata in FISH_TYPES.items():
            affinity = fdata["biome_affinity"]
            if affinity and biome not in affinity:
                continue
            if ocean_zone and fdata.get("ocean_zone", "") != ocean_zone:
                continue

            is_universal = species not in _ALL_BAIT_FISH
            is_preferred = species in bait_preferred

            if not bait:
                if not is_universal:
                    continue
            else:
                if not is_preferred and not is_universal:
                    continue

            base_rarity = fdata["rarity_pool"][0]
            w = _RARITY_WEIGHT.get(base_rarity, 10)
            if is_universal and bait:
                w = max(1, w // 3)
            w = w * _time_multiplier(species) * _season_multiplier(species)
            eligible.extend([species] * w)

        # Fallback: if the biome has no specific fish, use universal-only fish
        if not eligible:
            for species, fdata in FISH_TYPES.items():
                if not fdata["biome_affinity"]:
                    base_rarity = fdata["rarity_pool"][0]
                    w = _RARITY_WEIGHT.get(base_rarity, 10)
                    eligible.extend([species] * w)

        species = rng.choice(eligible)
        fdata = FISH_TYPES[species]

        # Hotspot: bias rarity toward rare+ by extending the rarity pool with extras.
        rarity_pool = list(fdata["rarity_pool"])
        if is_hotspot:
            rarity_pool += [r for r in rarity_pool if r in ("rare", "epic", "legendary")]
            rarity_pool += [r for r in rarity_pool if r in ("epic", "legendary")]
        rarity = rng.choice(rarity_pool)

        wmin, wmax = fdata["weight_range"]
        weight_kg = round(rng.uniform(wmin, wmax), 2)
        lmin, lmax = fdata["length_range"]
        length_cm = rng.randint(lmin, lmax)
        pattern = rng.choice(fdata["pattern_pool"])
        primary_color, secondary_color = rng.choice(fdata["colors"])

        uid = f"fish_{bx}_{by}_{seed}"
        return Fish(
            uid=uid,
            species=species,
            rarity=rarity,
            weight_kg=weight_kg,
            length_cm=length_cm,
            pattern=pattern,
            primary_color=primary_color,
            secondary_color=secondary_color,
            habitat=fdata["habitat"],
            biome_found=biome or "unknown",
            seed=seed,
            ocean_zone=fdata.get("ocean_zone", ""),
        )


# ---------------------------------------------------------------------------
# Fish rendering
# ---------------------------------------------------------------------------

_fish_render_cache = {}


def render_fish(fish, size=58):
    key = (fish.uid, size)
    cached = _fish_render_cache.get(key)
    if cached is not None:
        return cached

    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    rng = random.Random(fish.seed)

    pc = fish.primary_color
    sc = fish.secondary_color
    dark = (max(0, pc[0] - 45), max(0, pc[1] - 45), max(0, pc[2] - 45))

    # Body: elongated ellipse
    bw = int(size * 0.68)
    bh = int(size * 0.36)
    bx0 = int(size * 0.18)
    by0 = size // 2 - bh // 2

    pygame.draw.ellipse(surf, pc, (bx0, by0, bw, bh))

    # Tail fin
    cx_tail = bx0
    cy_mid = size // 2
    tail_pts = [
        (cx_tail, cy_mid),
        (int(size * 0.04), cy_mid - int(size * 0.19)),
        (int(size * 0.04), cy_mid + int(size * 0.19)),
    ]
    pygame.draw.polygon(surf, sc, tail_pts)

    # Dorsal fin
    fin_pts = [
        (bx0 + int(bw * 0.30), by0),
        (bx0 + int(bw * 0.15), by0 - int(size * 0.13)),
        (bx0 + int(bw * 0.52), by0 - int(size * 0.09)),
    ]
    pygame.draw.polygon(surf, sc, fin_pts)

    # Pattern overlay
    if fish.pattern == "striped":
        for i in range(3):
            sx = bx0 + int(bw * (0.22 + i * 0.22))
            pygame.draw.line(surf, sc, (sx, by0 + 3), (sx, by0 + bh - 3), 2)
    elif fish.pattern == "spotted":
        for _ in range(5):
            dot_x = rng.randint(bx0 + 6, bx0 + bw - 10)
            dot_y = rng.randint(by0 + 4, by0 + bh - 4)
            pygame.draw.circle(surf, sc, (dot_x, dot_y), rng.randint(2, 4))
    elif fish.pattern == "banded":
        for i in range(2):
            bnd_x = bx0 + int(bw * (0.28 + i * 0.28))
            bnd_w = max(3, int(bw * 0.10))
            r = pygame.Rect(bnd_x, by0 + 3, bnd_w, bh - 6)
            pygame.draw.rect(surf, sc, r)
    elif fish.pattern == "mottled":
        for _ in range(6):
            mx2 = rng.randint(bx0 + 4, bx0 + bw - 8)
            my2 = rng.randint(by0 + 3, by0 + bh - 3)
            pygame.draw.ellipse(surf, sc, (mx2, my2, rng.randint(4, 8), rng.randint(3, 6)))
    elif fish.pattern == "scaled":
        for row in range(3):
            for col in range(4):
                sx = bx0 + 8 + col * max(1, bw // 4)
                sy = by0 + 5 + row * max(1, bh // 3)
                pygame.draw.circle(surf, sc, (sx, sy), 3, 1)
    elif fish.pattern == "plated":
        for i in range(5):
            px_s = bx0 + int(bw * (0.10 + i * 0.17))
            pygame.draw.line(surf, sc, (px_s, by0 + 2), (px_s, by0 + bh - 2), 3)

    # Eye
    eye_x = bx0 + int(bw * 0.84)
    eye_y = size // 2 - 2
    pygame.draw.circle(surf, (15, 15, 15), (eye_x, eye_y), max(2, size // 20))
    pygame.draw.circle(surf, (230, 230, 230), (eye_x - 1, eye_y - 1), max(1, size // 40))

    # Body outline
    pygame.draw.ellipse(surf, dark, (bx0, by0, bw, bh), 1)

    _fish_render_cache[key] = surf
    return surf


def invalidate_fish_cache(uid):
    for k in [k for k in _fish_render_cache if k[0] == uid]:
        del _fish_render_cache[k]
