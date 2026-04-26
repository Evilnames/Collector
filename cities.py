import math
import random

from blocks import (STONE, BEDROCK, HOUSE_WALL, HOUSE_ROOF, AIR, LADDER,
                    TILLED_SOIL, WELL_BLOCK,
                    WHEAT_CROP_YOUNG, WHEAT_CROP_MATURE,
                    CARROT_CROP_YOUNG, CARROT_CROP_MATURE,
                    POTATO_CROP_YOUNG, POTATO_CROP_MATURE,
                    CABBAGE_CROP_YOUNG, CABBAGE_CROP_MATURE,
                    LEEK_CROP_YOUNG, LEEK_CROP_MATURE,
                    BEET_CROP_YOUNG, BEET_CROP_MATURE,
                    TURNIP_CROP_YOUNG, TURNIP_CROP_MATURE,
                    ONION_CROP_YOUNG, ONION_CROP_MATURE,
                    GARLIC_CROP_YOUNG, GARLIC_CROP_MATURE,
                    EGGPLANT_CROP_YOUNG, EGGPLANT_CROP_MATURE,
                    CHILI_CROP_YOUNG, CHILI_CROP_MATURE,
                    RICE_CROP_YOUNG, RICE_CROP_MATURE,
                    BOK_CHOY_CROP_YOUNG, BOK_CHOY_CROP_MATURE,
                    SWEET_POTATO_CROP_YOUNG, SWEET_POTATO_CROP_MATURE,
                    CELERY_CROP_YOUNG, CELERY_CROP_MATURE,
                    HOUSE_WALL_STONE, HOUSE_ROOF_STONE,
                    HOUSE_WALL_BRICK, HOUSE_ROOF_BRICK,
                    HOUSE_WALL_DARK,  HOUSE_ROOF_DARK,
                    RESTAURANT_WALL, RESTAURANT_AWNING,
                    SANDSTONE_BLOCK, POLISHED_MARBLE,
                    WHITEWASHED_WALL, MONASTERY_ROOF, MANI_STONE, PRAYER_FLAG_BLOCK,
                    WOOD_DOOR_CLOSED, WOOD_DOOR_OPEN, ALL_LOGS, ALL_LEAVES, BUSH_BLOCKS, SAPLING,
                    PINE_PLANK_WALL, SLATE_SHINGLE,
                    GRANITE_ASHLAR, ROUGH_STONE_WALL, ALPINE_PLASTER,
                    WHITE_PLASTER_WALL, ADOBE_BRICK, SPANISH_ROOF_TILE,
                    AFRICAN_MUD_BRICK, TERRACOTTA_ROOF_TILE,
                    COBBLESTONE, LIMESTONE_BLOCK,
                    FLOWER_BOX, GERANIUM_BOX, CARVED_SHUTTER, HANGING_BASKET,
                    WROUGHT_IRON_GRILLE, HAY_BALE, FIREWOOD_STACK,
                    TEXTILE_RUG_NATURAL, TEXTILE_RUG_GOLDEN, TEXTILE_RUG_CRIMSON,
                    TEXTILE_RUG_ROSE, TEXTILE_RUG_COBALT, TEXTILE_RUG_VIOLET,
                    TEXTILE_RUG_VERDANT, TEXTILE_RUG_AMBER, TEXTILE_RUG_IVORY,
                    TEXTILE_TAPESTRY_NATURAL, TEXTILE_TAPESTRY_GOLDEN,
                    TEXTILE_TAPESTRY_CRIMSON, TEXTILE_TAPESTRY_ROSE,
                    TEXTILE_TAPESTRY_COBALT, TEXTILE_TAPESTRY_VIOLET,
                    TEXTILE_TAPESTRY_VERDANT, TEXTILE_TAPESTRY_AMBER,
                    TEXTILE_TAPESTRY_IVORY,
                    LAVENDER_BED, ROSE_BED, TULIP_BED, COTTAGE_GARDEN_BED,
                    SUNFLOWER_BED, DAHLIA_BED, IRIS_BED, POPPY_BED,
                    MARIGOLD_BED, FOXGLOVE_PATCH, ALLIUM_PATCH, PEONY_BUSH,
                    HYDRANGEA_BUSH, RHODODENDRON_BUSH, FLOWERING_SHRUB,
                    HOLLY_SHRUB, BOXWOOD_BALL, FERN_CLUMP, BAMBOO_CLUMP,
                    TOPIARY_PEACOCK, TOPIARY_BEAR, TOPIARY_RABBIT,
                    TOPIARY_SWAN, TOPIARY_FOX, TOPIARY_HEDGEHOG,
                    TOPIARY_OWL, TOPIARY_SNAIL, TOPIARY_MUSHROOM,
                    TOPIARY_ARCH, ORNAMENTAL_GRASS, CHAMOMILE_LAWN,
                    CLOVER_LAWN, MOSS_PATCH, BARK_MULCH,
                    BIRD_TABLE, GARDEN_GNOME, BEE_SKEP, GARDEN_DOVECOTE,
                    GARDEN_WHEELBARROW, RAIN_BARREL, COMPOST_HEAP,
                    POTTING_TABLE, GARDEN_TOAD_HOUSE, STONE_FROG,
                    STONE_HEDGEHOG, GARDEN_CLOCK, GARDEN_OBELISK_METAL,
                    STONE_TROUGH_PLANTER, COLD_FRAME, TRELLIS_ARCH,
                    GARDEN_SWING, WICKER_FENCE, BUBBLE_FOUNTAIN,
                    SHELL_FOUNTAIN, MILLSTONE_FOUNTAIN, CHERUB_FOUNTAIN,
                    LION_HEAD_FOUNTAIN, MOSAIC_FOUNTAIN, KOI_POOL,
                    LILY_PAD_POND, KNOT_GARDEN, SWEET_PEA_TRELLIS,
                    WISTERIA_PILLAR, STANDARD_ROSE, AGAPANTHUS_PATCH,
                    BLEEDING_HEART_PATCH, ASTILBE_PATCH,
                    MARBLE_STATUE, MARBLE_PLINTH, GARDEN_OBELISK,
                    GARDEN_COLUMN, GARDEN_LANTERN, MARBLE_BIRDBATH,
                    GARDEN_TABLE, GARDEN_ROCK, HERRINGBONE_GARDEN,
                    INLAID_MARBLE, MARBLE_MEDALLION_REN, GARDEN_STAR_TILE,
                    HERMES_STELE, VICTORY_STELE, GREEK_STONE_BENCH,
                    DORIC_CAPITAL, TRIPOD_BRAZIER, VOTIVE_TABLET,
                    SYMPOSIUM_TABLE, LAUREL_WREATH_MOUNT, BRAZIER,
                    CARVED_BENCH, STONE_BASIN, WALL_SCONCE, STAR_LAMP,
                    TORCH, ARCH_STONE, GARDEN_GATE, LOW_GARDEN_WALL,
                    LANTERN_ORB, CHANDELIER, CANDELABRA, OLIVE_BRANCH,
                    PHILOSOPHERS_SCROLL, GREEK_THEATRE_MASK,
                    ROUND_TOWER_WALL, CURTAIN_WALL, GREAT_HALL_FLOOR,
                    CRENELLATION, HERALDIC_PANEL, CASTLE_FIREPLACE,
                    MACHICOLATION, PORTCULLIS_BLOCK, DRAWBRIDGE_CHAIN,
                    DRAWBRIDGE_PLANK, CASTLE_GATE_ARCH, WALL_WALK_FLOOR,
                    DUNGEON_WALL, DUNGEON_GRATE, MOAT_STONE,
                    MURDER_HOLE, CORBEL_COURSE, TOWER_CAP,
                    GARDEROBE_CHUTE, CHAPEL_STONE, GOTHIC_TRACERY,
                    ROSE_WINDOW, LANCET_WINDOW, GARGOYLE_BLOCK,
                    PALACE_FLOOR_TILE, PALACE_PORTAL, PALAZZO_BALCONY,
                    IRON_DOOR_CLOSED, BRONZE_SHIELD_MOUNT,
                    TOWN_FLAG_BLOCK, STAIRS_RIGHT, STAIRS_LEFT,
                    PAGODA_EAVE, TORII_PANEL, TATAMI_PAVING, JAPANESE_SHOJI,
                    PINE_TOPIARY_JP, JAPANESE_MAPLE, SHISHI_ODOSHI, RED_ARCH_BRIDGE,
                    ROMAN_MOSAIC, ROMAN_ARCH_REN,
                    GREEK_KEY, GREEK_AMPHORA,
                    MUGHAL_ARCH, MUGHAL_JALI,
                    ANDALUSIAN_FOUNTAIN, PORTUGUESE_BENCH,
                    SPANISH_PATIO_FLOOR, MUDEJAR_STAR_TILE, MUDEJAR_BRICK)
from constants import (BLOCK_SIZE, PLAYER_W, PLAYER_H, CITY_SPACING, CITY_COUNT,
                       NPC_INTERACT_RANGE, CHUNK_W, GRAVITY, MAX_FALL, SURFACE_Y)
from rocks import ROCK_TYPES


RARITY_ORDER  = ["common", "uncommon", "rare", "epic", "legendary"]
RARITY_REWARD = {
    "common":    5,
    "uncommon":  12,
    "rare":      25,
    "epic":      60,
    "legendary": 150,
}

QUEST_SPECIALS = ["luminous", "magnetic", "crystalline", "resonant", "voidtouched"]
SPECIAL_REWARD = {
    "luminous":    20,
    "magnetic":    18,
    "crystalline": 25,
    "resonant":    32,
    "voidtouched": 50,
}

DIFFICULTY_RARITY = {
    0: ["common", "uncommon"],
    1: ["common", "uncommon", "rare"],
    2: ["uncommon", "rare", "epic", "legendary"],
}

DIFFICULTY_KINDS = {
    0: ["single", "single", "single", "quantity"],
    1: ["single", "single", "any_rarity", "quantity"],
    2: ["single", "any_rarity", "quantity", "special"],
}

TRADE_TABLE = [
    ("lumber",        5,  3),
    ("iron_chunk",    3,  4),
    ("coal",          8,  3),
    ("gold_nugget",   1,  8),
    ("wool",          3,  5),
    ("crystal_shard", 1, 15),
    ("ruby",          1, 25),
    ("stone_chip",   10,  2),
    ("obsidian_slab", 1, 20),
    ("dirt_clump",   15,  1),
    ("milk",          2,  4),
]

# ---------------------------------------------------------------------------
# Wildflower quest data
# ---------------------------------------------------------------------------

_WF_RARITY_REWARD = {
    "common":    6,
    "uncommon":  15,
    "rare":      35,
    "epic":      80,
    "legendary": 200,
}

_WF_QUEST_POOL = {
    0: ["daisy", "buttercup", "clover", "poppy", "lavender", "chamomile", "forget_me_not"],
    1: ["lupine", "foxglove", "iris", "orchid", "sunflower", "bleeding_heart", "sweet_pea", "snapdragon"],
    2: ["edelweiss", "ghost_orchid", "crystal_bloom", "void_petal", "phantom_bloom", "biolume_bell"],
}

_WF_KINDS_BY_DIFF = {
    0: ["wf_single", "wf_single", "wf_quantity"],
    1: ["wf_single", "wf_rarity", "wf_quantity"],
    2: ["wf_rarity", "wf_rarity", "wf_quantity"],
}


