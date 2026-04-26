"""Dynamic NPC preference system.

Each collectible system registers itself with a PREFERENCE_PARAMS dict (describing
what sub-preferences are available) and a scorer function.  NPC preferences are
derived from a seeded RNG — no hardcoded per-NPC-type lists.

To add a new system: call register_system() with your system_id, display name,
PREFERENCE_PARAMS dict, and scorer callable.  Nothing else needs to change.
"""
import random

# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

PREFERENCE_SYSTEMS: dict[str, dict] = {}


def register_system(system_id: str, display_name: str,
                    preference_params: dict, scorer):
    """Register a collectible system for NPC preferences.

    preference_params: {param_name: [possible_values, ...], ...}
    scorer: fn(sub_prefs: dict, item: Any) -> float  (-1.0 to +1.0)
    """
    PREFERENCE_SYSTEMS[system_id] = {
        "display_name": display_name,
        "params": preference_params,
        "scorer": scorer,
    }


# ---------------------------------------------------------------------------
# Built-in system registrations  (each imports lazily to avoid circular deps)
# ---------------------------------------------------------------------------

def _score_fish(sub_prefs, item):
    from fish import Fish
    if not isinstance(item, Fish):
        return 0.0
    score = 0.0
    wanted_rarity = sub_prefs.get("rarity")
    if wanted_rarity and item.rarity == wanted_rarity:
        score += 0.6
    elif wanted_rarity:
        rarities = ["common", "uncommon", "rare", "epic", "legendary"]
        dist = abs(rarities.index(item.rarity) - rarities.index(wanted_rarity))
        score += max(-0.3, 0.3 - dist * 0.2)
    wanted_habitat = sub_prefs.get("habitat")
    if wanted_habitat and item.habitat == wanted_habitat:
        score += 0.4
    return max(-1.0, min(1.0, score))


def _score_fossil(sub_prefs, item):
    from fossils import Fossil
    if not isinstance(item, Fossil):
        return 0.0
    score = 0.0
    wanted_rarity = sub_prefs.get("rarity")
    if wanted_rarity and item.rarity == wanted_rarity:
        score += 0.6
    elif wanted_rarity:
        rarities = ["common", "uncommon", "rare", "epic", "legendary"]
        dist = abs(rarities.index(item.rarity) - rarities.index(wanted_rarity))
        score += max(-0.3, 0.3 - dist * 0.2)
    wanted_age = sub_prefs.get("age")
    if wanted_age and item.age == wanted_age:
        score += 0.4
    return max(-1.0, min(1.0, score))


def _score_rock(sub_prefs, item):
    from rocks import Rock
    if not isinstance(item, Rock):
        return 0.0
    score = 0.0
    wanted_rarity = sub_prefs.get("rarity")
    if wanted_rarity and item.rarity == wanted_rarity:
        score += 1.0
    elif wanted_rarity:
        rarities = ["common", "uncommon", "rare", "epic", "legendary"]
        dist = abs(rarities.index(item.rarity) - rarities.index(wanted_rarity))
        score += max(-0.4, 0.4 - dist * 0.2)
    return max(-1.0, min(1.0, score))


def _score_gem(sub_prefs, item):
    from gemstones import Gemstone
    if not isinstance(item, Gemstone):
        return 0.0
    score = 0.0
    wanted_rarity = sub_prefs.get("rarity")
    if wanted_rarity and item.rarity == wanted_rarity:
        score += 0.7
    elif wanted_rarity:
        rarities = ["common", "uncommon", "rare", "epic", "legendary"]
        dist = abs(rarities.index(item.rarity) - rarities.index(wanted_rarity))
        score += max(-0.3, 0.3 - dist * 0.2)
    wanted_cut = sub_prefs.get("cut")
    if wanted_cut and getattr(item, "cut", None) == wanted_cut:
        score += 0.3
    return max(-1.0, min(1.0, score))


def _score_wildflower(sub_prefs, item):
    from wildflowers import Wildflower
    if not isinstance(item, Wildflower):
        return 0.0
    score = 0.0
    wanted_rarity = sub_prefs.get("rarity")
    if wanted_rarity and item.rarity == wanted_rarity:
        score += 0.6
    elif wanted_rarity:
        rarities = ["common", "uncommon", "rare", "epic", "legendary"]
        dist = abs(rarities.index(item.rarity) - rarities.index(wanted_rarity))
        score += max(-0.3, 0.3 - dist * 0.2)
    return max(-1.0, min(1.0, score))


