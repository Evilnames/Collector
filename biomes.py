BIOMES = ["igneous", "sedimentary", "crystal", "ferrous", "void"]

BIODOME_TYPES = [
    "temperate", "boreal", "birch_forest", "jungle", "wetland",
    "redwood", "tropical", "savanna", "wasteland",
    "alpine_mountain", "rocky_mountain",
    "rolling_hills", "steep_hills",
    "steppe", "arid_steppe",
    "desert", "tundra", "swamp", "beach", "canyon", "red_rock",
    "mediterranean", "east_asian", "south_asian",
    # "coastal" is not in the random pool — it is auto-assigned adjacent to ocean zones
]

# (height_bias, noise_amplitude_scale) per biodome.
# height_bias: added to SURFACE_Y before noise (negative = higher terrain).
# noise_amplitude_scale: multiplies existing sine octave amplitudes.
# Missing entries default to (0, 1.0).
BIODOME_TERRAIN_MODS = {
    "alpine_mountain": (-14, 2.6),
    "rocky_mountain":  ( -7, 2.0),
    "rolling_hills":   ( -3, 1.5),
    "steep_hills":     ( -2, 1.8),
    "steppe":          (  3, 0.35),
    "arid_steppe":     (  2, 0.45),
    "desert":          (  2, 0.55),
    "tundra":          (  1, 0.40),
    "swamp":           (  7, 0.20),    # deeper lowland basin
    "beach":           ( -2, 0.15),   # slightly above sea level — sandy shore
    "coastal":         (  0, 0.30),   # flat at sea level — transitions into ocean
    "canyon":          ( -5, 2.80),
    "red_rock":        ( -4, 1.50),    # Sedona-style raised plateau; relief mostly from mesa/plateau anomalies
    "mediterranean":   ( -2, 0.95),    # raised dry ridges
    "east_asian":      ( -1, 1.10),
    "south_asian":     (  1, 0.80),
    "ocean":           ( 22, 0.04),   # deep flat terrain → fills with water
    "pacific_island":  (-8,  0.40),   # raised island above water level
    # Previously unmodded forest/wetland biodomes — give each a distinct silhouette.
    "temperate":       ( -1, 1.00),
    "boreal":          ( -3, 1.30),    # mid-hill forested
    "birch_forest":    (  0, 0.95),
    "redwood":         ( -4, 1.45),    # tall forested ridges
    "jungle":          (  1, 0.85),    # river basin lowlands
    "tropical":        ( -1, 0.75),
    "wetland":         (  4, 0.25),    # low + flat
    "savanna":         (  1, 0.55),
    "wasteland":       (  0, 1.20),    # broken, ragged
}

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
