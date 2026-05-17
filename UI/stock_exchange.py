"""Stock Exchange UI — Market and Portfolio tabs (Phase 1).

Phase 2+ will add Board Room and Charter tabs gated on research tiers and
ownership thresholds.
"""

import pygame

from guilds import (
    GUILDS, CHAPTERS, SHARE_HOLDINGS, INDUSTRY_DISPLAY,
    active_guilds,
    buy_shares, sell_shares,
    found_player_guild, buyback_shares, issue_shares,
    npc_holdings_for,
    open_short, close_short, player_short,
    borrow, repay, portfolio_value,
    FOUNDING_FEE, FOUNDING_FEE_PER_SHARE,
)
from bonds import BONDS, buy_bond, player_bonds, float_bonds
from guild_policies import (
    OWNERSHIP_FINANCIALS, OWNERSHIP_BOARD_SEAT, OWNERSHIP_MAJORITY,
    OWNERSHIP_SUBSIDIARY, player_tier,
)

# Palette — matches the bazaar look.
_BG        = (20, 15, 10)
_PANEL     = (42, 30, 18)
_BORDER    = (100, 72, 42)
_HEADER_BG = (55, 38, 20)
_ROW_BG    = (32, 24, 14)
_ROW_ALT   = (28, 21, 12)
_GOLD      = (210, 170, 55)
_SAND      = (185, 155, 100)
_MUTED     = (130, 110, 80)
_GAIN      = (100, 200, 100)
_LOSS      = (220, 90, 70)
_TAB_SEL   = (95, 70, 35)
_TAB_IDLE  = (50, 38, 22)

_PANEL_W = 760
_PANEL_H = 520
_ROW_H   = 32
_TAB_H   = 28


