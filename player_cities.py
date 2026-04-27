"""
player_cities.py — Data model and daily tick for player-established cities.

Each city is anchored by a CITY_BLOCK placed in the world.
The registry is keyed by (bx, by) of that block.
"""

import random
import math
from dataclasses import dataclass, field

from blocks import BED, CHEST_BLOCK, TILLED_SOIL, BEDROCK, MINING_POST_BLOCK, ALL_LOGS
from constants import BLOCK_SIZE as _BLOCK_SIZE

# City region half-width in blocks (±80 tiles)
CITY_REGION_HALF = 80
# Vertical scan range around the city block for beds/chests
_SCAN_V_HALF = 50

# Days without food/pay before becoming disgruntled / leaving
_DISGRUNTLED_THRESHOLD = 2
_LEAVE_THRESHOLD       = 3


# ── Data ─────────────────────────────────────────────────────────────────────

@dataclass
class PlayerCity:
    bx: int
    by: int
    name: str = "Unnamed City"
    coat_of_arms: dict = field(default_factory=lambda: {
        "primary":   [60, 100, 180],
        "secondary": [200, 168,  72],
        "metal":     [200, 168,  72],
        "division":  "plain",
        "ordinary":  "none",
        "charge":    "none",
        "motto":     "Stand Firm",
    })
    treasury: int = 0
    npcs: list = field(default_factory=list)   # list of settler record dicts

    @property
    def population(self):
        return len(self.npcs)

    @property
    def hired_count(self):
        return sum(1 for r in self.npcs if r.get("hired"))

    def count_beds(self, world) -> int:
        total = 0
        y0 = max(0, self.by - _SCAN_V_HALF)
        y1 = min(world.height - 1, self.by + _SCAN_V_HALF)
        for bx in range(self.bx - CITY_REGION_HALF, self.bx + CITY_REGION_HALF + 1):
            for by in range(y0, y1 + 1):
                if world.get_block(bx, by) == BED:
                    total += 1
        return total

    def count_food_chests(self, world) -> int:
        from items import ITEMS
        total = 0
        y0 = max(0, self.by - _SCAN_V_HALF)
        y1 = min(world.height - 1, self.by + _SCAN_V_HALF)
        for bx in range(self.bx - CITY_REGION_HALF, self.bx + CITY_REGION_HALF + 1):
            for by in range(y0, y1 + 1):
                if world.get_block(bx, by) == CHEST_BLOCK:
                    inv = world.chest_data.get((bx, by), {})
                    if any(ITEMS.get(iid, {}).get("edible") and qty > 0
                           for iid, qty in inv.items()):
                        total += 1
        return total

    def count_unemployed(self) -> int:
        return sum(1 for npc in self.npcs if not npc.get("hired"))

    def to_dict(self):
        return {
            "bx":           self.bx,
            "by":           self.by,
            "name":         self.name,
            "coat_of_arms": self.coat_of_arms,
            "treasury":     self.treasury,
            "npcs":         self.npcs,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            bx=d["bx"],
            by=d["by"],
            name=d.get("name", "Unnamed City"),
            coat_of_arms=d.get("coat_of_arms", {}),
            treasury=d.get("treasury", 0),
            npcs=d.get("npcs", []),
        )

    def to_coa(self):
        """Convert coat_of_arms dict to a heraldry.CoatOfArms for rendering."""
        import heraldry
        coa = self.coat_of_arms
        return heraldry.CoatOfArms(
            primary   = tuple(coa.get("primary",   [60, 100, 180])),
            secondary = tuple(coa.get("secondary", [200, 168,  72])),
            metal     = tuple(coa.get("metal",     [200, 168,  72])),
            division  = coa.get("division", "plain"),
            ordinary  = coa.get("ordinary", "none"),
            charge    = coa.get("charge",   "none"),
            motto     = coa.get("motto",    "Stand Firm"),
        )


def coa_from_dict(coa: dict):
    """Convert a stored coat_of_arms dict to a heraldry.CoatOfArms."""
    import heraldry
    return heraldry.CoatOfArms(
        primary   = tuple(coa.get("primary",   [60, 100, 180])),
        secondary = tuple(coa.get("secondary", [200, 168,  72])),
        metal     = tuple(coa.get("metal",     [200, 168,  72])),
        division  = coa.get("division", "plain"),
        ordinary  = coa.get("ordinary", "none"),
        charge    = coa.get("charge",   "none"),
        motto     = coa.get("motto",    "Stand Firm"),
    )


# ── Registry ──────────────────────────────────────────────────────────────────

