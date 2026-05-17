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
        self._sommelier_request_rects = {}
        self._sommelier_result_msg = ""
        self._sommelier_result_timer = 0.0

    def close_outpost_menu(self):
        self.outpost_menu_open = False
        self.active_outpost    = None
        self._sommelier_request_rects = {}
        self._sommelier_result_msg = ""

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

        # Guild affiliation
        line_y = sep_y + 60
        from guilds import chapter_for_outpost, guild_for_outpost
        ch = chapter_for_outpost(op.outpost_id)
        g  = guild_for_outpost(op.outpost_id)
        guild_lbl = self.small.render("Guild", True, _DIM_C)
        self.screen.blit(guild_lbl, (px + 16, line_y))
        if g is None:
            gtxt = "Independent — no guild charter"
            gcol = _DIM_C
        else:
            shuttered = ch is not None and op.outpost_id in ch.shuttered_outpost_ids
            tag = " (shuttered)" if shuttered else ""
            gtxt = f"{g.name}{tag}"
            gcol = (180, 100, 100) if shuttered else (160, 200, 170)
        gs = self.font.render(gtxt, True, gcol)
        self.screen.blit(gs, (px + 16, line_y + 16))
        line_y += 46

        # Leader / agenda (if known)
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

        # ── Tournament sign-up button (tournament_grounds only) ────────────
        self._tournament_sign_up_rect = None
        if op.outpost_type == "tournament_grounds":
            btn_w, btn_h = 220, 34
            bx = px + (_PW - btn_w) // 2
            by = py + _PH - 70
            from jousting import _equipped_lance
            ready = (_equipped_lance(player) is not None and
                     getattr(player, "mounted_horse", None) is not None)
            col = (140, 110, 50) if ready else (70, 65, 55)
            pygame.draw.rect(self.screen, col, (bx, by, btn_w, btn_h), border_radius=4)
            label = "Approach the Marshal" if ready else "Need lance + mount"
            ls = self.small.render(label, True, _WHITE)
            self.screen.blit(ls, (bx + (btn_w - ls.get_width()) // 2,
                                  by + (btn_h - ls.get_height()) // 2))
            if ready:
                self._tournament_sign_up_rect = pygame.Rect(bx, by, btn_w, btn_h)

        # ── Coat-of-arms card ──────────────────────────────────────────────
        coa_px = px + _PW + _COA_GAP
        self._draw_outpost_coa_card(region, coa_px, py)

        # ── Sommelier requests (wine outposts only) ────────────────────────
        from sommelier import WINE_OUTPOST_TYPES
        if op.outpost_type in WINE_OUTPOST_TYPES:
            self._draw_sommelier_board(player, op, px, py + _PH + 10,
                                       total_w, 230)

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

    # ──────────────────────────────────────────────────────────────────────
    # Sommelier request board
    # ──────────────────────────────────────────────────────────────────────

    def _draw_sommelier_board(self, player, op, bx, by, bw, bh):
        from sommelier import (get_requests, preview_fulfillment,
                               SOMMELIER_ARCHETYPES, PAIRINGS)
        from wine import WEATHER_TYPES
        from items import ITEMS

        pygame.draw.rect(self.screen, _BG,     (bx, by, bw, bh))
        pygame.draw.rect(self.screen, (170, 80, 90), (bx, by, bw, bh), 2)

        title = self.font.render("Sommelier Requests", True, (235, 200, 180))
        self.screen.blit(title, (bx + 12, by + 8))
        hint = self.small.render("Click a request to fulfill it.", True, _DIM_C)
        self.screen.blit(hint, (bx + 12, by + 30))

        requests = get_requests(op.outpost_id)
        self._sommelier_request_rects = {}

        if not requests:
            none_s = self.small.render("No active requests today.", True, _DIM_C)
            self.screen.blit(none_s, (bx + 12, by + 60))
            return

        card_h = 56
        for i, req in enumerate(requests):
            cy = by + 50 + i * (card_h + 4)
            if cy + card_h > by + bh - 24:
                break
            preview = preview_fulfillment(player, req)
            ok = preview["can_fulfill"]
            border = (180, 150, 80) if ok else (90, 80, 70)
            bg     = (40, 32, 28) if ok else (28, 24, 22)
            card_rect = pygame.Rect(bx + 10, cy, bw - 20, card_h)
            pygame.draw.rect(self.screen, bg, card_rect)
            pygame.draw.rect(self.screen, border, card_rect, 1)
            self._sommelier_request_rects[req["request_id"]] = card_rect

            arch_lbl = SOMMELIER_ARCHETYPES.get(req["archetype"], {}).get("label", "")
            head = self.small.render(
                f"{req['sommelier_name']} ({arch_lbl})", True, (220, 200, 160))
            self.screen.blit(head, (card_rect.x + 8, card_rect.y + 4))

            # Build short request line
            parts = [f"{req['wine_style'].title()}"]
            tier = req["min_tier"]
            if tier != "base":
                parts.append(f"{tier}+")
            if req["vintage_year_min"]:
                parts.append(f"Y{req['vintage_year_min']}+")
            if req["weather_pref"]:
                parts.append(WEATHER_TYPES[req["weather_pref"]]["label"])
            if req["pairing_item"]:
                pair_name = ITEMS.get(req["pairing_item"], {}).get("name", req["pairing_item"])
                parts.append(f"+ {pair_name}")
            req_line = self.small.render("  ·  ".join(parts), True, (200, 180, 150))
            self.screen.blit(req_line, (card_rect.x + 8, card_rect.y + 20))

            # Reward + readiness
            reward_str = f"{preview['total_reward']}g" if ok else f"≤{self._max_reward(req)}g"
            reward_col = (220, 200, 120) if ok else (140, 130, 110)
            r_s = self.small.render(reward_str, True, reward_col)
            self.screen.blit(r_s, (card_rect.right - r_s.get_width() - 8, card_rect.y + 4))

            status_col = (140, 200, 140) if ok else (180, 100, 100)
            status_txt = "Ready" if ok else "Missing wine"
            st = self.small.render(status_txt, True, status_col)
            self.screen.blit(st, (card_rect.right - st.get_width() - 8, card_rect.y + 22))

            if ok and preview["source_label"]:
                src = self.small.render(f"→ {preview['source_label']}", True, (160, 200, 170))
                self.screen.blit(src, (card_rect.x + 8, card_rect.y + 36))

        # Result toast
        if self._sommelier_result_msg:
            msg = self.small.render(self._sommelier_result_msg, True, (240, 220, 150))
            self.screen.blit(msg, (bx + 12, by + bh - 20))

    def _max_reward(self, req):
        return (req["base_reward"] + req["vintage_bonus"]
                + req["weather_bonus"] + req["pairing_bonus"])

    def handle_sommelier_click(self, pos, player):
        """Returns True if a sommelier request card was clicked."""
        # Tournament sign-up at tournament_grounds outposts
        rect = getattr(self, "_tournament_sign_up_rect", None)
        if rect is not None and rect.collidepoint(pos):
            self._open_tournament_from_outpost(player)
            return True
        if not getattr(self, "_sommelier_request_rects", None):
            return False
        from sommelier import fulfill_request
        for rid, rect in self._sommelier_request_rects.items():
            if rect.collidepoint(pos):
                ok, paid, msg = fulfill_request(player, rid)
                self._sommelier_result_msg = msg
                return True
        return False

    def _open_tournament_from_outpost(self, player):
        import random
        from outposts import region_for_outpost
        op = self.active_outpost
        region = region_for_outpost(op)
        rid = region.region_id if region else 0
        rng = random.Random((op.outpost_id * 7919) ^ getattr(player.world, "day_count", 0))
        self.close_outpost_menu()
        self.open_jousting(player, player.world, rid, rng)
