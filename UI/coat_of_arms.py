"""
UI/coat_of_arms.py — Coat of Arms designer panel for player-run cities.

Accessed via the City Block menu → "Design Coat of Arms".
Lets the player pick division, ordinary, charge, and colors, then
saves the result back to the active city's coat_of_arms dict.
"""

import pygame
import heraldry
from constants import SCREEN_W, SCREEN_H

_BG     = (18, 16, 12)
_BORDER = (180, 155, 90)
_GOLD   = (200, 168, 72)
_DIM    = (110, 100, 75)
_LABEL  = (200, 185, 140)
_WHITE  = (230, 225, 215)

_PW = 720
_PH = 540

# ── Palette ─────────────────────────────────────────────────────────────────

_TINCTURES = [
    (175,  38,  38),   # gules
    ( 38,  78, 175),   # azure
    ( 45, 130,  45),   # vert
    ( 55,  55,  55),   # sable
    (120,  45, 150),   # purpure
    (170,  85,  25),   # tenne
    ( 25, 120, 130),   # bleu-celeste
]
_METALS = [
    (205, 170,  45),   # or (gold)
    (210, 210, 210),   # argent (silver)
]
_ALL_COLORS = _TINCTURES + _METALS

# ── Choices lists ────────────────────────────────────────────────────────────

_DIVISIONS = [
    "plain", "per_pale", "per_fess", "quarterly",
    "per_bend", "per_bend_sinister", "gyronny",
    "barry", "paly", "bendy", "checky", "lozengy",
]
_ORDINARIES = [
    "none", "fess", "pale", "chief", "chevron",
    "cross", "saltire", "bend", "bordure", "pile", "pall", "base",
]
_CHARGES = [
    "none",
    "star", "moon", "sun", "tree", "tower", "sword", "fish", "eagle",
    "castle", "crown", "anchor", "fleur", "cross", "lion", "wolf",
    "horse", "bear", "axe", "hammer", "arrow", "rose", "key", "ship",
    "wheat", "bell", "dragon", "griffin", "stag", "boar", "fox",
    "owl", "raven", "serpent", "bull", "dolphin",
    "chalice", "torch", "lantern", "portcullis", "orb",
    "hourglass", "scales", "acorn", "oak_leaf", "thistle",
    "grapes", "eye", "gauntlet", "helmet", "buckler",
    "mill", "candle", "mace", "trident", "scythe",
    "crossbow", "dagger", "lance", "anvil", "plow",
    "quiver", "cannon", "mountain", "waves", "lightning",
    "snowflake", "flame", "cloud", "comet", "gate", "harp",
]

_MOTTOS = heraldry._MOTTOS

_BTN_H   = 22
_SWATCH  = 20


def _btn_rect(x, y, w, h=_BTN_H):
    return pygame.Rect(x, y, w, h)


def _draw_btn(surf, font, rect, label, active, can=True):
    if not can:
        bg = (35, 33, 28)
        fc = _DIM
        border = (55, 50, 40)
    elif active:
        bg = (60, 110, 60)
        fc = (200, 240, 180)
        border = _GOLD
    else:
        bg = (40, 38, 32)
        fc = _LABEL
        border = (80, 72, 55)
    pygame.draw.rect(surf, bg,     rect)
    pygame.draw.rect(surf, border, rect, 1)
    ls = font.render(label, True, fc)
    surf.blit(ls, ls.get_rect(center=rect.center))


