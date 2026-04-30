from collections import deque

from blocks import (
    HOPPER_BLOCK, PIPE_OUTPUT_BLOCK, PIPE_FILTER_BLOCK, PIPE_SORTER_BLOCK,
    PIPE_DEVICE_BLOCKS, CHEST_BLOCK, FACTORY_BLOCK,
)

PIPE_STEP_INTERVAL = 0.5   # seconds between routing ticks

# Tiles advanced per tick per pipe tier (stored in _pipe_chunks as 1/2/3)
PIPE_TIER_SPEED = {1: 1.0, 2: 3.0, 3: 8.0}

# Maps item_id to the tier value written to _pipe_chunks
PIPE_ITEM_TIER = {"pipe": 1, "pipe_iron": 2, "pipe_crystal": 3}
# Reverse: tier → item returned when pipe tile is mined
PIPE_TIER_ITEM = {1: "pipe", 2: "pipe_iron", 3: "pipe_crystal"}

_DIRS = [(0, -1), (0, 1), (-1, 0), (1, 0)]
_DIR_NAME = {(0, -1): "up", (0, 1): "down", (-1, 0): "left", (1, 0): "right"}
_NAME_DIR = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}

_tick_accum = 0.0


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def pipe_tick(world, dt):
    global _tick_accum
    _tick_accum += dt
    if _tick_accum < PIPE_STEP_INTERVAL:
        return
    _tick_accum -= PIPE_STEP_INTERVAL
    _run_pipe_pass(world)


def register_hopper(world, bx, by):
    world.pipe_state[(bx, by)] = {"pull_rate": 1, "enabled": True}


def register_pipe_output(world, bx, by, facing="down"):
    world.pipe_state[(bx, by)] = {"facing": facing, "enabled": True}


def register_pipe_filter(world, bx, by):
    world.pipe_state[(bx, by)] = {"allowed": []}


def register_pipe_sorter(world, bx, by):
    world.pipe_state[(bx, by)] = {"routes": {}}


# ---------------------------------------------------------------------------
# Core routing pass
# ---------------------------------------------------------------------------

def _run_pipe_pass(world):
    _hopper_pull(world)           # pull items from source into hopper buffer
    _launch_from_hoppers(world)   # move items from hopper buffer into transit
    _advance_transit(world)       # move in-transit items along their paths
    _output_deposit(world)        # flush any stranded items at output blocks


# ---------------------------------------------------------------------------
# Phase 1: Hoppers pull from source containers into their buffer
# ---------------------------------------------------------------------------

def _hopper_pull(world):
    for (bx, by), cfg in list(world.pipe_state.items()):
        if world.get_block(bx, by) != HOPPER_BLOCK:
            continue
        if _wire_disabled(world, bx, by):
            continue
        source = _get_container(world, bx, by - 1)
        if not source:
            continue
        pull_rate = cfg.get("pull_rate", 1)
        buf = world.pipe_buffers.setdefault((bx, by), {})
        pulled = 0
        for item_id in list(source.keys()):
            if pulled >= pull_rate:
                break
            if source.get(item_id, 0) > 0:
                source[item_id] -= 1
                if source[item_id] <= 0:
                    del source[item_id]
                buf[item_id] = buf.get(item_id, 0) + 1
                pulled += 1


# ---------------------------------------------------------------------------
# Phase 2: Launch buffered hopper items into transit
# ---------------------------------------------------------------------------

def _launch_from_hoppers(world):
    for (bx, by), cfg in list(world.pipe_state.items()):
        if world.get_block(bx, by) != HOPPER_BLOCK:
            continue
        buf = world.pipe_buffers.get((bx, by))
        if not buf:
            continue
        for item_id in list(buf.keys()):
            if buf.get(item_id, 0) <= 0:
                continue
            path = _bfs_full_path(world, bx, by, item_id)
            if path is None:
                continue  # no route yet; item stays buffered
            buf[item_id] -= 1
            if buf[item_id] <= 0:
                del buf[item_id]
            world.pipe_in_transit.append({
                "item_id": item_id,
                "count":   1,
                "path":    path,
                "progress": 0.0,
            })


