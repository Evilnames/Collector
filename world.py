import math
import random
import time as _time
from math import cos, sin, pi
from blocks import *  # noqa: F401,F403
from constants import CHUNK_W, CHUNK_LOAD_RADIUS, WORLD_MAX_X, WORLD_H, SURFACE_Y, BLOCK_SIZE, PLAYER_W, PLAYER_H
from biomes import BIOMES, BIOME_ORE_MULTIPLIERS, BIODOME_TYPES


class World:
    def __init__(self, seed=42, preloaded=None, save_mgr=None, player_x=0.0):
        self.seed = seed
        self.height = WORLD_H
        self._save_mgr = save_mgr
        self._chunks = {}           # chunk_x -> [[block_id]*CHUNK_W]*WORLD_H
        self._dirty_chunks = set()
        self.entities = []
        self.automations = []
        self.dropped_items = []
        self.chest_data = {}     # (bx, by) -> {item_id: count}
        self._water_level = {}   # (x,y) -> int 1-8; 8 = world-gen source block
        self._lake_cells  = []
        # Pre-compute deterministic terrain noise once
        _rng = random.Random(self.seed)
        self._surf_octaves = [(0.015, 6.0), (0.04, 3.0), (0.10, 1.5), (0.22, 0.6)]
        self._surf_phases  = [_rng.uniform(0, 6.28) for _ in self._surf_octaves]
        self._physics_timer = 0.0
        self._physics_interval = 0.5
        self._fall_chance = 0.25
        self._physics_rng = random.Random(seed + 77)
        self.pending_physics = set()
        self._physics_tick = 0
        self._physics_grace = {}
        if preloaded:
            self._load_from(preloaded, player_x)
        else:
            for cx in range(-CHUNK_LOAD_RADIUS, CHUNK_LOAD_RADIUS + 1):
                self.load_chunk(cx)
            self._spawn_animals()
            from cities import generate_cities
            generate_cities(self, self.seed)
        if preloaded:
            self._seed_physics()
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

    def surface_height(self, x: int) -> int:
        h = SURFACE_Y
        for (freq, amp), phase in zip(self._surf_octaves, self._surf_phases):
            h += amp * math.sin(x * freq + phase)
        return round(h)

    def biome_at(self, x: int) -> str:
        zone = x // 150
        nearest_biome, nearest_dist = BIOMES[0], float('inf')
        for z in (zone - 1, zone, zone + 1):
            rng = random.Random(hash((self.seed, z, 'bc')) & 0x7FFFFFFF)
            cx = z * 150 + rng.randint(-25, 25)
            dist = abs(x - cx)
            if dist < nearest_dist:
                nearest_dist = dist
                brng = random.Random(hash((self.seed, z, 'bt')) & 0x7FFFFFFF)
                nearest_biome = brng.choice(BIOMES)
        return nearest_biome

    def biodome_at(self, x: int) -> str:
        zone = x // 200
        nearest, nearest_dist = BIODOME_TYPES[0], float('inf')
        for z in (zone - 1, zone, zone + 1):
            rng = random.Random(hash((self.seed, z, 'bdc')) & 0x7FFFFFFF)
            cxz = z * 200 + rng.randint(-40, 40)
            dist = abs(x - cxz)
            if dist < nearest_dist:
                nearest_dist = dist
                brng = random.Random(hash((self.seed, z, 'bdt')) & 0x7FFFFFFF)
                nearest = brng.choice(BIODOME_TYPES)
        return nearest

    def get_biome(self, bx: int) -> str:
        return self.biome_at(bx)

    def get_biodome(self, bx: int) -> str:
        return self.biodome_at(bx)

    def surface_y_at(self, x: int) -> int:
        return self.surface_height(x)

    # ------------------------------------------------------------------
    # Chunk infrastructure
    # ------------------------------------------------------------------

    def load_chunk(self, cx: int):
        """Load chunk from DB, or generate fresh if unseen."""
        if cx in self._chunks:
            return
        data = self._save_mgr.load_chunk(cx) if self._save_mgr else None
        self._chunks[cx] = data if data is not None else [[AIR] * CHUNK_W for _ in range(WORLD_H)]
        if data is None:
            self._fill_chunk(cx)

    def unload_chunk(self, cx: int):
        """Save dirty chunk to DB and evict from memory."""
        if cx not in self._chunks:
            return
        if self._save_mgr and cx in self._dirty_chunks:
            self._save_mgr.save_chunk(cx, self._chunks[cx])
            self._dirty_chunks.discard(cx)
        del self._chunks[cx]

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
        for cx in to_unload:
            del self._chunks[cx]

        # Load all needed chunks from DB in one query, generate any that are new
        if to_load:
            db_data = self._save_mgr.load_chunks_batch(to_load) if self._save_mgr else {}
            for cx in to_load:
                if cx in db_data:
                    self._chunks[cx] = db_data[cx]
                else:
                    self._chunks[cx] = [[AIR] * CHUNK_W for _ in range(WORLD_H)]
                    self._fill_chunk(cx)

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
        self._water_level = data.get("water_level", {})
        raw_chests = data.get("chest_data", {})
        self.chest_data = {
            tuple(int(v) for v in k.split(",")): inv
            for k, inv in raw_chests.items()
        }
        # Load chunks around the player's saved position
        player_cx = int(player_x // BLOCK_SIZE) // CHUNK_W
        for cx in range(player_cx - CHUNK_LOAD_RADIUS, player_cx + CHUNK_LOAD_RADIUS + 1):
            self.load_chunk(cx)

        from automations import Automation
        for a_data in data["automations"]:
            a = Automation(a_data["x"], a_data["y"], a_data["auto_type"], a_data["direction"])
            a.fuel = a_data["fuel"]
            a.supports = a_data["supports"]
            a.stored = a_data["stored"]
            a._state = a_data["state"]
            a._halt_reason = a_data["halt_reason"]
            a._blocks_since_support = a_data["blocks_since_support"]
            self.automations.append(a)

        from animals import Sheep, Cow, Chicken
        _CLASS_MAP = {"Sheep": Sheep, "Cow": Cow, "Chicken": Chicken}
        for e_data in data["entities"]:
            cls = _CLASS_MAP.get(e_data["entity_type"])
            if cls is None:
                continue
            entity = cls(e_data["x"], e_data["y"], self)
            entity.facing = e_data["facing"]
            extra = e_data.get("extra", {})
            if isinstance(entity, Sheep) and "has_wool" in extra:
                entity.has_wool = extra["has_wool"]
            elif isinstance(entity, Cow) and "has_milk" in extra:
                entity.has_milk = extra["has_milk"]
            elif isinstance(entity, Chicken) and "has_egg" in extra:
                entity.has_egg = extra["has_egg"]
            self.entities.append(entity)

        from cities import generate_cities
        generate_cities(self, self.seed)

        from dropped_item import DroppedItem
        for d in data.get("dropped_items", []):
            self.dropped_items.append(
                DroppedItem(d["x"], d["y"], d["item_id"], d["count"], d["lifetime"])
            )

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
            for y in range(WORLD_H):
                if y < sy:
                    chunk[y][lx] = AIR
                elif y == sy:
                    chunk[y][lx] = GRASS
                elif y < sy + 6:
                    chunk[y][lx] = DIRT
                elif y >= WORLD_H - 1:
                    chunk[y][lx] = BEDROCK
                else:
                    chunk[y][lx] = self._pick_block(y - sy, ore_rng, biome)

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

        # Trees — _dispatch_grow uses set_block which silently skips unloaded chunks
        tree_rng = random.Random(hash((self.seed, cx, 'trees')) & 0x7FFFFFFF)
        lx = 2
        while lx < CHUNK_W - 2:
            x = cx * CHUNK_W + lx
            sy = self.surface_height(x)
            biodome = self.biodome_at(x)
            self._dispatch_grow(x, sy - 1, biodome, tree_rng)
            lo, hi = {
                "jungle":    (3, 6), "fungal":    (3, 7), "boreal":    (4, 8),
                "wetland":   (4, 8), "wasteland": (9, 16), "savanna":  (7, 13),
            }.get(biodome, (5, 10))
            lx += tree_rng.randint(lo, hi)

        # Bushes — write directly into chunk array (within-chunk positions)
        bush_rng = random.Random(hash((self.seed, cx, 'bushes')) & 0x7FFFFFFF)
        lx = 5
        while lx < CHUNK_W - 5:
            sy = self.surface_height(cx * CHUNK_W + lx)
            if 0 < sy < WORLD_H and chunk[sy - 1][lx] == AIR and chunk[sy][lx] == GRASS:
                chunk[sy - 1][lx] = bush_rng.choice([
                    STRAWBERRY_BUSH, WHEAT_BUSH, CARROT_BUSH, TOMATO_BUSH, CORN_BUSH,
                    PUMPKIN_BUSH, APPLE_BUSH, RICE_BUSH, GINGER_BUSH, BOK_CHOY_BUSH,
                    GARLIC_BUSH, SCALLION_BUSH, CHILI_BUSH, PEPPER_BUSH, ONION_BUSH,
                    POTATO_BUSH, EGGPLANT_BUSH, CABBAGE_BUSH,
                ])
            lx += bush_rng.randint(7, 15)

        # Wildflowers
        flower_rng = random.Random(hash((self.seed, cx, 'flowers')) & 0x7FFFFFFF)
        lx = 1
        while lx < CHUNK_W - 1:
            x = cx * CHUNK_W + lx
            sy = self.surface_height(x)
            biodome = self.biodome_at(x)
            if 0 < sy < WORLD_H and chunk[sy - 1][lx] == AIR and chunk[sy][lx] == GRASS:
                if flower_rng.random() < 0.75:
                    chunk[sy - 1][lx] = WILDFLOWER_PATCH
            lo, hi = {
                "jungle": (2, 5), "tropical": (2, 5), "wetland": (3, 7),
                "temperate": (4, 9), "boreal": (5, 10), "birch_forest": (4, 9),
                "redwood": (5, 11), "savanna": (6, 13), "wasteland": (12, 25),
                "fungal": (4, 10),
            }.get(biodome, (5, 10))
            lx += flower_rng.randint(lo, hi)

        # Lakes (chunk-local)
        self._gen_chunk_lakes(cx, chunk)

    def _gen_chunk_lakes(self, cx: int, chunk: list):
        """Carve small lakes within this chunk."""
        rng = random.Random(hash((self.seed, cx, 'lakes')) & 0x7FFFFFFF)
        _impassable = {BEDROCK, GATE_MID, GATE_DEEP, GATE_CORE}
        # Each zone has a probability of spawning one lake per chunk
        zones = [
            (15,  38,  0.43,  4,  8, 2, 3),
            (45,  98,  0.54,  7, 14, 3, 4),
            (105, 158, 0.54, 10, 20, 3, 5),
            (165, 190, 0.32, 12, 24, 4, 6),
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
            for fy in range(ceiling_y + 1, floor_y):
                if self.grid[fy][bx] == AIR:
                    self.grid[fy][bx] = STONE

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

    def _pick_block(self, depth, rng, biome="igneous"):
        r = rng.random()
        # Rock deposits — checked first, rare pockets of collectible rocks
        if depth >= 15:
            if depth >= 120 and r < 0.025:
                return ROCK_DEPOSIT
            elif depth >= 50 and r < 0.015:
                return ROCK_DEPOSIT
            elif r < 0.008:
                return ROCK_DEPOSIT
        r = rng.random()  # fresh roll so deposit chance doesn't eat ore slots
        m = BIOME_ORE_MULTIPLIERS.get(biome, {})
        cm = m.get("coal", 1.0)
        im = m.get("iron", 1.0)
        gm = m.get("gold", 1.0)
        xm = m.get("crystal", 1.0)
        rm = m.get("ruby", 1.0)
        om = m.get("obsidian", 1.0)
        if depth < 40:
            if r < 0.040 * cm: return COAL_ORE
            if r < 0.060 * im: return IRON_ORE
        elif depth < 100:
            if r < 0.030 * im: return IRON_ORE
            if r < 0.055 * gm: return GOLD_ORE
            if r < 0.065 * cm: return COAL_ORE
        elif depth < 160:
            if r < 0.025 * gm: return GOLD_ORE
            if r < 0.045 * xm: return CRYSTAL_ORE
            if r < 0.055 * rm: return RUBY_ORE
        else:
            if r < 0.150 * om: return OBSIDIAN
            if r < 0.180 * xm: return CRYSTAL_ORE
            if r < 0.195 * rm: return RUBY_ORE
        return STONE

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
        if block_id == SAPLING:
            self.pending_saplings.add((x, y))
        elif old_bid == SAPLING:
            self.pending_saplings.discard((x, y))
        if block_id in YOUNG_CROP_BLOCKS:
            self.pending_crops.add((x, y))
        elif old_bid in YOUNG_CROP_BLOCKS:
            self.pending_crops.discard((x, y))
        if old_bid == WATER:
            self._water_level.pop((x, y), None)
        if block_id == AIR:
            for ddx, ddy in ((0, -1), (-1, 0), (1, 0)):
                nx, ny = x + ddx, y + ddy
                if 0 <= ny < WORLD_H:
                    nb = self._chunk_get(nx, ny)
                    if nb in PHYSICS_BLOCKS:
                        self.pending_physics.add((nx, ny))
                        self._physics_grace[(nx, ny)] = self._physics_tick + 3
                    elif nb == WATER:
                        self._pending_water.add((nx, ny))
            if old_bid in ALL_SUPPORTS:
                r = SUPPORT_RANGE[old_bid]
                for check_y in (y, y - 1):
                    if 0 <= check_y < WORLD_H:
                        for ddx in range(-r, r + 1):
                            nx = x + ddx
                            if self._chunk_get(nx, check_y) in PHYSICS_BLOCKS:
                                self.pending_physics.add((nx, check_y))
                                self._physics_grace[(nx, check_y)] = self._physics_tick + 3

    def is_solid(self, x, y):
        bid = self.get_block(x, y)
        return (bid != AIR and bid != LADDER and bid not in ALL_SUPPORTS
                and bid != WATER and bid != SAPLING
                and bid not in BUSH_BLOCKS and bid not in CROP_BLOCKS
                and bid not in OPEN_DOORS)

    def _seed_physics(self):
        for cx, chunk in self._chunks.items():
            base_x = cx * CHUNK_W
            for y in range(WORLD_H - 1):
                for lx in range(CHUNK_W):
                    if chunk[y][lx] in PHYSICS_BLOCKS and chunk[y + 1][lx] == AIR:
                        self.pending_physics.add((base_x + lx, y))

    def _is_supported(self, x, y):
        for check_y in (y, y + 1):
            if 0 <= check_y < WORLD_H:
                for nx in range(x - 10, x + 11):
                    bid = self._chunk_get(nx, check_y)
                    if bid in SUPPORT_RANGE and abs(nx - x) <= SUPPORT_RANGE[bid]:
                        return True
        return False

    def _hits_player(self, bx, by, player):
        return (player.x < (bx + 1) * BLOCK_SIZE and
                player.x + PLAYER_W > bx * BLOCK_SIZE and
                player.y < (by + 1) * BLOCK_SIZE and
                player.y + PLAYER_H > by * BLOCK_SIZE)

    def _push_player(self, bx, by, player):
        by_top = int(player.y // BLOCK_SIZE)
        by_bot = int((player.y + PLAYER_H - 1) // BLOCK_SIZE)
        for dx in (-1, 1):
            nx = bx + dx
            if all(not self.is_solid(nx, ty) for ty in range(by_top, by_bot + 1)):
                player.x = float(nx * BLOCK_SIZE + (BLOCK_SIZE - PLAYER_W) // 2)
                return

    def update_physics(self, dt, player):
        self._physics_timer += dt
        if self._physics_timer < self._physics_interval:
            return
        self._physics_timer -= self._physics_interval

        self._physics_tick += 1
        to_check = list(self.pending_physics)
        self.pending_physics.clear()
        newly_pending = set()

        for (x, y) in to_check:
            bid = self._chunk_get(x, y)
            if bid not in PHYSICS_BLOCKS:
                self._physics_grace.pop((x, y), None)
                continue
            below_y = y + 1
            if below_y >= WORLD_H:
                continue
            if self._chunk_get(x, below_y) != AIR:
                continue
            if self._is_supported(x, y):
                self._physics_grace.pop((x, y), None)
                continue
            if self._physics_grace.get((x, y), 0) > self._physics_tick:
                newly_pending.add((x, y))
                continue
            self._physics_grace.pop((x, y), None)
            if self._physics_rng.random() < self._fall_chance:
                self._chunk_set(x, y, AIR)
                self._chunk_set(x, below_y, bid)
                if self._hits_player(x, below_y, player):
                    self._push_player(x, below_y, player)
                    player.health = max(0, player.health - 10)
                if y - 1 >= 0 and self._chunk_get(x, y - 1) in PHYSICS_BLOCKS:
                    newly_pending.add((x, y - 1))
                if below_y + 1 < WORLD_H and self._chunk_get(x, below_y + 1) == AIR:
                    newly_pending.add((x, below_y))
            else:
                newly_pending.add((x, y))

        self.pending_physics.update(newly_pending)

    def update_water(self, dt, player):
        self._water_timer += dt
        if self._water_timer < self._water_interval:
            return
        self._water_timer -= self._water_interval

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

            # Blocked below — spread sideways at reduced level (level > 1 only)
            if level > 1:
                for dx in (-1, 1):
                    nx = x + dx
                    if self._chunk_get(nx, y) == AIR:
                        self._chunk_set(nx, y, WATER)
                        self._water_level[(nx, y)] = level - 1
                        new_water.add((nx, y))
                        spreads += 1

        self._pending_water.update(new_water)

    def _has_sky_view(self, x, y):
        _transparent = BUSH_BLOCKS | CROP_BLOCKS | {SAPLING}
        for check_y in range(y - 1, -1, -1):
            bid = self.get_block(x, check_y)
            if bid != AIR and bid not in _transparent:
                return False
        return True

    def _place_canopy(self, layers, leaf_bid, rng=None, density=1.0):
        for ly, lx_range in layers:
            if ly < 0 or ly >= WORLD_H:
                continue
            for lx in lx_range:
                if self.get_block(lx, ly) == AIR:
                    if rng is None or density >= 1.0 or rng.random() < density:
                        self.set_block(lx, ly, leaf_bid)

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

    def _dispatch_grow(self, bx, by, biodome, rng=None):
        {
            "temperate":    self._grow_oak,
            "boreal":       self._grow_pine,
            "birch_forest": self._grow_birch,
            "jungle":       self._grow_jungle,
            "wetland":      self._grow_willow,
            "redwood":      self._grow_redwood,
            "tropical":     self._grow_palm,
            "savanna":      self._grow_acacia,
            "wasteland":    self._grow_dead,
            "fungal":       self._grow_mushroom,
        }.get(biodome, self._grow_oak)(bx, by, rng)

    def _grow_tree(self, bx, by):
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
            if self.get_block(x, y) != SAPLING:
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
            if below not in (GRASS, DIRT):
                still_pending.add((x, y))
                continue
            if not self._has_sky_view(x, y):
                still_pending.add((x, y))
                continue
            if self._crop_rng.random() < 0.15:
                _crop_mature_map = {
                    STRAWBERRY_CROP_YOUNG: STRAWBERRY_CROP_MATURE,
                    WHEAT_CROP_YOUNG:      WHEAT_CROP_MATURE,
                    CARROT_CROP_YOUNG:     CARROT_CROP_MATURE,
                    TOMATO_CROP_YOUNG:     TOMATO_CROP_MATURE,
                    CORN_CROP_YOUNG:       CORN_CROP_MATURE,
                    PUMPKIN_CROP_YOUNG:    PUMPKIN_CROP_MATURE,
                    APPLE_CROP_YOUNG:      APPLE_CROP_MATURE,
                    RICE_CROP_YOUNG:       RICE_CROP_MATURE,
                    GINGER_CROP_YOUNG:     GINGER_CROP_MATURE,
                    BOK_CHOY_CROP_YOUNG:   BOK_CHOY_CROP_MATURE,
                    GARLIC_CROP_YOUNG:     GARLIC_CROP_MATURE,
                    SCALLION_CROP_YOUNG:   SCALLION_CROP_MATURE,
                    CHILI_CROP_YOUNG:      CHILI_CROP_MATURE,
                    PEPPER_CROP_YOUNG:     PEPPER_CROP_MATURE,
                    ONION_CROP_YOUNG:      ONION_CROP_MATURE,
                    POTATO_CROP_YOUNG:     POTATO_CROP_MATURE,
                    EGGPLANT_CROP_YOUNG:   EGGPLANT_CROP_MATURE,
                    CABBAGE_CROP_YOUNG:    CABBAGE_CROP_MATURE,
                }
                self.set_block(x, y, _crop_mature_map[bid])
            else:
                still_pending.add((x, y))
        self.pending_crops = still_pending

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
                    if bid not in ALL_LEAVES:
                        continue
                    x = base_x + lx
                    log_bid = LEAF_LOG_MAP[bid]
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

        for (x, y) in to_remove:
            self.set_block(x, y, AIR)
            if self._leaves_rng.random() < 0.25:
                player._add_item("sapling")

    def _spawn_animals(self):
        from animals import Sheep, Cow, Chicken
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
