import math
import pygame


def draw_npc_elder(screen, sx, sy, npc):
    bob = int(npc._bob_offset)
    facing = getattr(npc, 'facing', 1)
    c = getattr(npc, 'clothing', {})
    body = c.get('body', (95, 95, 110))
    trim = c.get('trim', (60, 60, 75))
    skin = c.get('skin', (225, 200, 175))
    hair = (235, 235, 230)
    pygame.draw.rect(screen, body, (sx, sy + bob, 20, 18))
    pygame.draw.rect(screen, trim, (sx, sy + 16 + bob, 20, 2))
    pygame.draw.rect(screen, skin, (sx + 2, sy - 10 + bob, 16, 12))
    pygame.draw.rect(screen, (40, 30, 20), (sx + 4,  sy - 7 + bob, 3, 3))
    pygame.draw.rect(screen, (40, 30, 20), (sx + 11, sy - 7 + bob, 3, 3))
    pygame.draw.rect(screen, (170, 145, 120), (sx + 5, sy - 3 + bob, 10, 1))
    pygame.draw.rect(screen, hair, (sx + 2,  sy - 12 + bob, 16, 3))
    pygame.draw.rect(screen, hair, (sx + 1,  sy - 9 + bob, 2, 6))
    pygame.draw.rect(screen, hair, (sx + 17, sy - 9 + bob, 2, 6))
    pygame.draw.rect(screen, hair, (sx + 5, sy - 1 + bob, 10, 4))
    cane_x = sx + 19 if facing == 1 else sx - 1
    pygame.draw.rect(screen, (110, 80, 50), (cane_x, sy - 4 + bob, 2, 22))
    pygame.draw.rect(screen, (140, 100, 60), (cane_x - 1, sy - 5 + bob, 4, 2))


def draw_npc_beggar(screen, sx, sy, npc):
    bob = int(npc._bob_offset)
    c = getattr(npc, 'clothing', {})
    skin  = c.get('skin', (200, 175, 145))
    rags  = (95, 80, 65)
    patch = (135, 110, 80)
    dirt  = (70, 55, 40)
    pygame.draw.rect(screen, rags,  (sx, sy + bob, 20, 18))
    pygame.draw.rect(screen, patch, (sx + 3,  sy + 4  + bob, 4, 5))
    pygame.draw.rect(screen, patch, (sx + 12, sy + 9  + bob, 5, 4))
    pygame.draw.rect(screen, dirt,  (sx,      sy + 16 + bob, 20, 2))
    pygame.draw.rect(screen, rags, (sx + 1, sy - 13 + bob, 18, 11))
    pygame.draw.rect(screen, skin, (sx + 4, sy - 6  + bob, 12, 5))
    pygame.draw.rect(screen, (30, 25, 20), (sx + 6,  sy - 5 + bob, 2, 2))
    pygame.draw.rect(screen, (30, 25, 20), (sx + 12, sy - 5 + bob, 2, 2))
    pygame.draw.rect(screen, (90, 70, 55), (sx + 6, sy + 12 + bob, 8, 3))
    pygame.draw.rect(screen, (60, 45, 30), (sx + 6, sy + 12 + bob, 8, 1))


def draw_npc_noble(screen, sx, sy, npc):
    bob    = int(npc._bob_offset)
    facing = getattr(npc, 'facing', 1)
    c      = getattr(npc, 'clothing', {})
    skin   = c.get('skin', (250, 220, 185))

    palace_type  = getattr(npc, 'palace_type',  None)
    leader_color = getattr(npc, 'leader_color', None)

    if palace_type and leader_color:
        _draw_court_noble(screen, sx, sy, bob, facing, skin, palace_type, leader_color)
        return

    # Generic noble (no dynasty affiliation)
    body  = c.get('body', (90, 35, 110))
    trim  = c.get('trim', (220, 180, 70))
    plume = (210, 60, 70)
    pygame.draw.rect(screen, body, (sx, sy + bob, 20, 18))
    pygame.draw.rect(screen, trim, (sx + 8, sy + bob, 4, 18))
    pygame.draw.rect(screen, trim, (sx,    sy + bob, 20, 2))
    pygame.draw.rect(screen, (245, 240, 225), (sx + 5, sy + bob, 10, 3))
    pygame.draw.rect(screen, skin, (sx + 2, sy - 10 + bob, 16, 12))
    pygame.draw.rect(screen, (40, 30, 20), (sx + 4,  sy - 7 + bob, 3, 3))
    pygame.draw.rect(screen, (40, 30, 20), (sx + 11, sy - 7 + bob, 3, 3))
    hat_dark = tuple(max(0, v - 30) for v in body)
    pygame.draw.rect(screen, hat_dark, (sx - 2, sy - 13 + bob, 24, 3))
    pygame.draw.rect(screen, body,     (sx + 3, sy - 19 + bob, 14, 7))
    pygame.draw.rect(screen, trim,     (sx + 3, sy - 13 + bob, 14, 2))
    plume_x = sx + 13 if facing == 1 else sx + 3
    pygame.draw.rect(screen, plume, (plume_x,     sy - 22 + bob, 4, 2))
    pygame.draw.rect(screen, plume, (plume_x + 1, sy - 24 + bob, 3, 2))


