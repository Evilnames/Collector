import random
import pygame
from automations import Automation, AUTOMATION_DEFS, FarmBot, FARM_BOT_DEFS, FARM_BOT_TYPES, Backhoe
from blocks import (BLOCKS, AIR, ROCK_DEPOSIT, WILDFLOWER_PATCH, FOSSIL_DEPOSIT, GEM_DEPOSIT, CAVE_MUSHROOMS, EQUIPMENT_BLOCKS, LADDER, WATER,
                    WOOD_DOOR_CLOSED, WOOD_DOOR_OPEN, IRON_DOOR_CLOSED, IRON_DOOR_OPEN,
                    COBALT_DOOR_CLOSED, COBALT_DOOR_OPEN,
                    CRIMSON_CEDAR_DOOR_CLOSED, CRIMSON_CEDAR_DOOR_OPEN,
                    TEAL_DOOR_CLOSED, TEAL_DOOR_OPEN,
                    SAFFRON_DOOR_CLOSED, SAFFRON_DOOR_OPEN,
                    WOOD_FENCE, IRON_FENCE, WOOD_FENCE_OPEN, IRON_FENCE_OPEN,
                    SAPLING, GRASS, DIRT, ALL_LOGS, ALL_LEAVES,
                    YOUNG_CROP_BLOCKS, MATURE_CROP_BLOCKS, BUSH_BLOCKS,
                    STRAWBERRY_BUSH, WHEAT_BUSH,
                    CARROT_BUSH, TOMATO_BUSH, CORN_BUSH, PUMPKIN_BUSH, APPLE_BUSH,
                    RICE_BUSH, GINGER_BUSH, BOK_CHOY_BUSH, GARLIC_BUSH,
                    SCALLION_BUSH, CHILI_BUSH,
                    PEPPER_BUSH, ONION_BUSH, POTATO_BUSH, EGGPLANT_BUSH, CABBAGE_BUSH,
                    BEET_BUSH, TURNIP_BUSH, LEEK_BUSH, ZUCCHINI_BUSH, SWEET_POTATO_BUSH,
                    WATERMELON_BUSH, RADISH_BUSH, PEA_BUSH, CELERY_BUSH, BROCCOLI_BUSH,
                    STRAWBERRY_CROP_MATURE, WHEAT_CROP_MATURE,
                    CARROT_CROP_MATURE, TOMATO_CROP_MATURE, CORN_CROP_MATURE,
                    PUMPKIN_CROP_MATURE, APPLE_CROP_MATURE,
                    RICE_CROP_MATURE, GINGER_CROP_MATURE,
                    BOK_CHOY_CROP_MATURE, GARLIC_CROP_MATURE,
                    SCALLION_CROP_MATURE, CHILI_CROP_MATURE,
                    PEPPER_CROP_MATURE, ONION_CROP_MATURE, POTATO_CROP_MATURE,
                    EGGPLANT_CROP_MATURE, CABBAGE_CROP_MATURE,
                    BEET_CROP_MATURE, TURNIP_CROP_MATURE, LEEK_CROP_MATURE,
                    ZUCCHINI_CROP_MATURE, SWEET_POTATO_CROP_MATURE, WATERMELON_CROP_MATURE,
                    RADISH_CROP_MATURE, PEA_CROP_MATURE, CELERY_CROP_MATURE, BROCCOLI_CROP_MATURE,
                    PERENNIAL_CROP_MATURE, MATURE_TO_YOUNG_CROP, CHEST_BLOCK,
                    STRAWBERRY_CROP_MATURE_P, TOMATO_CROP_MATURE_P, WATERMELON_CROP_MATURE_P,
                    CORN_CROP_MATURE_P, RICE_CROP_MATURE_P,
                    OIL, BIRD_FEEDER_BLOCK, BIRD_BATH_BLOCK,
                    COFFEE_CROP_MATURE, GRAPEVINE_CROP_MATURE, GRAIN_CROP_MATURE, TEA_CROP_MATURE,
                    FLAX_CROP_MATURE, COTTON_CROP_MATURE,
                    CHAMOMILE_BUSH, LAVENDER_BUSH, MINT_BUSH, ROSEMARY_BUSH,
                    THYME_BUSH, SAGE_BUSH, BASIL_BUSH, OREGANO_BUSH,
                    DILL_BUSH, FENNEL_BUSH, TARRAGON_BUSH, LEMON_BALM_BUSH,
                    ECHINACEA_BUSH, VALERIAN_BUSH, ST_JOHNS_WORT_BUSH, YARROW_BUSH,
                    BERGAMOT_BUSH, WORMWOOD_BUSH, RUE_BUSH, LEMON_VERBENA_BUSH,
                    HYSSOP_BUSH, CATNIP_BUSH, WOOD_SORREL_BUSH, MARJORAM_BUSH,
                    SAVORY_BUSH, ANGELICA_BUSH, BORAGE_BUSH, COMFREY_BUSH, MUGWORT_BUSH,
                    CHAMOMILE_CROP_MATURE, LAVENDER_CROP_MATURE, MINT_CROP_MATURE, ROSEMARY_CROP_MATURE,
                    SKY_OPENING, STONE, TILLED_SOIL, SAND, COMPOST_BIN_BLOCK, WELL_BLOCK,
                    STAIRS_RIGHT, STAIRS_LEFT, STAIR_BLOCKS,
                    GARDEN_BLOCK, WILDFLOWER_DISPLAY_BLOCK,
                    COAL_ORE, IRON_ORE, GOLD_ORE, CRYSTAL_ORE, RUBY_ORE,
                    ELEVATOR_STOP_BLOCK,
                    MINE_TRACK_STOP_BLOCK,
                    SCULPTURE_BLOCK_ROOT, SCULPTURE_BLOCK_BODY,
                    CUSTOM_TAPESTRY_ROOT, CUSTOM_TAPESTRY_BODY,
                    POTTERY_DISPLAY_BLOCK,
                    SALT_DEPOSIT)
import soil as _soil
from items import ITEMS
from rocks import RockGenerator, Rock
from wildflowers import WildflowerGenerator, Wildflower
from fossils import FossilGenerator, Fossil
from gemstones import GemGenerator, Gemstone
from fish import FishGenerator, Fish
from coffee import CoffeeGenerator, CoffeeBean
from wine import WineGenerator, Grape
from sculpture import SculptureGenerator, Sculpture
from tapestry import TapestryGenerator, Tapestry
from pottery import PotteryPiece, PotteryGenerator
from spirits import SpiritGenerator, Spirit
from tea import TeaGenerator, TeaLeaf
from textiles import TextileGenerator, Textile
from cheese import CheeseGenerator, Cheese
from jewelry import Jewelry
from salt import SaltGenerator, SaltCrystal
from constants import (
    BLOCK_SIZE, PLAYER_W, PLAYER_H,
    GRAVITY, JUMP_FORCE, MOVE_SPEED, MAX_FALL,
    MINE_REACH, MAX_HEALTH, HOTBAR_SIZE,
    ROCK_DETECT_RANGE,
)

# Blocks that cannot be placed in the background layer
_BG_DISALLOWED = (
    {WATER, LADDER, SAPLING, CHEST_BLOCK, GARDEN_BLOCK, WILDFLOWER_DISPLAY_BLOCK,
     WOOD_DOOR_CLOSED, WOOD_DOOR_OPEN, IRON_DOOR_CLOSED, IRON_DOOR_OPEN,
     COBALT_DOOR_CLOSED, COBALT_DOOR_OPEN,
     CRIMSON_CEDAR_DOOR_CLOSED, CRIMSON_CEDAR_DOOR_OPEN,
     TEAL_DOOR_CLOSED, TEAL_DOOR_OPEN,
     SAFFRON_DOOR_CLOSED, SAFFRON_DOOR_OPEN,
     BIRD_FEEDER_BLOCK, BIRD_BATH_BLOCK}
    | BUSH_BLOCKS
    | YOUNG_CROP_BLOCKS
    | EQUIPMENT_BLOCKS
    | STAIR_BLOCKS
)


