import random
import math
from constants import BLOCK_SIZE

FLEE_SPEED       = 90.0   # px/s while fleeing
FLEE_DURATION    = 2.0    # seconds spent fleeing before hiding
HIDE_MIN         = 15.0   # seconds hidden before returning
HIDE_MAX         = 35.0
OBS_SPEED_THRESH = 40.0   # player px/s; below this counts as "slow approach"
OBS_DURATION     = 1.5    # seconds of slow approach needed for discovery


class Reptile:
    SPECIES       = "unknown"
    RARITY        = "common"
    BIOMES        = []       # empty = any biodome
    BODY_TYPE     = "lizard" # "snake" | "lizard" | "turtle"
    SPEED         = 30.0
    PATROL_RANGE  = 48       # px each side of spawn before turning
    SPOOK_RADIUS  = 6        # blocks — fast player within this triggers flee
    OBS_RADIUS    = 4        # blocks — slow player within this accumulates obs timer
    W, H          = 16, 8
    BODY_COLOR    = (180, 120, 60)
    PATTERN_COLOR = (120, 80, 40)
    BELLY_COLOR   = (220, 200, 160)

    def __init__(self, x, y, world):
        self.x         = float(x)
        self.y         = float(y)
        self._spawn_x  = float(x)
        self._spawn_y  = float(y)
        self.vx        = 0.0
        self.vy        = 0.0
        self.facing    = random.choice([-1, 1])
        self.state     = "resting"   # resting | moving | fleeing | hidden
        self._state_timer = random.uniform(2.0, 6.0)
        self._obs_timer   = 0.0
        self._anim_phase  = random.uniform(0, math.pi * 2)
        self.world        = world
        self.animal_id    = f"reptile_{self.SPECIES}"

    def flee(self):
        self.state = "fleeing"
        self._state_timer = FLEE_DURATION
        self.vx = self.facing * FLEE_SPEED
        self.vy = 0.0

    def update(self, dt):
        self._anim_phase += dt * 4.0

        if self.state == "hidden":
            self._state_timer -= dt
            if self._state_timer <= 0:
                self.state = "resting"
                self._state_timer = random.uniform(3.0, 7.0)
                self.x = self._spawn_x + random.uniform(-BLOCK_SIZE, BLOCK_SIZE)
                self.y = self._spawn_y
                self.vx = self.vy = 0.0
            return

        if self.state == "fleeing":
            self.x += self.vx * dt
            self._state_timer -= dt
            if self._state_timer <= 0:
                self.state = "hidden"
                self._state_timer = random.uniform(HIDE_MIN, HIDE_MAX)
                self.vx = self.vy = 0.0
            return

        player = getattr(self.world, '_player_ref', None)
        if player is not None:
            dx_b = abs(player.x - self.x) / BLOCK_SIZE
            dy_b = abs(player.y - self.y) / BLOCK_SIZE
            if dx_b < self.SPOOK_RADIUS and dy_b < self.SPOOK_RADIUS * 0.6:
                if abs(player.vx) > OBS_SPEED_THRESH:
                    self._obs_timer = 0.0
                    self.flee()
                    return

        self._state_timer -= dt
        if self.state == "resting":
            self.vx = 0.0
            if self._state_timer <= 0:
                self.state = "moving"
                self._state_timer = random.uniform(1.5, 4.0)
                self.facing = random.choice([-1, 1])
        elif self.state == "moving":
            dist = self.x - self._spawn_x
            if abs(dist) > self.PATROL_RANGE:
                self.facing = -1 if dist > 0 else 1
            self.vx = self.facing * self.SPEED
            self.x += self.vx * dt
            if self._state_timer <= 0:
                self.state = "resting"
                self._state_timer = random.uniform(3.0, 8.0)
                self.vx = 0.0


# ---------------------------------------------------------------------------
# Snakes (7)
# ---------------------------------------------------------------------------

class CornSnake(Reptile):
    SPECIES       = "corn_snake"
    RARITY        = "common"
    BIOMES        = ["temperate", "rolling_hills"]
    BODY_TYPE     = "snake"
    SPEED         = 35.0
    W, H          = 20, 6
    BODY_COLOR    = (210, 100, 60)
    PATTERN_COLOR = (160, 50, 30)
    BELLY_COLOR   = (245, 220, 190)

class GarterSnake(Reptile):
    SPECIES       = "garter_snake"
    RARITY        = "common"
    BIOMES        = ["temperate", "wetland"]
    BODY_TYPE     = "snake"
    SPEED         = 38.0
    W, H          = 18, 5
    BODY_COLOR    = (60, 100, 50)
    PATTERN_COLOR = (200, 190, 80)
    BELLY_COLOR   = (200, 220, 160)

class MilkSnake(Reptile):
    SPECIES       = "milk_snake"
    RARITY        = "common"
    BIOMES        = ["temperate", "birch_forest"]
    BODY_TYPE     = "snake"
    SPEED         = 32.0
    W, H          = 18, 6
    BODY_COLOR    = (210, 50, 40)
    PATTERN_COLOR = (240, 240, 240)
    BELLY_COLOR   = (245, 240, 220)

class Rattlesnake(Reptile):
    SPECIES       = "rattlesnake"
    RARITY        = "uncommon"
    BIOMES        = ["desert", "canyon", "wasteland"]
    BODY_TYPE     = "snake"
    SPEED         = 30.0
    W, H          = 20, 7
    BODY_COLOR    = (180, 150, 80)
    PATTERN_COLOR = (120, 90, 40)
    BELLY_COLOR   = (230, 215, 170)

class EmeraldTreeBoa(Reptile):
    SPECIES       = "emerald_tree_boa"
    RARITY        = "uncommon"
    BIOMES        = ["jungle", "tropical"]
    BODY_TYPE     = "snake"
    SPEED         = 28.0
    W, H          = 22, 6
    BODY_COLOR    = (50, 160, 70)
    PATTERN_COLOR = (255, 255, 255)
    BELLY_COLOR   = (200, 230, 180)

class KingCobra(Reptile):
    SPECIES       = "king_cobra"
    RARITY        = "rare"
    BIOMES        = ["jungle", "tropical"]
    BODY_TYPE     = "snake"
    SPEED         = 40.0
    W, H          = 24, 7
    SPOOK_RADIUS  = 7
    BODY_COLOR    = (60, 50, 30)
    PATTERN_COLOR = (180, 150, 80)
    BELLY_COLOR   = (220, 200, 150)

class BlackMamba(Reptile):
    SPECIES       = "black_mamba"
    RARITY        = "rare"
    BIOMES        = ["savanna", "steppe"]
    BODY_TYPE     = "snake"
    SPEED         = 45.0
    W, H          = 22, 6
    SPOOK_RADIUS  = 8
    BODY_COLOR    = (40, 40, 35)
    PATTERN_COLOR = (70, 65, 55)
    BELLY_COLOR   = (180, 170, 140)


# ---------------------------------------------------------------------------
# Lizards (8)
# ---------------------------------------------------------------------------

class Gecko(Reptile):
    SPECIES       = "gecko"
    RARITY        = "common"
    BIOMES        = ["tropical", "jungle"]
    BODY_TYPE     = "lizard"
    SPEED         = 40.0
    W, H          = 14, 7
    BODY_COLOR    = (120, 180, 100)
    PATTERN_COLOR = (80, 130, 60)
    BELLY_COLOR   = (200, 220, 180)

class BlueTonguedSkink(Reptile):
    SPECIES       = "blue_tongued_skink"
    RARITY        = "common"
    BIOMES        = ["savanna", "steppe"]
    BODY_TYPE     = "lizard"
    SPEED         = 25.0
    W, H          = 16, 8
    BODY_COLOR    = (140, 120, 80)
    PATTERN_COLOR = (180, 160, 110)
    BELLY_COLOR   = (210, 200, 170)

class HornedLizard(Reptile):
    SPECIES       = "horned_lizard"
    RARITY        = "uncommon"
    BIOMES        = ["desert", "canyon"]
    BODY_TYPE     = "lizard"
    SPEED         = 28.0
    W, H          = 14, 9
    BODY_COLOR    = (190, 155, 100)
    PATTERN_COLOR = (140, 100, 60)
    BELLY_COLOR   = (230, 210, 175)

class FrilledLizard(Reptile):
    SPECIES       = "frilled_lizard"
    RARITY        = "uncommon"
    BIOMES        = ["savanna", "desert"]
    BODY_TYPE     = "lizard"
    SPEED         = 42.0
    W, H          = 16, 10
    BODY_COLOR    = (130, 110, 70)
    PATTERN_COLOR = (200, 160, 90)
    BELLY_COLOR   = (220, 200, 160)

class Iguana(Reptile):
    SPECIES       = "iguana"
    RARITY        = "uncommon"
    BIOMES        = ["tropical", "jungle"]
    BODY_TYPE     = "lizard"
    SPEED         = 30.0
    W, H          = 20, 10
    BODY_COLOR    = (70, 140, 80)
    PATTERN_COLOR = (50, 100, 55)
    BELLY_COLOR   = (180, 210, 160)

class MonitorLizard(Reptile):
    SPECIES       = "monitor_lizard"
    RARITY        = "uncommon"
    BIOMES        = ["savanna", "tropical"]
    BODY_TYPE     = "lizard"
    SPEED         = 35.0
    W, H          = 22, 10
    BODY_COLOR    = (80, 80, 60)
    PATTERN_COLOR = (140, 130, 90)
    BELLY_COLOR   = (200, 190, 155)

class Chameleon(Reptile):
    SPECIES       = "chameleon"
    RARITY        = "rare"
    BIOMES        = ["jungle", "tropical"]
    BODY_TYPE     = "lizard"
    SPEED         = 20.0
    W, H          = 16, 12
    BODY_COLOR    = (80, 160, 90)
    PATTERN_COLOR = (120, 210, 130)
    BELLY_COLOR   = (180, 230, 170)

class KomodoDragon(Reptile):
    SPECIES       = "komodo_dragon"
    RARITY        = "rare"
    BIOMES        = ["tropical"]
    BODY_TYPE     = "lizard"
    SPEED         = 28.0
    W, H          = 26, 12
    SPOOK_RADIUS  = 7
    BODY_COLOR    = (90, 80, 60)
    PATTERN_COLOR = (130, 115, 85)
    BELLY_COLOR   = (195, 180, 150)


# ---------------------------------------------------------------------------
# Turtles (5)
# ---------------------------------------------------------------------------

class BoxTurtle(Reptile):
    SPECIES       = "box_turtle"
    RARITY        = "common"
    BIOMES        = ["temperate", "boreal"]
    BODY_TYPE     = "turtle"
    SPEED         = 12.0
    PATROL_RANGE  = 32
    W, H          = 14, 10
    BODY_COLOR    = (80, 55, 30)
    PATTERN_COLOR = (200, 160, 60)
    BELLY_COLOR   = (210, 190, 140)

class PaintedTurtle(Reptile):
    SPECIES       = "painted_turtle"
    RARITY        = "common"
    BIOMES        = ["wetland", "temperate"]
    BODY_TYPE     = "turtle"
    SPEED         = 10.0
    PATROL_RANGE  = 32
    W, H          = 14, 10
    BODY_COLOR    = (50, 60, 40)
    PATTERN_COLOR = (200, 80, 40)
    BELLY_COLOR   = (220, 200, 100)

class SnappingTurtle(Reptile):
    SPECIES       = "snapping_turtle"
    RARITY        = "uncommon"
    BIOMES        = ["swamp", "wetland"]
    BODY_TYPE     = "turtle"
    SPEED         = 8.0
    PATROL_RANGE  = 24
    W, H          = 16, 11
    SPOOK_RADIUS  = 5
    BODY_COLOR    = (50, 50, 35)
    PATTERN_COLOR = (80, 75, 50)
    BELLY_COLOR   = (180, 170, 130)

class Leatherback(Reptile):
    SPECIES       = "leatherback"
    RARITY        = "rare"
    BIOMES        = ["beach"]
    BODY_TYPE     = "turtle"
    SPEED         = 8.0
    PATROL_RANGE  = 32
    W, H          = 20, 13
    BODY_COLOR    = (40, 45, 55)
    PATTERN_COLOR = (80, 90, 100)
    BELLY_COLOR   = (160, 165, 170)