def _draw_court_noble(screen, sx, sy, bob, facing, skin, palace_type, lc):
    """Draw a dynasty-affiliated noble in their court's cultural style."""
    def _dim(c, f=0.72):  return tuple(int(v * f) for v in c)
    def _lite(c, a=55):   return tuple(min(255, v + a) for v in c)
    def _gold():          return (218, 175, 40)
    def _eyes():
        pygame.draw.rect(screen, (40, 30, 20), (sx + 4,  sy - 7 + bob, 3, 3))
        pygame.draw.rect(screen, (40, 30, 20), (sx + 11, sy - 7 + bob, 3, 3))

    _EAST_ASIAN  = {"east_asian", "chinese", "tang_imperial", "song_palace", "han_palace", "japanese"}
    _MED         = {"mediterranean", "byzantine", "incan", "mesoamerican"}
    _MID_EAST    = {"middle_eastern", "moorish", "persian"}
    _SOUTH_ASIAN = {"south_asian"}
    _AFRICAN     = {"african", "tibetan", "east_african"}

    if palace_type in _EAST_ASIAN:
        # Dark official's robe with leader_color sash band, tall wusha hat
        robe = _dim(lc, 0.35)
        pygame.draw.rect(screen, robe,    (sx, sy + bob, 20, 18))
        pygame.draw.rect(screen, _gold(), (sx, sy + 8 + bob, 20, 2))        # sash
        pygame.draw.rect(screen, _lite(lc, 40), (sx + 6, sy + bob, 8, 7))  # chest panel
        pygame.draw.rect(screen, skin,    (sx + 2, sy - 10 + bob, 16, 12))
        pygame.draw.rect(screen, (30, 20, 15), (sx + 2, sy - 12 + bob, 16, 3))
        _eyes()
        # Wusha mao (tall rectangular official hat)
        pygame.draw.rect(screen, (25, 20, 15), (sx - 1, sy - 14 + bob, 22, 3))  # brim
        pygame.draw.rect(screen, (25, 20, 15), (sx + 3, sy - 22 + bob, 14, 9))  # crown
        pygame.draw.rect(screen, _gold(),      (sx + 3, sy - 14 + bob, 14, 1))  # brim trim
        # Hanging hat wings (bianze)
        pygame.draw.rect(screen, (25, 20, 15), (sx - 4, sy - 13 + bob, 4, 2))
        pygame.draw.rect(screen, (25, 20, 15), (sx + 20, sy - 13 + bob, 4, 2))

    elif palace_type in _MED:
        # White tunic with vertical leader_color clavus stripe, simple laurel
        ivory = (245, 240, 225)
        pygame.draw.rect(screen, ivory,   (sx, sy + bob, 20, 18))
        pygame.draw.rect(screen, _dim(lc),(sx + 8, sy + bob, 4, 18))        # clavus stripe
        pygame.draw.rect(screen, _gold(), (sx + 14, sy + 1 + bob, 5, 4))   # shoulder brooch
        pygame.draw.rect(screen, lc,      (sx + 15, sy + 2 + bob, 3, 2))
        pygame.draw.rect(screen, skin,    (sx + 2, sy - 10 + bob, 16, 12))
        pygame.draw.rect(screen, (80, 55, 35), (sx + 2, sy - 12 + bob, 16, 3))
        _eyes()
        # Laurel wreath
        pygame.draw.rect(screen, (70, 140, 55), (sx + 2, sy - 14 + bob, 16, 2))
        for fx in (sx + 3, sx + 7, sx + 12, sx + 15):
            pygame.draw.rect(screen, (220, 180, 80), (fx, sy - 15 + bob, 2, 2))

    elif palace_type in _MID_EAST:
        # Kaftan in leader_color with gold border, wrapped turban
        robe = _dim(lc, 0.8)
        pygame.draw.rect(screen, robe,     (sx + 1, sy + bob, 18, 18))
        pygame.draw.rect(screen, _gold(),  (sx + 1, sy + bob, 2, 18))
        pygame.draw.rect(screen, _gold(),  (sx + 17, sy + bob, 2, 18))
        pygame.draw.rect(screen, _lite(lc, 40), (sx + 3, sy + 1 + bob, 14, 6))  # chest panel
        pygame.draw.rect(screen, skin,     (sx + 2, sy - 10 + bob, 16, 12))
        _eyes()
        # Simpler turban (no jewel — court official, not royalty)
        pygame.draw.rect(screen, (245, 240, 230), (sx + 1, sy - 18 + bob, 18, 8))
        pygame.draw.rect(screen, (245, 240, 230), (sx + 3, sy - 20 + bob, 14, 4))
        pygame.draw.rect(screen, _dim(lc, 0.8),   (sx + 1, sy - 15 + bob, 18, 2))

    elif palace_type in _SOUTH_ASIAN:
        # Sherwani jacket in leader_color with gold buttons, turban
        pygame.draw.rect(screen, _dim(lc), (sx + 1, sy + bob, 18, 18))
        for bx2 in range(sx + 9, sx + 10, 1):                              # center buttons
            for by2 in range(sy + 2, sy + 16, 4):
                pygame.draw.rect(screen, _gold(), (bx2, by2 + bob, 2, 2))
        pygame.draw.rect(screen, _gold(), (sx + 1, sy + bob, 18, 2))       # collar trim
        pygame.draw.rect(screen, skin,    (sx + 2, sy - 10 + bob, 16, 12))
        pygame.draw.rect(screen, (25, 18, 10), (sx + 2, sy - 12 + bob, 16, 3))
        _eyes()
        # Pagri turban in leader_color
        pygame.draw.rect(screen, lc,      (sx + 1, sy - 18 + bob, 18, 8))
        pygame.draw.rect(screen, _dim(lc),(sx + 1, sy - 15 + bob, 18, 2))  # fold line
        pygame.draw.rect(screen, _gold(), (sx + 6, sy - 19 + bob, 4, 2))   # brooch pin

    elif palace_type in _AFRICAN:
        # Formal wrap in leader_color with geometric dot pattern, bead collar
        base = _dim(lc, 0.8)
        pat  = _lite(lc, 50)
        pygame.draw.rect(screen, base, (sx, sy + bob, 20, 18))
        for row in range(0, 16, 4):
            for col in range(2, 18, 4):
                pygame.draw.rect(screen, pat, (sx + col, sy + row + bob, 2, 2))
        for bx2 in range(sx + 3, sx + 17, 2):                              # bead collar
            pygame.draw.rect(screen, _gold(), (bx2, sy + 1 + bob, 1, 2))
        pygame.draw.rect(screen, skin,    (sx + 2, sy - 10 + bob, 16, 12))
        pygame.draw.rect(screen, (20, 14, 8), (sx + 2, sy - 12 + bob, 16, 3))
        _eyes()
        # Beaded headband
        pygame.draw.rect(screen, _gold(), (sx + 2, sy - 13 + bob, 16, 2))
        for bx2 in range(sx + 3, sx + 18, 3):
            pygame.draw.rect(screen, lc, (bx2, sy - 13 + bob, 2, 2))

    else:
        # European court — doublet in leader_color with gold trim, plumed hat
        dark = _dim(lc, 0.75)
        pygame.draw.rect(screen, dark,    (sx, sy + bob, 20, 18))
        pygame.draw.rect(screen, _gold(), (sx + 8, sy + bob, 4, 18))       # center trim
        pygame.draw.rect(screen, _gold(), (sx, sy + bob, 20, 2))           # collar band
        pygame.draw.rect(screen, (245, 240, 225), (sx + 5, sy + bob, 10, 3))  # cravat
        pygame.draw.rect(screen, skin,    (sx + 2, sy - 10 + bob, 16, 12))
        _eyes()
        hat_dark = _dim(lc, 0.55)
        pygame.draw.rect(screen, hat_dark, (sx - 2, sy - 13 + bob, 24, 3))
        pygame.draw.rect(screen, dark,     (sx + 3, sy - 19 + bob, 14, 7))
        pygame.draw.rect(screen, _gold(),  (sx + 3, sy - 13 + bob, 14, 2))
        plume = _lite(lc, 70)
        plume_x = sx + 13 if facing == 1 else sx + 3
        pygame.draw.rect(screen, plume, (plume_x,     sy - 22 + bob, 4, 2))
        pygame.draw.rect(screen, plume, (plume_x + 1, sy - 24 + bob, 3, 2))


