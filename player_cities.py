"""
player_cities.py — Data model and daily tick for player-established cities.

Each city is anchored by a CITY_BLOCK placed in the world.
The registry is keyed by (bx, by) of that block.
"""

import random
from dataclasses import dataclass, field

from blocks import BED, CHEST_BLOCK

# City region half-width in blocks (±80 tiles)
CITY_REGION_HALF = 80
# Vertical scan range around the city block for beds/chests
_SCAN_V_HALF = 50

# ── Data ─────────────────────────────────────────────────────────────────────

@dataclass
class PlayerCity:
    bx: int
    by: int
    name: str = "Unnamed City"
    coat_of_arms: dict = field(default_factory=lambda: {
        "shape":        "heater",
        "bg_color":     [60, 100, 180],
        "pattern":      "none",
        "charge":       "none",
        "charge_color": [240, 220, 160],
    })
    treasury: int = 0
    npcs: list = field(default_factory=list)   # list of settler record dicts

    @property
    def population(self):
        return len(self.npcs)

    def count_beds(self, world) -> int:
        """Count BED blocks within the city region."""
        total = 0
        y0 = max(0, self.by - _SCAN_V_HALF)
        y1 = min(world.height - 1, self.by + _SCAN_V_HALF)
        for bx in range(self.bx - CITY_REGION_HALF, self.bx + CITY_REGION_HALF + 1):
            for by in range(y0, y1 + 1):
                if world.get_block(bx, by) == BED:
                    total += 1
        return total

    def count_food_chests(self, world) -> int:
        """Count CHEST_BLOCK blocks within the region that contain at least one food item."""
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


# ── Registry ──────────────────────────────────────────────────────────────────

PLAYER_CITIES: dict[tuple[int, int], PlayerCity] = {}


def register_city(bx: int, by: int) -> "PlayerCity":
    """Create a new PlayerCity at (bx, by) and register it. Returns the city."""
    city = PlayerCity(bx=bx, by=by)
    PLAYER_CITIES[(bx, by)] = city
    return city


def remove_city(bx: int, by: int) -> None:
    PLAYER_CITIES.pop((bx, by), None)


def get_city_at(bx: int, by: int) -> "PlayerCity | None":
    return PLAYER_CITIES.get((bx, by))


def get_city_for_block(world, bx: int, by: int) -> "PlayerCity | None":
    return PLAYER_CITIES.get((bx, by))


# ── Dawn tick ─────────────────────────────────────────────────────────────────

def tick_city_day(world) -> None:
    """Called once per in-game dawn. Processes declines then runs attraction rolls."""
    for city in PLAYER_CITIES.values():
        _process_declines(city, world)
        _run_attraction(city, world)


def _process_declines(city: PlayerCity, world) -> None:
    """Countdown declined settlers; remove those whose time is up."""
    to_remove = []
    for rec in city.npcs:
        if "decline_days_remaining" not in rec:
            continue
        rec["decline_days_remaining"] -= 1
        if rec["decline_days_remaining"] <= 0:
            to_remove.append(rec["id"])

    if not to_remove:
        return

    # Remove settler records
    city.npcs = [r for r in city.npcs if r["id"] not in to_remove]

    # Remove matching entities from world
    from settler_npcs import SettlerNPC
    world.entities = [e for e in world.entities
                      if not (isinstance(e, SettlerNPC) and e.settler_id in to_remove)]


def _run_attraction(city: PlayerCity, world) -> None:
    """Roll attraction for one city and spawn settlers into world.entities."""
    beds       = city.count_beds(world)
    food_chests = city.count_food_chests(world)
    unemployed = city.count_unemployed()

    if beds == 0:
        return

    # Each bed is an independent attraction roll
    for _ in range(beds):
        chance = 0.15                          # base 15%
        chance += 0.05 * food_chests           # +5% per food chest
        chance -= 0.05 * unemployed            # -5% per unhired settler
        chance = max(0.0, min(0.95, chance))

        if random.random() >= chance:
            continue

        # Attraction succeeded — generate a settler
        from settler_npcs import generate_settler_record, spawn_settler_entity
        day    = getattr(world, "day_count", 0)
        index  = len(city.npcs)
        record = generate_settler_record(city.bx, city.by, world.seed, day, index)
        city.npcs.append(record)
        spawn_settler_entity(world, city, record)

        # Notify player via _city_toasts (drained in main.py)
        if not hasattr(world, "_city_toasts"):
            world._city_toasts = []
        world._city_toasts.append(
            f"A traveler has arrived in {city.name} and is seeking work."
        )

        # Only attract one settler per bed per day (break after first success this bed)
        unemployed += 1   # update count so subsequent beds see the new arrival


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
        # Re-spawn settler entities that were alive when the game was saved
        from settler_npcs import spawn_settler_entity
        for record in city.npcs:
            spawn_settler_entity(world, city, record)