PLAYER_CITIES: dict[tuple[int, int], PlayerCity] = {}


def register_city(bx: int, by: int) -> "PlayerCity":
    city = PlayerCity(bx=bx, by=by)
    PLAYER_CITIES[(bx, by)] = city
    return city


def remove_city(bx: int, by: int) -> None:
    PLAYER_CITIES.pop((bx, by), None)


def get_city_at(bx: int, by: int) -> "PlayerCity | None":
    return PLAYER_CITIES.get((bx, by))


def get_city_for_block(world, bx: int, by: int) -> "PlayerCity | None":
    return PLAYER_CITIES.get((bx, by))


# ── Food helpers ──────────────────────────────────────────────────────────────

def _build_food_priority_list(city: "PlayerCity", world) -> list[tuple[int, str, tuple]]:
    """
    Scan all chests in the city region and return a list of
    (hunger_restore, item_id, chest_pos) sorted highest-first.
    Cooked meals (>= 30) naturally sort before raw food, then crops.
    """
    from items import ITEMS
    options = []
    y0 = max(0, city.by - _SCAN_V_HALF)
    y1 = min(world.height - 1, city.by + _SCAN_V_HALF)
    for bx in range(city.bx - CITY_REGION_HALF, city.bx + CITY_REGION_HALF + 1):
        for by in range(y0, y1 + 1):
            if world.get_block(bx, by) != CHEST_BLOCK:
                continue
            pos = (bx, by)
            inv = world.chest_data.get(pos, {})
            for iid, qty in inv.items():
                if qty <= 0:
                    continue
                data = ITEMS.get(iid, {})
                if data.get("edible"):
                    options.append((data.get("hunger_restore", 1), iid, pos))
    options.sort(key=lambda t: t[0], reverse=True)
    return options


def _consume_one_food(options: list, world) -> bool:
    """
    Consume one food item from the highest-priority entry in options.
    Modifies world.chest_data in place. Returns True if food was consumed.
    """
    for restore, iid, pos in options:
        inv = world.chest_data.get(pos, {})
        if inv.get(iid, 0) > 0:
            inv[iid] -= 1
            if inv[iid] == 0:
                del inv[iid]
            return True
    return False


# ── Dawn tick ─────────────────────────────────────────────────────────────────

def tick_city_day(world) -> None:
    """Called once per in-game dawn."""
    for city in PLAYER_CITIES.values():
        _process_upkeep(city, world)
        _process_declines(city, world)
        _process_jobs(city, world)
        _run_attraction(city, world)


def _process_upkeep(city: "PlayerCity", world) -> None:
    """Feed hired settlers from region chests and pay wages from treasury."""
    if not any(r.get("hired") for r in city.npcs):
        return

    food_options = _build_food_priority_list(city, world)
    to_remove: set[str] = set()

    for rec in city.npcs:
        if not rec.get("hired"):
            continue

        # ── Food ─────────────────────────────────────────────────────────────
        fed = _consume_one_food(food_options, world)
        if fed:
            rec["days_unfed"] = 0
        else:
            rec["days_unfed"] = rec.get("days_unfed", 0) + 1

        # ── Wages ─────────────────────────────────────────────────────────────
        wage = rec.get("wage", 0)
        if city.treasury >= wage:
            city.treasury -= wage
            rec["days_unpaid"] = 0
        else:
            rec["days_unpaid"] = rec.get("days_unpaid", 0) + 1

        # ── Disgruntled / leave ───────────────────────────────────────────────
        days_unfed   = rec.get("days_unfed", 0)
        days_unpaid  = rec.get("days_unpaid", 0)
        was_disgruntled = rec.get("disgruntled", False)

        if days_unfed >= _LEAVE_THRESHOLD or days_unpaid >= _LEAVE_THRESHOLD:
            to_remove.add(rec["id"])
        elif days_unfed >= _DISGRUNTLED_THRESHOLD or days_unpaid >= _DISGRUNTLED_THRESHOLD:
            rec["disgruntled"] = True
            if not was_disgruntled:
                _city_notify(world, city,
                             f"{rec['name']} in {city.name} is disgruntled!")
        else:
            rec["disgruntled"] = False

        # Keep live entity in sync
        from settler_npcs import sync_settler_entity
        sync_settler_entity(world, rec)

    if to_remove:
        _remove_settlers(city, world, to_remove)
        for sid in to_remove:
            rec = next((r for r in city.npcs if r["id"] == sid), None)
            name = rec["name"] if rec else "A settler"
            _city_notify(world, city, f"{name} has left {city.name}.")


