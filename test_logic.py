"""
Wire and logic gate tests.
No pygame required — tests evaluate_full_network in isolation.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from blocks import (
    AND_GATE_BLOCK, OR_GATE_BLOCK, NOT_GATE_BLOCK,
    SWITCH_BLOCK_ON, PRESSURE_PLATE_ON, PRESSURE_PLATE_OFF,
    ALARM_BELL_OFF, ALARM_BELL_ON,
)
import logic

WORLD_H = 256
WORLD_MAX_X = 5000


class MockWorld:
    def __init__(self):
        self._blocks = {}
        self._wires  = {}
        self.logic_state   = {}
        self.powered_wires = set()
        self.entities   = []
        self.chest_data = {}
        self.fish_traps = {}
        self.automations = []
        self.farm_bots   = []

    def get_block(self, x, y):
        return self._blocks.get((x, y), 0)

    def set_block(self, x, y, bid):
        self._blocks[(x, y)] = bid

    def get_wire(self, x, y):
        if y < 0 or y >= WORLD_H or abs(x) > WORLD_MAX_X:
            return 0
        return self._wires.get((x, y), 0)

    # ── helpers ──────────────────────────────────────────────────────────────

    def source(self, x, y):
        """Place an always-on switch source."""
        self._blocks[(x, y)] = SWITCH_BLOCK_ON
        self.logic_state[(x, y)] = {}          # must be in logic_state to be seeded

    def pressure_plate(self, x, y, pressed=False):
        """Place a pressure plate, optionally pressed."""
        bid = PRESSURE_PLATE_ON if pressed else PRESSURE_PLATE_OFF
        self._blocks[(x, y)] = bid
        self.logic_state[(x, y)] = {}

    def alarm(self, x, y):
        """Place an alarm bell output block."""
        self._blocks[(x, y)] = ALARM_BELL_OFF
        self.logic_state[(x, y)] = {"facing": "right", "latch_state": False, "prev_input": False}

    def wire(self, *positions):
        for x, y in positions:
            self._wires[(x, y)] = 1

    def gate(self, x, y, block_id, facing="right"):
        self._blocks[(x, y)] = block_id
        self.logic_state[(x, y)] = {"facing": facing}

    def on(self, x, y):
        return (x, y) in self.powered_wires


def run(world):
    logic.evaluate_full_network(world)


# ── Test cases ───────────────────────────────────────────────────────────────

def test_wire_propagates_from_source():
    w = MockWorld()
    w.source(0, 0)
    w.wire((1, 0), (2, 0), (3, 0))
    run(w)
    assert w.on(1, 0), "wire adjacent to source should be powered"
    assert w.on(2, 0), "wire 2 tiles away should be powered"
    assert w.on(3, 0), "wire 3 tiles away should be powered"


def test_and_gate_three_wires_one_unpowered_blocked():
    # 3 wires (N=3, threshold=2): only 1 powered → must NOT fire
    w = MockWorld()
    w.source(0, 2)
    w.wire((1, 2))          # left — powered
    w.wire((2, 1))          # top — connected but no source
    w.gate(2, 2, AND_GATE_BLOCK)
    w.wire((3, 2))          # right — output, unpowered
    run(w)
    assert w.on(1, 2),      "powered wire should be on"
    assert not w.on(2, 1),  "unpowered wire should stay off"
    assert not w.on(3, 2),  "AND gate (3 wires, 1 powered) must NOT fire"


def test_and_gate_two_wires_acts_as_buffer():
    # 2 wires (N=2, threshold=1): 1 powered → fires (N-1 model makes 2-wire AND a buffer)
    w = MockWorld()
    w.source(0, 2)
    w.wire((1, 2))           # left wire — powered
    w.gate(2, 2, AND_GATE_BLOCK)
    w.wire((3, 2))           # right wire — output
    run(w)
    assert w.on(1, 2),  "powered wire should be on"
    assert w.on(3, 2),  "AND gate with 2 wires, 1 powered acts as buffer (N-1=1 threshold)"


def test_and_gate_two_inputs_both_on_fires():
    # Left and top wires both powered → gate fires
    w = MockWorld()
    w.source(0, 2)
    w.wire((1, 2))                          # left input
    w.source(2, 0)
    w.wire((2, 1))                          # top input
    w.gate(2, 2, AND_GATE_BLOCK, facing="right")
    w.wire((3, 2))                          # output
    run(w)
    assert w.on(1, 2), "left input should be powered"
    assert w.on(2, 1), "top input should be powered"
    assert w.on(3, 2), "AND gate with all connected inputs powered should fire"


def test_and_gate_two_inputs_one_off_blocked():
    # Left wire powered, top wire exists but unpowered → gate must NOT fire
    w = MockWorld()
    w.source(0, 2)
    w.wire((1, 2))                          # left input (powered)
    w.wire((2, 1))                          # top input wire — no source
    w.gate(2, 2, AND_GATE_BLOCK, facing="right")
    w.wire((3, 2))
    run(w)
    assert w.on(1, 2),      "left input should be powered"
    assert not w.on(2, 1),  "top input has no source, should be unpowered"
    assert not w.on(3, 2),  "AND gate should NOT fire when an input is off"


def test_or_gate_one_input_fires():
    w = MockWorld()
    w.source(0, 2)
    w.wire((1, 2))
    w.gate(2, 2, OR_GATE_BLOCK, facing="right")
    w.wire((3, 2))
    run(w)
    assert w.on(3, 2), "OR gate with one powered input should fire"


def test_or_gate_no_inputs_blocked():
    w = MockWorld()
    w.wire((1, 2))                          # wire exists but no source
    w.gate(2, 2, OR_GATE_BLOCK, facing="right")
    w.wire((3, 2))
    run(w)
    assert not w.on(3, 2), "OR gate with no powered inputs should NOT fire"


def test_not_gate_fires_with_no_input():
    w = MockWorld()
    w.gate(2, 2, NOT_GATE_BLOCK, facing="right")
    w.wire((3, 2))
    run(w)
    assert w.on(3, 2), "NOT gate with unpowered input should fire"


def test_not_gate_blocked_when_input_on():
    w = MockWorld()
    w.source(0, 2)
    w.wire((1, 2))
    w.gate(2, 2, NOT_GATE_BLOCK, facing="right")
    w.wire((3, 2))
    run(w)
    assert w.on(1, 2),      "input wire to NOT gate should be powered"
    assert not w.on(3, 2),  "NOT gate with powered input should NOT fire"


def test_two_pressure_plates_and_gate_alarm():
    """
    Layout: plate1(0,2) --wire(1,2)--> AND gate(2,2,right) --wire(3,2)--> alarm(4,2)
                          plate2(2,0) --wire(2,1)----------/
    """
    def make_world(p1_pressed, p2_pressed):
        w = MockWorld()
        w.pressure_plate(0, 2, pressed=p1_pressed)
        w.wire((1, 2))
        w.pressure_plate(2, 0, pressed=p2_pressed)
        w.wire((2, 1))
        w.gate(2, 2, AND_GATE_BLOCK, facing="right")
        w.wire((3, 2))
        w.alarm(4, 2)
        return w

    # Neither plate pressed → alarm off
    w = make_world(False, False)
    run(w)
    assert not w.on(3, 2), "alarm wire should be off when no plates pressed"
    assert w.get_block(4, 2) == ALARM_BELL_OFF, "alarm should be off"

    # Only plate 1 pressed → alarm off
    w = make_world(True, False)
    run(w)
    assert not w.on(3, 2), "alarm wire should be off when only plate 1 pressed"
    assert w.get_block(4, 2) == ALARM_BELL_OFF, "alarm should be off"

    # Only plate 2 pressed → alarm off
    w = make_world(False, True)
    run(w)
    assert not w.on(3, 2), "alarm wire should be off when only plate 2 pressed"
    assert w.get_block(4, 2) == ALARM_BELL_OFF, "alarm should be off"

    # Both plates pressed → alarm ON
    w = make_world(True, True)
    run(w)
    assert w.on(3, 2), "alarm wire should be powered when both plates pressed"
    assert w.get_block(4, 2) == ALARM_BELL_ON, "alarm should ring"


def test_and_gate_three_wires_blocks_reverse_flow():
    # 3 wires (N=3, threshold=2): only the "output" wire is externally powered (n=1 < 2)
    # Gate must NOT fire, so the two input wires stay unpowered.
    w = MockWorld()
    w.source(5, 2)
    w.wire((4, 2))          # one wire — powered externally
    w.gate(3, 2, AND_GATE_BLOCK)
    w.wire((2, 2))          # second wire — no source
    w.wire((3, 1))          # third wire — no source
    run(w)
    assert w.on(4, 2),      "externally powered wire should be on"
    assert not w.on(2, 2),  "unpowered wire must stay off (only 1 of 3 powered)"
    assert not w.on(3, 1),  "unpowered wire must stay off (only 1 of 3 powered)"


# ── Runner ───────────────────────────────────────────────────────────────────

TESTS = [
    test_wire_propagates_from_source,
    test_and_gate_three_wires_one_unpowered_blocked,
    test_and_gate_two_wires_acts_as_buffer,
    test_and_gate_two_inputs_both_on_fires,
    test_and_gate_two_inputs_one_off_blocked,
    test_or_gate_one_input_fires,
    test_or_gate_no_inputs_blocked,
    test_not_gate_fires_with_no_input,
    test_not_gate_blocked_when_input_on,
    test_two_pressure_plates_and_gate_alarm,
    test_and_gate_three_wires_blocks_reverse_flow,
]

if __name__ == "__main__":
    passed = failed = 0
    for t in TESTS:
        try:
            t()
            print(f"PASS  {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"FAIL  {t.__name__}: {e}")
            failed += 1
        except Exception as e:
            import traceback
            print(f"ERROR {t.__name__}: {e}")
            traceback.print_exc()
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)
