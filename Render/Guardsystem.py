import pygame


_HELMET_FINISH_COLORS = {
    'bronze':         (180, 130, 70),
    'blackened':      (35, 35, 45),
    'burnished':      (200, 200, 210),
    'gilded':         (215, 175, 65),
    'rusted':         (140, 80, 50),
    'tarnished':      (115, 120, 110),
    'ivory':          (230, 220, 195),
    'lacquered_red':  (140, 35, 35),
    'lacquered_black':(20, 18, 28),
    'patina':         (95, 165, 150),
    'frost':          (210, 225, 235),
    'verdigris':      (110, 175, 130),
    'sooted':         (55, 50, 50),
    'silvered':       (220, 225, 235),
    'copper':         (190, 110, 60),
    'inlaid':         (170, 165, 130),
    'enameled_blue':  (45, 75, 165),
    'enameled_green': (40, 130, 70),
    'enameled_white': (235, 235, 240),
    'oiled':          (60, 55, 50),
    'pitted':         (105, 100, 95),
    'damascened':     (135, 130, 125),
    'horsehair':      (75, 60, 45),
    'brass':          (200, 165, 75),
    'obsidian':       (25, 25, 35),
    'moonstone':      (220, 225, 240),
    'crimson_enamel': (155, 30, 35),
    'cobalt':         (40, 60, 140),
    'midnight':       (25, 30, 55),
    'blooded':        (115, 45, 45),
    'weathered':      (130, 125, 110),
    'polished_iron':  (180, 185, 195),
    'quenched':       (45, 55, 75),
    'nickeled':       (215, 220, 225),
    'pewter':         (140, 140, 145),
    'tin':            (190, 195, 200),
    'mercury':        (175, 180, 200),
    'opal':           (230, 215, 220),
    'ember':          (200, 90, 50),
    'ash_gray':       (160, 155, 150),
    'shadowed':       (50, 40, 70),
    'mossed':         (110, 125, 80),
    'bone':           (225, 215, 185),
    'coal':           (20, 20, 20),
    'iridescent':     (120, 95, 165),
    'saffron':        (215, 175, 70),
    'ruby_inlay':     (155, 50, 65),
    'jade':           (110, 165, 130),
}


def _guard_helmet_color(finish, armor):
    col = _HELMET_FINISH_COLORS.get(finish)
    if col is not None:
        return col
    return tuple(min(255, v + 10) for v in armor)


def _draw_guard_tabard(screen, sx, sy, tabard, trim, plate, armor):
    if tabard == 'solid':
        return
    if tabard == 'vertical_split':
        half = tuple(max(0, min(255, v + 40)) for v in trim)
        pygame.draw.rect(screen, half, (sx, sy, 10, 16))
        pygame.draw.rect(screen, trim, (sx + 10, sy, 10, 16))
    elif tabard == 'quartered':
        a = trim
        b = tuple(min(255, v + 60) for v in trim)
        pygame.draw.rect(screen, a, (sx,      sy,      10, 8))
        pygame.draw.rect(screen, b, (sx + 10, sy,      10, 8))
        pygame.draw.rect(screen, b, (sx,      sy + 8,  10, 8))
        pygame.draw.rect(screen, a, (sx + 10, sy + 8,  10, 8))
    elif tabard == 'horizontal_band':
        pygame.draw.rect(screen, trim, (sx, sy + 6, 20, 5))
    elif tabard == 'diagonal_split':
        for i in range(16):
            w = min(20, 4 + i)
            pygame.draw.rect(screen, trim, (sx, sy + i, w, 1))
    elif tabard == 'checkered':
        a = trim
        b = tuple(min(255, v + 60) for v in trim)
        for row in range(4):
            for col in range(4):
                col_a = a if (row + col) % 2 == 0 else b
                pygame.draw.rect(screen, col_a, (sx + col * 5, sy + row * 4, 5, 4))
    elif tabard == 'diamond':
        pygame.draw.polygon(screen, trim,
                            [(sx + 10, sy + 2), (sx + 16, sy + 8),
                             (sx + 10, sy + 14), (sx + 4, sy + 8)])
    elif tabard == 'pale':
        pygame.draw.rect(screen, trim, (sx + 7, sy, 6, 16))
    elif tabard == 'cross':
        pygame.draw.rect(screen, trim, (sx + 8, sy, 4, 16))
        pygame.draw.rect(screen, trim, (sx, sy + 6, 20, 4))
    elif tabard == 'saltire':
        for i in range(16):
            x = sx + i if i < 20 else sx + 19
            pygame.draw.rect(screen, trim, (sx + i + 2, sy + i, 2, 1))
            pygame.draw.rect(screen, trim, (sx + 18 - i, sy + i, 2, 1))
    elif tabard == 'lozenge':
        for row in range(4):
            for col in range(4):
                if (row + col) % 2 == 0:
                    pygame.draw.polygon(screen, trim,
                                        [(sx + col * 5 + 2, sy + row * 4),
                                         (sx + col * 5 + 5, sy + row * 4 + 2),
                                         (sx + col * 5 + 2, sy + row * 4 + 4),
                                         (sx + col * 5,     sy + row * 4 + 2)])
    elif tabard == 'bordered':
        pygame.draw.rect(screen, trim, (sx, sy, 20, 2))
        pygame.draw.rect(screen, trim, (sx, sy + 14, 20, 2))
        pygame.draw.rect(screen, trim, (sx, sy, 2, 16))
        pygame.draw.rect(screen, trim, (sx + 18, sy, 2, 16))
    elif tabard == 'chevron_pattern':
        for i in range(4):
            y = sy + i * 4
            pygame.draw.polygon(screen, trim,
                                [(sx + 1, y + 3),
                                 (sx + 10, y),
                                 (sx + 19, y + 3),
                                 (sx + 19, y + 4),
                                 (sx + 10, y + 1),
                                 (sx + 1, y + 4)])
    elif tabard == 'stripes':
        for i in range(0, 16, 4):
            pygame.draw.rect(screen, trim, (sx, sy + i, 20, 2))
    elif tabard == 'starred':
        pygame.draw.rect(screen, trim, (sx + 9, sy + 6, 2, 1))
        pygame.draw.rect(screen, trim, (sx + 8, sy + 7, 4, 1))
        pygame.draw.rect(screen, trim, (sx + 7, sy + 8, 6, 1))
        pygame.draw.rect(screen, trim, (sx + 8, sy + 9, 4, 1))
        pygame.draw.rect(screen, trim, (sx + 9, sy + 10, 2, 1))
        pygame.draw.rect(screen, trim, (sx + 3, sy + 3, 1, 1))
        pygame.draw.rect(screen, trim, (sx + 16, sy + 3, 1, 1))
        pygame.draw.rect(screen, trim, (sx + 3, sy + 13, 1, 1))
        pygame.draw.rect(screen, trim, (sx + 16, sy + 13, 1, 1))


def _draw_guard_back_gear(screen, sx, sy, kit, trim, plate, facing):
    back_x = sx - 2 if facing == 1 else sx + 17
    if kit == 'archer':
        pygame.draw.rect(screen, (90, 60, 30),    (back_x, sy - 4, 5, 18))
        pygame.draw.rect(screen, (210, 210, 200), (back_x + 1, sy - 8, 1, 4))
        pygame.draw.rect(screen, trim,            (back_x + 3, sy - 8, 1, 4))
    elif kit == 'crossbowman':
        pouch_x = sx + 16 if facing == 1 else sx - 2
        pygame.draw.rect(screen, (95, 70, 40), (pouch_x, sy + 8, 6, 7))
        pygame.draw.rect(screen, (60, 45, 25), (pouch_x, sy + 8, 6, 1))
    elif kit in ('swordsman', 'captain', 'dao_swordsman', 'jian_swordsman',
                 'claymore_bearer', 'falchion_bearer',
                 'flamberge_bearer', 'estoc_bearer'):
        scab_x = sx - 3 if facing == 1 else sx + 18
        pygame.draw.rect(screen, (75, 55, 30), (scab_x, sy + 4, 2, 14))
        pygame.draw.rect(screen, plate,        (scab_x, sy + 16, 2, 2))
    elif kit == 'katana_samurai':
        # Katana worn at the hip, edge-up (bushi style)
        scab_x = sx - 4 if facing == 1 else sx + 18
        pygame.draw.rect(screen, (30, 25, 35), (scab_x, sy + 2, 2, 16))
        pygame.draw.rect(screen, (190, 165, 55), (scab_x, sy + 16, 2, 2))
    elif kit == 'watchman':
        lan_x = sx - 4 if facing == 1 else sx + 19
        pygame.draw.rect(screen, (90, 70, 35),    (lan_x, sy + 2, 5, 7))
        pygame.draw.rect(screen, (255, 220, 130), (lan_x + 1, sy + 3, 3, 5))
        pygame.draw.rect(screen, (60, 45, 25),    (lan_x + 1, sy,    3, 2))


def _draw_guard_cape(screen, sx, sy, cape, trim, armor, facing):
    if cape == 'none':
        return
    if cape == 'trim':
        col = trim
    elif cape == 'fur':
        col = (95, 75, 50)
    elif cape == 'royal':
        col = (95, 35, 110)
    elif cape == 'striped':
        col = trim
    elif cape == 'long':
        col = tuple(max(0, v - 35) for v in armor)
    elif cape == 'tattered':
        col = tuple(max(0, v - 40) for v in armor)
    elif cape == 'white':
        col = (225, 225, 230)
    elif cape == 'forest':
        col = (45, 80, 50)
    else:  # 'dark' / fallback
        col = tuple(max(0, v - 25) for v in armor)
    cape_x = sx - 3 if facing == 1 else sx + 17
    length = 22 if cape == 'long' else 16
    pygame.draw.polygon(screen, col,
                        [(cape_x, sy),
                         (cape_x + 6, sy),
                         (cape_x + 4, sy + length),
                         (cape_x + 1, sy + length)])
    if cape == 'fur':
        for i in range(4):
            pygame.draw.rect(screen, (140, 115, 80),
                             (cape_x, sy + i * 4, 6, 1))
    elif cape == 'striped':
        stripe = tuple(min(255, v + 60) for v in trim)
        pygame.draw.rect(screen, stripe, (cape_x + 1, sy + 4, 4, 2))
        pygame.draw.rect(screen, stripe, (cape_x + 1, sy + 10, 4, 2))
    elif cape == 'royal':
        pygame.draw.rect(screen, (220, 195, 90),
                         (cape_x, sy, 6, 2))