def _process_declines(city: "PlayerCity", world) -> None:
    """Countdown declined settlers; remove those whose time is up."""
    to_remove: set[str] = set()
    for rec in city.npcs:
        if "decline_days_remaining" not in rec:
            continue
        rec["decline_days_remaining"] -= 1
        if rec["decline_days_remaining"] <= 0:
            to_remove.add(rec["id"])
    if to_remove:
        _remove_settlers(city, world, to_remove)


def _run_attraction(city: "PlayerCity", world) -> None:
    """Roll attraction for one city and spawn settlers into world.entities."""
    beds        = city.count_beds(world)
    food_chests = city.count_food_chests(world)
    unemployed  = city.count_unemployed()

    if beds == 0:
        return

    for _ in range(beds):
        chance = 0.15
        chance += 0.05 * food_chests
        chance -= 0.05 * unemployed
        chance = max(0.0, min(0.95, chance))

        if random.random() >= chance:
            continue

        from settler_npcs import generate_settler_record, spawn_settler_entity
        day    = getattr(world, "day_count", 0)
        index  = len(city.npcs)
        record = generate_settler_record(city.bx, city.by, world.seed, day, index)
        city.npcs.append(record)
        spawn_settler_entity(world, city, record)
        _city_notify(world, city,
                     f"A traveler has arrived in {city.name} and is seeking work.")
        unemployed += 1


# ── Job helpers ───────────────────────────────────────────────────────────────

def _deposit_to_nearest_chest(city: "PlayerCity", world, item_id: str, qty: int = 1) -> bool:
    """Add qty of item_id to the first chest found in the city region. Returns True if found."""
    y0 = max(0, city.by - _SCAN_V_HALF)
    y1 = min(world.height - 1, city.by + _SCAN_V_HALF)
    for bx in range(city.bx - CITY_REGION_HALF, city.bx + CITY_REGION_HALF + 1):
        for by in range(y0, y1 + 1):
            if world.get_block(bx, by) == CHEST_BLOCK:
                inv = world.chest_data.setdefault((bx, by), {})
                inv[item_id] = inv.get(item_id, 0) + qty
                return True
    return False


def _deposit_to_chest(world, bx: int, by: int, item_id: str, qty: int = 1) -> None:
    inv = world.chest_data.setdefault((bx, by), {})
    inv[item_id] = inv.get(item_id, 0) + qty


_MATURE_CROP_IDS: set = set()

def _ensure_mature_crop_ids():
    if _MATURE_CROP_IDS:
        return
    import blocks as _blk
    for attr in dir(_blk):
        if attr.endswith("_CROP_MATURE") or attr.endswith("_MATURE"):
            val = getattr(_blk, attr)
            if isinstance(val, int):
                _MATURE_CROP_IDS.add(val)


def _job_farming(city: "PlayerCity", world, rec: dict, eff: float) -> None:
    _ensure_mature_crop_ids()
    from blocks import BLOCKS
    harvests = max(1, int(math.ceil((1 + rec["stats"].get("agility", 5) / 4) * eff)))
    count = 0
    y0 = max(0, city.by - _SCAN_V_HALF)
    y1 = min(world.height - 1, city.by + _SCAN_V_HALF)
    for bx in range(city.bx - CITY_REGION_HALF, city.bx + CITY_REGION_HALF + 1):
        if count >= harvests:
            break
        for by in range(y0, y1 + 1):
            if count >= harvests:
                break
            bid = world.get_block(bx, by)
            if bid not in _MATURE_CROP_IDS:
                continue
            data = BLOCKS.get(bid, {})
            drop = data.get("drop")
            world.set_block(bx, by, TILLED_SOIL)
            if drop:
                _deposit_to_nearest_chest(city, world, drop)
            count += 1


# Ore drop items (used for mining target filter "ores")
_ORE_DROPS = {"coal", "iron_chunk", "gold_nugget", "crystal_shard", "ruby",
              "obsidian_slab", "silver_chunk", "tin_chunk", "copper_chunk",
              "mithril_chunk", "adamant_chunk"}


