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
    BIOMES       = ["desert", "canyon", "arid_steppe"]
    W, H         = 13, 9
    BODY_COLOR   = (25, 20, 10)
    WING_COLOR   = (230, 215, 70)
    ACCENT_COLOR = (30, 30, 30)
    WING_TYPE    = "butterfly"

class ArizonaSkipper(Insect):
    SPECIES      = "arizona_skipper"
    RARITY       = "common"
    BIOMES       = ["desert", "canyon", "arid_steppe"]
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
    BIOMES       = ["desert", "arid_steppe", "canyon"]
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
    BIOMES       = ["savanna", "desert", "canyon"]
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
    BIOMES       = ["desert", "canyon"]
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
    BIOMES       = ["desert", "canyon", "arid_steppe"]
    W, H         = 9, 6
    BODY_COLOR   = (20, 20, 20)
    WING_COLOR   = (30, 30, 30)
    ACCENT_COLOR = (50, 45, 40)
    WING_TYPE    = "beetle"

class CactusLonghorn(Insect):
    SPECIES      = "cactus_longhorn"
    RARITY       = "uncommon"
    BIOMES       = ["desert", "canyon"]
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
    BIOMES       = ["beach", "desert", "canyon"]
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
    BIOMES       = ["desert", "arid_steppe", "canyon"]
    W, H         = 9, 6
    BODY_COLOR   = (18, 18, 18)
    WING_COLOR   = (28, 28, 26)
    ACCENT_COLOR = (55, 50, 42)
    WING_TYPE    = "beetle"

class DesertRoveBeetle(Insect):
    SPECIES      = "desert_rove"
    RARITY       = "common"
    BIOMES       = ["desert", "canyon", "arid_steppe"]
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
    BIOMES       = ["desert", "canyon"]
    W, H         = 13, 6
    BODY_COLOR   = (200, 200, 205)
    WING_COLOR   = (220, 235, 255)
    ACCENT_COLOR = (150, 185, 230)
    HOVER_RANGE  = 55
    WING_TYPE    = "dragonfly"

class VarMeadowhawk(Insect):
    SPECIES      = "variegated_meadowhawk"
    RARITY       = "common"
    BIOMES       = ["desert", "arid_steppe", "canyon"]
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
    BIOMES       = ["desert", "arid_steppe", "canyon"]
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
    BIOMES       = ["desert", "arid_steppe", "canyon"]
    W, H         = 15, 9
    BODY_COLOR   = (70, 65, 40)
    WING_COLOR   = (100, 90, 55)
    ACCENT_COLOR = (210, 130, 150)
    SPEED        = 38.0
    WING_TYPE    = "moth"

class CactusMoth(Insect):
    SPECIES      = "cactus_moth"
    RARITY       = "common"
    BIOMES       = ["desert", "canyon"]
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
    WING_TYPE    = "other"

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
    BIOMES       = ["desert", "canyon"]
    W, H         = 12, 7
    BODY_COLOR   = (15, 15, 15)
    WING_COLOR   = (210, 100, 20)
    ACCENT_COLOR = (240, 140, 30)
    SPEED        = 36.0
    WING_TYPE    = "other"

class SonoranBumblebee(Insect):
    SPECIES      = "sonoran_bumblebee"
    RARITY       = "common"
    BIOMES       = ["desert", "arid_steppe", "canyon"]
    W, H         = 9, 7
    BODY_COLOR   = (25, 20, 10)
    WING_COLOR   = (210, 230, 245)
    ACCENT_COLOR = (225, 195, 35)
    WING_TYPE    = "other"

class DesertCicada(Insect):
    SPECIES      = "desert_cicada"
    RARITY       = "common"
    BIOMES       = ["desert", "canyon", "arid_steppe"]
    W, H         = 11, 7
    BODY_COLOR   = (80, 95, 60)
    WING_COLOR   = (160, 180, 140)
    ACCENT_COLOR = (110, 130, 85)
    WING_TYPE    = "other"

class VelvetAnt(Insect):
    SPECIES      = "velvet_ant"
    RARITY       = "uncommon"
    BIOMES       = ["desert", "canyon"]
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
    BIOMES       = ["desert", "arid_steppe", "steppe", "canyon"]
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
    BIOMES       = ["desert", "canyon"]
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
    BIOMES       = ["desert", "arid_steppe", "canyon"]
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
    WING_TYPE    = "other"

class ArabianAssassinBug(Insect):
    SPECIES      = "arabian_assassin_bug"
    RARITY       = "uncommon"
    BIOMES       = ["desert", "arid_steppe", "canyon"]
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
    WING_TYPE    = "other"

class CarpenterBee(Insect):
    SPECIES      = "carpenter_bee"
    RARITY       = "common"
    BIOMES       = ["tropical", "savanna", "jungle"]
    W, H         = 10, 7
    BODY_COLOR   = (18, 18, 28)
    WING_COLOR   = (175, 195, 225)
    ACCENT_COLOR = (55, 55, 100)
    WING_TYPE    = "other"

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
    WING_TYPE    = "other"

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
    BIOMES       = ["canyon", "rocky_mountain"]
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
    BIOMES       = ["canyon", "rocky_mountain"]
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
]

INSECT_SPECIES_BY_ID = {cls.SPECIES: cls for cls in ALL_INSECT_SPECIES}
