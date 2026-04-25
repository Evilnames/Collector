import pygame
import copy
from constants import SCREEN_W, SCREEN_H
from sculpture import SCULPTABLE_MINERALS, TEMPLATES, BASE_TEMPLATES, MINERAL_COLORS

_ACCENT   = (200, 190, 160)
_DIM      = (120, 110, 90)
_BTN_BG   = (55, 45, 30)
_BTN_HL   = (80, 65, 40)
_CARVED   = (18, 14, 10)
_HOVER_CARVE   = (90, 30, 20)   # hover tint when left-btn held
_HOVER_RESTORE = (30, 70, 30)   # hover tint when right-btn held
_HOVER_IDLE    = (100, 95, 75)  # hover tint when no button held


def _bevel(surface, color, rect, carved=False):
    """Draw a single grid cell with a stone-chip bevel effect."""
    if carved:
        pygame.draw.rect(surface, _CARVED, rect)
        # Subtle inner recess lines
        shade = (28, 22, 16)
        pygame.draw.line(surface, shade, rect.topleft, (rect.right - 1, rect.top))
        pygame.draw.line(surface, shade, rect.topleft, (rect.left, rect.bottom - 1))
        return
    pygame.draw.rect(surface, color, rect)
    hi  = tuple(min(255, c + 55) for c in color)
    sha = tuple(max(0,   c - 55) for c in color)
    # Top + left highlight
    pygame.draw.line(surface, hi, rect.topleft, (rect.right - 2, rect.top))
    pygame.draw.line(surface, hi, rect.topleft, (rect.left, rect.bottom - 2))
    # Bottom + right shadow
    pygame.draw.line(surface, sha, (rect.left + 1, rect.bottom - 1), (rect.right - 1, rect.bottom - 1))
    pygame.draw.line(surface, sha, (rect.right - 1, rect.top + 1),   (rect.right - 1, rect.bottom - 1))


