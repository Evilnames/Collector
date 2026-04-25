import pygame
from constants import SCREEN_W, SCREEN_H
from spirits import (
    apply_distillation_result, apply_barrel_aging, make_blend,
    get_bottle_output_id,
    BARREL_TYPES, AGE_DURATIONS, BUFF_DESCS, SPIRIT_BUFFS,
    SPIRIT_TYPE_DESCS, SPIRIT_TYPE_COLORS, BIOME_DISPLAY_NAMES,
)

_BARREL_AGE_TIMES = {"short": 12.0, "medium": 24.0, "long": 40.0}


class SpiritsMixin:

    # ------------------------------------------------------------------ #
    #  Copper Still  (distillation mini-game — mirrors the Roaster)       #
    # ------------------------------------------------------------------ #

    def _draw_still(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("COPPER STILL", True, (210, 145, 60))
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, (100, 80, 50))
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        if self._still_phase == "select_spirit":
            self._still_select_rects.clear()
            raw = [(i, s) for i, s in enumerate(player.spirits) if s.state == "raw"]
            if not raw:
                msg = self.font.render("No raw grain mash! Harvest mature grain plants.", True, (130, 100, 60))
                self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2))
                return
            sub = self.small.render("Select a raw mash to distill:", True, (180, 140, 60))
            self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 32))
            CELL_W, CELL_H, GAP, COLS = 200, 56, 8, 5
            gx0 = (SCREEN_W - (COLS * CELL_W + (COLS - 1) * GAP)) // 2
            for li, (si, spirit) in enumerate(raw[:20]):
                col_i = li % COLS
                row_i = li // COLS
                rx = gx0 + col_i * (CELL_W + GAP)
                ry = 55 + row_i * (CELL_H + GAP)
                rect = pygame.Rect(rx, ry, CELL_W, CELL_H)
                self._still_select_rects[si] = rect
                pygame.draw.rect(self.screen, (38, 28, 14), rect)
                pygame.draw.rect(self.screen, (160, 105, 40), rect, 2)
                nm = BIOME_DISPLAY_NAMES.get(spirit.origin_biome, spirit.origin_biome)
                ns = self.small.render(f"{nm} — {spirit.spirit_type.title()}", True, (220, 175, 80))
                self.screen.blit(ns, (rx + 6, ry + 8))
                gt = self.small.render(spirit.grain_type.replace("_", " ").title(), True, (140, 110, 60))
                self.screen.blit(gt, (rx + 6, ry + 26))

        elif self._still_phase == "distilling":
            self._update_still_physics(dt)
            self._draw_still_minigame(player)

        elif self._still_phase == "result":
            self._draw_still_result(player)

    def _update_still_physics(self, dt):
        if self._still_heat_held:
            self._still_temp_vel = min(1.0, self._still_temp_vel + 0.018)
        else:
            self._still_temp_vel = max(-0.6, self._still_temp_vel - 0.010)
        self._still_temp = max(0.0, min(1.0, self._still_temp + self._still_temp_vel * dt))
        self._still_time += dt

        # Accumulate cut zone timers
        if self._still_cut1_done and not self._still_cut2_done:
            self._still_hearts_time += dt
        elif not self._still_cut1_done:
            self._still_heads_time += dt

        # Event flashes
        if 0.18 <= self._still_temp <= 0.22 and not self._still_foreshots_hit:
            self._still_foreshots_hit = True
            self._still_event_flash = ("Foreshots — cut approaching!", (255, 160, 60), 2.0)
        if 0.28 <= self._still_temp <= 0.33 and not self._still_hearts_hit:
            self._still_hearts_hit = True
            self._still_event_flash = ("HEARTS — make your cut!", (80, 235, 80), 2.5)
        if 0.68 <= self._still_temp <= 0.72 and not self._still_feints_hit:
            self._still_feints_hit = True
            self._still_event_flash = ("Feints approaching — stop hearts!", (255, 200, 60), 2.0)
        if self._still_event_flash:
            txt, col, timer = self._still_event_flash
            timer -= dt
            self._still_event_flash = (txt, col, timer) if timer > 0 else None

    def _draw_still_minigame(self, player):
        CX = SCREEN_W // 2
        # ---- Temperature bar (vertical still column) ----
        COL_X, COL_Y, COL_W, COL_H = CX - 250, 80, 40, 320
        pygame.draw.rect(self.screen, (40, 35, 20), (COL_X, COL_Y, COL_W, COL_H))
        pygame.draw.rect(self.screen, (140, 100, 40), (COL_X, COL_Y, COL_W, COL_H), 2)
        fill_h = int(COL_H * self._still_temp)
        if fill_h > 0:
            col = (
                int(80 + self._still_temp * 160),
                int(220 - self._still_temp * 180),
                40,
            )
            pygame.draw.rect(self.screen, col, (COL_X, COL_Y + COL_H - fill_h, COL_W, fill_h))
        # Zone markers on column
        for frac, label, clr in [(0.25, "FORESHOTS", (220, 140, 60)),
                                  (0.30, "HEARTS", (80, 220, 80)),
                                  (0.70, "FEINTS", (220, 200, 60))]:
            my = COL_Y + COL_H - int(COL_H * frac)
            pygame.draw.line(self.screen, clr, (COL_X - 6, my), (COL_X + COL_W + 6, my), 2)
            ls = self.small.render(label, True, clr)
            self.screen.blit(ls, (COL_X + COL_W + 10, my - 7))
        ts = self.small.render("TEMP", True, (150, 120, 60))
        self.screen.blit(ts, (COL_X, COL_Y - 18))

        # ---- Cut phase display ----
        phase_txt = (
            "Phase: HEADS (collecting impurities)" if not self._still_cut1_done else
            "Phase: HEARTS (collecting spirit)"    if not self._still_cut2_done else
            "Phase: TAILS (stop collection)"
        )
        ph_col = (220, 120, 60) if not self._still_cut1_done else (80, 220, 80) if not self._still_cut2_done else (220, 200, 60)
        ps = self.font.render(phase_txt, True, ph_col)
        self.screen.blit(ps, (CX - ps.get_width() // 2, 52))

        # ---- Cut buttons ----
        if not self._still_cut1_done:
            self._still_cut1_btn = pygame.Rect(CX - 120, 420, 240, 42)
            pygame.draw.rect(self.screen, (50, 40, 18), self._still_cut1_btn)
            pygame.draw.rect(self.screen, (200, 150, 60), self._still_cut1_btn, 2)
            b1s = self.font.render("MAKE HEADS CUT  [ENTER]", True, (240, 195, 80))
            self.screen.blit(b1s, (CX - b1s.get_width() // 2, 432))
        elif not self._still_cut2_done:
            self._still_cut2_btn = pygame.Rect(CX - 120, 420, 240, 42)
            pygame.draw.rect(self.screen, (22, 50, 22), self._still_cut2_btn)
            pygame.draw.rect(self.screen, (80, 220, 80), self._still_cut2_btn, 2)
            b2s = self.font.render("MAKE TAILS CUT  [ENTER]", True, (120, 240, 120))
            self.screen.blit(b2s, (CX - b2s.get_width() // 2, 432))
        else:
            self._still_finish_btn = pygame.Rect(CX - 100, 420, 200, 42)
            pygame.draw.rect(self.screen, (18, 40, 18), self._still_finish_btn)
            pygame.draw.rect(self.screen, (60, 180, 60), self._still_finish_btn, 2)
            fns = self.font.render("FINISH  [ENTER]", True, (100, 220, 100))
            self.screen.blit(fns, (CX - fns.get_width() // 2, 432))

        # SPACE hint
        hs = self.small.render("Hold SPACE to add heat", True, (120, 100, 60))
        self.screen.blit(hs, (CX - hs.get_width() // 2, 474))

        # Event flash
        if self._still_event_flash:
            txt, col, _ = self._still_event_flash
            fs = self.font.render(txt, True, col)
            self.screen.blit(fs, (CX - fs.get_width() // 2, SCREEN_H // 2 - 20))

        # Penalties
        if self._still_penalties > 0:
            pen = self.small.render(f"Impurity penalties: {self._still_penalties}", True, (220, 80, 60))
            self.screen.blit(pen, (10, SCREEN_H - 30))

    def _draw_still_result(self, player):
        spirit = self._still_result_spirit
        if spirit is None:
            return
        CX = SCREEN_W // 2
        rs = self.font.render("DISTILLATION COMPLETE", True, (80, 220, 120))
        self.screen.blit(rs, (CX - rs.get_width() // 2, 40))

        sc = SPIRIT_TYPE_COLORS.get(spirit.spirit_type, (200, 180, 120))
        bm = BIOME_DISPLAY_NAMES.get(spirit.origin_biome, spirit.origin_biome)
        ns = self.font.render(f"{bm} {spirit.spirit_type.title()}", True, sc)
        self.screen.blit(ns, (CX - ns.get_width() // 2, 80))

        qbar_x = CX - 150
        for label, val, col, y in [
            ("Cut Quality", spirit.cut_quality, (120, 220, 120), 120),
            ("Proof",       spirit.proof,       (180, 150, 80),  148),
            ("Smoothness",  spirit.smoothness,  (200, 200, 240), 176),
        ]:
            ls = self.small.render(label, True, (160, 140, 80))
            self.screen.blit(ls, (qbar_x, y))
            pygame.draw.rect(self.screen, (40, 35, 20), (qbar_x + 100, y + 1, 200, 14))
            pygame.draw.rect(self.screen, col, (qbar_x + 100, y + 1, int(200 * val), 14))

        note_y = 214
        nts = self.small.render("Notes: " + ", ".join(spirit.flavor_notes), True, (170, 150, 100))
        self.screen.blit(nts, (CX - nts.get_width() // 2, note_y))

        hint = self.small.render("Ready for barrel aging — take it to the Barrel Room.", True, (140, 120, 60))
        self.screen.blit(hint, (CX - hint.get_width() // 2, note_y + 22))

        self._still_result_done_btn = pygame.Rect(CX - 80, SCREEN_H - 70, 160, 38)
        pygame.draw.rect(self.screen, (28, 48, 28), self._still_result_done_btn)
        pygame.draw.rect(self.screen, (80, 200, 80), self._still_result_done_btn, 2)
        ds = self.font.render("Done", True, (130, 220, 130))
        self.screen.blit(ds, (CX - ds.get_width() // 2, SCREEN_H - 62))

    def handle_still_keydown(self, key, player):
        import pygame as _pg
        if key in (_pg.K_RETURN, _pg.K_KP_ENTER):
            if self._still_phase == "distilling":
                if not self._still_cut1_done:
                    self._still_cut1_done = True
                    if self._still_temp < 0.28 or self._still_temp > 0.38:
                        self._still_penalties += 1
                elif not self._still_cut2_done:
                    self._still_cut2_done = True
                    if self._still_temp < 0.60 or self._still_temp > 0.78:
                        self._still_penalties += 1
                else:
                    self._finish_distillation(player)

    def handle_still_keys(self, keys):
        import pygame as _pg
        self._still_heat_held = keys[_pg.K_SPACE]

    def _finish_distillation(self, player):
        idx = self._still_spirit_idx
        if idx is None or idx >= len(player.spirits):
            return
        spirit = player.spirits[idx]
        total = self._still_heads_time + self._still_hearts_time + self._still_tails_time
        apply_distillation_result(
            spirit,
            self._still_heads_time,
            self._still_hearts_time,
            self._still_tails_time,
            max(total, 0.1),
            self._still_penalties,
        )
        self._still_result_spirit = spirit
        self._still_phase = "result"

    def _handle_still_click(self, pos, player):
        if self._still_phase == "select_spirit":
            for idx, rect in self._still_select_rects.items():
                if rect.collidepoint(pos):
                    self._still_spirit_idx   = idx
                    self._still_phase        = "distilling"
                    self._still_time         = 0.0
                    self._still_temp         = 0.0
                    self._still_temp_vel     = 0.0
                    self._still_heat_held    = False
                    self._still_heads_time   = 0.0
                    self._still_hearts_time  = 0.0
                    self._still_tails_time   = 0.0
                    self._still_cut1_done    = False
                    self._still_cut2_done    = False
                    self._still_foreshots_hit = False
                    self._still_hearts_hit   = False
                    self._still_feints_hit   = False
                    self._still_event_flash  = None
                    self._still_penalties    = 0
                    return

        elif self._still_phase == "distilling":
            if self._still_cut1_btn and self._still_cut1_btn.collidepoint(pos):
                self.handle_still_keydown(__import__("pygame").K_RETURN, player)
            elif self._still_cut2_btn and self._still_cut2_btn.collidepoint(pos):
                self.handle_still_keydown(__import__("pygame").K_RETURN, player)
            elif self._still_finish_btn and self._still_finish_btn.collidepoint(pos):
                self._finish_distillation(player)

        elif self._still_phase == "result":
            if self._still_result_done_btn and self._still_result_done_btn.collidepoint(pos):
                self._still_phase = "select_spirit"
                self._still_result_spirit = None

    # ------------------------------------------------------------------ #
    #  Barrel Room  (aging — select distilled spirit, choose barrel/time) #
    # ------------------------------------------------------------------ #

    def _draw_barrel_room(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("BARREL ROOM", True, (175, 130, 65))
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, (100, 80, 50))
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        if self._barrel_phase == "aging":
            self._draw_barrel_aging(player, dt)
            return
        if self._barrel_phase == "result":
            self._draw_barrel_result(player)
            return

        CX = SCREEN_W // 2
        distilled = [(i, s) for i, s in enumerate(player.spirits) if s.state == "distilled"]
        if not distilled:
            msg = self.font.render("No distilled spirits! Use the Copper Still first.", True, (130, 100, 60))
            self.screen.blit(msg, (CX - msg.get_width() // 2, SCREEN_H // 2))
            return

        sub = self.small.render("Select a distilled spirit to age:", True, (170, 130, 60))
        self.screen.blit(sub, (CX - sub.get_width() // 2, 30))

        # Spirit list (left column)
        self._barrel_select_rects.clear()
        LIST_X, LIST_Y, LIST_W, LIST_H = 30, 54, 260, 52
        for li, (si, spirit) in enumerate(distilled[:8]):
            ry = LIST_Y + li * (LIST_H + 4)
            rect = pygame.Rect(LIST_X, ry, LIST_W, LIST_H)
            self._barrel_select_rects[si] = rect
            is_sel = (si == self._barrel_spirit_idx)
            pygame.draw.rect(self.screen, (48, 35, 15) if is_sel else (30, 22, 10), rect)
            pygame.draw.rect(self.screen, (175, 130, 55) if is_sel else (100, 75, 35), rect, 2 if is_sel else 1)
            bm = BIOME_DISPLAY_NAMES.get(spirit.origin_biome, spirit.origin_biome)
            ns = self.small.render(f"{bm} {spirit.spirit_type.title()}", True, (220, 180, 80) if is_sel else (160, 130, 60))
            self.screen.blit(ns, (LIST_X + 6, ry + 8))
            qs = self.small.render(f"Cut: {spirit.cut_quality:.0%}", True, (150, 120, 55) if is_sel else (100, 80, 40))
            self.screen.blit(qs, (LIST_X + 6, ry + 26))

        # Barrel type buttons (middle)
        self._barrel_type_rects.clear()
        BTN_X, BTN_Y, BTN_W, BTN_H = 320, 54, 280, 68
        btype_lbl = self.small.render("BARREL TYPE", True, (170, 130, 60))
        self.screen.blit(btype_lbl, (BTN_X, BTN_Y - 18))
        for bi, (bkey, bdata) in enumerate(BARREL_TYPES.items()):
            ry = BTN_Y + bi * (BTN_H + 6)
            rect = pygame.Rect(BTN_X, ry, BTN_W, BTN_H)
            self._barrel_type_rects[bkey] = rect
            is_sel = (bkey == self._barrel_type_sel)
            pygame.draw.rect(self.screen, (48, 35, 14) if is_sel else (28, 20, 8), rect)
            pygame.draw.rect(self.screen, (175, 130, 50) if is_sel else (100, 70, 30), rect, 2 if is_sel else 1)
            ls = self.small.render(bdata["label"], True, (230, 185, 80) if is_sel else (160, 120, 50))
            self.screen.blit(ls, (BTN_X + 6, ry + 6))
            ds = self.small.render(bdata["desc"], True, (140, 110, 55) if is_sel else (90, 70, 35))
            self.screen.blit(ds, (BTN_X + 6, ry + 24))

        # Age duration buttons (right)
        self._barrel_duration_rects.clear()
        DUR_X, DUR_Y, DUR_W, DUR_H = 630, 54, 220, 68
        dur_lbl = self.small.render("AGING TIME", True, (170, 130, 60))
        self.screen.blit(dur_lbl, (DUR_X, DUR_Y - 18))
        for di, (dkey, ddata) in enumerate(AGE_DURATIONS.items()):
            ry = DUR_Y + di * (DUR_H + 6)
            rect = pygame.Rect(DUR_X, ry, DUR_W, DUR_H)
            self._barrel_duration_rects[dkey] = rect
            is_sel = (dkey == self._barrel_duration_sel)
            pygame.draw.rect(self.screen, (48, 35, 14) if is_sel else (28, 20, 8), rect)
            pygame.draw.rect(self.screen, (175, 130, 50) if is_sel else (100, 70, 30), rect, 2 if is_sel else 1)
            ls = self.small.render(ddata["label"], True, (230, 185, 80) if is_sel else (160, 120, 50))
            self.screen.blit(ls, (DUR_X + 6, ry + 24))

        # Age button
        can_age = (self._barrel_spirit_idx is not None
                   and self._barrel_spirit_idx < len(player.spirits)
                   and self._barrel_type_sel is not None
                   and self._barrel_duration_sel is not None)
        self._barrel_age_btn = pygame.Rect(SCREEN_W // 2 - 100, SCREEN_H - 70, 200, 40)
        bc = (30, 50, 22) if can_age else (28, 28, 28)
        bbc = (100, 200, 60) if can_age else (60, 60, 60)
        pygame.draw.rect(self.screen, bc, self._barrel_age_btn)
        pygame.draw.rect(self.screen, bbc, self._barrel_age_btn, 2)
        age_lbl = self.font.render("AGE SPIRIT", True, (140, 220, 80) if can_age else (80, 80, 80))
        self.screen.blit(age_lbl, (SCREEN_W // 2 - age_lbl.get_width() // 2, SCREEN_H - 62))

    def _draw_barrel_aging(self, player, dt):
        si = self._barrel_spirit_idx
        if si is None or si >= len(player.spirits):
            self._barrel_phase = "select"
            return
        spirit = player.spirits[si]

        duration_secs = _BARREL_AGE_TIMES.get(self._barrel_duration_sel, 24.0)
        if not self._barrel_age_done:
            self._barrel_age_progress = min(1.0, self._barrel_age_progress + dt / duration_secs)
            self._barrel_age_care_timer -= dt
            if self._barrel_age_care_timer <= 0 and not self._barrel_age_care_active:
                self._barrel_age_care_active = True
                self._barrel_age_care_window = 4.0
            if self._barrel_age_care_active:
                self._barrel_age_care_window -= dt
                if self._barrel_age_care_window <= 0:
                    self._barrel_age_care_active = False
                    self._barrel_age_care_timer = max(5.0, duration_secs / 3)
            if self._barrel_age_progress >= 1.0:
                self._barrel_age_done = True

        CX = SCREEN_W // 2
        col = SPIRIT_TYPE_COLORS.get(spirit.spirit_type, (180, 140, 60))
        bm = BIOME_DISPLAY_NAMES.get(spirit.origin_biome, spirit.origin_biome)
        tl = self.font.render(f"Aging  {bm} {spirit.spirit_type.title()}", True, col)
        self.screen.blit(tl, (CX - tl.get_width() // 2, SCREEN_H // 2 - 80))
        bl_lbl = self.small.render(
            f"Barrel: {BARREL_TYPES.get(self._barrel_type_sel, {}).get('label', self._barrel_type_sel)}  —  "
            f"{AGE_DURATIONS.get(self._barrel_duration_sel, {}).get('label', self._barrel_duration_sel)}",
            True, (175, 145, 80))
        self.screen.blit(bl_lbl, (CX - bl_lbl.get_width() // 2, SCREEN_H // 2 - 55))

        bar_w = 400
        bar_x = CX - bar_w // 2
        bar_y = SCREEN_H // 2 - 10
        pygame.draw.rect(self.screen, (20, 15, 8), (bar_x, bar_y, bar_w, 30))
        pygame.draw.rect(self.screen, col, (bar_x, bar_y, int(bar_w * self._barrel_age_progress), 30))
        pygame.draw.rect(self.screen, (160, 130, 55), (bar_x, bar_y, bar_w, 30), 2)
        pct = int(self._barrel_age_progress * 100)
        pl = self.small.render(f"Aging: {pct}%", True, (190, 160, 80))
        self.screen.blit(pl, (CX - pl.get_width() // 2, SCREEN_H // 2 + 30))
        bonus_pct = int(self._barrel_age_care_bonus * 100)
        bl2 = self.small.render(f"Care bonus: +{bonus_pct}%", True, (160, 135, 65))
        self.screen.blit(bl2, (CX - bl2.get_width() // 2, SCREEN_H // 2 + 50))

        if self._barrel_age_care_active:
            flash = int(self._barrel_age_care_window * 4) % 2 == 0
            c_color = (100, 220, 100) if flash else (60, 160, 60)
            care_msg = self.font.render("PRESS W — Sample the cask!", True, c_color)
            self.screen.blit(care_msg, (CX - care_msg.get_width() // 2, SCREEN_H // 2 - 120))

        if self._barrel_age_done:
            self._finish_barrel_aging(player)

    def _finish_barrel_aging(self, player):
        si = self._barrel_spirit_idx
        if si is None or si >= len(player.spirits):
            self._barrel_phase = "select"
            return
        spirit = player.spirits[si]
        apply_barrel_aging(spirit, self._barrel_type_sel, self._barrel_duration_sel)
        spirit.age_quality = min(1.0, spirit.age_quality + self._barrel_age_care_bonus * 0.10)
        self._barrel_phase = "result"
        self._barrel_spirit_idx = None

    def _draw_barrel_result(self, player):
        CX = SCREEN_W // 2
        msg = self.font.render("Spirit Aged!", True, (220, 185, 80))
        self.screen.blit(msg, (CX - msg.get_width() // 2, SCREEN_H // 2 - 40))
        hint = self.small.render("Ready to bottle at the Bottling Station", True, (160, 130, 55))
        self.screen.blit(hint, (CX - hint.get_width() // 2, SCREEN_H // 2))
        ok = self.small.render("Click anywhere to continue", True, (140, 110, 50))
        self.screen.blit(ok, (CX - ok.get_width() // 2, SCREEN_H // 2 + 35))

    def handle_barrel_age_keydown(self, key):
        if self._barrel_phase != "aging":
            return
        if key == pygame.K_w and self._barrel_age_care_active:
            self._barrel_age_care_bonus = min(1.0, self._barrel_age_care_bonus + 0.12)
            self._barrel_age_care_active = False
            duration_secs = _BARREL_AGE_TIMES.get(self._barrel_duration_sel, 24.0)
            self._barrel_age_care_timer = max(5.0, duration_secs / 3)

    def _handle_barrel_room_click(self, pos, player):
        if self._barrel_phase == "result":
            self._barrel_phase = "select"
            self._barrel_age_progress = 0.0
            self._barrel_age_care_bonus = 0.0
            self._barrel_age_done = False
            return
        if self._barrel_phase == "aging":
            return
        for idx, rect in self._barrel_select_rects.items():
            if rect.collidepoint(pos):
                self._barrel_spirit_idx = idx
                return
        for bkey, rect in self._barrel_type_rects.items():
            if rect.collidepoint(pos):
                self._barrel_type_sel = bkey
                return
        for dkey, rect in self._barrel_duration_rects.items():
            if rect.collidepoint(pos):
                self._barrel_duration_sel = dkey
                return
        if (self._barrel_age_btn and self._barrel_age_btn.collidepoint(pos)
                and self._barrel_spirit_idx is not None
                and self._barrel_spirit_idx < len(player.spirits)
                and self._barrel_type_sel and self._barrel_duration_sel):
            duration_secs = _BARREL_AGE_TIMES.get(self._barrel_duration_sel, 24.0)
            self._barrel_phase = "aging"
            self._barrel_age_progress = 0.0
            self._barrel_age_care_active = False
            self._barrel_age_care_window = 0.0
            self._barrel_age_care_timer = max(4.0, duration_secs / 3)
            self._barrel_age_care_bonus = 0.0
            self._barrel_age_done = False

    # ------------------------------------------------------------------ #
    #  Bottling Station  (blend + bottle aged spirits)                    #
    # ------------------------------------------------------------------ #

    def _draw_bottling_station(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("BOTTLING STATION", True, (175, 160, 100))
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, (110, 95, 65))
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        CX = SCREEN_W // 2

        if self._bottle_phase == "select":
            self._bottle_select_rects.clear()
            aged = [(i, s) for i, s in enumerate(player.spirits)
                    if s.state in ("aged", "blended")]
            if not aged:
                msg = self.font.render("No aged spirits! Age in the Barrel Room first.", True, (130, 100, 60))
                self.screen.blit(msg, (CX - msg.get_width() // 2, SCREEN_H // 2))
                return

            sub = self.small.render("Select a spirit to bottle  (or fill 3 slots to blend first):", True, (170, 150, 80))
            self.screen.blit(sub, (CX - sub.get_width() // 2, 30))

            CELL_W, CELL_H, GAP, COLS = 210, 58, 8, 4
            gx0 = (SCREEN_W - (COLS * CELL_W + (COLS - 1) * GAP)) // 2
            for li, (si, spirit) in enumerate(aged[:16]):
                col_i = li % COLS
                row_i = li // COLS
                rx = gx0 + col_i * (CELL_W + GAP)
                ry = 55 + row_i * (CELL_H + GAP)
                rect = pygame.Rect(rx, ry, CELL_W, CELL_H)
                self._bottle_select_rects[si] = rect
                in_blend = si in self._bottle_blend_slots
                is_direct = (si == self._bottle_single_idx)
                bg = (42, 38, 18) if in_blend else (38, 28, 14) if is_direct else (25, 18, 8)
                br = (200, 180, 60) if in_blend else (175, 130, 50) if is_direct else (100, 75, 35)
                pygame.draw.rect(self.screen, bg, rect)
                pygame.draw.rect(self.screen, br, rect, 2 if (in_blend or is_direct) else 1)
                bm = BIOME_DISPLAY_NAMES.get(spirit.origin_biome, spirit.origin_biome)
                nm = self.small.render(f"{bm} {spirit.spirit_type.title()}", True, (220, 185, 80))
                self.screen.blit(nm, (rx + 6, ry + 8))
                ql = self.small.render(f"Aged: {spirit.age_quality:.0%}  {spirit.barrel_type.replace('_',' ')}", True, (150, 125, 55))
                self.screen.blit(ql, (rx + 6, ry + 28))
                tag = self.small.render("[B]lend slot" if in_blend else "[Single]" if is_direct else "click to select", True, (120, 100, 50))
                self.screen.blit(tag, (rx + 6, ry + 46))

            # Blend slots display
            blend_y = SCREEN_H - 160
            blend_lbl = self.small.render("BLEND SLOTS (up to 3):", True, (160, 140, 70))
            self.screen.blit(blend_lbl, (CX - 200, blend_y))
            for bi in range(3):
                sx = CX - 150 + bi * 100
                sr = pygame.Rect(sx, blend_y + 18, 88, 32)
                if bi < len(self._bottle_blend_slots):
                    si = self._bottle_blend_slots[bi]
                    if si < len(player.spirits):
                        s = player.spirits[si]
                        bm2 = BIOME_DISPLAY_NAMES.get(s.origin_biome, s.origin_biome)[:7]
                        pygame.draw.rect(self.screen, (45, 38, 18), sr)
                        pygame.draw.rect(self.screen, (180, 150, 60), sr, 2)
                        ts2 = self.small.render(bm2, True, (200, 170, 70))
                        self.screen.blit(ts2, (sx + 4, blend_y + 20))
                else:
                    pygame.draw.rect(self.screen, (25, 20, 10), sr)
                    pygame.draw.rect(self.screen, (80, 65, 30), sr, 1)
                    es = self.small.render("empty", True, (80, 65, 30))
                    self.screen.blit(es, (sx + 4, blend_y + 20))

            # Action buttons
            can_bottle_single = (self._bottle_single_idx is not None
                                 and self._bottle_single_idx < len(player.spirits))
            can_bottle_blend  = len(self._bottle_blend_slots) >= 2

            bx0 = CX - 220
            self._bottle_single_btn = pygame.Rect(bx0, SCREEN_H - 60, 200, 40)
            sc2 = (28, 48, 22) if can_bottle_single else (25, 25, 25)
            sb2 = (80, 200, 60) if can_bottle_single else (55, 55, 55)
            pygame.draw.rect(self.screen, sc2, self._bottle_single_btn)
            pygame.draw.rect(self.screen, sb2, self._bottle_single_btn, 2)
            s1l = self.font.render("BOTTLE SINGLE", True, (120, 210, 80) if can_bottle_single else (70, 70, 70))
            self.screen.blit(s1l, (bx0 + 100 - s1l.get_width() // 2, SCREEN_H - 52))

            bx1 = CX + 20
            self._bottle_blend_btn = pygame.Rect(bx1, SCREEN_H - 60, 200, 40)
            bc2 = (28, 28, 48) if can_bottle_blend else (25, 25, 25)
            bb2 = (80, 80, 200) if can_bottle_blend else (55, 55, 55)
            pygame.draw.rect(self.screen, bc2, self._bottle_blend_btn)
            pygame.draw.rect(self.screen, bb2, self._bottle_blend_btn, 2)
            bl2 = self.font.render("BOTTLE BLEND", True, (120, 120, 220) if can_bottle_blend else (70, 70, 70))
            self.screen.blit(bl2, (bx1 + 100 - bl2.get_width() // 2, SCREEN_H - 52))

        elif self._bottle_phase == "result":
            self._draw_bottle_result(player)

    def _draw_bottle_result(self, player):
        out_id = self._bottle_result_id
        spirit = self._bottle_result_spirit
        if out_id is None or spirit is None:
            return
        from items import ITEMS
        item = ITEMS.get(out_id, {})
        CX = SCREEN_W // 2
        rs = self.font.render("BOTTLED!", True, (200, 220, 160))
        self.screen.blit(rs, (CX - rs.get_width() // 2, 40))
        nm = self.font.render(item.get("name", out_id), True, item.get("color", (200, 180, 120)))
        self.screen.blit(nm, (CX - nm.get_width() // 2, 80))

        bm = BIOME_DISPLAY_NAMES.get(spirit.origin_biome, spirit.origin_biome)
        desc = SPIRIT_TYPE_DESCS.get(spirit.spirit_type, "")
        ds = self.small.render(desc, True, (170, 155, 100))
        self.screen.blit(ds, (CX - ds.get_width() // 2, 112))

        buff_key = SPIRIT_BUFFS.get(spirit.spirit_type)
        if buff_key:
            bs = self.small.render(f"Buff: {BUFF_DESCS.get(buff_key, buff_key)}", True, (140, 200, 140))
            self.screen.blit(bs, (CX - bs.get_width() // 2, 136))

        nts = self.small.render("Notes: " + ", ".join(spirit.flavor_notes), True, (160, 145, 90))
        self.screen.blit(nts, (CX - nts.get_width() // 2, 162))

        self._bottle_result_done_btn = pygame.Rect(CX - 80, SCREEN_H - 70, 160, 38)
        pygame.draw.rect(self.screen, (28, 48, 28), self._bottle_result_done_btn)
        pygame.draw.rect(self.screen, (80, 200, 80), self._bottle_result_done_btn, 2)
        dls = self.font.render("Done", True, (130, 220, 130))
        self.screen.blit(dls, (CX - dls.get_width() // 2, SCREEN_H - 62))

    def _handle_bottling_click(self, pos, player):
        if self._bottle_phase == "select":
            for idx, rect in self._bottle_select_rects.items():
                if rect.collidepoint(pos):
                    # Toggle blend slot vs single select
                    if idx in self._bottle_blend_slots:
                        self._bottle_blend_slots.remove(idx)
                    elif len(self._bottle_blend_slots) < 3:
                        self._bottle_blend_slots.append(idx)
                        self._bottle_single_idx = None
                    else:
                        self._bottle_single_idx = idx
                    return
            if self._bottle_single_btn and self._bottle_single_btn.collidepoint(pos):
                self._do_bottle_single(player)
                return
            if self._bottle_blend_btn and self._bottle_blend_btn.collidepoint(pos):
                self._do_bottle_blend(player)
                return
        elif self._bottle_phase == "result":
            if self._bottle_result_done_btn and self._bottle_result_done_btn.collidepoint(pos):
                self._bottle_phase = "select"
                self._bottle_result_id = None
                self._bottle_result_spirit = None
                self._bottle_blend_slots.clear()
                self._bottle_single_idx = None

    def _do_bottle_single(self, player):
        idx = self._bottle_single_idx
        if idx is None or idx >= len(player.spirits):
            return
        spirit = player.spirits[idx]
        quality = max(spirit.cut_quality, spirit.age_quality)
        out_id = get_bottle_output_id(spirit.spirit_type, quality)
        player._add_item(out_id)
        tier = "reserve" if quality >= 0.70 else "aged" if quality >= 0.40 else "young"
        player.discovered_spirit_types.add(f"{spirit.origin_biome}_{tier}")
        self._apply_spirit_buff(player, spirit)
        del player.spirits[idx]
        self._bottle_result_id = out_id
        self._bottle_result_spirit = spirit
        self._bottle_phase = "result"
        self._bottle_single_idx = None

    def _do_bottle_blend(self, player):
        slots = self._bottle_blend_slots
        if len(slots) < 2:
            return
        components = [player.spirits[i] for i in slots if i < len(player.spirits)]
        if len(components) < 2:
            return
        blended = make_blend(components)
        quality = max(blended.cut_quality, blended.age_quality)
        out_id = get_bottle_output_id(blended.spirit_type, quality)
        player._add_item(out_id)
        tier = "reserve" if quality >= 0.70 else "aged" if quality >= 0.40 else "young"
        player.discovered_spirit_types.add(f"blend_{tier}")
        self._apply_spirit_buff(player, blended)
        for i in sorted(slots, reverse=True):
            if i < len(player.spirits):
                del player.spirits[i]
        self._bottle_result_id = out_id
        self._bottle_result_spirit = blended
        self._bottle_phase = "result"
        self._bottle_blend_slots.clear()

    def _apply_spirit_buff(self, player, spirit):
        buff_key = SPIRIT_BUFFS.get(spirit.spirit_type)
        if not buff_key:
            return
        from items import ITEMS
        # Duration comes from the bottled item; we use the quality-tier version if available
        quality = max(spirit.cut_quality, spirit.age_quality)
        tier = "_reserve" if quality >= 0.70 else "_aged" if quality >= 0.40 else ""
        item_id = f"{spirit.spirit_type}{tier}"
        item = ITEMS.get(item_id, {})
        duration = item.get("spirit_buff_duration", 120.0)
        if hasattr(player, "spirit_buffs"):
            player.spirit_buffs[buff_key] = {"duration": duration}

    # ------------------------------------------------------------------ #
    #  Spirits codex  (drawn by collections.py, but helper lives here)    #
    # ------------------------------------------------------------------ #

    def _draw_spirits_codex(self, player, gy0=58, gx_off=0):
        from spirits import SPIRIT_TYPE_ORDER, BIOME_SPIRIT_PROFILES, BIOME_DISPLAY_NAMES as BDN
        import pygame as _pg

        CX = (gx_off + SCREEN_W) // 2
        CELL_W, CELL_H = 110, 36
        GAP = 4
        COLS = 6  # young / aged / reserve × 2 spirit types per row, wrap as needed

        tiers = ["young", "aged", "reserve"]
        tier_colors = {
            "young":   (160, 130,  60),
            "aged":    (185, 150,  80),
            "reserve": (220, 185, 100),
        }

        biomes = list(BIOME_SPIRIT_PROFILES.keys())
        row_count = len(biomes)
        total_h = row_count * (CELL_H + GAP)

        # Scrollable grid: biome rows × 3 tier columns
        GRID_W = 3 * (CELL_W + GAP) - GAP
        gx0 = CX - GRID_W // 2
        self._spirits_codex_rects = {}

        for ri, biome in enumerate(biomes):
            ry = gy0 + ri * (CELL_H + GAP) - self._spirits_codex_scroll
            if ry + CELL_H < gy0 or ry > SCREEN_H:
                continue
            bm_lbl = self.small.render(BDN.get(biome, biome), True, (160, 140, 80))
            self.screen.blit(bm_lbl, (gx0 - bm_lbl.get_width() - 8, ry + CELL_H // 2 - bm_lbl.get_height() // 2))
            for ci, tier in enumerate(tiers):
                key = f"{biome}_{tier}"
                discovered = key in player.discovered_spirit_types
                rx = gx0 + ci * (CELL_W + GAP)
                rect = _pg.Rect(rx, ry, CELL_W, CELL_H)
                self._spirits_codex_rects[key] = rect
                is_sel = (key == self._spirits_codex_selected)
                if discovered:
                    col = tier_colors[tier]
                    bg = (int(col[0] * 0.22), int(col[1] * 0.18), int(col[2] * 0.08))
                    border = col if is_sel else (int(col[0] * 0.7), int(col[1] * 0.7), int(col[2] * 0.4))
                else:
                    bg = (22, 18, 10)
                    border = (50, 42, 22) if is_sel else (38, 30, 14)
                _pg.draw.rect(self.screen, bg, rect)
                _pg.draw.rect(self.screen, border, rect, 2 if (is_sel or discovered) else 1)
                label = tier.title() if discovered else "???"
                ls = self.small.render(label, True, tier_colors[tier] if discovered else (60, 50, 28))
                self.screen.blit(ls, (rx + CELL_W // 2 - ls.get_width() // 2,
                                      ry + CELL_H // 2 - ls.get_height() // 2))

        # Column headers
        for ci, tier in enumerate(tiers):
            rx = gx0 + ci * (CELL_W + GAP)
            hs = self.small.render(tier.upper(), True, tier_colors[tier])
            self.screen.blit(hs, (rx + CELL_W // 2 - hs.get_width() // 2, gy0 - 16))

        self._max_spirits_codex_scroll = max(0, total_h - (SCREEN_H - gy0 - 20))

        # Detail panel for selected entry
        if self._spirits_codex_selected:
            biome, tier = self._spirits_codex_selected.rsplit("_", 1)
            if self._spirits_codex_selected in player.discovered_spirit_types:
                profile = BIOME_SPIRIT_PROFILES.get(biome, {})
                stype = profile.get("spirit_type", "?")
                PX = gx0 + GRID_W + 20
                PW = SCREEN_W - PX - 10
                bm_full = BDN.get(biome, biome)
                nms = self.font.render(f"{bm_full} {stype.title()} ({tier.title()})", True, (215, 185, 100))
                self.screen.blit(nms, (PX, gy0))
                desc = SPIRIT_TYPE_DESCS.get(stype, "")
                ds = self.small.render(desc, True, (170, 150, 90))
                self.screen.blit(ds, (PX, gy0 + 24))
                buff = SPIRIT_BUFFS.get(stype)
                if buff:
                    bs = self.small.render(f"Buff: {BUFF_DESCS.get(buff, buff)}", True, (140, 200, 140))
                    self.screen.blit(bs, (PX, gy0 + 44))