def draw_npc_pilgrim(screen, sx, sy, npc):
    bob = int(npc._bob_offset)
    facing = getattr(npc, 'facing', 1)
    c = getattr(npc, 'clothing', {})
    skin = c.get('skin', (235, 195, 150))
    robe = (170, 130, 70)
    sash = (130, 90, 45)
    pygame.draw.rect(screen, robe, (sx, sy + bob, 20, 18))
    pygame.draw.rect(screen, sash, (sx, sy + 9 + bob, 20, 2))
    pygame.draw.rect(screen, robe, (sx + 1, sy - 13 + bob, 18, 11))
    pygame.draw.rect(screen, skin, (sx + 4, sy - 7  + bob, 12, 6))
    pygame.draw.rect(screen, (40, 30, 20), (sx + 6,  sy - 5 + bob, 2, 2))
    pygame.draw.rect(screen, (40, 30, 20), (sx + 12, sy - 5 + bob, 2, 2))
    staff_x = sx + 19 if facing == 1 else sx - 1
    pygame.draw.rect(screen, (90, 65, 40), (staff_x, sy - 24 + bob, 2, 42))
    pygame.draw.rect(screen, (200, 175, 120), (staff_x - 1, sy - 24 + bob, 4, 2))
    bag_x = sx - 4 if facing == 1 else sx + 18
    pygame.draw.rect(screen, sash, (bag_x, sy + 6 + bob, 6, 6))
    pygame.draw.rect(screen, (60, 45, 25), (bag_x, sy + 6 + bob, 6, 1))


