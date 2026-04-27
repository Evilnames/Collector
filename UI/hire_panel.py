"""
UI/hire_panel.py — Settler interaction panel.

Unhired settler  → hire offer (name, trait, stats, wage, Accept/Decline).
Hired settler    → status view (job, upkeep health, complaint if disgruntled).
"""

import pygame
from constants import SCREEN_W, SCREEN_H

_BG      = (18, 16, 12)
_BORDER  = (150, 120, 70)
_TITLE_C = (240, 220, 160)
_LABEL_C = (200, 185, 140)
_DIM_C   = (110, 100, 75)
_GREEN   = (80, 185, 80)
_YELLOW  = (220, 185, 60)
_RED     = (185, 65, 55)
_BAR_BG  = (45, 42, 35)

_PW = 440
_PH = 400

_STAT_LABELS = [
    ("strength",        "Strength"),
    ("agility",         "Agility"),
    ("craft",           "Craft"),
    ("endurance",       "Endurance"),
    ("intelligence",    "Intelligence"),
    ("animal_affinity", "Animal Affinity"),
]

_FOOD_COMPLAINTS = [
    "I haven't eaten in days. I can't keep working like this.",
    "My stomach is empty. I need food to do my job.",
    "I'm too hungry to work properly. Where's the food?",
]
_WAGE_COMPLAINTS = [
    "I haven't been paid. This isn't what we agreed.",
    "The treasury is empty. I need my wages to stay.",
    "I've been working for free. That ends soon.",
]
_BOTH_COMPLAINTS = [
    "No food AND no pay? I'll be leaving soon.",
    "I'm hungry and broke. I can't stay much longer.",
]


