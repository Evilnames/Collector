import math
import random

from blocks import (STONE, NPC_QUEST_BLOCK, NPC_TRADE_BLOCK, BEDROCK,
                    HOUSE_WALL, HOUSE_ROOF, AIR,
                    ALL_LOGS, ALL_LEAVES, BUSH_BLOCKS, SAPLING)
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

# Special properties that can appear in quests
QUEST_SPECIALS = ["luminous", "magnetic", "crystalline", "resonant", "voidtouched"]
SPECIAL_REWARD = {
    "luminous":    20,
    "magnetic":    18,
    "crystalline": 25,
    "resonant":    32,
    "voidtouched": 50,
}

# Per-difficulty: which rarities can be requested
DIFFICULTY_RARITY = {
    0: ["common", "uncommon"],
    1: ["common", "uncommon", "rare"],
    2: ["uncommon", "rare", "epic", "legendary"],
}

# Per-difficulty: weighted pool of quest kinds to pick from
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
        self._bob_timer += dt
        self._bob_offset = math.sin(self._bob_timer * 1.5) * 1.5

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


def _quest_candidates(rng, difficulty):
    """Pick a rock type whose rarity pool overlaps the difficulty's allowed rarities."""
    allowed = set(DIFFICULTY_RARITY[difficulty])
    max_depth = 40 + difficulty * 50
    candidates = [
        k for k, v in ROCK_TYPES.items()
        if v["min_depth"] <= max_depth and any(r in allowed for r in v["rarity_pool"])
    ]
    return candidates if candidates else list(ROCK_TYPES.keys())


def _build_quest(rng, difficulty):
    """Return a quest dict for the given difficulty tier."""
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
        # Request the upper half of the difficulty's rarity range
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
    """Return a short human-readable description of a quest dict."""
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
    """Return a secondary hint line for depth/rarity context."""
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


class RockQuestNPC(NPC):
    def __init__(self, x, y, world, rng, difficulty=0):
        super().__init__(x, y, world, "npc_quest")
        self._rng = rng
        self.difficulty = difficulty
        self._streak = 0
        # Two simultaneously active quests
        self.quests = [_build_quest(rng, difficulty), _build_quest(rng, difficulty)]

    # Returns list of player.rocks indices that satisfy the quest
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
        # Remove oldest-found rocks first (lowest index)
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


def _place_house(world, left_x, sy, width, wall_height, facing='right'):
    """
    Build a house on the city platform. Walls use HOUSE_WALL (not a physics block),
    so they won't collapse. A door opening faces inward toward the city centre.
    """
    door_col = left_x + width - 2 if facing == 'right' else left_x + 1

    # Walls — solid except for 1-wide, 2-tall door opening
    for wy in range(sy - wall_height, sy):
        for wx in range(left_x, left_x + width):
            is_door = (wx == door_col and wy >= sy - 2)
            if not is_door and 0 <= wy < world.height:
                world.set_block(wx, wy, HOUSE_WALL)

    # Flat roof overhang (1 block wider each side, 1 row above walls)
    roof_y = sy - wall_height - 1
    for rx in range(left_x - 1, left_x + width + 1):
        if 0 <= roof_y < world.height:
            world.set_block(rx, roof_y, HOUSE_ROOF)

    # Peaked ridge (same width as walls, 1 row above overhang)
    peak_y = roof_y - 1
    for rx in range(left_x, left_x + width):
        if 0 <= peak_y < world.height:
            world.set_block(rx, peak_y, HOUSE_ROOF)


_CITY_HALF_WIDTH = 7  # platform extends cx±7
_PLANT_BLOCKS = ALL_LOGS | ALL_LEAVES | BUSH_BLOCKS | {SAPLING}


def generate_cities(world, seed):
    rng = random.Random(seed + 77777)
    placed = 0
    # Centre cities around x=0: e.g. 4 cities → -180, -60, 60, 180
    x = -(CITY_COUNT // 2) * CITY_SPACING + CITY_SPACING // 2
    world.city_zones = []  # list of (min_x, max_x) used by sapling-grow checks

    while placed < CITY_COUNT:
        jitter = rng.randint(-6, 6)
        cx = x + jitter
        sy = world.surface_y_at(cx)

        # Difficulty scales with city index: 0→0, 1→0, 2→1, 3→1, 4→2, 5→2
        difficulty = min(placed // 2, 2)

        world.city_zones.append((cx - _CITY_HALF_WIDTH, cx + _CITY_HALF_WIDTH))

        # Clear all vegetation above the city footprint so no trees poke through
        _CLEAR_HEIGHT = 25
        for bx in range(cx - _CITY_HALF_WIDTH, cx + _CITY_HALF_WIDTH + 1):
            for by in range(max(0, sy - _CLEAR_HEIGHT), sy):
                if world.get_block(bx, by) in _PLANT_BLOCKS:
                    world.set_block(bx, by, AIR)

        # Stone platform (14 blocks wide)
        for bx in range(cx - 7, cx + 8):
            if world.get_block(bx, sy) != BEDROCK:
                world.set_block(bx, sy, STONE)

        # Two houses flanking the NPC plaza (doors face the city centre)
        _place_house(world, cx - 7, sy, width=4, wall_height=3, facing='right')
        _place_house(world, cx + 4, sy, width=4, wall_height=3, facing='left')

        # NPC marker columns (2 blocks tall): quest on left, trade on right
        quest_bx = cx - 3
        trade_bx = cx + 3
        for dy in [1, 2]:
            qby = sy - dy
            if 0 <= qby < world.height:
                world.set_block(quest_bx, qby, NPC_QUEST_BLOCK)
            tby = sy - dy
            if 0 <= tby < world.height:
                world.set_block(trade_bx, tby, NPC_TRADE_BLOCK)

        # NPC entities positioned one block above marker columns
        npc_py = (sy - 3) * BLOCK_SIZE

        qx_px = quest_bx * BLOCK_SIZE + (BLOCK_SIZE - NPC.NPC_W) // 2
        world.entities.append(RockQuestNPC(qx_px, npc_py, world, rng, difficulty))

        tx_px = trade_bx * BLOCK_SIZE + (BLOCK_SIZE - NPC.NPC_W) // 2
        world.entities.append(TradeNPC(tx_px, npc_py, world, rng))

        placed += 1
        x += CITY_SPACING
