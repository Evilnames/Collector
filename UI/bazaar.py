"""Bazaar UI — auction floor, sealed bidding, fence trades, and result phases."""
import pygame

from bazaar import AuctionLot, RARITY_COLORS, RARITY_BG, CATEGORY_LABELS

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------

_BG          = (20, 15, 10)
_PANEL       = (42, 30, 18)
_BORDER      = (100, 72, 42)
_HEADER_BG   = (55, 38, 20)
_GOLD        = (210, 170, 55)
_SAND        = (185, 155, 100)
_MUTED       = (130, 110, 80)
_WIN         = (100, 220, 100)
_LOSS        = (220, 90,  70)
_PASS_COL    = (130, 130, 120)

# Bid tier buttons: pass / base / ×1.5 / ×2
_TIER_BG_SEL   = [(70, 65, 55), (160, 135, 55), (185, 130, 45), (205, 170, 50)]
_TIER_BG_IDLE  = (38, 30, 20)
_TIER_BRD_SEL  = [(110, 100, 80), (200, 170, 70), (215, 155, 60), (230, 195, 70)]
_TIER_BRD_IDLE = (70, 55, 35)
_TIER_MULTS    = [0.0, 1.0, 1.5, 2.0]


def _bid_amount(lot: AuctionLot, tier: int) -> int:
    if tier == 0:
        return 0
    return max(1, int(lot.base_price * _TIER_MULTS[tier]))


# ---------------------------------------------------------------------------
# Mixin
# ---------------------------------------------------------------------------

