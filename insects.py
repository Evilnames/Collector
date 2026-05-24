import random
import math
from constants import BLOCK_SIZE

SPOOK_SPEED_THRESHOLD = 0.8   # px/frame — player vx above this counts as moving
SPOOK_RADIUS_BLOCKS   = 3     # blocks (tighter than birds)
FLEE_DURATION         = 2.5   # seconds spent flying before hiding
RETURN_DELAY_MIN      = 15.0  # seconds hidden before returning
RETURN_DELAY_MAX      = 30.0


class Insect:
    SPECIES      = "unknown"
    RARITY       = "common"
    BIOMES       = []       # empty = any biodome
    W, H         = 10, 8
    BODY_COLOR   = (80, 60, 40)
    WING_COLOR   = (120, 180, 120)
    ACCENT_COLOR = (200, 200, 100)
    HOVER_RANGE  = 40       # pixel radius around spawn point
    SPEED        = 28.0
    WING_TYPE      = "butterfly"  # butterfly | moth | beetle | dragonfly | firefly | other
    NIGHT_ONLY     = False        # if True, only visible and catchable at night
    DAWN_ONLY      = False        # if True, only visible during dawn transition
    DUSK_ONLY      = False        # if True, only visible during dusk transition
    HAS_MORPH      = False        # if True, spawn position may seed a rare color morph
    MORPH_VARIANTS = ()           # tuple of morph names; used when HAS_MORPH = True

    def __init__(self, x, y, world):
        self.x        = float(x)
        self.y        = float(y)
        self._spawn_x = float(x)
        self._spawn_y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.world    = world
        self.spooked  = False
        self.hidden   = False
        self._flee_timer   = 0.0   # counts up while fleeing
        self._return_timer = 0.0   # counts down while hidden

        self._hover_phase = random.uniform(0, math.pi * 2)
        self._drift_timer = random.uniform(1.0, 3.0)
        self._drift_tx    = float(x)
        self._drift_ty    = float(y)

    def spook(self):
        self.spooked = True
        self.hidden  = False
        self._flee_timer = 0.0
        self.vx = random.choice([-1, 1]) * self.SPEED * 1.5
        self.vy = -self.SPEED * 3   # fly high

    def update(self, dt):
        self._hover_phase += dt * 4.0

        if self.hidden:
            self._return_timer -= dt
            if self._return_timer <= 0:
                self.hidden  = False
                self.spooked = False
                self.vx = 0.0
                self.vy = 0.0
                self.x = self._spawn_x + random.uniform(-24, 24)
                self.y = self._spawn_y + random.uniform(-12, 12)
            return

        if self.spooked:
            self.x += self.vx * dt
            self.y += self.vy * dt
            self._flee_timer += dt
            if self._flee_timer >= FLEE_DURATION:
                self.hidden = True
                self._return_timer = random.uniform(RETURN_DELAY_MIN, RETURN_DELAY_MAX)
            return

        player = getattr(self.world, '_player_ref', None)
        if player is not None:
            dx_b = abs(player.x - self.x) / BLOCK_SIZE
            dy_b = abs(player.y - self.y) / BLOCK_SIZE
            reduction = getattr(player, 'insect_net_reduction', 0.0)
            radius = SPOOK_RADIUS_BLOCKS * (1.0 - reduction)
            if dx_b < radius and dy_b < radius and abs(player.vx) > SPOOK_SPEED_THRESHOLD:
                self.spook()
                return

        self._drift_timer -= dt
        if self._drift_timer <= 0:
            self._drift_timer = random.uniform(1.5, 4.0)
            angle = random.uniform(0, math.pi * 2)
            dist  = random.uniform(0, self.HOVER_RANGE)
            self._drift_tx = self._spawn_x + math.cos(angle) * dist
            self._drift_ty = self._spawn_y + math.sin(angle) * dist

        dx = self._drift_tx - self.x
        dy = self._drift_ty - self.y
        d  = math.hypot(dx, dy)
        if d > 2:
            self.vx = (dx / d) * self.SPEED
            self.vy = (dy / d) * self.SPEED * 0.4
        else:
            self.vx = 0.0
            self.vy = 0.0

        self.y += math.sin(self._hover_phase) * 0.25
        self.x += self.vx * dt
        self.y += self.vy * dt


# ---------------------------------------------------------------------------
# Butterflies (8)
# ---------------------------------------------------------------------------

class Monarch(Insect):
    SPECIES      = "monarch"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills", "steppe"]
    W, H         = 12, 8
    BODY_COLOR   = (40, 25, 10)
    WING_COLOR   = (220, 110, 20)
    ACCENT_COLOR = (255, 255, 255)
    WING_TYPE    = "butterfly"

class Swallowtail(Insect):
    SPECIES      = "swallowtail"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "birch_forest", "rolling_hills"]
    W, H         = 14, 10
    BODY_COLOR   = (20, 20, 20)
    WING_COLOR   = (240, 220, 80)
    ACCENT_COLOR = (60, 120, 220)
    WING_TYPE    = "butterfly"

class BlueMorpho(Insect):
    SPECIES        = "blue_morpho"
    RARITY         = "rare"
    BIOMES         = ["jungle", "tropical"]
    W, H           = 14, 10
    BODY_COLOR     = (20, 30, 20)
    WING_COLOR     = (40, 130, 255)
    ACCENT_COLOR   = (80, 200, 255)
    WING_TYPE      = "butterfly"
    HAS_MORPH      = True
    MORPH_VARIANTS = ("melanistic", "golden")

class PaintedLady(Insect):
    SPECIES      = "painted_lady"
    RARITY       = "common"
    BIOMES       = []
    W, H         = 10, 8
    BODY_COLOR   = (30, 20, 15)
    WING_COLOR   = (210, 120, 60)
    ACCENT_COLOR = (200, 180, 160)
    WING_TYPE    = "butterfly"

class CabbageWhite(Insect):
    SPECIES      = "cabbage_white"
    RARITY       = "common"
    BIOMES       = []
    W, H         = 10, 7
    BODY_COLOR   = (200, 200, 190)
    WING_COLOR   = (240, 245, 230)
    ACCENT_COLOR = (180, 195, 160)
    WING_TYPE    = "butterfly"

class Birdwing(Insect):
    SPECIES      = "birdwing"
    RARITY       = "rare"
    BIOMES       = ["tropical"]
    W, H         = 16, 11
    BODY_COLOR   = (15, 40, 15)
    WING_COLOR   = (50, 185, 80)
    ACCENT_COLOR = (220, 195, 40)
    WING_TYPE    = "butterfly"

class Skipper(Insect):
    SPECIES      = "skipper"
    RARITY       = "common"
    BIOMES       = ["temperate", "savanna", "steppe"]
    W, H         = 8, 6
    BODY_COLOR   = (70, 45, 15)
    WING_COLOR   = (160, 110, 40)
    ACCENT_COLOR = (220, 180, 90)
    WING_TYPE    = "butterfly"

class Copper(Insect):
    SPECIES      = "copper"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 9, 7
    BODY_COLOR   = (40, 25, 10)
    WING_COLOR   = (200, 90, 30)
    ACCENT_COLOR = (240, 150, 60)
    WING_TYPE    = "butterfly"

class DesertSwallowtail(Insect):
    SPECIES      = "desert_swallowtail"
    RARITY       = "uncommon"
    BIOMES       = ["desert", "canyon", "red_rock", "arid_steppe"]
    W, H         = 13, 9
    BODY_COLOR   = (25, 20, 10)
    WING_COLOR   = (230, 215, 70)
    ACCENT_COLOR = (30, 30, 30)
    WING_TYPE    = "butterfly"

class ArizonaSkipper(Insect):
    SPECIES      = "arizona_skipper"
    RARITY       = "common"
    BIOMES       = ["desert", "canyon", "red_rock", "arid_steppe"]
    W, H         = 8, 6
    BODY_COLOR   = (80, 50, 20)
    WING_COLOR   = (190, 130, 50)
    ACCENT_COLOR = (240, 190, 90)
    WING_TYPE    = "butterfly"

class CheckeredWhite(Insect):
    SPECIES      = "checkered_white"
    RARITY       = "common"
    BIOMES       = ["desert", "arid_steppe"]
    W, H         = 10, 7
    BODY_COLOR   = (180, 175, 170)
    WING_COLOR   = (235, 235, 225)
    ACCENT_COLOR = (40, 40, 40)
    WING_TYPE    = "butterfly"

class MarineBlue(Insect):
    SPECIES      = "marine_blue"
    RARITY       = "uncommon"
    BIOMES       = ["desert", "arid_steppe", "canyon", "red_rock"]
    W, H         = 8, 6
    BODY_COLOR   = (30, 25, 50)
    WING_COLOR   = (130, 155, 220)
    ACCENT_COLOR = (200, 210, 245)
    WING_TYPE    = "butterfly"

class RajahBrookesBirdwing(Insect):
    SPECIES      = "rajahs_birdwing"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 16, 11
    BODY_COLOR   = (10, 20, 10)
    WING_COLOR   = (30, 140, 70)
    ACCENT_COLOR = (180, 215, 80)
    WING_TYPE    = "butterfly"

class CommonTiger(Insect):
    SPECIES      = "common_tiger"
    RARITY       = "common"
    BIOMES       = ["tropical", "jungle", "savanna"]
    W, H         = 12, 8
    BODY_COLOR   = (35, 22, 8)
    WING_COLOR   = (215, 115, 25)
    ACCENT_COLOR = (15, 15, 15)
    WING_TYPE    = "butterfly"

class GlassyTiger(Insect):
    SPECIES      = "glassy_tiger"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 11, 8
    BODY_COLOR   = (25, 20, 15)
    WING_COLOR   = (180, 160, 130)
    ACCENT_COLOR = (30, 30, 30)
    WING_TYPE    = "butterfly"

class RedHelen(Insect):
    SPECIES      = "red_helen"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 15, 10
    BODY_COLOR   = (15, 15, 15)
    WING_COLOR   = (20, 18, 18)
    ACCENT_COLOR = (200, 30, 30)
    WING_TYPE    = "butterfly"

class JapaneseMapButterfly(Insect):
    SPECIES      = "japanese_map"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "birch_forest"]
    W, H         = 11, 8
    BODY_COLOR   = (40, 30, 15)
    WING_COLOR   = (175, 120, 45)
    ACCENT_COLOR = (240, 210, 180)
    WING_TYPE    = "butterfly"

class DesertOrangeTip(Insect):
    SPECIES      = "desert_orange_tip"
    RARITY       = "common"
    BIOMES       = ["desert", "arid_steppe"]
    W, H         = 10, 7
    BODY_COLOR   = (200, 185, 165)
    WING_COLOR   = (240, 235, 220)
    ACCENT_COLOR = (240, 100, 30)
    WING_TYPE    = "butterfly"

class SinaiBatonBlue(Insect):
    SPECIES      = "sinai_baton_blue"
    RARITY       = "rare"
    BIOMES       = ["desert", "arid_steppe"]
    W, H         = 7, 5
    BODY_COLOR   = (30, 25, 50)
    WING_COLOR   = (90, 130, 210)
    ACCENT_COLOR = (160, 195, 245)
    WING_TYPE    = "butterfly"

class EasternFestoon(Insect):
    SPECIES      = "eastern_festoon"
    RARITY       = "uncommon"
    BIOMES       = ["rolling_hills", "steppe", "temperate"]
    W, H         = 12, 9
    BODY_COLOR   = (30, 20, 15)
    WING_COLOR   = (235, 220, 170)
    ACCENT_COLOR = (180, 30, 25)
    WING_TYPE    = "butterfly"

class CleopatraButterfly(Insect):
    SPECIES      = "cleopatra"
    RARITY       = "uncommon"
    BIOMES       = ["rolling_hills", "steppe", "arid_steppe"]
    W, H         = 12, 8
    BODY_COLOR   = (40, 35, 15)
    WING_COLOR   = (235, 225, 60)
    ACCENT_COLOR = (240, 130, 30)
    WING_TYPE    = "butterfly"

class SaharanCloudedYellow(Insect):
    SPECIES      = "saharan_clouded_yellow"
    RARITY       = "common"
    BIOMES       = ["desert", "arid_steppe", "steppe"]
    W, H         = 11, 8
    BODY_COLOR   = (35, 30, 10)
    WING_COLOR   = (220, 200, 50)
    ACCENT_COLOR = (180, 160, 30)
    WING_TYPE    = "butterfly"

class BathWhite(Insect):
    SPECIES      = "bath_white"
    RARITY       = "common"
    BIOMES       = ["arid_steppe", "steppe", "rolling_hills"]
    W, H         = 10, 7
    BODY_COLOR   = (180, 175, 165)
    WING_COLOR   = (240, 240, 235)
    ACCENT_COLOR = (100, 140, 80)
    WING_TYPE    = "butterfly"

class DesertDottedBlue(Insect):
    SPECIES      = "desert_dotted_blue"
    RARITY       = "uncommon"
    BIOMES       = ["desert", "arid_steppe"]
    W, H         = 8, 6
    BODY_COLOR   = (25, 20, 45)
    WING_COLOR   = (110, 145, 215)
    ACCENT_COLOR = (200, 215, 250)
    WING_TYPE    = "butterfly"

class ArabianHairstreak(Insect):
    SPECIES      = "arabian_hairstreak"
    RARITY       = "rare"
    BIOMES       = ["desert", "arid_steppe"]
    W, H         = 8, 6
    BODY_COLOR   = (40, 50, 25)
    WING_COLOR   = (70, 110, 55)
    ACCENT_COLOR = (170, 195, 140)
    WING_TYPE    = "butterfly"

class LevantChalcedony(Insect):
    SPECIES      = "levant_chalcedony"
    RARITY       = "uncommon"
    BIOMES       = ["steppe", "rolling_hills", "arid_steppe"]
    W, H         = 11, 8
    BODY_COLOR   = (45, 30, 10)
    WING_COLOR   = (210, 140, 50)
    ACCENT_COLOR = (240, 200, 110)
    WING_TYPE    = "butterfly"

class AcaciaBlue(Insect):
    SPECIES      = "acacia_blue"
    RARITY       = "common"
    BIOMES       = ["savanna", "steppe", "arid_steppe"]
    W, H         = 8, 6
    BODY_COLOR   = (25, 20, 45)
    WING_COLOR   = (130, 165, 230)
    ACCENT_COLOR = (200, 215, 255)
    WING_TYPE    = "butterfly"

class LargeTortoiseshell(Insect):
    SPECIES      = "large_tortoiseshell"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "rolling_hills", "steppe"]
    W, H         = 13, 9
    BODY_COLOR   = (35, 22, 8)
    WING_COLOR   = (200, 110, 30)
    ACCENT_COLOR = (20, 18, 15)
    WING_TYPE    = "butterfly"

class AfricanMigrant(Insect):
    SPECIES      = "african_migrant"
    RARITY       = "common"
    BIOMES       = ["desert", "savanna", "arid_steppe"]
    W, H         = 10, 7
    BODY_COLOR   = (160, 165, 140)
    WING_COLOR   = (215, 225, 190)
    ACCENT_COLOR = (80, 120, 60)
    WING_TYPE    = "butterfly"

class PurpleEmperor(Insect):
    SPECIES        = "purple_emperor"
    RARITY         = "rare"
    BIOMES         = ["boreal", "birch_forest", "temperate"]
    W, H           = 14, 10
    BODY_COLOR     = (25, 18, 35)
    WING_COLOR     = (70, 40, 110)
    ACCENT_COLOR   = (160, 100, 220)
    WING_TYPE      = "butterfly"
    HAS_MORPH      = True
    MORPH_VARIANTS = ("leucistic", "melanistic")

class ChalkHillBlue(Insect):
    SPECIES      = "chalkhill_blue"
    RARITY       = "uncommon"
    BIOMES       = ["rolling_hills", "steppe"]
    W, H         = 9, 7
    BODY_COLOR   = (30, 28, 50)
    WING_COLOR   = (170, 195, 235)
    ACCENT_COLOR = (220, 230, 255)
    WING_TYPE    = "butterfly"

class SilverWashedFritillary(Insect):
    SPECIES      = "silver_washed_fritillary"
    RARITY       = "uncommon"
    BIOMES       = ["boreal", "birch_forest", "temperate"]
    W, H         = 13, 9
    BODY_COLOR   = (40, 25, 8)
    WING_COLOR   = (210, 125, 30)
    ACCENT_COLOR = (20, 18, 12)
    WING_TYPE    = "butterfly"

class MarbledWhite(Insect):
    SPECIES      = "marbled_white"
    RARITY       = "common"
    BIOMES       = ["rolling_hills", "steppe"]
    W, H         = 11, 8
    BODY_COLOR   = (20, 20, 20)
    WING_COLOR   = (235, 235, 230)
    ACCENT_COLOR = (25, 25, 25)
    WING_TYPE    = "butterfly"

class Grayling(Insect):
    SPECIES      = "grayling"
    RARITY       = "common"
    BIOMES       = ["rocky_mountain", "steep_hills", "steppe"]
    W, H         = 11, 8
    BODY_COLOR   = (80, 70, 50)
    WING_COLOR   = (145, 130, 95)
    ACCENT_COLOR = (195, 178, 135)
    WING_TYPE    = "butterfly"

class OrangeTip(Insect):
    SPECIES      = "orange_tip"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 10, 7
    BODY_COLOR   = (180, 175, 165)
    WING_COLOR   = (242, 240, 230)
    ACCENT_COLOR = (235, 110, 25)
    WING_TYPE    = "butterfly"

class CommonBlue(Insect):
    SPECIES      = "common_blue"
    RARITY       = "common"
    BIOMES       = ["rolling_hills", "steppe", "temperate"]
    W, H         = 8, 6
    BODY_COLOR   = (28, 22, 48)
    WING_COLOR   = (100, 140, 220)
    ACCENT_COLOR = (165, 195, 250)
    WING_TYPE    = "butterfly"

class HollyBlue(Insect):
    SPECIES      = "holly_blue"
    RARITY       = "common"
    BIOMES       = ["temperate", "birch_forest"]
    W, H         = 8, 6
    BODY_COLOR   = (28, 22, 48)
    WING_COLOR   = (155, 170, 235)
    ACCENT_COLOR = (210, 218, 255)
    WING_TYPE    = "butterfly"

class RedAdmiral(Insect):
    SPECIES      = "red_admiral"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills", "birch_forest"]
    W, H         = 12, 9
    BODY_COLOR   = (18, 16, 14)
    WING_COLOR   = (22, 20, 18)
    ACCENT_COLOR = (215, 35, 25)
    WING_TYPE    = "butterfly"

class WhiteAdmiral(Insect):
    SPECIES      = "white_admiral"
    RARITY       = "uncommon"
    BIOMES       = ["boreal", "birch_forest"]
    W, H         = 12, 9
    BODY_COLOR   = (18, 16, 14)
    WING_COLOR   = (22, 20, 18)
    ACCENT_COLOR = (230, 230, 225)
    WING_TYPE    = "butterfly"

class ScotchArgus(Insect):
    SPECIES      = "scotch_argus"
    RARITY       = "uncommon"
    BIOMES       = ["alpine_mountain", "boreal"]
    W, H         = 11, 8
    BODY_COLOR   = (30, 20, 10)
    WING_COLOR   = (65, 40, 18)
    ACCENT_COLOR = (200, 110, 30)
    WING_TYPE    = "butterfly"

class GreenHairstreak(Insect):
    SPECIES      = "green_hairstreak"
    RARITY       = "common"
    BIOMES       = ["rolling_hills", "steppe", "temperate"]
    W, H         = 8, 6
    BODY_COLOR   = (30, 65, 25)
    WING_COLOR   = (60, 135, 50)
    ACCENT_COLOR = (120, 195, 90)
    WING_TYPE    = "butterfly"

class DingySkipper(Insect):
    SPECIES      = "dingy_skipper"
    RARITY       = "common"
    BIOMES       = ["rolling_hills", "steppe"]
    W, H         = 8, 6
    BODY_COLOR   = (65, 50, 28)
    WING_COLOR   = (110, 88, 50)
    ACCENT_COLOR = (165, 138, 90)
    WING_TYPE    = "butterfly"

class Brimstone(Insect):
    SPECIES      = "brimstone"
    RARITY       = "common"
    BIOMES       = ["temperate", "birch_forest", "rolling_hills"]
    W, H         = 12, 8
    BODY_COLOR   = (38, 38, 20)
    WING_COLOR   = (215, 225, 55)
    ACCENT_COLOR = (165, 185, 30)
    WING_TYPE    = "butterfly"

class AfricanSwordtail(Insect):
    SPECIES      = "african_swordtail"
    RARITY       = "uncommon"
    BIOMES       = ["savanna", "steppe"]
    W, H         = 13, 9
    BODY_COLOR   = (175, 170, 155)
    WING_COLOR   = (235, 235, 220)
    ACCENT_COLOR = (180, 35, 25)
    WING_TYPE    = "butterfly"

class MalachiteButterfly(Insect):
    SPECIES      = "malachite_butterfly"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 13, 9
    BODY_COLOR   = (20, 30, 18)
    WING_COLOR   = (50, 160, 70)
    ACCENT_COLOR = (15, 15, 15)
    WING_TYPE    = "butterfly"

class PostmanButterfly(Insect):
    SPECIES      = "postman_butterfly"
    RARITY       = "common"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 12, 8
    BODY_COLOR   = (18, 15, 15)
    WING_COLOR   = (20, 17, 17)
    ACCENT_COLOR = (200, 35, 25)
    WING_TYPE    = "butterfly"

class EightyEight(Insect):
    SPECIES      = "eighty_eight"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 11, 8
    BODY_COLOR   = (18, 18, 18)
    WING_COLOR   = (22, 22, 22)
    ACCENT_COLOR = (215, 215, 210)
    WING_TYPE    = "butterfly"

class BlueDiadem(Insect):
    SPECIES      = "blue_diadem"
    RARITY       = "uncommon"
    BIOMES       = ["savanna", "jungle"]
    W, H         = 13, 9
    BODY_COLOR   = (18, 18, 22)
    WING_COLOR   = (30, 55, 140)
    ACCENT_COLOR = (80, 140, 230)
    WING_TYPE    = "butterfly"

class GreatEggfly(Insect):
    SPECIES      = "great_eggfly"
    RARITY       = "uncommon"
    BIOMES       = ["tropical", "jungle"]
    W, H         = 13, 9
    BODY_COLOR   = (18, 15, 18)
    WING_COLOR   = (22, 18, 22)
    ACCENT_COLOR = (230, 230, 225)
    WING_TYPE    = "butterfly"

class TawnyCoaster(Insect):
    SPECIES      = "tawny_coaster"
    RARITY       = "common"
    BIOMES       = ["tropical", "jungle"]
    W, H         = 11, 8
    BODY_COLOR   = (35, 22, 8)
    WING_COLOR   = (205, 120, 28)
    ACCENT_COLOR = (18, 16, 14)
    WING_TYPE    = "butterfly"

class CommonMormon(Insect):
    SPECIES      = "common_mormon"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 13, 9
    BODY_COLOR   = (18, 15, 15)
    WING_COLOR   = (22, 18, 18)
    ACCENT_COLOR = (180, 80, 100)
    WING_TYPE    = "butterfly"

class ZebraLongwing(Insect):
    SPECIES      = "zebra_longwing"
    RARITY       = "common"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 14, 7
    BODY_COLOR   = (18, 16, 14)
    WING_COLOR   = (22, 20, 18)
    ACCENT_COLOR = (230, 210, 60)
    WING_TYPE    = "butterfly"

class ArcticCloudedYellow(Insect):
    SPECIES      = "arctic_clouded_yellow"
    RARITY       = "rare"
    BIOMES       = ["tundra", "alpine_mountain"]
    W, H         = 10, 7
    BODY_COLOR   = (38, 35, 20)
    WING_COLOR   = (235, 230, 195)
    ACCENT_COLOR = (180, 175, 140)
    WING_TYPE    = "butterfly"

class GreatSpangledFritillary(Insect):
    SPECIES      = "great_spangled_fritillary"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "boreal"]
    W, H         = 12, 9
    BODY_COLOR   = (38, 22, 8)
    WING_COLOR   = (205, 110, 25)
    ACCENT_COLOR = (210, 195, 160)
    WING_TYPE    = "butterfly"

class EasternTigerSwallowtail(Insect):
    SPECIES      = "eastern_tiger_swallowtail"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "birch_forest"]
    W, H         = 14, 10
    BODY_COLOR   = (28, 24, 10)
    WING_COLOR   = (235, 220, 60)
    ACCENT_COLOR = (22, 20, 18)
    WING_TYPE    = "butterfly"

class OceanBlue(Insect):
    SPECIES      = "ocean_blue"
    RARITY       = "common"
    BIOMES       = ["tropical", "savanna"]
    W, H         = 11, 8
    BODY_COLOR   = (28, 20, 48)
    WING_COLOR   = (60, 55, 185)
    ACCENT_COLOR = (130, 110, 235)
    WING_TYPE    = "butterfly"

class JungleSailor(Insect):
    SPECIES      = "jungle_sailor"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 12, 9
    BODY_COLOR   = (18, 16, 14)
    WING_COLOR   = (22, 20, 18)
    ACCENT_COLOR = (215, 215, 205)
    WING_TYPE    = "butterfly"

class SpottedAsparagusBeetle(Insect):
    SPECIES      = "spotted_asparagus_beetle"
    RARITY       = "common"
    BIOMES       = ["rolling_hills", "temperate"]
    W, H         = 8, 6
    BODY_COLOR   = (185, 85, 20)
    WING_COLOR   = (205, 105, 28)
    ACCENT_COLOR = (18, 16, 14)
    WING_TYPE    = "beetle"


# ---------------------------------------------------------------------------
# Beetles (7)
# ---------------------------------------------------------------------------

class StagBeetle(Insect):
    SPECIES      = "stag_beetle"
    RARITY       = "uncommon"
    BIOMES       = ["boreal", "birch_forest", "redwood"]
    W, H         = 11, 7
    BODY_COLOR   = (50, 30, 10)
    WING_COLOR   = (85, 50, 18)
    ACCENT_COLOR = (160, 100, 30)
    WING_TYPE    = "beetle"

class Ladybug(Insect):
    SPECIES      = "ladybug"
    RARITY       = "common"
    BIOMES       = []
    W, H         = 7, 6
    BODY_COLOR   = (200, 30, 20)
    WING_COLOR   = (210, 35, 25)
    ACCENT_COLOR = (15, 15, 15)
    WING_TYPE    = "beetle"

class JewelBeetle(Insect):
    SPECIES      = "jewel_beetle"
    RARITY       = "rare"
    BIOMES       = ["tropical", "jungle"]
    W, H         = 10, 7
    BODY_COLOR   = (20, 130, 90)
    WING_COLOR   = (30, 175, 120)
    ACCENT_COLOR = (200, 160, 40)
    WING_TYPE    = "beetle"

class DungBeetle(Insect):
    SPECIES      = "dung_beetle"
    RARITY       = "common"
    BIOMES       = ["savanna", "desert", "canyon", "red_rock"]
    W, H         = 9, 7
    BODY_COLOR   = (55, 45, 20)
    WING_COLOR   = (75, 60, 28)
    ACCENT_COLOR = (110, 90, 40)
    WING_TYPE    = "beetle"

class Longhorn(Insect):
    SPECIES      = "longhorn"
    RARITY       = "uncommon"
    BIOMES       = ["boreal", "redwood", "birch_forest"]
    W, H         = 12, 6
    BODY_COLOR   = (20, 20, 20)
    WING_COLOR   = (40, 30, 20)
    ACCENT_COLOR = (220, 200, 40)
    WING_TYPE    = "beetle"

class GroundBeetle(Insect):
    SPECIES      = "ground_beetle"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills", "steep_hills"]
    W, H         = 9, 6
    BODY_COLOR   = (15, 25, 15)
    WING_COLOR   = (25, 40, 25)
    ACCENT_COLOR = (80, 130, 60)
    WING_TYPE    = "beetle"

class ClickBeetle(Insect):
    SPECIES      = "click_beetle"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills", "boreal"]
    W, H         = 10, 6
    BODY_COLOR   = (90, 65, 30)
    WING_COLOR   = (115, 82, 40)
    ACCENT_COLOR = (160, 120, 55)
    WING_TYPE    = "beetle"

class PaloVerdeBeetle(Insect):
    SPECIES      = "palo_verde_beetle"
    RARITY       = "uncommon"
    BIOMES       = ["desert", "canyon", "red_rock"]
    W, H         = 14, 7
    BODY_COLOR   = (55, 35, 15)
    WING_COLOR   = (90, 58, 25)
    ACCENT_COLOR = (130, 85, 35)
    WING_TYPE    = "beetle"

class SonoranIroncladBeetle(Insect):
    SPECIES      = "sonoran_ironclad"
    RARITY       = "rare"
    BIOMES       = ["desert"]
    W, H         = 11, 7
    BODY_COLOR   = (30, 35, 60)
    WING_COLOR   = (50, 55, 85)
    ACCENT_COLOR = (200, 200, 210)
    WING_TYPE    = "beetle"

class DesertBlisterBeetle(Insect):
    SPECIES      = "desert_blister_beetle"
    RARITY       = "uncommon"
    BIOMES       = ["desert", "arid_steppe"]
    W, H         = 10, 6
    BODY_COLOR   = (160, 40, 20)
    WING_COLOR   = (200, 60, 25)
    ACCENT_COLOR = (240, 100, 40)
    WING_TYPE    = "beetle"

class SonoranDarkling(Insect):
    SPECIES      = "sonoran_darkling"
    RARITY       = "common"
    BIOMES       = ["desert", "canyon", "red_rock", "arid_steppe"]
    W, H         = 9, 6
    BODY_COLOR   = (20, 20, 20)
    WING_COLOR   = (30, 30, 30)
    ACCENT_COLOR = (50, 45, 40)
    WING_TYPE    = "beetle"

class CactusLonghorn(Insect):
    SPECIES      = "cactus_longhorn"
    RARITY       = "uncommon"
    BIOMES       = ["desert", "canyon", "red_rock"]
    W, H         = 12, 6
    BODY_COLOR   = (75, 60, 45)
    WING_COLOR   = (105, 85, 65)
    ACCENT_COLOR = (180, 160, 130)
    WING_TYPE    = "beetle"

class AtlasBeetle(Insect):
    SPECIES      = "atlas_beetle"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 15, 8
    BODY_COLOR   = (60, 38, 18)
    WING_COLOR   = (95, 60, 28)
    ACCENT_COLOR = (140, 90, 40)
    WING_TYPE    = "beetle"

class RainbowStagBeetle(Insect):
    SPECIES      = "rainbow_stag"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 12, 7
    BODY_COLOR   = (20, 60, 40)
    WING_COLOR   = (40, 100, 70)
    ACCENT_COLOR = (160, 220, 180)
    WING_TYPE    = "beetle"

class AsianLonghornBeetle(Insect):
    SPECIES      = "asian_longhorn"
    RARITY       = "uncommon"
    BIOMES       = ["boreal", "birch_forest"]
    W, H         = 13, 6
    BODY_COLOR   = (15, 15, 15)
    WING_COLOR   = (25, 25, 25)
    ACCENT_COLOR = (235, 235, 235)
    WING_TYPE    = "beetle"

class TigerBeetle(Insect):
    SPECIES      = "tiger_beetle"
    RARITY       = "common"
    BIOMES       = ["beach", "desert", "canyon", "red_rock"]
    W, H         = 9, 6
    BODY_COLOR   = (30, 80, 30)
    WING_COLOR   = (50, 130, 50)
    ACCENT_COLOR = (180, 240, 100)
    SPEED        = 34.0
    WING_TYPE    = "beetle"

class SacredScarab(Insect):
    SPECIES      = "sacred_scarab"
    RARITY       = "common"
    BIOMES       = ["desert", "arid_steppe", "savanna"]
    W, H         = 10, 7
    BODY_COLOR   = (20, 22, 20)
    WING_COLOR   = (35, 38, 32)
    ACCENT_COLOR = (70, 80, 55)
    WING_TYPE    = "beetle"

class EgyptianFlowerChafer(Insect):
    SPECIES      = "egyptian_flower_chafer"
    RARITY       = "uncommon"
    BIOMES       = ["savanna", "steppe", "arid_steppe"]
    W, H         = 10, 7
    BODY_COLOR   = (30, 100, 55)
    WING_COLOR   = (45, 150, 80)
    ACCENT_COLOR = (180, 215, 100)
    WING_TYPE    = "beetle"

class ArabicDarkling(Insect):
    SPECIES      = "arabic_darkling"
    RARITY       = "common"
    BIOMES       = ["desert", "arid_steppe", "canyon", "red_rock"]
    W, H         = 9, 6
    BODY_COLOR   = (18, 18, 18)
    WING_COLOR   = (28, 28, 26)
    ACCENT_COLOR = (55, 50, 42)
    WING_TYPE    = "beetle"

class DesertRoveBeetle(Insect):
    SPECIES      = "desert_rove"
    RARITY       = "common"
    BIOMES       = ["desert", "canyon", "red_rock", "arid_steppe"]
    W, H         = 9, 5
    BODY_COLOR   = (110, 80, 45)
    WING_COLOR   = (140, 105, 60)
    ACCENT_COLOR = (190, 155, 95)
    WING_TYPE    = "beetle"

class NileBuprestid(Insect):
    SPECIES      = "nile_buprestid"
    RARITY       = "rare"
    BIOMES       = ["wetland", "savanna"]
    W, H         = 11, 6
    BODY_COLOR   = (25, 95, 70)
    WING_COLOR   = (40, 155, 110)
    ACCENT_COLOR = (200, 175, 30)
    WING_TYPE    = "beetle"

class SyrianCarabid(Insect):
    SPECIES      = "syrian_carabid"
    RARITY       = "uncommon"
    BIOMES       = ["steppe", "rolling_hills", "arid_steppe"]
    W, H         = 10, 6
    BODY_COLOR   = (20, 40, 20)
    WING_COLOR   = (35, 65, 35)
    ACCENT_COLOR = (100, 165, 80)
    WING_TYPE    = "beetle"

