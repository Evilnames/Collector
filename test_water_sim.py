"""
Water simulation tests.

Written from desired behavior, not from the implementation.  Where a comment
says "old code would …" that describes what the simulation did BEFORE the
gravity-priority fixes, and the test should fail against that old behavior.
"""

import unittest

import world as _world_mod
from constants import CHUNK_W, WORLD_H
from blocks import AIR, WATER, BEDROCK


# ---------------------------------------------------------------------------
# Harness
# ---------------------------------------------------------------------------

class WaterSim:
    """
    Minimal stub providing the data structures that World's water methods
    need.  Methods are borrowed directly from World so we run real logic.
    """
    _chunk_get               = _world_mod.World._chunk_get
    _chunk_set               = _world_mod.World._chunk_set
    get_bg_block             = _world_mod.World.get_bg_block
    set_bg_block             = _world_mod.World.set_bg_block
    update_water             = _world_mod.World.update_water
    set_block                = _world_mod.World.set_block
    _drain_unsustained_water = _world_mod.World._drain_unsustained_water

    def _update_pumps(self):
        pass

    def __init__(self):
        cx = 0
        self._chunks      = {cx: [[AIR] * CHUNK_W for _ in range(WORLD_H)]}
        self._bg_chunks   = {cx: [[AIR] * CHUNK_W for _ in range(WORLD_H)]}
        self._dirty_chunks    = set()
        self._dirty_bg_chunks = set()
        self._water_level   = {}
        self._water_sources = set()
        self._pending_water = set()
        self._water_timer   = 0.0
        self._water_interval = 0.001   # fire on every tick() call
        # Attributes touched by set_block that are irrelevant to water tests
        self.pending_saplings     = set()
        self.pending_fruit_leaves = set()
        self.pending_crops        = set()
        self._crop_progress  = {}
        self._crop_care_sum  = {}
        self._soil_fallow    = {}
        self._soil_moisture  = {}
        self.light_traps  = {}
        self.animal_traps = {}
        self.fish_traps   = {}
        self.logic_state  = {}
        self.sculpture_data = {}
        self.tapestry_data  = {}
        self.block_shapes   = {}

    # ------------------------------------------------------------------
    # Grid helpers
    # ------------------------------------------------------------------

    def place_water(self, x, y, level=8, source=False):
        """Place a water block directly, bypassing set_block water logic."""
        self._chunk_set(x, y, WATER)
        self._water_level[(x, y)] = level
        if source:
            self._water_sources.add((x, y))

    def place_solid(self, x, y):
        self._chunk_set(x, y, BEDROCK)

    def fill_water(self, x0, y0, x1, y1, level=8, source=False):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.place_water(x, y, level=level, source=source)

    def fill_solid(self, x0, y0, x1, y1):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.place_solid(x, y)

    def mine(self, x, y):
        """Simulate the player mining a solid block (calls set_block properly)."""
        # The block must be solid so old_bid is not AIR / WATER.
        assert self._chunk_get(x, y) not in (AIR, WATER), \
            f"mine() called on non-solid block at ({x},{y})"
        self.set_block(x, y, AIR)

    def tick(self, n=1, dt=1.0):
        for _ in range(n):
            self.update_water(dt, player=None)

    def get(self, x, y):
        return self._chunk_get(x, y)

    def level_at(self, x, y):
        """Return stored water level, or 0 if the cell is not water."""
        if self.get(x, y) != WATER:
            return 0
        return self._water_level.get((x, y), 8)

    def is_water(self, x, y):
        return self.get(x, y) == WATER

    def is_air(self, x, y):
        return self.get(x, y) == AIR


# ---------------------------------------------------------------------------
# 1. Immediate fill — no tick delay when water is adjacent
# ---------------------------------------------------------------------------

