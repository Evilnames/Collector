import pygame

_crown_font = None

def _get_crown_font():
    global _crown_font
    if _crown_font is None:
        _crown_font = pygame.font.SysFont("consolas", 13, bold=True)
    return _crown_font


def draw_npc_soldier(screen, sx, sy, npc):
    bob        = int(npc._bob_offset)
    facing     = getattr(npc, 'facing', 1)
    c          = getattr(npc, 'clothing', {})
    armor_type = getattr(npc, 'armor_type', 'mail')
    armor = c.get('armor', (80, 85, 95))
    plate = c.get('plate', (130, 135, 145))
    trim  = c.get('trim',  (160, 50, 45))
    skin  = c.get('skin',  (215, 175, 125))
    body  = c.get('body',  (75, 80, 70))

    def _dim(col, f=0.7):  return tuple(int(v * f) for v in col)
    def _lite(col, a=20):  return tuple(min(255, v + a) for v in col)

    if armor_type == 'mail':
        pygame.draw.rect(screen, armor, (sx, sy + bob, 20, 18))
        for ry in range(1, 18, 3):
            pygame.draw.rect(screen, _lite(armor, 22), (sx + 1, sy + ry + bob, 18, 1))
        pygame.draw.rect(screen, trim, (sx + 8, sy + bob, 4, 18))
        helm = _lite(armor, 18)
        pygame.draw.ellipse(screen, helm, (sx + 3, sy - 13 + bob, 14, 12))
        pygame.draw.rect(screen, _dim(helm), (sx + 9, sy - 10 + bob, 2, 8))
        pygame.draw.rect(screen, skin, (sx + 4, sy - 8 + bob, 12, 6))
        pygame.draw.rect(screen, (30, 25, 20), (sx + 5,  sy - 6 + bob, 3, 2))
        pygame.draw.rect(screen, (30, 25, 20), (sx + 12, sy - 6 + bob, 3, 2))
        wx = sx + 20 if facing == 1 else sx - 2
        pygame.draw.rect(screen, (120, 100, 60), (wx, sy - 20 + bob, 2, 38))
        pygame.draw.polygon(screen, plate,
            [(wx + 1, sy - 28 + bob), (wx + 5, sy - 20 + bob), (wx - 3, sy - 20 + bob)])

    elif armor_type == 'plate':
        pygame.draw.rect(screen, armor, (sx, sy + bob, 20, 18))
        pygame.draw.rect(screen, plate, (sx + 3, sy + bob, 14, 14))
        pygame.draw.rect(screen, _dim(plate), (sx + 3, sy + 7 + bob, 14, 2))
        helm = _lite(plate, 18)
        pygame.draw.rect(screen, helm, (sx + 2, sy - 14 + bob, 16, 14))
        pygame.draw.rect(screen, (18, 14, 10), (sx + 3, sy - 9 + bob, 14, 3))
        pygame.draw.rect(screen, trim, (sx + 7, sy - 21 + bob, 6, 9))
        wx = sx + 20 if facing == 1 else sx - 2
        pygame.draw.rect(screen, (110, 90, 55), (wx, sy - 22 + bob, 2, 40))
        pygame.draw.rect(screen, plate, (wx - 2, sy - 28 + bob, 6, 8))
        pygame.draw.rect(screen, _dim(plate), (wx + 4, sy - 26 + bob, 2, 5))

    elif armor_type == 'lorica':
        pygame.draw.rect(screen, armor, (sx, sy + bob, 20, 18))
        for ry in range(0, 18, 4):
            pygame.draw.rect(screen, _lite(armor, 25), (sx, sy + ry + bob, 20, 2))
        helm = _lite(armor, 12)
        pygame.draw.rect(screen, helm, (sx + 2, sy - 13 + bob, 16, 13))
        pygame.draw.rect(screen, skin, (sx + 4, sy - 9 + bob, 12, 7))
        pygame.draw.rect(screen, (35, 25, 15), (sx + 5,  sy - 7 + bob, 3, 2))
        pygame.draw.rect(screen, (35, 25, 15), (sx + 12, sy - 7 + bob, 3, 2))
        pygame.draw.rect(screen, trim, (sx + 8, sy - 22 + bob, 4, 11))
        pygame.draw.rect(screen, _lite(trim, 30), (sx + 9, sy - 22 + bob, 2, 11))
        wx = sx + 20 if facing == 1 else sx - 2
        pygame.draw.rect(screen, (120, 100, 60), (wx, sy - 18 + bob, 2, 36))
        pygame.draw.rect(screen, plate, (wx - 1, sy - 24 + bob, 4, 8))

    elif armor_type == 'leather':
        pygame.draw.rect(screen, armor, (sx, sy + bob, 20, 18))
        for ry in range(1, 17, 3):
            offset = 0 if (ry // 3) % 2 == 0 else 2
            for rx in range(offset + 1, 19, 4):
                pygame.draw.rect(screen, plate, (sx + rx, sy + ry + bob, 3, 2))
        pygame.draw.rect(screen, body, (sx,      sy + bob, 5, 7))
        pygame.draw.rect(screen, body, (sx + 15, sy + bob, 5, 7))
        cap = _dim(armor, 0.75)
        pygame.draw.rect(screen, cap,  (sx + 3, sy - 14 + bob, 14, 8))
        pygame.draw.rect(screen, skin, (sx + 3, sy - 8  + bob, 14, 8))
        pygame.draw.rect(screen, (35, 25, 15), (sx + 5,  sy - 6 + bob, 3, 2))
        pygame.draw.rect(screen, (35, 25, 15), (sx + 12, sy - 6 + bob, 3, 2))
        bx2 = sx - 5 if facing == 1 else sx + 23
        pygame.draw.arc(screen, (110, 80, 40),
                        (bx2, sy - 8 + bob, 6, 20), 0.0, 3.14159, 2)

    elif armor_type == 'naval':
        pygame.draw.rect(screen, body,  (sx, sy + bob, 20, 18))
        pygame.draw.rect(screen, armor, (sx + 3, sy + bob, 14, 12))
        pygame.draw.rect(screen, trim,  (sx + 8, sy + bob, 4, 18))
        helm = _lite(armor, 16)
        pygame.draw.rect(screen, helm, (sx + 2, sy - 13 + bob, 16, 13))
        pygame.draw.rect(screen, skin, (sx + 4, sy - 9 + bob, 12, 7))
        pygame.draw.rect(screen, _dim(helm), (sx + 2, sy - 4 + bob, 16, 3))
        pygame.draw.rect(screen, (35, 25, 15), (sx + 5,  sy - 7 + bob, 3, 2))
        pygame.draw.rect(screen, (35, 25, 15), (sx + 12, sy - 7 + bob, 3, 2))
        cx = sx + 20 if facing == 1 else sx - 8
        pygame.draw.rect(screen, (110, 90, 55), (cx,     sy + 4 + bob, 8, 3))
        pygame.draw.rect(screen, (110, 90, 55), (cx + 3, sy + 1 + bob, 2, 9))
        pygame.draw.rect(screen, plate,         (cx,     sy + 4 + bob, 8, 1))

    # Kingdom pennant
    fx, fy = sx + 10, sy - 27 + bob
    pygame.draw.rect(screen, (140, 120, 80), (fx, fy, 1, 10))
    pygame.draw.polygon(screen, trim,
        [(fx + 1, fy), (fx + 8, fy + 3), (fx + 1, fy + 6)])


def draw_npc_chef(screen, sx, sy, npc, font):
    bob = int(npc._bob_offset)
    c = getattr(npc, 'clothing', {})
    body = c.get('body', (70, 55, 45))
    skin = c.get('skin', (255, 215, 160))
    pygame.draw.rect(screen, body, (sx, sy + bob, 20, 18))
    pygame.draw.rect(screen, (240, 235, 220), (sx + 5, sy + bob, 10, 18))
    pygame.draw.rect(screen, (245, 242, 235), (sx + 4, sy - 18 + bob, 12, 10))
    pygame.draw.rect(screen, (200, 195, 185), (sx + 4, sy - 18 + bob, 12, 2))
    pygame.draw.rect(screen, skin, (sx + 2, sy - 10 + bob, 16, 12))
    pygame.draw.rect(screen, (40, 30, 20), (sx + 4,  sy - 7 + bob, 3, 3))
    pygame.draw.rect(screen, (40, 30, 20), (sx + 11, sy - 7 + bob, 3, 3))
    txt = font.render("~", True, (240, 120, 30))
    screen.blit(txt, (sx + 6, sy - 28 + bob))


def draw_npc_monk(screen, sx, sy, npc):
    bob = int(npc._bob_offset)
    c = getattr(npc, 'clothing', {})
    body = c.get('body', (210, 130, 40))
    skin = c.get('skin', (240, 200, 150))
    fold = tuple(max(0, v - 35) for v in body)
    pygame.draw.rect(screen, body, (sx, sy + bob, 20, 18))
    pygame.draw.rect(screen, fold, (sx + 8, sy + bob, 5, 18))
    pygame.draw.rect(screen, skin, (sx + 2, sy - 10 + bob, 16, 12))
    pygame.draw.rect(screen, (40, 30, 20), (sx + 4,  sy - 7 + bob, 3, 3))
    pygame.draw.rect(screen, (40, 30, 20), (sx + 11, sy - 7 + bob, 3, 3))
    gx, gy = sx + 10, sy - 22 + bob
    for dx, dy in ((0, -5), (0, 5), (-5, 0), (5, 0)):
        pygame.draw.line(screen, (240, 220, 100), (gx, gy), (gx + dx, gy + dy), 2)
    pygame.draw.circle(screen, (255, 240, 130), (gx, gy), 2)


def draw_npc_leader(screen, sx, sy, npc):
    bob   = int(npc._bob_offset)
    lc    = getattr(npc, 'leader_color', (140, 30, 40))
    ptype = getattr(npc, 'palace_type',  'castle')

    def _dim(c, f=0.55):  return tuple(int(v * f) for v in c)
    def _lite(c, amt=60): return tuple(min(255, v + amt) for v in c)
    def _gold():          return (218, 175, 40)

    def _head(skin=(255, 210, 155), beard=True):
        pygame.draw.rect(screen, skin, (sx + 2, sy - 12 + bob, 16, 13))
        if beard:
            shadow = tuple(int(v * 0.78) for v in skin)
            pygame.draw.rect(screen, shadow, (sx + 3, sy - 4 + bob, 14, 5))
        pygame.draw.rect(screen, (35, 25, 15), (sx + 4,  sy - 10 + bob, 3, 3))
        pygame.draw.rect(screen, (35, 25, 15), (sx + 11, sy - 10 + bob, 3, 3))
        pygame.draw.rect(screen, (255, 255, 255), (sx + 5,  sy - 10 + bob, 1, 1))
        pygame.draw.rect(screen, (255, 255, 255), (sx + 12, sy - 10 + bob, 1, 1))

    def _star():
        screen.blit(_get_crown_font().render("★", True, _gold()), (sx + 6, sy - 32 + bob))

    if ptype == "mediterranean":
        toga = (245, 240, 225)
        pygame.draw.rect(screen, toga,   (sx + 1, sy + bob,      18, 20))
        pygame.draw.rect(screen, _gold(), (sx + 1, sy + bob,       2, 20))
        pygame.draw.rect(screen, lc,     (sx + 8, sy + 4 + bob,   4, 4))
        _head(skin=(240, 205, 160))
        crown_y = sy - 17 + bob
        for gx in range(sx + 2, sx + 18, 3):
            pygame.draw.rect(screen, (80, 140, 55),  (gx, crown_y,     2, 5))
            pygame.draw.rect(screen, (60, 110, 40),  (gx, crown_y,     2, 2))
        pygame.draw.rect(screen, (120, 100, 60), (sx - 2, sy - 14 + bob, 2, 32))
        pygame.draw.rect(screen, (80, 140, 55),  (sx - 4, sy - 17 + bob, 6, 4))

    elif ptype == "east_asian":
        silk = _dim(lc, 0.75)
        pale = _lite(lc, 80)
        pygame.draw.rect(screen, silk, (sx,      sy + bob,      20, 20))
        pygame.draw.rect(screen, pale, (sx - 3,  sy + 2 + bob,   7, 10))
        pygame.draw.rect(screen, pale, (sx + 16, sy + 2 + bob,   7, 10))
        for ey in range(0, 18, 3):
            pygame.draw.rect(screen, _gold(), (sx + 9, sy + ey + bob, 2, 2))
        _head(skin=(240, 200, 155))
        crown_y = sy - 23 + bob
        pygame.draw.rect(screen, (20, 20, 20),  (sx + 2, crown_y + 6, 16, 5))
        pygame.draw.rect(screen, (20, 20, 20),  (sx,     crown_y,     20, 3))
        pygame.draw.rect(screen, _gold(),        (sx + 2, crown_y + 6, 16, 2))
        pygame.draw.rect(screen, (130, 100, 60), (sx + 21, sy - 14 + bob, 2, 32))
        pygame.draw.rect(screen, (70, 180, 120), (sx + 19, sy - 18 + bob, 6, 6))

    elif ptype == "south_asian":
        sherwani = _dim(lc, 0.8)
        bright   = _lite(lc, 60)
        pygame.draw.rect(screen, sherwani, (sx + 1, sy + bob,       18, 20))
        pygame.draw.rect(screen, _gold(),   (sx + 1, sy + 3 + bob,   18, 2))
        pygame.draw.rect(screen, _gold(),   (sx + 1, sy + 7 + bob,   18, 2))
        pygame.draw.rect(screen, bright,    (sx + 1, sy + 11 + bob,  18, 3))
        _head(skin=(180, 130, 80))
        crown_y = sy - 22 + bob
        for i in range(4):
            bc = bright if i % 2 == 0 else sherwani
            pygame.draw.rect(screen, bc, (sx + 2, crown_y + i * 3, 16, 3))
        pygame.draw.rect(screen, (220, 60, 60), (sx + 8, crown_y + 2, 4, 4))
        pygame.draw.rect(screen, _gold(),        (sx + 7, crown_y + 1, 6, 1))
        pygame.draw.rect(screen, (140, 115, 50), (sx + 21, sy - 14 + bob, 2, 30))
        pygame.draw.rect(screen, _gold(),         (sx + 19, sy - 16 + bob, 6, 5))
        for mx in (sx + 19, sx + 21, sx + 23):
            pygame.draw.rect(screen, _gold(), (mx, sy - 20 + bob, 2, 5))

    elif ptype == "italian":
        doublet = _dim(lc, 0.8)
        slash   = _lite(lc, 80)
        pygame.draw.rect(screen, doublet, (sx + 1, sy + bob,      18, 20))
        for i in range(3):
            pygame.draw.rect(screen, slash, (sx + 1, sy + 2 + i * 5 + bob, 18, 2))
        pygame.draw.rect(screen, _gold(), (sx + 2, sy + 1 + bob, 16, 2))
        _head(skin=(235, 195, 145))
        crown_y = sy - 20 + bob
        pygame.draw.rect(screen, lc, (sx + 1, crown_y + 3, 18, 5))
        pygame.draw.rect(screen, lc, (sx + 3, crown_y,     14, 6))
        for pi in range(5):
            pc = (200, 200, 200) if pi % 2 == 0 else _lite(lc, 40)
            pygame.draw.rect(screen, pc, (sx + 15 + pi, crown_y - pi * 2, 2, 5))
        for ri in range(14):
            pygame.draw.rect(screen, (160, 160, 175),
                             (sx + 20 + ri // 3, sy + 4 + ri + bob, 2, 2))
        pygame.draw.rect(screen, _gold(), (sx + 20, sy + 3 + bob, 6, 2))

    elif ptype == "moorish":
        djellaba = _dim(lc, 0.75)
        ovr      = _lite(lc, 50)
        pygame.draw.rect(screen, djellaba, (sx,      sy + bob,       20, 20))
        pygame.draw.rect(screen, _gold(),   (sx,      sy + bob,        2, 20))
        pygame.draw.rect(screen, _gold(),   (sx + 18, sy + bob,        2, 20))
        pygame.draw.rect(screen, ovr,       (sx + 2,  sy + 14 + bob,  16,  6))
        _head(skin=(175, 130, 85))
        crown_y = sy - 21 + bob
        pygame.draw.rect(screen, (245, 240, 230), (sx + 2, crown_y + 4, 16, 5))
        pygame.draw.rect(screen, (245, 240, 230), (sx + 4, crown_y,     12, 7))
        pygame.draw.rect(screen, _gold(),          (sx + 7, crown_y + 1,  6, 5))
        pygame.draw.rect(screen, (245, 240, 230),  (sx + 8, crown_y + 2,  5, 3))
        pygame.draw.rect(screen, (110, 85, 55), (sx - 2, sy - 14 + bob, 2, 32))
        pygame.draw.rect(screen, _gold(),        (sx - 4, sy - 16 + bob, 6, 4))
        for si in range(3):
            pygame.draw.rect(screen, lc, (sx - 3 + si * 2, sy - 18 + bob, 2, 3))

    elif ptype == "middle_eastern":
        robe = _dim(lc, 0.7)
        sash = _lite(lc, 70)
        pygame.draw.rect(screen, robe,  (sx + 1, sy + bob,       18, 20))
        pygame.draw.rect(screen, sash,  (sx + 1, sy + 9 + bob,   18,  4))
        pygame.draw.rect(screen, _gold(),(sx + 1, sy + 17 + bob,  18,  3))
        _head(skin=(190, 145, 95))
        crown_y = sy - 22 + bob
        pygame.draw.rect(screen, (245, 240, 230), (sx + 1, crown_y + 3, 18, 7))
        pygame.draw.rect(screen, (245, 240, 230), (sx + 3, crown_y,     14, 5))
        pygame.draw.rect(screen, (20, 20, 20),    (sx + 2, crown_y + 4, 16, 2))
        pygame.draw.rect(screen, _gold(),          (sx + 2, crown_y + 3, 16, 2))
        pygame.draw.rect(screen, (150, 145, 160), (sx + 21, sy + 6 + bob,  2, 10))
        pygame.draw.rect(screen, _gold(),           (sx + 19, sy + 5 + bob,  6,  3))
        pygame.draw.rect(screen, (220, 60, 60),     (sx + 20, sy + 4 + bob,  4,  3))

    elif ptype == "norse":
        cloak = _dim(lc, 0.75)
        fur   = (200, 190, 170)
        pygame.draw.rect(screen, cloak, (sx, sy + bob,       20, 20))
        pygame.draw.rect(screen, fur,   (sx, sy + bob,       20,  4))
        pygame.draw.rect(screen, fur,   (sx, sy + 16 + bob,  20,  4))
        pygame.draw.rect(screen, _gold(),(sx + 8, sy + 2 + bob, 4, 4))
        _head(skin=(240, 200, 155))
        crown_y = sy - 21 + bob
        helm = (80, 80, 90)
        pygame.draw.rect(screen, helm, (sx + 2, crown_y + 3, 16,  6))
        pygame.draw.rect(screen, helm, (sx + 1, crown_y + 7, 18,  3))
        pygame.draw.rect(screen, helm, (sx + 8, crown_y + 6,  4,  6))
        ivory = (230, 215, 180)
        pygame.draw.rect(screen, ivory, (sx,      crown_y,     3,  8))
        pygame.draw.rect(screen, ivory, (sx + 17, crown_y,     3,  8))
        pygame.draw.rect(screen, ivory, (sx - 1,  crown_y + 2, 3,  4))
        pygame.draw.rect(screen, ivory, (sx + 18, crown_y + 2, 3,  4))
        pygame.draw.rect(screen, (130, 105, 70),  (sx + 21, sy - 10 + bob, 2, 28))
        pygame.draw.rect(screen, (140, 140, 155), (sx + 19, sy - 14 + bob, 8,  6))
        pygame.draw.rect(screen, (140, 140, 155), (sx + 21, sy - 17 + bob, 4,  5))

    elif ptype == "gothic":
        dark   = _dim(lc, 0.5)
        edge   = _lite(lc, 30)
        silver = (180, 180, 195)
        pygame.draw.rect(screen, dark,   (sx + 1, sy + bob,       18, 20))
        for i in range(0, 18, 4):
            pygame.draw.rect(screen, edge, (sx + 1 + i, sy + 15 + bob, 3, 5))
        pygame.draw.rect(screen, silver, (sx + 1, sy + bob,       18, 2))
        pygame.draw.rect(screen, silver, (sx + 1, sy + 10 + bob,  18, 2))
        pygame.draw.rect(screen, (240, 238, 232), (sx + 3, sy - 2 + bob, 14, 5))
        for spot_x in (sx + 5, sx + 9, sx + 13):
            pygame.draw.rect(screen, (30, 25, 20), (spot_x, sy - 1 + bob, 2, 2))
        _head(skin=(220, 185, 140))
        crown_y = sy - 26 + bob
        pygame.draw.rect(screen, _gold(), (sx + 3,  crown_y + 8, 14, 4))
        pygame.draw.rect(screen, _gold(), (sx + 4,  crown_y + 4,  4, 6))
        pygame.draw.rect(screen, _gold(), (sx + 8,  crown_y,      4, 10))
        pygame.draw.rect(screen, _gold(), (sx + 13, crown_y + 4,  4,  6))
        pygame.draw.rect(screen, lc,      (sx + 9,  crown_y + 1,  2,  3))
        crystal = _lite(lc, 100)
        pygame.draw.rect(screen, (60, 55, 70),   (sx + 21, sy - 14 + bob, 2, 32))
        pygame.draw.rect(screen, crystal,         (sx + 19, sy - 20 + bob, 6,  8))
        pygame.draw.rect(screen, (255, 255, 255), (sx + 21, sy - 19 + bob, 2,  2))

    elif ptype == "african":
        base = _dim(lc, 0.75)
        pat1 = _lite(lc, 70)
        pat2 = (220, 180, 40)
        pygame.draw.rect(screen, base,  (sx, sy + bob,  20, 20))
        for row in range(0, 18, 4):
            for col in range(0, 18, 4):
                c2 = pat1 if (row + col) % 8 == 0 else pat2
                pygame.draw.rect(screen, c2, (sx + col, sy + row + bob, 2, 2))
        pygame.draw.rect(screen, pat1, (sx - 2, sy + bob,       5, 8))
        pygame.draw.rect(screen, pat1, (sx + 17, sy + bob,      5, 8))
        _head(skin=(100, 65, 35), beard=False)
        crown_y = sy - 28 + bob
        pygame.draw.rect(screen, lc,   (sx + 3, crown_y + 4,  14, 12))
        pygame.draw.rect(screen, pat2,  (sx + 3, crown_y + 4,  14,  2))
        pygame.draw.rect(screen, pat2,  (sx + 3, crown_y + 12, 14,  2))
        for fi in range(5):
            fc = pat1 if fi % 2 == 0 else pat2
            pygame.draw.rect(screen, fc, (sx + 3 + fi * 3, crown_y, 2, 6))
        pygame.draw.rect(screen, (100, 75, 45), (sx + 22, sy - 12 + bob, 2, 30))
        pygame.draw.rect(screen, pat2,           (sx + 20, sy - 16 + bob, 6,  5))
        pygame.draw.rect(screen, (100, 75, 45),  (sx + 21, sy - 19 + bob, 4,  5))

    elif ptype == "byzantine":
        brocade = _dim(lc, 0.72)
        pygame.draw.rect(screen, brocade, (sx + 1, sy + bob, 18, 20))
        for li in range(7):
            pygame.draw.rect(screen, _gold(),
                             (sx + 1 + li * 2, sy + li * 2 + bob, 3, 3))
            pygame.draw.rect(screen, (220, 60, 60),
                             (sx + 2 + li * 2, sy + li * 2 + 1 + bob, 2, 1))
        for cx2 in (sx + 5, sx + 12):
            pygame.draw.rect(screen, _gold(), (cx2,     sy + 10 + bob, 4, 1))
            pygame.draw.rect(screen, _gold(), (cx2 + 1, sy + 8 + bob,  2, 5))
        pygame.draw.rect(screen, (240, 238, 232), (sx + 3, sy - 2 + bob, 14, 5))
        for spot_x in (sx + 5, sx + 9, sx + 13):
            pygame.draw.rect(screen, (30, 25, 20), (spot_x, sy - 1 + bob, 2, 2))
        _head(skin=(210, 170, 120))
        crown_y = sy - 18 + bob
        pygame.draw.rect(screen, _gold(), (sx + 2, crown_y, 16, 5))
        for gx in (sx + 3, sx + 7, sx + 11, sx + 15):
            pygame.draw.rect(screen, lc,           (gx,     crown_y - 1, 3, 4))
            pygame.draw.rect(screen, (220, 60, 60),(gx + 1, crown_y,     1, 2))
        pygame.draw.circle(screen, _gold(), (sx - 2, sy + 4 + bob), 5)
        pygame.draw.rect(screen,  _gold(),  (sx - 3, sy + 1 + bob, 2, 8))
        pygame.draw.rect(screen,  _gold(),  (sx - 5, sy + 4 + bob, 6, 2))
        sceptre_x = sx + 21
        pygame.draw.rect(screen, (160, 130, 50), (sceptre_x,     sy - 14 + bob, 2, 32))
        pygame.draw.rect(screen, _gold(),         (sceptre_x - 1, sy - 18 + bob, 4,  5))
        pygame.draw.circle(screen, _gold(),       (sceptre_x,     sy - 20 + bob), 4)
        pygame.draw.circle(screen, lc,            (sceptre_x,     sy - 20 + bob), 2)

    elif ptype == "tibetan":
        inner = (215, 140, 30)
        outer = _dim(lc, 0.7)
        pygame.draw.rect(screen, inner, (sx + 2, sy + bob,  16, 20))
        pygame.draw.rect(screen, outer, (sx,     sy + bob,   8, 20))
        pygame.draw.rect(screen, outer, (sx,     sy + bob,  20,  5))
        pygame.draw.rect(screen, _gold(),(sx,    sy + 4 + bob, 20, 2))
        _head(skin=(175, 135, 90), beard=False)
        crown_y  = sy - 28 + bob
        hat_col  = (210, 175, 20)
        pygame.draw.rect(screen, hat_col, (sx + 4, crown_y + 6, 12, 10))
        pygame.draw.rect(screen, hat_col, (sx + 6, crown_y,      8,  9))
        pygame.draw.rect(screen, hat_col, (sx + 7, crown_y - 3,  6,  5))
        pygame.draw.rect(screen, _gold(),  (sx + 4, crown_y + 6, 12,  2))
        dorje = (180, 155, 50)
        pygame.draw.rect(screen, (130, 105, 65), (sx - 2, sy - 12 + bob, 2, 30))
        pygame.draw.rect(screen, dorje,           (sx - 4, sy - 16 + bob, 6,  3))
        for di in (sx - 3, sx - 1, sx + 1):
            pygame.draw.rect(screen, dorje, (di, sy - 19 + bob, 2, 4))

    elif ptype in ("chinese", "tang_imperial", "song_palace", "han_palace"):
        imperial = (230, 185, 30)
        crimson  = (180, 35, 35)
        jade     = (60, 160, 100)
        pygame.draw.rect(screen, imperial, (sx,      sy + bob,       20, 20))
        pygame.draw.rect(screen, imperial, (sx - 5,  sy + 2 + bob,    7, 12))
        pygame.draw.rect(screen, imperial, (sx + 18, sy + 2 + bob,    7, 12))
        pygame.draw.rect(screen, crimson,  (sx + 8,  sy + bob,        4, 20))
        pygame.draw.rect(screen, _gold(),  (sx,      sy + 5 + bob,   20,  2))
        pygame.draw.rect(screen, _gold(),  (sx,      sy + 13 + bob,  20,  2))
        pygame.draw.rect(screen, crimson,  (sx + 4,  sy + 7 + bob,   12,  2))
        pygame.draw.rect(screen, crimson,  (sx + 9,  sy + 4 + bob,    2,  8))
        _head(skin=(240, 200, 150), beard=False)
        crown_y = sy - 26 + bob
        board_col = (20, 18, 15)
        pygame.draw.rect(screen, board_col, (sx,      crown_y,       20,  3))
        pygame.draw.rect(screen, board_col, (sx + 2,  crown_y + 3,   16,  7))
        pygame.draw.rect(screen, _gold(),   (sx + 2,  crown_y + 3,   16,  2))
        for bx in (sx + 1, sx + 4, sx + 7, sx + 10, sx + 13, sx + 16, sx + 19):
            for by in range(crown_y + 1, crown_y + 3, 1):
                pygame.draw.rect(screen, jade, (bx, by, 1, 1))
        for mx in (sx + 5, sx + 10, sx + 15):
            pygame.draw.rect(screen, jade, (mx, crown_y + 4, 2, 2))
        pygame.draw.rect(screen, (140, 110, 45), (sx + 21, sy - 14 + bob, 2, 30))
        pygame.draw.rect(screen, jade,            (sx + 19, sy - 18 + bob, 6,  5))
        pygame.draw.rect(screen, jade,            (sx + 19, sy - 16 + bob, 3,  3))

    elif ptype == "japanese":
        kimono = _dim(lc, 0.65)
        ivory  = (235, 225, 200)
        pygame.draw.rect(screen, kimono, (sx + 1, sy + bob,       18, 20))
        pygame.draw.rect(screen, ivory,  (sx + 3, sy + bob,        5, 12))
        pygame.draw.rect(screen, ivory,  (sx + 12, sy + bob,       5, 12))
        pygame.draw.rect(screen, ivory,  (sx + 6,  sy + bob,       8,  5))
        pygame.draw.rect(screen, (35, 30, 45), (sx + 1, sy + 12 + bob, 18, 8))
        pygame.draw.circle(screen, _gold(), (sx + 10, sy + 7 + bob), 4)
        pygame.draw.circle(screen, kimono,  (sx + 10, sy + 7 + bob), 2)
        _head(skin=(240, 200, 155))
        crown_y  = sy - 25 + bob
        helm_col = (30, 25, 30)
        pygame.draw.rect(screen, helm_col, (sx + 2, crown_y + 4,  16, 9))
        pygame.draw.rect(screen, helm_col, (sx + 1, crown_y + 11, 18, 3))
        pygame.draw.rect(screen, _gold(),   (sx + 2, crown_y + 4,  16, 2))
        pygame.draw.rect(screen, helm_col, (sx + 7, crown_y,       6, 6))
        pygame.draw.rect(screen, _gold(), (sx + 6,  crown_y - 2, 2, 5))
        pygame.draw.rect(screen, _gold(), (sx + 12, crown_y - 2, 2, 5))
        pygame.draw.rect(screen, _gold(), (sx + 8,  crown_y - 3, 4, 2))
        pygame.draw.rect(screen, (80, 60, 40),  (sx + 21, sy - 10 + bob, 2, 28))
        pygame.draw.rect(screen, (200, 185, 95), (sx + 21, sy - 14 + bob, 2,  6))
        pygame.draw.rect(screen, _gold(),         (sx + 19, sy - 11 + bob, 6,  2))

    else:
        robe   = _dim(lc, 0.7)
        trim   = lc
        mantle = _lite(lc, 40)
        pygame.draw.rect(screen, robe,    (sx + 1,  sy + bob,       18, 20))
        pygame.draw.rect(screen, mantle,  (sx,      sy + bob,        5, 14))
        pygame.draw.rect(screen, mantle,  (sx + 15, sy + bob,        5, 14))
        pygame.draw.rect(screen, _gold(),  (sx + 1,  sy + 11 + bob, 18,  3))
        for i in range(0, 18, 4):
            pygame.draw.rect(screen, trim, (sx + 1 + i, sy + 17 + bob, 2, 3))
        pygame.draw.rect(screen, (240, 238, 232), (sx + 3, sy - 2 + bob, 14, 6))
        for spot_x in (sx + 5, sx + 9, sx + 13):
            pygame.draw.rect(screen, (30, 25, 20), (spot_x, sy - 1 + bob, 2, 2))
        _head()
        crown_y = sy - 20 + bob
        pygame.draw.rect(screen, _gold(), (sx + 3,  crown_y + 3, 14, 5))
        pygame.draw.rect(screen, _gold(), (sx + 3,  crown_y,      3, 7))
        pygame.draw.rect(screen, _gold(), (sx + 8,  crown_y - 2,  4, 9))
        pygame.draw.rect(screen, _gold(), (sx + 14, crown_y,      3, 7))
        pygame.draw.rect(screen, trim,    (sx + 9,  crown_y,      2, 3))
        pygame.draw.rect(screen, (80, 200, 220), (sx + 4,  crown_y + 1, 2, 2))
        pygame.draw.rect(screen, (80, 200, 220), (sx + 14, crown_y + 1, 2, 2))
        pygame.draw.rect(screen, _lite(_gold(), 30), (sx + 3, crown_y + 3, 14, 2))
        sceptre_x = sx + 18
        pygame.draw.rect(screen, (160, 130, 50), (sceptre_x,      sy - 14 + bob, 3, 32))
        pygame.draw.rect(screen, _gold(),          (sceptre_x - 1, sy - 18 + bob, 5,  5))
        pygame.draw.circle(screen, _gold(),        (sceptre_x + 1, sy - 20 + bob), 4)
        pygame.draw.circle(screen, trim,           (sceptre_x + 1, sy - 20 + bob), 2)

    _star()


def draw_npc_farmer(screen, sx, sy, npc):
    bob = int(npc._bob_offset)
    facing = getattr(npc, 'facing', 1)
    c = getattr(npc, 'clothing', {})
    body  = c.get('body',  (175, 135, 85))
    trim  = c.get('trim',  (110,  75, 35))
    skin  = c.get('skin',  (230, 185, 135))
    hat   = c.get('hat',   (200, 175, 80))
    pygame.draw.rect(screen, body,  (sx, sy + bob, 20, 18))
    pygame.draw.rect(screen, trim,  (sx + 7,  sy + bob, 3, 18))
    pygame.draw.rect(screen, trim,  (sx + 12, sy + bob, 3, 18))
    pygame.draw.rect(screen, skin,  (sx + 2, sy - 10 + bob, 16, 12))
    pygame.draw.rect(screen, (40, 30, 20), (sx + 4,  sy - 7 + bob, 3, 3))
    pygame.draw.rect(screen, (40, 30, 20), (sx + 11, sy - 7 + bob, 3, 3))
    hat_dark = tuple(max(0, v - 25) for v in hat)
    brim_x = sx - 3 if facing == 1 else sx - 1
    pygame.draw.rect(screen, hat,      (brim_x, sy - 14 + bob, 26, 3))
    pygame.draw.rect(screen, hat,      (sx + 3, sy - 20 + bob, 14, 8))
    pygame.draw.rect(screen, hat_dark, (sx + 3, sy - 14 + bob, 14, 2))


def draw_npc_villager(screen, sx, sy, npc):
    bob = int(npc._bob_offset)
    facing = getattr(npc, 'facing', 1)
    c = getattr(npc, 'clothing', {})
    body  = c.get('body', (100, 125, 80))
    trim  = c.get('trim', (110,  75, 35))
    skin  = c.get('skin', (255, 215, 160))
    pygame.draw.rect(screen, body, (sx, sy + bob, 20, 18))
    collar = tuple(min(255, v + 100) for v in trim)
    pygame.draw.rect(screen, collar, (sx + 7, sy + bob, 6, 7))
    pygame.draw.rect(screen, skin, (sx + 2, sy - 10 + bob, 16, 12))
    pygame.draw.rect(screen, (40, 30, 20), (sx + 4,  sy - 7 + bob, 3, 3))
    pygame.draw.rect(screen, (40, 30, 20), (sx + 11, sy - 7 + bob, 3, 3))
    bx_off = 18 if facing == 1 else -6
    basket = tuple(min(255, v + 60) for v in trim)
    pygame.draw.rect(screen, basket, (sx + bx_off, sy + 4 + bob, 6, 5))
    pygame.draw.rect(screen, trim,   (sx + bx_off, sy + 4 + bob, 6, 1))


def draw_npc_child(screen, sx, sy, npc):
    bob = int(npc._bob_offset)
    c = getattr(npc, 'clothing', {})
    body = c.get('body', (200, 70, 70))
    leg  = c.get('leg',  (80, 60, 120))
    skin = c.get('skin', (255, 210, 160))
    w = npc.NPC_W
    pygame.draw.rect(screen, body, (sx, sy + bob, w, 11))
    pygame.draw.rect(screen, leg,  (sx + 1, sy + 11 + bob, w - 2, 9))
    pygame.draw.rect(screen, skin, (sx + 1, sy - 12 + bob, 12, 13))
    pygame.draw.rect(screen, (40, 30, 20), (sx + 2, sy - 9 + bob, 3, 4))
    pygame.draw.rect(screen, (40, 30, 20), (sx + 8, sy - 9 + bob, 3, 4))
    pygame.draw.circle(screen, (230, 150, 140), (sx + 3,  sy - 4 + bob), 2)
    pygame.draw.circle(screen, (230, 150, 140), (sx + 10, sy - 4 + bob), 2)
