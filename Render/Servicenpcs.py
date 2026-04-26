import pygame


def draw_npc_quest(screen, sx, sy, npc, font):
    bob = int(npc._bob_offset)
    c = getattr(npc, 'clothing', {})
    body = c.get('body', (190, 140, 70))
    skin = c.get('skin', (255, 215, 160))
    trim = c.get('trim', (130,  90, 30))
    # Body + belt
    pygame.draw.rect(screen, body, (sx, sy + bob, 20, 18))
    pygame.draw.rect(screen, trim, (sx, sy + 11 + bob, 20, 3))
    # Head
    pygame.draw.rect(screen, skin, (sx + 2, sy - 10 + bob, 16, 12))
    # Eyes
    pygame.draw.rect(screen, (40, 30, 20), (sx + 4,  sy - 7 + bob, 3, 3))
    pygame.draw.rect(screen, (40, 30, 20), (sx + 11, sy - 7 + bob, 3, 3))
    # Exclamation marker
    txt = font.render("!", True, (255, 220, 30))
    screen.blit(txt, (sx + 7, sy - 24 + bob))


def draw_npc_trade(screen, sx, sy, npc, font):
    bob = int(npc._bob_offset)
    c = getattr(npc, 'clothing', {})
    body = c.get('body', (60, 120, 175))
    skin = c.get('skin', (255, 215, 160))
    trim = c.get('trim', (40,  80, 130))
    # Body + lapel
    pygame.draw.rect(screen, body, (sx, sy + bob, 20, 18))
    pygame.draw.rect(screen, trim, (sx + 8, sy + bob, 4, 12))
    # Head
    pygame.draw.rect(screen, skin, (sx + 2, sy - 10 + bob, 16, 12))
    # Eyes
    pygame.draw.rect(screen, (40, 30, 20), (sx + 4,  sy - 7 + bob, 3, 3))
    pygame.draw.rect(screen, (40, 30, 20), (sx + 11, sy - 7 + bob, 3, 3))
    # Dollar marker
    txt = font.render("$", True, (80, 230, 120))
    screen.blit(txt, (sx + 6, sy - 24 + bob))


def draw_npc_herbalist(screen, sx, sy, npc):
    bob = int(npc._bob_offset)
    c = getattr(npc, 'clothing', {})
    body = c.get('body', (60, 140, 70))
    skin = c.get('skin', (255, 215, 160))
    trim = c.get('trim', (90,  55, 20))
    # Body + belt
    pygame.draw.rect(screen, body, (sx, sy + bob, 20, 18))
    pygame.draw.rect(screen, trim, (sx, sy + 11 + bob, 20, 3))
    # Head
    pygame.draw.rect(screen, skin, (sx + 2, sy - 10 + bob, 16, 12))
    # Eyes
    pygame.draw.rect(screen, (40, 30, 20), (sx + 4,  sy - 7 + bob, 3, 3))
    pygame.draw.rect(screen, (40, 30, 20), (sx + 11, sy - 7 + bob, 3, 3))
    # Flower indicator
    fx, fy = sx + 10, sy - 22 + bob
    for dx, dy in ((0, -4), (0, 4), (-4, 0), (4, 0)):
        pygame.draw.circle(screen, (100, 220, 100), (fx + dx, fy + dy), 2)
    pygame.draw.circle(screen, (255, 230, 50), (fx, fy), 2)


