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
    bob = int(npc._bob_offset)
    facing = getattr(npc, 'facing', 1)
    c = getattr(npc, 'clothing', {})
    body  = c.get('body', (90, 35, 110))
    trim  = c.get('trim', (220, 180, 70))
    skin  = c.get('skin', (250, 220, 185))
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
