"""Court & Crown — Politics & Dynasties UI.

A set of tabs grafted onto the reputation screen. The original Standing tab
(visited towns + map) is preserved unchanged; this mixin adds:

  Houses     — grid of every ruling house, click for deep panel
  Web        — graph of houses with alliance/feud + scandal halos
  Newswire   — scrolling political/economic news feed
  Orders     — knightly orders by region with prestige + sworn-to
  Actions    — six manipulation verbs against the selected house

Click handling is unified through CourtMixin.handle_court_click so the parent
ReputationScreenMixin only needs to dispatch into us when its tab is active.
"""

import math
import pygame

import heraldry
import politics as pol


_BG          = (24, 22, 18)
_PANEL_BG    = (32, 28, 22)
_BORDER      = (160, 130, 80)
_TITLE_C     = (240, 220, 160)
_LABEL_C     = (200, 185, 140)
_DIM_C       = (120, 110, 90)
_VDIM_C      = (70, 65, 55)
_GREEN       = (130, 200, 130)
_RED         = (210, 90, 80)
_YELLOW      = (220, 200, 70)
_GOLD        = (220, 175, 40)
_BLUE        = (130, 175, 230)
_PURPLE      = (175, 140, 210)

COURT_TABS = [
    ("standing", "STANDING"),
    ("houses",   "HOUSES"),
    ("faiths",   "FAITHS"),
    ("web",      "WEB"),
    ("news",     "NEWSWIRE"),
    ("orders",   "ORDERS"),
    ("actions",  "ACTIONS"),
]


def _posture_arrow(posture: str) -> tuple[str, tuple]:
    return {
        "rising":    ("↑", _GREEN),
        "declining": ("↓", _RED),
        "crisis":    ("!", _GOLD),
    }.get(posture, ("·", _DIM_C))


def _bar(screen, x, y, w, h, frac, fg, bg=(40, 38, 30), border=None):
    pygame.draw.rect(screen, bg, (x, y, w, h))
    fill = max(0, min(w, int(w * frac)))
    if fill:
        pygame.draw.rect(screen, fg, (x, y, fill, h))
    if border:
        pygame.draw.rect(screen, border, (x, y, w, h), 1)


def _bar_label(screen, font, x, y, label_w, label, color, frac, value_text):
    ls = font.render(label, True, _LABEL_C)
    screen.blit(ls, (x, y))
    _bar(screen, x + label_w, y + 2, 100, 8, frac, color, border=_VDIM_C)
    vs = font.render(value_text, True, color)
    screen.blit(vs, (x + label_w + 108, y))


def _point_near_segment(px, py, x1, y1, x2, y2, tol=6) -> bool:
    # Project point onto segment, measure perpendicular distance.
    dx = x2 - x1; dy = y2 - y1
    if dx == 0 and dy == 0:
        return ((px - x1) ** 2 + (py - y1) ** 2) ** 0.5 <= tol
    t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)
    t = max(0.0, min(1.0, t))
    cx = x1 + t * dx; cy = y1 + t * dy
    return ((px - cx) ** 2 + (py - cy) ** 2) ** 0.5 <= tol


