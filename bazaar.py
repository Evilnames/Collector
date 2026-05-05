"""Bazaar system — auction lots, rival bidders, and fence trades."""
import random

# ---------------------------------------------------------------------------
# Lot definitions
# ---------------------------------------------------------------------------

# item_id: (display_name, (qty_min, qty_max), base_price, rarity, category, swatch_color)
_LOT_DEFS = {
    "gold_nugget":         ("Gold Nugget",           (1, 3),  18, "uncommon", "material",   (218, 182,  55)),
    "crystal_shard":       ("Crystal Shard",         (1, 2),  32, "rare",     "material",   ( 90, 220, 220)),
    "ruby":                ("Ruby",                  (1, 1),  55, "rare",     "material",   (210,  35,  35)),
    "obsidian_slab":       ("Obsidian Slab",         (1, 3),  22, "uncommon", "material",   ( 60,  45,  75)),
    "iron_chunk":          ("Iron Chunk",            (3, 6),   5, "common",   "material",   (185, 140, 110)),
    "coal":                ("Coal",                  (4, 8),   3, "common",   "material",   ( 55,  55,  55)),
    "wool":                ("Wool",                  (2, 5),   6, "common",   "material",   (235, 235, 235)),
    "lumber":              ("Lumber",                (4, 8),   4, "common",   "material",   (139,  90,  43)),
    "dye_extract_crimson": ("Dye (Crimson)",          (1, 2),  18, "uncommon", "material",   (185,  35,  45)),
    "dye_extract_cobalt":  ("Dye (Cobalt)",           (1, 2),  18, "uncommon", "material",   ( 55,  90, 185)),
    "dye_extract_golden":  ("Dye (Golden)",           (1, 2),  18, "uncommon", "material",   (215, 175,  40)),
    "dye_extract_violet":  ("Dye (Violet)",           (1, 2),  18, "uncommon", "material",   (130,  65, 195)),
    "dye_extract_verdant": ("Dye (Verdant)",          (1, 2),  18, "uncommon", "material",   ( 60, 148,  75)),
    "health_potion":       ("Health Potion",         (1, 2),  18, "uncommon", "consumable", (220,  60,  80)),
    "luck_potion":         ("Luck Potion",           (1, 2),  25, "uncommon", "consumable", (255, 215,  50)),
    "speed_potion":        ("Speed Potion",          (1, 2),  20, "uncommon", "consumable", ( 80, 200, 240)),
    "mining_potion":       ("Mining Potion",         (1, 2),  20, "uncommon", "consumable", (200, 180,  60)),
    "health_potion_fine":  ("Health Potion (Fine)",  (1, 1),  35, "rare",     "consumable", (235,  80, 100)),
    "luck_potion_fine":    ("Luck Potion (Fine)",    (1, 1),  45, "rare",     "consumable", (255, 230,  80)),
    "fortune_elixir":      ("Fortune Elixir",        (1, 1),  65, "epic",     "consumable", (255, 230,  60)),
    "mining_elixir":       ("Mining Elixir",         (1, 1),  60, "epic",     "consumable", (255, 240,  90)),
    "swiftness_elixir":    ("Swiftness Elixir",      (1, 1),  60, "epic",     "consumable", (120, 240, 255)),
    "fortitude_elixir":    ("Fortitude Elixir",      (1, 1),  60, "epic",     "consumable", ( 90, 230, 165)),
    "red_wine":            ("Red Wine",              (1, 3),  15, "common",   "luxury",     (120,  30,  40)),
    "white_wine":          ("White Wine",            (1, 3),  15, "common",   "luxury",     (220, 210, 160)),
    "rose_wine":           ("Rosé Wine",             (1, 2),  18, "uncommon", "luxury",     (225, 145, 155)),
    "sparkling_wine":      ("Sparkling Wine",        (1, 2),  22, "uncommon", "luxury",     (240, 225, 180)),
    "dessert_wine":        ("Dessert Wine",          (1, 2),  25, "uncommon", "luxury",     (160,  95,  30)),
    "whiskey":             ("Whiskey",               (1, 2),  18, "common",   "luxury",     (180, 120,  40)),
    "rum":                 ("Rum",                   (1, 2),  18, "common",   "luxury",     (220, 160,  60)),
    "gin":                 ("Gin",                   (1, 2),  18, "common",   "luxury",     (190, 225, 235)),
    "vodka":               ("Vodka",                 (1, 2),  18, "common",   "luxury",     (230, 235, 240)),
    "wheat_beer":          ("Wheat Beer",            (2, 4),   8, "common",   "luxury",     (235, 220, 140)),
    "barleywine":          ("Barleywine",            (1, 2),  14, "common",   "luxury",     (165,  85,  25)),
    "pepper":              ("Pepper",                (2, 5),   6, "common",   "food",       (215,  65,  30)),
    "saffron":             ("Saffron",               (1, 3),  12, "uncommon", "food",       (215, 130,  30)),
    "olive":               ("Olive",                 (3, 6),   4, "common",   "food",       ( 60,  80,  45)),
    "cheese":              ("Cheese",                (1, 3),  10, "common",   "food",       (240, 210,  80)),
    "honey_jar":           ("Honey Jar",             (1, 3),  20, "uncommon", "food",       (235, 165,  30)),
    "honey_jar_fine":      ("Honey Jar (Fine)",      (1, 2),  45, "rare",     "food",       (245, 180,  40)),
    "honey_jar_artisan":   ("Honey Jar (Artisan)",   (1, 1),  85, "epic",     "food",       (255, 200,  55)),
    "beeswax":             ("Beeswax",               (2, 5),   8, "common",   "material",   (245, 220, 100)),
    "mead":                ("Mead",                  (1, 3),  22, "uncommon", "luxury",     (210, 155,  45)),
    "mead_fine":           ("Mead (Fine)",           (1, 2),  48, "rare",     "luxury",     (225, 170,  55)),
    "mead_reserve":        ("Mead (Reserve)",        (1, 1),  90, "epic",     "luxury",     (245, 195,  70)),
}

