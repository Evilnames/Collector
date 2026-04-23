from blocks import (
    BLOCKS,
    CAVE_MUSHROOM, EMBER_CAP, PALE_GHOST, GOLD_CHANTERELLE, COBALT_CAP,
    MOSSY_CAP, VIOLET_CROWN, BLOOD_CAP, SULFUR_DOME, IVORY_BELL,
    ASH_BELL, TEAL_BELL, RUST_SHELF, COPPER_SHELF, OBSIDIAN_SHELF,
    COAL_PUFF, STONE_PUFF, AMBER_PUFF, SULFUR_TUFT, HONEY_CLUSTER,
    CORAL_TUFT, BONE_STALK, MAGMA_CAP, DEEP_INK, BIOLUME,
)

_MUSHROOM_ORDER = [
    CAVE_MUSHROOM, EMBER_CAP, PALE_GHOST, GOLD_CHANTERELLE, COBALT_CAP,
    MOSSY_CAP, VIOLET_CROWN, BLOOD_CAP, SULFUR_DOME, IVORY_BELL,
    ASH_BELL, TEAL_BELL, RUST_SHELF, COPPER_SHELF, OBSIDIAN_SHELF,
    COAL_PUFF, STONE_PUFF, AMBER_PUFF, SULFUR_TUFT, HONEY_CLUSTER,
    CORAL_TUFT, BONE_STALK, MAGMA_CAP, DEEP_INK, BIOLUME,
]

_MUSHROOM_BIOME = {
    CAVE_MUSHROOM:   "All biomes",       EMBER_CAP:       "Igneous",
    PALE_GHOST:      "Void / Sedimentary", GOLD_CHANTERELLE:"Sedimentary",
    COBALT_CAP:      "Crystal / Ferrous", MOSSY_CAP:       "Sedimentary",
    VIOLET_CROWN:    "Void",              BLOOD_CAP:       "Igneous / Ferrous",
    SULFUR_DOME:     "Igneous",           IVORY_BELL:      "Crystal",
    ASH_BELL:        "Ferrous / Void",    TEAL_BELL:       "Crystal",
    RUST_SHELF:      "Igneous / Ferrous", COPPER_SHELF:    "Sedimentary",
    OBSIDIAN_SHELF:  "Void  (deep)",      COAL_PUFF:       "Igneous",
    STONE_PUFF:      "Ferrous",           AMBER_PUFF:      "Sedimentary",
    SULFUR_TUFT:     "Igneous",           HONEY_CLUSTER:   "Sedimentary",
    CORAL_TUFT:      "Crystal",           BONE_STALK:      "Ferrous",
    MAGMA_CAP:       "Igneous  (deep)",   DEEP_INK:        "Void  (deep)",
    BIOLUME:         "Crystal  (deep)",
}

_MUSHROOM_DROP_COLOR = {
    "cave_mushroom": (180, 160, 120),
    "rare_mushroom": (210, 165, 60),
    "glowing_spore": (60, 220, 200),
}

_MUSHROOM_SHAPES = {
    CAVE_MUSHROOM: "dome",    EMBER_CAP: "dome",     PALE_GHOST: "dome",
    GOLD_CHANTERELLE: "dome", COBALT_CAP: "dome",    MOSSY_CAP: "dome",
    VIOLET_CROWN: "dome",     BLOOD_CAP: "dome",     SULFUR_DOME: "dome",
    IVORY_BELL: "bell",       ASH_BELL: "bell",      TEAL_BELL: "bell",
    RUST_SHELF: "flat shelf", COPPER_SHELF: "flat shelf", OBSIDIAN_SHELF: "flat shelf",
    COAL_PUFF: "puffball",    STONE_PUFF: "puffball",AMBER_PUFF: "puffball",
    SULFUR_TUFT: "cluster",   HONEY_CLUSTER: "cluster", CORAL_TUFT: "cluster",
    BONE_STALK: "tall bell",  MAGMA_CAP: "dome",     DEEP_INK: "dome",
    BIOLUME: "dome",
}

_MUSHROOM_NAMES = {
    CAVE_MUSHROOM: "Cave Mushroom",      EMBER_CAP: "Ember Cap",
    PALE_GHOST: "Pale Ghost",            GOLD_CHANTERELLE: "Gold Chanterelle",
    COBALT_CAP: "Cobalt Cap",            MOSSY_CAP: "Mossy Cap",
    VIOLET_CROWN: "Violet Crown",        BLOOD_CAP: "Blood Cap",
    SULFUR_DOME: "Sulfur Dome",          IVORY_BELL: "Ivory Bell",
    ASH_BELL: "Ash Bell",                TEAL_BELL: "Teal Bell",
    RUST_SHELF: "Rust Shelf",            COPPER_SHELF: "Copper Shelf",
    OBSIDIAN_SHELF: "Obsidian Shelf",    COAL_PUFF: "Coal Puff",
    STONE_PUFF: "Stone Puff",            AMBER_PUFF: "Amber Puff",
    SULFUR_TUFT: "Sulfur Tuft",          HONEY_CLUSTER: "Honey Cluster",
    CORAL_TUFT: "Coral Tuft",            BONE_STALK: "Bone Stalk",
    MAGMA_CAP: "Magma Cap",              DEEP_INK: "Deep Ink",
    BIOLUME: "Biolume",
}

SPECIAL_DESCS = {
    "luminous":    ("Glows in collection",    "No upgrade bonus"),
    "magnetic":    ("Crusher +2 bonus items", "Tumbler blocked"),
    "crystalline": ("Gem Cutter max yield",   "Effective hardness -2"),
    "resonant":    ("Double research XP",     "One refine only"),
    "voidtouched": ("Chance: void essence",   "1% equip damage"),
    "dense":       ("Purity +0.3 effective",  "Size one tier smaller"),
    "hollow":      ("Output count +2",        "Luster -0.3 effective"),
    "fused":       ("Unique appearance",        "No upgrade bonus"),
}

RARITY_LABEL = {
    "common": "Common", "uncommon": "Uncommon", "rare": "Rare",
    "epic": "Epic", "legendary": "Legendary",
}
