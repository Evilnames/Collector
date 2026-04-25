import pygame
import copy
from constants import SCREEN_W, SCREEN_H
from tapestry import (
    WEAVABLE_THREADS, TEMPLATES, BASE_TEMPLATES, THREAD_COLORS,
    TAPESTRY_COLS_PER_BLOCK, TAPESTRY_ROWS_PER_BLOCK,
)

_ACCENT   = (215, 190, 145)
_DIM      = (115, 100, 75)
_BTN_BG   = (38, 30, 18)
_BTN_HL   = (62, 48, 28)
_EMPTY    = (14, 10, 8)
_HOVER_WEAVE   = (90, 30, 20)
_HOVER_RESTORE = (30, 70, 30)
_HOVER_IDLE    = (95, 85, 60)


def _weave_cell(surface, color, rect, empty=False):
    """Draw a single tapestry cell with a woven-cloth look."""
    if empty:
        pygame.draw.rect(surface, _EMPTY, rect)
        shade = (22, 16, 12)
        pygame.draw.line(surface, shade, rect.topleft, (rect.right - 1, rect.top))
        pygame.draw.line(surface, shade, rect.topleft, (rect.left, rect.bottom - 1))
        return
    pygame.draw.rect(surface, color, rect)
    hi  = tuple(min(255, c + 40) for c in color)
    sha = tuple(max(0,   c - 40) for c in color)
    if rect.width >= 4:
        wx = rect.x + rect.width // 2
        pygame.draw.line(surface, sha, (wx, rect.top), (wx, rect.bottom - 1))
    pygame.draw.line(surface, hi, rect.topleft, (rect.right - 2, rect.top))
    pygame.draw.line(surface, sha, (rect.left + 1, rect.bottom - 1),
                     (rect.right - 1, rect.bottom - 1))