class ArabianLonghornBeetle(Insect):
    SPECIES      = "arabian_longhorn_beetle"
    RARITY       = "uncommon"
    BIOMES       = ["steppe", "arid_steppe"]
    W, H         = 12, 6
    BODY_COLOR   = (80, 55, 25)
    WING_COLOR   = (115, 80, 38)
    ACCENT_COLOR = (200, 175, 120)
    WING_TYPE    = "beetle"

class DesertFogBeetle(Insect):
    SPECIES      = "desert_fog_beetle"
    RARITY       = "common"
    BIOMES       = ["desert", "arid_steppe"]
    W, H         = 9, 7
    BODY_COLOR   = (15, 14, 14)
    WING_COLOR   = (22, 22, 20)
    ACCENT_COLOR = (40, 38, 35)
    WING_TYPE    = "beetle"

class RedPalmWeevil(Insect):
    SPECIES      = "red_palm_weevil"
    RARITY       = "uncommon"
    BIOMES       = ["savanna", "steppe", "arid_steppe"]
    W, H         = 11, 7
    BODY_COLOR   = (160, 35, 20)
    WING_COLOR   = (195, 50, 30)
    ACCENT_COLOR = (220, 80, 40)
    WING_TYPE    = "beetle"

class BronzeChafer(Insect):
    SPECIES      = "bronze_chafer"
    RARITY       = "uncommon"
    BIOMES       = ["savanna", "steppe"]
    W, H         = 10, 7
    BODY_COLOR   = (100, 65, 30)
    WING_COLOR   = (150, 100, 48)
    ACCENT_COLOR = (195, 145, 80)
    WING_TYPE    = "beetle"

class VioletGroundBeetle(Insect):
    SPECIES      = "violet_ground_beetle"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 10, 6
    BODY_COLOR   = (40, 20, 60)
    WING_COLOR   = (65, 35, 95)
    ACCENT_COLOR = (130, 80, 190)
    WING_TYPE    = "beetle"

class HarlequinLadybird(Insect):
    SPECIES      = "harlequin_ladybird"
    RARITY       = "common"
    BIOMES       = ["temperate", "boreal", "rolling_hills"]
    W, H         = 7, 6
    BODY_COLOR   = (190, 28, 18)
    WING_COLOR   = (210, 32, 22)
    ACCENT_COLOR = (12, 12, 12)
    WING_TYPE    = "beetle"

class GoldenChafer(Insect):
    SPECIES      = "golden_chafer"
    RARITY       = "rare"
    BIOMES       = ["rolling_hills", "steppe"]
    W, H         = 10, 7
    BODY_COLOR   = (160, 135, 20)
    WING_COLOR   = (200, 175, 30)
    ACCENT_COLOR = (240, 220, 80)
    WING_TYPE    = "beetle"

class VioletOilBeetle(Insect):
    SPECIES      = "violet_oil_beetle"
    RARITY       = "uncommon"
    BIOMES       = ["rolling_hills", "steppe", "temperate"]
    W, H         = 11, 7
    BODY_COLOR   = (40, 30, 80)
    WING_COLOR   = (55, 42, 110)
    ACCENT_COLOR = (110, 85, 185)
    WING_TYPE    = "beetle"

class WaspBeetle(Insect):
    SPECIES      = "wasp_beetle"
    RARITY       = "common"
    BIOMES       = ["birch_forest", "boreal", "temperate"]
    W, H         = 10, 6
    BODY_COLOR   = (18, 18, 10)
    WING_COLOR   = (22, 22, 12)
    ACCENT_COLOR = (225, 200, 30)
    WING_TYPE    = "beetle"

class MuskBeetle(Insect):
    SPECIES      = "musk_beetle"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "boreal"]
    W, H         = 12, 6
    BODY_COLOR   = (25, 80, 45)
    WING_COLOR   = (40, 125, 70)
    ACCENT_COLOR = (100, 200, 130)
    WING_TYPE    = "beetle"

class AlpineLonghorn(Insect):
    SPECIES      = "alpine_longhorn"
    RARITY       = "uncommon"
    BIOMES       = ["alpine_mountain", "rocky_mountain"]
    W, H         = 13, 6
    BODY_COLOR   = (190, 185, 170)
    WING_COLOR   = (215, 210, 195)
    ACCENT_COLOR = (30, 28, 25)
    WING_TYPE    = "beetle"

class DorBeetle(Insect):
    SPECIES      = "dor_beetle"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills", "boreal"]
    W, H         = 10, 7
    BODY_COLOR   = (20, 22, 55)
    WING_COLOR   = (30, 32, 80)
    ACCENT_COLOR = (65, 75, 165)
    WING_TYPE    = "beetle"

class SoldierBeetle(Insect):
    SPECIES      = "soldier_beetle"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 10, 6
    BODY_COLOR   = (185, 80, 20)
    WING_COLOR   = (215, 100, 28)
    ACCENT_COLOR = (22, 20, 18)
    WING_TYPE    = "beetle"

class GreatDivingBeetle(Insect):
    SPECIES      = "great_diving_beetle"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "swamp"]
    W, H         = 12, 7
    BODY_COLOR   = (38, 50, 22)
    WING_COLOR   = (55, 72, 32)
    ACCENT_COLOR = (140, 160, 85)
    WING_TYPE    = "beetle"

class GoliathBeetle(Insect):
    SPECIES        = "goliath_beetle"
    RARITY         = "rare"
    BIOMES         = ["jungle", "tropical"]
    W, H           = 16, 9
    BODY_COLOR     = (18, 18, 18)
    WING_COLOR     = (28, 28, 28)
    ACCENT_COLOR   = (230, 225, 215)
    WING_TYPE      = "beetle"
    HAS_MORPH      = True
    MORPH_VARIANTS = ("golden", "albino")

class HerculesBeetle(Insect):
    SPECIES        = "hercules_beetle"
    RARITY         = "rare"
    BIOMES         = ["jungle"]
    W, H           = 16, 8
    BODY_COLOR     = (45, 55, 18)
    WING_COLOR     = (65, 80, 25)
    ACCENT_COLOR   = (18, 16, 14)
    HAS_MORPH      = True
    MORPH_VARIANTS = ("melanistic", "blue")
    WING_TYPE    = "beetle"

class RainbowWeevil(Insect):
    SPECIES      = "rainbow_weevil"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 10, 7
    BODY_COLOR   = (120, 30, 130)
    WING_COLOR   = (50, 160, 80)
    ACCENT_COLOR = (220, 165, 25)
    WING_TYPE    = "beetle"

class BombardierBeetle(Insect):
    SPECIES      = "bombardier_beetle"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 9, 6
    BODY_COLOR   = (30, 55, 80)
    WING_COLOR   = (45, 80, 118)
    ACCENT_COLOR = (210, 130, 30)
    WING_TYPE    = "beetle"

class GoldenTortoiseBeetle(Insect):
    SPECIES      = "golden_tortoise_beetle"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 8, 7
    BODY_COLOR   = (170, 145, 18)
    WING_COLOR   = (210, 185, 25)
    ACCENT_COLOR = (245, 230, 110)
    WING_TYPE    = "beetle"

class TwoBandedLonghorn(Insect):
    SPECIES      = "two_banded_longhorn"
    RARITY       = "common"
    BIOMES       = ["temperate", "boreal"]
    W, H         = 11, 6
    BODY_COLOR   = (20, 18, 16)
    WING_COLOR   = (28, 25, 22)
    ACCENT_COLOR = (235, 230, 225)
    WING_TYPE    = "beetle"

class TundraGroundBeetle(Insect):
    SPECIES      = "tundra_ground_beetle"
    RARITY       = "common"
    BIOMES       = ["tundra", "alpine_mountain"]
    W, H         = 9, 6
    BODY_COLOR   = (22, 22, 28)
    WING_COLOR   = (32, 32, 42)
    ACCENT_COLOR = (75, 80, 110)
    WING_TYPE    = "beetle"

class FungalBeetle(Insect):
    SPECIES      = "fungal_beetle"
    RARITY       = "uncommon"
    BIOMES       = ["boreal", "swamp"]
    W, H         = 8, 6
    BODY_COLOR   = (100, 55, 25)
    WING_COLOR   = (145, 80, 38)
    ACCENT_COLOR = (200, 140, 80)
    WING_TYPE    = "beetle"

class AustralianJewelBeetle(Insect):
    SPECIES      = "australian_jewel_beetle"
    RARITY       = "rare"
    BIOMES       = ["tropical", "savanna"]
    W, H         = 11, 6
    BODY_COLOR   = (20, 100, 130)
    WING_COLOR   = (30, 155, 200)
    ACCENT_COLOR = (130, 230, 255)
    WING_TYPE    = "beetle"


# ---------------------------------------------------------------------------
# Dragonflies (5)
# ---------------------------------------------------------------------------

class EmperorDragonfly(Insect):
    SPECIES      = "emperor_dragonfly"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "swamp", "beach"]
    W, H         = 14, 6
    BODY_COLOR   = (40, 80, 200)
    WING_COLOR   = (180, 220, 255)
    ACCENT_COLOR = (80, 160, 255)
    HOVER_RANGE  = 60
    WING_TYPE    = "dragonfly"

class AzureDamselfly(Insect):
    SPECIES      = "azure_damselfly"
    RARITY       = "common"
    BIOMES       = ["wetland", "swamp", "temperate"]
    W, H         = 11, 5
    BODY_COLOR   = (60, 130, 210)
    WING_COLOR   = (200, 235, 255)
    ACCENT_COLOR = (100, 180, 240)
    WING_TYPE    = "dragonfly"

class BroadBodiedChaser(Insect):
    SPECIES      = "broad_bodied_chaser"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "temperate", "rolling_hills"]
    W, H         = 12, 7
    BODY_COLOR   = (100, 160, 50)
    WING_COLOR   = (200, 225, 200)
    ACCENT_COLOR = (150, 210, 80)
    WING_TYPE    = "dragonfly"

class ScarceChaser(Insect):
    SPECIES      = "scarce_chaser"
    RARITY       = "rare"
    BIOMES       = ["wetland"]
    W, H         = 13, 6
    BODY_COLOR   = (180, 90, 20)
    WING_COLOR   = (230, 210, 180)
    ACCENT_COLOR = (220, 140, 50)
    WING_TYPE    = "dragonfly"

class BandedDemoiselle(Insect):
    SPECIES      = "banded_demoiselle"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "swamp", "boreal"]
    W, H         = 12, 5
    BODY_COLOR   = (20, 110, 60)
    WING_COLOR   = (100, 200, 140)
    ACCENT_COLOR = (160, 240, 180)
    WING_TYPE    = "dragonfly"

class DesertWhitetail(Insect):
    SPECIES      = "desert_whitetail"
    RARITY       = "uncommon"
    BIOMES       = ["desert", "canyon", "red_rock"]
    W, H         = 13, 6
    BODY_COLOR   = (200, 200, 205)
    WING_COLOR   = (220, 235, 255)
    ACCENT_COLOR = (150, 185, 230)
    HOVER_RANGE  = 55
    WING_TYPE    = "dragonfly"

class VarMeadowhawk(Insect):
    SPECIES      = "variegated_meadowhawk"
    RARITY       = "common"
    BIOMES       = ["desert", "arid_steppe", "canyon", "red_rock"]
    W, H         = 12, 6
    BODY_COLOR   = (180, 50, 20)
    WING_COLOR   = (220, 210, 190)
    ACCENT_COLOR = (230, 120, 50)
    HOVER_RANGE  = 50
    WING_TYPE    = "dragonfly"

class CrimsonMarshGlider(Insect):
    SPECIES      = "crimson_marsh_glider"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "tropical", "swamp"]
    W, H         = 13, 6
    BODY_COLOR   = (150, 30, 20)
    WING_COLOR   = (220, 200, 180)
    ACCENT_COLOR = (200, 60, 40)
    HOVER_RANGE  = 55
    WING_TYPE    = "dragonfly"

class OrientalScarlet(Insect):
    SPECIES      = "oriental_scarlet"
    RARITY       = "common"
    BIOMES       = ["wetland", "tropical", "swamp"]
    W, H         = 12, 6
    BODY_COLOR   = (200, 20, 15)
    WING_COLOR   = (230, 215, 200)
    ACCENT_COLOR = (240, 80, 50)
    WING_TYPE    = "dragonfly"

class NileBluetail(Insect):
    SPECIES      = "nile_bluetail"
    RARITY       = "common"
    BIOMES       = ["wetland", "beach"]
    W, H         = 10, 5
    BODY_COLOR   = (15, 15, 20)
    WING_COLOR   = (195, 225, 255)
    ACCENT_COLOR = (60, 140, 225)
    WING_TYPE    = "dragonfly"

class BlackTippedGroundling(Insect):
    SPECIES      = "black_tipped_groundling"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "swamp", "savanna"]
    W, H         = 11, 6
    BODY_COLOR   = (20, 20, 20)
    WING_COLOR   = (215, 215, 210)
    ACCENT_COLOR = (200, 200, 195)
    WING_TYPE    = "dragonfly"

class DesertDarter(Insect):
    SPECIES      = "desert_darter"
    RARITY       = "uncommon"
    BIOMES       = ["desert", "arid_steppe", "canyon", "red_rock"]
    W, H         = 11, 5
    BODY_COLOR   = (155, 75, 25)
    WING_COLOR   = (220, 210, 190)
    ACCENT_COLOR = (200, 130, 60)
    HOVER_RANGE  = 50
    WING_TYPE    = "dragonfly"

class ArabianSkimmer(Insect):
    SPECIES      = "arabian_skimmer"
    RARITY       = "common"
    BIOMES       = ["wetland", "savanna", "steppe"]
    W, H         = 12, 6
    BODY_COLOR   = (120, 120, 40)
    WING_COLOR   = (215, 220, 185)
    ACCENT_COLOR = (175, 175, 70)
    WING_TYPE    = "dragonfly"

class ArabianSprite(Insect):
    SPECIES      = "arabian_sprite"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "beach"]
    W, H         = 10, 5
    BODY_COLOR   = (20, 90, 70)
    WING_COLOR   = (190, 230, 220)
    ACCENT_COLOR = (50, 175, 145)
    WING_TYPE    = "dragonfly"

class WanderingGlider(Insect):
    SPECIES      = "wandering_glider"
    RARITY       = "common"
    BIOMES       = ["wetland", "savanna", "desert"]
    W, H         = 13, 6
    BODY_COLOR   = (185, 115, 25)
    WING_COLOR   = (225, 215, 175)
    ACCENT_COLOR = (220, 165, 55)
    HOVER_RANGE  = 70
    SPEED        = 36.0
    WING_TYPE    = "dragonfly"

class FourSpottedChaser(Insect):
    SPECIES      = "four_spotted_chaser"
    RARITY       = "common"
    BIOMES       = ["wetland", "boreal"]
    W, H         = 12, 6
    BODY_COLOR   = (140, 105, 30)
    WING_COLOR   = (220, 210, 180)
    ACCENT_COLOR = (185, 145, 45)
    WING_TYPE    = "dragonfly"

class BlackDarter(Insect):
    SPECIES      = "black_darter"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "boreal", "alpine_mountain"]
    W, H         = 10, 5
    BODY_COLOR   = (20, 20, 20)
    WING_COLOR   = (210, 210, 205)
    ACCENT_COLOR = (45, 45, 45)
    WING_TYPE    = "dragonfly"

class GoldenRingedDragonfly(Insect):
    SPECIES      = "golden_ringed_dragonfly"
    RARITY       = "rare"
    BIOMES       = ["wetland", "boreal"]
    W, H         = 15, 6
    BODY_COLOR   = (18, 18, 15)
    WING_COLOR   = (210, 220, 205)
    ACCENT_COLOR = (215, 185, 30)
    HOVER_RANGE  = 65
    WING_TYPE    = "dragonfly"

class EuropeanBluetail(Insect):
    SPECIES      = "european_bluetail"
    RARITY       = "common"
    BIOMES       = ["wetland", "temperate"]
    W, H         = 10, 5
    BODY_COLOR   = (15, 15, 22)
    WING_COLOR   = (195, 220, 255)
    ACCENT_COLOR = (75, 145, 230)
    WING_TYPE    = "dragonfly"

class EmeraldDamselfly(Insect):
    SPECIES      = "emerald_damselfly"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "swamp"]
    W, H         = 11, 5
    BODY_COLOR   = (20, 75, 45)
    WING_COLOR   = (190, 235, 215)
    ACCENT_COLOR = (50, 170, 110)
    WING_TYPE    = "dragonfly"

class CommonHawker(Insect):
    SPECIES      = "common_hawker"
    RARITY       = "common"
    BIOMES       = ["wetland", "boreal"]
    W, H         = 14, 6
    BODY_COLOR   = (20, 30, 60)
    WING_COLOR   = (200, 215, 235)
    ACCENT_COLOR = (55, 130, 210)
    HOVER_RANGE  = 65
    WING_TYPE    = "dragonfly"

class AfricanRiverDamsel(Insect):
    SPECIES      = "african_river_damsel"
    RARITY       = "common"
    BIOMES       = ["wetland", "savanna"]
    W, H         = 10, 5
    BODY_COLOR   = (15, 18, 28)
    WING_COLOR   = (195, 220, 255)
    ACCENT_COLOR = (65, 130, 220)
    WING_TYPE    = "dragonfly"

class MalachiteDamselfly(Insect):
    SPECIES      = "malachite_damselfly"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "jungle"]
    W, H         = 11, 5
    BODY_COLOR   = (18, 72, 40)
    WING_COLOR   = (180, 235, 210)
    ACCENT_COLOR = (40, 165, 100)
    WING_TYPE    = "dragonfly"

class TundraMosaic(Insect):
    SPECIES      = "tundra_mosaic"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "tundra"]
    W, H         = 13, 6
    BODY_COLOR   = (18, 28, 55)
    WING_COLOR   = (200, 215, 235)
    ACCENT_COLOR = (55, 120, 200)
    WING_TYPE    = "dragonfly"

class MagpieHawker(Insect):
    SPECIES      = "magpie_hawker"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "tropical"]
    W, H         = 14, 6
    BODY_COLOR   = (18, 18, 18)
    WING_COLOR   = (215, 215, 215)
    ACCENT_COLOR = (200, 200, 200)
    WING_TYPE    = "dragonfly"

class ScarletDragonlet(Insect):
    SPECIES      = "scarlet_dragonlet"
    RARITY       = "common"
    BIOMES       = ["wetland", "tropical", "savanna"]
    W, H         = 10, 5
    BODY_COLOR   = (195, 22, 18)
    WING_COLOR   = (225, 210, 200)
    ACCENT_COLOR = (235, 70, 50)
    WING_TYPE    = "dragonfly"


# ---------------------------------------------------------------------------
# Fireflies (3)
# ---------------------------------------------------------------------------

class CommonFirefly(Insect):
    SPECIES      = "common_firefly"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "swamp"]
    W, H         = 7, 5
    BODY_COLOR   = (30, 35, 20)
    WING_COLOR   = (50, 55, 35)
    ACCENT_COLOR = (220, 255, 80)
    WING_TYPE    = "firefly"
    NIGHT_ONLY   = True

class BlueFirefly(Insect):
    SPECIES      = "blue_firefly"
    RARITY       = "rare"
    BIOMES       = ["wetland"]
    W, H         = 7, 5
    BODY_COLOR   = (20, 25, 40)
    WING_COLOR   = (40, 50, 70)
    ACCENT_COLOR = (80, 160, 255)
    WING_TYPE    = "firefly"
    NIGHT_ONLY   = True

class GoldenFirefly(Insect):
    SPECIES      = "golden_firefly"
    RARITY       = "rare"
    BIOMES       = ["wetland", "swamp"]
    W, H         = 8, 5
    BODY_COLOR   = (35, 30, 15)
    WING_COLOR   = (60, 52, 28)
    ACCENT_COLOR = (255, 220, 60)
    WING_TYPE    = "firefly"
    NIGHT_ONLY   = True

class SyrianFirefly(Insect):
    SPECIES      = "syrian_firefly"
    RARITY       = "rare"
    BIOMES       = ["wetland", "swamp"]
    W, H         = 7, 5
    BODY_COLOR   = (25, 30, 20)
    WING_COLOR   = (45, 50, 35)
    ACCENT_COLOR = (255, 230, 60)
    WING_TYPE    = "firefly"
    NIGHT_ONLY   = True

class LevantineFirefly(Insect):
    SPECIES      = "levantine_firefly"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "steppe"]
    W, H         = 7, 5
    BODY_COLOR   = (28, 32, 22)
    WING_COLOR   = (48, 54, 38)
    ACCENT_COLOR = (160, 230, 100)
    WING_TYPE    = "firefly"
    NIGHT_ONLY   = True

class ItalianFirefly(Insect):
    SPECIES      = "italian_firefly"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "temperate"]
    W, H         = 7, 5
    BODY_COLOR   = (32, 28, 18)
    WING_COLOR   = (55, 48, 30)
    ACCENT_COLOR = (255, 200, 80)
    WING_TYPE    = "firefly"
    NIGHT_ONLY   = True

class AmericanFirefly(Insect):
    SPECIES      = "american_firefly"
    RARITY       = "common"
    BIOMES       = ["wetland", "boreal", "temperate"]
    W, H         = 7, 5
    BODY_COLOR   = (30, 28, 20)
    WING_COLOR   = (52, 48, 35)
    ACCENT_COLOR = (240, 240, 80)
    WING_TYPE    = "firefly"
    NIGHT_ONLY   = True


# ---------------------------------------------------------------------------
# Moths (4)
# ---------------------------------------------------------------------------

class LunaMoth(Insect):
    SPECIES        = "luna_moth"
    RARITY         = "rare"
    BIOMES         = ["boreal", "birch_forest", "redwood"]
    W, H           = 15, 10
    BODY_COLOR     = (180, 230, 180)
    WING_COLOR     = (120, 210, 140)
    ACCENT_COLOR   = (200, 245, 200)
    WING_TYPE      = "moth"
    HAS_MORPH      = True
    MORPH_VARIANTS = ("golden", "leucistic")

class AtlasMoth(Insect):
    SPECIES        = "atlas_moth"
    RARITY         = "rare"
    BIOMES         = ["jungle", "tropical"]
    W, H           = 16, 11
    BODY_COLOR     = (80, 45, 20)
    WING_COLOR     = (180, 110, 50)
    ACCENT_COLOR   = (240, 200, 120)
    WING_TYPE      = "moth"
    HAS_MORPH      = True
    MORPH_VARIANTS = ("melanistic", "albino")

class HawkMoth(Insect):
    SPECIES      = "hawk_moth"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "rolling_hills", "savanna"]
    W, H         = 13, 8
    BODY_COLOR   = (70, 60, 40)
    WING_COLOR   = (120, 100, 65)
    ACCENT_COLOR = (180, 155, 95)
    WING_TYPE    = "moth"
    DUSK_ONLY    = True

class PepperedMoth(Insect):
    SPECIES      = "peppered_moth"
    RARITY       = "common"
    BIOMES       = ["boreal", "birch_forest", "temperate"]
    W, H         = 11, 8
    BODY_COLOR   = (150, 145, 140)
    WING_COLOR   = (170, 165, 160)
    ACCENT_COLOR = (60, 55, 50)
    WING_TYPE    = "moth"

class WhiteLinedSphinx(Insect):
    SPECIES      = "white_lined_sphinx"
    RARITY       = "uncommon"
    BIOMES       = ["desert", "arid_steppe", "canyon", "red_rock"]
    W, H         = 15, 9
    BODY_COLOR   = (70, 65, 40)
    WING_COLOR   = (100, 90, 55)
    ACCENT_COLOR = (210, 130, 150)
    SPEED        = 38.0
    WING_TYPE    = "moth"

class CactusMoth(Insect):
    SPECIES      = "cactus_moth"
    RARITY       = "common"
    BIOMES       = ["desert", "canyon", "red_rock"]
    W, H         = 11, 7
    BODY_COLOR   = (90, 75, 55)
    WING_COLOR   = (140, 120, 90)
    ACCENT_COLOR = (220, 205, 180)
    WING_TYPE    = "moth"

class ChineseMoonMoth(Insect):
    SPECIES      = "chinese_moon_moth"
    RARITY       = "rare"
    BIOMES       = ["boreal", "birch_forest"]
    W, H         = 16, 11
    BODY_COLOR   = (200, 170, 160)
    WING_COLOR   = (225, 180, 170)
    ACCENT_COLOR = (255, 210, 190)
    WING_TYPE    = "moth"

class IndianMoonMoth(Insect):
    SPECIES      = "indian_moon_moth"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 16, 12
    BODY_COLOR   = (200, 230, 200)
    WING_COLOR   = (180, 220, 175)
    ACCENT_COLOR = (240, 255, 230)
    WING_TYPE    = "moth"

class AsianEmperorMoth(Insect):
    SPECIES      = "asian_emperor_moth"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "birch_forest", "boreal"]
    W, H         = 14, 10
    BODY_COLOR   = (75, 55, 30)
    WING_COLOR   = (130, 95, 55)
    ACCENT_COLOR = (220, 195, 150)
    WING_TYPE    = "moth"

class OleanderHawkMoth(Insect):
    SPECIES      = "oleander_hawk_moth"
    RARITY       = "uncommon"
    BIOMES       = ["savanna", "steppe", "arid_steppe"]
    W, H         = 15, 9
    BODY_COLOR   = (60, 100, 60)
    WING_COLOR   = (80, 135, 85)
    ACCENT_COLOR = (215, 130, 155)
    SPEED        = 36.0
    WING_TYPE    = "moth"

class DeathsHeadHawkMoth(Insect):
    SPECIES      = "deaths_head_hawk_moth"
    RARITY       = "rare"
    BIOMES       = ["steppe", "arid_steppe", "rolling_hills"]
    W, H         = 16, 10
    BODY_COLOR   = (35, 30, 15)
    WING_COLOR   = (80, 65, 40)
    ACCENT_COLOR = (235, 210, 50)
    SPEED        = 36.0
    WING_TYPE    = "moth"

class DesertHawkMoth(Insect):
    SPECIES      = "desert_hawk_moth"
    RARITY       = "uncommon"
    BIOMES       = ["desert", "arid_steppe"]
    W, H         = 14, 8
    BODY_COLOR   = (120, 105, 75)
    WING_COLOR   = (165, 145, 100)
    ACCENT_COLOR = (210, 150, 140)
    SPEED        = 35.0
    WING_TYPE    = "moth"

class CottonLeafworm(Insect):
    SPECIES      = "cotton_leafworm"
    RARITY       = "common"
    BIOMES       = ["savanna", "steppe"]
    W, H         = 11, 7
    BODY_COLOR   = (90, 80, 65)
    WING_COLOR   = (130, 115, 95)
    ACCENT_COLOR = (175, 165, 145)
    WING_TYPE    = "moth"

class FigMoth(Insect):
    SPECIES      = "fig_moth"
    RARITY       = "common"
    BIOMES       = ["steppe", "rolling_hills", "arid_steppe"]
    W, H         = 10, 7
    BODY_COLOR   = (100, 85, 60)
    WING_COLOR   = (145, 125, 90)
    ACCENT_COLOR = (215, 195, 160)
    WING_TYPE    = "moth"

class ArabianSandMoth(Insect):
    SPECIES      = "arabian_sand_moth"
    RARITY       = "common"
    BIOMES       = ["desert", "arid_steppe"]
    W, H         = 11, 7
    BODY_COLOR   = (145, 125, 90)
    WING_COLOR   = (195, 180, 145)
    ACCENT_COLOR = (230, 215, 185)
    WING_TYPE    = "moth"

class PomegranateMoth(Insect):
    SPECIES      = "pomegranate_moth"
    RARITY       = "uncommon"
    BIOMES       = ["steppe", "rolling_hills"]
    W, H         = 10, 7
    BODY_COLOR   = (80, 50, 40)
    WING_COLOR   = (120, 80, 65)
    ACCENT_COLOR = (195, 130, 105)
    WING_TYPE    = "moth"

class LebanonMoonMoth(Insect):
    SPECIES      = "lebanon_moon_moth"
    RARITY       = "rare"
    BIOMES       = ["rolling_hills", "steppe"]
    W, H         = 14, 10
    BODY_COLOR   = (165, 190, 155)
    WING_COLOR   = (140, 185, 140)
    ACCENT_COLOR = (210, 240, 200)
    WING_TYPE    = "moth"

class CinnabarMoth(Insect):
    SPECIES      = "cinnabar_moth"
    RARITY       = "uncommon"
    BIOMES       = ["rolling_hills", "steppe"]
    W, H         = 12, 8
    BODY_COLOR   = (18, 15, 15)
    WING_COLOR   = (22, 18, 18)
    ACCENT_COLOR = (210, 30, 25)
    WING_TYPE    = "moth"

class GardenTigerMoth(Insect):
    SPECIES      = "garden_tiger"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 13, 9
    BODY_COLOR   = (90, 68, 38)
    WING_COLOR   = (130, 100, 58)
    ACCENT_COLOR = (210, 80, 30)
    WING_TYPE    = "moth"

class SixSpotBurnet(Insect):
    SPECIES      = "six_spot_burnet"
    RARITY       = "common"
    BIOMES       = ["rolling_hills", "steppe"]
    W, H         = 10, 7
    BODY_COLOR   = (18, 55, 30)
    WING_COLOR   = (25, 80, 45)
    ACCENT_COLOR = (200, 30, 28)
    WING_TYPE    = "moth"

class OakEggar(Insect):
    SPECIES      = "oak_eggar"
    RARITY       = "uncommon"
    BIOMES       = ["boreal", "birch_forest"]
    W, H         = 13, 9
    BODY_COLOR   = (95, 60, 22)
    WING_COLOR   = (145, 95, 35)
    ACCENT_COLOR = (195, 140, 70)
    WING_TYPE    = "moth"

class EmperorMoth(Insect):
    SPECIES      = "emperor_moth"
    RARITY       = "uncommon"
    BIOMES       = ["rolling_hills", "boreal", "steppe"]
    W, H         = 14, 10
    BODY_COLOR   = (90, 85, 75)
    WING_COLOR   = (140, 130, 115)
    ACCENT_COLOR = (215, 185, 140)
    WING_TYPE    = "moth"

class MerveilleduJour(Insect):
    SPECIES      = "merveilledujour"
    RARITY       = "rare"
    BIOMES       = ["birch_forest", "boreal"]
    W, H         = 12, 8
    BODY_COLOR   = (55, 75, 45)
    WING_COLOR   = (90, 120, 75)
    ACCENT_COLOR = (175, 200, 155)
    WING_TYPE    = "moth"

class PrivetHawkMoth(Insect):
    SPECIES      = "privet_hawk_moth"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 15, 9
    BODY_COLOR   = (75, 65, 50)
    WING_COLOR   = (110, 95, 72)
    ACCENT_COLOR = (185, 125, 145)
    SPEED        = 35.0
    WING_TYPE    = "moth"

class ElephantHawkMoth(Insect):
    SPECIES      = "elephant_hawk_moth"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 14, 8
    BODY_COLOR   = (55, 80, 45)
    WING_COLOR   = (85, 120, 70)
    ACCENT_COLOR = (215, 80, 130)
    SPEED        = 34.0
    WING_TYPE    = "moth"

class LargeYellowUnderwing(Insect):
    SPECIES      = "large_yellow_underwing"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills", "boreal"]
    W, H         = 12, 8
    BODY_COLOR   = (90, 72, 45)
    WING_COLOR   = (125, 100, 65)
    ACCENT_COLOR = (230, 190, 35)
    WING_TYPE    = "moth"

class IoMoth(Insect):
    SPECIES      = "io_moth"
    RARITY       = "rare"
    BIOMES       = ["temperate", "boreal"]
    W, H         = 14, 10
    BODY_COLOR   = (160, 120, 35)
    WING_COLOR   = (200, 165, 50)
    ACCENT_COLOR = (35, 85, 175)
    WING_TYPE    = "moth"

class CecrotiaMoth(Insect):
    SPECIES      = "cecropia_moth"
    RARITY       = "rare"
    BIOMES       = ["temperate", "birch_forest"]
    W, H         = 16, 11
    BODY_COLOR   = (100, 30, 28)
    WING_COLOR   = (145, 45, 40)
    ACCENT_COLOR = (230, 215, 200)
    WING_TYPE    = "moth"

class PolyphemusMoth(Insect):
    SPECIES      = "polyphemus_moth"
    RARITY       = "rare"
    BIOMES       = ["boreal", "temperate"]
    W, H         = 15, 11
    BODY_COLOR   = (115, 85, 45)
    WING_COLOR   = (165, 125, 65)
    ACCENT_COLOR = (220, 185, 130)
    WING_TYPE    = "moth"

class HummingbirdHawkMoth(Insect):
    SPECIES      = "hummingbird_hawk_moth"
    RARITY       = "uncommon"
    BIOMES       = ["steppe", "rolling_hills", "temperate"]
    W, H         = 12, 7
    BODY_COLOR   = (65, 55, 35)
    WING_COLOR   = (95, 80, 52)
    ACCENT_COLOR = (200, 130, 35)
    SPEED        = 40.0
    WING_TYPE    = "moth"

class JerseyTigerMoth(Insect):
    SPECIES      = "jersey_tiger"
    RARITY       = "uncommon"
    BIOMES       = ["steppe", "rolling_hills"]
    W, H         = 12, 8
    BODY_COLOR   = (18, 18, 18)
    WING_COLOR   = (22, 22, 22)
    ACCENT_COLOR = (210, 65, 30)
    WING_TYPE    = "moth"

class WoodTiger(Insect):
    SPECIES      = "wood_tiger"
    RARITY       = "uncommon"
    BIOMES       = ["boreal", "birch_forest"]
    W, H         = 12, 8
    BODY_COLOR   = (18, 16, 12)
    WING_COLOR   = (22, 20, 15)
    ACCENT_COLOR = (220, 185, 30)
    WING_TYPE    = "moth"

