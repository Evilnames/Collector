"""UI/dynasty_tree.py — DynastyTreeMixin: clickable 500-year family tree.

Drawn on top of the dynasty chronicle when player.dynasty_tree_open is True.
Pan vertically with the scroll wheel; click a person card for their details.
"""

import pygame
from constants import SCREEN_W, SCREEN_H


_BG        = (12, 12, 20)
_BORDER    = (90, 130, 170)
_LINE      = (75, 95, 130)
_LINE_MAIN = (140, 175, 215)
_RULER_BG  = (28, 35, 55)
_RULER_BD  = (130, 170, 210)
_SP_BG     = (32, 28, 40)
_SP_BD     = (135, 110, 165)
_SIB_BG    = (22, 24, 32)
_SIB_BD    = (75, 85, 115)
_TITLE_C   = (220, 200, 130)
_TXT_C     = (210, 200, 175)
_DIM_C     = (130, 125, 105)
_HIGHLIGHT = (240, 220, 130)


class DynastyTreeMixin:

    # ---- state init ------------------------------------------------------

    def _ensure_tree_state(self):
        if not hasattr(self, "_tree_scroll"):        self._tree_scroll        = 0
        if not hasattr(self, "_tree_max_scroll"):    self._tree_max_scroll    = 0
        if not hasattr(self, "_tree_selected"):      self._tree_selected      = None
        if not hasattr(self, "_tree_person_rects"):  self._tree_person_rects  = {}
        if not hasattr(self, "_tree_back_btn"):      self._tree_back_btn      = None
        if not hasattr(self, "_tree_cached_for"):    self._tree_cached_for    = None
        if not hasattr(self, "_tree_cached"):        self._tree_cached        = None

    def open_dynasty_tree(self, npc):
        self._ensure_tree_state()
        self._tree_scroll   = 0
        self._tree_selected = None

    # ---- main draw -------------------------------------------------------

    def _draw_dynasty_tree(self, player, world):
        import npc_dynasty as _dyn
        self._ensure_tree_state()

        npc = getattr(player, "inspecting_npc", None)
        if npc is None:
            return

        chronicle  = getattr(npc, "dynasty_chronicle", None) or {}
        region_id  = getattr(npc, "dynasty_id", None)
        world_seed = getattr(world, "seed", 0)
        family     = (getattr(npc, "dynasty_name", "House ?")).replace("House ", "")

        from towns import TOWNS
        tobj       = TOWNS.get(getattr(npc, "town_id", -1))
        town_names = [tobj.name] if tobj else None

        # Cache the generated tree per region/seed (it's deterministic and not cheap)
        cache_key = (region_id, world_seed)
        if self._tree_cached_for != cache_key:
            self._tree_cached     = _dyn.generate_family_tree(
                region_id, world_seed, chronicle, family, town_names,
                rival_family    = getattr(npc, "dynasty_rival", None),
                rival_region_id = getattr(npc, "dynasty_rival_region_id", None),
                world           = world,
            )
            self._tree_cached_for = cache_key
        tree       = self._tree_cached
        people     = tree["people"]
        ppl_by_id  = {p["id"]: p for p in people}

        # Default selection = current head
        if self._tree_selected is None:
            self._tree_selected = tree["current_head_id"]

        # Layout panel
        PW = min(SCREEN_W - 60, 1200)
        PH = SCREEN_H - 60
        px = (SCREEN_W - PW) // 2
        py = (SCREEN_H - PH) // 2

        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        self.screen.blit(overlay, (0, 0))
        pygame.draw.rect(self.screen, _BG,     (px, py, PW, PH))
        pygame.draw.rect(self.screen, _BORDER, (px, py, PW, PH), 2)

        # Title
        title_s = self.font.render(f"House {family} — Five Centuries", True, _TITLE_C)
        self.screen.blit(title_s, (px + 16, py + 12))

        # Side detail panel
        SIDE_W = 320
        side_x = px + PW - SIDE_W - 10
        side_y = py + 50
        side_h = PH - 60 - 40
        pygame.draw.rect(self.screen, (18, 20, 30), (side_x, side_y, SIDE_W, side_h))
        pygame.draw.rect(self.screen, (60, 80, 110), (side_x, side_y, SIDE_W, side_h), 1)

        # Tree drawing area
        tree_x = px + 14
        tree_y = py + 50
        tree_w = side_x - tree_x - 14
        tree_h = PH - 60 - 40

        # Group by gen
        gens = {}
        for p in people:
            gens.setdefault(p["gen"], []).append(p)
        max_gen = max(gens.keys())

        ROW_H    = 110
        TOP_PAD  = 14
        content_h = TOP_PAD + (max_gen + 1) * ROW_H
        max_scroll = max(0, content_h - tree_h)
        self._tree_max_scroll = max_scroll
        self._tree_scroll     = max(0, min(max_scroll, self._tree_scroll))
        scroll = self._tree_scroll

        # Clip
        prev_clip = self.screen.get_clip()
        self.screen.set_clip(pygame.Rect(tree_x, tree_y, tree_w, tree_h))

        CENTER_X = tree_x + tree_w // 2
        RULER_W, RULER_H = 130, 56
        SIB_W, SIB_H     = 100, 36
        gap_marriage     = 10

        self._tree_person_rects.clear()

        # Draw succession backbone first (so cards sit on top)
        for gen in sorted(gens.keys()):
            ruler = next((p for p in gens[gen] if p["is_ruler"]), None)
            if not ruler:
                continue
            row_y = tree_y + TOP_PAD + gen * ROW_H - scroll
            mid_y = row_y + RULER_H // 2
            if ruler["parent_id"] is not None:
                par_row_y = tree_y + TOP_PAD + (gen - 1) * ROW_H - scroll
                par_mid   = par_row_y + RULER_H // 2
                pygame.draw.line(self.screen, _LINE_MAIN,
                                 (CENTER_X, par_mid + RULER_H // 2),
                                 (CENTER_X, mid_y - RULER_H // 2), 2)

        # Draw each generation row
        for gen in sorted(gens.keys()):
            row_y  = tree_y + TOP_PAD + gen * ROW_H - scroll
            ruler  = next((p for p in gens[gen] if p["is_ruler"]), None)
            spouse = ppl_by_id.get(ruler["spouse_id"]) if ruler else None
            siblings = [p for p in gens[gen]
                        if p is not ruler and p is not spouse and p["parent_id"] is not None]

            # Skip drawing if entirely off-screen (vertical clip optimisation)
            if row_y + RULER_H < tree_y or row_y > tree_y + tree_h:
                # Still need rects? No — clicking off-screen items doesn't matter
                continue

            # Ruler card left of center, spouse right of center
            if ruler:
                rx = CENTER_X - RULER_W - gap_marriage // 2
                self._draw_person_card(rx, row_y, RULER_W, RULER_H, ruler, kind="ruler")
                if spouse:
                    sx = CENTER_X + gap_marriage // 2
                    self._draw_person_card(sx, row_y, RULER_W, RULER_H, spouse, kind="spouse")
                    # Marriage connector
                    pygame.draw.line(self.screen, _SP_BD,
                                     (rx + RULER_W, row_y + RULER_H // 2),
                                     (sx,            row_y + RULER_H // 2), 2)

            # Siblings stacked horizontally to the left
            sib_origin_x = CENTER_X - RULER_W - gap_marriage // 2 - 18
            sib_y = row_y + (RULER_H - SIB_H) // 2
            for i, sib in enumerate(siblings[:3]):  # cap at 3 visible
                sx = sib_origin_x - SIB_W - i * (SIB_W + 8)
                self._draw_person_card(sx, sib_y, SIB_W, SIB_H, sib, kind="sibling")
                # Branch line from CENTER_X (just under parent) over to this sibling's right edge
                pygame.draw.line(self.screen, _LINE,
                                 (sx + SIB_W, sib_y + SIB_H // 2),
                                 (sib_origin_x + 4, sib_y + SIB_H // 2), 1)

        self.screen.set_clip(prev_clip)

        # Side detail
        sel_id = self._tree_selected
        person = ppl_by_id.get(sel_id) or ppl_by_id.get(tree["current_head_id"])
        if person:
            self._draw_tree_side_panel(side_x, side_y, SIDE_W, side_h,
                                       person, ppl_by_id, family)

        # Vertical scrollbar
        if max_scroll > 0:
            sb_x = side_x - 8
            sb_y = tree_y
            sb_h = tree_h
            pygame.draw.rect(self.screen, (25, 28, 38), (sb_x, sb_y, 6, sb_h))
            thumb_h = max(20, int(sb_h * sb_h / content_h))
            thumb_y = sb_y + int(scroll / max_scroll * (sb_h - thumb_h))
            pygame.draw.rect(self.screen, (70, 110, 145), (sb_x, thumb_y, 6, thumb_h))

        # Back button
        BTN_W, BTN_H = 100, 28
        back_rect = pygame.Rect(px + PW - BTN_W - 12, py + PH - BTN_H - 12, BTN_W, BTN_H)
        pygame.draw.rect(self.screen, (30, 40, 55), back_rect)
        pygame.draw.rect(self.screen, _BORDER, back_rect, 1)
        b_s = self.small.render("Back", True, (140, 190, 220))
        self.screen.blit(b_s, b_s.get_rect(center=back_rect.center))
        self._tree_back_btn = back_rect

        hint = self.small.render(
            "Click a person  ·  Mouse wheel to scroll  ·  ESC to close",
            True, _DIM_C)
        self.screen.blit(hint, (px + 16, py + PH - 22))

    # ---- helpers --------------------------------------------------------

    def _house_of(self, person, family):
        """Return the house surname for a person, or None for commoner spouses.

        - Explicit `house` field (married-in spouses, siblings who married out)
        - Children of this dynasty (parent_id set) inherit `family`
        - The founder belongs to `family`
        """
        if person.get("house"):
            return person["house"]
        if person.get("parent_id") is not None:
            return family
        if person.get("is_ruler") and person.get("gen") == 0:
            return family
        return None  # married-in commoner

    # ---- card + side panel ----------------------------------------------

    def _draw_person_card(self, x, y, w, h, person, kind="ruler"):
        if kind == "ruler":
            bg, bd, bw = _RULER_BG, _RULER_BD, 2
        elif kind == "spouse":
            bg, bd, bw = _SP_BG,    _SP_BD,    1
        else:
            bg, bd, bw = _SIB_BG,   _SIB_BD,   1

        if self._tree_selected == person["id"]:
            bd = _HIGHLIGHT
            bw = max(bw, 2)

        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(self.screen, bg, rect)
        pygame.draw.rect(self.screen, bd, rect, bw)

        name_col = _TITLE_C if kind == "ruler" else _TXT_C
        # Show surname when the person came from a different house (married-in
        # spouses, siblings who married out).
        first = person["first"]
        if person.get("house"):
            label = f"{first} {person['house']}"
        else:
            label = first
        # Truncate to fit the card width
        max_chars = max(8, (w - 12) // self.small.size("M")[0])
        if len(label) > max_chars:
            label = label[:max_chars - 1] + "…"
        name_s = self.small.render(label, True, name_col)
        self.screen.blit(name_s, (x + 6, y + 4))

        # Epithet on ruler card if it fits
        if kind == "ruler" and person.get("epithet"):
            ep = person["epithet"]
            if len(ep) > 18:
                ep = ep[:18]
            self.screen.blit(self.small.render(ep, True, (180, 165, 110)),
                              (x + 6, y + 18))

        b = person.get("born")
        d = person.get("died")
        b_s = "?" if b is None else f"{b}"
        d_s = "—"  if d is None else f"{d}"
        date_s = self.small.render(f"{b_s} – {d_s}", True, _DIM_C)
        self.screen.blit(date_s, (x + 6, y + h - 16))

        # Crown glyph for ruler
        if kind == "ruler":
            self.screen.blit(self.small.render("♚", True, (220, 190, 80)),
                              (x + w - 14, y + 2))

        self._tree_person_rects[person["id"]] = rect

    def _draw_tree_side_panel(self, x, y, w, h, person, ppl_by_id, family):
        from UI.panels import _wrap_text

        cy = y + 10
        # Resolve which house a person belongs to. Married-in commoners don't
        # belong to any noble house and shouldn't be falsely labelled.
        own_house = self._house_of(person, family)
        if own_house:
            full = f"{person['first']} of House {own_house}"
        else:
            full = f"{person['first']} (married in)"
        title = self.font.render(full, True, _HIGHLIGHT)
        self.screen.blit(title, (x + 10, cy))
        cy += 28

        if person.get("epithet"):
            ep_s = self.small.render(f'"{person["epithet"]}"', True, (200, 180, 120))
            self.screen.blit(ep_s, (x + 10, cy))
            cy += 18

        # Marriage politics — only meaningful for married-in spouses
        match_kind = person.get("match_kind")
        if person.get("house") and match_kind:
            kind_text = {
                "rival":   ("a marriage across the rival line",          (210, 130, 110)),
                "ally":    ("a match between allied houses",             (160, 210, 160)),
                "foreign": ("a match with a distant kingdom",            (180, 180, 220)),
                "common":  ("a match outside the great houses",          (180, 175, 150)),
            }.get(match_kind)
            if kind_text:
                self.screen.blit(self.small.render(kind_text[0], True, kind_text[1]),
                                 (x + 10, cy))
                cy += 18

        # Years
        b = person.get("born")
        d = person.get("died")
        b_s = "unknown" if b is None else f"y{b}"
        d_s = "still living" if d is None else f"y{d}"
        self.screen.blit(self.small.render(f"Born {b_s}  ·  {d_s}", True, _DIM_C),
                         (x + 10, cy))
        cy += 18

        # Reign
        if person.get("ruled_from") is not None:
            rf = person["ruled_from"]
            rt = person["ruled_to"]
            rt_s = "—" if rt is None else f"y{rt}"
            self.screen.blit(self.small.render(f"Held the seat: y{rf} – {rt_s}", True,
                                                (180, 200, 220)),
                             (x + 10, cy))
            cy += 18

        # Spouse — include their house for cross-dynasty matches
        sp_id = person.get("spouse_id")
        if sp_id is not None:
            sp = ppl_by_id.get(sp_id)
            if sp:
                sp_h = self._house_of(sp, family)
                if sp_h:
                    sp_label = f"Married to {sp['first']} of House {sp_h}"
                else:
                    sp_label = f"Married to {sp['first']}"
                for ln in _wrap_text(sp_label, self.small, w - 20):
                    self.screen.blit(self.small.render(ln, True, (190, 170, 200)),
                                     (x + 10, cy))
                    cy += 15
                cy += 3

        par_id = person.get("parent_id")
        if par_id is not None:
            par = ppl_by_id.get(par_id)
            if par:
                self.screen.blit(self.small.render(f"Child of {par['first']}",
                                                    True, _DIM_C),
                                 (x + 10, cy))
                cy += 18

        cy += 6

        # Death cause
        if person.get("death_cause") and d is not None:
            for ln in _wrap_text(f"Died of {person['death_cause']}.", self.small, w - 20):
                self.screen.blit(self.small.render(ln, True, (160, 140, 130)),
                                 (x + 10, cy))
                cy += 14
            cy += 4

        # Deed (chronicle prose for rulers; sibling fate for non-rulers)
        deed = person.get("deed") or ""
        if deed:
            for ln in _wrap_text(deed, self.small, w - 20):
                self.screen.blit(self.small.render(ln, True, _TXT_C),
                                 (x + 10, cy))
                cy += 15

    # ---- input -----------------------------------------------------------

    def handle_dynasty_tree_click(self, pos, player):
        self._ensure_tree_state()
        back_btn = getattr(self, "_tree_back_btn", None)
        if back_btn and back_btn.collidepoint(pos):
            player.dynasty_tree_open = False
            return True
        for pid, rect in self._tree_person_rects.items():
            if rect.collidepoint(pos):
                self._tree_selected = pid
                return True
        return True  # absorb stray clicks while open