def _score_bird(sub_prefs, item):
    # Birds are observed, not held — gift: a "bird sketch" or similar token isn't in game yet.
    # Accept any object with a SPECIES attribute (future-proof).
    species_cls = type(item)
    if not hasattr(species_cls, "SPECIES"):
        return 0.0
    wanted_rarity = sub_prefs.get("rarity")
    item_rarity = getattr(species_cls, "RARITY", "common")
    if wanted_rarity and item_rarity == wanted_rarity:
        return 0.7
    return 0.0


def _score_wine(sub_prefs, item):
    from wine import Grape
    if not isinstance(item, Grape):
        return 0.0
    score = 0.0
    wanted_style = sub_prefs.get("style")
    if wanted_style and getattr(item, "style", None) == wanted_style:
        score += 0.5
    complexity = getattr(item, "complexity", 0.5)
    score += (complexity - 0.5) * 0.8
    return max(-1.0, min(1.0, score))


def _score_coffee(sub_prefs, item):
    from coffee import CoffeeBean
    if not isinstance(item, CoffeeBean):
        return 0.0
    score = 0.0
    wanted_roast = sub_prefs.get("roast_level")
    if wanted_roast and getattr(item, "roast_level", None) == wanted_roast:
        score += 0.5
    quality = getattr(item, "roast_quality", 0.5)
    score += (quality - 0.5) * 0.8
    return max(-1.0, min(1.0, score))


def _score_tea(sub_prefs, item):
    from tea import TeaLeaf
    if not isinstance(item, TeaLeaf):
        return 0.0
    score = 0.0
    wanted_type = sub_prefs.get("tea_type")
    if wanted_type and getattr(item, "tea_type", None) == wanted_type:
        score += 0.5
    quality = getattr(item, "complexity", 0.5)
    score += (quality - 0.5) * 0.8
    return max(-1.0, min(1.0, score))


def _score_spirit(sub_prefs, item):
    from spirits import Spirit
    if not isinstance(item, Spirit):
        return 0.0
    score = 0.0
    wanted_type = sub_prefs.get("spirit_type")
    if wanted_type and getattr(item, "spirit_type", None) == wanted_type:
        score += 0.5
    age_quality = getattr(item, "age_quality", 0.5)
    score += (age_quality - 0.5) * 0.8
    return max(-1.0, min(1.0, score))


def _score_cheese(sub_prefs, item):
    from cheese import Cheese
    if not isinstance(item, Cheese):
        return 0.0
    score = 0.0
    wanted_type = sub_prefs.get("cheese_type")
    if wanted_type and getattr(item, "cheese_type", None) == wanted_type:
        score += 0.5
    age_quality = getattr(item, "age_quality", 0.5)
    score += (age_quality - 0.5) * 0.6
    return max(-1.0, min(1.0, score))


def _score_pottery(sub_prefs, item):
    from pottery import PotteryPiece
    if not isinstance(item, PotteryPiece):
        return 0.0
    score = 0.0
    wanted_shape = sub_prefs.get("shape")
    if wanted_shape and getattr(item, "shape", None) == wanted_shape:
        score += 0.4
    firing = getattr(item, "firing_level", "intact")
    tier = {"cracked": -0.3, "intact": 0.1, "fine": 0.5, "masterwork": 0.9}
    score += tier.get(firing, 0.0)
    return max(-1.0, min(1.0, score))


def _score_salt(sub_prefs, item):
    from salt import SaltCrystal
    if not isinstance(item, SaltCrystal):
        return 0.0
    score = 0.0
    wanted_grade = sub_prefs.get("refine_grade")
    if wanted_grade and getattr(item, "refine_grade", None) == wanted_grade:
        score += 0.6
    purity = getattr(item, "purity", 0.5)
    score += (purity - 0.5) * 0.6
    return max(-1.0, min(1.0, score))


def _score_weapon(sub_prefs, item):
    from weapons import Weapon
    if not isinstance(item, Weapon):
        return 0.0
    score = 0.0
    wanted_type = sub_prefs.get("weapon_type")
    if wanted_type and getattr(item, "weapon_type", None) == wanted_type:
        score += 0.4
    quality = getattr(item, "quality", 0.5)
    score += (quality - 0.5) * 1.0
    return max(-1.0, min(1.0, score))