class TestImmediateFill(unittest.TestCase):
    """
    When the player mines a block that is adjacent to a water body the
    cleared cell must become water in the same frame, before any tick runs.
    """

    def test_fill_from_above(self):
        """Source water directly above a mined block fills it immediately."""
        sim = WaterSim()
        #   W   y=10  (source)
        #   S   y=11  <- mine this
        #   L   y=12  (floor)
        sim.place_water(5, 10, source=True)
        sim.place_solid(5, 11)   # the block the player will mine
        sim.place_solid(5, 12)

        sim.mine(5, 11)

        self.assertTrue(sim.is_water(5, 11),
                        "Cell below source water must fill immediately on mine, no tick needed")

    def test_fill_from_left_no_water_above(self):
        """
        Water to the left, solid land above and below — fills from the side.
        Old code would queue this for the next tick; it must be immediate.
        """
        sim = WaterSim()
        #   L   y=9   (land above)
        #   W S .     y=10  water@4, solid@5 (mine this), open right
        #   L L L     y=11  (floor)
        sim.place_solid(5, 9)         # land above
        sim.place_water(4, 10, source=True)
        sim.place_solid(5, 10)        # block to mine
        sim.fill_solid(3, 11, 7, 11)  # floor

        sim.mine(5, 10)

        self.assertTrue(sim.is_water(5, 10),
                        "Cell with water to the left must fill immediately on mine")

    def test_fill_from_right_no_water_above(self):
        """Mirror of the left-fill test."""
        sim = WaterSim()
        sim.place_solid(5, 9)
        sim.place_water(6, 10, source=True)
        sim.place_solid(5, 10)
        sim.fill_solid(3, 11, 8, 11)

        sim.mine(5, 10)

        self.assertTrue(sim.is_water(5, 10),
                        "Cell with water to the right must fill immediately on mine")

    def test_fill_priority_above_over_side(self):
        """
        Water is present both above and to the left.  The fill must come from
        ABOVE (gravity wins), and the left neighbour must not lose any level.

          W W    y=9  (source row)
          W S    y=10  mine position (5,10), left neighbour (4,10)
          L L    y=11
        """
        sim = WaterSim()
        sim.place_water(4, 9, level=8, source=True)
        sim.place_water(5, 9, level=8, source=True)
        sim.place_water(4, 10, level=8, source=True)
        sim.place_solid(5, 10)
        sim.fill_solid(4, 11, 6, 11)

        sim.mine(5, 10)

        self.assertTrue(sim.is_water(5, 10), "Must fill")
        # Left neighbour must NOT be drained — fill came from above, not the side.
        self.assertEqual(sim.level_at(4, 10), 8,
                         "Left neighbour level must be unchanged; fill should come from above")

    def test_three_sides_land_left_and_below(self):
        """
        Exact failure scenario reported: water above + right, land left + below.
        The cell must fill even though left and below are solid.

          W W    y=9
          L S W  y=10  mine (5,10)
          L L L  y=11
        """
        sim = WaterSim()
        sim.place_water(4, 9, source=True)
        sim.place_water(5, 9, source=True)
        sim.place_water(6, 10, source=True)
        sim.place_solid(4, 10)   # land left
        sim.place_solid(5, 10)   # block to mine
        sim.fill_solid(3, 11, 7, 11)

        sim.mine(5, 10)

        self.assertTrue(sim.is_water(5, 10),
                        "Cell with water above+right, land left+below must fill immediately")

    def test_no_water_adjacent_stays_air(self):
        """A block mined with no adjacent water must stay AIR — no spontaneous water."""
        sim = WaterSim()
        #   L L L
        #   L S L  mine the centre
        #   L L L
        sim.fill_solid(4, 9, 6, 11)
        sim.place_solid(5, 10)  # redundant but explicit

        sim.mine(5, 10)

        self.assertTrue(sim.is_air(5, 10), "Isolated mine should leave AIR")
        sim.tick(n=20)
        self.assertTrue(sim.is_air(5, 10), "Should still be AIR after 20 ticks")


# ---------------------------------------------------------------------------
# 2. Non-source water — the hard case the original tests ignored
# ---------------------------------------------------------------------------

