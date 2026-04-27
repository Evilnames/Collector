"""
UI/city_block_menu.py — Panel for the player's City Block.

Shows city name (editable), population roster, treasury, and basic stats.
Interaction: [E] near a placed City Block opens this panel.
"""

import pygame
from constants import SCREEN_W, SCREEN_H

_BG      = (18, 16, 12)
_BORDER  = (180, 155, 90)
_TITLE_C = (240, 220, 160)
_LABEL_C = (200, 185, 140)
_DIM_C   = (110, 100, 75)
_GREEN   = (120, 200, 100)
_YELLOW  = (230, 200, 80)

_PW = 500
_PH = 420
_NAME_MAX = 28


class CityBlockMenuMixin:

    def open_city_block_menu(self, city):
        self.city_block_menu_open = True
        self.active_city_block    = city
        self._city_name_editing   = False
        self._city_name_draft     = city.name

    def close_city_block_menu(self):
        self.city_block_menu_open = False
        self.active_city_block    = None
        self._city_name_editing   = False
        self._city_name_draft     = ""

    def handle_city_block_keydown(self, key, unicode_char, player):
        if not self._city_name_editing:
            return
        city = self.active_city_block
        if city is None:
            return
        if key == pygame.K_ESCAPE:
            self._city_name_draft   = city.name
            self._city_name_editing = False
        elif key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            draft = self._city_name_draft.strip()
            if draft:
                city.name = draft
            self._city_name_editing = False
        elif key == pygame.K_BACKSPACE:
            self._city_name_draft = self._city_name_draft[:-1]
        elif unicode_char and unicode_char.isprintable() and len(self._city_name_draft) < _NAME_MAX:
            self._city_name_draft += unicode_char

    def _draw_city_block_menu(self, player):
        city = self.active_city_block
        if city is None:
            return

        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        px = (SCREEN_W - _PW) // 2
        py = (SCREEN_H - _PH) // 2

        pygame.draw.rect(self.screen, _BG,    (px, py, _PW, _PH))
        pygame.draw.rect(self.screen, _BORDER,(px, py, _PW, _PH), 2)

        # ── Header ────────────────────────────────────────────────────────────
        header_s = self.small.render("CITY BLOCK", True, _DIM_C)
        self.screen.blit(header_s, (px + 16, py + 10))

        name_display = self._city_name_draft if self._city_name_editing else city.name
        if self._city_name_editing:
            name_display += "|"
        name_s = self.font.render(name_display, True, _TITLE_C)
        self.screen.blit(name_s, (px + 16, py + 28))

        if not self._city_name_editing:
            edit_hint = self.small.render("[click name to rename]", True, _DIM_C)
            self.screen.blit(edit_hint, (px + 16 + name_s.get_width() + 8, py + 32))

        self._city_name_rect = pygame.Rect(px + 16, py + 28,
                                           name_s.get_width() + 120, name_s.get_height() + 4)

        sep_y = py + 58
        pygame.draw.line(self.screen, _BORDER, (px + 10, sep_y), (px + _PW - 10, sep_y))

        # ── Summary stats ─────────────────────────────────────────────────────
        y = sep_y + 12

        def row(label, value, color=_LABEL_C):
            nonlocal y
            lbl_s = self.small.render(label, True, _DIM_C)
            val_s = self.small.render(value, True, color)
            self.screen.blit(lbl_s, (px + 20, y))
            self.screen.blit(val_s, (px + 200, y))
            y += 20

        row("City Center",  f"({city.bx}, {city.by})")
        row("City Region",  f"x {city.bx - 80} – {city.bx + 80}  (±80 tiles)")
        row("Population",   str(city.population),
            _YELLOW if city.population > 0 else _DIM_C)
        row("Treasury",     f"{city.treasury} coins",
            _GREEN if city.treasury > 0 else _DIM_C)

        y += 4
        pygame.draw.line(self.screen, _BORDER, (px + 10, y), (px + _PW - 10, y))
        y += 10

        # ── Settler roster ────────────────────────────────────────────────────
        roster_label = self.small.render("SETTLERS", True, _DIM_C)
        self.screen.blit(roster_label, (px + 20, y))
        y += 18

        if not city.npcs:
            none_s = self.small.render(
                "No settlers yet.  Place beds within the city region to attract travelers.",
                True, _DIM_C)
            self.screen.blit(none_s, (px + 20, y))
            y += 18
        else:
            # Column headers
            hdr_name   = self.small.render("Name",   True, _DIM_C)
            hdr_trait  = self.small.render("Trait",  True, _DIM_C)
            hdr_status = self.small.render("Status", True, _DIM_C)
            self.screen.blit(hdr_name,   (px + 20,  y))
            self.screen.blit(hdr_trait,  (px + 175, y))
            self.screen.blit(hdr_status, (px + 385, y))
            y += 16
            pygame.draw.line(self.screen, (60, 55, 42), (px + 14, y), (px + _PW - 14, y))
            y += 4

            for rec in city.npcs[:10]:   # max 10 visible rows
                status = "Hired" if rec.get("hired") else "Seeking work"
                s_color = _GREEN if rec.get("hired") else _YELLOW
                if rec.get("disgruntled"):
                    status = "Disgruntled"
                    s_color = (220, 80, 60)

                n_s = self.small.render(rec.get("name", "???"),  True, _LABEL_C)
                t_s = self.small.render(rec.get("trait", ""),    True, _DIM_C)
                st_s = self.small.render(status,                 True, s_color)
                self.screen.blit(n_s,  (px + 20,  y))
                self.screen.blit(t_s,  (px + 175, y))
                self.screen.blit(st_s, (px + 385, y))
                y += 17

            if len(city.npcs) > 10:
                more_s = self.small.render(f"  … and {len(city.npcs) - 10} more", True, _DIM_C)
                self.screen.blit(more_s, (px + 20, y))
                y += 17

        y += 6
        pygame.draw.line(self.screen, _BORDER, (px + 10, y), (px + _PW - 10, y))
        y += 10

        # ── Hint line ─────────────────────────────────────────────────────────
        hint_parts = [
            "Beds in region attract travelers each dawn.",
            "Food chests improve attraction chance.",
        ]
        for part in hint_parts:
            hs = self.small.render(part, True, _DIM_C)
            self.screen.blit(hs, (px + 20, y))
            y += 15

        close_hint = self.small.render("[E] or [ESC] to close", True, _DIM_C)
        self.screen.blit(close_hint, (px + _PW - close_hint.get_width() - 16, py + _PH - 20))

    def handle_city_block_click(self, pos, player):
        if not self.city_block_menu_open:
            return False
        name_rect = getattr(self, "_city_name_rect", None)
        if name_rect and name_rect.collidepoint(pos):
            self._city_name_editing = True
            self._city_name_draft   = self.active_city_block.name
            return True
        return False
