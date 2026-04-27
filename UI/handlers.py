import pygame
from items import ITEMS
from item_icons import render_item_icon
from crafting import (RECIPES, BAKERY_RECIPES, WOK_RECIPES, STEAMER_RECIPES, NOODLE_POT_RECIPES,
                      BBQ_GRILL_RECIPES, CLAY_POT_RECIPES, FORGE_RECIPES, ARTISAN_RECIPES,
                      BAIT_STATION_RECIPES, FLETCHING_RECIPES, SMELTER_RECIPES, GLASS_KILN_RECIPES,
                      GARDEN_WORKSHOP_RECIPES, JUICER_RECIPES,
                      match_recipe, craft_costs, can_craft,
                      RESEARCH_LOCKED_RECIPES, is_research_locked, can_craft_with_research)
from rocks import get_refinery_equipment
from gemstones import get_fault_points, apply_cracking_result, invalidate_gem_cache
from blocks import (BAKERY_BLOCK, WOK_BLOCK, STEAMER_BLOCK, NOODLE_POT_BLOCK, BBQ_GRILL_BLOCK,
                    CLAY_POT_BLOCK, GEM_CUTTER_BLOCK, DESERT_FORGE_BLOCK,
                    ROASTER_BLOCK, BLEND_STATION_BLOCK, BREW_STATION_BLOCK, FOSSIL_TABLE_BLOCK,
                    ARTISAN_BENCH_BLOCK, JUICER_BLOCK,
                    GRAPE_PRESS_BLOCK, FERMENTATION_BLOCK, WINE_CELLAR_BLOCK,
                    STILL_BLOCK, BARREL_ROOM_BLOCK, BOTTLING_BLOCK,
                    BREW_KETTLE_BLOCK, FERM_VESSEL_BLOCK, TAPROOM_BLOCK,
                    COMPOST_BIN_BLOCK, GARDEN_BLOCK,
                    WITHERING_RACK_BLOCK, OXIDATION_STATION_BLOCK, TEA_CELLAR_BLOCK, ROASTING_KILN_BLOCK,
                    DRYING_RACK_BLOCK, KILN_BLOCK, RESONANCE_BLOCK,
                    BAIT_STATION_BLOCK,
                    SPINNING_WHEEL_BLOCK, DYE_VAT_BLOCK, LOOM_BLOCK,
                    DAIRY_VAT_BLOCK, CHEESE_PRESS_BLOCK, AGING_CAVE_BLOCK,
                    FLETCHING_TABLE_BLOCK, SMELTER_BLOCK, ANAEROBIC_TANK_BLOCK,
                    GLASS_KILN_BLOCK, GARDEN_WORKSHOP_BLOCK)
from constants import SCREEN_W, SCREEN_H, HOTBAR_SIZE, BLOCK_SIZE


def _is_garden_insect(insect, garden_pos):
    """True if this insect's spawn point is within 3 blocks of the garden block."""
    gx, gy = garden_pos
    cx = insect._spawn_x / BLOCK_SIZE
    cy = insect._spawn_y / BLOCK_SIZE
    return abs(cx - gx) <= 3 and abs(cy - gy) <= 3


