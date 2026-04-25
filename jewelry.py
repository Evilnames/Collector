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
    "ring":     {"label": "Ring",     "max_slots": 3, "base_value": 80},
    "necklace": {"label": "Necklace", "max_slots": 4, "base_value": 120},
    "bracelet": {"label": "Bracelet", "max_slots": 3, "base_value": 90},
    "pendant":  {"label": "Pendant",  "max_slots": 2, "base_value": 70},
    "crown":    {"label": "Crown",    "max_slots": 5, "base_value": 200},
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

# Jewelry type display order for codex
JEWELRY_TYPE_ORDER = list(JEWELRY_TYPES.keys())


def calculate_value(jewelry, player, master_jeweler=False):
    """Return gold value for a Jewelry piece based on slotted gems/rocks."""
    jtype = JEWELRY_TYPES.get(jewelry.jewelry_type, {})
    total = jtype.get("base_value", 80)

    gem_index  = {g.uid: g for g in player.gems}
    rock_index = {r.uid: r for r in player.rocks}

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

    if master_jeweler:
        total = int(total * 1.25)
    return total


def make_uid(seed, counter):
    raw = f"jewelry_{seed}_{counter}"
    return hashlib.md5(raw.encode()).hexdigest()[:12]