class AlligatorSnappingTurtle(Reptile):
    SPECIES       = "alligator_snapping_turtle"
    RARITY        = "rare"
    BIOMES        = ["swamp"]
    BODY_TYPE     = "turtle"
    SPEED         = 6.0
    PATROL_RANGE  = 20
    W, H          = 18, 12
    SPOOK_RADIUS  = 4
    OBS_RADIUS    = 3
    BODY_COLOR    = (45, 40, 30)
    PATTERN_COLOR = (70, 60, 45)
    BELLY_COLOR   = (170, 155, 120)


# ---------------------------------------------------------------------------
# Snakes — additional 35 species
# ---------------------------------------------------------------------------

class BallPython(Reptile):
    SPECIES       = "ball_python"
    RARITY        = "common"
    BIOMES        = ["jungle", "tropical"]
    BODY_TYPE     = "snake"
    SPEED         = 22.0
    W, H          = 18, 7
    BODY_COLOR    = (60, 45, 30)
    PATTERN_COLOR = (180, 140, 80)
    BELLY_COLOR   = (220, 210, 180)

class BoaConstrictor(Reptile):
    SPECIES       = "boa_constrictor"
    RARITY        = "uncommon"
    BIOMES        = ["jungle", "tropical"]
    BODY_TYPE     = "snake"
    SPEED         = 25.0
    W, H          = 24, 8
    BODY_COLOR    = (100, 80, 55)
    PATTERN_COLOR = (160, 120, 70)
    BELLY_COLOR   = (225, 215, 185)

class ReticulatedPython(Reptile):
    SPECIES       = "reticulated_python"
    RARITY        = "rare"
    BIOMES        = ["jungle", "tropical"]
    BODY_TYPE     = "snake"
    SPEED         = 20.0
    W, H          = 28, 9
    SPOOK_RADIUS  = 6
    BODY_COLOR    = (80, 65, 40)
    PATTERN_COLOR = (190, 150, 80)
    BELLY_COLOR   = (230, 220, 190)

class Anaconda(Reptile):
    SPECIES       = "anaconda"
    RARITY        = "rare"
    BIOMES        = ["wetland", "swamp"]
    BODY_TYPE     = "snake"
    SPEED         = 18.0
    W, H          = 28, 10
    SPOOK_RADIUS  = 7
    BODY_COLOR    = (55, 75, 40)
    PATTERN_COLOR = (90, 120, 65)
    BELLY_COLOR   = (210, 210, 170)

class WesternHognose(Reptile):
    SPECIES       = "western_hognose"
    RARITY        = "common"
    BIOMES        = ["temperate", "steppe"]
    BODY_TYPE     = "snake"
    SPEED         = 28.0
    W, H          = 16, 6
    BODY_COLOR    = (180, 150, 90)
    PATTERN_COLOR = (120, 90, 50)
    BELLY_COLOR   = (235, 220, 185)

class BullSnake(Reptile):
    SPECIES       = "bull_snake"
    RARITY        = "common"
    BIOMES        = ["steppe", "temperate"]
    BODY_TYPE     = "snake"
    SPEED         = 30.0
    W, H          = 20, 6
    BODY_COLOR    = (190, 160, 90)
    PATTERN_COLOR = (130, 100, 50)
    BELLY_COLOR   = (240, 230, 200)

class RingNeckedSnake(Reptile):
    SPECIES       = "ring_necked_snake"
    RARITY        = "common"
    BIOMES        = ["temperate", "boreal"]
    BODY_TYPE     = "snake"
    SPEED         = 32.0
    W, H          = 14, 5
    BODY_COLOR    = (50, 50, 45)
    PATTERN_COLOR = (220, 130, 30)
    BELLY_COLOR   = (230, 120, 40)

class SmoothGreenSnake(Reptile):
    SPECIES       = "smooth_green_snake"
    RARITY        = "common"
    BIOMES        = ["temperate", "steppe"]
    BODY_TYPE     = "snake"
    SPEED         = 35.0
    W, H          = 16, 5
    BODY_COLOR    = (90, 170, 70)
    PATTERN_COLOR = (70, 140, 55)
    BELLY_COLOR   = (210, 240, 180)

class EasternHognose(Reptile):
    SPECIES       = "eastern_hognose"
    RARITY        = "common"
    BIOMES        = ["temperate", "boreal"]
    BODY_TYPE     = "snake"
    SPEED         = 26.0
    W, H          = 16, 6
    BODY_COLOR    = (160, 130, 80)
    PATTERN_COLOR = (100, 75, 40)
    BELLY_COLOR   = (235, 215, 175)

class PineSnake(Reptile):
    SPECIES       = "pine_snake"
    RARITY        = "uncommon"
    BIOMES        = ["temperate", "boreal"]
    BODY_TYPE     = "snake"
    SPEED         = 30.0
    W, H          = 20, 7
    BODY_COLOR    = (200, 185, 150)
    PATTERN_COLOR = (100, 85, 60)
    BELLY_COLOR   = (245, 238, 215)

class Copperhead(Reptile):
    SPECIES       = "copperhead"
    RARITY        = "uncommon"
    BIOMES        = ["temperate", "boreal"]
    BODY_TYPE     = "snake"
    SPEED         = 28.0
    W, H          = 18, 7
    BODY_COLOR    = (185, 110, 55)
    PATTERN_COLOR = (130, 65, 25)
    BELLY_COLOR   = (230, 210, 175)

class Cottonmouth(Reptile):
    SPECIES       = "cottonmouth"
    RARITY        = "uncommon"
    BIOMES        = ["wetland", "swamp"]
    BODY_TYPE     = "snake"
    SPEED         = 26.0
    W, H          = 20, 8
    SPOOK_RADIUS  = 6
    BODY_COLOR    = (55, 50, 38)
    PATTERN_COLOR = (80, 72, 55)
    BELLY_COLOR   = (200, 185, 145)

class TimberRattlesnake(Reptile):
    SPECIES       = "timber_rattlesnake"
    RARITY        = "uncommon"
    BIOMES        = ["boreal", "temperate"]
    BODY_TYPE     = "snake"
    SPEED         = 28.0
    W, H          = 20, 8
    BODY_COLOR    = (100, 85, 55)
    PATTERN_COLOR = (50, 40, 25)
    BELLY_COLOR   = (215, 200, 165)

class Sidewinder(Reptile):
    SPECIES       = "sidewinder"
    RARITY        = "uncommon"
    BIOMES        = ["desert", "canyon"]
    BODY_TYPE     = "snake"
    SPEED         = 38.0
    W, H          = 16, 6
    BODY_COLOR    = (195, 170, 115)
    PATTERN_COLOR = (145, 120, 70)
    BELLY_COLOR   = (235, 225, 195)

class WesternDiamondback(Reptile):
    SPECIES       = "western_diamondback"
    RARITY        = "uncommon"
    BIOMES        = ["desert", "wasteland"]
    BODY_TYPE     = "snake"
    SPEED         = 28.0
    W, H          = 22, 8
    SPOOK_RADIUS  = 6
    BODY_COLOR    = (175, 148, 95)
    PATTERN_COLOR = (115, 90, 50)
    BELLY_COLOR   = (228, 215, 178)

class EasternCoralSnake(Reptile):
    SPECIES       = "eastern_coral_snake"
    RARITY        = "uncommon"
    BIOMES        = ["temperate", "jungle"]
    BODY_TYPE     = "snake"
    SPEED         = 30.0
    W, H          = 16, 5
    BODY_COLOR    = (210, 50, 40)
    PATTERN_COLOR = (240, 220, 30)
    BELLY_COLOR   = (240, 240, 240)

class WesternCoralSnake(Reptile):
    SPECIES       = "western_coral_snake"
    RARITY        = "uncommon"
    BIOMES        = ["desert", "savanna"]
    BODY_TYPE     = "snake"
    SPEED         = 28.0
    W, H          = 14, 5
    BODY_COLOR    = (205, 50, 42)
    PATTERN_COLOR = (235, 215, 28)
    BELLY_COLOR   = (238, 238, 238)

class ScarletKingsnake(Reptile):
    SPECIES       = "scarlet_kingsnake"
    RARITY        = "common"
    BIOMES        = ["temperate", "boreal"]
    BODY_TYPE     = "snake"
    SPEED         = 30.0
    W, H          = 16, 5
    BODY_COLOR    = (208, 52, 42)
    PATTERN_COLOR = (240, 240, 240)
    BELLY_COLOR   = (242, 242, 242)

class IndigoSnake(Reptile):
    SPECIES       = "indigo_snake"
    RARITY        = "uncommon"
    BIOMES        = ["tropical", "savanna"]
    BODY_TYPE     = "snake"
    SPEED         = 40.0
    W, H          = 22, 7
    BODY_COLOR    = (30, 30, 50)
    PATTERN_COLOR = (55, 50, 75)
    BELLY_COLOR   = (180, 140, 130)

class CapeCobra(Reptile):
    SPECIES       = "cape_cobra"
    RARITY        = "uncommon"
    BIOMES        = ["savanna", "steppe"]
    BODY_TYPE     = "snake"
    SPEED         = 36.0
    W, H          = 20, 7
    BODY_COLOR    = (200, 160, 60)
    PATTERN_COLOR = (150, 110, 35)
    BELLY_COLOR   = (235, 215, 165)

class PuffAdder(Reptile):
    SPECIES       = "puff_adder"
    RARITY        = "uncommon"
    BIOMES        = ["savanna", "steppe"]
    BODY_TYPE     = "snake"
    SPEED         = 22.0
    W, H          = 20, 9
    SPOOK_RADIUS  = 5
    BODY_COLOR    = (160, 130, 70)
    PATTERN_COLOR = (100, 78, 38)
    BELLY_COLOR   = (225, 210, 170)

class GaboonViper(Reptile):
    SPECIES       = "gaboon_viper"
    RARITY        = "rare"
    BIOMES        = ["jungle"]
    BODY_TYPE     = "snake"
    SPEED         = 20.0
    W, H          = 22, 10
    BODY_COLOR    = (130, 100, 60)
    PATTERN_COLOR = (90, 60, 30)
    BELLY_COLOR   = (210, 195, 155)

class Boomslang(Reptile):
    SPECIES       = "boomslang"
    RARITY        = "rare"
    BIOMES        = ["savanna", "jungle"]
    BODY_TYPE     = "snake"
    SPEED         = 38.0
    W, H          = 20, 6
    BODY_COLOR    = (75, 150, 55)
    PATTERN_COLOR = (55, 110, 38)
    BELLY_COLOR   = (195, 225, 165)

class VineSnake(Reptile):
    SPECIES       = "vine_snake"
    RARITY        = "uncommon"
    BIOMES        = ["jungle", "tropical"]
    BODY_TYPE     = "snake"
    SPEED         = 30.0
    W, H          = 18, 4
    BODY_COLOR    = (80, 150, 55)
    PATTERN_COLOR = (60, 120, 40)
    BELLY_COLOR   = (195, 230, 160)

class FlyingSnake(Reptile):
    SPECIES       = "flying_snake"
    RARITY        = "rare"
    BIOMES        = ["jungle", "tropical"]
    BODY_TYPE     = "snake"
    SPEED         = 42.0
    W, H          = 18, 5
    BODY_COLOR    = (60, 160, 80)
    PATTERN_COLOR = (200, 70, 50)
    BELLY_COLOR   = (200, 240, 185)

class MangroveSnake(Reptile):
    SPECIES       = "mangrove_snake"
    RARITY        = "uncommon"
    BIOMES        = ["wetland", "tropical"]
    BODY_TYPE     = "snake"
    SPEED         = 30.0
    W, H          = 20, 6
    BODY_COLOR    = (30, 30, 25)
    PATTERN_COLOR = (230, 200, 50)
    BELLY_COLOR   = (215, 200, 155)

class TigerSnake(Reptile):
    SPECIES       = "tiger_snake"
    RARITY        = "uncommon"
    BIOMES        = ["temperate", "wetland"]
    BODY_TYPE     = "snake"
    SPEED         = 30.0
    W, H          = 18, 7
    SPOOK_RADIUS  = 6
    BODY_COLOR    = (80, 75, 40)
    PATTERN_COLOR = (200, 185, 80)
    BELLY_COLOR   = (220, 215, 160)

