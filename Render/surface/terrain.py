import pygame
from blocks import BLOCKS, ALL_LOGS, ALL_LEAVES, ALL_FRUIT_CLUSTERS, FRUIT_CLUSTER_LEAF_MAP
from constants import BLOCK_SIZE


def _darken(color, amount=25):
    return tuple(max(0, c - amount) for c in color)


def build_log_variants():
    trunk_widths  = [BLOCK_SIZE, BLOCK_SIZE, 18, 12, BLOCK_SIZE, BLOCK_SIZE, 18, BLOCK_SIZE]
    bright_shifts = [0, 18, 0, -14, 0, 14, -8, 0]
    grain_gaps    = [5,  4,  5,   4,  6,   5,  4,  5]
    variants = {}
    for bid in ALL_LOGS:
        bdata = BLOCKS.get(bid)
        if not bdata or not bdata.get("color"):
            continue
        base = bdata["color"]
        surfs = []
        for v in range(8):
            shift = bright_shifts[v]
            tone  = tuple(max(0, min(255, c + shift)) for c in base)
            dark  = _darken(tone, 32)
            tw    = trunk_widths[v]
            cx    = (BLOCK_SIZE - tw) // 2
            gs    = grain_gaps[v]
            s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
            side_col = _darken(tone, 50)
            s.fill(side_col if tw < BLOCK_SIZE else tone)
            if tw < BLOCK_SIZE:
                pygame.draw.rect(s, tone, (cx, 0, tw, BLOCK_SIZE))
            grain = _darken(tone, 24)
            for gx in range(cx + 3, cx + tw - 2, gs):
                pygame.draw.line(s, grain, (gx, 1), (gx, BLOCK_SIZE - 2), 1)
            hi = tuple(min(255, c + 14) for c in tone)
            if cx + 2 < cx + tw - 1:
                pygame.draw.line(s, hi, (cx + 2, 1), (cx + 2, BLOCK_SIZE - 2), 1)
            if v == 4:
                kx, ky = BLOCK_SIZE // 2, BLOCK_SIZE // 2 + 4
                knot = _darken(tone, 55)
                pygame.draw.ellipse(s, knot,             (kx - 4, ky - 3, 8, 6))
                pygame.draw.ellipse(s, _darken(knot, 20),(kx - 2, ky - 1, 4, 3))
            if v == 5:
                moss = (max(0, tone[0] - 22), min(255, tone[1] + 32), max(0, tone[2] - 22))
                for mx, my in [(4, 2), (BLOCK_SIZE - 10, 5),
                               (6, BLOCK_SIZE - 10), (BLOCK_SIZE - 8, BLOCK_SIZE - 8)]:
                    pygame.draw.rect(s, moss,             (mx, my, 5, 4))
                    pygame.draw.rect(s, _darken(moss, 18),(mx + 1, my + 1, 3, 2))
            if v == 7:
                ring = _darken(tone, 28)
                for ry in range(4, BLOCK_SIZE - 2, 7):
                    pygame.draw.line(s, ring, (cx + 1, ry), (cx + tw - 2, ry), 1)
            border_rect = (cx, 0, tw, BLOCK_SIZE) if tw < BLOCK_SIZE else s.get_rect()
            pygame.draw.rect(s, dark, border_rect, 1)
            surfs.append(s)
        variants[bid] = surfs
    return variants


def build_leaf_variants():
    bright_shifts = [0, 20, 38, -16, 0, 20, 0, -16]
    speckled      = [False, False, False, False, True, True, True, True]
    _spots  = [(3,3),(9,11),(15,4),(21,8),(27,2),(5,19),(12,24),(19,17),(25,21),(7,28),(22,27),(14,14)]
    _bright = [(6,7),(18,5),(11,20),(24,15)]
    variants = {}
    for bid in ALL_LEAVES:
        bdata = BLOCKS.get(bid)
        if not bdata or not bdata.get("color"):
            continue
        base = bdata["color"]
        surfs = []
        for v in range(8):
            shift = bright_shifts[v]
            tone  = tuple(max(0, min(255, c + shift)) for c in base)
            if v == 6:
                tone = (min(255, tone[0] + 28), max(0, tone[1] - 12), max(0, tone[2] - 18))
            dark  = _darken(tone, 28)
            s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
            s.fill(tone)
            if speckled[v]:
                spot_col   = _darken(tone, 40)
                bright_col = tuple(min(255, c + 20) for c in tone)
                for sx2, sy2 in _spots:
                    if sx2 + 3 <= BLOCK_SIZE and sy2 + 3 <= BLOCK_SIZE:
                        pygame.draw.rect(s, spot_col, (sx2, sy2, 3, 3))
                for sx2, sy2 in _bright:
                    if sx2 + 2 <= BLOCK_SIZE and sy2 + 2 <= BLOCK_SIZE:
                        pygame.draw.rect(s, bright_col, (sx2, sy2, 2, 2))
            if v == 7:
                inner = _darken(tone, 22)
                pygame.draw.rect(s, inner, (2, 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4))
            pygame.draw.rect(s, dark, s.get_rect(), 1)
            surfs.append(s)
        variants[bid] = surfs
    return variants


