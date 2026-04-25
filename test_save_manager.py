"""
Round-trip tests for SaveManager.

Each test saves a world/player/research snapshot and then loads it back,
asserting that every field survives the round-trip.  No game modules are
imported — everything is stubbed with SimpleNamespace / plain dicts.
"""

import json
import tempfile
import types
import unittest
from pathlib import Path
from types import SimpleNamespace

from save_manager import SaveManager


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ns(**kw):
    return SimpleNamespace(**kw)


def _make_rock():
    return _ns(
        uid="r1", base_type="granite", rarity="common", size="medium",
        primary_color=(100, 100, 100), secondary_color=(80, 80, 80),
        pattern="speckled", pattern_density=0.5, hardness=7.0,
        luster=0.3, purity=0.9, specials=["shiny"],
        depth_found=5, seed=42, upgrades={"polish": 1},
    )


def _make_wildflower():
    return _ns(
        uid="wf1", flower_type="daisy", rarity="common", bloom_stage="full",
        primary_color=(255, 255, 0), secondary_color=(255, 255, 255),
        center_color=(200, 150, 0),
        petal_pattern="radial", petal_count=8, fragrance=0.7,
        vibrancy=0.9, specials=[], biodome_found="meadow", seed=1,
    )


def _make_fossil():
    return _ns(
        uid="f1", fossil_type="ammonite", rarity="rare", size="large",
        primary_color=(180, 160, 120), secondary_color=(140, 120, 90),
        pattern="spiral", pattern_density=0.8, age="jurassic",
        clarity=0.6, detail=0.75, specials=["complete"],
        depth_found=20, seed=7, upgrades={}, prepared=True,
    )


def _make_gem():
    return _ns(
        uid="g1", gem_type="emerald", rarity="epic", size="small",
        state="cut", cut="brilliant", clarity="vvs",
        color_saturation=0.9, optical_effect="none", inclusion="none",
        crystal_system="hexagonal",
        primary_color=(0, 200, 80), secondary_color=(0, 160, 60),
        depth_found=40, seed=99, biome="jungle", upgrades=[],
    )


def _make_fish():
    return _ns(
        uid="fish1", species="salmon", rarity="common",
        weight_kg=2.5, length_cm=45, pattern="striped",
        primary_color=(220, 80, 60), secondary_color=(180, 60, 40),
        habitat="river", biome_found="forest", seed=3,
    )


def _make_coffee_bean():
    return _ns(
        uid="cb1", origin_biome="tropical", variety="arabica",
        state="roasted", roast_level="medium", roast_quality=0.85,
        acidity=0.6, body=0.7, sweetness=0.5, earthiness=0.3, brightness=0.8,
        flavor_notes=["chocolate", "cherry"], seed=11,
        blend_components=[], processing_method="washed", terroir_quality=0.9,
    )


def _make_wine_grape():
    return _ns(
        uid="wg1", origin_biome="mediterranean", variety="cabernet",
        state="bottled", style="red",
        sweetness=0.2, acidity=0.7, tannin=0.6, body=0.8,
        aromatics=0.75, alcohol=13.5, complexity=0.9,
        press_quality=0.8, ferment_quality=0.85,
        flavor_notes=["blackcurrant"], seed=22,
        blend_components=[], crush_style="whole_cluster",
        yeast="wild", vessel="oak",
    )


def _make_spirit():
    return _ns(
        uid="sp1", origin_biome="highland", grain_type="barley",
        spirit_type="whisky", state="aged",
        cut_quality=0.8, proof=46.0,
        grain_character=0.7, sweetness=0.4, spice=0.5,
        smokiness=0.3, smoothness=0.75, age_quality=0.9,
        flavor_notes=["vanilla", "smoke"], seed=33,
        blend_components=[], barrel_type="ex-bourbon", age_duration="5y",
    )


def _make_tea_leaf():
    return _ns(
        uid="tl1", origin_biome="highland", variety="oolong",
        state="finished", tea_type="oolong",
        oxidation=0.5, astringency=0.4, floral=0.8, vegetal=0.2,
        earthiness=0.3, sweetness=0.6, steep_quality=0.85, complexity=0.9,
        flavor_notes=["orchid"], seed=44,
        blend_components=[], wither_method="solar",
        herbal_additions=["mint"], age_duration="",
    )


