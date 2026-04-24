import pygame
from constants import SCREEN_W, SCREEN_H
from coffee import (make_blend, apply_roast_result, apply_processing,
                    get_brew_output_id, get_brew_duration_multiplier, get_brew_quality_bonus,
                    BREW_METHODS, BUFF_DESCS, BIOME_DISPLAY_NAMES,
                    ROAST_LEVEL_DESCS, ROAST_COLORS,
                    PROCESSING_METHODS, GRIND_SIZES, WATER_QUALITIES)


class CoffeeMixin:

    def _draw_roaster(self, player, dt=0.0):
        from blocks import ROASTER_BLOCK
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("COFFEE ROASTER", True, (210, 145, 60))
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))

        hint = self.small.render("ESC to close", True, (100, 80, 50))
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        if self._roast_phase == "select_bean":
            self._roast_select_rects.clear()
            raw_beans = [(i, b) for i, b in enumerate(player.coffee_beans) if b.state == "raw"]
            if not raw_beans:
                msg = self.font.render("No raw coffee beans! Harvest mature coffee plants.", True, (130, 100, 60))
                self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2))
                return
            sub = self.small.render("Select a raw bean to roast:", True, (180, 140, 60))
            self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 32))
            CELL_W, CELL_H, GAP, COLS = 200, 56, 8, 5
            gx0 = (SCREEN_W - (COLS * CELL_W + (COLS - 1) * GAP)) // 2
            for li, (bi, bean) in enumerate(raw_beans[:20]):
                col_i = li % COLS
                row_i = li // COLS
                rx = gx0 + col_i * (CELL_W + GAP)
                ry = 55 + row_i * (CELL_H + GAP)
                rect = pygame.Rect(rx, ry, CELL_W, CELL_H)
                self._roast_select_rects[bi] = rect
                pygame.draw.rect(self.screen, (45, 28, 10), rect)
                pygame.draw.rect(self.screen, (140, 90, 35), rect, 2)
                nm = BIOME_DISPLAY_NAMES.get(bean.origin_biome, bean.origin_biome)
                ns = self.small.render(nm + " " + bean.variety.title(), True, (220, 170, 80))
                self.screen.blit(ns, (rx + 6, ry + 8))
                hint2 = self.small.render("Click to roast", True, (110, 80, 40))
                self.screen.blit(hint2, (rx + 6, ry + 26))

        elif self._roast_phase == "select_processing":
            self._roast_proc_rects.clear()
            sub = self.small.render("Choose a processing method:", True, (180, 140, 60))
            self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 32))
            BTN_W, BTN_H, BTN_GAP = 320, 80, 14
            total_w = len(PROCESSING_METHODS) * BTN_W + (len(PROCESSING_METHODS) - 1) * BTN_GAP
            gx0 = (SCREEN_W - total_w) // 2
            for pi, (pkey, pdata) in enumerate(PROCESSING_METHODS.items()):
                px = gx0 + pi * (BTN_W + BTN_GAP)
                py = SCREEN_H // 2 - BTN_H // 2
                prect = pygame.Rect(px, py, BTN_W, BTN_H)
                self._roast_proc_rects[pkey] = prect
                pygame.draw.rect(self.screen, (40, 25, 8), prect)
                pygame.draw.rect(self.screen, (170, 115, 45), prect, 2)
                lbl = self.font.render(pdata["label"], True, (230, 180, 80))
                self.screen.blit(lbl, (px + BTN_W // 2 - lbl.get_width() // 2, py + 10))
                desc_lines = pdata["desc"].split(". ")
                for di, dl in enumerate(desc_lines[:2]):
                    ds = self.small.render(dl, True, (160, 125, 60))
                    self.screen.blit(ds, (px + 8, py + 38 + di * 16))

        elif self._roast_phase == "roasting":
            # Update physics
            if self._roast_heat_held:
                self._roast_temp_vel = min(1.0, self._roast_temp_vel + 0.020)
            else:
                self._roast_temp_vel = max(-0.5, self._roast_temp_vel - 0.010)
            self._roast_temp = max(0.0, min(1.0, self._roast_temp + self._roast_temp_vel * dt))
            self._roast_time += dt

            if 0.30 <= self._roast_temp <= 0.80:
                self._roast_time_in_band += dt

            if not self._roast_first_crack_hit and self._roast_time >= 10.0:
                self._roast_first_crack_hit = True
                self._roast_event_flash = ("FIRST CRACK!", (240, 220, 80), 2.0)
            if not self._roast_second_crack_hit and self._roast_time >= 22.0:
                self._roast_second_crack_hit = True
                self._roast_event_flash = ("SECOND CRACK!", (240, 80, 60), 2.0)
            if self._roast_second_crack_hit and self._roast_temp > 0.80:
                self._roast_penalties = min(5, self._roast_penalties + int(dt))
            if self._roast_event_flash:
                txt, col, timer = self._roast_event_flash
                timer -= dt
                if timer <= 0:
                    self._roast_event_flash = None
                else:
                    self._roast_event_flash = (txt, col, timer)

            # Draw temperature bar
            BAR_X, BAR_Y, BAR_W, BAR_H = 80, 60, 30, SCREEN_H - 180
            pygame.draw.rect(self.screen, (25, 15, 5), (BAR_X, BAR_Y, BAR_W, BAR_H))
            pygame.draw.rect(self.screen, (60, 40, 20), (BAR_X, BAR_Y, BAR_W, BAR_H), 2)
            # Zone bands
            def _zone_y(v): return BAR_Y + BAR_H - int(BAR_H * v)
            pygame.draw.rect(self.screen, (30, 70, 30),
                             (BAR_X, _zone_y(0.65), BAR_W, _zone_y(0.40) - _zone_y(0.65)))  # green
            pygame.draw.rect(self.screen, (70, 70, 20),
                             (BAR_X, _zone_y(0.80), BAR_W, _zone_y(0.65) - _zone_y(0.80)))  # yellow
            pygame.draw.rect(self.screen, (80, 20, 10),
                             (BAR_X, _zone_y(1.00), BAR_W, _zone_y(0.80) - _zone_y(1.00)))  # red
            # Temp marker
            marker_y = _zone_y(self._roast_temp)
            marker_col = (255, 120, 40) if self._roast_temp > 0 else (80, 80, 80)
            pygame.draw.rect(self.screen, marker_col, (BAR_X - 6, marker_y - 4, BAR_W + 12, 8))
            temp_lbl = self.small.render(f"{self._roast_temp:.0%}", True, marker_col)
            self.screen.blit(temp_lbl, (BAR_X + BAR_W + 4, marker_y - 6))

            # Labels
            for v, lbl in [(0.25, "Light"), (0.45, "Medium"), (0.65, "Dark"), (0.80, "Charred")]:
                yl = _zone_y(v)
                s = self.small.render(lbl, True, (140, 100, 60))
                self.screen.blit(s, (BAR_X - s.get_width() - 4, yl - 6))
                pygame.draw.line(self.screen, (60, 40, 20), (BAR_X, yl), (BAR_X + BAR_W, yl), 1)

            # Time bar
            TIME_X, TIME_Y = 130, SCREEN_H - 110
            TIME_W = SCREEN_W - 260
            pygame.draw.rect(self.screen, (25, 15, 5), (TIME_X, TIME_Y, TIME_W, 18))
            pygame.draw.rect(self.screen, (60, 40, 20), (TIME_X, TIME_Y, TIME_W, 18), 2)
            prog = min(1.0, self._roast_time / self._roast_total_time)
            progress_col = (180, 120, 40)
            pygame.draw.rect(self.screen, progress_col, (TIME_X, TIME_Y, int(TIME_W * prog), 18))
            for t_mark, t_lbl in [(10, "1st crack"), (22, "2nd crack")]:
                tx = TIME_X + int(TIME_W * t_mark / self._roast_total_time)
                pygame.draw.line(self.screen, (220, 180, 80), (tx, TIME_Y - 4), (tx, TIME_Y + 22), 2)
                ms = self.small.render(t_lbl, True, (200, 160, 60))
                self.screen.blit(ms, (tx - ms.get_width() // 2, TIME_Y - 18))
            ts = self.small.render(f"{self._roast_time:.1f}s / {self._roast_total_time:.0f}s", True, (180, 140, 60))
            self.screen.blit(ts, (TIME_X + TIME_W // 2 - ts.get_width() // 2, TIME_Y + 22))

            # Event flash
            if self._roast_event_flash:
                txt, col, _ = self._roast_event_flash
                ef = self.font.render(txt, True, col)
                self.screen.blit(ef, (SCREEN_W // 2 - ef.get_width() // 2, SCREEN_H // 2 - 20))

            # Instruction
            inst = self.small.render("Hold SPACE / click HEAT to raise temp.  Press ENTER / click STOP to finish.", True, (140, 110, 60))
            self.screen.blit(inst, (SCREEN_W // 2 - inst.get_width() // 2, TIME_Y - 36))

            # STOP button
            stop_rect = pygame.Rect(SCREEN_W - 150, SCREEN_H - 110, 130, 32)
            pygame.draw.rect(self.screen, (80, 35, 10), stop_rect)
            pygame.draw.rect(self.screen, (200, 100, 40), stop_rect, 2)
            stop_lbl = self.font.render("STOP", True, (240, 160, 60))
            self.screen.blit(stop_lbl, (stop_rect.centerx - stop_lbl.get_width() // 2,
                                        stop_rect.centery - stop_lbl.get_height() // 2))
            self._roast_stop_btn = stop_rect

            # HEAT button
            heat_rect = pygame.Rect(SCREEN_W - 150, SCREEN_H - 150, 130, 32)
            hcol = (120, 50, 15) if not self._roast_heat_held else (180, 80, 20)
            pygame.draw.rect(self.screen, hcol, heat_rect)
            pygame.draw.rect(self.screen, (220, 120, 50), heat_rect, 2)
            hl = self.font.render("HEAT", True, (255, 200, 80))
            self.screen.blit(hl, (heat_rect.centerx - hl.get_width() // 2,
                                  heat_rect.centery - hl.get_height() // 2))
            self._roast_heat_btn = heat_rect

        elif self._roast_phase == "result":
            bean = player.coffee_beans[self._roast_bean_idx]
            roast_col = ROAST_COLORS.get(bean.roast_level, (140, 80, 30))
            cx2, cy2 = SCREEN_W // 2, 80
            # Bean preview
            bean_surf = pygame.Surface((100, 100), pygame.SRCALPHA)
            bean_surf.fill((0, 0, 0, 0))
            pygame.draw.ellipse(bean_surf, roast_col, (10, 5, 80, 90))
            lc = (max(0, roast_col[0] - 50), max(0, roast_col[1] - 50), max(0, roast_col[2] - 50))
            pygame.draw.line(bean_surf, lc, (50, 8), (50, 92), 4)
            self.screen.blit(bean_surf, (cx2 - 50, cy2))

            iy2 = cy2 + 115
            def rline(txt, col=(210, 160, 80)):
                nonlocal iy2
                s = self.font.render(txt, True, col)
                self.screen.blit(s, (cx2 - s.get_width() // 2, iy2))
                iy2 += 26

            rline(BIOME_DISPLAY_NAMES.get(bean.origin_biome, bean.origin_biome) + " " + bean.variety.title(), (230, 175, 90))
            if bean.processing_method:
                pm = PROCESSING_METHODS.get(bean.processing_method, {})
                rline(pm.get("label", bean.processing_method) + " Process", (170, 195, 120))
            rline(ROAST_LEVEL_DESCS.get(bean.roast_level, bean.roast_level), roast_col)
            stars = "★" * round(bean.roast_quality * 5) + "☆" * (5 - round(bean.roast_quality * 5))
            rline(stars, (220, 190, 60))
            if bean.flavor_notes:
                rline("Flavour Notes:", (180, 140, 70))
                for note in bean.flavor_notes:
                    rline(f"  • {note.title()}", (210, 175, 100))

            done_rect = pygame.Rect(cx2 - 70, iy2 + 20, 140, 34)
            pygame.draw.rect(self.screen, (50, 35, 10), done_rect)
            pygame.draw.rect(self.screen, (180, 130, 50), done_rect, 2)
            dl = self.font.render("DONE", True, (220, 180, 80))
            self.screen.blit(dl, (done_rect.centerx - dl.get_width() // 2,
                                  done_rect.centery - dl.get_height() // 2))
            self._roast_result_done_btn = done_rect

    def _handle_roaster_click(self, pos, player):
        keys = pygame.key.get_pressed()
        if self._roast_phase == "select_bean":
            for bi, rect in self._roast_select_rects.items():
                if rect.collidepoint(pos):
                    bean = player.coffee_beans[bi]
                    if bean.state == "raw":
                        self._roast_bean_idx = bi
                        self._roast_phase = "select_processing"
                    return
        elif self._roast_phase == "select_processing":
            for pkey, prect in self._roast_proc_rects.items():
                if prect.collidepoint(pos):
                    bi = self._roast_bean_idx
                    if bi is not None and bi < len(player.coffee_beans):
                        bean = player.coffee_beans[bi]
                        apply_processing(bean, pkey)
                        self._roast_time = 0.0
                        self._roast_temp = 0.0
                        self._roast_temp_vel = 0.0
                        self._roast_time_in_band = 0.0
                        self._roast_first_crack_hit = False
                        self._roast_second_crack_hit = False
                        self._roast_penalties = 0
                        self._roast_event_flash = None
                        self._roast_heat_held = False
                        self._roast_phase = "roasting"
                    return
        elif self._roast_phase == "roasting":
            if hasattr(self, '_roast_stop_btn') and self._roast_stop_btn and self._roast_stop_btn.collidepoint(pos):
                self._finish_roast(player)
                return
            if hasattr(self, '_roast_heat_btn') and self._roast_heat_btn and self._roast_heat_btn.collidepoint(pos):
                self._roast_heat_held = True
                return
        elif self._roast_phase == "result":
            if self._roast_result_done_btn and self._roast_result_done_btn.collidepoint(pos):
                self._roast_phase = "select_bean"
                self._roast_bean_idx = None
                return

    def handle_roaster_keydown(self, key, player):
        from blocks import ROASTER_BLOCK
        if self.refinery_block_id != ROASTER_BLOCK:
            return
        if self._roast_phase == "roasting":
            if key == pygame.K_RETURN or key == pygame.K_KP_ENTER:
                self._finish_roast(player)

    def handle_roaster_keys(self, keys):
        from blocks import ROASTER_BLOCK
        if self.refinery_block_id != ROASTER_BLOCK:
            return
        if self._roast_phase == "roasting":
            self._roast_heat_held = bool(keys[pygame.K_SPACE])

    def _finish_roast(self, player):
        idx = self._roast_bean_idx
        if idx is None or idx >= len(player.coffee_beans):
            self._roast_phase = "select_bean"
            return
        bean = player.coffee_beans[idx]
        timing_score = min(1.0, self._roast_time_in_band / max(0.1, self._roast_time))
        temp_ctrl    = self._roast_time_in_band / max(0.1, self._roast_total_time)
        apply_roast_result(bean, self._roast_temp, timing_score, temp_ctrl, self._roast_penalties)
        if getattr(player, 'roast_quality_bonus', 0.0) > 0:
            bean.roast_quality = min(1.0, bean.roast_quality * (1.0 + player.roast_quality_bonus))
        player.discovered_coffee_origins.add(f"{bean.origin_biome}_{bean.roast_level}")
        self._roast_phase = "result"

    # ------------------------------------------------------------------

    def _draw_blend_station(self, player):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("BLEND STATION", True, (200, 155, 80))
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, (100, 80, 50))
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        if self._blend_phase == "result":
            bean = self._blend_result_bean
            if bean:
                roast_col = ROAST_COLORS.get(bean.roast_level, (140, 80, 30))
                cx2, cy2 = SCREEN_W // 2, 60
                bean_surf = pygame.Surface((90, 90), pygame.SRCALPHA)
                bean_surf.fill((0, 0, 0, 0))
                pygame.draw.ellipse(bean_surf, roast_col, (8, 5, 74, 80))
                pygame.draw.line(bean_surf, (20, 10, 5), (45, 8), (45, 82), 3)
                self.screen.blit(bean_surf, (cx2 - 45, cy2))
                iy2 = cy2 + 100
                def bline(txt, col=(210, 160, 80)):
                    nonlocal iy2
                    s = self.font.render(txt, True, col)
                    self.screen.blit(s, (cx2 - s.get_width() // 2, iy2))
                    iy2 += 26
                bline("Blend Created!", (220, 180, 90))
                bline(f"Roast: {bean.roast_level.title()}", roast_col)
                if bean.flavor_notes:
                    bline("Flavour Notes:", (180, 140, 70))
                    for note in bean.flavor_notes:
                        bline(f"  {note.title()}", (210, 175, 100))
                done_rect = pygame.Rect(cx2 - 70, iy2 + 15, 140, 34)
                pygame.draw.rect(self.screen, (50, 35, 10), done_rect)
                pygame.draw.rect(self.screen, (180, 130, 50), done_rect, 2)
                dl = self.font.render("DONE", True, (220, 180, 80))
                self.screen.blit(dl, (done_rect.centerx - dl.get_width() // 2,
                                      done_rect.centery - dl.get_height() // 2))
                self._blend_result_done_btn = done_rect
            return

        roasted = [(i, b) for i, b in enumerate(player.coffee_beans) if b.state in ("roasted",)]
        # Left panel: bean list
        LIST_X, LIST_Y, LIST_W = 20, 36, 260
        pygame.draw.rect(self.screen, (20, 12, 5), (LIST_X, LIST_Y, LIST_W, SCREEN_H - LIST_Y - 10))
        pygame.draw.rect(self.screen, (80, 55, 25), (LIST_X, LIST_Y, LIST_W, SCREEN_H - LIST_Y - 10), 1)
        hdr = self.small.render("BEANS (click to fill slot):", True, (160, 120, 50))
        self.screen.blit(hdr, (LIST_X + 4, LIST_Y + 4))
        self._blend_list_rects.clear()
        for li, (bi, bean) in enumerate(roasted[:16]):
            ry = LIST_Y + 24 + li * 28
            rect = pygame.Rect(LIST_X + 4, ry, LIST_W - 8, 24)
            in_slot = bi in self._blend_slots
            pygame.draw.rect(self.screen, (50, 30, 12) if in_slot else (35, 20, 8), rect)
            pygame.draw.rect(self.screen, ROAST_COLORS.get(bean.roast_level, (120, 80, 30)), rect, 1)
            nm = BIOME_DISPLAY_NAMES.get(bean.origin_biome, bean.origin_biome)[:12]
            ns = self.small.render(f"{nm} {bean.roast_level[:3]}", True, (200, 155, 70))
            self.screen.blit(ns, (LIST_X + 8, ry + 4))
            self._blend_list_rects[bi] = rect

        # Right: 3 slots
        SLOT_X0 = LIST_X + LIST_W + 20
        SLOT_W, SLOT_H, SLOT_GAP = 220, 80, 14
        self._blend_slot_rects = []
        sub = self.small.render("BLEND SLOTS (2 required, 3rd optional):", True, (160, 120, 50))
        self.screen.blit(sub, (SLOT_X0, LIST_Y + 4))
        for si in range(3):
            sy = LIST_Y + 28 + si * (SLOT_H + SLOT_GAP)
            srect = pygame.Rect(SLOT_X0, sy, SLOT_W, SLOT_H)
            self._blend_slot_rects.append(srect)
            bi = self._blend_slots[si]
            if bi is not None and bi < len(player.coffee_beans):
                bean = player.coffee_beans[bi]
                rc = ROAST_COLORS.get(bean.roast_level, (120, 80, 30))
                pygame.draw.rect(self.screen, (45, 28, 10), srect)
                pygame.draw.rect(self.screen, rc, srect, 2)
                nm = BIOME_DISPLAY_NAMES.get(bean.origin_biome, bean.origin_biome)
                ns = self.small.render(f"{nm} {bean.variety.title()}", True, (220, 170, 80))
                self.screen.blit(ns, (SLOT_X0 + 6, sy + 8))
                rs = self.small.render(f"Roast: {bean.roast_level.title()}", True, rc)
                self.screen.blit(rs, (SLOT_X0 + 6, sy + 26))
                if bean.flavor_notes:
                    fn = self.small.render(", ".join(bean.flavor_notes[:2]), True, (170, 130, 60))
                    self.screen.blit(fn, (SLOT_X0 + 6, sy + 44))
                clear_s = self.small.render("[X]", True, (180, 80, 60))
                self.screen.blit(clear_s, (SLOT_X0 + SLOT_W - 24, sy + 4))
            else:
                pygame.draw.rect(self.screen, (18, 10, 4), srect)
                pygame.draw.rect(self.screen, (60, 40, 15), srect, 1)
                es = self.small.render(f"Slot {si + 1}  (empty)", True, (80, 55, 25))
                self.screen.blit(es, (SLOT_X0 + 6, sy + 30))

        can_blend = sum(1 for s in self._blend_slots if s is not None) >= 2
        btn_col = (60, 40, 12) if can_blend else (30, 20, 8)
        brd_col = (180, 130, 50) if can_blend else (60, 40, 15)
        blend_btn_rect = pygame.Rect(SLOT_X0, LIST_Y + 28 + 3 * (SLOT_H + SLOT_GAP) + 10, 120, 36)
        pygame.draw.rect(self.screen, btn_col, blend_btn_rect)
        pygame.draw.rect(self.screen, brd_col, blend_btn_rect, 2)
        bl = self.font.render("BLEND", True, (220, 175, 80) if can_blend else (80, 55, 25))
        self.screen.blit(bl, (blend_btn_rect.centerx - bl.get_width() // 2,
                               blend_btn_rect.centery - bl.get_height() // 2))
        self._blend_btn = blend_btn_rect

    def _handle_blend_click(self, pos, player):
        if self._blend_phase == "result":
            if self._blend_result_done_btn and self._blend_result_done_btn.collidepoint(pos):
                self._blend_phase = "select"
                self._blend_result_bean = None
                self._blend_slots = [None, None, None]
            return
        for bi, rect in self._blend_list_rects.items():
            if rect.collidepoint(pos):
                if bi in self._blend_slots:
                    idx = self._blend_slots.index(bi)
                    self._blend_slots[idx] = None
                else:
                    for si in range(3):
                        if self._blend_slots[si] is None:
                            self._blend_slots[si] = bi
                            break
                return
        for si, srect in enumerate(self._blend_slot_rects):
            if srect.collidepoint(pos):
                self._blend_slots[si] = None
                return
        if self._blend_btn and self._blend_btn.collidepoint(pos):
            filled = [s for s in self._blend_slots if s is not None]
            if len(filled) >= 2:
                components = [player.coffee_beans[bi] for bi in filled
                              if bi < len(player.coffee_beans)]
                if len(components) >= 2:
                    blended = make_blend(components)
                    for bi in sorted(filled, reverse=True):
                        player.coffee_beans.pop(bi)
                    player.coffee_beans.append(blended)
                    player.discovered_coffee_origins.add(f"blend_{blended.roast_level}")
                    self._blend_result_bean = blended
                    self._blend_phase = "result"
                    self._blend_slots = [None, None, None]

    # ------------------------------------------------------------------

    def _draw_brew_station(self, player):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("BREW STATION", True, (180, 130, 60))
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, (100, 80, 50))
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        brewable = [(i, b) for i, b in enumerate(player.coffee_beans)
                    if b.state in ("roasted", "blended")]

        # Left panel: bean list
        LIST_X, LIST_Y, LIST_W = 20, 36, 220
        pygame.draw.rect(self.screen, (18, 10, 4), (LIST_X, LIST_Y, LIST_W, SCREEN_H - LIST_Y - 10))
        pygame.draw.rect(self.screen, (70, 50, 20), (LIST_X, LIST_Y, LIST_W, SCREEN_H - LIST_Y - 10), 1)
        hdr = self.small.render("ROASTED BEANS:", True, (150, 110, 45))
        self.screen.blit(hdr, (LIST_X + 4, LIST_Y + 4))
        self._brew_bean_rects.clear()
        for li, (bi, bean) in enumerate(brewable[:16]):
            ry = LIST_Y + 24 + li * 28
            rect = pygame.Rect(LIST_X + 4, ry, LIST_W - 8, 24)
            selected = (self._brew_bean_idx == bi)
            rc = ROAST_COLORS.get(bean.roast_level, (120, 80, 30))
            pygame.draw.rect(self.screen, (55, 35, 12) if selected else (32, 18, 6), rect)
            pygame.draw.rect(self.screen, rc, rect, 2 if selected else 1)
            nm = BIOME_DISPLAY_NAMES.get(bean.origin_biome, bean.origin_biome)[:11]
            proc = f" [{bean.processing_method[:3]}]" if bean.processing_method else ""
            ns = self.small.render(f"{nm} {bean.roast_level[:3]}{proc}", True, (200, 155, 70))
            self.screen.blit(ns, (LIST_X + 8, ry + 4))
            self._brew_bean_rects[bi] = rect

        # Middle: method buttons
        METHOD_X = LIST_X + LIST_W + 12
        METHOD_W, METHOD_H, METHOD_GAP = 220, 66, 8
        self._brew_method_rects.clear()
        for mi, (mkey, mdata) in enumerate(BREW_METHODS.items()):
            my = LIST_Y + 4 + mi * (METHOD_H + METHOD_GAP)
            mrect = pygame.Rect(METHOD_X, my, METHOD_W, METHOD_H)
            self._brew_method_rects[mkey] = mrect
            is_sel = getattr(self, '_brew_selected_method', None) == mkey
            pygame.draw.rect(self.screen, (45, 28, 10) if is_sel else (28, 18, 8), mrect)
            pygame.draw.rect(self.screen, (200, 140, 50) if is_sel else (120, 80, 30), mrect, 2 if is_sel else 1)
            ml = self.font.render(mdata["label"], True, (230, 175, 80) if is_sel else (180, 135, 60))
            self.screen.blit(ml, (METHOD_X + 6, my + 6))
            bs = self.small.render(BUFF_DESCS.get(mdata["buff"], ""), True, (160, 130, 60))
            self.screen.blit(bs, (METHOD_X + 6, my + 28))
            amp = " + ".join(mdata.get("amplifies", ()))
            if amp:
                as2 = self.small.render(f"↑ {amp}", True, (120, 100, 45))
                self.screen.blit(as2, (METHOD_X + 6, my + 46))

        # Grind size selector
        PARAM_X = METHOD_X + METHOD_W + 12
        PARAM_W = 130
        gy = LIST_Y + 4
        gl = self.small.render("GRIND:", True, (150, 115, 50))
        self.screen.blit(gl, (PARAM_X, gy))
        gy += 16
        self._brew_grind_rects.clear()
        for gkey, gdata in GRIND_SIZES.items():
            gr = pygame.Rect(PARAM_X, gy, PARAM_W, 26)
            self._brew_grind_rects[gkey] = gr
            is_sel = self._brew_grind_size == gkey
            pygame.draw.rect(self.screen, (45, 28, 10) if is_sel else (25, 15, 5), gr)
            pygame.draw.rect(self.screen, (180, 130, 50) if is_sel else (80, 55, 20), gr, 2 if is_sel else 1)
            gtxt = self.small.render(gdata["label"], True, (220, 175, 80) if is_sel else (140, 105, 45))
            self.screen.blit(gtxt, (PARAM_X + 6, gy + 5))
            gy += 30

        gy += 8
        wl = self.small.render("WATER:", True, (150, 115, 50))
        self.screen.blit(wl, (PARAM_X, gy))
        gy += 16
        self._brew_water_rects.clear()
        for wkey, wdata in WATER_QUALITIES.items():
            wr = pygame.Rect(PARAM_X, gy, PARAM_W, 26)
            self._brew_water_rects[wkey] = wr
            is_sel = self._brew_water_quality == wkey
            pygame.draw.rect(self.screen, (10, 25, 45) if is_sel else (5, 15, 25), wr)
            pygame.draw.rect(self.screen, (80, 160, 220) if is_sel else (40, 80, 120), wr, 2 if is_sel else 1)
            wtxt = self.small.render(wdata["label"], True, (160, 210, 240) if is_sel else (80, 130, 170))
            self.screen.blit(wtxt, (PARAM_X + 6, gy + 5))
            gy += 30

        # Duration preview
        dm = get_brew_duration_multiplier(self._brew_water_quality, self._brew_grind_size)
        gy += 6
        prev = self.small.render(f"Duration: ×{dm:.2f}", True, (140, 170, 140))
        self.screen.blit(prev, (PARAM_X, gy))

        # BREW button
        can_brew = self._brew_bean_idx is not None and hasattr(self, '_brew_selected_method') and self._brew_selected_method
        brew_y = gy + 26
        brew_rect = pygame.Rect(PARAM_X, brew_y, PARAM_W, 36)
        pygame.draw.rect(self.screen, (55, 35, 10) if can_brew else (25, 15, 5), brew_rect)
        pygame.draw.rect(self.screen, (180, 130, 50) if can_brew else (60, 40, 15), brew_rect, 2)
        bwl = self.font.render("BREW", True, (220, 175, 80) if can_brew else (80, 55, 25))
        self.screen.blit(bwl, (brew_rect.centerx - bwl.get_width() // 2,
                                brew_rect.centery - bwl.get_height() // 2))
        self._brew_btn = brew_rect

        # Far right: selected bean details
        DX = PARAM_X + PARAM_W + 12
        DW = SCREEN_W - DX - 8
        if DW > 60 and self._brew_bean_idx is not None and self._brew_bean_idx < len(player.coffee_beans):
            bean = player.coffee_beans[self._brew_bean_idx]
            pygame.draw.rect(self.screen, (20, 12, 5), (DX, LIST_Y, DW, SCREEN_H - LIST_Y - 10))
            pygame.draw.rect(self.screen, ROAST_COLORS.get(bean.roast_level, (100, 60, 20)),
                             (DX, LIST_Y, DW, SCREEN_H - LIST_Y - 10), 1)
            iy2 = LIST_Y + 8
            def dline2(txt, col=(200, 155, 70)):
                nonlocal iy2
                s = self.small.render(txt, True, col)
                self.screen.blit(s, (DX + 4, iy2))
                iy2 += 14
            dline2(BIOME_DISPLAY_NAMES.get(bean.origin_biome, bean.origin_biome), (220, 170, 80))
            if bean.processing_method:
                pm = PROCESSING_METHODS.get(bean.processing_method, {})
                dline2(pm.get("label", bean.processing_method) + " Process", (160, 195, 120))
            dline2(bean.roast_level.title(), ROAST_COLORS.get(bean.roast_level, (140, 90, 40)))
            stars = "★" * round(bean.roast_quality * 5)
            dline2(stars, (220, 190, 60))
            for note in bean.flavor_notes:
                dline2(f"• {note.title()}", (200, 160, 80))

    def _handle_brew_click(self, pos, player):
        for bi, rect in self._brew_bean_rects.items():
            if rect.collidepoint(pos):
                self._brew_bean_idx = bi if self._brew_bean_idx != bi else None
                return
        for gkey, grect in self._brew_grind_rects.items():
            if grect.collidepoint(pos):
                self._brew_grind_size = gkey
                return
        for wkey, wrect in self._brew_water_rects.items():
            if wrect.collidepoint(pos):
                self._brew_water_quality = wkey
                return
        for mkey, mrect in self._brew_method_rects.items():
            if mrect.collidepoint(pos):
                self._brew_selected_method = mkey
                return
        if self._brew_btn and self._brew_btn.collidepoint(pos):
            mkey = getattr(self, '_brew_selected_method', None)
            if mkey and self._brew_bean_idx is not None and self._brew_bean_idx < len(player.coffee_beans):
                bean = player.coffee_beans[self._brew_bean_idx]
                quality_bonus = get_brew_quality_bonus(self._brew_water_quality)
                effective_quality = min(1.0, bean.roast_quality + quality_bonus)
                output_id = get_brew_output_id(mkey, effective_quality)
                dur_mult = get_brew_duration_multiplier(self._brew_water_quality, self._brew_grind_size)
                player.coffee_beans.pop(self._brew_bean_idx)
                self._brew_bean_idx = None
                from items import ITEMS
                base_dur = ITEMS.get(output_id, {}).get("coffee_buff_duration", 60.0)
                final_dur = base_dur * dur_mult
                item_data = ITEMS.get(output_id, {})
                player._add_item(output_id)
                if item_data.get("coffee_buff"):
                    player.active_buffs[item_data["coffee_buff"]] = {
                        "duration": final_dur, "intensity": 1.0
                    }

    # ------------------------------------------------------------------
    # Coffee buff HUD
    # ------------------------------------------------------------------

    def _draw_coffee_buffs(self, player):
        if not player.active_buffs:
            return
        BUFF_COLORS = {
            "focus":     (80,  180, 80),
            "rush":      (80,  120, 220),
            "clarity":   (180, 220, 80),
            "endurance": (80,  200, 160),
            "strength":  (220, 80,  80),
        }
        bx = SCREEN_W - 8
        by = 60
        for buff, data in player.active_buffs.items():
            dur = data["duration"]
            col = BUFF_COLORS.get(buff, (180, 180, 80))
            label = f"{buff.upper()} {dur:.0f}s"
            s = self.small.render(label, True, col)
            bx2 = bx - s.get_width() - 4
            pygame.draw.rect(self.screen, (15, 15, 20),
                             (bx2 - 4, by - 2, s.get_width() + 8, s.get_height() + 4))
            pygame.draw.rect(self.screen, col,
                             (bx2 - 4, by - 2, s.get_width() + 8, s.get_height() + 4), 1)
            self.screen.blit(s, (bx2, by))
            by += s.get_height() + 6