class BazaarUIMixin:

    def open_bazaar(self, lots, fence_wants, rival_names):
        self.bazaar_open          = True
        self._bazaar_phase        = "floor"
        self._bazaar_lots         = lots
        self._bazaar_fence_wants  = list(fence_wants)   # [(item_id, qty, pay, flavor), ...]
        self._bazaar_rivals       = list(rival_names)
        self._bazaar_bids         = [0] * len(lots)     # tier index per lot
        self._bazaar_fence_sold   = set()               # fence slot indices already sold
        self._bazaar_rects        = {}
        # resolve
        self._bazaar_resolve_log     = []   # [(text, tag), ...]
        self._bazaar_resolve_results = []   # [(lot, player_bid, rival_bid, won), ...]
        self._bazaar_reveal_idx      = 0
        self._bazaar_reveal_timer    = 0.0
        self._bazaar_reveal_done     = False
        # result
        self._bazaar_won_lots     = []
        self._bazaar_gold_spent   = 0
        self._bazaar_fence_earned = 0

    # -----------------------------------------------------------------------
    # Top-level draw dispatcher
    # -----------------------------------------------------------------------

    def _draw_bazaar(self, player, dt):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        sw, sh = self.screen.get_size()
        pw, ph = 700, 500
        px = (sw - pw) // 2
        py = (sh - ph) // 2

        pygame.draw.rect(self.screen, _BG,     (px, py, pw, ph), border_radius=6)
        pygame.draw.rect(self.screen, _BORDER, (px, py, pw, ph), 2, border_radius=6)
        pygame.draw.rect(self.screen, _PANEL,  (px + 10, py + 10, pw - 20, ph - 20), border_radius=4)

        title_strip = pygame.Rect(px + 10, py + 10, pw - 20, 28)
        pygame.draw.rect(self.screen, _HEADER_BG, title_strip, border_radius=4)
        title = self.font.render("THE GRAND BAZAAR", True, _GOLD)
        self.screen.blit(title, (px + pw // 2 - title.get_width() // 2, py + 15))

        if self._bazaar_phase == "floor":
            self._draw_bazaar_floor(player, px, py, pw, ph)
        elif self._bazaar_phase == "resolve":
            self._draw_bazaar_resolve(player, dt, px, py, pw, ph)
        elif self._bazaar_phase == "result":
            self._draw_bazaar_result(player, px, py, pw, ph)

    # -----------------------------------------------------------------------
    # Floor phase
    # -----------------------------------------------------------------------

    def _draw_bazaar_floor(self, player, px, py, pw, ph):
        self._bazaar_rects = {}
        font, small = self.font, self.small

        LEFT_W  = 432
        RIGHT_X = px + LEFT_W + 16
        RIGHT_W = pw - LEFT_W - 26
        LOT_H   = 72
        content_y = py + 48

        # ---- Left: lot cards ----
        hdr = small.render("TODAY'S LOTS  —  Sealed Bids", True, _SAND)
        self.screen.blit(hdr, (px + 14, content_y))

        for i, lot in enumerate(self._bazaar_lots):
            lx = px + 14
            ly = content_y + 18 + i * (LOT_H + 2)
            lw = LEFT_W - 8

            rar_bg  = RARITY_BG.get(lot.rarity, (35, 35, 35))
            rar_brd = RARITY_COLORS.get(lot.rarity, (180, 180, 180))
            crect   = pygame.Rect(lx, ly, lw, LOT_H)
            pygame.draw.rect(self.screen, rar_bg,  crect, border_radius=4)
            pygame.draw.rect(self.screen, rar_brd, crect, 1, border_radius=4)

            # Swatch
            pygame.draw.rect(self.screen, lot.swatch_color,
                             (lx + 6, ly + 7, 18, 18), border_radius=3)
            pygame.draw.rect(self.screen, (255, 255, 255),
                             (lx + 6, ly + 7, 18, 18), 1, border_radius=3)

            # Name + qty
            name_s = small.render(f"{lot.display_name}  ×{lot.qty}", True, (235, 215, 175))
            self.screen.blit(name_s, (lx + 30, ly + 5))

            # Rarity + category
            rar_s = small.render(lot.rarity.upper(), True, rar_brd)
            self.screen.blit(rar_s, (lx + 30, ly + 19))
            cat_s = small.render(CATEGORY_LABELS.get(lot.category, ""), True, _MUTED)
            self.screen.blit(cat_s, (lx + 30 + rar_s.get_width() + 8, ly + 19))

            # Est. price hint
            est_s = small.render(f"est. {lot.base_price}g", True, _MUTED)
            self.screen.blit(est_s, (lx + lw - est_s.get_width() - 6, ly + 5))

            # Bid tier buttons
            cur_tier = self._bazaar_bids[i]
            bw, bgap = 62, 4
            for t in range(4):
                amt   = _bid_amount(lot, t)
                bx    = lx + 6 + t * (bw + bgap)
                brect = pygame.Rect(bx, ly + 46, bw, 20)
                sel   = (cur_tier == t)
                bg    = _TIER_BG_SEL[t] if sel else _TIER_BG_IDLE
                brd   = _TIER_BRD_SEL[t] if sel else _TIER_BRD_IDLE
                pygame.draw.rect(self.screen, bg,  brect, border_radius=3)
                pygame.draw.rect(self.screen, brd, brect, 1, border_radius=3)
                if t == 0:
                    lbl_s = small.render("PASS", True, (190, 175, 145) if sel else (100, 90, 75))
                else:
                    lbl_s = small.render(f"{amt}g", True, (240, 220, 160) if sel else (130, 120, 90))
                self.screen.blit(lbl_s, (brect.centerx - lbl_s.get_width() // 2,
                                         brect.centery - lbl_s.get_height() // 2))
                self._bazaar_rects[("bid", i, t)] = brect

        # ---- Right: fence panel ----
        fence_hdr = small.render("FENCE  —  Buying Today", True, _SAND)
        self.screen.blit(fence_hdr, (RIGHT_X, py + 48))

        for fi, slot in enumerate(self._bazaar_fence_wants):
            f_id, f_qty, f_pay, f_flavor = slot
            fy     = py + 66 + fi * 72
            frect  = pygame.Rect(RIGHT_X, fy, RIGHT_W, 66)
            sold   = fi in self._bazaar_fence_sold
            f_bg   = (28, 22, 12) if not sold else (22, 22, 22)
            f_brd  = _BORDER    if not sold else (55, 50, 45)
            pygame.draw.rect(self.screen, f_bg,  frect, border_radius=3)
            pygame.draw.rect(self.screen, f_brd, frect, 1, border_radius=3)

            f_name = f_id.replace("_", " ").title()
            fn_s   = small.render(f"{f_qty}×  {f_name}", True,
                                  (225, 205, 160) if not sold else (100, 95, 85))
            fp_s   = small.render(f"Pays {f_pay * f_qty}g total", True,
                                  _GOLD if not sold else (90, 85, 60))
            ff_s   = small.render(f_flavor, True, _MUTED if not sold else (70, 68, 60))
            self.screen.blit(fn_s, (RIGHT_X + 6, fy + 4))
            self.screen.blit(fp_s, (RIGHT_X + 6, fy + 18))
            self.screen.blit(ff_s, (RIGHT_X + 6, fy + 32))

            if sold:
                sold_s = small.render("SOLD", True, (160, 160, 140))
                self.screen.blit(sold_s, (RIGHT_X + RIGHT_W - sold_s.get_width() - 8, fy + 24))
            else:
                inv      = getattr(player, "inventory", {})
                have     = inv.get(f_id, 0)
                can_sell = have >= f_qty
                have_s   = small.render(f"Have: {have}", True,
                                        _WIN if can_sell else (155, 115, 80))
                self.screen.blit(have_s, (RIGHT_X + 6, fy + 48))

                sell_rect = pygame.Rect(RIGHT_X + RIGHT_W - 48, fy + 20, 44, 26)
                sb_bg  = (45, 72, 28) if can_sell else (35, 35, 30)
                sb_brd = (90, 170, 50) if can_sell else (60, 55, 45)
                pygame.draw.rect(self.screen, sb_bg,  sell_rect, border_radius=3)
                pygame.draw.rect(self.screen, sb_brd, sell_rect, 1, border_radius=3)
                sl_s = small.render("SELL", True, (170, 235, 110) if can_sell else (85, 80, 70))
                self.screen.blit(sl_s, (sell_rect.centerx - sl_s.get_width() // 2,
                                        sell_rect.centery - sl_s.get_height() // 2))
                if can_sell:
                    self._bazaar_rects[("fence_sell", fi)] = sell_rect

        # ---- Right: rival names strip ----
        rival_y = py + 66 + 3 * 72 + 6
        if self._bazaar_rivals:
            riv_s = small.render("Rivals:  " + "  ·  ".join(self._bazaar_rivals), True, _MUTED)
            self.screen.blit(riv_s, (RIGHT_X, rival_y))

        # ---- Right: gold + action buttons ----
        total_bid  = sum(_bid_amount(l, t) for l, t in zip(self._bazaar_lots, self._bazaar_bids))
        affordable = player.money >= total_bid

        gold_y = py + ph - 108
        gold_s = small.render(f"Your gold: {player.money}g", True, (200, 175, 100))
        self.screen.blit(gold_s, (RIGHT_X, gold_y))
        if total_bid > 0:
            bid_col = (200, 225, 100) if affordable else (230, 100, 80)
            bid_s   = small.render(f"Max outlay: {total_bid}g", True, bid_col)
            self.screen.blit(bid_s, (RIGHT_X, gold_y + 16))

        attend_rect = pygame.Rect(RIGHT_X, py + ph - 84, RIGHT_W, 36)
        a_bg  = (58, 43, 13) if affordable else (40, 35, 25)
        a_brd = _GOLD        if affordable else (80, 70, 50)
        pygame.draw.rect(self.screen, a_bg,  attend_rect, border_radius=4)
        pygame.draw.rect(self.screen, a_brd, attend_rect, 1, border_radius=4)
        al = font.render("ATTEND AUCTION", True, (240, 220, 150) if affordable else (115, 105, 80))
        self.screen.blit(al, (attend_rect.centerx - al.get_width() // 2,
                               attend_rect.centery - al.get_height() // 2))
        self._bazaar_rects["attend"] = attend_rect

        leave_rect = pygame.Rect(RIGHT_X, py + ph - 42, RIGHT_W, 28)
        pygame.draw.rect(self.screen, (48, 24, 14), leave_rect, border_radius=3)
        pygame.draw.rect(self.screen, (125, 82, 58), leave_rect, 1, border_radius=3)
        ll = small.render("Leave", True, (200, 160, 130))
        self.screen.blit(ll, (leave_rect.centerx - ll.get_width() // 2,
                               leave_rect.centery - ll.get_height() // 2))
        self._bazaar_rects["leave"] = leave_rect

    # -----------------------------------------------------------------------
    # Resolve phase
    # -----------------------------------------------------------------------

    def _draw_bazaar_resolve(self, player, dt, px, py, pw, ph):
        self._bazaar_rects = {}
        small = self.small

        hdr_s = self.font.render("AUCTION IN PROGRESS", True, _SAND)
        self.screen.blit(hdr_s, (px + pw // 2 - hdr_s.get_width() // 2, py + 48))

        log_box = pygame.Rect(px + 30, py + 74, pw - 60, ph - 140)
        pygame.draw.rect(self.screen, (20, 14, 8), log_box, border_radius=4)
        pygame.draw.rect(self.screen, _BORDER, log_box, 1, border_radius=4)

        line_h  = 19
        visible = (log_box.height - 12) // line_h
        log     = self._bazaar_resolve_log
        revealed = log[:self._bazaar_reveal_idx]
        start_i  = max(0, len(revealed) - visible)

        _tag_colors = {
            "header": (230, 210, 170),
            "rival":  (175, 160, 125),
            "win":    _WIN,
            "loss":   _LOSS,
            "pass":   _PASS_COL,
        }
        for li, (text, tag) in enumerate(revealed[start_i:]):
            col = _tag_colors.get(tag, _SAND)
            self.screen.blit(small.render(text, True, col),
                             (log_box.x + 10, log_box.y + 8 + li * line_h))

        # Advance reveal timer
        self._bazaar_reveal_timer += dt
        if self._bazaar_reveal_timer >= 0.85 and self._bazaar_reveal_idx < len(log):
            self._bazaar_reveal_idx  += 1
            self._bazaar_reveal_timer = 0.0
        elif self._bazaar_reveal_idx >= len(log) and not self._bazaar_reveal_done:
            self._bazaar_reveal_done  = True
            self._bazaar_reveal_timer = 0.0
        elif self._bazaar_reveal_done and self._bazaar_reveal_timer >= 1.2:
            self._resolve_bazaar_result(player)
            self._bazaar_phase = "result"

        # Skip button
        skip_rect = pygame.Rect(px + pw - 112, py + ph - 46, 92, 28)
        pygame.draw.rect(self.screen, (50, 38, 18), skip_rect, border_radius=3)
        pygame.draw.rect(self.screen, (110, 88, 50), skip_rect, 1, border_radius=3)
        sk_s = small.render("SKIP", True, (185, 160, 100))
        self.screen.blit(sk_s, (skip_rect.centerx - sk_s.get_width() // 2,
                                  skip_rect.centery - sk_s.get_height() // 2))
        self._bazaar_rects["skip"] = skip_rect

    # -----------------------------------------------------------------------
    # Result phase
    # -----------------------------------------------------------------------

    def _draw_bazaar_result(self, player, px, py, pw, ph):
        self._bazaar_rects = {}
        font, small = self.font, self.small

        n_won    = len(self._bazaar_won_lots)
        hdr_text = (f"YOU WON {n_won} LOT{'S' if n_won != 1 else ''}!"
                    if n_won > 0 else "AUCTION CLOSED")
        hdr_col  = _GOLD if n_won > 0 else _SAND
        hdr_s    = font.render(hdr_text, True, hdr_col)
        cy       = py + 50
        self.screen.blit(hdr_s, (px + pw // 2 - hdr_s.get_width() // 2, cy))
        cy += 30

        if self._bazaar_won_lots:
            lbl_s = small.render("Items acquired:", True, _SAND)
            self.screen.blit(lbl_s, (px + pw // 2 - 120, cy))
            cy += 18

            for lot, player_bid in self._bazaar_won_lots:
                rar_col  = RARITY_COLORS.get(lot.rarity, (180, 180, 180))
                rar_bg   = RARITY_BG.get(lot.rarity, (35, 35, 35))
                item_r   = pygame.Rect(px + pw // 2 - 160, cy, 320, 32)
                pygame.draw.rect(self.screen, rar_bg,  item_r, border_radius=3)
                pygame.draw.rect(self.screen, rar_col, item_r, 1, border_radius=3)
                pygame.draw.rect(self.screen, lot.swatch_color,
                                 (item_r.x + 6, item_r.y + 7, 16, 16), border_radius=2)
                i_s = small.render(f"{lot.display_name}  ×{lot.qty}", True, (230, 215, 175))
                self.screen.blit(i_s, (item_r.x + 28, item_r.y + 10))
                p_s = small.render(f"{player_bid}g", True, (195, 165, 75))
                self.screen.blit(p_s, (item_r.right - p_s.get_width() - 8, item_r.y + 10))
                cy += 36
        else:
            none_s = small.render("No lots won this session.", True, _MUTED)
            self.screen.blit(none_s, (px + pw // 2 - none_s.get_width() // 2, cy + 8))
            cy += 28

        cy += 10
        spent_s = small.render(f"Gold spent at auction: {self._bazaar_gold_spent}g", True, _SAND)
        self.screen.blit(spent_s, (px + pw // 2 - spent_s.get_width() // 2, cy))
        cy += 18
        if self._bazaar_fence_earned > 0:
            fence_s = small.render(f"Fence earnings: +{self._bazaar_fence_earned}g", True, _WIN)
            self.screen.blit(fence_s, (px + pw // 2 - fence_s.get_width() // 2, cy))

        leave_rect = pygame.Rect(px + pw // 2 - 70, py + ph - 52, 140, 36)
        pygame.draw.rect(self.screen, (52, 28, 16), leave_rect, border_radius=4)
        pygame.draw.rect(self.screen, (148, 98, 68), leave_rect, 1, border_radius=4)
        ll = font.render("Leave", True, (220, 180, 150))
        self.screen.blit(ll, (leave_rect.centerx - ll.get_width() // 2,
                               leave_rect.centery - ll.get_height() // 2))
        self._bazaar_rects["leave"] = leave_rect

    # -----------------------------------------------------------------------
    # Resolution logic
    # -----------------------------------------------------------------------

    def _build_resolve_log(self):
        """Pre-compute all auction outcomes and build the animated log."""
        log     = []
        results = []
        rivals  = self._bazaar_rivals

        for i, (lot, tier) in enumerate(zip(self._bazaar_lots, self._bazaar_bids)):
            player_bid  = _bid_amount(lot, tier)
            rival_name  = rivals[i % len(rivals)] if rivals else "a buyer"

            if player_bid == 0:
                log.append((f"Lot {i + 1}:  {lot.display_name} ×{lot.qty}  —  passed", "pass"))
                results.append((lot, 0, lot.rival_max, False))
                continue

            log.append((f"Lot {i + 1}:  {lot.display_name} ×{lot.qty}  —  bidding...", "header"))
            log.append((f"    {rival_name} bids {lot.rival_max}g...", "rival"))

            won = player_bid >= lot.rival_max
            if won:
                log.append((f"    You: {player_bid}g  |  Rivals: {lot.rival_max}g  →  YOU WIN!", "win"))
            else:
                log.append((f"    You: {player_bid}g  |  Rivals: {lot.rival_max}g  →  OUTBID", "loss"))
            results.append((lot, player_bid, lot.rival_max, won))

        self._bazaar_resolve_log     = log
        self._bazaar_resolve_results = results

    def _resolve_bazaar_result(self, player):
        """Apply won lots to player inventory and deduct gold."""
        won_lots    = []
        total_spent = 0
        inv = getattr(player, "inventory", {})

        for lot, player_bid, rival_bid, won in self._bazaar_resolve_results:
            if won and player_bid > 0:
                inv[lot.item_id] = inv.get(lot.item_id, 0) + lot.qty
                total_spent     += player_bid
                won_lots.append((lot, player_bid))

        player.money = max(0, player.money - total_spent)
        self._bazaar_won_lots   = won_lots
        self._bazaar_gold_spent = total_spent

    # -----------------------------------------------------------------------
    # Click and key handlers
    # -----------------------------------------------------------------------

    def handle_bazaar_click(self, pos, player):
        for key, rect in self._bazaar_rects.items():
            if not rect.collidepoint(pos):
                continue

            if self._bazaar_phase == "floor":
                if isinstance(key, tuple) and key[0] == "bid":
                    _, lot_i, tier = key
                    self._bazaar_bids[lot_i] = tier

                elif isinstance(key, tuple) and key[0] == "fence_sell":
                    self._do_fence_sell(player, key[1])

                elif key == "attend":
                    total = sum(_bid_amount(l, t)
                                for l, t in zip(self._bazaar_lots, self._bazaar_bids))
                    if player.money >= total:
                        self._build_resolve_log()
                        self._bazaar_reveal_idx   = 0
                        self._bazaar_reveal_timer = 0.0
                        self._bazaar_reveal_done  = False
                        self._bazaar_phase = "resolve"

                elif key == "leave":
                    self.bazaar_open = False

            elif self._bazaar_phase == "resolve":
                if key == "skip":
                    self._bazaar_reveal_idx = len(self._bazaar_resolve_log)
                    self._resolve_bazaar_result(player)
                    self._bazaar_phase = "result"

            elif self._bazaar_phase == "result":
                if key == "leave":
                    self.bazaar_open = False
            break

    def _do_fence_sell(self, player, fence_idx):
        if fence_idx in self._bazaar_fence_sold:
            return
        f_id, f_qty, f_pay, _ = self._bazaar_fence_wants[fence_idx]
        inv = getattr(player, "inventory", {})
        if inv.get(f_id, 0) >= f_qty:
            inv[f_id] = inv[f_id] - f_qty
            total     = f_pay * f_qty
            player.money += total
            self._bazaar_fence_earned += total
            self._bazaar_fence_sold.add(fence_idx)

    def handle_bazaar_keydown(self, key, player):
        if key == pygame.K_ESCAPE:
            if self._bazaar_phase == "resolve":
                self._bazaar_reveal_idx = len(self._bazaar_resolve_log)
                self._resolve_bazaar_result(player)
                self._bazaar_phase = "result"
            else:
                self.bazaar_open = False
