"""Configuration for the multi-pass world generator.

Edit ``WORLDGEN_CONFIG`` to tune world size, history length, and viz pacing.
The ``world_span`` is the number of biome cells; each cell is
``cell_block_width`` blocks wide. Default produces a 25,600-block-wide world.
"""

WORLDGEN_CONFIG = {
    "world_span": 600,            # biome cells; configurable 100..1200
    "cell_block_width": 64,       # blocks per cell
    "history_years": 500,
    "starting_kingdoms_per_100_cells": 2.2,    # ~13 kingdoms — each gets a wide territory
    "settlements_per_kingdom_range": (3, 6),   # more settlements per kingdom (spread out)
    "settlement_min_separation_cells": 14,     # ~900 blocks between any two settlements
    "ocean_count_default": 2,     # baseline ocean stretches per world
    "ocean_count_variance": 2,    # extra stretches rolled on top: count = default + randint(0, variance)
    "ocean_stretch_width_range": (15, 35),  # fallback width if a type doesn't override
    "viz_seconds": 6.0,
}


SIZE_PRESETS = {
    "small":  100,
    "medium": 250,
    "large":  400,
    "huge":   800,
    "epic":   1200,
}


def resolve_span(preset_or_int):
    if isinstance(preset_or_int, int):
        return max(60, min(1200, preset_or_int))
    return SIZE_PRESETS.get(str(preset_or_int).lower(), WORLDGEN_CONFIG["world_span"])


def cell_block_width():
    return WORLDGEN_CONFIG["cell_block_width"]