def _build_wf_quest(rng, difficulty):
    kind = rng.choice(_WF_KINDS_BY_DIFF[difficulty])
    allowed = DIFFICULTY_RARITY[difficulty]

    if kind == "wf_single":
        flower_type = rng.choice(_WF_QUEST_POOL[difficulty])
        reward = int(_WF_RARITY_REWARD["common"] * (1 + difficulty))
        return {"kind": "wf_single", "flower_type": flower_type, "reward": reward}

    elif kind == "wf_quantity":
        pool = _WF_QUEST_POOL[min(difficulty, 1)]
        flower_type = rng.choice(pool)
        count = rng.randint(2, 3)
        reward = int(_WF_RARITY_REWARD["common"] * count * (1 + difficulty * 0.5))
        return {"kind": "wf_quantity", "flower_type": flower_type, "count": count, "reward": reward}

    else:  # wf_rarity
        upper = allowed[max(0, len(allowed) // 2):]
        min_rarity = rng.choice(upper)
        reward = int(_WF_RARITY_REWARD[min_rarity] * 1.4)
        return {"kind": "wf_rarity", "min_rarity": min_rarity, "reward": reward}


def wf_quest_display(quest):
    if quest["kind"] == "wf_single":
        return quest["flower_type"].replace("_", " ").title()
    elif quest["kind"] == "wf_quantity":
        return f"{quest['count']}x {quest['flower_type'].replace('_', ' ').title()}"
    elif quest["kind"] == "wf_rarity":
        from UI import RARITY_LABEL
        label = RARITY_LABEL.get(quest["min_rarity"], quest["min_rarity"])
        return f"Any {label}+ wildflower"
    return "Unknown quest"


def wf_quest_hint(quest):
    if quest["kind"] == "wf_single":
        return "Found at the surface in various biomes"
    elif quest["kind"] == "wf_quantity":
        return "Any rarity accepted"
    elif quest["kind"] == "wf_rarity":
        idx = RARITY_ORDER.index(quest["min_rarity"])
        above = " / ".join(r.title() for r in RARITY_ORDER[idx:])
        return f"Accepted: {above}"
    return ""


# ---------------------------------------------------------------------------
# Gem quest data
# ---------------------------------------------------------------------------

_GEM_RARITY_REWARD = {
    "common":    10,
    "uncommon":  25,
    "rare":      60,
    "epic":      140,
    "legendary": 350,
}

_GEM_QUEST_POOL = {
    0: ["amber", "garnet", "rose_quartz", "jet"],
    1: ["spinel", "peridot", "tourmaline", "obsidian"],
    2: ["alexandrite", "emerald", "ruby", "sapphire", "diamond"],
}

_GEM_KINDS_BY_DIFF = {
    0: ["gem_type", "gem_type", "gem_rarity"],
    1: ["gem_type", "gem_rarity", "gem_cut"],
    2: ["gem_rarity", "gem_cut", "gem_cut"],
}


def _build_gem_quest(rng, difficulty):
    kind = rng.choice(_GEM_KINDS_BY_DIFF[difficulty])
    allowed = DIFFICULTY_RARITY[difficulty]

    if kind == "gem_type":
        gem_type = rng.choice(_GEM_QUEST_POOL[difficulty])
        reward = int(_GEM_RARITY_REWARD["common"] * (1 + difficulty * 0.8))
        return {"kind": "gem_type", "gem_type": gem_type, "reward": reward}

    elif kind == "gem_cut":
        gem_type = rng.choice(_GEM_QUEST_POOL[min(difficulty, 1)])
        reward = int(_GEM_RARITY_REWARD["uncommon"] * (1 + difficulty * 0.6))
        return {"kind": "gem_cut", "gem_type": gem_type, "reward": reward}

    else:  # gem_rarity
        upper = allowed[max(0, len(allowed) // 2):]
        min_rarity = rng.choice(upper)
        reward = int(_GEM_RARITY_REWARD[min_rarity] * 1.3)
        return {"kind": "gem_rarity", "min_rarity": min_rarity, "reward": reward}


def gem_quest_display(quest):
    if quest["kind"] == "gem_type":
        return f"Any {quest['gem_type'].replace('_', ' ').title()}"
    elif quest["kind"] == "gem_cut":
        return f"Cut {quest['gem_type'].replace('_', ' ').title()}"
    elif quest["kind"] == "gem_rarity":
        from UI import RARITY_LABEL
        label = RARITY_LABEL.get(quest["min_rarity"], quest["min_rarity"])
        return f"Any {label}+ gemstone"
    return "Unknown quest"


def gem_quest_hint(quest):
    if quest["kind"] == "gem_type":
        return "Any rarity, rough or cut accepted"
    elif quest["kind"] == "gem_cut":
        return "Must be cut (use the Gem Cutter)"
    elif quest["kind"] == "gem_rarity":
        idx = RARITY_ORDER.index(quest["min_rarity"])
        above = " / ".join(r.title() for r in RARITY_ORDER[idx:])
        return f"Accepted: {above}"
    return ""


# ---------------------------------------------------------------------------
# Rock quest helpers (unchanged)
# ---------------------------------------------------------------------------

def _quest_candidates(rng, difficulty):
    allowed = set(DIFFICULTY_RARITY[difficulty])
    max_depth = 40 + difficulty * 50
    candidates = [
        k for k, v in ROCK_TYPES.items()
        if v["min_depth"] <= max_depth and any(r in allowed for r in v["rarity_pool"])
    ]
    return candidates if candidates else list(ROCK_TYPES.keys())


def _build_quest(rng, difficulty):
    kind = rng.choice(DIFFICULTY_KINDS[difficulty])
    allowed = DIFFICULTY_RARITY[difficulty]

    if kind == "single":
        candidates = _quest_candidates(rng, difficulty)
        rock_type = rng.choice(candidates)
        pool = [r for r in ROCK_TYPES[rock_type]["rarity_pool"] if r in allowed]
        rarity = rng.choice(pool) if pool else rng.choice(allowed)
        base_reward = RARITY_REWARD[rarity]
        reward = int(base_reward * (1 + difficulty * 0.3))
        return {"kind": "single", "rock_type": rock_type, "rarity": rarity, "reward": reward}

    elif kind == "any_rarity":
        upper = allowed[max(0, len(allowed) // 2):]
        min_rarity = rng.choice(upper)
        reward = int(RARITY_REWARD[min_rarity] * 1.5)
        return {"kind": "any_rarity", "min_rarity": min_rarity, "reward": reward}

    elif kind == "quantity":
        count = 2 if difficulty == 0 else rng.randint(2, 3)
        candidates = _quest_candidates(rng, difficulty)
        rock_type = rng.choice(candidates)
        reward = int(RARITY_REWARD["common"] * count * (1 + difficulty * 0.5))
        return {"kind": "quantity", "rock_type": rock_type, "count": count, "reward": reward}

    else:  # special
        special = rng.choice(QUEST_SPECIALS)
        reward = int(SPECIAL_REWARD[special] * (1 + difficulty * 0.4))
        return {"kind": "special", "special": special, "reward": reward}


_PRESTIGE_SPECIALS = ["resonant", "voidtouched"]


def _build_prestige_rock_quest(rng, difficulty):
    if difficulty == 0:
        upper = ["rare", "epic"]
        min_rarity = rng.choice(upper)
        reward = int(RARITY_REWARD[min_rarity] * 2.5)
        return {"kind": "any_rarity", "min_rarity": min_rarity, "reward": reward, "min_rep": 150}
    elif difficulty == 1:
        special = rng.choice(_PRESTIGE_SPECIALS)
        reward = int(SPECIAL_REWARD[special] * 3.5)
        return {"kind": "special", "special": special, "reward": reward, "min_rep": 250}
    else:
        candidates = [k for k, v in ROCK_TYPES.items() if "legendary" in v.get("rarity_pool", [])]
        rock_type = rng.choice(candidates) if candidates else rng.choice(list(ROCK_TYPES.keys()))
        reward = int(RARITY_REWARD["legendary"] * 4.0)
        return {"kind": "single", "rock_type": rock_type, "rarity": "legendary", "reward": reward, "min_rep": 400}


def _build_prestige_wf_quest(rng, difficulty):
    if difficulty == 0:
        min_rarity = "rare"
        reward = int(_WF_RARITY_REWARD[min_rarity] * 2.5)
        return {"kind": "wf_rarity", "min_rarity": min_rarity, "reward": reward, "min_rep": 150}
    elif difficulty == 1:
        min_rarity = "epic"
        reward = int(_WF_RARITY_REWARD[min_rarity] * 3.0)
        return {"kind": "wf_rarity", "min_rarity": min_rarity, "reward": reward, "min_rep": 250}
    else:
        flower_type = rng.choice(_WF_QUEST_POOL[2])
        reward = int(_WF_RARITY_REWARD["legendary"] * 4.0)
        return {"kind": "wf_single", "flower_type": flower_type, "reward": reward, "min_rep": 400}


def _build_prestige_gem_quest(rng, difficulty):
    if difficulty == 0:
        gem_type = rng.choice(_GEM_QUEST_POOL[0])
        reward = int(_GEM_RARITY_REWARD["uncommon"] * 2.5)
        return {"kind": "gem_cut", "gem_type": gem_type, "reward": reward, "min_rep": 150}
    elif difficulty == 1:
        upper = ["rare", "epic"]
        min_rarity = rng.choice(upper)
        reward = int(_GEM_RARITY_REWARD[min_rarity] * 3.0)
        return {"kind": "gem_rarity", "min_rarity": min_rarity, "reward": reward, "min_rep": 250}
    else:
        reward = int(_GEM_RARITY_REWARD["legendary"] * 3.5)
        return {"kind": "gem_rarity", "min_rarity": "legendary", "reward": reward, "min_rep": 400}


def quest_display(quest):
    if quest["kind"] == "single":
        from UI import RARITY_LABEL
        label = RARITY_LABEL.get(quest["rarity"], quest["rarity"])
        return f"{label} {quest['rock_type'].replace('_', ' ').title()}"
    elif quest["kind"] == "any_rarity":
        from UI import RARITY_LABEL
        label = RARITY_LABEL.get(quest["min_rarity"], quest["min_rarity"])
        return f"Any {label}+ rock"
    elif quest["kind"] == "quantity":
        return f"{quest['count']}x {quest['rock_type'].replace('_', ' ').title()} (any rarity)"
    elif quest["kind"] == "special":
        return f"Any {quest['special'].title()} rock"
    return "Unknown quest"


def quest_hint(quest):
    if quest["kind"] == "single":
        depth = ROCK_TYPES[quest["rock_type"]]["min_depth"]
        return f"Found from depth {depth} m"
    elif quest["kind"] == "any_rarity":
        idx = RARITY_ORDER.index(quest["min_rarity"])
        above = " / ".join(r.title() for r in RARITY_ORDER[idx:])
        return f"Accepted: {above}"
    elif quest["kind"] == "quantity":
        depth = ROCK_TYPES[quest["rock_type"]]["min_depth"]
        return f"Found from depth {depth} m"
    elif quest["kind"] == "special":
        return "Special properties appear randomly on any rock"
    return ""


# ---------------------------------------------------------------------------
# NPC base class
# ---------------------------------------------------------------------------

class NPC:
    NPC_W = 20
    NPC_H = 28

    def __init__(self, x, y, world, npc_id):
        self.x = float(x)
        self.y = float(y)
        self.vy = 0.0
        self.on_ground = False
        self.world = world
        self.animal_id = npc_id
        self._bob_timer = 0.0
        self._bob_offset = 0.0

    @property
    def rect(self):
        import pygame
        return pygame.Rect(int(self.x), int(self.y), self.NPC_W, self.NPC_H)

    def _collides(self):
        left  = int(self.x // BLOCK_SIZE)
        right = int((self.x + self.NPC_W - 1) // BLOCK_SIZE)
        top   = int(self.y // BLOCK_SIZE)
        bot   = int((self.y + self.NPC_H - 1) // BLOCK_SIZE)
        for bx in range(left, right + 1):
            for by in range(top, bot + 1):
                if self.world.is_solid(bx, by):
                    return True
        return False

    def update(self, dt):
        # Stationary NPCs respect gravity — they fall until they hit the ground
        # so they never end up floating after the building under them is removed.
        self.vy = min(self.vy + GRAVITY, MAX_FALL)
        self.y += self.vy
        if self._collides():
            self.y -= self.vy
            self.vy = 0.0
            self.on_ground = True
        else:
            self.on_ground = False

    def reset_harvest(self):
        pass

    def try_harvest(self, player, dt):
        return None

    def in_range(self, player):
        px = (player.x + PLAYER_W / 2) / BLOCK_SIZE
        py = (player.y + PLAYER_H / 2) / BLOCK_SIZE
        ex = (self.x + self.NPC_W / 2) / BLOCK_SIZE
        ey = (self.y + self.NPC_H / 2) / BLOCK_SIZE
        return ((px - ex) ** 2 + (py - ey) ** 2) ** 0.5 <= NPC_INTERACT_RANGE

    def _town_rep(self):
        from towns import TOWNS
        centers = getattr(self.world, "town_centers", [])
        if not centers:
            return 0
        town_id = min(range(len(centers)), key=lambda i: abs(centers[i] - round(self.x / BLOCK_SIZE)))
        return TOWNS[town_id].reputation if town_id in TOWNS else 0


# ---------------------------------------------------------------------------
# Ambient NPCs — non-interactive residents that walk and go home at night
# ---------------------------------------------------------------------------

class AmbientNPC(NPC):
    """Base class for city residents: farmers, villagers, children, guards.

    Walks a patrol range around patrol_cx, pauses occasionally, reverses at
    the edges.  is_ambient=True tells main.py to skip the E-key panel.
    """
    is_ambient = True

    def __init__(self, x, y, world, npc_id, patrol_half=48, biodome="temperate"):
        super().__init__(x, y, world, npc_id)
        self.patrol_cx   = float(x)
        self.patrol_half = float(patrol_half)
        self.facing      = 1       # 1 = right, -1 = left
        self._walk_speed = 28.0    # px/sec
        self._pause_max  = 3.5     # max idle seconds
        self._state      = "walk"
        self._state_timer = random.uniform(1.0, 4.0)
        style = _CLOTHING_STYLE_BY_BIODOME.get(biodome, "temperate")
        self.clothing = _CLOTHING_PALETTES.get(style, _CLOTHING_DEFAULT)
        # Ensure spawn is not inside solid terrain
        self._snap_to_surface()

    def _snap_to_surface(self):
        """Eject upward block-by-block until the NPC is no longer inside terrain."""
        for _ in range(60):
            if not self._collides():
                break
            self.y -= BLOCK_SIZE

    def update(self, dt):
        # Gravity
        self.vy = min(self.vy + GRAVITY, MAX_FALL)
        self.y += self.vy
        if self._collides():
            self.y -= self.vy
            self.vy = 0.0
            self.on_ground = True
        else:
            self.on_ground = False

        # Bob animation
        self._bob_timer += dt
        self._bob_offset = math.sin(self._bob_timer * 2.2) * 1.5

        # Walk / pause state machine
        self._state_timer -= dt
        if self._state == "pause":
            if self._state_timer <= 0:
                self._state = "walk"
                self._state_timer = random.uniform(2.0, 6.0)
        else:
            if self._walk_speed > 0:
                old_x = self.x
                self.x += self._walk_speed * dt * self.facing
                lo = self.patrol_cx - self.patrol_half
                hi = self.patrol_cx + self.patrol_half - self.NPC_W
                if self.x <= lo or self.x >= hi:
                    # Hit patrol boundary — clamp and turn around
                    self.x = max(lo, min(hi, self.x))
                    self.facing *= -1
                elif self._collides():
                    # Hit a wall — revert and turn around
                    self.x = old_x
                    self.facing *= -1
            if self._state_timer <= 0:
                self._state = "pause"
                self._state_timer = random.uniform(1.0, self._pause_max)


class FarmerNPC(AmbientNPC):
    def __init__(self, x, y, world, patrol_half=56, biodome="temperate"):
        super().__init__(x, y, world, "npc_farmer", patrol_half, biodome)
        self._walk_speed = 22.0
        self._pause_max  = 5.0   # lingers near crops

    def update(self, dt):
        from world import DAY_DURATION
        tod = getattr(self.world, 'time_of_day', 0.0)
        if tod >= DAY_DURATION:
            self._walk_speed = 0.0
            dx = self.patrol_cx - self.x
            if abs(dx) > 4:
                self.x += dx * min(1.0, dt * 2.0)
        else:
            self._walk_speed = 22.0
        super().update(dt)


class VillagerNPC(AmbientNPC):
    def __init__(self, x, y, world, patrol_half=60, biodome="temperate"):
        super().__init__(x, y, world, "npc_villager", patrol_half, biodome)

    def update(self, dt):
        from world import DAY_DURATION
        tod = getattr(self.world, 'time_of_day', 0.0)
        if tod >= DAY_DURATION:
            self._walk_speed = 0.0
            dx = self.patrol_cx - self.x
            if abs(dx) > 4:
                self.x += dx * min(1.0, dt * 2.0)
        else:
            self._walk_speed = 28.0
        super().update(dt)


class ChildNPC(AmbientNPC):
    NPC_W = 14
    NPC_H = 20

    def __init__(self, x, y, world, patrol_half=80, biodome="temperate"):
        super().__init__(x, y, world, "npc_child", patrol_half, biodome)
        self._walk_speed = 48.0
        self._pause_max  = 1.5


class GuardNPC(AmbientNPC):
    def __init__(self, x, y, world, patrol_half=40, biodome="temperate"):
        super().__init__(x, y, world, "npc_guard", patrol_half, biodome)
        self._walk_speed = 20.0
        self._pause_max  = 2.0


# ---------------------------------------------------------------------------
# NPC types
# ---------------------------------------------------------------------------

class RockQuestNPC(NPC):
    def __init__(self, x, y, world, rng, difficulty=0, biodome="temperate"):
        super().__init__(x, y, world, "npc_quest")
        self.clothing = _npc_clothing(biodome)
        self._rng = rng
        self.difficulty = difficulty
        self._streak = 0
        self.quests = [_build_quest(rng, difficulty), _build_prestige_rock_quest(rng, difficulty)]

    def find_matching_rocks(self, player, quest):
        if quest["kind"] == "single":
            return [i for i, r in enumerate(player.rocks)
                    if r.base_type == quest["rock_type"] and r.rarity == quest["rarity"]]
        elif quest["kind"] == "any_rarity":
            min_idx = RARITY_ORDER.index(quest["min_rarity"])
            return [i for i, r in enumerate(player.rocks)
                    if RARITY_ORDER.index(r.rarity) >= min_idx]
        elif quest["kind"] == "quantity":
            return [i for i, r in enumerate(player.rocks)
                    if r.base_type == quest["rock_type"]]
        elif quest["kind"] == "special":
            return [i for i, r in enumerate(player.rocks)
                    if quest["special"] in r.specials]
        return []

    def can_complete(self, player, quest_idx):
        quest = self.quests[quest_idx]
        if self._town_rep() < quest.get("min_rep", 0):
            return False
        needed = quest.get("count", 1)
        return len(self.find_matching_rocks(player, quest)) >= needed

    def complete_quest(self, player, quest_idx=0):
        quest = self.quests[quest_idx]
        needed = quest.get("count", 1)
        matching = self.find_matching_rocks(player, quest)
        if len(matching) < needed or self._town_rep() < quest.get("min_rep", 0):
            return False
        for i in sorted(matching[:needed], reverse=True):
            player.rocks.pop(i)
        self._streak += 1
        streak_mult = 1.0 + min(self._streak - 1, 2) * 0.25
        player.money += int(quest["reward"] * streak_mult * getattr(player, "blessing_mult", 1.0))
        builder = _build_prestige_rock_quest if quest_idx == 1 else _build_quest
        self.quests[quest_idx] = builder(self._rng, self.difficulty)
        return True


class TradeNPC(NPC):
    def __init__(self, x, y, world, rng, biodome="temperate"):
        super().__init__(x, y, world, "npc_trade")
        self.clothing = _npc_clothing(biodome)
        n = rng.randint(3, 4)
        self.trades = rng.sample(TRADE_TABLE, n)

    def boosted_gold(self, trade_idx):
        _, _, receive_gold = self.trades[trade_idx]
        return max(1, round(receive_gold * _rep_buy_bonus(self._town_rep())))

    def rep_bonus_pct(self):
        return round((_rep_buy_bonus(self._town_rep()) - 1.0) * 100)

    def can_trade(self, trade_idx, player):
        item_id, give_count, _ = self.trades[trade_idx]
        return player.inventory.get(item_id, 0) >= give_count

    def execute_trade(self, trade_idx, player):
        if not self.can_trade(trade_idx, player):
            return False
        item_id, give_count, _ = self.trades[trade_idx]
        player.inventory[item_id] -= give_count
        if player.inventory[item_id] <= 0:
            del player.inventory[item_id]
            for i in range(len(player.hotbar)):
                if player.hotbar[i] == item_id:
                    player.hotbar[i] = None
        player.money += self.boosted_gold(trade_idx)
        return True


class WildflowerQuestNPC(NPC):
    def __init__(self, x, y, world, rng, difficulty=0, biodome="temperate"):
        super().__init__(x, y, world, "npc_herbalist")
        self.clothing = _npc_clothing(biodome)
        self._rng = rng
        self.difficulty = difficulty
        self._streak = 0
        self.quests = [_build_wf_quest(rng, difficulty), _build_prestige_wf_quest(rng, difficulty)]

    def find_matching_flowers(self, player, quest):
        if quest["kind"] == "wf_single":
            return [i for i, f in enumerate(player.wildflowers)
                    if f.flower_type == quest["flower_type"]]
        elif quest["kind"] == "wf_quantity":
            return [i for i, f in enumerate(player.wildflowers)
                    if f.flower_type == quest["flower_type"]]
        elif quest["kind"] == "wf_rarity":
            min_idx = RARITY_ORDER.index(quest["min_rarity"])
            return [i for i, f in enumerate(player.wildflowers)
                    if RARITY_ORDER.index(f.rarity) >= min_idx]
        return []

    def can_complete(self, player, quest_idx):
        quest = self.quests[quest_idx]
        if self._town_rep() < quest.get("min_rep", 0):
            return False
        needed = quest.get("count", 1)
        return len(self.find_matching_flowers(player, quest)) >= needed

    def complete_quest(self, player, quest_idx=0):
        quest = self.quests[quest_idx]
        needed = quest.get("count", 1)
        matching = self.find_matching_flowers(player, quest)
        if len(matching) < needed or self._town_rep() < quest.get("min_rep", 0):
            return False
        for i in sorted(matching[:needed], reverse=True):
            player.wildflowers.pop(i)
        self._streak += 1
        streak_mult = 1.0 + min(self._streak - 1, 2) * 0.25
        player.money += int(quest["reward"] * streak_mult * getattr(player, "blessing_mult", 1.0))
        builder = _build_prestige_wf_quest if quest_idx == 1 else _build_wf_quest
        self.quests[quest_idx] = builder(self._rng, self.difficulty)
        return True


class GemQuestNPC(NPC):
    def __init__(self, x, y, world, rng, difficulty=0, biodome="temperate"):
        super().__init__(x, y, world, "npc_jeweler")
        self.clothing = _npc_clothing(biodome)
        self._rng = rng
        self.difficulty = difficulty
        self._streak = 0
        self.quests = [_build_gem_quest(rng, difficulty), _build_prestige_gem_quest(rng, difficulty)]

    def find_matching_gems(self, player, quest):
        gems = getattr(player, "gems", [])
        if quest["kind"] == "gem_type":
            return [i for i, g in enumerate(gems)
                    if g.gem_type == quest["gem_type"]]
        elif quest["kind"] == "gem_cut":
            return [i for i, g in enumerate(gems)
                    if g.gem_type == quest["gem_type"] and g.state == "cut"]
        elif quest["kind"] == "gem_rarity":
            min_idx = RARITY_ORDER.index(quest["min_rarity"])
            return [i for i, g in enumerate(gems)
                    if RARITY_ORDER.index(g.rarity) >= min_idx]
        return []

    def can_complete(self, player, quest_idx):
        quest = self.quests[quest_idx]
        if self._town_rep() < quest.get("min_rep", 0):
            return False
        needed = quest.get("count", 1)
        return len(self.find_matching_gems(player, quest)) >= needed

    def complete_quest(self, player, quest_idx=0):
        quest = self.quests[quest_idx]
        needed = quest.get("count", 1)
        matching = self.find_matching_gems(player, quest)
        if len(matching) < needed or self._town_rep() < quest.get("min_rep", 0):
            return False
        for i in sorted(matching[:needed], reverse=True):
            player.gems.pop(i)
        self._streak += 1
        streak_mult = 1.0 + min(self._streak - 1, 2) * 0.25
        player.money += int(quest["reward"] * streak_mult * getattr(player, "blessing_mult", 1.0))
        builder = _build_prestige_gem_quest if quest_idx == 1 else _build_gem_quest
        self.quests[quest_idx] = builder(self._rng, self.difficulty)
        return True


# ---------------------------------------------------------------------------
# Merchant / Restaurant / Shrine data
# ---------------------------------------------------------------------------

MERCHANT_SHOP_TABLE = [
    # (item_id, gold_cost, display_name, barter_item, barter_qty)
    ("iron_chunk",     8,  "Iron Chunk",    "lumber",       5),
    ("coal",          12,  "Coal",          "stone_chip",   7),
    ("lumber",        10,  "Lumber",        "stone_chip",   6),
    ("wool",          15,  "Wool",          "lumber",       9),
    ("crystal_shard", 40,  "Crystal Shard", "iron_chunk",   8),
    ("stone_chip",     5,  "Stone Chip",    "dirt_clump",  10),
    ("obsidian_slab", 50,  "Obsidian Slab", "coal",        10),
    ("ruby",          70,  "Ruby",          "spirits",      4),
    ("milk",          18,  "Milk",          "wool",         4),
    ("tempered_iron", 60,  "Tempered Iron", "iron_chunk",  10),
]

CUISINE_MENUS = {
    "Noodle Shop": [
        ("beef_noodle_soup",    18),
        ("chicken_noodle_soup", 15),
        ("noodle_soup",         12),
        ("ramen",               20),
        ("chili_noodles",       16),
    ],
    "BBQ Stall": [
        ("mutton_skewer",       14),
        ("bbq_beef_ribs",       22),
        ("grilled_corn",         8),
        ("stuffed_pepper",      16),
        ("grilled_mushroom",    12),
        ("eggplant_skewer",     13),
    ],
    "Dim Sum House": [
        ("steamed_bun",          8),
        ("veggie_dumplings",    14),
        ("chicken_bun",         15),
        ("crystal_rolls",       13),
        ("rice_noodle_roll",    10),
    ],
    "Bakery": [
        ("bread",                8),
        ("corn_bread",          10),
        ("pumpkin_pie",         20),
        ("apple_pie",           18),
        ("carrot_cake",         22),
        ("cheese_bread",        14),
    ],
    "Stew House": [
        ("beef_stew",           22),
        ("mutton_hotpot",       20),
        ("chicken_mushroom_pot", 18),
        ("hot_pot_broth",       15),
        ("braised_chicken",     17),
    ],
    "Tapas Bar": [
        ("patatas_bravas",      12),
        ("croquetas",           14),
        ("gambas_al_ajillo",    18),
        ("tortilla_espanola",   16),
        ("pimientos_padron",    10),
        ("pan_tostado",          8),
        ("chorizo",             13),
        ("espetos",             15),
    ],
    "Mezze Restaurant": [
        ("hummus",              10),
        ("baba_ghanoush",       12),
        ("falafel",             13),
        ("shawarma",            20),
        ("tabbouleh",           11),
        ("kibbeh",              15),
        ("fattoush",            12),
        ("manakish",            14),
        ("kofte",               16),
        ("labneh",               9),
    ],
    "Trattoria": [
        ("bruschetta",          10),
        ("minestrone",          14),
        ("spaghetti_pomodoro",  16),
        ("pesto_gnocchi",       17),
        ("ossobuco",            24),
        ("ribollita",           15),
        ("bistecca",            22),
        ("cacio_e_pepe",        16),
        ("zuppa_di_pesce",      18),
        ("polenta",             11),
    ],
    "Spanish Bodega": [
        ("pan_tostado",          8),
        ("empanada",            14),
        ("patatas_bravas",      12),
        ("tortilla_espanola",   16),
        ("croquetas",           14),
        ("paella",              22),
        ("cocido_madrileno",    20),
        ("rabo_de_toro",        22),
        ("fabada",              18),
        ("churros",              9),
    ],
    "Japanese Izakaya": [
        ("edamame",              8),
        ("miso_soup",           10),
        ("onigiri",             12),
        ("gyoza",               13),
        ("yakitori",            14),
        ("tempura",             18),
        ("soba",                15),
        ("udon",                15),
        ("teriyaki_chicken",    19),
        ("tonkatsu",            20),
        ("matcha_cake",         12),
    ],
    "Greek Taverna": [
        ("tzatziki",             9),
        ("horiatiki",           11),
        ("spanakopita",         14),
        ("dolmades",            13),
        ("keftedes",            15),
        ("saganaki",            14),
        ("souvlaki",            17),
        ("moussaka",            20),
        ("kleftiko",            23),
        ("pastitsio",           19),
        ("loukoumades",         11),
    ],
    "Roman Thermopolium": [
        ("puls",                 8),
        ("flatbread",            8),
        ("olive",                6),
        ("isicia",              14),
        ("patina",              15),
        ("garum_fish",          16),
        ("pullum_numidicum",    19),
        ("libum",               11),
        ("dulcia",              10),
    ],
    "Indian Dhaba": [
        ("naan",                 9),
        ("raita",                8),
        ("samosa",              12),
        ("aloo_gobi",           15),
        ("chana_masala",        17),
        ("dal_makhani",         17),
        ("paneer_tikka",        17),
        ("tandoori_chicken",    21),
        ("butter_chicken",      21),
        ("biryani",             23),
        ("kheer",               12),
    ],
}

RELIGION_BY_BIOME = {
    "alpine_mountain": ("Himalayan Monastery",  "dzong"),
    "rocky_mountain":  ("Mountain Monastery",   "temple"),
    "temperate":       ("Forest Chapel",        "chapel"),
    "boreal":          ("Forest Chapel",        "chapel"),
    "birch_forest":    ("Woodland Shrine",      "chapel"),
    "redwood":         ("Grove Sanctuary",      "chapel"),
    "desert":          ("Desert Sanctum",       "desert_shrine"),
    "arid_steppe":     ("Desert Sanctum",       "desert_shrine"),
    "savanna":         ("Savanna Altar",        "desert_shrine"),
    "jungle":          ("Jungle Altar",         "jungle_shrine"),
    "tropical":        ("Tropical Shrine",      "jungle_shrine"),
    "wetland":         ("Swamp Oracle",         "jungle_shrine"),
    "tundra":          ("Standing Stones",      "standing_stones"),
    "steppe":          ("Ancestor Circle",      "standing_stones"),
    "canyon":          ("Cave Sanctum",         "temple"),
    "mediterranean":   ("Temple Precinct",      "classical"),
    "east_asian":      ("Shinto Shrine",        "shinto"),
    "south_asian":     ("Hindu Mandir",         "mandir"),
}

SHRINE_FLAVOR = {
    "dzong":           "Prayer flags snap in the mountain wind.\nThe whitewashed walls glow against dark peaks.\nBells toll somewhere above the clouds.",
    "temple":          "Incense drifts through stone archways.\nMonks chant in quiet reverence.",
    "chapel":          "Sunlight filters through the canopy above.\nA small bell hangs in the doorway.\nThe wood is worn smooth by many hands.",
    "desert_shrine":   "Carved stone glows in the desert heat.\nOld prayers are scratched into the walls.\nA clay bowl holds the remains of an offering.",
    "jungle_shrine":   "Moss clings to ancient carvings.\nThe air hums with the sound of insects.\nSomething watches from between the stones.",
    "standing_stones": "Weathered stones stand in a silent row.\nNames are carved in a forgotten tongue.\nThe ground between them never grows grass.",
    "shinto":          "A red gate frames the path ahead.\nStone lanterns flicker in the still air.\nSomewhere, a wind chime answers the breeze.",
    "mandir":          "Carved figures cover every surface of the shrine.\nThe scent of marigold and incense fills the air.\nA bell sounds once, then fades into silence.",
    "classical":       "White columns rise into clear sky.\nOlive branches hang above the entrance.\nA slow-burning flame marks the sacred threshold.",
}


def _rep_discount(rep):
    if rep >= 1000: return 0.60
    if rep >= 500:  return 0.70
    if rep >= 200:  return 0.80
    if rep >= 50:   return 0.90
    return 1.0


def _rep_buy_bonus(rep):
    if rep >= 1000: return 1.50
    if rep >= 500:  return 1.40
    if rep >= 200:  return 1.25
    if rep >= 50:   return 1.10
    return 1.0


class MerchantNPC(NPC):
    def __init__(self, x, y, world, rng, biodome="temperate"):
        super().__init__(x, y, world, "npc_merchant")
        self.clothing = _npc_clothing(biodome)
        n = rng.randint(3, 4)
        self.shop = rng.sample(MERCHANT_SHOP_TABLE, n)

    def discounted_cost(self, idx):
        _, cost, *_ = self.shop[idx]
        return max(1, round(cost * _rep_discount(self._town_rep())))

    def rep_discount_pct(self):
        return round((1.0 - _rep_discount(self._town_rep())) * 100)

    def can_buy(self, idx, player):
        return player.money >= self.discounted_cost(idx)

    def execute_purchase(self, idx, player):
        if not self.can_buy(idx, player):
            return False
        item_id = self.shop[idx][0]
        player.money -= self.discounted_cost(idx)
        player._add_item(item_id)
        return True

    def can_barter(self, idx, player):
        *_, barter_item, barter_qty = self.shop[idx]
        return player.inventory.get(barter_item, 0) >= barter_qty

    def execute_barter(self, idx, player):
        if not self.can_barter(idx, player):
            return False
        item_id, _, _, barter_item, barter_qty = self.shop[idx]
        player.inventory[barter_item] = player.inventory.get(barter_item, 0) - barter_qty
        if player.inventory[barter_item] <= 0:
            del player.inventory[barter_item]
            for i in range(len(player.hotbar)):
                if player.hotbar[i] == barter_item:
                    player.hotbar[i] = None
        player._add_item(item_id)
        return True


class RestaurantNPC(NPC):
    def __init__(self, x, y, world, rng, biodome="temperate"):
        super().__init__(x, y, world, "npc_chef")
        self.clothing = _npc_clothing(biodome)
        pool = _CUISINE_POOL_BY_BIOME.get(biodome, list(CUISINE_MENUS.keys()))
        self.cuisine = rng.choice(pool)
        self.menu = CUISINE_MENUS[self.cuisine]

    def discounted_cost(self, idx):
        _, cost = self.menu[idx]
        return max(1, round(cost * _rep_discount(self._town_rep())))

    def rep_discount_pct(self):
        return round((1.0 - _rep_discount(self._town_rep())) * 100)

    def can_buy(self, idx, player):
        return player.money >= self.discounted_cost(idx)

    def execute_purchase(self, idx, player):
        if not self.can_buy(idx, player):
            return False
        item_id, _ = self.menu[idx]
        player.money -= self.discounted_cost(idx)
        player._add_item(item_id)
        return True


class ShrineKeeperNPC(NPC):
    def __init__(self, x, y, world, rng, difficulty=0, biodome="temperate"):
        super().__init__(x, y, world, "npc_monk")
        self.clothing = _npc_clothing(biodome)
        display_name, style = RELIGION_BY_BIOME.get(biodome, ("Forest Chapel", "chapel"))
        self.religion_name = display_name
        self.religion_style = style
        self.flavor = SHRINE_FLAVOR.get(style, SHRINE_FLAVOR["chapel"])
        self.blessing_cost = 10 + difficulty * 10

    def discounted_cost(self):
        return max(1, round(self.blessing_cost * _rep_discount(self._town_rep())))

    def rep_discount_pct(self):
        return round((1.0 - _rep_discount(self._town_rep())) * 100)

    def _blessing_duration(self):
        rep = self._town_rep()
        if rep >= 1000: return 360.0
        if rep >= 500:  return 300.0
        if rep >= 200:  return 240.0
        return 180.0

    def can_bless(self, player):
        return player.money >= self.discounted_cost()

    def give_blessing(self, player):
        if not self.can_bless(player):
            return False
        player.money -= self.discounted_cost()
        player.blessing_timer = self._blessing_duration()
        player.blessing_mult = 1.25
        return True


class JewelryMerchantNPC(NPC):
    """Buys custom jewelry pieces from the player."""
    def __init__(self, x, y, world, rng, biodome="temperate"):
        super().__init__(x, y, world, "npc_merchant")
        self.clothing = _npc_clothing(biodome)
        self.display_name = "Jewelry Merchant"

    def appraise(self, jewelry, player):
        from jewelry import calculate_value
        return calculate_value(jewelry, player, master_jeweler=getattr(player, "master_jeweler", False))

    def sell_piece(self, jewelry_uid, player):
        piece = next((j for j in player.jewelry if j.uid == jewelry_uid), None)
        if piece is None:
            return 0
        value = self.appraise(piece, player)
        player.jewelry.remove(piece)
        player.money += value
        return value


class LeaderNPC(NPC):
    """Region leader who resides in a capital town's castle."""
    def __init__(self, x, y, world, region_id: int, region_name: str,
                 leader_name: str, leader_color: tuple):
        super().__init__(x, y, world, "npc_leader")
        self.region_id   = region_id
        self.region_name = region_name
        self.leader_name = leader_name
        self.leader_color = leader_color
        self.display_name = leader_name

    def get_dialog_lines(self, player):
        from towns import TOWNS, REGIONS, leader_greeting_for
        region = REGIONS.get(self.region_id)
        if region is None:
            return [f"Welcome, traveller. I govern {self.region_name}."]
        total_rep = sum(TOWNS[tid].reputation for tid in region.member_town_ids if tid in TOWNS)
        title = region.leader_title
        greeting = leader_greeting_for(region.biome_group)
        lines = [
            greeting,
            f"I am {title} {self.leader_name} of {self.region_name}.",
            f"Regional standing: {total_rep} reputation.",
        ]
        for tid in region.member_town_ids:
            town = TOWNS.get(tid)
            if town:
                lines.append(f"  {town.name} ({town.tier_name()})  rep {town.reputation}")
        return lines


# ---------------------------------------------------------------------------
# City generation
# ---------------------------------------------------------------------------

_DESERT_BIOMES    = {"desert", "arid_steppe", "savanna"}
_DESERT_PALETTE   = (SANDSTONE_BLOCK, POLISHED_MARBLE)
_DOME_SWAP        = {"house": "dome", "two_story": "dome", "longhouse": "dome"}

_HIMALAYAN_BIOMES  = {"alpine_mountain", "tundra"}
_HIMALAYAN_PALETTE = (WHITEWASHED_WALL, MONASTERY_ROOF)
_HIMALAYAN_SWAP    = {"house": "himalayan", "two_story": "himalayan", "longhouse": "himalayan"}

_MEDITERRANEAN_BIOMES  = {"mediterranean"}
_MEDITERRANEAN_PALETTES = [
    (WHITE_PLASTER_WALL, SPANISH_ROOF_TILE),
    (LIMESTONE_BLOCK,    HOUSE_ROOF_STONE),
    (ADOBE_BRICK,        SPANISH_ROOF_TILE),
]

_EAST_ASIAN_BIOMES  = {"east_asian"}
_EAST_ASIAN_PALETTE = (PINE_PLANK_WALL, SLATE_SHINGLE)
_EAST_ASIAN_SWAP    = {"shrine": "temple"}

_SOUTH_ASIAN_BIOMES  = {"south_asian"}
_SOUTH_ASIAN_PALETTES = [
    (LIMESTONE_BLOCK, TERRACOTTA_ROOF_TILE),
    (ADOBE_BRICK,     TERRACOTTA_ROOF_TILE),
]

# Restaurant wall/awning blocks keyed by culture style
_RESTAURANT_STYLES = {
    "default":       (RESTAURANT_WALL,    RESTAURANT_AWNING),
    "mediterranean": (WHITE_PLASTER_WALL, SPANISH_ROOF_TILE),
    "east_asian":    (PINE_PLANK_WALL,    PAGODA_EAVE),
    "south_asian":   (LIMESTONE_BLOCK,    TERRACOTTA_ROOF_TILE),
    "desert":        (SANDSTONE_BLOCK,    POLISHED_MARBLE),
}
_RESTAURANT_STYLE_BY_BIOME = {
    "mediterranean": "mediterranean",
    "east_asian":    "east_asian",
    "south_asian":   "south_asian",
    "desert":        "desert",
    "arid_steppe":   "desert",
    "savanna":       "desert",
}

# Cuisine pools weighted by biome — fallback is all menus
_CUISINE_POOL_BY_BIOME: dict[str, list[str]] = {
    "mediterranean": ["Trattoria", "Spanish Bodega", "Tapas Bar", "Greek Taverna"],
    "east_asian":    ["Japanese Izakaya", "Noodle Shop", "Dim Sum House"],
    "south_asian":   ["Indian Dhaba"],
    "desert":        ["Mezze Restaurant"],
    "arid_steppe":   ["Mezze Restaurant"],
    "savanna":       ["Mezze Restaurant", "BBQ Stall"],
    "alpine_mountain": ["Stew House", "Bakery"],
    "tundra":        ["Stew House", "Bakery"],
    "jungle":        ["BBQ Stall", "Stew House"],
    "tropical":      ["BBQ Stall", "Noodle Shop"],
}

# Building style palettes: (wall_block, roof_block)
BUILDING_PALETTES = [
    (HOUSE_WALL,         HOUSE_ROOF),         # warm wood
    (HOUSE_WALL_STONE,   HOUSE_ROOF_STONE),   # grey stone
    (HOUSE_WALL_BRICK,   HOUSE_ROOF_BRICK),   # red brick
    (HOUSE_WALL_DARK,    HOUSE_ROOF_DARK),    # dark timber
    (PINE_PLANK_WALL,    SLATE_SHINGLE),      # alpine pine
    (GRANITE_ASHLAR,     SLATE_SHINGLE),      # grey ashlar
    (ALPINE_PLASTER,     HOUSE_ROOF_DARK),    # whitewash + dark timber
    (HOUSE_WALL_BRICK,   SLATE_SHINGLE),      # english brick + slate
    (LIMESTONE_BLOCK,    HOUSE_ROOF_STONE),   # pale stone
    (ROUGH_STONE_WALL,   HOUSE_ROOF),         # rough stone + wood
    (COBBLESTONE,        HOUSE_ROOF_DARK),    # cobble + dark timber
    (WHITE_PLASTER_WALL, SPANISH_ROOF_TILE),  # mediterranean white + tile
    (ADOBE_BRICK,        SPANISH_ROOF_TILE),  # spanish adobe
    (AFRICAN_MUD_BRICK,  TERRACOTTA_ROOF_TILE), # west african banco
    (LIMESTONE_BLOCK,    TERRACOTTA_ROOF_TILE), # mediterranean stone + tile
    (HOUSE_WALL_DARK,    SLATE_SHINGLE),      # dark tudor + slate
    (ALPINE_PLASTER,     SLATE_SHINGLE),      # alpine whitewash + slate
]

# Rug colour pool — each house picks one for its floor.
_INTERIOR_RUGS = (
    TEXTILE_RUG_NATURAL, TEXTILE_RUG_GOLDEN, TEXTILE_RUG_CRIMSON,
    TEXTILE_RUG_ROSE,    TEXTILE_RUG_COBALT, TEXTILE_RUG_VIOLET,
    TEXTILE_RUG_VERDANT, TEXTILE_RUG_AMBER,  TEXTILE_RUG_IVORY,
)

# Tapestry colour pool — each house picks one for its back wall.
_INTERIOR_TAPESTRIES = (
    TEXTILE_TAPESTRY_NATURAL, TEXTILE_TAPESTRY_GOLDEN, TEXTILE_TAPESTRY_CRIMSON,
    TEXTILE_TAPESTRY_ROSE,    TEXTILE_TAPESTRY_COBALT, TEXTILE_TAPESTRY_VIOLET,
    TEXTILE_TAPESTRY_VERDANT, TEXTILE_TAPESTRY_AMBER,  TEXTILE_TAPESTRY_IVORY,
)

# Window-box flora pool — drops onto facades just under windows.
_FACADE_FLOWER_BOXES = (FLOWER_BOX, GERANIUM_BOX)

# Building slot format: (offset_from_cx, (min_w, max_w), (min_h, max_h), variants)
# variants is a list sampled uniformly; repeat entries to weight them.
# Use (offset, None, None, None) for an outdoor NPC slot with no building.
# Variants: "house", "two_story", "tower", "longhouse", "ruin", "restaurant", "shrine"
CITY_CONFIGS = {
    "small": {
        "half_w": 16,
        "buildings": [
            (-15, (4, 6), (3, 5), ["house", "house", "two_story", "tower", "ruin", "market_stall", "well"]),
            ( -3, (4, 5), (3, 4), ["restaurant"]),
            (  5, (4, 6), (3, 5), ["house", "house", "two_story", "longhouse", "ruin", "market_stall", "well"]),
        ],
        "npc_types": ["quest_rock", "restaurant_npc", "merchant"],
        # (center_offset, half_w) — small garden plots tucked between buildings.
        "gardens": [(-9, 2), (10, 2)],
        "squares": [],
        # Growth slots per tier: (offset, w_range, h_range, variants)
        "growth_slots_tier1": [( 12, (4, 5), (3, 4), ["two_story", "house"]),
                               (-12, (4, 5), (3, 4), ["house", "two_story"])],
        "growth_slots_tier2": [( 14, (5, 6), (4, 5), ["tower"]),
                               (-14, (4, 5), (3, 4), ["longhouse"])],
        "growth_slots_tier3": [( 16, (6, 7), (5, 6), ["tower"]),
                               (-16, (5, 6), (4, 5), ["two_story"])],
        # (center_offset, half_w) — farm fields outside the main footprint
        "farms": [(-24, 6), (24, 6)],
        # (offset, npc_type_string) — ambient residents placed at street level
        "ambient_npcs": [(-6, "villager"), (8, "child")],
    },
    "medium": {
        "half_w": 26,
        "buildings": [
            (-25, (4, 6), (3, 5), ["house", "two_story", "tower", "ruin", "longhouse", "pavilion"]),
            (-17, (4, 6), (3, 4), ["house", "house", "two_story", "longhouse", "ruin", "market_stall", "restaurant"]),
            ( -8, (4, 5), (3, 4), ["restaurant"]),
            ( -2, None,   None,   None),    # outdoor NPC — stands in the town square, offset from flag
            (  5, (4, 6), (3, 4), ["house", "house", "two_story", "ruin", "tower", "market_stall", "well"]),
            ( 13, (4, 6), (3, 5), ["house", "two_story", "tower", "longhouse", "ruin", "pavilion", "restaurant"]),
            ( 19, (6, 7), (5, 7), ["shrine"]),
        ],
        "npc_types": ["quest_rock", "restaurant_npc", "restaurant_npc",
                      "merchant", "quest_gem", "restaurant_npc", "shrine_npc"],
        "gardens": [(-21, 2), (-12, 2), (16, 2)],
        # (center_offset, half_w) — paved plaza with a centre sculpture.
        "squares": [(0, 4)],
        "growth_slots_tier1": [( 22, (4, 6), (3, 4), ["house", "two_story"]),
                               (-22, (4, 6), (3, 4), ["house", "longhouse"])],
        "growth_slots_tier2": [( 24, (5, 7), (4, 5), ["tower", "two_story"]),
                               (-24, (5, 6), (4, 5), ["tower", "two_story"])],
        "growth_slots_tier3": [( 26, (6, 8), (5, 6), ["tower"]),
                               (-26, (5, 7), (4, 6), ["longhouse"])],
        "farms": [(-36, 7), (36, 7)],
        "ambient_npcs": [(-12, "villager"), (-6, "child"), (9, "villager"), (15, "child")],
    },
    "large": {
        "half_w": 36,
        "buildings": [
            (-35, (5, 7), (4, 5), ["house", "two_story", "two_story", "tower", "longhouse", "pavilion"]),
            (-27, (4, 6), (3, 5), ["house", "house", "ruin", "tower", "two_story", "market_stall", "restaurant"]),
            (-19, (4, 5), (3, 4), ["house", "house", "two_story", "ruin", "longhouse", "pavilion", "restaurant"]),
            ( -8, None,   None,   None),    # outdoor NPC — stands in left square, offset from flag
            ( -2, (4, 5), (3, 4), ["house", "two_story", "ruin", "tower", "longhouse", "market_stall"]),
            (  5, (4, 5), (3, 4), ["restaurant"]),
            ( 11, None,   None,   None),    # outdoor NPC — stands in right square, offset from flag
            ( 18, (4, 6), (3, 5), ["house", "house", "tower", "ruin", "two_story", "market_stall", "restaurant"]),
            ( 26, (7, 9), (5, 7), ["shrine"]),
        ],
        "npc_types": ["quest_rock", "restaurant_npc", "restaurant_npc", "merchant",
                      "quest_gem", "restaurant_npc", "quest_wildflower", "restaurant_npc",
                      "shrine_npc", "jewelry_merchant"],
        "gardens": [(-31, 2), (-23, 2), (22, 2)],
        "squares": [(-10, 4), (13, 4)],
        "growth_slots_tier1": [( 32, (4, 6), (3, 4), ["house", "two_story"]),
                               (-32, (4, 6), (3, 4), ["house", "longhouse"])],
        "growth_slots_tier2": [( 34, (5, 7), (4, 5), ["tower", "two_story"]),
                               (-34, (5, 7), (4, 5), ["tower", "longhouse"])],
        "growth_slots_tier3": [( 36, (6, 8), (5, 6), ["tower"]),
                               (-36, (5, 7), (4, 6), ["tower"])],
        "farms": [(-48, 8), (48, 8)],
        "ambient_npcs": [(-30, "villager"), (-14, "child"), (0, "villager"),
                         (8, "child"), (22, "villager"), (28, "guard")],
    },
    # Tier-3 metropolis (capital after max growth)
    "city": {
        "half_w": 46,
        "buildings": [],
        "npc_types": [],
        "gardens": [],
        "squares": [(0, 4)],
        "growth_slots_tier1": [],
        "growth_slots_tier2": [],
        "growth_slots_tier3": [],
        "farms": [(-60, 9), (60, 9)],
        "ambient_npcs": [(-30, "villager"), (-14, "child"), (0, "villager"),
                         (8, "child"), (22, "villager"), (28, "guard"),
                         (-42, "guard"), (42, "guard")],
    },
}

_SIZE_BY_DIFFICULTY = {
    0: ["small", "small", "medium"],
    1: ["medium", "medium", "large"],
    2: ["large", "large", "medium"],
}

_PLANT_BLOCKS = ALL_LOGS | ALL_LEAVES | BUSH_BLOCKS | {SAPLING}


# ---------------------------------------------------------------------------
# City gardens
# ---------------------------------------------------------------------------

# Each theme is a sequence of decorative garden blocks placed along the
# sy-1 row in front of buildings. Themes are chosen per-garden based on
# biome and a random pick.
GARDEN_THEMES = {
    "flower_meadow": (LAVENDER_BED, ROSE_BED, TULIP_BED, MARIGOLD_BED,
                      IRIS_BED, POPPY_BED, DAHLIA_BED, SUNFLOWER_BED),
    "cottage":       (COTTAGE_GARDEN_BED, BEE_SKEP, FOXGLOVE_PATCH,
                      ALLIUM_PATCH, COTTAGE_GARDEN_BED, FLOWERING_SHRUB,
                      PEONY_BUSH, HYDRANGEA_BUSH),
    "formal":        (BOXWOOD_BALL, TOPIARY_RABBIT, BOXWOOD_BALL,
                      TOPIARY_PEACOCK, BOXWOOD_BALL, TOPIARY_BEAR,
                      BOXWOOD_BALL, TOPIARY_SWAN),
    "topiary_zoo":   (TOPIARY_FOX, TOPIARY_OWL, TOPIARY_HEDGEHOG,
                      TOPIARY_SNAIL, TOPIARY_MUSHROOM, TOPIARY_ARCH,
                      TOPIARY_RABBIT, TOPIARY_PEACOCK),
    "fountain_plaza":(HOLLY_SHRUB, FLOWERING_SHRUB, BUBBLE_FOUNTAIN,
                      FLOWERING_SHRUB, HOLLY_SHRUB, RHODODENDRON_BUSH,
                      SHELL_FOUNTAIN, BOXWOOD_BALL),
    "kitchen":       (COMPOST_HEAP, COLD_FRAME, POTTING_TABLE,
                      RAIN_BARREL, BEE_SKEP, GARDEN_WHEELBARROW,
                      STONE_TROUGH_PLANTER, BIRD_TABLE),
    "ornament":      (GARDEN_GNOME, STONE_FROG, STONE_HEDGEHOG,
                      GARDEN_TOAD_HOUSE, BIRD_TABLE, GARDEN_DOVECOTE,
                      GARDEN_OBELISK_METAL, GARDEN_CLOCK),
    "fern_grove":    (FERN_CLUMP, BAMBOO_CLUMP, ORNAMENTAL_GRASS,
                      FERN_CLUMP, BAMBOO_CLUMP, MOSS_PATCH,
                      LILY_PAD_POND, FERN_CLUMP),
    "english_park":  (STANDARD_ROSE, BOXWOOD_BALL, AGAPANTHUS_PATCH,
                      ASTILBE_PATCH, BLEEDING_HEART_PATCH, STANDARD_ROSE,
                      KNOT_GARDEN, RHODODENDRON_BUSH),
    "wisteria_walk": (WISTERIA_PILLAR, SWEET_PEA_TRELLIS, TRELLIS_ARCH,
                      WISTERIA_PILLAR, FLOWERING_SHRUB, SWEET_PEA_TRELLIS,
                      WISTERIA_PILLAR, GARDEN_SWING),
    "alpine_yard":   (HAY_BALE, FIREWOOD_STACK, RAIN_BARREL,
                      COMPOST_HEAP, FLOWER_BOX, FERN_CLUMP,
                      WICKER_FENCE, GARDEN_WHEELBARROW),
    "monastic":      (HOLLY_SHRUB, BOXWOOD_BALL, KNOT_GARDEN,
                      LAVENDER_BED, ROSE_BED, BOXWOOD_BALL,
                      MARIGOLD_BED, BOXWOOD_BALL),
    "pondside":      (LILY_PAD_POND, KOI_POOL, FERN_CLUMP,
                      LILY_PAD_POND, BAMBOO_CLUMP, FERN_CLUMP,
                      KOI_POOL, MOSS_PATCH),
    "japanese_garden": (PINE_TOPIARY_JP, KOI_POOL, SHISHI_ODOSHI,
                        JAPANESE_MAPLE, BAMBOO_CLUMP, MOSS_PATCH,
                        RED_ARCH_BRIDGE, FERN_CLUMP),
    "mediterranean_patio": (STANDARD_ROSE, ROSE_BED, LAVENDER_BED,
                            AGAPANTHUS_PATCH, ORNAMENTAL_GRASS,
                            PORTUGUESE_BENCH, BUBBLE_FOUNTAIN, FLOWERING_SHRUB),
    "south_asian_garden": (MARIGOLD_BED, SUNFLOWER_BED, KOI_POOL,
                           ORNAMENTAL_GRASS, FERN_CLUMP, LILY_PAD_POND,
                           BAMBOO_CLUMP, FLOWERING_SHRUB),
}

# Lawn ground covers used to fill gaps between accent blocks.
_LAWN_BLOCKS = (CHAMOMILE_LAWN, CLOVER_LAWN, MOSS_PATCH, BARK_MULCH)

# Biome-flavoured garden theme bias. Falls back to "any" if not listed.
_GARDEN_THEMES_BY_BIOME = {
    "temperate":      ["flower_meadow", "cottage", "formal", "ornament",
                       "english_park", "wisteria_walk"],
    "boreal":         ["fern_grove", "cottage", "ornament", "alpine_yard"],
    "birch_forest":   ["cottage", "flower_meadow", "fern_grove", "english_park"],
    "redwood":        ["fern_grove", "ornament", "formal", "pondside"],
    "tropical":       ["fern_grove", "topiary_zoo", "fountain_plaza", "wisteria_walk"],
    "jungle":         ["fern_grove", "topiary_zoo", "pondside"],
    "savanna":        ["topiary_zoo", "ornament", "formal"],
    "wetland":        ["fern_grove", "cottage", "pondside"],
    "tundra":         ["formal", "ornament", "alpine_yard"],
    "steppe":         ["formal", "ornament", "cottage", "monastic"],
    "alpine_mountain":["fountain_plaza", "formal", "alpine_yard", "monastic"],
    "rocky_mountain": ["formal", "ornament", "alpine_yard"],
    "canyon":         ["ornament", "formal", "monastic"],
    "desert":         ["fountain_plaza", "ornament", "monastic"],
    "arid_steppe":    ["fountain_plaza", "ornament", "monastic"],
    "mediterranean":  ["mediterranean_patio", "flower_meadow", "formal",
                       "wisteria_walk", "cottage"],
    "east_asian":     ["japanese_garden", "pondside", "fern_grove",
                       "monastic"],
    "south_asian":    ["south_asian_garden", "flower_meadow", "fountain_plaza",
                       "topiary_zoo"],
}

_FOUNTAIN_BLOCKS = (BUBBLE_FOUNTAIN, SHELL_FOUNTAIN, MILLSTONE_FOUNTAIN,
                    CHERUB_FOUNTAIN, MOSAIC_FOUNTAIN, LION_HEAD_FOUNTAIN)

# ---------------------------------------------------------------------------
# Clothing palettes — keyed by cultural style, used by ambient NPC renderer
# ---------------------------------------------------------------------------
# Keys: body, leg, skin, trim (belt/collar), hat (farmer), armor/plate (guard)

_CLOTHING_PALETTES = {
    "temperate": {
        "body": (90, 115, 75), "leg": (90, 70, 45), "skin": (255, 215, 160),
        "trim": (110, 75, 35), "hat": (200, 175, 80),
        "armor": (55, 55, 75), "plate": (155, 160, 165),
    },
    "desert": {
        # Light flowing robes, warm skin, deep blue trim
        "body": (238, 232, 210), "leg": (230, 225, 200), "skin": (205, 160, 105),
        "trim": (50, 90, 160), "hat": (245, 238, 215),
        "armor": (200, 175, 100), "plate": (230, 200, 130),
    },
    "alpine": {
        # Heavy wool in deep burgundy, fair skin
        "body": (105, 40, 40), "leg": (75, 60, 50), "skin": (245, 205, 160),
        "trim": (165, 120, 70), "hat": (130, 60, 40),
        "armor": (50, 45, 55), "plate": (130, 135, 145),
    },
    "mediterranean": {
        # Terra cotta and ochre with olive skin
        "body": (185, 90, 50), "leg": (215, 200, 155), "skin": (220, 180, 125),
        "trim": (30, 25, 20), "hat": (215, 185, 100),
        "armor": (80, 50, 30), "plate": (195, 165, 100),
    },
    "east_asian": {
        # Indigo and grey-blue robes, warm-fair skin
        "body": (70, 95, 140), "leg": (60, 75, 115), "skin": (245, 205, 165),
        "trim": (25, 25, 35), "hat": (90, 80, 45),
        "armor": (40, 40, 55), "plate": (110, 130, 155),
    },
    "south_asian": {
        # Saffron and coral with warm brown skin
        "body": (215, 115, 35), "leg": (225, 215, 185), "skin": (180, 135, 85),
        "trim": (200, 175, 40), "hat": (235, 190, 80),
        "armor": (140, 85, 30), "plate": (210, 175, 80),
    },
    "jungle": {
        # Deep greens and earthy cotton, dark skin
        "body": (65, 145, 85), "leg": (100, 75, 45), "skin": (165, 115, 70),
        "trim": (190, 155, 50), "hat": (170, 140, 50),
        "armor": (45, 75, 45), "plate": (90, 130, 80),
    },
    "boreal": {
        # Dark forest green and navy, pale skin
        "body": (50, 80, 65), "leg": (55, 55, 70), "skin": (250, 215, 175),
        "trim": (100, 80, 55), "hat": (70, 100, 70),
        "armor": (45, 50, 60), "plate": (120, 130, 140),
    },
    "steppe": {
        # Rust orange and deep gold, medium warm skin
        "body": (175, 95, 40), "leg": (140, 100, 50), "skin": (200, 158, 100),
        "trim": (130, 35, 30), "hat": (195, 150, 55),
        "armor": (100, 65, 30), "plate": (175, 140, 70),
    },
    "coastal": {
        # Faded blues and sandy cream, tanned skin
        "body": (90, 130, 165), "leg": (210, 195, 160), "skin": (215, 175, 120),
        "trim": (50, 80, 110), "hat": (200, 180, 120),
        "armor": (55, 75, 95), "plate": (140, 160, 180),
    },
}
_CLOTHING_DEFAULT = _CLOTHING_PALETTES["temperate"]

# Maps biodome string → clothing style key
_CLOTHING_STYLE_BY_BIODOME = {
    "temperate": "temperate", "birch_forest": "temperate", "redwood": "temperate",
    "boreal": "boreal",
    "alpine_mountain": "alpine", "tundra": "alpine", "rocky_mountain": "alpine",
    "desert": "desert", "arid_steppe": "desert", "savanna": "desert", "canyon": "desert",
    "mediterranean": "mediterranean",
    "east_asian": "east_asian",
    "south_asian": "south_asian",
    "jungle": "jungle", "tropical": "jungle",
    "wetland": "boreal", "swamp": "boreal",
    "steppe": "steppe", "wasteland": "steppe",
    "beach": "coastal",
}

def _npc_clothing(biodome):
    style = _CLOTHING_STYLE_BY_BIODOME.get(biodome, "temperate")
    return _CLOTHING_PALETTES.get(style, _CLOTHING_DEFAULT)



# ---------------------------------------------------------------------------
# Farm data
# ---------------------------------------------------------------------------

# Maps biodome strings to a simplified group key for farm crop selection.
_BIOME_GROUP_SIMPLE = {
    "temperate": "temperate", "boreal": "boreal", "birch_forest": "temperate",
    "redwood": "temperate",   "jungle": "jungle",  "tropical": "jungle",
    "wetland": "wetland",     "swamp": "wetland",  "desert": "desert",
    "arid_steppe": "desert",  "savanna": "desert", "alpine_mountain": "alpine",
    "tundra": "alpine",       "rocky_mountain": "alpine", "steppe": "steppe",
    "wasteland": "steppe",    "canyon": "steppe",  "beach": "coastal",
    "mediterranean": "temperate", "east_asian": "temperate", "south_asian": "jungle",
}

# Crops that appear in city farm fields, by biome group.
FARM_CROPS_BY_BIOME = {
    "temperate": [WHEAT_CROP_YOUNG, CARROT_CROP_YOUNG, POTATO_CROP_YOUNG,
                  CABBAGE_CROP_YOUNG, LEEK_CROP_YOUNG, BEET_CROP_YOUNG],
    "boreal":    [WHEAT_CROP_YOUNG, POTATO_CROP_YOUNG, TURNIP_CROP_YOUNG,
                  BEET_CROP_YOUNG, LEEK_CROP_YOUNG],
    "desert":    [ONION_CROP_YOUNG, GARLIC_CROP_YOUNG, EGGPLANT_CROP_YOUNG,
                  CHILI_CROP_YOUNG],
    "alpine":    [TURNIP_CROP_YOUNG, POTATO_CROP_YOUNG, BEET_CROP_YOUNG,
                  WHEAT_CROP_YOUNG],
    "jungle":    [RICE_CROP_YOUNG, BOK_CHOY_CROP_YOUNG, CHILI_CROP_YOUNG,
                  SWEET_POTATO_CROP_YOUNG],
    "wetland":   [RICE_CROP_YOUNG, LEEK_CROP_YOUNG, CELERY_CROP_YOUNG],
    "steppe":    [WHEAT_CROP_YOUNG, ONION_CROP_YOUNG, POTATO_CROP_YOUNG],
    "coastal":   [CABBAGE_CROP_YOUNG, ONION_CROP_YOUNG, LEEK_CROP_YOUNG],
}
_FARM_CROPS_DEFAULT = [WHEAT_CROP_YOUNG, CARROT_CROP_YOUNG, POTATO_CROP_YOUNG]

# Maps young crop block → its mature variant for visual variety in pre-grown fields.
_YOUNG_TO_MATURE = {
    WHEAT_CROP_YOUNG:        WHEAT_CROP_MATURE,
    CARROT_CROP_YOUNG:       CARROT_CROP_MATURE,
    POTATO_CROP_YOUNG:       POTATO_CROP_MATURE,
    CABBAGE_CROP_YOUNG:      CABBAGE_CROP_MATURE,
    LEEK_CROP_YOUNG:         LEEK_CROP_MATURE,
    BEET_CROP_YOUNG:         BEET_CROP_MATURE,
    TURNIP_CROP_YOUNG:       TURNIP_CROP_MATURE,
    ONION_CROP_YOUNG:        ONION_CROP_MATURE,
    GARLIC_CROP_YOUNG:       GARLIC_CROP_MATURE,
    EGGPLANT_CROP_YOUNG:     EGGPLANT_CROP_MATURE,
    CHILI_CROP_YOUNG:        CHILI_CROP_MATURE,
    RICE_CROP_YOUNG:         RICE_CROP_MATURE,
    BOK_CHOY_CROP_YOUNG:     BOK_CHOY_CROP_MATURE,
    SWEET_POTATO_CROP_YOUNG: SWEET_POTATO_CROP_MATURE,
    CELERY_CROP_YOUNG:       CELERY_CROP_MATURE,
}


def _place_garden_plot(world, rng, center_bx, sy, biodome, half_w=3):
    """Paint a small garden along the row above the city floor.

    All accent blocks are placed as background blocks so the player can
    still walk through the city street — the garden reads visually but
    never obstructs movement.
    """
    pool = _GARDEN_THEMES_BY_BIOME.get(biodome, list(GARDEN_THEMES.keys()))
    theme_name = rng.choice(pool)
    blocks = GARDEN_THEMES[theme_name]

    plot_y = sy - 1
    fence_y = sy - 2
    if not (0 <= plot_y < world.height):
        return

    for wx in range(center_bx - half_w, center_bx + half_w + 1):
        if world.get_block(wx, plot_y) != AIR:
            continue
        # 65% accent block from the theme, 35% lawn cover
        if rng.random() < 0.65:
            world.set_bg_block(wx, plot_y, rng.choice(blocks))
        else:
            world.set_bg_block(wx, plot_y, rng.choice(_LAWN_BLOCKS))

    # Fountain centerpiece on plaza-style themes.
    if theme_name == "fountain_plaza" and 0 <= plot_y < world.height:
        world.set_bg_block(center_bx, plot_y, rng.choice(_FOUNTAIN_BLOCKS))

    # A few low wicker-fence segments behind the plot for visual framing.
    if 0 <= fence_y < world.height:
        for wx in (center_bx - half_w, center_bx + half_w):
            if world.get_block(wx, fence_y) == AIR:
                world.set_bg_block(wx, fence_y, WICKER_FENCE)


def _place_farm_plot(world, rng, center_bx, sy, biodome, half_w=7):
    """Place a strip of tilled soil with crops outside the city footprint.

    Layout rows (top-down):
      sy - 2 : crop blocks (young or ~50% mature for visual variety)
      sy - 1 : tilled soil
      sy     : city stone floor (already placed by _build_single_city)

    A well is placed as a background block at the centre column.
    Wicker fence posts frame the outer edges.
    Crops are chosen by biome group so farm contents match the landscape.
    """
    biome_group = _BIOME_GROUP_SIMPLE.get(biodome, "temperate")
    crops = FARM_CROPS_BY_BIOME.get(biome_group, _FARM_CROPS_DEFAULT)

    for bx in range(center_bx - half_w, center_bx + half_w + 1):
        soil_y = sy - 1
        crop_y = sy - 2
        if not (0 <= soil_y < world.height):
            continue
        if world.get_block(bx, soil_y) != AIR:
            continue
        world.set_block(bx, soil_y, TILLED_SOIL)
        if 0 <= crop_y < world.height and world.get_block(bx, crop_y) == AIR:
            chosen = rng.choice(crops)
            if rng.random() < 0.5:
                chosen = _YOUNG_TO_MATURE.get(chosen, chosen)
            world.set_block(bx, crop_y, chosen)

    # Central well as a background landmark
    well_y = sy - 1
    if 0 <= well_y < world.height:
        world.set_bg_block(center_bx, well_y, WELL_BLOCK)

    # Fence corner posts
    fence_y = sy - 3
    if 0 <= fence_y < world.height:
        for bx in (center_bx - half_w, center_bx + half_w):
            if world.get_block(bx, fence_y) == AIR:
                world.set_bg_block(bx, fence_y, WICKER_FENCE)


# ---------------------------------------------------------------------------
# Town squares
# ---------------------------------------------------------------------------

# Each theme is:
#   "monument" — list of bg blocks placed bottom-up at the centre column
#                (e.g. plinth on row sy-1, statue on row sy-2)
#   "flank"    — bg block flanking the monument, 2 rows out on each side
#   "edge"     — bg block at the outer edges of the plaza
#   "paving"   — solid block that replaces the city stone floor across the plaza
SQUARE_THEMES = {
    "civic_marble": {
        "monument": [MARBLE_PLINTH, MARBLE_STATUE],
        "flank":    GREEK_STONE_BENCH,
        "edge":     TRIPOD_BRAZIER,
        "paving":   INLAID_MARBLE,
    },
    "obelisk_court": {
        "monument": [MARBLE_PLINTH, GARDEN_OBELISK],
        "flank":    GARDEN_LANTERN,
        "edge":     GARDEN_COLUMN,
        "paving":   HERRINGBONE_GARDEN,
    },
    "victory_plaza": {
        "monument": [MARBLE_PLINTH, VICTORY_STELE],
        "flank":    LAUREL_WREATH_MOUNT,
        "edge":     CARVED_BENCH,
        "paving":   GARDEN_STAR_TILE,
    },
    "scholar_court": {
        "monument": [MARBLE_PLINTH, HERMES_STELE],
        "flank":    STONE_BASIN,
        "edge":     DORIC_CAPITAL,
        "paving":   INLAID_MARBLE,
    },
    "fountain_square": {
        "monument": [MOSAIC_FOUNTAIN],
        "flank":    GREEK_STONE_BENCH,
        "edge":     BRAZIER,
        "paving":   HERRINGBONE_GARDEN,
    },
    "cherub_court": {
        "monument": [CHERUB_FOUNTAIN],
        "flank":    CARVED_BENCH,
        "edge":     GARDEN_LANTERN,
        "paving":   MARBLE_MEDALLION_REN,
    },
    "birdbath_garden": {
        "monument": [MARBLE_BIRDBATH],
        "flank":    FERN_CLUMP,
        "edge":     STONE_TROUGH_PLANTER,
        "paving":   CHAMOMILE_LAWN,
    },
    "lion_plaza": {
        "monument": [LION_HEAD_FOUNTAIN],
        "flank":    GREEK_STONE_BENCH,
        "edge":     STAR_LAMP,
        "paving":   GARDEN_STAR_TILE,
    },
    "scholar_rock": {
        "monument": [GARDEN_ROCK],
        "flank":    BAMBOO_CLUMP,
        "edge":     GARDEN_LANTERN,
        "paving":   HERRINGBONE_GARDEN,
    },
    "agora_forum": {
        "monument": [MARBLE_PLINTH, DORIC_CAPITAL],
        "flank":    SYMPOSIUM_TABLE,
        "edge":     PHILOSOPHERS_SCROLL,
        "paving":   INLAID_MARBLE,
    },
    "festival_square": {
        "monument": [BRAZIER, CHANDELIER],
        "flank":    CANDELABRA,
        "edge":     STAR_LAMP,
        "paving":   GARDEN_STAR_TILE,
    },
    "olive_grove": {
        "monument": [STONE_BASIN, OLIVE_BRANCH],
        "flank":    SYMPOSIUM_TABLE,
        "edge":     GREEK_STONE_BENCH,
        "paving":   HERRINGBONE_GARDEN,
    },
    "theatre_court": {
        "monument": [MARBLE_PLINTH, GREEK_THEATRE_MASK],
        "flank":    GREEK_STONE_BENCH,
        "edge":     LAUREL_WREATH_MOUNT,
        "paving":   GARDEN_STAR_TILE,
    },
    "lantern_court": {
        "monument": [GARDEN_LANTERN, LANTERN_ORB],
        "flank":    GREEK_STONE_BENCH,
        "edge":     STAR_LAMP,
        "paving":   MARBLE_MEDALLION_REN,
    },
    "garden_pavilion": {
        "monument": [GARDEN_TABLE, MARBLE_BIRDBATH],
        "flank":    CARVED_BENCH,
        "edge":     GARDEN_LANTERN,
        "paving":   CHAMOMILE_LAWN,
    },
    "torii_plaza": {
        "monument": [TORII_PANEL, TORII_PANEL],
        "flank":    PINE_TOPIARY_JP,
        "edge":     SHISHI_ODOSHI,
        "paving":   TATAMI_PAVING,
    },
    "zen_court": {
        "monument": [GARDEN_ROCK, GARDEN_LANTERN],
        "flank":    PINE_TOPIARY_JP,
        "edge":     BAMBOO_CLUMP,
        "paving":   MOSS_PATCH,
    },
    "roman_forum": {
        "monument": [ROMAN_ARCH_REN, MARBLE_STATUE],
        "flank":    ROMAN_ARCH_REN,
        "edge":     MARBLE_PLINTH,
        "paving":   ROMAN_MOSAIC,
    },
    "greek_agora": {
        "monument": [MARBLE_PLINTH, GREEK_AMPHORA],
        "flank":    GREEK_STONE_BENCH,
        "edge":     VOTIVE_TABLET,
        "paving":   INLAID_MARBLE,
    },
    "mughal_court": {
        "monument": [MUGHAL_ARCH],
        "flank":    ORNAMENTAL_GRASS,
        "edge":     MARIGOLD_BED,
        "paving":   MUDEJAR_STAR_TILE,
    },
    "spanish_plaza": {
        "monument": [ANDALUSIAN_FOUNTAIN],
        "flank":    PORTUGUESE_BENCH,
        "edge":     ORNAMENTAL_GRASS,
        "paving":   SPANISH_PATIO_FLOOR,
    },
}

_SQUARE_THEMES_BY_BIOME = {
    "temperate":      ["civic_marble", "fountain_square", "victory_plaza",
                       "birdbath_garden", "garden_pavilion", "lantern_court"],
    "boreal":         ["civic_marble", "fountain_square", "scholar_court",
                       "lantern_court"],
    "birch_forest":   ["birdbath_garden", "fountain_square", "civic_marble",
                       "garden_pavilion"],
    "redwood":        ["scholar_court", "civic_marble", "birdbath_garden",
                       "garden_pavilion"],
    "tropical":       ["fountain_square", "lion_plaza", "scholar_rock",
                       "lantern_court"],
    "jungle":         ["scholar_rock", "lion_plaza", "fountain_square"],
    "savanna":        ["lion_plaza", "obelisk_court", "victory_plaza",
                       "agora_forum"],
    "wetland":        ["birdbath_garden", "scholar_rock", "lantern_court"],
    "tundra":         ["civic_marble", "victory_plaza", "festival_square"],
    "steppe":         ["obelisk_court", "victory_plaza", "agora_forum"],
    "alpine_mountain":["civic_marble", "scholar_court", "festival_square"],
    "rocky_mountain": ["civic_marble", "obelisk_court", "agora_forum"],
    "canyon":         ["obelisk_court", "lion_plaza", "theatre_court"],
    "desert":         ["obelisk_court", "lion_plaza", "fountain_square",
                       "olive_grove"],
    "arid_steppe":    ["obelisk_court", "lion_plaza", "olive_grove",
                       "theatre_court"],
    "mediterranean":  ["spanish_plaza", "greek_agora", "roman_forum",
                       "civic_marble", "fountain_square"],
    "east_asian":     ["torii_plaza", "zen_court", "scholar_rock",
                       "lantern_court"],
    "south_asian":    ["mughal_court", "lion_plaza", "fountain_square",
                       "festival_square"],
}


def _place_town_square(world, rng, center_bx, sy, biodome, half_w=4):
    """Carve out a paved town square with a central sculpture.

    Paving replaces the city floor (still solid, so the player walks on it).
    The monument, benches, lanterns, and other ornamentation are placed as
    background blocks so the entire plaza stays walkable.
    """
    pool = _SQUARE_THEMES_BY_BIOME.get(biodome, list(SQUARE_THEMES.keys()))
    theme_name = rng.choice(pool)
    theme = SQUARE_THEMES[theme_name]

    # Pave the floor row across the square.
    paving = theme["paving"]
    for wx in range(center_bx - half_w, center_bx + half_w + 1):
        if world.get_block(wx, sy) == STONE:
            world.set_block(wx, sy, paving)

    # Central sculpture (monument) — stacked bottom-up from sy-1.
    monument = theme["monument"]
    for i, blk in enumerate(monument):
        my = sy - 1 - i
        if 0 <= my < world.height and world.get_block(center_bx, my) == AIR:
            world.set_bg_block(center_bx, my, blk)

    # Flanking decoration two columns out on each side.
    flank = theme["flank"]
    flank_y = sy - 1
    for dx in (-2, 2):
        wx = center_bx + dx
        if 0 <= flank_y < world.height and world.get_block(wx, flank_y) == AIR:
            world.set_bg_block(wx, flank_y, flank)

    # Edge ornaments on the outer corners.
    edge = theme["edge"]
    edge_y = sy - 1
    for wx in (center_bx - half_w, center_bx + half_w):
        if 0 <= edge_y < world.height and world.get_block(wx, edge_y) == AIR:
            world.set_bg_block(wx, edge_y, edge)

    # Town flag — placed in background at square center, one block above the ground.
    flag_y = sy - 1
    if 0 <= flag_y < world.height:
        world.set_bg_block(center_bx, flag_y, TOWN_FLAG_BLOCK)


# ---------------------------------------------------------------------------
# Streets, streetlamps, gateposts, pavilions, wells
# ---------------------------------------------------------------------------

# Pool of paving blocks chosen per-city for the main street.
_STREET_PAVINGS = (COBBLESTONE, HERRINGBONE_GARDEN, GARDEN_STAR_TILE,
                   INLAID_MARBLE)

# Pool of streetlamp blocks placed periodically along the street.
_STREETLAMP_BLOCKS = (GARDEN_LANTERN, TORCH, WALL_SCONCE,
                      LANTERN_ORB, STAR_LAMP, BRAZIER)


def _pave_main_street(world, rng, lo_x, hi_x, sy):
    """Replace the bare-stone city floor with a chosen paving block.

    Skips bedrock and any non-stone block, so building floors, rugs, and
    square paving aren't overwritten.
    """
    paving = rng.choice(_STREET_PAVINGS)
    if not (0 <= sy < world.height):
        return
    for bx in range(lo_x, hi_x + 1):
        if world.get_block(bx, sy) == STONE:
            world.set_block(bx, sy, paving)


def _place_streetlamps(world, rng, lo_x, hi_x, sy, spacing=6):
    """Sprinkle bg-block streetlamps along the city street.

    Each lamp sits above the floor as a background block so it renders
    against the sky without blocking the player. Lamps are skipped over
    columns that are inside a roofed building — we test several rows of
    headroom to distinguish open street from interior.
    """
    lamp = rng.choice(_STREETLAMP_BLOCKS)
    lamp_y = sy - 2
    if not (0 <= lamp_y < world.height):
        return
    for bx in range(lo_x, hi_x + 1, spacing):
        # All four rows above the floor must be open air — guarantees we're
        # outdoors and not standing under a building roof.
        if all(world.get_block(bx, sy - dy) == AIR for dy in (1, 2, 3, 4, 5)):
            world.set_bg_block(bx, lamp_y, lamp)


def _place_gateposts(world, rng, lo_x, hi_x, sy):
    """Tall stone posts at the two ends of the city marking the entrance.

    Each post is 4 rows of stacked masonry topped with an ornamental cap.
    Posts are real solid blocks so they read as a clear threshold; the
    gap between post and city body is wide enough to walk through.
    """
    cap = rng.choice((GARDEN_OBELISK, ARCH_STONE, DORIC_CAPITAL,
                      LAUREL_WREATH_MOUNT, GARDEN_LANTERN))
    base_block = rng.choice((HOUSE_WALL_STONE, GRANITE_ASHLAR, LIMESTONE_BLOCK,
                             COBBLESTONE))
    for bx in (lo_x, hi_x):
        for dy in range(1, 5):
            wy = sy - dy
            if 0 <= wy < world.height and world.get_block(bx, wy) == AIR:
                world.set_block(bx, wy, base_block)
        cap_y = sy - 5
        if 0 <= cap_y < world.height and world.get_block(bx, cap_y) == AIR:
            world.set_block(bx, cap_y, cap)


def _place_pavilion(world, left_x, sy, width, wall_height,
                    wall_block=GARDEN_COLUMN, roof_block=HOUSE_ROOF_STONE):
    """Open-sided garden pavilion: columns at each corner, peaked roof, hollow inside."""
    h = max(3, wall_height)
    # Corner columns — stop one row short so the player can walk in at street level.
    for wy in range(sy - h, sy - 1):
        if 0 <= wy < world.height:
            world.set_block(left_x, wy, wall_block)
            world.set_block(left_x + width - 1, wy, wall_block)

    # Capitals just above each column.
    cap_y = sy - h
    if 0 <= cap_y < world.height:
        world.set_block(left_x, cap_y, DORIC_CAPITAL)
        world.set_block(left_x + width - 1, cap_y, DORIC_CAPITAL)

    # Lintel running across the top.
    lintel_y = cap_y - 1
    if 0 <= lintel_y < world.height:
        for rx in range(left_x, left_x + width):
            world.set_block(rx, lintel_y, ARCH_STONE)

    # Peaked roof over the lintel.
    half = max(1, width // 2)
    for row in range(half + 1):
        row_y = lintel_y - 1 - row
        if not (0 <= row_y < world.height):
            break
        for rx in range(left_x + row, left_x + width - row):
            if 0 <= rx < world.width:
                world.set_block(rx, row_y, roof_block)

    # A bench inside, as bg, so the pavilion reads as a sit-down spot.
    bench_y = sy - 1
    if 0 <= bench_y < world.height:
        for wx in range(left_x + 1, left_x + width - 1):
            if world.get_block(wx, bench_y) == AIR:
                world.set_bg_block(wx, bench_y, GREEK_STONE_BENCH)


def _place_well(world, left_x, sy, width, wall_height):
    """Stone well: low walls around a shaft with a peaked wood canopy on posts."""
    if width < 3:
        width = 3
    # Low stone wellhead around the centre column (centre stays open).
    # Edges are bg so the player can walk up to the well without collision.
    well_y = sy - 1
    if 0 <= well_y < world.height:
        world.set_bg_block(left_x, well_y, COBBLESTONE)
        world.set_bg_block(left_x + width - 1, well_y, COBBLESTONE)
        for wx in range(left_x + 1, left_x + width - 1):
            if world.get_block(wx, well_y) == AIR:
                world.set_bg_block(wx, well_y, COBBLESTONE)

    # Two timber posts holding up the canopy.
    post_h = max(2, wall_height - 1)
    for dy in range(1, post_h + 1):
        wy = sy - 1 - dy
        if 0 <= wy < world.height:
            world.set_block(left_x, wy, HOUSE_WALL_DARK)
            world.set_block(left_x + width - 1, wy, HOUSE_WALL_DARK)

    # Peaked canopy.
    canopy_y = sy - 1 - post_h - 1
    if 0 <= canopy_y < world.height:
        for rx in range(left_x - 1, left_x + width + 1):
            world.set_block(rx, canopy_y, HOUSE_ROOF)
    peak_y = canopy_y - 1
    if 0 <= peak_y < world.height:
        for rx in range(left_x, left_x + width):
            world.set_block(rx, peak_y, HOUSE_ROOF)

    # Bucket dangling under the canopy as a bg block.
    bucket_y = canopy_y + 1
    bucket_x = left_x + width // 2
    if 0 <= bucket_y < world.height and world.get_block(bucket_x, bucket_y) == AIR:
        world.set_bg_block(bucket_x, bucket_y, RAIN_BARREL)


def _decorate_interior(world, rng, left_x, sy, width, npc_col):
    """Replace the inside floor with a rug and pin a tapestry behind the back wall.

    The rug becomes the floor block (still solid, so the NPC stands on it).
    The tapestry is placed as a background block so it shows through the
    air-filled interior without obstructing movement.
    """
    if width < 4:
        return
    rug_block = rng.choice(_INTERIOR_RUGS)
    if 0 <= sy < world.height:
        for wx in range(left_x + 1, left_x + width - 1):
            if world.get_block(wx, sy) == STONE:
                world.set_block(wx, sy, rug_block)

    tapestry_block = rng.choice(_INTERIOR_TAPESTRIES)
    tap_x = left_x + width - 2
    if tap_x == npc_col:
        tap_x = left_x + 2
    tap_y = sy - 3
    if 0 <= tap_y < world.height and world.get_block(tap_x, tap_y) == AIR:
        world.set_bg_block(tap_x, tap_y, tapestry_block)


def _decorate_facade(world, rng, left_x, sy, width, wall_height, wall_block):
    """Add a carved shutter window and a flower box ledge to the front facade."""
    # Carve one of the upper-mid wall blocks into a shuttered window on each side wall.
    win_y = sy - wall_height + 2
    if 0 <= win_y < world.height:
        for bx in (left_x, left_x + width - 1):
            if world.get_block(bx, win_y) == wall_block:
                world.set_block(bx, win_y, CARVED_SHUTTER)

    # Flower-box ledge as a background block adjacent to each side wall — purely visual.
    box_block = rng.choice(_FACADE_FLOWER_BOXES)
    ledge_y = win_y + 1
    if 0 <= ledge_y < world.height:
        for bx, dx in ((left_x, -1), (left_x + width - 1, 1)):
            adj = bx + dx
            if world.get_block(adj, ledge_y) == AIR:
                world.set_bg_block(adj, ledge_y, box_block)

    # Hanging basket as a bg block hanging just under the eaves — outside the door arch.
    basket_y = sy - wall_height
    for bx in (left_x - 1, left_x + width):
        if 0 <= basket_y < world.height and world.get_block(bx, basket_y) == AIR:
            world.set_bg_block(bx, basket_y, HANGING_BASKET)


def _place_tower(world, left_x, sy, width, wall_height,
                 wall_block=HOUSE_WALL_STONE, roof_block=HOUSE_ROOF_STONE):
    """Tall narrow building with crenelated battlements and an iron-grille window."""
    tower_h = wall_height + 3
    for wy in range(sy - tower_h, sy):
        for wx in range(left_x, left_x + width):
            if not (0 <= wy < world.height):
                continue
            is_left  = (wx == left_x)
            is_right = (wx == left_x + width - 1)
            # 4-row opening so players approaching from terrain up to 3 blocks
            # above the city floor can still walk through without hitting solid wall.
            is_door  = (wy >= sy - 4) and (is_left or is_right)
            if is_door:
                world.set_block(wx, wy, WOOD_DOOR_OPEN)
            elif is_left or is_right:
                world.set_block(wx, wy, wall_block)
            else:
                world.set_block(wx, wy, AIR)
                world.set_bg_block(wx, wy, wall_block)

    # Iron-grille window mid-tower
    win_y = sy - tower_h + 2
    win_x = left_x + width // 2
    if 0 <= win_y < world.height:
        world.set_block(win_x, win_y, WROUGHT_IRON_GRILLE)

    # Crenelated battlements: alternating wall and air across the top.
    crown_y = sy - tower_h
    if 0 <= crown_y < world.height:
        for i, wx in enumerate(range(left_x - 1, left_x + width + 1)):
            if i % 2 == 0:
                world.set_block(wx, crown_y, roof_block)
    # Solid roof slab one row down so the inside is sealed.
    slab_y = crown_y + 1
    if 0 <= slab_y < world.height:
        for wx in range(left_x, left_x + width):
            world.set_block(wx, slab_y, roof_block)


def _place_longhouse(world, left_x, sy, width, wall_height,
                     wall_block=HOUSE_WALL, roof_block=HOUSE_ROOF):
    """Wide, low building with a stretched flat roof and shutter accents."""
    h = max(3, wall_height - 1)
    _place_house(world, left_x, sy, width, h, wall_block, roof_block)
    # Shutter pairs as bg accents along the long facade — visual only,
    # so they never block the inside of the longhouse.
    shutter_y = sy - h + 1
    if 0 <= shutter_y < world.height:
        for wx in range(left_x + 2, left_x + width - 2, 2):
            if world.get_block(wx, shutter_y) == AIR:
                world.set_bg_block(wx, shutter_y, CARVED_SHUTTER)


def _place_market_stall(world, rng, left_x, sy, width, wall_height):
    """Open-front market stall: two timber posts, a striped awning, a counter.

    The NPC inside is fully visible — the stall is just visual framing.
    """
    h = max(2, min(3, wall_height - 1))
    awning_block = rng.choice(_INTERIOR_TAPESTRIES)

    # Side posts — stop one row short of the ground so the player can walk in freely.
    for wy in range(sy - h, sy - 1):
        if 0 <= wy < world.height:
            world.set_block(left_x, wy, HOUSE_WALL_DARK)
            world.set_block(left_x + width - 1, wy, HOUSE_WALL_DARK)

    # Striped awning across the top, with overhang.
    awning_y = sy - h
    if 0 <= awning_y < world.height:
        for wx in range(left_x - 1, left_x + width + 1):
            world.set_block(wx, awning_y, awning_block)

    # Pendant valance dangling under the awning — bg only so it doesn't block entry.
    valance_y = awning_y + 1
    if 0 <= valance_y < world.height:
        for wx in range(left_x + 1, left_x + width - 1):
            if world.get_block(wx, valance_y) == AIR:
                world.set_bg_block(wx, valance_y, awning_block)

    # Counter / table along the front, also bg so the player can step in.
    counter_y = sy - 1
    counter_block = rng.choice((GARDEN_TABLE, SYMPOSIUM_TABLE))
    if 0 <= counter_y < world.height:
        for wx in range(left_x + 1, left_x + width - 1):
            if world.get_block(wx, counter_y) == AIR:
                world.set_bg_block(wx, counter_y, counter_block)


def _place_ruin(world, left_x, sy, width, wall_height):
    """Partial walls of weathered cobblestone — looks abandoned, no door, no roof.

    Loose rubble inside the footprint is placed as background so the player
    can walk through what's left of the building.
    """
    for wy in range(sy - wall_height, sy):
        for wx in range(left_x, left_x + width):
            if not (0 <= wy < world.height):
                continue
            is_left  = (wx == left_x)
            is_right = (wx == left_x + width - 1)
            # Top half of the side walls is broken away; bottom 2 rows are also
            # open so the player can walk through without being blocked.
            broken_top  = wy < sy - wall_height + 2
            broken_base = wy >= sy - 2
            if (is_left or is_right) and not broken_top and not broken_base:
                world.set_block(wx, wy, COBBLESTONE)
            else:
                world.set_block(wx, wy, AIR)
                world.set_bg_block(wx, wy, COBBLESTONE)
    # Scattered rubble — bg only so the ruin stays walkable.
    for wx in (left_x + 1, left_x + width // 2, left_x + width - 2):
        floor_y = sy - 1
        if 0 <= floor_y < world.height and world.get_block(wx, floor_y) == AIR:
            world.set_bg_block(wx, floor_y, COBBLESTONE)


def _place_house(world, left_x, sy, width, wall_height,
                 wall_block=HOUSE_WALL, roof_block=HOUSE_ROOF):
    """Hollow enterable house with doors on BOTH sides for city passthrough."""
    for wy in range(sy - wall_height, sy):
        for wx in range(left_x, left_x + width):
            if not (0 <= wy < world.height):
                continue
            is_top        = (wy == sy - wall_height)
            is_left_side  = (wx == left_x)
            is_right_side = (wx == left_x + width - 1)
            is_door_row   = (wy >= sy - 2)
            is_left_door  = is_left_side  and is_door_row
            is_right_door = is_right_side and is_door_row

            if is_left_door or is_right_door:
                world.set_block(wx, wy, WOOD_DOOR_OPEN)
            elif is_top or is_left_side or is_right_side:
                world.set_block(wx, wy, wall_block)
            else:
                world.set_block(wx, wy, AIR)
                world.set_bg_block(wx, wy, wall_block)

    # Flat roof overhang (1 block wider each side)
    roof_y = sy - wall_height - 1
    for rx in range(left_x - 1, left_x + width + 1):
        if 0 <= roof_y < world.height:
            world.set_block(rx, roof_y, roof_block)

    # Peaked ridge
    peak_y = roof_y - 1
    for rx in range(left_x, left_x + width):
        if 0 <= peak_y < world.height:
            world.set_block(rx, peak_y, roof_block)


def _place_house_two_story(world, left_x, sy, width, floor1_h, floor2_h,
                            wall_block=HOUSE_WALL, roof_block=HOUSE_ROOF):
    """Two-story building. Ground floor has doors on both sides; upper floor via ladder."""
    ladder_col = left_x + width - 2  # one column from right wall

    # Ground floor
    for wy in range(sy - floor1_h, sy):
        for wx in range(left_x, left_x + width):
            if not (0 <= wy < world.height):
                continue
            is_ceiling    = (wy == sy - floor1_h)
            is_left_side  = (wx == left_x)
            is_right_side = (wx == left_x + width - 1)
            is_door_row   = (wy >= sy - 2)
            is_left_door  = is_left_side  and is_door_row
            is_right_door = is_right_side and is_door_row
            is_ladder_pos = (wx == ladder_col)
            is_hole       = (is_ceiling and is_ladder_pos)

            if is_left_door or is_right_door:
                world.set_block(wx, wy, WOOD_DOOR_OPEN)
            elif is_hole:
                # Opening in ceiling for ladder passthrough
                world.set_block(wx, wy, LADDER)
                world.set_bg_block(wx, wy, wall_block)
            elif is_ceiling or is_left_side or is_right_side:
                world.set_block(wx, wy, wall_block)
            elif is_ladder_pos:
                world.set_block(wx, wy, LADDER)
                world.set_bg_block(wx, wy, wall_block)
            else:
                world.set_block(wx, wy, AIR)
                world.set_bg_block(wx, wy, wall_block)

    # Upper floor
    for wy in range(sy - floor1_h - floor2_h, sy - floor1_h):
        for wx in range(left_x, left_x + width):
            if not (0 <= wy < world.height):
                continue
            is_top        = (wy == sy - floor1_h - floor2_h)
            is_left_side  = (wx == left_x)
            is_right_side = (wx == left_x + width - 1)

            if is_top or is_left_side or is_right_side:
                world.set_block(wx, wy, wall_block)
            elif wx == ladder_col:
                world.set_block(wx, wy, LADDER)
                world.set_bg_block(wx, wy, wall_block)
            else:
                world.set_block(wx, wy, AIR)
                world.set_bg_block(wx, wy, wall_block)

    # Flat roof overhang
    roof_y = sy - floor1_h - floor2_h - 1
    for rx in range(left_x - 1, left_x + width + 1):
        if 0 <= roof_y < world.height:
            world.set_block(rx, roof_y, roof_block)

    # Peaked ridge
    peak_y = roof_y - 1
    for rx in range(left_x, left_x + width):
        if 0 <= peak_y < world.height:
            world.set_block(rx, peak_y, roof_block)


def _place_restaurant(world, left_x, sy, width, wall_height, style="default"):
    """Restaurant: hollow interior, doors on both sides, flat cultural awning."""
    wall_block, awning_block = _RESTAURANT_STYLES.get(style, _RESTAURANT_STYLES["default"])
    for wy in range(sy - wall_height, sy):
        for wx in range(left_x, left_x + width):
            if not (0 <= wy < world.height):
                continue
            is_top        = (wy == sy - wall_height)
            is_left_side  = (wx == left_x)
            is_right_side = (wx == left_x + width - 1)
            is_door_row   = (wy >= sy - 2)
            is_left_door  = is_left_side  and is_door_row
            is_right_door = is_right_side and is_door_row

            if is_left_door or is_right_door:
                world.set_block(wx, wy, WOOD_DOOR_OPEN)
            elif is_top or is_left_side or is_right_side:
                world.set_block(wx, wy, wall_block)
            else:
                world.set_block(wx, wy, AIR)
                world.set_bg_block(wx, wy, wall_block)

    # Flat awning overhang (wider than normal, no peak — distinctive canopy look)
    awning_y = sy - wall_height - 1
    for rx in range(left_x - 2, left_x + width + 2):
        if 0 <= awning_y < world.height:
            world.set_block(rx, awning_y, awning_block)


def _place_temple(world, left_x, sy, width, wall_height):
    """Wide stone temple with a 3-tier pagoda-style roof."""
    # Walls and hollow interior
    for wy in range(sy - wall_height, sy):
        for wx in range(left_x, left_x + width):
            if not (0 <= wy < world.height):
                continue
            is_top        = (wy == sy - wall_height)
            is_left_side  = (wx == left_x)
            is_right_side = (wx == left_x + width - 1)
            is_door_row   = (wy >= sy - 2)
            # Wide double-door entrance on both sides
            is_left_door  = is_left_side  and is_door_row
            is_right_door = is_right_side and is_door_row
            is_left_door2  = (wx == left_x + 1) and is_door_row
            is_right_door2 = (wx == left_x + width - 2) and is_door_row

            if is_left_door or is_right_door or is_left_door2 or is_right_door2:
                world.set_block(wx, wy, WOOD_DOOR_OPEN)
            elif is_top or is_left_side or is_right_side:
                world.set_block(wx, wy, HOUSE_WALL_STONE)
            else:
                world.set_block(wx, wy, AIR)
                world.set_bg_block(wx, wy, HOUSE_WALL_STONE)

    # 3-tier pagoda roof — each tier narrows by 1 block per side and adds 1 row
    base_y = sy - wall_height - 1
    for tier in range(3):
        tier_y = base_y - tier * 2
        shrink = tier
        for rx in range(left_x - 1 + shrink, left_x + width + 1 - shrink):
            if 0 <= tier_y < world.height:
                world.set_block(rx, tier_y, HOUSE_ROOF_STONE)
        peak_y = tier_y - 1
        for rx in range(left_x + shrink, left_x + width - shrink):
            if 0 <= peak_y < world.height:
                world.set_block(rx, peak_y, HOUSE_ROOF_STONE)


def _place_dome_house(world, left_x, sy, width, wall_height,
                      wall_block=SANDSTONE_BLOCK, dome_block=POLISHED_MARBLE):
    """Desert dome building: sandstone box walls topped with a white marble semicircle."""
    center_x = left_x + width // 2

    for wy in range(sy - wall_height, sy):
        for wx in range(left_x, left_x + width):
            if not (0 <= wy < world.height):
                continue
            is_left       = (wx == left_x)
            is_right      = (wx == left_x + width - 1)
            is_door_row   = (wy >= sy - 2)
            is_left_door  = is_left  and is_door_row
            is_right_door = is_right and is_door_row

            if is_left_door or is_right_door:
                world.set_block(wx, wy, WOOD_DOOR_OPEN)
            elif is_left or is_right:
                world.set_block(wx, wy, wall_block)
            else:
                world.set_block(wx, wy, AIR)
                world.set_bg_block(wx, wy, wall_block)

    # Semicircular dome — radius = half of building width
    radius = width // 2
    dome_base_y = sy - wall_height - 1
    for row in range(radius + 1):
        half_w = int((radius * radius - row * row) ** 0.5)
        row_y  = dome_base_y - row
        if not (0 <= row_y < world.height):
            break
        for dx in range(-half_w, half_w + 1):
            rx = center_x + dx
            if 0 <= rx < world.width:
                world.set_block(rx, row_y, dome_block)


def _place_chapel(world, left_x, sy, width, wall_height):
    """Wood chapel with a single center door and a tall triangular gabled roof."""
    center = left_x + width // 2
    for wy in range(sy - wall_height, sy):
        for wx in range(left_x, left_x + width):
            if not (0 <= wy < world.height):
                continue
            is_top        = (wy == sy - wall_height)
            is_left_side  = (wx == left_x)
            is_right_side = (wx == left_x + width - 1)
            is_door_row   = (wy >= sy - 2)
            is_left_door  = is_left_side  and is_door_row
            is_right_door = is_right_side and is_door_row
            is_center_door = (wx == center) and is_door_row

            if is_left_door or is_right_door or is_center_door:
                world.set_block(wx, wy, WOOD_DOOR_OPEN)
            elif is_top or is_left_side or is_right_side:
                world.set_block(wx, wy, HOUSE_WALL)
            else:
                world.set_block(wx, wy, AIR)
                world.set_bg_block(wx, wy, HOUSE_WALL)

    # Tall triangular gabled roof — each row narrows by 1 per side until 1 block wide
    base_y = sy - wall_height - 1
    half = width // 2 + 1
    for row in range(half):
        row_y = base_y - row
        if not (0 <= row_y < world.height):
            break
        for rx in range(left_x - 1 + row, left_x + width + 1 - row):
            if 0 <= rx < world.width:
                world.set_block(rx, row_y, HOUSE_ROOF)

    # Bell tower: one column above the roof peak, in background so it doesn't block movement
    peak_y = base_y - half
    for by in range(peak_y - 2, peak_y):
        if 0 <= by < world.height:
            world.set_bg_block(center, by, HOUSE_WALL)


def _place_desert_shrine(world, left_x, sy, width, wall_height):
    """Open-sided shrine with stone columns and a wide flat overhanging roof."""
    col_positions = {left_x, left_x + width // 2, left_x + width - 1}
    for wy in range(sy - wall_height, sy):
        for wx in range(left_x, left_x + width):
            if not (0 <= wy < world.height):
                continue
            if wx in col_positions:
                # Ground row is bg so the player can walk through the column bases.
                if wy == sy - 1:
                    world.set_bg_block(wx, wy, HOUSE_WALL_BRICK)
                else:
                    world.set_block(wx, wy, HOUSE_WALL_BRICK)
            else:
                world.set_block(wx, wy, AIR)
                world.set_bg_block(wx, wy, HOUSE_WALL_STONE)

    # Double-layer flat roof with wide overhang
    for roof_y, overhang in ((sy - wall_height - 1, 1), (sy - wall_height - 2, 2)):
        if 0 <= roof_y < world.height:
            for rx in range(left_x - overhang, left_x + width + overhang):
                if 0 <= rx < world.width:
                    world.set_block(rx, roof_y, HOUSE_WALL_STONE)


def _place_jungle_shrine(world, left_x, sy, width, wall_height):
    """Solid stone stepped pyramid narrowing toward a single capstone."""
    steps = min(wall_height, (width // 2) + 1)
    for step in range(steps):
        step_y = sy - step - 1
        if not (0 <= step_y < world.height):
            break
        for wx in range(left_x + step, left_x + width - step):
            if 0 <= wx < world.width:
                # Base row is bg so the player can walk up to the shrine NPC.
                if step_y == sy - 1:
                    world.set_bg_block(wx, step_y, HOUSE_WALL_STONE)
                else:
                    world.set_block(wx, step_y, HOUSE_WALL_STONE)

    # Capstone above pyramid tip
    cap_y = sy - steps - 1
    mid   = left_x + width // 2
    if 0 <= cap_y < world.height:
        world.set_block(mid, cap_y, HOUSE_ROOF_STONE)


def _place_standing_stones(world, left_x, sy, width, wall_height):
    """Three tall stone pillars — shorter at edges, tallest at center."""
    positions = [left_x, left_x + width // 2, left_x + width - 1]
    heights   = [wall_height - 1, wall_height + 1, wall_height - 1]
    for sx, h in zip(positions, heights):
        if not (0 <= sx < world.width):
            continue
        for wy in range(sy - h, sy):
            if 0 <= wy < world.height:
                # Ground row is bg so the player can walk up to the shrine NPC.
                if wy == sy - 1:
                    world.set_bg_block(sx, wy, HOUSE_WALL_STONE)
                else:
                    world.set_block(sx, wy, HOUSE_WALL_STONE)
        # Flat capstone block
        cap_y = sy - h - 1
        if 0 <= cap_y < world.height:
            world.set_block(sx, cap_y, HOUSE_ROOF_STONE)


def _place_himalayan_house(world, left_x, sy, width, wall_height):
    """Himalayan building: MANI_STONE base, whitewashed walls, flat roof + prayer flags."""
    stone_rows = min(2, wall_height - 2)

    for wy in range(sy - wall_height, sy):
        for wx in range(left_x, left_x + width):
            if not (0 <= wy < world.height):
                continue
            is_top        = (wy == sy - wall_height)
            is_left_side  = (wx == left_x)
            is_right_side = (wx == left_x + width - 1)
            is_door_row   = (wy >= sy - 2)
            is_left_door  = is_left_side  and is_door_row
            is_right_door = is_right_side and is_door_row
            is_stone_base = (wy >= sy - stone_rows)

            use_block = MANI_STONE if is_stone_base else WHITEWASHED_WALL

            if is_left_door or is_right_door:
                world.set_block(wx, wy, WOOD_DOOR_OPEN)
            elif is_top or is_left_side or is_right_side:
                world.set_block(wx, wy, use_block)
            else:
                world.set_block(wx, wy, AIR)
                world.set_bg_block(wx, wy, use_block)

    # Flat roof with slight overhang — characteristic Himalayan silhouette
    roof_y = sy - wall_height - 1
    for rx in range(left_x - 1, left_x + width + 1):
        if 0 <= roof_y < world.height and abs(rx) < world.width:
            world.set_block(rx, roof_y, MONASTERY_ROOF)

    # Prayer flags along the roof ridge
    flag_y = roof_y - 1
    for fx in range(left_x, left_x + width, 2):
        if 0 <= flag_y < world.height and abs(fx) < world.width:
            world.set_block(fx, flag_y, PRAYER_FLAG_BLOCK)


def _place_dzong(world, left_x, sy, width, wall_height):
    """Himalayan fortress-monastery (Dzong): battered stone base, white upper walls, tiered roof."""
    stone_split = wall_height * 2 // 3  # lower portion in MANI_STONE

    for wy in range(sy - wall_height, sy):
        for wx in range(left_x, left_x + width):
            if not (0 <= wy < world.height):
                continue
            is_stone_half = (wy >= sy - stone_split)
            wall_blk      = MANI_STONE if is_stone_half else WHITEWASHED_WALL
            is_left_wall  = (wx <= left_x + 1)
            is_right_wall = (wx >= left_x + width - 2)
            is_top        = (wy == sy - wall_height)
            is_door_row   = (wy >= sy - 2)
            # Wide double-door entrance on both sides
            is_left_door  = is_door_row and wx == left_x
            is_left_door2 = is_door_row and wx == left_x + 1
            is_right_door  = is_door_row and wx == left_x + width - 1
            is_right_door2 = is_door_row and wx == left_x + width - 2

            if is_left_door or is_left_door2 or is_right_door or is_right_door2:
                world.set_block(wx, wy, WOOD_DOOR_OPEN)
            elif is_top or is_left_wall or is_right_wall:
                world.set_block(wx, wy, wall_blk)
            else:
                world.set_block(wx, wy, AIR)
                world.set_bg_block(wx, wy, wall_blk)

    # 3-tier monastery roof — each tier slightly narrower
    base_y = sy - wall_height - 1
    for tier in range(3):
        tier_y = base_y - tier * 2
        shrink = tier
        for rx in range(left_x - 1 + shrink, left_x + width + 1 - shrink):
            if 0 <= tier_y < world.height and abs(rx) < world.width:
                world.set_block(rx, tier_y, MONASTERY_ROOF)
        fill_y = tier_y + 1
        for rx in range(left_x + shrink, left_x + width - shrink):
            if 0 <= fill_y < world.height and abs(rx) < world.width:
                world.set_block(rx, fill_y, MONASTERY_ROOF)

    # Prayer flags strung across the top
    flag_y = base_y - 7
    for fx in range(left_x, left_x + width):
        if 0 <= flag_y < world.height and abs(fx) < world.width:
            world.set_block(fx, flag_y, PRAYER_FLAG_BLOCK)


def _place_shrine_for_biome(world, left_x, sy, width, wall_height, biodome):
    _, style = RELIGION_BY_BIOME.get(biodome, ("Forest Chapel", "chapel"))
    if style == "dzong":
        _place_dzong(world, left_x, sy, width, wall_height)
    elif style == "chapel":
        _place_chapel(world, left_x, sy, width, wall_height)
    elif style == "desert_shrine":
        _place_desert_shrine(world, left_x, sy, width, wall_height)
    elif style == "jungle_shrine":
        _place_jungle_shrine(world, left_x, sy, width, wall_height)
    elif style == "standing_stones":
        _place_standing_stones(world, left_x, sy, width, wall_height)
    else:
        _place_temple(world, left_x, sy, width, wall_height)


_TRAVERSAL_THRESHOLD = 3   # height diff (blocks) below which no stairs are needed
_TRAVERSAL_MAX_STEPS = 25  # cap so extreme terrain doesn't create absurd staircases


def _ensure_city_traversal(world, city_bx, half_w, sy):
    """Guarantee the player can enter and exit the city on each side.

    Per-side logic:
      - City elevated above terrain → build a rising stone-supported ramp toward the city.
      - City below terrain (mountain wall) → carve a descending ramp through the hillside.
    Stair block direction is chosen so the ascending direction always uses a stair trigger.
    """
    def _side(edge_x, outward):
        # Sample the first terrain column outside the city edge.
        terrain_sy = world.surface_y_at(edge_x + outward)
        diff = terrain_sy - sy      # positive = terrain lower; negative = terrain higher
        if abs(diff) <= _TRAVERSAL_THRESHOLD:
            return
        steps = min(abs(diff), _TRAVERSAL_MAX_STEPS)

        far_x = edge_x + outward * (steps + 2)
        chunk_lo = min(edge_x, far_x) // CHUNK_W - 1
        chunk_hi = max(edge_x, far_x) // CHUNK_W + 1
        for c in range(chunk_lo, chunk_hi + 1):
            world.load_chunk(c)

        if diff > 0:
            # City is elevated: build a ramp rising toward the city.
            # Ascending direction = toward city, so use stair that triggers movement toward city.
            # Left side (outward=-1): player moves right toward city → STAIRS_RIGHT.
            # Right side (outward=+1): player moves left toward city → STAIRS_LEFT.
            stair_block = STAIRS_RIGHT if outward == -1 else STAIRS_LEFT
            for i in range(steps):
                sx      = edge_x + outward * (1 + i)
                stair_y = sy + i        # descends (y grows) as we step away from city
                world.set_block(sx, stair_y, stair_block)
                for h in range(1, 3):
                    if world.get_block(sx, stair_y - h) not in (AIR, BEDROCK):
                        world.set_block(sx, stair_y - h, AIR)
                for fill_y in range(stair_y + 1, terrain_sy + 1):
                    if world.get_block(sx, fill_y) == AIR:
                        world.set_block(sx, fill_y, STONE)
        else:
            # City is below terrain: carve a ramp through the hillside.
            # Ascending direction = away from city, so use stair that triggers movement away.
            # Left side (outward=-1): player exits left → STAIRS_LEFT.
            # Right side (outward=+1): player exits right → STAIRS_RIGHT.
            stair_block = STAIRS_LEFT if outward == -1 else STAIRS_RIGHT
            for i in range(steps):
                sx      = edge_x + outward * (1 + i)
                # Start at sy-1 (player row when at city floor) so the first stair fires.
                # Ascending outward; i=steps-1 lands at terrain_sy (mountain surface, cleared below).
                stair_y = sy - 1 - i
                world.set_block(sx, stair_y, stair_block)
                for h in range(1, 3):
                    if world.get_block(sx, stair_y - h) not in (AIR, BEDROCK):
                        world.set_block(sx, stair_y - h, AIR)
                # No fill needed — mountain stone below is already solid.

    _side(city_bx - half_w, -1)   # left exit
    _side(city_bx + half_w, +1)   # right exit


def _build_single_city(world, rng, city_bx, difficulty):
    sy = world.surface_y_at(city_bx)
    biodome = world.biodome_at(city_bx)
    city_size = rng.choice(_SIZE_BY_DIFFICULTY[difficulty])
    cfg = CITY_CONFIGS[city_size]
    half_w = cfg["half_w"]

    world.city_zones.append((city_bx - half_w, city_bx + half_w))

    # Pre-load every chunk the city footprint + farm strips touch
    chunk_lo = (city_bx - half_w - 20) // CHUNK_W
    chunk_hi = (city_bx + half_w + 20) // CHUNK_W
    for c_idx in range(chunk_lo, chunk_hi + 1):
        world.load_chunk(c_idx)

    for bx in range(city_bx - half_w - 2, city_bx + half_w + 3):
        for by in range(max(0, sy - 35), sy):
            if world.get_block(bx, by) in _PLANT_BLOCKS:
                world.set_block(bx, by, AIR)

    # Flatten terrain across the city footprint to sy
    for bx in range(city_bx - half_w, city_bx + half_w + 1):
        col_sy = world.surface_y_at(bx)
        # Hill: remove blocks above city floor
        for by in range(col_sy, sy):
            blk = world.get_block(bx, by)
            if blk not in (AIR, BEDROCK):
                world.set_block(bx, by, AIR)
        # Valley: fill gaps below city floor with stone
        for by in range(sy, col_sy + 1):
            if world.get_block(bx, by) == AIR:
                world.set_block(bx, by, STONE)

    for bx in range(city_bx - half_w, city_bx + half_w + 1):
        if world.get_block(bx, sy) != BEDROCK:
            world.set_block(bx, sy, STONE)

    is_desert        = biodome in _DESERT_BIOMES
    is_himalayan     = biodome in _HIMALAYAN_BIOMES
    is_mediterranean = biodome in _MEDITERRANEAN_BIOMES
    is_east_asian    = biodome in _EAST_ASIAN_BIOMES
    is_south_asian   = biodome in _SOUTH_ASIAN_BIOMES
    restaurant_style = _RESTAURANT_STYLE_BY_BIOME.get(biodome, "default")

    for (offset, w_range, h_range, variants), npc_type in zip(cfg["buildings"], cfg["npc_types"]):
        left_x = city_bx + offset
        if is_desert:
            wall_block, roof_block = _DESERT_PALETTE
            if variants:
                variants = [_DOME_SWAP.get(v, v) for v in variants]
        elif is_himalayan:
            wall_block, roof_block = _HIMALAYAN_PALETTE
            if variants:
                variants = [_HIMALAYAN_SWAP.get(v, v) for v in variants]
        elif is_mediterranean:
            wall_block, roof_block = rng.choice(_MEDITERRANEAN_PALETTES)
        elif is_east_asian:
            wall_block, roof_block = _EAST_ASIAN_PALETTE
            if variants:
                variants = [_EAST_ASIAN_SWAP.get(v, v) for v in variants]
        elif is_south_asian:
            wall_block, roof_block = rng.choice(_SOUTH_ASIAN_PALETTES)
        else:
            wall_block, roof_block = rng.choice(BUILDING_PALETTES)

        if w_range is None:
            npc_bx = left_x
        else:
            width   = rng.randint(*w_range)
            height  = rng.randint(*h_range)
            variant = rng.choice(variants) if variants else "house"

            if variant == "dome":
                _place_dome_house(world, left_x, sy, width, height, wall_block)
            elif variant == "himalayan":
                _place_himalayan_house(world, left_x, sy, width, height)
            elif variant == "two_story":
                floor2_h = rng.randint(2, 3)
                _place_house_two_story(world, left_x, sy, width, height, floor2_h,
                                       wall_block, roof_block)
            elif variant == "restaurant":
                _place_restaurant(world, left_x, sy, width, height, restaurant_style)
            elif variant == "shrine":
                _place_shrine_for_biome(world, left_x, sy, width, height, biodome)
            elif variant == "tower":
                _place_tower(world, left_x, sy, width, height, wall_block, roof_block)
            elif variant == "longhouse":
                _place_longhouse(world, left_x, sy, width, height, wall_block, roof_block)
            elif variant == "ruin":
                _place_ruin(world, left_x, sy, width, height)
            elif variant == "market_stall":
                _place_market_stall(world, rng, left_x, sy, width, height)
            elif variant == "pavilion":
                _place_pavilion(world, left_x, sy, width, height,
                                GARDEN_COLUMN, roof_block)
            elif variant == "well":
                _place_well(world, left_x, sy, width, height)
            else:
                _place_house(world, left_x, sy, width, height, wall_block, roof_block)

            npc_bx = left_x + 1

            # Decorate finished houses (skip ruins, restaurants, shrines, exotic styles)
            if variant in ("house", "two_story", "longhouse", "tower"):
                _decorate_interior(world, rng, left_x, sy, width, npc_bx)
                _decorate_facade(world, rng, left_x, sy, width, height, wall_block)

        npc_px = npc_bx * BLOCK_SIZE + (BLOCK_SIZE - NPC.NPC_W) // 2
        npc_py = (sy - 2) * BLOCK_SIZE

        if npc_type == "quest_rock":
            world.entities.append(RockQuestNPC(npc_px, npc_py, world, rng, difficulty, biodome))
        elif npc_type == "trade":
            world.entities.append(TradeNPC(npc_px, npc_py, world, rng, biodome))
        elif npc_type == "quest_wildflower":
            world.entities.append(WildflowerQuestNPC(npc_px, npc_py, world, rng, difficulty, biodome))
        elif npc_type == "quest_gem":
            world.entities.append(GemQuestNPC(npc_px, npc_py, world, rng, difficulty, biodome))
        elif npc_type == "merchant":
            world.entities.append(MerchantNPC(npc_px, npc_py, world, rng, biodome))
        elif npc_type == "restaurant_npc":
            world.entities.append(RestaurantNPC(npc_px, npc_py, world, rng, biodome))
        elif npc_type == "shrine_npc":
            world.entities.append(ShrineKeeperNPC(npc_px, npc_py, world, rng, difficulty, biodome))
        elif npc_type == "jewelry_merchant":
            world.entities.append(JewelryMerchantNPC(npc_px, npc_py, world, rng, biodome))

    # Town squares — paved plazas with a sculpture centerpiece, around outdoor NPC slots.
    for offset, half in cfg.get("squares", ()):
        _place_town_square(world, rng, city_bx + offset, sy, biodome, half)

    # Small towns with no square still need a flag at the city center.
    if not cfg.get("squares"):
        flag_y = sy - 1
        if 0 <= flag_y < world.height:
            world.set_bg_block(city_bx, flag_y, TOWN_FLAG_BLOCK)

    # Garden plots between buildings — placed last so they don't get overwritten.
    for offset, half in cfg.get("gardens", ()):
        _place_garden_plot(world, rng, city_bx + offset, sy, biodome, half)

    # Farm plots flanking the city, with farmer NPCs working the fields.
    _ambient_npc_cls = {"villager": VillagerNPC, "child": ChildNPC, "guard": GuardNPC}
    for offset, farm_half in cfg.get("farms", ()):
        farm_cx = city_bx + offset
        _place_farm_plot(world, rng, farm_cx, sy, biodome, farm_half)
        for _ in range(rng.randint(1, 2)):
            fx = (farm_cx + rng.randint(-farm_half + 1, farm_half - 1)) * BLOCK_SIZE
            fy = (sy - 2) * BLOCK_SIZE
            world.entities.append(FarmerNPC(fx, fy, world,
                                            patrol_half=(farm_half - 1) * BLOCK_SIZE,
                                            biodome=biodome))

    # Ambient residents — villagers, children, guards — roaming the city streets.
    for offset, npc_type in cfg.get("ambient_npcs", ()):
        cls = _ambient_npc_cls.get(npc_type)
        if cls is None:
            continue
        nx = (city_bx + offset) * BLOCK_SIZE + (BLOCK_SIZE - NPC.NPC_W) // 2
        ny = (sy - 2) * BLOCK_SIZE
        world.entities.append(cls(nx, ny, world, biodome=biodome))

    # Cobbled main street + lamps + entry gateposts wrap up the city.
    _pave_main_street(world, rng, city_bx - half_w, city_bx + half_w, sy)
    _place_streetlamps(world, rng, city_bx - half_w + 2,
                       city_bx + half_w - 2, sy)
    _place_gateposts(world, rng, city_bx - half_w, city_bx + half_w, sy)
    _ensure_city_traversal(world, city_bx, half_w, sy)

    return city_size


def _castle_set(world, bx, by, bid):
    """Set a foreground block only if in-bounds."""
    if 0 <= by < world.height:
        world.set_block(bx, by, bid)


def _castle_bg(world, bx, by, bid):
    """Set a background block only if in-bounds."""
    if 0 <= by < world.height:
        world.set_bg_block(bx, by, bid)


def _castle_fill_bg(world, lx, rx, top_y, bot_y, bid):
    """Flood-fill a rectangle with background blocks."""
    for bx in range(lx, rx + 1):
        for by in range(top_y, bot_y + 1):
            if 0 <= by < world.height:
                world.set_bg_block(bx, by, bid)


def _castle_door(world, bx, sy):
    """Carve a 2-wide × 2-tall walkable archway at bx and bx+1."""
    for col in (bx, bx + 1):
        _castle_set(world, col, sy - 1, AIR)
        _castle_set(world, col, sy - 2, AIR)
        _castle_bg(world, col, sy - 1, CASTLE_GATE_ARCH)
        _castle_bg(world, col, sy - 2, CASTLE_GATE_ARCH)


def _build_round_tower(world, lx: int, sy: int, w: int, h: int):
    """A fully detailed corner tower: solid round-tower walls, mid-floor, corbels,
    machicolations, crenellations, conical cap, arrow slit, garderobe chute."""
    # Foundation
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy, CURTAIN_WALL)
    # Full-height outer walls
    for by in range(sy - h, sy):
        _castle_set(world, lx,      by, ROUND_TOWER_WALL)
        _castle_set(world, lx + w,  by, ROUND_TOWER_WALL)
    # Full interior background fill
    _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, ROUND_TOWER_WALL)
    # Door openings on both sides so players can flow through
    _castle_door(world, lx,         sy)   # left entrance
    _castle_door(world, lx + w - 1, sy)   # right exit
    # Mid-level interior floor
    mid_floor = sy - h // 2
    for bx in range(lx + 1, lx + w):
        _castle_set(world, bx, mid_floor, WALL_WALK_FLOOR)
    # Arrow slit + sconce on mid level
    tmid = lx + w // 2
    _castle_bg(world, tmid, mid_floor - 2, DUNGEON_GRATE)
    _castle_bg(world, tmid, mid_floor - 1, WALL_SCONCE)
    # Garderobe chute jutting from lower outer wall
    _castle_bg(world, lx,     sy - 4, GARDEROBE_CHUTE)
    # Corbel course just below parapet
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy - h + 1, CORBEL_COURSE)
    # Machicolations at parapet level
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy - h, MACHICOLATION)
    # Crenellations (alternating merlons)
    for bx in range(lx, lx + w + 1):
        if (bx - lx) % 2 == 0:
            _castle_set(world, bx, sy - h - 1, CRENELLATION)
    # Conical tower cap — pyramid of TOWER_CAP blocks
    for i, span in enumerate(range(w // 2 + 1, 0, -1)):
        cap_y = sy - h - 2 - i
        for bx in range(tmid - span + 1, tmid + span):
            _castle_set(world, bx, cap_y, TOWER_CAP)
    # Wall sconce inside at ground level
    _castle_bg(world, tmid, sy - 2, BRAZIER)


# ── Castle piece dimensions ────────────────────────────────────────────────
_CW_MOAT      = 4   # moat approach
_CW_ROUND_TOW = 6   # round tower
_CW_SQ_TOW    = 8   # square tower
_CW_GATEHOUSE = 7   # gatehouse
_CW_GREAT_HALL= 13  # great hall
_CW_GRAND_HALL= 15  # wide grand hall
_CW_KEEP      = 10  # standard keep
_CW_PAL_KEEP  = 12  # palace keep (wider)
_CW_CHAPEL    = 9   # chapel wing
_CW_BARRACKS  = 11  # barracks wing

_CH_ROUND_TOW = 17  # round tower height
_CH_SQ_TOW    = 14  # square tower height
_CH_WALL      = 11  # standard hall/wall height
_CH_KEEP      = 22  # keep height
_CH_PAL_KEEP  = 26  # palace keep height
_CH_CHAPEL    = 14  # chapel height


def _piece_moat(world, lx, sy):
    """Moat approach — drawbridge planks over damp stone flanks."""
    for bx in range(lx, lx + _CW_MOAT):
        _castle_set(world, bx, sy,     DRAWBRIDGE_PLANK)
        _castle_bg(world,  bx, sy,     DRAWBRIDGE_CHAIN)
        _castle_bg(world,  bx, sy - 1, MOAT_STONE)
        _castle_bg(world,  bx, sy - 2, MOAT_STONE)
    return _CW_MOAT


def _piece_round_tower(world, lx, sy):
    """Round tower with conical cap and gargoyle corners."""
    _build_round_tower(world, lx, sy, _CW_ROUND_TOW, _CH_ROUND_TOW)
    _castle_bg(world, lx,                sy - _CH_ROUND_TOW - 1, GARGOYLE_BLOCK)
    _castle_bg(world, lx + _CW_ROUND_TOW, sy - _CH_ROUND_TOW - 1, GARGOYLE_BLOCK)
    return _CW_ROUND_TOW


def _piece_square_tower(world, lx, sy):
    """Square keep-tower: flat battlements, arrow slits, two interior floors."""
    w, h = _CW_SQ_TOW, _CH_SQ_TOW
    cx = lx + w // 2
    _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, CURTAIN_WALL)
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy, CURTAIN_WALL)
    for by in range(sy - h, sy):
        _castle_set(world, lx,     by, CURTAIN_WALL)
        _castle_set(world, lx + w, by, CURTAIN_WALL)
    _castle_door(world, lx,         sy)
    _castle_door(world, lx + w - 1, sy)
    mid = sy - h // 2
    for bx in range(lx + 1, lx + w):
        _castle_set(world, bx, mid, WALL_WALK_FLOOR)
    _castle_bg(world, lx,     mid - 2, DUNGEON_GRATE)
    _castle_bg(world, lx + w, mid - 2, DUNGEON_GRATE)
    _castle_bg(world, cx, mid - 1, WALL_SCONCE)
    _castle_bg(world, cx, sy  - 3, BRAZIER)
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy - h + 1, CORBEL_COURSE)
        _castle_set(world, bx, sy - h,     MACHICOLATION)
        if (bx - lx) % 2 == 0:
            _castle_set(world, bx, sy - h - 1, CRENELLATION)
    _castle_bg(world, lx,     sy - h - 1, GARGOYLE_BLOCK)
    _castle_bg(world, lx + w, sy - h - 1, GARGOYLE_BLOCK)
    return w


def _piece_gatehouse(world, lx, sy):
    """Gatehouse with portcullis, murder holes, and battlements."""
    w, h = _CW_GATEHOUSE, _CH_WALL
    cx = lx + w // 2
    _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, CURTAIN_WALL)
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy, CURTAIN_WALL)
    for by in range(sy - h, sy):
        _castle_set(world, lx,     by, CURTAIN_WALL)
        _castle_set(world, lx + w, by, CURTAIN_WALL)
    for by in range(sy - 3, sy):
        _castle_bg(world, cx,     by, CASTLE_GATE_ARCH)
        _castle_bg(world, cx - 1, by, CASTLE_GATE_ARCH)
    _castle_bg(world, cx,     sy - 4, PORTCULLIS_BLOCK)
    _castle_bg(world, cx - 1, sy - 4, PORTCULLIS_BLOCK)
    _castle_bg(world, lx + 1,     sy - 2, DRAWBRIDGE_CHAIN)
    _castle_bg(world, lx + w - 1, sy - 2, DRAWBRIDGE_CHAIN)
    _castle_bg(world, lx + 1,     sy - 4, DRAWBRIDGE_CHAIN)
    _castle_bg(world, lx + w - 1, sy - 4, DRAWBRIDGE_CHAIN)
    for bx in range(lx + 1, lx + w):
        _castle_set(world, bx, sy - 5, MURDER_HOLE)
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy - h + 1, CORBEL_COURSE)
        _castle_set(world, bx, sy - h,     MACHICOLATION)
        _castle_set(world, bx, sy - h - 1, CRENELLATION)
    return w


def _piece_great_hall(world, lx, sy):
    """Great hall with central fireplace, chandeliers, and heraldic panels."""
    w, h = _CW_GREAT_HALL, _CH_WALL
    cx = lx + w // 2
    _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, CURTAIN_WALL)
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy, GREAT_HALL_FLOOR)
    for by in range(sy - h, sy):
        _castle_set(world, lx, by, CURTAIN_WALL)
    for bx in range(lx + 1, lx + w):
        _castle_set(world, bx, sy - h + 1, WALL_WALK_FLOOR)
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy - h,     CURTAIN_WALL)
        _castle_set(world, bx, sy - h - 1, CORBEL_COURSE)
        if bx % 2 == 0:
            _castle_set(world, bx, sy - h - 2, CRENELLATION)
        else:
            _castle_set(world, bx, sy - h - 2, MACHICOLATION)
    _castle_bg(world, cx, sy - 1, CASTLE_FIREPLACE)
    _castle_bg(world, cx, sy - 2, CASTLE_FIREPLACE)
    _castle_bg(world, cx, sy - 3, HERALDIC_PANEL)
    _castle_bg(world, cx, sy - 4, HERALDIC_PANEL)
    _castle_bg(world, cx - 2, sy - 1, HERALDIC_PANEL)
    _castle_bg(world, cx + 2, sy - 1, HERALDIC_PANEL)
    _castle_bg(world, cx - 3, sy - 2, BRONZE_SHIELD_MOUNT)
    _castle_bg(world, cx + 3, sy - 2, BRONZE_SHIELD_MOUNT)
    _castle_bg(world, cx - 4, sy - h + 2, CHANDELIER)
    _castle_bg(world, cx,     sy - h + 2, CHANDELIER)
    _castle_bg(world, cx + 4, sy - h + 2, CHANDELIER)
    _castle_bg(world, lx + 2,     sy - 5, WALL_SCONCE)
    _castle_bg(world, lx + w - 2, sy - 5, WALL_SCONCE)
    _castle_bg(world, cx - 5, sy - 1, CANDELABRA)
    _castle_bg(world, cx + 5, sy - 1, CANDELABRA)
    _castle_bg(world, lx + 1,     sy - 1, VICTORY_STELE)
    _castle_bg(world, lx + w - 1, sy - 1, VICTORY_STELE)
    _castle_bg(world, lx + 3,     sy - 2, PHILOSOPHERS_SCROLL)
    _castle_bg(world, lx + w - 3, sy - 2, PHILOSOPHERS_SCROLL)
    for bx in range(lx + 2, lx + w, 3):
        _castle_bg(world, bx, sy - h + 2, CORBEL_COURSE)
    return w


def _piece_grand_hall(world, lx, sy):
    """Wide grand hall with twin fireplaces and extra opulence."""
    w, h = _CW_GRAND_HALL, _CH_WALL
    t1 = lx + w // 3
    t2 = lx + 2 * w // 3
    cx = lx + w // 2
    _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, CURTAIN_WALL)
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy, GREAT_HALL_FLOOR)
    for by in range(sy - h, sy):
        _castle_set(world, lx, by, CURTAIN_WALL)
    for bx in range(lx + 1, lx + w):
        _castle_set(world, bx, sy - h + 1, WALL_WALK_FLOOR)
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy - h,     CURTAIN_WALL)
        _castle_set(world, bx, sy - h - 1, CORBEL_COURSE)
        if bx % 2 == 0:
            _castle_set(world, bx, sy - h - 2, CRENELLATION)
        else:
            _castle_set(world, bx, sy - h - 2, MACHICOLATION)
    for fc in (t1, t2):
        _castle_bg(world, fc, sy - 1, CASTLE_FIREPLACE)
        _castle_bg(world, fc, sy - 2, CASTLE_FIREPLACE)
        _castle_bg(world, fc, sy - 3, HERALDIC_PANEL)
        _castle_bg(world, fc, sy - 4, HERALDIC_PANEL)
    _castle_bg(world, cx, sy - 1, HERALDIC_PANEL)
    _castle_bg(world, cx, sy - 2, HERALDIC_PANEL)
    _castle_bg(world, t1 - 2, sy - 2, BRONZE_SHIELD_MOUNT)
    _castle_bg(world, t2 + 2, sy - 2, BRONZE_SHIELD_MOUNT)
    _castle_bg(world, cx - 1, sy - 1, BRONZE_SHIELD_MOUNT)
    _castle_bg(world, cx + 1, sy - 1, BRONZE_SHIELD_MOUNT)
    for ch_x in (lx + 2, t1 + 1, t2 - 1, lx + w - 2):
        _castle_bg(world, ch_x, sy - h + 2, CHANDELIER)
    _castle_bg(world, t1 - 1, sy - 1, CANDELABRA)
    _castle_bg(world, t2 + 1, sy - 1, CANDELABRA)
    _castle_bg(world, lx + 2,     sy - 5, WALL_SCONCE)
    _castle_bg(world, lx + w - 2, sy - 5, WALL_SCONCE)
    _castle_bg(world, lx + 1,     sy - 1, VICTORY_STELE)
    _castle_bg(world, lx + w - 1, sy - 1, VICTORY_STELE)
    _castle_bg(world, lx + 4,     sy - 2, PHILOSOPHERS_SCROLL)
    _castle_bg(world, lx + w - 4, sy - 2, PHILOSOPHERS_SCROLL)
    return w


def _piece_keep(world, lx, sy):
    """Central keep — throne room, mezzanine, tallest structure."""
    w, h = _CW_KEEP, _CH_KEEP
    cx  = lx + w // 2
    mez = sy - h // 2
    _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, ROUND_TOWER_WALL)
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy, CURTAIN_WALL)
    for bx in range(lx + 1, lx + w):
        _castle_set(world, bx, sy, PALACE_FLOOR_TILE)
    for by in range(sy - h, sy):
        _castle_set(world, lx,     by, ROUND_TOWER_WALL)
        _castle_set(world, lx + w, by, ROUND_TOWER_WALL)
    for by in range(sy - h + 1, sy):
        _castle_bg(world, lx + 1,     by, CURTAIN_WALL)
        _castle_bg(world, lx + w - 1, by, CURTAIN_WALL)
    for bx in range(lx + 1, lx + w):
        _castle_set(world, bx, mez, GREAT_HALL_FLOOR)
    for col in (cx - 1, cx):
        _castle_set(world, col, sy - 1, AIR)
        _castle_set(world, col, sy - 2, AIR)
        _castle_bg(world,  col, sy - 1, PALACE_PORTAL)
    _castle_bg(world, cx, sy - 3, HERALDIC_PANEL)
    _castle_bg(world, cx, sy - 4, HERALDIC_PANEL)
    _castle_bg(world, cx, sy - 5, HERALDIC_PANEL)
    _castle_bg(world, cx - 1, sy - 3, CASTLE_FIREPLACE)
    _castle_bg(world, cx + 1, sy - 3, CASTLE_FIREPLACE)
    _castle_bg(world, cx - 2, sy - 1, CANDELABRA)
    _castle_bg(world, cx + 2, sy - 1, CANDELABRA)
    _castle_bg(world, cx - 3, sy - 1, BRONZE_SHIELD_MOUNT)
    _castle_bg(world, cx + 3, sy - 1, BRONZE_SHIELD_MOUNT)
    _castle_bg(world, cx - 2, sy - _CH_WALL + 1, CHANDELIER)
    _castle_bg(world, cx + 2, sy - _CH_WALL + 1, CHANDELIER)
    _castle_bg(world, cx - 1, mez - 2, LANTERN_ORB)
    _castle_bg(world, cx + 1, mez - 2, LANTERN_ORB)
    _castle_bg(world, cx,     mez - 3, HERALDIC_PANEL)
    _castle_bg(world, lx + 2,     sy - 6, WALL_SCONCE)
    _castle_bg(world, lx + w - 2, sy - 6, WALL_SCONCE)
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy - h + 1, CORBEL_COURSE)
        _castle_set(world, bx, sy - h,     MACHICOLATION)
        _castle_set(world, bx, sy - h - 1, CRENELLATION)
    _castle_bg(world, lx,     sy - h - 1, GARGOYLE_BLOCK)
    _castle_bg(world, lx + w, sy - h - 1, GARGOYLE_BLOCK)
    _castle_set(world, lx,     sy - _CH_WALL - 1, PALAZZO_BALCONY)
    _castle_set(world, lx + w, sy - _CH_WALL - 1, PALAZZO_BALCONY)
    _castle_bg(world, cx, sy - h + 3, STAR_LAMP)
    _castle_bg(world, cx, mez - 4,    HERALDIC_PANEL)
    return w