def draw_npc_drunkard(screen, sx, sy, npc):
    bob = int(npc._bob_offset)
    facing = getattr(npc, 'facing', 1)
    sway = int(math.sin(npc._bob_timer * 1.4) * 2)
    sx += sway
    c = getattr(npc, 'clothing', {})
    body  = c.get('body', (140, 95, 60))
    trim  = c.get('trim', (90, 55, 30))
    skin  = c.get('skin', (255, 195, 165))
    flush = (220, 110, 95)
    pygame.draw.rect(screen, body, (sx, sy + bob, 20, 18))
    pygame.draw.rect(screen, trim, (sx + 1, sy + 14 + bob, 18, 2))
    pygame.draw.rect(screen, trim, (sx + 4, sy + 16 + bob, 12, 2))
    pygame.draw.rect(screen, skin,  (sx + 2, sy - 10 + bob, 16, 12))
    pygame.draw.rect(screen, flush, (sx + 2, sy - 4 + bob, 4, 3))
    pygame.draw.rect(screen, flush, (sx + 14, sy - 4 + bob, 4, 3))
    pygame.draw.rect(screen, (40, 30, 20), (sx + 4,  sy - 6 + bob, 3, 1))
    pygame.draw.rect(screen, (40, 30, 20), (sx + 11, sy - 6 + bob, 3, 1))
    mug_x = sx + 18 if facing == 1 else sx - 4
    pygame.draw.rect(screen, (130, 110, 75), (mug_x, sy + 4 + bob, 6, 7))
    pygame.draw.rect(screen, (220, 200, 140), (mug_x + 1, sy + 4 + bob, 4, 2))
    pygame.draw.rect(screen, (130, 110, 75), (mug_x + 6, sy + 5 + bob, 1, 4))


def draw_npc_blacksmith(screen, sx, sy, npc):
    bob = int(npc._bob_offset)
    c = getattr(npc, 'clothing', {})
    body = c.get('body', (80, 55, 35))
    skin = c.get('skin', (200, 165, 115))
    soot = tuple(max(0, v - 40) for v in skin)
    pygame.draw.rect(screen, body,          (sx, sy + bob, 20, 18))
    pygame.draw.rect(screen, (80, 55, 30),  (sx + 6, sy + bob, 8, 18))
    pygame.draw.rect(screen, soot,          (sx + 2, sy - 10 + bob, 16, 12))
    pygame.draw.rect(screen, (30, 20, 10),  (sx + 4,  sy - 7 + bob, 3, 3))
    pygame.draw.rect(screen, (30, 20, 10),  (sx + 11, sy - 7 + bob, 3, 3))
    hx, hy = sx + 9, sy - 24 + bob
    pygame.draw.rect(screen, (150, 140, 130), (hx,     hy,     6, 3))
    pygame.draw.rect(screen, (130, 100,  60), (hx + 2, hy + 3, 2, 6))


