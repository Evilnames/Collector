import random
import math
from constants import BLOCK_SIZE

from blocks import (
    TREE_LEAVES, PINE_LEAVES, BIRCH_LEAVES, JUNGLE_LEAVES, WILLOW_LEAVES,
    REDWOOD_LEAVES, PALM_LEAVES, ACACIA_LEAVES, MAPLE_LEAVES, CHERRY_LEAVES,
    BIRD_FEEDER_BLOCK, BIRD_BATH_BLOCK, WATER,
)

LEAF_BLOCKS = frozenset({
    TREE_LEAVES, PINE_LEAVES, BIRCH_LEAVES, JUNGLE_LEAVES, WILLOW_LEAVES,
    REDWOOD_LEAVES, PALM_LEAVES, ACACIA_LEAVES, MAPLE_LEAVES, CHERRY_LEAVES,
})
FEEDER_BATH_BLOCKS = frozenset({BIRD_FEEDER_BLOCK, BIRD_BATH_BLOCK})

SPOOK_SPEED_THRESHOLD = 0.8   # px/frame — player vx above this counts as moving
SPOOK_RADIUS_BLOCKS   = 5     # blocks

_PERSONALITY_TRAITS = {
    "timid":   {"spook_mult": 1.6,  "rest_mult": 0.5},
    "wary":    {"spook_mult": 1.25, "rest_mult": 0.8},
    "normal":  {"spook_mult": 1.0,  "rest_mult": 1.0},
    "bold":    {"spook_mult": 0.55, "rest_mult": 1.4},
    "curious": {"spook_mult": 0.75, "rest_mult": 1.5},
}