class CourtMixin:

    # ---------------------------------------------------------------------
    # Tab bar (drawn at top of court panel; returns the content rect inside)
    # ---------------------------------------------------------------------

    def _draw_court_tab_bar(self, screen, cx, cy, cw, ch):
        active = getattr(self, "_court_tab", "standing")
        btn_h = 26
        btn_y = cy + 38
        # Total width of all tab buttons, evenly spaced
        n = len(COURT_TABS)
        gap = 4
        avail = cw - 24
        btn_w = (avail - gap * (n - 1)) // n
        self._court_tab_rects = {}
        x = cx + 12
        for key, label in COURT_TABS:
            r = pygame.Rect(x, btn_y, btn_w, btn_h)
            self._court_tab_rects[key] = r
            sel = (active == key)
            bg = (52, 46, 34) if sel else (28, 26, 20)
            brd = _GOLD if sel else _VDIM_C
            pygame.draw.rect(screen, bg, r)
            pygame.draw.rect(screen, brd, r, 1)
            ls = self.small.render(label, True, _TITLE_C if sel else _DIM_C)
            screen.blit(ls, (x + (btn_w - ls.get_width()) // 2,
                             btn_y + (btn_h - ls.get_height()) // 2))
            x += btn_w + gap

    def get_court_tab(self) -> str:
        return getattr(self, "_court_tab", "standing")

    def set_court_tab(self, tab: str) -> None:
        self._court_tab = tab
        # Reset per-tab scroll state when switching
        self._court_scroll = 0

    # ---------------------------------------------------------------------
    # Houses tab — grid of all ruling families
    # ---------------------------------------------------------------------

    def _draw_court_houses(self, screen, player, cx, cy, cw, ch, top, bot):
        # If a house deep panel is active, draw that instead of the grid.
        rid = getattr(self, "_court_house_panel_rid", None)
        if rid is not None:
            self._draw_house_deep_panel(screen, player, cx, cy, cw, ch, top, bot, rid)
            return
        from towns import REGIONS
        visited = getattr(player, "visited_town_ids", set())
        # Filter to regions the player has visited (at least one town)
        visible_regions = []
        for region in sorted(REGIONS.values(), key=lambda r: r.region_id):
            if any(tid in visited for tid in region.member_town_ids):
                visible_regions.append(region)
        # Always seed houses for visible regions
        for r in visible_regions:
            pol.seed_house_for_region(r)

        card_w, card_h = 260, 110
        cols = max(1, (cw - 28) // (card_w + 10))
        rows = (len(visible_regions) + cols - 1) // cols
        total_h = rows * (card_h + 10) + 14
        content_h = bot - top
        self._court_max_scroll = max(0, total_h - content_h)
        scroll = max(0, min(getattr(self, "_court_scroll", 0), self._court_max_scroll))
        self._court_scroll = scroll

        old_clip = screen.get_clip()
        screen.set_clip(pygame.Rect(cx, top, cw, content_h))

        self._court_house_rects = {}
        x0 = cx + 14
        y0 = top + 8 - scroll
        for i, region in enumerate(visible_regions):
            row, col = divmod(i, cols)
            cx_card = x0 + col * (card_w + 10)
            cy_card = y0 + row * (card_h + 10)
            if cy_card + card_h < top or cy_card > bot:
                continue
            house = pol.HOUSE_STATES.get(region.region_id)
            self._draw_house_card(screen, cx_card, cy_card, card_w, card_h, region, house, player)
            self._court_house_rects[region.region_id] = pygame.Rect(
                cx_card, cy_card, card_w, card_h)

        if not visible_regions:
            ns = self.font.render("No houses known yet — visit a town.", True, _DIM_C)
            screen.blit(ns, (cx + (cw - ns.get_width()) // 2, top + content_h // 2))

        screen.set_clip(old_clip)
        self._draw_court_scrollbar(screen, cx, top, cw, content_h)

    def _draw_house_card(self, screen, x, y, w, h, region, house, player):
        sel = (getattr(self, "_court_selected_rid", None) == region.region_id)
        pygame.draw.rect(screen, _PANEL_BG, (x, y, w, h))
        pygame.draw.rect(screen, _GOLD if sel else _BORDER, (x, y, w, h), 1)
        # COA on left
        coa_w, coa_h = 44, 56
        if region.coat_of_arms:
            heraldry.draw(screen, x + 6, y + 8, coa_w, coa_h, region.coat_of_arms)
        else:
            pygame.draw.rect(screen, (50, 45, 38), (x + 6, y + 8, coa_w, coa_h))
        # Name + posture
        tx = x + 6 + coa_w + 8
        name = house.name if house else region.name
        ns = self.small.render(name[:28], True, _TITLE_C)
        screen.blit(ns, (tx, y + 6))
        arrow, acol = _posture_arrow(house.posture if house else "stable")
        ps = self.font.render(arrow, True, acol)
        screen.blit(ps, (x + w - ps.get_width() - 8, y + 4))
        # Region · biome
        sub = f"{region.name} · {region.biome_group.title()}"
        ss = self.small.render(sub[:34], True, _DIM_C)
        screen.blit(ss, (tx, y + 22))
        # Power bar
        if house:
            bs = self.small.render("Power", True, _LABEL_C)
            screen.blit(bs, (tx, y + 40))
            _bar(screen, tx + 46, y + 42, 110, 8, house.power / 100, _BLUE, border=_VDIM_C)
            vs = self.small.render(str(house.power), True, _LABEL_C)
            screen.blit(vs, (tx + 160, y + 40))
            # Prestige bar
            ps2 = self.small.render("Pres.", True, _LABEL_C)
            screen.blit(ps2, (tx, y + 56))
            _bar(screen, tx + 46, y + 58, 110, 8, house.prestige / 100, _GOLD, border=_VDIM_C)
            vs = self.small.render(str(house.prestige), True, _LABEL_C)
            screen.blit(vs, (tx + 160, y + 56))
            # Scandal bar (only if > 0)
            if house.scandal > 0:
                ss2 = self.small.render("Scand.", True, _RED)
                screen.blit(ss2, (tx, y + 72))
                _bar(screen, tx + 46, y + 74, 110, 8, house.scandal / 100, _RED, border=_VDIM_C)
                vs = self.small.render(str(house.scandal), True, _RED)
                screen.blit(vs, (tx + 160, y + 72))
        # Influence tier (bottom-right)
        infl = pol.get_influence(region.region_id)
        tier_label, tcol = pol.influence_tier(infl)
        its = self.small.render(f"{tier_label} ({infl:+d})", True, tcol)
        screen.blit(its, (x + w - its.get_width() - 8, y + h - 16))

    # ---------------------------------------------------------------------
    # House Deep Panel — modal, replaces grid when an rid is "panel-open"
    # ---------------------------------------------------------------------

    def _draw_house_deep_panel(self, screen, player, cx, cy, cw, ch, top, bot, rid):
        try:
            from towns import REGIONS, TOWNS, agenda_label
        except Exception:
            REGIONS, TOWNS = {}, {}
            agenda_label = lambda a: a
        region = REGIONS.get(rid)
        house  = pol.HOUSE_STATES.get(rid)
        if region is None or house is None:
            ns = self.font.render("House not found.", True, _DIM_C)
            screen.blit(ns, (cx + 20, top + 20))
            return

        # ── Header: BACK button + house name + region · biome
        back_rect = pygame.Rect(cx + 14, top + 4, 64, 22)
        pygame.draw.rect(screen, (40, 38, 30), back_rect)
        pygame.draw.rect(screen, _GOLD, back_rect, 1)
        bs = self.small.render("< BACK", True, _TITLE_C)
        screen.blit(bs, (back_rect.x + 8, back_rect.y + 4))
        self._court_back_btn = back_rect

        # Sigil + name block
        sx = cx + 90
        sy = top + 6
        coa_w, coa_h = 56, 72
        if region.coat_of_arms:
            heraldry.draw(screen, sx, sy, coa_w, coa_h, region.coat_of_arms)
        else:
            pygame.draw.rect(screen, (50, 45, 38), (sx, sy, coa_w, coa_h))
        tx = sx + coa_w + 12
        ns = self.font.render(house.name, True, _TITLE_C)
        screen.blit(ns, (tx, sy))
        sub = f"{region.name}  ·  {region.biome_group.title()}  ·  {region.wealth.title()}  ·  {region.danger.title()}"
        ss = self.small.render(sub, True, _LABEL_C)
        screen.blit(ss, (tx, sy + 22))
        ag = agenda_label(getattr(region, "agenda", "")) or ""
        epithet = pol.agenda_profile(getattr(region, "agenda", ""))["epithet"]
        if ag:
            ags = self.small.render(f"Agenda: {ag}  ·  Reputation: {epithet}",
                                    True, _PURPLE)
            screen.blit(ags, (tx, sy + 38))
        if region.tagline:
            tgs = self.small.render(f"\"{region.tagline}\"", True, _DIM_C)
            screen.blit(tgs, (tx, sy + 54))

        # ── Ruler + Heir (left column)
        col_top = top + 92
        col_x   = cx + 18
        col_w   = (cw - 36) // 2 - 8
        col_h   = bot - col_top - 8

        slate = pol.get_heir_slate(region)
        self._draw_panel_section(screen, col_x, col_top, col_w, "RULER & HEIR")
        y = col_top + 22
        rs = self.small.render(
            f"{slate.ruler_title} {slate.ruler_name} {epithet}",
            True, _GOLD)
        screen.blit(rs, (col_x + 8, y)); y += 18
        heir_title = pol._HEIR_TITLES.get(slate.ruler_title, "Heir-Apparent")
        hs = self.small.render(
            f"{heir_title}: {slate.heir_name}  (age {slate.heir_age})",
            True, _LABEL_C)
        screen.blit(hs, (col_x + 8, y)); y += 18
        # Faith of the ruling house — always resolved via faith_for_region.
        try:
            import religion as rel
            ruler_faith = rel.faith_for_region(region.region_id)
            if ruler_faith is not None:
                tint = rel.doctrine_profile(ruler_faith.doctrine).get(
                    "tint", (200, 195, 170))
                fs = self.small.render(
                    f"Faith: {ruler_faith.name} ({ruler_faith.doctrine})",
                    True, tint)
                screen.blit(fs, (col_x + 8, y)); y += 18
        except Exception:
            pass
        y += 6

        # ── Power breakdown
        brk = pol.power_breakdown(rid)
        self._draw_panel_section(screen, col_x, y, col_w, "POWER BREAKDOWN")
        y += 22
        lines = [
            (f"Treasury  +{brk.get('treasury', 0):>3}",  _GOLD),
            (f"Guilds    +{brk.get('guilds',   0):>3}   ({brk.get('n_guilds', 0)} backing)", _BLUE),
            (f"Orders    +{brk.get('orders',   0):>3}   ({brk.get('n_orders', 0)} sworn)", _PURPLE),
            (f"Prestige  +{brk.get('prestige', 0):>3}", _YELLOW),
            (f"Scandal   -{brk.get('scandal_pen', 0):>3}", _RED),
        ]
        for txt, col in lines:
            ls = self.small.render(txt, True, col)
            screen.blit(ls, (col_x + 8, y))
            y += 15
        ts = self.small.render(f"= {brk.get('total', 0):3d} / 100 power",
                                True, _TITLE_C)
        screen.blit(ts, (col_x + 8, y)); y += 22

        # ── Backing guilds
        guilds = pol.backing_guilds(rid)
        self._draw_panel_section(screen, col_x, y, col_w, "BACKING GUILDS")
        y += 22
        if not guilds:
            ns = self.small.render("None — no industrial base.", True, _DIM_C)
            screen.blit(ns, (col_x + 8, y)); y += 16
        for g in guilds[:5]:
            gs = self.small.render(
                f"· {g.name[:24]:<24} {g.industry[:8]:<8} {g.treasury:>5}g",
                True, _LABEL_C)
            screen.blit(gs, (col_x + 8, y)); y += 14

        # ── Sworn orders
        y += 6
        orders = pol.backing_orders(rid)
        self._draw_panel_section(screen, col_x, y, col_w, "SWORN ORDERS")
        y += 22
        if not orders:
            ns = self.small.render("None.", True, _DIM_C)
            screen.blit(ns, (col_x + 8, y)); y += 16
        for o in orders[:4]:
            pledged = pol.PLAYER_PLEDGES.get(o.order_id) == rid
            tag = " [Pledged]" if pledged else ""
            os_ = self.small.render(
                f"· {o.name[:22]:<22} {o.tradition[:8]:<8} P{o.prestige}{tag}",
                True, _GOLD if pledged else _LABEL_C)
            screen.blit(os_, (col_x + 8, y)); y += 14

        # ── Right column: stats bars, succession crisis, envoy report,
        #    influence log, recent newswire mentions
        rcol_x = cx + 18 + col_w + 16
        ry = col_top
        self._draw_panel_section(screen, rcol_x, ry, col_w, "STATUS")
        ry += 22
        _bar_label(screen, self.small, rcol_x + 8, ry, 80, "Power", _BLUE,
                   house.power / 100, str(house.power))
        ry += 16
        _bar_label(screen, self.small, rcol_x + 8, ry, 80, "Prestige", _GOLD,
                   house.prestige / 100, str(house.prestige))
        ry += 16
        _bar_label(screen, self.small, rcol_x + 8, ry, 80, "Scandal", _RED,
                   house.scandal / 100, str(house.scandal))
        ry += 16
        arrow, acol = _posture_arrow(house.posture)
        ps = self.small.render(f"Posture: {arrow} {house.posture.title()}    "
                                f"Treasury: {house.treasury}g",
                                True, acol)
        screen.blit(ps, (rcol_x + 8, ry)); ry += 22

        # Succession crisis (if any)
        crisis = pol.SUCCESSION.get(rid)
        if crisis and not crisis.resolved:
            elapsed = max(0, getattr(player, "_court_day_cache", 0) - crisis.crisis_started_day)
            self._draw_panel_section(screen, rcol_x, ry, col_w,
                                      f"SUCCESSION CRISIS (day {elapsed})")
            ry += 22
            for c in crisis.contenders:
                marker = "★" if c["player_backed"] else "·"
                cs = self.small.render(
                    f"{marker} {c['name'][:32]:<32}  support {c['support']:>3}",
                    True, _GOLD if c["player_backed"] else _LABEL_C)
                screen.blit(cs, (rcol_x + 8, ry)); ry += 14
            ry += 6

        # Envoy report (if recent)
        report = pol.ENVOY_REPORTS.get(rid)
        if report:
            self._draw_panel_section(screen, rcol_x, ry, col_w,
                                      f"ENVOY REPORT (day {report['day']})")
            ry += 22
            ry = self._wrap_text(screen, self.small, report["report"],
                                  rcol_x + 8, ry, col_w - 16, _LABEL_C, max_lines=4)
            ry += 6

        # Influence log
        self._draw_panel_section(screen, rcol_x, ry, col_w, "YOUR INFLUENCE LOG")
        ry += 22
        rec = pol.PLAYER_INFLUENCE.get(rid)
        infl_total = rec.total if rec else 0
        tier_label, tcol = pol.influence_tier(infl_total)
        ts = self.small.render(f"{tier_label}  ({infl_total:+d})", True, tcol)
        screen.blit(ts, (rcol_x + 8, ry)); ry += 16
        log = rec.log if rec else []
        if not log:
            ns = self.small.render("No history yet.", True, _DIM_C)
            screen.blit(ns, (rcol_x + 8, ry)); ry += 14
        for entry in log[:6]:
            d = entry.get("day", 0); delta = entry.get("delta", 0); src = entry.get("source", "")
            ec = _GREEN if delta > 0 else _RED if delta < 0 else _LABEL_C
            es = self.small.render(
                f"d{d:>4}  {delta:+3d}  {src[:24]}", True, ec)
            screen.blit(es, (rcol_x + 8, ry)); ry += 14
        ry += 6

        # Recent newswire mentions of this house
        try:
            from industry_events import NEWSWIRE as _NW
        except Exception:
            _NW = []
        mentions = [n for n in _NW
                    if house.name and house.name in n.get("headline", "")][:5]
        if mentions and ry < bot - 30:
            self._draw_panel_section(screen, rcol_x, ry, col_w, "RECENT NEWSWIRE")
            ry += 22
            for n in mentions:
                if ry > bot - 16:
                    break
                ns_ = self.small.render(
                    f"d{n.get('day', 0):>4}  {n.get('headline', '')[:48]}",
                    True, _LABEL_C)
                screen.blit(ns_, (rcol_x + 8, ry)); ry += 14

    def _draw_panel_section(self, screen, x, y, w, label):
        pygame.draw.line(screen, _VDIM_C, (x, y + 16), (x + w, y + 16), 1)
        ls = self.small.render(label, True, _GOLD)
        screen.blit(ls, (x + 4, y + 2))

    def _wrap_text(self, screen, font, text, x, y, max_w, color, max_lines=4):
        words = text.split()
        line = ""
        lines = 0
        for w in words:
            test = (line + " " + w).strip()
            if font.size(test)[0] > max_w:
                screen.blit(font.render(line, True, color), (x, y))
                y += 14
                lines += 1
                line = w
                if lines >= max_lines:
                    line = ""
                    break
            else:
                line = test
        if line:
            screen.blit(font.render(line, True, color), (x, y))
            y += 14
        return y

    # ---------------------------------------------------------------------
    # Faiths tab — grid of faith cards + deep panel
    # ---------------------------------------------------------------------

    def _draw_court_faiths(self, screen, player, cx, cy, cw, ch, top, bot):
        fid = getattr(self, "_court_faith_panel_fid", None)
        if fid is not None:
            self._draw_faith_deep_panel(screen, player, cx, cy, cw, ch,
                                        top, bot, fid)
            return

        try:
            import religion as rel
            from towns import REGIONS
        except Exception:
            return

        # Faiths the player has any chance of knowing about — any faith with
        # non-zero adherence in a visited region.
        visited = getattr(player, "visited_town_ids", set())
        visited_rids = {r.region_id for r in REGIONS.values()
                        if any(tid in visited for tid in r.member_town_ids)}
        visible: list = []
        for faith in rel.FAITH_STATES.values():
            adh = rel.FAITH_REGIONS.get(faith.faith_id, {})
            if any(rid in visited_rids and adh.get(rid, 0) > 0 for rid in adh):
                visible.append(faith)

        if not visible:
            ns = self.font.render(
                "No faiths revealed yet — visit a town and speak to its clergy.",
                True, _DIM_C)
            screen.blit(ns, (cx + (cw - ns.get_width()) // 2,
                             top + (bot - top) // 2))
            return

        card_w, card_h = 280, 140
        cols = max(1, (cw - 28) // (card_w + 10))
        rows = (len(visible) + cols - 1) // cols
        total_h = rows * (card_h + 10) + 14
        content_h = bot - top
        self._court_max_scroll = max(0, total_h - content_h)
        scroll = max(0, min(getattr(self, "_court_scroll", 0),
                            self._court_max_scroll))
        self._court_scroll = scroll

        old_clip = screen.get_clip()
        screen.set_clip(pygame.Rect(cx, top, cw, content_h))
        self._court_faith_rects = {}
        x0 = cx + 14
        y0 = top + 8 - scroll
        for i, faith in enumerate(visible):
            row, col = divmod(i, cols)
            cx_card = x0 + col * (card_w + 10)
            cy_card = y0 + row * (card_h + 10)
            if cy_card + card_h < top or cy_card > bot:
                continue
            self._draw_faith_card(screen, cx_card, cy_card, card_w, card_h,
                                  faith, visited_rids)
            self._court_faith_rects[faith.faith_id] = pygame.Rect(
                cx_card, cy_card, card_w, card_h)
        screen.set_clip(old_clip)
        self._draw_court_scrollbar(screen, cx, top, cw, content_h)

    def _draw_faith_card(self, screen, x, y, w, h, faith, visited_rids):
        import religion as rel
        sel = (getattr(self, "_court_selected_fid", None) == faith.faith_id)
        pygame.draw.rect(screen, _PANEL_BG, (x, y, w, h))
        pygame.draw.rect(screen, _GOLD if sel else _BORDER, (x, y, w, h), 1)

        profile = rel.doctrine_profile(faith.doctrine)
        tint    = profile.get("tint", (180, 170, 150))

        # Doctrine swatch (left)
        pygame.draw.rect(screen, tint, (x + 8, y + 8, 26, 26))
        pygame.draw.rect(screen, _VDIM_C, (x + 8, y + 8, 26, 26), 1)

        # Name + doctrine subtitle
        tx = x + 42
        ns = self.small.render(faith.name[:32], True, _TITLE_C)
        screen.blit(ns, (tx, y + 6))
        sub = f"{faith.doctrine.title()}  ·  {profile.get('epithet', '')}"
        ss = self.small.render(sub[:38], True, tint)
        screen.blit(ss, (tx, y + 22))

        # Head + posture arrow
        head_line = f"{faith.head_title}: {faith.head_name}"
        hs = self.small.render(head_line[:36], True, _LABEL_C)
        screen.blit(hs, (tx, y + 38))
        # Posture sigil ─ schism takes priority over crisis
        post_glyph, pcol = self._faith_posture_glyph(faith.posture)
        psg = self.font.render(post_glyph, True, pcol)
        screen.blit(psg, (x + w - psg.get_width() - 8, y + 4))

        # Four bars: piety, ortho, zeal, scandal
        bx = tx
        by = y + 58
        for i, (lbl, val, col) in enumerate([
                ("Piety",  faith.piety,     _YELLOW),
                ("Ortho",  faith.orthodoxy, _BLUE),
                ("Zeal",   faith.zeal,      _RED),
                ("Scand.", faith.scandal,   _PURPLE)]):
            row_y = by + i * 14
            ls = self.small.render(lbl, True, _DIM_C)
            screen.blit(ls, (bx, row_y))
            _bar(screen, bx + 46, row_y + 2, 100, 7,
                 val / 100.0, col, border=_VDIM_C)
            vs = self.small.render(str(int(val)), True, _LABEL_C)
            screen.blit(vs, (bx + 152, row_y))

        # Player standing pill (bottom-right)
        standing = rel.get_standing(faith.faith_id)
        tier_lbl, tcol = rel.standing_tier(standing)
        its = self.small.render(f"{tier_lbl} ({standing:+d})", True, tcol)
        screen.blit(its, (x + w - its.get_width() - 8, y + h - 16))

        # Reach count (regions touched / visited)
        adh = rel.FAITH_REGIONS.get(faith.faith_id, {})
        reach = sum(1 for rid in adh if rid in visited_rids and adh[rid] > 0)
        rs = self.small.render(f"{reach} region{'s' if reach != 1 else ''}",
                                True, _DIM_C)
        screen.blit(rs, (x + 8, y + h - 16))

    def _faith_posture_glyph(self, posture: str):
        return {
            "rising":    ("↑", _GREEN),
            "declining": ("↓", _RED),
            "crisis":    ("!", _GOLD),
            "schism":    ("✕", _PURPLE),
        }.get(posture, ("·", _DIM_C))

    # ---------------------------------------------------------------------
    # Faith deep panel — opens when a card is clicked
    # ---------------------------------------------------------------------

    def _draw_faith_deep_panel(self, screen, player, cx, cy, cw, ch,
                                top, bot, fid):
        try:
            import religion as rel
            from towns import REGIONS
        except Exception:
            return
        faith = rel.FAITH_STATES.get(fid)
        if faith is None:
            ns = self.font.render("Faith not found.", True, _DIM_C)
            screen.blit(ns, (cx + 20, top + 20))
            return

        # ── Header: BACK + name + doctrine
        back_rect = pygame.Rect(cx + 14, top + 4, 64, 22)
        pygame.draw.rect(screen, (40, 38, 30), back_rect)
        pygame.draw.rect(screen, _GOLD, back_rect, 1)
        bs = self.small.render("< BACK", True, _TITLE_C)
        screen.blit(bs, (back_rect.x + 8, back_rect.y + 4))
        self._court_back_btn = back_rect

        profile = rel.doctrine_profile(faith.doctrine)
        tint    = profile.get("tint", (180, 170, 150))
        pygame.draw.rect(screen, tint, (cx + 90, top + 4, 38, 38))
        pygame.draw.rect(screen, _VDIM_C, (cx + 90, top + 4, 38, 38), 1)
        ns = self.font.render(faith.name, True, _TITLE_C)
        screen.blit(ns, (cx + 138, top + 4))
        sub = (f"{faith.doctrine.title()}  ·  {profile.get('epithet','')}  ·  "
               f"posture: {faith.posture}")
        screen.blit(self.small.render(sub, True, tint), (cx + 138, top + 26))

        # ── Two columns: stats on the left, regions/orders/news on the right
        col_y = top + 56
        left_x  = cx + 16
        right_x = cx + cw // 2 + 10
        col_w   = cw // 2 - 30

        self._draw_faith_stats_block(screen, faith, left_x, col_y, col_w)
        self._draw_faith_clergy_block(screen, faith, left_x, col_y + 160, col_w)
        self._draw_faith_history_block(screen, faith, left_x, col_y + 240,
                                        col_w, bot - (col_y + 240) - 6)
        self._draw_faith_regions_block(screen, faith, right_x, col_y, col_w)
        self._draw_faith_orders_block(screen, faith, right_x, col_y + 150,
                                       col_w)
        self._draw_faith_news_block(screen, faith, right_x, col_y + 280, col_w)

    def _draw_faith_stats_block(self, screen, faith, x, y, w):
        import religion as rel
        hdr = self.small.render("DOCTRINE & STANDING", True, _LABEL_C)
        screen.blit(hdr, (x, y))
        pygame.draw.line(screen, _BORDER, (x, y + 16), (x + w, y + 16))

        # Stat bars
        bars = [
            ("Piety",     faith.piety,     _YELLOW),
            ("Orthodoxy", faith.orthodoxy, _BLUE),
            ("Zeal",      faith.zeal,      _RED),
            ("Scandal",   faith.scandal,   _PURPLE),
        ]
        for i, (lbl, val, col) in enumerate(bars):
            row_y = y + 22 + i * 18
            ls = self.small.render(lbl, True, _DIM_C)
            screen.blit(ls, (x, row_y))
            _bar(screen, x + 80, row_y + 2, 140, 9,
                 val / 100.0, col, border=_VDIM_C)
            vs = self.small.render(str(int(val)), True, _LABEL_C)
            screen.blit(vs, (x + 226, row_y))

        # Treasury + player standing
        ty = y + 22 + 4 * 18 + 8
        ts = self.small.render(f"Treasury: {faith.treasury}g", True, _GOLD)
        screen.blit(ts, (x, ty))
        standing = rel.get_standing(faith.faith_id)
        tier, tcol = rel.standing_tier(standing)
        st = self.small.render(f"Your standing: {tier} ({standing:+d})",
                               True, tcol)
        screen.blit(st, (x, ty + 16))

    def _draw_faith_clergy_block(self, screen, faith, x, y, w):
        hdr = self.small.render("HEAD & DOCTRINE TENETS", True, _LABEL_C)
        screen.blit(hdr, (x, y))
        pygame.draw.line(screen, _BORDER, (x, y + 16), (x + w, y + 16))

        head_line = f"{faith.head_title}: {faith.head_name}"
        screen.blit(self.small.render(head_line, True, _TITLE_C),
                    (x, y + 22))

        # Doctrine flavor tags (hostile_to from profile)
        import religion as rel
        profile = rel.doctrine_profile(faith.doctrine)
        hostile = profile.get("hostile_to", ())
        if hostile:
            tags = "  ·  ".join(f"hostile: {h}" for h in hostile)
            screen.blit(self.small.render(tags, True, _RED), (x, y + 40))

        # Drift hint
        drift = (f"Drifts: piety {profile.get('piety_drift', 0):+.2f}/d  ·  "
                 f"orthodoxy {profile.get('orthodoxy_drift', 0):+.2f}/d  ·  "
                 f"zeal {profile.get('zeal_drift', 0):+.2f}/d")
        screen.blit(self.small.render(drift, True, _DIM_C), (x, y + 56))

    def _draw_faith_regions_block(self, screen, faith, x, y, w):
        import religion as rel
        try:
            from towns import REGIONS
        except Exception:
            REGIONS = {}
        hdr = self.small.render("REGIONS & CLERGY", True, _LABEL_C)
        screen.blit(hdr, (x, y))
        pygame.draw.line(screen, _BORDER, (x, y + 16), (x + w, y + 16))

        adh = rel.FAITH_REGIONS.get(faith.faith_id, {})
        if not adh:
            screen.blit(self.small.render("(no congregations)", True, _DIM_C),
                        (x, y + 22))
            return
        # Top 4 regions by adherence, with heresy% inline
        rows = sorted(adh.items(), key=lambda kv: -kv[1])[:4]
        ry = y + 22
        for rid, pct in rows:
            region = REGIONS.get(rid)
            rname  = region.name if region else f"Region {rid}"
            clergy = rel.CLERGY.get(rid)
            bishop = ""
            if clergy and clergy.faith_id == faith.faith_id:
                bishop = f"   ·   {clergy.bishop_title} {clergy.bishop_name}"
                if clergy.posture != "loyal":
                    bishop += f" [{clergy.posture}]"
            heresy_pct = rel.get_heresy(rid, faith.faith_id)
            line = f"{rname}  {pct}%{bishop}"
            screen.blit(self.small.render(line[:60], True, _LABEL_C),
                        (x, ry))
            _bar(screen, x + w - 80, ry + 2, 70, 7, pct / 100.0,
                 _YELLOW, border=_VDIM_C)
            if heresy_pct > 0:
                hs = self.small.render(f"heresy {heresy_pct}%", True, _PURPLE)
                screen.blit(hs, (x + w - 80, ry + 10))
            ry += 22

        # Schism crisis banner — replaces any spare space in this block
        crisis = rel.SCHISMS.get(faith.faith_id)
        if crisis and not crisis.resolved:
            bx = x
            by = ry + 4
            pygame.draw.rect(screen, (60, 30, 60), (bx, by, w, 32))
            pygame.draw.rect(screen, _PURPLE, (bx, by, w, 32), 1)
            sline = (f"SCHISM: {crisis.breakaway_name} "
                     f"({crisis.breakaway_doctrine})")
            screen.blit(self.small.render(sline[:50], True, _PURPLE),
                        (bx + 6, by + 3))
            slin2 = (f"support {crisis.support}/100  ·  "
                     f"resolves d{crisis.crisis_started_day + rel.SCHISM_RESOLVE_DAYS}")
            screen.blit(self.small.render(slin2, True, _DIM_C),
                        (bx + 6, by + 17))

    def _draw_faith_orders_block(self, screen, faith, x, y, w):
        import religion as rel
        try:
            from knightly_orders import ORDERS
        except Exception:
            ORDERS = {}
        hdr = self.small.render("SWORN ORDERS", True, _LABEL_C)
        screen.blit(hdr, (x, y))
        pygame.draw.line(screen, _BORDER, (x, y + 16), (x + w, y + 16))

        adh = rel.FAITH_REGIONS.get(faith.faith_id, {})
        bonded  = []
        clashed = []
        for o in ORDERS.values():
            rid = getattr(o, "home_region", None)
            if rid is None or rid not in adh:
                continue
            primary = rel.primary_faith_of(rid)
            if primary is None or primary.faith_id != faith.faith_id:
                continue
            aff = rel.ORDER_TRADITION_DOCTRINE_AFFINITY.get(
                getattr(o, "tradition", "errant"), {"+": (), "-": ()})
            if faith.doctrine in aff["+"]:
                bonded.append(o)
            elif faith.doctrine in aff["-"]:
                clashed.append(o)

        ry = y + 22
        if not bonded and not clashed:
            screen.blit(self.small.render("(no sworn orders)", True, _DIM_C),
                        (x, ry))
            return
        for o in bonded[:3]:
            screen.blit(self.small.render(f"+ {o.name[:40]}", True, _GREEN),
                        (x, ry))
            ry += 14
        for o in clashed[:3]:
            screen.blit(self.small.render(f"- {o.name[:40]}", True, _RED),
                        (x, ry))
            ry += 14

    def _draw_faith_news_block(self, screen, faith, x, y, w):
        hdr = self.small.render("RECENT NEWSWIRE MENTIONS", True, _LABEL_C)
        screen.blit(hdr, (x, y))
        pygame.draw.line(screen, _BORDER, (x, y + 16), (x + w, y + 16))
        try:
            from industry_events import NEWSWIRE as NW
        except Exception:
            NW = []
        # Match headlines that contain the faith's name OR its head name
        needle1 = faith.name
        needle2 = faith.head_name
        hits = []
        for entry in NW:
            h = entry.get("headline", "")
            if (needle1 and needle1 in h) or (needle2 and needle2 in h):
                hits.append(entry)
            if len(hits) >= 4:
                break
        if not hits:
            screen.blit(self.small.render("(no recent mentions)", True, _DIM_C),
                        (x, y + 22))
            return
        for i, entry in enumerate(hits):
            txt = f"d{entry['day']}: {entry['headline']}"
            screen.blit(self.small.render(txt[:72], True, _LABEL_C),
                        (x, y + 22 + i * 14))

    _HIST_KIND_COLORS = {
        "founding":     (240, 215, 110),
        "schism":       (200, 130, 220),
        "crusade":      (210, 120, 90),
        "miracle":      (160, 220, 210),
        "persecution":  (210, 90, 80),
        "saint":        (235, 220, 150),
        "council":      (180, 200, 230),
        "golden_age":   (235, 200, 100),
        "scandal":      (200, 110, 130),
        "trade_pact":   (200, 180, 110),
        "famine":       (170, 140, 100),
        "founder_fast": (180, 195, 210),
        "hermitage":    (170, 175, 195),
        "vow":          (190, 195, 215),
        "plague":       (170, 130, 100),
        "grove":        (140, 195, 130),
        "harvest":      (200, 215, 130),
        "axe_riot":     (200, 100, 80),
        "library":      (200, 200, 230),
        "translation":  (190, 200, 220),
        "debate":       (180, 200, 220),
        "burning":      (220, 110, 90),
        "vision":       (200, 160, 230),
        "pilgrimage":   (220, 200, 160),
    }

    def _draw_faith_history_block(self, screen, faith, x, y, w, h):
        """Show founding + line of past heads + scrolling event list."""
        hdr = self.small.render("HISTORICAL LEDGER", True, _LABEL_C)
        screen.blit(hdr, (x, y))
        pygame.draw.line(screen, _BORDER, (x, y + 16), (x + w, y + 16))

        founded = abs(faith.founded_year) if faith.founded_year else 0
        if founded:
            head_count = len(faith.past_heads)
            f_line = (f"Founded {founded}y ago  ·  "
                      f"{head_count} successions on record")
            screen.blit(self.small.render(f_line, True, _GOLD), (x, y + 22))
        else:
            screen.blit(self.small.render("(no recorded history)", True, _DIM_C),
                        (x, y + 22))
            return

        # Show ~ last 6 events (newest first). Clipped to block height.
        ry = y + 40
        max_y = y + h
        events = list(faith.historical_events)
        events.sort(key=lambda e: -e["year"])
        line_w = w - 6
        for ev in events:
            if ry + 14 > max_y:
                break
            kind = ev.get("kind", "")
            col  = self._HIST_KIND_COLORS.get(kind, _LABEL_C)
            age  = abs(ev["year"]) if ev["year"] < 0 else 0
            prefix = f"{age}y  " if age else "today  "
            full = f"{prefix}{ev.get('text', '')}"
            ls = self.small.render(full[:80], True, col)
            screen.blit(ls, (x, ry))
            ry += 14

    # ---------------------------------------------------------------------
    # Web tab — radial graph of houses + edges
    # ---------------------------------------------------------------------

    def _draw_court_web(self, screen, player, cx, cy, cw, ch, top, bot):
        try:
            from towns import REGIONS
            from industry_events import NEWSWIRE as _NW
        except Exception:
            REGIONS = {}
            _NW = []
        visited = getattr(player, "visited_town_ids", set())
        regions = [r for r in REGIONS.values()
                   if any(tid in visited for tid in r.member_town_ids)]
        for r in regions:
            pol.seed_house_for_region(r)
        n = len(regions)
        if n == 0:
            ns = self.font.render("Visit towns to chart the political web.", True, _DIM_C)
            screen.blit(ns, (cx + (cw - ns.get_width()) // 2, top + (bot - top) // 2))
            return
        center_x = cx + cw // 2
        center_y = (top + bot) // 2 - 8
        avail_r = min(cw // 2 - 40, (bot - top) // 2 - 70)
        avail_r = max(70, avail_r)

        # Day index for pulse animation
        day = getattr(player, "_court_day_cache", 0)
        pulse_t = (pygame.time.get_ticks() % 1400) / 1400.0   # 0..1

        # Distribute nodes across one or more concentric rings so they don't pile up
        # when there are many regions. Each ring holds up to `per_ring` nodes,
        # chosen so adjacent nodes on the outer ring stay roughly 2.4 * node_r apart.
        node_r_base = 28 if n <= 8 else (22 if n <= 16 else 16)
        # Max nodes that fit on a ring of radius R with min spacing s: floor(2πR / s)
        min_spacing = node_r_base * 2.4
        per_ring = max(4, int((2 * math.pi * avail_r) / max(min_spacing, 1)))
        rings = max(1, (n + per_ring - 1) // per_ring)
        # If we need multiple rings, shrink so inner ring fits too
        ring_step = 0 if rings == 1 else max(node_r_base * 2 + 8,
                                             (avail_r - 40) // max(1, rings - 1))
        positions = {}
        node_r_for = {}
        for i, region in enumerate(regions):
            if n == 1:
                positions[region.region_id] = (center_x, center_y)
                node_r_for[region.region_id] = node_r_base
                continue
            ring = i // per_ring
            in_ring = i % per_ring
            ring_count = min(per_ring, n - ring * per_ring)
            r_here = avail_r - ring * ring_step
            ang_off = -math.pi / 2 + (ring * math.pi / max(1, per_ring))
            ang = ang_off + in_ring * 2 * math.pi / max(1, ring_count)
            positions[region.region_id] = (
                int(center_x + math.cos(ang) * r_here),
                int(center_y + math.sin(ang) * r_here),
            )
            node_r_for[region.region_id] = node_r_base

        # ── Edges (alliance/feud) — also record hit-segments for click tooltips
        self._court_web_edge_rects = []
        sel_edge = getattr(self, "_court_selected_edge", None)
        for i, ra in enumerate(regions):
            for rb in regions[i + 1:]:
                score = pol.get_relation_score(ra.region_id, rb.region_id)
                xa, ya = positions[ra.region_id]
                xb, yb = positions[rb.region_id]
                if abs(score) >= 15:
                    if score >= pol.ALLIANCE_THRESHOLD:
                        col = _GREEN; width = 3
                    elif score >= 15:
                        col = (110, 160, 110); width = 1
                    elif score <= pol.RIVAL_THRESHOLD:
                        col = _RED; width = 3
                    else:
                        col = (160, 100, 90); width = 1
                    # Hover highlight if this edge is selected
                    if sel_edge == (min(ra.region_id, rb.region_id),
                                    max(ra.region_id, rb.region_id)):
                        pygame.draw.line(screen, _GOLD, (xa, ya), (xb, yb), width + 2)
                    pygame.draw.line(screen, col, (xa, ya), (xb, yb), width)
                    mx, my = (xa + xb) // 2, (ya + yb) // 2
                    sl = self.small.render(f"{score:+d}", True, col)
                    screen.blit(sl, (mx - sl.get_width() // 2, my - 8))
                # Record segment regardless of score so the user can click neutral pairs too
                self._court_web_edge_rects.append(
                    (ra.region_id, rb.region_id, xa, ya, xb, yb))

        # ── Nodes
        self._court_web_rects = {}
        for region in regions:
            house = pol.HOUSE_STATES.get(region.region_id)
            x, y = positions[region.region_id]
            # Node radius scales with power, capped by the per-ring size
            power = house.power if house else 50
            base_r = node_r_for.get(region.region_id, 28)
            node_r = max(10, base_r - 4 + int((power / 100) * 8))
            # Agenda tint background ring
            profile = pol.agenda_profile(getattr(region, "agenda", ""))
            tint = profile["tint"]
            # Pulse on recent newswire activity (last 7 days mentioning the house)
            has_pulse = False
            if house:
                for entry in _NW[:20]:
                    if (house.name and house.name in entry.get("headline", "")
                            and day - entry.get("day", 0) <= 7):
                        has_pulse = True
                        break
            if has_pulse:
                pulse_r = node_r + 6 + int(4 * math.sin(pulse_t * 2 * math.pi))
                pygame.draw.circle(screen, _YELLOW, (x, y), pulse_r, 1)
            # Scandal halo
            if house and house.scandal > 30:
                pygame.draw.circle(screen, _RED, (x, y), node_r + 4, 2)
            # Agenda tint disc beneath sigil
            pygame.draw.circle(screen, tint, (x, y), node_r + 2)
            # Sigil
            if region.coat_of_arms:
                heraldry.draw(screen, x - node_r, y - node_r,
                              node_r * 2, node_r * 2, region.coat_of_arms)
            else:
                pygame.draw.circle(screen, (60, 55, 45), (x, y), node_r)
            sel = (getattr(self, "_court_selected_rid", None) == region.region_id)
            pygame.draw.circle(screen, _GOLD if sel else _BORDER,
                               (x, y), node_r, 2 if sel else 1)
            # Backing-guild dots around the node (max 6)
            guilds = pol.backing_guilds(region.region_id)
            for gi, g in enumerate(guilds[:6]):
                ang = -math.pi / 2 + gi * (2 * math.pi / 6)
                gx = int(x + math.cos(ang) * (node_r + 10))
                gy = int(y + math.sin(ang) * (node_r + 10))
                pygame.draw.circle(screen, _BLUE, (gx, gy), 3)
                pygame.draw.circle(screen, _VDIM_C, (gx, gy), 3, 1)
            # Name below
            name = house.name if house else region.name
            ns = self.small.render(name[:18], True, _LABEL_C)
            screen.blit(ns, (x - ns.get_width() // 2, y + node_r + 6))
            # Power score badge under name
            if house:
                pws = self.small.render(f"P{house.power}", True, _DIM_C)
                screen.blit(pws, (x - pws.get_width() // 2, y + node_r + 20))
            # Posture arrow above
            arrow, acol = _posture_arrow(house.posture if house else "stable")
            ar = self.font.render(arrow, True, acol)
            screen.blit(ar, (x - ar.get_width() // 2, y - node_r - 20))
            # Hit rect for node clicks
            self._court_web_rects[region.region_id] = pygame.Rect(
                x - node_r, y - node_r, node_r * 2, node_r * 2)

        # ── Selected-edge reason tooltip (bottom of view)
        if sel_edge is not None:
            a, b = sel_edge
            ha = pol.HOUSE_STATES.get(a); hb = pol.HOUSE_STATES.get(b)
            reasons = pol.relation_reasons(a, b)
            score = pol.get_relation_score(a, b)
            label = f"{ha.name if ha else a}  ↔  {hb.name if hb else b}  ({score:+d})"
            tip_y = bot - 78
            pygame.draw.rect(screen, _PANEL_BG, (cx + 14, tip_y, cw - 28, 64))
            pygame.draw.rect(screen, _GOLD, (cx + 14, tip_y, cw - 28, 64), 1)
            ts = self.small.render(label, True, _TITLE_C)
            screen.blit(ts, (cx + 22, tip_y + 4))
            if reasons:
                for i, r in enumerate(reasons[:3]):
                    rs = self.small.render(
                        f"d{r.get('day', 0):>4}  [{r.get('kind','')}]  {r.get('note','')}"[:80],
                        True, _LABEL_C)
                    screen.blit(rs, (cx + 22, tip_y + 22 + i * 14))
            else:
                ns = self.small.render(
                    "No recorded incidents — relations are coasting.", True, _DIM_C)
                screen.blit(ns, (cx + 22, tip_y + 28))

        # Footer
        legend = ("● Allied   ● Rival   ●●● Backing guilds   ↑↓! Posture   "
                  "Click sigil → deep panel   Click edge → reason")
        fs = self.small.render(legend, True, _DIM_C)
        screen.blit(fs, (cx + (cw - fs.get_width()) // 2, bot - 14))

    # ---------------------------------------------------------------------
    # Newswire tab — list of headlines (reuses industry_events.NEWSWIRE)
    # ---------------------------------------------------------------------

    def _draw_court_news(self, screen, player, cx, cy, cw, ch, top, bot):
        try:
            from industry_events import NEWSWIRE
        except Exception:
            NEWSWIRE = []
        if not NEWSWIRE:
            ns = self.font.render("Newswire empty — give the world a day or two.", True, _DIM_C)
            screen.blit(ns, (cx + (cw - ns.get_width()) // 2, top + (bot - top) // 2))
            return
        row_h = 22
        total_h = len(NEWSWIRE) * row_h + 14
        content_h = bot - top
        self._court_max_scroll = max(0, total_h - content_h)
        scroll = max(0, min(getattr(self, "_court_scroll", 0), self._court_max_scroll))
        self._court_scroll = scroll
        old_clip = screen.get_clip()
        screen.set_clip(pygame.Rect(cx, top, cw, content_h))
        y = top + 8 - scroll
        kind_color = {
            "politics": _PURPLE, "scandal": _RED, "rivalry": (210, 140, 80),
            "event": _BLUE, "tournament": _GOLD,
        }
        for entry in NEWSWIRE:
            if y + row_h < top:
                y += row_h; continue
            if y > bot:
                break
            kind = entry.get("kind", "event")
            col = kind_color.get(kind, _LABEL_C)
            tag = self.small.render(f"[{kind[:4]}]", True, col)
            screen.blit(tag, (cx + 14, y))
            day = entry.get("day", 0)
            ds = self.small.render(f"d{day:>4}", True, _DIM_C)
            screen.blit(ds, (cx + 14 + 50, y))
            hs = self.small.render(entry.get("headline", ""), True, _LABEL_C)
            screen.blit(hs, (cx + 14 + 100, y))
            y += row_h
        screen.set_clip(old_clip)
        self._draw_court_scrollbar(screen, cx, top, cw, content_h)

    # ---------------------------------------------------------------------
    # Orders tab
    # ---------------------------------------------------------------------

    def _draw_court_orders(self, screen, player, cx, cy, cw, ch, top, bot):
        try:
            from knightly_orders import ORDERS
            from towns import REGIONS
        except Exception:
            ORDERS, REGIONS = {}, {}
        visited = getattr(player, "visited_town_ids", set())
        visible_orders = []
        for o in ORDERS.values():
            region = REGIONS.get(o.home_region)
            if region is None:
                continue
            if not any(tid in visited for tid in region.member_town_ids):
                continue
            visible_orders.append((o, region))
        if not visible_orders:
            ns = self.font.render("No orders known.", True, _DIM_C)
            screen.blit(ns, (cx + (cw - ns.get_width()) // 2, top + (bot - top) // 2))
            return
        row_h = 56
        total_h = len(visible_orders) * row_h + 14
        content_h = bot - top
        self._court_max_scroll = max(0, total_h - content_h)
        scroll = max(0, min(getattr(self, "_court_scroll", 0), self._court_max_scroll))
        self._court_scroll = scroll
        old_clip = screen.get_clip()
        screen.set_clip(pygame.Rect(cx, top, cw, content_h))
        self._court_order_rects = {}
        y = top + 8 - scroll
        for o, region in visible_orders:
            if y + row_h < top:
                y += row_h; continue
            if y > bot:
                break
            x = cx + 14
            pygame.draw.rect(screen, _PANEL_BG, (x, y, cw - 28, row_h - 6))
            pygame.draw.rect(screen, _BORDER, (x, y, cw - 28, row_h - 6), 1)
            if o.heraldry:
                heraldry.draw(screen, x + 4, y + 4, 36, 44, o.heraldry)
            ns = self.small.render(o.name[:38], True, _TITLE_C)
            screen.blit(ns, (x + 48, y + 4))
            sub = f"{o.tradition.title()}  ·  {region.name}  ·  Prestige {o.prestige}"
            ss = self.small.render(sub, True, _LABEL_C)
            screen.blit(ss, (x + 48, y + 20))
            # Sworn-to + player pledge
            sworn = ""
            if region.region_id in (o.kingdom_alignment or {}):
                state = o.kingdom_alignment[region.region_id]
                sworn = f"Aligned: {state.title()}"
            pledged_rid = pol.PLAYER_PLEDGES.get(o.order_id)
            pledge_str = ""
            if pledged_rid is not None:
                ph = pol.HOUSE_STATES.get(pledged_rid)
                pledge_str = f"  ·  Pledged to {ph.name if ph else 'a house'}"
            if sworn or pledge_str:
                ws = self.small.render(sworn + pledge_str, True, _GOLD)
                screen.blit(ws, (x + 48, y + 36))
            self._court_order_rects[o.order_id] = pygame.Rect(
                x, y, cw - 28, row_h - 6)
            y += row_h
        screen.set_clip(old_clip)
        self._draw_court_scrollbar(screen, cx, top, cw, content_h)

    # ---------------------------------------------------------------------
    # Actions tab — six manipulation verbs targeting selected house
    # ---------------------------------------------------------------------

    def _draw_court_actions(self, screen, player, cx, cy, cw, ch, top, bot):
        rid = getattr(self, "_court_selected_rid", None)
        if rid is None:
            ns = self.font.render("Select a house first (Houses or Web tab).", True, _DIM_C)
            screen.blit(ns, (cx + (cw - ns.get_width()) // 2, top + (bot - top) // 2))
            return
        house = pol.HOUSE_STATES.get(rid)
        if house is None:
            return
        # Header — target house summary
        hx = cx + 18
        hy = top + 8
        ns = self.font.render(f"Target: {house.name}", True, _TITLE_C)
        screen.blit(ns, (hx, hy))
        infl = pol.get_influence(rid)
        tier_label, tcol = pol.influence_tier(infl)
        its = self.small.render(f"  Your standing: {tier_label} ({infl:+d})", True, tcol)
        screen.blit(its, (hx + ns.get_width() + 6, hy + 4))
        # Stat ribbon
        sy = hy + 28
        ribbon = (f"Power {house.power}   Prestige {house.prestige}   "
                  f"Scandal {house.scandal}   Posture {house.posture.title()}   "
                  f"Treasury {house.treasury}g")
        rs = self.small.render(ribbon, True, _LABEL_C)
        screen.blit(rs, (hx, sy))

        # Action list
        money = getattr(player, "money", 0)
        crisis = pol.SUCCESSION.get(rid)
        in_crisis = crisis is not None and not crisis.resolved
        actions = []
        bribe_cost = pol.BRIBE_BASE_COST + house.power * 12
        actions.append((
            "Bribe Official",
            f"{bribe_cost}g · +8-13 influence with this house's officials.",
            money >= bribe_cost,
            "bribe", None,
        ))
        actions.append((
            "Sponsor Heir",
            (f"{pol.SPONSOR_HEIR_COST}g + 1 dynasty heir-token · back a contender "
             f"({len(crisis.contenders) if in_crisis else 0} active)."),
            in_crisis and money >= pol.SPONSOR_HEIR_COST,
            "sponsor_heir", None,
        ))
        # Broker marriage needs a second house — pick the highest-influence other
        partner_rid = self._pick_marriage_partner(rid)
        partner_house = pol.HOUSE_STATES.get(partner_rid) if partner_rid else None
        marriage_label = f"Broker Marriage → {partner_house.name}" if partner_house else "Broker Marriage"
        marriage_ok = (partner_rid is not None
                       and pol.get_influence(rid) >= 20
                       and pol.get_influence(partner_rid) >= 20
                       and money >= pol.BROKER_MARRIAGE_COST)
        actions.append((
            marriage_label,
            f"{pol.BROKER_MARRIAGE_COST}g · needs Recognized+ in both houses.",
            marriage_ok,
            "broker_marriage", partner_rid,
        ))
        # Fund rivalry — pick best rival
        rival_rid = self._pick_rival(rid)
        rival_house = pol.HOUSE_STATES.get(rival_rid) if rival_rid else None
        fund_label = f"Fund Rivalry vs {rival_house.name}" if rival_house else "Fund Rivalry"
        fund_ok = (rival_rid is not None and money >= pol.FUND_RIVALRY_COST
                   and len(pol.backing_guilds(rid)) > 0)
        actions.append((
            fund_label,
            f"{pol.FUND_RIVALRY_COST}g · empowers this house's guilds to sabotage a rival for 7 days.",
            fund_ok,
            "fund_rivalry", rival_rid,
        ))
        # Leak scandal
        inv = getattr(player, "inventory", {})
        has_evidence = any(isinstance(k, str) and k.startswith("dynasty_") and inv.get(k, 0) > 0 for k in inv)
        actions.append((
            "Leak Scandal",
            "1 dynasty heirloom as evidence · scandal +30, power -10, you lose standing.",
            has_evidence,
            "leak_scandal", None,
        ))
        # Pledge order — pick an order in this region
        pledge_order_id = self._pick_pledgeable_order(rid)
        try:
            from knightly_orders import ORDERS
            pledge_order = ORDERS.get(pledge_order_id) if pledge_order_id else None
        except Exception:
            pledge_order = None
        pledge_label = f"Pledge {pledge_order.name}" if pledge_order else "Pledge Order"
        actions.append((
            pledge_label,
            "Sworn this order to the house (locks future rival pledges in region).",
            pledge_order_id is not None,
            "pledge_order", pledge_order_id,
        ))
        # ── Five new verbs ────────────────────────────────────────────────
        actions.append((
            "Spread Rumor",
            f"{pol.SPREAD_RUMOR_COST}g · cheap +5 scandal (30% trace risk; no evidence needed).",
            money >= pol.SPREAD_RUMOR_COST,
            "spread_rumor", None,
        ))
        actions.append((
            "Endow Monastery",
            f"{pol.ENDOW_MONASTERY_COST}g · +8 prestige, -6 scandal, +12 influence (pious houses bonus).",
            money >= pol.ENDOW_MONASTERY_COST,
            "endow_monastery", None,
        ))
        n_orders = len(pol.backing_orders(rid))
        actions.append((
            "Arrange Tournament",
            f"{pol.ARRANGE_TOURNAMENT_COST}g · {n_orders} regional orders +5 prestige; house +6; you +10 standing.",
            n_orders > 0 and money >= pol.ARRANGE_TOURNAMENT_COST,
            "arrange_tournament", None,
        ))
        actions.append((
            "Send Envoy",
            f"{pol.SEND_ENVOY_COST}g · reveals hidden agenda, treasury net, contender support, scandal recency.",
            money >= pol.SEND_ENVOY_COST,
            "send_envoy", None,
        ))
        actions.append((
            "Demand Hostage",
            f"Free · requires Court Favored (+40) and 90-day cooldown; +30 influence, -20 prestige.",
            infl >= 40,
            "demand_hostage", None,
        ))

        # Render
        self._court_action_rects = []
        ay = sy + 28
        row_h = 50
        for label, desc, enabled, action_id, extra in actions:
            r = pygame.Rect(hx, ay, cw - 40, row_h - 6)
            bg = (40, 38, 30) if enabled else (24, 22, 18)
            brd = _GOLD if enabled else _VDIM_C
            pygame.draw.rect(screen, bg, r); pygame.draw.rect(screen, brd, r, 1)
            lc = _TITLE_C if enabled else _DIM_C
            ls = self.small.render(label, True, lc)
            screen.blit(ls, (r.x + 10, r.y + 6))
            ds = self.small.render(desc[:120], True, _LABEL_C if enabled else _VDIM_C)
            screen.blit(ds, (r.x + 10, r.y + 24))
            self._court_action_rects.append((r, action_id, extra, enabled))
            ay += row_h
        # Last-action result
        msg = getattr(self, "_court_last_msg", "")
        if msg:
            ms = self.small.render(msg[:140], True, _YELLOW)
            screen.blit(ms, (cx + (cw - ms.get_width()) // 2, bot - 18))

    def _pick_marriage_partner(self, rid: int):
        try:
            from towns import REGIONS
        except Exception:
            return None
        best = None
        best_score = -999
        for r in REGIONS.values():
            if r.region_id == rid:
                continue
            if r.region_id not in pol.HOUSE_STATES:
                continue
            score = pol.get_influence(r.region_id)
            if pol.get_relation_score(rid, r.region_id) < pol.RIVAL_THRESHOLD:
                continue
            if score > best_score:
                best_score = score
                best = r.region_id
        return best

    def _pick_rival(self, rid: int):
        try:
            from towns import REGIONS
        except Exception:
            return None
        best = None
        best_score = 0
        for r in REGIONS.values():
            if r.region_id == rid:
                continue
            s = pol.get_relation_score(rid, r.region_id)
            if s < best_score:
                best_score = s
                best = r.region_id
        # If no actual rival exists yet, pick any other house
        if best is None:
            for r in REGIONS.values():
                if r.region_id != rid and r.region_id in pol.HOUSE_STATES:
                    return r.region_id
        return best

    def _pick_pledgeable_order(self, rid: int):
        for o in pol.backing_orders(rid):
            if pol.PLAYER_PLEDGES.get(o.order_id) is None:
                return o.order_id
        return None

    # ---------------------------------------------------------------------
    # Scrollbar helper
    # ---------------------------------------------------------------------

    def _draw_court_scrollbar(self, screen, cx, top, cw, content_h):
        mx = getattr(self, "_court_max_scroll", 0)
        if mx <= 0:
            return
        sb_x = cx + cw - 10
        thumb_h = max(28, int(content_h * content_h / (content_h + mx)))
        scroll = getattr(self, "_court_scroll", 0)
        thumb_y = top + int((content_h - thumb_h) * scroll / mx)
        pygame.draw.rect(screen, (38, 35, 28), (sb_x, top, 6, content_h))
        pygame.draw.rect(screen, _BORDER, (sb_x, thumb_y, 6, thumb_h))

    # ---------------------------------------------------------------------
    # Click + scroll handlers (called by ReputationScreenMixin)
    # ---------------------------------------------------------------------

    def handle_court_tab_click(self, pos) -> bool:
        for key, rect in getattr(self, "_court_tab_rects", {}).items():
            if rect.collidepoint(pos):
                self.set_court_tab(key)
                return True
        return False

    def handle_court_content_click(self, pos, player, world) -> bool:
        tab = self.get_court_tab()
        # Cache day on player for the deep panel to reach
        if player is not None and world is not None:
            player._court_day_cache = getattr(world, "day_count", 0)
        if tab == "houses":
            # If deep panel is open, only the back button is clickable
            if getattr(self, "_court_house_panel_rid", None) is not None:
                back = getattr(self, "_court_back_btn", None)
                if back and back.collidepoint(pos):
                    self._court_house_panel_rid = None
                    return True
                return False
            for rid, rect in getattr(self, "_court_house_rects", {}).items():
                if rect.collidepoint(pos):
                    self._court_selected_rid = rid
                    self._court_house_panel_rid = rid
                    return True
        elif tab == "faiths":
            if getattr(self, "_court_faith_panel_fid", None) is not None:
                back = getattr(self, "_court_back_btn", None)
                if back and back.collidepoint(pos):
                    self._court_faith_panel_fid = None
                    return True
                return False
            for fid, rect in getattr(self, "_court_faith_rects", {}).items():
                if rect.collidepoint(pos):
                    self._court_selected_fid = fid
                    self._court_faith_panel_fid = fid
                    return True
        elif tab == "web":
            # Nodes first (smaller hit area than edges so they win ties)
            for rid, rect in getattr(self, "_court_web_rects", {}).items():
                if rect.collidepoint(pos):
                    self._court_selected_rid = rid
                    # In Web view, single click on a node opens the deep panel
                    # via the Houses tab — switch and pop it.
                    self.set_court_tab("houses")
                    self._court_house_panel_rid = rid
                    return True
            # Then edges
            px, py = pos
            for a, b, x1, y1, x2, y2 in getattr(self, "_court_web_edge_rects", []):
                if _point_near_segment(px, py, x1, y1, x2, y2, tol=8):
                    self._court_selected_edge = (min(a, b), max(a, b))
                    return True
            self._court_selected_edge = None
        elif tab == "actions":
            for rect, action_id, extra, enabled in getattr(self, "_court_action_rects", []):
                if rect.collidepoint(pos) and enabled:
                    self._invoke_court_action(action_id, extra, player, world)
                    return True
        elif tab == "orders":
            for oid, rect in getattr(self, "_court_order_rects", {}).items():
                if rect.collidepoint(pos):
                    self._court_selected_order_id = oid
                    return True
        return False

    def handle_court_scroll(self, dy) -> None:
        mx = getattr(self, "_court_max_scroll", 0)
        if mx <= 0:
            return
        self._court_scroll = max(0, min(
            getattr(self, "_court_scroll", 0) + dy, mx))

    def _invoke_court_action(self, action_id, extra, player, world):
        rid = getattr(self, "_court_selected_rid", None)
        if rid is None:
            return
        day = getattr(world, "day_count", 0)
        ok, msg, cost = False, "", 0
        if action_id == "bribe":
            ok, msg, cost = pol.action_bribe_official(player, rid, day)
        elif action_id == "sponsor_heir":
            ok, msg, cost = pol.action_sponsor_heir(player, rid, day)
        elif action_id == "broker_marriage" and extra is not None:
            ok, msg, cost = pol.action_broker_marriage(player, rid, extra, day)
        elif action_id == "fund_rivalry" and extra is not None:
            ok, msg, cost = pol.action_fund_rivalry(player, rid, extra, day)
        elif action_id == "leak_scandal":
            ok, msg, cost = pol.action_leak_scandal(player, rid, day)
        elif action_id == "pledge_order" and extra is not None:
            ok, msg, cost = pol.action_pledge_order(player, extra, rid, day)
        elif action_id == "spread_rumor":
            ok, msg, cost = pol.action_spread_rumor(player, rid, day)
        elif action_id == "endow_monastery":
            ok, msg, cost = pol.action_endow_monastery(player, rid, day)
        elif action_id == "arrange_tournament":
            ok, msg, cost = pol.action_arrange_tournament(player, rid, day)
        elif action_id == "send_envoy":
            ok, msg, cost = pol.action_send_envoy(player, rid, day)
        elif action_id == "demand_hostage":
            ok, msg, cost = pol.action_demand_hostage(player, rid, day)
        if ok and cost > 0:
            player.money = max(0, getattr(player, "money", 0) - cost)
        self._court_last_msg = msg