def _piece_palace_keep(world, lx, sy):
    """Grand palace keep — wider, taller, three-level throne complex."""
    w, h   = _CW_PAL_KEEP, _CH_PAL_KEEP
    cx     = lx + w // 2
    low_mez = sy - h // 3
    hi_mez  = sy - 2 * h // 3
    _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, ROUND_TOWER_WALL)
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy, CURTAIN_WALL)
    for bx in range(lx + 1, lx + w):
        _castle_set(world, bx, sy, PALACE_FLOOR_TILE)
    for by in range(sy - h, sy):
        _castle_set(world, lx,     by, ROUND_TOWER_WALL)
        _castle_set(world, lx + w, by, ROUND_TOWER_WALL)
    for by in range(sy - h + 1, sy):
        _castle_bg(world, lx + 1,     by, CURTAIN_WALL)
        _castle_bg(world, lx + w - 1, by, CURTAIN_WALL)
    for bx in range(lx + 1, lx + w):
        _castle_set(world, bx, low_mez, GREAT_HALL_FLOOR)
        _castle_set(world, bx, hi_mez,  WALL_WALK_FLOOR)
    for col in (cx - 1, cx, cx + 1):
        _castle_set(world, col, sy - 1, AIR)
        _castle_set(world, col, sy - 2, AIR)
        _castle_bg(world,  col, sy - 1, PALACE_PORTAL)
    _castle_bg(world, cx, sy - 3, HERALDIC_PANEL)
    _castle_bg(world, cx, sy - 4, HERALDIC_PANEL)
    _castle_bg(world, cx, sy - 5, HERALDIC_PANEL)
    _castle_bg(world, cx, sy - 6, HERALDIC_PANEL)
    _castle_bg(world, cx - 2, sy - 3, CASTLE_FIREPLACE)
    _castle_bg(world, cx + 2, sy - 3, CASTLE_FIREPLACE)
    _castle_bg(world, cx - 3, sy - 1, CANDELABRA)
    _castle_bg(world, cx + 3, sy - 1, CANDELABRA)
    _castle_bg(world, cx - 4, sy - 1, BRONZE_SHIELD_MOUNT)
    _castle_bg(world, cx + 4, sy - 1, BRONZE_SHIELD_MOUNT)
    _castle_bg(world, cx - 1, low_mez - 2, LANTERN_ORB)
    _castle_bg(world, cx + 1, low_mez - 2, LANTERN_ORB)
    _castle_bg(world, cx,     low_mez - 3, HERALDIC_PANEL)
    _castle_bg(world, cx - 3, low_mez - 1, CHANDELIER)
    _castle_bg(world, cx + 3, low_mez - 1, CHANDELIER)
    _castle_bg(world, cx, hi_mez - 2, STAR_LAMP)
    _castle_bg(world, cx, hi_mez - 3, HERALDIC_PANEL)
    _castle_bg(world, lx + 2,     sy - 7,       WALL_SCONCE)
    _castle_bg(world, lx + w - 2, sy - 7,       WALL_SCONCE)
    _castle_bg(world, lx + 2,     low_mez - 4,  WALL_SCONCE)
    _castle_bg(world, lx + w - 2, low_mez - 4,  WALL_SCONCE)
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy - h + 1, CORBEL_COURSE)
        _castle_set(world, bx, sy - h,     MACHICOLATION)
        _castle_set(world, bx, sy - h - 1, CRENELLATION)
    _castle_bg(world, lx,     sy - h - 1, GARGOYLE_BLOCK)
    _castle_bg(world, lx + w, sy - h - 1, GARGOYLE_BLOCK)
    _castle_set(world, lx,     sy - _CH_WALL - 1, PALAZZO_BALCONY)
    _castle_set(world, lx + w, sy - _CH_WALL - 1, PALAZZO_BALCONY)
    return w