def _score_textile(sub_prefs, item):
    from textiles import Textile
    if not isinstance(item, Textile):
        return 0.0
    score = 0.0
    wanted_dye = sub_prefs.get("dye_family")
    if wanted_dye and getattr(item, "dye_family", None) == wanted_dye:
        score += 0.5
    quality = getattr(item, "quality", 0.5)
    score += (quality - 0.5) * 0.6
    return max(-1.0, min(1.0, score))


def _score_jewelry(sub_prefs, item):
    from jewelry import Jewelry
    if not isinstance(item, Jewelry):
        return 0.0
    wanted_type = sub_prefs.get("jewelry_type")
    if wanted_type and getattr(item, "jewelry_type", None) == wanted_type:
        return 0.8
    return 0.2


def _score_food(sub_prefs, item):
    # Items are plain dicts from ITEMS; the item arg here is (item_id, count)
    if not isinstance(item, tuple) or len(item) != 2:
        return 0.0
    item_id, _ = item
    from items import ITEMS
    if item_id not in ITEMS:
        return 0.0
    data = ITEMS[item_id]
    if not data.get("edible"):
        return 0.0
    restore = data.get("hunger_restore", 0)
    wanted_cat = sub_prefs.get("category")
    # Simple category heuristic: high-restore foods score better if NPC likes "hearty"
    if wanted_cat == "hearty":
        return min(1.0, restore / 15.0) * 0.8
    if wanted_cat == "light":
        return max(0.0, 1.0 - restore / 15.0) * 0.6
    return 0.2


# Register all built-in systems
register_system("fish", "Fish", {
    "rarity":  ["common", "uncommon", "rare", "epic", "legendary"],
    "habitat": ["river", "lake", "ocean", "cave"],
}, _score_fish)

register_system("fossil", "Fossils", {
    "rarity": ["common", "uncommon", "rare", "epic", "legendary"],
    "age":    ["paleozoic", "mesozoic", "cenozoic"],
}, _score_fossil)

register_system("rock", "Rocks", {
    "rarity": ["common", "uncommon", "rare", "epic", "legendary"],
}, _score_rock)

register_system("gem", "Gemstones", {
    "rarity": ["common", "uncommon", "rare", "epic", "legendary"],
    "cut":    ["tumbled", "cabochon", "brilliant", "step", "cushion", "pear"],
}, _score_gem)

register_system("wildflower", "Wildflowers", {
    "rarity": ["common", "uncommon", "rare"],
}, _score_wildflower)

register_system("wine", "Wine", {
    "style": ["red", "white", "rose", "sparkling", "dessert"],
}, _score_wine)

register_system("coffee", "Coffee", {
    "roast_level": ["light", "medium", "dark"],
}, _score_coffee)

register_system("tea", "Tea", {
    "tea_type": ["green", "oolong", "black", "puerh"],
}, _score_tea)

register_system("spirit", "Spirits", {
    "spirit_type": ["whiskey", "bourbon", "rum", "gin", "brandy", "vodka"],
}, _score_spirit)

register_system("cheese", "Cheese", {
    "cheese_type": ["fresh", "aged_hard", "blue", "soft_ripened", "smoked"],
}, _score_cheese)

register_system("pottery", "Pottery", {
    "shape": ["pot", "amphora", "jar", "jug", "vase"],
}, _score_pottery)

register_system("salt", "Salt", {
    "refine_grade": ["coarse", "fine", "fleur_de_sel"],
}, _score_salt)

register_system("weapon", "Weapons", {
    "weapon_type": ["dagger", "sword", "spear", "axe", "mace"],
}, _score_weapon)

register_system("textile", "Textiles", {
    "dye_family": ["natural", "golden", "crimson", "rose", "cobalt", "violet",
                   "verdant", "amber", "ivory"],
}, _score_textile)

register_system("jewelry", "Jewelry", {
    "jewelry_type": ["ring", "necklace", "bracelet", "pendant", "crown"],
}, _score_jewelry)

register_system("food", "Food", {
    "category": ["hearty", "light"],
}, _score_food)


# ---------------------------------------------------------------------------
# Preference derivation
# ---------------------------------------------------------------------------