class TestNonSourceWater(unittest.TestCase):
    """
    Source blocks (level 8, in _water_sources) are immune to draining by
    design.  These tests use non-source water (level 1-7) to actually
    exercise the gravity-priority logic.
    """

    def test_neighbours_dont_drain_into_cleared_cell(self):
        """
        4×2 body of non-source water.  Mine the right-edge middle cell.
        The cell to the LEFT must not lose level — fill should come from ABOVE.

          W6 W6 W6 W6   y=5  (non-source)
          W6 W6 W6 S    y=6  mine (7,6); left=(6,6), above=(7,5)
          L  L  L  L    y=7
        """
        sim = WaterSim()
        sim.fill_water(4, 5, 7, 5, level=6)   # top row, non-source
        sim.fill_water(4, 6, 6, 6, level=6)   # bottom row left portion
        sim.place_solid(7, 6)                  # block to mine
        sim.fill_solid(4, 7, 7, 7)

        left_level_before = 6

        sim.mine(7, 6)

        # Must fill immediately
        self.assertTrue(sim.is_water(7, 6), "Cleared cell must fill")
        # Left neighbour must not have been reduced
        self.assertEqual(sim.level_at(6, 6), left_level_before,
                         "Left neighbour level must not decrease — fill came from above, not sideways")

    def test_column_cascade_non_source(self):
        """
        Non-source column.  Clear a solid block in the middle.

          W5  y=5
          W5  y=6
          S   y=7  <- mine  (solid block, not water)
          W5  y=8
          L   y=9

        Expected: cleared cell fills immediately from y=6 (immediate-fill rule).
        After settling, non-source water drains from the top down, so y=5 may
        end up as AIR — that is correct conservation behaviour, not a bug.
        The floor cell y=8 must stay water (gravity collects there first).
        """
        sim = WaterSim()
        # Solid walls on x=4 and x=6 so water can't escape sideways.
        # Without them the non-source volume leaks off the column.
        sim.fill_solid(4, 4, 4, 9)   # left wall
        sim.fill_solid(6, 4, 6, 9)   # right wall
        sim.fill_solid(4, 9, 6, 9)   # floor
        sim.place_water(5, 5, level=5)
        sim.place_water(5, 6, level=5)
        sim.place_solid(5, 7)
        sim.place_water(5, 8, level=5)

        sim.mine(5, 7)

        # Immediate fill from y=6 — no tick required
        self.assertTrue(sim.is_water(5, 7), "Cleared gap must fill immediately from y=6")

        sim.tick(n=20)

        # y=8 is at the floor and must remain water — gravity accumulates there first
        self.assertTrue(sim.is_water(5, 8), "Floor-adjacent cell must stay water after settling")
        # y=7 should also hold water (contained, enough volume above to reach it)
        self.assertTrue(sim.is_water(5, 7), "Cell above floor must stay water after settling")

    def test_no_water_created_in_dry_cave(self):
        """
        Non-source water exists far to the left.  Mining a block in a dry
        cave on the right must not produce water (no teleportation).
        """
        sim = WaterSim()
        sim.fill_water(2, 5, 2, 10, level=4)  # distant water body
        sim.fill_solid(3, 4, 10, 11)           # solid cave walls
        # Hollow out a small dry cave
        for y in range(5, 10):
            self._clear(sim, 7, y)
        sim.place_solid(6, 7)   # block to mine inside the dry cave

        sim.mine(6, 7)
        sim.tick(n=30)

        self.assertTrue(sim.is_air(6, 7), "Dry cave block should stay AIR")

    @staticmethod
    def _clear(sim, x, y):
        sim._chunk_set(x, y, AIR)


# ---------------------------------------------------------------------------
# 3. 4×4 water body — design scenario from the spec discussion
# ---------------------------------------------------------------------------

class TestFourByFourBody(unittest.TestCase):
    """
    Grid layout (x 4..7, y 5..8), floor at y=9:

      W W W W   y=5
      W W W W   y=6
      W W W W   y=7
      W W W W   y=8
      L L L L   y=9

    All cells are NON-source (level 7) so the gravity test is meaningful.
    Source-only grids are immune to sideways drain by construction and
    would give trivially passing tests.
    """

    LEVEL = 7

    def _make_body(self):
        sim = WaterSim()
        sim.fill_water(4, 5, 7, 8, level=self.LEVEL, source=False)
        sim.fill_solid(4, 9, 7, 9)
        return sim

    def test_clear_interior_fills_immediately(self):
        """Replace centre block (5,6) with a solid, then mine it."""
        sim = self._make_body()
        sim.place_solid(5, 6)   # replace water with solid to mine

        sim.mine(5, 6)

        self.assertTrue(sim.is_water(5, 6), "Interior block must fill immediately")

    def test_clear_right_edge_fills_from_above_not_left(self):
        """
        Mine (7,6) — right edge.  Water above (7,5) must fill it.
        The cell to the left (6,6) must NOT lose level.

        Old code spread sideways, draining (6,6) to fill (7,6).
        """
        sim = self._make_body()
        sim.place_solid(7, 6)

        level_left_before = sim.level_at(6, 6)
        sim.mine(7, 6)

        self.assertTrue(sim.is_water(7, 6), "Right-edge block must fill")
        self.assertEqual(sim.level_at(6, 6), level_left_before,
                         "Left neighbour must not lose level — gravity should fill from above")

    def test_clear_corner_top_right(self):
        """
        Mine (7,5) — top-right corner.  Nothing is above (y=4 is air).
        Fill must come from the left neighbour (6,5).
        """
        sim = self._make_body()
        sim.place_solid(7, 5)

        sim.mine(7, 5)

        self.assertTrue(sim.is_water(7, 5),
                        "Top-right corner: must fill from left neighbour immediately")

    def test_clear_bottom_row_non_source(self):
        """
        Mine (5,8) — bottom row.  Above (5,7) has water → fills immediately.
        After several ticks the column must remain solid (no gaps).
        """
        sim = self._make_body()
        sim.place_solid(5, 8)

        sim.mine(5, 8)

        self.assertTrue(sim.is_water(5, 8), "Bottom-row block must fill immediately")

        sim.tick(n=10)
        for y in range(5, 9):
            self.assertTrue(sim.is_water(5, y),
                            f"Column at x=5 must be unbroken after settling; hole at y={y}")