class Bird:
    SPECIES           = "unknown"
    RARITY            = "common"
    BIOMES            = []        # empty = any biodome
    IS_FLOCK          = False
    FLOCK_SIZE_RANGE  = (1, 1)
    ALTITUDE_BLOCKS   = (3, 8)   # height range above surface (in blocks)
    SPEED             = 65.0     # pixels / second while flying
    W, H              = 14, 10
    BODY_COLOR        = (120, 100, 80)
    WING_COLOR        = (100, 80, 60)
    BEAK_COLOR        = (200, 160, 40)
    HEAD_COLOR        = (120, 100, 80)
    ACCENT_COLOR      = (200, 120, 40)
    PERSONALITY       = "normal"    # timid, wary, normal, bold, curious
    NOCTURNAL         = False

    def __init__(self, x, y, world):
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.facing = random.choice([-1, 1])
        self.world  = world

        self.state        = "flying"
        self._state_timer = 0.0

        self._target_x  = float(x)
        self._target_y  = float(y)
        self._perch_bx  = None
        self._perch_by  = None

        self._wing_phase = random.uniform(0, math.pi * 2)
        self._bob_phase  = random.uniform(0, math.pi * 2)

        self._flock_leader = None          # Bird ref if this is a follower
        self._flock_offset = (0.0, 0.0)   # pixel offset from leader (followers only)

        self._perch_type = "leaf"  # "leaf", "feeder", or "bath"

        self.animal_id = f"bird_{self.SPECIES}"

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _surface_y_at(self, bx):
        try:
            return self.world.surface_height(int(bx))
        except Exception:
            return 40  # fallback

    def _flyable_surface_y_at(self, bx):
        """Like _surface_y_at but returns the water surface over oceans, not the ocean floor."""
        sy = self._surface_y_at(bx)
        # Scan upward from terrain; if we're in water, find where water ends
        for wy in range(sy - 1, max(0, sy - 40), -1):
            if self.world.get_block(int(bx), wy) != WATER:
                return wy + 1  # first block above air is the water surface
        return sy

    def _find_leaf_above(self, bx):
        """Scan upward from surface to find lowest leaf block at bx. Returns by or None."""
        sy = self._surface_y_at(bx)
        for by in range(sy - 1, max(0, sy - 16), -1):
            bid = self.world.get_block(int(bx), by)
            if bid in LEAF_BLOCKS:
                return by
        return None

    def _find_feeder_bath(self, radius=80):
        """Scan nearby blocks for a bird feeder or bath. Returns (bx, by, bid) or None."""
        bx_center = int(self.x // BLOCK_SIZE)
        results = []
        for bx in range(bx_center - radius, bx_center + radius):
            sy = self._surface_y_at(bx)
            for by in range(sy - 5, sy + 2):
                bid = self.world.get_block(bx, by)
                if bid in FEEDER_BATH_BLOCKS:
                    results.append((bx, by, bid))
        return random.choice(results) if results else None

    def _pick_flight_target(self, rng=None):
        """Pick a new (target_x, target_y) roughly ±30–100 blocks away."""
        rng = rng or random
        # 40% base chance to head toward a feeder or bath if one exists nearby
        _player = getattr(self.world, '_player_ref', None)
        _feeder_mult = getattr(_player, 'bird_feeder_bonus', 1.0) if _player else 1.0
        if rng.random() < min(0.90, 0.40 * _feeder_mult):
            fb = self._find_feeder_bath()
            if fb:
                bx, by, _ = fb
                self._target_x = float(bx * BLOCK_SIZE + BLOCK_SIZE // 2)
                sy = self._surface_y_at(bx)
                self._target_y = float((sy - 3) * BLOCK_SIZE)
                self.facing = 1 if self._target_x > self.x else -1
                return
        direction = rng.choice([-1, 1])
        dist = rng.uniform(30, 100) * BLOCK_SIZE
        tx_px = self.x + direction * dist
        tx_bx = int(tx_px // BLOCK_SIZE)
        sy    = self._flyable_surface_y_at(tx_bx)
        alt   = rng.randint(*self.ALTITUDE_BLOCKS) * BLOCK_SIZE
        ty_px = sy * BLOCK_SIZE - alt
        self._target_x = tx_px
        self._target_y = float(ty_px)
        self.facing    = direction

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def spook(self):
        """Force bird to take off immediately."""
        self.state        = "taking_off"
        self._state_timer = 0.0
        self.vy           = -60.0
        self._pick_flight_target()

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------

    def update(self, dt):
        self._wing_phase += dt * 8.0
        self._bob_phase  += dt * 2.5

        if self.state == "perching":
            self._update_perching(dt)
        elif self.state == "taking_off":
            self._update_taking_off(dt)
        elif self.state == "flying":
            self._update_flying(dt)
        elif self.state == "landing":
            self._update_landing(dt)

    def _player_dist_blocks(self):
        player = getattr(self.world, '_player_ref', None)
        if player is None:
            return 999.0
        dx = (self.x - player.x) / BLOCK_SIZE
        dy = (self.y - player.y) / BLOCK_SIZE
        return (dx * dx + dy * dy) ** 0.5

    def _player_moving(self):
        player = getattr(self.world, '_player_ref', None)
        if player is None:
            return False
        return abs(getattr(player, 'vx', 0.0)) > SPOOK_SPEED_THRESHOLD

    def _update_perching(self, dt):
        self._state_timer -= dt
        self.vx = 0.0
        self.vy = 0.0
        # Birds at feeders/baths are calmer; water perches are slightly skittish
        if self._perch_type in ("feeder", "bath"):
            spook_radius = 12
        elif self._perch_type == "water":
            spook_radius = SPOOK_RADIUS_BLOCKS + 2
        else:
            spook_radius = SPOOK_RADIUS_BLOCKS
        player = getattr(self.world, '_player_ref', None)
        reduction = getattr(player, 'bird_spook_reduction', 0.0) if player else 0.0
        spook_radius = spook_radius * (1.0 - reduction) * _PERSONALITY_TRAITS[self.PERSONALITY]["spook_mult"]
        if (self._player_dist_blocks() < spook_radius and self._player_moving()):
            self.spook()
            return
        if self._state_timer <= 0:
            self._perch_type  = "leaf"
            self.state        = "taking_off"
            self._state_timer = 0.0
            self.vy           = -80.0
            self._pick_flight_target()

    def _update_taking_off(self, dt):
        self._state_timer += dt
        self.vy = -80.0
        self.vx = self.facing * self.SPEED * 0.5
        self.x += self.vx * dt
        self.y += self.vy * dt
        if self._state_timer >= 0.4:
            self.state        = "flying"
            self._state_timer = 0.0

    def _update_flying(self, dt):
        if self._flock_leader is not None:
            # Follower: track leader + offset
            leader = self._flock_leader
            tx = leader.x + self._flock_offset[0]
            ty = leader.y + self._flock_offset[1]
        else:
            tx = self._target_x
            ty = self._target_y

        dx = tx - self.x
        dy = ty - self.y
        dist = (dx * dx + dy * dy) ** 0.5

        if dist < 24 and self._flock_leader is None:
            # Reached target — try to land
            self.state        = "landing"
            self._state_timer = 0.0
            return

        if dist > 0.1:
            spd = self.SPEED
            self.vx = (dx / dist) * spd
            self.vy = (dy / dist) * spd
            # Gentle sine-wave bob
            self.vy += math.sin(self._bob_phase) * 10.0
            self.facing = 1 if self.vx > 0 else -1

        self.x += self.vx * dt
        self.y += self.vy * dt

        # Don't fly above the near-sky ceiling (y < 5 blocks from top)
        if self.y < 5 * BLOCK_SIZE:
            self.y = 5 * BLOCK_SIZE

        # Don't fly below the surface (or below water surface over oceans)
        bx = int(self.x // BLOCK_SIZE)
        sy = self._flyable_surface_y_at(bx)
        ground_limit = (sy - 1) * BLOCK_SIZE
        if self.y > ground_limit:
            self.y = ground_limit
            if self.vy > 0:
                self.vy = 0.0

    def _find_feeder_bath_at(self, tx_bx, scan_radius=4):
        """Scan ±scan_radius blocks around tx_bx on the surface for a feeder/bath."""
        for dbx in range(-scan_radius, scan_radius + 1):
            bx = tx_bx + dbx
            sy = self._surface_y_at(bx)
            for by in range(sy - 5, sy + 2):
                bid = self.world.get_block(bx, by)
                if bid in FEEDER_BATH_BLOCKS:
                    return bx, by, bid
        return None

    def _update_landing(self, dt):
        # Descend toward perch
        tx_bx = int(self._target_x // BLOCK_SIZE)

        # Check for a feeder or bath near the target first
        fb = self._find_feeder_bath_at(tx_bx)
        if fb:
            fbx, fby, fbid = fb
            perch_x = float(fbx * BLOCK_SIZE + BLOCK_SIZE // 2)
            perch_y = float(fby * BLOCK_SIZE)  # sit on top of the block
            dx = perch_x - self.x
            dy = perch_y - self.y
            dist = (dx * dx + dy * dy) ** 0.5
            if dist < 8:
                self.x            = perch_x
                self.y            = perch_y
                self.vx           = 0.0
                self.vy           = 0.0
                self._perch_bx    = fbx
                self._perch_by    = fby
                self._perch_type  = "feeder" if fbid == BIRD_FEEDER_BLOCK else "bath"
                self._state_timer = random.uniform(20, 60) * _PERSONALITY_TRAITS[self.PERSONALITY]["rest_mult"]
                self.state        = "perching"
                return
            spd = self.SPEED * 0.5
            if dist > 0.1:
                self.vx = (dx / dist) * spd
                self.vy = (dy / dist) * spd
            self.x += self.vx * dt
            self.y += self.vy * dt
            return

        leaf_by = self._find_leaf_above(tx_bx)

        if leaf_by is None:
            # Check if this is a water surface — birds can float on water
            sy = self._surface_y_at(tx_bx)
            if self.world.get_block(int(tx_bx), sy) == WATER:
                perch_y = float(sy * BLOCK_SIZE)
                dx = self._target_x - self.x
                dy = perch_y - self.y
                dist = (dx * dx + dy * dy) ** 0.5
                if dist < 8:
                    self.x            = self._target_x
                    self.y            = perch_y
                    self.vx           = 0.0
                    self.vy           = 0.0
                    self._perch_bx    = int(tx_bx)
                    self._perch_by    = sy
                    self._perch_type  = "water"
                    self._state_timer = random.uniform(5, 15) * _PERSONALITY_TRAITS[self.PERSONALITY]["rest_mult"]
                    self.state        = "perching"
                    return
                spd = self.SPEED * 0.5
                if dist > 0.1:
                    self.vx = (dx / dist) * spd
                    self.vy = (dy / dist) * spd
                self.x += self.vx * dt
                self.y += self.vy * dt
                return
            # No tree or water here — fly somewhere else
            self._pick_flight_target()
            self.state = "flying"
            return

        perch_y = (leaf_by - 1) * BLOCK_SIZE  # sit just above the leaf

        dx = self._target_x - self.x
        dy = perch_y - self.y
        dist = (dx * dx + dy * dy) ** 0.5

        if dist < 8:
            # Snap to perch
            self.x            = self._target_x
            self.y            = float(perch_y)
            self.vx           = 0.0
            self.vy           = 0.0
            self._perch_bx    = tx_bx
            self._perch_by    = leaf_by
            self._perch_type  = "leaf"
            self._state_timer = random.uniform(5, 20) * _PERSONALITY_TRAITS[self.PERSONALITY]["rest_mult"]
            self.state        = "perching"
            return

        spd = self.SPEED * 0.5
        if dist > 0.1:
            self.vx = (dx / dist) * spd
            self.vy = (dy / dist) * spd
        self.x += self.vx * dt
        self.y += self.vy * dt


# ======================================================================
# Ground Birds
# ======================================================================

class GroundBird(Bird):
    """Birds that stay on the surface and walk/run rather than fly."""
    IS_GROUND       = True
    ALTITUDE_BLOCKS = (0, 1)

    def __init__(self, x, y, world):
        super().__init__(x, y, world)
        self.state        = "walking"
        self._state_timer = 0.0
        self._pick_walk_target()

    def _pick_walk_target(self, rng=None):
        rng = rng or random
        direction = rng.choice([-1, 1])
        dist = rng.uniform(5, 25) * BLOCK_SIZE
        self._target_x = self.x + direction * dist
        self.facing    = direction

    # Overridden so world spawn logic works without change
    def _pick_flight_target(self, rng=None):
        self._pick_walk_target(rng)

    def _ground_y(self):
        bx = int(self.x // BLOCK_SIZE)
        sy_guess = self._surface_y_at(bx)
        # Scan for the actual topmost solid block — terrain may have been
        # built up (towns, walls) or dug out, so the procedural surface alone
        # leaves birds floating or buried.
        for by in range(max(0, sy_guess - 24), sy_guess + 32):
            if self.world.is_solid(bx, by):
                return float((by - 1) * BLOCK_SIZE)
        return float((sy_guess - 1) * BLOCK_SIZE)

    def spook(self):
        player = getattr(self.world, '_player_ref', None)
        if player:
            self.facing = 1 if self.x > player.x else -1
        else:
            self.facing = random.choice([-1, 1])
        self._target_x  = self.x + self.facing * 30 * BLOCK_SIZE
        self.state       = "fleeing"
        self._state_timer = 0.0

    def update(self, dt):
        self._wing_phase += dt * 3.0  # slow fold/bob, not flying

        if self.state == "walking":
            self._update_walking(dt)
        elif self.state == "stopped":
            self._update_stopped(dt)
        elif self.state == "fleeing":
            self._update_fleeing(dt)

        # Always stay on the surface
        self.y  = self._ground_y()
        self.vy = 0.0

    def _spook_radius(self):
        player    = getattr(self.world, '_player_ref', None)
        reduction = getattr(player, 'bird_spook_reduction', 0.0) if player else 0.0
        mult      = _PERSONALITY_TRAITS[self.PERSONALITY]["spook_mult"]
        return SPOOK_RADIUS_BLOCKS * mult * (1.0 - reduction)

    def _update_walking(self, dt):
        if self._flock_leader is not None:
            target_x = self._flock_leader.x + self._flock_offset[0]
        else:
            target_x = self._target_x

        dx = target_x - self.x
        if abs(dx) < 8:
            if self._flock_leader is None:
                traits = _PERSONALITY_TRAITS[self.PERSONALITY]
                self._state_timer = random.uniform(1, 4) * traits["rest_mult"]
                self.state = "stopped"
            self.vx = 0.0
            return

        self.facing = 1 if dx > 0 else -1
        self.vx     = self.facing * self.SPEED * 0.4
        self.x     += self.vx * dt

        if self._player_dist_blocks() < self._spook_radius() and self._player_moving():
            self.spook()

    def _update_stopped(self, dt):
        self._state_timer -= dt
        self.vx = 0.0
        if self._player_dist_blocks() < self._spook_radius() and self._player_moving():
            self.spook()
            return
        if self._state_timer <= 0:
            self._pick_walk_target()
            self.state = "walking"

    def _update_fleeing(self, dt):
        self._state_timer += dt
        dx = self._target_x - self.x
        if abs(dx) < 8 or self._state_timer > 4.0:
            if self._player_dist_blocks() > SPOOK_RADIUS_BLOCKS * 2:
                self._pick_walk_target()
                self.state        = "walking"
                self._state_timer = 0.0
            else:
                # Still too close — extend flee
                self._target_x    = self.x + self.facing * 20 * BLOCK_SIZE
                self._state_timer = 0.0
            return
        self.vx  = self.facing * self.SPEED
        self.x  += self.vx * dt


class Nest:
    """A ground nest belonging to a GroundBird species."""
    def __init__(self, bx, by, species_cls):
        self.bx      = bx
        self.by      = by       # surface block row
        self.species = species_cls.SPECIES
        self.eggs    = random.randint(0, 3)


# ======================================================================
# Species
# ======================================================================

class Robin(Bird):
    SPECIES          = "robin"
    RARITY           = "common"
    BIOMES           = ["temperate", "birch_forest", "rolling_hills", "boreal"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (3, 7)
    SPEED            = 65.0
    W, H             = 14, 10
    BODY_COLOR       = (80, 55, 35)
    WING_COLOR       = (65, 45, 28)
    BEAK_COLOR       = (200, 140, 40)
    HEAD_COLOR       = (70, 48, 30)
    ACCENT_COLOR     = (215, 95, 40)   # orange-red breast


class BlueJay(Bird):
    SPECIES          = "blue_jay"
    RARITY           = "uncommon"
    BIOMES           = ["temperate", "birch_forest"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 4)
    ALTITUDE_BLOCKS  = (4, 9)
    SPEED            = 70.0
    W, H             = 16, 12
    BODY_COLOR       = (70, 120, 210)
    WING_COLOR       = (55, 95, 175)
    BEAK_COLOR       = (45, 45, 55)
    HEAD_COLOR       = (60, 105, 195)
    ACCENT_COLOR     = (240, 240, 240)  # white underside


class Eagle(Bird):
    SPECIES          = "eagle"
    RARITY           = "rare"
    BIOMES           = ["alpine_mountain", "rocky_mountain", "canyon"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (6, 14)
    SPEED            = 100.0
    W, H             = 22, 14
    BODY_COLOR       = (90, 60, 25)
    WING_COLOR       = (75, 50, 20)
    BEAK_COLOR       = (240, 190, 40)
    HEAD_COLOR       = (240, 240, 235)  # white head
    ACCENT_COLOR     = (240, 190, 40)   # yellow talons/beak


class Pelican(Bird):
    SPECIES          = "pelican"
    RARITY           = "uncommon"
    BIOMES           = ["beach", "wetland", "swamp"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (3, 5)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 60.0
    W, H             = 22, 14
    BODY_COLOR       = (225, 225, 225)
    WING_COLOR       = (200, 200, 200)
    BEAK_COLOR       = (235, 140, 30)
    HEAD_COLOR       = (225, 225, 225)
    ACCENT_COLOR     = (235, 140, 30)   # orange pouch


class Parrot(Bird):
    SPECIES          = "parrot"
    RARITY           = "uncommon"
    BIOMES           = ["jungle", "tropical"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 2)
    ALTITUDE_BLOCKS  = (3, 8)
    SPEED            = 75.0
    W, H             = 16, 12
    BODY_COLOR       = (50, 185, 70)
    WING_COLOR       = (40, 160, 55)
    BEAK_COLOR       = (210, 80, 30)
    HEAD_COLOR       = (220, 60, 40)    # red head
    ACCENT_COLOR     = (240, 210, 40)   # yellow wing-bar


class Sparrow(Bird):
    SPECIES          = "sparrow"
    RARITY           = "common"
    BIOMES           = ["temperate", "birch_forest", "rolling_hills", "steep_hills",
                        "boreal", "savanna", "steppe", "arid_steppe", "redwood"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (3, 6)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 60.0
    W, H             = 10, 8
    BODY_COLOR       = (130, 105, 75)
    WING_COLOR       = (110, 85, 60)
    BEAK_COLOR       = (170, 130, 60)
    HEAD_COLOR       = (100, 80, 55)
    ACCENT_COLOR     = (60, 45, 30)    # dark stripe


class Heron(Bird):
    SPECIES          = "heron"
    RARITY           = "uncommon"
    BIOMES           = ["wetland", "swamp", "beach"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 5)
    SPEED            = 45.0
    W, H             = 14, 20
    BODY_COLOR       = (145, 155, 165)
    WING_COLOR       = (125, 135, 145)
    BEAK_COLOR       = (245, 235, 80)
    HEAD_COLOR       = (230, 230, 235)
    ACCENT_COLOR     = (40, 40, 55)    # dark crown stripe


class Hummingbird(Bird):
    SPECIES          = "hummingbird"
    RARITY           = "rare"
    BIOMES           = ["jungle", "tropical", "temperate"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 150.0
    W, H             = 10, 8
    BODY_COLOR       = (50, 200, 130)
    WING_COLOR       = (40, 175, 110)
    BEAK_COLOR       = (40, 40, 50)
    HEAD_COLOR       = (50, 200, 130)
    ACCENT_COLOR     = (210, 80, 50)   # red throat


class Owl(Bird):
    SPECIES          = "owl"
    RARITY           = "uncommon"
    BIOMES           = ["boreal", "redwood", "birch_forest", "temperate"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (3, 8)
    SPEED            = 65.0
    W, H             = 18, 14
    BODY_COLOR       = (145, 120, 80)
    WING_COLOR       = (120, 100, 65)
    BEAK_COLOR       = (215, 185, 80)
    HEAD_COLOR       = (155, 130, 85)
    ACCENT_COLOR     = (245, 220, 130)  # pale face disc


class Crow(Bird):
    SPECIES          = "crow"
    RARITY           = "common"
    BIOMES           = ["temperate", "birch_forest", "boreal", "rolling_hills",
                        "steep_hills", "wasteland", "savanna", "redwood"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 4)
    ALTITUDE_BLOCKS  = (3, 9)
    SPEED            = 70.0
    W, H             = 16, 12
    BODY_COLOR       = (30, 30, 35)
    WING_COLOR       = (25, 25, 30)
    BEAK_COLOR       = (40, 40, 45)
    HEAD_COLOR       = (30, 30, 35)
    ACCENT_COLOR     = (60, 60, 70)    # slight sheen


class Flamingo(Bird):
    SPECIES          = "flamingo"
    RARITY           = "uncommon"
    BIOMES           = ["tropical", "wetland", "beach", "savanna"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (3, 6)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 50.0
    W, H             = 14, 20
    BODY_COLOR       = (235, 120, 130)
    WING_COLOR       = (210, 75, 95)
    BEAK_COLOR       = (28, 24, 24)
    HEAD_COLOR       = (240, 130, 140)
    ACCENT_COLOR     = (255, 210, 60)


class Toucan(Bird):
    SPECIES          = "toucan"
    RARITY           = "rare"
    BIOMES           = ["jungle", "tropical"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (3, 8)
    SPEED            = 70.0
    W, H             = 18, 14
    BODY_COLOR       = (20, 20, 25)
    WING_COLOR       = (20, 20, 25)
    BEAK_COLOR       = (230, 140, 30)
    HEAD_COLOR       = (20, 20, 25)
    ACCENT_COLOR     = (255, 255, 85)   # yellow chest


class Cardinal(Bird):
    SPECIES          = "cardinal"
    RARITY           = "uncommon"
    BIOMES           = ["temperate", "birch_forest", "rolling_hills"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 65.0
    W, H             = 14, 12
    BODY_COLOR       = (210, 30, 30)
    WING_COLOR       = (175, 22, 22)
    BEAK_COLOR       = (220, 140, 50)
    HEAD_COLOR       = (210, 30, 30)
    ACCENT_COLOR     = (25, 25, 25)     # black mask


class Puffin(Bird):
    SPECIES          = "puffin"
    RARITY           = "uncommon"
    BIOMES           = ["beach", "tundra"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 4)
    ALTITUDE_BLOCKS  = (2, 5)
    SPEED            = 75.0
    W, H             = 14, 10
    BODY_COLOR       = (20, 20, 25)
    WING_COLOR       = (20, 20, 25)
    BEAK_COLOR       = (230, 95, 30)
    HEAD_COLOR       = (240, 238, 235)  # white face
    ACCENT_COLOR     = (230, 95, 30)


class Vulture(Bird):
    SPECIES          = "vulture"
    RARITY           = "uncommon"
    BIOMES           = ["desert", "canyon", "wasteland", "arid_steppe"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 3)
    ALTITUDE_BLOCKS  = (8, 16)
    SPEED            = 55.0
    W, H             = 24, 14
    BODY_COLOR       = (60, 50, 40)
    WING_COLOR       = (45, 38, 30)
    BEAK_COLOR       = (175, 50, 30)
    HEAD_COLOR       = (195, 155, 125)  # bare skin
    ACCENT_COLOR     = (175, 50, 30)


class Roadrunner(GroundBird):
    SPECIES          = "roadrunner"
    RARITY           = "uncommon"
    BIOMES           = ["desert", "arid_steppe", "canyon", "scrubland"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    SPEED            = 115.0
    W, H             = 22, 11
    BODY_COLOR       = (95, 80, 55)
    WING_COLOR       = (75, 62, 42)
    BEAK_COLOR       = (65, 48, 28)
    HEAD_COLOR       = (85, 72, 50)
    ACCENT_COLOR     = (185, 75, 35)    # orange-red eye patch
    PERSONALITY      = "bold"


class Peacock(GroundBird):
    SPECIES          = "peacock"
    RARITY           = "rare"
    BIOMES           = ["tropical", "savanna"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    SPEED            = 55.0
    PERSONALITY      = "normal"
    W, H             = 20, 14
    BODY_COLOR       = (30, 120, 165)
    WING_COLOR       = (25, 100, 145)
    BEAK_COLOR       = (165, 145, 100)
    HEAD_COLOR       = (30, 120, 165)
    ACCENT_COLOR     = (80, 195, 65)    # green tail


class Kookaburra(Bird):
    SPECIES          = "kookaburra"
    RARITY           = "uncommon"
    BIOMES           = ["savanna", "tropical"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 65.0
    W, H             = 16, 12
    BODY_COLOR       = (220, 190, 140)
    WING_COLOR       = (100, 80, 50)
    BEAK_COLOR       = (100, 80, 50)
    HEAD_COLOR       = (240, 230, 210)
    ACCENT_COLOR     = (60, 130, 200)   # blue wing-bar


class Sandpiper(Bird):
    SPECIES          = "sandpiper"
    RARITY           = "common"
    BIOMES           = ["beach", "wetland"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (3, 6)
    ALTITUDE_BLOCKS  = (1, 3)
    SPEED            = 70.0
    W, H             = 12, 8
    BODY_COLOR       = (165, 145, 110)
    WING_COLOR       = (145, 125, 95)
    BEAK_COLOR       = (45, 40, 35)
    HEAD_COLOR       = (165, 145, 110)
    ACCENT_COLOR     = (245, 230, 200)  # pale belly


class Kingfisher(Bird):
    SPECIES          = "kingfisher"
    RARITY           = "uncommon"
    BIOMES           = ["wetland", "swamp", "beach", "temperate"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 5)
    SPEED            = 90.0
    W, H             = 14, 10
    BODY_COLOR       = (40, 80, 205)
    WING_COLOR       = (30, 65, 180)
    BEAK_COLOR       = (50, 42, 38)
    HEAD_COLOR       = (40, 80, 205)
    ACCENT_COLOR     = (220, 130, 50)   # orange breast


class Woodpecker(Bird):
    SPECIES          = "woodpecker"
    RARITY           = "uncommon"
    BIOMES           = ["redwood", "boreal", "birch_forest", "temperate"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 7)
    SPEED            = 60.0
    W, H             = 14, 14
    BODY_COLOR       = (30, 28, 30)
    WING_COLOR       = (30, 28, 30)
    BEAK_COLOR       = (200, 190, 158)
    HEAD_COLOR       = (200, 30, 30)    # red crown
    ACCENT_COLOR     = (235, 232, 228)  # white cheek


class Finch(Bird):
    SPECIES          = "finch"
    RARITY           = "common"
    BIOMES           = ["temperate", "rolling_hills", "steep_hills", "steppe", "savanna"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (3, 8)
    ALTITUDE_BLOCKS  = (2, 5)
    SPEED            = 65.0
    W, H             = 10, 8
    BODY_COLOR       = (230, 190, 50)
    WING_COLOR       = (160, 130, 30)
    BEAK_COLOR       = (180, 145, 60)
    HEAD_COLOR       = (230, 190, 50)
    ACCENT_COLOR     = (240, 210, 80)


class Stork(Bird):
    SPECIES          = "stork"
    RARITY           = "uncommon"
    BIOMES           = ["wetland", "swamp"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 5)
    SPEED            = 50.0
    W, H             = 14, 22
    BODY_COLOR       = (238, 238, 238)
    WING_COLOR       = (28, 26, 26)     # black wingtips
    BEAK_COLOR       = (215, 90, 40)
    HEAD_COLOR       = (238, 238, 238)
    ACCENT_COLOR     = (215, 90, 40)


class Macaw(Bird):
    SPECIES          = "macaw"
    RARITY           = "rare"
    BIOMES           = ["jungle", "tropical"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 3)
    ALTITUDE_BLOCKS  = (3, 9)
    SPEED            = 80.0
    W, H             = 18, 14
    BODY_COLOR       = (200, 30, 40)    # scarlet red body
    WING_COLOR       = (40, 100, 220)   # blue wings
    BEAK_COLOR       = (48, 43, 38)
    HEAD_COLOR       = (240, 220, 50)   # yellow face
    ACCENT_COLOR     = (40, 160, 60)    # green neck


class Pheasant(GroundBird):
    SPECIES          = "pheasant"
    RARITY           = "uncommon"
    BIOMES           = ["temperate", "birch_forest", "boreal", "rolling_hills"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    SPEED            = 55.0
    PERSONALITY      = "timid"
    W, H             = 18, 10
    BODY_COLOR       = (180, 100, 30)
    WING_COLOR       = (155, 85, 25)
    BEAK_COLOR       = (160, 140, 90)
    HEAD_COLOR       = (30, 80, 40)     # dark green head
    ACCENT_COLOR     = (220, 60, 40)    # red wattle


class Condor(Bird):
    SPECIES          = "condor"
    RARITY           = "rare"
    BIOMES           = ["alpine_mountain", "rocky_mountain", "canyon", "redwood"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (10, 20)
    SPEED            = 85.0
    W, H             = 28, 16
    BODY_COLOR       = (28, 26, 28)
    WING_COLOR       = (24, 22, 24)
    BEAK_COLOR       = (185, 160, 140)
    HEAD_COLOR       = (210, 140, 90)   # bare orange
    ACCENT_COLOR     = (240, 232, 228)  # white collar ruff


class SnowBunting(Bird):
    SPECIES          = "snow_bunting"
    RARITY           = "common"
    BIOMES           = ["tundra", "alpine_mountain"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (4, 8)
    ALTITUDE_BLOCKS  = (2, 5)
    SPEED            = 60.0
    W, H             = 10, 8
    BODY_COLOR       = (242, 242, 248)
    WING_COLOR       = (28, 26, 28)
    BEAK_COLOR       = (170, 162, 120)
    HEAD_COLOR       = (242, 242, 248)
    ACCENT_COLOR     = (205, 185, 145)


class PrairieFalcon(Bird):
    SPECIES          = "prairie_falcon"
    RARITY           = "uncommon"
    BIOMES           = ["steppe", "arid_steppe", "desert", "rocky_mountain"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (4, 10)
    SPEED            = 110.0
    W, H             = 18, 12
    BODY_COLOR       = (170, 140, 100)
    WING_COLOR       = (145, 115, 80)
    BEAK_COLOR       = (220, 200, 60)   # yellow cere
    HEAD_COLOR       = (170, 140, 100)
    ACCENT_COLOR     = (48, 42, 38)     # dark malar stripe


class Nightjar(Bird):
    SPECIES          = "nightjar"
    RARITY           = "uncommon"
    BIOMES           = ["savanna", "wasteland", "desert"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 5)
    SPEED            = 70.0
    W, H             = 16, 10
    BODY_COLOR       = (130, 115, 85)
    WING_COLOR       = (110, 100, 68)
    BEAK_COLOR       = (38, 36, 33)
    HEAD_COLOR       = (125, 110, 80)
    ACCENT_COLOR     = (220, 200, 150)  # pale throat bar


class Ibis(Bird):
    SPECIES          = "ibis"
    RARITY           = "uncommon"
    BIOMES           = ["wetland", "swamp", "tropical"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 4)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 55.0
    W, H             = 14, 18
    BODY_COLOR       = (230, 80, 60)    # scarlet ibis
    WING_COLOR       = (210, 65, 50)
    BEAK_COLOR       = (48, 43, 38)     # dark curved beak
    HEAD_COLOR       = (230, 80, 60)
    ACCENT_COLOR     = (255, 100, 70)


class Albatross(Bird):
    SPECIES          = "albatross"
    RARITY           = "rare"
    BIOMES           = ["beach"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (6, 14)
    SPEED            = 90.0
    W, H             = 28, 12
    BODY_COLOR       = (248, 248, 250)
    WING_COLOR       = (30, 28, 30)     # dark wingtips
    BEAK_COLOR       = (220, 195, 145)
    HEAD_COLOR       = (248, 248, 250)
    ACCENT_COLOR     = (200, 195, 175)


class Raven(Bird):
    SPECIES          = "raven"
    RARITY           = "uncommon"
    BIOMES           = ["boreal", "alpine_mountain", "tundra", "redwood", "wasteland"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (3, 9)
    SPEED            = 80.0
    W, H             = 18, 14
    BODY_COLOR       = (25, 22, 28)
    WING_COLOR       = (20, 18, 24)
    BEAK_COLOR       = (30, 28, 32)
    HEAD_COLOR       = (25, 22, 28)
    ACCENT_COLOR     = (55, 45, 65)     # purple iridescent sheen


class Swallow(Bird):
    SPECIES          = "swallow"
    RARITY           = "common"
    BIOMES           = ["temperate", "rolling_hills", "steep_hills"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (3, 6)
    ALTITUDE_BLOCKS  = (3, 7)
    SPEED            = 100.0
    W, H             = 14, 8
    BODY_COLOR       = (30, 50, 130)
    WING_COLOR       = (25, 42, 115)
    BEAK_COLOR       = (38, 36, 33)
    HEAD_COLOR       = (30, 50, 130)
    ACCENT_COLOR     = (220, 80, 50)    # rust-orange breast


class Crane(Bird):
    SPECIES          = "crane"
    RARITY           = "uncommon"
    BIOMES           = ["wetland", "steppe", "tundra"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 4)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 60.0
    W, H             = 16, 22
    BODY_COLOR       = (215, 215, 222)
    WING_COLOR       = (190, 190, 200)
    BEAK_COLOR       = (170, 160, 132)
    HEAD_COLOR       = (200, 30, 30)    # red crown cap
    ACCENT_COLOR     = (215, 215, 222)


class Spoonbill(Bird):
    SPECIES          = "spoonbill"
    RARITY           = "uncommon"
    BIOMES           = ["wetland", "tropical", "beach"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 5)
    SPEED            = 55.0
    W, H             = 16, 18
    BODY_COLOR       = (240, 170, 185)
    WING_COLOR       = (220, 148, 163)
    BEAK_COLOR       = (182, 162, 132)  # flat gray spoon-bill
    HEAD_COLOR       = (245, 212, 220)
    ACCENT_COLOR     = (255, 182, 62)   # yellow eye area


class PeregrineFalcon(Bird):
    SPECIES          = "peregrine_falcon"
    RARITY           = "rare"
    BIOMES           = ["alpine_mountain", "rocky_mountain", "canyon", "steep_hills"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (8, 16)
    SPEED            = 130.0
    W, H             = 18, 12
    BODY_COLOR       = (60, 75, 110)
    WING_COLOR       = (45, 60, 95)
    BEAK_COLOR       = (220, 200, 60)
    HEAD_COLOR       = (25, 28, 38)
    ACCENT_COLOR     = (240, 230, 210)  # pale underside


class BarnOwl(Bird):
    SPECIES          = "barn_owl"
    RARITY           = "uncommon"
    BIOMES           = ["temperate", "rolling_hills", "wasteland", "steppe"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (3, 8)
    SPEED            = 55.0
    W, H             = 18, 14
    BODY_COLOR       = (225, 205, 155)
    WING_COLOR       = (195, 180, 130)
    BEAK_COLOR       = (200, 185, 145)
    HEAD_COLOR       = (248, 245, 238)
    ACCENT_COLOR     = (165, 148, 108)


class Magpie(Bird):
    SPECIES          = "magpie"
    RARITY           = "common"
    BIOMES           = ["temperate", "birch_forest", "rolling_hills", "boreal"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 4)
    ALTITUDE_BLOCKS  = (3, 7)
    SPEED            = 75.0
    W, H             = 16, 12
    BODY_COLOR       = (22, 22, 28)
    WING_COLOR       = (40, 100, 200)
    BEAK_COLOR       = (22, 22, 28)
    HEAD_COLOR       = (22, 22, 28)
    ACCENT_COLOR     = (245, 245, 245)


class GoldenOriole(Bird):
    SPECIES          = "golden_oriole"
    RARITY           = "uncommon"
    BIOMES           = ["jungle", "tropical", "temperate"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (4, 9)
    SPEED            = 80.0
    W, H             = 16, 12
    BODY_COLOR       = (240, 210, 30)
    WING_COLOR       = (22, 22, 28)
    BEAK_COLOR       = (205, 90, 50)
    HEAD_COLOR       = (240, 210, 30)
    ACCENT_COLOR     = (22, 22, 28)


class Hoopoe(Bird):
    SPECIES          = "hoopoe"
    RARITY           = "uncommon"
    BIOMES           = ["savanna", "arid_steppe", "temperate", "desert"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 65.0
    W, H             = 16, 12
    BODY_COLOR       = (200, 130, 60)
    WING_COLOR       = (22, 22, 28)
    BEAK_COLOR       = (60, 55, 48)
    HEAD_COLOR       = (210, 140, 65)
    ACCENT_COLOR     = (240, 230, 200)


class Sunbird(Bird):
    SPECIES          = "sunbird"
    RARITY           = "rare"
    BIOMES           = ["jungle", "tropical"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 7)
    SPEED            = 120.0
    W, H             = 10, 8
    BODY_COLOR       = (30, 180, 100)
    WING_COLOR       = (22, 145, 80)
    BEAK_COLOR       = (22, 20, 22)
    HEAD_COLOR       = (80, 40, 180)
    ACCENT_COLOR     = (220, 60, 40)


class Ptarmigan(Bird):
    SPECIES          = "ptarmigan"
    RARITY           = "common"
    BIOMES           = ["tundra", "alpine_mountain"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (3, 6)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 55.0
    W, H             = 14, 10
    BODY_COLOR       = (245, 244, 242)
    WING_COLOR       = (232, 230, 225)
    BEAK_COLOR       = (50, 45, 40)
    HEAD_COLOR       = (245, 244, 242)
    ACCENT_COLOR     = (180, 22, 22)


class Bittern(Bird):
    SPECIES          = "bittern"
    RARITY           = "uncommon"
    BIOMES           = ["wetland", "swamp"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 45.0
    W, H             = 14, 18
    BODY_COLOR       = (165, 138, 85)
    WING_COLOR       = (145, 118, 72)
    BEAK_COLOR       = (200, 190, 130)
    HEAD_COLOR       = (145, 118, 72)
    ACCENT_COLOR     = (220, 200, 150)


class CedarWaxwing(Bird):
    SPECIES          = "cedar_waxwing"
    RARITY           = "uncommon"
    BIOMES           = ["boreal", "birch_forest", "temperate"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (3, 7)
    ALTITUDE_BLOCKS  = (3, 8)
    SPEED            = 70.0
    W, H             = 14, 10
    BODY_COLOR       = (165, 130, 90)
    WING_COLOR       = (90, 85, 100)
    BEAK_COLOR       = (38, 35, 32)
    HEAD_COLOR       = (175, 140, 95)
    ACCENT_COLOR     = (240, 210, 40)


class Mockingbird(Bird):
    SPECIES          = "mockingbird"
    RARITY           = "common"
    BIOMES           = ["temperate", "arid_steppe", "savanna", "rolling_hills"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 75.0
    W, H             = 14, 10
    BODY_COLOR       = (140, 140, 148)
    WING_COLOR       = (110, 110, 118)
    BEAK_COLOR       = (48, 44, 40)
    HEAD_COLOR       = (148, 148, 155)
    ACCENT_COLOR     = (235, 232, 228)


class Egret(Bird):
    SPECIES          = "egret"
    RARITY           = "uncommon"
    BIOMES           = ["wetland", "swamp", "beach", "tropical"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 4)
    ALTITUDE_BLOCKS  = (2, 5)
    SPEED            = 50.0
    W, H             = 14, 20
    BODY_COLOR       = (252, 252, 255)
    WING_COLOR       = (240, 240, 245)
    BEAK_COLOR       = (240, 220, 50)
    HEAD_COLOR       = (252, 252, 255)
    ACCENT_COLOR     = (240, 220, 50)


class ArcticTern(Bird):
    SPECIES          = "arctic_tern"
    RARITY           = "uncommon"
    BIOMES           = ["beach", "tundra"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (4, 8)
    ALTITUDE_BLOCKS  = (3, 9)
    SPEED            = 95.0
    W, H             = 16, 8
    BODY_COLOR       = (245, 245, 248)
    WING_COLOR       = (220, 222, 228)
    BEAK_COLOR       = (215, 50, 40)
    HEAD_COLOR       = (22, 22, 28)
    ACCENT_COLOR     = (215, 50, 40)


class Cormorant(Bird):
    SPECIES          = "cormorant"
    RARITY           = "common"
    BIOMES           = ["beach", "wetland", "swamp"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 5)
    ALTITUDE_BLOCKS  = (2, 7)
    SPEED            = 65.0
    W, H             = 18, 14
    BODY_COLOR       = (28, 30, 35)
    WING_COLOR       = (38, 42, 48)
    BEAK_COLOR       = (155, 130, 50)
    HEAD_COLOR       = (28, 30, 35)
    ACCENT_COLOR     = (155, 130, 50)


class Curlew(Bird):
    SPECIES          = "curlew"
    RARITY           = "uncommon"
    BIOMES           = ["wetland", "steppe", "tundra", "beach"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 5)
    SPEED            = 60.0
    W, H             = 16, 14
    BODY_COLOR       = (155, 128, 88)
    WING_COLOR       = (138, 112, 75)
    BEAK_COLOR       = (60, 55, 50)
    HEAD_COLOR       = (148, 122, 82)
    ACCENT_COLOR     = (215, 195, 150)


class Avocet(Bird):
    SPECIES          = "avocet"
    RARITY           = "uncommon"
    BIOMES           = ["wetland", "beach", "steppe"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 5)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 65.0
    W, H             = 16, 14
    BODY_COLOR       = (245, 242, 238)
    WING_COLOR       = (22, 22, 28)
    BEAK_COLOR       = (38, 34, 30)
    HEAD_COLOR       = (215, 140, 70)
    ACCENT_COLOR     = (22, 22, 28)


class Jacana(Bird):
    SPECIES          = "jacana"
    RARITY           = "uncommon"
    BIOMES           = ["wetland", "tropical", "swamp"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 3)
    SPEED            = 55.0
    W, H             = 14, 12
    BODY_COLOR       = (120, 65, 28)
    WING_COLOR       = (100, 52, 22)
    BEAK_COLOR       = (240, 220, 40)
    HEAD_COLOR       = (22, 22, 28)
    ACCENT_COLOR     = (240, 220, 40)


class Lyrebird(GroundBird):
    SPECIES          = "lyrebird"
    RARITY           = "rare"
    BIOMES           = ["jungle", "redwood"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    SPEED            = 50.0
    PERSONALITY      = "wary"
    W, H             = 18, 14
    BODY_COLOR       = (110, 80, 55)
    WING_COLOR       = (95, 68, 45)
    BEAK_COLOR       = (50, 45, 40)
    HEAD_COLOR       = (120, 88, 60)
    ACCENT_COLOR     = (185, 165, 120)


class BeeEater(Bird):
    SPECIES          = "bee_eater"
    RARITY           = "uncommon"
    BIOMES           = ["savanna", "tropical", "desert", "arid_steppe"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (3, 6)
    ALTITUDE_BLOCKS  = (3, 8)
    SPEED            = 85.0
    W, H             = 16, 10
    BODY_COLOR       = (50, 190, 130)
    WING_COLOR       = (40, 165, 110)
    BEAK_COLOR       = (28, 25, 22)
    HEAD_COLOR       = (240, 200, 40)
    ACCENT_COLOR     = (30, 100, 200)


class Roller(Bird):
    SPECIES          = "roller"
    RARITY           = "uncommon"
    BIOMES           = ["savanna", "arid_steppe", "desert"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (3, 8)
    SPEED            = 75.0
    W, H             = 16, 12
    BODY_COLOR       = (50, 140, 210)
    WING_COLOR       = (38, 100, 180)
    BEAK_COLOR       = (42, 38, 35)
    HEAD_COLOR       = (50, 150, 215)
    ACCENT_COLOR     = (28, 68, 155)


class Hornbill(Bird):
    SPECIES          = "hornbill"
    RARITY           = "uncommon"
    BIOMES           = ["jungle", "tropical"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (3, 8)
    SPEED            = 55.0
    W, H             = 22, 14
    BODY_COLOR       = (22, 22, 28)
    WING_COLOR       = (22, 22, 28)
    BEAK_COLOR       = (235, 145, 30)
    HEAD_COLOR       = (240, 238, 232)
    ACCENT_COLOR     = (235, 145, 30)


class Quetzal(Bird):
    SPECIES          = "quetzal"
    RARITY           = "rare"
    BIOMES           = ["jungle", "tropical"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (4, 10)
    SPEED            = 70.0
    W, H             = 16, 14
    BODY_COLOR       = (40, 185, 80)
    WING_COLOR       = (30, 160, 65)
    BEAK_COLOR       = (220, 200, 50)
    HEAD_COLOR       = (40, 190, 85)
    ACCENT_COLOR     = (210, 40, 50)


class SnowyOwl(Bird):
    SPECIES          = "snowy_owl"
    RARITY           = "rare"
    BIOMES           = ["tundra", "alpine_mountain"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (4, 10)
    SPEED            = 60.0
    W, H             = 20, 16
    BODY_COLOR       = (250, 250, 255)
    WING_COLOR       = (235, 238, 248)
    BEAK_COLOR       = (48, 44, 40)
    HEAD_COLOR       = (252, 252, 255)
    ACCENT_COLOR     = (200, 200, 210)


class Osprey(Bird):
    SPECIES          = "osprey"
    RARITY           = "uncommon"
    BIOMES           = ["beach", "wetland", "temperate", "boreal"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (5, 12)
    SPEED            = 95.0
    W, H             = 22, 14
    BODY_COLOR       = (55, 45, 35)
    WING_COLOR       = (45, 36, 28)
    BEAK_COLOR       = (38, 35, 32)
    HEAD_COLOR       = (245, 242, 238)
    ACCENT_COLOR     = (245, 242, 238)


class GoldenPheasant(GroundBird):
    SPECIES          = "golden_pheasant"
    RARITY           = "rare"
    BIOMES           = ["jungle", "tropical", "redwood"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    SPEED            = 60.0
    PERSONALITY      = "timid"
    W, H             = 20, 14
    BODY_COLOR       = (215, 40, 35)
    WING_COLOR       = (30, 85, 195)
    BEAK_COLOR       = (200, 185, 120)
    HEAD_COLOR       = (240, 210, 30)
    ACCENT_COLOR     = (235, 140, 25)


class Treecreeper(Bird):
    SPECIES          = "treecreeper"
    RARITY           = "common"
    BIOMES           = ["redwood", "boreal", "birch_forest", "temperate"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 55.0
    W, H             = 10, 8
    BODY_COLOR       = (130, 105, 72)
    WING_COLOR       = (110, 88, 58)
    BEAK_COLOR       = (48, 44, 38)
    HEAD_COLOR       = (118, 95, 65)
    ACCENT_COLOR     = (230, 218, 195)


class Wren(Bird):
    SPECIES          = "wren"
    RARITY           = "common"
    BIOMES           = ["boreal", "birch_forest", "temperate", "rocky_mountain"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 65.0
    W, H             = 9, 7
    BODY_COLOR       = (135, 100, 65)
    WING_COLOR       = (115, 85, 52)
    BEAK_COLOR       = (55, 50, 42)
    HEAD_COLOR       = (128, 95, 60)
    ACCENT_COLOR     = (195, 170, 120)


class Nuthatch(Bird):
    SPECIES          = "nuthatch"
    RARITY           = "common"
    BIOMES           = ["boreal", "birch_forest", "redwood", "temperate"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 60.0
    W, H             = 12, 8
    BODY_COLOR       = (80, 110, 160)
    WING_COLOR       = (60, 88, 135)
    BEAK_COLOR       = (55, 50, 44)
    HEAD_COLOR       = (70, 100, 150)
    ACCENT_COLOR     = (235, 185, 130)


class Gannet(Bird):
    SPECIES          = "gannet"
    RARITY           = "uncommon"
    BIOMES           = ["beach"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 4)
    ALTITUDE_BLOCKS  = (5, 14)
    SPEED            = 95.0
    W, H             = 24, 12
    BODY_COLOR       = (248, 248, 252)
    WING_COLOR       = (22, 22, 28)
    BEAK_COLOR       = (165, 175, 168)
    HEAD_COLOR       = (240, 220, 130)
    ACCENT_COLOR     = (100, 150, 195)


class Frigatebird(Bird):
    SPECIES          = "frigatebird"
    RARITY           = "uncommon"
    BIOMES           = ["beach", "tropical"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 4)
    ALTITUDE_BLOCKS  = (6, 14)
    SPEED            = 100.0
    W, H             = 28, 10
    BODY_COLOR       = (22, 20, 26)
    WING_COLOR       = (18, 16, 22)
    BEAK_COLOR       = (55, 50, 45)
    HEAD_COLOR       = (22, 20, 26)
    ACCENT_COLOR     = (210, 40, 35)


class NightHeron(Bird):
    SPECIES          = "night_heron"
    RARITY           = "uncommon"
    BIOMES           = ["wetland", "swamp", "tropical"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 50.0
    W, H             = 14, 16
    BODY_COLOR       = (195, 198, 205)
    WING_COLOR       = (175, 178, 188)
    BEAK_COLOR       = (35, 32, 28)
    HEAD_COLOR       = (22, 22, 28)
    ACCENT_COLOR     = (248, 245, 238)


class Lapwing(Bird):
    SPECIES          = "lapwing"
    RARITY           = "common"
    BIOMES           = ["rolling_hills", "steppe", "wetland", "temperate"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (3, 6)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 70.0
    W, H             = 16, 12
    BODY_COLOR       = (80, 105, 60)
    WING_COLOR       = (62, 85, 45)
    BEAK_COLOR       = (38, 35, 30)
    HEAD_COLOR       = (22, 22, 28)
    ACCENT_COLOR     = (235, 225, 200)


class Wheatear(Bird):
    SPECIES          = "wheatear"
    RARITY           = "common"
    BIOMES           = ["rocky_mountain", "steppe", "tundra", "arid_steppe"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 70.0
    W, H             = 12, 9
    BODY_COLOR       = (168, 148, 115)
    WING_COLOR       = (22, 22, 28)
    BEAK_COLOR       = (38, 35, 30)
    HEAD_COLOR       = (168, 148, 115)
    ACCENT_COLOR     = (245, 235, 215)


class Redstart(Bird):
    SPECIES          = "redstart"
    RARITY           = "uncommon"
    BIOMES           = ["boreal", "birch_forest", "temperate"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 70.0
    W, H             = 12, 9
    BODY_COLOR       = (50, 55, 80)
    WING_COLOR       = (40, 44, 68)
    BEAK_COLOR       = (38, 35, 30)
    HEAD_COLOR       = (22, 22, 28)
    ACCENT_COLOR     = (215, 90, 35)


class Warbler(Bird):
    SPECIES          = "warbler"
    RARITY           = "common"
    BIOMES           = ["wetland", "temperate", "boreal", "jungle"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 5)
    SPEED            = 65.0
    W, H             = 10, 8
    BODY_COLOR       = (115, 145, 70)
    WING_COLOR       = (95, 122, 55)
    BEAK_COLOR       = (42, 38, 32)
    HEAD_COLOR       = (105, 135, 62)
    ACCENT_COLOR     = (225, 215, 160)


class LongTailedTit(Bird):
    SPECIES          = "long_tailed_tit"
    RARITY           = "common"
    BIOMES           = ["temperate", "birch_forest", "boreal"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (4, 8)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 60.0
    W, H             = 10, 8
    BODY_COLOR       = (235, 215, 210)
    WING_COLOR       = (22, 22, 28)
    BEAK_COLOR       = (38, 35, 30)
    HEAD_COLOR       = (240, 235, 230)
    ACCENT_COLOR     = (210, 140, 140)


class Oystercatcher(Bird):
    SPECIES          = "oystercatcher"
    RARITY           = "uncommon"
    BIOMES           = ["beach", "wetland"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 4)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 70.0
    W, H             = 16, 12
    BODY_COLOR       = (22, 22, 28)
    WING_COLOR       = (22, 22, 28)
    BEAK_COLOR       = (230, 95, 30)
    HEAD_COLOR       = (22, 22, 28)
    ACCENT_COLOR     = (245, 242, 238)


class Kite(Bird):
    SPECIES          = "kite"
    RARITY           = "uncommon"
    BIOMES           = ["savanna", "wasteland", "rolling_hills", "temperate"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (5, 12)
    SPEED            = 90.0
    W, H             = 22, 12
    BODY_COLOR       = (185, 95, 40)
    WING_COLOR       = (160, 78, 32)
    BEAK_COLOR       = (210, 195, 60)
    HEAD_COLOR       = (215, 205, 180)
    ACCENT_COLOR     = (210, 195, 60)


class Harrier(Bird):
    SPECIES          = "harrier"
    RARITY           = "uncommon"
    BIOMES           = ["steppe", "wetland", "rolling_hills", "arid_steppe"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (3, 8)
    SPEED            = 80.0
    W, H             = 22, 12
    BODY_COLOR       = (155, 158, 168)
    WING_COLOR       = (130, 134, 148)
    BEAK_COLOR       = (38, 35, 32)
    HEAD_COLOR       = (155, 158, 168)
    ACCENT_COLOR     = (248, 245, 240)


class Snipe(Bird):
    SPECIES          = "snipe"
    RARITY           = "uncommon"
    BIOMES           = ["wetland", "swamp", "tundra"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 75.0
    W, H             = 14, 9
    BODY_COLOR       = (125, 100, 65)
    WING_COLOR       = (108, 85, 52)
    BEAK_COLOR       = (58, 52, 44)
    HEAD_COLOR       = (115, 92, 58)
    ACCENT_COLOR     = (215, 195, 148)


class Merlin(Bird):
    SPECIES          = "merlin"
    RARITY           = "uncommon"
    BIOMES           = ["tundra", "steppe", "boreal"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (4, 10)
    SPEED            = 105.0
    W, H             = 14, 10
    BODY_COLOR       = (72, 88, 128)
    WING_COLOR       = (58, 72, 112)
    BEAK_COLOR       = (200, 185, 60)
    HEAD_COLOR       = (72, 88, 128)
    ACCENT_COLOR     = (205, 155, 80)


class Goshawk(Bird):
    SPECIES          = "goshawk"
    RARITY           = "rare"
    BIOMES           = ["boreal", "redwood", "birch_forest"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (5, 12)
    SPEED            = 110.0
    W, H             = 22, 14
    BODY_COLOR       = (95, 105, 118)
    WING_COLOR       = (78, 88, 102)
    BEAK_COLOR       = (200, 185, 60)
    HEAD_COLOR       = (55, 60, 72)
    ACCENT_COLOR     = (232, 228, 218)


class Shoebill(Bird):
    SPECIES          = "shoebill"
    RARITY           = "rare"
    BIOMES           = ["wetland", "swamp"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 40.0
    W, H             = 16, 22
    BODY_COLOR       = (88, 100, 118)
    WING_COLOR       = (75, 88, 105)
    BEAK_COLOR       = (195, 175, 115)
    HEAD_COLOR       = (88, 100, 118)
    ACCENT_COLOR     = (240, 235, 200)


class Booby(Bird):
    SPECIES          = "booby"
    RARITY           = "uncommon"
    BIOMES           = ["beach", "tropical"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 4)
    ALTITUDE_BLOCKS  = (3, 9)
    SPEED            = 80.0
    W, H             = 20, 12
    BODY_COLOR       = (242, 240, 235)
    WING_COLOR       = (28, 26, 32)
    BEAK_COLOR       = (50, 155, 210)
    HEAD_COLOR       = (242, 240, 235)
    ACCENT_COLOR     = (50, 100, 200)


class Tropicbird(Bird):
    SPECIES          = "tropicbird"
    RARITY           = "rare"
    BIOMES           = ["beach", "tropical"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (5, 12)
    SPEED            = 85.0
    W, H             = 18, 10
    BODY_COLOR       = (250, 248, 252)
    WING_COLOR       = (22, 22, 28)
    BEAK_COLOR       = (220, 80, 30)
    HEAD_COLOR       = (250, 248, 252)
    ACCENT_COLOR     = (220, 80, 30)


class BrownNoddy(Bird):
    SPECIES          = "brown_noddy"
    RARITY           = "common"
    BIOMES           = ["beach", "pacific_island", "ocean"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (3, 7)
    ALTITUDE_BLOCKS  = (4, 10)
    SPEED            = 75.0
    W, H             = 18, 9
    BODY_COLOR       = (55, 45, 35)
    WING_COLOR       = (45, 38, 28)
    BEAK_COLOR       = (40, 35, 30)
    HEAD_COLOR       = (220, 215, 205)
    ACCENT_COLOR     = (200, 195, 185)


class WhiteTern(Bird):
    SPECIES          = "white_tern"
    RARITY           = "rare"
    BIOMES           = ["pacific_island", "beach"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (6, 14)
    SPEED            = 90.0
    W, H             = 16, 8
    BODY_COLOR       = (252, 252, 255)
    WING_COLOR       = (245, 248, 252)
    BEAK_COLOR       = (22, 22, 28)
    HEAD_COLOR       = (252, 252, 255)
    ACCENT_COLOR     = (200, 225, 240)


class PacificGoldenPlover(Bird):
    SPECIES          = "pacific_golden_plover"
    RARITY           = "uncommon"
    BIOMES           = ["pacific_island", "beach"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 5)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 55.0
    W, H             = 16, 10
    BODY_COLOR       = (60, 55, 35)
    WING_COLOR       = (45, 42, 28)
    BEAK_COLOR       = (35, 30, 25)
    HEAD_COLOR       = (245, 240, 195)
    ACCENT_COLOR     = (22, 22, 22)


class CommonMyna(Bird):
    SPECIES          = "common_myna"
    RARITY           = "common"
    BIOMES           = ["pacific_island", "tropical", "beach"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (3, 6)
    ALTITUDE_BLOCKS  = (2, 7)
    SPEED            = 65.0
    W, H             = 16, 10
    BODY_COLOR       = (55, 45, 40)
    WING_COLOR       = (40, 35, 30)
    BEAK_COLOR       = (215, 175, 40)
    HEAD_COLOR       = (30, 25, 22)
    ACCENT_COLOR     = (240, 190, 30)


class ReefHeron(Bird):
    SPECIES          = "reef_heron"
    RARITY           = "uncommon"
    BIOMES           = ["pacific_island", "beach", "ocean"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 5)
    SPEED            = 45.0
    W, H             = 18, 14
    BODY_COLOR       = (80, 95, 110)
    WING_COLOR       = (70, 85, 100)
    BEAK_COLOR       = (175, 155, 90)
    HEAD_COLOR       = (80, 95, 110)
    ACCENT_COLOR     = (245, 242, 235)


class Dunlin(Bird):
    SPECIES          = "dunlin"
    RARITY           = "common"
    BIOMES           = ["beach", "tundra", "wetland"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (5, 10)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 75.0
    W, H             = 10, 7
    BODY_COLOR       = (148, 128, 98)
    WING_COLOR       = (128, 110, 82)
    BEAK_COLOR       = (38, 35, 30)
    HEAD_COLOR       = (142, 122, 92)
    ACCENT_COLOR     = (22, 22, 28)


class Godwit(Bird):
    SPECIES          = "godwit"
    RARITY           = "uncommon"
    BIOMES           = ["wetland", "tundra", "beach"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 4)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 80.0
    W, H             = 18, 12
    BODY_COLOR       = (195, 130, 75)
    WING_COLOR       = (165, 108, 58)
    BEAK_COLOR       = (215, 170, 105)
    HEAD_COLOR       = (185, 120, 65)
    ACCENT_COLOR     = (240, 225, 190)


class Oxpecker(Bird):
    SPECIES          = "oxpecker"
    RARITY           = "uncommon"
    BIOMES           = ["savanna"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 5)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 65.0
    W, H             = 12, 9
    BODY_COLOR       = (120, 100, 68)
    WING_COLOR       = (105, 88, 58)
    BEAK_COLOR       = (215, 75, 30)
    HEAD_COLOR       = (112, 92, 62)
    ACCENT_COLOR     = (240, 210, 90)


class Dipper(Bird):
    SPECIES          = "dipper"
    RARITY           = "uncommon"
    BIOMES           = ["boreal", "alpine_mountain", "temperate"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 3)
    SPEED            = 60.0
    W, H             = 12, 9
    BODY_COLOR       = (52, 48, 55)
    WING_COLOR       = (42, 38, 45)
    BEAK_COLOR       = (48, 44, 40)
    HEAD_COLOR       = (95, 72, 50)
    ACCENT_COLOR     = (245, 245, 248)


class Skua(Bird):
    SPECIES          = "skua"
    RARITY           = "uncommon"
    BIOMES           = ["beach", "tundra"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (4, 10)
    SPEED            = 95.0
    W, H             = 22, 12
    BODY_COLOR       = (95, 80, 55)
    WING_COLOR       = (80, 68, 45)
    BEAK_COLOR       = (42, 38, 34)
    HEAD_COLOR       = (85, 72, 48)
    ACCENT_COLOR     = (215, 195, 145)


class Firecrest(Bird):
    SPECIES          = "firecrest"
    RARITY           = "uncommon"
    BIOMES           = ["boreal", "temperate", "birch_forest"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 65.0
    W, H             = 9, 7
    BODY_COLOR       = (92, 115, 65)
    WING_COLOR       = (75, 95, 52)
    BEAK_COLOR       = (38, 35, 30)
    HEAD_COLOR       = (95, 118, 68)
    ACCENT_COLOR     = (235, 130, 30)


class RedCrownedCrane(Bird):
    SPECIES          = "red_crowned_crane"
    RARITY           = "rare"
    BIOMES           = ["wetland", "steppe", "tundra"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 4)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 55.0
    W, H             = 18, 24
    BODY_COLOR       = (240, 238, 235)
    WING_COLOR       = (22, 22, 28)      # black secondary wings
    BEAK_COLOR       = (175, 168, 130)
    HEAD_COLOR       = (200, 25, 25)     # vivid red crown cap
    ACCENT_COLOR     = (240, 238, 235)


class MandarinDuck(Bird):
    SPECIES          = "mandarin_duck"
    RARITY           = "uncommon"
    BIOMES           = ["wetland", "swamp", "boreal"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 3)
    SPEED            = 50.0
    W, H             = 14, 12
    BODY_COLOR       = (210, 120, 40)    # copper-orange flanks
    WING_COLOR       = (40, 115, 145)    # teal sail feathers
    BEAK_COLOR       = (215, 90, 45)     # coral-red bill
    HEAD_COLOR       = (40, 150, 120)    # iridescent green crown
    ACCENT_COLOR     = (245, 242, 238)   # white cheek stripe


class ChineseMonal(Bird):
    SPECIES          = "chinese_monal"
    RARITY           = "rare"
    BIOMES           = ["alpine_mountain", "rocky_mountain"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 55.0
    W, H             = 20, 14
    BODY_COLOR       = (30, 140, 110)    # iridescent blue-green
    WING_COLOR       = (55, 35, 100)     # deep purple-black
    BEAK_COLOR       = (185, 168, 125)
    HEAD_COLOR       = (40, 160, 130)    # metallic turquoise
    ACCENT_COLOR     = (210, 85, 40)     # copper tail


class SilverPheasant(GroundBird):
    SPECIES          = "silver_pheasant"
    RARITY           = "uncommon"
    BIOMES           = ["jungle", "redwood", "boreal"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    SPEED            = 55.0
    PERSONALITY      = "wary"
    W, H             = 20, 14
    BODY_COLOR       = (238, 235, 232)   # silver-white
    WING_COLOR       = (28, 26, 30)      # black
    BEAK_COLOR       = (165, 152, 130)
    HEAD_COLOR       = (30, 26, 30)      # glossy black head
    ACCENT_COLOR     = (195, 45, 40)     # red facial wattle


class CrestedIbis(Bird):
    SPECIES          = "crested_ibis"
    RARITY           = "rare"
    BIOMES           = ["wetland", "steppe"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 50.0
    W, H             = 16, 18
    BODY_COLOR       = (242, 228, 220)   # pale white with rosy flush
    WING_COLOR       = (228, 195, 175)
    BEAK_COLOR       = (38, 34, 30)      # dark downcurved bill
    HEAD_COLOR       = (195, 45, 40)     # red facial skin
    ACCENT_COLOR     = (230, 180, 170)   # rosy wing flush


class ChinesePondHeron(Bird):
    SPECIES          = "chinese_pond_heron"
    RARITY           = "common"
    BIOMES           = ["wetland", "swamp", "beach"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 45.0
    W, H             = 12, 16
    BODY_COLOR       = (155, 120, 75)    # streaked brown mantle
    WING_COLOR       = (235, 230, 222)   # white wings (fold contrast)
    BEAK_COLOR       = (195, 175, 80)    # yellow bill
    HEAD_COLOR       = (140, 108, 65)
    ACCENT_COLOR     = (235, 230, 222)


class FairyPitta(Bird):
    SPECIES          = "fairy_pitta"
    RARITY           = "rare"
    BIOMES           = ["jungle", "tropical"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 75.0
    W, H             = 14, 12
    BODY_COLOR       = (50, 170, 80)     # vivid green back
    WING_COLOR       = (30, 100, 200)    # cobalt blue
    BEAK_COLOR       = (35, 32, 28)
    HEAD_COLOR       = (22, 22, 28)      # black crown
    ACCENT_COLOR     = (220, 50, 50)     # scarlet belly


class Hwamei(Bird):
    SPECIES          = "hwamei"
    RARITY           = "uncommon"
    BIOMES           = ["temperate", "birch_forest", "boreal", "jungle"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 70.0
    W, H             = 14, 10
    BODY_COLOR       = (155, 115, 72)    # warm brown
    WING_COLOR       = (130, 95, 58)
    BEAK_COLOR       = (195, 170, 70)    # yellowish bill
    HEAD_COLOR       = (145, 108, 65)
    ACCENT_COLOR     = (220, 195, 145)   # white eye-stripe / spectacles


class BlackDrongo(Bird):
    SPECIES          = "black_drongo"
    RARITY           = "common"
    BIOMES           = ["savanna", "tropical", "wetland", "temperate"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (3, 8)
    SPEED            = 85.0
    W, H             = 14, 10
    BODY_COLOR       = (22, 22, 30)      # glossy black
    WING_COLOR       = (18, 18, 26)
    BEAK_COLOR       = (40, 38, 42)
    HEAD_COLOR       = (22, 22, 30)
    ACCENT_COLOR     = (40, 40, 60)      # blue-black iridescent sheen


class RedBilledBlueMagpie(Bird):
    SPECIES          = "red_billed_blue_magpie"
    RARITY           = "uncommon"
    BIOMES           = ["temperate", "jungle", "boreal"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 4)
    ALTITUDE_BLOCKS  = (3, 8)
    SPEED            = 80.0
    W, H             = 18, 14
    BODY_COLOR       = (40, 120, 210)    # vivid azure blue
    WING_COLOR       = (30, 95, 180)
    BEAK_COLOR       = (215, 55, 35)     # bright red bill
    HEAD_COLOR       = (22, 22, 28)      # black hood
    ACCENT_COLOR     = (240, 238, 230)   # white nape / tail tip


class AfricanFishEagle(Bird):
    SPECIES          = "african_fish_eagle"
    RARITY           = "rare"
    BIOMES           = ["savanna", "wetland", "beach"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (6, 14)
    SPEED            = 95.0
    W, H             = 24, 14
    BODY_COLOR       = (90, 55, 25)     # dark brown
    WING_COLOR       = (75, 45, 20)
    BEAK_COLOR       = (235, 195, 50)   # yellow
    HEAD_COLOR       = (245, 245, 240)  # white
    ACCENT_COLOR     = (195, 60, 30)    # chestnut breast


class SecretaryBird(GroundBird):
    SPECIES          = "secretary_bird"
    RARITY           = "rare"
    BIOMES           = ["savanna", "steppe", "arid_steppe"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    SPEED            = 60.0
    PERSONALITY      = "bold"
    W, H             = 16, 24
    BODY_COLOR       = (165, 168, 175)  # grey
    WING_COLOR       = (30, 28, 32)     # black
    BEAK_COLOR       = (210, 180, 80)   # yellow-grey
    HEAD_COLOR       = (165, 168, 175)
    ACCENT_COLOR     = (220, 115, 40)   # orange facial skin


class MartialEagle(Bird):
    SPECIES          = "martial_eagle"
    RARITY           = "rare"
    BIOMES           = ["savanna", "arid_steppe", "canyon"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (7, 15)
    SPEED            = 105.0
    W, H             = 22, 14
    BODY_COLOR       = (245, 242, 238)  # white spotted underside
    WING_COLOR       = (60, 55, 48)     # dark brown
    BEAK_COLOR       = (200, 185, 130)  # pale grey
    HEAD_COLOR       = (65, 60, 52)     # dark brown head
    ACCENT_COLOR     = (60, 55, 48)     # spots same shade as wings


class MarabouStork(Bird):
    SPECIES          = "marabou_stork"
    RARITY           = "uncommon"
    BIOMES           = ["savanna", "wetland", "swamp"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 4)
    ALTITUDE_BLOCKS  = (2, 7)
    SPEED            = 55.0
    W, H             = 18, 24
    BODY_COLOR       = (242, 240, 238)  # white
    WING_COLOR       = (48, 46, 52)     # dark grey-black
    BEAK_COLOR       = (195, 182, 148)  # pale massive bill
    HEAD_COLOR       = (195, 135, 105)  # bare pinkish skin
    ACCENT_COLOR     = (210, 90, 75)    # throat pouch


class SuperbStarling(Bird):
    SPECIES          = "superb_starling"
    RARITY           = "common"
    BIOMES           = ["savanna"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (3, 7)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 75.0
    W, H             = 12, 9
    BODY_COLOR       = (195, 118, 45)   # rufous-orange belly
    WING_COLOR       = (28, 135, 90)    # iridescent green
    BEAK_COLOR       = (35, 32, 28)
    HEAD_COLOR       = (25, 80, 150)    # iridescent blue-green
    ACCENT_COLOR     = (245, 240, 235)  # white breast band


class CapeWeaver(Bird):
    SPECIES          = "cape_weaver"
    RARITY           = "common"
    BIOMES           = ["savanna", "rolling_hills", "wetland"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (4, 8)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 65.0
    W, H             = 12, 9
    BODY_COLOR       = (228, 192, 22)   # bright yellow
    WING_COLOR       = (72, 95, 38)     # olive green
    BEAK_COLOR       = (55, 48, 35)     # dark conical
    HEAD_COLOR       = (215, 180, 18)   # golden yellow
    ACCENT_COLOR     = (195, 48, 28)    # red eye ring


class Hamerkop(Bird):
    SPECIES          = "hamerkop"
    RARITY           = "uncommon"
    BIOMES           = ["wetland", "swamp", "savanna"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 55.0
    W, H             = 16, 14
    BODY_COLOR       = (120, 88, 58)    # brown
    WING_COLOR       = (105, 75, 48)    # darker brown
    BEAK_COLOR       = (55, 48, 38)
    HEAD_COLOR       = (115, 82, 52)    # brown
    ACCENT_COLOR     = (148, 108, 70)   # lighter brown crest


class AfricanGreyParrot(Bird):
    SPECIES          = "african_grey_parrot"
    RARITY           = "rare"
    BIOMES           = ["jungle", "tropical"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (3, 8)
    SPEED            = 75.0
    W, H             = 16, 12
    BODY_COLOR       = (148, 148, 155)  # grey
    WING_COLOR       = (125, 125, 132)  # darker grey
    BEAK_COLOR       = (38, 36, 38)     # black hooked
    HEAD_COLOR       = (155, 155, 162)  # slightly lighter grey
    ACCENT_COLOR     = (210, 38, 35)    # bright red tail


class GroundHornbill(GroundBird):
    SPECIES          = "ground_hornbill"
    RARITY           = "rare"
    BIOMES           = ["savanna"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    SPEED            = 50.0
    PERSONALITY      = "bold"
    W, H             = 24, 16
    BODY_COLOR       = (25, 22, 28)     # black
    WING_COLOR       = (240, 238, 235)  # white wing patches (in flight)
    BEAK_COLOR       = (28, 25, 28)     # black massive casqued bill
    HEAD_COLOR       = (200, 45, 40)    # red facial skin
    ACCENT_COLOR     = (200, 45, 40)    # red throat wattle


class AfricanPenguin(GroundBird):
    SPECIES          = "african_penguin"
    RARITY           = "uncommon"
    BIOMES           = ["beach"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 5)
    SPEED            = 45.0
    PERSONALITY      = "curious"
    W, H             = 12, 14
    BODY_COLOR       = (245, 242, 238)  # white
    WING_COLOR       = (28, 25, 32)     # black
    BEAK_COLOR       = (38, 35, 30)
    HEAD_COLOR       = (28, 25, 32)     # black
    ACCENT_COLOR     = (218, 148, 132)  # pink cheek patches


# ======================================================================
# African species (100)
# ======================================================================

class LilacBreastedRoller(Bird):
    SPECIES          = "lilac_breasted_roller"
    RARITY           = "uncommon"
    BIOMES           = ["savanna", "rolling_hills"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (3, 8)
    SPEED            = 70.0
    W, H             = 16, 10
    BODY_COLOR       = (130, 100, 185)
    WING_COLOR       = (50, 120, 185)
    BEAK_COLOR       = (72, 58, 40)
    HEAD_COLOR       = (60, 165, 90)
    ACCENT_COLOR     = (185, 145, 215)


class CarmineBeeEater(Bird):
    SPECIES          = "carmine_bee_eater"
    RARITY           = "common"
    BIOMES           = ["savanna", "wetland"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 6)
    ALTITUDE_BLOCKS  = (3, 9)
    SPEED            = 80.0
    W, H             = 18, 10
    BODY_COLOR       = (210, 55, 80)
    WING_COLOR       = (38, 148, 110)
    BEAK_COLOR       = (35, 30, 25)
    HEAD_COLOR       = (210, 55, 80)
    ACCENT_COLOR     = (35, 30, 25)


class WhiteFrontedBeeEater(Bird):
    SPECIES          = "white_fronted_bee_eater"
    RARITY           = "uncommon"
    BIOMES           = ["canyon", "savanna"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 5)
    ALTITUDE_BLOCKS  = (3, 8)
    SPEED            = 75.0
    W, H             = 16, 10
    BODY_COLOR       = (195, 68, 55)
    WING_COLOR       = (52, 128, 72)
    BEAK_COLOR       = (35, 30, 25)
    HEAD_COLOR       = (245, 245, 240)
    ACCENT_COLOR     = (240, 210, 60)


class LittleBeeEater(Bird):
    SPECIES          = "little_bee_eater"
    RARITY           = "common"
    BIOMES           = ["savanna", "steppe"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 68.0
    W, H             = 12, 8
    BODY_COLOR       = (220, 180, 50)
    WING_COLOR       = (55, 130, 72)
    BEAK_COLOR       = (35, 30, 25)
    HEAD_COLOR       = (55, 130, 72)
    ACCENT_COLOR     = (30, 28, 22)


class AbyssinianRoller(Bird):
    SPECIES          = "abyssinian_roller"
    RARITY           = "uncommon"
    BIOMES           = ["savanna", "steppe"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (3, 8)
    SPEED            = 70.0
    W, H             = 16, 10
    BODY_COLOR       = (62, 120, 195)
    WING_COLOR       = (48, 85, 168)
    BEAK_COLOR       = (68, 55, 38)
    HEAD_COLOR       = (62, 120, 195)
    ACCENT_COLOR     = (105, 55, 145)


class MalachiteKingfisher(Bird):
    SPECIES          = "malachite_kingfisher"
    RARITY           = "uncommon"
    BIOMES           = ["wetland", "swamp"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 70.0
    W, H             = 10, 8
    BODY_COLOR       = (215, 120, 45)
    WING_COLOR       = (38, 158, 118)
    BEAK_COLOR       = (215, 80, 40)
    HEAD_COLOR       = (38, 158, 118)
    ACCENT_COLOR     = (245, 240, 235)


class GiantKingfisher(Bird):
    SPECIES          = "giant_kingfisher"
    RARITY           = "uncommon"
    BIOMES           = ["wetland", "beach"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 5)
    SPEED            = 65.0
    W, H             = 20, 12
    BODY_COLOR       = (185, 105, 55)
    WING_COLOR       = (55, 65, 72)
    BEAK_COLOR       = (55, 48, 38)
    HEAD_COLOR       = (55, 65, 72)
    ACCENT_COLOR     = (245, 240, 235)


class PygmyKingfisher(Bird):
    SPECIES          = "pygmy_kingfisher"
    RARITY           = "common"
    BIOMES           = ["jungle", "wetland"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 72.0
    W, H             = 10, 8
    BODY_COLOR       = (215, 110, 55)
    WING_COLOR       = (95, 62, 145)
    BEAK_COLOR       = (215, 80, 40)
    HEAD_COLOR       = (95, 62, 145)
    ACCENT_COLOR     = (245, 235, 210)


class PiedKingfisher(Bird):
    SPECIES          = "pied_kingfisher"
    RARITY           = "common"
    BIOMES           = ["wetland", "beach"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 5)
    SPEED            = 75.0
    W, H             = 16, 10
    BODY_COLOR       = (245, 242, 238)
    WING_COLOR       = (28, 25, 32)
    BEAK_COLOR       = (28, 22, 18)
    HEAD_COLOR       = (28, 25, 32)
    ACCENT_COLOR     = (245, 242, 238)


class GreyHeadedKingfisher(Bird):
    SPECIES          = "grey_headed_kingfisher"
    RARITY           = "common"
    BIOMES           = ["savanna", "wetland"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 68.0
    W, H             = 14, 10
    BODY_COLOR       = (195, 120, 50)
    WING_COLOR       = (45, 110, 185)
    BEAK_COLOR       = (215, 75, 40)
    HEAD_COLOR       = (148, 150, 155)
    ACCENT_COLOR     = (245, 240, 235)


class BateleurEagle(Bird):
    SPECIES          = "bateleur_eagle"
    RARITY           = "rare"
    BIOMES           = ["savanna"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (7, 16)
    SPEED            = 100.0
    W, H             = 30, 14
    BODY_COLOR       = (245, 242, 238)
    WING_COLOR       = (28, 25, 32)
    BEAK_COLOR       = (215, 58, 42)
    HEAD_COLOR       = (28, 25, 32)
    ACCENT_COLOR     = (215, 58, 42)


class TawnyEagle(Bird):
    SPECIES          = "tawny_eagle"
    RARITY           = "uncommon"
    BIOMES           = ["savanna", "steppe", "arid_steppe"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (6, 14)
    SPEED            = 90.0
    W, H             = 24, 14
    BODY_COLOR       = (175, 118, 50)
    WING_COLOR       = (140, 90, 38)
    BEAK_COLOR       = (205, 185, 110)
    HEAD_COLOR       = (185, 128, 55)
    ACCENT_COLOR     = (205, 185, 110)


class VerreauxsEagle(Bird):
    SPECIES          = "verreauxs_eagle"
    RARITY           = "rare"
    BIOMES           = ["rocky_mountain", "canyon"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (8, 18)
    SPEED            = 110.0
    W, H             = 30, 14
    BODY_COLOR       = (28, 25, 32)
    WING_COLOR       = (28, 25, 32)
    BEAK_COLOR       = (200, 185, 120)
    HEAD_COLOR       = (28, 25, 32)
    ACCENT_COLOR     = (245, 242, 238)


class BrownSnakeEagle(Bird):
    SPECIES          = "brown_snake_eagle"
    RARITY           = "uncommon"
    BIOMES           = ["savanna", "steppe"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (5, 12)
    SPEED            = 85.0
    W, H             = 22, 14
    BODY_COLOR       = (115, 88, 55)
    WING_COLOR       = (95, 72, 42)
    BEAK_COLOR       = (200, 185, 120)
    HEAD_COLOR       = (115, 88, 55)
    ACCENT_COLOR     = (245, 240, 218)


class LongCrestedEagle(Bird):
    SPECIES          = "long_crested_eagle"
    RARITY           = "uncommon"
    BIOMES           = ["wetland", "rolling_hills"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (4, 10)
    SPEED            = 80.0
    W, H             = 20, 12
    BODY_COLOR       = (245, 242, 238)
    WING_COLOR       = (48, 42, 52)
    BEAK_COLOR       = (215, 195, 130)
    HEAD_COLOR       = (48, 42, 52)
    ACCENT_COLOR     = (245, 242, 238)


class AfricanCrownedEagle(Bird):
    SPECIES          = "african_crowned_eagle"
    RARITY           = "rare"
    BIOMES           = ["jungle", "rolling_hills"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (5, 12)
    SPEED            = 95.0
    W, H             = 24, 14
    BODY_COLOR       = (215, 185, 140)
    WING_COLOR       = (65, 55, 48)
    BEAK_COLOR       = (195, 178, 115)
    HEAD_COLOR       = (65, 55, 48)
    ACCENT_COLOR     = (185, 138, 88)


class LannerFalcon(Bird):
    SPECIES          = "lanner_falcon"
    RARITY           = "uncommon"
    BIOMES           = ["savanna", "canyon", "desert"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (5, 12)
    SPEED            = 100.0
    W, H             = 18, 12
    BODY_COLOR       = (235, 225, 205)
    WING_COLOR       = (75, 68, 62)
    BEAK_COLOR       = (215, 195, 118)
    HEAD_COLOR       = (185, 115, 70)
    ACCENT_COLOR     = (215, 195, 118)


class PygmyFalcon(Bird):
    SPECIES          = "pygmy_falcon"
    RARITY           = "uncommon"
    BIOMES           = ["arid_steppe", "savanna"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (3, 8)
    SPEED            = 80.0
    W, H             = 10, 8
    BODY_COLOR       = (240, 235, 225)
    WING_COLOR       = (88, 80, 75)
    BEAK_COLOR       = (218, 195, 118)
    HEAD_COLOR       = (148, 148, 155)
    ACCENT_COLOR     = (200, 90, 68)


class AfricanKestrel(Bird):
    SPECIES          = "african_kestrel"
    RARITY           = "common"
    BIOMES           = ["savanna", "steppe", "rolling_hills"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (4, 10)
    SPEED            = 85.0
    W, H             = 16, 10
    BODY_COLOR       = (195, 145, 78)
    WING_COLOR       = (148, 100, 50)
    BEAK_COLOR       = (215, 195, 118)
    HEAD_COLOR       = (148, 148, 158)
    ACCENT_COLOR     = (215, 195, 118)


class RedNeckedFalcon(Bird):
    SPECIES          = "red_necked_falcon"
    RARITY           = "uncommon"
    BIOMES           = ["savanna", "tropical"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (4, 10)
    SPEED            = 95.0
    W, H             = 16, 10
    BODY_COLOR       = (218, 205, 185)
    WING_COLOR       = (68, 62, 58)
    BEAK_COLOR       = (215, 195, 118)
    HEAD_COLOR       = (195, 88, 55)
    ACCENT_COLOR     = (215, 195, 118)


class LappetFacedVulture(Bird):
    SPECIES          = "lappet_faced_vulture"
    RARITY           = "rare"
    BIOMES           = ["savanna", "desert"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (5, 14)
    SPEED            = 75.0
    W, H             = 32, 14
    BODY_COLOR       = (245, 240, 230)
    WING_COLOR       = (35, 30, 28)
    BEAK_COLOR       = (200, 182, 128)
    HEAD_COLOR       = (210, 90, 78)
    ACCENT_COLOR     = (210, 90, 78)


class WhiteBackedVulture(Bird):
    SPECIES          = "white_backed_vulture"
    RARITY           = "uncommon"
    BIOMES           = ["savanna"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 5)
    ALTITUDE_BLOCKS  = (5, 14)
    SPEED            = 72.0
    W, H             = 28, 14
    BODY_COLOR       = (185, 168, 140)
    WING_COLOR       = (38, 32, 28)
    BEAK_COLOR       = (200, 182, 125)
    HEAD_COLOR       = (215, 195, 165)
    ACCENT_COLOR     = (245, 242, 238)


class EgyptianVulture(Bird):
    SPECIES          = "egyptian_vulture"
    RARITY           = "uncommon"
    BIOMES           = ["desert", "savanna", "canyon"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (5, 12)
    SPEED            = 70.0
    W, H             = 22, 12
    BODY_COLOR       = (245, 242, 238)
    WING_COLOR       = (32, 28, 25)
    BEAK_COLOR       = (215, 175, 52)
    HEAD_COLOR       = (215, 175, 52)
    ACCENT_COLOR     = (245, 242, 238)


class PalmNutVulture(Bird):
    SPECIES          = "palm_nut_vulture"
    RARITY           = "uncommon"
    BIOMES           = ["tropical", "jungle", "beach"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (4, 10)
    SPEED            = 68.0
    W, H             = 22, 12
    BODY_COLOR       = (245, 242, 238)
    WING_COLOR       = (32, 28, 25)
    BEAK_COLOR       = (200, 182, 125)
    HEAD_COLOR       = (245, 242, 238)
    ACCENT_COLOR     = (215, 90, 55)


class SaddlebilledStork(Bird):
    SPECIES          = "saddlebilled_stork"
    RARITY           = "rare"
    BIOMES           = ["wetland", "savanna"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 8)
    SPEED            = 55.0
    W, H             = 20, 28
    BODY_COLOR       = (245, 242, 238)
    WING_COLOR       = (28, 25, 32)
    BEAK_COLOR       = (215, 55, 42)
    HEAD_COLOR       = (245, 242, 238)
    ACCENT_COLOR     = (240, 210, 55)


class YellowBilledStork(Bird):
    SPECIES          = "yellow_billed_stork"
    RARITY           = "common"
    BIOMES           = ["wetland", "savanna"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 5)
    ALTITUDE_BLOCKS  = (2, 7)
    SPEED            = 55.0
    W, H             = 18, 24
    BODY_COLOR       = (245, 205, 195)
    WING_COLOR       = (28, 25, 32)
    BEAK_COLOR       = (240, 185, 45)
    HEAD_COLOR       = (215, 80, 58)
    ACCENT_COLOR     = (240, 185, 45)


class GoliathHeron(Bird):
    SPECIES          = "goliath_heron"
    RARITY           = "rare"
    BIOMES           = ["wetland", "beach"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 5)
    SPEED            = 50.0
    W, H             = 20, 30
    BODY_COLOR       = (145, 148, 158)
    WING_COLOR       = (118, 122, 132)
    BEAK_COLOR       = (58, 50, 38)
    HEAD_COLOR       = (145, 62, 62)
    ACCENT_COLOR     = (245, 240, 225)


class PurpleHeron(Bird):
    SPECIES          = "purple_heron"
    RARITY           = "uncommon"
    BIOMES           = ["wetland", "swamp"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 5)
    SPEED            = 52.0
    W, H             = 16, 26
    BODY_COLOR       = (105, 72, 128)
    WING_COLOR       = (85, 78, 92)
    BEAK_COLOR       = (195, 162, 72)
    HEAD_COLOR       = (28, 22, 38)
    ACCENT_COLOR     = (175, 128, 68)


class BlackHeadedHeron(Bird):
    SPECIES          = "black_headed_heron"
    RARITY           = "common"
    BIOMES           = ["savanna", "rolling_hills"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 5)
    SPEED            = 52.0
    W, H             = 18, 26
    BODY_COLOR       = (148, 150, 158)
    WING_COLOR       = (118, 120, 128)
    BEAK_COLOR       = (55, 48, 35)
    HEAD_COLOR       = (28, 25, 32)
    ACCENT_COLOR     = (245, 242, 238)


class GreatEgret(Bird):
    SPECIES          = "great_egret"
    RARITY           = "common"
    BIOMES           = ["wetland", "beach"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 4)
    ALTITUDE_BLOCKS  = (1, 5)
    SPEED            = 52.0
    W, H             = 18, 24
    BODY_COLOR       = (248, 246, 244)
    WING_COLOR       = (242, 240, 238)
    BEAK_COLOR       = (218, 185, 55)
    HEAD_COLOR       = (248, 246, 244)
    ACCENT_COLOR     = (218, 185, 55)


class CattleEgret(Bird):
    SPECIES          = "cattle_egret"
    RARITY           = "common"
    BIOMES           = ["savanna", "rolling_hills"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (4, 10)
    ALTITUDE_BLOCKS  = (1, 5)
    SPEED            = 58.0
    W, H             = 14, 16
    BODY_COLOR       = (248, 246, 244)
    WING_COLOR       = (240, 238, 235)
    BEAK_COLOR       = (228, 180, 48)
    HEAD_COLOR       = (238, 195, 148)
    ACCENT_COLOR     = (238, 195, 148)


class SquaccoHeron(Bird):
    SPECIES          = "squacco_heron"
    RARITY           = "uncommon"
    BIOMES           = ["wetland", "swamp"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 50.0
    W, H             = 14, 16
    BODY_COLOR       = (218, 188, 140)
    WING_COLOR       = (248, 246, 244)
    BEAK_COLOR       = (95, 168, 88)
    HEAD_COLOR       = (218, 188, 140)
    ACCENT_COLOR     = (185, 152, 108)


class GreyCrownedCrane(Bird):
    SPECIES          = "grey_crowned_crane"
    RARITY           = "rare"
    BIOMES           = ["savanna", "wetland"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 7)
    SPEED            = 58.0
    W, H             = 20, 26
    BODY_COLOR       = (165, 168, 175)
    WING_COLOR       = (245, 242, 238)
    BEAK_COLOR       = (48, 42, 38)
    HEAD_COLOR       = (48, 42, 38)
    ACCENT_COLOR     = (228, 202, 50)


class HadedaIbis(Bird):
    SPECIES          = "hadeda_ibis"
    RARITY           = "common"
    BIOMES           = ["rolling_hills", "wetland"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 5)
    ALTITUDE_BLOCKS  = (2, 7)
    SPEED            = 60.0
    W, H             = 18, 14
    BODY_COLOR       = (105, 108, 100)
    WING_COLOR       = (62, 148, 95)
    BEAK_COLOR       = (145, 48, 38)
    HEAD_COLOR       = (108, 110, 105)
    ACCENT_COLOR     = (62, 148, 95)


class SacredIbis(Bird):
    SPECIES          = "sacred_ibis"
    RARITY           = "common"
    BIOMES           = ["wetland", "savanna", "beach"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (3, 7)
    ALTITUDE_BLOCKS  = (2, 7)
    SPEED            = 60.0
    W, H             = 18, 14
    BODY_COLOR       = (245, 242, 238)
    WING_COLOR       = (245, 242, 238)
    BEAK_COLOR       = (32, 28, 25)
    HEAD_COLOR       = (32, 28, 25)
    ACCENT_COLOR     = (32, 28, 25)


class GlossyIbis(Bird):
    SPECIES          = "glossy_ibis"
    RARITY           = "uncommon"
    BIOMES           = ["wetland", "savanna"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 5)
    ALTITUDE_BLOCKS  = (2, 7)
    SPEED            = 62.0
    W, H             = 16, 12
    BODY_COLOR       = (108, 62, 32)
    WING_COLOR       = (55, 118, 75)
    BEAK_COLOR       = (55, 48, 38)
    HEAD_COLOR       = (108, 62, 32)
    ACCENT_COLOR     = (72, 62, 148)


class AfricanSpoonbill(Bird):
    SPECIES          = "african_spoonbill"
    RARITY           = "uncommon"
    BIOMES           = ["wetland", "beach"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 4)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 58.0
    W, H             = 18, 14
    BODY_COLOR       = (248, 245, 242)
    WING_COLOR       = (242, 240, 238)
    BEAK_COLOR       = (215, 80, 62)
    HEAD_COLOR       = (215, 80, 62)
    ACCENT_COLOR     = (215, 80, 62)


class GreatWhitePelican(Bird):
    SPECIES          = "great_white_pelican"
    RARITY           = "uncommon"
    BIOMES           = ["wetland", "beach"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 5)
    ALTITUDE_BLOCKS  = (2, 8)
    SPEED            = 60.0
    W, H             = 26, 14
    BODY_COLOR       = (248, 245, 242)
    WING_COLOR       = (32, 28, 25)
    BEAK_COLOR       = (218, 178, 48)
    HEAD_COLOR       = (248, 245, 242)
    ACCENT_COLOR     = (218, 178, 48)


class AfricanDarter(Bird):
    SPECIES          = "african_darter"
    RARITY           = "uncommon"
    BIOMES           = ["wetland", "swamp"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 5)
    SPEED            = 60.0
    W, H             = 18, 14
    BODY_COLOR       = (65, 55, 42)
    WING_COLOR       = (48, 40, 32)
    BEAK_COLOR       = (185, 162, 85)
    HEAD_COLOR       = (80, 50, 32)
    ACCENT_COLOR     = (215, 185, 120)


class CrownedLapwing(Bird):
    SPECIES          = "crowned_lapwing"
    RARITY           = "common"
    BIOMES           = ["savanna", "steppe"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 65.0
    W, H             = 14, 10
    BODY_COLOR       = (165, 135, 78)
    WING_COLOR       = (58, 52, 45)
    BEAK_COLOR       = (225, 190, 52)
    HEAD_COLOR       = (28, 25, 32)
    ACCENT_COLOR     = (245, 242, 238)


class BlackwingedStilt(Bird):
    SPECIES          = "blackwinged_stilt"
    RARITY           = "common"
    BIOMES           = ["wetland", "beach"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 5)
    ALTITUDE_BLOCKS  = (1, 5)
    SPEED            = 65.0
    W, H             = 14, 16
    BODY_COLOR       = (245, 242, 238)
    WING_COLOR       = (28, 25, 32)
    BEAK_COLOR       = (32, 28, 25)
    HEAD_COLOR       = (245, 242, 238)
    ACCENT_COLOR     = (215, 68, 58)


class PurpleSwamphen(Bird):
    SPECIES          = "purple_swamphen"
    RARITY           = "uncommon"
    BIOMES           = ["wetland", "swamp"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 3)
    SPEED            = 55.0
    W, H             = 14, 12
    BODY_COLOR       = (88, 78, 155)
    WING_COLOR       = (72, 62, 128)
    BEAK_COLOR       = (215, 68, 52)
    HEAD_COLOR       = (88, 78, 155)
    ACCENT_COLOR     = (215, 68, 52)


class AfricanRail(Bird):
    SPECIES          = "african_rail"
    RARITY           = "uncommon"
    BIOMES           = ["wetland", "swamp"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 3)
    SPEED            = 52.0
    W, H             = 12, 10
    BODY_COLOR       = (105, 68, 38)
    WING_COLOR       = (88, 55, 30)
    BEAK_COLOR       = (215, 68, 52)
    HEAD_COLOR       = (68, 88, 118)
    ACCENT_COLOR     = (68, 88, 118)


class AfricanJacana(Bird):
    SPECIES          = "african_jacana"
    RARITY           = "common"
    BIOMES           = ["wetland", "swamp"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 3)
    SPEED            = 58.0
    W, H             = 12, 10
    BODY_COLOR       = (145, 88, 42)
    WING_COLOR       = (118, 68, 32)
    BEAK_COLOR       = (215, 195, 55)
    HEAD_COLOR       = (28, 25, 32)
    ACCENT_COLOR     = (215, 195, 55)


class RedBilledQuelea(Bird):
    SPECIES          = "red_billed_quelea"
    RARITY           = "common"
    BIOMES           = ["savanna", "steppe"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (8, 16)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 72.0
    W, H             = 10, 8
    BODY_COLOR       = (195, 162, 88)
    WING_COLOR       = (88, 72, 48)
    BEAK_COLOR       = (215, 55, 42)
    HEAD_COLOR       = (28, 25, 32)
    ACCENT_COLOR     = (215, 195, 138)


class VillageWeaver(Bird):
    SPECIES          = "village_weaver"
    RARITY           = "common"
    BIOMES           = ["savanna", "rolling_hills"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (3, 7)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 68.0
    W, H             = 12, 9
    BODY_COLOR       = (228, 192, 22)
    WING_COLOR       = (68, 88, 42)
    BEAK_COLOR       = (52, 45, 35)
    HEAD_COLOR       = (28, 25, 32)
    ACCENT_COLOR     = (228, 165, 22)


class GoldenBishop(Bird):
    SPECIES          = "golden_bishop"
    RARITY           = "uncommon"
    BIOMES           = ["wetland", "savanna"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 5)
    ALTITUDE_BLOCKS  = (2, 5)
    SPEED            = 65.0
    W, H             = 12, 9
    BODY_COLOR       = (228, 185, 22)
    WING_COLOR       = (32, 28, 25)
    BEAK_COLOR       = (52, 45, 35)
    HEAD_COLOR       = (228, 185, 22)
    ACCENT_COLOR     = (32, 28, 25)


class SouthernRedBishop(Bird):
    SPECIES          = "southern_red_bishop"
    RARITY           = "common"
    BIOMES           = ["wetland", "savanna"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (3, 7)
    ALTITUDE_BLOCKS  = (2, 5)
    SPEED            = 65.0
    W, H             = 12, 9
    BODY_COLOR       = (215, 58, 38)
    WING_COLOR       = (32, 28, 25)
    BEAK_COLOR       = (52, 45, 35)
    HEAD_COLOR       = (32, 28, 25)
    ACCENT_COLOR     = (215, 58, 38)


class WattledStarling(Bird):
    SPECIES          = "wattled_starling"
    RARITY           = "common"
    BIOMES           = ["savanna"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (4, 9)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 72.0
    W, H             = 14, 10
    BODY_COLOR       = (218, 215, 210)
    WING_COLOR       = (48, 45, 40)
    BEAK_COLOR       = (52, 45, 35)
    HEAD_COLOR       = (225, 195, 48)
    ACCENT_COLOR     = (28, 25, 22)


class MalachiteSunbird(Bird):
    SPECIES          = "malachite_sunbird"
    RARITY           = "uncommon"
    BIOMES           = ["rolling_hills", "alpine_mountain"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 72.0
    W, H             = 14, 10
    BODY_COLOR       = (38, 165, 88)
    WING_COLOR       = (28, 128, 68)
    BEAK_COLOR       = (32, 28, 22)
    HEAD_COLOR       = (38, 165, 88)
    ACCENT_COLOR     = (228, 185, 22)


class OrangeBreastSunbird(Bird):
    SPECIES          = "orange_breasted_sunbird"
    RARITY           = "uncommon"
    BIOMES           = ["mediterranean", "rolling_hills"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 70.0
    W, H             = 14, 10
    BODY_COLOR       = (215, 118, 38)
    WING_COLOR       = (35, 108, 72)
    BEAK_COLOR       = (32, 28, 22)
    HEAD_COLOR       = (35, 108, 72)
    ACCENT_COLOR     = (228, 215, 55)


class ScarletChestSunbird(Bird):
    SPECIES          = "scarlet_chested_sunbird"
    RARITY           = "common"
    BIOMES           = ["savanna", "tropical"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 70.0
    W, H             = 12, 9
    BODY_COLOR       = (215, 48, 38)
    WING_COLOR       = (28, 25, 22)
    BEAK_COLOR       = (32, 28, 22)
    HEAD_COLOR       = (28, 25, 22)
    ACCENT_COLOR     = (215, 48, 38)


class AmethystSunbird(Bird):
    SPECIES          = "amethyst_sunbird"
    RARITY           = "uncommon"
    BIOMES           = ["jungle", "tropical", "rolling_hills"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 70.0
    W, H             = 12, 9
    BODY_COLOR       = (28, 25, 32)
    WING_COLOR       = (28, 25, 32)
    BEAK_COLOR       = (32, 28, 22)
    HEAD_COLOR       = (158, 68, 175)
    ACCENT_COLOR     = (215, 48, 38)


class CollaredSunbird(Bird):
    SPECIES          = "collared_sunbird"
    RARITY           = "common"
    BIOMES           = ["jungle", "tropical"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 68.0
    W, H             = 11, 8
    BODY_COLOR       = (225, 205, 55)
    WING_COLOR       = (42, 125, 72)
    BEAK_COLOR       = (32, 28, 22)
    HEAD_COLOR       = (42, 125, 72)
    ACCENT_COLOR     = (98, 52, 148)


class VariableSunbird(Bird):
    SPECIES          = "variable_sunbird"
    RARITY           = "common"
    BIOMES           = ["jungle", "tropical", "savanna"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 68.0
    W, H             = 11, 8
    BODY_COLOR       = (225, 205, 55)
    WING_COLOR       = (35, 118, 68)
    BEAK_COLOR       = (32, 28, 22)
    HEAD_COLOR       = (35, 118, 68)
    ACCENT_COLOR     = (215, 78, 52)


class VioletBackedStarling(Bird):
    SPECIES          = "violet_backed_starling"
    RARITY           = "uncommon"
    BIOMES           = ["savanna", "jungle"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 5)
    ALTITUDE_BLOCKS  = (2, 7)
    SPEED            = 72.0
    W, H             = 12, 9
    BODY_COLOR       = (245, 242, 238)
    WING_COLOR       = (98, 72, 188)
    BEAK_COLOR       = (35, 30, 25)
    HEAD_COLOR       = (98, 72, 188)
    ACCENT_COLOR     = (245, 242, 238)


class GreaterBlueEaredStarling(Bird):
    SPECIES          = "greater_blue_eared_starling"
    RARITY           = "common"
    BIOMES           = ["savanna"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (3, 7)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 70.0
    W, H             = 14, 10
    BODY_COLOR       = (38, 158, 98)
    WING_COLOR       = (35, 108, 178)
    BEAK_COLOR       = (35, 30, 25)
    HEAD_COLOR       = (35, 108, 178)
    ACCENT_COLOR     = (215, 55, 148)


class PlumColoredStarling(Bird):
    SPECIES          = "plum_colored_starling"
    RARITY           = "uncommon"
    BIOMES           = ["jungle", "tropical"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 5)
    ALTITUDE_BLOCKS  = (2, 7)
    SPEED            = 70.0
    W, H             = 12, 9
    BODY_COLOR       = (245, 240, 235)
    WING_COLOR       = (128, 62, 145)
    BEAK_COLOR       = (35, 30, 25)
    HEAD_COLOR       = (128, 62, 145)
    ACCENT_COLOR     = (245, 240, 235)


class PiedStarling(Bird):
    SPECIES          = "pied_starling"
    RARITY           = "common"
    BIOMES           = ["rolling_hills", "savanna"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (3, 6)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 68.0
    W, H             = 12, 9
    BODY_COLOR       = (28, 25, 32)
    WING_COLOR       = (28, 25, 32)
    BEAK_COLOR       = (228, 192, 55)
    HEAD_COLOR       = (28, 25, 32)
    ACCENT_COLOR     = (245, 242, 238)


class BurchellsStarling(Bird):
    SPECIES          = "burchells_starling"
    RARITY           = "common"
    BIOMES           = ["savanna"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 5)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 70.0
    W, H             = 14, 10
    BODY_COLOR       = (58, 48, 128)
    WING_COLOR       = (48, 38, 108)
    BEAK_COLOR       = (35, 30, 25)
    HEAD_COLOR       = (68, 58, 148)
    ACCENT_COLOR     = (88, 78, 168)


class AfricanFirefinch(Bird):
    SPECIES          = "african_firefinch"
    RARITY           = "common"
    BIOMES           = ["savanna", "jungle"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 5)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 65.0
    W, H             = 10, 8
    BODY_COLOR       = (205, 55, 42)
    WING_COLOR       = (118, 42, 32)
    BEAK_COLOR       = (215, 72, 58)
    HEAD_COLOR       = (205, 55, 42)
    ACCENT_COLOR     = (245, 240, 230)


class BlueWaxbill(Bird):
    SPECIES          = "blue_waxbill"
    RARITY           = "common"
    BIOMES           = ["savanna", "steppe"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (3, 7)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 65.0
    W, H             = 10, 8
    BODY_COLOR       = (85, 145, 205)
    WING_COLOR       = (128, 88, 52)
    BEAK_COLOR       = (95, 148, 215)
    HEAD_COLOR       = (85, 145, 205)
    ACCENT_COLOR     = (245, 240, 230)


class VioletEaredWaxbill(Bird):
    SPECIES          = "violet_eared_waxbill"
    RARITY           = "uncommon"
    BIOMES           = ["arid_steppe", "steppe"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 5)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 65.0
    W, H             = 11, 8
    BODY_COLOR       = (145, 88, 52)
    WING_COLOR       = (118, 68, 38)
    BEAK_COLOR       = (215, 55, 128)
    HEAD_COLOR       = (115, 78, 168)
    ACCENT_COLOR     = (215, 55, 128)


class YellowFrontedCanary(Bird):
    SPECIES          = "yellow_fronted_canary"
    RARITY           = "common"
    BIOMES           = ["savanna", "rolling_hills"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 5)
    ALTITUDE_BLOCKS  = (2, 5)
    SPEED            = 65.0
    W, H             = 11, 8
    BODY_COLOR       = (222, 195, 55)
    WING_COLOR       = (85, 105, 55)
    BEAK_COLOR       = (52, 45, 35)
    HEAD_COLOR       = (218, 188, 42)
    ACCENT_COLOR     = (88, 145, 68)


class MelbaFinch(Bird):
    SPECIES          = "melba_finch"
    RARITY           = "uncommon"
    BIOMES           = ["savanna", "jungle"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 4)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 65.0
    W, H             = 12, 9
    BODY_COLOR       = (245, 240, 230)
    WING_COLOR       = (55, 115, 62)
    BEAK_COLOR       = (215, 52, 38)
    HEAD_COLOR       = (55, 115, 62)
    ACCENT_COLOR     = (215, 52, 38)


class AfricanSilverbill(Bird):
    SPECIES          = "african_silverbill"
    RARITY           = "common"
    BIOMES           = ["savanna", "arid_steppe"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (3, 7)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 65.0
    W, H             = 10, 8
    BODY_COLOR       = (198, 178, 148)
    WING_COLOR       = (128, 110, 88)
    BEAK_COLOR       = (178, 195, 215)
    HEAD_COLOR       = (168, 148, 118)
    ACCENT_COLOR     = (32, 28, 25)


class LocustFinch(Bird):
    SPECIES          = "locust_finch"
    RARITY           = "uncommon"
    BIOMES           = ["wetland", "savanna"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (3, 8)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 68.0
    W, H             = 10, 8
    BODY_COLOR       = (195, 72, 32)
    WING_COLOR       = (28, 25, 22)
    BEAK_COLOR       = (215, 55, 38)
    HEAD_COLOR       = (195, 72, 32)
    ACCENT_COLOR     = (245, 235, 215)


class DoubleToothBarbet(Bird):
    SPECIES          = "double_tooth_barbet"
    RARITY           = "uncommon"
    BIOMES           = ["jungle", "tropical"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 62.0
    W, H             = 14, 10
    BODY_COLOR       = (215, 55, 42)
    WING_COLOR       = (28, 25, 32)
    BEAK_COLOR       = (245, 205, 55)
    HEAD_COLOR       = (28, 25, 32)
    ACCENT_COLOR     = (245, 240, 230)


class BlackCollaredBarbet(Bird):
    SPECIES          = "black_collared_barbet"
    RARITY           = "common"
    BIOMES           = ["savanna", "rolling_hills"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 62.0
    W, H             = 14, 10
    BODY_COLOR       = (215, 55, 42)
    WING_COLOR       = (32, 28, 25)
    BEAK_COLOR       = (215, 55, 42)
    HEAD_COLOR       = (215, 55, 42)
    ACCENT_COLOR     = (32, 28, 25)


class RedYellowBarbet(Bird):
    SPECIES          = "red_yellow_barbet"
    RARITY           = "uncommon"
    BIOMES           = ["arid_steppe", "savanna"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 5)
    SPEED            = 60.0
    W, H             = 14, 10
    BODY_COLOR       = (218, 78, 45)
    WING_COLOR       = (32, 28, 25)
    BEAK_COLOR       = (245, 205, 55)
    HEAD_COLOR       = (218, 78, 45)
    ACCENT_COLOR     = (245, 205, 55)


class AfricanGreenPigeon(Bird):
    SPECIES          = "african_green_pigeon"
    RARITY           = "common"
    BIOMES           = ["jungle", "tropical"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 5)
    ALTITUDE_BLOCKS  = (3, 8)
    SPEED            = 65.0
    W, H             = 16, 12
    BODY_COLOR       = (95, 155, 68)
    WING_COLOR       = (72, 128, 52)
    BEAK_COLOR       = (215, 195, 55)
    HEAD_COLOR       = (88, 148, 62)
    ACCENT_COLOR     = (168, 145, 72)


class NamaquaDove(Bird):
    SPECIES          = "namaqua_dove"
    RARITY           = "common"
    BIOMES           = ["arid_steppe", "desert"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 5)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 62.0
    W, H             = 12, 9
    BODY_COLOR       = (195, 178, 148)
    WING_COLOR       = (138, 118, 88)
    BEAK_COLOR       = (215, 195, 55)
    HEAD_COLOR       = (168, 155, 128)
    ACCENT_COLOR     = (32, 28, 25)


class LaughingDove(Bird):
    SPECIES          = "laughing_dove"
    RARITY           = "common"
    BIOMES           = ["savanna", "arid_steppe"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 5)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 60.0
    W, H             = 12, 9
    BODY_COLOR       = (195, 148, 112)
    WING_COLOR       = (88, 118, 158)
    BEAK_COLOR       = (48, 42, 35)
    HEAD_COLOR       = (188, 142, 108)
    ACCENT_COLOR     = (155, 88, 62)


class MeyerParrot(Bird):
    SPECIES          = "meyer_parrot"
    RARITY           = "uncommon"
    BIOMES           = ["savanna", "jungle"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (3, 8)
    SPEED            = 68.0
    W, H             = 14, 12
    BODY_COLOR       = (72, 105, 88)
    WING_COLOR       = (55, 82, 68)
    BEAK_COLOR       = (38, 32, 28)
    HEAD_COLOR       = (88, 72, 55)
    ACCENT_COLOR     = (225, 188, 42)


class CapeParrot(Bird):
    SPECIES          = "cape_parrot"
    RARITY           = "rare"
    BIOMES           = ["rolling_hills", "jungle"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (3, 8)
    SPEED            = 68.0
    W, H             = 16, 14
    BODY_COLOR       = (82, 118, 82)
    WING_COLOR       = (62, 95, 62)
    BEAK_COLOR       = (38, 32, 28)
    HEAD_COLOR       = (215, 105, 48)
    ACCENT_COLOR     = (225, 188, 42)


class RosyFacedLovebird(Bird):
    SPECIES          = "rosy_faced_lovebird"
    RARITY           = "uncommon"
    BIOMES           = ["arid_steppe", "desert"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 6)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 68.0
    W, H             = 12, 10
    BODY_COLOR       = (72, 155, 88)
    WING_COLOR       = (55, 125, 72)
    BEAK_COLOR       = (215, 158, 78)
    HEAD_COLOR       = (215, 105, 90)
    ACCENT_COLOR     = (72, 118, 215)


class Ostrich(GroundBird):
    SPECIES          = "ostrich"
    RARITY           = "common"
    BIOMES           = ["savanna", "arid_steppe", "desert"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    SPEED            = 130.0
    PERSONALITY      = "bold"
    W, H             = 20, 32
    BODY_COLOR       = (28, 22, 28)
    WING_COLOR       = (245, 242, 238)
    BEAK_COLOR       = (215, 175, 118)
    HEAD_COLOR       = (215, 135, 108)
    ACCENT_COLOR     = (215, 135, 108)


class KoriBustard(GroundBird):
    SPECIES          = "kori_bustard"
    RARITY           = "uncommon"
    BIOMES           = ["savanna", "steppe"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    SPEED            = 52.0
    PERSONALITY      = "wary"
    W, H             = 22, 18
    BODY_COLOR       = (185, 165, 118)
    WING_COLOR       = (148, 130, 95)
    BEAK_COLOR       = (218, 195, 118)
    HEAD_COLOR       = (148, 148, 148)
    ACCENT_COLOR     = (32, 28, 25)


class HelmettedGuineafowl(GroundBird):
    SPECIES          = "helmeted_guineafowl"
    RARITY           = "common"
    BIOMES           = ["savanna", "rolling_hills"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (4, 10)
    SPEED            = 52.0
    PERSONALITY      = "wary"
    W, H             = 16, 14
    BODY_COLOR       = (58, 55, 62)
    WING_COLOR       = (48, 45, 52)
    BEAK_COLOR       = (215, 195, 118)
    HEAD_COLOR       = (85, 168, 188)
    ACCENT_COLOR     = (215, 52, 38)


class NamaquaSandgrouse(Bird):
    SPECIES          = "namaqua_sandgrouse"
    RARITY           = "uncommon"
    BIOMES           = ["desert", "arid_steppe"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (3, 7)
    ALTITUDE_BLOCKS  = (1, 5)
    SPEED            = 72.0
    W, H             = 14, 10
    BODY_COLOR       = (195, 168, 115)
    WING_COLOR       = (165, 138, 88)
    BEAK_COLOR       = (148, 128, 88)
    HEAD_COLOR       = (188, 148, 88)
    ACCENT_COLOR     = (32, 28, 25)


class FiscalShrike(Bird):
    SPECIES          = "fiscal_shrike"
    RARITY           = "common"
    BIOMES           = ["savanna", "rolling_hills"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 68.0
    W, H             = 14, 10
    BODY_COLOR       = (245, 242, 238)
    WING_COLOR       = (28, 25, 32)
    BEAK_COLOR       = (38, 32, 28)
    HEAD_COLOR       = (28, 25, 32)
    ACCENT_COLOR     = (245, 242, 238)


class RedBackedShrike(Bird):
    SPECIES          = "red_backed_shrike"
    RARITY           = "common"
    BIOMES           = ["savanna", "steppe"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 65.0
    W, H             = 14, 10
    BODY_COLOR       = (218, 195, 158)
    WING_COLOR       = (155, 88, 48)
    BEAK_COLOR       = (38, 32, 28)
    HEAD_COLOR       = (148, 148, 158)
    ACCENT_COLOR     = (32, 28, 25)


class PiedCrow(Bird):
    SPECIES          = "pied_crow"
    RARITY           = "common"
    BIOMES           = ["savanna", "rolling_hills", "wasteland"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 5)
    ALTITUDE_BLOCKS  = (3, 8)
    SPEED            = 72.0
    W, H             = 18, 12
    BODY_COLOR       = (245, 242, 238)
    WING_COLOR       = (28, 25, 32)
    BEAK_COLOR       = (38, 32, 28)
    HEAD_COLOR       = (28, 25, 32)
    ACCENT_COLOR     = (245, 242, 238)


class FanTailedRaven(Bird):
    SPECIES          = "fan_tailed_raven"
    RARITY           = "uncommon"
    BIOMES           = ["rocky_mountain", "canyon", "desert"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (4, 10)
    SPEED            = 75.0
    W, H             = 20, 14
    BODY_COLOR       = (28, 25, 32)
    WING_COLOR       = (28, 25, 32)
    BEAK_COLOR       = (38, 32, 28)
    HEAD_COLOR       = (28, 25, 32)
    ACCENT_COLOR     = (48, 45, 55)


class ParadiseFlycatcher(Bird):
    SPECIES          = "paradise_flycatcher"
    RARITY           = "uncommon"
    BIOMES           = ["jungle", "tropical", "rolling_hills"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (3, 7)
    SPEED            = 70.0
    W, H             = 16, 10
    BODY_COLOR       = (188, 95, 42)
    WING_COLOR       = (158, 72, 32)
    BEAK_COLOR       = (72, 108, 215)
    HEAD_COLOR       = (28, 25, 32)
    ACCENT_COLOR     = (188, 95, 42)


class Batis(Bird):
    SPECIES          = "batis"
    RARITY           = "common"
    BIOMES           = ["jungle", "savanna"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 65.0
    W, H             = 10, 8
    BODY_COLOR       = (245, 242, 238)
    WING_COLOR       = (48, 45, 52)
    BEAK_COLOR       = (38, 32, 28)
    HEAD_COLOR       = (48, 45, 52)
    ACCENT_COLOR     = (188, 112, 38)


class CapeRobinChat(Bird):
    SPECIES          = "cape_robin_chat"
    RARITY           = "common"
    BIOMES           = ["mediterranean", "rolling_hills"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 62.0
    W, H             = 12, 9
    BODY_COLOR       = (215, 128, 52)
    WING_COLOR       = (78, 82, 88)
    BEAK_COLOR       = (38, 32, 28)
    HEAD_COLOR       = (78, 82, 88)
    ACCENT_COLOR     = (215, 128, 52)


class AfricanStonechat(Bird):
    SPECIES          = "african_stonechat"
    RARITY           = "common"
    BIOMES           = ["rolling_hills", "steppe"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 62.0
    W, H             = 11, 8
    BODY_COLOR       = (205, 128, 65)
    WING_COLOR       = (32, 28, 25)
    BEAK_COLOR       = (32, 28, 25)
    HEAD_COLOR       = (32, 28, 25)
    ACCENT_COLOR     = (245, 242, 238)


class PennantWingedNightjar(Bird):
    SPECIES          = "pennant_winged_nightjar"
    RARITY           = "rare"
    BIOMES           = ["savanna"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 7)
    SPEED            = 65.0
    W, H             = 22, 10
    BODY_COLOR       = (128, 108, 78)
    WING_COLOR       = (95, 78, 55)
    BEAK_COLOR       = (88, 72, 52)
    HEAD_COLOR       = (118, 98, 68)
    ACCENT_COLOR     = (245, 242, 238)


class AlpineSwift(Bird):
    SPECIES          = "alpine_swift"
    RARITY           = "uncommon"
    BIOMES           = ["rocky_mountain", "canyon"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (3, 8)
    ALTITUDE_BLOCKS  = (6, 16)
    SPEED            = 110.0
    W, H             = 20, 8
    BODY_COLOR       = (55, 52, 58)
    WING_COLOR       = (48, 45, 52)
    BEAK_COLOR       = (38, 35, 32)
    HEAD_COLOR       = (55, 52, 58)
    ACCENT_COLOR     = (245, 242, 238)


class AfricanPalmSwift(Bird):
    SPECIES          = "african_palm_swift"
    RARITY           = "common"
    BIOMES           = ["savanna", "tropical"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (3, 8)
    ALTITUDE_BLOCKS  = (5, 14)
    SPEED            = 105.0
    W, H             = 18, 8
    BODY_COLOR       = (98, 88, 78)
    WING_COLOR       = (78, 70, 62)
    BEAK_COLOR       = (38, 35, 32)
    HEAD_COLOR       = (108, 98, 88)
    ACCENT_COLOR     = (218, 210, 195)


class RedKnobbedCoot(Bird):
    SPECIES          = "red_knobbed_coot"
    RARITY           = "common"
    BIOMES           = ["wetland"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 6)
    ALTITUDE_BLOCKS  = (1, 3)
    SPEED            = 52.0
    W, H             = 14, 12
    BODY_COLOR       = (52, 50, 58)
    WING_COLOR       = (42, 40, 48)
    BEAK_COLOR       = (245, 242, 238)
    HEAD_COLOR       = (52, 50, 58)
    ACCENT_COLOR     = (215, 55, 42)


class AfricanSnipe(Bird):
    SPECIES          = "african_snipe"
    RARITY           = "uncommon"
    BIOMES           = ["wetland", "swamp"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 65.0
    W, H             = 14, 10
    BODY_COLOR       = (128, 98, 62)
    WING_COLOR       = (95, 72, 45)
    BEAK_COLOR       = (148, 128, 88)
    HEAD_COLOR       = (118, 90, 55)
    ACCENT_COLOR     = (218, 195, 128)


class SpottedThickKnee(Bird):
    SPECIES          = "spotted_thick_knee"
    RARITY           = "uncommon"
    BIOMES           = ["savanna", "steppe"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 3)
    SPEED            = 55.0
    W, H             = 16, 12
    BODY_COLOR       = (178, 155, 108)
    WING_COLOR       = (148, 125, 85)
    BEAK_COLOR       = (215, 195, 55)
    HEAD_COLOR       = (178, 155, 108)
    ACCENT_COLOR     = (235, 220, 55)


class WattledPlover(Bird):
    SPECIES          = "wattled_plover"
    RARITY           = "common"
    BIOMES           = ["wetland", "savanna"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 62.0
    W, H             = 16, 14
    BODY_COLOR       = (155, 135, 88)
    WING_COLOR       = (28, 25, 32)
    BEAK_COLOR       = (215, 195, 55)
    HEAD_COLOR       = (245, 242, 238)
    ACCENT_COLOR     = (215, 195, 55)


class BlacksmithLapwing(Bird):
    SPECIES          = "blacksmith_lapwing"
    RARITY           = "common"
    BIOMES           = ["savanna", "wetland"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 65.0
    W, H             = 14, 10
    BODY_COLOR       = (148, 150, 155)
    WING_COLOR       = (28, 25, 32)
    BEAK_COLOR       = (38, 32, 28)
    HEAD_COLOR       = (245, 242, 238)
    ACCENT_COLOR     = (32, 28, 25)


class ThreeBandedPlover(Bird):
    SPECIES          = "three_banded_plover"
    RARITY           = "common"
    BIOMES           = ["wetland", "beach"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 62.0
    W, H             = 12, 9
    BODY_COLOR       = (158, 135, 95)
    WING_COLOR       = (128, 108, 75)
    BEAK_COLOR       = (215, 55, 42)
    HEAD_COLOR       = (32, 28, 25)
    ACCENT_COLOR     = (245, 242, 238)


class AfricanFishOwl(Bird):
    SPECIES          = "african_fish_owl"
    RARITY           = "rare"
    BIOMES           = ["wetland", "jungle"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 7)
    SPEED            = 55.0
    W, H             = 20, 18
    BODY_COLOR       = (195, 148, 78)
    WING_COLOR       = (148, 105, 52)
    BEAK_COLOR       = (218, 195, 118)
    HEAD_COLOR       = (195, 148, 78)
    ACCENT_COLOR     = (245, 240, 218)


class VerreauxsEagleOwl(Bird):
    SPECIES          = "verreauxs_eagle_owl"
    RARITY           = "rare"
    BIOMES           = ["savanna", "rocky_mountain"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 8)
    SPEED            = 55.0
    W, H             = 22, 18
    BODY_COLOR       = (185, 175, 168)
    WING_COLOR       = (145, 135, 128)
    BEAK_COLOR       = (218, 195, 118)
    HEAD_COLOR       = (185, 175, 168)
    ACCENT_COLOR     = (215, 135, 158)


class SpeckledMousebird(Bird):
    SPECIES          = "speckled_mousebird"
    RARITY           = "common"
    BIOMES           = ["savanna", "rolling_hills", "mediterranean"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (3, 7)
    ALTITUDE_BLOCKS  = (1, 5)
    SPEED            = 60.0
    W, H             = 14, 14
    BODY_COLOR       = (118, 105, 88)
    WING_COLOR       = (98, 85, 70)
    BEAK_COLOR       = (165, 148, 112)
    HEAD_COLOR       = (108, 95, 80)
    ACCENT_COLOR     = (245, 240, 225)


class GambelsQuail(GroundBird):
    SPECIES          = "gambels_quail"
    RARITY           = "uncommon"
    BIOMES           = ["desert", "scrubland", "arid_steppe", "chaparral"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (3, 8)
    SPEED            = 65.0
    W, H             = 13, 11
    BODY_COLOR       = (160, 130, 90)
    WING_COLOR       = (130, 105, 75)
    BEAK_COLOR       = (40, 28, 18)
    HEAD_COLOR       = (55, 40, 20)
    ACCENT_COLOR     = (210, 170, 55)   # topknot
    PERSONALITY      = "wary"


# ======================================================================
# Bats (nocturnal)
# ======================================================================

class LittleBrownBat(Bird):
    SPECIES          = "little_brown_bat"
    RARITY           = "common"
    BIOMES           = ["temperate", "boreal", "birch_forest"]
    NOCTURNAL        = True
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (3, 8)
    ALTITUDE_BLOCKS  = (2, 7)
    SPEED            = 80.0
    W, H             = 12, 6
    BODY_COLOR       = (95, 72, 45)
    WING_COLOR       = (62, 45, 28)
    BEAK_COLOR       = (38, 28, 18)
    HEAD_COLOR       = (95, 72, 45)
    ACCENT_COLOR     = (5, 5, 10)


class BigBrownBat(Bird):
    SPECIES          = "big_brown_bat"
    RARITY           = "uncommon"
    BIOMES           = ["temperate", "rolling_hills", "mediterranean"]
    NOCTURNAL        = True
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 7)
    SPEED            = 75.0
    W, H             = 16, 7
    BODY_COLOR       = (128, 95, 58)
    WING_COLOR       = (85, 62, 35)
    BEAK_COLOR       = (38, 28, 18)
    HEAD_COLOR       = (128, 95, 58)
    ACCENT_COLOR     = (5, 5, 10)


class FruitBat(Bird):
    SPECIES          = "fruit_bat"
    RARITY           = "common"
    BIOMES           = ["jungle", "tropical"]
    NOCTURNAL        = True
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (4, 10)
    ALTITUDE_BLOCKS  = (3, 8)
    SPEED            = 65.0
    W, H             = 18, 8
    BODY_COLOR       = (138, 85, 35)
    WING_COLOR       = (75, 48, 22)
    BEAK_COLOR       = (48, 32, 18)
    HEAD_COLOR       = (158, 98, 42)
    ACCENT_COLOR     = (5, 5, 10)


class VampireBat(Bird):
    SPECIES          = "vampire_bat"
    RARITY           = "rare"
    BIOMES           = ["jungle", "swamp"]
    NOCTURNAL        = True
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 5)
    SPEED            = 70.0
    W, H             = 13, 6
    BODY_COLOR       = (55, 35, 28)
    WING_COLOR       = (38, 22, 18)
    BEAK_COLOR       = (188, 35, 35)
    HEAD_COLOR       = (55, 35, 28)
    ACCENT_COLOR     = (245, 242, 238)


class HorseshoeBat(Bird):
    SPECIES          = "horseshoe_bat"
    RARITY           = "uncommon"
    BIOMES           = ["rocky_mountain", "canyon"]
    NOCTURNAL        = True
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 6)
    ALTITUDE_BLOCKS  = (1, 6)
    SPEED            = 60.0
    W, H             = 12, 6
    BODY_COLOR       = (105, 88, 78)
    WING_COLOR       = (72, 58, 48)
    BEAK_COLOR       = (38, 28, 18)
    HEAD_COLOR       = (105, 88, 78)
    ACCENT_COLOR     = (5, 5, 10)


class PipistrelBat(Bird):
    SPECIES          = "pipistrel_bat"
    RARITY           = "common"
    BIOMES           = ["temperate", "mediterranean", "south_asian"]
    NOCTURNAL        = True
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (3, 7)
    ALTITUDE_BLOCKS  = (2, 7)
    SPEED            = 85.0
    W, H             = 11, 5
    BODY_COLOR       = (72, 52, 32)
    WING_COLOR       = (45, 32, 18)
    BEAK_COLOR       = (38, 28, 18)
    HEAD_COLOR       = (72, 52, 32)
    ACCENT_COLOR     = (5, 5, 10)


class NoctuleBat(Bird):
    SPECIES          = "noctule_bat"
    RARITY           = "uncommon"
    BIOMES           = ["boreal", "temperate", "redwood"]
    NOCTURNAL        = True
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (3, 9)
    SPEED            = 90.0
    W, H             = 18, 7
    BODY_COLOR       = (185, 138, 62)
    WING_COLOR       = (128, 92, 38)
    BEAK_COLOR       = (48, 32, 18)
    HEAD_COLOR       = (185, 138, 62)
    ACCENT_COLOR     = (5, 5, 10)


class LeafNosedBat(Bird):
    SPECIES          = "leaf_nosed_bat"
    RARITY           = "uncommon"
    BIOMES           = ["desert", "arid_steppe", "canyon"]
    NOCTURNAL        = True
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 5)
    ALTITUDE_BLOCKS  = (1, 5)
    SPEED            = 65.0
    W, H             = 13, 6
    BODY_COLOR       = (148, 128, 105)
    WING_COLOR       = (108, 90, 72)
    BEAK_COLOR       = (78, 62, 45)
    HEAD_COLOR       = (148, 128, 105)
    ACCENT_COLOR     = (5, 5, 10)


class GhostBat(Bird):
    SPECIES          = "ghost_bat"
    RARITY           = "rare"
    BIOMES           = ["wasteland"]
    NOCTURNAL        = True
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 7)
    SPEED            = 70.0
    W, H             = 16, 7
    BODY_COLOR       = (228, 218, 208)
    WING_COLOR       = (195, 182, 168)
    BEAK_COLOR       = (155, 138, 122)
    HEAD_COLOR       = (228, 218, 208)
    ACCENT_COLOR     = (5, 5, 10)


class HammerHeadedBat(Bird):
    SPECIES          = "hammer_headed_bat"
    RARITY           = "rare"
    BIOMES           = ["savanna", "tropical"]
    NOCTURNAL        = True
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (3, 8)
    SPEED            = 60.0
    W, H             = 20, 9
    BODY_COLOR       = (88, 65, 42)
    WING_COLOR       = (58, 42, 25)
    BEAK_COLOR       = (48, 32, 18)
    HEAD_COLOR       = (88, 65, 42)
    ACCENT_COLOR     = (5, 5, 10)


# ======================================================================
# Nocturnal birds
# ======================================================================

class TawnyFrogmouth(Bird):
    SPECIES          = "tawny_frogmouth"
    RARITY           = "uncommon"
    BIOMES           = ["jungle", "east_asian", "south_asian"]
    NOCTURNAL        = True
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 52.0
    W, H             = 18, 12
    BODY_COLOR       = (145, 125, 98)
    WING_COLOR       = (118, 98, 72)
    BEAK_COLOR       = (78, 68, 48)
    HEAD_COLOR       = (135, 115, 88)
    ACCENT_COLOR     = (168, 148, 112)


class CommonPotoo(Bird):
    SPECIES          = "common_potoo"
    RARITY           = "rare"
    BIOMES           = ["jungle", "tropical"]
    NOCTURNAL        = True
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 58.0
    W, H             = 14, 10
    BODY_COLOR       = (148, 128, 95)
    WING_COLOR       = (118, 98, 68)
    BEAK_COLOR       = (58, 48, 38)
    HEAD_COLOR       = (138, 118, 85)
    ACCENT_COLOR     = (175, 155, 108)


class WhippoorWill(Bird):
    SPECIES          = "whip_poor_will"
    RARITY           = "common"
    BIOMES           = ["temperate", "boreal", "rolling_hills"]
    NOCTURNAL        = True
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 5)
    SPEED            = 72.0
    W, H             = 16, 8
    BODY_COLOR       = (138, 115, 78)
    WING_COLOR       = (108, 88, 58)
    BEAK_COLOR       = (38, 32, 25)
    HEAD_COLOR       = (128, 105, 68)
    ACCENT_COLOR     = (225, 198, 138)


class CommonPoorwill(Bird):
    SPECIES          = "common_poorwill"
    RARITY           = "common"
    BIOMES           = ["desert", "arid_steppe", "steppe"]
    NOCTURNAL        = True
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 68.0
    W, H             = 14, 7
    BODY_COLOR       = (128, 108, 72)
    WING_COLOR       = (98, 82, 52)
    BEAK_COLOR       = (38, 32, 25)
    HEAD_COLOR       = (118, 98, 62)
    ACCENT_COLOR     = (215, 188, 128)


class ElfOwl(Bird):
    SPECIES          = "elf_owl"
    RARITY           = "common"
    BIOMES           = ["desert", "canyon", "arid_steppe"]
    NOCTURNAL        = True
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 58.0
    W, H             = 10, 10
    BODY_COLOR       = (218, 185, 128)
    WING_COLOR       = (168, 138, 88)
    BEAK_COLOR       = (195, 162, 52)
    HEAD_COLOR       = (198, 168, 112)
    ACCENT_COLOR     = (235, 215, 168)


class BurrowingOwl(GroundBird):
    SPECIES          = "burrowing_owl"
    RARITY           = "uncommon"
    BIOMES           = ["steppe", "savanna", "arid_steppe"]
    NOCTURNAL        = True
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    SPEED            = 55.0
    W, H             = 10, 14
    BODY_COLOR       = (218, 188, 128)
    WING_COLOR       = (168, 142, 88)
    BEAK_COLOR       = (215, 185, 55)
    HEAD_COLOR       = (188, 158, 98)
    ACCENT_COLOR     = (245, 238, 218)
    PERSONALITY      = "bold"


class BarredOwl(Bird):
    SPECIES          = "barred_owl"
    RARITY           = "uncommon"
    BIOMES           = ["temperate", "boreal", "birch_forest"]
    NOCTURNAL        = True
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (3, 9)
    SPEED            = 52.0
    W, H             = 18, 20
    BODY_COLOR       = (178, 155, 115)
    WING_COLOR       = (138, 112, 78)
    BEAK_COLOR       = (218, 195, 115)
    HEAD_COLOR       = (168, 148, 108)
    ACCENT_COLOR     = (245, 240, 218)


class SpectacledOwl(Bird):
    SPECIES          = "spectacled_owl"
    RARITY           = "rare"
    BIOMES           = ["jungle", "tropical"]
    NOCTURNAL        = True
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (3, 9)
    SPEED            = 50.0
    W, H             = 18, 20
    BODY_COLOR       = (245, 240, 218)
    WING_COLOR       = (42, 38, 45)
    BEAK_COLOR       = (218, 195, 115)
    HEAD_COLOR       = (42, 38, 45)
    ACCENT_COLOR     = (245, 240, 218)


class LongEaredOwl(Bird):
    SPECIES          = "long_eared_owl"
    RARITY           = "uncommon"
    BIOMES           = ["boreal", "temperate", "steppe"]
    NOCTURNAL        = True
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (3, 9)
    SPEED            = 54.0
    W, H             = 16, 20
    BODY_COLOR       = (198, 152, 88)
    WING_COLOR       = (152, 112, 58)
    BEAK_COLOR       = (195, 162, 52)
    HEAD_COLOR       = (188, 142, 78)
    ACCENT_COLOR     = (215, 172, 105)


class ShortEaredOwl(Bird):
    SPECIES          = "short_eared_owl"
    RARITY           = "uncommon"
    BIOMES           = ["tundra", "steppe", "wetland"]
    NOCTURNAL        = True
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 6)
    SPEED            = 60.0
    W, H             = 18, 16
    BODY_COLOR       = (215, 182, 128)
    WING_COLOR       = (162, 132, 82)
    BEAK_COLOR       = (195, 162, 52)
    HEAD_COLOR       = (205, 172, 118)
    ACCENT_COLOR     = (228, 195, 138)


class FerruginousPygmyOwl(Bird):
    SPECIES          = "ferruginous_pygmy_owl"
    RARITY           = "common"
    BIOMES           = ["savanna", "tropical"]
    NOCTURNAL        = True
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 62.0
    W, H             = 10, 12
    BODY_COLOR       = (188, 115, 62)
    WING_COLOR       = (148, 88, 42)
    BEAK_COLOR       = (195, 162, 52)
    HEAD_COLOR       = (178, 105, 55)
    ACCENT_COLOR     = (228, 185, 128)


class Kiwi(GroundBird):
    SPECIES          = "kiwi"
    RARITY           = "rare"
    BIOMES           = ["jungle"]
    NOCTURNAL        = True
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    SPEED            = 45.0
    W, H             = 14, 12
    BODY_COLOR       = (118, 88, 55)
    WING_COLOR       = (98, 72, 42)
    BEAK_COLOR       = (178, 155, 112)
    HEAD_COLOR       = (108, 80, 48)
    ACCENT_COLOR     = (5, 5, 5)
    PERSONALITY      = "timid"


class NightParrot(GroundBird):
    SPECIES          = "night_parrot"
    RARITY           = "rare"
    BIOMES           = ["desert", "arid_steppe"]
    NOCTURNAL        = True
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    SPEED            = 52.0
    W, H             = 12, 10
    BODY_COLOR       = (88, 132, 58)
    WING_COLOR       = (62, 108, 38)
    BEAK_COLOR       = (128, 108, 38)
    HEAD_COLOR       = (72, 115, 45)
    ACCENT_COLOR     = (218, 205, 65)
    PERSONALITY      = "timid"


class CommonScopsOwl(Bird):
    SPECIES          = "common_scops_owl"
    RARITY           = "common"
    BIOMES           = ["mediterranean", "savanna", "east_asian"]
    NOCTURNAL        = True
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 7)
    SPEED            = 56.0
    W, H             = 14, 16
    BODY_COLOR       = (152, 140, 118)
    WING_COLOR       = (118, 108, 88)
    BEAK_COLOR       = (195, 172, 52)
    HEAD_COLOR       = (142, 130, 108)
    ACCENT_COLOR     = (168, 155, 128)


class EasternScreechOwl(Bird):
    SPECIES          = "eastern_screech_owl"
    RARITY           = "common"
    BIOMES           = ["temperate", "rolling_hills", "birch_forest"]
    NOCTURNAL        = True
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 7)
    SPEED            = 58.0
    W, H             = 12, 14
    BODY_COLOR       = (158, 148, 128)
    WING_COLOR       = (122, 112, 95)
    BEAK_COLOR       = (195, 172, 52)
    HEAD_COLOR       = (148, 138, 118)
    ACCENT_COLOR     = (222, 198, 152)


# ======================================================================
# Penguins (tundra / alpine ground birds)
# ======================================================================

class EmperorPenguin(GroundBird):
    SPECIES          = "emperor_penguin"
    RARITY           = "rare"
    BIOMES           = ["tundra", "alpine_mountain"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 5)
    SPEED            = 35.0
    W, H             = 16, 22
    BODY_COLOR       = (245, 242, 238)
    WING_COLOR       = (22, 22, 28)
    BEAK_COLOR       = (205, 155, 55)
    HEAD_COLOR       = (22, 22, 28)
    ACCENT_COLOR     = (235, 195, 85)
    PERSONALITY      = "curious"


class KingPenguin(GroundBird):
    SPECIES          = "king_penguin"
    RARITY           = "uncommon"
    BIOMES           = ["tundra", "alpine_mountain"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 5)
    SPEED            = 40.0
    W, H             = 14, 19
    BODY_COLOR       = (245, 242, 238)
    WING_COLOR       = (25, 22, 30)
    BEAK_COLOR       = (215, 145, 48)
    HEAD_COLOR       = (25, 22, 30)
    ACCENT_COLOR     = (225, 175, 65)
    PERSONALITY      = "curious"


class GentooPenguin(GroundBird):
    SPECIES          = "gentoo_penguin"
    RARITY           = "common"
    BIOMES           = ["tundra", "alpine_mountain"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (3, 7)
    SPEED            = 45.0
    W, H             = 13, 17
    BODY_COLOR       = (245, 242, 238)
    WING_COLOR       = (28, 25, 32)
    BEAK_COLOR       = (215, 105, 35)
    HEAD_COLOR       = (28, 25, 32)
    ACCENT_COLOR     = (245, 242, 238)
    PERSONALITY      = "curious"


class ChinStrapPenguin(GroundBird):
    SPECIES          = "chin_strap_penguin"
    RARITY           = "common"
    BIOMES           = ["tundra", "alpine_mountain"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (3, 8)
    SPEED            = 47.0
    W, H             = 12, 15
    BODY_COLOR       = (245, 242, 238)
    WING_COLOR       = (28, 25, 32)
    BEAK_COLOR       = (35, 30, 25)
    HEAD_COLOR       = (28, 25, 32)
    ACCENT_COLOR     = (245, 242, 238)
    PERSONALITY      = "bold"


class AdeliePenguin(GroundBird):
    SPECIES          = "adelie_penguin"
    RARITY           = "common"
    BIOMES           = ["tundra", "alpine_mountain"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (4, 9)
    SPEED            = 50.0
    W, H             = 11, 14
    BODY_COLOR       = (245, 242, 238)
    WING_COLOR       = (22, 20, 28)
    BEAK_COLOR       = (175, 80, 28)
    HEAD_COLOR       = (22, 20, 28)
    ACCENT_COLOR     = (245, 242, 238)
    PERSONALITY      = "bold"


class MacaroniPenguin(GroundBird):
    SPECIES          = "macaroni_penguin"
    RARITY           = "uncommon"
    BIOMES           = ["tundra", "alpine_mountain"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 6)
    SPEED            = 42.0
    W, H             = 12, 16
    BODY_COLOR       = (245, 242, 238)
    WING_COLOR       = (28, 25, 32)
    BEAK_COLOR       = (155, 88, 28)
    HEAD_COLOR       = (22, 20, 28)
    ACCENT_COLOR     = (235, 185, 28)
    PERSONALITY      = "curious"


class RockHopperPenguin(GroundBird):
    SPECIES          = "rock_hopper_penguin"
    RARITY           = "uncommon"
    BIOMES           = ["tundra", "alpine_mountain"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 6)
    SPEED            = 50.0
    W, H             = 11, 13
    BODY_COLOR       = (245, 242, 238)
    WING_COLOR       = (28, 25, 32)
    BEAK_COLOR       = (195, 88, 28)
    HEAD_COLOR       = (22, 20, 28)
    ACCENT_COLOR     = (235, 198, 22)
    PERSONALITY      = "bold"


class SnaresPenguin(GroundBird):
    SPECIES          = "snares_penguin"
    RARITY           = "uncommon"
    BIOMES           = ["tundra", "alpine_mountain"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 5)
    SPEED            = 45.0
    W, H             = 11, 14
    BODY_COLOR       = (245, 242, 238)
    WING_COLOR       = (25, 22, 30)
    BEAK_COLOR       = (35, 28, 22)
    HEAD_COLOR       = (25, 22, 30)
    ACCENT_COLOR     = (235, 195, 28)
    PERSONALITY      = "normal"


class FjordlandPenguin(GroundBird):
    SPECIES          = "fjordland_penguin"
    RARITY           = "uncommon"
    BIOMES           = ["tundra", "alpine_mountain"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 4)
    SPEED            = 47.0
    W, H             = 10, 13
    BODY_COLOR       = (245, 242, 238)
    WING_COLOR       = (28, 25, 35)
    BEAK_COLOR       = (42, 32, 22)
    HEAD_COLOR       = (28, 25, 35)
    ACCENT_COLOR     = (225, 182, 22)
    PERSONALITY      = "normal"


class LittleBluePenguin(GroundBird):
    SPECIES          = "little_blue_penguin"
    RARITY           = "common"
    BIOMES           = ["tundra", "beach"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (3, 7)
    SPEED            = 55.0
    W, H             = 9, 11
    BODY_COLOR       = (245, 242, 238)
    WING_COLOR       = (55, 78, 138)
    BEAK_COLOR       = (38, 32, 28)
    HEAD_COLOR       = (55, 78, 138)
    ACCENT_COLOR     = (245, 242, 238)
    PERSONALITY      = "curious"


# ======================================================================
# Registry
# ======================================================================

ALL_SPECIES = [
    Robin, BlueJay, Eagle, Pelican, Parrot, Sparrow, Heron, Hummingbird, Owl, Crow,
    Flamingo, Toucan, Cardinal, Puffin, Vulture, Roadrunner, Peacock, Kookaburra,
    Sandpiper, Kingfisher, Woodpecker, Finch, Stork, Macaw, Pheasant, Condor,
    SnowBunting, PrairieFalcon, Nightjar, Ibis, Albatross, Raven, Swallow, Crane,
    Spoonbill,
    PeregrineFalcon, BarnOwl, Magpie, GoldenOriole, Hoopoe, Sunbird, Ptarmigan,
    Bittern, CedarWaxwing, Mockingbird, Egret, ArcticTern, Cormorant, Curlew,
    Avocet, Jacana, Lyrebird, BeeEater, Roller, Hornbill, Quetzal, SnowyOwl,
    Osprey, GoldenPheasant, Treecreeper,
    Wren, Nuthatch, Gannet, Frigatebird, NightHeron, Lapwing, Wheatear, Redstart,
    Warbler, LongTailedTit, Oystercatcher, Kite, Harrier, Snipe, Merlin, Goshawk,
    Shoebill, Booby, Tropicbird, Dunlin, Godwit, Oxpecker, Dipper, Skua, Firecrest,
    BrownNoddy, WhiteTern, PacificGoldenPlover, CommonMyna, ReefHeron,
    RedCrownedCrane, MandarinDuck, ChineseMonal, SilverPheasant, CrestedIbis,
    ChinesePondHeron, FairyPitta, Hwamei, BlackDrongo, RedBilledBlueMagpie,
    AfricanFishEagle, SecretaryBird, MartialEagle, MarabouStork, SuperbStarling,
    CapeWeaver, Hamerkop, AfricanGreyParrot, GroundHornbill, AfricanPenguin,
    # African 100
    LilacBreastedRoller, CarmineBeeEater, WhiteFrontedBeeEater, LittleBeeEater,
    AbyssinianRoller, MalachiteKingfisher, GiantKingfisher, PygmyKingfisher,
    PiedKingfisher, GreyHeadedKingfisher,
    BateleurEagle, TawnyEagle, VerreauxsEagle, BrownSnakeEagle, LongCrestedEagle,
    AfricanCrownedEagle, LannerFalcon, PygmyFalcon, AfricanKestrel, RedNeckedFalcon,
    LappetFacedVulture, WhiteBackedVulture, EgyptianVulture, PalmNutVulture,
    SaddlebilledStork, YellowBilledStork, GoliathHeron, PurpleHeron, BlackHeadedHeron,
    GreatEgret, CattleEgret, SquaccoHeron, GreyCrownedCrane,
    HadedaIbis, SacredIbis, GlossyIbis, AfricanSpoonbill, GreatWhitePelican, AfricanDarter,
    CrownedLapwing, BlackwingedStilt, PurpleSwamphen, AfricanRail, AfricanJacana,
    RedBilledQuelea, VillageWeaver, GoldenBishop, SouthernRedBishop, WattledStarling,
    MalachiteSunbird, OrangeBreastSunbird, ScarletChestSunbird, AmethystSunbird,
    CollaredSunbird, VariableSunbird,
    VioletBackedStarling, GreaterBlueEaredStarling, PlumColoredStarling, PiedStarling,
    BurchellsStarling,
    AfricanFirefinch, BlueWaxbill, VioletEaredWaxbill, YellowFrontedCanary, MelbaFinch,
    AfricanSilverbill, LocustFinch,
    DoubleToothBarbet, BlackCollaredBarbet, RedYellowBarbet,
    AfricanGreenPigeon, NamaquaDove, LaughingDove, MeyerParrot, CapeParrot,
    RosyFacedLovebird,
    Ostrich, KoriBustard, HelmettedGuineafowl, NamaquaSandgrouse,
    FiscalShrike, RedBackedShrike, PiedCrow, FanTailedRaven, ParadiseFlycatcher,
    Batis, CapeRobinChat, AfricanStonechat,
    PennantWingedNightjar, AlpineSwift, AfricanPalmSwift,
    RedKnobbedCoot, AfricanSnipe, SpottedThickKnee, WattledPlover, BlacksmithLapwing,
    ThreeBandedPlover, AfricanFishOwl, VerreauxsEagleOwl, SpeckledMousebird,
    # Ground birds
    GambelsQuail,
    # Nocturnal birds
    TawnyFrogmouth, CommonPotoo, WhippoorWill, CommonPoorwill,
    ElfOwl, BurrowingOwl, BarredOwl, SpectacledOwl,
    LongEaredOwl, ShortEaredOwl, FerruginousPygmyOwl,
    Kiwi, NightParrot, CommonScopsOwl, EasternScreechOwl,
    # Bats (nocturnal)
    LittleBrownBat, BigBrownBat, FruitBat, VampireBat, HorseshoeBat,
    PipistrelBat, NoctuleBat, LeafNosedBat, GhostBat, HammerHeadedBat,
    # Penguins
    EmperorPenguin, KingPenguin, GentooPenguin, ChinStrapPenguin, AdeliePenguin,
    MacaroniPenguin, RockHopperPenguin, SnaresPenguin, FjordlandPenguin, LittleBluePenguin,
]

SPECIES_BY_ID = {cls.SPECIES: cls for cls in ALL_SPECIES}

# Opportunistic birds that spawn in any biome not covered by ALL_SPECIES entries.
# Add to this list when adding a new biome if no existing species cover it.
COMMON_SPECIES = [Crow, Vulture, Raven]
