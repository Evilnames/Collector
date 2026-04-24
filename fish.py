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
}

# Order for display in the fish codex (roughly by biome group, then rarity)
FISH_TYPE_ORDER = [
    # Universal
    "minnow", "dace", "stone_loach",
    # Temperate
    "perch", "yellow_perch", "bass", "smallmouth_bass", "white_bass", "striped_bass",
    "spotted_bass", "yellow_bass", "white_perch",
    "bluegill", "sunfish", "pumpkinseed", "rock_bass", "redear_sunfish",
    "green_sunfish", "longear_sunfish", "redbreast_sunfish",
    "crappie", "white_crappie", "walleye", "sauger",
    "carp", "tench", "roach", "rudd", "chub", "bream",
    "bigmouth_buffalo", "white_sucker", "golden_shiner", "gizzard_shad",
    "channel_catfish", "yellow_bullhead", "brown_bullhead",
    "freshwater_drum", "american_eel", "muskie", "tiger_muskie", "golden_koi",
    # Cold
    "trout", "brown_trout", "brook_trout", "lake_trout", "arctic_char", "dolly_varden",
    "grayling", "golden_trout",
    "cisco", "lake_whitefish", "round_whitefish", "burbot", "goldeye",
    "salmon", "steelhead", "pike", "sturgeon",
    # Jungle/Tropical
    "tilapia", "cichlid", "discus", "oscar", "peacock_bass",
    "piranha", "tambaqui", "pacu", "catfish",
    "redtail_catfish", "electric_eel", "payara", "arapaima",
    # Wetland/Swamp
    "warmouth", "flier", "mudskipper", "bowfin", "walking_catfish",
    "pickerel", "spotted_gar", "snakehead", "longnose_gar", "grass_carp",
    "flathead_catfish", "blue_catfish", "paddlefish",
    "gar", "alligator_gar",
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
    ("Universal",       ["minnow", "dace", "stone_loach"]),
    ("Temperate",       ["perch", "yellow_perch", "bass", "smallmouth_bass", "white_bass", "striped_bass",
                         "spotted_bass", "yellow_bass", "white_perch",
                         "bluegill", "sunfish", "pumpkinseed", "rock_bass", "redear_sunfish",
                         "green_sunfish", "longear_sunfish", "redbreast_sunfish",
                         "crappie", "white_crappie", "walleye", "sauger",
                         "carp", "tench", "roach", "rudd", "chub", "bream",
                         "bigmouth_buffalo", "white_sucker", "golden_shiner", "gizzard_shad",
                         "channel_catfish", "yellow_bullhead", "brown_bullhead",
                         "freshwater_drum", "american_eel", "muskie", "tiger_muskie", "golden_koi"]),
    ("Cold / Boreal",   ["trout", "brown_trout", "brook_trout", "lake_trout", "arctic_char", "dolly_varden",
                         "grayling", "golden_trout",
                         "cisco", "lake_whitefish", "round_whitefish", "burbot", "goldeye",
                         "salmon", "steelhead", "pike", "sturgeon"]),
    ("Jungle / Tropical", ["tilapia", "cichlid", "discus", "oscar", "peacock_bass",
                            "piranha", "tambaqui", "pacu", "catfish",
                            "redtail_catfish", "electric_eel", "payara", "arapaima"]),
    ("Wetland / Swamp", ["warmouth", "flier", "mudskipper", "bowfin", "walking_catfish",
                         "pickerel", "spotted_gar", "snakehead", "longnose_gar", "grass_carp",
                         "flathead_catfish", "blue_catfish", "paddlefish",
                         "gar", "alligator_gar"]),
]

# Weight toward rarer rarity pools
_RARITY_WEIGHT = {
    "common": 40, "uncommon": 25, "rare": 10, "epic": 4, "legendary": 1
}


class FishGenerator:
    def __init__(self, world_seed):
        self._world_seed = world_seed
        self._counter = 0

    def generate(self, bx, by, biome):
        self._counter += 1
        seed = (self._world_seed * 31337 + bx * 7919 + by * 4481 + self._counter) & 0x7FFFFFFF
        rng = random.Random(seed)

        # Build weighted species list filtered to this biome.
        # biome_affinity=[] means the fish can appear in any biome.
        eligible = []
        for species, fdata in FISH_TYPES.items():
            affinity = fdata["biome_affinity"]
            if not affinity or biome in affinity:
                base_rarity = fdata["rarity_pool"][0]
                w = _RARITY_WEIGHT.get(base_rarity, 10)
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
        rarity = rng.choice(fdata["rarity_pool"])

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
