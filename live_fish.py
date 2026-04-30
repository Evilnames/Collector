import math
import random
from constants import BLOCK_SIZE
from blocks import WATER, FISHING_SPOT_BLOCK


SPOOK_RADIUS_BLOCKS = 3
FLEE_DURATION       = 3.0


# ---------------------------------------------------------------------------
# Live fish definitions
# Each entry: species id (must exist in fish.FISH_TYPES) + biome filters and
# spawn behavior. Rare/legendary species are weighted lower in the spawn loop.
# ---------------------------------------------------------------------------

# Each entry references a real species id from fish.FISH_TYPES.
# `ocean_zones` filters by depth band ("surface", "reef", "twilight", "deep").
# Empty `ocean_zones` means surface/freshwater spawn.
LIVE_FISH_SPECIES = [
    # Freshwater / universal — spawn in any water, ocean_zones=[]
    {"species": "minnow",            "ocean_zones": [],            "rarity_weight": 12, "schooling": True},
    {"species": "perch",             "ocean_zones": [],            "rarity_weight": 8,  "schooling": True},
    {"species": "bass",              "ocean_zones": [],            "rarity_weight": 6,  "schooling": False},
    {"species": "bluegill",          "ocean_zones": [],            "rarity_weight": 8,  "schooling": True},
    {"species": "trout",             "ocean_zones": [],            "rarity_weight": 6,  "schooling": False},
    {"species": "salmon",            "ocean_zones": [],            "rarity_weight": 4,  "schooling": False},
    {"species": "pike",              "ocean_zones": [],            "rarity_weight": 3,  "schooling": False},
    # Ocean surface / coastal
    {"species": "sergeant_major",    "ocean_zones": ["tidal", "reef"], "rarity_weight": 8,  "schooling": True},
    # Reef
    {"species": "clownfish",         "ocean_zones": ["reef"],      "rarity_weight": 7,  "schooling": True},
    {"species": "damselfish",        "ocean_zones": ["reef"],      "rarity_weight": 9,  "schooling": True},
    {"species": "blue_tang",         "ocean_zones": ["reef"],      "rarity_weight": 6,  "schooling": True},
    {"species": "wrasse",            "ocean_zones": ["reef"],      "rarity_weight": 6,  "schooling": False},
    {"species": "parrotfish_reef",   "ocean_zones": ["reef"],      "rarity_weight": 5,  "schooling": False},
    {"species": "grouper",           "ocean_zones": ["reef"],      "rarity_weight": 5,  "schooling": False},
    {"species": "moorish_idol",      "ocean_zones": ["reef"],      "rarity_weight": 3,  "schooling": False},
    {"species": "lionfish",          "ocean_zones": ["reef"],      "rarity_weight": 2,  "schooling": False},
    {"species": "barracuda",         "ocean_zones": ["reef"],      "rarity_weight": 2,  "schooling": False},
    # Twilight
    {"species": "lanternfish",       "ocean_zones": ["twilight"],  "rarity_weight": 6,  "schooling": True},
    {"species": "flashlight_fish",   "ocean_zones": ["twilight"],  "rarity_weight": 3,  "schooling": False},
    {"species": "swordfish",         "ocean_zones": ["twilight"],  "rarity_weight": 2,  "schooling": False},
    # Deep / legendary
    {"species": "anglerfish",        "ocean_zones": ["deep"],      "rarity_weight": 1,  "schooling": False},
]


# Default colors used when a species has no entry in fish.FISH_TYPES.
_FALLBACK_COLORS = ((180, 200, 220), (110, 140, 175))


def _species_colors(species):
    try:
        from fish import FISH_TYPES
    except Exception:
        return _FALLBACK_COLORS
    fdata = FISH_TYPES.get(species)
    if not fdata:
        return _FALLBACK_COLORS
    colors = fdata.get("colors") or []
    if not colors:
        return _FALLBACK_COLORS
    return colors[0]


class LiveFish:
    """A fish entity swimming in WATER blocks. Modeled on the Insect base class."""
    W = 14
    H = 6

    def __init__(self, x, y, world, species, rarity, seed,
                 biome="ocean", ocean_zone="", schooling=False):
        self.x = float(x)
        self.y = float(y)
        self._spawn_x = float(x)
        self._spawn_y = float(y)
        self.vx = random.choice([-1.0, 1.0]) * 18.0
        self.vy = 0.0
        self.world = world
        self.species = species
        self.rarity = rarity
        self.seed = seed
        self.biome = biome
        self.ocean_zone = ocean_zone
        self.schooling = schooling
        self.dead = False
        self.spooked = False
        self._spook_timer = 0.0
        self._drift_timer = random.uniform(1.0, 3.0)
        self._drift_phase = random.uniform(0.0, math.pi * 2)
        self._target_x = self._spawn_x
        self._target_y = self._spawn_y
        self.facing = -1 if self.vx < 0 else 1
        primary, secondary = _species_colors(species)
        self.primary_color = primary
        self.secondary_color = secondary
        self.HOVER_RANGE = 80  # pixels

    @property
    def rect(self):
        import pygame
        return pygame.Rect(int(self.x), int(self.y), self.W, self.H)

    def _is_water_at(self, px, py):
        bx = int(px // BLOCK_SIZE)
        by = int(py // BLOCK_SIZE)
        bid = self.world.get_block(bx, by)
        return bid == WATER or bid == FISHING_SPOT_BLOCK

    def update(self, dt):
        if self.dead:
            return

        self._drift_phase += dt * 2.4

        if self.spooked:
            self._spook_timer += dt
            if self._spook_timer >= FLEE_DURATION:
                self.spooked = False
                self._spook_timer = 0.0
        else:
            player = getattr(self.world, "_player_ref", None)
            if player is not None:
                dx_b = abs(player.x - self.x) / BLOCK_SIZE
                dy_b = abs(player.y - self.y) / BLOCK_SIZE
                if dx_b < SPOOK_RADIUS_BLOCKS and dy_b < SPOOK_RADIUS_BLOCKS:
                    if getattr(player, "_in_water", lambda: False)():
                        self.spooked = True
                        self._spook_timer = 0.0
                        # flee away from player
                        self.vx = -math.copysign(50.0, player.x - self.x)
                        self.vy = -math.copysign(20.0, player.y - self.y)

        if not self.spooked:
            self._drift_timer -= dt
            if self._drift_timer <= 0:
                self._drift_timer = random.uniform(1.5, 3.5)
                angle = random.uniform(0, math.pi * 2)
                dist = random.uniform(self.HOVER_RANGE * 0.3, self.HOVER_RANGE)
                self._target_x = self._spawn_x + math.cos(angle) * dist
                self._target_y = self._spawn_y + math.sin(angle) * dist * 0.5

            dx = self._target_x - self.x
            dy = self._target_y - self.y
            d = math.hypot(dx, dy)
            speed = 22.0
            if d > 2.0:
                self.vx = (dx / d) * speed
                self.vy = (dy / d) * speed * 0.5

        # Apply movement
        new_x = self.x + self.vx * dt
        new_y = self.y + self.vy * dt + math.sin(self._drift_phase) * 0.3

        # Clamp to water — bounce off air or solid
        if self._is_water_at(new_x + self.W / 2, new_y + self.H / 2):
            self.x = new_x
            self.y = new_y
        else:
            self.vx = -self.vx
            self.vy = -abs(self.vy)
            self._target_x = self._spawn_x
            self._target_y = self._spawn_y

        if self.vx < 0:
            self.facing = -1
        elif self.vx > 0:
            self.facing = 1
