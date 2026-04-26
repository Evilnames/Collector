"""
UI/outpost_menu.py — OutpostMenuMixin for the outpost flag interaction panel.
Diplomatic-only: shows the outpost's kingdom (region), coat of arms, and the
trade niche. Trade itself happens through the keeper NPC, not the flag.
"""

import pygame
from constants import SCREEN_W, SCREEN_H

import heraldry
from .panels import _wrap_text

_BG       = (24, 22, 18)
_BORDER   = (160, 130, 80)
_TITLE_C  = (240, 220, 160)
_LABEL_C  = (200, 185, 140)
_DIM_C    = (110, 100, 75)
_WHITE    = (240, 240, 230)

# Info card
_PW = 460
_PH = 360

# Coat-of-arms card (right of info card)
_COA_GAP = 12
_COA_CW  = 200
_COA_CH  = _PH
_SHIELD_W = 160
_SHIELD_H = 200


class OutpostMenuMixin:

    def open_outpost_menu(self, outpost):
        self.outpost_menu_open = True
        self.active_outpost    = outpost

    def close_outpost_menu(self):
        self.outpost_menu_open = False
        self.active_outpost    = None

    def _draw_outpost_menu(self, player):
        from outposts import OUTPOST_TYPES, region_for_outpost

        op = self.active_outpost
        if op is None:
            return

        cfg    = OUTPOST_TYPES.get(op.outpost_type, {})
        region = region_for_outpost(op)

        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        total_w = _PW + _COA_GAP + _COA_CW
        px = (SCREEN_W - total_w) // 2
        py = (SCREEN_H - _PH) // 2

        # ── Info card ──────────────────────────────────────────────────────
        pygame.draw.rect(self.screen, _BG,     (px, py, _PW, _PH))
        pygame.draw.rect(self.screen, _BORDER, (px, py, _PW, _PH), 2)

        type_label   = cfg.get("display_name", op.outpost_type.replace("_", " ").title())
        region_name  = region.name if region else "Unaligned Frontier"
        biome_label  = op.biome.replace("_", " ").title()

        title = self.font.render(op.name, True, _TITLE_C)
        self.screen.blit(title, (px + 16, py + 14))

        type_s = self.small.render(f"{type_label}  ─  {biome_label}", True, _DIM_C)
        self.screen.blit(type_s, (px + 16, py + 40))

        sep_y = py + 64
        pygame.draw.line(self.screen, _BORDER, (px + 10, sep_y), (px + _PW - 10, sep_y))

        # Allegiance line
        kingdom_lbl = self.small.render("Allegiance", True, _DIM_C)
        self.screen.blit(kingdom_lbl, (px + 16, sep_y + 12))
        kingdom_s = self.font.render(region_name, True, _LABEL_C)
        self.screen.blit(kingdom_s, (px + 16, sep_y + 28))

        # Leader / agenda (if known)
        line_y = sep_y + 60
        if region is not None:
            from towns import TOWNS, agenda_label
            cap_town = TOWNS.get(region.capital_town_id)
            if cap_town is not None and cap_town.leader_name:
                title_s = self.small.render(
                    f"{region.leader_title or 'Lord'}: {cap_town.leader_name}",
                    True, _LABEL_C)
                self.screen.blit(title_s, (px + 16, line_y))
                line_y += 18
            if region.agenda:
                ag_s = self.small.render(
                    f"Agenda: {agenda_label(region.agenda)}", True, (210, 175, 80))
                self.screen.blit(ag_s, (px + 16, line_y))
                line_y += 18
            if region.tagline:
                line_y += 6
                for ln in _wrap_text(region.tagline, self.small, _PW - 32):
                    ts = self.small.render(ln, True, (155, 140, 100))
                    self.screen.blit(ts, (px + 16, line_y))
                    line_y += 14
        else:
            note = self.small.render(
                "This outpost answers to no charted kingdom.", True, _DIM_C)
            self.screen.blit(note, (px + 16, line_y))

        hint = self.small.render(
            "Speak with the keeper to trade.   [E] or [ESC] to close",
            True, _DIM_C)
        self.screen.blit(hint, (px + 16, py + _PH - 24))

        # ── Coat-of-arms card ──────────────────────────────────────────────
        coa_px = px + _PW + _COA_GAP
        self._draw_outpost_coa_card(region, coa_px, py)

    def _draw_outpost_coa_card(self, region, cx, cy):
        pygame.draw.rect(self.screen, _BG,     (cx, cy, _COA_CW, _COA_CH))
        pygame.draw.rect(self.screen, _BORDER, (cx, cy, _COA_CW, _COA_CH), 2)

        lbl = self.small.render("Coat of Arms", True, _DIM_C)
        self.screen.blit(lbl, (cx + (_COA_CW - lbl.get_width()) // 2, cy + 10))

        if region is None or region.coat_of_arms is None:
            msg = self.small.render("Unaligned", True, _DIM_C)
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
                ms = self.small.render(ln, True, (200, 185, 140))
                self.screen.blit(ms, (cx + (_COA_CW - ms.get_width()) // 2, motto_y))
                motto_y += 14
