import sqlite3
import zlib
import struct
import json
from datetime import datetime
from pathlib import Path

from constants import CHUNK_W, WORLD_H

DB_PATH = Path(__file__).parent / "collectorblocks.db"
SAVE_VERSION = 2


class SaveManager:
    def __init__(self, db_path=None):
        self.db_path = Path(db_path) if db_path else DB_PATH

    def new_game(self):
        """Wipe all saved state so a new World generates fresh terrain."""
        try:
            with sqlite3.connect(self.db_path) as con:
                self._create_tables(con)
                for tbl in ("save_meta", "chunks", "world_meta", "player",
                            "rocks", "wildflowers", "research", "automations",
                            "entities", "dropped_items", "chests"):
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
        with sqlite3.connect(self.db_path) as con:
            self._create_tables(con)
            self._save_meta(con, world.seed)
            self._save_dirty_chunks(con, world)
            self._save_world_meta(con, world)
            self._save_player(con, player)
            self._save_rocks(con, player)
            self._save_wildflowers(con, player)
            self._save_research(con, research)
            self._save_automations(con, world)
            self._save_entities(con, world)
            self._save_dropped_items(con, world)
            self._save_chests(con, world)
            con.commit()

    def load(self):
        with sqlite3.connect(self.db_path) as con:
            self._create_tables(con)
            self._maybe_migrate(con)
            seed = con.execute("SELECT seed FROM save_meta LIMIT 1").fetchone()[0]
            water_level = self._load_world_meta(con)
            player_data = self._load_player(con)
            automations = self._load_automations(con)
            entities = self._load_entities(con)
            research = self._load_research(con)
            dropped_items = self._load_dropped_items(con)
            chest_data = self._load_chests(con)
        return {
            "seed": seed,
            "water_level": water_level,
            "player": player_data,
            "automations": automations,
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
        CREATE TABLE IF NOT EXISTS world_meta (
            water_level TEXT
        );
        CREATE TABLE IF NOT EXISTS player (
            x REAL, y REAL, vx REAL, vy REAL, facing INTEGER,
            health INTEGER, hunger REAL, pick_power INTEGER, money INTEGER,
            selected_slot INTEGER,
            inventory TEXT, hotbar TEXT, hotbar_uses TEXT, known_recipes TEXT,
            discovered_types TEXT, discovered_flower_types TEXT,
            discovered_mushroom_types TEXT, mushrooms_found TEXT
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
        CREATE TABLE IF NOT EXISTS research (
            node_id TEXT PRIMARY KEY, unlocked INTEGER
        );
        CREATE TABLE IF NOT EXISTS automations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            x REAL, y REAL, auto_type TEXT, direction INTEGER,
            fuel REAL, supports INTEGER,
            stored TEXT, state TEXT, halt_reason TEXT,
            blocks_since_support INTEGER
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
        """)
        for col, default in [("spawn_x", "NULL"), ("spawn_y", "NULL")]:
            try:
                con.execute(f"ALTER TABLE player ADD COLUMN {col} REAL DEFAULT {default}")
            except Exception:
                pass

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

    def _save_world_meta(self, con, world):
        water = {f"{x},{y}": lvl for (x, y), lvl in world._water_level.items()}
        con.execute("DELETE FROM world_meta")
        con.execute("INSERT INTO world_meta (water_level) VALUES (?)",
                    (json.dumps(water),))

    def _save_player(self, con, player):
        con.execute("DELETE FROM player")
        mushrooms = {str(k): v for k, v in player.mushrooms_found.items()}
        con.execute(
            """INSERT INTO player
               (x, y, vx, vy, facing, health, hunger, pick_power, money,
                selected_slot, inventory, hotbar, hotbar_uses, known_recipes,
                discovered_types, discovered_flower_types,
                discovered_mushroom_types, mushrooms_found,
                spawn_x, spawn_y)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
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
                    a.x, a.y, a.auto_type, a.direction,
                    a.fuel, a.supports,
                    json.dumps(a.stored),
                    a._state, a._halt_reason,
                    a._blocks_since_support,
                )
            )

    def _save_entities(self, con, world):
        from animals import Sheep, Cow, Chicken
        from cities import NPC
        con.execute("DELETE FROM entities")
        for e in world.entities:
            if isinstance(e, NPC):
                continue
            extra = {}
            if isinstance(e, Sheep):
                extra = {"has_wool": e.has_wool}
            elif isinstance(e, Cow):
                extra = {"has_milk": e.has_milk}
            elif isinstance(e, Chicken):
                extra = {"has_egg": e.has_egg}
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
        row = con.execute("SELECT water_level FROM world_meta LIMIT 1").fetchone()
        if row is None or row[0] is None:
            return {}
        water_raw = json.loads(row[0])
        water = {}
        for key, lvl in water_raw.items():
            xs, ys = key.split(",")
            water[(int(xs), int(ys))] = lvl
        return water

    def _load_player(self, con):
        row = con.execute("""
            SELECT x, y, vx, vy, facing, health, hunger, pick_power, money,
                   selected_slot, inventory, hotbar, hotbar_uses, known_recipes,
                   discovered_types, discovered_flower_types,
                   discovered_mushroom_types, mushrooms_found,
                   spawn_x, spawn_y
            FROM player LIMIT 1
        """).fetchone()

        (x, y, vx, vy, facing, health, hunger, pick_power, money,
         selected_slot, inventory, hotbar, hotbar_uses, known_recipes,
         discovered_types, discovered_flower_types,
         discovered_mushroom_types, mushrooms_found,
         spawn_x, spawn_y) = row

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
            "spawn_x": spawn_x,
            "spawn_y": spawn_y,
        }

    def _load_automations(self, con):
        rows = con.execute("""
            SELECT x, y, auto_type, direction, fuel, supports, stored,
                   state, halt_reason, blocks_since_support
            FROM automations
        """).fetchall()
        result = []
        for row in rows:
            (x, y, auto_type, direction, fuel, supports, stored,
             state, halt_reason, blocks_since_support) = row
            result.append({
                "x": x, "y": y, "auto_type": auto_type, "direction": direction,
                "fuel": fuel, "supports": supports,
                "stored": json.loads(stored),
                "state": state, "halt_reason": halt_reason,
                "blocks_since_support": blocks_since_support,
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
