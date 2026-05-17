"""
UI/chapter_house.py — Chapter House (in-city) panel.

A focused UI for joining a Knightly Order, accepting tradition-flavored
quests, turning them in, and watching prestige unlock new ranks.

Opened by the ChapterMasterNPC who lives in the Knights' Hall building of
every medium+ city — the order shown is the order seated in that town's
region (resolved via knightly_orders.order_for_town).
"""

import pygame

from constants import SCREEN_W, SCREEN_H
import heraldry
import knightly_orders as ko
from .panels import _wrap_text


_BG       = (24, 22, 18)
_BORDER   = (160, 130, 80)
_TITLE_C  = (240, 220, 160)
_LABEL_C  = (200, 185, 140)
_DIM_C    = (110, 100, 75)
_WHITE    = (240, 240, 230)
_OK_C     = (160, 200, 130)
_WARN_C   = (220, 140,  90)
_BTN_BG   = (140, 110,  50)
_BTN_OFF  = ( 70,  65,  55)

_PW = 520
_PH = 460
_COA_W = 180


class ChapterHouseMixin:
    """Drawing + click handling for chapter_house outposts."""

    REROLL_COST = 5  # gold per reroll
    MAX_VOWS = 2     # how many vows the player may swear at petition

    def _ch_init_rects(self):
        self._ch_petition_rect = None
        self._ch_accept_rect   = None
        self._ch_turnin_rect   = None
        self._ch_abandon_rect  = None
        self._ch_leave_rect    = None
        self._ch_reroll_rect   = None
        self._ch_vow_rects     = {}      # vow text -> Rect
        self._ch_swear_rect    = None
        self._ch_cancel_rect   = None
        self._ch_open_trial_rect = None
        self._ch_trial_turnin_rect = None
        self._ch_msg           = getattr(self, "_ch_msg", "")
        # Transient vow-picker state (not persisted; lives until close)
        if not hasattr(self, "_ch_vow_picking"):
            self._ch_vow_picking = False
            self._ch_vow_selected = []
        # Quartermaster shop state
        if not hasattr(self, "_ch_tab"):
            self._ch_tab = "quests"   # "quests" | "shop"
        if not hasattr(self, "_ch_shop_scroll"):
            self._ch_shop_scroll = 0
        self._ch_tab_quests_rect = None
        self._ch_tab_shop_rect   = None
        self._ch_shop_buy_rects  = {}   # item_id -> (Rect, price)

    def _draw_chapter_house_panel(self, player):
        """Replaces the NPC panel when active_npc is a ChapterMasterNPC. Returns True."""
        npc = self.active_npc
        if npc is None:
            return False
        self._ch_init_rects()

        town_id = getattr(npc, "town_id", None)
        if town_id is None:
            town_id = npc._nearest_town_id() or 0
        from constants import BLOCK_SIZE
        bx = int(npc.x / BLOCK_SIZE)
        order = ko.order_for_town(town_id, bx=bx)
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        total_w = _PW + 12 + _COA_W
        px = (SCREEN_W - total_w) // 2
        py = (SCREEN_H - _PH) // 2

        pygame.draw.rect(self.screen, _BG,     (px, py, _PW, _PH))
        pygame.draw.rect(self.screen, _BORDER, (px, py, _PW, _PH), 2)

        if order is None:
            msg = self.font.render("No knightly orders abide here.", True, _DIM_C)
            self.screen.blit(msg, (px + 16, py + 20))
            return True

        # ── Header
        title = self.font.render(order.name, True, _TITLE_C)
        self.screen.blit(title, (px + 16, py + 14))
        seat_s = self.small.render(order.seat or "Chapter House", True, _DIM_C)
        self.screen.blit(seat_s, (px + 16, py + 38))

        trad = ko.ORDER_TRADITIONS.get(order.tradition, {})
        motto_s = self.small.render(f"“{order.motto}”", True, (190, 175, 130))
        self.screen.blit(motto_s, (px + 16, py + 56))

        sep_y = py + 78
        pygame.draw.line(self.screen, _BORDER, (px + 10, sep_y),
                         (px + _PW - 10, sep_y))

        # ── Member status
        is_member = (getattr(player, "order_id", 0) == order.order_id)
        in_other  = (not is_member and getattr(player, "order_id", 0))

        y = sep_y + 12
        if is_member:
            prestige = player.order_prestige
            eff_idx = ko.player_effective_rank_idx(player)
            rank_lbl = ko.player_rank_label(order.order_id, prestige,
                                             rank_idx=eff_idx)
            standing = ko.standing_label(prestige)
            head = self.font.render(
                f"{rank_lbl}  ·  {standing}", True, _OK_C)
            self.screen.blit(head, (px + 16, y))
            y += 24

            nxt = ko.next_rank_threshold(prestige)
            if nxt is None:
                p_s = self.small.render(
                    f"Prestige {prestige} — top of the order.", True, _LABEL_C)
            else:
                p_s = self.small.render(
                    f"Prestige {prestige}/{nxt} to next rank.", True, _LABEL_C)
            self.screen.blit(p_s, (px + 16, y))
            y += 18
            vows = getattr(player, "order_vows", []) or []
            bonus = ko.vow_prestige_bonus(vows)
            if vows:
                v_lbl = self.small.render(
                    f"Vows held: {len(vows)} (+{bonus} prestige per quest)",
                    True, (200, 200, 130))
                self.screen.blit(v_lbl, (px + 16, y))
                y += 16
                for v in vows:
                    for ln in _wrap_text(f"  • {v}", self.small, _PW - 36):
                        s = self.small.render(ln, True, (165, 160, 130))
                        self.screen.blit(s, (px + 16, y))
                        y += 14
            done_s = self.small.render(
                f"Quests completed: {player.order_quests_done}",
                True, _DIM_C)
            self.screen.blit(done_s, (px + 16, y))
            y += 16

            # ── Rank Trial (gates promotion at threshold)
            y = self._draw_trial_block(player, order, px, y)
            y += 6
        elif in_other:
            other = ko.order(player.order_id)
            name = other.name if other else "another order"
            warn = self.small.render(
                f"You are sworn to {name}. Leave that order first.",
                True, _WARN_C)
            self.screen.blit(warn, (px + 16, y))
            y += 22
        else:
            desc = trad.get("desc", "")
            for ln in _wrap_text(desc, self.small, _PW - 32):
                s = self.small.render(ln, True, _LABEL_C)
                self.screen.blit(s, (px + 16, y))
                y += 16
            y += 4
            init_rite = ko.order_initiation_rite(order.order_id)
            for ln in _wrap_text(f"Initiation: {init_rite}",
                                 self.small, _PW - 32):
                s = self.small.render(ln, True, (170, 160, 120))
                self.screen.blit(s, (px + 16, y))
                y += 16
            y += 6

        # ── Tabs + content (members only)
        if is_member:
            ty = y + 4
            pygame.draw.line(self.screen, _BORDER, (px + 10, ty),
                             (px + _PW - 10, ty))
            ty += 8
            self._ch_tab_quests_rect = self._draw_tab_btn(
                px + 16, ty, 140, 26, "Quest Board", self._ch_tab == "quests")
            self._ch_tab_shop_rect = self._draw_tab_btn(
                px + 16 + 148, ty, 160, 26, "Quartermaster", self._ch_tab == "shop")
            ty += 32

            if self._ch_tab == "shop":
                self._draw_quartermaster(player, px, ty)
            else:
                self._draw_quest_board(player, order, px, ty)

        # ── Vow picker (overlay on petition flow)
        if self._ch_vow_picking and not is_member and not in_other:
            y = self._draw_vow_picker(order, px, sep_y + 12)

        # ── Footer buttons
        fy = py + _PH - 44
        if not is_member and not in_other and not self._ch_vow_picking:
            self._ch_petition_rect = self._draw_btn(
                px + 16, fy, 200, 30, "Petition for Membership", True)
        elif self._ch_vow_picking:
            ready = 1 <= len(self._ch_vow_selected) <= self.MAX_VOWS
            self._ch_swear_rect = self._draw_btn(
                px + 16, fy, 160, 30,
                f"Swear ({len(self._ch_vow_selected)})", ready)
            self._ch_cancel_rect = self._draw_btn(
                px + 16 + 170, fy, 110, 30, "Cancel", True)
        elif is_member:
            self._ch_leave_rect = self._draw_btn(
                px + _PW - 16 - 140, fy, 140, 30, "Leave Order", True)

        if self._ch_msg:
            ms = self.small.render(self._ch_msg, True, (235, 220, 140))
            self.screen.blit(ms, (px + 16, py + _PH - 64))

        hint = self.small.render("[E] or [ESC] to close",
                                 True, _DIM_C)
        self.screen.blit(hint, (px + _PW - hint.get_width() - 16,
                                py + _PH - 22))

        # ── Coat of Arms card
        cx = px + _PW + 12
        self._draw_ch_coa_card(order, cx, py)
        return True

    def _draw_ch_coa_card(self, order, cx, cy):
        pygame.draw.rect(self.screen, _BG,     (cx, cy, _COA_W, _PH))
        pygame.draw.rect(self.screen, _BORDER, (cx, cy, _COA_W, _PH), 2)
        lbl = self.small.render("Order Heraldry", True, _DIM_C)
        self.screen.blit(lbl, (cx + (_COA_W - lbl.get_width()) // 2, cy + 10))
        shield_w = 140
        shield_h = 180
        shield_x = cx + (_COA_W - shield_w) // 2
        shield_y = cy + 36
        try:
            heraldry.draw(self.screen, shield_x, shield_y, shield_w, shield_h,
                          order.heraldry)
        except Exception:
            pass
        ty = shield_y + shield_h + 12
        trad_lbl = self.small.render(
            ko.ORDER_TRADITIONS.get(order.tradition, {}).get("desc",
                                                              order.tradition)[:60],
            True, _LABEL_C)
        for ln in _wrap_text(order.tradition.title(),
                             self.font, _COA_W - 12):
            s = self.font.render(ln, True, _TITLE_C)
            self.screen.blit(s, (cx + (_COA_W - s.get_width()) // 2, ty))
            ty += 20
        for ln in _wrap_text(f"Patron: {order.patron}", self.small,
                             _COA_W - 16):
            s = self.small.render(ln, True, _LABEL_C)
            self.screen.blit(s, (cx + 8, ty))
            ty += 14
        for ln in _wrap_text(f"Relic: {order.relic}", self.small,
                             _COA_W - 16):
            s = self.small.render(ln, True, _LABEL_C)
            self.screen.blit(s, (cx + 8, ty))
            ty += 14
        pres = self.small.render(f"Order prestige: {order.prestige}",
                                 True, _DIM_C)
        self.screen.blit(pres, (cx + 8, cy + _PH - 22))

    def _draw_btn(self, x, y, w, h, label, enabled):
        col = _BTN_BG if enabled else _BTN_OFF
        pygame.draw.rect(self.screen, col, (x, y, w, h), border_radius=4)
        s = self.small.render(label, True, _WHITE)
        self.screen.blit(s, (x + (w - s.get_width()) // 2,
                             y + (h - s.get_height()) // 2))
        return pygame.Rect(x, y, w, h) if enabled else None

    def _draw_tab_btn(self, x, y, w, h, label, active):
        bg  = (60, 50, 32) if active else (32, 28, 22)
        brd = _TITLE_C if active else _DIM_C
        pygame.draw.rect(self.screen, bg, (x, y, w, h))
        pygame.draw.rect(self.screen, brd, (x, y, w, h), 2 if active else 1)
        s = self.small.render(label, True, _TITLE_C if active else _LABEL_C)
        self.screen.blit(s, (x + (w - s.get_width()) // 2,
                             y + (h - s.get_height()) // 2))
        return pygame.Rect(x, y, w, h)

    def _draw_quest_board(self, player, order, px, qy):
        board = self.font.render("Quest Board", True, _TITLE_C)
        self.screen.blit(board, (px + 16, qy))
        qy += 26

        day = getattr(player.world, "day_count", 0)
        rank_idx = ko.player_rank_idx(player.order_prestige)
        quest = player.order_quest
        if quest is None:
            refresh = getattr(player, "order_reroll_count", 0)
            quest = ko.roll_order_quest(order.order_id, day,
                                         rank_idx=rank_idx,
                                         refresh=refresh)

        self._ch_active_quest_preview = quest

        if quest:
            tier = quest.get("tier", 0)
            tier_lbl = f"Tier {tier} · {quest.get('kind','quest').title()}"
            ts = self.small.render(tier_lbl, True, (210, 175, 80))
            self.screen.blit(ts, (px + 16, qy))
            qy += 16
            lines = _wrap_text(quest["summary"], self.small, _PW - 32)
            for ln in lines:
                s = self.small.render(ln, True, _WHITE)
                self.screen.blit(s, (px + 16, qy))
                qy += 16
            qy += 4
            rew = self.small.render(
                f"Reward: {quest['prestige']} prestige, {quest['gold']}g",
                True, _LABEL_C)
            self.screen.blit(rew, (px + 16, qy))
            qy += 22

            accepted = (player.order_quest is not None
                        and player.order_quest.get("order_id") == order.order_id)
            if not accepted:
                self._ch_accept_rect = self._draw_btn(
                    px + 16, qy, 180, 30, "Accept Quest", True)
                can_reroll = player.money >= self.REROLL_COST
                self._ch_reroll_rect = self._draw_btn(
                    px + 16 + 190, qy, 150, 30,
                    f"Reroll ({self.REROLL_COST}g)", can_reroll)
            else:
                progress = self._ch_quest_progress(player, player.order_quest)
                p_s = self.small.render(progress["text"], True, _LABEL_C)
                self.screen.blit(p_s, (px + 16, qy))
                qy += 22
                can_turn = progress["complete"]
                self._ch_turnin_rect = self._draw_btn(
                    px + 16, qy, 180, 30, "Turn In", can_turn)
                self._ch_abandon_rect = self._draw_btn(
                    px + 16 + 190, qy, 130, 30, "Abandon", True)

    def _draw_quartermaster(self, player, px, qy):
        """Render the rank-gated provisioner shop."""
        from items import ITEMS as _ITEMS
        rank_idx = ko.player_effective_rank_idx(player)
        offers = ko.quartermaster_offers_for_rank(rank_idx)

        title = self.font.render("Quartermaster's Provisions", True, _TITLE_C)
        self.screen.blit(title, (px + 16, qy))
        qy += 22
        sub = self.small.render(
            f"Stocking ranks 1..{min(rank_idx,4)} — your gold: {int(getattr(player,'money',0))}g",
            True, _LABEL_C)
        self.screen.blit(sub, (px + 16, qy))
        qy += 18

        if not offers:
            note = self.small.render(
                "Rank up to unlock the quartermaster's shelves.", True, _DIM_C)
            self.screen.blit(note, (px + 16, qy + 8))
            return

        # Scrollable list (no scrollbar UI yet — wheel handler can adjust _ch_shop_scroll).
        rows_visible = 11
        row_h = 22
        list_top = qy
        list_bot = qy + rows_visible * row_h
        scroll = max(0, min(self._ch_shop_scroll, max(0, len(offers) - rows_visible)))
        self._ch_shop_scroll = scroll
        self._ch_shop_buy_rects.clear()
        for idx, (item_id, price, min_rank) in enumerate(offers[scroll:scroll + rows_visible]):
            row_y = list_top + idx * row_h
            name = _ITEMS.get(item_id, {}).get("name", item_id)
            color = _ITEMS.get(item_id, {}).get("color", _LABEL_C)
            # Rank pip
            rank_s = self.small.render(f"r{min_rank}", True, _DIM_C)
            self.screen.blit(rank_s, (px + 14, row_y + 4))
            # Item name (truncate)
            n_s = self.small.render(name[:36], True, color)
            self.screen.blit(n_s, (px + 44, row_y + 4))
            # Price
            can_afford = int(getattr(player, "money", 0)) >= price
            p_col = _OK_C if can_afford else _WARN_C
            p_s = self.small.render(f"{price}g", True, p_col)
            self.screen.blit(p_s, (px + _PW - 130, row_y + 4))
            # Buy button
            btn = self._draw_btn(px + _PW - 84, row_y, 64, row_h - 2,
                                 "Buy", can_afford)
            if btn is not None:
                self._ch_shop_buy_rects[item_id] = (btn, price)

        # Scroll hint
        if len(offers) > rows_visible:
            hint = self.small.render(
                f"({scroll + 1}-{min(scroll + rows_visible, len(offers))} of {len(offers)} · mouse wheel)",
                True, _DIM_C)
            self.screen.blit(hint, (px + 16, list_bot + 4))

    def _ch_quest_progress(self, player, quest) -> dict:
        if quest.get("kill_kind") == "joust_win":
            baseline = quest.get("joust_baseline", 0)
            won = max(0, getattr(player, "order_joust_wins", 0) - baseline)
            need = quest["count"]
            return {
                "complete": won >= need,
                "text": f"Joust wins since accept: {won}/{need}",
            }
        item_id = quest["item_id"]
        need = quest["count"]
        have = self._ch_count_item(player, item_id)
        return {
            "complete": have >= need,
            "text":     f"{item_id.replace('_', ' ').title()}: {have}/{need}",
        }

    def _ch_count_item(self, player, item_id: str) -> int:
        return int(player.inventory.get(item_id, 0))

    def _ch_consume_item(self, player, item_id: str, count: int) -> bool:
        have = int(player.inventory.get(item_id, 0))
        if have < count:
            return False
        player.inventory[item_id] = have - count
        if player.inventory[item_id] <= 0:
            del player.inventory[item_id]
        return True

    # ──────────────────────────────────────────────────────────────────────
    # Vow picker — shown after Petition pressed, before swearing in.
    # ──────────────────────────────────────────────────────────────────────

    def _draw_vow_picker(self, order, px, y):
        title = self.font.render("Choose your Vows", True, _TITLE_C)
        self.screen.blit(title, (px + 16, y))
        y += 24
        hint = self.small.render(
            f"Pick 1-{self.MAX_VOWS}. Each vow gives +1 prestige per quest turned in.",
            True, _DIM_C)
        self.screen.blit(hint, (px + 16, y))
        y += 18

        candidates = ko.candidate_vows_for_order(order.order_id, k=4)
        self._ch_vow_rects = {}
        for vow in candidates:
            chosen = vow in self._ch_vow_selected
            box_h = max(28, 14 * max(1, len(_wrap_text(vow, self.small, _PW - 60))))
            r = pygame.Rect(px + 16, y, _PW - 32, box_h + 6)
            bg = (50, 50, 38) if chosen else (32, 30, 26)
            border = (200, 175, 90) if chosen else (90, 80, 60)
            pygame.draw.rect(self.screen, bg, r)
            pygame.draw.rect(self.screen, border, r, 1)
            ty = y + 6
            for ln in _wrap_text(vow, self.small, _PW - 60):
                s = self.small.render(ln, True, _WHITE if chosen else _LABEL_C)
                self.screen.blit(s, (px + 30, ty))
                ty += 14
            mark = "●" if chosen else "○"
            ms = self.small.render(mark, True,
                                   (240, 200, 100) if chosen else _DIM_C)
            self.screen.blit(ms, (px + 22, y + 8))
            self._ch_vow_rects[vow] = r
            y += box_h + 12
        return y

    def _toggle_vow(self, vow):
        if vow in self._ch_vow_selected:
            self._ch_vow_selected.remove(vow)
        elif len(self._ch_vow_selected) < self.MAX_VOWS:
            self._ch_vow_selected.append(vow)

    # ──────────────────────────────────────────────────────────────────────
    # Rank Trial block — gates promotion past the prestige threshold.
    # ──────────────────────────────────────────────────────────────────────

    def _draw_trial_block(self, player, order, px, y):
        # Determine the next rank that needs a trial.
        passed = int(getattr(player, "order_passed_trials", 0))
        by_prestige = ko.player_rank_idx(player.order_prestige)
        if passed >= by_prestige or passed >= len(ko.RANK_THRESHOLDS) - 1:
            return y  # nothing to show — either no trial unlocked, or maxed.

        target_rank = passed + 1
        trial_def = ko.rank_trial_for(target_rank)
        if trial_def is None:
            return y
        label, kind, count, item_id, flavor = trial_def

        pygame.draw.line(self.screen, _BORDER, (px + 10, y),
                         (px + _PW - 10, y))
        y += 8
        head = self.font.render(label, True, (240, 200, 110))
        self.screen.blit(head, (px + 16, y))
        y += 22
        for ln in _wrap_text(flavor, self.small, _PW - 32):
            s = self.small.render(ln, True, _LABEL_C)
            self.screen.blit(s, (px + 16, y))
            y += 14
        y += 4

        # Active trial state
        trial = player.order_trial
        is_active = (trial is not None
                     and trial.get("order_id") == order.order_id
                     and trial.get("rank") == target_rank)

        if not is_active:
            self._ch_open_trial_rect = self._draw_btn(
                px + 16, y, 180, 28, "Open Trial", True)
            y += 36
        else:
            progress = self._ch_trial_progress(player, trial, order)
            p_s = self.small.render(progress["text"], True, _LABEL_C)
            self.screen.blit(p_s, (px + 16, y))
            y += 18
            can_complete = progress["complete"]
            self._ch_trial_turnin_rect = self._draw_btn(
                px + 16, y, 180, 28, "Complete Trial", can_complete)
            y += 36
        return y

    def _ch_trial_progress(self, player, trial, order):
        kind = trial["kind"]
        need = trial["count"]
        if kind == "joust_win":
            won = max(0, getattr(player, "order_joust_wins", 0)
                          - trial.get("baseline", 0))
            return {"complete": won >= need,
                    "text": f"Joust wins since trial opened: {won}/{need}"}
        if kind == "joust_pennant":
            # Count wins under THIS order's pennant since trial opened.
            # We don't track per-pennant historical wins, so this trial
            # requires you to be currently flying the order's colors.
            flying = (getattr(player, "champion_order_id", None)
                      == order.order_id)
            won = max(0, getattr(player, "order_joust_wins", 0)
                          - trial.get("baseline", 0))
            ok = flying and won >= need
            tag = "(flying order colors)" if flying else "(must fly order pennant)"
            return {"complete": ok,
                    "text": f"Pennant wins since trial: {won}/{need} {tag}"}
        # tribute
        item_id = trial.get("item_id")
        have = self._ch_count_item(player, item_id) if item_id else 0
        return {"complete": have >= need,
                "text": f"{item_id.replace('_', ' ').title()}: {have}/{need}"}

    def _ch_open_trial(self, player, order):
        passed = int(getattr(player, "order_passed_trials", 0))
        target_rank = passed + 1
        trial_def = ko.rank_trial_for(target_rank)
        if trial_def is None:
            return
        label, kind, count, item_id, flavor = trial_def
        player.order_trial = {
            "order_id": order.order_id,
            "rank":     target_rank,
            "kind":     kind,
            "count":    count,
            "item_id":  item_id,
            "baseline": getattr(player, "order_joust_wins", 0),
            "label":    label,
        }
        self._ch_msg = f"{label} opened — earn it on the field."

    def _ch_complete_trial(self, player, order):
        trial = player.order_trial
        if trial is None:
            return
        progress = self._ch_trial_progress(player, trial, order)
        if not progress["complete"]:
            self._ch_msg = "Trial is not yet won."
            return
        if trial["kind"] == "tribute" and trial.get("item_id"):
            ok = self._ch_consume_item(player, trial["item_id"], trial["count"])
            if not ok:
                self._ch_msg = "Tribute could not be collected."
                return
        player.order_passed_trials = int(getattr(player, "order_passed_trials", 0)) + 1
        player.order_trial = None
        new_rank = player.order_passed_trials
        trad = order.tradition
        ceremony = ko.promotion_ceremony_line(trad, new_rank)
        rank_lbl = ko.player_rank_label(order.order_id, player.order_prestige,
                                         rank_idx=new_rank)
        grants = ko.grant_rank_rewards(player, trad, new_rank)
        if grants:
            from items import ITEMS as _ITEMS
            grant_lbl = ", ".join(_ITEMS.get(it, {}).get("name", it) for it, _ in grants[:3])
            extra = "" if len(grants) <= 3 else f" and {len(grants) - 3} more"
            self._ch_msg = (f"Trial passed. Raised to {rank_lbl} — {ceremony}. "
                            f"Granted: {grant_lbl}{extra}.")
        else:
            self._ch_msg = f"Trial passed. Raised to {rank_lbl} — {ceremony}."

    # ──────────────────────────────────────────────────────────────────────
    # Click handling — called from OutpostMenuMixin.handle_sommelier_click
    # ──────────────────────────────────────────────────────────────────────

    def _handle_chapter_house_click(self, pos, player) -> bool:
        npc = self.active_npc
        if npc is None:
            return False
        from cities import ChapterMasterNPC
        if not isinstance(npc, ChapterMasterNPC):
            return False
        town_id = getattr(npc, "town_id", None)
        if town_id is None:
            town_id = npc._nearest_town_id() or 0
        from constants import BLOCK_SIZE
        bx = int(npc.x / BLOCK_SIZE)
        order = ko.order_for_town(town_id, bx=bx)
        if order is None:
            return False

        r = getattr(self, "_ch_petition_rect", None)
        if r and r.collidepoint(pos):
            self._ch_petition(player, order)
            return True
        # Tab switching
        r = getattr(self, "_ch_tab_quests_rect", None)
        if r and r.collidepoint(pos):
            self._ch_tab = "quests"
            return True
        r = getattr(self, "_ch_tab_shop_rect", None)
        if r and r.collidepoint(pos):
            self._ch_tab = "shop"
            return True
        # Quartermaster buy clicks
        for item_id, (rect, price) in list(getattr(self, "_ch_shop_buy_rects", {}).items()):
            if rect.collidepoint(pos):
                from items import ITEMS as _ITEMS
                name = _ITEMS.get(item_id, {}).get("name", item_id)
                if ko.quartermaster_buy(player, item_id, price):
                    self._ch_msg = f"Bought {name} for {price}g."
                else:
                    self._ch_msg = f"Need {price}g for {name}."
                return True
        # Vow picker mode
        if getattr(self, "_ch_vow_picking", False):
            for vow, rect in self._ch_vow_rects.items():
                if rect.collidepoint(pos):
                    self._toggle_vow(vow)
                    return True
            if self._ch_swear_rect and self._ch_swear_rect.collidepoint(pos):
                self._ch_swear(player, order)
                return True
            if self._ch_cancel_rect and self._ch_cancel_rect.collidepoint(pos):
                self._ch_cancel_petition()
                return True
            return True  # swallow clicks while picking
        # Trial controls
        r = getattr(self, "_ch_open_trial_rect", None)
        if r and r.collidepoint(pos):
            self._ch_open_trial(player, order)
            return True
        r = getattr(self, "_ch_trial_turnin_rect", None)
        if r and r.collidepoint(pos):
            self._ch_complete_trial(player, order)
            return True
        r = getattr(self, "_ch_leave_rect", None)
        if r and r.collidepoint(pos):
            self._ch_leave(player)
            return True
        r = getattr(self, "_ch_accept_rect", None)
        if r and r.collidepoint(pos):
            self._ch_accept_quest(player, order)
            return True
        r = getattr(self, "_ch_turnin_rect", None)
        if r and r.collidepoint(pos):
            self._ch_turn_in_quest(player)
            return True
        r = getattr(self, "_ch_abandon_rect", None)
        if r and r.collidepoint(pos):
            player.order_quest = None
            self._ch_msg = "Quest abandoned."
            return True
        r = getattr(self, "_ch_reroll_rect", None)
        if r and r.collidepoint(pos):
            if player.money < self.REROLL_COST:
                self._ch_msg = "Not enough gold to reroll."
            else:
                player.money -= self.REROLL_COST
                player.order_reroll_count = getattr(player, "order_reroll_count", 0) + 1
                self._ch_msg = "Quest offering rerolled."
            return True
        return False

    def _ch_petition(self, player, order):
        # Opens the vow-picker; the actual swearing happens in _ch_swear.
        if getattr(player, "order_id", 0):
            self._ch_msg = "Already sworn to another order."
            return
        self._ch_vow_picking = True
        self._ch_vow_selected = []
        self._ch_msg = "Choose 1-2 vows to swear before the chapter."

    def _ch_swear(self, player, order):
        if not (1 <= len(self._ch_vow_selected) <= self.MAX_VOWS):
            return
        player.order_id = order.order_id
        player.order_prestige = 0
        player.order_quest = None
        player.order_quests_done = 0
        player.order_joust_wins = 0
        player.order_vows = list(self._ch_vow_selected)
        player.order_trial = None
        self._ch_vow_picking = False
        self._ch_vow_selected = []
        rite = ko.order_initiation_rite(order.order_id)
        self._ch_msg = f"Sworn to {order.name}. ({rite[:60]})"

    def _ch_cancel_petition(self):
        self._ch_vow_picking = False
        self._ch_vow_selected = []
        self._ch_msg = ""

    def _ch_leave(self, player):
        # Prestige hit on leaving — a knight who breaks vows is no longer
        # welcome at this seat.
        player.order_id = 0
        player.order_prestige = 0
        player.order_quest = None
        player.order_vows = []
        player.order_trial = None
        self._ch_msg = "You have set down the colors of the order."

    def _ch_accept_quest(self, player, order):
        day = getattr(player.world, "day_count", 0)
        rank_idx = ko.player_rank_idx(player.order_prestige)
        refresh = getattr(player, "order_reroll_count", 0)
        quest = ko.roll_order_quest(order.order_id, day,
                                     rank_idx=rank_idx, refresh=refresh)
        if quest is None:
            return
        if quest.get("kill_kind") == "joust_win":
            quest["joust_baseline"] = getattr(player, "order_joust_wins", 0)
        player.order_quest = quest
        self._ch_msg = "Quest accepted."

    def _ch_turn_in_quest(self, player):
        quest = player.order_quest
        if not quest:
            return
        progress = self._ch_quest_progress(player, quest)
        if not progress["complete"]:
            self._ch_msg = "Quest not yet complete."
            return
        if quest.get("kill_kind") != "joust_win":
            ok = self._ch_consume_item(player, quest["item_id"], quest["count"])
            if not ok:
                self._ch_msg = "Could not collect the required items."
                return
        old_rank = ko.player_rank_idx(player.order_prestige)
        vow_bonus = ko.vow_prestige_bonus(getattr(player, "order_vows", []))
        player.order_prestige += int(quest.get("prestige", 0)) + vow_bonus
        player.money = getattr(player, "money", 0) + int(quest.get("gold", 0))
        player.order_quests_done += 1
        player.order_quest = None
        new_rank = ko.player_rank_idx(player.order_prestige)
        if new_rank > old_rank:
            order = ko.order(player.order_id)
            rank_lbl = ko.player_rank_label(player.order_id, player.order_prestige)
            trad = order.tradition if order else "errant"
            ceremony = ko.promotion_ceremony_line(trad, new_rank)
            self._ch_msg = f"Raised to {rank_lbl} — {ceremony}."
            if order is not None:
                order.prestige = min(100, order.prestige + 2)
        else:
            self._ch_msg = (f"Quest complete. +{quest['prestige']} prestige, "
                            f"+{quest['gold']}g.")
