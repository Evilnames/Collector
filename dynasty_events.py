"""Runtime dynasty events.

Each in-game day, a small chance an event fires somewhere in the realm:
coronation, royal marriage, succession, royal death, royal birth, court
intrigue. The event is announced to the player and a thematic bundle of
dynasty heirlooms is dropped into their inventory — pageant courier bringing
mementos, royal pyre ashes blown on the wind, etc.

This is the runtime counterpart to the worldgen-only chronicle text in
worldgen/history/. We don't mutate the plan; we just sample names/houses
from it for flavor and drop items keyed off the event kind.
"""
import random

# Event kind → (notification verb, dynasty item-cluster names).
# Item keys must exist in items.py. See cities._DYNASTY_HEIRLOOM_POOL for
# the source list — these are a subset partitioned by narrative event.
_EVENT_CLUSTERS = {
    "coronation": [
        "dynasty_coronation_carpet", "dynasty_coronation_cup",
        "dynasty_coronation_cushion", "dynasty_coronation_dish",
        "dynasty_coronation_robe", "dynasty_coronation_trumpet",
        "dynasty_crown_bearer_cushion", "dynasty_procession_banner",
        "dynasty_investiture_cap", "dynasty_investiture_cloak",
        "dynasty_investiture_sword", "dynasty_acclamation_horn",
        "dynasty_anointing_oil", "dynasty_anointing_spoon",
        "dynasty_herald_tabard", "dynasty_parade_lance",
        "dynasty_state_robe",
    ],
    "marriage": [
        "dynasty_betrothal_brooch", "dynasty_bridal_dagger",
        "dynasty_bridal_feast_recipe", "dynasty_bridal_gown",
        "dynasty_bridal_portrait", "dynasty_engagement_necklace",
        "dynasty_engagement_proposal", "dynasty_first_marriage_locket",
        "dynasty_marriage_bangles", "dynasty_signet_bridal",
        "dynasty_wedding_band_pair",
    ],
    "succession": [
        "dynasty_heir_bracelet", "dynasty_heir_first_letter",
        "dynasty_heir_first_robe", "dynasty_heir_horoscope",
        "dynasty_recognition_locket", "dynasty_succession_decree",
        "dynasty_acknowledgment_letter",
    ],
    "abdication": [
        "dynasty_abdication_letter", "dynasty_recall_heir",
        "dynasty_legitimization", "dynasty_disinheritance",
        "dynasty_cadet_brooch", "dynasty_cadet_robe", "dynasty_signet_cadet",
    ],
    "royal_birth": [
        "dynasty_toy_crib_coverlet", "dynasty_toy_doll",
        "dynasty_toy_first_book", "dynasty_toy_kite",
        "dynasty_toy_locket", "dynasty_toy_practice_sword",
        "dynasty_toy_rattle",
    ],
    "royal_death": [
        "dynasty_death_shroud", "dynasty_funeral_sweet",
        "dynasty_mourning_robe", "dynasty_mourning_veil",
        "dynasty_pyre_ashes", "dynasty_royal_shroud",
        "dynasty_walking_cane", "throne_ash",
    ],
    "court_ritual": [
        "dynasty_astrologer_chart", "dynasty_augur_liver",
        "dynasty_diviner_coin", "dynasty_iching_stalks",
        "dynasty_omens_book", "dynasty_dream_journal",
    ],
    "court_culture": [
        "dynasty_backgammon_set", "dynasty_chaturanga_board",
        "dynasty_go_board", "dynasty_pachisi_cloth",
        "dynasty_shogi_board", "dynasty_bust_lacquer",
        "dynasty_court_pipa", "dynasty_court_sketch",
        "dynasty_painted_fan", "dynasty_masquerade_mask",
        "dynasty_jester_bells", "dynasty_storyteller_drum",
        "dynasty_lineage_mural",
    ],
    "diplomacy": [
        "dynasty_diplomatic_missive", "dynasty_oath_of_fealty",
        "dynasty_rival_treaty", "dynasty_cipher_key",
        "dynasty_pigeon_tube",
    ],
    "intrigue": [
        "dynasty_bastard_signet", "dynasty_book_bastard_roll",
        "dynasty_concubine_ring",
    ],
}

