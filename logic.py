import random as _random
from collections import deque
from blocks import (
    LOGIC_SOURCE_BLOCKS, LOGIC_OUTPUT_BLOCKS,
    LOGIC_SENSOR_BLOCKS, LOGIC_TIMER_BLOCKS,
    FISH_TRAP_BLOCKS,
    AND_GATE_BLOCK, OR_GATE_BLOCK, NOT_GATE_BLOCK,
    REPEATER_BLOCK, PULSE_GEN_BLOCK,
    RS_LATCH_Q0, RS_LATCH_Q1,
    COUNTER_BLOCK, COMPARATOR_BLOCK, OBSERVER_BLOCK,
    SEQUENCER_BLOCK, T_FLIPFLOP_BLOCK,
    DEPOSIT_TRIGGER_BLOCK,
    DAY_SENSOR_BLOCK, NIGHT_SENSOR_BLOCK,
    WATER_SENSOR_BLOCK, CROP_SENSOR_BLOCK,
    PRESSURE_PLATE_OFF, PRESSURE_PLATE_ON,
    DAM_BLOCK_CLOSED, DAM_BLOCK_OPEN,
    PUMP_BLOCK_OFF, PUMP_BLOCK_ON,
    IRON_GATE_BLOCK_CLOSED, IRON_GATE_BLOCK_OPEN,
    POWERED_LANTERN_OFF, POWERED_LANTERN_ON,
    ALARM_BELL_OFF, ALARM_BELL_ON,
    WATER, MATURE_CROP_BLOCKS, CHEST_BLOCK,
)
from constants import BLOCK_SIZE as _BS, PLAYER_W as _PW, PLAYER_H as _PH

_DIRS = [(0, -1), (0, 1), (-1, 0), (1, 0)]

# Fixed step directions for sequencer (absolute, not facing-relative)
_SEQ_DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

_OPEN_STATE = {
    DAM_BLOCK_CLOSED: DAM_BLOCK_OPEN,   DAM_BLOCK_OPEN: DAM_BLOCK_OPEN,
    PUMP_BLOCK_OFF:   PUMP_BLOCK_ON,    PUMP_BLOCK_ON:  PUMP_BLOCK_ON,
    IRON_GATE_BLOCK_CLOSED: IRON_GATE_BLOCK_OPEN,
    IRON_GATE_BLOCK_OPEN:   IRON_GATE_BLOCK_OPEN,
    POWERED_LANTERN_OFF: POWERED_LANTERN_ON,
    POWERED_LANTERN_ON:  POWERED_LANTERN_ON,
    ALARM_BELL_OFF: ALARM_BELL_ON,
    ALARM_BELL_ON:  ALARM_BELL_ON,
}
_CLOSED_STATE = {
    DAM_BLOCK_CLOSED: DAM_BLOCK_CLOSED, DAM_BLOCK_OPEN: DAM_BLOCK_CLOSED,
    PUMP_BLOCK_OFF:   PUMP_BLOCK_OFF,   PUMP_BLOCK_ON:  PUMP_BLOCK_OFF,
    IRON_GATE_BLOCK_CLOSED: IRON_GATE_BLOCK_CLOSED,
    IRON_GATE_BLOCK_OPEN:   IRON_GATE_BLOCK_CLOSED,
    POWERED_LANTERN_OFF: POWERED_LANTERN_OFF,
    POWERED_LANTERN_ON:  POWERED_LANTERN_OFF,
    ALARM_BELL_OFF: ALARM_BELL_OFF,
    ALARM_BELL_ON:  ALARM_BELL_OFF,
}


