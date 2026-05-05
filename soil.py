# Soil / moisture / fertility / growth system for the farming overhaul (Phases 1-2).
# Centralizes tunable constants, per-crop preferences, and pure helpers.

from blocks import (
    STRAWBERRY_CROP_YOUNG, WHEAT_CROP_YOUNG, CARROT_CROP_YOUNG, TOMATO_CROP_YOUNG,
    CORN_CROP_YOUNG, PUMPKIN_CROP_YOUNG, APPLE_CROP_YOUNG,
    RICE_CROP_YOUNG, GINGER_CROP_YOUNG, BOK_CHOY_CROP_YOUNG, GARLIC_CROP_YOUNG,
    SCALLION_CROP_YOUNG, CHILI_CROP_YOUNG,
    PEPPER_CROP_YOUNG, ONION_CROP_YOUNG, POTATO_CROP_YOUNG,
    EGGPLANT_CROP_YOUNG, CABBAGE_CROP_YOUNG,
    BEET_CROP_YOUNG, TURNIP_CROP_YOUNG, LEEK_CROP_YOUNG,
    ZUCCHINI_CROP_YOUNG, SWEET_POTATO_CROP_YOUNG, WATERMELON_CROP_YOUNG,
    RADISH_CROP_YOUNG, PEA_CROP_YOUNG, CELERY_CROP_YOUNG, BROCCOLI_CROP_YOUNG,
    CACTUS_YOUNG, DATE_PALM_CROP_YOUNG, AGAVE_CROP_YOUNG,
    SAGUARO_YOUNG, BARREL_CACTUS_YOUNG, OCOTILLO_YOUNG,
    PRICKLY_PEAR_YOUNG, CHOLLA_YOUNG, PALO_VERDE_YOUNG,
    COFFEE_CROP_YOUNG, GRAPEVINE_CROP_YOUNG,
    STRAWBERRY_CROP_YOUNG_P, TOMATO_CROP_YOUNG_P, WATERMELON_CROP_YOUNG_P,
    CORN_CROP_YOUNG_P, RICE_CROP_YOUNG_P,
)

# --- Tunable constants ------------------------------------------------------

MAX_MOISTURE              = 8      # upper bound for any tilled tile
MAX_FERTILITY             = 8      # upper bound for fertility (raised to 10 by composting research)
SOIL_TICK_SECS            = 5.0    # how often update_soil runs
MOISTURE_DECAY_CHANCE     = 0.1    # per tick chance to lose 1 moisture
WATER_ADJACENT_FLOOR      = 4      # tilled soil adjacent to a WATER block clamps up to this
TILL_START_MOISTURE       = 2      # moisture applied when a tile is first tilled
WATERING_AMOUNT           = 5      # moisture added per watering can use
WATERING_CAN_CAPACITY     = 8      # uses per full watering can
REVERT_AFTER_FALLOW_TICKS = 24     # empty tilled soil → DIRT after this many soil ticks

# Growth progress (0..GROWTH_PROGRESS_MAX)
GROWTH_PROGRESS_MAX  = 100
GROWTH_DELTA_MAX     = 22          # perfect care → ~5 ticks to mature
GROWTH_DELTA_MIN     = 5           # minimum positive delta inside the tolerance band
DESERT_GROWTH_SPEED  = 0.2         # desert plants grow ~5x slower than normal crops

# Yield scaling
YIELD_MIN_MULT = 0.5
YIELD_MAX_MULT = 2.5

# Fertility
FERTILITY_DRAIN_PER_HARVEST     = 2    # default fertility drained when a crop matures
COMPOST_FERTILITY_GAIN          = 3    # fertility gained per compost item applied
MANURE_FERTILITY_GAIN           = 2    # fertility gained per raw manure item applied
RICH_COMPOST_FERTILITY_GAIN     = 4    # fertility gained per rich compost item applied

MANURE_ITEM_IDS = {"chicken_droppings", "sheep_droppings", "goat_droppings", "cow_manure"}

# Rain events (Phase 2)
RAIN_MIN_GAP_SECS      = 360.0    # shortest gap between rain events (6 min)
RAIN_MAX_GAP_SECS      = 720.0    # longest gap (12 min)
RAIN_DURATION_MIN_SECS =  30.0    # shortest rain duration
RAIN_DURATION_MAX_SECS =  60.0    # longest rain duration

# Compost bin (Phase 2)
COMPOST_PROGRESS_PER_SEC  = 2.0   # progress points per second (100 = 50 s per compost)
COMPOST_OUTPUT_THRESHOLD  = 100.0
COMPOST_INPUT_PER_OUTPUT  = 2     # organic items consumed per compost produced

