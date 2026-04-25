import math
import random

from blocks import (STONE, BEDROCK, HOUSE_WALL, HOUSE_ROOF, AIR, LADDER,
                    HOUSE_WALL_STONE, HOUSE_ROOF_STONE,
                    HOUSE_WALL_BRICK, HOUSE_ROOF_BRICK,
                    HOUSE_WALL_DARK,  HOUSE_ROOF_DARK,
                    RESTAURANT_WALL, RESTAURANT_AWNING,
                    SANDSTONE_BLOCK, POLISHED_MARBLE,
                    WHITEWASHED_WALL, MONASTERY_ROOF, MANI_STONE, PRAYER_FLAG_BLOCK,
                    WOOD_DOOR_CLOSED, ALL_LOGS, ALL_LEAVES, BUSH_BLOCKS, SAPLING,
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
                    PHILOSOPHERS_SCROLL, GREEK_THEATRE_MASK)
from constants import (BLOCK_SIZE, PLAYER_W, PLAYER_H, CITY_SPACING, CITY_COUNT,
                       NPC_INTERACT_RANGE, CHUNK_W, GRAVITY, MAX_FALL)
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


# ---------------------------------------------------------------------------
# NPC types
# ---------------------------------------------------------------------------

class RockQuestNPC(NPC):
    def __init__(self, x, y, world, rng, difficulty=0):
        super().__init__(x, y, world, "npc_quest")
        self._rng = rng
        self.difficulty = difficulty
        self._streak = 0
        self.quests = [_build_quest(rng, difficulty), _build_quest(rng, difficulty)]

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
        needed = quest.get("count", 1)
        return len(self.find_matching_rocks(player, quest)) >= needed

    def complete_quest(self, player, quest_idx=0):
        quest = self.quests[quest_idx]
        needed = quest.get("count", 1)
        matching = self.find_matching_rocks(player, quest)
        if len(matching) < needed:
            return False
        for i in sorted(matching[:needed], reverse=True):
            player.rocks.pop(i)
        self._streak += 1
        streak_mult = 1.0 + min(self._streak - 1, 2) * 0.25
        player.money += int(quest["reward"] * streak_mult * getattr(player, "blessing_mult", 1.0))
        self.quests[quest_idx] = _build_quest(self._rng, self.difficulty)
        return True


class TradeNPC(NPC):
    def __init__(self, x, y, world, rng):
        super().__init__(x, y, world, "npc_trade")
        n = rng.randint(3, 4)
        self.trades = rng.sample(TRADE_TABLE, n)

    def can_trade(self, trade_idx, player):
        item_id, give_count, _ = self.trades[trade_idx]
        return player.inventory.get(item_id, 0) >= give_count

    def execute_trade(self, trade_idx, player):
        if not self.can_trade(trade_idx, player):
            return False
        item_id, give_count, receive_gold = self.trades[trade_idx]
        player.inventory[item_id] -= give_count
        if player.inventory[item_id] <= 0:
            del player.inventory[item_id]
            for i in range(len(player.hotbar)):
                if player.hotbar[i] == item_id:
                    player.hotbar[i] = None
        player.money += receive_gold
        return True


class WildflowerQuestNPC(NPC):
    def __init__(self, x, y, world, rng, difficulty=0):
        super().__init__(x, y, world, "npc_herbalist")
        self._rng = rng
        self.difficulty = difficulty
        self._streak = 0
        self.quests = [_build_wf_quest(rng, difficulty), _build_wf_quest(rng, difficulty)]

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
        needed = quest.get("count", 1)
        return len(self.find_matching_flowers(player, quest)) >= needed

    def complete_quest(self, player, quest_idx=0):
        quest = self.quests[quest_idx]
        needed = quest.get("count", 1)
        matching = self.find_matching_flowers(player, quest)
        if len(matching) < needed:
            return False
        for i in sorted(matching[:needed], reverse=True):
            player.wildflowers.pop(i)
        self._streak += 1
        streak_mult = 1.0 + min(self._streak - 1, 2) * 0.25
        player.money += int(quest["reward"] * streak_mult * getattr(player, "blessing_mult", 1.0))
        self.quests[quest_idx] = _build_wf_quest(self._rng, self.difficulty)
        return True


