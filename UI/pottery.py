import pygame
import math
from constants import SCREEN_W, SCREEN_H
from pottery import (apply_firing_result, get_output_item, classify_shape,
                     profile_evenness, profile_thickness,
                     CLAY_BIOME_PROFILES, BIOME_DISPLAY_NAMES, GLAZE_TYPES,
                     FIRING_LEVELS, WHEEL_ROWS, WHEEL_MAX_RAD, WHEEL_MIN_RAD)

_CLAY_COLOR   = (155, 105, 75)
_KILN_ORANGE  = (230, 110, 40)
_PANEL_BG     = (30, 18, 8)
_PANEL_BORDER = (160, 110, 80)
_TEXT_MAIN    = (220, 170, 110)
_TEXT_DIM     = (130, 95, 60)
_SHAPE_LABELS = {"pot": "Pot", "amphora": "Amphora", "jar": "Jar", "jug": "Jug", "vase": "Vase"}


class PotteryMixin:

    # ── Pottery Wheel ─────────────────────────────────────────────────────────

    def _draw_pottery_wheel(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("POTTERY WHEEL", True, _TEXT_MAIN)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, _TEXT_DIM)
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        if self._wheel_phase == "select_clay":
            self._draw_wheel_select_clay(player)
        elif self._wheel_phase == "shaping":
            self._wheel_spin_angle = (self._wheel_spin_angle + dt * 120) % 360
            self._draw_wheel_shaping(player)
        elif self._wheel_phase == "confirm":
            self._draw_wheel_confirm(player)

    def _draw_wheel_select_clay(self, player):
        clay_count = player.inventory.get("clay", 0)
        sub = self.font.render(f"Clay in inventory: {clay_count}", True, _TEXT_MAIN)
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 40))

        if clay_count < 3:
            msg = self.small.render("Need at least 3 clay. Mine Clay Deposits in wetland and river biomes.", True, (200, 80, 60))
            self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2))
            return

        hint = self.small.render("Choose how much clay to load (3–8). More clay = larger starting piece.", True, _TEXT_DIM)
        self.screen.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, 70))

        self._wheel_clay_btn_rects = {}
        options = [n for n in range(3, 9) if n <= clay_count]
        BTN_W, BTN_H = 80, 60
        gx0 = SCREEN_W // 2 - (len(options) * (BTN_W + 10)) // 2
        for i, n in enumerate(options):
            rx = gx0 + i * (BTN_W + 10)
            ry = SCREEN_H // 2 - BTN_H // 2
            rect = pygame.Rect(rx, ry, BTN_W, BTN_H)
            self._wheel_clay_btn_rects[n] = rect
            pygame.draw.rect(self.screen, _PANEL_BG, rect)
            pygame.draw.rect(self.screen, _PANEL_BORDER, rect, 2)
            lbl = self.font.render(str(n), True, _TEXT_MAIN)
            self.screen.blit(lbl, (rx + BTN_W // 2 - lbl.get_width() // 2, ry + 8))
            sub2 = self.small.render("clay", True, _TEXT_DIM)
            self.screen.blit(sub2, (rx + BTN_W // 2 - sub2.get_width() // 2, ry + 36))

    def _draw_wheel_shaping(self, player):
        # Left panel: spinning wheel animation + silhouette
        cx, cy = 220, SCREEN_H // 2
        self._draw_spinning_wheel(cx, cy)
        self._draw_profile_silhouette(cx, cy - WHEEL_ROWS * 6, self._wheel_profile)

        # Detected shape label
        shape = classify_shape(self._wheel_profile)
        shape_lbl = self.font.render(_SHAPE_LABELS.get(shape, shape.title()), True, (180, 230, 120))
        self.screen.blit(shape_lbl, (cx - shape_lbl.get_width() // 2, cy - WHEEL_ROWS * 6 - 24))

        # Right panel: row editors
        self._wheel_row_rects.clear()
        rx0 = 360
        row_h = (SCREEN_H - 80) // WHEEL_ROWS
        for row in range(WHEEL_ROWS):
            ry = 40 + row * row_h
            rad = self._wheel_profile[row]

            # Row bar (shows current radius)
            bar_w = 200
            bar_x = rx0
            bar_rect = pygame.Rect(bar_x, ry + row_h // 2 - 6, bar_w, 12)
            pygame.draw.rect(self.screen, (50, 35, 20), bar_rect)
            fill_w = int(bar_w * rad / WHEEL_MAX_RAD)
            pygame.draw.rect(self.screen, _CLAY_COLOR, pygame.Rect(bar_x, ry + row_h // 2 - 6, fill_w, 12))
            pygame.draw.rect(self.screen, _PANEL_BORDER, bar_rect, 1)

            # – button
            minus_rect = pygame.Rect(bar_x - 22, ry + row_h // 2 - 10, 20, 20)
            pygame.draw.rect(self.screen, (60, 35, 18) if rad > WHEEL_MIN_RAD else (30, 20, 12), minus_rect)
            pygame.draw.rect(self.screen, _PANEL_BORDER, minus_rect, 1)
            m = self.small.render("-", True, _TEXT_MAIN if rad > WHEEL_MIN_RAD else _TEXT_DIM)
            self.screen.blit(m, (minus_rect.x + 7, minus_rect.y + 3))

            # + button
            plus_rect = pygame.Rect(bar_x + bar_w + 2, ry + row_h // 2 - 10, 20, 20)
            can_add = rad < WHEEL_MAX_RAD and self._wheel_clay_budget > 0
            pygame.draw.rect(self.screen, (60, 35, 18) if can_add else (30, 20, 12), plus_rect)
            pygame.draw.rect(self.screen, _PANEL_BORDER, plus_rect, 1)
            p = self.small.render("+", True, _TEXT_MAIN if can_add else _TEXT_DIM)
            self.screen.blit(p, (plus_rect.x + 5, plus_rect.y + 3))

            self._wheel_row_rects[row] = {"minus": minus_rect, "plus": plus_rect, "bar": bar_rect}

        # Clay budget display
        budget_txt = self.small.render(f"Clay budget: {self._wheel_clay_budget}", True, _TEXT_MAIN)
        self.screen.blit(budget_txt, (rx0, SCREEN_H - 60))

        # Add more clay button
        clay_avail = player.inventory.get("clay", 0)
        if clay_avail > 0:
            add_rect = pygame.Rect(rx0 + 160, SCREEN_H - 65, 100, 24)
            if not hasattr(self, '_wheel_add_clay_rect'):
                self._wheel_add_clay_rect = add_rect
            else:
                self._wheel_add_clay_rect = add_rect
            pygame.draw.rect(self.screen, (50, 30, 12), add_rect)
            pygame.draw.rect(self.screen, _PANEL_BORDER, add_rect, 1)
            at = self.small.render(f"+1 clay ({clay_avail})", True, _TEXT_MAIN)
            self.screen.blit(at, (add_rect.x + 5, add_rect.y + 5))

        # Undo hint
        undo_hint = self.small.render(f"Z: undo ({len(self._wheel_undo_stack)} steps)", True, _TEXT_DIM)
        self.screen.blit(undo_hint, (rx0, SCREEN_H - 40))

        # Confirm button
        conf_rect = pygame.Rect(SCREEN_W - 130, SCREEN_H - 50, 120, 36)
        self._wheel_confirm_rect = conf_rect
        pygame.draw.rect(self.screen, (50, 32, 14), conf_rect)
        pygame.draw.rect(self.screen, _PANEL_BORDER, conf_rect, 2)
        ct = self.font.render("SHAPE", True, _TEXT_MAIN)
        self.screen.blit(ct, (conf_rect.x + conf_rect.w // 2 - ct.get_width() // 2, conf_rect.y + 8))

    def _draw_profile_silhouette(self, cx, top_y, profile):
        row_h = 12
        for row, rad in enumerate(profile):
            ry = top_y + row * row_h
            w = rad * 4
            pygame.draw.rect(self.screen, _CLAY_COLOR, (cx - w, ry, w * 2, row_h - 1))
            pygame.draw.rect(self.screen, _darken_color(_CLAY_COLOR, 25), (cx - w, ry, w * 2, row_h - 1), 1)

    def _draw_spinning_wheel(self, cx, cy):
        angle = math.radians(self._wheel_spin_angle)
        # Wheel disc
        pygame.draw.ellipse(self.screen, (120, 85, 55), (cx - 55, cy - 20, 110, 40))
        pygame.draw.ellipse(self.screen, (80, 55, 30), (cx - 55, cy - 20, 110, 40), 2)
        # Spokes rotating
        for i in range(8):
            spoke_a = angle + i * math.pi / 4
            ex = int(cx + math.cos(spoke_a) * 50)
            ey = int(cy + math.sin(spoke_a) * 18)
            pygame.draw.line(self.screen, (80, 55, 30), (cx, cy), (ex, ey), 2)
        pygame.draw.circle(self.screen, (100, 70, 45), (cx, cy), 6)

    def _draw_wheel_confirm(self, player):
        shape = classify_shape(self._wheel_profile)
        thick = profile_thickness(self._wheel_profile)
        even  = profile_evenness(self._wheel_profile)

        cx = SCREEN_W // 2
        top_y = SCREEN_H // 2 - WHEEL_ROWS * 6

        # Centred silhouette preview
        self._draw_profile_silhouette(cx, top_y, self._wheel_profile)

        lbl = self.font.render(_SHAPE_LABELS.get(shape, shape.title()), True, _TEXT_MAIN)
        self.screen.blit(lbl, (cx - lbl.get_width() // 2, top_y - 28))

        # Stats
        stats = [
            f"Thickness: {int(thick * 100)}%",
            f"Evenness:  {int(even  * 100)}%",
            f"Clay used: {self._wheel_clay_loaded - self._wheel_clay_budget}",
        ]
        for i, s in enumerate(stats):
            st = self.small.render(s, True, _TEXT_DIM)
            self.screen.blit(st, (cx - 60, top_y + WHEEL_ROWS * 12 + 10 + i * 18))

        # Accept / Back buttons
        acc_rect = pygame.Rect(cx + 20, SCREEN_H - 55, 120, 36)
        bk_rect  = pygame.Rect(cx - 150, SCREEN_H - 55, 120, 36)
        self._wheel_accept_rect = acc_rect
        self._wheel_back_rect   = bk_rect

        for rect, label, color in [(acc_rect, "CONFIRM", (50, 90, 50)), (bk_rect, "EDIT", (60, 40, 20))]:
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, _PANEL_BORDER, rect, 2)
            t = self.font.render(label, True, _TEXT_MAIN)
            self.screen.blit(t, (rect.x + rect.w // 2 - t.get_width() // 2, rect.y + 8))

    # ── Pottery Kiln ──────────────────────────────────────────────────────────

    def _draw_pottery_kiln(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("POTTERY KILN", True, _TEXT_MAIN)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, _TEXT_DIM)
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        # Tab bar
        glaze_unlocked = self._pottery_glaze_arts_unlocked(player)
        self._kiln_tab_rects = {}
        tabs = [("fire", "FIRE"), ("glaze", "GLAZE")]
        for i, (tkey, tlbl) in enumerate(tabs):
            if tkey == "glaze" and not glaze_unlocked:
                continue
            tr = pygame.Rect(SCREEN_W // 2 - 80 + i * 85, 28, 80, 22)
            self._kiln_tab_rects[tkey] = tr
            active = self._kiln_tab == tkey
            pygame.draw.rect(self.screen, _PANEL_BG if not active else (60, 38, 15), tr)
            pygame.draw.rect(self.screen, _PANEL_BORDER, tr, 1 if not active else 2)
            tl = self.small.render(tlbl, True, _TEXT_MAIN if active else _TEXT_DIM)
            self.screen.blit(tl, (tr.x + tr.w // 2 - tl.get_width() // 2, tr.y + 4))

        if self._kiln_tab == "fire":
            self._draw_kiln_fire(player, dt)
        elif self._kiln_tab == "glaze":
            self._draw_kiln_glaze(player)

    def _draw_kiln_fire(self, player, dt=0.0):
        formed = [p for p in player.pottery_pieces if p.state == "formed"]

        if self._kiln_phase == "select_piece":
            self._kiln_select_rects.clear()
            if not formed:
                msg = self.small.render("No formed pieces. Shape clay at the Pottery Wheel first.", True, (180, 110, 60))
                self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2))
                return

            sub = self.small.render("Select a formed piece to fire:", True, _TEXT_DIM)
            self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 58))

            CELL_W, CELL_H, GAP, COLS = 180, 64, 8, 5
            gx0 = (SCREEN_W - (COLS * CELL_W + (COLS - 1) * GAP)) // 2
            for li, piece in enumerate(formed[:20]):
                col_i = li % COLS
                row_i = li // COLS
                rx = gx0 + col_i * (CELL_W + GAP)
                ry = 80 + row_i * (CELL_H + GAP)
                rect = pygame.Rect(rx, ry, CELL_W, CELL_H)
                self._kiln_select_rects[li] = (rect, piece)
                pygame.draw.rect(self.screen, _PANEL_BG, rect)
                pygame.draw.rect(self.screen, _PANEL_BORDER, rect, 2)

                biome_lbl = BIOME_DISPLAY_NAMES.get(piece.clay_biome, piece.clay_biome.title())
                shape_lbl = _SHAPE_LABELS.get(piece.shape, piece.shape.title())
                ns = self.small.render(f"{biome_lbl} {shape_lbl}", True, _TEXT_MAIN)
                self.screen.blit(ns, (rx + 6, ry + 8))

                thick_s = self.small.render(f"Thick {int(piece.thickness * 100)}%  Even {int(piece.evenness * 100)}%", True, _TEXT_DIM)
                self.screen.blit(thick_s, (rx + 6, ry + 28))

                ks = self.small.render("Click to fire", True, (100, 75, 45))
                self.screen.blit(ks, (rx + 6, ry + 46))

        elif self._kiln_phase == "firing":
            self._kiln_fire_tick(dt)
            self._draw_kiln_firing_minigame(player)

        elif self._kiln_phase == "result":
            self._draw_kiln_result(player)

    def _kiln_fire_tick(self, dt):
        if self._kiln_heat_held:
            self._kiln_temp_vel = min(1.0, self._kiln_temp_vel + 0.018)
        else:
            self._kiln_temp_vel = max(-0.45, self._kiln_temp_vel - 0.009)
        self._kiln_temp = max(0.0, min(1.0, self._kiln_temp + self._kiln_temp_vel * dt))
        self._kiln_time += dt

        # Track green-zone time
        if 0.35 <= self._kiln_temp <= 0.82:
            self._kiln_time_in_green += dt

        # Thermal shock: spending time above 0.85
        if self._kiln_temp > 0.85:
            self._kiln_shock_penalties += dt * 2

        # Event flashes
        if self._kiln_time >= 8.0 and not getattr(self, '_kiln_ev1_done', False):
            self._kiln_event_flash = ("Clay drying complete", 2.0)
            self._kiln_ev1_done = True
        if self._kiln_time >= 18.0 and not getattr(self, '_kiln_ev2_done', False):
            self._kiln_event_flash = ("Bisque stage reached", 2.0)
            self._kiln_ev2_done = True
        if self._kiln_time >= 28.0 and not getattr(self, '_kiln_ev3_done', False):
            self._kiln_event_flash = ("Vitrification zone!", 2.0)
            self._kiln_ev3_done = True

        # Tick flash timer
        if self._kiln_event_flash:
            msg, remaining = self._kiln_event_flash
            remaining -= dt
            if remaining <= 0:
                self._kiln_event_flash = None
            else:
                self._kiln_event_flash = (msg, remaining)

        if self._kiln_time >= self._kiln_total_time:
            self._finish_kiln_firing()

    def _draw_kiln_firing_minigame(self, player):
        piece = self._kiln_firing_piece
        if piece is None:
            return

        # Title row
        biome_lbl = BIOME_DISPLAY_NAMES.get(piece.clay_biome, piece.clay_biome.title())
        shape_lbl = _SHAPE_LABELS.get(piece.shape, piece.shape.title())
        sub = self.small.render(f"Firing: {biome_lbl} {shape_lbl}  —  HOLD SPACE to heat", True, _TEXT_DIM)
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 58))

        # Time bar
        bar_x, bar_y, bar_w, bar_h = 80, 80, SCREEN_W - 160, 18
        progress = min(1.0, self._kiln_time / self._kiln_total_time)
        pygame.draw.rect(self.screen, (40, 26, 14), (bar_x, bar_y, bar_w, bar_h))
        pygame.draw.rect(self.screen, (180, 120, 50), (bar_x, bar_y, int(bar_w * progress), bar_h))
        pygame.draw.rect(self.screen, _PANEL_BORDER, (bar_x, bar_y, bar_w, bar_h), 1)
        time_s = self.small.render(f"{self._kiln_time:.1f} / {self._kiln_total_time:.0f}s", True, _TEXT_DIM)
        self.screen.blit(time_s, (bar_x + bar_w + 6, bar_y))

        # Temperature gauge
        gauge_x = SCREEN_W // 2 - 12
        gauge_y, gauge_h = 115, 280
        gauge_w = 24
        pygame.draw.rect(self.screen, (30, 18, 8), (gauge_x, gauge_y, gauge_w, gauge_h))
        fill_h = int(gauge_h * self._kiln_temp)
        fill_y = gauge_y + gauge_h - fill_h
        fill_col = self._kiln_temp_color(self._kiln_temp)
        pygame.draw.rect(self.screen, fill_col, (gauge_x, fill_y, gauge_w, fill_h))

        # Zone markers on gauge
        for frac, label, color in [(0.35, "intact", (180, 200, 120)),
                                    (0.55, "fine",   (120, 200, 120)),
                                    (0.72, "master", (80, 220, 180)),
                                    (0.85, "crack",  (220, 60, 60))]:
            zy = int(gauge_y + gauge_h * (1.0 - frac))
            pygame.draw.line(self.screen, color, (gauge_x - 4, zy), (gauge_x + gauge_w + 4, zy), 1)
            zl = self.small.render(label, True, color)
            self.screen.blit(zl, (gauge_x + gauge_w + 6, zy - 7))

        pygame.draw.rect(self.screen, _PANEL_BORDER, (gauge_x, gauge_y, gauge_w, gauge_h), 2)
        temp_pct = self.small.render(f"{int(self._kiln_temp * 100)}%", True, _TEXT_MAIN)
        self.screen.blit(temp_pct, (gauge_x, gauge_y + gauge_h + 4))

        # Shock penalty indicator
        shock_lbl = self.small.render(f"Shock: {int(self._kiln_shock_penalties)}", True,
                                       (220, 80, 60) if self._kiln_shock_penalties > 1 else _TEXT_DIM)
        self.screen.blit(shock_lbl, (gauge_x - 60, gauge_y + gauge_h + 4))

        # HEAT button
        heat_rect = pygame.Rect(SCREEN_W // 2 - 60, SCREEN_H - 58, 120, 40)
        self._kiln_heat_rect = heat_rect
        pygame.draw.rect(self.screen, (120, 50, 20) if self._kiln_heat_held else (60, 30, 12), heat_rect)
        pygame.draw.rect(self.screen, _PANEL_BORDER, heat_rect, 2)
        hl = self.font.render("HEAT", True, (255, 180, 60) if self._kiln_heat_held else _TEXT_MAIN)
        self.screen.blit(hl, (heat_rect.x + heat_rect.w // 2 - hl.get_width() // 2, heat_rect.y + 8))

        # Event flash
        if self._kiln_event_flash:
            msg, _ = self._kiln_event_flash
            fs = self.font.render(msg, True, (255, 220, 80))
            self.screen.blit(fs, (SCREEN_W // 2 - fs.get_width() // 2, SCREEN_H // 2 - 20))

    def _kiln_temp_color(self, t):
        if t < 0.35:
            return (200, 180, 160)
        elif t < 0.55:
            return (230, 130, 60)
        elif t < 0.72:
            return (240, 200, 80)
        elif t < 0.85:
            return (160, 240, 160)
        else:
            return (240, 60, 40)

    def _finish_kiln_firing(self):
        piece = self._kiln_firing_piece
        if piece is None:
            self._kiln_phase = "select_piece"
            return
        total = self._kiln_total_time
        timing_score = min(1.0, self._kiln_time_in_green / (total * 0.6))
        # temp control: how centered was temp in the optimal band
        ctrl = max(0.0, 1.0 - self._kiln_shock_penalties * 0.08)
        # apply research bonus
        ctrl = min(1.0, ctrl + getattr(self, '_kiln_quality_bonus_cache', 0.0))
        apply_firing_result(piece, self._kiln_temp, timing_score, ctrl, int(self._kiln_shock_penalties))
        self._kiln_firing_result_piece = piece
        self._kiln_phase = "result"

    def _draw_kiln_result(self, player):
        piece = getattr(self, '_kiln_firing_result_piece', None)
        if piece is None:
            self._kiln_phase = "select_piece"
            return

        biome_lbl = BIOME_DISPLAY_NAMES.get(piece.clay_biome, piece.clay_biome.title())
        shape_lbl = _SHAPE_LABELS.get(piece.shape, piece.shape.title())
        level_colors = {"cracked": (180, 80, 60), "intact": (200, 160, 80),
                        "fine": (120, 200, 120), "masterwork": (80, 200, 230)}
        level_col = level_colors.get(piece.firing_level, _TEXT_MAIN)

        result_lbl = self.font.render(f"{biome_lbl} {shape_lbl} — {piece.firing_level.upper()}", True, level_col)
        self.screen.blit(result_lbl, (SCREEN_W // 2 - result_lbl.get_width() // 2, SCREEN_H // 2 - 60))

        q_lbl = self.small.render(f"Quality: {int(piece.firing_quality * 100)}%", True, _TEXT_DIM)
        self.screen.blit(q_lbl, (SCREEN_W // 2 - q_lbl.get_width() // 2, SCREEN_H // 2 - 30))

        notes_lbl = self.small.render("  ·  ".join(piece.texture_notes), True, _TEXT_DIM)
        self.screen.blit(notes_lbl, (SCREEN_W // 2 - notes_lbl.get_width() // 2, SCREEN_H // 2))

        # Collect button
        self._kiln_collect_rect = pygame.Rect(SCREEN_W // 2 - 70, SCREEN_H // 2 + 40, 140, 36)
        pygame.draw.rect(self.screen, (40, 65, 30), self._kiln_collect_rect)
        pygame.draw.rect(self.screen, _PANEL_BORDER, self._kiln_collect_rect, 2)
        cl = self.font.render("COLLECT", True, _TEXT_MAIN)
        self.screen.blit(cl, (self._kiln_collect_rect.x + self._kiln_collect_rect.w // 2 - cl.get_width() // 2,
                               self._kiln_collect_rect.y + 8))

    def _draw_kiln_glaze(self, player):
        fired = [p for p in player.pottery_pieces
                 if p.state == "fired" and p.firing_level in ("intact", "fine", "masterwork")]

        if self._glaze_piece_idx is None:
            # Piece selection
            self._glaze_piece_rects = {}
            if not fired:
                msg = self.small.render("No fired pieces available. Fire pieces in the FIRE tab first.", True, (180, 110, 60))
                self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2))
                return

            sub = self.small.render("Select a fired piece to glaze:", True, _TEXT_DIM)
            self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 58))

            CELL_W, CELL_H, GAP, COLS = 180, 64, 8, 5
            gx0 = (SCREEN_W - (COLS * CELL_W + (COLS - 1) * GAP)) // 2
            for li, piece in enumerate(fired[:20]):
                col_i = li % COLS
                row_i = li // COLS
                rx = gx0 + col_i * (CELL_W + GAP)
                ry = 80 + row_i * (CELL_H + GAP)
                rect = pygame.Rect(rx, ry, CELL_W, CELL_H)
                self._glaze_piece_rects[li] = (rect, piece)
                pygame.draw.rect(self.screen, _PANEL_BG, rect)
                pygame.draw.rect(self.screen, _PANEL_BORDER, rect, 2)
                biome_lbl = BIOME_DISPLAY_NAMES.get(piece.clay_biome, piece.clay_biome.title())
                shape_lbl = _SHAPE_LABELS.get(piece.shape, piece.shape.title())
                ns = self.small.render(f"{biome_lbl} {shape_lbl}", True, _TEXT_MAIN)
                self.screen.blit(ns, (rx + 6, ry + 8))
                lvl_s = self.small.render(piece.firing_level.title(), True, _TEXT_DIM)
                self.screen.blit(lvl_s, (rx + 6, ry + 28))
                ks = self.small.render("Select", True, (100, 75, 45))
                self.screen.blit(ks, (rx + 6, ry + 46))

        elif self._glaze_dust_key is None:
            # Glaze type selection
            piece = fired[self._glaze_piece_idx] if self._glaze_piece_idx < len(fired) else None
            if piece is None:
                self._glaze_piece_idx = None
                return

            sub = self.small.render("Choose a glaze (requires 2 gem dust):", True, _TEXT_DIM)
            self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 58))

            self._glaze_dust_rects = {}
            BTN_W, BTN_H = 130, 80
            glaze_items = list(GLAZE_TYPES.items())
            gx0 = (SCREEN_W - (len(glaze_items) * (BTN_W + 10))) // 2
            for i, (gkey, gdata) in enumerate(glaze_items):
                gx = gx0 + i * (BTN_W + 10)
                gy = SCREEN_H // 2 - BTN_H // 2
                grect = pygame.Rect(gx, gy, BTN_W, BTN_H)
                dust_id = gdata["dust_item"]
                avail = player.inventory.get(dust_id, 0)
                self._glaze_dust_rects[gkey] = grect
                can = avail >= 2
                pygame.draw.rect(self.screen, _PANEL_BG if can else (22, 14, 7), grect)
                pygame.draw.rect(self.screen, gdata["color"] if can else _TEXT_DIM, grect, 2)
                gl = self.small.render(gdata["label"], True, _TEXT_MAIN if can else _TEXT_DIM)
                self.screen.blit(gl, (gx + BTN_W // 2 - gl.get_width() // 2, gy + 10))
                al = self.small.render(f"({avail} dust)", True, _TEXT_DIM)
                self.screen.blit(al, (gx + BTN_W // 2 - al.get_width() // 2, gy + 42))
                pygame.draw.rect(self.screen, gdata["color"], (gx + 10, gy + 60, BTN_W - 20, 10))

            bk = pygame.Rect(10, SCREEN_H - 50, 80, 30)
            self._glaze_back_rect = bk
            pygame.draw.rect(self.screen, _PANEL_BG, bk)
            pygame.draw.rect(self.screen, _PANEL_BORDER, bk, 1)
            bt = self.small.render("Back", True, _TEXT_DIM)
            self.screen.blit(bt, (bk.x + 8, bk.y + 7))

        else:
            # Confirm application
            piece = fired[self._glaze_piece_idx] if self._glaze_piece_idx < len(fired) else None
            if piece is None:
                self._glaze_piece_idx = None
                self._glaze_dust_key = None
                return

            gdata = GLAZE_TYPES.get(self._glaze_dust_key, {})
            tier_up = {"intact": "fine", "fine": "masterwork", "masterwork": "masterwork"}
            new_level = tier_up.get(piece.firing_level, piece.firing_level)

            biome_lbl = BIOME_DISPLAY_NAMES.get(piece.clay_biome, piece.clay_biome.title())
            shape_lbl = _SHAPE_LABELS.get(piece.shape, piece.shape.title())

            preview = self.font.render(f"{biome_lbl} {shape_lbl}", True, _TEXT_MAIN)
            self.screen.blit(preview, (SCREEN_W // 2 - preview.get_width() // 2, SCREEN_H // 2 - 60))

            info = self.small.render(f"{piece.firing_level.title()} → {new_level.title()}  +  {gdata.get('label', '')} coating", True, _TEXT_DIM)
            self.screen.blit(info, (SCREEN_W // 2 - info.get_width() // 2, SCREEN_H // 2 - 30))

            cost_lbl = self.small.render("Cost: 2 gem dust", True, _TEXT_DIM)
            self.screen.blit(cost_lbl, (SCREEN_W // 2 - cost_lbl.get_width() // 2, SCREEN_H // 2))

            conf_rect = pygame.Rect(SCREEN_W // 2 + 10, SCREEN_H // 2 + 35, 120, 34)
            bk_rect   = pygame.Rect(SCREEN_W // 2 - 140, SCREEN_H // 2 + 35, 120, 34)
            self._glaze_confirm_rect = conf_rect
            self._glaze_cancel_rect  = bk_rect

            for rect, label, col in [(conf_rect, "APPLY", (40, 70, 40)), (bk_rect, "BACK", (50, 30, 14))]:
                pygame.draw.rect(self.screen, col, rect)
                pygame.draw.rect(self.screen, _PANEL_BORDER, rect, 2)
                tl = self.font.render(label, True, _TEXT_MAIN)
                self.screen.blit(tl, (rect.x + rect.w // 2 - tl.get_width() // 2, rect.y + 7))

    # ── Click Handlers ────────────────────────────────────────────────────────

    def _handle_pottery_wheel_click(self, pos, player):
        if self._wheel_phase == "select_clay":
            for n, rect in getattr(self, '_wheel_clay_btn_rects', {}).items():
                if rect.collidepoint(pos):
                    self._wheel_clay_loaded  = n
                    self._wheel_clay_budget  = n * 3
                    self._wheel_profile      = [min(WHEEL_MAX_RAD, max(WHEEL_MIN_RAD, (n * 3) // WHEEL_ROWS)) for _ in range(WHEEL_ROWS)]
                    self._wheel_undo_stack   = []
                    self._wheel_phase = "shaping"
                    return

        elif self._wheel_phase == "shaping":
            # Add clay button
            add_rect = getattr(self, '_wheel_add_clay_rect', None)
            if add_rect and add_rect.collidepoint(pos) and player.inventory.get("clay", 0) > 0:
                player.inventory["clay"] = player.inventory.get("clay", 0) - 1
                if player.inventory["clay"] <= 0:
                    del player.inventory["clay"]
                self._wheel_clay_budget += 3
                return

            # Row +/- buttons
            for row, rects in self._wheel_row_rects.items():
                if rects["minus"].collidepoint(pos) and self._wheel_profile[row] > WHEEL_MIN_RAD:
                    self._push_undo()
                    self._wheel_profile[row] -= 1
                    self._wheel_clay_budget += 1
                    return
                if rects["plus"].collidepoint(pos) and self._wheel_profile[row] < WHEEL_MAX_RAD and self._wheel_clay_budget > 0:
                    self._push_undo()
                    self._wheel_profile[row] += 1
                    self._wheel_clay_budget -= 1
                    return

            # Confirm → shaping done
            confirm = getattr(self, '_wheel_confirm_rect', None)
            if confirm and confirm.collidepoint(pos):
                self._wheel_phase = "confirm"
                return

        elif self._wheel_phase == "confirm":
            acc = getattr(self, '_wheel_accept_rect', None)
            bk  = getattr(self, '_wheel_back_rect',   None)
            if acc and acc.collidepoint(pos):
                self._complete_pottery_wheel(player)
            elif bk and bk.collidepoint(pos):
                self._wheel_phase = "shaping"

    def _complete_pottery_wheel(self, player):
        profile = list(self._wheel_profile)
        thick   = profile_thickness(profile)
        even    = profile_evenness(profile)
        biodome = getattr(player, '_last_biodome', 'temperate')
        if hasattr(player, 'world'):
            px = int(player.x // 32)
            biodome = player.world.get_biodome(px)

        # Map biodome to clay biome profile key
        clay_biome_map = {"wetland": "wetland", "river": "river", "swamp": "wetland",
                          "tropical": "tropical", "jungle": "tropical"}
        clay_biome = clay_biome_map.get(biodome, "temperate")

        piece = player._pottery_gen.generate(clay_biome, profile, thick, even)

        # Spend clay (loaded chunks already reserved; excess refunded)
        clay_used = max(1, self._wheel_clay_loaded - max(0, self._wheel_clay_budget // 3))
        # clay was already removed from inventory on load; just track the piece
        player.pottery_pieces.append(piece)
        player.pending_notifications.append(("Pottery", f"{piece.shape.title()} formed", None))

        # Reset wheel state
        self._wheel_phase = "select_clay"
        self._wheel_undo_stack = []
        self.active_panel = None
        self.refinery_open = False

    def _handle_pottery_kiln_click(self, pos, player):
        # Tab switching
        for tkey, trect in getattr(self, '_kiln_tab_rects', {}).items():
            if trect.collidepoint(pos):
                self._kiln_tab = tkey
                self._kiln_phase = "select_piece"
                self._glaze_piece_idx = None
                self._glaze_dust_key  = None
                return

        if self._kiln_tab == "fire":
            self._handle_kiln_fire_click(pos, player)
        else:
            self._handle_kiln_glaze_click(pos, player)

    def _handle_kiln_fire_click(self, pos, player):
        if self._kiln_phase == "select_piece":
            for li, (rect, piece) in self._kiln_select_rects.items():
                if rect.collidepoint(pos):
                    self._start_kiln_firing(piece, player)
                    return

        elif self._kiln_phase == "firing":
            heat_rect = getattr(self, '_kiln_heat_rect', None)
            if heat_rect and heat_rect.collidepoint(pos):
                self._kiln_heat_held = True

        elif self._kiln_phase == "result":
            collect = getattr(self, '_kiln_collect_rect', None)
            if collect and collect.collidepoint(pos):
                self._collect_kiln_result(player)

    def _start_kiln_firing(self, piece, player):
        self._kiln_firing_piece    = piece
        self._kiln_phase           = "firing"
        self._kiln_temp            = 0.0
        self._kiln_temp_vel        = 0.0
        self._kiln_time            = 0.0
        self._kiln_time_in_green   = 0.0
        self._kiln_shock_penalties = 0.0
        self._kiln_heat_held       = False
        self._kiln_event_flash     = None
        self._kiln_ev1_done        = False
        self._kiln_ev2_done        = False
        self._kiln_ev3_done        = False
        self._kiln_quality_bonus_cache = getattr(player, 'kiln_quality_bonus', 0.0)

    def _collect_kiln_result(self, player):
        piece = getattr(self, '_kiln_firing_result_piece', None)
        if piece is None:
            self._kiln_phase = "select_piece"
            return

        output_id = get_output_item(piece)
        player._add_item(output_id)

        # Track discovery
        if piece.firing_level != "cracked":
            key = f"{piece.clay_biome}_{piece.firing_level}"
            player.discovered_pottery.add(key)
            player.pending_notifications.append(("Pottery", f"{piece.shape.title()} fired: {piece.firing_level.title()}", None))

        self._kiln_phase = "select_piece"
        self._kiln_firing_result_piece = None

    def _handle_kiln_glaze_click(self, pos, player):
        fired = [p for p in player.pottery_pieces
                 if p.state == "fired" and p.firing_level in ("intact", "fine", "masterwork")]

        if self._glaze_piece_idx is None:
            for li, (rect, _) in getattr(self, '_glaze_piece_rects', {}).items():
                if rect.collidepoint(pos) and li < len(fired):
                    self._glaze_piece_idx = li
                    return

        elif self._glaze_dust_key is None:
            bk = getattr(self, '_glaze_back_rect', None)
            if bk and bk.collidepoint(pos):
                self._glaze_piece_idx = None
                return
            for gkey, grect in getattr(self, '_glaze_dust_rects', {}).items():
                if grect.collidepoint(pos):
                    dust_id = GLAZE_TYPES[gkey]["dust_item"]
                    if player.inventory.get(dust_id, 0) >= 2:
                        self._glaze_dust_key = gkey
                    return

        else:
            piece = fired[self._glaze_piece_idx] if self._glaze_piece_idx < len(fired) else None
            conf = getattr(self, '_glaze_confirm_rect', None)
            canc = getattr(self, '_glaze_cancel_rect', None)
            if canc and canc.collidepoint(pos):
                self._glaze_dust_key = None
                return
            if conf and conf.collidepoint(pos) and piece is not None:
                self._apply_glaze(piece, player)

    def _apply_glaze(self, piece, player):
        gkey = self._glaze_dust_key
        gdata = GLAZE_TYPES.get(gkey, {})
        dust_id = gdata.get("dust_item")
        if dust_id and player.inventory.get(dust_id, 0) >= 2:
            player.inventory[dust_id] -= 2
            if player.inventory[dust_id] <= 0:
                del player.inventory[dust_id]

            tier_up = {"intact": "fine", "fine": "masterwork", "masterwork": "masterwork"}
            piece.firing_level = tier_up.get(piece.firing_level, piece.firing_level)
            piece.state = "glazed"
            piece.glaze_type = gkey

            # Swap for the new item
            old_id = get_output_item(piece)
            # Piece stays in pottery_pieces; buff item stays in inventory already granted
            # Just update discovery
            key = f"{piece.clay_biome}_{piece.firing_level}"
            player.discovered_pottery.add(key)
            player.pending_notifications.append(("Pottery", f"Glazed with {gdata.get('label', gkey)}", None))

        self._glaze_piece_idx = None
        self._glaze_dust_key  = None

    # ── Keyboard Handlers ─────────────────────────────────────────────────────

    def handle_pottery_keydown(self, key, player):
        if key == pygame.K_ESCAPE:
            if self._wheel_phase == "shaping":
                self._wheel_phase = "select_clay"
            elif self._wheel_phase == "confirm":
                self._wheel_phase = "shaping"
            elif self._kiln_phase == "result":
                self._kiln_phase = "select_piece"
            elif self._glaze_piece_idx is not None:
                if self._glaze_dust_key is not None:
                    self._glaze_dust_key = None
                else:
                    self._glaze_piece_idx = None
            else:
                self.active_panel = None
                self.refinery_open = False

        elif key == pygame.K_RETURN or key == pygame.K_KP_ENTER:
            if self._wheel_phase == "shaping":
                self._wheel_phase = "confirm"
            elif self._wheel_phase == "confirm":
                self._complete_pottery_wheel(player)

        elif key == pygame.K_z:
            if self._wheel_phase == "shaping" and self._wheel_undo_stack:
                self._wheel_profile = self._wheel_undo_stack.pop()

    def handle_pottery_keys(self, keys, dt, player):
        from blocks import POTTERY_KILN_BLOCK as _PKB
        if hasattr(self, 'refinery_block_id') and self.refinery_block_id == _PKB:
            self._kiln_heat_held = bool(keys[pygame.K_SPACE])
        # Spin wheel animation
        if self._wheel_phase in ("shaping", "confirm"):
            self._wheel_spin_angle = (self._wheel_spin_angle + dt * 120) % 360

    def _handle_pottery_wheel_drag(self, pos, buttons):
        if self._wheel_phase != "shaping":
            self._wheel_drag_row = None
            return
        if not buttons[0]:
            self._wheel_drag_row = None
            return
        # Detect which row is being dragged via bar rect
        for row, rects in self._wheel_row_rects.items():
            bar = rects.get("bar")
            if bar is None:
                continue
            if bar.y <= pos[1] <= bar.y + bar.height:
                if self._wheel_drag_row is None:
                    self._push_undo()
                self._wheel_drag_row = row
                # Map x position within bar to radius
                bar_x, bar_w = bar.x, bar.w
                frac = max(0.0, min(1.0, (pos[0] - bar_x) / bar_w))
                new_rad = max(WHEEL_MIN_RAD, min(WHEEL_MAX_RAD, round(frac * WHEEL_MAX_RAD)))
                delta = new_rad - self._wheel_profile[row]
                if delta > 0 and self._wheel_clay_budget >= delta:
                    self._wheel_clay_budget -= delta
                    self._wheel_profile[row] = new_rad
                elif delta < 0:
                    self._wheel_clay_budget += abs(delta)
                    self._wheel_profile[row] = new_rad
                return

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _push_undo(self):
        self._wheel_undo_stack.append(list(self._wheel_profile))
        if len(self._wheel_undo_stack) > 20:
            self._wheel_undo_stack.pop(0)

    def _pottery_glaze_arts_unlocked(self, player):
        research = getattr(self, '_research', None)
        if research is None:
            research = getattr(player, '_research', None)
        if research is None:
            return False
        node = research.nodes.get("glaze_arts")
        return node is not None and node.unlocked


def _darken_color(c, amt):
    return (max(0, c[0] - amt), max(0, c[1] - amt), max(0, c[2] - amt))
