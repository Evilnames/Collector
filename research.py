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


def _noop(player, world):
    pass


class ResearchTree:
    COLUMNS = ["Mining Speed", "Zone Access", "Farming", "Coffee", "Birding"]

    def __init__(self):
        self.nodes = {}    # id -> ResearchNode
        self.layout = []   # [(col, row, node_id), ...]
        self._build()

    def apply_save(self, unlocked_ids):
        for node_id in unlocked_ids:
            if node_id in self.nodes:
                self.nodes[node_id].unlocked = True

    def apply_bonuses(self, player):
        """Set all research-derived bonuses on player from current unlock state."""
        def u(nid):
            n = self.nodes.get(nid)
            return n is not None and n.unlocked

        player.crop_grow_bonus           = 0.12 if u("irrigation")        else 0.0
        player.harvest_bonus             = 1    if u("composting")         else 0
        player.roast_quality_bonus       = 0.15 if u("roast_mastery")      else 0.0
        player.coffee_buff_duration_bonus = 0.5 if u("master_barista")     else 0.0
        player.bird_spook_reduction      = 0.4  if u("bird_sanctuary")     else 0.0
        player.bird_feeder_bonus         = 2.0  if u("bird_lure")          else 1.0
        player.avian_mastery             = u("avian_mastery")

    def _add(self, node, col, row):
        self.nodes[node.id] = node
        self.layout.append((col, row, node.id))

    def _build(self):
        # --- Mining Speed (column 0) ---
        self._add(ResearchNode(
            "swift_1", "Swift Mining I",
            "Improved technique boosts dig speed",
            {"coal": 3}, [],
            _add_pick(0.5), money_cost=5), 0, 0)

        self._add(ResearchNode(
            "swift_2", "Swift Mining II",
            "Refined motion, even faster results",
            {"coal": 5, "iron_chunk": 2}, ["swift_1"],
            _add_pick(0.5), money_cost=20), 0, 1)

        # --- Zone Access (column 1) ---
        self._add(ResearchNode(
            "mid_access", "Mid Zone Access",
            "Shatters the barrier to mid depths",
            {"coal": 5}, [],
            _unlock_gate(GATE_MID), money_cost=15), 1, 0)

        self._add(ResearchNode(
            "deep_access", "Deep Zone Access",
            "Opens passage to the deep",
            {"iron_chunk": 3}, ["mid_access"],
            _unlock_gate(GATE_DEEP), money_cost=40), 1, 1)

        self._add(ResearchNode(
            "core_access", "Core Zone Access",
            "Descend to the planet's core",
            {"gold_nugget": 2}, ["deep_access"],
            _unlock_gate(GATE_CORE), money_cost=80), 1, 2)

        # --- Farming (column 2) ---
        self._add(ResearchNode(
            "soil_prep", "Soil Preparation",
            "Basic farming — unlocks Farm Bot",
            {"dirt_clump": 8, "wheat": 3}, [],
            _noop, money_cost=5), 2, 0)

        self._add(ResearchNode(
            "irrigation", "Irrigation",
            "Water channels make crops mature 80% faster",
            {"stone_chip": 5, "carrot": 3}, ["soil_prep"],
            _noop, money_cost=15), 2, 1)

        self._add(ResearchNode(
            "composting", "Composting",
            "Rich soil yields +1 extra produce per harvest",
            {"dirt_clump": 15, "carrot": 5}, ["irrigation"],
            _noop, money_cost=25), 2, 2)

        self._add(ResearchNode(
            "selective_breeding", "Selective Breeding",
            "Advanced crops — unlocks Iron Farm Bot",
            {"iron_chunk": 3, "wheat": 5}, ["composting"],
            _noop, money_cost=40), 2, 3)

        self._add(ResearchNode(
            "agri_automation", "Advanced Agriculture",
            "Full automation — unlocks Crystal Farm Bot",
            {"gold_nugget": 2, "corn": 5}, ["selective_breeding"],
            _noop, money_cost=70), 2, 4)

        # --- Coffee (column 3) ---
        self._add(ResearchNode(
            "coffee_basics", "Coffee Cultivation",
            "Learn to roast — unlocks Coffee Roaster",
            {"coffee_seed": 5, "stone_chip": 3}, [],
            _noop, money_cost=10), 3, 0)

        self._add(ResearchNode(
            "roast_mastery", "Roast Mastery",
            "Technique improves roast quality by 15%",
            {"coal": 3, "coffee_seed": 5}, ["coffee_basics"],
            _noop, money_cost=20), 3, 1)

        self._add(ResearchNode(
            "blend_arts", "Blending Arts",
            "Art of blending — unlocks Blend Station",
            {"lumber": 5, "coffee_seed": 8}, ["roast_mastery"],
            _noop, money_cost=35), 3, 2)

        self._add(ResearchNode(
            "brew_expertise", "Brewing Expertise",
            "Five brew methods — unlocks Brew Station",
            {"iron_chunk": 3, "coffee_seed": 5}, ["blend_arts"],
            _noop, money_cost=50), 3, 3)

        self._add(ResearchNode(
            "master_barista", "Master Barista",
            "Coffee buffs last 50% longer",
            {"gold_nugget": 1, "coffee_seed": 10}, ["brew_expertise"],
            _noop, money_cost=80), 3, 4)

        # --- Birding (column 4) ---
        self._add(ResearchNode(
            "bird_watching", "Bird Watching",
            "Learn to observe — unlocks Bird Feeder",
            {"lumber": 5, "wheat": 3}, [],
            _noop, money_cost=8), 4, 0)

        self._add(ResearchNode(
            "bird_sanctuary", "Bird Sanctuary",
            "Unlocks Bird Bath. Birds spook less easily",
            {"stone_chip": 5, "lumber": 5}, ["bird_watching"],
            _noop, money_cost=20), 4, 1)

        self._add(ResearchNode(
            "ornithology", "Ornithology",
            "Rare raptors and exotic species appear nearby",
            {"lumber": 8, "stone_chip": 5}, ["bird_sanctuary"],
            _noop, money_cost=35), 4, 2)

        self._add(ResearchNode(
            "bird_lure", "Bird Luring",
            "Birds seek feeders and baths twice as often",
            {"wheat": 10, "coal": 3}, ["ornithology"],
            _noop, money_cost=50), 4, 3)

        self._add(ResearchNode(
            "avian_mastery", "Avian Mastery",
            "Larger flocks, more species in your world",
            {"gold_nugget": 1, "lumber": 10}, ["bird_lure"],
            _noop, money_cost=80), 4, 4)

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
        self.apply_bonuses(player)
        return True
