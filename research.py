from blocks import GATE_MID, GATE_DEEP, GATE_CORE, STONE


class ResearchNode:
    def __init__(self, node_id, name, description, cost, prerequisites, effect_fn, money_cost=0):
        self.id = node_id
        self.name = name
        self.description = description
        self.cost = cost              # {item_id: count}
        self.prerequisites = prerequisites  # [node_id, ...]
        self._effect_fn = effect_fn
        self.money_cost = money_cost
        self.unlocked = False

    def apply(self, player, world):
        self._effect_fn(player, world)
        self.unlocked = True


def _set_pick(tier):
    def effect(player, world):
        if player.pick_power < tier:
            player.pick_power = tier
    return effect


def _add_pick(amount):
    def effect(player, world):
        player.pick_power += amount
    return effect


def _unlock_gate(gate_block):
    from constants import CHUNK_W, WORLD_H
    def effect(player, world):
        for cx, chunk in list(world._chunks.items()):
            for y in range(WORLD_H):
                for lx in range(CHUNK_W):
                    if chunk[y][lx] == gate_block:
                        chunk[y][lx] = STONE
                        world._dirty_chunks.add(cx)
    return effect


class ResearchTree:
    COLUMNS = ["Pickaxe Upgrades", "Mining Speed", "Zone Access"]

    def __init__(self):
        self.nodes = {}    # id -> ResearchNode
        self.layout = []   # [(col, row, node_id), ...]
        self._build()

    def apply_save(self, unlocked_ids):
        for node_id in unlocked_ids:
            if node_id in self.nodes:
                self.nodes[node_id].unlocked = True

    def _add(self, node, col, row):
        self.nodes[node.id] = node
        self.layout.append((col, row, node.id))

    def _build(self):
        # --- Pickaxe tiers (column 0) ---
        self._add(ResearchNode(
            "iron_pick", "Iron Pickaxe",
            "Faster mining through tough rock",
            {"stone_chip": 5, "iron_chunk": 3}, [],
            _set_pick(2), money_cost=10), 0, 0)

        self._add(ResearchNode(
            "gold_pick", "Gold Pickaxe",
            "Golden efficiency in deep stone",
            {"iron_chunk": 3, "gold_nugget": 2}, ["iron_pick"],
            _set_pick(3), money_cost=30), 0, 1)

        self._add(ResearchNode(
            "crystal_pick", "Crystal Pickaxe",
            "Crystal clarity cuts anything",
            {"gold_nugget": 2, "crystal_shard": 1}, ["gold_pick"],
            _set_pick(4), money_cost=60), 0, 2)

        self._add(ResearchNode(
            "ruby_pick", "Ruby Pickaxe",
            "Red-hot cutting power",
            {"crystal_shard": 1, "ruby": 1}, ["crystal_pick"],
            _set_pick(5), money_cost=100), 0, 3)

        self._add(ResearchNode(
            "obsidian_pick", "Obsidian Pickaxe",
            "The ultimate mining tool",
            {"ruby": 1, "obsidian_slab": 1}, ["ruby_pick"],
            _set_pick(6), money_cost=150), 0, 4)

        # --- Speed upgrades (column 1) ---
        self._add(ResearchNode(
            "swift_1", "Swift Mining I",
            "Improved technique boosts dig speed",
            {"coal": 3}, [],
            _add_pick(0.5), money_cost=5), 1, 0)

        self._add(ResearchNode(
            "swift_2", "Swift Mining II",
            "Refined motion, even faster results",
            {"coal": 5, "iron_chunk": 2}, ["swift_1"],
            _add_pick(0.5), money_cost=20), 1, 1)

        # --- Zone access (column 2) ---
        self._add(ResearchNode(
            "mid_access", "Mid Zone Access",
            "Shatters the barrier to mid depths",
            {"coal": 5}, [],
            _unlock_gate(GATE_MID), money_cost=15), 2, 0)

        self._add(ResearchNode(
            "deep_access", "Deep Zone Access",
            "Opens passage to the deep",
            {"iron_chunk": 3}, ["mid_access"],
            _unlock_gate(GATE_DEEP), money_cost=40), 2, 1)

        self._add(ResearchNode(
            "core_access", "Core Zone Access",
            "Descend to the planet's core",
            {"gold_nugget": 2}, ["deep_access"],
            _unlock_gate(GATE_CORE), money_cost=80), 2, 2)

    def prereqs_met(self, node_id):
        return all(self.nodes[p].unlocked for p in self.nodes[node_id].prerequisites)

    def can_unlock(self, node_id, inventory, money=0):
        node = self.nodes[node_id]
        if node.unlocked:
            return False
        if not self.prereqs_met(node_id):
            return False
        if money < node.money_cost:
            return False
        return all(inventory.get(item_id, 0) >= needed
                   for item_id, needed in node.cost.items())

    def unlock(self, node_id, player, world):
        if not self.can_unlock(node_id, player.inventory, player.money):
            return False
        node = self.nodes[node_id]
        for item_id, needed in node.cost.items():
            player.inventory[item_id] -= needed
        player.money -= node.money_cost
        node.apply(player, world)
        return True
