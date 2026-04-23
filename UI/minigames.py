import pygame
from ._data import RARITY_LABEL
from constants import SCREEN_W, SCREEN_H
from gemstones import (render_rough_gem, render_gem, GEM_TYPES,
                       RARITY_COLORS as GEM_RARITY_COLORS, GEM_CUT_DESCS,
                       get_fault_points, apply_cracking_result)
from fossils import (render_fossil, generate_prep_grid, apply_preparation_result,
                     FOSSIL_AGE_COLORS)
from fish import FISH_TYPES, FISH_RARITY_COLORS
from rocks import RARITY_COLORS
from items import ITEMS


class MinigamesMixin:

    _FPREP_CELL_SIZES = {"fragment": 68, "small": 56, "medium": 46, "large": 40, "complete": 34}
    _FPREP_GAP = 4

    # ------------------------------------------------------------------
    # Bird observation
    # ------------------------------------------------------------------

    def open_bird_observation(self, bird):
        if self._bird_obs_active:
            return
        self._bird_obs_active    = True
        self._bird_obs_bird      = bird
        self._bird_obs_timer     = 0.0
        self._bird_obs_failed    = False
        self._bird_obs_fail_timer = 0.0

    def _draw_bird_observation_overlay(self, player):
        PANEL_W, PANEL_H = 200, 150
        px = SCREEN_W - PANEL_W - 12
        py = SCREEN_H - PANEL_H - 60

        surf = pygame.Surface((PANEL_W, PANEL_H), pygame.SRCALPHA)
        surf.fill((15, 20, 30, 210))
        self.screen.blit(surf, (px, py))
        pygame.draw.rect(self.screen, (80, 150, 200), (px, py, PANEL_W, PANEL_H), 2)

        bird = self._bird_obs_bird
        already_seen = bird.SPECIES in player.birds_observed

        title = "OBSERVING..." if not self._bird_obs_failed else "BIRD FLEW AWAY!"
        title_col = (180, 220, 255) if not self._bird_obs_failed else (255, 120, 80)
        ts = self.small.render(title, True, title_col)
        self.screen.blit(ts, (px + PANEL_W // 2 - ts.get_width() // 2, py + 6))

        bird_surf = pygame.Surface((bird.W * 3, bird.H * 3), pygame.SRCALPHA)
        bird_surf.fill((0, 0, 0, 0))
        col = bird.BODY_COLOR
        wing_col = bird.WING_COLOR
        W2, H2 = bird.W * 3, bird.H * 3
        pygame.draw.ellipse(bird_surf, wing_col, (0, H2 // 3, W2, H2 // 2))
        pygame.draw.ellipse(bird_surf, col, (W2 // 6, H2 // 3, W2 * 2 // 3, H2 // 2))
        pygame.draw.circle(bird_surf, bird.HEAD_COLOR, (W2 - W2 // 5, H2 // 4), H2 // 5)
        pygame.draw.rect(bird_surf, bird.ACCENT_COLOR,
                         (W2 // 6, H2 // 3 + H2 // 8, W2 // 2, H2 // 5))
        self.screen.blit(bird_surf, (px + PANEL_W // 2 - W2 // 2, py + 22))

        if already_seen or self._bird_obs_timer >= 2.0:
            name_str = bird.SPECIES.replace("_", " ").title()
            name_col = (255, 220, 100)
        else:
            full = bird.SPECIES.replace("_", " ").title()
            chars_shown = max(1, int(len(full) * (self._bird_obs_timer / 2.0)))
            name_str = full[:chars_shown] + "?" * (len(full) - chars_shown)
            name_col = (180, 200, 220)
        ns = self.small.render(name_str, True, name_col)
        self.screen.blit(ns, (px + PANEL_W // 2 - ns.get_width() // 2, py + 22 + bird.H * 3 + 4))

        rarity_cols = {"common": (180, 200, 180), "uncommon": (120, 200, 255),
                       "rare": (200, 130, 255)}
        rc = rarity_cols.get(bird.RARITY, (200, 200, 200))
        rs = self.small.render(bird.RARITY.upper(), True, rc)
        self.screen.blit(rs, (px + PANEL_W // 2 - rs.get_width() // 2,
                               py + 22 + bird.H * 3 + 18))

        bar_y = py + PANEL_H - 22
        bar_w = PANEL_W - 24
        pygame.draw.rect(self.screen, (30, 40, 50), (px + 12, bar_y, bar_w, 10))
        fill = int(bar_w * min(1.0, self._bird_obs_timer / 2.0))
        if not self._bird_obs_failed and fill > 0:
            pygame.draw.rect(self.screen, (80, 200, 130), (px + 12, bar_y, fill, 10))
        pygame.draw.rect(self.screen, (80, 150, 200), (px + 12, bar_y, bar_w, 10), 1)

        hint = "Stay still!" if not self._bird_obs_failed else ""
        hs = self.small.render(hint, True, (140, 180, 200))
        self.screen.blit(hs, (px + PANEL_W // 2 - hs.get_width() // 2, py + PANEL_H - 38))

    # ------------------------------------------------------------------
    # Gem Cutter mini-game
    # ------------------------------------------------------------------

    def _draw_gem_cutter(self, player, dt=0.0):
        import math as _math

        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 225))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("GEM CUTTER", True, (110, 230, 205))
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))

        rough_gems = [(i, g) for i, g in enumerate(player.gems) if g.state == "rough"]
        phase = self._gc_phase

        if phase == "show_seq":
            self._gc_seq_timer -= dt
            if self._gc_seq_timer <= 0:
                self._gc_seq_idx += 1
                if self._gc_seq_idx >= len(self._gc_fault_pts):
                    self._gc_phase = "player_turn"
                    self._gc_fault_lit = -1
                else:
                    self._gc_fault_lit = self._gc_seq_idx
                    self._gc_seq_timer = 0.6
            else:
                self._gc_fault_lit = self._gc_seq_idx

        if phase == "reveal":
            self._gc_reveal_timer -= dt
            if self._gc_reveal_timer <= 0:
                self._gc_phase = "choose_cut"
                self._gc_reveal_timer = 0.0

        if phase == "select":
            hint = self.small.render("ESC to close  |  Select a rough gem to begin cracking", True, (75, 130, 115))
            self.screen.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, 26))

            if not rough_gems:
                msg = self.font.render("No rough gems to cut.  Mine Gem Deposits!", True, (70, 120, 105))
                self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2))
                return

            CELL, GAP, COLS = 90, 10, 8
            gx0 = (SCREEN_W - (COLS * CELL + (COLS - 1) * GAP)) // 2
            gy0 = 48
            self._gc_select_rects.clear()
            for j, (idx, gem) in enumerate(rough_gems):
                col = j % COLS
                row = j // COLS
                x = gx0 + col * (CELL + GAP)
                y = gy0 + row * (CELL + GAP)
                if y + CELL > SCREEN_H - 40:
                    break
                rect = pygame.Rect(x, y, CELL, CELL)
                self._gc_select_rects[idx] = rect
                rar_col = GEM_RARITY_COLORS.get(gem.rarity, (120, 120, 120))
                pygame.draw.rect(self.screen, (22, 35, 32), rect)
                pygame.draw.rect(self.screen, rar_col, rect, 2)
                img = render_rough_gem(gem, 68)
                self.screen.blit(img, (x + (CELL - 68) // 2, y + (CELL - 68) // 2 - 5))
                ns = self.small.render(self._fit_label(gem.gem_type.replace("_", " "), CELL - 4), True, (105, 175, 155))
                self.screen.blit(ns, (x + CELL // 2 - ns.get_width() // 2, y + CELL - 14))
            return

        gem = player.gems[self._gc_gem_idx]
        cx_gem = SCREEN_W // 2
        cy_gem = SCREEN_H // 2 - 30

        preview_size = 200
        if phase in ("show_seq", "player_turn"):
            img = render_rough_gem(gem, preview_size)
        elif phase == "reveal":
            img = render_rough_gem(gem, preview_size)
        else:
            img = render_gem(gem, preview_size)
        self.screen.blit(img, (cx_gem - preview_size // 2, cy_gem - preview_size // 2))

        pts_offset_x = cx_gem - 110
        pts_offset_y = cy_gem - 110
        fault_pts_screen = [
            (pts_offset_x + px, pts_offset_y + py)
            for px, py in self._gc_fault_pts
        ]

        if phase in ("show_seq", "player_turn"):
            self._gc_fault_rects = []
            for i, (fx, fy) in enumerate(fault_pts_screen):
                r = 14
                rect = pygame.Rect(fx - r, fy - r, r * 2, r * 2)
                self._gc_fault_rects.append(rect)

                already_clicked = i < len(self._gc_seq_clicks)
                is_lit = (i == self._gc_fault_lit)
                is_next = (i == len(self._gc_seq_clicks) and phase == "player_turn")

                if already_clicked:
                    col = (50, 200, 120)
                    alpha = 220
                elif is_lit:
                    col = (255, 240, 80)
                    alpha = 255
                elif is_next:
                    col = (80, 180, 255)
                    alpha = 200
                else:
                    col = (160, 140, 120)
                    alpha = 140

                glow_surf = pygame.Surface((r * 4, r * 4), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, col + (60,), (r * 2, r * 2), r * 2)
                self.screen.blit(glow_surf, (fx - r * 2, fy - r * 2))
                pygame.draw.circle(self.screen, col, (fx, fy), r)

                if is_lit or already_clicked:
                    num_s = self.font.render(str(i + 1), True, (20, 20, 20))
                    self.screen.blit(num_s, (fx - num_s.get_width() // 2, fy - num_s.get_height() // 2))

            if phase == "show_seq":
                status = self.font.render("MEMORISE THE ORDER!", True, (255, 230, 80))
            else:
                expected = len(self._gc_seq_clicks)
                status = self.font.render(
                    f"Tap point {expected + 1} of {len(self._gc_fault_pts)}  —  Mistakes: {self._gc_mistakes}",
                    True, (160, 220, 200)
                )
            self.screen.blit(status, (SCREEN_W // 2 - status.get_width() // 2, cy_gem + preview_size // 2 + 18))

        elif phase == "reveal":
            prog = 1.0 - self._gc_reveal_timer / 1.2
            import random as _rnd
            rng2 = _rnd.Random(gem.seed ^ 0xABC)
            n_sparks = int(prog * 24)
            for _ in range(n_sparks):
                a = rng2.uniform(0, 2 * _math.pi)
                d = rng2.uniform(10, int(preview_size * 0.7 * prog))
                sx = int(cx_gem + d * _math.cos(a))
                sy = int(cy_gem - 30 + d * _math.sin(a))
                sc_spark = rng2.choice([gem.primary_color, gem.secondary_color, (255, 255, 200)])
                pygame.draw.circle(self.screen, sc_spark, (sx, sy), rng2.randint(2, 5))

            pct_s = self.font.render("Cracking open...", True, (200, 230, 210))
            self.screen.blit(pct_s, (SCREEN_W // 2 - pct_s.get_width() // 2, cy_gem + preview_size // 2 + 18))

        elif phase == "choose_cut":
            header = self.font.render("GEM REVEALED!", True, (140, 255, 200))
            self.screen.blit(header, (SCREEN_W // 2 - header.get_width() // 2, cy_gem - preview_size // 2 - 30))

            info_y = cy_gem + preview_size // 2 + 10
            rar_col = GEM_RARITY_COLORS.get(gem.rarity, (120, 120, 120))
            clarity_s = self.small.render(f"Clarity: {gem.clarity}  |  Inclusion: {gem.inclusion.replace('_', ' ')}",
                                          True, (145, 210, 185))
            self.screen.blit(clarity_s, (SCREEN_W // 2 - clarity_s.get_width() // 2, info_y))
            info_y += 18
            if gem.optical_effect != "none":
                opt_s = self.small.render(f"Optical effect hidden in this gem: {gem.optical_effect.replace('_', ' ')}",
                                          True, (200, 155, 255))
                self.screen.blit(opt_s, (SCREEN_W // 2 - opt_s.get_width() // 2, info_y))
                info_y += 18

            cut_label = self.font.render("Choose a cut:", True, (110, 200, 180))
            self.screen.blit(cut_label, (SCREEN_W // 2 - cut_label.get_width() // 2, info_y + 4))
            info_y += 32

            tdef = GEM_TYPES[gem.gem_type]
            cuts = tdef["available_cuts"]
            BTN_W, BTN_H, BTN_GAP = 160, 48, 12
            total_w = len(cuts) * BTN_W + (len(cuts) - 1) * BTN_GAP
            bx0 = SCREEN_W // 2 - total_w // 2
            self._gc_cut_rects.clear()
            for ci, cut_name in enumerate(cuts):
                bx = bx0 + ci * (BTN_W + BTN_GAP)
                br = pygame.Rect(bx, info_y, BTN_W, BTN_H)
                self._gc_cut_rects[cut_name] = br
                pygame.draw.rect(self.screen, (22, 48, 44), br)
                pygame.draw.rect(self.screen, (80, 195, 165), br, 2)
                cut_title = self.small.render(cut_name.replace("_", " ").title(), True, (130, 215, 195))
                self.screen.blit(cut_title, (bx + BTN_W // 2 - cut_title.get_width() // 2, info_y + 8))
                cut_desc_short = GEM_CUT_DESCS.get(cut_name, "").split(" —")[0]
                cd = self.small.render(self._fit_label(cut_desc_short, BTN_W - 8), True, (72, 140, 122))
                self.screen.blit(cd, (bx + BTN_W // 2 - cd.get_width() // 2, info_y + 26))

    # ------------------------------------------------------------------
    # Fossil Prep Table mini-game
    # ------------------------------------------------------------------

    def _fprep_reset(self):
        self._fprep_phase     = "select"
        self._fprep_fossil    = None
        self._fprep_grid      = None
        self._fprep_n         = 0
        self._fprep_tool      = "chisel"
        self._fprep_damage    = 0
        self._fprep_cell_hits = None
        self._fprep_cleared   = None
        self._fprep_reveal_t  = 0.0
        self._fprep_hover_cell = None
        self._fprep_done_btn  = None

    def _draw_fossil_table(self, player, dt=0.0):
        import math as _math

        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 225))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("FOSSIL PREP TABLE", True, (200, 175, 120))
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 8))

        unprepared = [(i, f) for i, f in enumerate(player.fossils) if not f.prepared]
        phase = self._fprep_phase

        if phase == "select":
            self._fprep_select_rects.clear()
            if not unprepared:
                msg = self.font.render("No raw fossils to prepare.", True, (150, 135, 100))
                self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2 - 30))
                sub = self.small.render("Mine Fossil Deposits underground to find specimens.", True, (100, 90, 68))
                self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, SCREEN_H // 2 + 8))
                return

            header = self.small.render("Select a fossil to prepare:", True, (170, 150, 110))
            self.screen.blit(header, (SCREEN_W // 2 - header.get_width() // 2, 38))

            CELL = 72
            GAP  = 10
            COLS = min(len(unprepared), 8)
            total_w = COLS * CELL + (COLS - 1) * GAP
            gx0 = SCREEN_W // 2 - total_w // 2
            gy0 = 68

            for slot, (orig_idx, fossil) in enumerate(unprepared[:COLS * 4]):
                col = slot % COLS
                row = slot // COLS
                x = gx0 + col * (CELL + GAP)
                y = gy0 + row * (CELL + GAP)
                rect = pygame.Rect(x, y, CELL, CELL)
                self._fprep_select_rects[orig_idx] = rect

                pygame.draw.rect(self.screen, (38, 32, 22), rect)
                pygame.draw.rect(self.screen, (110, 95, 68), rect, 2)

                grey_surf = render_fossil(fossil, 56)
                grey_copy = grey_surf.copy()
                grey_copy.fill((80, 70, 55, 200), special_flags=pygame.BLEND_RGBA_MULT)
                self.screen.blit(grey_copy, (x + (CELL - 56) // 2, y + (CELL - 56) // 2 - 4))

                q = self.font.render("?", True, (200, 180, 130))
                self.screen.blit(q, (x + CELL // 2 - q.get_width() // 2, y + CELL // 2 - q.get_height() // 2))

                size_s = self.small.render(fossil.size.title(), True, (140, 125, 95))
                self.screen.blit(size_s, (x + CELL // 2 - size_s.get_width() // 2, y + CELL - 13))

            hint = self.small.render("Click a specimen to begin preparation", True, (100, 90, 68))
            self.screen.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, SCREEN_H - 30))

        elif phase == "prep":
            fossil = self._fprep_fossil
            n      = self._fprep_n
            cs     = self._FPREP_CELL_SIZES.get(fossil.size, 46)
            gap    = self._FPREP_GAP
            grid_w = n * cs + (n - 1) * gap
            grid_h = grid_w
            gx = SCREEN_W // 2 - grid_w // 2
            gy = SCREEN_H // 2 - grid_h // 2 + 10
            self._fprep_grid_rect = pygame.Rect(gx, gy, grid_w, grid_h)
            self._fprep_cell_size = cs

            fossil_surf = render_fossil(fossil, n * cs)

            mx, my = pygame.mouse.get_pos()
            hover = None
            if self._fprep_grid_rect.collidepoint(mx, my):
                hc = (mx - gx) // (cs + gap)
                hr = (my - gy) // (cs + gap)
                if 0 <= hr < n and 0 <= hc < n:
                    hover = (hr, hc)
            self._fprep_hover_cell = hover

            tb_y = gy - 44
            for ti, (tool_key, tool_label) in enumerate([("chisel", "CHISEL"), ("brush", "BRUSH")]):
                tb_x = SCREEN_W // 2 - 100 + ti * 110
                tb_rect = pygame.Rect(tb_x, tb_y, 90, 30)
                selected = (self._fprep_tool == tool_key)
                col = (160, 130, 80) if selected else (55, 48, 35)
                border = (220, 185, 100) if selected else (100, 88, 65)
                pygame.draw.rect(self.screen, col, tb_rect, border_radius=4)
                pygame.draw.rect(self.screen, border, tb_rect, 2, border_radius=4)
                tls = self.small.render(tool_label, True, (240, 220, 160) if selected else (140, 125, 95))
                self.screen.blit(tls, (tb_x + 45 - tls.get_width() // 2, tb_y + 8))
                if tool_key == "chisel":
                    self._fprep_chisel_btn = tb_rect
                else:
                    self._fprep_brush_btn = tb_rect

            for row in range(n):
                for col in range(n):
                    cx_cell = gx + col * (cs + gap)
                    cy_cell = gy + row * (cs + gap)
                    cell_rect = pygame.Rect(cx_cell, cy_cell, cs, cs)
                    cleared = self._fprep_cleared[row][col]

                    if cleared:
                        src_rect = pygame.Rect(col * cs, row * cs, cs, cs)
                        self.screen.blit(fossil_surf, (cx_cell, cy_cell), src_rect)
                        pygame.draw.rect(self.screen, (80, 70, 50, 80), cell_rect, 1)
                    else:
                        cell = self._fprep_grid[row][col]
                        base = (50, 44, 32)
                        is_hover = (hover == (row, col))
                        is_chisel_warning = (is_hover and self._fprep_tool == "chisel"
                                             and cell["type"] == "fragile")
                        if is_hover:
                            base = (72, 62, 44) if not is_chisel_warning else (80, 40, 32)
                        pygame.draw.rect(self.screen, base, cell_rect)

                        import random as _rnd
                        cell_rng = _rnd.Random(fossil.seed ^ (row * 31 + col * 97))
                        for _ in range(3):
                            lx1 = cx_cell + cell_rng.randint(2, cs - 2)
                            ly1 = cy_cell + cell_rng.randint(2, cs - 2)
                            lx2 = lx1 + cell_rng.randint(-8, 8)
                            ly2 = ly1 + cell_rng.randint(-4, 4)
                            pygame.draw.line(self.screen, (62, 55, 40), (lx1, ly1), (lx2, ly2))

                        if is_chisel_warning:
                            warn = self.small.render("!", True, (220, 80, 60))
                            self.screen.blit(warn, (cx_cell + cs // 2 - warn.get_width() // 2,
                                                    cy_cell + cs // 2 - warn.get_height() // 2))

                        hits = self._fprep_cell_hits[row][col]
                        if hits > 0:
                            needed = cell["hits_brush"]
                            for di in range(hits):
                                dx2 = cx_cell + 4 + di * 7
                                pygame.draw.circle(self.screen, (180, 160, 100), (dx2, cy_cell + cs - 5), 3)

                        border_col = (78, 68, 50)
                        pygame.draw.rect(self.screen, border_col, cell_rect, 1)

            bar_x, bar_y = gx, gy + grid_h + 14
            bar_w = grid_w
            bar_h = 14
            integ = max(0, 100 - self._fprep_damage)
            integ_norm = integ / 100.0
            fill_col = (
                (80, 180, 80) if integ > 70 else
                (200, 170, 50) if integ > 40 else
                (200, 60, 50)
            )
            pygame.draw.rect(self.screen, (30, 26, 18), (bar_x, bar_y, bar_w, bar_h))
            pygame.draw.rect(self.screen, fill_col, (bar_x, bar_y, int(bar_w * integ_norm), bar_h))
            pygame.draw.rect(self.screen, (80, 70, 50), (bar_x, bar_y, bar_w, bar_h), 1)
            integ_s = self.small.render(f"Integrity: {integ}%", True, (180, 165, 130))
            self.screen.blit(integ_s, (bar_x + bar_w // 2 - integ_s.get_width() // 2, bar_y + 18))

            if self._fprep_tool == "chisel":
                hint_txt = "Chisel: 1 click (hard) | Damages soft/fragile zones"
            else:
                hint_txt = "Brush: safe on all zones | 1–3 clicks to clear"
            hint_s = self.small.render(hint_txt, True, (100, 90, 65))
            self.screen.blit(hint_s, (SCREEN_W // 2 - hint_s.get_width() // 2, SCREEN_H - 24))

        elif phase == "reveal":
            fossil = self._fprep_fossil
            self._fprep_reveal_t = min(1.0, self._fprep_reveal_t + dt / 2.0)
            t = self._fprep_reveal_t

            n   = self._fprep_n
            cs  = self._FPREP_CELL_SIZES.get(fossil.size, 46)
            min_size = n * cs
            max_size = 160
            cur_size = int(min_size + (max_size - min_size) * t)
            cx_c = SCREEN_W // 2
            cy_c = SCREEN_H // 2 - 20
            img = render_fossil(fossil, cur_size)
            self.screen.blit(img, (cx_c - cur_size // 2, cy_c - cur_size // 2))

            import random as _rnd2
            rng2 = _rnd2.Random(fossil.seed ^ 0xF055117)
            n_sparks = int(t * 30)
            for _ in range(n_sparks):
                a = rng2.uniform(0, 2 * _math.pi)
                d = rng2.uniform(10, int(cur_size * 0.65 * t))
                sx = int(cx_c + d * _math.cos(a))
                sy = int(cy_c + d * _math.sin(a))
                sc = rng2.choice([fossil.primary_color, fossil.secondary_color, (240, 220, 160)])
                pygame.draw.circle(self.screen, sc, (sx, sy), rng2.randint(2, 5))

            alpha = int(min(255, t * 2 * 255))
            rar_col = RARITY_COLORS.get(fossil.rarity, (180, 160, 120))

            if t > 0.5:
                name_surf = self.font.render(
                    fossil.fossil_type.replace("_", " ").title(), True, (240, 215, 140))
                name_surf.set_alpha(alpha)
                self.screen.blit(name_surf, (cx_c - name_surf.get_width() // 2, cy_c + cur_size // 2 + 12))

            if t > 0.65:
                rar_surf = self.small.render(RARITY_LABEL.get(fossil.rarity, fossil.rarity.title()),
                                             True, rar_col)
                rar_surf.set_alpha(alpha)
                self.screen.blit(rar_surf, (cx_c - rar_surf.get_width() // 2, cy_c + cur_size // 2 + 34))

            if t > 0.80:
                dmg_label = (
                    "Perfect preparation!" if self._fprep_damage == 0 else
                    f"Integrity loss: {self._fprep_damage}%"
                )
                dmg_col = (80, 200, 120) if self._fprep_damage == 0 else (200, 150, 80)
                dmg_s = self.small.render(dmg_label, True, dmg_col)
                dmg_s.set_alpha(alpha)
                self.screen.blit(dmg_s, (cx_c - dmg_s.get_width() // 2, cy_c + cur_size // 2 + 52))

            if t >= 1.0:
                done_rect = pygame.Rect(cx_c - 70, cy_c + cur_size // 2 + 74, 140, 34)
                pygame.draw.rect(self.screen, (60, 100, 60), done_rect, border_radius=6)
                pygame.draw.rect(self.screen, (100, 180, 100), done_rect, 2, border_radius=6)
                btn_s = self.small.render("ADD TO COLLECTION", True, (180, 240, 180))
                self.screen.blit(btn_s, (cx_c - btn_s.get_width() // 2, done_rect.y + 9))
                self._fprep_done_btn = done_rect

    def _handle_fossil_table_click(self, pos, player):
        phase = self._fprep_phase

        if phase == "select":
            for orig_idx, rect in self._fprep_select_rects.items():
                if rect.collidepoint(pos):
                    fossil = player.fossils[orig_idx]
                    self._fprep_fossil = fossil
                    self._fprep_grid, self._fprep_n = generate_prep_grid(fossil)
                    n = self._fprep_n
                    self._fprep_cell_hits = [[0] * n for _ in range(n)]
                    self._fprep_cleared   = [[False] * n for _ in range(n)]
                    self._fprep_damage    = 0
                    self._fprep_tool      = "chisel"
                    self._fprep_phase     = "prep"
                    return

        elif phase == "prep":
            if self._fprep_chisel_btn and self._fprep_chisel_btn.collidepoint(pos):
                self._fprep_tool = "chisel"
                return
            if self._fprep_brush_btn and self._fprep_brush_btn.collidepoint(pos):
                self._fprep_tool = "brush"
                return

            if not self._fprep_grid_rect or not self._fprep_grid_rect.collidepoint(pos):
                return
            cs  = self._fprep_cell_size
            gap = self._FPREP_GAP
            gx  = self._fprep_grid_rect.x
            gy  = self._fprep_grid_rect.y
            n   = self._fprep_n
            col = (pos[0] - gx) // (cs + gap)
            row = (pos[1] - gy) // (cs + gap)
            if not (0 <= row < n and 0 <= col < n):
                return
            if self._fprep_cleared[row][col]:
                return

            cell = self._fprep_grid[row][col]

            if self._fprep_tool == "chisel":
                self._fprep_damage = min(100, self._fprep_damage + cell["chisel_damage"])
                self._fprep_cleared[row][col] = True
            else:
                self._fprep_cell_hits[row][col] += 1
                if self._fprep_cell_hits[row][col] >= cell["hits_brush"]:
                    self._fprep_cleared[row][col] = True

            if all(self._fprep_cleared[r][c] for r in range(n) for c in range(n)):
                fossil = self._fprep_fossil
                apply_preparation_result(fossil, self._fprep_damage)
                fossil.prepared = True
                player.discovered_fossil_types.add(fossil.fossil_type)
                player.pending_notifications.append(
                    ("Fossil", fossil.fossil_type.replace("_", " ").title(), fossil.rarity))
                self._fprep_phase    = "reveal"
                self._fprep_reveal_t = 0.0

        elif phase == "reveal":
            if self._fprep_done_btn and self._fprep_done_btn.collidepoint(pos):
                self._fprep_reset()

    # ------------------------------------------------------------------
    # Backhoe UI
    # ------------------------------------------------------------------

    def open_backhoe(self, bh):
        self.backhoe_open   = True
        self.active_backhoe = bh

    def close_backhoe(self):
        self.backhoe_open   = False
        self.active_backhoe = None

    def _draw_backhoe_panel(self, player):
        bh = self.active_backhoe
        PW, PH = 380, 340
        px = (SCREEN_W - PW) // 2
        py = (SCREEN_H - PH) // 2

        panel = pygame.Surface((PW, PH), pygame.SRCALPHA)
        panel.fill((20, 18, 12, 235))
        self.screen.blit(panel, (px, py))
        pygame.draw.rect(self.screen, (120, 90, 30), (px, py, PW, PH), 2)

        title = self.font.render("BACKHOE", True, (230, 190, 60))
        self.screen.blit(title, (px + 14, py + 10))
        hint = self.small.render("[E] close", True, (140, 110, 50))
        self.screen.blit(hint, (px + PW - hint.get_width() - 10, py + 13))

        pygame.draw.line(self.screen, (90, 70, 20), (px + 10, py + 42), (px + PW - 10, py + 42))

        bar_w = PW - 28
        fuel_label = self.small.render(
            f"OIL FUEL  {bh.fuel:.1f} / {bh.FUEL_TANK:.0f}", True, (210, 160, 40)
        )
        self.screen.blit(fuel_label, (px + 14, py + 52))
        pygame.draw.rect(self.screen, (30, 25, 10), (px + 14, py + 68, bar_w, 12))
        frac = bh.fuel / bh.FUEL_TANK if bh.FUEL_TANK > 0 else 0
        if frac > 0:
            pygame.draw.rect(self.screen, (200, 140, 30), (px + 14, py + 68, int(bar_w * frac), 12))
        pygame.draw.rect(self.screen, (90, 70, 20), (px + 14, py + 68, bar_w, 12), 1)

        has_oil = player.inventory.get("oil_barrel", 0) > 0
        b1c  = (50, 40, 10) if has_oil else (30, 28, 20)
        b1bc = (160, 120, 30) if has_oil else (70, 60, 30)
        b1t  = (230, 180, 60) if has_oil else (90, 80, 50)
        BW, BH_ = 100, 24
        b1x = px + 14
        b_y = py + 86
        self._bh_deposit1_btn = pygame.Rect(b1x, b_y, BW, BH_)
        pygame.draw.rect(self.screen, b1c, self._bh_deposit1_btn)
        pygame.draw.rect(self.screen, b1bc, self._bh_deposit1_btn, 1)
        d1t = self.small.render("Deposit 1", True, b1t)
        self.screen.blit(d1t, (b1x + BW // 2 - d1t.get_width() // 2,
                                b_y + BH_ // 2 - d1t.get_height() // 2))
        b2x = b1x + BW + 8
        self._bh_deposit_all_btn = pygame.Rect(b2x, b_y, BW, BH_)
        pygame.draw.rect(self.screen, b1c, self._bh_deposit_all_btn)
        pygame.draw.rect(self.screen, b1bc, self._bh_deposit_all_btn, 1)
        d2t = self.small.render("Deposit All", True, b1t)
        self.screen.blit(d2t, (b2x + BW // 2 - d2t.get_width() // 2,
                                b_y + BH_ // 2 - d2t.get_height() // 2))

        player_oil = player.inventory.get("oil_barrel", 0)
        oil_info = self.small.render(f"  (you have: {player_oil})", True, (140, 110, 40))
        self.screen.blit(oil_info, (b2x + BW + 8, b_y + BH_ // 2 - oil_info.get_height() // 2))

        pygame.draw.line(self.screen, (90, 70, 20), (px + 10, py + 122), (px + PW - 10, py + 122))

        inv_count = bh.inv_count
        inv_label = self.small.render("STORED ITEMS", True, (200, 175, 100))
        self.screen.blit(inv_label, (px + 14, py + 130))
        cnt_lbl = self.small.render(f"{inv_count} / {bh.INV_LIMIT}", True, (160, 140, 80))
        self.screen.blit(cnt_lbl, (px + PW - cnt_lbl.get_width() - 14, py + 130))

        SW, SH_, GAP = 44, 44, 6
        items_per_row = (PW - 28 + GAP) // (SW + GAP)
        ix0, iy0 = px + 14, py + 148
        for idx, (item_id, count) in enumerate(sorted(bh.stored.items())):
            col_i = idx % items_per_row
            row_i = idx // items_per_row
            sx_ = ix0 + col_i * (SW + GAP)
            sy_ = iy0 + row_i * (SH_ + GAP)
            if sy_ + SH_ > py + PH - 70:
                break
            item_color = ITEMS.get(item_id, {}).get("color", (120, 120, 120))
            pygame.draw.rect(self.screen, item_color, (sx_, sy_, SW, SH_))
            pygame.draw.rect(self.screen, (90, 70, 30), (sx_, sy_, SW, SH_), 1)
            c_surf = self.small.render(str(count), True, (255, 255, 255))
            self.screen.blit(c_surf, (sx_ + SW - c_surf.get_width() - 2,
                                       sy_ + SH_ - c_surf.get_height() - 1))
            name_surf = self.small.render(
                ITEMS.get(item_id, {}).get("name", item_id)[:6], True, (220, 220, 220)
            )
            self.screen.blit(name_surf, (sx_ + 2, sy_ + 2))
        if inv_count == 0:
            empty = self.small.render("(empty)", True, (100, 90, 60))
            self.screen.blit(empty, (ix0, iy0 + 6))

        BotBW, BotBH = 110, 28
        take_x = px + 14
        take_y = py + PH - BotBH - 10
        has_items = inv_count > 0
        tc  = (30, 70, 30) if has_items else (25, 30, 25)
        tbc = (60, 160, 60) if has_items else (50, 55, 50)
        ttc = (150, 240, 150) if has_items else (70, 80, 70)
        self._bh_take_btn = pygame.Rect(take_x, take_y, BotBW, BotBH)
        pygame.draw.rect(self.screen, tc, self._bh_take_btn)
        pygame.draw.rect(self.screen, tbc, self._bh_take_btn, 1)
        take_t = self.small.render("TAKE ALL", True, ttc)
        self.screen.blit(take_t, (take_x + BotBW // 2 - take_t.get_width() // 2,
                                   take_y + BotBH // 2 - take_t.get_height() // 2))

        ride_x = take_x + BotBW + 8
        ride_c  = (30, 50, 90)
        ride_bc = (70, 120, 200)
        ride_tc = (150, 200, 255)
        self._bh_ride_btn = pygame.Rect(ride_x, take_y, BotBW, BotBH)
        pygame.draw.rect(self.screen, ride_c, self._bh_ride_btn)
        pygame.draw.rect(self.screen, ride_bc, self._bh_ride_btn, 1)
        ride_t = self.small.render("RIDE  [SPC]", True, ride_tc)
        self.screen.blit(ride_t, (ride_x + BotBW // 2 - ride_t.get_width() // 2,
                                   take_y + BotBH // 2 - ride_t.get_height() // 2))

        pickup_x = ride_x + BotBW + 8
        self._bh_pickup_btn = pygame.Rect(pickup_x, take_y, BotBW, BotBH)
        pygame.draw.rect(self.screen, (60, 30, 10), self._bh_pickup_btn)
        pygame.draw.rect(self.screen, (160, 80, 30), self._bh_pickup_btn, 1)
        pickup_t = self.small.render("PICK UP", True, (230, 160, 80))
        self.screen.blit(pickup_t, (pickup_x + BotBW // 2 - pickup_t.get_width() // 2,
                                    take_y + BotBH // 2 - pickup_t.get_height() // 2))

    def handle_backhoe_click(self, pos, player):
        bh = self.active_backhoe
        if bh is None:
            return False
        if self._bh_deposit1_btn and self._bh_deposit1_btn.collidepoint(pos):
            bh.deposit_fuel(player, amount=1)
            return True
        if self._bh_deposit_all_btn and self._bh_deposit_all_btn.collidepoint(pos):
            bh.deposit_fuel(player)
            return True
        if self._bh_take_btn and self._bh_take_btn.collidepoint(pos):
            bh.take_all(player)
            return True
        if self._bh_ride_btn and self._bh_ride_btn.collidepoint(pos):
            return "ride"
        if self._bh_pickup_btn and self._bh_pickup_btn.collidepoint(pos):
            return "pickup"
        return False

    # ------------------------------------------------------------------
    # Fishing overlay (drawn on top of the game world, no UI panel)
    # ------------------------------------------------------------------

    def draw_fishing_overlay(self, player, dt):
        import math
        state = player.fishing_state
        if state is None:
            return

        W, H = SCREEN_W, SCREEN_H
        cx = W // 2

        if state == "casting":
            tick = pygame.time.get_ticks()
            dots = "." * (1 + (tick // 500) % 3)
            msg = f"Fishing{dots}"
            s = self.font.render(msg, True, (160, 210, 255))
            bw = s.get_width() + 24
            bh = s.get_height() + 10
            bx2 = cx - bw // 2
            by2 = H - 110
            box = pygame.Surface((bw + 4, bh + 4), pygame.SRCALPHA)
            box.fill((12, 28, 48, 200))
            self.screen.blit(box, (bx2 - 2, by2 - 2))
            pygame.draw.rect(self.screen, (60, 120, 200), (bx2 - 2, by2 - 2, bw + 4, bh + 4), 1)
            self.screen.blit(s, (bx2 + 12, by2 + 5))

        elif state == "biting":
            frac = max(0.0, player._fishing_timer / 2.0)
            pulse = (math.sin(pygame.time.get_ticks() * 0.012) + 1) * 0.5
            r = int(235 + 20 * pulse)
            g = int(60 + 80 * pulse)
            glow_col = (r, g, 20)

            bite_s = self._fish_bite_font.render("! BITE !", True, glow_col)
            sub_s = self.small.render("Press  F  to reel in!", True, (230, 230, 230))

            bar_w = 220
            bar_h = 11
            pad = 10
            box_w = max(bite_s.get_width(), sub_s.get_width(), bar_w) + pad * 2
            box_h = bite_s.get_height() + sub_s.get_height() + bar_h + pad * 3 + 4
            bx2 = cx - box_w // 2
            by2 = H - 140 - box_h

            box = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
            box.fill((32, 18, 8, 215))
            self.screen.blit(box, (bx2, by2))
            pygame.draw.rect(self.screen, glow_col, (bx2, by2, box_w, box_h), 2)

            self.screen.blit(bite_s, (cx - bite_s.get_width() // 2, by2 + pad))
            self.screen.blit(sub_s, (cx - sub_s.get_width() // 2,
                                     by2 + pad + bite_s.get_height() + 4))

            bar_y = by2 + box_h - bar_h - pad
            bar_x = cx - bar_w // 2
            pygame.draw.rect(self.screen, (50, 38, 18), (bar_x, bar_y, bar_w, bar_h))
            fill = max(0, int(bar_w * frac))
            bar_col = (int(80 + 175 * frac), int(200 * frac), 20)
            if fill > 0:
                pygame.draw.rect(self.screen, bar_col, (bar_x, bar_y, fill, bar_h))
            pygame.draw.rect(self.screen, (110, 90, 40), (bar_x, bar_y, bar_w, bar_h), 1)

        elif state == "result":
            if player._fishing_result == "caught" and player.fish_caught:
                last = player.fish_caught[-1]
                species_name = FISH_TYPES.get(last.species, {}).get("name", last.species.replace("_", " ").title())
                msg = f"Caught a {species_name}!  ({last.weight_kg:.2f} kg)"
                col = FISH_RARITY_COLORS.get(last.rarity, (180, 220, 180))
            else:
                msg = "The fish got away..."
                col = (180, 145, 100)

            s = self.font.render(msg, True, col)
            bw = s.get_width() + 24
            bh = s.get_height() + 10
            bx2 = cx - bw // 2
            by2 = H - 110
            box = pygame.Surface((bw + 4, bh + 4), pygame.SRCALPHA)
            box.fill((12, 22, 14, 205))
            self.screen.blit(box, (bx2 - 2, by2 - 2))
            pygame.draw.rect(self.screen, col, (bx2 - 2, by2 - 2, bw + 4, bh + 4), 1)
            self.screen.blit(s, (bx2 + 12, by2 + 5))
