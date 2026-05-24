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
    "tournament": [
        "dynasty_tournament_sash", "dynasty_parade_lance",
        "dynasty_ceremonial_bow", "dynasty_ancestral_spurs",
        "dynasty_herald_tabard",
    ],
    "royal_hunt": [
        "dynasty_hawk_glove", "dynasty_hunting_cloak",
        "dynasty_ceremonial_bow", "dynasty_ancestral_spurs",
        "dynasty_royal_boots",
    ],
    "state_banquet": [
        "dynasty_imperial_tea_set", "dynasty_royal_goblet",
        "dynasty_state_plate", "dynasty_tasting_spoon",
        "dynasty_reception_tureen", "dynasty_royal_saltcellar",
        "dynasty_royal_recipe_book", "dynasty_court_chopsticks",
    ],
    "royal_progress": [
        "dynasty_royal_boots", "dynasty_walking_cane",
        "dynasty_court_slippers", "dynasty_state_robe",
        "dynasty_procession_banner", "dynasty_throne_footstool",
    ],
    "archive_compilation": [
        "dynasty_book_births", "dynasty_book_cadet_roll",
        "dynasty_book_coronations", "dynasty_book_court_etiquette",
        "dynasty_book_deaths", "dynasty_book_dynastic_law",
        "dynasty_book_heir_roll", "dynasty_book_marriages",
    ],
    "regency": [
        "dynasty_dowager_crown", "dynasty_consort_robe",
        "dynasty_queen_gown", "dynasty_acknowledgment_letter",
        "dynasty_recall_heir",
    ],
    "garden_fete": [
        "dynasty_garden_pavilion_key", "dynasty_painted_fan",
        "dynasty_lotus_pendant", "dynasty_crescent_pendant",
        "dynasty_sun_pendant", "dynasty_court_anklet",
        "dynasty_topaz_circlet",
    ],
    "investiture_of_state": [
        "dynasty_ruby_pin_of_state", "dynasty_sapphire_earrings",
        "dynasty_topaz_circlet", "dynasty_state_robe",
        "dynasty_state_plate", "dynasty_herald_tabard",
    ],
    "royal_betrothal": [
        "dynasty_betrothal_brooch", "dynasty_engagement_necklace",
        "dynasty_engagement_proposal", "dynasty_first_marriage_locket",
        "dynasty_signet_bridal",
    ],
    "prince_of_age": [
        "dynasty_heir_first_robe", "dynasty_heir_horoscope",
        "dynasty_investiture_sword", "dynasty_recognition_locket",
        "dynasty_heir_bracelet", "dynasty_investiture_cap",
    ],
    "royal_pilgrimage": [
        "dynasty_anointing_oil", "dynasty_anointing_spoon",
        "dynasty_walking_cane", "dynasty_royal_boots",
        "dynasty_state_robe",
    ],
    "harvest_festival": [
        "dynasty_royal_recipe_book", "dynasty_tasting_spoon",
        "dynasty_reception_tureen", "dynasty_court_chopsticks",
        "dynasty_painted_fan", "dynasty_state_plate",
    ],
    "alliance_signed": [
        "dynasty_oath_of_fealty", "dynasty_diplomatic_missive",
        "dynasty_cipher_key", "dynasty_rival_treaty",
        "dynasty_pigeon_tube",
    ],
    "rebellion_quelled": [
        "dynasty_parade_lance", "dynasty_ceremonial_bow",
        "dynasty_herald_tabard", "dynasty_oath_of_fealty",
        "dynasty_ancestral_spurs",
    ],
    "plague_at_court": [
        "dynasty_mourning_robe", "dynasty_mourning_veil",
        "dynasty_augur_liver", "dynasty_omens_book",
        "dynasty_astrologer_chart", "dynasty_funeral_sweet",
    ],
    "bastard_recognized": [
        "dynasty_bastard_signet", "dynasty_book_bastard_roll",
        "dynasty_acknowledgment_letter", "dynasty_legitimization",
        "dynasty_cadet_brooch", "dynasty_signet_cadet",
    ],
    "dowager_council": [
        "dynasty_dowager_crown", "dynasty_queen_gown",
        "dynasty_consort_robe", "dynasty_signet_cadet",
        "dynasty_acknowledgment_letter",
    ],
    "royal_pardon": [
        "dynasty_succession_decree", "dynasty_acknowledgment_letter",
        "dynasty_oath_of_fealty", "dynasty_recall_heir",
    ],
    "state_visit": [
        "dynasty_state_robe", "dynasty_state_plate",
        "dynasty_herald_tabard", "dynasty_imperial_tea_set",
        "dynasty_diplomatic_missive", "dynasty_reception_tureen",
    ],
    "patronage_of_arts": [
        "dynasty_court_sketch", "dynasty_court_pipa",
        "dynasty_painted_fan", "dynasty_lineage_mural",
        "dynasty_bust_lacquer", "dynasty_storyteller_drum",
    ],
    "monastery_founded": [
        "dynasty_anointing_oil", "dynasty_omens_book",
        "dynasty_dream_journal", "dynasty_lineage_mural",
        "dynasty_iching_stalks",
    ],
    "military_review": [
        "dynasty_parade_lance", "dynasty_ancestral_spurs",
        "dynasty_herald_tabard", "dynasty_ceremonial_bow",
        "dynasty_procession_banner", "dynasty_acclamation_horn",
    ],
    "assassination_attempt": [
        "dynasty_bastard_signet", "dynasty_cipher_key",
        "dynasty_concubine_ring", "dynasty_pigeon_tube",
        "dynasty_disinheritance",
    ],
    "heir_fostered": [
        "dynasty_heir_first_letter", "dynasty_heir_first_robe",
        "dynasty_toy_first_book", "dynasty_recall_heir",
        "dynasty_acknowledgment_letter",
    ],
    "silver_jubilee": [
        "dynasty_coronation_cup", "dynasty_coronation_robe",
        "dynasty_state_robe", "dynasty_parade_lance",
        "dynasty_lineage_mural", "dynasty_acclamation_horn",
    ],
    "royal_audience": [
        "dynasty_throne_footstool", "dynasty_royal_goblet",
        "dynasty_court_slippers", "dynasty_herald_tabard",
        "dynasty_state_robe",
    ],
    "court_ball": [
        "dynasty_masquerade_mask", "dynasty_painted_fan",
        "dynasty_court_pipa", "dynasty_jester_bells",
        "dynasty_court_anklet", "dynasty_queen_gown",
    ],
    "mint_dedication": [
        "dynasty_diviner_coin", "dynasty_state_plate",
        "dynasty_herald_tabard", "dynasty_succession_decree",
        "dynasty_ruby_pin_of_state",
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
    if kind == "tournament":
        return f"Lances are blessed for the grand tournament of {realm}."
    if kind == "royal_hunt":
        return f"{house} rides out from {realm} on a royal hunt."
    if kind == "state_banquet":
        return f"A state banquet honors visiting envoys at {realm}."
    if kind == "royal_progress":
        return f"The royal progress of {house} winds through the towns of {realm}."
    if kind == "archive_compilation":
        return f"Court scribes of {realm} bind a new volume of the {house} chronicles."
    if kind == "regency":
        return f"A regency is proclaimed in {realm} — {house} rules in trust."
    if kind == "garden_fete":
        return f"Lanterns light the palace gardens of {realm} for a midsummer fete."
    if kind == "investiture_of_state":
        return f"Great officers of {realm} receive their seals from {house}."
    if kind == "royal_betrothal":
        return f"A betrothal is announced at the court of {realm}."
    if kind == "prince_of_age":
        return f"The heir of {house} comes of age in {realm}."
    if kind == "royal_pilgrimage":
        return f"{house} sets out on a royal pilgrimage from {realm}."
    if kind == "harvest_festival":
        return f"{realm} celebrates the harvest with a court-led festival."
    if kind == "alliance_signed":
        return f"{realm} signs a binding alliance with a neighboring crown."
    if kind == "rebellion_quelled":
        return f"A rebellion against {house} is put down in {realm}."
    if kind == "plague_at_court":
        return f"Sickness sweeps the court of {realm} — physicians attend {house}."
    if kind == "bastard_recognized":
        return f"A natural-born child of {house} is recognized in {realm}."
    if kind == "dowager_council":
        return f"The dowager of {house} convenes a council of state in {realm}."
    if kind == "royal_pardon":
        return f"{house} issues a royal pardon in {realm}."
    if kind == "state_visit":
        return f"A foreign monarch arrives in {realm} on a state visit."
    if kind == "patronage_of_arts":
        return f"{house} bestows patronage on the artists of {realm}."
    if kind == "monastery_founded":
        return f"{house} endows a new monastery in {realm}."
    if kind == "military_review":
        return f"{house} reviews the assembled hosts of {realm}."
    if kind == "assassination_attempt":
        return f"An assassin is foiled at the court of {realm}."
    if kind == "heir_fostered":
        return f"An heir of {house} is sent to be fostered abroad."
    if kind == "silver_jubilee":
        return f"{realm} marks a silver jubilee of {house}'s reign."
    if kind == "royal_audience":
        return f"{house} holds a grand audience in {realm}."
    if kind == "court_ball":
        return f"A masked ball lights the halls of {realm}."
    if kind == "mint_dedication":
        return f"A new royal coinage is struck in {realm} under {house}."
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
        ("tournament", 4), ("royal_hunt", 4), ("state_banquet", 4),
        ("royal_progress", 3), ("archive_compilation", 2),
        ("regency", 1), ("garden_fete", 3),
        ("investiture_of_state", 2),
        ("royal_betrothal", 4), ("prince_of_age", 3),
        ("royal_pilgrimage", 2), ("harvest_festival", 4),
        ("alliance_signed", 3), ("rebellion_quelled", 2),
        ("plague_at_court", 1), ("bastard_recognized", 2),
        ("dowager_council", 2), ("royal_pardon", 2),
        ("state_visit", 3), ("patronage_of_arts", 4),
        ("monastery_founded", 2), ("military_review", 3),
        ("assassination_attempt", 1), ("heir_fostered", 2),
        ("silver_jubilee", 1), ("royal_audience", 4),
        ("court_ball", 4), ("mint_dedication", 2),
    ]
    kinds, weight_vals = zip(*weights)
    kind = rng.choices(kinds, weights=weight_vals, k=1)[0]

    drops = _grant_drops(player, kind, rng)
    msg = _format_message(kind, kingdom, house)
    # Politics hook — let the live political layer react. Map to a random
    # known region since kingdoms (plan-level) and regions (runtime) are
    # separate id spaces.
    try:
        from politics import on_dynasty_event, HOUSE_STATES
        from towns import REGIONS
        if REGIONS:
            pool = list(REGIONS.keys())
            picked_rid = rng.choice(pool)
            on_dynasty_event(kind, picked_rid, getattr(world, "day_count", 0))
    except Exception:
        pass
    notes = getattr(player, "pending_notifications", None)
    if notes is not None:
        # The HUD tuple format is (category, text, rarity_or_tone)
        notes.append(("Royal News", msg, "royal"))
        if drops:
            from items import ITEMS as _ITEMS
            preview = ", ".join(_ITEMS.get(i, {}).get("name", i) for i in drops[:2])
            extra = "" if len(drops) <= 2 else f" + {len(drops) - 2} more"
            notes.append(("Royal Gift", f"{preview}{extra}", "royal"))