class Taipan(Reptile):
    SPECIES       = "taipan"
    RARITY        = "rare"
    BIOMES        = ["tropical", "savanna"]
    BODY_TYPE     = "snake"
    SPEED         = 44.0
    W, H          = 22, 7
    SPOOK_RADIUS  = 7
    BODY_COLOR    = (130, 100, 55)
    PATTERN_COLOR = (90, 68, 32)
    BELLY_COLOR   = (230, 215, 175)

class InlandTaipan(Reptile):
    SPECIES       = "inland_taipan"
    RARITY        = "rare"
    BIOMES        = ["desert", "wasteland"]
    BODY_TYPE     = "snake"
    SPEED         = 46.0
    W, H          = 22, 7
    SPOOK_RADIUS  = 8
    BODY_COLOR    = (100, 75, 35)
    PATTERN_COLOR = (65, 48, 20)
    BELLY_COLOR   = (225, 208, 165)

class DeathAdder(Reptile):
    SPECIES       = "death_adder"
    RARITY        = "rare"
    BIOMES        = ["savanna", "tropical"]
    BODY_TYPE     = "snake"
    SPEED         = 30.0
    W, H          = 18, 8
    BODY_COLOR    = (115, 90, 55)
    PATTERN_COLOR = (75, 55, 28)
    BELLY_COLOR   = (215, 200, 162)

class RedBelliedBlackSnake(Reptile):
    SPECIES       = "red_bellied_black_snake"
    RARITY        = "uncommon"
    BIOMES        = ["wetland", "temperate"]
    BODY_TYPE     = "snake"
    SPEED         = 32.0
    W, H          = 20, 6
    BODY_COLOR    = (25, 22, 28)
    PATTERN_COLOR = (35, 30, 38)
    BELLY_COLOR   = (200, 60, 60)

class GreenMamba(Reptile):
    SPECIES       = "green_mamba"
    RARITY        = "uncommon"
    BIOMES        = ["jungle", "tropical"]
    BODY_TYPE     = "snake"
    SPEED         = 42.0
    W, H          = 20, 6
    SPOOK_RADIUS  = 7
    BODY_COLOR    = (55, 165, 75)
    PATTERN_COLOR = (42, 130, 58)
    BELLY_COLOR   = (195, 235, 175)

class AsianPitViper(Reptile):
    SPECIES       = "asian_pit_viper"
    RARITY        = "uncommon"
    BIOMES        = ["jungle", "tropical"]
    BODY_TYPE     = "snake"
    SPEED         = 26.0
    W, H          = 18, 7
    BODY_COLOR    = (65, 140, 65)
    PATTERN_COLOR = (42, 100, 42)
    BELLY_COLOR   = (190, 225, 170)

class RoughScaledSnake(Reptile):
    SPECIES       = "rough_scaled_snake"
    RARITY        = "common"
    BIOMES        = ["temperate", "boreal"]
    BODY_TYPE     = "snake"
    SPEED         = 30.0
    W, H          = 16, 6
    BODY_COLOR    = (75, 90, 55)
    PATTERN_COLOR = (55, 68, 38)
    BELLY_COLOR   = (205, 215, 170)

class ScalelessCornSnake(Reptile):
    SPECIES       = "scaleless_corn_snake"
    RARITY        = "rare"
    BIOMES        = ["temperate"]
    BODY_TYPE     = "snake"
    SPEED         = 32.0
    W, H          = 18, 6
    BODY_COLOR    = (225, 115, 75)
    PATTERN_COLOR = (175, 65, 40)
    BELLY_COLOR   = (248, 228, 198)


# ---------------------------------------------------------------------------
# Snakes — additional 50 species
# ---------------------------------------------------------------------------

class AfricanRockPython(Reptile):
    SPECIES       = "african_rock_python"
    RARITY        = "rare"
    BIOMES        = ["savanna", "tropical"]
    BODY_TYPE     = "snake"
    SPEED         = 22.0
    W, H          = 28, 10
    SPOOK_RADIUS  = 7
    BODY_COLOR    = (110, 90, 55)
    PATTERN_COLOR = (170, 140, 80)
    BELLY_COLOR   = (228, 218, 185)

class BurmesePython(Reptile):
    SPECIES       = "burmese_python"
    RARITY        = "rare"
    BIOMES        = ["jungle", "tropical"]
    BODY_TYPE     = "snake"
    SPEED         = 20.0
    W, H          = 28, 10
    SPOOK_RADIUS  = 6
    BODY_COLOR    = (115, 95, 58)
    PATTERN_COLOR = (175, 148, 85)
    BELLY_COLOR   = (230, 222, 188)

class GreenTreePython(Reptile):
    SPECIES       = "green_tree_python"
    RARITY        = "uncommon"
    BIOMES        = ["jungle", "tropical"]
    BODY_TYPE     = "snake"
    SPEED         = 24.0
    W, H          = 20, 6
    BODY_COLOR    = (50, 168, 68)
    PATTERN_COLOR = (255, 255, 255)
    BELLY_COLOR   = (195, 235, 172)

class ChildrensPython(Reptile):
    SPECIES       = "childrens_python"
    RARITY        = "common"
    BIOMES        = ["tropical", "savanna"]
    BODY_TYPE     = "snake"
    SPEED         = 28.0
    W, H          = 16, 6
    BODY_COLOR    = (155, 128, 82)
    PATTERN_COLOR = (108, 85, 52)
    BELLY_COLOR   = (228, 218, 185)

class WomaPython(Reptile):
    SPECIES       = "woma_python"
    RARITY        = "uncommon"
    BIOMES        = ["desert", "arid_steppe"]
    BODY_TYPE     = "snake"
    SPEED         = 26.0
    W, H          = 20, 7
    BODY_COLOR    = (185, 155, 90)
    PATTERN_COLOR = (130, 105, 58)
    BELLY_COLOR   = (232, 220, 182)

class BloodPython(Reptile):
    SPECIES       = "blood_python"
    RARITY        = "uncommon"
    BIOMES        = ["jungle", "wetland"]
    BODY_TYPE     = "snake"
    SPEED         = 18.0
    W, H          = 22, 9
    BODY_COLOR    = (175, 65, 42)
    PATTERN_COLOR = (120, 38, 22)
    BELLY_COLOR   = (235, 215, 178)

class SpottedPython(Reptile):
    SPECIES       = "spotted_python"
    RARITY        = "common"
    BIOMES        = ["tropical", "savanna"]
    BODY_TYPE     = "snake"
    SPEED         = 28.0
    W, H          = 16, 6
    BODY_COLOR    = (145, 115, 70)
    PATTERN_COLOR = (72, 55, 30)
    BELLY_COLOR   = (228, 215, 180)

class AfricanEggEater(Reptile):
    SPECIES       = "african_egg_eater"
    RARITY        = "common"
    BIOMES        = ["savanna", "jungle"]
    BODY_TYPE     = "snake"
    SPEED         = 30.0
    W, H          = 14, 5
    BODY_COLOR    = (130, 105, 65)
    PATTERN_COLOR = (85, 65, 35)
    BELLY_COLOR   = (225, 215, 180)

class NightSnake(Reptile):
    SPECIES       = "night_snake"
    RARITY        = "common"
    BIOMES        = ["desert", "rolling_hills"]
    BODY_TYPE     = "snake"
    SPEED         = 30.0
    W, H          = 15, 5
    BODY_COLOR    = (155, 138, 95)
    PATTERN_COLOR = (95, 80, 50)
    BELLY_COLOR   = (230, 220, 188)

class LyreSnake(Reptile):
    SPECIES       = "lyre_snake"
    RARITY        = "uncommon"
    BIOMES        = ["desert", "canyon"]
    BODY_TYPE     = "snake"
    SPEED         = 28.0
    W, H          = 16, 6
    BODY_COLOR    = (165, 140, 88)
    PATTERN_COLOR = (105, 85, 50)
    BELLY_COLOR   = (232, 220, 185)

class MudSnake(Reptile):
    SPECIES       = "mud_snake"
    RARITY        = "common"
    BIOMES        = ["wetland", "swamp"]
    BODY_TYPE     = "snake"
    SPEED         = 28.0
    W, H          = 18, 6
    BODY_COLOR    = (38, 35, 28)
    PATTERN_COLOR = (200, 55, 45)
    BELLY_COLOR   = (205, 60, 50)

class RainbowSnake(Reptile):
    SPECIES       = "rainbow_snake"
    RARITY        = "uncommon"
    BIOMES        = ["wetland", "swamp"]
    BODY_TYPE     = "snake"
    SPEED         = 30.0
    W, H          = 18, 6
    BODY_COLOR    = (30, 28, 22)
    PATTERN_COLOR = (200, 55, 42)
    BELLY_COLOR   = (218, 195, 75)

class RedBelliedSnake(Reptile):
    SPECIES       = "red_bellied_snake"
    RARITY        = "common"
    BIOMES        = ["temperate", "boreal"]
    BODY_TYPE     = "snake"
    SPEED         = 30.0
    W, H          = 13, 5
    BODY_COLOR    = (95, 75, 50)
    PATTERN_COLOR = (65, 50, 32)
    BELLY_COLOR   = (210, 68, 52)

class QueenSnake(Reptile):
    SPECIES       = "queen_snake"
    RARITY        = "common"
    BIOMES        = ["wetland", "temperate"]
    BODY_TYPE     = "snake"
    SPEED         = 32.0
    W, H          = 15, 5
    BODY_COLOR    = (70, 62, 42)
    PATTERN_COLOR = (48, 42, 28)
    BELLY_COLOR   = (215, 200, 155)

class RibbonSnake(Reptile):
    SPECIES       = "ribbon_snake"
    RARITY        = "common"
    BIOMES        = ["wetland", "temperate"]
    BODY_TYPE     = "snake"
    SPEED         = 36.0
    W, H          = 16, 4
    BODY_COLOR    = (45, 45, 35)
    PATTERN_COLOR = (200, 185, 80)
    BELLY_COLOR   = (205, 220, 165)

class RoughGreenSnake(Reptile):
    SPECIES       = "rough_green_snake"
    RARITY        = "common"
    BIOMES        = ["temperate", "steppe"]
    BODY_TYPE     = "snake"
    SPEED         = 34.0
    W, H          = 15, 5
    BODY_COLOR    = (88, 172, 68)
    PATTERN_COLOR = (65, 132, 50)
    BELLY_COLOR   = (208, 238, 178)

class CaliforniaKingsnake(Reptile):
    SPECIES       = "california_kingsnake"
    RARITY        = "common"
    BIOMES        = ["temperate", "rolling_hills"]
    BODY_TYPE     = "snake"
    SPEED         = 32.0
    W, H          = 18, 6
    BODY_COLOR    = (28, 25, 20)
    PATTERN_COLOR = (235, 235, 225)
    BELLY_COLOR   = (240, 238, 222)

class DesertKingsnake(Reptile):
    SPECIES       = "desert_kingsnake"
    RARITY        = "common"
    BIOMES        = ["desert", "canyon"]
    BODY_TYPE     = "snake"
    SPEED         = 30.0
    W, H          = 18, 6
    BODY_COLOR    = (28, 28, 20)
    PATTERN_COLOR = (205, 195, 80)
    BELLY_COLOR   = (235, 225, 175)

class SpeckledKingsnake(Reptile):
    SPECIES       = "speckled_kingsnake"
    RARITY        = "common"
    BIOMES        = ["temperate", "steppe"]
    BODY_TYPE     = "snake"
    SPEED         = 30.0
    W, H          = 18, 6
    BODY_COLOR    = (32, 30, 22)
    PATTERN_COLOR = (215, 205, 90)
    BELLY_COLOR   = (235, 228, 185)

class PrairieKingsnake(Reptile):
    SPECIES       = "prairie_kingsnake"
    RARITY        = "common"
    BIOMES        = ["steppe", "temperate"]
    BODY_TYPE     = "snake"
    SPEED         = 30.0
    W, H          = 18, 6
    BODY_COLOR    = (155, 130, 82)
    PATTERN_COLOR = (105, 85, 50)
    BELLY_COLOR   = (228, 215, 178)