def build_fruit_cluster_variants():
    _dot_positions = [(4,5),(10,12),(18,6),(24,14),(8,22),(20,20),(14,9),(6,17),(22,4),(16,25)]
    variants = {}
    for bid, leaf_bid in FRUIT_CLUSTER_LEAF_MAP.items():
        bdata      = BLOCKS.get(bid)
        leaf_bdata = BLOCKS.get(leaf_bid)
        if not bdata or not leaf_bdata:
            continue
        fruit_col = bdata["color"]
        leaf_col  = leaf_bdata["color"]
        surfs = []
        for v in range(4):
            shift = [0, 15, -12, -20][v]
            tone  = tuple(max(0, min(255, c + shift)) for c in leaf_col)
            dark  = _darken(tone, 28)
            s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
            s.fill(tone)
            pygame.draw.rect(s, dark, s.get_rect(), 1)
            dot_dark = _darken(fruit_col, 20)
            for i, (dx, dy) in enumerate(_dot_positions):
                if i % 4 == v % 4:
                    continue
                col = dot_dark if (dx + dy) % 3 == 0 else fruit_col
                pygame.draw.rect(s, col, (dx, dy, 4, 4))
            surfs.append(s)
        variants[bid] = surfs
    return variants


def build_grass_variants():
    base = (58, 154, 58)
    bright_shifts = [0, 16, -14, 0, -8, 0, -20, 24, -10, 10]
    surfs = []
    for v in range(10):
        shift = bright_shifts[v]
        tone = tuple(max(0, min(255, c + shift)) for c in base)
        if v == 3:
            tone = (min(255, tone[0]+22), max(0, tone[1]-8), max(0, tone[2]-18))
        elif v == 6:
            tone = (max(0, tone[0]-8), min(255, tone[1]+6), max(0, tone[2]-4))
        dark = _darken(tone, 28)
        s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        s.fill(tone)
        if v == 1:
            for px2, py2 in [(4,7),(18,20),(24,5),(11,14),(27,22)]:
                pygame.draw.rect(s, _darken(tone,18), (px2, py2, 3, 3))
        elif v == 2:
            for px2, py2 in [(7,4),(22,16),(3,24),(15,10),(28,6)]:
                pygame.draw.rect(s, tuple(min(255,c+22) for c in tone), (px2, py2, 2, 2))
        elif v == 4:
            for px2, py2, pw, ph in [(3,3,4,3),(13,18,3,4),(22,8,2,2),(8,26,4,2)]:
                pygame.draw.rect(s, _darken(tone,18), (px2, py2, pw, ph))
        elif v == 5:
            for px2, py2 in [(14,22),(6,10),(23,16)]:
                pygame.draw.rect(s, (105,68,30), (px2, py2, 2, 2))
        elif v == 7:
            for px2, py2, pw, ph in [(2,2,5,3),(16,8,4,4),(8,18,3,5),(22,24,5,3)]:
                hi = tuple(min(255,c+14) for c in tone)
                pygame.draw.rect(s, hi, (px2, py2, pw, ph))
        elif v == 8:
            for px2, py2, pw, ph in [(1,1,6,5),(18,4,5,6),(3,20,7,4),(20,20,6,7)]:
                pygame.draw.rect(s, _darken(tone,24), (px2, py2, pw, ph))
        elif v == 9:
            for px2, py2 in [(3,5),(10,2),(17,8),(25,3),(6,16),(20,12),(12,22),(27,18),(4,26),(22,27)]:
                pygame.draw.rect(s, tuple(min(255,c+20) for c in tone), (px2, py2, 2, 2))
        pygame.draw.rect(s, dark, s.get_rect(), 1)
        surfs.append(s)
    return surfs


