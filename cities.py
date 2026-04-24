import math
import random

from blocks import (STONE, BEDROCK, HOUSE_WALL, HOUSE_ROOF, AIR, LADDER,
                    HOUSE_WALL_STONE, HOUSE_ROOF_STONE,
                    HOUSE_WALL_BRICK, HOUSE_ROOF_BRICK,
                    HOUSE_WALL_DARK,  HOUSE_ROOF_DARK,
                    RESTAURANT_WALL, RESTAURANT_AWNING,
                    SANDSTONE_BLOCK, POLISHED_MARBLE,
                    WHITEWASHED_WALL, MONASTERY_ROOF, MANI_STONE, PRAYER_FLAG_BLOCK,
                    WOOD_DOOR_CLOSED, ALL_LOGS, ALL_LEAVES, BUSH_BLOCKS, SAPLING)
from constants import BLOCK_SIZE, PLAYER_W, PLAYER_H, CITY_SPACING, CITY_COUNT, NPC_INTERACT_RANGE, CHUNK_W
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
    (HOUSE_WALL,       HOUSE_ROOF),        # warm wood
    (HOUSE_WALL_STONE, HOUSE_ROOF_STONE),  # grey stone
    (HOUSE_WALL_BRICK, HOUSE_ROOF_BRICK),  # red brick
    (HOUSE_WALL_DARK,  HOUSE_ROOF_DARK),   # dark timber
]

# Building slot format: (offset_from_cx, (min_w, max_w), (min_h, max_h), variants)
# variants is a list sampled uniformly; repeat entries to weight them.
# Use (offset, None, None, None) for an outdoor NPC slot with no building.
# Variants: "house", "two_story", "tower", "longhouse", "ruin", "restaurant", "shrine"
CITY_CONFIGS = {
    "small": {
        "half_w": 16,
        "buildings": [
            (-15, (4, 6), (3, 5), ["house", "house", "two_story", "tower", "ruin"]),
            ( -3, (4, 5), (3, 4), ["restaurant"]),
            (  5, (4, 6), (3, 5), ["house", "house", "two_story", "longhouse", "ruin"]),
        ],
        "npc_types": ["quest_rock", "restaurant_npc", "merchant"],
    },
    "medium": {
        "half_w": 26,
        "buildings": [
            (-25, (4, 6), (3, 5), ["house", "two_story", "tower", "ruin", "longhouse"]),
            (-17, (4, 6), (3, 4), ["house", "house", "two_story", "longhouse", "ruin"]),
            ( -8, (4, 5), (3, 4), ["restaurant"]),
            (  0, None,   None,   None),    # outdoor NPC at city center
            (  5, (4, 6), (3, 4), ["house", "house", "two_story", "ruin", "tower"]),
            ( 13, (4, 6), (3, 5), ["house", "two_story", "tower", "longhouse", "ruin"]),
            ( 19, (6, 7), (5, 7), ["shrine"]),
        ],
        "npc_types": ["quest_rock", "quest_wildflower", "restaurant_npc",
                      "merchant", "quest_gem", "trade", "shrine_npc"],
    },
    "large": {
        "half_w": 36,
        "buildings": [
            (-35, (5, 7), (4, 5), ["house", "two_story", "two_story", "tower", "longhouse"]),
            (-27, (4, 6), (3, 5), ["house", "house", "ruin", "tower", "two_story"]),
            (-19, (4, 5), (3, 4), ["house", "house", "two_story", "ruin", "longhouse"]),
            (-10, None,   None,   None),    # outdoor NPC — main-street left
            ( -2, (4, 5), (3, 4), ["house", "two_story", "ruin", "tower", "longhouse"]),
            (  5, (4, 5), (3, 4), ["restaurant"]),
            ( 13, None,   None,   None),    # outdoor NPC — main-street right
            ( 18, (4, 6), (3, 5), ["house", "house", "tower", "ruin", "two_story"]),
            ( 26, (7, 9), (5, 7), ["shrine"]),
        ],
        "npc_types": ["quest_rock", "quest_wildflower", "trade", "merchant",
                      "quest_gem", "restaurant_npc", "quest_wildflower", "trade",
                      "shrine_npc"],
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
        elif npc_type == "merchant":
            world.entities.append(MerchantNPC(npc_px, npc_py, world, rng))
        elif npc_type == "restaurant_npc":
            world.entities.append(RestaurantNPC(npc_px, npc_py, world, rng))
        elif npc_type == "shrine_npc":
            world.entities.append(ShrineKeeperNPC(npc_px, npc_py, world, rng, difficulty, biodome))


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