class GrayBandedKingsnake(Reptile):
    SPECIES       = "gray_banded_kingsnake"
    RARITY        = "uncommon"
    BIOMES        = ["canyon", "desert"]
    BODY_TYPE     = "snake"
    SPEED         = 28.0
    W, H          = 16, 6
    BODY_COLOR    = (155, 155, 155)
    PATTERN_COLOR = (210, 68, 48)
    BELLY_COLOR   = (230, 225, 215)

class EasternKingsnake(Reptile):
    SPECIES       = "eastern_kingsnake"
    RARITY        = "common"
    BIOMES        = ["temperate", "boreal"]
    BODY_TYPE     = "snake"
    SPEED         = 30.0
    W, H          = 18, 6
    BODY_COLOR    = (28, 25, 18)
    PATTERN_COLOR = (230, 228, 218)
    BELLY_COLOR   = (235, 230, 205)

class MoleKingsnake(Reptile):
    SPECIES       = "mole_kingsnake"
    RARITY        = "uncommon"
    BIOMES        = ["temperate", "boreal"]
    BODY_TYPE     = "snake"
    SPEED         = 28.0
    W, H          = 16, 6
    BODY_COLOR    = (175, 135, 80)
    PATTERN_COLOR = (122, 88, 48)
    BELLY_COLOR   = (228, 215, 178)

class ShovelNosedSnake(Reptile):
    SPECIES       = "shovel_nosed_snake"
    RARITY        = "common"
    BIOMES        = ["desert"]
    BODY_TYPE     = "snake"
    SPEED         = 32.0
    W, H          = 13, 5
    BODY_COLOR    = (210, 185, 125)
    PATTERN_COLOR = (48, 42, 28)
    BELLY_COLOR   = (240, 232, 202)

class GroundSnake(Reptile):
    SPECIES       = "ground_snake"
    RARITY        = "common"
    BIOMES        = ["desert", "steppe"]
    BODY_TYPE     = "snake"
    SPEED         = 28.0
    W, H          = 12, 5
    BODY_COLOR    = (160, 130, 80)
    PATTERN_COLOR = (108, 85, 50)
    BELLY_COLOR   = (228, 215, 178)

class LongNoseSnake(Reptile):
    SPECIES       = "long_nose_snake"
    RARITY        = "common"
    BIOMES        = ["desert", "steppe"]
    BODY_TYPE     = "snake"
    SPEED         = 30.0
    W, H          = 16, 5
    BODY_COLOR    = (195, 165, 105)
    PATTERN_COLOR = (45, 38, 25)
    BELLY_COLOR   = (235, 228, 198)

class SandBoa(Reptile):
    SPECIES       = "sand_boa"
    RARITY        = "common"
    BIOMES        = ["desert", "arid_steppe"]
    BODY_TYPE     = "snake"
    SPEED         = 20.0
    W, H          = 15, 7
    BODY_COLOR    = (195, 165, 105)
    PATTERN_COLOR = (120, 95, 55)
    BELLY_COLOR   = (235, 225, 195)

class KenyanSandBoa(Reptile):
    SPECIES       = "kenyan_sand_boa"
    RARITY        = "common"
    BIOMES        = ["desert", "savanna"]
    BODY_TYPE     = "snake"
    SPEED         = 20.0
    W, H          = 15, 7
    BODY_COLOR    = (205, 155, 70)
    PATTERN_COLOR = (42, 35, 22)
    BELLY_COLOR   = (238, 228, 195)

class RubberBoa(Reptile):
    SPECIES       = "rubber_boa"
    RARITY        = "uncommon"
    BIOMES        = ["boreal", "temperate"]
    BODY_TYPE     = "snake"
    SPEED         = 18.0
    W, H          = 14, 7
    BODY_COLOR    = (100, 88, 65)
    PATTERN_COLOR = (70, 60, 42)
    BELLY_COLOR   = (218, 205, 168)

class RosyBoa(Reptile):
    SPECIES       = "rosy_boa"
    RARITY        = "uncommon"
    BIOMES        = ["desert", "rolling_hills"]
    BODY_TYPE     = "snake"
    SPEED         = 18.0
    W, H          = 15, 7
    BODY_COLOR    = (175, 148, 105)
    PATTERN_COLOR = (140, 100, 65)
    BELLY_COLOR   = (232, 222, 195)

class AsianRatSnake(Reptile):
    SPECIES       = "asian_rat_snake"
    RARITY        = "common"
    BIOMES        = ["jungle", "tropical"]
    BODY_TYPE     = "snake"
    SPEED         = 36.0
    W, H          = 18, 6
    BODY_COLOR    = (60, 90, 50)
    PATTERN_COLOR = (42, 65, 34)
    BELLY_COLOR   = (200, 222, 172)

class RadiatedRatSnake(Reptile):
    SPECIES       = "radiated_rat_snake"
    RARITY        = "common"
    BIOMES        = ["jungle", "tropical"]
    BODY_TYPE     = "snake"
    SPEED         = 38.0
    W, H          = 18, 6
    BODY_COLOR    = (55, 85, 48)
    PATTERN_COLOR = (215, 210, 80)
    BELLY_COLOR   = (202, 225, 172)

class BlackRatSnake(Reptile):
    SPECIES       = "black_rat_snake"
    RARITY        = "common"
    BIOMES        = ["temperate", "boreal"]
    BODY_TYPE     = "snake"
    SPEED         = 34.0
    W, H          = 20, 7
    BODY_COLOR    = (28, 25, 20)
    PATTERN_COLOR = (48, 44, 36)
    BELLY_COLOR   = (205, 198, 175)

class TexasRatSnake(Reptile):
    SPECIES       = "texas_rat_snake"
    RARITY        = "common"
    BIOMES        = ["temperate", "steppe"]
    BODY_TYPE     = "snake"
    SPEED         = 34.0
    W, H          = 20, 7
    BODY_COLOR    = (85, 80, 52)
    PATTERN_COLOR = (48, 44, 28)
    BELLY_COLOR   = (208, 200, 165)

class YellowRatSnake(Reptile):
    SPECIES       = "yellow_rat_snake"
    RARITY        = "common"
    BIOMES        = ["temperate", "tropical"]
    BODY_TYPE     = "snake"
    SPEED         = 34.0
    W, H          = 20, 7
    BODY_COLOR    = (195, 182, 80)
    PATTERN_COLOR = (140, 128, 52)
    BELLY_COLOR   = (230, 225, 175)

class BairdsRatSnake(Reptile):
    SPECIES       = "bairds_rat_snake"
    RARITY        = "uncommon"
    BIOMES        = ["desert", "canyon"]
    BODY_TYPE     = "snake"
    SPEED         = 32.0
    W, H          = 18, 7
    BODY_COLOR    = (165, 128, 75)
    PATTERN_COLOR = (115, 85, 48)
    BELLY_COLOR   = (228, 215, 178)

class TransPecosRatSnake(Reptile):
    SPECIES       = "trans_pecos_rat_snake"
    RARITY        = "rare"
    BIOMES        = ["desert", "canyon"]
    BODY_TYPE     = "snake"
    SPEED         = 30.0
    W, H          = 18, 7
    BODY_COLOR    = (185, 168, 105)
    PATTERN_COLOR = (52, 48, 32)
    BELLY_COLOR   = (232, 225, 192)

class FoxSnake(Reptile):
    SPECIES       = "fox_snake"
    RARITY        = "common"
    BIOMES        = ["temperate", "steppe"]
    BODY_TYPE     = "snake"
    SPEED         = 32.0
    W, H          = 18, 6
    BODY_COLOR    = (175, 148, 88)
    PATTERN_COLOR = (115, 90, 52)
    BELLY_COLOR   = (228, 218, 178)

class GreatPlainsRatSnake(Reptile):
    SPECIES       = "great_plains_rat_snake"
    RARITY        = "common"
    BIOMES        = ["steppe", "temperate"]
    BODY_TYPE     = "snake"
    SPEED         = 30.0
    W, H          = 18, 6
    BODY_COLOR    = (175, 152, 95)
    PATTERN_COLOR = (118, 98, 58)
    BELLY_COLOR   = (230, 218, 182)

class AesculapianSnake(Reptile):
    SPECIES       = "aesculapian_snake"
    RARITY        = "uncommon"
    BIOMES        = ["temperate", "mediterranean"]
    BODY_TYPE     = "snake"
    SPEED         = 34.0
    W, H          = 20, 6
    BODY_COLOR    = (75, 82, 55)
    PATTERN_COLOR = (52, 58, 36)
    BELLY_COLOR   = (210, 218, 178)

class FourLinedSnake(Reptile):
    SPECIES       = "four_lined_snake"
    RARITY        = "uncommon"
    BIOMES        = ["temperate", "mediterranean"]
    BODY_TYPE     = "snake"
    SPEED         = 34.0
    W, H          = 20, 7
    BODY_COLOR    = (165, 145, 90)
    PATTERN_COLOR = (48, 45, 28)
    BELLY_COLOR   = (228, 220, 182)

class LadderSnake(Reptile):
    SPECIES       = "ladder_snake"
    RARITY        = "common"
    BIOMES        = ["mediterranean", "temperate"]
    BODY_TYPE     = "snake"
    SPEED         = 32.0
    W, H          = 18, 6
    BODY_COLOR    = (158, 135, 85)
    PATTERN_COLOR = (100, 80, 48)
    BELLY_COLOR   = (228, 215, 178)

class MontpellierSnake(Reptile):
    SPECIES       = "montpellier_snake"
    RARITY        = "uncommon"
    BIOMES        = ["mediterranean", "desert"]
    BODY_TYPE     = "snake"
    SPEED         = 40.0
    W, H          = 20, 6
    BODY_COLOR    = (85, 95, 62)
    PATTERN_COLOR = (58, 68, 40)
    BELLY_COLOR   = (215, 225, 182)

class HorseshoeWhipSnake(Reptile):
    SPECIES       = "horseshoe_whip_snake"
    RARITY        = "uncommon"
    BIOMES        = ["mediterranean", "rolling_hills"]
    BODY_TYPE     = "snake"
    SPEED         = 42.0
    W, H          = 18, 5
    BODY_COLOR    = (65, 80, 52)
    PATTERN_COLOR = (42, 55, 32)
    BELLY_COLOR   = (208, 220, 175)

class DiceSnake(Reptile):
    SPECIES       = "dice_snake"
    RARITY        = "common"
    BIOMES        = ["wetland", "temperate"]
    BODY_TYPE     = "snake"
    SPEED         = 30.0
    W, H          = 16, 6
    BODY_COLOR    = (72, 80, 55)
    PATTERN_COLOR = (48, 55, 34)
    BELLY_COLOR   = (205, 215, 172)

class GrassSnake(Reptile):
    SPECIES       = "grass_snake"
    RARITY        = "common"
    BIOMES        = ["temperate", "wetland"]
    BODY_TYPE     = "snake"
    SPEED         = 32.0
    W, H          = 17, 6
    BODY_COLOR    = (65, 95, 52)
    PATTERN_COLOR = (240, 230, 60)
    BELLY_COLOR   = (208, 218, 175)

class SmoothSnake(Reptile):
    SPECIES       = "smooth_snake"
    RARITY        = "common"
    BIOMES        = ["temperate", "rolling_hills"]
    BODY_TYPE     = "snake"
    SPEED         = 28.0
    W, H          = 15, 5
    BODY_COLOR    = (115, 100, 68)
    PATTERN_COLOR = (78, 65, 42)
    BELLY_COLOR   = (215, 205, 172)

class VipBerus(Reptile):
    SPECIES       = "viper_berus"
    RARITY        = "uncommon"
    BIOMES        = ["temperate", "boreal"]
    BODY_TYPE     = "snake"
    SPEED         = 26.0
    W, H          = 16, 7
    SPOOK_RADIUS  = 6
    BODY_COLOR    = (130, 120, 80)
    PATTERN_COLOR = (45, 40, 25)
    BELLY_COLOR   = (218, 208, 175)

class AspiViper(Reptile):
    SPECIES       = "aspic_viper"
    RARITY        = "uncommon"
    BIOMES        = ["mediterranean", "rolling_hills"]
    BODY_TYPE     = "snake"
    SPEED         = 24.0
    W, H          = 15, 7
    BODY_COLOR    = (155, 132, 82)
    PATTERN_COLOR = (100, 80, 48)
    BELLY_COLOR   = (222, 212, 178)