class TussockMoth(Insect):
    SPECIES      = "tussock_moth"
    RARITY       = "uncommon"
    BIOMES       = ["boreal", "birch_forest"]
    W, H         = 11, 8
    BODY_COLOR   = (200, 195, 185)
    WING_COLOR   = (225, 220, 210)
    ACCENT_COLOR = (240, 235, 225)
    WING_TYPE    = "moth"

class TailedMoonMoth(Insect):
    SPECIES      = "tailed_moon_moth"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 15, 12
    BODY_COLOR   = (180, 210, 165)
    WING_COLOR   = (145, 195, 140)
    ACCENT_COLOR = (215, 245, 200)
    WING_TYPE    = "moth"

class VineMoth(Insect):
    SPECIES      = "vine_moth"
    RARITY       = "common"
    BIOMES       = ["rolling_hills", "steppe"]
    W, H         = 10, 7
    BODY_COLOR   = (105, 90, 65)
    WING_COLOR   = (150, 132, 100)
    ACCENT_COLOR = (195, 178, 145)
    WING_TYPE    = "moth"

class SpotWingedGlassywing(Insect):
    SPECIES      = "spot_winged_glassywing"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 13, 9
    BODY_COLOR   = (28, 25, 22)
    WING_COLOR   = (190, 215, 230)
    ACCENT_COLOR = (22, 20, 18)
    WING_TYPE    = "moth"


# ---------------------------------------------------------------------------
# Other (3)
# ---------------------------------------------------------------------------

class PrayingMantis(Insect):
    SPECIES      = "praying_mantis"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical", "savanna"]
    W, H         = 10, 12
    BODY_COLOR   = (60, 140, 60)
    WING_COLOR   = (80, 165, 80)
    ACCENT_COLOR = (110, 200, 110)
    WING_TYPE    = "other"

class Honeybee(Insect):
    SPECIES      = "honeybee"
    RARITY       = "common"
    BIOMES       = []
    W, H         = 8, 6
    BODY_COLOR   = (30, 25, 10)
    WING_COLOR   = (200, 225, 240)
    ACCENT_COLOR = (230, 185, 30)
    WING_TYPE    = "bee"

class GiantHornet(Insect):
    SPECIES      = "giant_hornet"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical", "boreal"]
    W, H         = 11, 7
    BODY_COLOR   = (30, 25, 5)
    WING_COLOR   = (200, 215, 230)
    ACCENT_COLOR = (220, 170, 15)
    WING_TYPE    = "other"

class TarantulaHawk(Insect):
    SPECIES      = "tarantula_hawk"
    RARITY       = "rare"
    BIOMES       = ["desert", "canyon", "red_rock"]
    W, H         = 12, 7
    BODY_COLOR   = (15, 15, 15)
    WING_COLOR   = (210, 100, 20)
    ACCENT_COLOR = (240, 140, 30)
    SPEED        = 36.0
    WING_TYPE    = "other"

class SonoranBumblebee(Insect):
    SPECIES      = "sonoran_bumblebee"
    RARITY       = "common"
    BIOMES       = ["desert", "arid_steppe", "canyon", "red_rock"]
    W, H         = 9, 7
    BODY_COLOR   = (25, 20, 10)
    WING_COLOR   = (210, 230, 245)
    ACCENT_COLOR = (225, 195, 35)
    WING_TYPE    = "bee"

class DesertCicada(Insect):
    SPECIES      = "desert_cicada"
    RARITY       = "common"
    BIOMES       = ["desert", "canyon", "red_rock", "arid_steppe"]
    W, H         = 11, 7
    BODY_COLOR   = (80, 95, 60)
    WING_COLOR   = (160, 180, 140)
    ACCENT_COLOR = (110, 130, 85)
    WING_TYPE    = "other"

class VelvetAnt(Insect):
    SPECIES      = "velvet_ant"
    RARITY       = "uncommon"
    BIOMES       = ["desert", "canyon", "red_rock"]
    W, H         = 9, 6
    BODY_COLOR   = (20, 10, 10)
    WING_COLOR   = (180, 30, 20)
    ACCENT_COLOR = (230, 50, 30)
    SPEED        = 32.0
    WING_TYPE    = "other"

class AntLion(Insect):
    SPECIES      = "ant_lion"
    RARITY       = "uncommon"
    BIOMES       = ["desert", "arid_steppe"]
    W, H         = 10, 6
    BODY_COLOR   = (100, 80, 50)
    WING_COLOR   = (160, 140, 100)
    ACCENT_COLOR = (200, 180, 140)
    WING_TYPE    = "other"

class DesertLocust(Insect):
    SPECIES      = "desert_locust"
    RARITY       = "common"
    BIOMES       = ["desert", "arid_steppe", "steppe", "canyon", "red_rock"]
    W, H         = 12, 6
    BODY_COLOR   = (100, 115, 40)
    WING_COLOR   = (160, 175, 80)
    ACCENT_COLOR = (200, 200, 100)
    HOVER_RANGE  = 50
    SPEED        = 35.0
    WING_TYPE    = "other"

class GiantMesquiteBug(Insect):
    SPECIES      = "giant_mesquite_bug"
    RARITY       = "uncommon"
    BIOMES       = ["desert", "canyon", "red_rock"]
    W, H         = 11, 7
    BODY_COLOR   = (20, 15, 10)
    WING_COLOR   = (45, 35, 20)
    ACCENT_COLOR = (210, 100, 20)
    WING_TYPE    = "other"

class LanternFly(Insect):
    SPECIES      = "lantern_fly"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 11, 7
    BODY_COLOR   = (60, 80, 40)
    WING_COLOR   = (90, 120, 60)
    ACCENT_COLOR = (220, 60, 30)
    WING_TYPE    = "other"

class GiantWaterBug(Insect):
    SPECIES      = "giant_water_bug"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "swamp"]
    W, H         = 12, 7
    BODY_COLOR   = (70, 55, 30)
    WING_COLOR   = (95, 75, 42)
    ACCENT_COLOR = (130, 105, 60)
    WING_TYPE    = "other"

class ChineseMantis(Insect):
    SPECIES      = "chinese_mantis"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical", "temperate"]
    W, H         = 11, 12
    BODY_COLOR   = (90, 130, 70)
    WING_COLOR   = (115, 155, 90)
    ACCENT_COLOR = (180, 210, 140)
    WING_TYPE    = "other"

class BambooLocust(Insect):
    SPECIES      = "bamboo_locust"
    RARITY       = "common"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 11, 6
    BODY_COLOR   = (60, 130, 50)
    WING_COLOR   = (100, 175, 80)
    ACCENT_COLOR = (200, 230, 120)
    HOVER_RANGE  = 50
    SPEED        = 33.0
    WING_TYPE    = "other"

class AsianGiantHornet(Insect):
    SPECIES      = "asian_giant_hornet"
    RARITY       = "rare"
    BIOMES       = ["boreal", "temperate", "birch_forest"]
    W, H         = 13, 8
    BODY_COLOR   = (35, 28, 8)
    WING_COLOR   = (210, 225, 240)
    ACCENT_COLOR = (230, 160, 10)
    SPEED        = 34.0
    WING_TYPE    = "other"

class GiantStickInsect(Insect):
    SPECIES      = "giant_stick_insect"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 14, 5
    BODY_COLOR   = (70, 100, 50)
    WING_COLOR   = (85, 115, 65)
    ACCENT_COLOR = (120, 150, 90)
    SPEED        = 18.0
    HOVER_RANGE  = 30
    WING_TYPE    = "other"

class ArabianMantis(Insect):
    SPECIES      = "arabian_mantis"
    RARITY       = "uncommon"
    BIOMES       = ["desert", "arid_steppe", "steppe"]
    W, H         = 10, 11
    BODY_COLOR   = (185, 160, 100)
    WING_COLOR   = (215, 190, 130)
    ACCENT_COLOR = (240, 220, 170)
    SPEED        = 20.0
    WING_TYPE    = "other"

class FlowerMantis(Insect):
    SPECIES      = "flower_mantis"
    RARITY       = "rare"
    BIOMES       = ["savanna", "steppe"]
    W, H         = 9, 10
    BODY_COLOR   = (230, 215, 215)
    WING_COLOR   = (245, 230, 230)
    ACCENT_COLOR = (210, 130, 155)
    SPEED        = 18.0
    HOVER_RANGE  = 30
    WING_TYPE    = "other"

class EgyptianGrasshopper(Insect):
    SPECIES      = "egyptian_grasshopper"
    RARITY       = "common"
    BIOMES       = ["savanna", "steppe", "arid_steppe"]
    W, H         = 12, 6
    BODY_COLOR   = (110, 90, 50)
    WING_COLOR   = (155, 130, 75)
    ACCENT_COLOR = (195, 170, 110)
    HOVER_RANGE  = 55
    SPEED        = 34.0
    WING_TYPE    = "other"

class SahariCricket(Insect):
    SPECIES      = "sahari_cricket"
    RARITY       = "common"
    BIOMES       = ["desert", "arid_steppe"]
    W, H         = 10, 6
    BODY_COLOR   = (150, 125, 80)
    WING_COLOR   = (175, 148, 100)
    ACCENT_COLOR = (210, 185, 135)
    SPEED        = 30.0
    WING_TYPE    = "other"

class DesertKatydid(Insect):
    SPECIES      = "desert_katydid"
    RARITY       = "common"
    BIOMES       = ["desert", "arid_steppe", "canyon", "red_rock"]
    W, H         = 11, 7
    BODY_COLOR   = (175, 155, 95)
    WING_COLOR   = (205, 185, 130)
    ACCENT_COLOR = (230, 215, 170)
    HOVER_RANGE  = 45
    WING_TYPE    = "other"

class MudDauberWasp(Insect):
    SPECIES      = "mud_dauber_wasp"
    RARITY       = "uncommon"
    BIOMES       = ["desert", "arid_steppe", "steppe"]
    W, H         = 11, 6
    BODY_COLOR   = (20, 18, 10)
    WING_COLOR   = (185, 205, 225)
    ACCENT_COLOR = (220, 185, 35)
    SPEED        = 34.0
    WING_TYPE    = "other"

class ArabianBee(Insect):
    SPECIES      = "arabian_bee"
    RARITY       = "common"
    BIOMES       = ["desert", "steppe", "arid_steppe"]
    W, H         = 8, 6
    BODY_COLOR   = (30, 22, 8)
    WING_COLOR   = (205, 225, 240)
    ACCENT_COLOR = (200, 145, 20)
    WING_TYPE    = "bee"

class ArabianAssassinBug(Insect):
    SPECIES      = "arabian_assassin_bug"
    RARITY       = "uncommon"
    BIOMES       = ["desert", "arid_steppe", "canyon", "red_rock"]
    W, H         = 10, 6
    BODY_COLOR   = (30, 15, 12)
    WING_COLOR   = (55, 28, 22)
    ACCENT_COLOR = (190, 50, 35)
    SPEED        = 28.0
    WING_TYPE    = "other"

class FireBug(Insect):
    SPECIES      = "fire_bug"
    RARITY       = "common"
    BIOMES       = ["steppe", "rolling_hills", "arid_steppe"]
    W, H         = 8, 6
    BODY_COLOR   = (170, 25, 20)
    WING_COLOR   = (195, 32, 25)
    ACCENT_COLOR = (15, 12, 12)
    WING_TYPE    = "other"

class PalestineMoleCricket(Insect):
    SPECIES      = "palestine_mole_cricket"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "steppe"]
    W, H         = 12, 7
    BODY_COLOR   = (100, 75, 40)
    WING_COLOR   = (130, 100, 55)
    ACCENT_COLOR = (165, 130, 75)
    SPEED        = 22.0
    HOVER_RANGE  = 35
    WING_TYPE    = "other"

class ScorpionFly(Insect):
    SPECIES      = "scorpion_fly"
    RARITY       = "uncommon"
    BIOMES       = ["steppe", "rolling_hills", "arid_steppe"]
    W, H         = 10, 6
    BODY_COLOR   = (140, 80, 30)
    WING_COLOR   = (175, 155, 110)
    ACCENT_COLOR = (215, 120, 50)
    WING_TYPE    = "other"

class DesertTermite(Insect):
    SPECIES      = "desert_termite"
    RARITY       = "common"
    BIOMES       = ["desert", "arid_steppe"]
    W, H         = 7, 5
    BODY_COLOR   = (210, 195, 160)
    WING_COLOR   = (230, 220, 195)
    ACCENT_COLOR = (250, 240, 220)
    SPEED        = 20.0
    HOVER_RANGE  = 30
    WING_TYPE    = "other"

class GlowWorm(Insect):
    SPECIES      = "glow_worm"
    RARITY       = "uncommon"
    BIOMES       = ["rolling_hills", "temperate"]
    W, H         = 8, 5
    BODY_COLOR   = (38, 45, 28)
    WING_COLOR   = (55, 62, 40)
    ACCENT_COLOR = (130, 230, 60)
    SPEED        = 18.0
    HOVER_RANGE  = 25
    WING_TYPE    = "firefly"
    NIGHT_ONLY   = True

class EuropeanMantis(Insect):
    SPECIES      = "european_mantis"
    RARITY       = "uncommon"
    BIOMES       = ["steppe", "arid_steppe", "rolling_hills"]
    W, H         = 10, 12
    BODY_COLOR   = (55, 130, 55)
    WING_COLOR   = (72, 160, 72)
    ACCENT_COLOR = (110, 200, 110)
    SPEED        = 20.0
    WING_TYPE    = "other"

class FieldGrasshopper(Insect):
    SPECIES      = "field_grasshopper"
    RARITY       = "common"
    BIOMES       = ["rolling_hills", "steppe", "temperate"]
    W, H         = 11, 6
    BODY_COLOR   = (80, 100, 45)
    WING_COLOR   = (115, 140, 65)
    ACCENT_COLOR = (160, 185, 100)
    HOVER_RANGE  = 55
    SPEED        = 33.0
    WING_TYPE    = "other"

class GreatGreenBushCricket(Insect):
    SPECIES      = "great_green_bush_cricket"
    RARITY       = "common"
    BIOMES       = ["rolling_hills", "steppe"]
    W, H         = 13, 7
    BODY_COLOR   = (45, 125, 40)
    WING_COLOR   = (62, 165, 55)
    ACCENT_COLOR = (110, 215, 100)
    HOVER_RANGE  = 45
    WING_TYPE    = "other"

class NewForestCicada(Insect):
    SPECIES      = "new_forest_cicada"
    RARITY       = "rare"
    BIOMES       = ["boreal", "temperate"]
    W, H         = 12, 7
    BODY_COLOR   = (50, 75, 35)
    WING_COLOR   = (130, 165, 105)
    ACCENT_COLOR = (80, 115, 58)
    WING_TYPE    = "other"

class EuropeanHornet(Insect):
    SPECIES      = "european_hornet"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "birch_forest", "boreal"]
    W, H         = 12, 7
    BODY_COLOR   = (35, 28, 8)
    WING_COLOR   = (205, 220, 235)
    ACCENT_COLOR = (215, 170, 20)
    SPEED        = 33.0
    WING_TYPE    = "other"

class BeeWolf(Insect):
    SPECIES      = "bee_wolf"
    RARITY       = "uncommon"
    BIOMES       = ["rolling_hills", "steppe", "beach"]
    W, H         = 11, 6
    BODY_COLOR   = (22, 20, 10)
    WING_COLOR   = (195, 210, 230)
    ACCENT_COLOR = (220, 190, 30)
    SPEED        = 34.0
    WING_TYPE    = "other"

class ForestBug(Insect):
    SPECIES      = "forest_bug"
    RARITY       = "common"
    BIOMES       = ["boreal", "birch_forest", "temperate"]
    W, H         = 9, 7
    BODY_COLOR   = (80, 45, 18)
    WING_COLOR   = (105, 60, 24)
    ACCENT_COLOR = (195, 130, 50)
    WING_TYPE    = "other"

class AlpineGrasshopper(Insect):
    SPECIES      = "alpine_grasshopper"
    RARITY       = "uncommon"
    BIOMES       = ["alpine_mountain", "rocky_mountain"]
    W, H         = 11, 6
    BODY_COLOR   = (45, 80, 75)
    WING_COLOR   = (65, 115, 108)
    ACCENT_COLOR = (110, 185, 175)
    HOVER_RANGE  = 40
    WING_TYPE    = "other"

class WaterScorpion(Insect):
    SPECIES      = "water_scorpion"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "swamp"]
    W, H         = 12, 6
    BODY_COLOR   = (70, 55, 32)
    WING_COLOR   = (90, 72, 42)
    ACCENT_COLOR = (125, 100, 60)
    SPEED        = 18.0
    HOVER_RANGE  = 30
    WING_TYPE    = "other"

class IndianWalkingStick(Insect):
    SPECIES      = "indian_walking_stick"
    RARITY       = "common"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 14, 4
    BODY_COLOR   = (75, 105, 52)
    WING_COLOR   = (88, 118, 62)
    ACCENT_COLOR = (110, 145, 78)
    SPEED        = 16.0
    HOVER_RANGE  = 25
    WING_TYPE    = "other"

class GiantAfricanMantis(Insect):
    SPECIES      = "giant_african_mantis"
    RARITY       = "uncommon"
    BIOMES       = ["savanna", "jungle"]
    W, H         = 11, 13
    BODY_COLOR   = (155, 185, 115)
    WING_COLOR   = (180, 210, 135)
    ACCENT_COLOR = (210, 235, 165)
    SPEED        = 20.0
    WING_TYPE    = "other"

class PrairieLocust(Insect):
    SPECIES      = "prairie_locust"
    RARITY       = "common"
    BIOMES       = ["steppe", "rolling_hills"]
    W, H         = 12, 6
    BODY_COLOR   = (115, 95, 55)
    WING_COLOR   = (155, 132, 80)
    ACCENT_COLOR = (195, 170, 112)
    HOVER_RANGE  = 55
    SPEED        = 33.0
    WING_TYPE    = "other"

class TundraBumblebee(Insect):
    SPECIES      = "tundra_bumblebee"
    RARITY       = "uncommon"
    BIOMES       = ["tundra", "alpine_mountain"]
    W, H         = 9, 7
    BODY_COLOR   = (28, 22, 8)
    WING_COLOR   = (210, 228, 242)
    ACCENT_COLOR = (218, 190, 30)
    WING_TYPE    = "bee"

class CarpenterBee(Insect):
    SPECIES      = "carpenter_bee"
    RARITY       = "common"
    BIOMES       = ["tropical", "savanna", "jungle"]
    W, H         = 10, 7
    BODY_COLOR   = (18, 18, 28)
    WING_COLOR   = (175, 195, 225)
    ACCENT_COLOR = (55, 55, 100)
    WING_TYPE    = "bee"

class JungleAssassinBug(Insect):
    SPECIES      = "jungle_assassin_bug"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 10, 6
    BODY_COLOR   = (22, 12, 10)
    WING_COLOR   = (40, 22, 18)
    ACCENT_COLOR = (185, 40, 28)
    SPEED        = 28.0
    WING_TYPE    = "other"

class GiantWeta(Insect):
    SPECIES      = "giant_weta"
    RARITY       = "rare"
    BIOMES       = ["rocky_mountain", "boreal"]
    W, H         = 14, 7
    BODY_COLOR   = (95, 72, 38)
    WING_COLOR   = (118, 90, 48)
    ACCENT_COLOR = (155, 120, 70)
    SPEED        = 15.0
    HOVER_RANGE  = 25
    WING_TYPE    = "other"

class AfricanMoleCricket(Insect):
    SPECIES      = "african_mole_cricket"
    RARITY       = "common"
    BIOMES       = ["savanna", "wetland"]
    W, H         = 12, 7
    BODY_COLOR   = (110, 82, 42)
    WING_COLOR   = (138, 105, 55)
    ACCENT_COLOR = (172, 135, 75)
    SPEED        = 22.0
    HOVER_RANGE  = 35
    WING_TYPE    = "other"

class ArcticBumblebee(Insect):
    SPECIES      = "arctic_bumblebee"
    RARITY       = "uncommon"
    BIOMES       = ["tundra", "alpine_mountain"]
    W, H         = 9, 7
    BODY_COLOR   = (28, 22, 8)
    WING_COLOR   = (205, 225, 240)
    ACCENT_COLOR = (240, 230, 210)
    WING_TYPE    = "bee"

class TropicalMantis(Insect):
    SPECIES      = "tropical_mantis"
    RARITY       = "uncommon"
    BIOMES       = ["tropical", "jungle"]
    W, H         = 10, 11
    BODY_COLOR   = (160, 145, 60)
    WING_COLOR   = (190, 175, 78)
    ACCENT_COLOR = (225, 210, 110)
    SPEED        = 20.0
    WING_TYPE    = "other"


# ---------------------------------------------------------------------------
# Night insects (NIGHT_ONLY = True)
# ---------------------------------------------------------------------------

# -- Nocturnal moths --

class GhostMoth(Insect):
    SPECIES      = "ghost_moth"
    RARITY       = "rare"
    BIOMES       = ["temperate", "boreal", "birch_forest"]
    W, H         = 16, 10
    BODY_COLOR   = (235, 230, 220)
    WING_COLOR   = (245, 242, 238)
    ACCENT_COLOR = (208, 200, 185)
    HOVER_RANGE  = 70
    SPEED        = 22.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class CometMoth(Insect):
    SPECIES      = "comet_moth"
    RARITY       = "rare"
    BIOMES       = ["jungle"]
    W, H         = 17, 11
    BODY_COLOR   = (155, 125, 40)
    WING_COLOR   = (235, 195, 55)
    ACCENT_COLOR = (195, 65, 35)
    HOVER_RANGE  = 65
    SPEED        = 20.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class VampireMoth(Insect):
    SPECIES      = "vampire_moth"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 14, 9
    BODY_COLOR   = (65, 42, 28)
    WING_COLOR   = (88, 58, 38)
    ACCENT_COLOR = (145, 48, 35)
    HOVER_RANGE  = 55
    SPEED        = 24.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class BogongMoth(Insect):
    SPECIES      = "bogong_moth"
    RARITY       = "uncommon"
    BIOMES       = ["alpine_mountain", "steppe"]
    W, H         = 13, 8
    BODY_COLOR   = (68, 58, 48)
    WING_COLOR   = (88, 75, 62)
    ACCENT_COLOR = (118, 105, 88)
    HOVER_RANGE  = 60
    SPEED        = 26.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class UnderwingMoth(Insect):
    SPECIES      = "underwing_moth"
    RARITY       = "common"
    BIOMES       = ["temperate", "boreal", "rolling_hills"]
    W, H         = 14, 8
    BODY_COLOR   = (88, 80, 68)
    WING_COLOR   = (108, 98, 85)
    ACCENT_COLOR = (195, 45, 35)
    HOVER_RANGE  = 60
    SPEED        = 24.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


# -- Bioluminescent --

class RailroadWorm(Insect):
    SPECIES      = "railroad_worm"
    RARITY       = "rare"
    BIOMES       = ["wetland", "jungle", "swamp"]
    W, H         = 10, 5
    BODY_COLOR   = (28, 32, 18)
    WING_COLOR   = (38, 42, 25)
    ACCENT_COLOR = (45, 220, 45)
    HOVER_RANGE  = 30
    SPEED        = 18.0
    WING_TYPE    = "firefly"
    NIGHT_ONLY   = True


class AsianFirefly(Insect):
    SPECIES      = "asian_firefly"
    RARITY       = "common"
    BIOMES       = ["jungle", "east_asian", "tropical"]
    W, H         = 7, 5
    BODY_COLOR   = (25, 28, 15)
    WING_COLOR   = (42, 48, 28)
    ACCENT_COLOR = (205, 255, 70)
    HOVER_RANGE  = 45
    SPEED        = 20.0
    WING_TYPE    = "firefly"
    NIGHT_ONLY   = True


# -- Nocturnal beetles --

class NocturnalGroundBeetle(Insect):
    SPECIES      = "nocturnal_ground_beetle"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills", "wasteland"]
    W, H         = 12, 7
    BODY_COLOR   = (18, 15, 20)
    WING_COLOR   = (28, 25, 32)
    ACCENT_COLOR = (55, 48, 62)
    HOVER_RANGE  = 35
    SPEED        = 22.0
    WING_TYPE    = "beetle"
    NIGHT_ONLY   = True


# -- Nocturnal crickets and cockroaches --

class CaveCricket(Insect):
    SPECIES      = "cave_cricket"
    RARITY       = "uncommon"
    BIOMES       = ["canyon", "red_rock", "rocky_mountain"]
    W, H         = 13, 7
    BODY_COLOR   = (195, 168, 128)
    WING_COLOR   = (178, 152, 112)
    ACCENT_COLOR = (215, 195, 158)
    HOVER_RANGE  = 45
    SPEED        = 26.0
    WING_TYPE    = "other"
    NIGHT_ONLY   = True


class JungleCricket(Insect):
    SPECIES      = "jungle_cricket"
    RARITY       = "common"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 12, 6
    BODY_COLOR   = (55, 118, 42)
    WING_COLOR   = (72, 148, 58)
    ACCENT_COLOR = (95, 178, 75)
    HOVER_RANGE  = 48
    SPEED        = 28.0
    WING_TYPE    = "other"
    NIGHT_ONLY   = True


class MadagascarHissingCockroach(Insect):
    SPECIES      = "madagascar_hissing_cockroach"
    RARITY       = "rare"
    BIOMES       = ["jungle"]
    W, H         = 15, 8
    BODY_COLOR   = (88, 52, 22)
    WING_COLOR   = (108, 68, 32)
    ACCENT_COLOR = (128, 88, 48)
    HOVER_RANGE  = 38
    SPEED        = 30.0
    WING_TYPE    = "other"
    NIGHT_ONLY   = True


class TropicalCockroach(Insect):
    SPECIES      = "tropical_cockroach"
    RARITY       = "uncommon"
    BIOMES       = ["tropical", "swamp"]
    W, H         = 11, 6
    BODY_COLOR   = (115, 55, 25)
    WING_COLOR   = (138, 72, 35)
    ACCENT_COLOR = (162, 95, 52)
    HOVER_RANGE  = 40
    SPEED        = 32.0
    WING_TYPE    = "other"
    NIGHT_ONLY   = True


# ---------------------------------------------------------------------------
# Night insects batch 2 (NIGHT_ONLY = True)
# ---------------------------------------------------------------------------

# -- Moths --

class BlackWitchMoth(Insect):
    SPECIES      = "black_witch_moth"
    RARITY       = "rare"
    BIOMES       = ["tropical", "jungle"]
    W, H         = 18, 11
    BODY_COLOR   = (22, 18, 15)
    WING_COLOR   = (35, 28, 22)
    ACCENT_COLOR = (58, 45, 35)
    HOVER_RANGE  = 75
    SPEED        = 22.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class SaturnidMoth(Insect):
    SPECIES      = "saturnid_moth"
    RARITY       = "uncommon"
    BIOMES       = ["redwood", "boreal", "birch_forest"]
    W, H         = 16, 10
    BODY_COLOR   = (95, 62, 25)
    WING_COLOR   = (142, 92, 35)
    ACCENT_COLOR = (62, 28, 8)
    HOVER_RANGE  = 68
    SPEED        = 21.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class SilkMoth(Insect):
    SPECIES      = "silk_moth"
    RARITY       = "common"
    BIOMES       = ["east_asian", "south_asian"]
    W, H         = 14, 9
    BODY_COLOR   = (218, 198, 158)
    WING_COLOR   = (232, 215, 180)
    ACCENT_COLOR = (175, 142, 88)
    HOVER_RANGE  = 55
    SPEED        = 20.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class OwletMoth(Insect):
    SPECIES      = "owlet_moth"
    RARITY       = "common"
    BIOMES       = ["temperate", "steppe", "mediterranean"]
    W, H         = 12, 7
    BODY_COLOR   = (82, 78, 65)
    WING_COLOR   = (105, 100, 85)
    ACCENT_COLOR = (128, 122, 102)
    HOVER_RANGE  = 58
    SPEED        = 24.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class DesertMoonMoth(Insect):
    SPECIES      = "desert_moon_moth"
    RARITY       = "uncommon"
    BIOMES       = ["desert", "arid_steppe"]
    W, H         = 15, 9
    BODY_COLOR   = (215, 210, 198)
    WING_COLOR   = (228, 224, 215)
    ACCENT_COLOR = (175, 168, 152)
    HOVER_RANGE  = 65
    SPEED        = 22.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class AfricanMoonMoth(Insect):
    SPECIES      = "african_moon_moth"
    RARITY       = "uncommon"
    BIOMES       = ["savanna", "tropical"]
    W, H         = 15, 10
    BODY_COLOR   = (85, 158, 72)
    WING_COLOR   = (105, 188, 88)
    ACCENT_COLOR = (145, 218, 125)
    HOVER_RANGE  = 65
    SPEED        = 21.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


# -- Fireflies / bioluminescent --

class TropicalFirefly(Insect):
    SPECIES      = "tropical_firefly"
    RARITY       = "common"
    BIOMES       = ["tropical", "savanna"]
    W, H         = 7, 5
    BODY_COLOR   = (22, 24, 12)
    WING_COLOR   = (35, 38, 18)
    ACCENT_COLOR = (255, 242, 45)
    HOVER_RANGE  = 45
    SPEED        = 20.0
    WING_TYPE    = "firefly"
    NIGHT_ONLY   = True


class MountainFirefly(Insect):
    SPECIES      = "mountain_firefly"
    RARITY       = "uncommon"
    BIOMES       = ["alpine_mountain", "rocky_mountain"]
    W, H         = 7, 5
    BODY_COLOR   = (18, 22, 22)
    WING_COLOR   = (30, 38, 36)
    ACCENT_COLOR = (75, 238, 195)
    HOVER_RANGE  = 38
    SPEED        = 18.0
    WING_TYPE    = "firefly"
    NIGHT_ONLY   = True


class CaveGlowworm(Insect):
    SPECIES      = "cave_glowworm"
    RARITY       = "rare"
    BIOMES       = ["canyon", "red_rock", "rocky_mountain"]
    W, H         = 8, 4
    BODY_COLOR   = (25, 30, 22)
    WING_COLOR   = (35, 42, 30)
    ACCENT_COLOR = (88, 218, 148)
    HOVER_RANGE  = 25
    SPEED        = 15.0
    WING_TYPE    = "firefly"
    NIGHT_ONLY   = True


# -- Beetles --

class DarklingBeetle(Insect):
    SPECIES      = "darkling_beetle"
    RARITY       = "common"
    BIOMES       = ["desert", "arid_steppe"]
    W, H         = 11, 6
    BODY_COLOR   = (22, 18, 15)
    WING_COLOR   = (32, 28, 22)
    ACCENT_COLOR = (48, 42, 36)
    HOVER_RANGE  = 32
    SPEED        = 22.0
    WING_TYPE    = "beetle"
    NIGHT_ONLY   = True


class OilBeetle(Insect):
    SPECIES      = "oil_beetle"
    RARITY       = "uncommon"
    BIOMES       = ["mediterranean", "temperate"]
    W, H         = 12, 7
    BODY_COLOR   = (32, 25, 48)
    WING_COLOR   = (42, 32, 62)
    ACCENT_COLOR = (58, 45, 88)
    HOVER_RANGE  = 35
    SPEED        = 20.0
    WING_TYPE    = "beetle"
    NIGHT_ONLY   = True


class WoodBoringBeetle(Insect):
    SPECIES      = "wood_boring_beetle"
    RARITY       = "common"
    BIOMES       = ["boreal", "redwood"]
    W, H         = 11, 6
    BODY_COLOR   = (68, 45, 22)
    WING_COLOR   = (85, 58, 32)
    ACCENT_COLOR = (108, 75, 45)
    HOVER_RANGE  = 32
    SPEED        = 21.0
    WING_TYPE    = "beetle"
    NIGHT_ONLY   = True


# -- Other nocturnal insects --

class NightCicada(Insect):
    SPECIES      = "night_cicada"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "mediterranean", "savanna"]
    W, H         = 13, 7
    BODY_COLOR   = (42, 48, 32)
    WING_COLOR   = (62, 70, 48)
    ACCENT_COLOR = (85, 95, 65)
    HOVER_RANGE  = 52
    SPEED        = 28.0
    WING_TYPE    = "other"
    NIGHT_ONLY   = True


class JungleKatydid(Insect):
    SPECIES      = "jungle_katydid"
    RARITY       = "common"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 14, 7
    BODY_COLOR   = (45, 118, 35)
    WING_COLOR   = (58, 148, 45)
    ACCENT_COLOR = (78, 172, 62)
    HOVER_RANGE  = 50
    SPEED        = 28.0
    WING_TYPE    = "other"
    NIGHT_ONLY   = True


class Earwig(Insect):
    SPECIES      = "earwig"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills", "steep_hills"]
    W, H         = 11, 5
    BODY_COLOR   = (108, 72, 35)
    WING_COLOR   = (88, 58, 25)
    ACCENT_COLOR = (148, 105, 58)
    HOVER_RANGE  = 40
    SPEED        = 26.0
    WING_TYPE    = "other"
    NIGHT_ONLY   = True


class TundraCricket(Insect):
    SPECIES      = "tundra_cricket"
    RARITY       = "uncommon"
    BIOMES       = ["tundra", "alpine_mountain"]
    W, H         = 11, 6
    BODY_COLOR   = (65, 58, 45)
    WING_COLOR   = (85, 75, 58)
    ACCENT_COLOR = (110, 98, 78)
    HOVER_RANGE  = 42
    SPEED        = 26.0
    WING_TYPE    = "other"
    NIGHT_ONLY   = True


class WaterBoatman(Insect):
    SPECIES      = "water_boatman"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "beach"]
    W, H         = 10, 5
    BODY_COLOR   = (35, 52, 48)
    WING_COLOR   = (48, 68, 62)
    ACCENT_COLOR = (65, 92, 85)
    HOVER_RANGE  = 38
    SPEED        = 24.0
    WING_TYPE    = "other"
    NIGHT_ONLY   = True


