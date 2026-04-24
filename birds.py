import random
import math
from constants import BLOCK_SIZE

from blocks import (
    TREE_LEAVES, PINE_LEAVES, BIRCH_LEAVES, JUNGLE_LEAVES, WILLOW_LEAVES,
    REDWOOD_LEAVES, PALM_LEAVES, ACACIA_LEAVES, MAPLE_LEAVES, CHERRY_LEAVES,
    BIRD_FEEDER_BLOCK, BIRD_BATH_BLOCK,
)

LEAF_BLOCKS = frozenset({
    TREE_LEAVES, PINE_LEAVES, BIRCH_LEAVES, JUNGLE_LEAVES, WILLOW_LEAVES,
    REDWOOD_LEAVES, PALM_LEAVES, ACACIA_LEAVES, MAPLE_LEAVES, CHERRY_LEAVES,
})
FEEDER_BATH_BLOCKS = frozenset({BIRD_FEEDER_BLOCK, BIRD_BATH_BLOCK})

SPOOK_SPEED_THRESHOLD = 0.8   # px/frame — player vx above this counts as moving
SPOOK_RADIUS_BLOCKS   = 5     # blocks


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
        sy    = self._surface_y_at(tx_bx)
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
        # Birds at feeders/baths are calmer — larger spook distance needed
        if self._perch_type in ("feeder", "bath"):
            spook_radius = 12
        else:
            spook_radius = SPOOK_RADIUS_BLOCKS
        player = getattr(self.world, '_player_ref', None)
        reduction = getattr(player, 'bird_spook_reduction', 0.0) if player else 0.0
        spook_radius = spook_radius * (1.0 - reduction)
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

        # Don't fly below the surface
        bx = int(self.x // BLOCK_SIZE)
        sy = self._surface_y_at(bx)
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
                self._state_timer = random.uniform(20, 60)
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
            # No tree here — fly somewhere else
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
            self._state_timer = random.uniform(5, 20)
            self.state        = "perching"
            return

        spd = self.SPEED * 0.5
        if dist > 0.1:
            self.vx = (dx / dist) * spd
            self.vy = (dy / dist) * spd
        self.x += self.vx * dt
        self.y += self.vy * dt


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


class Roadrunner(Bird):
    SPECIES          = "roadrunner"
    RARITY           = "common"
    BIOMES           = ["desert", "arid_steppe", "canyon"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 3)
    SPEED            = 90.0
    W, H             = 18, 10
    BODY_COLOR       = (100, 90, 70)
    WING_COLOR       = (85, 75, 58)
    BEAK_COLOR       = (70, 65, 55)
    HEAD_COLOR       = (100, 90, 70)
    ACCENT_COLOR     = (30, 100, 160)   # blue eye-ring


class Peacock(Bird):
    SPECIES          = "peacock"
    RARITY           = "rare"
    BIOMES           = ["tropical", "savanna"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (2, 6)
    SPEED            = 55.0
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


class Pheasant(Bird):
    SPECIES          = "pheasant"
    RARITY           = "uncommon"
    BIOMES           = ["temperate", "birch_forest", "boreal", "rolling_hills"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 55.0
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
    BIOMES           = ["savanna", "wasteland", "fungal", "desert"]
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
    BIOMES           = ["boreal", "alpine_mountain", "tundra", "redwood", "wasteland", "fungal"]
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


class Lyrebird(Bird):
    SPECIES          = "lyrebird"
    RARITY           = "rare"
    BIOMES           = ["jungle", "redwood"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 50.0
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


class GoldenPheasant(Bird):
    SPECIES          = "golden_pheasant"
    RARITY           = "rare"
    BIOMES           = ["jungle", "tropical", "redwood"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 5)
    SPEED            = 60.0
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


class SilverPheasant(Bird):
    SPECIES          = "silver_pheasant"
    RARITY           = "uncommon"
    BIOMES           = ["jungle", "redwood", "boreal"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 5)
    SPEED            = 55.0
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


class SecretaryBird(Bird):
    SPECIES          = "secretary_bird"
    RARITY           = "rare"
    BIOMES           = ["savanna", "steppe", "arid_steppe"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 50.0
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


class GroundHornbill(Bird):
    SPECIES          = "ground_hornbill"
    RARITY           = "rare"
    BIOMES           = ["savanna"]
    IS_FLOCK         = False
    FLOCK_SIZE_RANGE = (1, 1)
    ALTITUDE_BLOCKS  = (1, 4)
    SPEED            = 50.0
    W, H             = 24, 16
    BODY_COLOR       = (25, 22, 28)     # black
    WING_COLOR       = (240, 238, 235)  # white wing patches (in flight)
    BEAK_COLOR       = (28, 25, 28)     # black massive casqued bill
    HEAD_COLOR       = (200, 45, 40)    # red facial skin
    ACCENT_COLOR     = (200, 45, 40)    # red throat wattle


class AfricanPenguin(Bird):
    SPECIES          = "african_penguin"
    RARITY           = "uncommon"
    BIOMES           = ["beach"]
    IS_FLOCK         = True
    FLOCK_SIZE_RANGE = (2, 5)
    ALTITUDE_BLOCKS  = (1, 3)
    SPEED            = 55.0
    W, H             = 12, 14
    BODY_COLOR       = (245, 242, 238)  # white
    WING_COLOR       = (28, 25, 32)     # black
    BEAK_COLOR       = (38, 35, 30)
    HEAD_COLOR       = (28, 25, 32)     # black
    ACCENT_COLOR     = (218, 148, 132)  # pink cheek patches


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
    RedCrownedCrane, MandarinDuck, ChineseMonal, SilverPheasant, CrestedIbis,
    ChinesePondHeron, FairyPitta, Hwamei, BlackDrongo, RedBilledBlueMagpie,
    AfricanFishEagle, SecretaryBird, MartialEagle, MarabouStork, SuperbStarling,
    CapeWeaver, Hamerkop, AfricanGreyParrot, GroundHornbill, AfricanPenguin,
]

SPECIES_BY_ID = {cls.SPECIES: cls for cls in ALL_SPECIES}