def _draw_guard_emblem(screen, sx, sy, emblem, trim, plate):
    cx, cy = sx + 10, sy + 8
    if emblem == 'cross':
        pygame.draw.rect(screen, trim, (cx,     sy + 4, 1, 9))
        pygame.draw.rect(screen, trim, (cx - 2, sy + 7, 5, 1))
    elif emblem == 'star':
        pygame.draw.rect(screen, trim, (cx,     cy,     1, 1))
        pygame.draw.rect(screen, trim, (cx - 1, cy - 1, 3, 1))
        pygame.draw.rect(screen, trim, (cx - 1, cy + 1, 3, 1))
        pygame.draw.rect(screen, trim, (cx,     cy - 2, 1, 1))
        pygame.draw.rect(screen, trim, (cx,     cy + 2, 1, 1))
    elif emblem == 'circle':
        pygame.draw.circle(screen, trim, (cx, cy), 2, 1)
    elif emblem == 'chevron':
        pygame.draw.polygon(screen, trim,
                            [(cx - 2, sy + 9), (cx, sy + 6), (cx + 2, sy + 9),
                             (cx + 2, sy + 11), (cx, sy + 8), (cx - 2, sy + 11)])
    elif emblem == 'fleur':
        pygame.draw.rect(screen, trim, (cx, sy + 5, 1, 7))
        pygame.draw.rect(screen, trim, (cx - 2, sy + 6, 5, 1))
        pygame.draw.rect(screen, trim, (cx - 1, sy + 4, 3, 1))
        pygame.draw.rect(screen, trim, (cx - 2, sy + 9, 5, 1))
    elif emblem == 'anchor':
        pygame.draw.rect(screen, trim, (cx,     sy + 4, 1, 8))
        pygame.draw.rect(screen, trim, (cx - 1, sy + 5, 3, 1))
        pygame.draw.rect(screen, trim, (cx - 2, sy + 11, 5, 1))
        pygame.draw.rect(screen, trim, (cx - 2, sy + 10, 1, 2))
        pygame.draw.rect(screen, trim, (cx + 2, sy + 10, 1, 2))
    elif emblem == 'wing':
        pygame.draw.rect(screen, trim, (cx - 3, sy + 7, 7, 1))
        pygame.draw.rect(screen, trim, (cx - 2, sy + 6, 5, 1))
        pygame.draw.rect(screen, trim, (cx - 1, sy + 5, 3, 1))
        pygame.draw.rect(screen, trim, (cx - 2, sy + 8, 5, 1))
    elif emblem == 'eye':
        pygame.draw.rect(screen, plate, (cx - 2, sy + 7, 5, 2))
        pygame.draw.rect(screen, trim, (cx, sy + 7, 1, 2))
    elif emblem == 'sun':
        pygame.draw.rect(screen, trim, (cx - 1, sy + 6, 3, 3))
        pygame.draw.rect(screen, trim, (cx, sy + 4, 1, 1))
        pygame.draw.rect(screen, trim, (cx, sy + 10, 1, 1))
        pygame.draw.rect(screen, trim, (cx - 3, sy + 7, 1, 1))
        pygame.draw.rect(screen, trim, (cx + 3, sy + 7, 1, 1))
    elif emblem == 'moon':
        pygame.draw.rect(screen, trim, (cx - 1, sy + 5, 3, 5))
        pygame.draw.rect(screen, plate, (cx, sy + 5, 2, 5))
    elif emblem == 'lion':
        pygame.draw.rect(screen, trim, (cx - 2, sy + 6, 5, 3))
        pygame.draw.rect(screen, trim, (cx - 3, sy + 5, 2, 2))
        pygame.draw.rect(screen, trim, (cx + 2, sy + 5, 2, 2))
        pygame.draw.rect(screen, trim, (cx - 2, sy + 9, 1, 2))
        pygame.draw.rect(screen, trim, (cx + 2, sy + 9, 1, 2))
    elif emblem == 'wolf':
        pygame.draw.rect(screen, trim, (cx - 2, sy + 7, 5, 2))
        pygame.draw.rect(screen, trim, (cx - 3, sy + 6, 1, 1))
        pygame.draw.rect(screen, trim, (cx + 3, sy + 6, 1, 1))
        pygame.draw.rect(screen, trim, (cx - 1, sy + 9, 1, 1))
        pygame.draw.rect(screen, trim, (cx + 1, sy + 9, 1, 1))
    elif emblem == 'eagle':
        pygame.draw.rect(screen, trim, (cx, sy + 5, 1, 6))
        pygame.draw.rect(screen, trim, (cx - 3, sy + 6, 7, 1))
        pygame.draw.rect(screen, trim, (cx - 2, sy + 7, 5, 1))
        pygame.draw.rect(screen, trim, (cx - 1, sy + 4, 3, 1))
    elif emblem == 'crown':
        pygame.draw.rect(screen, trim, (cx - 3, sy + 8, 7, 2))
        pygame.draw.rect(screen, trim, (cx - 3, sy + 6, 1, 2))
        pygame.draw.rect(screen, trim, (cx, sy + 6, 1, 2))
        pygame.draw.rect(screen, trim, (cx + 3, sy + 6, 1, 2))
    elif emblem == 'tower':
        pygame.draw.rect(screen, trim, (cx - 2, sy + 6, 5, 6))
        pygame.draw.rect(screen, trim, (cx - 3, sy + 5, 1, 2))
        pygame.draw.rect(screen, trim, (cx - 1, sy + 5, 1, 2))
        pygame.draw.rect(screen, trim, (cx + 1, sy + 5, 1, 2))
        pygame.draw.rect(screen, trim, (cx + 3, sy + 5, 1, 2))
    elif emblem == 'oak':
        pygame.draw.rect(screen, trim, (cx - 1, sy + 5, 3, 3))
        pygame.draw.rect(screen, trim, (cx - 2, sy + 6, 1, 1))
        pygame.draw.rect(screen, trim, (cx + 2, sy + 6, 1, 1))
        pygame.draw.rect(screen, trim, (cx, sy + 8, 1, 4))
    elif emblem == 'serpent':
        pygame.draw.rect(screen, trim, (cx - 3, sy + 6, 2, 1))
        pygame.draw.rect(screen, trim, (cx - 1, sy + 7, 2, 1))
        pygame.draw.rect(screen, trim, (cx + 1, sy + 8, 2, 1))
        pygame.draw.rect(screen, trim, (cx - 1, sy + 9, 2, 1))
        pygame.draw.rect(screen, trim, (cx - 3, sy + 10, 2, 1))
    elif emblem == 'hammer':
        pygame.draw.rect(screen, trim, (cx - 2, sy + 5, 5, 3))
        pygame.draw.rect(screen, trim, (cx, sy + 8, 1, 5))
    elif emblem == 'key':
        pygame.draw.rect(screen, trim, (cx - 2, sy + 5, 3, 3))
        pygame.draw.rect(screen, plate, (cx - 1, sy + 6, 1, 1))
        pygame.draw.rect(screen, trim, (cx + 1, sy + 6, 4, 1))
        pygame.draw.rect(screen, trim, (cx + 3, sy + 7, 1, 1))
    elif emblem == 'fish':
        pygame.draw.polygon(screen, trim,
                            [(cx - 3, sy + 8),
                             (cx + 2, sy + 6),
                             (cx + 2, sy + 10)])
        pygame.draw.polygon(screen, trim,
                            [(cx + 2, sy + 8),
                             (cx + 4, sy + 6),
                             (cx + 4, sy + 10)])
    elif emblem == 'flame':
        pygame.draw.polygon(screen, trim,
                            [(cx,     sy + 4),
                             (cx + 2, sy + 8),
                             (cx,     sy + 12),
                             (cx - 2, sy + 8)])
        pygame.draw.rect(screen, plate, (cx, sy + 7, 1, 3))
    elif emblem == 'horn':
        pygame.draw.polygon(screen, trim,
                            [(cx - 3, sy + 9),
                             (cx + 2, sy + 5),
                             (cx + 3, sy + 6),
                             (cx - 2, sy + 11)])


