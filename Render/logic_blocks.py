import pygame
from constants import BLOCK_SIZE

BS = BLOCK_SIZE
H  = BS // 2
Q  = BS // 4

_POWERED_TINT = (0, 220, 255)
_DIM_WIRE     = (80, 85, 110)
_LIT_WIRE     = (0, 210, 240)


# ---------------------------------------------------------------------------
# Wire tile
# ---------------------------------------------------------------------------

def draw_wire_tile(screen, bx, by, world, cam_x, cam_y):
    sx = bx * BS - cam_x
    sy = by * BS - cam_y
    powered = (bx, by) in world.powered_wires
    col = _LIT_WIRE if powered else _DIM_WIRE

    n = world.get_wire(bx, by - 1)
    s = world.get_wire(bx, by + 1)
    w = world.get_wire(bx - 1, by)
    e = world.get_wire(bx + 1, by)

    cx, cy = sx + H, sy + H
    r = 3
    pygame.draw.circle(screen, col, (cx, cy), r)
    if n:
        pygame.draw.line(screen, col, (cx, cy), (cx, sy),     2)
    if s:
        pygame.draw.line(screen, col, (cx, cy), (cx, sy + BS), 2)
    if w:
        pygame.draw.line(screen, col, (cx, cy), (sx, cy),     2)
    if e:
        pygame.draw.line(screen, col, (cx, cy), (sx + BS, cy), 2)
    if not (n or s or w or e):
        pygame.draw.line(screen, col, (sx + Q, cy), (sx + BS - Q, cy), 2)


# ---------------------------------------------------------------------------
# Switch
# ---------------------------------------------------------------------------

def build_switch_surfs():
    surfs = {}
    for on in (False, True):
        s = pygame.Surface((BS, BS))
        s.fill((70, 65, 62))
        pygame.draw.rect(s, (110, 100, 90), (4, 4, BS - 8, BS - 8), 0)
        pivot_x, pivot_y = H, H + 2
        knob_y = pivot_y - 10 if on else pivot_y + 4
        pygame.draw.line(s, (180, 170, 155), (pivot_x, pivot_y), (pivot_x, knob_y), 3)
        knob_col = (0, 200, 120) if on else (180, 60, 60)
        pygame.draw.circle(s, knob_col, (pivot_x, knob_y), 4)
        surfs[on] = s
    return surfs


# ---------------------------------------------------------------------------
# Toggle Latch
# ---------------------------------------------------------------------------

def build_latch_surfs():
    surfs = {}
    for on in (False, True):
        s = pygame.Surface((BS, BS))
        s.fill((62, 62, 72))
        pygame.draw.rect(s, (95, 95, 110), (4, 4, BS - 8, BS - 8), 0)
        pygame.draw.line(s, (140, 140, 160), (Q, H), (BS - Q, H), 2)
        pygame.draw.circle(s, (160, 160, 180), (Q, H), 3)
        pygame.draw.circle(s, (160, 160, 180), (BS - Q, H), 3)
        dot_x = BS - Q - 2 if on else Q + 2
        dot_col = (0, 200, 120) if on else (200, 100, 60)
        pygame.draw.circle(s, dot_col, (dot_x, H), 5)
        surfs[on] = s
    return surfs


# ---------------------------------------------------------------------------
# Gates (AND / OR / NOT)
# ---------------------------------------------------------------------------

def _gate_base(col_body, col_border):
    s = pygame.Surface((BS, BS))
    s.fill((55, 55, 62))
    pygame.draw.rect(s, col_body,   (5, 5, BS - 10, BS - 10), 0)
    pygame.draw.rect(s, col_border, (5, 5, BS - 10, BS - 10), 2)
    return s


