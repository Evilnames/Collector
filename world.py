import math
import random
import time as _time
from math import cos, sin, pi
from blocks import *  # noqa: F401,F403
from constants import CHUNK_W, CHUNK_LOAD_RADIUS, WORLD_MAX_X, WORLD_H, SURFACE_Y, BLOCK_SIZE, PLAYER_W, PLAYER_H
from biomes import BIOMES, BIOME_ORE_MULTIPLIERS, BIODOME_TYPES, BIODOME_TERRAIN_MODS
import soil as _soil


# Young → mature block mapping for crop maturation. Lifted out of the crop
# update loop so it isn't rebuilt every tick.
DAY_DURATION   = 480.0   # 8 minutes of daylight
NIGHT_DURATION = 300.0   # 5 minutes of night
CYCLE_DURATION = DAY_DURATION + NIGHT_DURATION

_CROP_MATURE_MAP = {
    STRAWBERRY_CROP_YOUNG:   STRAWBERRY_CROP_MATURE,
    WHEAT_CROP_YOUNG:        WHEAT_CROP_MATURE,
    CARROT_CROP_YOUNG:       CARROT_CROP_MATURE,
    TOMATO_CROP_YOUNG:       TOMATO_CROP_MATURE,
    CORN_CROP_YOUNG:         CORN_CROP_MATURE,
    PUMPKIN_CROP_YOUNG:      PUMPKIN_CROP_MATURE,
    APPLE_CROP_YOUNG:        APPLE_CROP_MATURE,
    RICE_CROP_YOUNG:         RICE_CROP_MATURE,
    GINGER_CROP_YOUNG:       GINGER_CROP_MATURE,
    BOK_CHOY_CROP_YOUNG:     BOK_CHOY_CROP_MATURE,
    GARLIC_CROP_YOUNG:       GARLIC_CROP_MATURE,
    SCALLION_CROP_YOUNG:     SCALLION_CROP_MATURE,
    CHILI_CROP_YOUNG:        CHILI_CROP_MATURE,
    PEPPER_CROP_YOUNG:       PEPPER_CROP_MATURE,
    ONION_CROP_YOUNG:        ONION_CROP_MATURE,
    POTATO_CROP_YOUNG:       POTATO_CROP_MATURE,
    EGGPLANT_CROP_YOUNG:     EGGPLANT_CROP_MATURE,
    CABBAGE_CROP_YOUNG:      CABBAGE_CROP_MATURE,
    BEET_CROP_YOUNG:         BEET_CROP_MATURE,
    TURNIP_CROP_YOUNG:       TURNIP_CROP_MATURE,
    LEEK_CROP_YOUNG:         LEEK_CROP_MATURE,
    ZUCCHINI_CROP_YOUNG:     ZUCCHINI_CROP_MATURE,
    SWEET_POTATO_CROP_YOUNG: SWEET_POTATO_CROP_MATURE,
    WATERMELON_CROP_YOUNG:   WATERMELON_CROP_MATURE,
    RADISH_CROP_YOUNG:       RADISH_CROP_MATURE,
    PEA_CROP_YOUNG:          PEA_CROP_MATURE,
    CELERY_CROP_YOUNG:       CELERY_CROP_MATURE,
    BROCCOLI_CROP_YOUNG:     BROCCOLI_CROP_MATURE,
    CACTUS_YOUNG:            CACTUS_MATURE,
    SAGUARO_YOUNG:           SAGUARO_MATURE,
    BARREL_CACTUS_YOUNG:     BARREL_CACTUS_MATURE,
    OCOTILLO_YOUNG:          OCOTILLO_MATURE,
    PRICKLY_PEAR_YOUNG:      PRICKLY_PEAR_MATURE,
    CHOLLA_YOUNG:            CHOLLA_MATURE,
    PALO_VERDE_YOUNG:        PALO_VERDE_MATURE,
    DATE_PALM_CROP_YOUNG:    DATE_PALM_CROP_MATURE,
    AGAVE_CROP_YOUNG:        AGAVE_CROP_MATURE,
    COFFEE_CROP_YOUNG:       COFFEE_CROP_MATURE,
    GRAPEVINE_CROP_YOUNG:    GRAPEVINE_CROP_MATURE,
    FLAX_CROP_YOUNG:         FLAX_CROP_MATURE,
    COTTON_CROP_YOUNG:       COTTON_CROP_MATURE,
    TARO_CROP_YOUNG:         TARO_CROP_MATURE,
    BREADFRUIT_CROP_YOUNG:   BREADFRUIT_CROP_MATURE,
    COCONUT_CROP_YOUNG:      COCONUT_CROP_MATURE,
    CHAMOMILE_CROP_YOUNG:    CHAMOMILE_CROP_MATURE,
    LAVENDER_CROP_YOUNG:     LAVENDER_CROP_MATURE,
    MINT_CROP_YOUNG:         MINT_CROP_MATURE,
    ROSEMARY_CROP_YOUNG:     ROSEMARY_CROP_MATURE,
    THYME_CROP_YOUNG:        THYME_CROP_MATURE,
    SAGE_CROP_YOUNG:         SAGE_CROP_MATURE,
    BASIL_CROP_YOUNG:        BASIL_CROP_MATURE,
    OREGANO_CROP_YOUNG:      OREGANO_CROP_MATURE,
    GRAIN_CROP_YOUNG:        GRAIN_CROP_MATURE,
    TEA_CROP_YOUNG:          TEA_CROP_MATURE,
    DILL_CROP_YOUNG:         DILL_CROP_MATURE,
    FENNEL_CROP_YOUNG:       FENNEL_CROP_MATURE,
    TARRAGON_CROP_YOUNG:     TARRAGON_CROP_MATURE,
    LEMON_BALM_CROP_YOUNG:   LEMON_BALM_CROP_MATURE,
    ECHINACEA_CROP_YOUNG:    ECHINACEA_CROP_MATURE,
    VALERIAN_CROP_YOUNG:     VALERIAN_CROP_MATURE,
    ST_JOHNS_WORT_CROP_YOUNG:ST_JOHNS_WORT_CROP_MATURE,
    YARROW_CROP_YOUNG:       YARROW_CROP_MATURE,
    BERGAMOT_CROP_YOUNG:     BERGAMOT_CROP_MATURE,
    WORMWOOD_CROP_YOUNG:     WORMWOOD_CROP_MATURE,
    RUE_CROP_YOUNG:          RUE_CROP_MATURE,
    LEMON_VERBENA_CROP_YOUNG:LEMON_VERBENA_CROP_MATURE,
    HYSSOP_CROP_YOUNG:       HYSSOP_CROP_MATURE,
    CATNIP_CROP_YOUNG:       CATNIP_CROP_MATURE,
    WOOD_SORREL_CROP_YOUNG:  WOOD_SORREL_CROP_MATURE,
    MARJORAM_CROP_YOUNG:     MARJORAM_CROP_MATURE,
    SAVORY_CROP_YOUNG:       SAVORY_CROP_MATURE,
    ANGELICA_CROP_YOUNG:     ANGELICA_CROP_MATURE,
    BORAGE_CROP_YOUNG:       BORAGE_CROP_MATURE,
    COMFREY_CROP_YOUNG:      COMFREY_CROP_MATURE,
    MUGWORT_CROP_YOUNG:      MUGWORT_CROP_MATURE,
    CHICKPEA_CROP_YOUNG:     CHICKPEA_CROP_MATURE,
    LENTIL_CROP_YOUNG:       LENTIL_CROP_MATURE,
    SESAME_CROP_YOUNG:       SESAME_CROP_MATURE,
    POMEGRANATE_TREE_YOUNG:  POMEGRANATE_TREE_MATURE,
    OLIVE_TREE_YOUNG:        OLIVE_TREE_MATURE,
    SAFFRON_CROP_YOUNG:      SAFFRON_CROP_MATURE,
    STRAWBERRY_CROP_YOUNG_P: STRAWBERRY_CROP_MATURE_P,
    TOMATO_CROP_YOUNG_P:     TOMATO_CROP_MATURE_P,
    WATERMELON_CROP_YOUNG_P: WATERMELON_CROP_MATURE_P,
    CORN_CROP_YOUNG_P:       CORN_CROP_MATURE_P,
    RICE_CROP_YOUNG_P:       RICE_CROP_MATURE_P,
}


_OCEAN_SPREAD    = 2     # zones on each side of an ocean seed that expand to ocean
_OCEAN_SEED_PROB = 0.025 # probability a zone seeds an ocean cluster
_ISLAND_PROB     = 0.22  # probability an ocean zone becomes a pacific_island
_COASTAL_BUFFER  = 1     # zones just outside ocean spread that become coastal (beach transition)


