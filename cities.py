import math
import random

from blocks import (STONE, BEDROCK, HOUSE_WALL, HOUSE_ROOF, AIR, LADDER,
                    HOUSE_WALL_STONE, HOUSE_ROOF_STONE,
                    HOUSE_WALL_BRICK, HOUSE_ROOF_BRICK,
                    HOUSE_WALL_DARK,  HOUSE_ROOF_DARK,
                    WOOD_DOOR_CLOSED, ALL_LOGS, ALL_LEAVES, BUSH_BLOCKS, SAPLING)
from constants import BLOCK_SIZE, PLAYER_W, PLAYER_H, CITY_SPACING, CITY_COUNT, NPC_INTERACT_RANGE
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
        from ui import RARITY_LABEL
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
        from ui import RARITY_LABEL
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
        from ui import RARITY_LABEL
        label = RARITY_LABEL.get(quest["rarity"], quest["rarity"])
        return f"{label} {quest['rock_type'].replace('_', ' ').title()}"
    elif quest["kind"] == "any_rarity":
        from ui import RARITY_LABEL
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
        self.world = world
        self.animal_id = npc_id
        self._bob_timer = 0.0
        self._bob_offset = 0.0

    @property
    def rect(self):
        import pygame
        return pygame.Rect(int(self.x), int(self.y), self.NPC_W, self.NPC_H)

    def update(self, dt):
        pass

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
        player.money += int(quest["reward"] * streak_mult)
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
        player.money += int(quest["reward"] * streak_mult)
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
        player.money += int(quest["reward"] * streak_mult)
        self.quests[quest_idx] = _build_gem_quest(self._rng, self.difficulty)
        return True


# ---------------------------------------------------------------------------
# City generation
# ---------------------------------------------------------------------------

# Building style palettes: (wall_block, roof_block)
BUILDING_PALETTES = [
    (HOUSE_WALL,       HOUSE_ROOF),        # warm wood
    (HOUSE_WALL_STONE, HOUSE_ROOF_STONE),  # grey stone
    (HOUSE_WALL_BRICK, HOUSE_ROOF_BRICK),  # red brick
    (HOUSE_WALL_DARK,  HOUSE_ROOF_DARK),   # dark timber
]

# Building slot format: (offset_from_cx, (min_w, max_w), (min_h, max_h), variants)
# variants is a list sampled uniformly; repeat entries to weight them.
# Use (offset, None, None, None) for an outdoor NPC slot with no building.
# Variants: "house", "two_story", "tower", "longhouse", "ruin"
CITY_CONFIGS = {
    "small": {
        "half_w": 11,
        "buildings": [
            (-10, (4, 6), (3, 5), ["house", "house", "two_story", "tower", "ruin"]),
            (  4, (4, 6), (3, 5), ["house", "house", "two_story", "longhouse", "ruin"]),
        ],
        "npc_types": ["quest_rock", "trade"],
    },
    "medium": {
        "half_w": 18,
        "buildings": [
            (-17, (4, 6), (3, 5), ["house", "two_story", "tower", "ruin", "longhouse"]),
            (-10, (4, 6), (3, 4), ["house", "house", "two_story", "longhouse", "ruin"]),
            (  0, None,   None,   None),    # outdoor NPC at city center
            (  4, (4, 6), (3, 4), ["house", "house", "two_story", "ruin", "tower"]),
            ( 11, (4, 6), (3, 5), ["house", "two_story", "tower", "longhouse", "ruin"]),
        ],
        "npc_types": ["quest_rock", "quest_wildflower", "trade", "quest_gem", "trade"],
    },
    "large": {
        "half_w": 26,
        "buildings": [
            (-25, (5, 7), (4, 5), ["house", "two_story", "two_story", "tower", "longhouse"]),
            (-17, (4, 6), (3, 5), ["house", "house", "ruin", "tower", "two_story"]),
            (-10, (4, 5), (3, 4), ["house", "house", "two_story", "ruin", "longhouse"]),
            ( -2, None,   None,   None),    # outdoor NPC — main-street left
            (  4, (4, 5), (3, 4), ["house", "two_story", "ruin", "tower", "longhouse"]),
            ( 10, (4, 6), (3, 5), ["house", "house", "tower", "ruin", "two_story"]),
            ( 17, None,   None,   None),    # outdoor NPC — main-street right
            ( 20, (5, 7), (4, 5), ["house", "two_story", "two_story", "tower", "longhouse"]),
        ],
        "npc_types": ["quest_rock", "quest_wildflower", "trade", "trade",
                      "quest_gem", "trade", "quest_wildflower", "quest_rock"],
    },
}

_SIZE_BY_DIFFICULTY = {
    0: ["small", "small", "medium"],
    1: ["medium", "medium", "large"],
    2: ["large", "large", "medium"],
}

_PLANT_BLOCKS = ALL_LOGS | ALL_LEAVES | BUSH_BLOCKS | {SAPLING}


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


def generate_cities(world, seed):
    rng = random.Random(seed + 77777)
    placed = 0
    x = -(CITY_COUNT // 2) * CITY_SPACING + CITY_SPACING // 2
    world.city_zones = []

    while placed < CITY_COUNT:
        jitter = rng.randint(-6, 6)
        cx = x + jitter
        sy = world.surface_y_at(cx)

        difficulty = min(placed // 2, 2)
        city_size  = rng.choice(_SIZE_BY_DIFFICULTY[difficulty])
        cfg        = CITY_CONFIGS[city_size]
        half_w     = cfg["half_w"]

        world.city_zones.append((cx - half_w, cx + half_w))

        # Clear vegetation above city footprint
        for bx in range(cx - half_w - 2, cx + half_w + 3):
            for by in range(max(0, sy - 35), sy):
                if world.get_block(bx, by) in _PLANT_BLOCKS:
                    world.set_block(bx, by, AIR)

        # Stone platform
        for bx in range(cx - half_w, cx + half_w + 1):
            if world.get_block(bx, sy) != BEDROCK:
                world.set_block(bx, sy, STONE)

        # Build structures and place NPCs
        for (offset, w_range, h_range, variants), npc_type in zip(cfg["buildings"], cfg["npc_types"]):
            left_x = cx + offset
            wall_block, roof_block = rng.choice(BUILDING_PALETTES)

            if w_range is None:
                # Outdoor NPC — no building
                npc_bx = left_x
            else:
                width   = rng.randint(*w_range)
                height  = rng.randint(*h_range)
                variant = rng.choice(variants) if variants else "house"

                if variant == "two_story":
                    floor2_h = rng.randint(2, 3)
                    _place_house_two_story(world, left_x, sy, width, height, floor2_h,
                                           wall_block, roof_block)
                else:
                    _place_house(world, left_x, sy, width, height, wall_block, roof_block)

                npc_bx = left_x + 1

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

        placed += 1
        x += CITY_SPACING
