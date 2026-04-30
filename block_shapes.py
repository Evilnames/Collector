"""
block_shapes.py — Block placement brush system.

Shapes are a rendering + metadata layer: the block ID never changes,
only the polygon of material that is visible at each tile.

SHAPE_VARIANTS is the ordered list the player cycles through with Tab.
Each entry: (shape_type: str, rotation: int, label: str)

Shapes and rotations:
  full        0               full block (default)
  slab        0=bottom        lower half
              1=top           upper half
              2=left          left half
              3=right         right half
  slope       0=SW rise       triangle: lower-left (ramp going up-right)
              1=SE rise       triangle: lower-right (ramp going up-left)
              2=NE upper      triangle: upper-right
              3=NW upper      triangle: upper-left
  arch        0=open-down     arch opening faces down  (top lintel + side piers)
              1=open-right    arch opening faces right
              2=open-up       arch opening faces up
              3=open-left     arch opening faces left
  corner_out  0=cut NE        convex L-corner, cut in top-right quadrant
              1=cut SE        cut in bottom-right
              2=cut SW        cut in bottom-left
              3=cut NW        cut in top-left
  corner_in   0=fill NW       concave: fills only top-left quadrant
              1=fill NE       fills only top-right quadrant
              2=fill SE       fills only bottom-right quadrant
              3=fill SW       fills only bottom-left quadrant
"""

import pygame

# ── Variant list (Tab cycles through this) ──────────────────────────────────

SHAPE_VARIANTS = [
    # shape_type,   rotation, label
    ("full",        0,  "Full Block"),
    ("slab",        0,  "Slab — Bottom"),
    ("slab",        1,  "Slab — Top"),
    ("slab",        2,  "Slab — Left"),
    ("slab",        3,  "Slab — Right"),
    ("slope",       0,  "Slope ↗"),
    ("slope",       1,  "Slope ↖"),
    ("slope",       2,  "Slope ↘ (inv)"),
    ("slope",       3,  "Slope ↙ (inv)"),
    ("arch",        0,  "Arch — opens down"),
    ("arch",        1,  "Arch — opens right"),
    ("arch",        2,  "Arch — opens up"),
    ("arch",        3,  "Arch — opens left"),
    ("corner_out",  0,  "Corner — cut NE"),
    ("corner_out",  1,  "Corner — cut SE"),
    ("corner_out",  2,  "Corner — cut SW"),
    ("corner_out",  3,  "Corner — cut NW"),
    ("corner_in",   0,  "Inner Corner NW"),
    ("corner_in",   1,  "Inner Corner NE"),
    ("corner_in",   2,  "Inner Corner SE"),
    ("corner_in",   3,  "Inner Corner SW"),
]

# ── Polygon definitions (normalised 0–1, scaled to BS at build time) ─────────
# Arch shapes are handled separately (carve ellipse from full rect).

def _poly(pts, bs):
    """Scale normalised [(x,y)...] points to pixel space."""
    return [(round(x * bs), round(y * bs)) for x, y in pts]


_NORM_POLYS = {
    ("full",       0): [(0,0),(1,0),(1,1),(0,1)],
    # slabs
    ("slab",       0): [(0,.5),(1,.5),(1,1),(0,1)],
    ("slab",       1): [(0,0),(1,0),(1,.5),(0,.5)],
    ("slab",       2): [(0,0),(.5,0),(.5,1),(0,1)],
    ("slab",       3): [(.5,0),(1,0),(1,1),(.5,1)],
    # slopes (triangles)
    ("slope",      0): [(0,0),(0,1),(1,1)],          # lower-left tri  ↗ ramp
    ("slope",      1): [(1,0),(0,1),(1,1)],          # lower-right tri ↖ ramp
    ("slope",      2): [(0,0),(1,0),(1,1)],          # upper-right tri
    ("slope",      3): [(0,0),(1,0),(0,1)],          # upper-left tri
    # convex L-corners (3/4 block, one quadrant removed)
    ("corner_out", 0): [(0,0),(.5,0),(.5,.5),(1,.5),(1,1),(0,1)],   # cut NE
    ("corner_out", 1): [(0,0),(1,0),(1,.5),(.5,.5),(.5,1),(0,1)],   # cut SE
    ("corner_out", 2): [(.5,0),(1,0),(1,1),(0,1),(0,.5),(.5,.5)],   # cut SW
    ("corner_out", 3): [(0,0),(1,0),(1,1),(.5,1),(.5,.5),(0,.5)],   # cut NW
    # concave (inner) corners — single quadrant fill
    ("corner_in",  0): [(0,0),(.5,0),(.5,.5),(0,.5)],               # NW quadrant
    ("corner_in",  1): [(.5,0),(1,0),(1,.5),(.5,.5)],               # NE quadrant
    ("corner_in",  2): [(.5,.5),(1,.5),(1,1),(.5,1)],               # SE quadrant
    ("corner_in",  3): [(0,.5),(.5,.5),(.5,1),(0,1)],               # SW quadrant
}

# ── Mask surfaces ─────────────────────────────────────────────────────────────
# White-polygon-on-transparent; pre-built once at startup.
# Arch masks are computed separately using ellipse carving.

_MASKS: dict = {}   # (shape_type, rotation) → pygame.Surface (SRCALPHA)