class HirePanelMixin:

    def open_hire_panel(self, settler_npc, city, record):
        self.hire_panel_open    = True
        self.active_hire_npc    = settler_npc
        self.active_hire_city   = city
        self.active_hire_record = record
        self._hire_accept_btn   = None
        self._hire_decline_btn  = None

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

        if rec.get("hired"):
            self._draw_status_view(rec, city)
        else:
            self._draw_hire_offer(rec, city)

    # ── Hire offer ────────────────────────────────────────────────────────────

    def _draw_hire_offer(self, rec, city):
        px, py = self._panel_base()

        self.screen.blit(
            self.small.render(f"Traveler seeking work in {city.name}", True, _DIM_C),
            (px + 16, py + 10))
        self.screen.blit(self.font.render(rec["name"], True, _TITLE_C), (px + 16, py + 28))
        self.screen.blit(
            self.small.render(f'"{rec["trait"]}"', True, (190, 175, 120)),
            (px + 16, py + 50))

        sep_y = py + 70
        pygame.draw.line(self.screen, _BORDER, (px + 10, sep_y), (px + _PW - 10, sep_y))
        y = sep_y + 12

        self._draw_stat_bars(rec, px, y)
        y += 6 * 20 + 6

        pygame.draw.line(self.screen, _BORDER, (px + 10, y), (px + _PW - 10, y))
        y += 10

        self.screen.blit(self.small.render("Daily Wage:", True, _DIM_C), (px + 20, y))
        self.screen.blit(
            self.font.render(f"{rec['wage']} coins / day", True, _TITLE_C),
            (px + 130, y - 2))
        y += 28

        btn_w, btn_h = 140, 30
        gap = 20
        btn_left = px + (_PW - btn_w * 2 - gap) // 2

        acc_r = pygame.Rect(btn_left, y, btn_w, btn_h)
        dec_r = pygame.Rect(btn_left + btn_w + gap, y, btn_w, btn_h)

        pygame.draw.rect(self.screen, (40, 110, 50), acc_r)
        pygame.draw.rect(self.screen, _GREEN, acc_r, 2)
        self._center_text(acc_r, "Accept  (hire)", (200, 240, 200))

        pygame.draw.rect(self.screen, (100, 38, 32), dec_r)
        pygame.draw.rect(self.screen, _RED, dec_r, 2)
        self._center_text(dec_r, "Decline", (240, 200, 195))

        self._hire_accept_btn  = acc_r
        self._hire_decline_btn = dec_r

        self.screen.blit(
            self.small.render("[ESC] to close  •  declined settlers leave after 2 days", True, _DIM_C),
            (px + (_PW - self.small.size("[ESC] to close  •  declined settlers leave after 2 days")[0]) // 2,
             py + _PH - 20))

    # ── Hired status view ─────────────────────────────────────────────────────

    def _draw_status_view(self, rec, city):
        self._hire_accept_btn     = None
        self._hire_decline_btn    = None
        self._hire_assign_job_btn = None

        px, py = self._panel_base()

        self.screen.blit(
            self.small.render(f"Settler of {city.name}", True, _DIM_C),
            (px + 16, py + 10))
        self.screen.blit(self.font.render(rec["name"], True, _TITLE_C), (px + 16, py + 28))
        self.screen.blit(
            self.small.render(f'"{rec["trait"]}"', True, (190, 175, 120)),
            (px + 16, py + 50))

        sep_y = py + 70
        pygame.draw.line(self.screen, _BORDER, (px + 10, sep_y), (px + _PW - 10, sep_y))
        y = sep_y + 12

        # Stat bars (compact)
        self._draw_stat_bars(rec, px, y)
        y += 6 * 20 + 6

        pygame.draw.line(self.screen, _BORDER, (px + 10, y), (px + _PW - 10, y))
        y += 10

        # Upkeep health
        days_unfed  = rec.get("days_unfed", 0)
        days_unpaid = rec.get("days_unpaid", 0)

        def upkeep_row(label, days, threshold_warn=2, threshold_bad=3):
            nonlocal y
            col = _GREEN if days == 0 else (_YELLOW if days < threshold_bad else _RED)
            status = "OK" if days == 0 else f"{days} day{'s' if days != 1 else ''} missed"
            self.screen.blit(self.small.render(label, True, _DIM_C),   (px + 20, y))
            self.screen.blit(self.small.render(status, True, col),     (px + 170, y))
            y += 19

        upkeep_row("Food supply:", days_unfed)
        upkeep_row("Wages paid:", days_unpaid)
        self.screen.blit(
            self.small.render(f"Daily wage: {rec.get('wage', 0)} coins", True, _DIM_C),
            (px + 20, y))
        y += 22

        # Disgruntled complaint
        if rec.get("disgruntled"):
            y += 4
            pygame.draw.line(self.screen, _RED, (px + 10, y), (px + _PW - 10, y))
            y += 8
            import random as _rnd
            rng = _rnd.Random(rec["id"])
            if days_unfed >= 2 and days_unpaid >= 2:
                complaint = rng.choice(_BOTH_COMPLAINTS)
            elif days_unfed >= 2:
                complaint = rng.choice(_FOOD_COMPLAINTS)
            else:
                complaint = rng.choice(_WAGE_COMPLAINTS)

            cw = _PW - 40
            words = complaint.split()
            lines, line = [], ""
            for w in words:
                test = (line + " " + w).strip()
                if self.small.size(test)[0] > cw:
                    lines.append(line)
                    line = w
                else:
                    line = test
            if line:
                lines.append(line)

            self.screen.blit(self.small.render("Complaint:", True, _RED), (px + 20, y))
            y += 16
            for ln in lines:
                self.screen.blit(self.small.render(ln, True, (230, 190, 180)), (px + 28, y))
                y += 14

        # Assign Job button
        job = rec.get("job")
        job_label = f"Job: {job.capitalize()}" if job else "Job: None"
        aj_w, aj_h = 160, 24
        aj_x = px + (_PW - aj_w) // 2
        aj_y = py + _PH - 46
        aj_r = pygame.Rect(aj_x, aj_y, aj_w, aj_h)
        pygame.draw.rect(self.screen, (38, 62, 90), aj_r)
        pygame.draw.rect(self.screen, (80, 140, 200), aj_r, 1)
        ls = self.small.render(f"[Assign Job]  {job_label}", True, (160, 200, 240))
        self.screen.blit(ls, aj_r.move((aj_w - ls.get_width()) // 2,
                                        (aj_h - ls.get_height()) // 2))
        self._hire_assign_job_btn = aj_r

        self.screen.blit(
            self.small.render("[ESC] to close", True, _DIM_C),
            (px + _PW - self.small.size("[ESC] to close")[0] - 16, py + _PH - 20))

    # ── Shared helpers ────────────────────────────────────────────────────────

    def _panel_base(self):
        px = (SCREEN_W - _PW) // 2
        py = (SCREEN_H - _PH) // 2
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        self.screen.blit(overlay, (0, 0))
        pygame.draw.rect(self.screen, _BG,    (px, py, _PW, _PH))
        pygame.draw.rect(self.screen, _BORDER,(px, py, _PW, _PH), 2)
        return px, py

    def _draw_stat_bars(self, rec, px, y):
        stats     = rec.get("stats", {})
        bar_x     = px + 175
        bar_w_max = 160
        bar_h     = 10
        for key, label in _STAT_LABELS:
            val = stats.get(key, 1)
            self.screen.blit(self.small.render(label, True, _LABEL_C), (px + 20, y))
            pygame.draw.rect(self.screen, _BAR_BG, (bar_x, y + 1, bar_w_max, bar_h))
            fill_w = int(bar_w_max * val / 10)
            if fill_w > 0:
                bar_col = (80, 185, 80) if val >= 7 else (200, 175, 60) if val >= 4 else (185, 80, 60)
                pygame.draw.rect(self.screen, bar_col, (bar_x, y + 1, fill_w, bar_h))
            self.screen.blit(self.small.render(str(val), True, _LABEL_C),
                             (bar_x + bar_w_max + 6, y))
            y += 20

    def _center_text(self, rect, text, color):
        s = self.small.render(text, True, color)
        self.screen.blit(s, rect.move((rect.w - s.get_width()) // 2,
                                      (rect.h - s.get_height()) // 2))

    # ── Click handling ────────────────────────────────────────────────────────

    def handle_hire_panel_click(self, pos, player):
        if not self.hire_panel_open:
            return False
        if self._hire_accept_btn and self._hire_accept_btn.collidepoint(pos):
            self._do_hire(player)
            return True
        if self._hire_decline_btn and self._hire_decline_btn.collidepoint(pos):
            self._do_decline(player)
            return True
        if (getattr(self, "_hire_assign_job_btn", None) and
                self._hire_assign_job_btn.collidepoint(pos)):
            self.open_job_panel(self.active_hire_record, self.active_hire_city)
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
        rec = self.active_hire_record
        if rec is None:
            return
        rec["decline_days_remaining"] = 2
        player.pending_notifications.append(
            ("City", f"{rec['name']} was declined and will leave soon.", None))
        self.close_hire_panel()
