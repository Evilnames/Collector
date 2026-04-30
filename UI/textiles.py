import pygame
from constants import SCREEN_W, SCREEN_H
from textiles import (
    FIBER_PROFILES, TEXTURE_PATTERNS, DYE_FAMILY_COLORS, DYE_FAMILY_DISPLAY,
    GARMENT_BUFFS, GARMENT_BUFF_DESCS, GARMENT_MAX_BONUS, OUTPUT_DISPLAY,
    apply_dye, apply_weave, output_item_key, discovery_key, dye_family_from_color,
    TOTAL_TEXTILE_TYPES,
)

_ACCENT  = (160,  90, 190)
_DARK_BG = ( 18,  10,  22)
_CELL_BG = ( 28,  16,  35)
_TITLE_C = (220, 160, 250)
_LABEL_C = (175, 130, 210)
_DIM_C   = ( 90,  60, 110)
_HINT_C  = (120,  90, 145)

_SPIN_DURATION   = 20.0  # seconds per spin session
_SPIN_TARGET_LO  = 0.35
_SPIN_TARGET_HI  = 0.72

_LOOM_GRID_COLS  = 5
_LOOM_GRID_ROWS  = 4
_LOOM_CELL_W     = 44
_LOOM_CELL_H     = 44
_LOOM_CELL_GAP   = 6
_LOOM_CLICK_WINDOW = 2.5  # seconds the active cell stays clickable

# Short description of each fiber's passive bonus when worn
_FIBER_INTRINSIC_DESCS = {
    "silk":     "Lucky Drop: +8% chance to double a block drop per piece",
    "cashmere": "HP Regen: +0.4 HP/s per piece when not hungry",
    "jute":     "Move Hunger: -8% hunger drain while moving per piece",
    "wool":     "Warmth: +6% extra cold resistance per piece",
    "linen":    "Day Speed: +4% movement speed during daytime per piece",
    "cotton":   "Jump: +5% jump force per piece",
    "blend":    "No fiber intrinsic bonus",
}