# ---------------------------------------------------------------------------
# Phase 3: Advance items along their paths
# ---------------------------------------------------------------------------

def _advance_transit(world):
    still_moving = []

    for packet in world.pipe_in_transit:
        path     = packet["path"]
        progress = packet["progress"]
        path_len = len(path)

        idx = min(int(progress), path_len - 1)
        cur_bx, cur_by = path[idx]

        # Determine speed from the current tile's tier
        tier = world.get_pipe(cur_bx, cur_by)
        if tier > 0:
            speed = PIPE_TIER_SPEED.get(tier, 1.0)
        elif world.get_block(cur_bx, cur_by) in PIPE_DEVICE_BLOCKS:
            speed = PIPE_TIER_SPEED[2]   # device nodes don't slow items
        else:
            # Pipe tile was removed; strand item at last known position
            _strand(world, packet, cur_bx, cur_by)
            continue

        new_progress = progress + speed
        new_idx      = min(int(new_progress), path_len - 1)

        # Validate every tile we're jumping through this tick
        stranded = False
        for step in range(idx + 1, new_idx + 1):
            sbx, sby = path[step]
            block = world.get_block(sbx, sby)

            if block == PIPE_FILTER_BLOCK:
                f_cfg    = world.pipe_state.get((sbx, sby), {})
                allowed  = f_cfg.get("allowed", [])
                if allowed and packet["item_id"] not in allowed:
                    prev = path[step - 1]
                    _strand(world, packet, *prev)
                    stranded = True
                    break

            if world.get_pipe(sbx, sby) == 0 and block not in PIPE_DEVICE_BLOCKS:
                prev = path[step - 1]
                _strand(world, packet, *prev)
                stranded = True
                break

        if stranded:
            continue

        packet["progress"] = new_progress

        if new_progress >= path_len - 1:
            # Arrived at the output block
            out_bx, out_by = path[-1]
            if world.get_block(out_bx, out_by) == PIPE_OUTPUT_BLOCK:
                out_cfg = world.pipe_state.get((out_bx, out_by), {})
                if not _wire_disabled(world, out_bx, out_by):
                    facing = out_cfg.get("facing", "down")
                    ddx, ddy = _NAME_DIR.get(facing, (0, 1))
                    tx, ty = out_bx + ddx, out_by + ddy
                    if not _container_full(world, tx, ty):
                        target = _get_container(world, tx, ty)
                        if target is not None:
                            target[packet["item_id"]] = (
                                target.get(packet["item_id"], 0) + packet["count"]
                            )
                            continue
            # Output unavailable or full — buffer at the output block for retry
            _strand(world, packet, out_bx, out_by)
        else:
            still_moving.append(packet)

    world.pipe_in_transit = still_moving


def _strand(world, packet, bx, by):
    """Drop a transit packet into pipe_buffers at (bx,by) for re-routing."""
    buf = world.pipe_buffers.setdefault((bx, by), {})
    buf[packet["item_id"]] = buf.get(packet["item_id"], 0) + packet["count"]


# ---------------------------------------------------------------------------
# Phase 4: Retry any stranded items sitting at output blocks
# ---------------------------------------------------------------------------

def _output_deposit(world):
    for (bx, by), cfg in list(world.pipe_state.items()):
        if world.get_block(bx, by) != PIPE_OUTPUT_BLOCK:
            continue
        if _wire_disabled(world, bx, by):
            continue
        buf = world.pipe_buffers.get((bx, by), {})
        if not buf:
            continue
        facing = cfg.get("facing", "down")
        ddx, ddy = _NAME_DIR.get(facing, (0, 1))
        tx, ty = bx + ddx, by + ddy
        if _container_full(world, tx, ty):
            continue
        target = _get_container(world, tx, ty)
        if target is None:
            continue
        for item_id in list(buf.keys()):
            count = buf.pop(item_id, 0)
            if count > 0:
                target[item_id] = target.get(item_id, 0) + count


# ---------------------------------------------------------------------------
# BFS — returns the FULL path from first pipe tile after src to the sink
# ---------------------------------------------------------------------------

