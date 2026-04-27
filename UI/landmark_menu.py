"""
UI/landmark_menu.py — LandmarkMenuMixin: dedicated landmark info screen.

First E-press near a landmark flag opens this panel (name, tagline, region,
coat of arms, effect status). Second E-press fires the effect.
"""

import pygame
from constants import SCREEN_W, SCREEN_H
import heraldry
from .panels import _wrap_text

_BG      = (20, 18, 14)
_BORDER  = (160, 130, 80)
_TITLE_C = (240, 220, 160)
_LABEL_C = (200, 185, 140)
_DIM_C   = (110, 100, 75)
_GOLD    = (210, 175, 80)
_READY_C = (120, 200, 120)
_WAIT_C  = (180, 140, 80)

_PW = 480
_PH = 380

_COA_GAP = 12
_COA_CW  = 200
_COA_CH  = _PH
_SHIELD_W = 160
_SHIELD_H = 200


class LandmarkMenuMixin:

    def open_landmark_menu(self, region, spec):
        self.landmark_menu_open    = True
        self.active_landmark_region = region
        self.active_landmark_spec   = spec

    def close_landmark_menu(self):
        self.landmark_menu_open     = False
        self.active_landmark_region = None
        self.active_landmark_spec   = None

    def _draw_landmark_menu(self, player):
        from landmarks import preview_effect
        from towns import TOWNS, agenda_label

        region = self.active_landmark_region
        spec   = self.active_landmark_spec
        if region is None or spec is None:
            return

        world     = getattr(player, "world", None)
        day_count = getattr(world, "day_count", 0)

        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        total_w = _PW + _COA_GAP + _COA_CW
        px = (SCREEN_W - total_w) // 2
        py = (SCREEN_H - _PH) // 2

        # ── Info card ──────────────────────────────────────────────────────
        pygame.draw.rect(self.screen, _BG,     (px, py, _PW, _PH))
        pygame.draw.rect(self.screen, _BORDER, (px, py, _PW, _PH), 2)

        lm_name = spec.get("name", "Landmark")
        tagline  = spec.get("tagline", "")
        desc     = spec.get("description", "")

        title_s = self.font.render(lm_name, True, _TITLE_C)
        self.screen.blit(title_s, (px + 16, py + 14))

        if tagline:
            tag_s = self.small.render(f"“{tagline}”", True, _DIM_C)
            self.screen.blit(tag_s, (px + 16, py + 36))

        sep_y = py + 58
        pygame.draw.line(self.screen, _BORDER, (px + 10, sep_y), (px + _PW - 10, sep_y))

        # Region
        line_y = sep_y + 10
        region_s = self.small.render(f"Kingdom: {region.name}", True, _LABEL_C)
        self.screen.blit(region_s, (px + 16, line_y))
        line_y += 16

        cap_town = TOWNS.get(region.capital_town_id)
        if cap_town and cap_town.leader_name:
            leader_s = self.small.render(
                f"{region.leader_title or 'Lord'}: {cap_town.leader_name}", True, _LABEL_C)
            self.screen.blit(leader_s, (px + 16, line_y))
            line_y += 16

        if region.agenda:
            ag_s = self.small.render(
                f"Agenda: {agenda_label(region.agenda)}", True, _GOLD)
            self.screen.blit(ag_s, (px + 16, line_y))
            line_y += 20

        # Description
        if desc:
            pygame.draw.line(self.screen, _BORDER,
                             (px + 10, line_y), (px + _PW - 10, line_y))
            line_y += 10
            for ln in _wrap_text(desc, self.small, _PW - 32):
                ds = self.small.render(ln, True, _LABEL_C)
                self.screen.blit(ds, (px + 16, line_y))
                line_y += 15

        # Status line
        status, ready = preview_effect(region, day_count)
        if status:
            line_y += 6
            pygame.draw.line(self.screen, _BORDER,
                             (px + 10, line_y), (px + _PW - 10, line_y))
            line_y += 10
            color = _READY_C if ready else _WAIT_C
            for ln in _wrap_text(f"Status: {status}", self.small, _PW - 32):
                ss = self.small.render(ln, True, color)
                self.screen.blit(ss, (px + 16, line_y))
                line_y += 15

        # Hint
        hint_text = "[E] Activate landmark   [ESC] Close" if ready else "[ESC] Close"
        hint_s = self.small.render(hint_text, True, _DIM_C)
        self.screen.blit(hint_s, (px + 16, py + _PH - 24))

        # ── Coat-of-arms card ──────────────────────────────────────────────
        coa_px = px + _PW + _COA_GAP
        self._draw_landmark_coa_card(region, coa_px, py)

    def _draw_landmark_coa_card(self, region, cx, cy):
        pygame.draw.rect(self.screen, _BG,     (cx, cy, _COA_CW, _COA_CH))
        pygame.draw.rect(self.screen, _BORDER, (cx, cy, _COA_CW, _COA_CH), 2)

        lbl = self.small.render("Coat of Arms", True, _DIM_C)
        self.screen.blit(lbl, (cx + (_COA_CW - lbl.get_width()) // 2, cy + 10))

        if region is None or region.coat_of_arms is None:
            msg = self.small.render("No arms", True, _DIM_C)
            self.screen.blit(msg, (cx + (_COA_CW - msg.get_width()) // 2,
                                   cy + _COA_CH // 2))
            return

        rname = self.small.render(region.name, True, _TITLE_C)
        self.screen.blit(rname, (cx + (_COA_CW - rname.get_width()) // 2, cy + 26))

        shield_x = cx + (_COA_CW - _SHIELD_W) // 2
        shield_y = cy + 50
        heraldry.draw(self.screen, shield_x, shield_y, _SHIELD_W, _SHIELD_H,
                      region.coat_of_arms)

        coa = region.coat_of_arms
        if coa.motto:
            motto_y = shield_y + _SHIELD_H + 10
            for ln in _wrap_text(f"“{coa.motto}”", self.small, _COA_CW - 16):
                ms = self.small.render(ln, True, _LABEL_C)
                self.screen.blit(ms, (cx + (_COA_CW - ms.get_width()) // 2, motto_y))
                motto_y += 14