# ---------------------------------------------------------------------------
# Biome lot pools
# ---------------------------------------------------------------------------

_BIOME_LOT_POOLS = {
    "mediterranean": ["red_wine", "white_wine", "olive", "saffron", "obsidian_slab",
                      "crystal_shard", "luck_potion", "health_potion", "cheese", "gold_nugget",
                      "sparkling_wine", "rum", "fortune_elixir", "dye_extract_crimson"],
    "desert":        ["saffron", "pepper", "gold_nugget", "ruby", "obsidian_slab",
                      "whiskey", "luck_potion", "fortune_elixir", "mining_elixir",
                      "crystal_shard", "health_potion_fine", "luck_potion_fine",
                      "dye_extract_golden", "dye_extract_cobalt"],
    "temperate":     ["iron_chunk", "coal", "wool", "lumber", "wheat_beer",
                      "barleywine", "health_potion", "speed_potion", "mining_potion",
                      "gold_nugget", "crystal_shard", "cheese", "luck_potion",
                      "dye_extract_verdant", "honey_jar", "beeswax", "mead"],
    "steppe":        ["wool", "lumber", "iron_chunk", "whiskey", "barleywine",
                      "gold_nugget", "health_potion", "fortitude_elixir", "speed_potion",
                      "coal", "ruby", "mining_potion", "dye_extract_golden"],
    "jungle":        ["pepper", "saffron", "rum", "red_wine", "crystal_shard",
                      "ruby", "luck_potion", "fortune_elixir", "swiftness_elixir",
                      "health_potion_fine", "gold_nugget", "obsidian_slab",
                      "dye_extract_verdant", "dye_extract_violet", "honey_jar_fine"],
    "east_asian":    ["saffron", "pepper", "vodka", "white_wine", "crystal_shard",
                      "ruby", "obsidian_slab", "mining_elixir", "luck_potion_fine",
                      "fortune_elixir", "swiftness_elixir", "gold_nugget",
                      "dye_extract_cobalt", "dye_extract_violet"],
    "coastal":       ["rum", "wheat_beer", "crystal_shard", "obsidian_slab",
                      "sparkling_wine", "health_potion", "speed_potion", "gold_nugget",
                      "lumber", "wool", "luck_potion", "gin", "swiftness_elixir",
                      "dye_extract_cobalt"],
    "alpine":        ["wool", "lumber", "coal", "barleywine", "whiskey",
                      "iron_chunk", "crystal_shard", "fortitude_elixir",
                      "health_potion_fine", "mining_elixir", "gold_nugget",
                      "obsidian_slab", "dye_extract_violet", "honey_jar", "beeswax", "mead_fine"],
    "silk_road":     ["saffron", "pepper", "gold_nugget", "ruby", "whiskey",
                      "vodka", "obsidian_slab", "crystal_shard", "fortune_elixir",
                      "luck_potion_fine", "mining_elixir", "fortitude_elixir",
                      "dye_extract_golden", "dye_extract_cobalt"],
}
_DEFAULT_LOT_POOL = ["iron_chunk", "coal", "wool", "lumber", "gold_nugget",
                     "crystal_shard", "health_potion", "luck_potion", "red_wine", "wheat_beer"]

