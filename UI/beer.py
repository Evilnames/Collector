import pygame
from constants import SCREEN_W, SCREEN_H
from beer import (
    apply_brew_result, apply_ferment_result, apply_condition_result,
    make_beer_blend, get_bottle_output_id,
    MASH_TYPES, HOP_ADDITIONS, YEAST_TYPES, VESSEL_TYPES, CONDITION_DURATIONS,
    BUFF_DESCS, BEER_BUFFS, BEER_TYPE_DESCS, BEER_TYPE_COLORS, BIOME_DISPLAY_NAMES,
    _CODEX_BIOMES, BEER_TYPE_ORDER,
)

_SECS_PER_AGING_DAY = 5.0


def _condition_duration_secs(key):
    return CONDITION_DURATIONS.get(key, {}).get("days", 4) * _SECS_PER_AGING_DAY

_ACCENT   = (155, 205,  70)   # hoppy green
_MUTED    = ( 90, 130,  50)
_DARK_BG  = ( 22,  30,  14)
_MID_BG   = ( 38,  50,  24)


class BeerMixin:

    # ------------------------------------------------------------------ #
    #  Brew Kettle  (mash selection + boil/hop mini-game)                 #
    # ------------------------------------------------------------------ #

    def _draw_brew_kettle(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("BREW KETTLE", True, _ACCENT)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, _MUTED)
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        phase = self._brew_phase

        if phase == "select_hop":
            self._brew_hop_rects.clear()
            raw = [(i, b) for i, b in enumerate(player.beers) if b.state == "raw"]
            if not raw:
                msg = self.font.render("No raw hops! Harvest mature hop vines.", True, (100, 130, 60))
                self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2))
                return
            sub = self.small.render("Select a hop cluster to brew:", True, _ACCENT)
            self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 32))
            CELL_W, CELL_H, GAP, COLS = 200, 56, 8, 5
            gx0 = (SCREEN_W - (COLS * CELL_W + (COLS - 1) * GAP)) // 2
            for li, (bi, beer) in enumerate(raw[:20]):
                ci = li % COLS
                ri = li // COLS
                rx = gx0 + ci * (CELL_W + GAP)
                ry = 55 + ri * (CELL_H + GAP)
                rect = pygame.Rect(rx, ry, CELL_W, CELL_H)
                self._brew_hop_rects[bi] = rect
                pygame.draw.rect(self.screen, _DARK_BG, rect)
                pygame.draw.rect(self.screen, _MUTED, rect, 2)
                nm = BIOME_DISPLAY_NAMES.get(beer.origin_biome, beer.origin_biome)
                ns = self.small.render(f"{nm} — {beer.beer_type.replace('_', ' ').title()}", True, _ACCENT)
                self.screen.blit(ns, (rx + 6, ry + 8))
                gt = self.small.render(beer.grain_type.replace("_", " ").title(), True, _MUTED)
                self.screen.blit(gt, (rx + 6, ry + 26))

        elif phase == "select_mash":
            self._brew_mash_rects.clear()
            CX = SCREEN_W // 2
            beer = player.beers[self._brew_beer_idx]
            bm = BIOME_DISPLAY_NAMES.get(beer.origin_biome, beer.origin_biome)
            sub = self.font.render(f"{bm} — {beer.beer_type.replace('_', ' ').title()}", True, BEER_TYPE_COLORS.get(beer.beer_type, _ACCENT))
            self.screen.blit(sub, (CX - sub.get_width() // 2, 32))
            lbl = self.small.render("Choose your mash bill:", True, _ACCENT)
            self.screen.blit(lbl, (CX - lbl.get_width() // 2, 62))
            BTN_W, BTN_H, GAP = 310, 75, 10
            for i, (mkey, mdata) in enumerate(MASH_TYPES.items()):
                rx = CX - BTN_W // 2
                ry = 86 + i * (BTN_H + GAP)
                rect = pygame.Rect(rx, ry, BTN_W, BTN_H)
                self._brew_mash_rects[mkey] = rect
                is_sel = (mkey == self._brew_mash_sel)
                pygame.draw.rect(self.screen, (48, 65, 28) if is_sel else _DARK_BG, rect)
                pygame.draw.rect(self.screen, _ACCENT if is_sel else _MUTED, rect, 2 if is_sel else 1)
                ls = self.small.render(mdata["label"], True, _ACCENT if is_sel else (150, 180, 90))
                self.screen.blit(ls, (rx + 8, ry + 8))
                ds = self.small.render(mdata["desc"], True, (120, 150, 70) if is_sel else (80, 110, 50))
                self.screen.blit(ds, (rx + 8, ry + 28))
            if self._brew_mash_sel:
                btn = pygame.Rect(CX - 100, SCREEN_H - 70, 200, 40)
                self._brew_start_btn = btn
                pygame.draw.rect(self.screen, (30, 50, 15), btn)
                pygame.draw.rect(self.screen, _ACCENT, btn, 2)
                sl = self.font.render("BEGIN BREWING", True, _ACCENT)
                self.screen.blit(sl, (CX - sl.get_width() // 2, SCREEN_H - 62))

        elif phase == "brewing":
            self._update_brew_physics(dt)
            self._draw_brew_minigame(player)

        elif phase == "result":
            self._draw_brew_result(player)

    def _update_brew_physics(self, dt):
        if self._brew_heat_held:
            self._brew_temp_vel = min(1.0, self._brew_temp_vel + 0.016)
        else:
            self._brew_temp_vel = max(-0.55, self._brew_temp_vel - 0.009)
        self._brew_temp = max(0.0, min(1.0, self._brew_temp + self._brew_temp_vel * dt))
        self._brew_time += dt

        # Event flashes
        if 0.28 <= self._brew_temp <= 0.35 and not self._brew_mash_zone_hit:
            self._brew_mash_zone_hit = True
            self._brew_event_flash = ("MASH ZONE — Set your mash! [ENTER]", (80, 220, 120), 2.5)
        if 0.68 <= self._brew_temp <= 0.75 and not self._brew_boil_zone_hit:
            self._brew_boil_zone_hit = True
            self._brew_event_flash = ("BOIL — Add hops now! [ENTER]", (220, 200, 80), 2.5)
        if self._brew_event_flash:
            txt, col, timer = self._brew_event_flash
            timer -= dt
            self._brew_event_flash = (txt, col, timer) if timer > 0 else None

    def _draw_brew_minigame(self, player):
        CX = SCREEN_W // 2
        beer = player.beers[self._brew_beer_idx]
        bm = BIOME_DISPLAY_NAMES.get(beer.origin_biome, beer.origin_biome)
        tl = self.small.render(f"Brewing: {bm} {beer.beer_type.replace('_', ' ').title()}  |  Mash: {MASH_TYPES[self._brew_mash_sel]['label']}", True, _ACCENT)
        self.screen.blit(tl, (CX - tl.get_width() // 2, 32))

        # Temperature bar
        COL_X, COL_Y, COL_W, COL_H = CX - 250, 80, 40, 320
        pygame.draw.rect(self.screen, _DARK_BG, (COL_X, COL_Y, COL_W, COL_H))
        pygame.draw.rect(self.screen, _MUTED, (COL_X, COL_Y, COL_W, COL_H), 2)
        fill_h = int(COL_H * self._brew_temp)
        if fill_h > 0:
            col = (int(80 + self._brew_temp * 160), int(200 - self._brew_temp * 160), 40)
            pygame.draw.rect(self.screen, col, (COL_X, COL_Y + COL_H - fill_h, COL_W, fill_h))
        for frac, label, clr in [
            (0.30, "MASH",  (80, 220, 120)),
            (0.70, "BOIL",  (220, 200, 80)),
        ]:
            my = COL_Y + COL_H - int(COL_H * frac)
            pygame.draw.line(self.screen, clr, (COL_X - 6, my), (COL_X + COL_W + 6, my), 2)
            ls = self.small.render(label, True, clr)
            self.screen.blit(ls, (COL_X + COL_W + 10, my - 7))
        ts = self.small.render("TEMP", True, _MUTED)
        self.screen.blit(ts, (COL_X, COL_Y - 18))

        # Status
        if not self._brew_mash_set:
            ph_txt = "Step 1: Reach MASH zone and press ENTER"
            ph_col = (80, 220, 120)
        elif not self._brew_hop_set:
            ph_txt = "Step 2: Raise to BOIL zone and press ENTER"
            ph_col = (220, 200, 80)
        else:
            ph_txt = "Both steps done — press ENTER to finish"
            ph_col = _ACCENT
        ps = self.font.render(ph_txt, True, ph_col)
        self.screen.blit(ps, (CX - ps.get_width() // 2, 52))

        # Action button
        if not self._brew_mash_set:
            btn = pygame.Rect(CX - 130, 420, 260, 42)
            self._brew_action_btn = btn
            pygame.draw.rect(self.screen, (22, 45, 22), btn)
            pygame.draw.rect(self.screen, (80, 200, 100), btn, 2)
            bl = self.font.render("SET MASH  [ENTER]", True, (100, 230, 120))
            self.screen.blit(bl, (CX - bl.get_width() // 2, 432))
        elif not self._brew_hop_set:
            btn = pygame.Rect(CX - 130, 420, 260, 42)
            self._brew_action_btn = btn
            pygame.draw.rect(self.screen, (48, 45, 15), btn)
            pygame.draw.rect(self.screen, (210, 190, 60), btn, 2)
            bl = self.font.render("ADD HOPS  [ENTER]", True, (240, 220, 80))
            self.screen.blit(bl, (CX - bl.get_width() // 2, 432))
        else:
            btn = pygame.Rect(CX - 90, 420, 180, 42)
            self._brew_action_btn = btn
            pygame.draw.rect(self.screen, (20, 38, 16), btn)
            pygame.draw.rect(self.screen, (80, 200, 80), btn, 2)
            bl = self.font.render("FINISH  [ENTER]", True, (120, 230, 100))
            self.screen.blit(bl, (CX - bl.get_width() // 2, 432))

        hs = self.small.render("Hold SPACE to heat the kettle", True, _MUTED)
        self.screen.blit(hs, (CX - hs.get_width() // 2, 474))

        if self._brew_event_flash:
            txt, col, _ = self._brew_event_flash
            fs = self.font.render(txt, True, col)
            self.screen.blit(fs, (CX - fs.get_width() // 2, SCREEN_H // 2 - 20))

        # Quality preview bars
        mq_lbl = self.small.render(f"Mash quality:  {'✓' if self._brew_mash_set else '—'}  Hop timing:  {'✓' if self._brew_hop_set else '—'}", True, _MUTED)
        self.screen.blit(mq_lbl, (CX - mq_lbl.get_width() // 2, SCREEN_H - 30))

    def _draw_brew_result(self, player):
        beer = self._brew_result_beer
        if beer is None:
            return
        CX = SCREEN_W // 2
        rs = self.font.render("WORT BREWED", True, (80, 220, 120))
        self.screen.blit(rs, (CX - rs.get_width() // 2, 40))
        sc = BEER_TYPE_COLORS.get(beer.beer_type, _ACCENT)
        bm = BIOME_DISPLAY_NAMES.get(beer.origin_biome, beer.origin_biome)
        ns = self.font.render(f"{bm} {beer.beer_type.replace('_', ' ').title()}", True, sc)
        self.screen.blit(ns, (CX - ns.get_width() // 2, 78))
        qbar_x = CX - 150
        for label, val, col, y in [
            ("Bitterness",     beer.bitterness,     (180, 130, 60), 118),
            ("Maltiness",      beer.maltiness,      (210, 175, 80), 146),
            ("Wort Quality",   beer.ferment_quality,(100, 210, 100), 174),
        ]:
            ls = self.small.render(label, True, _MUTED)
            self.screen.blit(ls, (qbar_x, y))
            pygame.draw.rect(self.screen, _DARK_BG, (qbar_x + 110, y + 1, 200, 14))
            pygame.draw.rect(self.screen, col, (qbar_x + 110, y + 1, int(200 * val), 14))
        note_y = 210
        nts = self.small.render("Notes: " + ", ".join(beer.flavor_notes), True, (140, 170, 80))
        self.screen.blit(nts, (CX - nts.get_width() // 2, note_y))
        hint = self.small.render("Ready to ferment — take it to the Fermentation Vessel.", True, _MUTED)
        self.screen.blit(hint, (CX - hint.get_width() // 2, note_y + 22))
        self._brew_result_done_btn = pygame.Rect(CX - 70, SCREEN_H - 70, 140, 38)
        pygame.draw.rect(self.screen, (22, 40, 15), self._brew_result_done_btn)
        pygame.draw.rect(self.screen, (80, 200, 80), self._brew_result_done_btn, 2)
        ds = self.font.render("Done", True, (120, 220, 100))
        self.screen.blit(ds, (CX - ds.get_width() // 2, SCREEN_H - 62))

    def handle_brew_keydown(self, key, player):
        if key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            if self._brew_phase == "brewing":
                if not self._brew_mash_set:
                    self._brew_mash_set = True
                    # Quality based on how close we are to ideal mash zone center (0.375)
                    self._brew_mash_quality = max(0.0, 1.0 - abs(self._brew_temp - 0.375) * 4.0)
                elif not self._brew_hop_set:
                    self._brew_hop_set = True
                    # Quality based on how close we are to ideal boil zone center (0.775)
                    self._brew_hop_quality = max(0.0, 1.0 - abs(self._brew_temp - 0.775) * 4.0)
                else:
                    self._finish_brewing(player)

    def handle_brew_keys(self, keys):
        self._brew_heat_held = keys[pygame.K_SPACE]

    def _finish_brewing(self, player):
        bi = self._brew_beer_idx
        if bi is None or bi >= len(player.beers):
            return
        beer = player.beers[bi]
        apply_brew_result(beer, self._brew_mash_sel, self._brew_hop_add, self._brew_mash_quality, self._brew_hop_quality)
        self._brew_result_beer = beer
        self._brew_phase = "result"

    def _handle_brew_kettle_click(self, pos, player):
        if self._brew_phase == "select_hop":
            for idx, rect in self._brew_hop_rects.items():
                if rect.collidepoint(pos):
                    self._brew_beer_idx = idx
                    self._brew_phase = "select_mash"
                    self._brew_mash_sel = None
                    return

        elif self._brew_phase == "select_mash":
            for mkey, rect in self._brew_mash_rects.items():
                if rect.collidepoint(pos):
                    self._brew_mash_sel = mkey
                    return
            if (self._brew_start_btn and self._brew_start_btn.collidepoint(pos)
                    and self._brew_mash_sel):
                self._brew_phase = "brewing"
                self._brew_temp = 0.0
                self._brew_temp_vel = 0.0
                self._brew_heat_held = False
                self._brew_time = 0.0
                self._brew_mash_set = False
                self._brew_hop_set = False
                self._brew_mash_quality = 0.0
                self._brew_hop_quality = 0.0
                self._brew_hop_add = "early"
                self._brew_mash_zone_hit = False
                self._brew_boil_zone_hit = False
                self._brew_event_flash = None

        elif self._brew_phase == "brewing":
            if self._brew_action_btn and self._brew_action_btn.collidepoint(pos):
                self.handle_brew_keydown(pygame.K_RETURN, player)

        elif self._brew_phase == "result":
            if self._brew_result_done_btn and self._brew_result_done_btn.collidepoint(pos):
                self._brew_phase = "select_hop"
                self._brew_result_beer = None

    # ------------------------------------------------------------------ #
    #  Fermentation Vessel  (yeast selection + ferment monitoring)        #
    # ------------------------------------------------------------------ #

    def _draw_ferm_vessel(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("FERMENTATION VESSEL", True, (100, 200, 130))
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, _MUTED)
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        phase = self._ferm_phase
        if phase == "select_beer":
            self._ferm_beer_rects.clear()
            brewed = [(i, b) for i, b in enumerate(player.beers) if b.state == "brewed"]
            CX = SCREEN_W // 2
            if not brewed:
                msg = self.font.render("No brewed wort! Use the Brew Kettle first.", True, (80, 130, 80))
                self.screen.blit(msg, (CX - msg.get_width() // 2, SCREEN_H // 2))
                return
            sub = self.small.render("Select a brewed wort to ferment:", True, (100, 190, 110))
            self.screen.blit(sub, (CX - sub.get_width() // 2, 32))
            CELL_W, CELL_H, GAP, COLS = 200, 60, 8, 5
            gx0 = (SCREEN_W - (COLS * CELL_W + (COLS - 1) * GAP)) // 2
            for li, (bi, beer) in enumerate(brewed[:20]):
                ci = li % COLS
                ri = li // COLS
                rx = gx0 + ci * (CELL_W + GAP)
                ry = 55 + ri * (CELL_H + GAP)
                rect = pygame.Rect(rx, ry, CELL_W, CELL_H)
                self._ferm_beer_rects[bi] = rect
                pygame.draw.rect(self.screen, _DARK_BG, rect)
                pygame.draw.rect(self.screen, (60, 110, 70), rect, 2)
                nm = BIOME_DISPLAY_NAMES.get(beer.origin_biome, beer.origin_biome)
                ns = self.small.render(f"{nm} — {beer.beer_type.replace('_', ' ').title()}", True, (100, 200, 120))
                self.screen.blit(ns, (rx + 6, ry + 8))
                qs = self.small.render(f"Wort Q: {beer.ferment_quality:.0%}", True, (70, 140, 85))
                self.screen.blit(qs, (rx + 6, ry + 28))

        elif phase == "select_yeast":
            self._ferm_yeast_rects.clear()
            CX = SCREEN_W // 2
            beer = player.beers[self._ferm_beer_idx]
            bm = BIOME_DISPLAY_NAMES.get(beer.origin_biome, beer.origin_biome)
            sub = self.font.render(f"{bm} {beer.beer_type.replace('_', ' ').title()}", True, BEER_TYPE_COLORS.get(beer.beer_type, _ACCENT))
            self.screen.blit(sub, (CX - sub.get_width() // 2, 32))
            lbl = self.small.render("Choose your yeast strain:", True, (100, 190, 110))
            self.screen.blit(lbl, (CX - lbl.get_width() // 2, 60))
            BTN_W, BTN_H, GAP = 310, 75, 10
            for i, (ykey, ydata) in enumerate(YEAST_TYPES.items()):
                rx = CX - BTN_W // 2
                ry = 84 + i * (BTN_H + GAP)
                rect = pygame.Rect(rx, ry, BTN_W, BTN_H)
                self._ferm_yeast_rects[ykey] = rect
                is_sel = (ykey == self._ferm_yeast_sel)
                pygame.draw.rect(self.screen, (24, 48, 30) if is_sel else _DARK_BG, rect)
                pygame.draw.rect(self.screen, (80, 190, 100) if is_sel else (50, 100, 60), rect, 2 if is_sel else 1)
                ls = self.small.render(ydata["label"], True, (120, 220, 130) if is_sel else (80, 150, 90))
                self.screen.blit(ls, (rx + 8, ry + 8))
                ds = self.small.render(ydata["desc"], True, (90, 160, 100) if is_sel else (55, 100, 65))
                self.screen.blit(ds, (rx + 8, ry + 28))
            if self._ferm_yeast_sel:
                btn = pygame.Rect(CX - 110, SCREEN_H - 70, 220, 40)
                self._ferm_start_btn = btn
                pygame.draw.rect(self.screen, (20, 45, 25), btn)
                pygame.draw.rect(self.screen, (80, 190, 100), btn, 2)
                sl = self.font.render("BEGIN FERMENTATION", True, (100, 220, 120))
                self.screen.blit(sl, (CX - sl.get_width() // 2, SCREEN_H - 62))

        elif phase == "fermenting":
            self._update_ferm_physics(dt)
            self._draw_ferm_minigame(player, dt)

        elif phase == "result":
            self._draw_ferm_result(player)

    def _update_ferm_physics(self, dt):
        # Temperature drifts upward; SPACE cools it
        if self._ferm_cool_held:
            self._ferm_temp_vel = max(-0.70, self._ferm_temp_vel - 0.012)
        else:
            self._ferm_temp_vel = min(0.50, self._ferm_temp_vel + 0.006)
        self._ferm_temp = max(0.0, min(1.0, self._ferm_temp + self._ferm_temp_vel * dt))
        self._ferm_time += dt

        # Optimal zone: 0.30–0.55
        if 0.30 <= self._ferm_temp <= 0.55:
            self._ferm_time_in_optimal += dt

        # Rack prompts every ~10s
        self._ferm_rack_timer -= dt
        if self._ferm_rack_timer <= 0 and not self._ferm_rack_active:
            self._ferm_rack_active = True
            self._ferm_rack_window = 4.0
        if self._ferm_rack_active:
            self._ferm_rack_window -= dt
            if self._ferm_rack_window <= 0:
                self._ferm_rack_active = False
                self._ferm_rack_timer = 10.0

        if self._ferm_time >= self._ferm_duration and not self._ferm_done:
            self._ferm_done = True

    def _draw_ferm_minigame(self, player, dt):
        CX = SCREEN_W // 2
        beer = player.beers[self._ferm_beer_idx]
        bm = BIOME_DISPLAY_NAMES.get(beer.origin_biome, beer.origin_biome)
        tl = self.small.render(f"Fermenting: {bm} {beer.beer_type.replace('_', ' ').title()}  |  Yeast: {YEAST_TYPES[self._ferm_yeast_sel]['label']}", True, (100, 190, 110))
        self.screen.blit(tl, (CX - tl.get_width() // 2, 32))

        # Temperature gauge
        COL_X, COL_Y, COL_W, COL_H = CX - 250, 80, 40, 260
        pygame.draw.rect(self.screen, _DARK_BG, (COL_X, COL_Y, COL_W, COL_H))
        pygame.draw.rect(self.screen, (60, 100, 70), (COL_X, COL_Y, COL_W, COL_H), 2)
        fill_h = int(COL_H * self._ferm_temp)
        if fill_h > 0:
            col = (int(60 + self._ferm_temp * 180), int(180 - self._ferm_temp * 120), 60)
            pygame.draw.rect(self.screen, col, (COL_X, COL_Y + COL_H - fill_h, COL_W, fill_h))
        # Optimal zone band
        opt_lo = COL_Y + COL_H - int(COL_H * 0.55)
        opt_hi = COL_Y + COL_H - int(COL_H * 0.30)
        zone_surf = pygame.Surface((COL_W, opt_hi - opt_lo), pygame.SRCALPHA)
        zone_surf.fill((80, 220, 100, 40))
        self.screen.blit(zone_surf, (COL_X, opt_lo))
        pygame.draw.line(self.screen, (80, 200, 90), (COL_X - 6, opt_hi), (COL_X + COL_W + 6, opt_hi), 1)
        pygame.draw.line(self.screen, (80, 200, 90), (COL_X - 6, opt_lo), (COL_X + COL_W + 6, opt_lo), 1)
        zl = self.small.render("OPTIMAL", True, (80, 200, 90))
        self.screen.blit(zl, (COL_X + COL_W + 6, (opt_lo + opt_hi) // 2 - 7))
        ts = self.small.render("TEMP", True, _MUTED)
        self.screen.blit(ts, (COL_X, COL_Y - 18))

        # Progress bar
        progress = min(1.0, self._ferm_time / self._ferm_duration)
        bar_x, bar_y, bar_w = CX - 150, SCREEN_H // 2 + 40, 300
        pygame.draw.rect(self.screen, _DARK_BG, (bar_x, bar_y, bar_w, 22))
        pygame.draw.rect(self.screen, (80, 180, 100), (bar_x, bar_y, int(bar_w * progress), 22))
        pygame.draw.rect(self.screen, (60, 120, 75), (bar_x, bar_y, bar_w, 22), 2)
        pl = self.small.render(f"Fermentation: {int(progress*100)}%", True, (100, 190, 110))
        self.screen.blit(pl, (CX - pl.get_width() // 2, bar_y + 28))
        rb = self.small.render(f"Rack bonus: +{int(self._ferm_rack_bonus * 100)}%  |  Hold SPACE to cool", True, _MUTED)
        self.screen.blit(rb, (CX - rb.get_width() // 2, SCREEN_H - 30))

        if self._ferm_rack_active:
            flash = int(self._ferm_rack_window * 4) % 2 == 0
            rc = (100, 230, 110) if flash else (60, 160, 70)
            rm = self.font.render("PRESS W — Rack the wort!", True, rc)
            self.screen.blit(rm, (CX - rm.get_width() // 2, SCREEN_H // 2 - 30))

        if self._ferm_done:
            self._finish_fermentation(player)

    def _finish_fermentation(self, player):
        bi = self._ferm_beer_idx
        if bi is None or bi >= len(player.beers):
            self._ferm_phase = "select_beer"
            return
        beer = player.beers[bi]
        apply_ferment_result(
            beer, self._ferm_yeast_sel,
            self._ferm_time_in_optimal, self._ferm_time,
            self._ferm_rack_bonus, self._ferm_penalties,
        )
        self._ferm_result_beer = beer
        self._ferm_phase = "result"

    def _draw_ferm_result(self, player):
        beer = self._ferm_result_beer
        if beer is None:
            return
        CX = SCREEN_W // 2
        rs = self.font.render("FERMENTATION COMPLETE", True, (100, 220, 120))
        self.screen.blit(rs, (CX - rs.get_width() // 2, 40))
        sc = BEER_TYPE_COLORS.get(beer.beer_type, _ACCENT)
        bm = BIOME_DISPLAY_NAMES.get(beer.origin_biome, beer.origin_biome)
        ns = self.font.render(f"{bm} {beer.beer_type.replace('_', ' ').title()}", True, sc)
        self.screen.blit(ns, (CX - ns.get_width() // 2, 78))
        qbar_x = CX - 150
        for label, val, col, y in [
            ("Ferment Quality", beer.ferment_quality, (100, 210, 100), 118),
            ("Clarity",         beer.clarity,         (190, 225, 240), 146),
            ("Aroma",           beer.aroma,           (200, 230, 120), 174),
        ]:
            ls = self.small.render(label, True, _MUTED)
            self.screen.blit(ls, (qbar_x, y))
            pygame.draw.rect(self.screen, _DARK_BG, (qbar_x + 120, y + 1, 200, 14))
            pygame.draw.rect(self.screen, col, (qbar_x + 120, y + 1, int(200 * val), 14))
        note_y = 210
        nts = self.small.render("Notes: " + ", ".join(beer.flavor_notes), True, (140, 190, 100))
        self.screen.blit(nts, (CX - nts.get_width() // 2, note_y))
        hint = self.small.render("Ready to condition — take it to the Taproom.", True, _MUTED)
        self.screen.blit(hint, (CX - hint.get_width() // 2, note_y + 22))
        self._ferm_result_done_btn = pygame.Rect(CX - 70, SCREEN_H - 70, 140, 38)
        pygame.draw.rect(self.screen, (20, 42, 20), self._ferm_result_done_btn)
        pygame.draw.rect(self.screen, (80, 200, 80), self._ferm_result_done_btn, 2)
        ds = self.font.render("Done", True, (110, 220, 110))
        self.screen.blit(ds, (CX - ds.get_width() // 2, SCREEN_H - 62))

    def handle_ferm_keydown(self, key, player):
        if key == pygame.K_w and self._ferm_phase == "fermenting" and self._ferm_rack_active:
            self._ferm_rack_bonus = min(1.0, self._ferm_rack_bonus + 0.10)
            self._ferm_rack_active = False
            self._ferm_rack_timer = 10.0

    def handle_ferm_keys(self, keys):
        self._ferm_cool_held = keys[pygame.K_SPACE]

    def _handle_ferm_vessel_click(self, pos, player):
        if self._ferm_phase == "select_beer":
            for idx, rect in self._ferm_beer_rects.items():
                if rect.collidepoint(pos):
                    self._ferm_beer_idx = idx
                    self._ferm_phase = "select_yeast"
                    self._ferm_yeast_sel = None
                    return

        elif self._ferm_phase == "select_yeast":
            for ykey, rect in self._ferm_yeast_rects.items():
                if rect.collidepoint(pos):
                    self._ferm_yeast_sel = ykey
                    return
            if (self._ferm_start_btn and self._ferm_start_btn.collidepoint(pos)
                    and self._ferm_yeast_sel):
                self._ferm_phase = "fermenting"
                self._ferm_temp = 0.15
                self._ferm_temp_vel = 0.0
                self._ferm_cool_held = False
                self._ferm_time = 0.0
                self._ferm_duration = 45.0
                self._ferm_time_in_optimal = 0.0
                self._ferm_rack_timer = 10.0
                self._ferm_rack_active = False
                self._ferm_rack_window = 0.0
                self._ferm_rack_bonus = 0.0
                self._ferm_penalties = 0
                self._ferm_done = False

        elif self._ferm_phase == "fermenting":
            pass

        elif self._ferm_phase == "result":
            if self._ferm_result_done_btn and self._ferm_result_done_btn.collidepoint(pos):
                self._ferm_phase = "select_beer"
                self._ferm_result_beer = None

    # ------------------------------------------------------------------ #
    #  Taproom  (vessel + duration selection + conditioning mini-game)    #
    # ------------------------------------------------------------------ #

    def _draw_taproom(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("TAPROOM", True, (185, 145, 80))
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, (110, 90, 55))
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        phase = self._tap_phase
        if phase == "select":
            self._tap_beer_rects.clear()
            CX = SCREEN_W // 2
            fermented = [(i, b) for i, b in enumerate(player.beers)
                         if b.state in ("fermented", "blended")]
            if not fermented:
                msg = self.font.render("No fermented beer! Use the Fermentation Vessel first.", True, (130, 100, 55))
                self.screen.blit(msg, (CX - msg.get_width() // 2, SCREEN_H // 2))
                return
            sub = self.small.render("Select a fermented beer to condition:", True, (185, 150, 80))
            self.screen.blit(sub, (CX - sub.get_width() // 2, 32))
            CELL_W, CELL_H, GAP, COLS = 200, 60, 8, 5
            gx0 = (SCREEN_W - (COLS * CELL_W + (COLS - 1) * GAP)) // 2
            for li, (bi, beer) in enumerate(fermented[:20]):
                ci = li % COLS
                ri = li // COLS
                rx = gx0 + ci * (CELL_W + GAP)
                ry = 55 + ri * (CELL_H + GAP)
                rect = pygame.Rect(rx, ry, CELL_W, CELL_H)
                self._tap_beer_rects[bi] = rect
                sc = BEER_TYPE_COLORS.get(beer.beer_type, (180, 140, 60))
                pygame.draw.rect(self.screen, _DARK_BG, rect)
                pygame.draw.rect(self.screen, (120, 90, 40), rect, 2)
                nm = BIOME_DISPLAY_NAMES.get(beer.origin_biome, beer.origin_biome)
                ns = self.small.render(f"{nm} — {beer.beer_type.replace('_', ' ').title()}", True, sc)
                self.screen.blit(ns, (rx + 6, ry + 8))
                qs = self.small.render(f"Ferm Q: {beer.ferment_quality:.0%}", True, (130, 100, 50))
                self.screen.blit(qs, (rx + 6, ry + 28))

        elif phase == "configure":
            self._draw_tap_configure(player)

        elif phase == "conditioning":
            self._draw_tap_conditioning(player, dt)

        elif phase == "result":
            self._draw_tap_result(player)

    def _draw_tap_configure(self, player):
        self._tap_vessel_rects.clear()
        self._tap_duration_rects.clear()
        CX = SCREEN_W // 2
        beer = player.beers[self._tap_beer_idx]
        bm = BIOME_DISPLAY_NAMES.get(beer.origin_biome, beer.origin_biome)
        tl = self.font.render(f"{bm} {beer.beer_type.replace('_', ' ').title()}", True, BEER_TYPE_COLORS.get(beer.beer_type, _ACCENT))
        self.screen.blit(tl, (CX - tl.get_width() // 2, 32))

        # Vessel buttons (left)
        v_lbl = self.small.render("VESSEL", True, (175, 140, 65))
        self.screen.blit(v_lbl, (100, 58))
        BTN_W, BTN_H, GAP = 240, 72, 8
        for i, (vkey, vdata) in enumerate(VESSEL_TYPES.items()):
            ry = 80 + i * (BTN_H + GAP)
            rect = pygame.Rect(80, ry, BTN_W, BTN_H)
            self._tap_vessel_rects[vkey] = rect
            is_sel = (vkey == self._tap_vessel_sel)
            pygame.draw.rect(self.screen, (48, 35, 14) if is_sel else _DARK_BG, rect)
            pygame.draw.rect(self.screen, (175, 135, 55) if is_sel else (100, 75, 35), rect, 2 if is_sel else 1)
            ls = self.small.render(vdata["label"], True, (225, 185, 80) if is_sel else (150, 115, 50))
            self.screen.blit(ls, (88, ry + 8))
            ds = self.small.render(vdata["desc"], True, (155, 120, 55) if is_sel else (95, 70, 38))
            self.screen.blit(ds, (88, ry + 28))

        # Duration buttons (right)
        d_lbl = self.small.render("CONDITION TIME", True, (175, 140, 65))
        self.screen.blit(d_lbl, (380, 58))
        for i, (dkey, ddata) in enumerate(CONDITION_DURATIONS.items()):
            ry = 80 + i * (BTN_H + GAP)
            rect = pygame.Rect(360, ry, BTN_W, BTN_H)
            self._tap_duration_rects[dkey] = rect
            is_sel = (dkey == self._tap_duration_sel)
            pygame.draw.rect(self.screen, (48, 35, 14) if is_sel else _DARK_BG, rect)
            pygame.draw.rect(self.screen, (175, 135, 55) if is_sel else (100, 75, 35), rect, 2 if is_sel else 1)
            ls = self.small.render(ddata["label"], True, (225, 185, 80) if is_sel else (150, 115, 50))
            self.screen.blit(ls, (368, ry + 28))

        # Dry-hop toggle
        dh_rect = pygame.Rect(CX + 60, 80, 180, 42)
        self._tap_dryhop_btn = dh_rect
        pygame.draw.rect(self.screen, (28, 48, 20) if self._tap_dry_hop else _DARK_BG, dh_rect)
        pygame.draw.rect(self.screen, _ACCENT if self._tap_dry_hop else _MUTED, dh_rect, 2)
        dh_lbl = self.small.render("DRY HOP: " + ("ON" if self._tap_dry_hop else "OFF"), True, _ACCENT if self._tap_dry_hop else _MUTED)
        self.screen.blit(dh_lbl, (CX + 68, 93))

        can_start = (self._tap_vessel_sel is not None and self._tap_duration_sel is not None)
        btn = pygame.Rect(CX - 110, SCREEN_H - 70, 220, 40)
        self._tap_start_btn = btn
        bc = (30, 50, 15) if can_start else (20, 20, 20)
        bbc = _ACCENT if can_start else (50, 50, 50)
        pygame.draw.rect(self.screen, bc, btn)
        pygame.draw.rect(self.screen, bbc, btn, 2)
        sl = self.font.render("BEGIN CONDITIONING", True, _ACCENT if can_start else (60, 60, 60))
        self.screen.blit(sl, (CX - sl.get_width() // 2, SCREEN_H - 62))

    def _draw_tap_conditioning(self, player, dt):
        bi = self._tap_beer_idx
        if bi is None or bi >= len(player.beers):
            self._tap_phase = "select"
            return
        beer = player.beers[bi]

        duration_secs = _condition_duration_secs(self._tap_duration_sel)
        total_days = CONDITION_DURATIONS.get(self._tap_duration_sel, {}).get("days", 4)
        if not self._tap_cond_done:
            self._tap_cond_progress = min(1.0, self._tap_cond_progress + dt / duration_secs)
            # Dry-hop window: last 30%
            if self._tap_dry_hop and self._tap_cond_progress >= 0.70 and not self._tap_dryhop_done:
                self._tap_dryhop_active = True

            if self._tap_cond_progress >= 1.0:
                self._tap_cond_done = True

        CX = SCREEN_W // 2
        sc = BEER_TYPE_COLORS.get(beer.beer_type, _ACCENT)
        bm = BIOME_DISPLAY_NAMES.get(beer.origin_biome, beer.origin_biome)
        tl = self.font.render(f"Conditioning  {bm} {beer.beer_type.replace('_', ' ').title()}", True, sc)
        self.screen.blit(tl, (CX - tl.get_width() // 2, SCREEN_H // 2 - 80))
        vl = self.small.render(
            f"{VESSEL_TYPES[self._tap_vessel_sel]['label']}  —  {CONDITION_DURATIONS[self._tap_duration_sel]['label']}",
            True, (175, 140, 65))
        self.screen.blit(vl, (CX - vl.get_width() // 2, SCREEN_H // 2 - 55))

        bar_w = 400
        bar_x = CX - bar_w // 2
        bar_y = SCREEN_H // 2 - 10
        pygame.draw.rect(self.screen, _DARK_BG, (bar_x, bar_y, bar_w, 30))
        pygame.draw.rect(self.screen, sc, (bar_x, bar_y, int(bar_w * self._tap_cond_progress), 30))
        pygame.draw.rect(self.screen, (160, 130, 55), (bar_x, bar_y, bar_w, 30), 2)
        # Dry-hop zone marker
        if self._tap_dry_hop:
            mx = bar_x + int(bar_w * 0.70)
            pygame.draw.line(self.screen, _ACCENT, (mx, bar_y - 4), (mx, bar_y + 34), 2)
            hl = self.small.render("DH", True, _ACCENT)
            self.screen.blit(hl, (mx + 4, bar_y - 4))
        days_elapsed = int(self._tap_cond_progress * total_days)
        day_lbl = "day" if total_days == 1 else "days"
        pl = self.small.render(f"Conditioning: Day {days_elapsed} / {total_days} {day_lbl}", True, (180, 150, 70))
        self.screen.blit(pl, (CX - pl.get_width() // 2, SCREEN_H // 2 + 30))
        if self._tap_dry_hop:
            dh_bonus_pct = int(self._tap_dryhop_bonus * 100)
            dl = self.small.render(f"Dry-hop aroma bonus: +{dh_bonus_pct}%", True, _MUTED)
            self.screen.blit(dl, (CX - dl.get_width() // 2, SCREEN_H // 2 + 50))

        if self._tap_dryhop_active and not self._tap_dryhop_done:
            flash = int(self._tap_cond_progress * 20) % 2 == 0
            fc = _ACCENT if flash else _MUTED
            dm = self.font.render("PRESS W — Dry hop the beer!", True, fc)
            self.screen.blit(dm, (CX - dm.get_width() // 2, SCREEN_H // 2 - 120))

        if self._tap_cond_done:
            self._finish_conditioning(player)

    def _finish_conditioning(self, player):
        bi = self._tap_beer_idx
        if bi is None or bi >= len(player.beers):
            self._tap_phase = "select"
            return
        beer = player.beers[bi]
        apply_condition_result(
            beer, self._tap_vessel_sel, self._tap_duration_sel,
            self._tap_dry_hop, self._tap_dryhop_bonus,
        )
        output_id = get_bottle_output_id(beer.beer_type, beer.condition_quality)
        player._add_item(output_id)
        tier = "reserve" if beer.condition_quality >= 0.70 else "fine" if beer.condition_quality >= 0.40 else "standard"
        player.discovered_beers.add(f"{beer.origin_biome}_{tier}")
        player.beers.pop(bi)
        self._tap_result_id = output_id
        self._tap_result_beer_type = beer.beer_type
        self._tap_result_quality = beer.condition_quality
        self._tap_result_notes = beer.flavor_notes[:]
        self._tap_phase = "result"
        self._tap_beer_idx = None

    def _draw_tap_result(self, player):
        CX = SCREEN_W // 2
        rs = self.font.render("BEER READY!", True, (220, 190, 80))
        self.screen.blit(rs, (CX - rs.get_width() // 2, 40))
        if self._tap_result_id:
            from items import ITEMS
            item_name = ITEMS.get(self._tap_result_id, {}).get("name", self._tap_result_id)
            sc = BEER_TYPE_COLORS.get(self._tap_result_beer_type, _ACCENT)
            ns = self.font.render(item_name, True, sc)
            self.screen.blit(ns, (CX - ns.get_width() // 2, 80))
            tier_txt = ("Reserve" if self._tap_result_quality >= 0.70
                        else "Fine" if self._tap_result_quality >= 0.40 else "Standard")
            qs = self.font.render(f"Quality: {tier_txt}  ({self._tap_result_quality:.0%})", True, (190, 160, 70))
            self.screen.blit(qs, (CX - qs.get_width() // 2, 118))
            buff_key = BEER_BUFFS.get(self._tap_result_beer_type, "")
            if buff_key and buff_key in BUFF_DESCS:
                bs = self.small.render(f"Buff: {BUFF_DESCS[buff_key]}", True, (150, 190, 100))
                self.screen.blit(bs, (CX - bs.get_width() // 2, 156))
            if self._tap_result_notes:
                nts = self.small.render("Notes: " + ", ".join(self._tap_result_notes[:5]), True, (140, 175, 80))
                self.screen.blit(nts, (CX - nts.get_width() // 2, 188))
        ok_btn = pygame.Rect(CX - 70, SCREEN_H - 70, 140, 38)
        self._tap_result_done_btn = ok_btn
        pygame.draw.rect(self.screen, (30, 48, 14), ok_btn)
        pygame.draw.rect(self.screen, _ACCENT, ok_btn, 2)
        ds = self.font.render("Done", True, _ACCENT)
        self.screen.blit(ds, (CX - ds.get_width() // 2, SCREEN_H - 62))

    def handle_tap_keydown(self, key, player):
        if key == pygame.K_w and self._tap_phase == "conditioning" and self._tap_dryhop_active:
            self._tap_dryhop_bonus = min(1.0, self._tap_dryhop_bonus + 0.15)
            self._tap_dryhop_done = True
            self._tap_dryhop_active = False

    def _handle_taproom_click(self, pos, player):
        if self._tap_phase == "select":
            for idx, rect in self._tap_beer_rects.items():
                if rect.collidepoint(pos):
                    self._tap_beer_idx = idx
                    self._tap_phase = "configure"
                    self._tap_vessel_sel = None
                    self._tap_duration_sel = None
                    self._tap_dry_hop = False
                    return

        elif self._tap_phase == "configure":
            for vkey, rect in self._tap_vessel_rects.items():
                if rect.collidepoint(pos):
                    self._tap_vessel_sel = vkey
                    return
            for dkey, rect in self._tap_duration_rects.items():
                if rect.collidepoint(pos):
                    self._tap_duration_sel = dkey
                    return
            if self._tap_dryhop_btn and self._tap_dryhop_btn.collidepoint(pos):
                self._tap_dry_hop = not self._tap_dry_hop
                return
            if (self._tap_start_btn and self._tap_start_btn.collidepoint(pos)
                    and self._tap_vessel_sel and self._tap_duration_sel):
                self._tap_phase = "conditioning"
                self._tap_cond_progress = 0.0
                self._tap_cond_done = False
                self._tap_dryhop_active = False
                self._tap_dryhop_done = False
                self._tap_dryhop_bonus = 0.0

        elif self._tap_phase == "result":
            if self._tap_result_done_btn and self._tap_result_done_btn.collidepoint(pos):
                self._tap_phase = "select"
                self._tap_result_id = None

    # ------------------------------------------------------------------ #
    #  Beer Codex                                                         #
    # ------------------------------------------------------------------ #

    def _draw_beer_codex(self, player, gy0=58, gx_off=0):
        import pygame as _pg
        TIERS = ["standard", "fine", "reserve"]
        TIER_COLS = [(190, 190, 190), (220, 190, 100), (230, 200, 60)]
        CELL_W, CELL_H = 72, 42
        GAP = 4
        ROW_LABEL_W = 80
        GRID_X = gx_off + ROW_LABEL_W + 12
        GRID_Y = gy0 + 28

        # Column headers
        for ti, (tier, col) in enumerate(zip(TIERS, TIER_COLS)):
            hx = GRID_X + ti * (CELL_W + GAP)
            hs = self.small.render(tier.upper(), True, col)
            self.screen.blit(hs, (hx + CELL_W // 2 - hs.get_width() // 2, gy0 + 4))

        self._beer_codex_rects.clear()
        total_h = len(_CODEX_BIOMES) * (CELL_H + GAP)
        visible_h = SCREEN_H - GRID_Y - 4
        self._max_beer_codex_scroll = max(0, total_h - visible_h)
        self._beer_codex_scroll = min(self._beer_codex_scroll, self._max_beer_codex_scroll)

        clip = _pg.Rect(gx_off, GRID_Y, SCREEN_W - gx_off - 300, visible_h)
        self.screen.set_clip(clip)
        for ri, biome in enumerate(_CODEX_BIOMES):
            ry = GRID_Y + ri * (CELL_H + GAP) - self._beer_codex_scroll
            if ry + CELL_H <= GRID_Y or ry >= GRID_Y + visible_h:
                continue
            # Row label
            bname = BIOME_DISPLAY_NAMES.get(biome, biome)
            ls = self.small.render(bname, True, (150, 170, 100))
            self.screen.blit(ls, (gx_off + 4, ry + CELL_H // 2 - ls.get_height() // 2))
            # Tier cells
            for ti, tier in enumerate(TIERS):
                key = f"{biome}_{tier}"
                discovered = key in player.discovered_beers
                cx = GRID_X + ti * (CELL_W + GAP)
                rect = _pg.Rect(cx, ry, CELL_W, CELL_H)
                if clip.contains(rect):
                    self._beer_codex_rects[key] = rect
                is_sel = (self._beer_codex_selected == key)
                if discovered:
                    bg = (40, 55, 22) if not is_sel else (60, 82, 30)
                    brd = TIER_COLS[ti]
                else:
                    bg = (18, 22, 12)
                    brd = (45, 55, 30)
                _pg.draw.rect(self.screen, bg, rect)
                _pg.draw.rect(self.screen, brd, rect, 2 if is_sel else 1)
                if discovered:
                    # Beer type icon (colored circle)
                    sc = BEER_TYPE_COLORS.get(BIOME_BEER_PROFILES_LOOKUP(biome), _ACCENT)
                    _pg.draw.circle(self.screen, sc, (cx + CELL_W // 2, ry + CELL_H // 2), 9)
                else:
                    qs = self.small.render("?", True, (50, 65, 35))
                    self.screen.blit(qs, (cx + CELL_W // 2 - qs.get_width() // 2, ry + CELL_H // 2 - qs.get_height() // 2))
        self.screen.set_clip(None)

        # Detail panel
        PANEL_X = SCREEN_W - 285
        PANEL_W = 275
        sel = self._beer_codex_selected
        if sel and sel in player.discovered_beers:
            parts = sel.rsplit("_", 1)
            if len(parts) == 2:
                biome, tier = parts[0], parts[1]
                from beer import BIOME_BEER_PROFILES, BIOME_DISPLAY_NAMES as BDN
                profile = BIOME_BEER_PROFILES.get(biome, {})
                beer_type = profile.get("beer_type", "ale")
                sc = BEER_TYPE_COLORS.get(beer_type, _ACCENT)
                _pg.draw.rect(self.screen, (20, 28, 12), (PANEL_X, gy0, PANEL_W, SCREEN_H - gy0 - 4))
                _pg.draw.rect(self.screen, _MUTED, (PANEL_X, gy0, PANEL_W, SCREEN_H - gy0 - 4), 1)
                nm = self.font.render(f"{BDN.get(biome, biome)}", True, sc)
                self.screen.blit(nm, (PANEL_X + PANEL_W // 2 - nm.get_width() // 2, gy0 + 8))
                bt_s = self.small.render(beer_type.replace("_", " ").title() + f"  [{tier.upper()}]", True, (155, 185, 90))
                self.screen.blit(bt_s, (PANEL_X + PANEL_W // 2 - bt_s.get_width() // 2, gy0 + 32))
                _pg.draw.line(self.screen, _MUTED, (PANEL_X + 8, gy0 + 52), (PANEL_X + PANEL_W - 8, gy0 + 52), 1)
                desc = BEER_TYPE_DESCS.get(beer_type, "")
                desc_s = self.small.render(desc, True, (130, 160, 80))
                self.screen.blit(desc_s, (PANEL_X + 8, gy0 + 60))
                buff_key = BEER_BUFFS.get(beer_type, "")
                if buff_key in BUFF_DESCS:
                    bs = self.small.render(f"Buff: {BUFF_DESCS[buff_key]}", True, (140, 190, 90))
                    self.screen.blit(bs, (PANEL_X + 8, gy0 + 80))

        # Scroll hint
        self._draw_sidebar_scroll_hint(GRID_Y, visible_h, gx_off + ROW_LABEL_W + 8,
                                       self._beer_codex_scroll, self._max_beer_codex_scroll)

    def _handle_beer_codex_click(self, pos):
        for key, rect in self._beer_codex_rects.items():
            if rect.collidepoint(pos):
                self._beer_codex_selected = key if self._beer_codex_selected != key else None
                return


def BIOME_BEER_PROFILES_LOOKUP(biome):
    from beer import BIOME_BEER_PROFILES
    return BIOME_BEER_PROFILES.get(biome, {}).get("beer_type", "ale")
