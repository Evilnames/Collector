"""
UI/town_menu.py — TownMenuMixin for the town flag interaction panel.
Shows town name, biome, tier, region, reputation, active needs, and supply buttons
in the main card, plus a separate coat-of-arms card to the right.
"""

import pygame
from constants import SCREEN_W, SCREEN_H

import heraldry
from town_needs import (
    TOWN_CATEGORIES, CATEGORY_DISPLAY, CATEGORY_COLOR,
    GOLD_PER_UNIT, BASE_NEED_AMOUNT,
)

_BG      = (24, 22, 18)
_BORDER  = (160, 130, 80)
_TITLE_C = (240, 220, 160)
_LABEL_C = (200, 185, 140)
_DIM_C   = (110, 100, 75)
_GREEN   = (90, 210, 100)
_YELLOW  = (220, 200, 70)
_RED     = (210, 75, 65)
_WHITE   = (240, 240, 230)

# City info card — tall enough for 4 basic + 2 luxury need rows
_PW = 580
_PH = 570

# Coat-of-arms card (separate, to the right of the city card)
_COA_GAP = 12    # gap between city card and CoA card
_COA_CW  = 200   # coat-of-arms card width
_COA_CH  = _PH   # same height as city card
_SHIELD_W = 160
_SHIELD_H = 200