def _piece_chapel(world, lx, sy):
    """Gothic chapel wing with tracery, lancet windows, and rose window."""
    w, h = _CW_CHAPEL, _CH_CHAPEL
    cx = lx + w // 2
    _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, CHAPEL_STONE)
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy, GREAT_HALL_FLOOR)
    for by in range(sy - h, sy):
        _castle_set(world, lx,     by, CHAPEL_STONE)
        _castle_set(world, lx + w, by, CHAPEL_STONE)
    for by in range(sy - h + 2, sy - 2):
        _castle_bg(world, cx - 1, by, GOTHIC_TRACERY)
        _castle_bg(world, cx + 1, by, GOTHIC_TRACERY)
        _castle_bg(world, cx,     by, CHAPEL_STONE)
    _castle_bg(world, cx,     sy - h + 1, ROSE_WINDOW)
    _castle_bg(world, cx - 1, sy - h + 2, GOTHIC_TRACERY)
    _castle_bg(world, cx + 1, sy - h + 2, GOTHIC_TRACERY)
    for by in range(sy - 5, sy - 2):
        _castle_bg(world, lx + 2,     by, LANCET_WINDOW)
        _castle_bg(world, lx + w - 2, by, LANCET_WINDOW)
    _castle_bg(world, cx,     sy - 1, CHAPEL_STONE)
    _castle_bg(world, cx,     sy - 2, CHAPEL_STONE)
    _castle_bg(world, cx - 2, sy - 1, CANDELABRA)
    _castle_bg(world, cx + 2, sy - 1, CANDELABRA)
    _castle_bg(world, cx - 3, sy - 3, WALL_SCONCE)
    _castle_bg(world, cx + 3, sy - 3, WALL_SCONCE)
    _castle_bg(world, cx,     sy - h + 4, CHANDELIER)
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy - h, CHAPEL_STONE)
        if (bx - lx) % 2 == 0:
            _castle_set(world, bx, sy - h - 1, CRENELLATION)
        else:
            _castle_bg(world, bx, sy - h - 1, GOTHIC_TRACERY)
    return w