# ---------------------------------------------------------------------------
# Rival bidder names by biome
# ---------------------------------------------------------------------------

_RIVAL_NAMES = {
    "mediterranean": ["Demetrios", "Sophia", "Nikolas", "Erastos", "Lydia"],
    "desert":        ["Tariq", "Fatima", "Hamid", "Layla", "Rashid"],
    "east_asian":    ["Wei Lin", "Mei", "Jin Bo", "Shan", "Yuki"],
    "steppe":        ["Batu", "Kara", "Tengri", "Arslan", "Nurgul"],
    "silk_road":     ["Ilkhan", "Zara", "Omar", "Selin", "Nasrin"],
    "jungle":        ["Atl", "Ixchel", "Talo", "Manik", "Citlali"],
    "coastal":       ["Barnabas", "Mira", "Sven", "Idunn", "Pol"],
    "alpine":        ["Konrad", "Hilde", "Urs", "Lisl", "Sigurd"],
    "temperate":     ["Oswald", "Brita", "Henning", "Lyra", "Marcus"],
}
_DEFAULT_RIVALS = ["Marcus", "Lyra", "Oswald", "Brita", "Henning"]

# ---------------------------------------------------------------------------
# Fence — items the fence buys from the player (item_id, qty, pay_per, flavor)
# ---------------------------------------------------------------------------

_FENCE_WANTS = [
    ("coal",              4,  5, "Fuel for the smelters"),
    ("iron_chunk",        3,  9, "Private commission"),
    ("lumber",            5,  7, "Building crew nearby"),
    ("wool",              3, 10, "Textile merchant contact"),
    ("gold_nugget",       2, 28, "Jewelry work"),
    ("crystal_shard",     2, 50, "Lens grinding"),
    ("obsidian_slab",     2, 32, "Blade commission"),
    ("ruby",              1, 80, "Collector's piece"),
    ("red_wine",          2, 22, "Private buyer"),
    ("whiskey",           2, 26, "Long voyage ahead"),
    ("pepper",            4,  9, "Spice merchant"),
    ("saffron",           3, 18, "Cooking school order"),
    ("cheese",            3, 16, "Guest banquet tonight"),
    ("dye_extract_crimson", 2, 28, "Fashion house contact"),
    ("dye_extract_golden",  2, 28, "Tapestry weavers"),
    ("luck_potion",       1, 35, "Anxious merchant"),
    ("health_potion",     2, 28, "Caravan medic"),
    ("fortune_elixir",    1, 90, "Discreet buyer"),
    ("honey_jar",         2, 30, "Pastry chef commission"),
    ("honey_jar_fine",    1, 68, "Apothecary order"),
    ("beeswax",           3, 12, "Candlemaker's supply"),
    ("mead",              2, 32, "Celebration supply"),
    ("mead_fine",         1, 70, "Noble household order"),
]