class NightMantis(Insect):
    SPECIES      = "night_mantis"
    RARITY       = "uncommon"
    BIOMES       = ["savanna", "arid_steppe"]
    W, H         = 11, 13
    BODY_COLOR   = (32, 38, 22)
    WING_COLOR   = (45, 52, 32)
    ACCENT_COLOR = (62, 72, 46)
    HOVER_RANGE  = 35
    SPEED        = 18.0
    WING_TYPE    = "other"
    NIGHT_ONLY   = True


class GlowingMillipede(Insect):
    SPECIES      = "glowing_millipede"
    RARITY       = "rare"
    BIOMES       = ["jungle", "swamp"]
    W, H         = 12, 5
    BODY_COLOR   = (28, 35, 20)
    WING_COLOR   = (38, 48, 28)
    ACCENT_COLOR = (38, 210, 135)
    HOVER_RANGE  = 25
    SPEED        = 15.0
    WING_TYPE    = "firefly"
    NIGHT_ONLY   = True


class SandRoach(Insect):
    SPECIES      = "sand_roach"
    RARITY       = "uncommon"
    BIOMES       = ["desert", "beach"]
    W, H         = 12, 6
    BODY_COLOR   = (185, 158, 108)
    WING_COLOR   = (205, 178, 128)
    ACCENT_COLOR = (218, 195, 148)
    HOVER_RANGE  = 40
    SPEED        = 32.0
    WING_TYPE    = "other"
    NIGHT_ONLY   = True


# ---------------------------------------------------------------------------
# Water insects
# ---------------------------------------------------------------------------

class PondSkater(Insect):
    SPECIES      = "pond_skater"
    RARITY       = "common"
    BIOMES       = ["wetland", "swamp"]
    W, H         = 13, 4
    BODY_COLOR   = (42, 50, 58)
    WING_COLOR   = (62, 72, 82)
    ACCENT_COLOR = (120, 148, 168)
    HOVER_RANGE  = 50
    SPEED        = 36.0
    WING_TYPE    = "other"


class WhirligigBeetle(Insect):
    SPECIES      = "whirligig_beetle"
    RARITY       = "common"
    BIOMES       = ["wetland", "beach"]
    W, H         = 8, 5
    BODY_COLOR   = (18, 22, 18)
    WING_COLOR   = (32, 38, 32)
    ACCENT_COLOR = (80, 105, 80)
    HOVER_RANGE  = 35
    SPEED        = 38.0
    WING_TYPE    = "beetle"


class MayflySilver(Insect):
    SPECIES      = "mayfly_silver"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "swamp"]
    W, H         = 12, 5
    BODY_COLOR   = (185, 195, 210)
    WING_COLOR   = (215, 228, 248)
    ACCENT_COLOR = (240, 248, 255)
    HOVER_RANGE  = 55
    SPEED        = 30.0
    WING_TYPE    = "dragonfly"
    DAWN_ONLY    = True


class StoneflyRiver(Insect):
    SPECIES      = "stonefly_river"
    RARITY       = "common"
    BIOMES       = ["wetland", "boreal"]
    W, H         = 11, 5
    BODY_COLOR   = (72, 62, 45)
    WING_COLOR   = (105, 92, 70)
    ACCENT_COLOR = (148, 132, 100)
    HOVER_RANGE  = 30
    SPEED        = 22.0
    WING_TYPE    = "moth"
    DAWN_ONLY    = True


class CaddisflyGold(Insect):
    SPECIES      = "caddisfly_gold"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "swamp"]
    W, H         = 11, 6
    BODY_COLOR   = (115, 92, 38)
    WING_COLOR   = (168, 138, 68)
    ACCENT_COLOR = (210, 178, 105)
    HOVER_RANGE  = 40
    SPEED        = 25.0
    WING_TYPE    = "moth"
    DUSK_ONLY    = True


class WaterMeasurer(Insect):
    SPECIES      = "water_measurer"
    RARITY       = "rare"
    BIOMES       = ["wetland", "swamp"]
    W, H         = 14, 3
    BODY_COLOR   = (52, 48, 38)
    WING_COLOR   = (78, 72, 58)
    ACCENT_COLOR = (130, 120, 95)
    HOVER_RANGE  = 28
    SPEED        = 18.0
    WING_TYPE    = "other"


class MarshSpreadwing(Insect):
    SPECIES      = "marsh_spreadwing"
    RARITY       = "uncommon"
    BIOMES       = ["swamp", "wetland"]
    W, H         = 13, 5
    BODY_COLOR   = (55, 105, 68)
    WING_COLOR   = (88, 162, 108)
    ACCENT_COLOR = (140, 210, 165)
    HOVER_RANGE  = 48
    SPEED        = 28.0
    WING_TYPE    = "dragonfly"


class RiverHawker(Insect):
    SPECIES      = "river_hawker"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "swamp"]
    W, H         = 15, 6
    BODY_COLOR   = (28, 70, 125)
    WING_COLOR   = (68, 128, 195)
    ACCENT_COLOR = (145, 195, 248)
    HOVER_RANGE  = 65
    SPEED        = 35.0
    WING_TYPE    = "dragonfly"


class TealGlosskirt(Insect):
    SPECIES      = "teal_glosskirt"
    RARITY       = "rare"
    BIOMES       = ["swamp", "wetland"]
    W, H         = 13, 6
    BODY_COLOR   = (20, 88, 85)
    WING_COLOR   = (35, 148, 142)
    ACCENT_COLOR = (75, 210, 200)
    HOVER_RANGE  = 42
    SPEED        = 27.0
    WING_TYPE    = "dragonfly"


class PlumedMidge(Insect):
    SPECIES      = "plumed_midge"
    RARITY       = "common"
    BIOMES       = ["wetland", "swamp", "beach"]
    W, H         = 7, 5
    BODY_COLOR   = (55, 62, 52)
    WING_COLOR   = (115, 128, 110)
    ACCENT_COLOR = (175, 192, 168)
    HOVER_RANGE  = 60
    SPEED        = 40.0
    WING_TYPE    = "other"


class BogSkimmer(Insect):
    SPECIES      = "bog_skimmer"
    RARITY       = "uncommon"
    BIOMES       = ["swamp", "wetland"]
    W, H         = 13, 5
    BODY_COLOR   = (88, 58, 28)
    WING_COLOR   = (140, 95, 48)
    ACCENT_COLOR = (200, 155, 85)
    HOVER_RANGE  = 50
    SPEED        = 30.0
    WING_TYPE    = "dragonfly"


class MarshFirefly(Insect):
    SPECIES      = "marsh_firefly"
    RARITY       = "uncommon"
    BIOMES       = ["swamp", "wetland"]
    W, H         = 8, 5
    BODY_COLOR   = (28, 38, 22)
    WING_COLOR   = (45, 58, 35)
    ACCENT_COLOR = (80, 230, 80)
    HOVER_RANGE  = 52
    SPEED        = 24.0
    WING_TYPE    = "firefly"
    NIGHT_ONLY   = True


class WetlandGlowfly(Insect):
    SPECIES      = "wetland_glowfly"
    RARITY       = "rare"
    BIOMES       = ["wetland", "swamp"]
    W, H         = 9, 5
    BODY_COLOR   = (22, 32, 28)
    WING_COLOR   = (38, 55, 48)
    ACCENT_COLOR = (60, 235, 185)
    HOVER_RANGE  = 58
    SPEED        = 22.0
    WING_TYPE    = "firefly"
    NIGHT_ONLY   = True


class RiverDivingBeetle(Insect):
    SPECIES      = "river_diving_beetle"
    RARITY       = "common"
    BIOMES       = ["wetland", "beach"]
    W, H         = 10, 6
    BODY_COLOR   = (32, 50, 38)
    WING_COLOR   = (48, 72, 55)
    ACCENT_COLOR = (85, 125, 95)
    HOVER_RANGE  = 32
    SPEED        = 26.0
    WING_TYPE    = "beetle"


class SwampRiflebeetle(Insect):
    SPECIES      = "swamp_riflebeetle"
    RARITY       = "uncommon"
    BIOMES       = ["swamp", "wetland"]
    W, H         = 11, 5
    BODY_COLOR   = (25, 40, 28)
    WING_COLOR   = (40, 62, 45)
    ACCENT_COLOR = (72, 108, 80)
    HOVER_RANGE  = 28
    SPEED        = 20.0
    WING_TYPE    = "beetle"


class WaterScavengerBeetle(Insect):
    SPECIES      = "water_scavenger_beetle"
    RARITY       = "common"
    BIOMES       = ["wetland", "swamp"]
    W, H         = 11, 6
    BODY_COLOR   = (20, 28, 22)
    WING_COLOR   = (35, 48, 38)
    ACCENT_COLOR = (62, 85, 68)
    HOVER_RANGE  = 30
    SPEED        = 22.0
    WING_TYPE    = "beetle"


class ReedMarshMoth(Insect):
    SPECIES      = "reed_marsh_moth"
    RARITY       = "uncommon"
    BIOMES       = ["swamp", "wetland"]
    W, H         = 13, 7
    BODY_COLOR   = (95, 82, 55)
    WING_COLOR   = (148, 130, 90)
    ACCENT_COLOR = (192, 175, 128)
    HOVER_RANGE  = 42
    SPEED        = 22.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class BeachFoamMoth(Insect):
    SPECIES      = "beach_foam_moth"
    RARITY       = "common"
    BIOMES       = ["beach", "wetland"]
    W, H         = 12, 6
    BODY_COLOR   = (195, 188, 172)
    WING_COLOR   = (228, 222, 208)
    ACCENT_COLOR = (248, 244, 236)
    HOVER_RANGE  = 45
    SPEED        = 24.0
    WING_TYPE    = "moth"
    DUSK_ONLY    = True


class ReedMaiden(Insect):
    SPECIES        = "reed_maiden"
    RARITY         = "rare"
    BIOMES         = ["wetland"]
    W, H           = 14, 5
    BODY_COLOR     = (38, 110, 95)
    WING_COLOR     = (72, 175, 155)
    ACCENT_COLOR   = (155, 235, 218)
    HOVER_RANGE    = 45
    SPEED          = 26.0
    WING_TYPE      = "dragonfly"
    HAS_MORPH      = True
    MORPH_VARIANTS = ("golden", "albino")


class BrookJewel(Insect):
    SPECIES        = "brook_jewel"
    RARITY         = "rare"
    BIOMES         = ["wetland", "swamp"]
    W, H           = 13, 6
    BODY_COLOR     = (15, 75, 35)
    WING_COLOR     = (28, 148, 72)
    ACCENT_COLOR   = (88, 225, 138)
    HOVER_RANGE    = 40
    SPEED          = 28.0
    WING_TYPE      = "dragonfly"
    HAS_MORPH      = True
    MORPH_VARIANTS = ("melanistic", "golden")


class CraneFly(Insect):
    SPECIES      = "crane_fly"
    RARITY       = "common"
    BIOMES       = ["wetland", "swamp", "beach"]
    W, H         = 14, 5
    BODY_COLOR   = (105, 88, 58)
    WING_COLOR   = (175, 162, 138)
    ACCENT_COLOR = (215, 205, 185)
    HOVER_RANGE  = 55
    SPEED        = 28.0
    WING_TYPE    = "other"


class WaterGnat(Insect):
    SPECIES      = "water_gnat"
    RARITY       = "common"
    BIOMES       = ["wetland", "swamp", "beach"]
    W, H         = 7, 4
    BODY_COLOR   = (38, 42, 38)
    WING_COLOR   = (88, 98, 88)
    ACCENT_COLOR = (155, 172, 155)
    HOVER_RANGE  = 65
    SPEED        = 42.0
    WING_TYPE    = "other"


class SwampDragonlet(Insect):
    SPECIES      = "swamp_dragonlet"
    RARITY       = "uncommon"
    BIOMES       = ["swamp", "wetland"]
    W, H         = 11, 5
    BODY_COLOR   = (95, 28, 28)
    WING_COLOR   = (148, 48, 48)
    ACCENT_COLOR = (210, 105, 85)
    HOVER_RANGE  = 45
    SPEED        = 32.0
    WING_TYPE    = "dragonfly"


class BluetailPondfly(Insect):
    SPECIES      = "bluetail_pondfly"
    RARITY       = "common"
    BIOMES       = ["wetland", "swamp"]
    W, H         = 12, 5
    BODY_COLOR   = (28, 52, 105)
    WING_COLOR   = (55, 98, 175)
    ACCENT_COLOR = (120, 175, 245)
    HOVER_RANGE  = 48
    SPEED        = 30.0
    WING_TYPE    = "dragonfly"


class MoonlitPondskipper(Insect):
    SPECIES      = "moonlit_pondskipper"
    RARITY       = "rare"
    BIOMES       = ["wetland", "swamp"]
    W, H         = 10, 5
    BODY_COLOR   = (38, 42, 55)
    WING_COLOR   = (72, 80, 108)
    ACCENT_COLOR = (178, 188, 228)
    HOVER_RANGE  = 50
    SPEED        = 25.0
    WING_TYPE    = "other"
    NIGHT_ONLY   = True


class GreatPondDamsel(Insect):
    SPECIES      = "great_pond_damsel"
    RARITY       = "common"
    BIOMES       = ["wetland", "swamp"]
    W, H         = 13, 5
    BODY_COLOR   = (30, 88, 148)
    WING_COLOR   = (62, 138, 210)
    ACCENT_COLOR = (145, 200, 255)
    HOVER_RANGE  = 52
    SPEED        = 28.0
    WING_TYPE    = "dragonfly"


class CopperDemoiselle(Insect):
    SPECIES      = "copper_demoiselle"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "beach"]
    W, H         = 12, 5
    BODY_COLOR   = (120, 65, 12)
    WING_COLOR   = (188, 108, 28)
    ACCENT_COLOR = (240, 170, 75)
    HOVER_RANGE  = 45
    SPEED        = 26.0
    WING_TYPE    = "dragonfly"


class BlacktipReedfly(Insect):
    SPECIES      = "blacktip_reedfly"
    RARITY       = "common"
    BIOMES       = ["wetland", "swamp"]
    W, H         = 12, 5
    BODY_COLOR   = (18, 18, 18)
    WING_COLOR   = (50, 65, 55)
    ACCENT_COLOR = (100, 130, 108)
    HOVER_RANGE  = 40
    SPEED        = 30.0
    WING_TYPE    = "dragonfly"


class SilverPondHawker(Insect):
    SPECIES      = "silver_pond_hawker"
    RARITY       = "rare"
    BIOMES       = ["wetland"]
    W, H         = 15, 6
    BODY_COLOR   = (165, 178, 195)
    WING_COLOR   = (205, 218, 235)
    ACCENT_COLOR = (240, 245, 255)
    HOVER_RANGE  = 68
    SPEED        = 36.0
    WING_TYPE    = "dragonfly"


class FenSkimmer(Insect):
    SPECIES      = "fen_skimmer"
    RARITY       = "uncommon"
    BIOMES       = ["swamp", "wetland"]
    W, H         = 13, 5
    BODY_COLOR   = (78, 42, 10)
    WING_COLOR   = (128, 72, 22)
    ACCENT_COLOR = (188, 125, 58)
    HOVER_RANGE  = 48
    SPEED        = 32.0
    WING_TYPE    = "dragonfly"


class MudMinnowfly(Insect):
    SPECIES      = "mud_minnowfly"
    RARITY       = "common"
    BIOMES       = ["swamp", "wetland"]
    W, H         = 8, 4
    BODY_COLOR   = (68, 55, 32)
    WING_COLOR   = (105, 88, 55)
    ACCENT_COLOR = (148, 128, 88)
    HOVER_RANGE  = 35
    SPEED        = 34.0
    WING_TYPE    = "other"


class WillowEmerald(Insect):
    SPECIES      = "willow_emerald"
    RARITY       = "rare"
    BIOMES       = ["wetland", "swamp"]
    W, H         = 14, 5
    BODY_COLOR   = (22, 88, 48)
    WING_COLOR   = (42, 158, 88)
    ACCENT_COLOR = (105, 228, 148)
    HOVER_RANGE  = 55
    SPEED        = 30.0
    WING_TYPE    = "dragonfly"


class WaterTreader(Insect):
    SPECIES      = "water_treader"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "swamp"]
    W, H         = 11, 3
    BODY_COLOR   = (45, 52, 42)
    WING_COLOR   = (68, 78, 62)
    ACCENT_COLOR = (112, 128, 102)
    HOVER_RANGE  = 30
    SPEED        = 20.0
    WING_TYPE    = "other"


class HoverCaddis(Insect):
    SPECIES      = "hover_caddis"
    RARITY       = "common"
    BIOMES       = ["wetland", "boreal"]
    W, H         = 10, 6
    BODY_COLOR   = (82, 70, 48)
    WING_COLOR   = (122, 105, 72)
    ACCENT_COLOR = (165, 145, 105)
    HOVER_RANGE  = 38
    SPEED        = 24.0
    WING_TYPE    = "moth"


class SwampLantern(Insect):
    SPECIES      = "swamp_lantern"
    RARITY       = "rare"
    BIOMES       = ["swamp"]
    W, H         = 9, 6
    BODY_COLOR   = (25, 35, 25)
    WING_COLOR   = (40, 55, 40)
    ACCENT_COLOR = (105, 240, 108)
    HOVER_RANGE  = 55
    SPEED        = 20.0
    WING_TYPE    = "firefly"
    NIGHT_ONLY   = True


class PondshoreGlimmer(Insect):
    SPECIES      = "pondshore_glimmer"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "beach"]
    W, H         = 8, 5
    BODY_COLOR   = (28, 38, 30)
    WING_COLOR   = (45, 60, 48)
    ACCENT_COLOR = (165, 230, 110)
    HOVER_RANGE  = 48
    SPEED        = 22.0
    WING_TYPE    = "firefly"
    NIGHT_ONLY   = True


class MarshCricket(Insect):
    SPECIES      = "marsh_cricket"
    RARITY       = "common"
    BIOMES       = ["swamp", "wetland"]
    W, H         = 11, 6
    BODY_COLOR   = (55, 72, 42)
    WING_COLOR   = (78, 102, 60)
    ACCENT_COLOR = (118, 148, 92)
    HOVER_RANGE  = 35
    SPEED        = 28.0
    WING_TYPE    = "other"


class WetlandKatydid(Insect):
    SPECIES      = "wetland_katydid"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "swamp"]
    W, H         = 13, 7
    BODY_COLOR   = (48, 82, 38)
    WING_COLOR   = (72, 118, 58)
    ACCENT_COLOR = (115, 172, 92)
    HOVER_RANGE  = 38
    SPEED        = 24.0
    WING_TYPE    = "other"


class TidalFlatBeetle(Insect):
    SPECIES      = "tidal_flat_beetle"
    RARITY       = "uncommon"
    BIOMES       = ["beach", "wetland"]
    W, H         = 10, 6
    BODY_COLOR   = (105, 92, 72)
    WING_COLOR   = (152, 135, 108)
    ACCENT_COLOR = (195, 178, 148)
    HOVER_RANGE  = 30
    SPEED        = 28.0
    WING_TYPE    = "beetle"


class SaltmarshWeevil(Insect):
    SPECIES      = "saltmarsh_weevil"
    RARITY       = "common"
    BIOMES       = ["beach", "wetland"]
    W, H         = 9, 5
    BODY_COLOR   = (88, 72, 48)
    WING_COLOR   = (125, 105, 72)
    ACCENT_COLOR = (165, 142, 98)
    HOVER_RANGE  = 28
    SPEED        = 22.0
    WING_TYPE    = "beetle"


class ReedBeetle(Insect):
    SPECIES      = "reed_beetle"
    RARITY       = "common"
    BIOMES       = ["wetland", "swamp"]
    W, H         = 9, 5
    BODY_COLOR   = (32, 55, 28)
    WING_COLOR   = (50, 82, 44)
    ACCENT_COLOR = (90, 138, 78)
    HOVER_RANGE  = 32
    SPEED        = 24.0
    WING_TYPE    = "beetle"


class DuskReedmoth(Insect):
    SPECIES      = "dusk_reedmoth"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "swamp"]
    W, H         = 12, 7
    BODY_COLOR   = (60, 50, 35)
    WING_COLOR   = (98, 82, 58)
    ACCENT_COLOR = (148, 125, 88)
    HOVER_RANGE  = 42
    SPEED        = 20.0
    WING_TYPE    = "moth"
    DUSK_ONLY    = True


class FogMothlet(Insect):
    SPECIES      = "fog_mothlet"
    RARITY       = "common"
    BIOMES       = ["swamp", "beach"]
    W, H         = 10, 6
    BODY_COLOR   = (128, 128, 128)
    WING_COLOR   = (175, 175, 175)
    ACCENT_COLOR = (218, 218, 218)
    HOVER_RANGE  = 40
    SPEED        = 22.0
    WING_TYPE    = "moth"
    DUSK_ONLY    = True


class GoldenRushfly(Insect):
    SPECIES      = "golden_rushfly"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "swamp"]
    W, H         = 11, 5
    BODY_COLOR   = (148, 118, 28)
    WING_COLOR   = (205, 172, 55)
    ACCENT_COLOR = (248, 222, 105)
    HOVER_RANGE  = 52
    SPEED        = 32.0
    WING_TYPE    = "dragonfly"


class CinnabarMarshfly(Insect):
    SPECIES      = "cinnabar_marshfly"
    RARITY       = "rare"
    BIOMES       = ["wetland", "swamp"]
    W, H         = 12, 5
    BODY_COLOR   = (148, 22, 22)
    WING_COLOR   = (205, 48, 38)
    ACCENT_COLOR = (248, 115, 95)
    HOVER_RANGE  = 50
    SPEED        = 30.0
    WING_TYPE    = "dragonfly"


class StoneflyMoss(Insect):
    SPECIES      = "stonefly_moss"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "boreal"]
    W, H         = 10, 5
    BODY_COLOR   = (42, 58, 38)
    WING_COLOR   = (68, 90, 58)
    ACCENT_COLOR = (108, 138, 90)
    HOVER_RANGE  = 28
    SPEED        = 20.0
    WING_TYPE    = "moth"
    DAWN_ONLY    = True


class VioletWaterfly(Insect):
    SPECIES      = "violet_waterfly"
    RARITY       = "rare"
    BIOMES       = ["wetland", "swamp"]
    W, H         = 14, 6
    BODY_COLOR   = (65, 18, 105)
    WING_COLOR   = (118, 42, 185)
    ACCENT_COLOR = (195, 130, 255)
    HOVER_RANGE  = 55
    SPEED        = 28.0
    WING_TYPE    = "dragonfly"


class SpottedMayfly(Insect):
    SPECIES      = "spotted_mayfly"
    RARITY       = "common"
    BIOMES       = ["wetland", "beach"]
    W, H         = 11, 5
    BODY_COLOR   = (155, 148, 118)
    WING_COLOR   = (198, 188, 158)
    ACCENT_COLOR = (235, 225, 195)
    HOVER_RANGE  = 50
    SPEED        = 30.0
    WING_TYPE    = "dragonfly"
    DAWN_ONLY    = True


class MidnightMarshSkater(Insect):
    SPECIES      = "midnight_marsh_skater"
    RARITY       = "rare"
    BIOMES       = ["swamp", "wetland"]
    W, H         = 14, 4
    BODY_COLOR   = (18, 20, 25)
    WING_COLOR   = (35, 38, 52)
    ACCENT_COLOR = (88, 108, 178)
    HOVER_RANGE  = 55
    SPEED        = 38.0
    WING_TYPE    = "other"
    NIGHT_ONLY   = True


class ElmPondButterfly(Insect):
    SPECIES      = "elm_pond_butterfly"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "swamp"]
    W, H         = 13, 8
    BODY_COLOR   = (62, 88, 45)
    WING_COLOR   = (105, 148, 78)
    ACCENT_COLOR = (175, 218, 138)
    HOVER_RANGE  = 50
    SPEED        = 26.0
    WING_TYPE    = "butterfly"


# --- Arctic ---

class ArcticFritillary(Insect):
    SPECIES      = "arctic_fritillary"
    RARITY       = "rare"
    BIOMES       = ["tundra"]
    W, H         = 11, 9
    BODY_COLOR   = (210, 125, 35)
    WING_COLOR   = (200, 110, 25)
    ACCENT_COLOR = (245, 242, 238)
    HOVER_RANGE  = 55
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class GlacierMoth(Insect):
    SPECIES      = "glacier_moth"
    RARITY       = "uncommon"
    BIOMES       = ["tundra", "alpine_mountain"]
    W, H         = 12, 8
    BODY_COLOR   = (195, 215, 235)
    WING_COLOR   = (225, 238, 252)
    ACCENT_COLOR = (158, 185, 215)
    HOVER_RANGE  = 48
    SPEED        = 22.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class FrostMidge(Insect):
    SPECIES      = "frost_midge"
    RARITY       = "common"
    BIOMES       = ["tundra"]
    W, H         = 7, 5
    BODY_COLOR   = (18, 22, 28)
    WING_COLOR   = (180, 210, 230)
    ACCENT_COLOR = (140, 178, 205)
    HOVER_RANGE  = 35
    SPEED        = 38.0
    WING_TYPE    = "other"
    DAWN_ONLY    = True


# ---------------------------------------------------------------------------
# Asian fauna (100 species)
# ---------------------------------------------------------------------------

# --- Asian butterflies ---

class PaperKite(Insect):
    SPECIES      = "paper_kite"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 14, 10
    BODY_COLOR   = (40, 40, 40)
    WING_COLOR   = (245, 245, 240)
    ACCENT_COLOR = (20, 20, 20)
    HOVER_RANGE  = 60
    SPEED        = 24.0
    WING_TYPE    = "butterfly"


class CommonRose(Insect):
    SPECIES      = "common_rose"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 13, 10
    BODY_COLOR   = (25, 18, 22)
    WING_COLOR   = (45, 30, 38)
    ACCENT_COLOR = (215, 55, 75)
    HOVER_RANGE  = 55
    SPEED        = 28.0
    WING_TYPE    = "butterfly"


class CrimsonRose(Insect):
    SPECIES      = "crimson_rose"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 14, 11
    BODY_COLOR   = (30, 12, 18)
    WING_COLOR   = (55, 22, 32)
    ACCENT_COLOR = (235, 30, 55)
    HOVER_RANGE  = 60
    SPEED        = 28.0
    WING_TYPE    = "butterfly"


class BlueTigerButterfly(Insect):
    SPECIES      = "blue_tiger_butterfly"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 13, 10
    BODY_COLOR   = (28, 28, 38)
    WING_COLOR   = (62, 92, 178)
    ACCENT_COLOR = (235, 235, 245)
    HOVER_RANGE  = 55
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class PlainTigerAsia(Insect):
    SPECIES      = "plain_tiger_asia"
    RARITY       = "common"
    BIOMES       = ["jungle", "tropical", "savanna"]
    W, H         = 12, 9
    BODY_COLOR   = (40, 25, 12)
    WING_COLOR   = (220, 140, 40)
    ACCENT_COLOR = (35, 25, 18)
    HOVER_RANGE  = 50
    SPEED        = 28.0
    WING_TYPE    = "butterfly"


class CommonJezebel(Insect):
    SPECIES      = "common_jezebel"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 12, 9
    BODY_COLOR   = (35, 35, 35)
    WING_COLOR   = (240, 235, 220)
    ACCENT_COLOR = (235, 105, 45)
    HOVER_RANGE  = 50
    SPEED        = 28.0
    WING_TYPE    = "butterfly"


class PeacockPansy(Insect):
    SPECIES      = "peacock_pansy"
    RARITY       = "common"
    BIOMES       = ["jungle", "wetland"]
    W, H         = 12, 9
    BODY_COLOR   = (62, 42, 22)
    WING_COLOR   = (205, 145, 55)
    ACCENT_COLOR = (35, 65, 145)
    HOVER_RANGE  = 50
    SPEED        = 26.0
    WING_TYPE    = "butterfly"


class BandedPeacock(Insect):
    SPECIES      = "banded_peacock"
    RARITY       = "rare"
    BIOMES       = ["jungle"]
    W, H         = 14, 10
    BODY_COLOR   = (15, 25, 18)
    WING_COLOR   = (22, 60, 38)
    ACCENT_COLOR = (95, 215, 165)
    HOVER_RANGE  = 60
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class CommonNawab(Insect):
    SPECIES      = "common_nawab"
    RARITY       = "uncommon"
    BIOMES       = ["jungle"]
    W, H         = 13, 10
    BODY_COLOR   = (45, 38, 18)
    WING_COLOR   = (185, 170, 65)
    ACCENT_COLOR = (78, 102, 38)
    HOVER_RANGE  = 55
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class RedLacewing(Insect):
    SPECIES      = "red_lacewing"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 13, 9
    BODY_COLOR   = (38, 18, 18)
    WING_COLOR   = (215, 55, 38)
    ACCENT_COLOR = (250, 235, 220)
    HOVER_RANGE  = 55
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class MalayLacewing(Insect):
    SPECIES      = "malay_lacewing"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 13, 9
    BODY_COLOR   = (40, 18, 18)
    WING_COLOR   = (228, 75, 45)
    ACCENT_COLOR = (35, 22, 18)
    HOVER_RANGE  = 58
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class CommonMime(Insect):
    SPECIES      = "common_mime"
    RARITY       = "uncommon"
    BIOMES       = ["jungle"]
    W, H         = 13, 10
    BODY_COLOR   = (22, 22, 22)
    WING_COLOR   = (40, 40, 45)
    ACCENT_COLOR = (240, 240, 245)
    HOVER_RANGE  = 55
    SPEED        = 28.0
    WING_TYPE    = "butterfly"


class ChocolatePansy(Insect):
    SPECIES      = "chocolate_pansy"
    RARITY       = "common"
    BIOMES       = ["jungle", "wetland"]
    W, H         = 11, 8
    BODY_COLOR   = (55, 32, 18)
    WING_COLOR   = (115, 72, 38)
    ACCENT_COLOR = (185, 138, 78)
    HOVER_RANGE  = 45
    SPEED        = 26.0
    WING_TYPE    = "butterfly"


class GreatMormon(Insect):
    SPECIES      = "great_mormon"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 15, 11
    BODY_COLOR   = (18, 18, 22)
    WING_COLOR   = (35, 35, 42)
    ACCENT_COLOR = (220, 215, 235)
    HOVER_RANGE  = 65
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class JapaneseEmperor(Insect):
    SPECIES      = "japanese_emperor"
    RARITY       = "rare"
    BIOMES       = ["temperate"]
    W, H         = 15, 11
    BODY_COLOR   = (32, 18, 38)
    WING_COLOR   = (98, 62, 165)
    ACCENT_COLOR = (240, 235, 230)
    HOVER_RANGE  = 60
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class KaiserIHind(Insect):
    SPECIES      = "kaiser_i_hind"
    RARITY       = "rare"
    BIOMES       = ["alpine_mountain", "rocky_mountain"]
    W, H         = 15, 11
    BODY_COLOR   = (28, 28, 18)
    WING_COLOR   = (105, 158, 72)
    ACCENT_COLOR = (235, 195, 55)
    HOVER_RANGE  = 60
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class CommonCrow(Insect):
    SPECIES      = "common_crow_butterfly"
    RARITY       = "common"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 13, 10
    BODY_COLOR   = (15, 15, 15)
    WING_COLOR   = (35, 28, 42)
    ACCENT_COLOR = (215, 215, 220)
    HOVER_RANGE  = 50
    SPEED        = 26.0
    WING_TYPE    = "butterfly"


class ChestnutTiger(Insect):
    SPECIES      = "chestnut_tiger"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "alpine_mountain"]
    W, H         = 13, 9
    BODY_COLOR   = (55, 32, 18)
    WING_COLOR   = (155, 95, 45)
    ACCENT_COLOR = (245, 240, 220)
    HOVER_RANGE  = 55
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class AsianCommaButterfly(Insect):
    SPECIES      = "asian_comma_butterfly"
    RARITY       = "common"
    BIOMES       = ["temperate", "boreal"]
    W, H         = 11, 8
    BODY_COLOR   = (62, 32, 12)
    WING_COLOR   = (205, 125, 38)
    ACCENT_COLOR = (38, 22, 12)
    HOVER_RANGE  = 45
    SPEED        = 28.0
    WING_TYPE    = "butterfly"


class YellowOrangeTip(Insect):
    SPECIES      = "yellow_orange_tip"
    RARITY       = "common"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 11, 8
    BODY_COLOR   = (60, 50, 22)
    WING_COLOR   = (245, 220, 90)
    ACCENT_COLOR = (235, 110, 38)
    HOVER_RANGE  = 45
    SPEED        = 28.0
    WING_TYPE    = "butterfly"


class StripedAlbatross(Insect):
    SPECIES      = "striped_albatross"
    RARITY       = "common"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 12, 9
    BODY_COLOR   = (35, 35, 35)
    WING_COLOR   = (245, 240, 230)
    ACCENT_COLOR = (28, 28, 32)
    HOVER_RANGE  = 50
    SPEED        = 28.0
    WING_TYPE    = "butterfly"


class CommonGull(Insect):
    SPECIES      = "common_gull_butterfly"
    RARITY       = "common"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 11, 8
    BODY_COLOR   = (28, 28, 28)
    WING_COLOR   = (242, 240, 232)
    ACCENT_COLOR = (78, 78, 82)
    HOVER_RANGE  = 45
    SPEED        = 28.0
    WING_TYPE    = "butterfly"


class CommonSailor(Insect):
    SPECIES      = "common_sailor"
    RARITY       = "common"
    BIOMES       = ["jungle"]
    W, H         = 12, 9
    BODY_COLOR   = (22, 22, 22)
    WING_COLOR   = (32, 32, 32)
    ACCENT_COLOR = (235, 235, 235)
    HOVER_RANGE  = 50
    SPEED        = 28.0
    WING_TYPE    = "butterfly"


class BlueOakleaf(Insect):
    SPECIES      = "blue_oakleaf"
    RARITY       = "rare"
    BIOMES       = ["jungle", "temperate"]
    W, H         = 13, 10
    BODY_COLOR   = (45, 32, 18)
    WING_COLOR   = (62, 92, 158)
    ACCENT_COLOR = (105, 78, 38)
    HOVER_RANGE  = 55
    SPEED        = 28.0
    WING_TYPE    = "butterfly"