def build_and_gate_surf(powered):
    s = _gate_base((55, 80, 100), (80, 120, 150))
    font = _small_font()
    lbl = font.render("AND", True, (200, 230, 255) if powered else (120, 150, 180))
    s.blit(lbl, (H - lbl.get_width() // 2, H - lbl.get_height() // 2))
    if powered:
        pygame.draw.rect(s, _POWERED_TINT, (0, 0, BS, BS), 2)
    return s


def build_or_gate_surf(powered):
    s = _gate_base((55, 100, 80), (80, 150, 110))
    font = _small_font()
    lbl = font.render("OR", True, (200, 255, 220) if powered else (120, 180, 140))
    s.blit(lbl, (H - lbl.get_width() // 2, H - lbl.get_height() // 2))
    if powered:
        pygame.draw.rect(s, _POWERED_TINT, (0, 0, BS, BS), 2)
    return s


def build_not_gate_surf(powered):
    s = _gate_base((100, 55, 55), (150, 80, 80))
    font = _small_font()
    lbl = font.render("NOT", True, (255, 200, 200) if powered else (180, 120, 120))
    s.blit(lbl, (H - lbl.get_width() // 2, H - lbl.get_height() // 2))
    pygame.draw.circle(s, (220, 80, 80), (BS - 6, H), 4, 1)
    if powered:
        pygame.draw.rect(s, _POWERED_TINT, (0, 0, BS, BS), 2)
    return s


# ---------------------------------------------------------------------------
# Dam
# ---------------------------------------------------------------------------

def build_dam_surfs():
    surfs = {}
    for closed in (True, False):
        s = pygame.Surface((BS, BS))
        if closed:
            s.fill((120, 112, 95))
            for y in range(0, BS, 8):
                pygame.draw.line(s, (100, 94, 78), (0, y), (BS, y), 1)
            pygame.draw.rect(s, (90, 84, 70), (0, 0, BS, BS), 2)
        else:
            s.fill((0, 0, 0, 0))
            s.set_colorkey((0, 0, 0))
            for x in range(2, BS - 2, 6):
                pygame.draw.line(s, (80, 110, 160), (x, 4), (x, BS - 4), 1)
        surfs[closed] = s
    return surfs


# ---------------------------------------------------------------------------
# Pump
# ---------------------------------------------------------------------------

def build_pump_surfs():
    surfs = {}
    for on in (False, True):
        s = pygame.Surface((BS, BS))
        s.fill((75, 80, 85))
        pygame.draw.rect(s, (100, 108, 115), (4, 4, BS - 8, BS - 8), 0)
        pygame.draw.circle(s, (130, 140, 150), (H, H), 8, 2)
        if on:
            pygame.draw.line(s, (0, 210, 240), (H, H - 6), (H, H + 6), 2)
            pygame.draw.line(s, (0, 210, 240), (H - 6, H), (H + 6, H), 2)
        else:
            pygame.draw.circle(s, (80, 85, 90), (H, H), 3)
        surfs[on] = s
    return surfs


# ---------------------------------------------------------------------------
# Iron Gate
# ---------------------------------------------------------------------------

def build_iron_gate_surfs():
    surfs = {}
    for closed in (True, False):
        s = pygame.Surface((BS, BS))
        s.set_colorkey((0, 0, 0))
        s.fill((0, 0, 0))
        if closed:
            bar_col = (80, 85, 92)
            for x in (Q, H, BS - Q):
                pygame.draw.rect(s, bar_col, (x - 2, 0, 4, BS))
            pygame.draw.rect(s, (65, 70, 78), (2, Q, BS - 4, 4))
            pygame.draw.rect(s, (65, 70, 78), (2, BS - Q - 4, BS - 4, 4))
        else:
            bar_col = (80, 85, 92)
            for y in (Q, H, BS - Q):
                pygame.draw.rect(s, bar_col, (0, y - 2, BS, 4))
        surfs[closed] = s
    return surfs


# ---------------------------------------------------------------------------
# Surface cache + build helper
# ---------------------------------------------------------------------------

_surf_cache = {}


def build_pressure_plate_surfs():
    surfs = {}
    for on in (False, True):
        s = pygame.Surface((BS, BS), pygame.SRCALPHA)
        s.fill((0, 0, 0, 0))
        col = (150, 145, 135)
        pygame.draw.rect(s, col, (2, BS - 6, BS - 4, 5))
        pygame.draw.rect(s, (120, 115, 105), (2, BS - 6, BS - 4, 5), 1)
        if on:
            pygame.draw.rect(s, (0, 200, 120), (4, BS - 8, BS - 8, 3))
        surfs[on] = s
    return surfs


def build_day_sensor_surf():
    import math
    s = _gate_base((60, 55, 30), (120, 100, 40))
    pygame.draw.circle(s, (240, 210, 60), (H, H), 6)
    for i in range(8):
        a = math.radians(i * 45)
        x1 = int(H + 9 * math.cos(a))
        y1 = int(H + 9 * math.sin(a))
        x2 = int(H + 13 * math.cos(a))
        y2 = int(H + 13 * math.sin(a))
        pygame.draw.line(s, (240, 200, 40), (x1, y1), (x2, y2), 2)
    return s


def build_night_sensor_surf():
    s = _gate_base((20, 20, 60), (50, 60, 140))
    pygame.draw.circle(s, (180, 190, 230), (H - 1, H), 7)
    pygame.draw.circle(s, (20, 20, 60), (H + 3, H - 3), 5)
    for i, (ox, oy) in enumerate([(BS - Q - 2, Q), (BS - Q, H), (BS - Q - 3, H + 5)]):
        r = 1 + (i == 1)
        pygame.draw.circle(s, (200, 210, 255), (ox, oy), r)
    return s


def build_water_sensor_surf():
    s = _gate_base((30, 55, 80), (50, 100, 160))
    pts1 = [(Q, H - 2), (H - 2, H - 6), (H + 2, H - 2), (BS - Q, H - 6)]
    pts2 = [(Q, H + 4), (H - 2, H), (H + 2, H + 4), (BS - Q, H)]
    pygame.draw.lines(s, (80, 160, 220), False, pts1, 2)
    pygame.draw.lines(s, (80, 160, 220), False, pts2, 2)
    pygame.draw.circle(s, (0, 200, 255), (BS - Q - 2, BS - Q - 2), 3)
    return s


def build_crop_sensor_surf():
    s = _gate_base((30, 55, 30), (50, 130, 60))
    cx = H
    pygame.draw.line(s, (80, 160, 60), (cx, BS - 5), (cx, Q + 2), 2)
    lpts = [(cx, Q + 6), (cx - 6, Q + 10), (cx, Q + 8)]
    rpts = [(cx, Q + 6), (cx + 6, Q + 10), (cx, Q + 8)]
    pygame.draw.polygon(s, (80, 200, 70), lpts)
    pygame.draw.polygon(s, (80, 200, 70), rpts)
    pygame.draw.circle(s, (220, 200, 60), (cx, Q + 2), 3)
    return s


def build_repeater_surf(powered):
    s = _gate_base((50, 50, 75), (90, 90, 130))
    col = _POWERED_TINT if powered else (120, 120, 160)
    mid_y = H
    pygame.draw.line(s, col, (Q, mid_y), (BS - Q - 4, mid_y), 2)
    pts = [(BS - Q - 4, mid_y - 4), (BS - Q, mid_y), (BS - Q - 4, mid_y + 4)]
    pygame.draw.polygon(s, col, pts)
    if powered:
        pygame.draw.rect(s, _POWERED_TINT, (0, 0, BS, BS), 2)
    return s


def build_pulse_gen_surf(on):
    s = _gate_base((60, 35, 70), (120, 70, 140))
    col = _POWERED_TINT if on else (150, 100, 170)
    pygame.draw.circle(s, col, (H, H), 8, 2)
    pygame.draw.line(s, col, (H, H), (H, H - 6), 2)
    pygame.draw.line(s, col, (H, H), (H + 4, H), 2)
    if on:
        pygame.draw.circle(s, (200, 100, 220), (H, H), 3)
        pygame.draw.rect(s, _POWERED_TINT, (0, 0, BS, BS), 2)
    return s


def build_rs_latch_surfs():
    surfs = {}
    font = _small_font()
    for q in (False, True):
        s = _gate_base((40, 60, 60), (70, 110, 110))
        pygame.draw.line(s, (100, 160, 160), (Q, H - 3), (BS - Q, H - 3), 1)
        pygame.draw.line(s, (100, 160, 160), (Q, H + 3), (BS - Q, H + 3), 1)
        sl = font.render("S", True, (0, 220, 120) if q else (140, 180, 160))
        rl = font.render("R", True, (220, 80, 80) if not q else (180, 140, 140))
        s.blit(sl, (3, H - sl.get_height() // 2 - 4))
        s.blit(rl, (3, H - rl.get_height() // 2 + 4))
        dot_x = BS - Q
        dot_y = H - 3 if q else H + 3
        pygame.draw.circle(s, (0, 220, 120) if q else (220, 80, 80), (dot_x, dot_y), 4)
        surfs[q] = s
    return surfs


def build_powered_lantern_surfs():
    surfs = {}
    for on in (False, True):
        s = pygame.Surface((BS, BS), pygame.SRCALPHA)
        s.fill((0, 0, 0, 0))
        body_col = (200, 170, 60) if on else (100, 90, 50)
        glass_col = (255, 240, 120) if on else (80, 80, 70)
        pygame.draw.rect(s, body_col, (H - 5, Q, 10, BS - Q * 2))
        pygame.draw.rect(s, glass_col, (H - 4, Q + 3, 8, BS - Q * 2 - 6))
        pygame.draw.rect(s, body_col, (H - 7, Q - 2, 14, 4))
        pygame.draw.rect(s, body_col, (H - 7, BS - Q - 2, 14, 4))
        pygame.draw.line(s, body_col, (H, 2), (H, Q), 2)
        if on:
            pygame.draw.polygon(s, (255, 200, 50), [(H, Q + 5), (H - 3, H), (H, H - 3), (H + 3, H)])
            pygame.draw.rect(s, _POWERED_TINT, (H - 7, Q - 2, 14, BS - Q * 2), 1)
        surfs[on] = s
    return surfs


def build_alarm_bell_surfs():
    surfs = {}
    for on in (False, True):
        s = pygame.Surface((BS, BS), pygame.SRCALPHA)
        s.fill((0, 0, 0, 0))
        col = (220, 100, 40) if on else (140, 70, 30)
        bell_pts = [
            (H, Q), (H - 9, Q + 6), (H - 11, H + 4),
            (H - 5, H + 8), (H + 5, H + 8), (H + 11, H + 4), (H + 9, Q + 6),
        ]
        pygame.draw.polygon(s, col, bell_pts)
        pygame.draw.polygon(s, (80, 40, 15), bell_pts, 1)
        pygame.draw.circle(s, (80, 40, 15), (H, H + 11), 2)
        if on:
            for ox, oy, r in [(-13, H - 2, 5), (13, H - 2, 5), (-15, H + 6, 4), (15, H + 6, 4)]:
                pygame.draw.arc(s, (255, 140, 60),
                                pygame.Rect(H + ox - r, oy - r, r * 2, r * 2), 0, 3, 1)
            pygame.draw.rect(s, (255, 120, 40), (0, 0, BS, BS), 2)
        surfs[on] = s
    return surfs


def build_counter_surf():
    s = _gate_base((40, 65, 90), (70, 110, 150))
    font = _small_font()
    lbl = font.render("CNT", True, (160, 210, 255))
    s.blit(lbl, (H - lbl.get_width() // 2, Q - 2))
    # Progress bar showing threshold
    pygame.draw.rect(s, (30, 50, 70), (4, H, BS - 8, 6))
    pygame.draw.rect(s, (80, 150, 220), (4, H, BS - 8, 6), 1)
    return s


def build_comparator_surf():
    s = _gate_base((85, 35, 55), (150, 65, 90))
    font = _small_font()
    lbl = font.render("CMP", True, (255, 160, 190))
    s.blit(lbl, (H - lbl.get_width() // 2, Q - 2))
    pygame.draw.line(s, (200, 100, 130), (Q, H), (BS - Q, H), 2)
    pygame.draw.polygon(s, (200, 100, 130),
                        [(BS - Q - 4, H - 3), (BS - Q, H), (BS - Q - 4, H + 3)])
    return s


def build_observer_surf():
    s = _gate_base((30, 50, 40), (55, 110, 75))
    pygame.draw.ellipse(s, (80, 180, 100), (Q, H - 5, H, 10))
    pygame.draw.circle(s, (20, 40, 25), (H, H), 4)
    pygame.draw.circle(s, (100, 220, 130), (H, H), 2)
    pygame.draw.line(s, (55, 110, 75), (H, H), (BS - Q + 2, H), 2)
    return s


def build_sequencer_surf(step):
    s = _gate_base((55, 40, 80), (100, 75, 145))
    positions = [(BS - Q, H), (H, BS - Q), (Q, H), (H, Q)]
    for i, (px, py) in enumerate(positions):
        col = (0, 220, 255) if i == step else (70, 55, 100)
        pygame.draw.circle(s, col, (px, py), 4)
    pygame.draw.circle(s, (130, 100, 180), (H, H), 3)
    return s


def build_t_flipflop_surf(q):
    s = _gate_base((80, 70, 30), (150, 130, 55))
    font = _small_font()
    lbl = font.render("T", True, (255, 230, 100))
    s.blit(lbl, (H - lbl.get_width() // 2, Q))
    q_col = (0, 220, 120) if q else (180, 60, 60)
    pygame.draw.circle(s, q_col, (H, BS - Q - 2), 5)
    pygame.draw.line(s, (200, 180, 80), (Q, H), (BS - Q, H), 1)
    return s


def build_deposit_trigger_surf():
    s = pygame.Surface((BS, BS))
    s.fill((50, 38, 20))
    # Amber body
    pygame.draw.rect(s, (200, 140, 50), (Q, Q, H, H))
    pygame.draw.rect(s, (240, 180, 80), (Q, Q, H, H), 2)
    # Downward arrow (funnel symbol)
    cx = BS // 2
    pygame.draw.line(s, (255, 220, 100), (cx, Q + 3), (cx, H + 2), 2)
    pts = [(cx, H + 6), (cx - 4, H + 1), (cx + 4, H + 1)]
    pygame.draw.polygon(s, (255, 220, 100), pts)
    return s


def build_xor_gate_surf(powered):
    s = _gate_base((70, 95, 45), (110, 145, 70))
    font = _small_font()
    lbl = font.render("XOR", True, (195, 240, 140) if powered else (120, 170, 80))
    s.blit(lbl, (H - lbl.get_width() // 2, H - lbl.get_height() // 2))
    # Double curve on output side to distinguish from OR
    pygame.draw.arc(s, (110, 145, 70), (BS - Q - 4, H - 5, 8, 10), 0, 3, 1)
    if powered:
        pygame.draw.rect(s, _POWERED_TINT, (0, 0, BS, BS), 2)
    return s


def build_player_sensor_surf():
    import math
    s = _gate_base((40, 55, 90), (65, 90, 150))
    # Silhouette body
    pygame.draw.circle(s, (120, 160, 220), (H, Q + 4), 4)
    pygame.draw.line(s, (120, 160, 220), (H, Q + 8), (H, H + 4), 2)
    pygame.draw.line(s, (120, 160, 220), (H, H + 1), (H - 4, H + 7), 2)
    pygame.draw.line(s, (120, 160, 220), (H, H + 1), (H + 4, H + 7), 2)
    # Detection radius arcs
    for r in (10, 14):
        pygame.draw.arc(s, (0, 180, 240),
                        pygame.Rect(H - r, H - r, r * 2, r * 2), 0, 6.28, 1)
    return s


def build_crossover_wire_surf(h_powered, v_powered):
    s = pygame.Surface((BS, BS))
    s.fill((40, 42, 50))
    cx, cy = H, H
    h_col = _LIT_WIRE if h_powered else _DIM_WIRE
    v_col = _LIT_WIRE if v_powered else _DIM_WIRE
    # Horizontal channel
    pygame.draw.line(s, h_col, (0, cy), (BS, cy), 2)
    # Vertical channel (drawn over, with a tiny gap at centre to hint at separation)
    pygame.draw.line(s, v_col, (cx, 0), (cx, cy - 4), 2)
    pygame.draw.line(s, v_col, (cx, cy + 4), (cx, BS), 2)
    # Bridge marker at crossing point
    pygame.draw.circle(s, (70, 75, 90), (cx, cy), 3)
    return s


def build_signal_lamp_surfs():
    surfs = {}
    for on in (False, True):
        s = pygame.Surface((BS, BS))
        s.fill((45, 45, 50))
        body_col = (100, 100, 108) if not on else (200, 200, 80)
        glass_col = (70, 70, 80) if not on else (255, 255, 100)
        pygame.draw.circle(s, body_col, (H, H), 10)
        pygame.draw.circle(s, glass_col, (H, H), 7)
        pygame.draw.circle(s, (60, 60, 68), (H, H), 10, 2)
        if on:
            pygame.draw.circle(s, (255, 255, 180), (H, H), 4)
            pygame.draw.rect(s, _POWERED_TINT, (0, 0, BS, BS), 2)
        surfs[on] = s
    return surfs


def build_pipe_valve_surfs():
    surfs = {}
    for open_ in (False, True):
        s = pygame.Surface((BS, BS))
        s.fill((55, 45, 35))
        pipe_col = (100, 85, 65)
        # Horizontal pipe body
        pygame.draw.rect(s, pipe_col, (2, H - 4, BS - 4, 8))
        pygame.draw.rect(s, (80, 65, 50), (2, H - 4, BS - 4, 8), 1)
        # Gate disc
        disc_col = (160, 120, 60) if open_ else (200, 70, 50)
        if open_:
            pygame.draw.line(s, disc_col, (H - 4, Q + 2), (H + 4, BS - Q - 2), 3)
        else:
            pygame.draw.rect(s, disc_col, (H - 3, Q, 6, BS - Q * 2))
        # Actuator stem on top
        pygame.draw.line(s, (130, 120, 100), (H, H - 4), (H, Q), 2)
        pygame.draw.rect(s, (150, 130, 100), (H - 4, Q - 4, 8, 5))
        surfs[open_] = s
    return surfs


def build_pipe_buffer_surf():
    s = pygame.Surface((BS, BS))
    s.fill((40, 48, 38))
    # Tank body
    pygame.draw.rect(s, (70, 90, 60), (Q, Q + 2, H, BS - Q * 2 - 2))
    pygame.draw.rect(s, (50, 70, 45), (Q, Q + 2, H, BS - Q * 2 - 2), 1)
    # Fill indicator lines
    for i in range(3):
        y = Q + 4 + i * 6
        pygame.draw.line(s, (80, 110, 70), (Q + 2, y), (Q + H - 3, y), 1)
    # Input/output arrows
    pygame.draw.polygon(s, (100, 140, 90),
                        [(2, H - 3), (Q - 1, H), (2, H + 3)])
    pygame.draw.polygon(s, (100, 140, 90),
                        [(BS - 2, H - 3), (BS - Q + 1, H), (BS - 2, H + 3)])
    return s


def build_trapdoor_surfs():
    surfs = {}
    for open_ in (False, True):
        s = pygame.Surface((BS, BS))
        if not open_:
            s.fill((80, 65, 45))
            # Plank lines
            for y in range(4, BS - 4, 8):
                pygame.draw.line(s, (65, 52, 36), (4, y), (BS - 4, y), 1)
            pygame.draw.rect(s, (55, 44, 30), (0, 0, BS, BS), 2)
            # Hinge hints
            for hx in (Q, BS - Q - 2):
                pygame.draw.rect(s, (110, 100, 80), (hx, BS - 6, 6, 5))
        else:
            s.set_colorkey((0, 0, 0))
            s.fill((0, 0, 0))
            # Open: show a dark pit with edge boards folded up
            pygame.draw.rect(s, (30, 25, 18), (0, 0, BS, BS))
            for brd_y in (0, BS - 5):
                pygame.draw.rect(s, (80, 65, 45), (0, brd_y, BS, 5))
        surfs[open_] = s
    return surfs


def build_logic_surfs():
    from blocks import (SWITCH_BLOCK_OFF, SWITCH_BLOCK_ON,
                        LATCH_BLOCK_OFF, LATCH_BLOCK_ON,
                        AND_GATE_BLOCK, OR_GATE_BLOCK, NOT_GATE_BLOCK,
                        XOR_GATE_BLOCK,
                        DAM_BLOCK_CLOSED, DAM_BLOCK_OPEN,
                        PUMP_BLOCK_OFF, PUMP_BLOCK_ON,
                        IRON_GATE_BLOCK_CLOSED, IRON_GATE_BLOCK_OPEN,
                        PRESSURE_PLATE_OFF, PRESSURE_PLATE_ON,
                        DAY_SENSOR_BLOCK, NIGHT_SENSOR_BLOCK,
                        WATER_SENSOR_BLOCK, CROP_SENSOR_BLOCK,
                        PLAYER_SENSOR_BLOCK,
                        REPEATER_BLOCK, PULSE_GEN_BLOCK,
                        RS_LATCH_Q0, RS_LATCH_Q1,
                        POWERED_LANTERN_OFF, POWERED_LANTERN_ON,
                        ALARM_BELL_OFF, ALARM_BELL_ON,
                        COUNTER_BLOCK, COMPARATOR_BLOCK, OBSERVER_BLOCK,
                        SEQUENCER_BLOCK, T_FLIPFLOP_BLOCK,
                        DEPOSIT_TRIGGER_BLOCK,
                        CROSSOVER_WIRE_BLOCK,
                        SIGNAL_LAMP_OFF, SIGNAL_LAMP_ON,
                        PIPE_VALVE_CLOSED, PIPE_VALVE_OPEN,
                        PIPE_BUFFER_BLOCK,
                        TRAPDOOR_CLOSED, TRAPDOOR_OPEN)
    sw = build_switch_surfs()
    lt = build_latch_surfs()
    dm = build_dam_surfs()
    pm = build_pump_surfs()
    ig = build_iron_gate_surfs()
    pp = build_pressure_plate_surfs()
    rsl = build_rs_latch_surfs()
    pl = build_powered_lantern_surfs()
    ab = build_alarm_bell_surfs()
    sl = build_signal_lamp_surfs()
    pv = build_pipe_valve_surfs()
    td = build_trapdoor_surfs()
    return {
        SWITCH_BLOCK_OFF:       sw[False],
        SWITCH_BLOCK_ON:        sw[True],
        LATCH_BLOCK_OFF:        lt[False],
        LATCH_BLOCK_ON:         lt[True],
        AND_GATE_BLOCK:         build_and_gate_surf(False),
        OR_GATE_BLOCK:          build_or_gate_surf(False),
        NOT_GATE_BLOCK:         build_not_gate_surf(False),
        XOR_GATE_BLOCK:         build_xor_gate_surf(False),
        DAM_BLOCK_CLOSED:       dm[True],
        DAM_BLOCK_OPEN:         dm[False],
        PUMP_BLOCK_OFF:         pm[False],
        PUMP_BLOCK_ON:          pm[True],
        IRON_GATE_BLOCK_CLOSED: ig[True],
        IRON_GATE_BLOCK_OPEN:   ig[False],
        PRESSURE_PLATE_OFF:     pp[False],
        PRESSURE_PLATE_ON:      pp[True],
        DAY_SENSOR_BLOCK:       build_day_sensor_surf(),
        NIGHT_SENSOR_BLOCK:     build_night_sensor_surf(),
        WATER_SENSOR_BLOCK:     build_water_sensor_surf(),
        CROP_SENSOR_BLOCK:      build_crop_sensor_surf(),
        PLAYER_SENSOR_BLOCK:    build_player_sensor_surf(),
        REPEATER_BLOCK:         build_repeater_surf(False),
        PULSE_GEN_BLOCK:        build_pulse_gen_surf(False),
        RS_LATCH_Q0:            rsl[False],
        RS_LATCH_Q1:            rsl[True],
        POWERED_LANTERN_OFF:    pl[False],
        POWERED_LANTERN_ON:     pl[True],
        ALARM_BELL_OFF:         ab[False],
        ALARM_BELL_ON:          ab[True],
        COUNTER_BLOCK:          build_counter_surf(),
        COMPARATOR_BLOCK:       build_comparator_surf(),
        OBSERVER_BLOCK:         build_observer_surf(),
        SEQUENCER_BLOCK:        build_sequencer_surf(0),
        T_FLIPFLOP_BLOCK:       build_t_flipflop_surf(False),
        DEPOSIT_TRIGGER_BLOCK:  build_deposit_trigger_surf(),
        CROSSOVER_WIRE_BLOCK:   build_crossover_wire_surf(False, False),
        SIGNAL_LAMP_OFF:        sl[False],
        SIGNAL_LAMP_ON:         sl[True],
        PIPE_VALVE_CLOSED:      pv[False],
        PIPE_VALVE_OPEN:        pv[True],
        PIPE_BUFFER_BLOCK:      build_pipe_buffer_surf(),
        TRAPDOOR_CLOSED:        td[False],
        TRAPDOOR_OPEN:          td[True],
    }


_font_cache = {}


def _small_font():
    if "f" not in _font_cache:
        _font_cache["f"] = pygame.font.SysFont(None, 14)
    return _font_cache["f"]


# ---------------------------------------------------------------------------
# Pressure Plate  (1198=off, 1199=on)
# ---------------------------------------------------------------------------

def build_pressure_plate_surfs():
    surfs = {}
    for on in (False, True):
        s = pygame.Surface((BS, BS))
        s.fill((55, 55, 62))
        slab_y = BS - BS // 3
        pygame.draw.rect(s, (130, 130, 135), (2, slab_y, BS - 4, BS // 3 - 2))
        pygame.draw.rect(s, (100, 100, 105), (2, slab_y, BS - 4, BS // 3 - 2), 1)
        if on:
            pygame.draw.line(s, (0, 220, 80), (Q, slab_y + 2), (BS - Q, slab_y + 2), 2)
        surfs[on] = s
    return surfs


# ---------------------------------------------------------------------------
# Day Sensor  (1200)
# ---------------------------------------------------------------------------

def build_day_sensor_surf():
    s = _gate_base((60, 58, 50), (100, 95, 70))
    cx, cy = H, H
    pygame.draw.circle(s, (240, 200, 40), (cx, cy), 6)
    for angle in range(0, 360, 45):
        import math
        rx = int(cx + 10 * math.cos(math.radians(angle)))
        ry = int(cy + 10 * math.sin(math.radians(angle)))
        ix = int(cx + 7 * math.cos(math.radians(angle)))
        iy = int(cy + 7 * math.sin(math.radians(angle)))
        pygame.draw.line(s, (220, 180, 30), (ix, iy), (rx, ry), 1)
    return s


# ---------------------------------------------------------------------------
# Night Sensor  (1201)
# ---------------------------------------------------------------------------

def build_night_sensor_surf():
    s = _gate_base((25, 28, 55), (50, 55, 100))
    cx, cy = H, H
    pygame.draw.circle(s, (180, 185, 220), (cx, cy), 7)
    pygame.draw.circle(s, (25, 28, 55), (cx + 4, cy - 3), 5)
    pygame.draw.circle(s, (220, 220, 255), (cx + 8, cy - 6), 2)
    pygame.draw.circle(s, (200, 200, 240), (cx - 4, cy + 7), 1)
    return s


# ---------------------------------------------------------------------------
# Water Sensor  (1202)
# ---------------------------------------------------------------------------

def build_water_sensor_surf():
    s = _gate_base((60, 70, 80), (80, 100, 120))
    for i, dy in enumerate((-4, 0, 4)):
        pts = [(Q + j * 4, H + dy + (2 if j % 2 == 0 else -2)) for j in range(6)]
        pygame.draw.lines(s, (80, 160, 220), False, pts, 2)
    pygame.draw.circle(s, (0, 220, 240), (BS - Q - 2, Q + 2), 3)
    return s


# ---------------------------------------------------------------------------
# Crop Sensor  (1203)
# ---------------------------------------------------------------------------

def build_crop_sensor_surf():
    s = _gate_base((50, 68, 48), (70, 100, 68))
    stem_x = H
    pygame.draw.line(s, (80, 140, 60), (stem_x, BS - 6), (stem_x, Q + 2), 2)
    leaf_pts_l = [(stem_x, H), (stem_x - 7, H - 4), (stem_x - 3, H + 2)]
    leaf_pts_r = [(stem_x, H - 3), (stem_x + 7, H - 7), (stem_x + 3, H + 1)]
    pygame.draw.polygon(s, (60, 180, 60), leaf_pts_l)
    pygame.draw.polygon(s, (60, 180, 60), leaf_pts_r)
    pygame.draw.circle(s, (100, 210, 80), (stem_x, Q + 2), 3)
    return s


# ---------------------------------------------------------------------------
# Repeater  (1204=off, 1205=on)
# ---------------------------------------------------------------------------

def build_repeater_surf(powered):
    s = _gate_base((65, 65, 75), (90, 90, 105))
    col = _POWERED_TINT if powered else (140, 140, 160)
    tip_x, mid_y = BS - Q, H
    pygame.draw.line(s, col, (Q + 2, mid_y), (tip_x - 4, mid_y), 2)
    pygame.draw.polygon(s, col, [(tip_x - 6, mid_y - 5), (tip_x, mid_y), (tip_x - 6, mid_y + 5)])
    if powered:
        pygame.draw.rect(s, _POWERED_TINT, (0, 0, BS, BS), 2)
    return s


# ---------------------------------------------------------------------------
# Pulse Generator  (1206=off, 1207=on)
# ---------------------------------------------------------------------------

def build_pulse_gen_surf(on):
    s = _gate_base((60, 62, 70), (85, 88, 100))
    col = _POWERED_TINT if on else (120, 125, 145)
    pygame.draw.circle(s, col, (H, H), 9, 2)
    pygame.draw.line(s, col, (H, H), (H + 6, H - 5), 2)
    pygame.draw.line(s, col, (H, H - 9), (H, H - 6), 2)
    if on:
        pygame.draw.circle(s, _POWERED_TINT, (H, H), 4)
        pygame.draw.rect(s, _POWERED_TINT, (0, 0, BS, BS), 2)
    return s


# ---------------------------------------------------------------------------
# RS Latch  (1208=Q0, 1209=Q1)
# ---------------------------------------------------------------------------

def build_rs_latch_surfs():
    surfs = {}
    font = _small_font()
    for q1 in (False, True):
        s = _gate_base((58, 58, 68), (85, 85, 100))
        track_y1, track_y2 = H - 6, H + 6
        pygame.draw.line(s, (100, 100, 120), (Q, track_y1), (BS - Q, track_y1), 2)
        pygame.draw.line(s, (100, 100, 120), (Q, track_y2), (BS - Q, track_y2), 2)
        s_lbl = font.render("S", True, (180, 180, 210))
        r_lbl = font.render("R", True, (180, 180, 210))
        s.blit(s_lbl, (Q - s_lbl.get_width() // 2, track_y1 - 8))
        s.blit(r_lbl, (BS - Q - r_lbl.get_width() // 2, track_y1 - 8))
        dot_x = BS - Q if q1 else Q
        dot_y = track_y1 if not q1 else track_y2
        pygame.draw.circle(s, _POWERED_TINT if q1 else (200, 80, 80), (dot_x, dot_y), 4)
        surfs[q1] = s
    return surfs


# ---------------------------------------------------------------------------
# Powered Lantern  (1210=off, 1211=on)
# ---------------------------------------------------------------------------

def build_powered_lantern_surfs():
    surfs = {}
    for on in (False, True):
        s = pygame.Surface((BS, BS))
        s.fill((45, 45, 50))
        body_col = (80, 80, 88) if not on else (100, 95, 70)
        glass_col = (100, 105, 115) if not on else (255, 240, 100)
        pygame.draw.rect(s, body_col,  (H - 7, Q + 2, 14, BS - Q - 4))
        pygame.draw.rect(s, glass_col, (H - 5, Q + 5, 10, BS - Q - 10))
        pygame.draw.rect(s, (60, 60, 68), (H - 7, Q + 2, 14, BS - Q - 4), 1)
        pygame.draw.rect(s, (50, 48, 40), (H - 4, 2, 8, Q))
        if on:
            pygame.draw.polygon(s, (255, 160, 20),
                                [(H, Q + 6), (H - 3, H + 2), (H, H - 1), (H + 3, H + 2)])
            pygame.draw.rect(s, _POWERED_TINT, (0, 0, BS, BS), 2)
        surfs[on] = s
    return surfs


# ---------------------------------------------------------------------------
# Alarm Bell  (1212=off, 1213=on)  — NOTE: only 12 new IDs needed; bell uses last 2
# ---------------------------------------------------------------------------

def build_alarm_bell_surfs():
    surfs = {}
    for on in (False, True):
        s = pygame.Surface((BS, BS))
        s.fill((45, 42, 40))
        bell_col = (160, 130, 60) if not on else (220, 140, 30)
        pts = [(H - 10, BS - Q), (H - 12, H), (H, Q + 2), (H + 12, H), (H + 10, BS - Q)]
        pygame.draw.polygon(s, bell_col, pts)
        pygame.draw.polygon(s, (120, 100, 40) if not on else (200, 120, 20), pts, 2)
        pygame.draw.rect(s, (80, 70, 30), (H - 3, Q - 2, 6, 6))
        pygame.draw.circle(s, (100, 90, 40) if not on else (240, 100, 20),
                           (H, BS - Q + 2), 3)
        if on:
            wave_col = (220, 80, 20)
            for dx, dy in ((-14, -4), (14, -4), (-16, H - 4), (16, H - 4)):
                pygame.draw.arc(s, wave_col,
                                (H + dx - 4, H + dy - 4, 8, 8), 0, 3, 2)
            pygame.draw.rect(s, (220, 60, 0), (0, 0, BS, BS), 2)
        surfs[on] = s
    return surfs