class HandlersMixin:

    def handle_research_click(self, pos, player, world, research):
        for ci, rect in self._research_cat_rects.items():
            if rect.collidepoint(pos):
                self._research_selected_col = ci
                self._research_right_scroll = 0
                return
        for node_id, rect in self._card_rects.items():
            if rect.collidepoint(pos):
                research.unlock(node_id, player, world)
                break

    def handle_inventory_click(self, pos, player):
        for item_id, rect in self._inv_rects.items():
            if rect.collidepoint(pos):
                self._drag_item_id = item_id
                self._drag_pos = pos
                break

    def handle_inventory_drag(self, pos):
        if self._drag_item_id is not None:
            self._drag_pos = pos

    def handle_inventory_release(self, pos, player):
        if self._drag_item_id is not None:
            for i, rect in enumerate(self._hotbar_rects):
                if rect.collidepoint(pos):
                    player.hotbar[i] = self._drag_item_id
                    max_uses = ITEMS.get(self._drag_item_id, {}).get("max_uses")
                    player.hotbar_uses[i] = max_uses
                    break
            self._drag_item_id = None

    def _draw_drag_item(self):
        item = ITEMS.get(self._drag_item_id)
        if item is None:
            return
        icon = render_item_icon(self._drag_item_id, item["color"], 40)
        mx, my = self._drag_pos
        self.screen.blit(icon, (mx - 20, my - 20))
        # Highlight hotbar slots as drop targets
        for rect in self._hotbar_rects:
            s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            s.fill((220, 200, 50, 60))
            self.screen.blit(s, rect.topleft)

    def handle_hotbar_click(self, pos, player):
        for i, rect in enumerate(self._hotbar_rects):
            if rect.collidepoint(pos):
                player.selected_slot = i
                return True
        return False

    def handle_crafting_click(self, pos, player, button=1, research=None, debug=False):
        for (r, c), rect in self._cell_rects.items():
            if rect.collidepoint(pos):
                if button == 3:
                    self._craft_grid[r][c] = None
                else:
                    self._craft_grid[r][c] = self._cycle_craft_item(r, c, player)
                return
        if button == 1 and self._craft_btn and self._craft_btn.collidepoint(pos):
            self._do_grid_craft(player, research, debug=debug)
            return
        if button == 1:
            for ridx, rect in self._recipe_rects.items():
                if rect.collidepoint(pos):
                    self._craft_grid = [list(row) for row in RECIPES[ridx]["pattern"]]
                    return

    def _cycle_craft_item(self, row, col, player):
        choices = [None] + sorted(
            [iid for iid, cnt in player.inventory.items() if cnt > 0],
            key=lambda x: ITEMS.get(x, {}).get("name", x),
        )
        cur = self._craft_grid[row][col]
        idx = choices.index(cur) if cur in choices else -1
        return choices[(idx + 1) % len(choices)]

    def _do_grid_craft(self, player, research=None, debug=False):
        out_id, out_count = match_recipe(self._craft_grid)
        if not out_id:
            return
        if debug:
            for _ in range(out_count):
                player._add_item(out_id)
        elif can_craft_with_research(self._craft_grid, player.inventory, research):
            costs = craft_costs(self._craft_grid)
            for iid, needed in costs.items():
                player.inventory[iid] = player.inventory.get(iid, 0) - needed
                if player.inventory[iid] <= 0:
                    del player.inventory[iid]
                    for i in range(len(player.hotbar)):
                        if player.hotbar[i] == iid:
                            player.hotbar[i] = None
                            player.hotbar_uses[i] = None
            for _ in range(out_count):
                player._add_item(out_id)

    def handle_collection_click(self, pos, player):
        # Main tab buttons
        for tab_idx, rect in self._tab_rects.items():
            if rect.collidepoint(pos):
                self._collection_tab = tab_idx
                self._unified_selected = None
                self._unified_scroll = 0
                self._codex_scroll = 0
                self._flower_codex_scroll = 0
                self._mushroom_codex_scroll = 0
                self._fossil_codex_scroll = 0
                self._gem_codex_scroll = 0
                self._bird_codex_scroll = 0
                self._fish_codex_scroll = 0
                self._coffee_codex_scroll = 0
                self._wine_codex_scroll = 0
                self._spirits_codex_scroll = 0
                self._insect_codex_scroll = 0
                self._food_codex_scroll = 0
                self._horse_codex_scroll = 0
                self._tea_codex_scroll = 0
                self._herb_codex_scroll = 0
                self._codex_selected_type = None
                self._flower_codex_selected_type = None
                self._mushroom_codex_selected_bid = None
                self._fossil_codex_selected_type = None
                self._gem_codex_selected_type = None
                self._coffee_codex_selected = None
                self._wine_codex_selected = None
                self._spirits_codex_selected = None
                return

        if self._collection_tab == 0:
            # Filter buttons
            for fkey, frect in self._collection_filter_rects.items():
                if frect.collidepoint(pos):
                    self._collection_filter = fkey
                    self._unified_selected = None
                    self._unified_scroll = 0
                    return
            # Collection item clicks
            for key, rect in self._unified_rects.items():
                if rect.collidepoint(pos):
                    self._unified_selected = key if self._unified_selected != key else None
                    return

        elif self._collection_tab == 1:
            # Encyclopedia sub-category buttons
            for cat_i, erect in self._encyclopedia_cat_rects.items():
                if erect.collidepoint(pos):
                    self._encyclopedia_cat = cat_i
                    self._codex_scroll = 0
                    self._flower_codex_scroll = 0
                    self._mushroom_codex_scroll = 0
                    self._fossil_codex_scroll = 0
                    self._gem_codex_scroll = 0
                    self._bird_codex_scroll = 0
                    self._fish_codex_scroll = 0
                    self._coffee_codex_scroll = 0
                    self._wine_codex_scroll = 0
                    self._spirits_codex_scroll = 0
                    self._tea_codex_scroll = 0
                    self._hunting_codex_scroll = 0
                    self._codex_selected_type = None
                    self._flower_codex_selected_type = None
                    self._mushroom_codex_selected_bid = None
                    self._fossil_codex_selected_type = None
                    self._gem_codex_selected_type = None
                    self._coffee_codex_selected = None
                    self._wine_codex_selected = None
                    self._spirits_codex_selected = None
                    return
            # Codex item clicks
            if self._encyclopedia_cat == 0:
                for type_key, rect in self._codex_rects.items():
                    if rect.collidepoint(pos):
                        self._codex_selected_type = type_key if self._codex_selected_type != type_key else None
                        return
            elif self._encyclopedia_cat == 1:
                for type_key, rect in self._flower_codex_rects.items():
                    if rect.collidepoint(pos):
                        self._flower_codex_selected_type = type_key if self._flower_codex_selected_type != type_key else None
                        return
            elif self._encyclopedia_cat == 2:
                for bid, rect in self._mushroom_codex_rects.items():
                    if rect.collidepoint(pos):
                        self._mushroom_codex_selected_bid = bid if self._mushroom_codex_selected_bid != bid else None
                        return
            elif self._encyclopedia_cat == 3:
                for type_key, rect in self._fossil_codex_rects.items():
                    if rect.collidepoint(pos):
                        self._fossil_codex_selected_type = type_key if self._fossil_codex_selected_type != type_key else None
                        return
            elif self._encyclopedia_cat == 4:
                for type_key, rect in self._gem_codex_rects.items():
                    if rect.collidepoint(pos):
                        self._gem_codex_selected_type = type_key if self._gem_codex_selected_type != type_key else None
                        return
            elif self._encyclopedia_cat == 7:
                for key, rect in self._coffee_codex_rects.items():
                    if rect.collidepoint(pos):
                        self._coffee_codex_selected = key if self._coffee_codex_selected != key else None
                        return
            elif self._encyclopedia_cat == 8:
                for key, rect in self._wine_codex_rects.items():
                    if rect.collidepoint(pos):
                        self._wine_codex_selected = key if self._wine_codex_selected != key else None
                        return
            elif self._encyclopedia_cat == 9:
                for key, rect in self._spirits_codex_rects.items():
                    if rect.collidepoint(pos):
                        self._spirits_codex_selected = key if self._spirits_codex_selected != key else None
                        return
            elif self._encyclopedia_cat == 13:
                for key, rect in self._tea_codex_rects.items():
                    if rect.collidepoint(pos):
                        self._tea_codex_selected = key if self._tea_codex_selected != key else None
                        return
            elif self._encyclopedia_cat == 14:
                for key, rect in self._herb_codex_rects.items():
                    if rect.collidepoint(pos):
                        self._herb_codex_selected = key if self._herb_codex_selected != key else None
                        return
            elif self._encyclopedia_cat == 15:
                for key, rect in self._textile_codex_rects.items():
                    if rect.collidepoint(pos):
                        self._textile_codex_selected = key if self._textile_codex_selected != key else None
                        return
            elif self._encyclopedia_cat == 16:
                for key, rect in self._cheese_codex_rects.items():
                    if rect.collidepoint(pos):
                        self._cheese_codex_selected = key if self._cheese_codex_selected != key else None
                        return
            elif self._encyclopedia_cat == 19:
                for key, rect in self._salt_codex_rects.items():
                    if rect.collidepoint(pos):
                        self._salt_codex_selected = key if self._salt_codex_selected != key else None
                        return
            # cat 5 = bird codex (view only, no selection needed)
        # tab 2 (awards) has no click-to-select items

    def handle_scroll(self, dy):
        if self.research_open:
            mouse = pygame.mouse.get_pos()
            SIDEBAR_RIGHT = 20 + 175 + 28
            if mouse[0] < SIDEBAR_RIGHT:
                self._research_cat_scroll = max(0, min(self._max_research_cat_scroll, self._research_cat_scroll - dy * 58))
            else:
                self._research_right_scroll = max(0, min(self._max_research_right_scroll, self._research_right_scroll - dy * 58))
        elif self.inventory_open:
            self._inv_scroll = max(0, min(self._max_inv_scroll, self._inv_scroll - dy))
        elif self.crafting_open:
            self._recipe_scroll = max(0, min(self._max_recipe_scroll, self._recipe_scroll - dy * 58))
        elif self.refinery_open and self.refinery_block_id == BAKERY_BLOCK:
            self._bakery_scroll = max(0, min(self._max_bakery_scroll, self._bakery_scroll - dy))
        elif self.refinery_open:
            bid = self.refinery_block_id
            cur = self._cook_station_scroll.get(bid, 0)
            self._cook_station_scroll[bid] = max(
                0, min(self._cook_station_max_scroll.get(bid, 0), cur - dy))
        elif self.collection_open:
            mouse = pygame.mouse.get_pos()
            SIDEBAR_W = 130
            over_sidebar = mouse[0] < SIDEBAR_W
            if self._collection_tab == 0:
                if over_sidebar:
                    self._collection_sidebar_scroll = max(0, min(
                        self._max_collection_sidebar_scroll,
                        self._collection_sidebar_scroll - dy * 30))
                else:
                    self._unified_scroll = max(0, min(self._max_unified_scroll, self._unified_scroll - dy))
            elif self._collection_tab == 1:
                if over_sidebar:
                    self._encyclopedia_sidebar_scroll = max(0, min(
                        self._max_encyclopedia_sidebar_scroll,
                        self._encyclopedia_sidebar_scroll - dy * 30))
                    return
                if self._encyclopedia_cat == 0:
                    self._codex_scroll = max(0, min(self._max_codex_scroll, self._codex_scroll - dy))
                elif self._encyclopedia_cat == 1:
                    self._flower_codex_scroll = max(0, min(self._max_flower_codex_scroll, self._flower_codex_scroll - dy))
                elif self._encyclopedia_cat == 2:
                    self._mushroom_codex_scroll = max(0, min(self._max_mushroom_codex_scroll, self._mushroom_codex_scroll - dy))
                elif self._encyclopedia_cat == 3:
                    self._fossil_codex_scroll = max(0, min(self._max_fossil_codex_scroll, self._fossil_codex_scroll - dy))
                elif self._encyclopedia_cat == 4:
                    self._gem_codex_scroll = max(0, min(self._max_gem_codex_scroll, self._gem_codex_scroll - dy))
                elif self._encyclopedia_cat == 5:
                    self._bird_codex_scroll = max(0, min(self._max_bird_codex_scroll, self._bird_codex_scroll - dy * 80))
                elif self._encyclopedia_cat == 6:
                    self._fish_codex_scroll = max(0, min(self._max_fish_codex_scroll, self._fish_codex_scroll - dy * 80))
                elif self._encyclopedia_cat == 7:
                    self._coffee_codex_scroll = max(0, min(self._max_coffee_codex_scroll, self._coffee_codex_scroll - dy * 60))
                elif self._encyclopedia_cat == 8:
                    self._wine_codex_scroll = max(0, min(self._max_wine_codex_scroll, self._wine_codex_scroll - dy * 60))
                elif self._encyclopedia_cat == 9:
                    self._spirits_codex_scroll = max(0, min(self._max_spirits_codex_scroll, self._spirits_codex_scroll - dy * 40))
                elif self._encyclopedia_cat == 10:
                    self._insect_codex_scroll = max(0, min(self._max_insect_codex_scroll, self._insect_codex_scroll - dy * 80))
                elif self._encyclopedia_cat == 11:
                    self._food_codex_scroll = max(0, min(self._max_food_codex_scroll, self._food_codex_scroll - dy * 60))
                elif self._encyclopedia_cat == 12:
                    self._horse_codex_scroll = max(0, min(self._max_horse_codex_scroll, self._horse_codex_scroll - dy * 60))
                elif self._encyclopedia_cat == 13:
                    self._tea_codex_scroll = max(0, min(self._max_tea_codex_scroll, self._tea_codex_scroll - dy * 60))
                elif self._encyclopedia_cat == 14:
                    self._herb_codex_scroll = max(0, min(self._max_herb_codex_scroll, self._herb_codex_scroll - dy * 60))
            elif self._collection_tab == 2:
                self._achievement_scroll = max(0, min(self._max_achievement_scroll, self._achievement_scroll - dy))
        elif self.breeding_open:
            self._breed_scroll = max(0, min(self._max_breed_scroll, self._breed_scroll - dy))
        elif self.chest_open:
            mouse = pygame.mouse.get_pos()
            PW = 1140
            px = (SCREEN_W - PW) // 2
            if mouse[0] < px + PW // 2:
                self._chest_scroll = max(0, min(self._max_chest_scroll, self._chest_scroll - dy))
            else:
                self._player_chest_scroll = max(0, min(self._max_player_chest_scroll, self._player_chest_scroll - dy))
        elif self.garden_open:
            self._garden_col_scroll = max(0, min(self._max_garden_col_scroll, self._garden_col_scroll - dy))

    def handle_chest_click(self, pos, player, button):
        """Left-click transfers whole stack; right-click transfers one."""
        inv = self.active_chest_inv
        if inv is None:
            return
        count = 1 if button == 3 else None
        for item_id, rect in self._chest_rects.items():
            if rect.collidepoint(pos) and inv.get(item_id, 0) > 0:
                available = inv[item_id]
                take = min(available, count if count else available)
                inv[item_id] = available - take
                if inv[item_id] <= 0:
                    del inv[item_id]
                player._add_item(item_id, take)
                return
        for item_id, rect in self._player_for_chest_rects.items():
            if rect.collidepoint(pos) and player.inventory.get(item_id, 0) > 0:
                available = player.inventory[item_id]
                deposit = min(available, count if count else available)
                player.inventory[item_id] = available - deposit
                if player.inventory[item_id] <= 0:
                    del player.inventory[item_id]
                    if item_id in player.hotbar:
                        idx = player.hotbar.index(item_id)
                        player.hotbar[idx] = None
                        player.hotbar_uses[idx] = None
                inv[item_id] = inv.get(item_id, 0) + deposit
                return

    def handle_wildflower_display_click(self, pos, player):
        if self.active_display_pos is None:
            return
        bx, by = self.active_display_pos
        stored = player.world.wildflower_display_data.get((bx, by))
        # Click the display slot area to reclaim the flower
        slot_from_left = (SCREEN_W - 820) // 2 + 10
        half = (820 - 30) // 2
        slot_rect_x = slot_from_left + half // 2 - 60
        slot_rect_y = (SCREEN_H - 500) // 2 + 70
        slot_rect = pygame.Rect(slot_rect_x, slot_rect_y, 120, 120)
        if slot_rect.collidepoint(pos) and stored is not None:
            player.wildflowers.append(stored)
            player.world.wildflower_display_data.pop((bx, by), None)
            return
        # Click a flower in the player collection → place it (replaces any existing)
        for uid, rect in self._display_player_rects.items():
            if rect.collidepoint(pos):
                for i, wf in enumerate(player.wildflowers):
                    if wf.uid == uid:
                        if stored is not None:
                            player.wildflowers.append(stored)
                        player.world.wildflower_display_data[(bx, by)] = player.wildflowers.pop(i)
                        return

    def handle_garden_mousedown(self, pos, player):
        flowers    = self.active_garden_flowers
        garden_pos = self.active_garden_pos
        if flowers is None or garden_pos is None:
            return
        CAPACITY = 12
        # Pick up from an occupied garden slot
        for slot_idx, rect in self._garden_slot_rects.items():
            if rect.collidepoint(pos) and slot_idx < len(flowers):
                self._garden_drag_flower = flowers[slot_idx]
                self._garden_drag_source = 'slot'
                self._garden_drag_pos    = pos
                flowers.pop(slot_idx)
                if not flowers:
                    player.world.insects = [
                        ins for ins in player.world.insects
                        if not _is_garden_insect(ins, garden_pos)
                    ]
                return
        # Pick up from the collection panel
        for uid, rect in self._garden_col_rects.items():
            if rect.collidepoint(pos):
                for i, wf in enumerate(player.wildflowers):
                    if wf.uid == uid and len(flowers) < CAPACITY:
                        self._garden_drag_flower = player.wildflowers.pop(i)
                        self._garden_drag_source = 'collection'
                        self._garden_drag_pos    = pos
                        return

    def handle_garden_mousemotion(self, pos):
        if self._garden_drag_flower is not None:
            self._garden_drag_pos = pos

    def handle_garden_mouseup(self, pos, player):
        drag_wf    = self._garden_drag_flower
        drag_src   = self._garden_drag_source
        flowers    = self.active_garden_flowers
        garden_pos = self.active_garden_pos
        if drag_wf is None or flowers is None:
            return

        CAPACITY = 12
        dropped  = False

        # Drop onto a garden slot
        for slot_idx, rect in self._garden_slot_rects.items():
            if rect.collidepoint(pos):
                insert_idx = min(slot_idx, len(flowers))
                flowers.insert(insert_idx, drag_wf)
                was_first = len(flowers) == 1
                if was_first:
                    player.world.spawn_insects_near_garden(*garden_pos)
                dropped = True
                break

        if not dropped:
            # Drop onto the collection panel → return flower to inventory
            PW = 1160
            px = (SCREEN_W - PW) // 2
            col_zone_x = px + 730 + 18 + 8
            col_zone_w = PW - (730 + 18 + 8 + 10)
            if pos[0] >= col_zone_x and pos[0] <= col_zone_x + col_zone_w:
                player.wildflowers.append(drag_wf)
                if drag_src == 'slot' and not flowers:
                    player.world.insects = [
                        ins for ins in player.world.insects
                        if not _is_garden_insect(ins, garden_pos)
                    ]
                dropped = True

        if not dropped:
            # Dropped nowhere — return to original source
            if drag_src == 'slot':
                flowers.append(drag_wf)
                if len(flowers) == 1:
                    player.world.spawn_insects_near_garden(*garden_pos)
            else:
                player.wildflowers.append(drag_wf)

        self._garden_drag_flower = None
        self._garden_drag_source = None


    def handle_npc_click(self, pos, player):
        from cities import (RockQuestNPC, TradeNPC, WildflowerQuestNPC, GemQuestNPC,
                            MerchantNPC, RestaurantNPC, ShrineKeeperNPC, JewelryMerchantNPC,
                            LeaderNPC, BlacksmithNPC, InnkeeperNPC, ScholarNPC,
                            RoyalPaleontologistNPC, RoyalAnglerNPC,
                            WeaponArmorerNPC, QuartermasterNPC, GarrisonCommanderNPC,
                            DoctorNPC)
        from outpost_npcs import OutpostKeeperNPC
        npc = self.active_npc
        if isinstance(npc, RockQuestNPC):
            for quest_idx, rect in self._trade_rects.items():
                if rect.collidepoint(pos):
                    npc.complete_quest(player, quest_idx)
                    break
        elif isinstance(npc, TradeNPC):
            for i, rect in self._trade_rects.items():
                if rect.collidepoint(pos):
                    npc.execute_trade(i, player)
                    break
        elif isinstance(npc, WildflowerQuestNPC):
            for quest_idx, rect in self._trade_rects.items():
                if rect.collidepoint(pos):
                    npc.complete_quest(player, quest_idx)
                    break
        elif isinstance(npc, GemQuestNPC):
            for quest_idx, rect in self._trade_rects.items():
                if rect.collidepoint(pos):
                    npc.complete_quest(player, quest_idx)
                    break
        elif isinstance(npc, RoyalPaleontologistNPC):
            for quest_idx, rect in self._trade_rects.items():
                if rect.collidepoint(pos):
                    npc.complete_quest(player, quest_idx)
                    break
        elif isinstance(npc, RoyalAnglerNPC):
            for quest_idx, rect in self._trade_rects.items():
                if rect.collidepoint(pos):
                    npc.complete_quest(player, quest_idx)
                    break
        elif isinstance(npc, MerchantNPC):
            for key, rect in self._trade_rects.items():
                if rect.collidepoint(pos):
                    idx, action = key
                    if action == "buy":
                        npc.execute_purchase(idx, player)
                    else:
                        npc.execute_barter(idx, player)
                    break
        elif isinstance(npc, RestaurantNPC):
            for i, rect in self._trade_rects.items():
                if rect.collidepoint(pos):
                    npc.execute_purchase(i, player)
                    break
        elif isinstance(npc, ShrineKeeperNPC):
            if self._trade_rects.get(0) and self._trade_rects[0].collidepoint(pos):
                npc.give_blessing(player)
        elif isinstance(npc, JewelryMerchantNPC):
            self.handle_jewelry_merchant_click(pos, player, npc)
        elif isinstance(npc, BlacksmithNPC):
            for key, rect in self._trade_rects.items():
                if rect.collidepoint(pos):
                    idx, action = key
                    if action == "buy":
                        npc.execute_purchase(idx, player)
                    else:
                        npc.execute_barter(idx, player)
                    break
        elif isinstance(npc, InnkeeperNPC):
            for key, rect in self._trade_rects.items():
                if rect.collidepoint(pos):
                    if key == "rest":
                        if npc.give_rest(player):
                            _deliver_farmer_seeds(player, player.world)
                    else:
                        npc.execute_purchase(key, player)
                    break
        elif isinstance(npc, ScholarNPC):
            for key, rect in self._trade_rects.items():
                if rect.collidepoint(pos):
                    idx, action = key
                    if action == "buy":
                        npc.execute_purchase(idx, player)
                    else:
                        npc.execute_barter(idx, player)
                    break
        elif isinstance(npc, LeaderNPC):
            for idx, rect in self._trade_rects.items():
                if rect.collidepoint(pos):
                    npc.execute_contract(idx, player)
                    break
        elif isinstance(npc, WeaponArmorerNPC):
            self._handle_weapon_armorer_click(pos, player, npc)
        elif isinstance(npc, QuartermasterNPC):
            for i, rect in self._trade_rects.items():
                if rect.collidepoint(pos):
                    npc.execute_trade(i, player)
                    break
        elif isinstance(npc, GarrisonCommanderNPC):
            self._handle_garrison_commander_click(pos, player, npc)
        elif isinstance(npc, DoctorNPC):
            if self._trade_rects.get(0) and self._trade_rects[0].collidepoint(pos):
                npc.execute_heal(player)
        elif isinstance(npc, OutpostKeeperNPC):
            for key, value in self._trade_rects.items():
                idx, action = key
                if action == "supply":
                    rect, item_id = value
                    if rect.collidepoint(pos):
                        npc.execute_supply(item_id, player)
                        break
                elif value.collidepoint(pos):
                    if action == "buy":
                        npc.execute_purchase(idx, player)
                    else:
                        npc.execute_sell(idx, player)
                    break

    def handle_gem_cutter_click(self, pos, player):
        """Handle clicks inside the gem cutter mini-game overlay."""
        phase = self._gc_phase

        if phase == "select":
            for idx, rect in self._gc_select_rects.items():
                if rect.collidepoint(pos):
                    gem = player.gems[idx]
                    if gem.state == "rough":
                        self._gc_gem_idx = idx
                        self._gc_fault_pts = get_fault_points(gem, area_size=220)
                        self._gc_seq_idx = 0
                        self._gc_seq_timer = 0.6
                        self._gc_seq_clicks = []
                        self._gc_mistakes = 0
                        self._gc_fault_lit = 0
                        self._gc_phase = "show_seq"
            return

        if phase == "player_turn":
            for i, rect in enumerate(self._gc_fault_rects):
                if rect.collidepoint(pos):
                    expected = self._gc_seq_clicks.__len__()
                    if i == expected:
                        self._gc_seq_clicks.append(i)
                        if len(self._gc_seq_clicks) == len(self._gc_fault_pts):
                            # All tapped correctly — begin reveal
                            self._gc_phase = "reveal"
                            self._gc_reveal_timer = 1.2
                    else:
                        self._gc_mistakes = min(3, self._gc_mistakes + 1)
                        # Allow them to still click the right one
                    return

        if phase == "choose_cut":
            for cut_name, rect in self._gc_cut_rects.items():
                if rect.collidepoint(pos):
                    gem = player.gems[self._gc_gem_idx]
                    gem.cut = cut_name
                    gem.state = "cut"
                    apply_cracking_result(gem, self._gc_mistakes)
                    invalidate_gem_cache(gem.uid)
                    player.discovered_gem_types.add(gem.gem_type)
                    self._gc_phase = "select"
                    self._gc_gem_idx = None
                    return

    def handle_refinery_click(self, pos, player):
        if self.refinery_block_id == FOSSIL_TABLE_BLOCK:
            self._handle_fossil_table_click(pos, player)
            return
        if self.refinery_block_id == ROASTER_BLOCK:
            self._handle_roaster_click(pos, player)
            return
        if self.refinery_block_id == BLEND_STATION_BLOCK:
            self._handle_blend_click(pos, player)
            return
        if self.refinery_block_id == BREW_STATION_BLOCK:
            self._handle_brew_click(pos, player)
            return
        if self.refinery_block_id == GRAPE_PRESS_BLOCK:
            self._handle_grape_press_click(pos, player)
            return
        if self.refinery_block_id == FERMENTATION_BLOCK:
            self._handle_fermenter_click(pos, player)
            return
        if self.refinery_block_id == WINE_CELLAR_BLOCK:
            self._handle_wine_cellar_click(pos, player)
            return
        if self.refinery_block_id == STILL_BLOCK:
            self._handle_still_click(pos, player)
            return
        if self.refinery_block_id == BARREL_ROOM_BLOCK:
            self._handle_barrel_room_click(pos, player)
            return
        if self.refinery_block_id == BOTTLING_BLOCK:
            self._handle_bottling_click(pos, player)
            return
        if self.refinery_block_id == BREW_KETTLE_BLOCK:
            self._handle_brew_kettle_click(pos, player)
            return
        if self.refinery_block_id == FERM_VESSEL_BLOCK:
            self._handle_ferm_vessel_click(pos, player)
            return
        if self.refinery_block_id == TAPROOM_BLOCK:
            self._handle_taproom_click(pos, player)
            return
        if self.refinery_block_id == WITHERING_RACK_BLOCK:
            self._handle_withering_rack_click(pos, player)
            return
        if self.refinery_block_id == OXIDATION_STATION_BLOCK:
            self._handle_oxidation_station_click(pos, player)
            return
        if self.refinery_block_id == TEA_CELLAR_BLOCK:
            self._handle_tea_cellar_click(pos, player)
            return
        if self.refinery_block_id == ROASTING_KILN_BLOCK:
            self._handle_roasting_kiln_click(pos, player)
            return
        if self.refinery_block_id == DRYING_RACK_BLOCK:
            self._handle_drying_rack_click(pos, player)
            return
        if self.refinery_block_id == KILN_BLOCK:
            self._handle_kiln_click(pos, player, getattr(self, "_research", None))
            return
        if self.refinery_block_id == RESONANCE_BLOCK:
            self._handle_resonance_click(pos, player, getattr(self, "_research", None))
            return
        if self.refinery_block_id == SPINNING_WHEEL_BLOCK:
            self._handle_spinning_wheel_click(pos, player)
            return
        if self.refinery_block_id == DYE_VAT_BLOCK:
            self._handle_dye_vat_click(pos, player)
            return
        if self.refinery_block_id == LOOM_BLOCK:
            self._handle_loom_click(pos, player)
            return
        if self.refinery_block_id == DAIRY_VAT_BLOCK:
            self.handle_dairy_vat_click(pos, player)
            return
        if self.refinery_block_id == CHEESE_PRESS_BLOCK:
            self.handle_cheese_press_click(pos, player)
            return
        if self.refinery_block_id == AGING_CAVE_BLOCK:
            self.handle_aging_cave_click(pos, player)
            return
        if self.refinery_block_id == ANAEROBIC_TANK_BLOCK:
            self._handle_anaerobic_click(pos, player)
            return
        from blocks import JEWELRY_WORKBENCH_BLOCK, SCULPTORS_BENCH, TAPESTRY_FRAME_BLOCK
        if self.refinery_block_id == JEWELRY_WORKBENCH_BLOCK:
            self._handle_jewelry_workbench_click(pos, player)
            return
        if self.refinery_block_id == SCULPTORS_BENCH:
            self._handle_sculptor_bench_click(pos, player, right=False)
            return
        if self.refinery_block_id == TAPESTRY_FRAME_BLOCK:
            self._handle_tapestry_frame_click(pos, player, right=False)
            return
        from blocks import POTTERY_WHEEL_BLOCK, POTTERY_KILN_BLOCK
        if self.refinery_block_id == POTTERY_WHEEL_BLOCK:
            self._handle_pottery_wheel_click(pos, player)
            return
        if self.refinery_block_id == POTTERY_KILN_BLOCK:
            self._handle_pottery_kiln_click(pos, player)
            return
        from blocks import FORGE_BLOCK, WEAPON_RACK_BLOCK
        if self.refinery_block_id == FORGE_BLOCK:
            self._handle_forge_click(pos, player)
            return
        if self.refinery_block_id == WEAPON_RACK_BLOCK:
            self._handle_weapon_rack_click(pos, player)
            return
        if self.refinery_block_id == BAKERY_BLOCK:
            for i, rect in self._bakery_recipe_rects.items():
                if rect.collidepoint(pos):
                    self._bakery_selected_recipe = i
                    return
            if self._refine_btn and self._refine_btn.collidepoint(pos):
                self._do_bake(player)
            return
        if self.refinery_block_id == WOK_BLOCK:
            for i, rect in self._wok_recipe_rects.items():
                if rect.collidepoint(pos):
                    self._wok_selected_recipe = i
                    return
            if self._refine_btn and self._refine_btn.collidepoint(pos):
                self._do_cook(player, WOK_RECIPES, self._wok_selected_recipe)
            return
        if self.refinery_block_id == STEAMER_BLOCK:
            for i, rect in self._steamer_recipe_rects.items():
                if rect.collidepoint(pos):
                    self._steamer_selected_recipe = i
                    return
            if self._refine_btn and self._refine_btn.collidepoint(pos):
                self._do_cook(player, STEAMER_RECIPES, self._steamer_selected_recipe)
            return
        if self.refinery_block_id == NOODLE_POT_BLOCK:
            for i, rect in self._noodle_pot_recipe_rects.items():
                if rect.collidepoint(pos):
                    self._noodle_pot_selected_recipe = i
                    return
            if self._refine_btn and self._refine_btn.collidepoint(pos):
                self._do_cook(player, NOODLE_POT_RECIPES, self._noodle_pot_selected_recipe)
            return
        if self.refinery_block_id == BBQ_GRILL_BLOCK:
            for i, rect in self._bbq_grill_recipe_rects.items():
                if rect.collidepoint(pos):
                    self._bbq_grill_selected_recipe = i
                    return
            if self._refine_btn and self._refine_btn.collidepoint(pos):
                self._do_cook(player, BBQ_GRILL_RECIPES, self._bbq_grill_selected_recipe)
            return
        if self.refinery_block_id == CLAY_POT_BLOCK:
            for i, rect in self._clay_pot_recipe_rects.items():
                if rect.collidepoint(pos):
                    self._clay_pot_selected_recipe = i
                    return
            if self._refine_btn and self._refine_btn.collidepoint(pos):
                self._do_cook(player, CLAY_POT_RECIPES, self._clay_pot_selected_recipe)
            return
        if self.refinery_block_id == DESERT_FORGE_BLOCK:
            for i, rect in self._desert_forge_recipe_rects.items():
                if rect.collidepoint(pos):
                    self._desert_forge_selected_recipe = i
                    return
            if self._refine_btn and self._refine_btn.collidepoint(pos):
                self._do_cook(player, FORGE_RECIPES, self._desert_forge_selected_recipe)
            return
        if self.refinery_block_id == ARTISAN_BENCH_BLOCK:
            for i, rect in self._artisan_recipe_rects.items():
                if rect.collidepoint(pos):
                    self._artisan_selected_recipe = i
                    return
            if self._refine_btn and self._refine_btn.collidepoint(pos):
                self._do_cook(player, ARTISAN_RECIPES, self._artisan_selected_recipe)
            return
        if self.refinery_block_id == BAIT_STATION_BLOCK:
            for i, rect in self._bait_station_recipe_rects.items():
                if rect.collidepoint(pos):
                    self._bait_station_selected_recipe = i
                    return
            if self._refine_btn and self._refine_btn.collidepoint(pos):
                self._do_cook(player, BAIT_STATION_RECIPES, self._bait_station_selected_recipe)
            return
        if self.refinery_block_id == FLETCHING_TABLE_BLOCK:
            for i, rect in self._fletching_recipe_rects.items():
                if rect.collidepoint(pos):
                    self._fletching_selected_recipe = i
                    return
            if self._refine_btn and self._refine_btn.collidepoint(pos):
                self._do_cook(player, FLETCHING_RECIPES, self._fletching_selected_recipe)
            return
        if self.refinery_block_id == SMELTER_BLOCK:
            for i, rect in self._smelter_recipe_rects.items():
                if rect.collidepoint(pos):
                    self._smelter_selected_recipe = i
                    return
            if self._refine_btn and self._refine_btn.collidepoint(pos):
                self._do_cook(player, SMELTER_RECIPES, self._smelter_selected_recipe)
            return
        if self.refinery_block_id == GLASS_KILN_BLOCK:
            for i, rect in self._glass_kiln_recipe_rects.items():
                if rect.collidepoint(pos):
                    self._glass_kiln_selected_recipe = i
                    return
            if self._refine_btn and self._refine_btn.collidepoint(pos):
                self._do_cook(player, GLASS_KILN_RECIPES, self._glass_kiln_selected_recipe)
            return
        if self.refinery_block_id == GARDEN_WORKSHOP_BLOCK:
            for i, rect in self._garden_workshop_recipe_rects.items():
                if rect.collidepoint(pos):
                    self._garden_workshop_selected_recipe = i
                    return
            if self._refine_btn and self._refine_btn.collidepoint(pos):
                self._do_cook(player, GARDEN_WORKSHOP_RECIPES, self._garden_workshop_selected_recipe)
            return
        if self.refinery_block_id == JUICER_BLOCK:
            for i, rect in self._juicer_recipe_rects.items():
                if rect.collidepoint(pos):
                    self._juicer_selected_recipe = i
                    return
            if self._refine_btn and self._refine_btn.collidepoint(pos):
                self._do_cook(player, JUICER_RECIPES, self._juicer_selected_recipe)
            return
        if self.refinery_block_id == COMPOST_BIN_BLOCK:
            self._handle_compost_bin_click(pos, player)
            return
        from blocks import CHICKEN_COOP_BLOCK
        if self.refinery_block_id == CHICKEN_COOP_BLOCK:
            self._handle_coop_click(pos, player)
            return
        from blocks import EVAPORATION_PAN_BLOCK, SALT_GRINDER_BLOCK
        if self.refinery_block_id == EVAPORATION_PAN_BLOCK:
            self._handle_evap_pan_click(pos, player)
            return
        if self.refinery_block_id == SALT_GRINDER_BLOCK:
            self._handle_salt_grinder_click(pos, player)
            return
        for idx, rect in self._refine_rects.items():
            if rect.collidepoint(pos):
                self._refinery_selected_idx = idx
                return
        if self._refine_btn and self._refine_btn.collidepoint(pos):
            self._do_refine(player)

    def _record_food_discovery(self, player, output_id):
        from items import ITEMS
        if not ITEMS.get(output_id, {}).get("edible"):
            return
        is_new = output_id not in player.discovered_foods
        player.discovered_foods.add(output_id)
        player.foods_cooked[output_id] = player.foods_cooked.get(output_id, 0) + 1
        if is_new:
            player.pending_notifications.append(("Food", ITEMS[output_id]["name"], "recipe"))

    def _do_bake(self, player):
        recipe = BAKERY_RECIPES[self._bakery_selected_recipe]
        for item_id, needed in recipe["ingredients"].items():
            if player.inventory.get(item_id, 0) < needed:
                return
        for item_id, needed in recipe["ingredients"].items():
            player.inventory[item_id] -= needed
            if player.inventory[item_id] <= 0:
                del player.inventory[item_id]
                for i in range(HOTBAR_SIZE):
                    if player.hotbar[i] == item_id:
                        player.hotbar[i] = None
                        player.hotbar_uses[i] = None
        for _ in range(recipe["output_count"]):
            player._add_item(recipe["output_id"])
        self._record_food_discovery(player, recipe["output_id"])

    def _do_cook(self, player, recipe_list, selected_idx):
        recipe = recipe_list[selected_idx]
        for item_id, needed in recipe["ingredients"].items():
            if player.inventory.get(item_id, 0) < needed:
                return
        for item_id, needed in recipe["ingredients"].items():
            player.inventory[item_id] -= needed
            if player.inventory[item_id] <= 0:
                del player.inventory[item_id]
                for i in range(HOTBAR_SIZE):
                    if player.hotbar[i] == item_id:
                        player.hotbar[i] = None
                        player.hotbar_uses[i] = None
        for _ in range(recipe["output_count"]):
            player._add_item(recipe["output_id"])
        self._record_food_discovery(player, recipe["output_id"])

    def _do_refine(self, player):
        equip = get_refinery_equipment().get(self.refinery_block_id)
        if equip is None:
            return
        idx = self._refinery_selected_idx
        if idx is None or idx >= len(player.rocks):
            return
        rock = player.rocks[idx]
        if not equip["can_use"](rock):
            return
        outputs = equip["refine"](rock)
        if outputs:
            player.rocks.pop(idx)
            self._refinery_selected_idx = None
            for item_id, count in outputs:
                for _ in range(count):
                    player._add_item(item_id)

    def _handle_compost_bin_click(self, pos, player):
        import soil as _soil
        bin_pos = self.active_compost_bin_pos
        if bin_pos is None:
            return
        bin_data = player.world.compost_bin_data.setdefault(
            bin_pos, {"input": {}, "progress": 0.0, "output": 0})

        if self._compost_deposit_btn and self._compost_deposit_btn.collidepoint(pos):
            sel = player.hotbar[player.selected_slot]
            if sel and sel in _soil.ORGANIC_ITEM_IDS and player.inventory.get(sel, 0) > 0:
                player.inventory[sel] -= 1
                if player.inventory[sel] <= 0:
                    del player.inventory[sel]
                bin_data["input"][sel] = bin_data["input"].get(sel, 0) + 1

        if self._compost_collect_btn and self._compost_collect_btn.collidepoint(pos):
            if bin_data["output"] > 0:
                player._add_item("compost", bin_data["output"])
                bin_data["output"] = 0

    def _handle_coop_click(self, pos, player):
        coop_pos = self.active_coop_pos
        if coop_pos is None:
            return
        coop_data = player.world.chicken_coop_data.setdefault(
            coop_pos, {"eggs": 0, "progress": 0.0})
        if self._coop_collect_btn and self._coop_collect_btn.collidepoint(pos):
            if coop_data["eggs"] > 0:
                player._add_item("egg", coop_data["eggs"])
                coop_data["eggs"] = 0

    def handle_horse_breeding_click(self, pos, player, world):
        if self._hbr_close_btn and self._hbr_close_btn.collidepoint(pos):
            self.horse_breeding_open = False
            self._hbr_horse_a = None
            self._hbr_horse_b = None
            return

        if self._hbr_breed_btn and self._hbr_breed_btn.collidepoint(pos):
            horse_a = self._hbr_horse_a
            horse_b = self._hbr_horse_b
            if horse_a is None or horse_b is None:
                return
            horse_a.breed_with(horse_b, world, player)
            # Close the panel after breeding
            self.horse_breeding_open = False
            self._hbr_horse_a = None
            self._hbr_horse_b = None

    def handle_kennel_breeding_click(self, pos, player, world):
        if self._dbr_close_btn and self._dbr_close_btn.collidepoint(pos):
            self.dog_breeding_open = False
            self._dbr_dog_a = None
            self._dbr_dog_b = None
            return
        if self._dbr_breed_btn and self._dbr_breed_btn.collidepoint(pos):
            dog_a = self._dbr_dog_a
            dog_b = self._dbr_dog_b
            if dog_a and dog_b:
                dog_a.breed_with(dog_b, world, player)
            self.dog_breeding_open = False
            self._dbr_dog_a = None
            self._dbr_dog_b = None
            return

    def handle_dog_view_click(self, pos, player):
        if self._dv_close_btn and self._dv_close_btn.collidepoint(pos):
            self.dog_view_open = False
            self._dv_dog = None
            return
        if self._dv_stay_btn and self._dv_stay_btn.collidepoint(pos):
            if self._dv_dog:
                self._dv_dog.stay_mode = not self._dv_dog.stay_mode
            return

    def handle_trade_block_click(self, pos, player, world, button):
        from horses import Horse
        from towns import TOWNS

        state = world.trade_block_data.get(self.active_trade_pos)
        if state is None:
            return

        tamed_horses = [e for e in world.entities if isinstance(e, Horse) and e.tamed and not e.dead]
        town_list = sorted(TOWNS.values(), key=lambda t: t.town_id)
        idle = state["state"] == "idle"

        # Horse prev/next arrows and assign button
        if isinstance(self._trade_horse_btn, tuple):
            nav_r, assign_r = self._trade_horse_btn
            if nav_r.collidepoint(pos) and tamed_horses:
                if pos[0] < nav_r.centerx:
                    self._trade_horse_idx = (self._trade_horse_idx - 1) % len(tamed_horses)
                else:
                    self._trade_horse_idx = (self._trade_horse_idx + 1) % len(tamed_horses)
                return
            if assign_r.collidepoint(pos) and tamed_horses:
                h = tamed_horses[min(self._trade_horse_idx, len(tamed_horses) - 1)]
                state["horse_uid"] = h.uid
                return

        # Cart assign
        if self._trade_cart_btn and self._trade_cart_btn.collidepoint(pos):
            if not state["has_cart"]:
                if player.inventory.get("cart", 0) > 0:
                    player.inventory["cart"] -= 1
                    if player.inventory["cart"] <= 0:
                        del player.inventory["cart"]
                        if "cart" in player.hotbar:
                            idx = player.hotbar.index("cart")
                            player.hotbar[idx] = None
                            player.hotbar_uses[idx] = None
                    state["has_cart"] = True
            return

        # City prev/next arrows and link button
        if isinstance(self._trade_city_btn, tuple):
            city_nav_r, link_r = self._trade_city_btn
            if city_nav_r.collidepoint(pos) and town_list:
                if pos[0] < city_nav_r.centerx:
                    self._trade_city_idx = (self._trade_city_idx - 1) % len(town_list)
                else:
                    self._trade_city_idx = (self._trade_city_idx + 1) % len(town_list)
                return
            if link_r.collidepoint(pos) and town_list:
                t = town_list[min(self._trade_city_idx, len(town_list) - 1)]
                state["linked_town_id"] = t.town_id
                return

        # Threshold buttons
        if self._trade_thresh_minus and self._trade_thresh_minus.collidepoint(pos):
            state["threshold"] = max(1, state["threshold"] - 1)
            return
        if self._trade_thresh_plus and self._trade_thresh_plus.collidepoint(pos):
            state["threshold"] = min(100, state["threshold"] + 1)
            return

        # Dispatch button (manual override)
        if self._trade_dispatch_btn and self._trade_dispatch_btn.collidepoint(pos):
            from horses import Horse as _H
            from towns import TOWNS as _T
            from constants import BLOCK_SIZE as _BS
            horse = next(
                (e for e in world.entities if isinstance(e, _H) and e.uid == state["horse_uid"] and e.tamed and not e.dead),
                None,
            )
            town = _T.get(state["linked_town_id"])
            if horse and town and sum(state["inventory"].values()) > 0:
                horse._on_trade_run = True
                horse._trade_target_x = town.center_bx * _BS
                state["state"] = "traveling"
            return

        # Goods grid: left-click returns item to player (idle only)
        if idle:
            for item_id, rect in self._trade_goods_rects.items():
                if rect.collidepoint(pos):
                    count = 1 if button == 3 else state["inventory"].get(item_id, 0)
                    take = min(count, state["inventory"].get(item_id, 0))
                    if take > 0:
                        state["inventory"][item_id] = state["inventory"].get(item_id, 0) - take
                        if state["inventory"][item_id] <= 0:
                            del state["inventory"][item_id]
                        player._add_item(item_id, take)
                    return

        # Player inventory grid: click to deposit into trade block (idle only)
        if idle:
            CAPACITY = 20
            for item_id, rect in self._trade_player_rects.items():
                if rect.collidepoint(pos):
                    if len(state["inventory"]) >= CAPACITY and item_id not in state["inventory"]:
                        return
                    available = player.inventory.get(item_id, 0)
                    deposit = 1 if button == 3 else available
                    deposit = min(deposit, available)
                    if deposit > 0:
                        player.inventory[item_id] = available - deposit
                        if player.inventory[item_id] <= 0:
                            del player.inventory[item_id]
                            if item_id in player.hotbar:
                                idx = player.hotbar.index(item_id)
                                player.hotbar[idx] = None
                                player.hotbar_uses[idx] = None
                        state["inventory"][item_id] = state["inventory"].get(item_id, 0) + deposit
                    return


def _deliver_farmer_seeds(player, world):
    """If any Beloved farmer donors exist, give the player 1–3 random crop seeds."""
    donors = getattr(player, "farm_seed_donors", set())
    if not donors:
        return
    import random
    _SEED_POOL = [
        "wheat_seed", "carrot_seed", "tomato_seed", "corn_seed", "pumpkin_seed",
        "rice_seed", "ginger_seed", "chili_seed", "pepper_seed", "apple_seed",
        "strawberry_seed", "bok_choy_seed", "garlic_seed", "scallion_seed",
    ]
    count = random.randint(1, min(3, len(donors) + 1))
    chosen = random.sample(_SEED_POOL, min(count, len(_SEED_POOL)))
    for seed_id in chosen:
        player._add_item(seed_id)
    names = ", ".join(seed_id.replace("_", " ").title() for seed_id in chosen)
    player.pending_notifications.append(("Gift", f"A farmer sent seeds: {names}", "uncommon"))