class TownMenuMixin:

    def open_town_menu(self, town, player=None):
        self.town_menu_open      = True
        self.town_chronicle_open = False
        self.active_town         = town
        self._town_supply_btns   = {}
        self._town_history_btn   = None
        if player is not None:
            player.visited_town_ids.add(town.town_id)

    def close_town_menu(self):
        self.town_menu_open      = False
        self.town_chronicle_open = False
        self.active_town         = None
        self._town_supply_btns   = {}
        self._town_history_btn   = None

    def _draw_town_menu(self, player):
        from towns import REGIONS, TOWNS

        town = self.active_town
        if town is None:
            return

        # Darken background
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        # Both cards together are centred on screen
        total_w = _PW + _COA_GAP + _COA_CW
        px = (SCREEN_W - total_w) // 2
        py = (SCREEN_H - _PH) // 2

        # ── City info card ──────────────────────────────────────────────────
        pygame.draw.rect(self.screen, _BG,    (px, py, _PW, _PH))
        pygame.draw.rect(self.screen, _BORDER,(px, py, _PW, _PH), 2)

        region     = REGIONS.get(town.region_id)
        is_capital = town.is_capital
        region_name = region.name if region else "Unknown Region"
        tier_label  = town.tier_name()

        # Title row
        ts = self.font.render(f"{town.name}  ─  {tier_label}", True, _TITLE_C)
        self.screen.blit(ts, (px + 16, py + 14))

        if is_capital:
            cap_s = self.small.render("★ Capital", True, (240, 210, 80))
            self.screen.blit(cap_s, (px + _PW - cap_s.get_width() - 14, py + 18))

        rg_s = self.small.render(
            f"Region: {region_name}  |  Biome: {town.biome.replace('_', ' ').title()}",
            True, _DIM_C)
        self.screen.blit(rg_s, (px + 16, py + 40))

        # Annexed-from indicator — only present when the town's current
        # kingdom differs from its founding one.
        chronicle_pre = getattr(town, "chronicle", None) or {}
        orig_k = chronicle_pre.get("original_kingdom_name")
        if orig_k:
            ann_s = self.small.render(
                f"Annexed from {orig_k}", True, (210, 165, 100))
            self.screen.blit(ann_s, (px + _PW - ann_s.get_width() - 14, py + 40))

        # Reputation
        rep_label = self.small.render(f"Reputation: {town.reputation}", True, _LABEL_C)
        self.screen.blit(rep_label, (px + 16, py + 60))

        # Growth bar
        gbar_x = px + 200; gbar_y = py + 62; gbar_w = 180; gbar_h = 12
        pygame.draw.rect(self.screen, (50, 50, 40), (gbar_x, gbar_y, gbar_w, gbar_h))
        fill_w = int(gbar_w * min(town.growth_progress, 1.0))
        fill_c = _GREEN if town.all_needs_met() else _DIM_C
        if fill_w > 0:
            pygame.draw.rect(self.screen, fill_c, (gbar_x, gbar_y, fill_w, gbar_h))
        pygame.draw.rect(self.screen, _BORDER, (gbar_x, gbar_y, gbar_w, gbar_h), 1)
        gp_label = self.small.render(f"Growth: {int(town.growth_progress * 100)}%", True, _DIM_C)
        self.screen.blit(gp_label, (gbar_x + gbar_w + 8, gbar_y - 1))

        # Separator
        sep_y = py + 82
        pygame.draw.line(self.screen, _BORDER, (px + 10, sep_y), (px + _PW - 10, sep_y))

        # ── Needs list ──────────────────────────────────────────────────────
        self._town_supply_btns.clear()
        needs_y = sep_y + 10
        row_h   = 76

        for i, (cat, nd) in enumerate(town.needs.items()):
            required  = nd["required"]
            supplied  = nd["supplied"]
            cat_color = CATEGORY_COLOR[cat]
            cat_label = CATEGORY_DISPLAY[cat]
            row_y     = needs_y + i * row_h

            pygame.draw.rect(self.screen, cat_color, (px + 16, row_y + 4, 12, 12))
            cat_s = self.font.render(cat_label, True, _LABEL_C)
            self.screen.blit(cat_s, (px + 34, row_y + 2))

            pct_s = self.small.render(f"{supplied} / {required}", True,
                                      _WHITE if supplied >= required else _YELLOW)

            bar_x = px + 140; bar_y = row_y + 6; bar_w = 200; bar_h = 14
            pygame.draw.rect(self.screen, (45, 40, 30), (bar_x, bar_y, bar_w, bar_h))
            pct = min(supplied / max(required, 1), 1.0)
            fill_c2 = _GREEN if pct >= 1.0 else (_YELLOW if pct >= 0.5 else _RED)
            if pct > 0:
                pygame.draw.rect(self.screen, fill_c2, (bar_x, bar_y, int(bar_w * pct), bar_h))
            pygame.draw.rect(self.screen, _BORDER, (bar_x, bar_y, bar_w, bar_h), 1)

            gld_s = self.small.render(f"{GOLD_PER_UNIT[cat]}g/unit", True, _DIM_C)
            self.screen.blit(gld_s, (bar_x + bar_w + 6, bar_y + 1))

            # Preferred variant hint for luxury needs
            preferred = nd.get("preferred")
            if preferred:
                pref_name = preferred.replace("_", " ").title()
                pref_s = self.small.render(f"Prefers: {pref_name}  (+50% gold)", True,
                                           (210, 175, 60))
                self.screen.blit(pref_s, (px + 34, row_y + 24))
                pct_s_x = px + 34 + pref_s.get_width() + 10
            else:
                pct_s_x = px + 34
            self.screen.blit(pct_s, (pct_s_x, row_y + 24))

            space = max(0, required - supplied)
            have  = player.count_items_in_category(cat)
            btn_y = row_y + 42
            for bi, (label, amount) in enumerate([("+1", 1), ("+10", 10),
                                                   ("ALL", min(space, have))]):
                if amount <= 0 and label != "ALL":
                    amount = 0
                bw = 44; bh = 20
                btn_rect = pygame.Rect(px + 34 + bi * (bw + 4), btn_y, bw, bh)
                enabled  = have > 0 and space > 0 and amount > 0
                col = (70, 130, 70) if enabled else (50, 50, 45)
                pygame.draw.rect(self.screen, col,     btn_rect)
                pygame.draw.rect(self.screen, _BORDER, btn_rect, 1)
                ls = self.small.render(label, True, _WHITE if enabled else _DIM_C)
                self.screen.blit(ls, ls.get_rect(center=btn_rect.center))
                if enabled:
                    self._town_supply_btns[(cat, amount)] = btn_rect

            if i < len(town.needs) - 1:
                line_y = row_y + row_h - 4
                pygame.draw.line(self.screen, (60, 55, 45),
                                 (px + 16, line_y), (px + _PW - 16, line_y))

        # History button
        hist_rect = pygame.Rect(px + 16, py + _PH - 34, 80, 22)
        pygame.draw.rect(self.screen, (55, 70, 55), hist_rect)
        pygame.draw.rect(self.screen, _BORDER, hist_rect, 1)
        hs = self.small.render("History", True, _WHITE)
        self.screen.blit(hs, hs.get_rect(center=hist_rect.center))
        self._town_history_btn = hist_rect

        hint_s = self.small.render("[E] or [ESC] to close", True, _DIM_C)
        self.screen.blit(hint_s, (px + _PW - hint_s.get_width() - 14, py + _PH - 20))

        # ── Coat-of-arms card (separate, to the right) ──────────────────────
        coa_px = px + _PW + _COA_GAP
        self._draw_coat_of_arms_card(region, coa_px, py)

    def _draw_coat_of_arms_card(self, region, cx, cy):
        """Standalone coat-of-arms card at screen position (cx, cy)."""
        # Card background
        pygame.draw.rect(self.screen, _BG,    (cx, cy, _COA_CW, _COA_CH))
        pygame.draw.rect(self.screen, _BORDER,(cx, cy, _COA_CW, _COA_CH), 2)

        # Card title
        lbl = self.small.render("Coat of Arms", True, _DIM_C)
        self.screen.blit(lbl, (cx + (_COA_CW - lbl.get_width()) // 2, cy + 10))

        if region is None or region.coat_of_arms is None:
            msg = self.small.render("Unavailable", True, _DIM_C)
            self.screen.blit(msg, (cx + (_COA_CW - msg.get_width()) // 2, cy + _COA_CH // 2))
            return

        coa = region.coat_of_arms

        # Region name
        rname = self.small.render(region.name, True, _TITLE_C)
        self.screen.blit(rname, (cx + (_COA_CW - rname.get_width()) // 2, cy + 26))

        # Tagline (word-wrapped, italic colour, below region name)
        tagline_y = cy + 42
        if region.tagline:
            tag_words = region.tagline.split()
            tag_lines, tag_line = [], []
            for word in tag_words:
                test = " ".join(tag_line + [word])
                if self.small.size(test)[0] > _COA_CW - 16:
                    if tag_line:
                        tag_lines.append(" ".join(tag_line))
                    tag_line = [word]
                else:
                    tag_line.append(word)
            if tag_line:
                tag_lines.append(" ".join(tag_line))
            for li, ln in enumerate(tag_lines):
                ls = self.small.render(ln, True, (155, 140, 100))
                self.screen.blit(ls, (cx + (_COA_CW - ls.get_width()) // 2,
                                      tagline_y + li * 13))
            tagline_y += len(tag_lines) * 13 + 4

        # Agenda chip — leader's personality
        if region.agenda:
            from towns import agenda_label
            ag_s = self.small.render(f"♚ {agenda_label(region.agenda)} Lord",
                                     True, (210, 175, 80))
            self.screen.blit(ag_s, (cx + (_COA_CW - ag_s.get_width()) // 2, tagline_y))
            tagline_y += 16

        # Shield centred in card
        shield_x = cx + (_COA_CW - _SHIELD_W) // 2
        shield_y = tagline_y
        heraldry.draw(self.screen, shield_x, shield_y, _SHIELD_W, _SHIELD_H, coa)

        # Motto (word-wrapped under shield)
        motto_y = shield_y + _SHIELD_H + 10
        words = coa.motto.split()
        lines, line = [], []
        for word in words:
            test = " ".join(line + [word])
            if self.small.size(test)[0] > _COA_CW - 12:
                if line:
                    lines.append(" ".join(line))
                line = [word]
            else:
                line.append(word)
        if line:
            lines.append(" ".join(line))

        for li, ln in enumerate(lines):
            ls = self.small.render(ln, True, (180, 165, 110))
            self.screen.blit(ls, (cx + (_COA_CW - ls.get_width()) // 2,
                                  motto_y + li * 14))

        # Heraldic details
        detail_y = motto_y + len(lines) * 14 + 8
        pygame.draw.line(self.screen, (60, 55, 40),
                         (cx + 8, detail_y), (cx + _COA_CW - 8, detail_y))
        detail_y += 6

        details = [
            ("Division", coa.division.replace("_", " ").title()),
            ("Ordinary", coa.ordinary.replace("_", " ").title()
                         if coa.ordinary != "none" else "—"),
            ("Charge",   coa.charge.replace("_", " ").title()
                         if coa.charge != "none" else "—"),
        ]
        for label, value in details:
            lbl_s = self.small.render(f"{label}:", True, _DIM_C)
            val_s = self.small.render(value,        True, _LABEL_C)
            self.screen.blit(lbl_s, (cx + 8,                                detail_y))
            self.screen.blit(val_s, (cx + _COA_CW - val_s.get_width() - 8, detail_y))
            detail_y += 14

        # Region specialties — exports (cheaper here) / imports (premium for the leader)
        from towns import region_specialty
        spec = region_specialty(region)
        if spec.get("exports") or spec.get("imports"):
            detail_y += 4
            pygame.draw.line(self.screen, (60, 55, 40),
                             (cx + 8, detail_y), (cx + _COA_CW - 8, detail_y))
            detail_y += 5
            if spec.get("exports"):
                exp_text = "Exports: " + ", ".join(t.title() for t in spec["exports"])
                exp_s = self.small.render(exp_text, True, (140, 200, 130))
                self.screen.blit(exp_s, (cx + 8, detail_y))
                detail_y += 14
            if spec.get("imports"):
                imp_text = "Imports: " + ", ".join(t.title() for t in spec["imports"])
                imp_s = self.small.render(imp_text, True, (220, 170,  90))
                self.screen.blit(imp_s, (cx + 8, detail_y))
                detail_y += 14

    def _draw_city_chronicle(self, town):
        chronicle = getattr(town, "chronicle", None)
        if not chronicle:
            return

        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        self.screen.blit(overlay, (0, 0))

        PW, PH = 700, 660
        px = (SCREEN_W - PW) // 2
        py = (SCREEN_H - PH) // 2

        pygame.draw.rect(self.screen, (14, 12, 10), (px, py, PW, PH))
        pygame.draw.rect(self.screen, (130, 100, 55), (px, py, PW, PH), 2)

        cy = [py + 14]  # mutable via list so closures can update it

        def _section(label):
            pygame.draw.line(self.screen, (80, 65, 35),
                             (px + 10, cy[0]), (px + PW - 10, cy[0]))
            cy[0] += 8
            self.screen.blit(
                self.small.render(label, True, (190, 160, 90)),
                (px + 14, cy[0]))
            cy[0] += 20

        def _body(text, col=(190, 183, 168), indent=14):
            max_w = PW - indent - 28
            words = text.split()
            line_words, lines = [], []
            for word in words:
                test = " ".join(line_words + [word])
                if self.small.size(test)[0] > max_w:
                    if line_words:
                        lines.append(" ".join(line_words))
                    line_words = [word]
                else:
                    line_words.append(word)
            if line_words:
                lines.append(" ".join(line_words))
            for ln in lines:
                self.screen.blit(
                    self.small.render(ln, True, col),
                    (px + indent, cy[0]))
                cy[0] += 15
            cy[0] += 4

        # Title
        title_s = self.font.render(town.name.upper(), True, (230, 210, 140))
        self.screen.blit(title_s, (px + 14, cy[0]))
        cy[0] += 30

        # THE FOUNDING
        _section("THE FOUNDING")
        # Plan-derived founding summary if available, else seeded flavor.
        founding_summary = chronicle.get("founding_summary")
        if founding_summary:
            _body(founding_summary, col=(200, 190, 165), indent=20)
        _body(f"It began as {chronicle['founding_type']}.", indent=20)
        _body(chronicle["founding_act"].capitalize() + ".", col=(180, 175, 158), indent=20)
        _body(chronicle["founding_legacy"].capitalize() + ".", col=(155, 148, 130), indent=20)

        # CHANGE OF BANNER (annexation) — only shown if the town's current
        # kingdom differs from its founding one.
        annex_summary = chronicle.get("annexation_summary")
        if annex_summary:
            _section("A CHANGE OF BANNER")
            _body(annex_summary, col=(210, 165, 110), indent=20)

        # A NOTABLE FIGURE
        _section("A NOTABLE FIGURE")
        self.screen.blit(
            self.small.render(f'"{chronicle["figure_full"]}"', True, (215, 200, 145)),
            (px + 20, cy[0]))
        cy[0] += 18
        _body(chronicle["figure_act"].capitalize() + ".", col=(185, 178, 160), indent=20)

        # A TURNING POINT
        _section("A TURNING POINT")
        _body(chronicle["notable_event"].capitalize() + ".", indent=20)

        # FIVE CENTURIES OF HISTORY (real sim chronicle for this settlement)
        events = chronicle.get("historical_events") or []
        if events:
            _section("FIVE CENTURIES OF HISTORY")
            tier_arc = chronicle.get("tier_arc")
            if tier_arc:
                _body(tier_arc, col=(165, 175, 160), indent=20)
            # Show up to 12 most recent, oldest first
            for line in events[-12:]:
                _body(line, col=(180, 175, 165), indent=20)

        # TODAY
        _section("TODAY")
        _body(chronicle["current_era"].capitalize() + ".", indent=20)

        # LOCAL LEGEND
        _section("LOCAL LEGEND")
        _body(chronicle["local_legend"].capitalize() + ".", col=(170, 155, 130), indent=20)

        # Close hint
        hint = self.small.render("[H] or [ESC] to close", True, (90, 80, 55))
        self.screen.blit(hint, (px + PW - hint.get_width() - 14, py + PH - 18))

    def _draw_ruin_plaque(self):
        info = getattr(self, "ruin_plaque_info", None)
        if not info:
            return

        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        PW, PH = 640, 520
        px = (SCREEN_W - PW) // 2
        py = (SCREEN_H - PH) // 2

        pygame.draw.rect(self.screen, (18, 16, 12), (px, py, PW, PH))
        pygame.draw.rect(self.screen, (140, 125,  90), (px, py, PW, PH), 2)

        cy = [py + 14]

        def _section(label):
            pygame.draw.line(self.screen, (90, 75, 40),
                             (px + 10, cy[0]), (px + PW - 10, cy[0]))
            cy[0] += 8
            self.screen.blit(self.small.render(label, True, (200, 175, 100)),
                             (px + 14, cy[0]))
            cy[0] += 20

        def _body(text, col=(195, 185, 165), indent=14):
            max_w = PW - indent - 28
            words = text.split()
            line, lines = [], []
            for w in words:
                test = " ".join(line + [w])
                if self.small.size(test)[0] > max_w:
                    if line:
                        lines.append(" ".join(line))
                    line = [w]
                else:
                    line.append(w)
            if line:
                lines.append(" ".join(line))
            for ln in lines:
                self.screen.blit(self.small.render(ln, True, col),
                                 (px + indent, cy[0]))
                cy[0] += 15
            cy[0] += 4

        # Title
        title_s = self.font.render(f"HERE LIES {info['name'].upper()}",
                                    True, (235, 215, 145))
        self.screen.blit(title_s, (px + 14, cy[0]))
        cy[0] += 28

        tier_s = self.small.render(
            f"Once a {info['tier']} of {info['original_kingdom']}",
            True, (150, 140, 110))
        self.screen.blit(tier_s, (px + 14, cy[0]))
        cy[0] += 22

        _section("THE FOUNDING")
        founder_dyn = info.get("founder_dynasty")
        if founder_dyn:
            _body(f"Raised in year {info['founded_year']} under {founder_dyn}.",
                  indent=20)
        else:
            _body(f"Raised in year {info['founded_year']}.", indent=20)

        _section("THE FALL")
        ruined_year = info.get("ruined_year", -1)
        years_ago = info["history_years"] - ruined_year if ruined_year > 0 else None
        if ruined_year > 0:
            ago_str = f" — {years_ago} years ago" if years_ago is not None else ""
            _body(f"Ruined in year {ruined_year}{ago_str}. {info['cause_phrase']}",
                  indent=20)
        else:
            _body(info["cause_phrase"], indent=20)

        cur = info.get("current_kingdom")
        if cur and cur != info["original_kingdom"]:
            _body(f"The land now lies under {cur}.",
                  col=(180, 170, 150), indent=20)
        elif cur is None:
            _body("The land has lain masterless ever since.",
                  col=(165, 155, 130), indent=20)

        events = info.get("events") or []
        if events:
            _section("WHAT THE STONES REMEMBER")
            for line in events:
                _body(line, col=(180, 175, 160), indent=20)

        hint = self.small.render("[E] or [ESC] to leave", True, (90, 80, 55))
        self.screen.blit(hint, (px + PW - hint.get_width() - 14, py + PH - 22))

    def handle_town_menu_click(self, pos, player):
        if self.town_chronicle_open:
            return True  # absorb clicks while chronicle is open
        if self._town_history_btn and self._town_history_btn.collidepoint(pos):
            self.town_chronicle_open = True
            return True
        for (cat, amount), rect in self._town_supply_btns.items():
            if rect.collidepoint(pos):
                from towns import supply_need
                gold, rep = supply_need(self.active_town, player, cat, amount)
                if gold > 0:
                    player.pending_notifications.append(
                        ("Town", f"Supplied {amount} {CATEGORY_DISPLAY[cat]} → +{gold}g", None)
                    )
                return True
        return False