def _piece_barracks(world, lx, sy):
    """Military barracks wing — rough stone, weapon racks, soldier quarters."""
    w, h = _CW_BARRACKS, _CH_WALL
    cx = lx + w // 2
    _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, DUNGEON_WALL)
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy, CURTAIN_WALL)
    for by in range(sy - h, sy):
        _castle_set(world, lx,     by, CURTAIN_WALL)
        _castle_set(world, lx + w, by, CURTAIN_WALL)
    for bx in range(lx + 1, lx + w):
        _castle_set(world, bx, sy - h + 1, WALL_WALK_FLOOR)
    for bx in range(lx, lx + w + 1):
        _castle_set(world, bx, sy - h,     CURTAIN_WALL)
        _castle_set(world, bx, sy - h - 1, CORBEL_COURSE)
        if bx % 2 == 0:
            _castle_set(world, bx, sy - h - 2, CRENELLATION)
        else:
            _castle_set(world, bx, sy - h - 2, MACHICOLATION)
    for off in range(1, w, 2):
        _castle_bg(world, lx + off, sy - 2, BRONZE_SHIELD_MOUNT)
    _castle_bg(world, cx - 2, sy - 1, DUNGEON_GRATE)
    _castle_bg(world, cx + 2, sy - 1, DUNGEON_GRATE)
    _castle_bg(world, cx,     sy - 1, VICTORY_STELE)
    _castle_bg(world, lx + 2,     sy - 5, WALL_SCONCE)
    _castle_bg(world, lx + w - 2, sy - 5, WALL_SCONCE)
    _castle_bg(world, cx - 4, sy - 1, BRAZIER)
    _castle_bg(world, cx + 4, sy - 1, BRAZIER)
    return w


