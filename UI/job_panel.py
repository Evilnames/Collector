"""
UI/job_panel.py — Job assignment panel for hired settlers.

Opens over the hire panel when the player clicks "Assign Job".
Lets the player choose a job type and configure its parameters.
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

_PW = 480
_PH = 320

_JOBS_ROW1 = [
    ("farming", "Farming"),
    ("mining",  "Mining"),
    ("hauling", "Hauling"),
    ("taming",  "Taming"),
]
_JOBS_ROW2 = [
    ("logging", "Logging"),
    ("cooking", "Cooking"),
    (None,      "Unassign"),
]
_JOBS = _JOBS_ROW1 + _JOBS_ROW2

_JOB_DESCS = {
    "farming": "Harvests mature crops in the city region each dawn.",
    "mining":  "Mines blocks around a Mining Post placed in the city.",
    "hauling": "Moves items from a source chest to a destination chest.",
    "taming":  "Tends animals in the city region and collects milk/eggs.",
    "logging": "Fells trees in the city region and deposits lumber.",
    "cooking": "Cooks raw meat and eggs from a supply chest into meals.",
    None:      "NPC wanders the city without producing anything.",
}

_MINING_TARGETS = [("all", "All"), ("ores", "Ores"), ("stone", "Stone")]


class JobPanelMixin:

    def open_job_panel(self, record, city):
        self.job_panel_open    = True
        self.active_job_record = record
        self.active_job_city   = city
        # Working copies — committed on Confirm
        self._jp_job_type  = record.get("job")
        cfg = record.get("job_config") or {}
        self._jp_radius    = cfg.get("radius", 3)
        self._jp_target    = cfg.get("target", "all")
        self._jp_depth     = cfg.get("depth_limit", 20)
        # Hauling uses src_bx/dst_bx; Cooking uses supply_bx/output_bx — both map to src/dst fields
        self._jp_src_bx    = cfg.get("src_bx", cfg.get("supply_bx", ""))
        self._jp_src_by    = cfg.get("src_by", cfg.get("supply_by", ""))
        self._jp_dst_bx    = cfg.get("dst_bx", cfg.get("output_bx", ""))
        self._jp_dst_by    = cfg.get("dst_by", cfg.get("output_by", ""))
        self._jp_active_field = None  # which text field has focus
        self._jp_job_btns  = {}
        self._jp_confirm   = None
        self._jp_cancel    = None

    def close_job_panel(self):
        self.job_panel_open    = False
        self.active_job_record = None
        self.active_job_city   = None
        self._jp_active_field  = None

    def _draw_job_panel(self):
        rec = self.active_job_record
        if rec is None:
            return

        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        px = (SCREEN_W - _PW) // 2
        py = (SCREEN_H - _PH) // 2

        pygame.draw.rect(self.screen, _BG,    (px, py, _PW, _PH))
        pygame.draw.rect(self.screen, _BORDER,(px, py, _PW, _PH), 2)

        # Reset per-frame click rects
        self._jp_radius_btns = {}
        self._jp_target_btns = {}
        self._jp_haul_fields  = {}

        # Header
        self.screen.blit(self.small.render("ASSIGN JOB", True, _DIM_C), (px + 16, py + 10))
        self.screen.blit(self.font.render(rec["name"], True, _TITLE_C),  (px + 16, py + 26))

        sep_y = py + 52
        pygame.draw.line(self.screen, _BORDER, (px + 10, sep_y), (px + _PW - 10, sep_y))
        y = sep_y + 10

        # Job type buttons — two rows
        self._jp_job_btns = {}
        btn_h = 22
        gap = 4
        area_w = _PW - 40

        def _draw_job_row(row, row_y):
            bw = (area_w - gap * (len(row) - 1)) // len(row)
            bx_s = px + 20
            for job_key, job_label in row:
                selected = (self._jp_job_type == job_key)
                bg = (50, 100, 55) if selected else (35, 33, 28)
                border_c = _GREEN if selected else _BORDER
                btn_r = pygame.Rect(bx_s, row_y, bw, btn_h)
                pygame.draw.rect(self.screen, bg, btn_r)
                pygame.draw.rect(self.screen, border_c, btn_r, 1)
                lbl = self.small.render(job_label, True, (_TITLE_C if selected else _LABEL_C))
                self.screen.blit(lbl, btn_r.move((bw - lbl.get_width()) // 2,
                                                  (btn_h - lbl.get_height()) // 2))
                self._jp_job_btns[job_key] = btn_r
                bx_s += bw + gap

        _draw_job_row(_JOBS_ROW1, y)
        _draw_job_row(_JOBS_ROW2, y + btn_h + gap)
        y += btn_h * 2 + gap + 10

        # Description
        desc = _JOB_DESCS.get(self._jp_job_type, "")
        self.screen.blit(self.small.render(desc, True, _DIM_C), (px + 20, y))
        y += 20

        pygame.draw.line(self.screen, _BORDER, (px + 10, y), (px + _PW - 10, y))
        y += 10

        # Config section
        if self._jp_job_type == "mining":
            y = self._draw_mining_config(px, y)
        elif self._jp_job_type in ("hauling", "cooking"):
            y = self._draw_chest_pair_config(px, y)
        else:
            self.screen.blit(
                self.small.render("No configuration required.", True, _DIM_C),
                (px + 20, y))
            y += 20

        # Confirm / Cancel buttons
        btn_y = py + _PH - 38
        cw = 120
        cancel_r  = pygame.Rect(px + 20, btn_y, cw, 26)
        confirm_r = pygame.Rect(px + _PW - 20 - cw, btn_y, cw, 26)

        pygame.draw.rect(self.screen, (60, 38, 32), cancel_r)
        pygame.draw.rect(self.screen, _RED, cancel_r, 1)
        ls = self.small.render("Cancel", True, (240, 200, 195))
        self.screen.blit(ls, cancel_r.move((cw - ls.get_width()) // 2,
                                            (26 - ls.get_height()) // 2))

        pygame.draw.rect(self.screen, (40, 90, 48), confirm_r)
        pygame.draw.rect(self.screen, _GREEN, confirm_r, 1)
        ls = self.small.render("Confirm", True, (200, 240, 200))
        self.screen.blit(ls, confirm_r.move((cw - ls.get_width()) // 2,
                                             (26 - ls.get_height()) // 2))

        self._jp_confirm = confirm_r
        self._jp_cancel  = cancel_r

    # ── Config sub-draws ──────────────────────────────────────────────────────

    def _draw_mining_config(self, px, y):
        # Radius row
        self.screen.blit(self.small.render("Radius:", True, _LABEL_C), (px + 20, y))
        self._jp_radius_btns = {}
        rx = px + 110
        for r in range(1, 6):
            sel = (self._jp_radius == r)
            br = pygame.Rect(rx, y - 1, 28, 18)
            pygame.draw.rect(self.screen, (50, 100, 55) if sel else (35, 33, 28), br)
            pygame.draw.rect(self.screen, (_GREEN if sel else _BORDER), br, 1)
            ls = self.small.render(str(r), True, (_TITLE_C if sel else _DIM_C))
            self.screen.blit(ls, br.move((28 - ls.get_width()) // 2, (18 - ls.get_height()) // 2))
            self._jp_radius_btns[r] = br
            rx += 32
        y += 22

        # Target row
        self.screen.blit(self.small.render("Target:", True, _LABEL_C), (px + 20, y))
        self._jp_target_btns = {}
        tx = px + 110
        for t_key, t_label in _MINING_TARGETS:
            sel = (self._jp_target == t_key)
            tw = 58
            tr = pygame.Rect(tx, y - 1, tw, 18)
            pygame.draw.rect(self.screen, (50, 100, 55) if sel else (35, 33, 28), tr)
            pygame.draw.rect(self.screen, (_GREEN if sel else _BORDER), tr, 1)
            ls = self.small.render(t_label, True, (_TITLE_C if sel else _DIM_C))
            self.screen.blit(ls, tr.move((tw - ls.get_width()) // 2, (18 - ls.get_height()) // 2))
            self._jp_target_btns[t_key] = tr
            tx += tw + 4
        y += 22

        self.screen.blit(
            self.small.render("Place a Mining Post block near ores to assign the work zone.",
                              True, _DIM_C),
            (px + 20, y))
        y += 18
        return y

    def _draw_chest_pair_config(self, px, y):
        self._jp_haul_fields = {}
        cooking = (self._jp_job_type == "cooking")
        lbl_a = "Supply chest:" if cooking else "Source chest:"
        lbl_b = "Output chest:" if cooking else "Dest chest:"

        def field_row(label, field_key_bx, field_key_by, val_bx, val_by):
            nonlocal y
            self.screen.blit(self.small.render(label, True, _LABEL_C), (px + 20, y))
            for fk, fval, fx in [(field_key_bx, val_bx, px + 130),
                                  (field_key_by, val_by, px + 230)]:
                active = (self._jp_active_field == fk)
                fr = pygame.Rect(fx, y - 2, 76, 18)
                pygame.draw.rect(self.screen, (28, 26, 22), fr)
                pygame.draw.rect(self.screen, (_YELLOW if active else _BORDER), fr, 1)
                txt = str(fval) + ("|" if active else "")
                ls = self.small.render(txt, True, _LABEL_C)
                self.screen.blit(ls, (fx + 4, y))
                self._jp_haul_fields[fk] = fr
            y += 22

        field_row(lbl_a, "src_bx", "src_by", self._jp_src_bx, self._jp_src_by)
        field_row(lbl_b, "dst_bx", "dst_by", self._jp_dst_bx, self._jp_dst_by)
        self.screen.blit(
            self.small.render("Enter block coordinates (bx, by) of each chest.",
                              True, _DIM_C),
            (px + 20, y))
        y += 18
        return y

    # ── Click handling ────────────────────────────────────────────────────────

    def handle_job_panel_click(self, pos, player):
        if not self.job_panel_open:
            return False

        # Cancel
        if self._jp_cancel and self._jp_cancel.collidepoint(pos):
            self.close_job_panel()
            return True

        # Confirm
        if self._jp_confirm and self._jp_confirm.collidepoint(pos):
            self._jp_commit(player)
            return True

        # Job type buttons
        for job_key, btn_r in getattr(self, "_jp_job_btns", {}).items():
            if btn_r.collidepoint(pos):
                self._jp_job_type = job_key
                return True

        # Mining radius
        for r, btn_r in getattr(self, "_jp_radius_btns", {}).items():
            if btn_r.collidepoint(pos):
                self._jp_radius = r
                return True

        # Mining target
        for t_key, btn_r in getattr(self, "_jp_target_btns", {}).items():
            if btn_r.collidepoint(pos):
                self._jp_target = t_key
                return True

        # Hauling text fields
        for fk, fr in getattr(self, "_jp_haul_fields", {}).items():
            if fr.collidepoint(pos):
                self._jp_active_field = fk
                return True

        # Clicked outside a field — deselect
        self._jp_active_field = None
        return True  # still consumed (panel is open)

    def handle_job_panel_keydown(self, key, unicode_char):
        if not self.job_panel_open or self._jp_active_field is None:
            return
        fk = self._jp_active_field
        cur = str(getattr(self, f"_jp_{fk}", ""))
        if key == pygame.K_BACKSPACE:
            cur = cur[:-1]
        elif key == pygame.K_TAB:
            fields = ["src_bx", "src_by", "dst_bx", "dst_by"]
            idx = fields.index(fk) if fk in fields else -1
            self._jp_active_field = fields[(idx + 1) % len(fields)]
            return
        elif unicode_char and (unicode_char.isdigit() or unicode_char == "-") and len(cur) < 8:
            cur += unicode_char
        setattr(self, f"_jp_{fk}", cur)

    def _jp_commit(self, player):
        rec = self.active_job_record
        if rec is None:
            return

        rec["job"] = self._jp_job_type

        def _int(v):
            try:
                return int(v)
            except (ValueError, TypeError):
                return None

        cfg = {}
        if self._jp_job_type == "mining":
            cfg["radius"]      = self._jp_radius
            cfg["target"]      = self._jp_target
            cfg["depth_limit"] = self._jp_depth
        elif self._jp_job_type == "hauling":
            cfg["src_bx"] = _int(self._jp_src_bx)
            cfg["src_by"] = _int(self._jp_src_by)
            cfg["dst_bx"] = _int(self._jp_dst_bx)
            cfg["dst_by"] = _int(self._jp_dst_by)
        elif self._jp_job_type == "cooking":
            cfg["supply_bx"] = _int(self._jp_src_bx)
            cfg["supply_by"] = _int(self._jp_src_by)
            cfg["output_bx"] = _int(self._jp_dst_bx)
            cfg["output_by"] = _int(self._jp_dst_by)
        rec["job_config"] = cfg

        job_name = dict(_JOBS).get(self._jp_job_type, "Unassigned")
        player.pending_notifications.append(
            ("City", f"{rec['name']} assigned to: {job_name}.", None))
        self.close_job_panel()