# Items that can be deposited into the compost bin
ORGANIC_ITEM_IDS = {
    "wheat", "carrot", "tomato", "corn", "pumpkin", "apple", "strawberry",
    "rice", "ginger", "bok_choy", "garlic", "scallion", "chili", "pepper",
    "onion", "potato", "eggplant", "cabbage", "beet", "turnip", "leek",
    "zucchini", "sweet_potato", "watermelon", "radish", "pea", "celery",
    "broccoli", "cactus_pulp", "date", "agave_fibre",
    "lumber", "sapling",
    "chicken_droppings", "sheep_droppings", "goat_droppings", "cow_manure",
}


# --- Crop preferences -------------------------------------------------------
# moisture: (min_tolerable, max_beneficial) on a 0..MAX_MOISTURE scale.
# fertility_drain: points drained from soil when this crop matures (default 2).
# base_yield: food items dropped at harvest under neutral care.

_DRY         = (0, 3)
_MEDIUM_DRY  = (1, 4)
_MEDIUM      = (2, 5)
_MEDIUM_WET  = (3, 6)
_WET         = (5, 8)

CROP_PREFERENCES = {
    STRAWBERRY_CROP_YOUNG:   {"moisture": _MEDIUM,     "base_yield": 2, "fertility_drain": 2},
    WHEAT_CROP_YOUNG:        {"moisture": _MEDIUM_DRY, "base_yield": 2, "fertility_drain": 1},
    CARROT_CROP_YOUNG:       {"moisture": _MEDIUM,     "base_yield": 2, "fertility_drain": 2},
    TOMATO_CROP_YOUNG:       {"moisture": _MEDIUM_WET, "base_yield": 2, "fertility_drain": 3},
    CORN_CROP_YOUNG:         {"moisture": _MEDIUM,     "base_yield": 2, "fertility_drain": 3},
    PUMPKIN_CROP_YOUNG:      {"moisture": _MEDIUM,     "base_yield": 2, "fertility_drain": 2},
    APPLE_CROP_YOUNG:        {"moisture": _MEDIUM,     "base_yield": 2, "fertility_drain": 2},
    RICE_CROP_YOUNG:         {"moisture": _WET,        "base_yield": 2, "fertility_drain": 2},
    GINGER_CROP_YOUNG:       {"moisture": _MEDIUM_WET, "base_yield": 2, "fertility_drain": 2},
    BOK_CHOY_CROP_YOUNG:     {"moisture": _MEDIUM_WET, "base_yield": 2, "fertility_drain": 2},
    GARLIC_CROP_YOUNG:       {"moisture": _MEDIUM_DRY, "base_yield": 2, "fertility_drain": 1},
    SCALLION_CROP_YOUNG:     {"moisture": _MEDIUM,     "base_yield": 2, "fertility_drain": 1},
    CHILI_CROP_YOUNG:        {"moisture": _MEDIUM_DRY, "base_yield": 2, "fertility_drain": 2},
    PEPPER_CROP_YOUNG:       {"moisture": _MEDIUM,     "base_yield": 2, "fertility_drain": 2},
    ONION_CROP_YOUNG:        {"moisture": _MEDIUM,     "base_yield": 2, "fertility_drain": 2},
    POTATO_CROP_YOUNG:       {"moisture": _MEDIUM,     "base_yield": 2, "fertility_drain": 2},
    EGGPLANT_CROP_YOUNG:     {"moisture": _MEDIUM_WET, "base_yield": 2, "fertility_drain": 3},
    CABBAGE_CROP_YOUNG:      {"moisture": _MEDIUM,     "base_yield": 2, "fertility_drain": 2},
    BEET_CROP_YOUNG:         {"moisture": _MEDIUM,     "base_yield": 2, "fertility_drain": 2},
    TURNIP_CROP_YOUNG:       {"moisture": _MEDIUM,     "base_yield": 2, "fertility_drain": 2},
    LEEK_CROP_YOUNG:         {"moisture": _MEDIUM_WET, "base_yield": 2, "fertility_drain": 2},
    ZUCCHINI_CROP_YOUNG:     {"moisture": _MEDIUM_WET, "base_yield": 2, "fertility_drain": 3},
    SWEET_POTATO_CROP_YOUNG: {"moisture": _MEDIUM,     "base_yield": 2, "fertility_drain": 2},
    WATERMELON_CROP_YOUNG:   {"moisture": _WET,        "base_yield": 2, "fertility_drain": 3},
    RADISH_CROP_YOUNG:       {"moisture": _MEDIUM,     "base_yield": 2, "fertility_drain": 1},
    PEA_CROP_YOUNG:          {"moisture": _MEDIUM,     "base_yield": 2, "fertility_drain": 1},
    CELERY_CROP_YOUNG:       {"moisture": _MEDIUM_WET, "base_yield": 2, "fertility_drain": 2},
    BROCCOLI_CROP_YOUNG:     {"moisture": _MEDIUM,     "base_yield": 2, "fertility_drain": 2},
    CACTUS_YOUNG:            {"moisture": _DRY, "base_yield": 2, "fertility_drain": 1, "growth_speed": DESERT_GROWTH_SPEED},
    DATE_PALM_CROP_YOUNG:    {"moisture": _DRY, "base_yield": 2, "fertility_drain": 1, "growth_speed": DESERT_GROWTH_SPEED},
    AGAVE_CROP_YOUNG:        {"moisture": _DRY, "base_yield": 2, "fertility_drain": 1, "growth_speed": DESERT_GROWTH_SPEED},
    SAGUARO_YOUNG:           {"moisture": _DRY, "base_yield": 2, "fertility_drain": 1, "growth_speed": DESERT_GROWTH_SPEED},
    BARREL_CACTUS_YOUNG:     {"moisture": _DRY, "base_yield": 2, "fertility_drain": 1, "growth_speed": DESERT_GROWTH_SPEED},
    OCOTILLO_YOUNG:          {"moisture": _DRY, "base_yield": 2, "fertility_drain": 1, "growth_speed": DESERT_GROWTH_SPEED},
    PRICKLY_PEAR_YOUNG:      {"moisture": _DRY, "base_yield": 2, "fertility_drain": 1, "growth_speed": DESERT_GROWTH_SPEED},
    CHOLLA_YOUNG:            {"moisture": _DRY, "base_yield": 2, "fertility_drain": 1, "growth_speed": DESERT_GROWTH_SPEED},
    PALO_VERDE_YOUNG:        {"moisture": _DRY, "base_yield": 2, "fertility_drain": 1, "growth_speed": DESERT_GROWTH_SPEED},
    COFFEE_CROP_YOUNG:       {"moisture": _MEDIUM_WET, "base_yield": 1, "fertility_drain": 3},
    GRAPEVINE_CROP_YOUNG:    {"moisture": _MEDIUM,     "base_yield": 1, "fertility_drain": 2},
    # --- Premium variants: wider moisture band, +50% base yield, lower fertility drain ---
    STRAWBERRY_CROP_YOUNG_P:  {"moisture": (1, 7), "base_yield": 3, "fertility_drain": 1},
    TOMATO_CROP_YOUNG_P:      {"moisture": (2, 7), "base_yield": 3, "fertility_drain": 2},
    WATERMELON_CROP_YOUNG_P:  {"moisture": (3, 8), "base_yield": 3, "fertility_drain": 2},
    CORN_CROP_YOUNG_P:        {"moisture": (1, 6), "base_yield": 3, "fertility_drain": 2},
    RICE_CROP_YOUNG_P:        {"moisture": (4, 8), "base_yield": 3, "fertility_drain": 1},
}

