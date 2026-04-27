import pygame
from constants import SCREEN_W, SCREEN_H
from cheese import (
    apply_curd_result, apply_press_result, apply_aging_result,
    get_cheese_output_id,
    CHEESE_TYPE_DESCS, CHEESE_TYPE_COLORS, CHEESE_TYPE_AGING,
    CHEESE_PRESS_INGREDIENTS,
    BUFF_DESCS, BIOME_DISPLAY_NAMES, ANIMAL_MILK_PROFILES,
    _CODEX_BIOMES, BIOME_CHEESE_PROFILES,
)

_SECS_PER_AGING_DAY = 5.0

_ACCENT  = (210, 185, 110)
_DARK_BG = ( 28,  22,  12)
_CELL_BG = ( 40,  32,  18)
_TITLE_C = (240, 220, 160)
_LABEL_C = (195, 170, 110)
_DIM_C   = ( 90,  72,  40)
_HINT_C  = (130, 110,  65)

_ANIMAL_COLORS = {
    "cow":   (200, 180, 140),
    "goat":  (185, 195, 175),
    "sheep": (230, 225, 215),
}


class CheeseMixin:

    # ─────────────────────────────────────────────────────────────────────────
    # DAIRY VAT
    # ─────────────────────────────────────────────────────────────────────────

    def _draw_dairy_vat(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("DAIRY VAT", True, _TITLE_C)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, _HINT_C)
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        if self._vat_phase == "select_milk":
            self._vat_select_rects.clear()
            milk_items = {"milk": "cow", "goat_milk": "goat", "sheep_milk": "sheep"}
            available = [(k, at) for k, at in milk_items.items() if player.inventory.get(k, 0) > 0]
            # Also need corresponding cheese objects in state "milk"
            pending = [c for c in player.cheese_wheels if c.state == "milk"]
            if not available or not pending:
                msg = self.font.render("No milk! Use a bucket on a cow, goat, or sheep.", True, _LABEL_C)
                self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2))
                return
            sub = self.small.render("Select milk to curdle:", True, _LABEL_C)
            self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 32))
            CELL_W, CELL_H, GAP, COLS = 220, 60, 10, 4
            gx0 = (SCREEN_W - (COLS * CELL_W + (COLS - 1) * GAP)) // 2
            shown = 0
            for item_id, animal_type in available:
                matching = [c for c in pending if c.animal_type == animal_type]
                if not matching:
                    continue
                cheese = matching[0]
                col_i = shown % COLS
                row_i = shown // COLS
                rx = gx0 + col_i * (CELL_W + GAP)
                ry = 55 + row_i * (CELL_H + GAP)
                rect = pygame.Rect(rx, ry, CELL_W, CELL_H)
                self._vat_select_rects[cheese.uid] = (rect, cheese, item_id)
                pygame.draw.rect(self.screen, _CELL_BG, rect)
                pygame.draw.rect(self.screen, _ACCENT, rect, 2)
                acolor = _ANIMAL_COLORS.get(animal_type, _LABEL_C)
                nm = self.small.render(f"{animal_type.capitalize()} Milk", True, acolor)
                self.screen.blit(nm, (rx + 6, ry + 8))
                biome_nm = BIOME_DISPLAY_NAMES.get(cheese.origin_biome, cheese.origin_biome)
                bn = self.small.render(biome_nm, True, _HINT_C)
                self.screen.blit(bn, (rx + 6, ry + 28))
                cnt = self.small.render(f"x{player.inventory.get(item_id, 0)}", True, _DIM_C)
                self.screen.blit(cnt, (rx + CELL_W - cnt.get_width() - 6, ry + 8))
                shown += 1
                if shown >= 16:
                    break

        elif self._vat_phase == "mini_game":
            self._draw_vat_minigame(player, dt)

        elif self._vat_phase == "result":
            self._draw_vat_result(player)

    def _draw_vat_minigame(self, player, dt):
        cx, cy = SCREEN_W // 2, SCREEN_H // 2

        # Advance game state
        if not self._vat_game_done:
            keys = pygame.key.get_pressed()
            # Heat key: W or UP
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self._vat_temp = min(1.0, self._vat_temp + 1.8 * dt)
            else:
                self._vat_temp = max(0.0, self._vat_temp - 0.6 * dt)
            # Temp score: how long we stayed in the ideal band
            if 0.40 <= self._vat_temp <= 0.65:
                self._vat_temp_score = min(1.0, self._vat_temp_score + 0.5 * dt)
            else:
                if self._vat_temp > 0.75:
                    self._vat_penalties += dt * 0.5
            # Culture window: pulsing readiness
            self._vat_culture_pulse = (self._vat_culture_pulse + dt * 1.2) % 1.0
            # Culture already added
            if self._vat_culture_added:
                self._vat_finish_timer -= dt
                if self._vat_finish_timer <= 0:
                    self._vat_game_done = True

        # Draw temperature gauge
        gauge_x, gauge_y, gauge_h = cx - 200, cy - 80, 160
        pygame.draw.rect(self.screen, _CELL_BG, (gauge_x, gauge_y, 28, gauge_h))
        fill_h = int(gauge_h * self._vat_temp)
        tc = (
            (220, 80, 60) if self._vat_temp > 0.75 else
            (100, 200, 100) if 0.40 <= self._vat_temp <= 0.65 else
            (100, 150, 220)
        )
        pygame.draw.rect(self.screen, tc, (gauge_x, gauge_y + gauge_h - fill_h, 28, fill_h))
        pygame.draw.rect(self.screen, _ACCENT, (gauge_x, gauge_y, 28, gauge_h), 2)
        # Ideal zone marker
        ideal_y0 = gauge_y + gauge_h - int(gauge_h * 0.65)
        ideal_y1 = gauge_y + gauge_h - int(gauge_h * 0.40)
        pygame.draw.rect(self.screen, (100, 200, 100, 80),
                         pygame.Rect(gauge_x, ideal_y0, 28, ideal_y1 - ideal_y0))
        pygame.draw.line(self.screen, (100, 200, 100), (gauge_x - 4, ideal_y0), (gauge_x + 32, ideal_y0))
        pygame.draw.line(self.screen, (100, 200, 100), (gauge_x - 4, ideal_y1), (gauge_x + 32, ideal_y1))

        tl = self.small.render("TEMP", True, _LABEL_C)
        self.screen.blit(tl, (gauge_x, gauge_y - 18))
        kl = self.small.render("Hold W/↑ to heat", True, _HINT_C)
        self.screen.blit(kl, (gauge_x - 30, gauge_y + gauge_h + 6))

        # Culture readiness indicator
        pulse_v = abs(self._vat_culture_pulse - 0.5) * 2.0  # 0..1..0
        ready = 0.35 <= self._vat_temp <= 0.70
        ccolor = (100, 220, 100) if ready else (150, 150, 150)
        cr = cx + 60
        pygame.draw.circle(self.screen, _CELL_BG, (cr, cy), 40)
        if ready:
            pygame.draw.circle(self.screen, ccolor, (cr, cy), int(28 + 8 * pulse_v))
        else:
            pygame.draw.circle(self.screen, ccolor, (cr, cy), 20)
        pygame.draw.circle(self.screen, _ACCENT, (cr, cy), 40, 2)
        cl_txt = "READY" if ready else "WAIT"
        cl = self.small.render(cl_txt, True, ccolor)
        self.screen.blit(cl, (cr - cl.get_width() // 2, cy - cl.get_height() // 2))

        if not self._vat_culture_added:
            ka = self.small.render("Press SPACE to add culture", True, _HINT_C)
            self.screen.blit(ka, (SCREEN_W // 2 - ka.get_width() // 2, cy + 60))
        else:
            ka = self.small.render("Culture added! Curdling...", True, (100, 220, 100))
            self.screen.blit(ka, (SCREEN_W // 2 - ka.get_width() // 2, cy + 60))
            bar_w = 200
            prog = max(0.0, 1.0 - self._vat_finish_timer / 3.0)
            pygame.draw.rect(self.screen, _CELL_BG, (SCREEN_W // 2 - bar_w // 2, cy + 85, bar_w, 16))
            pygame.draw.rect(self.screen, _ACCENT, (SCREEN_W // 2 - bar_w // 2, cy + 85, int(bar_w * prog), 16))

        # Quality preview
        ts_label = self.small.render(f"Temp score: {int(self._vat_temp_score * 100)}%", True, _DIM_C)
        self.screen.blit(ts_label, (cx - 200, cy + gauge_h // 2 + 20))

        if self._vat_game_done:
            self._finish_vat(player)

    def _draw_vat_result(self, player):
        if not self._vat_result_cheese:
            return
        c = self._vat_result_cheese
        cx = SCREEN_W // 2
        msg = self.font.render("Curd Ready!", True, _TITLE_C)
        self.screen.blit(msg, (cx - msg.get_width() // 2, SCREEN_H // 2 - 60))
        q_pct = int(c.culture_quality * 100)
        q_color = (100, 220, 100) if c.culture_quality >= 0.7 else (220, 200, 80) if c.culture_quality >= 0.45 else (200, 100, 80)
        ql = self.font.render(f"Culture Quality: {q_pct}%", True, q_color)
        self.screen.blit(ql, (cx - ql.get_width() // 2, SCREEN_H // 2 - 20))
        bl = self.small.render(f"{c.animal_type.capitalize()} milk from {BIOME_DISPLAY_NAMES.get(c.origin_biome, c.origin_biome)}", True, _LABEL_C)
        self.screen.blit(bl, (cx - bl.get_width() // 2, SCREEN_H // 2 + 18))
        ok = self.small.render("Click anywhere to continue", True, _HINT_C)
        self.screen.blit(ok, (cx - ok.get_width() // 2, SCREEN_H // 2 + 50))

    def _finish_vat(self, player):
        c = self._vat_current_cheese
        if c is None:
            return
        culture_score = self._vat_culture_score if self._vat_culture_added else 0.2
        pen = min(2, int(self._vat_penalties))
        bonus = getattr(player, "curd_quality_bonus", 0.0)
        apply_curd_result(c, min(1.0, self._vat_temp_score + bonus), culture_score, pen)
        # consume milk item
        milk_key = {"cow": "milk", "goat": "goat_milk", "sheep": "sheep_milk"}.get(c.animal_type, "milk")
        if player.inventory.get(milk_key, 0) > 0:
            player.inventory[milk_key] -= 1
            if player.inventory[milk_key] <= 0:
                del player.inventory[milk_key]
        self._vat_result_cheese = c
        self._vat_phase = "result"

    def handle_dairy_vat_click(self, pos, player):
        if self._vat_phase == "select_milk":
            for uid, (rect, cheese, item_id) in self._vat_select_rects.items():
                if rect.collidepoint(pos):
                    self._vat_current_cheese = cheese
                    self._vat_phase = "mini_game"
                    self._vat_temp = 0.0
                    self._vat_temp_score = 0.0
                    self._vat_culture_added = False
                    self._vat_culture_score = 0.0
                    self._vat_culture_pulse = 0.0
                    self._vat_penalties = 0.0
                    self._vat_finish_timer = 3.0
                    self._vat_game_done = False
                    self._vat_result_cheese = None
                    return
        elif self._vat_phase == "result":
            self._vat_phase = "select_milk"
            self._vat_result_cheese = None

    def handle_dairy_vat_keydown(self, key, player):
        if self._vat_phase == "mini_game" and key == pygame.K_SPACE:
            if not self._vat_culture_added:
                ready = 0.35 <= self._vat_temp <= 0.70
                self._vat_culture_score = 0.9 if ready else 0.3
                self._vat_culture_added = True

    # ─────────────────────────────────────────────────────────────────────────
    # CHEESE PRESS
    # ─────────────────────────────────────────────────────────────────────────

    def _draw_cheese_press(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("CHEESE PRESS", True, _TITLE_C)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, _HINT_C)
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        if self._cp_phase == "select_curd":
            self._cp_select_rects.clear()
            curds = [(i, c) for i, c in enumerate(player.cheese_wheels) if c.state == "curd"]
            if not curds:
                msg = self.font.render("No curds! Process milk in the Dairy Vat first.", True, _LABEL_C)
                self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2))
                return
            sub = self.small.render("Select a curd to press:", True, _LABEL_C)
            self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 32))
            CELL_W, CELL_H, GAP, COLS = 220, 60, 10, 4
            gx0 = (SCREEN_W - (COLS * CELL_W + (COLS - 1) * GAP)) // 2
            for li, (bi, curd) in enumerate(curds[:16]):
                col_i, row_i = li % COLS, li // COLS
                rx = gx0 + col_i * (CELL_W + GAP)
                ry = 55 + row_i * (CELL_H + GAP)
                rect = pygame.Rect(rx, ry, CELL_W, CELL_H)
                self._cp_select_rects[bi] = rect
                pygame.draw.rect(self.screen, _CELL_BG, rect)
                pygame.draw.rect(self.screen, _ACCENT, rect, 2)
                nm = BIOME_DISPLAY_NAMES.get(curd.origin_biome, curd.origin_biome)
                ns = self.small.render(f"{curd.animal_type.capitalize()} — {nm}", True, _TITLE_C)
                self.screen.blit(ns, (rx + 6, ry + 8))
                qs = self.small.render(f"Culture: {int(curd.culture_quality * 100)}%", True, _HINT_C)
                self.screen.blit(qs, (rx + 6, ry + 28))

        elif self._cp_phase == "select_type":
            self._draw_press_type_select(player)

        elif self._cp_phase == "mini_game":
            self._draw_press_minigame(player, dt)

        elif self._cp_phase == "result":
            self._draw_press_result(player)

    def _draw_press_type_select(self, player):
        self._cp_type_rects.clear()
        sub = self.small.render("Choose the cheese type to make:", True, _LABEL_C)
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 32))
        types = list(CHEESE_TYPE_DESCS.items())
        # Hide blue unless researched
        if not getattr(player, "blue_cheese_unlocked", False):
            types = [(k, v) for k, v in types if k != "blue"]
        BTN_W, BTN_H, BTN_GAP = 200, 90, 12
        cols = 3
        rows = (len(types) + cols - 1) // cols
        total_w = cols * BTN_W + (cols - 1) * BTN_GAP
        gx0 = (SCREEN_W - total_w) // 2
        for pi, (ct_key, ct_desc) in enumerate(types):
            col_i, row_i = pi % cols, pi // cols
            px = gx0 + col_i * (BTN_W + BTN_GAP)
            py = 60 + row_i * (BTN_H + BTN_GAP)
            prect = pygame.Rect(px, py, BTN_W, BTN_H)
            self._cp_type_rects[ct_key] = prect
            age_cycles = CHEESE_TYPE_AGING[ct_key]
            col = CHEESE_TYPE_COLORS.get(ct_key, _CELL_BG)
            darker = tuple(max(0, v - 40) for v in col)
            pygame.draw.rect(self.screen, darker, prect)
            pygame.draw.rect(self.screen, col, prect, 3)
            lbl = self.font.render(ct_key.replace("_", " ").title(), True, _TITLE_C)
            self.screen.blit(lbl, (px + BTN_W // 2 - lbl.get_width() // 2, py + 10))
            desc_short = ct_desc.split("—")[-1].strip()
            dl = self.small.render(desc_short, True, _LABEL_C)
            self.screen.blit(dl, (px + BTN_W // 2 - dl.get_width() // 2, py + 38))
            ag = self.small.render(f"Aging: {age_cycles} day{'s' if age_cycles != 1 else ''}", True, _HINT_C)
            self.screen.blit(ag, (px + BTN_W // 2 - ag.get_width() // 2, py + 62))
            opt = CHEESE_PRESS_INGREDIENTS.get(ct_key)
            if opt:
                opt_lbl = self.small.render(f"+ {opt['label']}", True, (140, 200, 140))
                self.screen.blit(opt_lbl, (px + BTN_W // 2 - opt_lbl.get_width() // 2, py + 76))

    def _draw_press_minigame(self, player, dt):
        if not self._cp_game_done:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]:
                self._cp_pressure = min(1.0, self._cp_pressure + 2.5 * dt)
            else:
                self._cp_pressure = max(0.0, self._cp_pressure - 1.0 * dt)
            # Score: time in ideal pressure band 0.45–0.75
            if 0.45 <= self._cp_pressure <= 0.75:
                self._cp_score = min(1.0, self._cp_score + 0.7 * dt)
            self._cp_timer -= dt
            if self._cp_timer <= 0:
                self._cp_game_done = True

        cx = SCREEN_W // 2
        cy = SCREEN_H // 2

        # Pressure bar
        bar_w = 320
        bar_x = cx - bar_w // 2
        bar_y = cy - 20
        pygame.draw.rect(self.screen, _CELL_BG, (bar_x, bar_y, bar_w, 40))
        pc = CHEESE_TYPE_COLORS.get(self._cp_type, _ACCENT)
        pygame.draw.rect(self.screen, pc, (bar_x, bar_y, int(bar_w * self._cp_pressure), 40))
        pygame.draw.rect(self.screen, _ACCENT, (bar_x, bar_y, bar_w, 40), 2)
        # Ideal zone markers
        ideal_x0 = bar_x + int(bar_w * 0.45)
        ideal_x1 = bar_x + int(bar_w * 0.75)
        pygame.draw.line(self.screen, (100, 220, 100), (ideal_x0, bar_y - 6), (ideal_x0, bar_y + 46))
        pygame.draw.line(self.screen, (100, 220, 100), (ideal_x1, bar_y - 6), (ideal_x1, bar_y + 46))

        ct_lbl = self.font.render(self._cp_type.replace("_", " ").title(), True, _TITLE_C)
        self.screen.blit(ct_lbl, (cx - ct_lbl.get_width() // 2, cy - 70))
        pl = self.small.render("Hold W/↑/SPACE to increase pressure", True, _HINT_C)
        self.screen.blit(pl, (cx - pl.get_width() // 2, cy + 35))
        sc = self.small.render(f"Score: {int(self._cp_score * 100)}%", True, _LABEL_C)
        self.screen.blit(sc, (cx - sc.get_width() // 2, cy + 55))

        # Timer bar
        time_frac = max(0.0, self._cp_timer / 8.0)
        pygame.draw.rect(self.screen, _CELL_BG, (bar_x, cy + 75, bar_w, 10))
        pygame.draw.rect(self.screen, _DIM_C, (bar_x, cy + 75, int(bar_w * time_frac), 10))

        if self._cp_game_done:
            self._finish_press(player)

    def _draw_press_result(self, player):
        if not self._cp_result_cheese:
            return
        c = self._cp_result_cheese
        cx = SCREEN_W // 2
        msg = self.font.render("Wheel Pressed!", True, _TITLE_C)
        self.screen.blit(msg, (cx - msg.get_width() // 2, SCREEN_H // 2 - 60))
        ct_lbl = self.font.render(c.cheese_type.replace("_", " ").title(), True,
                                  CHEESE_TYPE_COLORS.get(c.cheese_type, _ACCENT))
        self.screen.blit(ct_lbl, (cx - ct_lbl.get_width() // 2, SCREEN_H // 2 - 20))
        aging_cycles = CHEESE_TYPE_AGING.get(c.cheese_type, 0)
        if aging_cycles == 0:
            msg2 = self.small.render("Fresh — no aging needed. Collect from Aging Cave.", True, _LABEL_C)
        else:
            msg2 = self.small.render(f"Needs {aging_cycles} aging day(s) in the Aging Cave.", True, _LABEL_C)
        self.screen.blit(msg2, (cx - msg2.get_width() // 2, SCREEN_H // 2 + 18))
        ok = self.small.render("Click anywhere to continue", True, _HINT_C)
        self.screen.blit(ok, (cx - ok.get_width() // 2, SCREEN_H // 2 + 50))

    def _finish_press(self, player):
        c = self._cp_current_curd
        if c is None:
            return
        # Optional ingredient bonus
        press_score = self._cp_score
        opt = CHEESE_PRESS_INGREDIENTS.get(self._cp_type)
        if opt:
            for item_id in opt["items"]:
                if player.inventory.get(item_id, 0) > 0:
                    player.inventory[item_id] -= 1
                    if player.inventory[item_id] <= 0:
                        del player.inventory[item_id]
                    press_score = min(1.0, press_score + opt["bonus"])
                    break
        apply_press_result(c, self._cp_type, press_score)
        self._cp_result_cheese = c
        self._cp_phase = "result"

    def handle_cheese_press_click(self, pos, player):
        if self._cp_phase == "select_curd":
            for bi, rect in self._cp_select_rects.items():
                if rect.collidepoint(pos):
                    self._cp_current_curd = player.cheese_wheels[bi]
                    self._cp_phase = "select_type"
                    return
        elif self._cp_phase == "select_type":
            for ct_key, rect in self._cp_type_rects.items():
                if rect.collidepoint(pos):
                    self._cp_type = ct_key
                    if ct_key == "fresh":
                        # Fresh skips pressing — go straight to mini-game briefly
                        self._finish_press_as_fresh(player)
                    else:
                        self._cp_phase = "mini_game"
                        self._cp_pressure = 0.0
                        self._cp_score = 0.0
                        self._cp_timer = 8.0
                        self._cp_game_done = False
                    return
        elif self._cp_phase == "result":
            self._cp_phase = "select_curd"
            self._cp_result_cheese = None

    def _finish_press_as_fresh(self, player):
        c = self._cp_current_curd
        if c is None:
            return
        apply_press_result(c, "fresh", 0.8)  # fresh always base quality
        self._cp_result_cheese = c
        self._cp_phase = "result"

    # ─────────────────────────────────────────────────────────────────────────
    # AGING CAVE
    # ─────────────────────────────────────────────────────────────────────────

    def _draw_aging_cave(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("AGING CAVE", True, _TITLE_C)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, _HINT_C)
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        if self._cave_phase == "select_wheel":
            self._cave_select_rects.clear()
            wheels = [(i, c) for i, c in enumerate(player.cheese_wheels) if c.state == "pressed"]
            if not wheels:
                msg = self.font.render("No pressed wheels! Use the Cheese Press first.", True, _LABEL_C)
                self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2))
                return
            sub = self.small.render("Select a wheel to age:", True, _LABEL_C)
            self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 32))
            CELL_W, CELL_H, GAP, COLS = 230, 65, 10, 4
            gx0 = (SCREEN_W - (COLS * CELL_W + (COLS - 1) * GAP)) // 2
            for li, (bi, wheel) in enumerate(wheels[:16]):
                col_i, row_i = li % COLS, li // COLS
                rx = gx0 + col_i * (CELL_W + GAP)
                ry = 55 + row_i * (CELL_H + GAP)
                rect = pygame.Rect(rx, ry, CELL_W, CELL_H)
                self._cave_select_rects[bi] = rect
                col = CHEESE_TYPE_COLORS.get(wheel.cheese_type, _CELL_BG)
                darker = tuple(max(0, v - 50) for v in col)
                pygame.draw.rect(self.screen, darker, rect)
                pygame.draw.rect(self.screen, col, rect, 2)
                ct_nm = wheel.cheese_type.replace("_", " ").title()
                ns = self.small.render(ct_nm, True, _TITLE_C)
                self.screen.blit(ns, (rx + 6, ry + 8))
                biome_nm = BIOME_DISPLAY_NAMES.get(wheel.origin_biome, wheel.origin_biome)
                bn = self.small.render(f"{wheel.animal_type.capitalize()} — {biome_nm}", True, _HINT_C)
                self.screen.blit(bn, (rx + 6, ry + 28))
                req = CHEESE_TYPE_AGING.get(wheel.cheese_type, 0)
                ag = self.small.render(f"Needs {req} day(s)", True, _DIM_C)
                self.screen.blit(ag, (rx + 6, ry + 46))

        elif self._cave_phase == "select_duration":
            self._draw_cave_duration_select(player)

        elif self._cave_phase == "aging":
            self._draw_cave_aging(player, dt)

        elif self._cave_phase == "result":
            self._draw_cave_result(player)

    def _draw_cave_duration_select(self, player):
        self._cave_duration_rects.clear()
        w = self._cave_current_wheel
        required = CHEESE_TYPE_AGING.get(w.cheese_type, 1)
        sub = self.small.render("Choose aging duration (more days = sharper, nuttier):", True, _LABEL_C)
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 32))
        max_cycles = 6 if getattr(player, "blue_cheese_unlocked", False) else 5
        durations = list(range(required, max_cycles + 1))
        BTN_W, BTN_H, BTN_GAP = 140, 70, 12
        total_w = len(durations) * BTN_W + (len(durations) - 1) * BTN_GAP
        gx0 = (SCREEN_W - total_w) // 2
        for pi, cycles in enumerate(durations):
            px = gx0 + pi * (BTN_W + BTN_GAP)
            py = SCREEN_H // 2 - BTN_H // 2
            prect = pygame.Rect(px, py, BTN_W, BTN_H)
            self._cave_duration_rects[cycles] = prect
            pygame.draw.rect(self.screen, _CELL_BG, prect)
            pygame.draw.rect(self.screen, _ACCENT, prect, 2)
            lbl = self.font.render(f"{cycles}", True, _TITLE_C)
            self.screen.blit(lbl, (px + BTN_W // 2 - lbl.get_width() // 2, py + 8))
            cl = self.small.render("day" if cycles == 1 else "days", True, _LABEL_C)
            self.screen.blit(cl, (px + BTN_W // 2 - cl.get_width() // 2, py + 34))
            tier = "Superior" if cycles >= 5 else "Fine" if cycles >= 3 else "Base"
            tl = self.small.render(tier, True, _HINT_C)
            self.screen.blit(tl, (px + BTN_W // 2 - tl.get_width() // 2, py + 50))

    def _draw_cave_aging(self, player, dt):
        w = self._cave_current_wheel
        cx = SCREEN_W // 2

        # Advance aging bar
        if not self._cave_game_done:
            total_secs = self._cave_cycles * _SECS_PER_AGING_DAY
            self._cave_age_progress = min(1.0, self._cave_age_progress + dt / total_secs)
            # Periodic care prompt
            self._cave_care_prompt_timer -= dt
            if self._cave_care_prompt_timer <= 0 and not self._cave_care_active:
                self._cave_care_active = True
                self._cave_care_window = 3.0
            if self._cave_care_active:
                self._cave_care_window -= dt
                if self._cave_care_window <= 0:
                    self._cave_care_active = False
                    self._cave_care_prompt_timer = max(4.0, self._cave_cycles * 3.0)
            if self._cave_age_progress >= 1.0:
                self._cave_game_done = True

        # Draw aging bar
        bar_w = 400
        bar_x = cx - bar_w // 2
        bar_y = SCREEN_H // 2 - 10
        pygame.draw.rect(self.screen, _CELL_BG, (bar_x, bar_y, bar_w, 30))
        col = CHEESE_TYPE_COLORS.get(w.cheese_type, _ACCENT)
        pygame.draw.rect(self.screen, col, (bar_x, bar_y, int(bar_w * self._cave_age_progress), 30))
        pygame.draw.rect(self.screen, _ACCENT, (bar_x, bar_y, bar_w, 30), 2)

        ct = self.font.render(w.cheese_type.replace("_", " ").title(), True, _TITLE_C)
        self.screen.blit(ct, (cx - ct.get_width() // 2, SCREEN_H // 2 - 55))
        days_elapsed = int(self._cave_age_progress * self._cave_cycles)
        day_lbl = "day" if self._cave_cycles == 1 else "days"
        pl = self.small.render(f"Aging: Day {days_elapsed} / {self._cave_cycles} {day_lbl}", True, _LABEL_C)
        self.screen.blit(pl, (cx - pl.get_width() // 2, SCREEN_H // 2 + 30))

        bonus_pct = int(self._cave_care_bonus * 100)
        bl = self.small.render(f"Care bonus: +{bonus_pct}%", True, _HINT_C)
        self.screen.blit(bl, (cx - bl.get_width() // 2, SCREEN_H // 2 + 50))

        # Care prompt
        if self._cave_care_active:
            flash = int(self._cave_care_window * 4) % 2 == 0
            c_color = (100, 220, 100) if flash else (60, 160, 60)
            care_msg = self.font.render("PRESS C — Turn the wheel!", True, c_color)
            self.screen.blit(care_msg, (cx - care_msg.get_width() // 2, SCREEN_H // 2 - 90))

        if self._cave_game_done:
            self._finish_cave(player)

    def _draw_cave_result(self, player):
        if not self._cave_result_item:
            return
        cx = SCREEN_W // 2
        msg = self.font.render("Cheese Aged!", True, _TITLE_C)
        self.screen.blit(msg, (cx - msg.get_width() // 2, SCREEN_H // 2 - 80))
        from items import ITEMS
        item_name = ITEMS.get(self._cave_result_item, {}).get("name", self._cave_result_item)
        nl = self.font.render(item_name, True, CHEESE_TYPE_COLORS.get(
            self._cave_result_item.split("_cheese")[0].replace("cheese_", "") if "cheese_" in self._cave_result_item else "pressed",
            _ACCENT))
        self.screen.blit(nl, (cx - nl.get_width() // 2, SCREEN_H // 2 - 35))
        w = self._cave_result_wheel
        if w and w.flavor_notes:
            notes_str = ", ".join(w.flavor_notes[:4])
            fn = self.small.render(f"Notes: {notes_str}", True, _LABEL_C)
            self.screen.blit(fn, (cx - fn.get_width() // 2, SCREEN_H // 2 + 10))
        ok = self.small.render("Click anywhere to continue", True, _HINT_C)
        self.screen.blit(ok, (cx - ok.get_width() // 2, SCREEN_H // 2 + 50))

    def _finish_cave(self, player):
        w = self._cave_current_wheel
        if w is None:
            return
        apply_aging_result(w, self._cave_cycles, self._cave_care_bonus)
        out_id = get_cheese_output_id(w.cheese_type, w.culture_quality, w.press_quality, w.age_quality)
        player._add_item(out_id)
        player.discovered_cheese.add(f"{w.origin_biome}_{w.cheese_type}")
        self._cave_result_item = out_id
        self._cave_result_wheel = w
        self._cave_phase = "result"

    def handle_aging_cave_click(self, pos, player):
        if self._cave_phase == "select_wheel":
            for bi, rect in self._cave_select_rects.items():
                if rect.collidepoint(pos):
                    self._cave_current_wheel = player.cheese_wheels[bi]
                    self._cave_phase = "select_duration"
                    return
        elif self._cave_phase == "select_duration":
            for cycles, rect in self._cave_duration_rects.items():
                if rect.collidepoint(pos):
                    self._cave_cycles = cycles
                    self._cave_phase = "aging"
                    self._cave_age_progress = 0.0
                    self._cave_care_bonus = 0.0
                    self._cave_care_prompt_timer = max(3.0, cycles * 2.5)
                    self._cave_care_active = False
                    self._cave_care_window = 0.0
                    self._cave_game_done = False
                    self._cave_result_item = None
                    self._cave_result_wheel = None
                    return
        elif self._cave_phase == "result":
            self._cave_phase = "select_wheel"
            self._cave_result_item = None
            self._cave_result_wheel = None

    def handle_aging_cave_keydown(self, key, player):
        if self._cave_phase == "aging" and key == pygame.K_c:
            if self._cave_care_active:
                self._cave_care_bonus = min(1.0, self._cave_care_bonus + 0.15)
                self._cave_care_active = False
                self._cave_care_prompt_timer = max(4.0, self._cave_cycles * 2.5)
