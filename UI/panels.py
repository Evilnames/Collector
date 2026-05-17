import pygame
from items import ITEMS
from item_icons import render_item_icon
from rocks import (render_rock, RARITY_COLORS, ROCK_TYPE_ORDER, ROCK_TYPE_DESCRIPTIONS,
                   ROCK_TYPES, get_refinery_equipment)
from constants import SCREEN_W, SCREEN_H, HOTBAR_SIZE, MAX_HEALTH
from automations import AUTOMATION_ITEM
from ._data import RARITY_LABEL, SPECIAL_DESCS
from Render.dogs import draw_dog
from cities import GuardNPC
from guard_sketches import sketch_from_npc


def _is_coin_npc(npc, suffix: str) -> bool:
    """Tag-based check that avoids importing coin_npcs at module load time."""
    return type(npc).__name__ == f"{suffix}NPC" or type(npc).__name__.endswith(suffix + "NPC")


_SEED_IDS = {"cactus_spine", "prickly_pear_pad", "cholla_segment"}
_TOOL_PROPS = {"pick_power", "axe_power", "till_tool", "water_tool",
               "harvest_tool", "fertilize_tool", "fishing_tool",
               "weapon_part", "wire_layer", "pipe_layer"}


def _inv_tab_match(item_id, item, tab):
    if tab == 0:
        return True
    is_seed = item_id.endswith("_seed") or "sapling" in item_id or item_id in _SEED_IDS
    is_tool = any(item.get(k) for k in _TOOL_PROPS) or (
              item.get("max_uses") and not item.get("edible"))
    is_food = item.get("edible") and not is_seed
    return (tab == 1 and is_seed) or (tab == 2 and is_food) or (tab == 3 and is_tool)


