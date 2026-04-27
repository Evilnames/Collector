"""
UI/city_block_menu.py — Panel for the player's City Block.

Shows city name (editable), population roster, treasury balance with
deposit controls, and upkeep status.
"""

import pygame
import heraldry
from player_cities import coa_from_dict
from constants import SCREEN_W, SCREEN_H

_BG      = (18, 16, 12)
_BORDER  = (180, 155, 90)
_TITLE_C = (240, 220, 160)
_LABEL_C = (200, 185, 140)
_DIM_C   = (110, 100, 75)
_GREEN   = (120, 200, 100)
_YELLOW  = (230, 200, 80)
_RED     = (220, 80, 60)

_PW = 560
_PH = 480
_NAME_MAX = 28

_DEPOSIT_AMOUNTS = (10, 50, 200)


class CityBlockMenuMixin:

    def open_city_block_menu(self, city):
        self.city_block_menu_open  = True
        self.active_city_block     = city
        self._city_name_editing    = False
        self._city_name_draft      = city.name
        self._city_deposit_btns    = {}
        self._city_design_btn      = None

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

        # ── Header / name ─────────────────────────────────────────────────────
        # Mini shield (40×48) on the right side of the header
        _SHIELD_W, _SHIELD_H = 40, 48
        shield_x = px + _PW - _SHIELD_W - 12
        shield_y = py + 6
        coa_obj = coa_from_dict(city.coat_of_arms)
        heraldry.draw(self.screen, shield_x, shield_y, _SHIELD_W, _SHIELD_H, coa_obj)

        # "Design" button below the mini shield
        design_r = pygame.Rect(shield_x - 14, shield_y + _SHIELD_H + 4, _SHIELD_W + 14, 18)
        pygame.draw.rect(self.screen, (40, 38, 30), design_r)
        pygame.draw.rect(self.screen, _BORDER, design_r, 1)
        ds = self.small.render("Design", True, _TITLE_C)
        self.screen.blit(ds, ds.get_rect(center=design_r.center))
        self._city_design_btn = design_r

        header_s = self.small.render("CITY BLOCK", True, _DIM_C)
        self.screen.blit(header_s, (px + 16, py + 10))

        name_display = self._city_name_draft if self._city_name_editing else city.name
        if self._city_name_editing:
            name_display += "|"
        name_s = self.font.render(name_display, True, _TITLE_C)
        self.screen.blit(name_s, (px + 16, py + 28))
        self._city_name_rect = pygame.Rect(px + 16, py + 28,
                                           name_s.get_width() + 120, name_s.get_height() + 4)
        if not self._city_name_editing:
            hint_s = self.small.render("[click name to rename]", True, _DIM_C)
            self.screen.blit(hint_s, (px + 16 + name_s.get_width() + 8, py + 32))

        sep_y = py + 58
        pygame.draw.line(self.screen, _BORDER, (px + 10, sep_y), (px + _PW - 10, sep_y))

        y = sep_y + 12

        def stat_row(label, value, col=_LABEL_C):
            nonlocal y
            self.screen.blit(self.small.render(label, True, _DIM_C),  (px + 20, y))
            self.screen.blit(self.small.render(value, True, col),      (px + 210, y))
            y += 20

        stat_row("City Center",  f"({city.bx}, {city.by})")
        stat_row("Region",       f"x {city.bx - 80} – {city.bx + 80}  (±80 tiles)")
        stat_row("Population",   str(city.population),
                 _YELLOW if city.population > 0 else _DIM_C)

        # ── Treasury + deposit ────────────────────────────────────────────────
        y += 4
        pygame.draw.line(self.screen, _BORDER, (px + 10, y), (px + _PW - 10, y))
        y += 10

        treas_lbl = self.small.render("TREASURY", True, _DIM_C)
        self.screen.blit(treas_lbl, (px + 20, y))

        treas_col = _GREEN if city.treasury > 0 else _RED
        treas_val = self.font.render(f"{city.treasury} coins", True, treas_col)
        self.screen.blit(treas_val, (px + 110, y - 2))

        wallet_s = self.small.render(f"(your wallet: {player.money})", True, _DIM_C)
        self.screen.blit(wallet_s, (px + 110 + treas_val.get_width() + 10, y + 2))
        y += 26

        # Deposit buttons
        self._city_deposit_btns = {}
        btn_x = px + 20
        for amount in _DEPOSIT_AMOUNTS:
            label  = f"+{amount}"
            can    = player.money >= amount
            bcol   = (40, 100, 50) if can else (40, 40, 38)
            fcol   = (180, 230, 180) if can else _DIM_C
            bw, bh = 68, 22
            btn_r  = pygame.Rect(btn_x, y, bw, bh)
            pygame.draw.rect(self.screen, bcol,   btn_r)
            pygame.draw.rect(self.screen, _BORDER if can else (60, 58, 50), btn_r, 1)
            ls = self.small.render(label, True, fcol)
            self.screen.blit(ls, btn_r.move((bw - ls.get_width()) // 2,
                                             (bh - ls.get_height()) // 2))
            self._city_deposit_btns[amount] = btn_r
            btn_x += bw + 8

        # "Deposit All" button
        all_can   = player.money > 0
        all_bcol  = (40, 100, 50) if all_can else (40, 40, 38)
        all_fcol  = (180, 230, 180) if all_can else _DIM_C
        all_bw    = 90
        all_r     = pygame.Rect(btn_x, y, all_bw, 22)
        pygame.draw.rect(self.screen, all_bcol,  all_r)
        pygame.draw.rect(self.screen, _BORDER if all_can else (60, 58, 50), all_r, 1)
        all_s = self.small.render("All", True, all_fcol)
        self.screen.blit(all_s, all_r.move((all_bw - all_s.get_width()) // 2, 4))
        self._city_deposit_btns["all"] = all_r
        y += 30

        # Daily wage drain hint
        if city.hired_count > 0:
            daily_drain = sum(r.get("wage", 0) for r in city.npcs if r.get("hired"))
            days_left   = city.treasury // daily_drain if daily_drain else 999
            drain_col   = _RED if days_left < 3 else (_YELLOW if days_left < 7 else _DIM_C)
            drain_s = self.small.render(
                f"Daily wage drain: {daily_drain} coins  ({days_left} days remaining)",
                True, drain_col)
            self.screen.blit(drain_s, (px + 20, y))
            y += 18

        # ── Settler roster ────────────────────────────────────────────────────
        y += 4
        pygame.draw.line(self.screen, _BORDER, (px + 10, y), (px + _PW - 10, y))
        y += 10

        self.screen.blit(self.small.render("SETTLERS", True, _DIM_C), (px + 20, y))
        y += 18

        if not city.npcs:
            self.screen.blit(
                self.small.render(
                    "No settlers yet.  Place beds in the city region to attract travelers.",
                    True, _DIM_C),
                (px + 20, y))
            y += 16
        else:
            # Column headers
            for text, col_x in [("Name", px + 20), ("Trait", px + 185),
                                 ("Job / Status", px + 335), ("Wage", px + 460)]:
                self.screen.blit(self.small.render(text, True, _DIM_C), (col_x, y))
            y += 16
            pygame.draw.line(self.screen, (60, 55, 42), (px + 14, y), (px + _PW - 14, y))
            y += 4

            for rec in city.npcs[:9]:
                if rec.get("disgruntled"):
                    status, sc = "Disgruntled", _RED
                elif rec.get("hired"):
                    job = rec.get("job")
                    status = job.capitalize() if job else "Hired (idle)"
                    sc = _GREEN if job else _YELLOW
                elif "decline_days_remaining" in rec:
                    status, sc = "Leaving soon", _RED
                else:
                    status, sc = "Seeking work", _YELLOW

                for text, col_x, fc in [
                    (rec.get("name", "???"),  px + 20,  _LABEL_C),
                    (rec.get("trait", ""),    px + 185, _DIM_C),
                    (status,                  px + 335, sc),
                    (f"{rec.get('wage',0)}c", px + 460, _DIM_C),
                ]:
                    self.screen.blit(self.small.render(text, True, fc), (col_x, y))
                y += 17

            if len(city.npcs) > 9:
                more_s = self.small.render(f"… and {len(city.npcs) - 9} more", True, _DIM_C)
                self.screen.blit(more_s, (px + 20, y))
                y += 17

        # ── Footer ────────────────────────────────────────────────────────────
        hint = self.small.render("[E] or [ESC] to close", True, _DIM_C)
        self.screen.blit(hint, (px + _PW - hint.get_width() - 16, py + _PH - 20))

    def handle_city_block_click(self, pos, player):
        if not self.city_block_menu_open:
            return False

        # Design coat of arms button
        if getattr(self, "_city_design_btn", None) and self._city_design_btn.collidepoint(pos):
            self.open_coat_of_arms_designer(self.active_city_block)
            return True

        # Name field
        if getattr(self, "_city_name_rect", None) and self._city_name_rect.collidepoint(pos):
            self._city_name_editing = True
            self._city_name_draft   = self.active_city_block.name
            return True

        # Deposit buttons
        city = self.active_city_block
        for amount, rect in getattr(self, "_city_deposit_btns", {}).items():
            if rect.collidepoint(pos):
                if amount == "all":
                    city.treasury  += player.money
                    player.money    = 0
                elif player.money >= amount:
                    city.treasury  += amount
                    player.money   -= amount
                return True

        return False