# ---------------------------------------------------------------------------
# Shared display constants (imported by UI)
# ---------------------------------------------------------------------------

RARITY_COLORS = {
    "common":    (180, 180, 180),
    "uncommon":  (120, 220, 100),
    "rare":      (120, 180, 255),
    "epic":      (190, 100, 240),
    "legendary": (255, 215,  60),
}
RARITY_BG = {
    "common":    (35, 35, 35),
    "uncommon":  (28, 45, 28),
    "rare":      (25, 35, 65),
    "epic":      (45, 28, 60),
    "legendary": (55, 45, 10),
}
CATEGORY_LABELS = {
    "material":   "MATERIAL",
    "consumable": "CONSUMABLE",
    "luxury":     "LUXURY",
    "food":       "FOOD",
}

# ---------------------------------------------------------------------------
# AuctionLot
# ---------------------------------------------------------------------------

class AuctionLot:
    """One lot up for sealed bidding."""
    __slots__ = ("item_id", "display_name", "qty", "base_price",
                 "rarity", "category", "swatch_color", "rival_max")

    def __init__(self, item_id, display_name, qty, base_price,
                 rarity, category, swatch_color, rival_max):
        self.item_id      = item_id
        self.display_name = display_name
        self.qty          = qty
        self.base_price   = base_price
        self.rarity       = rarity
        self.category     = category
        self.swatch_color = swatch_color
        self.rival_max    = rival_max   # rivals will bid up to this amount

# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------

def generate_bazaar_day(region_seed: int, day_count: int,
                        biome: str = "temperate") -> list:
    """Return 5 AuctionLots for today (deterministic per region + day)."""
    rng  = random.Random(region_seed ^ (day_count * 0x6b4f5a3d))
    pool = _BIOME_LOT_POOLS.get(biome, _DEFAULT_LOT_POOL)

    chosen = rng.sample(pool, min(5, len(pool)))
    if len(chosen) < 5:
        extras = [k for k in _DEFAULT_LOT_POOL if k not in chosen]
        chosen += rng.sample(extras, 5 - len(chosen))

    lots = []
    for item_id in chosen:
        defn = _LOT_DEFS.get(item_id)
        if defn is None:
            continue
        name, qty_range, base, rarity, cat, swatch = defn
        qty        = rng.randint(*qty_range)
        total_base = base * qty
        rival_max  = int(total_base * rng.uniform(0.75, 2.4))
        lots.append(AuctionLot(
            item_id=item_id, display_name=name, qty=qty,
            base_price=total_base, rarity=rarity, category=cat,
            swatch_color=swatch, rival_max=rival_max,
        ))
    return lots


def generate_fence_wants(region_seed: int, day_count: int) -> list:
    """Return 3 fence buy-slots for today."""
    rng = random.Random(region_seed ^ (day_count * 0x1f7c4b9e))
    return list(rng.sample(_FENCE_WANTS, 3))


def get_rival_names(biome: str, rng: random.Random, n: int = 3) -> list:
    pool = _RIVAL_NAMES.get(biome, _DEFAULT_RIVALS)
    return rng.sample(pool, min(n, len(pool)))

# ---------------------------------------------------------------------------
# Scheduling
# ---------------------------------------------------------------------------

def is_bazaar_day(region_seed: int, day_count: int) -> bool:
    """True on 3 out of every 5 days for this region."""
    offset = region_seed % 5
    return (day_count + offset) % 5 in (0, 1, 2)


def days_until_bazaar(region_seed: int, day_count: int) -> int:
    for d in range(1, 6):
        if is_bazaar_day(region_seed, day_count + d):
            return d
    return 1