def draw_npc_innkeeper(screen, sx, sy, npc):
    bob = int(npc._bob_offset)
    c = getattr(npc, 'clothing', {})
    body = c.get('body', (130, 80, 40))
    skin = c.get('skin', (255, 215, 160))
    pygame.draw.rect(screen, body,            (sx, sy + bob, 20, 18))
    pygame.draw.rect(screen, (240, 235, 220), (sx + 5, sy + bob, 10, 10))
    pygame.draw.rect(screen, skin,            (sx + 2, sy - 10 + bob, 16, 12))
    pygame.draw.rect(screen, (40, 30, 20),    (sx + 4,  sy - 7 + bob, 3, 3))
    pygame.draw.rect(screen, (40, 30, 20),    (sx + 11, sy - 7 + bob, 3, 3))
    mx, my = sx + 7, sy - 23 + bob
    pygame.draw.rect(screen, (200, 155, 100), (mx,     my,     8, 6))
    pygame.draw.rect(screen, (200, 155, 100), (mx + 7, my + 1, 3, 4))
    pygame.draw.rect(screen, (160, 210, 240), (mx + 1, my + 1, 6, 3))


def draw_npc_scholar(screen, sx, sy, npc):
    bob = int(npc._bob_offset)
    c = getattr(npc, 'clothing', {})
    body = c.get('body', (60, 60, 100))
    skin = c.get('skin', (255, 215, 160))
    fold = tuple(max(0, v - 30) for v in body)
    pygame.draw.rect(screen, body, (sx + 2, sy + bob, 16, 20))
    pygame.draw.rect(screen, fold, (sx + 8, sy + bob,  4, 20))
    pygame.draw.rect(screen, skin, (sx + 2, sy - 10 + bob, 16, 12))
    pygame.draw.circle(screen, (60, 50, 40), (sx + 6,  sy - 6 + bob), 3, 1)
    pygame.draw.circle(screen, (60, 50, 40), (sx + 13, sy - 6 + bob), 3, 1)
    pygame.draw.line(screen, (60, 50, 40),
                     (sx + 9, sy - 6 + bob), (sx + 10, sy - 6 + bob), 1)
    qx, qy = sx + 10, sy - 26 + bob
    pygame.draw.line(screen, (240, 235, 210), (qx, qy), (qx - 3, qy + 10), 2)
    pygame.draw.polygon(screen, (240, 235, 210),
                        [(qx, qy), (qx - 5, qy + 3), (qx - 2, qy + 5)])


# ---------------------------------------------------------------------------
# Royal family NPCs
# ---------------------------------------------------------------------------