def _bfs_full_path(world, src_bx, src_by, item_id):
    """
    Return a list of (bx,by) positions from the immediate neighbor of
    (src_bx, src_by) to the nearest reachable PIPE_OUTPUT_BLOCK sink.
    Returns None if no path exists.
    """
    queue   = deque()
    visited = {(src_bx, src_by)}
    parent  = {}

    for dx, dy in _DIRS:
        nx, ny = src_bx + dx, src_by + dy
        if (nx, ny) not in visited and _is_traversable(world, nx, ny, item_id, src_bx, src_by):
            queue.append((nx, ny))
            visited.add((nx, ny))
            parent[(nx, ny)] = (src_bx, src_by)

    while queue:
        bx, by = queue.popleft()
        if _is_sink(world, bx, by):
            path = []
            pos  = (bx, by)
            while pos != (src_bx, src_by):
                path.append(pos)
                pos = parent[pos]
            path.reverse()
            return path

        for dx, dy in _DIRS:
            nx, ny = bx + dx, by + dy
            if (nx, ny) not in visited and _is_traversable(world, nx, ny, item_id, bx, by):
                queue.append((nx, ny))
                visited.add((nx, ny))
                parent[(nx, ny)] = (bx, by)

    return None


# ---------------------------------------------------------------------------
# Traversal / sink helpers
# ---------------------------------------------------------------------------

def _is_traversable(world, bx, by, item_id, from_bx, from_by):
    if not _is_pipe_node(world, bx, by):
        return False
    block = world.get_block(bx, by)
    if block == PIPE_FILTER_BLOCK:
        cfg     = world.pipe_state.get((bx, by), {})
        allowed = cfg.get("allowed", [])
        if allowed and item_id not in allowed:
            return False
    if world.get_block(from_bx, from_by) == PIPE_SORTER_BLOCK:
        cfg    = world.pipe_state.get((from_bx, from_by), {})
        routes = cfg.get("routes", {})
        if item_id in routes:
            required = routes[item_id]
            dx, dy   = bx - from_bx, by - from_by
            if _DIR_NAME.get((dx, dy)) != required:
                return False
    return True


def _is_sink(world, bx, by):
    return (world.get_block(bx, by) == PIPE_OUTPUT_BLOCK
            and not _wire_disabled(world, bx, by))


def _is_pipe_node(world, bx, by):
    return world.get_pipe(bx, by) > 0 or world.get_block(bx, by) in PIPE_DEVICE_BLOCKS


# ---------------------------------------------------------------------------
# Container helpers
# ---------------------------------------------------------------------------

def _container_full(world, bx, by):
    """Return True if the container at (bx,by) is at or over its cap."""
    if world.get_block(bx, by) == FACTORY_BLOCK:
        state = world.factory_data.get((bx, by))
        if state is None:
            return False
        cap = state.get("inv_cap", 64)
        inv = state.get("inventory", {})
        return sum(inv.values()) >= cap
    return False


def _get_container(world, bx, by):
    block = world.get_block(bx, by)
    if block == CHEST_BLOCK:
        return world.chest_data.setdefault((bx, by), {})
    if block == FACTORY_BLOCK:
        state = world.factory_data.get((bx, by))
        if state is not None:
            return state.setdefault("inventory", {})
        return None
    bs = _block_size(world)
    for auto in world.automations:
        if int(auto.x) // bs == bx and int(auto.y) // bs == by:
            return auto.stored
    for fb in world.farm_bots:
        if int(fb.x) // bs == bx and int(fb.y) // bs == by:
            return fb.stored
    return None


def _block_size(world):
    try:
        from constants import BLOCK_SIZE
        return BLOCK_SIZE
    except ImportError:
        return 32


# ---------------------------------------------------------------------------
# Wire enable/disable (same semantics as automations)
# ---------------------------------------------------------------------------

def _wire_disabled(world, bx, by):
    has_wire = any(world.get_wire(bx + dx, by + dy) == 1 for dx, dy in _DIRS)
    if not has_wire:
        return False
    return not any((bx + dx, by + dy) in world.powered_wires for dx, dy in _DIRS)
