"""Silkworm rearing + silk manufacturing pipeline.

Pipeline shape:
    mulberry tree  → mulberry_leaves
    silkworm_eggs  → SILKWORM_TRAY_EGG (placed block)
    feed leaves    → tray advances EGG → LARVA → SPINNING → COCOON
    harvest COCOON → silk_cocoon (or silk_cocoon_double, ~10% chance)
    REELING_FRAME  → cocoon  → raw_silk
    DEGUMMING_VAT  → raw_silk → silk_thread

Variants share the same stations but use different inputs:
    mulberry silk : silk_cocoon        → raw_silk         → silk_thread        (fiber = "silk")
    dupioni silk  : silk_cocoon_double → dupioni_raw_silk → dupioni_silk_thread (fiber = "dupioni_silk")
    tussah silk   : tussah_cocoon      → tussah_raw_silk  → tussah_silk_thread  (fiber = "tussah_silk")
    sea silk      : byssus_fiber       → (skip reeling)   → sea_silk_thread     (fiber = "sea_silk")
"""


# How many leaves it takes to advance each rearing stage.
LEAVES_PER_STAGE = {
    "egg":      2,   # hatch into larva
    "larva":    4,   # eat into spinning
    "spinning": 2,   # finish cocoon
}

# Stage-advance order (used by the feeding handler in UI/handlers.py).
TRAY_STAGE_ORDER = ["egg", "larva", "spinning", "cocoon"]

# Random chance a finished cocoon comes out as a double-cocoon (dupioni).
DUPIONI_CHANCE = 0.10

# Reeling: 1 cocoon → 1 raw silk of the matching kind.
REELING_RECIPES = {
    "silk_cocoon":        "raw_silk",
    "silk_cocoon_double": "dupioni_raw_silk",
    "tussah_cocoon":      "tussah_raw_silk",
    # byssus_fiber skips reeling — it's already a continuous filament
}

# Degumming: raw silk → finished thread (boil off sericin / sea-silk treatment).
DEGUMMING_RECIPES = {
    "raw_silk":          "silk_thread",
    "dupioni_raw_silk":  "dupioni_silk_thread",
    "tussah_raw_silk":   "tussah_silk_thread",
    "byssus_fiber":      "sea_silk_thread",
}

# Items the silkworm tray accepts as feed.
TRAY_FEED_ITEMS = {"mulberry_leaves"}

# Display labels (UI / encyclopedia).
SILK_VARIANT_DISPLAY = {
    "silk":         "Mulberry Silk",
    "dupioni_silk": "Dupioni Silk",
    "tussah_silk":  "Tussah (Wild) Silk",
    "sea_silk":     "Sea Silk (Byssus)",
}

# Inventory key each fiber type spins from (used by the spinning UI to surface
# the new fibers, and by _finish_spinning to consume the right inventory item).
SILK_FIBER_SOURCE = {
    "silk":         "silk_thread",
    "dupioni_silk": "dupioni_silk_thread",
    "tussah_silk":  "tussah_silk_thread",
    "sea_silk":     "sea_silk_thread",
}