def derive_preferences(npc_uid: str, world_seed: int) -> dict:
    """Derive stable, seeded preferences for one NPC.

    Returns:
        {
          "liked_systems":    [system_id, ...],          # 2–4
          "disliked_systems": [system_id, ...],          # 1–2
          "weights":          {system_id: float},        # 0.5–2.0
          "sub_prefs":        {system_id: {param: val}},
        }
    """
    rng = random.Random(hash((npc_uid, world_seed, "prefs")) & 0xFFFFFFFF)

    all_systems = list(PREFERENCE_SYSTEMS.keys())
    rng.shuffle(all_systems)

    num_liked    = rng.randint(2, 4)
    num_disliked = rng.randint(1, 2)

    liked    = all_systems[:num_liked]
    disliked = all_systems[num_liked: num_liked + num_disliked]

    weights = {}
    for sid in liked:
        weights[sid] = round(rng.uniform(1.0, 2.0), 2)
    for sid in disliked:
        weights[sid] = round(rng.uniform(-1.5, -0.5), 2)

    sub_prefs = {}
    for sid in liked:
        params = PREFERENCE_SYSTEMS[sid]["params"]
        sub_prefs[sid] = {
            param: rng.choice(values)
            for param, values in params.items()
        }

    return {
        "liked_systems":    liked,
        "disliked_systems": disliked,
        "weights":          weights,
        "sub_prefs":        sub_prefs,
    }


# ---------------------------------------------------------------------------
# Gift scoring
# ---------------------------------------------------------------------------

def score_gift(npc_prefs: dict, item) -> float:
    """Score how much an NPC would value a gift item.

    Returns a float roughly in [-1.0, +1.0].
    Positive = they'd like it; negative = they'd dislike it.
    """
    weights  = npc_prefs.get("weights", {})
    sub_prefs = npc_prefs.get("sub_prefs", {})

    best = 0.0
    matched = False
    for sid, sys_info in PREFERENCE_SYSTEMS.items():
        try:
            raw = sys_info["scorer"](sub_prefs.get(sid, {}), item)
        except Exception:
            continue
        if raw == 0.0:
            continue
        matched = True
        weight = weights.get(sid, 0.0)
        best = max(best, raw * weight) if weight > 0 else min(best, raw * abs(weight))

    if not matched:
        return 0.0
    return max(-1.0, min(1.0, best))


def gift_tier_label(score: float) -> tuple[str, tuple]:
    """Return (label, colour) for a gift score."""
    if score >= 0.6:
        return "Would love this!", (255, 215, 80)
    if score >= 0.2:
        return "Would like this", (140, 210, 120)
    if score >= -0.2:
        return "Neutral", (160, 160, 160)
    return "Wouldn't like this", (200, 90, 80)


# ---------------------------------------------------------------------------
# Relationship tiers
# ---------------------------------------------------------------------------

_TIERS = [
    (-100, "Hostile",     (200,  80,  60)),
    (  -1, "Cold",        (170, 120,  90)),
    (   0, "Neutral",     (160, 160, 160)),
    (  20, "Acquainted",  (120, 190, 140)),
    (  50, "Friendly",    (100, 200, 100)),
    (  80, "Beloved",     (255, 215,  80)),
]


def relationship_tier(score: int) -> tuple[str, tuple]:
    """Return (tier_name, colour) for a relationship score."""
    name, col = "Neutral", (160, 160, 160)
    for threshold, tier_name, colour in _TIERS:
        if score >= threshold:
            name, col = tier_name, colour
    return name, col


# ---------------------------------------------------------------------------
# Relationship milestone handling
# ---------------------------------------------------------------------------

_MILESTONE_REP = {20: 5, 50: 10, 80: 20}
_MILESTONES = sorted(_MILESTONE_REP.keys())