class LongNosedViper(Reptile):
    SPECIES       = "long_nosed_viper"
    RARITY        = "uncommon"
    BIOMES        = ["mediterranean", "canyon"]
    BODY_TYPE     = "snake"
    SPEED         = 24.0
    W, H          = 16, 7
    BODY_COLOR    = (118, 108, 72)
    PATTERN_COLOR = (78, 68, 44)
    BELLY_COLOR   = (218, 210, 175)

class OrnateFlightSnake(Reptile):
    SPECIES       = "ornate_flying_snake"
    RARITY        = "rare"
    BIOMES        = ["jungle", "south_asian"]
    BODY_TYPE     = "snake"
    SPEED         = 44.0
    W, H          = 18, 5
    BODY_COLOR    = (48, 155, 65)
    PATTERN_COLOR = (195, 65, 48)
    BELLY_COLOR   = (198, 238, 182)

class TweedleSnake(Reptile):
    SPECIES       = "tentacled_snake"
    RARITY        = "rare"
    BIOMES        = ["wetland", "east_asian"]
    BODY_TYPE     = "snake"
    SPEED         = 22.0
    W, H          = 16, 7
    BODY_COLOR    = (68, 80, 58)
    PATTERN_COLOR = (48, 58, 40)
    BELLY_COLOR   = (200, 215, 168)

class SunbeamSnake(Reptile):
    SPECIES       = "sunbeam_snake"
    RARITY        = "rare"
    BIOMES        = ["jungle", "east_asian"]
    BODY_TYPE     = "snake"
    SPEED         = 24.0
    W, H          = 18, 7
    BODY_COLOR    = (55, 50, 38)
    PATTERN_COLOR = (175, 165, 145)
    BELLY_COLOR   = (215, 210, 192)

class BrownTreeSnake(Reptile):
    SPECIES       = "brown_tree_snake"
    RARITY        = "uncommon"
    BIOMES        = ["tropical", "jungle"]
    BODY_TYPE     = "snake"
    SPEED         = 30.0
    W, H          = 17, 6
    BODY_COLOR    = (145, 115, 68)
    PATTERN_COLOR = (98, 75, 42)
    BELLY_COLOR   = (225, 215, 178)

class WesternShovelNose(Reptile):
    SPECIES       = "western_shovel_nose"
    RARITY        = "common"
    BIOMES        = ["desert", "arid_steppe"]
    BODY_TYPE     = "snake"
    SPEED         = 32.0
    W, H          = 13, 5
    BODY_COLOR    = (208, 182, 122)
    PATTERN_COLOR = (42, 36, 22)
    BELLY_COLOR   = (242, 235, 205)

class StripedRacerSnake(Reptile):
    SPECIES       = "striped_racer"
    RARITY        = "common"
    BIOMES        = ["rolling_hills", "temperate"]
    BODY_TYPE     = "snake"
    SPEED         = 42.0
    W, H          = 17, 5
    BODY_COLOR    = (50, 45, 32)
    PATTERN_COLOR = (215, 200, 80)
    BELLY_COLOR   = (205, 218, 172)

class EasternRacerSnake(Reptile):
    SPECIES       = "eastern_racer"
    RARITY        = "common"
    BIOMES        = ["temperate", "steppe"]
    BODY_TYPE     = "snake"
    SPEED         = 44.0
    W, H          = 17, 5
    BODY_COLOR    = (38, 42, 28)
    PATTERN_COLOR = (55, 60, 40)
    BELLY_COLOR   = (200, 215, 168)

class CoachwhipSnake(Reptile):
    SPECIES       = "coachwhip"
    RARITY        = "common"
    BIOMES        = ["desert", "steppe"]
    BODY_TYPE     = "snake"
    SPEED         = 46.0
    W, H          = 18, 5
    BODY_COLOR    = (52, 45, 30)
    PATTERN_COLOR = (168, 148, 95)
    BELLY_COLOR   = (218, 208, 172)


# ---------------------------------------------------------------------------
# Lizards — additional 45 species
# ---------------------------------------------------------------------------

class LeopardGecko(Reptile):
    SPECIES       = "leopard_gecko"
    RARITY        = "common"
    BIOMES        = ["desert", "canyon"]
    BODY_TYPE     = "lizard"
    SPEED         = 35.0
    W, H          = 14, 7
    BODY_COLOR    = (210, 185, 110)
    PATTERN_COLOR = (50, 45, 35)
    BELLY_COLOR   = (240, 235, 210)

class CrestedGecko(Reptile):
    SPECIES       = "crested_gecko"
    RARITY        = "common"
    BIOMES        = ["tropical", "jungle"]
    BODY_TYPE     = "lizard"
    SPEED         = 38.0
    W, H          = 14, 8
    BODY_COLOR    = (100, 130, 75)
    PATTERN_COLOR = (155, 185, 115)
    BELLY_COLOR   = (205, 220, 175)

class DayGecko(Reptile):
    SPECIES       = "day_gecko"
    RARITY        = "common"
    BIOMES        = ["tropical"]
    BODY_TYPE     = "lizard"
    SPEED         = 42.0
    W, H          = 12, 6
    BODY_COLOR    = (60, 185, 75)
    PATTERN_COLOR = (200, 55, 45)
    BELLY_COLOR   = (195, 235, 175)

class TokayGecko(Reptile):
    SPECIES       = "tokay_gecko"
    RARITY        = "uncommon"
    BIOMES        = ["jungle", "tropical"]
    BODY_TYPE     = "lizard"
    SPEED         = 45.0
    W, H          = 16, 8
    BODY_COLOR    = (65, 85, 135)
    PATTERN_COLOR = (210, 80, 60)
    BELLY_COLOR   = (185, 200, 225)

class GroundGecko(Reptile):
    SPECIES       = "ground_gecko"
    RARITY        = "common"
    BIOMES        = ["desert"]
    BODY_TYPE     = "lizard"
    SPEED         = 40.0
    W, H          = 12, 6
    BODY_COLOR    = (200, 175, 120)
    PATTERN_COLOR = (150, 125, 80)
    BELLY_COLOR   = (235, 225, 195)

class CommonWallLizard(Reptile):
    SPECIES       = "common_wall_lizard"
    RARITY        = "common"
    BIOMES        = ["temperate"]
    BODY_TYPE     = "lizard"
    SPEED         = 40.0
    W, H          = 14, 6
    BODY_COLOR    = (100, 110, 75)
    PATTERN_COLOR = (70, 78, 50)
    BELLY_COLOR   = (200, 210, 170)

class SandLizard(Reptile):
    SPECIES       = "sand_lizard"
    RARITY        = "common"
    BIOMES        = ["desert", "temperate"]
    BODY_TYPE     = "lizard"
    SPEED         = 38.0
    W, H          = 14, 6
    BODY_COLOR    = (170, 150, 95)
    PATTERN_COLOR = (120, 100, 58)
    BELLY_COLOR   = (225, 215, 180)

class GreenAnole(Reptile):
    SPECIES       = "green_anole"
    RARITY        = "common"
    BIOMES        = ["tropical", "steppe"]
    BODY_TYPE     = "lizard"
    SPEED         = 44.0
    W, H          = 12, 6
    BODY_COLOR    = (70, 175, 75)
    PATTERN_COLOR = (50, 135, 55)
    BELLY_COLOR   = (195, 235, 175)

class BrownAnole(Reptile):
    SPECIES       = "brown_anole"
    RARITY        = "common"
    BIOMES        = ["tropical", "jungle"]
    BODY_TYPE     = "lizard"
    SPEED         = 42.0
    W, H          = 12, 6
    BODY_COLOR    = (130, 100, 65)
    PATTERN_COLOR = (90, 68, 40)
    BELLY_COLOR   = (220, 200, 165)

class GlassLizard(Reptile):
    SPECIES       = "glass_lizard"
    RARITY        = "uncommon"
    BIOMES        = ["temperate", "steppe"]
    BODY_TYPE     = "lizard"
    SPEED         = 32.0
    W, H          = 22, 7
    BODY_COLOR    = (140, 125, 80)
    PATTERN_COLOR = (95, 82, 50)
    BELLY_COLOR   = (225, 215, 180)

class AlligatorLizard(Reptile):
    SPECIES       = "alligator_lizard"
    RARITY        = "common"
    BIOMES        = ["temperate", "rolling_hills"]
    BODY_TYPE     = "lizard"
    SPEED         = 30.0
    W, H          = 18, 7
    BODY_COLOR    = (110, 100, 65)
    PATTERN_COLOR = (75, 65, 40)
    BELLY_COLOR   = (215, 205, 170)

class WhiptailLizard(Reptile):
    SPECIES       = "whiptail_lizard"
    RARITY        = "common"
    BIOMES        = ["desert", "steppe"]
    BODY_TYPE     = "lizard"
    SPEED         = 48.0
    W, H          = 16, 6
    BODY_COLOR    = (140, 120, 70)
    PATTERN_COLOR = (95, 78, 42)
    BELLY_COLOR   = (225, 215, 180)

class CollaredLizard(Reptile):
    SPECIES       = "collared_lizard"
    RARITY        = "uncommon"
    BIOMES        = ["desert", "canyon"]
    BODY_TYPE     = "lizard"
    SPEED         = 42.0
    W, H          = 16, 8
    BODY_COLOR    = (75, 155, 80)
    PATTERN_COLOR = (35, 32, 28)
    BELLY_COLOR   = (200, 230, 175)

class SpinyLizard(Reptile):
    SPECIES       = "spiny_lizard"
    RARITY        = "common"
    BIOMES        = ["desert", "canyon"]
    BODY_TYPE     = "lizard"
    SPEED         = 35.0
    W, H          = 15, 8
    BODY_COLOR    = (160, 135, 85)
    PATTERN_COLOR = (110, 88, 52)
    BELLY_COLOR   = (225, 210, 175)

class EasternFenceLizard(Reptile):
    SPECIES       = "eastern_fence_lizard"
    RARITY        = "common"
    BIOMES        = ["temperate", "boreal"]
    BODY_TYPE     = "lizard"
    SPEED         = 36.0
    W, H          = 14, 7
    BODY_COLOR    = (110, 105, 70)
    PATTERN_COLOR = (72, 68, 44)
    BELLY_COLOR   = (210, 205, 170)

class WesternFenceLizard(Reptile):
    SPECIES       = "western_fence_lizard"
    RARITY        = "common"
    BIOMES        = ["temperate", "rolling_hills"]
    BODY_TYPE     = "lizard"
    SPEED         = 36.0
    W, H          = 14, 7
    BODY_COLOR    = (105, 100, 65)
    PATTERN_COLOR = (68, 62, 38)
    BELLY_COLOR   = (165, 210, 190)

class DesertIguana(Reptile):
    SPECIES       = "desert_iguana"
    RARITY        = "uncommon"
    BIOMES        = ["desert"]
    BODY_TYPE     = "lizard"
    SPEED         = 32.0
    W, H          = 18, 9
    BODY_COLOR    = (190, 170, 125)
    PATTERN_COLOR = (145, 125, 85)
    BELLY_COLOR   = (235, 225, 195)

class MarineIguana(Reptile):
    SPECIES       = "marine_iguana"
    RARITY        = "rare"
    BIOMES        = ["beach"]
    BODY_TYPE     = "lizard"
    SPEED         = 22.0
    W, H          = 20, 11
    BODY_COLOR    = (40, 40, 42)
    PATTERN_COLOR = (65, 60, 62)
    BELLY_COLOR   = (170, 165, 165)

class RhinocerosIguana(Reptile):
    SPECIES       = "rhinoceros_iguana"
    RARITY        = "rare"
    BIOMES        = ["tropical"]
    BODY_TYPE     = "lizard"
    SPEED         = 25.0
    W, H          = 22, 12
    SPOOK_RADIUS  = 6
    BODY_COLOR    = (70, 75, 65)
    PATTERN_COLOR = (50, 55, 45)
    BELLY_COLOR   = (180, 175, 160)

class Chuckwalla(Reptile):
    SPECIES       = "chuckwalla"
    RARITY        = "uncommon"
    BIOMES        = ["desert", "canyon"]
    BODY_TYPE     = "lizard"
    SPEED         = 25.0
    W, H          = 18, 10
    BODY_COLOR    = (95, 80, 55)
    PATTERN_COLOR = (135, 110, 75)
    BELLY_COLOR   = (205, 190, 155)

