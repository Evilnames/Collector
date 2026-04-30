import math
import pygame
from blocks import (CORAL_FRAGMENT_BLOCK, CORAL_GROWING, CORAL_FULL,
                    KELP_BLOCK, SEASHELL_BLOCK, SEA_ANEMONE,
                    BIOLUME_DEEP_BLOCK, OCEAN_ROCK, OYSTER_BLOCK)
from constants import BLOCK_SIZE

BS = BLOCK_SIZE
_HALF = BS // 2


def _s(alpha=255):
    """Blank SRCALPHA surface one block large."""
    surf = pygame.Surface((BS, BS), pygame.SRCALPHA)
    surf.fill((0, 0, 0, 0))
    return surf


# ---------------------------------------------------------------------------
# draw_coral_fragment — small pink/orange nub on the sea floor
# ---------------------------------------------------------------------------

def draw_coral_fragment():
    surf = _s()
    # Sandy floor strip
    pygame.draw.rect(surf, (200, 185, 150), (0, BS - 6, BS, 6))
    # Small stubby nub centered, sitting on the floor
    cx = _HALF
    base_y = BS - 6
    pygame.draw.ellipse(surf, (225, 100, 140), (cx - 5, base_y - 10, 10, 11))
    pygame.draw.ellipse(surf, (240, 130, 165), (cx - 3, base_y - 14, 6, 7))
    # Tiny tip polyp
    pygame.draw.circle(surf, (255, 160, 190), (cx, base_y - 15), 3)
    pygame.draw.circle(surf, (255, 200, 215), (cx, base_y - 15), 2)
    return surf


# ---------------------------------------------------------------------------
# draw_coral_growing — branching mid-size coral (Y-shape)
# ---------------------------------------------------------------------------

def draw_coral_growing():
    surf = _s()
    pygame.draw.rect(surf, (200, 185, 150), (0, BS - 6, BS, 6))
    cx = _HALF
    base_y = BS - 6
    trunk_top = base_y - 16
    # Main trunk
    pygame.draw.line(surf, (210, 80, 120), (cx, base_y), (cx, trunk_top), 4)
    pygame.draw.line(surf, (230, 110, 145), (cx, base_y), (cx, trunk_top), 2)
    # Left branch
    lx, ly = cx - 9, trunk_top - 8
    pygame.draw.line(surf, (210, 80, 120), (cx, trunk_top), (lx, ly), 3)
    pygame.draw.circle(surf, (255, 150, 185), (lx, ly), 4)
    pygame.draw.circle(surf, (255, 190, 210), (lx, ly), 2)
    # Right branch
    rx, ry = cx + 9, trunk_top - 7
    pygame.draw.line(surf, (210, 80, 120), (cx, trunk_top), (rx, ry), 3)
    pygame.draw.circle(surf, (255, 150, 185), (rx, ry), 4)
    pygame.draw.circle(surf, (255, 190, 210), (rx, ry), 2)
    return surf


# ---------------------------------------------------------------------------
# draw_coral_full — large vivid branching coral with polyp dots
# ---------------------------------------------------------------------------

def draw_coral_full():
    surf = _s()
    pygame.draw.rect(surf, (200, 185, 150), (0, BS - 6, BS, 6))
    cx = _HALF
    base_y = BS - 6
    trunk_top = base_y - 12

    trunk_col  = (215, 65, 100)
    branch_col = (240, 90, 125)
    polyp_col  = (255, 170, 195)
    polyp_hi   = (255, 215, 225)

    # Trunk
    pygame.draw.line(surf, trunk_col, (cx, base_y), (cx, trunk_top), 5)
    pygame.draw.line(surf, branch_col, (cx, base_y), (cx, trunk_top), 3)

    # Three branch tiers: (dx, dy) offsets from trunk_top
    branches = [
        (cx - 11, trunk_top - 9),
        (cx + 11, trunk_top - 8),
        (cx - 5,  trunk_top - 17),
        (cx + 6,  trunk_top - 18),
        (cx,      trunk_top - 22),
    ]
    for bx2, by2 in branches:
        pygame.draw.line(surf, trunk_col, (cx, trunk_top), (bx2, by2), 3)
        pygame.draw.line(surf, branch_col, (cx, trunk_top), (bx2, by2), 2)

    # Polyp circles at every branch tip and mid-branch
    for bx2, by2 in branches:
        pygame.draw.circle(surf, polyp_col, (bx2, by2), 5)
        pygame.draw.circle(surf, polyp_hi,  (bx2, by2), 3)
        # Tiny satellite polyp
        pygame.draw.circle(surf, polyp_col, (bx2 - 3, by2 - 4), 2)

    return surf


# ---------------------------------------------------------------------------
# draw_kelp — tall dark-green stalk with wavy leaf blades
# ---------------------------------------------------------------------------