class AutumnLeafButterfly(Insect):
    SPECIES      = "autumn_leaf_butterfly"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 13, 10
    BODY_COLOR   = (62, 32, 12)
    WING_COLOR   = (185, 88, 28)
    ACCENT_COLOR = (95, 45, 18)
    HOVER_RANGE  = 50
    SPEED        = 28.0
    WING_TYPE    = "butterfly"


# --- Asian beetles ---

class JapaneseRhinocerosBeetle(Insect):
    SPECIES      = "japanese_rhinoceros_beetle"
    RARITY       = "rare"
    BIOMES       = ["temperate", "boreal"]
    W, H         = 14, 8
    BODY_COLOR   = (52, 28, 12)
    WING_COLOR   = (88, 52, 22)
    ACCENT_COLOR = (158, 108, 55)
    HOVER_RANGE  = 30
    SPEED        = 22.0
    WING_TYPE    = "beetle"


class GoldenStagBeetle(Insect):
    SPECIES      = "golden_stag_beetle"
    RARITY       = "rare"
    BIOMES       = ["jungle", "temperate"]
    W, H         = 13, 7
    BODY_COLOR   = (108, 78, 18)
    WING_COLOR   = (188, 142, 38)
    ACCENT_COLOR = (245, 220, 88)
    HOVER_RANGE  = 32
    SPEED        = 22.0
    WING_TYPE    = "beetle"


class MiyamaStagBeetle(Insect):
    SPECIES      = "miyama_stag_beetle"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "boreal", "alpine_mountain"]
    W, H         = 13, 7
    BODY_COLOR   = (62, 38, 18)
    WING_COLOR   = (118, 72, 32)
    ACCENT_COLOR = (175, 125, 65)
    HOVER_RANGE  = 30
    SPEED        = 22.0
    WING_TYPE    = "beetle"


class SaberhornLonghorn(Insect):
    SPECIES      = "saberhorn_longhorn"
    RARITY       = "uncommon"
    BIOMES       = ["jungle"]
    W, H         = 14, 6
    BODY_COLOR   = (28, 38, 22)
    WING_COLOR   = (52, 78, 42)
    ACCENT_COLOR = (138, 168, 92)
    HOVER_RANGE  = 30
    SPEED        = 24.0
    WING_TYPE    = "beetle"


class AsiaticTigerBeetle(Insect):
    SPECIES      = "asiatic_tiger_beetle"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 12, 6
    BODY_COLOR   = (22, 68, 48)
    WING_COLOR   = (38, 128, 88)
    ACCENT_COLOR = (245, 220, 92)
    HOVER_RANGE  = 32
    SPEED        = 32.0
    WING_TYPE    = "beetle"


class JapaneseRoseChafer(Insect):
    SPECIES      = "japanese_rose_chafer"
    RARITY       = "common"
    BIOMES       = ["temperate"]
    W, H         = 11, 6
    BODY_COLOR   = (60, 92, 38)
    WING_COLOR   = (108, 158, 62)
    ACCENT_COLOR = (175, 215, 95)
    HOVER_RANGE  = 30
    SPEED        = 24.0
    WING_TYPE    = "beetle"


class HimalayanLonghorn(Insect):
    SPECIES      = "himalayan_longhorn"
    RARITY       = "rare"
    BIOMES       = ["alpine_mountain", "rocky_mountain"]
    W, H         = 14, 6
    BODY_COLOR   = (32, 28, 38)
    WING_COLOR   = (62, 52, 78)
    ACCENT_COLOR = (158, 138, 195)
    HOVER_RANGE  = 32
    SPEED        = 22.0
    WING_TYPE    = "beetle"


class ThaiJewelBeetle(Insect):
    SPECIES      = "thai_jewel_beetle"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 12, 7
    BODY_COLOR   = (18, 78, 92)
    WING_COLOR   = (32, 148, 158)
    ACCENT_COLOR = (118, 235, 215)
    HOVER_RANGE  = 32
    SPEED        = 26.0
    WING_TYPE    = "beetle"


class BalinesePeacockBeetle(Insect):
    SPECIES      = "balinese_peacock_beetle"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 12, 7
    BODY_COLOR   = (22, 38, 88)
    WING_COLOR   = (38, 78, 175)
    ACCENT_COLOR = (108, 215, 188)
    HOVER_RANGE  = 32
    SPEED        = 24.0
    WING_TYPE    = "beetle"


class CelebesGoldenStag(Insect):
    SPECIES      = "celebes_golden_stag"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 13, 7
    BODY_COLOR   = (118, 78, 22)
    WING_COLOR   = (215, 158, 38)
    ACCENT_COLOR = (250, 230, 95)
    HOVER_RANGE  = 30
    SPEED        = 22.0
    WING_TYPE    = "beetle"


class SumatranLonghorn(Insect):
    SPECIES      = "sumatran_longhorn"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 14, 6
    BODY_COLOR   = (35, 22, 18)
    WING_COLOR   = (72, 45, 32)
    ACCENT_COLOR = (188, 142, 88)
    HOVER_RANGE  = 32
    SPEED        = 22.0
    WING_TYPE    = "beetle"


class JapaneseLadyBeetle(Insect):
    SPECIES      = "japanese_lady_beetle"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 8, 5
    BODY_COLOR   = (35, 18, 18)
    WING_COLOR   = (215, 55, 38)
    ACCENT_COLOR = (28, 22, 18)
    HOVER_RANGE  = 28
    SPEED        = 26.0
    WING_TYPE    = "beetle"


class KoreanGroundBeetle(Insect):
    SPECIES      = "korean_ground_beetle"
    RARITY       = "common"
    BIOMES       = ["temperate", "boreal"]
    W, H         = 11, 5
    BODY_COLOR   = (28, 28, 32)
    WING_COLOR   = (48, 52, 62)
    ACCENT_COLOR = (105, 115, 138)
    HOVER_RANGE  = 28
    SPEED        = 26.0
    WING_TYPE    = "beetle"


class AsianFlowerChafer(Insect):
    SPECIES      = "asian_flower_chafer"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "jungle"]
    W, H         = 11, 6
    BODY_COLOR   = (78, 102, 22)
    WING_COLOR   = (128, 168, 42)
    ACCENT_COLOR = (215, 235, 118)
    HOVER_RANGE  = 32
    SPEED        = 26.0
    WING_TYPE    = "beetle"


class RainbowMountainStag(Insect):
    SPECIES      = "rainbow_mountain_stag"
    RARITY       = "rare"
    BIOMES       = ["alpine_mountain", "rocky_mountain"]
    W, H         = 13, 7
    BODY_COLOR   = (45, 22, 78)
    WING_COLOR   = (108, 62, 188)
    ACCENT_COLOR = (235, 158, 215)
    HOVER_RANGE  = 32
    SPEED        = 22.0
    WING_TYPE    = "beetle"


# --- Asian dragonflies ---

class AsianEmperorDragonfly(Insect):
    SPECIES      = "asian_emperor_dragonfly"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "jungle"]
    W, H         = 15, 5
    BODY_COLOR   = (22, 78, 128)
    WING_COLOR   = (138, 188, 235)
    ACCENT_COLOR = (235, 245, 255)
    HOVER_RANGE  = 65
    SPEED        = 38.0
    WING_TYPE    = "dragonfly"


class ChineseRedDragonfly(Insect):
    SPECIES      = "chinese_red_dragonfly"
    RARITY       = "common"
    BIOMES       = ["wetland", "temperate"]
    W, H         = 13, 4
    BODY_COLOR   = (185, 38, 28)
    WING_COLOR   = (235, 78, 55)
    ACCENT_COLOR = (250, 215, 195)
    HOVER_RANGE  = 55
    SPEED        = 34.0
    WING_TYPE    = "dragonfly"


class JapaneseGoldenRing(Insect):
    SPECIES      = "japanese_golden_ring"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "temperate"]
    W, H         = 15, 5
    BODY_COLOR   = (22, 22, 22)
    WING_COLOR   = (188, 188, 195)
    ACCENT_COLOR = (240, 195, 55)
    HOVER_RANGE  = 60
    SPEED        = 36.0
    WING_TYPE    = "dragonfly"


class YellowStripedHawker(Insect):
    SPECIES      = "yellow_striped_hawker"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "jungle"]
    W, H         = 14, 5
    BODY_COLOR   = (38, 38, 22)
    WING_COLOR   = (148, 148, 92)
    ACCENT_COLOR = (245, 218, 78)
    HOVER_RANGE  = 60
    SPEED        = 36.0
    WING_TYPE    = "dragonfly"


class RubyMeadowhawkAsia(Insect):
    SPECIES      = "ruby_meadowhawk_asia"
    RARITY       = "common"
    BIOMES       = ["wetland", "temperate"]
    W, H         = 12, 4
    BODY_COLOR   = (158, 35, 38)
    WING_COLOR   = (215, 78, 75)
    ACCENT_COLOR = (245, 200, 195)
    HOVER_RANGE  = 50
    SPEED        = 32.0
    WING_TYPE    = "dragonfly"


class PiedPaddyDragonfly(Insect):
    SPECIES      = "pied_paddy_dragonfly"
    RARITY       = "common"
    BIOMES       = ["wetland"]
    W, H         = 12, 5
    BODY_COLOR   = (22, 22, 22)
    WING_COLOR   = (215, 215, 215)
    ACCENT_COLOR = (78, 78, 88)
    HOVER_RANGE  = 50
    SPEED        = 32.0
    WING_TYPE    = "dragonfly"


class CrimsonDropwing(Insect):
    SPECIES      = "crimson_dropwing"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "jungle"]
    W, H         = 13, 5
    BODY_COLOR   = (148, 22, 22)
    WING_COLOR   = (215, 38, 32)
    ACCENT_COLOR = (248, 175, 142)
    HOVER_RANGE  = 55
    SPEED        = 36.0
    WING_TYPE    = "dragonfly"


class AsianClubtail(Insect):
    SPECIES      = "asian_clubtail"
    RARITY       = "uncommon"
    BIOMES       = ["wetland"]
    W, H         = 14, 5
    BODY_COLOR   = (28, 35, 22)
    WING_COLOR   = (108, 138, 92)
    ACCENT_COLOR = (215, 235, 158)
    HOVER_RANGE  = 55
    SPEED        = 32.0
    WING_TYPE    = "dragonfly"


class RiceFieldSkimmer(Insect):
    SPECIES      = "rice_field_skimmer"
    RARITY       = "common"
    BIOMES       = ["wetland"]
    W, H         = 12, 4
    BODY_COLOR   = (138, 105, 38)
    WING_COLOR   = (195, 168, 92)
    ACCENT_COLOR = (235, 218, 158)
    HOVER_RANGE  = 50
    SPEED        = 32.0
    WING_TYPE    = "dragonfly"


class KoreanGreenSkimmer(Insect):
    SPECIES      = "korean_green_skimmer"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "temperate"]
    W, H         = 13, 5
    BODY_COLOR   = (28, 88, 48)
    WING_COLOR   = (62, 158, 92)
    ACCENT_COLOR = (148, 235, 158)
    HOVER_RANGE  = 55
    SPEED        = 34.0
    WING_TYPE    = "dragonfly"


# --- Asian fireflies ---

class GenjiFirefly(Insect):
    SPECIES      = "genji_firefly"
    RARITY       = "rare"
    BIOMES       = ["wetland", "temperate"]
    W, H         = 9, 6
    BODY_COLOR   = (28, 28, 22)
    WING_COLOR   = (45, 45, 38)
    ACCENT_COLOR = (245, 250, 158)
    HOVER_RANGE  = 55
    SPEED        = 20.0
    WING_TYPE    = "firefly"
    NIGHT_ONLY   = True


class HeikeFirefly(Insect):
    SPECIES      = "heike_firefly"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "temperate"]
    W, H         = 8, 5
    BODY_COLOR   = (28, 28, 22)
    WING_COLOR   = (42, 42, 38)
    ACCENT_COLOR = (235, 245, 175)
    HOVER_RANGE  = 50
    SPEED        = 22.0
    WING_TYPE    = "firefly"
    NIGHT_ONLY   = True


class TaiwaneseFirefly(Insect):
    SPECIES      = "taiwanese_firefly"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 8, 5
    BODY_COLOR   = (32, 22, 22)
    WING_COLOR   = (52, 38, 38)
    ACCENT_COLOR = (255, 230, 138)
    HOVER_RANGE  = 50
    SPEED        = 22.0
    WING_TYPE    = "firefly"
    NIGHT_ONLY   = True


class KoreanFirefly(Insect):
    SPECIES      = "korean_firefly"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "wetland"]
    W, H         = 8, 5
    BODY_COLOR   = (30, 30, 22)
    WING_COLOR   = (48, 48, 38)
    ACCENT_COLOR = (215, 248, 145)
    HOVER_RANGE  = 48
    SPEED        = 22.0
    WING_TYPE    = "firefly"
    NIGHT_ONLY   = True


class HimalayanFirefly(Insect):
    SPECIES      = "himalayan_firefly"
    RARITY       = "rare"
    BIOMES       = ["alpine_mountain", "rocky_mountain"]
    W, H         = 9, 6
    BODY_COLOR   = (22, 22, 32)
    WING_COLOR   = (38, 38, 52)
    ACCENT_COLOR = (158, 215, 245)
    HOVER_RANGE  = 55
    SPEED        = 20.0
    WING_TYPE    = "firefly"
    NIGHT_ONLY   = True


# --- Asian moths ---

class JapaneseSilkmoth(Insect):
    SPECIES      = "japanese_silkmoth"
    RARITY       = "uncommon"
    BIOMES       = ["temperate"]
    W, H         = 14, 9
    BODY_COLOR   = (215, 205, 185)
    WING_COLOR   = (245, 238, 218)
    ACCENT_COLOR = (185, 158, 118)
    HOVER_RANGE  = 50
    SPEED        = 24.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class ChineseTussahMoth(Insect):
    SPECIES      = "chinese_tussah_moth"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "jungle"]
    W, H         = 14, 9
    BODY_COLOR   = (118, 78, 38)
    WING_COLOR   = (175, 132, 62)
    ACCENT_COLOR = (240, 205, 105)
    HOVER_RANGE  = 50
    SPEED        = 24.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class JapaneseOakSilkmoth(Insect):
    SPECIES      = "japanese_oak_silkmoth"
    RARITY       = "rare"
    BIOMES       = ["temperate", "boreal"]
    W, H         = 15, 10
    BODY_COLOR   = (88, 118, 62)
    WING_COLOR   = (148, 188, 108)
    ACCENT_COLOR = (215, 245, 178)
    HOVER_RANGE  = 55
    SPEED        = 24.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class MalayanMoonMoth(Insect):
    SPECIES      = "malayan_moon_moth"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 16, 11
    BODY_COLOR   = (78, 138, 88)
    WING_COLOR   = (128, 215, 158)
    ACCENT_COLOR = (218, 248, 215)
    HOVER_RANGE  = 60
    SPEED        = 24.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class MalaccanMoonmoth(Insect):
    SPECIES      = "malaccan_moonmoth"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 15, 10
    BODY_COLOR   = (78, 128, 95)
    WING_COLOR   = (138, 215, 168)
    ACCENT_COLOR = (235, 248, 215)
    HOVER_RANGE  = 60
    SPEED        = 24.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class HimalayanGiantMoth(Insect):
    SPECIES      = "himalayan_giant_moth"
    RARITY       = "rare"
    BIOMES       = ["alpine_mountain", "rocky_mountain"]
    W, H         = 16, 11
    BODY_COLOR   = (85, 65, 45)
    WING_COLOR   = (148, 118, 78)
    ACCENT_COLOR = (220, 195, 138)
    HOVER_RANGE  = 60
    SPEED        = 22.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class JadeHawkMoth(Insect):
    SPECIES      = "jade_hawk_moth"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 14, 8
    BODY_COLOR   = (28, 88, 62)
    WING_COLOR   = (52, 158, 108)
    ACCENT_COLOR = (118, 245, 188)
    HOVER_RANGE  = 55
    SPEED        = 38.0
    WING_TYPE    = "moth"


class AsianBeeHawkmoth(Insect):
    SPECIES      = "asian_bee_hawkmoth"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "temperate"]
    W, H         = 11, 7
    BODY_COLOR   = (62, 82, 38)
    WING_COLOR   = (215, 215, 215)
    ACCENT_COLOR = (245, 195, 55)
    HOVER_RANGE  = 45
    SPEED        = 38.0
    WING_TYPE    = "moth"


class BambooBorerMoth(Insect):
    SPECIES      = "bamboo_borer_moth"
    RARITY       = "common"
    BIOMES       = ["temperate", "jungle"]
    W, H         = 11, 7
    BODY_COLOR   = (118, 118, 88)
    WING_COLOR   = (175, 175, 138)
    ACCENT_COLOR = (220, 215, 178)
    HOVER_RANGE  = 40
    SPEED        = 22.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class TigerSwallowtailMoth(Insect):
    SPECIES      = "tiger_swallowtail_moth"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 14, 9
    BODY_COLOR   = (38, 22, 12)
    WING_COLOR   = (215, 152, 42)
    ACCENT_COLOR = (38, 18, 12)
    HOVER_RANGE  = 50
    SPEED        = 24.0
    WING_TYPE    = "moth"


class RubyTailedMoth(Insect):
    SPECIES      = "ruby_tailed_moth"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 13, 9
    BODY_COLOR   = (148, 28, 38)
    WING_COLOR   = (215, 55, 65)
    ACCENT_COLOR = (245, 215, 145)
    HOVER_RANGE  = 50
    SPEED        = 24.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class CrimsonTigerMoth(Insect):
    SPECIES      = "crimson_tiger_moth"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "temperate"]
    W, H         = 13, 8
    BODY_COLOR   = (32, 18, 18)
    WING_COLOR   = (175, 38, 38)
    ACCENT_COLOR = (245, 215, 178)
    HOVER_RANGE  = 48
    SPEED        = 26.0
    WING_TYPE    = "moth"


class EmperorSilkmoth(Insect):
    SPECIES      = "emperor_silkmoth"
    RARITY       = "rare"
    BIOMES       = ["temperate", "boreal"]
    W, H         = 16, 11
    BODY_COLOR   = (138, 78, 28)
    WING_COLOR   = (205, 138, 55)
    ACCENT_COLOR = (245, 220, 138)
    HOVER_RANGE  = 60
    SPEED        = 24.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class CherryBlossomMoth(Insect):
    SPECIES      = "cherry_blossom_moth"
    RARITY       = "uncommon"
    BIOMES       = ["temperate"]
    W, H         = 12, 8
    BODY_COLOR   = (138, 78, 88)
    WING_COLOR   = (235, 188, 200)
    ACCENT_COLOR = (250, 235, 240)
    HOVER_RANGE  = 50
    SPEED        = 24.0
    WING_TYPE    = "moth"


class MountainSilkmoth(Insect):
    SPECIES      = "mountain_silkmoth"
    RARITY       = "rare"
    BIOMES       = ["alpine_mountain", "rocky_mountain"]
    W, H         = 15, 10
    BODY_COLOR   = (155, 145, 175)
    WING_COLOR   = (205, 195, 220)
    ACCENT_COLOR = (235, 230, 245)
    HOVER_RANGE  = 55
    SPEED        = 22.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


# --- Asian other (mantises, wasps, cicadas, stick insects, etc.) ---

class JapaneseMantis(Insect):
    SPECIES      = "japanese_mantis"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 14, 7
    BODY_COLOR   = (88, 128, 52)
    WING_COLOR   = (128, 168, 78)
    ACCENT_COLOR = (185, 215, 118)
    HOVER_RANGE  = 35
    SPEED        = 24.0
    WING_TYPE    = "other"


class OrchidMantis(Insect):
    SPECIES      = "orchid_mantis"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 13, 7
    BODY_COLOR   = (235, 218, 230)
    WING_COLOR   = (250, 235, 245)
    ACCENT_COLOR = (220, 138, 178)
    HOVER_RANGE  = 35
    SPEED        = 22.0
    WING_TYPE    = "other"


class JadeMantis(Insect):
    SPECIES      = "jade_mantis"
    RARITY       = "uncommon"
    BIOMES       = ["jungle"]
    W, H         = 14, 7
    BODY_COLOR   = (38, 108, 78)
    WING_COLOR   = (62, 158, 118)
    ACCENT_COLOR = (138, 220, 178)
    HOVER_RANGE  = 35
    SPEED        = 24.0
    WING_TYPE    = "other"


class BorneanLeafMantis(Insect):
    SPECIES      = "bornean_leaf_mantis"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 14, 8
    BODY_COLOR   = (88, 78, 38)
    WING_COLOR   = (128, 118, 62)
    ACCENT_COLOR = (188, 175, 105)
    HOVER_RANGE  = 35
    SPEED        = 22.0
    WING_TYPE    = "other"


class BambooMantis(Insect):
    SPECIES      = "bamboo_mantis"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "temperate"]
    W, H         = 14, 7
    BODY_COLOR   = (115, 138, 62)
    WING_COLOR   = (158, 188, 95)
    ACCENT_COLOR = (215, 235, 138)
    HOVER_RANGE  = 35
    SPEED        = 24.0
    WING_TYPE    = "other"


class JapaneseHornet(Insect):
    SPECIES      = "japanese_hornet"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "boreal"]
    W, H         = 12, 6
    BODY_COLOR   = (50, 28, 12)
    WING_COLOR   = (185, 138, 38)
    ACCENT_COLOR = (245, 215, 78)
    HOVER_RANGE  = 50
    SPEED        = 38.0
    WING_TYPE    = "other"


class KoreanHornet(Insect):
    SPECIES      = "korean_hornet"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "boreal"]
    W, H         = 12, 6
    BODY_COLOR   = (62, 38, 18)
    WING_COLOR   = (175, 125, 48)
    ACCENT_COLOR = (235, 195, 88)
    HOVER_RANGE  = 50
    SPEED        = 38.0
    WING_TYPE    = "other"


class AsianPaperWasp(Insect):
    SPECIES      = "asian_paper_wasp"
    RARITY       = "common"
    BIOMES       = ["temperate", "jungle"]
    W, H         = 11, 5
    BODY_COLOR   = (78, 52, 22)
    WING_COLOR   = (175, 138, 65)
    ACCENT_COLOR = (235, 215, 138)
    HOVER_RANGE  = 45
    SPEED        = 36.0
    WING_TYPE    = "other"


class JapaneseHoneybee(Insect):
    SPECIES      = "japanese_honeybee"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 9, 5
    BODY_COLOR   = (88, 62, 28)
    WING_COLOR   = (215, 215, 220)
    ACCENT_COLOR = (235, 188, 78)
    HOVER_RANGE  = 45
    SPEED        = 32.0
    WING_TYPE    = "other"


class AsianBlueCarpenterBee(Insect):
    SPECIES      = "asian_blue_carpenter_bee"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 12, 6
    BODY_COLOR   = (22, 38, 88)
    WING_COLOR   = (62, 92, 158)
    ACCENT_COLOR = (148, 188, 245)
    HOVER_RANGE  = 50
    SPEED        = 34.0
    WING_TYPE    = "other"


class AsianCarpenterAnt(Insect):
    SPECIES      = "asian_carpenter_ant"
    RARITY       = "common"
    BIOMES       = ["temperate", "jungle"]
    W, H         = 8, 4
    BODY_COLOR   = (32, 22, 18)
    WING_COLOR   = (48, 38, 32)
    ACCENT_COLOR = (95, 72, 52)
    HOVER_RANGE  = 25
    SPEED        = 26.0
    WING_TYPE    = "other"


class WeaverAnt(Insect):
    SPECIES      = "weaver_ant"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 8, 4
    BODY_COLOR   = (138, 62, 22)
    WING_COLOR   = (188, 92, 38)
    ACCENT_COLOR = (235, 158, 88)
    HOVER_RANGE  = 28
    SPEED        = 28.0
    WING_TYPE    = "other"


class AsianFireAnt(Insect):
    SPECIES      = "asian_fire_ant"
    RARITY       = "common"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 7, 4
    BODY_COLOR   = (148, 38, 18)
    WING_COLOR   = (185, 65, 32)
    ACCENT_COLOR = (235, 118, 72)
    HOVER_RANGE  = 25
    SPEED        = 28.0
    WING_TYPE    = "other"


class JapaneseGiantCicada(Insect):
    SPECIES      = "japanese_giant_cicada"
    RARITY       = "uncommon"
    BIOMES       = ["temperate"]
    W, H         = 14, 7
    BODY_COLOR   = (35, 32, 28)
    WING_COLOR   = (188, 188, 195)
    ACCENT_COLOR = (105, 95, 78)
    HOVER_RANGE  = 35
    SPEED        = 28.0
    WING_TYPE    = "other"


class EveningCicada(Insect):
    SPECIES      = "evening_cicada"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "boreal"]
    W, H         = 12, 6
    BODY_COLOR   = (78, 62, 42)
    WING_COLOR   = (195, 178, 148)
    ACCENT_COLOR = (235, 215, 178)
    HOVER_RANGE  = 35
    SPEED        = 28.0
    WING_TYPE    = "other"
    DUSK_ONLY    = True


class AnnualCicada(Insect):
    SPECIES      = "annual_cicada"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 11, 6
    BODY_COLOR   = (68, 78, 52)
    WING_COLOR   = (158, 168, 138)
    ACCENT_COLOR = (215, 220, 195)
    HOVER_RANGE  = 35
    SPEED        = 28.0
    WING_TYPE    = "other"


class JungleCicadaAsia(Insect):
    SPECIES      = "jungle_cicada_asia"
    RARITY       = "common"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 12, 6
    BODY_COLOR   = (38, 52, 38)
    WING_COLOR   = (148, 165, 138)
    ACCENT_COLOR = (215, 235, 188)
    HOVER_RANGE  = 35
    SPEED        = 28.0
    WING_TYPE    = "other"


class CherryBlossomCicada(Insect):
    SPECIES      = "cherry_blossom_cicada"
    RARITY       = "uncommon"
    BIOMES       = ["temperate"]
    W, H         = 11, 6
    BODY_COLOR   = (118, 62, 78)
    WING_COLOR   = (220, 175, 188)
    ACCENT_COLOR = (245, 225, 230)
    HOVER_RANGE  = 35
    SPEED        = 28.0
    WING_TYPE    = "other"


class RiceGrasshopper(Insect):
    SPECIES      = "rice_grasshopper"
    RARITY       = "common"
    BIOMES       = ["wetland", "rolling_hills"]
    W, H         = 11, 6
    BODY_COLOR   = (108, 138, 62)
    WING_COLOR   = (158, 188, 92)
    ACCENT_COLOR = (215, 235, 138)
    HOVER_RANGE  = 32
    SPEED        = 32.0
    WING_TYPE    = "other"


class JapaneseKatydid(Insect):
    SPECIES      = "japanese_katydid"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 13, 7
    BODY_COLOR   = (78, 128, 52)
    WING_COLOR   = (128, 178, 88)
    ACCENT_COLOR = (188, 220, 128)
    HOVER_RANGE  = 35
    SPEED        = 24.0
    WING_TYPE    = "other"


class BellCricket(Insect):
    SPECIES      = "bell_cricket"
    RARITY       = "uncommon"
    BIOMES       = ["temperate"]
    W, H         = 10, 6
    BODY_COLOR   = (28, 28, 22)
    WING_COLOR   = (48, 45, 38)
    ACCENT_COLOR = (115, 105, 72)
    HOVER_RANGE  = 30
    SPEED        = 24.0
    WING_TYPE    = "other"
    NIGHT_ONLY   = True


class PineCricket(Insect):
    SPECIES      = "pine_cricket"
    RARITY       = "common"
    BIOMES       = ["temperate", "boreal"]
    W, H         = 10, 6
    BODY_COLOR   = (62, 48, 28)
    WING_COLOR   = (92, 72, 45)
    ACCENT_COLOR = (148, 118, 78)
    HOVER_RANGE  = 30
    SPEED        = 26.0
    WING_TYPE    = "other"
    NIGHT_ONLY   = True


class BambooStickInsect(Insect):
    SPECIES      = "bamboo_stick_insect"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "temperate"]
    W, H         = 16, 4
    BODY_COLOR   = (115, 138, 62)
    WING_COLOR   = (158, 188, 95)
    ACCENT_COLOR = (215, 235, 138)
    HOVER_RANGE  = 30
    SPEED        = 18.0
    WING_TYPE    = "other"


class MalayanLeafInsect(Insect):
    SPECIES      = "malayan_leaf_insect"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 12, 9
    BODY_COLOR   = (62, 108, 38)
    WING_COLOR   = (108, 168, 62)
    ACCENT_COLOR = (175, 215, 105)
    HOVER_RANGE  = 30
    SPEED        = 18.0
    WING_TYPE    = "other"


class BorneanStickInsect(Insect):
    SPECIES      = "bornean_stick_insect"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 16, 4
    BODY_COLOR   = (78, 52, 28)
    WING_COLOR   = (118, 88, 45)
    ACCENT_COLOR = (175, 138, 78)
    HOVER_RANGE  = 30
    SPEED        = 18.0
    WING_TYPE    = "other"


class HimalayanStickInsect(Insect):
    SPECIES      = "himalayan_stick_insect"
    RARITY       = "rare"
    BIOMES       = ["alpine_mountain", "rocky_mountain"]
    W, H         = 15, 4
    BODY_COLOR   = (88, 78, 62)
    WING_COLOR   = (128, 115, 92)
    ACCENT_COLOR = (188, 175, 148)
    HOVER_RANGE  = 30
    SPEED        = 18.0
    WING_TYPE    = "other"


class AsianAssassinBug(Insect):
    SPECIES      = "asian_assassin_bug"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 10, 6
    BODY_COLOR   = (118, 22, 28)
    WING_COLOR   = (175, 38, 42)
    ACCENT_COLOR = (28, 22, 22)
    HOVER_RANGE  = 35
    SPEED        = 30.0
    WING_TYPE    = "other"


class JapaneseShieldBug(Insect):
    SPECIES      = "japanese_shield_bug"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 9, 7
    BODY_COLOR   = (68, 95, 48)
    WING_COLOR   = (108, 148, 78)
    ACCENT_COLOR = (175, 205, 118)
    HOVER_RANGE  = 30
    SPEED        = 22.0
    WING_TYPE    = "other"


class JapaneseBumblebee(Insect):
    SPECIES      = "japanese_bumblebee"
    RARITY       = "common"
    BIOMES       = ["temperate", "alpine_mountain"]
    W, H         = 10, 6
    BODY_COLOR   = (40, 32, 18)
    WING_COLOR   = (185, 178, 165)
    ACCENT_COLOR = (245, 195, 78)
    HOVER_RANGE  = 45
    SPEED        = 32.0
    WING_TYPE    = "other"


class AsianHoneyWasp(Insect):
    SPECIES      = "asian_honey_wasp"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 10, 5
    BODY_COLOR   = (118, 78, 18)
    WING_COLOR   = (188, 138, 38)
    ACCENT_COLOR = (245, 215, 105)
    HOVER_RANGE  = 45
    SPEED        = 36.0
    WING_TYPE    = "other"


# --- Asian fauna (batch 2, 25 species) ---

class GoldenBirdwing(Insect):
    SPECIES      = "golden_birdwing"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 16, 11
    BODY_COLOR   = (28, 28, 22)
    WING_COLOR   = (50, 50, 40)
    ACCENT_COLOR = (245, 200, 55)
    HOVER_RANGE  = 65
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class TreeNymph(Insect):
    SPECIES      = "tree_nymph"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 15, 10
    BODY_COLOR   = (32, 32, 32)
    WING_COLOR   = (242, 240, 230)
    ACCENT_COLOR = (28, 28, 28)
    HOVER_RANGE  = 60
    SPEED        = 22.0
    WING_TYPE    = "butterfly"


class CommonBluebottle(Insect):
    SPECIES      = "common_bluebottle"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 12, 9
    BODY_COLOR   = (22, 22, 32)
    WING_COLOR   = (32, 32, 48)
    ACCENT_COLOR = (88, 178, 235)
    HOVER_RANGE  = 55
    SPEED        = 34.0
    WING_TYPE    = "butterfly"


class PaintedJezebel(Insect):
    SPECIES      = "painted_jezebel"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 13, 9
    BODY_COLOR   = (32, 32, 32)
    WING_COLOR   = (240, 235, 215)
    ACCENT_COLOR = (235, 88, 55)
    HOVER_RANGE  = 55
    SPEED        = 28.0
    WING_TYPE    = "butterfly"


class CommonLeopardButterfly(Insect):
    SPECIES      = "common_leopard_butterfly"
    RARITY       = "common"
    BIOMES       = ["jungle", "temperate"]
    W, H         = 12, 9
    BODY_COLOR   = (62, 38, 12)
    WING_COLOR   = (215, 148, 38)
    ACCENT_COLOR = (32, 22, 12)
    HOVER_RANGE  = 50
    SPEED        = 28.0
    WING_TYPE    = "butterfly"


class RustyTippedPage(Insect):
    SPECIES      = "rusty_tipped_page"
    RARITY       = "uncommon"
    BIOMES       = ["jungle"]
    W, H         = 13, 9
    BODY_COLOR   = (42, 22, 18)
    WING_COLOR   = (158, 65, 32)
    ACCENT_COLOR = (235, 215, 178)
    HOVER_RANGE  = 55
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class ChineseGoldenChafer(Insect):
    SPECIES      = "chinese_golden_chafer"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 11, 6
    BODY_COLOR   = (118, 92, 22)
    WING_COLOR   = (205, 168, 42)
    ACCENT_COLOR = (250, 230, 105)
    HOVER_RANGE  = 32
    SPEED        = 24.0
    WING_TYPE    = "beetle"


class JapaneseTigerLonghorn(Insect):
    SPECIES      = "japanese_tiger_longhorn"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "boreal"]
    W, H         = 13, 6
    BODY_COLOR   = (28, 22, 22)
    WING_COLOR   = (45, 38, 38)
    ACCENT_COLOR = (245, 200, 78)
    HOVER_RANGE  = 32
    SPEED        = 26.0
    WING_TYPE    = "beetle"


