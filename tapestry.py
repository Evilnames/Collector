import hashlib
from dataclasses import dataclass


@dataclass
class Tapestry:
    uid: str
    thread: str            # item id of thread/dye used
    height: int            # 1–4 blocks tall
    width: int             # 1–4 blocks wide
    grid: list             # list[list[bool]] — height*8 rows × width*16 cols; True = thread present
    color: tuple           # base thread RGB as (r,g,b), already pigment-tinted if dyed
    template: str          # "custom" or template name
    seed: int
    # ── Dye Bath fields (all optional; default to undyed) ─────────────────
    pigment_key: str = ""      # key into PIGMENT_TYPES, "" if undyed
    purity: float = 0.0        # 0–1, from the pigment used
    opacity: float = 0.0       # 0–1, blend weight applied to thread color
    stability: float = 0.0     # 0–1, lightfastness (used for value/aging later)
    ink_key: str = ""          # pigment key used as outline ink, "" if none
    ink_color: tuple = (0, 0, 0)
    ink_grid: list = None      # same shape as grid; True = outline cell

    def to_dict(self):
        return {
            "uid": self.uid,
            "thread": self.thread,
            "height": self.height,
            "width": self.width,
            "grid": self.grid,
            "color": list(self.color),
            "template": self.template,
            "seed": self.seed,
            "pigment_key": self.pigment_key,
            "purity": self.purity,
            "opacity": self.opacity,
            "stability": self.stability,
            "ink_key": self.ink_key,
            "ink_color": list(self.ink_color),
            "ink_grid": self.ink_grid,
        }

    @classmethod
    def from_dict(cls, d):
        ink_color = d.get("ink_color", [0, 0, 0])
        return cls(
            uid=d["uid"],
            thread=d["thread"],
            height=d["height"],
            width=d.get("width", 1),
            grid=d["grid"],
            color=tuple(d["color"]),
            template=d["template"],
            seed=d["seed"],
            pigment_key=d.get("pigment_key", ""),
            purity=d.get("purity", 0.0),
            opacity=d.get("opacity", 0.0),
            stability=d.get("stability", 0.0),
            ink_key=d.get("ink_key", ""),
            ink_color=tuple(ink_color) if ink_color else (0, 0, 0),
            ink_grid=d.get("ink_grid"),
        )

    def has_dye(self) -> bool:
        return bool(self.pigment_key)

    def has_ink(self) -> bool:
        return bool(self.ink_key) and self.ink_grid is not None

    def quality(self) -> float:
        """Combined visual quality (0–1) based on pigment attributes."""
        if not self.pigment_key:
            return 0.0
        return round(self.purity * 0.45 + self.opacity * 0.30 + self.stability * 0.25, 3)


THREAD_COLORS = {
    "wool":                (235, 235, 235),
    "cotton_fiber":        (240, 242, 235),
    "dye_extract_golden":  (215, 175,  40),
    "dye_extract_crimson": (185,  35,  45),
    "dye_extract_rose":    (220, 110, 155),
    "dye_extract_cobalt":  ( 55,  90, 185),
    "dye_extract_violet":  (130,  65, 195),
    "dye_extract_verdant": ( 60, 148,  75),
    "dye_extract_amber":   (200, 115,  35),
    "dye_extract_ivory":   (245, 240, 220),
}

WEAVABLE_THREADS = {
    "wool":                "Wool",
    "cotton_fiber":        "Cotton",
    "dye_extract_golden":  "Golden Thread",
    "dye_extract_crimson": "Crimson Thread",
    "dye_extract_rose":    "Rose Thread",
    "dye_extract_cobalt":  "Cobalt Thread",
    "dye_extract_violet":  "Violet Thread",
    "dye_extract_verdant": "Verdant Thread",
    "dye_extract_amber":   "Amber Thread",
    "dye_extract_ivory":   "Ivory Thread",
}


TAPESTRY_COLS_PER_BLOCK = 16
TAPESTRY_ROWS_PER_BLOCK = 8