def draw_kelp():
    surf = _s()
    pygame.draw.rect(surf, (200, 185, 150), (0, BS - 6, BS, 6))
    cx = _HALF
    stalk_col  = (20, 100, 45)
    stalk_hi   = (35, 130, 60)
    blade_col  = (28, 115, 52)
    blade_edge = (18, 90, 38)

    # Central wavy stalk — draw as connected short segments with lateral drift
    pts = []
    for i in range(8):
        t = i / 7.0
        y = int((BS - 6) * (1.0 - t))
        x = cx + int(math.sin(t * math.pi * 2) * 3)
        pts.append((x, y))

    if len(pts) >= 2:
        pygame.draw.lines(surf, stalk_col, False, pts, 4)
        pygame.draw.lines(surf, stalk_hi,  False, pts, 2)

    # Leaf blades at every other stalk node
    for i, (sx2, sy2) in enumerate(pts):
        if i % 2 == 0 and i < len(pts) - 1:
            side = 1 if (i // 2) % 2 == 0 else -1
            lx0, ly0 = sx2, sy2
            lx1 = sx2 + side * 9
            ly1 = sy2 + 4
            lx2 = sx2 + side * 6
            ly2 = sy2 + 9
            pygame.draw.polygon(surf, blade_col, [(lx0, ly0), (lx1, ly1), (lx2, ly2)])
            pygame.draw.polygon(surf, blade_edge, [(lx0, ly0), (lx1, ly1), (lx2, ly2)], 1)

    return surf


# ---------------------------------------------------------------------------
# draw_sea_anemone — circular tentacle fan (bright orange/purple)
# ---------------------------------------------------------------------------

def draw_sea_anemone():
    surf = _s()
    pygame.draw.rect(surf, (200, 185, 150), (0, BS - 6, BS, 6))
    cx = _HALF
    base_y = BS - 6

    body_col     = (240, 110, 55)
    body_dark    = (200, 80, 35)
    tentacle_col = (255, 145, 80)
    tentacle_tip = (255, 200, 120)
    center_col   = (255, 70, 100)

    # Bulbous body base
    pygame.draw.ellipse(surf, body_col,  (cx - 8, base_y - 10, 16, 11))
    pygame.draw.ellipse(surf, body_dark, (cx - 8, base_y - 10, 16, 11), 1)

    # Radiating tentacles — 10 arms in a fan
    n_arms = 10
    for i in range(n_arms):
        angle = math.pi + (i / (n_arms - 1)) * math.pi   # lower half-circle
        length = 9 + (4 if i in (4, 5) else 0)           # center ones taller
        tip_x = int(cx + length * math.cos(angle))
        tip_y = int(base_y - 10 + length * math.sin(angle))
        pygame.draw.line(surf, tentacle_col, (cx, base_y - 6), (tip_x, tip_y), 2)
        pygame.draw.circle(surf, tentacle_tip, (tip_x, tip_y), 2)

    # Central disk
    pygame.draw.circle(surf, center_col, (cx, base_y - 5), 4)
    pygame.draw.circle(surf, (255, 130, 130), (cx, base_y - 5), 2)

    return surf


# ---------------------------------------------------------------------------
# draw_biolume_deep — dark dome with pulsing cyan inner glow
# ---------------------------------------------------------------------------

def draw_biolume_deep():
    surf = _s()
    pygame.draw.rect(surf, (55, 60, 70), (0, BS - 6, BS, 6))   # dark rocky floor
    cx = _HALF
    base_y = BS - 6

    dome_dark  = (20, 35, 42)
    dome_mid   = (25, 55, 65)
    glow_outer = (20, 150, 145, 120)
    glow_inner = (30, 210, 195, 180)
    glow_core  = (80, 245, 235, 220)

    # Dome silhouette
    r_dome = 11
    pygame.draw.ellipse(surf, dome_dark, (cx - r_dome, base_y - r_dome - 2, r_dome * 2, r_dome + 3))
    pygame.draw.ellipse(surf, dome_mid,  (cx - r_dome, base_y - r_dome - 2, r_dome * 2, r_dome + 3), 2)

    # Layered inner glow (SRCALPHA allows transparency)
    glow_surf = pygame.Surface((BS, BS), pygame.SRCALPHA)
    pygame.draw.circle(glow_surf, glow_outer, (cx, base_y - 8), 9)
    pygame.draw.circle(glow_surf, glow_inner, (cx, base_y - 8), 6)
    pygame.draw.circle(glow_surf, glow_core,  (cx, base_y - 8), 3)
    surf.blit(glow_surf, (0, 0))

    # Small spore dots around the base
    for angle_deg in (30, 90, 150, 210, 270, 330):
        angle = math.radians(angle_deg)
        sx2 = int(cx + 13 * math.cos(angle))
        sy2 = int(base_y - 4 + 6 * math.sin(angle))
        pygame.draw.circle(surf, (25, 180, 170, 160), (sx2, sy2), 2)

    return surf


# ---------------------------------------------------------------------------
# draw_ocean_rock — grey encrusted boulder with barnacle dots
# ---------------------------------------------------------------------------

def draw_ocean_rock():
    surf = _s()
    pygame.draw.rect(surf, (65, 70, 80), (0, BS - 6, BS, 6))  # dark seabed
    cx = _HALF
    base_y = BS - 6

    rock_base  = (88, 92, 100)
    rock_dark  = (62, 66, 74)
    rock_hi    = (110, 115, 125)
    barnacle   = (155, 148, 130)
    barnacle_d = (120, 115, 100)

    # Irregular boulder polygon
    pts = [
        (cx - 11, base_y),
        (cx - 13, base_y - 8),
        (cx - 8,  base_y - 17),
        (cx + 2,  base_y - 19),
        (cx + 12, base_y - 14),
        (cx + 13, base_y - 5),
        (cx + 9,  base_y),
    ]
    pygame.draw.polygon(surf, rock_base, pts)
    pygame.draw.polygon(surf, rock_dark, pts, 2)
    # Highlight ridge along upper-left face
    pygame.draw.line(surf, rock_hi,
                     (cx - 10, base_y - 9), (cx, base_y - 18), 2)

    # Barnacle clusters — small circles with a dark ring
    barnacle_pos = [
        (cx - 5, base_y - 5),
        (cx + 4, base_y - 4),
        (cx + 7, base_y - 11),
        (cx - 2, base_y - 14),
        (cx + 2, base_y - 8),
    ]
    for bx2, by2 in barnacle_pos:
        pygame.draw.circle(surf, barnacle,   (bx2, by2), 3)
        pygame.draw.circle(surf, barnacle_d, (bx2, by2), 3, 1)
        pygame.draw.circle(surf, (175, 168, 150), (bx2, by2), 1)

    return surf


# ---------------------------------------------------------------------------
# draw_seashell_block — small shell silhouette on sand floor
# ---------------------------------------------------------------------------

def draw_seashell_block():
    surf = _s()
    pygame.draw.rect(surf, (200, 185, 150), (0, BS - 6, BS, 6))
    cx = _HALF
    base_y = BS - 6

    shell_col  = (230, 210, 170)
    shell_dark = (180, 158, 118)
    shell_hi   = (250, 235, 200)
    rib_col    = (195, 172, 130)

    # Fan-shaped scallop silhouette (tidal) on left, small cone (reef) hint on right
    # Primary: scallop fan
    fan_cx, fan_cy = cx - 3, base_y - 8
    for i in range(6):
        angle = math.pi + i * math.pi / 5
        ex = int(fan_cx + 9 * math.cos(angle))
        ey = int(fan_cy + 9 * math.sin(angle))
        pygame.draw.line(surf, rib_col, (fan_cx, fan_cy + 3), (ex, ey), 1)
    pygame.draw.ellipse(surf, shell_col,  (fan_cx - 9, fan_cy - 3, 18, 12))
    pygame.draw.ellipse(surf, shell_dark, (fan_cx - 9, fan_cy - 3, 18, 12), 1)
    pygame.draw.ellipse(surf, shell_hi,   (fan_cx - 5, fan_cy - 1, 8,  5))

    # Secondary: small cone shell partially behind/beside
    cone_pts = [(cx + 9, base_y - 2), (cx + 14, base_y - 2), (cx + 11, base_y - 12)]
    pygame.draw.polygon(surf, (215, 185, 145), cone_pts)
    pygame.draw.polygon(surf, shell_dark,      cone_pts, 1)

    return surf


# ---------------------------------------------------------------------------
# Public builder
# ---------------------------------------------------------------------------

def draw_oyster_block():
    surf = _s()
    pygame.draw.rect(surf, (200, 185, 150), (0, BS - 6, BS, 6))
    base_y = BS - 6
    cx = _HALF

    shell_outer = (155, 140, 115)
    shell_dark  = (105,  95,  75)
    pearl_hi    = (240, 235, 220)

    # Two clamped half-shells, slightly open
    pygame.draw.ellipse(surf, shell_outer, (cx - 12, base_y - 11, 24, 13))
    pygame.draw.ellipse(surf, shell_dark,  (cx - 12, base_y - 11, 24, 13), 1)
    # Hinge line
    pygame.draw.line(surf, shell_dark, (cx - 11, base_y - 4), (cx + 11, base_y - 4), 1)
    # Open gap revealing inner pearl-light
    pygame.draw.ellipse(surf, pearl_hi, (cx - 4, base_y - 7, 8, 4))
    pygame.draw.ellipse(surf, (255, 250, 240), (cx - 1, base_y - 6, 2, 2))
    return surf


def build_ocean_surfs():
    return {
        CORAL_FRAGMENT_BLOCK: draw_coral_fragment(),
        CORAL_GROWING:        draw_coral_growing(),
        CORAL_FULL:           draw_coral_full(),
        KELP_BLOCK:           draw_kelp(),
        SEA_ANEMONE:          draw_sea_anemone(),
        BIOLUME_DEEP_BLOCK:   draw_biolume_deep(),
        OCEAN_ROCK:           draw_ocean_rock(),
        SEASHELL_BLOCK:       draw_seashell_block(),
        OYSTER_BLOCK:         draw_oyster_block(),
    }
