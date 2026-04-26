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
    COLUMNS = ["Mining Speed", "Zone Access", "Farming", "Coffee", "Birding", "Winemaking", "Distillation", "Entomology", "Horsemanship", "Tea Cultivation", "Herbalism", "Textile Arts", "Dairy Arts", "Hunting", "Jewelry Arts", "Garden Arts", "Masonry Arts", "Ceramics", "Cynology"]

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
        player.master_hunter              = u("master_hunter")
        player.insect_net_reduction       = 0.4  if u("net_mastery")        else 0.0
        player.insect_pollination_mult    = 1.35 if u("advanced_entomology") else 1.1

        # Dairy Arts bonuses
        player.curd_quality_bonus       = 0.15 if u("curd_mastery")      else 0.0
        player.cheese_buff_duration_bonus = 0.5 if u("affineurs_touch")  else 0.0
        player.blue_cheese_unlocked     = u("affineurs_touch")

        # Ceramics bonuses
        player.kiln_quality_bonus           = 0.15 if u("kiln_mastery")       else 0.0
        player.pottery_buff_duration_bonus  = 0.5  if u("glaze_arts")         else 0.0

        # Horsemanship bonuses
        player.horse_whisperer_bonus    = 2    if u("horse_whisperer")   else 0
        player.horse_breeding_mastery   = u("breeding_mastery")
        player.horse_stamina_drain_mult = 0.7  if u("endurance_riding")  else 1.0
        player.horse_shoe_bonus         = 0.15 if u("speed_training")    else 0.05

        # Cynology bonuses
        player.dog_whisperer_bonus  = 2    if u("scent_tracking")    else 0
        player.dog_breeding_mastery = u("breed_mastery")
        player.dog_ability_chance   = 0.15 if u("advanced_genetics") else 0.0
        player.kennel_capacity      = 6    if u("kennel_mastery")    else 4
        player.pure_breed_bonus     = u("pure_breeding")
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

        self._add(ResearchNode(
            "anaerobic_processing", "Anaerobic Fermentation",
            "Seal beans in oxygen-deprived tanks for intense, volatile flavours — unlocks Anaerobic Tank",
            {"gold_nugget": 2, "crystal_shard": 2}, ["master_barista"],
            _noop, money_cost=100), 3, 5)

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

        # --- Tea Cultivation (column 9) ---
        self._add(ResearchNode(
            "tea_cultivation", "Tea Cultivation",
            "Learn to cultivate tea — unlocks Withering Rack crafting",
            {"lumber": 6, "coal": 4}, [],
            _noop, money_cost=20), 9, 0)

        self._add(ResearchNode(
            "tea_processing_arts", "Processing Arts",
            "Master tea oxidation — unlocks Oxidation Station crafting",
            {"iron_chunk": 3, "coal": 6}, ["tea_cultivation"],
            _noop, money_cost=35), 9, 1)

        self._add(ResearchNode(
            "tea_blending", "Blending",
            "Learn herbal blending — unlocks herbal additions in Tea Cellar",
            {"lumber": 4, "ginger": 5}, ["tea_processing_arts"],
            _noop, money_cost=50), 9, 2)

        self._add(ResearchNode(
            "tea_ceremony", "Tea Ceremony",
            "Perfect the art of tea — unlocks Tea Cellar crafting and fine/aged quality tier",
            {"gold_nugget": 2, "iron_chunk": 3}, ["tea_blending"],
            _noop, money_cost=70), 9, 3)

        # --- Herbalism (column 10) ---
        self._add(ResearchNode(
            "herbalism_basics", "Herbalism Basics",
            "Learn to dry herbs — unlocks Drying Rack crafting",
            {"lumber": 4, "coal": 2}, [],
            _noop, money_cost=15), 10, 0)

        self._add(ResearchNode(
            "tincture_crafting", "Tincture Crafting",
            "Brew basic potions in the Alchemical Kiln",
            {"coal": 4, "crystal_shard": 2}, ["herbalism_basics"],
            _noop, money_cost=30), 10, 1)

        self._add(ResearchNode(
            "alchemy", "Alchemy",
            "Unlock fine-tier potions — more complex ingredient combinations",
            {"crystal_shard": 4, "iron_chunk": 2}, ["tincture_crafting"],
            _noop, money_cost=50), 10, 2)

        self._add(ResearchNode(
            "resonance_mastery", "Resonance Mastery",
            "Unlock the Resonance Chamber — elixirs with gem-infused power",
            {"ruby": 2, "crystal_shard": 4}, ["alchemy"],
            _noop, money_cost=80), 10, 3)

        # --- Textile Arts (column 11) ---
        self._add(ResearchNode(
            "fiber_arts", "Fiber Arts Basics",
            "Learn to spin fiber — unlocks Spinning Wheel crafting",
            {"iron_chunk": 3, "coal": 2}, [],
            _noop, money_cost=25), 11, 0)

        self._add(ResearchNode(
            "natural_dyes", "Natural Dyeing",
            "Extract pigment from wildflowers — unlocks Dye Vat crafting",
            {"iron_chunk": 2, "crystal_shard": 1}, ["fiber_arts"],
            _noop, money_cost=40), 11, 1)

        self._add(ResearchNode(
            "loom_mastery", "Loom Mastery",
            "Weave cloth into rugs, tapestries, and garments — unlocks Loom crafting",
            {"iron_chunk": 3, "gold_nugget": 1}, ["natural_dyes"],
            _noop, money_cost=55), 11, 2)

        self._add(ResearchNode(
            "master_weaver", "Master Weaver",
            "Advanced weaving patterns — unlocks diamond texture and tapestry output",
            {"gold_nugget": 2, "ruby": 1}, ["loom_mastery"],
            _noop, money_cost=70), 11, 3)

        self._add(ResearchNode(
            "cotton_cultivation", "Cotton Cultivation",
            "Cultivate cotton plants — a soft, warm-climate fiber for spinning",
            {"flax_fiber": 3, "coal": 2}, ["fiber_arts"],
            _noop, money_cost=30), 11, 5)

        self._add(ResearchNode(
            "glassblowing", "Glassblowing",
            "Smelt sand into glass — unlocks Glass Kiln crafting",
            {"sand_grain": 6, "coal": 3}, ["natural_dyes"],
            _noop, money_cost=45), 11, 4)

        # --- Dairy Arts (column 12) ---
        self._add(ResearchNode(
            "dairy_basics", "Dairy Basics",
            "Learn cheesemaking — unlocks Dairy Vat crafting; goats and sheep become milkable",
            {"milk": 5, "stone_chip": 4}, [],
            _noop, money_cost=20), 12, 0)

        self._add(ResearchNode(
            "curd_mastery", "Curd Mastery",
            "Curdling technique improves culture quality by 15%",
            {"milk": 8, "coal": 3}, ["dairy_basics"],
            _noop, money_cost=35), 12, 1)

        self._add(ResearchNode(
            "aging_arts", "Aging Arts",
            "Learn to age and press — unlocks Cheese Press and Aging Cave crafting",
            {"lumber": 6, "iron_chunk": 3}, ["curd_mastery"],
            _noop, money_cost=50), 12, 2)

        self._add(ResearchNode(
            "affineurs_touch", "Affineur's Touch",
            "Unlock blue cheese aging; cheese buffs last 50% longer",
            {"gold_nugget": 2, "iron_chunk": 3}, ["aging_arts"],
            _noop, money_cost=80), 12, 3)

        # --- Hunting (column 13) ---
        self._add(ResearchNode(
            "basic_archery", "Basic Archery",
            "Learn to craft bows and arrows — unlocks Fletching Table",
            {"lumber": 4, "stone_chip": 3}, [],
            _noop, money_cost=12), 13, 0)

        self._add(ResearchNode(
            "iron_arrows", "Iron Arrows",
            "Heavier arrowheads — craft iron arrows that deal double damage",
            {"iron_chunk": 3, "lumber": 2}, ["basic_archery"],
            _noop, money_cost=28), 13, 1)

        self._add(ResearchNode(
            "master_hunter", "Master Hunter",
            "Each successful hunt yields one extra drop",
            {"gold_nugget": 1, "iron_chunk": 3}, ["iron_arrows"],
            _noop, money_cost=55), 13, 2)

        self._add(ResearchNode(
            "composite_bow", "Composite Bow",
            "Laminated wood and sinew — craft a bow that fires 40% faster with greater range",
            {"lumber": 4, "iron_chunk": 2, "wool": 3}, ["master_hunter"],
            _noop, money_cost=70), 13, 3)

        self._add(ResearchNode(
            "broadhead_arrows", "Broadhead Arrows",
            "Wide iron tips — 3 damage and +1 to every drop on kill",
            {"iron_chunk": 5, "bone": 3}, ["composite_bow"],
            _noop, money_cost=90), 13, 4)

        self._add(ResearchNode(
            "longbow", "Longbow",
            "Tall stave bow — faster arrows and 36-block range, trades fire rate",
            {"lumber": 6, "deer_hide": 2, "wool": 3}, ["broadhead_arrows"],
            _noop, money_cost=85), 13, 5)

        self._add(ResearchNode(
            "poison_arrows", "Poison Arrows",
            "Treated tips — stun animals for 3 seconds on hit, preventing escape",
            {"bone": 3, "iron_chunk": 2, "feather": 2}, ["longbow"],
            _noop, money_cost=110), 13, 6)

        self._add(ResearchNode(
            "flint_arrows", "Flint Arrows",
            "Chipped stone tips — craft iron-strength arrows without needing metal",
            {"stone_chip": 6, "feather": 2}, ["basic_archery"],
            _noop, money_cost=18), 13, 7)

        self._add(ResearchNode(
            "recurve_bow", "Recurve Bow",
            "Curved limbs store more energy — faster draw than a wood bow",
            {"lumber": 3, "stone_chip": 2, "wool": 2}, ["flint_arrows"],
            _noop, money_cost=38), 13, 8)

        self._add(ResearchNode(
            "barbed_arrows", "Barbed Arrows",
            "Hooked tips slow fleeing animals to 40% speed for 5 seconds",
            {"iron_chunk": 3, "bone": 2}, ["iron_arrows"],
            _noop, money_cost=48), 13, 9)

        self._add(ResearchNode(
            "crossbow", "Crossbow",
            "Mechanical draw — slow to reload but adds +1 damage to every arrow fired",
            {"lumber": 4, "iron_chunk": 4, "stone_chip": 2}, ["longbow"],
            _noop, money_cost=130), 13, 10)

        self._add(ResearchNode(
            "gold_arrows", "Gold Arrows",
            "Dense gold tips — 4 damage, one-shots most prey",
            {"gold_nugget": 3, "feather": 3}, ["crossbow"],
            _noop, money_cost=160), 13, 11)

        # --- Jewelry Arts (column 14) ---
        self._add(ResearchNode(
            "goldsmithing", "Goldsmithing",
            "Unlock the Jewelry Workbench — craft custom rings, necklaces, pendants and more",
            {"iron_chunk": 8, "crystal_shard": 4}, [],
            _noop, money_cost=30), 14, 0)

        self._add(ResearchNode(
            "master_jeweler", "Master Jeweler",
            "Jewelry merchants pay 25% more for your pieces",
            {"gold_nugget": 3, "ruby": 1}, ["goldsmithing"],
            lambda p, w: setattr(p, "master_jeweler", True), money_cost=70), 14, 1)

        # --- Garden Arts (column 15) ---
        self._add(ResearchNode(
            "garden_workshop", "Garden Workshop",
            "Unlock the Garden Workshop — craft Moorish zellige tiles, Italian topiaries, fountains, and more",
            {"stone_chip": 10, "iron_chunk": 3}, [],
            _noop, money_cost=25), 15, 0)

        self._add(ResearchNode(
            "master_gardener", "Master Gardener",
            "Your garden blocks look 20% more impressive (sell bonus for adjacent structures)",
            {"limestone_block": 3, "sapling": 4}, ["garden_workshop"],
            _noop, money_cost=50), 15, 1)

        # --- Masonry Arts (column 16) ---
        self._add(ResearchNode(
            "stone_carving", "Stone Carving",
            "Unlock the Sculptor's Bench — chisel minerals into custom decorative sculptures",
            {"stone_chip": 8, "iron_chunk": 2}, [],
            _noop, money_cost=20), 16, 0)

        self._add(ResearchNode(
            "fine_chiseling", "Fine Chiseling",
            "Increase carving grid resolution: use 6 rows per mineral piece instead of 4",
            {"limestone_chip": 4, "iron_bar": 1}, ["stone_carving"],
            _noop, money_cost=35), 16, 1)

        self._add(ResearchNode(
            "master_sculptor", "Master Sculptor",
            "Unlock the Effigy template and allow mixing mineral colors in a single sculpture",
            {"polished_marble": 3, "chisel": 1}, ["fine_chiseling"],
            _noop, money_cost=60), 16, 2)

        # --- Cynology (column 18) ---
        self._add(ResearchNode(
            "dog_basics", "Dog Husbandry",
            "Learn to tame dogs — unlocks Dog Collar, Dog Bowl, and Dog Treat crafting",
            {"bone": 4, "raw_meat": 2}, [],
            _noop, money_cost=12), 18, 0)

        self._add(ResearchNode(
            "scent_tracking", "Scent Tracking",
            "Taming threshold reduced by 2 — unlocks Dog Whistle crafting",
            {"bone": 6, "carrot": 4}, ["dog_basics"],
            _noop, money_cost=25), 18, 1)

        self._add(ResearchNode(
            "breed_mastery", "Breed Mastery",
            "Full stat prediction shown in kennel breeding panel",
            {"lumber": 5, "iron_chunk": 2}, ["scent_tracking"],
            _noop, money_cost=42), 18, 2)

        self._add(ResearchNode(
            "advanced_genetics", "Advanced Genetics",
            "+15% chance ability genes pass from single-carrier parent to offspring",
            {"crystal_shard": 2, "iron_chunk": 3}, ["breed_mastery"],
            _noop, money_cost=60), 18, 3)

        self._add(ResearchNode(
            "kennel_mastery", "Kennel Mastery",
            "Kennel capacity increases to 6 dogs — unlocks Kennel crafting",
            {"lumber": 8, "stone_chip": 4}, ["advanced_genetics"],
            _noop, money_cost=80), 18, 4)

        self._add(ResearchNode(
            "pure_breeding", "Pure Breeding",
            "Pure-breed offspring receive +0.05 bonus on their breed's signature trait",
            {"gold_nugget": 2, "iron_chunk": 3}, ["kennel_mastery"],
            _noop, money_cost=110), 18, 5)

        # --- Ceramics (column 17) ---
        self._add(ResearchNode(
            "clay_working", "Clay Working",
            "Unlock the Pottery Wheel — shape clay into bowls, pots, jugs, and vases",
            {"clay": 8, "stone_chip": 4}, [],
            _noop, money_cost=15), 17, 0)

        self._add(ResearchNode(
            "kiln_mastery", "Kiln Mastery",
            "Unlock the Pottery Kiln and gain +15% firing quality bonus",
            {"clay": 12, "coal": 5}, ["clay_working"],
            _noop, money_cost=30), 17, 1)

        self._add(ResearchNode(
            "glaze_arts", "Glaze Arts",
            "Unlock gem dust glazing at the kiln — glazed pieces gain a quality tier and extend buff durations by 50%",
            {"clay": 8, "ruby": 1}, ["kiln_mastery"],
            _noop, money_cost=50), 17, 2)

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
