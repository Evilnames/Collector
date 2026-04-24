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
    COLUMNS = ["Mining Speed", "Zone Access", "Farming", "Coffee", "Birding", "Winemaking", "Distillation", "Entomology", "Horsemanship"]

    def __init__(self):
        self.nodes = {}    # id -> ResearchNode
        self.layout = []   # [(col, row, node_id), ...]
        self._build()

    def apply_save(self, unlocked_ids):
        for node_id in unlocked_ids:
            if node_id in self.nodes:
                self.nodes[node_id].unlocked = True

    def apply_bonuses(self, player, world=None):
        """Set all research-derived bonuses on player (and world) from current unlock state."""
        import soil as _soil
        def u(nid):
            n = self.nodes.get(nid)
            return n is not None and n.unlocked

        # Deprecated flat bonuses kept at 0 — soil math now drives farming output.
        player.crop_grow_bonus            = 0.0
        player.harvest_bonus              = 0
        player.roast_quality_bonus        = 0.15 if u("roast_mastery")      else 0.0
        player.coffee_buff_duration_bonus = 0.5  if u("master_barista")     else 0.0
        player.bird_spook_reduction       = 0.4  if u("bird_sanctuary")     else 0.0
        player.bird_feeder_bonus          = 2.0  if u("bird_lure")          else 1.0
        player.avian_mastery              = u("avian_mastery")
        player.insect_net_reduction       = 0.4  if u("net_mastery")        else 0.0
        player.insect_pollination_mult    = 1.35 if u("advanced_entomology") else 1.1

        # Horsemanship bonuses
        player.horse_whisperer_bonus    = 2    if u("horse_whisperer")   else 0
        player.horse_breeding_mastery   = u("breeding_mastery")
        player.horse_stamina_drain_mult = 0.7  if u("endurance_riding")  else 1.0
        player.horse_shoe_bonus         = 0.15 if u("speed_training")    else 0.05
        if world is not None:
            # irrigation: moisture decays half as fast
            world.moisture_decay_chance = (
                _soil.MOISTURE_DECAY_CHANCE / 2 if u("irrigation")
                else _soil.MOISTURE_DECAY_CHANCE
            )
            # composting: raises the max fertility cap
            world.max_fertility = 10 if u("composting") else _soil.MAX_FERTILITY

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
            "Till dirt, water crops — unlocks Hoe, Watering Can, and Farm Bot",
            {"dirt_clump": 8, "wheat": 3}, [],
            _noop, money_cost=5), 2, 0)

        self._add(ResearchNode(
            "irrigation", "Irrigation",
            "Moisture decays half as fast — unlocks Compost Bin crafting",
            {"stone_chip": 5, "carrot": 3}, ["soil_prep"],
            _noop, money_cost=15), 2, 1)

        self._add(ResearchNode(
            "composting", "Composting",
            "Raises max soil fertility cap from 8 to 10",
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
            {"stone_chip": 5, "dirt_clump": 5}, [],
            _noop, money_cost=10), 3, 0)

        self._add(ResearchNode(
            "roast_mastery", "Roast Mastery",
            "Technique improves roast quality by 15%",
            {"coal": 5, "stone_chip": 3}, ["coffee_basics"],
            _noop, money_cost=20), 3, 1)

        self._add(ResearchNode(
            "blend_arts", "Blending Arts",
            "Art of blending — unlocks Blend Station",
            {"lumber": 8, "stone_chip": 5}, ["roast_mastery"],
            _noop, money_cost=35), 3, 2)

        self._add(ResearchNode(
            "brew_expertise", "Brewing Expertise",
            "Five brew methods — unlocks Brew Station",
            {"iron_chunk": 5, "coal": 3}, ["blend_arts"],
            _noop, money_cost=50), 3, 3)

        self._add(ResearchNode(
            "master_barista", "Master Barista",
            "Coffee buffs last 50% longer",
            {"gold_nugget": 2, "iron_chunk": 3}, ["brew_expertise"],
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

        # --- Winemaking (column 5) ---
        self._add(ResearchNode(
            "wine_basics", "Viticulture",
            "Unlock Grape Press, Fermentation Tank, Wine Cellar",
            {"lumber": 6, "stone_chip": 4}, [],
            _noop, money_cost=15), 5, 0)

        self._add(ResearchNode(
            "fermentation_arts", "Fermentation Arts",
            "Ferment quality bonus +15%",
            {"iron_chunk": 4, "coal": 3}, ["wine_basics"],
            _noop, money_cost=30), 5, 1)

        self._add(ResearchNode(
            "winemaking_mastery", "Winemaking Mastery",
            "Wine buffs last 50% longer",
            {"gold_nugget": 2, "iron_chunk": 3}, ["fermentation_arts"],
            _noop, money_cost=60), 5, 2)

        # --- Distillation (column 6) ---
        self._add(ResearchNode(
            "distillation_basics", "Distillation Basics",
            "Learn to distill — unlocks Still, Barrel Room, Bottling Station",
            {"coal": 8, "iron_chunk": 4}, [],
            _noop, money_cost=20), 6, 0)

        self._add(ResearchNode(
            "cut_mastery", "Cut Mastery",
            "Hearts-cut window +20% wider — easier to nail quality distillation",
            {"coal": 6, "iron_chunk": 3}, ["distillation_basics"],
            _noop, money_cost=35), 6, 1)

        self._add(ResearchNode(
            "barrel_arts", "Barrel Arts",
            "Aging quality bonus +15% on all barrels",
            {"lumber": 8, "gold_nugget": 1}, ["cut_mastery"],
            _noop, money_cost=50), 6, 2)

        self._add(ResearchNode(
            "master_distiller", "Master Distiller",
            "Spirit buffs last 50% longer",
            {"gold_nugget": 3, "iron_chunk": 4}, ["barrel_arts"],
            _noop, money_cost=80), 6, 3)

        # --- Entomology (column 7) ---
        self._add(ResearchNode(
            "entomology_basics", "Entomology Basics",
            "Learn to catch insects — unlocks Bug Net and Display Case",
            {"lumber": 3, "wool": 2}, [],
            _noop, money_cost=8), 7, 0)

        self._add(ResearchNode(
            "insect_habitats", "Insect Habitats",
            "Biome hints appear for undiscovered insects in the codex",
            {"stone_chip": 4, "wheat": 3}, ["entomology_basics"],
            _noop, money_cost=20), 7, 1)

        self._add(ResearchNode(
            "net_mastery", "Net Mastery",
            "Insects spook 40% less easily when approaching",
            {"lumber": 6, "wool": 4}, ["insect_habitats"],
            _noop, money_cost=35), 7, 2)

        self._add(ResearchNode(
            "advanced_entomology", "Advanced Entomology",
            "Insect pollination bonus increases from 10% to 35% crop growth boost",
            {"gold_nugget": 1, "lumber": 8}, ["net_mastery"],
            _noop, money_cost=80), 7, 3)

        # --- Horsemanship (column 8) ---
        self._add(ResearchNode(
            "saddle_craft", "Saddle Craft",
            "Learn to craft saddles and stables — required for riding horses",
            {"lumber": 3, "wool": 2}, [],
            _noop, money_cost=10), 8, 0)

        self._add(ResearchNode(
            "horse_whisperer", "Horse Whisperer",
            "Taming threshold reduced by 2 for all horse temperaments",
            {"apple": 5, "wheat": 5}, ["saddle_craft"],
            _noop, money_cost=22), 8, 1)

        self._add(ResearchNode(
            "breeding_mastery", "Breeding Mastery",
            "Offspring temperament skews calmer; stat prediction shown in breeding panel",
            {"lumber": 6, "iron_chunk": 3}, ["horse_whisperer"],
            _noop, money_cost=40), 8, 2)

        self._add(ResearchNode(
            "speed_training", "Speed Training",
            "Horseshoes grant +15% speed instead of +5%",
            {"iron_chunk": 5, "coal": 3}, ["breeding_mastery"],
            _noop, money_cost=55), 8, 3)

        self._add(ResearchNode(
            "endurance_riding", "Endurance",
            "Stamina drains 30% slower while sprinting on horseback",
            {"gold_nugget": 1, "wheat": 8}, ["speed_training"],
            _noop, money_cost=80), 8, 4)

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