class TapestryMixin:

    # ── Phase routing ────────────────────────────────────────────────────────

    def _draw_tapestry_frame(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("TAPESTRY FRAME", True, _ACCENT)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 4))
        hint = self.small.render("ESC back  ·  ENTER confirm", True, _DIM)
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        if self._tapestry_phase == "idle":
            self._tapestry_phase = "select_thread"

        self._draw_tapestry_breadcrumb()

        if self._tapestry_phase == "select_thread":
            self._draw_tapestry_select_thread(player)
        elif self._tapestry_phase == "select_template":
            self._draw_tapestry_select_template(player)
        elif self._tapestry_phase == "weave":
            self._draw_tapestry_weave(player)
        elif self._tapestry_phase == "confirm":
            self._draw_tapestry_confirm(player)

    def _draw_tapestry_breadcrumb(self):
        steps = [
            ("select_thread",   "1 · Thread"),
            ("select_template", "2 · Pattern"),
            ("weave",           "3 · Weave"),
            ("confirm",         "4 · Done"),
        ]
        phase_order = [s[0] for s in steps]
        current_idx = phase_order.index(self._tapestry_phase) if self._tapestry_phase in phase_order else 0

        SW, SH, GAP = 110, 20, 6
        total_w = len(steps) * SW + (len(steps) - 1) * GAP
        bx = SCREEN_W // 2 - total_w // 2
        by = 22
        for i, (phase, label) in enumerate(steps):
            rx = bx + i * (SW + GAP)
            done    = i < current_idx
            current = i == current_idx
            if current:
                bg = (55, 42, 22);  brd = _ACCENT;  tc = _ACCENT
            elif done:
                bg = (30, 42, 22);  brd = (85, 148, 62);  tc = (105, 175, 82)
            else:
                bg = (24, 20, 12);  brd = (52, 44, 30);   tc = _DIM
            pygame.draw.rect(self.screen, bg,  (rx, by, SW, SH))
            pygame.draw.rect(self.screen, brd, (rx, by, SW, SH), 1)
            ls = self.small.render(label, True, tc)
            self.screen.blit(ls, (rx + SW // 2 - ls.get_width() // 2,
                                  by + SH // 2 - ls.get_height() // 2))

    # ── Phase 1: Thread Selection ────────────────────────────────────────────

    def _draw_tapestry_select_thread(self, player):
        self._tapestry_thread_rects.clear()
        has_needle = player.inventory.get("weaving_needle", 0) > 0
        if not has_needle:
            msg = self.font.render("You need a Weaving Needle to make tapestries.", True, (220, 80, 60))
            self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2 - 20))
            sub = self.small.render("Craft one at a workbench: 2 iron ingots + 1 wool", True, _DIM)
            self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, SCREEN_H // 2 + 10))
            return

        available = {tid: player.inventory.get(tid, 0)
                     for tid in WEAVABLE_THREADS if player.inventory.get(tid, 0) > 0}
        if not available:
            msg = self.font.render("No thread materials in inventory.", True, (200, 140, 60))
            self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2 - 20))
            sub2 = self.small.render("Use Wool, Cotton Fiber, or Dye Extracts as thread.", True, _DIM)
            self.screen.blit(sub2, (SCREEN_W // 2 - sub2.get_width() // 2, SCREEN_H // 2 + 10))
            return

        sub = self.small.render("Choose thread, height (1–4 tall) and width (1–4 wide):", True, _ACCENT)
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 48))

        CARD_W, CARD_H, GAP = 200, 150, 12
        total_w = len(available) * CARD_W + (len(available) - 1) * GAP
        gx0 = (SCREEN_W - total_w) // 2
        gy0 = 65

        cost = self._tapestry_count * self._tapestry_width

        for ti, (tid, count) in enumerate(available.items()):
            cx  = gx0 + ti * (CARD_W + GAP)
            col = THREAD_COLORS.get(tid, (200, 195, 175))
            sel = (self._tapestry_thread == tid)
            bg  = _BTN_HL if sel else _BTN_BG
            brd = col if sel else _DIM

            pygame.draw.rect(self.screen, bg,  (cx, gy0, CARD_W, CARD_H))
            pygame.draw.rect(self.screen, brd, (cx, gy0, CARD_W, CARD_H), 2 if sel else 1)

            sw_r = pygame.Rect(cx + 10, gy0 + 10, 28, 28)
            _weave_cell(self.screen, col, sw_r)

            name_lbl  = self.font.render(WEAVABLE_THREADS[tid], True, col)
            count_lbl = self.small.render(f"×{count} available", True, _DIM)
            self.screen.blit(name_lbl,  (cx + 46, gy0 + 12))
            self.screen.blit(count_lbl, (cx + 46, gy0 + 32))

            self._tapestry_thread_rects[tid] = pygame.Rect(cx, gy0, CARD_W, CARD_H)

            if sel:
                # Height row
                h_label = self.small.render("Height:", True, _DIM)
                self.screen.blit(h_label, (cx + 10, gy0 + CARD_H - 96))
                for h in range(1, 5):
                    bx2 = cx + 10 + (h - 1) * 46
                    by2 = gy0 + CARD_H - 80
                    ok  = count >= h * self._tapestry_width
                    cur = (self._tapestry_count == h)
                    btn_col = col if cur else (_BTN_HL if ok else (28, 22, 14))
                    brd2    = brd if cur else (_DIM if ok else (36, 30, 20))
                    r2 = pygame.Rect(bx2, by2, 38, 26)
                    pygame.draw.rect(self.screen, btn_col, r2)
                    pygame.draw.rect(self.screen, brd2, r2, 2 if cur else 1)
                    hl = self.small.render(str(h), True, (255, 255, 255) if ok else (55, 48, 32))
                    self.screen.blit(hl, (bx2 + 19 - hl.get_width() // 2, by2 + 5))
                    self._tapestry_thread_rects[f"{tid}_h{h}"] = r2

                # Width row
                w_label = self.small.render("Width:", True, _DIM)
                self.screen.blit(w_label, (cx + 10, gy0 + CARD_H - 52))
                for w in range(1, 5):
                    bx3 = cx + 10 + (w - 1) * 46
                    by3 = gy0 + CARD_H - 36
                    ok2 = count >= self._tapestry_count * w
                    cur2 = (self._tapestry_width == w)
                    btn_col2 = col if cur2 else (_BTN_HL if ok2 else (28, 22, 14))
                    brd3     = brd if cur2 else (_DIM if ok2 else (36, 30, 20))
                    r3 = pygame.Rect(bx3, by3, 38, 26)
                    pygame.draw.rect(self.screen, btn_col2, r3)
                    pygame.draw.rect(self.screen, brd3, r3, 2 if cur2 else 1)
                    wl = self.small.render(str(w), True, (255, 255, 255) if ok2 else (55, 48, 32))
                    self.screen.blit(wl, (bx3 + 19 - wl.get_width() // 2, by3 + 5))
                    self._tapestry_thread_rects[f"{tid}_w{w}"] = r3

        if self._tapestry_thread and self._tapestry_count > 0:
            thread_count = player.inventory.get(self._tapestry_thread, 0)
            can_proceed  = thread_count >= cost
            col2 = THREAD_COLORS.get(self._tapestry_thread, _ACCENT)
            prev_x = SCREEN_W // 2 + max(len(available), 1) * (CARD_W + GAP) // 2 + 20
            prev_x = min(prev_x, SCREEN_W - 80)
            # Draw footprint preview (width × height blocks)
            for k in range(self._tapestry_count):
                for wk in range(self._tapestry_width):
                    bk_r = pygame.Rect(prev_x + wk * 22,
                                       gy0 + (self._tapestry_count - 1 - k) * 30, 18, 26)
                    _weave_cell(self.screen, col2, bk_r)
            dim_lbl = self.small.render(
                f"{self._tapestry_width}W × {self._tapestry_count}H  (cost: ×{cost})",
                True, _DIM)
            self.screen.blit(dim_lbl, (prev_x, gy0 + self._tapestry_count * 30 + 4))

            btn_y    = gy0 + CARD_H + 24
            btn_rect = pygame.Rect(SCREEN_W // 2 - 95, btn_y, 190, 36)
            bg3  = (48, 68, 30) if can_proceed else (32, 25, 14)
            brd3 = (105, 185, 72) if can_proceed else (56, 46, 28)
            tc3  = (155, 235, 115) if can_proceed else _DIM
            pygame.draw.rect(self.screen, bg3,  btn_rect)
            pygame.draw.rect(self.screen, brd3, btn_rect, 2)
            lbl3 = self.font.render("Choose Pattern  →", True, tc3)
            self.screen.blit(lbl3, (btn_rect.centerx - lbl3.get_width() // 2, btn_rect.y + 8))
            self._tapestry_thread_rects["_confirm"] = btn_rect

    # ── Phase 2: Template Selection ──────────────────────────────────────────

    def _draw_tapestry_select_template(self, player):
        self._tapestry_template_rects.clear()
        sub = self.small.render("Pick a pattern to start from — or weave from scratch:", True, _ACCENT)
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 48))

        CARD_W, CARD_H, GAP = 98, 90, 7
        COLS = 7
        all_opts  = ["Custom"] + list(BASE_TEMPLATES)
        total_rows = (len(all_opts) + COLS - 1) // COLS
        total_w    = min(len(all_opts), COLS) * CARD_W + (min(len(all_opts), COLS) - 1) * GAP
        gx0 = max(8, (SCREEN_W - total_w) // 2)
        gy0 = 54
        col = THREAD_COLORS.get(self._tapestry_thread, (200, 195, 175))

        for oi, opt in enumerate(all_opts):
            ci2 = oi % COLS
            ri2 = oi // COLS
            cx  = gx0 + ci2 * (CARD_W + GAP)
            cy  = gy0 + ri2 * (CARD_H + GAP)
            sel = (opt == "Custom" and self._tapestry_template is None) or \
                  (opt != "Custom" and self._tapestry_template == opt)
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
                pygame.draw.rect(self.screen, _EMPTY, preview_rect)
            else:
                lbl = self.small.render(opt, True, _ACCENT)
                self.screen.blit(lbl, (cx + CARD_W // 2 - lbl.get_width() // 2, cy + 4))
                if opt in TEMPLATES:
                    grid = TEMPLATES[opt](self._tapestry_count, self._tapestry_width)
                    self._draw_mini_tapestry_preview(self.screen, grid, self._tapestry_count,
                                                     cx + 5, cy + 18, CARD_W - 10, CARD_H - 24, col)

            self._tapestry_template_rects[opt] = pygame.Rect(cx, cy, CARD_W, CARD_H)

        info_y = gy0 + total_rows * (CARD_H + GAP) + 8
        mc  = THREAD_COLORS.get(self._tapestry_thread, _ACCENT)
        mn  = WEAVABLE_THREADS.get(self._tapestry_thread, "?")
        tag = self.small.render(
            f"  {mn}  ×{self._tapestry_count * self._tapestry_width}   ·   "
            f"{self._tapestry_width}W × {self._tapestry_count}H",
            True, mc)
        pygame.draw.rect(self.screen, _BTN_BG,
                         (SCREEN_W // 2 - tag.get_width() // 2 - 8,
                          info_y - 2, tag.get_width() + 16, tag.get_height() + 4))
        self.screen.blit(tag, (SCREEN_W // 2 - tag.get_width() // 2, info_y))

    def _draw_mini_tapestry_preview(self, surf, grid, height, x, y, w, h, color):
        rows = len(grid) if grid else height * TAPESTRY_ROWS_PER_BLOCK
        cols = len(grid[0]) if grid and grid[0] else TAPESTRY_COLS_PER_BLOCK
        if grid is None:
            pygame.draw.rect(surf, _EMPTY, (x, y, w, h))
            return
        cw = max(1, w // cols)
        ch = max(1, h // max(1, rows))
        hi = tuple(min(255, c + 25) for c in color)
        lo = tuple(max(0,   c - 30) for c in color)
        for ri, row in enumerate(grid):
            for ci, filled in enumerate(row):
                px = x + ci * cw
                py = y + ri * ch
                cell_c = (hi if ri % 2 == 0 else lo) if filled else _EMPTY
                pygame.draw.rect(surf, cell_c, (px, py, cw, ch))

    # ── Phase 3: Weaving ─────────────────────────────────────────────────────

    def _draw_tapestry_weave(self, player):
        self._tapestry_cell_rects.clear()
        col  = THREAD_COLORS.get(self._tapestry_thread, (200, 195, 175))
        rows = len(self._tapestry_grid)
        COLS = len(self._tapestry_grid[0]) if self._tapestry_grid else TAPESTRY_COLS_PER_BLOCK

        available_h = SCREEN_H - 100
        available_w = SCREEN_W - 260
        CELL_SIZE   = min(available_w // COLS, available_h // max(1, rows))
        CELL_SIZE   = max(4, CELL_SIZE)
        grid_w = COLS * CELL_SIZE
        grid_h = rows * CELL_SIZE

        PANEL_W = 220
        PANEL_X = SCREEN_W - PANEL_W - 12
        gx = (PANEL_X - grid_w) // 2
        gx = max(12, gx)
        gy = 50

        hi_col  = tuple(min(255, c + 35) for c in col)
        lo_col  = tuple(max(0,   c - 42) for c in col)

        for ri, row in enumerate(self._tapestry_grid):
            for ci, filled in enumerate(row):
                px = gx + ci * CELL_SIZE
                py = gy + ri * CELL_SIZE
                cr = pygame.Rect(px, py, CELL_SIZE, CELL_SIZE)

                hover = (self._tapestry_hover_cell == (ri, ci))
                if hover:
                    mode = self._tapestry_drag_mode
                    if mode == "weave":
                        tint = _HOVER_WEAVE
                    elif mode == "unweave":
                        tint = _HOVER_RESTORE
                    else:
                        tint = _HOVER_IDLE
                    pygame.draw.rect(self.screen, tint, cr)
                else:
                    if filled:
                        cell_col = hi_col if ri % 2 == 0 else lo_col
                        _weave_cell(self.screen, cell_col, cr)
                    else:
                        pygame.draw.rect(self.screen, _EMPTY, cr)

                if self._tapestry_symmetry and CELL_SIZE >= 6:
                    mirror_ci = COLS - 1 - ci
                    if hover and ci != mirror_ci:
                        mr = pygame.Rect(gx + mirror_ci * CELL_SIZE, py, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(self.screen, (tint[0] // 2, tint[1] // 2, tint[2] // 2), mr)

                self._tapestry_cell_rects[(ri, ci)] = cr

        # Block dividers — horizontal (height seams)
        for k in range(1, self._tapestry_count):
            div_y = gy + k * TAPESTRY_ROWS_PER_BLOCK * CELL_SIZE
            pygame.draw.line(self.screen, col, (gx, div_y), (gx + grid_w, div_y), 2)
            lbl = self.small.render(f"R{k + 1}", True, col)
            self.screen.blit(lbl, (gx - lbl.get_width() - 4, div_y + 2))

        # Block dividers — vertical (width seams)
        for k in range(1, self._tapestry_width):
            div_x = gx + k * TAPESTRY_COLS_PER_BLOCK * CELL_SIZE
            pygame.draw.line(self.screen, col, (div_x, gy), (div_x, gy + grid_h), 2)

        pygame.draw.rect(self.screen, col, (gx - 2, gy - 2, grid_w + 4, grid_h + 4), 2)

        # Side panel
        py2 = gy

        mode_text  = "WEAVE (left-drag)" if self._tapestry_drag_mode != "unweave" else "UNWEAVE (right-drag)"
        mode_color = (220, 80, 60) if self._tapestry_drag_mode != "unweave" else (80, 200, 80)
        if self._tapestry_drag_mode is None:
            mode_text, mode_color = "No drag", _DIM
        tool_s = self.small.render(mode_text, True, mode_color)
        self.screen.blit(tool_s, (PANEL_X, py2))
        py2 += 18

        controls = [
            ("Left-drag",  "add thread"),
            ("Right-drag", "remove thread"),
            ("Z",          "undo stroke"),
            ("ENTER",      "preview"),
        ]
        for key_s, desc_s in controls:
            ks = self.small.render(key_s, True, _ACCENT)
            ds = self.small.render(desc_s, True, _DIM)
            self.screen.blit(ks, (PANEL_X, py2))
            self.screen.blit(ds, (PANEL_X + ks.get_width() + 6, py2))
            py2 += 15
        py2 += 8

        tn  = WEAVABLE_THREADS.get(self._tapestry_thread, "")
        for line in [f"Thread: {tn}",
                     f"Size: {self._tapestry_width}W × {self._tapestry_count}H",
                     f"Pattern: {self._tapestry_template or 'Custom'}"]:
            s = self.small.render(line, True, _DIM)
            self.screen.blit(s, (PANEL_X, py2))
            py2 += 14
        py2 += 8

        sym_r = pygame.Rect(PANEL_X, py2, PANEL_W - 4, 28)
        sym_bg  = (28, 46, 28) if self._tapestry_symmetry else _BTN_BG
        sym_brd = (78, 180, 78) if self._tapestry_symmetry else _DIM
        sym_tc  = (128, 230, 98) if self._tapestry_symmetry else _ACCENT
        pygame.draw.rect(self.screen, sym_bg,  sym_r)
        pygame.draw.rect(self.screen, sym_brd, sym_r, 2)
        sym_lbl = self.small.render(
            ("✦ Mirror  ON" if self._tapestry_symmetry else "  Mirror  OFF"), True, sym_tc)
        self.screen.blit(sym_lbl, (sym_r.centerx - sym_lbl.get_width() // 2, sym_r.y + 6))
        self._tapestry_cell_rects["_symmetry"] = sym_r
        py2 += 36

        half_w = (PANEL_W - 4) // 2 - 4
        fill_r  = pygame.Rect(PANEL_X,              py2, half_w, 26)
        clear_r = pygame.Rect(PANEL_X + half_w + 8, py2, half_w, 26)
        for r, label in ((fill_r, "Fill All"), (clear_r, "Clear All")):
            pygame.draw.rect(self.screen, _BTN_BG, r)
            pygame.draw.rect(self.screen, _DIM, r, 1)
            ls = self.small.render(label, True, _ACCENT)
            self.screen.blit(ls, (r.centerx - ls.get_width() // 2, r.y + 5))
        self._tapestry_cell_rects["_fill"]  = fill_r
        self._tapestry_cell_rects["_clear"] = clear_r
        py2 += 34

        if self._tapestry_undo_stack:
            us = self.small.render(
                f"  undo: {len(self._tapestry_undo_stack)} step{'s' if len(self._tapestry_undo_stack) > 1 else ''}",
                True, _DIM)
            self.screen.blit(us, (PANEL_X, py2))
        py2 += 20

        py2 += 6
        prev_label = self.small.render("Preview:", True, _DIM)
        self.screen.blit(prev_label, (PANEL_X, py2))
        py2 += 14
        self._draw_tapestry_world_preview(PANEL_X, py2, PANEL_W - 4, col)
        py2 += self._tapestry_count * 32 + 8

        confirm_r = pygame.Rect(PANEL_X, py2, PANEL_W - 4, 34)
        pygame.draw.rect(self.screen, (40, 58, 28), confirm_r)
        pygame.draw.rect(self.screen, (78, 160, 58), confirm_r, 2)
        cl2 = self.font.render("Preview  →", True, (128, 220, 98))
        self.screen.blit(cl2, (confirm_r.centerx - cl2.get_width() // 2, confirm_r.y + 7))
        self._tapestry_cell_rects["_confirm"] = confirm_r

    def _draw_tapestry_world_preview(self, px, py, w, thread_color):
        actual_cols = len(self._tapestry_grid[0]) if self._tapestry_grid else TAPESTRY_COLS_PER_BLOCK
        CELL_W = max(1, (w * self._tapestry_width) // actual_cols)
        CELL_H = max(1, 32 // TAPESTRY_ROWS_PER_BLOCK)
        grid_px_w = actual_cols * CELL_W
        grid_px_h = len(self._tapestry_grid) * CELL_H
        pygame.draw.rect(self.screen, (10, 8, 6), (px, py, grid_px_w + 4, grid_px_h + 4))
        hi  = tuple(min(255, c + 28) for c in thread_color)
        lo  = tuple(max(0,   c - 38) for c in thread_color)
        for row_idx, row in enumerate(self._tapestry_grid):
            world_py = py + 2 + row_idx * CELL_H
            for ci, filled in enumerate(row):
                if filled:
                    c = hi if row_idx % 2 == 0 else lo
                    pygame.draw.rect(self.screen, c,
                                     (px + 2 + ci * CELL_W, world_py, CELL_W, CELL_H))
        for k in range(1, self._tapestry_count):
            line_y = py + 2 + k * TAPESTRY_ROWS_PER_BLOCK * CELL_H
            pygame.draw.line(self.screen, (45, 38, 28),
                             (px + 2, line_y), (px + 2 + grid_px_w, line_y))
        pygame.draw.rect(self.screen, thread_color, (px, py, grid_px_w + 4, grid_px_h + 4), 1)

    # ── Phase 4: Confirm ─────────────────────────────────────────────────────

    def _draw_tapestry_confirm(self, player):
        col  = THREAD_COLORS.get(self._tapestry_thread, (200, 195, 175))
        rows = len(self._tapestry_grid)
        actual_cols = len(self._tapestry_grid[0]) if self._tapestry_grid else TAPESTRY_COLS_PER_BLOCK

        sub = self.font.render("Hang this tapestry?", True, _ACCENT)
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 48))

        max_cell_w = (SCREEN_W - 40) // actual_cols
        max_cell_h = max(6, (SCREEN_H - 180) // max(1, rows))
        CELL_SIZE = min(max_cell_w, max_cell_h)
        grid_w = actual_cols * CELL_SIZE
        grid_h = rows * CELL_SIZE
        gx = SCREEN_W // 2 - grid_w // 2
        gy = 70

        hi = tuple(min(255, c + 35) for c in col)
        lo = tuple(max(0,   c - 42) for c in col)
        for ri, row in enumerate(self._tapestry_grid):
            for ci, filled in enumerate(row):
                r = pygame.Rect(gx + ci * CELL_SIZE, gy + ri * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if filled:
                    cell_col = hi if ri % 2 == 0 else lo
                    _weave_cell(self.screen, cell_col, r)
                else:
                    pygame.draw.rect(self.screen, _EMPTY, r)

        for k in range(1, self._tapestry_count):
            div_y = gy + k * TAPESTRY_ROWS_PER_BLOCK * CELL_SIZE
            pygame.draw.line(self.screen, col, (gx, div_y), (gx + grid_w, div_y), 2)
        for k in range(1, self._tapestry_width):
            div_x = gx + k * TAPESTRY_COLS_PER_BLOCK * CELL_SIZE
            pygame.draw.line(self.screen, col, (div_x, gy), (div_x, gy + grid_h), 2)

        pygame.draw.rect(self.screen, col, (gx - 2, gy - 2, grid_w + 4, grid_h + 4), 2)

        total_cells  = rows * actual_cols
        filled_cells = sum(cell for row in self._tapestry_grid for cell in row)
        coverage_pct = int(100 * filled_cells / max(1, total_cells))
        tn = WEAVABLE_THREADS.get(self._tapestry_thread, "?")
        cost = self._tapestry_count * self._tapestry_width
        info = self.small.render(
            f"{tn}  ·  {self._tapestry_width}W × {self._tapestry_count}H  ·  cost ×{cost}  ·  "
            f"{coverage_pct}% woven  ·  pattern: {self._tapestry_template or 'custom'}",
            True, _DIM)
        self.screen.blit(info, (SCREEN_W // 2 - info.get_width() // 2, gy + grid_h + 10))

        btn_y = gy + grid_h + 32
        accept_r = pygame.Rect(SCREEN_W // 2 - 104, btn_y, 96, 34)
        back_r   = pygame.Rect(SCREEN_W // 2 + 8,   btn_y, 96, 34)
        pygame.draw.rect(self.screen, (32, 52, 24), accept_r)
        pygame.draw.rect(self.screen, (72, 158, 52), accept_r, 2)
        pygame.draw.rect(self.screen, _BTN_BG, back_r)
        pygame.draw.rect(self.screen, _DIM, back_r, 2)
        al = self.font.render("Weave!", True, (112, 215, 82))
        bl = self.font.render("← Edit",  True, _ACCENT)
        self.screen.blit(al, (accept_r.centerx - al.get_width() // 2, accept_r.y + 7))
        self.screen.blit(bl, (back_r.centerx   - bl.get_width() // 2, back_r.y   + 7))
        self._tapestry_cell_rects["_accept"] = accept_r
        self._tapestry_cell_rects["_back"]   = back_r

    # ── Click handlers ───────────────────────────────────────────────────────

    def _handle_tapestry_frame_click(self, pos, player, right=False):
        if self._tapestry_phase == "select_thread":
            self._handle_tapestry_thread_click(pos, player)
        elif self._tapestry_phase == "select_template":
            self._handle_tapestry_template_click(pos, player)
        elif self._tapestry_phase == "weave":
            self._handle_tapestry_weave_click(pos, player, right)
        elif self._tapestry_phase == "confirm":
            self._handle_tapestry_confirm_click(pos, player)

    def _handle_tapestry_thread_click(self, pos, player):
        confirm_r = self._tapestry_thread_rects.get("_confirm")
        if confirm_r and confirm_r.collidepoint(pos):
            if self._tapestry_thread and self._tapestry_count > 0:
                cost = self._tapestry_count * self._tapestry_width
                if player.inventory.get(self._tapestry_thread, 0) >= cost:
                    self._tapestry_phase = "select_template"
            return
        # Height buttons
        for key, rect in self._tapestry_thread_rects.items():
            if "_h" not in str(key):
                continue
            if rect.collidepoint(pos):
                parts = key.rsplit("_h", 1)
                if len(parts) == 2:
                    h   = int(parts[1])
                    tid = parts[0]
                    if player.inventory.get(tid, 0) >= h * self._tapestry_width:
                        self._tapestry_count = h
                return
        # Width buttons
        for key, rect in self._tapestry_thread_rects.items():
            if "_w" not in str(key):
                continue
            if rect.collidepoint(pos):
                parts = key.rsplit("_w", 1)
                if len(parts) == 2:
                    w   = int(parts[1])
                    tid = parts[0]
                    if player.inventory.get(tid, 0) >= self._tapestry_count * w:
                        self._tapestry_width = w
                return
        # Thread card
        for key, rect in self._tapestry_thread_rects.items():
            if "_h" in str(key) or "_w" in str(key) or key == "_confirm":
                continue
            if rect.collidepoint(pos):
                self._tapestry_thread = key
                if self._tapestry_count == 0:
                    self._tapestry_count = 1
                return

    def _handle_tapestry_template_click(self, pos, player):
        cols = self._tapestry_width * TAPESTRY_COLS_PER_BLOCK
        for opt, rect in self._tapestry_template_rects.items():
            if rect.collidepoint(pos):
                self._tapestry_template = None if opt == "Custom" else opt
                rows = self._tapestry_count * TAPESTRY_ROWS_PER_BLOCK
                if opt == "Custom":
                    self._tapestry_grid = [[True] * cols for _ in range(rows)]
                elif opt in TEMPLATES:
                    self._tapestry_grid = TEMPLATES[opt](self._tapestry_count, self._tapestry_width)
                else:
                    self._tapestry_grid = [[True] * cols for _ in range(rows)]
                self._tapestry_undo_stack = []
                self._tapestry_drag_mode  = None
                self._tapestry_phase = "weave"
                return

    def _handle_tapestry_weave_click(self, pos, player, right=False):
        sr = self._tapestry_cell_rects.get("_symmetry")
        if sr and sr.collidepoint(pos):
            self._tapestry_symmetry = not self._tapestry_symmetry
            return
        fr = self._tapestry_cell_rects.get("_fill")
        if fr and fr.collidepoint(pos):
            self._tapestry_push_undo()
            cols = len(self._tapestry_grid[0]) if self._tapestry_grid else TAPESTRY_COLS_PER_BLOCK
            self._tapestry_grid = [[True] * cols for _ in range(len(self._tapestry_grid))]
            return
        cr = self._tapestry_cell_rects.get("_clear")
        if cr and cr.collidepoint(pos):
            self._tapestry_push_undo()
            cols = len(self._tapestry_grid[0]) if self._tapestry_grid else TAPESTRY_COLS_PER_BLOCK
            self._tapestry_grid = [[False] * cols for _ in range(len(self._tapestry_grid))]
            return
        confirm_r = self._tapestry_cell_rects.get("_confirm")
        if confirm_r and confirm_r.collidepoint(pos):
            self._tapestry_phase = "confirm"
            return
        COLS = len(self._tapestry_grid[0]) if self._tapestry_grid else TAPESTRY_COLS_PER_BLOCK
        for key, rect in self._tapestry_cell_rects.items():
            if not isinstance(key, tuple):
                continue
            ri, ci = key
            if rect.collidepoint(pos):
                self._tapestry_push_undo()
                new_val = not right
                self._tapestry_grid[ri][ci] = new_val
                if self._tapestry_symmetry:
                    self._tapestry_grid[ri][COLS - 1 - ci] = new_val
                self._tapestry_drag_mode = "unweave" if right else "weave"
                return

    def _handle_tapestry_confirm_click(self, pos, player):
        accept_r = self._tapestry_cell_rects.get("_accept")
        if accept_r and accept_r.collidepoint(pos):
            self._complete_tapestry(player)
            return
        back_r = self._tapestry_cell_rects.get("_back")
        if back_r and back_r.collidepoint(pos):
            self._tapestry_phase = "weave"

    # ── Per-frame drag update ─────────────────────────────────────────────────

    def _tapestry_update_drag(self, pos, mouse_btns):
        if self._tapestry_phase != "weave":
            self._tapestry_drag_mode  = None
            self._tapestry_hover_cell = None
            return

        left_held  = mouse_btns[0]
        right_held = mouse_btns[2]
        COLS = len(self._tapestry_grid[0]) if self._tapestry_grid else TAPESTRY_COLS_PER_BLOCK

        hover_hit = None
        for key, rect in self._tapestry_cell_rects.items():
            if not isinstance(key, tuple):
                continue
            if rect.collidepoint(pos):
                hover_hit = key
                break
        self._tapestry_hover_cell = hover_hit

        if left_held or right_held:
            if self._tapestry_drag_mode is None:
                return
            if hover_hit is not None:
                ri, ci = hover_hit
                new_val = (self._tapestry_drag_mode == "weave")
                if self._tapestry_grid[ri][ci] != new_val:
                    self._tapestry_grid[ri][ci] = new_val
                    if self._tapestry_symmetry:
                        self._tapestry_grid[ri][COLS - 1 - ci] = new_val
        else:
            self._tapestry_drag_mode = None

    # ── Keyboard ─────────────────────────────────────────────────────────────

    def handle_tapestry_keydown(self, key, player):
        if key == pygame.K_ESCAPE:
            if self._tapestry_phase in ("select_thread", "idle"):
                self._tapestry_phase = "idle"
                self.refinery_open = False
            elif self._tapestry_phase == "select_template":
                self._tapestry_phase = "select_thread"
            elif self._tapestry_phase == "weave":
                self._tapestry_phase = "select_template"
            elif self._tapestry_phase == "confirm":
                self._tapestry_phase = "weave"
        elif key == pygame.K_RETURN:
            if self._tapestry_phase == "weave":
                self._tapestry_phase = "confirm"
            elif self._tapestry_phase == "confirm":
                self._complete_tapestry(player)
        elif key == pygame.K_z:
            if self._tapestry_phase == "weave":
                self._tapestry_pop_undo()
        elif key == pygame.K_s:
            if self._tapestry_phase == "weave":
                self._tapestry_symmetry = not self._tapestry_symmetry

    # ── Undo ─────────────────────────────────────────────────────────────────

    def _tapestry_push_undo(self):
        self._tapestry_undo_stack.append(copy.deepcopy(self._tapestry_grid))
        if len(self._tapestry_undo_stack) > 40:
            self._tapestry_undo_stack.pop(0)

    def _tapestry_pop_undo(self):
        if self._tapestry_undo_stack:
            self._tapestry_grid = self._tapestry_undo_stack.pop()

    # ── Completion ───────────────────────────────────────────────────────────

    def _complete_tapestry(self, player):
        tp = player._tapestry_gen.generate(
            thread   = self._tapestry_thread,
            height   = self._tapestry_count,
            width    = self._tapestry_width,
            grid     = copy.deepcopy(self._tapestry_grid),
            template = self._tapestry_template or "custom",
        )
        player.pending_tapestries.append(tp)
        player.tapestries_created.append(tp)
        player._add_item("custom_tapestry")

        # Consume thread material (height × width units)
        thread    = self._tapestry_thread
        cost      = self._tapestry_count * self._tapestry_width
        remaining = player.inventory.get(thread, 0) - cost
        if remaining <= 0:
            player.inventory.pop(thread, None)
            for slot_i, slot_id in enumerate(player.hotbar):
                if slot_id == thread:
                    player.hotbar[slot_i] = None
                    break
        else:
            player.inventory[thread] = remaining

        # Consume one needle use
        from items import ITEMS as _ITEMS
        needle_max = _ITEMS.get("weaving_needle", {}).get("max_uses", 30)
        for slot_i, slot_id in enumerate(player.hotbar):
            if slot_id == "weaving_needle":
                cur = player.hotbar_uses[slot_i]
                if cur is None:
                    cur = needle_max
                cur -= 1
                if cur <= 0:
                    player.inventory["weaving_needle"] = player.inventory.get("weaving_needle", 1) - 1
                    if player.inventory.get("weaving_needle", 0) <= 0:
                        player.inventory.pop("weaving_needle", None)
                        player.hotbar[slot_i]      = None
                        player.hotbar_uses[slot_i] = None
                    else:
                        player.hotbar_uses[slot_i] = needle_max
                else:
                    player.hotbar_uses[slot_i] = cur
                break

        tn = WEAVABLE_THREADS.get(self._tapestry_thread, "Thread")
        size_str = f"{self._tapestry_width}W×{self._tapestry_count}H" if self._tapestry_width > 1 else f"{self._tapestry_count}H"
        player.pending_notifications.append(("Tapestry", f"{tn} Tapestry ({size_str})", None))

        self._tapestry_phase      = "idle"
        self._tapestry_drag_mode  = None
        self._tapestry_hover_cell = None
        self.refinery_open        = False