class MalayanFireBeetle(Insect):
    SPECIES      = "malayan_fire_beetle"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 11, 6
    BODY_COLOR   = (148, 32, 18)
    WING_COLOR   = (215, 62, 28)
    ACCENT_COLOR = (250, 188, 95)
    HOVER_RANGE  = 32
    SPEED        = 26.0
    WING_TYPE    = "beetle"


class AsianFlatHeadedBorer(Insect):
    SPECIES      = "asian_flat_headed_borer"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "temperate"]
    W, H         = 11, 6
    BODY_COLOR   = (38, 78, 62)
    WING_COLOR   = (62, 138, 108)
    ACCENT_COLOR = (148, 220, 178)
    HOVER_RANGE  = 30
    SPEED        = 24.0
    WING_TYPE    = "beetle"


class JapaneseSkimmer(Insect):
    SPECIES      = "japanese_skimmer"
    RARITY       = "common"
    BIOMES       = ["wetland", "temperate"]
    W, H         = 13, 5
    BODY_COLOR   = (148, 105, 32)
    WING_COLOR   = (215, 178, 78)
    ACCENT_COLOR = (245, 225, 158)
    HOVER_RANGE  = 55
    SPEED        = 34.0
    WING_TYPE    = "dragonfly"


class ChineseDarner(Insect):
    SPECIES      = "chinese_darner"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "jungle"]
    W, H         = 15, 5
    BODY_COLOR   = (28, 62, 38)
    WING_COLOR   = (108, 158, 92)
    ACCENT_COLOR = (195, 235, 158)
    HOVER_RANGE  = 60
    SPEED        = 36.0
    WING_TYPE    = "dragonfly"


class AsianBlueDamsel(Insect):
    SPECIES      = "asian_blue_damsel"
    RARITY       = "common"
    BIOMES       = ["wetland", "jungle"]
    W, H         = 11, 3
    BODY_COLOR   = (42, 78, 158)
    WING_COLOR   = (148, 188, 240)
    ACCENT_COLOR = (220, 235, 250)
    HOVER_RANGE  = 45
    SPEED        = 30.0
    WING_TYPE    = "dragonfly"


class SilverlinedHawkmoth(Insect):
    SPECIES      = "silverlined_hawkmoth"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "temperate"]
    W, H         = 14, 8
    BODY_COLOR   = (62, 52, 42)
    WING_COLOR   = (118, 105, 88)
    ACCENT_COLOR = (220, 220, 225)
    HOVER_RANGE  = 55
    SPEED        = 38.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class PinkUnderwingMoth(Insect):
    SPECIES      = "pink_underwing_moth"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 13, 9
    BODY_COLOR   = (72, 48, 42)
    WING_COLOR   = (115, 78, 68)
    ACCENT_COLOR = (235, 138, 168)
    HOVER_RANGE  = 50
    SPEED        = 26.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class RoyalSilkmoth(Insect):
    SPECIES      = "royal_silkmoth"
    RARITY       = "rare"
    BIOMES       = ["temperate"]
    W, H         = 15, 10
    BODY_COLOR   = (118, 38, 88)
    WING_COLOR   = (175, 78, 138)
    ACCENT_COLOR = (245, 215, 235)
    HOVER_RANGE  = 55
    SPEED        = 24.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class SnowMoth(Insect):
    SPECIES      = "snow_moth"
    RARITY       = "uncommon"
    BIOMES       = ["alpine_mountain", "tundra"]
    W, H         = 12, 8
    BODY_COLOR   = (215, 220, 230)
    WING_COLOR   = (240, 243, 248)
    ACCENT_COLOR = (175, 195, 220)
    HOVER_RANGE  = 45
    SPEED        = 22.0
    WING_TYPE    = "moth"


class GiantAsianHoneybee(Insect):
    SPECIES      = "giant_asian_honeybee"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 11, 6
    BODY_COLOR   = (78, 52, 22)
    WING_COLOR   = (205, 195, 178)
    ACCENT_COLOR = (240, 200, 88)
    HOVER_RANGE  = 50
    SPEED        = 36.0
    WING_TYPE    = "other"


class AsianTreeMantis(Insect):
    SPECIES      = "asian_tree_mantis"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "temperate"]
    W, H         = 14, 7
    BODY_COLOR   = (62, 42, 22)
    WING_COLOR   = (108, 78, 45)
    ACCENT_COLOR = (175, 138, 92)
    HOVER_RANGE  = 35
    SPEED        = 22.0
    WING_TYPE    = "other"


class DeadLeafMantis(Insect):
    SPECIES      = "dead_leaf_mantis"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 13, 8
    BODY_COLOR   = (88, 55, 28)
    WING_COLOR   = (138, 92, 48)
    ACCENT_COLOR = (195, 148, 88)
    HOVER_RANGE  = 32
    SPEED        = 20.0
    WING_TYPE    = "other"


class ChineseRiceLocust(Insect):
    SPECIES      = "chinese_rice_locust"
    RARITY       = "common"
    BIOMES       = ["wetland", "rolling_hills"]
    W, H         = 12, 6
    BODY_COLOR   = (118, 138, 52)
    WING_COLOR   = (165, 188, 88)
    ACCENT_COLOR = (215, 235, 138)
    HOVER_RANGE  = 32
    SPEED        = 32.0
    WING_TYPE    = "other"


class PaddyKatydid(Insect):
    SPECIES      = "paddy_katydid"
    RARITY       = "common"
    BIOMES       = ["wetland", "jungle"]
    W, H         = 12, 7
    BODY_COLOR   = (88, 138, 62)
    WING_COLOR   = (138, 188, 92)
    ACCENT_COLOR = (195, 230, 138)
    HOVER_RANGE  = 33
    SPEED        = 24.0
    WING_TYPE    = "other"


class AsianTreeCricket(Insect):
    SPECIES      = "asian_tree_cricket"
    RARITY       = "common"
    BIOMES       = ["jungle", "temperate"]
    W, H         = 10, 6
    BODY_COLOR   = (118, 138, 78)
    WING_COLOR   = (158, 188, 108)
    ACCENT_COLOR = (215, 235, 158)
    HOVER_RANGE  = 28
    SPEED        = 24.0
    WING_TYPE    = "other"
    NIGHT_ONLY   = True


class AsianLeafhopper(Insect):
    SPECIES      = "asian_leafhopper"
    RARITY       = "common"
    BIOMES       = ["jungle", "temperate"]
    W, H         = 7, 4
    BODY_COLOR   = (62, 138, 88)
    WING_COLOR   = (108, 188, 128)
    ACCENT_COLOR = (175, 235, 178)
    HOVER_RANGE  = 28
    SPEED        = 30.0
    WING_TYPE    = "other"


class JadeWeevil(Insect):
    SPECIES      = "jade_weevil"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 9, 6
    BODY_COLOR   = (32, 92, 78)
    WING_COLOR   = (62, 158, 128)
    ACCENT_COLOR = (138, 235, 195)
    HOVER_RANGE  = 28
    SPEED        = 22.0
    WING_TYPE    = "beetle"


# ---------------------------------------------------------------------------
# North American fauna (100 species)
# ---------------------------------------------------------------------------

# --- NA butterflies ---

class MourningCloak(Insect):
    SPECIES      = "mourning_cloak"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "boreal", "birch_forest"]
    W, H         = 13, 10
    BODY_COLOR   = (28, 22, 22)
    WING_COLOR   = (62, 28, 22)
    ACCENT_COLOR = (235, 215, 145)
    HOVER_RANGE  = 55
    SPEED        = 28.0
    WING_TYPE    = "butterfly"


class Viceroy(Insect):
    SPECIES      = "viceroy"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "wetland"]
    W, H         = 12, 9
    BODY_COLOR   = (38, 22, 12)
    WING_COLOR   = (215, 118, 32)
    ACCENT_COLOR = (32, 22, 12)
    HOVER_RANGE  = 50
    SPEED        = 28.0
    WING_TYPE    = "butterfly"


class SpicebushSwallowtail(Insect):
    SPECIES      = "spicebush_swallowtail"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "birch_forest"]
    W, H         = 14, 10
    BODY_COLOR   = (22, 22, 28)
    WING_COLOR   = (38, 38, 52)
    ACCENT_COLOR = (108, 178, 188)
    HOVER_RANGE  = 60
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class PipevineSwallowtail(Insect):
    SPECIES      = "pipevine_swallowtail"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 14, 10
    BODY_COLOR   = (18, 22, 32)
    WING_COLOR   = (32, 42, 62)
    ACCENT_COLOR = (88, 188, 178)
    HOVER_RANGE  = 60
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class AmericanLady(Insect):
    SPECIES      = "american_lady"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 11, 8
    BODY_COLOR   = (62, 32, 18)
    WING_COLOR   = (215, 118, 38)
    ACCENT_COLOR = (32, 22, 18)
    HOVER_RANGE  = 50
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class WoodlandSkipper(Insect):
    SPECIES      = "woodland_skipper"
    RARITY       = "common"
    BIOMES       = ["temperate", "birch_forest"]
    W, H         = 9, 7
    BODY_COLOR   = (62, 38, 18)
    WING_COLOR   = (188, 128, 45)
    ACCENT_COLOR = (32, 22, 12)
    HOVER_RANGE  = 40
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class ZebraSwallowtail(Insect):
    SPECIES      = "zebra_swallowtail"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "wetland"]
    W, H         = 14, 10
    BODY_COLOR   = (22, 22, 22)
    WING_COLOR   = (240, 240, 240)
    ACCENT_COLOR = (28, 28, 28)
    HOVER_RANGE  = 60
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class GiantSwallowtail(Insect):
    SPECIES      = "giant_swallowtail"
    RARITY       = "rare"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 16, 11
    BODY_COLOR   = (28, 22, 18)
    WING_COLOR   = (45, 35, 28)
    ACCENT_COLOR = (245, 215, 92)
    HOVER_RANGE  = 65
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class PineWhite(Insect):
    SPECIES      = "pine_white"
    RARITY       = "common"
    BIOMES       = ["boreal", "redwood"]
    W, H         = 11, 8
    BODY_COLOR   = (28, 28, 28)
    WING_COLOR   = (245, 240, 230)
    ACCENT_COLOR = (38, 38, 38)
    HOVER_RANGE  = 45
    SPEED        = 28.0
    WING_TYPE    = "butterfly"


class CloudedSulphur(Insect):
    SPECIES      = "clouded_sulphur"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 10, 8
    BODY_COLOR   = (108, 92, 32)
    WING_COLOR   = (245, 220, 88)
    ACCENT_COLOR = (188, 138, 38)
    HOVER_RANGE  = 45
    SPEED        = 28.0
    WING_TYPE    = "butterfly"


class OrangeSulphur(Insect):
    SPECIES      = "orange_sulphur"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 10, 8
    BODY_COLOR   = (108, 62, 18)
    WING_COLOR   = (245, 175, 55)
    ACCENT_COLOR = (188, 88, 22)
    HOVER_RANGE  = 45
    SPEED        = 28.0
    WING_TYPE    = "butterfly"


class PearlCrescent(Insect):
    SPECIES      = "pearl_crescent"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 9, 7
    BODY_COLOR   = (62, 32, 12)
    WING_COLOR   = (220, 138, 38)
    ACCENT_COLOR = (32, 22, 12)
    HOVER_RANGE  = 40
    SPEED        = 28.0
    WING_TYPE    = "butterfly"


class AmericanCopper(Insect):
    SPECIES      = "american_copper"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 9, 7
    BODY_COLOR   = (62, 32, 18)
    WING_COLOR   = (215, 105, 32)
    ACCENT_COLOR = (28, 22, 18)
    HOVER_RANGE  = 40
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class EasternTailedBlue(Insect):
    SPECIES      = "eastern_tailed_blue"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 8, 6
    BODY_COLOR   = (62, 82, 138)
    WING_COLOR   = (118, 158, 215)
    ACCENT_COLOR = (215, 230, 245)
    HOVER_RANGE  = 38
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class SpringAzure(Insect):
    SPECIES      = "spring_azure"
    RARITY       = "common"
    BIOMES       = ["temperate", "birch_forest"]
    W, H         = 9, 7
    BODY_COLOR   = (62, 88, 158)
    WING_COLOR   = (138, 188, 245)
    ACCENT_COLOR = (225, 238, 250)
    HOVER_RANGE  = 40
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class RegalFritillary(Insect):
    SPECIES      = "regal_fritillary"
    RARITY       = "rare"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 13, 10
    BODY_COLOR   = (62, 28, 18)
    WING_COLOR   = (175, 75, 28)
    ACCENT_COLOR = (32, 28, 32)
    HOVER_RANGE  = 55
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class GulfFritillary(Insect):
    SPECIES      = "gulf_fritillary"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "savanna", "beach"]
    W, H         = 13, 10
    BODY_COLOR   = (62, 28, 18)
    WING_COLOR   = (215, 88, 32)
    ACCENT_COLOR = (245, 215, 178)
    HOVER_RANGE  = 55
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class QuestionMarkButterfly(Insect):
    SPECIES      = "question_mark_butterfly"
    RARITY       = "common"
    BIOMES       = ["temperate", "birch_forest"]
    W, H         = 11, 9
    BODY_COLOR   = (62, 32, 18)
    WING_COLOR   = (175, 92, 32)
    ACCENT_COLOR = (215, 215, 215)
    HOVER_RANGE  = 50
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class EasternComma(Insect):
    SPECIES      = "eastern_comma"
    RARITY       = "common"
    BIOMES       = ["temperate", "birch_forest"]
    W, H         = 11, 9
    BODY_COLOR   = (62, 32, 18)
    WING_COLOR   = (188, 105, 38)
    ACCENT_COLOR = (215, 215, 215)
    HOVER_RANGE  = 48
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class CommonBuckeye(Insect):
    SPECIES      = "common_buckeye"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 12, 9
    BODY_COLOR   = (62, 42, 18)
    WING_COLOR   = (138, 92, 42)
    ACCENT_COLOR = (62, 92, 168)
    HOVER_RANGE  = 50
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class RedSpottedPurple(Insect):
    SPECIES      = "red_spotted_purple"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "birch_forest"]
    W, H         = 13, 10
    BODY_COLOR   = (18, 18, 32)
    WING_COLOR   = (32, 28, 78)
    ACCENT_COLOR = (188, 38, 78)
    HOVER_RANGE  = 55
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class AmericanSnout(Insect):
    SPECIES      = "american_snout"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 10, 8
    BODY_COLOR   = (62, 42, 22)
    WING_COLOR   = (148, 88, 38)
    ACCENT_COLOR = (215, 178, 118)
    HOVER_RANGE  = 45
    SPEED        = 28.0
    WING_TYPE    = "butterfly"


class HackberryEmperor(Insect):
    SPECIES      = "hackberry_emperor"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 12, 9
    BODY_COLOR   = (62, 42, 22)
    WING_COLOR   = (138, 95, 48)
    ACCENT_COLOR = (215, 178, 118)
    HOVER_RANGE  = 50
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class TawnyEmperor(Insect):
    SPECIES      = "tawny_emperor"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 12, 9
    BODY_COLOR   = (72, 38, 18)
    WING_COLOR   = (175, 105, 38)
    ACCENT_COLOR = (220, 175, 92)
    HOVER_RANGE  = 50
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class FloridaLeafwing(Insect):
    SPECIES      = "florida_leafwing"
    RARITY       = "rare"
    BIOMES       = ["temperate", "tropical"]
    W, H         = 13, 10
    BODY_COLOR   = (62, 22, 18)
    WING_COLOR   = (195, 62, 32)
    ACCENT_COLOR = (115, 38, 22)
    HOVER_RANGE  = 55
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


# --- NA beetles ---

class EasternEyedClickBeetle(Insect):
    SPECIES      = "eastern_eyed_click_beetle"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "birch_forest"]
    W, H         = 12, 6
    BODY_COLOR   = (22, 22, 22)
    WING_COLOR   = (45, 45, 45)
    ACCENT_COLOR = (235, 235, 235)
    HOVER_RANGE  = 32
    SPEED        = 26.0
    WING_TYPE    = "beetle"


class ColoradoPotatoBeetle(Insect):
    SPECIES      = "colorado_potato_beetle"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 9, 6
    BODY_COLOR   = (62, 42, 18)
    WING_COLOR   = (235, 215, 78)
    ACCENT_COLOR = (32, 22, 12)
    HOVER_RANGE  = 28
    SPEED        = 24.0
    WING_TYPE    = "beetle"


class SixSpottedTigerBeetle(Insect):
    SPECIES      = "six_spotted_tiger_beetle"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "birch_forest"]
    W, H         = 11, 6
    BODY_COLOR   = (28, 105, 78)
    WING_COLOR   = (52, 175, 128)
    ACCENT_COLOR = (235, 240, 235)
    HOVER_RANGE  = 32
    SPEED        = 34.0
    WING_TYPE    = "beetle"


class AmericanBuryingBeetle(Insect):
    SPECIES      = "american_burying_beetle"
    RARITY       = "rare"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 12, 6
    BODY_COLOR   = (22, 22, 22)
    WING_COLOR   = (38, 38, 38)
    ACCENT_COLOR = (235, 105, 32)
    HOVER_RANGE  = 30
    SPEED        = 24.0
    WING_TYPE    = "beetle"


class GoldsmithBeetle(Insect):
    SPECIES      = "goldsmith_beetle"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 11, 6
    BODY_COLOR   = (118, 92, 22)
    WING_COLOR   = (215, 180, 62)
    ACCENT_COLOR = (250, 235, 138)
    HOVER_RANGE  = 32
    SPEED        = 24.0
    WING_TYPE    = "beetle"


class JuneBeetle(Insect):
    SPECIES      = "june_beetle"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 10, 6
    BODY_COLOR   = (62, 38, 12)
    WING_COLOR   = (118, 78, 32)
    ACCENT_COLOR = (175, 138, 78)
    HOVER_RANGE  = 35
    SPEED        = 30.0
    WING_TYPE    = "beetle"
    NIGHT_ONLY   = True


class NorthernCornRootworm(Insect):
    SPECIES      = "northern_corn_rootworm"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 7, 4
    BODY_COLOR   = (78, 108, 32)
    WING_COLOR   = (138, 175, 62)
    ACCENT_COLOR = (215, 235, 118)
    HOVER_RANGE  = 25
    SPEED        = 22.0
    WING_TYPE    = "beetle"


class AmericanCarrionBeetle(Insect):
    SPECIES      = "american_carrion_beetle"
    RARITY       = "common"
    BIOMES       = ["temperate", "birch_forest"]
    W, H         = 11, 6
    BODY_COLOR   = (22, 22, 22)
    WING_COLOR   = (38, 38, 38)
    ACCENT_COLOR = (215, 195, 88)
    HOVER_RANGE  = 30
    SPEED        = 24.0
    WING_TYPE    = "beetle"


class PennsylvaniaLeatherwing(Insect):
    SPECIES      = "pennsylvania_leatherwing"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 10, 5
    BODY_COLOR   = (108, 78, 22)
    WING_COLOR   = (215, 178, 62)
    ACCENT_COLOR = (32, 22, 22)
    HOVER_RANGE  = 35
    SPEED        = 32.0
    WING_TYPE    = "beetle"


class BronzedCarabid(Insect):
    SPECIES      = "bronzed_carabid"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "boreal"]
    W, H         = 11, 5
    BODY_COLOR   = (78, 52, 22)
    WING_COLOR   = (148, 105, 42)
    ACCENT_COLOR = (215, 175, 95)
    HOVER_RANGE  = 30
    SPEED        = 28.0
    WING_TYPE    = "beetle"


class GiantStagBeetle(Insect):
    SPECIES      = "giant_stag_beetle"
    RARITY       = "rare"
    BIOMES       = ["temperate", "birch_forest"]
    W, H         = 14, 7
    BODY_COLOR   = (38, 22, 18)
    WING_COLOR   = (72, 42, 28)
    ACCENT_COLOR = (138, 92, 55)
    HOVER_RANGE  = 32
    SPEED        = 22.0
    WING_TYPE    = "beetle"


class RedMilkweedBeetle(Insect):
    SPECIES      = "red_milkweed_beetle"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 10, 5
    BODY_COLOR   = (148, 32, 22)
    WING_COLOR   = (215, 55, 38)
    ACCENT_COLOR = (32, 22, 22)
    HOVER_RANGE  = 30
    SPEED        = 24.0
    WING_TYPE    = "beetle"


class SpottedPineSawyer(Insect):
    SPECIES      = "spotted_pine_sawyer"
    RARITY       = "uncommon"
    BIOMES       = ["boreal", "redwood"]
    W, H         = 13, 6
    BODY_COLOR   = (38, 28, 22)
    WING_COLOR   = (72, 55, 42)
    ACCENT_COLOR = (215, 215, 215)
    HOVER_RANGE  = 32
    SPEED        = 26.0
    WING_TYPE    = "beetle"


class BumbleFlowerBeetle(Insect):
    SPECIES      = "bumble_flower_beetle"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 10, 6
    BODY_COLOR   = (62, 42, 18)
    WING_COLOR   = (188, 138, 55)
    ACCENT_COLOR = (32, 22, 22)
    HOVER_RANGE  = 32
    SPEED        = 26.0
    WING_TYPE    = "beetle"


class AmericanOakBorer(Insect):
    SPECIES      = "american_oak_borer"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "birch_forest"]
    W, H         = 13, 6
    BODY_COLOR   = (45, 32, 18)
    WING_COLOR   = (88, 65, 38)
    ACCENT_COLOR = (175, 138, 78)
    HOVER_RANGE  = 32
    SPEED        = 24.0
    WING_TYPE    = "beetle"


# --- NA dragonflies ---

class CommonGreenDarner(Insect):
    SPECIES      = "common_green_darner"
    RARITY       = "common"
    BIOMES       = ["wetland", "temperate"]
    W, H         = 15, 5
    BODY_COLOR   = (32, 108, 62)
    WING_COLOR   = (62, 158, 105)
    ACCENT_COLOR = (215, 235, 158)
    HOVER_RANGE  = 65
    SPEED        = 38.0
    WING_TYPE    = "dragonfly"


class TwelveSpottedSkimmer(Insect):
    SPECIES      = "twelve_spotted_skimmer"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "temperate"]
    W, H         = 13, 5
    BODY_COLOR   = (62, 62, 62)
    WING_COLOR   = (215, 215, 215)
    ACCENT_COLOR = (28, 28, 28)
    HOVER_RANGE  = 55
    SPEED        = 36.0
    WING_TYPE    = "dragonfly"


class WidowSkimmer(Insect):
    SPECIES      = "widow_skimmer"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "temperate"]
    W, H         = 13, 5
    BODY_COLOR   = (32, 32, 38)
    WING_COLOR   = (62, 62, 78)
    ACCENT_COLOR = (215, 215, 235)
    HOVER_RANGE  = 55
    SPEED        = 36.0
    WING_TYPE    = "dragonfly"


class EasternPondhawk(Insect):
    SPECIES      = "eastern_pondhawk"
    RARITY       = "common"
    BIOMES       = ["wetland"]
    W, H         = 12, 5
    BODY_COLOR   = (62, 138, 78)
    WING_COLOR   = (108, 188, 118)
    ACCENT_COLOR = (215, 240, 175)
    HOVER_RANGE  = 50
    SPEED        = 34.0
    WING_TYPE    = "dragonfly"


class BlueDasher(Insect):
    SPECIES      = "blue_dasher"
    RARITY       = "common"
    BIOMES       = ["wetland", "temperate"]
    W, H         = 12, 4
    BODY_COLOR   = (62, 108, 188)
    WING_COLOR   = (148, 188, 245)
    ACCENT_COLOR = (215, 235, 250)
    HOVER_RANGE  = 50
    SPEED        = 34.0
    WING_TYPE    = "dragonfly"


class AutumnMeadowhawk(Insect):
    SPECIES      = "autumn_meadowhawk"
    RARITY       = "common"
    BIOMES       = ["wetland", "temperate"]
    W, H         = 11, 4
    BODY_COLOR   = (188, 62, 38)
    WING_COLOR   = (235, 105, 78)
    ACCENT_COLOR = (250, 195, 158)
    HOVER_RANGE  = 48
    SPEED        = 32.0
    WING_TYPE    = "dragonfly"


class EasternAmberwing(Insect):
    SPECIES      = "eastern_amberwing"
    RARITY       = "uncommon"
    BIOMES       = ["wetland"]
    W, H         = 10, 4
    BODY_COLOR   = (148, 92, 22)
    WING_COLOR   = (235, 178, 65)
    ACCENT_COLOR = (250, 225, 158)
    HOVER_RANGE  = 45
    SPEED        = 32.0
    WING_TYPE    = "dragonfly"


class RoseateSkimmer(Insect):
    SPECIES      = "roseate_skimmer"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "temperate"]
    W, H         = 13, 5
    BODY_COLOR   = (188, 88, 138)
    WING_COLOR   = (235, 158, 195)
    ACCENT_COLOR = (250, 215, 230)
    HOVER_RANGE  = 55
    SPEED        = 34.0
    WING_TYPE    = "dragonfly"


class EbonyJewelwing(Insect):
    SPECIES      = "ebony_jewelwing"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "birch_forest"]
    W, H         = 13, 5
    BODY_COLOR   = (28, 88, 78)
    WING_COLOR   = (22, 22, 28)
    ACCENT_COLOR = (62, 178, 148)
    HOVER_RANGE  = 50
    SPEED        = 30.0
    WING_TYPE    = "dragonfly"


class AmericanRubyspot(Insect):
    SPECIES      = "american_rubyspot"
    RARITY       = "uncommon"
    BIOMES       = ["wetland"]
    W, H         = 12, 4
    BODY_COLOR   = (38, 32, 32)
    WING_COLOR   = (62, 62, 62)
    ACCENT_COLOR = (215, 38, 55)
    HOVER_RANGE  = 50
    SPEED        = 32.0
    WING_TYPE    = "dragonfly"


# --- NA fireflies ---

class BigDipperFirefly(Insect):
    SPECIES      = "big_dipper_firefly"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 9, 6
    BODY_COLOR   = (32, 22, 22)
    WING_COLOR   = (52, 38, 32)
    ACCENT_COLOR = (245, 230, 138)
    HOVER_RANGE  = 50
    SPEED        = 22.0
    WING_TYPE    = "firefly"
    NIGHT_ONLY   = True


class SynchronousFirefly(Insect):
    SPECIES      = "synchronous_firefly"
    RARITY       = "rare"
    BIOMES       = ["temperate", "birch_forest"]
    W, H         = 9, 6
    BODY_COLOR   = (28, 22, 22)
    WING_COLOR   = (48, 38, 32)
    ACCENT_COLOR = (250, 240, 158)
    HOVER_RANGE  = 55
    SPEED        = 22.0
    WING_TYPE    = "firefly"
    NIGHT_ONLY   = True


class PennsylvaniaFirefly(Insect):
    SPECIES      = "pennsylvania_firefly"
    RARITY       = "common"
    BIOMES       = ["temperate", "wetland"]
    W, H         = 8, 5
    BODY_COLOR   = (30, 22, 22)
    WING_COLOR   = (52, 38, 32)
    ACCENT_COLOR = (240, 225, 138)
    HOVER_RANGE  = 48
    SPEED        = 22.0
    WING_TYPE    = "firefly"
    NIGHT_ONLY   = True


class WinterFirefly(Insect):
    SPECIES      = "winter_firefly"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "boreal"]
    W, H         = 8, 5
    BODY_COLOR   = (30, 30, 32)
    WING_COLOR   = (52, 52, 58)
    ACCENT_COLOR = (188, 220, 225)
    HOVER_RANGE  = 40
    SPEED        = 20.0
    WING_TYPE    = "firefly"
    DAWN_ONLY    = True


class AppalachianBlueGhost(Insect):
    SPECIES      = "appalachian_blue_ghost"
    RARITY       = "rare"
    BIOMES       = ["temperate", "birch_forest"]
    W, H         = 8, 5
    BODY_COLOR   = (25, 25, 32)
    WING_COLOR   = (42, 42, 55)
    ACCENT_COLOR = (158, 210, 245)
    HOVER_RANGE  = 50
    SPEED        = 18.0
    WING_TYPE    = "firefly"
    NIGHT_ONLY   = True


# --- NA moths ---

class CecropiaSilkmoth(Insect):
    SPECIES      = "cecropia_silkmoth"
    RARITY       = "rare"
    BIOMES       = ["temperate", "birch_forest"]
    W, H         = 16, 11
    BODY_COLOR   = (108, 38, 38)
    WING_COLOR   = (158, 78, 62)
    ACCENT_COLOR = (235, 215, 178)
    HOVER_RANGE  = 60
    SPEED        = 24.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class PrometheaMoth(Insect):
    SPECIES      = "promethea_moth"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "birch_forest"]
    W, H         = 14, 9
    BODY_COLOR   = (62, 32, 32)
    WING_COLOR   = (105, 55, 48)
    ACCENT_COLOR = (215, 175, 138)
    HOVER_RANGE  = 50
    SPEED        = 24.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class RegalMoth(Insect):
    SPECIES      = "regal_moth"
    RARITY       = "rare"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 16, 11
    BODY_COLOR   = (62, 32, 18)
    WING_COLOR   = (158, 92, 38)
    ACCENT_COLOR = (235, 215, 88)
    HOVER_RANGE  = 60
    SPEED        = 24.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class ImperialMoth(Insect):
    SPECIES      = "imperial_moth"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "birch_forest"]
    W, H         = 15, 10
    BODY_COLOR   = (138, 105, 22)
    WING_COLOR   = (220, 188, 62)
    ACCENT_COLOR = (148, 78, 38)
    HOVER_RANGE  = 55
    SPEED        = 24.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class RosyMapleMoth(Insect):
    SPECIES      = "rosy_maple_moth"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "birch_forest"]
    W, H         = 11, 8
    BODY_COLOR   = (235, 195, 78)
    WING_COLOR   = (245, 215, 105)
    ACCENT_COLOR = (235, 138, 178)
    HOVER_RANGE  = 45
    SPEED        = 26.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class WhiteFurcula(Insect):
    SPECIES      = "white_furcula"
    RARITY       = "common"
    BIOMES       = ["temperate", "birch_forest"]
    W, H         = 11, 7
    BODY_COLOR   = (215, 215, 215)
    WING_COLOR   = (235, 235, 235)
    ACCENT_COLOR = (108, 108, 108)
    HOVER_RANGE  = 42
    SPEED        = 24.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class PandoraSphinx(Insect):
    SPECIES      = "pandora_sphinx"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "birch_forest"]
    W, H         = 14, 8
    BODY_COLOR   = (62, 78, 52)
    WING_COLOR   = (108, 128, 88)
    ACCENT_COLOR = (188, 138, 175)
    HOVER_RANGE  = 55
    SPEED        = 38.0
    WING_TYPE    = "moth"


class AbbottsSphinx(Insect):
    SPECIES      = "abbotts_sphinx"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "wetland"]
    W, H         = 13, 8
    BODY_COLOR   = (62, 42, 22)
    WING_COLOR   = (108, 78, 45)
    ACCENT_COLOR = (188, 158, 88)
    HOVER_RANGE  = 50
    SPEED        = 36.0
    WING_TYPE    = "moth"


class BlindedSphinx(Insect):
    SPECIES      = "blinded_sphinx"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "birch_forest"]
    W, H         = 13, 8
    BODY_COLOR   = (78, 62, 38)
    WING_COLOR   = (138, 115, 78)
    ACCENT_COLOR = (215, 92, 62)
    HOVER_RANGE  = 50
    SPEED        = 38.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class AchemonSphinx(Insect):
    SPECIES      = "achemon_sphinx"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 13, 8
    BODY_COLOR   = (105, 78, 65)
    WING_COLOR   = (175, 138, 115)
    ACCENT_COLOR = (215, 188, 158)
    HOVER_RANGE  = 50
    SPEED        = 36.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class UnderwingCatocala(Insect):
    SPECIES      = "underwing_catocala"
    RARITY       = "rare"
    BIOMES       = ["temperate", "birch_forest"]
    W, H         = 14, 9
    BODY_COLOR   = (78, 62, 38)
    WING_COLOR   = (118, 95, 62)
    ACCENT_COLOR = (215, 65, 38)
    HOVER_RANGE  = 50
    SPEED        = 26.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class GiantLeopardMoth(Insect):
    SPECIES      = "giant_leopard_moth"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 14, 9
    BODY_COLOR   = (245, 245, 245)
    WING_COLOR   = (245, 245, 245)
    ACCENT_COLOR = (28, 28, 28)
    HOVER_RANGE  = 50
    SPEED        = 26.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class SaltMarshMoth(Insect):
    SPECIES      = "salt_marsh_moth"
    RARITY       = "common"
    BIOMES       = ["wetland", "beach"]
    W, H         = 12, 8
    BODY_COLOR   = (215, 165, 38)
    WING_COLOR   = (245, 235, 215)
    ACCENT_COLOR = (32, 32, 32)
    HOVER_RANGE  = 45
    SPEED        = 26.0
    WING_TYPE    = "moth"


class EightSpottedForester(Insect):
    SPECIES      = "eight_spotted_forester"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "birch_forest"]
    W, H         = 11, 7
    BODY_COLOR   = (28, 22, 22)
    WING_COLOR   = (38, 32, 32)
    ACCENT_COLOR = (240, 230, 218)
    HOVER_RANGE  = 45
    SPEED        = 28.0
    WING_TYPE    = "moth"


class TulipTreeBeauty(Insect):
    SPECIES      = "tulip_tree_beauty"
    RARITY       = "common"
    BIOMES       = ["temperate", "birch_forest"]
    W, H         = 12, 8
    BODY_COLOR   = (138, 105, 78)
    WING_COLOR   = (188, 158, 128)
    ACCENT_COLOR = (62, 48, 38)
    HOVER_RANGE  = 45
    SPEED        = 26.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


# --- NA other ---