class StockExchangeMixin:

    # ------------------------------------------------------------------
    # Open / state
    # ------------------------------------------------------------------

    def open_stock_exchange(self, research=None, focus_guild_id=None):
        self.stock_exchange_open = True
        self._stock_tab          = "market"   # market | portfolio | board | charter
        self._stock_selected_gid = focus_guild_id
        self._stock_buy_qty      = 1
        self._stock_status_msg   = ""
        self._stock_rects        = {}
        self._stock_scroll       = 0
        self._stock_research     = research
        # Charter wizard state
        self._charter_step       = 0
        self._charter_name       = ""
        self._charter_industry   = None
        self._charter_region_id  = None
        self._charter_share_count = 1000
        self._charter_ipo_price  = 10.0
        self._charter_float_pct  = 0.40
        self._charter_name_editing = False
        # Buyback/dilution quantity
        self._board_action_qty   = 10

    # ------------------------------------------------------------------
    # Top-level draw
    # ------------------------------------------------------------------

    def _draw_stock_exchange(self, player):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        sw, sh = self.screen.get_size()
        pw, ph = _PANEL_W, _PANEL_H
        px = (sw - pw) // 2
        py = (sh - ph) // 2

        pygame.draw.rect(self.screen, _BG,     (px, py, pw, ph), border_radius=6)
        pygame.draw.rect(self.screen, _BORDER, (px, py, pw, ph), 2, border_radius=6)
        pygame.draw.rect(self.screen, _PANEL,  (px + 10, py + 10, pw - 20, ph - 20), border_radius=4)

        title_strip = pygame.Rect(px + 10, py + 10, pw - 20, 28)
        pygame.draw.rect(self.screen, _HEADER_BG, title_strip, border_radius=4)
        title = self.font.render("STOCK EXCHANGE", True, _GOLD)
        self.screen.blit(title, (px + pw // 2 - title.get_width() // 2, py + 15))

        gold_s = self.small.render(f"Gold: {getattr(player, 'money', 0)}g", True, _SAND)
        self.screen.blit(gold_s, (px + pw - gold_s.get_width() - 20, py + 18))

        self._stock_rects = {}
        self._draw_stock_tabs(px, py, pw)
        content_rect = pygame.Rect(px + 14, py + 50 + _TAB_H, pw - 28, ph - 70 - _TAB_H)

        if self._stock_tab == "market":
            self._draw_stock_market(player, content_rect)
        elif self._stock_tab == "portfolio":
            self._draw_stock_portfolio(player, content_rect)
        elif self._stock_tab == "history":
            self._draw_stock_history(player, content_rect)
        elif self._stock_tab == "board":
            self._draw_stock_board_room(player, content_rect)
        else:
            self._draw_stock_charter(player, content_rect)

        if self._stock_status_msg:
            msg = self.small.render(self._stock_status_msg, True, _SAND)
            self.screen.blit(msg, (px + 14, py + ph - 24))

        close_r = pygame.Rect(px + pw - 70, py + ph - 30, 56, 22)
        pygame.draw.rect(self.screen, _TAB_IDLE, close_r, border_radius=3)
        pygame.draw.rect(self.screen, _BORDER,   close_r, 1, border_radius=3)
        cs = self.small.render("Close", True, _SAND)
        self.screen.blit(cs, (close_r.centerx - cs.get_width() // 2,
                              close_r.centery - cs.get_height() // 2))
        self._stock_rects["close"] = close_r

    # ------------------------------------------------------------------
    # Tab bar
    # ------------------------------------------------------------------

    def _draw_stock_tabs(self, px, py, pw):
        tabs = [("market", "Market"), ("portfolio", "Portfolio"),
                ("history", "History")]
        if self._board_view_unlocked():
            tabs.append(("board", "Board Room"))
        if self._charter_unlocked():
            tabs.append(("charter", "Charter"))
        x = px + 14
        for key, label in tabs:
            sel = (self._stock_tab == key)
            r = pygame.Rect(x, py + 48, 110, _TAB_H)
            pygame.draw.rect(self.screen, _TAB_SEL if sel else _TAB_IDLE, r, border_radius=3)
            pygame.draw.rect(self.screen, _BORDER, r, 1, border_radius=3)
            s = self.small.render(label, True, _GOLD if sel else _SAND)
            self.screen.blit(s, (r.centerx - s.get_width() // 2,
                                 r.centery - s.get_height() // 2))
            self._stock_rects[("tab", key)] = r
            x += 116

    # ------------------------------------------------------------------
    # Market tab
    # ------------------------------------------------------------------

    def _draw_stock_market(self, player, rect):
        _state_rank = {"active": 0, "distressed": 1, "bankrupt": 2}
        guilds_list = sorted(
            GUILDS.values(),
            key=lambda g: (_state_rank.get(g.state, 3), -g.share_price, g.name))
        # Reserve the bottom strip for the newswire log.
        newswire_h = 76
        newswire_rect = pygame.Rect(rect.x, rect.bottom - newswire_h, rect.w, newswire_h)
        rect = pygame.Rect(rect.x, rect.y, rect.w, rect.h - newswire_h - 6)
        self._draw_newswire(newswire_rect)
        if not guilds_list:
            s = self.small.render("No guilds active in this world yet — explore to discover regional outposts.", True, _MUTED)
            self.screen.blit(s, (rect.x, rect.y + 8))
            return

        # Header row
        hdr_y = rect.y
        self._draw_market_header(rect.x, hdr_y, rect.w)

        # Split: list on left, detail on right
        list_w   = int(rect.w * 0.55)
        detail_x = rect.x + list_w + 12
        detail_w = rect.w - list_w - 12

        list_rect = pygame.Rect(rect.x, hdr_y + 22, list_w, rect.h - 22)
        self._draw_market_list(guilds_list, list_rect)

        if self._stock_selected_gid is None and guilds_list:
            self._stock_selected_gid = guilds_list[0].guild_id

        sel = GUILDS.get(self._stock_selected_gid)
        if sel is not None:
            self._draw_market_detail(player, sel,
                                     pygame.Rect(detail_x, hdr_y, detail_w, rect.h))

    def _draw_market_header(self, x, y, w):
        cols = [("Guild", 0), ("Industry", int(w * 0.42)),
                ("Price", int(w * 0.65)), ("Δ%", int(w * 0.82))]
        for label, off in cols:
            s = self.small.render(label, True, _MUTED)
            self.screen.blit(s, (x + off, y))

    def _draw_market_list(self, guilds_list, rect):
        max_rows = rect.h // _ROW_H
        max_scroll = max(0, len(guilds_list) - max_rows)
        self._stock_scroll = max(0, min(self._stock_scroll, max_scroll))

        for i, g in enumerate(guilds_list[self._stock_scroll:self._stock_scroll + max_rows]):
            row_y = rect.y + i * _ROW_H
            row_r = pygame.Rect(rect.x, row_y, rect.w, _ROW_H - 2)
            bg = _ROW_BG if i % 2 == 0 else _ROW_ALT
            if g.guild_id == self._stock_selected_gid:
                bg = _HEADER_BG
            pygame.draw.rect(self.screen, bg, row_r, border_radius=3)

            name_color = _SAND if g.state == "active" else _MUTED
            name_s = self.small.render(g.name[:32], True, name_color)
            self.screen.blit(name_s, (row_r.x + 6, row_r.y + 7))

            industry_label = INDUSTRY_DISPLAY.get(g.industry, g.industry)
            if g.state != "active":
                industry_label = f"{industry_label}  ·  {g.state.upper()}"
            ind_s = self.small.render(industry_label, True, _MUTED)
            self.screen.blit(ind_s, (row_r.x + int(rect.w * 0.42), row_r.y + 7))

            price_color = _GOLD if g.state == "active" else _MUTED
            price_s = self.small.render(f"{g.share_price:6.2f}g", True, price_color)
            self.screen.blit(price_s, (row_r.x + int(rect.w * 0.65), row_r.y + 7))

            delta = _price_delta_pct(g)
            color = _GAIN if delta >= 0 else _LOSS
            delta_s = self.small.render(f"{delta:+5.1f}%", True, color)
            self.screen.blit(delta_s, (row_r.x + int(rect.w * 0.82), row_r.y + 7))

            self._stock_rects[("select", g.guild_id)] = row_r

    def _draw_market_detail(self, player, g, rect):
        pygame.draw.rect(self.screen, _ROW_BG, rect, border_radius=4)
        pygame.draw.rect(self.screen, _BORDER, rect, 1, border_radius=4)

        # Title
        title = self.font.render(g.name, True, _GOLD)
        self.screen.blit(title, (rect.x + 10, rect.y + 8))
        sub = self.small.render(INDUSTRY_DISPLAY.get(g.industry, g.industry), True, _MUTED)
        self.screen.blit(sub, (rect.x + 10, rect.y + 30))

        # Stats grid
        stats = [
            ("Share price",   f"{g.share_price:.2f}g"),
            ("Outstanding",   f"{g.share_count}"),
            ("Market cap",    f"{g.market_cap()}g"),
            ("Treasury",      f"{g.treasury}g"),
            ("Last week P/L", f"{g.last_week_profit:+}g"),
            ("Dividend rate", f"{g.dividend_rate*100:.1f}%"),
            ("Status",        g.state),
        ]
        if self._insider_unlocked():
            from stock_market import forecast_target
            fc = forecast_target(g)
            delta = (fc - g.share_price) / max(g.share_price, 0.01) * 100.0
            stats.append(("Forecast (insider)", f"{fc:.2f}g  ({delta:+.1f}%)"))
        y = rect.y + 56
        for label, val in stats:
            ls = self.small.render(label, True, _MUTED)
            vs = self.small.render(val, True, _SAND)
            self.screen.blit(ls, (rect.x + 10, y))
            self.screen.blit(vs, (rect.x + rect.w - vs.get_width() - 12, y))
            y += 18

        # Active industry effects ribbon
        if g.active_effects:
            y += 4
            eff_label = "  ·  ".join(
                f"{eff.get('note', '?')} ×{eff.get('mult', 1.0):.2f} ({eff.get('days_left', 0)}d)"
                for eff in g.active_effects)
            color = _LOSS if any(eff.get("mult", 1.0) < 1.0 for eff in g.active_effects) else _GAIN
            eff_s = self.small.render(eff_label[:80], True, color)
            self.screen.blit(eff_s, (rect.x + 10, y))
            y += 18

        # Heritage line — surfaces worldgen-era backstory so buyers see "this
        # is a 380-year-old House Voss guild" without leaving the Market tab.
        if g.founded_year or g.historical_ledger:
            age_label = (f"Est. yr {g.founded_year}  ·  "
                         f"{len(g.historical_ledger)}yr ledger" if g.founded_year
                         else "Recent charter")
            if g.founder_house:
                age_label += f"  ·  {g.founder_house[:24]}"
            self.screen.blit(self.small.render(age_label, True, _MUTED),
                             (rect.x + 10, y))
            y += 16
            if g.historical_ledger:
                prices = [r.share_price for r in g.historical_ledger]
                hi = max(prices); lo = min(prices)
                crashes = sum(1 for r in g.historical_ledger
                              if r.event in ("sacked", "plague", "collapse",
                                             "earthquake", "civil_war",
                                             "founder_extinct"))
                hist_line = f"All-time {lo:.1f}g..{hi:.1f}g  ·  {crashes} crash(es) on record"
                color = _LOSS if crashes >= 3 else _SAND
                self.screen.blit(self.small.render(hist_line, True, color),
                                 (rect.x + 10, y))
                y += 16

        # Sparkline
        spark_rect = pygame.Rect(rect.x + 10, y + 6, rect.w - 20, 64)
        pygame.draw.rect(self.screen, _BG, spark_rect, border_radius=3)
        pygame.draw.rect(self.screen, _BORDER, spark_rect, 1, border_radius=3)
        _draw_sparkline(self.screen, list(g.price_history), spark_rect)

        # Player holding line
        h = player_holding(g.guild_id)
        held = h.shares if h else 0
        avg  = h.avg_buy_price if h else 0.0
        pl   = (g.share_price - avg) * held if h else 0.0
        hold_s = self.small.render(
            f"You own: {held} share(s) @ avg {avg:.2f}g    P/L: {pl:+.0f}g",
            True, _SAND)
        self.screen.blit(hold_s, (rect.x + 10, spark_rect.bottom + 8))

        # Trade controls
        ctl_y = spark_rect.bottom + 32
        qty_label = self.small.render(f"Qty: {self._stock_buy_qty}", True, _SAND)
        self.screen.blit(qty_label, (rect.x + 10, ctl_y + 4))

        def _btn(label, key, x, color=_TAB_IDLE):
            r = pygame.Rect(x, ctl_y, 36, 22)
            pygame.draw.rect(self.screen, color, r, border_radius=3)
            pygame.draw.rect(self.screen, _BORDER, r, 1, border_radius=3)
            s = self.small.render(label, True, _SAND)
            self.screen.blit(s, (r.centerx - s.get_width() // 2,
                                 r.centery - s.get_height() // 2))
            self._stock_rects[key] = r

        _btn("-1",  "qty_-1",  rect.x + 80)
        _btn("+1",  "qty_+1",  rect.x + 120)
        _btn("+10", "qty_+10", rect.x + 160)
        _btn("Max", "qty_max", rect.x + 200)

        buy_r   = pygame.Rect(rect.x + 10,  ctl_y + 30, 88, 26)
        sell_r  = pygame.Rect(rect.x + 104, ctl_y + 30, 88, 26)
        short_r = pygame.Rect(rect.x + 198, ctl_y + 30, 88, 26)
        sh = player_short(g.guild_id)
        short_label = "Cover" if sh else "Short"
        pygame.draw.rect(self.screen, (60, 110, 60),  buy_r,   border_radius=3)
        pygame.draw.rect(self.screen, (110, 60, 60),  sell_r,  border_radius=3)
        pygame.draw.rect(self.screen, (110, 90, 130), short_r, border_radius=3)
        for r in (buy_r, sell_r, short_r):
            pygame.draw.rect(self.screen, _BORDER, r, 1, border_radius=3)
        bs = self.small.render(f"Buy ({int(g.share_price * self._stock_buy_qty)}g)",  True, (240, 240, 230))
        ss = self.small.render(f"Sell ({int(g.share_price * self._stock_buy_qty)}g)", True, (240, 240, 230))
        sho = self.small.render(short_label, True, (240, 240, 230))
        self.screen.blit(bs,  (buy_r.centerx  - bs.get_width()  // 2, buy_r.centery  - bs.get_height()  // 2))
        self.screen.blit(ss,  (sell_r.centerx - ss.get_width()  // 2, sell_r.centery - ss.get_height()  // 2))
        self.screen.blit(sho, (short_r.centerx - sho.get_width()// 2, short_r.centery - sho.get_height()// 2))
        self._stock_rects["buy"]   = buy_r
        self._stock_rects["sell"]  = sell_r
        self._stock_rects["short"] = short_r

    # ------------------------------------------------------------------
    # Portfolio tab
    # ------------------------------------------------------------------

    def _draw_stock_portfolio(self, player, rect):
        # Reserve right column for Finance (shorts + bonds + loan)
        left_w = int(rect.w * 0.60)
        left   = pygame.Rect(rect.x, rect.y, left_w, rect.h)
        right  = pygame.Rect(rect.x + left_w + 8, rect.y, rect.w - left_w - 8, rect.h)
        self._draw_portfolio_finance(player, right)
        rect = left
        holdings = [h for h in SHARE_HOLDINGS if h.owner_id == "player" and h.shares > 0]
        if not holdings:
            s = self.small.render("You don't own any guild shares yet.", True, _MUTED)
            self.screen.blit(s, (rect.x, rect.y + 8))
            return

        hdr_cols = [("Guild", 0), ("Shares", int(rect.w * 0.42)),
                    ("Avg cost", int(rect.w * 0.55)), ("Price", int(rect.w * 0.70)),
                    ("Value", int(rect.w * 0.82))]
        for label, off in hdr_cols:
            s = self.small.render(label, True, _MUTED)
            self.screen.blit(s, (rect.x + off, rect.y))

        total_value  = 0
        total_cost   = 0
        for i, h in enumerate(holdings):
            g = GUILDS.get(h.guild_id)
            if g is None:
                continue
            row_y = rect.y + 22 + i * _ROW_H
            row_r = pygame.Rect(rect.x, row_y, rect.w, _ROW_H - 2)
            bg = _ROW_BG if i % 2 == 0 else _ROW_ALT
            pygame.draw.rect(self.screen, bg, row_r, border_radius=3)

            value = int(g.share_price * h.shares)
            cost  = int(h.avg_buy_price * h.shares)
            total_value += value
            total_cost  += cost

            self.screen.blit(self.small.render(g.name[:32], True, _SAND),
                             (row_r.x + 6, row_r.y + 7))
            self.screen.blit(self.small.render(str(h.shares), True, _SAND),
                             (row_r.x + int(rect.w * 0.42), row_r.y + 7))
            self.screen.blit(self.small.render(f"{h.avg_buy_price:.2f}g", True, _MUTED),
                             (row_r.x + int(rect.w * 0.55), row_r.y + 7))
            self.screen.blit(self.small.render(f"{g.share_price:.2f}g", True, _GOLD),
                             (row_r.x + int(rect.w * 0.70), row_r.y + 7))
            self.screen.blit(self.small.render(f"{value}g", True, _SAND),
                             (row_r.x + int(rect.w * 0.82), row_r.y + 7))

        # Footer totals
        pl = total_value - total_cost
        color = _GAIN if pl >= 0 else _LOSS
        footer_y = rect.bottom - 40
        self.screen.blit(self.small.render(f"Total value: {total_value}g", True, _SAND),
                         (rect.x + 6, footer_y))
        self.screen.blit(self.small.render(f"Cost basis: {total_cost}g", True, _MUTED),
                         (rect.x + 180, footer_y))
        self.screen.blit(self.small.render(f"Unrealized P/L: {pl:+}g", True, color),
                         (rect.x + 360, footer_y))

    # ------------------------------------------------------------------
    # History tab — worldgen-era backstory per guild
    # ------------------------------------------------------------------

    def _draw_stock_history(self, player, rect):
        """Two-pane: guild list on the left, deep history on the right.
        Pulls Guild.historical_ledger + legendary_events seeded by the
        worldgen economy sim. Lets the player judge centuries of track
        record before committing to a position."""
        guilds_list = sorted(GUILDS.values(),
                             key=lambda g: (-len(g.historical_ledger), g.name))

        list_w   = int(rect.w * 0.34)
        list_rect = pygame.Rect(rect.x, rect.y, list_w, rect.h)
        detail_rect = pygame.Rect(rect.x + list_w + 8, rect.y,
                                  rect.w - list_w - 8, rect.h)

        # Left: guild list (scrollable)
        max_rows = list_rect.h // _ROW_H
        max_scroll = max(0, len(guilds_list) - max_rows)
        self._stock_scroll = max(0, min(self._stock_scroll, max_scroll))
        for i, g in enumerate(guilds_list[self._stock_scroll:self._stock_scroll + max_rows]):
            row_y = list_rect.y + i * _ROW_H
            row_r = pygame.Rect(list_rect.x, row_y, list_rect.w, _ROW_H - 2)
            sel = (g.guild_id == self._stock_selected_gid)
            bg = _HEADER_BG if sel else (_ROW_BG if i % 2 == 0 else _ROW_ALT)
            pygame.draw.rect(self.screen, bg, row_r, border_radius=3)
            name_s = self.small.render(g.name[:30], True, _SAND if g.state == "active" else _MUTED)
            self.screen.blit(name_s, (row_r.x + 6, row_r.y + 4))
            if g.founded_year:
                meta = f"Est. yr {g.founded_year}  ·  {len(g.historical_ledger)} yr ledger"
            else:
                meta = "No recorded history"
            self.screen.blit(self.small.render(meta, True, _MUTED),
                             (row_r.x + 6, row_r.y + 18))
            self._stock_rects[("select", g.guild_id)] = row_r

        # Right: detail
        if self._stock_selected_gid is None and guilds_list:
            self._stock_selected_gid = guilds_list[0].guild_id
        sel = GUILDS.get(self._stock_selected_gid)
        if sel is None:
            return
        self._draw_history_detail(sel, detail_rect)

    def _draw_history_detail(self, g, rect):
        pygame.draw.rect(self.screen, _ROW_BG, rect, border_radius=4)
        pygame.draw.rect(self.screen, _BORDER, rect, 1, border_radius=4)

        title = self.font.render(g.name, True, _GOLD)
        self.screen.blit(title, (rect.x + 10, rect.y + 8))
        sub = self.small.render(
            INDUSTRY_DISPLAY.get(g.industry, g.industry), True, _MUTED)
        self.screen.blit(sub, (rect.x + 10, rect.y + 30))

        # Founder line
        y = rect.y + 50
        if g.founded_year:
            founder_line = (f"Chartered in year {g.founded_year} by "
                            f"{g.founder_name or 'an unrecorded founder'}"
                            f" of {g.founder_house or 'a forgotten house'}.")
        else:
            founder_line = "Founded recently — no centuries-deep ledger yet."
        # Wrap roughly.
        for line in _wrap(founder_line, 70):
            self.screen.blit(self.small.render(line, True, _SAND), (rect.x + 10, y))
            y += 16

        # Long-term sparkline (the centuries chart)
        ledger = g.historical_ledger
        if ledger:
            y += 6
            self.screen.blit(self.small.render("Share price — full history", True, _MUTED),
                             (rect.x + 10, y))
            y += 16
            spark_rect = pygame.Rect(rect.x + 10, y, rect.w - 20, 80)
            pygame.draw.rect(self.screen, _BG, spark_rect, border_radius=3)
            pygame.draw.rect(self.screen, _BORDER, spark_rect, 1, border_radius=3)
            _draw_long_sparkline(self.screen, ledger, spark_rect)
            y = spark_rect.bottom + 6

            # Final stats line.
            last = ledger[-1]
            stats = (f"Ledger: {len(ledger)} yr   "
                     f"Final treasury: {last.treasury}g   "
                     f"Final price: {last.share_price:.2f}g   "
                     f"Houses/branches: {last.members}")
            self.screen.blit(self.small.render(stats, True, _SAND),
                             (rect.x + 10, y))
            y += 18
        else:
            y += 6

        # Legendary events scroll.
        self.screen.blit(self.small.render("Legendary events", True, _GOLD),
                         (rect.x + 10, y))
        y += 18
        events = g.legendary_events or ["No notable events recorded — a quiet history."]
        for line in events:
            for chunk in _wrap(line, 72):
                if y + 14 > rect.bottom - 6:
                    break
                self.screen.blit(self.small.render(chunk, True, _SAND),
                                 (rect.x + 10, y))
                y += 14
            if y + 14 > rect.bottom - 6:
                break

    # ------------------------------------------------------------------
    # Click + key handlers
    # ------------------------------------------------------------------

    def handle_stock_exchange_click(self, pos, player):
        for key, r in list(self._stock_rects.items()):
            if not r.collidepoint(pos):
                continue
            if key == "close":
                self.stock_exchange_open = False
            elif isinstance(key, tuple) and key[0] == "tab":
                self._stock_tab = key[1]
            elif isinstance(key, tuple) and key[0] == "select":
                self._stock_selected_gid = key[1]
            elif key == "qty_-1":
                self._stock_buy_qty = max(1, self._stock_buy_qty - 1)
            elif key == "qty_+1":
                self._stock_buy_qty += 1
            elif key == "qty_+10":
                self._stock_buy_qty += 10
            elif key == "qty_max":
                g = GUILDS.get(self._stock_selected_gid)
                if g is not None and g.share_price > 0:
                    self._stock_buy_qty = max(1, int(getattr(player, "money", 0) // g.share_price))
            elif key == "buy":
                self._do_stock_buy(player)
            elif key == "sell":
                self._do_stock_sell(player)
            elif key == "short":
                self._do_short(player)
            elif isinstance(key, tuple) and key[0] == "bond_buy":
                self._do_buy_bond(player, key[1])
            elif key == "loan_borrow":
                self._do_borrow(player)
            elif key == "loan_repay":
                self._do_repay(player)
            elif isinstance(key, tuple) and key[0] == "charter":
                self._adjust_charter(*key[1:])
            elif isinstance(key, tuple) and key[0] == "board_qty":
                self._board_action_qty = max(1, self._board_action_qty + key[1])
            elif key == "buyback":
                self._do_buyback(player)
            elif key == "dilute":
                self._do_dilute(player)
            elif key == "charter_back":
                self._charter_back()
                self._charter_name_editing = False
            elif key == "charter_next":
                self._charter_next(player)
                self._charter_name_editing = False
            elif key == "charter_name_field":
                self._charter_name_editing = not self._charter_name_editing
            elif isinstance(key, tuple) and key[0] == "charter_industry":
                self._charter_industry = key[1]
            elif isinstance(key, tuple) and key[0] == "charter_region":
                self._charter_region_id = key[1]
            elif isinstance(key, tuple) and key[0] in ("charter_shares", "charter_price", "charter_float"):
                self._adjust_charter_wizard(*key)
            break

    def handle_stock_exchange_keydown(self, key, player, unicode=""):
        if self._charter_name_editing and self._stock_tab == "charter":
            if key == pygame.K_BACKSPACE:
                self._charter_name = self._charter_name[:-1]
                return
            if key == pygame.K_RETURN:
                self._charter_name_editing = False
                return
            if unicode and unicode.isprintable() and len(self._charter_name) < 40:
                self._charter_name += unicode
                return
        if key == pygame.K_ESCAPE:
            self.stock_exchange_open = False
        elif key == pygame.K_TAB:
            order = ["market", "portfolio", "history"]
            try:
                idx = order.index(self._stock_tab)
            except ValueError:
                idx = -1
            self._stock_tab = order[(idx + 1) % len(order)]

    def _do_buyback(self, player):
        if self._stock_selected_gid is None:
            return
        g = GUILDS.get(self._stock_selected_gid)
        if g is None or g.player_pct() < OWNERSHIP_MAJORITY or not self._majority_unlocked():
            self._stock_status_msg = "Majority Control required."
            return
        ok, _, msg = buyback_shares(self._stock_selected_gid, self._board_action_qty)
        self._stock_status_msg = msg

    def _do_dilute(self, player):
        if self._stock_selected_gid is None:
            return
        g = GUILDS.get(self._stock_selected_gid)
        if g is None or g.player_pct() < OWNERSHIP_MAJORITY or not self._majority_unlocked():
            self._stock_status_msg = "Majority Control required."
            return
        ok, _, msg = issue_shares(self._stock_selected_gid, self._board_action_qty)
        self._stock_status_msg = msg

    # ------------------------------------------------------------------
    # Phase 7 action handlers
    # ------------------------------------------------------------------

    def _do_short(self, player):
        if self._stock_selected_gid is None:
            return
        gid = self._stock_selected_gid
        if player_short(gid) is not None:
            ok, gain, msg = close_short(gid, 0)
            if ok:
                player.money = max(0, getattr(player, "money", 0) + gain)
        else:
            ok, margin, msg = open_short(gid, self._stock_buy_qty,
                                         getattr(player, "money", 0))
            if ok:
                player.money = max(0, getattr(player, "money", 0) - margin)
        self._stock_status_msg = msg

    def _do_buy_bond(self, player, bond_id):
        ok, _, msg = buy_bond(bond_id, player)
        self._stock_status_msg = msg

    def _do_borrow(self, player):
        ok, _, msg = borrow(player, self._stock_buy_qty * 50)
        self._stock_status_msg = msg

    def _do_repay(self, player):
        ok, _, msg = repay(player, self._stock_buy_qty * 50)
        self._stock_status_msg = msg

    def _adjust_charter_wizard(self, field, delta, lo, hi):
        if field == "charter_shares":
            self._charter_share_count = int(max(lo, min(hi, self._charter_share_count + delta)))
        elif field == "charter_price":
            self._charter_ipo_price = max(lo, min(hi, self._charter_ipo_price + delta))
        elif field == "charter_float":
            self._charter_float_pct = max(lo, min(hi, self._charter_float_pct + delta))

    def _do_stock_buy(self, player):
        if self._stock_selected_gid is None:
            return
        ok, cost, msg = buy_shares(
            self._stock_selected_gid, self._stock_buy_qty,
            getattr(player, "money", 0))
        self._stock_status_msg = msg
        if ok:
            player.money = max(0, getattr(player, "money", 0) - cost)

    def _do_stock_sell(self, player):
        if self._stock_selected_gid is None:
            return
        ok, gain, msg = sell_shares(self._stock_selected_gid, self._stock_buy_qty)
        self._stock_status_msg = msg
        if ok:
            player.money = getattr(player, "money", 0) + gain


    # ------------------------------------------------------------------
    # Board Room tab
    # ------------------------------------------------------------------

    def _board_view_unlocked(self):
        r = getattr(self, "_stock_research", None)
        if r is None:
            return False
        n = r.nodes.get("board_seat_view")
        return n is not None and n.unlocked

    def _majority_unlocked(self):
        r = getattr(self, "_stock_research", None)
        if r is None:
            return False
        n = r.nodes.get("majority_control")
        return n is not None and n.unlocked

    def _insider_unlocked(self):
        r = getattr(self, "_stock_research", None)
        if r is None:
            return False
        n = r.nodes.get("insider_information")
        return n is not None and n.unlocked

    def _charter_unlocked(self):
        r = getattr(self, "_stock_research", None)
        if r is None:
            return False
        n = r.nodes.get("founders_charter")
        return n is not None and n.unlocked

    def _draw_stock_board_room(self, player, rect):
        # Filter to guilds where the player holds at least board-seat ownership.
        eligible = [g for g in active_guilds()
                    if g.player_pct() >= OWNERSHIP_BOARD_SEAT]
        if not self._board_view_unlocked():
            s = self.small.render(
                "Board Seat Privileges (research T2) required.",
                True, _MUTED)
            self.screen.blit(s, (rect.x, rect.y + 8))
            return
        if not eligible:
            s = self.small.render(
                "You need a ≥25% stake in at least one guild to attend a board.",
                True, _MUTED)
            self.screen.blit(s, (rect.x, rect.y + 8))
            return

        # Auto-select first eligible if current selection isn't eligible.
        if self._stock_selected_gid not in {g.guild_id for g in eligible}:
            self._stock_selected_gid = eligible[0].guild_id

        # Left: eligible guild list
        list_w = int(rect.w * 0.42)
        list_rect = pygame.Rect(rect.x, rect.y, list_w, rect.h)
        for i, g in enumerate(eligible):
            row_y = rect.y + i * _ROW_H
            row_r = pygame.Rect(rect.x, row_y, list_w - 6, _ROW_H - 2)
            bg = _HEADER_BG if g.guild_id == self._stock_selected_gid else (_ROW_BG if i % 2 == 0 else _ROW_ALT)
            pygame.draw.rect(self.screen, bg, row_r, border_radius=3)
            name_s = self.small.render(g.name[:32], True, _SAND)
            self.screen.blit(name_s, (row_r.x + 6, row_r.y + 4))
            pct_s = self.small.render(f"{g.player_pct()*100:5.1f}% — {player_tier(g)}", True, _GOLD)
            self.screen.blit(pct_s, (row_r.x + 6, row_r.y + 18))
            self._stock_rects[("select", g.guild_id)] = row_r

        # Right: board panel
        sel = GUILDS.get(self._stock_selected_gid)
        if sel is None:
            return
        panel = pygame.Rect(rect.x + list_w + 8, rect.y, rect.w - list_w - 8, rect.h)
        pygame.draw.rect(self.screen, _ROW_BG, panel, border_radius=4)
        pygame.draw.rect(self.screen, _BORDER, panel, 1, border_radius=4)
        self._draw_board_panel(sel, panel)

    def _draw_board_panel(self, g, panel):
        # Header
        title = self.font.render(g.name, True, _GOLD)
        self.screen.blit(title, (panel.x + 10, panel.y + 8))
        sub = self.small.render(
            f"{INDUSTRY_DISPLAY.get(g.industry, g.industry)}  ·  "
            f"You own {g.player_pct()*100:.1f}% ({player_tier(g)})",
            True, _MUTED)
        self.screen.blit(sub, (panel.x + 10, panel.y + 30))

        # Private financials (board-seat tier)
        chapter_count = len(g.chapter_ids)
        outpost_count = sum(len(CHAPTERS[cid].outpost_ids)
                            for cid in g.chapter_ids if cid in CHAPTERS)
        stats = [
            ("Treasury",        f"{g.treasury}g"),
            ("Chapters",        f"{chapter_count}"),
            ("Owned outposts",  f"{outpost_count}"),
            ("Profit (EMA)",    f"{g.profit_ema:+.1f}g/day"),
            ("Last week P/L",   f"{g.last_week_profit:+}g"),
            ("Days underwater", f"{g.days_negative}"),
        ]
        y = panel.y + 56
        for label, val in stats:
            ls = self.small.render(label, True, _MUTED)
            vs = self.small.render(val, True, _SAND)
            self.screen.blit(ls, (panel.x + 10, y))
            self.screen.blit(vs, (panel.x + panel.w - vs.get_width() - 12, y))
            y += 18

        # Chapter price multipliers (read-only at board tier, editable at majority)
        y += 8
        hdr = self.small.render("Regional chapters", True, _SAND)
        self.screen.blit(hdr, (panel.x + 10, y))
        y += 20
        for cid in g.chapter_ids:
            ch = CHAPTERS.get(cid)
            if ch is None:
                continue
            row = pygame.Rect(panel.x + 10, y, panel.w - 20, 22)
            label = f"Region {ch.region_id}: ×{ch.local_price_mult:.2f}  ({len(ch.outpost_ids)} outposts)"
            self.screen.blit(self.small.render(label, True, _SAND), (row.x, row.y + 4))
            y += 22

        # Top NPC shareholders (anonymous traders)
        npc_held = sorted(npc_holdings_for(g.guild_id), key=lambda h: -h.shares)[:4]
        if npc_held:
            y += 4
            self.screen.blit(self.small.render("Top NPC holders", True, _SAND),
                             (panel.x + 10, y))
            y += 20
            for i, h in enumerate(npc_held):
                pct = h.shares / max(1, g.share_count) * 100.0
                label = f"Trader {i+1}: {h.shares} shares ({pct:.1f}%)"
                self.screen.blit(self.small.render(label, True, _MUTED),
                                 (panel.x + 10, y + 4))
                y += 18

        # Charter sliders (majority tier only)
        y += 12
        majority = g.player_pct() >= OWNERSHIP_MAJORITY and self._majority_unlocked()
        if not majority:
            note = self.small.render(
                "Majority Control (≥51% + research T3) required to set charter policy.",
                True, _MUTED)
            self.screen.blit(note, (panel.x + 10, y))
            return

        hdr2 = self.small.render("Charter policy (you control)", True, _GOLD)
        self.screen.blit(hdr2, (panel.x + 10, y))
        y += 22

        self._draw_charter_row(g, "price_mult",
                               "Price multiplier", g.charter.get("price_mult", 1.0),
                               "%.2f×", panel.x + 10, y, panel.w - 20,
                               step=0.05, lo=0.75, hi=1.50)
        y += 28
        self._draw_charter_row(g, "dividend_rate",
                               "Dividend rate", g.dividend_rate,
                               "%.1f%%", panel.x + 10, y, panel.w - 20,
                               step=0.01, lo=0.0, hi=0.15, scale=100.0)
        y += 28
        self._draw_charter_row(g, "expansion_appetite",
                               "Expansion appetite", g.charter.get("expansion_appetite", 0.5),
                               "%.2f", panel.x + 10, y, panel.w - 20,
                               step=0.10, lo=0.0, hi=1.0)
        y += 36

        # Capital actions: buyback + dilution
        hdr3 = self.small.render(
            f"Capital actions  (qty {self._board_action_qty})", True, _GOLD)
        self.screen.blit(hdr3, (panel.x + 10, y))
        y += 22
        for label, dq, key_x in [("-10", -10, 0), ("-1", -1, 36),
                                  ("+1", 1, 72), ("+10", 10, 108)]:
            r = pygame.Rect(panel.x + 10 + key_x, y, 32, 22)
            pygame.draw.rect(self.screen, _TAB_IDLE, r, border_radius=3)
            pygame.draw.rect(self.screen, _BORDER, r, 1, border_radius=3)
            s = self.small.render(label, True, _SAND)
            self.screen.blit(s, (r.centerx - s.get_width() // 2,
                                 r.centery - s.get_height() // 2))
            self._stock_rects[("board_qty", dq)] = r

        cost_estimate = int(g.share_price * self._board_action_qty)
        buy_r  = pygame.Rect(panel.x + 10,  y + 30, 130, 24)
        iss_r  = pygame.Rect(panel.x + 150, y + 30, 130, 24)
        pygame.draw.rect(self.screen, (60, 110, 60),  buy_r, border_radius=3)
        pygame.draw.rect(self.screen, (110, 90, 50),  iss_r, border_radius=3)
        pygame.draw.rect(self.screen, _BORDER, buy_r, 1, border_radius=3)
        pygame.draw.rect(self.screen, _BORDER, iss_r, 1, border_radius=3)
        bs = self.small.render(f"Buyback (-{cost_estimate}g)", True, (240, 240, 230))
        ds = self.small.render(f"Dilute (+{cost_estimate}g)", True, (240, 240, 230))
        self.screen.blit(bs, (buy_r.centerx - bs.get_width() // 2,
                              buy_r.centery - bs.get_height() // 2))
        self.screen.blit(ds, (iss_r.centerx - ds.get_width() // 2,
                              iss_r.centery - ds.get_height() // 2))
        self._stock_rects["buyback"] = buy_r
        self._stock_rects["dilute"]  = iss_r

    def _draw_charter_row(self, g, field, label, value, fmt, x, y, w,
                           step, lo, hi, scale=1.0):
        ls = self.small.render(label, True, _SAND)
        self.screen.blit(ls, (x, y + 4))
        val_str = fmt % (value * scale)
        vs = self.small.render(val_str, True, _GOLD)
        self.screen.blit(vs, (x + 160, y + 4))

        minus = pygame.Rect(x + w - 80, y, 32, 22)
        plus  = pygame.Rect(x + w - 40, y, 32, 22)
        for r, label_btn in ((minus, "-"), (plus, "+")):
            pygame.draw.rect(self.screen, _TAB_IDLE, r, border_radius=3)
            pygame.draw.rect(self.screen, _BORDER, r, 1, border_radius=3)
            s = self.small.render(label_btn, True, _SAND)
            self.screen.blit(s, (r.centerx - s.get_width() // 2,
                                 r.centery - s.get_height() // 2))
        self._stock_rects[("charter", g.guild_id, field, -step, lo, hi)] = minus
        self._stock_rects[("charter", g.guild_id, field, +step, lo, hi)] = plus

    def _adjust_charter(self, guild_id, field, delta, lo, hi):
        g = GUILDS.get(guild_id)
        if g is None:
            return
        if g.player_pct() < OWNERSHIP_MAJORITY or not self._majority_unlocked():
            self._stock_status_msg = "Majority Control required to edit charter."
            return
        if field == "dividend_rate":
            g.dividend_rate = max(lo, min(hi, g.dividend_rate + delta))
        else:
            g.charter[field] = max(lo, min(hi, float(g.charter.get(field, 1.0)) + delta))
        # Propagate price_mult to existing chapters as the regional baseline.
        if field == "price_mult":
            for cid in g.chapter_ids:
                ch = CHAPTERS.get(cid)
                if ch is not None:
                    ch.local_price_mult = g.charter["price_mult"]
        self._stock_status_msg = f"Updated {field}."


    # ------------------------------------------------------------------
    # Portfolio Finance side panel (shorts, bonds, loan)
    # ------------------------------------------------------------------

    def _draw_portfolio_finance(self, player, rect):
        pygame.draw.rect(self.screen, _ROW_BG, rect, border_radius=4)
        pygame.draw.rect(self.screen, _BORDER, rect, 1, border_radius=4)
        y = rect.y + 6

        # Shorts
        self.screen.blit(self.small.render("SHORT POSITIONS", True, _GOLD), (rect.x + 8, y))
        y += 18
        shorts = [h for h in SHARE_HOLDINGS if h.owner_id == "player_short" and h.shares > 0]
        if not shorts:
            self.screen.blit(self.small.render("None open.", True, _MUTED), (rect.x + 8, y))
            y += 16
        for h in shorts:
            g = GUILDS.get(h.guild_id)
            if g is None:
                continue
            pnl = int((h.avg_buy_price - g.share_price) * h.shares)
            color = _GAIN if pnl >= 0 else _LOSS
            label = f"{g.name[:18]} ×{h.shares}  @ {h.avg_buy_price:.1f} → {g.share_price:.1f}  P/L {pnl:+}g"
            self.screen.blit(self.small.render(label, True, color), (rect.x + 8, y))
            y += 14
        y += 8

        # Bonds
        self.screen.blit(self.small.render("BONDS", True, _GOLD), (rect.x + 8, y))
        y += 18
        held_bonds = player_bonds()
        float_bs   = float_bonds()
        if held_bonds:
            for b in held_bonds[:4]:
                g = GUILDS.get(b.issuer_guild_id)
                gname = g.name[:18] if g else "?"
                label = f"{gname} ({b.face_value}g, {b.coupon_rate*100:.1f}%/wk)"
                self.screen.blit(self.small.render(label, True, _SAND), (rect.x + 8, y))
                y += 14
        else:
            self.screen.blit(self.small.render("None held.", True, _MUTED), (rect.x + 8, y))
            y += 14
        if float_bs:
            self.screen.blit(self.small.render("Available to buy:", True, _MUTED), (rect.x + 8, y))
            y += 14
            for b in float_bs[:3]:
                g = GUILDS.get(b.issuer_guild_id)
                gname = g.name[:18] if g else "?"
                btn_r = pygame.Rect(rect.x + 8, y, rect.w - 16, 20)
                pygame.draw.rect(self.screen, _TAB_IDLE, btn_r, border_radius=3)
                pygame.draw.rect(self.screen, _BORDER, btn_r, 1, border_radius=3)
                label = f"+ {gname} bond  ({b.face_value}g face)"
                self.screen.blit(self.small.render(label, True, _SAND), (btn_r.x + 6, btn_r.y + 3))
                self._stock_rects[("bond_buy", b.bond_id)] = btn_r
                y += 22
        y += 8

        # Loan
        debt = getattr(player, "guild_debt", 0)
        pv   = portfolio_value()
        ltv  = (debt / pv) if pv > 0 else 0.0
        self.screen.blit(self.small.render("MARGIN LOAN", True, _GOLD), (rect.x + 8, y))
        y += 18
        loan_line = f"Debt: {debt}g  ·  LTV: {ltv*100:.0f}%  ·  Cap 30%"
        self.screen.blit(self.small.render(loan_line, True, _SAND), (rect.x + 8, y))
        y += 18
        amt = self._stock_buy_qty * 50
        borrow_r = pygame.Rect(rect.x + 8,                y, (rect.w - 24) // 2, 24)
        repay_r  = pygame.Rect(rect.x + 16 + borrow_r.w,  y, (rect.w - 24) // 2, 24)
        pygame.draw.rect(self.screen, (60, 110, 60), borrow_r, border_radius=3)
        pygame.draw.rect(self.screen, (110, 60, 60), repay_r,  border_radius=3)
        for r in (borrow_r, repay_r):
            pygame.draw.rect(self.screen, _BORDER, r, 1, border_radius=3)
        bs = self.small.render(f"Borrow +{amt}g", True, (240, 240, 230))
        rs = self.small.render(f"Repay {amt}g", True, (240, 240, 230))
        self.screen.blit(bs, (borrow_r.centerx - bs.get_width() // 2,
                              borrow_r.centery - bs.get_height() // 2))
        self.screen.blit(rs, (repay_r.centerx - rs.get_width() // 2,
                              repay_r.centery - rs.get_height() // 2))
        self._stock_rects["loan_borrow"] = borrow_r
        self._stock_rects["loan_repay"]  = repay_r

    # ------------------------------------------------------------------
    # Newswire
    # ------------------------------------------------------------------

    def _draw_newswire(self, rect):
        from industry_events import newswire_snapshot
        pygame.draw.rect(self.screen, _BG, rect, border_radius=3)
        pygame.draw.rect(self.screen, _BORDER, rect, 1, border_radius=3)
        hdr = self.small.render("NEWSWIRE", True, _GOLD)
        self.screen.blit(hdr, (rect.x + 8, rect.y + 4))
        items = newswire_snapshot(4)
        if not items:
            self.screen.blit(self.small.render("No headlines yet.", True, _MUTED),
                             (rect.x + 8, rect.y + 22))
            return
        for i, item in enumerate(items):
            color = _LOSS if item["kind"] == "rivalry" else _SAND
            line = f"Day {item['day']}: {item['headline']}"
            self.screen.blit(self.small.render(line[:90], True, color),
                             (rect.x + 8, rect.y + 22 + i * 14))

    # ------------------------------------------------------------------
    # Charter tab (player-founded guild wizard)
    # ------------------------------------------------------------------

    def _draw_stock_charter(self, player, rect):
        from guilds import INDUSTRY_DISPLAY as _IND
        from towns import REGIONS as _REGIONS
        steps = ["Name", "Industry", "Region", "IPO", "Confirm"]
        # Stepper
        x = rect.x
        for i, label in enumerate(steps):
            color = _GOLD if i == self._charter_step else _MUTED
            s = self.small.render(f"{i+1}. {label}", True, color)
            self.screen.blit(s, (x, rect.y))
            x += s.get_width() + 18

        body = pygame.Rect(rect.x, rect.y + 28, rect.w, rect.h - 28)
        pygame.draw.rect(self.screen, _ROW_BG, body, border_radius=4)
        pygame.draw.rect(self.screen, _BORDER, body, 1, border_radius=4)

        if self._charter_step == 0:
            self._draw_charter_step_name(body)
        elif self._charter_step == 1:
            self._draw_charter_step_industry(body, _IND)
        elif self._charter_step == 2:
            self._draw_charter_step_region(body, _REGIONS)
        elif self._charter_step == 3:
            self._draw_charter_step_ipo(body, player)
        else:
            self._draw_charter_step_confirm(body, player, _IND, _REGIONS)

        # Step nav buttons
        nav_y = rect.bottom - 28
        back_r   = pygame.Rect(rect.x,            nav_y, 90, 24)
        next_r   = pygame.Rect(rect.x + 100,      nav_y, 90, 24)
        pygame.draw.rect(self.screen, _TAB_IDLE, back_r, border_radius=3)
        pygame.draw.rect(self.screen, _TAB_IDLE, next_r, border_radius=3)
        pygame.draw.rect(self.screen, _BORDER, back_r, 1, border_radius=3)
        pygame.draw.rect(self.screen, _BORDER, next_r, 1, border_radius=3)
        self.screen.blit(self.small.render("◀ Back", True, _SAND),
                         (back_r.centerx - 26, back_r.centery - 7))
        next_label = "Found ▶" if self._charter_step == len(steps) - 1 else "Next ▶"
        self.screen.blit(self.small.render(next_label, True, _SAND),
                         (next_r.centerx - 30, next_r.centery - 7))
        self._stock_rects["charter_back"] = back_r
        self._stock_rects["charter_next"] = next_r

    def _draw_charter_step_name(self, body):
        self.screen.blit(self.small.render("Guild name (click to edit):", True, _SAND),
                         (body.x + 12, body.y + 10))
        name_r = pygame.Rect(body.x + 12, body.y + 32, body.w - 24, 28)
        color = _HEADER_BG if self._charter_name_editing else _BG
        pygame.draw.rect(self.screen, color, name_r, border_radius=3)
        pygame.draw.rect(self.screen, _BORDER, name_r, 1, border_radius=3)
        cursor = "_" if self._charter_name_editing else ""
        self.screen.blit(self.font.render(self._charter_name + cursor, True, _GOLD),
                         (name_r.x + 8, name_r.y + 4))
        self._stock_rects["charter_name_field"] = name_r

    def _draw_charter_step_industry(self, body, ind_display):
        self.screen.blit(self.small.render("Pick an industry for your charter:", True, _SAND),
                         (body.x + 12, body.y + 10))
        col_w  = (body.w - 24) // 3
        keys = list(ind_display.keys())
        for i, key in enumerate(keys):
            cx = body.x + 12 + (i % 3) * col_w
            cy = body.y + 32 + (i // 3) * 26
            r = pygame.Rect(cx, cy, col_w - 6, 22)
            sel = (self._charter_industry == key)
            pygame.draw.rect(self.screen, _TAB_SEL if sel else _TAB_IDLE, r, border_radius=3)
            pygame.draw.rect(self.screen, _BORDER, r, 1, border_radius=3)
            s = self.small.render(ind_display[key], True, _GOLD if sel else _SAND)
            self.screen.blit(s, (r.centerx - s.get_width() // 2,
                                 r.centery - s.get_height() // 2))
            self._stock_rects[("charter_industry", key)] = r

    def _draw_charter_step_region(self, body, regions):
        self.screen.blit(self.small.render("Pick a home region:", True, _SAND),
                         (body.x + 12, body.y + 10))
        if not regions:
            self.screen.blit(self.small.render("No regions exist yet — explore the world first.", True, _MUTED),
                             (body.x + 12, body.y + 32))
            return
        col_w = (body.w - 24) // 2
        for i, region in enumerate(regions.values()):
            cx = body.x + 12 + (i % 2) * col_w
            cy = body.y + 32 + (i // 2) * 26
            r = pygame.Rect(cx, cy, col_w - 6, 22)
            sel = (self._charter_region_id == region.region_id)
            pygame.draw.rect(self.screen, _TAB_SEL if sel else _TAB_IDLE, r, border_radius=3)
            pygame.draw.rect(self.screen, _BORDER, r, 1, border_radius=3)
            label = f"{region.name} ({region.biome_group})"
            s = self.small.render(label[:34], True, _GOLD if sel else _SAND)
            self.screen.blit(s, (r.centerx - s.get_width() // 2,
                                 r.centery - s.get_height() // 2))
            self._stock_rects[("charter_region", region.region_id)] = r

    def _draw_charter_step_ipo(self, body, player):
        rows = [
            ("Share count",   self._charter_share_count, "charter_shares", 100, 100, 10000, "%d"),
            ("IPO price",     self._charter_ipo_price,   "charter_price",  1.0, 1.0,  100.0, "%.1f g"),
            ("Public float",  self._charter_float_pct,   "charter_float",  0.05, 0.0,  1.0,   "%.0f%%"),
        ]
        y = body.y + 14
        for label, value, key, step, lo, hi, fmt in rows:
            self.screen.blit(self.small.render(label, True, _SAND), (body.x + 12, y + 4))
            display = fmt % (value * 100.0 if "%%" in fmt else value)
            self.screen.blit(self.small.render(display, True, _GOLD), (body.x + 140, y + 4))
            minus = pygame.Rect(body.x + body.w - 80, y, 32, 22)
            plus  = pygame.Rect(body.x + body.w - 40, y, 32, 22)
            for r, lbl in ((minus, "-"), (plus, "+")):
                pygame.draw.rect(self.screen, _TAB_IDLE, r, border_radius=3)
                pygame.draw.rect(self.screen, _BORDER, r, 1, border_radius=3)
                s = self.small.render(lbl, True, _SAND)
                self.screen.blit(s, (r.centerx - s.get_width() // 2,
                                     r.centery - s.get_height() // 2))
            self._stock_rects[(key, -step, lo, hi)] = minus
            self._stock_rects[(key, +step, lo, hi)] = plus
            y += 30
        # Live numbers
        public_shares = int(round(self._charter_share_count * self._charter_float_pct))
        treasury_seed = int(round(self._charter_ipo_price * public_shares))
        info = (f"You keep {self._charter_share_count - public_shares} shares; "
                f"public buys {public_shares} → treasury seeded {treasury_seed}g")
        self.screen.blit(self.small.render(info, True, _MUTED), (body.x + 12, y + 4))

    def _draw_charter_step_confirm(self, body, player, ind_display, regions):
        fee = int(FOUNDING_FEE + self._charter_share_count * FOUNDING_FEE_PER_SHARE)
        region_name = "—"
        if self._charter_region_id is not None and self._charter_region_id in regions:
            region_name = regions[self._charter_region_id].name
        lines = [
            f"Name:       {self._charter_name or '(unnamed)'}",
            f"Industry:   {ind_display.get(self._charter_industry, '—')}",
            f"Region:     {region_name}",
            f"Shares:     {self._charter_share_count}",
            f"IPO price:  {self._charter_ipo_price:.2f}g",
            f"Public:     {self._charter_float_pct*100:.0f}%",
            f"Fee:        {fee}g  (you have {getattr(player, 'money', 0)}g)",
        ]
        for i, line in enumerate(lines):
            color = _SAND if "Fee:" not in line or getattr(player, 'money', 0) >= fee else _LOSS
            self.screen.blit(self.small.render(line, True, color),
                             (body.x + 12, body.y + 12 + i * 20))

    # ------------------------------------------------------------------
    # Charter wizard helpers
    # ------------------------------------------------------------------

    def _charter_next(self, player):
        # On final step, perform the IPO.
        if self._charter_step >= 4:
            if self._charter_industry is None or self._charter_region_id is None:
                self._stock_status_msg = "Pick an industry and region first."
                return
            from towns import REGIONS
            region = REGIONS.get(self._charter_region_id)
            capital = region.capital_town_id if region else 0
            ok, msg, cost, gid = found_player_guild(
                self._charter_name,
                self._charter_industry,
                self._charter_region_id,
                capital,
                self._charter_share_count,
                self._charter_ipo_price,
                self._charter_float_pct,
                getattr(player, "money", 0),
            )
            self._stock_status_msg = msg
            if ok:
                player.money = max(0, getattr(player, "money", 0) - cost)
                self._stock_selected_gid = gid
                self._stock_tab = "board"
                self._charter_step = 0
            return
        self._charter_step += 1

    def _charter_back(self):
        self._charter_step = max(0, self._charter_step - 1)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _price_delta_pct(g) -> float:
    hist = list(g.price_history)
    if len(hist) < 2 or hist[0] <= 0:
        return 0.0
    return (hist[-1] - hist[0]) / hist[0] * 100.0


def _wrap(text: str, width: int):
    """Cheap word-wrap to ``width`` chars per line. Returns a list."""
    out = []
    line = ""
    for word in text.split():
        if line and len(line) + 1 + len(word) > width:
            out.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    if line:
        out.append(line)
    return out


def _draw_long_sparkline(surface, ledger, rect):
    """Sparkline for the full historical ledger. Tints crash-years red so
    players can spot wars/plagues at a glance."""
    if len(ledger) < 2:
        return
    prices = [row.share_price for row in ledger]
    lo, hi = min(prices), max(prices)
    span = max(0.001, hi - lo)
    n = len(prices)
    pts = []
    for i, v in enumerate(prices):
        x = rect.x + 4 + int((rect.w - 8) * (i / (n - 1)))
        y = rect.y + 4 + int((rect.h - 8) * (1.0 - (v - lo) / span))
        pts.append((x, y))
    color = _GAIN if prices[-1] >= prices[0] else _LOSS
    pygame.draw.lines(surface, color, False, pts, 2)
    # Mark crash/boom years with a small dot.
    for i, row in enumerate(ledger):
        tag = getattr(row, "event", "") or ""
        if not tag:
            continue
        dot_color = _LOSS if tag in ("sacked", "plague", "collapse",
                                     "earthquake", "schism", "civil_war",
                                     "founder_extinct") else _GAIN
        pygame.draw.circle(surface, dot_color, pts[i], 2)


def _draw_sparkline(surface, values, rect):
    if len(values) < 2:
        return
    lo, hi = min(values), max(values)
    span = max(0.001, hi - lo)
    pts = []
    n = len(values)
    for i, v in enumerate(values):
        x = rect.x + 4 + int((rect.w - 8) * (i / (n - 1)))
        y = rect.y + 4 + int((rect.h - 8) * (1.0 - (v - lo) / span))
        pts.append((x, y))
    color = _GAIN if values[-1] >= values[0] else _LOSS
    pygame.draw.lines(surface, color, False, pts, 2)