def draw_npc_jeweler(screen, sx, sy, npc):
    bob = int(npc._bob_offset)
    c = getattr(npc, 'clothing', {})
    body = c.get('body', (110, 50, 160))
    skin = c.get('skin', (255, 215, 160))
    coat  = tuple(max(0, min(255, (v + 110) // 2)) for v in body)
    coat2 = tuple(max(0, min(255, v + 50)) for v in coat)
    # Body + trim stripe
    pygame.draw.rect(screen, coat,  (sx, sy + bob, 20, 18))
    pygame.draw.rect(screen, coat2, (sx + 8, sy + bob, 4, 18))
    # Head
    pygame.draw.rect(screen, skin, (sx + 2, sy - 10 + bob, 16, 12))
    # Eyes
    pygame.draw.rect(screen, (40, 30, 20), (sx + 4,  sy - 7 + bob, 3, 3))
    pygame.draw.rect(screen, (40, 30, 20), (sx + 11, sy - 7 + bob, 3, 3))
    # Diamond indicator
    gx, gy = sx + 10, sy - 22 + bob
    pygame.draw.polygon(screen, (190, 110, 255),
                        [(gx, gy - 5), (gx + 4, gy), (gx, gy + 5), (gx - 4, gy)])
    pygame.draw.polygon(screen, (230, 180, 255),
                        [(gx, gy - 5), (gx + 4, gy), (gx, gy + 5), (gx - 4, gy)], 1)


def draw_npc_royal_curator(screen, sx, sy, npc):
    bob = int(npc._bob_offset)
    c = getattr(npc, 'clothing', {})
    skin = c.get('skin', (255, 215, 160))
    # Crimson-gold robe with gold sash
    pygame.draw.rect(screen, (160, 40, 30), (sx, sy + bob, 20, 18))
    pygame.draw.rect(screen, (220, 175, 40), (sx, sy + 12 + bob, 20, 4))
    pygame.draw.rect(screen, (220, 175, 40), (sx + 5, sy + bob, 10, 12))
    # Head
    pygame.draw.rect(screen, skin, (sx + 2, sy - 10 + bob, 16, 12))
    pygame.draw.rect(screen, (40, 30, 20), (sx + 4,  sy - 7 + bob, 3, 3))
    pygame.draw.rect(screen, (40, 30, 20), (sx + 11, sy - 7 + bob, 3, 3))
    # Gold crown marker
    cx, cy = sx + 10, sy - 22 + bob
    pygame.draw.polygon(screen, (220, 175, 40),
                        [(cx - 5, cy + 4), (cx - 5, cy), (cx - 2, cy - 3),
                         (cx, cy + 1), (cx + 2, cy - 3), (cx + 5, cy), (cx + 5, cy + 4)])
    pygame.draw.rect(screen, (255, 215, 80), (cx - 1, cy + 2, 2, 2))


def draw_npc_royal_florist(screen, sx, sy, npc):
    bob = int(npc._bob_offset)
    c = getattr(npc, 'clothing', {})
    skin = c.get('skin', (255, 215, 160))
    # Deep green robe with gold trim
    pygame.draw.rect(screen, (30, 100, 50), (sx, sy + bob, 20, 18))
    pygame.draw.rect(screen, (220, 175, 40), (sx, sy + 13 + bob, 20, 3))
    pygame.draw.rect(screen, (220, 175, 40), (sx + 7, sy + bob, 6, 13))
    # Head
    pygame.draw.rect(screen, skin, (sx + 2, sy - 10 + bob, 16, 12))
    pygame.draw.rect(screen, (40, 30, 20), (sx + 4,  sy - 7 + bob, 3, 3))
    pygame.draw.rect(screen, (40, 30, 20), (sx + 11, sy - 7 + bob, 3, 3))
    # Crown with flower accent
    cx, cy = sx + 10, sy - 22 + bob
    pygame.draw.polygon(screen, (220, 175, 40),
                        [(cx - 5, cy + 4), (cx - 5, cy), (cx - 2, cy - 3),
                         (cx, cy + 1), (cx + 2, cy - 3), (cx + 5, cy), (cx + 5, cy + 4)])
    pygame.draw.circle(screen, (230, 80, 120), (cx, cy - 2), 2)


def draw_npc_royal_jeweler(screen, sx, sy, npc):
    bob = int(npc._bob_offset)
    c = getattr(npc, 'clothing', {})
    skin = c.get('skin', (255, 215, 160))
    # Deep navy robe with heavy gold banding
    pygame.draw.rect(screen, (30, 40, 120), (sx, sy + bob, 20, 18))
    pygame.draw.rect(screen, (220, 175, 40), (sx, sy + 12 + bob, 20, 4))
    pygame.draw.rect(screen, (220, 175, 40), (sx, sy + bob, 20, 3))
    # Head
    pygame.draw.rect(screen, skin, (sx + 2, sy - 10 + bob, 16, 12))
    pygame.draw.rect(screen, (40, 30, 20), (sx + 4,  sy - 7 + bob, 3, 3))
    pygame.draw.rect(screen, (40, 30, 20), (sx + 11, sy - 7 + bob, 3, 3))
    # Crown with gem accent
    cx, cy = sx + 10, sy - 22 + bob
    pygame.draw.polygon(screen, (220, 175, 40),
                        [(cx - 5, cy + 4), (cx - 5, cy), (cx - 2, cy - 3),
                         (cx, cy + 1), (cx + 2, cy - 3), (cx + 5, cy), (cx + 5, cy + 4)])
    pygame.draw.polygon(screen, (160, 220, 255),
                        [(cx, cy - 4), (cx + 3, cy - 1), (cx, cy + 2), (cx - 3, cy - 1)])


def draw_npc_royal_paleontologist(screen, sx, sy, npc):
    bob = int(npc._bob_offset)
    c = getattr(npc, 'clothing', {})
    skin = c.get('skin', (255, 215, 160))
    # Earthy tan robes with gold trim
    pygame.draw.rect(screen, (165, 130, 75), (sx, sy + bob, 20, 18))
    pygame.draw.rect(screen, (220, 175, 40), (sx, sy + 13 + bob, 20, 3))
    pygame.draw.rect(screen, (220, 175, 40), (sx + 8, sy + bob, 4, 13))
    # Head
    pygame.draw.rect(screen, skin, (sx + 2, sy - 10 + bob, 16, 12))
    pygame.draw.rect(screen, (40, 30, 20), (sx + 4,  sy - 7 + bob, 3, 3))
    pygame.draw.rect(screen, (40, 30, 20), (sx + 11, sy - 7 + bob, 3, 3))
    # Crown with bone/fossil accent
    cx, cy = sx + 10, sy - 22 + bob
    pygame.draw.polygon(screen, (220, 175, 40),
                        [(cx - 5, cy + 4), (cx - 5, cy), (cx - 2, cy - 3),
                         (cx, cy + 1), (cx + 2, cy - 3), (cx + 5, cy), (cx + 5, cy + 4)])
    pygame.draw.rect(screen, (235, 225, 200), (cx - 1, cy - 1, 2, 3))


def draw_npc_royal_angler(screen, sx, sy, npc):
    bob = int(npc._bob_offset)
    c = getattr(npc, 'clothing', {})
    skin = c.get('skin', (255, 215, 160))
    # Deep teal robes with gold trim — maritime royal
    pygame.draw.rect(screen, (25, 90, 110), (sx, sy + bob, 20, 18))
    pygame.draw.rect(screen, (220, 175, 40), (sx, sy + 13 + bob, 20, 3))
    pygame.draw.rect(screen, (60, 180, 200), (sx + 7, sy + bob, 6, 13))
    # Head
    pygame.draw.rect(screen, skin, (sx + 2, sy - 10 + bob, 16, 12))
    pygame.draw.rect(screen, (40, 30, 20), (sx + 4,  sy - 7 + bob, 3, 3))
    pygame.draw.rect(screen, (40, 30, 20), (sx + 11, sy - 7 + bob, 3, 3))
    # Crown with fish-scale accent
    cx, cy = sx + 10, sy - 22 + bob
    pygame.draw.polygon(screen, (220, 175, 40),
                        [(cx - 5, cy + 4), (cx - 5, cy), (cx - 2, cy - 3),
                         (cx, cy + 1), (cx + 2, cy - 3), (cx + 5, cy), (cx + 5, cy + 4)])
    pygame.draw.ellipse(screen, (80, 200, 220), (cx - 2, cy - 2, 4, 3))


def draw_npc_merchant(screen, sx, sy, npc):
    bob = int(npc._bob_offset)
    c = getattr(npc, 'clothing', {})
    body = c.get('body', (90, 55, 25))
    skin = c.get('skin', (255, 215, 160))
    trim = c.get('trim', (120, 75, 35))
    lapel = tuple(min(255, v + 30) for v in body)
    # Body + lapel
    pygame.draw.rect(screen, body,  (sx, sy + bob, 20, 18))
    pygame.draw.rect(screen, lapel, (sx + 8, sy + bob, 4, 12))
    # Head
    pygame.draw.rect(screen, skin, (sx + 2, sy - 10 + bob, 16, 12))
    # Eyes
    pygame.draw.rect(screen, (40, 30, 20), (sx + 4,  sy - 7 + bob, 3, 3))
    pygame.draw.rect(screen, (40, 30, 20), (sx + 11, sy - 7 + bob, 3, 3))
    # Gold coin marker
    gx, gy = sx + 10, sy - 21 + bob
    pygame.draw.circle(screen, (220, 175, 40), (gx, gy), 5)
    pygame.draw.circle(screen, (180, 140, 20), (gx, gy), 5, 1)


def draw_npc_outpost_keeper(screen, sx, sy, npc):
    bob = int(npc._bob_offset)
    c = getattr(npc, 'clothing', {})
    body = c.get('body', (80, 120, 80))
    skin = c.get('skin', (220, 180, 130))
    trim = c.get('trim', (55, 85, 55))
    # Tunic + trim stripe
    pygame.draw.rect(screen, body, (sx, sy + bob, 20, 18))
    pygame.draw.rect(screen, trim, (sx + 7, sy + bob, 3, 18))
    # Head
    pygame.draw.rect(screen, skin, (sx + 2, sy - 10 + bob, 16, 12))
    # Eyes
    pygame.draw.rect(screen, (40, 30, 20), (sx + 4,  sy - 7 + bob, 3, 3))
    pygame.draw.rect(screen, (40, 30, 20), (sx + 11, sy - 7 + bob, 3, 3))
    # Small green leaf marker above head
    pygame.draw.circle(screen, (70, 155, 80), (sx + 10, sy - 20 + bob), 4)
