"""Charcuterie UI mixin — Salting Rack + Curing Cellar panels."""
import time
import pygame
from constants import SCREEN_W, SCREEN_H
from charcuterie import (
    MEAT_SOURCES, CURE_TYPES, CURE_METHODS, CURE_METHOD_ORDER, CURE_ORDER,
    BUFF_DESCS, CURE_TYPE_BUFFS, OUTPUT_DESCS, OUTPUT_COLORS,
    _CODEX_MEATS, TYPE_ORDER, MEAT_DISPLAY_NAMES,
    apply_cure_method, start_aging, finish_aging,
    get_charcuterie_output_id, age_progress,
)

# Zone fill rate: hold mouse ~2.5 s to fill one zone
_ZONE_FILL_RATE = 0.40  # per second while held

# Colors
_COL_BG       = (22, 15, 10)
_COL_TITLE    = (210, 165, 100)
_COL_SUBTITLE = (150, 120, 80)
_COL_HINT     = (110, 90, 60)
_COL_BORDER   = (140, 105, 70)
_COL_SEL_BG   = (55, 38, 18)
_COL_SEL_BOR  = (210, 165, 90)
_COL_DIM_BG   = (18, 12, 8)
_COL_DIM_BOR  = (65, 50, 30)
_COL_ZONE_FILL   = (190, 140, 80)
_COL_ZONE_DONE   = (100, 175, 90)
_COL_ZONE_ACTIVE = (230, 185, 80)
_COL_BAR_BG  = (35, 25, 15)
_COL_BAR_FILL = (160, 115, 65)
_COL_BAR_DONE = (90, 165, 80)


def _has_salt(player) -> bool:
    """Returns True if the player has any salt item in inventory."""
    return any(
        player.inventory.get(k, 0) > 0
        for k in player.inventory
        if "salt" in k
    )


def _consume_salt(player) -> bool:
    """Consume one salt item. Returns True if successful."""
    for k in sorted(player.inventory):
        if "salt" in k and player.inventory.get(k, 0) > 0:
            player._remove_item(k)
            return True
    return False