class GemQuestNPC(NPC):
    def __init__(self, x, y, world, rng, difficulty=0):
        super().__init__(x, y, world, "npc_jeweler")
        self._rng = rng
        self.difficulty = difficulty
        self._streak = 0
        self.quests = [_build_gem_quest(rng, difficulty), _build_gem_quest(rng, difficulty)]

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
        needed = quest.get("count", 1)
        return len(self.find_matching_gems(player, quest)) >= needed

    def complete_quest(self, player, quest_idx=0):
        quest = self.quests[quest_idx]
        needed = quest.get("count", 1)
        matching = self.find_matching_gems(player, quest)
        if len(matching) < needed:
            return False
        for i in sorted(matching[:needed], reverse=True):
            player.gems.pop(i)
        self._streak += 1
        streak_mult = 1.0 + min(self._streak - 1, 2) * 0.25
        player.money += int(quest["reward"] * streak_mult * getattr(player, "blessing_mult", 1.0))
        self.quests[quest_idx] = _build_gem_quest(self._rng, self.difficulty)
        return True


# ---------------------------------------------------------------------------
# Merchant / Restaurant / Shrine data
# ---------------------------------------------------------------------------

MERCHANT_SHOP_TABLE = [
    ("iron_chunk",       8,  "Iron Chunk"),
    ("coal",            12,  "Coal"),
    ("lumber",          10,  "Lumber"),
    ("wool",            15,  "Wool"),
    ("crystal_shard",   40,  "Crystal Shard"),
    ("stone_chip",       5,  "Stone Chip"),
    ("obsidian_slab",   50,  "Obsidian Slab"),
    ("ruby",            70,  "Ruby"),
    ("milk",            18,  "Milk"),
    ("tempered_iron",   60,  "Tempered Iron"),
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
}

SHRINE_FLAVOR = {
    "dzong":           "Prayer flags snap in the mountain wind.\nThe whitewashed walls glow against dark peaks.\nBells toll somewhere above the clouds.",
    "temple":          "Incense drifts through stone archways.\nMonks chant in quiet reverence.",
    "chapel":          "Sunlight filters through the canopy above.\nA small bell hangs in the doorway.\nThe wood is worn smooth by many hands.",
    "desert_shrine":   "Carved stone glows in the desert heat.\nOld prayers are scratched into the walls.\nA clay bowl holds the remains of an offering.",
    "jungle_shrine":   "Moss clings to ancient carvings.\nThe air hums with the sound of insects.\nSomething watches from between the stones.",
    "standing_stones": "Weathered stones stand in a silent row.\nNames are carved in a forgotten tongue.\nThe ground between them never grows grass.",
}


class MerchantNPC(NPC):
    def __init__(self, x, y, world, rng):
        super().__init__(x, y, world, "npc_merchant")
        n = rng.randint(3, 4)
        self.shop = rng.sample(MERCHANT_SHOP_TABLE, n)

    def can_buy(self, idx, player):
        _, cost, _ = self.shop[idx]
        return player.money >= cost

    def execute_purchase(self, idx, player):
        if not self.can_buy(idx, player):
            return False
        item_id, cost, _ = self.shop[idx]
        player.money -= cost
        player._add_item(item_id)
        return True


class RestaurantNPC(NPC):
    def __init__(self, x, y, world, rng):
        super().__init__(x, y, world, "npc_chef")
        self.cuisine = rng.choice(list(CUISINE_MENUS.keys()))
        self.menu = CUISINE_MENUS[self.cuisine]

    def can_buy(self, idx, player):
        _, cost = self.menu[idx]
        return player.money >= cost

    def execute_purchase(self, idx, player):
        if not self.can_buy(idx, player):
            return False
        item_id, cost = self.menu[idx]
        player.money -= cost
        player._add_item(item_id)
        return True


class ShrineKeeperNPC(NPC):
    def __init__(self, x, y, world, rng, difficulty=0, biodome="temperate"):
        super().__init__(x, y, world, "npc_monk")
        display_name, style = RELIGION_BY_BIOME.get(biodome, ("Forest Chapel", "chapel"))
        self.religion_name = display_name
        self.religion_style = style
        self.flavor = SHRINE_FLAVOR.get(style, SHRINE_FLAVOR["chapel"])
        self.blessing_cost = 10 + difficulty * 10

    def can_bless(self, player):
        return player.money >= self.blessing_cost

    def give_blessing(self, player):
        if not self.can_bless(player):
            return False
        player.money -= self.blessing_cost
        player.blessing_timer = 180.0
        player.blessing_mult = 1.25
        return True


class JewelryMerchantNPC(NPC):
    """Buys custom jewelry pieces from the player."""
    def __init__(self, x, y, world, rng):
        super().__init__(x, y, world, "npc_merchant")
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


# ---------------------------------------------------------------------------
# City generation
# ---------------------------------------------------------------------------

_DESERT_BIOMES    = {"desert", "arid_steppe", "savanna"}
_DESERT_PALETTE   = (SANDSTONE_BLOCK, POLISHED_MARBLE)
_DOME_SWAP        = {"house": "dome", "two_story": "dome", "longhouse": "dome"}

