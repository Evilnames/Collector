import math
import random
import pygame
from constants import SCREEN_W, SCREEN_H
from tea import (
    apply_wither, apply_oxidation, apply_aging, apply_herbal_blend, apply_roasting,
    get_brew_item_id, make_blend,
    WITHER_METHODS, WITHER_RACK_SLOTS,
    TEA_TYPE_DESCS, TEA_TYPE_COLORS, TEA_TYPE_BUFFS,
    BUFF_DESCS, BIOME_DISPLAY_NAMES, VARIETY_DISPLAY_NAMES,
    HERBAL_ADDITIVES, AGE_DURATIONS, ROASTING_LEVELS, _CODEX_BIOMES, _CODEX_TEA_TYPES,
)
from world import CYCLE_DURATION
from dataclasses import asdict


_ACCENT   = ( 65, 160,  75)
_DARK_BG  = ( 12,  28,  14)
_CELL_BG  = ( 18,  38,  20)
_TITLE_C  = (140, 215, 130)
_LABEL_C  = (100, 175,  90)
_DIM_C    = ( 55,  90,  50)
_HINT_C   = ( 80, 130,  70)


class TeaMixin:

    # ─────────────────────────────────────────────────────────────────────────
    # WITHERING RACK
    # ─────────────────────────────────────────────────────────────────────────

    def _draw_withering_rack(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("WITHERING RACK", True, _TITLE_C)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, _HINT_C)
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        slots = player.withering_rack_slots
        SLOT_W, SLOT_H = 160, 76
        GAP = 12
        total_w = WITHER_RACK_SLOTS * SLOT_W + (WITHER_RACK_SLOTS - 1) * GAP
        sx0 = (SCREEN_W - total_w) // 2
        sy0 = 34

        # ── Withering slots row ───────────────────────────────────────────
        self._wither_rack_slot_rects.clear()
        for i in range(WITHER_RACK_SLOTS):
            sx = sx0 + i * (SLOT_W + GAP)
            rect = pygame.Rect(sx, sy0, SLOT_W, SLOT_H)
            self._wither_rack_slot_rects[i] = rect

            slot = slots[i] if i < len(slots) else None
            if slot is None:
                pygame.draw.rect(self.screen, _DARK_BG, rect)
                pygame.draw.rect(self.screen, _DIM_C, rect, 1)
                es = self.small.render("Empty", True, _DIM_C)
                self.screen.blit(es, (rect.centerx - es.get_width() // 2,
                                      rect.centery - es.get_height() // 2))
            else:
                done = slot["elapsed"] >= slot["duration"]
                bg   = (14, 44, 18) if not done else (10, 52, 16)
                brd  = (100, 220, 80) if done else _ACCENT
                pygame.draw.rect(self.screen, bg, rect)
                pygame.draw.rect(self.screen, brd, rect, 2 if done else 1)

                ld   = slot["leaf_data"]
                biome_name = BIOME_DISPLAY_NAMES.get(ld["origin_biome"], ld["origin_biome"])
                var_name   = VARIETY_DISPLAY_NAMES.get(ld["variety"], ld["variety"])
                nm_s = self.small.render((biome_name + " " + var_name)[:22], True, _TITLE_C)
                self.screen.blit(nm_s, (rect.x + 5, rect.y + 4))
                wm_s = self.small.render(WITHER_METHODS[slot["method"]]["label"], True, _LABEL_C)
                self.screen.blit(wm_s, (rect.x + 5, rect.y + 20))

                if done:
                    ready_s = self.font.render("READY", True, (100, 255, 80))
                    self.screen.blit(ready_s, (rect.centerx - ready_s.get_width() // 2,
                                               rect.y + 46))
                else:
                    frac = slot["elapsed"] / slot["duration"]
                    bar_x, bar_y = rect.x + 5, rect.y + 56
                    bar_w = SLOT_W - 10
                    pygame.draw.rect(self.screen, (18, 42, 18), (bar_x, bar_y, bar_w, 8))
                    pygame.draw.rect(self.screen, _ACCENT, (bar_x, bar_y, int(bar_w * frac), 8))
                    days_left = (slot["duration"] - slot["elapsed"]) / CYCLE_DURATION
                    ts = self.small.render(f"{days_left:.1f}d", True, _HINT_C)
                    self.screen.blit(ts, (rect.x + 5, rect.y + 42))

        bottom_y  = sy0 + SLOT_H + 14
        leaf_col_w = (SCREEN_W - 20) * 2 // 3
        meth_col_x = leaf_col_w + 20
        meth_col_w = SCREEN_W - meth_col_x - 10

        # ── Bottom-left: raw leaves to place ─────────────────────────────
        pygame.draw.rect(self.screen, _DARK_BG, (8, bottom_y, leaf_col_w, SCREEN_H - bottom_y - 8))
        pygame.draw.rect(self.screen, _DIM_C,   (8, bottom_y, leaf_col_w, SCREEN_H - bottom_y - 8), 1)
        free_slots = sum(1 for i in range(WITHER_RACK_SLOTS)
                         if i >= len(slots) or slots[i] is None)
        hdr = self.small.render(
            f"RAW LEAVES — click to select  (free slots: {free_slots}/{WITHER_RACK_SLOTS})",
            True, _LABEL_C)
        self.screen.blit(hdr, (16, bottom_y + 5))

        self._wither_leaf_rects.clear()
        raw = [(i, x) for i, x in enumerate(player.tea_leaves) if x.state == "raw"]
        CELL_W, CELL_H, GAP2, COLS = 200, 52, 6, max(1, leaf_col_w // 207)
        gx0 = 16
        for li, (bi, leaf) in enumerate(raw[:20]):
            col_i = li % COLS
            row_i = li // COLS
            rx = gx0 + col_i * (CELL_W + GAP2)
            ry = bottom_y + 24 + row_i * (CELL_H + GAP2)
            if ry + CELL_H > SCREEN_H - 10:
                break
            rect = pygame.Rect(rx, ry, CELL_W, CELL_H)
            self._wither_leaf_rects[bi] = rect
            sel = (self._wither_pending_leaf_idx == bi)
            nm = BIOME_DISPLAY_NAMES.get(leaf.origin_biome, leaf.origin_biome)
            vr = VARIETY_DISPLAY_NAMES.get(leaf.variety, leaf.variety)
            pygame.draw.rect(self.screen, (30, 60, 30) if sel else _CELL_BG, rect)
            pygame.draw.rect(self.screen, (120, 220, 100) if sel else _ACCENT, rect,
                             2 if sel else 1)
            ns = self.small.render((nm + " " + vr)[:24], True, _TITLE_C)
            self.screen.blit(ns, (rx + 5, ry + 6))
            rs = self.small.render("Raw — click to select", True, _HINT_C)
            self.screen.blit(rs, (rx + 5, ry + 24))

        if not raw:
            msg = self.font.render("No raw tea leaves! Harvest ripe Tea Plants.", True, _DIM_C)
            self.screen.blit(msg, (16, bottom_y + 30))

        # ── Bottom-right: method picker (shown when leaf is selected) ─────
        pygame.draw.rect(self.screen, _DARK_BG, (meth_col_x, bottom_y, meth_col_w, SCREEN_H - bottom_y - 8))
        pygame.draw.rect(self.screen, _DIM_C,   (meth_col_x, bottom_y, meth_col_w, SCREEN_H - bottom_y - 8), 1)

        if self._wither_pending_leaf_idx is not None and free_slots > 0:
            mhdr = self.small.render("Choose method:", True, _LABEL_C)
            self.screen.blit(mhdr, (meth_col_x + 8, bottom_y + 5))
            self._wither_method_rects.clear()
            for mi, (wkey, wdata) in enumerate(WITHER_METHODS.items()):
                mrect = pygame.Rect(meth_col_x + 8, bottom_y + 24 + mi * 68,
                                    meth_col_w - 16, 60)
                self._wither_method_rects[wkey] = mrect
                pygame.draw.rect(self.screen, _CELL_BG, mrect)
                pygame.draw.rect(self.screen, _ACCENT, mrect, 2)
                lbl = self.font.render(wdata["label"], True, _TITLE_C)
                self.screen.blit(lbl, (mrect.x + 8, mrect.y + 4))
                desc = wdata["desc"].split(".")[0]
                ds   = self.small.render(desc[:36], True, _LABEL_C)
                self.screen.blit(ds, (mrect.x + 8, mrect.y + 24))
                dur_s = self.small.render(f"{wdata['days']}d", True, _HINT_C)
                self.screen.blit(dur_s, (mrect.x + 8, mrect.y + 42))
        elif free_slots == 0:
            full_s = self.small.render("All slots in use.", True, _DIM_C)
            self.screen.blit(full_s, (meth_col_x + 8, bottom_y + 30))
        else:
            sel_s = self.small.render("Select a leaf first.", True, _DIM_C)
            self.screen.blit(sel_s, (meth_col_x + 8, bottom_y + 30))

    def _handle_withering_rack_click(self, pos, player):
        from tea import TeaLeaf, WITHER_RACK_SLOTS
        slots = player.withering_rack_slots

        # Collect from ready slots
        for i, rect in self._wither_rack_slot_rects.items():
            if rect.collidepoint(pos):
                if i < len(slots) and slots[i] is not None:
                    slot = slots[i]
                    if slot["elapsed"] >= slot["duration"]:
                        leaf = TeaLeaf(**slot["leaf_data"])
                        apply_wither(leaf, slot["method"])
                        player.tea_leaves.append(leaf)
                        slots[i] = None
                        while slots and slots[-1] is None:
                            slots.pop()
                return

        # Select a raw leaf
        for bi, rect in self._wither_leaf_rects.items():
            if rect.collidepoint(pos):
                self._wither_pending_leaf_idx = bi
                self._wither_method_rects.clear()
                return

        # Choose method for selected leaf
        if self._wither_pending_leaf_idx is not None:
            free_slots = sum(1 for i in range(WITHER_RACK_SLOTS)
                             if i >= len(slots) or slots[i] is None)
            if free_slots == 0:
                return
            for wkey, rect in self._wither_method_rects.items():
                if rect.collidepoint(pos):
                    bi = self._wither_pending_leaf_idx
                    if bi >= len(player.tea_leaves) or player.tea_leaves[bi].state != "raw":
                        self._wither_pending_leaf_idx = None
                        return
                    leaf = player.tea_leaves.pop(bi)
                    # Find first free slot
                    free_idx = next(
                        (i for i in range(WITHER_RACK_SLOTS)
                         if i >= len(slots) or slots[i] is None),
                        None)
                    if free_idx is None:
                        player.tea_leaves.insert(bi, leaf)
                        return
                    while len(slots) <= free_idx:
                        slots.append(None)
                    slots[free_idx] = {
                        "leaf_data": asdict(leaf),
                        "method":   wkey,
                        "elapsed":  0.0,
                        "duration": WITHER_METHODS[wkey]["days"] * CYCLE_DURATION,
                    }
                    self._wither_pending_leaf_idx = None
                    return

    # ─────────────────────────────────────────────────────────────────────────
    # OXIDATION STATION
    # ─────────────────────────────────────────────────────────────────────────

    def _draw_oxidation_station(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("OXIDATION STATION", True, _TITLE_C)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, _HINT_C)
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        if self._oxidation_phase == "select_leaf":
            self._oxidation_select_rects.clear()
            withered = [(i, x) for i, x in enumerate(player.tea_leaves) if x.state == "withered"]
            if not withered:
                msg = self.font.render("No withered leaves! Use the Withering Rack first.", True, _LABEL_C)
                self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2))
                return
            sub = self.small.render("Select a withered leaf to oxidize:", True, _LABEL_C)
            self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 32))
            CELL_W, CELL_H, GAP, COLS = 200, 56, 8, 5
            gx0 = (SCREEN_W - (COLS * CELL_W + (COLS - 1) * GAP)) // 2
            for li, (bi, leaf) in enumerate(withered[:20]):
                col_i, row_i = li % COLS, li // COLS
                rx = gx0 + col_i * (CELL_W + GAP)
                ry = 55 + row_i * (CELL_H + GAP)
                rect = pygame.Rect(rx, ry, CELL_W, CELL_H)
                self._oxidation_select_rects[bi] = rect
                pygame.draw.rect(self.screen, _CELL_BG, rect)
                pygame.draw.rect(self.screen, _ACCENT, rect, 2)
                nm = BIOME_DISPLAY_NAMES.get(leaf.origin_biome, leaf.origin_biome)
                wm = WITHER_METHODS.get(leaf.wither_method, {}).get("label", leaf.wither_method)
                ns = self.small.render(nm + " — " + wm, True, _TITLE_C)
                self.screen.blit(ns, (rx + 6, ry + 8))
                hint2 = self.small.render("Click to oxidize", True, _HINT_C)
                self.screen.blit(hint2, (rx + 6, ry + 26))

        elif self._oxidation_phase == "oxidizing":
            if not self._oxidation_locked:
                # Surge state machine: idle → warning → active → idle
                self._surge_timer += dt
                if self._surge_phase == "idle":
                    if self._oxidation_time >= self._surge_next_at:
                        self._surge_phase     = "warning"
                        self._surge_timer     = 0.0
                        self._surge_intensity = random.uniform(0.85, 1.20)
                        self._surge_duration  = random.uniform(2.0, 3.5)
                elif self._surge_phase == "warning":
                    if self._surge_timer >= 1.5:
                        self._surge_phase = "active"
                        self._surge_timer = 0.0
                elif self._surge_phase == "active":
                    self._enzymatic_velocity = min(
                        self._enzymatic_velocity + self._surge_intensity * 0.012 * dt * 60,
                        0.025)
                    if self._surge_timer >= self._surge_duration:
                        self._surge_phase   = "idle"
                        self._surge_timer   = 0.0
                        self._surge_next_at = self._oxidation_time + random.uniform(6.0, 11.0)

                # Decay momentum when not in active surge
                if self._surge_phase != "active":
                    self._enzymatic_velocity = max(
                        0.0, self._enzymatic_velocity - 0.006 * dt * 60)

                # Speed: sin-wave base + enzymatic momentum; SPACE halves surge component
                base      = 0.006 + 0.003 * math.sin(self._oxidation_time * 1.8)
                effective = base + self._enzymatic_velocity
                if self._oxidation_held:
                    effective = base * 0.25 + self._enzymatic_velocity * 0.50
                self._oxidation_level = min(1.0, self._oxidation_level + effective * dt * 60)
                self._oxidation_time  = min(self._oxidation_total_time,
                                            self._oxidation_time + dt)

            # Zone colors and labels (bottom to top: green 0–20%, oolong 20–75%, black 75–95%, puerh 95–100%)
            BAR_X, BAR_Y, BAR_W, BAR_H = 80, 60, 40, SCREEN_H - 180
            _bar_border = (200, 160, 40) if self._surge_phase in ("warning", "active") else _DIM_C
            pygame.draw.rect(self.screen, (15, 25, 12), (BAR_X, BAR_Y, BAR_W, BAR_H))
            pygame.draw.rect(self.screen, _bar_border, (BAR_X, BAR_Y, BAR_W, BAR_H), 2)

            def _zone_y(v): return BAR_Y + BAR_H - int(BAR_H * v)

            zone_bands = [
                (0.00, 0.08,  (205, 200, 180), "White"),
                (0.08, 0.18,  (190, 170,  70), "Yellow"),
                (0.18, 0.28,  ( 50, 140,  50), "Green"),
                (0.28, 0.75,  (160, 130,  40), "Oolong"),
                (0.75, 0.93,  ( 55,  25,  10), "Black"),
                (0.93, 1.00,  ( 35,  20,   8), "Pu-erh"),
            ]
            for lo, hi, band_col, band_lbl in zone_bands:
                y_top = _zone_y(hi)
                y_bot = _zone_y(lo)
                pygame.draw.rect(self.screen, band_col, (BAR_X, y_top, BAR_W, y_bot - y_top))
                lbl_s = self.small.render(band_lbl, True, (200, 200, 200))
                self.screen.blit(lbl_s, (BAR_X - lbl_s.get_width() - 6,
                                         (y_top + y_bot) // 2 - lbl_s.get_height() // 2))

            # Zone divider lines
            for v in (0.08, 0.18, 0.28, 0.75, 0.93):
                yl = _zone_y(v)
                pygame.draw.line(self.screen, (180, 180, 160), (BAR_X, yl), (BAR_X + BAR_W, yl), 1)

            # Oxidation level marker — color reflects surge state
            marker_y = _zone_y(self._oxidation_level)
            if self._oxidation_locked:
                marker_col = (255, 230, 80)
            elif self._surge_phase == "active":
                marker_col = (255, 140, 30) if int(self._oxidation_time * 4) % 2 else (120, 210, 100)
            elif self._surge_phase == "warning":
                marker_col = (255, 190, 60)
            elif self._enzymatic_velocity > 0.004:
                marker_col = (200, 170, 60)
            else:
                marker_col = (120, 210, 100)
            pygame.draw.rect(self.screen, marker_col, (BAR_X - 8, marker_y - 4, BAR_W + 16, 8))
            pct_lbl = self.small.render(f"{self._oxidation_level:.0%}", True, marker_col)
            self.screen.blit(pct_lbl, (BAR_X + BAR_W + 6, marker_y - 6))

            # Current tea type label
            from tea import tea_type_from_oxidation
            cur_type = tea_type_from_oxidation(self._oxidation_level)
            type_col  = TEA_TYPE_COLORS.get(cur_type, _ACCENT)
            type_lbl  = self.font.render(TEA_TYPE_DESCS.get(cur_type, cur_type), True, type_col)
            self.screen.blit(type_lbl, (SCREEN_W // 2 - type_lbl.get_width() // 2, 38))

            # Time bar
            TIME_X, TIME_Y = 150, SCREEN_H - 110
            TIME_W = SCREEN_W - 300
            pygame.draw.rect(self.screen, _DARK_BG, (TIME_X, TIME_Y, TIME_W, 18))
            pygame.draw.rect(self.screen, _DIM_C, (TIME_X, TIME_Y, TIME_W, 18), 2)
            prog = min(1.0, self._oxidation_time / self._oxidation_total_time)
            pygame.draw.rect(self.screen, _ACCENT, (TIME_X, TIME_Y, int(TIME_W * prog), 18))
            ts = self.small.render(f"{self._oxidation_time:.1f}s", True, _LABEL_C)
            self.screen.blit(ts, (TIME_X + TIME_W + 6, TIME_Y + 1))

            # Instructions
            inst = self.small.render(
                "Hold SPACE to resist.  ENTER or click LOCK to set the level.", True, _HINT_C)
            self.screen.blit(inst, (SCREEN_W // 2 - inst.get_width() // 2, TIME_Y - 50))
            _surge_active = self._surge_phase in ("warning", "active")
            hint2_col = (255, 190, 60) if _surge_active else _DIM_C
            hint2 = self.small.render(
                "Enzyme surges push the bar — SPACE won't fully stop them.", True, hint2_col)
            self.screen.blit(hint2, (SCREEN_W // 2 - hint2.get_width() // 2, TIME_Y - 34))

            # Surge warning label (blinks during warning/active)
            if _surge_active and int(self._oxidation_time * 6) % 2 == 0:
                surge_lbl = self.font.render("ENZYME SURGE!", True, (255, 190, 60))
                self.screen.blit(surge_lbl, (SCREEN_W // 2 - surge_lbl.get_width() // 2, TIME_Y - 80))

            # LOCK button
            lock_rect = pygame.Rect(SCREEN_W - 150, SCREEN_H - 110, 130, 32)
            lock_col  = (30, 80, 35) if not self._oxidation_locked else (50, 120, 50)
            pygame.draw.rect(self.screen, lock_col, lock_rect)
            pygame.draw.rect(self.screen, _ACCENT, lock_rect, 2)
            ll = self.font.render("LOCK", True, _TITLE_C)
            self.screen.blit(ll, (lock_rect.centerx - ll.get_width() // 2,
                                  lock_rect.centery - ll.get_height() // 2))
            self._oxidation_lock_btn = lock_rect

            # SLOW button (visual for SPACE)
            slow_rect = pygame.Rect(SCREEN_W - 150, SCREEN_H - 150, 130, 32)
            slow_col  = (40, 100, 45) if self._oxidation_held else (25, 60, 30)
            pygame.draw.rect(self.screen, slow_col, slow_rect)
            pygame.draw.rect(self.screen, _ACCENT, slow_rect, 2)
            sl = self.font.render("RESIST" if self._surge_phase == "active" else "SLOW", True, _TITLE_C)
            self.screen.blit(sl, (slow_rect.centerx - sl.get_width() // 2,
                                  slow_rect.centery - sl.get_height() // 2))
            self._oxidation_slow_btn = slow_rect

        elif self._oxidation_phase == "result":
            leaf = player.tea_leaves[self._oxidation_leaf_idx]
            tea_col = TEA_TYPE_COLORS.get(leaf.tea_type, _ACCENT)
            cx, cy  = SCREEN_W // 2, 80
            pygame.draw.circle(self.screen, tea_col, (cx, cy + 40), 36)
            pygame.draw.circle(self.screen, (min(255, tea_col[0] + 40),
                                              min(255, tea_col[1] + 40),
                                              min(255, tea_col[2] + 40)),
                                (cx, cy + 40), 36, 3)

            iy = cy + 95
            def rline(txt, col=_TITLE_C):
                nonlocal iy
                s = self.font.render(txt, True, col)
                self.screen.blit(s, (cx - s.get_width() // 2, iy))
                iy += 28

            rline(BIOME_DISPLAY_NAMES.get(leaf.origin_biome, leaf.origin_biome) + " " +
                  VARIETY_DISPLAY_NAMES.get(leaf.variety, leaf.variety))
            rline(TEA_TYPE_DESCS.get(leaf.tea_type, leaf.tea_type), tea_col)
            stars  = "★" * round(leaf.steep_quality * 5) + "☆" * (5 - round(leaf.steep_quality * 5))
            rline(stars, (220, 200, 80))
            rline(f"Oxidation: {leaf.oxidation:.0%}", _LABEL_C)
            if leaf.flavor_notes:
                rline("Flavour Notes:", (160, 200, 130))
                for note in leaf.flavor_notes:
                    rline(f"  • {note.title()}", _TITLE_C)

            done_rect = pygame.Rect(cx - 70, iy + 20, 140, 34)
            pygame.draw.rect(self.screen, _DARK_BG, done_rect)
            pygame.draw.rect(self.screen, _ACCENT, done_rect, 2)
            dl = self.font.render("DONE", True, _TITLE_C)
            self.screen.blit(dl, (done_rect.centerx - dl.get_width() // 2,
                                  done_rect.centery - dl.get_height() // 2))
            self._oxidation_result_btn = done_rect

    def _handle_oxidation_station_click(self, pos, player):
        if self._oxidation_phase == "select_leaf":
            for bi, rect in self._oxidation_select_rects.items():
                if rect.collidepoint(pos):
                    if player.tea_leaves[bi].state == "withered":
                        self._oxidation_leaf_idx  = bi
                        self._oxidation_level     = 0.0
                        self._oxidation_time      = 0.0
                        self._oxidation_locked    = False
                        self._oxidation_quality   = 0.0
                        self._oxidation_phase     = "oxidizing"
                        self._surge_phase        = "idle"
                        self._surge_timer        = 0.0
                        self._surge_next_at      = random.uniform(5.0, 9.0)
                        self._surge_duration     = 0.0
                        self._surge_intensity    = 1.0
                        self._enzymatic_velocity = 0.0
                    return
        elif self._oxidation_phase == "oxidizing":
            if hasattr(self, "_oxidation_slow_btn") and self._oxidation_slow_btn and \
               self._oxidation_slow_btn.collidepoint(pos):
                self._oxidation_held = not self._oxidation_held
                return
            if hasattr(self, "_oxidation_lock_btn") and self._oxidation_lock_btn and \
               self._oxidation_lock_btn.collidepoint(pos):
                self._finish_oxidation(player)
                return
        elif self._oxidation_phase == "result":
            if self._oxidation_result_btn and self._oxidation_result_btn.collidepoint(pos):
                self._oxidation_phase    = "select_leaf"
                self._oxidation_leaf_idx = None

    def handle_oxidation_keydown(self, key, player):
        import pygame as _pg
        if key == _pg.K_RETURN and self._oxidation_phase == "oxidizing":
            self._finish_oxidation(player)
        elif key == _pg.K_RETURN and self._oxidation_phase == "result":
            self._oxidation_phase    = "select_leaf"
            self._oxidation_leaf_idx = None

    def handle_oxidation_keys(self, keys, dt, player):
        import pygame as _pg
        if self._oxidation_phase == "oxidizing":
            self._oxidation_held = keys[_pg.K_SPACE]

    def _finish_oxidation(self, player):
        leaf = player.tea_leaves[self._oxidation_leaf_idx]
        ox   = self._oxidation_level
        # Quality = how centered in the active zone
        from tea import tea_type_from_oxidation, OXIDATION_ZONES
        t_type = tea_type_from_oxidation(ox)
        lo, hi = OXIDATION_ZONES[t_type]
        zone_size = hi - lo
        center    = (lo + hi) / 2
        centrality = max(0.0, 1.0 - abs(ox - center) / (zone_size * 0.5 + 1e-6))
        # Time bonus: reaching optimal zone earlier yields better quality
        time_bonus = max(0.0, 1.0 - self._oxidation_time / self._oxidation_total_time) * 0.3
        quality    = min(1.0, centrality * 0.7 + time_bonus)
        apply_oxidation(leaf, ox, quality)
        player.discovered_tea_origins.add(f"{leaf.origin_biome}_{leaf.tea_type}")
        self._oxidation_locked = True
        self._oxidation_phase  = "result"

    # ─────────────────────────────────────────────────────────────────────────
    # TEA CELLAR
    # ─────────────────────────────────────────────────────────────────────────

    def _draw_tea_cellar(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("TEA CELLAR", True, _TITLE_C)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, _HINT_C)
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        # Tab bar
        tabs     = [("brew", "Brew"), ("blend", "Blend"), ("age", "Age (Pu-erh)"), ("roast", "Roast")]
        tab_w    = 180
        tab_x    = SCREEN_W // 2 - (len(tabs) * tab_w) // 2
        self._tea_cellar_tab_rects = {}
        for ti, (tkey, tlbl) in enumerate(tabs):
            trect = pygame.Rect(tab_x + ti * tab_w, 30, tab_w - 4, 26)
            self._tea_cellar_tab_rects[tkey] = trect
            active = (self._tea_cellar_tab == tkey)
            pygame.draw.rect(self.screen, (_ACCENT if active else _DARK_BG), trect)
            pygame.draw.rect(self.screen, _ACCENT, trect, 1)
            ts = self.small.render(tlbl, True, (255, 255, 255) if active else _LABEL_C)
            self.screen.blit(ts, (trect.centerx - ts.get_width() // 2,
                                  trect.centery - ts.get_height() // 2))

        if self._tea_cellar_tab == "brew":
            self._draw_tea_cellar_brew(player)
        elif self._tea_cellar_tab == "blend":
            self._draw_tea_cellar_blend(player)
        elif self._tea_cellar_tab == "age":
            self._draw_tea_cellar_age(player)
        elif self._tea_cellar_tab == "roast":
            self._draw_tea_cellar_roast(player)

    def _draw_tea_cellar_brew(self, player):
        self._tea_cellar_select_rects.clear()
        oxidized = [(i, x) for i, x in enumerate(player.tea_leaves)
                    if x.state in ("oxidized", "blended")]
        if not oxidized:
            msg = self.font.render("No processed leaves! Use the Oxidation Station first.", True, _LABEL_C)
            self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2))
            return
        sub = self.small.render("Select a leaf to brew into tea:", True, _LABEL_C)
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 62))
        CELL_W, CELL_H, GAP, COLS = 220, 66, 8, 5
        gx0 = (SCREEN_W - (COLS * CELL_W + (COLS - 1) * GAP)) // 2
        for li, (bi, leaf) in enumerate(oxidized[:20]):
            col_i, row_i = li % COLS, li // COLS
            rx = gx0 + col_i * (CELL_W + GAP)
            ry = 82 + row_i * (CELL_H + GAP)
            rect = pygame.Rect(rx, ry, CELL_W, CELL_H)
            self._tea_cellar_select_rects[bi] = rect
            tea_col = TEA_TYPE_COLORS.get(leaf.tea_type, _ACCENT)
            pygame.draw.rect(self.screen, _CELL_BG, rect)
            pygame.draw.rect(self.screen, tea_col, rect, 2)
            nm = BIOME_DISPLAY_NAMES.get(leaf.origin_biome, leaf.origin_biome)
            ns = self.small.render(nm + " — " + leaf.tea_type.title(), True, tea_col)
            self.screen.blit(ns, (rx + 6, ry + 6))
            stars = "★" * round(leaf.steep_quality * 5)
            ss = self.small.render(stars, True, (220, 200, 80))
            self.screen.blit(ss, (rx + 6, ry + 24))
            out_id = get_brew_item_id(leaf)
            from items import ITEMS
            out_name = ITEMS.get(out_id, {}).get("name", out_id)
            os = self.small.render("→ " + out_name, True, _HINT_C)
            self.screen.blit(os, (rx + 6, ry + 42))

    def _draw_tea_cellar_blend(self, player):
        self._tea_cellar_select_rects.clear()
        oxidized = [(i, x) for i, x in enumerate(player.tea_leaves)
                    if x.state in ("oxidized", "blended") and x.tea_type]
        if not oxidized:
            msg = self.font.render("No processed leaves to blend.", True, _LABEL_C)
            self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2 - 20))
            return
        sub = self.small.render("Select a leaf to add herbal blends:", True, _LABEL_C)
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 62))
        CELL_W, CELL_H, GAP, COLS = 220, 56, 8, 5
        gx0 = (SCREEN_W - (COLS * CELL_W + (COLS - 1) * GAP)) // 2
        for li, (bi, leaf) in enumerate(oxidized[:15]):
            col_i, row_i = li % COLS, li // COLS
            rx = gx0 + col_i * (CELL_W + GAP)
            ry = 82 + row_i * (CELL_H + GAP)
            rect = pygame.Rect(rx, ry, CELL_W, CELL_H)
            self._tea_cellar_select_rects[bi] = rect
            tea_col = TEA_TYPE_COLORS.get(leaf.tea_type, _ACCENT)
            pygame.draw.rect(self.screen, _CELL_BG, rect)
            pygame.draw.rect(self.screen, tea_col, rect, 2)
            nm  = BIOME_DISPLAY_NAMES.get(leaf.origin_biome, leaf.origin_biome)
            ns  = self.small.render(nm + " " + leaf.tea_type.title(), True, tea_col)
            self.screen.blit(ns, (rx + 6, ry + 6))
            adds = ", ".join(HERBAL_ADDITIVES.get(k, {}).get("label", k) for k in leaf.herbal_additions)
            if adds:
                as_ = self.small.render("+ " + adds, True, (180, 210, 140))
                self.screen.blit(as_, (rx + 6, ry + 24))

        # Show available additives on the right
        if self._tea_cellar_leaf_idx is not None and \
           0 <= self._tea_cellar_leaf_idx < len(player.tea_leaves):
            leaf = player.tea_leaves[self._tea_cellar_leaf_idx]
            rx0 = SCREEN_W - 280
            ry0 = 82
            pygame.draw.rect(self.screen, _DARK_BG, (rx0, ry0, 260, 200))
            pygame.draw.rect(self.screen, _ACCENT, (rx0, ry0, 260, 200), 2)
            hdr = self.small.render("Add Herbals (from inventory):", True, _LABEL_C)
            self.screen.blit(hdr, (rx0 + 8, ry0 + 6))
            self._tea_herbal_rects = {}
            for hi, (hkey, hdata) in enumerate(HERBAL_ADDITIVES.items()):
                have = player.inventory.get(hkey, 0)
                if have <= 0:
                    continue
                hrect = pygame.Rect(rx0 + 8, ry0 + 30 + hi * 34, 244, 28)
                self._tea_herbal_rects[hkey] = hrect
                already = hkey in leaf.herbal_additions
                pygame.draw.rect(self.screen, (30, 60, 30) if not already else (50, 90, 50), hrect)
                pygame.draw.rect(self.screen, _ACCENT, hrect, 1)
                lbl_s = self.small.render(
                    hdata["label"] + (f"  (x{have})" if not already else "  ✓"), True,
                    _TITLE_C if not already else (180, 220, 140))
                self.screen.blit(lbl_s, (hrect.x + 6, hrect.centery - lbl_s.get_height() // 2))

    def _draw_tea_cellar_age(self, player):
        self._tea_cellar_select_rects.clear()
        puerh = [(i, x) for i, x in enumerate(player.tea_leaves)
                 if x.state == "oxidized" and x.tea_type == "puerh"]
        if not puerh:
            msg = self.font.render("No oxidized Pu-erh leaves! Only Pu-erh can be aged.", True, _LABEL_C)
            self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2 - 20))
            return
        sub = self.small.render("Select a Pu-erh leaf to age:", True, _LABEL_C)
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 62))
        CELL_W, CELL_H, GAP, COLS = 220, 56, 8, 4
        gx0 = (SCREEN_W - (COLS * CELL_W + (COLS - 1) * GAP)) // 2
        for li, (bi, leaf) in enumerate(puerh[:12]):
            col_i, row_i = li % COLS, li // COLS
            rx = gx0 + col_i * (CELL_W + GAP)
            ry = 82 + row_i * (CELL_H + GAP)
            rect = pygame.Rect(rx, ry, CELL_W, CELL_H)
            self._tea_cellar_select_rects[bi] = rect
            tea_col = TEA_TYPE_COLORS.get("puerh", _ACCENT)
            pygame.draw.rect(self.screen, _CELL_BG, rect)
            pygame.draw.rect(self.screen, tea_col, rect, 2)
            nm  = BIOME_DISPLAY_NAMES.get(leaf.origin_biome, leaf.origin_biome)
            ns  = self.small.render(nm, True, tea_col)
            self.screen.blit(ns, (rx + 6, ry + 8))
            stars = "★" * round(leaf.steep_quality * 5)
            ss = self.small.render(stars, True, (220, 200, 80))
            self.screen.blit(ss, (rx + 6, ry + 26))

        if self._tea_cellar_leaf_idx is not None and \
           0 <= self._tea_cellar_leaf_idx < len(player.tea_leaves):
            leaf = player.tea_leaves[self._tea_cellar_leaf_idx]
            rx0 = SCREEN_W - 300
            ry0 = 82
            pygame.draw.rect(self.screen, _DARK_BG, (rx0, ry0, 280, 220))
            pygame.draw.rect(self.screen, TEA_TYPE_COLORS.get("puerh", _ACCENT), (rx0, ry0, 280, 220), 2)
            hdr = self.small.render("Choose aging duration:", True, _LABEL_C)
            self.screen.blit(hdr, (rx0 + 8, ry0 + 6))
            self._tea_cellar_age_rects.clear()
            for ai, (akey, adata) in enumerate(AGE_DURATIONS.items()):
                arect = pygame.Rect(rx0 + 8, ry0 + 32 + ai * 52, 264, 44)
                self._tea_cellar_age_rects[akey] = arect
                pygame.draw.rect(self.screen, (30, 22, 10), arect)
                pygame.draw.rect(self.screen, (130, 90, 40), arect, 2)
                al  = self.font.render(adata["label"], True, (200, 160, 80))
                self.screen.blit(al, (arect.x + 10, arect.y + 6))
                qm  = self.small.render(f"Quality ×{adata['quality_mult']:.2f}  +{adata['complexity_delta']:.0%} complexity",
                                         True, _HINT_C)
                self.screen.blit(qm, (arect.x + 10, arect.y + 26))

    def _handle_tea_cellar_click(self, pos, player):
        # Tab clicks
        if hasattr(self, "_tea_cellar_tab_rects"):
            for tkey, trect in self._tea_cellar_tab_rects.items():
                if trect.collidepoint(pos):
                    self._tea_cellar_tab      = tkey
                    self._tea_cellar_leaf_idx = None
                    return

        if self._tea_cellar_tab == "brew":
            for bi, rect in self._tea_cellar_select_rects.items():
                if rect.collidepoint(pos):
                    leaf = player.tea_leaves[bi]
                    out_id = get_brew_item_id(leaf)
                    player._add_item(out_id)
                    player.tea_leaves.pop(bi)
                    return

        elif self._tea_cellar_tab == "blend":
            for bi, rect in self._tea_cellar_select_rects.items():
                if rect.collidepoint(pos):
                    self._tea_cellar_leaf_idx = bi
                    return
            if hasattr(self, "_tea_herbal_rects") and self._tea_cellar_leaf_idx is not None:
                leaf = player.tea_leaves[self._tea_cellar_leaf_idx]
                for hkey, hrect in self._tea_herbal_rects.items():
                    if hrect.collidepoint(pos) and hkey not in leaf.herbal_additions:
                        if player.inventory.get(hkey, 0) > 0:
                            apply_herbal_blend(leaf, [hkey])
                            player.inventory[hkey] = player.inventory[hkey] - 1
                            if player.inventory[hkey] <= 0:
                                del player.inventory[hkey]
                            return

        elif self._tea_cellar_tab == "age":
            for bi, rect in self._tea_cellar_select_rects.items():
                if rect.collidepoint(pos):
                    self._tea_cellar_leaf_idx = bi
                    return
            if self._tea_cellar_leaf_idx is not None:
                leaf = player.tea_leaves[self._tea_cellar_leaf_idx]
                for akey, arect in self._tea_cellar_age_rects.items():
                    if arect.collidepoint(pos):
                        apply_aging(leaf, akey)
                        self._tea_cellar_leaf_idx = None
                        return

        elif self._tea_cellar_tab == "roast":
            for bi, rect in self._tea_cellar_select_rects.items():
                if rect.collidepoint(pos):
                    self._tea_cellar_leaf_idx = bi
                    return
            if self._tea_cellar_leaf_idx is not None:
                leaf = player.tea_leaves[self._tea_cellar_leaf_idx]
                for rkey, rrect in self._tea_cellar_roast_rects.items():
                    if rrect.collidepoint(pos):
                        apply_roasting(leaf, rkey)
                        player.discovered_tea_origins.add(f"{leaf.origin_biome}_hojicha")
                        self._tea_cellar_leaf_idx = None
                        return

    def _draw_tea_cellar_roast(self, player):
        self._tea_cellar_select_rects.clear()
        roastable = [(i, x) for i, x in enumerate(player.tea_leaves)
                     if x.state == "oxidized" and x.tea_type in ("green", "oolong", "white", "yellow")]
        if not roastable:
            msg = self.font.render("No roastable leaves! Use oxidized Green, White, Yellow, or Oolong.", True, _LABEL_C)
            self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2 - 20))
            return
        sub = self.small.render("Select a leaf to roast into Hojicha:", True, _LABEL_C)
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 62))
        CELL_W, CELL_H, GAP, COLS = 220, 56, 8, 4
        gx0 = (SCREEN_W - (COLS * CELL_W + (COLS - 1) * GAP)) // 2
        for li, (bi, leaf) in enumerate(roastable[:12]):
            col_i, row_i = li % COLS, li // COLS
            rx = gx0 + col_i * (CELL_W + GAP)
            ry = 82 + row_i * (CELL_H + GAP)
            rect = pygame.Rect(rx, ry, CELL_W, CELL_H)
            self._tea_cellar_select_rects[bi] = rect
            tea_col = TEA_TYPE_COLORS.get(leaf.tea_type, _ACCENT)
            pygame.draw.rect(self.screen, _CELL_BG, rect)
            pygame.draw.rect(self.screen, tea_col, rect, 2)
            nm  = BIOME_DISPLAY_NAMES.get(leaf.origin_biome, leaf.origin_biome)
            ns  = self.small.render(nm + " — " + leaf.tea_type.title(), True, tea_col)
            self.screen.blit(ns, (rx + 6, ry + 8))
            stars = "★" * round(leaf.steep_quality * 5)
            ss = self.small.render(stars, True, (220, 200, 80))
            self.screen.blit(ss, (rx + 6, ry + 26))

        if self._tea_cellar_leaf_idx is not None and \
           0 <= self._tea_cellar_leaf_idx < len(player.tea_leaves):
            leaf = player.tea_leaves[self._tea_cellar_leaf_idx]
            rx0 = SCREEN_W - 300
            ry0 = 82
            pygame.draw.rect(self.screen, _DARK_BG, (rx0, ry0, 280, 240))
            pygame.draw.rect(self.screen, TEA_TYPE_COLORS.get("hojicha", _ACCENT), (rx0, ry0, 280, 240), 2)
            hdr = self.small.render("Choose roast level:", True, _LABEL_C)
            self.screen.blit(hdr, (rx0 + 8, ry0 + 6))
            self._tea_cellar_roast_rects.clear()
            for ri, (rkey, rdata) in enumerate(ROASTING_LEVELS.items()):
                rrect = pygame.Rect(rx0 + 8, ry0 + 32 + ri * 62, 264, 54)
                self._tea_cellar_roast_rects[rkey] = rrect
                pygame.draw.rect(self.screen, (35, 20, 10), rrect)
                pygame.draw.rect(self.screen, TEA_TYPE_COLORS.get("hojicha", _ACCENT), rrect, 2)
                rl  = self.font.render(rdata["label"], True, (200, 140, 70))
                self.screen.blit(rl, (rrect.x + 10, rrect.y + 6))
                desc_lines = rdata["desc"].split(". ")
                for di, dl in enumerate(desc_lines[:1]):
                    ds = self.small.render(dl, True, _HINT_C)
                    self.screen.blit(ds, (rrect.x + 10, rrect.y + 28))
                qm = self.small.render(f"Quality ×{rdata['quality_mult']:.2f}  +{rdata['complexity_bonus']:.0%} complexity",
                                       True, _DIM_C)
                self.screen.blit(qm, (rrect.x + 10, rrect.y + 40))

    # ─────────────────────────────────────────────────────────────────────────
    # ROASTING KILN (standalone block)
    # ─────────────────────────────────────────────────────────────────────────

    def _draw_roasting_kiln(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("ROASTING KILN", True, (200, 140, 70))
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, _HINT_C)
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        if self._roasting_phase == "select_leaf":
            self._roasting_select_rects.clear()
            roastable = [(i, x) for i, x in enumerate(player.tea_leaves)
                         if x.state == "oxidized" and x.tea_type in ("green", "oolong", "white", "yellow")]
            if not roastable:
                msg = self.font.render("No roastable leaves! Use oxidized Green, White, Yellow, or Oolong.", True, _LABEL_C)
                self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2))
                return
            sub = self.small.render("Select a leaf to roast into Hojicha:", True, _LABEL_C)
            self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 32))
            CELL_W, CELL_H, GAP, COLS = 200, 56, 8, 5
            gx0 = (SCREEN_W - (COLS * CELL_W + (COLS - 1) * GAP)) // 2
            for li, (bi, leaf) in enumerate(roastable[:20]):
                col_i, row_i = li % COLS, li // COLS
                rx = gx0 + col_i * (CELL_W + GAP)
                ry = 55 + row_i * (CELL_H + GAP)
                rect = pygame.Rect(rx, ry, CELL_W, CELL_H)
                self._roasting_select_rects[bi] = rect
                tea_col = TEA_TYPE_COLORS.get(leaf.tea_type, _ACCENT)
                pygame.draw.rect(self.screen, _CELL_BG, rect)
                pygame.draw.rect(self.screen, tea_col, rect, 2)
                nm = BIOME_DISPLAY_NAMES.get(leaf.origin_biome, leaf.origin_biome)
                ns = self.small.render(nm + " — " + leaf.tea_type.title(), True, tea_col)
                self.screen.blit(ns, (rx + 6, ry + 8))
                stars = "★" * round(leaf.steep_quality * 5)
                ss = self.small.render(stars, True, (220, 200, 80))
                self.screen.blit(ss, (rx + 6, ry + 26))

        elif self._roasting_phase == "select_level":
            sub = self.small.render("Choose a roast level:", True, _LABEL_C)
            self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 32))
            self._roasting_level_rects.clear()
            BTN_W, BTN_H, BTN_GAP = 280, 120, 20
            total_w = len(ROASTING_LEVELS) * BTN_W + (len(ROASTING_LEVELS) - 1) * BTN_GAP
            gx0 = (SCREEN_W - total_w) // 2
            for ri, (rkey, rdata) in enumerate(ROASTING_LEVELS.items()):
                px = gx0 + ri * (BTN_W + BTN_GAP)
                py = SCREEN_H // 2 - BTN_H // 2
                prect = pygame.Rect(px, py, BTN_W, BTN_H)
                self._roasting_level_rects[rkey] = prect
                pygame.draw.rect(self.screen, (30, 18, 8), prect)
                pygame.draw.rect(self.screen, (160, 90, 35), prect, 2)
                lbl = self.font.render(rdata["label"], True, (210, 150, 80))
                self.screen.blit(lbl, (px + BTN_W // 2 - lbl.get_width() // 2, py + 10))
                desc_lines = rdata["desc"].split(". ")
                for di, dl in enumerate(desc_lines[:2]):
                    ds = self.small.render(dl, True, _LABEL_C)
                    self.screen.blit(ds, (px + 8, py + 40 + di * 16))
                qm = self.small.render(f"Quality ×{rdata['quality_mult']:.2f}  +{rdata['complexity_bonus']:.0%} complexity",
                                       True, _HINT_C)
                self.screen.blit(qm, (px + 8, py + 90))

        elif self._roasting_phase == "result":
            leaf = player.tea_leaves[self._roasting_leaf_idx]
            hojicha_col = TEA_TYPE_COLORS.get("hojicha", _ACCENT)
            cx, cy = SCREEN_W // 2, 80
            pygame.draw.circle(self.screen, hojicha_col, (cx, cy + 40), 36)
            pygame.draw.circle(self.screen, (min(255, hojicha_col[0] + 40),
                                              min(255, hojicha_col[1] + 40),
                                              min(255, hojicha_col[2] + 40)),
                                (cx, cy + 40), 36, 3)

            iy = cy + 95
            def rline(txt, col=_TITLE_C):
                nonlocal iy
                s = self.font.render(txt, True, col)
                self.screen.blit(s, (cx - s.get_width() // 2, iy))
                iy += 28

            rline(BIOME_DISPLAY_NAMES.get(leaf.origin_biome, leaf.origin_biome) + " " +
                  VARIETY_DISPLAY_NAMES.get(leaf.variety, leaf.variety))
            rline(TEA_TYPE_DESCS.get("hojicha", "Hojicha"), hojicha_col)
            rline(f"Roast: {ROASTING_LEVELS.get(leaf.roasting_level, {}).get('label', leaf.roasting_level)}", (200, 140, 70))
            stars = "★" * round(leaf.steep_quality * 5) + "☆" * (5 - round(leaf.steep_quality * 5))
            rline(stars, (220, 200, 80))
            if leaf.flavor_notes:
                rline("Flavour Notes:", (160, 200, 130))
                for note in leaf.flavor_notes:
                    rline(f"  • {note.title()}", _TITLE_C)

            done_rect = pygame.Rect(cx - 70, iy + 20, 140, 34)
            pygame.draw.rect(self.screen, _DARK_BG, done_rect)
            pygame.draw.rect(self.screen, (160, 90, 35), done_rect, 2)
            dl = self.font.render("DONE", True, _TITLE_C)
            self.screen.blit(dl, (done_rect.centerx - dl.get_width() // 2,
                                  done_rect.centery - dl.get_height() // 2))
            self._roasting_result_btn = done_rect

    def _handle_roasting_kiln_click(self, pos, player):
        if self._roasting_phase == "select_leaf":
            for bi, rect in self._roasting_select_rects.items():
                if rect.collidepoint(pos):
                    if player.tea_leaves[bi].state == "oxidized":
                        self._roasting_leaf_idx = bi
                        self._roasting_phase    = "select_level"
                    return
        elif self._roasting_phase == "select_level":
            for rkey, rect in self._roasting_level_rects.items():
                if rect.collidepoint(pos):
                    leaf = player.tea_leaves[self._roasting_leaf_idx]
                    apply_roasting(leaf, rkey)
                    player.discovered_tea_origins.add(f"{leaf.origin_biome}_hojicha")
                    self._roasting_phase = "result"
                    return
        elif self._roasting_phase == "result":
            if self._roasting_result_btn and self._roasting_result_btn.collidepoint(pos):
                self._roasting_phase    = "select_leaf"
                self._roasting_leaf_idx = None

    # ─────────────────────────────────────────────────────────────────────────
    # BUFF HUD
    # ─────────────────────────────────────────────────────────────────────────

    def _draw_tea_buffs(self, player):
        if not player.tea_buffs:
            return
        x = SCREEN_W - 200
        y = 260
        for buff, data in player.tea_buffs.items():
            dur    = data["duration"]
            label  = BUFF_DESCS.get(buff, buff)
            lbl_s  = self.small.render(f"☕ {label}", True, _TITLE_C)
            self.screen.blit(lbl_s, (x, y))
            bar_w  = 180
            bar_h  = 6
            max_dur = 225.0
            fill    = max(0, min(bar_w, int(bar_w * dur / max_dur)))
            pygame.draw.rect(self.screen, _DARK_BG, (x, y + 14, bar_w, bar_h))
            pygame.draw.rect(self.screen, _ACCENT,   (x, y + 14, fill,  bar_h))
            y += 26

    # ─────────────────────────────────────────────────────────────────────────
    # CODEX (called from collections.py)
    # ─────────────────────────────────────────────────────────────────────────

    def _draw_tea_codex(self, player, gy0=58, gx_off=0):
        from tea import TEA_TYPE_ORDER
        TEA_TYPES = _CODEX_TEA_TYPES
        BIOMES    = _CODEX_BIOMES
        COLS      = len(TEA_TYPES)
        CELL_W, CELL_H, GAP = 96, 64, 4
        HDR_H     = 22
        gx0 = gx_off + (SCREEN_W - gx_off - (COLS * CELL_W + (COLS - 1) * GAP)) // 2

        # Column headers
        hdr_y = gy0
        for ci, t_type in enumerate(TEA_TYPES):
            hx    = gx0 + ci * (CELL_W + GAP)
            tc    = TEA_TYPE_COLORS.get(t_type, _ACCENT)
            lbl   = self.small.render(t_type.upper(), True, tc)
            self.screen.blit(lbl, (hx + CELL_W // 2 - lbl.get_width() // 2, hdr_y + 4))

        self._tea_codex_rects.clear()
        cy = hdr_y + HDR_H - self._tea_codex_scroll

        total_h   = len(BIOMES) * (CELL_H + GAP) + HDR_H
        visible_h = SCREEN_H - gy0 - 10
        self._max_tea_codex_scroll = max(0, total_h - visible_h)

        for biome in BIOMES:
            bnm = BIOME_DISPLAY_NAMES.get(biome, biome)
            bl  = self.font.render(bnm.upper(), True, (140, 200, 120))
            self.screen.blit(bl, (gx0 - bl.get_width() - 8, cy + (CELL_H - bl.get_height()) // 2))

            for ci, t_type in enumerate(TEA_TYPES):
                hx   = gx0 + ci * (CELL_W + GAP)
                key  = f"{biome}_{t_type}"
                disc = key in player.discovered_tea_origins
                rect = pygame.Rect(hx, cy, CELL_W, CELL_H)
                self._tea_codex_rects[key] = rect
                tc   = TEA_TYPE_COLORS.get(t_type, _ACCENT)
                sel  = (self._tea_codex_selected == key)

                if disc:
                    pygame.draw.rect(self.screen, _CELL_BG, rect)
                    pygame.draw.rect(self.screen, tc, rect, 3 if sel else 1)
                    # Best quality for this origin+type
                    best_q = max(
                        (x.steep_quality for x in player.tea_leaves
                         if x.origin_biome == biome and x.tea_type == t_type), default=0.0)
                    stars = "★" * round(best_q * 5) if best_q > 0 else "★"
                    nm_s  = self.small.render(
                        BIOME_DISPLAY_NAMES.get(biome, biome), True, tc)
                    ss_s  = self.small.render(stars, True, (220, 200, 80))
                    self.screen.blit(nm_s, (hx + 4, cy + 6))
                    self.screen.blit(ss_s, (hx + 4, cy + 26))
                    if sel:
                        buff_key = TEA_TYPE_BUFFS.get(t_type, "")
                        buff_desc = BUFF_DESCS.get(buff_key, "")
                        bs = self.small.render(buff_desc, True, (180, 230, 160))
                        self.screen.blit(bs, (hx + 4, cy + 44))
                else:
                    pygame.draw.rect(self.screen, (10, 20, 10), rect)
                    pygame.draw.rect(self.screen, _DIM_C, rect, 1)
                    lock = self.small.render("?", True, (30, 55, 30))
                    self.screen.blit(lock, (hx + CELL_W // 2 - lock.get_width() // 2,
                                            cy + CELL_H // 2 - lock.get_height() // 2))

            cy += CELL_H + GAP

        # Detail panel for selected discovered entry
        if self._tea_codex_selected:
            key = self._tea_codex_selected
            if key in player.discovered_tea_origins:
                parts   = key.rsplit("_", 1)
                if len(parts) == 2:
                    biome, t_type = parts
                    tc  = TEA_TYPE_COLORS.get(t_type, _ACCENT)
                    px0 = SCREEN_W - 300
                    py0 = gy0
                    pygame.draw.rect(self.screen, _DARK_BG, (px0, py0, 290, 260))
                    pygame.draw.rect(self.screen, tc, (px0, py0, 290, 260), 2)

                    iy = py0 + 10
                    def dline(txt, col=_TITLE_C):
                        nonlocal iy
                        s = self.small.render(txt, True, col)
                        self.screen.blit(s, (px0 + 10, iy))
                        iy += 18

                    dline(BIOME_DISPLAY_NAMES.get(biome, biome) + " — " + t_type.title(), tc)
                    dline(TEA_TYPE_DESCS.get(t_type, t_type), (180, 215, 160))
                    buff_key = TEA_TYPE_BUFFS.get(t_type, "")
                    dline("Buff: " + BUFF_DESCS.get(buff_key, ""), (160, 210, 140))
                    best_leaves = [x for x in player.tea_leaves
                                   if x.origin_biome == biome and x.tea_type == t_type]
                    if best_leaves:
                        best = max(best_leaves, key=lambda x: x.steep_quality)
                        dline(f"Best Quality: {'★' * round(best.steep_quality * 5)}", (220, 200, 80))
                        if best.flavor_notes:
                            dline("Notes:", _LABEL_C)
                            for note in best.flavor_notes[:3]:
                                dline(f"  • {note.title()}", _TITLE_C)
