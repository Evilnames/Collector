import pygame
from items import ITEMS
from item_icons import render_item_icon
from rocks import (render_rock, RARITY_COLORS, ROCK_TYPE_ORDER, ROCK_TYPE_DESCRIPTIONS,
                   ROCK_TYPES, get_refinery_equipment)
from constants import SCREEN_W, SCREEN_H, HOTBAR_SIZE
from automations import AUTOMATION_ITEM
from ._data import RARITY_LABEL, SPECIAL_DESCS
from Render.dogs import draw_dog


def _wrap_text(text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        test = (cur + " " + word).strip()
        if font.size(test)[0] <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


class PanelsMixin:

    def _draw_npc_panel(self, player):
        from cities import (RockQuestNPC, TradeNPC, WildflowerQuestNPC, GemQuestNPC,
                            MerchantNPC, RestaurantNPC, ShrineKeeperNPC, JewelryMerchantNPC,
                            LeaderNPC, BlacksmithNPC, InnkeeperNPC, ScholarNPC,
                            RoyalCuratorNPC, RoyalFloristNPC, RoyalJewelerNPC,
                            RoyalPaleontologistNPC, RoyalAnglerNPC,
                            WeaponArmorerNPC, QuartermasterNPC, GarrisonCommanderNPC,
                            DoctorNPC)
        from outpost_npcs import OutpostKeeperNPC
        npc = self.active_npc
        if isinstance(npc, LeaderNPC):
            self._draw_leader_panel(player, npc)
            return

        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        self.screen.blit(overlay, (0, 0))

        is_quest = isinstance(npc, (RockQuestNPC, WildflowerQuestNPC, GemQuestNPC))
        is_outpost = isinstance(npc, OutpostKeeperNPC)
        PW = 660
        PH = 580 if is_outpost else (490 if is_quest else 460)
        px = (SCREEN_W - PW) // 2
        py = (SCREEN_H - PH) // 2

        # Border colour per NPC type — royal classes checked first
        if isinstance(npc, (RoyalCuratorNPC, RoyalFloristNPC, RoyalJewelerNPC,
                             RoyalPaleontologistNPC, RoyalAnglerNPC)):
            border_col = (220, 175, 40)
        elif isinstance(npc, WildflowerQuestNPC):
            border_col = (60, 140, 70)
        elif isinstance(npc, GemQuestNPC):
            border_col = (110, 50, 160)
        elif isinstance(npc, MerchantNPC):
            border_col = (180, 140, 40)
        elif isinstance(npc, RestaurantNPC):
            border_col = (200, 90, 30)
        elif isinstance(npc, ShrineKeeperNPC):
            border_col = (160, 130, 60)
        elif isinstance(npc, JewelryMerchantNPC):
            border_col = (200, 165, 55)
        elif isinstance(npc, WeaponArmorerNPC):
            border_col = (155, 140, 120)
        elif isinstance(npc, QuartermasterNPC):
            border_col = (100, 120, 140)
        elif isinstance(npc, GarrisonCommanderNPC):
            border_col = (160,  90,  70)
        elif isinstance(npc, BlacksmithNPC):
            border_col = (100, 110, 130)
        elif isinstance(npc, InnkeeperNPC):
            border_col = (170, 110, 50)
        elif isinstance(npc, ScholarNPC):
            border_col = (100, 140, 190)
        elif is_outpost:
            border_col = (80, 145, 95)
        else:
            border_col = (120, 100, 60)

        pygame.draw.rect(self.screen, (22, 22, 30), (px, py, PW, PH))
        pygame.draw.rect(self.screen, border_col, (px, py, PW, PH), 2)

        hint = self.small.render("E or ESC to close", True, (100, 100, 110))
        self.screen.blit(hint, (px + PW - hint.get_width() - 8, py + 8))

        if isinstance(npc, RoyalCuratorNPC):
            self._draw_quest_content(player, npc, px, py, PW, PH)
        elif isinstance(npc, RoyalFloristNPC):
            self._draw_wf_quest_content(player, npc, px, py, PW, PH)
        elif isinstance(npc, RoyalJewelerNPC):
            self._draw_gem_quest_content(player, npc, px, py, PW, PH)
        elif isinstance(npc, RoyalPaleontologistNPC):
            self._draw_fossil_quest_content(player, npc, px, py, PW, PH)
        elif isinstance(npc, RoyalAnglerNPC):
            self._draw_fish_quest_content(player, npc, px, py, PW, PH)
        elif isinstance(npc, RockQuestNPC):
            self._draw_quest_content(player, npc, px, py, PW, PH)
        elif isinstance(npc, TradeNPC):
            self._draw_trade_content(player, npc, px, py, PW, PH)
        elif isinstance(npc, WildflowerQuestNPC):
            self._draw_wf_quest_content(player, npc, px, py, PW, PH)
        elif isinstance(npc, GemQuestNPC):
            self._draw_gem_quest_content(player, npc, px, py, PW, PH)
        elif isinstance(npc, MerchantNPC):
            self._draw_merchant_content(player, npc, px, py, PW, PH)
        elif isinstance(npc, RestaurantNPC):
            self._draw_restaurant_content(player, npc, px, py, PW, PH)
        elif isinstance(npc, ShrineKeeperNPC):
            self._draw_shrine_content(player, npc, px, py, PW, PH)
        elif isinstance(npc, JewelryMerchantNPC):
            self._draw_jewelry_merchant_content(player, npc, px, py, PW, PH)
        elif isinstance(npc, BlacksmithNPC):
            self._draw_blacksmith_content(player, npc, px, py, PW, PH)
        elif isinstance(npc, InnkeeperNPC):
            self._draw_innkeeper_content(player, npc, px, py, PW, PH)
        elif isinstance(npc, ScholarNPC):
            self._draw_scholar_content(player, npc, px, py, PW, PH)
        elif isinstance(npc, WeaponArmorerNPC):
            self._draw_weapon_armorer_content(player, npc, px, py, PW, PH)
        elif isinstance(npc, QuartermasterNPC):
            self._draw_trade_content(player, npc, px, py, PW, PH)
        elif isinstance(npc, GarrisonCommanderNPC):
            self._draw_garrison_commander_content(player, npc, px, py, PW, PH)
        elif isinstance(npc, DoctorNPC):
            self._draw_doctor_content(player, npc, px, py, PW, PH)
        elif is_outpost:
            self._draw_outpost_keeper_content(player, npc, px, py, PW, PH)

    def _draw_rep_rank(self, npc, px, py):
        from cities import rep_rank
        rep = npc._town_rep()
        name, color = rep_rank(rep)
        s = self.small.render(f"{name}  [{rep} rep]", True, color)
        self.screen.blit(s, (px + 14, py + 10))

    def _draw_garrison_commander_content(self, player, npc, px, py, PW, PH):
        title = self.large.render("GARRISON COMMANDER", True, (210, 110, 90))
        self.screen.blit(title, (px + 20, py + 20))
        self._draw_rep_rank(npc, px, py)

        desc = _wrap_text("The crown requires weapons of fine craftsmanship to secure our borders. "
                          "Provide the following gear to receive your reward.", self.small, PW - 40)
        for i, line in enumerate(desc):
            s = self.small.render(line, True, (200, 190, 180))
            self.screen.blit(s, (px + 20, py + 65 + i * 20))

        self._trade_rects = {}
        for i, quest in enumerate(npc.quests):
            qy = py + 140 + i * 150
            pygame.draw.rect(self.screen, (35, 35, 45), (px + 15, qy, PW - 30, 140))
            pygame.draw.rect(self.screen, (160, 90, 70), (px + 15, qy, PW - 30, 140), 1)

            wtype = quest["weapon_type"].replace("_", " ").title() if quest["weapon_type"] else "Any Weapons"
            q_title = self.medium.render(f"Requirement: {quest['count']}x {quest['min_tier']} {wtype}", True, (255, 255, 255))
            self.screen.blit(q_title, (px + 30, qy + 15))

            reward_txt = f"Reward: {quest['reward']} gold"
            r_s = self.medium.render(reward_txt, True, (240, 200, 40))
            self.screen.blit(r_s, (px + 30, qy + 45))

            # Matching weapons count
            matches = len(npc.matching_weapons(player, quest))
            m_txt = f"In Inventory: {matches} / {quest['count']}"
            m_s = self.small.render(m_txt, True, (120, 220, 120) if matches >= quest["count"] else (180, 180, 180))
            self.screen.blit(m_s, (px + 30, qy + 75))

            btn_rect = pygame.Rect(px + PW - 160, qy + 40, 130, 60)
            can_finish = matches >= quest["count"]
            btn_col = (160, 90, 70) if can_finish else (80, 80, 80)
            pygame.draw.rect(self.screen, btn_col, btn_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), btn_rect, 2)

            btn_txt = self.small.render("DELIVER", True, (255, 255, 255))
            self.screen.blit(btn_txt, (btn_rect.centerx - btn_txt.get_width() // 2,
                                       btn_rect.centery - btn_txt.get_height() // 2))
            self._trade_rects[i] = btn_rect

    def _draw_doctor_content(self, player, npc, px, py, PW, PH):
        # Header
        title = self.large.render("TOWN DOCTOR", True, (240, 240, 240))
        self.screen.blit(title, (px + 20, py + 20))

        desc = _wrap_text("I can tend to your wounds and restore your vitality. For a modest fee, of course.", self.small, PW - 60)
        for i, line in enumerate(desc):
            s = self.small.render(line, True, (200, 200, 210))
            self.screen.blit(s, (px + 20, py + 65 + i * 20))

        # Stats
        health_txt = f"Current Health: {player.health} / {player.MAX_HEALTH}"
        h_s = self.medium.render(health_txt, True, (220, 80, 80))
        self.screen.blit(h_s, (px + 20, py + 140))

        cost_txt = f"Treatment Cost: {npc.heal_cost} gold"
        c_s = self.medium.render(cost_txt, True, (220, 200, 40))
        self.screen.blit(c_s, (px + 20, py + 180))

        # Heal Button
        btn_w, btn_h = 240, 60
        btn_rect = pygame.Rect(px + (PW - btn_w) // 2, py + PH - 100, btn_w, btn_h)

        can_afford = player.money >= npc.heal_cost
        can_heal = player.health < player.MAX_HEALTH

        btn_col = (60, 140, 70) if (can_afford and can_heal) else (80, 80, 80)
        pygame.draw.rect(self.screen, btn_col, btn_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), btn_rect, 2)

        txt = "HEAL ME" if can_heal else "FULLY HEALED"
        if not can_afford and can_heal:
            txt = "INSUFFICIENT GOLD"

        t_s = self.small.render(txt, True, (255, 255, 255))
        self.screen.blit(t_s, (btn_rect.centerx - t_s.get_width() // 2, btn_rect.centery - t_s.get_height() // 2))

        self._trade_rects = {0: btn_rect}

    def _draw_quest_content(self, player, npc, px, py, PW, PH):
        from cities import quest_display, quest_hint, RARITY_ORDER, RoyalCuratorNPC, ROYAL_QUEST_REP
        from rocks import RARITY_COLORS

        if isinstance(npc, RoyalCuratorNPC):
            title_txt = "ROYAL CURATOR  ★ By Order of the King ★"
            title_col = (220, 175, 40)
        else:
            DIFF_LABELS = {0: "Novice", 1: "Journeyman", 2: "Expert"}
            diff_col    = {0: (120, 190, 120), 1: (190, 170, 80), 2: (210, 80, 80)}
            title_txt = f"ROCK COLLECTOR  [{DIFF_LABELS[npc.difficulty]}]"
            title_col = diff_col[npc.difficulty]
        title = self.font.render(title_txt, True, title_col)
        self.screen.blit(title, (px + PW // 2 - title.get_width() // 2, py + 10))
        self._draw_rep_rank(npc, px, py)

        # Streak indicator
        if npc._streak > 0:
            bonus_pct = min(npc._streak - 1, 2) * 25
            streak_label = f"Streak: {npc._streak}  (+{bonus_pct}% bonus)" if bonus_pct else f"Streak: {npc._streak}"
            s_col = (80, 220, 130) if bonus_pct else (160, 200, 160)
            stxt = self.small.render(streak_label, True, s_col)
            self.screen.blit(stxt, (px + PW - stxt.get_width() - 12, py + 32))

        self._trade_rects.clear()
        y = py + 40

        for quest_idx, quest in enumerate(npc.quests):
            row_h = 150
            row_rect = pygame.Rect(px + 14, y, PW - 28, row_h)

            min_rep    = quest.get("min_rep", 0)
            rep_locked = npc._town_rep() < min_rep
            can = npc.can_complete(player, quest_idx)

            if rep_locked:
                bg, bdr = (28, 24, 10), (160, 130, 30)
            else:
                bg  = (25, 40, 20) if can else (22, 22, 30)
                bdr = (60, 160, 60) if can else (70, 60, 80)
            pygame.draw.rect(self.screen, bg, row_rect)
            pygame.draw.rect(self.screen, bdr, row_rect, 2)

            iy = y + 10
            if rep_locked:
                badge_label = "ROYAL COMMISSION" if min_rep >= ROYAL_QUEST_REP else "PRESTIGE QUEST"
                badge = self.small.render(badge_label, True, (220, 175, 40) if min_rep >= ROYAL_QUEST_REP else (200, 165, 40))
                self.screen.blit(badge, (px + 22, iy))
                lock_s = self.small.render(
                    f"Requires {min_rep} rep  (you have: {npc._town_rep()})",
                    True, (200, 100, 60))
                self.screen.blit(lock_s, (px + 22 + badge.get_width() + 12, iy))
            else:
                kind_labels = {"single": "SPECIFIC", "any_rarity": "ANY RARITY",
                               "quantity": "BULK", "special": "SPECIAL TRAIT"}
                badge_col   = {"single": (120, 120, 180), "any_rarity": (100, 160, 200),
                               "quantity": (160, 120, 60), "special": (160, 80, 180)}
                badge = self.small.render(kind_labels.get(quest["kind"], "QUEST"), True,
                                          badge_col.get(quest["kind"], (150, 150, 150)))
                self.screen.blit(badge, (px + 22, iy))
            iy += 18

            desc = quest_display(quest)
            rarity_col = (140, 120, 60) if rep_locked else (220, 220, 220)
            if not rep_locked:
                if quest["kind"] == "single":
                    rarity_col = RARITY_COLORS.get(quest["rarity"], rarity_col)
                elif quest["kind"] == "any_rarity":
                    rarity_col = RARITY_COLORS.get(quest["min_rarity"], rarity_col)
            self.screen.blit(self.font.render(desc, True, rarity_col), (px + 22, iy))
            iy += 24

            hint = quest_hint(quest)
            self.screen.blit(self.small.render(hint, True, (140, 150, 170)), (px + 22, iy))
            iy += 20

            if not rep_locked:
                matching = npc.find_matching_rocks(player, quest)
                needed   = quest.get("count", 1)
                if len(matching) >= needed:
                    status, status_col = f"Ready!  ({len(matching)} matching in collection)", (80, 220, 80)
                else:
                    status, status_col = f"Need {needed}  —  you have {len(matching)}", (180, 90, 90)
                self.screen.blit(self.small.render(status, True, status_col), (px + 22, iy))
                iy += 18

            streak_bonus = min(npc._streak, 2) * 25
            reward_str = f"Reward: {quest['reward']} gold"
            if streak_bonus and not rep_locked:
                bonus_val = int(quest["reward"] * (1 + streak_bonus / 100)) - quest["reward"]
                reward_str += f"  (+{bonus_val} streak bonus)"
            self.screen.blit(self.font.render(reward_str, True, (240, 210, 50)), (px + 22, iy))

            BW, BH = 170, 36
            bx2 = px + PW - BW - 20
            by2 = y + row_h // 2 - BH // 2
            btn_rect = pygame.Rect(bx2, by2, BW, BH)
            self._trade_rects[quest_idx] = btn_rect
            if rep_locked:
                b_bg, b_bdr, b_tc = (40, 30, 8), (140, 110, 30), (180, 140, 40)
                btn_text = "LOCKED"
            elif len(npc.find_matching_rocks(player, quest)) >= quest.get("count", 1):
                b_bg, b_bdr, b_tc = (18, 90, 18), (45, 200, 45), (190, 255, 190)
                btn_text = "HAND OVER"
            else:
                b_bg, b_bdr, b_tc = (30, 30, 36), (55, 55, 68), (70, 70, 82)
                btn_text = "HAND OVER"
            pygame.draw.rect(self.screen, b_bg, btn_rect)
            pygame.draw.rect(self.screen, b_bdr, btn_rect, 2)
            bl = self.small.render(btn_text, True, b_tc)
            self.screen.blit(bl, (bx2 + BW // 2 - bl.get_width() // 2,
                                   by2 + BH // 2 - bl.get_height() // 2))

            y += row_h + 8

    def _draw_trade_content(self, player, npc, px, py, PW, PH):
        title = self.font.render("TRADER", True, (80, 210, 160))
        self.screen.blit(title, (px + PW // 2 - title.get_width() // 2, py + 10))
        self._draw_rep_rank(npc, px, py)

        bonus_pct = npc.rep_bonus_pct()
        if bonus_pct > 0:
            rep_txt = self.small.render(
                f"Town reputation bonus: +{bonus_pct}% on all prices", True, (120, 200, 120))
            self.screen.blit(rep_txt, (px + 20, py + 32))

        self._trade_rects.clear()
        y = py + 56

        for i, (item_id, give_count, _) in enumerate(npc.trades):
            can = npc.can_trade(i, player)
            have = player.inventory.get(item_id, 0)
            item_name = ITEMS.get(item_id, {}).get("name", item_id)
            gold = npc.boosted_gold(i)

            row_h = 64
            rect = pygame.Rect(px + 20, y, PW - 40, row_h)
            self._trade_rects[i] = rect

            bg  = (20, 50, 20) if can else (26, 26, 34)
            bdr = (50, 180, 80) if can else (55, 55, 70)
            pygame.draw.rect(self.screen, bg, rect)
            pygame.draw.rect(self.screen, bdr, rect, 2)

            item_color = ITEMS.get(item_id, {}).get("color", (128, 128, 128))
            pygame.draw.rect(self.screen, item_color, (px + 28, y + 16, 30, 30))

            give_col = (80, 220, 80) if can else (170, 80, 80)
            self.screen.blit(
                self.font.render(f"Give: {give_count}x {item_name}  (have: {have})",
                                 True, give_col),
                (px + 68, y + 10))
            self.screen.blit(
                self.font.render(f"Receive: {gold} gold", True, (240, 210, 50)),
                (px + 68, y + 32))

            lbl = self.font.render("TRADE", True, (190, 255, 190) if can else (70, 70, 82))
            self.screen.blit(lbl, (rect.right - lbl.get_width() - 10,
                                    y + row_h // 2 - lbl.get_height() // 2))
            y += row_h + 8

    def _draw_wf_quest_content(self, player, npc, px, py, PW, PH):
        from cities import wf_quest_display, wf_quest_hint, RARITY_ORDER, RoyalFloristNPC, ROYAL_QUEST_REP
        from rocks import RARITY_COLORS

        if isinstance(npc, RoyalFloristNPC):
            title_txt = "ROYAL FLORIST  ★ By Order of the King ★"
            title_col = (220, 175, 40)
        else:
            DIFF_LABELS = {0: "Apprentice", 1: "Journeyman", 2: "Master"}
            diff_col    = {0: (100, 200, 110), 1: (80, 190, 140), 2: (60, 180, 80)}
            title_txt   = f"HERBALIST  [{DIFF_LABELS[npc.difficulty]}]"
            title_col   = diff_col[npc.difficulty]
        title = self.font.render(title_txt, True, title_col)
        self.screen.blit(title, (px + PW // 2 - title.get_width() // 2, py + 10))
        self._draw_rep_rank(npc, px, py)

        if npc._streak > 0:
            bonus_pct = min(npc._streak - 1, 2) * 25
            streak_label = f"Streak: {npc._streak}  (+{bonus_pct}% bonus)" if bonus_pct else f"Streak: {npc._streak}"
            stxt = self.small.render(streak_label, True, (80, 220, 130))
            self.screen.blit(stxt, (px + PW - stxt.get_width() - 12, py + 32))

        self._trade_rects.clear()
        y = py + 40
        for quest_idx, quest in enumerate(npc.quests):
            row_h    = 150
            row_rect = pygame.Rect(px + 14, y, PW - 28, row_h)
            min_rep    = quest.get("min_rep", 0)
            rep_locked = npc._town_rep() < min_rep
            can = npc.can_complete(player, quest_idx)
            if rep_locked:
                bg, bdr = (28, 24, 10), (160, 130, 30)
            else:
                bg  = (20, 40, 22) if can else (22, 22, 30)
                bdr = (55, 160, 65) if can else (55, 80, 55)
            pygame.draw.rect(self.screen, bg, row_rect)
            pygame.draw.rect(self.screen, bdr, row_rect, 2)

            iy = y + 10
            if rep_locked:
                badge_label = "ROYAL COMMISSION" if min_rep >= ROYAL_QUEST_REP else "PRESTIGE QUEST"
                badge = self.small.render(badge_label, True, (220, 175, 40) if min_rep >= ROYAL_QUEST_REP else (200, 165, 40))
                self.screen.blit(badge, (px + 22, iy))
                lock_s = self.small.render(
                    f"Requires {min_rep} rep  (you have: {npc._town_rep()})", True, (200, 100, 60))
                self.screen.blit(lock_s, (px + 22 + badge.get_width() + 12, iy))
            else:
                kind_labels = {"wf_single": "SPECIFIC FLOWER", "wf_quantity": "BULK FLOWERS", "wf_rarity": "RARITY"}
                badge_col   = {"wf_single": (80, 180, 90), "wf_quantity": (140, 160, 60), "wf_rarity": (60, 180, 130)}
                badge = self.small.render(kind_labels.get(quest["kind"], "QUEST"), True,
                                          badge_col.get(quest["kind"], (150, 150, 150)))
                self.screen.blit(badge, (px + 22, iy))
            iy += 18

            rarity_col = (140, 120, 60) if rep_locked else RARITY_COLORS.get(quest.get("min_rarity", "common"), (220, 220, 220))
            self.screen.blit(self.font.render(wf_quest_display(quest), True, rarity_col), (px + 22, iy)); iy += 24
            self.screen.blit(self.small.render(wf_quest_hint(quest), True, (140, 170, 150)), (px + 22, iy)); iy += 20

            if not rep_locked:
                matching = npc.find_matching_flowers(player, quest)
                needed   = quest.get("count", 1)
                if len(matching) >= needed:
                    status, sc = f"Ready!  ({len(matching)} matching in collection)", (80, 220, 80)
                else:
                    status, sc = f"Need {needed}  —  you have {len(matching)}", (180, 90, 90)
                self.screen.blit(self.small.render(status, True, sc), (px + 22, iy)); iy += 18

            streak_bonus = min(npc._streak, 2) * 25
            reward_str = f"Reward: {quest['reward']} gold"
            if streak_bonus and not rep_locked:
                bonus_val = int(quest["reward"] * (1 + streak_bonus / 100)) - quest["reward"]
                reward_str += f"  (+{bonus_val} streak bonus)"
            self.screen.blit(self.font.render(reward_str, True, (240, 210, 50)), (px + 22, iy))

            BW, BH = 170, 36
            bx2, by2 = px + PW - BW - 20, y + row_h // 2 - BH // 2
            btn_rect = pygame.Rect(bx2, by2, BW, BH)
            self._trade_rects[quest_idx] = btn_rect
            if rep_locked:
                b_bg, b_bdr, b_tc = (40, 30, 8), (140, 110, 30), (180, 140, 40)
                btn_text = "LOCKED"
            elif len(npc.find_matching_flowers(player, quest)) >= quest.get("count", 1):
                b_bg, b_bdr, b_tc = (18, 90, 30), (45, 200, 65), (190, 255, 200)
                btn_text = "HAND OVER"
            else:
                b_bg, b_bdr, b_tc = (30, 30, 36), (55, 55, 68), (70, 70, 82)
                btn_text = "HAND OVER"
            pygame.draw.rect(self.screen, b_bg, btn_rect)
            pygame.draw.rect(self.screen, b_bdr, btn_rect, 2)
            bl = self.small.render(btn_text, True, b_tc)
            self.screen.blit(bl, (bx2 + BW // 2 - bl.get_width() // 2,
                                   by2 + BH // 2 - bl.get_height() // 2))
            y += row_h + 8

    def _draw_gem_quest_content(self, player, npc, px, py, PW, PH):
        from cities import gem_quest_display, gem_quest_hint, RARITY_ORDER, RoyalJewelerNPC, ROYAL_QUEST_REP
        from rocks import RARITY_COLORS

        if isinstance(npc, RoyalJewelerNPC):
            title_txt = "ROYAL JEWELER  ★ By Order of the King ★"
            title_col = (220, 175, 40)
        else:
            DIFF_LABELS = {0: "Apprentice", 1: "Journeyman", 2: "Master"}
            diff_col    = {0: (160, 110, 220), 1: (190, 80, 210), 2: (220, 60, 200)}
            title_txt   = f"JEWELER  [{DIFF_LABELS[npc.difficulty]}]"
            title_col   = diff_col[npc.difficulty]
        title = self.font.render(title_txt, True, title_col)
        self.screen.blit(title, (px + PW // 2 - title.get_width() // 2, py + 10))
        self._draw_rep_rank(npc, px, py)

        if npc._streak > 0:
            bonus_pct = min(npc._streak - 1, 2) * 25
            streak_label = f"Streak: {npc._streak}  (+{bonus_pct}% bonus)" if bonus_pct else f"Streak: {npc._streak}"
            stxt = self.small.render(streak_label, True, (200, 140, 255))
            self.screen.blit(stxt, (px + PW - stxt.get_width() - 12, py + 32))

        self._trade_rects.clear()
        y = py + 40
        for quest_idx, quest in enumerate(npc.quests):
            row_h    = 150
            row_rect = pygame.Rect(px + 14, y, PW - 28, row_h)
            min_rep    = quest.get("min_rep", 0)
            rep_locked = npc._town_rep() < min_rep
            can = npc.can_complete(player, quest_idx)
            if rep_locked:
                bg, bdr = (28, 24, 10), (160, 130, 30)
            else:
                bg  = (25, 18, 40) if can else (22, 22, 30)
                bdr = (130, 60, 200) if can else (70, 50, 90)
            pygame.draw.rect(self.screen, bg, row_rect)
            pygame.draw.rect(self.screen, bdr, row_rect, 2)

            iy = y + 10
            if rep_locked:
                badge_label = "ROYAL COMMISSION" if min_rep >= ROYAL_QUEST_REP else "PRESTIGE QUEST"
                badge = self.small.render(badge_label, True, (220, 175, 40) if min_rep >= ROYAL_QUEST_REP else (200, 165, 40))
                self.screen.blit(badge, (px + 22, iy))
                lock_s = self.small.render(
                    f"Requires {min_rep} rep  (you have: {npc._town_rep()})", True, (200, 100, 60))
                self.screen.blit(lock_s, (px + 22 + badge.get_width() + 12, iy))
            else:
                kind_labels = {"gem_type": "GEM TYPE", "gem_cut": "CUT GEM", "gem_rarity": "RARITY",
                               "gem_royal": "CROWN JEWEL"}
                badge_col   = {"gem_type": (160, 100, 220), "gem_cut": (200, 120, 80), "gem_rarity": (120, 80, 210),
                               "gem_royal": (220, 175, 40)}
                badge = self.small.render(kind_labels.get(quest["kind"], "QUEST"), True,
                                          badge_col.get(quest["kind"], (150, 150, 150)))
                self.screen.blit(badge, (px + 22, iy))
            iy += 18

            rarity_col = (140, 120, 60) if rep_locked else RARITY_COLORS.get(quest.get("min_rarity", "common"), (220, 220, 220))
            self.screen.blit(self.font.render(gem_quest_display(quest), True, rarity_col), (px + 22, iy)); iy += 24
            self.screen.blit(self.small.render(gem_quest_hint(quest), True, (170, 140, 200)), (px + 22, iy)); iy += 20

            if not rep_locked:
                matching = npc.find_matching_gems(player, quest)
                needed   = quest.get("count", 1)
                if len(matching) >= needed:
                    status, sc = f"Ready!  ({len(matching)} matching in collection)", (80, 220, 80)
                else:
                    status, sc = f"Need {needed}  —  you have {len(matching)}", (180, 90, 90)
                self.screen.blit(self.small.render(status, True, sc), (px + 22, iy)); iy += 18

            streak_bonus = min(npc._streak, 2) * 25
            reward_str = f"Reward: {quest['reward']} gold"
            if streak_bonus and not rep_locked:
                bonus_val = int(quest["reward"] * (1 + streak_bonus / 100)) - quest["reward"]
                reward_str += f"  (+{bonus_val} streak bonus)"
            self.screen.blit(self.font.render(reward_str, True, (240, 210, 50)), (px + 22, iy))

            BW, BH = 170, 36
            bx2, by2 = px + PW - BW - 20, y + row_h // 2 - BH // 2
            btn_rect = pygame.Rect(bx2, by2, BW, BH)
            self._trade_rects[quest_idx] = btn_rect
            if rep_locked:
                b_bg, b_bdr, b_tc = (40, 30, 8), (140, 110, 30), (180, 140, 40)
                btn_text = "LOCKED"
            elif len(npc.find_matching_gems(player, quest)) >= quest.get("count", 1):
                b_bg, b_bdr, b_tc = (40, 18, 80), (140, 60, 220), (220, 180, 255)
                btn_text = "HAND OVER"
            else:
                b_bg, b_bdr, b_tc = (30, 30, 36), (55, 55, 68), (70, 70, 82)
                btn_text = "HAND OVER"
            pygame.draw.rect(self.screen, b_bg, btn_rect)
            pygame.draw.rect(self.screen, b_bdr, btn_rect, 2)
            bl = self.small.render(btn_text, True, b_tc)
            self.screen.blit(bl, (bx2 + BW // 2 - bl.get_width() // 2,
                                   by2 + BH // 2 - bl.get_height() // 2))
            y += row_h + 8

    def _draw_fossil_quest_content(self, player, npc, px, py, PW, PH):
        from cities import fossil_quest_display, fossil_quest_hint, ROYAL_QUEST_REP
        from rocks import RARITY_COLORS

        title = self.font.render("ROYAL PALEONTOLOGIST  ★ By Order of the King ★", True, (220, 175, 40))
        self.screen.blit(title, (px + PW // 2 - title.get_width() // 2, py + 10))
        self._draw_rep_rank(npc, px, py)

        self._trade_rects.clear()
        y = py + 40
        for quest_idx, quest in enumerate(npc.quests):
            row_h    = 150
            row_rect = pygame.Rect(px + 14, y, PW - 28, row_h)
            min_rep    = quest.get("min_rep", 0)
            rep_locked = npc._town_rep() < min_rep
            can = npc.can_complete(player, quest_idx)
            if rep_locked:
                bg, bdr = (28, 24, 10), (160, 130, 30)
            else:
                bg  = (25, 38, 18) if can else (22, 22, 30)
                bdr = (180, 145, 30) if can else (100, 85, 40)
            pygame.draw.rect(self.screen, bg, row_rect)
            pygame.draw.rect(self.screen, bdr, row_rect, 2)

            iy = y + 10
            if rep_locked:
                badge = self.small.render("ROYAL COMMISSION", True, (220, 175, 40))
                self.screen.blit(badge, (px + 22, iy))
                lock_s = self.small.render(
                    f"Requires {min_rep} rep  (you have: {npc._town_rep()})", True, (200, 100, 60))
                self.screen.blit(lock_s, (px + 22 + badge.get_width() + 12, iy))
            else:
                kind_labels = {"fossil_single": "SPECIFIC FOSSIL", "fossil_special": "RARE QUALITY"}
                badge_col   = {"fossil_single": (180, 155, 60), "fossil_special": (200, 130, 40)}
                badge = self.small.render(kind_labels.get(quest["kind"], "QUEST"), True,
                                          badge_col.get(quest["kind"], (220, 175, 40)))
                self.screen.blit(badge, (px + 22, iy))
            iy += 18

            rarity_col = (140, 120, 60) if rep_locked else RARITY_COLORS.get(quest.get("rarity", "legendary"), (220, 200, 100))
            self.screen.blit(self.font.render(fossil_quest_display(quest), True, rarity_col), (px + 22, iy)); iy += 24
            self.screen.blit(self.small.render(fossil_quest_hint(quest), True, (160, 150, 120)), (px + 22, iy)); iy += 20

            if not rep_locked:
                matching = npc.find_matching_fossils(player, quest)
                needed   = quest.get("count", 1)
                if len(matching) >= needed:
                    status, sc = f"Ready!  ({len(matching)} matching in collection)", (80, 220, 80)
                else:
                    status, sc = f"Need {needed}  —  you have {len(matching)}", (180, 90, 90)
                self.screen.blit(self.small.render(status, True, sc), (px + 22, iy)); iy += 18

            self.screen.blit(self.font.render(f"Reward: {quest['reward']} gold", True, (240, 210, 50)), (px + 22, iy))

            BW, BH = 170, 36
            bx2, by2 = px + PW - BW - 20, y + row_h // 2 - BH // 2
            btn_rect = pygame.Rect(bx2, by2, BW, BH)
            self._trade_rects[quest_idx] = btn_rect
            if rep_locked:
                b_bg, b_bdr, b_tc = (40, 30, 8), (140, 110, 30), (180, 140, 40)
                btn_text = "LOCKED"
            elif len(npc.find_matching_fossils(player, quest)) >= quest.get("count", 1):
                b_bg, b_bdr, b_tc = (45, 35, 8), (200, 160, 35), (255, 230, 120)
                btn_text = "HAND OVER"
            else:
                b_bg, b_bdr, b_tc = (30, 30, 36), (55, 55, 68), (70, 70, 82)
                btn_text = "HAND OVER"
            pygame.draw.rect(self.screen, b_bg, btn_rect)
            pygame.draw.rect(self.screen, b_bdr, btn_rect, 2)
            bl = self.small.render(btn_text, True, b_tc)
            self.screen.blit(bl, (bx2 + BW // 2 - bl.get_width() // 2,
                                   by2 + BH // 2 - bl.get_height() // 2))
            y += row_h + 8

    def _draw_fish_quest_content(self, player, npc, px, py, PW, PH):
        from cities import fish_quest_display, fish_quest_hint, ROYAL_QUEST_REP
        from rocks import RARITY_COLORS

        title = self.font.render("ROYAL ANGLER  ★ By Order of the King ★", True, (220, 175, 40))
        self.screen.blit(title, (px + PW // 2 - title.get_width() // 2, py + 10))
        self._draw_rep_rank(npc, px, py)

        self._trade_rects.clear()
        y = py + 40
        for quest_idx, quest in enumerate(npc.quests):
            row_h    = 150
            row_rect = pygame.Rect(px + 14, y, PW - 28, row_h)
            min_rep    = quest.get("min_rep", 0)
            rep_locked = npc._town_rep() < min_rep
            can = npc.can_complete(player, quest_idx)
            if rep_locked:
                bg, bdr = (28, 24, 10), (160, 130, 30)
            else:
                bg  = (15, 30, 45) if can else (22, 22, 30)
                bdr = (50, 140, 200) if can else (40, 70, 100)
            pygame.draw.rect(self.screen, bg, row_rect)
            pygame.draw.rect(self.screen, bdr, row_rect, 2)

            iy = y + 10
            if rep_locked:
                badge = self.small.render("ROYAL COMMISSION", True, (220, 175, 40))
                self.screen.blit(badge, (px + 22, iy))
                lock_s = self.small.render(
                    f"Requires {min_rep} rep  (you have: {npc._town_rep()})", True, (200, 100, 60))
                self.screen.blit(lock_s, (px + 22 + badge.get_width() + 12, iy))
            else:
                badge = self.small.render("LEGENDARY CATCH", True, (80, 180, 230))
                self.screen.blit(badge, (px + 22, iy))
            iy += 18

            rarity_col = (140, 120, 60) if rep_locked else RARITY_COLORS.get("legendary", (255, 180, 0))
            self.screen.blit(self.font.render(fish_quest_display(quest), True, rarity_col), (px + 22, iy)); iy += 24
            self.screen.blit(self.small.render(fish_quest_hint(quest), True, (120, 170, 200)), (px + 22, iy)); iy += 20

            if not rep_locked:
                matching = npc.find_matching_fish(player, quest)
                needed   = quest.get("count", 1)
                if len(matching) >= needed:
                    status, sc = f"Ready!  ({len(matching)} matching in collection)", (80, 220, 80)
                else:
                    status, sc = f"Need {needed}  —  you have {len(matching)}", (180, 90, 90)
                self.screen.blit(self.small.render(status, True, sc), (px + 22, iy)); iy += 18

            self.screen.blit(self.font.render(f"Reward: {quest['reward']} gold", True, (240, 210, 50)), (px + 22, iy))

            BW, BH = 170, 36
            bx2, by2 = px + PW - BW - 20, y + row_h // 2 - BH // 2
            btn_rect = pygame.Rect(bx2, by2, BW, BH)
            self._trade_rects[quest_idx] = btn_rect
            if rep_locked:
                b_bg, b_bdr, b_tc = (40, 30, 8), (140, 110, 30), (180, 140, 40)
                btn_text = "LOCKED"
            elif len(npc.find_matching_fish(player, quest)) >= quest.get("count", 1):
                b_bg, b_bdr, b_tc = (10, 35, 55), (50, 150, 210), (160, 230, 255)
                btn_text = "HAND OVER"
            else:
                b_bg, b_bdr, b_tc = (30, 30, 36), (55, 55, 68), (70, 70, 82)
                btn_text = "HAND OVER"
            pygame.draw.rect(self.screen, b_bg, btn_rect)
            pygame.draw.rect(self.screen, b_bdr, btn_rect, 2)
            bl = self.small.render(btn_text, True, b_tc)
            self.screen.blit(bl, (bx2 + BW // 2 - bl.get_width() // 2,
                                   by2 + BH // 2 - bl.get_height() // 2))
            y += row_h + 8

    def _draw_research(self, player, research):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("RESEARCH TREE", True, (255, 220, 50))
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 8))
        hint = self.small.render("R to close  |  Select a category, then click a node to unlock",
                                 True, (150, 150, 150))
        self.screen.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, 28))

        # --- Left sidebar: category list ---
        SIDEBAR_X = 20
        SIDEBAR_Y = 52
        CAT_W, CAT_H, CAT_GAP = 175, 52, 6

        SIDEBAR_AREA_H = SCREEN_H - SIDEBAR_Y
        total_cat_h = len(research.COLUMNS) * (CAT_H + CAT_GAP) - CAT_GAP
        self._max_research_cat_scroll = max(0, total_cat_h - SIDEBAR_AREA_H)
        self._research_cat_scroll = max(0, min(self._max_research_cat_scroll, self._research_cat_scroll))

        old_clip = self.screen.get_clip()
        self.screen.set_clip(pygame.Rect(SIDEBAR_X, SIDEBAR_Y, CAT_W + 20, SIDEBAR_AREA_H))

        self._research_cat_rects = {}
        for ci, col_name in enumerate(research.COLUMNS):
            col_nodes = [nid for (c, _r, nid) in research.layout if c == ci]
            available_count = sum(
                1 for nid in col_nodes
                if research.can_unlock(nid, player.inventory, player.money)
            )
            has_available = available_count > 0
            is_selected   = (self._research_selected_col == ci)

            cat_y = SIDEBAR_Y + ci * (CAT_H + CAT_GAP) - self._research_cat_scroll
            if cat_y + CAT_H < SIDEBAR_Y or cat_y > SCREEN_H:
                continue
            cat_rect = pygame.Rect(SIDEBAR_X, cat_y, CAT_W, CAT_H)
            self._research_cat_rects[ci] = cat_rect

            if has_available:
                bg_col  = (55, 44, 4)
                bdr_col = (220, 178, 28)
            elif is_selected:
                bg_col  = (22, 32, 68)
                bdr_col = (75, 115, 215)
            else:
                bg_col  = (14, 17, 32)
                bdr_col = (48, 52, 86)

            pygame.draw.rect(self.screen, bg_col, cat_rect, border_radius=6)
            pygame.draw.rect(self.screen, bdr_col, cat_rect, 2, border_radius=6)

            if has_available:
                stripe = pygame.Rect(cat_rect.x, cat_rect.y + 4, 4, cat_rect.height - 8)
                pygame.draw.rect(self.screen, (255, 200, 0), stripe, border_radius=2)

            if is_selected:
                tx = cat_rect.right + 5
                ty = cat_rect.centery
                pygame.draw.polygon(self.screen, (180, 190, 255),
                                    [(tx, ty - 6), (tx + 9, ty), (tx, ty + 6)])

            name_col = (255, 210, 0) if has_available else (215, 220, 255) if is_selected else (155, 158, 188)
            lbl = self.small.render(col_name, True, name_col)
            lbl_x = cat_rect.x + 10
            lbl_y = cat_rect.y + (CAT_H - lbl.get_height()) // 2
            self.screen.blit(lbl, (lbl_x, lbl_y))

            if available_count > 0:
                badge = self.small.render(str(available_count), True, (10, 10, 10))
                bw = badge.get_width() + 8
                bh = badge.get_height() + 4
                bx = cat_rect.right - bw - 5
                by = cat_rect.y + (CAT_H - bh) // 2
                pygame.draw.rect(self.screen, (220, 178, 28), (bx, by, bw, bh), border_radius=4)
                self.screen.blit(badge, (bx + 4, by + 2))

        self.screen.set_clip(old_clip)

        # --- Right panel: nodes for selected column ---
        RIGHT_X  = SIDEBAR_X + CAT_W + 28
        RIGHT_W  = SCREEN_W - RIGHT_X - 20
        CARD_W   = RIGHT_W
        CARD_H   = 115
        ROW_GAP  = 8
        TEXT_PAD = 10
        TEXT_W   = CARD_W - TEXT_PAD * 2
        NODE_Y   = SIDEBAR_Y

        sel_col       = self._research_selected_col
        col_node_rows = sorted((r, nid) for (c, r, nid) in research.layout if c == sel_col)

        RIGHT_AREA_H = SCREEN_H - NODE_Y
        if col_node_rows:
            max_row = col_node_rows[-1][0]
            total_right_h = (max_row + 1) * (CARD_H + ROW_GAP) - ROW_GAP
        else:
            total_right_h = 0
        self._max_research_right_scroll = max(0, total_right_h - RIGHT_AREA_H)
        self._research_right_scroll = max(0, min(self._max_research_right_scroll, self._research_right_scroll))

        self.screen.set_clip(pygame.Rect(RIGHT_X, NODE_Y, RIGHT_W, RIGHT_AREA_H))

        self._card_rects.clear()
        for row, node_id in col_node_rows:
            node = research.nodes[node_id]
            y    = NODE_Y + row * (CARD_H + ROW_GAP) - self._research_right_scroll
            if y + CARD_H < NODE_Y or y > SCREEN_H:
                continue
            rect = pygame.Rect(RIGHT_X, y, CARD_W, CARD_H)
            self._card_rects[node_id] = rect

            prereqs_ok = research.prereqs_met(node_id)
            can        = research.can_unlock(node_id, player.inventory, player.money)

            if node.unlocked:
                bg, border = (10, 45, 10), (40, 170, 40)
                status_txt, status_col = "UNLOCKED", (50, 200, 50)
            elif can:
                bg, border = (55, 45, 5), (220, 180, 30)
                status_txt, status_col = "AVAILABLE", (220, 180, 30)
            elif prereqs_ok:
                bg, border = (45, 20, 20), (160, 70, 70)
                status_txt, status_col = "NEED ITEMS", (200, 90, 90)
            else:
                bg, border = (20, 20, 28), (55, 55, 80)
                status_txt, status_col = "LOCKED", (90, 90, 120)

            pygame.draw.rect(self.screen, bg, rect, border_radius=6)
            pygame.draw.rect(self.screen, border, rect, 2, border_radius=6)

            st_surf    = self.small.render(status_txt, True, status_col)
            st_x       = rect.right - st_surf.get_width() - TEXT_PAD
            name_max_w = st_x - (rect.x + TEXT_PAD) - 6
            name_surf  = self.font.render(node.name, True, (255, 255, 220))
            if name_surf.get_width() > name_max_w:
                name_surf = name_surf.subsurface((0, 0, name_max_w, name_surf.get_height()))
            self.screen.blit(name_surf, (rect.x + TEXT_PAD, y + 7))
            self.screen.blit(st_surf,   (st_x, y + 10))

            desc_lines = _wrap_text(node.description, self.small, TEXT_W)
            dy = y + 30
            for line in desc_lines[:2]:
                self.screen.blit(self.small.render(line, True, (150, 150, 150)), (rect.x + TEXT_PAD, dy))
                dy += 15

            cost_y = y + 64
            if not node.unlocked:
                if not prereqs_ok:
                    blocked   = [research.nodes[p].name for p in node.prerequisites
                                 if not research.nodes[p].unlocked]
                    req_lines = _wrap_text("Requires: " + ", ".join(blocked[:2]), self.small, TEXT_W)
                    for line in req_lines[:2]:
                        self.screen.blit(self.small.render(line, True, (160, 80, 80)),
                                         (rect.x + TEXT_PAD, cost_y))
                        cost_y += 15
                else:
                    cx2 = rect.x + TEXT_PAD
                    for item_id, needed in node.cost.items():
                        have  = player.inventory.get(item_id, 0)
                        iname = ITEMS.get(item_id, {}).get("name", item_id)
                        cc    = (70, 200, 70) if have >= needed else (210, 80, 80)
                        cs    = self.small.render(f"{iname}: {have}/{needed}", True, cc)
                        if cx2 + cs.get_width() > rect.right - TEXT_PAD and cx2 > rect.x + TEXT_PAD:
                            cost_y += 15
                            cx2 = rect.x + TEXT_PAD
                        self.screen.blit(cs, (cx2, cost_y))
                        cx2 += cs.get_width() + 12
                    if node.money_cost > 0:
                        cm = (70, 200, 70) if player.money >= node.money_cost else (210, 80, 80)
                        ms = self.small.render(f"Gold: {player.money}/{node.money_cost}", True, cm)
                        if cx2 + ms.get_width() > rect.right - TEXT_PAD and cx2 > rect.x + TEXT_PAD:
                            cost_y += 15
                            cx2 = rect.x + TEXT_PAD
                        self.screen.blit(ms, (cx2, cost_y))

            if row > 0 and prereqs_ok and not node.unlocked:
                mid_x = rect.x + CARD_W // 2
                pygame.draw.line(self.screen, border, (mid_x, y - ROW_GAP), (mid_x, y), 1)

        self.screen.set_clip(old_clip)

    def _draw_inventory(self, player):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("INVENTORY", True, (220, 220, 100))
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 8))
        hint = self.small.render("I to close  |  Drag item to a hotbar slot  |  Scroll to navigate",
                                 True, (130, 130, 130))
        self.screen.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, 30))

        items_held = sorted(
            [(iid, cnt) for iid, cnt in player.inventory.items() if cnt > 0],
            key=lambda t: ITEMS.get(t[0], {}).get("name", t[0])
        )
        self._inv_rects.clear()

        if not items_held:
            empty = self.font.render("Your inventory is empty.", True, (90, 90, 90))
            self.screen.blit(empty, (SCREEN_W // 2 - empty.get_width() // 2, SCREEN_H // 2 - 10))
            return

        COLS, CELL_W, CELL_H, GAP = 4, 210, 74, 8
        total_w = COLS * CELL_W + (COLS - 1) * GAP
        start_x = (SCREEN_W - total_w) // 2
        hotbar_map = {iid: i for i, iid in enumerate(player.hotbar) if iid}

        AREA_TOP = 50
        AREA_BOT = SCREEN_H - 68  # leave room above hotbar (48px slot + 10px gap + 10px margin)
        area_h = AREA_BOT - AREA_TOP

        num_rows = (len(items_held) + COLS - 1) // COLS
        total_content_h = num_rows * (CELL_H + GAP) - GAP
        self._max_inv_scroll = max(0, total_content_h - area_h)
        self._inv_scroll = max(0, min(self._max_inv_scroll, self._inv_scroll))

        old_clip = self.screen.get_clip()
        self.screen.set_clip(pygame.Rect(0, AREA_TOP, SCREEN_W, area_h))

        for idx, (item_id, count) in enumerate(items_held):
            col = idx % COLS
            row = idx // COLS
            x = start_x + col * (CELL_W + GAP)
            y = AREA_TOP + row * (CELL_H + GAP) - self._inv_scroll
            if y + CELL_H < AREA_TOP or y > AREA_BOT:
                continue
            rect = pygame.Rect(x, y, CELL_W, CELL_H)
            self._inv_rects[item_id] = rect

            item = ITEMS.get(item_id, {})
            hotbar_slot = hotbar_map.get(item_id)
            in_selected = (hotbar_slot == player.selected_slot)

            if in_selected:
                bg, border = (55, 50, 10), (220, 200, 50)
            elif hotbar_slot is not None:
                bg, border = (25, 38, 52), (70, 120, 175)
            else:
                bg, border = (32, 32, 38), (75, 75, 88)

            pygame.draw.rect(self.screen, bg, rect)
            pygame.draw.rect(self.screen, border, rect, 2)
            sw = 46
            sy = y + (CELL_H - sw) // 2
            icon = render_item_icon(item_id, item.get("color", (128, 128, 128)), sw)
            self.screen.blit(icon, (x + 8, sy))
            self.screen.blit(self.font.render(item.get("name", item_id), True, (235, 235, 215)),
                             (x + 62, y + 10))
            self.screen.blit(self.small.render(f"x{count}", True, (150, 215, 150)), (x + 62, y + 33))
            if item.get("place_block") is not None:
                self.screen.blit(self.small.render("placeable", True, (90, 160, 90)), (x + 62, y + 50))
            if hotbar_slot is not None:
                badge_col = (220, 200, 50) if in_selected else (100, 150, 210)
                badge = self.small.render(f"[{hotbar_slot + 1}]", True, badge_col)
                self.screen.blit(badge, (x + CELL_W - badge.get_width() - 7, y + 7))

        self.screen.set_clip(old_clip)

        if self._max_inv_scroll > 0:
            bar_x = start_x + total_w + 10
            pygame.draw.rect(self.screen, (40, 40, 50), (bar_x, AREA_TOP, 6, area_h))
            thumb_h = max(20, int(area_h * area_h / total_content_h))
            thumb_y = AREA_TOP + int((area_h - thumb_h) * self._inv_scroll / self._max_inv_scroll)
            pygame.draw.rect(self.screen, (120, 120, 150), (bar_x, thumb_y, 6, thumb_h))

    def _draw_leader_panel(self, player, npc):
        from towns import TOWNS, REGIONS
        from cities import rep_rank

        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        PW, PH = 640, 560
        px = (SCREEN_W - PW) // 2
        py = (SCREEN_H - PH) // 2

        border_col = npc.leader_color
        pygame.draw.rect(self.screen, (22, 20, 16), (px, py, PW, PH))
        pygame.draw.rect(self.screen, border_col, (px, py, PW, PH), 3)

        title_s = self.font.render(npc.leader_name, True, (240, 220, 160))
        self.screen.blit(title_s, (px + 16, py + 14))

        region = REGIONS.get(npc.region_id)
        title = region.leader_title if region else "Leader"
        role_s = self.small.render(f"{title} of {npc.region_name}", True, (180, 160, 110))
        self.screen.blit(role_s, (px + 16, py + 38))

        # Agenda chip — shows the leader's personality and what they value
        if region and region.agenda:
            from towns import agenda_label, agenda_description
            ag_label = agenda_label(region.agenda)
            ag_desc  = agenda_description(region.agenda)
            ag_s = self.small.render(f"Agenda: {ag_label} — {ag_desc}",
                                     True, (210, 175,  80))
            self.screen.blit(ag_s, (px + 16, py + 56))

        # Diplomacy: allies and rivals from the relations graph
        if region:
            allies = [REGIONS[r].name for r in region.relations
                      if region.relations[r] == "allied" and r in REGIONS]
            rivals = [REGIONS[r].name for r in region.relations
                      if region.relations[r] == "rival"  and r in REGIONS]
            ally_text = ", ".join(allies[:3]) + ("…" if len(allies) > 3 else "") if allies else "none"
            rival_text = ", ".join(rivals[:3]) + ("…" if len(rivals) > 3 else "") if rivals else "none"
            self.screen.blit(
                self.small.render(f"Allied: {ally_text}", True, (140, 200, 130)),
                (px + 16, py + 76))
            self.screen.blit(
                self.small.render(f"Rival:  {rival_text}", True, (210, 120, 110)),
                (px + 16, py + 94))

        # Regional rep + rank
        total_rep = npc.regional_rep()
        rank_name, rank_col = rep_rank(npc._town_rep())
        rep_s = self.small.render(
            f"Regional reputation: {total_rep}   |   Your standing: {rank_name}",
            True, rank_col)
        self.screen.blit(rep_s, (px + 16, py + 114))

        pygame.draw.line(self.screen, border_col, (px + 10, py + 132), (px + PW - 10, py + 132))

        cy = py + 140
        if region:
            for tid in region.member_town_ids:
                town = TOWNS.get(tid)
                if not town:
                    continue
                star = "★ " if town.is_capital else "  "
                town_rank, tcol = rep_rank(town.reputation)
                entry = f"{star}{town.name} ({town.tier_name()})  rep {town.reputation}  [{town_rank}]"
                col = (220, 200, 100) if town.is_capital else (180, 170, 130)
                self.screen.blit(self.small.render(entry, True, col), (px + 22, cy)); cy += 20

        cy += 8
        pygame.draw.line(self.screen, border_col, (px + 10, cy), (px + PW - 10, cy))
        cy += 10

        # Regional contracts
        contracts_lbl = self.font.render("REGIONAL CONTRACTS", True, (210, 185, 60))
        self.screen.blit(contracts_lbl, (px + 16, cy)); cy += 24

        self._trade_rects.clear()
        for idx, contract in enumerate(npc.contracts):
            row_h = 60
            row_rect = pygame.Rect(px + 12, cy, PW - 24, row_h)

            if contract is None:
                # Rival embargo: anchor region is rival to this leader's, and
                # the slot rolled refusal at generation time.
                pygame.draw.rect(self.screen, (30, 18, 18), row_rect)
                pygame.draw.rect(self.screen, (110,  60,  60), row_rect, 2)
                emb_s = self.font.render("— Slot embargoed —", True, (180, 110, 110))
                why_s = self.small.render(
                    "Your home region is at odds with this court.", True, (140,  90,  90))
                self.screen.blit(emb_s, (px + 22, cy +  8))
                self.screen.blit(why_s, (px + 22, cy + 32))
                cy += row_h + 6
                continue

            item_id, give_count, reward_gold, display_name, min_rep, rep_bonus = contract
            rep_locked = npc._town_rep() < min_rep
            can = npc.can_fulfill(idx, player)
            have = player.inventory.get(item_id, 0)
            if rep_locked:
                bg, bdr = (28, 24, 10), (140, 110, 30)
            else:
                bg  = (28, 38, 18) if can else (22, 22, 30)
                bdr = (100, 170, 50) if can else (60, 70, 50)
            pygame.draw.rect(self.screen, bg, row_rect)
            pygame.draw.rect(self.screen, bdr, row_rect, 2)

            item_color = ITEMS.get(item_id, {}).get("color", (160, 160, 160))
            pygame.draw.rect(self.screen, item_color, (px + 18, cy + 14, 24, 24))

            if rep_locked:
                name_s = self.font.render(display_name, True, (130, 115, 60))
                lock_s = self.small.render(
                    f"Requires {min_rep} rep  (you have: {npc._town_rep()})", True, (190, 100, 50))
                self.screen.blit(name_s, (px + 52, cy + 8))
                self.screen.blit(lock_s, (px + 52, cy + 30))
                btn_text, b_bg, b_bdr, b_tc = "LOCKED", (40, 30, 8), (130, 100, 25), (170, 130, 40)
            else:
                name_col = (220, 210, 140) if can else (130, 120, 90)
                name_s = self.font.render(display_name, True, name_col)
                detail_col = (160, 200, 80) if can else (90, 110, 60)
                inv_s = self.small.render(
                    f"Give: {give_count}x  (have: {have})   Reward: {reward_gold}g  +{rep_bonus} rep/town",
                    True, detail_col)
                self.screen.blit(name_s, (px + 52, cy + 8))
                self.screen.blit(inv_s,  (px + 52, cy + 30))
                if can:
                    btn_text, b_bg, b_bdr, b_tc = "FULFILL", (20, 70, 15), (60, 200, 50), (180, 255, 160)
                else:
                    btn_text, b_bg, b_bdr, b_tc = "FULFILL", (30, 30, 36), (55, 55, 68), (70, 70, 82)

            BW, BH = 90, 30
            bx2 = row_rect.right - BW - 10
            by2 = cy + row_h // 2 - BH // 2
            btn_rect = pygame.Rect(bx2, by2, BW, BH)
            self._trade_rects[idx] = btn_rect
            pygame.draw.rect(self.screen, b_bg, btn_rect)
            pygame.draw.rect(self.screen, b_bdr, btn_rect, 2)
            bl = self.small.render(btn_text, True, b_tc)
            self.screen.blit(bl, (btn_rect.centerx - bl.get_width() // 2,
                                   btn_rect.centery - bl.get_height() // 2))
            cy += row_h + 6

        hint_s = self.small.render("[E] or [ESC] to close", True, (90, 82, 60))
        self.screen.blit(hint_s, (px + PW - hint_s.get_width() - 14, py + PH - 20))

    def _draw_chest(self, player):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        self.screen.blit(overlay, (0, 0))

        PW, PH = 1140, 580
        px = (SCREEN_W - PW) // 2
        py = (SCREEN_H - PH) // 2
        pygame.draw.rect(self.screen, (22, 18, 12), (px, py, PW, PH))
        pygame.draw.rect(self.screen, (140, 95, 45), (px, py, PW, PH), 2)

        hint = self.small.render(
            "Left-click: transfer all  |  Right-click: transfer one  |  E or ESC: close",
            True, (110, 90, 60))
        self.screen.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, py + 8))

        half = (PW - 30) // 2
        lx = px + 10
        rx = px + 20 + half

        # --- divider ---
        pygame.draw.line(self.screen, (80, 60, 35),
                         (px + half + 15, py + 30), (px + half + 15, py + PH - 10), 1)

        COLS, CW, CH, GAP = 3, 170, 54, 6
        VISIBLE_ROWS = 7
        AREA_H = VISIBLE_ROWS * (CH + GAP)

        def _draw_section(title, items_list, start_x, scroll, rects_out):
            title_s = self.font.render(title, True, (220, 190, 100))
            self.screen.blit(title_s, (start_x + half // 2 - title_s.get_width() // 2, py + 30))

            clip_rect = pygame.Rect(start_x, py + 55, half, AREA_H + 5)
            self.screen.set_clip(clip_rect)
            rects_out.clear()

            for idx, (item_id, count) in enumerate(items_list):
                col = idx % COLS
                row = idx // COLS
                x = start_x + col * (CW + GAP)
                y = py + 58 + row * (CH + GAP) - scroll * (CH + GAP)
                if y + CH < clip_rect.top or y > clip_rect.bottom:
                    continue
                rect = pygame.Rect(x, y, CW, CH)
                rects_out[item_id] = rect
                item = ITEMS.get(item_id, {})
                pygame.draw.rect(self.screen, (38, 28, 16), rect)
                pygame.draw.rect(self.screen, (110, 80, 40), rect, 1)
                icon = render_item_icon(item_id, item.get("color", (128, 128, 128)), 38)
                self.screen.blit(icon, (x + 6, y + (CH - 38) // 2))
                self.screen.blit(self.small.render(item.get("name", item_id), True, (235, 215, 185)),
                                 (x + 50, y + 8))
                self.screen.blit(self.small.render(f"x{count}", True, (160, 220, 160)),
                                 (x + 50, y + 30))

            self.screen.set_clip(None)
            total_rows = max(0, (len(items_list) - 1) // COLS + 1)
            return max(0, total_rows - VISIBLE_ROWS)

        chest_items = sorted(
            [(iid, cnt) for iid, cnt in self.active_chest_inv.items() if cnt > 0],
            key=lambda t: ITEMS.get(t[0], {}).get("name", t[0])
        )
        player_items = sorted(
            [(iid, cnt) for iid, cnt in player.inventory.items() if cnt > 0],
            key=lambda t: ITEMS.get(t[0], {}).get("name", t[0])
        )

        self._max_chest_scroll = _draw_section(
            "CHEST CONTENTS", chest_items, lx, self._chest_scroll, self._chest_rects)
        self._chest_scroll = min(self._chest_scroll, self._max_chest_scroll)

        self._max_player_chest_scroll = _draw_section(
            "YOUR INVENTORY", player_items, rx, self._player_chest_scroll,
            self._player_for_chest_rects)
        self._player_chest_scroll = min(self._player_chest_scroll, self._max_player_chest_scroll)

        if not chest_items:
            empty_s = self.small.render("Chest is empty", True, (80, 65, 45))
            self.screen.blit(empty_s, (lx + half // 2 - empty_s.get_width() // 2, py + 280))
        if not player_items:
            empty_s = self.small.render("Inventory is empty", True, (80, 65, 45))
            self.screen.blit(empty_s, (rx + half // 2 - empty_s.get_width() // 2, py + 280))

    _RARITY_COLOR = {
        "common":    (160, 160, 160),
        "uncommon":  ( 80, 200,  80),
        "rare":      ( 80, 120, 255),
        "epic":      (180,  80, 255),
        "legendary": (255, 180,  40),
    }

    def _draw_garden(self, player):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        self.screen.blit(overlay, (0, 0))

        PW, PH = 1140, 580
        px = (SCREEN_W - PW) // 2
        py = (SCREEN_H - PH) // 2
        pygame.draw.rect(self.screen, (14, 26, 14), (px, py, PW, PH))
        pygame.draw.rect(self.screen, ( 60, 140, 60), (px, py, PW, PH), 2)

        hint = self.small.render(
            "Left-click: move flower  |  E or ESC: close",
            True, (90, 150, 90))
        self.screen.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, py + 8))

        has_flowers = bool(self.active_garden_flowers)
        status_color = (80, 200, 80) if has_flowers else (160, 80, 80)
        status_text  = "Attracting insects" if has_flowers else "No wildflowers — insects won't visit"
        status_s = self.small.render(status_text, True, status_color)
        self.screen.blit(status_s, (SCREEN_W // 2 - status_s.get_width() // 2, py + PH - 24))

        half = (PW - 30) // 2
        lx = px + 10
        rx = px + 20 + half
        pygame.draw.line(self.screen, (40, 90, 40),
                         (px + half + 15, py + 30), (px + half + 15, py + PH - 30), 1)

        CW, CH, GAP = 520, 52, 6
        VISIBLE_ROWS = 7
        AREA_H = VISIBLE_ROWS * (CH + GAP)

        def _draw_section(title, flowers, start_x, scroll, rects_out):
            title_s = self.font.render(title, True, (140, 220, 100))
            self.screen.blit(title_s, (start_x + half // 2 - title_s.get_width() // 2, py + 30))

            clip_rect = pygame.Rect(start_x, py + 55, half, AREA_H + 5)
            self.screen.set_clip(clip_rect)
            rects_out.clear()

            for idx, wf in enumerate(flowers):
                row = idx - scroll
                if row < 0 or row >= VISIBLE_ROWS:
                    continue
                y = py + 58 + row * (CH + GAP)
                rect = pygame.Rect(start_x + 10, y, CW, CH)
                rects_out[wf.uid] = rect
                pygame.draw.rect(self.screen, (24, 40, 24), rect)
                pygame.draw.rect(self.screen, (50, 110, 50), rect, 1)

                # Color swatch
                swatch = pygame.Rect(start_x + 16, y + 8, 36, 36)
                pygame.draw.rect(self.screen, wf.primary_color, swatch)
                pygame.draw.rect(self.screen, wf.secondary_color, swatch, 3)

                # Name and rarity
                name = wf.flower_type.replace("_", " ").title()
                rarity_col = self._RARITY_COLOR.get(wf.rarity, (160, 160, 160))
                self.screen.blit(self.small.render(name, True, (220, 255, 200)),
                                 (start_x + 60, y + 8))
                self.screen.blit(self.small.render(wf.rarity.capitalize(), True, rarity_col),
                                 (start_x + 60, y + 28))
                biome_s = self.small.render(f"  {wf.biodome_found}", True, (100, 160, 100))
                self.screen.blit(biome_s, (start_x + 200, y + 28))

            self.screen.set_clip(None)
            return max(0, len(flowers) - VISIBLE_ROWS)

        self._max_garden_scroll = _draw_section(
            "IN GARDEN", self.active_garden_flowers, lx, self._garden_scroll, self._garden_rects)
        self._garden_scroll = min(self._garden_scroll, self._max_garden_scroll)

        self._max_player_garden_scroll = _draw_section(
            "YOUR WILDFLOWERS", player.wildflowers, rx, self._player_garden_scroll,
            self._player_garden_rects)
        self._player_garden_scroll = min(self._player_garden_scroll, self._max_player_garden_scroll)

        if not self.active_garden_flowers:
            empty_s = self.small.render("Garden is empty", True, (50, 90, 50))
            self.screen.blit(empty_s, (lx + half // 2 - empty_s.get_width() // 2, py + 280))
        if not player.wildflowers:
            empty_s = self.small.render("No wildflowers in collection", True, (50, 90, 50))
            self.screen.blit(empty_s, (rx + half // 2 - empty_s.get_width() // 2, py + 280))

    def _draw_wildflower_display(self, player):
        world = player.world
        bx, by = self.active_display_pos
        stored = world.wildflower_display_data.get((bx, by))

        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        PW, PH = 820, 500
        px = (SCREEN_W - PW) // 2
        py = (SCREEN_H - PH) // 2
        pygame.draw.rect(self.screen, (10, 24, 18), (px, py, PW, PH))
        pygame.draw.rect(self.screen, (80, 160, 100), (px, py, PW, PH), 2)

        hint = self.small.render("Left-click flower to display it  |  Left-click display to reclaim  |  E or ESC: close",
                                 True, (80, 150, 90))
        self.screen.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, py + 8))

        # Left panel: current display slot
        lw = (PW - 30) // 2
        lx = px + 10
        title_s = self.font.render("DISPLAYED", True, (160, 230, 130))
        self.screen.blit(title_s, (lx + lw // 2 - title_s.get_width() // 2, py + 30))
        slot_rect = pygame.Rect(lx + lw // 2 - 60, py + 70, 120, 120)
        pygame.draw.rect(self.screen, (20, 40, 28), slot_rect)
        pygame.draw.rect(self.screen, (60, 120, 80), slot_rect, 2)
        if stored is not None:
            self._draw_wf_preview(stored, slot_rect)
            name_s = self.font.render(stored.flower_type.replace("_", " ").title(), True, (220, 255, 200))
            self.screen.blit(name_s, (lx + lw // 2 - name_s.get_width() // 2, py + 200))
            rar_col = self._RARITY_COLOR.get(stored.rarity, (160, 160, 160))
            rar_s = self.small.render(stored.rarity.capitalize(), True, rar_col)
            self.screen.blit(rar_s, (lx + lw // 2 - rar_s.get_width() // 2, py + 224))
            bio_s = self.small.render(stored.biodome_found, True, (100, 160, 110))
            self.screen.blit(bio_s, (lx + lw // 2 - bio_s.get_width() // 2, py + 244))
        else:
            empty_s = self.small.render("Empty", True, (60, 100, 70))
            self.screen.blit(empty_s, (slot_rect.centerx - empty_s.get_width() // 2,
                                       slot_rect.centery - empty_s.get_height() // 2))

        # Divider
        div_x = px + lw + 20
        pygame.draw.line(self.screen, (40, 90, 50), (div_x, py + 30), (div_x, py + PH - 20), 1)

        # Right panel: player's wildflower collection
        rx = div_x + 10
        title2_s = self.font.render("YOUR WILDFLOWERS", True, (160, 230, 130))
        self.screen.blit(title2_s, (rx + lw // 2 - title2_s.get_width() // 2, py + 30))

        CW, CH, GAP = lw - 20, 50, 5
        VISIBLE = 6
        AREA_H = VISIBLE * (CH + GAP)
        clip = pygame.Rect(rx, py + 55, lw, AREA_H + 5)
        self.screen.set_clip(clip)
        self._display_player_rects.clear()
        for idx, wf in enumerate(player.wildflowers):
            row = idx - getattr(self, '_display_scroll', 0)
            if row < 0 or row >= VISIBLE:
                continue
            y = py + 58 + row * (CH + GAP)
            rect = pygame.Rect(rx + 10, y, CW, CH)
            self._display_player_rects[wf.uid] = rect
            bg = (30, 50, 35) if stored and stored.uid == wf.uid else (20, 38, 26)
            pygame.draw.rect(self.screen, bg, rect)
            pygame.draw.rect(self.screen, (50, 110, 65), rect, 1)
            swatch = pygame.Rect(rx + 16, y + 7, 36, 36)
            pygame.draw.rect(self.screen, wf.primary_color, swatch)
            pygame.draw.rect(self.screen, wf.secondary_color, swatch, 3)
            name_s = self.small.render(wf.flower_type.replace("_", " ").title(), True, (210, 245, 195))
            self.screen.blit(name_s, (rx + 60, y + 7))
            rar_col = self._RARITY_COLOR.get(wf.rarity, (160, 160, 160))
            self.screen.blit(self.small.render(wf.rarity.capitalize(), True, rar_col), (rx + 60, y + 27))
        self.screen.set_clip(None)

        max_scroll = max(0, len(player.wildflowers) - VISIBLE)
        self._display_scroll = min(getattr(self, '_display_scroll', 0), max_scroll)
        if not player.wildflowers:
            empty_s = self.small.render("No wildflowers in collection", True, (50, 90, 60))
            self.screen.blit(empty_s, (rx + lw // 2 - empty_s.get_width() // 2, py + 240))

    def _draw_wf_preview(self, wf, slot_rect):
        import math as _math
        cx = slot_rect.centerx
        cy = slot_rect.centery
        pygame.draw.line(self.screen, (50, 140, 40), (cx, cy + 20), (cx, cy - 20), 2)
        for i in range(wf.petal_count):
            ang = i * 2 * _math.pi / wf.petal_count - _math.pi / 2
            px = int(cx + 22 * _math.cos(ang))
            py = int(cy - 12 + 22 * _math.sin(ang))
            col = wf.primary_color if i % 2 == 0 else wf.secondary_color
            pygame.draw.circle(self.screen, col, (px, py), 10)
        pygame.draw.circle(self.screen, wf.center_color, (cx, cy - 12), 8)

    _STATUS_COLOR = {
        "active":         (80, 220, 80),
        "halted_fuel":    (220, 140, 40),
        "halted_full":    (220, 220, 40),
        "halted_blocked": (220, 60, 60),
    }
    _STATUS_LABEL = {
        "active":         "Active",
        "halted_fuel":    "Out of Fuel",
        "halted_full":    "Storage Full",
        "halted_blocked": "Blocked",
    }

    def _draw_resource_row(self, label, value, max_val, item_name, bar_color,
                           btn1_attr, btnall_attr, has_resource, y_label,
                           px, bar_w, btn_row_y):
        """Draw a labeled bar + two deposit buttons for a resource (fuel or supports)."""
        lbl = self.small.render(label, True, (200, 190, 230))
        self.screen.blit(lbl, (px + 14, y_label))
        val_txt = self.small.render(f"{int(value)} / {max_val}  {item_name}", True, (180, 170, 210))
        self.screen.blit(val_txt, (px + 14 + lbl.get_width() + 6, y_label))

        bar_x, bar_y, bar_h = px + 14, y_label + 16, 14
        frac = value / max_val if max_val > 0 else 0
        pygame.draw.rect(self.screen, (35, 30, 45), (bar_x, bar_y, bar_w, bar_h))
        if frac > 0:
            pygame.draw.rect(self.screen, bar_color, (bar_x, bar_y, int(bar_w * frac), bar_h))
        pygame.draw.rect(self.screen, (80, 70, 100), (bar_x, bar_y, bar_w, bar_h), 1)

        BW, BH = 130, 26
        col    = (30, 80, 30) if has_resource else (30, 30, 40)
        border = (60, 180, 60) if has_resource else (55, 55, 68)
        tc     = (160, 255, 160) if has_resource else (70, 70, 82)
        for i, (lbl_txt, attr) in enumerate([("Deposit 1", btn1_attr), ("Deposit All", btnall_attr)]):
            bx_ = px + 14 + i * (BW + 8)
            btn = pygame.Rect(bx_, btn_row_y, BW, BH)
            setattr(self, attr, btn)
            pygame.draw.rect(self.screen, col, btn)
            pygame.draw.rect(self.screen, border, btn, 1)
            t = self.small.render(lbl_txt, True, tc)
            self.screen.blit(t, (bx_ + BW // 2 - t.get_width() // 2,
                                  btn_row_y + BH // 2 - t.get_height() // 2))

    def _draw_automation_panel(self, player):
        auto = self.active_automation
        adef = auto._def
        PW, PH = 480, 420
        px = (SCREEN_W - PW) // 2
        py = (SCREEN_H - PH) // 2
        bar_w = PW - 28

        # Background
        panel = pygame.Surface((PW, PH), pygame.SRCALPHA)
        panel.fill((20, 18, 28, 230))
        self.screen.blit(panel, (px, py))
        pygame.draw.rect(self.screen, (80, 70, 100), (px, py, PW, PH), 2)

        # Title + close hint
        title = self.font.render(adef["name"].upper(), True, (230, 220, 255))
        self.screen.blit(title, (px + 14, py + 10))
        hint = self.small.render("[E] close", True, (120, 110, 150))
        self.screen.blit(hint, (px + PW - hint.get_width() - 10, py + 13))

        # Status
        status = auto.status
        sc = self._STATUS_COLOR.get(status, (180, 180, 180))
        sl = self._STATUS_LABEL.get(status, status)
        st = self.small.render(f"Status: {sl}", True, sc)
        self.screen.blit(st, (px + 14, py + 32))

        pygame.draw.line(self.screen, (70, 60, 90), (px + 10, py + 52), (px + PW - 10, py + 52))

        # --- Fuel section ---
        fuel_item_name = ITEMS.get(adef["fuel_item"], {}).get("name", adef["fuel_item"])
        self._draw_resource_row(
            "FUEL", auto.fuel, adef["fuel_tank"], fuel_item_name,
            (220, 155, 40),
            "_auto_deposit1_btn", "_auto_deposit_all_btn",
            player.inventory.get(adef["fuel_item"], 0) > 0,
            py + 58, px, bar_w, py + 90,
        )

        pygame.draw.line(self.screen, (70, 60, 90), (px + 10, py + 124), (px + PW - 10, py + 124))

        # --- Stored items section ---
        inv_count = auto.inv_count
        inv_label = self.small.render("STORED ITEMS", True, (200, 190, 230))
        self.screen.blit(inv_label, (px + 14, py + 130))
        count_label = self.small.render(f"{inv_count} / {adef['inv_limit']}", True, (160, 150, 200))
        self.screen.blit(count_label, (px + PW - count_label.get_width() - 14, py + 130))

        SW, SH, GAP = 44, 44, 6
        items_per_row = (PW - 28 + GAP) // (SW + GAP)
        ix0, iy0 = px + 14, py + 148
        for idx, (item_id, count) in enumerate(sorted(auto.stored.items())):
            col_i = idx % items_per_row
            row_i = idx // items_per_row
            sx_ = ix0 + col_i * (SW + GAP)
            sy_ = iy0 + row_i * (SH + GAP)
            if sy_ + SH > py + 298:
                break
            item_color = ITEMS.get(item_id, {}).get("color", (120, 120, 120))
            pygame.draw.rect(self.screen, item_color, (sx_, sy_, SW, SH))
            pygame.draw.rect(self.screen, (80, 70, 100), (sx_, sy_, SW, SH), 1)
            c_surf = self.small.render(str(count), True, (255, 255, 255))
            self.screen.blit(c_surf, (sx_ + SW - c_surf.get_width() - 2, sy_ + SH - c_surf.get_height() - 1))
            name_surf = self.small.render(
                ITEMS.get(item_id, {}).get("name", item_id)[:6], True, (220, 220, 220)
            )
            self.screen.blit(name_surf, (sx_ + 2, sy_ + 2))

        if inv_count == 0:
            empty = self.small.render("(empty)", True, (100, 90, 120))
            self.screen.blit(empty, (ix0, iy0 + 10))

        pygame.draw.line(self.screen, (70, 60, 90), (px + 10, py + 304), (px + PW - 10, py + 304))

        # --- Direction section ---
        dir_lbl = self.small.render("DIRECTION", True, (200, 190, 230))
        self.screen.blit(dir_lbl, (px + 14, py + 312))

        _DIRS = [
            ((-1, 0), "← Left"),
            ((1,  0), "→ Right"),
            ((0, -1), "↑ Up"),
            ((0,  1), "↓ Down"),
        ]
        DBW, DBH, DB_GAP = 98, 26, 6
        self._auto_dir_btns = {}
        cur_dir = tuple(auto.direction)
        for i, (d, label) in enumerate(_DIRS):
            bx_ = px + 14 + i * (DBW + DB_GAP)
            btn = pygame.Rect(bx_, py + 328, DBW, DBH)
            self._auto_dir_btns[d] = btn
            selected = (d == cur_dir)
            bg  = (40, 50, 80) if selected else (25, 22, 38)
            bdr = (120, 160, 255) if selected else (60, 55, 80)
            tc  = (200, 220, 255) if selected else (100, 90, 130)
            pygame.draw.rect(self.screen, bg, btn)
            pygame.draw.rect(self.screen, bdr, btn, 1 if not selected else 2)
            t = self.small.render(label, True, tc)
            self.screen.blit(t, (bx_ + DBW // 2 - t.get_width() // 2,
                                  py + 328 + DBH // 2 - t.get_height() // 2))

        pygame.draw.line(self.screen, (70, 60, 90), (px + 10, py + 362), (px + PW - 10, py + 362))

        # --- Bottom buttons: Pick Up (left) + Take All (right) ---
        BW, BH = 140, 28
        by_ = py + 372

        # Pick Up button
        self._auto_pickup_btn = pygame.Rect(px + 14, by_, BW, BH)
        pygame.draw.rect(self.screen, (50, 30, 70), self._auto_pickup_btn)
        pygame.draw.rect(self.screen, (140, 80, 200), self._auto_pickup_btn, 1)
        pu_t = self.small.render("PICK UP", True, (200, 150, 255))
        self.screen.blit(pu_t, (px + 14 + BW // 2 - pu_t.get_width() // 2,
                                 by_ + BH // 2 - pu_t.get_height() // 2))

        # Take All button
        has_items = inv_count > 0
        t_col     = (30, 80, 30)    if has_items else (30, 30, 40)
        t_border  = (60, 180, 60)   if has_items else (55, 55, 68)
        t_txt_col = (160, 255, 160) if has_items else (70, 70, 82)
        self._auto_take_btn = pygame.Rect(px + PW - BW - 14, by_, BW, BH)
        pygame.draw.rect(self.screen, t_col, self._auto_take_btn)
        pygame.draw.rect(self.screen, t_border, self._auto_take_btn, 1)
        take_t = self.small.render("TAKE ALL ITEMS", True, t_txt_col)
        self.screen.blit(take_t, (self._auto_take_btn.x + BW // 2 - take_t.get_width() // 2,
                                   by_ + BH // 2 - take_t.get_height() // 2))

    def handle_automation_click(self, pos, player):
        auto = self.active_automation
        if auto is None:
            return None
        if self._auto_deposit1_btn and self._auto_deposit1_btn.collidepoint(pos):
            auto.deposit_fuel(player, 1)
        elif self._auto_deposit_all_btn and self._auto_deposit_all_btn.collidepoint(pos):
            auto.deposit_fuel(player)
        elif self._auto_take_btn and self._auto_take_btn.collidepoint(pos):
            auto.take_all(player)
        elif self._auto_pickup_btn and self._auto_pickup_btn.collidepoint(pos):
            return "pickup"
        else:
            for direction, btn in self._auto_dir_btns.items():
                if btn.collidepoint(pos):
                    auto.set_direction(direction)
                    break
        return None

    def _draw_farm_bot_panel(self, player):
        fb = self.active_farm_bot
        adef = fb._def
        PW, PH = 480, 460
        px = (SCREEN_W - PW) // 2
        py = (SCREEN_H - PH) // 2
        bar_w = PW - 28

        panel = pygame.Surface((PW, PH), pygame.SRCALPHA)
        panel.fill((18, 28, 20, 230))
        self.screen.blit(panel, (px, py))
        pygame.draw.rect(self.screen, (60, 100, 70), (px, py, PW, PH), 2)

        # Title
        title = self.font.render(adef["name"].upper(), True, (200, 255, 200))
        self.screen.blit(title, (px + 14, py + 10))
        hint = self.small.render("[E] close", True, (100, 150, 110))
        self.screen.blit(hint, (px + PW - hint.get_width() - 10, py + 13))

        # Status
        status = fb.status
        sc = self._STATUS_COLOR.get(status, (180, 180, 180))
        sl = self._STATUS_LABEL.get(status, status)
        st = self.small.render(f"Status: {sl}", True, sc)
        self.screen.blit(st, (px + 14, py + 32))
        r_t = self.small.render(f"Scan radius: {adef['scan_radius']} blocks", True, (120, 160, 130))
        self.screen.blit(r_t, (px + PW - r_t.get_width() - 14, py + 32))

        pygame.draw.line(self.screen, (60, 100, 70), (px + 10, py + 52), (px + PW - 10, py + 52))

        # Fuel section
        fuel_item_name = ITEMS.get(adef["fuel_item"], {}).get("name", adef["fuel_item"])
        self._draw_resource_row(
            "FUEL", fb.fuel, adef["fuel_tank"], fuel_item_name,
            (220, 155, 40),
            "_fb_deposit1_btn", "_fb_deposit_all_btn",
            player.inventory.get(adef["fuel_item"], 0) > 0,
            py + 58, px, bar_w, py + 90,
        )

        pygame.draw.line(self.screen, (60, 100, 70), (px + 10, py + 124), (px + PW - 10, py + 124))

        # Seeds section
        seeds_label = self.small.render("SEEDS LOADED", True, (180, 230, 180))
        self.screen.blit(seeds_label, (px + 14, py + 130))
        has_seeds_in_inv = any(
            idata.get("place_block") in __import__("blocks").YOUNG_CROP_BLOCKS
            and player.inventory.get(iid, 0) > 0
            for iid, idata in ITEMS.items()
        )
        has_seeds_in_bot = bool(fb.seeds)
        BW, BH = 152, 22
        # Deposit All Seeds button (right side)
        btn_col    = (20, 60, 25) if has_seeds_in_inv else (25, 30, 25)
        btn_border = (60, 180, 80) if has_seeds_in_inv else (50, 60, 50)
        btn_tc     = (140, 255, 160) if has_seeds_in_inv else (60, 70, 60)
        self._fb_seeds_btn = pygame.Rect(px + PW - BW - 14, py + 127, BW, BH)
        pygame.draw.rect(self.screen, btn_col, self._fb_seeds_btn)
        pygame.draw.rect(self.screen, btn_border, self._fb_seeds_btn, 1)
        bt = self.small.render("Deposit All Seeds", True, btn_tc)
        self.screen.blit(bt, (self._fb_seeds_btn.x + BW // 2 - bt.get_width() // 2,
                               self._fb_seeds_btn.y + BH // 2 - bt.get_height() // 2))
        # Get Seeds button (left of deposit button)
        gs_col    = (20, 50, 60) if has_seeds_in_bot else (25, 28, 30)
        gs_border = (60, 160, 200) if has_seeds_in_bot else (40, 50, 55)
        gs_tc     = (120, 220, 255) if has_seeds_in_bot else (50, 60, 65)
        self._fb_get_seeds_btn = pygame.Rect(px + PW - BW * 2 - 20, py + 127, BW, BH)
        pygame.draw.rect(self.screen, gs_col, self._fb_get_seeds_btn)
        pygame.draw.rect(self.screen, gs_border, self._fb_get_seeds_btn, 1)
        gs_t = self.small.render("Get Seeds", True, gs_tc)
        self.screen.blit(gs_t, (self._fb_get_seeds_btn.x + BW // 2 - gs_t.get_width() // 2,
                                 self._fb_get_seeds_btn.y + BH // 2 - gs_t.get_height() // 2))

        # Show loaded seeds as small items
        SW2, GAP2 = 36, 4
        ix0, iy0 = px + 14, py + 156
        for idx, (seed_id, count) in enumerate(sorted(fb.seeds.items())):
            sx_ = ix0 + idx * (SW2 + GAP2)
            if sx_ + SW2 > px + PW - 14:
                break
            seed_color = ITEMS.get(seed_id, {}).get("color", (120, 160, 90))
            pygame.draw.rect(self.screen, seed_color, (sx_, iy0, SW2, SW2))
            pygame.draw.rect(self.screen, (60, 100, 70), (sx_, iy0, SW2, SW2), 1)
            c_surf = self.small.render(str(count), True, (255, 255, 255))
            self.screen.blit(c_surf, (sx_ + SW2 - c_surf.get_width() - 2, iy0 + SW2 - c_surf.get_height() - 1))
        if not fb.seeds:
            empty_s = self.small.render("(no seeds)", True, (80, 110, 80))
            self.screen.blit(empty_s, (ix0, iy0 + 8))

        pygame.draw.line(self.screen, (60, 100, 70), (px + 10, py + 200), (px + PW - 10, py + 200))

        # Stored produce section
        inv_count = fb.inv_count
        inv_label = self.small.render("HARVESTED PRODUCE", True, (200, 230, 200))
        self.screen.blit(inv_label, (px + 14, py + 206))
        count_label = self.small.render(f"{inv_count} / {adef['inv_limit']}", True, (140, 180, 150))
        self.screen.blit(count_label, (px + PW - count_label.get_width() - 14, py + 206))

        SW, SH, GAP = 44, 44, 6
        items_per_row = (PW - 28 + GAP) // (SW + GAP)
        ix0, iy0 = px + 14, py + 224
        for idx, (item_id, count) in enumerate(sorted(fb.stored.items())):
            col_i = idx % items_per_row
            row_i = idx // items_per_row
            sx_ = ix0 + col_i * (SW + GAP)
            sy_ = iy0 + row_i * (SH + GAP)
            if sy_ + SH > py + PH - 50:
                break
            item_color = ITEMS.get(item_id, {}).get("color", (120, 120, 120))
            pygame.draw.rect(self.screen, item_color, (sx_, sy_, SW, SH))
            pygame.draw.rect(self.screen, (60, 100, 70), (sx_, sy_, SW, SH), 1)
            c_surf = self.small.render(str(count), True, (255, 255, 255))
            self.screen.blit(c_surf, (sx_ + SW - c_surf.get_width() - 2, sy_ + SH - c_surf.get_height() - 1))
            name_surf = self.small.render(ITEMS.get(item_id, {}).get("name", item_id)[:6], True, (220, 240, 220))
            self.screen.blit(name_surf, (sx_ + 2, sy_ + 2))

        if inv_count == 0:
            empty = self.small.render("(empty)", True, (80, 110, 80))
            self.screen.blit(empty, (ix0, iy0 + 10))

        # Take All button
        TW, TH = 140, 28
        tx = px + PW - TW - 14
        ty = py + PH - TH - 10
        has_items = inv_count > 0
        t_col    = (20, 70, 25)    if has_items else (25, 30, 25)
        t_border = (50, 180, 70)   if has_items else (50, 60, 50)
        t_txt_col = (140, 255, 160) if has_items else (60, 70, 60)
        self._fb_take_btn = pygame.Rect(tx, ty, TW, TH)
        pygame.draw.rect(self.screen, t_col, self._fb_take_btn)
        pygame.draw.rect(self.screen, t_border, self._fb_take_btn, 1)
        take_t = self.small.render("TAKE ALL ITEMS", True, t_txt_col)
        self.screen.blit(take_t, (tx + TW // 2 - take_t.get_width() // 2,
                                   ty + TH // 2 - take_t.get_height() // 2))

        # Pick Up button
        PUW, PUH = 100, 28
        pux = px + 14
        puy = py + PH - PUH - 10
        self._fb_pickup_btn = pygame.Rect(pux, puy, PUW, PUH)
        pygame.draw.rect(self.screen, (50, 30, 70), self._fb_pickup_btn)
        pygame.draw.rect(self.screen, (140, 80, 200), self._fb_pickup_btn, 1)
        pu_t = self.small.render("PICK UP", True, (200, 160, 255))
        self.screen.blit(pu_t, (pux + PUW // 2 - pu_t.get_width() // 2,
                                 puy + PUH // 2 - pu_t.get_height() // 2))

    def handle_farm_bot_click(self, pos, player):
        fb = self.active_farm_bot
        if fb is None:
            return
        if self._fb_deposit1_btn and self._fb_deposit1_btn.collidepoint(pos):
            fb.deposit_fuel(player, 1)
        elif self._fb_deposit_all_btn and self._fb_deposit_all_btn.collidepoint(pos):
            fb.deposit_fuel(player)
        elif self._fb_seeds_btn and self._fb_seeds_btn.collidepoint(pos):
            fb.deposit_all_seeds(player)
        elif self._fb_get_seeds_btn and self._fb_get_seeds_btn.collidepoint(pos):
            fb.get_seeds(player)
        elif self._fb_take_btn and self._fb_take_btn.collidepoint(pos):
            fb.take_all(player)
        elif self._fb_pickup_btn and self._fb_pickup_btn.collidepoint(pos):
            return "pickup"

    def _draw_animal_preview(self, animal, cx, cy, scale=3.5):
        """Draw a scaled animal preview centred at (cx, cy) on self.screen."""
        def _t(base, sh):
            return tuple(max(0, min(255, int(base[i] + sh[i] * 255))) for i in range(3))
        aid    = getattr(animal, 'animal_id', '')
        traits = getattr(animal, 'traits', {})
        sh     = traits.get("color_shift", (0, 0, 0))
        if traits.get("mutation") == "golden":
            sh = (0.35, 0.25, -0.30)
        s      = traits.get("size", 1.0) * scale
        if aid == "sheep":
            BW, BH = int(24 * s), int(18 * s)
            sx, sy = cx - BW // 2, cy - BH // 2
            bh = BH - int(8 * s)
            for lo in (2, 7, 14, 19):
                pygame.draw.rect(self.screen, (80, 60, 40),
                                 (sx + int(lo * s), sy + bh, max(1, int(3 * s)), int(8 * s)))
            bclr = _t((220, 220, 220) if getattr(animal, 'has_wool', True) else (175, 140, 95), sh)
            pygame.draw.rect(self.screen, bclr, (sx, sy, BW, bh))
            hw, hh = int(9 * s), int(9 * s)
            hclr = _t((200, 200, 200) if getattr(animal, 'has_wool', True) else (155, 125, 85), sh)
            hx = sx + BW - int(2 * s)
            hy = sy - max(1, int(1 * s))
            pygame.draw.rect(self.screen, hclr, (hx, hy, hw, hh))
            pygame.draw.rect(self.screen, (30, 30, 30),
                             (hx + hw - int(3 * s), hy + int(3 * s), max(1, int(2 * s)), max(1, int(2 * s))))
        elif aid == "cow":
            BW, BH = int(30 * s), int(20 * s)
            sx, sy = cx - BW // 2, cy - BH // 2
            bh = BH - int(8 * s)
            for lo in (2, 8, 18, 24):
                pygame.draw.rect(self.screen, (60, 40, 30),
                                 (sx + int(lo * s), sy + bh, max(1, int(4 * s)), int(8 * s)))
            bclr = _t((140, 85, 45), sh)
            pygame.draw.rect(self.screen, bclr, (sx, sy, BW, bh))
            pygame.draw.rect(self.screen, (30, 20, 10),
                             (sx + int(8 * s), sy + int(2 * s), int(10 * s), int(5 * s)))
            hw, hh = int(11 * s), int(11 * s)
            hx = sx + BW - int(3 * s)
            hy = sy - int(2 * s)
            hclr = _t((140, 85, 45), sh)
            pygame.draw.rect(self.screen, hclr, (hx, hy, hw, hh))
            pygame.draw.rect(self.screen, _t((190, 130, 100), sh),
                             (hx + hw - int(4 * s), hy + int(6 * s), int(4 * s), int(4 * s)))
            pygame.draw.rect(self.screen, (20, 10, 5),
                             (hx + hw - int(4 * s), hy + int(2 * s), max(1, int(2 * s)), max(1, int(2 * s))))
        elif aid == "goat":
            BW, BH = int(22 * s), int(18 * s)
            sx, sy = cx - BW // 2, cy - BH // 2
            bh = BH - int(8 * s)
            for lo in (2, 6, 13, 17):
                pygame.draw.rect(self.screen, _t((90, 70, 50), sh),
                                 (sx + int(lo * s), sy + bh, max(1, int(3 * s)), int(8 * s)))
            bclr = _t((195, 180, 155), sh)
            pygame.draw.rect(self.screen, bclr, (sx, sy, BW, bh))
            hw, hh = int(9 * s), int(9 * s)
            hclr = _t((185, 170, 145), sh)
            hx = sx + BW - int(2 * s)
            hy = sy - int(2 * s)
            pygame.draw.rect(self.screen, hclr, (hx, hy, hw, hh))
            # horns
            horn_c = _t((80, 65, 45), sh)
            pygame.draw.rect(self.screen, horn_c, (hx + int(1 * s), hy - int(4 * s), max(1, int(2 * s)), int(4 * s)))
            pygame.draw.rect(self.screen, horn_c, (hx + int(5 * s), hy - int(5 * s), max(1, int(2 * s)), int(5 * s)))
            # beard
            pygame.draw.rect(self.screen, _t((155, 140, 115), sh),
                             (hx + int(1 * s), hy + hh, max(1, int(2 * s)), max(1, int(4 * s))))
            # eye
            pygame.draw.rect(self.screen, (20, 12, 5),
                             (hx + hw - int(3 * s), hy + int(3 * s), max(1, int(2 * s)), max(1, int(2 * s))))
        elif aid == "chicken":
            BW, BH = int(18 * s), int(16 * s)
            sx, sy = cx - BW // 2, cy - BH // 2
            for lo in (4, 11):
                pygame.draw.rect(self.screen, (220, 160, 30),
                                 (sx + int(lo * s), sy + BH - int(6 * s), max(1, int(2 * s)), int(6 * s)))
            bclr = _t((235, 235, 210), sh)
            pygame.draw.ellipse(self.screen, bclr,
                                (sx + max(1, int(1 * s)), sy + int(2 * s),
                                 max(2, BW - int(4 * s)), max(2, BH - int(8 * s))))
            hw, hh = int(8 * s), int(8 * s)
            hx = sx + BW - int(4 * s)
            hy = sy - int(2 * s)
            pygame.draw.ellipse(self.screen, bclr, (hx, hy, max(4, hw), max(4, hh)))
            pygame.draw.rect(self.screen, (220, 160, 30),
                             (hx + hw - max(1, int(1 * s)), hy + int(3 * s),
                              max(1, int(3 * s)), max(1, int(2 * s))))
            pygame.draw.rect(self.screen, (20, 20, 20),
                             (hx + hw - int(3 * s), hy + int(2 * s), max(1, int(2 * s)), max(1, int(2 * s))))
            pygame.draw.rect(self.screen, (220, 50, 50),
                             (hx + int(2 * s), hy - max(1, int(2 * s)),
                              max(1, int(4 * s)), max(1, int(3 * s))))
        elif aid == "dog":
            draw_dog(self.screen, cx - int(17 * s), cy - int(11 * s), animal, scale=s, facing=1)
        elif aid == "horse":
            coat  = traits.get("coat_color", (160, 115, 65))
            sh    = traits.get("color_shift", (0, 0, 0))
            body_color = _t(coat, sh)
            dark_coat  = tuple(max(0, c - 40) for c in body_color)
            mane_color = tuple(max(0, c - 60) for c in body_color)
            BW, BH = int(40 * s), int(26 * s)
            sx2, sy2 = cx - BW // 2, cy - BH // 2
            body_h = int(BH * 0.65)
            leg_h  = BH - body_h
            leg_y  = sy2 + body_h
            leg_w  = max(1, int(4 * s))
            for lx_off in [3, 9, 22, 28]:
                pygame.draw.rect(self.screen, dark_coat,
                                 (sx2 + int(lx_off * s), leg_y, leg_w, leg_h))
                pygame.draw.rect(self.screen, (30, 25, 20),
                                 (sx2 + int(lx_off * s), leg_y + leg_h - max(1, int(2 * s)), leg_w, max(1, int(2 * s))))
            pygame.draw.rect(self.screen, body_color, (sx2, sy2, BW, body_h))
            pygame.draw.rect(self.screen, mane_color,
                             (sx2 + int(4 * s), sy2, int((BW - 8) * s), max(2, int(4 * s))))
            pygame.draw.rect(self.screen, mane_color,
                             (sx2, sy2 + int(4 * s), max(2, int(4 * s)), int(body_h * 0.6)))
            head_w = int(12 * s)
            head_h = int(12 * s)
            hx2 = sx2 + BW - int(2 * s)
            hy2 = sy2 - int(4 * s)
            pygame.draw.rect(self.screen, body_color, (hx2, hy2, head_w, head_h))
            pygame.draw.rect(self.screen, _t((200, 175, 145), sh),
                             (hx2 + head_w - int(5 * s), hy2 + int(6 * s), int(5 * s), int(5 * s)))
            pygame.draw.rect(self.screen, (15, 10, 5),
                             (hx2 + head_w - int(5 * s), hy2 + int(3 * s), max(1, int(2 * s)), max(1, int(2 * s))))

    def handle_breeding_click(self, pos, player):
        for tab_idx, rect in self._breed_tab_rects.items():
            if rect.collidepoint(pos):
                if self._breed_tab != tab_idx:
                    self._breed_tab = tab_idx
                    self._breed_scroll = 0
                    self._breed_selected_uid = None
                return
        # No-breed toggle button
        nb_rects = getattr(self, '_breed_nb_rects', {})
        for uid, rect in nb_rects.items():
            if rect.collidepoint(pos):
                world = self.world_ref
                if world:
                    entity = next((e for e in world.entities if getattr(e, 'uid', None) == uid), None)
                    if entity:
                        entity.no_breed = not entity.no_breed
                return
        for uid, rect in self._breed_list_rects.items():
            if rect.collidepoint(pos):
                self._breed_selected_uid = uid if uid != self._breed_selected_uid else None
                return

    def _draw_breeding(self, player):
        world = self.world_ref
        if world is None:
            return

        ov = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 215))
        self.screen.blit(ov, (0, 0))

        PW, PH = 1060, 580
        px = (SCREEN_W - PW) // 2
        py = (SCREEN_H - PH) // 2

        pygame.draw.rect(self.screen, (16, 22, 20), (px, py, PW, PH))
        pygame.draw.rect(self.screen, (55, 120, 75), (px, py, PW, PH), 2)

        # All living tamed animals; uid map for the whole world
        all_tamed = [e for e in world.entities
                     if getattr(e, 'tamed', False) and not getattr(e, 'dead', False)]
        uid_map   = {e.uid: e for e in world.entities if hasattr(e, 'uid')}

        # Stable numbering within each type (by appearance order in all_tamed)
        type_ctr       = {}
        animal_numbers = {}
        for e in all_tamed:
            aid = e.animal_id
            type_ctr[aid] = type_ctr.get(aid, 0) + 1
            animal_numbers[e.uid] = type_ctr[aid]

        TYPE_LABELS = {"sheep": "Sheep", "cow": "Cow", "chicken": "Chicken", "horse": "Horse", "goat": "Goat", "dog": "Dog"}

        # ── LEFT LIST COLUMN ──────────────────────────────────────────
        LW = 295
        lx0 = px
        lx1 = px + LW

        title_s = self.font.render(f"ANIMALS  ({len(all_tamed)})", True, (110, 210, 135))
        self.screen.blit(title_s, (lx0 + LW // 2 - title_s.get_width() // 2, py + 10))

        # Species filter tabs
        tab_defs = [(0, "All"), (1, "Sheep"), (2, "Cow"), (3, "Chicken"), (4, "Horse"), (5, "Goat"), (6, "Dogs")]
        tw = (LW - 6) // len(tab_defs)
        self._breed_tab_rects.clear()
        for ti, (tidx, label) in enumerate(tab_defs):
            tx = lx0 + ti * (tw + 2)
            tr = pygame.Rect(tx, py + 36, tw, 22)
            self._breed_tab_rects[tidx] = tr
            active = (tidx == self._breed_tab)
            pygame.draw.rect(self.screen, (28, 62, 40) if active else (20, 30, 24), tr)
            pygame.draw.rect(self.screen, (55, 150, 80) if active else (38, 65, 48), tr, 1)
            lbl = self.small.render(label, True, (150, 255, 170) if active else (90, 130, 105))
            self.screen.blit(lbl, (tx + tw // 2 - lbl.get_width() // 2,
                                   py + 36 + 11 - lbl.get_height() // 2))

        # Divider
        pygame.draw.line(self.screen, (38, 75, 52), (lx1, py), (lx1, py + PH))

        # Build filtered list
        tab_filter = {1: "sheep", 2: "cow", 3: "chicken", 4: "horse", 5: "goat", 6: "dog"}.get(self._breed_tab)
        filtered = [e for e in all_tamed
                    if tab_filter is None or e.animal_id == tab_filter]

        ROW_H   = 54
        list_y0 = py + 64
        list_h  = PH - 68
        vis     = list_h // ROW_H
        self._max_breed_scroll = max(0, len(filtered) - vis)
        self._breed_scroll     = max(0, min(self._max_breed_scroll, self._breed_scroll))

        clip_rect = pygame.Rect(lx0, list_y0, LW, list_h)
        old_clip  = self.screen.get_clip()
        self.screen.set_clip(clip_rect)
        self._breed_list_rects.clear()

        for i, animal in enumerate(filtered[self._breed_scroll: self._breed_scroll + vis + 1]):
            ry  = list_y0 + i * ROW_H
            row = pygame.Rect(lx0, ry, LW - 1, ROW_H - 2)
            sel = (animal.uid == self._breed_selected_uid)
            pygame.draw.rect(self.screen, (26, 50, 34) if sel else (18, 28, 22), row)
            if sel:
                pygame.draw.rect(self.screen, (70, 170, 95), row, 1)

            self._draw_animal_preview(animal, lx0 + 28, ry + ROW_H // 2, scale=1.4)

            num  = animal_numbers.get(animal.uid, 1)
            name = f"{TYPE_LABELS.get(animal.animal_id, animal.animal_id)} #{num}"
            nl   = self.small.render(name, True, (195, 240, 210))
            self.screen.blit(nl, (lx0 + 60, ry + 8))

            uid_s = self.small.render(animal.uid[:12], True, (70, 95, 80))
            self.screen.blit(uid_s, (lx0 + 60, ry + 23))

            row_mut = getattr(animal, 'traits', {}).get('mutation')
            if row_mut is not None:
                _MUT_ABBREV = {"albino": "ALB", "giant": "GNT", "miniature": "MIN", "golden": "GLD"}
                _MUT_RCOLS  = {"albino": (200, 200, 255), "giant": (120, 220, 90),
                               "miniature": (100, 160, 240), "golden": (240, 195, 50)}
                tag_s = self.small.render(_MUT_ABBREV.get(row_mut, row_mut[:3].upper()),
                                          True, _MUT_RCOLS.get(row_mut, (200, 200, 200)))
                self.screen.blit(tag_s, (lx0 + LW - 30 - tag_s.get_width(), ry + 23))

            breed_ready = animal._breed_cooldown <= 0
            no_breed = getattr(animal, 'no_breed', False)
            dot_col = (175, 75, 75) if no_breed else ((75, 215, 100) if breed_ready else (175, 75, 75))
            pygame.draw.circle(self.screen, dot_col, (lx0 + LW - 15, ry + ROW_H // 2), 5)
            if no_breed:
                nb_tag = self.small.render("✗", True, (210, 80, 80))
                self.screen.blit(nb_tag, (lx0 + LW - 10 - nb_tag.get_width(), ry + 8))

            self._breed_list_rects[animal.uid] = row

        self.screen.set_clip(old_clip)

        if not filtered:
            empty = self.small.render("No tamed animals in this category", True, (70, 95, 80))
            self.screen.blit(empty, (lx0 + LW // 2 - empty.get_width() // 2, list_y0 + 30))

        # ── RIGHT DETAIL COLUMN ───────────────────────────────────────
        rx0 = lx1 + 10
        rw  = PW - LW - 10

        if self._breed_selected_uid is None:
            msg = self.font.render("Select an animal to view details", True, (70, 100, 80))
            self.screen.blit(msg, (rx0 + rw // 2 - msg.get_width() // 2, py + PH // 2 - 20))
            legend_rows = [((75, 215, 100), "Ready to breed"),
                           ((175, 75, 75),  "Breed cooldown")]
            for li, (dot_col, dot_txt) in enumerate(legend_rows):
                ly = py + PH // 2 + 10 + li * 18
                pygame.draw.circle(self.screen, dot_col, (rx0 + rw // 2 - 55, ly + 5), 5)
                lg = self.small.render(dot_txt, True, (100, 135, 110))
                self.screen.blit(lg, (rx0 + rw // 2 - 45, ly))
            return

        animal = uid_map.get(self._breed_selected_uid)
        if animal is None or getattr(animal, 'dead', False):
            self._breed_selected_uid = None
            return

        num   = animal_numbers.get(animal.uid, 1)
        tname = TYPE_LABELS.get(animal.animal_id, animal.animal_id)

        # Header row
        hdg = self.font.render(f"{tname}  #{num}", True, (170, 255, 195))
        self.screen.blit(hdg, (rx0 + 12, py + 12))

        uid_lbl = self.small.render(f"uid: {animal.uid[:18]}…", True, (65, 90, 75))
        self.screen.blit(uid_lbl, (rx0 + 12, py + 35))

        breed_ready = animal._breed_cooldown <= 0
        if breed_ready:
            bst_s = self.small.render("● READY TO BREED", True, (75, 215, 100))
        else:
            m = int(animal._breed_cooldown // 60)
            s_rem = int(animal._breed_cooldown % 60)
            bst_s = self.small.render(f"● COOLDOWN  {m}m {s_rem:02d}s", True, (200, 95, 75))
        self.screen.blit(bst_s, (rx0 + rw - bst_s.get_width() - 12, py + 35))

        # ── Sub-layout: preview (left) | stats+lineage (right) ──
        PREV_W  = 260
        prev_cx = rx0 + PREV_W // 2 + 8
        stats_x = rx0 + PREV_W + 28

        # Preview box
        prev_box = pygame.Rect(rx0 + 8, py + 58, PREV_W, 210)
        pygame.draw.rect(self.screen, (20, 30, 24), prev_box)
        pygame.draw.rect(self.screen, (38, 78, 52), prev_box, 1)
        self._draw_animal_preview(animal, prev_cx, py + 58 + 105, scale=3.5)

        # Harvest-resource status below preview
        res_parts = []
        if animal.animal_id == "sheep":
            res_parts = [("Wool", getattr(animal, 'has_wool', False))]
        elif animal.animal_id == "cow":
            res_parts = [("Milk", getattr(animal, 'has_milk', False))]
        elif animal.animal_id == "chicken":
            res_parts = [("Egg", getattr(animal, 'has_egg', False))]
        elif animal.animal_id == "goat":
            res_parts = [("Milk", getattr(animal, 'has_milk', False))]
        elif animal.animal_id == "horse":
            broken = getattr(animal, '_broken', False)
            res_parts = [("Broken", broken)]
        for label, ready in res_parts:
            if label == "Broken":
                col = (120, 180, 255) if ready else (200, 160, 60)
                txt = "saddle-ready" if ready else "needs breaking"
            else:
                col = (120, 220, 140) if ready else (140, 100, 80)
                txt = "ready" if ready else "regrow..."
            rs = self.small.render(f"{label}: {txt}", True, col)
            self.screen.blit(rs, (prev_box.x + prev_box.w // 2 - rs.get_width() // 2,
                                  prev_box.bottom + 5))

        # ── GENETICS ─────────────────────────────────────────────────
        sy = py + 58
        gen_lbl = self.small.render("GENETICS", True, (85, 155, 105))
        self.screen.blit(gen_lbl, (stats_x, sy))
        pygame.draw.line(self.screen, (38, 75, 52),
                         (stats_x, sy + 16), (rx0 + rw - 8, sy + 16))
        sy += 24

        traits  = animal.traits
        geno    = getattr(animal, 'genotype', {})
        BAR_W   = 80
        BAR_H   = 8
        COL_W   = 130  # width for one allele column

        def _draw_allele_quant(label, gene_key, lo, hi, bar_col, label_w=60):
            nonlocal sy
            pair = geno.get(gene_key)
            expressed = traits.get(gene_key.replace("_gene", ""), (lo + hi) / 2)
            lbl_s = self.small.render(label, True, (150, 195, 165))
            self.screen.blit(lbl_s, (stats_x, sy))
            for ai, av in enumerate(pair if pair else [expressed, expressed]):
                ax = stats_x + label_w + ai * (BAR_W + 14)
                fill = max(0, min(BAR_W, int(BAR_W * (av - lo) / (hi - lo))))
                pygame.draw.rect(self.screen, (22, 40, 30), (ax, sy + 1, BAR_W, BAR_H))
                pygame.draw.rect(self.screen, bar_col, (ax, sy + 1, fill, BAR_H))
                vl = self.small.render(f"{av:.2f}", True, (160, 205, 175))
                self.screen.blit(vl, (ax + BAR_W + 3, sy))
            exp_s = self.small.render(f"→{expressed:.2f}", True, (220, 240, 225))
            self.screen.blit(exp_s, (stats_x + label_w + 2 * (BAR_W + 14) + 4, sy))
            sy += 18

        def _draw_allele_cat(label, gene_key, label_w=60):
            nonlocal sy
            pair = geno.get(gene_key)
            expressed = traits.get(gene_key.replace("_gene", ""), "?")
            lbl_s = self.small.render(label, True, (150, 195, 165))
            self.screen.blit(lbl_s, (stats_x, sy))
            if pair:
                a_s = self.small.render(str(pair[0]), True, (180, 220, 195))
                b_s = self.small.render(str(pair[1]), True, (180, 220, 195))
                slash = self.small.render(" / ", True, (60, 90, 70))
                self.screen.blit(a_s,   (stats_x + label_w, sy))
                self.screen.blit(slash, (stats_x + label_w + a_s.get_width(), sy))
                self.screen.blit(b_s,   (stats_x + label_w + a_s.get_width() + slash.get_width(), sy))
                arr = self.small.render(f"→ {expressed}", True, (220, 240, 225))
                self.screen.blit(arr, (stats_x + label_w + 2 * COL_W // 3 + 20, sy))
            sy += 16

        if animal.animal_id == "dog":
            breed = traits.get("breed", "Unknown")
            sz    = traits.get("size_class", "medium")
            br_s  = self.small.render(f"Breed: {breed}  ({sz})", True, (195, 230, 210))
            self.screen.blit(br_s, (stats_x, sy))
            sy += 18
            coat = traits.get("coat_color", (160, 100, 50))
            coat_lbl = self.small.render("Coat", True, (150, 195, 165))
            self.screen.blit(coat_lbl, (stats_x, sy))
            pygame.draw.rect(self.screen, coat, (stats_x + 50, sy, 24, 14))
            pygame.draw.rect(self.screen, (75, 108, 88), (stats_x + 50, sy, 24, 14), 1)
            pat = traits.get("coat_pattern", "solid")
            pat_s = self.small.render(pat, True, (160, 200, 175))
            self.screen.blit(pat_s, (stats_x + 80, sy))
            sy += 18
            _draw_allele_quant("Speed",    "speed_gene",    0.7, 1.4, (65, 155, 235), label_w=75)
            _draw_allele_quant("Nose",     "nose_gene",     0.6, 1.4, (120, 200, 120), label_w=75)
            _draw_allele_quant("Agility",  "agility_gene",  0.7, 1.4, (200, 155, 65), label_w=75)
            _draw_allele_quant("Strength", "strength_gene", 0.7, 1.3, (210, 90, 90), label_w=75)
            _draw_allele_quant("Alert",    "alertness_gene",0.7, 1.4, (155, 130, 220), label_w=75)
        elif animal.animal_id == "horse":
            _draw_allele_quant("Speed",     "speed_gene",    0.7, 1.4, (65, 155, 235))
            _draw_allele_quant("Stamina",   "stamina_gene",  0.8, 1.2, (80, 210, 120))
            _draw_allele_quant("Endurance", "endurance_gene",0.7, 1.3, (100, 185, 240))
            _draw_allele_quant("Gait",      "gait_gene",     0.7, 1.3, (160, 120, 230))
            temp = traits.get("temperament", "spirited")
            temp_lbl = self.small.render("Temper", True, (150, 195, 165))
            self.screen.blit(temp_lbl, (stats_x, sy))
            temp_cols = {"calm": (80, 200, 80), "spirited": (220, 180, 40), "wild": (220, 60, 60)}
            temp_s = self.small.render(temp.capitalize(), True, temp_cols.get(temp, (180, 180, 180)))
            self.screen.blit(temp_s, (stats_x + 60, sy))
            sy += 16
            coat = traits.get("coat_color", (160, 115, 65))
            coat_lbl = self.small.render("Coat", True, (150, 195, 165))
            self.screen.blit(coat_lbl, (stats_x, sy))
            pygame.draw.rect(self.screen, coat, (stats_x + 60, sy, 24, 14))
            pygame.draw.rect(self.screen, (75, 108, 88), (stats_x + 60, sy, 24, 14), 1)
            sy += 16
            _draw_allele_cat("Pattern", "coat_pattern_gene")
            _draw_allele_cat("Legs",    "leg_marking_gene")
            _draw_allele_cat("Mane",    "mane_color_gene")
            _draw_allele_cat("Marking", "face_marking_gene")
        else:
            _draw_allele_quant("Size",  "size_gene",        0.85, 1.15, (65, 185, 95), label_w=50)
            _draw_allele_quant("Yield", "productivity_gene",0.7,  1.3,  (200, 160, 40), label_w=50)
            if animal.animal_id == "sheep":
                _draw_allele_quant("Fleece",  "fleece_gene", 0.7, 1.3, (200, 200, 255), label_w=50)
                _draw_allele_cat("Wool",  "wool_color_gene", label_w=50)
                _draw_allele_cat("Birth", "birth_gene",      label_w=50)
            elif animal.animal_id == "cow":
                _draw_allele_quant("Richness", "milk_richness_gene", 0.7, 1.3, (220, 200, 80), label_w=65)
                _draw_allele_cat("Hide", "hide_gene", label_w=65)
            elif animal.animal_id == "goat":
                _draw_allele_quant("Richness", "milk_richness_gene", 0.7, 1.3, (220, 200, 80), label_w=65)
                _draw_allele_cat("Coat", "coat_color_gene", label_w=65)
            elif animal.animal_id == "chicken":
                _draw_allele_quant("Lay Rate", "lay_rate_gene",  0.7, 1.3, (240, 200, 80), label_w=65)
                _draw_allele_cat("Plumage",  "plumage_gene", label_w=65)

            cs = traits.get("color_shift", (0, 0, 0))
            CB_W = 52
            cs_label = self.small.render("Color", True, (150, 195, 165))
            self.screen.blit(cs_label, (stats_x, sy))
            for ci, (ch_name, ch_col) in enumerate([("R", (215, 55, 55)),
                                                     ("G", (55, 195, 75)),
                                                     ("B", (55, 105, 225))]):
                cx2 = stats_x + 50 + ci * (CB_W + 4)
                v   = cs[ci]
                pygame.draw.rect(self.screen, (28, 48, 36), (cx2, sy + 1, CB_W, BAR_H))
                mid = cx2 + CB_W // 2
                fp  = int(CB_W // 2 * abs(v) / 0.25)
                if v >= 0:
                    pygame.draw.rect(self.screen, ch_col, (mid, sy + 1, fp, BAR_H))
                else:
                    pygame.draw.rect(self.screen, ch_col, (mid - fp, sy + 1, fp, BAR_H))
                cl = self.small.render(ch_name, True, ch_col)
                self.screen.blit(cl, (mid - cl.get_width() // 2, sy + BAR_H + 3))
            sy += 22

        # Mutation gene — show carrier status
        _MUT_BADGE = {
            "albino":    ((240, 240, 255), (120, 120, 200)),
            "giant":     ((80,  140,  60), (210, 255, 185)),
            "miniature": ((60,   90, 140), (185, 215, 255)),
            "golden":    ((180, 150,  20), (255, 240, 100)),
        }
        _MUT_HINT = {
            "albino":    "Tames in 2 feeds  (faster taming)",
            "giant":     "Oversized body  +1 extra drop",
            "miniature": "Tiny body  breed cooldown 60s",
            "golden":    "Drops a golden bonus resource",
        }
        mut_pair = geno.get("mutation", [None, None])
        mut      = traits.get("mutation")
        if mut is not None:
            bg_col, tx_col = _MUT_BADGE.get(mut, ((100, 100, 100), (220, 220, 220)))
            badge_s = self.small.render(f"★ {mut.upper()} MUTATION", True, tx_col)
            badge_rect = pygame.Rect(stats_x, sy, badge_s.get_width() + 16, 20)
            pygame.draw.rect(self.screen, bg_col, badge_rect, border_radius=4)
            self.screen.blit(badge_s, (stats_x + 8, sy + 3))
            sy += 24
            hint = _MUT_HINT.get(mut, "")
            if hint:
                hint_s = self.small.render(hint, True, (130, 175, 145))
                self.screen.blit(hint_s, (stats_x, sy))
                sy += 16
        else:
            # Check if carrier (one non-None allele)
            carrier_type = next((a for a in mut_pair if a is not None), None)
            if carrier_type is not None:
                car_s = self.small.render(f"◈ CARRIER: {carrier_type}", True, (220, 175, 60))
                self.screen.blit(car_s, (stats_x, sy))
                sy += 16
                hint_s = self.small.render("Hidden gene — breed two carriers for 25% expression", True, (120, 145, 110))
                self.screen.blit(hint_s, (stats_x, sy))
                sy += 16
            else:
                no_mut = self.small.render("No mutation gene", True, (55, 80, 65))
                self.screen.blit(no_mut, (stats_x, sy))
                sy += 16

        # ── NO BREED TOGGLE ───────────────────────────────────────────
        sy += 4
        nb = getattr(animal, 'no_breed', False)
        nb_col   = (110, 30, 30) if nb else (28, 52, 36)
        nb_bdr   = (200, 60, 60) if nb else (60, 140, 80)
        nb_txt   = "BREEDING: OFF" if nb else "BREEDING: ON"
        nb_tc    = (240, 100, 100) if nb else (90, 200, 115)
        nb_r = pygame.Rect(stats_x, sy, 130, 22)
        pygame.draw.rect(self.screen, nb_col, nb_r, border_radius=4)
        pygame.draw.rect(self.screen, nb_bdr, nb_r, 1, border_radius=4)
        nb_s = self.small.render(nb_txt, True, nb_tc)
        self.screen.blit(nb_s, (nb_r.centerx - nb_s.get_width() // 2, nb_r.centery - nb_s.get_height() // 2))
        if not hasattr(self, '_breed_nb_rects'):
            self._breed_nb_rects = {}
        self._breed_nb_rects[animal.uid] = nb_r
        sy += 26

        # ── LINEAGE ───────────────────────────────────────────────────
        lin_lbl = self.small.render("LINEAGE", True, (85, 155, 105))
        self.screen.blit(lin_lbl, (stats_x, sy))
        pygame.draw.line(self.screen, (38, 75, 52),
                         (stats_x, sy + 16), (rx0 + rw - 8, sy + 16))
        sy += 24

        parent_uids   = [animal.parent_a_uid, animal.parent_b_uid]
        parent_labels = ["Parent A", "Parent B"]
        has_parents   = any(p is not None for p in parent_uids)

        if not has_parents:
            wb = self.small.render("Wild-born  (no recorded parents)", True, (110, 145, 120))
            self.screen.blit(wb, (stats_x, sy))
            sy += 18
        else:
            for puid, plabel in zip(parent_uids, parent_labels):
                pl_s = self.small.render(plabel + ":", True, (95, 135, 110))
                self.screen.blit(pl_s, (stats_x, sy + 4))
                if puid is None:
                    unk = self.small.render("Unknown", True, (65, 88, 75))
                    self.screen.blit(unk, (stats_x + 80, sy + 4))
                else:
                    parent = uid_map.get(puid)
                    if parent is not None and not getattr(parent, 'dead', True):
                        self._draw_animal_preview(parent, stats_x + 88, sy + 10, scale=1.2)
                        pnum  = animal_numbers.get(puid, "?")
                        ptxt  = f"{TYPE_LABELS.get(parent.animal_id, parent.animal_id)} #{pnum}"
                        pt_s  = self.small.render(ptxt, True, (175, 218, 188))
                        self.screen.blit(pt_s, (stats_x + 112, sy + 2))
                        is_tamed = getattr(parent, 'tamed', False)
                        st_txt = "alive (tamed)" if is_tamed else "alive (wild)"
                        st_s   = self.small.render(st_txt, True, (75, 195, 100))
                        self.screen.blit(st_s, (stats_x + 112, sy + 16))
                    else:
                        gone = self.small.render(f"Deceased  ({puid[:10]}…)", True, (155, 80, 80))
                        self.screen.blit(gone, (stats_x + 80, sy + 4))
                sy += 40

        # Generation depth
        def _gen(uid, depth=0):
            if depth > 20 or uid is None:
                return depth
            e2 = uid_map.get(uid)
            if e2 is None:
                return depth
            pa, pb = getattr(e2, 'parent_a_uid', None), getattr(e2, 'parent_b_uid', None)
            if pa is None and pb is None:
                return depth
            return max(_gen(pa, depth + 1), _gen(pb, depth + 1))

        gen = _gen(animal.uid)
        gen_txt = "Wild-born" if gen == 0 else f"Gen {gen}"
        gen_s = self.small.render(f"Generation: {gen_txt}", True, (110, 150, 125))
        self.screen.blit(gen_s, (stats_x, sy))
        sy += 20

        # Children list
        children = [e for e in all_tamed
                    if getattr(e, 'parent_a_uid', None) == animal.uid
                    or getattr(e, 'parent_b_uid', None) == animal.uid]
        if children:
            ch_hdr = self.small.render(f"Children: {len(children)}", True, (85, 155, 105))
            self.screen.blit(ch_hdr, (stats_x, sy))
            sy += 16
            for ch in children[:5]:
                cnum  = animal_numbers.get(ch.uid, "?")
                ctxt  = f"  {TYPE_LABELS.get(ch.animal_id, ch.animal_id)} #{cnum}"
                ch_s  = self.small.render(ctxt, True, (140, 195, 155))
                self.screen.blit(ch_s, (stats_x, sy))
                sy += 14

    # ------------------------------------------------------------------
    # Merchant / Restaurant / Shrine panels
    # ------------------------------------------------------------------

    def _draw_merchant_content(self, player, npc, px, py, PW, PH):
        title = self.font.render("MERCHANT", True, (220, 175, 40))
        self.screen.blit(title, (px + PW // 2 - title.get_width() // 2, py + 10))
        self._draw_rep_rank(npc, px, py)

        gold_txt = self.font.render(f"Your gold: {player.money}", True, (220, 175, 40))
        self.screen.blit(gold_txt, (px + PW - gold_txt.get_width() - 20, py + 10))

        disc_pct = npc.rep_discount_pct()
        header_y = py + 32
        if disc_pct > 0:
            rep_txt = self.small.render(
                f"Town reputation bonus: -{disc_pct}% off", True, (120, 200, 120))
            self.screen.blit(rep_txt, (px + 20, header_y))

        self._trade_rects.clear()
        y = py + 56

        from cities import specialty_price_label
        for i, (item_id, _, display, barter_item, barter_qty) in enumerate(npc.shop):
            cost      = npc.discounted_cost(i)
            can_buy   = npc.can_buy(i, player)
            can_barter = npc.can_barter(i, player)

            row_h = 72
            row_rect = pygame.Rect(px + 20, y, PW - 40, row_h)

            bg  = (30, 25, 10) if (can_buy or can_barter) else (26, 26, 34)
            bdr = (200, 160, 40) if (can_buy or can_barter) else (55, 55, 70)
            pygame.draw.rect(self.screen, bg, row_rect)
            pygame.draw.rect(self.screen, bdr, row_rect, 2)

            item_color = ITEMS.get(item_id, {}).get("color", (128, 128, 128))
            pygame.draw.rect(self.screen, item_color, (px + 28, y + 20, 28, 28))

            name_col = (240, 220, 130) if (can_buy or can_barter) else (130, 120, 90)
            self.screen.blit(self.font.render(display, True, name_col), (px + 66, y + 8))

            # --- BUY row ---
            buy_col  = (220, 175, 40) if can_buy else (90, 80, 40)
            buy_lbl  = self.font.render("BUY", True, (255, 220, 80) if can_buy else (70, 70, 82))
            gold_lbl = self.font.render(f"{cost} gold", True, buy_col)
            self.screen.blit(gold_lbl, (px + 66, y + 30))
            # Specialty tag — green for region exports, amber for imports
            spec_tag = specialty_price_label(npc, item_id)
            if spec_tag:
                tag_col = (130, 200, 130) if spec_tag == "export" else (220, 170, 90)
                tag_s = self.small.render(f"({spec_tag})", True, tag_col)
                self.screen.blit(tag_s, (px + 66 + gold_lbl.get_width() + 6, y + 34))
            buy_rect = pygame.Rect(row_rect.right - 70, y + 26, 58, 20)
            buy_bg   = (80, 60, 10) if can_buy else (35, 35, 45)
            pygame.draw.rect(self.screen, buy_bg, buy_rect)
            pygame.draw.rect(self.screen, buy_col, buy_rect, 1)
            self.screen.blit(buy_lbl, (buy_rect.centerx - buy_lbl.get_width() // 2,
                                       buy_rect.centery - buy_lbl.get_height() // 2))
            self._trade_rects[(i, "buy")] = buy_rect

            # --- TRADE row ---
            barter_name = ITEMS.get(barter_item, {}).get("name", barter_item)
            trade_col   = (100, 190, 140) if can_barter else (60, 90, 75)
            trade_lbl   = self.font.render("TRADE", True, (120, 220, 160) if can_barter else (60, 80, 70))
            barter_lbl  = self.font.render(f"{barter_qty} {barter_name}", True, trade_col)
            self.screen.blit(barter_lbl, (px + 66, y + 50))
            trade_rect = pygame.Rect(row_rect.right - 70, y + 46, 58, 20)
            trade_bg   = (10, 50, 35) if can_barter else (35, 35, 45)
            pygame.draw.rect(self.screen, trade_bg, trade_rect)
            pygame.draw.rect(self.screen, trade_col, trade_rect, 1)
            self.screen.blit(trade_lbl, (trade_rect.centerx - trade_lbl.get_width() // 2,
                                         trade_rect.centery - trade_lbl.get_height() // 2))
            self._trade_rects[(i, "barter")] = trade_rect

            y += row_h + 6

    def _draw_restaurant_content(self, player, npc, px, py, PW, PH):
        title = self.font.render(npc.cuisine.upper(), True, (240, 120, 30))
        self.screen.blit(title, (px + PW // 2 - title.get_width() // 2, py + 10))
        self._draw_rep_rank(npc, px, py)

        gold_txt = self.font.render(f"Your gold: {player.money}", True, (220, 175, 40))
        self.screen.blit(gold_txt, (px + PW - gold_txt.get_width() - 20, py + 10))

        disc_pct = npc.rep_discount_pct()
        if disc_pct > 0:
            rep_txt = self.small.render(
                f"Town reputation bonus: -{disc_pct}% off", True, (120, 200, 120))
            self.screen.blit(rep_txt, (px + 20, py + 32))

        self._trade_rects.clear()
        y = py + 56

        from cities import specialty_price_label
        for i, (item_id, _) in enumerate(npc.menu):
            can = npc.can_buy(i, player)
            cost = npc.discounted_cost(i)
            item_data = ITEMS.get(item_id, {})
            item_name = item_data.get("name", item_id)
            hunger    = item_data.get("hunger_restore", 0)

            row_h = 64
            rect = pygame.Rect(px + 20, y, PW - 40, row_h)
            self._trade_rects[i] = rect

            bg  = (35, 18, 8) if can else (26, 26, 34)
            bdr = (210, 100, 30) if can else (55, 55, 70)
            pygame.draw.rect(self.screen, bg, rect)
            pygame.draw.rect(self.screen, bdr, rect, 2)

            item_color = item_data.get("color", (128, 128, 128))
            pygame.draw.rect(self.screen, item_color, (px + 28, y + 16, 30, 30))

            name_col = (245, 200, 140) if can else (130, 110, 80)
            self.screen.blit(
                self.font.render(item_name, True, name_col),
                (px + 68, y + 10))
            cost_s = self.font.render(
                f"{cost} gold  •  +{hunger} hunger", True,
                (200, 160, 80) if can else (100, 90, 60))
            self.screen.blit(cost_s, (px + 68, y + 32))
            spec_tag = specialty_price_label(npc, item_id)
            if spec_tag:
                tag_col = (130, 200, 130) if spec_tag == "export" else (220, 170, 90)
                tag_s = self.small.render(f"({spec_tag})", True, tag_col)
                self.screen.blit(tag_s, (px + 68 + cost_s.get_width() + 6, y + 36))

            lbl = self.font.render("BUY", True, (255, 175, 80) if can else (70, 70, 82))
            self.screen.blit(lbl, (rect.right - lbl.get_width() - 10,
                                   y + row_h // 2 - lbl.get_height() // 2))
            y += row_h + 8

    def _draw_blacksmith_content(self, player, npc, px, py, PW, PH):
        title = self.font.render("BLACKSMITH", True, (160, 175, 210))
        self.screen.blit(title, (px + PW // 2 - title.get_width() // 2, py + 10))
        self._draw_rep_rank(npc, px, py)

        gold_txt = self.font.render(f"Your gold: {player.money}", True, (220, 175, 40))
        self.screen.blit(gold_txt, (px + PW - gold_txt.get_width() - 20, py + 10))

        disc_pct = npc.rep_discount_pct()
        if disc_pct > 0:
            rep_txt = self.small.render(
                f"Town reputation bonus: -{disc_pct}% off", True, (120, 200, 120))
            self.screen.blit(rep_txt, (px + 20, py + 32))

        self._trade_rects.clear()
        y = py + 56

        from cities import specialty_price_label
        for i, (item_id, _, display, barter_item, barter_qty) in enumerate(npc.shop):
            cost       = npc.discounted_cost(i)
            can_buy    = npc.can_buy(i, player)
            can_barter = npc.can_barter(i, player)

            row_h    = 72
            row_rect = pygame.Rect(px + 20, y, PW - 40, row_h)
            bg  = (20, 22, 30) if (can_buy or can_barter) else (22, 22, 30)
            bdr = (120, 135, 165) if (can_buy or can_barter) else (50, 55, 70)
            pygame.draw.rect(self.screen, bg, row_rect)
            pygame.draw.rect(self.screen, bdr, row_rect, 2)

            item_color = ITEMS.get(item_id, {}).get("color", (128, 128, 128))
            pygame.draw.rect(self.screen, item_color, (px + 28, y + 20, 28, 28))

            name_col = (210, 220, 240) if (can_buy or can_barter) else (110, 115, 130)
            self.screen.blit(self.font.render(display, True, name_col), (px + 66, y + 8))

            buy_col = (180, 155, 60) if can_buy else (80, 75, 40)
            buy_lbl = self.font.render("BUY", True, (220, 195, 80) if can_buy else (70, 70, 82))
            gold_lbl = self.font.render(f"{cost} gold", True, buy_col)
            self.screen.blit(gold_lbl, (px + 66, y + 30))
            spec_tag = specialty_price_label(npc, item_id)
            if spec_tag:
                tag_col = (130, 200, 130) if spec_tag == "export" else (220, 170, 90)
                tag_s = self.small.render(f"({spec_tag})", True, tag_col)
                self.screen.blit(tag_s, (px + 66 + gold_lbl.get_width() + 6, y + 34))
            buy_rect = pygame.Rect(row_rect.right - 70, y + 26, 58, 20)
            buy_bg   = (50, 50, 30) if can_buy else (35, 35, 45)
            pygame.draw.rect(self.screen, buy_bg, buy_rect)
            pygame.draw.rect(self.screen, buy_col, buy_rect, 1)
            self.screen.blit(buy_lbl, (buy_rect.centerx - buy_lbl.get_width() // 2,
                                       buy_rect.centery - buy_lbl.get_height() // 2))
            self._trade_rects[(i, "buy")] = buy_rect

            barter_name = ITEMS.get(barter_item, {}).get("name", barter_item)
            trade_col   = (100, 190, 140) if can_barter else (55, 85, 70)
            trade_lbl   = self.font.render("TRADE", True, (120, 220, 160) if can_barter else (60, 80, 70))
            barter_lbl  = self.font.render(f"{barter_qty} {barter_name}", True, trade_col)
            self.screen.blit(barter_lbl, (px + 66, y + 50))
            trade_rect = pygame.Rect(row_rect.right - 70, y + 46, 58, 20)
            trade_bg   = (10, 50, 35) if can_barter else (35, 35, 45)
            pygame.draw.rect(self.screen, trade_bg, trade_rect)
            pygame.draw.rect(self.screen, trade_col, trade_rect, 1)
            self.screen.blit(trade_lbl, (trade_rect.centerx - trade_lbl.get_width() // 2,
                                         trade_rect.centery - trade_lbl.get_height() // 2))
            self._trade_rects[(i, "barter")] = trade_rect

            y += row_h + 6

    def _draw_innkeeper_content(self, player, npc, px, py, PW, PH):
        title = self.font.render("THE INN", True, (240, 175, 80))
        self.screen.blit(title, (px + PW // 2 - title.get_width() // 2, py + 10))
        self._draw_rep_rank(npc, px, py)

        gold_txt = self.font.render(f"Your gold: {player.money}", True, (220, 175, 40))
        self.screen.blit(gold_txt, (px + PW - gold_txt.get_width() - 20, py + 10))

        disc_pct = npc.rep_discount_pct()
        if disc_pct > 0:
            rep_txt = self.small.render(
                f"Town reputation bonus: -{disc_pct}% off", True, (120, 200, 120))
            self.screen.blit(rep_txt, (px + 20, py + 32))

        rest_cost = npc.discounted_cost()
        can_rest  = npc.can_rest(player)
        rest_rect = pygame.Rect(px + 20, py + 52, PW - 40, 48)
        rest_bg   = (25, 18, 8) if can_rest else (22, 22, 28)
        rest_bdr  = (180, 130, 55) if can_rest else (55, 55, 70)
        pygame.draw.rect(self.screen, rest_bg, rest_rect)
        pygame.draw.rect(self.screen, rest_bdr, rest_rect, 2)
        rest_lbl = self.font.render(
            f"Rest for the night  —  {rest_cost} gold  (+15% luck, 4 min)", True,
            (240, 195, 100) if can_rest else (100, 90, 65))
        self.screen.blit(rest_lbl, (px + 30, py + 64))
        self._trade_rects.clear()
        self._trade_rects["rest"] = rest_rect

        sep_y = py + 112
        sep_lbl = self.small.render("FOOD & DRINK", True, (140, 120, 80))
        self.screen.blit(sep_lbl, (px + 20, sep_y))
        pygame.draw.line(self.screen, (80, 65, 40), (px + 20, sep_y + 16), (px + PW - 20, sep_y + 16))

        y = sep_y + 24
        from cities import specialty_price_label
        for i, (item_id, _) in enumerate(npc.menu):
            can  = npc.can_buy(i, player)
            cost = npc.discounted_cost(i)
            item_data = ITEMS.get(item_id, {})
            item_name = item_data.get("name", item_id)
            hunger    = item_data.get("hunger_restore", 0)

            row_h = 56
            rect  = pygame.Rect(px + 20, y, PW - 40, row_h)
            self._trade_rects[i] = rect

            bg  = (35, 20, 8) if can else (26, 26, 34)
            bdr = (200, 130, 55) if can else (55, 55, 70)
            pygame.draw.rect(self.screen, bg, rect)
            pygame.draw.rect(self.screen, bdr, rect, 2)

            item_color = item_data.get("color", (128, 128, 128))
            pygame.draw.rect(self.screen, item_color, (px + 28, y + 12, 28, 28))

            name_col = (245, 210, 150) if can else (130, 110, 80)
            self.screen.blit(self.font.render(item_name, True, name_col), (px + 68, y + 8))
            cost_s = self.font.render(
                f"{cost} gold  •  +{hunger} hunger", True,
                (200, 155, 75) if can else (100, 90, 60))
            self.screen.blit(cost_s, (px + 68, y + 28))
            spec_tag = specialty_price_label(npc, item_id)
            if spec_tag:
                tag_col = (130, 200, 130) if spec_tag == "export" else (220, 170, 90)
                tag_s = self.small.render(f"({spec_tag})", True, tag_col)
                self.screen.blit(tag_s, (px + 68 + cost_s.get_width() + 6, y + 32))

            buy_lbl = self.font.render("BUY", True, (255, 185, 90) if can else (70, 70, 82))
            self.screen.blit(buy_lbl, (rect.right - buy_lbl.get_width() - 10,
                                       y + row_h // 2 - buy_lbl.get_height() // 2))
            y += row_h + 6

    def _draw_scholar_content(self, player, npc, px, py, PW, PH):
        title = self.font.render("SCHOLAR", True, (140, 185, 230))
        self.screen.blit(title, (px + PW // 2 - title.get_width() // 2, py + 10))
        self._draw_rep_rank(npc, px, py)

        gold_txt = self.font.render(f"Your gold: {player.money}", True, (220, 175, 40))
        self.screen.blit(gold_txt, (px + PW - gold_txt.get_width() - 20, py + 10))

        disc_pct = npc.rep_discount_pct()
        if disc_pct > 0:
            rep_txt = self.small.render(
                f"Town reputation bonus: -{disc_pct}% off", True, (120, 200, 120))
            self.screen.blit(rep_txt, (px + 20, py + 32))

        self._trade_rects.clear()
        y = py + 56

        from cities import specialty_price_label
        for i, (item_id, _, display, barter_item, barter_qty) in enumerate(npc.shop):
            cost       = npc.discounted_cost(i)
            can_buy    = npc.can_buy(i, player)
            can_barter = npc.can_barter(i, player)

            row_h    = 72
            row_rect = pygame.Rect(px + 20, y, PW - 40, row_h)
            bg  = (18, 22, 32) if (can_buy or can_barter) else (22, 22, 30)
            bdr = (110, 150, 200) if (can_buy or can_barter) else (50, 55, 70)
            pygame.draw.rect(self.screen, bg, row_rect)
            pygame.draw.rect(self.screen, bdr, row_rect, 2)

            item_color = ITEMS.get(item_id, {}).get("color", (128, 128, 128))
            pygame.draw.rect(self.screen, item_color, (px + 28, y + 20, 28, 28))

            name_col = (200, 220, 245) if (can_buy or can_barter) else (100, 110, 130)
            self.screen.blit(self.font.render(display, True, name_col), (px + 66, y + 8))

            buy_col = (180, 155, 60) if can_buy else (80, 75, 40)
            buy_lbl = self.font.render("BUY", True, (220, 195, 80) if can_buy else (70, 70, 82))
            gold_lbl = self.font.render(f"{cost} gold", True, buy_col)
            self.screen.blit(gold_lbl, (px + 66, y + 30))
            spec_tag = specialty_price_label(npc, item_id)
            if spec_tag:
                tag_col = (130, 200, 130) if spec_tag == "export" else (220, 170, 90)
                tag_s = self.small.render(f"({spec_tag})", True, tag_col)
                self.screen.blit(tag_s, (px + 66 + gold_lbl.get_width() + 6, y + 34))
            buy_rect = pygame.Rect(row_rect.right - 70, y + 26, 58, 20)
            buy_bg   = (30, 35, 55) if can_buy else (35, 35, 45)
            pygame.draw.rect(self.screen, buy_bg, buy_rect)
            pygame.draw.rect(self.screen, buy_col, buy_rect, 1)
            self.screen.blit(buy_lbl, (buy_rect.centerx - buy_lbl.get_width() // 2,
                                       buy_rect.centery - buy_lbl.get_height() // 2))
            self._trade_rects[(i, "buy")] = buy_rect

            barter_name = ITEMS.get(barter_item, {}).get("name", barter_item)
            trade_col   = (100, 190, 140) if can_barter else (55, 85, 70)
            trade_lbl   = self.font.render("TRADE", True, (120, 220, 160) if can_barter else (60, 80, 70))
            barter_lbl  = self.font.render(f"{barter_qty} {barter_name}", True, trade_col)
            self.screen.blit(barter_lbl, (px + 66, y + 50))
            trade_rect = pygame.Rect(row_rect.right - 70, y + 46, 58, 20)
            trade_bg   = (10, 50, 35) if can_barter else (35, 35, 45)
            pygame.draw.rect(self.screen, trade_bg, trade_rect)
            pygame.draw.rect(self.screen, trade_col, trade_rect, 1)
            self.screen.blit(trade_lbl, (trade_rect.centerx - trade_lbl.get_width() // 2,
                                         trade_rect.centery - trade_lbl.get_height() // 2))
            self._trade_rects[(i, "barter")] = trade_rect

            y += row_h + 6

    def _draw_outpost_keeper_content(self, player, npc, px, py, PW, PH):
        from outposts import OUTPOSTS
        op = OUTPOSTS.get(npc.outpost_id)

        # ── Header ────────────────────────────────────────────────────────────
        title = self.font.render(npc.display_name.upper(), True, (110, 200, 120))
        self.screen.blit(title, (px + PW // 2 - title.get_width() // 2, py + 10))

        gold_txt = self.font.render(f"Your gold: {player.money}", True, (220, 175, 40))
        self.screen.blit(gold_txt, (px + PW - gold_txt.get_width() - 20, py + 10))

        if op:
            name_s = self.small.render(op.name, True, (160, 180, 155))
            self.screen.blit(name_s, (px + 14, py + 10))

        status_col = (120, 200, 120) if npc.needs_met() else (210, 160, 60)
        status_txt = npc.needs_status_lines()[0]
        self.screen.blit(self.small.render(status_txt, True, status_col), (px + 14, py + 28))

        content_y = py + 50
        self._trade_rects.clear()

        # ── Two-column layout: BUY (left) | SELL (right) ──────────────────────
        col_w   = (PW - 42) // 2   # ~309px each
        left_x  = px + 14
        right_x = px + 14 + col_w + 14

        # Column headers
        self.screen.blit(
            self.small.render("BUY FROM KEEPER", True, (90, 145, 100)),
            (left_x, content_y))
        self.screen.blit(
            self.small.render("SELL TO KEEPER", True, (145, 100, 165)),
            (right_x, content_y))

        row_start = content_y + 16
        row_h     = 46

        # BUY column
        y_left = row_start
        for i, (item_id, _) in enumerate(npc.sells):
            cost       = npc.sell_cost(i)
            stocked    = npc.in_stock(i)
            can_buy    = npc.can_afford(i, player) and stocked
            item_data  = ITEMS.get(item_id, {})
            item_name  = item_data.get("name", item_id)
            item_color = item_data.get("color", (128, 128, 128))

            rr = pygame.Rect(left_x, y_left, col_w, row_h)
            bg  = (18, 32, 22) if can_buy else (26, 26, 34)
            bdr = (80, 165, 100) if can_buy else ((80, 55, 55) if not stocked else (45, 55, 48))
            pygame.draw.rect(self.screen, bg, rr)
            pygame.draw.rect(self.screen, bdr, rr, 1)

            pygame.draw.rect(self.screen, item_color, (left_x + 4, y_left + 11, 20, 20))
            nc = (200, 235, 200) if can_buy else (100, 110, 100)
            self.screen.blit(self.small.render(item_name, True, nc), (left_x + 28, y_left + 6))

            if stocked:
                sub = f"{cost}g  •  {npc.stock_line(i)}"
                sc  = (180, 155, 50) if can_buy else (75, 70, 35)
                self.screen.blit(self.small.render(sub, True, sc), (left_x + 28, y_left + 24))
                btn = pygame.Rect(rr.right - 42, y_left + 12, 38, 20)
                pygame.draw.rect(self.screen, (30, 60, 35) if can_buy else (35, 35, 45), btn)
                pygame.draw.rect(self.screen, bdr, btn, 1)
                bl = self.small.render("BUY", True, (130, 230, 145) if can_buy else (55, 65, 58))
                self.screen.blit(bl, (btn.centerx - bl.get_width() // 2,
                                      btn.centery - bl.get_height() // 2))
                self._trade_rects[(i, "buy")] = btn
            else:
                self.screen.blit(
                    self.small.render("Out of stock", True, (130, 70, 70)),
                    (left_x + 28, y_left + 24))

            y_left += row_h + 3

        # SELL column
        y_right = row_start
        for j, (item_id, _, max_qty) in enumerate(npc.buys):
            pay       = npc.buy_pay(j)
            have      = player.inventory.get(item_id, 0)
            can_sell  = have >= 1
            item_data  = ITEMS.get(item_id, {})
            item_name  = item_data.get("name", item_id)
            item_color = item_data.get("color", (128, 128, 128))

            rr = pygame.Rect(right_x, y_right, col_w, row_h)
            bg  = (22, 18, 30) if can_sell else (26, 26, 34)
            bdr = (140, 90, 165) if can_sell else (50, 45, 58)
            pygame.draw.rect(self.screen, bg, rr)
            pygame.draw.rect(self.screen, bdr, rr, 1)

            pygame.draw.rect(self.screen, item_color, (right_x + 4, y_right + 11, 20, 20))
            nc = (215, 185, 235) if can_sell else (95, 85, 105)
            self.screen.blit(self.small.render(item_name, True, nc), (right_x + 28, y_right + 6))
            sub = f"Have {have}  •  {pay}g ea"
            sc  = (155, 120, 175) if can_sell else (65, 60, 75)
            self.screen.blit(self.small.render(sub, True, sc), (right_x + 28, y_right + 24))

            btn = pygame.Rect(rr.right - 52, y_right + 12, 48, 20)
            pygame.draw.rect(self.screen, (38, 22, 50) if can_sell else (35, 35, 45), btn)
            pygame.draw.rect(self.screen, bdr, btn, 1)
            bl = self.small.render("SELL", True, (200, 130, 230) if can_sell else (60, 55, 70))
            self.screen.blit(bl, (btn.centerx - bl.get_width() // 2,
                                  btn.centery - bl.get_height() // 2))
            self._trade_rects[(j, "sell")] = btn

            y_right += row_h + 3

        # ── SUPPLY section (full-width, below both columns) ───────────────────
        supply_y = max(y_left, y_right) + 6
        supply_items = npc.supply_items()
        if supply_items:
            pygame.draw.line(self.screen, (65, 60, 35),
                             (px + 14, supply_y), (px + PW - 14, supply_y), 1)
            supply_y += 8
            self.screen.blit(
                self.small.render("SUPPLY OUTPOST", True, (185, 165, 70)),
                (px + 14, supply_y))
            supply_y += 16

            for k, (item_id, still_needed, pay_per) in enumerate(supply_items):
                have      = player.inventory.get(item_id, 0)
                can_give  = have >= 1
                item_data  = ITEMS.get(item_id, {})
                item_name  = item_data.get("name", item_id)
                item_color = item_data.get("color", (128, 128, 128))

                rr  = pygame.Rect(px + 14, supply_y, PW - 28, 40)
                bg  = (28, 24, 10) if can_give else (26, 26, 34)
                bdr = (190, 168, 55) if can_give else (55, 52, 38)
                pygame.draw.rect(self.screen, bg, rr)
                pygame.draw.rect(self.screen, bdr, rr, 1)

                pygame.draw.rect(self.screen, item_color, (px + 22, supply_y + 9, 18, 18))
                nc = (235, 220, 140) if can_give else (105, 100, 65)
                self.screen.blit(self.small.render(item_name, True, nc), (px + 46, supply_y + 5))
                sub = f"Need {still_needed}  •  have {have}  •  {pay_per}g each"
                sc  = (180, 160, 65) if can_give else (75, 72, 40)
                self.screen.blit(self.small.render(sub, True, sc), (px + 46, supply_y + 22))

                btn = pygame.Rect(rr.right - 72, supply_y + 8, 62, 22)
                pygame.draw.rect(self.screen, (40, 35, 10) if can_give else (35, 35, 45), btn)
                pygame.draw.rect(self.screen, bdr, btn, 1)
                bl = self.small.render("DELIVER", True, (240, 220, 80) if can_give else (68, 65, 40))
                self.screen.blit(bl, (btn.centerx - bl.get_width() // 2,
                                      btn.centery - bl.get_height() // 2))
                self._trade_rects[(k, "supply")] = (btn, item_id)

                supply_y += 43

    def _draw_shrine_content(self, player, npc, px, py, PW, PH):
        title = self.font.render(npc.religion_name.upper(), True, (230, 210, 110))
        self.screen.blit(title, (px + PW // 2 - title.get_width() // 2, py + 10))
        self._draw_rep_rank(npc, px, py)

        gold_txt = self.font.render(f"Your gold: {player.money}", True, (220, 175, 40))
        self.screen.blit(gold_txt, (px + PW - gold_txt.get_width() - 20, py + 10))

        disc_pct = npc.rep_discount_pct()
        duration = int(npc._blessing_duration())
        if disc_pct > 0:
            rep_txt = self.small.render(
                f"Town rep: -{disc_pct}% cost, {duration}s blessing", True, (120, 200, 120))
            self.screen.blit(rep_txt, (px + 20, py + 32))

        # Flavor text
        fy = py + 56
        for line in npc.flavor.split("\n"):
            flavor_s = self.font.render(line, True, (170, 160, 130))
            self.screen.blit(flavor_s, (px + PW // 2 - flavor_s.get_width() // 2, fy))
            fy += 28

        # Blessing status
        blessed = getattr(player, "blessing_timer", 0) > 0
        if blessed:
            secs_left = int(player.blessing_timer)
            status_txt = self.font.render(
                f"Blessed  ({secs_left}s remaining)", True, (120, 220, 140))
            self.screen.blit(status_txt,
                             (px + PW // 2 - status_txt.get_width() // 2, fy + 10))

        # Blessing button
        self._trade_rects.clear()
        can = npc.can_bless(player)
        cost = npc.discounted_cost()
        btn_w, btn_h = 340, 52
        btn_rect = pygame.Rect(px + PW // 2 - btn_w // 2, py + PH - 80, btn_w, btn_h)
        self._trade_rects[0] = btn_rect

        bg  = (40, 35, 10) if can and not blessed else (26, 26, 34)
        bdr = (210, 180, 50) if can and not blessed else (55, 55, 70)
        pygame.draw.rect(self.screen, bg, btn_rect)
        pygame.draw.rect(self.screen, bdr, btn_rect, 2)

        if blessed:
            btn_label = "Already Blessed"
            btn_col   = (140, 130, 80)
        elif can:
            btn_label = f"Receive Blessing  —  {cost} gold  ({duration}s)"
            btn_col   = (255, 230, 80)
        else:
            btn_label = f"Receive Blessing  —  {cost} gold  (need more gold)"
            btn_col   = (90, 80, 50)

        lbl = self.font.render(btn_label, True, btn_col)
        self.screen.blit(lbl, (btn_rect.centerx - lbl.get_width() // 2,
                                btn_rect.centery - lbl.get_height() // 2))

    def _draw_trade_block_panel(self, player):
        from towns import TOWNS
        from town_needs import ITEM_TO_CATEGORY
        from horses import Horse

        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        self.screen.blit(overlay, (0, 0))

        PW, PH = 900, 560
        px = (SCREEN_W - PW) // 2
        py = (SCREEN_H - PH) // 2
        pygame.draw.rect(self.screen, (22, 18, 12), (px, py, PW, PH))
        pygame.draw.rect(self.screen, (140, 95, 45), (px, py, PW, PH), 2)

        title = self.font.render("Trade Post", True, (220, 190, 100))
        self.screen.blit(title, (px + PW // 2 - title.get_width() // 2, py + 10))

        hint = self.small.render("E / ESC: close  |  Left-click goods: move to inventory (when idle)", True, (110, 90, 60))
        self.screen.blit(hint, (px + PW // 2 - hint.get_width() // 2, py + 34))

        pos = self.active_trade_pos
        state = player.world.trade_block_data.get(pos)
        if state is None:
            return

        tamed_horses = [e for e in player.world.entities if isinstance(e, Horse) and e.tamed and not e.dead]
        town_list = sorted(TOWNS.values(), key=lambda t: t.town_id)

        config_y = py + 58
        row_h = 34

        # --- Row 1: Horse ---
        lbl = self.small.render("Horse:", True, (190, 175, 140))
        self.screen.blit(lbl, (px + 20, config_y + 8))
        if tamed_horses:
            idx = min(self._trade_horse_idx, len(tamed_horses) - 1)
            h = tamed_horses[idx]
            temp = h.traits.get("temperament", "?")
            sr = h.traits.get("speed_rating", 1.0)
            selected = state.get("horse_uid") == h.uid
            label = f"[◄] {temp.title()} {idx + 1}/{len(tamed_horses)} (spd {sr:.2f}) [►]"
            col = (120, 220, 120) if selected else (200, 190, 160)
        else:
            label = "No tamed horses"
            col = (120, 80, 60)
        btn_r = pygame.Rect(px + 100, config_y + 2, 340, 28)
        self._trade_horse_btn = btn_r
        pygame.draw.rect(self.screen, (38, 28, 18), btn_r)
        pygame.draw.rect(self.screen, (90, 70, 40), btn_r, 1)
        s = self.small.render(label, True, col)
        self.screen.blit(s, (btn_r.x + 6, btn_r.y + 6))

        # Assign horse button
        assign_r = pygame.Rect(px + 450, config_y + 2, 110, 28)
        assigned = state.get("horse_uid") is not None and tamed_horses and any(e.uid == state["horse_uid"] for e in tamed_horses)
        a_col = (60, 120, 60) if assigned else (50, 90, 50)
        pygame.draw.rect(self.screen, a_col, assign_r)
        pygame.draw.rect(self.screen, (80, 140, 80), assign_r, 1)
        a_lbl = self.small.render("Assigned ✓" if assigned else "Assign Horse", True, (180, 240, 180) if assigned else (140, 200, 140))
        self.screen.blit(a_lbl, (assign_r.x + 6, assign_r.y + 6))
        self._trade_horse_btn = (btn_r, assign_r)

        # --- Row 2: Cart ---
        config_y += row_h
        lbl = self.small.render("Cart:", True, (190, 175, 140))
        self.screen.blit(lbl, (px + 20, config_y + 8))
        cart_r = pygame.Rect(px + 100, config_y + 2, 200, 28)
        has_c = state.get("has_cart", False)
        pygame.draw.rect(self.screen, (38, 28, 18), cart_r)
        pygame.draw.rect(self.screen, (90, 70, 40), cart_r, 1)
        cart_col = (120, 220, 120) if has_c else (200, 190, 160)
        cart_lbl = "Assigned ✓" if has_c else "Assign (uses 1 cart)"
        self.screen.blit(self.small.render(cart_lbl, True, cart_col), (cart_r.x + 6, cart_r.y + 6))
        self._trade_cart_btn = cart_r

        # --- Row 3: City ---
        config_y += row_h
        lbl = self.small.render("City:", True, (190, 175, 140))
        self.screen.blit(lbl, (px + 20, config_y + 8))
        if town_list:
            tidx = min(self._trade_city_idx, len(town_list) - 1)
            town = town_list[tidx]
            linked = state.get("linked_town_id") == town.town_id
            city_label = f"[◄] {town.name}  ({tidx + 1}/{len(town_list)}) [►]"
            c_col = (120, 220, 120) if linked else (200, 190, 160)
        else:
            city_label = "No towns discovered"
            c_col = (120, 80, 60)
        city_r = pygame.Rect(px + 100, config_y + 2, 340, 28)
        pygame.draw.rect(self.screen, (38, 28, 18), city_r)
        pygame.draw.rect(self.screen, (90, 70, 40), city_r, 1)
        self.screen.blit(self.small.render(city_label, True, c_col), (city_r.x + 6, city_r.y + 6))

        link_r = pygame.Rect(px + 450, config_y + 2, 110, 28)
        linked_any = state.get("linked_town_id") is not None
        l_col = (60, 120, 60) if linked_any else (50, 90, 50)
        pygame.draw.rect(self.screen, l_col, link_r)
        pygame.draw.rect(self.screen, (80, 140, 80), link_r, 1)
        l_lbl = self.small.render("Linked ✓" if linked_any else "Link City", True, (180, 240, 180) if linked_any else (140, 200, 140))
        self.screen.blit(l_lbl, (link_r.x + 6, link_r.y + 6))
        self._trade_city_btn = (city_r, link_r)

        # --- Row 4: Threshold ---
        config_y += row_h
        lbl = self.small.render("Threshold:", True, (190, 175, 140))
        self.screen.blit(lbl, (px + 20, config_y + 8))
        thr = state.get("threshold", 10)
        minus_r = pygame.Rect(px + 130, config_y + 4, 24, 24)
        plus_r  = pygame.Rect(px + 220, config_y + 4, 24, 24)
        pygame.draw.rect(self.screen, (60, 40, 25), minus_r)
        pygame.draw.rect(self.screen, (100, 75, 45), minus_r, 1)
        pygame.draw.rect(self.screen, (60, 40, 25), plus_r)
        pygame.draw.rect(self.screen, (100, 75, 45), plus_r, 1)
        self.screen.blit(self.small.render("-", True, (200, 180, 140)), (minus_r.x + 7, minus_r.y + 5))
        self.screen.blit(self.small.render("+", True, (200, 180, 140)), (plus_r.x + 6, plus_r.y + 5))
        self.screen.blit(self.small.render(str(thr), True, (230, 210, 160)), (px + 160, config_y + 8))
        self.screen.blit(self.small.render("items min. to dispatch", True, (140, 125, 100)), (px + 250, config_y + 8))
        self._trade_thresh_minus = minus_r
        self._trade_thresh_plus  = plus_r

        # --- Status row ---
        config_y += row_h
        st = state.get("state", "idle")
        linked_town = TOWNS.get(state.get("linked_town_id"))
        town_name = linked_town.name if linked_town else "?"
        from horses import Horse as _Horse
        from constants import BLOCK_SIZE as _BS
        active_horse = next(
            (e for e in player.world.entities if isinstance(e, _Horse) and e.uid == state.get("horse_uid") and not e.dead),
            None,
        )
        horse_stuck = active_horse is not None and getattr(active_horse, '_trade_stuck', False)
        if st == "idle":
            total = sum(state.get("inventory", {}).values())
            status_text = f"Idle — {total}/{state.get('threshold', 10)} items stored"
            st_col = (140, 200, 140)
        elif st == "traveling":
            if active_horse is not None and linked_town is not None:
                blocks_left = max(0, abs((active_horse.x + active_horse.W / 2) - linked_town.center_bx * _BS) // _BS)
                status_text = f"Traveling to {town_name}… (~{blocks_left:.0f} blocks away)"
            else:
                status_text = f"Traveling to {town_name}…"
            st_col = (255, 160, 0) if horse_stuck else (200, 200, 80)
        else:
            if active_horse is not None:
                blocks_left = max(0, abs((active_horse.x + active_horse.W / 2) - pos[0] * _BS) // _BS)
                status_text = f"Returning home… (~{blocks_left:.0f} blocks away)"
            else:
                status_text = "Returning home…"
            st_col = (255, 160, 0) if horse_stuck else (200, 160, 80)
        self.screen.blit(self.small.render(status_text, True, st_col), (px + 20, config_y + 8))
        if horse_stuck:
            warn_s = self.small.render("⚠ Horse is stuck!", True, (255, 160, 0))
            self.screen.blit(warn_s, (px + 20, config_y + 22))

        # --- Dispatch button ---
        dispatch_r = pygame.Rect(px + PW - 150, config_y, 130, 28)
        ready = (state.get("has_cart") and state.get("horse_uid") and state.get("linked_town_id") is not None
                 and sum(state.get("inventory", {}).values()) > 0 and st == "idle")
        d_bg = (80, 50, 20) if ready else (40, 35, 25)
        d_fg = (250, 220, 80) if ready else (80, 70, 50)
        pygame.draw.rect(self.screen, d_bg, dispatch_r)
        pygame.draw.rect(self.screen, (120, 90, 40) if ready else (60, 55, 45), dispatch_r, 1)
        d_lbl = self.small.render("Dispatch ▶", True, d_fg)
        self.screen.blit(d_lbl, (dispatch_r.centerx - d_lbl.get_width() // 2, dispatch_r.centery - d_lbl.get_height() // 2))
        self._trade_dispatch_btn = dispatch_r if ready else None

        # --- Goods grid (stored inventory) ---
        pygame.draw.line(self.screen, (60, 45, 28), (px + 10, config_y + 36), (px + PW - 10, config_y + 36), 1)
        goods_y = config_y + 44
        goods_title = self.small.render(f"Stored Goods ({sum(state.get('inventory', {}).values())}/20 stacks)", True, (190, 175, 140))
        self.screen.blit(goods_title, (px + 20, goods_y))
        goods_y += 20

        COLS, CW, CH, GAP = 6, 130, 50, 5
        self._trade_goods_rects.clear()
        idle = st == "idle"
        inv = state.get("inventory", {})
        for idx, (item_id, count) in enumerate(sorted(inv.items())):
            col = idx % COLS
            row = idx // COLS
            rx = px + 20 + col * (CW + GAP)
            ry = goods_y + row * (CH + GAP)
            rect = pygame.Rect(rx, ry, CW, CH)
            self._trade_goods_rects[item_id] = rect
            bg_col = (38, 28, 16) if idle else (25, 20, 12)
            pygame.draw.rect(self.screen, bg_col, rect)
            pygame.draw.rect(self.screen, (90, 68, 35), rect, 1)
            item = ITEMS.get(item_id, {})
            icon = render_item_icon(item_id, item.get("color", (128, 128, 128)), 32)
            self.screen.blit(icon, (rx + 4, ry + (CH - 32) // 2))
            self.screen.blit(self.small.render(item.get("name", item_id), True, (215, 195, 165)), (rx + 40, ry + 8))
            self.screen.blit(self.small.render(f"x{count}", True, (150, 210, 150)), (rx + 40, ry + 26))

        # --- Player inventory (right side: items that can be stored) ---
        player_x_start = px + 20 + COLS * (CW + GAP) + 15
        pygame.draw.line(self.screen, (60, 45, 28), (player_x_start - 8, goods_y - 20), (player_x_start - 8, py + PH - 10), 1)
        p_title = self.small.render("Your Items", True, (190, 175, 140))
        self.screen.blit(p_title, (player_x_start, goods_y - 20))

        self._trade_player_rects.clear()
        from town_needs import ITEM_TO_CATEGORY
        tradeable = [(iid, cnt) for iid, cnt in player.inventory.items()
                     if cnt > 0 and ITEM_TO_CATEGORY.get(iid) is not None]
        PCOLS, PCW, PCH, PGAP = 2, 130, 50, 5
        for idx, (item_id, count) in enumerate(sorted(tradeable)):
            col = idx % PCOLS
            row = idx // PCOLS
            rx = player_x_start + col * (PCW + PGAP)
            ry = goods_y + row * (PCH + PGAP)
            if ry + PCH > py + PH - 10:
                break
            rect = pygame.Rect(rx, ry, PCW, PCH)
            self._trade_player_rects[item_id] = rect
            item = ITEMS.get(item_id, {})
            pygame.draw.rect(self.screen, (28, 38, 18), rect)
            pygame.draw.rect(self.screen, (65, 90, 40), rect, 1)
            icon = render_item_icon(item_id, item.get("color", (128, 128, 128)), 32)
            self.screen.blit(icon, (rx + 4, ry + (PCH - 32) // 2))
            self.screen.blit(self.small.render(item.get("name", item_id), True, (215, 195, 165)), (rx + 40, ry + 8))
            self.screen.blit(self.small.render(f"x{count}", True, (150, 210, 150)), (rx + 40, ry + 26))
