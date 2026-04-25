import sqlite3
import zlib
import struct
import json
from datetime import datetime
from pathlib import Path

from constants import CHUNK_W, WORLD_H

DB_PATH = Path(__file__).parent / "collectorblocks.db"


def _wf_to_dict(wf):
    return {
        "uid": wf.uid, "flower_type": wf.flower_type, "rarity": wf.rarity,
        "bloom_stage": wf.bloom_stage,
        "primary_color": list(wf.primary_color),
        "secondary_color": list(wf.secondary_color),
        "center_color": list(wf.center_color),
        "petal_pattern": wf.petal_pattern, "petal_count": wf.petal_count,
        "fragrance": wf.fragrance, "vibrancy": wf.vibrancy,
        "specials": wf.specials, "biodome_found": wf.biodome_found, "seed": wf.seed,
    }
SAVE_VERSION = 2


class SaveManager:
    def __init__(self, db_path=None):
        self.db_path = Path(db_path) if db_path else DB_PATH

    def new_game(self):
        """Wipe all saved state so a new World generates fresh terrain."""
        try:
            with sqlite3.connect(self.db_path) as con:
                self._create_tables(con)
                for tbl in ("save_meta", "chunks", "bg_chunks", "world_meta", "player",
                            "rocks", "wildflowers", "fossils", "gems", "bird_observations",
                            "insect_observations",
                            "fish", "coffee_beans", "wine_grapes", "spirits",
                            "tea_leaves", "textiles", "cheese_wheels", "jewelry", "sculptures", "pottery_pieces",
                            "research", "automations",
                            "farm_bots", "backhoes", "elevator_cars", "entities", "dropped_items", "chests"):
                    # global_collection and achievements are intentionally preserved
                    con.execute(f"DELETE FROM {tbl}")
                con.commit()
        except Exception:
            pass

    def has_save(self):
        if not self.db_path.exists():
            return False
        try:
            with sqlite3.connect(self.db_path) as con:
                row = con.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='save_meta'"
                ).fetchone()
                if row is None:
                    return False
                row = con.execute("SELECT seed FROM save_meta LIMIT 1").fetchone()
                return row is not None
        except Exception:
            return False

    def save(self, world, player, research):
        """Save game state. Returns list of newly unlocked Achievement objects."""
        with sqlite3.connect(self.db_path) as con:
            self._create_tables(con)
            self._save_meta(con, world.seed)
            self._save_dirty_chunks(con, world)
            self._save_world_meta(con, world, player)
            self._save_player(con, player)
            self._save_rocks(con, player)
            self._save_wildflowers(con, player)
            self._save_fossils(con, player)
            self._save_gems(con, player)
            self._save_fish(con, player)
            self._save_coffee_beans(con, player)
            self._save_wine_grapes(con, player)
            self._save_spirits(con, player)
            self._save_tea_leaves(con, player)
            self._save_textiles(con, player)
            self._save_cheese_wheels(con, player)
            self._save_jewelry(con, player)
            self._save_sculptures(con, player)
            self._save_pottery_pieces(con, player)
            self._save_bird_observations(con, player)
            self._save_insect_observations(con, player)
            self._save_research(con, research)
            self._save_automations(con, world)
            self._save_farm_bots(con, world)
            self._save_backhoes(con, world)
            self._save_elevator_cars(con, world)
            self._save_entities(con, world)
            self._save_dropped_items(con, world)
            self._save_chests(con, world)
            self._merge_global_collection(con, player)
            newly_unlocked = self._check_and_save_achievements(con)
            con.commit()
        return newly_unlocked

    def load(self):
        with sqlite3.connect(self.db_path) as con:
            self._create_tables(con)
            self._maybe_migrate(con)
            seed = con.execute("SELECT seed FROM save_meta LIMIT 1").fetchone()[0]
            world_meta  = self._load_world_meta(con)
            bird_obs    = self._load_bird_observations(con)
            insect_obs  = self._load_insect_observations(con)
            player_data = self._load_player(con, bird_obs, insect_obs)
            automations = self._load_automations(con)
            farm_bots = self._load_farm_bots(con)
            backhoes = self._load_backhoes(con)
            elevator_cars = self._load_elevator_cars(con)
            entities = self._load_entities(con)
            research = self._load_research(con)
            dropped_items = self._load_dropped_items(con)
            chest_data = self._load_chests(con)
        return {
            "seed": seed,
            "water_level":     world_meta["water_level"],
            "soil_moisture":   world_meta["soil_moisture"],
            "soil_fertility":  world_meta["soil_fertility"],
            "crop_progress":   world_meta["crop_progress"],
            "crop_care_sum":   world_meta["crop_care_sum"],
            "compost_bin_data":    world_meta["compost_bin_data"],
            "garden_data":             world_meta["garden_data"],
            "sculpture_positions":     world_meta.get("sculpture_positions", {}),
            "wildflower_display_data": world_meta.get("wildflower_display_data", {}),
            "pottery_display_data":    world_meta.get("pottery_display_data", {}),
            "unplaced_vase_uids":      world_meta.get("unplaced_vase_uids", []),
            "player": player_data,
            "automations": automations,
            "farm_bots": farm_bots,
            "backhoes": backhoes,
            "elevator_cars": elevator_cars,
            "entities": entities,
            "research": research,
            "dropped_items": dropped_items,
            "chest_data": chest_data,
        }

    def load_chunk(self, chunk_x):
        """Load a single chunk from DB. Returns 2-D list [y][lx] or None."""
        try:
            with sqlite3.connect(self.db_path) as con:
                row = con.execute(
                    "SELECT data FROM chunks WHERE chunk_x=?", (chunk_x,)
                ).fetchone()
        except Exception:
            return None
        if row is None:
            return None
        flat = struct.unpack(f"<{CHUNK_W * WORLD_H}H", zlib.decompress(row[0]))
        return [[flat[y * CHUNK_W + lx] for lx in range(CHUNK_W)]
                for y in range(WORLD_H)]

    def save_chunk(self, chunk_x, chunk):
        """Immediately persist a single chunk to DB."""
        raw = struct.pack(
            f"<{CHUNK_W * WORLD_H}H",
            *[chunk[y][lx] for y in range(WORLD_H) for lx in range(CHUNK_W)],
        )
        data = zlib.compress(raw, level=1)
        with sqlite3.connect(self.db_path) as con:
            con.execute("CREATE TABLE IF NOT EXISTS chunks "
                        "(chunk_x INTEGER PRIMARY KEY, data BLOB NOT NULL)")
            con.execute("INSERT OR REPLACE INTO chunks VALUES (?,?)", (chunk_x, data))
            con.commit()

    def save_chunks_batch(self, chunks_dict):
        """Persist multiple chunks in a single transaction."""
        if not chunks_dict:
            return
        with sqlite3.connect(self.db_path) as con:
            con.execute("CREATE TABLE IF NOT EXISTS chunks "
                        "(chunk_x INTEGER PRIMARY KEY, data BLOB NOT NULL)")
            for cx, chunk in chunks_dict.items():
                raw = struct.pack(
                    f"<{CHUNK_W * WORLD_H}H",
                    *[chunk[y][lx] for y in range(WORLD_H) for lx in range(CHUNK_W)],
                )
                con.execute("INSERT OR REPLACE INTO chunks VALUES (?,?)",
                            (cx, zlib.compress(raw, level=1)))
            con.commit()

    def load_chunks_batch(self, chunk_xs):
        """Load multiple chunks from DB in one query. Returns {cx: 2D-list}."""
        if not chunk_xs:
            return {}
        placeholders = ",".join("?" * len(chunk_xs))
        try:
            with sqlite3.connect(self.db_path) as con:
                rows = con.execute(
                    f"SELECT chunk_x, data FROM chunks WHERE chunk_x IN ({placeholders})",
                    list(chunk_xs),
                ).fetchall()
        except Exception:
            return {}
        result = {}
        for cx, data in rows:
            flat = struct.unpack(f"<{CHUNK_W * WORLD_H}H", zlib.decompress(data))
            result[cx] = [[flat[y * CHUNK_W + lx] for lx in range(CHUNK_W)]
                          for y in range(WORLD_H)]
        return result

    def load_bg_chunk(self, chunk_x):
        """Load a single background chunk from DB. Returns 2-D list or None."""
        try:
            with sqlite3.connect(self.db_path) as con:
                row = con.execute(
                    "SELECT data FROM bg_chunks WHERE chunk_x=?", (chunk_x,)
                ).fetchone()
        except Exception:
            return None
        if row is None:
            return None
        flat = struct.unpack(f"<{CHUNK_W * WORLD_H}H", zlib.decompress(row[0]))
        return [[flat[y * CHUNK_W + lx] for lx in range(CHUNK_W)]
                for y in range(WORLD_H)]

    def save_bg_chunk(self, chunk_x, chunk):
        """Immediately persist a single background chunk to DB."""
        raw = struct.pack(
            f"<{CHUNK_W * WORLD_H}H",
            *[chunk[y][lx] for y in range(WORLD_H) for lx in range(CHUNK_W)],
        )
        data = zlib.compress(raw, level=1)
        with sqlite3.connect(self.db_path) as con:
            con.execute("CREATE TABLE IF NOT EXISTS bg_chunks "
                        "(chunk_x INTEGER PRIMARY KEY, data BLOB NOT NULL)")
            con.execute("INSERT OR REPLACE INTO bg_chunks VALUES (?,?)", (chunk_x, data))
            con.commit()

    def load_bg_chunks_batch(self, chunk_xs):
        """Load multiple background chunks from DB in one query."""
        if not chunk_xs:
            return {}
        placeholders = ",".join("?" * len(chunk_xs))
        try:
            with sqlite3.connect(self.db_path) as con:
                rows = con.execute(
                    f"SELECT chunk_x, data FROM bg_chunks WHERE chunk_x IN ({placeholders})",
                    list(chunk_xs),
                ).fetchall()
        except Exception:
            return {}
        result = {}
        for cx, data in rows:
            flat = struct.unpack(f"<{CHUNK_W * WORLD_H}H", zlib.decompress(data))
            result[cx] = [[flat[y * CHUNK_W + lx] for lx in range(CHUNK_W)]
                          for y in range(WORLD_H)]
        return result

    def save_bg_chunks_batch(self, chunks_dict):
        """Persist multiple background chunks in a single transaction."""
        if not chunks_dict:
            return
        with sqlite3.connect(self.db_path) as con:
            con.execute("CREATE TABLE IF NOT EXISTS bg_chunks "
                        "(chunk_x INTEGER PRIMARY KEY, data BLOB NOT NULL)")
            for cx, chunk in chunks_dict.items():
                raw = struct.pack(
                    f"<{CHUNK_W * WORLD_H}H",
                    *[chunk[y][lx] for y in range(WORLD_H) for lx in range(CHUNK_W)],
                )
                con.execute("INSERT OR REPLACE INTO bg_chunks VALUES (?,?)",
                            (cx, zlib.compress(raw, level=1)))
            con.commit()

    # ------------------------------------------------------------------
    # Schema
    # ------------------------------------------------------------------

    def _create_tables(self, con):
        con.executescript("""
        CREATE TABLE IF NOT EXISTS save_meta (
            seed INTEGER, save_version INTEGER DEFAULT 2, last_saved TEXT
        );
        CREATE TABLE IF NOT EXISTS chunks (
            chunk_x INTEGER PRIMARY KEY,
            data    BLOB NOT NULL
        );
        CREATE TABLE IF NOT EXISTS bg_chunks (
            chunk_x INTEGER PRIMARY KEY,
            data    BLOB NOT NULL
        );
        CREATE TABLE IF NOT EXISTS world_meta (
            water_level TEXT,
            soil_moisture TEXT,
            crop_progress TEXT,
            crop_care_sum TEXT,
            soil_fertility TEXT,
            compost_bin_data TEXT,
            garden_data TEXT,
            sculpture_positions TEXT,
            wildflower_display_data TEXT,
            pottery_display_data TEXT,
            unplaced_vase_uids TEXT
        );
        CREATE TABLE IF NOT EXISTS player (
            x REAL, y REAL, vx REAL, vy REAL, facing INTEGER,
            health INTEGER, hunger REAL, pick_power INTEGER, money INTEGER,
            selected_slot INTEGER,
            inventory TEXT, hotbar TEXT, hotbar_uses TEXT, known_recipes TEXT,
            discovered_types TEXT, discovered_flower_types TEXT,
            discovered_mushroom_types TEXT, mushrooms_found TEXT,
            discovered_fossil_types TEXT
        );
        CREATE TABLE IF NOT EXISTS rocks (
            uid TEXT PRIMARY KEY, base_type TEXT, rarity TEXT, size TEXT,
            primary_color TEXT, secondary_color TEXT,
            pattern TEXT, pattern_density REAL, hardness REAL,
            luster REAL, purity REAL, specials TEXT,
            depth_found INTEGER, seed INTEGER, upgrades TEXT
        );
        CREATE TABLE IF NOT EXISTS wildflowers (
            uid TEXT PRIMARY KEY, flower_type TEXT, rarity TEXT, bloom_stage TEXT,
            primary_color TEXT, secondary_color TEXT, center_color TEXT,
            petal_pattern TEXT, petal_count INTEGER, fragrance REAL,
            vibrancy REAL, specials TEXT, biodome_found TEXT, seed INTEGER
        );
        CREATE TABLE IF NOT EXISTS fossils (
            uid TEXT PRIMARY KEY, fossil_type TEXT, rarity TEXT, size TEXT,
            primary_color TEXT, secondary_color TEXT,
            pattern TEXT, pattern_density REAL, age TEXT,
            clarity REAL, detail REAL, specials TEXT,
            depth_found INTEGER, seed INTEGER, upgrades TEXT,
            prepared INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS gems (
            uid TEXT PRIMARY KEY, gem_type TEXT, rarity TEXT, size TEXT,
            state TEXT, cut TEXT, clarity TEXT, color_saturation REAL,
            optical_effect TEXT, inclusion TEXT, crystal_system TEXT,
            primary_color TEXT, secondary_color TEXT,
            depth_found INTEGER, seed INTEGER, biome TEXT, upgrades TEXT
        );
        CREATE TABLE IF NOT EXISTS bird_observations (
            species_id TEXT PRIMARY KEY, count INTEGER, biome TEXT
        );
        CREATE TABLE IF NOT EXISTS insect_observations (
            species_id TEXT PRIMARY KEY, count INTEGER, biome TEXT
        );
        CREATE TABLE IF NOT EXISTS fish (
            uid TEXT PRIMARY KEY, species TEXT, rarity TEXT,
            weight_kg REAL, length_cm INTEGER, pattern TEXT,
            primary_color TEXT, secondary_color TEXT,
            habitat TEXT, biome_found TEXT, seed INTEGER
        );
        CREATE TABLE IF NOT EXISTS research (
            node_id TEXT PRIMARY KEY, unlocked INTEGER
        );
        CREATE TABLE IF NOT EXISTS automations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            x REAL, y REAL, auto_type TEXT, direction TEXT,
            fuel REAL, supports INTEGER,
            stored TEXT, state TEXT, halt_reason TEXT,
            blocks_since_support INTEGER
        );
        CREATE TABLE IF NOT EXISTS farm_bots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            x REAL, y REAL, bot_type TEXT,
            fuel REAL, seeds TEXT, stored TEXT, state TEXT
        );
        CREATE TABLE IF NOT EXISTS backhoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            x REAL, y REAL,
            fuel REAL, stored TEXT,
            arm_dx INTEGER, arm_dy INTEGER
        );
        CREATE TABLE IF NOT EXISTS elevator_cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shaft_x INTEGER, stop_by INTEGER, car_by INTEGER
        );
        CREATE TABLE IF NOT EXISTS entities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entity_type TEXT, x REAL, y REAL, facing INTEGER,
            animal_id TEXT, extra TEXT
        );
        CREATE TABLE IF NOT EXISTS dropped_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            x REAL, y REAL, item_id TEXT, count INTEGER, lifetime REAL
        );
        CREATE TABLE IF NOT EXISTS chests (
            x INTEGER, y INTEGER, contents TEXT
        );
        CREATE TABLE IF NOT EXISTS coffee_beans (
            uid                TEXT PRIMARY KEY,
            origin_biome       TEXT,
            variety            TEXT,
            state              TEXT,
            roast_level        TEXT,
            roast_quality      REAL,
            acidity            REAL,
            body               REAL,
            sweetness          REAL,
            earthiness         REAL,
            brightness         REAL,
            flavor_notes       TEXT,
            seed               INTEGER,
            blend_components   TEXT,
            processing_method  TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS wine_grapes (
            uid                TEXT PRIMARY KEY,
            origin_biome       TEXT,
            variety            TEXT,
            state              TEXT,
            style              TEXT,
            sweetness          REAL,
            acidity            REAL,
            tannin             REAL,
            body               REAL,
            aromatics          REAL,
            alcohol            REAL,
            complexity         REAL,
            press_quality      REAL,
            ferment_quality    REAL,
            flavor_notes       TEXT,
            seed               INTEGER,
            blend_components   TEXT,
            crush_style        TEXT DEFAULT '',
            yeast              TEXT DEFAULT '',
            vessel             TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS spirits (
            uid               TEXT PRIMARY KEY,
            origin_biome      TEXT,
            grain_type        TEXT,
            spirit_type       TEXT,
            state             TEXT,
            cut_quality       REAL,
            proof             REAL,
            grain_character   REAL,
            sweetness         REAL,
            spice             REAL,
            smokiness         REAL,
            smoothness        REAL,
            age_quality       REAL,
            flavor_notes      TEXT,
            seed              INTEGER,
            blend_components  TEXT,
            barrel_type       TEXT DEFAULT '',
            age_duration      TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS tea_leaves (
            uid               TEXT PRIMARY KEY,
            origin_biome      TEXT,
            variety           TEXT,
            state             TEXT,
            tea_type          TEXT,
            oxidation         REAL,
            astringency       REAL,
            floral            REAL,
            vegetal           REAL,
            earthiness        REAL,
            sweetness         REAL,
            steep_quality     REAL,
            complexity        REAL,
            flavor_notes      TEXT,
            seed              INTEGER,
            blend_components  TEXT,
            wither_method     TEXT DEFAULT '',
            herbal_additions  TEXT DEFAULT '[]',
            age_duration      TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS textiles (
            uid            TEXT PRIMARY KEY,
            fiber_type     TEXT,
            state          TEXT,
            output_type    TEXT,
            texture        TEXT,
            dye_family     TEXT,
            dye_color      TEXT,
            quality        REAL,
            softness       REAL,
            luster         REAL,
            pattern_quality REAL,
            seed           INTEGER
        );
        CREATE TABLE IF NOT EXISTS cheese_wheels (
            uid             TEXT PRIMARY KEY,
            origin_biome    TEXT,
            animal_type     TEXT,
            variety         TEXT,
            state           TEXT,
            richness        REAL,
            sharpness       REAL,
            nuttiness       REAL,
            saltiness       REAL,
            moisture        REAL,
            culture_quality REAL,
            age_quality     REAL,
            flavor_notes    TEXT,
            seed            INTEGER,
            blend_components TEXT,
            cheese_type     TEXT DEFAULT '',
            press_quality   REAL DEFAULT 0.0
        );
        CREATE TABLE IF NOT EXISTS jewelry (
            uid          TEXT PRIMARY KEY,
            jewelry_type TEXT,
            slot_count   INTEGER,
            slots        TEXT,
            custom_name  TEXT,
            seed         INTEGER
        );
        CREATE TABLE IF NOT EXISTS global_collection (
            category TEXT NOT NULL,
            item_id  TEXT NOT NULL,
            PRIMARY KEY (category, item_id)
        );
        CREATE TABLE IF NOT EXISTS achievements (
            id           TEXT PRIMARY KEY,
            unlocked     INTEGER DEFAULT 0,
            unlocked_date TEXT
        );
        CREATE TABLE IF NOT EXISTS sculptures (
            uid      TEXT PRIMARY KEY,
            mineral  TEXT,
            height   INTEGER,
            grid     TEXT,
            color    TEXT,
            template TEXT,
            seed     INTEGER,
            pending  INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS pottery_pieces (
            uid            TEXT PRIMARY KEY,
            clay_biome     TEXT,
            shape          TEXT,
            state          TEXT,
            firing_level   TEXT,
            firing_quality REAL,
            thickness      REAL,
            evenness       REAL,
            glaze_type     TEXT DEFAULT '',
            texture_notes  TEXT,
            seed           INTEGER,
            profile        TEXT,
            blend_components TEXT DEFAULT '[]'
        );
        """)
        for col, default in [("spawn_x", "NULL"), ("spawn_y", "NULL")]:
            try:
                con.execute(f"ALTER TABLE player ADD COLUMN {col} REAL DEFAULT {default}")
            except Exception:
                pass
        try:
            con.execute("ALTER TABLE player ADD COLUMN discovered_fossil_types TEXT DEFAULT '[]'")
        except Exception:
            pass
        try:
            con.execute("ALTER TABLE player ADD COLUMN known_crops TEXT DEFAULT '[]'")
        except Exception:
            pass
        try:
            con.execute("ALTER TABLE player ADD COLUMN discovered_foods TEXT DEFAULT '[]'")
        except Exception:
            pass
        try:
            con.execute("ALTER TABLE player ADD COLUMN foods_cooked TEXT DEFAULT '{}'")
        except Exception:
            pass
        try:
            con.execute("ALTER TABLE player ADD COLUMN worn TEXT DEFAULT '{}'")
        except Exception:
            pass
        for col in ("water_reservoir", "compost_slot"):
            try:
                con.execute(f"ALTER TABLE farm_bots ADD COLUMN {col} REAL DEFAULT 0")
            except Exception:
                pass
        for col in ("soil_moisture", "crop_progress", "crop_care_sum",
                    "soil_fertility", "compost_bin_data", "garden_data",
                    "sculpture_positions", "wildflower_display_data",
                    "pottery_display_data", "unplaced_vase_uids"):
            try:
                con.execute(f"ALTER TABLE world_meta ADD COLUMN {col} TEXT")
            except Exception:
                pass
        for col, default in [
            ("horses_tamed", "0"),
            ("horses_bred", "0"),
            ("horse_records", "'{}'"),
            ("discovered_coat_biomes", "'[]'"),
            ("discovered_recipes", "'[]'"),
            ("animals_hunted", "'{}'"),
            ("roast_profiles", "'[]'"),
        ]:
            try:
                con.execute(f"ALTER TABLE player ADD COLUMN {col} TEXT DEFAULT {default}")
            except Exception:
                pass
        for col in ("crush_style", "yeast", "vessel"):
            try:
                con.execute(f"ALTER TABLE wine_grapes ADD COLUMN {col} TEXT DEFAULT ''")
            except Exception:
                pass
        for col in ("barrel_type", "age_duration"):
            try:
                con.execute(f"ALTER TABLE spirits ADD COLUMN {col} TEXT DEFAULT ''")
            except Exception:
                pass
        for col, default in [("wither_method", "''"), ("herbal_additions", "'[]'"), ("age_duration", "''")]:
            try:
                con.execute(f"ALTER TABLE tea_leaves ADD COLUMN {col} TEXT DEFAULT {default}")
            except Exception:
                pass
        for col, default in [("cheese_type", "''"), ("press_quality", "0.0")]:
            try:
                con.execute(f"ALTER TABLE cheese_wheels ADD COLUMN {col} DEFAULT {default}")
            except Exception:
                pass

    # ------------------------------------------------------------------
    # Achievements (global, cross-save)
    # ------------------------------------------------------------------

    def _merge_global_collection(self, con, player):
        """Accumulate this player's discoveries into the global collection table."""
        for bid in player.discovered_mushroom_types:
            con.execute(
                "INSERT OR IGNORE INTO global_collection VALUES (?, ?)",
                ("mushroom", str(bid)),
            )
        for t in player.discovered_types:
            con.execute(
                "INSERT OR IGNORE INTO global_collection VALUES (?, ?)",
                ("rock", t),
            )
        for t in player.discovered_flower_types:
            con.execute(
                "INSERT OR IGNORE INTO global_collection VALUES (?, ?)",
                ("wildflower", t),
            )
        for t in player.discovered_fossil_types:
            con.execute(
                "INSERT OR IGNORE INTO global_collection VALUES (?, ?)",
                ("fossil", t),
            )
        for t in player.discovered_gem_types:
            con.execute(
                "INSERT OR IGNORE INTO global_collection VALUES (?, ?)",
                ("gem", t),
            )
        for t in player.discovered_fish_species:
            con.execute(
                "INSERT OR IGNORE INTO global_collection VALUES (?, ?)",
                ("fish", t),
            )
        for t in player.discovered_coffee_origins:
            con.execute(
                "INSERT OR IGNORE INTO global_collection VALUES (?, ?)",
                ("coffee", t),
            )
        for t in player.discovered_wine_origins:
            con.execute(
                "INSERT OR IGNORE INTO global_collection VALUES (?, ?)",
                ("wine", t),
            )
        for t in player.discovered_spirit_types:
            con.execute(
                "INSERT OR IGNORE INTO global_collection VALUES (?, ?)",
                ("spirit", t),
            )

    def _check_and_save_achievements(self, con):
        """Check all achievements against global_collection; persist new unlocks.

        Returns list of newly unlocked Achievement objects.
        """
        from achievements import ACHIEVEMENTS
        rows = con.execute("SELECT category, item_id FROM global_collection").fetchall()
        global_col = {}
        for cat, item_id in rows:
            global_col.setdefault(cat, set()).add(item_id)

        already = {
            row[0]
            for row in con.execute("SELECT id FROM achievements WHERE unlocked=1").fetchall()
        }

        newly_unlocked = []
        for ach in ACHIEVEMENTS:
            if ach.id in already:
                continue
            cat_items = global_col.get(ach.category, set())
            if all(str(r) in cat_items for r in ach.required_items):
                con.execute(
                    "INSERT OR REPLACE INTO achievements VALUES (?, 1, ?)",
                    (ach.id, datetime.now().isoformat()),
                )
                newly_unlocked.append(ach)
        return newly_unlocked

    def load_achievements(self):
        """Return (unlocked_dict, global_collection_dict).

        unlocked_dict: {achievement_id: bool}
        global_collection_dict: {category: set_of_item_id_strings}
        """
        from achievements import ACHIEVEMENTS
        try:
            with sqlite3.connect(self.db_path) as con:
                self._create_tables(con)
                ach_rows = con.execute("SELECT id, unlocked FROM achievements").fetchall()
                col_rows = con.execute("SELECT category, item_id FROM global_collection").fetchall()
        except Exception:
            ach_rows, col_rows = [], []

        unlocked = {row[0]: bool(row[1]) for row in ach_rows}
        global_col: dict = {}
        for cat, item_id in col_rows:
            global_col.setdefault(cat, set()).add(item_id)

        unlocked_dict = {ach.id: unlocked.get(ach.id, False) for ach in ACHIEVEMENTS}
        return unlocked_dict, global_col

    # ------------------------------------------------------------------
    # Migration: old world_grid BLOB → per-chunk rows
    # ------------------------------------------------------------------

    def _maybe_migrate(self, con):
        has_grid = con.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='world_grid'"
        ).fetchone()
        if not has_grid:
            return

        already_done = con.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
        if already_done > 0:
            return

        blob_row = con.execute("SELECT data FROM world_grid LIMIT 1").fetchone()
        if blob_row is None:
            return

        OLD_W = 300
        OFFSET = OLD_W // 2  # old spawn was at x=150; map to new x=0

        raw = zlib.decompress(blob_row[0])
        flat = list(struct.unpack(f"{OLD_W * WORLD_H}h", raw))
        old_grid = [[flat[y * OLD_W + x] for x in range(OLD_W)] for y in range(WORLD_H)]

        chunks_dict = {}
        for old_x in range(OLD_W):
            new_x = old_x - OFFSET
            cx = new_x // CHUNK_W
            lx = new_x % CHUNK_W  # Python mod is always non-negative
            if cx not in chunks_dict:
                chunks_dict[cx] = [[0] * CHUNK_W for _ in range(WORLD_H)]
            for y in range(WORLD_H):
                chunks_dict[cx][y][lx] = old_grid[y][old_x]

        for cx, chunk in chunks_dict.items():
            raw_chunk = struct.pack(
                f"<{CHUNK_W * WORLD_H}H",
                *[chunk[y][lx] for y in range(WORLD_H) for lx in range(CHUNK_W)],
            )
            data = zlib.compress(raw_chunk, level=1)
            con.execute("INSERT OR REPLACE INTO chunks VALUES (?,?)", (cx, data))

        # Migrate world_meta water_level from old multi-column row
        old_meta = con.execute(
            "SELECT water_level FROM world_meta LIMIT 1"
        ).fetchone()
        if old_meta:
            con.execute("DELETE FROM world_meta")
            con.execute("INSERT INTO world_meta (water_level) VALUES (?)", (old_meta[0],))

        con.commit()

    # ------------------------------------------------------------------
    # Save helpers
    # ------------------------------------------------------------------

    def _save_meta(self, con, seed):
        con.execute("DELETE FROM save_meta")
        con.execute("INSERT INTO save_meta VALUES (?, ?, ?)",
                    (seed, SAVE_VERSION, datetime.now().isoformat()))

    def _save_dirty_chunks(self, con, world):
        for cx in list(world._dirty_chunks):
            if cx not in world._chunks:
                continue
            chunk = world._chunks[cx]
            raw = struct.pack(
                f"<{CHUNK_W * WORLD_H}H",
                *[chunk[y][lx] for y in range(WORLD_H) for lx in range(CHUNK_W)],
            )
            data = zlib.compress(raw, level=1)
            con.execute("INSERT OR REPLACE INTO chunks VALUES (?,?)", (cx, data))
        world._dirty_chunks.clear()
        for cx in list(world._dirty_bg_chunks):
            if cx not in world._bg_chunks:
                continue
            chunk = world._bg_chunks[cx]
            raw = struct.pack(
                f"<{CHUNK_W * WORLD_H}H",
                *[chunk[y][lx] for y in range(WORLD_H) for lx in range(CHUNK_W)],
            )
            data = zlib.compress(raw, level=1)
            con.execute("INSERT OR REPLACE INTO bg_chunks VALUES (?,?)", (cx, data))
        world._dirty_bg_chunks.clear()

    def _save_world_meta(self, con, world, player=None):
        water        = {f"{x},{y}": lvl    for (x, y), lvl   in world._water_level.items()}
        moisture     = {f"{x},{y}": m      for (x, y), m     in world._soil_moisture.items()}
        fertility    = {f"{x},{y}": f      for (x, y), f     in world._soil_fertility.items()}
        progress     = {f"{x},{y}": p      for (x, y), p     in world._crop_progress.items()}
        care_sum     = {f"{x},{y}": [s, c] for (x, y), (s, c) in world._crop_care_sum.items()}
        compost_bins = {f"{x},{y}": d      for (x, y), d     in world.compost_bin_data.items()}
        garden_flowers = {
            f"{x},{y}": [_wf_to_dict(wf) for wf in flowers]
            for (x, y), flowers in world.garden_data.items()
            if flowers
        }
        # sculpture_positions: "bx,by" -> uid (root) or {"root": "rbx,rby"} (body)
        sculpture_pos = {}
        for (x, y), data in world.sculpture_data.items():
            if isinstance(data, dict) and "root" in data:
                rbx, rby = data["root"]
                sculpture_pos[f"{x},{y}"] = {"root": f"{rbx},{rby}"}
            else:
                sculpture_pos[f"{x},{y}"] = data.uid
        wf_displays = {
            f"{x},{y}": _wf_to_dict(wf)
            for (x, y), wf in world.wildflower_display_data.items()
            if wf is not None
        }
        import dataclasses
        pottery_displays = {
            f"{x},{y}": dataclasses.asdict(piece)
            for (x, y), piece in world.pottery_display_data.items()
        }
        unplaced_uids = [p.uid for p in (player.unplaced_vases if player else [])]
        con.execute("DELETE FROM world_meta")
        con.execute(
            "INSERT INTO world_meta "
            "(water_level, soil_moisture, crop_progress, crop_care_sum, soil_fertility, compost_bin_data, garden_data, sculpture_positions, wildflower_display_data, pottery_display_data, unplaced_vase_uids) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (json.dumps(water), json.dumps(moisture), json.dumps(progress),
             json.dumps(care_sum), json.dumps(fertility), json.dumps(compost_bins),
             json.dumps(garden_flowers), json.dumps(sculpture_pos), json.dumps(wf_displays),
             json.dumps(pottery_displays), json.dumps(unplaced_uids)),
        )

    def _save_player(self, con, player):
        con.execute("DELETE FROM player")
        mushrooms = {str(k): v for k, v in player.mushrooms_found.items()}
        con.execute(
            """INSERT INTO player
               (x, y, vx, vy, facing, health, hunger, pick_power, money,
                selected_slot, inventory, hotbar, hotbar_uses, known_recipes,
                discovered_types, discovered_flower_types,
                discovered_mushroom_types, mushrooms_found,
                spawn_x, spawn_y, discovered_fossil_types, known_crops,
                discovered_foods, foods_cooked,
                horses_tamed, horses_bred, horse_records, discovered_coat_biomes,
                discovered_recipes, animals_hunted, roast_profiles)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                player.x, player.y, player.vx, player.vy, player.facing,
                player.health, player.hunger, player.pick_power, player.money,
                player.selected_slot,
                json.dumps(player.inventory),
                json.dumps(player.hotbar),
                json.dumps(player.hotbar_uses),
                json.dumps(list(player.known_recipes)),
                json.dumps(list(player.discovered_types)),
                json.dumps(list(player.discovered_flower_types)),
                json.dumps([str(x) for x in player.discovered_mushroom_types]),
                json.dumps(mushrooms),
                player.spawn_x, player.spawn_y,
                json.dumps(list(player.discovered_fossil_types)),
                json.dumps(list(player.known_crops)),
                json.dumps(list(player.discovered_foods)),
                json.dumps(player.foods_cooked),
                getattr(player, "horses_tamed", 0),
                getattr(player, "horses_bred", 0),
                json.dumps(getattr(player, "horse_records", {})),
                json.dumps(list(getattr(player, "discovered_coat_biomes", set()))),
                json.dumps(list(getattr(player, "discovered_recipes", set()))),
                json.dumps(getattr(player, "animals_hunted", {})),
                json.dumps(getattr(player, "roast_profiles", [])),
            )
        )

    def _save_rocks(self, con, player):
        con.execute("DELETE FROM rocks")
        for r in player.rocks:
            con.execute(
                "INSERT OR REPLACE INTO rocks VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    r.uid, r.base_type, r.rarity, r.size,
                    json.dumps(list(r.primary_color)),
                    json.dumps(list(r.secondary_color)),
                    r.pattern, r.pattern_density, r.hardness,
                    r.luster, r.purity,
                    json.dumps(r.specials),
                    r.depth_found, r.seed,
                    json.dumps(r.upgrades),
                )
            )

    def _save_wildflowers(self, con, player):
        con.execute("DELETE FROM wildflowers")
        for wf in player.wildflowers:
            con.execute(
                "INSERT OR REPLACE INTO wildflowers VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    wf.uid, wf.flower_type, wf.rarity, wf.bloom_stage,
                    json.dumps(list(wf.primary_color)),
                    json.dumps(list(wf.secondary_color)),
                    json.dumps(list(wf.center_color)),
                    wf.petal_pattern, wf.petal_count, wf.fragrance,
                    wf.vibrancy, json.dumps(wf.specials),
                    wf.biodome_found, wf.seed,
                )
            )

    def _save_fossils(self, con, player):
        try:
            con.execute("ALTER TABLE fossils ADD COLUMN prepared INTEGER DEFAULT 0")
        except Exception:
            pass
        con.execute("DELETE FROM fossils")
        for f in player.fossils:
            con.execute(
                "INSERT OR REPLACE INTO fossils VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    f.uid, f.fossil_type, f.rarity, f.size,
                    json.dumps(list(f.primary_color)),
                    json.dumps(list(f.secondary_color)),
                    f.pattern, f.pattern_density, f.age,
                    f.clarity, f.detail,
                    json.dumps(f.specials),
                    f.depth_found, f.seed,
                    json.dumps(f.upgrades),
                    1 if f.prepared else 0,
                )
            )

    def _save_gems(self, con, player):
        con.execute("DELETE FROM gems")
        for g in player.gems:
            con.execute(
                "INSERT OR REPLACE INTO gems VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    g.uid, g.gem_type, g.rarity, g.size,
                    g.state, g.cut, g.clarity,
                    g.color_saturation, g.optical_effect, g.inclusion, g.crystal_system,
                    json.dumps(list(g.primary_color)),
                    json.dumps(list(g.secondary_color)),
                    g.depth_found, g.seed, g.biome,
                    json.dumps(g.upgrades),
                )
            )

    def _save_fish(self, con, player):
        con.execute("DELETE FROM fish")
        for f in player.fish_caught:
            con.execute(
                "INSERT OR REPLACE INTO fish VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (
                    f.uid, f.species, f.rarity,
                    f.weight_kg, f.length_cm, f.pattern,
                    json.dumps(list(f.primary_color)),
                    json.dumps(list(f.secondary_color)),
                    f.habitat, f.biome_found, f.seed,
                )
            )

    def _save_coffee_beans(self, con, player):
        try:
            con.execute("ALTER TABLE coffee_beans ADD COLUMN processing_method TEXT DEFAULT ''")
        except Exception:
            pass
        try:
            con.execute("ALTER TABLE coffee_beans ADD COLUMN terroir_quality REAL DEFAULT 0.0")
        except Exception:
            pass
        con.execute("DELETE FROM coffee_beans")
        for b in player.coffee_beans:
            con.execute(
                "INSERT OR REPLACE INTO coffee_beans VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    b.uid, b.origin_biome, b.variety, b.state, b.roast_level,
                    b.roast_quality, b.acidity, b.body, b.sweetness, b.earthiness, b.brightness,
                    json.dumps(b.flavor_notes), b.seed,
                    json.dumps(b.blend_components),
                    getattr(b, "processing_method", ""),
                    getattr(b, "terroir_quality", 0.0),
                )
            )

    def _save_wine_grapes(self, con, player):
        con.execute("DELETE FROM wine_grapes")
        for g in player.wine_grapes:
            con.execute(
                "INSERT OR REPLACE INTO wine_grapes VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    g.uid, g.origin_biome, g.variety, g.state, g.style,
                    g.sweetness, g.acidity, g.tannin, g.body, g.aromatics,
                    g.alcohol, g.complexity, g.press_quality, g.ferment_quality,
                    json.dumps(g.flavor_notes), g.seed,
                    json.dumps(g.blend_components),
                    getattr(g, "crush_style", ""),
                    getattr(g, "yeast", ""),
                    getattr(g, "vessel", ""),
                )
            )

    def _save_spirits(self, con, player):
        con.execute("DELETE FROM spirits")
        for s in player.spirits:
            con.execute(
                "INSERT OR REPLACE INTO spirits VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    s.uid, s.origin_biome, s.grain_type, s.spirit_type, s.state,
                    s.cut_quality, s.proof,
                    s.grain_character, s.sweetness, s.spice, s.smokiness, s.smoothness,
                    s.age_quality,
                    json.dumps(s.flavor_notes), s.seed,
                    json.dumps(s.blend_components),
                    getattr(s, "barrel_type", ""),
                    getattr(s, "age_duration", ""),
                )
            )

    def _save_tea_leaves(self, con, player):
        con.execute("DELETE FROM tea_leaves")
        for x in player.tea_leaves:
            con.execute(
                "INSERT OR REPLACE INTO tea_leaves VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    x.uid, x.origin_biome, x.variety, x.state, x.tea_type,
                    x.oxidation, x.astringency, x.floral, x.vegetal,
                    x.earthiness, x.sweetness, x.steep_quality, x.complexity,
                    json.dumps(x.flavor_notes), x.seed,
                    json.dumps(x.blend_components),
                    getattr(x, "wither_method", ""),
                    json.dumps(getattr(x, "herbal_additions", [])),
                    getattr(x, "age_duration", ""),
                )
            )

    def _save_textiles(self, con, player):
        con.execute("DELETE FROM textiles")
        for t in player.textiles:
            con.execute(
                "INSERT OR REPLACE INTO textiles VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    t.uid, t.fiber_type, t.state, t.output_type, t.texture,
                    t.dye_family, json.dumps(t.dye_color),
                    t.quality, t.softness, t.luster, t.pattern_quality, t.seed,
                )
            )
        # Save worn slots as JSON in player table
        con.execute(
            "UPDATE player SET worn = ?",
            (json.dumps(player.worn),)
        )

    def _save_cheese_wheels(self, con, player):
        con.execute("DELETE FROM cheese_wheels")
        for c in player.cheese_wheels:
            con.execute(
                "INSERT OR REPLACE INTO cheese_wheels VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    c.uid, c.origin_biome, c.animal_type, c.variety, c.state,
                    c.richness, c.sharpness, c.nuttiness, c.saltiness, c.moisture,
                    c.culture_quality, c.age_quality,
                    json.dumps(c.flavor_notes), c.seed,
                    json.dumps(c.blend_components),
                    getattr(c, "cheese_type", ""),
                    getattr(c, "press_quality", 0.0),
                )
            )

    def _save_jewelry(self, con, player):
        con.execute("DELETE FROM jewelry")
        for j in player.jewelry:
            con.execute(
                "INSERT OR REPLACE INTO jewelry VALUES (?,?,?,?,?,?)",
                (j.uid, j.jewelry_type, j.slot_count, json.dumps(j.slots), j.custom_name, j.seed),
            )

    def _save_sculptures(self, con, player):
        con.execute("DELETE FROM sculptures")
        all_sc = player.sculptures_created[:]
        pending_uids = {sc.uid for sc in player.pending_sculptures}
        for sc in all_sc:
            con.execute(
                "INSERT OR REPLACE INTO sculptures VALUES (?,?,?,?,?,?,?,?)",
                (sc.uid, sc.mineral, sc.height,
                 json.dumps(sc.grid), json.dumps(list(sc.color)),
                 sc.template, sc.seed,
                 1 if sc.uid in pending_uids else 0),
            )

    def _save_pottery_pieces(self, con, player):
        con.execute("DELETE FROM pottery_pieces")
        for p in player.pottery_pieces:
            con.execute(
                "INSERT OR REPLACE INTO pottery_pieces VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    p.uid, p.clay_biome, p.shape, p.state, p.firing_level,
                    p.firing_quality, p.thickness, p.evenness,
                    getattr(p, "glaze_type", ""),
                    json.dumps(p.texture_notes), p.seed,
                    json.dumps(p.profile),
                    json.dumps(getattr(p, "blend_components", [])),
                )
            )

    def _save_bird_observations(self, con, player):
        con.execute("DELETE FROM bird_observations")
        for species_id, data in player.birds_observed.items():
            con.execute(
                "INSERT INTO bird_observations VALUES (?,?,?)",
                (species_id, data.get("count", 0), data.get("biome", "")),
            )

    def _load_bird_observations(self, con):
        try:
            rows = con.execute(
                "SELECT species_id, count, biome FROM bird_observations"
            ).fetchall()
        except Exception:
            return {}
        return {row[0]: {"count": row[1], "biome": row[2]} for row in rows}

    def _save_insect_observations(self, con, player):
        con.execute("DELETE FROM insect_observations")
        for species_id, data in player.insects_observed.items():
            con.execute(
                "INSERT INTO insect_observations VALUES (?,?,?)",
                (species_id, data.get("count", 0), data.get("biome", "")),
            )

    def _load_insect_observations(self, con):
        try:
            rows = con.execute(
                "SELECT species_id, count, biome FROM insect_observations"
            ).fetchall()
        except Exception:
            return {}
        return {row[0]: {"count": row[1], "biome": row[2]} for row in rows}

    def _save_research(self, con, research):
        con.execute("DELETE FROM research")
        for node_id, node in research.nodes.items():
            con.execute("INSERT INTO research VALUES (?, ?)",
                        (node_id, 1 if node.unlocked else 0))

    def _save_automations(self, con, world):
        con.execute("DELETE FROM automations")
        for a in world.automations:
            con.execute(
                """INSERT INTO automations
                   (x, y, auto_type, direction, fuel, supports, stored,
                    state, halt_reason, blocks_since_support)
                   VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (
                    a.x, a.y, a.auto_type, json.dumps(list(a.direction)),
                    a.fuel, 0,
                    json.dumps(a.stored),
                    a._state, a._halt_reason,
                    0,
                )
            )

    def _save_farm_bots(self, con, world):
        con.execute("DELETE FROM farm_bots")
        for fb in world.farm_bots:
            con.execute(
                "INSERT INTO farm_bots (x, y, bot_type, fuel, seeds, stored, state, "
                "water_reservoir, compost_slot) VALUES (?,?,?,?,?,?,?,?,?)",
                (fb.x, fb.y, fb.bot_type, fb.fuel,
                 json.dumps(fb.seeds), json.dumps(fb.stored), fb._state,
                 fb.water_reservoir, fb.compost_slot)
            )

    def _save_backhoes(self, con, world):
        con.execute("DELETE FROM backhoes")
        for bh in world.backhoes:
            con.execute(
                "INSERT INTO backhoes (x, y, fuel, stored, arm_dx, arm_dy) VALUES (?,?,?,?,?,?)",
                (bh.x, bh.y, bh.fuel, json.dumps(bh.stored), bh.arm_dx, bh.arm_dy)
            )

    def _save_elevator_cars(self, con, world):
        con.execute("DELETE FROM elevator_cars")
        for car in world.elevator_cars:
            car_by = int(car.car_y // 32)  # BLOCK_SIZE = 32
            con.execute(
                "INSERT INTO elevator_cars (shaft_x, stop_by, car_by) VALUES (?,?,?)",
                (car.shaft_x, int(car.car_y // 32), car_by)
            )

    def _load_elevator_cars(self, con):
        try:
            rows = con.execute("SELECT shaft_x, stop_by, car_by FROM elevator_cars").fetchall()
        except Exception:
            return []
        return [{"shaft_x": r[0], "stop_by": r[1], "car_by": r[2]} for r in rows]

    def _save_entities(self, con, world):
        from animals import Sheep, Cow, Chicken, Goat, SnowLeopard, MountainLion
        from horses import Horse
        from cities import NPC
        con.execute("DELETE FROM entities")
        for e in world.entities:
            if isinstance(e, NPC):
                continue
            traits_dict = {}
            if hasattr(e, 'traits'):
                traits_dict = {
                    "color_shift": list(e.traits["color_shift"]),
                    "size":        e.traits["size"],
                    "productivity": e.traits.get("productivity", 1.0),
                    "mutation":    e.traits.get("mutation"),
                }
                if isinstance(e, Horse):
                    traits_dict["speed_rating"]     = e.traits["speed_rating"]
                    traits_dict["stamina_max"]       = e.traits["stamina_max"]
                    traits_dict["temperament"]       = e.traits["temperament"]
                    traits_dict["coat_color"]        = list(e.traits["coat_color"])
                    traits_dict["horseshoe_applied"] = e.traits.get("horseshoe_applied", False)
                    traits_dict["endurance"]         = e.traits.get("endurance", 1.0)
                    traits_dict["gait"]              = e.traits.get("gait", 1.0)
                    traits_dict["coat_pattern"]  = e.traits.get("coat_pattern", "solid")
                    traits_dict["leg_marking"]   = e.traits.get("leg_marking", "none")
                    traits_dict["mane_color"]    = e.traits.get("mane_color", "match")
                    traits_dict["face_marking"]  = e.traits.get("face_marking", "none")
                elif isinstance(e, Sheep):
                    traits_dict["wool_color"] = e.traits.get("wool_color", "white")
                    traits_dict["fleece"]     = e.traits.get("fleece", 1.0)
                    traits_dict["birth"]      = e.traits.get("birth", "single")
                elif isinstance(e, Cow):
                    traits_dict["milk_richness"] = e.traits.get("milk_richness", 1.0)
                    traits_dict["hide"]          = e.traits.get("hide", "solid")
                elif isinstance(e, Goat):
                    traits_dict["milk_richness"] = e.traits.get("milk_richness", 1.0)
                    traits_dict["coat_color"]    = e.traits.get("coat_color", "tan")
                elif isinstance(e, Chicken):
                    traits_dict["lay_rate"] = e.traits.get("lay_rate", 1.0)
                    traits_dict["plumage"]  = e.traits.get("plumage", "white")
            extra = {
                "uid":           getattr(e, 'uid', None),
                "parent_a_uid":  getattr(e, 'parent_a_uid', None),
                "parent_b_uid":  getattr(e, 'parent_b_uid', None),
                "traits":        traits_dict,
                "genotype":      getattr(e, 'genotype', {}),
                "no_breed":      getattr(e, 'no_breed', False),
                "health":          getattr(e, 'health', 3),
                "dead":            getattr(e, 'dead', False),
                "_breed_cooldown": getattr(e, '_breed_cooldown', 60.0),
                "tamed":           getattr(e, 'tamed', False),
                "tame_progress":   getattr(e, 'tame_progress', 0),
            }
            if isinstance(e, Sheep):
                extra["has_wool"] = e.has_wool
                extra["has_milk"] = e.has_milk
            elif isinstance(e, Cow):
                extra["has_milk"] = e.has_milk
            elif isinstance(e, Goat):
                extra["has_milk"] = e.has_milk
            elif isinstance(e, Chicken):
                extra["has_egg"] = e.has_egg
            elif isinstance(e, Horse):
                extra["stamina"] = e.stamina
                extra["broken"]  = e._broken
            con.execute(
                "INSERT INTO entities (entity_type, x, y, facing, animal_id, extra) VALUES (?,?,?,?,?,?)",
                (type(e).__name__, e.x, e.y, e.facing, e.animal_id, json.dumps(extra))
            )

    def _save_chests(self, con, world):
        con.execute("DELETE FROM chests")
        for (bx, by), inv in world.chest_data.items():
            non_empty = {k: v for k, v in inv.items() if v > 0}
            if non_empty:
                con.execute("INSERT INTO chests (x, y, contents) VALUES (?,?,?)",
                            (bx, by, json.dumps(non_empty)))

    def _save_dropped_items(self, con, world):
        con.execute("DELETE FROM dropped_items")
        for item in world.dropped_items:
            con.execute(
                "INSERT INTO dropped_items (x, y, item_id, count, lifetime) VALUES (?,?,?,?,?)",
                (item.x, item.y, item.item_id, item.count, item._life)
            )

    # ------------------------------------------------------------------
    # Load helpers
    # ------------------------------------------------------------------

    def _load_world_meta(self, con):
        try:
            con.execute("SELECT garden_data FROM world_meta LIMIT 1")
        except Exception:
            pass
        row = con.execute(
            "SELECT water_level, soil_moisture, crop_progress, crop_care_sum, "
            "soil_fertility, compost_bin_data, garden_data, sculpture_positions, "
            "wildflower_display_data, "
            "COALESCE(pottery_display_data, '{}'), COALESCE(unplaced_vase_uids, '[]') "
            "FROM world_meta LIMIT 1"
        ).fetchone()
        if row is None:
            return {"water_level": {}, "soil_moisture": {}, "crop_progress": {},
                    "crop_care_sum": {}, "soil_fertility": {}, "compost_bin_data": {},
                    "garden_data": {}, "sculpture_positions": {}, "wildflower_display_data": {},
                    "pottery_display_data": {}, "unplaced_vase_uids": []}

        def _parse_coord_dict(raw, transform=lambda v: v):
            if raw is None:
                return {}
            out = {}
            for key, val in json.loads(raw).items():
                xs, ys = key.split(",")
                out[(int(xs), int(ys))] = transform(val)
            return out

        def _parse_bin_data(raw):
            if raw is None:
                return {}
            return json.loads(raw)

        def _parse_garden_data(raw):
            if not raw:
                return {}
            from wildflowers import Wildflower
            result = {}
            for key, flowers in json.loads(raw).items():
                xs, ys = key.split(",")
                result[(int(xs), int(ys))] = [
                    Wildflower(
                        uid=f["uid"], flower_type=f["flower_type"], rarity=f["rarity"],
                        bloom_stage=f["bloom_stage"],
                        primary_color=tuple(f["primary_color"]),
                        secondary_color=tuple(f["secondary_color"]),
                        center_color=tuple(f["center_color"]),
                        petal_pattern=f["petal_pattern"], petal_count=f["petal_count"],
                        fragrance=f["fragrance"], vibrancy=f["vibrancy"],
                        specials=f["specials"], biodome_found=f["biodome_found"], seed=f["seed"],
                    )
                    for f in flowers
                ]
            return result

        raw_sculpt = row[7] if len(row) > 7 else None
        sculpture_positions = {}
        if raw_sculpt:
            for key, val in json.loads(raw_sculpt).items():
                xs, ys = key.split(",")
                pos = (int(xs), int(ys))
                if isinstance(val, dict) and "root" in val:
                    rbx, rby = val["root"].split(",")
                    sculpture_positions[pos] = {"root": (int(rbx), int(rby))}
                else:
                    sculpture_positions[pos] = val   # uid string

        def _parse_display_data(raw):
            if not raw:
                return {}
            from wildflowers import Wildflower
            result = {}
            for key, f in json.loads(raw).items():
                xs, ys = key.split(",")
                result[(int(xs), int(ys))] = Wildflower(
                    uid=f["uid"], flower_type=f["flower_type"], rarity=f["rarity"],
                    bloom_stage=f["bloom_stage"],
                    primary_color=tuple(f["primary_color"]),
                    secondary_color=tuple(f["secondary_color"]),
                    center_color=tuple(f["center_color"]),
                    petal_pattern=f["petal_pattern"], petal_count=f["petal_count"],
                    fragrance=f["fragrance"], vibrancy=f["vibrancy"],
                    specials=f["specials"], biodome_found=f["biodome_found"], seed=f["seed"],
                )
            return result

        def _parse_pottery_displays(raw):
            if not raw:
                return {}
            from pottery import PotteryPiece
            result = {}
            for key, p in json.loads(raw).items():
                xs, ys = key.split(",")
                p["texture_notes"] = p.get("texture_notes") or []
                p["profile"]       = p.get("profile") or []
                p["blend_components"] = p.get("blend_components") or []
                result[(int(xs), int(ys))] = PotteryPiece(**p)
            return result

        return {
            "water_level":            _parse_coord_dict(row[0]),
            "soil_moisture":          _parse_coord_dict(row[1]),
            "crop_progress":          _parse_coord_dict(row[2]),
            "crop_care_sum":          _parse_coord_dict(row[3], lambda v: (float(v[0]), int(v[1]))),
            "soil_fertility":         _parse_coord_dict(row[4]),
            "compost_bin_data":       _parse_bin_data(row[5]),
            "garden_data":            _parse_garden_data(row[6] if len(row) > 6 else None),
            "sculpture_positions":    sculpture_positions,
            "wildflower_display_data": _parse_display_data(row[8] if len(row) > 8 else None),
            "pottery_display_data":   _parse_pottery_displays(row[9] if len(row) > 9 else None),
            "unplaced_vase_uids":     json.loads(row[10]) if len(row) > 10 and row[10] else [],
        }

    def _load_player(self, con, bird_obs=None, insect_obs=None):
        row = con.execute("""
            SELECT x, y, vx, vy, facing, health, hunger, pick_power, money,
                   selected_slot, inventory, hotbar, hotbar_uses, known_recipes,
                   discovered_types, discovered_flower_types,
                   discovered_mushroom_types, mushrooms_found,
                   spawn_x, spawn_y, discovered_fossil_types, known_crops,
                   discovered_foods, foods_cooked,
                   horses_tamed, horses_bred, horse_records, discovered_coat_biomes,
                   COALESCE(discovered_recipes, '[]'),
                   COALESCE(worn, '{}'),
                   COALESCE(animals_hunted, '{}'),
                   COALESCE(roast_profiles, '[]')
            FROM player LIMIT 1
        """).fetchone()

        (x, y, vx, vy, facing, health, hunger, pick_power, money,
         selected_slot, inventory, hotbar, hotbar_uses, known_recipes,
         discovered_types, discovered_flower_types,
         discovered_mushroom_types, mushrooms_found,
         spawn_x, spawn_y, discovered_fossil_types, known_crops,
         discovered_foods, foods_cooked,
         horses_tamed, horses_bred, horse_records_raw, discovered_coat_biomes_raw,
         discovered_recipes_raw, worn_raw, animals_hunted_raw, roast_profiles_raw) = row

        rocks_rows = con.execute("""
            SELECT uid, base_type, rarity, size, primary_color, secondary_color,
                   pattern, pattern_density, hardness, luster, purity, specials,
                   depth_found, seed, upgrades
            FROM rocks
        """).fetchall()
        rocks_data = []
        for r in rocks_rows:
            rocks_data.append({
                "uid": r[0], "base_type": r[1], "rarity": r[2], "size": r[3],
                "primary_color": tuple(json.loads(r[4])),
                "secondary_color": tuple(json.loads(r[5])),
                "pattern": r[6], "pattern_density": r[7], "hardness": r[8],
                "luster": r[9], "purity": r[10],
                "specials": json.loads(r[11]),
                "depth_found": r[12], "seed": r[13],
                "upgrades": json.loads(r[14]),
            })

        wf_rows = con.execute("""
            SELECT uid, flower_type, rarity, bloom_stage, primary_color,
                   secondary_color, center_color, petal_pattern, petal_count,
                   fragrance, vibrancy, specials, biodome_found, seed
            FROM wildflowers
        """).fetchall()
        wf_data = []
        for wf in wf_rows:
            wf_data.append({
                "uid": wf[0], "flower_type": wf[1], "rarity": wf[2],
                "bloom_stage": wf[3],
                "primary_color": tuple(json.loads(wf[4])),
                "secondary_color": tuple(json.loads(wf[5])),
                "center_color": tuple(json.loads(wf[6])),
                "petal_pattern": wf[7], "petal_count": wf[8],
                "fragrance": wf[9], "vibrancy": wf[10],
                "specials": json.loads(wf[11]),
                "biodome_found": wf[12], "seed": wf[13],
            })

        fossil_cols = [row[1] for row in con.execute("PRAGMA table_info(fossils)").fetchall()]
        has_prepared_col = "prepared" in fossil_cols
        fossil_rows = con.execute("""
            SELECT uid, fossil_type, rarity, size, primary_color, secondary_color,
                   pattern, pattern_density, age, clarity, detail, specials,
                   depth_found, seed, upgrades
            FROM fossils
        """).fetchall()
        fossils_data = []
        for f in fossil_rows:
            fossils_data.append({
                "uid": f[0], "fossil_type": f[1], "rarity": f[2], "size": f[3],
                "primary_color": tuple(json.loads(f[4])),
                "secondary_color": tuple(json.loads(f[5])),
                "pattern": f[6], "pattern_density": f[7], "age": f[8],
                "clarity": f[9], "detail": f[10],
                "specials": json.loads(f[11]),
                "depth_found": f[12], "seed": f[13],
                "upgrades": json.loads(f[14]),
                "prepared": not has_prepared_col,  # grandfather old saves as prepared
            })
        if has_prepared_col:
            prepared_rows = con.execute("SELECT uid, prepared FROM fossils").fetchall()
            prepared_map = {row[0]: bool(row[1]) for row in prepared_rows}
            for fd in fossils_data:
                fd["prepared"] = prepared_map.get(fd["uid"], False)

        gem_rows = con.execute("""
            SELECT uid, gem_type, rarity, size, state, cut, clarity,
                   color_saturation, optical_effect, inclusion, crystal_system,
                   primary_color, secondary_color, depth_found, seed, biome, upgrades
            FROM gems
        """).fetchall()
        gems_data = []
        for g in gem_rows:
            gems_data.append({
                "uid": g[0], "gem_type": g[1], "rarity": g[2], "size": g[3],
                "state": g[4], "cut": g[5], "clarity": g[6],
                "color_saturation": g[7], "optical_effect": g[8],
                "inclusion": g[9], "crystal_system": g[10],
                "primary_color": tuple(json.loads(g[11])),
                "secondary_color": tuple(json.loads(g[12])),
                "depth_found": g[13], "seed": g[14],
                "biome": g[15] or "",
                "upgrades": json.loads(g[16]) if g[16] else [],
            })

        fish_rows = con.execute("""
            SELECT uid, species, rarity, weight_kg, length_cm, pattern,
                   primary_color, secondary_color, habitat, biome_found, seed
            FROM fish
        """).fetchall()
        fish_data = []
        for f in fish_rows:
            fish_data.append({
                "uid": f[0], "species": f[1], "rarity": f[2],
                "weight_kg": f[3], "length_cm": f[4], "pattern": f[5],
                "primary_color": tuple(json.loads(f[6])),
                "secondary_color": tuple(json.loads(f[7])),
                "habitat": f[8], "biome_found": f[9] or "", "seed": f[10],
            })

        try:
            con.execute("ALTER TABLE coffee_beans ADD COLUMN terroir_quality REAL DEFAULT 0.0")
        except Exception:
            pass
        coffee_rows = con.execute("""
            SELECT uid, origin_biome, variety, state, roast_level, roast_quality,
                   acidity, body, sweetness, earthiness, brightness,
                   flavor_notes, seed, blend_components,
                   COALESCE(processing_method, ''),
                   COALESCE(terroir_quality, 0.0)
            FROM coffee_beans
        """).fetchall()
        coffee_data = []
        for c in coffee_rows:
            coffee_data.append({
                "uid": c[0], "origin_biome": c[1], "variety": c[2], "state": c[3],
                "roast_level": c[4], "roast_quality": c[5],
                "acidity": c[6], "body": c[7], "sweetness": c[8],
                "earthiness": c[9], "brightness": c[10],
                "flavor_notes": json.loads(c[11]) if c[11] else [],
                "seed": c[12],
                "blend_components": json.loads(c[13]) if c[13] else [],
                "processing_method": c[14] or "",
                "terroir_quality": c[15] or 0.0,
            })

        try:
            wine_rows = con.execute("""
                SELECT uid, origin_biome, variety, state, style,
                       sweetness, acidity, tannin, body, aromatics,
                       alcohol, complexity, press_quality, ferment_quality,
                       flavor_notes, seed, blend_components,
                       COALESCE(crush_style, ''),
                       COALESCE(yeast, ''),
                       COALESCE(vessel, '')
                FROM wine_grapes
            """).fetchall()
        except Exception:
            wine_rows = []
        wine_data = []
        for w in wine_rows:
            wine_data.append({
                "uid": w[0], "origin_biome": w[1], "variety": w[2], "state": w[3],
                "style": w[4],
                "sweetness": w[5], "acidity": w[6], "tannin": w[7], "body": w[8], "aromatics": w[9],
                "alcohol": w[10], "complexity": w[11],
                "press_quality": w[12], "ferment_quality": w[13],
                "flavor_notes": json.loads(w[14]) if w[14] else [],
                "seed": w[15],
                "blend_components": json.loads(w[16]) if w[16] else [],
                "crush_style": w[17] or "",
                "yeast": w[18] or "",
                "vessel": w[19] or "",
            })

        try:
            tea_rows = con.execute("""
                SELECT uid, origin_biome, variety, state, tea_type,
                       oxidation, astringency, floral, vegetal,
                       earthiness, sweetness, steep_quality, complexity,
                       flavor_notes, seed, blend_components,
                       COALESCE(wither_method, ''),
                       COALESCE(herbal_additions, '[]'),
                       COALESCE(age_duration, '')
                FROM tea_leaves
            """).fetchall()
        except Exception:
            tea_rows = []
        tea_data = []
        for t in tea_rows:
            tea_data.append({
                "uid": t[0], "origin_biome": t[1], "variety": t[2], "state": t[3],
                "tea_type": t[4],
                "oxidation": t[5], "astringency": t[6], "floral": t[7], "vegetal": t[8],
                "earthiness": t[9], "sweetness": t[10], "steep_quality": t[11], "complexity": t[12],
                "flavor_notes": json.loads(t[13]) if t[13] else [],
                "seed": t[14],
                "blend_components": json.loads(t[15]) if t[15] else [],
                "wither_method": t[16] or "",
                "herbal_additions": json.loads(t[17]) if t[17] else [],
                "age_duration": t[18] or "",
            })

        try:
            spirit_rows = con.execute("""
                SELECT uid, origin_biome, grain_type, spirit_type, state,
                       cut_quality, proof, grain_character, sweetness, spice,
                       smokiness, smoothness, age_quality,
                       flavor_notes, seed, blend_components,
                       COALESCE(barrel_type, ''), COALESCE(age_duration, '')
                FROM spirits
            """).fetchall()
        except Exception:
            spirit_rows = []
        spirit_data = []
        for s in spirit_rows:
            spirit_data.append({
                "uid": s[0], "origin_biome": s[1], "grain_type": s[2],
                "spirit_type": s[3], "state": s[4],
                "cut_quality": s[5], "proof": s[6],
                "grain_character": s[7], "sweetness": s[8], "spice": s[9],
                "smokiness": s[10], "smoothness": s[11], "age_quality": s[12],
                "flavor_notes": json.loads(s[13]) if s[13] else [],
                "seed": s[14],
                "blend_components": json.loads(s[15]) if s[15] else [],
                "barrel_type": s[16] or "",
                "age_duration": s[17] or "",
            })

        try:
            textile_rows = con.execute(
                "SELECT uid, fiber_type, state, output_type, texture, dye_family, "
                "dye_color, quality, softness, luster, pattern_quality, seed FROM textiles"
            ).fetchall()
        except Exception:
            textile_rows = []
        textile_data = [
            {
                "uid": r[0], "fiber_type": r[1], "state": r[2], "output_type": r[3],
                "texture": r[4], "dye_family": r[5],
                "dye_color": json.loads(r[6]) if r[6] else [230, 215, 185],
                "quality": r[7], "softness": r[8], "luster": r[9],
                "pattern_quality": r[10], "seed": r[11],
            }
            for r in textile_rows
        ]

        try:
            cheese_rows = con.execute(
                "SELECT uid, origin_biome, animal_type, variety, state, "
                "richness, sharpness, nuttiness, saltiness, moisture, "
                "culture_quality, age_quality, flavor_notes, seed, blend_components, "
                "COALESCE(cheese_type, ''), COALESCE(press_quality, 0.0) "
                "FROM cheese_wheels"
            ).fetchall()
        except Exception:
            cheese_rows = []
        cheese_data = [
            {
                "uid": r[0], "origin_biome": r[1], "animal_type": r[2],
                "variety": r[3], "state": r[4],
                "richness": r[5], "sharpness": r[6], "nuttiness": r[7],
                "saltiness": r[8], "moisture": r[9],
                "culture_quality": r[10], "age_quality": r[11],
                "flavor_notes": json.loads(r[12]) if r[12] else [],
                "seed": r[13],
                "blend_components": json.loads(r[14]) if r[14] else [],
                "cheese_type": r[15] or "",
                "press_quality": r[16] or 0.0,
            }
            for r in cheese_rows
        ]

        try:
            jewelry_rows = con.execute("SELECT uid, jewelry_type, slot_count, slots, custom_name, seed FROM jewelry").fetchall()
        except Exception:
            jewelry_rows = []
        _jewelry_data = [
            {
                "uid": r[0], "jewelry_type": r[1], "slot_count": r[2],
                "slots": json.loads(r[3]) if r[3] else [],
                "custom_name": r[4] or "", "seed": r[5],
            }
            for r in jewelry_rows
        ]

        try:
            sc_rows = con.execute(
                "SELECT uid, mineral, height, grid, color, template, seed, pending FROM sculptures"
            ).fetchall()
        except Exception:
            sc_rows = []
        _sculpture_created = []
        _sculpture_pending = []
        for r in sc_rows:
            sc_dict = {
                "uid": r[0], "mineral": r[1], "height": r[2],
                "grid": json.loads(r[3]),
                "color": tuple(json.loads(r[4])),
                "template": r[5], "seed": r[6],
            }
            _sculpture_created.append(sc_dict)
            if r[7]:
                _sculpture_pending.append(sc_dict)

        try:
            pottery_rows = con.execute(
                "SELECT uid, clay_biome, shape, state, firing_level, firing_quality, "
                "thickness, evenness, glaze_type, texture_notes, seed, profile, blend_components "
                "FROM pottery_pieces"
            ).fetchall()
        except Exception:
            pottery_rows = []
        pottery_data = []
        for r in pottery_rows:
            pottery_data.append({
                "uid": r[0], "clay_biome": r[1], "shape": r[2], "state": r[3],
                "firing_level": r[4], "firing_quality": r[5],
                "thickness": r[6], "evenness": r[7],
                "glaze_type": r[8] or "",
                "texture_notes": json.loads(r[9] or "[]"),
                "seed": r[10],
                "profile": json.loads(r[11] or "[]"),
                "blend_components": json.loads(r[12] or "[]"),
            })

        return {
            "x": x, "y": y, "vx": vx, "vy": vy, "facing": facing,
            "health": health, "hunger": hunger, "pick_power": pick_power,
            "money": money, "selected_slot": selected_slot,
            "inventory": json.loads(inventory),
            "hotbar": json.loads(hotbar),
            "hotbar_uses": json.loads(hotbar_uses),
            "known_recipes": json.loads(known_recipes),
            "discovered_types": json.loads(discovered_types),
            "discovered_flower_types": json.loads(discovered_flower_types),
            "discovered_mushroom_types": json.loads(discovered_mushroom_types),
            "mushrooms_found": json.loads(mushrooms_found),
            "rocks": rocks_data,
            "wildflowers": wf_data,
            "fossils": fossils_data,
            "gems": gems_data,
            "discovered_fossil_types": json.loads(discovered_fossil_types or "[]"),
            "discovered_gem_types": list({g["gem_type"] for g in gems_data}),
            "birds_observed": bird_obs or {},
            "discovered_bird_types": list((bird_obs or {}).keys()),
            "insects_observed": insect_obs or {},
            "discovered_insect_types": list((insect_obs or {}).keys()),
            "fish": fish_data,
            "discovered_fish_species": list({f["species"] for f in fish_data}),
            "coffee_beans": coffee_data,
            "discovered_coffee_origins": list({
                f"{c['origin_biome']}_{c['roast_level']}"
                for c in coffee_data if c["state"] != "raw"
            }),
            "wine_grapes": wine_data,
            "tea_leaves": tea_data,
            "discovered_tea_origins": list({
                f"{t['origin_biome']}_{t['tea_type']}"
                for t in tea_data if t["tea_type"]
            }),
            "discovered_wine_origins": list({
                f"{w['origin_biome']}_{w['style']}"
                for w in wine_data if w["state"] not in ("raw", "crushed") and w["style"]
            }),
            "spirits": spirit_data,
            "discovered_spirit_types": list({
                f"{s['origin_biome']}_{('reserve' if s['age_quality'] >= 0.70 else 'aged' if s['age_quality'] >= 0.40 else 'young')}"
                for s in spirit_data if s["state"] in ("aged", "blended")
            }),
            "textiles": textile_data,
            "discovered_textiles": list({
                f"{t['fiber_type']}_{t['dye_family']}_{t['output_type']}"
                for t in textile_data if t["state"] == "woven"
            }),
            "cheese_wheels": cheese_data,
            "discovered_cheese": list({
                f"{c['origin_biome']}_{c['cheese_type']}"
                for c in cheese_data if c["state"] == "aged" and c["cheese_type"]
            }),
            "jewelry": _jewelry_data,
            "discovered_jewelry": list({j["jewelry_type"] for j in _jewelry_data}),
            "worn": json.loads(worn_raw or "{}") or {"head": None, "chest": None, "feet": None},
            "spawn_x": spawn_x,
            "spawn_y": spawn_y,
            "known_crops": json.loads(known_crops or "[]"),
            "discovered_foods": json.loads(discovered_foods or "[]"),
            "foods_cooked": json.loads(foods_cooked or "{}"),
            "horses_tamed": int(horses_tamed or 0),
            "horses_bred": int(horses_bred or 0),
            "horse_records": json.loads(horse_records_raw or "{}"),
            "discovered_coat_biomes": json.loads(discovered_coat_biomes_raw or "[]"),
            "discovered_recipes": json.loads(discovered_recipes_raw or "[]"),
            "animals_hunted":     json.loads(animals_hunted_raw or "{}"),
            "roast_profiles":     json.loads(roast_profiles_raw or "[]"),
            "sculptures_created": _sculpture_created,
            "pending_sculptures": _sculpture_pending,
            "pottery_pieces": pottery_data,
            "discovered_pottery": list({
                f"{p['clay_biome']}_{p['firing_level']}"
                for p in pottery_data if p["state"] == "fired" and p["firing_level"] != "cracked"
            }),
        }

    def _load_automations(self, con):
        rows = con.execute("""
            SELECT x, y, auto_type, direction, fuel, supports, stored,
                   state, halt_reason, blocks_since_support
            FROM automations
        """).fetchall()
        result = []
        for row in rows:
            (x, y, auto_type, raw_dir, fuel, supports, stored,
             state, halt_reason, blocks_since_support) = row
            if isinstance(raw_dir, int):
                direction = (raw_dir, 0)
            else:
                direction = tuple(json.loads(raw_dir))
            result.append({
                "x": x, "y": y, "auto_type": auto_type, "direction": direction,
                "fuel": fuel,
                "stored": json.loads(stored),
                "state": state, "halt_reason": halt_reason,
            })
        return result

    def _load_farm_bots(self, con):
        try:
            rows = con.execute(
                "SELECT x, y, bot_type, fuel, seeds, stored, state, "
                "water_reservoir, compost_slot FROM farm_bots"
            ).fetchall()
        except Exception:
            return []
        result = []
        for x, y, bot_type, fuel, seeds, stored, state, water_res, compost in rows:
            result.append({
                "x": x, "y": y, "bot_type": bot_type, "fuel": fuel,
                "seeds": json.loads(seeds), "stored": json.loads(stored),
                "state": state,
                "water_reservoir": float(water_res or 0),
                "compost_slot":    int(compost or 0),
            })
        return result

    def _load_backhoes(self, con):
        try:
            rows = con.execute(
                "SELECT x, y, fuel, stored, arm_dx, arm_dy FROM backhoes"
            ).fetchall()
        except Exception:
            return []
        result = []
        for x, y, fuel, stored, arm_dx, arm_dy in rows:
            result.append({
                "x": x, "y": y, "fuel": fuel,
                "stored": json.loads(stored) if stored else {},
                "arm_dx": arm_dx if arm_dx is not None else 2,
                "arm_dy": arm_dy if arm_dy is not None else 0,
            })
        return result

    def _load_entities(self, con):
        rows = con.execute(
            "SELECT entity_type, x, y, facing, animal_id, extra FROM entities"
        ).fetchall()
        result = []
        for row in rows:
            entity_type, x, y, facing, animal_id, extra = row
            result.append({
                "entity_type": entity_type,
                "x": x, "y": y, "facing": facing, "animal_id": animal_id,
                "extra": json.loads(extra) if extra else {},
            })
        return result

    def _load_research(self, con):
        rows = con.execute("SELECT node_id, unlocked FROM research").fetchall()
        return [node_id for node_id, unlocked in rows if unlocked]

    def _load_chests(self, con):
        try:
            rows = con.execute("SELECT x, y, contents FROM chests").fetchall()
        except Exception:
            return {}
        return {f"{x},{y}": json.loads(contents) for x, y, contents in rows}

    def _load_dropped_items(self, con):
        try:
            rows = con.execute(
                "SELECT x, y, item_id, count, lifetime FROM dropped_items"
            ).fetchall()
        except Exception:
            return []
        return [{"x": x, "y": y, "item_id": iid, "count": cnt, "lifetime": lt}
                for x, y, iid, cnt, lt in rows]