def _job_mining(city: "PlayerCity", world, rec: dict, eff: float) -> None:
    from blocks import BLOCKS
    cfg = rec.get("job_config") or {}
    radius = cfg.get("radius", 3)
    target = cfg.get("target", "all")
    depth_limit = cfg.get("depth_limit", 20)

    # Find the assigned or nearest Mining Post in the city region
    post_bx = cfg.get("post_bx")
    post_by = cfg.get("post_by")
    if post_bx is None or post_by is None:
        # Auto-detect nearest post
        best_dist = float("inf")
        y0 = max(0, city.by - _SCAN_V_HALF)
        y1 = min(world.height - 1, city.by + _SCAN_V_HALF)
        for bx in range(city.bx - CITY_REGION_HALF, city.bx + CITY_REGION_HALF + 1):
            for by in range(y0, y1 + 1):
                if world.get_block(bx, by) == MINING_POST_BLOCK:
                    d = abs(bx - city.bx) + abs(by - city.by)
                    if d < best_dist:
                        best_dist = d
                        post_bx, post_by = bx, by
    if post_bx is None:
        return  # no mining post found

    mines = max(1, int(math.ceil((1 + rec["stats"].get("strength", 5) / 4) * eff)))
    count = 0
    for dbx in range(-radius, radius + 1):
        if count >= mines:
            break
        for dby in range(1, depth_limit + 1):
            if count >= mines:
                break
            bx = post_bx + dbx
            by = post_by + dby
            bid = world.get_block(bx, by)
            if bid == 0:
                continue
            data = BLOCKS.get(bid, {})
            hardness = data.get("hardness", 0)
            if hardness <= 0 or hardness == float("inf"):
                continue
            drop = data.get("drop")
            if not drop:
                continue
            if target == "ores" and drop not in _ORE_DROPS:
                continue
            if target == "stone" and drop in _ORE_DROPS:
                continue
            world.set_block(bx, by, 0)
            _deposit_to_nearest_chest(city, world, drop)
            count += 1


def _job_hauling(city: "PlayerCity", world, rec: dict, eff: float) -> None:
    cfg = rec.get("job_config") or {}
    src_bx = cfg.get("src_bx")
    src_by = cfg.get("src_by")
    dst_bx = cfg.get("dst_bx")
    dst_by = cfg.get("dst_by")
    if None in (src_bx, src_by, dst_bx, dst_by):
        return
    if world.get_block(src_bx, src_by) != CHEST_BLOCK:
        return
    if world.get_block(dst_bx, dst_by) != CHEST_BLOCK:
        return

    src_inv = world.chest_data.get((src_bx, src_by), {})
    if not src_inv:
        return

    batch = max(1, int(math.ceil((5 + rec["stats"].get("agility", 5) + rec["stats"].get("strength", 5)) * eff)))
    item_filter = cfg.get("filter")
    dst_inv = world.chest_data.setdefault((dst_bx, dst_by), {})

    moved = 0
    for item_id in list(src_inv.keys()):
        if moved >= batch:
            break
        if item_filter and item_id != item_filter:
            continue
        qty = src_inv.get(item_id, 0)
        if qty <= 0:
            continue
        take = min(qty, batch - moved)
        src_inv[item_id] -= take
        if src_inv[item_id] <= 0:
            del src_inv[item_id]
        dst_inv[item_id] = dst_inv.get(item_id, 0) + take
        moved += take


def _job_taming(city: "PlayerCity", world, rec: dict, eff: float) -> None:
    from animals import Goat, Sheep, Cow, Chicken
    cfg = rec.get("job_config") or {}
    affinity = rec["stats"].get("animal_affinity", 5)
    max_animals = 5 + affinity
    day = getattr(world, "day_count", 0)

    tended = 0
    region_x0 = (city.bx - CITY_REGION_HALF) * _BLOCK_SIZE
    region_x1 = (city.bx + CITY_REGION_HALF) * _BLOCK_SIZE

    for entity in world.entities:
        if tended >= max_animals:
            break
        if not hasattr(entity, "x"):
            continue
        if not (region_x0 <= entity.x <= region_x1):
            continue

        if isinstance(entity, (Goat, Cow, Sheep)):
            # Produce milk every other day; affinity improves yield
            if day % 2 == 0:
                milk_id = "goat_milk" if isinstance(entity, Goat) else (
                    "sheep_milk" if isinstance(entity, Sheep) else "milk")
                yield_qty = max(1, int((1 + affinity / 10) * eff))
                _deposit_to_nearest_chest(city, world, milk_id, yield_qty)
                tended += 1
        elif isinstance(entity, Chicken):
            # Produce egg every day
            egg_qty = max(1, int(eff))
            _deposit_to_nearest_chest(city, world, "egg", egg_qty)
            tended += 1