def _draw_guard_helmet(screen, sx, sy, helmet, finish, armor, plate, trim, c, npc, facing):
    helm = _guard_helmet_color(finish, armor)
    skin = getattr(npc, 'skin_tone', None) or c.get('skin', (230, 195, 155))
    if helmet == 'pot':
        pygame.draw.rect(screen, helm,         (sx + 2, sy - 12, 16, 14))
        pygame.draw.rect(screen, (20, 20, 30), (sx + 3, sy - 8,  14, 3))
    elif helmet == 'kettle':
        pygame.draw.rect(screen, helm,         (sx + 3, sy - 10, 14, 9))
        pygame.draw.rect(screen, helm,         (sx,     sy - 6,  20, 2))
        pygame.draw.rect(screen, (20, 20, 30), (sx + 4, sy - 4,  12, 2))
        pygame.draw.rect(screen, skin,         (sx + 4, sy - 2,  12, 1))
    elif helmet == 'sallet':
        pygame.draw.rect(screen, helm,         (sx + 2, sy - 12, 16, 11))
        tail_x = sx + 17 if facing == -1 else sx - 1
        pygame.draw.polygon(screen, helm,
                            [(tail_x, sy - 10),
                             (tail_x + (3 if facing == -1 else -1), sy - 6),
                             (tail_x, sy - 4)])
        pygame.draw.rect(screen, (20, 20, 30), (sx + 3, sy - 7, 14, 2))
    elif helmet == 'plumed':
        pygame.draw.rect(screen, helm,         (sx + 2, sy - 12, 16, 14))
        pygame.draw.rect(screen, (20, 20, 30), (sx + 3, sy - 8,  14, 3))
        pygame.draw.rect(screen, plate,        (sx + 2, sy - 5,  16, 1))
        pygame.draw.rect(screen, trim,         (sx + 7, sy - 22, 6, 10))
        pygame.draw.rect(screen, trim,         (sx + 5, sy - 24, 10, 3))
    elif helmet == 'coif':
        mail = tuple(max(0, v - 10) for v in armor)
        pygame.draw.rect(screen, mail,         (sx + 1, sy - 13, 18, 13))
        pygame.draw.rect(screen, skin,         (sx + 4, sy - 9,  12, 8))
        pygame.draw.rect(screen, (40, 30, 20), (sx + 5, sy - 6,  3, 2))
        pygame.draw.rect(screen, (40, 30, 20), (sx + 12, sy - 6, 3, 2))
    elif helmet == 'horned':
        pygame.draw.rect(screen, helm,         (sx + 2, sy - 12, 16, 14))
        pygame.draw.rect(screen, (20, 20, 30), (sx + 3, sy - 8,  14, 3))
        horn = (240, 230, 200)
        pygame.draw.polygon(screen, horn,
                            [(sx + 1, sy - 12),
                             (sx - 3, sy - 16),
                             (sx + 2, sy - 14)])
        pygame.draw.polygon(screen, horn,
                            [(sx + 19, sy - 12),
                             (sx + 23, sy - 16),
                             (sx + 18, sy - 14)])
    elif helmet == 'zhou_helm':
        # Rounded bowl with flared brow guard — Han/Tang style
        pygame.draw.rect(screen, helm,         (sx + 3, sy - 12, 14, 12))
        pygame.draw.rect(screen, helm,         (sx + 1, sy - 4,  18, 2))
        pygame.draw.rect(screen, (20, 20, 30), (sx + 4, sy - 7,  12, 3))
        pygame.draw.rect(screen, plate,        (sx + 3, sy - 13, 14, 1))
    elif helmet == 'zan_helm':
        # Conical spire helm — common from Han through Tang
        pygame.draw.polygon(screen, helm,
                            [(sx + 10, sy - 18),
                             (sx + 2,  sy - 5),
                             (sx + 18, sy - 5)])
        pygame.draw.rect(screen, helm,         (sx,     sy - 6, 20, 2))
        pygame.draw.rect(screen, plate,        (sx + 8, sy - 18, 4, 2))
        pygame.draw.rect(screen, (20, 20, 30), (sx + 4, sy - 3, 12, 2))
    elif helmet == 'dou_mou':
        # Wide-brimmed iron hat — Song/Ming infantry staple
        pygame.draw.rect(screen, helm,         (sx + 4, sy - 10, 12, 9))
        pygame.draw.rect(screen, helm,         (sx - 1, sy - 4,  22, 2))
        pygame.draw.rect(screen, plate,        (sx + 4, sy - 11, 12, 1))
        pygame.draw.rect(screen, (20, 20, 30), (sx + 5, sy - 6,  10, 2))
    elif helmet == 'mianpao':
        # Lamellar curtain helm — bowl with hanging strip aventail
        pygame.draw.rect(screen, helm,         (sx + 2, sy - 12, 16, 10))
        pygame.draw.rect(screen, (20, 20, 30), (sx + 4, sy - 7,  12, 3))
        lam = tuple(max(0, v - 20) for v in armor)
        for i in range(5):
            pygame.draw.rect(screen, lam, (sx + 2 + i * 3, sy - 3, 2, 5))
    elif helmet == 'kabuto':
        # Japanese kabuto — domed bowl with shikoro neck guard and maedate crest
        shikoro = tuple(max(0, v - 30) for v in armor)
        pygame.draw.rect(screen, shikoro,      (sx,     sy - 6,  20, 4))   # shikoro
        pygame.draw.rect(screen, helm,         (sx + 2, sy - 14, 16, 10))  # bowl
        pygame.draw.rect(screen, (20, 20, 30), (sx + 4, sy - 9,  12, 3))   # menpō shadow
        pygame.draw.rect(screen, plate,        (sx + 8, sy - 16, 4,  2))   # maedate crest
        pygame.draw.rect(screen, plate,        (sx + 9, sy - 18, 2,  2))
    elif helmet == 'jingasa':
        # Wide conical straw/iron field hat — common ashigaru footsoldier
        pygame.draw.polygon(screen, helm,
                            [(sx + 10, sy - 14),
                             (sx + 1,  sy - 5),
                             (sx + 19, sy - 5)])
        pygame.draw.rect(screen, helm,         (sx - 1, sy - 6, 22, 2))
        pygame.draw.rect(screen, (20, 20, 30), (sx + 4, sy - 3, 12, 2))
    elif helmet == 'barbute':
        # T-faced Italian infantry helm
        pygame.draw.rect(screen, helm, (sx + 2, sy - 13, 16, 14))
        pygame.draw.rect(screen, skin, (sx + 9, sy - 8, 2, 6))
        pygame.draw.rect(screen, (20, 20, 30), (sx + 3, sy - 7, 6, 2))
        pygame.draw.rect(screen, (20, 20, 30), (sx + 11, sy - 7, 6, 2))
    elif helmet == 'bascinet':
        # Pointed bascinet with mail aventail
        mail = tuple(max(0, v - 15) for v in armor)
        pygame.draw.polygon(screen, helm,
                            [(sx + 10, sy - 14),
                             (sx + 2,  sy - 4),
                             (sx + 18, sy - 4)])
        pygame.draw.rect(screen, mail, (sx + 1, sy - 4, 18, 4))
        pygame.draw.rect(screen, (20, 20, 30), (sx + 4, sy - 7, 12, 2))
    elif helmet == 'armet':
        # Fully enclosed armet — late medieval knight
        pygame.draw.rect(screen, helm, (sx + 1, sy - 14, 18, 14))
        pygame.draw.rect(screen, (20, 20, 30), (sx + 3, sy - 9, 14, 2))
        pygame.draw.rect(screen, plate, (sx + 1, sy - 4, 18, 1))
        pygame.draw.rect(screen, plate, (sx + 9, sy - 14, 2, 2))
    elif helmet == 'morion':
        # Spanish morion — high crest with upturned brim
        pygame.draw.rect(screen, helm, (sx + 3, sy - 12, 14, 11))
        pygame.draw.rect(screen, helm, (sx + 8, sy - 16, 4, 4))
        pygame.draw.polygon(screen, helm,
                            [(sx - 1, sy - 4), (sx + 21, sy - 4),
                             (sx + 17, sy - 7), (sx + 3, sy - 7)])
        pygame.draw.rect(screen, (20, 20, 30), (sx + 4, sy - 8, 12, 2))
    elif helmet == 'nasal_helm':
        # Conical helm with nasal bar
        pygame.draw.polygon(screen, helm,
                            [(sx + 10, sy - 14),
                             (sx + 3,  sy - 4),
                             (sx + 17, sy - 4)])
        pygame.draw.rect(screen, helm, (sx + 9, sy - 4, 2, 6))
        pygame.draw.rect(screen, skin, (sx + 4, sy - 2, 5, 2))
        pygame.draw.rect(screen, skin, (sx + 11, sy - 2, 5, 2))
    elif helmet == 'frog_mouth':
        # Jousting great helm — flat-top with horizontal vision slit
        pygame.draw.rect(screen, helm, (sx + 1, sy - 14, 18, 14))
        pygame.draw.rect(screen, plate, (sx + 1, sy - 14, 18, 1))
        pygame.draw.rect(screen, (20, 20, 30), (sx + 2, sy - 8, 16, 2))
        pygame.draw.rect(screen, helm, (sx + 1, sy - 6, 18, 1))
    elif helmet == 'lobstertail':
        # Lobster-tail pot helm — bowl with hinged neck lames
        pygame.draw.rect(screen, helm, (sx + 2, sy - 12, 16, 11))
        lam = tuple(max(0, v - 25) for v in armor)
        for i in range(3):
            pygame.draw.rect(screen, lam, (sx + 1, sy - 1 + i * 2, 18, 2))
        pygame.draw.rect(screen, plate, (sx + 9, sy - 13, 2, 2))
        pygame.draw.rect(screen, (20, 20, 30), (sx + 4, sy - 8, 12, 2))
    elif helmet == 'winged_helm':
        pygame.draw.rect(screen, helm, (sx + 2, sy - 12, 16, 14))
        pygame.draw.rect(screen, (20, 20, 30), (sx + 3, sy - 8, 14, 3))
        wing = (240, 235, 220)
        pygame.draw.polygon(screen, wing,
                            [(sx + 1,  sy - 11),
                             (sx - 6,  sy - 16),
                             (sx + 1,  sy - 7)])
        pygame.draw.polygon(screen, wing,
                            [(sx + 19, sy - 11),
                             (sx + 26, sy - 16),
                             (sx + 19, sy - 7)])
    elif helmet == 'fur_cap':
        fur = (105, 80, 55)
        pygame.draw.rect(screen, fur, (sx + 2, sy - 10, 16, 9))
        for i in range(8):
            pygame.draw.rect(screen, (75, 55, 35), (sx + 2 + i * 2, sy - 11, 1, 1))
        pygame.draw.rect(screen, skin, (sx + 4, sy - 2, 12, 1))
    elif helmet == 'wolf_pelt':
        pelt = (130, 120, 110)
        pygame.draw.rect(screen, pelt, (sx + 2, sy - 13, 16, 12))
        pygame.draw.polygon(screen, pelt,
                            [(sx + 4,  sy - 13),
                             (sx + 7,  sy - 18),
                             (sx + 9,  sy - 13)])
        pygame.draw.polygon(screen, pelt,
                            [(sx + 11, sy - 13),
                             (sx + 13, sy - 18),
                             (sx + 16, sy - 13)])
        pygame.draw.rect(screen, (35, 25, 20), (sx + 6, sy - 8, 2, 2))
        pygame.draw.rect(screen, (35, 25, 20), (sx + 12, sy - 8, 2, 2))
    elif helmet == 'wide_brim':
        cloth = tuple(max(0, v - 20) for v in armor)
        pygame.draw.rect(screen, cloth, (sx + 4, sy - 12, 12, 7))
        pygame.draw.rect(screen, cloth, (sx - 2, sy - 5, 24, 2))
        pygame.draw.rect(screen, skin, (sx + 4, sy - 3, 12, 2))
    elif helmet == 'tricorn':
        cloth = tuple(max(0, v - 30) for v in armor)
        pygame.draw.rect(screen, cloth, (sx + 4, sy - 10, 12, 6))
        pygame.draw.polygon(screen, cloth,
                            [(sx - 2, sy - 4),
                             (sx + 10, sy - 14),
                             (sx + 22, sy - 4),
                             (sx + 18, sy - 3),
                             (sx + 10, sy - 10),
                             (sx + 2,  sy - 3)])
        pygame.draw.rect(screen, skin, (sx + 4, sy - 2, 12, 2))
    elif helmet == 'shako':
        cloth = tuple(max(0, v - 20) for v in armor)
        pygame.draw.rect(screen, cloth, (sx + 3, sy - 16, 14, 14))
        pygame.draw.rect(screen, (20, 20, 25), (sx + 3, sy - 4, 14, 2))
        pygame.draw.rect(screen, plate, (sx + 8, sy - 18, 4, 4))
        pygame.draw.rect(screen, trim, (sx + 3, sy - 8, 14, 1))
    elif helmet == 'mitre':
        cloth = tuple(min(255, v + 30) for v in trim)
        pygame.draw.polygon(screen, cloth,
                            [(sx + 10, sy - 20),
                             (sx + 4,  sy - 2),
                             (sx + 16, sy - 2)])
        pygame.draw.rect(screen, plate, (sx + 9, sy - 18, 2, 14))
        pygame.draw.rect(screen, plate, (sx + 4, sy - 9, 12, 1))
    elif helmet == 'closed_visor':
        pygame.draw.rect(screen, helm, (sx + 1, sy - 14, 18, 16))
        pygame.draw.rect(screen, plate, (sx + 1, sy - 14, 18, 1))
        for i in range(4):
            pygame.draw.rect(screen, (20, 20, 30), (sx + 3 + i * 4, sy - 7, 2, 2))
        pygame.draw.rect(screen, plate, (sx + 9, sy - 14, 2, 2))
    elif helmet == 'burgonet':
        pygame.draw.rect(screen, helm, (sx + 3, sy - 12, 14, 11))
        pygame.draw.rect(screen, helm, (sx + 9, sy - 15, 2, 4))
        pygame.draw.polygon(screen, helm,
                            [(sx + 1, sy - 6),
                             (sx - 2, sy - 2),
                             (sx + 3, sy - 1)])
        pygame.draw.polygon(screen, helm,
                            [(sx + 19, sy - 6),
                             (sx + 22, sy - 2),
                             (sx + 17, sy - 1)])
        pygame.draw.rect(screen, (20, 20, 30), (sx + 4, sy - 8, 12, 2))
    elif helmet == 'bandana':
        cloth = trim
        pygame.draw.rect(screen, cloth, (sx + 2, sy - 8, 16, 4))
        tail_x = sx + 17 if facing == 1 else sx - 1
        pygame.draw.polygon(screen, cloth,
                            [(tail_x, sy - 8),
                             (tail_x + (4 if facing == 1 else -4), sy - 6),
                             (tail_x, sy - 4)])
        pygame.draw.rect(screen, skin, (sx + 3, sy - 4, 14, 4))
        pygame.draw.rect(screen, (35, 25, 20), (sx + 6, sy - 2, 2, 1))
        pygame.draw.rect(screen, (35, 25, 20), (sx + 12, sy - 2, 2, 1))
    elif helmet == 'straw_hat':
        straw = (210, 180, 110)
        pygame.draw.polygon(screen, straw,
                            [(sx - 2, sy - 4),
                             (sx + 10, sy - 14),
                             (sx + 22, sy - 4),
                             (sx + 22, sy - 3),
                             (sx - 2, sy - 3)])
        for i in range(5):
            pygame.draw.rect(screen, (165, 140, 80), (sx + i * 4, sy - 3, 1, 1))
        pygame.draw.rect(screen, skin, (sx + 4, sy - 2, 12, 2))
    elif helmet == 'crowned_helm':
        pygame.draw.rect(screen, helm, (sx + 2, sy - 12, 16, 14))
        pygame.draw.rect(screen, (20, 20, 30), (sx + 3, sy - 8, 14, 3))
        gold = (225, 185, 70)
        pygame.draw.rect(screen, gold, (sx + 2, sy - 16, 16, 2))
        pygame.draw.rect(screen, gold, (sx + 3, sy - 18, 2, 2))
        pygame.draw.rect(screen, gold, (sx + 9, sy - 19, 2, 3))
        pygame.draw.rect(screen, gold, (sx + 15, sy - 18, 2, 2))
    elif helmet == 'peaked_cap':
        cloth = tuple(max(0, v - 15) for v in armor)
        pygame.draw.rect(screen, cloth, (sx + 3, sy - 10, 14, 8))
        pygame.draw.polygon(screen, cloth,
                            [(sx + 3,  sy - 2),
                             (sx + 19, sy - 2),
                             (sx + 17, sy),
                             (sx + 1,  sy)])
        pygame.draw.rect(screen, trim, (sx + 3, sy - 4, 14, 1))
    elif helmet == 'antlered':
        pygame.draw.rect(screen, helm, (sx + 2, sy - 12, 16, 14))
        pygame.draw.rect(screen, (20, 20, 30), (sx + 3, sy - 8, 14, 3))
        ant = (190, 170, 130)
        pygame.draw.rect(screen, ant, (sx + 1, sy - 14, 1, 6))
        pygame.draw.rect(screen, ant, (sx - 1, sy - 18, 1, 4))
        pygame.draw.rect(screen, ant, (sx - 3, sy - 16, 1, 3))
        pygame.draw.rect(screen, ant, (sx + 18, sy - 14, 1, 6))
        pygame.draw.rect(screen, ant, (sx + 20, sy - 18, 1, 4))
        pygame.draw.rect(screen, ant, (sx + 22, sy - 16, 1, 3))
    elif helmet == 'tasseled':
        pygame.draw.rect(screen, helm, (sx + 2, sy - 12, 16, 11))
        pygame.draw.rect(screen, (20, 20, 30), (sx + 4, sy - 8, 12, 2))
        pygame.draw.rect(screen, plate, (sx + 9, sy - 15, 2, 4))
        tass = trim
        pygame.draw.rect(screen, tass, (sx + 8, sy - 17, 4, 2))
        pygame.draw.rect(screen, tass, (sx + 7, sy - 18, 1, 1))
        pygame.draw.rect(screen, tass, (sx + 12, sy - 18, 1, 1))
    elif helmet == 'forked_crest':
        pygame.draw.rect(screen, helm, (sx + 2, sy - 12, 16, 14))
        pygame.draw.rect(screen, (20, 20, 30), (sx + 3, sy - 8, 14, 3))
        crest = trim
        pygame.draw.polygon(screen, crest,
                            [(sx + 6,  sy - 18),
                             (sx + 8,  sy - 12),
                             (sx + 4,  sy - 13)])
        pygame.draw.polygon(screen, crest,
                            [(sx + 14, sy - 18),
                             (sx + 12, sy - 12),
                             (sx + 16, sy - 13)])
    elif helmet == 'earflaps':
        fur = (105, 80, 55)
        pygame.draw.rect(screen, helm, (sx + 3, sy - 12, 14, 11))
        pygame.draw.rect(screen, fur, (sx + 1, sy - 6, 3, 6))
        pygame.draw.rect(screen, fur, (sx + 16, sy - 6, 3, 6))
        pygame.draw.rect(screen, fur, (sx + 3, sy - 13, 14, 2))
        pygame.draw.rect(screen, (20, 20, 30), (sx + 4, sy - 8, 12, 2))
    elif helmet == 'ridge_helm':
        pygame.draw.rect(screen, helm, (sx + 2, sy - 12, 16, 14))
        pygame.draw.rect(screen, plate, (sx + 9, sy - 13, 2, 11))
        pygame.draw.rect(screen, (20, 20, 30), (sx + 3, sy - 8, 14, 3))
        pygame.draw.rect(screen, plate, (sx + 2, sy - 4, 16, 1))
    elif helmet == 'veiled_helm':
        pygame.draw.rect(screen, helm, (sx + 3, sy - 12, 14, 11))
        veil = tuple(min(255, v + 60) for v in trim)
        pygame.draw.rect(screen, veil, (sx + 1, sy - 4, 18, 6))
        pygame.draw.rect(screen, veil, (sx + 2, sy + 2, 16, 2))
        pygame.draw.rect(screen, plate, (sx + 9, sy - 13, 2, 2))
        pygame.draw.rect(screen, skin, (sx + 5, sy - 6, 10, 2))
    elif helmet == 'mask_helm':
        pygame.draw.rect(screen, helm, (sx + 1, sy - 14, 18, 16))
        pygame.draw.rect(screen, (20, 20, 30), (sx + 4, sy - 8, 3, 2))
        pygame.draw.rect(screen, (20, 20, 30), (sx + 13, sy - 8, 3, 2))
        pygame.draw.polygon(screen, (20, 20, 30),
                            [(sx + 8, sy - 4),
                             (sx + 12, sy - 4),
                             (sx + 10, sy - 1)])
        pygame.draw.rect(screen, plate, (sx + 1, sy - 14, 18, 1))
    elif helmet == 'crested':
        # Roman/centurion-style crested helm
        pygame.draw.rect(screen, helm, (sx + 3, sy - 12, 14, 11))
        pygame.draw.rect(screen, trim, (sx + 9, sy - 18, 2, 6))
        pygame.draw.rect(screen, trim, (sx + 6, sy - 16, 8, 2))
        pygame.draw.rect(screen, (20, 20, 30), (sx + 4, sy - 8, 12, 2))
        pygame.draw.rect(screen, helm, (sx + 1, sy - 4, 18, 2))
    elif helmet == 'feathered':
        # Pot helm with a wide spray of feathers
        pygame.draw.rect(screen, helm, (sx + 2, sy - 12, 16, 14))
        pygame.draw.rect(screen, (20, 20, 30), (sx + 3, sy - 8, 14, 3))
        plume = tuple(min(255, v + 50) for v in trim)
        pygame.draw.rect(screen, plume, (sx + 4, sy - 20, 2, 8))
        pygame.draw.rect(screen, plume, (sx + 8, sy - 22, 2, 10))
        pygame.draw.rect(screen, plume, (sx + 12, sy - 20, 2, 8))
        pygame.draw.rect(screen, trim, (sx + 4, sy - 14, 12, 2))
    elif helmet == 'visor_open':
        # Visored helm with hinged visor lifted up
        pygame.draw.rect(screen, helm, (sx + 2, sy - 12, 16, 11))
        pygame.draw.rect(screen, plate, (sx + 2, sy - 18, 16, 6))
        pygame.draw.rect(screen, skin, (sx + 4, sy - 6, 12, 4))
        pygame.draw.rect(screen, (20, 20, 30), (sx + 5, sy - 4, 3, 2))
        pygame.draw.rect(screen, (20, 20, 30), (sx + 12, sy - 4, 3, 2))
    elif helmet == 'turban_helm':
        # Spired helm wrapped in turban cloth
        cloth = tuple(min(255, v + 50) for v in trim)
        pygame.draw.polygon(screen, helm,
                            [(sx + 10, sy - 16),
                             (sx + 4,  sy - 8),
                             (sx + 16, sy - 8)])
        pygame.draw.rect(screen, cloth, (sx + 2, sy - 9, 16, 5))
        pygame.draw.rect(screen, cloth, (sx + 1, sy - 5, 18, 2))
        pygame.draw.rect(screen, (20, 20, 30), (sx + 4, sy - 3, 12, 2))
    elif helmet == 'pagri':
        # Layered wound cloth — no metal helm shows. Vermilion gem at the brow.
        cloth  = tuple(min(255, v + 40) for v in trim)
        accent = tuple(min(255, v + 80) for v in trim)
        for i, row_y in enumerate((sy - 11, sy - 8, sy - 5)):
            col = cloth if i % 2 == 0 else accent
            pygame.draw.rect(screen, col, (sx + 1, row_y, 18, 3))
        # Forehead gem (rajput aigrette)
        pygame.draw.rect(screen, (240, 220, 90), (sx + 9, sy - 8, 2, 2))
        pygame.draw.rect(screen, (220,  40,  60), (sx + 9, sy - 6, 2, 2))
        # Short pleat sticking up at the back
        pygame.draw.polygon(screen, accent,
                            [(sx + 6, sy - 12), (sx + 9, sy - 16),
                             (sx + 10, sy - 12)])
    elif helmet == 'great_helm':
        # Flat-top great helm with cross slits
        pygame.draw.rect(screen, helm, (sx + 1, sy - 14, 18, 14))
        pygame.draw.rect(screen, plate, (sx + 1, sy - 14, 18, 1))
        pygame.draw.rect(screen, (20, 20, 30), (sx + 5, sy - 9, 4, 2))
        pygame.draw.rect(screen, (20, 20, 30), (sx + 11, sy - 9, 4, 2))
        pygame.draw.rect(screen, (20, 20, 30), (sx + 9, sy - 11, 2, 6))
    elif helmet == 'cervelliere':
        # Small rounded skull cap worn close to the head
        pygame.draw.rect(screen, helm, (sx + 4, sy - 9, 12, 8))
        pygame.draw.rect(screen, helm, (sx + 5, sy - 11, 10, 2))
        pygame.draw.rect(screen, skin, (sx + 4, sy - 1, 12, 3))
    elif helmet == 'spangenhelm':
        # Framed conical with vertical iron bands
        pygame.draw.polygon(screen, helm,
                            [(sx + 10, sy - 14),
                             (sx + 3,  sy - 3),
                             (sx + 17, sy - 3)])
        pygame.draw.rect(screen, plate, (sx + 9, sy - 14, 2, 11))
        pygame.draw.rect(screen, plate, (sx + 5, sy - 10, 1, 7))
        pygame.draw.rect(screen, plate, (sx + 14, sy - 10, 1, 7))
    elif helmet == 'cabasset':
        # Pear-shaped Spanish foot helm with stalk top
        pygame.draw.rect(screen, helm, (sx + 3, sy - 12, 14, 11))
        pygame.draw.rect(screen, helm, (sx + 9, sy - 14, 2, 3))
        pygame.draw.rect(screen, helm, (sx + 1, sy - 4, 18, 2))
        pygame.draw.rect(screen, (20, 20, 30), (sx + 4, sy - 8, 12, 2))
    elif helmet == 'phrygian':
        # Forward-curling tall conical helm
        pygame.draw.polygon(screen, helm,
                            [(sx + 10, sy - 16),
                             (sx + 14, sy - 14),
                             (sx + 4,  sy - 3),
                             (sx + 16, sy - 3)])
        pygame.draw.rect(screen, helm, (sx + 2, sy - 4, 18, 2))
        pygame.draw.rect(screen, (20, 20, 30), (sx + 4, sy - 7, 12, 2))
    elif helmet == 'hood':
        # Cloth/leather hood — for watchmen and irregulars
        cloth = tuple(max(0, v - 30) for v in armor)
        pygame.draw.rect(screen, cloth, (sx + 1, sy - 13, 18, 12))
        pygame.draw.rect(screen, skin, (sx + 4, sy - 6, 12, 5))
        pygame.draw.polygon(screen, cloth,
                            [(sx + 1, sy - 1), (sx + 1, sy - 6),
                             (sx - 2, sy + 2)])
    elif helmet == 'skull_cap':
        # Simple riveted iron skull cap, hair visible underneath
        hair = (95, 75, 55)
        pygame.draw.rect(screen, hair, (sx + 3, sy - 6, 14, 4))
        pygame.draw.rect(screen, helm, (sx + 3, sy - 10, 14, 5))
        pygame.draw.rect(screen, plate, (sx + 5, sy - 11, 2, 1))
        pygame.draw.rect(screen, plate, (sx + 13, sy - 11, 2, 1))
    elif helmet == 'zunari':
        # Zunari kabuto — simple rounded helmet with prominent peak brim
        pygame.draw.rect(screen, helm,         (sx + 3, sy - 12, 14, 11))
        pygame.draw.rect(screen, helm,         (sx + 1, sy - 5,  18, 2))   # peak brim
        pygame.draw.rect(screen, helm,         (sx,     sy - 3,  6,  2))   # left cheek
        pygame.draw.rect(screen, helm,         (sx + 14, sy - 3, 6,  2))   # right cheek
        pygame.draw.rect(screen, (20, 20, 30), (sx + 4, sy - 8,  12, 3))