class CharcuterieMixin:

    # ── Open helpers ─────────────────────────────────────────────────────────

    def _open_salting_rack(self, bx, by, player):
        from blocks import SALTING_RACK_BLOCK
        self.refinery_open      = True
        self.refinery_block_id  = SALTING_RACK_BLOCK
        self._curing_rack_phase  = "select_meat"
        self._curing_meat_sel    = None
        self._curing_cure_sel    = None
        self._curing_method_sel  = None
        self._curing_zone_prog   = [0.0, 0.0, 0.0, 0.0]
        self._curing_zone_held   = None
        self._curing_wip         = None
        self._curing_zone_rects  = []

    def _open_curing_cellar(self, bx, by, player):
        from blocks import CURING_CELLAR_BLOCK
        self.refinery_open      = True
        self.refinery_block_id  = CURING_CELLAR_BLOCK
        self._curing_cellar_phase = "select"
        self._curing_cellar_idx   = None
        self._curing_result_item  = None
        self._curing_item_btns    = []

    # ── Top-level draw ────────────────────────────────────────────────────────

    def _draw_salting_rack(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("SALTING RACK", True, _COL_TITLE)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, _COL_HINT)
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        ph = self._curing_rack_phase
        if ph == "select_meat":
            self._draw_rack_select_meat(player)
        elif ph == "select_cure":
            self._draw_rack_select_cure(player)
        elif ph == "select_method":
            self._draw_rack_select_method(player)
        elif ph == "massaging":
            self._draw_rack_massage(player, dt)
        elif ph == "result":
            self._draw_rack_result(player)

    def _draw_curing_cellar(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("CURING CELLAR", True, (160, 120, 75))
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, _COL_HINT)
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        ph = self._curing_cellar_phase
        if ph == "select":
            self._draw_cellar_select(player)
        elif ph == "aging":
            self._draw_cellar_aging(player)

    # ── Salting Rack — phase: select_meat ────────────────────────────────────

    def _draw_rack_select_meat(self, player):
        cx = SCREEN_W // 2
        lbl = self.font.render("SELECT MEAT", True, _COL_TITLE)
        self.screen.blit(lbl, (cx - lbl.get_width() // 2, 48))

        if not _has_salt(player):
            warn = self.small.render("You need a salt item in your inventory.", True, (220, 100, 80))
            self.screen.blit(warn, (cx - warn.get_width() // 2, 80))

        self._curing_meat_btns = {}
        bw, bh, gap = 190, 58, 12
        meats = list(MEAT_SOURCES.keys())
        total_w = min(len(meats), 4) * (bw + gap) - gap
        x0 = cx - total_w // 2
        y0 = 100
        row = 0
        for i, meat_key in enumerate(meats):
            if i > 0 and i % 4 == 0:
                row += 1
                x0 = cx - total_w // 2
                y0 += bh + 14
            count = player.inventory.get(meat_key, 0)
            has   = count > 0 and _has_salt(player)
            info  = MEAT_SOURCES[meat_key]
            rect  = pygame.Rect(x0 + (i % 4) * (bw + gap), y0, bw, bh)
            bg    = _COL_SEL_BG if has else _COL_DIM_BG
            pygame.draw.rect(self.screen, bg, rect, border_radius=6)
            border = _COL_SEL_BOR if has else _COL_DIM_BOR
            pygame.draw.rect(self.screen, border, rect, 2, border_radius=6)
            name_s = self.small.render(info["display"], True,
                                       _COL_TITLE if has else (80, 65, 40))
            self.screen.blit(name_s, (rect.centerx - name_s.get_width() // 2, rect.y + 8))
            cnt_s = self.small.render(f"x{count} in inventory", True,
                                      (160, 130, 70) if has else (60, 50, 28))
            self.screen.blit(cnt_s, (rect.centerx - cnt_s.get_width() // 2, rect.y + 28))
            cures_txt = ", ".join(c.capitalize() for c in info["eligible_cures"])
            c_s = self.small.render(cures_txt, True, (120, 100, 55) if has else (50, 42, 22))
            self.screen.blit(c_s, (rect.centerx - c_s.get_width() // 2, rect.y + 42))
            if has:
                self._curing_meat_btns[meat_key] = rect

        note = self.small.render("Click a meat to continue →", True, _COL_SUBTITLE)
        self.screen.blit(note, (cx - note.get_width() // 2, y0 + bh + 20))

    # ── Salting Rack — phase: select_cure ────────────────────────────────────

    def _draw_rack_select_cure(self, player):
        cx = SCREEN_W // 2
        meat_disp = MEAT_DISPLAY_NAMES.get(self._curing_meat_sel, self._curing_meat_sel)
        lbl = self.font.render(f"SELECT CURE — {meat_disp.upper()}", True, _COL_TITLE)
        self.screen.blit(lbl, (cx - lbl.get_width() // 2, 48))

        eligible = MEAT_SOURCES[self._curing_meat_sel]["eligible_cures"]
        self._curing_cure_btns = {}
        bw, bh, gap = 210, 72, 14
        total_w = len(CURE_ORDER) * (bw + gap) - gap
        x0 = cx - total_w // 2
        y0 = 105
        for cure_key in CURE_ORDER:
            ct   = CURE_TYPES[cure_key]
            has  = cure_key in eligible
            sel  = (cure_key == self._curing_cure_sel)
            rect = pygame.Rect(x0, y0, bw, bh)
            bg   = (60, 42, 18) if sel else (_COL_SEL_BG if has else _COL_DIM_BG)
            pygame.draw.rect(self.screen, bg, rect, border_radius=6)
            border = (230, 185, 75) if sel else (_COL_SEL_BOR if has else _COL_DIM_BOR)
            pygame.draw.rect(self.screen, border, rect, 2, border_radius=6)
            col = _COL_TITLE if has else (65, 52, 30)
            lbl2 = self.small.render(ct["label"], True, col)
            self.screen.blit(lbl2, (rect.centerx - lbl2.get_width() // 2, rect.y + 6))
            desc_s = self.small.render(ct["desc"][:36], True,
                                       (140, 115, 65) if has else (50, 42, 22))
            self.screen.blit(desc_s, (rect.centerx - desc_s.get_width() // 2, rect.y + 26))
            day_s = self.small.render(f"{ct['age_days']} real days to age", True,
                                      (120, 100, 52) if has else (45, 38, 18))
            self.screen.blit(day_s, (rect.centerx - day_s.get_width() // 2, rect.y + 46))
            if has:
                self._curing_cure_btns[cure_key] = rect
            x0 += bw + gap

        if self._curing_cure_sel:
            next_btn = pygame.Rect(cx - 100, y0 + bh + 24, 200, 36)
            pygame.draw.rect(self.screen, _COL_SEL_BG, next_btn, border_radius=5)
            pygame.draw.rect(self.screen, _COL_SEL_BOR, next_btn, 2, border_radius=5)
            nxt = self.small.render("CONFIRM →", True, _COL_TITLE)
            self.screen.blit(nxt, (next_btn.centerx - nxt.get_width() // 2,
                                   next_btn.centery - nxt.get_height() // 2))
            self._curing_cure_confirm_btn = next_btn
        else:
            self._curing_cure_confirm_btn = None

        back = self.small.render("← Back", True, _COL_SUBTITLE)
        self.screen.blit(back, (20, SCREEN_H - back.get_height() - 10))
        self._curing_back_btn = pygame.Rect(14, SCREEN_H - back.get_height() - 14,
                                            back.get_width() + 12, back.get_height() + 8)

    # ── Salting Rack — phase: select_method ──────────────────────────────────

    def _draw_rack_select_method(self, player):
        cx = SCREEN_W // 2
        cure_label = CURE_TYPES[self._curing_cure_sel]["label"]
        lbl = self.font.render(f"SELECT CURE METHOD — {cure_label.upper()}", True, _COL_TITLE)
        self.screen.blit(lbl, (cx - lbl.get_width() // 2, 48))

        self._curing_method_btns = {}
        bw, bh, gap = 210, 72, 14
        total_w = len(CURE_METHOD_ORDER) * (bw + gap) - gap
        x0 = cx - total_w // 2
        y0 = 105
        for method_key in CURE_METHOD_ORDER:
            cm   = CURE_METHODS[method_key]
            sel  = (method_key == self._curing_method_sel)
            rect = pygame.Rect(x0, y0, bw, bh)
            bg   = (60, 42, 18) if sel else _COL_SEL_BG
            pygame.draw.rect(self.screen, bg, rect, border_radius=6)
            border = (230, 185, 75) if sel else _COL_BORDER
            pygame.draw.rect(self.screen, border, rect, 2, border_radius=6)
            lbl2 = self.small.render(cm["label"], True, _COL_TITLE)
            self.screen.blit(lbl2, (rect.centerx - lbl2.get_width() // 2, rect.y + 6))
            desc_s = self.small.render(cm["desc"][:36], True, _COL_SUBTITLE)
            self.screen.blit(desc_s, (rect.centerx - desc_s.get_width() // 2, rect.y + 26))
            sp = cm["salt_penetration"]
            si = cm["spice_intensity"]
            stat_s = self.small.render(
                f"Salt {'↑' if sp > 0 else '↓'}  Spice {'↑' if si > 0 else '↓'}",
                True, (150, 130, 70))
            self.screen.blit(stat_s, (rect.centerx - stat_s.get_width() // 2, rect.y + 46))
            self._curing_method_btns[method_key] = rect
            x0 += bw + gap

        if self._curing_method_sel:
            start_btn = pygame.Rect(cx - 100, y0 + bh + 24, 200, 36)
            pygame.draw.rect(self.screen, _COL_SEL_BG, start_btn, border_radius=5)
            pygame.draw.rect(self.screen, _COL_SEL_BOR, start_btn, 2, border_radius=5)
            s = self.small.render("START CURING →", True, _COL_TITLE)
            self.screen.blit(s, (start_btn.centerx - s.get_width() // 2,
                                  start_btn.centery - s.get_height() // 2))
            self._curing_method_start_btn = start_btn
        else:
            self._curing_method_start_btn = None

        back = self.small.render("← Back", True, _COL_SUBTITLE)
        self.screen.blit(back, (20, SCREEN_H - back.get_height() - 10))
        self._curing_back_btn = pygame.Rect(14, SCREEN_H - back.get_height() - 14,
                                            back.get_width() + 12, back.get_height() + 8)

    # ── Salting Rack — phase: massaging ──────────────────────────────────────

    def _draw_rack_massage(self, player, dt):
        cx = SCREEN_W // 2

        # Advance held zone
        if self._curing_zone_held is not None:
            zi = self._curing_zone_held
            if self._curing_zone_prog[zi] < 1.0:
                self._curing_zone_prog[zi] = min(1.0, self._curing_zone_prog[zi] + _ZONE_FILL_RATE * dt)

        # Check completion
        if all(p >= 1.0 for p in self._curing_zone_prog):
            self._finish_massage(player)
            return

        lbl = self.font.render("WORK IN THE CURE", True, _COL_TITLE)
        self.screen.blit(lbl, (cx - lbl.get_width() // 2, 48))
        sub = self.small.render("Hold the mouse button over each zone to massage in the cure.",
                                True, _COL_SUBTITLE)
        self.screen.blit(sub, (cx - sub.get_width() // 2, 74))

        zone_labels = ["Shoulder", "Belly", "Leg", "Rump"]
        zw, zh, zgap = 160, 110, 18
        total_w = 4 * zw + 3 * zgap
        x0 = cx - total_w // 2
        y0 = 115
        self._curing_zone_rects = []
        for i, label in enumerate(zone_labels):
            prog  = self._curing_zone_prog[i]
            done  = prog >= 1.0
            held  = (self._curing_zone_held == i)
            rect  = pygame.Rect(x0 + i * (zw + zgap), y0, zw, zh)
            self._curing_zone_rects.append(rect)

            bg = (35, 55, 28) if done else ((52, 40, 14) if held else (28, 20, 10))
            pygame.draw.rect(self.screen, bg, rect, border_radius=8)
            border = _COL_ZONE_DONE if done else (_COL_ZONE_ACTIVE if held else _COL_BORDER)
            pygame.draw.rect(self.screen, border, rect, 2, border_radius=8)

            name_s = self.small.render(label, True, _COL_TITLE)
            self.screen.blit(name_s, (rect.centerx - name_s.get_width() // 2, rect.y + 10))

            # Progress bar
            bar_rect = pygame.Rect(rect.x + 12, rect.y + 40, rect.w - 24, 18)
            pygame.draw.rect(self.screen, _COL_BAR_BG, bar_rect, border_radius=4)
            fill_w = int((rect.w - 24) * prog)
            if fill_w > 0:
                fill_col = _COL_ZONE_DONE if done else _COL_ZONE_ACTIVE
                pygame.draw.rect(self.screen, fill_col,
                                 pygame.Rect(bar_rect.x, bar_rect.y, fill_w, 18), border_radius=4)
            pygame.draw.rect(self.screen, _COL_BORDER, bar_rect, 1, border_radius=4)

            pct_s = self.small.render(f"{int(prog * 100)}%", True, _COL_SUBTITLE)
            self.screen.blit(pct_s, (rect.centerx - pct_s.get_width() // 2, rect.y + 66))

            if done:
                done_s = self.small.render("✓ Done", True, _COL_ZONE_DONE)
                self.screen.blit(done_s, (rect.centerx - done_s.get_width() // 2, rect.y + 86))

        remaining = sum(1 for p in self._curing_zone_prog if p < 1.0)
        prog_hint = self.small.render(f"{4 - remaining} / 4 zones complete", True, _COL_SUBTITLE)
        self.screen.blit(prog_hint, (cx - prog_hint.get_width() // 2, y0 + zh + 18))

    def _finish_massage(self, player):
        """All zones filled — consume resources, create CuredMeat, enter result."""
        item = self._curing_wip
        if item is None:
            return
        apply_cure_method(item, self._curing_method_sel)
        player.charcuterie_items.append(item)
        player.inventory[self._curing_meat_sel] = max(
            0, player.inventory.get(self._curing_meat_sel, 0) - 1)
        _consume_salt(player)
        self._curing_rack_phase = "result"

    # ── Salting Rack — phase: result ─────────────────────────────────────────

    def _draw_rack_result(self, player):
        cx = SCREEN_W // 2
        item = player.charcuterie_items[-1] if player.charcuterie_items else None

        lbl = self.font.render("MEAT SALTED", True, _COL_ZONE_DONE)
        self.screen.blit(lbl, (cx - lbl.get_width() // 2, 48))

        if item:
            cure_label = CURE_TYPES[item.cure_type]["label"]
            meat_label = MEAT_DISPLAY_NAMES.get(item.meat_source, item.meat_source)
            method_label = CURE_METHODS[item.cure_method]["label"] if item.cure_method else ""
            info_lines = [
                f"{meat_label}  →  {cure_label}",
                f"Cure method: {method_label}",
                f"Salt penetration: {item.salt_penetration:.2f}   Spice: {item.spice_intensity:.2f}",
                f"Will age for {CURE_TYPES[item.cure_type]['age_days']} real days in the Curing Cellar.",
            ]
            y = 90
            for line in info_lines:
                s = self.small.render(line, True, _COL_SUBTITLE)
                self.screen.blit(s, (cx - s.get_width() // 2, y))
                y += 22

        close_btn = pygame.Rect(cx - 90, SCREEN_H // 2 + 60, 180, 36)
        pygame.draw.rect(self.screen, _COL_SEL_BG, close_btn, border_radius=5)
        pygame.draw.rect(self.screen, _COL_SEL_BOR, close_btn, 2, border_radius=5)
        close_s = self.small.render("Place in Curing Cellar →", True, _COL_TITLE)
        self.screen.blit(close_s, (close_btn.centerx - close_s.get_width() // 2,
                                    close_btn.centery - close_s.get_height() // 2))
        self._curing_result_close_btn = close_btn

    # ── Curing Cellar — phase: select ────────────────────────────────────────

    def _draw_cellar_select(self, player):
        cx = SCREEN_W // 2
        lbl = self.font.render("CURING CELLAR", True, (160, 120, 75))
        self.screen.blit(lbl, (cx - lbl.get_width() // 2, 48))

        items_in_cellar = [c for c in player.charcuterie_items if c.state in ("salted", "aging")]
        if not items_in_cellar:
            empty_s = self.small.render(
                "No salted meats. Use the Salting Rack first, then place them here.",
                True, _COL_SUBTITLE)
            self.screen.blit(empty_s, (cx - empty_s.get_width() // 2, SCREEN_H // 2))
            return

        self._curing_item_btns = []
        bw, bh, gap = 340, 64, 10
        x0 = cx - bw // 2
        y0 = 80
        for item in items_in_cellar:
            rect = pygame.Rect(x0, y0, bw, bh)
            prog = age_progress(item)
            done = prog >= 1.0

            bg = (30, 45, 22) if done else _COL_SEL_BG
            pygame.draw.rect(self.screen, bg, rect, border_radius=6)
            border = _COL_ZONE_DONE if done else _COL_BORDER
            pygame.draw.rect(self.screen, border, rect, 2, border_radius=6)

            cure_l = CURE_TYPES[item.cure_type]["label"]
            meat_l = MEAT_DISPLAY_NAMES.get(item.meat_source, item.meat_source)
            name_s = self.small.render(f"{meat_l} — {cure_l}", True, _COL_TITLE)
            self.screen.blit(name_s, (rect.x + 10, rect.y + 8))

            if item.state == "salted":
                state_s = self.small.render("Not started — click to begin aging",
                                            True, (180, 145, 75))
                self.screen.blit(state_s, (rect.x + 10, rect.y + 30))
            elif done:
                days = CURE_TYPES[item.cure_type]["age_days"]
                ready_s = self.small.render(f"Ready! {days} days complete — click to retrieve",
                                            True, _COL_ZONE_DONE)
                self.screen.blit(ready_s, (rect.x + 10, rect.y + 30))
            else:
                days_total = item.age_total_days
                days_done  = prog * days_total
                elapsed_s  = self.small.render(
                    f"Aging: Day {days_done:.1f} / {days_total}", True, (150, 120, 65))
                self.screen.blit(elapsed_s, (rect.x + 10, rect.y + 30))
                # Progress bar
                bar = pygame.Rect(rect.x + 10, rect.y + 48, rect.w - 20, 8)
                pygame.draw.rect(self.screen, _COL_BAR_BG, bar, border_radius=3)
                fw = int((rect.w - 20) * min(prog, 1.0))
                if fw > 0:
                    pygame.draw.rect(self.screen, _COL_BAR_FILL,
                                     pygame.Rect(bar.x, bar.y, fw, 8), border_radius=3)

            self._curing_item_btns.append((rect, item))
            y0 += bh + gap
            if y0 + bh > SCREEN_H - 20:
                break

    # ── Curing Cellar — phase: aging ─────────────────────────────────────────

    def _draw_cellar_aging(self, player):
        """Show detail view for a selected aging item, with retrieve button if done."""
        cx = SCREEN_W // 2
        items = [c for c in player.charcuterie_items if c.state in ("salted", "aging")]
        if self._curing_cellar_idx is None or self._curing_cellar_idx >= len(items):
            self._curing_cellar_phase = "select"
            return
        item = items[self._curing_cellar_idx]

        prog = age_progress(item)
        done = prog >= 1.0

        title_txt = f"{MEAT_DISPLAY_NAMES.get(item.meat_source, '')} {CURE_TYPES[item.cure_type]['label']}"
        title_s = self.font.render(title_txt.upper(), True, _COL_TITLE)
        self.screen.blit(title_s, (cx - title_s.get_width() // 2, 48))

        lines = [
            f"Cure method: {CURE_METHODS.get(item.cure_method, {}).get('label', '')}",
            f"Salt penetration: {item.salt_penetration:.2f}   Spice intensity: {item.spice_intensity:.2f}",
        ]
        y = 88
        for line in lines:
            s = self.small.render(line, True, _COL_SUBTITLE)
            self.screen.blit(s, (cx - s.get_width() // 2, y))
            y += 20

        # Progress bar
        bar_w = 400
        bar_x = cx - bar_w // 2
        bar_y = y + 20
        pygame.draw.rect(self.screen, _COL_BAR_BG, (bar_x, bar_y, bar_w, 26), border_radius=6)
        fw = int(bar_w * min(prog, 1.0))
        bar_col = _COL_ZONE_DONE if done else _COL_BAR_FILL
        if fw > 0:
            pygame.draw.rect(self.screen, bar_col, (bar_x, bar_y, fw, 26), border_radius=6)
        pygame.draw.rect(self.screen, _COL_BORDER, (bar_x, bar_y, bar_w, 26), 2, border_radius=6)

        days_total = item.age_total_days
        days_done  = min(prog, 1.0) * days_total
        day_s = self.small.render(f"Day {days_done:.1f} / {days_total}", True,
                                  _COL_ZONE_DONE if done else _COL_SUBTITLE)
        self.screen.blit(day_s, (cx - day_s.get_width() // 2, bar_y + 32))

        if done:
            btn_y = bar_y + 68
            retrieve_btn = pygame.Rect(cx - 110, btn_y, 220, 40)
            pygame.draw.rect(self.screen, (30, 50, 22), retrieve_btn, border_radius=6)
            pygame.draw.rect(self.screen, _COL_ZONE_DONE, retrieve_btn, 2, border_radius=6)
            ret_s = self.font.render("RETRIEVE", True, _COL_ZONE_DONE)
            self.screen.blit(ret_s, (retrieve_btn.centerx - ret_s.get_width() // 2,
                                      retrieve_btn.centery - ret_s.get_height() // 2))
            self._curing_retrieve_btn = retrieve_btn
        else:
            self._curing_retrieve_btn = None

        back = self.small.render("← Back", True, _COL_SUBTITLE)
        self.screen.blit(back, (20, SCREEN_H - back.get_height() - 10))
        self._curing_back_btn = pygame.Rect(14, SCREEN_H - back.get_height() - 14,
                                            back.get_width() + 12, back.get_height() + 8)

    # ── Click handlers ────────────────────────────────────────────────────────

    def _handle_salting_rack_click(self, pos, player):
        ph = self._curing_rack_phase

        if ph == "select_meat":
            for meat_key, rect in getattr(self, "_curing_meat_btns", {}).items():
                if rect.collidepoint(pos):
                    self._curing_meat_sel = meat_key
                    self._curing_cure_sel = None
                    self._curing_rack_phase = "select_cure"
                    return

        elif ph == "select_cure":
            if getattr(self, "_curing_back_btn", None) and self._curing_back_btn.collidepoint(pos):
                self._curing_rack_phase = "select_meat"
                return
            for cure_key, rect in getattr(self, "_curing_cure_btns", {}).items():
                if rect.collidepoint(pos):
                    self._curing_cure_sel = cure_key
                    return
            if (self._curing_cure_sel and
                    getattr(self, "_curing_cure_confirm_btn", None) and
                    self._curing_cure_confirm_btn.collidepoint(pos)):
                self._curing_rack_phase = "select_method"
                self._curing_method_sel = None
                return

        elif ph == "select_method":
            if getattr(self, "_curing_back_btn", None) and self._curing_back_btn.collidepoint(pos):
                self._curing_rack_phase = "select_cure"
                return
            for method_key, rect in getattr(self, "_curing_method_btns", {}).items():
                if rect.collidepoint(pos):
                    self._curing_method_sel = method_key
                    return
            if (self._curing_method_sel and
                    getattr(self, "_curing_method_start_btn", None) and
                    self._curing_method_start_btn.collidepoint(pos)):
                # Generate the CuredMeat and enter massaging phase
                self._curing_wip = player._charcuterie_gen.generate(
                    self._curing_meat_sel, self._curing_cure_sel)
                self._curing_zone_prog  = [0.0, 0.0, 0.0, 0.0]
                self._curing_zone_held  = None
                self._curing_rack_phase = "massaging"
                return

        elif ph == "massaging":
            # mousedown — set held zone
            for i, rect in enumerate(getattr(self, "_curing_zone_rects", [])):
                if rect.collidepoint(pos):
                    self._curing_zone_held = i
                    return

        elif ph == "result":
            if (getattr(self, "_curing_result_close_btn", None) and
                    self._curing_result_close_btn.collidepoint(pos)):
                self.refinery_open = False
                return

    def handle_salting_rack_mouseup(self, player):
        """Call on MOUSEBUTTONUP to stop zone filling."""
        self._curing_zone_held = None

    def _handle_curing_cellar_click(self, pos, player):
        ph = self._curing_cellar_phase

        if ph == "select":
            for rect, item in getattr(self, "_curing_item_btns", []):
                if rect.collidepoint(pos):
                    prog = age_progress(item)
                    if item.state == "salted":
                        # Start aging
                        start_aging(item)
                        # Immediately save so timestamp persists
                        self._curing_cellar_phase = "aging"
                        idx = [c for c in player.charcuterie_items
                               if c.state == "aging"].index(item)
                        self._curing_cellar_idx = idx
                    elif prog >= 1.0:
                        # Retrieve
                        output_id = finish_aging(item)
                        player._add_item(output_id)
                        player.discovered_charcuterie.add(
                            f"{item.meat_source}_{item.cure_type}")
                        player.charcuterie_items.remove(item)
                        player.pending_notifications.append(
                            ("Charcuterie", CURE_TYPES[item.cure_type]["label"], None))
                    else:
                        # View detail
                        aging_items = [c for c in player.charcuterie_items if c.state == "aging"]
                        if item in aging_items:
                            self._curing_cellar_idx   = aging_items.index(item)
                            self._curing_cellar_phase = "aging"
                    return

        elif ph == "aging":
            if getattr(self, "_curing_back_btn", None) and self._curing_back_btn.collidepoint(pos):
                self._curing_cellar_phase = "select"
                return
            if (getattr(self, "_curing_retrieve_btn", None) and
                    self._curing_retrieve_btn.collidepoint(pos)):
                aging_items = [c for c in player.charcuterie_items if c.state == "aging"]
                if self._curing_cellar_idx is not None and self._curing_cellar_idx < len(aging_items):
                    item = aging_items[self._curing_cellar_idx]
                    if age_progress(item) >= 1.0:
                        output_id = finish_aging(item)
                        player._add_item(output_id)
                        player.discovered_charcuterie.add(
                            f"{item.meat_source}_{item.cure_type}")
                        player.charcuterie_items.remove(item)
                        player.pending_notifications.append(
                            ("Charcuterie", CURE_TYPES[item.cure_type]["label"], None))
                        self._curing_cellar_phase = "select"
                return

    # ── Per-frame key/mouse handler ───────────────────────────────────────────

    def handle_charcuterie_keys(self, keys, dt, player):
        """Called every frame when salting rack is active — advances held zone."""
        if self._curing_rack_phase == "massaging":
            if not pygame.mouse.get_pressed()[0]:
                self._curing_zone_held = None
            # Zone advancement handled inside _draw_rack_massage via dt

    # ── Codex ─────────────────────────────────────────────────────────────────

    def _draw_charcuterie_codex(self, player, gy0=58, gx_off=0):
        cx = SCREEN_W // 2 + gx_off
        title_s = self.font.render("CHARCUTERIE", True, _COL_TITLE)
        self.screen.blit(title_s, (cx - title_s.get_width() // 2, gy0))

        # Column headers — cure types
        cell_w, cell_h = 110, 46
        gap_x, gap_y   = 6, 6
        col_x_start = cx - (len(CURE_ORDER) * (cell_w + gap_x)) // 2 + 60
        row_y_start = gy0 + 34

        for ci, cure_key in enumerate(CURE_ORDER):
            hdr_s = self.small.render(CURE_TYPES[cure_key]["label"], True, _COL_SUBTITLE)
            hx = col_x_start + ci * (cell_w + gap_x) + cell_w // 2 - hdr_s.get_width() // 2
            self.screen.blit(hdr_s, (hx, row_y_start))

        self._curing_codex_rects = {}
        for ri, meat_key in enumerate(_CODEX_MEATS):
            row_y = row_y_start + 20 + ri * (cell_h + gap_y)
            # Row label
            lbl_s = self.small.render(MEAT_DISPLAY_NAMES[meat_key], True, _COL_SUBTITLE)
            self.screen.blit(lbl_s, (col_x_start - lbl_s.get_width() - 6, row_y + 14))

            eligible = set(MEAT_SOURCES[meat_key]["eligible_cures"])
            for ci, cure_key in enumerate(CURE_ORDER):
                cell_x = col_x_start + ci * (cell_w + gap_x)
                rect   = pygame.Rect(cell_x, row_y, cell_w, cell_h)
                key    = f"{meat_key}_{cure_key}"

                if cure_key not in eligible:
                    pygame.draw.rect(self.screen, (18, 14, 10), rect, border_radius=4)
                    dash_s = self.small.render("—", True, (45, 38, 25))
                    self.screen.blit(dash_s, (rect.centerx - dash_s.get_width() // 2,
                                               rect.centery - dash_s.get_height() // 2))
                    continue

                discovered = key in player.discovered_charcuterie
                if discovered:
                    output_items = [c for c in player.charcuterie_items
                                    if c.meat_source == meat_key and c.cure_type == cure_key
                                    and c.state == "finished"]
                    best_q = max((c.age_quality for c in output_items), default=0.0)
                    stars  = "★" * (3 if best_q >= 0.72 else (2 if best_q >= 0.45 else 1))
                    out_key = get_charcuterie_output_id(cure_key, best_q)
                    col    = OUTPUT_COLORS.get(out_key, _COL_TITLE)
                    bg     = (int(col[0] * 0.18), int(col[1] * 0.18), int(col[2] * 0.18))
                    pygame.draw.rect(self.screen, bg, rect, border_radius=4)
                    pygame.draw.rect(self.screen, col, rect, 2, border_radius=4)
                    cure_s = self.small.render(CURE_TYPES[cure_key]["label"][:10], True, col)
                    self.screen.blit(cure_s, (rect.centerx - cure_s.get_width() // 2, rect.y + 4))
                    star_s = self.small.render(stars, True, (240, 200, 80))
                    self.screen.blit(star_s, (rect.centerx - star_s.get_width() // 2, rect.y + 24))
                else:
                    pygame.draw.rect(self.screen, (28, 22, 14), rect, border_radius=4)
                    pygame.draw.rect(self.screen, (65, 52, 32), rect, 1, border_radius=4)
                    q_s = self.small.render("?", True, (80, 65, 40))
                    self.screen.blit(q_s, (rect.centerx - q_s.get_width() // 2,
                                           rect.centery - q_s.get_height() // 2))

                self._curing_codex_rects[key] = rect

        # Detail panel for selected cell
        sel = getattr(self, "_curing_codex_selected", None)
        if sel and sel in self._curing_codex_rects:
            meat_key, cure_key = sel.rsplit("_", 1)
            dx = col_x_start + len(CURE_ORDER) * (cell_w + gap_x) + 12
            dy = row_y_start + 20
            dw, dh = 220, 180
            pygame.draw.rect(self.screen, (28, 20, 12),
                             pygame.Rect(dx, dy, dw, dh), border_radius=6)
            pygame.draw.rect(self.screen, _COL_BORDER,
                             pygame.Rect(dx, dy, dw, dh), 2, border_radius=6)
            lbl = self.small.render(CURE_TYPES[cure_key]["label"], True, _COL_TITLE)
            self.screen.blit(lbl, (dx + 8, dy + 8))
            meat_lbl = self.small.render(MEAT_DISPLAY_NAMES[meat_key], True, _COL_SUBTITLE)
            self.screen.blit(meat_lbl, (dx + 8, dy + 28))
            buff_key = CURE_TYPE_BUFFS.get(cure_key, "")
            buff_s = self.small.render(BUFF_DESCS.get(buff_key, ""), True, (160, 200, 140))
            self.screen.blit(buff_s, (dx + 8, dy + 52))
            days_s = self.small.render(f"Ages {CURE_TYPES[cure_key]['age_days']} real days",
                                       True, _COL_SUBTITLE)
            self.screen.blit(days_s, (dx + 8, dy + 74))

            if sel in player.discovered_charcuterie:
                finished = [c for c in player.charcuterie_items
                            if c.meat_source == meat_key and c.cure_type == cure_key
                            and c.state == "finished"]
                if finished:
                    best = max(finished, key=lambda c: c.age_quality)
                    q_s = self.small.render(f"Best quality: {best.age_quality:.2f}", True, _COL_TITLE)
                    self.screen.blit(q_s, (dx + 8, dy + 98))
                    fy = dy + 120
                    for note in best.flavor_notes[:3]:
                        n_s = self.small.render(f"• {note}", True, (150, 130, 80))
                        self.screen.blit(n_s, (dx + 8, fy))
                        fy += 18
