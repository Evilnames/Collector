import pygame
from items import ITEMS
from item_icons import render_item_icon
from crafting import (RECIPES, BAKERY_RECIPES, WOK_RECIPES, STEAMER_RECIPES, NOODLE_POT_RECIPES,
                      BBQ_GRILL_RECIPES, CLAY_POT_RECIPES, FORGE_RECIPES, ARTISAN_RECIPES,
                      match_recipe, craft_costs, can_craft,
                      RESEARCH_LOCKED_RECIPES, is_research_locked, can_craft_with_research)
from rocks import get_refinery_equipment
from gemstones import get_fault_points, apply_cracking_result, invalidate_gem_cache
from blocks import (BAKERY_BLOCK, WOK_BLOCK, STEAMER_BLOCK, NOODLE_POT_BLOCK, BBQ_GRILL_BLOCK,
                    CLAY_POT_BLOCK, GEM_CUTTER_BLOCK, DESERT_FORGE_BLOCK,
                    ROASTER_BLOCK, BLEND_STATION_BLOCK, BREW_STATION_BLOCK, FOSSIL_TABLE_BLOCK,
                    ARTISAN_BENCH_BLOCK,
                    GRAPE_PRESS_BLOCK, FERMENTATION_BLOCK, WINE_CELLAR_BLOCK,
                    STILL_BLOCK, BARREL_ROOM_BLOCK, BOTTLING_BLOCK,
                    COMPOST_BIN_BLOCK, GARDEN_BLOCK)
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

    def handle_crafting_click(self, pos, player, button=1, research=None):
        for (r, c), rect in self._cell_rects.items():
            if rect.collidepoint(pos):
                if button == 3:
                    self._craft_grid[r][c] = None
                else:
                    self._craft_grid[r][c] = self._cycle_craft_item(r, c, player)
                return
        if button == 1 and self._craft_btn and self._craft_btn.collidepoint(pos):
            self._do_grid_craft(player, research)
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

    def _do_grid_craft(self, player, research=None):
        out_id, out_count = match_recipe(self._craft_grid)
        if out_id and can_craft_with_research(self._craft_grid, player.inventory, research):
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
            # cat 5 = bird codex (view only, no selection needed)
        # tab 2 (awards) has no click-to-select items

    def handle_scroll(self, dy):
        if self.inventory_open:
            self._inv_scroll = max(0, min(self._max_inv_scroll, self._inv_scroll - dy))
        elif self.crafting_open:
            self._recipe_scroll = max(0, min(self._max_recipe_scroll, self._recipe_scroll - dy))
        elif self.refinery_open and self.refinery_block_id == BAKERY_BLOCK:
            self._bakery_scroll = max(0, min(self._max_bakery_scroll, self._bakery_scroll - dy))
        elif self.refinery_open:
            bid = self.refinery_block_id
            cur = self._cook_station_scroll.get(bid, 0)
            self._cook_station_scroll[bid] = max(
                0, min(self._cook_station_max_scroll.get(bid, 0), cur - dy))
        elif self.collection_open:
            if self._collection_tab == 0:
                self._unified_scroll = max(0, min(self._max_unified_scroll, self._unified_scroll - dy))
            elif self._collection_tab == 1:
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
            mouse = pygame.mouse.get_pos()
            PW = 1140
            px = (SCREEN_W - PW) // 2
            if mouse[0] < px + PW // 2:
                self._garden_scroll = max(0, min(self._max_garden_scroll, self._garden_scroll - dy))
            else:
                self._player_garden_scroll = max(0, min(self._max_player_garden_scroll, self._player_garden_scroll - dy))

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

    def handle_garden_click(self, pos, player):
        flowers = self.active_garden_flowers
        garden_pos = self.active_garden_pos
        if flowers is None or garden_pos is None:
            return
        # Click on a flower in the garden → return to player collection
        for uid, rect in self._garden_rects.items():
            if rect.collidepoint(pos):
                for i, wf in enumerate(flowers):
                    if wf.uid == uid:
                        player.wildflowers.append(flowers.pop(i))
                        # Remove garden insects if now empty
                        if not flowers:
                            player.world.insects = [
                                ins for ins in player.world.insects
                                if not _is_garden_insect(ins, garden_pos)
                            ]
                        return
        # Click on a wildflower in the player collection → move to garden
        for uid, rect in self._player_garden_rects.items():
            if rect.collidepoint(pos):
                for i, wf in enumerate(player.wildflowers):
                    if wf.uid == uid:
                        was_empty = not flowers
                        flowers.append(player.wildflowers.pop(i))
                        if was_empty:
                            player.world.spawn_insects_near_garden(*garden_pos)
                        return

    def handle_npc_click(self, pos, player):
        from cities import RockQuestNPC, TradeNPC, WildflowerQuestNPC, GemQuestNPC
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
        if self.refinery_block_id == COMPOST_BIN_BLOCK:
            self._handle_compost_bin_click(pos, player)
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
