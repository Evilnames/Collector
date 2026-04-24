import random
import math
from constants import BLOCK_SIZE

SPOOK_SPEED_THRESHOLD = 0.8   # px/frame — player vx above this counts as moving
SPOOK_RADIUS_BLOCKS   = 3     # blocks (tighter than birds)


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
    WING_TYPE    = "butterfly"  # butterfly | moth | beetle | dragonfly | firefly | other

    def __init__(self, x, y, world):
        self.x        = float(x)
        self.y        = float(y)
        self._spawn_x = float(x)
        self._spawn_y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.world    = world
        self.spooked  = False

        self._hover_phase = random.uniform(0, math.pi * 2)
        self._drift_timer = random.uniform(1.0, 3.0)
        self._drift_tx    = float(x)
        self._drift_ty    = float(y)

    def spook(self):
        self.spooked = True
        self.vx = random.choice([-1, 1]) * self.SPEED * 3
        self.vy = -self.SPEED * 2

    def update(self, dt):
        self._hover_phase += dt * 4.0
        if self.spooked:
            self.x += self.vx * dt
            self.y += self.vy * dt
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
    SPECIES      = "blue_morpho"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 14, 10
    BODY_COLOR   = (20, 30, 20)
    WING_COLOR   = (40, 130, 255)
    ACCENT_COLOR = (80, 200, 255)
    WING_TYPE    = "butterfly"

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

class BlueFirefly(Insect):
    SPECIES      = "blue_firefly"
    RARITY       = "rare"
    BIOMES       = ["wetland"]
    W, H         = 7, 5
    BODY_COLOR   = (20, 25, 40)
    WING_COLOR   = (40, 50, 70)
    ACCENT_COLOR = (80, 160, 255)
    WING_TYPE    = "firefly"

class GoldenFirefly(Insect):
    SPECIES      = "golden_firefly"
    RARITY       = "rare"
    BIOMES       = ["wetland", "swamp"]
    W, H         = 8, 5
    BODY_COLOR   = (35, 30, 15)
    WING_COLOR   = (60, 52, 28)
    ACCENT_COLOR = (255, 220, 60)
    WING_TYPE    = "firefly"


# ---------------------------------------------------------------------------
# Moths (4)
# ---------------------------------------------------------------------------

class LunaMoth(Insect):
    SPECIES      = "luna_moth"
    RARITY       = "rare"
    BIOMES       = ["boreal", "birch_forest", "redwood"]
    W, H         = 15, 10
    BODY_COLOR   = (180, 230, 180)
    WING_COLOR   = (120, 210, 140)
    ACCENT_COLOR = (200, 245, 200)
    WING_TYPE    = "moth"

class AtlasMoth(Insect):
    SPECIES      = "atlas_moth"
    RARITY       = "rare"
    BIOMES       = ["jungle", "tropical"]
    W, H         = 16, 11
    BODY_COLOR   = (80, 45, 20)
    WING_COLOR   = (180, 110, 50)
    ACCENT_COLOR = (240, 200, 120)
    WING_TYPE    = "moth"

class HawkMoth(Insect):
    SPECIES      = "hawk_moth"
    RARITY       = "uncommon"
    BIOMES       = ["temperate", "rolling_hills", "savanna"]
    W, H         = 13, 8
    BODY_COLOR   = (70, 60, 40)
    WING_COLOR   = (120, 100, 65)
    ACCENT_COLOR = (180, 155, 95)
    WING_TYPE    = "moth"

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


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

ALL_INSECT_SPECIES = [
    # Butterflies
    Monarch, Swallowtail, BlueMorpho, PaintedLady, CabbageWhite,
    Birdwing, Skipper, Copper,
    DesertSwallowtail, ArizonaSkipper, CheckeredWhite, MarineBlue,
    RajahBrookesBirdwing, CommonTiger, GlassyTiger, RedHelen, JapaneseMapButterfly,
    # Beetles
    StagBeetle, Ladybug, JewelBeetle, DungBeetle, Longhorn,
    GroundBeetle, ClickBeetle,
    PaloVerdeBeetle, SonoranIroncladBeetle, DesertBlisterBeetle,
    SonoranDarkling, CactusLonghorn,
    AtlasBeetle, RainbowStagBeetle, AsianLonghornBeetle, TigerBeetle,
    # Dragonflies
    EmperorDragonfly, AzureDamselfly, BroadBodiedChaser,
    ScarceChaser, BandedDemoiselle,
    DesertWhitetail, VarMeadowhawk,
    CrimsonMarshGlider, OrientalScarlet,
    # Fireflies
    CommonFirefly, BlueFirefly, GoldenFirefly,
    # Moths
    LunaMoth, AtlasMoth, HawkMoth, PepperedMoth,
    WhiteLinedSphinx, CactusMoth,
    ChineseMoonMoth, IndianMoonMoth, AsianEmperorMoth,
    # Other
    PrayingMantis, Honeybee, GiantHornet,
    TarantulaHawk, SonoranBumblebee, DesertCicada,
    VelvetAnt, AntLion, DesertLocust, GiantMesquiteBug,
    LanternFly, GiantWaterBug, ChineseMantis, BambooLocust,
    AsianGiantHornet, GiantStickInsect,
]

INSECT_SPECIES_BY_ID = {cls.SPECIES: cls for cls in ALL_INSECT_SPECIES}