def _draw_guard_beard(screen, sx, sy, helmet, beard):
    if beard == 'none' or helmet in ('pot', 'plumed', 'horned', 'mianpao'):
        return
    col = (95, 75, 55)
    if beard == 'short':
        pygame.draw.rect(screen, col, (sx + 6, sy - 2, 8, 3))
    elif beard == 'full':
        pygame.draw.rect(screen, col, (sx + 5, sy - 3, 10, 5))
        pygame.draw.rect(screen, col, (sx + 6, sy + 1, 8, 1))
    elif beard == 'mustache':
        pygame.draw.rect(screen, col, (sx + 6, sy - 4, 8, 1))


def _draw_weapon_polearm(screen, sx, sy, plate, facing, length, head):
    shaft_x = sx + 19 if facing == 1 else sx - 1
    pygame.draw.rect(screen, (110, 85, 50), (shaft_x, sy - (length - 18), 2, length))
    if head == 'spear':
        pygame.draw.polygon(screen, plate,
                            [(shaft_x + 1, sy - (length - 10)),
                             (shaft_x + 5, sy - (length - 18)),
                             (shaft_x - 3, sy - (length - 18))])
    elif head == 'lance':
        pygame.draw.polygon(screen, plate,
                            [(shaft_x + 1, sy - (length - 4)),
                             (shaft_x + 3, sy - (length - 14)),
                             (shaft_x - 1, sy - (length - 14))])
        pen_x = shaft_x - 8 if facing == 1 else shaft_x + 2
        pygame.draw.polygon(screen, (180, 40, 50),
                            [(pen_x, sy - (length - 12)),
                             (pen_x + 8, sy - (length - 12)),
                             (pen_x + 4, sy - (length - 18))])
    else:  # halberd: axe head + top spike
        head_x = shaft_x + 2 if facing == 1 else shaft_x - 6
        pygame.draw.polygon(screen, plate,
                            [(head_x, sy - (length - 22)),
                             (head_x + 6, sy - (length - 18)),
                             (head_x + 6, sy - (length - 28)),
                             (head_x, sy - (length - 26))])
        pygame.draw.rect(screen, plate, (shaft_x, sy - length, 2, 6))