def _job_logging(city: "PlayerCity", world, rec: dict, eff: float) -> None:
    chops = max(1, int(math.ceil((1 + rec["stats"].get("strength", 5) / 4) * eff)))
    count = 0
    y0 = max(0, city.by - _SCAN_V_HALF)
    y1 = min(world.height - 1, city.by + _SCAN_V_HALF)
    for bx in range(city.bx - CITY_REGION_HALF, city.bx + CITY_REGION_HALF + 1):
        if count >= chops:
            break
        for by in range(y0, y1 + 1):
            if count >= chops:
                break
            if world.get_block(bx, by) in ALL_LOGS:
                world.set_block(bx, by, 0)
                _deposit_to_nearest_chest(city, world, "lumber")
                count += 1


_RAW_TO_COOKED = {
    "raw_mutton":    "cooked_mutton",
    "raw_beef":      "cooked_beef",
    "raw_chicken":   "cooked_chicken",
    "raw_venison":   "cooked_venison",
    "raw_boar_meat": "cooked_boar",
    "raw_rabbit":    "cooked_rabbit",
    "raw_turkey":    "cooked_turkey",
    "raw_bear_meat": "cooked_bear",
    "raw_duck":      "cooked_duck",
    "raw_bison_meat":"cooked_bison",
    "raw_pheasant":  "cooked_pheasant",
    "raw_goose":     "cooked_goose",
    "raw_crocodile": "cooked_crocodile",
    "egg":           "cooked_egg",
}


def _job_cooking(city: "PlayerCity", world, rec: dict, eff: float) -> None:
    cfg = rec.get("job_config") or {}
    sup_bx = cfg.get("supply_bx")
    sup_by = cfg.get("supply_by")
    out_bx = cfg.get("output_bx")
    out_by = cfg.get("output_by")
    if None in (sup_bx, sup_by, out_bx, out_by):
        return
    if world.get_block(sup_bx, sup_by) != CHEST_BLOCK:
        return
    if world.get_block(out_bx, out_by) != CHEST_BLOCK:
        return

    sup_inv = world.chest_data.get((sup_bx, sup_by), {})
    if not sup_inv:
        return

    batch = max(1, int(math.ceil((1 + rec["stats"].get("craft", 5) / 4) * eff)))
    out_inv = world.chest_data.setdefault((out_bx, out_by), {})

    cooked = 0
    for raw_id, cooked_id in _RAW_TO_COOKED.items():
        if cooked >= batch:
            break
        qty = sup_inv.get(raw_id, 0)
        if qty <= 0:
            continue
        take = min(qty, batch - cooked)
        sup_inv[raw_id] -= take
        if sup_inv[raw_id] <= 0:
            del sup_inv[raw_id]
        out_inv[cooked_id] = out_inv.get(cooked_id, 0) + take
        cooked += take


# ── Jobs dispatcher ───────────────────────────────────────────────────────────

def _process_jobs(city: "PlayerCity", world) -> None:
    for rec in city.npcs:
        if not rec.get("hired"):
            continue
        job = rec.get("job")
        if not job:
            continue
        eff = 0.5 if rec.get("disgruntled") else 1.0
        if job == "farming":
            _job_farming(city, world, rec, eff)
        elif job == "mining":
            _job_mining(city, world, rec, eff)
        elif job == "hauling":
            _job_hauling(city, world, rec, eff)
        elif job == "taming":
            _job_taming(city, world, rec, eff)
        elif job == "logging":
            _job_logging(city, world, rec, eff)
        elif job == "cooking":
            _job_cooking(city, world, rec, eff)


# ── Shared helpers ────────────────────────────────────────────────────────────

def _remove_settlers(city: "PlayerCity", world, id_set: set) -> None:
    city.npcs = [r for r in city.npcs if r["id"] not in id_set]
    from settler_npcs import SettlerNPC
    world.entities = [e for e in world.entities
                      if not (isinstance(e, SettlerNPC) and e.settler_id in id_set)]


def _city_notify(world, city: "PlayerCity", msg: str) -> None:
    if not hasattr(world, "_city_toasts"):
        world._city_toasts = []
    world._city_toasts.append(msg)


# ── Load / restore ────────────────────────────────────────────────────────────

def init_player_cities(world) -> None:
    """Restore player cities from the save database and re-spawn settler entities."""
    PLAYER_CITIES.clear()
    if not hasattr(world, "_save_mgr") or world._save_mgr is None:
        return
    city_data = world._save_mgr._load_player_cities()
    for d in city_data:
        city = PlayerCity.from_dict(d)
        PLAYER_CITIES[(city.bx, city.by)] = city
        from settler_npcs import spawn_settler_entity
        for record in city.npcs:
            spawn_settler_entity(world, city, record)