def draw_npc_royal_spouse(screen, sx, sy, npc):
    bob    = int(npc._bob_offset)
    facing = getattr(npc, 'facing', 1)
    lc     = getattr(npc, 'leader_color', (160, 40, 80))
    ptype  = getattr(npc, 'palace_type',  'castle')

    def _dim(c, f=0.72):  return tuple(int(v * f) for v in c)
    def _lite(c, a=65):   return tuple(min(255, v + a) for v in c)
    def _gold():          return (218, 175, 40)

    _EAST_ASIAN  = {"east_asian", "chinese", "tang_imperial", "song_palace", "han_palace", "japanese"}
    _MED         = {"mediterranean", "byzantine", "incan", "mesoamerican"}
    _MID_EAST    = {"middle_eastern", "moorish", "persian"}
    _SOUTH_ASIAN = {"south_asian"}
    _AFRICAN     = {"african", "tibetan", "east_african"}

    if ptype in _EAST_ASIAN:
        # Layered hanfu — wide sleeves, high hair bun, gold hairpin, fan
        skin  = (240, 200, 155)
        inner = _lite(lc, 80)
        outer = _dim(lc)
        pygame.draw.rect(screen, outer,  (sx - 5, sy + 2 + bob,  8, 7))   # left sleeve
        pygame.draw.rect(screen, outer,  (sx + 17, sy + 2 + bob, 8, 7))   # right sleeve
        pygame.draw.rect(screen, inner,  (sx + 1, sy + bob, 18, 18))
        pygame.draw.rect(screen, _gold(),(sx + 4, sy + 10 + bob, 12, 2))  # gold sash
        pygame.draw.rect(screen, outer,  (sx, sy + 12 + bob, 20, 6))      # darker lower skirt
        pygame.draw.rect(screen, skin,   (sx + 2, sy - 10 + bob, 16, 12))
        pygame.draw.rect(screen, (30, 20, 15), (sx + 2, sy - 12 + bob, 16, 3))  # hair
        pygame.draw.rect(screen, (30, 20, 15), (sx + 5, sy - 18 + bob, 10, 5))  # bun
        pygame.draw.rect(screen, (30, 20, 15), (sx + 7, sy - 20 + bob,  6, 3))  # bun top
        pygame.draw.rect(screen, _gold(),(sx + 7,  sy - 22 + bob, 8, 2))        # hairpin bar
        pygame.draw.rect(screen, _gold(),(sx + 10, sy - 22 + bob, 2, 10))       # hairpin shaft
        pygame.draw.rect(screen, (35, 25, 15), (sx + 4,  sy - 7 + bob, 3, 3))
        pygame.draw.rect(screen, (35, 25, 15), (sx + 11, sy - 7 + bob, 3, 3))
        fan_x = sx + 21 if facing == 1 else sx - 7
        pygame.draw.rect(screen, inner,  (fan_x, sy + 2 + bob, 5, 7))
        pygame.draw.rect(screen, _gold(),(fan_x, sy + 2 + bob, 1, 7))
        pygame.draw.rect(screen, _gold(),(fan_x + 4, sy + 2 + bob, 1, 7))

    elif ptype in _MED:
        # Draped ivory stola — gold brooch, flower wreath, pearl earrings
        skin  = (220, 180, 125)
        ivory = (245, 240, 225)
        pygame.draw.rect(screen, ivory,   (sx, sy + bob, 20, 18))
        pygame.draw.rect(screen, _gold(), (sx, sy + bob, 2, 18))
        pygame.draw.rect(screen, _gold(), (sx + 18, sy + bob, 2, 10))
        pygame.draw.rect(screen, _dim(lc),(sx + 6, sy + 4 + bob, 8, 10))  # colored panel
        pygame.draw.rect(screen, _gold(), (sx + 14, sy + 1 + bob, 5, 4))  # brooch
        pygame.draw.rect(screen, lc,      (sx + 15, sy + 2 + bob, 3, 2))
        pygame.draw.rect(screen, skin,    (sx + 2, sy - 10 + bob, 16, 12))
        pygame.draw.rect(screen, (80, 55, 35), (sx + 2, sy - 12 + bob, 16, 3))
        pygame.draw.rect(screen, (70, 140, 55), (sx + 2, sy - 14 + bob, 16, 2))  # wreath
        for fx in (sx + 3, sx + 7, sx + 12, sx + 15):
            pygame.draw.rect(screen, (220, 180, 80), (fx, sy - 15 + bob, 2, 2))  # flowers
        pygame.draw.rect(screen, (245, 240, 230), (sx + 1,  sy - 8 + bob, 2, 2))  # earring L
        pygame.draw.rect(screen, (245, 240, 230), (sx + 17, sy - 8 + bob, 2, 2))  # earring R
        pygame.draw.rect(screen, (35, 25, 15), (sx + 4,  sy - 7 + bob, 3, 3))
        pygame.draw.rect(screen, (35, 25, 15), (sx + 11, sy - 7 + bob, 3, 3))

    elif ptype in _MID_EAST:
        # Gold-bordered kaftan — fabric turban with jeweled pin, nose stud
        skin = (190, 145, 95)
        robe = _dim(lc, 0.7)
        pygame.draw.rect(screen, robe,     (sx + 1, sy + bob, 18, 18))
        pygame.draw.rect(screen, _gold(),  (sx + 1, sy + bob, 2, 18))
        pygame.draw.rect(screen, _gold(),  (sx + 17, sy + bob, 2, 18))
        pygame.draw.rect(screen, _gold(),  (sx + 1, sy + 8 + bob, 18, 2))
        pygame.draw.rect(screen, _lite(lc, 50), (sx + 3, sy + 1 + bob, 14, 6))  # chest panel
        pygame.draw.rect(screen, skin,     (sx + 2, sy - 10 + bob, 16, 12))
        pygame.draw.rect(screen, (245, 240, 230), (sx + 1, sy - 18 + bob, 18, 8))  # turban
        pygame.draw.rect(screen, (245, 240, 230), (sx + 3, sy - 20 + bob, 14, 4))  # turban top
        pygame.draw.rect(screen, _dim(lc, 0.8), (sx + 1, sy - 15 + bob, 18, 2))   # wrap band
        pygame.draw.rect(screen, _gold(), (sx + 7, sy - 20 + bob, 6, 3))           # turban gem
        pygame.draw.rect(screen, lc,      (sx + 8, sy - 20 + bob, 4, 2))
        pygame.draw.rect(screen, (35, 25, 15), (sx + 4,  sy - 7 + bob, 3, 3))
        pygame.draw.rect(screen, (35, 25, 15), (sx + 11, sy - 7 + bob, 3, 3))
        pygame.draw.rect(screen, _gold(), (sx + 9, sy - 4 + bob, 1, 1))            # nose stud

    elif ptype in _SOUTH_ASIAN:
        # Sari — blouse + draped fabric + dupatta + bindi + gold necklace
        skin   = (175, 130, 80)
        blouse = _dim(lc, 0.8)
        sari   = _lite(lc, 40)
        pygame.draw.rect(screen, _dim(lc), (sx + 1, sy + 8 + bob, 18, 10))  # underskirt
        pygame.draw.rect(screen, sari,     (sx, sy + 4 + bob, 20, 14))
        pygame.draw.rect(screen, blouse,   (sx + 3, sy + bob, 14, 8))
        pygame.draw.rect(screen, _gold(),  (sx, sy + 4 + bob, 20, 2))
        pygame.draw.rect(screen, _gold(),  (sx, sy + 16 + bob, 20, 2))
        for i in range(5):                                                           # sari diagonal
            pygame.draw.rect(screen, _lite(lc, 80), (sx + 1 + i*3, sy + 5 + i + bob, 2, 2))
        pygame.draw.rect(screen, skin,     (sx + 2, sy - 10 + bob, 16, 12))
        pygame.draw.rect(screen, (25, 18, 10), (sx + 2, sy - 12 + bob, 16, 3))
        pygame.draw.rect(screen, _lite(lc, 90), (sx + 10, sy - 14 + bob, 10, 10))  # dupatta
        pygame.draw.rect(screen, (200, 40, 60), (sx + 8, sy - 12 + bob, 3, 2))     # bindi
        pygame.draw.rect(screen, _gold(),  (sx + 4, sy + 1 + bob, 12, 2))          # necklace
        pygame.draw.rect(screen, (35, 25, 15), (sx + 4,  sy - 7 + bob, 3, 3))
        pygame.draw.rect(screen, (35, 25, 15), (sx + 11, sy - 7 + bob, 3, 3))

    elif ptype in _AFRICAN:
        # Patterned wrap skirt, bead necklace, tall feathered headdress
        skin  = (100, 65, 35)
        base  = _dim(lc, 0.8)
        pat   = _lite(lc, 60)
        pat2  = (220, 180, 40)
        pygame.draw.rect(screen, base, (sx - 2, sy + 6 + bob, 24, 12))    # wide wrap skirt
        for row in range(0, 10, 3):
            for col in range(0, 22, 4):
                c2 = pat if (row + col) % 8 == 0 else pat2
                pygame.draw.rect(screen, c2, (sx - 2 + col, sy + 6 + row + bob, 2, 2))
        pygame.draw.rect(screen, base, (sx + 2, sy + bob, 16, 7))         # bodice
        for bx2 in range(sx + 3, sx + 17, 2):                             # bead necklace
            pygame.draw.rect(screen, _gold(), (bx2, sy + 1 + bob, 1, 2))
        pygame.draw.rect(screen, skin, (sx + 2, sy - 10 + bob, 16, 12))
        pygame.draw.rect(screen, (20, 14, 8), (sx + 2, sy - 12 + bob, 16, 3))
        pygame.draw.rect(screen, (240, 230, 210), (sx + 2, sy - 15 + bob, 16, 4))  # headdress base
        pygame.draw.rect(screen, _gold(),          (sx + 2, sy - 15 + bob, 16, 1))
        for i, fc in enumerate([lc, pat2, pat, pat2, lc]):                 # feathers
            fx  = sx + 2 + i * 4
            fh  = 10 if i == 2 else 8
            pygame.draw.rect(screen, fc,           (fx, sy - 15 - fh + bob, 3, fh))
            pygame.draw.rect(screen, _lite(fc, 40),(fx + 1, sy - 15 - fh + bob, 1, fh))
        pygame.draw.rect(screen, (35, 25, 15), (sx + 4,  sy - 7 + bob, 3, 3))
        pygame.draw.rect(screen, (35, 25, 15), (sx + 11, sy - 7 + bob, 3, 3))

    else:
        # European gown — puffed sleeves, fitted bodice, flared skirt, hennin hat + veil
        skin   = (240, 210, 165)
        bodice = _dim(lc, 0.75)
        skirt  = _dim(lc, 0.85)
        pygame.draw.rect(screen, bodice,  (sx - 3, sy + 1 + bob,  6, 7))   # left puff sleeve
        pygame.draw.rect(screen, bodice,  (sx + 17, sy + 1 + bob, 6, 7))   # right puff sleeve
        pygame.draw.rect(screen, _gold(), (sx - 2, sy + 3 + bob,  2, 3))   # sleeve trim L
        pygame.draw.rect(screen, _gold(), (sx + 18, sy + 3 + bob, 2, 3))   # sleeve trim R
        pygame.draw.rect(screen, bodice,  (sx + 2, sy + bob, 16, 9))       # fitted bodice
        pygame.draw.rect(screen, _gold(), (sx + 7, sy + bob, 6, 2))        # neckline trim
        pygame.draw.rect(screen, _gold(), (sx + 7, sy + 3 + bob, 6, 4))    # jeweled brooch
        pygame.draw.rect(screen, lc,      (sx + 8, sy + 4 + bob, 4, 2))
        pygame.draw.rect(screen, skirt,   (sx + 1, sy + 9 + bob, 18, 4))   # skirt upper
        pygame.draw.rect(screen, skirt,   (sx,     sy + 13 + bob, 20, 5))  # skirt lower (flared)
        pygame.draw.rect(screen, _gold(), (sx + 1, sy + 9 + bob, 18, 1))   # waist trim
        pygame.draw.rect(screen, skin,    (sx + 2, sy - 10 + bob, 16, 12))
        pygame.draw.rect(screen, (45, 30, 18), (sx + 2, sy - 12 + bob, 16, 3))
        pygame.draw.rect(screen, (35, 25, 15), (sx + 4,  sy - 7 + bob, 3, 3))
        pygame.draw.rect(screen, (35, 25, 15), (sx + 11, sy - 7 + bob, 3, 3))
        pygame.draw.rect(screen, _gold(), (sx + 3, sy - 14 + bob, 14, 2))  # gold circlet
        pygame.draw.rect(screen, lc,      (sx + 9, sy - 15 + bob, 2, 2))   # circlet gem
        pygame.draw.rect(screen, bodice,  (sx + 4, sy - 22 + bob, 12, 9))  # hennin base
        pygame.draw.rect(screen, bodice,  (sx + 6, sy - 27 + bob,  8, 6))  # hennin mid
        pygame.draw.rect(screen, bodice,  (sx + 8, sy - 30 + bob,  4, 4))  # hennin tip
        pygame.draw.rect(screen, _gold(), (sx + 4, sy - 22 + bob, 12, 2))  # hennin base trim
        veil_x = sx + 14 if facing == 1 else sx + 2
        veil   = _lite(bodice, 80)
        pygame.draw.rect(screen, veil, (veil_x, sy - 28 + bob, 4, 14))     # trailing veil