class GilaMonster(Reptile):
    SPECIES       = "gila_monster"
    RARITY        = "rare"
    BIOMES        = ["desert"]
    BODY_TYPE     = "lizard"
    SPEED         = 18.0
    PATROL_RANGE  = 36
    W, H          = 18, 10
    SPOOK_RADIUS  = 4
    BODY_COLOR    = (40, 35, 30)
    PATTERN_COLOR = (200, 80, 40)
    BELLY_COLOR   = (195, 175, 145)

class BeadedLizard(Reptile):
    SPECIES       = "beaded_lizard"
    RARITY        = "rare"
    BIOMES        = ["jungle", "tropical"]
    BODY_TYPE     = "lizard"
    SPEED         = 18.0
    PATROL_RANGE  = 36
    W, H          = 20, 11
    SPOOK_RADIUS  = 4
    BODY_COLOR    = (40, 35, 28)
    PATTERN_COLOR = (185, 165, 45)
    BELLY_COLOR   = (195, 180, 145)

class NileMonitor(Reptile):
    SPECIES       = "nile_monitor"
    RARITY        = "uncommon"
    BIOMES        = ["savanna", "wetland"]
    BODY_TYPE     = "lizard"
    SPEED         = 34.0
    W, H          = 24, 11
    BODY_COLOR    = (60, 65, 45)
    PATTERN_COLOR = (145, 145, 75)
    BELLY_COLOR   = (195, 190, 155)

class WaterMonitor(Reptile):
    SPECIES       = "water_monitor"
    RARITY        = "uncommon"
    BIOMES        = ["wetland", "tropical"]
    BODY_TYPE     = "lizard"
    SPEED         = 36.0
    W, H          = 24, 11
    BODY_COLOR    = (50, 60, 42)
    PATTERN_COLOR = (130, 140, 70)
    BELLY_COLOR   = (190, 195, 155)

class BlackWhiteTegu(Reptile):
    SPECIES       = "black_white_tegu"
    RARITY        = "uncommon"
    BIOMES        = ["savanna", "tropical"]
    BODY_TYPE     = "lizard"
    SPEED         = 30.0
    W, H          = 22, 10
    BODY_COLOR    = (30, 28, 25)
    PATTERN_COLOR = (225, 225, 215)
    BELLY_COLOR   = (200, 195, 180)

class FiveLinedSkink(Reptile):
    SPECIES       = "five_lined_skink"
    RARITY        = "common"
    BIOMES        = ["temperate", "boreal"]
    BODY_TYPE     = "lizard"
    SPEED         = 38.0
    W, H          = 14, 6
    BODY_COLOR    = (55, 50, 38)
    PATTERN_COLOR = (215, 200, 80)
    BELLY_COLOR   = (205, 200, 170)

class BroadHeadedSkink(Reptile):
    SPECIES       = "broad_headed_skink"
    RARITY        = "uncommon"
    BIOMES        = ["temperate", "boreal"]
    BODY_TYPE     = "lizard"
    SPEED         = 34.0
    W, H          = 16, 8
    BODY_COLOR    = (70, 62, 44)
    PATTERN_COLOR = (195, 165, 65)
    BELLY_COLOR   = (210, 200, 165)

class Sandfish(Reptile):
    SPECIES       = "sandfish"
    RARITY        = "uncommon"
    BIOMES        = ["desert"]
    BODY_TYPE     = "lizard"
    SPEED         = 30.0
    W, H          = 14, 6
    BODY_COLOR    = (210, 185, 125)
    PATTERN_COLOR = (165, 140, 85)
    BELLY_COLOR   = (238, 230, 200)

class BasiliskLizard(Reptile):
    SPECIES       = "basilisk"
    RARITY        = "uncommon"
    BIOMES        = ["jungle", "tropical"]
    BODY_TYPE     = "lizard"
    SPEED         = 46.0
    W, H          = 18, 10
    BODY_COLOR    = (60, 140, 70)
    PATTERN_COLOR = (42, 100, 50)
    BELLY_COLOR   = (190, 230, 170)

class PlumedBasilisk(Reptile):
    SPECIES       = "plumed_basilisk"
    RARITY        = "rare"
    BIOMES        = ["jungle", "tropical"]
    BODY_TYPE     = "lizard"
    SPEED         = 48.0
    W, H          = 20, 12
    BODY_COLOR    = (48, 155, 72)
    PATTERN_COLOR = (32, 110, 50)
    BELLY_COLOR   = (185, 235, 165)

class TexasHornedLizard(Reptile):
    SPECIES       = "texas_horned_lizard"
    RARITY        = "uncommon"
    BIOMES        = ["desert", "steppe"]
    BODY_TYPE     = "lizard"
    SPEED         = 25.0
    W, H          = 14, 9
    BODY_COLOR    = (185, 155, 100)
    PATTERN_COLOR = (135, 105, 62)
    BELLY_COLOR   = (230, 215, 178)

class GreaterEarlessLizard(Reptile):
    SPECIES       = "greater_earless_lizard"
    RARITY        = "common"
    BIOMES        = ["desert", "steppe"]
    BODY_TYPE     = "lizard"
    SPEED         = 36.0
    W, H          = 14, 6
    BODY_COLOR    = (170, 145, 90)
    PATTERN_COLOR = (120, 95, 55)
    BELLY_COLOR   = (228, 215, 178)

class ChineseWaterDragon(Reptile):
    SPECIES       = "chinese_water_dragon"
    RARITY        = "uncommon"
    BIOMES        = ["jungle", "wetland"]
    BODY_TYPE     = "lizard"
    SPEED         = 38.0
    W, H          = 18, 10
    BODY_COLOR    = (65, 160, 80)
    PATTERN_COLOR = (45, 120, 58)
    BELLY_COLOR   = (185, 235, 170)

class ThornyDevil(Reptile):
    SPECIES       = "thorny_devil"
    RARITY        = "rare"
    BIOMES        = ["desert"]
    BODY_TYPE     = "lizard"
    SPEED         = 20.0
    W, H          = 14, 9
    BODY_COLOR    = (185, 145, 75)
    PATTERN_COLOR = (130, 95, 42)
    BELLY_COLOR   = (230, 210, 168)

class MountainHornedDragon(Reptile):
    SPECIES       = "mountain_horned_dragon"
    RARITY        = "uncommon"
    BIOMES        = ["jungle", "tropical"]
    BODY_TYPE     = "lizard"
    SPEED         = 26.0
    W, H          = 16, 9
    BODY_COLOR    = (70, 105, 65)
    PATTERN_COLOR = (50, 78, 46)
    BELLY_COLOR   = (190, 215, 170)

class PlatedLizard(Reptile):
    SPECIES       = "plated_lizard"
    RARITY        = "common"
    BIOMES        = ["savanna", "steppe"]
    BODY_TYPE     = "lizard"
    SPEED         = 32.0
    W, H          = 16, 7
    BODY_COLOR    = (120, 105, 65)
    PATTERN_COLOR = (80, 68, 40)
    BELLY_COLOR   = (215, 205, 170)

class CamelLizard(Reptile):
    SPECIES       = "camel_lizard"
    RARITY        = "common"
    BIOMES        = ["desert", "wasteland"]
    BODY_TYPE     = "lizard"
    SPEED         = 34.0
    W, H          = 14, 7
    BODY_COLOR    = (195, 170, 115)
    PATTERN_COLOR = (145, 120, 72)
    BELLY_COLOR   = (235, 225, 190)

class CaimanLizard(Reptile):
    SPECIES       = "caiman_lizard"
    RARITY        = "rare"
    BIOMES        = ["wetland", "jungle"]
    BODY_TYPE     = "lizard"
    SPEED         = 28.0
    W, H          = 22, 11
    BODY_COLOR    = (55, 100, 55)
    PATTERN_COLOR = (38, 72, 38)
    BELLY_COLOR   = (185, 195, 155)

class SpiderTailedViper(Reptile):  # ground lizard-like shape used
    SPECIES       = "spider_tailed_viper"
    RARITY        = "rare"
    BIOMES        = ["desert", "canyon"]
    BODY_TYPE     = "snake"
    SPEED         = 22.0
    W, H          = 18, 7
    BODY_COLOR    = (155, 130, 80)
    PATTERN_COLOR = (105, 82, 48)
    BELLY_COLOR   = (225, 210, 172)

class LaceMonitor(Reptile):
    SPECIES       = "lace_monitor"
    RARITY        = "uncommon"
    BIOMES        = ["tropical", "boreal"]
    BODY_TYPE     = "lizard"
    SPEED         = 36.0
    W, H          = 24, 11
    BODY_COLOR    = (38, 38, 30)
    PATTERN_COLOR = (195, 190, 140)
    BELLY_COLOR   = (200, 195, 160)

class ScalySandLizard(Reptile):
    SPECIES       = "scaly_sand_lizard"
    RARITY        = "common"
    BIOMES        = ["desert", "canyon"]
    BODY_TYPE     = "lizard"
    SPEED         = 38.0
    W, H          = 14, 6
    BODY_COLOR    = (200, 175, 120)
    PATTERN_COLOR = (150, 125, 78)
    BELLY_COLOR   = (238, 228, 198)

class CopperSkink(Reptile):
    SPECIES       = "copper_skink"
    RARITY        = "common"
    BIOMES        = ["temperate", "boreal"]
    BODY_TYPE     = "lizard"
    SPEED         = 36.0
    W, H          = 14, 6
    BODY_COLOR    = (175, 115, 55)
    PATTERN_COLOR = (130, 80, 35)
    BELLY_COLOR   = (228, 210, 178)

class BlueTailedSkink(Reptile):
    SPECIES       = "blue_tailed_skink"
    RARITY        = "uncommon"
    BIOMES        = ["tropical", "boreal"]
    BODY_TYPE     = "lizard"
    SPEED         = 38.0
    W, H          = 14, 6
    BODY_COLOR    = (65, 58, 42)
    PATTERN_COLOR = (215, 195, 70)
    BELLY_COLOR   = (90, 160, 215)

class ArmadilloLizard(Reptile):
    SPECIES       = "armadillo_lizard"
    RARITY        = "rare"
    BIOMES        = ["desert", "savanna"]
    BODY_TYPE     = "lizard"
    SPEED         = 22.0
    W, H          = 14, 8
    BODY_COLOR    = (165, 138, 80)
    PATTERN_COLOR = (115, 90, 50)
    BELLY_COLOR   = (225, 210, 172)

class FlatHeadedAgama(Reptile):
    SPECIES       = "flat_headed_agama"
    RARITY        = "common"
    BIOMES        = ["savanna", "steppe"]
    BODY_TYPE     = "lizard"
    SPEED         = 34.0
    W, H          = 14, 6
    BODY_COLOR    = (95, 125, 165)
    PATTERN_COLOR = (68, 95, 130)
    BELLY_COLOR   = (205, 210, 195)


# ---------------------------------------------------------------------------
# Turtles — additional 20 species
# ---------------------------------------------------------------------------

class DesertTortoise(Reptile):
    SPECIES       = "desert_tortoise"
    RARITY        = "uncommon"
    BIOMES        = ["desert"]
    BODY_TYPE     = "turtle"
    SPEED         = 10.0
    PATROL_RANGE  = 28
    W, H          = 14, 10
    BODY_COLOR    = (145, 120, 75)
    PATTERN_COLOR = (195, 170, 110)
    BELLY_COLOR   = (220, 205, 165)

class GopherTortoise(Reptile):
    SPECIES       = "gopher_tortoise"
    RARITY        = "uncommon"
    BIOMES        = ["steppe", "temperate"]
    BODY_TYPE     = "turtle"
    SPEED         = 9.0
    PATROL_RANGE  = 28
    W, H          = 14, 10
    BODY_COLOR    = (110, 90, 58)
    PATTERN_COLOR = (160, 135, 85)
    BELLY_COLOR   = (210, 195, 155)

class SulcataTortoise(Reptile):
    SPECIES       = "sulcata_tortoise"
    RARITY        = "uncommon"
    BIOMES        = ["savanna", "desert"]
    BODY_TYPE     = "turtle"
    SPEED         = 8.0
    PATROL_RANGE  = 24
    W, H          = 16, 11
    BODY_COLOR    = (175, 148, 95)
    PATTERN_COLOR = (225, 200, 140)
    BELLY_COLOR   = (228, 215, 178)