def _draw_weapon_club(screen, sx, sy, plate, facing):
    haft_x = sx + 19 if facing == 1 else sx - 1
    pygame.draw.rect(screen, (95, 65, 35),  (haft_x, sy - 4, 2, 22))
    pygame.draw.rect(screen, (130, 95, 55), (haft_x - 1, sy - 8, 4, 6))
    pygame.draw.rect(screen, plate,         (haft_x - 1, sy - 8, 4, 1))


def _draw_watchman_lantern(screen, sx, sy, facing):
    lan_x = sx - 5 if facing == 1 else sx + 19
    pygame.draw.rect(screen, (90, 70, 35),    (lan_x, sy - 4, 6, 8))
    pygame.draw.rect(screen, (255, 230, 140), (lan_x + 1, sy - 3, 4, 6))
    pygame.draw.rect(screen, (60, 45, 25),    (lan_x + 1, sy - 6, 4, 2))
    pygame.draw.rect(screen, (130, 100, 55),  (lan_x + 2, sy - 9, 2, 3))


def _draw_weapon_sword(screen, sx, sy, plate, facing, blade):
    sword_x = sx + 19 if facing == 1 else sx - 3
    pygame.draw.rect(screen, plate,         (sword_x, sy - blade // 2, 2, blade))
    pygame.draw.rect(screen, (110, 80, 40), (sword_x - 1, sy + blade // 2, 4, 2))
    pygame.draw.rect(screen, (130, 90, 50), (sword_x, sy + blade // 2 + 2, 2, 3))


def _draw_weapon_axe(screen, sx, sy, plate, facing):
    haft_x = sx + 19 if facing == 1 else sx - 1
    pygame.draw.rect(screen, (110, 85, 50), (haft_x, sy - 8, 2, 24))
    head_x = haft_x + 2 if facing == 1 else haft_x - 6
    pygame.draw.polygon(screen, plate,
                        [(head_x, sy - 6),
                         (head_x + 6, sy - 9),
                         (head_x + 6, sy - 1),
                         (head_x, sy + 1)])


def _draw_weapon_mace(screen, sx, sy, plate, facing, head):
    haft_x = sx + 19 if facing == 1 else sx - 1
    pygame.draw.rect(screen, (110, 85, 50), (haft_x, sy - 4, 2, 22))
    if head == 'flanged':
        pygame.draw.rect(screen, plate, (haft_x - 2, sy - 9, 6, 6))
        pygame.draw.rect(screen, plate, (haft_x - 1, sy - 11, 4, 2))
    elif head == 'morningstar':
        pygame.draw.circle(screen, plate, (haft_x + 1, sy - 6), 3)
        for dx, dy in ((-3, -3), (3, -3), (-3, 3), (3, 3), (0, -5)):
            pygame.draw.rect(screen, plate, (haft_x + 1 + dx, sy - 6 + dy, 1, 1))
    else:  # flail
        pygame.draw.rect(screen, (90, 90, 95), (haft_x, sy - 7, 1, 1))
        pygame.draw.rect(screen, (90, 90, 95), (haft_x + 1, sy - 9, 1, 1))
        pygame.draw.circle(screen, plate, (haft_x + 2, sy - 11), 3)


def _draw_weapon_crossbow(screen, sx, sy, plate, facing):
    bow_x = sx + 2 if facing == 1 else sx
    pygame.draw.rect(screen, (110, 80, 45), (bow_x, sy + 4, 16, 2))
    pygame.draw.rect(screen, (90, 65, 35),  (bow_x + 7, sy + 1, 2, 8))
    pygame.draw.rect(screen, plate,         (bow_x, sy + 3, 1, 4))
    pygame.draw.rect(screen, plate,         (bow_x + 15, sy + 3, 1, 4))
    pygame.draw.rect(screen, plate,         (bow_x + 8, sy + 5, 6, 1))


def _draw_weapon_longbow(screen, sx, sy, plate, facing):
    bow_x = sx + 18 if facing == 1 else sx - 2
    pygame.draw.rect(screen, (140, 105, 60), (bow_x, sy - 14, 2, 32))
    pygame.draw.rect(screen, (140, 105, 60), (bow_x - (1 if facing == 1 else -1), sy - 16, 1, 2))
    pygame.draw.rect(screen, (140, 105, 60), (bow_x - (1 if facing == 1 else -1), sy + 16, 1, 2))
    pygame.draw.rect(screen, (235, 230, 220), (bow_x + (1 if facing == 1 else 0), sy - 14, 1, 32))
    arrow_x = sx + 4
    pygame.draw.rect(screen, (110, 80, 40), (arrow_x, sy + 1, 14, 1))


def _draw_weapon_katana(screen, sx, sy, plate, facing):
    # Katana — long slightly-curved blade, tsuba guard, wrapped handle
    kat_x = sx + 19 if facing == 1 else sx - 3
    curve = 1 if facing == 1 else -1
    pygame.draw.rect(screen, plate,          (kat_x,          sy - 18, 2, 28))
    pygame.draw.rect(screen, plate,          (kat_x + curve,  sy - 20, 2,  4))
    pygame.draw.rect(screen, (190, 165, 55), (kat_x - 2,      sy + 8,  6,  1))  # tsuba
    pygame.draw.rect(screen, (80,  55,  35), (kat_x,          sy + 9,  2,  5))  # handle
    pygame.draw.rect(screen, (200, 170, 60), (kat_x,          sy + 11, 2,  1))  # wrap band


def _draw_weapon_naginata(screen, sx, sy, plate, facing):
    # Naginata — long pole with a curved blade at the top
    shaft_x = sx + 19 if facing == 1 else sx - 1
    pygame.draw.rect(screen, (110, 85, 50), (shaft_x, sy - 32, 2, 50))
    curve = 1 if facing == 1 else -1
    pygame.draw.polygon(screen, plate,
                        [(shaft_x + 1,          sy - 32),
                         (shaft_x + curve * 7,  sy - 44),
                         (shaft_x + curve * 8,  sy - 38),
                         (shaft_x + 1,          sy - 26)])
    pygame.draw.rect(screen, (190, 165, 55), (shaft_x - 1, sy - 26, 4, 2))  # habaki collar


def _draw_weapon_yumi(screen, sx, sy, plate, facing):
    # Yumi — asymmetric Japanese longbow (upper limb longer)
    bow_x = sx + 18 if facing == 1 else sx - 2
    pygame.draw.rect(screen, (120, 88, 45), (bow_x, sy - 20, 2, 40))
    pygame.draw.rect(screen, (120, 88, 45), (bow_x - (1 if facing == 1 else -1), sy - 22, 1, 4))
    pygame.draw.rect(screen, (120, 88, 45), (bow_x - (1 if facing == 1 else -1), sy + 18, 1, 2))
    pygame.draw.rect(screen, (235, 228, 215), (bow_x + (1 if facing == 1 else 0), sy - 20, 1, 40))
    arrow_x = sx + 4
    pygame.draw.rect(screen, (100, 75, 38), (arrow_x, sy + 1, 14, 1))
    pygame.draw.polygon(screen, plate,
                        [(arrow_x + 13, sy + 1),
                         (arrow_x + 16, sy),
                         (arrow_x + 13, sy + 2)])


def _draw_weapon_guandao(screen, sx, sy, plate, facing):
    # Chinese guandao — long shaft with a heavy curved blade at the top
    shaft_x = sx + 19 if facing == 1 else sx - 1
    pygame.draw.rect(screen, (110, 85, 50), (shaft_x, sy - 28, 2, 46))
    blade_x = shaft_x + 2 if facing == 1 else shaft_x - 8
    pygame.draw.polygon(screen, plate,
                        [(shaft_x + 1, sy - 28),
                         (blade_x + 8, sy - 38),
                         (blade_x + 8, sy - 22),
                         (shaft_x + 1, sy - 20)])
    back_x = shaft_x - 2 if facing == 1 else shaft_x + 4
    pygame.draw.polygon(screen, plate,
                        [(back_x,     sy - 28),
                         (back_x - 2, sy - 33),
                         (back_x + 2, sy - 30)])


def _draw_weapon_jian(screen, sx, sy, plate, facing):
    # Chinese jian — straight double-edged sword, officer's weapon
    jian_x = sx + 19 if facing == 1 else sx - 3
    pygame.draw.rect(screen, plate,          (jian_x,     sy - 14, 2, 24))
    pygame.draw.rect(screen, plate,          (jian_x - 1, sy - 15, 4,  1))
    pygame.draw.rect(screen, (190, 165, 60), (jian_x - 2, sy + 8,  6,  1))
    pygame.draw.rect(screen, (130, 95,  50), (jian_x,     sy + 9,  2,  4))
    pygame.draw.rect(screen, plate,          (jian_x,     sy + 12, 2,  1))


def _draw_weapon_ji(screen, sx, sy, plate, facing):
    # Chinese ji — spear shaft with lateral hook blade partway up
    shaft_x = sx + 19 if facing == 1 else sx - 1
    pygame.draw.rect(screen, (110, 85, 50), (shaft_x, sy - 30, 2, 48))
    pygame.draw.polygon(screen, plate,
                        [(shaft_x + 1, sy - 38),
                         (shaft_x + 4, sy - 30),
                         (shaft_x - 2, sy - 30)])
    hook_x = shaft_x + 2 if facing == 1 else shaft_x - 6
    pygame.draw.polygon(screen, plate,
                        [(hook_x,     sy - 20),
                         (hook_x + 6, sy - 17),
                         (hook_x + 6, sy - 23)])


def _draw_weapon_dao(screen, sx, sy, plate, facing):
    # Chinese dao — broad curved saber with round guard
    dao_x = sx + 19 if facing == 1 else sx - 3
    curve = 1 if facing == 1 else -1
    pygame.draw.rect(screen, plate, (dao_x,          sy - 8,  2, 20))
    pygame.draw.rect(screen, plate, (dao_x + curve,  sy - 10, 2, 4))
    pygame.draw.rect(screen, (110, 80, 40), (dao_x - 1, sy + 10, 4, 2))
    pygame.draw.rect(screen, (130, 90, 50), (dao_x,     sy + 12, 2, 4))


def _draw_weapon_billhook(screen, sx, sy, plate, facing):
    shaft_x = sx + 19 if facing == 1 else sx - 1
    pygame.draw.rect(screen, (110, 85, 50), (shaft_x, sy - 28, 2, 46))
    head_x = shaft_x + 2 if facing == 1 else shaft_x - 6
    pygame.draw.polygon(screen, plate,
                        [(shaft_x + 1, sy - 30),
                         (head_x + 4, sy - 36),
                         (head_x + 6, sy - 32),
                         (shaft_x + 1, sy - 26)])
    pygame.draw.polygon(screen, plate,
                        [(head_x + 4, sy - 36),
                         (head_x + 7, sy - 40),
                         (head_x + 6, sy - 32)])


def _draw_weapon_warhammer(screen, sx, sy, plate, facing):
    haft_x = sx + 19 if facing == 1 else sx - 1
    pygame.draw.rect(screen, (90, 65, 35), (haft_x, sy - 10, 2, 26))
    head_x = haft_x - 3 if facing == 1 else haft_x - 1
    pygame.draw.rect(screen, plate, (head_x, sy - 12, 8, 5))
    spike_x = head_x + 8 if facing == 1 else head_x - 3
    pygame.draw.polygon(screen, plate,
                        [(spike_x, sy - 11),
                         (spike_x + 3, sy - 10),
                         (spike_x, sy - 9)])


def _draw_weapon_bardiche(screen, sx, sy, plate, facing):
    shaft_x = sx + 19 if facing == 1 else sx - 1
    pygame.draw.rect(screen, (110, 85, 50), (shaft_x, sy - 30, 2, 48))
    blade_x = shaft_x + 2 if facing == 1 else shaft_x - 8
    pygame.draw.polygon(screen, plate,
                        [(shaft_x + 1, sy - 32),
                         (blade_x + 8, sy - 28),
                         (blade_x + 6, sy - 14),
                         (shaft_x + 1, sy - 18)])


def _draw_weapon_glaive(screen, sx, sy, plate, facing):
    shaft_x = sx + 19 if facing == 1 else sx - 1
    pygame.draw.rect(screen, (110, 85, 50), (shaft_x, sy - 30, 2, 48))
    curve = 1 if facing == 1 else -1
    pygame.draw.polygon(screen, plate,
                        [(shaft_x + 1, sy - 30),
                         (shaft_x + curve * 6, sy - 42),
                         (shaft_x + curve * 7, sy - 36),
                         (shaft_x + 1, sy - 24)])


def _draw_weapon_rondel(screen, sx, sy, plate, facing):
    dag_x = sx + 19 if facing == 1 else sx - 3
    pygame.draw.rect(screen, plate, (dag_x, sy - 4, 2, 14))
    pygame.draw.circle(screen, plate, (dag_x + 1, sy + 10), 2)
    pygame.draw.rect(screen, (80, 55, 35), (dag_x, sy + 11, 2, 4))
    pygame.draw.circle(screen, plate, (dag_x + 1, sy + 16), 2)


def _draw_weapon_claymore(screen, sx, sy, plate, facing):
    cl_x = sx + 19 if facing == 1 else sx - 3
    pygame.draw.rect(screen, plate, (cl_x, sy - 22, 2, 34))
    pygame.draw.rect(screen, plate, (cl_x - 1, sy - 24, 4, 2))
    pygame.draw.polygon(screen, plate,
                        [(cl_x - 4, sy + 12), (cl_x + 6, sy + 12),
                         (cl_x - 2, sy + 10), (cl_x + 4, sy + 10)])
    pygame.draw.rect(screen, (90, 65, 35), (cl_x, sy + 13, 2, 6))
    pygame.draw.rect(screen, plate, (cl_x - 1, sy + 19, 4, 2))


def _draw_weapon_falchion(screen, sx, sy, plate, facing):
    fal_x = sx + 19 if facing == 1 else sx - 4
    curve = 1 if facing == 1 else -1
    pygame.draw.rect(screen, plate, (fal_x, sy - 6, 2, 18))
    pygame.draw.polygon(screen, plate,
                        [(fal_x, sy + 2),
                         (fal_x + curve * 3, sy + 8),
                         (fal_x + curve * 3, sy + 12),
                         (fal_x, sy + 12)])
    pygame.draw.rect(screen, (110, 80, 40), (fal_x - 1, sy + 12, 4, 2))
    pygame.draw.rect(screen, (130, 90, 50), (fal_x, sy + 14, 2, 4))


def _draw_weapon_whip(screen, sx, sy, plate, facing):
    wh_x = sx + 19 if facing == 1 else sx - 1
    pygame.draw.rect(screen, (90, 60, 30), (wh_x, sy + 4, 2, 5))
    curve = 1 if facing == 1 else -1
    cx = wh_x
    cy = sy + 9
    for i in range(8):
        cx += curve * 2
        cy += 1 if i % 2 == 0 else 2
        pygame.draw.rect(screen, (60, 40, 25), (cx, cy, 1, 1))


def _draw_weapon_net(screen, sx, sy, plate, facing):
    n_x = sx - 4 if facing == 1 else sx + 18
    pygame.draw.polygon(screen, (130, 110, 80),
                        [(n_x, sy + 2),
                         (n_x + 6, sy + 2),
                         (n_x + 6, sy + 14),
                         (n_x, sy + 14)])
    for r in range(4):
        for c in range(3):
            pygame.draw.rect(screen, (95, 80, 55),
                             (n_x + 1 + c * 2, sy + 3 + r * 3, 1, 1))
    pygame.draw.rect(screen, plate, (n_x, sy + 2, 6, 1))


def _draw_weapon_torch(screen, sx, sy, plate, facing):
    t_x = sx + 19 if facing == 1 else sx - 1
    pygame.draw.rect(screen, (95, 65, 35), (t_x, sy - 2, 2, 16))
    pygame.draw.rect(screen, (140, 95, 45), (t_x - 1, sy - 4, 4, 2))
    pygame.draw.polygon(screen, (255, 200, 80),
                        [(t_x + 1, sy - 14),
                         (t_x + 4, sy - 6),
                         (t_x - 2, sy - 6)])
    pygame.draw.polygon(screen, (255, 240, 160),
                        [(t_x + 1, sy - 11),
                         (t_x + 3, sy - 6),
                         (t_x - 1, sy - 6)])


def _draw_weapon_buckler(screen, sx, sy, plate, facing):
    sword_x = sx + 19 if facing == 1 else sx - 3
    pygame.draw.rect(screen, plate, (sword_x, sy - 6, 2, 14))
    pygame.draw.rect(screen, (110, 80, 40), (sword_x - 1, sy + 8, 4, 2))
    buck_x = sx - 4 if facing == 1 else sx + 18
    pygame.draw.circle(screen, plate, (buck_x + 3, sy + 6), 3)
    pygame.draw.circle(screen, (50, 50, 60), (buck_x + 3, sy + 6), 1)


def _draw_weapon_flamberge(screen, sx, sy, plate, facing):
    fl_x = sx + 19 if facing == 1 else sx - 3
    for i in range(8):
        off = 1 if (i % 2 == 0) else -1
        pygame.draw.rect(screen, plate, (fl_x + off, sy - 22 + i * 4, 2, 4))
    pygame.draw.rect(screen, plate, (fl_x - 2, sy + 12, 6, 2))
    pygame.draw.rect(screen, (90, 65, 35), (fl_x, sy + 14, 2, 5))
    pygame.draw.rect(screen, plate, (fl_x - 1, sy + 19, 4, 2))


def _draw_weapon_estoc(screen, sx, sy, plate, facing):
    es_x = sx + 19 if facing == 1 else sx - 3
    pygame.draw.rect(screen, plate, (es_x, sy - 26, 1, 38))
    pygame.draw.rect(screen, plate, (es_x - 1, sy + 12, 4, 1))
    pygame.draw.rect(screen, (90, 65, 35), (es_x, sy + 13, 2, 5))
    pygame.draw.rect(screen, plate, (es_x, sy + 18, 2, 2))


def _draw_weapon_javelin(screen, sx, sy, plate, facing):
    jav_x = sx + 19 if facing == 1 else sx - 1
    pygame.draw.rect(screen, (130, 95, 55), (jav_x, sy - 14, 2, 32))
    pygame.draw.polygon(screen, plate,
                        [(jav_x + 1, sy - 18),
                         (jav_x + 3, sy - 12),
                         (jav_x - 1, sy - 12)])
    spare_x = sx - 3 if facing == 1 else sx + 19
    pygame.draw.rect(screen, (130, 95, 55), (spare_x, sy - 8, 1, 22))


def _draw_weapon_sling(screen, sx, sy, plate, facing):
    sl_x = sx + 19 if facing == 1 else sx - 4
    pygame.draw.rect(screen, (150, 130, 100), (sl_x, sy + 4, 2, 12))
    pygame.draw.rect(screen, (95, 75, 50), (sl_x - 2, sy + 16, 6, 3))
    pygame.draw.rect(screen, (110, 90, 65), (sl_x - 1, sy + 6, 1, 10))
    pygame.draw.rect(screen, (110, 90, 65), (sl_x + 2, sy + 6, 1, 10))


def _draw_weapon_cudgel(screen, sx, sy, plate, facing):
    cg_x = sx + 19 if facing == 1 else sx - 1
    pygame.draw.rect(screen, (120, 90, 55), (cg_x, sy - 2, 2, 18))
    pygame.draw.rect(screen, (140, 105, 65), (cg_x - 1, sy - 6, 4, 5))


def _draw_weapon_partisan(screen, sx, sy, plate, facing):
    shaft_x = sx + 19 if facing == 1 else sx - 1
    pygame.draw.rect(screen, (110, 85, 50), (shaft_x, sy - 28, 2, 46))
    pygame.draw.polygon(screen, plate,
                        [(shaft_x + 1, sy - 36),
                         (shaft_x + 4, sy - 26),
                         (shaft_x - 2, sy - 26)])
    pygame.draw.polygon(screen, plate,
                        [(shaft_x + 1, sy - 30),
                         (shaft_x + 6, sy - 24),
                         (shaft_x + 1, sy - 24)])
    pygame.draw.polygon(screen, plate,
                        [(shaft_x + 1, sy - 30),
                         (shaft_x - 4, sy - 24),
                         (shaft_x + 1, sy - 24)])


def _draw_weapon_boar_spear(screen, sx, sy, plate, facing):
    shaft_x = sx + 19 if facing == 1 else sx - 1
    pygame.draw.rect(screen, (110, 85, 50), (shaft_x, sy - 22, 2, 40))
    pygame.draw.polygon(screen, plate,
                        [(shaft_x + 1, sy - 30),
                         (shaft_x + 4, sy - 22),
                         (shaft_x - 2, sy - 22)])
    pygame.draw.rect(screen, plate, (shaft_x - 4, sy - 18, 10, 1))


def _draw_shield(screen, sx, sy, trim, plate, facing, shape):
    sx_off = sx - 4 if facing == 1 else sx + 18
    cx, cy = sx_off + 3, sy + 6
    if shape == 'round':
        pygame.draw.circle(screen, trim,  (cx, cy), 5)
        pygame.draw.circle(screen, plate, (cx, cy), 2)
    elif shape == 'kite':
        pygame.draw.polygon(screen, trim,
                            [(cx - 4, cy - 4), (cx + 4, cy - 4),
                             (cx + 3, cy + 3), (cx, cy + 6),
                             (cx - 3, cy + 3)])
        pygame.draw.rect(screen, plate, (cx - 1, cy - 2, 2, 4))
    else:  # heater
        pygame.draw.polygon(screen, trim,
                            [(cx - 4, cy - 4), (cx + 4, cy - 4),
                             (cx + 3, cy + 2), (cx, cy + 5),
                             (cx - 3, cy + 2)])
        pygame.draw.rect(screen, plate, (cx - 1, cy - 3, 2, 5))


def _draw_guard_loadout(screen, sx, sy, npc, kit, plate, trim, facing):
    variant = getattr(npc, 'weapon_variant', 0)
    shield_col = getattr(npc, 'shield_color', trim)
    if kit == 'spearman':
        _draw_weapon_polearm(screen, sx, sy, plate, facing, length=38, head='spear')
    elif kit == 'pikeman':
        _draw_weapon_polearm(screen, sx, sy, plate, facing, length=46, head='spear')
    elif kit == 'lancer':
        _draw_weapon_polearm(screen, sx, sy, plate, facing, length=52, head='lance')
        _draw_shield(screen, sx, sy, shield_col, plate, facing, shape='heater')
    elif kit == 'halberdier':
        _draw_weapon_polearm(screen, sx, sy, plate, facing, length=42, head='halberd')
    elif kit == 'swordsman':
        _draw_weapon_sword(screen, sx, sy, plate, facing, blade=16)
        _draw_shield(screen, sx, sy, shield_col, plate, facing, shape=('round', 'kite', 'heater')[variant])
    elif kit == 'axeman':
        _draw_weapon_axe(screen, sx, sy, plate, facing)
        _draw_shield(screen, sx, sy, shield_col, plate, facing, shape=('round', 'kite')[variant % 2])
    elif kit == 'macer':
        _draw_weapon_mace(screen, sx, sy, plate, facing, head=('flanged', 'morningstar', 'flail')[variant])
        _draw_shield(screen, sx, sy, shield_col, plate, facing, shape=('heater', 'round')[variant % 2])
    elif kit == 'crossbowman':
        _draw_weapon_crossbow(screen, sx, sy, plate, facing)
    elif kit == 'archer':
        _draw_weapon_longbow(screen, sx, sy, plate, facing)
    elif kit == 'watchman':
        _draw_weapon_club(screen, sx, sy, plate, facing)
        _draw_watchman_lantern(screen, sx, sy, facing)
    elif kit == 'captain':
        _draw_weapon_sword(screen, sx, sy, plate, facing, blade=24)
    elif kit == 'ji_bearer':
        _draw_weapon_ji(screen, sx, sy, plate, facing)
    elif kit == 'guandao_bearer':
        _draw_weapon_guandao(screen, sx, sy, plate, facing)
    elif kit == 'dao_swordsman':
        _draw_weapon_dao(screen, sx, sy, plate, facing)
        _draw_shield(screen, sx, sy, shield_col, plate, facing, shape='round')
    elif kit == 'jian_swordsman':
        _draw_weapon_jian(screen, sx, sy, plate, facing)
    elif kit == 'katana_samurai':
        _draw_weapon_katana(screen, sx, sy, plate, facing)
    elif kit == 'naginata_bearer':
        _draw_weapon_naginata(screen, sx, sy, plate, facing)
    elif kit == 'yumi_archer':
        _draw_weapon_yumi(screen, sx, sy, plate, facing)
    elif kit == 'billhook_bearer':
        _draw_weapon_billhook(screen, sx, sy, plate, facing)
    elif kit == 'warhammer':
        _draw_weapon_warhammer(screen, sx, sy, plate, facing)
        _draw_shield(screen, sx, sy, shield_col, plate, facing, shape='heater')
    elif kit == 'bardiche_bearer':
        _draw_weapon_bardiche(screen, sx, sy, plate, facing)
    elif kit == 'glaive_bearer':
        _draw_weapon_glaive(screen, sx, sy, plate, facing)
    elif kit == 'rondel_bearer':
        _draw_weapon_rondel(screen, sx, sy, plate, facing)
        _draw_shield(screen, sx, sy, shield_col, plate, facing, shape='round')
    elif kit == 'claymore_bearer':
        _draw_weapon_claymore(screen, sx, sy, plate, facing)
    elif kit == 'falchion_bearer':
        _draw_weapon_falchion(screen, sx, sy, plate, facing)
        _draw_shield(screen, sx, sy, shield_col, plate, facing, shape=('round', 'heater')[variant % 2])
    elif kit == 'boar_spear_bearer':
        _draw_weapon_boar_spear(screen, sx, sy, plate, facing)
    elif kit == 'flamberge_bearer':
        _draw_weapon_flamberge(screen, sx, sy, plate, facing)
    elif kit == 'estoc_bearer':
        _draw_weapon_estoc(screen, sx, sy, plate, facing)
    elif kit == 'javelin_thrower':
        _draw_weapon_javelin(screen, sx, sy, plate, facing)
        _draw_shield(screen, sx, sy, shield_col, plate, facing, shape='round')
    elif kit == 'slinger':
        _draw_weapon_sling(screen, sx, sy, plate, facing)
    elif kit == 'cudgeler':
        _draw_weapon_cudgel(screen, sx, sy, plate, facing)
    elif kit == 'partisan_bearer':
        _draw_weapon_partisan(screen, sx, sy, plate, facing)
    elif kit == 'whip_bearer':
        _draw_weapon_whip(screen, sx, sy, plate, facing)
    elif kit == 'net_thrower':
        _draw_weapon_net(screen, sx, sy, plate, facing)
    elif kit == 'torchbearer':
        _draw_weapon_torch(screen, sx, sy, plate, facing)
    elif kit == 'buckler_duelist':
        _draw_weapon_buckler(screen, sx, sy, plate, facing)
    elif kit == 'horse_archer':
        _draw_weapon_horse_bow(screen, sx, sy, plate, trim, facing)
    elif kit == 'cataphract_lancer':
        _draw_weapon_kontos(screen, sx, sy, plate, facing)
        _draw_cataphract_scale(screen, sx, sy, plate, trim)
    elif kit == 'tulwar_bearer':
        _draw_weapon_tulwar(screen, sx, sy, plate, facing)
        _draw_shield(screen, sx, sy, shield_col, plate, facing, shape='round')


def _draw_weapon_horse_bow(screen, sx, sy, plate, trim, facing):
    """Short Mongol-style composite bow held horizontal, with a back quiver."""
    hand_x = sx + (17 if facing == 1 else 1)
    bow_y  = sy + 4
    # Bow body: short recurve, drawn as two arcs flanking the hand
    bow_col = (110, 70, 30)
    string  = (235, 230, 215)
    if facing == 1:
        # Upper limb
        pygame.draw.polygon(screen, bow_col,
                            [(hand_x,      bow_y - 6),
                             (hand_x + 6,  bow_y - 4),
                             (hand_x + 7,  bow_y),
                             (hand_x + 1,  bow_y - 2)])
        # Lower limb
        pygame.draw.polygon(screen, bow_col,
                            [(hand_x,      bow_y + 6),
                             (hand_x + 6,  bow_y + 4),
                             (hand_x + 7,  bow_y),
                             (hand_x + 1,  bow_y + 2)])
        pygame.draw.rect(screen, string, (hand_x + 7, bow_y - 4, 1, 9))
    else:
        pygame.draw.polygon(screen, bow_col,
                            [(hand_x,      bow_y - 6),
                             (hand_x - 6,  bow_y - 4),
                             (hand_x - 7,  bow_y),
                             (hand_x - 1,  bow_y - 2)])
        pygame.draw.polygon(screen, bow_col,
                            [(hand_x,      bow_y + 6),
                             (hand_x - 6,  bow_y + 4),
                             (hand_x - 7,  bow_y),
                             (hand_x - 1,  bow_y + 2)])
        pygame.draw.rect(screen, string, (hand_x - 8, bow_y - 4, 1, 9))
    # Back quiver — visible silhouette behind the shoulder
    back_x = sx - 3 if facing == 1 else sx + 18
    pygame.draw.rect(screen, (95, 65, 35), (back_x, sy - 4, 4, 16))
    # Three arrow fletchings poking out the top
    pygame.draw.rect(screen, trim, (back_x + 1, sy - 7, 1, 4))
    pygame.draw.rect(screen, (235, 230, 215), (back_x + 2, sy - 7, 1, 4))
    pygame.draw.rect(screen, trim, (back_x + 3, sy - 7, 1, 4))


def _draw_weapon_kontos(screen, sx, sy, plate, facing):
    """Two-handed cavalry lance — the kontos. Longer + thicker than a normal lance."""
    hand_x = sx + (17 if facing == 1 else 1)
    head_x = hand_x + (18 if facing == 1 else -18)
    shaft  = (135, 95, 50)
    # Shaft held diagonally
    if facing == 1:
        for i in range(20):
            pygame.draw.rect(screen, shaft, (hand_x + i, sy + 8 - i // 3, 2, 2))
        pygame.draw.polygon(screen, plate,
                            [(head_x + 2, sy + 2),
                             (head_x + 8, sy - 2),
                             (head_x + 2, sy + 6)])
    else:
        for i in range(20):
            pygame.draw.rect(screen, shaft, (hand_x - i, sy + 8 - i // 3, 2, 2))
        pygame.draw.polygon(screen, plate,
                            [(head_x - 2, sy + 2),
                             (head_x - 8, sy - 2),
                             (head_x - 2, sy + 6)])


def _draw_cataphract_scale(screen, sx, sy, plate, trim):
    """Lamellar / scale highlight overpainted on the cuirass — small reflective squares."""
    accent = tuple(min(255, v + 20) for v in plate)
    shadow = tuple(max(0, v - 30) for v in plate)
    # Three rows of small scales across the chest
    for row_y in (sy + 4, sy + 8, sy + 12):
        for col_x in (sx + 3, sx + 7, sx + 11, sx + 15):
            pygame.draw.rect(screen, accent, (col_x, row_y, 3, 3))
            pygame.draw.rect(screen, shadow, (col_x, row_y + 2, 3, 1))


def _draw_weapon_tulwar(screen, sx, sy, plate, facing):
    """Curved sabre held diagonal — disc pommel, deep curve."""
    hand_x = sx + (17 if facing == 1 else 1)
    blade  = (220, 220, 230)
    edge   = (255, 255, 255)
    hilt   = (90, 60, 30)
    disc   = (220, 180, 70)
    if facing == 1:
        # Curved blade — three short rects approximating a sabre arc
        pygame.draw.rect(screen, blade, (hand_x + 1, sy + 2, 3, 5))
        pygame.draw.rect(screen, blade, (hand_x + 3, sy - 1, 4, 4))
        pygame.draw.rect(screen, blade, (hand_x + 6, sy - 4, 4, 3))
        pygame.draw.rect(screen, edge, (hand_x + 4, sy, 4, 1))
        # Hilt + disc pommel
        pygame.draw.rect(screen, hilt, (hand_x - 1, sy + 5, 3, 4))
        pygame.draw.rect(screen, disc, (hand_x - 2, sy + 8, 4, 2))
    else:
        pygame.draw.rect(screen, blade, (hand_x - 3, sy + 2, 3, 5))
        pygame.draw.rect(screen, blade, (hand_x - 6, sy - 1, 4, 4))
        pygame.draw.rect(screen, blade, (hand_x - 9, sy - 4, 4, 3))
        pygame.draw.rect(screen, edge, (hand_x - 7, sy, 4, 1))
        pygame.draw.rect(screen, hilt, (hand_x - 1, sy + 5, 3, 4))
        pygame.draw.rect(screen, disc, (hand_x - 1, sy + 8, 4, 2))


def draw_npc_guard(screen, sx, sy, npc):
    bob = int(npc._bob_offset)
    facing = getattr(npc, 'facing', 1)
    c = getattr(npc, 'clothing', {})
    kit    = getattr(npc, 'kit',           'spearman')
    helmet = getattr(npc, 'helmet',        'pot')
    finish = getattr(npc, 'helmet_finish', 'steel')
    emblem = getattr(npc, 'emblem',        'none')
    beard  = getattr(npc, 'beard',         'none')
    cape   = getattr(npc, 'cape',          'none')
    tint   = getattr(npc, 'tint',          0)
    tabard = getattr(npc, 'tabard',        'solid')
    boots  = getattr(npc, 'boots',         (60, 45, 30))
    sash   = getattr(npc, 'sash',          False)

    armor = tuple(max(0, min(255, v + tint)) for v in c.get('armor', (55, 55, 75)))
    plate = c.get('plate', (155, 160, 165))
    trim  = c.get('trim',  (140, 35, 35))
    if kit == 'captain':
        armor = tuple(min(255, v + 35) for v in armor)
        plate = (215, 195, 110)
        trim  = (190, 40, 40)
    body_y = sy + bob

    _draw_guard_cape(screen, sx, body_y, cape, trim, armor, facing)
    _draw_guard_back_gear(screen, sx, body_y, kit, trim, plate, facing)
    pygame.draw.rect(screen, armor, (sx, body_y, 20, 18))
    _draw_guard_tabard(screen, sx, body_y, tabard, trim, plate, armor)
    pygame.draw.rect(screen, plate, (sx + 8, body_y, 5, 18))
    pygame.draw.rect(screen, boots, (sx, body_y + 16, 20, 2))
    if sash:
        sash_col = tuple(min(255, v + 40) for v in trim)
        pygame.draw.polygon(screen, sash_col,
                            [(sx + 1, body_y + 1), (sx + 5, body_y + 1),
                             (sx + 19, body_y + 14), (sx + 16, body_y + 16)])
    _draw_guard_emblem(screen, sx, body_y, emblem, trim, plate)
    _draw_guard_helmet(screen, sx, body_y, helmet, finish, armor, plate, trim, c, npc, facing)
    _draw_guard_beard(screen, sx, body_y, helmet, beard)
    _draw_guard_loadout(screen, sx, body_y, npc, kit, plate, trim, facing)


def draw_npc_knight(screen, sx, sy, npc):
    """Knight rendered through the guard armor pipeline.

    KnightNPC carries the same guard-system attributes (clothing palette, kit,
    helmet, finish, emblem, cape, tabard, boots, sash) — so we feed them
    straight into the same primitives draw_npc_guard uses. The only knight
    distinction is a small crest plume on top of the helm in the order color.
    """
    bob = int(npc._bob_offset)
    facing = getattr(npc, 'facing', 1)
    c = getattr(npc, 'clothing', {})
    kit    = getattr(npc, 'kit',           'swordsman')
    helmet = getattr(npc, 'helmet',        'great_helm')
    finish = getattr(npc, 'helmet_finish', 'polished')
    emblem = getattr(npc, 'emblem',        'cross')
    beard  = getattr(npc, 'beard',         'none')
    cape   = getattr(npc, 'cape',          'trim')
    tint   = getattr(npc, 'tint',          0)
    tabard = getattr(npc, 'tabard',        'cross')
    boots  = getattr(npc, 'boots',         (40, 30, 22))
    sash   = getattr(npc, 'sash',          False)

    armor = tuple(max(0, min(255, v + tint)) for v in c.get('armor', (185, 190, 200)))
    plate = c.get('plate', (220, 222, 230))
    trim  = c.get('trim',  getattr(npc, 'shield_color', (140, 60, 60)))
    body_y = sy + bob

    _draw_guard_cape(screen, sx, body_y, cape, trim, armor, facing)
    _draw_guard_back_gear(screen, sx, body_y, kit, trim, plate, facing)
    pygame.draw.rect(screen, armor, (sx, body_y, 20, 18))
    _draw_guard_tabard(screen, sx, body_y, tabard, trim, plate, armor)
    pygame.draw.rect(screen, plate, (sx + 8, body_y, 5, 18))
    pygame.draw.rect(screen, boots, (sx, body_y + 16, 20, 2))
    if sash:
        sash_col = tuple(min(255, v + 40) for v in trim)
        pygame.draw.polygon(screen, sash_col,
                            [(sx + 1, body_y + 1), (sx + 5, body_y + 1),
                             (sx + 19, body_y + 14), (sx + 16, body_y + 16)])
    _draw_guard_emblem(screen, sx, body_y, emblem, trim, plate)
    _draw_guard_helmet(screen, sx, body_y, helmet, finish, armor, plate, trim, c, npc, facing)
    _draw_guard_beard(screen, sx, body_y, helmet, beard)
    _draw_guard_loadout(screen, sx, body_y, npc, kit, plate, trim, facing)

    # Knight-only flourish: a small crest plume in the order's primary color.
    pygame.draw.polygon(screen, trim,
                        [(sx + 9,  body_y - 16),
                         (sx + 11, body_y - 16),
                         (sx + 13, body_y - 12),
                         (sx + 7,  body_y - 12)])