_HIMALAYAN_BIOMES = {"alpine_mountain", "tundra"}
_HIMALAYAN_PALETTE = (WHITEWASHED_WALL, MONASTERY_ROOF)
_HIMALAYAN_SWAP   = {"house": "himalayan", "two_story": "himalayan", "longhouse": "himalayan"}

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
    },
    "medium": {
        "half_w": 26,
        "buildings": [
            (-25, (4, 6), (3, 5), ["house", "two_story", "tower", "ruin", "longhouse", "pavilion"]),
            (-17, (4, 6), (3, 4), ["house", "house", "two_story", "longhouse", "ruin", "market_stall"]),
            ( -8, (4, 5), (3, 4), ["restaurant"]),
            (  0, None,   None,   None),    # outdoor NPC at city centre — sits in the town square
            (  5, (4, 6), (3, 4), ["house", "house", "two_story", "ruin", "tower", "market_stall", "well"]),
            ( 13, (4, 6), (3, 5), ["house", "two_story", "tower", "longhouse", "ruin", "pavilion"]),
            ( 19, (6, 7), (5, 7), ["shrine"]),
        ],
        "npc_types": ["quest_rock", "quest_wildflower", "restaurant_npc",
                      "merchant", "quest_gem", "trade", "shrine_npc"],
        "gardens": [(-21, 2), (-12, 2), (16, 2)],
        # (center_offset, half_w) — paved plaza with a centre sculpture.
        "squares": [(0, 4)],
    },
    "large": {
        "half_w": 36,
        "buildings": [
            (-35, (5, 7), (4, 5), ["house", "two_story", "two_story", "tower", "longhouse", "pavilion"]),
            (-27, (4, 6), (3, 5), ["house", "house", "ruin", "tower", "two_story", "market_stall", "well"]),
            (-19, (4, 5), (3, 4), ["house", "house", "two_story", "ruin", "longhouse", "pavilion"]),
            (-10, None,   None,   None),    # outdoor NPC — main-street left, sits in left square
            ( -2, (4, 5), (3, 4), ["house", "two_story", "ruin", "tower", "longhouse", "market_stall"]),
            (  5, (4, 5), (3, 4), ["restaurant"]),
            ( 13, None,   None,   None),    # outdoor NPC — main-street right, sits in right square
            ( 18, (4, 6), (3, 5), ["house", "house", "tower", "ruin", "two_story", "market_stall", "well"]),
            ( 26, (7, 9), (5, 7), ["shrine"]),
        ],
        "npc_types": ["quest_rock", "quest_wildflower", "trade", "merchant",
                      "quest_gem", "restaurant_npc", "quest_wildflower", "trade",
                      "shrine_npc", "jewelry_merchant"],
        "gardens": [(-31, 2), (-23, 2), (22, 2)],
        "squares": [(-10, 4), (13, 4)],
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
}

_FOUNTAIN_BLOCKS = (BUBBLE_FOUNTAIN, SHELL_FOUNTAIN, MILLSTONE_FOUNTAIN,
                    CHERUB_FOUNTAIN, MOSAIC_FOUNTAIN, LION_HEAD_FOUNTAIN)


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
    # Corner columns only — sides stay open.
    for wy in range(sy - h, sy):
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
    well_y = sy - 1
    if 0 <= well_y < world.height:
        world.set_block(left_x, well_y, COBBLESTONE)
        world.set_block(left_x + width - 1, well_y, COBBLESTONE)
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
            is_door  = (wy >= sy - 2) and (is_left or is_right)
            if is_door:
                world.set_block(wx, wy, WOOD_DOOR_CLOSED)
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

    # Side posts (solid).
    for wy in range(sy - h, sy):
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
            # Top half of the side walls is broken away.
            broken_top = wy < sy - wall_height + 2
            if (is_left or is_right) and not broken_top:
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
                world.set_block(wx, wy, WOOD_DOOR_CLOSED)
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
                world.set_block(wx, wy, WOOD_DOOR_CLOSED)
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