# Piece width lookup (defined after all piece functions)
_PIECE_W = None  # lazy-initialised on first _place_castle call


def _get_piece_w():
    global _PIECE_W
    if _PIECE_W is None:
        _PIECE_W = {
            _piece_moat:         _CW_MOAT,
            _piece_round_tower:  _CW_ROUND_TOW,
            _piece_square_tower: _CW_SQ_TOW,
            _piece_gatehouse:    _CW_GATEHOUSE,
            _piece_great_hall:   _CW_GREAT_HALL,
            _piece_grand_hall:   _CW_GRAND_HALL,
            _piece_keep:         _CW_KEEP,
            _piece_palace_keep:  _CW_PAL_KEEP,
            _piece_chapel:       _CW_CHAPEL,
            _piece_barracks:     _CW_BARRACKS,
        }
    return _PIECE_W


# Castle layout templates — each is a sequence of piece functions
def _castle_templates():
    return [
        # 0 — Classic fortress (original layout)
        [_piece_moat, _piece_round_tower, _piece_gatehouse, _piece_great_hall,
         _piece_keep, _piece_chapel, _piece_round_tower, _piece_moat],
        # 1 — Grand palace: enter through hall, no gatehouse, palace keep
        [_piece_moat, _piece_square_tower, _piece_grand_hall,
         _piece_palace_keep, _piece_chapel, _piece_square_tower, _piece_moat],
        # 2 — War citadel: barracks flanking the keep, military feel
        [_piece_moat, _piece_round_tower, _piece_gatehouse, _piece_barracks,
         _piece_keep, _piece_barracks, _piece_round_tower, _piece_moat],
        # 3 — Manor keep: grand hall west, palace keep east, no chapel
        [_piece_moat, _piece_square_tower, _piece_gatehouse, _piece_grand_hall,
         _piece_palace_keep, _piece_round_tower, _piece_moat],
    ]