class SculptureMixin:

    # ── Phase routing ────────────────────────────────────────────────────────

    def _draw_sculptor_bench(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("SCULPTOR'S BENCH", True, _ACCENT)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 4))
        hint = self.small.render("ESC back  ·  ENTER confirm", True, _DIM)
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        if self._sculpt_phase == "idle":
            self._sculpt_phase = "select_minerals"

        self._draw_sculpt_breadcrumb()

        if self._sculpt_phase == "select_minerals":
            self._draw_sculpt_select_minerals(player)
        elif self._sculpt_phase == "select_template":
            self._draw_sculpt_select_template(player)
        elif self._sculpt_phase == "carve":
            self._draw_sculpt_carve(player)
        elif self._sculpt_phase == "confirm":
            self._draw_sculpt_confirm(player)

    def _draw_sculpt_breadcrumb(self):
        steps = [
            ("select_minerals", "1 · Mineral"),
            ("select_template", "2 · Design"),
            ("carve",           "3 · Carve"),
            ("confirm",         "4 · Done"),
        ]
        phase_order = [s[0] for s in steps]
        current_idx = phase_order.index(self._sculpt_phase) if self._sculpt_phase in phase_order else 0

        SW, SH, GAP = 110, 20, 6
        total_w = len(steps) * SW + (len(steps) - 1) * GAP
        bx = SCREEN_W // 2 - total_w // 2
        by = 22
        for i, (phase, label) in enumerate(steps):
            rx = bx + i * (SW + GAP)
            done    = i < current_idx
            current = i == current_idx
            if current:
                bg = (65, 55, 35);  brd = _ACCENT;  tc = _ACCENT
            elif done:
                bg = (35, 45, 25);  brd = (80, 140, 60);  tc = (100, 170, 80)
            else:
                bg = (28, 24, 18);  brd = (55, 48, 35);   tc = _DIM
            pygame.draw.rect(self.screen, bg,  (rx, by, SW, SH))
            pygame.draw.rect(self.screen, brd, (rx, by, SW, SH), 1)
            ls = self.small.render(label, True, tc)
            self.screen.blit(ls, (rx + SW // 2 - ls.get_width() // 2, by + SH // 2 - ls.get_height() // 2))

    # ── Phase 1: Mineral Selection ───────────────────────────────────────────

    def _draw_sculpt_select_minerals(self, player):
        self._sculpt_mineral_rects.clear()
        has_chisel = player.inventory.get("chisel", 0) > 0
        if not has_chisel:
            msg = self.font.render("You need a Stone Chisel to sculpt.", True, (220, 80, 60))
            self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2 - 20))
            sub = self.small.render("Craft one at a workbench: 2 stone chips + 1 lumber", True, _DIM)
            self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, SCREEN_H // 2 + 10))
            return

        available = {mid: player.inventory.get(mid, 0)
                     for mid in SCULPTABLE_MINERALS if player.inventory.get(mid, 0) > 0}
        if not available:
            msg = self.font.render("No sculptable minerals in inventory.", True, (200, 140, 60))
            self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2 - 20))
            sub2 = self.small.render("Mine Limestone, Granite, Marble, Basalt, or Magmatic Stone.", True, _DIM)
            self.screen.blit(sub2, (SCREEN_W // 2 - sub2.get_width() // 2, SCREEN_H // 2 + 10))
            return

        sub = self.small.render("Choose mineral type and height (1–4 blocks tall):", True, _ACCENT)
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 48))

        CARD_W, CARD_H, GAP = 210, 130, 14
        total_w = len(available) * CARD_W + (len(available) - 1) * GAP
        gx0 = (SCREEN_W - total_w) // 2
        gy0 = 65

        for mi, (mid, count) in enumerate(available.items()):
            cx  = gx0 + mi * (CARD_W + GAP)
            col = MINERAL_COLORS.get(mid, (180, 170, 155))
            sel = (self._sculpt_mineral == mid)
            bg  = _BTN_HL if sel else _BTN_BG
            brd = col if sel else _DIM

            pygame.draw.rect(self.screen, bg,  (cx, gy0, CARD_W, CARD_H))
            pygame.draw.rect(self.screen, brd, (cx, gy0, CARD_W, CARD_H), 2 if sel else 1)

            # Stone chip swatch with bevel
            swatch_r = pygame.Rect(cx + 10, gy0 + 10, 28, 28)
            _bevel(self.screen, col, swatch_r)

            name_lbl  = self.font.render(SCULPTABLE_MINERALS[mid], True, col)
            count_lbl = self.small.render(f"×{count} available", True, _DIM)
            self.screen.blit(name_lbl,  (cx + 46, gy0 + 12))
            self.screen.blit(count_lbl, (cx + 46, gy0 + 32))

            self._sculpt_mineral_rects[mid] = pygame.Rect(cx, gy0, CARD_W, CARD_H)

            # Height buttons (only when selected)
            if sel:
                btn_label = self.small.render("Height:", True, _DIM)
                self.screen.blit(btn_label, (cx + 10, gy0 + CARD_H - 56))
                for h in range(1, 5):
                    bx2 = cx + 10 + (h - 1) * 48
                    by2 = gy0 + CARD_H - 40
                    ok  = count >= h
                    cur = (self._sculpt_count == h)
                    btn_col = col if cur else (_BTN_HL if ok else (30, 25, 18))
                    brd2    = brd if cur else (_DIM if ok else (40, 35, 25))
                    r2 = pygame.Rect(bx2, by2, 40, 30)
                    pygame.draw.rect(self.screen, btn_col, r2)
                    pygame.draw.rect(self.screen, brd2, r2, 2 if cur else 1)
                    hl = self.small.render(str(h), True, (255, 255, 255) if ok else (60, 52, 40))
                    self.screen.blit(hl, (bx2 + 20 - hl.get_width() // 2, by2 + 7))
                    self._sculpt_mineral_rects[f"{mid}_h{h}"] = r2

        # Height preview: show how tall the sculpture will be as stacked blocks
        if self._sculpt_mineral and self._sculpt_count > 0:
            mineral_count = player.inventory.get(self._sculpt_mineral, 0)
            can_proceed   = mineral_count >= self._sculpt_count
            col2 = MINERAL_COLORS.get(self._sculpt_mineral, _ACCENT)
            prev_x = SCREEN_W // 2 + max(len(available), 1) * (CARD_W + GAP) // 2 + 20
            prev_x = min(prev_x, SCREEN_W - 60)
            for k in range(self._sculpt_count):
                bk_r = pygame.Rect(prev_x, gy0 + (self._sculpt_count - 1 - k) * 34, 32, 30)
                _bevel(self.screen, col2, bk_r)
            h_lbl = self.small.render(f"{self._sculpt_count} block{'s' if self._sculpt_count > 1 else ''}", True, _DIM)
            self.screen.blit(h_lbl, (prev_x + 16 - h_lbl.get_width() // 2,
                                     gy0 + self._sculpt_count * 34 + 4))

            btn_y    = gy0 + CARD_H + 24
            btn_rect = pygame.Rect(SCREEN_W // 2 - 95, btn_y, 190, 36)
            bg3  = (50, 70, 38) if can_proceed else (35, 28, 18)
            brd3 = (100, 180, 70) if can_proceed else (60, 50, 35)
            tc3  = (150, 230, 110) if can_proceed else _DIM
            pygame.draw.rect(self.screen, bg3,  btn_rect)
            pygame.draw.rect(self.screen, brd3, btn_rect, 2)
            lbl3 = self.font.render("Choose Design  →", True, tc3)
            self.screen.blit(lbl3, (btn_rect.centerx - lbl3.get_width() // 2, btn_rect.y + 8))
            self._sculpt_mineral_rects["_confirm"] = btn_rect

    # ── Phase 2: Template Selection ──────────────────────────────────────────

    def _draw_sculpt_select_template(self, player):
        self._sculpt_template_rects.clear()
        sub = self.small.render("Pick a template to start from — or carve from scratch:", True, _ACCENT)
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 48))

        researched = set(getattr(self, '_researched_nodes', set()))
        if hasattr(self, '_research') and self._research:
            researched = {nid for nid, node in self._research.nodes.items() if node.unlocked}
        master_unlocked = "master_sculptor" in researched
        available_templates = list(BASE_TEMPLATES)
        if master_unlocked:
            available_templates.append("Effigy")

        CARD_W, CARD_H, GAP = 98, 90, 7
        COLS = 7
        all_opts  = ["Custom"] + available_templates
        total_rows = (len(all_opts) + COLS - 1) // COLS
        total_w    = min(len(all_opts), COLS) * CARD_W + (min(len(all_opts), COLS) - 1) * GAP
        gx0 = max(8, (SCREEN_W - total_w) // 2)
        gy0 = 54
        col = MINERAL_COLORS.get(self._sculpt_mineral, (180, 170, 155))

        for oi, opt in enumerate(all_opts):
            ci2 = oi % COLS
            ri2 = oi // COLS
            cx  = gx0 + ci2 * (CARD_W + GAP)
            cy  = gy0 + ri2 * (CARD_H + GAP)
            sel = (opt == "Custom" and self._sculpt_template is None) or \
                  (opt != "Custom" and self._sculpt_template == opt)
            bg  = _BTN_HL if sel else _BTN_BG
            brd = col if sel else _DIM

            pygame.draw.rect(self.screen, bg,  (cx, cy, CARD_W, CARD_H))
            pygame.draw.rect(self.screen, brd, (cx, cy, CARD_W, CARD_H), 2 if sel else 1)

            if opt == "Custom":
                lbl = self.small.render("Custom", True, _ACCENT)
                self.screen.blit(lbl, (cx + CARD_W // 2 - lbl.get_width() // 2, cy + 5))
                sub2 = self.small.render("blank", True, _DIM)
                self.screen.blit(sub2, (cx + CARD_W // 2 - sub2.get_width() // 2, cy + 18))
                preview_rect = pygame.Rect(cx + 6, cy + 32, CARD_W - 12, CARD_H - 38)
                pygame.draw.rect(self.screen, _CARVED, preview_rect)
                for r in range(4):
                    for c2 in range(8):
                        pygame.draw.rect(self.screen, (35, 30, 22),
                                         (preview_rect.x + c2 * (preview_rect.w // 8) + 1,
                                          preview_rect.y + r * (preview_rect.h // 4) + 1,
                                          max(1, preview_rect.w // 8 - 2),
                                          max(1, preview_rect.h // 4 - 2)))
            else:
                lbl = self.small.render(opt, True, _ACCENT)
                self.screen.blit(lbl, (cx + CARD_W // 2 - lbl.get_width() // 2, cy + 4))
                if opt in TEMPLATES:
                    grid = TEMPLATES[opt](self._sculpt_count)
                    self._draw_mini_grid_preview(self.screen, grid, self._sculpt_count,
                                                 cx + 5, cy + 18, CARD_W - 10, CARD_H - 24, col)

            self._sculpt_template_rects[opt] = pygame.Rect(cx, cy, CARD_W, CARD_H)

        info_y = gy0 + total_rows * (CARD_H + GAP) + 8
        mc  = MINERAL_COLORS.get(self._sculpt_mineral, _ACCENT)
        mn  = SCULPTABLE_MINERALS.get(self._sculpt_mineral, "?")
        tag = self.small.render(
            f"  {mn}  ×{self._sculpt_count}   ·   {self._sculpt_count} block{'s' if self._sculpt_count > 1 else ''} tall",
            True, mc)
        pygame.draw.rect(self.screen, _BTN_BG, (SCREEN_W // 2 - tag.get_width() // 2 - 8,
                                                 info_y - 2, tag.get_width() + 16, tag.get_height() + 4))
        self.screen.blit(tag, (SCREEN_W // 2 - tag.get_width() // 2, info_y))

    def _draw_mini_grid_preview(self, surf, grid, height, x, y, w, h, color):
        rows = height * 4
        if grid is None:
            pygame.draw.rect(surf, _CARVED, (x, y, w, h))
            return
        cw = max(1, w // 8)
        ch = max(1, h // max(1, rows))
        hi = tuple(min(255, c + 22) for c in color)
        lo = tuple(max(0,   c - 28) for c in color)
        for ri, row in enumerate(grid):
            for ci, filled in enumerate(row):
                px = x + ci * cw
                py = y + ri * ch
                cell_c = (hi if ci % 2 == 0 else lo) if filled else _CARVED
                pygame.draw.rect(surf, cell_c, (px, py, cw, ch))

    # ── Phase 3: Carving ─────────────────────────────────────────────────────

    def _draw_sculpt_carve(self, player):
        self._sculpt_cell_rects.clear()
        col  = MINERAL_COLORS.get(self._sculpt_mineral, (180, 170, 155))
        rows = len(self._sculpt_grid)
        COLS = 8

        # Cell sizing: leave space for panel on right and breadcrumb above
        available_h = SCREEN_H - 100
        CELL_SIZE   = min(40, available_h // max(1, rows))
        CELL_SIZE   = max(10, CELL_SIZE)
        grid_w = COLS * CELL_SIZE
        grid_h = rows * CELL_SIZE

        # Panel width
        PANEL_W = 220
        PANEL_X = SCREEN_W - PANEL_W - 12
        gx = (PANEL_X - grid_w) // 2
        gx = max(12, gx)
        gy = 50

        hi_col  = tuple(min(255, c + 30) for c in col)
        lo_col  = tuple(max(0,   c - 40) for c in col)

        # ── Draw grid cells ──
        for ri, row in enumerate(self._sculpt_grid):
            for ci, filled in enumerate(row):
                px = gx + ci * CELL_SIZE
                py = gy + ri * CELL_SIZE
                cr = pygame.Rect(px, py, CELL_SIZE, CELL_SIZE)

                # Hover highlight
                hover = (self._sculpt_hover_cell == (ri, ci))
                if hover:
                    mode = self._sculpt_drag_mode
                    if mode == "carve":
                        tint = _HOVER_CARVE
                    elif mode == "restore":
                        tint = _HOVER_RESTORE
                    else:
                        tint = _HOVER_IDLE
                    pygame.draw.rect(self.screen, tint, cr)
                else:
                    cell_col = (hi_col if ci % 2 == 0 else lo_col) if filled else _CARVED
                    _bevel(self.screen, cell_col, cr, carved=not filled)

                # Symmetry mirror indicator: highlight the mirror cell faintly
                if self._sculpt_symmetry and CELL_SIZE >= 14:
                    mirror_ci = 7 - ci
                    if hover and ci != mirror_ci:
                        mr = pygame.Rect(gx + mirror_ci * CELL_SIZE, py, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(self.screen, (tint[0] // 2, tint[1] // 2, tint[2] // 2), mr)

                self._sculpt_cell_rects[(ri, ci)] = cr

        # ── Block dividers ──
        rows_per_block = 4
        for k in range(1, self._sculpt_count):
            div_y = gy + k * rows_per_block * CELL_SIZE
            pygame.draw.line(self.screen, col, (gx, div_y), (gx + grid_w, div_y), 2)
            lbl = self.small.render(f"Piece {k + 1}", True, col)
            self.screen.blit(lbl, (gx - lbl.get_width() - 6, div_y + 2))

        # Label for piece 1 (top)
        if self._sculpt_count > 1:
            lbl0 = self.small.render("Piece 1", True, col)
            self.screen.blit(lbl0, (gx - lbl0.get_width() - 6, gy + 2))

        # Outer border
        pygame.draw.rect(self.screen, col, (gx - 2, gy - 2, grid_w + 4, grid_h + 4), 2)

        # ── Side panel ──
        py2 = gy

        # Tool mode indicator
        mode_text  = "CARVE (left-drag)" if self._sculpt_drag_mode != "restore" else "RESTORE (right-drag)"
        mode_color = (220, 80, 60) if self._sculpt_drag_mode != "restore" else (80, 200, 80)
        if self._sculpt_drag_mode is None:
            mode_text, mode_color = "No drag", _DIM
        tool_s = self.small.render(mode_text, True, mode_color)
        self.screen.blit(tool_s, (PANEL_X, py2))
        py2 += 18

        # Instructions
        controls = [
            ("Left-drag",   "carve stone"),
            ("Right-drag",  "restore stone"),
            ("Z",           "undo stroke"),
            ("ENTER",       "preview"),
        ]
        for key_s, desc_s in controls:
            ks = self.small.render(key_s, True, _ACCENT)
            ds = self.small.render(desc_s, True, _DIM)
            self.screen.blit(ks, (PANEL_X, py2))
            self.screen.blit(ds, (PANEL_X + ks.get_width() + 6, py2))
            py2 += 15
        py2 += 8

        # Info bar
        mn  = SCULPTABLE_MINERALS.get(self._sculpt_mineral, "")
        for line in [f"Mineral: {mn}", f"Height: {self._sculpt_count}blk",
                     f"Template: {self._sculpt_template or 'Custom'}"]:
            s = self.small.render(line, True, _DIM)
            self.screen.blit(s, (PANEL_X, py2))
            py2 += 14
        py2 += 8

        # Symmetry toggle
        sym_r = pygame.Rect(PANEL_X, py2, PANEL_W - 4, 28)
        sym_bg  = (30, 50, 30) if self._sculpt_symmetry else _BTN_BG
        sym_brd = (80, 180, 80) if self._sculpt_symmetry else _DIM
        sym_tc  = (130, 230, 100) if self._sculpt_symmetry else _ACCENT
        pygame.draw.rect(self.screen, sym_bg,  sym_r)
        pygame.draw.rect(self.screen, sym_brd, sym_r, 2)
        sym_lbl = self.small.render(
            ("✦ Mirror  ON" if self._sculpt_symmetry else "  Mirror  OFF"), True, sym_tc)
        self.screen.blit(sym_lbl, (sym_r.centerx - sym_lbl.get_width() // 2,
                                   sym_r.y + 6))
        self._sculpt_cell_rects["_symmetry"] = sym_r
        py2 += 36

        # Fill / Clear
        half_w = (PANEL_W - 4) // 2 - 4
        fill_r  = pygame.Rect(PANEL_X,              py2, half_w, 26)
        clear_r = pygame.Rect(PANEL_X + half_w + 8, py2, half_w, 26)
        for r, label in ((fill_r, "Fill All"), (clear_r, "Clear All")):
            pygame.draw.rect(self.screen, _BTN_BG, r)
            pygame.draw.rect(self.screen, _DIM, r, 1)
            ls = self.small.render(label, True, _ACCENT)
            self.screen.blit(ls, (r.centerx - ls.get_width() // 2, r.y + 5))
        self._sculpt_cell_rects["_fill"]  = fill_r
        self._sculpt_cell_rects["_clear"] = clear_r
        py2 += 34

        # Undo count
        if self._sculpt_undo_stack:
            us = self.small.render(f"  undo: {len(self._sculpt_undo_stack)} step{'s' if len(self._sculpt_undo_stack) > 1 else ''}", True, _DIM)
            self.screen.blit(us, (PANEL_X, py2))
        py2 += 20

        # Mini world-preview
        py2 += 6
        prev_label = self.small.render("Preview:", True, _DIM)
        self.screen.blit(prev_label, (PANEL_X, py2))
        py2 += 14
        self._draw_sculpt_world_preview(PANEL_X, py2, PANEL_W - 4, col)
        py2 += self._sculpt_count * 32 + 8

        # Confirm button
        confirm_r = pygame.Rect(PANEL_X, py2, PANEL_W - 4, 34)
        pygame.draw.rect(self.screen, (42, 62, 32), confirm_r)
        pygame.draw.rect(self.screen, (80, 160, 60), confirm_r, 2)
        cl2 = self.font.render("Preview  →", True, (130, 220, 100))
        self.screen.blit(cl2, (confirm_r.centerx - cl2.get_width() // 2, confirm_r.y + 7))
        self._sculpt_cell_rects["_confirm"] = confirm_r

    def _draw_sculpt_world_preview(self, px, py, w, mineral_color):
        """Small pixel-accurate preview of the final in-world appearance."""
        CELL_W = 4   # matches renderer._draw_sculpture_at: 8 cols × 4px
        CELL_H = 4
        grid_px_w = 8 * CELL_W   # = 32
        grid_px_h = len(self._sculpt_grid) * CELL_H
        # Draw background
        pygame.draw.rect(self.screen, (12, 10, 8), (px, py, grid_px_w + 4, grid_px_h + 4))
        hi  = tuple(min(255, c + 25) for c in mineral_color)
        lo  = tuple(max(0,   c - 35) for c in mineral_color)
        rows_total = len(self._sculpt_grid)
        for row_idx in range(rows_total - 1, -1, -1):
            row              = self._sculpt_grid[row_idx]
            rows_from_bottom = rows_total - 1 - row_idx
            local_row        = rows_from_bottom % 4
            block_offset     = rows_from_bottom // 4
            world_py = py + 2 + block_offset * 16 + local_row * CELL_H
            for ci, filled in enumerate(row):
                if filled:
                    c = hi if ci % 2 == 0 else lo
                    pygame.draw.rect(self.screen, c,
                                     (px + 2 + ci * CELL_W, world_py, CELL_W, CELL_H))

        # Block separator lines
        for k in range(1, self._sculpt_count):
            line_y = py + 2 + k * 16
            pygame.draw.line(self.screen, (50, 45, 35), (px + 2, line_y), (px + 2 + 32, line_y))
        # Border
        pygame.draw.rect(self.screen, mineral_color, (px, py, grid_px_w + 4, grid_px_h + 4), 1)

    # ── Phase 4: Confirm ─────────────────────────────────────────────────────

    def _draw_sculpt_confirm(self, player):
        col  = MINERAL_COLORS.get(self._sculpt_mineral, (180, 170, 155))
        rows = len(self._sculpt_grid)

        sub = self.font.render("Confirm your sculpture?", True, _ACCENT)
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 48))

        CELL_SIZE = min(44, max(8, (SCREEN_H - 180) // max(1, rows)))
        grid_w = 8 * CELL_SIZE
        grid_h = rows * CELL_SIZE
        gx = SCREEN_W // 2 - grid_w // 2
        gy = 70

        hi = tuple(min(255, c + 30) for c in col)
        lo = tuple(max(0,   c - 40) for c in col)
        for ri, row in enumerate(self._sculpt_grid):
            for ci, filled in enumerate(row):
                r = pygame.Rect(gx + ci * CELL_SIZE, gy + ri * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                cell_col = (hi if ci % 2 == 0 else lo) if filled else _CARVED
                _bevel(self.screen, cell_col, r, carved=not filled)

        # Block dividers
        for k in range(1, self._sculpt_count):
            div_y = gy + k * 4 * CELL_SIZE
            pygame.draw.line(self.screen, col, (gx, div_y), (gx + grid_w, div_y), 2)

        pygame.draw.rect(self.screen, col, (gx - 2, gy - 2, grid_w + 4, grid_h + 4), 2)

        # Stats
        total_cells = rows * 8
        filled_cells = sum(cell for row in self._sculpt_grid for cell in row)
        coverage_pct = int(100 * filled_cells / max(1, total_cells))
        mn = SCULPTABLE_MINERALS.get(self._sculpt_mineral, "?")
        info = self.small.render(
            f"{mn}  ·  {self._sculpt_count} block{'s' if self._sculpt_count > 1 else ''} tall  ·  "
            f"{coverage_pct}% solid  ·  template: {self._sculpt_template or 'custom'}",
            True, _DIM)
        self.screen.blit(info, (SCREEN_W // 2 - info.get_width() // 2, gy + grid_h + 10))

        btn_y = gy + grid_h + 32
        accept_r = pygame.Rect(SCREEN_W // 2 - 104, btn_y, 96, 34)
        back_r   = pygame.Rect(SCREEN_W // 2 + 8,   btn_y, 96, 34)
        pygame.draw.rect(self.screen, (35, 56, 28), accept_r)
        pygame.draw.rect(self.screen, (75, 160, 55), accept_r, 2)
        pygame.draw.rect(self.screen, _BTN_BG, back_r)
        pygame.draw.rect(self.screen, _DIM, back_r, 2)
        al = self.font.render("Create!", True, (115, 215, 85))
        bl = self.font.render("← Edit",  True, _ACCENT)
        self.screen.blit(al, (accept_r.centerx - al.get_width() // 2, accept_r.y + 7))
        self.screen.blit(bl, (back_r.centerx   - bl.get_width() // 2, back_r.y   + 7))
        self._sculpt_cell_rects["_accept"] = accept_r
        self._sculpt_cell_rects["_back"]   = back_r

    # ── Click handlers ───────────────────────────────────────────────────────

    def _handle_sculptor_bench_click(self, pos, player, right=False):
        if self._sculpt_phase == "select_minerals":
            self._handle_sculpt_mineral_click(pos, player)
        elif self._sculpt_phase == "select_template":
            self._handle_sculpt_template_click(pos, player)
        elif self._sculpt_phase == "carve":
            self._handle_sculpt_carve_click(pos, player, right)
        elif self._sculpt_phase == "confirm":
            self._handle_sculpt_confirm_click(pos, player)

    def _handle_sculpt_mineral_click(self, pos, player):
        for key, rect in self._sculpt_mineral_rects.items():
            if not rect.collidepoint(pos):
                continue
            if key == "_confirm":
                if self._sculpt_mineral and self._sculpt_count > 0:
                    if player.inventory.get(self._sculpt_mineral, 0) >= self._sculpt_count:
                        self._sculpt_phase = "select_template"
            elif "_h" in str(key):
                parts = key.rsplit("_h", 1)
                if len(parts) == 2:
                    h   = int(parts[1])
                    mid = parts[0]
                    if player.inventory.get(mid, 0) >= h:
                        self._sculpt_count = h
            else:
                self._sculpt_mineral = key
                if self._sculpt_count == 0:
                    self._sculpt_count = 1
            return

    def _handle_sculpt_template_click(self, pos, player):
        for opt, rect in self._sculpt_template_rects.items():
            if rect.collidepoint(pos):
                self._sculpt_template = None if opt == "Custom" else opt
                rows = self._sculpt_count * 4
                if opt == "Custom":
                    self._sculpt_grid = [[True] * 8 for _ in range(rows)]
                elif opt in TEMPLATES:
                    self._sculpt_grid = TEMPLATES[opt](self._sculpt_count)
                else:
                    self._sculpt_grid = [[True] * 8 for _ in range(rows)]
                self._sculpt_undo_stack = []
                self._sculpt_drag_mode  = None
                self._sculpt_phase = "carve"
                return

    def _handle_sculpt_carve_click(self, pos, player, right=False):
        """Handles button clicks in the carve phase.  Grid painting is handled
        by the per-frame drag system (_sculpt_update_drag)."""
        sr = self._sculpt_cell_rects.get("_symmetry")
        if sr and sr.collidepoint(pos):
            self._sculpt_symmetry = not self._sculpt_symmetry
            return
        fr = self._sculpt_cell_rects.get("_fill")
        if fr and fr.collidepoint(pos):
            self._push_undo()
            self._sculpt_grid = [[True] * 8 for _ in range(len(self._sculpt_grid))]
            return
        cr = self._sculpt_cell_rects.get("_clear")
        if cr and cr.collidepoint(pos):
            self._push_undo()
            self._sculpt_grid = [[False] * 8 for _ in range(len(self._sculpt_grid))]
            return
        confirm_r = self._sculpt_cell_rects.get("_confirm")
        if confirm_r and confirm_r.collidepoint(pos):
            self._sculpt_phase = "confirm"
            return
        # Grid cells: start drag (push undo once, paint first cell)
        for (ri, ci), rect in self._sculpt_cell_rects.items():
            if not isinstance(ri, int):
                continue
            if rect.collidepoint(pos):
                self._push_undo()
                new_val = right   # True = restore, False = carve
                self._sculpt_grid[ri][ci] = new_val
                if self._sculpt_symmetry:
                    self._sculpt_grid[ri][7 - ci] = new_val
                self._sculpt_drag_mode = "restore" if right else "carve"
                return

    def _handle_sculpt_confirm_click(self, pos, player):
        accept_r = self._sculpt_cell_rects.get("_accept")
        if accept_r and accept_r.collidepoint(pos):
            self._complete_sculpture(player)
            return
        back_r = self._sculpt_cell_rects.get("_back")
        if back_r and back_r.collidepoint(pos):
            self._sculpt_phase = "carve"

    # ── Per-frame drag update (called from main.py every frame) ─────────────

    def _sculpt_update_drag(self, pos, mouse_btns):
        """Called every frame to handle click-drag painting and hover tracking."""
        if self._sculpt_phase != "carve":
            self._sculpt_drag_mode  = None
            self._sculpt_hover_cell = None
            return

        left_held  = mouse_btns[0]
        right_held = mouse_btns[2]

        # Hover tracking (even when not dragging)
        hover_hit = None
        for (ri, ci), rect in self._sculpt_cell_rects.items():
            if not isinstance(ri, int):
                continue
            if rect.collidepoint(pos):
                hover_hit = (ri, ci)
                break
        self._sculpt_hover_cell = hover_hit

        # Drag painting
        if left_held or right_held:
            if self._sculpt_drag_mode is None:
                return   # drag started from a non-grid area; wait for next press
            if hover_hit is not None:
                ri, ci = hover_hit
                new_val = (self._sculpt_drag_mode == "restore")
                if self._sculpt_grid[ri][ci] != new_val:
                    self._sculpt_grid[ri][ci] = new_val
                    if self._sculpt_symmetry:
                        self._sculpt_grid[ri][7 - ci] = new_val
        else:
            self._sculpt_drag_mode = None

    # ── Keyboard ─────────────────────────────────────────────────────────────

    def handle_sculptor_keydown(self, key, player):
        if key == pygame.K_ESCAPE:
            if self._sculpt_phase in ("select_minerals", "idle"):
                self._sculpt_phase = "idle"
                self.refinery_open = False
            elif self._sculpt_phase == "select_template":
                self._sculpt_phase = "select_minerals"
            elif self._sculpt_phase == "carve":
                self._sculpt_phase = "select_template"
            elif self._sculpt_phase == "confirm":
                self._sculpt_phase = "carve"
        elif key == pygame.K_RETURN:
            if self._sculpt_phase == "carve":
                self._sculpt_phase = "confirm"
            elif self._sculpt_phase == "confirm":
                self._complete_sculpture(player)
        elif key == pygame.K_z:
            if self._sculpt_phase == "carve":
                self._pop_undo()
        elif key == pygame.K_s:
            if self._sculpt_phase == "carve":
                self._sculpt_symmetry = not self._sculpt_symmetry

    # ── Undo ─────────────────────────────────────────────────────────────────

    def _push_undo(self):
        self._sculpt_undo_stack.append(copy.deepcopy(self._sculpt_grid))
        if len(self._sculpt_undo_stack) > 40:
            self._sculpt_undo_stack.pop(0)

    def _pop_undo(self):
        if self._sculpt_undo_stack:
            self._sculpt_grid = self._sculpt_undo_stack.pop()

    # ── Completion ───────────────────────────────────────────────────────────

    def _complete_sculpture(self, player):
        sc = player._sculpture_gen.generate(
            mineral  = self._sculpt_mineral,
            height   = self._sculpt_count,
            grid     = copy.deepcopy(self._sculpt_grid),
            template = self._sculpt_template or "custom",
        )
        player.pending_sculptures.append(sc)
        player.sculptures_created.append(sc)
        player._add_item("sculpture")

        # Consume minerals
        mineral   = self._sculpt_mineral
        remaining = player.inventory.get(mineral, 0) - self._sculpt_count
        if remaining <= 0:
            player.inventory.pop(mineral, None)
            for slot_i, slot_id in enumerate(player.hotbar):
                if slot_id == mineral:
                    player.hotbar[slot_i] = None
                    break
        else:
            player.inventory[mineral] = remaining

        # Consume one chisel use
        from items import ITEMS as _ITEMS
        chisel_max = _ITEMS.get("chisel", {}).get("max_uses", 25)
        for slot_i, slot_id in enumerate(player.hotbar):
            if slot_id == "chisel":
                cur = player.hotbar_uses[slot_i]
                if cur is None:
                    cur = chisel_max
                cur -= 1
                if cur <= 0:
                    player.inventory["chisel"] = player.inventory.get("chisel", 1) - 1
                    if player.inventory.get("chisel", 0) <= 0:
                        player.inventory.pop("chisel", None)
                        player.hotbar[slot_i]       = None
                        player.hotbar_uses[slot_i]  = None
                    else:
                        player.hotbar_uses[slot_i] = chisel_max
                else:
                    player.hotbar_uses[slot_i] = cur
                break

        mn = SCULPTABLE_MINERALS.get(self._sculpt_mineral, "Stone")
        player.pending_notifications.append(("Sculpture", f"{mn} Sculpture", None))

        self._sculpt_phase      = "idle"
        self._sculpt_drag_mode  = None
        self._sculpt_hover_cell = None
        self.refinery_open      = False