def _item_matches_system(item, system_id: str) -> bool:
    """Return True if item belongs to the given preference system."""
    try:
        if system_id == "fish":
            from fish import Fish; return isinstance(item, Fish)
        if system_id == "fossil":
            from fossils import Fossil; return isinstance(item, Fossil)
        if system_id == "rock":
            from rocks import Rock; return isinstance(item, Rock)
        if system_id == "gem":
            from gemstones import Gemstone; return isinstance(item, Gemstone)
        if system_id == "wildflower":
            from wildflowers import Wildflower; return isinstance(item, Wildflower)
        if system_id == "wine":
            from wine import Grape; return isinstance(item, Grape)
        if system_id == "coffee":
            from coffee import CoffeeBean; return isinstance(item, CoffeeBean)
        if system_id == "tea":
            from tea import TeaLeaf; return isinstance(item, TeaLeaf)
        if system_id == "spirit":
            from spirits import Spirit; return isinstance(item, Spirit)
        if system_id == "cheese":
            from cheese import Cheese; return isinstance(item, Cheese)
        if system_id == "pottery":
            from pottery import PotteryPiece; return isinstance(item, PotteryPiece)
        if system_id == "salt":
            from salt import SaltCrystal; return isinstance(item, SaltCrystal)
        if system_id == "weapon":
            from weapons import Weapon; return isinstance(item, Weapon)
        if system_id == "textile":
            from textiles import Textile; return isinstance(item, Textile)
        if system_id == "jewelry":
            from jewelry import Jewelry; return isinstance(item, Jewelry)
        if system_id == "food":
            return isinstance(item, tuple) and len(item) == 2
    except Exception:
        pass
    return False


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
                            DoctorNPC, CoinDealerNPC,
                            NobleMaecenasNPC, WeaponOrderNPC,
                            sculpture_commission_display, sculpture_commission_hint,
                            tapestry_commission_display, tapestry_commission_hint,
                            weapon_commission_display, weapon_commission_hint)
        from outpost_npcs import OutpostKeeperNPC
        npc = self.active_npc
        if isinstance(npc, LeaderNPC):
            self._draw_leader_panel(player, npc)
            return
        from cities import ChapterMasterNPC
        if isinstance(npc, ChapterMasterNPC):
            self._draw_chapter_house_panel(player)
            return

        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        self.screen.blit(overlay, (0, 0))

        is_quest = isinstance(npc, (RockQuestNPC, WildflowerQuestNPC, GemQuestNPC))
        is_outpost = isinstance(npc, OutpostKeeperNPC)
        is_commission = isinstance(npc, (NobleMaecenasNPC, WeaponOrderNPC))
        PW = 660
        PH = 580 if is_outpost else (490 if (is_quest or is_commission) else 460)
        px = (SCREEN_W - PW) // 2
        py = (SCREEN_H - PH) // 2

        # Border colour per NPC type — royal classes checked first
        if isinstance(npc, (RoyalCuratorNPC, RoyalFloristNPC, RoyalJewelerNPC,
                             RoyalPaleontologistNPC, RoyalAnglerNPC)):
            border_col = (220, 175, 40)
        elif isinstance(npc, NobleMaecenasNPC):
            border_col = (140, 110, 170)
        elif isinstance(npc, WeaponOrderNPC):
            border_col = (130, 115, 90)
        elif isinstance(npc, WildflowerQuestNPC):
            border_col = (60, 140, 70)
        elif isinstance(npc, GemQuestNPC):
            border_col = (110, 50, 160)
        elif isinstance(npc, CoinDealerNPC):
            border_col = (200, 165, 45)
        elif _is_coin_npc(npc, "Auctioneer"):
            border_col = (190, 150, 230)
        elif _is_coin_npc(npc, "MoneyChanger"):
            border_col = (200, 200, 215)
        elif _is_coin_npc(npc, "Appraiser"):
            border_col = (130, 170, 230)
        elif _is_coin_npc(npc, "Collector"):
            border_col = (200, 165, 100)
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
        elif isinstance(npc, (NobleMaecenasNPC, WeaponOrderNPC)):
            self._draw_commission_content(player, npc, px, py, PW, PH)
        elif isinstance(npc, RockQuestNPC):
            self._draw_quest_content(player, npc, px, py, PW, PH)
        elif isinstance(npc, TradeNPC):
            self._draw_trade_content(player, npc, px, py, PW, PH)
        elif isinstance(npc, WildflowerQuestNPC):
            self._draw_wf_quest_content(player, npc, px, py, PW, PH)
        elif isinstance(npc, GemQuestNPC):
            self._draw_gem_quest_content(player, npc, px, py, PW, PH)
        elif isinstance(npc, CoinDealerNPC):
            self._draw_coin_dealer_content(player, npc, px, py, PW, PH)
        elif _is_coin_npc(npc, "Auctioneer"):
            self._draw_auctioneer_content(player, npc, px, py, PW, PH)
        elif _is_coin_npc(npc, "MoneyChanger"):
            self._draw_money_changer_content(player, npc, px, py, PW, PH)
        elif _is_coin_npc(npc, "Appraiser"):
            self._draw_coin_appraiser_content(player, npc, px, py, PW, PH)
        elif _is_coin_npc(npc, "Collector"):
            self._draw_coin_collector_content(player, npc, px, py, PW, PH)
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
        rank_name, color = rep_rank(rep)
        identity = getattr(npc, "identity", None)
        if identity:
            name_s = self.small.render(identity["display_name"], True, (220, 215, 200))
            self.screen.blit(name_s, (px + 14, py + 10))
            rep_s = self.small.render(f"{rank_name}  [{rep} rep]", True, color)
            self.screen.blit(rep_s, (px + 14, py + 26))
        else:
            s = self.small.render(f"{rank_name}  [{rep} rep]", True, color)
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
        health_txt = f"Current Health: {player.health} / {MAX_HEALTH}"
        h_s = self.medium.render(health_txt, True, (220, 80, 80))
        self.screen.blit(h_s, (px + 20, py + 140))

        cost_txt = f"Treatment Cost: {npc.heal_cost} gold"
        c_s = self.medium.render(cost_txt, True, (220, 200, 40))
        self.screen.blit(c_s, (px + 20, py + 180))

        # Heal Button
        btn_w, btn_h = 240, 60
        btn_rect = pygame.Rect(px + (PW - btn_w) // 2, py + PH - 100, btn_w, btn_h)

        can_afford = player.money >= npc.heal_cost
        can_heal = player.health < MAX_HEALTH

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

        if hasattr(npc, "ore_commission"):
            day_count = getattr(getattr(player, "world", None), "day_count", 0)
            npc.refresh_commission(day_count)
            c = npc.ore_commission
            if c:
                y += 10
                can = npc.can_complete_commission(player)
                have = player.inventory.get(c["ore_id"], 0)
                rect = pygame.Rect(px + 20, y, PW - 40, 68)
                self._trade_rects["commission"] = rect
                pygame.draw.rect(self.screen, (20, 36, 52) if can else (26, 26, 34), rect)
                pygame.draw.rect(self.screen, (60, 140, 200) if can else (50, 60, 75), rect, 2)
                hdr = self.small.render("TOWN COMMISSION", True, (100, 180, 240))
                self.screen.blit(hdr, (px + 28, y + 6))
                give_col = (80, 200, 255) if can else (160, 80, 80)
                self.screen.blit(
                    self.font.render(
                        f"Deliver: {c['amount']}x {c['ore_name']}  (have: {have})",
                        True, give_col),
                    (px + 28, y + 24))
                self.screen.blit(
                    self.font.render(f"Reward: {c['reward']} gold", True, (240, 210, 50)),
                    (px + 28, y + 44))
                lbl = self.font.render("DELIVER", True, (160, 220, 255) if can else (70, 70, 82))
                self.screen.blit(lbl, (rect.right - lbl.get_width() - 10,
                                       y + 34 - lbl.get_height() // 2))

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

    def _draw_commission_content(self, player, npc, px, py, PW, PH):
        from cities import (NobleMaecenasNPC, WeaponOrderNPC,
                            sculpture_commission_display, sculpture_commission_hint,
                            tapestry_commission_display, tapestry_commission_hint,
                            weapon_commission_display, weapon_commission_hint)

        if isinstance(npc, WeaponOrderNPC):
            title_txt = "WEAPON ORDER CLERK"
            title_col = (190, 170, 120)
        else:
            DIFF_LABELS = {0: "Patron", 1: "Grand Patron", 2: "Royal Patron"}
            diff_col    = {0: (160, 140, 200), 1: (190, 155, 220), 2: (220, 175, 255)}
            d = getattr(npc, "difficulty", 0)
            title_txt = f"NOBLE PATRON  [{DIFF_LABELS.get(d, 'Patron')}]"
            title_col = diff_col.get(d, (160, 140, 200))

        title = self.font.render(title_txt, True, title_col)
        self.screen.blit(title, (px + PW // 2 - title.get_width() // 2, py + 10))
        self._draw_rep_rank(npc, px, py)

        streak = getattr(npc, "_streak", 0)
        if streak > 0:
            bonus_pct = min(streak - 1, 2) * 25
            s_label = f"Streak: {streak}  (+{bonus_pct}% bonus)" if bonus_pct else f"Streak: {streak}"
            s_col = (80, 220, 130) if bonus_pct else (160, 200, 160)
            stxt = self.small.render(s_label, True, s_col)
            self.screen.blit(stxt, (px + PW - stxt.get_width() - 12, py + 32))

        self._trade_rects.clear()
        y = py + 40

        for cidx, c in enumerate(npc.commissions):
            row_h    = 150
            row_rect = pygame.Rect(px + 14, y, PW - 28, row_h)
            can = npc.can_complete(player, cidx)
            bg  = (25, 40, 20) if can else (22, 22, 30)
            bdr = (60, 160, 60) if can else (70, 60, 80)
            pygame.draw.rect(self.screen, bg, row_rect)
            pygame.draw.rect(self.screen, bdr, row_rect, 2)

            iy = y + 10
            kind = c["kind"]
            kind_labels = {"sculpture": "SCULPTURE", "tapestry": "TAPESTRY", "weapon": "WEAPON"}
            kind_cols   = {"sculpture": (180, 160, 120), "tapestry": (120, 160, 200), "weapon": (190, 140, 100)}
            badge = self.small.render(kind_labels.get(kind, "COMMISSION"), True,
                                      kind_cols.get(kind, (160, 160, 160)))
            self.screen.blit(badge, (px + 22, iy)); iy += 18

            if kind == "sculpture":
                desc = sculpture_commission_display(c)
                hint = sculpture_commission_hint(c)
            elif kind == "tapestry":
                desc = tapestry_commission_display(c)
                hint = tapestry_commission_hint(c)
            else:
                desc = weapon_commission_display(c)
                hint = weapon_commission_hint(c)

            self.screen.blit(self.font.render(desc, True, (220, 220, 220)), (px + 22, iy)); iy += 24
            self.screen.blit(self.small.render(hint, True, (140, 150, 170)), (px + 22, iy)); iy += 20

            matching_count = len(npc.find_matching(player, cidx)) if hasattr(npc, "find_matching") else \
                             len(npc.find_matching_weapons(player, c))
            if matching_count >= 1:
                status, sc = f"Ready!  ({matching_count} matching)", (80, 220, 80)
            else:
                status, sc = "None matching in inventory", (180, 90, 90)
            self.screen.blit(self.small.render(status, True, sc), (px + 22, iy)); iy += 18

            streak_bonus = min(streak, 2) * 25
            reward_str = f"Reward: {c['reward']} gold"
            if streak_bonus:
                bonus_val = int(c["reward"] * (1 + streak_bonus / 100)) - c["reward"]
                reward_str += f"  (+{bonus_val} streak bonus)"
            self.screen.blit(self.font.render(reward_str, True, (240, 210, 50)), (px + 22, iy))

            BW, BH = 170, 36
            bx2, by2 = px + PW - BW - 20, y + row_h // 2 - BH // 2
            btn_rect = pygame.Rect(bx2, by2, BW, BH)
            self._trade_rects[cidx] = btn_rect
            if can:
                b_bg, b_bdr, b_tc = (18, 90, 18), (45, 200, 45), (190, 255, 190)
            else:
                b_bg, b_bdr, b_tc = (30, 30, 36), (55, 55, 68), (70, 70, 82)
            pygame.draw.rect(self.screen, b_bg, btn_rect)
            pygame.draw.rect(self.screen, b_bdr, btn_rect, 2)
            bl = self.small.render("HAND OVER", True, b_tc)
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

        # --- Search bar ---
        sb_w, sb_h = 320, 24
        sb_x = SCREEN_W // 2 - sb_w // 2
        sb_y = 30
        self._inv_search_rect = pygame.Rect(sb_x, sb_y, sb_w, sb_h)
        sb_bg = (45, 45, 58) if self._inv_search_active else (28, 28, 36)
        pygame.draw.rect(self.screen, sb_bg, self._inv_search_rect)
        pygame.draw.rect(self.screen, (90, 90, 110), self._inv_search_rect, 1)
        if self._inv_search:
            sb_text = self._inv_search + ("|" if self._inv_search_active else "")
            sb_surf = self.small.render(sb_text, True, (220, 220, 220))
        elif self._inv_search_active:
            sb_surf = self.small.render("|", True, (160, 160, 180))
        else:
            sb_surf = self.small.render("Search...", True, (80, 80, 100))
        self.screen.blit(sb_surf, (sb_x + 6, sb_y + (sb_h - sb_surf.get_height()) // 2))

        # --- Tab row ---
        TAB_LABELS = ["All", "Seeds", "Food", "Tools"]
        tab_y = 58
        tab_h = 22
        COLS, CELL_W, CELL_H, GAP = 4, 210, 74, 8
        total_w = COLS * CELL_W + (COLS - 1) * GAP
        start_x = (SCREEN_W - total_w) // 2
        tab_total_w = total_w - 70  # leave room for sort button on right
        tab_w = tab_total_w // len(TAB_LABELS)
        self._inv_tab_rects.clear()
        for i, label in enumerate(TAB_LABELS):
            tx = start_x + i * (tab_w + 4)
            tab_rect = pygame.Rect(tx, tab_y, tab_w, tab_h)
            self._inv_tab_rects[i] = tab_rect
            if i == self._inv_tab:
                pygame.draw.rect(self.screen, (50, 50, 65), tab_rect)
                pygame.draw.rect(self.screen, (160, 155, 80), tab_rect, 1)
                tab_surf = self.small.render(label, True, (220, 210, 100))
            else:
                pygame.draw.rect(self.screen, (28, 28, 36), tab_rect)
                pygame.draw.rect(self.screen, (65, 65, 78), tab_rect, 1)
                tab_surf = self.small.render(label, True, (140, 140, 155))
            self.screen.blit(tab_surf, (tx + (tab_w - tab_surf.get_width()) // 2,
                                        tab_y + (tab_h - tab_surf.get_height()) // 2))

        sort_label = "#→1" if self._inv_sort_count else "A→Z"
        sort_w = 58
        sort_x = start_x + total_w - sort_w
        self._inv_sort_btn_rect = pygame.Rect(sort_x, tab_y, sort_w, tab_h)
        sort_bg = (40, 55, 40) if self._inv_sort_count else (28, 28, 36)
        pygame.draw.rect(self.screen, sort_bg, self._inv_sort_btn_rect)
        pygame.draw.rect(self.screen, (65, 90, 65), self._inv_sort_btn_rect, 1)
        sort_surf = self.small.render(sort_label, True, (150, 210, 150))
        self.screen.blit(sort_surf, (sort_x + (sort_w - sort_surf.get_width()) // 2,
                                     tab_y + (tab_h - sort_surf.get_height()) // 2))

        hint = self.small.render(
            "I to close  |  Right-click item → hotbar slot  |  Drag to move  |  Scroll to navigate",
            True, (80, 80, 95))
        self.screen.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, 84))

        # --- Filter + sort items ---
        search_lc = self._inv_search.lower()
        items_held = [
            (iid, cnt) for iid, cnt in player.inventory.items()
            if cnt > 0
            and _inv_tab_match(iid, ITEMS.get(iid, {}), self._inv_tab)
            and (not search_lc or search_lc in ITEMS.get(iid, {}).get("name", iid).lower())
        ]
        if self._inv_sort_count:
            items_held.sort(key=lambda t: -t[1])
        else:
            items_held.sort(key=lambda t: ITEMS.get(t[0], {}).get("name", t[0]))

        self._inv_rects.clear()

        AREA_TOP = 100
        AREA_BOT = SCREEN_H - 68
        area_h = AREA_BOT - AREA_TOP

        if not items_held:
            empty = self.font.render("Nothing here.", True, (90, 90, 90))
            self.screen.blit(empty, (SCREEN_W // 2 - empty.get_width() // 2, AREA_TOP + area_h // 2 - 10))
            return

        hotbar_map = {iid: i for i, iid in enumerate(player.hotbar) if iid}

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
        from cities import (rep_rank, supply_status_label,
                            sculpture_commission_display, sculpture_commission_hint,
                            tapestry_commission_display, tapestry_commission_hint)

        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        PW, PH = 640, 700
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
            ally_text = ", ".join(allies[:3]) + ("..." if len(allies) > 3 else "") if allies else "none"
            rival_text = ", ".join(rivals[:3]) + ("..." if len(rivals) > 3 else "") if rivals else "none"
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

        # Wealth + danger pills — region's economic and physical identity.
        if region:
            _WEALTH_COL = {"poor": (170, 130, 80), "modest": (180, 175, 140), "rich": (220, 200, 90)}
            _DANGER_COL = {"calm": (140, 200, 160), "rough": (200, 180, 110), "wild": (220, 110, 100)}
            wcol = _WEALTH_COL.get(region.wealth, (180, 180, 180))
            dcol = _DANGER_COL.get(region.danger, (180, 180, 180))
            wd_s = self.small.render(
                f"Wealth: {region.wealth.title()}   |   Danger: {region.danger.title()}",
                True, dcol if region.danger == "wild" else wcol)
            self.screen.blit(wd_s, (px + 16, py + 132))
            # Supply chips — inline after wealth/danger, shows scarce↓ or glut↑ tags only
            if region.supply:
                chips = []
                for tag, s in sorted(region.supply.items()):
                    if s >= 1.20:
                        chips.append((f"{tag}↑", (130, 175, 230)))
                    elif s <= 0.75:
                        chips.append((f"{tag}↓", (230, 120, 80)))
                if chips:
                    x_off = px + 16 + wd_s.get_width() + 12
                    for chip_text, chip_col in chips[:4]:
                        cs = self.small.render(chip_text + "  ", True, chip_col)
                        self.screen.blit(cs, (x_off, py + 132))
                        x_off += cs.get_width()

        pygame.draw.line(self.screen, border_col, (px + 10, py + 152), (px + PW - 10, py + 152))

        cy = py + 160
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
                # Supply chip — signals why this contract's reward may be elevated or reduced
                sup = supply_status_label(npc, item_id)
                if sup:
                    sup_label, sup_col = sup
                    sup_s = self.small.render(f"[{sup_label}]", True, sup_col)
                    self.screen.blit(sup_s, (px + 52 + inv_s.get_width() + 6, cy + 30))
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

        # --- ART COMMISSIONS ---
        cy += 4
        pygame.draw.line(self.screen, border_col, (px + 10, cy), (px + PW - 10, cy))
        cy += 8
        art_lbl = self.font.render("ART COMMISSIONS", True, (190, 160, 220))
        self.screen.blit(art_lbl, (px + 16, cy)); cy += 24

        art_streak = getattr(npc, "_art_streak", 0)
        if art_streak > 0:
            bonus_pct = min(art_streak - 1, 2) * 25
            as_label = f"Streak: {art_streak}  (+{bonus_pct}% bonus)" if bonus_pct else f"Streak: {art_streak}"
            as_txt = self.small.render(as_label, True, (160, 200, 160))
            self.screen.blit(as_txt, (px + PW - as_txt.get_width() - 14, cy - 20))

        for slot, c in enumerate(getattr(npc, "art_commissions", [])):
            row_h_art = 80
            row_rect_art = pygame.Rect(px + 12, cy, PW - 24, row_h_art)
            can_art = npc.can_complete_art(player, slot)
            bg  = (30, 20, 40) if can_art else (22, 18, 30)
            bdr = (140, 80, 200) if can_art else (80, 60, 100)
            pygame.draw.rect(self.screen, bg, row_rect_art)
            pygame.draw.rect(self.screen, bdr, row_rect_art, 2)

            kind = c["kind"]
            if kind == "sculpture":
                desc = sculpture_commission_display(c)
                hint_txt = sculpture_commission_hint(c)
            else:
                desc = tapestry_commission_display(c)
                hint_txt = tapestry_commission_hint(c)

            kind_col = (200, 170, 120) if kind == "sculpture" else (140, 180, 220)
            badge_s = self.small.render(kind.upper(), True, kind_col)
            self.screen.blit(badge_s, (px + 20, cy + 8))
            desc_s = self.font.render(desc, True, (220, 215, 200) if can_art else (140, 130, 110))
            self.screen.blit(desc_s, (px + 20 + badge_s.get_width() + 10, cy + 6))
            hint_s2 = self.small.render(hint_txt, True, (140, 130, 160))
            self.screen.blit(hint_s2, (px + 20, cy + 30))

            art_streak_bonus = min(art_streak, 2) * 25
            reward_str = f"{c['reward']} gold"
            if art_streak_bonus:
                bonus_val = int(c["reward"] * (1 + art_streak_bonus / 100)) - c["reward"]
                reward_str += f"  (+{bonus_val})"
            rwd_s = self.small.render(f"Reward: {reward_str}", True, (240, 210, 50))
            self.screen.blit(rwd_s, (px + 20, cy + 52))

            BW2, BH2 = 110, 28
            bx3 = row_rect_art.right - BW2 - 8
            by3 = cy + row_h_art // 2 - BH2 // 2
            btn_rect_art = pygame.Rect(bx3, by3, BW2, BH2)
            self._trade_rects[f"art_{slot}"] = btn_rect_art
            if can_art:
                b_bg2, b_bdr2, b_tc2 = (55, 20, 80), (160, 80, 220), (220, 180, 255)
            else:
                b_bg2, b_bdr2, b_tc2 = (30, 25, 38), (70, 55, 85), (90, 75, 105)
            pygame.draw.rect(self.screen, b_bg2, btn_rect_art)
            pygame.draw.rect(self.screen, b_bdr2, btn_rect_art, 2)
            bl2 = self.small.render("HAND OVER", True, b_tc2)
            self.screen.blit(bl2, (btn_rect_art.centerx - bl2.get_width() // 2,
                                    btn_rect_art.centery - bl2.get_height() // 2))
            cy += row_h_art + 6

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
        from wildflowers import render_wildflower

        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        PW, PH = 1160, 600
        px = (SCREEN_W - PW) // 2
        py = (SCREEN_H - PH) // 2
        pygame.draw.rect(self.screen, (10, 20, 10), (px, py, PW, PH))
        pygame.draw.rect(self.screen, (55, 130, 55), (px, py, PW, PH), 2)

        title_s = self.font.render("FLOWER ARRANGEMENT", True, (170, 235, 120))
        self.screen.blit(title_s, (SCREEN_W // 2 - title_s.get_width() // 2, py + 7))
        hint_s = self.small.render("Drag flowers from your collection into the garden  |  E or ESC: close", True, (80, 140, 80))
        self.screen.blit(hint_s, (SCREEN_W // 2 - hint_s.get_width() // 2, py + 27))

        flowers  = self.active_garden_flowers   # list of (Wildflower, cx, cy)
        drag_wf  = self._garden_drag_flower
        CAPACITY = 12
        FLOWER_R = 36

        # ── Left: free-form garden canvas ─────────────────────────────────
        CANVAS_W = 730
        canvas = pygame.Rect(px + 10, py + 48, CANVAS_W - 20, PH - 48 - 90)
        self._garden_canvas_rect = canvas

        pygame.draw.rect(self.screen, (20, 13, 7), canvas)
        pygame.draw.rect(self.screen, (52, 35, 18), canvas, 2)
        for i in range(35):
            dx = (i * 137 + 43) % (canvas.width - 16) + 8
            dy = (i * 89  + 17) % (canvas.height - 16) + 8
            pygame.draw.circle(self.screen, (38, 26, 12), (canvas.x + dx, canvas.y + dy), 2)

        self._garden_flower_rects.clear()

        for wf, cx, cy in flowers:
            draw_x = canvas.x + cx
            draw_y = canvas.y + cy
            surf = render_wildflower(wf, FLOWER_R * 2)
            self.screen.blit(surf, (draw_x - surf.get_width() // 2, draw_y - surf.get_height() // 2))
            name_s = self.small.render(wf.flower_type.replace("_", " ").title(), True, (200, 240, 175))
            self.screen.blit(name_s, (draw_x - name_s.get_width() // 2, draw_y + FLOWER_R - 2))
            hit_rect = pygame.Rect(draw_x - FLOWER_R, draw_y - FLOWER_R, FLOWER_R * 2, FLOWER_R * 2)
            self._garden_flower_rects[wf.uid] = hit_rect

        if drag_wf is not None:
            mx, my = pygame.mouse.get_pos()
            if canvas.collidepoint(mx, my):
                tx = max(FLOWER_R, min(canvas.width  - FLOWER_R, mx - canvas.x))
                ty = max(FLOWER_R, min(canvas.height - FLOWER_R, my - canvas.y))
                ind = pygame.Surface((FLOWER_R * 2, FLOWER_R * 2), pygame.SRCALPHA)
                ind.fill((100, 200, 100, 55))
                self.screen.blit(ind, (canvas.x + tx - FLOWER_R, canvas.y + ty - FLOWER_R))
                pygame.draw.rect(self.screen, (80, 180, 80),
                                 (canvas.x + tx - FLOWER_R, canvas.y + ty - FLOWER_R, FLOWER_R * 2, FLOWER_R * 2), 1)

        # ── Stats bar ─────────────────────────────────────────────────────
        stats_y = canvas.bottom + 8
        placed  = [wf for wf, cx, cy in flowers]

        if placed:
            avg_frag     = sum(f.fragrance for f in placed) / len(placed)
            avg_vibr     = sum(f.vibrancy  for f in placed) / len(placed)
            unique_sp    = len(set(f.flower_type   for f in placed))
            variety      = unique_sp / max(1, len(placed))
            biodomes     = len(set(f.biodome_found for f in placed))
            all_specials = sorted({s for f in placed for s in f.specials})

            def _bar(label, val, col, bx):
                ls = self.small.render(label, True, (130, 175, 110))
                self.screen.blit(ls, (bx, stats_y))
                bw = 150
                bx2 = bx + ls.get_width() + 5
                pygame.draw.rect(self.screen, (22, 32, 18), (bx2, stats_y + 2, bw, 13))
                fill = int(bw * min(1.0, val))
                if fill > 0:
                    pygame.draw.rect(self.screen, col, (bx2, stats_y + 2, fill, 13))
                pygame.draw.rect(self.screen, (50, 80, 45), (bx2, stats_y + 2, bw, 13), 1)
                pct = self.small.render(f"{int(val * 100)}%", True, (155, 195, 130))
                self.screen.blit(pct, (bx2 + bw + 4, stats_y))

            sx0 = px + 12
            _bar("Fragrance", avg_frag, (170, 100, 210), sx0)
            _bar("Vibrancy",  avg_vibr, (210, 170,  40), sx0 + 246)
            _bar("Variety",   variety,  ( 80, 185, 120), sx0 + 492)

            info_y = stats_y + 20
            bio_s = self.small.render(f"{biodomes} biodome{'s' if biodomes != 1 else ''} · {unique_sp} species · {len(placed)}/{CAPACITY} placed", True, (120, 185, 140))
            self.screen.blit(bio_s, (sx0, info_y))
            if all_specials:
                sp_s = self.small.render("Traits: " + ", ".join(all_specials), True, (175, 210, 120))
                self.screen.blit(sp_s, (sx0 + 370, info_y))
            ins_s = self.small.render("Attracting insects!", True, (80, 200, 80))
            self.screen.blit(ins_s, (sx0 + CANVAS_W - ins_s.get_width() - 16, info_y))
        else:
            es = self.small.render("Drag wildflowers from your collection into the garden", True, (60, 100, 60))
            self.screen.blit(es, (px + CANVAS_W // 2 - es.get_width() // 2, stats_y + 12))

        # ── Divider ───────────────────────────────────────────────────────
        div_x = px + CANVAS_W + 18
        pygame.draw.line(self.screen, (40, 90, 40), (div_x, py + 44), (div_x, py + PH - 16), 1)

        # ── Right: collection panel ───────────────────────────────────────
        rx  = div_x + 8
        RW  = PW - CANVAS_W - 38
        title2 = self.font.render("YOUR WILDFLOWERS", True, (140, 215, 100))
        self.screen.blit(title2, (rx + RW // 2 - title2.get_width() // 2, py + 10))

        # View All toggle button
        va_label = "VIEW LIST" if self._garden_view_all else "VIEW ALL"
        va_s = self.small.render(va_label, True, (140, 215, 100))
        va_rect = pygame.Rect(rx + RW - va_s.get_width() - 18, py + 29, va_s.get_width() + 12, 20)
        pygame.draw.rect(self.screen, (20, 48, 20) if self._garden_view_all else (12, 30, 12), va_rect)
        pygame.draw.rect(self.screen, (55, 130, 55), va_rect, 1)
        self.screen.blit(va_s, (va_rect.x + 6, va_rect.y + 2))
        self._garden_view_all_btn = va_rect

        placed_uids = {wf.uid for wf, cx, cy in flowers}
        if drag_wf and self._garden_drag_source == 'collection':
            placed_uids.add(drag_wf.uid)
        available = [f for f in player.wildflowers if f.uid not in placed_uids]

        COL_TOP = py + 52

        if self._garden_view_all:
            # ── Grid view ──
            GCELL   = (RW - 8) // 3
            cols    = 3
            AREA_H  = PH - 52 - 20
            total_rows = max(1, (len(available) + cols - 1) // cols)
            vis_rows   = max(1, AREA_H // GCELL)
            max_vs     = max(0, total_rows - vis_rows)
            self._garden_view_all_scroll = max(0, min(max_vs, self._garden_view_all_scroll))
            row_off = self._garden_view_all_scroll

            if max_vs > 0:
                sb_x  = rx + RW - 6
                sb_h  = AREA_H
                sb_th = max(20, sb_h * vis_rows // total_rows)
                sb_top = COL_TOP + (sb_h - sb_th) * row_off // max_vs
                pygame.draw.rect(self.screen, (14, 28, 14), (sb_x, COL_TOP, 5, sb_h))
                pygame.draw.rect(self.screen, (55, 130, 55), (sb_x, sb_top, 5, sb_th))

            clip = pygame.Rect(rx, COL_TOP, RW, AREA_H)
            self.screen.set_clip(clip)
            self._garden_view_all_rects.clear()
            self._garden_col_rects.clear()

            for i, wf in enumerate(available):
                c   = i % cols
                r   = i // cols - row_off
                if r < 0:
                    continue
                gx  = rx + 4 + c * GCELL
                gy  = COL_TOP + r * GCELL
                if gy + GCELL > COL_TOP + AREA_H:
                    break
                cell_rect = pygame.Rect(gx, gy, GCELL - 2, GCELL - 2)
                rar_col = self._RARITY_COLOR.get(wf.rarity, (100, 100, 100))
                pygame.draw.rect(self.screen, (18, 32, 18), cell_rect)
                pygame.draw.rect(self.screen, rar_col, cell_rect, 1)
                thumb_sz = min(GCELL - 24, 52)
                surf = render_wildflower(wf, thumb_sz)
                self.screen.blit(surf, (gx + (GCELL - 2) // 2 - surf.get_width() // 2, gy + 4))
                name = wf.flower_type.replace("_", " ").title()
                short = name if len(name) <= 10 else name[:9] + "..."
                ns = self.small.render(short, True, (210, 245, 188))
                self.screen.blit(ns, (gx + (GCELL - 2) // 2 - ns.get_width() // 2, gy + thumb_sz + 6))
                self._garden_view_all_rects[wf.uid] = cell_rect
                self._garden_col_rects[wf.uid] = cell_rect

            self.screen.set_clip(None)

            if not available and not placed:
                es = self.small.render("No wildflowers in collection", True, (50, 90, 55))
                self.screen.blit(es, (rx + RW // 2 - es.get_width() // 2, py + 280))
        else:
            # ── Normal list view ──
            CH, GAP   = 58, 6
            VISIBLE   = 7
            AREA_H    = VISIBLE * (CH + GAP)
            self._max_garden_col_scroll = max(0, len(available) - VISIBLE)
            self._garden_col_scroll = min(self._garden_col_scroll, self._max_garden_col_scroll)

            clip = pygame.Rect(rx, COL_TOP, RW, AREA_H + 4)
            self.screen.set_clip(clip)
            self._garden_col_rects.clear()

            for i, wf in enumerate(available):
                row = i - self._garden_col_scroll
                if row < 0 or row >= VISIBLE:
                    continue
                ry2 = py + 55 + row * (CH + GAP)
                rect = pygame.Rect(rx + 4, ry2, RW - 8, CH)
                self._garden_col_rects[wf.uid] = rect

                pygame.draw.rect(self.screen, (18, 32, 18), rect)
                rar_col = self._RARITY_COLOR.get(wf.rarity, (100, 100, 100))
                pygame.draw.rect(self.screen, rar_col, rect, 1)

                surf = render_wildflower(wf, 44)
                self.screen.blit(surf, (rx + 8, ry2 + (CH - 44) // 2))

                name = wf.flower_type.replace("_", " ").title()
                self.screen.blit(self.small.render(name, True, (210, 245, 188)), (rx + 58, ry2 + 6))
                self.screen.blit(self.small.render(wf.rarity.capitalize(), True, rar_col), (rx + 58, ry2 + 24))
                bio_s = self.small.render(wf.biodome_found, True, (95, 155, 105))
                self.screen.blit(bio_s, (rx + 58, ry2 + 40))
                if wf.specials:
                    sp_label = self.small.render(wf.specials[0], True, (160, 200, 115))
                    self.screen.blit(sp_label, (rx + RW - sp_label.get_width() - 12, ry2 + 6))

            self.screen.set_clip(None)

            if not available and not placed:
                es = self.small.render("No wildflowers in collection", True, (50, 90, 55))
                self.screen.blit(es, (rx + RW // 2 - es.get_width() // 2, py + 280))

        if len(flowers) >= CAPACITY:
            full_s = self.small.render("Garden full (12/12)", True, (140, 100, 40))
            self.screen.blit(full_s, (rx + RW // 2 - full_s.get_width() // 2, py + 510))

        # Collection drop-zone highlight when dragging from garden
        if drag_wf and self._garden_drag_source == 'canvas':
            col_zone = pygame.Rect(rx, py + 44, RW, PH - 60)
            hover = pygame.mouse.get_pos()
            if col_zone.collidepoint(hover):
                pygame.draw.rect(self.screen, (100, 60, 60), col_zone, 2)
            return_s = self.small.render("Drop here to return to collection", True, (180, 100, 100))
            self.screen.blit(return_s, (rx + RW // 2 - return_s.get_width() // 2, py + 530))

        # ── Dragged flower follows cursor ─────────────────────────────────
        if drag_wf is not None:
            surf = render_wildflower(drag_wf, 72)
            surf = surf.copy()
            surf.set_alpha(210)
            mx, my = self._garden_drag_pos
            self.screen.blit(surf, (mx - surf.get_width() // 2, my - surf.get_height() // 2))

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
        from Render.farmanimal import draw_sheep, draw_goat, draw_cow, draw_chicken, draw_capybara
        from Render.largeAnimal import draw_horse
        import types

        aid    = getattr(animal, 'animal_id', '')
        traits = dict(getattr(animal, 'traits', {}))
        if traits.get("mutation") == "golden":
            traits["color_shift"] = (0.35, 0.25, -0.30)

        sz    = traits.get("size", 1.0)
        eff_s = sz * scale
        traits["size"] = eff_s  # draw functions read size from traits for pixel offsets

        def _make_stub(base_w, base_h, **extra):
            stub = types.SimpleNamespace(
                traits=traits,
                W=int(base_w * eff_s),
                H=int(base_h * eff_s),
                facing=1,
                tamed=False,
                being_harvested=False,
                _kill_timer=0,
                _harvest_time=0,
                health=3,
            )
            for k, v in extra.items():
                setattr(stub, k, v)
            return stub

        if aid == "sheep":
            stub = _make_stub(24, 18, has_wool=getattr(animal, 'has_wool', True))
            draw_sheep(self.screen, cx - stub.W // 2, cy - stub.H // 2, stub)
        elif aid == "cow":
            stub = _make_stub(30, 20,
                              has_milk=getattr(animal, 'has_milk', False),
                              _milking=None)
            draw_cow(self.screen, cx - stub.W // 2, cy - stub.H // 2, stub)
        elif aid == "goat":
            stub = _make_stub(22, 18, has_milk=getattr(animal, 'has_milk', False))
            draw_goat(self.screen, cx - stub.W // 2, cy - stub.H // 2, stub)
        elif aid == "chicken":
            stub = _make_stub(18, 16, has_egg=getattr(animal, 'has_egg', False))
            draw_chicken(self.screen, cx - stub.W // 2, cy - stub.H // 2, stub)
        elif aid == "capybara":
            stub = _make_stub(34, 18)
            draw_capybara(self.screen, cx - stub.W // 2, cy - stub.H // 2, stub)
        elif aid == "dog":
            draw_dog(self.screen, cx - int(17 * eff_s), cy - int(11 * eff_s), animal, scale=eff_s, facing=1)
        elif aid == "horse":
            stub = _make_stub(40, 26, tamed=False, _broken=False, _on_trade_run=False)
            draw_horse(self.screen, cx - stub.W // 2, cy - stub.H // 2, stub)

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

        TYPE_LABELS = {"sheep": "Sheep", "cow": "Cow", "chicken": "Chicken", "horse": "Horse", "goat": "Goat", "dog": "Dog", "llama": "Llama", "yak": "Yak", "pig": "Pig"}

        # ── LEFT LIST COLUMN ──────────────────────────────────────────
        LW = 295
        lx0 = px
        lx1 = px + LW

        title_s = self.font.render(f"ANIMALS  ({len(all_tamed)})", True, (110, 210, 135))
        self.screen.blit(title_s, (lx0 + LW // 2 - title_s.get_width() // 2, py + 10))

        # Species filter tabs (two rows so labels stay readable)
        tab_rows = [
            [(0, "All"), (1, "Sheep"), (2, "Cow"), (3, "Chicken"), (4, "Horse")],
            [(5, "Goat"), (6, "Dogs"), (7, "Llama"), (8, "Yak"), (9, "Pig")],
        ]
        self._breed_tab_rects.clear()
        for ri, row in enumerate(tab_rows):
            tw = (LW - 6) // len(row)
            ry_tab = py + 36 + ri * 24
            for ti, (tidx, label) in enumerate(row):
                tx = lx0 + ti * (tw + 2)
                tr = pygame.Rect(tx, ry_tab, tw, 22)
                self._breed_tab_rects[tidx] = tr
                active = (tidx == self._breed_tab)
                pygame.draw.rect(self.screen, (28, 62, 40) if active else (20, 30, 24), tr)
                pygame.draw.rect(self.screen, (55, 150, 80) if active else (38, 65, 48), tr, 1)
                lbl = self.small.render(label, True, (150, 255, 170) if active else (90, 130, 105))
                self.screen.blit(lbl, (tx + tw // 2 - lbl.get_width() // 2,
                                       ry_tab + 11 - lbl.get_height() // 2))

        # Divider
        pygame.draw.line(self.screen, (38, 75, 52), (lx1, py), (lx1, py + PH))

        # Build filtered list
        tab_filter = {1: "sheep", 2: "cow", 3: "chicken", 4: "horse", 5: "goat", 6: "dog", 7: "llama", 8: "yak", 9: "pig"}.get(self._breed_tab)
        filtered = [e for e in all_tamed
                    if tab_filter is None or e.animal_id == tab_filter]

        ROW_H   = 54
        list_y0 = py + 88
        list_h  = PH - 92
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

        old_right_clip = self.screen.get_clip()
        self.screen.set_clip(pygame.Rect(rx0, py, rw, PH))

        num   = animal_numbers.get(animal.uid, 1)
        tname = TYPE_LABELS.get(animal.animal_id, animal.animal_id)

        # Header row
        hdg = self.font.render(f"{tname}  #{num}", True, (170, 255, 195))
        self.screen.blit(hdg, (rx0 + 12, py + 12))
        sex = getattr(animal, 'traits', {}).get("sex", "female")
        sex_sym  = "M" if sex == "male" else "F"
        sex_col  = (110, 175, 255) if sex == "male" else (255, 140, 180)
        sex_lbl  = self.font.render(sex_sym, True, sex_col)
        self.screen.blit(sex_lbl, (rx0 + 12 + hdg.get_width() + 8, py + 12))

        uid_lbl = self.small.render(f"uid: {animal.uid[:18]}...", True, (65, 90, 75))
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
        BAR_W   = 72
        BAR_H   = 8
        BAR_GAP = 5   # gap between the two allele bars
        COL_W   = 130  # width for one allele column

        # Column header row: explains what A / B / → mean
        _HDR_LW = 60
        hdr_a = self.small.render("A", True, (65, 95, 75))
        hdr_b = self.small.render("B", True, (65, 95, 75))
        hdr_e = self.small.render("→ expressed", True, (80, 115, 90))
        self.screen.blit(hdr_a, (stats_x + _HDR_LW + BAR_W // 2 - hdr_a.get_width() // 2, sy))
        self.screen.blit(hdr_b, (stats_x + _HDR_LW + BAR_W + BAR_GAP + BAR_W // 2 - hdr_b.get_width() // 2, sy))
        self.screen.blit(hdr_e, (stats_x + _HDR_LW + 2 * (BAR_W + BAR_GAP) + 8, sy))
        sy += 14

        def _draw_allele_quant(label, gene_key, lo, hi, bar_col, label_w=60):
            nonlocal sy
            pair = geno.get(gene_key)
            expressed = traits.get(gene_key.replace("_gene", ""), (lo + hi) / 2)
            lbl_s = self.small.render(label, True, (150, 195, 165))
            self.screen.blit(lbl_s, (stats_x, sy))
            for ai, av in enumerate(pair if pair else [expressed, expressed]):
                ax = stats_x + label_w + ai * (BAR_W + BAR_GAP)
                fill = max(0, min(BAR_W, int(BAR_W * (av - lo) / (hi - lo))))
                pygame.draw.rect(self.screen, (22, 40, 30), (ax, sy + 1, BAR_W, BAR_H))
                pygame.draw.rect(self.screen, bar_col, (ax, sy + 1, fill, BAR_H))
            exp_x = stats_x + label_w + 2 * (BAR_W + BAR_GAP) + 8
            exp_s = self.small.render(f"{expressed:.2f}", True, (220, 240, 225))
            self.screen.blit(exp_s, (exp_x, sy))
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
            _draw_allele_quant("Recovery",  "endurance_gene",0.7, 1.3, (100, 185, 240))
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
                        gone = self.small.render(f"Deceased  ({puid[:10]}...)", True, (155, 80, 80))
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

        self.screen.set_clip(old_right_clip)

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

        from cities import specialty_price_label, supply_status_label
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
            tag_x = px + 66 + gold_lbl.get_width() + 6
            if spec_tag:
                tag_col = (130, 200, 130) if spec_tag == "export" else (220, 170, 90)
                tag_s = self.small.render(f"({spec_tag})", True, tag_col)
                self.screen.blit(tag_s, (tag_x, y + 34))
                tag_x += tag_s.get_width() + 4
            # Supply chip — shows regional scarcity or glut
            sup = supply_status_label(npc, item_id)
            if sup:
                sup_label, sup_col = sup
                sup_s = self.small.render(f"[{sup_label}]", True, sup_col)
                self.screen.blit(sup_s, (tag_x, y + 34))
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

    def _draw_coin_dealer_content(self, player, npc, px, py, PW, PH):
        from UI.coins import _render_coin, _render_coin_reverse
        from coins import RARITY_COLORS, coin_price, ERROR_TYPES

        npc._ensure_stock(player, npc.world)

        _GOLD_C  = (218, 182, 55)
        _LABEL_C = (200, 185, 130)
        _DIM_C   = (90, 82, 58)
        _ERR_C   = (220, 80, 60)

        title_s = self.font.render("COIN DEALER", True, _GOLD_C)
        self.screen.blit(title_s, (px + PW // 2 - title_s.get_width() // 2, py + 10))
        gold_s = self.font.render(f"Your gold: {player.money}", True, _GOLD_C)
        self.screen.blit(gold_s, (px + PW - gold_s.get_width() - 16, py + 10))

        # Tab buttons
        tab = getattr(self, "_coin_dealer_tab", "buy")
        for t_label, t_key, t_x in (
            ("FOR SALE", "buy",  px + PW // 4 - 50),
            ("SELL COINS", "sell", px + 3 * PW // 4 - 50),
        ):
            active = (tab == t_key)
            tc = _GOLD_C if active else _DIM_C
            bg = (40, 35, 14) if active else (24, 22, 18)
            tb_rect = pygame.Rect(t_x, py + 34, 100, 22)
            pygame.draw.rect(self.screen, bg, tb_rect)
            pygame.draw.rect(self.screen, tc, tb_rect, 1)
            ts = self.small.render(t_label, True, tc)
            self.screen.blit(ts, (t_x + 50 - ts.get_width() // 2, py + 38))
            self._trade_rects[("tab", t_key)] = tb_rect

        sep_y = py + 60
        pygame.draw.line(self.screen, (80, 72, 45),
                         (px + 10, sep_y), (px + PW - 10, sep_y))

        self._coin_dealer_buy_rects  = {}
        self._coin_dealer_sell_rects = {}
        row_h   = 58
        col_w   = PW - 32
        y_start = sep_y + 8
        visible_rows = max(1, (PH - (sep_y - py) - 16) // (row_h + 4))

        if tab == "buy":
            stock  = npc._stock
            scroll = getattr(self, "_coin_dealer_scroll", 0)
            scroll = max(0, min(scroll, max(0, len(stock) - visible_rows)))
            self._coin_dealer_scroll = scroll

            for i, coin in enumerate(stock[scroll: scroll + visible_rows]):
                real_i = i + scroll
                y = y_start + i * (row_h + 4)
                price   = npc.sell_price(real_i)
                can_buy = player.money >= price
                rarity_col = RARITY_COLORS.get(coin.rarity, (160, 140, 80))
                is_err = getattr(coin, "error_type", "")

                bg  = (35, 30, 10) if can_buy else (26, 24, 32)
                brd = rarity_col if can_buy else (55, 50, 65)
                row_rect = pygame.Rect(px + 16, y, col_w, row_h)
                pygame.draw.rect(self.screen, bg, row_rect)
                pygame.draw.rect(self.screen, brd, row_rect, 2)
                if is_err:
                    pygame.draw.rect(self.screen, _ERR_C, row_rect, 1)

                coin_s = _render_coin(coin, 20)
                rev_s  = _render_coin_reverse(coin, 14)
                self.screen.blit(coin_s, (px + 20, y + row_h // 2 - 21))
                self.screen.blit(rev_s,  (px + 44, y + row_h // 2 - 15))

                name_col = _GOLD_C if can_buy else _DIM_C
                name_s = self.small.render(coin.denomination_label, True, name_col)
                self.screen.blit(name_s, (px + 68, y + 6))
                info_s = self.small.render(
                    f"{coin.civilization_name}  •  {coin.year_label}  •  {coin.condition.replace('_',' ').title()}",
                    True, _LABEL_C)
                self.screen.blit(info_s, (px + 68, y + 22))

                if is_err:
                    err_lbl = ERROR_TYPES.get(is_err, {}).get("label", is_err)
                    err_s = self.small.render(f"ERROR: {err_lbl}", True, _ERR_C)
                    self.screen.blit(err_s, (px + 68, y + 38))
                elif getattr(coin, "provenance", ""):
                    trunc = coin.provenance[:52] + ("..." if len(coin.provenance) > 52 else "")
                    prov_s = self.small.render(f'"{trunc}"', True, (140, 160, 120))
                    self.screen.blit(prov_s, (px + 68, y + 38))

                price_col = _GOLD_C if can_buy else (90, 80, 40)
                buy_s = self.font.render(f"{price}g  BUY", True, price_col)
                bx = px + PW - buy_s.get_width() - 20
                self.screen.blit(buy_s, (bx, y + row_h // 2 - buy_s.get_height() // 2))
                buy_rect = pygame.Rect(bx - 4, y + 4, buy_s.get_width() + 8, row_h - 8)
                self._coin_dealer_buy_rects[real_i] = buy_rect
                self._trade_rects[("buy", real_i)] = buy_rect

            if not stock:
                empty_s = self.small.render("No coins in stock today.", True, _DIM_C)
                self.screen.blit(empty_s, (px + PW // 2 - empty_s.get_width() // 2,
                                           y_start + 20))

        else:  # sell tab
            my_coins = getattr(player, "coins", [])
            scroll   = getattr(self, "_coin_dealer_sell_scroll", 0)
            scroll   = max(0, min(scroll, max(0, len(my_coins) - visible_rows)))
            self._coin_dealer_sell_scroll = scroll

            for i, coin in enumerate(my_coins[scroll: scroll + visible_rows]):
                real_i = i + scroll
                y      = y_start + i * (row_h + 4)
                price  = npc.buy_price(coin)
                rarity_col = RARITY_COLORS.get(coin.rarity, (160, 140, 80))
                is_err = getattr(coin, "error_type", "")

                row_rect = pygame.Rect(px + 16, y, col_w, row_h)
                pygame.draw.rect(self.screen, (26, 24, 20), row_rect)
                pygame.draw.rect(self.screen, rarity_col if not is_err else _ERR_C, row_rect, 2)

                coin_s = _render_coin(coin, 20)
                rev_s  = _render_coin_reverse(coin, 14)
                self.screen.blit(coin_s, (px + 20, y + row_h // 2 - 21))
                self.screen.blit(rev_s,  (px + 44, y + row_h // 2 - 15))

                name_s = self.small.render(coin.denomination_label, True, _LABEL_C)
                self.screen.blit(name_s, (px + 68, y + 6))
                info_s = self.small.render(
                    f"{coin.civilization_name}  •  {coin.year_label}  •  {coin.rarity.title()}",
                    True, _DIM_C)
                self.screen.blit(info_s, (px + 68, y + 22))
                if is_err:
                    err_s = self.small.render(
                        f"ERROR: {ERROR_TYPES.get(is_err,{}).get('label', is_err)}",
                        True, _ERR_C)
                    self.screen.blit(err_s, (px + 68, y + 38))

                sell_s = self.font.render(f"+{price}g  SELL", True, _GOLD_C)
                bx = px + PW - sell_s.get_width() - 20
                self.screen.blit(sell_s, (bx, y + row_h // 2 - sell_s.get_height() // 2))
                sell_rect = pygame.Rect(bx - 4, y + 4, sell_s.get_width() + 8, row_h - 8)
                self._coin_dealer_sell_rects[real_i] = sell_rect
                self._trade_rects[("sell", real_i)] = sell_rect

            if not my_coins:
                empty_s = self.small.render("You have no coins to sell.", True, _DIM_C)
                self.screen.blit(empty_s, (px + PW // 2 - empty_s.get_width() // 2,
                                           y_start + 20))

    # ── Auctioneer ──────────────────────────────────────────────────────────
    def _draw_auctioneer_content(self, player, npc, px, py, PW, PH):
        from UI.coins import _render_coin, _render_coin_reverse
        from coins import RARITY_COLORS

        npc._ensure_lots(player)

        _GOLD_C  = (230, 195, 60)
        _PURPLE  = (190, 150, 230)
        _LABEL_C = (200, 185, 130)
        _DIM_C   = (90, 82, 58)

        title_s = self.font.render("WEEKLY AUCTION", True, _PURPLE)
        self.screen.blit(title_s, (px + PW // 2 - title_s.get_width() // 2, py + 10))
        gold_s = self.font.render(f"Your gold: {player.money}", True, _GOLD_C)
        self.screen.blit(gold_s, (px + PW - gold_s.get_width() - 16, py + 10))

        sub = self.small.render(
            "Place a bid to enter; rival bidders respond automatically. "
            "Claim a winning lot before week's end.", True, _LABEL_C)
        self.screen.blit(sub, (px + 16, py + 34))

        self._auction_bid_rects   = {}
        self._auction_claim_rects = {}

        if not npc._lots:
            empty_s = self.small.render(
                "All lots awarded. New lots arrive next week.", True, _DIM_C)
            self.screen.blit(empty_s, (px + PW // 2 - empty_s.get_width() // 2, py + 200))
            return

        row_h = 88
        y     = py + 60
        for i, lot in enumerate(npc._lots):
            coin = lot["coin"]
            rarity_col = RARITY_COLORS.get(coin.rarity, _LABEL_C)
            bg = (30, 22, 42)
            row_rect = pygame.Rect(px + 16, y, PW - 32, row_h)
            pygame.draw.rect(self.screen, bg, row_rect)
            pygame.draw.rect(self.screen, rarity_col, row_rect, 2)

            coin_s = _render_coin(coin, 28)
            rev_s  = _render_coin_reverse(coin, 22)
            self.screen.blit(coin_s, (px + 26, y + row_h // 2 - 29))
            self.screen.blit(rev_s,  (px + 82, y + row_h // 2 - 23))

            name_s = self.font.render(coin.denomination_label, True, _GOLD_C)
            self.screen.blit(name_s, (px + 130, y + 6))
            info_s = self.small.render(
                f"{coin.civilization_name}  •  {coin.year_label}  •  "
                f"{coin.rarity.title()}  •  {coin.condition.replace('_',' ').title()}",
                True, _LABEL_C)
            self.screen.blit(info_s, (px + 130, y + 28))
            bid_s = self.small.render(
                f"Current bid: {lot['current_bid']}g    "
                f"Leader: {'You' if lot['leader']=='player' else 'House'}    "
                f"Rivals left: {lot['ai_bidders']}",
                True, _PURPLE if lot["leader"] == "player" else _LABEL_C)
            self.screen.blit(bid_s, (px + 130, y + 46))

            next_bid = npc.min_next_bid(i)
            can_bid  = npc.can_bid(i, player)
            label = f"BID {next_bid}g" if can_bid else (
                "LEADING" if lot["leader"] == "player" else "TOO COSTLY")
            bid_col = _GOLD_C if can_bid else _DIM_C
            bs = self.small.render(label, True, bid_col)
            bx = px + PW - bs.get_width() - 30
            by = y + 12
            br = pygame.Rect(bx - 6, by - 2, bs.get_width() + 12, bs.get_height() + 6)
            pygame.draw.rect(self.screen, (40, 30, 55), br)
            pygame.draw.rect(self.screen, bid_col, br, 1)
            self.screen.blit(bs, (bx, by))
            self._auction_bid_rects[i] = br
            self._trade_rects[("auction_bid", i)] = br

            if lot["leader"] == "player":
                claim_label = f"CLAIM {lot['current_bid']}g"
                claim_col = _GOLD_C if player.money >= lot["current_bid"] else _DIM_C
                cs = self.small.render(claim_label, True, claim_col)
                cx = px + PW - cs.get_width() - 30
                cy = y + 44
                cr = pygame.Rect(cx - 6, cy - 2, cs.get_width() + 12, cs.get_height() + 6)
                pygame.draw.rect(self.screen, (35, 50, 30), cr)
                pygame.draw.rect(self.screen, claim_col, cr, 1)
                self.screen.blit(cs, (cx, cy))
                self._auction_claim_rects[i] = cr
                self._trade_rects[("auction_claim", i)] = cr

            y += row_h + 6

    # ── Money-Changer ───────────────────────────────────────────────────────
    def _draw_money_changer_content(self, player, npc, px, py, PW, PH):
        from UI.coins import _render_coin
        from coins import RARITY_COLORS, coin_metal

        _GOLD_C  = (220, 200, 100)
        _LABEL_C = (200, 200, 215)
        _DIM_C   = (90, 90, 100)

        title_s = self.font.render("MONEY-CHANGER", True, _LABEL_C)
        self.screen.blit(title_s, (px + PW // 2 - title_s.get_width() // 2, py + 10))
        gold_s = self.font.render(f"Your gold: {player.money}", True, _GOLD_C)
        self.screen.blit(gold_s, (px + PW - gold_s.get_width() - 16, py + 10))

        sub = self.small.render(
            "I weigh coins by metal, not by rarity. Common iron-rate, every time.",
            True, _DIM_C)
        self.screen.blit(sub, (px + 16, py + 34))

        self._money_changer_rects = {}
        my_coins = getattr(player, "coins", [])
        if not my_coins:
            empty_s = self.small.render("You have no coins to weigh.", True, _DIM_C)
            self.screen.blit(empty_s, (px + PW // 2 - empty_s.get_width() // 2, py + 200))
            return

        row_h = 50
        scroll = getattr(self, "_money_changer_scroll", 0)
        visible_rows = max(1, (PH - 80) // (row_h + 4))
        scroll = max(0, min(scroll, max(0, len(my_coins) - visible_rows)))
        self._money_changer_scroll = scroll

        y = py + 60
        for i, coin in enumerate(my_coins[scroll: scroll + visible_rows]):
            real_i = i + scroll
            row_rect = pygame.Rect(px + 16, y, PW - 32, row_h)
            pygame.draw.rect(self.screen, (24, 24, 30), row_rect)
            pygame.draw.rect(self.screen, RARITY_COLORS.get(coin.rarity, _LABEL_C), row_rect, 1)

            coin_s = _render_coin(coin, 18)
            self.screen.blit(coin_s, (px + 22, y + row_h // 2 - 19))

            metal = coin_metal(coin.denomination_key).title()
            name_s = self.small.render(
                f"{coin.denomination_label}  •  {metal}", True, _LABEL_C)
            self.screen.blit(name_s, (px + 64, y + 8))

            collector = self.small.render(
                f"Collector value: ~{coin.rarity.title()}", True, _DIM_C)
            self.screen.blit(collector, (px + 64, y + 26))

            price = npc.buy_price(coin)
            ps = self.font.render(f"+{price}g  MELT", True, _GOLD_C)
            bx = px + PW - ps.get_width() - 24
            self.screen.blit(ps, (bx, y + row_h // 2 - ps.get_height() // 2))
            pr = pygame.Rect(bx - 4, y + 4, ps.get_width() + 8, row_h - 8)
            self._money_changer_rects[real_i] = pr
            self._trade_rects[("money_changer", real_i)] = pr

            y += row_h + 4

    # ── Coin Appraiser ──────────────────────────────────────────────────────
    def _draw_coin_appraiser_content(self, player, npc, px, py, PW, PH):
        from UI.coins import _render_coin, _render_coin_reverse
        from coins import RARITY_COLORS

        _GOLD_C  = (220, 190, 80)
        _BLUE_C  = (130, 170, 230)
        _LABEL_C = (200, 185, 130)
        _DIM_C   = (90, 82, 58)

        title_s = self.font.render("COIN APPRAISER", True, _BLUE_C)
        self.screen.blit(title_s, (px + PW // 2 - title_s.get_width() // 2, py + 10))
        gold_s = self.font.render(f"Your gold: {player.money}", True, _GOLD_C)
        self.screen.blit(gold_s, (px + PW - gold_s.get_width() - 16, py + 10))

        sub = self.small.render(
            "Pay to research a coin's provenance, or to re-grade its condition (one attempt per coin).",
            True, _LABEL_C)
        self.screen.blit(sub, (px + 16, py + 34))

        self._appraiser_appraise_rects = {}
        self._appraiser_regrade_rects  = {}

        my_coins = getattr(player, "coins", [])
        if not my_coins:
            empty_s = self.small.render("You have no coins to appraise.", True, _DIM_C)
            self.screen.blit(empty_s, (px + PW // 2 - empty_s.get_width() // 2, py + 200))
            return

        row_h = 64
        scroll = getattr(self, "_appraiser_scroll", 0)
        visible_rows = max(1, (PH - 80) // (row_h + 4))
        scroll = max(0, min(scroll, max(0, len(my_coins) - visible_rows)))
        self._appraiser_scroll = scroll

        y = py + 60
        for i, coin in enumerate(my_coins[scroll: scroll + visible_rows]):
            real_i = i + scroll
            row_rect = pygame.Rect(px + 16, y, PW - 32, row_h)
            pygame.draw.rect(self.screen, (22, 24, 36), row_rect)
            pygame.draw.rect(self.screen, RARITY_COLORS.get(coin.rarity, _LABEL_C), row_rect, 1)

            coin_s = _render_coin(coin, 22)
            rev_s  = _render_coin_reverse(coin, 14)
            self.screen.blit(coin_s, (px + 24, y + row_h // 2 - 23))
            self.screen.blit(rev_s,  (px + 50, y + row_h // 2 - 15))

            name_s = self.small.render(coin.denomination_label, True, _LABEL_C)
            self.screen.blit(name_s, (px + 74, y + 6))
            info_s = self.small.render(
                f"{coin.civilization_name}  •  {coin.rarity.title()}  •  "
                f"{coin.condition.replace('_',' ').title()}",
                True, _DIM_C)
            self.screen.blit(info_s, (px + 74, y + 22))

            prov_state = "Has provenance" if coin.provenance else "No provenance"
            ps = self.small.render(prov_state, True,
                                   (160, 180, 130) if coin.provenance else _DIM_C)
            self.screen.blit(ps, (px + 74, y + 38))

            # Appraise button
            ap_cost = npc.appraise_cost(coin)
            can_ap  = npc.can_appraise(coin, player)
            ap_lbl  = f"APPRAISE {ap_cost}g" if not coin.provenance else "DONE"
            ap_col  = _BLUE_C if can_ap else _DIM_C
            aps = self.small.render(ap_lbl, True, ap_col)
            ax  = px + PW - aps.get_width() - 24
            ay  = y + 8
            ar  = pygame.Rect(ax - 4, ay - 2, aps.get_width() + 8, aps.get_height() + 6)
            pygame.draw.rect(self.screen, (28, 32, 48), ar)
            pygame.draw.rect(self.screen, ap_col, ar, 1)
            self.screen.blit(aps, (ax, ay))
            self._appraiser_appraise_rects[real_i] = ar
            self._trade_rects[("appraise", real_i)] = ar

            # Regrade button
            re_cost = npc.regrade_cost(coin)
            can_re  = npc.can_regrade(coin, player)
            used    = npc._regrade_attempts.get(coin.uid, 0) > 0
            re_lbl  = f"REGRADE {re_cost}g" if not used else "USED"
            re_col  = _GOLD_C if can_re else _DIM_C
            res = self.small.render(re_lbl, True, re_col)
            rx  = px + PW - res.get_width() - 24
            ry  = y + 34
            rr  = pygame.Rect(rx - 4, ry - 2, res.get_width() + 8, res.get_height() + 6)
            pygame.draw.rect(self.screen, (44, 36, 16), rr)
            pygame.draw.rect(self.screen, re_col, rr, 1)
            self.screen.blit(res, (rx, ry))
            self._appraiser_regrade_rects[real_i] = rr
            self._trade_rects[("regrade", real_i)] = rr

            y += row_h + 4

    # ── Coin Collector ──────────────────────────────────────────────────────
    def _draw_coin_collector_content(self, player, npc, px, py, PW, PH):
        from UI.coins import _render_coin
        from coins import RARITY_COLORS

        npc._ensure_interest(player)
        npc._refresh_budget()
        interest = npc._interest or {"label": "any coin", "premium": 1.0}

        _GOLD_C  = (220, 175, 50)
        _BUFF_C  = (220, 190, 130)
        _LABEL_C = (200, 185, 130)
        _DIM_C   = (90, 82, 58)

        title_s = self.font.render("COIN COLLECTOR", True, _BUFF_C)
        self.screen.blit(title_s, (px + PW // 2 - title_s.get_width() // 2, py + 10))
        gold_s = self.font.render(f"Your gold: {player.money}", True, _GOLD_C)
        self.screen.blit(gold_s, (px + PW - gold_s.get_width() - 16, py + 10))

        intro = self.small.render(
            f'"I fancy {interest["label"]} — I pay well for them!"', True, _BUFF_C)
        self.screen.blit(intro, (px + 16, py + 34))
        budget_s = self.small.render(
            f"Today's purse: {npc._budget}g    Premium: {int((interest.get('premium',1)-1)*100)}% over collector value",
            True, _LABEL_C)
        self.screen.blit(budget_s, (px + 16, py + 50))

        self._collector_rects = {}
        my_coins = getattr(player, "coins", [])
        if not my_coins:
            empty_s = self.small.render("You have no coins to offer.", True, _DIM_C)
            self.screen.blit(empty_s, (px + PW // 2 - empty_s.get_width() // 2, py + 200))
            return

        # Ordered: matches first, then non-matches (greyed out)
        from coins import coin_matches_interest as _cmi
        ordered = ([(i, c) for i, c in enumerate(my_coins) if _cmi(c, interest)]
                   + [(i, c) for i, c in enumerate(my_coins) if not _cmi(c, interest)])

        row_h = 50
        scroll = getattr(self, "_collector_scroll", 0)
        visible_rows = max(1, (PH - 90) // (row_h + 4))
        scroll = max(0, min(scroll, max(0, len(ordered) - visible_rows)))
        self._collector_scroll = scroll

        y = py + 76
        for slot, (real_i, coin) in enumerate(ordered[scroll: scroll + visible_rows]):
            is_match = _cmi(coin, interest)
            row_rect = pygame.Rect(px + 16, y, PW - 32, row_h)
            pygame.draw.rect(self.screen, (32, 28, 18) if is_match else (22, 22, 24),
                             row_rect)
            brd = (RARITY_COLORS.get(coin.rarity, _LABEL_C) if is_match else _DIM_C)
            pygame.draw.rect(self.screen, brd, row_rect, 2 if is_match else 1)

            coin_s = _render_coin(coin, 18)
            self.screen.blit(coin_s, (px + 22, y + row_h // 2 - 19))

            name_col = _BUFF_C if is_match else _DIM_C
            name_s = self.small.render(coin.denomination_label, True, name_col)
            self.screen.blit(name_s, (px + 64, y + 6))
            info_s = self.small.render(
                f"{coin.civilization_name}  •  {coin.rarity.title()}",
                True, _LABEL_C if is_match else _DIM_C)
            self.screen.blit(info_s, (px + 64, y + 24))

            if is_match:
                offer = npc.offer_for(coin)
                can_buy = npc.can_buy(coin)
                lbl = f"+{offer}g  OFFER" if can_buy else f"+{offer}g  (no purse)"
                col = _GOLD_C if can_buy else _DIM_C
                ps = self.font.render(lbl, True, col)
                bx = px + PW - ps.get_width() - 24
                self.screen.blit(ps, (bx, y + row_h // 2 - ps.get_height() // 2))
                pr = pygame.Rect(bx - 4, y + 4, ps.get_width() + 8, row_h - 8)
                self._collector_rects[real_i] = pr
                self._trade_rects[("collector", real_i)] = pr
            else:
                ns = self.small.render("not interested", True, _DIM_C)
                self.screen.blit(ns, (px + PW - ns.get_width() - 24,
                                      y + row_h // 2 - ns.get_height() // 2))

            y += row_h + 4

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
            active     = can_buy or can_barter

            row_h    = 64
            row_rect = pygame.Rect(px + 20, y, PW - 40, row_h)
            pygame.draw.rect(self.screen, (24, 26, 34), row_rect)
            pygame.draw.rect(self.screen, (60, 70, 90) if active else (40, 44, 55), row_rect, 1)

            item_color = ITEMS.get(item_id, {}).get("color", (128, 128, 128))
            pygame.draw.rect(self.screen, item_color, (px + 30, y + 18, 28, 28))

            name_col = (220, 228, 245) if active else (115, 120, 135)
            self.screen.blit(self.font.render(display, True, name_col), (px + 70, y + 8))

            spec_tag = specialty_price_label(npc, item_id)
            if spec_tag:
                tag_col = (130, 200, 130) if spec_tag == "export" else (220, 170, 90)
                tag_s = self.small.render(spec_tag, True, tag_col)
                name_w = self.font.size(display)[0]
                self.screen.blit(tag_s, (px + 70 + name_w + 8, y + 12))

            sub_col = (150, 155, 170) if active else (90, 95, 105)
            cost_col = (210, 180, 80) if can_buy else sub_col
            self.screen.blit(self.small.render(f"{cost} gold", True, cost_col), (px + 70, y + 30))

            barter_name = ITEMS.get(barter_item, {}).get("name", barter_item)
            barter_col = (140, 210, 165) if can_barter else sub_col
            self.screen.blit(self.small.render(f"or {barter_qty} {barter_name}", True, barter_col),
                             (px + 70, y + 46))

            btn_w, btn_h = 64, 22
            buy_rect = pygame.Rect(row_rect.right - btn_w - 10, y + 8, btn_w, btn_h)
            buy_fill = (90, 75, 25) if can_buy else (38, 40, 50)
            buy_text = (255, 220, 110) if can_buy else (95, 95, 110)
            pygame.draw.rect(self.screen, buy_fill, buy_rect, border_radius=3)
            buy_lbl = self.small.render("BUY", True, buy_text)
            self.screen.blit(buy_lbl, (buy_rect.centerx - buy_lbl.get_width() // 2,
                                       buy_rect.centery - buy_lbl.get_height() // 2))
            self._trade_rects[(i, "buy")] = buy_rect

            trade_rect = pygame.Rect(row_rect.right - btn_w - 10, y + 34, btn_w, btn_h)
            trade_fill = (25, 75, 55) if can_barter else (38, 40, 50)
            trade_text = (140, 230, 175) if can_barter else (95, 95, 110)
            pygame.draw.rect(self.screen, trade_fill, trade_rect, border_radius=3)
            trade_lbl = self.small.render("TRADE", True, trade_text)
            self.screen.blit(trade_lbl, (trade_rect.centerx - trade_lbl.get_width() // 2,
                                         trade_rect.centery - trade_lbl.get_height() // 2))
            self._trade_rects[(i, "barter")] = trade_rect

            y += row_h + 4

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
                status_text = f"Traveling to {town_name}... (~{blocks_left:.0f} blocks away)"
            else:
                status_text = f"Traveling to {town_name}..."
            st_col = (255, 160, 0) if horse_stuck else (200, 200, 80)
        else:
            if active_horse is not None:
                blocks_left = max(0, abs((active_horse.x + active_horse.W / 2) - pos[0] * _BS) // _BS)
                status_text = f"Returning home... (~{blocks_left:.0f} blocks away)"
            else:
                status_text = "Returning home..."
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

    def _draw_npc_inspect(self, player, world):
        import npc_preferences as npc_prefs_mod
        npc = getattr(player, "inspecting_npc", None)
        if npc is None:
            return

        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        has_dynasty = bool(getattr(npc, "dynasty_name", None))
        npc_uid_pre = getattr(npc, "npc_uid", None) or ""
        _pre_rel    = player.npc_relationships.get(npc_uid_pre, 0)
        _pre_ident  = getattr(npc, "identity", None) or {}
        has_rumour  = bool(_pre_ident.get("personal_tension")) and _pre_rel >= 50
        PW = 620
        PH = min(700, SCREEN_H - 40)
        px = (SCREEN_W - PW) // 2
        py = (SCREEN_H - PH) // 2

        pygame.draw.rect(self.screen, (18, 18, 26), (px, py, PW, PH))
        pygame.draw.rect(self.screen, (90, 80, 140), (px, py, PW, PH), 2)

        hint = self.small.render("I or ESC to close", True, (90, 90, 110))
        self.screen.blit(hint, (px + PW - hint.get_width() - 8, py + 8))

        is_guard = isinstance(npc, GuardNPC)
        sketch_rect = None
        npc_uid_val = getattr(npc, "npc_uid", None) or ""
        already_sketched = any(
            s.npc_uid == npc_uid_val
            for s in getattr(player, "guard_sketches", [])
            if npc_uid_val
        )
        if is_guard and not already_sketched:
            BTN_W2, BTN_H2 = 130, 24
            sketch_rect = pygame.Rect(px + PW - BTN_W2 - 8, py + 26, BTN_W2, BTN_H2)
            pygame.draw.rect(self.screen, (30, 40, 55), sketch_rect)
            pygame.draw.rect(self.screen, (80, 130, 180), sketch_rect, 1)
            sk_s = self.small.render("Make a Sketch", True, (160, 200, 240))
            self.screen.blit(sk_s, (sketch_rect.x + (BTN_W2 - sk_s.get_width()) // 2,
                                    sketch_rect.y + (BTN_H2 - sk_s.get_height()) // 2))

        identity = getattr(npc, "identity", None) or {}
        first  = identity.get("first_name", "???")
        family = identity.get("family_name", "")
        blurb  = identity.get("blurb", "")
        role   = getattr(npc, "display_name", npc.animal_id)

        cy = py + 18
        name_s = self.font.render(f"{first} {family}", True, (240, 220, 160))
        self.screen.blit(name_s, (px + 16, cy))
        cy += 26
        role_s = self.small.render(role, True, (170, 150, 110))
        self.screen.blit(role_s, (px + 16, cy))
        cy += 20
        bio = identity.get("bio", blurb)
        if bio:
            for line in _wrap_text(bio, self.small, PW - 32):
                self.screen.blit(self.small.render(line, True, (140, 133, 120)), (px + 16, cy))
                cy += 16
        cy += 6

        pygame.draw.line(self.screen, (60, 55, 80), (px + 8, cy), (px + PW - 8, cy))
        cy += 10

        scroll_top    = cy
        BTN_AREA      = 52
        scroll_bottom = py + PH - BTN_AREA
        scroll_offset = max(0, getattr(self, '_inspect_panel_scroll', 0))
        cy -= scroll_offset
        self.screen.set_clip(pygame.Rect(px, scroll_top, PW, scroll_bottom - scroll_top))

        self.screen.blit(self.small.render("FAMILY", True, (110, 110, 160)), (px + 16, cy))
        cy += 18
        if npc.spouse_uid:
            spouse_name = self._resolve_npc_name(npc.spouse_uid, world)
            self.screen.blit(self.small.render(f"Spouse:   {spouse_name}", True, (195, 185, 165)), (px + 24, cy))
            cy += 16
        if npc.parent_uids:
            parents = [self._resolve_npc_name(u, world) for u in npc.parent_uids[:2]]
            self.screen.blit(self.small.render(f"Parents:  {', '.join(parents)}", True, (195, 185, 165)), (px + 24, cy))
            cy += 16
        if npc.sibling_uids:
            sibs = [self._resolve_npc_name(u, world) for u in npc.sibling_uids[:3]]
            extra = len(npc.sibling_uids) - 3
            sib_str = ", ".join(sibs) + (f" +{extra}" if extra > 0 else "")
            self.screen.blit(self.small.render(f"Siblings: {sib_str}", True, (195, 185, 165)), (px + 24, cy))
            cy += 16
        if not npc.spouse_uid and not npc.parent_uids and not npc.sibling_uids:
            self.screen.blit(self.small.render("No known family in this town.", True, (120, 115, 100)), (px + 24, cy))
            cy += 16
        cy += 4

        # ---- Knightly Order section (KnightNPCs / any NPC linked to a knight) ----
        npc_order_id  = getattr(npc, "order_id", None)
        npc_knight_id = getattr(npc, "knight_id", None)
        if npc_order_id is not None:
            try:
                import knightly_orders as _ko
                _ord = _ko.order(npc_order_id)
                _kn  = _ko.knight(npc_knight_id) if npc_knight_id is not None else None
            except Exception:
                _ord, _kn = None, None
            if _ord is not None:
                pygame.draw.line(self.screen, (60, 55, 80), (px + 8, cy), (px + PW - 8, cy))
                cy += 10
                tint = _ord.heraldry.primary
                pygame.draw.rect(self.screen, tint, (px + 16, cy + 2, 12, 12))
                self.screen.blit(self.small.render(
                    f"KNIGHTLY ORDER  —  {_ord.name}", True, (200, 175, 110)),
                    (px + 34, cy))
                cy += 18
                rank_raw = (_kn.rank if _kn else "Knight-Errant")
                rank_lbl = _ko.cultural_rank_label(_ord.tradition, rank_raw)
                noble_tag = ""
                if _kn and _kn.is_noble and _kn.noble_title:
                    noble_tag = f"  ·  {_kn.noble_title}"
                self.screen.blit(self.small.render(
                    f"Rank: {rank_lbl}  ({_ord.tradition.title()}){noble_tag}",
                    True, (210, 200, 165)), (px + 24, cy))
                cy += 16
                if _ord.motto:
                    self.screen.blit(self.small.render(
                        f'Motto: "{_ord.motto}"', True, (190, 175, 130)),
                        (px + 24, cy))
                    cy += 16
                if _ord.seat:
                    self.screen.blit(self.small.render(
                        f"Seat: {_ord.seat}", True, (175, 165, 130)),
                        (px + 24, cy))
                    cy += 16
                self.screen.blit(self.small.render(
                    f"Order prestige: {_ord.prestige}/100", True, (175, 165, 130)),
                    (px + 24, cy))
                cy += 16
                if _kn and _kn.tournament_wins:
                    self.screen.blit(self.small.render(
                        f"Tournament wins: {_kn.tournament_wins}",
                        True, (200, 180, 110)), (px + 24, cy))
                    cy += 16
                if _kn and _kn.quirks:
                    self.screen.blit(self.small.render(
                        f"— {_kn.quirks[0]}", True, (165, 150, 110)),
                        (px + 24, cy))
                    cy += 16
                if _ord.rival_id is not None:
                    try:
                        _riv = _ko.order(_ord.rival_id)
                        if _riv:
                            self.screen.blit(self.small.render(
                                f"Sworn rival: {_riv.name}", True, (200, 110, 100)),
                                (px + 24, cy))
                            cy += 16
                    except Exception:
                        pass
                cy += 4

        # ---- Dynasty section (nobles and elders only) ----
        dynasty_name    = getattr(npc, "dynasty_name", None)
        dynasty_role    = getattr(npc, "dynasty_role", None)
        dynasty_kin     = getattr(npc, "dynasty_kin", None) or []
        dynasty_history = getattr(npc, "dynasty_history", None)
        dynasty_tension = getattr(npc, "dynasty_tension", None)
        dynasty_rival   = getattr(npc, "dynasty_rival", None)
        if dynasty_name:
            pygame.draw.line(self.screen, (60, 55, 80), (px + 8, cy), (px + PW - 8, cy))
            cy += 10
            header = f"DYNASTY  —  {dynasty_name}  ({dynasty_role.title()} of House)"
            self.screen.blit(self.small.render(header, True, (180, 160, 90)), (px + 16, cy))
            cy += 18
            # Kin across towns
            if dynasty_kin:
                for kin in dynasty_kin[:4]:
                    label = (f"{kin['display_name']}  ·  {kin['dynasty_role'].title()}"
                             f"  in  {kin['town_name']}")
                    self.screen.blit(self.small.render(label, True, (195, 185, 140)), (px + 24, cy))
                    cy += 16
                if len(dynasty_kin) > 4:
                    extra = self.small.render(f"  +{len(dynasty_kin) - 4} more kin...", True, (120, 115, 100))
                    self.screen.blit(extra, (px + 24, cy))
                    cy += 16
            else:
                self.screen.blit(self.small.render("Sole ruler of this dynasty.", True, (120, 115, 100)), (px + 24, cy))
                cy += 16
            # Origin and current tension
            cy += 4
            if dynasty_history:
                for line in _wrap_text(dynasty_history, self.small, PW - 40):
                    self.screen.blit(self.small.render(line, True, (150, 140, 95)), (px + 24, cy))
                    cy += 15
            if dynasty_tension:
                for line in _wrap_text(dynasty_tension, self.small, PW - 40):
                    self.screen.blit(self.small.render(line, True, (190, 120, 95)), (px + 24, cy))
                    cy += 15
            if dynasty_rival:
                self.screen.blit(
                    self.small.render(f"Long rivals with: {dynasty_rival}", True, (170, 75, 75)),
                    (px + 24, cy))
                cy += 16
                # Rivalry tension display
                import npc_dynasty as _dyn_inspect
                npc_rid  = getattr(npc, "dynasty_id", None)
                rival_rid_inspect = getattr(npc, "dynasty_rival_region_id", None)
                if npc_rid is not None and rival_rid_inspect is not None:
                    _rkey = _dyn_inspect._rivalry_key(npc_rid, rival_rid_inspect)
                    _tlabel, _tcol = _dyn_inspect.tension_label(player, _rkey)
                    self.screen.blit(
                        self.small.render(f"Rivalry status: {_tlabel}", True, _tcol),
                        (px + 24, cy))
                    cy += 16
                    if _dyn_inspect.tension_level(player, _rkey) >= 2:
                        self.screen.blit(
                            self.small.render("Merchants here charge more while the feud holds.",
                                              True, (200, 130, 80)),
                            (px + 24, cy))
                        cy += 16
            # Rival/favored status for this player
            dynasty_region_id = getattr(npc, "dynasty_id", None)
            if dynasty_region_id in getattr(player, "rival_dynasty_regions", set()):
                self.screen.blit(
                    self.small.render("⚠ You are allied with their enemy.", True, (210, 80, 70)),
                    (px + 24, cy))
                cy += 16
            elif dynasty_region_id in getattr(player, "champion_dynasty_regions", set()):
                self.screen.blit(
                    self.small.render("★ You are Champion of this house.", True, (220, 190, 60)),
                    (px + 24, cy))
                cy += 16
            elif dynasty_region_id in getattr(player, "favored_dynasty_regions", set()):
                self.screen.blit(
                    self.small.render("✦ You are Favored by this house.", True, (140, 200, 120)),
                    (px + 24, cy))
                cy += 16
            cy += 4

            # ---- Knightly orders patronized by / based in this house's lands ----
            try:
                import knightly_orders as _ko_dyn
                _home_orders = _ko_dyn.orders_for_region(dynasty_region_id) \
                    if dynasty_region_id is not None else []
            except Exception:
                _home_orders = []
            if _home_orders:
                pygame.draw.line(self.screen, (60, 55, 80), (px + 8, cy), (px + PW - 8, cy))
                cy += 10
                self.screen.blit(self.small.render(
                    "KNIGHTLY ORDERS OF THIS HOUSE", True, (150, 130, 180)),
                    (px + 16, cy))
                cy += 18
                for _o in _home_orders[:3]:
                    tint = _o.heraldry.primary
                    pygame.draw.rect(self.screen, tint, (px + 24, cy + 2, 10, 10))
                    self.screen.blit(self.small.render(
                        f"{_o.name}  ·  {_o.tradition.title()}  ·  prestige {_o.prestige}",
                        True, (200, 190, 220)), (px + 40, cy))
                    cy += 16
                    if _o.motto:
                        self.screen.blit(self.small.render(
                            f'   "{_o.motto}"', True, (160, 150, 180)),
                            (px + 40, cy))
                        cy += 14
                if len(_home_orders) > 3:
                    self.screen.blit(self.small.render(
                        f"  +{len(_home_orders) - 3} more chapters...",
                        True, (120, 115, 100)), (px + 40, cy))
                    cy += 14
                cy += 4

            # ---- Incident quest (if one is active for this dynasty's rivalry pair) ----
            _npc_rid2  = getattr(npc, "dynasty_id", None)
            _rival_rid2 = getattr(npc, "dynasty_rival_region_id", None)
            self._incident_quest_btn  = None
            self._incident_quest_side = None
            self._incident_quest_key  = None
            if _npc_rid2 is not None and _rival_rid2 is not None:
                import npc_dynasty as _dyn_iq
                _iq_key2 = _dyn_iq._rivalry_key(_npc_rid2, _rival_rid2)
                _iq2 = getattr(player, "incident_quests_active", {}).get(_iq_key2)
                if _iq2 and world.day_count <= _iq2["expires_day"]:
                    _side2 = "side_a" if _iq2["side_a"]["region_id"] == _npc_rid2 else "side_b"
                    _qdata2 = _iq2[_side2]
                    _days_left = _iq2["expires_day"] - world.day_count
                    pygame.draw.line(self.screen, (60, 55, 80), (px + 8, cy), (px + PW - 8, cy))
                    cy += 8
                    self.screen.blit(
                        self.small.render("INCIDENT QUEST", True, (210, 160, 60)), (px + 16, cy))
                    expiry_s = self.small.render(f"Expires in {_days_left} day(s)", True, (150, 120, 80))
                    self.screen.blit(expiry_s, (px + PW - expiry_s.get_width() - 16, cy))
                    cy += 18
                    for _line in _wrap_text(f'"{_iq2["incident_text"]}"', self.small, PW - 48):
                        self.screen.blit(self.small.render(_line, True, (190, 170, 110)), (px + 24, cy))
                        cy += 14
                    cy += 2
                    _attr2 = _qdata2["attr"]
                    _need2 = _qdata2["count"]
                    _have2 = len(getattr(player, _attr2, []))
                    _hcol2 = (130, 200, 100) if _have2 >= _need2 else (200, 130, 80)
                    self.screen.blit(
                        self.small.render(
                            f"Help {_qdata2['house_name']}: {_qdata2['label']}  "
                            f"({_have2}/{_need2})  · Reward: {_qdata2['reward_gold']} gold",
                            True, _hcol2),
                        (px + 24, cy))
                    cy += 18
                    if _have2 >= _need2:
                        IQ_W, IQ_H = 150, 26
                        _iq_btn = pygame.Rect(px + 24, cy, IQ_W, IQ_H)
                        pygame.draw.rect(self.screen, (50, 55, 20), _iq_btn)
                        pygame.draw.rect(self.screen, (170, 190, 60), _iq_btn, 1)
                        _iq_s = self.small.render("Aid This House", True, (220, 240, 100))
                        self.screen.blit(_iq_s, (_iq_btn.x + (IQ_W - _iq_s.get_width()) // 2,
                                                  _iq_btn.y + (IQ_H - _iq_s.get_height()) // 2))
                        cy += IQ_H + 6
                        self._incident_quest_btn  = _iq_btn
                        self._incident_quest_side = _side2
                        self._incident_quest_key  = _iq_key2

        pygame.draw.line(self.screen, (60, 55, 80), (px + 8, cy), (px + PW - 8, cy))
        cy += 10

        npc_uid = getattr(npc, "npc_uid", None) or ""
        rel_score = player.npc_relationships.get(npc_uid, 0)
        tier_name, tier_col = npc_prefs_mod.relationship_tier(rel_score)

        self.screen.blit(self.small.render("RELATIONSHIP", True, (110, 110, 160)), (px + 16, cy))
        cy += 18

        BAR_W, BAR_H = PW - 160, 14
        bar_x = px + 24
        pygame.draw.rect(self.screen, (35, 30, 45), (bar_x, cy, BAR_W, BAR_H))
        filled = int((rel_score + 100) / 200 * BAR_W)
        if filled > 0:
            pygame.draw.rect(self.screen, tier_col, (bar_x, cy, filled, BAR_H))
        pygame.draw.rect(self.screen, (80, 70, 100), (bar_x, cy, BAR_W, BAR_H), 1)
        tier_s = self.small.render(f"{tier_name}  ({rel_score:+d})", True, tier_col)
        self.screen.blit(tier_s, (bar_x + BAR_W + 8, cy))
        cy += BAR_H + 10

        pygame.draw.line(self.screen, (60, 55, 80), (px + 8, cy), (px + PW - 8, cy))
        cy += 10

        prefs = getattr(npc, "preferences", None) or {}
        self.screen.blit(self.small.render("PREFERENCES", True, (110, 110, 160)), (px + 16, cy))
        cy += 18

        if rel_score >= 20:
            liked    = npc_prefs_mod.preferred_system_labels(prefs, 4)
            disliked = npc_prefs_mod.disliked_system_labels(prefs)
            if liked:
                self.screen.blit(self.small.render("Loves: " + " . ".join(liked), True, (140, 210, 120)), (px + 24, cy))
                cy += 18
            if disliked:
                self.screen.blit(self.small.render("Dislikes: " + ", ".join(disliked), True, (200, 100, 90)), (px + 24, cy))
                cy += 18
        else:
            self.screen.blit(self.small.render("Get to know them better...", True, (100, 95, 90)), (px + 24, cy))
            cy += 18

        # ---- Rumour section (Friendly tier and above) ----
        personal_tension = identity.get("personal_tension", None)
        if personal_tension and rel_score >= 50:
            pygame.draw.line(self.screen, (60, 55, 80), (px + 8, cy), (px + PW - 8, cy))
            cy += 10
            self.screen.blit(self.small.render("RUMOUR", True, (160, 120, 60)), (px + 16, cy))
            cy += 18
            rumour_text = f"Word has it that {first} {personal_tension}"
            for line in _wrap_text(rumour_text, self.small, PW - 32):
                self.screen.blit(self.small.render(line, True, (165, 150, 105)), (px + 24, cy))
                cy += 16
            cy += 4

        # ---- Active request section ----
        npc_uid2 = getattr(npc, "npc_uid", None) or ""
        active_req = getattr(player, "npc_requests", {}).get(npc_uid2)
        if active_req:
            pygame.draw.line(self.screen, (60, 55, 80), (px + 8, cy), (px + PW - 8, cy))
            cy += 10
            self.screen.blit(self.small.render("REQUEST", True, (200, 175, 90)), (px + 16, cy))
            cy += 18
            hint_lines = _wrap_text(f'"{active_req["hint_label"]}"', self.small, PW - 48)
            for line in hint_lines:
                self.screen.blit(self.small.render(line, True, (195, 185, 135)), (px + 24, cy))
                cy += 16
            reward_s = self.small.render(f"Reward: {active_req['reward_gold']} gold", True, (180, 210, 130))
            self.screen.blit(reward_s, (px + 24, cy))
            cy += 18

        self._inspect_scroll_max = max(0, cy + scroll_offset - scroll_bottom + 20)
        self.screen.set_clip(None)
        if self._inspect_scroll_max > 0:
            sb_total = scroll_bottom - scroll_top
            sb_h = max(20, sb_total * sb_total // (sb_total + self._inspect_scroll_max))
            sb_y  = scroll_top + int(scroll_offset / max(1, self._inspect_scroll_max) * (sb_total - sb_h))
            pygame.draw.rect(self.screen, (40, 36, 55), (px + PW - 7, scroll_top, 5, sb_total))
            pygame.draw.rect(self.screen, (120, 110, 150), (px + PW - 7, sb_y, 5, sb_h))

        # ---- Buttons ----
        BTN_W, BTN_H = 100, 28
        close_rect   = pygame.Rect(px + PW - BTN_W - 12, py + PH - BTN_H - 12, BTN_W, BTN_H)
        gift_rect    = pygame.Rect(px + PW - BTN_W * 2 - 20, py + PH - BTN_H - 12, BTN_W, BTN_H)
        fulfill_rect = pygame.Rect(px + PW - BTN_W * 3 - 28, py + PH - BTN_H - 12, BTN_W, BTN_H)
        # History button — left side, only for dynasty rulers
        history_rect = (pygame.Rect(px + 12, py + PH - BTN_H - 12, BTN_W, BTN_H)
                        if dynasty_name else None)

        pygame.draw.rect(self.screen, (40, 55, 40), gift_rect)
        pygame.draw.rect(self.screen, (80, 130, 80), gift_rect, 1)
        g_s = self.small.render("Gift", True, (160, 220, 140))
        self.screen.blit(g_s, (gift_rect.x + (BTN_W - g_s.get_width()) // 2,
                                gift_rect.y + (BTN_H - g_s.get_height()) // 2))

        if active_req:
            pygame.draw.rect(self.screen, (55, 50, 25), fulfill_rect)
            pygame.draw.rect(self.screen, (160, 140, 60), fulfill_rect, 1)
            f_s = self.small.render("Fulfill", True, (230, 210, 120))
            self.screen.blit(f_s, (fulfill_rect.x + (BTN_W - f_s.get_width()) // 2,
                                    fulfill_rect.y + (BTN_H - f_s.get_height()) // 2))
        else:
            fulfill_rect = None

        pygame.draw.rect(self.screen, (40, 35, 50), close_rect)
        pygame.draw.rect(self.screen, (100, 90, 120), close_rect, 1)
        c_s = self.small.render("Close", True, (200, 190, 210))
        self.screen.blit(c_s, (close_rect.x + (BTN_W - c_s.get_width()) // 2,
                                close_rect.y + (BTN_H - c_s.get_height()) // 2))
        if history_rect:
            pygame.draw.rect(self.screen, (30, 40, 55), history_rect)
            pygame.draw.rect(self.screen, (70, 110, 150), history_rect, 1)
            h_s = self.small.render("History", True, (140, 190, 220))
            self.screen.blit(h_s, (history_rect.x + (BTN_W - h_s.get_width()) // 2,
                                    history_rect.y + (BTN_H - h_s.get_height()) // 2))

        self._inspect_gift_btn    = gift_rect
        self._inspect_close_btn   = close_rect
        self._inspect_fulfill_btn = fulfill_rect
        self._inspect_history_btn = history_rect
        self._inspect_sketch_btn  = sketch_rect

    def _resolve_npc_name(self, npc_uid, world):
        for e in world.entities:
            if getattr(e, "npc_uid", None) == npc_uid:
                ident = getattr(e, "identity", None) or {}
                name = ident.get("display_name", npc_uid)
                role = getattr(e, "display_name", "")
                return f"{name}" + (f" ({role})" if role else "")
        return npc_uid

    def _draw_dynasty_chronicle(self, player, world):
        npc = getattr(player, "inspecting_npc", None)
        if npc is None:
            return

        chronicle = getattr(npc, "dynasty_chronicle", None)
        if not chronicle:
            return

        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        self.screen.blit(overlay, (0, 0))

        PW, PH = 700, 760
        px = (SCREEN_W - PW) // 2
        py = (SCREEN_H - PH) // 2

        pygame.draw.rect(self.screen, (12, 12, 20), (px, py, PW, PH))
        pygame.draw.rect(self.screen, (70, 110, 150), (px, py, PW, PH), 2)

        dynasty_name  = getattr(npc, "dynasty_name", "Unknown House")
        dynasty_rival = getattr(npc, "dynasty_rival", None)
        npc_uid       = getattr(npc, "npc_uid", "") or ""
        rel_score     = player.npc_relationships.get(npc_uid, 0)
        identity      = getattr(npc, "identity", None) or {}

        import npc_dynasty as _dyn

        # ---- Fixed header (drawn directly to screen) ----
        cy = py + 14
        title_s = self.font.render(dynasty_name.upper(), True, (220, 200, 130))
        self.screen.blit(title_s, (px + 14, cy))
        cy += 28

        region_id = getattr(npc, "dynasty_id", None)
        favor     = _dyn.calculate_dynasty_favor(player, region_id, world) if region_id is not None else 0
        tier      = _dyn.favor_tier(favor)
        BAR_W, BAR_H = PW - 160, 12
        bar_x = px + 14
        pygame.draw.rect(self.screen, (30, 28, 35), (bar_x, cy, BAR_W, BAR_H))
        filled = int((favor + 100) / 200 * BAR_W)
        if filled > 0:
            pygame.draw.rect(self.screen, tier["color"], (bar_x, cy, max(filled, 2), BAR_H))
        pygame.draw.rect(self.screen, (70, 65, 80), (bar_x, cy, BAR_W, BAR_H), 1)
        tier_s = self.small.render(f"Favor: {tier['name']}  ({favor:+d})", True, tier["color"])
        self.screen.blit(tier_s, (bar_x + BAR_W + 8, cy))
        cy += BAR_H + 4
        if tier["perk"]:
            for line in _wrap_text(tier["perk"], self.small, PW - 32):
                self.screen.blit(self.small.render(line, True, (120, 115, 95)), (px + 14, cy))
                cy += 14
        cy += 8
        content_top = cy  # where the scrollable area begins on screen

        # ---- Fixed back button ----
        BTN_W, BTN_H = 100, 28
        back_rect = pygame.Rect(px + PW - BTN_W - 12, py + PH - BTN_H - 12, BTN_W, BTN_H)
        pygame.draw.rect(self.screen, (30, 40, 55), back_rect)
        pygame.draw.rect(self.screen, (70, 110, 150), back_rect, 1)
        b_s = self.small.render("Back", True, (140, 190, 220))
        self.screen.blit(b_s, (back_rect.x + (BTN_W - b_s.get_width()) // 2,
                                back_rect.y + (BTN_H - b_s.get_height()) // 2))
        self._chronicle_back_btn = back_rect

        # ---- Family Tree button (left of Back) ----
        TREE_W = 130
        tree_rect = pygame.Rect(back_rect.x - TREE_W - 8, back_rect.y, TREE_W, BTN_H)
        pygame.draw.rect(self.screen, (35, 50, 35), tree_rect)
        pygame.draw.rect(self.screen, (130, 180, 130), tree_rect, 1)
        t_s = self.small.render("View Family Tree", True, (180, 220, 180))
        self.screen.blit(t_s, (tree_rect.x + (TREE_W - t_s.get_width()) // 2,
                                tree_rect.y + (BTN_H - t_s.get_height()) // 2))
        self._chronicle_tree_btn = tree_rect

        SB_W = 8
        SCROLL_AREA_H = (py + PH - BTN_H - 20) - content_top
        CONTENT_W = PW - SB_W - 6

        # ---- Build scrollable content onto an off-screen surface ----
        content_surf = pygame.Surface((CONTENT_W, 4000), pygame.SRCALPHA)
        content_surf.fill((0, 0, 0, 0))
        cy_c = 8

        def _section(label, col=(140, 190, 220)):
            nonlocal cy_c
            pygame.draw.line(content_surf, (45, 65, 90), (0, cy_c), (CONTENT_W - 4, cy_c))
            cy_c += 8
            content_surf.blit(self.small.render(label, True, col), (4, cy_c))
            cy_c += 20

        def _body(text, col=(190, 183, 168), indent=14):
            nonlocal cy_c
            for line in _wrap_text(text, self.small, CONTENT_W - indent - 14):
                content_surf.blit(self.small.render(line, True, col), (indent, cy_c))
                cy_c += 15
            cy_c += 4

        # ---- FOUNDING ----
        _section("THE FOUNDING")
        founder = chronicle.get("founder_full", "")
        if founder:
            content_surf.blit(self.small.render(f'"{founder}"', True, (215, 200, 145)), (20, cy_c))
            cy_c += 18
        _body(chronicle.get("founder_act", ""), col=(185, 178, 160), indent=20)
        _body(chronicle.get("founder_legacy", ""), col=(155, 148, 130), indent=20)

        # ---- SECOND GENERATION ----
        _section("THE SECOND GENERATION")
        _body(chronicle.get("gen2", ""), indent=20)

        # ---- THIRD GENERATION ----
        gen3 = chronicle.get("gen3", "")
        if gen3:
            _section("THE THIRD GENERATION")
            _body(gen3, indent=20)

        # ---- FIVE CENTURIES OF HISTORY (real sim chronicle) ----
        kingdom_summary = chronicle.get("kingdom_summary", "")
        kingdom_events = chronicle.get("kingdom_events", []) or []
        dynasty_events = chronicle.get("dynasty_events", []) or []
        dynasty_arc = chronicle.get("dynasty_arc", "")
        if kingdom_summary or kingdom_events or dynasty_events:
            _section("FIVE CENTURIES OF HISTORY")
            if kingdom_summary:
                _body(kingdom_summary, col=(200, 190, 165), indent=20)
            if dynasty_arc:
                _body(dynasty_arc, col=(165, 175, 160), indent=20)
            # Show interleaved kingdom + dynasty events, ordered by year, last 14
            combined = []
            for line in kingdom_events:
                combined.append(("k", line))
            for line in dynasty_events:
                combined.append(("d", line))
            # naive sort by leading "Yr N" prefix
            def _yr(t):
                try:
                    return int(t[1].split()[1])
                except Exception:
                    return 0
            combined.sort(key=_yr)
            shown = combined[-14:]
            for tag, line in shown:
                col = (180, 175, 165) if tag == "k" else (170, 180, 195)
                _body(line, col=col, indent=20)

        # ---- TODAY ----
        _section("TODAY")
        house_trait = chronicle.get("house_trait", "")
        if house_trait:
            _body(house_trait, col=(160, 155, 130), indent=20)
        _body(chronicle.get("current_era", ""), indent=20)
        house_saying = chronicle.get("house_saying", "")
        if house_saying:
            _body(house_saying, col=(130, 125, 105), indent=20)
        dynasty_tension = getattr(npc, "dynasty_tension", None)
        if dynasty_tension:
            _body(dynasty_tension, col=(200, 140, 110), indent=20)
        cy_c += 4

        content_surf.blit(self.small.render("Members of the house:", True, (130, 125, 115)), (20, cy_c))
        cy_c += 17
        npc_display  = identity.get("display_name", "?")
        npc_role_str = getattr(npc, "dynasty_role", "").title()
        from towns import TOWNS
        npc_town = TOWNS.get(getattr(npc, "town_id", -1))
        npc_town_name = npc_town.name if npc_town else "Unknown"
        content_surf.blit(
            self.small.render(f"  {npc_display}  ·  {npc_role_str}  ·  {npc_town_name}", True, (230, 215, 160)),
            (20, cy_c))
        cy_c += 16
        ambition = getattr(npc, "dynasty_ambition", None)
        if ambition:
            for line in _wrap_text(f'    "{ambition}"', self.small, CONTENT_W - 48):
                content_surf.blit(self.small.render(line, True, (155, 148, 115)), (20, cy_c))
                cy_c += 14
            cy_c += 4
        for kin in getattr(npc, "dynasty_kin", []):
            kin_line = (f"  {kin['display_name']}  ·  {kin['dynasty_role'].title()}"
                        f"  ·  {kin['town_name']}")
            content_surf.blit(self.small.render(kin_line, True, (190, 183, 155)), (20, cy_c))
            cy_c += 16
        cy_c += 4

        # ---- RIVALRY ----
        rivalry_text = chronicle.get("rivalry_text")
        rival_rid_chronicle = getattr(npc, "dynasty_rival_region_id", None)
        if rivalry_text and dynasty_rival:
            _section(f"RIVALRY WITH {dynasty_rival.upper()}", col=(200, 110, 90))
            _body(rivalry_text, col=(195, 160, 145), indent=20)
            if region_id is not None and rival_rid_chronicle is not None:
                _rkey_c = _dyn._rivalry_key(region_id, rival_rid_chronicle)
                _tlabel_c, _tcol_c = _dyn.tension_label(player, _rkey_c)
                content_surf.blit(
                    self.small.render(f"Current tension: {_tlabel_c}", True, _tcol_c),
                    (20, cy_c))
                cy_c += 16

        # ---- BROKER PEACE ----
        _peace_btn_cy = None
        self._peace_quest_data = None
        if region_id is not None and rival_rid_chronicle is not None:
            if _dyn.can_broker_peace(player, region_id, rival_rid_chronicle, world):
                world_seed_p = getattr(world, "seed", 0)
                pq = _dyn.generate_peace_quest(region_id, rival_rid_chronicle, world_seed_p)
                _section("BROKER PEACE", col=(140, 190, 220))
                _body(
                    f"As a Champion trusted by both houses, you could deliver {pq['label']} "
                    f"as a formal gesture. If accepted, hostilities would pause for 60 days.",
                    col=(170, 200, 210), indent=20)
                _phave = len(getattr(player, pq["attr"], []))
                _pneed = pq["count"]
                _phcol = (130, 200, 100) if _phave >= _pneed else (200, 130, 80)
                content_surf.blit(
                    self.small.render(
                        f"You have {_phave} / {_pneed}  ·  Reward: {pq['reward_gold']} gold  "
                        f"·  Rival incidents pause 60 days",
                        True, _phcol),
                    (20, cy_c))
                cy_c += 18
                if _phave >= _pneed:
                    PQ_W, PQ_H = 150, 26
                    _pbtn_c = pygame.Rect(20, cy_c, PQ_W, PQ_H)
                    pygame.draw.rect(content_surf, (20, 45, 55), _pbtn_c)
                    pygame.draw.rect(content_surf, (80, 160, 200), _pbtn_c, 1)
                    _ps = self.small.render("Broker Peace", True, (160, 220, 240))
                    content_surf.blit(_ps, (_pbtn_c.x + (PQ_W - _ps.get_width()) // 2,
                                            _pbtn_c.y + (PQ_H - _ps.get_height()) // 2))
                    _peace_btn_cy = cy_c
                    cy_c += PQ_H + 6
                    self._peace_quest_data = pq

        # ---- DARK SECRET (Beloved only) ----
        _section("THE HIDDEN TRUTH", col=(120, 100, 140))
        if rel_score >= 80:
            dark = chronicle.get("dark_secret", "")
            _body(dark, col=(175, 155, 185), indent=20)
        else:
            content_surf.blit(
                self.small.render("Reach Beloved to learn what those closest to the house will say.",
                                  True, (90, 85, 100)),
                (20, cy_c))
            cy_c += 16

        # ---- Dynasty Quest (Champion only, head of house, not yet completed) ----
        world_seed  = getattr(world, "seed", 0)
        completed   = getattr(player, "dynasty_quests_completed", set())
        is_champion = region_id in getattr(player, "champion_dynasty_regions", set())
        _quest_btn_cy = None
        quest = None
        if is_champion and region_id not in completed:
            quest = _dyn.generate_dynasty_quest(region_id, world_seed)
            attr  = quest["attr"]
            need  = quest["count"]
            have  = len(getattr(player, attr, []))
            _section("DYNASTY QUEST", col=(220, 190, 80))
            content_surf.blit(
                self.small.render(f"The house requires: {quest['label']}.", True, (210, 195, 145)),
                (20, cy_c))
            cy_c += 16
            have_col = (130, 200, 100) if have >= need else (200, 130, 80)
            content_surf.blit(
                self.small.render(f"You have {have} / {need}  ·  Reward: {quest['gold']} gold",
                                  True, have_col),
                (20, cy_c))
            cy_c += 18
            if have >= need:
                BTN_W2, BTN_H2 = 140, 26
                _qbtn_c = pygame.Rect(20, cy_c, BTN_W2, BTN_H2)
                pygame.draw.rect(content_surf, (50, 60, 25), _qbtn_c)
                pygame.draw.rect(content_surf, (160, 200, 60), _qbtn_c, 1)
                qf_s = self.small.render("Fulfill Dynasty Quest", True, (200, 240, 100))
                content_surf.blit(qf_s, (_qbtn_c.x + (BTN_W2 - qf_s.get_width()) // 2,
                                         _qbtn_c.y + (BTN_H2 - qf_s.get_height()) // 2))
                _quest_btn_cy = cy_c
                cy_c += BTN_H2 + 6
        self._chronicle_quest_data = quest if (is_champion and region_id not in completed) else None

        content_h = cy_c + 8

        # ---- Scroll state ----
        if not hasattr(self, "_chronicle_scroll"):
            self._chronicle_scroll = 0
        max_scroll = max(0, content_h - SCROLL_AREA_H)
        self._chronicle_scroll = max(0, min(max_scroll, self._chronicle_scroll))
        self._chronicle_max_scroll = max_scroll
        scroll = self._chronicle_scroll

        # ---- Clip and blit content surface ----
        clip_rect = pygame.Rect(0, scroll, CONTENT_W, SCROLL_AREA_H)
        self.screen.blit(content_surf, (px, content_top), clip_rect)

        # ---- Scrollbar ----
        if max_scroll > 0:
            sb_x = px + PW - SB_W - 2
            pygame.draw.rect(self.screen, (25, 28, 38), (sb_x, content_top, SB_W, SCROLL_AREA_H))
            thumb_h = max(20, int(SCROLL_AREA_H * SCROLL_AREA_H / content_h))
            thumb_y = content_top + int(scroll / max_scroll * (SCROLL_AREA_H - thumb_h))
            pygame.draw.rect(self.screen, (70, 110, 145), (sb_x, thumb_y, SB_W, thumb_h))

        # ---- Convert content-space button positions to screen rects ----
        def _to_screen_rect(content_y, w, h):
            sy = content_top + content_y - scroll
            if sy < content_top or sy + h > content_top + SCROLL_AREA_H:
                return None
            return pygame.Rect(px + 20, sy, w, h)

        self._peace_quest_btn   = _to_screen_rect(_peace_btn_cy, 150, 26) if _peace_btn_cy is not None else None
        self._chronicle_quest_btn = _to_screen_rect(_quest_btn_cy, 140, 26) if _quest_btn_cy is not None else None

    def _draw_npc_gift(self, player, world):
        import npc_preferences as npc_prefs_mod
        npc = getattr(player, "inspecting_npc", None)
        if npc is None:
            return
        PW, PH = 560, 480
        px = (SCREEN_W - PW) // 2
        py = (SCREEN_H - PH) // 2
        pygame.draw.rect(self.screen, (14, 14, 20), (px, py, PW, PH))
        pygame.draw.rect(self.screen, (70, 130, 70), (px, py, PW, PH), 2)
        title_name = (getattr(npc, "identity", None) or {}).get("first_name", "NPC")
        title_s = self.font.render(f"Gift to {title_name}", True, (210, 200, 160))
        self.screen.blit(title_s, (px + 16, py + 14))
        hint = self.small.render("Click item to give . ESC to cancel", True, (90, 90, 100))
        self.screen.blit(hint, (px + PW - hint.get_width() - 8, py + 16))
        prefs = getattr(npc, "preferences", None) or {}
        giftable = self._gather_giftable_items(player)
        scored = sorted(giftable, key=lambda x: npc_prefs_mod.score_gift(prefs, x[1]), reverse=True)
        ROW_H = 38
        area_top = py + 52
        max_rows = (PH - 70) // ROW_H
        self._gift_item_rects = {}
        for i, (label, item) in enumerate(scored[:max_rows]):
            raw_score = npc_prefs_mod.score_gift(prefs, item)
            tier_label, tier_col = npc_prefs_mod.gift_tier_label(raw_score)
            ry = area_top + i * ROW_H
            rect = pygame.Rect(px + 8, ry, PW - 16, ROW_H - 4)
            bg = (25, 35, 25) if raw_score > 0.1 else (35, 25, 25) if raw_score < -0.1 else (28, 28, 30)
            pygame.draw.rect(self.screen, bg, rect)
            pygame.draw.rect(self.screen, (55, 50, 65), rect, 1)
            name_s = self.small.render(label, True, (210, 200, 180))
            self.screen.blit(name_s, (rect.x + 8, rect.y + (ROW_H - 4 - name_s.get_height()) // 2))
            tier_s = self.small.render(tier_label, True, tier_col)
            self.screen.blit(tier_s, (rect.right - tier_s.get_width() - 8,
                                       rect.y + (ROW_H - 4 - tier_s.get_height()) // 2))
            self._gift_item_rects[i] = (rect, item)
        if not scored:
            empty_s = self.small.render("Nothing to give right now.", True, (130, 120, 100))
            self.screen.blit(empty_s, (px + PW // 2 - empty_s.get_width() // 2, py + PH // 2))

    def _draw_npc_fulfill_request(self, player, world):
        import npc_preferences as npc_prefs_mod
        npc = getattr(player, "inspecting_npc", None)
        if npc is None:
            return
        uid = getattr(npc, "npc_uid", None) or ""
        request = getattr(player, "npc_requests", {}).get(uid)
        if request is None:
            player.fulfill_request_open = False
            return
        PW, PH = 560, 480
        px = (SCREEN_W - PW) // 2
        py = (SCREEN_H - PH) // 2
        pygame.draw.rect(self.screen, (14, 14, 18), (px, py, PW, PH))
        pygame.draw.rect(self.screen, (160, 140, 60), (px, py, PW, PH), 2)
        first_name = (getattr(npc, "identity", None) or {}).get("first_name", "NPC")
        title_s = self.font.render(f"Fulfill {first_name}'s Request", True, (230, 210, 120))
        self.screen.blit(title_s, (px + 16, py + 14))
        hint_lines = _wrap_text(f'"{request["hint_label"]}"', self.small, PW - 32)
        hy = py + 44
        for line in hint_lines:
            self.screen.blit(self.small.render(line, True, (195, 185, 135)), (px + 16, hy))
            hy += 16
        reward_s = self.small.render(f"Reward: {request['reward_gold']} gold", True, (180, 210, 130))
        self.screen.blit(reward_s, (px + 16, hy))
        cancel_hint = self.small.render("Click item to fulfill . ESC to cancel", True, (90, 90, 100))
        self.screen.blit(cancel_hint, (px + PW - cancel_hint.get_width() - 8, py + 16))

        system_id = request.get("system_id", "")
        giftable = self._gather_giftable_items(player)
        prefs = getattr(npc, "preferences", None) or {}
        matching = [(lbl, item) for lbl, item in giftable
                    if _item_matches_system(item, system_id)]
        if not matching:
            matching = giftable  # fallback: show everything
        scored = sorted(matching, key=lambda x: npc_prefs_mod.score_gift(prefs, x[1]), reverse=True)
        ROW_H = 38
        area_top = hy + 22
        max_rows = max(1, (py + PH - area_top - 16) // ROW_H)
        self._fulfill_item_rects = {}
        for i, (label, item) in enumerate(scored[:max_rows]):
            raw_score = npc_prefs_mod.score_gift(prefs, item)
            tier_label, tier_col = npc_prefs_mod.gift_tier_label(raw_score)
            ry = area_top + i * ROW_H
            rect = pygame.Rect(px + 8, ry, PW - 16, ROW_H - 4)
            bg = (30, 40, 20) if raw_score > 0.1 else (40, 28, 20) if raw_score < -0.1 else (28, 28, 30)
            pygame.draw.rect(self.screen, bg, rect)
            pygame.draw.rect(self.screen, (100, 90, 40), rect, 1)
            name_s = self.small.render(label, True, (210, 200, 180))
            self.screen.blit(name_s, (rect.x + 8, rect.y + (ROW_H - 4 - name_s.get_height()) // 2))
            tier_s = self.small.render(tier_label, True, tier_col)
            self.screen.blit(tier_s, (rect.right - tier_s.get_width() - 8,
                                       rect.y + (ROW_H - 4 - tier_s.get_height()) // 2))
            self._fulfill_item_rects[i] = (rect, item)
        if not scored:
            empty_s = self.small.render("Nothing matching in your inventory.", True, (130, 120, 100))
            self.screen.blit(empty_s, (px + PW // 2 - empty_s.get_width() // 2, py + PH // 2))

    def _gather_giftable_items(self, player):
        items = []
        for fish in getattr(player, "fish_caught", []):
            items.append((f"Fish: {fish.species.title()} ({fish.rarity})", fish))
        for fossil in getattr(player, "fossils", []):
            items.append((f"Fossil: {fossil.fossil_type.replace('_', ' ').title()} ({fossil.rarity})", fossil))
        for rock in getattr(player, "rocks", []):
            items.append((f"Rock: {rock.base_type.replace('_', ' ').title()} ({rock.rarity})", rock))
        for gem in getattr(player, "gems", []):
            items.append((f"Gem: {gem.gem_type.replace('_', ' ').title()} ({gem.rarity})", gem))
        for wf in getattr(player, "wildflowers", []):
            items.append((f"Flower: {wf.flower_type.replace('_', ' ').title()} ({wf.rarity})", wf))
        for grape in getattr(player, "wine_grapes", []):
            if getattr(grape, "state", "") in ("fermented", "aged", "blended"):
                items.append((f"Wine: {grape.style.title()} from {grape.origin_biome}", grape))
        for bean in getattr(player, "coffee_beans", []):
            if getattr(bean, "state", "") in ("roasted", "blended"):
                items.append((f"Coffee: {bean.roast_level.title()} roast", bean))
        for leaf in getattr(player, "tea_leaves", []):
            if getattr(leaf, "state", "") in ("oxidized", "brewed", "blended"):
                label = f"Tea: {leaf.tea_type.title()}" if hasattr(leaf, "tea_type") else "Tea"
                items.append((label, leaf))
        for spirit in getattr(player, "spirits", []):
            if getattr(spirit, "state", "") in ("aged", "blended"):
                items.append((f"Spirit: {spirit.spirit_type.title()}", spirit))
        for cheese in getattr(player, "cheese_wheels", []):
            if getattr(cheese, "state", "") in ("pressed", "aged"):
                items.append((f"Cheese: {cheese.cheese_type.replace('_', ' ').title()}", cheese))
        for pot in getattr(player, "pottery_pieces", []):
            if getattr(pot, "state", "") in ("fired", "glazed"):
                items.append((f"Pottery: {pot.shape.title()} ({pot.firing_level})", pot))
        for salt in getattr(player, "salt_crystals", []):
            if getattr(salt, "state", "") == "finished":
                items.append((f"Salt: {salt.refine_grade.replace('_', ' ').title()}", salt))
        for weapon in getattr(player, "crafted_weapons", []):
            items.append((f"Weapon: {weapon.weapon_type.title()}", weapon))
        for textile in getattr(player, "textiles", []):
            if getattr(textile, "state", "") == "woven":
                items.append((f"Textile: {textile.output_type.replace('_', ' ').title()}", textile))
        for jewel in getattr(player, "jewelry", []):
            items.append((f"Jewelry: {jewel.jewelry_type.title()}", jewel))
        from items import ITEMS
        for item_id, count in player.inventory.items():
            if count > 0:
                data = ITEMS.get(item_id, {})
                if data.get("edible"):
                    items.append((f"Food: {data.get('name', item_id)} x{count}", (item_id, count)))
        return items

    def handle_inspect_click(self, pos, player, world):
        import npc_preferences as npc_prefs_mod

        # ---- Fulfill-request sub-panel ----
        if getattr(player, "fulfill_request_open", False):
            for i, (rect, item) in getattr(self, "_fulfill_item_rects", {}).items():
                if rect.collidepoint(pos):
                    npc = player.inspecting_npc
                    delta, gold = npc_prefs_mod.fulfill_request(player, npc, item, world)
                    self._remove_gifted_item(player, item)
                    player.pending_notifications.append(
                        ("Gift", f"Request fulfilled! +{gold} gold  ({delta:+d} rep)", "rare")
                    )
                    player.fulfill_request_open = False
                    return
            player.fulfill_request_open = False
            return

        # ---- Gift sub-panel ----
        if getattr(player, "gift_panel_open", False):
            for i, (rect, item) in getattr(self, "_gift_item_rects", {}).items():
                if rect.collidepoint(pos):
                    npc = player.inspecting_npc
                    delta, label = npc_prefs_mod.apply_gift(player, npc, item, world)
                    self._remove_gifted_item(player, item)
                    player.pending_notifications.append(("Gift", f"{label}  ({delta:+d})", "common"))
                    player.gift_panel_open = False
                    return
            player.gift_panel_open = False
            return

        # ---- Dynasty family tree panel ----
        if getattr(player, "dynasty_tree_open", False):
            self.handle_dynasty_tree_click(pos, player)
            return

        # ---- Dynasty chronicle panel ----
        if getattr(player, "dynasty_panel_open", False):
            import npc_dynasty as _dyn
            # Peace quest button
            peace_btn  = getattr(self, "_peace_quest_btn",  None)
            peace_data = getattr(self, "_peace_quest_data", None)
            if peace_btn and peace_data and peace_btn.collidepoint(pos):
                npc = player.inspecting_npc
                rid_a  = getattr(npc, "dynasty_id", None)
                rid_b  = getattr(npc, "dynasty_rival_region_id", None)
                attr   = peace_data["attr"]
                need   = peace_data["count"]
                lst    = getattr(player, attr, [])
                if rid_a is not None and rid_b is not None and len(lst) >= need:
                    del lst[:need]
                    _dyn.fulfill_peace_quest(player, rid_a, rid_b, world)
                return
            quest_btn  = getattr(self, "_chronicle_quest_btn",  None)
            quest_data = getattr(self, "_chronicle_quest_data", None)
            if quest_btn and quest_data and quest_btn.collidepoint(pos):
                npc       = player.inspecting_npc
                region_id = getattr(npc, "dynasty_id", None)
                attr      = quest_data["attr"]
                need      = quest_data["count"]
                lst       = getattr(player, attr, [])
                if region_id is not None and len(lst) >= need:
                    del lst[:need]
                    player.money += quest_data["gold"]
                    if not hasattr(player, "dynasty_quests_completed"):
                        player.dynasty_quests_completed = set()
                    player.dynasty_quests_completed.add(region_id)
                    dynasty_name = getattr(npc, "dynasty_name", "the house")
                    player.pending_notifications.append((
                        "Dynasty",
                        f"Dynasty Quest complete! {dynasty_name} grants you {quest_data['gold']} gold.",
                        "epic",
                    ))
                return
            tree_btn = getattr(self, "_chronicle_tree_btn", None)
            if tree_btn and tree_btn.collidepoint(pos):
                player.dynasty_tree_open = True
                self.open_dynasty_tree(player.inspecting_npc)
                return
            back_btn = getattr(self, "_chronicle_back_btn", None)
            if back_btn is None or back_btn.collidepoint(pos):
                player.dynasty_panel_open = False
            return

        # ---- Incident quest button ----
        iq_btn = getattr(self, "_incident_quest_btn", None)
        if iq_btn and iq_btn.collidepoint(pos):
            import npc_dynasty as _dyn_click
            side = getattr(self, "_incident_quest_side", None)
            key  = getattr(self, "_incident_quest_key",  None)
            if side and key:
                iq = getattr(player, "incident_quests_active", {}).get(key)
                if iq:
                    qdata = iq[side]
                    attr  = qdata["attr"]
                    need  = qdata["count"]
                    lst   = getattr(player, attr, [])
                    if len(lst) >= need:
                        del lst[:need]
                        _dyn_click.fulfill_incident_quest(player, side, key, world)
            return

        # ---- Main inspect panel buttons ----
        fulfill_btn = getattr(self, "_inspect_fulfill_btn", None)
        if fulfill_btn and fulfill_btn.collidepoint(pos):
            player.fulfill_request_open = True
            return
        history_btn = getattr(self, "_inspect_history_btn", None)
        if history_btn and history_btn.collidepoint(pos):
            player.dynasty_panel_open = True
            self._chronicle_scroll = 0
            return
        if hasattr(self, "_inspect_gift_btn") and self._inspect_gift_btn.collidepoint(pos):
            player.gift_panel_open = True
            return
        if hasattr(self, "_inspect_close_btn") and self._inspect_close_btn.collidepoint(pos):
            player.inspecting_npc = None
            player.gift_panel_open = False
            player.fulfill_request_open = False
            player.dynasty_panel_open = False
            player.dynasty_tree_open = False
            return

        sketch_btn = getattr(self, "_inspect_sketch_btn", None)
        if sketch_btn and sketch_btn.collidepoint(pos):
            npc = player.inspecting_npc
            biodome = getattr(npc, "biodome", "unknown")
            location = biodome.replace("_", " ").title()
            sketch = sketch_from_npc(npc, location)
            player.guard_sketches.append(sketch)
            player.pending_notifications.append(
                ("Guards", f"Sketched {sketch.name} — {sketch.kit.title()}", "common")
            )
            return

    def _remove_gifted_item(self, player, item):
        from fish import Fish
        from fossils import Fossil
        from rocks import Rock
        from gemstones import Gemstone

        def _try_remove(lst, obj):
            try:
                lst.remove(obj)
            except (ValueError, AttributeError):
                pass

        if isinstance(item, Fish):
            _try_remove(player.fish_caught, item)
        elif isinstance(item, Fossil):
            _try_remove(player.fossils, item)
        elif isinstance(item, Rock):
            _try_remove(player.rocks, item)
        elif isinstance(item, Gemstone):
            _try_remove(player.gems, item)
        elif isinstance(item, tuple) and len(item) == 2:
            item_id, _ = item
            if player.inventory.get(item_id, 0) > 0:
                player.inventory[item_id] -= 1
        else:
            for attr in ("wine_grapes", "coffee_beans", "tea_leaves", "spirits",
                         "cheese_wheels", "pottery_pieces", "salt_crystals",
                         "crafted_weapons", "textiles", "jewelry", "wildflowers"):
                lst = getattr(player, attr, None)
                if lst is not None and item in lst:
                    _try_remove(lst, item)
                    break

    # =========================================================================
    # Pipe layer panels
    # =========================================================================

    def _draw_hopper(self, player, world):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        PW, PH = 500, 280
        px = (SCREEN_W - PW) // 2
        py = (SCREEN_H - PH) // 2
        pygame.draw.rect(self.screen, (22, 18, 12), (px, py, PW, PH))
        pygame.draw.rect(self.screen, (140, 100, 60), (px, py, PW, PH), 2)

        title = self.font.render("HOPPER", True, (220, 170, 80))
        self.screen.blit(title, (px + PW // 2 - title.get_width() // 2, py + 10))

        bx, by = self.active_hopper_pos
        cfg = world.pipe_state.get((bx, by), {})
        pull_rate = cfg.get("pull_rate", 1)

        # Pull rate control
        rate_label = self.font.render(f"Pull Rate: {pull_rate}", True, (210, 200, 180))
        self.screen.blit(rate_label, (px + 20, py + 55))
        bw = 30
        minus_r = pygame.Rect(px + 210, py + 52, bw, 26)
        plus_r  = pygame.Rect(px + 250, py + 52, bw, 26)
        for r, lbl in ((minus_r, "-"), (plus_r, "+")):
            pygame.draw.rect(self.screen, (60, 50, 38), r)
            pygame.draw.rect(self.screen, (140, 100, 60), r, 1)
            s = self.font.render(lbl, True, (220, 200, 160))
            self.screen.blit(s, (r.x + r.w // 2 - s.get_width() // 2,
                                 r.y + r.h // 2 - s.get_height() // 2))
        self._hopper_rate_minus = minus_r
        self._hopper_rate_plus  = plus_r

        # Source contents
        from pipes import _get_container
        source = _get_container(world, bx, by - 1)
        src_label = self.small.render("Source above:", True, (160, 140, 110))
        self.screen.blit(src_label, (px + 20, py + 95))
        if source:
            items_str = "  ".join(f"{ITEMS.get(k, {}).get('name', k)} x{v}"
                                  for k, v in list(source.items())[:5])
            ts = self.small.render(items_str or "(empty)", True, (180, 200, 160))
        else:
            ts = self.small.render("(nothing above)", True, (120, 100, 80))
        self.screen.blit(ts, (px + 20, py + 115))

        # Buffer contents
        buf = world.pipe_buffers.get((bx, by), {})
        buf_label = self.small.render("Buffer:", True, (160, 140, 110))
        self.screen.blit(buf_label, (px + 20, py + 145))
        buf_str = "  ".join(f"{ITEMS.get(k, {}).get('name', k)} x{v}"
                             for k, v in list(buf.items())[:5])
        bs = self.small.render(buf_str or "(empty)", True, (180, 200, 160))
        self.screen.blit(bs, (px + 20, py + 165))

        # Wire status
        from pipes import _wire_disabled
        wire_st = "Disabled by wire" if _wire_disabled(world, bx, by) else "Active"
        ws = self.small.render(f"Wire: {wire_st}", True, (120, 180, 220))
        self.screen.blit(ws, (px + 20, py + 205))

        close_r = pygame.Rect(px + PW - 90, py + PH - 40, 80, 28)
        pygame.draw.rect(self.screen, (60, 40, 30), close_r)
        pygame.draw.rect(self.screen, (140, 80, 50), close_r, 1)
        cs = self.small.render("Close [E]", True, (220, 180, 120))
        self.screen.blit(cs, (close_r.x + close_r.w // 2 - cs.get_width() // 2,
                               close_r.y + close_r.h // 2 - cs.get_height() // 2))
        self._hopper_close_btn = close_r

    def _draw_pipe_output(self, player, world):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        PW, PH = 420, 220
        px = (SCREEN_W - PW) // 2
        py = (SCREEN_H - PH) // 2
        pygame.draw.rect(self.screen, (14, 20, 28), (px, py, PW, PH))
        pygame.draw.rect(self.screen, (60, 110, 150), (px, py, PW, PH), 2)

        title = self.font.render("PIPE OUTPUT", True, (120, 180, 220))
        self.screen.blit(title, (px + PW // 2 - title.get_width() // 2, py + 10))

        bx, by = self.active_pipe_output_pos
        cfg = world.pipe_state.get((bx, by), {})
        facing = cfg.get("facing", "down")

        dirs_label = self.font.render("Output Direction:", True, (190, 190, 190))
        self.screen.blit(dirs_label, (px + 20, py + 50))

        self._po_facing_btns = {}
        directions = [("up", 0), ("down", 1), ("left", 2), ("right", 3)]
        for name, idx in directions:
            bx_btn = px + 20 + idx * 90
            by_btn = py + 80
            r = pygame.Rect(bx_btn, by_btn, 80, 30)
            active = (name == facing)
            pygame.draw.rect(self.screen, (40, 80, 110) if active else (25, 40, 55), r)
            pygame.draw.rect(self.screen, (80, 160, 210) if active else (50, 80, 100), r, 1)
            s = self.small.render(name.capitalize(), True, (220, 220, 240) if active else (140, 160, 180))
            self.screen.blit(s, (r.x + r.w // 2 - s.get_width() // 2,
                                 r.y + r.h // 2 - s.get_height() // 2))
            self._po_facing_btns[name] = r

        buf = world.pipe_buffers.get((bx, by), {})
        buf_str = "  ".join(f"{ITEMS.get(k, {}).get('name', k)} x{v}"
                             for k, v in list(buf.items())[:4])
        bl = self.small.render(f"Buffer: {buf_str or '(empty)'}", True, (170, 200, 160))
        self.screen.blit(bl, (px + 20, py + 130))

        close_r = pygame.Rect(px + PW - 90, py + PH - 38, 80, 26)
        pygame.draw.rect(self.screen, (40, 30, 20), close_r)
        pygame.draw.rect(self.screen, (80, 110, 140), close_r, 1)
        cs = self.small.render("Close [E]", True, (180, 200, 220))
        self.screen.blit(cs, (close_r.x + close_r.w // 2 - cs.get_width() // 2,
                               close_r.y + close_r.h // 2 - cs.get_height() // 2))
        self._po_close_btn = close_r

    def _draw_pipe_filter(self, player, world):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        PW, PH = 760, 420
        px = (SCREEN_W - PW) // 2
        py = (SCREEN_H - PH) // 2
        pygame.draw.rect(self.screen, (20, 16, 10), (px, py, PW, PH))
        pygame.draw.rect(self.screen, (150, 120, 70), (px, py, PW, PH), 2)

        title = self.font.render("PIPE FILTER", True, (220, 180, 80))
        self.screen.blit(title, (px + PW // 2 - title.get_width() // 2, py + 10))

        bx, by = self.active_pipe_filter_pos
        cfg = world.pipe_state.get((bx, by), {})
        allowed = cfg.get("allowed", [])

        half = (PW - 30) // 2
        lx, rx = px + 10, px + 20 + half
        pygame.draw.line(self.screen, (80, 60, 30),
                         (px + half + 15, py + 35), (px + half + 15, py + PH - 10), 1)

        # Left: allowed items
        lbl = self.small.render("Allowed (click to remove)", True, (200, 170, 90))
        self.screen.blit(lbl, (lx, py + 38))
        self._pf_item_rects = {}
        CW, CH, GAP = 200, 36, 4
        for i, item_id in enumerate(allowed):
            y = py + 60 + i * (CH + GAP) - self._pf_scroll * (CH + GAP)
            if y + CH < py + 60 or y > py + PH - 20:
                continue
            r = pygame.Rect(lx, y, CW, CH)
            pygame.draw.rect(self.screen, (45, 35, 20), r)
            pygame.draw.rect(self.screen, (160, 120, 60), r, 1)
            nm = ITEMS.get(item_id, {}).get("name", item_id)
            s = self.small.render(f"[X] {nm}", True, (220, 200, 150))
            self.screen.blit(s, (r.x + 6, r.y + r.h // 2 - s.get_height() // 2))
            self._pf_item_rects[item_id] = r

        # Right: player inventory to add
        rlbl = self.small.render("Add from inventory (click)", True, (180, 180, 180))
        self.screen.blit(rlbl, (rx, py + 38))
        self._pf_add_rects = {}
        inv_items = [(k, v) for k, v in player.inventory.items() if v > 0 and k not in allowed]
        for i, (item_id, count) in enumerate(inv_items[:12]):
            col = i % 2
            row = i // 2
            x = rx + col * (CW + GAP)
            y = py + 60 + row * (CH + GAP)
            if y + CH > py + PH - 20:
                break
            r = pygame.Rect(x, y, CW, CH)
            pygame.draw.rect(self.screen, (30, 28, 20), r)
            pygame.draw.rect(self.screen, (100, 90, 60), r, 1)
            nm = ITEMS.get(item_id, {}).get("name", item_id)
            s = self.small.render(f"{nm} x{count}", True, (200, 210, 180))
            self.screen.blit(s, (r.x + 6, r.y + r.h // 2 - s.get_height() // 2))
            self._pf_add_rects[item_id] = r

        close_r = pygame.Rect(px + PW - 90, py + PH - 38, 80, 26)
        pygame.draw.rect(self.screen, (45, 32, 18), close_r)
        pygame.draw.rect(self.screen, (140, 100, 50), close_r, 1)
        cs = self.small.render("Close [E]", True, (210, 180, 110))
        self.screen.blit(cs, (close_r.x + close_r.w // 2 - cs.get_width() // 2,
                               close_r.y + close_r.h // 2 - cs.get_height() // 2))
        self._pf_close_btn = close_r

    def _draw_pipe_sorter(self, player, world):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        PW, PH = 800, 460
        px = (SCREEN_W - PW) // 2
        py = (SCREEN_H - PH) // 2
        pygame.draw.rect(self.screen, (12, 10, 20), (px, py, PW, PH))
        pygame.draw.rect(self.screen, (80, 70, 140), (px, py, PW, PH), 2)

        title = self.font.render("PIPE SORTER", True, (180, 160, 240))
        self.screen.blit(title, (px + PW // 2 - title.get_width() // 2, py + 10))

        bx, by = self.active_pipe_sorter_pos
        cfg = world.pipe_state.get((bx, by), {})
        routes = cfg.get("routes", {})

        col_hdrs = ["Item", "Up", "Down", "Left", "Right", "Clear"]
        col_xs = [px + 10, px + 230, px + 310, px + 390, px + 470, px + 560]
        for hdr, hx in zip(col_hdrs, col_xs):
            hs = self.small.render(hdr, True, (180, 170, 210))
            self.screen.blit(hs, (hx, py + 38))

        pygame.draw.line(self.screen, (60, 55, 90),
                         (px + 10, py + 56), (px + PW - 10, py + 56), 1)

        self._ps_item_rects = {}
        self._ps_dir_rects  = {}
        inv_items = [(k, v) for k, v in player.inventory.items() if v > 0]
        VISIBLE = 8
        ROW_H = 34
        self._ps_scroll = max(0, min(self._ps_scroll, max(0, len(inv_items) - VISIBLE)))

        for idx in range(self._ps_scroll, min(self._ps_scroll + VISIBLE, len(inv_items))):
            item_id, count = inv_items[idx]
            row = idx - self._ps_scroll
            ry = py + 62 + row * ROW_H

            nm = ITEMS.get(item_id, {}).get("name", item_id)
            ns = self.small.render(f"{nm} x{count}", True, (200, 195, 220))
            self.screen.blit(ns, (col_xs[0], ry + 8))

            current_dir = routes.get(item_id)
            for di, dname in enumerate(("up", "down", "left", "right")):
                r = pygame.Rect(col_xs[1 + di], ry + 4, 60, 26)
                active = (current_dir == dname)
                pygame.draw.rect(self.screen, (50, 40, 80) if active else (25, 20, 40), r)
                pygame.draw.rect(self.screen, (140, 120, 200) if active else (60, 55, 90), r, 1)
                ds = self.small.render(dname[0].upper(), True, (230, 220, 255) if active else (130, 120, 160))
                self.screen.blit(ds, (r.x + r.w // 2 - ds.get_width() // 2,
                                      r.y + r.h // 2 - ds.get_height() // 2))
                self._ps_dir_rects[(item_id, dname)] = r

            clr_r = pygame.Rect(col_xs[5], ry + 4, 55, 26)
            pygame.draw.rect(self.screen, (50, 20, 20), clr_r)
            pygame.draw.rect(self.screen, (120, 60, 60), clr_r, 1)
            xs = self.small.render("Clear", True, (200, 140, 130))
            self.screen.blit(xs, (clr_r.x + clr_r.w // 2 - xs.get_width() // 2,
                                   clr_r.y + clr_r.h // 2 - xs.get_height() // 2))
            self._ps_item_rects[item_id] = clr_r

        close_r = pygame.Rect(px + PW - 90, py + PH - 38, 80, 26)
        pygame.draw.rect(self.screen, (35, 28, 50), close_r)
        pygame.draw.rect(self.screen, (80, 70, 120), close_r, 1)
        cs = self.small.render("Close [E]", True, (190, 180, 220))
        self.screen.blit(cs, (close_r.x + close_r.w // 2 - cs.get_width() // 2,
                               close_r.y + close_r.h // 2 - cs.get_height() // 2))
        self._ps_close_btn = close_r

    # =========================================================================
    # Factory panel
    # =========================================================================

    def _draw_factory(self, player, world):
        from factory import MAX_INPUT_SLOTS, MAX_OUTPUT_SLOTS

        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        PW, PH = 860, 500
        px = (SCREEN_W - PW) // 2
        py = (SCREEN_H - PH) // 2
        pygame.draw.rect(self.screen, (18, 26, 22), (px, py, PW, PH))
        pygame.draw.rect(self.screen, (80, 160, 110), (px, py, PW, PH), 2)

        title = self.font.render("FACTORY", True, (120, 210, 150))
        self.screen.blit(title, (px + PW // 2 - title.get_width() // 2, py + 10))

        bx, by = self.active_factory_pos
        state  = world.factory_data.get((bx, by), {})
        recipe = state.get("recipe", {})
        inputs_cfg  = recipe.get("inputs",  [None] * MAX_INPUT_SLOTS)
        outputs_cfg = recipe.get("outputs", [None] * MAX_OUTPUT_SLOTS)
        craft_time  = recipe.get("craft_time", 5.0)
        inv         = state.get("inventory", {})
        inv_cap     = state.get("inv_cap", 64)
        progress    = state.get("progress", 0.0)

        # ── Layout ────────────────────────────────────────────────────────────
        col_w   = 230
        slot_h  = 44
        slot_gap = 6
        in_x    = px + 20
        out_x   = px + PW - col_w - 20
        arrow_x = px + PW // 2 - 18
        slots_y = py + 48

        # ── Input column ──────────────────────────────────────────────────────
        ih = self.small.render("INPUTS  (click to assign / right-click clear)", True, (160, 200, 170))
        self.screen.blit(ih, (in_x, slots_y))

        self._fac_input_rects = {}
        self._fac_count_btns  = {}
        for i, slot in enumerate(inputs_cfg):
            sy = slots_y + 22 + i * (slot_h + slot_gap)
            r  = pygame.Rect(in_x, sy, col_w, slot_h)
            picking_this = (self._fac_picking == ("input", i))
            bg = (40, 70, 55) if picking_this else (28, 42, 34)
            bdr = (120, 210, 140) if picking_this else (55, 100, 70)
            pygame.draw.rect(self.screen, bg, r)
            pygame.draw.rect(self.screen, bdr, r, 1)
            if slot:
                nm = ITEMS.get(slot["item_id"], {}).get("name", slot["item_id"])
                ns = self.small.render(nm, True, (200, 230, 210))
                self.screen.blit(ns, (r.x + 6, r.y + 6))
                # count +/-
                cnt = slot["count"]
                cs  = self.small.render(f"x{cnt}", True, (180, 220, 190))
                self.screen.blit(cs, (r.x + 6, r.y + 24))
                minus_r = pygame.Rect(r.right - 50, r.y + 8, 20, 20)
                plus_r  = pygame.Rect(r.right - 26, r.y + 8, 20, 20)
                for btn_r, lbl in ((minus_r, "-"), (plus_r, "+")):
                    pygame.draw.rect(self.screen, (40, 60, 48), btn_r)
                    pygame.draw.rect(self.screen, (80, 140, 100), btn_r, 1)
                    bs2 = self.small.render(lbl, True, (180, 240, 200))
                    self.screen.blit(bs2, (btn_r.x + btn_r.w // 2 - bs2.get_width() // 2,
                                           btn_r.y + btn_r.h // 2 - bs2.get_height() // 2))
                self._fac_count_btns[("input", i, "-")] = minus_r
                self._fac_count_btns[("input", i, "+")] = plus_r
            else:
                es = self.small.render("— empty —", True, (80, 110, 90))
                self.screen.blit(es, (r.x + 6, r.y + r.h // 2 - es.get_height() // 2))
            self._fac_input_rects[i] = r

        # ── Arrow ─────────────────────────────────────────────────────────────
        ay = slots_y + 22 + MAX_INPUT_SLOTS * (slot_h + slot_gap) // 2 - 8
        for step in range(3):
            pygame.draw.polygon(self.screen, (80, 160, 110),
                                [(arrow_x + step * 10, ay),
                                 (arrow_x + step * 10 + 8, ay + 8),
                                 (arrow_x + step * 10, ay + 16)])

        # ── Output column ─────────────────────────────────────────────────────
        oh = self.small.render("OUTPUTS  (click to assign / right-click clear)", True, (160, 200, 170))
        self.screen.blit(oh, (out_x, slots_y))

        self._fac_output_rects = {}
        for i, slot in enumerate(outputs_cfg):
            sy = slots_y + 22 + i * (slot_h + slot_gap)
            r  = pygame.Rect(out_x, sy, col_w, slot_h)
            picking_this = (self._fac_picking == ("output", i))
            bg  = (40, 55, 70) if picking_this else (26, 34, 44)
            bdr = (100, 150, 210) if picking_this else (50, 80, 120)
            pygame.draw.rect(self.screen, bg, r)
            pygame.draw.rect(self.screen, bdr, r, 1)
            if slot:
                nm = ITEMS.get(slot["item_id"], {}).get("name", slot["item_id"])
                ns = self.small.render(nm, True, (190, 210, 240))
                self.screen.blit(ns, (r.x + 6, r.y + 6))
                cnt = slot["count"]
                cs  = self.small.render(f"x{cnt}", True, (170, 200, 230))
                self.screen.blit(cs, (r.x + 6, r.y + 24))
                minus_r = pygame.Rect(r.right - 50, r.y + 8, 20, 20)
                plus_r  = pygame.Rect(r.right - 26, r.y + 8, 20, 20)
                for btn_r, lbl in ((minus_r, "-"), (plus_r, "+")):
                    pygame.draw.rect(self.screen, (35, 45, 65), btn_r)
                    pygame.draw.rect(self.screen, (70, 110, 170), btn_r, 1)
                    bs2 = self.small.render(lbl, True, (180, 210, 255))
                    self.screen.blit(bs2, (btn_r.x + btn_r.w // 2 - bs2.get_width() // 2,
                                           btn_r.y + btn_r.h // 2 - bs2.get_height() // 2))
                self._fac_count_btns[("output", i, "-")] = minus_r
                self._fac_count_btns[("output", i, "+")] = plus_r
            else:
                es = self.small.render("— empty —", True, (70, 90, 120))
                self.screen.blit(es, (r.x + 6, r.y + r.h // 2 - es.get_height() // 2))
            self._fac_output_rects[i] = r

        # ── Craft time ────────────────────────────────────────────────────────
        ct_y = slots_y + 22 + MAX_INPUT_SLOTS * (slot_h + slot_gap) + 12
        ctl  = self.small.render(f"Craft time: {craft_time:.1f}s", True, (180, 200, 180))
        self.screen.blit(ctl, (in_x, ct_y))
        tm = self.small.render("[-]", True, (200, 180, 140))
        tp = self.small.render("[+]", True, (200, 180, 140))
        tm_r = pygame.Rect(in_x + 160, ct_y - 2, 28, 20)
        tp_r = pygame.Rect(in_x + 194, ct_y - 2, 28, 20)
        for btn_r, lbl in ((tm_r, "−"), (tp_r, "+")):
            pygame.draw.rect(self.screen, (40, 55, 40), btn_r)
            pygame.draw.rect(self.screen, (100, 140, 100), btn_r, 1)
            bs2 = self.small.render(lbl, True, (200, 230, 180))
            self.screen.blit(bs2, (btn_r.x + btn_r.w // 2 - bs2.get_width() // 2,
                                   btn_r.y + btn_r.h // 2 - bs2.get_height() // 2))
        self._fac_time_btns = {"-": tm_r, "+": tp_r}

        # ── Inventory cap ────────────────────────────────────────────────────
        cap_y  = ct_y + 24
        total  = sum(inv.values())
        cap_col = (220, 80, 80) if total >= inv_cap else (180, 200, 180)
        cap_lbl = self.small.render(f"Inv cap: {total}/{inv_cap}", True, cap_col)
        self.screen.blit(cap_lbl, (in_x, cap_y))
        cm_r = pygame.Rect(in_x + 160, cap_y - 2, 28, 20)
        cp_r = pygame.Rect(in_x + 194, cap_y - 2, 28, 20)
        for btn_r, lbl in ((cm_r, "−"), (cp_r, "+")):
            pygame.draw.rect(self.screen, (50, 38, 38), btn_r)
            pygame.draw.rect(self.screen, (130, 80, 80), btn_r, 1)
            bs2 = self.small.render(lbl, True, (230, 190, 190))
            self.screen.blit(bs2, (btn_r.x + btn_r.w // 2 - bs2.get_width() // 2,
                                   btn_r.y + btn_r.h // 2 - bs2.get_height() // 2))
        self._fac_cap_btns = {"-": cm_r, "+": cp_r}

        # ── Progress bar ─────────────────────────────────────────────────────
        bar_y = cap_y + 26
        bar_w = col_w * 2 + (arrow_x - in_x - col_w) * 2
        bar_h = 16
        bar_x = in_x
        pygame.draw.rect(self.screen, (30, 45, 35), (bar_x, bar_y, bar_w, bar_h))
        if craft_time > 0:
            fill = int(bar_w * min(1.0, progress / craft_time))
            if fill > 0:
                pygame.draw.rect(self.screen, (60, 180, 100), (bar_x, bar_y, fill, bar_h))
        pygame.draw.rect(self.screen, (70, 120, 80), (bar_x, bar_y, bar_w, bar_h), 1)
        pct_s = self.small.render(f"{int(min(100, progress / max(craft_time, 0.01) * 100))}%",
                                   True, (180, 220, 180))
        self.screen.blit(pct_s, (bar_x + bar_w // 2 - pct_s.get_width() // 2,
                                   bar_y + bar_h // 2 - pct_s.get_height() // 2))

        # ── Inventory ─────────────────────────────────────────────────────────
        inv_y = bar_y + bar_h + 12
        inv_label = self.small.render("Inventory:", True, (140, 180, 150))
        self.screen.blit(inv_label, (bar_x, inv_y))
        inv_str = "  ".join(
            f"{ITEMS.get(k, {}).get('name', k)} x{v}"
            for k, v in list(inv.items())[:8]
        ) or "(empty)"
        inv_s = self.small.render(inv_str, True, (170, 210, 180))
        self.screen.blit(inv_s, (bar_x, inv_y + 18))

        # ── Item picker (when a slot is being assigned) ───────────────────────
        if self._fac_picking is not None:
            pick_y   = py + PH - 170
            pick_lbl = self.small.render("Pick item from inventory:", True, (220, 220, 180))
            self.screen.blit(pick_lbl, (in_x, pick_y - 20))
            self._fac_pick_rects = {}
            inv_items = [(k, v) for k, v in player.inventory.items() if v > 0]
            PCOLS, PCW, PCH, PGAP = 4, 180, 32, 4
            for idx, (item_id, count) in enumerate(inv_items[:16]):
                col = idx % PCOLS
                row = idx // PCOLS
                rx  = in_x + col * (PCW + PGAP)
                ry  = pick_y + row * (PCH + PGAP)
                r   = pygame.Rect(rx, ry, PCW, PCH)
                pygame.draw.rect(self.screen, (35, 38, 28), r)
                pygame.draw.rect(self.screen, (100, 130, 80), r, 1)
                nm = ITEMS.get(item_id, {}).get("name", item_id)
                ns = self.small.render(f"{nm} x{count}", True, (210, 220, 190))
                self.screen.blit(ns, (r.x + 5, r.y + r.h // 2 - ns.get_height() // 2))
                self._fac_pick_rects[item_id] = r

        # ── Close button ─────────────────────────────────────────────────────
        close_r = pygame.Rect(px + PW - 90, py + PH - 38, 80, 26)
        pygame.draw.rect(self.screen, (28, 42, 34), close_r)
        pygame.draw.rect(self.screen, (70, 140, 90), close_r, 1)
        cs = self.small.render("Close [E]", True, (160, 220, 170))
        self.screen.blit(cs, (close_r.x + close_r.w // 2 - cs.get_width() // 2,
                               close_r.y + close_r.h // 2 - cs.get_height() // 2))
        self._fac_close_btn = close_r