def _place_castle(world, left_x: int, sy: int):
    """Assemble a castle from modular pieces — 4 different layouts."""
    rng     = random.Random(left_x ^ (world.seed * 0x9E3779B9) ^ 0xC4571E)
    pieces  = rng.choice(_castle_templates())
    pw      = _get_piece_w()
    total_w = sum(pw[p] for p in pieces)
    for cx in range((left_x - 4) // CHUNK_W,
                    (left_x + total_w + 4) // CHUNK_W + 1):
        world.load_chunk(cx)
    max_h = _CH_PAL_KEEP + 6
    for bx in range(left_x - 2, left_x + total_w + 3):
        for by in range(sy - max_h, sy):
            if world.get_block(bx, by) not in (AIR, BEDROCK):
                world.set_block(bx, by, AIR)
    for bx in range(left_x, left_x + total_w + 1):
        col_sy = world.surface_y_at(bx)
        for by in range(col_sy, sy):
            if world.get_block(bx, by) not in (AIR, BEDROCK):
                world.set_block(bx, by, AIR)
        for by in range(sy, col_sy + 1):
            if world.get_block(bx, by) == AIR:
                world.set_block(bx, by, STONE)
    sections = []
    x = left_x
    for piece_fn in pieces:
        sections.append((piece_fn, x))
        x += piece_fn(world, x, sy)
    for i in range(1, len(sections)):
        prev_fn, _  = sections[i - 1]
        this_fn, lx = sections[i]
        if prev_fn is _piece_moat and this_fn is not _piece_moat:
            _castle_door(world, lx, sy)
        elif prev_fn is not _piece_moat and this_fn is _piece_moat:
            _castle_door(world, lx, sy)
        elif prev_fn is not _piece_moat:
            _castle_door(world, lx - 1, sy)
    # assembly complete


def _palace_clear_terrain(world, left_x: int, sy: int, total_w: int, max_h: int):
    """Shared terrain prep for all cultural palaces."""
    for cx in range((left_x - 2) // CHUNK_W, (left_x + total_w + 4) // CHUNK_W + 1):
        world.load_chunk(cx)
    for bx in range(left_x - 1, left_x + total_w + 2):
        for by in range(sy - max_h, sy):
            if world.get_block(bx, by) not in (AIR, BEDROCK):
                world.set_block(bx, by, AIR)
    for bx in range(left_x, left_x + total_w + 1):
        col_sy = world.surface_y_at(bx)
        for by in range(col_sy, sy):
            if world.get_block(bx, by) not in (AIR, BEDROCK):
                world.set_block(bx, by, AIR)
        for by in range(sy, col_sy + 1):
            if world.get_block(bx, by) == AIR:
                world.set_block(bx, by, STONE)


def _palace_npc_at(world, bx, sy, npc_cls, *args, **kwargs):
    """Spawn an NPC centred on block bx, standing on floor row sy."""
    px = bx * BLOCK_SIZE + (BLOCK_SIZE - NPC.NPC_W) // 2
    py = (sy - 2) * BLOCK_SIZE
    world.entities.append(npc_cls(px, py, world, *args, **kwargs))


# Block-offset from palace left_x to throne centre — used by _place_capital_structures.
PALACE_NPC_OFFSET = {
    "mediterranean": 45,   # 8 garden + 12 stoa + 14 wing + 11 half-basilica
    "east_asian":    46,   # 10 garden + 14 reception + 12 pavilion + 10 half-keep
    "south_asian":   44,   # 8 garden + 10 gate + 14 court + 12 half-diwan
}


def _populate_castle(world, left_x: int, sy: int, rng: random.Random):
    """Spawn supporting staff inside a medieval castle (works for all layout templates)."""
    _palace_npc_at(world, left_x + 18, sy, TradeNPC, rng)
    _palace_npc_at(world, left_x + 30, sy, MerchantNPC, rng)
    _palace_npc_at(world, left_x + 44, sy, ShrineKeeperNPC, rng)


def _place_mediterranean_palace(world, left_x: int, sy: int):
    """Grand forum complex — outer gardens, market stoa, temple wing, domed basilica,
    treasury, banquet hall.  Staff: court trader, oracle, quartermaster, palace chef.
    """
    rng = random.Random(left_x ^ (world.seed * 0x1B4C3A7) ^ 0xA3D5E1)

    W_GARD = 8
    W_STOA = 12;  H_STOA = 10
    W_WING = 14;  H_WING = 13
    W_HALL = 22;  H_HALL = 18
    total_w = W_GARD + W_STOA + W_WING + W_HALL + W_WING + W_STOA + W_GARD
    _palace_clear_terrain(world, left_x, sy, total_w, H_HALL + 14)

    # --- shared room builder ---
    def _med_room(lx, w, h):
        _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, LIMESTONE_BLOCK)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy, ROMAN_MOSAIC)
        for by in range(sy - h, sy):
            _castle_set(world, lx,      by, LIMESTONE_BLOCK)
            _castle_set(world, lx + w,  by, LIMESTONE_BLOCK)
        _castle_door(world, lx, sy)
        _castle_door(world, lx + w - 2, sy)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy - h,     POLISHED_MARBLE)
            _castle_set(world, bx, sy - h - 1, POLISHED_MARBLE)
        for bx in range(lx + 1, lx + w, 3):
            _castle_bg(world, bx, sy - 5, ROMAN_ARCH_REN)

    def _med_cols(lx, w, n=2):
        step = max(3, w // (n + 1))
        for i in range(1, n + 1):
            cx = lx + i * step
            for by in range(sy - 10, sy):
                _castle_bg(world, cx, by, GARDEN_COLUMN)
            _castle_bg(world, cx, sy - 11, DORIC_CAPITAL)

    x = left_x

    # ── outer garden (left) ─────────────────────────────────────────────────
    for bx in range(x, x + W_GARD):
        _castle_set(world, bx, sy, INLAID_MARBLE)
    for bx in range(x, x + W_GARD, 2):
        _castle_bg(world, bx, sy - 1, GARDEN_COLUMN)
        _castle_bg(world, bx, sy - 2, GARDEN_COLUMN)
        _castle_bg(world, bx, sy - 3, DORIC_CAPITAL)
    _castle_bg(world, x + 1, sy - 1, LAVENDER_BED)
    _castle_bg(world, x + 3, sy - 1, ROSE_BED)
    _castle_bg(world, x + 5, sy - 1, LAVENDER_BED)
    _castle_bg(world, x + W_GARD // 2, sy - 2, MARBLE_PLINTH)
    _castle_bg(world, x + W_GARD // 2, sy - 1, MARBLE_STATUE)
    x += W_GARD

    # ── market stoa — court trader ───────────────────────────────────────────
    _med_room(x, W_STOA, H_STOA)
    _med_cols(x, W_STOA, n=2)
    _castle_bg(world, x + W_STOA // 2,     sy - 1, SYMPOSIUM_TABLE)
    _castle_bg(world, x + 2,               sy - 1, CARVED_BENCH)
    _castle_bg(world, x + W_STOA - 2,      sy - 1, CARVED_BENCH)
    _castle_bg(world, x + 1,               sy - 2, OLIVE_BRANCH)
    _castle_bg(world, x + W_STOA - 1,      sy - 2, OLIVE_BRANCH)
    _castle_bg(world, x + W_STOA // 2,     sy - H_STOA + 2, WALL_SCONCE)
    _palace_npc_at(world, x + W_STOA // 2, sy, TradeNPC, rng)
    x += W_STOA

    # ── temple wing — oracle / philosopher ──────────────────────────────────
    _med_room(x, W_WING, H_WING)
    _med_cols(x, W_WING, n=2)
    _castle_bg(world, x + W_WING // 2,     sy - 1, MARBLE_PLINTH)
    _castle_bg(world, x + W_WING // 2,     sy - 2, VOTIVE_TABLET)
    _castle_bg(world, x + 2,               sy - 1, TRIPOD_BRAZIER)
    _castle_bg(world, x + W_WING - 2,      sy - 1, TRIPOD_BRAZIER)
    _castle_bg(world, x + 3,               sy - 3, PHILOSOPHERS_SCROLL)
    _castle_bg(world, x + W_WING - 3,      sy - 3, PHILOSOPHERS_SCROLL)
    _castle_bg(world, x + W_WING // 2,     sy - H_WING + 3, CHANDELIER)
    _palace_npc_at(world, x + W_WING // 2, sy, ShrineKeeperNPC, rng,
                   biodome="mediterranean")
    x += W_WING

    # ── central basilica — Leader throne (spawned by caller) ─────────────────
    cx_hall = x + W_HALL // 2
    _castle_fill_bg(world, x, x + W_HALL, sy - H_HALL, sy - 1, LIMESTONE_BLOCK)
    for bx in range(x, x + W_HALL + 1):
        _castle_set(world, bx, sy, INLAID_MARBLE)
    for by in range(sy - H_HALL, sy):
        _castle_set(world, x,          by, LIMESTONE_BLOCK)
        _castle_set(world, x + W_HALL, by, LIMESTONE_BLOCK)
    _castle_door(world, x, sy)
    _castle_door(world, x + W_HALL - 2, sy)
    # Nave — four column pairs forming a processional aisle
    for col_x in (x + 4, x + 8, x + W_HALL - 8, x + W_HALL - 4):
        for by in range(sy - H_HALL + 4, sy):
            _castle_bg(world, col_x, by, GARDEN_COLUMN)
        _castle_bg(world, col_x, sy - H_HALL + 3, DORIC_CAPITAL)
    # Arch band across the upper wall
    for bx in range(x + 1, x + W_HALL, 2):
        _castle_bg(world, bx, sy - 9, ROMAN_ARCH_REN)
    # Double marble cornice
    for bx in range(x, x + W_HALL + 1):
        _castle_set(world, bx, sy - H_HALL,     POLISHED_MARBLE)
        _castle_set(world, bx, sy - H_HALL - 1, POLISHED_MARBLE)
    # Full dome
    for row in range(1, W_HALL // 2 + 1):
        dome_y = sy - H_HALL - 1 - row
        if not (0 <= dome_y < world.height):
            break
        for bx in range(x + row, x + W_HALL + 1 - row):
            _castle_set(world, bx, dome_y, POLISHED_MARBLE)
    # Throne dais and lighting
    _castle_bg(world, cx_hall,     sy - 1, MARBLE_PLINTH)
    _castle_bg(world, cx_hall,     sy - 2, HERMES_STELE)
    _castle_bg(world, cx_hall - 4, sy - 1, TRIPOD_BRAZIER)
    _castle_bg(world, cx_hall + 4, sy - 1, TRIPOD_BRAZIER)
    _castle_bg(world, cx_hall - 7, sy - 1, LAUREL_WREATH_MOUNT)
    _castle_bg(world, cx_hall + 7, sy - 1, LAUREL_WREATH_MOUNT)
    _castle_bg(world, cx_hall,     sy - H_HALL + 4, CHANDELIER)
    _castle_bg(world, cx_hall - 3, sy - H_HALL + 6, CANDELABRA)
    _castle_bg(world, cx_hall + 3, sy - H_HALL + 6, CANDELABRA)
    x += W_HALL

    # ── treasury wing — court merchant / quartermaster ───────────────────────
    _med_room(x, W_WING, H_WING)
    _med_cols(x, W_WING, n=2)
    _castle_bg(world, x + W_WING // 2,     sy - 1, HERMES_STELE)
    _castle_bg(world, x + W_WING // 2,     sy - 2, MARBLE_PLINTH)
    _castle_bg(world, x + 2,               sy - 2, WALL_SCONCE)
    _castle_bg(world, x + W_WING - 2,      sy - 2, WALL_SCONCE)
    _castle_bg(world, x + 3,               sy - 1, CARVED_BENCH)
    _castle_bg(world, x + W_WING - 3,      sy - 1, CARVED_BENCH)
    _castle_bg(world, x + W_WING // 2,     sy - H_WING + 3, CHANDELIER)
    _palace_npc_at(world, x + W_WING // 2, sy, MerchantNPC, rng)
    x += W_WING

    # ── banquet stoa — palace chef ───────────────────────────────────────────
    _med_room(x, W_STOA, H_STOA)
    _med_cols(x, W_STOA, n=2)
    _castle_bg(world, x + W_STOA // 2,     sy - 1, SYMPOSIUM_TABLE)
    _castle_bg(world, x + 2,               sy - 1, GREEK_STONE_BENCH)
    _castle_bg(world, x + W_STOA - 2,      sy - 1, GREEK_STONE_BENCH)
    _castle_bg(world, x + 1,               sy - 2, LAUREL_WREATH_MOUNT)
    _castle_bg(world, x + W_STOA - 1,      sy - 2, LAUREL_WREATH_MOUNT)
    _castle_bg(world, x + W_STOA // 2,     sy - H_STOA + 2, CHANDELIER)
    _palace_npc_at(world, x + W_STOA // 2, sy, RestaurantNPC, rng, "mediterranean")
    x += W_STOA

    # ── outer garden (right) ─────────────────────────────────────────────────
    for bx in range(x, x + W_GARD):
        _castle_set(world, bx, sy, INLAID_MARBLE)
    for bx in range(x, x + W_GARD, 2):
        _castle_bg(world, bx, sy - 1, GARDEN_COLUMN)
        _castle_bg(world, bx, sy - 2, GARDEN_COLUMN)
        _castle_bg(world, bx, sy - 3, DORIC_CAPITAL)
    _castle_bg(world, x + 1, sy - 1, ROSE_BED)
    _castle_bg(world, x + 3, sy - 1, LAVENDER_BED)
    _castle_bg(world, x + 5, sy - 1, ROSE_BED)
    _castle_bg(world, x + W_GARD // 2, sy - 2, MARBLE_PLINTH)
    _castle_bg(world, x + W_GARD // 2, sy - 1, MARBLE_BIRDBATH)


def _place_east_asian_palace(world, left_x: int, sy: int):
    """Imperial compound — garden approaches, shinto reception courts, pavilion wings,
    central 4-tier pagoda keep.  Staff: shrine priest, court steward, palace chef, trader.
    """
    rng = random.Random(left_x ^ (world.seed * 0x7E3C1F9) ^ 0xD4E7B2)

    W_GARD = 10   # outer garden + torii approach
    W_RCRT = 14;  H_RCRT = 12   # reception court
    W_PAV  = 12;  H_PAV  = 12   # inner pavilion
    W_KEEP = 20;  H_KEEP = 18   # central pagoda keep
    total_w = W_GARD + W_RCRT + W_PAV + W_KEEP + W_PAV + W_RCRT + W_GARD
    _palace_clear_terrain(world, left_x, sy, total_w, H_KEEP + 16)

    # --- shared builders ---
    def _ea_room(lx, w, h, tiers=2):
        _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, PINE_PLANK_WALL)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy, TATAMI_PAVING)
        for by in range(sy - h, sy):
            _castle_set(world, lx,      by, PINE_PLANK_WALL)
            _castle_set(world, lx + w,  by, PINE_PLANK_WALL)
        _castle_door(world, lx, sy)
        _castle_door(world, lx + w - 2, sy)
        for bx in range(lx + 1, lx + w, 2):
            _castle_bg(world, bx, sy - 4, JAPANESE_SHOJI)
            _castle_bg(world, bx, sy - 5, JAPANESE_SHOJI)
        for tier in range(tiers):
            base_y = sy - h - 1 - tier * 2
            for bx in range(lx - 1 + tier, lx + w + 2 - tier):
                _castle_set(world, bx, base_y, PAGODA_EAVE)
            for bx in range(lx + tier, lx + w + 1 - tier):
                _castle_set(world, bx, base_y - 1, PINE_PLANK_WALL)

    def _torii(ax, w):
        for bx in range(ax, ax + w):
            _castle_set(world, bx, sy, TATAMI_PAVING)
        mid = ax + w // 2
        for post in (mid, mid + 2):
            for row in range(1, 4):
                _castle_set(world, post, sy - row, TORII_PANEL)
        for bx in range(mid - 1, mid + 4):
            _castle_set(world, bx, sy - 4, TORII_PANEL)
            _castle_set(world, bx, sy - 5, TORII_PANEL)
        _castle_bg(world, ax + 1,      sy - 1, PINE_TOPIARY_JP)
        _castle_bg(world, ax + 2,      sy - 1, JAPANESE_MAPLE)
        _castle_bg(world, ax + w - 2,  sy - 1, JAPANESE_MAPLE)
        _castle_bg(world, ax + w - 1,  sy - 1, PINE_TOPIARY_JP)
        _castle_bg(world, ax + w // 2, sy - 1, KOI_POOL)

    x = left_x

    # ── outer garden + torii (left) ──────────────────────────────────────────
    _torii(x, W_GARD)
    x += W_GARD

    # ── left reception court — shinto shrine priest ──────────────────────────
    _ea_room(x, W_RCRT, H_RCRT, tiers=2)
    _castle_bg(world, x + W_RCRT // 2,     sy - 1, STONE_BASIN)
    _castle_bg(world, x + 2,               sy - 1, PINE_TOPIARY_JP)
    _castle_bg(world, x + W_RCRT - 2,      sy - 1, PINE_TOPIARY_JP)
    _castle_bg(world, x + W_RCRT // 2,     sy - H_RCRT + 3, CHANDELIER)
    _castle_bg(world, x + 1,               sy - 3, BAMBOO_CLUMP)
    _castle_bg(world, x + W_RCRT - 1,      sy - 3, BAMBOO_CLUMP)
    _palace_npc_at(world, x + W_RCRT // 2, sy, ShrineKeeperNPC, rng,
                   biodome="east_asian")
    x += W_RCRT

    # ── left inner pavilion — court steward ─────────────────────────────────
    _ea_room(x, W_PAV, H_PAV, tiers=2)
    _castle_bg(world, x + W_PAV // 2,     sy - 1, GARDEN_LANTERN)
    _castle_bg(world, x + 2,              sy - 1, BAMBOO_CLUMP)
    _castle_bg(world, x + W_PAV - 2,      sy - 1, BAMBOO_CLUMP)
    _castle_bg(world, x + W_PAV // 2,     sy - H_PAV + 3, STAR_LAMP)
    _palace_npc_at(world, x + W_PAV // 2, sy, MerchantNPC, rng)
    x += W_PAV

    # ── central pagoda keep — Leader throne (spawned by caller) ──────────────
    cx_keep = x + W_KEEP // 2
    _castle_fill_bg(world, x, x + W_KEEP, sy - H_KEEP, sy - 1, PINE_PLANK_WALL)
    for bx in range(x, x + W_KEEP + 1):
        _castle_set(world, bx, sy, TATAMI_PAVING)
    for by in range(sy - H_KEEP, sy):
        _castle_set(world, x,          by, PINE_PLANK_WALL)
        _castle_set(world, x + W_KEEP, by, PINE_PLANK_WALL)
    _castle_door(world, x, sy)
    _castle_door(world, x + W_KEEP - 2, sy)
    # Mid-floor gallery
    mid_floor = sy - H_KEEP // 2
    for bx in range(x + 1, x + W_KEEP):
        _castle_set(world, bx, mid_floor, TATAMI_PAVING)
    # Upper-level shoji screens
    for bx in range(x + 1, x + W_KEEP, 2):
        _castle_bg(world, bx, sy - 6, JAPANESE_SHOJI)
        _castle_bg(world, bx, sy - 7, JAPANESE_SHOJI)
    for bx in range(x + 1, x + W_KEEP, 2):
        _castle_bg(world, bx, mid_floor - 2, JAPANESE_SHOJI)
        _castle_bg(world, bx, mid_floor - 3, JAPANESE_SHOJI)
    # Interior wooden columns
    for col_x in (x + 4, x + W_KEEP - 4):
        for by in range(sy - H_KEEP + 4, sy):
            _castle_bg(world, col_x, by, PINE_PLANK_WALL)
        _castle_bg(world, col_x, sy - H_KEEP + 3, GARDEN_LANTERN)
    # Throne and lighting
    _castle_bg(world, cx_keep,     sy - 1, CARVED_BENCH)
    _castle_bg(world, cx_keep - 4, sy - 1, STAR_LAMP)
    _castle_bg(world, cx_keep + 4, sy - 1, STAR_LAMP)
    _castle_bg(world, cx_keep - 6, sy - 1, BAMBOO_CLUMP)
    _castle_bg(world, cx_keep + 6, sy - 1, BAMBOO_CLUMP)
    _castle_bg(world, cx_keep,     sy - H_KEEP + 4, CHANDELIER)
    # 4-tier pagoda roof
    for tier in range(4):
        base_y = sy - H_KEEP - 1 - tier * 2
        for bx in range(x - 1 + tier, x + W_KEEP + 2 - tier):
            _castle_set(world, bx, base_y, PAGODA_EAVE)
        for bx in range(x + tier, x + W_KEEP + 1 - tier):
            _castle_set(world, bx, base_y - 1, PINE_PLANK_WALL)
    x += W_KEEP

    # ── right inner pavilion — palace chef ───────────────────────────────────
    _ea_room(x, W_PAV, H_PAV, tiers=2)
    _castle_bg(world, x + W_PAV // 2,     sy - 1, GARDEN_LANTERN)
    _castle_bg(world, x + 2,              sy - 1, BAMBOO_CLUMP)
    _castle_bg(world, x + W_PAV - 2,      sy - 1, BAMBOO_CLUMP)
    _castle_bg(world, x + W_PAV // 2,     sy - H_PAV + 3, STAR_LAMP)
    _palace_npc_at(world, x + W_PAV // 2, sy, RestaurantNPC, rng, "east_asian")
    x += W_PAV

    # ── right reception court — court trader ─────────────────────────────────
    _ea_room(x, W_RCRT, H_RCRT, tiers=2)
    _castle_bg(world, x + W_RCRT // 2,     sy - 1, SHISHI_ODOSHI)
    _castle_bg(world, x + 2,               sy - 1, JAPANESE_MAPLE)
    _castle_bg(world, x + W_RCRT - 2,      sy - 1, JAPANESE_MAPLE)
    _castle_bg(world, x + W_RCRT // 2,     sy - H_RCRT + 3, CHANDELIER)
    _castle_bg(world, x + 1,               sy - 3, PINE_TOPIARY_JP)
    _castle_bg(world, x + W_RCRT - 1,      sy - 3, PINE_TOPIARY_JP)
    _palace_npc_at(world, x + W_RCRT // 2, sy, TradeNPC, rng)
    x += W_RCRT

    # ── outer garden + torii (right) ─────────────────────────────────────────
    _torii(x, W_GARD)


def _place_south_asian_palace(world, left_x: int, sy: int):
    """Ornate Mughal imperial complex — peacock gardens, soaring gate towers, jali courts,
    massive central Diwan-i-Khas.  Staff: vizier, court pandit, quartermaster, palace chef.
    """
    rng = random.Random(left_x ^ (world.seed * 0xC3E5A91) ^ 0xF2B6D3)

    W_GARD = 8
    W_GATE = 10;  H_GATE = 14
    W_CORT = 14;  H_CORT = 12
    W_DIWAN= 24;  H_DIWAN= 20
    total_w = W_GARD + W_GATE + W_CORT + W_DIWAN + W_CORT + W_GATE + W_GARD
    _palace_clear_terrain(world, left_x, sy, total_w, H_DIWAN + 16)

    # --- shared builders ---
    def _sa_room(lx, w, h, fountain=False):
        _castle_fill_bg(world, lx, lx + w, sy - h, sy - 1, LIMESTONE_BLOCK)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy, MUDEJAR_STAR_TILE)
        for by in range(sy - h, sy):
            _castle_set(world, lx,      by, LIMESTONE_BLOCK)
            _castle_set(world, lx + w,  by, LIMESTONE_BLOCK)
        _castle_door(world, lx, sy)
        _castle_door(world, lx + w - 2, sy)
        for bx in range(lx + 1, lx + w, 2):
            _castle_bg(world, bx, sy - 4, MUGHAL_JALI)
            _castle_bg(world, bx, sy - 5, MUGHAL_JALI)
        for bx in range(lx, lx + w + 1):
            _castle_set(world, bx, sy - h, TERRACOTTA_ROOF_TILE)
        if fountain:
            _castle_bg(world, lx + w // 2, sy - 1, ANDALUSIAN_FOUNTAIN)

    def _gate_tower(gx):
        _castle_fill_bg(world, gx, gx + W_GATE, sy - H_GATE, sy - 1, LIMESTONE_BLOCK)
        for bx in range(gx, gx + W_GATE + 1):
            _castle_set(world, bx, sy, MUDEJAR_STAR_TILE)
        for by in range(sy - H_GATE, sy):
            _castle_set(world, gx,          by, LIMESTONE_BLOCK)
            _castle_set(world, gx + W_GATE, by, LIMESTONE_BLOCK)
        # Central Mughal arch passage
        _castle_door(world, gx + W_GATE // 2 - 1, sy)
        for by in range(sy - 6, sy):
            _castle_bg(world, gx + W_GATE // 2,     by, MUGHAL_ARCH)
            _castle_bg(world, gx + W_GATE // 2 - 1, by, MUGHAL_ARCH)
        # Upper jali screens
        for bx in range(gx + 1, gx + W_GATE, 2):
            _castle_bg(world, bx, sy - 8, MUGHAL_JALI)
            _castle_bg(world, bx, sy - 9, MUGHAL_JALI)
        # Stepped terracotta parapet
        for bx in range(gx, gx + W_GATE + 1):
            _castle_set(world, bx, sy - H_GATE, TERRACOTTA_ROOF_TILE)
            if (bx - gx) % 2 == 0:
                _castle_set(world, bx, sy - H_GATE - 1, TERRACOTTA_ROOF_TILE)
        # Corner flower decoration
        _castle_bg(world, gx + 1,          sy - H_GATE + 2, MARIGOLD_BED)
        _castle_bg(world, gx + W_GATE - 1, sy - H_GATE + 2, MARIGOLD_BED)

    x = left_x

    # ── outer peacock garden (left) ──────────────────────────────────────────
    for bx in range(x, x + W_GARD):
        _castle_set(world, bx, sy, MUDEJAR_STAR_TILE)
    _castle_bg(world, x + 1, sy - 1, TOPIARY_PEACOCK)
    _castle_bg(world, x + 3, sy - 1, MARIGOLD_BED)
    _castle_bg(world, x + 5, sy - 1, SUNFLOWER_BED)
    _castle_bg(world, x + W_GARD // 2, sy - 1, ANDALUSIAN_FOUNTAIN)
    x += W_GARD

    # ── left gate tower (purely structural — no NPC) ─────────────────────────
    _gate_tower(x)
    x += W_GATE

    # ── left jali court — vizier / court trader ──────────────────────────────
    _sa_room(x, W_CORT, H_CORT, fountain=True)
    _castle_bg(world, x + 2,               sy - 1, MARIGOLD_BED)
    _castle_bg(world, x + W_CORT - 2,      sy - 1, MARIGOLD_BED)
    _castle_bg(world, x + W_CORT // 2,     sy - H_CORT + 3, CHANDELIER)
    _castle_bg(world, x + W_CORT // 2 - 3, sy - 2, MUGHAL_JALI)
    _castle_bg(world, x + W_CORT // 2 + 3, sy - 2, MUGHAL_JALI)
    _palace_npc_at(world, x + W_CORT // 2, sy, TradeNPC, rng)
    x += W_CORT

    # ── central Diwan-i-Khas — Leader throne (spawned by caller) ────────────
    cx_diwan = x + W_DIWAN // 2
    _castle_fill_bg(world, x, x + W_DIWAN, sy - H_DIWAN, sy - 1, LIMESTONE_BLOCK)
    for bx in range(x, x + W_DIWAN + 1):
        _castle_set(world, bx, sy, MUDEJAR_STAR_TILE)
    for by in range(sy - H_DIWAN, sy):
        _castle_set(world, x,          by, LIMESTONE_BLOCK)
        _castle_set(world, x + W_DIWAN, by, LIMESTONE_BLOCK)
    _castle_door(world, x, sy)
    _castle_door(world, x + W_DIWAN - 2, sy)
    # Four Mughal arch columns forming the audience hall
    for col_x in (x + 4, x + 8, x + W_DIWAN - 8, x + W_DIWAN - 4):
        for by in range(sy - 8, sy):
            _castle_bg(world, col_x, by, MUGHAL_ARCH)
    # Upper jali screen band
    for bx in range(x + 1, x + W_DIWAN, 2):
        _castle_bg(world, bx, sy - 10, MUGHAL_JALI)
        _castle_bg(world, bx, sy - 11, MUGHAL_JALI)
    # Stepped terracotta roof
    for bx in range(x, x + W_DIWAN + 1):
        _castle_set(world, bx, sy - H_DIWAN, TERRACOTTA_ROOF_TILE)
    for step in range(1, 7):
        step_y = sy - H_DIWAN - step
        if not (0 <= step_y < world.height):
            break
        for bx in range(x + step * 2, x + W_DIWAN + 1 - step * 2):
            _castle_set(world, bx, step_y, TERRACOTTA_ROOF_TILE)
    # Throne dais
    _castle_bg(world, cx_diwan,     sy - 1, MARBLE_PLINTH)
    _castle_bg(world, cx_diwan,     sy - 2, VICTORY_STELE)
    _castle_bg(world, cx_diwan - 4, sy - 1, STAR_LAMP)
    _castle_bg(world, cx_diwan + 4, sy - 1, STAR_LAMP)
    _castle_bg(world, cx_diwan - 7, sy - 1, MARIGOLD_BED)
    _castle_bg(world, cx_diwan + 7, sy - 1, MARIGOLD_BED)
    _castle_bg(world, cx_diwan - 9, sy - 1, TOPIARY_PEACOCK)
    _castle_bg(world, cx_diwan + 9, sy - 1, TOPIARY_PEACOCK)
    _castle_bg(world, cx_diwan,     sy - H_DIWAN + 5, CHANDELIER)
    _castle_bg(world, cx_diwan - 3, sy - H_DIWAN + 7, CANDELABRA)
    _castle_bg(world, cx_diwan + 3, sy - H_DIWAN + 7, CANDELABRA)
    x += W_DIWAN

    # ── right jali court — court pandit / priest ─────────────────────────────
    _sa_room(x, W_CORT, H_CORT, fountain=True)
    _castle_bg(world, x + 2,               sy - 1, SUNFLOWER_BED)
    _castle_bg(world, x + W_CORT - 2,      sy - 1, SUNFLOWER_BED)
    _castle_bg(world, x + W_CORT // 2,     sy - H_CORT + 3, CHANDELIER)
    _castle_bg(world, x + W_CORT // 2 - 3, sy - 2, MUGHAL_JALI)
    _castle_bg(world, x + W_CORT // 2 + 3, sy - 2, MUGHAL_JALI)
    _palace_npc_at(world, x + W_CORT // 2, sy, ShrineKeeperNPC, rng,
                   biodome="south_asian")
    x += W_CORT

    # ── right gate tower — palace quartermaster ──────────────────────────────
    _gate_tower(x)
    _palace_npc_at(world, x + W_GATE // 2, sy, MerchantNPC, rng)
    x += W_GATE

    # ── outer peacock garden (right) ─────────────────────────────────────────
    for bx in range(x, x + W_GARD):
        _castle_set(world, bx, sy, MUDEJAR_STAR_TILE)
    _castle_bg(world, x + 1,          sy - 1, SUNFLOWER_BED)
    _castle_bg(world, x + 3,          sy - 1, MARIGOLD_BED)
    _castle_bg(world, x + 5,          sy - 1, TOPIARY_PEACOCK)
    _castle_bg(world, x + W_GARD // 2, sy - 1, ANDALUSIAN_FOUNTAIN)


def _city_slot_metadata(slot_x: int) -> dict:
    """Return deterministic region identity for the city slot at slot_x.

    slot_x must be the true slot center (n * CITY_SPACING + CITY_SPACING // 2),
    not the jittered city_bx.
    """
    slot_index = slot_x // CITY_SPACING      # floor div handles negatives correctly
    region_id  = slot_index // 3
    is_capital = (slot_index % 3 == 1)       # Python % is non-negative, works for negatives
    return {"slot_index": slot_index, "region_id": region_id, "is_capital": is_capital}


def generate_cities(world, seed):
    rng = random.Random(seed + 77777)
    placed = 0
    x = -(CITY_COUNT // 2) * CITY_SPACING + CITY_SPACING // 2
    world.city_zones = []
    world.town_centers = []
    world.city_sizes = []
    world.city_slot_xs = []

    while placed < CITY_COUNT:
        slot_x = x
        jitter = rng.randint(-6, 6)
        city_bx = slot_x + jitter
        difficulty = min(placed // 2, 2)
        city_size = _build_single_city(world, rng, city_bx, difficulty)
        world.town_centers.append(city_bx)
        world.city_sizes.append(city_size)
        world.city_slot_xs.append(slot_x)
        placed += 1
        x += CITY_SPACING


def _restore_city_metadata(world, seed):
    """Restore world.town_centers/city_zones/etc. from the seed without placing blocks.
    Used when loading a saved game so city queries work without overwriting saved chunks."""
    rng = random.Random(seed + 77777)
    placed = 0
    x = -(CITY_COUNT // 2) * CITY_SPACING + CITY_SPACING // 2
    world.city_zones = []
    world.town_centers = []
    world.city_sizes = []
    world.city_slot_xs = []

    while placed < CITY_COUNT:
        slot_x = x
        jitter = rng.randint(-6, 6)
        city_bx = slot_x + jitter
        difficulty = min(placed // 2, 2)
        city_size = rng.choice(_SIZE_BY_DIFFICULTY[difficulty])
        half_w = CITY_CONFIGS[city_size]["half_w"]
        world.city_zones.append((city_bx - half_w, city_bx + half_w))
        world.town_centers.append(city_bx)
        world.city_sizes.append(city_size)
        world.city_slot_xs.append(slot_x)
        placed += 1
        x += CITY_SPACING


def generate_city_for_chunk(world, seed, cx):
    """Build a city in newly-generated chunk cx if a city slot falls there."""
    from constants import CHUNK_W
    base_x = cx * CHUNK_W
    half = CITY_SPACING // 2
    slot_x = None
    for bx in range(base_x, base_x + CHUNK_W):
        if ((bx % CITY_SPACING) + CITY_SPACING) % CITY_SPACING == half:
            slot_x = bx
            break
    if slot_x is None:
        return
    meta = _city_slot_metadata(slot_x)
    rng = random.Random(seed + slot_x * 9001 + 33333)
    jitter = rng.randint(-6, 6)
    city_bx = slot_x + jitter
    if any(lo - 10 <= city_bx <= hi + 10 for lo, hi in world.city_zones):
        return
    city_size = _build_single_city(world, rng, city_bx, 2)
    world.town_centers.append(city_bx)
    world.city_sizes.append(city_size)
    world.city_slot_xs.append(slot_x)
    from towns import register_new_town
    register_new_town(world, city_bx, city_size,
                      region_id=meta["region_id"],
                      is_capital=meta["is_capital"])
