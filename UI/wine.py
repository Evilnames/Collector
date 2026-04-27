import pygame
from constants import SCREEN_W, SCREEN_H
from wine import (
    apply_crush_style, apply_press_result, apply_yeast, apply_ferment_result,
    apply_aging, make_blend, generate_flavor_notes,
    get_bottle_output_id, get_bottle_duration_multiplier, get_bottle_quality_bonus,
    CRUSH_STYLES, YEASTS, VESSELS, AGE_DURATIONS,
    SERVING_METHODS, SERVING_TEMPS,
    WINE_STYLE_DESCS, WINE_STYLE_COLORS, BUFF_DESCS,
    BIOME_DISPLAY_NAMES, VARIETY_DISPLAY_NAMES,
)

_SECS_PER_AGING_DAY = 5.0


def _age_duration_secs(key):
    return AGE_DURATIONS.get(key, {}).get("days", 8) * _SECS_PER_AGING_DAY


class WineMixin:
    """Mirror of CoffeeMixin for the wine-making track.

    Three stations:
      1. Grape Press (crush mini-game: select grape → style → press → result)
      2. Fermentation Tank (deep mini-game: temp + nutrient + punchdowns)
      3. Wine Cellar (three tabs: blend / age / bottle)
    """

    # ==================================================================
    # GRAPE PRESS
    # ==================================================================

    def _draw_grape_press(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("GRAPE PRESS", True, (200, 120, 140))
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, (100, 70, 80))
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        if self._press_phase == "select_grape":
            self._press_select_rects.clear()
            raw = [(i, g) for i, g in enumerate(player.wine_grapes) if g.state == "raw"]
            if not raw:
                msg = self.font.render("No raw grapes! Harvest mature grapevines.", True, (160, 110, 130))
                self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2))
                return
            sub = self.small.render("Select a grape cluster to crush:", True, (190, 130, 150))
            self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 32))
            CELL_W, CELL_H, GAP, COLS = 220, 56, 8, 5
            gx0 = (SCREEN_W - (COLS * CELL_W + (COLS - 1) * GAP)) // 2
            for li, (bi, g) in enumerate(raw[:20]):
                col_i = li % COLS
                row_i = li // COLS
                rx = gx0 + col_i * (CELL_W + GAP)
                ry = 55 + row_i * (CELL_H + GAP)
                rect = pygame.Rect(rx, ry, CELL_W, CELL_H)
                self._press_select_rects[bi] = rect
                pygame.draw.rect(self.screen, (40, 18, 30), rect)
                pygame.draw.rect(self.screen, (160, 90, 120), rect, 2)
                nm = BIOME_DISPLAY_NAMES.get(g.origin_biome, g.origin_biome)
                vn = VARIETY_DISPLAY_NAMES.get(g.variety, g.variety)
                ns = self.small.render(f"{nm}  {vn}", True, (230, 170, 190))
                self.screen.blit(ns, (rx + 6, ry + 8))
                hint2 = self.small.render("Click to crush", True, (130, 90, 110))
                self.screen.blit(hint2, (rx + 6, ry + 26))

        elif self._press_phase == "select_style":
            self._press_style_rects.clear()
            sub = self.small.render("Choose a crush style:", True, (190, 130, 150))
            self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 32))
            BTN_W, BTN_H, BTN_GAP = 260, 80, 14
            total_w = len(CRUSH_STYLES) * BTN_W + (len(CRUSH_STYLES) - 1) * BTN_GAP
            gx0 = (SCREEN_W - total_w) // 2
            for pi, (skey, sdata) in enumerate(CRUSH_STYLES.items()):
                px = gx0 + pi * (BTN_W + BTN_GAP)
                py = SCREEN_H // 2 - BTN_H // 2
                prect = pygame.Rect(px, py, BTN_W, BTN_H)
                self._press_style_rects[skey] = prect
                pygame.draw.rect(self.screen, (35, 18, 28), prect)
                pygame.draw.rect(self.screen, (175, 100, 130), prect, 2)
                lbl = self.font.render(sdata["label"], True, (235, 175, 195))
                self.screen.blit(lbl, (px + BTN_W // 2 - lbl.get_width() // 2, py + 8))
                for di, dl in enumerate(sdata["desc"].split(". ")[:2]):
                    ds = self.small.render(dl, True, (175, 130, 150))
                    self.screen.blit(ds, (px + 8, py + 36 + di * 14))

        elif self._press_phase == "pressing":
            self._press_time += dt
            # Physics: hold raises pressure, release drops it.
            if self._press_held:
                self._press_pressure = min(1.0, self._press_pressure + 0.8 * dt)
            else:
                self._press_pressure = max(0.0, self._press_pressure - 0.45 * dt)
            p = self._press_pressure
            if 0.30 <= p <= 0.65:
                self._press_time_green += dt
            elif 0.65 < p <= 0.85:
                self._press_time_yellow += dt
            elif p > 0.85:
                self._press_over_penalty = min(5, self._press_over_penalty + int(dt * 2))

            if not self._press_freerun_hit and self._press_time >= 10.0:
                self._press_freerun_hit = True
                self._press_event_flash = ("FREE-RUN COMPLETE", (240, 210, 120), 2.0)
            if not self._press_wine_hit and self._press_time >= 22.0:
                self._press_wine_hit = True
                self._press_event_flash = ("PRESS-WINE STAGE", (240, 120, 120), 2.0)
            if self._press_event_flash:
                txt, col, timer = self._press_event_flash
                timer -= dt
                if timer <= 0:
                    self._press_event_flash = None
                else:
                    self._press_event_flash = (txt, col, timer)

            # Vertical pressure gauge
            BAR_X, BAR_Y, BAR_W, BAR_H = 80, 60, 36, SCREEN_H - 140
            pygame.draw.rect(self.screen, (22, 12, 18), (BAR_X, BAR_Y, BAR_W, BAR_H))
            pygame.draw.rect(self.screen, (75, 40, 55), (BAR_X, BAR_Y, BAR_W, BAR_H), 2)

            def _zy(v):
                return BAR_Y + BAR_H - int(BAR_H * v)

            # Green (good), yellow (risky), red (bad)
            pygame.draw.rect(self.screen, (35, 85, 45),
                             (BAR_X, _zy(0.65), BAR_W, _zy(0.30) - _zy(0.65)))
            pygame.draw.rect(self.screen, (95, 85, 35),
                             (BAR_X, _zy(0.85), BAR_W, _zy(0.65) - _zy(0.85)))
            pygame.draw.rect(self.screen, (110, 30, 30),
                             (BAR_X, _zy(1.00), BAR_W, _zy(0.85) - _zy(1.00)))
            my = _zy(p)
            pygame.draw.rect(self.screen, (220, 150, 170), (BAR_X - 6, my - 4, BAR_W + 12, 8))
            lbl = self.small.render(f"{p:.0%}", True, (220, 160, 180))
            self.screen.blit(lbl, (BAR_X + BAR_W + 6, my - 6))
            for zv, zn in [(0.30, "Low"), (0.65, "Good"), (0.85, "Risky"), (1.00, "Over")]:
                yl = _zy(zv)
                s = self.small.render(zn, True, (170, 110, 130))
                self.screen.blit(s, (BAR_X - s.get_width() - 4, yl - 6))
                pygame.draw.line(self.screen, (70, 40, 55), (BAR_X, yl), (BAR_X + BAR_W, yl), 1)

            # Time bar
            TIME_X, TIME_Y = 140, SCREEN_H - 56
            TIME_W = SCREEN_W - 270
            total = self._press_total_time
            pygame.draw.rect(self.screen, (22, 12, 18), (TIME_X, TIME_Y, TIME_W, 18))
            pygame.draw.rect(self.screen, (75, 40, 55), (TIME_X, TIME_Y, TIME_W, 18), 2)
            prog = min(1.0, self._press_time / total)
            pygame.draw.rect(self.screen, (180, 110, 140),
                             (TIME_X, TIME_Y, int(TIME_W * prog), 18))
            for tm, tl in [(10, "free-run"), (22, "press-wine")]:
                tx = TIME_X + int(TIME_W * tm / total)
                pygame.draw.line(self.screen, (230, 180, 200), (tx, TIME_Y - 4), (tx, TIME_Y + 22), 2)
                ts = self.small.render(tl, True, (210, 160, 180))
                self.screen.blit(ts, (tx - ts.get_width() // 2, TIME_Y - 18))
            ts = self.small.render(f"{self._press_time:.1f}s / {total:.0f}s", True, (190, 140, 160))
            self.screen.blit(ts, (TIME_X + TIME_W // 2 - ts.get_width() // 2, TIME_Y + 22))

            if self._press_event_flash:
                txt, col, _ = self._press_event_flash
                ef = self.font.render(txt, True, col)
                self.screen.blit(ef, (SCREEN_W // 2 - ef.get_width() // 2, SCREEN_H // 2 - 20))

            inst = self.small.render("Hold SPACE / click PRESS to apply pressure.  Press ENTER / click STOP to finish.", True, (170, 120, 140))
            self.screen.blit(inst, (SCREEN_W // 2 - inst.get_width() // 2, TIME_Y - 40))

            stop_rect = pygame.Rect(SCREEN_W - 150, SCREEN_H - 56, 130, 32)
            pygame.draw.rect(self.screen, (80, 30, 40), stop_rect)
            pygame.draw.rect(self.screen, (200, 100, 130), stop_rect, 2)
            sl = self.font.render("STOP", True, (240, 170, 190))
            self.screen.blit(sl, (stop_rect.centerx - sl.get_width() // 2, stop_rect.centery - sl.get_height() // 2))
            self._press_stop_btn = stop_rect

            press_rect = pygame.Rect(SCREEN_W - 150, SCREEN_H - 96, 130, 32)
            pcol = (120, 50, 75) if not self._press_held else (180, 80, 110)
            pygame.draw.rect(self.screen, pcol, press_rect)
            pygame.draw.rect(self.screen, (220, 120, 160), press_rect, 2)
            pl = self.font.render("PRESS", True, (255, 200, 220))
            self.screen.blit(pl, (press_rect.centerx - pl.get_width() // 2, press_rect.centery - pl.get_height() // 2))
            self._press_btn = press_rect

        elif self._press_phase == "result":
            g = player.wine_grapes[self._press_grape_idx] if self._press_grape_idx < len(player.wine_grapes) else None
            if not g:
                self._press_phase = "select_grape"
                return
            cx2, cy2 = SCREEN_W // 2, 80
            pygame.draw.circle(self.screen, (120, 50, 100), (cx2, cy2 + 40), 36)
            pygame.draw.circle(self.screen, (180, 100, 150), (cx2, cy2 + 40), 36, 2)

            iy2 = cy2 + 100
            def rline(t, col=(210, 160, 180)):
                nonlocal iy2
                s = self.font.render(t, True, col)
                self.screen.blit(s, (cx2 - s.get_width() // 2, iy2))
                iy2 += 26

            rline(f"{BIOME_DISPLAY_NAMES.get(g.origin_biome, g.origin_biome)}  {VARIETY_DISPLAY_NAMES.get(g.variety, g.variety)}", (240, 180, 200))
            rline(f"Crush: {CRUSH_STYLES.get(g.crush_style, {}).get('label', '-')}", (190, 150, 170))
            rline(f"Must ready for fermentation", (170, 200, 160))
            stars = "★" * round(g.press_quality * 5) + "☆" * (5 - round(g.press_quality * 5))
            rline(stars, (230, 190, 90))

            done_rect = pygame.Rect(cx2 - 70, iy2 + 20, 140, 34)
            pygame.draw.rect(self.screen, (50, 25, 35), done_rect)
            pygame.draw.rect(self.screen, (190, 130, 160), done_rect, 2)
            dl = self.font.render("DONE", True, (230, 180, 200))
            self.screen.blit(dl, (done_rect.centerx - dl.get_width() // 2, done_rect.centery - dl.get_height() // 2))
            self._press_result_done_btn = done_rect

    def _handle_grape_press_click(self, pos, player):
        if self._press_phase == "select_grape":
            for bi, rect in self._press_select_rects.items():
                if rect.collidepoint(pos):
                    g = player.wine_grapes[bi]
                    if g.state == "raw":
                        self._press_grape_idx = bi
                        self._press_phase = "select_style"
                    return
        elif self._press_phase == "select_style":
            for skey, srect in self._press_style_rects.items():
                if srect.collidepoint(pos):
                    bi = self._press_grape_idx
                    if bi is not None and bi < len(player.wine_grapes):
                        g = player.wine_grapes[bi]
                        apply_crush_style(g, skey)
                        self._press_time = 0.0
                        self._press_pressure = 0.0
                        self._press_time_green = 0.0
                        self._press_time_yellow = 0.0
                        self._press_over_penalty = 0
                        self._press_freerun_hit = False
                        self._press_wine_hit = False
                        self._press_event_flash = None
                        self._press_held = False
                        self._press_phase = "pressing"
                    return
        elif self._press_phase == "pressing":
            if self._press_stop_btn and self._press_stop_btn.collidepoint(pos):
                self._finish_press(player)
                return
            if self._press_btn and self._press_btn.collidepoint(pos):
                self._press_held = True
                return
        elif self._press_phase == "result":
            if self._press_result_done_btn and self._press_result_done_btn.collidepoint(pos):
                self._press_phase = "select_grape"
                self._press_grape_idx = None
                return

    def handle_press_keys(self, keys):
        from blocks import GRAPE_PRESS_BLOCK
        if self.refinery_block_id != GRAPE_PRESS_BLOCK:
            return
        if self._press_phase == "pressing":
            self._press_held = bool(keys[pygame.K_SPACE])

    def handle_press_keydown(self, key, player):
        from blocks import GRAPE_PRESS_BLOCK
        if self.refinery_block_id != GRAPE_PRESS_BLOCK:
            return
        if self._press_phase == "pressing":
            if key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self._finish_press(player)

    def _finish_press(self, player):
        bi = self._press_grape_idx
        if bi is None or bi >= len(player.wine_grapes):
            self._press_phase = "select_grape"
            return
        g = player.wine_grapes[bi]
        apply_press_result(g, self._press_pressure,
                           self._press_time_green, self._press_time_yellow,
                           self._press_time, self._press_over_penalty)
        self._press_phase = "result"

    # ==================================================================
    # FERMENTATION TANK
    # ==================================================================

    def _draw_fermenter(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("FERMENTATION TANK", True, (190, 140, 80))
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, (100, 80, 50))
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        if self._ferm_phase == "select_must":
            self._ferm_select_rects.clear()
            musts = [(i, g) for i, g in enumerate(player.wine_grapes) if g.state == "crushed"]
            if not musts:
                msg = self.font.render("No crushed must! Press grapes at the Grape Press first.", True, (160, 120, 80))
                self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2))
                return
            sub = self.small.render("Select a must to ferment:", True, (190, 150, 80))
            self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 32))
            CELL_W, CELL_H, GAP, COLS = 220, 56, 8, 5
            gx0 = (SCREEN_W - (COLS * CELL_W + (COLS - 1) * GAP)) // 2
            for li, (bi, g) in enumerate(musts[:20]):
                col_i = li % COLS
                row_i = li // COLS
                rx = gx0 + col_i * (CELL_W + GAP)
                ry = 55 + row_i * (CELL_H + GAP)
                rect = pygame.Rect(rx, ry, CELL_W, CELL_H)
                self._ferm_select_rects[bi] = rect
                pygame.draw.rect(self.screen, (40, 30, 12), rect)
                pygame.draw.rect(self.screen, (160, 110, 50), rect, 2)
                nm = BIOME_DISPLAY_NAMES.get(g.origin_biome, g.origin_biome)
                vn = VARIETY_DISPLAY_NAMES.get(g.variety, g.variety)
                ns = self.small.render(f"{nm}  {vn}", True, (230, 180, 100))
                self.screen.blit(ns, (rx + 6, ry + 6))
                qs = self.small.render(f"Crush: {CRUSH_STYLES.get(g.crush_style, {}).get('label', '-')}", True, (170, 130, 70))
                self.screen.blit(qs, (rx + 6, ry + 24))

        elif self._ferm_phase == "select_yeast":
            self._ferm_yeast_rects.clear()
            sub = self.small.render("Choose a yeast strain:", True, (190, 150, 80))
            self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 32))
            BTN_W, BTN_H, BTN_GAP = 260, 80, 14
            total_w = len(YEASTS) * BTN_W + (len(YEASTS) - 1) * BTN_GAP
            gx0 = (SCREEN_W - total_w) // 2
            for pi, (ykey, ydata) in enumerate(YEASTS.items()):
                px = gx0 + pi * (BTN_W + BTN_GAP)
                py = SCREEN_H // 2 - BTN_H // 2
                prect = pygame.Rect(px, py, BTN_W, BTN_H)
                self._ferm_yeast_rects[ykey] = prect
                pygame.draw.rect(self.screen, (38, 28, 10), prect)
                pygame.draw.rect(self.screen, (175, 125, 55), prect, 2)
                lbl = self.font.render(ydata["label"], True, (235, 185, 95))
                self.screen.blit(lbl, (px + BTN_W // 2 - lbl.get_width() // 2, py + 8))
                for di, dl in enumerate(ydata["desc"].split(". ")[:2]):
                    ds = self.small.render(dl, True, (175, 140, 70))
                    self.screen.blit(ds, (px + 8, py + 36 + di * 14))

        elif self._ferm_phase == "fermenting":
            total = self._ferm_total_time
            self._ferm_time += dt

            # Temperature physics
            if self._ferm_temp_held:
                self._ferm_temp_vel = min(1.0, self._ferm_temp_vel + 0.55 * dt)
            else:
                self._ferm_temp_vel = max(-0.7, self._ferm_temp_vel - 0.35 * dt)
            self._ferm_temp = max(0.0, min(1.0, self._ferm_temp + self._ferm_temp_vel * dt))

            # Nutrient physics: drifts down, hold N to add
            if self._ferm_nut_held:
                self._ferm_nutrient = min(1.0, self._ferm_nutrient + 0.45 * dt)
            else:
                self._ferm_nutrient = max(0.0, self._ferm_nutrient - 0.12 * dt)

            # Bands
            t_low, t_hi = 0.40, 0.70
            n_low, n_hi = 0.35, 0.65
            # Malolactic shift widens nutrient band after 30s
            if self._ferm_time >= 30.0:
                n_low, n_hi = 0.25, 0.75
            if t_low <= self._ferm_temp <= t_hi:
                self._ferm_temp_band_time += dt
            if n_low <= self._ferm_nutrient <= n_hi:
                self._ferm_nutrient_band_time += dt
            # Stuck / vinegar penalties
            if self._ferm_nutrient < 0.05:
                self._ferm_penalties = min(8, self._ferm_penalties + int(dt * 0.5))
            if self._ferm_time > 55.0:
                self._ferm_penalties = min(8, self._ferm_penalties + int(dt * 0.5))

            # Punchdown prompts ~every 8s, 3s window
            if self._ferm_punch_active_until > 0 and self._ferm_time >= self._ferm_punch_active_until:
                # Expired
                self._ferm_punch_total += 1
                self._ferm_punch_active_until = 0
                self._ferm_next_punch_time = self._ferm_time + 8.0
            if self._ferm_punch_active_until == 0 and self._ferm_time >= self._ferm_next_punch_time and self._ferm_time < total - 3.0:
                self._ferm_punch_active_until = self._ferm_time + 3.0

            # Milestones
            if not self._ferm_primary_hit and self._ferm_time >= 12.0:
                self._ferm_primary_hit = True
                self._ferm_event_flash = ("PRIMARY FERMENT", (240, 220, 120), 2.0)
            if not self._ferm_malolactic_hit and self._ferm_time >= 30.0:
                self._ferm_malolactic_hit = True
                self._ferm_event_flash = ("MALOLACTIC SHIFT", (200, 240, 140), 2.0)
            if not self._ferm_finish_hit and self._ferm_time >= 48.0:
                self._ferm_finish_hit = True
                self._ferm_event_flash = ("FERMENT FINISHED", (180, 220, 240), 2.0)
            if self._ferm_event_flash:
                txt, col, timer = self._ferm_event_flash
                timer -= dt
                if timer <= 0:
                    self._ferm_event_flash = None
                else:
                    self._ferm_event_flash = (txt, col, timer)

            # Layout: two gauges, time bar, punchdown button, stop button
            # Temp gauge (left)
            TX, TY, TW, TH = 60, 60, 28, SCREEN_H - 160
            pygame.draw.rect(self.screen, (20, 18, 12), (TX, TY, TW, TH))
            pygame.draw.rect(self.screen, (80, 60, 30), (TX, TY, TW, TH), 2)

            def _ty(v):
                return TY + TH - int(TH * v)

            pygame.draw.rect(self.screen, (35, 80, 45),
                             (TX, _ty(t_hi), TW, _ty(t_low) - _ty(t_hi)))
            pygame.draw.rect(self.screen, (100, 20, 20),
                             (TX, _ty(1.0), TW, _ty(t_hi) - _ty(1.0)))
            pygame.draw.rect(self.screen, (30, 50, 100),
                             (TX, _ty(t_low), TW, _ty(0.0) - _ty(t_low)))
            my = _ty(self._ferm_temp)
            pygame.draw.rect(self.screen, (240, 180, 100), (TX - 5, my - 3, TW + 10, 6))
            tl = self.small.render("TEMP", True, (200, 160, 80))
            self.screen.blit(tl, (TX - 4, TY - 18))
            tv = self.small.render(f"{self._ferm_temp:.0%}", True, (220, 170, 90))
            self.screen.blit(tv, (TX + TW + 4, my - 6))

            # Nutrient gauge (next to temp)
            NX = TX + TW + 50
            NY, NW, NH = TY, 28, TH
            pygame.draw.rect(self.screen, (20, 16, 14), (NX, NY, NW, NH))
            pygame.draw.rect(self.screen, (80, 50, 60), (NX, NY, NW, NH), 2)

            def _ny(v):
                return NY + NH - int(NH * v)

            pygame.draw.rect(self.screen, (100, 60, 90),
                             (NX, _ny(n_hi), NW, _ny(n_low) - _ny(n_hi)))
            pygame.draw.rect(self.screen, (90, 20, 30),
                             (NX, _ny(n_low), NW, _ny(0.0) - _ny(n_low)))
            my2 = _ny(self._ferm_nutrient)
            pygame.draw.rect(self.screen, (220, 130, 200), (NX - 5, my2 - 3, NW + 10, 6))
            nl = self.small.render("NUTR", True, (180, 120, 170))
            self.screen.blit(nl, (NX - 4, NY - 18))
            nv = self.small.render(f"{self._ferm_nutrient:.0%}", True, (210, 140, 190))
            self.screen.blit(nv, (NX + NW + 4, my2 - 6))

            # Alcohol readout (right side)
            stop_frac = self._ferm_time / total
            live_alcohol = 0.35 + stop_frac * 0.55
            ax = NX + NW + 60
            ay = TY + 6
            alc = self.font.render(f"Alcohol: {live_alcohol:.0%}", True, (220, 180, 100))
            self.screen.blit(alc, (ax, ay))
            drys = "Sweet" if stop_frac < 0.35 else ("Off-Dry" if stop_frac < 0.65 else "Dry")
            drl = self.small.render(f"If you stop now: {drys}", True, (180, 160, 120))
            self.screen.blit(drl, (ax, ay + 22))
            punch_info = self.small.render(f"Punchdowns: {self._ferm_punch_hits}/{self._ferm_punch_total}", True, (180, 150, 180))
            self.screen.blit(punch_info, (ax, ay + 42))

            # Punchdown prompt / button
            PUNCH_X, PUNCH_Y = SCREEN_W - 180, TY + 80
            PUNCH_W, PUNCH_H = 160, 60
            punch_rect = pygame.Rect(PUNCH_X, PUNCH_Y, PUNCH_W, PUNCH_H)
            self._ferm_punch_btn = punch_rect
            punch_active = self._ferm_punch_active_until > 0
            if punch_active:
                # flash border
                pulse = (int((self._ferm_time * 6) % 2) == 0)
                pygame.draw.rect(self.screen, (120, 50, 100), punch_rect)
                pygame.draw.rect(self.screen, (240, 140, 200) if pulse else (180, 90, 150), punch_rect, 3)
                pmsg = self.font.render("PUNCHDOWN!", True, (250, 200, 230))
                self.screen.blit(pmsg, (punch_rect.centerx - pmsg.get_width() // 2, punch_rect.centery - 12))
                rem = self._ferm_punch_active_until - self._ferm_time
                ps = self.small.render(f"{rem:.1f}s left  (P)", True, (230, 170, 210))
                self.screen.blit(ps, (punch_rect.centerx - ps.get_width() // 2, punch_rect.centery + 8))
            else:
                pygame.draw.rect(self.screen, (40, 28, 35), punch_rect)
                pygame.draw.rect(self.screen, (100, 70, 90), punch_rect, 2)
                nxt = max(0.0, self._ferm_next_punch_time - self._ferm_time)
                pmsg = self.small.render("Next punchdown", True, (160, 120, 140))
                self.screen.blit(pmsg, (punch_rect.centerx - pmsg.get_width() // 2, punch_rect.centery - 8))
                ps = self.small.render(f"in {nxt:.1f}s", True, (140, 100, 120))
                self.screen.blit(ps, (punch_rect.centerx - ps.get_width() // 2, punch_rect.centery + 6))

            # Time bar
            TBX, TBY = 140, SCREEN_H - 56
            TBW = SCREEN_W - 300
            pygame.draw.rect(self.screen, (22, 16, 12), (TBX, TBY, TBW, 18))
            pygame.draw.rect(self.screen, (80, 60, 30), (TBX, TBY, TBW, 18), 2)
            prog = min(1.0, self._ferm_time / total)
            pygame.draw.rect(self.screen, (180, 130, 80), (TBX, TBY, int(TBW * prog), 18))
            for tm, tl in [(12, "primary"), (30, "malolactic"), (48, "finish")]:
                tx = TBX + int(TBW * tm / total)
                pygame.draw.line(self.screen, (230, 190, 110), (tx, TBY - 4), (tx, TBY + 22), 2)
                ts = self.small.render(tl, True, (210, 170, 100))
                self.screen.blit(ts, (tx - ts.get_width() // 2, TBY - 18))
            ts = self.small.render(f"{self._ferm_time:.1f}s / {total:.0f}s", True, (200, 160, 90))
            self.screen.blit(ts, (TBX + TBW // 2 - ts.get_width() // 2, TBY + 22))

            if self._ferm_event_flash:
                txt, col, _ = self._ferm_event_flash
                ef = self.font.render(txt, True, col)
                self.screen.blit(ef, (SCREEN_W // 2 - ef.get_width() // 2, SCREEN_H // 2 - 60))

            inst = self.small.render("SPACE=TEMP  N=NUTRIENT  P=PUNCHDOWN  ENTER=STOP", True, (180, 140, 100))
            self.screen.blit(inst, (SCREEN_W // 2 - inst.get_width() // 2, TBY - 40))

            # Buttons (mouse alternatives)
            stop_rect = pygame.Rect(SCREEN_W - 150, SCREEN_H - 56, 130, 32)
            pygame.draw.rect(self.screen, (60, 28, 32), stop_rect)
            pygame.draw.rect(self.screen, (200, 100, 110), stop_rect, 2)
            sl = self.font.render("STOP", True, (240, 170, 180))
            self.screen.blit(sl, (stop_rect.centerx - sl.get_width() // 2, stop_rect.centery - sl.get_height() // 2))
            self._ferm_stop_btn = stop_rect

            temp_rect = pygame.Rect(SCREEN_W - 150, SCREEN_H - 96, 62, 32)
            tcol = (100, 50, 20) if not self._ferm_temp_held else (180, 90, 30)
            pygame.draw.rect(self.screen, tcol, temp_rect)
            pygame.draw.rect(self.screen, (220, 140, 60), temp_rect, 2)
            tl2 = self.small.render("TEMP", True, (250, 200, 100))
            self.screen.blit(tl2, (temp_rect.centerx - tl2.get_width() // 2, temp_rect.centery - tl2.get_height() // 2))
            self._ferm_temp_btn = temp_rect

            nut_rect = pygame.Rect(SCREEN_W - 82, SCREEN_H - 96, 62, 32)
            ncol = (70, 30, 60) if not self._ferm_nut_held else (140, 60, 120)
            pygame.draw.rect(self.screen, ncol, nut_rect)
            pygame.draw.rect(self.screen, (200, 120, 180), nut_rect, 2)
            nl2 = self.small.render("NUTR", True, (230, 170, 210))
            self.screen.blit(nl2, (nut_rect.centerx - nl2.get_width() // 2, nut_rect.centery - nl2.get_height() // 2))
            self._ferm_nut_btn = nut_rect

        elif self._ferm_phase == "result":
            bi = self._ferm_must_idx
            if bi is None or bi >= len(player.wine_grapes):
                self._ferm_phase = "select_must"
                return
            g = player.wine_grapes[bi]
            col = WINE_STYLE_COLORS.get(g.style, (150, 60, 80))
            cx2, cy2 = SCREEN_W // 2, 70
            pygame.draw.rect(self.screen, col, (cx2 - 40, cy2, 80, 80))
            pygame.draw.rect(self.screen, (230, 200, 180), (cx2 - 40, cy2, 80, 80), 2)
            iy2 = cy2 + 100
            def rline(t, c=(220, 180, 130)):
                nonlocal iy2
                s = self.font.render(t, True, c)
                self.screen.blit(s, (cx2 - s.get_width() // 2, iy2))
                iy2 += 24
            rline(WINE_STYLE_DESCS.get(g.style, g.style), col)
            rline(f"Alcohol: {g.alcohol:.0%}   Complexity: {g.complexity:.0%}", (200, 170, 120))
            stars = "★" * round(g.ferment_quality * 5) + "☆" * (5 - round(g.ferment_quality * 5))
            rline(stars, (230, 200, 90))
            if g.flavor_notes:
                rline("Flavour Notes:", (180, 150, 90))
                for note in g.flavor_notes[:6]:
                    rline(f"  • {note.title()}", (210, 180, 130))
            done_rect = pygame.Rect(cx2 - 70, iy2 + 10, 140, 34)
            pygame.draw.rect(self.screen, (50, 35, 20), done_rect)
            pygame.draw.rect(self.screen, (190, 140, 80), done_rect, 2)
            dl = self.font.render("DONE", True, (230, 180, 110))
            self.screen.blit(dl, (done_rect.centerx - dl.get_width() // 2, done_rect.centery - dl.get_height() // 2))
            self._ferm_result_done_btn = done_rect

    def _handle_fermenter_click(self, pos, player):
        if self._ferm_phase == "select_must":
            for bi, rect in self._ferm_select_rects.items():
                if rect.collidepoint(pos):
                    self._ferm_must_idx = bi
                    self._ferm_phase = "select_yeast"
                    return
        elif self._ferm_phase == "select_yeast":
            for ykey, yrect in self._ferm_yeast_rects.items():
                if yrect.collidepoint(pos):
                    bi = self._ferm_must_idx
                    if bi is not None and bi < len(player.wine_grapes):
                        g = player.wine_grapes[bi]
                        apply_yeast(g, ykey)
                        self._ferm_time = 0.0
                        self._ferm_temp = 0.45
                        self._ferm_temp_vel = 0.0
                        self._ferm_nutrient = 0.5
                        self._ferm_temp_band_time = 0.0
                        self._ferm_nutrient_band_time = 0.0
                        self._ferm_penalties = 0
                        self._ferm_primary_hit = False
                        self._ferm_malolactic_hit = False
                        self._ferm_finish_hit = False
                        self._ferm_event_flash = None
                        self._ferm_temp_held = False
                        self._ferm_nut_held = False
                        self._ferm_punch_hits = 0
                        self._ferm_punch_total = 0
                        self._ferm_next_punch_time = 8.0
                        self._ferm_punch_active_until = 0.0
                        self._ferm_phase = "fermenting"
                    return
        elif self._ferm_phase == "fermenting":
            if self._ferm_stop_btn and self._ferm_stop_btn.collidepoint(pos):
                self._finish_ferment(player)
                return
            if self._ferm_punch_btn and self._ferm_punch_btn.collidepoint(pos):
                self._register_punchdown()
                return
            if self._ferm_temp_btn and self._ferm_temp_btn.collidepoint(pos):
                self._ferm_temp_held = True
                return
            if self._ferm_nut_btn and self._ferm_nut_btn.collidepoint(pos):
                self._ferm_nut_held = True
                return
        elif self._ferm_phase == "result":
            if self._ferm_result_done_btn and self._ferm_result_done_btn.collidepoint(pos):
                self._ferm_phase = "select_must"
                self._ferm_must_idx = None
                return

    def _register_punchdown(self):
        if self._ferm_punch_active_until > 0 and self._ferm_time <= self._ferm_punch_active_until:
            self._ferm_punch_hits += 1
            self._ferm_punch_total += 1
            self._ferm_punch_active_until = 0
            self._ferm_next_punch_time = self._ferm_time + 8.0
            self._ferm_event_flash = ("PUNCHDOWN +1", (230, 170, 210), 1.0)

    def handle_fermenter_keys(self, keys):
        from blocks import FERMENTATION_BLOCK
        if self.refinery_block_id != FERMENTATION_BLOCK:
            return
        if self._ferm_phase == "fermenting":
            self._ferm_temp_held = bool(keys[pygame.K_SPACE])
            self._ferm_nut_held = bool(keys[pygame.K_n])

    def handle_fermenter_keydown(self, key, player):
        from blocks import FERMENTATION_BLOCK
        if self.refinery_block_id != FERMENTATION_BLOCK:
            return
        if self._ferm_phase == "fermenting":
            if key == pygame.K_p:
                self._register_punchdown()
            elif key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self._finish_ferment(player)

    def _finish_ferment(self, player):
        bi = self._ferm_must_idx
        if bi is None or bi >= len(player.wine_grapes):
            self._ferm_phase = "select_must"
            return
        g = player.wine_grapes[bi]
        total = self._ferm_total_time
        stop_frac = min(1.0, self._ferm_time / total)
        temp_band_frac = min(1.0, self._ferm_temp_band_time / max(0.1, self._ferm_time))
        nut_band_frac = min(1.0, self._ferm_nutrient_band_time / max(0.1, self._ferm_time))
        punch_hit_frac = (self._ferm_punch_hits / self._ferm_punch_total) if self._ferm_punch_total > 0 else 0.0
        apply_ferment_result(g, temp_band_frac, nut_band_frac, punch_hit_frac,
                             stop_frac, self._ferm_penalties, self._ferm_time, total)
        player.discovered_wine_origins.add(f"{g.origin_biome}_{g.style}")
        self._ferm_phase = "result"

    # ==================================================================
    # WINE CELLAR (tabs: blend / age / bottle)
    # ==================================================================

    def _draw_wine_cellar(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("WINE CELLAR", True, (200, 150, 140))
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, (100, 80, 80))
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        # Tab bar
        TAB_Y = 30
        TAB_W, TAB_H, TAB_GAP = 120, 28, 8
        tabs = [("blend", "BLEND"), ("age", "AGE"), ("bottle", "BOTTLE")]
        total_tw = len(tabs) * TAB_W + (len(tabs) - 1) * TAB_GAP
        tx0 = (SCREEN_W - total_tw) // 2
        self._cellar_tab_rects = {}
        for ti, (tkey, tlabel) in enumerate(tabs):
            tx = tx0 + ti * (TAB_W + TAB_GAP)
            trect = pygame.Rect(tx, TAB_Y, TAB_W, TAB_H)
            self._cellar_tab_rects[tkey] = trect
            is_sel = self._cellar_tab == tkey
            pygame.draw.rect(self.screen, (60, 30, 40) if is_sel else (30, 18, 24), trect)
            pygame.draw.rect(self.screen, (210, 140, 150) if is_sel else (110, 70, 80), trect, 2)
            tl = self.small.render(tlabel, True, (240, 180, 180) if is_sel else (150, 110, 120))
            self.screen.blit(tl, (trect.centerx - tl.get_width() // 2, trect.centery - tl.get_height() // 2))

        if self._cellar_tab == "blend":
            self._draw_cellar_blend(player)
        elif self._cellar_tab == "age":
            self._draw_cellar_age(player, dt)
        elif self._cellar_tab == "bottle":
            self._draw_cellar_bottle(player)

    def _blendable_wines(self, player):
        return [(i, g) for i, g in enumerate(player.wine_grapes)
                if g.state in ("fermented", "aged", "blended")]

    def _draw_cellar_blend(self, player):
        if self._blend_wine_phase == "result":
            g = self._blend_wine_result
            if g:
                col = WINE_STYLE_COLORS.get(g.style, (150, 60, 80))
                cx2, cy2 = SCREEN_W // 2, 80
                pygame.draw.rect(self.screen, col, (cx2 - 35, cy2, 70, 70))
                pygame.draw.rect(self.screen, (230, 200, 180), (cx2 - 35, cy2, 70, 70), 2)
                iy2 = cy2 + 90
                def bline(t, c=(220, 180, 130)):
                    nonlocal iy2
                    s = self.font.render(t, True, c)
                    self.screen.blit(s, (cx2 - s.get_width() // 2, iy2))
                    iy2 += 24
                bline("Blend Created!", (240, 190, 150))
                bline(WINE_STYLE_DESCS.get(g.style, g.style), col)
                if g.flavor_notes:
                    bline("Flavour Notes:", (180, 150, 130))
                    for note in g.flavor_notes[:6]:
                        bline(f"  {note.title()}", (210, 180, 140))
                done_rect = pygame.Rect(cx2 - 70, iy2 + 15, 140, 34)
                pygame.draw.rect(self.screen, (50, 30, 35), done_rect)
                pygame.draw.rect(self.screen, (190, 140, 150), done_rect, 2)
                dl = self.font.render("DONE", True, (230, 180, 190))
                self.screen.blit(dl, (done_rect.centerx - dl.get_width() // 2, done_rect.centery - dl.get_height() // 2))
                self._blend_wine_done_btn = done_rect
            return

        wines = self._blendable_wines(player)
        LIST_X, LIST_Y, LIST_W = 20, 70, 260
        pygame.draw.rect(self.screen, (20, 12, 16), (LIST_X, LIST_Y, LIST_W, SCREEN_H - LIST_Y - 10))
        pygame.draw.rect(self.screen, (80, 50, 60), (LIST_X, LIST_Y, LIST_W, SCREEN_H - LIST_Y - 10), 1)
        hdr = self.small.render("WINES (click to slot):", True, (170, 120, 130))
        self.screen.blit(hdr, (LIST_X + 4, LIST_Y + 4))
        self._blend_wine_list_rects.clear()
        for li, (bi, g) in enumerate(wines[:16]):
            ry = LIST_Y + 24 + li * 28
            rect = pygame.Rect(LIST_X + 4, ry, LIST_W - 8, 24)
            in_slot = bi in self._blend_wine_slots
            col = WINE_STYLE_COLORS.get(g.style, (120, 60, 80))
            pygame.draw.rect(self.screen, (50, 28, 32) if in_slot else (30, 15, 20), rect)
            pygame.draw.rect(self.screen, col, rect, 1)
            nm = BIOME_DISPLAY_NAMES.get(g.origin_biome, g.origin_biome)[:12]
            ns = self.small.render(f"{nm}  {g.style[:4]}", True, (220, 170, 180))
            self.screen.blit(ns, (LIST_X + 8, ry + 4))
            self._blend_wine_list_rects[bi] = rect

        SLOT_X0 = LIST_X + LIST_W + 20
        SLOT_W, SLOT_H, SLOT_GAP = 220, 80, 14
        self._blend_wine_slot_rects = []
        sub = self.small.render("BLEND SLOTS (2 required, 3rd optional):", True, (170, 120, 130))
        self.screen.blit(sub, (SLOT_X0, LIST_Y + 4))
        for si in range(3):
            sy = LIST_Y + 28 + si * (SLOT_H + SLOT_GAP)
            srect = pygame.Rect(SLOT_X0, sy, SLOT_W, SLOT_H)
            self._blend_wine_slot_rects.append(srect)
            bi = self._blend_wine_slots[si]
            if bi is not None and bi < len(player.wine_grapes):
                g = player.wine_grapes[bi]
                col = WINE_STYLE_COLORS.get(g.style, (120, 60, 80))
                pygame.draw.rect(self.screen, (45, 25, 30), srect)
                pygame.draw.rect(self.screen, col, srect, 2)
                nm = BIOME_DISPLAY_NAMES.get(g.origin_biome, g.origin_biome)
                vn = VARIETY_DISPLAY_NAMES.get(g.variety, g.variety)
                ns = self.small.render(f"{nm}  {vn}", True, (230, 180, 190))
                self.screen.blit(ns, (SLOT_X0 + 6, sy + 8))
                rs = self.small.render(f"Style: {g.style.title()}", True, col)
                self.screen.blit(rs, (SLOT_X0 + 6, sy + 26))
                if g.flavor_notes:
                    fn = self.small.render(", ".join(g.flavor_notes[:2]), True, (180, 140, 150))
                    self.screen.blit(fn, (SLOT_X0 + 6, sy + 44))
                cs = self.small.render("[X]", True, (200, 90, 110))
                self.screen.blit(cs, (SLOT_X0 + SLOT_W - 24, sy + 4))
            else:
                pygame.draw.rect(self.screen, (18, 10, 14), srect)
                pygame.draw.rect(self.screen, (60, 35, 45), srect, 1)
                es = self.small.render(f"Slot {si + 1}  (empty)", True, (90, 60, 70))
                self.screen.blit(es, (SLOT_X0 + 6, sy + 30))

        can = sum(1 for s in self._blend_wine_slots if s is not None) >= 2
        btn_col = (60, 35, 40) if can else (30, 18, 22)
        brd = (200, 140, 160) if can else (70, 40, 50)
        bbtn = pygame.Rect(SLOT_X0, LIST_Y + 28 + 3 * (SLOT_H + SLOT_GAP) + 10, 120, 36)
        pygame.draw.rect(self.screen, btn_col, bbtn)
        pygame.draw.rect(self.screen, brd, bbtn, 2)
        bl = self.font.render("BLEND", True, (230, 180, 200) if can else (90, 60, 75))
        self.screen.blit(bl, (bbtn.centerx - bl.get_width() // 2, bbtn.centery - bl.get_height() // 2))
        self._blend_wine_btn = bbtn

    def _draw_cellar_age(self, player, dt=0.0):
        if self._age_phase == "aging":
            self._draw_cellar_age_active(player, dt)
            return
        if self._age_phase == "result":
            self._draw_cellar_age_result()
            return

        fermented = [(i, g) for i, g in enumerate(player.wine_grapes)
                     if g.state in ("fermented", "blended")]
        LIST_X, LIST_Y, LIST_W = 20, 70, 240
        pygame.draw.rect(self.screen, (20, 12, 16), (LIST_X, LIST_Y, LIST_W, SCREEN_H - LIST_Y - 10))
        pygame.draw.rect(self.screen, (80, 50, 60), (LIST_X, LIST_Y, LIST_W, SCREEN_H - LIST_Y - 10), 1)
        hdr = self.small.render("FERMENTED WINES:", True, (170, 120, 130))
        self.screen.blit(hdr, (LIST_X + 4, LIST_Y + 4))
        self._age_wine_list_rects.clear()
        for li, (bi, g) in enumerate(fermented[:18]):
            ry = LIST_Y + 24 + li * 26
            rect = pygame.Rect(LIST_X + 4, ry, LIST_W - 8, 22)
            selected = self._age_wine_idx == bi
            col = WINE_STYLE_COLORS.get(g.style, (120, 60, 80))
            pygame.draw.rect(self.screen, (55, 30, 38) if selected else (30, 15, 20), rect)
            pygame.draw.rect(self.screen, col, rect, 2 if selected else 1)
            nm = BIOME_DISPLAY_NAMES.get(g.origin_biome, g.origin_biome)[:12]
            ns = self.small.render(f"{nm}  {g.style[:5]}", True, (220, 170, 180))
            self.screen.blit(ns, (LIST_X + 8, ry + 3))
            self._age_wine_list_rects[bi] = rect

        # Vessels
        VES_X = LIST_X + LIST_W + 20
        VES_W, VES_H, VES_GAP = 220, 70, 10
        self._age_vessel_rects.clear()
        for vi, (vkey, vdata) in enumerate(VESSELS.items()):
            vy = LIST_Y + 4 + vi * (VES_H + VES_GAP)
            vrect = pygame.Rect(VES_X, vy, VES_W, VES_H)
            self._age_vessel_rects[vkey] = vrect
            is_sel = self._age_vessel == vkey
            pygame.draw.rect(self.screen, (45, 25, 30) if is_sel else (25, 15, 20), vrect)
            pygame.draw.rect(self.screen, (210, 150, 160) if is_sel else (110, 70, 80), vrect, 2 if is_sel else 1)
            ml = self.font.render(vdata["label"], True, (235, 180, 190) if is_sel else (170, 130, 140))
            self.screen.blit(ml, (VES_X + 6, vy + 6))
            ds = self.small.render(vdata["desc"], True, (170, 130, 140))
            self.screen.blit(ds, (VES_X + 6, vy + 32))

        # Durations
        DUR_X = VES_X + VES_W + 20
        DUR_W = 150
        self._age_duration_rects.clear()
        dy = LIST_Y + 4
        dl = self.small.render("DURATION:", True, (170, 120, 130))
        self.screen.blit(dl, (DUR_X, dy))
        dy += 16
        for dkey, ddata in AGE_DURATIONS.items():
            drect = pygame.Rect(DUR_X, dy, DUR_W, 26)
            self._age_duration_rects[dkey] = drect
            is_sel = self._age_duration == dkey
            pygame.draw.rect(self.screen, (45, 25, 30) if is_sel else (25, 15, 20), drect)
            pygame.draw.rect(self.screen, (200, 140, 150) if is_sel else (90, 60, 70), drect, 2 if is_sel else 1)
            dtxt = self.small.render(ddata["label"], True, (230, 180, 190) if is_sel else (150, 110, 120))
            self.screen.blit(dtxt, (DUR_X + 6, dy + 5))
            dy += 30

        can_age = (self._age_wine_idx is not None
                   and self._age_wine_idx < len(player.wine_grapes)
                   and self._age_vessel is not None)
        age_btn = pygame.Rect(DUR_X, dy + 10, DUR_W, 36)
        pygame.draw.rect(self.screen, (55, 30, 38) if can_age else (25, 15, 20), age_btn)
        pygame.draw.rect(self.screen, (210, 140, 160) if can_age else (70, 40, 50), age_btn, 2)
        abl = self.font.render("AGE", True, (230, 180, 200) if can_age else (90, 60, 75))
        self.screen.blit(abl, (age_btn.centerx - abl.get_width() // 2, age_btn.centery - abl.get_height() // 2))
        self._age_btn = age_btn

    def _draw_cellar_age_active(self, player, dt):
        bi = self._age_wine_idx
        if bi is None or bi >= len(player.wine_grapes):
            self._age_phase = "select"
            return
        g = player.wine_grapes[bi]

        duration_secs = _age_duration_secs(self._age_duration)
        total_days = AGE_DURATIONS.get(self._age_duration, {}).get("days", 8)
        if not self._age_game_done:
            self._age_progress = min(1.0, self._age_progress + dt / duration_secs)
            self._age_care_prompt_timer -= dt
            if self._age_care_prompt_timer <= 0 and not self._age_care_active:
                self._age_care_active = True
                self._age_care_window = 4.0
            if self._age_care_active:
                self._age_care_window -= dt
                if self._age_care_window <= 0:
                    self._age_care_active = False
                    self._age_care_prompt_timer = max(5.0, duration_secs / 3)
            if self._age_progress >= 1.0:
                self._age_game_done = True

        cx = SCREEN_W // 2
        col = WINE_STYLE_COLORS.get(g.style, (120, 60, 80))
        nm = BIOME_DISPLAY_NAMES.get(g.origin_biome, g.origin_biome)
        vn = VARIETY_DISPLAY_NAMES.get(g.variety, g.variety)
        tl = self.font.render(f"Aging  {nm} {vn}", True, col)
        self.screen.blit(tl, (cx - tl.get_width() // 2, SCREEN_H // 2 - 80))
        vl = self.small.render(
            f"Vessel: {VESSELS.get(self._age_vessel, {}).get('label', self._age_vessel)}  —  "
            f"{AGE_DURATIONS.get(self._age_duration, {}).get('label', self._age_duration)}",
            True, (190, 150, 160))
        self.screen.blit(vl, (cx - vl.get_width() // 2, SCREEN_H // 2 - 55))

        bar_w = 400
        bar_x = cx - bar_w // 2
        bar_y = SCREEN_H // 2 - 10
        pygame.draw.rect(self.screen, (20, 12, 16), (bar_x, bar_y, bar_w, 30))
        pygame.draw.rect(self.screen, col, (bar_x, bar_y, int(bar_w * self._age_progress), 30))
        pygame.draw.rect(self.screen, (180, 130, 140), (bar_x, bar_y, bar_w, 30), 2)
        days_elapsed = int(self._age_progress * total_days)
        day_lbl = "day" if total_days == 1 else "days"
        pl = self.small.render(f"Aging: Day {days_elapsed} / {total_days} {day_lbl}", True, (200, 160, 170))
        self.screen.blit(pl, (cx - pl.get_width() // 2, SCREEN_H // 2 + 30))
        bonus_pct = int(self._age_care_bonus * 100)
        bl = self.small.render(f"Care bonus: +{bonus_pct}%", True, (170, 140, 150))
        self.screen.blit(bl, (cx - bl.get_width() // 2, SCREEN_H // 2 + 50))

        if self._age_care_active:
            flash = int(self._age_care_window * 4) % 2 == 0
            c_color = (100, 220, 100) if flash else (60, 160, 60)
            care_msg = self.font.render("PRESS W — Swirl the wine!", True, c_color)
            self.screen.blit(care_msg, (cx - care_msg.get_width() // 2, SCREEN_H // 2 - 120))

        if self._age_game_done:
            self._finish_cellar_age(player)

    def _finish_cellar_age(self, player):
        bi = self._age_wine_idx
        if bi is None or bi >= len(player.wine_grapes):
            self._age_phase = "select"
            return
        g = player.wine_grapes[bi]
        apply_aging(g, self._age_vessel, self._age_duration)
        g.ferment_quality = min(1.0, g.ferment_quality + self._age_care_bonus * 0.15)
        g.flavor_notes = generate_flavor_notes(g)
        player.discovered_wine_origins.add(f"{g.origin_biome}_{g.style}")
        self._age_phase = "result"
        self._age_wine_idx = None

    def _draw_cellar_age_result(self):
        cx = SCREEN_W // 2
        msg = self.font.render("Wine Aged!", True, (230, 180, 190))
        self.screen.blit(msg, (cx - msg.get_width() // 2, SCREEN_H // 2 - 40))
        ok = self.small.render("Click anywhere to continue", True, (170, 130, 140))
        self.screen.blit(ok, (cx - ok.get_width() // 2, SCREEN_H // 2 + 20))

    def _draw_cellar_bottle(self, player):
        if self._bottle_wine_result_id:
            self._draw_bottle_wine_result()
            return
        bottleable = [(i, g) for i, g in enumerate(player.wine_grapes)
                      if g.state in ("fermented", "aged", "blended")]
        LIST_X, LIST_Y, LIST_W = 20, 70, 230
        pygame.draw.rect(self.screen, (20, 12, 16), (LIST_X, LIST_Y, LIST_W, SCREEN_H - LIST_Y - 10))
        pygame.draw.rect(self.screen, (80, 50, 60), (LIST_X, LIST_Y, LIST_W, SCREEN_H - LIST_Y - 10), 1)
        hdr = self.small.render("READY WINES:", True, (170, 120, 130))
        self.screen.blit(hdr, (LIST_X + 4, LIST_Y + 4))
        self._bottle_wine_rects.clear()
        for li, (bi, g) in enumerate(bottleable[:18]):
            ry = LIST_Y + 24 + li * 26
            rect = pygame.Rect(LIST_X + 4, ry, LIST_W - 8, 22)
            selected = self._bottle_wine_idx == bi
            col = WINE_STYLE_COLORS.get(g.style, (120, 60, 80))
            pygame.draw.rect(self.screen, (55, 30, 38) if selected else (30, 15, 20), rect)
            pygame.draw.rect(self.screen, col, rect, 2 if selected else 1)
            nm = BIOME_DISPLAY_NAMES.get(g.origin_biome, g.origin_biome)[:11]
            vess = f" [{g.vessel[:3]}]" if g.vessel else ""
            ns = self.small.render(f"{nm}  {g.style[:5]}{vess}", True, (220, 170, 180))
            self.screen.blit(ns, (LIST_X + 8, ry + 3))
            self._bottle_wine_rects[bi] = rect

        # Serving glassware (method)
        GLS_X = LIST_X + LIST_W + 12
        GLS_W, GLS_H, GLS_GAP = 210, 58, 6
        self._bottle_method_rects.clear()
        for mi, (mkey, mdata) in enumerate(SERVING_METHODS.items()):
            my = LIST_Y + 4 + mi * (GLS_H + GLS_GAP)
            mrect = pygame.Rect(GLS_X, my, GLS_W, GLS_H)
            self._bottle_method_rects[mkey] = mrect
            is_sel = self._bottle_method == mkey
            col = WINE_STYLE_COLORS.get(mdata["style"], (120, 60, 80))
            pygame.draw.rect(self.screen, (45, 25, 30) if is_sel else (25, 15, 20), mrect)
            pygame.draw.rect(self.screen, col if is_sel else (80, 55, 65), mrect, 2 if is_sel else 1)
            ml = self.font.render(mdata["label"], True, (230, 180, 190) if is_sel else (160, 120, 130))
            self.screen.blit(ml, (GLS_X + 6, my + 4))
            bs = self.small.render(BUFF_DESCS.get(mdata["buff"], ""), True, (170, 140, 150))
            self.screen.blit(bs, (GLS_X + 6, my + 24))
            ss = self.small.render(f"For: {mdata['style'].title()}", True, (140, 110, 120))
            self.screen.blit(ss, (GLS_X + 6, my + 40))

        # Serving temp
        TMP_X = GLS_X + GLS_W + 12
        TMP_W = 140
        self._bottle_temp_rects.clear()
        ty = LIST_Y + 4
        tlbl = self.small.render("SERVE TEMP:", True, (170, 120, 130))
        self.screen.blit(tlbl, (TMP_X, ty))
        ty += 16
        for tkey, tdata in SERVING_TEMPS.items():
            trect = pygame.Rect(TMP_X, ty, TMP_W, 26)
            self._bottle_temp_rects[tkey] = trect
            is_sel = self._bottle_temp == tkey
            pygame.draw.rect(self.screen, (45, 28, 32) if is_sel else (22, 14, 18), trect)
            pygame.draw.rect(self.screen, (200, 140, 150) if is_sel else (90, 60, 70), trect, 2 if is_sel else 1)
            s = self.small.render(tdata["label"], True, (230, 180, 190) if is_sel else (150, 110, 120))
            self.screen.blit(s, (TMP_X + 6, ty + 5))
            ty += 30

        # Duration preview
        dm = get_bottle_duration_multiplier(self._bottle_temp)
        ty += 4
        prev = self.small.render(f"Duration ×{dm:.2f}", True, (160, 180, 160))
        self.screen.blit(prev, (TMP_X, ty))
        ty += 18

        # BOTTLE button
        can = self._bottle_wine_idx is not None and self._bottle_method is not None
        bbtn = pygame.Rect(TMP_X, ty + 8, TMP_W, 36)
        pygame.draw.rect(self.screen, (60, 30, 40) if can else (25, 15, 20), bbtn)
        pygame.draw.rect(self.screen, (210, 140, 160) if can else (70, 40, 50), bbtn, 2)
        bl = self.font.render("BOTTLE", True, (230, 180, 200) if can else (90, 60, 75))
        self.screen.blit(bl, (bbtn.centerx - bl.get_width() // 2, bbtn.centery - bl.get_height() // 2))
        self._bottle_btn = bbtn

        # Far right: selected wine detail
        DX = TMP_X + TMP_W + 12
        DW = SCREEN_W - DX - 8
        if DW > 60 and self._bottle_wine_idx is not None and self._bottle_wine_idx < len(player.wine_grapes):
            g = player.wine_grapes[self._bottle_wine_idx]
            col = WINE_STYLE_COLORS.get(g.style, (120, 60, 80))
            pygame.draw.rect(self.screen, (20, 12, 16), (DX, LIST_Y, DW, SCREEN_H - LIST_Y - 10))
            pygame.draw.rect(self.screen, col, (DX, LIST_Y, DW, SCREEN_H - LIST_Y - 10), 1)
            iy = LIST_Y + 8
            def dline(t, c=(210, 170, 180)):
                nonlocal iy
                s = self.small.render(t, True, c)
                self.screen.blit(s, (DX + 4, iy))
                iy += 14
            dline(BIOME_DISPLAY_NAMES.get(g.origin_biome, g.origin_biome), (230, 180, 190))
            dline(VARIETY_DISPLAY_NAMES.get(g.variety, g.variety), (210, 170, 180))
            dline(WINE_STYLE_DESCS.get(g.style, g.style), col)
            if g.vessel:
                dline(f"Aged: {VESSELS.get(g.vessel, {}).get('label', g.vessel)}", (170, 140, 150))
            dline(f"Alcohol {g.alcohol:.0%}  Complexity {g.complexity:.0%}", (190, 160, 170))
            stars = "★" * round(g.ferment_quality * 5)
            dline(stars, (230, 200, 90))
            for note in g.flavor_notes:
                dline(f"• {note.title()}", (200, 160, 170))

    def _handle_wine_cellar_click(self, pos, player):
        # Tabs always clickable
        for tkey, trect in self._cellar_tab_rects.items():
            if trect.collidepoint(pos):
                self._cellar_tab = tkey
                return
        if self._cellar_tab == "blend":
            self._handle_cellar_blend_click(pos, player)
        elif self._cellar_tab == "age":
            self._handle_cellar_age_click(pos, player)
        elif self._cellar_tab == "bottle":
            self._handle_cellar_bottle_click(pos, player)

    def _handle_cellar_blend_click(self, pos, player):
        if self._blend_wine_phase == "result":
            if self._blend_wine_done_btn and self._blend_wine_done_btn.collidepoint(pos):
                self._blend_wine_phase = "select"
                self._blend_wine_result = None
                self._blend_wine_slots = [None, None, None]
            return
        for bi, rect in self._blend_wine_list_rects.items():
            if rect.collidepoint(pos):
                if bi in self._blend_wine_slots:
                    idx = self._blend_wine_slots.index(bi)
                    self._blend_wine_slots[idx] = None
                else:
                    for si in range(3):
                        if self._blend_wine_slots[si] is None:
                            self._blend_wine_slots[si] = bi
                            break
                return
        for si, srect in enumerate(self._blend_wine_slot_rects):
            if srect.collidepoint(pos):
                self._blend_wine_slots[si] = None
                return
        if self._blend_wine_btn and self._blend_wine_btn.collidepoint(pos):
            filled = [s for s in self._blend_wine_slots if s is not None]
            if len(filled) >= 2:
                comps = [player.wine_grapes[bi] for bi in filled if bi < len(player.wine_grapes)]
                if len(comps) >= 2:
                    blended = make_blend(comps)
                    for bi in sorted(filled, reverse=True):
                        player.wine_grapes.pop(bi)
                    player.wine_grapes.append(blended)
                    player.discovered_wine_origins.add(f"blend_{blended.style}")
                    self._blend_wine_result = blended
                    self._blend_wine_phase = "result"
                    self._blend_wine_slots = [None, None, None]

    def handle_wine_age_keydown(self, key):
        if self._cellar_tab != "age" or self._age_phase != "aging":
            return
        if key == pygame.K_w and self._age_care_active:
            self._age_care_bonus = min(1.0, self._age_care_bonus + 0.12)
            self._age_care_active = False
            self._age_care_prompt_timer = max(5.0, _age_duration_secs(self._age_duration) / 3)

    def _handle_cellar_age_click(self, pos, player):
        if self._age_phase == "result":
            self._age_phase = "select"
            self._age_progress = 0.0
            self._age_care_bonus = 0.0
            self._age_game_done = False
            return
        if self._age_phase == "aging":
            return
        for bi, rect in self._age_wine_list_rects.items():
            if rect.collidepoint(pos):
                self._age_wine_idx = bi if self._age_wine_idx != bi else None
                return
        for vkey, vrect in self._age_vessel_rects.items():
            if vrect.collidepoint(pos):
                self._age_vessel = vkey
                return
        for dkey, drect in self._age_duration_rects.items():
            if drect.collidepoint(pos):
                self._age_duration = dkey
                return
        if self._age_btn and self._age_btn.collidepoint(pos):
            bi = self._age_wine_idx
            if (bi is not None and bi < len(player.wine_grapes)
                    and self._age_vessel in VESSELS):
                self._age_phase = "aging"
                self._age_progress = 0.0
                self._age_care_active = False
                self._age_care_window = 0.0
                self._age_care_prompt_timer = max(4.0, _age_duration_secs(self._age_duration) / 3)
                self._age_care_bonus = 0.0
                self._age_game_done = False

    def _handle_cellar_bottle_click(self, pos, player):
        if self._bottle_wine_result_id:
            self._bottle_wine_result_id = None
            self._bottle_wine_result_g = None
            return
        for bi, rect in self._bottle_wine_rects.items():
            if rect.collidepoint(pos):
                self._bottle_wine_idx = bi if self._bottle_wine_idx != bi else None
                return
        for mkey, mrect in self._bottle_method_rects.items():
            if mrect.collidepoint(pos):
                self._bottle_method = mkey
                return
        for tkey, trect in self._bottle_temp_rects.items():
            if trect.collidepoint(pos):
                self._bottle_temp = tkey
                return
        if self._bottle_btn and self._bottle_btn.collidepoint(pos):
            if self._bottle_wine_idx is None or self._bottle_method is None:
                return
            bi = self._bottle_wine_idx
            if bi >= len(player.wine_grapes):
                return
            g = player.wine_grapes[bi]
            method_data = SERVING_METHODS.get(self._bottle_method, {})
            effective_style = method_data.get("style", g.style)
            quality_bonus = get_bottle_quality_bonus(self._bottle_temp)
            eff_quality = min(1.0, g.ferment_quality + quality_bonus)
            output_id = get_bottle_output_id(effective_style, eff_quality)
            player.wine_grapes.pop(bi)
            self._bottle_wine_idx = None
            player._add_item(output_id)
            player.discovered_wine_origins.add(f"{g.origin_biome}_{effective_style}")
            self._bottle_wine_result_id = output_id
            self._bottle_wine_result_g = g

    def _draw_bottle_wine_result(self):
        from items import ITEMS
        cx = SCREEN_W // 2
        out_id = self._bottle_wine_result_id
        item_name = ITEMS.get(out_id, {}).get("name", out_id)
        g = self._bottle_wine_result_g
        col = WINE_STYLE_COLORS.get(g.style if g else "red", (180, 80, 100))
        msg = self.font.render("Wine Bottled!", True, (230, 180, 190))
        self.screen.blit(msg, (cx - msg.get_width() // 2, SCREEN_H // 2 - 60))
        nl = self.font.render(item_name, True, col)
        self.screen.blit(nl, (cx - nl.get_width() // 2, SCREEN_H // 2 - 20))
        if g and g.flavor_notes:
            fn = self.small.render(", ".join(g.flavor_notes[:4]), True, (190, 155, 165))
            self.screen.blit(fn, (cx - fn.get_width() // 2, SCREEN_H // 2 + 14))
        ok = self.small.render("Click anywhere to continue", True, (170, 130, 140))
        self.screen.blit(ok, (cx - ok.get_width() // 2, SCREEN_H // 2 + 45))

    # ==================================================================
    # Wine buff HUD (draws alongside coffee buffs)
    # ==================================================================

    def _draw_wine_buffs(self, player):
        if not getattr(player, "wine_buffs", None):
            return
        BUFF_COLORS = {
            "warmth":        (220, 80,  80),
            "serenity":      (160, 200, 220),
            "charm":         (230, 150, 180),
            "vivacity":      (240, 220, 140),
            "contemplation": (180, 130, 210),
        }
        # Render below any coffee buffs (coffee HUD starts at y=60, leave room).
        bx = SCREEN_W - 8
        # Count existing coffee buffs so wine column offsets below them.
        coffee_count = len(getattr(player, "active_buffs", {}) or {})
        by = 60 + coffee_count * (self.small.get_height() + 6)
        for buff, data in player.wine_buffs.items():
            dur = data["duration"]
            col = BUFF_COLORS.get(buff, (200, 150, 170))
            label = f"{buff.upper()} {dur:.0f}s"
            s = self.small.render(label, True, col)
            bx2 = bx - s.get_width() - 4
            pygame.draw.rect(self.screen, (20, 15, 20),
                             (bx2 - 4, by - 2, s.get_width() + 8, s.get_height() + 4))
            pygame.draw.rect(self.screen, col,
                             (bx2 - 4, by - 2, s.get_width() + 8, s.get_height() + 4), 1)
            self.screen.blit(s, (bx2, by))
            by += s.get_height() + 6