def _make_textile():
    return _ns(
        uid="tx1", fiber_type="wool", state="dyed", output_type="cloth",
        texture="twill", dye_family="natural", dye_color=[120, 80, 40],
        quality=0.8, softness=0.7, luster=0.5, pattern_quality=0.6, seed=55,
    )


def _make_cheese():
    return _ns(
        uid="ch1", origin_biome="alpine", animal_type="cow",
        variety="gruyere", state="aged",
        richness=0.8, sharpness=0.7, nuttiness=0.6,
        saltiness=0.4, moisture=0.3,
        culture_quality=0.9, age_quality=0.85,
        flavor_notes=["nutty"], seed=66,
        blend_components=[], cheese_type="hard", press_quality=0.75,
    )


def _make_jewelry():
    return _ns(
        uid="jw1", jewelry_type="ring", slot_count=2,
        slots=[{"gem": "emerald"}, {"gem": "ruby"}],
        custom_name="Band of Power", seed=77,
    )


def _make_sculpture():
    return _ns(
        uid="sc1", mineral="marble", height=3,
        grid=[[0, 1], [1, 0]], color=(230, 220, 210),
        template="bust", seed=88,
    )


def _make_pottery():
    return _ns(
        uid="pt1", clay_biome="riverbed", shape="vase",
        state="fired", firing_level="high", firing_quality=0.9,
        thickness=0.5, evenness=0.8, glaze_type="celadon",
        texture_notes=["smooth"], seed=99,
        profile=["wide_body"], blend_components=[],
    )


def _make_player():
    sc = _make_sculpture()
    return _ns(
        x=10.0, y=20.0, vx=0.0, vy=0.0, facing=1,
        health=100, hunger=80.0, pick_power=3, money=500,
        selected_slot=0,
        inventory=[{"id": "stone", "count": 5}],
        hotbar=[None] * 9,
        hotbar_uses=[0] * 9,
        known_recipes=["wood_plank"],
        discovered_types={1, 2},
        discovered_flower_types={"daisy"},
        discovered_mushroom_types={3},
        mushrooms_found={3: 2},
        spawn_x=0.0, spawn_y=50.0,
        discovered_fossil_types={"ammonite"},
        known_crops=["wheat"],
        discovered_foods=["bread"],
        foods_cooked={"bread": 3},
        horses_tamed=2, horses_bred=1,
        horse_records={"h1": {"name": "Buck"}},
        discovered_coat_biomes={"plains"},
        discovered_recipes={"saddle"},
        animals_hunted={"deer": 4},
        roast_profiles=[{"profile": "medium"}],
        rocks=[_make_rock()],
        wildflowers=[_make_wildflower()],
        fossils=[_make_fossil()],
        gems=[_make_gem()],
        fish_caught=[_make_fish()],
        coffee_beans=[_make_coffee_bean()],
        wine_grapes=[_make_wine_grape()],
        spirits=[_make_spirit()],
        tea_leaves=[_make_tea_leaf()],
        textiles=[_make_textile()],
        worn={"head": None, "body": None},
        cheese_wheels=[_make_cheese()],
        jewelry=[_make_jewelry()],
        sculptures_created=[sc],
        pending_sculptures=[],
        pottery_pieces=[_make_pottery()],
        birds_observed={"robin": {"count": 3, "biome": "forest"}},
        insects_observed={"monarch": {"count": 1, "biome": "meadow"}},
        # global_collection merge
        discovered_gem_types={"emerald"},
        discovered_fish_species={"salmon"},
        discovered_coffee_origins={"tropical"},
        discovered_wine_origins={"mediterranean"},
        discovered_spirit_types={"whisky"},
    )