_DEFAULT_PREFS = {"moisture": _MEDIUM, "base_yield": 2, "fertility_drain": 2}


# --- Helpers ----------------------------------------------------------------

def get_prefs(block_id):
    return CROP_PREFERENCES.get(block_id, _DEFAULT_PREFS)


def care_score(prefs, moisture, fertility=None):
    """0..1 quality score for the crop's current moisture and fertility.

    Fertility acts as a multiplier: low fertility caps growth even with ideal moisture.
    Old call sites that pass no fertility default to MAX_FERTILITY (full).
    """
    if fertility is None:
        fertility = MAX_FERTILITY
    m_lo, m_hi = prefs["moisture"]
    if moisture < m_lo:
        moisture_score = 0.1
    else:
        center = (m_lo + m_hi) / 2.0
        half   = max(1.0, (m_hi - m_lo) / 2.0)
        if moisture <= m_hi:
            moisture_score = max(0.3, 1.0 - abs(moisture - center) / half)
        else:
            over = moisture - m_hi
            moisture_score = max(0.1, 0.6 - 0.15 * over)

    fert_factor = max(0.2, fertility / MAX_FERTILITY)
    return moisture_score * fert_factor


def growth_delta(prefs, moisture, fertility=None):
    """Progress points added this tick. Zero if below the crop's minimum moisture."""
    m_lo, _ = prefs["moisture"]
    if moisture < m_lo:
        return 0
    delta = int(round(care_score(prefs, moisture, fertility) * GROWTH_DELTA_MAX))
    delta = max(GROWTH_DELTA_MIN, delta)
    speed = prefs.get("growth_speed", 1.0)
    return max(1, int(round(delta * speed)))


def yield_multiplier(avg_care):
    """Final yield multiplier given the running-average care across growth."""
    c = max(0.0, min(1.0, avg_care))
    return YIELD_MIN_MULT + (YIELD_MAX_MULT - YIELD_MIN_MULT) * c
