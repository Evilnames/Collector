"""
UI/hire_panel.py — Hire panel for SettlerNPC interactions.

Opened when the player presses [E] near an unhired settler.
Shows name, trait, 6 stats with progress bars, daily wage.
Accept → settler becomes hired. Decline → settler leaves after 2 days.
"""

import pygame
from constants import SCREEN_W, SCREEN_H

_BG      = (18, 16, 12)
_BORDER  = (150, 120, 70)
_TITLE_C = (240, 220, 160)
_LABEL_C = (200, 185, 140)
_DIM_C   = (110, 100, 75)
_GREEN   = (80, 185, 80)
_RED     = (185, 65, 55)
_BAR_BG  = (45, 42, 35)

_PW = 440
_PH = 380

_STAT_LABELS = [
    ("strength",        "Strength"),
    ("agility",         "Agility"),
    ("craft",           "Craft"),
    ("endurance",       "Endurance"),
    ("intelligence",    "Intelligence"),
    ("animal_affinity", "Animal Affinity"),
]


class HirePanelMixin:

    def open_hire_panel(self, settler_npc, city, record):
        self.hire_panel_open   = True
        self.active_hire_npc   = settler_npc
        self.active_hire_city  = city
        self.active_hire_record = record
        self._hire_accept_btn  = None
        self._hire_decline_btn = None

    def close_hire_panel(self):
        self.hire_panel_open    = False
        self.active_hire_npc    = None
        self.active_hire_city   = None
        self.active_hire_record = None

    def _draw_hire_panel(self, player):
        rec  = self.active_hire_record
        city = self.active_hire_city
        if rec is None or city is None:
            return

        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        self.screen.blit(overlay, (0, 0))

        px = (SCREEN_W - _PW) // 2
        py = (SCREEN_H - _PH) // 2

        pygame.draw.rect(self.screen, _BG,    (px, py, _PW, _PH))
        pygame.draw.rect(self.screen, _BORDER,(px, py, _PW, _PH), 2)

        # ── Header ────────────────────────────────────────────────────────────
        sub = self.small.render(f"Traveler seeking work in {city.name}", True, _DIM_C)
        self.screen.blit(sub, (px + 16, py + 10))

        name_s = self.font.render(rec["name"], True, _TITLE_C)
        self.screen.blit(name_s, (px + 16, py + 28))

        trait_s = self.small.render(f'"{rec["trait"]}"', True, (190, 175, 120))
        self.screen.blit(trait_s, (px + 16, py + 50))

        sep_y = py + 70
        pygame.draw.line(self.screen, _BORDER, (px + 10, sep_y), (px + _PW - 10, sep_y))

        # ── Stats ─────────────────────────────────────────────────────────────
        y = sep_y + 12
        stats = rec.get("stats", {})
        bar_x     = px + 175
        bar_w_max = 160
        bar_h     = 10

        for key, label in _STAT_LABELS:
            val = stats.get(key, 1)
            lbl_s = self.small.render(label, True, _LABEL_C)
            self.screen.blit(lbl_s, (px + 20, y))

            # Background track
            pygame.draw.rect(self.screen, _BAR_BG, (bar_x, y + 1, bar_w_max, bar_h))
            # Filled bar — colour shifts green→yellow→red by value
            fill_w = int(bar_w_max * val / 10)
            if val >= 7:
                bar_col = (80, 185, 80)
            elif val >= 4:
                bar_col = (200, 175, 60)
            else:
                bar_col = (185, 80, 60)
            if fill_w > 0:
                pygame.draw.rect(self.screen, bar_col, (bar_x, y + 1, fill_w, bar_h))

            val_s = self.small.render(str(val), True, _LABEL_C)
            self.screen.blit(val_s, (bar_x + bar_w_max + 6, y))
            y += 20

        y += 6
        pygame.draw.line(self.screen, _BORDER, (px + 10, y), (px + _PW - 10, y))
        y += 10

        # ── Wage ──────────────────────────────────────────────────────────────
        wage_lbl = self.small.render("Daily Wage:", True, _DIM_C)
        wage_val = self.font.render(f"{rec['wage']} coins / day", True, _TITLE_C)
        self.screen.blit(wage_lbl, (px + 20, y))
        self.screen.blit(wage_val, (px + 130, y - 2))
        y += 26

        # ── Accept / Decline buttons ───────────────────────────────────────────
        btn_w, btn_h = 140, 30
        gap = 20
        total_btn_w = btn_w * 2 + gap
        btn_left = px + (_PW - total_btn_w) // 2

        acc_rect = pygame.Rect(btn_left, y, btn_w, btn_h)
        dec_rect = pygame.Rect(btn_left + btn_w + gap, y, btn_w, btn_h)

        pygame.draw.rect(self.screen, (40, 110, 50), acc_rect)
        pygame.draw.rect(self.screen, _GREEN, acc_rect, 2)
        acc_s = self.small.render("Accept  (hire)", True, (200, 240, 200))
        self.screen.blit(acc_s, acc_rect.move(
            (btn_w - acc_s.get_width()) // 2, (btn_h - acc_s.get_height()) // 2))

        pygame.draw.rect(self.screen, (100, 38, 32), dec_rect)
        pygame.draw.rect(self.screen, _RED, dec_rect, 2)
        dec_s = self.small.render("Decline", True, (240, 200, 195))
        self.screen.blit(dec_s, dec_rect.move(
            (btn_w - dec_s.get_width()) // 2, (btn_h - dec_s.get_height()) // 2))

        self._hire_accept_btn  = acc_rect
        self._hire_decline_btn = dec_rect

        hint = self.small.render("[ESC] to close  •  declined settlers leave after 2 days", True, _DIM_C)
        self.screen.blit(hint, (px + (_PW - hint.get_width()) // 2, py + _PH - 20))

    def handle_hire_panel_click(self, pos, player):
        if not self.hire_panel_open:
            return False

        if self._hire_accept_btn and self._hire_accept_btn.collidepoint(pos):
            self._do_hire(player)
            return True

        if self._hire_decline_btn and self._hire_decline_btn.collidepoint(pos):
            self._do_decline(player)
            return True

        return False

    def _do_hire(self, player):
        rec  = self.active_hire_record
        city = self.active_hire_city
        if rec is None:
            return
        rec["hired"] = True
        if self.active_hire_npc is not None:
            self.active_hire_npc.settler_hired = True
        player.pending_notifications.append(
            ("City", f"{rec['name']} has joined {city.name}!", None))
        self.close_hire_panel()

    def _do_decline(self, player):
        rec  = self.active_hire_record
        city = self.active_hire_city
        if rec is None:
            return
        # tick_city_day decrements this each dawn; at 0 the settler leaves
        rec["decline_days_remaining"] = 2
        player.pending_notifications.append(
            ("City", f"{rec['name']} was declined and will leave soon.", None))
        self.close_hire_panel()
