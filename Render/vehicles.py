import pygame
from constants import BLOCK_SIZE


def fmt_fuel_time(fuel, fuel_rate):
    if fuel <= 0 or fuel_rate <= 0:
        return None
    secs = fuel / fuel_rate
    if secs >= 3600:
        return f"{int(secs // 3600)}h{int((secs % 3600) // 60):02d}m"
    if secs >= 60:
        return f"{int(secs // 60)}m"
    return f"{int(secs)}s"


def draw_arrows(screen, arrows, cam_x, cam_y):
    for arrow in arrows:
        if arrow.dead:
            continue
        ax = int(arrow.x) - cam_x
        ay = int(arrow.y) - cam_y
        tip_x = ax + (arrow.W if arrow.vx > 0 else -arrow.W)
        shaft_col = getattr(arrow, "color", (200, 170, 100))
        head_col  = tuple(max(0, c - 20) for c in shaft_col)
        pygame.draw.line(screen, shaft_col, (ax, ay), (tip_x, ay), 2)
        head_x = tip_x + (2 if arrow.vx > 0 else -2)
        pygame.draw.circle(screen, head_col, (head_x, ay), 2)


def draw_automations(screen, automations, cam_x, cam_y, font):
    for a in automations:
        a.draw(screen, cam_x, cam_y)
        label = fmt_fuel_time(a.fuel, a._def["fuel_rate"])
        if label:
            sx = int(a.x - cam_x)
            sy = int(a.y - cam_y)
            txt = font.render(label, True, (220, 160, 40))
            screen.blit(txt, (sx + a.W // 2 - txt.get_width() // 2, sy - 27))


def draw_farm_bots(screen, farm_bots, cam_x, cam_y, font):
    for fb in farm_bots:
        fb.draw(screen, cam_x, cam_y)
        label = fmt_fuel_time(fb.fuel, fb._def["fuel_rate"])
        if label:
            sx = int(fb.x - cam_x)
            sy = int(fb.y - cam_y)
            txt = font.render(label, True, (220, 160, 40))
            screen.blit(txt, (sx + fb.W // 2 - txt.get_width() // 2, sy - 22))


def _draw_backhoe(screen, bh, cam_x, cam_y, font, is_mounted=False):
    sx = int(bh.x - cam_x)
    sy = int(bh.y - cam_y)
    W, H = bh.W, bh.H

    BODY_COLOR = (210, 160, 30)
    BODY_DARK  = (130, 95, 15)
    CAB_COLOR  = (240, 200, 50)

    body_rect = (sx, sy + H // 3, W, H * 2 // 3)
    pygame.draw.rect(screen, BODY_COLOR, body_rect)
    pygame.draw.rect(screen, BODY_DARK, body_rect, 2)

    cab_rect = (sx + 2, sy, W // 2, H // 2 + 4)
    pygame.draw.rect(screen, CAB_COLOR, cab_rect)
    pygame.draw.rect(screen, BODY_DARK, cab_rect, 2)
    pygame.draw.rect(screen, (180, 230, 240), (sx + 5, sy + 3, W // 2 - 8, H // 3))

    wheel_y = sy + H - 5
    for wx in (sx + 9, sx + W - 9):
        pygame.draw.circle(screen, (30, 30, 30), (wx, wheel_y), 6)
        pygame.draw.circle(screen, (80, 80, 80), (wx, wheel_y), 3)

    cbx, cby = bh.center_block()
    body_cx = int(cbx * BLOCK_SIZE - cam_x + BLOCK_SIZE // 2)
    body_cy = int(cby * BLOCK_SIZE - cam_y + BLOCK_SIZE // 2)
    tbx, tby = bh.arm_target_block()
    tip_x = int(tbx * BLOCK_SIZE - cam_x + BLOCK_SIZE // 2)
    tip_y = int(tby * BLOCK_SIZE - cam_y + BLOCK_SIZE // 2)
    pygame.draw.line(screen, BODY_DARK,  (body_cx, body_cy), (tip_x, tip_y), 4)
    pygame.draw.line(screen, BODY_COLOR, (body_cx, body_cy), (tip_x, tip_y), 2)
    pygame.draw.rect(screen, (60, 50, 20), (tip_x - 4, tip_y - 4, 8, 8))
    pygame.draw.rect(screen, BODY_DARK, (tip_x - 4, tip_y - 4, 8, 8), 1)

    hx = tbx * BLOCK_SIZE - int(cam_x)
    hy = tby * BLOCK_SIZE - int(cam_y)
    if is_mounted:
        pygame.draw.rect(screen, (255, 200, 0), (hx, hy, BLOCK_SIZE, BLOCK_SIZE), 3)
    else:
        pygame.draw.rect(screen, (160, 120, 0), (hx, hy, BLOCK_SIZE, BLOCK_SIZE), 1)

    prog = bh.mine_progress
    if prog > 0:
        pygame.draw.rect(screen, (30, 30, 30), (hx, hy + BLOCK_SIZE + 1, BLOCK_SIZE, 3))
        pygame.draw.rect(screen, (80, 200, 80),
                         (hx, hy + BLOCK_SIZE + 1, int(BLOCK_SIZE * prog), 3))

    frac = bh.fuel / bh.FUEL_TANK if bh.FUEL_TANK > 0 else 0
    pygame.draw.rect(screen, (30, 30, 30), (sx, sy - 6, W, 4))
    pygame.draw.rect(screen, (200, 140, 30), (sx, sy - 6, int(W * frac), 4))

    if is_mounted:
        hint = font.render("[E] Dismount", True, (255, 220, 100))
        screen.blit(hint, (sx + W // 2 - hint.get_width() // 2, sy - 22))


def draw_backhoes(screen, backhoes, cam_x, cam_y, font, player):
    for bh in backhoes:
        _draw_backhoe(screen, bh, cam_x, cam_y, font,
                      is_mounted=(player.mounted_machine is bh))


def draw_elevator_cars(screen, elevator_cars, cam_x, cam_y, font, player=None):
    for car in elevator_cars:
        sx = int(car.shaft_x * BLOCK_SIZE - cam_x)
        sy = int(car.car_y - cam_y)
        W, H = car.W, car.H
        pygame.draw.rect(screen, (85, 88, 108), (sx, sy, W, H))
        pygame.draw.rect(screen, (130, 135, 160), (sx, sy, W, H), 2)
        pygame.draw.rect(screen, (100, 104, 128), (sx + 2, sy + 4, 3, H - 8))
        pygame.draw.rect(screen, (100, 104, 128), (sx + W - 5, sy + 4, 3, H - 8))
        pygame.draw.rect(screen, (55, 55, 65), (sx + W // 2 - 2, sy - 4, 4, 6))
        if player is not None and car.in_range(player):
            if player.riding_elevator is car:
                hint = "[W/S] Change floor  [E] Exit"
            elif car.state == "idle":
                car_by = int(round(car.car_y / BLOCK_SIZE))
                nearby_stop = player.get_nearby_elevator_stop()
                if nearby_stop is not None and nearby_stop[0] == car.shaft_x and nearby_stop[1] == car_by:
                    hint = "[E] Board  [Q] Deconstruct"
                else:
                    hint = "[E] Call Elevator  [Q] Deconstruct"
            else:
                hint = "Arriving..."
            txt = font.render(hint, True, (220, 220, 240))
            screen.blit(txt, (sx + W // 2 - txt.get_width() // 2, sy - 18))


def draw_minecarts(screen, minecarts, cam_x, cam_y, font, player=None):
    for cart in minecarts:
        sx = int(cart.cart_x - cam_x)
        sy = int(cart.cart_y - cam_y)
        W, H = cart.W, cart.H
        pygame.draw.rect(screen, (90, 75, 55), (sx, sy, W, H))
        pygame.draw.rect(screen, (140, 120, 90), (sx, sy, W, H), 2)
        pygame.draw.rect(screen, (55, 45, 35), (sx + 4, sy + 4, W - 8, H - 10))
        wheel_y = sy + H - 3
        for wx in (sx + 6, sx + W - 6):
            pygame.draw.circle(screen, (50, 40, 30), (wx, wheel_y), 4)
            pygame.draw.circle(screen, (110, 100, 80), (wx, wheel_y), 2)
        pygame.draw.rect(screen, (80, 70, 55), (sx + 6, wheel_y - 1, W - 12, 2))
        if player is not None and cart.in_range(player):
            if player.riding_minecart is cart:
                hint = "[A/D] Move  [S] Stop  [E] Exit"
            elif cart.state == "idle":
                cart_bx = int(round(cart.cart_x / BLOCK_SIZE))
                nearby_stop = player.get_nearby_mine_track_stop()
                if nearby_stop is not None and nearby_stop[0] == cart_bx and nearby_stop[1] == cart.track_by:
                    hint = "[E] Board"
                else:
                    hint = "[E] Call Cart"
            else:
                hint = "Arriving..."
            txt = font.render(hint, True, (240, 220, 160))
            screen.blit(txt, (sx + W // 2 - txt.get_width() // 2, sy - 18))