def _place_restaurant(world, left_x, sy, width, wall_height):
    """Restaurant: hollow interior, doors on both sides, flat crimson awning (no peak)."""
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
                world.set_block(wx, wy, WOOD_DOOR_CLOSED)
            elif is_top or is_left_side or is_right_side:
                world.set_block(wx, wy, RESTAURANT_WALL)
            else:
                world.set_block(wx, wy, AIR)
                world.set_bg_block(wx, wy, RESTAURANT_WALL)

    # Flat awning overhang (wider than normal, no peak — distinctive canopy look)
    awning_y = sy - wall_height - 1
    for rx in range(left_x - 2, left_x + width + 2):
        if 0 <= awning_y < world.height:
            world.set_block(rx, awning_y, RESTAURANT_AWNING)


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
                world.set_block(wx, wy, WOOD_DOOR_CLOSED)
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
                world.set_block(wx, wy, WOOD_DOOR_CLOSED)
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
                world.set_block(wx, wy, WOOD_DOOR_CLOSED)
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

    # Bell tower: one column above the roof peak
    peak_y = base_y - half
    for by in range(peak_y - 2, peak_y):
        if 0 <= by < world.height:
            world.set_block(center, by, HOUSE_WALL)


def _place_desert_shrine(world, left_x, sy, width, wall_height):
    """Open-sided shrine with stone columns and a wide flat overhanging roof."""
    col_positions = {left_x, left_x + width // 2, left_x + width - 1}
    for wy in range(sy - wall_height, sy):
        for wx in range(left_x, left_x + width):
            if not (0 <= wy < world.height):
                continue
            if wx in col_positions:
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
                world.set_block(wx, wy, WOOD_DOOR_CLOSED)
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
                world.set_block(wx, wy, WOOD_DOOR_CLOSED)
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


def _build_single_city(world, rng, city_bx, difficulty):
    sy = world.surface_y_at(city_bx)
    biodome = world.biodome_at(city_bx)
    city_size = rng.choice(_SIZE_BY_DIFFICULTY[difficulty])
    cfg = CITY_CONFIGS[city_size]
    half_w = cfg["half_w"]

    world.city_zones.append((city_bx - half_w, city_bx + half_w))

    # Pre-load every chunk the city footprint touches so set_block never silently fails
    chunk_lo = (city_bx - half_w - 4) // CHUNK_W
    chunk_hi = (city_bx + half_w + 4) // CHUNK_W
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

    is_desert    = biodome in _DESERT_BIOMES
    is_himalayan = biodome in _HIMALAYAN_BIOMES

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
                _place_restaurant(world, left_x, sy, width, height)
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
            world.entities.append(RockQuestNPC(npc_px, npc_py, world, rng, difficulty))
        elif npc_type == "trade":
            world.entities.append(TradeNPC(npc_px, npc_py, world, rng))
        elif npc_type == "quest_wildflower":
            world.entities.append(WildflowerQuestNPC(npc_px, npc_py, world, rng, difficulty))
        elif npc_type == "quest_gem":
            world.entities.append(GemQuestNPC(npc_px, npc_py, world, rng, difficulty))
        elif npc_type == "merchant":
            world.entities.append(MerchantNPC(npc_px, npc_py, world, rng))
        elif npc_type == "restaurant_npc":
            world.entities.append(RestaurantNPC(npc_px, npc_py, world, rng))
        elif npc_type == "shrine_npc":
            world.entities.append(ShrineKeeperNPC(npc_px, npc_py, world, rng, difficulty, biodome))
        elif npc_type == "jewelry_merchant":
            world.entities.append(JewelryMerchantNPC(npc_px, npc_py, world, rng))

    # Town squares — paved plazas with a sculpture centerpiece, around outdoor NPC slots.
    for offset, half in cfg.get("squares", ()):
        _place_town_square(world, rng, city_bx + offset, sy, biodome, half)

    # Garden plots between buildings — placed last so they don't get overwritten.
    for offset, half in cfg.get("gardens", ()):
        _place_garden_plot(world, rng, city_bx + offset, sy, biodome, half)

    # Cobbled main street + lamps + entry gateposts wrap up the city.
    _pave_main_street(world, rng, city_bx - half_w, city_bx + half_w, sy)
    _place_streetlamps(world, rng, city_bx - half_w + 2,
                       city_bx + half_w - 2, sy)
    _place_gateposts(world, rng, city_bx - half_w, city_bx + half_w, sy)


def generate_cities(world, seed):
    rng = random.Random(seed + 77777)
    placed = 0
    x = -(CITY_COUNT // 2) * CITY_SPACING + CITY_SPACING // 2
    world.city_zones = []

    while placed < CITY_COUNT:
        jitter = rng.randint(-6, 6)
        city_bx = x + jitter
        difficulty = min(placed // 2, 2)
        _build_single_city(world, rng, city_bx, difficulty)
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
    rng = random.Random(seed + slot_x * 9001 + 33333)
    jitter = rng.randint(-6, 6)
    city_bx = slot_x + jitter
    if any(lo - 10 <= city_bx <= hi + 10 for lo, hi in world.city_zones):
        return
    _build_single_city(world, rng, city_bx, 2)