class Player:
    def __init__(self, world):
        self.world = world
        sx = 0
        sy = world.surface_y_at(sx)
        self.x = float(sx * BLOCK_SIZE + (BLOCK_SIZE - PLAYER_W) // 2)
        self.y = float((sy - 2) * BLOCK_SIZE)
        self.vx = 0.0
        self.vy = 0.0
        self.on_ground = False
        self._on_ladder = False
        self.facing = 1          # 1 = right, -1 = left
        self.health = MAX_HEALTH
        self.pick_power = 1
        self.inventory = {}
        self.hotbar = [None] * HOTBAR_SIZE
        self.hotbar_uses = [None] * HOTBAR_SIZE
        self.selected_slot = 0
        self.money = 0
        self.blessing_timer = 0.0
        self.blessing_mult  = 1.0
        # Rock collection
        self.rocks = []
        self.discovered_types = set()
        self.rock_detect_range = ROCK_DETECT_RANGE
        self._rock_gen = RockGenerator(world.seed)
        # Wildflower collection
        self.wildflowers = []
        self.discovered_flower_types = set()
        self._flower_gen = WildflowerGenerator(world.seed)
        # Mushroom collection
        self.mushrooms_found = {}        # block_id -> count
        self.discovered_mushroom_types = set()
        # Fossil collection
        self.fossils = []
        self.discovered_fossil_types = set()
        self._fossil_gen = FossilGenerator(world.seed)
        # Gem collection
        self.gems = []
        self.discovered_gem_types = set()
        self._gem_gen = GemGenerator(world.seed)
        # Fish collection
        self.fish_caught = []
        self.discovered_fish_species = set()
        self._fish_gen = FishGenerator(world.seed)
        # Coffee collection
        self.coffee_beans = []
        self.discovered_coffee_origins = set()  # "biome_roastlevel" strings
        self._coffee_gen = CoffeeGenerator(world.seed)
        self.roast_profiles = []  # [{name, biome, roast_level, curve: [(t, temp), ...]}]
        # Active buffs from drinking coffee
        self.active_buffs = {}  # buff_name -> {"duration": float}
        # Wine collection
        self.wine_grapes = []
        self.discovered_wine_origins = set()  # "biome_style" strings
        self._wine_gen = WineGenerator(world.seed)
        # Active buffs from drinking wine (separate pool, stacks with coffee)
        self.wine_buffs = {}  # buff_name -> {"duration": float}
        # Tea collection
        self.tea_leaves = []
        self.discovered_tea_origins = set()   # "biome_teatype" strings
        self._tea_gen = TeaGenerator(world.seed)
        # Active buffs from drinking tea (separate pool, stacks with coffee/wine)
        self.tea_buffs = {}   # buff_name -> {"duration": float}
        # Herbalism
        self.discovered_recipes = set()  # output_id strings of discovered recipes
        self.herb_buffs         = {}     # buff_name -> {"duration": float}
        # Spirits collection
        self.spirits = []
        self.discovered_spirit_types = set()  # "biome_tier" strings e.g. "canyon_aged"
        self._spirit_gen = SpiritGenerator(world.seed)
        # Active buffs from drinking spirits (separate pool, stacks with coffee/wine)
        self.spirit_buffs = {}  # buff_name -> {"duration": float}
        # Textile collection
        self.textiles = []
        self.discovered_textiles = set()         # "fiber_dye_output" strings
        self.worn = {"head": None, "chest": None, "feet": None}  # Textile UIDs
        self._textile_gen = TextileGenerator(world.seed)
        # Cheese collection
        self.cheese_wheels = []
        self.discovered_cheese = set()           # "biome_cheesetype" strings
        self._cheese_gen = CheeseGenerator(world.seed)
        self.cheese_buffs = {}                   # buff_name -> {"duration": float}
        # Salt collection
        self.salt_crystals = []
        self.discovered_salt_origins = set()    # "biome_grade" strings
        self._salt_gen = SaltGenerator(world.seed)
        self.salt_buffs = {}                    # buff_name -> {"duration": float}
        # Jewelry collection
        self.jewelry = []
        self.discovered_jewelry = set()          # jewelry_type strings
        self.master_jeweler = False              # set True by research bonus
        # Sculpture system
        self.pending_sculptures = []   # Sculpture objects ready to place
        self.sculptures_created = []   # permanent log of all completed sculptures
        self._sculpture_gen     = SculptureGenerator(world.seed)
        # Tapestry system
        self.pending_tapestries = []   # Tapestry objects ready to place
        self.tapestries_created = []   # permanent log of all completed tapestries
        self._tapestry_gen      = TapestryGenerator(world.seed)
        # Pottery & Ceramics
        self.pottery_pieces       = []   # PotteryPiece objects
        self.discovered_pottery   = set()  # "biome_firinglevel" strings
        self._pottery_gen         = PotteryGenerator(world.seed)
        self.unplaced_vases       = []   # PotteryPiece vases available to mount on a display pedestal
        self.pottery_buffs        = {}   # buff_name -> {"duration": float}
        # Hunting
        self.animals_hunted  = {}   # animal_id -> count killed
        self._bow_cooldown   = 0.0
        self.master_hunter   = False  # set True by research bonus
        # Fishing mini-game state
        self.fishing_state = None     # None | "casting" | "biting" | "result"
        self._fishing_timer = 0.0
        self._fishing_result = None   # "caught" | "missed"
        self._fishing_biome = None
        # Bird observations
        self.birds_observed = {}           # species_id -> {"count": int, "biome": str}
        self.discovered_bird_types = set()
        # Insect observations
        self.insects_observed = {}         # species_id -> {"count": int, "biome": str}
        self.discovered_insect_types = set()
        # Food codex
        self.discovered_foods = set()      # output_id strings of crafted food items
        self.foods_cooked = {}             # output_id -> count crafted
        self.pending_notifications = []   # (category, name_or_bid, rarity)
        self.known_recipes = set()
        self.known_crops   = set()   # young block IDs the player has harvested at least once
        self.pending_harvest_floats = []  # (world_x, world_y, text, color) consumed by renderer
        # Water state
        self._drowning_timer = 0.0
        # Hunger
        self.hunger             = 100.0
        self._hunger_drain_rate = 100.0 / 600.0  # 100% over 10 minutes
        self._eat_cooldown      = 0.0
        # Spawn / death
        self.spawn_x = None
        self.spawn_y = None
        self.dead = False
        self.god_mode = False
        self.no_hunger = False
        # Mining state
        self.mining_block = None  # (bx, by) or None
        self.mine_progress = 0.0
        self._mine_time = 0.0
        self._mine_total = 0.0
        # Placement state
        self.place_target = None  # (bx, by) ghost shown by renderer
        self.bg_place_mode = False  # True when Shift held — places in background layer
        self._shift_held = False    # True when Shift held — required to mine background layer
        # Farm sense: block under mouse (for crop readiness display)
        self.target_block = None
        # Construction equipment
        self.mounted_machine = None
        # Elevator
        self.riding_elevator = None
        # Minecart
        self.riding_minecart = None
        # Doors the player auto-opened by walking into them
        self._auto_opened_doors = set()  # set of (bx, by)
        # Research-derived bonuses (computed by ResearchTree.apply_bonuses)
        self.crop_grow_bonus            = 0.0   # added to 0.15 crop-mature chance
        self.harvest_bonus              = 0     # extra drops per crop harvest
        self.roast_quality_bonus        = 0.0
        self.coffee_buff_duration_bonus = 0.0
        self.curd_quality_bonus         = 0.0
        self.cheese_buff_duration_bonus = 0.0
        self.blue_cheese_unlocked       = False
        self.kiln_quality_bonus          = 0.0   # added to firing quality score
        self.pottery_buff_duration_bonus = 0.0   # multiplier on pottery buff durations
        self.bird_spook_reduction        = 0.0   # fraction of spook radius removed
        self.bird_feeder_bonus          = 1.0   # multiplier on feeder attraction chance
        self.avian_mastery              = False # enables larger flocks
        self.insect_net_reduction       = 0.0   # fraction of insect spook radius removed
        self.insect_pollination_mult    = 1.1   # crop growth multiplier when insects nearby
        # Horsemanship research bonuses
        self.horse_whisperer_bonus    = 0
        self.horse_breeding_mastery   = False
        self.horse_stamina_drain_mult = 1.0
        self.horse_shoe_bonus         = 0.05
        # Horse riding state
        self.mounted_horse         = None   # Horse ref or None
        self._sprint_cooldown      = 0.0    # exhaustion cooldown after stamina empty
        self._pending_horse_break  = None   # Horse ref; set on right-click, read by main.py
        # Horse codex tracking
        self.horses_tamed           = 0
        self.horses_bred            = 0
        self.horse_records          = {"best_speed": 0.0, "best_stamina": 0.0}
        self.discovered_coat_biomes = set()

    def apply_save(self, d):
        self.x, self.y = d["x"], d["y"]
        self.vx, self.vy = d["vx"], d["vy"]
        self.facing = d["facing"]
        self.health, self.hunger = d["health"], d["hunger"]
        self.pick_power, self.money = d["pick_power"], d["money"]
        self.selected_slot = d["selected_slot"]
        self.inventory = d["inventory"]
        self.hotbar = d["hotbar"]
        self.hotbar_uses = d["hotbar_uses"]
        self.known_recipes = set(d["known_recipes"])
        self.known_crops   = set(d.get("known_crops", []))
        self.rocks = [Rock(**r) for r in d["rocks"]]
        self.wildflowers = [Wildflower(**wf) for wf in d["wildflowers"]]
        self.fossils = [Fossil(**f) for f in d.get("fossils", [])]
        self.gems = [Gemstone(**g) for g in d.get("gems", [])]
        self.fish_caught = [Fish(**f) for f in d.get("fish", [])]
        self.coffee_beans = [CoffeeBean(**cb) for cb in d.get("coffee_beans", [])]
        self.discovered_coffee_origins = set(d.get("discovered_coffee_origins", []))
        self.roast_profiles = d.get("roast_profiles", [])
        self.wine_grapes = [Grape(**g) for g in d.get("wine_grapes", [])]
        self.discovered_wine_origins = set(d.get("discovered_wine_origins", []))
        self.tea_leaves = [TeaLeaf(**x) for x in d.get("tea_leaves", [])]
        self.discovered_tea_origins = set(d.get("discovered_tea_origins", []))
        self.discovered_recipes = set(d.get("discovered_recipes", []))
        self.spirits = [Spirit(**s) for s in d.get("spirits", [])]
        self.discovered_spirit_types = set(d.get("discovered_spirit_types", []))
        self.textiles = [Textile(**x) for x in d.get("textiles", [])]
        self.discovered_textiles = set(d.get("discovered_textiles", []))
        self.worn = d.get("worn", {"head": None, "chest": None, "feet": None})
        self.cheese_wheels = [Cheese(**x) for x in d.get("cheese_wheels", [])]
        self.discovered_cheese = set(d.get("discovered_cheese", []))
        self.birds_observed = d.get("birds_observed", {})
        self.discovered_bird_types = set(d.get("discovered_bird_types", []))
        self.insects_observed = d.get("insects_observed", {})
        self.discovered_insect_types = set(d.get("discovered_insect_types", []))
        self.discovered_foods = set(d.get("discovered_foods", []))
        self.jewelry = [Jewelry(**j) for j in d.get("jewelry", [])]
        self.discovered_jewelry = set(d.get("discovered_jewelry", []))
        self.foods_cooked = d.get("foods_cooked", {})
        self.discovered_types = set(d["discovered_types"])
        self.discovered_flower_types = set(d["discovered_flower_types"])
        self.discovered_fossil_types = set(d.get("discovered_fossil_types", []))
        self.discovered_gem_types = set(d.get("discovered_gem_types", []))
        self.discovered_fish_species = set(d.get("discovered_fish_species", []))
        self.mushrooms_found = {int(k): v for k, v in d["mushrooms_found"].items()}
        self.discovered_mushroom_types = set(int(x) for x in d["discovered_mushroom_types"])
        self.spawn_x = d.get("spawn_x")
        self.spawn_y = d.get("spawn_y")
        self.horses_tamed           = d.get("horses_tamed", 0)
        self.horses_bred            = d.get("horses_bred", 0)
        self.horse_records          = d.get("horse_records", {"best_speed": 0.0, "best_stamina": 0.0})
        self.discovered_coat_biomes = set(d.get("discovered_coat_biomes", []))
        self.animals_hunted = d.get("animals_hunted", {})
        self.pending_sculptures = [Sculpture.from_dict(x) for x in d.get("pending_sculptures", [])]
        self.sculptures_created = [Sculpture.from_dict(x) for x in d.get("sculptures_created", [])]
        self.pending_tapestries = [Tapestry.from_dict(x) for x in d.get("pending_tapestries", [])]
        self.tapestries_created = [Tapestry.from_dict(x) for x in d.get("tapestries_created", [])]
        self.pottery_pieces     = [PotteryPiece(**x) for x in d.get("pottery_pieces", [])]
        self.discovered_pottery = set(d.get("discovered_pottery", []))
        self.pottery_buffs      = d.get("pottery_buffs", {})
        self.salt_crystals          = [SaltCrystal(**x) for x in d.get("salt_crystals", [])]
        self.discovered_salt_origins= set(d.get("discovered_salt_origins", []))
        self.salt_buffs             = d.get("salt_buffs", {})
        # Reconstruct unplaced_vases from saved UIDs
        _piece_by_uid = {p.uid: p for p in self.pottery_pieces}
        _pending_uids = getattr(self.world, "_pending_unplaced_vase_uids", [])
        self.unplaced_vases = [_piece_by_uid[uid] for uid in _pending_uids if uid in _piece_by_uid]
        if hasattr(self.world, "_pending_unplaced_vase_uids"):
            del self.world._pending_unplaced_vase_uids

    # ------------------------------------------------------------------
    # Sculpture helpers
    # ------------------------------------------------------------------

    def _demolish_sculpture(self, root_bx, root_by):
        sc = self.world.sculpture_data.pop((root_bx, root_by), None)
        height = sc.height if sc else 1
        self.world.set_bg_block(root_bx, root_by, AIR)
        for k in range(1, height):
            self.world.sculpture_data.pop((root_bx, root_by - k), None)
            self.world.set_bg_block(root_bx, root_by - k, AIR)

    def _place_sculpture(self, bx, by):
        if not self.pending_sculptures:
            return False
        sc = self.pending_sculptures[0]
        for k in range(sc.height):
            if self.world.get_bg_block(bx, by - k) != AIR:
                return False
        self.pending_sculptures.pop(0)
        self.world.set_bg_block(bx, by, SCULPTURE_BLOCK_ROOT)
        self.world.sculpture_data[(bx, by)] = sc
        for k in range(1, sc.height):
            self.world.set_bg_block(bx, by - k, SCULPTURE_BLOCK_BODY)
            self.world.sculpture_data[(bx, by - k)] = {"root": (bx, by)}
        return True

    # ------------------------------------------------------------------
    # Tapestry helpers
    # ------------------------------------------------------------------

    def _demolish_tapestry(self, root_bx, root_by):
        tp = self.world.tapestry_data.pop((root_bx, root_by), None)
        height = tp.height if tp else 1
        width  = tp.width  if tp else 1
        for dx in range(width):
            self.world.set_bg_block(root_bx + dx, root_by, AIR)
            for k in range(1, height):
                self.world.tapestry_data.pop((root_bx + dx, root_by - k), None)
                self.world.set_bg_block(root_bx + dx, root_by - k, AIR)
            if dx > 0:
                self.world.tapestry_data.pop((root_bx + dx, root_by), None)

    def _place_tapestry(self, bx, by):
        if not self.pending_tapestries:
            return False
        tp = self.pending_tapestries[0]
        for dx in range(tp.width):
            for k in range(tp.height):
                if self.world.get_bg_block(bx + dx, by - k) != AIR:
                    return False
        self.pending_tapestries.pop(0)
        self.world.set_bg_block(bx, by, CUSTOM_TAPESTRY_ROOT)
        self.world.tapestry_data[(bx, by)] = tp
        for dx in range(tp.width):
            for k in range(tp.height):
                if dx == 0 and k == 0:
                    continue
                self.world.set_bg_block(bx + dx, by - k, CUSTOM_TAPESTRY_BODY)
                self.world.tapestry_data[(bx + dx, by - k)] = {"root": (bx, by)}
        return True

    # ------------------------------------------------------------------
    # Bow / Arrow firing
    # ------------------------------------------------------------------

    def fire_arrow(self):
        """Fire an arrow in player.facing direction. Returns True on success."""
        tool = self.hotbar[self.selected_slot]
        if not tool or not ITEMS.get(tool, {}).get("bow"):
            return False
        if self._bow_cooldown > 0:
            return False
        arrow_id = None
        for aid in ("iron_arrow", "wood_arrow"):
            if self.inventory.get(aid, 0) > 0:
                arrow_id = aid
                break
        if not arrow_id:
            return False
        self.inventory[arrow_id] -= 1
        if self.inventory[arrow_id] <= 0:
            del self.inventory[arrow_id]
            for i in range(HOTBAR_SIZE):
                if self.hotbar[i] == arrow_id and self.inventory.get(arrow_id, 0) == 0:
                    pass  # keep bow in slot; arrows are separate inventory items
        from hunting import Arrow
        cx = self.x + PLAYER_W / 2
        cy = self.y + PLAYER_H / 2 - 4
        damage = ITEMS.get(arrow_id, {}).get("arrow_damage", 1)
        self.world.arrows.append(Arrow(cx, cy, self.facing, self.world, damage))
        self._bow_cooldown = 0.45
        return True

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------

    def handle_input(self, keys, mouse_buttons, mouse_world_pos, dt):
        if self.mounted_machine is not None:
            return
        if self.riding_elevator is not None:
            return
        if self.riding_minecart is not None:
            return
        if self.mounted_horse is not None:
            self._handle_horse_input(keys, dt)
            return
        self.vx = 0.0
        speed = MOVE_SPEED * (1.25 if "rush" in self.active_buffs else 1.0)
        if "swiftness" in self.herb_buffs:
            speed *= 1.50
        elif "haste" in self.herb_buffs:
            speed *= 1.35
        if "nimbleness" in self.cheese_buffs:
            speed *= 1.20
        textile_swift = self.get_textile_bonus("swiftness")
        if textile_swift > 0:
            speed *= (1.0 + textile_swift)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vx = -speed
            self.facing = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vx = speed
            self.facing = 1

        pressing_down = keys[pygame.K_s] or keys[pygame.K_DOWN]
        self._on_ladder = self._in_ladder()
        if self._on_ladder:
            if keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]:
                self.vy = -4   # climb up
            elif pressing_down:
                self.vy = 2    # climb down
            else:
                self.vy = 0    # hold position
        elif self._in_water():
            if keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]:
                self.vy = -3   # swim up
            self.vx *= 0.55    # water drag on horizontal movement
        elif (keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.on_ground:
            self.vy = JUMP_FORCE * (1.25 if "vivacity" in self.wine_buffs else 1.0)
            self.on_ground = False

        mining = False
        harvest_target = None
        shift_held = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        self._shift_held = shift_held

        # Keyboard mining: Z key digs in the direction you're facing.
        # Z + W = dig up, Z + S = dig down.
        if keys[pygame.K_z]:
            mining = True
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                bx = int((self.x + PLAYER_W / 2) // BLOCK_SIZE)
                by = int(self.y // BLOCK_SIZE) - 1
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                bx = int((self.x + PLAYER_W / 2) // BLOCK_SIZE)
                by = int((self.y + PLAYER_H - 1) // BLOCK_SIZE) + 1
            else:
                by = int((self.y + PLAYER_H / 2) // BLOCK_SIZE)
                if self.facing == 1:
                    bx = int((self.x + PLAYER_W - 1) // BLOCK_SIZE) + 1
                else:
                    bx = int(self.x // BLOCK_SIZE) - 1
            self._mine_at(bx, by, dt)

        # Mouse mining: left-click, but only on the facing side.
        elif mouse_buttons[0]:
            mining = True
            mx, my = mouse_world_pos
            pcx = self.x + PLAYER_W / 2

            # Try animal interaction first
            harvest_target = self._find_animal_at(mx, my)
            if harvest_target is not None:
                result = harvest_target.try_harvest(self, dt)
                if result is not None:
                    for item_id, count in result:
                        for _ in range(count):
                            self._add_item(item_id)
                    self._consume_tool_use()
                    self._on_milk_harvested(harvest_target, result)
                if getattr(harvest_target, 'dead', False):
                    if harvest_target in self.world.entities:
                        self.world.entities.remove(harvest_target)
                    harvest_target = None
                self._reset_mine()
            else:
                # Normal block mining (facing-side check)
                if self.facing == 1 and mx < pcx - BLOCK_SIZE * 0.5:
                    self._reset_mine()
                elif self.facing == -1 and mx > pcx + BLOCK_SIZE * 0.5:
                    self._reset_mine()
                else:
                    bx = int(mx // BLOCK_SIZE)
                    by = int(my // BLOCK_SIZE)
                    cx = pcx / BLOCK_SIZE
                    cy = (self.y + PLAYER_H / 2) / BLOCK_SIZE
                    if ((bx - cx) ** 2 + (by - cy) ** 2) ** 0.5 > MINE_REACH:
                        self._reset_mine()
                    else:
                        self._mine_at(bx, by, dt)
        if not mining:
            self._reset_mine()

        # Track mouse target for farm sense display
        self.target_block = None
        mx, my = mouse_world_pos
        tbx = int(mx // BLOCK_SIZE)
        tby = int(my // BLOCK_SIZE)
        pcx = self.x + PLAYER_W / 2
        if ((tbx - pcx / BLOCK_SIZE) ** 2 + (tby - (self.y + PLAYER_H / 2) / BLOCK_SIZE) ** 2) ** 0.5 <= MINE_REACH:
            self.target_block = (tbx, tby)

        # Reset harvest state for animals not currently targeted
        for entity in getattr(self.world, 'entities', []):
            if entity is not harvest_target:
                entity.reset_harvest()

        # Block placement: right-click = mouse target, Ctrl = block in facing direction
        # Hold Shift to place in background layer instead of foreground
        self.bg_place_mode = bool(shift_held)
        placing = mouse_buttons[2] or keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]
        if placing:
            if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                # Ctrl: place in facing direction
                by = int((self.y + PLAYER_H / 2) // BLOCK_SIZE)
                if self.facing == 1:
                    bx = int((self.x + PLAYER_W - 1) // BLOCK_SIZE) + 1
                else:
                    bx = int(self.x // BLOCK_SIZE) - 1
                self.place_target = (bx, by)
                self._try_place(bx, by, bg=self.bg_place_mode)
            else:
                # Right-click: place at cursor
                mx, my = mouse_world_pos
                bx = int(mx // BLOCK_SIZE)
                by = int(my // BLOCK_SIZE)
                cx = (self.x + PLAYER_W / 2) / BLOCK_SIZE
                cy = (self.y + PLAYER_H / 2) / BLOCK_SIZE
                if ((bx - cx) ** 2 + (by - cy) ** 2) ** 0.5 <= MINE_REACH:
                    # Feed animals (or mount horses) before block placement
                    feed_target = self._find_animal_at(mx, my)
                    if feed_target is not None and not getattr(feed_target, 'dead', False):
                        from horses import Horse as _Horse
                        held = self.hotbar[self.selected_slot]
                        if isinstance(feed_target, _Horse) and feed_target.tamed and held == "saddle":
                            if feed_target._broken:
                                self.mounted_horse = feed_target
                                feed_target.rider = self
                            else:
                                self._pending_horse_break = feed_target
                        else:
                            feed_target.try_feed(self)
                    else:
                        self.place_target = (bx, by)
                        self._try_place(bx, by, bg=self.bg_place_mode)
                else:
                    self.place_target = None
        else:
            self.place_target = None

    def _handle_horse_input(self, keys, dt):
        horse = self.mounted_horse
        gait = horse.traits.get("gait", 1.0)
        base_speed = MOVE_SPEED * (1.0 + horse.traits["speed_rating"]) * (0.9 + gait * 0.1)
        if horse.traits.get("horseshoe_applied"):
            base_speed *= 1.0 + getattr(self, "horse_shoe_bonus", 0.05)

        # Spacebar sprint burst — endurance gene slows drain (higher = slower)
        if keys[pygame.K_SPACE] and horse.stamina > 0 and self._sprint_cooldown <= 0:
            endurance = horse.traits.get("endurance", 1.0)
            drain = 25.0 * getattr(self, "horse_stamina_drain_mult", 1.0) / endurance * dt
            horse.stamina = max(0.0, horse.stamina - drain)
            if horse.stamina == 0.0:
                self._sprint_cooldown = 3.0
            base_speed *= 1.5
        else:
            self._sprint_cooldown = max(0.0, self._sprint_cooldown - dt)

        self.vx = 0.0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vx = -base_speed
            self.facing = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vx = base_speed
            self.facing = 1

        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.vy = JUMP_FORCE * 0.9
            self.on_ground = False

    def _find_animal_at(self, mx, my):
        for entity in getattr(self.world, 'entities', []):
            if entity.rect.collidepoint(mx, my) and entity.in_range(self):
                return entity
        return None

    def _reset_mine(self):
        self.mining_block = None
        self.mine_progress = 0.0
        self._mine_time = 0.0

    def _has_line_of_sight(self, target_bx, target_by):
        px = (self.x + PLAYER_W / 2) / BLOCK_SIZE
        py = (self.y + PLAYER_H / 2) / BLOCK_SIZE
        dx = (target_bx + 0.5) - px
        dy = (target_by + 0.5) - py
        dist = (dx * dx + dy * dy) ** 0.5
        if dist == 0:
            return True
        step = 0.35
        sx, sy = dx / dist * step, dy / dist * step
        cx, cy = px + sx, py + sy
        for _ in range(int(dist / step)):
            ibx, iby = int(cx), int(cy)
            if ibx == target_bx and iby == target_by:
                return True
            if self.world.is_solid(ibx, iby):
                return False
            cx += sx
            cy += sy
        return True

    def _mine_at(self, bx, by, dt):
        block_id = self.world.get_block(bx, by)
        if block_id == AIR:
            if not self._shift_held:
                self._reset_mine()
                return
            bg_bid = self.world.get_bg_block(bx, by)
            if bg_bid == SKY_OPENING:
                self._reset_mine()
                return
            if bg_bid == AIR:
                # Cave-wall backdrop: only drawn below procedural surface height.
                # Mining it replaces the tile with a SKY_OPENING sentinel so the
                # renderer shows sky — lets the player clear out mountains.
                if by <= self.world.surface_height(bx):
                    self._reset_mine()
                    return
                if self.mining_block != (bx, by):
                    self.mining_block = (bx, by)
                    self._mine_time = 0.0
                    self._mine_total = max(0.05, BLOCKS[STONE]["hardness"] / self._mining_power_for(STONE))
                self._mine_time += dt
                self.mine_progress = min(1.0, self._mine_time / self._mine_total)
                if self.mine_progress >= 1.0:
                    self.world.set_bg_block(bx, by, SKY_OPENING)
                    self._reset_mine()
                return
            hardness = BLOCKS[bg_bid]["hardness"]
            if hardness == float('inf'):
                return
            if self.mining_block != (bx, by):
                self.mining_block = (bx, by)
                self._mine_time = 0.0
                self._mine_total = max(0.05, hardness / self._mining_power_for(bg_bid))
            self._mine_time += dt
            self.mine_progress = min(1.0, self._mine_time / self._mine_total)
            if self.mine_progress >= 1.0:
                if bg_bid == SCULPTURE_BLOCK_BODY:
                    ptr = self.world.sculpture_data.get((bx, by))
                    if ptr and "root" in ptr:
                        rbx, rby = ptr["root"]
                        self._demolish_sculpture(rbx, rby)
                    self._reset_mine()
                    return
                if bg_bid == SCULPTURE_BLOCK_ROOT:
                    self._demolish_sculpture(bx, by)
                    self._reset_mine()
                    return
                if bg_bid == CUSTOM_TAPESTRY_BODY:
                    ptr = self.world.tapestry_data.get((bx, by))
                    if ptr and "root" in ptr:
                        rbx, rby = ptr["root"]
                        self._demolish_tapestry(rbx, rby)
                    self._reset_mine()
                    return
                if bg_bid == CUSTOM_TAPESTRY_ROOT:
                    self._demolish_tapestry(bx, by)
                    self._reset_mine()
                    return
                block_data = BLOCKS[bg_bid]
                drop = block_data["drop"]
                if drop:
                    chance = block_data.get("drop_chance", 1.0)
                    if random.random() < chance:
                        self._add_item(drop)
                self.world.set_bg_block(bx, by, AIR)
                self._reset_mine()
            return
        if block_id in YOUNG_CROP_BLOCKS:
            self._reset_mine()
            return

        hardness = BLOCKS[block_id]["hardness"]
        if hardness == float('inf'):
            return

        if self.mining_block != (bx, by):
            self.mining_block = (bx, by)
            self._mine_time = 0.0
            self._mine_total = hardness / self._mining_power_for(block_id)

        self._mine_time += dt
        self.mine_progress = min(1.0, self._mine_time / self._mine_total)

        if self.mine_progress >= 1.0:
            if block_id == ROCK_DEPOSIT:
                rock = self._rock_gen.generate(bx, by, self.get_depth(), self.world.get_biome(bx))
                self.rocks.append(rock)
                self.discovered_types.add(rock.base_type)
                self.pending_notifications.append(
                    ("Rock", rock.base_type.replace("_", " ").title(), rock.rarity))
            elif block_id == WILDFLOWER_PATCH:
                flower = self._flower_gen.generate(bx, by, self.world.get_biodome(bx))
                self.wildflowers.append(flower)
                self.discovered_flower_types.add(flower.flower_type)
                self.pending_notifications.append(
                    ("Wildflower", flower.flower_type.replace("_", " ").title(), flower.rarity))
            elif block_id == FOSSIL_DEPOSIT:
                fossil = self._fossil_gen.generate(bx, by, self.get_depth(), self.world.get_biome(bx))
                self.fossils.append(fossil)
                self.pending_notifications.append(
                    ("Raw Fossil", "Prepare at Fossil Table", "common"))
            elif block_id == GEM_DEPOSIT:
                gem = self._gem_gen.generate(bx, by, self.get_depth(), self.world.get_biome(bx))
                self.gems.append(gem)
                self.discovered_gem_types.add(gem.gem_type)
                self.pending_notifications.append(
                    ("Gem", gem.gem_type.replace("_", " ").title(), gem.rarity))
            elif block_id == SALT_DEPOSIT:
                biodome = self.world.get_biodome(bx)
                crystal = self._salt_gen.generate(biodome)
                self.salt_crystals.append(crystal)
                self.pending_notifications.append(("Salt", "Salt Deposit", None))
            elif block_id == COFFEE_CROP_MATURE:
                biodome = self.world.get_biodome(bx)
                # Farmed crops: compute terroir from soil below the crop tile.
                moisture  = self.world._soil_moisture.get((bx, by + 1), 0)
                fertility = self.world._soil_fertility.get((bx, by + 1), 0)
                if moisture > 0 or fertility > 0:
                    from soil import MAX_MOISTURE, MAX_FERTILITY
                    terroir = (moisture / MAX_MOISTURE * 0.5 + fertility / MAX_FERTILITY * 0.5)
                else:
                    terroir = 0.0  # wild bush — no terroir bonus
                bean = self._coffee_gen.generate(biodome, terroir=terroir)
                self.coffee_beans.append(bean)
                self._add_item("coffee_seed")
                self.pending_notifications.append(("Coffee", "Coffee Cherry", None))
            elif block_id == GRAPEVINE_CROP_MATURE:
                biodome = self.world.get_biodome(bx)
                grape = self._wine_gen.generate(biodome)
                self.wine_grapes.append(grape)
                self._add_item("grape_seed")
                self.pending_notifications.append(("Wine", "Grape Cluster", None))
            elif block_id == GRAIN_CROP_MATURE:
                biodome = self.world.get_biodome(bx)
                spirit = self._spirit_gen.generate(biodome)
                self.spirits.append(spirit)
                self._add_item("grain_seed")
                self.pending_notifications.append(("Spirits", "Grain Harvest", None))
            elif block_id == TEA_CROP_MATURE:
                biodome = self.world.get_biodome(bx)
                leaf = self._tea_gen.generate(biodome)
                self.tea_leaves.append(leaf)
                self._add_item("tea_seed")
                self.pending_notifications.append(("Tea", "Tea Leaf", None))
            elif block_id == FLAX_CROP_MATURE:
                self._add_item("flax_fiber")
                self._add_item("flax_seed")
                self.pending_notifications.append(("Textile", "Flax Harvested", None))
            elif block_id == COTTON_CROP_MATURE:
                self._add_item("cotton_fiber")
                self._add_item("cotton_seed")
                self.pending_notifications.append(("Textile", "Cotton Harvested", None))
            elif block_id in CAVE_MUSHROOMS:
                self.mushrooms_found[block_id] = self.mushrooms_found.get(block_id, 0) + 1
                self.discovered_mushroom_types.add(block_id)
                drop = BLOCKS[block_id].get("drop")
                if drop in ("cave_mushroom", "rare_mushroom"):
                    self._add_item(drop)
                self.pending_notifications.append(("Mushroom", block_id, None))
            else:
                block_data = BLOCKS[block_id]
                drop = block_data["drop"]
                if drop:
                    if block_id in MATURE_CROP_BLOCKS:
                        # Care-scaled yield: running-mean care across growth → multiplier.
                        csum, ccount = self.world._crop_care_sum.pop((bx, by), (0.0, 0))
                        avg_care = csum / ccount if ccount > 0 else 0.5
                        young_bid  = MATURE_TO_YOUNG_CROP.get(block_id, block_id)
                        prefs      = _soil.get_prefs(young_bid)
                        base_yield = prefs.get("base_yield", 1)
                        count      = max(1, int(round(base_yield * _soil.yield_multiplier(avg_care))))
                        if self.harvest_bonus >= 1:
                            count += 1
                        if "abundance" in self.cheese_buffs and count >= 1:
                            import random as _r
                            if _r.random() < 0.20:
                                count += 1
                        self._add_item(drop, count)
                        self.known_crops.add(young_bid)
                        self._emit_harvest_float(bx, by, drop, count, avg_care)
                    else:
                        chance = block_data.get("drop_chance", 1.0)
                        if random.random() < chance:
                            count = 1
                            if block_id in (COAL_ORE, IRON_ORE, GOLD_ORE, CRYSTAL_ORE, RUBY_ORE):
                                count = self.world._ore_richness.get((bx, by), 1)
                            self._add_item(drop, count)
                if block_id == CHEST_BLOCK:
                    for item_id, count in self.world.chest_data.pop((bx, by), {}).items():
                        if count > 0:
                            self._add_item(item_id, count)
                if block_id == GARDEN_BLOCK:
                    garden_flowers = self.world.garden_data.pop((bx, by), [])
                    for wf in garden_flowers:
                        self.wildflowers.append(wf)
                if block_id == WILDFLOWER_DISPLAY_BLOCK:
                    stored = self.world.wildflower_display_data.pop((bx, by), None)
                    if stored is not None:
                        self.wildflowers.append(stored)
                if block_id == COMPOST_BIN_BLOCK:
                    bin_data = self.world.compost_bin_data.pop((bx, by), None)
                    if bin_data:
                        for item_id, count in bin_data["input"].items():
                            if count > 0:
                                self._add_item(item_id, count)
                        if bin_data["output"] > 0:
                            self._add_item("compost", bin_data["output"])
                if block_id == POTTERY_DISPLAY_BLOCK:
                    piece = self.world.pottery_display_data.pop((bx, by), None)
                    if piece is not None:
                        from pottery import get_output_item
                        self._add_item(get_output_item(piece))
                # Mature crops also drop seeds back
                if block_id == STRAWBERRY_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("strawberry_seed")
                elif block_id == WHEAT_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("wheat_seed")
                elif block_id == CARROT_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("carrot_seed")
                elif block_id == TOMATO_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("tomato_seed")
                elif block_id == CORN_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("corn_seed")
                elif block_id == PUMPKIN_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("pumpkin_seed")
                elif block_id == APPLE_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("apple_seed")
                elif block_id == RICE_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("rice_seed")
                elif block_id == GINGER_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("ginger_seed")
                elif block_id == BOK_CHOY_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("bok_choy_seed")
                elif block_id == GARLIC_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("garlic_seed")
                elif block_id == SCALLION_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("scallion_seed")
                elif block_id == CHILI_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("chili_seed")
                elif block_id == PEPPER_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("pepper_seed")
                elif block_id == ONION_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("onion_seed")
                elif block_id == POTATO_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("potato_seed")
                elif block_id == EGGPLANT_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("eggplant_seed")
                elif block_id == CABBAGE_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("cabbage_seed")
                elif block_id == BEET_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("beet_seed")
                elif block_id == TURNIP_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("turnip_seed")
                elif block_id == LEEK_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("leek_seed")
                elif block_id == ZUCCHINI_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("zucchini_seed")
                elif block_id == SWEET_POTATO_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("sweet_potato_seed")
                elif block_id == WATERMELON_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("watermelon_seed")
                elif block_id == RADISH_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("radish_seed")
                elif block_id == PEA_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("pea_seed")
                elif block_id == CELERY_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("celery_seed")
                elif block_id == BROCCOLI_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("broccoli_seed")
                # Premium mature crops: drop premium seeds
                elif block_id == STRAWBERRY_CROP_MATURE_P:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("strawberry_seed_premium")
                elif block_id == TOMATO_CROP_MATURE_P:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("tomato_seed_premium")
                elif block_id == WATERMELON_CROP_MATURE_P:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("watermelon_seed_premium")
                elif block_id == CORN_CROP_MATURE_P:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("corn_seed_premium")
                elif block_id == RICE_CROP_MATURE_P:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("rice_seed_premium")
                # Bushes: small chance of food directly
                elif block_id == STRAWBERRY_BUSH and random.random() < 0.25:
                    self._add_item("strawberry")
                elif block_id == WHEAT_BUSH and random.random() < 0.20:
                    self._add_item("wheat")
                elif block_id == CARROT_BUSH and random.random() < 0.30:
                    self._add_item("carrot")
                elif block_id == TOMATO_BUSH and random.random() < 0.25:
                    self._add_item("tomato")
                elif block_id == CORN_BUSH and random.random() < 0.20:
                    self._add_item("corn")
                elif block_id == PUMPKIN_BUSH and random.random() < 0.15:
                    self._add_item("pumpkin")
                elif block_id == APPLE_BUSH and random.random() < 0.30:
                    self._add_item("apple")
                elif block_id == RICE_BUSH and random.random() < 0.25:
                    self._add_item("rice")
                elif block_id == GINGER_BUSH and random.random() < 0.20:
                    self._add_item("ginger")
                elif block_id == BOK_CHOY_BUSH and random.random() < 0.30:
                    self._add_item("bok_choy")
                elif block_id == GARLIC_BUSH and random.random() < 0.20:
                    self._add_item("garlic")
                elif block_id == SCALLION_BUSH and random.random() < 0.30:
                    self._add_item("scallion")
                elif block_id == CHILI_BUSH and random.random() < 0.25:
                    self._add_item("chili")
                elif block_id == PEPPER_BUSH and random.random() < 0.25:
                    self._add_item("pepper")
                elif block_id == ONION_BUSH and random.random() < 0.20:
                    self._add_item("onion")
                elif block_id == POTATO_BUSH and random.random() < 0.20:
                    self._add_item("potato")
                elif block_id == EGGPLANT_BUSH and random.random() < 0.25:
                    self._add_item("eggplant")
                elif block_id == CABBAGE_BUSH and random.random() < 0.30:
                    self._add_item("cabbage")
                elif block_id == BEET_BUSH and random.random() < 0.25:
                    self._add_item("beet")
                elif block_id == TURNIP_BUSH and random.random() < 0.25:
                    self._add_item("turnip")
                elif block_id == LEEK_BUSH and random.random() < 0.30:
                    self._add_item("leek")
                elif block_id == ZUCCHINI_BUSH and random.random() < 0.20:
                    self._add_item("zucchini")
                elif block_id == SWEET_POTATO_BUSH and random.random() < 0.20:
                    self._add_item("sweet_potato")
                elif block_id == WATERMELON_BUSH and random.random() < 0.15:
                    self._add_item("watermelon")
                elif block_id == RADISH_BUSH and random.random() < 0.30:
                    self._add_item("radish")
                elif block_id == PEA_BUSH and random.random() < 0.30:
                    self._add_item("pea")
                elif block_id == CELERY_BUSH and random.random() < 0.25:
                    self._add_item("celery")
                elif block_id == BROCCOLI_BUSH and random.random() < 0.20:
                    self._add_item("broccoli")
                elif block_id == CHAMOMILE_BUSH and random.random() < 0.25:
                    self._add_item("chamomile_item")
                elif block_id == LAVENDER_BUSH and random.random() < 0.25:
                    self._add_item("lavender")
                elif block_id == MINT_BUSH and random.random() < 0.30:
                    self._add_item("mint")
                elif block_id == ROSEMARY_BUSH and random.random() < 0.20:
                    self._add_item("rosemary")
                elif block_id == THYME_BUSH and random.random() < 0.25:
                    self._add_item("thyme")
                elif block_id == SAGE_BUSH and random.random() < 0.20:
                    self._add_item("sage")
                elif block_id == BASIL_BUSH and random.random() < 0.30:
                    self._add_item("basil")
                elif block_id == OREGANO_BUSH and random.random() < 0.25:
                    self._add_item("oregano")
                elif block_id == DILL_BUSH and random.random() < 0.25:
                    self._add_item("dill")
                elif block_id == FENNEL_BUSH and random.random() < 0.20:
                    self._add_item("fennel")
                elif block_id == TARRAGON_BUSH and random.random() < 0.20:
                    self._add_item("tarragon")
                elif block_id == LEMON_BALM_BUSH and random.random() < 0.30:
                    self._add_item("lemon_balm")
                elif block_id == ECHINACEA_BUSH and random.random() < 0.15:
                    self._add_item("echinacea")
                elif block_id == VALERIAN_BUSH and random.random() < 0.15:
                    self._add_item("valerian")
                elif block_id == ST_JOHNS_WORT_BUSH and random.random() < 0.20:
                    self._add_item("st_johns_wort")
                elif block_id == YARROW_BUSH and random.random() < 0.20:
                    self._add_item("yarrow")
                elif block_id == BERGAMOT_BUSH and random.random() < 0.20:
                    self._add_item("bergamot")
                elif block_id == WORMWOOD_BUSH and random.random() < 0.15:
                    self._add_item("wormwood")
                elif block_id == RUE_BUSH and random.random() < 0.15:
                    self._add_item("rue")
                elif block_id == LEMON_VERBENA_BUSH and random.random() < 0.25:
                    self._add_item("lemon_verbena")
                elif block_id == HYSSOP_BUSH and random.random() < 0.20:
                    self._add_item("hyssop")
                elif block_id == CATNIP_BUSH and random.random() < 0.25:
                    self._add_item("catnip")
                elif block_id == WOOD_SORREL_BUSH and random.random() < 0.30:
                    self._add_item("wood_sorrel")
                elif block_id == MARJORAM_BUSH and random.random() < 0.25:
                    self._add_item("marjoram")
                elif block_id == SAVORY_BUSH and random.random() < 0.20:
                    self._add_item("savory")
                elif block_id == ANGELICA_BUSH and random.random() < 0.15:
                    self._add_item("angelica")
                elif block_id == BORAGE_BUSH and random.random() < 0.25:
                    self._add_item("borage")
                elif block_id == COMFREY_BUSH and random.random() < 0.20:
                    self._add_item("comfrey")
                elif block_id == MUGWORT_BUSH and random.random() < 0.25:
                    self._add_item("mugwort")
            if block_id in PERENNIAL_CROP_MATURE and random.random() > 0.33:
                self.world.set_block(bx, by, MATURE_TO_YOUNG_CROP[block_id])
            else:
                self.world.set_block(bx, by, AIR)
            self._consume_tool_use()
            self._reset_mine()

    def _selected_place_block(self):
        """Returns (item_id, block_id) for the selected hotbar slot, or (None, None)."""
        item_id = self.hotbar[self.selected_slot]
        if item_id is None:
            return None, None
        block_id = ITEMS.get(item_id, {}).get("place_block")
        if block_id is None:
            return None, None
        if self.inventory.get(item_id, 0) <= 0:
            return None, None
        return item_id, block_id

    def _try_place(self, bx, by, bg=False):
        if not bg:
            current = self.world.get_block(bx, by)
            if current == WOOD_DOOR_CLOSED:
                self.world.set_block(bx, by, WOOD_DOOR_OPEN)
                for dy in (-1, 1):
                    if self.world.get_block(bx, by + dy) == WOOD_DOOR_CLOSED:
                        self.world.set_block(bx, by + dy, WOOD_DOOR_OPEN); break
                return
            if current == WOOD_DOOR_OPEN:
                self.world.set_block(bx, by, WOOD_DOOR_CLOSED)
                for dy in (-1, 1):
                    if self.world.get_block(bx, by + dy) == WOOD_DOOR_OPEN:
                        self.world.set_block(bx, by + dy, WOOD_DOOR_CLOSED); break
                return
            if current == IRON_DOOR_CLOSED:
                self.world.set_block(bx, by, IRON_DOOR_OPEN)
                for dy in (-1, 1):
                    if self.world.get_block(bx, by + dy) == IRON_DOOR_CLOSED:
                        self.world.set_block(bx, by + dy, IRON_DOOR_OPEN); break
                return
            if current == IRON_DOOR_OPEN:
                self.world.set_block(bx, by, IRON_DOOR_CLOSED)
                for dy in (-1, 1):
                    if self.world.get_block(bx, by + dy) == IRON_DOOR_OPEN:
                        self.world.set_block(bx, by + dy, IRON_DOOR_CLOSED); break
                return
            for closed, opened in (
                (COBALT_DOOR_CLOSED,        COBALT_DOOR_OPEN),
                (CRIMSON_CEDAR_DOOR_CLOSED, CRIMSON_CEDAR_DOOR_OPEN),
                (TEAL_DOOR_CLOSED,          TEAL_DOOR_OPEN),
                (SAFFRON_DOOR_CLOSED,       SAFFRON_DOOR_OPEN),
            ):
                if current == closed:
                    self.world.set_block(bx, by, opened)
                    for dy in (-1, 1):
                        if self.world.get_block(bx, by + dy) == closed:
                            self.world.set_block(bx, by + dy, opened); break
                    return
                if current == opened:
                    self.world.set_block(bx, by, closed)
                    for dy in (-1, 1):
                        if self.world.get_block(bx, by + dy) == opened:
                            self.world.set_block(bx, by + dy, closed); break
                    return
            if current == WOOD_FENCE:
                self.world.set_block(bx, by, WOOD_FENCE_OPEN)
                return
            if current == WOOD_FENCE_OPEN:
                self.world.set_block(bx, by, WOOD_FENCE)
                return
            if current == IRON_FENCE:
                self.world.set_block(bx, by, IRON_FENCE_OPEN)
                return
            if current == IRON_FENCE_OPEN:
                self.world.set_block(bx, by, IRON_FENCE)
                return
        item_id = self.hotbar[self.selected_slot]
        if item_id is None:
            return
        item_data = ITEMS.get(item_id, {})
        if item_data.get("edible", False):
            self._try_eat()
            return
        if not bg:
            spawn_type = item_data.get("spawn_automation")
            if spawn_type:
                if self.inventory.get(item_id, 0) <= 0:
                    return
                if spawn_type in FARM_BOT_TYPES:
                    adef = FARM_BOT_DEFS[spawn_type]
                    ax = bx * BLOCK_SIZE + (BLOCK_SIZE - adef["w"]) // 2
                    ay = by * BLOCK_SIZE + (BLOCK_SIZE - adef["h"]) // 2
                    self.world.farm_bots.append(FarmBot(ax, ay, spawn_type))
                else:
                    adef = AUTOMATION_DEFS[spawn_type]
                    ax = bx * BLOCK_SIZE + (BLOCK_SIZE - adef["w"]) // 2
                    ay = by * BLOCK_SIZE + (BLOCK_SIZE - adef["h"]) // 2
                    pcx = int((self.x + PLAYER_W / 2) // BLOCK_SIZE)
                    pcy = int((self.y + PLAYER_H / 2) // BLOCK_SIZE)
                    ddx, ddy = bx - pcx, by - pcy
                    if abs(ddx) >= abs(ddy):
                        spawn_dir = (1 if ddx >= 0 else -1, 0)
                    else:
                        spawn_dir = (0, 1 if ddy >= 0 else -1)
                    self.world.automations.append(Automation(ax, ay, spawn_type, spawn_dir))
                self.inventory[item_id] -= 1
                if self.inventory[item_id] <= 0:
                    del self.inventory[item_id]
                    for i in range(HOTBAR_SIZE):
                        if self.hotbar[i] == item_id:
                            self.hotbar[i] = None
                            break
                return
            # Oil barrel harvesting: use empty_barrel on an OIL block
            if item_data.get("harvest_oil") and self.world.get_block(bx, by) == OIL:
                if self.inventory.get(item_id, 0) > 0:
                    self.world.set_block(bx, by, AIR)
                    self._add_item("oil_barrel")
                    self.inventory[item_id] -= 1
                    if self.inventory[item_id] <= 0:
                        del self.inventory[item_id]
                        for i in range(HOTBAR_SIZE):
                            if self.hotbar[i] == item_id:
                                self.hotbar[i] = None
                                break
                return
            # Hoe: till grass/dirt/sand into tilled soil.
            if item_data.get("till_tool"):
                target = self.world.get_block(bx, by)
                if target in (GRASS, DIRT, SAND):
                    # Don't till under a solid block — soil dries out & stays barren.
                    if by > 0 and self.world.is_solid(bx, by - 1):
                        return
                    self.world.set_block(bx, by, TILLED_SOIL)
                    self.world._soil_moisture[(bx, by)] = _soil.TILL_START_MOISTURE
                    self._consume_tool_use()
                return
            # Watering can: refill from WATER; otherwise apply moisture to tilled soil / crop-on-tilled.
            if item_data.get("water_tool"):
                self._use_watering_can(bx, by)
                return
            # Compost: apply fertility to tilled soil or the tilled tile below a young crop.
            if item_data.get("fertilize_tool"):
                target = self.world.get_block(bx, by)
                soil_pos = None
                if target == TILLED_SOIL:
                    soil_pos = (bx, by)
                elif target in YOUNG_CROP_BLOCKS and self.world.get_block(bx, by + 1) == TILLED_SOIL:
                    soil_pos = (bx, by + 1)
                if soil_pos is None:
                    return
                fx, fy = soil_pos
                gain    = item_data.get("fertility_gain", _soil.COMPOST_FERTILITY_GAIN)
                cap     = self.world.max_fertility
                cur     = self.world._soil_fertility.get((fx, fy), 0)
                self.world._soil_fertility[(fx, fy)] = min(cap, cur + gain)
                self.inventory[item_id] = self.inventory.get(item_id, 1) - 1
                if self.inventory[item_id] <= 0:
                    del self.inventory[item_id]
                    for i in range(HOTBAR_SIZE):
                        if self.hotbar[i] == item_id:
                            self.hotbar[i] = None
                            break
                return
            # Elevator car placement — place on or adjacent to an elevator stop
            if item_data.get("spawn_elevator_car"):
                if self.inventory.get(item_id, 0) <= 0:
                    return
                nearby = self.get_nearby_elevator_stop()
                if nearby is None:
                    return
                from elevators import ElevatorCar
                nbx, nby = nearby
                self.world.elevator_cars.append(ElevatorCar(nbx, nby))
                self.inventory[item_id] -= 1
                if self.inventory[item_id] <= 0:
                    del self.inventory[item_id]
                    for i in range(HOTBAR_SIZE):
                        if self.hotbar[i] == item_id:
                            self.hotbar[i] = None
                            break
                return
            # Minecart placement — must be near a mine track stop
            if item_data.get("spawn_minecart"):
                if self.inventory.get(item_id, 0) <= 0:
                    return
                nearby = self.get_nearby_mine_track_stop()
                if nearby is None:
                    return
                from minecarts import Minecart
                nbx, nby = nearby
                self.world.minecarts.append(Minecart(nby, nbx))
                self.inventory[item_id] -= 1
                if self.inventory[item_id] <= 0:
                    del self.inventory[item_id]
                    for i in range(HOTBAR_SIZE):
                        if self.hotbar[i] == item_id:
                            self.hotbar[i] = None
                            break
                return
            # Backhoe placement
            if item_data.get("spawn_backhoe"):
                if self.inventory.get(item_id, 0) <= 0:
                    return
                bh_x = bx * BLOCK_SIZE - (Backhoe.W - BLOCK_SIZE) // 2
                bh_y = by * BLOCK_SIZE
                self.world.backhoes.append(Backhoe(bh_x, bh_y))
                self.inventory[item_id] -= 1
                if self.inventory[item_id] <= 0:
                    del self.inventory[item_id]
                    for i in range(HOTBAR_SIZE):
                        if self.hotbar[i] == item_id:
                            self.hotbar[i] = None
                            break
                return
        if item_id == "sculpture":
            if bg and self._place_sculpture(bx, by):
                self.inventory[item_id] = self.inventory.get(item_id, 1) - 1
                if self.inventory[item_id] <= 0:
                    del self.inventory[item_id]
                    for i in range(HOTBAR_SIZE):
                        if self.hotbar[i] == item_id:
                            self.hotbar[i] = None
                            break
            return
        if item_id == "custom_tapestry":
            if bg and self._place_tapestry(bx, by):
                self.inventory[item_id] = self.inventory.get(item_id, 1) - 1
                if self.inventory[item_id] <= 0:
                    del self.inventory[item_id]
                    for i in range(HOTBAR_SIZE):
                        if self.hotbar[i] == item_id:
                            self.hotbar[i] = None
                            break
            return
        block_id = item_data.get("place_block")
        if block_id is None:
            return
        if block_id in STAIR_BLOCKS:
            block_id = STAIRS_RIGHT if self.facing == 1 else STAIRS_LEFT
        if self.inventory.get(item_id, 0) <= 0:
            return
        if bg:
            if block_id in _BG_DISALLOWED:
                return
            if self.world.get_bg_block(bx, by) not in (AIR, SKY_OPENING):
                return
            self.world.set_bg_block(bx, by, block_id)
        else:
            if self.world.get_block(bx, by) not in (AIR, WATER):
                return
            # Seeds must be planted on tilled soil (prep with a hoe first).
            if block_id in YOUNG_CROP_BLOCKS:
                if self.world.get_block(bx, by + 1) != TILLED_SOIL:
                    return
            # Don't place inside the player (passable blocks are exempt)
            passable = {LADDER, SAPLING} | BUSH_BLOCKS | YOUNG_CROP_BLOCKS | EQUIPMENT_BLOCKS
            if block_id not in passable:
                block_px = pygame.Rect(bx * BLOCK_SIZE, by * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                if block_px.colliderect(self.rect):
                    return
            self.world.set_block(bx, by, block_id)
        self.inventory[item_id] -= 1
        if self.inventory[item_id] <= 0:
            del self.inventory[item_id]
            for i in range(HOTBAR_SIZE):
                if self.hotbar[i] == item_id:
                    self.hotbar[i] = None

    def _use_watering_can(self, bx, by):
        """Water a tilled tile or young crop on tilled soil. No durability or refill needed."""
        target = self.world.get_block(bx, by)
        water_target = None
        if target == TILLED_SOIL:
            water_target = (bx, by)
        elif target in YOUNG_CROP_BLOCKS and self.world.get_block(bx, by + 1) == TILLED_SOIL:
            water_target = (bx, by + 1)
        if water_target is None:
            return
        wx, wy = water_target
        cur_m = self.world._soil_moisture.get((wx, wy), 0)
        self.world._soil_moisture[(wx, wy)] = min(_soil.MAX_MOISTURE, cur_m + _soil.WATERING_AMOUNT)

    def _consume_tool_use(self):
        """Decrement uses for a consumable tool in the selected hotbar slot."""
        slot = self.selected_slot
        item_id = self.hotbar[slot]
        if item_id is None:
            return
        max_uses = ITEMS.get(item_id, {}).get("max_uses")
        if max_uses is None:
            return
        uses = self.hotbar_uses[slot]
        if uses is None:
            return
        uses -= 1
        if uses <= 0:
            self.inventory[item_id] = self.inventory.get(item_id, 1) - 1
            if self.inventory.get(item_id, 0) <= 0:
                self.inventory.pop(item_id, None)
                self.hotbar[slot] = None
                self.hotbar_uses[slot] = None
            else:
                self.hotbar_uses[slot] = max_uses
        else:
            self.hotbar_uses[slot] = uses

    def _add_item(self, item_id, count=1):
        self.inventory[item_id] = self.inventory.get(item_id, 0) + count
        if item_id not in self.hotbar:
            for i in range(HOTBAR_SIZE):
                if self.hotbar[i] is None:
                    self.hotbar[i] = item_id
                    max_uses = ITEMS.get(item_id, {}).get("max_uses")
                    if max_uses is not None:
                        self.hotbar_uses[i] = max_uses
                    break

    def _on_milk_harvested(self, animal, result):
        """Generate a Cheese milk object whenever an animal yields milk."""
        milk_to_animal = {"milk": "cow", "goat_milk": "goat", "sheep_milk": "sheep"}
        for item_id, count in result:
            animal_type = milk_to_animal.get(item_id)
            if animal_type is None:
                continue
            bx = int(animal.x // BLOCK_SIZE)
            biodome = self.world.get_biodome(bx)
            for _ in range(count):
                wheel = self._cheese_gen.generate(biodome, animal_type)
                self.cheese_wheels.append(wheel)

    def _emit_harvest_float(self, bx, by, item_id, count, avg_care):
        if avg_care >= 0.7:
            label, color = "great care!", (100, 255, 120)
        elif avg_care >= 0.5:
            label, color = "good care",   (200, 255, 100)
        elif avg_care >= 0.3:
            label, color = "ok care",     (200, 200, 200)
        else:
            label, color = "neglected",   (220, 100, 100)
        name = ITEMS.get(item_id, {}).get("name", item_id)
        text = f"+{count} {name} ({label})"
        wx = bx * BLOCK_SIZE + BLOCK_SIZE // 2
        wy = by * BLOCK_SIZE
        self.pending_harvest_floats.append((wx, wy, text, color))

    def collect_all_items(self):
        drops = {k: v for k, v in self.inventory.items() if v > 0}
        self.inventory = {}
        self.hotbar = [None] * HOTBAR_SIZE
        self.hotbar_uses = [None] * HOTBAR_SIZE
        return drops

    def respawn(self):
        if self.spawn_x is not None and self.spawn_y is not None:
            self.x = float(self.spawn_x)
            self.y = float(self.spawn_y)
        else:
            sx = 0
            sy = self.world.surface_y_at(sx)
            self.x = float(sx * BLOCK_SIZE + (BLOCK_SIZE - PLAYER_W) // 2)
            self.y = float((sy - 2) * BLOCK_SIZE)
        self.vx = 0.0
        self.vy = 0.0
        self.health = MAX_HEALTH
        self.hunger = 100.0
        self.dead = False
        self._drowning_timer = 0.0

    def get_worn_textile(self, slot):
        uid = self.worn.get(slot)
        if uid:
            return next((t for t in self.textiles if t.uid == uid), None)
        return None

    def get_textile_bonus(self, stat):
        """Return passive bonus fraction (0.0–max) from the equipped garment for stat."""
        from textiles import GARMENT_BUFFS, GARMENT_MAX_BONUS
        for slot, uid in self.worn.items():
            if uid is None:
                continue
            t = next((x for x in self.textiles if x.uid == uid), None)
            if t and GARMENT_BUFFS.get(t.output_type) == stat:
                return t.quality * GARMENT_MAX_BONUS[stat]
        return 0.0

    def get_nearby_bed(self):
        from blocks import BED
        cx = int((self.x + PLAYER_W / 2) // BLOCK_SIZE)
        cy = int((self.y + PLAYER_H / 2) // BLOCK_SIZE)
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                if dx * self.facing < 0:
                    continue
                if self.world.get_block(cx + dx, cy + dy) == BED:
                    return (cx + dx, cy + dy)
        return None

    def set_spawn(self, bx, by):
        self.spawn_x = float(bx * BLOCK_SIZE + (BLOCK_SIZE - PLAYER_W) // 2)
        self.spawn_y = float((by - 1) * BLOCK_SIZE)

    # ------------------------------------------------------------------
    # Fishing
    # ------------------------------------------------------------------

    def has_fishing_pole(self):
        item_id = self.hotbar[self.selected_slot]
        return item_id is not None and ITEMS.get(item_id, {}).get("fishing_tool", False)

    def get_active_bait(self):
        """Return bait item_id from the hotbar slot immediately right of the fishing rod, else None."""
        bait_slot = self.selected_slot + 1
        if bait_slot >= HOTBAR_SIZE:
            return None
        item_id = self.hotbar[bait_slot]
        if item_id and ITEMS.get(item_id, {}).get("bait", False):
            return item_id
        return None

    def get_nearby_water_biome(self):
        """Return biome string if water is within 3 blocks and player is not in water, else None."""
        if self._in_water():
            return None
        cx = int((self.x + PLAYER_W / 2) // BLOCK_SIZE)
        cy = int((self.y + PLAYER_H / 2) // BLOCK_SIZE)
        for dy in range(-2, 3):
            for dx in range(-3, 4):
                if self.world.get_block(cx + dx, cy + dy) == WATER:
                    return self.world.get_biome(cx + dx)
        return None

    def on_fish_press(self):
        """Called when the player presses the fishing key (F)."""
        if self.fishing_state is None:
            return self._start_fishing()
        elif self.fishing_state == "biting":
            self._catch_fish()
            return True
        elif self.fishing_state == "casting":
            # Cancel
            self.fishing_state = None
            self._fishing_biome = None
            return True
        return False

    def _start_fishing(self):
        if not self.has_fishing_pole():
            return False
        biome = self.get_nearby_water_biome()
        if biome is None:
            return False
        self.fishing_state = "casting"
        self._fishing_timer = random.uniform(3.0, 8.0)
        self._fishing_biome = biome
        return True

    def _catch_fish(self):
        cx = int((self.x + PLAYER_W / 2) // BLOCK_SIZE)
        cy = int((self.y + PLAYER_H / 2) // BLOCK_SIZE)
        bait = self.get_active_bait()
        fish = self._fish_gen.generate(cx, cy, self._fishing_biome or "", bait=bait)
        self.fish_caught.append(fish)
        self.discovered_fish_species.add(fish.species)
        self._add_item("fish")
        self._consume_tool_use()
        if bait:
            self.inventory[bait] -= 1
            if self.inventory[bait] <= 0:
                del self.inventory[bait]
                bait_slot = self.selected_slot + 1
                if bait_slot < HOTBAR_SIZE and self.hotbar[bait_slot] == bait:
                    self.hotbar[bait_slot] = None
        self.pending_notifications.append(
            ("Fish", fish.species.replace("_", " ").title(), fish.rarity))
        self.fishing_state = "result"
        self._fishing_result = "caught"
        self._fishing_timer = 2.0

    def _update_fishing(self, dt):
        if self.fishing_state is None:
            return
        # Auto-cancel if pole no longer equipped or left the water
        if self.fishing_state in ("casting", "biting"):
            if not self.has_fishing_pole() or self.get_nearby_water_biome() is None:
                self.fishing_state = None
                self._fishing_biome = None
                return

        self._fishing_timer -= dt

        if self.fishing_state == "casting":
            if self._fishing_timer <= 0:
                self.fishing_state = "biting"
                self._fishing_timer = 2.0

        elif self.fishing_state == "biting":
            if self._fishing_timer <= 0:
                self.fishing_state = "result"
                self._fishing_result = "missed"
                self._fishing_timer = 1.5

        elif self.fishing_state == "result":
            if self._fishing_timer <= 0:
                self.fishing_state = None
                self._fishing_result = None
                self._fishing_biome = None

    def _try_eat(self):
        if self._eat_cooldown > 0:
            return False
        item_id = self.hotbar[self.selected_slot]
        if item_id is None:
            return False
        item_data = ITEMS.get(item_id, {})
        if not item_data.get("edible", False):
            return False
        if self.inventory.get(item_id, 0) <= 0:
            return False
        hunger_restore = item_data.get("hunger_restore", 0)
        if "preservation" in self.salt_buffs:
            hunger_restore = int(hunger_restore * 1.25)
        self.hunger = min(100.0, self.hunger + hunger_restore)
        self.health = min(MAX_HEALTH, self.health + hunger_restore * 0.25)
        self._eat_cooldown = 0.5
        if item_data.get("coffee_buff"):
            buff = item_data["coffee_buff"]
            duration = item_data.get("coffee_buff_duration", 60.0)
            duration *= 1.0 + self.coffee_buff_duration_bonus
            self.active_buffs[buff] = {"duration": duration}
        if item_data.get("wine_buff"):
            buff = item_data["wine_buff"]
            duration = item_data.get("wine_buff_duration", 120.0)
            self.wine_buffs[buff] = {"duration": duration}
        if item_data.get("tea_buff"):
            buff = item_data["tea_buff"]
            duration = item_data.get("tea_buff_duration", 90.0)
            self.tea_buffs[buff] = {"duration": duration}
        if item_data.get("herb_heal"):
            self.health = min(MAX_HEALTH, self.health + item_data["herb_heal"])
        if item_data.get("herb_buff"):
            buff = item_data["herb_buff"]
            duration = item_data.get("herb_buff_duration", 90.0)
            self.herb_buffs[buff] = {"duration": duration}
        if item_data.get("cheese_buff"):
            buff = item_data["cheese_buff"]
            duration = item_data.get("cheese_buff_duration", 90.0)
            if buff == "resilience":
                heal = item_data.get("cheese_heal_amount", 5)
                self.health = min(MAX_HEALTH, self.health + heal)
            else:
                self.cheese_buffs[buff] = {"duration": duration}
        if item_data.get("cheese_buff_2"):
            buff2 = item_data["cheese_buff_2"]
            dur2  = item_data.get("cheese_buff_2_duration", 60.0)
            if buff2 == "resilience":
                heal = item_data.get("cheese_heal_amount", 5)
                self.health = min(MAX_HEALTH, self.health + heal)
            else:
                self.cheese_buffs[buff2] = {"duration": dur2}
        if item_data.get("pottery_buff"):
            buff = item_data["pottery_buff"]
            duration = item_data.get("pottery_buff_duration", 120.0)
            duration *= 1.0 + self.pottery_buff_duration_bonus
            self.pottery_buffs[buff] = {"duration": duration}
        if item_data.get("salt_buff"):
            buff = item_data["salt_buff"]
            duration = item_data.get("salt_buff_duration", 90.0)
            self.salt_buffs[buff] = {"duration": duration}
        self.inventory[item_id] -= 1
        if self.inventory[item_id] <= 0:
            del self.inventory[item_id]
            for i in range(HOTBAR_SIZE):
                if self.hotbar[i] == item_id:
                    self.hotbar[i] = None
        return True

    # ------------------------------------------------------------------
    # Physics
    # ------------------------------------------------------------------

    def update(self, dt):
        if self.riding_elevator is not None:
            self.vy = 0.0
            self.vx = 0.0
            self.on_ground = True
            return  # car.update() sets player x/y each frame
        if self.riding_minecart is not None:
            self.vy = 0.0
            self.vx = 0.0
            self.on_ground = True
            return  # cart.update() sets player x/y each frame
        if self.blessing_timer > 0:
            self.blessing_timer -= dt
            if self.blessing_timer <= 0:
                self.blessing_timer = 0.0
                self.blessing_mult  = 1.0
        in_water = self._in_water()
        if self._on_ladder:
            self.vy = min(self.vy, 2)  # suppress gravity; allow slow drift but not free-fall
        elif in_water:
            # Buoyancy: reduced gravity and terminal velocity while submerged
            self.vy = min(self.vy + GRAVITY * 0.25, 2.5)
        else:
            self.vy = min(self.vy + GRAVITY, MAX_FALL)
        self._move_x(self.vx)
        prev_vy = self.vy
        landed = self._move_y(self.vy)
        if not self.god_mode:
            # Fall damage only applies outside water (wine "vivacity" negates it)
            if landed and prev_vy > 10 and not in_water and "vivacity" not in self.wine_buffs:
                dmg = int((prev_vy - 10) * 5)
                if "tranquility" in self.tea_buffs:
                    dmg = int(dmg * 0.7)
                resilience = self.get_textile_bonus("resilience")
                if resilience > 0:
                    dmg = int(dmg * (1.0 - resilience))
                self.health = max(0, self.health - dmg)
            # Drowning: after 5 s with head submerged, 5 HP/s damage
            if self._head_in_water():
                self._drowning_timer += dt
                if self._drowning_timer > 5.0:
                    resilience = self.get_textile_bonus("resilience")
                    drown_dmg = 5 * dt * (1.0 - resilience)
                    self.health = max(0, self.health - drown_dmg)
            else:
                self._drowning_timer = max(0.0, self._drowning_timer - dt * 2)
        else:
            self._drowning_timer = 0.0
            self.health = MAX_HEALTH
            self.hunger = 100.0
        # Hunger drain and starvation damage
        if self._eat_cooldown > 0:
            self._eat_cooldown -= dt
        # Tick active coffee and wine buffs
        for buff in list(self.active_buffs):
            self.active_buffs[buff]["duration"] -= dt
            if self.active_buffs[buff]["duration"] <= 0:
                del self.active_buffs[buff]
        for buff in list(self.wine_buffs):
            self.wine_buffs[buff]["duration"] -= dt
            if self.wine_buffs[buff]["duration"] <= 0:
                del self.wine_buffs[buff]
        for buff in list(self.tea_buffs):
            self.tea_buffs[buff]["duration"] -= dt
            if self.tea_buffs[buff]["duration"] <= 0:
                del self.tea_buffs[buff]
        for buff in list(self.herb_buffs):
            self.herb_buffs[buff]["duration"] -= dt
            if self.herb_buffs[buff]["duration"] <= 0:
                del self.herb_buffs[buff]
        for buff in list(self.cheese_buffs):
            self.cheese_buffs[buff]["duration"] -= dt
            if self.cheese_buffs[buff]["duration"] <= 0:
                del self.cheese_buffs[buff]
        for buff in list(self.pottery_buffs):
            self.pottery_buffs[buff]["duration"] -= dt
            if self.pottery_buffs[buff]["duration"] <= 0:
                del self.pottery_buffs[buff]
        for buff in list(self.salt_buffs):
            self.salt_buffs[buff]["duration"] -= dt
            if self.salt_buffs[buff]["duration"] <= 0:
                del self.salt_buffs[buff]
        if self._bow_cooldown > 0:
            self._bow_cooldown -= dt
        if not self.god_mode and not self.no_hunger:
            drain_mult = 1.0
            if "endurance" in self.active_buffs:
                drain_mult *= 0.6
            if "serenity" in self.wine_buffs:
                drain_mult *= 0.4
            if "longevity" in self.tea_buffs:
                drain_mult *= 0.45
            if "satiation" in self.cheese_buffs:
                drain_mult *= 0.60
        if "vitality" in self.cheese_buffs and self.hunger > 20.0:
            self.health = min(MAX_HEALTH, self.health + 1.0 * dt)
        if not self.god_mode and not self.no_hunger:
            self.hunger = max(0.0, self.hunger - self._hunger_drain_rate * drain_mult * dt)
            if self.hunger == 0.0:
                self.health = max(0, self.health - 3 * dt)
        # Death detection
        if not self.dead and self.health <= 0:
            self.dead = True
        self._update_fishing(dt)
        # Auto-close doors the player has walked away from
        if self._auto_opened_doors:
            player_left  = int(self.x // BLOCK_SIZE) - 1
            player_right = int((self.x + PLAYER_W - 1) // BLOCK_SIZE) + 1
            to_close = {(dbx, dby) for (dbx, dby) in self._auto_opened_doors
                        if dbx < player_left or dbx > player_right}
            for (dbx, dby) in to_close:
                self._auto_opened_doors.discard((dbx, dby))
                bid = self.world.get_block(dbx, dby)
                if bid == WOOD_DOOR_OPEN:
                    self.world.set_block(dbx, dby, WOOD_DOOR_CLOSED)
                elif bid == IRON_DOOR_OPEN:
                    self.world.set_block(dbx, dby, IRON_DOOR_CLOSED)

    def _move_x(self, dx):
        if dx == 0:
            return
        self.x += dx
        if self._collides():
            if self._try_auto_open_door():
                return
            if self._try_stair_step(dx):
                return
            self.x -= dx
            self.vx = 0.0

    def _try_auto_open_door(self):
        left  = int(self.x // BLOCK_SIZE)
        right = int((self.x + PLAYER_W - 1) // BLOCK_SIZE)
        top   = int(self.y // BLOCK_SIZE)
        bot   = int((self.y + PLAYER_H - 1) // BLOCK_SIZE)
        opened = False
        for bx in range(left, right + 1):
            for by in range(top, bot + 1):
                bid = self.world.get_block(bx, by)
                if bid == WOOD_DOOR_CLOSED:
                    self.world.set_block(bx, by, WOOD_DOOR_OPEN)
                    self._auto_opened_doors.add((bx, by))
                    for dy in (-1, 1):
                        if self.world.get_block(bx, by + dy) == WOOD_DOOR_CLOSED:
                            self.world.set_block(bx, by + dy, WOOD_DOOR_OPEN)
                            self._auto_opened_doors.add((bx, by + dy))
                            break
                    opened = True
                elif bid == IRON_DOOR_CLOSED:
                    self.world.set_block(bx, by, IRON_DOOR_OPEN)
                    self._auto_opened_doors.add((bx, by))
                    for dy in (-1, 1):
                        if self.world.get_block(bx, by + dy) == IRON_DOOR_CLOSED:
                            self.world.set_block(bx, by + dy, IRON_DOOR_OPEN)
                            self._auto_opened_doors.add((bx, by + dy))
                            break
                    opened = True
        return opened

    def _try_stair_step(self, dx):
        left  = int(self.x // BLOCK_SIZE)
        right = int((self.x + PLAYER_W - 1) // BLOCK_SIZE)
        top   = int(self.y // BLOCK_SIZE)
        bot   = int((self.y + PLAYER_H - 1) // BLOCK_SIZE)
        for bx in range(left, right + 1):
            for by in range(top, bot + 1):
                bid = self.world.get_block(bx, by)
                if (bid == STAIRS_RIGHT and dx > 0) or (bid == STAIRS_LEFT and dx < 0):
                    self.y -= BLOCK_SIZE
                    if not self._collides():
                        self.on_ground = False
                        return True
                    self.y += BLOCK_SIZE
        return False

    def _move_y(self, dy):
        if dy == 0:
            return False
        self.y += dy
        if self._collides():
            self.y -= dy
            hit_floor = dy > 0
            if hit_floor:
                self.on_ground = True
            self.vy = 0.0
            return hit_floor
        else:
            if dy > 0:
                self.on_ground = False
            return False

    def _in_ladder(self):
        left  = int(self.x // BLOCK_SIZE)
        right = int((self.x + PLAYER_W - 1) // BLOCK_SIZE)
        top   = int(self.y // BLOCK_SIZE)
        bot   = int((self.y + PLAYER_H - 1) // BLOCK_SIZE)
        for bx in range(left, right + 1):
            for by in range(top, bot + 1):
                if self.world.get_block(bx, by) == LADDER:
                    return True
        return False

    def _in_water(self):
        left  = int(self.x // BLOCK_SIZE)
        right = int((self.x + PLAYER_W - 1) // BLOCK_SIZE)
        top   = int(self.y // BLOCK_SIZE)
        bot   = int((self.y + PLAYER_H - 1) // BLOCK_SIZE)
        for bx in range(left, right + 1):
            for by in range(top, bot + 1):
                if self.world.get_block(bx, by) == WATER:
                    return True
        return False

    def _head_in_water(self):
        left  = int(self.x // BLOCK_SIZE)
        right = int((self.x + PLAYER_W - 1) // BLOCK_SIZE)
        head_y = int(self.y // BLOCK_SIZE)
        for bx in range(left, right + 1):
            if self.world.get_block(bx, head_y) == WATER:
                return True
        return False

    def _collides(self):
        left  = int(self.x // BLOCK_SIZE)
        right = int((self.x + PLAYER_W - 1) // BLOCK_SIZE)
        top   = int(self.y // BLOCK_SIZE)
        bot   = int((self.y + PLAYER_H - 1) // BLOCK_SIZE)
        for bx in range(left, right + 1):
            for by in range(top, bot + 1):
                if self.world.is_solid(bx, by):
                    return True
        return False

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def get_nearby_equipment(self):
        """Return the block_id of an equipment block within 2 blocks of the player, or None."""
        cx = int((self.x + PLAYER_W / 2) // BLOCK_SIZE)
        cy = int((self.y + PLAYER_H / 2) // BLOCK_SIZE)
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                if dx * self.facing < 0:
                    continue
                bid = self.world.get_block(cx + dx, cy + dy)
                if bid in EQUIPMENT_BLOCKS:
                    return bid
        return None

    def get_nearby_equipment_pos(self, target_bid):
        """Return (bx, by) of the nearest matching equipment block within 2 blocks, or None."""
        cx = int((self.x + PLAYER_W / 2) // BLOCK_SIZE)
        cy = int((self.y + PLAYER_H / 2) // BLOCK_SIZE)
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                if dx * self.facing < 0:
                    continue
                if self.world.get_block(cx + dx, cy + dy) == target_bid:
                    return (cx + dx, cy + dy)
        return None

    def get_nearby_chest(self):
        """Return (bx, by) of a chest block within 2 blocks of the player, or None."""
        cx = int((self.x + PLAYER_W / 2) // BLOCK_SIZE)
        cy = int((self.y + PLAYER_H / 2) // BLOCK_SIZE)
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                if dx * self.facing < 0:
                    continue
                if self.world.get_block(cx + dx, cy + dy) == CHEST_BLOCK:
                    return (cx + dx, cy + dy)
        return None

    def get_nearby_garden(self):
        """Return (bx, by) of a garden block within 2 blocks of the player, or None."""
        cx = int((self.x + PLAYER_W / 2) // BLOCK_SIZE)
        cy = int((self.y + PLAYER_H / 2) // BLOCK_SIZE)
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                if dx * self.facing < 0:
                    continue
                if self.world.get_block(cx + dx, cy + dy) == GARDEN_BLOCK:
                    return (cx + dx, cy + dy)
        return None

    def get_nearby_wildflower_display(self):
        """Return (bx, by) of a wildflower display block within 2 blocks of the player, or None."""
        cx = int((self.x + PLAYER_W / 2) // BLOCK_SIZE)
        cy = int((self.y + PLAYER_H / 2) // BLOCK_SIZE)
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                if dx * self.facing < 0:
                    continue
                if self.world.get_block(cx + dx, cy + dy) == WILDFLOWER_DISPLAY_BLOCK:
                    return (cx + dx, cy + dy)
        return None

    def get_nearby_pottery_display(self):
        """Return (bx, by) of a pottery display pedestal within 2 blocks of the player, or None."""
        from blocks import POTTERY_DISPLAY_BLOCK
        cx = int((self.x + PLAYER_W / 2) // BLOCK_SIZE)
        cy = int((self.y + PLAYER_H / 2) // BLOCK_SIZE)
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                if dx * self.facing < 0:
                    continue
                if self.world.get_block(cx + dx, cy + dy) == POTTERY_DISPLAY_BLOCK:
                    return (cx + dx, cy + dy)
        return None

    def get_nearby_elevator_stop(self):
        """Return (bx, by) of an elevator stop within 2 blocks of the player, or None."""
        cx = int((self.x + PLAYER_W / 2) // BLOCK_SIZE)
        cy = int((self.y + PLAYER_H / 2) // BLOCK_SIZE)
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                if self.world.get_block(cx + dx, cy + dy) == ELEVATOR_STOP_BLOCK:
                    return (cx + dx, cy + dy)
        return None

    def get_nearby_mine_track_stop(self):
        """Return (bx, by) of a track stop within 2 blocks of the player, or None."""
        cx = int((self.x + PLAYER_W / 2) // BLOCK_SIZE)
        cy = int((self.y + PLAYER_H / 2) // BLOCK_SIZE)
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                if self.world.get_block(cx + dx, cy + dy) == MINE_TRACK_STOP_BLOCK:
                    return (cx + dx, cy + dy)
        return None

    def get_depth(self):
        block_y = int(self.y // BLOCK_SIZE)
        surface_y = self.world.surface_y_at(int(self.x // BLOCK_SIZE))
        return max(0, block_y - surface_y)

    @property
    def effective_pick_power(self):
        item_id = self.hotbar[self.selected_slot]
        tool_power = ITEMS.get(item_id, {}).get("pick_power", 0) if item_id else 0
        bonus = 1 if "strength" in self.active_buffs else 0
        base = max(self.pick_power, tool_power) + bonus
        # Focus buffs (coffee, herb potions, woven hat) multiply effective power
        mult = 1.0
        if "focus" in self.active_buffs:
            mult *= 1.20
        if "focus" in self.herb_buffs:
            mult *= 1.20
        if "mastery" in self.herb_buffs:
            mult *= 1.40
        if "keenness" in self.cheese_buffs:
            mult *= 1.15
        if "vitality" in self.salt_buffs:
            mult *= 1.15
        mult += self.get_textile_bonus("focus")
        vigor_bonus = 1 if "vigor" in self.cheese_buffs else 0
        return base * mult + vigor_bonus

    @property
    def effective_axe_power(self):
        item_id = self.hotbar[self.selected_slot]
        tool_power = ITEMS.get(item_id, {}).get("axe_power", 0) if item_id else 0
        return max(self.pick_power, tool_power)

    def _mining_power_for(self, block_id):
        if block_id in ALL_LOGS or block_id in ALL_LEAVES:
            return max(self.effective_pick_power, self.effective_axe_power)
        return self.effective_pick_power

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), PLAYER_W, PLAYER_H)

    @property
    def center_px(self):
        return (int(self.x + PLAYER_W // 2), int(self.y + PLAYER_H // 2))