class CarolinaMantis(Insect):
    SPECIES      = "carolina_mantis"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 13, 7
    BODY_COLOR   = (108, 95, 62)
    WING_COLOR   = (148, 138, 92)
    ACCENT_COLOR = (188, 175, 128)
    HOVER_RANGE  = 35
    SPEED        = 24.0
    WING_TYPE    = "other"


class BaldfacedHornet(Insect):
    SPECIES      = "baldfaced_hornet"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "birch_forest"]
    W, H         = 12, 6
    BODY_COLOR   = (22, 22, 22)
    WING_COLOR   = (62, 62, 62)
    ACCENT_COLOR = (235, 235, 235)
    HOVER_RANGE  = 50
    SPEED        = 38.0
    WING_TYPE    = "other"


class AmericanYellowjacket(Insect):
    SPECIES      = "american_yellowjacket"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 10, 5
    BODY_COLOR   = (38, 28, 12)
    WING_COLOR   = (215, 215, 220)
    ACCENT_COLOR = (245, 215, 62)
    HOVER_RANGE  = 45
    SPEED        = 36.0
    WING_TYPE    = "other"


class GreatBlackWasp(Insect):
    SPECIES      = "great_black_wasp"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 12, 5
    BODY_COLOR   = (18, 18, 22)
    WING_COLOR   = (32, 32, 38)
    ACCENT_COLOR = (88, 105, 178)
    HOVER_RANGE  = 50
    SPEED        = 38.0
    WING_TYPE    = "other"


class CicadaKiller(Insect):
    SPECIES      = "cicada_killer"
    RARITY       = "rare"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 13, 6
    BODY_COLOR   = (45, 28, 12)
    WING_COLOR   = (175, 138, 78)
    ACCENT_COLOR = (240, 215, 92)
    HOVER_RANGE  = 55
    SPEED        = 40.0
    WING_TYPE    = "other"


class EasternCarpenterBee(Insect):
    SPECIES      = "eastern_carpenter_bee"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 11, 6
    BODY_COLOR   = (22, 22, 28)
    WING_COLOR   = (105, 105, 115)
    ACCENT_COLOR = (215, 195, 78)
    HOVER_RANGE  = 50
    SPEED        = 34.0
    WING_TYPE    = "other"


class ValleyCarpenterBee(Insect):
    SPECIES      = "valley_carpenter_bee"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "desert"]
    W, H         = 11, 6
    BODY_COLOR   = (108, 78, 32)
    WING_COLOR   = (175, 138, 65)
    ACCENT_COLOR = (235, 195, 105)
    HOVER_RANGE  = 50
    SPEED        = 34.0
    WING_TYPE    = "other"


class SweatBee(Insect):
    SPECIES      = "sweat_bee"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 7, 4
    BODY_COLOR   = (38, 108, 78)
    WING_COLOR   = (108, 188, 128)
    ACCENT_COLOR = (215, 240, 175)
    HOVER_RANGE  = 38
    SPEED        = 34.0
    WING_TYPE    = "other"


class LeafcutterBee(Insect):
    SPECIES      = "leafcutter_bee"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 9, 5
    BODY_COLOR   = (62, 38, 22)
    WING_COLOR   = (215, 200, 178)
    ACCENT_COLOR = (148, 215, 88)
    HOVER_RANGE  = 40
    SPEED        = 34.0
    WING_TYPE    = "other"


class PeriodicalCicada(Insect):
    SPECIES      = "periodical_cicada"
    RARITY       = "rare"
    BIOMES       = ["temperate", "birch_forest"]
    W, H         = 11, 6
    BODY_COLOR   = (22, 22, 22)
    WING_COLOR   = (188, 158, 32)
    ACCENT_COLOR = (215, 48, 32)
    HOVER_RANGE  = 35
    SPEED        = 28.0
    WING_TYPE    = "other"


class DogDayCicada(Insect):
    SPECIES      = "dog_day_cicada"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 12, 6
    BODY_COLOR   = (38, 52, 38)
    WING_COLOR   = (158, 175, 138)
    ACCENT_COLOR = (215, 235, 195)
    HOVER_RANGE  = 35
    SPEED        = 28.0
    WING_TYPE    = "other"


class ScissorGrinderCicada(Insect):
    SPECIES      = "scissor_grinder_cicada"
    RARITY       = "uncommon"
    BIOMES       = ["temperate"]
    W, H         = 12, 6
    BODY_COLOR   = (48, 62, 32)
    WING_COLOR   = (158, 178, 128)
    ACCENT_COLOR = (218, 235, 188)
    HOVER_RANGE  = 35
    SPEED        = 28.0
    WING_TYPE    = "other"


class RockyMountainLocust(Insect):
    SPECIES      = "rocky_mountain_locust"
    RARITY       = "rare"
    BIOMES       = ["rocky_mountain", "rolling_hills"]
    W, H         = 12, 6
    BODY_COLOR   = (118, 92, 38)
    WING_COLOR   = (158, 128, 62)
    ACCENT_COLOR = (215, 195, 138)
    HOVER_RANGE  = 35
    SPEED        = 34.0
    WING_TYPE    = "other"


class EasternLubberGrasshopper(Insect):
    SPECIES      = "eastern_lubber_grasshopper"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "savanna"]
    W, H         = 14, 8
    BODY_COLOR   = (215, 178, 38)
    WING_COLOR   = (188, 65, 32)
    ACCENT_COLOR = (32, 22, 22)
    HOVER_RANGE  = 32
    SPEED        = 22.0
    WING_TYPE    = "other"


class DifferentialGrasshopper(Insect):
    SPECIES      = "differential_grasshopper"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 12, 6
    BODY_COLOR   = (138, 108, 38)
    WING_COLOR   = (185, 148, 65)
    ACCENT_COLOR = (32, 32, 28)
    HOVER_RANGE  = 32
    SPEED        = 32.0
    WING_TYPE    = "other"


class AmericanGrasshopper(Insect):
    SPECIES      = "american_grasshopper"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 12, 6
    BODY_COLOR   = (108, 78, 28)
    WING_COLOR   = (158, 128, 52)
    ACCENT_COLOR = (215, 188, 105)
    HOVER_RANGE  = 32
    SPEED        = 32.0
    WING_TYPE    = "other"


class SnowyTreeCricket(Insect):
    SPECIES      = "snowy_tree_cricket"
    RARITY       = "common"
    BIOMES       = ["temperate", "birch_forest"]
    W, H         = 10, 5
    BODY_COLOR   = (215, 240, 188)
    WING_COLOR   = (240, 248, 215)
    ACCENT_COLOR = (138, 175, 108)
    HOVER_RANGE  = 28
    SPEED        = 24.0
    WING_TYPE    = "other"
    NIGHT_ONLY   = True


class JerusalemCricket(Insect):
    SPECIES      = "jerusalem_cricket"
    RARITY       = "rare"
    BIOMES       = ["desert", "rocky_mountain"]
    W, H         = 13, 7
    BODY_COLOR   = (188, 138, 78)
    WING_COLOR   = (215, 175, 108)
    ACCENT_COLOR = (108, 62, 32)
    HOVER_RANGE  = 30
    SPEED        = 20.0
    WING_TYPE    = "other"
    NIGHT_ONLY   = True


class NorthernMoleCricket(Insect):
    SPECIES      = "northern_mole_cricket"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "wetland"]
    W, H         = 12, 6
    BODY_COLOR   = (88, 65, 38)
    WING_COLOR   = (128, 92, 55)
    ACCENT_COLOR = (175, 138, 88)
    HOVER_RANGE  = 30
    SPEED        = 22.0
    WING_TYPE    = "other"
    NIGHT_ONLY   = True


class AmericanWalkingstick(Insect):
    SPECIES      = "american_walkingstick"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "birch_forest"]
    W, H         = 16, 4
    BODY_COLOR   = (88, 62, 38)
    WING_COLOR   = (138, 105, 62)
    ACCENT_COLOR = (188, 158, 105)
    HOVER_RANGE  = 30
    SPEED        = 18.0
    WING_TYPE    = "other"


class WheelBug(Insect):
    SPECIES      = "wheel_bug"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 12, 7
    BODY_COLOR   = (108, 95, 78)
    WING_COLOR   = (148, 128, 108)
    ACCENT_COLOR = (62, 52, 42)
    HOVER_RANGE  = 32
    SPEED        = 26.0
    WING_TYPE    = "other"


class MaskedHunter(Insect):
    SPECIES      = "masked_hunter"
    RARITY       = "uncommon"
    BIOMES       = ["temperate"]
    W, H         = 10, 5
    BODY_COLOR   = (28, 22, 22)
    WING_COLOR   = (45, 38, 38)
    ACCENT_COLOR = (108, 92, 78)
    HOVER_RANGE  = 30
    SPEED        = 30.0
    WING_TYPE    = "other"
    NIGHT_ONLY   = True


class LargeMilkweedBug(Insect):
    SPECIES      = "large_milkweed_bug"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 9, 5
    BODY_COLOR   = (188, 38, 32)
    WING_COLOR   = (215, 62, 45)
    ACCENT_COLOR = (28, 22, 22)
    HOVER_RANGE  = 30
    SPEED        = 24.0
    WING_TYPE    = "other"


class SquashBug(Insect):
    SPECIES      = "squash_bug"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 9, 6
    BODY_COLOR   = (78, 55, 32)
    WING_COLOR   = (118, 88, 55)
    ACCENT_COLOR = (175, 138, 92)
    HOVER_RANGE  = 28
    SPEED        = 22.0
    WING_TYPE    = "other"


class BoxElderBug(Insect):
    SPECIES      = "box_elder_bug"
    RARITY       = "common"
    BIOMES       = ["temperate", "rolling_hills"]
    W, H         = 9, 5
    BODY_COLOR   = (22, 22, 22)
    WING_COLOR   = (42, 38, 38)
    ACCENT_COLOR = (215, 38, 38)
    HOVER_RANGE  = 28
    SPEED        = 24.0
    WING_TYPE    = "other"


class WesternConiferSeedBug(Insect):
    SPECIES      = "western_conifer_seed_bug"
    RARITY       = "common"
    BIOMES       = ["boreal", "redwood"]
    W, H         = 10, 5
    BODY_COLOR   = (78, 52, 22)
    WING_COLOR   = (118, 88, 38)
    ACCENT_COLOR = (175, 138, 78)
    HOVER_RANGE  = 32
    SPEED        = 26.0
    WING_TYPE    = "other"


class AmericanCockroach(Insect):
    SPECIES      = "american_cockroach"
    RARITY       = "common"
    BIOMES       = ["wetland", "swamp"]
    W, H         = 12, 6
    BODY_COLOR   = (108, 62, 28)
    WING_COLOR   = (158, 95, 42)
    ACCENT_COLOR = (215, 158, 88)
    HOVER_RANGE  = 30
    SPEED        = 38.0
    WING_TYPE    = "other"
    NIGHT_ONLY   = True


class DobsonFly(Insect):
    SPECIES      = "dobson_fly"
    RARITY       = "rare"
    BIOMES       = ["wetland", "birch_forest"]
    W, H         = 15, 6
    BODY_COLOR   = (62, 42, 28)
    WING_COLOR   = (148, 128, 95)
    ACCENT_COLOR = (215, 195, 158)
    HOVER_RANGE  = 45
    SPEED        = 28.0
    WING_TYPE    = "other"
    NIGHT_ONLY   = True


class AmericanMayfly(Insect):
    SPECIES      = "american_mayfly"
    RARITY       = "common"
    BIOMES       = ["wetland", "temperate"]
    W, H         = 11, 5
    BODY_COLOR   = (188, 158, 92)
    WING_COLOR   = (220, 205, 158)
    ACCENT_COLOR = (245, 235, 215)
    HOVER_RANGE  = 50
    SPEED        = 32.0
    WING_TYPE    = "dragonfly"
    DAWN_ONLY    = True


class AmericanCaddisfly(Insect):
    SPECIES      = "american_caddisfly"
    RARITY       = "common"
    BIOMES       = ["wetland", "birch_forest"]
    W, H         = 10, 5
    BODY_COLOR   = (78, 62, 32)
    WING_COLOR   = (138, 115, 62)
    ACCENT_COLOR = (188, 175, 118)
    HOVER_RANGE  = 38
    SPEED        = 28.0
    WING_TYPE    = "moth"
    DUSK_ONLY    = True


# ---------------------------------------------------------------------------
# South American fauna (100 species)
# ---------------------------------------------------------------------------

# --- SA butterflies ---

class HelenaMorpho(Insect):
    SPECIES      = "helena_morpho"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 16, 12
    BODY_COLOR   = (22, 22, 32)
    WING_COLOR   = (62, 92, 215)
    ACCENT_COLOR = (138, 175, 245)
    HOVER_RANGE  = 65
    SPEED        = 28.0
    WING_TYPE    = "butterfly"


class CommonMorpho(Insect):
    SPECIES      = "common_morpho"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 15, 11
    BODY_COLOR   = (22, 22, 32)
    WING_COLOR   = (72, 108, 215)
    ACCENT_COLOR = (155, 188, 245)
    HOVER_RANGE  = 60
    SPEED        = 28.0
    WING_TYPE    = "butterfly"


class AchillesMorpho(Insect):
    SPECIES      = "achilles_morpho"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 15, 11
    BODY_COLOR   = (28, 28, 38)
    WING_COLOR   = (62, 88, 195)
    ACCENT_COLOR = (240, 240, 248)
    HOVER_RANGE  = 60
    SPEED        = 28.0
    WING_TYPE    = "butterfly"


class CramerMorpho(Insect):
    SPECIES      = "cramer_morpho"
    RARITY       = "rare"
    BIOMES       = ["jungle"]
    W, H         = 15, 11
    BODY_COLOR   = (32, 32, 48)
    WING_COLOR   = (78, 118, 188)
    ACCENT_COLOR = (188, 215, 248)
    HOVER_RANGE  = 60
    SPEED        = 28.0
    WING_TYPE    = "butterfly"


class OwlButterfly(Insect):
    SPECIES      = "owl_butterfly"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 15, 11
    BODY_COLOR   = (62, 42, 22)
    WING_COLOR   = (118, 88, 55)
    ACCENT_COLOR = (32, 22, 18)
    HOVER_RANGE  = 55
    SPEED        = 26.0
    WING_TYPE    = "butterfly"


class GiantOwlButterfly(Insect):
    SPECIES      = "giant_owl_butterfly"
    RARITY       = "rare"
    BIOMES       = ["jungle"]
    W, H         = 16, 12
    BODY_COLOR   = (62, 38, 22)
    WING_COLOR   = (118, 78, 48)
    ACCENT_COLOR = (28, 22, 22)
    HOVER_RANGE  = 60
    SPEED        = 24.0
    WING_TYPE    = "butterfly"


class GlasswingButterfly(Insect):
    SPECIES      = "glasswing_butterfly"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 12, 9
    BODY_COLOR   = (22, 22, 22)
    WING_COLOR   = (215, 215, 220)
    ACCENT_COLOR = (148, 38, 32)
    HOVER_RANGE  = 50
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class CrackerButterfly(Insect):
    SPECIES      = "cracker_butterfly"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 12, 9
    BODY_COLOR   = (62, 62, 78)
    WING_COLOR   = (138, 138, 158)
    ACCENT_COLOR = (28, 28, 32)
    HOVER_RANGE  = 50
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class BlueCracker(Insect):
    SPECIES      = "blue_cracker"
    RARITY       = "uncommon"
    BIOMES       = ["jungle"]
    W, H         = 12, 9
    BODY_COLOR   = (32, 42, 78)
    WING_COLOR   = (78, 118, 178)
    ACCENT_COLOR = (188, 220, 245)
    HOVER_RANGE  = 50
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class JuliaHeliconian(Insect):
    SPECIES      = "julia_heliconian"
    RARITY       = "common"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 12, 8
    BODY_COLOR   = (78, 32, 12)
    WING_COLOR   = (235, 118, 38)
    ACCENT_COLOR = (32, 22, 18)
    HOVER_RANGE  = 50
    SPEED        = 32.0
    WING_TYPE    = "butterfly"


class ErythraeaHeliconian(Insect):
    SPECIES      = "erythraea_heliconian"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 13, 8
    BODY_COLOR   = (78, 22, 22)
    WING_COLOR   = (188, 38, 38)
    ACCENT_COLOR = (245, 218, 88)
    HOVER_RANGE  = 50
    SPEED        = 32.0
    WING_TYPE    = "butterfly"


class ScarletPeacock(Insect):
    SPECIES      = "scarlet_peacock"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 12, 9
    BODY_COLOR   = (78, 22, 18)
    WING_COLOR   = (215, 55, 32)
    ACCENT_COLOR = (32, 22, 18)
    HOVER_RANGE  = 50
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class AmazonNymph(Insect):
    SPECIES      = "amazon_nymph"
    RARITY       = "uncommon"
    BIOMES       = ["jungle"]
    W, H         = 12, 9
    BODY_COLOR   = (62, 38, 22)
    WING_COLOR   = (188, 138, 62)
    ACCENT_COLOR = (235, 215, 138)
    HOVER_RANGE  = 50
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class RuddyDaggerwing(Insect):
    SPECIES      = "ruddy_daggerwing"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 13, 9
    BODY_COLOR   = (118, 62, 22)
    WING_COLOR   = (215, 105, 38)
    ACCENT_COLOR = (38, 22, 18)
    HOVER_RANGE  = 55
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class SilverEmperorButterfly(Insect):
    SPECIES      = "silver_emperor_butterfly"
    RARITY       = "rare"
    BIOMES       = ["jungle"]
    W, H         = 14, 10
    BODY_COLOR   = (108, 108, 118)
    WING_COLOR   = (188, 188, 200)
    ACCENT_COLOR = (245, 245, 250)
    HOVER_RANGE  = 60
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class PurpleSpottedSwallowtail(Insect):
    SPECIES      = "purple_spotted_swallowtail"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 14, 10
    BODY_COLOR   = (32, 22, 42)
    WING_COLOR   = (62, 38, 92)
    ACCENT_COLOR = (175, 105, 215)
    HOVER_RANGE  = 60
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class AmazonianSwallowtail(Insect):
    SPECIES      = "amazonian_swallowtail"
    RARITY       = "uncommon"
    BIOMES       = ["jungle"]
    W, H         = 14, 10
    BODY_COLOR   = (22, 22, 22)
    WING_COLOR   = (32, 38, 28)
    ACCENT_COLOR = (245, 220, 92)
    HOVER_RANGE  = 60
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class TropicalKiteSwallowtail(Insect):
    SPECIES      = "tropical_kite_swallowtail"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 14, 10
    BODY_COLOR   = (32, 32, 32)
    WING_COLOR   = (245, 240, 230)
    ACCENT_COLOR = (108, 188, 138)
    HOVER_RANGE  = 60
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class AmazonSulphur(Insect):
    SPECIES      = "amazon_sulphur"
    RARITY       = "common"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 11, 8
    BODY_COLOR   = (108, 92, 32)
    WING_COLOR   = (245, 215, 75)
    ACCENT_COLOR = (188, 138, 38)
    HOVER_RANGE  = 45
    SPEED        = 28.0
    WING_TYPE    = "butterfly"


class CloudedMimic(Insect):
    SPECIES      = "clouded_mimic"
    RARITY       = "uncommon"
    BIOMES       = ["jungle"]
    W, H         = 12, 9
    BODY_COLOR   = (52, 42, 22)
    WING_COLOR   = (108, 88, 55)
    ACCENT_COLOR = (215, 195, 138)
    HOVER_RANGE  = 50
    SPEED        = 28.0
    WING_TYPE    = "butterfly"


class RubyEyedBrushfoot(Insect):
    SPECIES      = "ruby_eyed_brushfoot"
    RARITY       = "uncommon"
    BIOMES       = ["jungle"]
    W, H         = 12, 9
    BODY_COLOR   = (78, 22, 22)
    WING_COLOR   = (138, 42, 42)
    ACCENT_COLOR = (235, 188, 78)
    HOVER_RANGE  = 50
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class AndeanFritillary(Insect):
    SPECIES      = "andean_fritillary"
    RARITY       = "uncommon"
    BIOMES       = ["alpine_mountain", "rocky_mountain"]
    W, H         = 12, 9
    BODY_COLOR   = (62, 38, 18)
    WING_COLOR   = (205, 138, 38)
    ACCENT_COLOR = (32, 28, 22)
    HOVER_RANGE  = 55
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class PatagonianBlue(Insect):
    SPECIES      = "patagonian_blue"
    RARITY       = "uncommon"
    BIOMES       = ["steppe", "rocky_mountain"]
    W, H         = 9, 7
    BODY_COLOR   = (38, 62, 138)
    WING_COLOR   = (88, 138, 215)
    ACCENT_COLOR = (188, 220, 248)
    HOVER_RANGE  = 40
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class ScarletMormon(Insect):
    SPECIES      = "scarlet_mormon"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 14, 10
    BODY_COLOR   = (28, 22, 22)
    WING_COLOR   = (45, 38, 38)
    ACCENT_COLOR = (215, 38, 55)
    HOVER_RANGE  = 60
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


class MarbledGlasswing(Insect):
    SPECIES      = "marbled_glasswing"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 12, 9
    BODY_COLOR   = (32, 32, 32)
    WING_COLOR   = (220, 215, 220)
    ACCENT_COLOR = (62, 62, 65)
    HOVER_RANGE  = 50
    SPEED        = 30.0
    WING_TYPE    = "butterfly"


# --- SA beetles ---

class TitanBeetle(Insect):
    SPECIES      = "titan_beetle"
    RARITY       = "rare"
    BIOMES       = ["jungle"]
    W, H         = 16, 8
    BODY_COLOR   = (62, 42, 22)
    WING_COLOR   = (108, 78, 38)
    ACCENT_COLOR = (175, 138, 78)
    HOVER_RANGE  = 32
    SPEED        = 22.0
    WING_TYPE    = "beetle"


class ElephantBeetle(Insect):
    SPECIES      = "elephant_beetle"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 15, 8
    BODY_COLOR   = (38, 32, 22)
    WING_COLOR   = (62, 52, 38)
    ACCENT_COLOR = (115, 105, 78)
    HOVER_RANGE  = 32
    SPEED        = 22.0
    WING_TYPE    = "beetle"


class HarlequinBeetle(Insect):
    SPECIES      = "harlequin_beetle"
    RARITY       = "rare"
    BIOMES       = ["jungle"]
    W, H         = 15, 6
    BODY_COLOR   = (138, 92, 32)
    WING_COLOR   = (32, 32, 38)
    ACCENT_COLOR = (215, 55, 38)
    HOVER_RANGE  = 32
    SPEED        = 24.0
    WING_TYPE    = "beetle"


class JewelScarab(Insect):
    SPECIES      = "jewel_scarab"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 12, 7
    BODY_COLOR   = (45, 105, 88)
    WING_COLOR   = (62, 188, 148)
    ACCENT_COLOR = (188, 245, 215)
    HOVER_RANGE  = 32
    SPEED        = 24.0
    WING_TYPE    = "beetle"


class BrazilianJewelBeetle(Insect):
    SPECIES      = "brazilian_jewel_beetle"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 12, 7
    BODY_COLOR   = (78, 32, 105)
    WING_COLOR   = (138, 62, 188)
    ACCENT_COLOR = (215, 138, 235)
    HOVER_RANGE  = 32
    SPEED        = 24.0
    WING_TYPE    = "beetle"


class AmazonianFireBeetle(Insect):
    SPECIES      = "amazonian_fire_beetle"
    RARITY       = "uncommon"
    BIOMES       = ["jungle"]
    W, H         = 11, 6
    BODY_COLOR   = (138, 38, 18)
    WING_COLOR   = (215, 78, 38)
    ACCENT_COLOR = (250, 178, 105)
    HOVER_RANGE  = 32
    SPEED        = 26.0
    WING_TYPE    = "beetle"


class AndeanWeevil(Insect):
    SPECIES      = "andean_weevil"
    RARITY       = "uncommon"
    BIOMES       = ["alpine_mountain", "rocky_mountain"]
    W, H         = 9, 6
    BODY_COLOR   = (62, 62, 78)
    WING_COLOR   = (108, 108, 138)
    ACCENT_COLOR = (175, 178, 215)
    HOVER_RANGE  = 28
    SPEED        = 22.0
    WING_TYPE    = "beetle"


class CaribbeanRhinoBeetle(Insect):
    SPECIES      = "caribbean_rhino_beetle"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 13, 7
    BODY_COLOR   = (32, 22, 22)
    WING_COLOR   = (62, 42, 32)
    ACCENT_COLOR = (138, 92, 55)
    HOVER_RANGE  = 32
    SPEED        = 24.0
    WING_TYPE    = "beetle"


class AmazonStagBeetle(Insect):
    SPECIES      = "amazon_stag_beetle"
    RARITY       = "rare"
    BIOMES       = ["jungle"]
    W, H         = 14, 7
    BODY_COLOR   = (42, 28, 18)
    WING_COLOR   = (78, 52, 32)
    ACCENT_COLOR = (148, 105, 62)
    HOVER_RANGE  = 32
    SPEED        = 22.0
    WING_TYPE    = "beetle"


class NeotropicalLonghorn(Insect):
    SPECIES      = "neotropical_longhorn"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 14, 6
    BODY_COLOR   = (62, 42, 22)
    WING_COLOR   = (118, 78, 38)
    ACCENT_COLOR = (188, 148, 92)
    HOVER_RANGE  = 32
    SPEED        = 24.0
    WING_TYPE    = "beetle"


class NeotropicalRhinoBeetle(Insect):
    SPECIES      = "neotropical_rhino_beetle"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 13, 7
    BODY_COLOR   = (38, 28, 18)
    WING_COLOR   = (72, 52, 28)
    ACCENT_COLOR = (148, 115, 65)
    HOVER_RANGE  = 32
    SPEED        = 24.0
    WING_TYPE    = "beetle"


class AndeanTigerBeetle(Insect):
    SPECIES      = "andean_tiger_beetle"
    RARITY       = "uncommon"
    BIOMES       = ["alpine_mountain", "rocky_mountain"]
    W, H         = 11, 6
    BODY_COLOR   = (38, 62, 88)
    WING_COLOR   = (78, 118, 148)
    ACCENT_COLOR = (235, 215, 92)
    HOVER_RANGE  = 32
    SPEED        = 34.0
    WING_TYPE    = "beetle"


class AmazonianGoldChafer(Insect):
    SPECIES      = "amazonian_gold_chafer"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 11, 6
    BODY_COLOR   = (138, 105, 22)
    WING_COLOR   = (215, 178, 55)
    ACCENT_COLOR = (250, 235, 138)
    HOVER_RANGE  = 32
    SPEED        = 26.0
    WING_TYPE    = "beetle"


class HornedPassalusBeetle(Insect):
    SPECIES      = "horned_passalus_beetle"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 12, 6
    BODY_COLOR   = (22, 22, 22)
    WING_COLOR   = (42, 38, 38)
    ACCENT_COLOR = (108, 92, 78)
    HOVER_RANGE  = 30
    SPEED        = 22.0
    WING_TYPE    = "beetle"


class AmazonianClickBeetle(Insect):
    SPECIES      = "amazonian_click_beetle"
    RARITY       = "uncommon"
    BIOMES       = ["jungle"]
    W, H         = 12, 6
    BODY_COLOR   = (28, 28, 28)
    WING_COLOR   = (52, 52, 52)
    ACCENT_COLOR = (175, 235, 138)
    HOVER_RANGE  = 32
    SPEED        = 28.0
    WING_TYPE    = "beetle"


# --- SA dragonflies ---

class AmazonHelicopterDamsel(Insect):
    SPECIES      = "amazon_helicopter_damsel"
    RARITY       = "rare"
    BIOMES       = ["jungle"]
    W, H         = 16, 5
    BODY_COLOR   = (32, 32, 32)
    WING_COLOR   = (62, 62, 62)
    ACCENT_COLOR = (215, 235, 215)
    HOVER_RANGE  = 65
    SPEED        = 32.0
    WING_TYPE    = "dragonfly"


class NeotropicalGreatPondhawk(Insect):
    SPECIES      = "neotropical_great_pondhawk"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "jungle"]
    W, H         = 13, 5
    BODY_COLOR   = (62, 138, 88)
    WING_COLOR   = (108, 188, 128)
    ACCENT_COLOR = (215, 245, 175)
    HOVER_RANGE  = 55
    SPEED        = 36.0
    WING_TYPE    = "dragonfly"


class ScarletSkimmerSA(Insect):
    SPECIES      = "scarlet_skimmer_sa"
    RARITY       = "common"
    BIOMES       = ["wetland", "jungle"]
    W, H         = 12, 4
    BODY_COLOR   = (188, 38, 28)
    WING_COLOR   = (235, 78, 55)
    ACCENT_COLOR = (250, 215, 195)
    HOVER_RANGE  = 50
    SPEED        = 34.0
    WING_TYPE    = "dragonfly"


class FieryRubyspot(Insect):
    SPECIES      = "fiery_rubyspot"
    RARITY       = "uncommon"
    BIOMES       = ["wetland", "jungle"]
    W, H         = 12, 4
    BODY_COLOR   = (32, 22, 22)
    WING_COLOR   = (62, 32, 32)
    ACCENT_COLOR = (235, 55, 38)
    HOVER_RANGE  = 50
    SPEED        = 32.0
    WING_TYPE    = "dragonfly"


class NeotropicalGlider(Insect):
    SPECIES      = "neotropical_glider"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "wetland"]
    W, H         = 14, 5
    BODY_COLOR   = (188, 92, 32)
    WING_COLOR   = (235, 158, 55)
    ACCENT_COLOR = (250, 215, 138)
    HOVER_RANGE  = 55
    SPEED        = 36.0
    WING_TYPE    = "dragonfly"


class AmazonianDarner(Insect):
    SPECIES      = "amazonian_darner"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "wetland"]
    W, H         = 15, 5
    BODY_COLOR   = (32, 88, 62)
    WING_COLOR   = (78, 158, 108)
    ACCENT_COLOR = (188, 235, 175)
    HOVER_RANGE  = 60
    SPEED        = 38.0
    WING_TYPE    = "dragonfly"


class AndeanGreenSkimmer(Insect):
    SPECIES      = "andean_green_skimmer"
    RARITY       = "uncommon"
    BIOMES       = ["alpine_mountain", "wetland"]
    W, H         = 13, 5
    BODY_COLOR   = (38, 108, 78)
    WING_COLOR   = (78, 178, 128)
    ACCENT_COLOR = (175, 245, 195)
    HOVER_RANGE  = 55
    SPEED        = 34.0
    WING_TYPE    = "dragonfly"


class PatagonianDarter(Insect):
    SPECIES      = "patagonian_darter"
    RARITY       = "uncommon"
    BIOMES       = ["steppe", "wetland"]
    W, H         = 12, 4
    BODY_COLOR   = (158, 78, 38)
    WING_COLOR   = (215, 138, 78)
    ACCENT_COLOR = (245, 215, 175)
    HOVER_RANGE  = 50
    SPEED        = 34.0
    WING_TYPE    = "dragonfly"


class RustyClubtail(Insect):
    SPECIES      = "rusty_clubtail"
    RARITY       = "common"
    BIOMES       = ["wetland", "jungle"]
    W, H         = 13, 5
    BODY_COLOR   = (108, 62, 22)
    WING_COLOR   = (175, 118, 55)
    ACCENT_COLOR = (235, 195, 138)
    HOVER_RANGE  = 50
    SPEED        = 32.0
    WING_TYPE    = "dragonfly"


class RainforestDamselfly(Insect):
    SPECIES      = "rainforest_damselfly"
    RARITY       = "common"
    BIOMES       = ["jungle", "wetland"]
    W, H         = 11, 3
    BODY_COLOR   = (62, 138, 88)
    WING_COLOR   = (148, 215, 178)
    ACCENT_COLOR = (220, 248, 235)
    HOVER_RANGE  = 45
    SPEED        = 30.0
    WING_TYPE    = "dragonfly"


# --- SA fireflies ---

class AmazonianFirefly(Insect):
    SPECIES      = "amazonian_firefly"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "wetland"]
    W, H         = 9, 6
    BODY_COLOR   = (28, 22, 22)
    WING_COLOR   = (48, 38, 32)
    ACCENT_COLOR = (245, 235, 138)
    HOVER_RANGE  = 52
    SPEED        = 22.0
    WING_TYPE    = "firefly"
    NIGHT_ONLY   = True


class AndeanFirefly(Insect):
    SPECIES      = "andean_firefly"
    RARITY       = "rare"
    BIOMES       = ["alpine_mountain", "rocky_mountain"]
    W, H         = 9, 6
    BODY_COLOR   = (22, 22, 32)
    WING_COLOR   = (38, 38, 52)
    ACCENT_COLOR = (188, 235, 195)
    HOVER_RANGE  = 50
    SPEED        = 20.0
    WING_TYPE    = "firefly"
    NIGHT_ONLY   = True


class BrazilianRailroadGlow(Insect):
    SPECIES      = "brazilian_railroad_glow"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 10, 5
    BODY_COLOR   = (32, 22, 18)
    WING_COLOR   = (62, 42, 32)
    ACCENT_COLOR = (235, 88, 55)
    HOVER_RANGE  = 45
    SPEED        = 18.0
    WING_TYPE    = "firefly"
    NIGHT_ONLY   = True


class AmazonGiantFirefly(Insect):
    SPECIES      = "amazon_giant_firefly"
    RARITY       = "rare"
    BIOMES       = ["jungle"]
    W, H         = 11, 7
    BODY_COLOR   = (32, 22, 22)
    WING_COLOR   = (52, 42, 32)
    ACCENT_COLOR = (250, 240, 158)
    HOVER_RANGE  = 58
    SPEED        = 22.0
    WING_TYPE    = "firefly"
    NIGHT_ONLY   = True


class TropicalNightfire(Insect):
    SPECIES      = "tropical_nightfire"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 9, 6
    BODY_COLOR   = (28, 22, 22)
    WING_COLOR   = (48, 38, 32)
    ACCENT_COLOR = (255, 175, 78)
    HOVER_RANGE  = 50
    SPEED        = 22.0
    WING_TYPE    = "firefly"
    NIGHT_ONLY   = True