def _build_arch_mask(rotation: int, bs: int) -> pygame.Surface:
    """
    Arch: full block with a semicircle void carved from one face.
    rotation 0=void at bottom, 1=right, 2=top, 3=left.
    """
    s = pygame.Surface((bs, bs), pygame.SRCALPHA)
    s.fill((255, 255, 255, 255))        # start fully solid
    # Arch void: ellipse half the block wide, quarter-block tall, hugging one edge
    void = pygame.Surface((bs, bs), pygame.SRCALPHA)
    void.fill((0, 0, 0, 0))
    ew = bs * 3 // 4    # ellipse width
    eh = bs // 2        # ellipse height (full diameter)
    ex = (bs - ew) // 2
    if rotation == 0:   # opening down — void at bottom
        pygame.draw.ellipse(void, (255, 255, 255, 255), (ex, bs - eh, ew, eh))
    elif rotation == 1: # opening right
        pygame.draw.ellipse(void, (255, 255, 255, 255), (bs - eh, ex, eh, ew))
    elif rotation == 2: # opening up
        pygame.draw.ellipse(void, (255, 255, 255, 255), (ex, 0, ew, eh))
    else:               # opening left
        pygame.draw.ellipse(void, (255, 255, 255, 255), (0, ex, eh, ew))
    # Carve: subtract void from solid using BLEND_RGBA_SUB
    s.blit(void, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
    return s


def build_shape_masks(block_size: int) -> None:
    """Call once after pygame.init() to pre-build all shape mask surfaces."""
    _MASKS.clear()
    for shape_type, rotation, _label in SHAPE_VARIANTS:
        key = (shape_type, rotation)
        if key in _MASKS:
            continue
        if shape_type == "arch":
            _MASKS[key] = _build_arch_mask(rotation, block_size)
        else:
            s = pygame.Surface((block_size, block_size), pygame.SRCALPHA)
            s.fill((0, 0, 0, 0))
            poly = _poly(_NORM_POLYS[key], block_size)
            pygame.draw.polygon(s, (255, 255, 255, 255), poly)
            _MASKS[key] = s


# ── Runtime blit ──────────────────────────────────────────────────────────────

def blit_shaped(
    screen: pygame.Surface,
    surf: pygame.Surface,
    sx: int,
    sy: int,
    shape_type: str,
    rotation: int,
) -> None:
    """
    Blit `surf` to `screen` at (sx, sy) clipped to the shape polygon.
    Falls through to a plain blit for full blocks (no overhead).
    """
    if shape_type == "full":
        screen.blit(surf, (sx, sy))
        return

    mask = _MASKS.get((shape_type, rotation))
    if mask is None:
        screen.blit(surf, (sx, sy))
        return

    bs = surf.get_width()
    shaped = pygame.Surface((bs, bs), pygame.SRCALPHA)
    # Copy block texture into alpha-capable surface
    shaped.blit(surf, (0, 0))
    # Multiply alpha channel by mask: pixels outside polygon become transparent
    shaped.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    screen.blit(shaped, (sx, sy))


# ── HUD preview drawing ───────────────────────────────────────────────────────

def draw_shape_preview(
    screen: pygame.Surface,
    shape_type: str,
    rotation: int,
    block_color: tuple,
    cx: int,
    cy: int,
    size: int,
    highlight: bool = False,
) -> None:
    """
    Draw a single shape thumbnail centred at (cx, cy) in a box of `size`×`size`.
    Used by the HUD brush indicator.
    """
    padding = max(2, size // 8)
    inner = size - padding * 2
    ox, oy = cx - size // 2, cy - size // 2

    # Background slot
    slot_col = (60, 65, 70) if not highlight else (100, 110, 120)
    border_col = (180, 190, 200) if highlight else (80, 88, 94)
    pygame.draw.rect(screen, slot_col, (ox, oy, size, size), border_radius=3)
    pygame.draw.rect(screen, border_col, (ox, oy, size, size), 1, border_radius=3)

    # Shape polygon or arch carved from rect
    ix, iy = ox + padding, oy + padding
    key = (shape_type, rotation)

    if shape_type == "arch":
        # Draw filled rect then carve ellipse
        pygame.draw.rect(screen, block_color, (ix, iy, inner, inner))
        ew = inner * 3 // 4
        eh = inner // 2
        ex = ix + (inner - ew) // 2
        void_col = slot_col
        if rotation == 0:
            pygame.draw.ellipse(screen, void_col, (ex, iy + inner - eh, ew, eh))
        elif rotation == 1:
            pygame.draw.ellipse(screen, void_col, (ix + inner - eh, iy + (inner - ew) // 2, eh, ew))
        elif rotation == 2:
            pygame.draw.ellipse(screen, void_col, (ex, iy, ew, eh))
        else:
            pygame.draw.ellipse(screen, void_col, (ix, iy + (inner - ew) // 2, eh, ew))
    elif key in _NORM_POLYS:
        pts = [(ix + round(x * inner), iy + round(y * inner)) for x, y in _NORM_POLYS[key]]
        if len(pts) >= 3:
            pygame.draw.polygon(screen, block_color, pts)
        # outline
        pygame.draw.polygon(screen, _lighter(block_color, 30), pts, 1)
    else:
        pygame.draw.rect(screen, block_color, (ix, iy, inner, inner))


def _lighter(color: tuple, amt: int = 25) -> tuple:
    return tuple(min(255, c + amt) for c in color)