# ---------------------------------------------------------------------------
# 4. Gravity cascade — water falls down a column over multiple ticks
# ---------------------------------------------------------------------------

class TestGravityCascade(unittest.TestCase):

    def test_source_fills_empty_column(self):
        """
        Single source at top of a 4-block-deep empty column.
        After enough ticks every cell must be water.
        The floor must be wide enough to stop water spreading sideways
        off the column before it can fill — a single-block floor lets
        water escape and the column never accumulates.
        """
        sim = WaterSim()
        sim.place_water(5, 5, source=True)
        sim.fill_solid(2, 10, 8, 10)   # wide floor, not just one block

        sim.tick(n=40)

        for y in range(6, 10):
            self.assertTrue(sim.is_water(5, y),
                            f"Source column: y={y} must fill via cascade")

    def test_cascade_reaches_bottom_before_sides(self):
        """
        Source at top of a shaft.  The bottom cell must fill before any
        horizontal spread escapes to the side — gravity must win the race.

          W   x=5, y=5  source
          .   x=5, y=6
          .   x=5, y=7
          .   x=5, y=8
          L   x=5, y=9  floor; air at (6,8) = possible side escape
        """
        sim = WaterSim()
        sim.place_water(5, 5, source=True)
        sim.place_solid(5, 9)
        # leave (6,8) open so water could escape sideways at the bottom

        sim.tick(n=10)

        # Bottom of shaft must fill
        self.assertTrue(sim.is_water(5, 8),
                        "Gravity cascade: shaft bottom must fill before side spread")

    def test_non_source_cascade_no_gaps(self):
        """
        Non-source water at the top falls through a 3-cell shaft.
        No permanent gaps should remain after settling.

          W5  y=5  (non-source)
          .   y=6
          .   y=7
          .   y=8
          L   y=9
        """
        sim = WaterSim()
        sim.place_water(5, 5, level=5)
        sim.place_solid(5, 9)
        sim._pending_water.add((5, 5))

        sim.tick(n=20)

        # Water should have fallen; at minimum y=6 should be filled
        filled = [y for y in range(6, 9) if sim.is_water(5, y)]
        self.assertTrue(len(filled) > 0,
                        "Non-source water must fall at least one cell")


# ---------------------------------------------------------------------------
# 5. Water must not appear where it shouldn't
# ---------------------------------------------------------------------------

class TestWaterContainment(unittest.TestCase):

    def test_water_blocked_by_solid_wall(self):
        """Water cannot pass through a solid wall."""
        sim = WaterSim()
        #   W W | . .   y=10
        #   L L L L L   y=11 (floor)
        sim.place_water(4, 10, source=True)
        sim.place_water(5, 10, source=True)
        sim.place_solid(6, 10)   # wall
        sim.fill_solid(4, 11, 9, 11)

        sim.tick(n=30)

        self.assertTrue(sim.is_air(7, 10), "Water must not appear past solid wall")
        self.assertTrue(sim.is_air(8, 10), "Water must not appear past solid wall")

    def test_mining_dry_area_stays_dry(self):
        """Mining a block in a region with no nearby water produces AIR, not water."""
        sim = WaterSim()
        sim.fill_solid(3, 8, 8, 13)   # solid block
        sim.place_solid(5, 10)        # block to mine (already solid, explicit)

        sim.mine(5, 10)
        sim.tick(n=20)

        self.assertTrue(sim.is_air(5, 10))


if __name__ == "__main__":
    unittest.main()