def _make_world():
    return _ns(
        seed=12345,
        _dirty_chunks=set(),
        _chunks={},
        _dirty_bg_chunks=set(),
        _bg_chunks={},
        _water_level={(0, 5): 3},
        _soil_moisture={(1, 6): 0.5},
        _crop_progress={(2, 7): 0.8},
        _crop_care_sum={(2, 7): (1.0, 2)},
        _soil_fertility={(3, 8): 0.6},
        compost_bin_data={(4, 9): {"slots": []}},
        garden_data={},
        sculpture_data={},
        automations=[],
        farm_bots=[],
        backhoes=[],
        elevator_cars=[],
        entities=[],
        dropped_items=[],
        chest_data={},
    )


def _make_research():
    return _ns(nodes={
        "mining_1": _ns(unlocked=True),
        "farming_1": _ns(unlocked=False),
    })


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestSaveManagerRoundTrip(unittest.TestCase):

    def setUp(self):
        self._tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self._tmp.close()
        self.sm = SaveManager(self._tmp.name)

    def tearDown(self):
        Path(self._tmp.name).unlink(missing_ok=True)

    def _save_and_load(self):
        world = _make_world()
        player = _make_player()
        research = _make_research()
        self.sm.save(world, player, research)
        return self.sm.load()

    # --- meta ---------------------------------------------------------------

    def test_seed_survives(self):
        data = self._save_and_load()
        self.assertEqual(data["seed"], 12345)

    # --- world_meta ---------------------------------------------------------

    def test_water_level(self):
        data = self._save_and_load()
        self.assertEqual(data["water_level"]["0,5"], 3)

    def test_soil_moisture(self):
        data = self._save_and_load()
        self.assertAlmostEqual(data["soil_moisture"]["1,6"], 0.5)

    def test_crop_progress(self):
        data = self._save_and_load()
        self.assertAlmostEqual(data["crop_progress"]["2,7"], 0.8)

    def test_crop_care_sum(self):
        data = self._save_and_load()
        self.assertEqual(data["crop_care_sum"]["2,7"], [1.0, 2])

    def test_soil_fertility(self):
        data = self._save_and_load()
        self.assertAlmostEqual(data["soil_fertility"]["3,8"], 0.6)

    def test_compost_bin_data(self):
        data = self._save_and_load()
        self.assertIn("4,9", data["compost_bin_data"])

    # --- player core --------------------------------------------------------

    def test_player_position(self):
        data = self._save_and_load()
        p = data["player"]
        self.assertAlmostEqual(p["x"], 10.0)
        self.assertAlmostEqual(p["y"], 20.0)

    def test_player_stats(self):
        data = self._save_and_load()
        p = data["player"]
        self.assertEqual(p["health"], 100)
        self.assertAlmostEqual(p["hunger"], 80.0)
        self.assertEqual(p["money"], 500)
        self.assertEqual(p["pick_power"], 3)

    def test_player_inventory(self):
        data = self._save_and_load()
        inv = data["player"]["inventory"]
        self.assertEqual(inv[0]["id"], "stone")
        self.assertEqual(inv[0]["count"], 5)

    def test_known_recipes(self):
        data = self._save_and_load()
        self.assertIn("wood_plank", data["player"]["known_recipes"])

    def test_discovered_types(self):
        data = self._save_and_load()
        self.assertIn(1, data["player"]["discovered_types"])

    def test_spawn_point(self):
        data = self._save_and_load()
        p = data["player"]
        self.assertAlmostEqual(p["spawn_x"], 0.0)
        self.assertAlmostEqual(p["spawn_y"], 50.0)

    def test_horses(self):
        data = self._save_and_load()
        p = data["player"]
        self.assertEqual(p["horses_tamed"], 2)
        self.assertEqual(p["horses_bred"], 1)
        self.assertIn("h1", p["horse_records"])

    def test_animals_hunted(self):
        data = self._save_and_load()
        self.assertEqual(data["player"]["animals_hunted"]["deer"], 4)

    def test_foods_cooked(self):
        data = self._save_and_load()
        self.assertEqual(data["player"]["foods_cooked"]["bread"], 3)

    # --- collections --------------------------------------------------------

    def test_rocks(self):
        data = self._save_and_load()
        rocks = data["player"]["rocks"]
        self.assertEqual(len(rocks), 1)
        r = rocks[0]
        self.assertEqual(r["uid"], "r1")
        self.assertEqual(r["base_type"], "granite")
        self.assertEqual(r["specials"], ["shiny"])
        self.assertEqual(r["upgrades"], {"polish": 1})

    def test_wildflowers(self):
        data = self._save_and_load()
        wf = data["player"]["wildflowers"][0]
        self.assertEqual(wf["uid"], "wf1")
        self.assertEqual(wf["flower_type"], "daisy")

    def test_fossils(self):
        data = self._save_and_load()
        f = data["player"]["fossils"][0]
        self.assertEqual(f["uid"], "f1")
        self.assertTrue(f["prepared"])

    def test_gems(self):
        data = self._save_and_load()
        g = data["player"]["gems"][0]
        self.assertEqual(g["uid"], "g1")
        self.assertEqual(g["gem_type"], "emerald")

    def test_fish(self):
        data = self._save_and_load()
        f = data["player"]["fish_caught"][0]
        self.assertEqual(f["uid"], "fish1")
        self.assertAlmostEqual(f["weight_kg"], 2.5)

    def test_coffee_beans(self):
        data = self._save_and_load()
        b = data["player"]["coffee_beans"][0]
        self.assertEqual(b["uid"], "cb1")
        self.assertEqual(b["processing_method"], "washed")
        self.assertAlmostEqual(b["terroir_quality"], 0.9)

    def test_wine_grapes(self):
        data = self._save_and_load()
        w = data["player"]["wine_grapes"][0]
        self.assertEqual(w["uid"], "wg1")
        self.assertEqual(w["crush_style"], "whole_cluster")
        self.assertEqual(w["yeast"], "wild")
        self.assertEqual(w["vessel"], "oak")

    def test_spirits(self):
        data = self._save_and_load()
        s = data["player"]["spirits"][0]
        self.assertEqual(s["uid"], "sp1")
        self.assertEqual(s["barrel_type"], "ex-bourbon")
        self.assertEqual(s["age_duration"], "5y")

    def test_tea_leaves(self):
        data = self._save_and_load()
        t = data["player"]["tea_leaves"][0]
        self.assertEqual(t["uid"], "tl1")
        self.assertEqual(t["wither_method"], "solar")
        self.assertEqual(t["herbal_additions"], ["mint"])

    def test_textiles(self):
        data = self._save_and_load()
        tx = data["player"]["textiles"][0]
        self.assertEqual(tx["uid"], "tx1")
        self.assertEqual(tx["fiber_type"], "wool")
        self.assertEqual(tx["dye_color"], [120, 80, 40])

    def test_cheese_wheels(self):
        data = self._save_and_load()
        c = data["player"]["cheese_wheels"][0]
        self.assertEqual(c["uid"], "ch1")
        self.assertEqual(c["cheese_type"], "hard")
        self.assertAlmostEqual(c["press_quality"], 0.75)

    def test_jewelry(self):
        data = self._save_and_load()
        j = data["player"]["jewelry"][0]
        self.assertEqual(j["uid"], "jw1")
        self.assertEqual(j["custom_name"], "Band of Power")
        self.assertEqual(len(j["slots"]), 2)

    def test_sculptures(self):
        data = self._save_and_load()
        sc = data["player"]["sculptures_created"][0]
        self.assertEqual(sc["uid"], "sc1")
        self.assertEqual(sc["mineral"], "marble")
        self.assertFalse(sc in data["player"]["pending_sculptures"])

    def test_pottery(self):
        data = self._save_and_load()
        pt = data["player"]["pottery_pieces"][0]
        self.assertEqual(pt["uid"], "pt1")
        self.assertEqual(pt["glaze_type"], "celadon")

    def test_bird_observations(self):
        data = self._save_and_load()
        birds = data["player"]["birds_observed"]
        self.assertEqual(birds["robin"]["count"], 3)
        self.assertEqual(birds["robin"]["biome"], "forest")

    def test_insect_observations(self):
        data = self._save_and_load()
        insects = data["player"]["insects_observed"]
        self.assertEqual(insects["monarch"]["count"], 1)

    # --- research -----------------------------------------------------------

    def test_research(self):
        data = self._save_and_load()
        r = data["research"]
        self.assertTrue(r["mining_1"])
        self.assertFalse(r["farming_1"])

    # --- migration: old save missing sculpture_positions -------------------

    def test_migration_missing_sculpture_positions(self):
        """Simulate a save file that predates the sculpture_positions column."""
        import sqlite3
        db = Path(self._tmp.name)
        with sqlite3.connect(db) as con:
            con.execute("""CREATE TABLE IF NOT EXISTS save_meta
                           (seed INTEGER, save_version INTEGER, last_saved TEXT)""")
            con.execute("""CREATE TABLE IF NOT EXISTS world_meta
                           (water_level TEXT, soil_moisture TEXT,
                            crop_progress TEXT, crop_care_sum TEXT,
                            soil_fertility TEXT, compost_bin_data TEXT,
                            garden_data TEXT)""")  # no sculpture_positions
            con.execute("INSERT INTO save_meta VALUES (999, 2, '2025-01-01')")
            con.execute("INSERT INTO world_meta VALUES ('{}','{}','{}','{}','{}','{}','{}')")
            con.commit()
        # Save should add the missing column and not crash
        world = _make_world()
        player = _make_player()
        research = _make_research()
        self.sm.save(world, player, research)
        data = self.sm.load()
        self.assertEqual(data["seed"], 12345)

    def test_migration_missing_wine_columns(self):
        """Simulate wine_grapes table missing crush_style/yeast/vessel."""
        import sqlite3
        db = Path(self._tmp.name)
        with sqlite3.connect(db) as con:
            con.execute("""CREATE TABLE IF NOT EXISTS save_meta
                           (seed INTEGER, save_version INTEGER, last_saved TEXT)""")
            con.execute("""CREATE TABLE IF NOT EXISTS world_meta
                           (water_level TEXT, soil_moisture TEXT,
                            crop_progress TEXT, crop_care_sum TEXT,
                            soil_fertility TEXT, compost_bin_data TEXT,
                            garden_data TEXT, sculpture_positions TEXT)""")
            con.execute("""CREATE TABLE IF NOT EXISTS wine_grapes
                           (uid TEXT PRIMARY KEY, origin_biome TEXT, variety TEXT,
                            state TEXT, style TEXT, sweetness REAL, acidity REAL,
                            tannin REAL, body REAL, aromatics REAL, alcohol REAL,
                            complexity REAL, press_quality REAL, ferment_quality REAL,
                            flavor_notes TEXT, seed INTEGER, blend_components TEXT)""")
            con.execute("INSERT INTO save_meta VALUES (999, 2, '2025-01-01')")
            con.execute("INSERT INTO world_meta VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')")
            con.commit()
        world = _make_world()
        player = _make_player()
        research = _make_research()
        self.sm.save(world, player, research)
        data = self.sm.load()
        wg = data["player"]["wine_grapes"][0]
        self.assertEqual(wg["crush_style"], "whole_cluster")
        self.assertEqual(wg["vessel"], "oak")

    def test_migration_missing_spirit_columns(self):
        """Simulate spirits table missing barrel_type/age_duration."""
        import sqlite3
        db = Path(self._tmp.name)
        with sqlite3.connect(db) as con:
            con.execute("""CREATE TABLE IF NOT EXISTS save_meta
                           (seed INTEGER, save_version INTEGER, last_saved TEXT)""")
            con.execute("""CREATE TABLE IF NOT EXISTS world_meta
                           (water_level TEXT, soil_moisture TEXT,
                            crop_progress TEXT, crop_care_sum TEXT,
                            soil_fertility TEXT, compost_bin_data TEXT,
                            garden_data TEXT, sculpture_positions TEXT)""")
            con.execute("""CREATE TABLE IF NOT EXISTS spirits
                           (uid TEXT PRIMARY KEY, origin_biome TEXT, grain_type TEXT,
                            spirit_type TEXT, state TEXT, cut_quality REAL, proof REAL,
                            grain_character REAL, sweetness REAL, spice REAL,
                            smokiness REAL, smoothness REAL, age_quality REAL,
                            flavor_notes TEXT, seed INTEGER, blend_components TEXT)""")
            con.execute("INSERT INTO save_meta VALUES (999, 2, '2025-01-01')")
            con.execute("INSERT INTO world_meta VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')")
            con.commit()
        world = _make_world()
        player = _make_player()
        research = _make_research()
        self.sm.save(world, player, research)
        s = self.sm.load()["player"]["spirits"][0]
        self.assertEqual(s["barrel_type"], "ex-bourbon")

    def test_migration_missing_tea_columns(self):
        """Simulate tea_leaves table missing wither_method/herbal_additions/age_duration."""
        import sqlite3
        db = Path(self._tmp.name)
        with sqlite3.connect(db) as con:
            con.execute("""CREATE TABLE IF NOT EXISTS save_meta
                           (seed INTEGER, save_version INTEGER, last_saved TEXT)""")
            con.execute("""CREATE TABLE IF NOT EXISTS world_meta
                           (water_level TEXT, soil_moisture TEXT,
                            crop_progress TEXT, crop_care_sum TEXT,
                            soil_fertility TEXT, compost_bin_data TEXT,
                            garden_data TEXT, sculpture_positions TEXT)""")
            con.execute("""CREATE TABLE IF NOT EXISTS tea_leaves
                           (uid TEXT PRIMARY KEY, origin_biome TEXT, variety TEXT,
                            state TEXT, tea_type TEXT, oxidation REAL, astringency REAL,
                            floral REAL, vegetal REAL, earthiness REAL, sweetness REAL,
                            steep_quality REAL, complexity REAL, flavor_notes TEXT,
                            seed INTEGER, blend_components TEXT)""")
            con.execute("INSERT INTO save_meta VALUES (999, 2, '2025-01-01')")
            con.execute("INSERT INTO world_meta VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')")
            con.commit()
        world = _make_world()
        player = _make_player()
        research = _make_research()
        self.sm.save(world, player, research)
        t = self.sm.load()["player"]["tea_leaves"][0]
        self.assertEqual(t["wither_method"], "solar")
        self.assertEqual(t["herbal_additions"], ["mint"])

    def test_migration_missing_cheese_columns(self):
        """Simulate cheese_wheels table missing cheese_type/press_quality."""
        import sqlite3
        db = Path(self._tmp.name)
        with sqlite3.connect(db) as con:
            con.execute("""CREATE TABLE IF NOT EXISTS save_meta
                           (seed INTEGER, save_version INTEGER, last_saved TEXT)""")
            con.execute("""CREATE TABLE IF NOT EXISTS world_meta
                           (water_level TEXT, soil_moisture TEXT,
                            crop_progress TEXT, crop_care_sum TEXT,
                            soil_fertility TEXT, compost_bin_data TEXT,
                            garden_data TEXT, sculpture_positions TEXT)""")
            con.execute("""CREATE TABLE IF NOT EXISTS cheese_wheels
                           (uid TEXT PRIMARY KEY, origin_biome TEXT, animal_type TEXT,
                            variety TEXT, state TEXT, richness REAL, sharpness REAL,
                            nuttiness REAL, saltiness REAL, moisture REAL,
                            culture_quality REAL, age_quality REAL,
                            flavor_notes TEXT, seed INTEGER, blend_components TEXT)""")
            con.execute("INSERT INTO save_meta VALUES (999, 2, '2025-01-01')")
            con.execute("INSERT INTO world_meta VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')")
            con.commit()
        world = _make_world()
        player = _make_player()
        research = _make_research()
        self.sm.save(world, player, research)
        c = self.sm.load()["player"]["cheese_wheels"][0]
        self.assertEqual(c["cheese_type"], "hard")
        self.assertAlmostEqual(c["press_quality"], 0.75)


if __name__ == "__main__":
    unittest.main()