def apply_gift(player, npc, item, world) -> tuple[int, str]:
    """Apply a gift from player to npc.

    Returns (delta, tier_label) where delta is the relationship point change.
    Handles: milestone town-rep bonuses, family ripple.
    """
    from towns import TOWNS

    score = score_gift(npc.preferences, item)
    label, _ = gift_tier_label(score)

    # Scale score to relationship points: range -15 to +15
    delta = int(round(score * 15))
    if delta == 0 and score > 0:
        delta = 1

    npc_uid = npc.npc_uid
    old_score = player.npc_relationships.get(npc_uid, 0)
    new_score = max(-100, min(100, old_score + delta))
    player.npc_relationships[npc_uid] = new_score

    # Milestone bonus → town rep + beloved perk at 80
    tid = getattr(npc, "town_id", None) or npc._nearest_town_id()
    if tid is not None and tid in TOWNS:
        for m in _MILESTONES:
            if old_score < m <= new_score:
                TOWNS[tid].reputation += _MILESTONE_REP[m]
                if m == 80 and npc_uid not in getattr(player, "beloved_perks", set()):
                    if not hasattr(player, "beloved_perks"):
                        player.beloved_perks = set()
                    grant_beloved_perk(player, npc, world)
                    player.beloved_perks.add(npc_uid)

    # Family ripple: each linked NPC gains 10% of delta (at least 1 if positive)
    if delta != 0:
        family_uids = (
            npc.sibling_uids + npc.parent_uids
            + ([npc.spouse_uid] if npc.spouse_uid else [])
        )
        ripple = max(1, abs(delta) // 10) * (1 if delta > 0 else -1)
        for uid in family_uids:
            cur = player.npc_relationships.get(uid, 0)
            player.npc_relationships[uid] = max(-100, min(100, cur + ripple))

    # Dynasty favor milestone check
    import npc_dynasty as _dyn
    _dyn.check_dynasty_milestones(player, npc, world)

    return delta, label


# ---------------------------------------------------------------------------
# NPC Requests
# ---------------------------------------------------------------------------

_REQUEST_HINTS = {
    "fish":       ["a fine catch from the waters", "something reeled from the deep"],
    "fossil":     ["a relic from deep below", "something ancient and preserved"],
    "rock":       ["a handsome specimen of stone", "something with unusual markings"],
    "gem":        ["a precious thing that catches the light", "a rare gem for my collection"],
    "wildflower": ["a delicate flower from the wild", "something that blooms in open fields"],
    "wine":       ["a fine wine to share at my table", "something aged and fermented well"],
    "coffee":     ["a richly roasted brew", "dark beans, freshly roasted"],
    "tea":        ["a calming tea for the evenings", "something leafy and aromatic"],
    "spirit":     ["a well-aged spirit", "something strong and smooth"],
    "cheese":     ["a good aged cheese", "something pressed and matured"],
    "pottery":    ["a fine piece of pottery", "a well-fired vessel for the home"],
    "salt":       ["refined salt for the table", "pure crystallized salt"],
    "weapon":     ["a well-crafted weapon", "something sharp and well-balanced"],
    "textile":    ["a finely woven cloth", "colourful woven goods"],
    "jewelry":    ["a piece of fine jewelry", "something crafted and elegant"],
    "food":       ["something hearty to eat", "a filling and well-made meal"],
}


def maybe_generate_request(player, npc, world_day: int) -> None:
    """Generate an NPC request if conditions are met (call when inspect panel opens)."""
    uid = getattr(npc, "npc_uid", None)
    if uid is None:
        return
    if uid in getattr(player, "npc_requests", {}):
        return
    if player.npc_relationships.get(uid, 0) < 20:
        return
    if world_day < getattr(player, "npc_request_cooldowns", {}).get(uid, 0):
        return
    prefs = getattr(npc, "preferences", None) or {}
    liked = prefs.get("liked_systems", [])
    if not liked:
        return
    rng = random.Random(hash((uid, world_day, "req")) & 0xFFFFFFFF)
    system_id = rng.choice(liked)
    hint = rng.choice(_REQUEST_HINTS.get(system_id, ["something special"]))
    rel_score = player.npc_relationships.get(uid, 0)
    reward = 60 + int(rel_score * 1.5)
    if not hasattr(player, "npc_requests"):
        player.npc_requests = {}
    player.npc_requests[uid] = {
        "system_id": system_id,
        "hint_label": hint,
        "reward_gold": reward,
        "posted_day":  world_day,
    }


def fulfill_request(player, npc, item, world) -> tuple[int, int]:
    """Fulfill an NPC's active request.  Returns (relationship_delta, gold_awarded)."""
    uid = getattr(npc, "npc_uid", None)
    if uid is None:
        return 0, 0
    requests = getattr(player, "npc_requests", {})
    request = requests.pop(uid, None)
    if request is None:
        return 0, 0

    world_day = getattr(world, "day_count", 0)
    if not hasattr(player, "npc_request_cooldowns"):
        player.npc_request_cooldowns = {}
    player.npc_request_cooldowns[uid] = world_day + 5

    gold = request.get("reward_gold", 60)
    # Known-tier dynasty bonus: +50 gold for requests from a house that knows you
    import npc_dynasty as _dyn
    region_id = getattr(npc, "dynasty_id", None)
    if region_id is not None:
        favor = _dyn.calculate_dynasty_favor(player, region_id, world)
        if _dyn.favor_tier(favor)["name"] in ("Known", "Favored", "Champion"):
            gold += 50
    player.money += gold

    old_score = player.npc_relationships.get(uid, 0)
    delta = random.randint(20, 30)
    new_score = min(100, old_score + delta)
    player.npc_relationships[uid] = new_score

    from towns import TOWNS
    tid = getattr(npc, "town_id", None)
    if tid is None:
        try:
            tid = npc._nearest_town_id()
        except Exception:
            tid = None
    if tid is not None and tid in TOWNS:
        for m in _MILESTONES:
            if old_score < m <= new_score:
                TOWNS[tid].reputation += _MILESTONE_REP[m]

    if new_score >= 80 and uid not in getattr(player, "beloved_perks", set()):
        if not hasattr(player, "beloved_perks"):
            player.beloved_perks = set()
        grant_beloved_perk(player, npc, world)
        player.beloved_perks.add(uid)

    _dyn.check_dynasty_milestones(player, npc, world)

    return delta, gold


# ---------------------------------------------------------------------------
# Beloved perks
# ---------------------------------------------------------------------------

_ROLE_PERKS = {
    "npc_blacksmith": "merchant_discount",
    "npc_merchant":   "merchant_discount",
    "npc_trade":      "merchant_discount",
    "npc_monk":       "merchant_discount",
    "npc_chef":       "merchant_discount",
    "npc_scholar":    "merchant_discount",
    "npc_innkeeper":  "inn_beloved",
    "npc_doctor":     "free_doctor",
    "npc_farmer":     "farm_seeds",
    "npc_elder":      "town_rep_bonus",
    "npc_noble":      "town_rep_bonus",
}

_PERK_DESCRIPTIONS = {
    "merchant_discount": "10% discount at shops in this town",
    "inn_beloved":       "Innkeeper rest now restores full HP",
    "free_doctor":       "Free healing from the doctor in this town",
    "farm_seeds":        "Farmer will occasionally send you seeds",
    "town_rep_bonus":    "+25 reputation with this town",
}


def grant_beloved_perk(player, npc, world) -> None:
    """Apply the one-time Beloved perk for this NPC's role."""
    animal_id = getattr(npc, "animal_id", "")
    perk = _ROLE_PERKS.get(animal_id)
    tid = getattr(npc, "town_id", None)
    if tid is None:
        try:
            tid = npc._nearest_town_id()
        except Exception:
            tid = None

    if perk == "merchant_discount":
        if not hasattr(player, "merchant_beloved_towns"):
            player.merchant_beloved_towns = set()
        if tid is not None:
            player.merchant_beloved_towns.add(tid)
    elif perk == "inn_beloved":
        player.inn_beloved = True
    elif perk == "free_doctor":
        if not hasattr(player, "doctor_beloved_towns"):
            player.doctor_beloved_towns = set()
        if tid is not None:
            player.doctor_beloved_towns.add(tid)
    elif perk == "farm_seeds":
        if not hasattr(player, "farm_seed_donors"):
            player.farm_seed_donors = set()
        uid = getattr(npc, "npc_uid", None)
        if uid:
            player.farm_seed_donors.add(uid)
    elif perk == "town_rep_bonus":
        from towns import TOWNS
        if tid is not None and tid in TOWNS:
            TOWNS[tid].reputation += 25
    else:
        from towns import TOWNS
        if tid is not None and tid in TOWNS:
            TOWNS[tid].reputation += 10

    desc = _PERK_DESCRIPTIONS.get(perk, "Perk unlocked")
    player.pending_notifications.append(("Beloved", f"Beloved! {desc}", "epic"))


def preferred_system_labels(npc_prefs: dict, count: int = 3) -> list[str]:
    """Return display names of the NPC's top liked systems (up to count)."""
    liked = npc_prefs.get("liked_systems", [])[:count]
    return [PREFERENCE_SYSTEMS[sid]["display_name"] for sid in liked
            if sid in PREFERENCE_SYSTEMS]


def disliked_system_labels(npc_prefs: dict) -> list[str]:
    disliked = npc_prefs.get("disliked_systems", [])
    return [PREFERENCE_SYSTEMS[sid]["display_name"] for sid in disliked
            if sid in PREFERENCE_SYSTEMS]