def build_dirt_variants():
    base = (115, 77, 38)
    bright_shifts = [0, 18, -14, 0, 0, 0, 0, 26, -18, 0]
    surfs = []
    for v in range(10):
        shift = bright_shifts[v]
        tone = tuple(max(0, min(255, c + shift)) for c in base)
        if v == 3:
            tone = (min(255,tone[0]+20), max(0,tone[1]-6), max(0,tone[2]-10))
        elif v == 7:
            tone = (min(255,tone[0]+8), min(255,tone[1]+14), min(255,tone[2]+22))
        elif v == 8:
            tone = (max(0,tone[0]-5), max(0,tone[1]-3), max(0,tone[2]+4))
        dark = _darken(tone, 30)
        s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        s.fill(tone)
        if v == 4:
            for px2, py2 in [(5,5),(16,9),(25,14),(8,22),(20,25),(12,15)]:
                pygame.draw.rect(s, _darken(tone,42), (px2, py2, 2, 2))
        elif v == 5:
            for px2, py2 in [(3,8),(14,3),(22,18),(9,26),(27,6),(18,22)]:
                pygame.draw.rect(s, tuple(min(255,c+30) for c in tone), (px2, py2, 2, 2))
        elif v == 6:
            for px2, py2 in [(10,12),(5,25),(22,7)]:
                pygame.draw.rect(s, _darken(tone,40), (px2, py2, 2, 2))
            for px2, py2 in [(22,20),(15,28),(3,16)]:
                pygame.draw.rect(s, tuple(min(255,c+24) for c in tone), (px2, py2, 2, 2))
        elif v == 8:
            for py2 in [6, 14, 22]:
                pygame.draw.rect(s, _darken(tone,20), (2, py2, BLOCK_SIZE-4, 2))
        elif v == 9:
            for px2, py2, pw, ph in [(2,3,4,3),(14,2,3,4),(24,6,3,3),(6,14,4,3),(19,16,3,4),(3,23,4,3),(22,23,3,3)]:
                pygame.draw.rect(s, _darken(tone,22), (px2, py2, pw, ph))
        pygame.draw.rect(s, dark, s.get_rect(), 1)
        surfs.append(s)
    return surfs


def build_sand_variants():
    base = (210, 190, 140)
    surfs = []
    for v in range(8):
        tone = base
        if v == 1:   tone = tuple(min(255,c+16) for c in base)
        elif v == 2: tone = tuple(max(0,c-14) for c in base)
        elif v == 3: tone = (min(255,base[0]+18), max(0,base[1]-6), max(0,base[2]-20))
        elif v == 4: tone = (min(255,base[0]+28), min(255,base[1]+22), min(255,base[2]+18))
        elif v == 7: tone = (max(0,base[0]-20), max(0,base[1]-16), max(0,base[2]-10))
        dark = _darken(tone, 26)
        s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        s.fill(tone)
        if v == 5:
            for py2 in [5, 12, 19, 26]:
                pygame.draw.rect(s, _darken(tone,18), (2, py2, BLOCK_SIZE-4, 1))
                pygame.draw.rect(s, tuple(min(255,c+14) for c in tone), (2, py2+1, BLOCK_SIZE-4, 1))
        elif v == 6:
            for px2, py2 in [(4,4),(13,8),(22,5),(7,17),(18,13),(26,20),(10,25),(20,27),(3,24)]:
                pygame.draw.rect(s, _darken(tone,32), (px2, py2, 2, 2))
        elif v == 7:
            for i in range(0, BLOCK_SIZE, 8):
                pygame.draw.rect(s, _darken(tone,24), (i, 0, 2, BLOCK_SIZE))
        pygame.draw.rect(s, dark, s.get_rect(), 1)
        surfs.append(s)
    return surfs


def build_snow_variants():
    base = (220, 232, 245)
    surfs = []
    for v in range(8):
        tone = base
        if v == 1:   tone = (245, 250, 255)
        elif v == 2: tone = (200, 215, 238)
        elif v == 3: tone = (210, 212, 215)
        elif v == 4: tone = base
        elif v == 5: tone = (215, 228, 242)
        elif v == 6: tone = (230, 240, 252)
        elif v == 7: tone = (205, 218, 232)
        dark = _darken(tone, 22)
        s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        s.fill(tone)
        if v == 2:
            for px2, py2, pw, ph in [(1,1,7,5),(18,3,6,7),(3,20,8,5),(20,22,7,6)]:
                pygame.draw.rect(s, _darken(tone,16), (px2, py2, pw, ph))
        elif v == 3:
            for px2, py2, pw, ph in [(2,4,5,4),(15,10,6,3),(8,20,5,5),(22,18,4,6)]:
                pygame.draw.rect(s, (190,192,194), (px2, py2, pw, ph))
        elif v == 4:
            for px2, py2 in [(5,3),(12,9),(21,5),(8,16),(18,14),(26,8),(3,23),(15,26),(24,22),(10,28)]:
                pygame.draw.rect(s, (255,255,255), (px2, py2, 2, 2))
        elif v == 5:
            for i in range(-BLOCK_SIZE, BLOCK_SIZE*2, 7):
                pygame.draw.line(s, tuple(min(255,c+12) for c in tone),
                                 (max(0,i),0), (min(BLOCK_SIZE,i+BLOCK_SIZE),min(BLOCK_SIZE,BLOCK_SIZE-i)), 1)
        elif v == 6:
            for px2, py2, pw, ph in [(4,2,8,4),(2,14,6,6),(16,18,7,5),(20,6,5,5)]:
                pygame.draw.rect(s, tuple(min(255,c+10) for c in tone), (px2, py2, pw, ph))
        elif v == 7:
            for py2 in [7, 16, 24]:
                pygame.draw.rect(s, _darken(tone,14), (1, py2, BLOCK_SIZE-2, 1))
        pygame.draw.rect(s, dark, s.get_rect(), 1)
        surfs.append(s)
    return surfs