def evaluate_full_network(world):
    """
    Re-evaluate the entire wire network from scratch.
    Phase 1: seed all sources → BFS through wire and AND/OR gates.
    Phase 2: NOT gate inversion (loop-guarded).
    Phase 2b: RS latch resolution.
    Phase 3: apply output block state changes.
    """
    powered = set()
    queue = deque()
    visited = set()

    # --- Phase 1: seed omnidirectional sources, then directional memory blocks ---
    for (bx, by), gs in world.logic_state.items():
        bid = world.get_block(bx, by)
        facing = gs.get("facing", "right")

        # Omnidirectional sources (spread in all directions via BFS)
        is_omni_source = (
            bid in LOGIC_SOURCE_BLOCKS
            or (bid in LOGIC_SENSOR_BLOCKS and gs.get("sensor_on", False))
            or (bid == PULSE_GEN_BLOCK and gs.get("pulse_on", False))
            or (bid == REPEATER_BLOCK and gs.get("active_out", False))
        )
        if is_omni_source:
            powered.add((bx, by))
            visited.add((bx, by))
            queue.append((bx, by))
            continue

        # Directional memory sources: powered only if their stored state is active,
        # and they only emit through their designated output wire.
        out_pos = None
        if bid == COUNTER_BLOCK and gs.get("count", 0) >= gs.get("threshold", 4):
            fdx, fdy = _facing_dir(facing)
            out_pos = (bx + fdx, by + fdy)
        elif bid == T_FLIPFLOP_BLOCK and gs.get("q", False):
            fdx, fdy = _facing_dir(facing)
            out_pos = (bx + fdx, by + fdy)
        elif bid == COMPARATOR_BLOCK and gs.get("comp_on", False):
            fdx, fdy = _facing_dir(facing)
            out_pos = (bx + fdx, by + fdy)
        elif bid == OBSERVER_BLOCK and gs.get("pulse_ticks", 0) > 0:
            # Output comes out the back (opposite of the watched direction)
            odx, ody = _opposite_dir(facing)
            out_pos = (bx + odx, by + ody)
        elif bid == SEQUENCER_BLOCK:
            # Always emits on current step's output channel
            sdx, sdy = _SEQ_DIRS[gs.get("step", 0) % 4]
            out_pos = (bx + sdx, by + sdy)

        if out_pos is not None:
            powered.add((bx, by))
            visited.add((bx, by))
            if out_pos not in visited and world.get_wire(*out_pos) == 1:
                powered.add(out_pos)
                visited.add(out_pos)
                queue.append(out_pos)

    # BFS through wires and AND/OR gates
    while queue:
        bx, by = queue.popleft()
        for dx, dy in _DIRS:
            nx, ny = bx + dx, by + dy
            if (nx, ny) in visited:
                continue
            nw = world.get_wire(nx, ny)
            nb = world.get_block(nx, ny)
            if nw == 1:
                powered.add((nx, ny))
                visited.add((nx, ny))
                queue.append((nx, ny))
            elif nb in (AND_GATE_BLOCK, OR_GATE_BLOCK):
                # Symmetric: no fixed input/output sides.
                # AND: fires when all-but-one connected wire is powered (N-1 threshold).
                #      The one unpowered wire is the natural "output" — it gets powered.
                # OR:  fires when any connected wire is powered.
                # Both emit to all connected wires when triggered.
                connected = [(nx+dx, ny+dy) for dx, dy in _DIRS
                             if world.get_wire(nx+dx, ny+dy) == 1]
                n_powered = sum(1 for p in connected if p in powered)
                triggered = (
                    bool(connected) and n_powered >= len(connected) - 1
                    if nb == AND_GATE_BLOCK
                    else n_powered > 0
                )
                if triggered:
                    powered.add((nx, ny))
                    visited.add((nx, ny))
                    for ox, oy in connected:
                        if (ox, oy) not in visited:
                            powered.add((ox, oy))
                            visited.add((ox, oy))
                            queue.append((ox, oy))

    # --- Phase 2: NOT gate (loop-guarded, up to 8 passes) ---
    for _ in range(8):
        added = False
        for (bx, by), gs in world.logic_state.items():
            if world.get_block(bx, by) != NOT_GATE_BLOCK:
                continue
            if (bx, by) in powered:
                continue
            facing = gs.get("facing", "right")
            in_dx, in_dy = _opposite_dir(facing)
            if (bx + in_dx, by + in_dy) not in powered:
                powered.add((bx, by))
                added = True
                out_dx, out_dy = _facing_dir(facing)
                _bfs_from((bx + out_dx, by + out_dy), powered, world)
        if not added:
            break

    # --- Phase 2b: RS latch (edge-triggered state, up to 4 passes) ---
    for _ in range(4):
        rs_changed = False
        for (bx, by), gs in world.logic_state.items():
            bid = world.get_block(bx, by)
            if bid not in (RS_LATCH_Q0, RS_LATCH_Q1):
                continue
            facing = gs.get("facing", "right")
            s_pos, r_pos = _rs_inputs(bx, by, facing)
            s_on, r_on = s_pos in powered, r_pos in powered
            if r_on and bid == RS_LATCH_Q1:
                world.set_block(bx, by, RS_LATCH_Q0)
                powered.discard((bx, by))
                rs_changed = True
            elif s_on and not r_on and bid == RS_LATCH_Q0:
                world.set_block(bx, by, RS_LATCH_Q1)
                powered.add((bx, by))
                visited.add((bx, by))
                out_dx, out_dy = _facing_dir(facing)
                _bfs_from((bx + out_dx, by + out_dy), powered, world)
                rs_changed = True
        if not rs_changed:
            break

    # --- Phase 3: apply output block state changes ---
    for (bx, by) in list(world.logic_state.keys()):
        bid = world.get_block(bx, by)
        if bid not in LOGIC_OUTPUT_BLOCKS:
            continue
        adj_powered = any((bx + dx, by + dy) in powered for dx, dy in _DIRS)
        new_bid = _OPEN_STATE[bid] if adj_powered else _CLOSED_STATE[bid]
        if new_bid != bid:
            world.set_block(bx, by, new_bid)

    world.powered_wires = powered