class CoatOfArmsDesignerMixin:

    # ── Open / close ──────────────────────────────────────────────────────────

    def open_coat_of_arms_designer(self, city):
        self.coa_designer_open = True
        self._coa_city          = city
        coa = city.coat_of_arms
        self._coa_division  = coa.get("division",  "plain")
        self._coa_ordinary  = coa.get("ordinary",  "none")
        self._coa_charge    = coa.get("charge",    "none")
        self._coa_primary   = tuple(coa.get("primary",   [60,  100, 180]))
        self._coa_secondary = tuple(coa.get("secondary", [200, 168,  72]))
        self._coa_metal     = tuple(coa.get("metal",     [200, 168,  72]))
        self._coa_motto     = coa.get("motto", "Stand Firm")
        self._coa_charge_scroll = 0
        self._coa_rects = {}

    def close_coat_of_arms_designer(self):
        self.coa_designer_open = False
        self._coa_city = None

    def _coa_save(self):
        city = self._coa_city
        if city is None:
            return
        city.coat_of_arms = {
            "primary":   list(self._coa_primary),
            "secondary": list(self._coa_secondary),
            "metal":     list(self._coa_metal),
            "division":  self._coa_division,
            "ordinary":  self._coa_ordinary,
            "charge":    self._coa_charge,
            "motto":     self._coa_motto,
        }
        self.close_coat_of_arms_designer()

    def _build_live_coa(self):
        return heraldry.CoatOfArms(
            primary   = self._coa_primary,
            secondary = self._coa_secondary,
            metal     = self._coa_metal,
            division  = self._coa_division,
            ordinary  = self._coa_ordinary,
            charge    = self._coa_charge,
            motto     = self._coa_motto,
        )

    # ── Draw ──────────────────────────────────────────────────────────────────

    def _draw_coat_of_arms_designer(self):
        rects = {}
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        self.screen.blit(overlay, (0, 0))

        px = (SCREEN_W - _PW) // 2
        py = (SCREEN_H - _PH) // 2

        pygame.draw.rect(self.screen, _BG,     (px, py, _PW, _PH))
        pygame.draw.rect(self.screen, _BORDER, (px, py, _PW, _PH), 2)

        # ── Header ────────────────────────────────────────────────────────────
        hdr = self.font.render("COAT OF ARMS DESIGNER", True, _GOLD)
        self.screen.blit(hdr, (px + (_PW - hdr.get_width()) // 2, py + 10))
        pygame.draw.line(self.screen, _BORDER, (px + 10, py + 34), (px + _PW - 10, py + 34))

        # ── Shield preview (left column) ─────────────────────────────────────
        shield_w, shield_h = 180, 220
        shield_x = px + 20
        shield_y = py + 44
        heraldry.draw(self.screen, shield_x, shield_y, shield_w, shield_h, self._build_live_coa())
        # Motto below shield
        motto_s = self.small.render(f'"{self._coa_motto}"', True, _DIM)
        self.screen.blit(motto_s, (shield_x + (shield_w - motto_s.get_width()) // 2,
                                   shield_y + shield_h + 6))
        # Cycle motto button
        m_btn = pygame.Rect(shield_x, shield_y + shield_h + 22, shield_w, _BTN_H)
        _draw_btn(self.screen, self.small, m_btn, "Cycle Motto", False)
        rects["motto"] = m_btn

        # ── Right column setup ────────────────────────────────────────────────
        rx  = px + 220
        ry  = py + 44
        rcw = _PW - 220 - 16      # right column width

        def section_label(text):
            nonlocal ry
            ls = self.small.render(text, True, _DIM)
            self.screen.blit(ls, (rx, ry))
            ry += 16

        def choice_row(key, choices, current, cols=6, btn_w=None):
            nonlocal ry
            if btn_w is None:
                btn_w = min(70, (rcw - (cols - 1) * 3) // cols)
            x = rx
            for i, ch in enumerate(choices):
                if x + btn_w > px + _PW - 10:
                    x  = rx
                    ry += _BTN_H + 3
                r = pygame.Rect(x, ry, btn_w, _BTN_H)
                label = ch.replace("_", " ") if ch else "none"
                label = label[:8]
                _draw_btn(self.screen, self.small, r, label, ch == current)
                rects[(key, ch)] = r
                x += btn_w + 3
            ry += _BTN_H + 6

        # ── Division ──────────────────────────────────────────────────────────
        section_label("DIVISION  (field pattern)")
        choice_row("division", _DIVISIONS, self._coa_division, cols=6)

        # ── Ordinary ──────────────────────────────────────────────────────────
        section_label("ORDINARY  (geometric band)")
        choice_row("ordinary", _ORDINARIES, self._coa_ordinary, cols=6)

        # ── Charge ────────────────────────────────────────────────────────────
        section_label("CHARGE  (central symbol)")
        charges_per_row = 8
        charge_btn_w = (rcw - (charges_per_row - 1) * 3) // charges_per_row
        visible_rows  = 4
        max_scroll    = max(0, (len(_CHARGES) + charges_per_row - 1) // charges_per_row - visible_rows)
        self._coa_charge_scroll = max(0, min(self._coa_charge_scroll, max_scroll))
        row_start = self._coa_charge_scroll * charges_per_row
        row_end   = row_start + visible_rows * charges_per_row
        visible   = _CHARGES[row_start:row_end]
        x = rx
        for i, ch in enumerate(visible):
            if i > 0 and i % charges_per_row == 0:
                x   = rx
                ry += _BTN_H + 3
            r = pygame.Rect(x, ry, charge_btn_w, _BTN_H)
            label = ch.replace("_", " ")[:8] if ch else "none"
            _draw_btn(self.screen, self.small, r, label, ch == self._coa_charge)
            rects[("charge", ch)] = r
            x += charge_btn_w + 3
        ry += _BTN_H + 2
        # Scroll arrows for charges
        up_r   = pygame.Rect(rx + rcw - 40, ry - _BTN_H * visible_rows - 3 * visible_rows - 18,
                              18, 18)
        down_r = pygame.Rect(rx + rcw - 20, up_r.y, 18, 18)
        _draw_btn(self.screen, self.small, up_r,   "^", False, self._coa_charge_scroll > 0)
        _draw_btn(self.screen, self.small, down_r, "v", False, self._coa_charge_scroll < max_scroll)
        rects["charge_up"]   = up_r
        rects["charge_down"] = down_r
        ry += 6

        # ── Color rows ───────────────────────────────────────────────────────
        def color_row(key, current, label_text):
            nonlocal ry
            ls = self.small.render(label_text, True, _DIM)
            self.screen.blit(ls, (rx, ry + 2))
            sx = rx + 90
            for col in _ALL_COLORS:
                r = pygame.Rect(sx, ry, _SWATCH, _SWATCH)
                pygame.draw.rect(self.screen, col, r)
                if col == current:
                    pygame.draw.rect(self.screen, _WHITE, r, 2)
                else:
                    pygame.draw.rect(self.screen, (30, 28, 22), r, 1)
                rects[(key, col)] = r
                sx += _SWATCH + 3
            ry += _SWATCH + 5

        color_row("primary",   self._coa_primary,   "Primary:")
        color_row("secondary", self._coa_secondary, "Secondary:")
        color_row("metal",     self._coa_metal,     "Charge:")

        # ── Save / Cancel ────────────────────────────────────────────────────
        btn_y = py + _PH - 34
        save_r   = pygame.Rect(px + _PW - 200, btn_y, 88, 26)
        cancel_r = pygame.Rect(px + _PW - 106, btn_y, 88, 26)
        _draw_btn(self.screen, self.small, save_r,   "Save",   False)
        _draw_btn(self.screen, self.small, cancel_r, "Cancel", False)
        rects["save"]   = save_r
        rects["cancel"] = cancel_r

        hint = self.small.render("[ESC] Cancel", True, _DIM)
        self.screen.blit(hint, (px + 12, btn_y + 4))

        self._coa_rects = rects

    # ── Click handler ─────────────────────────────────────────────────────────

    def handle_coa_click(self, pos):
        if not self.coa_designer_open:
            return False
        rects = self._coa_rects
        for key, rect in rects.items():
            if not rect.collidepoint(pos):
                continue
            if key == "save":
                self._coa_save()
                return True
            if key == "cancel":
                self.close_coat_of_arms_designer()
                return True
            if key == "motto":
                import random
                idx  = _MOTTOS.index(self._coa_motto) if self._coa_motto in _MOTTOS else 0
                self._coa_motto = _MOTTOS[(idx + 1) % len(_MOTTOS)]
                return True
            if key == "charge_up":
                self._coa_charge_scroll = max(0, self._coa_charge_scroll - 1)
                return True
            if key == "charge_down":
                self._coa_charge_scroll += 1
                return True
            if isinstance(key, tuple) and len(key) == 2:
                kind, val = key
                if kind == "division":
                    self._coa_division  = val
                elif kind == "ordinary":
                    self._coa_ordinary  = val
                elif kind == "charge":
                    self._coa_charge    = val
                elif kind == "primary":
                    self._coa_primary   = val
                elif kind == "secondary":
                    self._coa_secondary = val
                elif kind == "metal":
                    self._coa_metal     = val
                return True
        return False

    # ── Scroll ────────────────────────────────────────────────────────────────

    def handle_coa_scroll(self, dy):
        if not self.coa_designer_open:
            return False
        self._coa_charge_scroll = max(0, self._coa_charge_scroll - dy)
        return True