# --- SA moths ---

class WhiteWitchMoth(Insect):
    SPECIES      = "white_witch_moth"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 16, 11
    BODY_COLOR   = (188, 175, 158)
    WING_COLOR   = (235, 230, 220)
    ACCENT_COLOR = (108, 95, 78)
    HOVER_RANGE  = 60
    SPEED        = 26.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class JaguarMoth(Insect):
    SPECIES      = "jaguar_moth"
    RARITY       = "uncommon"
    BIOMES       = ["jungle"]
    W, H         = 13, 9
    BODY_COLOR   = (188, 138, 38)
    WING_COLOR   = (235, 188, 62)
    ACCENT_COLOR = (32, 28, 22)
    HOVER_RANGE  = 50
    SPEED        = 26.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class AmazonHawkMoth(Insect):
    SPECIES      = "amazon_hawk_moth"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 14, 8
    BODY_COLOR   = (62, 48, 32)
    WING_COLOR   = (118, 95, 62)
    ACCENT_COLOR = (188, 158, 105)
    HOVER_RANGE  = 55
    SPEED        = 38.0
    WING_TYPE    = "moth"


class RubyHawkMoth(Insect):
    SPECIES      = "ruby_hawk_moth"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 13, 7
    BODY_COLOR   = (108, 22, 38)
    WING_COLOR   = (188, 38, 55)
    ACCENT_COLOR = (245, 138, 158)
    HOVER_RANGE  = 50
    SPEED        = 38.0
    WING_TYPE    = "moth"


class PinkSpottedHawkmoth(Insect):
    SPECIES      = "pink_spotted_hawkmoth"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 14, 8
    BODY_COLOR   = (78, 62, 62)
    WING_COLOR   = (148, 118, 118)
    ACCENT_COLOR = (235, 138, 175)
    HOVER_RANGE  = 55
    SPEED        = 38.0
    WING_TYPE    = "moth"


class AndeanSilkmoth(Insect):
    SPECIES      = "andean_silkmoth"
    RARITY       = "rare"
    BIOMES       = ["alpine_mountain", "rocky_mountain"]
    W, H         = 14, 9
    BODY_COLOR   = (158, 148, 138)
    WING_COLOR   = (215, 205, 195)
    ACCENT_COLOR = (115, 78, 65)
    HOVER_RANGE  = 55
    SPEED        = 24.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class TropicalEmperorMoth(Insect):
    SPECIES      = "tropical_emperor_moth"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 15, 10
    BODY_COLOR   = (62, 38, 78)
    WING_COLOR   = (138, 92, 148)
    ACCENT_COLOR = (235, 195, 218)
    HOVER_RANGE  = 60
    SPEED        = 24.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class AmazonRoyalMoth(Insect):
    SPECIES      = "amazon_royal_moth"
    RARITY       = "rare"
    BIOMES       = ["jungle"]
    W, H         = 16, 11
    BODY_COLOR   = (108, 38, 22)
    WING_COLOR   = (175, 78, 38)
    ACCENT_COLOR = (245, 215, 92)
    HOVER_RANGE  = 60
    SPEED        = 24.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class AmazonGiantSilkmoth(Insect):
    SPECIES      = "amazon_giant_silkmoth"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 16, 11
    BODY_COLOR   = (78, 52, 32)
    WING_COLOR   = (148, 105, 62)
    ACCENT_COLOR = (220, 188, 138)
    HOVER_RANGE  = 60
    SPEED        = 24.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class UraniaMoth(Insect):
    SPECIES      = "urania_moth"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 14, 10
    BODY_COLOR   = (22, 22, 22)
    WING_COLOR   = (38, 38, 42)
    ACCENT_COLOR = (62, 188, 158)
    HOVER_RANGE  = 55
    SPEED        = 30.0
    WING_TYPE    = "moth"


class SunsetMoth(Insect):
    SPECIES      = "sunset_moth"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 14, 10
    BODY_COLOR   = (22, 22, 22)
    WING_COLOR   = (62, 38, 38)
    ACCENT_COLOR = (235, 128, 38)
    HOVER_RANGE  = 55
    SPEED        = 30.0
    WING_TYPE    = "moth"


class EcuadorianHawkMoth(Insect):
    SPECIES      = "ecuadorian_hawk_moth"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "alpine_mountain"]
    W, H         = 14, 8
    BODY_COLOR   = (62, 92, 62)
    WING_COLOR   = (108, 148, 105)
    ACCENT_COLOR = (188, 215, 175)
    HOVER_RANGE  = 55
    SPEED        = 38.0
    WING_TYPE    = "moth"


class SaturniidEclipseMoth(Insect):
    SPECIES      = "saturniid_eclipse_moth"
    RARITY       = "rare"
    BIOMES       = ["jungle"]
    W, H         = 15, 10
    BODY_COLOR   = (28, 22, 32)
    WING_COLOR   = (62, 52, 78)
    ACCENT_COLOR = (215, 178, 95)
    HOVER_RANGE  = 55
    SPEED        = 24.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


class PatagonianTigerMoth(Insect):
    SPECIES      = "patagonian_tiger_moth"
    RARITY       = "uncommon"
    BIOMES       = ["steppe", "rocky_mountain"]
    W, H         = 12, 8
    BODY_COLOR   = (28, 22, 22)
    WING_COLOR   = (62, 38, 38)
    ACCENT_COLOR = (235, 195, 88)
    HOVER_RANGE  = 50
    SPEED        = 26.0
    WING_TYPE    = "moth"


class AmazonTussockMoth(Insect):
    SPECIES      = "amazon_tussock_moth"
    RARITY       = "common"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 11, 7
    BODY_COLOR   = (148, 105, 62)
    WING_COLOR   = (215, 175, 118)
    ACCENT_COLOR = (245, 218, 175)
    HOVER_RANGE  = 42
    SPEED        = 24.0
    WING_TYPE    = "moth"
    NIGHT_ONLY   = True


# --- SA other ---

class JungleNymphMantis(Insect):
    SPECIES      = "jungle_nymph_mantis"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 14, 8
    BODY_COLOR   = (62, 108, 38)
    WING_COLOR   = (108, 158, 62)
    ACCENT_COLOR = (175, 215, 108)
    HOVER_RANGE  = 35
    SPEED        = 22.0
    WING_TYPE    = "other"


class BrazilianDeadLeafMantis(Insect):
    SPECIES      = "brazilian_dead_leaf_mantis"
    RARITY       = "rare"
    BIOMES       = ["jungle"]
    W, H         = 14, 8
    BODY_COLOR   = (88, 55, 28)
    WING_COLOR   = (138, 88, 45)
    ACCENT_COLOR = (188, 138, 78)
    HOVER_RANGE  = 32
    SPEED        = 20.0
    WING_TYPE    = "other"


class PeruvianStickInsect(Insect):
    SPECIES      = "peruvian_stick_insect"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "alpine_mountain"]
    W, H         = 16, 4
    BODY_COLOR   = (78, 55, 32)
    WING_COLOR   = (118, 88, 52)
    ACCENT_COLOR = (175, 138, 88)
    HOVER_RANGE  = 30
    SPEED        = 18.0
    WING_TYPE    = "other"


class AmazonLeafInsect(Insect):
    SPECIES      = "amazon_leaf_insect"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 13, 9
    BODY_COLOR   = (62, 105, 38)
    WING_COLOR   = (108, 158, 62)
    ACCENT_COLOR = (175, 215, 105)
    HOVER_RANGE  = 30
    SPEED        = 18.0
    WING_TYPE    = "other"


class BulletAnt(Insect):
    SPECIES      = "bullet_ant"
    RARITY       = "rare"
    BIOMES       = ["jungle"]
    W, H         = 9, 5
    BODY_COLOR   = (38, 22, 18)
    WING_COLOR   = (62, 38, 28)
    ACCENT_COLOR = (138, 88, 55)
    HOVER_RANGE  = 28
    SPEED        = 30.0
    WING_TYPE    = "other"


class LeafcutterAnt(Insect):
    SPECIES      = "leafcutter_ant"
    RARITY       = "common"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 8, 4
    BODY_COLOR   = (88, 52, 32)
    WING_COLOR   = (138, 88, 55)
    ACCENT_COLOR = (138, 188, 88)
    HOVER_RANGE  = 28
    SPEED        = 30.0
    WING_TYPE    = "other"


class ArmyAnt(Insect):
    SPECIES      = "army_ant"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 8, 4
    BODY_COLOR   = (62, 32, 18)
    WING_COLOR   = (108, 55, 32)
    ACCENT_COLOR = (158, 88, 52)
    HOVER_RANGE  = 28
    SPEED        = 32.0
    WING_TYPE    = "other"


class AmazonFireAnt(Insect):
    SPECIES      = "amazon_fire_ant"
    RARITY       = "common"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 7, 4
    BODY_COLOR   = (148, 38, 22)
    WING_COLOR   = (185, 62, 32)
    ACCENT_COLOR = (235, 118, 78)
    HOVER_RANGE  = 25
    SPEED        = 30.0
    WING_TYPE    = "other"


class NeotropicalAssassinBug(Insect):
    SPECIES      = "neotropical_assassin_bug"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 11, 6
    BODY_COLOR   = (118, 22, 28)
    WING_COLOR   = (175, 38, 42)
    ACCENT_COLOR = (28, 22, 22)
    HOVER_RANGE  = 35
    SPEED        = 30.0
    WING_TYPE    = "other"


class AmazonOrchidBee(Insect):
    SPECIES      = "amazon_orchid_bee"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 10, 5
    BODY_COLOR   = (32, 88, 78)
    WING_COLOR   = (62, 188, 158)
    ACCENT_COLOR = (148, 245, 215)
    HOVER_RANGE  = 50
    SPEED        = 38.0
    WING_TYPE    = "other"


class EuglossineBee(Insect):
    SPECIES      = "euglossine_bee"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 9, 5
    BODY_COLOR   = (32, 38, 138)
    WING_COLOR   = (62, 78, 215)
    ACCENT_COLOR = (158, 188, 245)
    HOVER_RANGE  = 45
    SPEED        = 36.0
    WING_TYPE    = "other"


class AmazonStinglessBee(Insect):
    SPECIES      = "amazon_stingless_bee"
    RARITY       = "common"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 8, 5
    BODY_COLOR   = (62, 42, 18)
    WING_COLOR   = (138, 105, 62)
    ACCENT_COLOR = (215, 178, 105)
    HOVER_RANGE  = 40
    SPEED        = 32.0
    WING_TYPE    = "other"


class CitronellaAnt(Insect):
    SPECIES      = "citronella_ant"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "wetland"]
    W, H         = 7, 4
    BODY_COLOR   = (188, 148, 38)
    WING_COLOR   = (215, 188, 78)
    ACCENT_COLOR = (245, 230, 148)
    HOVER_RANGE  = 28
    SPEED        = 28.0
    WING_TYPE    = "other"


class AmazonGiantCockroach(Insect):
    SPECIES      = "amazon_giant_cockroach"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 13, 7
    BODY_COLOR   = (78, 42, 22)
    WING_COLOR   = (128, 78, 38)
    ACCENT_COLOR = (188, 138, 78)
    HOVER_RANGE  = 30
    SPEED        = 36.0
    WING_TYPE    = "other"
    NIGHT_ONLY   = True


class PatagonianGrasshopper(Insect):
    SPECIES      = "patagonian_grasshopper"
    RARITY       = "common"
    BIOMES       = ["steppe", "rocky_mountain"]
    W, H         = 11, 6
    BODY_COLOR   = (108, 92, 62)
    WING_COLOR   = (158, 138, 92)
    ACCENT_COLOR = (215, 195, 148)
    HOVER_RANGE  = 32
    SPEED        = 30.0
    WING_TYPE    = "other"


class AmazonGiantLocust(Insect):
    SPECIES      = "amazon_giant_locust"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "savanna"]
    W, H         = 14, 7
    BODY_COLOR   = (118, 138, 38)
    WING_COLOR   = (175, 195, 78)
    ACCENT_COLOR = (235, 215, 138)
    HOVER_RANGE  = 35
    SPEED        = 34.0
    WING_TYPE    = "other"


class BrazilianFireGrasshopper(Insect):
    SPECIES      = "brazilian_fire_grasshopper"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 12, 6
    BODY_COLOR   = (215, 78, 22)
    WING_COLOR   = (245, 138, 38)
    ACCENT_COLOR = (32, 22, 22)
    HOVER_RANGE  = 32
    SPEED        = 32.0
    WING_TYPE    = "other"


class TropicalLeafhopper(Insect):
    SPECIES      = "tropical_leafhopper"
    RARITY       = "common"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 7, 4
    BODY_COLOR   = (78, 138, 62)
    WING_COLOR   = (128, 215, 105)
    ACCENT_COLOR = (215, 245, 178)
    HOVER_RANGE  = 28
    SPEED        = 30.0
    WING_TYPE    = "other"


class RubyTreehopper(Insect):
    SPECIES      = "ruby_treehopper"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 7, 5
    BODY_COLOR   = (148, 28, 38)
    WING_COLOR   = (215, 62, 78)
    ACCENT_COLOR = (245, 178, 188)
    HOVER_RANGE  = 28
    SPEED        = 28.0
    WING_TYPE    = "other"


class AmazonStinkBug(Insect):
    SPECIES      = "amazon_stink_bug"
    RARITY       = "common"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 10, 7
    BODY_COLOR   = (62, 92, 62)
    WING_COLOR   = (105, 148, 105)
    ACCENT_COLOR = (175, 215, 148)
    HOVER_RANGE  = 30
    SPEED        = 24.0
    WING_TYPE    = "other"


class BrazilianCockroach(Insect):
    SPECIES      = "brazilian_cockroach"
    RARITY       = "common"
    BIOMES       = ["jungle", "swamp"]
    W, H         = 11, 6
    BODY_COLOR   = (105, 62, 28)
    WING_COLOR   = (148, 92, 42)
    ACCENT_COLOR = (215, 158, 88)
    HOVER_RANGE  = 28
    SPEED        = 36.0
    WING_TYPE    = "other"
    NIGHT_ONLY   = True


class AmazonShieldBug(Insect):
    SPECIES      = "amazon_shield_bug"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 10, 7
    BODY_COLOR   = (28, 88, 62)
    WING_COLOR   = (62, 148, 108)
    ACCENT_COLOR = (148, 235, 188)
    HOVER_RANGE  = 30
    SPEED        = 22.0
    WING_TYPE    = "other"


class PeanutHeadBug(Insect):
    SPECIES      = "peanut_head_bug"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 13, 7
    BODY_COLOR   = (108, 88, 62)
    WING_COLOR   = (175, 148, 105)
    ACCENT_COLOR = (235, 215, 158)
    HOVER_RANGE  = 35
    SPEED        = 24.0
    WING_TYPE    = "other"


class PeruvianMantis(Insect):
    SPECIES      = "peruvian_mantis"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "alpine_mountain"]
    W, H         = 13, 7
    BODY_COLOR   = (88, 108, 62)
    WING_COLOR   = (128, 158, 92)
    ACCENT_COLOR = (188, 215, 138)
    HOVER_RANGE  = 32
    SPEED        = 22.0
    WING_TYPE    = "other"


class AmazonGhostMantis(Insect):
    SPECIES      = "amazon_ghost_mantis"
    RARITY       = "rare"
    BIOMES       = ["jungle"]
    W, H         = 12, 7
    BODY_COLOR   = (108, 78, 55)
    WING_COLOR   = (158, 128, 92)
    ACCENT_COLOR = (215, 195, 158)
    HOVER_RANGE  = 32
    SPEED        = 20.0
    WING_TYPE    = "other"


class AmazonGiantWasp(Insect):
    SPECIES      = "amazon_giant_wasp"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 13, 6
    BODY_COLOR   = (38, 18, 12)
    WING_COLOR   = (108, 55, 22)
    ACCENT_COLOR = (235, 138, 38)
    HOVER_RANGE  = 55
    SPEED        = 40.0
    WING_TYPE    = "other"


class NeotropicalScorpionFly(Insect):
    SPECIES      = "neotropical_scorpion_fly"
    RARITY       = "uncommon"
    BIOMES       = ["jungle", "wetland"]
    W, H         = 11, 5
    BODY_COLOR   = (62, 42, 22)
    WING_COLOR   = (138, 108, 62)
    ACCENT_COLOR = (215, 188, 138)
    HOVER_RANGE  = 38
    SPEED        = 32.0
    WING_TYPE    = "other"


class AmazonDragonHeadKatydid(Insect):
    SPECIES      = "amazon_dragonhead_katydid"
    RARITY       = "rare"
    BIOMES       = ["jungle"]
    W, H         = 14, 8
    BODY_COLOR   = (78, 138, 62)
    WING_COLOR   = (128, 188, 92)
    ACCENT_COLOR = (215, 235, 138)
    HOVER_RANGE  = 35
    SPEED        = 24.0
    WING_TYPE    = "other"


class PeruvianCricket(Insect):
    SPECIES      = "peruvian_cricket"
    RARITY       = "common"
    BIOMES       = ["jungle", "alpine_mountain"]
    W, H         = 10, 6
    BODY_COLOR   = (62, 42, 22)
    WING_COLOR   = (105, 78, 45)
    ACCENT_COLOR = (158, 128, 78)
    HOVER_RANGE  = 28
    SPEED        = 26.0
    WING_TYPE    = "other"
    NIGHT_ONLY   = True


class PampasCricket(Insect):
    SPECIES      = "pampas_cricket"
    RARITY       = "common"
    BIOMES       = ["steppe", "savanna"]
    W, H         = 10, 6
    BODY_COLOR   = (118, 95, 62)
    WING_COLOR   = (158, 128, 88)
    ACCENT_COLOR = (215, 188, 138)
    HOVER_RANGE  = 28
    SPEED        = 26.0
    WING_TYPE    = "other"


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

ALL_INSECT_SPECIES = [
    # Butterflies
    Monarch, Swallowtail, BlueMorpho, PaintedLady, CabbageWhite,
    Birdwing, Skipper, Copper,
    DesertSwallowtail, ArizonaSkipper, CheckeredWhite, MarineBlue,
    RajahBrookesBirdwing, CommonTiger, GlassyTiger, RedHelen, JapaneseMapButterfly,
    DesertOrangeTip, SinaiBatonBlue, EasternFestoon, CleopatraButterfly,
    SaharanCloudedYellow, BathWhite, DesertDottedBlue, ArabianHairstreak,
    LevantChalcedony, AcaciaBlue, LargeTortoiseshell, AfricanMigrant,
    PurpleEmperor, ChalkHillBlue, SilverWashedFritillary, MarbledWhite,
    Grayling, OrangeTip, CommonBlue, HollyBlue, RedAdmiral, WhiteAdmiral,
    ScotchArgus, GreenHairstreak, DingySkipper, Brimstone,
    AfricanSwordtail, MalachiteButterfly, PostmanButterfly, EightyEight,
    BlueDiadem, GreatEggfly, TawnyCoaster, CommonMormon, ZebraLongwing,
    ArcticCloudedYellow, GreatSpangledFritillary, EasternTigerSwallowtail, OceanBlue, JungleSailor,
    # Beetles
    StagBeetle, Ladybug, JewelBeetle, DungBeetle, Longhorn,
    GroundBeetle, ClickBeetle,
    PaloVerdeBeetle, SonoranIroncladBeetle, DesertBlisterBeetle,
    SonoranDarkling, CactusLonghorn,
    AtlasBeetle, RainbowStagBeetle, AsianLonghornBeetle, TigerBeetle,
    SacredScarab, EgyptianFlowerChafer, ArabicDarkling, DesertRoveBeetle,
    NileBuprestid, SyrianCarabid, ArabianLonghornBeetle, DesertFogBeetle,
    RedPalmWeevil, BronzeChafer,
    VioletGroundBeetle, HarlequinLadybird, GoldenChafer, VioletOilBeetle,
    WaspBeetle, MuskBeetle, AlpineLonghorn, DorBeetle, SoldierBeetle, GreatDivingBeetle,
    GoliathBeetle, HerculesBeetle, RainbowWeevil, BombardierBeetle, GoldenTortoiseBeetle,
    TwoBandedLonghorn, TundraGroundBeetle, FungalBeetle, AustralianJewelBeetle, SpottedAsparagusBeetle,
    # Dragonflies
    EmperorDragonfly, AzureDamselfly, BroadBodiedChaser,
    ScarceChaser, BandedDemoiselle,
    DesertWhitetail, VarMeadowhawk,
    CrimsonMarshGlider, OrientalScarlet,
    NileBluetail, BlackTippedGroundling, DesertDarter,
    ArabianSkimmer, ArabianSprite, WanderingGlider,
    FourSpottedChaser, BlackDarter, GoldenRingedDragonfly,
    EuropeanBluetail, EmeraldDamselfly, CommonHawker,
    AfricanRiverDamsel, MalachiteDamselfly, TundraMosaic, MagpieHawker, ScarletDragonlet,
    # Fireflies
    CommonFirefly, BlueFirefly, GoldenFirefly,
    SyrianFirefly, LevantineFirefly, ItalianFirefly, AmericanFirefly,
    # Moths
    LunaMoth, AtlasMoth, HawkMoth, PepperedMoth,
    WhiteLinedSphinx, CactusMoth,
    ChineseMoonMoth, IndianMoonMoth, AsianEmperorMoth,
    OleanderHawkMoth, DeathsHeadHawkMoth, DesertHawkMoth,
    CottonLeafworm, FigMoth, ArabianSandMoth, PomegranateMoth, LebanonMoonMoth,
    CinnabarMoth, GardenTigerMoth, SixSpotBurnet, OakEggar, EmperorMoth,
    MerveilleduJour, PrivetHawkMoth, ElephantHawkMoth, LargeYellowUnderwing,
    IoMoth, CecrotiaMoth, PolyphemusMoth, HummingbirdHawkMoth, JerseyTigerMoth,
    WoodTiger, TussockMoth, TailedMoonMoth, VineMoth, SpotWingedGlassywing,
    # Other
    PrayingMantis, Honeybee, GiantHornet,
    TarantulaHawk, SonoranBumblebee, DesertCicada,
    VelvetAnt, AntLion, DesertLocust, GiantMesquiteBug,
    LanternFly, GiantWaterBug, ChineseMantis, BambooLocust,
    AsianGiantHornet, GiantStickInsect,
    ArabianMantis, FlowerMantis, EgyptianGrasshopper, SahariCricket,
    DesertKatydid, MudDauberWasp, ArabianBee, ArabianAssassinBug,
    FireBug, PalestineMoleCricket, ScorpionFly, DesertTermite,
    GlowWorm, EuropeanMantis, FieldGrasshopper, GreatGreenBushCricket,
    NewForestCicada, EuropeanHornet, BeeWolf, ForestBug,
    AlpineGrasshopper, WaterScorpion,
    IndianWalkingStick, GiantAfricanMantis, PrairieLocust, TundraBumblebee,
    CarpenterBee, JungleAssassinBug, GiantWeta, AfricanMoleCricket,
    ArcticBumblebee, TropicalMantis,
    # Night insects (batch 1)
    GhostMoth, CometMoth, VampireMoth, BogongMoth, UnderwingMoth,
    RailroadWorm, AsianFirefly,
    NocturnalGroundBeetle,
    CaveCricket, JungleCricket, MadagascarHissingCockroach, TropicalCockroach,
    # Night insects (batch 2)
    BlackWitchMoth, SaturnidMoth, SilkMoth, OwletMoth, DesertMoonMoth, AfricanMoonMoth,
    TropicalFirefly, MountainFirefly, CaveGlowworm,
    DarklingBeetle, OilBeetle, WoodBoringBeetle,
    NightCicada, JungleKatydid, Earwig, TundraCricket,
    WaterBoatman, NightMantis, GlowingMillipede, SandRoach,
    # Water insects
    PondSkater, WhirligigBeetle, MayflySilver, StoneflyRiver, CaddisflyGold,
    WaterMeasurer, MarshSpreadwing, RiverHawker, TealGlosskirt, PlumedMidge,
    BogSkimmer, MarshFirefly, WetlandGlowfly, RiverDivingBeetle, SwampRiflebeetle,
    WaterScavengerBeetle, ReedMarshMoth, BeachFoamMoth, ReedMaiden, BrookJewel,
    CraneFly, WaterGnat, SwampDragonlet, BluetailPondfly, MoonlitPondskipper,
    # Water insects (batch 2)
    GreatPondDamsel, CopperDemoiselle, BlacktipReedfly, SilverPondHawker, FenSkimmer,
    MudMinnowfly, WillowEmerald, WaterTreader, HoverCaddis, SwampLantern,
    PondshoreGlimmer, MarshCricket, WetlandKatydid, TidalFlatBeetle, SaltmarshWeevil,
    ReedBeetle, DuskReedmoth, FogMothlet, GoldenRushfly, CinnabarMarshfly,
    StoneflyMoss, VioletWaterfly, SpottedMayfly, MidnightMarshSkater, ElmPondButterfly,
    # Arctic
    ArcticFritillary, GlacierMoth, FrostMidge,
    # Asian butterflies
    PaperKite, CommonRose, CrimsonRose, BlueTigerButterfly, PlainTigerAsia,
    CommonJezebel, PeacockPansy, BandedPeacock, CommonNawab, RedLacewing,
    MalayLacewing, CommonMime, ChocolatePansy, GreatMormon, JapaneseEmperor,
    KaiserIHind, CommonCrow, ChestnutTiger, AsianCommaButterfly, YellowOrangeTip,
    StripedAlbatross, CommonGull, CommonSailor, BlueOakleaf, AutumnLeafButterfly,
    # Asian beetles
    JapaneseRhinocerosBeetle, GoldenStagBeetle, MiyamaStagBeetle, SaberhornLonghorn,
    AsiaticTigerBeetle, JapaneseRoseChafer, HimalayanLonghorn, ThaiJewelBeetle,
    BalinesePeacockBeetle, CelebesGoldenStag, SumatranLonghorn, JapaneseLadyBeetle,
    KoreanGroundBeetle, AsianFlowerChafer, RainbowMountainStag,
    # Asian dragonflies
    AsianEmperorDragonfly, ChineseRedDragonfly, JapaneseGoldenRing, YellowStripedHawker,
    RubyMeadowhawkAsia, PiedPaddyDragonfly, CrimsonDropwing, AsianClubtail,
    RiceFieldSkimmer, KoreanGreenSkimmer,
    # Asian fireflies
    GenjiFirefly, HeikeFirefly, TaiwaneseFirefly, KoreanFirefly, HimalayanFirefly,
    # Asian moths
    JapaneseSilkmoth, ChineseTussahMoth, JapaneseOakSilkmoth, MalayanMoonMoth,
    MalaccanMoonmoth, HimalayanGiantMoth, JadeHawkMoth, AsianBeeHawkmoth,
    BambooBorerMoth, TigerSwallowtailMoth, RubyTailedMoth, CrimsonTigerMoth,
    EmperorSilkmoth, CherryBlossomMoth, MountainSilkmoth,
    # Asian other
    JapaneseMantis, OrchidMantis, JadeMantis, BorneanLeafMantis, BambooMantis,
    JapaneseHornet, KoreanHornet, AsianPaperWasp, JapaneseHoneybee, AsianBlueCarpenterBee,
    AsianCarpenterAnt, WeaverAnt, AsianFireAnt, JapaneseGiantCicada, EveningCicada,
    AnnualCicada, JungleCicadaAsia, CherryBlossomCicada, RiceGrasshopper, JapaneseKatydid,
    BellCricket, PineCricket, BambooStickInsect, MalayanLeafInsect, BorneanStickInsect,
    HimalayanStickInsect, AsianAssassinBug, JapaneseShieldBug, JapaneseBumblebee, AsianHoneyWasp,
    # Asian fauna (batch 2)
    GoldenBirdwing, TreeNymph, CommonBluebottle, PaintedJezebel, CommonLeopardButterfly,
    RustyTippedPage, ChineseGoldenChafer, JapaneseTigerLonghorn, MalayanFireBeetle, AsianFlatHeadedBorer,
    JapaneseSkimmer, ChineseDarner, AsianBlueDamsel, SilverlinedHawkmoth, PinkUnderwingMoth,
    RoyalSilkmoth, SnowMoth, GiantAsianHoneybee, AsianTreeMantis, DeadLeafMantis,
    ChineseRiceLocust, PaddyKatydid, AsianTreeCricket, AsianLeafhopper, JadeWeevil,
    # NA butterflies
    MourningCloak, Viceroy, SpicebushSwallowtail, PipevineSwallowtail, AmericanLady,
    WoodlandSkipper, ZebraSwallowtail, GiantSwallowtail, PineWhite, CloudedSulphur,
    OrangeSulphur, PearlCrescent, AmericanCopper, EasternTailedBlue, SpringAzure,
    RegalFritillary, GulfFritillary, QuestionMarkButterfly, EasternComma, CommonBuckeye,
    RedSpottedPurple, AmericanSnout, HackberryEmperor, TawnyEmperor, FloridaLeafwing,
    # NA beetles
    EasternEyedClickBeetle, ColoradoPotatoBeetle, SixSpottedTigerBeetle, AmericanBuryingBeetle,
    GoldsmithBeetle, JuneBeetle, NorthernCornRootworm, AmericanCarrionBeetle,
    PennsylvaniaLeatherwing, BronzedCarabid, GiantStagBeetle, RedMilkweedBeetle,
    SpottedPineSawyer, BumbleFlowerBeetle, AmericanOakBorer,
    # NA dragonflies
    CommonGreenDarner, TwelveSpottedSkimmer, WidowSkimmer, EasternPondhawk, BlueDasher,
    AutumnMeadowhawk, EasternAmberwing, RoseateSkimmer, EbonyJewelwing, AmericanRubyspot,
    # NA fireflies
    BigDipperFirefly, SynchronousFirefly, PennsylvaniaFirefly, WinterFirefly, AppalachianBlueGhost,
    # NA moths
    CecropiaSilkmoth, PrometheaMoth, RegalMoth, ImperialMoth, RosyMapleMoth,
    WhiteFurcula, PandoraSphinx, AbbottsSphinx, BlindedSphinx, AchemonSphinx,
    UnderwingCatocala, GiantLeopardMoth, SaltMarshMoth, EightSpottedForester, TulipTreeBeauty,
    # NA other
    CarolinaMantis, BaldfacedHornet, AmericanYellowjacket, GreatBlackWasp, CicadaKiller,
    EasternCarpenterBee, ValleyCarpenterBee, SweatBee, LeafcutterBee, PeriodicalCicada,
    DogDayCicada, ScissorGrinderCicada, RockyMountainLocust, EasternLubberGrasshopper,
    DifferentialGrasshopper, AmericanGrasshopper, SnowyTreeCricket, JerusalemCricket,
    NorthernMoleCricket, AmericanWalkingstick, WheelBug, MaskedHunter, LargeMilkweedBug,
    SquashBug, BoxElderBug, WesternConiferSeedBug, AmericanCockroach, DobsonFly,
    AmericanMayfly, AmericanCaddisfly,
    # SA butterflies
    HelenaMorpho, CommonMorpho, AchillesMorpho, CramerMorpho, OwlButterfly,
    GiantOwlButterfly, GlasswingButterfly, CrackerButterfly, BlueCracker, JuliaHeliconian,
    ErythraeaHeliconian, ScarletPeacock, AmazonNymph, RuddyDaggerwing, SilverEmperorButterfly,
    PurpleSpottedSwallowtail, AmazonianSwallowtail, TropicalKiteSwallowtail, AmazonSulphur, CloudedMimic,
    RubyEyedBrushfoot, AndeanFritillary, PatagonianBlue, ScarletMormon, MarbledGlasswing,
    # SA beetles
    TitanBeetle, ElephantBeetle, HarlequinBeetle, JewelScarab, BrazilianJewelBeetle,
    AmazonianFireBeetle, AndeanWeevil, CaribbeanRhinoBeetle, AmazonStagBeetle, NeotropicalLonghorn,
    NeotropicalRhinoBeetle, AndeanTigerBeetle, AmazonianGoldChafer, HornedPassalusBeetle, AmazonianClickBeetle,
    # SA dragonflies
    AmazonHelicopterDamsel, NeotropicalGreatPondhawk, ScarletSkimmerSA, FieryRubyspot, NeotropicalGlider,
    AmazonianDarner, AndeanGreenSkimmer, PatagonianDarter, RustyClubtail, RainforestDamselfly,
    # SA fireflies
    AmazonianFirefly, AndeanFirefly, BrazilianRailroadGlow, AmazonGiantFirefly, TropicalNightfire,
    # SA moths
    WhiteWitchMoth, JaguarMoth, AmazonHawkMoth, RubyHawkMoth, PinkSpottedHawkmoth,
    AndeanSilkmoth, TropicalEmperorMoth, AmazonRoyalMoth, AmazonGiantSilkmoth, UraniaMoth,
    SunsetMoth, EcuadorianHawkMoth, SaturniidEclipseMoth, PatagonianTigerMoth, AmazonTussockMoth,
    # SA other
    JungleNymphMantis, BrazilianDeadLeafMantis, PeruvianStickInsect, AmazonLeafInsect, BulletAnt,
    LeafcutterAnt, ArmyAnt, AmazonFireAnt, NeotropicalAssassinBug, AmazonOrchidBee,
    EuglossineBee, AmazonStinglessBee, CitronellaAnt, AmazonGiantCockroach, PatagonianGrasshopper,
    AmazonGiantLocust, BrazilianFireGrasshopper, TropicalLeafhopper, RubyTreehopper, AmazonStinkBug,
    BrazilianCockroach, AmazonShieldBug, PeanutHeadBug, PeruvianMantis, AmazonGhostMantis,
    AmazonGiantWasp, NeotropicalScorpionFly, AmazonDragonHeadKatydid, PeruvianCricket, PampasCricket,
]

INSECT_SPECIES_BY_ID = {cls.SPECIES: cls for cls in ALL_INSECT_SPECIES}