def draw_npc_royal_child(screen, sx, sy, npc):
    bob    = int(npc._bob_offset)
    facing = getattr(npc, 'facing', 1)
    lc     = getattr(npc, 'leader_color', (160, 40, 80))

    def _dim(c, f=0.75):  return tuple(int(v * f) for v in c)
    def _gold():          return (218, 175, 40)

    c    = getattr(npc, 'clothing', {})
    skin = c.get('skin', (255, 210, 160))
    body = _dim(lc, 0.8)
    legs = _dim(lc, 0.6)

    pygame.draw.rect(screen, legs,  (sx + 3,  sy + 10 + bob, 5, 8))   # left leg
    pygame.draw.rect(screen, legs,  (sx + 12, sy + 10 + bob, 5, 8))   # right leg
    pygame.draw.rect(screen, body,  (sx + 2, sy + bob, 16, 11))        # tunic
    pygame.draw.rect(screen, _gold(),(sx + 2, sy + bob, 16, 2))        # gold top band
    pygame.draw.rect(screen, (245, 240, 225), (sx + 6, sy + 2 + bob, 8, 3))  # cream collar
    pygame.draw.rect(screen, skin,  (sx + 3, sy - 9 + bob, 14, 10))   # head (slightly smaller)
    pygame.draw.rect(screen, (55, 40, 25), (sx + 3, sy - 11 + bob, 14, 3))   # hair
    pygame.draw.rect(screen, (35, 25, 15), (sx + 5,  sy - 6 + bob, 2, 2))    # eye L
    pygame.draw.rect(screen, (35, 25, 15), (sx + 11, sy - 6 + bob, 2, 2))    # eye R
    pygame.draw.rect(screen, (220, 150, 130), (sx + 4,  sy - 4 + bob, 2, 2)) # cheek L
    pygame.draw.rect(screen, (220, 150, 130), (sx + 12, sy - 4 + bob, 2, 2)) # cheek R
    pygame.draw.rect(screen, _gold(),(sx + 4, sy - 12 + bob, 12, 2))   # circlet
    pygame.draw.rect(screen, lc,     (sx + 9, sy - 13 + bob,  2, 2))   # circlet gem
    toy_x = sx + 19 if facing == 1 else sx - 2
    pygame.draw.rect(screen, (160, 130, 70),   (toy_x, sy + 3 + bob, 2, 8))  # scroll stick
    pygame.draw.rect(screen, (240, 230, 200),  (toy_x - 1, sy + 3 + bob, 4, 4))  # scroll roll