class World:
    def __init__(self, seed=42, preloaded=None, save_mgr=None, player_x=0.0):
        self.seed = seed
        self.height = WORLD_H
        self._save_mgr = save_mgr
        self._chunks = {}           # chunk_x -> [[block_id]*CHUNK_W]*WORLD_H
        self._dirty_chunks = set()
        self._bg_chunks = {}        # background layer: chunk_x -> [[block_id]*CHUNK_W]*WORLD_H
        self._dirty_bg_chunks = set()
        self._wire_chunks = {}      # chunk_x -> [[uint8]*CHUNK_W]*WORLD_H (0=empty 1=wire)
        self._dirty_wire_chunks = set()
        self.logic_state = {}       # (bx,by) -> {"facing": str, "latch_state": bool, "prev_input": bool}
        self.powered_wires = set()  # (bx,by) of currently-powered wire/gate tiles
        self.wire_mode = False      # True = wire layer visible
        self.entities = []
        self.arrows   = []
        self.automations = []
        self.farm_bots = []
        self.backhoes = []
        self.elevator_cars = []
        self.minecarts = []
        self.birds = []
        self.nests = []
        self.insects = []
        self.dropped_items = []
        self.chest_data = {}     # (bx, by) -> {item_id: count}
        self.banner_data = {}    # (bx, by) -> coat_of_arms dict
        self.light_traps = {}    # (bx, by) -> {"accumulated": [species_id, ...]}
        self.garden_data = {}    # (bx, by) -> [Wildflower, ...]
        self.wildflower_display_data = {}  # (bx, by) -> Wildflower | None
        self._surface_height_cache = {}
        self._water_level   = {}   # (x,y) -> int 1-8; 8 = world-gen source block
        self._ore_richness  = {}   # (bx,by) -> int 1-3; richer veins drop more ore
        # Soil state (Phases 1-2): parallel dicts keyed by (x,y)
        self._soil_moisture  = {}  # tilled tile -> int 0..MAX_MOISTURE
        self._soil_fertility = {}  # tilled tile -> int 0..MAX_FERTILITY
        self._crop_progress  = {}  # young crop tile -> int 0..GROWTH_PROGRESS_MAX
        self._crop_care_sum  = {}  # young crop tile -> (sum, count) running mean of care
        self._soil_fallow    = {}  # tilled-but-empty tile -> ticks without a crop
        # Rain state (Phase 2)
        self._rain_active   = False
        self._rain_timer    = 0.0
        self._rain_duration = 0.0
        self._rain_gap      = 0.0  # set after soil_rng is initialized below
        # Compost bins (Phase 2): (bx,by) -> {"input": {}, "progress": float, "output": int}
        self.compost_bin_data = {}
        # Chicken coops: (bx,by) -> {"eggs": int, "progress": float}
        self.chicken_coop_data = {}
        # Trade blocks: (bx,by) -> {horse_uid, has_cart, linked_town_id, inventory, threshold, state, ticks_left}
        self.trade_block_data = {}
        # Sculpture data: root pos -> Sculpture obj; body pos -> {"root": (bx, root_y)}
        self.sculpture_data = {}
        # Tapestry data: root pos -> Tapestry obj; body pos -> {"root": (bx, root_y)}
        self.tapestry_data = {}
        # Pottery display pedestals: (bx, by) -> PotteryPiece
        self.pottery_display_data = {}
        # Research-derived world flags (set by research.apply_bonuses)
        self.moisture_decay_chance = _soil.MOISTURE_DECAY_CHANCE
        self.max_fertility         = _soil.MAX_FERTILITY
        self._lake_cells  = []
        # Pre-compute deterministic terrain noise once
        _rng = random.Random(self.seed)
        self._surf_octaves = [(0.015, 6.0), (0.04, 3.0), (0.10, 1.5), (0.22, 0.6)]
        self._surf_phases  = [_rng.uniform(0, 6.28) for _ in self._surf_octaves]
        self._surf_water_cache = {}
        # Water simulation
        self._water_timer = 0.0
        self._water_interval = 0.12
        self._pending_water = set()
        # Sapling growth
        self._sapling_timer = 0.0
        self._sapling_interval = 30.0
        self._sapling_rng = random.Random(seed + 99999)
        self.pending_saplings = set()
        # Leaf decay
        self._leaves_timer = 0.0
        self._leaves_interval = 5.0
        self._leaves_rng = random.Random(seed + 54321)
        # Crop growth
        self._crop_timer    = 0.0
        self._crop_interval = 20.0
        self._crop_rng      = random.Random(seed + 11111)
        self.pending_crops  = set()
        self._grow_lamps    = set()   # (x, y) of all placed GROW_LAMP bg blocks
        # Fruit tree regrowth — tracks leaf positions that may regrow a fruit cluster
        self._fruit_timer    = 0.0
        self._fruit_interval = 30.0
        self._fruit_rng      = random.Random(seed + 33333)
        self.pending_fruit_leaves = set()
        if preloaded:
            self._load_from(preloaded, player_x)
        else:
            for cx in range(-CHUNK_LOAD_RADIUS, CHUNK_LOAD_RADIUS + 1):
                self.load_chunk(cx)
            self._spawn_animals()
            self._spawn_huntable_animals()
            self._spawn_capybaras()
        # Soil moisture tick (independent of crop growth — faster so care feels responsive)
        self._soil_timer    = 0.0
        self._soil_interval = _soil.SOIL_TICK_SECS
        self._soil_rng      = random.Random(seed + 22222)
        self._rain_gap      = self._soil_rng.uniform(_soil.RAIN_MIN_GAP_SECS, _soil.RAIN_MAX_GAP_SECS)
        # Day/night cycle
        self.time_of_day = 0.0   # seconds, 0 = start of day, wraps at CYCLE_DURATION
        self.day_count = 0
        self.pending_arena_open = None  # set by landmark effect; consumed by main loop
        self.town_centers: list[int] = []  # city_bx values from generate_cities
        self.city_slot_xs: list[int] = []  # un-jittered slot centers, parallel to town_centers
        self.city_zones:   list     = []   # (lo, hi) block ranges occupied by cities
        if not preloaded:
            from cities import generate_cities
            generate_cities(self, self.seed)
            from outposts import generate_outpost_for_chunk
            for cx in list(self._chunks.keys()):
                generate_outpost_for_chunk(self, self.seed, cx)
        from towns import init_towns
        init_towns(self)
        if not preloaded:
            import npc_identity
            npc_identity.assign_ruling_dynasties(self, self.seed)
        from outposts import init_outposts
        init_outposts(self)
        from player_cities import init_player_cities
        init_player_cities(self)
        self._spawn_birds()
        self._spawn_insects()

    # ------------------------------------------------------------------
    # Backward-compat properties
    # ------------------------------------------------------------------

    @property
    def width(self):
        """Loaded world span in blocks — used for minimap and backward compat."""
        if not self._chunks:
            return CHUNK_W
        return (max(self._chunks) - min(self._chunks) + 1) * CHUNK_W

    @property
    def chunk_min_x(self):
        return min(self._chunks, default=0) * CHUNK_W

    # ------------------------------------------------------------------
    # Deterministic terrain queries (replace fixed arrays)
    # ------------------------------------------------------------------

    @staticmethod
    def _zone_seed(world_seed, z, purpose):
        return (world_seed * 1000003 + z * 31337 + purpose) & 0x7FFFFFFF

    def _zone_biodome(self, z: int) -> str:
        """Effective biodome for ecological zone z, including ocean-cluster spreading."""
        for z_check in range(z - _OCEAN_SPREAD, z + _OCEAN_SPREAD + 1):
            seed_rng = random.Random(self._zone_seed(self.seed, z_check, 14))
            if seed_rng.random() < _OCEAN_SEED_PROB:
                island_rng = random.Random(self._zone_seed(self.seed, z, 13))
                if island_rng.random() < _ISLAND_PROB:
                    return "pacific_island"
                return "ocean"
        # Coastal buffer — one zone ring outside the ocean spread becomes beach/transition
        for dz in range(1, _COASTAL_BUFFER + 1):
            for z_outer in (z - (_OCEAN_SPREAD + dz), z + (_OCEAN_SPREAD + dz)):
                seed_rng = random.Random(self._zone_seed(self.seed, z_outer, 14))
                if seed_rng.random() < _OCEAN_SEED_PROB:
                    return "coastal"
        brng = random.Random(self._zone_seed(self.seed, z, 3))
        return brng.choice(BIODOME_TYPES)

    def _biodome_terrain_mod(self, x: int):
        """Return (height_bias, amplitude_scale) blended from the two nearest biodome zones."""
        zone = x // 200
        data = []
        for z in range(zone - 1, zone + 2):
            rng_c = random.Random(self._zone_seed(self.seed, z, 2))
            cx = z * 200 + rng_c.randint(-40, 40)
            biodome = self._zone_biodome(z)
            bias, scale = BIODOME_TERRAIN_MODS.get(biodome, (0, 1.0))
            data.append((abs(x - cx), bias, scale))
        data.sort()
        d0, b0, s0 = data[0]
        d1, b1, s1 = data[1]
        if d0 == 0:
            return b0, s0
        w0, w1 = 1.0 / d0, 1.0 / d1
        total = w0 + w1
        return (w0 * b0 + w1 * b1) / total, (w0 * s0 + w1 * s1) / total

    def surface_height(self, x: int) -> int:
        cached = self._surface_height_cache.get(x)
        if cached is not None:
            return cached
        bias, scale = self._biodome_terrain_mod(x)
        h = SURFACE_Y + bias
        for (freq, amp), phase in zip(self._surf_octaves, self._surf_phases):
            h += amp * scale * math.sin(x * freq + phase)
        result = max(30, round(h))
        self._surface_height_cache[x] = result
        return result

    def biome_at(self, x: int) -> str:
        zone = x // 150
        nearest_biome, nearest_dist = BIOMES[0], float('inf')
        for z in (zone - 1, zone, zone + 1):
            rng = random.Random(self._zone_seed(self.seed, z, 0))
            cx = z * 150 + rng.randint(-25, 25)
            dist = abs(x - cx)
            if dist < nearest_dist:
                nearest_dist = dist
                brng = random.Random(self._zone_seed(self.seed, z, 1))
                nearest_biome = brng.choice(BIOMES)
        return nearest_biome

    def biodome_at(self, x: int) -> str:
        zone = x // 200
        nearest, nearest_dist = BIODOME_TYPES[0], float('inf')
        for z in (zone - 1, zone, zone + 1):
            rng = random.Random(self._zone_seed(self.seed, z, 2))
            cxz = z * 200 + rng.randint(-40, 40)
            dist = abs(x - cxz)
            if dist < nearest_dist:
                nearest_dist = dist
                nearest = self._zone_biodome(z)
        return nearest

    def _biodome_owning_zone(self, x: int) -> int:
        zone = x // 200
        owner, best = zone, float('inf')
        for z in (zone - 1, zone, zone + 1):
            rng = random.Random(self._zone_seed(self.seed, z, 2))
            cxz = z * 200 + rng.randint(-40, 40)
            dist = abs(x - cxz)
            if dist < best:
                best = dist
                owner = z
        return owner

    def biodome_tree_density(self, x: int) -> float:
        """Per-biodome-instance spacing multiplier: <1 = dense forest, >1 = sparse."""
        zone = self._biodome_owning_zone(x)
        drng = random.Random(self._zone_seed(self.seed, zone, 11))
        roll = drng.random()
        if roll < 0.15:
            return drng.uniform(0.35, 0.55)   # dense forest
        if roll < 0.55:
            return drng.uniform(0.75, 1.15)   # normal
        if roll < 0.85:
            return drng.uniform(1.4, 2.0)     # sparse
        return drng.uniform(2.5, 3.5)         # very sparse

    def get_biome(self, bx: int) -> str:
        return self.biome_at(bx)

    def get_biodome(self, bx: int) -> str:
        return self.biodome_at(bx)

    def surface_y_at(self, x: int) -> int:
        return self.surface_height(x)

    # ------------------------------------------------------------------
    # Chunk infrastructure
    # ------------------------------------------------------------------

    def _scan_chunk_for_crops(self, cx: int):
        """Rebuild pending_crops, pending_saplings, and _grow_lamps for a loaded chunk."""
        chunk = self._chunks.get(cx)
        if chunk is None:
            return
        x_base = cx * CHUNK_W
        for y in range(WORLD_H):
            row = chunk[y]
            for lx in range(CHUNK_W):
                bid = row[lx]
                if bid in YOUNG_CROP_BLOCKS:
                    self.pending_crops.add((x_base + lx, y))
                elif bid == SAPLING or bid in ALL_FRUIT_SAPLINGS:
                    self.pending_saplings.add((x_base + lx, y))
                elif bid in LEAF_FRUIT_CLUSTER_MAP:
                    self.pending_fruit_leaves.add((x_base + lx, y))
        bg = self._bg_chunks.get(cx)
        if bg is not None:
            for y in range(WORLD_H):
                row = bg[y]
                for lx in range(CHUNK_W):
                    if row[lx] == GROW_LAMP:
                        self._grow_lamps.add((x_base + lx, y))

    def load_chunk(self, cx: int):
        """Load chunk from DB, or generate fresh if unseen."""
        if cx in self._chunks:
            return
        data = self._save_mgr.load_chunk(cx) if self._save_mgr else None
        self._chunks[cx] = data if data is not None else [[AIR] * CHUNK_W for _ in range(WORLD_H)]
        if data is None:
            self._fill_chunk(cx)
        else:
            self._scan_chunk_for_crops(cx)
        bg_data = self._save_mgr.load_bg_chunk(cx) if self._save_mgr else None
        if bg_data is not None:
            self._bg_chunks[cx] = bg_data
        wire_data = self._save_mgr.load_wire_chunk(cx) if self._save_mgr else None
        if wire_data is not None:
            self._wire_chunks[cx] = wire_data

    def unload_chunk(self, cx: int):
        """Save dirty chunk to DB and evict from memory."""
        if cx not in self._chunks:
            return
        if self._save_mgr and cx in self._dirty_chunks:
            self._save_mgr.save_chunk(cx, self._chunks[cx])
            self._dirty_chunks.discard(cx)
        if self._save_mgr and cx in self._dirty_bg_chunks and cx in self._bg_chunks:
            self._save_mgr.save_bg_chunk(cx, self._bg_chunks[cx])
            self._dirty_bg_chunks.discard(cx)
        del self._chunks[cx]
        self._bg_chunks.pop(cx, None)

    def update_loaded_chunks(self, player_x_pixels: float):
        """Call each frame to stream chunks in and out around the player."""
        player_cx = int(player_x_pixels // BLOCK_SIZE) // CHUNK_W
        desired = set(range(player_cx - CHUNK_LOAD_RADIUS, player_cx + CHUNK_LOAD_RADIUS + 1))
        loaded = set(self._chunks.keys())

        to_unload = loaded - desired
        to_load = desired - loaded
        if not to_unload and not to_load:
            return

        # Save all dirty evicted chunks in one transaction
        if to_unload and self._save_mgr:
            dirty = {cx: self._chunks[cx] for cx in to_unload if cx in self._dirty_chunks}
            if dirty:
                self._save_mgr.save_chunks_batch(dirty)
                self._dirty_chunks -= set(dirty.keys())
            dirty_bg = {cx: self._bg_chunks[cx] for cx in to_unload
                        if cx in self._dirty_bg_chunks and cx in self._bg_chunks}
            if dirty_bg:
                self._save_mgr.save_bg_chunks_batch(dirty_bg)
                self._dirty_bg_chunks -= set(dirty_bg.keys())
        if to_unload:
            unload_ranges = [(cx * CHUNK_W * BLOCK_SIZE, (cx + 1) * CHUNK_W * BLOCK_SIZE)
                             for cx in to_unload]
            self.insects = [i for i in self.insects
                            if not any(x0 <= i.x < x1 for x0, x1 in unload_ranges)]
            unload_x_ranges = [(cx * CHUNK_W, (cx + 1) * CHUNK_W) for cx in to_unload]
            self._grow_lamps = {(lx, ly) for lx, ly in self._grow_lamps
                                if not any(x0 <= lx < x1 for x0, x1 in unload_x_ranges)}
        for cx in to_unload:
            del self._chunks[cx]
            self._bg_chunks.pop(cx, None)

        # Load all needed chunks from DB in one query, generate any that are new
        if to_load:
            from cities import generate_city_for_chunk
            db_data = self._save_mgr.load_chunks_batch(to_load) if self._save_mgr else {}
            bg_db_data = self._save_mgr.load_bg_chunks_batch(to_load) if self._save_mgr else {}
            wire_db_data = self._save_mgr.load_wire_chunks_batch(to_load) if self._save_mgr else {}
            newly_generated = []
            for cx in to_load:
                if cx in db_data:
                    self._chunks[cx] = db_data[cx]
                    self._scan_chunk_for_crops(cx)
                else:
                    self._chunks[cx] = [[AIR] * CHUNK_W for _ in range(WORLD_H)]
                    self._fill_chunk(cx)
                    newly_generated.append(cx)
                if cx in bg_db_data:
                    self._bg_chunks[cx] = bg_db_data[cx]
                if cx in wire_db_data:
                    self._wire_chunks[cx] = wire_db_data[cx]
                self._spawn_insects_for_chunk(cx)
                self._spawn_garden_insects_in_chunk(cx)
            for cx in newly_generated:
                self._spawn_animals_for_chunk(cx)
                self._spawn_birds_for_chunk(cx)
                generate_city_for_chunk(self, self.seed, cx)
                from outposts import generate_outpost_for_chunk
                generate_outpost_for_chunk(self, self.seed, cx)

    def _chunk_get(self, x: int, y: int) -> int:
        """Raw chunk read — no side effects. Returns BEDROCK for unloaded/OOB."""
        if y < 0 or y >= WORLD_H:
            return BEDROCK
        chunk = self._chunks.get(x // CHUNK_W)
        return chunk[y][x % CHUNK_W] if chunk is not None else BEDROCK

    def _chunk_set(self, x: int, y: int, bid: int):
        """Raw chunk write — no side effects. Silently skips unloaded chunks."""
        if y < 0 or y >= WORLD_H:
            return
        cx = x // CHUNK_W
        chunk = self._chunks.get(cx)
        if chunk is not None:
            chunk[y][x % CHUNK_W] = bid
            self._dirty_chunks.add(cx)

    def _load_from(self, data, player_x: float = 0.0):
        self._water_level    = data.get("water_level", {})
        self._soil_moisture  = data.get("soil_moisture", {})
        self._soil_fertility = data.get("soil_fertility", {})
        self._crop_progress  = data.get("crop_progress", {})
        self._crop_care_sum  = data.get("crop_care_sum", {})
        raw_bins = data.get("compost_bin_data", {})
        self.compost_bin_data = {
            tuple(int(v) for v in k.split(",")): bin_d
            for k, bin_d in raw_bins.items()
        }
        raw_coops = data.get("chicken_coop_data", {})
        self.chicken_coop_data = {
            tuple(int(v) for v in k.split(",")): coop_d
            for k, coop_d in raw_coops.items()
        }
        raw_chests = data.get("chest_data", {})
        self.chest_data = {
            tuple(int(v) for v in k.split(",")): inv
            for k, inv in raw_chests.items()
        }
        raw_banners = data.get("banner_data", {})
        self.banner_data = {
            tuple(int(v) for v in k.split(",")): coa
            for k, coa in raw_banners.items()
        }
        self.garden_data = data.get("garden_data", {})
        self.wildflower_display_data = data.get("wildflower_display_data", {})
        # sculpture_positions loaded here as uid strings; resolved in main.py
        # after player.apply_save (which loads the Sculpture objects)
        self._pending_sculpture_positions = data.get("sculpture_positions", {})
        self._pending_tapestry_positions  = data.get("tapestry_positions", {})
        self.pottery_display_data = data.get("pottery_display_data", {})
        self._pending_unplaced_vase_uids  = data.get("unplaced_vase_uids", [])
        self.day_count = data.get("day_count", 0)
        self.logic_state = data.get("logic_state", {})
        raw_trade = data.get("trade_block_data", {})
        self.trade_block_data = {
            tuple(int(v) for v in k.split(",")): td
            for k, td in raw_trade.items()
        }
        # Load chunks around the player's saved position
        player_cx = int(player_x // BLOCK_SIZE) // CHUNK_W
        for cx in range(player_cx - CHUNK_LOAD_RADIUS, player_cx + CHUNK_LOAD_RADIUS + 1):
            self.load_chunk(cx)

        from automations import Automation, FarmBot, Backhoe
        for a_data in data["automations"]:
            a = Automation(a_data["x"], a_data["y"], a_data["auto_type"], a_data["direction"])
            a.fuel = a_data["fuel"]
            a.stored = a_data["stored"]
            a._state = a_data["state"]
            a._halt_reason = a_data["halt_reason"]
            if a._halt_reason == "no_supports":
                a._halt_reason = ""
                a._state = "moving"
            self.automations.append(a)
        for fb_data in data.get("farm_bots", []):
            fb = FarmBot(fb_data["x"], fb_data["y"], fb_data["bot_type"],
                         fuel=fb_data["fuel"], seeds=fb_data["seeds"],
                         stored=fb_data["stored"], state=fb_data["state"],
                         water_reservoir=fb_data.get("water_reservoir", 0.0),
                         compost_slot=fb_data.get("compost_slot", 0))
            self.farm_bots.append(fb)
        for bh_data in data.get("backhoes", []):
            self.backhoes.append(Backhoe.from_dict(bh_data))
        from elevators import ElevatorCar
        for car_data in data.get("elevator_cars", []):
            self.elevator_cars.append(ElevatorCar.from_dict(car_data))
        from minecarts import Minecart
        for cart_data in data.get("minecarts", []):
            self.minecarts.append(Minecart.from_dict(cart_data))

        from animals import Sheep, Cow, Chicken, Goat, SnowLeopard, MountainLion, Tiger
        from horses import Horse
        from dogs import Dog
        _CLASS_MAP = {"Sheep": Sheep, "Cow": Cow, "Chicken": Chicken, "Goat": Goat,
                      "SnowLeopard": SnowLeopard, "MountainLion": MountainLion,
                      "Tiger": Tiger, "Horse": Horse, "Dog": Dog}
        for e_data in data["entities"]:
            cls = _CLASS_MAP.get(e_data["entity_type"])
            if cls is None:
                continue
            entity = cls(e_data["x"], e_data["y"], self)
            entity.facing = e_data["facing"]
            extra = e_data.get("extra", {})
            if isinstance(entity, Sheep):
                if "has_wool" in extra:
                    entity.has_wool = extra["has_wool"]
                if "has_milk" in extra:
                    entity.has_milk = extra["has_milk"]
            elif isinstance(entity, Cow) and "has_milk" in extra:
                entity.has_milk = extra["has_milk"]
            elif isinstance(entity, Goat) and "has_milk" in extra:
                entity.has_milk = extra["has_milk"]
            elif isinstance(entity, Chicken) and "has_egg" in extra:
                entity.has_egg = extra["has_egg"]
            elif isinstance(entity, Horse):
                entity.stamina   = extra.get("stamina", 100.0)
                entity._broken   = extra.get("broken", False)
            elif isinstance(entity, Dog):
                entity.stay_mode = extra.get("stay_mode", False)
            # Genetics / new state fields (fallback defaults keep old saves working)
            if "uid" in extra:
                entity.uid = extra["uid"]
            entity.parent_a_uid = extra.get("parent_a_uid", None)
            entity.parent_b_uid = extra.get("parent_b_uid", None)
            if "traits" in extra:
                raw = extra["traits"]
                entity.traits = {
                    "color_shift":  tuple(raw.get("color_shift", [0, 0, 0])),
                    "size":         raw.get("size", 1.0),
                    "productivity": raw.get("productivity", 1.0),
                    "mutation":     raw.get("mutation", None),
                }
                if isinstance(entity, Horse):
                    entity.traits["speed_rating"]      = raw.get("speed_rating", 1.0)
                    entity.traits["stamina_max"]        = raw.get("stamina_max", 1.0)
                    entity.traits["temperament"]        = raw.get("temperament", "spirited")
                    entity.traits["coat_color"]         = tuple(raw.get("coat_color", [160, 115, 65]))
                    entity.traits["horseshoe_applied"]  = raw.get("horseshoe_applied", False)
                    entity.traits["endurance"]          = raw.get("endurance", 1.0)
                    entity.traits["gait"]               = raw.get("gait", 1.0)
                    entity.traits["coat_pattern"]  = raw.get("coat_pattern", "solid")
                    entity.traits["leg_marking"]   = raw.get("leg_marking", "none")
                    entity.traits["mane_color"]    = raw.get("mane_color", "match")
                    entity.traits["face_marking"]  = raw.get("face_marking", "none")
                elif isinstance(entity, Sheep):
                    entity.traits["wool_color"] = raw.get("wool_color", "white")
                    entity.traits["fleece"]     = raw.get("fleece", raw.get("productivity", 1.0))
                    entity.traits["birth"]      = raw.get("birth", "single")
                elif isinstance(entity, Cow):
                    entity.traits["milk_richness"] = raw.get("milk_richness", raw.get("productivity", 1.0))
                    entity.traits["hide"]          = raw.get("hide", "solid")
                elif isinstance(entity, Goat):
                    entity.traits["milk_richness"] = raw.get("milk_richness", raw.get("productivity", 1.0))
                    entity.traits["coat_color"]    = raw.get("coat_color", "tan")
                elif isinstance(entity, Chicken):
                    entity.traits["lay_rate"] = raw.get("lay_rate", raw.get("productivity", 1.0))
                    entity.traits["plumage"]  = raw.get("plumage", "white")
                elif isinstance(entity, Dog):
                    entity.traits["breed"]         = raw.get("breed", "Mixed")
                    entity.traits["generation"]    = raw.get("generation", 1)
                    entity.traits["coat_color"]    = tuple(raw.get("coat_color", [160, 100, 50]))
                    entity.traits["coat_pattern"]  = raw.get("coat_pattern", "solid")
                    entity.traits["coat_length"]   = raw.get("coat_length", "short")
                    entity.traits["coat_type"]     = raw.get("coat_type", "smooth")
                    entity.traits["ear_type"]      = raw.get("ear_type", "floppy")
                    entity.traits["tail_type"]     = raw.get("tail_type", "long")
                    entity.traits["eye_color"]     = raw.get("eye_color", "brown")
                    entity.traits["size_class"]    = raw.get("size_class", "medium")
                    entity.traits["collar_applied"]= raw.get("collar_applied", False)
                    entity.traits["dog_name"]      = raw.get("dog_name")
                    for tk in ("speed","endurance","agility","strength","nose","alertness",
                               "loyalty","playfulness","stubbornness","prey_drive"):
                        entity.traits[tk] = raw.get(tk, 1.0)
                    for ability in ("tracking","herding","guard","retrieve"):
                        entity.traits[f"has_{ability}"] = raw.get(f"has_{ability}", False)
                    entity.traits["base_color"]      = raw.get("base_color", "yellow")
                    entity.traits["dilute_expressed"]= raw.get("dilute_expressed", False)
                    entity.traits["dilute_carrier"]  = raw.get("dilute_carrier", False)
                    entity.traits["white_spotting"]  = raw.get("white_spotting", "solid")
            entity.no_breed        = extra.get("no_breed", False)
            entity.health          = extra.get("health", 3)
            entity.dead            = extra.get("dead", False)
            entity._breed_cooldown = extra.get("_breed_cooldown", 60.0)
            entity.tamed           = extra.get("tamed", False)
            entity.tame_progress   = extra.get("tame_progress", 0)
            # Restore genotype; synthesize from traits for pre-genetics saves
            raw_geno = extra.get("genotype")
            if raw_geno:
                entity.genotype = {k: list(v) for k, v in raw_geno.items()}
                entity._apply_genotype_to_traits()
            else:
                entity._synthesize_genotype_from_traits()
            self.entities.append(entity)

        # Reconstruct saved NPCs (all types except LeaderNPC/LandmarkNPC/RoyalSpouseNPC/RoyalChildNPC,
        # which are handled by _respawn_leader_npcs in init_towns).
        import cities as _cities
        import random as _rnd
        _NPC_NO_RNG = {
            "FarmerNPC", "VillagerNPC", "ChildNPC", "GuardNPC", "ElderNPC",
            "BeggarNPC", "NobleNPC", "PilgrimNPC", "DrunkardNPC",
            "DoctorNPC", "MusicianNPC", "TownCrierNPC",
        }
        _dummy_rng = _rnd.Random(0)
        for e_data in data["entities"]:
            etype = e_data["entity_type"]
            cls = getattr(_cities, etype, None)
            if cls is None or not (isinstance(cls, type) and issubclass(cls, _cities.NPC)):
                continue
            x, y  = e_data["x"], e_data["y"]
            extra  = e_data.get("extra", {})
            biodome = extra.get("biodome", "temperate")
            if etype in _NPC_NO_RNG:
                entity = cls(x, y, self, biodome=biodome)
            else:
                entity = cls(x, y, self, _dummy_rng, biodome=biodome)
            entity.facing      = e_data["facing"]
            entity.npc_uid     = extra.get("npc_uid")
            entity.town_id     = extra.get("town_id")
            entity.identity    = extra.get("identity")
            entity.preferences = extra.get("preferences")
            if "shop"          in extra: entity.shop          = [tuple(i) for i in extra["shop"]]
            if "quests"        in extra: entity.quests        = extra["quests"]
            if "trades"        in extra: entity.trades        = [tuple(t) for t in extra["trades"]]
            if "streak"        in extra: entity._streak       = extra["streak"]
            if "difficulty"    in extra: entity.difficulty    = extra["difficulty"]
            if "npc_horses"    in extra: entity._npc_horses   = extra["npc_horses"]
            if "rest_cost"     in extra: entity.rest_cost     = extra["rest_cost"]
            if "blessing_cost" in extra: entity.blessing_cost = extra["blessing_cost"]
            if "religion_name" in extra: entity.religion_name = extra["religion_name"]
            if "religion_style"in extra: entity.religion_style= extra["religion_style"]
            if "cuisine" in extra:
                entity.cuisine = extra["cuisine"]
                entity.menu    = _cities.CUISINE_MENUS.get(extra["cuisine"], entity.menu)
            self.entities.append(entity)

        from dropped_item import DroppedItem
        for d in data.get("dropped_items", []):
            self.dropped_items.append(
                DroppedItem(d["x"], d["y"], d["item_id"], d["count"], d["lifetime"])
            )

        # One-time retroactive dog seeding for saves that pre-date the dog system
        has_any_dogs = any(isinstance(e, Dog) for e in self.entities)
        if not has_any_dogs:
            for cx in sorted(self._chunks.keys()):
                self._spawn_dogs_for_chunk(cx)

    # ------------------------------------------------------------------
    # Chunk terrain generation
    # ------------------------------------------------------------------

    def _fill_chunk(self, cx: int):
        """Fill self._chunks[cx] with generated terrain (chunk must already be in dict)."""
        chunk = self._chunks[cx]
        ore_rng = random.Random(hash((self.seed, cx, 'ore')) & 0x7FFFFFFF)

        for lx in range(CHUNK_W):
            x = cx * CHUNK_W + lx
            sy = self.surface_height(x)
            biome = self.biome_at(x)
            biodome = self.biodome_at(x)
            rocky = biodome in ("alpine_mountain", "rocky_mountain", "tundra", "canyon")
            sandy = biodome in ("desert", "beach", "coastal", "ocean")
            submerged = sy > SURFACE_Y and biodome in ("ocean", "coastal")
            for y in range(WORLD_H):
                if y < sy:
                    if submerged and y >= SURFACE_Y:
                        chunk[y][lx] = WATER
                        self._water_level[(x, y)] = 8
                        self._lake_cells.append((y, x))
                    else:
                        chunk[y][lx] = AIR
                elif y == sy:
                    if biodome in ("alpine_mountain", "tundra"):
                        chunk[y][lx] = SNOW
                    elif sandy or submerged:
                        chunk[y][lx] = SAND
                    elif biodome == "canyon":
                        chunk[y][lx] = STONE
                    else:
                        chunk[y][lx] = GRASS
                elif y < sy + 6:
                    if rocky:
                        chunk[y][lx] = STONE
                    elif sandy:
                        chunk[y][lx] = SAND
                    else:
                        chunk[y][lx] = DIRT
                elif y >= WORLD_H - 1:
                    chunk[y][lx] = BEDROCK
                else:
                    chunk[y][lx] = self._pick_block(y - sy, ore_rng, biome, x, y)

        # Bedrock bottom
        for lx in range(CHUNK_W):
            chunk[WORLD_H - 1][lx] = BEDROCK

        # Zone barriers (2 rows thick at fixed depths)
        for y_abs, gate in [(SURFACE_Y + 40, GATE_MID), (SURFACE_Y + 100, GATE_DEEP),
                             (SURFACE_Y + 160, GATE_CORE)]:
            for dy in range(2):
                gy = y_abs + dy
                if 0 < gy < WORLD_H - 1:
                    for lx in range(CHUNK_W):
                        chunk[gy][lx] = gate

        self._gen_surface_water(cx, chunk)

        # Trees — _dispatch_grow uses set_block which silently skips unloaded chunks
        tree_rng = random.Random(hash((self.seed, cx, 'trees')) & 0x7FFFFFFF)
        lx = 2
        while lx < CHUNK_W - 2:
            x = cx * CHUNK_W + lx
            sy = self.surface_height(x)
            biodome = self.biodome_at(x)
            coast_submerged = sy > SURFACE_Y and biodome in ("ocean", "coastal")
            if chunk[sy][lx] != WATER and biodome != "ocean" and not coast_submerged:
                self._dispatch_grow(x, sy - 1, biodome, tree_rng)
            lo, hi = {
                "jungle":          (3, 6),  "fungal":         (3, 7),
                "boreal":          (4, 8),  "wetland":        (4, 8),
                "wasteland":       (9, 16), "savanna":        (7, 13),
                "alpine_mountain": (14, 22),"rocky_mountain": (12, 20),
                "rolling_hills":   (5, 11), "steep_hills":    (5, 10),
                "steppe":          (13, 22),"arid_steppe":    (18, 30),
                "desert":          (18, 32),"tundra":         (16, 28),
                "swamp":           (3, 7),  "beach":          (9, 16),
                "coastal":         (9, 16),
                "canyon":          (12, 22),
                "pacific_island":  ( 6, 12),
            }.get(biodome, (5, 10))
            factor = self.biodome_tree_density(x)
            lo = max(2, int(lo * factor))
            hi = max(lo + 1, int(hi * factor))
            lx += tree_rng.randint(lo, hi)

        # Bushes — biome-appropriate plants on grass surfaces
        _BIOME_BUSHES = {
            "temperate":      [STRAWBERRY_BUSH, WHEAT_BUSH, CARROT_BUSH, POTATO_BUSH,
                               BEET_BUSH, TURNIP_BUSH, CABBAGE_BUSH, LEEK_BUSH, CORN_BUSH,
                               PUMPKIN_BUSH, GARLIC_BUSH, SCALLION_BUSH, APPLE_BUSH,
                               RADISH_BUSH, PEA_BUSH, ZUCCHINI_BUSH, BROCCOLI_BUSH,
                               GRAPEVINE_BUSH, GRAPEVINE_BUSH,
                               CHAMOMILE_BUSH, LAVENDER_BUSH, MINT_BUSH, FLAX_BUSH, FLAX_BUSH,
                               COTTON_BUSH,
                               DILL_BUSH, TARRAGON_BUSH, LEMON_BALM_BUSH, CATNIP_BUSH,
                               ST_JOHNS_WORT_BUSH, YARROW_BUSH, BERGAMOT_BUSH, WOOD_SORREL_BUSH,
                               COMFREY_BUSH, HOP_VINE_BUSH, LENTIL_CROP_YOUNG, TEA_BUSH],
            "boreal":         [STRAWBERRY_BUSH, CARROT_BUSH, POTATO_BUSH, BEET_BUSH,
                               TURNIP_BUSH, CABBAGE_BUSH, LEEK_BUSH, APPLE_BUSH,
                               RADISH_BUSH, PEA_BUSH, BROCCOLI_BUSH, COFFEE_BUSH, GRAPEVINE_BUSH,
                               CHAMOMILE_BUSH, LAVENDER_BUSH, YARROW_BUSH, VALERIAN_BUSH,
                               HOP_VINE_BUSH, TEA_BUSH],
            "birch_forest":   [STRAWBERRY_BUSH, CARROT_BUSH, APPLE_BUSH, POTATO_BUSH,
                               BEET_BUSH, PUMPKIN_BUSH, PEA_BUSH, BROCCOLI_BUSH,
                               COFFEE_BUSH, GRAPEVINE_BUSH,
                               CHAMOMILE_BUSH, LAVENDER_BUSH, LEMON_BALM_BUSH, BERGAMOT_BUSH,
                               WOOD_SORREL_BUSH, HOP_VINE_BUSH, TEA_BUSH],
            "jungle":         [RICE_BUSH, GINGER_BUSH, BOK_CHOY_BUSH, TOMATO_BUSH,
                               PEPPER_BUSH, EGGPLANT_BUSH, SCALLION_BUSH, SWEET_POTATO_BUSH,
                               CHILI_BUSH, COFFEE_BUSH, COFFEE_BUSH, GRAPEVINE_BUSH,
                               TEA_BUSH, TEA_BUSH, MINT_BUSH, BASIL_BUSH, BASIL_BUSH,
                               SESAME_CROP_YOUNG],
            "wetland":        [RICE_BUSH, GINGER_BUSH, BOK_CHOY_BUSH, LEEK_BUSH,
                               CELERY_BUSH, SCALLION_BUSH, PUMPKIN_BUSH, TOMATO_BUSH,
                               WATERMELON_BUSH, COFFEE_BUSH, COFFEE_BUSH, GRAPEVINE_BUSH,
                               MINT_BUSH, MINT_BUSH, ANGELICA_BUSH, COMFREY_BUSH, WOOD_SORREL_BUSH,
                               TEA_BUSH, TEA_BUSH],
            "redwood":        [STRAWBERRY_BUSH, APPLE_BUSH, POTATO_BUSH, CARROT_BUSH,
                               BEET_BUSH, BROCCOLI_BUSH, CABBAGE_BUSH, WOOD_SORREL_BUSH,
                               TEA_BUSH],
            "tropical":       [RICE_BUSH, GINGER_BUSH, BOK_CHOY_BUSH, TOMATO_BUSH,
                               CORN_BUSH, PEPPER_BUSH, CHILI_BUSH, EGGPLANT_BUSH,
                               WATERMELON_BUSH, SCALLION_BUSH, SWEET_POTATO_BUSH, ZUCCHINI_BUSH,
                               COFFEE_BUSH, COFFEE_BUSH, COFFEE_BUSH, GRAPEVINE_BUSH,
                               TEA_BUSH, TEA_BUSH, TEA_BUSH, MINT_BUSH,
                               COTTON_BUSH, COTTON_BUSH,
                               BASIL_BUSH, BASIL_BUSH, LEMON_VERBENA_BUSH,
                               SESAME_CROP_YOUNG, SESAME_CROP_YOUNG],
            "savanna":        [CORN_BUSH, CHILI_BUSH, PEPPER_BUSH, EGGPLANT_BUSH,
                               SWEET_POTATO_BUSH, WATERMELON_BUSH, ONION_BUSH, PUMPKIN_BUSH,
                               COFFEE_BUSH, COFFEE_BUSH, GRAPEVINE_BUSH, ROSEMARY_BUSH,
                               COTTON_BUSH, COTTON_BUSH, COTTON_BUSH,
                               MARJORAM_BUSH, LEMON_VERBENA_BUSH,
                               SESAME_CROP_YOUNG, SESAME_CROP_YOUNG],
            "wasteland":      [BEET_BUSH, TURNIP_BUSH, RADISH_BUSH, ONION_BUSH, ROSEMARY_BUSH,
                               WORMWOOD_BUSH, WORMWOOD_BUSH, MUGWORT_BUSH],
            "fungal":         [],
            "alpine_mountain":[BEET_BUSH, TURNIP_BUSH, BROCCOLI_BUSH, CABBAGE_BUSH, POTATO_BUSH, COFFEE_BUSH, GRAPEVINE_BUSH,
                               TEA_BUSH, TEA_BUSH, CHAMOMILE_BUSH, LAVENDER_BUSH, YARROW_BUSH, VALERIAN_BUSH,
                               SAFFRON_CROP_YOUNG],
            "rocky_mountain": [BEET_BUSH, TURNIP_BUSH, POTATO_BUSH, CARROT_BUSH, COFFEE_BUSH, GRAPEVINE_BUSH, ROSEMARY_BUSH,
                               SAVORY_BUSH, RUE_BUSH, HYSSOP_BUSH,
                               SAFFRON_CROP_YOUNG, CHICKPEA_CROP_YOUNG],
            "rolling_hills":  [STRAWBERRY_BUSH, WHEAT_BUSH, CARROT_BUSH, CORN_BUSH,
                               POTATO_BUSH, APPLE_BUSH, PUMPKIN_BUSH, GARLIC_BUSH,
                               RADISH_BUSH, PEA_BUSH, ZUCCHINI_BUSH, CABBAGE_BUSH, ONION_BUSH,
                               COFFEE_BUSH, GRAPEVINE_BUSH, GRAPEVINE_BUSH, GRAPEVINE_BUSH,
                               TEA_BUSH, CHAMOMILE_BUSH, LAVENDER_BUSH, ROSEMARY_BUSH,
                               FLAX_BUSH, FLAX_BUSH, COTTON_BUSH,
                               THYME_BUSH, THYME_BUSH, OREGANO_BUSH, SAGE_BUSH, MARJORAM_BUSH,
                               YARROW_BUSH, ECHINACEA_BUSH, HYSSOP_BUSH, MUGWORT_BUSH,
                               LENTIL_CROP_YOUNG, HOP_VINE_BUSH],
            "steep_hills":    [STRAWBERRY_BUSH, CARROT_BUSH, POTATO_BUSH, BEET_BUSH,
                               APPLE_BUSH, CABBAGE_BUSH, BROCCOLI_BUSH, GRAPEVINE_BUSH,
                               LAVENDER_BUSH, ROSEMARY_BUSH, THYME_BUSH, SAVORY_BUSH, RUE_BUSH,
                               TEA_BUSH, TEA_BUSH],
            "steppe":         [WHEAT_BUSH, CORN_BUSH, RADISH_BUSH, ONION_BUSH,
                               GARLIC_BUSH, TURNIP_BUSH, GRAPEVINE_BUSH, ROSEMARY_BUSH,
                               FLAX_BUSH, COTTON_BUSH, COTTON_BUSH,
                               THYME_BUSH, SAGE_BUSH, OREGANO_BUSH, WORMWOOD_BUSH,
                               YARROW_BUSH, MUGWORT_BUSH,
                               CHICKPEA_CROP_YOUNG, LENTIL_CROP_YOUNG, LENTIL_CROP_YOUNG],
            "arid_steppe":    [ONION_BUSH, GARLIC_BUSH, CHILI_BUSH, RADISH_BUSH,
                               SWEET_POTATO_BUSH, COFFEE_BUSH, GRAPEVINE_BUSH, ROSEMARY_BUSH,
                               COTTON_BUSH, COTTON_BUSH,
                               THYME_BUSH, SAGE_BUSH, WORMWOOD_BUSH, RUE_BUSH,
                               CHICKPEA_CROP_YOUNG, CHICKPEA_CROP_YOUNG, SESAME_CROP_YOUNG],
            "tundra":         [BEET_BUSH, TURNIP_BUSH, CABBAGE_BUSH, RADISH_BUSH, COFFEE_BUSH, TEA_BUSH, CHAMOMILE_BUSH,
                               YARROW_BUSH, ANGELICA_BUSH],
            "coastal":        [WATERMELON_BUSH, SWEET_POTATO_BUSH, CORN_BUSH, COFFEE_BUSH, GRAPEVINE_BUSH,
                               TEA_BUSH, TEA_BUSH, MINT_BUSH, LAVENDER_BUSH, FENNEL_BUSH, LEMON_VERBENA_BUSH,
                               OLIVE_TREE_YOUNG],
            "mediterranean":  [TOMATO_BUSH, ONION_BUSH, GARLIC_BUSH, PEPPER_BUSH, CORN_BUSH,
                               COFFEE_BUSH, GRAPEVINE_BUSH, GRAPEVINE_BUSH, GRAPEVINE_BUSH,
                               TEA_BUSH, TEA_BUSH, LAVENDER_BUSH, ROSEMARY_BUSH, THYME_BUSH,
                               SAGE_BUSH, FENNEL_BUSH, OREGANO_BUSH, MARJORAM_BUSH,
                               CHICKPEA_CROP_YOUNG, LENTIL_CROP_YOUNG, SAFFRON_CROP_YOUNG,
                               POMEGRANATE_TREE_YOUNG, POMEGRANATE_TREE_YOUNG, OLIVE_TREE_YOUNG, OLIVE_TREE_YOUNG],
            "bamboo_forest":  [RICE_BUSH, BOK_CHOY_BUSH, SCALLION_BUSH, GINGER_BUSH,
                               TEA_BUSH, TEA_BUSH, TEA_BUSH, MINT_BUSH, BASIL_BUSH,
                               CHAMOMILE_BUSH, LEMON_VERBENA_BUSH],
            "swamp":          [RICE_BUSH, CELERY_BUSH, LEEK_BUSH, SCALLION_BUSH, COFFEE_BUSH, MINT_BUSH, MINT_BUSH,
                               VALERIAN_BUSH, ANGELICA_BUSH, COMFREY_BUSH, CATNIP_BUSH,
                               TEA_BUSH, TEA_BUSH],
            "beach":          [WATERMELON_BUSH, SWEET_POTATO_BUSH, CORN_BUSH, COFFEE_BUSH],
            "pacific_island": [SWEET_POTATO_BUSH, CORN_BUSH, WATERMELON_BUSH, GINGER_BUSH,
                               RICE_BUSH, COFFEE_BUSH, COFFEE_BUSH,
                               TARO_BUSH, TARO_BUSH, BREADFRUIT_BUSH, COCONUT_BUSH, COCONUT_BUSH,
                               TEA_BUSH, TEA_BUSH],
            "canyon":         [ONION_BUSH, GARLIC_BUSH, CHILI_BUSH, TOMATO_BUSH, CORN_BUSH, COFFEE_BUSH, GRAPEVINE_BUSH, GRAPEVINE_BUSH, ROSEMARY_BUSH,
                               OREGANO_BUSH, FENNEL_BUSH, LEMON_VERBENA_BUSH, WORMWOOD_BUSH,
                               CHICKPEA_CROP_YOUNG, SESAME_CROP_YOUNG, POMEGRANATE_TREE_YOUNG, OLIVE_TREE_YOUNG],
        }
        bush_rng = random.Random(hash((self.seed, cx, 'bushes')) & 0x7FFFFFFF)
        lx = 5
        while lx < CHUNK_W - 5:
            x = cx * CHUNK_W + lx
            sy = self.surface_height(x)
            biodome = self.biodome_at(x)
            pool = _BIOME_BUSHES.get(biodome, [])
            surf = chunk[sy][lx]
            if pool and 0 < sy < WORLD_H and chunk[sy - 1][lx] == AIR and surf in (GRASS, SNOW, SAND):
                chunk[sy - 1][lx] = bush_rng.choice(pool)
            lx += bush_rng.randint(4, 9)

        # Water-edge plants — spawn on grass tiles adjacent to surface water,
        # and floating plants on open water surface tiles.
        _WATER_EDGE_BIOMES = frozenset({
            "temperate", "boreal", "birch_forest", "wetland", "swamp",
            "jungle", "tropical", "rolling_hills", "tundra",
        })
        _FLOAT_POOL = {
            # biome → weighted list of floating blocks
            "wetland":  [POND_WEED_BLOCK, POND_WEED_BLOCK, WATER_HYACINTH_BLOCK, DUCKWEED_BLOCK, FROGBIT_BLOCK],
            "swamp":    [POND_WEED_BLOCK, DUCKWEED_BLOCK, DUCKWEED_BLOCK, FROGBIT_BLOCK, WATER_HYACINTH_BLOCK],
            "jungle":   [LOTUS_BLOCK, LOTUS_BLOCK, WATER_HYACINTH_BLOCK, FROGBIT_BLOCK, POND_WEED_BLOCK],
            "tropical": [LOTUS_BLOCK, LOTUS_BLOCK, WATER_HYACINTH_BLOCK, WATER_HYACINTH_BLOCK, FROGBIT_BLOCK],
        }
        _FLOAT_DEFAULT = [POND_WEED_BLOCK, POND_WEED_BLOCK, DUCKWEED_BLOCK, FROGBIT_BLOCK]
        _EDGE_POOL = {
            # biome → weighted list of edge blocks
            "wetland":  [CATTAIL_BLOCK, CATTAIL_BLOCK, REED_BLOCK, BULRUSH_BLOCK,
                         SEDGE_BLOCK, PICKERELWEED_BLOCK, ARROWHEAD_BLOCK],
            "swamp":    [BULRUSH_BLOCK, BULRUSH_BLOCK, CATTAIL_BLOCK, SEDGE_BLOCK,
                         REED_BLOCK, PICKERELWEED_BLOCK],
            "jungle":   [ARROWHEAD_BLOCK, ARROWHEAD_BLOCK, REED_BLOCK, BULRUSH_BLOCK,
                         PICKERELWEED_BLOCK, WATER_CRESS_BLOCK],
            "tropical": [ARROWHEAD_BLOCK, REED_BLOCK, PICKERELWEED_BLOCK, WATER_CRESS_BLOCK],
            "temperate":[REED_BLOCK, REED_BLOCK, WATER_CRESS_BLOCK, MARSH_MARIGOLD_BLOCK,
                         WATER_IRIS_BLOCK, HORSETAIL_BLOCK, ARROWHEAD_BLOCK],
            "boreal":   [REED_BLOCK, REED_BLOCK, HORSETAIL_BLOCK, SEDGE_BLOCK,
                         WATER_CRESS_BLOCK, MARSH_MARIGOLD_BLOCK],
            "birch_forest": [REED_BLOCK, WATER_CRESS_BLOCK, WATER_IRIS_BLOCK,
                             MARSH_MARIGOLD_BLOCK, HORSETAIL_BLOCK],
            "rolling_hills": [REED_BLOCK, WATER_CRESS_BLOCK, WATER_IRIS_BLOCK,
                              MARSH_MARIGOLD_BLOCK, ARROWHEAD_BLOCK],
            "tundra":   [SEDGE_BLOCK, SEDGE_BLOCK, FROZEN_BOG, REED_BLOCK, HORSETAIL_BLOCK],
        }
        _EDGE_DEFAULT = [REED_BLOCK]
        _SNOW_EDGE_BIOMES = frozenset({"tundra", "alpine_mountain"})
        water_rng = random.Random(hash((self.seed, cx, 'water_plants')) & 0x7FFFFFFF)
        chunk_x0 = cx * CHUNK_W
        for lx in range(CHUNK_W):
            x = chunk_x0 + lx
            sy = self.surface_height(x)
            if sy <= 0 or sy >= WORLD_H - 1:
                continue
            # Floating plants: go in the bg layer at the air tile above the water
            if chunk[sy][lx] == WATER and sy > 0 and chunk[sy - 1][lx] == AIR:
                if water_rng.random() < 0.20:
                    biodome = self.biodome_at(x)
                    if biodome in _WATER_EDGE_BIOMES:
                        pool = _FLOAT_POOL.get(biodome, _FLOAT_DEFAULT)
                        self.set_bg_block(x, sy - 1, water_rng.choice(pool))
                continue
            biodome_here = self.biodome_at(x)
            surface_ok = chunk[sy][lx] == GRASS or (biodome_here in _SNOW_EDGE_BIOMES and chunk[sy][lx] == SNOW)
            if not surface_ok:
                continue
            # Check for water within 3 tiles horizontally at same surface level
            water_adj = any(
                0 <= lx + dx < CHUNK_W and chunk[sy][lx + dx] == WATER
                for dx in range(-3, 4) if dx != 0
            )
            if not water_adj or water_rng.random() > 0.65:
                continue
            if biodome_here not in _WATER_EDGE_BIOMES:
                continue
            pool = _EDGE_POOL.get(biodome_here, _EDGE_DEFAULT)
            self.set_bg_block(x, sy - 1, water_rng.choice(pool))

        # Desert surface flora — spawns on SAND in desert/arid biomes
        desert_rng = random.Random(hash((self.seed, cx, 'desert')) & 0x7FFFFFFF)
        lx = 4
        while lx < CHUNK_W - 4:
            x = cx * CHUNK_W + lx
            sy = self.surface_height(x)
            biodome = self.biodome_at(x)
            if biodome in ("desert", "arid_steppe") and 0 < sy < WORLD_H \
                    and chunk[sy - 1][lx] == AIR and chunk[sy][lx] == SAND:
                chunk[sy - 1][lx] = desert_rng.choice([
                    CACTUS_YOUNG, CACTUS_YOUNG, CACTUS_YOUNG,
                    DATE_PALM_BUSH, DATE_PALM_BUSH,
                    AGAVE_BUSH, AGAVE_BUSH,
                    SAGUARO_YOUNG, SAGUARO_YOUNG,
                    BARREL_CACTUS_YOUNG, BARREL_CACTUS_YOUNG,
                    OCOTILLO_YOUNG,
                    PRICKLY_PEAR_YOUNG, PRICKLY_PEAR_YOUNG,
                    CHOLLA_YOUNG,
                    PALO_VERDE_YOUNG,
                ])
            lx += desert_rng.randint(5, 11)

        # Tundra ice formations — ice shards on snow surface in tundra
        ice_rng = random.Random(hash((self.seed, cx, 'tundra_ice')) & 0x7FFFFFFF)
        lx = 3
        while lx < CHUNK_W - 3:
            x = cx * CHUNK_W + lx
            sy = self.surface_height(x)
            biodome = self.biodome_at(x)
            if biodome == "tundra" and 0 < sy < WORLD_H \
                    and chunk[sy - 1][lx] == AIR and chunk[sy][lx] == SNOW:
                if ice_rng.random() < 0.03:
                    chunk[sy - 1][lx] = ICE_SHARD
            lx += ice_rng.randint(6, 16)

        # Wildflowers
        flower_rng = random.Random(hash((self.seed, cx, 'flowers')) & 0x7FFFFFFF)
        lx = 1
        while lx < CHUNK_W - 1:
            x = cx * CHUNK_W + lx
            sy = self.surface_height(x)
            biodome = self.biodome_at(x)
            if 0 < sy < WORLD_H and chunk[sy - 1][lx] == AIR and chunk[sy][lx] == GRASS:
                if flower_rng.random() < 0.25:
                    chunk[sy - 1][lx] = WILDFLOWER_PATCH
            lo, hi = {
                "jungle": (5, 10), "tropical": (5, 10), "wetland": (6, 12),
                "temperate": (8, 16), "boreal": (9, 18), "birch_forest": (8, 16),
                "redwood": (9, 18), "savanna": (10, 20), "wasteland": (20, 40),
                "fungal": (8, 16),
                "alpine_mountain": (30, 55), "rocky_mountain": (22, 42),
                "rolling_hills": (8, 16), "steep_hills": (9, 18),
                "steppe": (15, 28), "arid_steppe": (24, 46),
                "desert": (35, 65), "tundra": (28, 50),
                "swamp": (5, 10), "beach": (18, 34),
                "canyon": (20, 38),
            }.get(biodome, (9, 18))
            lx += flower_rng.randint(lo, hi)

        # Lakes (chunk-local)
        self._gen_chunk_lakes(cx, chunk)
        self._gen_chunk_oil_pockets(cx, chunk)

    def _gen_chunk_lakes(self, cx: int, chunk: list):
        """Carve small lakes within this chunk."""
        rng = random.Random(hash((self.seed, cx, 'lakes')) & 0x7FFFFFFF)
        _impassable = {BEDROCK, GATE_MID, GATE_DEEP, GATE_CORE}
        # Each zone has a probability of spawning one lake per chunk
        zones = [
            (15,  38,  1.00,  4,  8, 2, 3),
            (45,  98,  1.00,  7, 14, 3, 4),
            (105, 158, 1.00, 10, 20, 3, 5),
            (165, 190, 0.96, 12, 24, 4, 6),
        ]
        for depth_min, depth_max, prob, w_min, w_max, h_min, h_max in zones:
            if rng.random() > prob:
                continue
            center_lx = rng.randint(4, CHUNK_W - 5)
            depth  = rng.randint(depth_min, depth_max)
            abs_y  = SURFACE_Y + depth
            w = rng.randint(w_min, w_max)
            h = rng.randint(h_min, h_max)
            lx0 = max(0, center_lx - w // 2)
            lx1 = min(CHUNK_W - 1, center_lx + w // 2)
            y0  = max(SURFACE_Y + 8, abs_y - h // 2)
            y1  = min(WORLD_H - 3, abs_y + h // 2)
            for ly in range(y0, y1 + 1):
                for lx in range(lx0, lx1 + 1):
                    if chunk[ly][lx] not in _impassable:
                        chunk[ly][lx] = WATER
                        world_x = cx * CHUNK_W + lx
                        self._water_level[(world_x, ly)] = 8
                        self._lake_cells.append((ly, world_x))

    def _gen_chunk_oil_pockets(self, cx: int, chunk: list):
        """Carve small static oil pockets within this chunk (no flow)."""
        rng = random.Random(hash((self.seed, cx, 'oil')) & 0x7FFFFFFF)
        _impassable = {BEDROCK, GATE_MID, GATE_DEEP, GATE_CORE, WATER}
        if rng.random() > 0.30:
            return
        center_lx = rng.randint(4, CHUNK_W - 5)
        depth = rng.randint(40, 150)
        abs_y = SURFACE_Y + depth
        w = rng.randint(3, 8)
        h = rng.randint(2, 4)
        lx0 = max(0, center_lx - w // 2)
        lx1 = min(CHUNK_W - 1, center_lx + w // 2)
        y0  = max(SURFACE_Y + 35, abs_y - h // 2)
        y1  = min(WORLD_H - 3, abs_y + h // 2)
        for ly in range(y0, y1 + 1):
            for lx in range(lx0, lx1 + 1):
                if chunk[ly][lx] not in _impassable:
                    chunk[ly][lx] = OIL

    # ------------------------------------------------------------------ surface water --

    _SURF_WATER_ZONE_W = 300
    _SURF_WATER_LAKE_BIOMES = frozenset({
        "temperate", "boreal", "birch_forest", "wetland", "swamp",
        "tundra", "jungle", "tropical", "rolling_hills", "pacific_island",
    })
    _SURF_WATER_RIVER_BIOMES = frozenset({
        "temperate", "boreal", "wetland", "swamp", "rolling_hills",
        "birch_forest", "jungle",
    })

    def _get_surf_water_body(self, zone_idx: int):
        if zone_idx in self._surf_water_cache:
            return self._surf_water_cache[zone_idx]

        zone_center = zone_idx * self._SURF_WATER_ZONE_W + self._SURF_WATER_ZONE_W // 2
        biodome = self.biodome_at(zone_center)
        can_lake = biodome in self._SURF_WATER_LAKE_BIOMES
        can_river = biodome in self._SURF_WATER_RIVER_BIOMES

        if not can_lake and not can_river:
            self._surf_water_cache[zone_idx] = None
            return None

        rng = random.Random(self._zone_seed(self.seed, zone_idx, 7))
        prob = 1.00 if can_river else 0.75
        if rng.random() > prob:
            self._surf_water_cache[zone_idx] = None
            return None

        if can_river and can_lake:
            wb_type = rng.choice(["lake", "lake", "river"])
        elif can_river:
            wb_type = "river"
        else:
            wb_type = "lake"

        zone_start = zone_idx * self._SURF_WATER_ZONE_W
        cx_abs = zone_start + rng.randint(50, self._SURF_WATER_ZONE_W - 50)

        if wb_type == "lake":
            half_w = rng.randint(6, 18)
            max_depth = rng.randint(3, 10)
        else:
            half_w = rng.randint(15, 35)
            max_depth = rng.randint(2, 5)

        result = {"type": wb_type, "cx_abs": cx_abs, "half_w": half_w, "max_depth": max_depth}
        self._surf_water_cache[zone_idx] = result
        return result

    def _gen_surface_water(self, cx: int, chunk: list):
        _impassable = {BEDROCK, GATE_MID, GATE_DEEP, GATE_CORE}
        chunk_x0 = cx * CHUNK_W
        chunk_x1 = chunk_x0 + CHUNK_W - 1
        max_reach = 35

        z0 = (chunk_x0 - max_reach) // self._SURF_WATER_ZONE_W
        z1 = (chunk_x1 + max_reach) // self._SURF_WATER_ZONE_W

        for zone_idx in range(z0, z1 + 1):
            wb = self._get_surf_water_body(zone_idx)
            if wb is None:
                continue

            cx_abs = wb["cx_abs"]
            half_w = wb["half_w"]
            max_depth = wb["max_depth"]
            wb_type = wb["type"]

            x_start = cx_abs - half_w
            x_end = cx_abs + half_w
            if x_end < chunk_x0 or x_start > chunk_x1:
                continue

            water_top_y = self.surface_height(cx_abs)

            for x in range(max(x_start, chunk_x0), min(x_end, chunk_x1) + 1):
                lx = x - chunk_x0
                dx = abs(x - cx_abs)
                t = dx / half_w

                # Skip columns where terrain drops below the water level — water
                # would float in air above the actual ground surface there.
                local_sy = self.surface_height(x)
                if local_sy > water_top_y:
                    continue

                if wb_type == "lake":
                    depth_x = max(1, round(max_depth * (1.0 - t * t)))
                else:
                    flat_half = half_w * 0.55
                    if dx <= flat_half:
                        depth_x = max_depth
                    else:
                        edge_t = (dx - flat_half) / (half_w - flat_half)
                        depth_x = max(1, round(max_depth * (1.0 - edge_t)))

                spot_rng = random.Random(hash((self.seed, x, zone_idx, 'fspot')) & 0x7FFFFFFF)
                for y in range(water_top_y, water_top_y + depth_x):
                    if y <= 0 or y >= WORLD_H - 1:
                        continue
                    if chunk[y][lx] not in _impassable:
                        is_surface_row = (y == water_top_y)
                        use_spot = is_surface_row and spot_rng.random() < 0.08
                        chunk[y][lx] = FISHING_SPOT_BLOCK if use_spot else WATER
                        self._water_level[(x, y)] = 8
                        self._lake_cells.append((y, x))

            # Bank fill: where terrain dips below the water surface level on
            # the shore or at skipped edge columns, fill with dirt so the
            # waterline is never visually "above" a dirt-free gap.
            shore_fill = 4
            bx0 = max(x_start - shore_fill, chunk_x0)
            bx1 = min(x_end + shore_fill, chunk_x1)
            for x in range(bx0, bx1 + 1):
                lx = x - chunk_x0
                local_sy = self.surface_height(x)
                if local_sy <= water_top_y:
                    continue  # terrain at or above water surface — no gap to fill
                for y in range(water_top_y, local_sy):
                    if y <= 0 or y >= WORLD_H - 1:
                        continue
                    if chunk[y][lx] == AIR:
                        chunk[y][lx] = DIRT

    # ------------------------------------------------------------------ caves --

    _BIOME_CAVE = {
        "igneous":     {"freq": 1.0, "size": 1.0},
        "sedimentary": {"freq": 1.3, "size": 0.8},
        "crystal":     {"freq": 0.8, "size": 1.4},
        "ferrous":     {"freq": 0.9, "size": 0.9},
        "void":        {"freq": 1.5, "size": 1.6},
    }
    _BIOME_STALA = {
        "igneous": 0.12, "sedimentary": 0.18, "crystal": 0.22, "ferrous": 0.10, "void": 0.08,
    }

    def _gen_caves(self):
        def _ct(label, t):
            print(f"    cave/{label}: {(_time.perf_counter()-t)*1000:.0f}ms")
            return _time.perf_counter()

        rng = random.Random(self.seed + 9876)
        impassable = {BEDROCK, GATE_MID, GATE_DEEP, GATE_CORE}
        t = _time.perf_counter()

        # Pre-compute 3-block water-proximity guard using positions tracked by _gen_lakes
        water_near = [[False] * self.width for _ in range(self.height)]
        H, W = self.height, self.width
        for wy, wx in self._lake_cells:
            for dy in range(-3, 4):
                ny = wy + dy
                if 0 <= ny < H:
                    row = water_near[ny]
                    for dx in range(-3, 4):
                        nx = wx + dx
                        if 0 <= nx < W:
                            row[nx] = True
        t = _ct("water_near", t)

        # (depth_min, depth_max, n_nets, min_len, max_len, r_min, r_max, branch_chance)
        zones = [
            (10,  38,  4,  30,  60,  1, 2, 0.25),
            (42,  98,  6,  50, 100,  2, 3, 0.40),
            (102, 158, 7,  70, 130,  2, 4, 0.50),
            (162, 192, 5,  80, 150,  3, 5, 0.55),
        ]

        cave_cells = set()
        for d_min, d_max, n_nets, min_len, max_len, r_min, r_max, branch_ch in zones:
            for _ in range(n_nets):
                cx = rng.randint(10, self.width - 10)
                cy = SURFACE_Y + rng.randint(d_min, d_max)
                bm = self._biome_cave_params(cx)
                n_actual = max(1, round(n_nets * bm["freq"]))
                r_actual = r_max * bm["size"]
                l_actual = round(max_len * bm["size"])
                self._carve_network(
                    cx, cy, min_len, l_actual, r_min, r_actual,
                    branch_ch, rng, impassable, water_near, cave_cells,
                )
        t = _ct("carve_networks", t)

        self._carve_chimneys(rng, impassable, water_near, cave_cells)
        t = _ct("chimneys", t)
        self._carve_geodes(rng, impassable, water_near, cave_cells)
        t = _ct("geodes", t)
        self._cave_ca_smooth(cave_cells, impassable)
        t = _ct("ca_smooth", t)
        self._mark_cracked_ceilings(cave_cells, impassable)
        t = _ct("cracked_ceilings", t)
        self._place_natural_columns(cave_cells)
        t = _ct("columns", t)
        self._place_speleothems(cave_cells, rng)
        t = _ct("speleothems", t)
        self._place_cave_flora(cave_cells, rng)
        t = _ct("flora", t)
        self._place_gravel(cave_cells, rng)
        t = _ct("gravel", t)
        self._place_cave_mushrooms(cave_cells, rng)
        _ct("mushrooms", t)

    def _biome_cave_params(self, bx):
        biome = self.biome_at(bx)
        return self._BIOME_CAVE.get(biome, {"freq": 1.0, "size": 1.0})

    _circle_cache = {}

    @staticmethod
    def _circle_offsets(ir):
        if ir not in World._circle_cache:
            World._circle_cache[ir] = [
                (dx, dy)
                for dy in range(-ir, ir + 1)
                for dx in range(-ir, ir + 1)
                if dx * dx + dy * dy <= ir * ir
            ]
        return World._circle_cache[ir]

    def _carve_network(self, sx, sy, min_len, max_len, r_min, r_max,
                       branch_chance, rng, impassable, water_near, cave_cells):
        W, H = self.width, self.height
        grid = self.grid
        stack = [(float(sx), float(sy), rng.uniform(0, 2 * pi), float(r_min), float(r_max))]
        max_segments = 8
        segments = 0
        while stack and segments < max_segments:
            segments += 1
            x, y, angle, radius, max_r = stack.pop()
            length = rng.randint(min_len, max_len)
            for _ in range(length):
                angle += rng.uniform(-0.4, 0.4)
                x += cos(angle)
                y += sin(angle) * 0.5
                bx, by = int(x), int(y)
                if not (1 <= bx < W - 1 and SURFACE_Y + 5 <= by < H - 2):
                    break
                if water_near[by][bx]:
                    continue
                radius += rng.uniform(-0.15, 0.2)
                radius = max(r_min, min(max_r, radius))
                ir = max(1, int(radius))
                for dx, dy in World._circle_offsets(ir):
                    nx, ny = bx + dx, by + dy
                    if (1 <= nx < W - 1
                            and SURFACE_Y + 5 <= ny < H - 2
                            and not water_near[ny][nx]
                            and grid[ny][nx] not in impassable):
                        grid[ny][nx] = AIR
                        cave_cells.add((nx, ny))
                if rng.random() < branch_chance:
                    ba = angle + rng.choice([-1.0, 1.0]) * rng.uniform(0.5, 1.2)
                    stack.append((x, y, ba, max(r_min, radius - 0.5), max(r_min, max_r - 0.5)))

    def _cave_ca_smooth(self, cave_cells, impassable):
        neighbours8 = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)]
        candidates = set()
        for cx, cy in cave_cells:
            for dx, dy in neighbours8:
                nx, ny = cx + dx, cy + dy
                if (0 <= nx < self.width and 0 <= ny < self.height
                        and self.grid[ny][nx] not in impassable
                        and self.grid[ny][nx] != AIR):
                    candidates.add((nx, ny))
        for bx, by in candidates:
            air_count = sum(
                1 for dx, dy in neighbours8
                if 0 <= bx + dx < self.width and 0 <= by + dy < self.height
                and self.grid[by + dy][bx + dx] == AIR
            )
            if air_count >= 5:
                self.grid[by][bx] = AIR
                cave_cells.add((bx, by))

    def _mark_cracked_ceilings(self, cave_cells, impassable):
        cells_by_row = {}
        for cx, cy in cave_cells:
            cells_by_row.setdefault(cy, []).append(cx)
        for cy, xs in cells_by_row.items():
            ceiling_y = cy - 1
            if ceiling_y < 0:
                continue
            xs.sort()
            run_start = xs[0]
            prev_x = xs[0]
            for x in xs[1:] + [None]:
                if x is None or x > prev_x + 1:
                    span = prev_x - run_start + 1
                    if span >= 7:
                        for cx2 in range(run_start, prev_x + 1):
                            b = self.grid[ceiling_y][cx2]
                            if b not in impassable and b != AIR:
                                if (cx2 * 1031 + ceiling_y * 7919) % 2 == 0:
                                    self.grid[ceiling_y][cx2] = CRACKED_STONE
                    if x is not None:
                        run_start = x
                prev_x = x if x is not None else prev_x

    def _place_natural_columns(self, cave_cells):
        cells_by_row = {}
        for cx, cy in cave_cells:
            cells_by_row.setdefault(cy, []).append(cx)
        placed_cols = set()
        for cy, xs in cells_by_row.items():
            xs.sort()
            run_start = xs[0]
            prev_x = xs[0]
            for x in xs[1:] + [None]:
                if x is None or x > prev_x + 1:
                    span = prev_x - run_start + 1
                    if span >= 10:
                        col_x = run_start + 3
                        while col_x < prev_x - 3:
                            if col_x not in placed_cols:
                                self._try_place_column(col_x, cy)
                                placed_cols.add(col_x)
                            col_x += 7
                    if x is not None:
                        run_start = x
                prev_x = x if x is not None else prev_x

    def _try_place_column(self, bx, mid_y):
        ceiling_y = mid_y
        while ceiling_y > 0 and self.grid[ceiling_y][bx] == AIR:
            ceiling_y -= 1
        floor_y = mid_y
        while floor_y < self.height - 1 and self.grid[floor_y][bx] == AIR:
            floor_y += 1
        if floor_y - ceiling_y > 4:
            sy = self.surface_y_at(bx)
            for fy in range(ceiling_y + 1, floor_y):
                if self.grid[fy][bx] == AIR:
                    self.grid[fy][bx] = self._stone_for_depth(fy - sy)

    def _place_speleothems(self, cave_cells, rng):
        for cx, cy in cave_cells:
            biome = self._biome_map[max(0, min(self.width - 1, cx))]
            freq = self._BIOME_STALA.get(biome, 0.12)
            if cy > 0:
                above = self.grid[cy - 1][cx]
                if above not in (AIR, CRACKED_STONE) and above != WATER:
                    if rng.random() < freq:
                        self.grid[cy][cx] = STALACTITE
                        continue
            if cy < self.height - 1:
                below = self.grid[cy + 1][cx]
                if below not in (AIR,) and below != WATER and self.grid[cy][cx] == AIR:
                    if rng.random() < freq * 0.7:
                        self.grid[cy][cx] = STALAGMITE

    def _carve_chimneys(self, rng, impassable, water_near, cave_cells):
        # Narrow vertical shafts that punch between depth zones, linking them visually
        n_chimneys = rng.randint(6, 10)
        for _ in range(n_chimneys):
            cx = rng.randint(10, self.width - 10)
            top_y = SURFACE_Y + rng.randint(15, 130)
            bottom_y = top_y + rng.randint(20, 50)
            bottom_y = min(bottom_y, self.height - 5)
            radius = rng.randint(1, 2)
            for cy in range(top_y, bottom_y):
                if water_near[cy][cx]:
                    break
                for dx in range(-radius, radius + 1):
                    nx = cx + dx
                    if (1 <= nx < self.width - 1
                            and self.grid[cy][nx] not in impassable
                            and not water_near[cy][nx]):
                        self.grid[cy][nx] = AIR
                        cave_cells.add((nx, cy))

    def _carve_geodes(self, rng, impassable, water_near, cave_cells):
        # Rare spherical chambers with crystal-lined walls; 2-4 per world
        n_geodes = rng.randint(2, 4)
        for _ in range(n_geodes):
            cx = rng.randint(12, self.width - 12)
            cy = SURFACE_Y + rng.randint(80, 185)
            radius = rng.randint(5, 9)
            if not (0 <= cy < self.height and 0 <= cx < self.width):
                continue
            if water_near[cy][cx]:
                continue
            # Carve sphere interior (r-2) as air, ring (r-2 to r) as crystal ore
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    dist2 = dx * dx + dy * dy
                    ny, nx = cy + dy, cx + dx
                    if not (1 <= nx < self.width - 1 and SURFACE_Y + 5 <= ny < self.height - 2):
                        continue
                    if self.grid[ny][nx] in impassable or water_near[ny][nx]:
                        continue
                    inner = (radius - 2) ** 2
                    outer = radius * radius
                    if dist2 <= inner:
                        self.grid[ny][nx] = AIR
                        cave_cells.add((nx, ny))
                    elif dist2 <= outer:
                        self.grid[ny][nx] = CRYSTAL_ORE

    def _place_cave_flora(self, cave_cells, rng):
        # Cave moss: floor cells in shallow/sedimentary; cave crystals: deep/crystal wall cells
        _moss_biomes    = {"sedimentary", "igneous"}
        _crystal_biomes = {"crystal", "void"}
        for cx, cy in cave_cells:
            biome = self._biome_map[max(0, min(self.width - 1, cx))]
            depth = cy - SURFACE_Y
            # Cave moss on floors (solid block below, air above) in shallow zones
            if (cy < self.height - 1 and self.grid[cy + 1][cx] not in (AIR, WATER)
                    and self.grid[cy][cx] == AIR and depth < 80
                    and biome in _moss_biomes and rng.random() < 0.18):
                self.grid[cy][cx] = CAVE_MOSS
            # Cave crystal clusters on walls/floors in deep crystal zones
            elif (depth >= 80 and biome in _crystal_biomes and self.grid[cy][cx] == AIR):
                # Attach to any adjacent solid block
                has_solid_neighbour = any(
                    0 <= cy + dy < self.height and 0 <= cx + dx < self.width
                    and self.grid[cy + dy][cx + dx] not in (AIR, WATER)
                    for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))
                )
                if has_solid_neighbour and rng.random() < 0.10:
                    self.grid[cy][cx] = CAVE_CRYSTAL

    def _place_gravel(self, cave_cells, rng):
        # Gravel pockets along cave floors and in shallow sedimentary zones
        _gravel_biomes = {"sedimentary", "igneous", "ferrous"}
        solid = {STONE, COAL_ORE, IRON_ORE, GOLD_ORE, CRYSTAL_ORE, RUBY_ORE, OBSIDIAN, CRACKED_STONE}
        for cx, cy in cave_cells:
            biome = self._biome_map[max(0, min(self.width - 1, cx))]
            depth = cy - SURFACE_Y
            if depth > 100 or biome not in _gravel_biomes:
                continue
            if (cy < self.height - 1 and self.grid[cy][cx] == AIR
                    and self.grid[cy + 1][cx] in solid and rng.random() < 0.12):
                # Chance to also convert the solid block below into gravel (pebble patch)
                if rng.random() < 0.4:
                    self.grid[cy + 1][cx] = GRAVEL

    def _place_cave_mushrooms(self, cave_cells, rng):
        _freq = {"igneous": 0.10, "sedimentary": 0.12, "crystal": 0.18, "ferrous": 0.06, "void": 0.16}
        _DEEP_ONLY = {BIOLUME, MAGMA_CAP, DEEP_INK, OBSIDIAN_SHELF}  # require depth >= 80
        _BIOME_POOL = {
            "igneous":     [CAVE_MUSHROOM, EMBER_CAP, BLOOD_CAP, MAGMA_CAP, COAL_PUFF, SULFUR_DOME, RUST_SHELF, SULFUR_TUFT],
            "sedimentary": [CAVE_MUSHROOM, GOLD_CHANTERELLE, HONEY_CLUSTER, AMBER_PUFF, COPPER_SHELF, PALE_GHOST, MOSSY_CAP],
            "crystal":     [CAVE_MUSHROOM, COBALT_CAP, TEAL_BELL, BIOLUME, CORAL_TUFT, IVORY_BELL, SULFUR_DOME],
            "ferrous":     [CAVE_MUSHROOM, RUST_SHELF, ASH_BELL, STONE_PUFF, BONE_STALK, BLOOD_CAP],
            "void":        [CAVE_MUSHROOM, DEEP_INK, VIOLET_CROWN, PALE_GHOST, OBSIDIAN_SHELF, ASH_BELL],
        }
        solid = {STONE, COAL_ORE, IRON_ORE, GOLD_ORE, CRYSTAL_ORE, RUBY_ORE, OBSIDIAN,
                 CRACKED_STONE, GRAVEL}
        placed = set()
        for cx, cy in cave_cells:
            if (cx, cy) in placed:
                continue
            if cy < 1 or cy + 1 >= self.height:
                continue
            depth = cy - SURFACE_Y
            if depth < 12:
                continue
            if self.grid[cy][cx] != AIR:
                continue
            if self.grid[cy + 1][cx] not in solid:
                continue
            biome = self._biome_map[max(0, min(self.width - 1, cx))]
            freq = _freq.get(biome, 0.10)
            if rng.random() < freq:
                pool = [m for m in _BIOME_POOL.get(biome, [CAVE_MUSHROOM])
                        if m not in _DEEP_ONLY or depth >= 80]
                self.grid[cy][cx] = rng.choice(pool or [CAVE_MUSHROOM])
                placed.add((cx, cy))

    # ---------------------------------------------------------------- /caves --

    def _stone_for_depth(self, depth):
        """Return the geological stone block appropriate for this depth."""
        if depth < 15:  return STONE
        if depth < 60:  return LIMESTONE_STONE
        if depth < 120: return GRANITE_STONE
        if depth < 180: return BASALT_STONE
        return MAGMATIC_STONE

    def _vein_noise(self, bx, by, seed_offset, scale=5):
        """Smooth value noise [0,1] for vein/cluster placement — nearby blocks return similar values."""
        fx = bx / scale
        fy = by / scale
        ix = math.floor(fx)
        iy = math.floor(fy)
        tx = fx - ix
        ty = fy - iy
        tx = tx * tx * (3.0 - 2.0 * tx)
        ty = ty * ty * (3.0 - 2.0 * ty)
        s = (self.seed + seed_offset) & 0x7FFFFFFF
        def _h(gx, gy):
            v = (s ^ (gx * 374761393)) & 0xFFFFFFFF
            v = (v ^ (gy * 668265263)) & 0xFFFFFFFF
            v = ((v ^ (v >> 15)) * 2246822519) & 0xFFFFFFFF
            v = ((v ^ (v >> 13)) * 3266489917) & 0xFFFFFFFF
            return (v & 0xFFFF) / 65535.0
        v00 = _h(ix,   iy)
        v10 = _h(ix+1, iy)
        v01 = _h(ix,   iy+1)
        v11 = _h(ix+1, iy+1)
        return (v00*(1.0-tx) + v10*tx)*(1.0-ty) + (v01*(1.0-tx) + v11*tx)*ty

    def _pick_block(self, depth, rng, biome="igneous", bx=0, by=0):
        r = rng.random()
        # Clay deposits — shallow pockets in sedimentary/temperate/wetland/river zones
        if depth < 35 and biome in ("sedimentary", "temperate", "wetland", "river", "swamp",
                                    "steppe", "arid_steppe", "savanna",
                                    "birch_forest", "boreal", "rolling_hills", "rocky_mountain", "canyon"):
            clay_n = self._vein_noise(bx, by, 0x3C1A2, scale=5)
            if clay_n >= 0.60 and r < 0.07:
                return CLAY_DEPOSIT
        # Salt deposits — mid-depth evaporite beds in arid/sedimentary strata
        if depth < 60 and biome in ("sedimentary", "arid_steppe", "steppe", "igneous"):
            salt_n = self._vein_noise(bx, by, 0x5A1C3B, scale=6)
            if salt_n >= 0.62 and r < 0.045:
                return SALT_DEPOSIT
        # Marble veins — medium-depth sedimentary pockets; rarer than limestone
        if 25 <= depth < 80 and biome in ("sedimentary", "temperate"):
            marb_n = self._vein_noise(bx, by, 0xD4A1F2, scale=6)
            if marb_n >= 0.63 and r < 0.018:
                return MARBLE_VEIN
        # Alabaster veins — shallow to mid, warm sedimentary
        if 15 <= depth < 55 and biome in ("sedimentary", "temperate"):
            alab_n = self._vein_noise(bx, by, 0xE2B8C4, scale=6)
            if alab_n >= 0.64 and r < 0.013:
                return ALABASTER_VEIN
        # Verdite veins — mid to deep igneous zones; striking green
        if 60 <= depth < 140 and biome in ("igneous", "volcanic"):
            verd_n = self._vein_noise(bx, by, 0x3B8F5A, scale=5)
            if verd_n >= 0.65 and r < 0.010:
                return VERDITE_VEIN
        # Onyx veins — very deep igneous/volcanic; very rare
        if 130 <= depth and biome in ("igneous", "volcanic"):
            onyx_n = self._vein_noise(bx, by, 0x1F1A2E, scale=5)
            if onyx_n >= 0.67 and r < 0.007:
                return ONYX_VEIN
        # Limestone layers — shallow to mid depth in sedimentary zones
        if 4 <= depth < 55 and biome in ("sedimentary", "temperate", "igneous"):
            lime_n = self._vein_noise(bx, by, 0xA7E23, scale=7)
            if lime_n >= 0.57 and r < (0.05 if biome == "sedimentary" else 0.025):
                return LIMESTONE_DEPOSIT
        # Rock deposits — cluster in tight pockets (scale 4, threshold 0.58 → ~42% coverage, 2.4x density inside)
        if depth >= 15:
            rock_n = self._vein_noise(bx, by, 0x5A7E3, scale=4)
            if rock_n >= 0.58:
                base = 0.025 if depth >= 120 else 0.015 if depth >= 50 else 0.008
                if r < base * 2.4:
                    return ROCK_DEPOSIT
        # Fossil deposits — small groups (scale 4, threshold 0.62)
        if depth >= 50:
            fr = rng.random()
            fossil_n = self._vein_noise(bx, by, 0xF0551, scale=4)
            if fossil_n >= 0.62:
                base = 0.004 if depth >= 150 else 0.002 if depth >= 100 else 0.001
                if fr < base * 2.6:
                    return FOSSIL_DEPOSIT
        # Gem deposits — tiny pockets (scale 3, threshold 0.66)
        if depth >= 8:
            gr = rng.random()
            gem_n = self._vein_noise(bx, by, 0x6E534, scale=3)
            if gem_n >= 0.66:
                base = 0.0018 if depth >= 172 else 0.0012 if depth >= 100 else 0.0008 if depth >= 50 else 0.0004
                if gr < base * 2.9:
                    return GEM_DEPOSIT
        r = rng.random()  # fresh roll so deposit chance doesn't eat ore slots
        m = BIOME_ORE_MULTIPLIERS.get(biome, {})
        cm = m.get("coal", 1.0)
        im = m.get("iron", 1.0)
        gm = m.get("gold", 1.0)
        xm = m.get("crystal", 1.0)
        rm = m.get("ruby", 1.0)
        om = m.get("obsidian", 1.0)
        # Ore veins: each type has its own noise field (scale 6) so veins are type-specific and independent
        if depth < 40:
            coal_n = self._vein_noise(bx, by, 0x1C0A1, scale=6)
            iron_n = self._vein_noise(bx, by, 0x17EA4, scale=6)
            if coal_n >= 0.55 and r < 0.040 * cm * 2.2:
                self._ore_richness[(bx, by)] = 3 if coal_n >= 0.68 else 2 if coal_n >= 0.63 else 1
                return COAL_ORE
            if iron_n >= 0.55 and r < 0.060 * im * 2.2:
                self._ore_richness[(bx, by)] = 3 if iron_n >= 0.68 else 2 if iron_n >= 0.63 else 1
                return IRON_ORE
        elif depth < 100:
            iron_n = self._vein_noise(bx, by, 0x17EA4, scale=6)
            gold_n = self._vein_noise(bx, by, 0xC01D1, scale=6)
            coal_n = self._vein_noise(bx, by, 0x1C0A1, scale=6)
            if iron_n >= 0.55 and r < 0.030 * im * 2.2:
                self._ore_richness[(bx, by)] = 3 if iron_n >= 0.68 else 2 if iron_n >= 0.63 else 1
                return IRON_ORE
            if gold_n >= 0.55 and r < 0.055 * gm * 2.2:
                self._ore_richness[(bx, by)] = 3 if gold_n >= 0.68 else 2 if gold_n >= 0.63 else 1
                return GOLD_ORE
            if coal_n >= 0.55 and r < 0.065 * cm * 2.2:
                self._ore_richness[(bx, by)] = 3 if coal_n >= 0.68 else 2 if coal_n >= 0.63 else 1
                return COAL_ORE
        elif depth < 160:
            gold_n = self._vein_noise(bx, by, 0xC01D1, scale=6)
            crys_n = self._vein_noise(bx, by, 0xCE750, scale=6)
            ruby_n = self._vein_noise(bx, by, 0xB4E1D, scale=6)
            if gold_n >= 0.55 and r < 0.025 * gm * 2.2:
                self._ore_richness[(bx, by)] = 3 if gold_n >= 0.68 else 2 if gold_n >= 0.63 else 1
                return GOLD_ORE
            if crys_n >= 0.55 and r < 0.045 * xm * 2.2:
                self._ore_richness[(bx, by)] = 3 if crys_n >= 0.68 else 2 if crys_n >= 0.63 else 1
                return CRYSTAL_ORE
            if ruby_n >= 0.55 and r < 0.055 * rm * 2.2:
                self._ore_richness[(bx, by)] = 3 if ruby_n >= 0.68 else 2 if ruby_n >= 0.63 else 1
                return RUBY_ORE
        else:
            obsi_n = self._vein_noise(bx, by, 0x0B51D, scale=5)
            crys_n = self._vein_noise(bx, by, 0xCE750, scale=5)
            ruby_n = self._vein_noise(bx, by, 0xB4E1D, scale=5)
            if obsi_n >= 0.55 and r < 0.150 * om * 2.2: return OBSIDIAN
            if crys_n >= 0.55 and r < 0.180 * xm * 2.2:
                self._ore_richness[(bx, by)] = 3 if crys_n >= 0.68 else 2 if crys_n >= 0.63 else 1
                return CRYSTAL_ORE
            if ruby_n >= 0.55 and r < 0.195 * rm * 2.2:
                self._ore_richness[(bx, by)] = 3 if ruby_n >= 0.68 else 2 if ruby_n >= 0.63 else 1
                return RUBY_ORE
        return self._stone_for_depth(depth)

    def get_block(self, x, y):
        if y < 0 or y >= WORLD_H or abs(x) > WORLD_MAX_X:
            return BEDROCK
        cx = x // CHUNK_W
        chunk = self._chunks.get(cx)
        return chunk[y][x % CHUNK_W] if chunk is not None else BEDROCK

    def set_block(self, x, y, block_id):
        if y < 0 or y >= WORLD_H or abs(x) > WORLD_MAX_X:
            return
        cx = x // CHUNK_W
        chunk = self._chunks.get(cx)
        if chunk is None:
            return  # silently skip unloaded chunks
        old_bid = chunk[y][x % CHUNK_W]
        chunk[y][x % CHUNK_W] = block_id
        self._dirty_chunks.add(cx)
        if block_id == SAPLING or block_id in ALL_FRUIT_SAPLINGS:
            self.pending_saplings.add((x, y))
        elif old_bid == SAPLING or old_bid in ALL_FRUIT_SAPLINGS:
            self.pending_saplings.discard((x, y))
        # Fruit clusters live in the bg_block layer; clear them when their leaf is destroyed.
        if old_bid in LEAF_FRUIT_CLUSTER_MAP and block_id == AIR:
            self.set_bg_block(x, y, AIR)
            self.pending_fruit_leaves.discard((x, y))
        elif block_id in LEAF_FRUIT_CLUSTER_MAP:
            self.pending_fruit_leaves.add((x, y))
        elif old_bid in LEAF_FRUIT_CLUSTER_MAP and block_id not in LEAF_FRUIT_CLUSTER_MAP:
            self.pending_fruit_leaves.discard((x, y))
        if block_id in YOUNG_CROP_BLOCKS:
            self.pending_crops.add((x, y))
            if old_bid not in YOUNG_CROP_BLOCKS:
                # Fresh planting (incl. perennial regrowth from MATURE): reset progress.
                self._crop_progress[(x, y)] = 0
                self._crop_care_sum[(x, y)] = (0.0, 0)
                self._soil_fallow.pop((x, y), None)
        elif old_bid in YOUNG_CROP_BLOCKS:
            self.pending_crops.discard((x, y))
            # Progress stops mattering the moment the young stage ends.
            self._crop_progress.pop((x, y), None)
            # Preserve care_sum through maturation so harvest can read it; drop it
            # only when the crop is destroyed before maturing.
            if block_id not in MATURE_CROP_BLOCKS:
                self._crop_care_sum.pop((x, y), None)
        if old_bid == TILLED_SOIL and block_id != TILLED_SOIL:
            self._soil_moisture.pop((x, y), None)
            self._soil_fallow.pop((x, y), None)
        if old_bid in (WATER, FISHING_SPOT_BLOCK):
            self._water_level.pop((x, y), None)
        if block_id == AIR:
            for ddx, ddy in ((0, -1), (-1, 0), (1, 0)):
                nx, ny = x + ddx, y + ddy
                if 0 <= ny < WORLD_H:
                    nb = self._chunk_get(nx, ny)
                    if nb == WATER:
                        self._pending_water.add((nx, ny))
        elif old_bid in (DAM_BLOCK_CLOSED,) and block_id == DAM_BLOCK_OPEN:
            # DAM open: release water pooled above the dam
            for check_y in range(y - 1, max(0, y - 20), -1):
                if self._chunk_get(x, check_y) == WATER:
                    self._pending_water.add((x, check_y))
                elif self._chunk_get(x, check_y) != AIR:
                    break
        elif block_id != WATER:
            for ddx, ddy in ((-1, 0), (1, 0), (0, 1)):
                nx, ny = x + ddx, y + ddy
                if self._chunk_get(nx, ny) == WATER:
                    self._drain_unsustained_water(nx, ny)
        from blocks import LIGHT_TRAP_BLOCK as _LTB
        if block_id == _LTB:
            self.light_traps.setdefault((x, y), {"accumulated": []})
        elif old_bid == _LTB:
            self.light_traps.pop((x, y), None)

    def get_bg_block(self, x, y):
        if y < 0 or y >= WORLD_H or abs(x) > WORLD_MAX_X:
            return AIR
        chunk = self._bg_chunks.get(x // CHUNK_W)
        return chunk[y][x % CHUNK_W] if chunk is not None else AIR

    def set_bg_block(self, x, y, block_id):
        if y < 0 or y >= WORLD_H or abs(x) > WORLD_MAX_X:
            return
        cx = x // CHUNK_W
        if cx not in self._bg_chunks:
            self._bg_chunks[cx] = [[AIR] * CHUNK_W for _ in range(WORLD_H)]
        old = self._bg_chunks[cx][y][x % CHUNK_W]
        if old == GROW_LAMP:
            self._grow_lamps.discard((x, y))
        self._bg_chunks[cx][y][x % CHUNK_W] = block_id
        if block_id == GROW_LAMP:
            self._grow_lamps.add((x, y))
        self._dirty_bg_chunks.add(cx)

    def get_wire(self, x, y) -> int:
        if y < 0 or y >= WORLD_H or abs(x) > WORLD_MAX_X:
            return 0
        chunk = self._wire_chunks.get(x // CHUNK_W)
        return chunk[y][x % CHUNK_W] if chunk is not None else 0

    def set_wire(self, x, y, val: int):
        if y < 0 or y >= WORLD_H or abs(x) > WORLD_MAX_X:
            return
        cx = x // CHUNK_W
        if cx not in self._wire_chunks:
            self._wire_chunks[cx] = [[0] * CHUNK_W for _ in range(WORLD_H)]
        self._wire_chunks[cx][y][x % CHUNK_W] = val
        self._dirty_wire_chunks.add(cx)

    def toggle_wire_mode(self):
        self.wire_mode = not self.wire_mode

    def is_solid(self, x, y):
        bid = self.get_block(x, y)
        return (bid != AIR and bid != LADDER
                and bid != WATER and bid != FISHING_SPOT_BLOCK and bid != OIL and bid != SAPLING and bid not in ALL_FRUIT_SAPLINGS
                and bid != WILDFLOWER_PATCH
                and bid not in BUSH_BLOCKS and bid not in CROP_BLOCKS
                and bid not in OPEN_DOORS
                and bid not in ALL_LOGS and bid not in ALL_LEAVES
                and bid not in EQUIPMENT_BLOCKS
                and bid != MINE_TRACK_BLOCK and bid != MINE_TRACK_STOP_BLOCK
                and bid != ELEVATOR_CABLE_BLOCK)

    def update_time(self, dt):
        prev = self.time_of_day
        self.time_of_day = (self.time_of_day + dt) % CYCLE_DURATION
        if self.time_of_day < prev:
            self.day_count += 1
            from towns import advance_day
            advance_day(self)
            from outposts import tick_outpost_day
            tick_outpost_day(self.day_count)
            from player_cities import tick_city_day
            tick_city_day(self)
        self._tick_light_traps(dt)

    def _tick_light_traps(self, dt):
        if not self.light_traps:
            return
        is_night = self.time_of_day >= DAY_DURATION
        if not is_night:
            return
        self._light_trap_timer = getattr(self, "_light_trap_timer", 0.0) + dt
        if self._light_trap_timer < 20.0:
            return
        self._light_trap_timer = 0.0
        import random as _rnd
        from constants import BLOCK_SIZE as _BS
        for pos, trap in self.light_traps.items():
            if len(trap["accumulated"]) >= 4:
                continue
            tx = pos[0] * _BS
            ty = pos[1] * _BS
            candidates = [ins for ins in self.insects
                          if ins.NIGHT_ONLY
                          and abs(ins.x - tx) < 6 * _BS
                          and abs(ins.y - ty) < 6 * _BS
                          and ins.SPECIES not in trap["accumulated"]]
            if candidates:
                sp = _rnd.choice(candidates).SPECIES
                trap["accumulated"].append(sp)

    def _update_pumps(self):
        """When a pump block is on and adjacent to water, push water one tile upward."""
        from blocks import PUMP_BLOCK_ON as _PMP, WATER as _W, AIR as _A
        for (bx, by) in list(getattr(self, 'logic_state', {}).keys()):
            if self.get_block(bx, by) != _PMP:
                continue
            has_water = any(self.get_block(bx + dx, by + dy) == _W
                            for dx, dy in ((0, 1), (-1, 0), (1, 0)))
            if not has_water:
                continue
            target_y = by - 1
            if target_y >= 0 and self.get_block(bx, target_y) == _A:
                self.set_block(bx, target_y, _W)
                self._water_level[(bx, target_y)] = 7
                self._pending_water.add((bx, target_y))

    def update_irrigation(self, dt):
        """Passively moisten tilled soil near water sources."""
        from soil import MAX_MOISTURE as _MAXM
        from blocks import TILLED_SOIL as _TS, WATER as _W
        self._irr_timer = getattr(self, '_irr_timer', 0.0) + dt
        if self._irr_timer < 8.0:
            return
        self._irr_timer = 0.0
        for (wx, wy), level in list(self._water_level.items()):
            if level < 4:
                continue
            for dy in range(0, 4):
                for dx in range(-3, 4):
                    sx, sy = wx + dx, wy + dy
                    if self.get_block(sx, sy) == _TS:
                        cur = self._soil_moisture.get((sx, sy), 0)
                        if cur < _MAXM:
                            self._soil_moisture[(sx, sy)] = min(_MAXM, cur + 8)

    def update_water(self, dt, player):
        self._water_timer += dt
        if self._water_timer < self._water_interval:
            return
        self._water_timer -= self._water_interval
        self._update_pumps()

        if not self._pending_water:
            return

        # Process top-to-bottom: downward flow has priority
        to_process = sorted(self._pending_water, key=lambda p: p[1])
        self._pending_water.clear()

        new_water = set()
        spreads = 0
        max_spreads = 160

        for (x, y) in to_process:
            if self._chunk_get(x, y) != WATER:
                self._water_level.pop((x, y), None)
                continue
            level = self._water_level.get((x, y), 8)
            if spreads >= max_spreads:
                self._pending_water.add((x, y))
                continue

            below = y + 1
            if below < WORLD_H and self._chunk_get(x, below) == AIR:
                # Water FALLS: block moves down, leaving AIR behind.
                self._chunk_set(x, y, AIR)
                self._water_level.pop((x, y), None)
                self._chunk_set(x, below, WATER)
                self._water_level[(x, below)] = level
                new_water.add((x, below))
                for adx in (-1, 1):
                    anx = x + adx
                    if self._chunk_get(anx, y) == WATER:
                        new_water.add((anx, y))
                spreads += 1
                continue

            # Blocked below — spread sideways
            if level > 1:
                from blocks import IRRIGATION_CHANNEL_BLOCK as _ICB
                source_in_channel = self.get_bg_block(x, y) == _ICB
                for dx in (-1, 1):
                    nx = x + dx
                    if self._chunk_get(nx, y) == AIR:
                        dest_in_channel = self.get_bg_block(nx, y) == _ICB
                        spread_level = level if (source_in_channel and dest_in_channel) else level - 1
                        if spread_level > 0:
                            self._chunk_set(nx, y, WATER)
                            self._water_level[(nx, y)] = spread_level
                            new_water.add((nx, y))
                            spreads += 1

        self._pending_water.update(new_water)

    def _drain_unsustained_water(self, start_x, start_y):
        """Drain water tiles that can no longer be fed after a block was placed nearby."""
        queue = [(start_x, start_y)]
        seen = set()
        while queue:
            x, y = queue.pop()
            if (x, y) in seen:
                continue
            seen.add((x, y))
            if self._chunk_get(x, y) != WATER:
                continue
            level = self._water_level.get((x, y), 8)
            if level == 8:
                continue  # never drain world-gen source blocks
            # Sustained if a horizontal neighbor can supply it (level >= this+1)
            # or a water tile above can fall into it (level >= this).
            sustained = False
            for dx in (-1, 1):
                if self._chunk_get(x + dx, y) == WATER:
                    if self._water_level.get((x + dx, y), 8) >= level + 1:
                        sustained = True
                        break
            if not sustained and y > 0 and self._chunk_get(x, y - 1) == WATER:
                if self._water_level.get((x, y - 1), 8) >= level:
                    sustained = True
            if sustained:
                continue
            self._chunk_set(x, y, AIR)
            self._water_level.pop((x, y), None)
            for dx in (-1, 1):
                if self._chunk_get(x + dx, y) == WATER:
                    queue.append((x + dx, y))
            if y + 1 < WORLD_H and self._chunk_get(x, y + 1) == WATER:
                queue.append((x, y + 1))

    def _has_sky_view(self, x, y):
        _transparent = BUSH_BLOCKS | CROP_BLOCKS | {SAPLING} | ALL_FRUIT_SAPLINGS
        for check_y in range(y - 1, -1, -1):
            bid = self.get_block(x, check_y)
            if bid != AIR and bid not in _transparent:
                return False
        return True

    _LAMP_H_RADIUS = 8   # tiles left/right a grow lamp reaches
    _LAMP_V_RANGE  = 12  # max tiles above the crop a lamp can sit

    def _has_grow_light(self, x, y):
        for lx, ly in self._grow_lamps:
            if abs(lx - x) <= self._LAMP_H_RADIUS and (y - self._LAMP_V_RANGE) <= ly < y:
                return True
        return False

    def _place_canopy(self, layers, leaf_bid, rng=None, density=1.0):
        for ly, lx_range in layers:
            if ly < 0 or ly >= WORLD_H:
                continue
            for lx in lx_range:
                if self.get_block(lx, ly) == AIR:
                    if rng is None or density >= 1.0 or rng.random() < density:
                        self.set_block(lx, ly, leaf_bid)

    def _scatter_fruit_clusters(self, layers, leaf_bid, rng, chance=0.25):
        """Place fruit cluster bg_blocks on a fraction of freshly placed leaf_bid tiles."""
        fruit_bid = LEAF_FRUIT_CLUSTER_MAP.get(leaf_bid)
        if fruit_bid is None:
            return
        for ly, lx_range in layers:
            if ly < 0 or ly >= WORLD_H:
                continue
            for lx in lx_range:
                if self.get_block(lx, ly) == leaf_bid and rng.random() < chance:
                    self.set_bg_block(lx, ly, fruit_bid)

    def _add_branch_stubs(self, bx, by, h, log_bid, rng, count=2):
        used = set()
        for _ in range(count):
            for _ in range(8):
                branch_y = by - rng.randint(max(1, h // 3), h - 1)
                if branch_y in used:
                    continue
                used.add(branch_y)
                side = rng.choice([-1, 1])
                for dx in range(1, rng.randint(1, 3)):
                    bx2 = bx + side * dx
                    if 0 <= branch_y < WORLD_H:
                        if self.get_block(bx2, branch_y) == AIR:
                            self.set_block(bx2, branch_y, log_bid)
                break

    def _add_root_flare(self, bx, by, log_bid, rng):
        for side in [-1, 1]:
            if rng.random() < 0.65:
                rx = bx + side
                if self.get_block(rx, by) == AIR:
                    self.set_block(rx, by, log_bid)

    def _place_trunk(self, bx, by, h, log_bid):
        for i in range(h):
            ly = by - i
            if 0 <= ly < self.height:
                self.set_block(bx, ly, log_bid)
        return by - (h - 1)  # returns top_y

    def _grow_oak(self, bx, by, rng=None):
        rng = rng or self._sapling_rng
        h = rng.randint(3, 6)
        top_y = self._place_trunk(bx, by, h, TREE_LOG)
        self._place_canopy([
            (top_y - 1, range(bx - 1, bx + 2)),
            (top_y,     range(bx - 2, bx + 3)),
            (top_y + 1, range(bx - 2, bx + 3)),
        ], TREE_LEAVES, rng, density=0.85)
        self._add_branch_stubs(bx, by, h, TREE_LOG, rng, count=rng.randint(1, 2))

    def _grow_pine(self, bx, by, rng=None):
        rng = rng or self._sapling_rng
        h = rng.randint(5, 9)
        top_y = self._place_trunk(bx, by, h, PINE_LOG)
        # Wider base when taller
        extra = 1 if h >= 8 else 0
        self._place_canopy([
            (top_y,         range(bx, bx + 1)),
            (top_y + 1,     range(bx - 1, bx + 2)),
            (top_y + 2,     range(bx - 2, bx + 3)),
            (top_y + 3,     range(bx - 1 - extra, bx + 2 + extra)),
        ], PINE_LEAVES, rng, density=0.92)

    def _grow_birch(self, bx, by, rng=None):
        rng = rng or self._sapling_rng
        h = rng.randint(4, 7)
        top_y = self._place_trunk(bx, by, h, BIRCH_LOG)
        self._place_canopy([
            (top_y - 1, range(bx - 1, bx + 2)),
            (top_y,     range(bx - 2, bx + 3)),
            (top_y + 1, range(bx - 2, bx + 3)),
            (top_y + 2, range(bx - 1, bx + 2)),
        ], BIRCH_LEAVES, rng, density=0.80)
        if rng.random() < 0.55:
            self._add_branch_stubs(bx, by, h, BIRCH_LOG, rng, count=1)

    def _grow_jungle(self, bx, by, rng=None):
        rng = rng or self._sapling_rng
        h = rng.randint(7, 11)
        top_y = self._place_trunk(bx, by, h, JUNGLE_LOG)
        self._place_canopy([
            (top_y - 1, range(bx - 1, bx + 2)),
            (top_y,     range(bx - 3, bx + 4)),
            (top_y + 1, range(bx - 4, bx + 5)),
            (top_y + 2, range(bx - 3, bx + 4)),
            (top_y + 3, range(bx - 2, bx + 3)),
        ], JUNGLE_LEAVES, rng, density=0.72)
        # Hanging vines below canopy
        for lx in range(bx - 4, bx + 5):
            if rng.random() < 0.38:
                vine_y = top_y + 4
                if 0 <= vine_y < WORLD_H:
                    if self.get_block(lx, vine_y) == AIR:
                        self.set_block(lx, vine_y, JUNGLE_LEAVES)
                        # Occasionally a second vine block below
                        if rng.random() < 0.4 and vine_y + 1 < WORLD_H:
                            if self.get_block(lx, vine_y + 1) == AIR:
                                self.set_block(lx, vine_y + 1, JUNGLE_LEAVES)
        self._add_branch_stubs(bx, by, h, JUNGLE_LOG, rng, count=rng.randint(2, 3))
        self._add_root_flare(bx, by, JUNGLE_LOG, rng)

    def _grow_willow(self, bx, by, rng=None):
        rng = rng or self._sapling_rng
        h = rng.randint(4, 7)
        top_y = self._place_trunk(bx, by, h, WILLOW_LOG)
        self._place_canopy([
            (top_y - 1, range(bx - 2, bx + 3)),
            (top_y,     range(bx - 3, bx + 4)),
            (top_y + 1, range(bx - 4, bx + 5)),
            (top_y + 2, range(bx - 4, bx + 5)),
            (top_y + 3, range(bx - 3, bx + 4)),
        ], WILLOW_LEAVES, rng, density=0.82)
        # Hanging curtain strands
        for lx in range(bx - 4, bx + 5):
            if rng.random() < 0.60:
                dangle = rng.randint(1, 4)
                for dy in range(1, dangle + 1):
                    hy = top_y + 3 + dy
                    if 0 <= hy < WORLD_H:
                        if self.get_block(lx, hy) == AIR:
                            self.set_block(lx, hy, WILLOW_LEAVES)
        self._add_branch_stubs(bx, by, h, WILLOW_LOG, rng, count=1)

    def _grow_redwood(self, bx, by, rng=None):
        rng = rng or self._sapling_rng
        h = rng.randint(9, 14)
        top_y = self._place_trunk(bx, by, h, REDWOOD_LOG)
        self._place_canopy([
            (top_y,     range(bx, bx + 1)),
            (top_y + 1, range(bx - 1, bx + 2)),
            (top_y + 2, range(bx - 2, bx + 3)),
            (top_y + 3, range(bx - 1, bx + 2)),
            (top_y + 4, range(bx - 2, bx + 3)),
            (top_y + 5, range(bx - 1, bx + 2)),
        ], REDWOOD_LEAVES, rng, density=0.88)
        self._add_root_flare(bx, by, REDWOOD_LOG, rng)

    def _grow_palm(self, bx, by, rng=None):
        rng = rng or self._sapling_rng
        h = rng.randint(6, 10)
        # Slight lean — offset trunk top by 0 or 1
        lean = rng.choice([-1, 0, 0, 1])
        top_y = self._place_trunk(bx, by, h, PALM_LOG)
        cx = bx + lean
        self._place_canopy([
            (top_y - 1, range(cx - 1, cx + 2)),
            (top_y,     range(cx - 3, cx + 4)),
            (top_y + 1, range(cx - 2, cx + 3)),
        ], PALM_LEAVES, rng, density=1.0)
        # Crown tip
        if 0 <= top_y - 2 < WORLD_H and self.get_block(cx, top_y - 2) == AIR:
            self.set_block(cx, top_y - 2, PALM_LEAVES)

    def _grow_acacia(self, bx, by, rng=None):
        rng = rng or self._sapling_rng
        h = rng.randint(3, 5)
        top_y = self._place_trunk(bx, by, h, ACACIA_LOG)
        # Offset canopy centre simulates the characteristic acacia lean
        off = rng.randint(-1, 1)
        self._place_canopy([
            (top_y - 1, range(bx + off - 1, bx + off + 2)),
            (top_y,     range(bx + off - 3, bx + off + 4)),
            (top_y + 1, range(bx + off - 3, bx + off + 4)),
        ], ACACIA_LEAVES, rng, density=0.73)

    def _grow_dead(self, bx, by, rng=None):
        rng = rng or self._sapling_rng
        h = rng.randint(4, 8)
        top_y = self._place_trunk(bx, by, h, DEAD_LOG)
        mid_y = by - h // 2
        # Randomised branch set — 60-80% of candidates placed
        candidates = [
            (bx - 2, mid_y), (bx + 2, mid_y),
            (bx - 1, mid_y - 1), (bx + 1, mid_y - 1),
            (bx - 3, mid_y + 1), (bx + 3, mid_y + 1),
            (bx - 1, top_y + 1), (bx + 1, top_y + 1),
            (bx - 2, top_y + 2), (bx + 2, top_y + 2),
        ]
        for tx, ty in candidates:
            if rng.random() < 0.65 and 0 <= ty < WORLD_H:
                if self.get_block(tx, ty) == AIR:
                    self.set_block(tx, ty, DEAD_LOG)

    def _grow_mushroom(self, bx, by, rng=None):
        rng = rng or self._sapling_rng
        h = rng.randint(2, 5)
        top_y = self._place_trunk(bx, by, h, MUSHROOM_STEM)
        cap_w = rng.randint(2, 4)
        self._place_canopy([
            (top_y - 1, range(bx - 1, bx + 2)),
            (top_y,     range(bx - cap_w, bx + cap_w + 1)),
            (top_y + 1, range(bx - cap_w, bx + cap_w + 1)),
        ], MUSHROOM_CAP, rng, density=0.92)

    def _grow_maple(self, bx, by, rng=None):
        rng = rng or self._sapling_rng
        h = rng.randint(4, 7)
        top_y = self._place_trunk(bx, by, h, MAPLE_LOG)
        self._place_canopy([
            (top_y - 2, range(bx - 1, bx + 2)),
            (top_y - 1, range(bx - 2, bx + 3)),
            (top_y,     range(bx - 3, bx + 4)),
            (top_y + 1, range(bx - 3, bx + 4)),
            (top_y + 2, range(bx - 2, bx + 3)),
        ], MAPLE_LEAVES, rng, density=0.82)
        self._add_branch_stubs(bx, by, h, MAPLE_LOG, rng, count=rng.randint(1, 3))
        if rng.random() < 0.5:
            self._add_root_flare(bx, by, MAPLE_LOG, rng)

    def _grow_cherry(self, bx, by, rng=None):
        rng = rng or self._sapling_rng
        h = rng.randint(3, 5)
        top_y = self._place_trunk(bx, by, h, CHERRY_LOG)
        off = rng.randint(-1, 1)
        self._place_canopy([
            (top_y - 1, range(bx + off - 1, bx + off + 2)),
            (top_y,     range(bx + off - 2, bx + off + 3)),
            (top_y + 1, range(bx + off - 2, bx + off + 3)),
            (top_y + 2, range(bx + off - 1, bx + off + 2)),
        ], CHERRY_LEAVES, rng, density=0.78)
        if rng.random() < 0.4:
            self._add_branch_stubs(bx, by, h, CHERRY_LOG, rng, count=1)

    def _grow_cypress(self, bx, by, rng=None):
        rng = rng or self._sapling_rng
        h = rng.randint(8, 13)
        top_y = self._place_trunk(bx, by, h, CYPRESS_LOG)
        # Tight columnar canopy — narrow throughout, slightly wider near base
        layers = [(top_y, range(bx, bx + 1))]  # bare pointed tip
        for i in range(1, h):
            w = 2 if i >= h - 2 else 1
            layers.append((top_y + i, range(bx - w, bx + w + 1)))
        self._place_canopy(layers, CYPRESS_LEAVES, rng, density=0.93)

    def _grow_baobab(self, bx, by, rng=None):
        rng = rng or self._sapling_rng
        h = rng.randint(3, 5)
        top_y = self._place_trunk(bx, by, h, BAOBAB_LOG)
        # Fat trunk — widen the bottom two rows
        for i in range(min(2, h)):
            ty = by - i
            if 0 <= ty < WORLD_H:
                for dx in (-1, 1):
                    if self.get_block(bx + dx, ty) == AIR:
                        self.set_block(bx + dx, ty, BAOBAB_LOG)
        # Small sparse crown offset slightly for character
        off = rng.randint(-1, 1)
        self._place_canopy([
            (top_y - 1, range(bx + off - 2, bx + off + 3)),
            (top_y,     range(bx + off - 3, bx + off + 4)),
            (top_y + 1, range(bx + off - 2, bx + off + 3)),
        ], BAOBAB_LEAVES, rng, density=0.55)

    def _grow_mangrove(self, bx, by, rng=None):
        rng = rng or self._sapling_rng
        h = rng.randint(4, 7)
        top_y = self._place_trunk(bx, by, h, MANGROVE_LOG)
        self._place_canopy([
            (top_y - 1, range(bx - 1, bx + 2)),
            (top_y,     range(bx - 3, bx + 4)),
            (top_y + 1, range(bx - 3, bx + 4)),
            (top_y + 2, range(bx - 2, bx + 3)),
        ], MANGROVE_LEAVES, rng, density=0.80)
        # Prop roots arching out from mid-trunk
        mid_y = by - h // 3
        for dx, angle in [(-2, 1), (-1, 2), (1, 2), (2, 1)]:
            if rng.random() < 0.75:
                rx = bx + dx
                ry = mid_y + angle
                if 0 <= ry < WORLD_H and self.get_block(rx, ry) == AIR:
                    self.set_block(rx, ry, MANGROVE_LOG)
                if 0 <= ry + 1 < WORLD_H and self.get_block(rx, ry + 1) == AIR:
                    self.set_block(rx, ry + 1, MANGROVE_LOG)

    def _grow_spruce(self, bx, by, rng=None):
        rng = rng or self._sapling_rng
        h = rng.randint(6, 10)
        top_y = self._place_trunk(bx, by, h, SPRUCE_LOG)
        # Very tight conical canopy, narrower than pine
        layers = [(top_y, range(bx, bx + 1))]
        for i in range(1, h):
            w = min(2, (i + 1) // 3)
            layers.append((top_y + i, range(bx - w, bx + w + 1)))
        self._place_canopy(layers, SPRUCE_LEAVES, rng, density=0.95)

    def _grow_ginkgo(self, bx, by, rng=None):
        rng = rng or self._sapling_rng
        h = rng.randint(5, 8)
        top_y = self._place_trunk(bx, by, h, GINKGO_LOG)
        # Wide fan-shaped crown — broad and flat at top
        self._place_canopy([
            (top_y - 1, range(bx - 1, bx + 2)),
            (top_y,     range(bx - 3, bx + 4)),
            (top_y + 1, range(bx - 4, bx + 5)),
            (top_y + 2, range(bx - 4, bx + 5)),
            (top_y + 3, range(bx - 3, bx + 4)),
        ], GINKGO_LEAVES, rng, density=0.78)
        self._add_branch_stubs(bx, by, h, GINKGO_LOG, rng, count=rng.randint(2, 3))

    def _grow_banyan(self, bx, by, rng=None):
        rng = rng or self._sapling_rng
        h = rng.randint(5, 9)
        top_y = self._place_trunk(bx, by, h, BANYAN_LOG)
        self._place_canopy([
            (top_y - 1, range(bx - 2, bx + 3)),
            (top_y,     range(bx - 4, bx + 5)),
            (top_y + 1, range(bx - 5, bx + 6)),
            (top_y + 2, range(bx - 4, bx + 5)),
            (top_y + 3, range(bx - 2, bx + 3)),
        ], BANYAN_LEAVES, rng, density=0.72)
        # Aerial roots hanging from canopy underside
        for lx in range(bx - 4, bx + 5):
            if rng.random() < 0.45:
                for dy in range(1, rng.randint(2, 5)):
                    ry = top_y + 3 + dy
                    if 0 <= ry < WORLD_H and self.get_block(lx, ry) == AIR:
                        self.set_block(lx, ry, BANYAN_LOG)
        self._add_root_flare(bx, by, BANYAN_LOG, rng)

    def _grow_pear(self, bx, by, rng=None):
        rng = rng or self._sapling_rng
        h = rng.randint(3, 6)
        top_y = self._place_trunk(bx, by, h, PEAR_LOG)
        layers = [
            (top_y - 1, range(bx - 1, bx + 2)),
            (top_y,     range(bx - 2, bx + 3)),
            (top_y + 1, range(bx - 2, bx + 3)),
            (top_y + 2, range(bx - 1, bx + 2)),
        ]
        self._place_canopy(layers, PEAR_LEAVES, rng, density=0.85)
        self._scatter_fruit_clusters(layers, PEAR_LEAVES, rng, chance=0.25)
        if rng.random() < 0.5:
            self._add_branch_stubs(bx, by, h, PEAR_LOG, rng, count=1)

    def _grow_fig(self, bx, by, rng=None):
        rng = rng or self._sapling_rng
        h = rng.randint(3, 6)
        top_y = self._place_trunk(bx, by, h, FIG_LOG)
        off = rng.randint(-1, 1)
        layers = [
            (top_y - 1, range(bx + off - 1, bx + off + 2)),
            (top_y,     range(bx + off - 3, bx + off + 4)),
            (top_y + 1, range(bx + off - 3, bx + off + 4)),
            (top_y + 2, range(bx + off - 2, bx + off + 3)),
        ]
        self._place_canopy(layers, FIG_LEAVES, rng, density=0.75)
        self._scatter_fruit_clusters(layers, FIG_LEAVES, rng, chance=0.25)
        self._add_branch_stubs(bx, by, h, FIG_LOG, rng, count=rng.randint(1, 2))

    def _grow_citrus(self, bx, by, rng=None):
        rng = rng or self._sapling_rng
        h = rng.randint(3, 5)
        top_y = self._place_trunk(bx, by, h, CITRUS_LOG)
        layers = [
            (top_y - 1, range(bx - 1, bx + 2)),
            (top_y,     range(bx - 2, bx + 3)),
            (top_y + 1, range(bx - 2, bx + 3)),
            (top_y + 2, range(bx - 1, bx + 2)),
        ]
        self._place_canopy(layers, CITRUS_LEAVES, rng, density=0.90)
        self._scatter_fruit_clusters(layers, CITRUS_LEAVES, rng, chance=0.25)

    def _grow_apple(self, bx, by, rng=None):
        rng = rng or self._sapling_rng
        h = rng.randint(3, 6)
        top_y = self._place_trunk(bx, by, h, APPLE_LOG)
        layers = [
            (top_y - 1, range(bx - 1, bx + 2)),
            (top_y,     range(bx - 2, bx + 3)),
            (top_y + 1, range(bx - 2, bx + 3)),
            (top_y + 2, range(bx - 1, bx + 2)),
        ]
        self._place_canopy(layers, APPLE_LEAVES, rng, density=0.88)
        self._scatter_fruit_clusters(layers, APPLE_LEAVES, rng, chance=0.25)
        if rng.random() < 0.5:
            self._add_branch_stubs(bx, by, h, APPLE_LOG, rng, count=1)

    def _grow_pomegranate(self, bx, by, rng=None):
        rng = rng or self._sapling_rng
        h = rng.randint(3, 5)
        top_y = self._place_trunk(bx, by, h, POMEGRANATE_LOG)
        off = rng.randint(-1, 1)
        layers = [
            (top_y - 1, range(bx + off - 1, bx + off + 2)),
            (top_y,     range(bx + off - 2, bx + off + 3)),
            (top_y + 1, range(bx + off - 2, bx + off + 3)),
            (top_y + 2, range(bx + off - 1, bx + off + 2)),
        ]
        self._place_canopy(layers, POMEGRANATE_LEAVES, rng, density=0.82)
        self._scatter_fruit_clusters(layers, POMEGRANATE_LEAVES, rng, chance=0.25)

    def _dispatch_grow(self, bx, by, biodome, rng=None):
        rng = rng or self._sapling_rng
        options = {
            # temperate: orchard fruit trees common alongside oak/maple
            "temperate":       [(self._grow_oak, 4),    (self._grow_maple, 3),   (self._grow_cherry, 1),
                                (self._grow_pear, 2),   (self._grow_apple, 2),   (self._grow_ginkgo, 1)],
            # rolling_hills: best orchard biome — apple, pear, pomegranate all common
            "rolling_hills":   [(self._grow_oak, 3),    (self._grow_maple, 2),   (self._grow_cherry, 1),
                                (self._grow_pear, 2),   (self._grow_apple, 2),   (self._grow_pomegranate, 2),
                                (self._grow_fig, 1),    (self._grow_ginkgo, 1)],
            # birch_forest: apple and pear appear as scattered orchard remnants
            "birch_forest":    [(self._grow_birch, 6),  (self._grow_maple, 2),   (self._grow_oak, 1),
                                (self._grow_apple, 1),  (self._grow_pear, 1),    (self._grow_ginkgo, 1)],
            # steep_hills: apple and pear on hillside terraces
            "steep_hills":     [(self._grow_birch, 5),  (self._grow_maple, 3),   (self._grow_apple, 1),
                                (self._grow_pear, 1),   (self._grow_ginkgo, 1)],
            "boreal":          [(self._grow_pine, 5),   (self._grow_spruce, 3),  (self._grow_birch, 2)],
            "alpine_mountain": [(self._grow_pine, 6),   (self._grow_spruce, 4),  (self._grow_cypress, 1)],
            "rocky_mountain":  [(self._grow_pine, 5),   (self._grow_spruce, 3),  (self._grow_cypress, 2)],
            # jungle: citrus and fig grow in humid understory alongside jungle/banyan
            "jungle":          [(self._grow_jungle, 5), (self._grow_banyan, 3),  (self._grow_citrus, 1),
                                (self._grow_fig, 1)],
            "wetland":         [(self._grow_willow, 4), (self._grow_cypress, 3), (self._grow_mangrove, 3)],
            "swamp":           [(self._grow_willow, 3), (self._grow_cypress, 3), (self._grow_mangrove, 4)],
            "redwood":         [(self._grow_redwood, 8),(self._grow_birch, 1),   (self._grow_pine, 1)],
            # tropical: citrus very common; banyan and palm fill the rest
            "tropical":        [(self._grow_palm, 3),   (self._grow_banyan, 3),  (self._grow_citrus, 4)],
            # savanna: fig and pomegranate both drought-tolerant
            "savanna":         [(self._grow_acacia, 5), (self._grow_baobab, 3),  (self._grow_fig, 2),
                                (self._grow_pomegranate, 2)],
            # steppe: pomegranate and fig are the main fruit trees of semi-arid scrub
            "steppe":          [(self._grow_acacia, 3), (self._grow_baobab, 2),  (self._grow_fig, 3),
                                (self._grow_pomegranate, 3)],
            # canyon: pomegranate and fig survive the dry heat; citrus in shaded slots
            "canyon":          [(self._grow_dead, 4),   (self._grow_pomegranate, 2), (self._grow_fig, 1),
                                (self._grow_citrus, 1)],
            "wasteland":       [(self._grow_dead, 1)],
            "arid_steppe":     [(self._grow_dead, 1)],
            "desert":          [(self._grow_dead, 1)],
            "tundra":          [(self._grow_pine, 1)],
            # beach/coastal: palms and mangroves along the shore
            "beach":           [(self._grow_palm, 4),   (self._grow_mangrove, 3),(self._grow_citrus, 3)],
            "coastal":         [(self._grow_palm, 4),   (self._grow_mangrove, 3),(self._grow_citrus, 3)],
            "pacific_island":  [(self._grow_palm, 4),   (self._grow_mangrove, 2),(self._grow_citrus, 3),
                                (self._grow_banyan, 2)],
            "fungal":          [(self._grow_mushroom, 1)],
        }.get(biodome, [(self._grow_oak, 1)])
        fns, wts = zip(*options)
        rng.choices(fns, weights=wts)[0](bx, by, rng)

    def _grow_tree(self, bx, by):
        bid = self.get_block(bx, by)
        fruit_map = {
            APPLE_SAPLING:       self._grow_apple,
            PEAR_SAPLING:        self._grow_pear,
            FIG_SAPLING:         self._grow_fig,
            CITRUS_SAPLING:      self._grow_citrus,
            POMEGRANATE_SAPLING: self._grow_pomegranate,
        }
        if bid in fruit_map:
            fruit_map[bid](bx, by)
        else:
            biodome = self.get_biodome(bx)
            self._dispatch_grow(bx, by, biodome)

    def update_saplings(self, dt):
        self._sapling_timer += dt
        if self._sapling_timer < self._sapling_interval:
            return
        self._sapling_timer -= self._sapling_interval

        city_zones = getattr(self, 'city_zones', [])
        to_check = list(self.pending_saplings)
        still_pending = set()
        for (x, y) in to_check:
            bid = self.get_block(x, y)
            if bid != SAPLING and bid not in ALL_FRUIT_SAPLINGS:
                continue
            # Saplings inside a city should never grow into trees
            if any(lo <= x <= hi for lo, hi in city_zones):
                still_pending.add((x, y))
                continue
            # Must be on solid ground
            if y + 1 >= self.height or self.get_block(x, y + 1) == AIR:
                still_pending.add((x, y))
                continue
            # Must have unobstructed sky view
            if not self._has_sky_view(x, y):
                still_pending.add((x, y))
                continue
            # 10% chance per 30s tick (~5 min average, range ~3-6 min)
            if self._sapling_rng.random() < 0.10:
                self._grow_tree(x, y)
            else:
                still_pending.add((x, y))
        self.pending_saplings = still_pending

    def update_crops(self, dt):
        self._crop_timer += dt
        if self._crop_timer < self._crop_interval:
            return
        self._crop_timer -= self._crop_interval

        to_check = list(self.pending_crops)
        still_pending = set()
        for (x, y) in to_check:
            bid = self._chunk_get(x, y)
            if bid not in YOUNG_CROP_BLOCKS:
                continue
            if y + 1 >= WORLD_H:
                still_pending.add((x, y))
                continue
            below = self.get_block(x, y + 1)
            # Wild desert plants grow on SAND without tilled soil.
            if bid in WILD_DESERT_PLANT_BLOCKS and below == SAND:
                if not self._has_sky_view(x, y) and not self._has_grow_light(x, y):
                    still_pending.add((x, y))
                    continue
                delta = max(1, int(_soil.GROWTH_DELTA_MAX * _soil.DESERT_GROWTH_SPEED))
            else:
                # Crops require tilled soil underneath. Existing old-save crops on
                # plain dirt/grass simply stall until the player re-tills.
                if below != TILLED_SOIL:
                    still_pending.add((x, y))
                    continue
                if not self._has_sky_view(x, y) and not self._has_grow_light(x, y):
                    still_pending.add((x, y))
                    continue
                moisture  = self._soil_moisture.get((x, y + 1), 0)
                fertility = self._soil_fertility.get((x, y + 1), self.max_fertility)
                prefs     = _soil.get_prefs(bid)
                delta     = _soil.growth_delta(prefs, moisture, fertility)
                # Record care quality for yield scaling at harvest, even if delta is 0.
                care = _soil.care_score(prefs, moisture, fertility)
                csum, ccount = self._crop_care_sum.get((x, y), (0.0, 0))
                self._crop_care_sum[(x, y)] = (csum + care, ccount + 1)
                if delta <= 0:
                    still_pending.add((x, y))
                    continue
            # Pollination bonus: nearby non-spooked insects boost growth
            player = getattr(self, '_player_ref', None)
            poll_mult = getattr(player, 'insect_pollination_mult', 1.1)
            if any(abs(ins.x / BLOCK_SIZE - x) < 6 and abs(ins.y / BLOCK_SIZE - y) < 4
                   for ins in self.insects if not ins.spooked):
                delta *= poll_mult
            progress = self._crop_progress.get((x, y), 0) + delta
            if progress >= _soil.GROWTH_PROGRESS_MAX:
                if bid not in WILD_DESERT_PLANT_BLOCKS or below != SAND:
                    # Drain fertility from soil on maturation (not for wild sand plants)
                    fert = self._soil_fertility.get((x, y + 1), self.max_fertility)
                    drain = prefs.get("fertility_drain", _soil.FERTILITY_DRAIN_PER_HARVEST)
                    self._soil_fertility[(x, y + 1)] = max(0, fert - drain)
                self.set_block(x, y, _CROP_MATURE_MAP[bid])
            else:
                self._crop_progress[(x, y)] = progress
                still_pending.add((x, y))
        self.pending_crops = still_pending

    def update_fruit_trees(self, dt):
        """Slowly regrow fruit clusters on bare fruit-tree leaf blocks."""
        self._fruit_timer += dt
        if self._fruit_timer < self._fruit_interval:
            return
        self._fruit_timer -= self._fruit_interval

        candidates = list(self.pending_fruit_leaves)
        self._fruit_rng.shuffle(candidates)
        # Process up to 60 candidates per tick to keep it cheap
        for (x, y) in candidates[:60]:
            bid = self._chunk_get(x, y)
            if bid not in LEAF_FRUIT_CLUSTER_MAP:
                self.pending_fruit_leaves.discard((x, y))
                continue
            if self.get_bg_block(x, y) in ALL_FRUIT_CLUSTERS:
                self.pending_fruit_leaves.discard((x, y))
                continue
            if self._fruit_rng.random() < 0.15:
                self.set_bg_block(x, y, LEAF_FRUIT_CLUSTER_MAP[bid])
                self.pending_fruit_leaves.discard((x, y))

    def update_soil(self, dt):
        """Per-tick moisture decay, water-adjacency top-up, rain events, and fallow cleanup."""
        self._update_rain(dt)

        self._soil_timer += dt
        if self._soil_timer < self._soil_interval:
            return
        self._soil_timer -= self._soil_interval

        if not self._soil_moisture:
            return

        # During rain: all sky-exposed tilled tiles fill to max moisture.
        if self._rain_active:
            for (x, y) in list(self._soil_moisture.keys()):
                if self._has_sky_view(x, y):
                    self._soil_moisture[(x, y)] = _soil.MAX_MOISTURE

        # Snapshot keys so we can mutate safely inside the loop.
        to_revert = []
        for (x, y), moisture in list(self._soil_moisture.items()):
            # Sanity: tile may have changed out from under us.
            if self.get_block(x, y) != TILLED_SOIL:
                to_revert.append((x, y))
                continue
            # Natural irrigation: adjacent water keeps soil at least modestly wet.
            if self._adjacent_to_water(x, y):
                if moisture < _soil.WATER_ADJACENT_FLOOR:
                    moisture = _soil.WATER_ADJACENT_FLOOR
            elif moisture > 0 and self._soil_rng.random() < self.moisture_decay_chance:
                moisture -= 1
            self._soil_moisture[(x, y)] = moisture
            # Fallow tracking: tilled tile with no crop above → revert after a while.
            above = self.get_block(x, y - 1) if y > 0 else AIR
            if above in YOUNG_CROP_BLOCKS or above in MATURE_CROP_BLOCKS:
                self._soil_fallow.pop((x, y), None)
            else:
                self._soil_fallow[(x, y)] = self._soil_fallow.get((x, y), 0) + 1
                if self._soil_fallow[(x, y)] >= _soil.REVERT_AFTER_FALLOW_TICKS:
                    to_revert.append((x, y))

        for (x, y) in to_revert:
            # Only flip tiles that are still tilled; leave the rest alone.
            if self.get_block(x, y) == TILLED_SOIL:
                self.set_block(x, y, DIRT)
            else:
                self._soil_moisture.pop((x, y), None)
                self._soil_fallow.pop((x, y), None)

    def _adjacent_to_water(self, x, y):
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            if self.get_block(x + dx, y + dy) == WATER:
                return True
        return False

    def _update_rain(self, dt):
        self._rain_timer += dt
        if self._rain_active:
            if self._rain_timer >= self._rain_duration:
                self._rain_active = False
                self._rain_timer  = 0.0
                self._rain_gap    = self._soil_rng.uniform(
                    _soil.RAIN_MIN_GAP_SECS, _soil.RAIN_MAX_GAP_SECS)
        else:
            if self._rain_timer >= self._rain_gap:
                self._rain_active   = True
                self._rain_timer    = 0.0
                self._rain_duration = self._soil_rng.uniform(
                    _soil.RAIN_DURATION_MIN_SECS, _soil.RAIN_DURATION_MAX_SECS)

    def update_compost_bins(self, dt):
        """Advance composting progress; produce compost items when threshold reached."""
        import soil as _s
        for pos, bin_data in self.compost_bin_data.items():
            total = sum(bin_data["input"].values())
            if total < _s.COMPOST_INPUT_PER_OUTPUT:
                continue
            prev = bin_data["progress"]
            bin_data["progress"] += _s.COMPOST_PROGRESS_PER_SEC * dt
            if int(prev) != int(bin_data["progress"]):
                print(f"[Compost] {pos}: progress={bin_data['progress']:.0f}/{_s.COMPOST_OUTPUT_THRESHOLD:.0f} items={bin_data['input']}")
            if bin_data["progress"] >= _s.COMPOST_OUTPUT_THRESHOLD:
                bin_data["progress"] -= _s.COMPOST_OUTPUT_THRESHOLD
                bin_data["output"] += 1
                remaining = _s.COMPOST_INPUT_PER_OUTPUT
                for item_id in list(bin_data["input"].keys()):
                    take = min(remaining, bin_data["input"][item_id])
                    bin_data["input"][item_id] -= take
                    remaining -= take
                    if bin_data["input"][item_id] <= 0:
                        del bin_data["input"][item_id]
                    if remaining <= 0:
                        break

    _COOP_REFILL_TIME = 30.0  # seconds per egg per hen (matches Chicken.REFILL_TIME)
    _COOP_MAX_EGGS    = 24

    def update_chicken_coops(self, dt):
        """Accumulate eggs in all placed coops based on live female chickens."""
        if not self.chicken_coop_data:
            return
        from animals import Chicken as _Chicken
        hens = [e for e in self.entities
                if isinstance(e, _Chicken) and not e.dead
                and e.traits.get("sex") == "female"]
        if not hens:
            return
        rate = sum(e.traits.get("lay_rate", 1.0) / self._COOP_REFILL_TIME for e in hens)
        for coop in self.chicken_coop_data.values():
            if coop["eggs"] >= self._COOP_MAX_EGGS:
                continue
            coop["progress"] += rate * dt
            while coop["progress"] >= 1.0 and coop["eggs"] < self._COOP_MAX_EGGS:
                coop["progress"] -= 1.0
                coop["eggs"] += 1

    def update_trade_blocks(self, dt, player):
        """Tick all trade blocks: dispatch horse, track position-based travel, deliver on arrival."""
        from towns import TOWNS, supply_need
        from town_needs import ITEM_TO_CATEGORY
        from horses import Horse
        from constants import BLOCK_SIZE as _BS

        ARRIVE_THRESH = _BS * 2   # within 2 blocks = arrived

        def _find_horse(uid):
            return next(
                (e for e in self.entities if isinstance(e, Horse) and e.uid == uid and not e.dead),
                None,
            )

        def _deliver(state, town, player):
            for item_id, count in list(state["inventory"].items()):
                player._add_item(item_id, count)
            delivered_cats = set()
            for item_id in list(state["inventory"]):
                cat = ITEM_TO_CATEGORY.get(item_id)
                if cat and cat in town.needs and cat not in delivered_cats:
                    supply_need(town, player, cat, player.count_items_in_category(cat))
                    delivered_cats.add(cat)
            state["inventory"] = {}

        for pos, state in list(self.trade_block_data.items()):

            if state["state"] == "idle":
                if not (state["has_cart"] and state["horse_uid"] and state["linked_town_id"] is not None):
                    continue
                if sum(state["inventory"].values()) < state["threshold"]:
                    continue
                town = TOWNS.get(state["linked_town_id"])
                if town is None:
                    continue
                horse = _find_horse(state["horse_uid"])
                if horse is None or not horse.tamed:
                    continue
                horse._on_trade_run = True
                horse._trade_target_x = town.center_bx * _BS
                state["state"] = "traveling"

            elif state["state"] == "traveling":
                town = TOWNS.get(state["linked_town_id"])
                if town is None:
                    state["state"] = "idle"
                    continue

                horse = _find_horse(state["horse_uid"])

                # Restore flag after save/load
                if horse and not horse._on_trade_run:
                    horse._on_trade_run = True
                    horse._trade_target_x = town.center_bx * _BS

                # Check arrival by position (horse present) or fall back to timer
                if horse is not None:
                    target_px = town.center_bx * _BS
                    if abs((horse.x + horse.W / 2) - target_px) > ARRIVE_THRESH:
                        continue  # still moving
                else:
                    state["ticks_left"] = state.get("ticks_left", 0) - dt
                    if state["ticks_left"] > 0:
                        continue

                # Arrived at city — deliver goods
                _deliver(state, town, player)
                player.pending_notifications.append(
                    ("Trade Post", f"Horse delivered goods to {town.name}", None)
                )
                state["state"] = "returning"
                if horse:
                    horse._trade_target_x = pos[0] * _BS

            elif state["state"] == "returning":
                horse = _find_horse(state["horse_uid"])

                # Restore flag after save/load
                if horse and not horse._on_trade_run:
                    horse._on_trade_run = True
                    horse._trade_target_x = pos[0] * _BS

                if horse is not None:
                    target_px = pos[0] * _BS
                    if abs((horse.x + horse.W / 2) - target_px) > ARRIVE_THRESH:
                        continue  # still returning
                else:
                    state["ticks_left"] = state.get("ticks_left", 0) - dt
                    if state["ticks_left"] > 0:
                        continue

                # Back home
                if horse:
                    horse._on_trade_run = False
                    horse._trade_target_x = None
                    horse._trade_stuck = False
                    horse._trade_stuck_timer = 0.0
                state["state"] = "idle"
                state["ticks_left"] = 0.0

    def update_leaves(self, dt, player):
        self._leaves_timer += dt
        if self._leaves_timer < self._leaves_interval:
            return
        self._leaves_timer -= self._leaves_interval

        to_remove = []
        for cx, chunk in list(self._chunks.items()):
            base_x = cx * CHUNK_W
            for y in range(WORLD_H):
                for lx in range(CHUNK_W):
                    bid = chunk[y][lx]
                    if bid in ALL_LEAVES:
                        log_bid = LEAF_LOG_MAP.get(bid)
                        if log_bid is None:
                            continue
                    else:
                        continue
                    x = base_x + lx
                    has_wood = False
                    for dy in range(-2, 3):
                        for dx in range(-2, 3):
                            if self.get_block(x + dx, y + dy) == log_bid:
                                has_wood = True
                                break
                        if has_wood:
                            break
                    if not has_wood:
                        to_remove.append((x, y))

        from dropped_item import DroppedItem
        for (x, y) in to_remove:
            self.set_block(x, y, AIR)
            if self._leaves_rng.random() < 0.25:
                wx = x * BLOCK_SIZE + BLOCK_SIZE // 2
                wy = y * BLOCK_SIZE + BLOCK_SIZE // 2
                self.dropped_items.append(DroppedItem(wx, wy, "sapling", 1))

    def _spawn_animals(self):
        from animals import Sheep, Cow, Chicken, SnowLeopard, MountainLion, Tiger
        rng = random.Random(self.seed + 12345)
        for cx in sorted(self._chunks.keys()):
            chunk = self._chunks[cx]
            base_x = cx * CHUNK_W
            x = base_x + 5
            x_end = base_x + CHUNK_W - 5
            while x < x_end:
                lx = x - base_x
                sy = self.surface_height(x)
                if 0 < sy < WORLD_H and chunk[sy][lx] == GRASS and chunk[sy - 1][lx] == AIR:
                    animal_cls = rng.choice([Sheep, Sheep, Cow, Chicken])
                    ax = x * BLOCK_SIZE + (BLOCK_SIZE - animal_cls.ANIMAL_W) // 2
                    ay = sy * BLOCK_SIZE - animal_cls.ANIMAL_H
                    self.entities.append(animal_cls(ax, ay, self))
                x += rng.randint(8, 20)

        # Big cats — rare, biome-specific
        cat_rng = random.Random(self.seed + 99991)
        for cx in sorted(self._chunks.keys()):
            chunk = self._chunks[cx]
            base_x = cx * CHUNK_W
            x = base_x + 3
            x_end = base_x + CHUNK_W - 3
            while x < x_end:
                lx = x - base_x
                sy = self.surface_height(x)
                if 0 < sy < WORLD_H and chunk[sy - 1][lx] == AIR:
                    surf = chunk[sy][lx]
                    biodome = self.biodome_at(x)
                    if surf == SNOW and biodome in ("alpine_mountain", "tundra") and cat_rng.random() < 0.05:
                        ax = x * BLOCK_SIZE + (BLOCK_SIZE - SnowLeopard.ANIMAL_W) // 2
                        ay = sy * BLOCK_SIZE - SnowLeopard.ANIMAL_H
                        self.entities.append(SnowLeopard(ax, ay, self))
                    elif surf == GRASS and biodome == "rocky_mountain" and cat_rng.random() < 0.05:
                        ax = x * BLOCK_SIZE + (BLOCK_SIZE - MountainLion.ANIMAL_W) // 2
                        ay = sy * BLOCK_SIZE - MountainLion.ANIMAL_H
                        self.entities.append(MountainLion(ax, ay, self))
                    elif surf == GRASS and biodome == "jungle" and cat_rng.random() < 0.04:
                        ax = x * BLOCK_SIZE + (BLOCK_SIZE - Tiger.ANIMAL_W) // 2
                        ay = sy * BLOCK_SIZE - Tiger.ANIMAL_H
                        self.entities.append(Tiger(ax, ay, self))
                x += cat_rng.randint(25, 55)

        # Horses — biome-specific herds of 2-4
        from horses import Horse, HORSE_BIOMES, _blend_to_herd_template
        horse_rng = random.Random(self.seed + 55551)
        for cx in sorted(self._chunks.keys()):
            chunk = self._chunks[cx]
            base_x = cx * CHUNK_W
            x = base_x + 5
            x_end = base_x + CHUNK_W - 5
            while x < x_end:
                lx = x - base_x
                sy = self.surface_height(x)
                biodome = self.biodome_at(x)
                if (0 < sy < WORLD_H
                        and chunk[sy][lx] == GRASS
                        and chunk[sy - 1][lx] == AIR
                        and biodome in HORSE_BIOMES
                        and horse_rng.random() < 0.12):
                    herd_size = horse_rng.randint(2, 5)
                    alpha = None
                    for _ in range(herd_size):
                        hx_off = horse_rng.randint(-3, 3)
                        hx_bx = max(base_x, min(base_x + CHUNK_W - 1, x + hx_off))
                        hsy = self.surface_height(hx_bx)
                        hx = hx_bx * BLOCK_SIZE + (BLOCK_SIZE - Horse.ANIMAL_W) // 2
                        hy = hsy * BLOCK_SIZE - Horse.ANIMAL_H
                        horse = Horse(hx, hy, self)
                        if alpha is None:
                            alpha = horse
                        else:
                            _blend_to_herd_template(horse, alpha)
                        self.entities.append(horse)
                    x += 55
                    continue
                x += horse_rng.randint(8, 16)

        # Dogs — biome-specific packs of 2-3 by breed
        for cx in sorted(self._chunks.keys()):
            self._spawn_dogs_for_chunk(cx)

    def _spawn_dogs_for_chunk(self, cx: int):
        from dogs import Dog, DOG_BIOME_MAP, _blend_to_pack_template
        chunk = self._chunks.get(cx)
        if chunk is None:
            return
        base_x = cx * CHUNK_W
        dog_rng = random.Random(self.seed + 77773 + cx * 3313)
        x = base_x + 5
        while x < base_x + CHUNK_W - 5:
            lx = x - base_x
            sy = self.surface_height(x)
            biodome = self.biodome_at(x)
            eligible_breeds = DOG_BIOME_MAP.get(biodome, [])
            if (0 < sy < WORLD_H
                    and chunk[sy][lx] == GRASS
                    and chunk[sy - 1][lx] == AIR
                    and eligible_breeds
                    and dog_rng.random() < 0.22):
                breed = dog_rng.choice(eligible_breeds)
                pack_size = dog_rng.randint(2, 4)
                alpha = None
                for _ in range(pack_size):
                    dx_off = dog_rng.randint(-3, 3)
                    dx_bx = max(base_x, min(base_x + CHUNK_W - 1, x + dx_off))
                    dsy = self.surface_height(dx_bx)
                    dox = dx_bx * BLOCK_SIZE + (BLOCK_SIZE - Dog.ANIMAL_W) // 2
                    doy = dsy * BLOCK_SIZE - Dog.ANIMAL_H
                    dog = Dog(dox, doy, self, breed=breed)
                    if alpha is None:
                        alpha = dog
                    else:
                        _blend_to_pack_template(dog, alpha)
                    self.entities.append(dog)
                x += 28
                continue
            x += dog_rng.randint(8, 16)

    def _spawn_capybaras(self):
        from animals import Capybara, CAPYBARA_BIOMES
        rng = random.Random(self.seed + 38471)
        for cx in sorted(self._chunks.keys()):
            chunk = self._chunks[cx]
            base_x = cx * CHUNK_W
            x = base_x + 3
            while x < base_x + CHUNK_W - 3:
                lx = x - base_x
                sy = self.surface_height(x)
                if 0 < sy < WORLD_H and chunk[sy - 1][lx] == AIR:
                    biodome = self.biodome_at(x)
                    if biodome in CAPYBARA_BIOMES and rng.random() < 0.05:
                        ax = x * BLOCK_SIZE + (BLOCK_SIZE - Capybara.ANIMAL_W) // 2
                        ay = sy * BLOCK_SIZE - Capybara.ANIMAL_H
                        self.entities.append(Capybara(ax, ay, self))
                x += rng.randint(18, 40)

    def _spawn_huntable_animals(self):
        from animals import (Deer, Boar, Rabbit, Turkey, Wolf, Bear, Duck, Elk, Bison, Fox,
                             DEER_BIOMES, BOAR_BIOMES, RABBIT_BIOMES, TURKEY_BIOMES,
                             WOLF_BIOMES, BEAR_BIOMES, DUCK_BIOMES, ELK_BIOMES, BISON_BIOMES, FOX_BIOMES,
                             Moose, Bighorn, Pheasant, Warthog, MuskOx, Crocodile, Goose, Hare,
                             MOOSE_BIOMES, BIGHORN_BIOMES, PHEASANT_BIOMES, WARTHOG_BIOMES,
                             MUSK_OX_BIOMES, CROC_BIOMES, GOOSE_BIOMES, HARE_BIOMES,
                             ArcticFox, ARCTIC_FOX_BIOMES)
        _HUNTABLE_MAP = [
            (Deer,      DEER_BIOMES,         0.06),
            (Boar,      BOAR_BIOMES,         0.05),
            (Rabbit,    RABBIT_BIOMES,        0.08),
            (Turkey,    TURKEY_BIOMES,        0.05),
            (Wolf,      WOLF_BIOMES,          0.04),
            (Bear,      BEAR_BIOMES,          0.03),
            (Duck,      DUCK_BIOMES,          0.07),
            (Elk,       ELK_BIOMES,           0.04),
            (Bison,     BISON_BIOMES,         0.05),
            (Fox,       FOX_BIOMES,           0.05),
            (ArcticFox, ARCTIC_FOX_BIOMES,    0.06),
            (Moose,     MOOSE_BIOMES,         0.04),
            (Bighorn,   BIGHORN_BIOMES,       0.05),
            (Pheasant,  PHEASANT_BIOMES,      0.06),
            (Warthog,   WARTHOG_BIOMES,       0.05),
            (MuskOx,    MUSK_OX_BIOMES,       0.05),
            (Crocodile, CROC_BIOMES,          0.04),
            (Goose,     GOOSE_BIOMES,         0.06),
            (Hare,      HARE_BIOMES,          0.07),
        ]
        # Region.danger scales predator density: calm 0.5x, rough 1.0x, wild 1.5x.
        _PREDATORS = (Wolf, Bear, Crocodile)
        _DANGER_MULT = {"calm": 0.5, "rough": 1.0, "wild": 1.5}
        from towns import region_for_bx
        rng = random.Random(self.seed + 74193)
        for cx in sorted(self._chunks.keys()):
            chunk  = self._chunks[cx]
            base_x = cx * CHUNK_W
            x      = base_x + 3
            x_end  = base_x + CHUNK_W - 3
            while x < x_end:
                lx      = x - base_x
                sy      = self.surface_height(x)
                biodome = self.biodome_at(x)
                surf = chunk[sy][lx] if 0 < sy < WORLD_H else AIR
                if 0 < sy < WORLD_H and surf in (GRASS, SNOW) and chunk[sy - 1][lx] == AIR:
                    region = region_for_bx(self, x)
                    danger_mult = _DANGER_MULT.get(region.danger, 1.0) if region else 1.0
                    for cls, biomes, rate in _HUNTABLE_MAP:
                        eff_rate = rate * danger_mult if cls in _PREDATORS else rate
                        if biodome in biomes and rng.random() < eff_rate:
                            ax = x * BLOCK_SIZE + (BLOCK_SIZE - cls.ANIMAL_W) // 2
                            ay = sy * BLOCK_SIZE - cls.ANIMAL_H
                            self.entities.append(cls(ax, ay, self))
                            break
                x += rng.randint(12, 28)

    def _spawn_birds(self):
        from birds import ALL_SPECIES, COMMON_SPECIES, Nest
        self.birds.clear()
        self.nests.clear()
        rng = random.Random()
        max_birds = 150
        spacing = 15  # blocks between spawn attempts

        for cx in sorted(self._chunks.keys()):
            base_x = cx * CHUNK_W
            x = base_x + 2
            while x < base_x + CHUNK_W - 2:
                if len(self.birds) >= max_birds:
                    return
                biodome = self.biodome_at(x)
                is_night = self.time_of_day >= DAY_DURATION
                candidates = [cls for cls in ALL_SPECIES
                              if (not cls.BIOMES or biodome in cls.BIOMES)
                              and (not getattr(cls, 'NOCTURNAL', False) or is_night)]
                if not candidates:
                    candidates = COMMON_SPECIES
                if not candidates:
                    x += rng.randint(spacing, spacing * 2)
                    continue

                species_cls = rng.choice(candidates)
                is_ground = getattr(species_cls, 'IS_GROUND', False)
                sy = self.surface_height(x)
                # Over water, treat the sea surface as ground; skip ground birds
                if sy >= SURFACE_Y:
                    if is_ground:
                        x += rng.randint(spacing, spacing * 2)
                        continue
                    sy = SURFACE_Y
                alt_px = rng.randint(*species_cls.ALTITUDE_BLOCKS) * BLOCK_SIZE
                spawn_x = float(x * BLOCK_SIZE)
                spawn_y = float(sy * BLOCK_SIZE - alt_px)

                if species_cls.IS_FLOCK:
                    n = rng.randint(*species_cls.FLOCK_SIZE_RANGE)
                    leader = species_cls(spawn_x, spawn_y, self)
                    leader._pick_flight_target(rng)
                    self.birds.append(leader)
                    if is_ground:
                        self.nests.append(Nest(x + rng.randint(-5, 5), sy, species_cls))
                    for _ in range(n - 1):
                        if len(self.birds) >= max_birds:
                            break
                        follower = species_cls(
                            spawn_x + rng.uniform(-20, 20),
                            spawn_y + rng.uniform(-10, 10),
                            self,
                        )
                        follower._flock_leader = leader
                        follower._flock_offset = (
                            rng.uniform(-28, 28),
                            rng.uniform(-12, 12),
                        )
                        self.birds.append(follower)
                else:
                    bird = species_cls(spawn_x, spawn_y, self)
                    bird._pick_flight_target(rng)
                    self.birds.append(bird)
                    if is_ground:
                        self.nests.append(Nest(x + rng.randint(-5, 5), sy, species_cls))

                x += rng.randint(spacing, spacing * 2)

    def _spawn_animals_for_chunk(self, cx: int):
        from animals import Sheep, Cow, Chicken, Goat, SnowLeopard, MountainLion, Tiger
        chunk = self._chunks.get(cx)
        if chunk is None:
            return
        base_x = cx * CHUNK_W

        _GOAT_BIOMES = {"rocky_mountain", "alpine_mountain", "canyon", "arid_steppe", "boreal"}

        rng = random.Random(self.seed + 12345 + cx * 6271)
        x = base_x + 5
        while x < base_x + CHUNK_W - 5:
            lx = x - base_x
            sy = self.surface_height(x)
            if 0 < sy < WORLD_H and chunk[sy][lx] == GRASS and chunk[sy - 1][lx] == AIR:
                biodome = self.biodome_at(x)
                if biodome in _GOAT_BIOMES:
                    animal_cls = rng.choice([Goat, Goat, Sheep, Cow])
                else:
                    animal_cls = rng.choice([Sheep, Sheep, Cow, Chicken])
                ax = x * BLOCK_SIZE + (BLOCK_SIZE - animal_cls.ANIMAL_W) // 2
                ay = sy * BLOCK_SIZE - animal_cls.ANIMAL_H
                self.entities.append(animal_cls(ax, ay, self))
            x += rng.randint(8, 20)

        cat_rng = random.Random(self.seed + 99991 + cx * 3571)
        x = base_x + 3
        while x < base_x + CHUNK_W - 3:
            lx = x - base_x
            sy = self.surface_height(x)
            if 0 < sy < WORLD_H and chunk[sy - 1][lx] == AIR:
                surf = chunk[sy][lx]
                biodome = self.biodome_at(x)
                if surf == SNOW and biodome in ("alpine_mountain", "tundra") and cat_rng.random() < 0.05:
                    ax = x * BLOCK_SIZE + (BLOCK_SIZE - SnowLeopard.ANIMAL_W) // 2
                    ay = sy * BLOCK_SIZE - SnowLeopard.ANIMAL_H
                    self.entities.append(SnowLeopard(ax, ay, self))
                elif surf == GRASS and biodome == "rocky_mountain" and cat_rng.random() < 0.05:
                    ax = x * BLOCK_SIZE + (BLOCK_SIZE - MountainLion.ANIMAL_W) // 2
                    ay = sy * BLOCK_SIZE - MountainLion.ANIMAL_H
                    self.entities.append(MountainLion(ax, ay, self))
                elif surf == GRASS and biodome == "jungle" and cat_rng.random() < 0.04:
                    ax = x * BLOCK_SIZE + (BLOCK_SIZE - Tiger.ANIMAL_W) // 2
                    ay = sy * BLOCK_SIZE - Tiger.ANIMAL_H
                    self.entities.append(Tiger(ax, ay, self))
            x += cat_rng.randint(25, 55)

        from horses import Horse, HORSE_BIOMES
        horse_rng = random.Random(self.seed + 55551 + cx * 4987)
        x = base_x + 5
        while x < base_x + CHUNK_W - 5:
            lx = x - base_x
            sy = self.surface_height(x)
            biodome = self.biodome_at(x)
            if (0 < sy < WORLD_H
                    and chunk[sy][lx] == GRASS
                    and chunk[sy - 1][lx] == AIR
                    and biodome in HORSE_BIOMES
                    and horse_rng.random() < 0.12):
                herd_size = horse_rng.randint(2, 5)
                for _ in range(herd_size):
                    hx_off = horse_rng.randint(-3, 3)
                    hx_bx = max(base_x, min(base_x + CHUNK_W - 1, x + hx_off))
                    hsy = self.surface_height(hx_bx)
                    hx = hx_bx * BLOCK_SIZE + (BLOCK_SIZE - Horse.ANIMAL_W) // 2
                    hy = hsy * BLOCK_SIZE - Horse.ANIMAL_H
                    self.entities.append(Horse(hx, hy, self))
                x += 55
                continue
            x += horse_rng.randint(8, 16)

        self._spawn_dogs_for_chunk(cx)

        from animals import (Deer, Boar, Rabbit, Turkey, Wolf, Bear, Duck, Elk, Bison, Fox,
                             DEER_BIOMES, BOAR_BIOMES, RABBIT_BIOMES, TURKEY_BIOMES,
                             WOLF_BIOMES, BEAR_BIOMES, DUCK_BIOMES, ELK_BIOMES, BISON_BIOMES, FOX_BIOMES,
                             Moose, Bighorn, Pheasant, Warthog, MuskOx, Crocodile, Goose, Hare,
                             MOOSE_BIOMES, BIGHORN_BIOMES, PHEASANT_BIOMES, WARTHOG_BIOMES,
                             MUSK_OX_BIOMES, CROC_BIOMES, GOOSE_BIOMES, HARE_BIOMES,
                             ArcticFox, ARCTIC_FOX_BIOMES)
        _HUNTABLE_MAP = [
            (Deer,      DEER_BIOMES,         0.06),
            (Boar,      BOAR_BIOMES,         0.05),
            (Rabbit,    RABBIT_BIOMES,        0.08),
            (Turkey,    TURKEY_BIOMES,        0.05),
            (Wolf,      WOLF_BIOMES,          0.04),
            (Bear,      BEAR_BIOMES,          0.03),
            (Duck,      DUCK_BIOMES,          0.07),
            (Elk,       ELK_BIOMES,           0.04),
            (Bison,     BISON_BIOMES,         0.05),
            (Fox,       FOX_BIOMES,           0.05),
            (ArcticFox, ARCTIC_FOX_BIOMES,    0.06),
            (Moose,     MOOSE_BIOMES,         0.04),
            (Bighorn,   BIGHORN_BIOMES,       0.05),
            (Pheasant,  PHEASANT_BIOMES,      0.06),
            (Warthog,   WARTHOG_BIOMES,       0.05),
            (MuskOx,    MUSK_OX_BIOMES,       0.05),
            (Crocodile, CROC_BIOMES,          0.04),
            (Goose,     GOOSE_BIOMES,         0.06),
            (Hare,      HARE_BIOMES,          0.07),
        ]
        # Region.danger scales predator density: calm 0.5x, rough 1.0x, wild 1.5x.
        _PREDATORS = (Wolf, Bear, Crocodile)
        _DANGER_MULT = {"calm": 0.5, "rough": 1.0, "wild": 1.5}
        from towns import region_for_bx
        hunt_rng = random.Random(self.seed + 74193 + cx * 8317)
        x = base_x + 3
        while x < base_x + CHUNK_W - 3:
            lx = x - base_x
            sy = self.surface_height(x)
            biodome = self.biodome_at(x)
            surf = chunk[sy][lx] if 0 < sy < WORLD_H else AIR
            if 0 < sy < WORLD_H and surf in (GRASS, SNOW) and chunk[sy - 1][lx] == AIR:
                region = region_for_bx(self, x)
                danger_mult = _DANGER_MULT.get(region.danger, 1.0) if region else 1.0
                for cls, biomes, rate in _HUNTABLE_MAP:
                    eff_rate = rate * danger_mult if cls in _PREDATORS else rate
                    if biodome in biomes and hunt_rng.random() < eff_rate:
                        ax = x * BLOCK_SIZE + (BLOCK_SIZE - cls.ANIMAL_W) // 2
                        ay = sy * BLOCK_SIZE - cls.ANIMAL_H
                        self.entities.append(cls(ax, ay, self))
                        break
            x += hunt_rng.randint(12, 28)

        from animals import Capybara, CAPYBARA_BIOMES
        cap_rng = random.Random(self.seed + 38471 + cx * 5923)
        x = base_x + 3
        while x < base_x + CHUNK_W - 3:
            lx = x - base_x
            sy = self.surface_height(x)
            if 0 < sy < WORLD_H and chunk[sy - 1][lx] == AIR:
                biodome = self.biodome_at(x)
                if biodome in CAPYBARA_BIOMES and cap_rng.random() < 0.05:
                    ax = x * BLOCK_SIZE + (BLOCK_SIZE - Capybara.ANIMAL_W) // 2
                    ay = sy * BLOCK_SIZE - Capybara.ANIMAL_H
                    self.entities.append(Capybara(ax, ay, self))
            x += cap_rng.randint(18, 40)

    def _spawn_birds_for_chunk(self, cx: int):
        from birds import ALL_SPECIES, COMMON_SPECIES, Nest
        base_x = cx * CHUNK_W
        rng = random.Random()
        spacing = 15
        x = base_x + 2
        while x < base_x + CHUNK_W - 2:
            biodome = self.biodome_at(x)
            is_night = self.time_of_day >= DAY_DURATION
            candidates = [cls for cls in ALL_SPECIES
                          if (not cls.BIOMES or biodome in cls.BIOMES)
                          and (not getattr(cls, 'NOCTURNAL', False) or is_night)]
            if not candidates:
                candidates = COMMON_SPECIES
            if not candidates:
                x += rng.randint(spacing, spacing * 2)
                continue
            species_cls = rng.choice(candidates)
            is_ground = getattr(species_cls, 'IS_GROUND', False)
            sy = self.surface_height(x)
            # Over water, treat the sea surface as ground; skip ground birds
            if sy >= SURFACE_Y:
                if is_ground:
                    x += rng.randint(spacing, spacing * 2)
                    continue
                sy = SURFACE_Y
            alt_px = rng.randint(*species_cls.ALTITUDE_BLOCKS) * BLOCK_SIZE
            spawn_x = float(x * BLOCK_SIZE)
            spawn_y = float(sy * BLOCK_SIZE - alt_px)
            if species_cls.IS_FLOCK:
                n = rng.randint(*species_cls.FLOCK_SIZE_RANGE)
                leader = species_cls(spawn_x, spawn_y, self)
                leader._pick_flight_target(rng)
                self.birds.append(leader)
                if is_ground:
                    self.nests.append(Nest(x + rng.randint(-5, 5), sy, species_cls))
                for _ in range(n - 1):
                    follower = species_cls(
                        spawn_x + rng.uniform(-20, 20),
                        spawn_y + rng.uniform(-10, 10),
                        self,
                    )
                    follower._flock_leader = leader
                    follower._flock_offset = (rng.uniform(-28, 28), rng.uniform(-12, 12))
                    self.birds.append(follower)
            else:
                bird = species_cls(spawn_x, spawn_y, self)
                bird._pick_flight_target(rng)
                self.birds.append(bird)
                if is_ground:
                    self.nests.append(Nest(x + rng.randint(-5, 5), sy, species_cls))
            x += rng.randint(spacing, spacing * 2)

    def _spawn_insects_for_chunk(self, cx):
        from insects import ALL_INSECT_SPECIES
        from blocks import WILDFLOWER_PATCH, WATER
        rng = random.Random(self.seed + 99991 + cx * 7919)
        spacing = 6
        base_x = cx * CHUNK_W
        x = base_x + 2
        while x < base_x + CHUNK_W - 2:
            biodome = self.biodome_at(x)
            candidates = [cls for cls in ALL_INSECT_SPECIES
                          if not cls.BIOMES or biodome in cls.BIOMES]
            if not candidates:
                x += rng.randint(spacing, spacing * 2)
                continue
            sy = self.surface_height(x)
            if sy >= SURFACE_Y:  # submerged — no insects underwater
                x += rng.randint(spacing, spacing * 2)
                continue
            near_feature = (
                self.get_block(x, sy - 1) == WILDFLOWER_PATCH
                or self.get_block(x, sy) == WATER
                or self.get_block(x - 1, sy) == WATER
                or self.get_block(x + 1, sy) == WATER
            )
            if not near_feature and rng.random() > 0.4:
                x += rng.randint(spacing, spacing * 2)
                continue
            species_cls = rng.choice(candidates)
            spawn_x = float(x * BLOCK_SIZE + rng.randint(-8, 8))
            spawn_y = float(sy * BLOCK_SIZE - rng.randint(8, 24))
            self.insects.append(species_cls(spawn_x, spawn_y, self))
            x += rng.randint(spacing, spacing * 2)

    def _spawn_garden_insects_in_chunk(self, cx):
        base_x = cx * CHUNK_W
        for (gx, gy), flowers in self.garden_data.items():
            if base_x <= gx < base_x + CHUNK_W and flowers:
                self._add_garden_insects(gx, gy)

    def _add_garden_insects(self, bx, by):
        from insects import ALL_INSECT_SPECIES
        biodome = self.biodome_at(bx)
        candidates = [cls for cls in ALL_INSECT_SPECIES
                      if not cls.BIOMES or biodome in cls.BIOMES]
        if not candidates:
            return
        rng = random.Random(self.seed + 77777 + bx * 31 + by * 97)
        for _ in range(3):
            species_cls = rng.choice(candidates)
            spawn_x = float(bx * BLOCK_SIZE + rng.randint(-16, 16))
            spawn_y = float(by * BLOCK_SIZE - rng.randint(8, 28))
            self.insects.append(species_cls(spawn_x, spawn_y, self))

    def spawn_insects_near_garden(self, bx, by):
        """Dynamically add insects near a garden block when wildflowers are deposited."""
        self._add_garden_insects(bx, by)

    def _spawn_insects(self):
        self.insects.clear()
        for cx in sorted(self._chunks.keys()):
            self._spawn_insects_for_chunk(cx)
            self._spawn_garden_insects_in_chunk(cx)

    def surface_y_at(self, x: int) -> int:
        return self.surface_height(x)

    def spawn_drops(self, x, y, items_dict):
        from dropped_item import DroppedItem
        import random as _rnd
        for item_id, count in items_dict.items():
            if count <= 0:
                continue
            dx = _rnd.uniform(-2.5, 2.5) * BLOCK_SIZE
            dy = _rnd.uniform(-1.5, 0) * BLOCK_SIZE
            self.dropped_items.append(DroppedItem(x + dx, y + dy, item_id, count))

    def update_dropped_items(self, dt, player):
        to_remove = []
        for item in self.dropped_items:
            item.update(dt)
            if item.expired:
                to_remove.append(item)
            elif item.in_range(player):
                player._add_item(item.item_id, item.count)
                to_remove.append(item)
        for item in to_remove:
            self.dropped_items.remove(item)