class TextileMixin:

    # ─────────────────────────────────────────────────────────────────────────
    # SPINNING WHEEL
    # ─────────────────────────────────────────────────────────────────────────

    def _draw_spinning_wheel(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("SPINNING WHEEL", True, _TITLE_C)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, _HINT_C)
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        if self._spin_phase == "select_fiber":
            self._spin_fiber_rects.clear()
            sub = self.small.render("Select fiber to spin:", True, _LABEL_C)
            self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 34))

            fibers = []
            if player.inventory.get("wool", 0) > 0:
                fibers.append(("wool", "Wool", f"x{player.inventory['wool']}"))
            if player.inventory.get("flax_fiber", 0) > 0:
                fibers.append(("linen", "Flax Fiber", f"x{player.inventory['flax_fiber']}"))
            if player.inventory.get("wool", 0) > 0 and player.inventory.get("flax_fiber", 0) > 0:
                fibers.append(("blend", "Wool + Flax (Blend)", "1 of each"))
            if player.inventory.get("silk_thread", 0) > 0:
                fibers.append(("silk", "Silk Thread", f"x{player.inventory['silk_thread']}"))
            if player.inventory.get("cashmere_fiber", 0) > 0:
                fibers.append(("cashmere", "Cashmere Fiber", f"x{player.inventory['cashmere_fiber']}"))
            if player.inventory.get("jute_fiber", 0) > 0:
                fibers.append(("jute", "Jute Fiber", f"x{player.inventory['jute_fiber']}"))

            if not fibers:
                msg = self.font.render("No fiber! Shear Sheep for wool, grow Flax/Jute, or collect Silk.", True, _LABEL_C)
                self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2))
                return

            BTN_W, BTN_H, BTN_GAP = 240, 90, 16
            FIBER_COLS = 4
            rows = (len(fibers) + FIBER_COLS - 1) // FIBER_COLS
            total_w = min(len(fibers), FIBER_COLS) * BTN_W + (min(len(fibers), FIBER_COLS) - 1) * BTN_GAP
            gx0 = (SCREEN_W - total_w) // 2
            gy0 = SCREEN_H // 2 - (rows * (BTN_H + BTN_GAP)) // 2
            for fi, (ftype, flabel, fcount) in enumerate(fibers):
                col_i, row_i = fi % FIBER_COLS, fi // FIBER_COLS
                px = gx0 + col_i * (BTN_W + BTN_GAP)
                py = gy0 + row_i * (BTN_H + BTN_GAP)
                prect = pygame.Rect(px, py, BTN_W, BTN_H)
                self._spin_fiber_rects[ftype] = prect
                pygame.draw.rect(self.screen, _CELL_BG, prect)
                pygame.draw.rect(self.screen, _ACCENT, prect, 2)
                lbl = self.font.render(flabel, True, _TITLE_C)
                self.screen.blit(lbl, (px + BTN_W // 2 - lbl.get_width() // 2, py + 12))
                cnt = self.small.render(fcount, True, _LABEL_C)
                self.screen.blit(cnt, (px + BTN_W // 2 - cnt.get_width() // 2, py + 44))
                prof = FIBER_PROFILES.get(ftype, {})
                soft_s = self.small.render(f"Softness {prof.get('softness',0):.0%}  Luster {prof.get('luster',0):.0%}", True, _DIM_C)
                self.screen.blit(soft_s, (px + BTN_W // 2 - soft_s.get_width() // 2, py + 63))

        elif self._spin_phase == "spinning":
            # Advance timer and tension physics
            if dt > 0:
                if self._spin_held:
                    self._spin_tension = min(1.0, self._spin_tension + dt * 0.45)
                else:
                    self._spin_tension = max(0.0, self._spin_tension - dt * 0.30)
                in_zone = _SPIN_TARGET_LO <= self._spin_tension <= _SPIN_TARGET_HI
                if in_zone:
                    self._spin_quality = min(1.0, self._spin_quality + dt * (1.0 / _SPIN_DURATION))
                self._spin_time += dt
                if self._spin_time >= _SPIN_DURATION:
                    self._finish_spinning(player)
                    return

            cx = SCREEN_W // 2
            # Progress bar
            prog = self._spin_time / _SPIN_DURATION
            bar_w, bar_h = 320, 16
            bx0, by0 = cx - bar_w // 2, 35
            pygame.draw.rect(self.screen, _CELL_BG, (bx0, by0, bar_w, bar_h))
            pygame.draw.rect(self.screen, _ACCENT, (bx0, by0, int(bar_w * prog), bar_h))
            pygame.draw.rect(self.screen, _DIM_C, (bx0, by0, bar_w, bar_h), 1)
            pt = self.small.render(f"Time: {_SPIN_DURATION - self._spin_time:.1f}s", True, _LABEL_C)
            self.screen.blit(pt, (bx0, by0 - 18))

            # Tension bar (vertical)
            tb_x, tb_y, tb_w, tb_h = cx - 20, 80, 40, 260
            pygame.draw.rect(self.screen, _CELL_BG, (tb_x, tb_y, tb_w, tb_h))
            # Target zone
            tz_y0 = tb_y + int(tb_h * (1.0 - _SPIN_TARGET_HI))
            tz_y1 = tb_y + int(tb_h * (1.0 - _SPIN_TARGET_LO))
            pygame.draw.rect(self.screen, (50, 140, 60), (tb_x, tz_y0, tb_w, tz_y1 - tz_y0))
            # Tension fill
            fill_h = int(tb_h * self._spin_tension)
            fill_col = (160, 90, 190) if _SPIN_TARGET_LO <= self._spin_tension <= _SPIN_TARGET_HI else (200, 60, 60)
            pygame.draw.rect(self.screen, fill_col, (tb_x, tb_y + tb_h - fill_h, tb_w, fill_h))
            pygame.draw.rect(self.screen, _DIM_C, (tb_x, tb_y, tb_w, tb_h), 1)

            zone_lbl = self.small.render("Target zone", True, (100, 200, 110))
            self.screen.blit(zone_lbl, (tb_x + tb_w + 8, tz_y0 + (tz_y1 - tz_y0) // 2 - 8))

            # Quality so far
            q_lbl = self.small.render(f"Quality: {self._spin_quality:.0%}", True, _TITLE_C)
            self.screen.blit(q_lbl, (cx - q_lbl.get_width() // 2, tb_y + tb_h + 14))

            key_hint = self.font.render("Hold SPACE — keep tension in the green zone", True, _LABEL_C)
            self.screen.blit(key_hint, (cx - key_hint.get_width() // 2, tb_y + tb_h + 44))

            fiber_lbl = self.small.render(f"Spinning: {self._spin_fiber_type.title()}", True, _HINT_C)
            self.screen.blit(fiber_lbl, (cx - fiber_lbl.get_width() // 2, 58))

        elif self._spin_phase == "result":
            thread = player.textiles[-1] if player.textiles else None
            if not thread:
                self._spin_phase = "select_fiber"
                return
            cx, cy = SCREEN_W // 2, 80
            pygame.draw.circle(self.screen, _ACCENT, (cx, cy + 40), 36)
            pygame.draw.circle(self.screen, _CELL_BG, (cx, cy + 40), 36, 3)
            iy = cy + 100

            def rline(txt, col=_TITLE_C):
                nonlocal iy
                s = self.font.render(txt, True, col)
                self.screen.blit(s, (cx - s.get_width() // 2, iy))
                iy += 28

            rline(f"{thread.fiber_type.title()} Thread")
            rline(f"Quality: {thread.quality:.0%}", _LABEL_C)
            rline(f"Softness: {thread.softness:.0%}  Luster: {thread.luster:.0%}", _DIM_C)

            if self._spin_result_btn is None:
                bw, bh = 180, 38
                self._spin_result_btn = pygame.Rect(cx - bw // 2, iy + 12, bw, bh)
            pygame.draw.rect(self.screen, _ACCENT, self._spin_result_btn)
            pygame.draw.rect(self.screen, _TITLE_C, self._spin_result_btn, 2)
            done = self.font.render("Done", True, (255, 255, 255))
            self.screen.blit(done, (self._spin_result_btn.centerx - done.get_width() // 2,
                                    self._spin_result_btn.centery - done.get_height() // 2))

    def _finish_spinning(self, player):
        ftype = self._spin_fiber_type
        # Consume inventory
        if ftype == "blend":
            player.inventory["wool"] = max(0, player.inventory.get("wool", 0) - 1)
            player.inventory["flax_fiber"] = max(0, player.inventory.get("flax_fiber", 0) - 1)
        elif ftype == "linen":
            player.inventory["flax_fiber"] = max(0, player.inventory.get("flax_fiber", 0) - 1)
        elif ftype == "silk":
            player.inventory["silk_thread"] = max(0, player.inventory.get("silk_thread", 0) - 1)
        elif ftype == "cashmere":
            player.inventory["cashmere_fiber"] = max(0, player.inventory.get("cashmere_fiber", 0) - 1)
        elif ftype == "jute":
            player.inventory["jute_fiber"] = max(0, player.inventory.get("jute_fiber", 0) - 1)
        else:  # wool
            player.inventory["wool"] = max(0, player.inventory.get("wool", 0) - 1)
        thread = player._textile_gen.generate(ftype)
        thread.quality = self._spin_quality
        precision_bonus = player.get_textile_bonus("precision")
        if precision_bonus > 0:
            thread.quality = min(1.0, thread.quality + precision_bonus * 0.5)
        player.textiles.append(thread)
        self._spin_phase = "result"
        self._spin_result_btn = None

    def handle_spinning_wheel_keydown(self, key, player):
        if key == pygame.K_ESCAPE:
            self.refinery_open = False
        elif key == pygame.K_SPACE and self._spin_phase == "spinning":
            pass  # held handled in handle_spinning_wheel_keys

    def handle_spinning_wheel_keys(self, keys, dt, player):
        self._spin_held = bool(keys[pygame.K_SPACE])

    def _handle_spinning_wheel_click(self, pos, player):
        if self._spin_phase == "select_fiber":
            for ftype, rect in self._spin_fiber_rects.items():
                if rect.collidepoint(pos):
                    self._spin_fiber_type = ftype
                    self._spin_phase = "spinning"
                    self._spin_time = 0.0
                    self._spin_tension = 0.0
                    self._spin_quality = 0.0
                    self._spin_held = False
                    return
        elif self._spin_phase == "result":
            if self._spin_result_btn and self._spin_result_btn.collidepoint(pos):
                self._spin_phase = "select_fiber"
                self._spin_result_btn = None

    # ─────────────────────────────────────────────────────────────────────────
    # DYE VAT
    # ─────────────────────────────────────────────────────────────────────────

    def _draw_dye_vat(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("DYE VAT", True, _TITLE_C)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, _HINT_C)
        self.screen.blit(hint, (SCREEN_W - hint.get_width() // 2 - 8, 6))

        # Tab bar
        self._dye_tab_rects = {}
        tab_labels = [("extract", "Extract Dye"), ("dye", "Dye Thread")]
        tw, th, tgap = 180, 30, 6
        tx0 = SCREEN_W // 2 - (len(tab_labels) * tw + (len(tab_labels) - 1) * tgap) // 2
        for ti, (tkey, tlabel) in enumerate(tab_labels):
            tr = pygame.Rect(tx0 + ti * (tw + tgap), 30, tw, th)
            self._dye_tab_rects[tkey] = tr
            col = _ACCENT if self._dye_tab == tkey else _CELL_BG
            pygame.draw.rect(self.screen, col, tr)
            pygame.draw.rect(self.screen, _DIM_C, tr, 1)
            ts = self.small.render(tlabel, True, _TITLE_C if self._dye_tab == tkey else _LABEL_C)
            self.screen.blit(ts, (tr.centerx - ts.get_width() // 2, tr.centery - ts.get_height() // 2))

        if self._dye_tab == "extract":
            self._draw_dye_extract_tab(player)
        else:
            self._draw_dye_thread_tab(player)

    def _draw_dye_extract_tab(self, player):
        self._dye_flower_rects.clear()
        sub = self.small.render("Select a wildflower specimen to extract dye from:", True, _LABEL_C)
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 68))

        if not player.wildflowers:
            msg = self.font.render("No wildflowers collected!", True, _LABEL_C)
            self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2))
            return

        CELL_W, CELL_H, GAP, COLS = 190, 58, 8, 6
        gx0 = (SCREEN_W - (COLS * CELL_W + (COLS - 1) * GAP)) // 2
        scroll = getattr(self, "_dye_flower_scroll", 0)
        visible = player.wildflowers[scroll: scroll + COLS * 4]
        for li, wf in enumerate(visible):
            col_i, row_i = li % COLS, li // COLS
            rx = gx0 + col_i * (CELL_W + GAP)
            ry = 88 + row_i * (CELL_H + GAP)
            rect = pygame.Rect(rx, ry, CELL_W, CELL_H)
            self._dye_flower_rects[scroll + li] = rect
            fam = dye_family_from_color(wf.primary_color)
            fam_col = tuple(DYE_FAMILY_COLORS.get(fam, [200, 180, 160]))
            pygame.draw.rect(self.screen, _CELL_BG, rect)
            pygame.draw.rect(self.screen, fam_col, rect, 2)
            nm = self.small.render(wf.flower_type.replace("_", " ").title(), True, _TITLE_C)
            self.screen.blit(nm, (rx + 5, ry + 6))
            fam_s = self.small.render(f"→ {DYE_FAMILY_DISPLAY.get(fam, fam).title()} dye", True, fam_col)
            self.screen.blit(fam_s, (rx + 5, ry + 24))
            rar = self.small.render(wf.rarity.title(), True, _DIM_C)
            self.screen.blit(rar, (rx + 5, ry + 41))

    def _draw_dye_thread_tab(self, player):
        self._dye_thread_rects.clear()
        self._dye_extract_rects.clear()

        threads = [(i, t) for i, t in enumerate(player.textiles) if t.state == "thread"]
        if not threads:
            msg = self.font.render("No thread! Spin fiber at the Spinning Wheel first.", True, _LABEL_C)
            self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2))
            return

        # Thread list (left half)
        sub_t = self.small.render("Select thread:", True, _LABEL_C)
        self.screen.blit(sub_t, (40, 68))
        CELL_W, CELL_H, GAP = 220, 52, 6
        for li, (bi, t) in enumerate(threads[:8]):
            ry = 88 + li * (CELL_H + GAP)
            rect = pygame.Rect(40, ry, CELL_W, CELL_H)
            self._dye_thread_rects[bi] = rect
            sel = self._dye_thread_idx == bi
            pygame.draw.rect(self.screen, _CELL_BG, rect)
            pygame.draw.rect(self.screen, _ACCENT if sel else _DIM_C, rect, 2 if sel else 1)
            nt = self.small.render(f"{t.fiber_type.title()} Thread", True, _TITLE_C)
            self.screen.blit(nt, (44, ry + 8))
            qt = self.small.render(f"Quality {t.quality:.0%}", True, _LABEL_C)
            self.screen.blit(qt, (44, ry + 26))

        # Dye extract list (right half)
        sub_d = self.small.render("Select dye extract:", True, _LABEL_C)
        self.screen.blit(sub_d, (SCREEN_W // 2 + 40, 68))
        dye_families = ["golden", "crimson", "rose", "cobalt", "violet", "verdant", "amber", "ivory", "teal", "indigo", "ochre"]
        CELL_W2, CELL_H2, GAP2 = 200, 44, 6
        rx0 = SCREEN_W // 2 + 40
        for di, fam in enumerate(dye_families):
            key = f"dye_extract_{fam}"
            count = player.inventory.get(key, 0)
            ry = 88 + di * (CELL_H2 + GAP2)
            rect = pygame.Rect(rx0, ry, CELL_W2, CELL_H2)
            self._dye_extract_rects[fam] = rect
            sel = self._dye_selected_extract == fam
            fam_col = tuple(DYE_FAMILY_COLORS.get(fam, [200, 180, 160]))
            bg_col = (min(fam_col[0], 60), min(fam_col[1], 60), min(fam_col[2], 60)) if sel and count > 0 else _CELL_BG
            pygame.draw.rect(self.screen, bg_col, rect)
            if sel and count > 0:
                border_col = (255, 255, 255)
                border_w = 2
            elif count > 0:
                border_col = fam_col
                border_w = 1
            else:
                border_col = _DIM_C
                border_w = 1
            pygame.draw.rect(self.screen, border_col, rect, border_w)
            label_s = self.small.render(
                f"{'▶ ' if sel and count > 0 else ''}{DYE_FAMILY_DISPLAY.get(fam, fam).title()}",
                True, (255, 255, 255) if sel and count > 0 else (_TITLE_C if count > 0 else _DIM_C)
            )
            self.screen.blit(label_s, (rx0 + 6, ry + 6))
            cnt_s = self.small.render(f"x{count}", True, _LABEL_C if count > 0 else _DIM_C)
            self.screen.blit(cnt_s, (rx0 + 6, ry + 24))

        # Apply button — only shown when both thread and extract are ready
        if self._dye_thread_idx is not None and self._dye_selected_extract:
            can_apply = player.inventory.get(f"dye_extract_{self._dye_selected_extract}", 0) > 0
            if can_apply:
                if self._dye_result_btn is None:
                    self._dye_result_btn = pygame.Rect(SCREEN_W // 2 - 100, SCREEN_H - 60, 200, 40)
                pygame.draw.rect(self.screen, _ACCENT, self._dye_result_btn)
                pygame.draw.rect(self.screen, _TITLE_C, self._dye_result_btn, 1)
                lbl = self.font.render("Apply Dye", True, (255, 255, 255))
                self.screen.blit(lbl, (self._dye_result_btn.centerx - lbl.get_width() // 2,
                                       self._dye_result_btn.centery - lbl.get_height() // 2))
            else:
                # Selected extract was consumed — clear stale selection
                self._dye_selected_extract = None
                self._dye_result_btn = None

    def _handle_dye_vat_click(self, pos, player):
        if hasattr(self, "_dye_tab_rects"):
            for tkey, tr in self._dye_tab_rects.items():
                if tr.collidepoint(pos):
                    self._dye_tab = tkey
                    return

        if self._dye_tab == "extract":
            for idx, rect in self._dye_flower_rects.items():
                if rect.collidepoint(pos) and idx < len(player.wildflowers):
                    wf = player.wildflowers[idx]
                    fam = dye_family_from_color(wf.primary_color)
                    if fam == "natural":
                        player.pending_notifications.append(("Textile", "Too muted — no dye extracted", None))
                        return
                    player.wildflowers.pop(idx)
                    player._add_item(f"dye_extract_{fam}")
                    player.pending_notifications.append(("Textile", f"{DYE_FAMILY_DISPLAY.get(fam,'').title()} Dye Extract", None))
                    return
        else:
            for bi, rect in self._dye_thread_rects.items():
                if rect.collidepoint(pos):
                    self._dye_thread_idx = bi
                    self._dye_result_btn = None
                    return
            for fam, rect in self._dye_extract_rects.items():
                if rect.collidepoint(pos) and player.inventory.get(f"dye_extract_{fam}", 0) > 0:
                    self._dye_selected_extract = fam
                    self._dye_result_btn = None
                    return
            if self._dye_result_btn and self._dye_result_btn.collidepoint(pos):
                bi = self._dye_thread_idx
                fam = self._dye_selected_extract
                if bi is not None and fam and player.inventory.get(f"dye_extract_{fam}", 0) > 0:
                    apply_dye(player.textiles[bi], fam)
                    key = f"dye_extract_{fam}"
                    player.inventory[key] = player.inventory.get(key, 0) - 1
                    player.pending_notifications.append(("Textile", f"Thread Dyed — {DYE_FAMILY_DISPLAY.get(fam,'').title()}", None))
                    self._dye_thread_idx = None
                    self._dye_selected_extract = None
                    self._dye_result_btn = None

    # ─────────────────────────────────────────────────────────────────────────
    # LOOM
    # ─────────────────────────────────────────────────────────────────────────

    def _draw_loom(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("LOOM", True, _TITLE_C)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, _HINT_C)
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        if self._loom_phase == "select_thread":
            self._loom_thread_rects.clear()
            threads = [(i, t) for i, t in enumerate(player.textiles) if t.state in ("thread", "dyed")]
            if not threads:
                msg = self.font.render("No thread ready! Spin fiber or dye at the Dye Vat.", True, _LABEL_C)
                self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2))
                return
            sub = self.small.render("Select thread to weave:", True, _LABEL_C)
            self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 34))
            CELL_W, CELL_H, GAP, COLS = 260, 78, 8, 4
            gx0 = (SCREEN_W - (COLS * CELL_W + (COLS - 1) * GAP)) // 2
            for li, (bi, t) in enumerate(threads[:16]):
                col_i, row_i = li % COLS, li // COLS
                rx = gx0 + col_i * (CELL_W + GAP)
                ry = 55 + row_i * (CELL_H + GAP)
                rect = pygame.Rect(rx, ry, CELL_W, CELL_H)
                self._loom_thread_rects[bi] = rect
                dye_col = tuple(DYE_FAMILY_COLORS.get(t.dye_family, DYE_FAMILY_COLORS["natural"]))
                pygame.draw.rect(self.screen, _CELL_BG, rect)
                pygame.draw.rect(self.screen, dye_col, rect, 2)
                nm = self.small.render(f"{t.fiber_type.title()} Thread", True, _TITLE_C)
                self.screen.blit(nm, (rx + 5, ry + 5))
                dye_s = self.small.render(f"{DYE_FAMILY_DISPLAY.get(t.dye_family, 'Natural')} dye · Q {t.quality:.0%}", True, dye_col)
                self.screen.blit(dye_s, (rx + 5, ry + 23))
                intr = _FIBER_INTRINSIC_DESCS.get(t.fiber_type, "")
                if intr:
                    intr_s = self.small.render(intr, True, _DIM_C)
                    self.screen.blit(intr_s, (rx + 5, ry + 41))
                st = self.small.render(t.state.title(), True, _DIM_C)
                self.screen.blit(st, (rx + 5, ry + 59))

        elif self._loom_phase == "select_texture":
            self._loom_texture_rects.clear()
            sub = self.small.render("Choose a weave texture:", True, _LABEL_C)
            self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 34))
            BTN_W, BTN_H, BTN_GAP = 210, 120, 14
            TCOLS = 4
            items = list(TEXTURE_PATTERNS.items())
            rows = (len(items) + TCOLS - 1) // TCOLS
            grid_h = rows * BTN_H + (rows - 1) * BTN_GAP
            gy0 = SCREEN_H // 2 - grid_h // 2
            for ti, (tkey, tdata) in enumerate(items):
                col_i = ti % TCOLS
                row_i = ti // TCOLS
                row_count = min(TCOLS, len(items) - row_i * TCOLS)
                row_w = row_count * BTN_W + (row_count - 1) * BTN_GAP
                gx0 = (SCREEN_W - row_w) // 2
                px = gx0 + col_i * (BTN_W + BTN_GAP)
                py = gy0 + row_i * (BTN_H + BTN_GAP)
                prect = pygame.Rect(px, py, BTN_W, BTN_H)
                self._loom_texture_rects[tkey] = prect
                pygame.draw.rect(self.screen, _CELL_BG, prect)
                pygame.draw.rect(self.screen, _ACCENT, prect, 2)
                lbl = self.font.render(tdata["label"], True, _TITLE_C)
                self.screen.blit(lbl, (px + BTN_W // 2 - lbl.get_width() // 2, py + 12))
                desc_s = self.small.render(tdata["desc"], True, _LABEL_C)
                self.screen.blit(desc_s, (px + 8, py + 46))
                mod_val = tdata["pattern_mod"]
                mod_str = "No pattern bonus" if mod_val == 0 else f"+{mod_val:.0%} pattern quality"
                mod_s = self.small.render(mod_str, True, _DIM_C if mod_val == 0 else (130, 210, 140))
                self.screen.blit(mod_s, (px + 8, py + 66))
                diff_s = self.small.render(
                    ["Simple", "Easy", "Moderate", "Moderate", "Complex", "Complex", "Master"][ti],
                    True, [(160,160,160),(140,200,140),(200,200,100),(200,200,100),(220,160,80),(220,160,80),(210,80,80)][ti]
                )
                self.screen.blit(diff_s, (px + BTN_W - diff_s.get_width() - 8, py + 12))

        elif self._loom_phase == "select_output":
            self._loom_output_rects.clear()
            sub = self.small.render("Choose what to weave:", True, _LABEL_C)
            self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 34))
            outputs = list(OUTPUT_DISPLAY.items())
            BTN_W, BTN_H, BTN_GAP = 200, 100, 14
            COLS = 3
            total_w = min(len(outputs), COLS) * BTN_W + (min(len(outputs), COLS) - 1) * BTN_GAP
            gx0 = (SCREEN_W - total_w) // 2
            for oi, (okey, olabel) in enumerate(outputs):
                col_i, row_i = oi % COLS, oi // COLS
                px = gx0 + col_i * (BTN_W + BTN_GAP)
                py = 58 + row_i * (BTN_H + BTN_GAP)
                prect = pygame.Rect(px, py, BTN_W, BTN_H)
                self._loom_output_rects[okey] = prect
                pygame.draw.rect(self.screen, _CELL_BG, prect)
                pygame.draw.rect(self.screen, _ACCENT, prect, 2)
                lbl = self.font.render(olabel, True, _TITLE_C)
                self.screen.blit(lbl, (px + BTN_W // 2 - lbl.get_width() // 2, py + 12))
                if okey in GARMENT_BUFFS:
                    stat = GARMENT_BUFFS[okey]
                    mx = GARMENT_MAX_BONUS[stat]
                    desc_s = self.small.render(GARMENT_BUFF_DESCS[stat].format(mx * 100), True, _LABEL_C)
                    self.screen.blit(desc_s, (px + 8, py + 44))
                elif okey in ("rug", "tapestry"):
                    ps = self.small.render("Placeable decoration", True, _LABEL_C)
                    self.screen.blit(ps, (px + 8, py + 44))
                else:
                    cs = self.small.render("Encyclopedia collectible", True, _LABEL_C)
                    self.screen.blit(cs, (px + 8, py + 44))

        elif self._loom_phase == "weaving":
            if dt > 0:
                self._loom_cell_timer -= dt
                if self._loom_cell_timer <= 0:
                    self._loom_active_cell += 1
                    self._loom_cell_timer = _LOOM_CLICK_WINDOW
                    if self._loom_active_cell >= _LOOM_GRID_COLS * _LOOM_GRID_ROWS:
                        self._finish_weaving(player)
                        return

            self._draw_loom_grid()

            if self._loom_active_cell < _LOOM_GRID_COLS * _LOOM_GRID_ROWS:
                timer_ratio = self._loom_cell_timer / _LOOM_CLICK_WINDOW
                timer_col = (int(60 + 160 * timer_ratio), int(140 + 80 * timer_ratio), 60)
                hint_s = self.font.render("Click the highlighted cell!", True, timer_col)
                self.screen.blit(hint_s, (SCREEN_W // 2 - hint_s.get_width() // 2, SCREEN_H - 52))
            prog = self._loom_active_cell / (_LOOM_GRID_COLS * _LOOM_GRID_ROWS)
            q_s = self.small.render(f"Pattern quality: {self._loom_pattern_score:.0%}", True, _TITLE_C)
            self.screen.blit(q_s, (SCREEN_W // 2 - q_s.get_width() // 2, SCREEN_H - 30))

        elif self._loom_phase == "result":
            if not player.textiles:
                self._loom_phase = "select_thread"
                return
            t = next((x for x in player.textiles if x.state == "woven"), None)
            if not t:
                self._loom_phase = "select_thread"
                return
            cx, cy = SCREEN_W // 2, 70
            dye_col = tuple(DYE_FAMILY_COLORS.get(t.dye_family, DYE_FAMILY_COLORS["natural"]))
            pygame.draw.rect(self.screen, dye_col, (cx - 30, cy, 60, 60))
            pygame.draw.rect(self.screen, _ACCENT, (cx - 30, cy, 60, 60), 3)
            iy = cy + 80

            def rline(txt, col=_TITLE_C):
                nonlocal iy
                s = self.font.render(txt, True, col)
                self.screen.blit(s, (cx - s.get_width() // 2, iy))
                iy += 28

            rline(f"{OUTPUT_DISPLAY.get(t.output_type, t.output_type)}")
            rline(f"{t.fiber_type.title()} · {DYE_FAMILY_DISPLAY.get(t.dye_family,'Natural')} · {TEXTURE_PATTERNS[t.texture]['label']}", dye_col)
            rline(f"Quality: {t.quality:.0%}  Pattern: {t.pattern_quality:.0%}", _LABEL_C)
            if t.output_type in GARMENT_BUFFS:
                from textiles import get_garment_bonus
                bonus = get_garment_bonus(t)
                stat = GARMENT_BUFFS[t.output_type]
                rline(GARMENT_BUFF_DESCS[stat].format(bonus * 100), (120, 220, 140))

            if self._loom_result_btn is None:
                bw, bh = 180, 38
                self._loom_result_btn = pygame.Rect(cx - bw // 2, iy + 12, bw, bh)
            pygame.draw.rect(self.screen, _ACCENT, self._loom_result_btn)
            done = self.font.render("Done", True, (255, 255, 255))
            self.screen.blit(done, (self._loom_result_btn.centerx - done.get_width() // 2,
                                    self._loom_result_btn.centery - done.get_height() // 2))

    def _draw_loom_grid(self):
        total_w = _LOOM_GRID_COLS * (_LOOM_CELL_W + _LOOM_CELL_GAP) - _LOOM_CELL_GAP
        total_h = _LOOM_GRID_ROWS * (_LOOM_CELL_H + _LOOM_CELL_GAP) - _LOOM_CELL_GAP
        gx0 = SCREEN_W // 2 - total_w // 2
        gy0 = 70
        self._loom_grid_rects = []
        for row in range(_LOOM_GRID_ROWS):
            for col in range(_LOOM_GRID_COLS):
                idx = row * _LOOM_GRID_COLS + col
                rx = gx0 + col * (_LOOM_CELL_W + _LOOM_CELL_GAP)
                ry = gy0 + row * (_LOOM_CELL_H + _LOOM_CELL_GAP)
                rect = pygame.Rect(rx, ry, _LOOM_CELL_W, _LOOM_CELL_H)
                self._loom_grid_rects.append(rect)
                if idx < self._loom_active_cell:
                    bg = (50, 120, 55) if idx in self._loom_clicked_cells else (80, 35, 35)
                elif idx == self._loom_active_cell:
                    timer_ratio = self._loom_cell_timer / _LOOM_CLICK_WINDOW
                    g_val = int(100 + 120 * timer_ratio)
                    bg = (40, g_val, 50)
                else:
                    bg = _CELL_BG
                pygame.draw.rect(self.screen, bg, rect)
                border = _ACCENT if idx == self._loom_active_cell else _DIM_C
                pygame.draw.rect(self.screen, border, rect, 2 if idx == self._loom_active_cell else 1)

    def _finish_weaving(self, player):
        bi = self._loom_thread_idx
        t = player.textiles[bi]
        score = self._loom_pattern_score
        precision_bonus = player.get_textile_bonus("precision")
        if precision_bonus > 0:
            score = min(1.0, score + precision_bonus * 0.5)
        apply_weave(t, self._loom_output_type, self._loom_texture, score)
        dk = discovery_key(t)
        player.discovered_textiles.add(dk)
        item_key = output_item_key(t)
        player._add_item(item_key)
        player.pending_notifications.append(("Textile", OUTPUT_DISPLAY.get(t.output_type, t.output_type), None))
        self._loom_phase = "result"
        self._loom_result_btn = None

    def _handle_loom_click(self, pos, player):
        if self._loom_phase == "select_thread":
            for bi, rect in self._loom_thread_rects.items():
                if rect.collidepoint(pos):
                    self._loom_thread_idx = bi
                    self._loom_phase = "select_texture"
                    return
        elif self._loom_phase == "select_texture":
            for tkey, rect in self._loom_texture_rects.items():
                if rect.collidepoint(pos):
                    self._loom_texture = tkey
                    self._loom_phase = "select_output"
                    return
        elif self._loom_phase == "select_output":
            for okey, rect in self._loom_output_rects.items():
                if rect.collidepoint(pos):
                    self._loom_output_type = okey
                    self._loom_phase = "weaving"
                    self._loom_active_cell = 0
                    self._loom_cell_timer = _LOOM_CLICK_WINDOW
                    self._loom_pattern_score = 0.0
                    self._loom_clicked_cells = set()
                    self._loom_grid_rects = []
                    return
        elif self._loom_phase == "weaving":
            if hasattr(self, "_loom_grid_rects"):
                active = self._loom_active_cell
                if active < len(self._loom_grid_rects):
                    if self._loom_grid_rects[active].collidepoint(pos):
                        timer_ratio = self._loom_cell_timer / _LOOM_CLICK_WINDOW
                        self._loom_pattern_score = min(1.0, self._loom_pattern_score + timer_ratio / (_LOOM_GRID_COLS * _LOOM_GRID_ROWS))
                        self._loom_clicked_cells.add(active)
                        self._loom_active_cell += 1
                        self._loom_cell_timer = _LOOM_CLICK_WINDOW
                        if self._loom_active_cell >= _LOOM_GRID_COLS * _LOOM_GRID_ROWS:
                            self._finish_weaving(player)
        elif self._loom_phase == "result":
            if self._loom_result_btn and self._loom_result_btn.collidepoint(pos):
                self._loom_phase = "select_thread"
                self._loom_result_btn = None
                self._loom_thread_idx = None

    def handle_loom_keydown(self, key, player):
        if key == pygame.K_ESCAPE:
            self.refinery_open = False

    # ─────────────────────────────────────────────────────────────────────────
    # WARDROBE
    # ─────────────────────────────────────────────────────────────────────────

    def _draw_wardrobe(self, player):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        # Centered panel with double border
        PNL_X, PNL_Y, PNL_W, PNL_H = 140, 18, 1000, 684
        pygame.draw.rect(self.screen, (18, 10, 26), (PNL_X, PNL_Y, PNL_W, PNL_H))
        pygame.draw.rect(self.screen, (55, 30, 72), (PNL_X, PNL_Y, PNL_W, PNL_H), 1)
        pygame.draw.rect(self.screen, _ACCENT, (PNL_X + 3, PNL_Y + 3, PNL_W - 6, PNL_H - 6), 1)

        # Header bar
        HDR_H = 38
        pygame.draw.rect(self.screen, (35, 18, 48), (PNL_X, PNL_Y, PNL_W, HDR_H))
        pygame.draw.line(self.screen, _ACCENT, (PNL_X + 4, PNL_Y + HDR_H), (PNL_X + PNL_W - 4, PNL_Y + HDR_H), 1)
        title = self.font.render("W A R D R O B E", True, _TITLE_C)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, PNL_Y + (HDR_H - title.get_height()) // 2))
        hint = self.small.render("ESC or T to close", True, _HINT_C)
        self.screen.blit(hint, (PNL_X + PNL_W - hint.get_width() - 12, PNL_Y + (HDR_H - hint.get_height()) // 2))

        CONTENT_Y = PNL_Y + HDR_H + 10
        LEFT_X = PNL_X + 16

        def _sec(text, y):
            lbl = self.small.render(text, True, _DIM_C)
            self.screen.blit(lbl, (LEFT_X, y))
            lx = LEFT_X + lbl.get_width() + 8
            pygame.draw.line(self.screen, (55, 35, 68), (lx, y + 6), (PNL_X + PNL_W - 16, y + 6), 1)

        # ── Clothing slots ─────────────────────────────────────────────────
        _sec("CLOTHING SLOTS", CONTENT_Y)

        self._wardrobe_slot_rects = {}
        SLOT_W, SLOT_H, SLOT_GAP_X, SLOT_GAP_Y = 280, 78, 20, 8
        SLOT_HDR_H = 20
        slots = [
            ("head",  "Head"),  ("hands", "Hands"),
            ("chest", "Chest"), ("legs",  "Legs"),
            ("feet",  "Feet"),  ("back",  "Back"),
        ]
        gx0 = SCREEN_W // 2 - (SLOT_W * 2 + SLOT_GAP_X) // 2
        SLOTS_Y = CONTENT_Y + 16
        for si, (slot, slot_label) in enumerate(slots):
            col_i, row_i = si % 2, si // 2
            rx = gx0 + col_i * (SLOT_W + SLOT_GAP_X)
            ry = SLOTS_Y + row_i * (SLOT_H + SLOT_GAP_Y)
            rect = pygame.Rect(rx, ry, SLOT_W, SLOT_H)
            self._wardrobe_slot_rects[slot] = rect
            pygame.draw.rect(self.screen, _CELL_BG, rect)
            pygame.draw.rect(self.screen, _ACCENT, rect, 1)
            pygame.draw.rect(self.screen, (38, 20, 50), (rx, ry, SLOT_W, SLOT_HDR_H))
            pygame.draw.line(self.screen, _ACCENT, (rx, ry + SLOT_HDR_H), (rx + SLOT_W, ry + SLOT_HDR_H), 1)
            sl = self.small.render(slot_label.upper(), True, _LABEL_C)
            self.screen.blit(sl, (rx + 8, ry + (SLOT_HDR_H - sl.get_height()) // 2))
            worn_t = player.get_worn_textile(slot)
            if worn_t:
                dye_col = tuple(DYE_FAMILY_COLORS.get(worn_t.dye_family, DYE_FAMILY_COLORS["natural"]))
                pygame.draw.rect(self.screen, dye_col, (rx + SLOT_W - 14, ry + 4, 10, 12))
                pygame.draw.rect(self.screen, (160, 160, 160), (rx + SLOT_W - 14, ry + 4, 10, 12), 1)
                nm = self.font.render(OUTPUT_DISPLAY.get(worn_t.output_type, worn_t.output_type), True, dye_col)
                self.screen.blit(nm, (rx + 8, ry + SLOT_HDR_H + 6))
                from textiles import GARMENT_BUFFS, GARMENT_BUFF_DESCS, get_garment_bonus
                stat = GARMENT_BUFFS.get(worn_t.output_type, "")
                if stat:
                    bonus = get_garment_bonus(worn_t)
                    bs = self.small.render(GARMENT_BUFF_DESCS[stat].format(bonus * 100), True, (120, 220, 140))
                    self.screen.blit(bs, (rx + 8, ry + SLOT_HDR_H + 30))
                un_s = self.small.render("[click to unequip]", True, _HINT_C)
                self.screen.blit(un_s, (rx + SLOT_W - un_s.get_width() - 8, ry + SLOT_H - un_s.get_height() - 4))
            else:
                emp = self.small.render("— empty —", True, (52, 34, 64))
                self.screen.blit(emp, (rx + SLOT_W // 2 - emp.get_width() // 2,
                                       ry + SLOT_HDR_H + (SLOT_H - SLOT_HDR_H) // 2 - 6))

        slots_bottom = SLOTS_Y + 3 * (SLOT_H + SLOT_GAP_Y)

        # ── Garment inventory ─────────────────────────────────────────────
        INV_Y = slots_bottom + 14
        pygame.draw.line(self.screen, (48, 28, 60), (PNL_X + 8, INV_Y - 6), (PNL_X + PNL_W - 8, INV_Y - 6), 1)
        _sec("GARMENTS IN INVENTORY", INV_Y)

        self._wardrobe_item_rects = {}
        garment_slots = {
            "garment_hat": "head", "garment_vest": "chest", "garment_boots": "feet",
            "garment_gloves": "hands", "garment_leggings": "legs",
            "garment_cloak": "back", "garment_cloak_hooded": "back",
            "garment_cloak_royal": "back", "garment_cloak_tattered": "back",
            "garment_cloak_half": "back",
        }
        garment_items = [(k, player.inventory.get(k, 0)) for k in garment_slots if player.inventory.get(k, 0) > 0]
        GCELL_W, GCELL_H, GCELL_HDR_H, GCELL_GAP = 175, 60, 18, 10
        GCELLS_Y = INV_Y + 16
        if garment_items:
            for gi, (gkey, gcount) in enumerate(garment_items):
                rx = LEFT_X + gi * (GCELL_W + GCELL_GAP)
                ry = GCELLS_Y
                rect = pygame.Rect(rx, ry, GCELL_W, GCELL_H)
                self._wardrobe_item_rects[gkey] = rect
                pygame.draw.rect(self.screen, _CELL_BG, rect)
                pygame.draw.rect(self.screen, _ACCENT, rect, 1)
                pygame.draw.rect(self.screen, (38, 20, 50), (rx, ry, GCELL_W, GCELL_HDR_H))
                pygame.draw.line(self.screen, _ACCENT, (rx, ry + GCELL_HDR_H), (rx + GCELL_W, ry + GCELL_HDR_H), 1)
                from items import ITEMS
                slot_lbl = garment_slots[gkey].upper()
                sl_s = self.small.render(slot_lbl, True, _DIM_C)
                self.screen.blit(sl_s, (rx + 5, ry + (GCELL_HDR_H - sl_s.get_height()) // 2))
                nm = self.font.render(ITEMS[gkey]["name"], True, _TITLE_C)
                self.screen.blit(nm, (rx + 5, ry + GCELL_HDR_H + 4))
                cnt_s = self.small.render(f"× {gcount}", True, _LABEL_C)
                self.screen.blit(cnt_s, (rx + GCELL_W - cnt_s.get_width() - 6, ry + GCELL_H - cnt_s.get_height() - 4))
        else:
            none_s = self.small.render("No garments in inventory", True, (52, 34, 64))
            self.screen.blit(none_s, (LEFT_X, GCELLS_Y + 18))

        # ── Armor ─────────────────────────────────────────────────────────
        ARMOR_Y = GCELLS_Y + GCELL_H + 16
        pygame.draw.line(self.screen, (48, 28, 60), (PNL_X + 8, ARMOR_Y - 6), (PNL_X + PNL_W - 8, ARMOR_Y - 6), 1)
        _sec("ARMOR", ARMOR_Y)

        from items import ITEMS as _ITEMS
        ARMOR_SLOTS = [("helmet", "Helmet"), ("chestplate", "Chest"), ("leggings", "Legs"), ("boots", "Boots")]
        self._armor_slot_rects = {}
        ACELL_W, ACELL_H, ACELL_HDR_H, AGAP = 190, 80, 20, 12
        ARMOR_SLOTS_Y = ARMOR_Y + 16
        for ai, (aslot, alabel) in enumerate(ARMOR_SLOTS):
            rx = LEFT_X + ai * (ACELL_W + AGAP)
            ry = ARMOR_SLOTS_Y
            equipped = player.worn_armor.get(aslot)
            dye_fam  = player.worn_armor_dye.get(aslot)
            dye_rgb  = tuple(DYE_FAMILY_COLORS[dye_fam]) if dye_fam and dye_fam in DYE_FAMILY_COLORS else None
            rect = pygame.Rect(rx, ry, ACELL_W, ACELL_H)
            self._armor_slot_rects[aslot] = rect
            pygame.draw.rect(self.screen, _CELL_BG, rect)
            border_col = dye_rgb if (dye_rgb and equipped) else _ACCENT
            pygame.draw.rect(self.screen, border_col, rect, 1)
            pygame.draw.rect(self.screen, (38, 20, 50), (rx, ry, ACELL_W, ACELL_HDR_H))
            pygame.draw.line(self.screen, border_col, (rx, ry + ACELL_HDR_H), (rx + ACELL_W, ry + ACELL_HDR_H), 1)
            sl = self.small.render(alabel.upper(), True, _LABEL_C)
            self.screen.blit(sl, (rx + 8, ry + (ACELL_HDR_H - sl.get_height()) // 2))
            if dye_rgb:
                pygame.draw.rect(self.screen, dye_rgb, (rx + ACELL_W - 18, ry + (ACELL_HDR_H - 12) // 2, 14, 12))
                pygame.draw.rect(self.screen, (200, 200, 200), (rx + ACELL_W - 18, ry + (ACELL_HDR_H - 12) // 2, 14, 12), 1)
            if equipped and equipped in _ITEMS:
                idata = _ITEMS[equipped]
                nm = self.font.render(idata["name"], True, tuple(idata["color"]))
                self.screen.blit(nm, (rx + 8, ry + ACELL_HDR_H + 6))
                def_s = self.small.render(f"DEF  +{idata['defense']}", True, (120, 220, 140))
                self.screen.blit(def_s, (rx + 8, ry + ACELL_HDR_H + 28))
                if dye_rgb:
                    dn = self.small.render(DYE_FAMILY_DISPLAY.get(dye_fam, dye_fam).title(), True, dye_rgb)
                    self.screen.blit(dn, (rx + 8, ry + ACELL_HDR_H + 46))
                un_s = self.small.render("[click: unequip]", True, _HINT_C)
                self.screen.blit(un_s, (rx + ACELL_W - un_s.get_width() - 6, ry + ACELL_H - un_s.get_height() - 4))
            else:
                candidates = [k for k, v in player.inventory.items()
                              if v > 0 and k in _ITEMS and _ITEMS[k].get("armor_slot") == aslot]
                if candidates:
                    best = max(candidates, key=lambda k: _ITEMS[k].get("defense", 0))
                    eq_s = self.small.render(_ITEMS[best]["name"], True, tuple(_ITEMS[best]["color"]))
                    self.screen.blit(eq_s, (rx + 8, ry + ACELL_HDR_H + 8))
                    cl_s = self.small.render("[click to equip]", True, _HINT_C)
                    self.screen.blit(cl_s, (rx + 8, ry + ACELL_H - cl_s.get_height() - 6))
                else:
                    emp = self.small.render("— empty —", True, (52, 34, 64))
                    self.screen.blit(emp, (rx + ACELL_W // 2 - emp.get_width() // 2,
                                           ry + ACELL_HDR_H + (ACELL_H - ACELL_HDR_H) // 2 - 6))

        # ── Dye palette ───────────────────────────────────────────────────
        DYE_Y0 = ARMOR_SLOTS_Y + ACELL_H + 12
        pygame.draw.line(self.screen, (48, 28, 60), (PNL_X + 8, DYE_Y0 - 4), (PNL_X + PNL_W - 8, DYE_Y0 - 4), 1)
        _sec("DYE ARMOR  (click swatch to apply,  ✕ to remove)", DYE_Y0)

        _DYE_ORDER = ["golden", "crimson", "rose", "cobalt", "violet",
                      "verdant", "amber", "ivory", "teal", "indigo", "ochre"]
        self._armor_dye_rects = {}
        SLOT_SHORT = {"helmet": "HELM", "chestplate": "CHEST", "leggings": "LEGS", "boots": "BOOTS"}
        SWATCH = 18
        for ri, (aslot, _) in enumerate(ARMOR_SLOTS):
            ry = DYE_Y0 + 16 + ri * (SWATCH + 6)
            active = bool(player.worn_armor.get(aslot))
            lbl_col = _LABEL_C if active else _DIM_C
            sl_s = self.small.render(SLOT_SHORT[aslot], True, lbl_col)
            self.screen.blit(sl_s, (LEFT_X, ry + (SWATCH - sl_s.get_height()) // 2))
            cur_dye = player.worn_armor_dye.get(aslot)
            sx = LEFT_X + 62
            for fam in _DYE_ORDER:
                has_item = player.inventory.get(f"dye_extract_{fam}", 0) > 0
                is_cur   = cur_dye == fam
                if not (has_item or is_cur):
                    continue
                sc = tuple(DYE_FAMILY_COLORS.get(fam, [180, 180, 180]))
                sr = pygame.Rect(sx, ry, SWATCH, SWATCH)
                self._armor_dye_rects[(aslot, fam)] = sr
                pygame.draw.rect(self.screen, sc, sr)
                border_c = (255, 255, 255) if is_cur else ((180, 180, 180) if has_item else (80, 80, 80))
                pygame.draw.rect(self.screen, border_c, sr, 2 if is_cur else 1)
                sx += SWATCH + 4
            if cur_dye and active:
                sr = pygame.Rect(sx, ry, SWATCH, SWATCH)
                self._armor_dye_rects[(aslot, "__remove__")] = sr
                pygame.draw.rect(self.screen, (65, 30, 30), sr)
                pygame.draw.line(self.screen, (220, 70, 70), (sx + 3, ry + 3), (sx + SWATCH - 4, ry + SWATCH - 4), 2)
                pygame.draw.line(self.screen, (220, 70, 70), (sx + SWATCH - 4, ry + 3), (sx + 3, ry + SWATCH - 4), 2)
                pygame.draw.rect(self.screen, (150, 60, 60), sr, 1)

    def handle_wardrobe_click(self, pos, player):
        if hasattr(self, "_wardrobe_slot_rects"):
            for slot, rect in self._wardrobe_slot_rects.items():
                if rect.collidepoint(pos):
                    worn_uid = player.worn.get(slot)
                    if worn_uid:
                        # Unequip: find output_type to determine item key
                        t = player.get_worn_textile(slot)
                        if t:
                            player._add_item(t.output_type)
                        player.worn[slot] = None
                    return
        if hasattr(self, "_wardrobe_item_rects"):
            garment_slots = {
                "garment_hat": "head", "garment_vest": "chest", "garment_boots": "feet",
                "garment_gloves": "hands", "garment_leggings": "legs",
                "garment_cloak": "back", "garment_cloak_hooded": "back",
                "garment_cloak_royal": "back", "garment_cloak_tattered": "back",
                "garment_cloak_half": "back",
            }
            for gkey, rect in self._wardrobe_item_rects.items():
                if rect.collidepoint(pos):
                    slot = garment_slots[gkey]
                    # Find first matching woven garment textile
                    match = next((t for t in player.textiles
                                  if t.output_type == gkey and t.state == "woven"
                                  and t.uid not in player.worn.values()), None)
                    if match and player.inventory.get(gkey, 0) > 0:
                        # Unequip current if any
                        if player.worn.get(slot):
                            old_t = player.get_worn_textile(slot)
                            if old_t:
                                player._add_item(old_t.output_type)
                        player.worn[slot] = match.uid
                        player.inventory[gkey] = player.inventory.get(gkey, 0) - 1
                    return
        if hasattr(self, "_armor_dye_rects"):
            for (aslot, fam), rect in self._armor_dye_rects.items():
                if rect.collidepoint(pos):
                    if not player.worn_armor.get(aslot):
                        return
                    if fam == "__remove__":
                        player.worn_armor_dye[aslot] = None
                    elif fam and player.inventory.get(f"dye_extract_{fam}", 0) > 0:
                        player.inventory[f"dye_extract_{fam}"] -= 1
                        if player.inventory[f"dye_extract_{fam}"] <= 0:
                            del player.inventory[f"dye_extract_{fam}"]
                        player.worn_armor_dye[aslot] = fam
                    return
        if hasattr(self, "_armor_slot_rects"):
            from items import ITEMS as _ITEMS
            for aslot, rect in self._armor_slot_rects.items():
                if rect.collidepoint(pos):
                    equipped = player.worn_armor.get(aslot)
                    if equipped:
                        player._add_item(equipped)
                        player.worn_armor[aslot] = None
                        player.worn_armor_dye[aslot] = None
                    else:
                        candidates = [k for k, v in player.inventory.items()
                                      if v > 0 and k in _ITEMS and _ITEMS[k].get("armor_slot") == aslot]
                        if candidates:
                            best = max(candidates, key=lambda k: _ITEMS[k].get("defense", 0))
                            player.inventory[best] -= 1
                            if player.inventory[best] <= 0:
                                del player.inventory[best]
                            player.worn_armor[aslot] = best
                    return
