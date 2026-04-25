import pygame
from constants import SCREEN_W, SCREEN_H
from salt import (
    apply_evap_method, apply_evap_result, apply_refine_grade,
    EVAP_METHODS, REFINE_GRADES, GRADES,
    OUTPUT_DESCS, OUTPUT_COLORS, BUFF_DESCS,
    BIOME_DISPLAY_NAMES, fleur_eligible,
)

_ACCENT  = (210, 200, 175)
_DARK_BG = ( 22,  20,  16)
_CELL_BG = ( 38,  34,  24)
_TITLE_C = (245, 240, 220)
_LABEL_C = (200, 190, 155)
_DIM_C   = ( 95,  88,  60)
_HINT_C  = (140, 130,  90)
_GREEN   = (100, 220, 110)
_YELLOW  = (220, 200,  80)
_RED     = (220,  80,  70)

_SWEET_LO  = 0.35
_SWEET_HI  = 0.65
_DANGER_HI = 0.85
_EVAP_DURATION = 30.0
_NUCLEATION_T  = 10.0
_HARVEST_T     = 22.0


class SaltMixin:

    # ─────────────────────────────────────────────────────────────────────────
    # EVAPORATION PAN
    # ─────────────────────────────────────────────────────────────────────────

    def _draw_evap_pan(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("EVAPORATION PAN", True, _TITLE_C)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, _HINT_C)
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        if self._evap_phase == "select_crystal":
            self._draw_evap_select(player)
        elif self._evap_phase == "select_method":
            self._draw_evap_method_select(player)
        elif self._evap_phase == "evaporating":
            self._draw_evap_minigame(player, dt)
        elif self._evap_phase == "result":
            self._draw_evap_result(player)

    def _draw_evap_select(self, player):
        self._evap_select_rects.clear()
        raw = [(i, c) for i, c in enumerate(player.salt_crystals) if c.state == "raw"]
        if not raw:
            msg = self.font.render("No raw salt! Mine Salt Deposits underground.", True, _LABEL_C)
            self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2))
            return
        sub = self.small.render("Select a salt crystal to evaporate:", True, _LABEL_C)
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 32))
        CELL_W, CELL_H, GAP, COLS = 210, 62, 10, 4
        gx0 = (SCREEN_W - (COLS * CELL_W + (COLS - 1) * GAP)) // 2
        for li, (bi, crystal) in enumerate(raw[:16]):
            col_i, row_i = li % COLS, li // COLS
            rx = gx0 + col_i * (CELL_W + GAP)
            ry = 55 + row_i * (CELL_H + GAP)
            rect = pygame.Rect(rx, ry, CELL_W, CELL_H)
            self._evap_select_rects[bi] = rect
            pygame.draw.rect(self.screen, _CELL_BG, rect)
            pygame.draw.rect(self.screen, _ACCENT, rect, 2)
            biome_nm = BIOME_DISPLAY_NAMES.get(crystal.origin_biome, crystal.origin_biome)
            nm = self.small.render(biome_nm, True, _TITLE_C)
            self.screen.blit(nm, (rx + 6, ry + 8))
            pur = self.small.render(f"Purity {int(crystal.purity * 100)}%  Moist {int(crystal.moisture * 100)}%", True, _HINT_C)
            self.screen.blit(pur, (rx + 6, ry + 30))
            var = self.small.render(crystal.variety.capitalize(), True, _DIM_C)
            self.screen.blit(var, (rx + CELL_W - var.get_width() - 6, ry + 8))

    def _draw_evap_method_select(self, player):
        self._evap_method_rects.clear()
        sub = self.small.render("Choose an evaporation method:", True, _LABEL_C)
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 32))
        methods = list(EVAP_METHODS.items())
        BTN_W, BTN_H, BTN_GAP = 240, 90, 14
        total_w = len(methods) * BTN_W + (len(methods) - 1) * BTN_GAP
        gx0 = (SCREEN_W - total_w) // 2
        for pi, (mk, md) in enumerate(methods):
            px = gx0 + pi * (BTN_W + BTN_GAP)
            py = SCREEN_H // 2 - BTN_H // 2
            prect = pygame.Rect(px, py, BTN_W, BTN_H)
            self._evap_method_rects[mk] = prect
            pygame.draw.rect(self.screen, _CELL_BG, prect)
            pygame.draw.rect(self.screen, _ACCENT, prect, 2)
            lbl = self.font.render(md["label"], True, _TITLE_C)
            self.screen.blit(lbl, (px + BTN_W // 2 - lbl.get_width() // 2, py + 10))
            desc_short = md["desc"].split(".")[0]
            dl = self.small.render(desc_short, True, _LABEL_C)
            self.screen.blit(dl, (px + BTN_W // 2 - dl.get_width() // 2, py + 38))
            if "variance_mult" in md:
                warn = self.small.render("High variance!", True, _YELLOW)
                self.screen.blit(warn, (px + BTN_W // 2 - warn.get_width() // 2, py + 64))

    def _draw_evap_minigame(self, player, dt):
        if not self._evap_game_done:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self._evap_temp = min(1.0, self._evap_temp + 0.55 * dt)
            else:
                self._evap_temp = max(0.0, self._evap_temp - 0.30 * dt)

            if _SWEET_LO <= self._evap_temp <= _SWEET_HI:
                self._evap_time_in_sweet += dt
            elif self._evap_temp > _DANGER_HI:
                self._evap_overheat_accum += dt
                while self._evap_overheat_accum >= 1.5:
                    self._evap_overheat_penalty += 1
                    self._evap_overheat_accum -= 1.5

            self._evap_time += dt

            # Milestone events
            if not self._evap_crystallize_hit and self._evap_time >= _NUCLEATION_T:
                self._evap_crystallize_hit = True
                self._evap_event_flash = ("NUCLEATION STAGE", _GREEN, 2.5)
            if not self._evap_harvest_hit and self._evap_time >= _HARVEST_T:
                self._evap_harvest_hit = True
                self._evap_event_flash = ("HARVEST WINDOW!", _YELLOW, 2.5)

            if self._evap_event_flash:
                txt, col, timer = self._evap_event_flash
                timer -= dt
                if timer <= 0:
                    self._evap_event_flash = None
                else:
                    self._evap_event_flash = (txt, col, timer)

            if self._evap_time >= _EVAP_DURATION:
                self._evap_game_done = True

        cx, cy = SCREEN_W // 2, SCREEN_H // 2

        # Left: vertical temperature gauge
        gx, gy, gw, gh = cx - 260, cy - 100, 30, 200
        pygame.draw.rect(self.screen, _CELL_BG, (gx, gy, gw, gh))
        fill_h = int(gh * self._evap_temp)
        tc = (
            _RED    if self._evap_temp > _DANGER_HI else
            _YELLOW if self._evap_temp > _SWEET_HI  else
            _GREEN  if self._evap_temp >= _SWEET_LO  else
            (100, 150, 200)
        )
        pygame.draw.rect(self.screen, tc, (gx, gy + gh - fill_h, gw, fill_h))
        pygame.draw.rect(self.screen, _ACCENT, (gx, gy, gw, gh), 2)
        # Sweet zone band
        sweet_y0 = gy + gh - int(gh * _SWEET_HI)
        sweet_y1 = gy + gh - int(gh * _SWEET_LO)
        for band_y in range(sweet_y0, sweet_y1):
            pygame.draw.line(self.screen, (100, 220, 110, 40), (gx, band_y), (gx + gw, band_y))
        pygame.draw.line(self.screen, _GREEN, (gx - 4, sweet_y0), (gx + gw + 4, sweet_y0))
        pygame.draw.line(self.screen, _GREEN, (gx - 4, sweet_y1), (gx + gw + 4, sweet_y1))
        gl = self.small.render("HEAT", True, _LABEL_C)
        self.screen.blit(gl, (gx, gy - 18))
        pct_l = self.small.render(f"{int(self._evap_temp * 100)}%", True, tc)
        self.screen.blit(pct_l, (gx, gy + gh + 4))

        # Centre: time progress bar
        bar_w = 320
        bar_x = cx - bar_w // 2
        bar_y = cy + 80
        frac = min(1.0, self._evap_time / _EVAP_DURATION)
        pygame.draw.rect(self.screen, _CELL_BG, (bar_x, bar_y, bar_w, 16))
        pygame.draw.rect(self.screen, _DIM_C,   (bar_x, bar_y, int(bar_w * frac), 16))
        pygame.draw.rect(self.screen, _ACCENT,  (bar_x, bar_y, bar_w, 16), 1)
        # Milestone ticks
        for tick_t, tick_lbl in ((_NUCLEATION_T, "Nucleation"), (_HARVEST_T, "Harvest")):
            tx = bar_x + int(bar_w * tick_t / _EVAP_DURATION)
            pygame.draw.line(self.screen, _YELLOW, (tx, bar_y - 6), (tx, bar_y + 22))
            tl = self.small.render(tick_lbl, True, _HINT_C)
            self.screen.blit(tl, (tx - tl.get_width() // 2, bar_y + 24))
        time_left = max(0.0, _EVAP_DURATION - self._evap_time)
        tl = self.small.render(f"{time_left:.1f}s remaining", True, _LABEL_C)
        self.screen.blit(tl, (cx - tl.get_width() // 2, bar_y - 22))

        # Right: crystal preview shape
        crx, cry = cx + 180, cy - 20
        purity_now = getattr(self._evap_current_crystal, "purity", 0.5)
        cbase = int(215 + purity_now * 40)
        warm  = (220, 80, 60) if self._evap_temp > _DANGER_HI else (cbase, cbase, cbase - 15)
        crystal_pts = [
            (crx, cry - 40), (crx + 28, cry - 10), (crx + 28, cry + 20),
            (crx, cry + 40), (crx - 28, cry + 20), (crx - 28, cry - 10),
        ]
        pygame.draw.polygon(self.screen, warm, crystal_pts)
        pygame.draw.polygon(self.screen, _ACCENT, crystal_pts, 2)
        cr_lbl = self.small.render(f"Pur {int(purity_now * 100)}%", True, _LABEL_C)
        self.screen.blit(cr_lbl, (crx - cr_lbl.get_width() // 2, cry + 50))

        # Sweet-time score
        score_now = min(1.0, self._evap_time_in_sweet / max(0.1, self._evap_time)) if self._evap_time > 0 else 0
        sc = self.small.render(f"Sweet zone: {int(score_now * 100)}%", True, _DIM_C)
        self.screen.blit(sc, (cx - sc.get_width() // 2, cy + 115))

        # Controls
        kl = self.small.render("Hold SPACE — Apply Heat   |   ENTER — Stop & Harvest", True, _HINT_C)
        self.screen.blit(kl, (cx - kl.get_width() // 2, cy - 130))

        # Penalty warning
        if self._evap_overheat_penalty > 0:
            pw = self.small.render(f"Overheat penalties: {self._evap_overheat_penalty}", True, _RED)
            self.screen.blit(pw, (cx - pw.get_width() // 2, cy - 110))

        # Event flash
        if self._evap_event_flash:
            etxt, ecol, _ = self._evap_event_flash
            ef = self.font.render(etxt, True, ecol)
            self.screen.blit(ef, (cx - ef.get_width() // 2, cy - 80))

        if self._evap_game_done:
            self._finish_evap(player)

    def _draw_evap_result(self, player):
        if not self._evap_result_crystal:
            return
        c = self._evap_result_crystal
        cx = SCREEN_W // 2
        msg = self.font.render("Evaporation Complete!", True, _TITLE_C)
        self.screen.blit(msg, (cx - msg.get_width() // 2, SCREEN_H // 2 - 70))
        q = getattr(c, "_evap_quality", 0.0)
        q_col = _GREEN if q >= 0.7 else _YELLOW if q >= 0.4 else _RED
        ql = self.font.render(f"Quality: {int(q * 100)}%", True, q_col)
        self.screen.blit(ql, (cx - ql.get_width() // 2, SCREEN_H // 2 - 28))
        biome_nm = BIOME_DISPLAY_NAMES.get(c.origin_biome, c.origin_biome)
        bl = self.small.render(f"Origin: {biome_nm}  |  Method: {c.evap_method.replace('_', ' ').title()}", True, _LABEL_C)
        self.screen.blit(bl, (cx - bl.get_width() // 2, SCREEN_H // 2 + 12))
        note = self.small.render("Take it to the Salt Grinder to finish.", True, _HINT_C)
        self.screen.blit(note, (cx - note.get_width() // 2, SCREEN_H // 2 + 38))
        ok = self.small.render("Click anywhere to close", True, _DIM_C)
        self.screen.blit(ok, (cx - ok.get_width() // 2, SCREEN_H // 2 + 62))

    def _finish_evap(self, player):
        c = self._evap_current_crystal
        if c is None:
            return
        apply_evap_method(c, self._evap_selected_method)
        apply_evap_result(c, self._evap_time_in_sweet, self._evap_time, self._evap_overheat_penalty)
        self._evap_result_crystal = c
        self._evap_phase = "result"

    def _handle_evap_pan_click(self, pos, player):
        if self._evap_phase == "select_crystal":
            for bi, rect in self._evap_select_rects.items():
                if rect.collidepoint(pos):
                    self._evap_current_crystal = player.salt_crystals[bi]
                    self._evap_phase = "select_method"
                    return
        elif self._evap_phase == "select_method":
            for mk, rect in self._evap_method_rects.items():
                if rect.collidepoint(pos):
                    self._evap_selected_method = mk
                    self._evap_phase = "evaporating"
                    self._evap_temp = 0.0
                    self._evap_time = 0.0
                    self._evap_time_in_sweet = 0.0
                    self._evap_overheat_penalty = 0
                    self._evap_overheat_accum = 0.0
                    self._evap_crystallize_hit = False
                    self._evap_harvest_hit = False
                    self._evap_event_flash = None
                    self._evap_game_done = False
                    self._evap_result_crystal = None
                    return
        elif self._evap_phase == "result":
            self._evap_phase = "select_crystal"
            self._evap_result_crystal = None

    def handle_evap_pan_keydown(self, key, player):
        if self._evap_phase == "evaporating" and key == pygame.K_RETURN:
            self._evap_game_done = True

    def handle_evap_pan_keys(self, keys, dt, player):
        pass  # heat polling is done inline in _draw_evap_minigame via pygame.key.get_pressed()

    # ─────────────────────────────────────────────────────────────────────────
    # SALT GRINDER
    # ─────────────────────────────────────────────────────────────────────────

    def _draw_salt_grinder(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("SALT GRINDER", True, _TITLE_C)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, _HINT_C)
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        if self._grinder_phase == "select_crystal":
            self._draw_grinder_select(player)
        elif self._grinder_phase == "select_grade":
            self._draw_grinder_grade_select(player)
        elif self._grinder_phase == "result":
            self._draw_grinder_result(player)

    def _draw_grinder_select(self, player):
        self._grinder_select_rects.clear()
        dried = [(i, c) for i, c in enumerate(player.salt_crystals) if c.state == "dried"]
        if not dried:
            msg = self.font.render("No dried salt! Evaporate raw salt in the Evaporation Pan.", True, _LABEL_C)
            self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2))
            return
        sub = self.small.render("Select a dried crystal to grind:", True, _LABEL_C)
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 32))
        CELL_W, CELL_H, GAP, COLS = 210, 70, 10, 4
        gx0 = (SCREEN_W - (COLS * CELL_W + (COLS - 1) * GAP)) // 2
        for li, (bi, crystal) in enumerate(dried[:16]):
            col_i, row_i = li % COLS, li // COLS
            rx = gx0 + col_i * (CELL_W + GAP)
            ry = 55 + row_i * (CELL_H + GAP)
            rect = pygame.Rect(rx, ry, CELL_W, CELL_H)
            self._grinder_select_rects[bi] = rect
            pygame.draw.rect(self.screen, _CELL_BG, rect)
            pygame.draw.rect(self.screen, _ACCENT, rect, 2)
            biome_nm = BIOME_DISPLAY_NAMES.get(crystal.origin_biome, crystal.origin_biome)
            nm = self.small.render(biome_nm, True, _TITLE_C)
            self.screen.blit(nm, (rx + 6, ry + 8))
            q = getattr(crystal, "_evap_quality", 0.0)
            q_col = _GREEN if q >= 0.7 else _YELLOW if q >= 0.4 else _RED
            ql = self.small.render(f"Quality {int(q * 100)}%", True, q_col)
            self.screen.blit(ql, (rx + 6, ry + 26))
            pur = self.small.render(f"Pur {int(crystal.purity * 100)}%  Moist {int(crystal.moisture * 100)}%", True, _HINT_C)
            self.screen.blit(pur, (rx + 6, ry + 46))

    def _draw_grinder_grade_select(self, player):
        self._grinder_grade_rects.clear()
        c = self._grinder_current_crystal
        if c is None:
            return
        sub = self.small.render("Choose a grind grade:", True, _LABEL_C)
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 32))
        BTN_W, BTN_H, BTN_GAP = 220, 110, 14
        total_w = len(GRADES) * BTN_W + (len(GRADES) - 1) * BTN_GAP
        gx0 = (SCREEN_W - total_w) // 2
        for pi, grade_key in enumerate(GRADES):
            gd = REFINE_GRADES[grade_key]
            px = gx0 + pi * (BTN_W + BTN_GAP)
            py = SCREEN_H // 2 - BTN_H // 2
            prect = pygame.Rect(px, py, BTN_W, BTN_H)
            self._grinder_grade_rects[grade_key] = prect
            is_eligible = (grade_key != "fleur_de_sel") or fleur_eligible(c)
            border_col = _ACCENT if is_eligible else _RED
            pygame.draw.rect(self.screen, _CELL_BG, prect)
            pygame.draw.rect(self.screen, border_col, prect, 2)
            lbl = self.font.render(gd["label"], True, _TITLE_C)
            self.screen.blit(lbl, (px + BTN_W // 2 - lbl.get_width() // 2, py + 10))
            desc_short = gd["desc"].split(".")[0]
            dl = self.small.render(desc_short, True, _LABEL_C)
            self.screen.blit(dl, (px + BTN_W // 2 - dl.get_width() // 2, py + 36))
            if grade_key == "fleur_de_sel" and not is_eligible:
                warn = self.small.render("Will demote to Fine!", True, _RED)
                self.screen.blit(warn, (px + BTN_W // 2 - warn.get_width() // 2, py + 56))
                req_txt = f"Need purity≥65%  moisture≤35%"
                rl = self.small.render(req_txt, True, _DIM_C)
                self.screen.blit(rl, (px + BTN_W // 2 - rl.get_width() // 2, py + 72))
            else:
                # Show buff for this grade
                buff_key = {"coarse": "vitality", "fine": "preservation", "fleur_de_sel": "refinement"}.get(grade_key)
                if buff_key:
                    bd = self.small.render(BUFF_DESCS[buff_key], True, _HINT_C)
                    self.screen.blit(bd, (px + BTN_W // 2 - bd.get_width() // 2, py + 70))

    def _draw_grinder_result(self, player):
        if not self._grinder_result_item:
            return
        cx = SCREEN_W // 2
        msg = self.font.render("Salt Ready!", True, _TITLE_C)
        self.screen.blit(msg, (cx - msg.get_width() // 2, SCREEN_H // 2 - 80))
        from items import ITEMS
        item_nm = ITEMS.get(self._grinder_result_item, {}).get("name", self._grinder_result_item)
        col = OUTPUT_COLORS.get(self._grinder_result_item, _ACCENT)
        nl = self.font.render(item_nm, True, col)
        self.screen.blit(nl, (cx - nl.get_width() // 2, SCREEN_H // 2 - 36))
        c = self._grinder_result_crystal
        if c and c.flavor_notes:
            notes_str = ", ".join(c.flavor_notes[:4])
            fn = self.small.render(f"Notes: {notes_str}", True, _LABEL_C)
            self.screen.blit(fn, (cx - fn.get_width() // 2, SCREEN_H // 2 + 8))
        desc = OUTPUT_DESCS.get(self._grinder_result_item, "")
        if desc:
            dl = self.small.render(desc.split("—")[-1].strip(), True, _HINT_C)
            self.screen.blit(dl, (cx - dl.get_width() // 2, SCREEN_H // 2 + 30))
        ok = self.small.render("Click anywhere to close", True, _DIM_C)
        self.screen.blit(ok, (cx - ok.get_width() // 2, SCREEN_H // 2 + 60))

    def _finish_grinder(self, player, grade_key):
        c = self._grinder_current_crystal
        if c is None:
            return
        out_id = apply_refine_grade(c, grade_key)
        player._add_item(out_id)
        player.discovered_salt_origins.add(f"{c.origin_biome}_{c.refine_grade}")
        # Remove the crystal from player collection (it's been processed)
        if c in player.salt_crystals:
            player.salt_crystals.remove(c)
        self._grinder_result_item = out_id
        self._grinder_result_crystal = c
        self._grinder_phase = "result"

    def _handle_salt_grinder_click(self, pos, player):
        if self._grinder_phase == "select_crystal":
            for bi, rect in self._grinder_select_rects.items():
                if rect.collidepoint(pos):
                    self._grinder_current_crystal = player.salt_crystals[bi]
                    self._grinder_phase = "select_grade"
                    return
        elif self._grinder_phase == "select_grade":
            for grade_key, rect in self._grinder_grade_rects.items():
                if rect.collidepoint(pos):
                    self._finish_grinder(player, grade_key)
                    return
        elif self._grinder_phase == "result":
            self._grinder_phase = "select_crystal"
            self._grinder_result_item = None
            self._grinder_result_crystal = None

    # ─────────────────────────────────────────────────────────────────────────
    # BUFF HUD
    # ─────────────────────────────────────────────────────────────────────────

    def _draw_salt_buffs(self, player):
        if not player.salt_buffs:
            return
        from items import ITEMS
        x = 8
        y_offset = 0
        # Stack below other buff rows — find bottom of existing buffs
        for attr in ("active_buffs", "wine_buffs", "tea_buffs", "cheese_buffs"):
            y_offset += len(getattr(player, attr, {})) * 22
        y = SCREEN_H - 120 - y_offset
        for buff_name, data in player.salt_buffs.items():
            dur = data["duration"]
            desc = BUFF_DESCS.get(buff_name, buff_name)
            txt = self.small.render(f"[Salt] {desc} {dur:.0f}s", True, (235, 230, 210))
            self.screen.blit(txt, (x, y))
            y += 22