def _full(h, w=1):
    cols = w * TAPESTRY_COLS_PER_BLOCK
    return [[True] * cols for _ in range(h * TAPESTRY_ROWS_PER_BLOCK)]

def _empty(h, w=1):
    cols = w * TAPESTRY_COLS_PER_BLOCK
    return [[False] * cols for _ in range(h * TAPESTRY_ROWS_PER_BLOCK)]


def _make_stripes_grid(height, width=1):
    cols = width * TAPESTRY_COLS_PER_BLOCK
    rows = height * TAPESTRY_ROWS_PER_BLOCK
    g = _empty(height, width)
    for r in range(rows):
        for c in range(cols):
            if (c // 2) % 2 == 0:
                g[r][c] = True
    return g

def _make_horizontal_stripes_grid(height, width=1):
    cols = width * TAPESTRY_COLS_PER_BLOCK
    rows = height * TAPESTRY_ROWS_PER_BLOCK
    g = _empty(height, width)
    for r in range(rows):
        if (r // 2) % 2 == 0:
            g[r] = [True] * cols
    return g

def _make_checkerboard_grid(height, width=1):
    cols = width * TAPESTRY_COLS_PER_BLOCK
    rows = height * TAPESTRY_ROWS_PER_BLOCK
    g = _empty(height, width)
    for r in range(rows):
        for c in range(cols):
            if ((r // 2) + (c // 2)) % 2 == 0:
                g[r][c] = True
    return g

def _make_diamond_grid(height, width=1):
    cols = width * TAPESTRY_COLS_PER_BLOCK
    rows = height * TAPESTRY_ROWS_PER_BLOCK
    g = _empty(height, width)
    cx, cy = (cols - 1) / 2, (rows - 1) / 2
    for r in range(rows):
        for c in range(cols):
            if abs(c - cx) + abs(r - cy) <= min(cols // 2 - 1, rows * 0.45):
                g[r][c] = True
    return g

def _make_border_grid(height, width=1):
    cols = width * TAPESTRY_COLS_PER_BLOCK
    rows = height * TAPESTRY_ROWS_PER_BLOCK
    g = _empty(height, width)
    for r in range(rows):
        for c in range(cols):
            if r < 3 or r >= rows - 3 or c < 3 or c >= cols - 3:
                g[r][c] = True
    return g

def _make_zigzag_grid(height, width=1):
    cols = width * TAPESTRY_COLS_PER_BLOCK
    rows = height * TAPESTRY_ROWS_PER_BLOCK
    g = _empty(height, width)
    period = 8
    for r in range(rows):
        phase = r % (period * 2)
        if phase < period:
            c = phase
        else:
            c = period * 2 - 1 - phase
        # Repeat the zigzag across the width
        for x_offset in range(0, cols, period * 2):
            for dc in range(3):
                col_pos = x_offset + c + dc
                if 0 <= col_pos < cols:
                    g[r][col_pos] = True
    return g

def _make_cross_grid(height, width=1):
    cols = width * TAPESTRY_COLS_PER_BLOCK
    rows = height * TAPESTRY_ROWS_PER_BLOCK
    g = _empty(height, width)
    mid_c = cols // 2 - 1
    mid_r = rows // 2 - 1
    for r in range(rows):
        g[r][mid_c] = g[r][mid_c + 1] = True
    for c in range(cols):
        g[mid_r][c] = g[mid_r + 1][c] = True
    return g

def _make_tree_of_life_grid(height, width=1):
    cols = width * TAPESTRY_COLS_PER_BLOCK
    rows = height * TAPESTRY_ROWS_PER_BLOCK
    g = _empty(height, width)
    trunk_start = max(rows * 2 // 3, rows - 8)
    mid = cols // 2 - 1
    for r in range(trunk_start, rows):
        g[r][mid] = g[r][mid + 1] = True
    for r in range(trunk_start):
        frac = 1 - r / max(1, trunk_start - 1)
        spread = int(frac * (cols // 3))
        for dc in range(-spread, spread + 2):
            if 0 <= mid + dc < cols:
                g[r][mid + dc] = True
        if r % 4 == 0:
            for dc in range(-spread - 2, spread + 4):
                if 0 <= mid + dc < cols:
                    g[r][mid + dc] = True
    return g

def _make_sun_grid(height, width=1):
    import math
    cols = width * TAPESTRY_COLS_PER_BLOCK
    rows = height * TAPESTRY_ROWS_PER_BLOCK
    g = _empty(height, width)
    cx, cy = (cols - 1) / 2, (rows - 1) / 2
    rad = min(cols * 0.3, rows * 0.3)
    ray_len = min(cols * 0.2, rows * 0.2)
    for r in range(rows):
        for c in range(cols):
            dist = math.sqrt((c - cx) ** 2 + (r - cy) ** 2)
            if dist <= rad:
                g[r][c] = True
            elif dist <= rad + ray_len:
                angle = math.atan2(r - cy, c - cx)
                for ray_angle in [i * math.pi / 4 for i in range(8)]:
                    if abs(math.cos(angle - ray_angle)) > 0.85:
                        g[r][c] = True
                        break
    return g

def _make_moon_grid(height, width=1):
    import math
    cols = width * TAPESTRY_COLS_PER_BLOCK
    rows = height * TAPESTRY_ROWS_PER_BLOCK
    g = _empty(height, width)
    cx, cy = (cols - 1) / 2, (rows - 1) / 2
    rad = min(cols * 0.36, rows * 0.36)
    for r in range(rows):
        for c in range(cols):
            if math.sqrt((c - cx) ** 2 + (r - cy) ** 2) <= rad:
                g[r][c] = True
    cut_cx = cx + rad * 0.45
    for r in range(rows):
        for c in range(cols):
            if math.sqrt((c - cut_cx) ** 2 + (r - cy) ** 2) < rad * 0.85:
                g[r][c] = False
    return g

def _make_fish_grid(height, width=1):
    import math
    cols = width * TAPESTRY_COLS_PER_BLOCK
    rows = height * TAPESTRY_ROWS_PER_BLOCK
    g = _empty(height, width)
    cx, cy = cols * 0.55, (rows - 1) / 2
    for r in range(rows):
        for c in range(cols):
            dx = (c - cx) / (cols * 0.35)
            dy = (r - cy) / max(2, rows * 0.18)
            if dx * dx + dy * dy <= 1.0 and c < cx + 2:
                g[r][c] = True
    tail_x = int(cx - cols * 0.35)
    for r in range(rows):
        spread = abs(r - cy) * 0.8
        if 0 <= tail_x < cols and spread < 4:
            for c in range(max(0, tail_x - int(spread)), min(cols, tail_x + 1)):
                g[r][c] = True
    return g

def _make_herringbone_grid(height, width=1):
    cols = width * TAPESTRY_COLS_PER_BLOCK
    rows = height * TAPESTRY_ROWS_PER_BLOCK
    g = _empty(height, width)
    for r in range(rows):
        for c in range(cols):
            zone = (r + c) // 4
            if zone % 2 == 0:
                if (c - r) % 4 < 2:
                    g[r][c] = True
            else:
                if (c + r) % 4 < 2:
                    g[r][c] = True
    return g

def _make_wave_grid(height, width=1):
    import math
    cols = width * TAPESTRY_COLS_PER_BLOCK
    rows = height * TAPESTRY_ROWS_PER_BLOCK
    g = _empty(height, width)
    cx = (cols - 1) / 2
    for r in range(rows):
        wave_c = cx + (cols * 0.3) * math.sin(r / max(1, rows - 1) * math.pi * 4)
        for c in range(cols):
            if abs(c - wave_c) < 2:
                g[r][c] = True
    return g

def _make_maze_grid(height, width=1):
    cols = width * TAPESTRY_COLS_PER_BLOCK
    rows = height * TAPESTRY_ROWS_PER_BLOCK
    g = _empty(height, width)
    for r in range(rows):
        for c in range(cols):
            cell_r, cell_c = r // 4, c // 4
            local_r, local_c = r % 4, c % 4
            is_wall = (local_r == 0 or local_c == 0)
            if is_wall:
                if local_r == 0 and (cell_r + cell_c) % 2 == 0 and local_c not in (0, 3):
                    is_wall = False
                if local_c == 0 and (cell_r + cell_c) % 2 == 1 and local_r not in (0, 3):
                    is_wall = False
            g[r][c] = is_wall
    g[0] = [True] * cols
    g[-1] = [True] * cols
    return g

def _make_spiral_grid(height, width=1):
    import math
    cols = width * TAPESTRY_COLS_PER_BLOCK
    rows = height * TAPESTRY_ROWS_PER_BLOCK
    g = _empty(height, width)
    cx, cy = (cols - 1) / 2, (rows - 1) / 2
    scale_y = rows / 16.0
    max_r = cols / 2.0
    for r in range(rows):
        for c in range(cols):
            dx = c - cx
            dy = (r - cy) / scale_y
            dist = math.sqrt(dx * dx + dy * dy)
            angle = math.atan2(dy, dx)
            if dist > 0.5:
                target_dist = (angle % (2 * math.pi)) / (math.pi * 2) * max_r
                if abs(dist - target_dist) < 1.0 or abs(dist - target_dist - max_r) < 1.0:
                    g[r][c] = True
    return g

def _make_diamonds_pattern_grid(height, width=1):
    cols = width * TAPESTRY_COLS_PER_BLOCK
    rows = height * TAPESTRY_ROWS_PER_BLOCK
    g = _empty(height, width)
    for r in range(rows):
        for c in range(cols):
            mr = r % 8
            mc = c % 8
            if abs(mr - 4) + abs(mc - 4) <= 3:
                g[r][c] = True
    return g

def _make_medallion_grid(height, width=1):
    import math
    cols = width * TAPESTRY_COLS_PER_BLOCK
    rows = height * TAPESTRY_ROWS_PER_BLOCK
    g = _full(height, width)
    cx, cy = (cols - 1) / 2, (rows - 1) / 2
    rad = min(cols * 0.32, rows * 0.32)
    for r in range(rows):
        for c in range(cols):
            if math.sqrt((c - cx) ** 2 + (r - cy) ** 2) <= rad:
                g[r][c] = False
    for r in range(rows):
        for c in range(cols):
            if r < 3 and c < 3:
                g[r][c] = True
            if r < 3 and c >= cols - 3:
                g[r][c] = True
            if r >= rows - 3 and c < 3:
                g[r][c] = True
            if r >= rows - 3 and c >= cols - 3:
                g[r][c] = True
    return g

def _make_hunting_scene_grid(height, width=1):
    cols = width * TAPESTRY_COLS_PER_BLOCK
    rows = height * TAPESTRY_ROWS_PER_BLOCK
    g = _empty(height, width)
    ground = rows - 4
    for c in range(cols):
        for dr in range(4):
            g[ground + dr][c] = True
    deer_c = cols // 2
    for r in range(max(0, ground - 8), ground):
        for dc in range(-3, 4):
            if 0 <= deer_c + dc < cols:
                g[r][deer_c + dc] = True
    for r in range(max(0, ground - 12), ground - 8):
        for dc in range(1, 4):
            if 0 <= deer_c + dc < cols:
                g[r][deer_c + dc] = True
    if ground - 13 >= 0:
        for dc in range(1, 6):
            if 0 <= deer_c + dc < cols:
                g[ground - 13][deer_c + dc] = True
        if ground - 14 >= 0:
            g[ground - 14][deer_c + 2] = g[ground - 14][deer_c + 4] = True
    tree_c = max(1, cols // 8)
    for r in range(ground - 10, ground):
        g[r][tree_c] = g[r][tree_c + 1] = True
    for r in range(max(0, ground - 16), ground - 10):
        frac = (r - (ground - 16)) / 6
        w_spread = max(1, int(5 - frac * 3))
        for dc in range(-w_spread, w_spread + 1):
            if 0 <= tree_c + dc < cols:
                g[r][tree_c + dc] = True
    return g


TEMPLATES = {
    "Stripes":         _make_stripes_grid,
    "H. Stripes":      _make_horizontal_stripes_grid,
    "Checkerboard":    _make_checkerboard_grid,
    "Diamond":         _make_diamond_grid,
    "Border":          _make_border_grid,
    "Zigzag":          _make_zigzag_grid,
    "Cross":           _make_cross_grid,
    "Tree of Life":    _make_tree_of_life_grid,
    "Sun":             _make_sun_grid,
    "Moon":            _make_moon_grid,
    "Fish":            _make_fish_grid,
    "Herringbone":     _make_herringbone_grid,
    "Wave":            _make_wave_grid,
    "Maze":            _make_maze_grid,
    "Spiral":          _make_spiral_grid,
    "Diamonds":        _make_diamonds_pattern_grid,
    "Medallion":       _make_medallion_grid,
    "Hunting Scene":   _make_hunting_scene_grid,
}

BASE_TEMPLATES = list(TEMPLATES.keys())


def make_outline_grid(grid):
    """Return a binary grid the same shape as `grid`. True for filled cells
    that touch the empty void on any 4-neighbour side (or the boundary)."""
    if not grid or not grid[0]:
        return None
    rows = len(grid)
    cols = len(grid[0])
    out = [[False] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if not grid[r][c]:
                continue
            on_edge = (r == 0 or r == rows - 1 or c == 0 or c == cols - 1)
            if on_edge:
                out[r][c] = True
                continue
            if (not grid[r - 1][c]) or (not grid[r + 1][c]) \
               or (not grid[r][c - 1]) or (not grid[r][c + 1]):
                out[r][c] = True
    return out


def _lerp_color(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


class TapestryGenerator:
    def __init__(self, world_seed: int):
        self._world_seed = world_seed
        self._counter    = 0

    def generate(self, thread: str, height: int, width: int, grid: list,
                 template: str, pigment=None, ink=None) -> Tapestry:
        self._counter += 1
        seed = (self._world_seed * 31 + self._counter * 6271) & 0xFFFFFFFF
        uid  = hashlib.md5(f"tapestry_{seed}_{self._counter}".encode()).hexdigest()[:12]
        base_color = THREAD_COLORS.get(thread, (220, 210, 190))
        import random
        rng = random.Random(seed)

        # ── Apply dye bath ────────────────────────────────────────────────
        pigment_key = ""
        purity = opacity = stability = 0.0
        if pigment is not None:
            pigment_key = pigment.pigment_key
            purity      = pigment.purity
            opacity     = pigment.opacity
            stability   = pigment.stability
            pig_rgb     = tuple(pigment.color_rgb)
            # Opacity acts as blend weight: opaque pigments overwrite thread color,
            # transparent ones (e.g. lakes) tint subtly.
            blend = 0.30 + 0.65 * opacity
            base_color = _lerp_color(base_color, pig_rgb, blend)

        # Purity inversely controls colour jitter — pure pigments give cleaner colour.
        amp = int(round(8 - purity * 6)) if pigment_key else 6
        amp = max(1, amp)
        jitter = lambda c: max(0, min(255, c + rng.randint(-amp, amp)))
        color = tuple(jitter(c) for c in base_color)

        # ── Apply ink outline ─────────────────────────────────────────────
        ink_key   = ""
        ink_color = (0, 0, 0)
        ink_grid  = None
        if ink is not None:
            ink_key   = ink.pigment_key
            ir, ig, ib = ink.color_rgb
            # Inks always render dark — clamp brightness regardless of source colour.
            ink_color = (max(0, ir - 25), max(0, ig - 25), max(0, ib - 25))
            ink_grid  = make_outline_grid(grid)

        return Tapestry(
            uid=uid,
            thread=thread,
            height=height,
            width=width,
            grid=grid,
            color=color,
            template=template,
            seed=seed,
            pigment_key=pigment_key,
            purity=round(purity, 3),
            opacity=round(opacity, 3),
            stability=round(stability, 3),
            ink_key=ink_key,
            ink_color=ink_color,
            ink_grid=ink_grid,
        )
