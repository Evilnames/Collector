import pygame


def _guard_helmet_color(finish, armor):
    if finish == 'bronze':
        return (180, 130, 70)
    if finish == 'blackened':
        return (35, 35, 45)
    if finish == 'burnished':
        return (200, 200, 210)
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
    elif kit in ('swordsman', 'captain'):
        scab_x = sx - 3 if facing == 1 else sx + 18
        pygame.draw.rect(screen, (75, 55, 30), (scab_x, sy + 4, 2, 14))
        pygame.draw.rect(screen, plate,        (scab_x, sy + 16, 2, 2))
    elif kit == 'watchman':
        lan_x = sx - 4 if facing == 1 else sx + 19
        pygame.draw.rect(screen, (90, 70, 35),    (lan_x, sy + 2, 5, 7))
        pygame.draw.rect(screen, (255, 220, 130), (lan_x + 1, sy + 3, 3, 5))
        pygame.draw.rect(screen, (60, 45, 25),    (lan_x + 1, sy,    3, 2))


def _draw_guard_cape(screen, sx, sy, cape, trim, armor, facing):
    if cape == 'none':
        return
    col = trim if cape == 'trim' else tuple(max(0, v - 25) for v in armor)
    cape_x = sx - 3 if facing == 1 else sx + 17
    pygame.draw.polygon(screen, col,
                        [(cape_x, sy),
                         (cape_x + 6, sy),
                         (cape_x + 4, sy + 16),
                         (cape_x + 1, sy + 16)])


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


def _draw_guard_beard(screen, sx, sy, helmet, beard):
    if beard == 'none' or helmet in ('pot', 'plumed', 'horned'):
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