class AldabraGiantTortoise(Reptile):
    SPECIES       = "aldabra_giant_tortoise"
    RARITY        = "rare"
    BIOMES        = ["tropical"]
    BODY_TYPE     = "turtle"
    SPEED         = 6.0
    PATROL_RANGE  = 20
    W, H          = 20, 13
    BODY_COLOR    = (65, 55, 38)
    PATTERN_COLOR = (95, 82, 58)
    BELLY_COLOR   = (185, 175, 145)

class GalapagosTortoise(Reptile):
    SPECIES       = "galapagos_tortoise"
    RARITY        = "rare"
    BIOMES        = ["tropical", "beach"]
    BODY_TYPE     = "turtle"
    SPEED         = 5.0
    PATROL_RANGE  = 18
    W, H          = 22, 14
    BODY_COLOR    = (55, 48, 32)
    PATTERN_COLOR = (82, 72, 50)
    BELLY_COLOR   = (180, 170, 138)

class RedFootedTortoise(Reptile):
    SPECIES       = "red_footed_tortoise"
    RARITY        = "common"
    BIOMES        = ["jungle", "tropical"]
    BODY_TYPE     = "turtle"
    SPEED         = 11.0
    PATROL_RANGE  = 30
    W, H          = 14, 10
    BODY_COLOR    = (55, 48, 32)
    PATTERN_COLOR = (215, 80, 42)
    BELLY_COLOR   = (200, 185, 148)

class RussianTortoise(Reptile):
    SPECIES       = "russian_tortoise"
    RARITY        = "common"
    BIOMES        = ["temperate", "desert"]
    BODY_TYPE     = "turtle"
    SPEED         = 10.0
    PATROL_RANGE  = 28
    W, H          = 12, 9
    BODY_COLOR    = (130, 110, 70)
    PATTERN_COLOR = (80, 65, 38)
    BELLY_COLOR   = (210, 198, 162)

class HermannsTortoise(Reptile):
    SPECIES       = "hermanns_tortoise"
    RARITY        = "common"
    BIOMES        = ["temperate"]
    BODY_TYPE     = "turtle"
    SPEED         = 10.0
    PATROL_RANGE  = 28
    W, H          = 12, 9
    BODY_COLOR    = (100, 82, 48)
    PATTERN_COLOR = (210, 185, 85)
    BELLY_COLOR   = (215, 202, 165)

class StarTortoise(Reptile):
    SPECIES       = "star_tortoise"
    RARITY        = "uncommon"
    BIOMES        = ["tropical", "savanna"]
    BODY_TYPE     = "turtle"
    SPEED         = 9.0
    PATROL_RANGE  = 26
    W, H          = 13, 10
    BODY_COLOR    = (28, 25, 18)
    PATTERN_COLOR = (215, 195, 95)
    BELLY_COLOR   = (205, 190, 148)

class MapTurtle(Reptile):
    SPECIES       = "map_turtle"
    RARITY        = "common"
    BIOMES        = ["wetland", "temperate"]
    BODY_TYPE     = "turtle"
    SPEED         = 11.0
    PATROL_RANGE  = 32
    W, H          = 13, 9
    BODY_COLOR    = (50, 60, 38)
    PATTERN_COLOR = (155, 175, 75)
    BELLY_COLOR   = (210, 200, 148)

class SpottedTurtle(Reptile):
    SPECIES       = "spotted_turtle"
    RARITY        = "common"
    BIOMES        = ["wetland", "temperate"]
    BODY_TYPE     = "turtle"
    SPEED         = 11.0
    PATROL_RANGE  = 30
    W, H          = 12, 9
    BODY_COLOR    = (28, 28, 22)
    PATTERN_COLOR = (235, 220, 70)
    BELLY_COLOR   = (200, 190, 145)

class BlandingsTurtle(Reptile):
    SPECIES       = "blandings_turtle"
    RARITY        = "uncommon"
    BIOMES        = ["wetland"]
    BODY_TYPE     = "turtle"
    SPEED         = 10.0
    PATROL_RANGE  = 30
    W, H          = 14, 10
    BODY_COLOR    = (35, 35, 28)
    PATTERN_COLOR = (200, 190, 80)
    BELLY_COLOR   = (225, 215, 100)

class WoodTurtle(Reptile):
    SPECIES       = "wood_turtle"
    RARITY        = "uncommon"
    BIOMES        = ["temperate", "boreal"]
    BODY_TYPE     = "turtle"
    SPEED         = 10.0
    PATROL_RANGE  = 30
    W, H          = 13, 9
    BODY_COLOR    = (90, 72, 42)
    PATTERN_COLOR = (145, 118, 68)
    BELLY_COLOR   = (210, 195, 155)

class BogTurtle(Reptile):
    SPECIES       = "bog_turtle"
    RARITY        = "rare"
    BIOMES        = ["wetland", "swamp"]
    BODY_TYPE     = "turtle"
    SPEED         = 9.0
    PATROL_RANGE  = 24
    W, H          = 11, 8
    BODY_COLOR    = (42, 38, 28)
    PATTERN_COLOR = (200, 120, 50)
    BELLY_COLOR   = (195, 180, 138)

class PondSlider(Reptile):
    SPECIES       = "pond_slider"
    RARITY        = "common"
    BIOMES        = ["wetland", "temperate"]
    BODY_TYPE     = "turtle"
    SPEED         = 12.0
    PATROL_RANGE  = 34
    W, H          = 13, 9
    BODY_COLOR    = (50, 62, 38)
    PATTERN_COLOR = (110, 155, 75)
    BELLY_COLOR   = (210, 205, 148)

class RedEaredSlider(Reptile):
    SPECIES       = "red_eared_slider"
    RARITY        = "common"
    BIOMES        = ["wetland"]
    BODY_TYPE     = "turtle"
    SPEED         = 13.0
    PATROL_RANGE  = 34
    W, H          = 13, 9
    BODY_COLOR    = (48, 60, 36)
    PATTERN_COLOR = (205, 55, 45)
    BELLY_COLOR   = (210, 202, 148)

class MudTurtle(Reptile):
    SPECIES       = "mud_turtle"
    RARITY        = "common"
    BIOMES        = ["swamp", "wetland"]
    BODY_TYPE     = "turtle"
    SPEED         = 9.0
    PATROL_RANGE  = 26
    W, H          = 11, 8
    BODY_COLOR    = (55, 48, 32)
    PATTERN_COLOR = (85, 75, 52)
    BELLY_COLOR   = (185, 175, 138)

class MuskTurtle(Reptile):
    SPECIES       = "musk_turtle"
    RARITY        = "common"
    BIOMES        = ["swamp", "wetland"]
    BODY_TYPE     = "turtle"
    SPEED         = 8.0
    PATROL_RANGE  = 24
    W, H          = 11, 8
    BODY_COLOR    = (50, 45, 30)
    PATTERN_COLOR = (80, 72, 50)
    BELLY_COLOR   = (182, 172, 135)

class SoftshellTurtle(Reptile):
    SPECIES       = "softshell_turtle"
    RARITY        = "uncommon"
    BIOMES        = ["wetland", "temperate"]
    BODY_TYPE     = "turtle"
    SPEED         = 14.0
    PATROL_RANGE  = 36
    W, H          = 16, 10
    BODY_COLOR    = (105, 115, 78)
    PATTERN_COLOR = (75, 85, 55)
    BELLY_COLOR   = (205, 215, 175)

class FlatbackTurtle(Reptile):
    SPECIES       = "flatback_turtle"
    RARITY        = "rare"
    BIOMES        = ["beach"]
    BODY_TYPE     = "turtle"
    SPEED         = 8.0
    PATROL_RANGE  = 30
    W, H          = 18, 11
    BODY_COLOR    = (95, 110, 78)
    PATTERN_COLOR = (130, 148, 108)
    BELLY_COLOR   = (215, 222, 188)


# ---------------------------------------------------------------------------
# Frogs (25)
# ---------------------------------------------------------------------------

class CommonFrog(Reptile):
    SPECIES       = "common_frog"
    RARITY        = "common"
    BIOMES        = ["temperate", "wetland"]
    BODY_TYPE     = "frog"
    SPEED         = 50.0
    PATROL_RANGE  = 40
    W, H          = 12, 9
    BODY_COLOR    = (80, 115, 55)
    PATTERN_COLOR = (55, 80, 35)
    BELLY_COLOR   = (210, 225, 185)

class AmericanBullfrog(Reptile):
    SPECIES       = "american_bullfrog"
    RARITY        = "common"
    BIOMES        = ["wetland", "temperate"]
    BODY_TYPE     = "frog"
    SPEED         = 55.0
    PATROL_RANGE  = 44
    W, H          = 16, 12
    BODY_COLOR    = (65, 110, 50)
    PATTERN_COLOR = (45, 78, 32)
    BELLY_COLOR   = (215, 230, 185)

class WoodFrog(Reptile):
    SPECIES       = "wood_frog"
    RARITY        = "common"
    BIOMES        = ["boreal", "temperate"]
    BODY_TYPE     = "frog"
    SPEED         = 48.0
    PATROL_RANGE  = 38
    W, H          = 12, 9
    BODY_COLOR    = (130, 90, 55)
    PATTERN_COLOR = (90, 58, 30)
    BELLY_COLOR   = (220, 210, 175)

class SpringPeeper(Reptile):
    SPECIES       = "spring_peeper"
    RARITY        = "common"
    BIOMES        = ["wetland", "boreal"]
    BODY_TYPE     = "frog"
    SPEED         = 52.0
    PATROL_RANGE  = 36
    W, H          = 8, 6
    BODY_COLOR    = (120, 90, 55)
    PATTERN_COLOR = (80, 58, 32)
    BELLY_COLOR   = (215, 210, 180)

class LeopardFrog(Reptile):
    SPECIES       = "leopard_frog"
    RARITY        = "common"
    BIOMES        = ["wetland", "steppe"]
    BODY_TYPE     = "frog"
    SPEED         = 55.0
    PATROL_RANGE  = 44
    W, H          = 13, 10
    BODY_COLOR    = (70, 120, 55)
    PATTERN_COLOR = (45, 80, 32)
    BELLY_COLOR   = (218, 230, 188)

class PickerelFrog(Reptile):
    SPECIES       = "pickerel_frog"
    RARITY        = "common"
    BIOMES        = ["wetland", "temperate"]
    BODY_TYPE     = "frog"
    SPEED         = 50.0
    PATROL_RANGE  = 40
    W, H          = 12, 9
    BODY_COLOR    = (100, 115, 65)
    PATTERN_COLOR = (65, 78, 40)
    BELLY_COLOR   = (215, 228, 185)

class GrayTreeFrog(Reptile):
    SPECIES       = "gray_tree_frog"
    RARITY        = "common"
    BIOMES        = ["temperate", "boreal"]
    BODY_TYPE     = "frog"
    SPEED         = 46.0
    PATROL_RANGE  = 36
    W, H          = 11, 8
    BODY_COLOR    = (155, 155, 140)
    PATTERN_COLOR = (105, 105, 88)
    BELLY_COLOR   = (220, 218, 205)

class GreenTreeFrog(Reptile):
    SPECIES       = "green_tree_frog"
    RARITY        = "common"
    BIOMES        = ["wetland", "tropical"]
    BODY_TYPE     = "frog"
    SPEED         = 48.0
    PATROL_RANGE  = 38
    W, H          = 10, 8
    BODY_COLOR    = (80, 185, 85)
    PATTERN_COLOR = (55, 140, 60)
    BELLY_COLOR   = (210, 235, 185)

class PacificTreeFrog(Reptile):
    SPECIES       = "pacific_tree_frog"
    RARITY        = "common"
    BIOMES        = ["temperate", "rolling_hills"]
    BODY_TYPE     = "frog"
    SPEED         = 46.0
    PATROL_RANGE  = 36
    W, H          = 9, 7
    BODY_COLOR    = (80, 160, 70)
    PATTERN_COLOR = (55, 115, 46)
    BELLY_COLOR   = (212, 232, 182)