# Roll rate: one event roll per day, ~1/12 chance fires. Average ~30/year.
_DAILY_ROLL_CHANCE = 1.0 / 12.0
_DROPS_PER_EVENT = (2, 4)  # min/max items granted


def _alive_kingdoms(world):
    plan = getattr(world, "plan", None)
    if plan is None:
        return []
    return [k for k in plan.kingdoms.values() if k.fallen_year < 0]


def _format_message(kind: str, kingdom, dyn_house: str) -> str:
    """Short notification line. (category, text, tone) format expected by HUD."""
    realm = getattr(kingdom, "name", "the realm")
    house = dyn_house or "the ruling house"
    if kind == "coronation":
        return f"A new monarch is crowned in {realm} — {house} ascends."
    if kind == "marriage":
        return f"A royal marriage is sealed at the court of {realm}."
    if kind == "succession":
        return f"The heir-apparent of {house} is presented to the court of {realm}."
    if kind == "abdication":
        return f"The throne of {realm} changes hands — {house} steps aside."
    if kind == "royal_birth":
        return f"A child is born to {house} of {realm}."
    if kind == "royal_death":
        return f"A pyre is lit in {realm} — {house} mourns."
    if kind == "court_ritual":
        return f"Augurs read omens in the court of {realm}."
    if kind == "court_culture":
        return f"A grand pageant unfolds at the court of {realm}."
    if kind == "diplomacy":
        return f"Heralds ride between {realm} and a rival court."
    if kind == "intrigue":
        return f"Whispers of scandal flutter through {realm}."
    return f"News from the court of {realm}."


def _grant_drops(player, kind: str, rng: random.Random) -> list:
    pool = _EVENT_CLUSTERS.get(kind)
    if not pool:
        return []
    inv = getattr(player, "inventory", None)
    if inv is None:
        return []
    n = rng.randint(*_DROPS_PER_EVENT)
    picks = rng.sample(pool, min(n, len(pool)))
    for item_id in picks:
        inv[item_id] = inv.get(item_id, 0) + 1
    return picks


def tick_dynasty_events(world, player) -> None:
    """Called once per in-game day. Rolls for and possibly fires one event."""
    if player is None or not hasattr(player, "inventory"):
        return
    alive = _alive_kingdoms(world)
    if not alive:
        return
    # Seed by day so save/reload doesn't re-fire.
    seed = (getattr(world, "seed", 0) ^ getattr(world, "day_count", 0) * 0x9E3779B1) & 0xFFFFFFFF
    rng = random.Random(seed)
    if rng.random() >= _DAILY_ROLL_CHANCE:
        return

    kingdom = rng.choice(alive)
    plan = world.plan
    dyn = plan.dynasties.get(getattr(kingdom, "dynasty_id", -1))
    house = getattr(dyn, "house_name", "") if dyn is not None else ""

    # Weights skewed toward common ceremonial events.
    weights = [
        ("coronation", 3), ("marriage", 5), ("succession", 4),
        ("abdication", 1), ("royal_birth", 4), ("royal_death", 3),
        ("court_ritual", 3), ("court_culture", 5),
        ("diplomacy", 3), ("intrigue", 2),
    ]
    kinds, weight_vals = zip(*weights)
    kind = rng.choices(kinds, weights=weight_vals, k=1)[0]

    drops = _grant_drops(player, kind, rng)
    msg = _format_message(kind, kingdom, house)
    notes = getattr(player, "pending_notifications", None)
    if notes is not None:
        # The HUD tuple format is (category, text, rarity_or_tone)
        notes.append(("Royal News", msg, "royal"))
        if drops:
            from items import ITEMS as _ITEMS
            preview = ", ".join(_ITEMS.get(i, {}).get("name", i) for i in drops[:2])
            extra = "" if len(drops) <= 2 else f" + {len(drops) - 2} more"
            notes.append(("Royal Gift", f"{preview}{extra}", "royal"))
