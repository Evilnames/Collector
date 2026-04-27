"""
settler_npcs.py — SettlerNPC class for player-run cities.

Settlers are procedurally generated NPCs that wander the city region.
They are interactable (is_ambient = False) so the player can open the
hire panel (Section C). Stats and trait are rolled at generation and
stored in the owning PlayerCity's npcs list.
"""

import random
import math

from cities import AmbientNPC
from constants import BLOCK_SIZE

_SETTLER_TRAITS = [
    "hardworking",
    "lazy",
    "skilled with their hands",
    "clumsy but earnest",
    "sharp-minded",
    "strong as an ox",
    "quick on their feet",
    "steady and reliable",
    "easily distracted",
    "unusually gifted with animals",
]


class SettlerNPC(AmbientNPC):
    """A wandering settler seeking work in a player city."""

    is_ambient = False  # interactable: opens hire panel on [E]

    def __init__(self, x, y, world, city_bx: int, settler_id: str):
        patrol_half = 80 * BLOCK_SIZE
        super().__init__(x, y, world, "settler", patrol_half)
        self.patrol_cx  = city_bx * BLOCK_SIZE
        self.settler_id = settler_id
        # These are set after construction from the npc record dict
        self.display_name        = ""
        self.settler_trait       = ""
        self.settler_stats: dict = {}
        self.settler_hired       = False
        self.settler_disgruntled = False
        self.settler_city_bx     = city_bx

    def update(self, dt):
        from world import DAY_DURATION
        tod = getattr(self.world, "time_of_day", 0.0)
        if tod >= DAY_DURATION:
            # Go home (return toward city block) at night
            self._walk_speed = 0.0
            dx = self.patrol_cx - self.x
            if abs(dx) > 4:
                self.x += dx * min(1.0, dt * 2.0)
        else:
            self._walk_speed = 28.0
        super().update(dt)

    def in_range(self, player) -> bool:
        return (abs(self.x - player.x) < 64 and
                abs(self.y - player.y) < 64)


# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------

def _roll_stats(rng: random.Random) -> dict:
    return {
        "strength":       rng.randint(1, 10),
        "agility":        rng.randint(1, 10),
        "craft":          rng.randint(1, 10),
        "endurance":      rng.randint(1, 10),
        "intelligence":   rng.randint(1, 10),
        "animal_affinity":rng.randint(1, 10),
    }


def _wage_from_stats(stats: dict) -> int:
    """Daily wage scales with total stat quality: 5–25 coins."""
    total = sum(stats.values())   # 6–60
    return max(5, min(25, total // 4))


def generate_settler_record(city_bx: int, city_by: int, world_seed: int, day: int, index: int) -> dict:
    """Return a settler data dict. All fields are serialisable."""
    settler_id = f"settler_{city_bx}_{city_by}_{day}_{index}"
    rng = random.Random(hash((settler_id, world_seed)) & 0xFFFFFFFF)

    gender = rng.choice(("m", "f"))

    import npc_identity as _nid
    names_m = _nid._FIRST_NAMES_M
    names_f = _nid._FIRST_NAMES_F
    family_names = _nid._FAMILY_NAMES
    first = rng.choice(names_m if gender == "m" else names_f)
    family = rng.choice(family_names)

    trait = rng.choice(_SETTLER_TRAITS)
    stats = _roll_stats(rng)
    wage  = _wage_from_stats(stats)

    return {
        "id":         settler_id,
        "name":       f"{first} {family}",
        "gender":     gender,
        "trait":      trait,
        "stats":      stats,
        "hired":      False,
        "job":        None,
        "job_config": {},
        "wage":       wage,
        "days_unpaid":  0,
        "days_unfed":   0,
        "disgruntled":  False,
    }


def sync_settler_entity(world, record: dict) -> None:
    """Push record flags onto the live SettlerNPC entity (call after upkeep changes)."""
    for e in world.entities:
        if isinstance(e, SettlerNPC) and e.settler_id == record["id"]:
            e.settler_hired      = record.get("hired", False)
            e.settler_disgruntled = record.get("disgruntled", False)
            break


def spawn_settler_entity(world, city, record: dict) -> SettlerNPC:
    """Create a SettlerNPC entity and add it to world.entities."""
    from constants import BLOCK_SIZE as BS
    spawn_bx = city.bx + random.randint(-3, 3)
    spawn_y  = world.surface_y_at(spawn_bx) * BS - 28
    spawn_x  = spawn_bx * BS

    npc = SettlerNPC(spawn_x, spawn_y, world, city.bx, record["id"])
    npc.display_name         = record["name"]
    npc.settler_trait        = record["trait"]
    npc.settler_stats        = record["stats"]
    npc.settler_hired        = record.get("hired", False)
    npc.settler_disgruntled  = record.get("disgruntled", False)

    world.entities.append(npc)
    return npc
