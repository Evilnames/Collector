BIOMES = ["igneous", "sedimentary", "crystal", "ferrous", "void"]

BIODOME_TYPES = [
    "temperate", "boreal", "birch_forest", "jungle", "wetland",
    "redwood", "tropical", "savanna", "wasteland", "fungal",
]

BIOME_STONE_COLORS = {
    "igneous":     (90,  85,  88),
    "sedimentary": (130, 118, 100),
    "crystal":     (108, 115, 130),
    "ferrous":     (115, 95,  90),
    "void":        (55,  45,  70),
}

# Multipliers applied to ore probability thresholds in _pick_block().
# Keys match the ore variable names used in that function.
BIOME_ORE_MULTIPLIERS = {
    "igneous":     {"obsidian": 1.6, "coal": 0.7},
    "sedimentary": {"coal": 1.5, "iron": 1.2},
    "crystal":     {"crystal": 1.5, "ruby": 1.2},
    "ferrous":     {"iron": 1.4, "gold": 1.3},
    "void":        {"crystal": 1.3, "obsidian": 1.4},
}
