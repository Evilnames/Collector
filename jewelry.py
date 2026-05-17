import hashlib
from dataclasses import dataclass, field


@dataclass
class Jewelry:
    uid: str
    jewelry_type: str    # key in JEWELRY_TYPES
    slot_count: int      # 1 – max_slots for this type
    slots: list          # list of {"kind": "gem"|"rock", "uid": str} or None per slot
    custom_name: str     # player-given name
    seed: int


JEWELRY_TYPES = {
    "ring":      {"label": "Ring",      "max_slots": 3, "base_value": 80},
    "necklace":  {"label": "Necklace",  "max_slots": 4, "base_value": 120},
    "bracelet":  {"label": "Bracelet",  "max_slots": 3, "base_value": 90},
    "pendant":   {"label": "Pendant",   "max_slots": 2, "base_value": 70},
    "crown":     {"label": "Crown",     "max_slots": 5, "base_value": 200},
    "earring":   {"label": "Earring",   "max_slots": 2, "base_value": 60},
    "brooch":    {"label": "Brooch",    "max_slots": 3, "base_value": 85},
    "tiara":     {"label": "Tiara",     "max_slots": 4, "base_value": 160},
    "anklet":    {"label": "Anklet",    "max_slots": 3, "base_value": 75},
    "cufflinks": {"label": "Cufflinks", "max_slots": 2, "base_value": 70},
    "circlet":   {"label": "Circlet",   "max_slots": 3, "base_value": 130},
    "choker":    {"label": "Choker",    "max_slots": 3, "base_value": 95},
    "signet":    {"label": "Signet",    "max_slots": 1, "base_value": 65},
    "amulet":    {"label": "Amulet",    "max_slots": 3, "base_value": 100},
    "tiepin":    {"label": "Tiepin",    "max_slots": 1, "base_value": 50},
}

RARITY_VALUES = {
    "common":    10,
    "uncommon":  25,
    "rare":      60,
    "epic":     150,
    "legendary":400,
}

OPTICAL_BONUS = {
    "chatoyancy":   40,
    "asterism":     50,
    "color_change": 80,
    "fluorescence": 30,
    "adularescence":35,
}

# Extra gold for pearl luster quality on top of rarity value
PEARL_LUSTER_BONUS = {
    "matte":       0,
    "satin":      10,
    "lustrous":   25,
    "iridescent": 50,
}

# Jewelry type display order for codex
JEWELRY_TYPE_ORDER = list(JEWELRY_TYPES.keys())


def calculate_value(jewelry, player, master_jeweler=False):
    """Return gold value for a Jewelry piece based on slotted gems/rocks/pearls."""
    jtype = JEWELRY_TYPES.get(jewelry.jewelry_type, {})
    total = jtype.get("base_value", 80)

    gem_index   = {g.uid: g for g in player.gems}
    rock_index  = {r.uid: r for r in player.rocks}
    pearl_index = {p.uid: p for p in getattr(player, "pearls", [])}

    for slot in jewelry.slots:
        if slot is None:
            continue
        if slot["kind"] == "gem":
            gem = gem_index.get(slot["uid"])
            if gem:
                total += RARITY_VALUES.get(gem.rarity, 10)
                total += OPTICAL_BONUS.get(gem.optical_effect, 0)
        elif slot["kind"] == "rock":
            rock = rock_index.get(slot["uid"])
            if rock:
                total += RARITY_VALUES.get(rock.rarity, 10)
        elif slot["kind"] == "pearl":
            pearl = pearl_index.get(slot["uid"])
            if pearl:
                total += RARITY_VALUES.get(pearl.rarity, 10)
                total += PEARL_LUSTER_BONUS.get(pearl.luster, 0)

    if master_jeweler:
        total = int(total * 1.25)
    return total


def pearl_raw_value(pearl):
    """Gold value for selling a loose pearl (no jewelry wrapping)."""
    return RARITY_VALUES.get(pearl.rarity, 10) + PEARL_LUSTER_BONUS.get(pearl.luster, 0)


def make_uid(seed, counter):
    raw = f"jewelry_{seed}_{counter}"
    return hashlib.md5(raw.encode()).hexdigest()[:12]
