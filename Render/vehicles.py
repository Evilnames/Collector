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
    import math
    for arrow in arrows:
        if arrow.dead:
            continue
        ax = int(arrow.x) - cam_x
        ay = int(arrow.y) - cam_y
        angle = math.atan2(arrow.vy, arrow.vx)
        cos_a, sin_a = math.cos(angle), math.sin(angle)
        tip_x = ax + int(cos_a * arrow.W)
        tip_y = ay + int(sin_a * arrow.W)
        shaft_col = getattr(arrow, "color", (200, 170, 100))
        head_col  = tuple(max(0, c - 20) for c in shaft_col)
        pygame.draw.line(screen, shaft_col, (ax, ay), (tip_x, tip_y), 2)
        head_x = tip_x + int(cos_a * 2)
        head_y = tip_y + int(sin_a * 2)
        pygame.draw.circle(screen, head_col, (head_x, head_y), 2)


def draw_aim_preview(screen, player, mouse_scr, cam_x, cam_y):
    """Trajectory dots + power bar while the player is holding to aim."""
    import math
    state = player._aim_state
    if state is None:
        return

    from constants import GRAVITY, MAX_FALL, PLAYER_W, PLAYER_H, BLOCK_SIZE
    from hunting import ARROW_SPEED, ARROW_MAX_X, SPEAR_SPEED, SPEAR_MAX_X
    from items import ITEMS

    AIM_MAX_TIME  = player._AIM_MAX_TIME
    AIM_MIN_POWER = player._AIM_MIN_POWER
    power = AIM_MIN_POWER + (1.0 - AIM_MIN_POWER) * (state["timer"] / AIM_MAX_TIME)

    px_s = int(player.x + PLAYER_W / 2) - cam_x
    py_s = int(player.y + PLAYER_H / 2) - cam_y

    mx, my = mouse_scr
    dx = mx - px_s
    dy = my - py_s
    if abs(dx) < 1:
        dx = float(player.facing)
    angle = math.atan2(dy, abs(dx))
    angle = max(-math.pi / 3, min(math.pi / 3, angle))

    tool      = player.hotbar[player.selected_slot]
    tool_data = ITEMS.get(tool or "", {})

    if state["type"] == "bow":
        base_speed    = tool_data.get("arrow_speed", ARROW_SPEED)
        bow_range     = tool_data.get("arrow_range", None)
        base_range    = (bow_range * BLOCK_SIZE) if bow_range else ARROW_MAX_X
        gravity_scale = 0.18
        fall_cap      = MAX_FALL * 0.35
    else:
        base_speed    = tool_data.get("spear_speed", SPEAR_SPEED)
        gun_range     = tool_data.get("spear_range", None)
        base_range    = (gun_range * BLOCK_SIZE) if gun_range else SPEAR_MAX_X
        gravity_scale = 0.30
        fall_cap      = MAX_FALL * 0.50

    speed_val = base_speed * power
    cvx = player.facing * speed_val * math.cos(angle)
    cvy = speed_val * math.sin(angle)
    max_range = base_range * power

    # Trajectory dots — simulate every 3 ticks
    sx = float(player.x + PLAYER_W / 2)
    sy = float(player.y + PLAYER_H / 2)
    dist = 0.0
    for i in range(28):
        for _ in range(3):
            cvy = min(cvy + GRAVITY * gravity_scale, fall_cap)
            sx += cvx
            sy += cvy
            dist += abs(cvx)
        if dist >= max_range:
            break
        dot_x = int(sx) - cam_x
        dot_y = int(sy) - cam_y
        radius = max(1, 3 - i // 9)
        alpha  = max(80, 255 - int(175 * (dist / max_range)))
        col    = (255, min(255, 200 + int(55 * (1 - power))), 50)
        pygame.draw.circle(screen, col, (dot_x, dot_y), radius)

    # Power bar above player
    BAR_W, BAR_H = 40, 5
    bx = px_s - BAR_W // 2
    by = py_s - 32
    pygame.draw.rect(screen, (40, 40, 40), (bx - 1, by - 1, BAR_W + 2, BAR_H + 2))
    fill_w = max(1, int(BAR_W * power))
    r = min(255, int(510 * min(1.0, power)))
    g = min(255, int(510 * max(0.0, 1.0 - power)))
    pygame.draw.rect(screen, (r, g, 30), (bx, by, fill_w, BAR_H))


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