def logic_tick(world, dt, player):
    """Per-frame: poll sensors, advance timers, update edge-triggered memory blocks."""
    changed = False

    for (bx, by), gs in list(world.logic_state.items()):
        bid = world.get_block(bx, by)

        # ── Pressure plate ──────────────────────────────────────────────────
        if bid in (PRESSURE_PLATE_OFF, PRESSURE_PLATE_ON):
            bx1, by1 = bx * _BS, by * _BS
            bx2, by2 = bx1 + _BS, by1 + _BS
            pr = player.rect
            occupied = pr.left < bx2 and pr.right > bx1 and pr.top < by2 and pr.bottom >= by1
            if not occupied:
                for ent in world.entities:
                    ex = getattr(ent, 'x', None)
                    if ex is None:
                        continue
                    ey, ew, eh = getattr(ent, 'y', 0), getattr(ent, 'W', _BS), getattr(ent, 'H', _BS)
                    if ex < bx2 and ex + ew > bx1 and ey < by2 and ey + eh >= by1:
                        occupied = True
                        break
            new_bid = PRESSURE_PLATE_ON if occupied else PRESSURE_PLATE_OFF
            if new_bid != bid:
                world.set_block(bx, by, new_bid)
                changed = True

        # ── Day sensor ──────────────────────────────────────────────────────
        elif bid == DAY_SENSOR_BLOCK:
            from world import DAY_DURATION as _DD
            tod = world.time_of_day
            now_on = 60.0 <= tod < (_DD - 60.0)
            if gs.get("sensor_on", False) != now_on:
                gs["sensor_on"] = now_on
                changed = True

        # ── Night sensor ────────────────────────────────────────────────────
        elif bid == NIGHT_SENSOR_BLOCK:
            from world import DAY_DURATION as _DD
            tod = world.time_of_day
            now_on = tod < 60.0 or tod >= (_DD - 60.0)
            if gs.get("sensor_on", False) != now_on:
                gs["sensor_on"] = now_on
                changed = True

        # ── Water sensor ────────────────────────────────────────────────────
        elif bid == WATER_SENSOR_BLOCK:
            now_on = any(world.get_block(bx + dx, by + dy) == WATER for dx, dy in _DIRS)
            if gs.get("sensor_on", False) != now_on:
                gs["sensor_on"] = now_on
                changed = True

        # ── Crop sensor ─────────────────────────────────────────────────────
        elif bid == CROP_SENSOR_BLOCK:
            now_on = world.get_block(bx, by + 1) in MATURE_CROP_BLOCKS
            if gs.get("sensor_on", False) != now_on:
                gs["sensor_on"] = now_on
                changed = True

        # ── Fish trap sensor — HIGH when trap has accumulated fish ───────────
        elif bid in FISH_TRAP_BLOCKS:
            trap   = world.fish_traps.get((bx, by))
            now_on = bool(trap and trap.get("accumulated"))
            if gs.get("sensor_on", False) != now_on:
                gs["sensor_on"] = now_on
                changed = True

        # ── Pulse generator ─────────────────────────────────────────────────
        elif bid == PULSE_GEN_BLOCK:
            timer = gs.get("timer", 0.0) + dt
            period = gs.get("period", 2.0)
            if timer >= period:
                timer -= period
                gs["pulse_on"] = not gs.get("pulse_on", False)
                changed = True
            gs["timer"] = timer

        # ── Repeater ────────────────────────────────────────────────────────
        elif bid == REPEATER_BLOCK:
            facing = gs.get("facing", "right")
            in_dx, in_dy = _opposite_dir(facing)
            input_pos = (bx + in_dx, by + in_dy)
            input_powered = (input_pos in world.powered_wires
                             or world.get_block(*input_pos) in LOGIC_SOURCE_BLOCKS)
            prev_input = gs.get("prev_input", False)
            if input_powered and not prev_input:
                gs["prev_input"] = True
                gs["countdown"] = gs.get("delay", 0.5)
            elif not input_powered and prev_input:
                gs["prev_input"] = False
                gs["countdown"] = 0.0
                if gs.get("active_out", False):
                    gs["active_out"] = False
                    changed = True
            elif input_powered and gs.get("countdown", 0.0) > 0:
                gs["countdown"] -= dt
                if gs["countdown"] <= 0:
                    gs["countdown"] = 0.0
                    if not gs.get("active_out", False):
                        gs["active_out"] = True
                        changed = True

        # ── Counter ─────────────────────────────────────────────────────────
        # Input (opposite facing) counts rising edges.
        # Reset (left of facing) zeroes count when HIGH.
        # Output (facing) goes HIGH and stays HIGH when count >= threshold.
        elif bid == COUNTER_BLOCK:
            facing = gs.get("facing", "right")
            in_dx, in_dy = _opposite_dir(facing)
            input_powered = (bx + in_dx, by + in_dy) in world.powered_wires
            fdx, fdy = _facing_dir(facing)
            reset_powered = (bx + fdy, by - fdx) in world.powered_wires  # left of facing
            count = gs.get("count", 0)
            threshold = gs.get("threshold", 4)
            was_triggered = count >= threshold
            if reset_powered:
                if count != 0:
                    gs["count"] = 0
                    gs["prev_input"] = input_powered
                    changed = True
            elif input_powered and not gs.get("prev_input", False):
                gs["count"] = count + 1
                gs["prev_input"] = True
                now_triggered = gs["count"] >= threshold
                if now_triggered != was_triggered:
                    changed = True
            elif not input_powered and gs.get("prev_input", False):
                gs["prev_input"] = False

        # ── Comparator ──────────────────────────────────────────────────────
        # Reads fill level of any adjacent chest (0-8 scale).
        # Outputs when fill_level >= threshold.
        elif bid == COMPARATOR_BLOCK:
            threshold = gs.get("threshold", 4)
            fill_level = 0
            for dx, dy in _DIRS:
                chest = world.chest_data.get((bx + dx, by + dy))
                if chest is not None:
                    total = sum(chest.values())
                    fill_level = min(8, total // 4)
                    break
            was_on = gs.get("comp_on", False)
            now_on = fill_level >= threshold
            if now_on != was_on:
                gs["comp_on"] = now_on
                gs["fill_level"] = fill_level
                changed = True
            else:
                gs["fill_level"] = fill_level

        # ── Observer ────────────────────────────────────────────────────────
        # Watches the block one tile in facing direction.
        # Emits a 2-tick pulse out the back whenever that block ID changes.
        elif bid == OBSERVER_BLOCK:
            facing = gs.get("facing", "right")
            fdx, fdy = _facing_dir(facing)
            watched_bid = world.get_block(bx + fdx, by + fdy)
            prev_bid = gs.get("prev_block", -1)
            if watched_bid != prev_bid:
                gs["prev_block"] = watched_bid
                gs["pulse_ticks"] = 2
                changed = True
            elif gs.get("pulse_ticks", 0) > 0:
                gs["pulse_ticks"] -= 1
                if gs["pulse_ticks"] == 0:
                    changed = True

        # ── Sequencer ───────────────────────────────────────────────────────
        # Rising edge on input (opposite facing) advances step 0→1→2→3→0.
        # Always emits on current step's output channel (fixed: R/D/L/U).
        elif bid == SEQUENCER_BLOCK:
            facing = gs.get("facing", "right")
            in_dx, in_dy = _opposite_dir(facing)
            input_powered = (bx + in_dx, by + in_dy) in world.powered_wires
            if input_powered and not gs.get("prev_input", False):
                gs["step"] = (gs.get("step", 0) + 1) % 4
                gs["prev_input"] = True
                changed = True
            elif not input_powered and gs.get("prev_input", False):
                gs["prev_input"] = False

        # ── T-Flip-Flop ─────────────────────────────────────────────────────
        # Rising edge on input (opposite facing) toggles Q.
        # Output (facing) is HIGH when Q=True.
        elif bid == T_FLIPFLOP_BLOCK:
            facing = gs.get("facing", "right")
            in_dx, in_dy = _opposite_dir(facing)
            input_powered = (bx + in_dx, by + in_dy) in world.powered_wires
            if input_powered and not gs.get("prev_input", False):
                gs["q"] = not gs.get("q", False)
                gs["prev_input"] = True
                changed = True
            elif not input_powered and gs.get("prev_input", False):
                gs["prev_input"] = False

        # ── Deposit Trigger ─────────────────────────────────────────────────
        # Rising edge: dump nearby bot inventories into an adjacent chest.
        elif bid == DEPOSIT_TRIGGER_BLOCK:
            adj_powered = any((bx + dx, by + dy) in world.powered_wires for dx, dy in _DIRS)
            if adj_powered and not gs.get("prev_powered", False):
                _trigger_deposit(world, bx, by)
            gs["prev_powered"] = adj_powered

    if changed:
        evaluate_full_network(world)


# ── Registration helpers ─────────────────────────────────────────────────────

def register_output_block(world, bx, by):
    world.logic_state.setdefault((bx, by), {"facing": "right", "latch_state": False, "prev_input": False})

def register_sensor_block(world, bx, by):
    world.logic_state.setdefault((bx, by), {"sensor_on": False})

def register_repeater(world, bx, by, facing="right"):
    world.logic_state[(bx, by)] = {"facing": facing, "delay": 0.5,
                                    "countdown": 0.0, "active_out": False, "prev_input": False}

def register_pulse_gen(world, bx, by):
    world.logic_state[(bx, by)] = {"period": 2.0, "timer": 0.0, "pulse_on": False}

def register_rs_latch(world, bx, by, facing="right"):
    world.logic_state[(bx, by)] = {"facing": facing}

def register_counter(world, bx, by, facing="right"):
    world.logic_state[(bx, by)] = {"facing": facing, "count": 0, "threshold": 4, "prev_input": False}

def register_comparator(world, bx, by, facing="right"):
    world.logic_state[(bx, by)] = {"facing": facing, "threshold": 4, "comp_on": False, "fill_level": 0}

def register_observer(world, bx, by, facing="right"):
    world.logic_state[(bx, by)] = {"facing": facing, "prev_block": -1, "pulse_ticks": 0}

def register_sequencer(world, bx, by, facing="right"):
    world.logic_state[(bx, by)] = {"facing": facing, "step": 0, "prev_input": False}

def register_t_flipflop(world, bx, by, facing="right"):
    world.logic_state[(bx, by)] = {"facing": facing, "q": False, "prev_input": False}

def register_deposit_trigger(world, bx, by):
    world.logic_state[(bx, by)] = {"prev_powered": False}


def _trigger_deposit(world, bx, by):
    """On rising-edge power: dump nearby bot stored items into an adjacent chest."""
    RADIUS = 3
    all_bots = list(world.automations) + list(world.farm_bots)
    for bot in all_bots:
        if not bot.stored:
            continue
        cbx = int((bot.x + bot.W / 2) // _BS)
        cby = int((bot.y + bot.H / 2) // _BS)
        if abs(cbx - bx) > RADIUS or abs(cby - by) > RADIUS:
            continue
        for ddx, ddy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nx, ny = cbx + ddx, cby + ddy
            if world.get_block(nx, ny) == CHEST_BLOCK:
                chest = world.chest_data.setdefault((nx, ny), {})
                for item_id, count in bot.stored.items():
                    chest[item_id] = chest.get(item_id, 0) + count
                bot.stored.clear()
                break


# ── Direction helpers ────────────────────────────────────────────────────────

def _facing_dir(facing):
    return {"right": (1, 0), "left": (-1, 0), "up": (0, -1), "down": (0, 1)}.get(facing, (1, 0))

def _opposite_dir(facing):
    return {"right": (-1, 0), "left": (1, 0), "up": (0, 1), "down": (0, -1)}.get(facing, (-1, 0))

def _rotate_facing(facing):
    return {"right": "down", "down": "left", "left": "up", "up": "right"}.get(facing, "right")

def _input_wire_tiles(bx, by, facing):
    out_dx, out_dy = _facing_dir(facing)
    return [(bx + dx, by + dy) for dx, dy in _DIRS if (dx, dy) != (out_dx, out_dy)]

def _rs_inputs(bx, by, facing):
    dx, dy = _facing_dir(facing)
    return (bx + dy, by - dx), (bx - dy, by + dx)

def _bfs_from(start, powered, world):
    if world.get_wire(*start) != 1 or start in powered:
        return
    queue = deque([start])
    powered.add(start)
    while queue:
        bx, by = queue.popleft()
        for dx, dy in _DIRS:
            nx, ny = bx + dx, by + dy
            if (nx, ny) not in powered and world.get_wire(nx, ny) == 1:
                powered.add((nx, ny))
                queue.append((nx, ny))