class RedEyedTreeFrog(Reptile):
    SPECIES       = "red_eyed_tree_frog"
    RARITY        = "uncommon"
    BIOMES        = ["jungle", "tropical"]
    BODY_TYPE     = "frog"
    SPEED         = 44.0
    PATROL_RANGE  = 36
    W, H          = 12, 9
    BODY_COLOR    = (60, 175, 70)
    PATTERN_COLOR = (42, 130, 50)
    BELLY_COLOR   = (215, 235, 175)

class PoisonDartFrog(Reptile):
    SPECIES       = "poison_dart_frog"
    RARITY        = "uncommon"
    BIOMES        = ["jungle", "tropical"]
    BODY_TYPE     = "frog"
    SPEED         = 40.0
    PATROL_RANGE  = 32
    W, H          = 9, 7
    BODY_COLOR    = (55, 130, 215)
    PATTERN_COLOR = (30, 80, 165)
    BELLY_COLOR   = (180, 210, 245)

class StrawberryPoisonFrog(Reptile):
    SPECIES       = "strawberry_poison_frog"
    RARITY        = "uncommon"
    BIOMES        = ["jungle", "tropical"]
    BODY_TYPE     = "frog"
    SPEED         = 40.0
    PATROL_RANGE  = 32
    W, H          = 8, 6
    BODY_COLOR    = (215, 48, 42)
    PATTERN_COLOR = (165, 28, 22)
    BELLY_COLOR   = (235, 155, 145)

class GoldenPoisonFrog(Reptile):
    SPECIES       = "golden_poison_frog"
    RARITY        = "rare"
    BIOMES        = ["jungle"]
    BODY_TYPE     = "frog"
    SPEED         = 38.0
    PATROL_RANGE  = 30
    W, H          = 9, 7
    BODY_COLOR    = (220, 190, 40)
    PATTERN_COLOR = (175, 148, 22)
    BELLY_COLOR   = (240, 225, 155)

class TomatoFrog(Reptile):
    SPECIES       = "tomato_frog"
    RARITY        = "uncommon"
    BIOMES        = ["tropical", "jungle"]
    BODY_TYPE     = "frog"
    SPEED         = 35.0
    PATROL_RANGE  = 28
    W, H          = 13, 10
    BODY_COLOR    = (215, 75, 42)
    PATTERN_COLOR = (170, 48, 22)
    BELLY_COLOR   = (240, 195, 165)

class GoliathFrog(Reptile):
    SPECIES       = "goliath_frog"
    RARITY        = "rare"
    BIOMES        = ["jungle", "wetland"]
    BODY_TYPE     = "frog"
    SPEED         = 45.0
    PATROL_RANGE  = 40
    W, H          = 20, 15
    BODY_COLOR    = (55, 100, 48)
    PATTERN_COLOR = (35, 70, 28)
    BELLY_COLOR   = (200, 225, 175)

class AfricanClawedFrog(Reptile):
    SPECIES       = "african_clawed_frog"
    RARITY        = "common"
    BIOMES        = ["wetland", "savanna"]
    BODY_TYPE     = "frog"
    SPEED         = 42.0
    PATROL_RANGE  = 36
    W, H          = 13, 9
    BODY_COLOR    = (100, 100, 75)
    PATTERN_COLOR = (68, 68, 50)
    BELLY_COLOR   = (210, 210, 185)

class RainFrog(Reptile):
    SPECIES       = "rain_frog"
    RARITY        = "common"
    BIOMES        = ["savanna", "tropical"]
    BODY_TYPE     = "frog"
    SPEED         = 35.0
    PATROL_RANGE  = 28
    W, H          = 10, 8
    BODY_COLOR    = (130, 115, 75)
    PATTERN_COLOR = (88, 78, 48)
    BELLY_COLOR   = (220, 215, 185)

class DesertRainFrog(Reptile):
    SPECIES       = "desert_rain_frog"
    RARITY        = "uncommon"
    BIOMES        = ["desert", "arid_steppe"]
    BODY_TYPE     = "frog"
    SPEED         = 32.0
    PATROL_RANGE  = 26
    W, H          = 11, 9
    BODY_COLOR    = (195, 165, 110)
    PATTERN_COLOR = (148, 118, 72)
    BELLY_COLOR   = (235, 225, 195)

class AustralianGreenTreeFrog(Reptile):
    SPECIES       = "australian_green_tree_frog"
    RARITY        = "common"
    BIOMES        = ["tropical", "wetland"]
    BODY_TYPE     = "frog"
    SPEED         = 44.0
    PATROL_RANGE  = 36
    W, H          = 13, 10
    BODY_COLOR    = (75, 185, 80)
    PATTERN_COLOR = (50, 140, 55)
    BELLY_COLOR   = (210, 238, 185)

class WaxyTreeFrog(Reptile):
    SPECIES       = "waxy_tree_frog"
    RARITY        = "uncommon"
    BIOMES        = ["savanna", "tropical"]
    BODY_TYPE     = "frog"
    SPEED         = 42.0
    PATROL_RANGE  = 34
    W, H          = 10, 8
    BODY_COLOR    = (65, 155, 75)
    PATTERN_COLOR = (44, 110, 52)
    BELLY_COLOR   = (210, 232, 180)

class GlassFrog(Reptile):
    SPECIES       = "glass_frog"
    RARITY        = "rare"
    BIOMES        = ["jungle", "tropical"]
    BODY_TYPE     = "frog"
    SPEED         = 38.0
    PATROL_RANGE  = 30
    W, H          = 9, 7
    BODY_COLOR    = (120, 210, 105)
    PATTERN_COLOR = (85, 168, 72)
    BELLY_COLOR   = (195, 240, 185)

class HairyFrog(Reptile):
    SPECIES       = "hairy_frog"
    RARITY        = "rare"
    BIOMES        = ["jungle", "wetland"]
    BODY_TYPE     = "frog"
    SPEED         = 42.0
    PATROL_RANGE  = 32
    W, H          = 13, 10
    BODY_COLOR    = (60, 75, 45)
    PATTERN_COLOR = (40, 52, 28)
    BELLY_COLOR   = (195, 210, 165)

class FlyingFrog(Reptile):
    SPECIES       = "flying_frog"
    RARITY        = "rare"
    BIOMES        = ["jungle", "tropical"]
    BODY_TYPE     = "frog"
    SPEED         = 50.0
    PATROL_RANGE  = 44
    W, H          = 12, 9
    BODY_COLOR    = (60, 170, 72)
    PATTERN_COLOR = (40, 125, 50)
    BELLY_COLOR   = (190, 235, 172)

class FirebellyToad(Reptile):
    SPECIES       = "firebelly_toad"
    RARITY        = "uncommon"
    BIOMES        = ["wetland", "boreal"]
    BODY_TYPE     = "frog"
    SPEED         = 36.0
    PATROL_RANGE  = 30
    W, H          = 11, 8
    BODY_COLOR    = (55, 80, 45)
    PATTERN_COLOR = (38, 55, 28)
    BELLY_COLOR   = (215, 65, 42)

class SpadeFootToad(Reptile):
    SPECIES       = "spadefoot_toad"
    RARITY        = "uncommon"
    BIOMES        = ["desert", "steppe"]
    BODY_TYPE     = "frog"
    SPEED         = 38.0
    PATROL_RANGE  = 32
    W, H          = 12, 9
    BODY_COLOR    = (140, 120, 72)
    PATTERN_COLOR = (95, 80, 46)
    BELLY_COLOR   = (225, 215, 180)


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

ALL_REPTILE_SPECIES = [
    # Snakes (original 7)
    CornSnake, GarterSnake, MilkSnake,
    Rattlesnake, EmeraldTreeBoa,
    KingCobra, BlackMamba,
    # Snakes (additional 35)
    BallPython, BoaConstrictor, ReticulatedPython, Anaconda,
    WesternHognose, BullSnake, RingNeckedSnake, SmoothGreenSnake,
    EasternHognose, PineSnake, Copperhead, Cottonmouth,
    TimberRattlesnake, Sidewinder, WesternDiamondback,
    EasternCoralSnake, WesternCoralSnake, ScarletKingsnake,
    IndigoSnake, CapeCobra, PuffAdder, GaboonViper, Boomslang,
    VineSnake, FlyingSnake, MangroveSnake, TigerSnake,
    Taipan, InlandTaipan, DeathAdder, RedBelliedBlackSnake,
    GreenMamba, AsianPitViper, RoughScaledSnake, ScalelessCornSnake,
    SpiderTailedViper,
    # Snakes (additional 50)
    AfricanRockPython, BurmesePython, GreenTreePython, ChildrensPython,
    WomaPython, BloodPython, SpottedPython, AfricanEggEater,
    NightSnake, LyreSnake, MudSnake, RainbowSnake,
    RedBelliedSnake, QueenSnake, RibbonSnake, RoughGreenSnake,
    CaliforniaKingsnake, DesertKingsnake, SpeckledKingsnake, PrairieKingsnake,
    GrayBandedKingsnake, EasternKingsnake, MoleKingsnake,
    ShovelNosedSnake, GroundSnake, LongNoseSnake, SandBoa, KenyanSandBoa,
    RubberBoa, RosyBoa,
    AsianRatSnake, RadiatedRatSnake, BlackRatSnake, TexasRatSnake,
    YellowRatSnake, BairdsRatSnake, TransPecosRatSnake,
    FoxSnake, GreatPlainsRatSnake,
    AesculapianSnake, FourLinedSnake, LadderSnake, MontpellierSnake,
    HorseshoeWhipSnake, DiceSnake, GrassSnake, SmoothSnake,
    VipBerus, AspiViper, LongNosedViper,
    OrnateFlightSnake, TweedleSnake, SunbeamSnake, BrownTreeSnake,
    WesternShovelNose, StripedRacerSnake, EasternRacerSnake, CoachwhipSnake,
    # Lizards (original 8)
    Gecko, BlueTonguedSkink,
    HornedLizard, FrilledLizard, Iguana, MonitorLizard,
    Chameleon, KomodoDragon,
    # Lizards (additional 45)
    LeopardGecko, CrestedGecko, DayGecko, TokayGecko, GroundGecko,
    CommonWallLizard, SandLizard, GreenAnole, BrownAnole,
    GlassLizard, AlligatorLizard, WhiptailLizard, CollaredLizard,
    SpinyLizard, EasternFenceLizard, WesternFenceLizard,
    DesertIguana, MarineIguana, RhinocerosIguana,
    Chuckwalla, GilaMonster, BeadedLizard,
    NileMonitor, WaterMonitor, BlackWhiteTegu,
    FiveLinedSkink, BroadHeadedSkink, Sandfish,
    BasiliskLizard, PlumedBasilisk,
    TexasHornedLizard, GreaterEarlessLizard,
    ChineseWaterDragon, ThornyDevil, MountainHornedDragon,
    PlatedLizard, CamelLizard, CaimanLizard,
    LaceMonitor, ScalySandLizard, CopperSkink, BlueTailedSkink,
    ArmadilloLizard, FlatHeadedAgama,
    # Turtles (original 5)
    BoxTurtle, PaintedTurtle,
    SnappingTurtle, Leatherback, AlligatorSnappingTurtle,
    # Turtles (additional 20)
    DesertTortoise, GopherTortoise, SulcataTortoise,
    AldabraGiantTortoise, GalapagosTortoise,
    RedFootedTortoise, RussianTortoise, HermannsTortoise,
    StarTortoise, MapTurtle, SpottedTurtle, BlandingsTurtle,
    WoodTurtle, BogTurtle, PondSlider, RedEaredSlider,
    MudTurtle, MuskTurtle, SoftshellTurtle, FlatbackTurtle,
    # Frogs (25)
    CommonFrog, AmericanBullfrog, WoodFrog, SpringPeeper,
    LeopardFrog, PickerelFrog, GrayTreeFrog, GreenTreeFrog, PacificTreeFrog,
    RedEyedTreeFrog, PoisonDartFrog, StrawberryPoisonFrog, GoldenPoisonFrog,
    TomatoFrog, GoliathFrog, AfricanClawedFrog, RainFrog, DesertRainFrog,
    AustralianGreenTreeFrog, WaxyTreeFrog, GlassFrog, HairyFrog,
    FlyingFrog, FirebellyToad, SpadeFootToad,
]
