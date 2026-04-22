import pygame
from items import ITEMS
from item_icons import render_item_icon
from crafting import (RECIPES, BAKERY_RECIPES, WOK_RECIPES, STEAMER_RECIPES, NOODLE_POT_RECIPES,
                      BBQ_GRILL_RECIPES, CLAY_POT_RECIPES,
                      match_recipe, craft_costs, can_craft)
from rocks import (render_rock, render_codex_preview, RARITY_COLORS,
                   ROCK_TYPE_ORDER, ROCK_TYPE_DESCRIPTIONS, ROCK_TYPES,
                   get_refinery_equipment)
from wildflowers import (render_wildflower, get_flower_preview,
                         WILDFLOWER_TYPE_ORDER, WILDFLOWER_TYPES,
                         WILDFLOWER_BIODOME_AFFINITY)
from renderer import render_mushroom_preview
from constants import SCREEN_W, SCREEN_H, HOTBAR_SIZE, MAX_HEALTH
from blocks import (BLOCKS, BAKERY_BLOCK, WOK_BLOCK, STEAMER_BLOCK, NOODLE_POT_BLOCK, BBQ_GRILL_BLOCK, CLAY_POT_BLOCK,
                    CAVE_MUSHROOMS,
                    CAVE_MUSHROOM, EMBER_CAP, PALE_GHOST, GOLD_CHANTERELLE, COBALT_CAP,
                    MOSSY_CAP, VIOLET_CROWN, BLOOD_CAP, SULFUR_DOME, IVORY_BELL,
                    ASH_BELL, TEAL_BELL, RUST_SHELF, COPPER_SHELF, OBSIDIAN_SHELF,
                    COAL_PUFF, STONE_PUFF, AMBER_PUFF, SULFUR_TUFT, HONEY_CLUSTER,
                    CORAL_TUFT, BONE_STALK, MAGMA_CAP, DEEP_INK, BIOLUME)

_MUSHROOM_ORDER = [
    CAVE_MUSHROOM, EMBER_CAP, PALE_GHOST, GOLD_CHANTERELLE, COBALT_CAP,
    MOSSY_CAP, VIOLET_CROWN, BLOOD_CAP, SULFUR_DOME, IVORY_BELL,
    ASH_BELL, TEAL_BELL, RUST_SHELF, COPPER_SHELF, OBSIDIAN_SHELF,
    COAL_PUFF, STONE_PUFF, AMBER_PUFF, SULFUR_TUFT, HONEY_CLUSTER,
    CORAL_TUFT, BONE_STALK, MAGMA_CAP, DEEP_INK, BIOLUME,
]

_MUSHROOM_BIOME = {
    CAVE_MUSHROOM:   "All biomes",       EMBER_CAP:       "Igneous",
    PALE_GHOST:      "Void / Sedimentary", GOLD_CHANTERELLE:"Sedimentary",
    COBALT_CAP:      "Crystal / Ferrous", MOSSY_CAP:       "Sedimentary",
    VIOLET_CROWN:    "Void",              BLOOD_CAP:       "Igneous / Ferrous",
    SULFUR_DOME:     "Igneous",           IVORY_BELL:      "Crystal",
    ASH_BELL:        "Ferrous / Void",    TEAL_BELL:       "Crystal",
    RUST_SHELF:      "Igneous / Ferrous", COPPER_SHELF:    "Sedimentary",
    OBSIDIAN_SHELF:  "Void  (deep)",      COAL_PUFF:       "Igneous",
    STONE_PUFF:      "Ferrous",           AMBER_PUFF:      "Sedimentary",
    SULFUR_TUFT:     "Igneous",           HONEY_CLUSTER:   "Sedimentary",
    CORAL_TUFT:      "Crystal",           BONE_STALK:      "Ferrous",
    MAGMA_CAP:       "Igneous  (deep)",   DEEP_INK:        "Void  (deep)",
    BIOLUME:         "Crystal  (deep)",
}

_MUSHROOM_DROP_COLOR = {
    "cave_mushroom": (180, 160, 120),
    "rare_mushroom": (210, 165, 60),
    "glowing_spore": (60, 220, 200),
}

_MUSHROOM_SHAPES = {
    CAVE_MUSHROOM: "dome",    EMBER_CAP: "dome",     PALE_GHOST: "dome",
    GOLD_CHANTERELLE: "dome", COBALT_CAP: "dome",    MOSSY_CAP: "dome",
    VIOLET_CROWN: "dome",     BLOOD_CAP: "dome",     SULFUR_DOME: "dome",
    IVORY_BELL: "bell",       ASH_BELL: "bell",      TEAL_BELL: "bell",
    RUST_SHELF: "flat shelf", COPPER_SHELF: "flat shelf", OBSIDIAN_SHELF: "flat shelf",
    COAL_PUFF: "puffball",    STONE_PUFF: "puffball",AMBER_PUFF: "puffball",
    SULFUR_TUFT: "cluster",   HONEY_CLUSTER: "cluster", CORAL_TUFT: "cluster",
    BONE_STALK: "tall bell",  MAGMA_CAP: "dome",     DEEP_INK: "dome",
    BIOLUME: "dome",
}

SPECIAL_DESCS = {
    "luminous":    ("Glows in collection",    "No upgrade bonus"),
    "magnetic":    ("Crusher +2 bonus items", "Tumbler blocked"),
    "crystalline": ("Gem Cutter max yield",   "Effective hardness -2"),
    "resonant":    ("Double research XP",     "One refine only"),
    "voidtouched": ("Chance: void essence",   "1% equip damage"),
    "dense":       ("Purity +0.3 effective",  "Size one tier smaller"),
    "hollow":      ("Output count +2",        "Luster -0.3 effective"),
    "fused":       ("Unique appearance",        "No upgrade bonus"),
}

RARITY_LABEL = {
    "common": "Common", "uncommon": "Uncommon", "rare": "Rare",
    "epic": "Epic", "legendary": "Legendary",
}


class UI:
    def __init__(self, screen):
        self.screen = screen
        pygame.font.init()
        self.font  = pygame.font.SysFont("consolas", 18)
        self.small = pygame.font.SysFont("consolas", 13)
        self.research_open           = False
        self.inventory_open          = False
        self.crafting_open           = False   # C: crafting panel
        self.collection_open         = False   # G: rock collection
        self.refinery_open           = False   # E near equipment block
        self.refinery_block_id       = None
        self._selected_rock_idx      = None
        self._refinery_selected_idx  = None
        self._card_rects    = {}
        self._inv_rects     = {}
        self._recipe_rects  = {}
        self._rock_rects    = {}
        self._refine_rects  = {}
        self._refine_btn    = None
        self._collection_tab       = 0   # 0=my rocks, 1=codex, 2=my flowers, 3=flower codex, 4=mushroom codex
        self._codex_selected_type  = None
        self._tab_rects            = {}
        self._codex_rects          = {}
        self._selected_flower_idx       = None
        self._flower_rects              = {}
        self._flower_codex_rects        = {}
        self._flower_codex_selected_type = None
        self._flower_codex_scroll       = 0
        self._my_flowers_scroll         = 0
        self._max_flower_codex_scroll   = 0
        self._max_my_flowers_scroll     = 0
        self._mushroom_codex_selected_bid = None
        self._mushroom_codex_rects        = {}
        self._mushroom_codex_scroll       = 0
        self._max_mushroom_codex_scroll   = 0
        self._craft_btn     = None
        self._craft_grid    = [[None] * 3 for _ in range(3)]
        self._cell_rects    = {}
        self._hotbar_rects  = []
        self._recipe_scroll     = 0
        self._codex_scroll      = 0
        self._my_rocks_scroll   = 0
        self._max_recipe_scroll = 0
        self._max_codex_scroll  = 0
        self._max_my_rocks_scroll = 0
        self._bakery_scroll         = 0
        self._max_bakery_scroll     = 0
        self._bakery_selected_recipe = 0
        self._bakery_recipe_rects    = {}
        self._wok_selected_recipe       = 0
        self._wok_recipe_rects          = {}
        self._steamer_selected_recipe   = 0
        self._steamer_recipe_rects      = {}
        self._noodle_pot_selected_recipe = 0
        self._noodle_pot_recipe_rects   = {}
        self._bbq_grill_selected_recipe  = 0
        self._bbq_grill_recipe_rects     = {}
        self._clay_pot_selected_recipe   = 0
        self._clay_pot_recipe_rects      = {}
        self._cook_station_scroll        = {}
        self._cook_station_max_scroll    = {}
        self.npc_open   = False
        self.active_npc = None
        self._trade_rects = {}
        self._quest_btn   = None
        self.automation_open   = False
        self.active_automation = None
        self._auto_deposit1_btn    = None
        self._auto_deposit_all_btn = None
        self._auto_support1_btn    = None
        self._auto_support_all_btn = None
        self._auto_take_btn        = None
        # Chest UI
        self.chest_open       = False
        self.active_chest_inv = None   # direct reference to world.chest_data[(bx,by)]
        self.active_chest_pos = None   # (bx, by) for title display
        self._chest_rects     = {}     # item_id -> Rect  (chest side)
        self._player_for_chest_rects = {}  # item_id -> Rect  (player side)
        self._chest_scroll    = 0
        self._max_chest_scroll = 0
        self._player_chest_scroll = 0
        self._max_player_chest_scroll = 0
        # Cheat console
        self.cheat_open    = False
        self.cheat_text    = ""
        self.cheat_message = ""
        self._cheat_msg_timer = 0.0
        self._death_font  = pygame.font.SysFont("Arial Black", 72, bold=True)
        self._death_font2 = pygame.font.SysFont("Arial", 26)
        # Pause menu
        self.pause_open = False
        self._pause_btn_rects = {}
        self._pause_font  = pygame.font.SysFont("Arial Black", 56, bold=True)
        self._pause_font2 = pygame.font.SysFont("Arial Black", 30, bold=True)
        self._cheat_font  = pygame.font.SysFont("consolas", 20)
        # Drag-and-drop state for inventory → hotbar
        self._drag_item_id = None
        self._drag_pos     = (0, 0)
        self._inv_scroll     = 0
        self._max_inv_scroll = 0

    def draw(self, player, research=None, dt=0.0):
        if self._cheat_msg_timer > 0:
            self._cheat_msg_timer -= dt
        if player.dead:
            self._draw_death_screen(player)
            return
        self._draw_health(player)
        self._draw_hunger(player)
        self._draw_depth(player)
        self._draw_pick_level(player)
        self._draw_money(player)
        self._draw_mine_bar(player)
        self._draw_hints(research, player)
        if self.research_open and research:
            self._draw_research(player, research)
        if self.inventory_open:
            self._draw_inventory(player)
        if self.crafting_open:
            self._draw_crafting(player, research)
        if self.collection_open:
            self._draw_collection(player)
        if self.refinery_open and self.refinery_block_id is not None:
            self._draw_refinery(player)
        if self.npc_open and self.active_npc is not None:
            self._draw_npc_panel(player)
        if self.automation_open and self.active_automation is not None:
            self._draw_automation_panel(player)
        if self.chest_open and self.active_chest_inv is not None:
            self._draw_chest(player)
        if self.cheat_open:
            self._draw_cheat_console()
        if self.pause_open:
            self._draw_pause_menu()
        self._draw_hotbar(player)
        if self._drag_item_id is not None and self.inventory_open:
            self._draw_drag_item()

    # ------------------------------------------------------------------
    # Click handlers
    # ------------------------------------------------------------------

    def handle_research_click(self, pos, player, world, research):
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

    def handle_crafting_click(self, pos, player, button=1):
        for (r, c), rect in self._cell_rects.items():
            if rect.collidepoint(pos):
                if button == 3:
                    self._craft_grid[r][c] = None
                else:
                    self._craft_grid[r][c] = self._cycle_craft_item(r, c, player)
                return
        if button == 1 and self._craft_btn and self._craft_btn.collidepoint(pos):
            self._do_grid_craft(player)
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

    def _do_grid_craft(self, player):
        out_id, out_count = match_recipe(self._craft_grid)
        if out_id and can_craft(self._craft_grid, player.inventory):
            costs = craft_costs(self._craft_grid)
            for iid, needed in costs.items():
                player.inventory[iid] = player.inventory.get(iid, 0) - needed
                if player.inventory[iid] <= 0:
                    del player.inventory[iid]
                    for i in range(len(player.hotbar)):
                        if player.hotbar[i] == iid:
                            player.hotbar[i] = None
            for _ in range(out_count):
                player._add_item(out_id)

    def handle_collection_click(self, pos, player):
        for tab_idx, rect in self._tab_rects.items():
            if rect.collidepoint(pos):
                self._collection_tab = tab_idx
                self._selected_rock_idx = None
                self._codex_selected_type = None
                self._selected_flower_idx = None
                self._flower_codex_selected_type = None
                self._mushroom_codex_selected_bid = None
                self._codex_scroll = 0
                self._my_rocks_scroll = 0
                self._flower_codex_scroll = 0
                self._my_flowers_scroll = 0
                self._mushroom_codex_scroll = 0
                return
        if self._collection_tab == 0:
            for idx, rect in self._rock_rects.items():
                if rect.collidepoint(pos):
                    self._selected_rock_idx = idx if self._selected_rock_idx != idx else None
                    return
        elif self._collection_tab == 1:
            for type_key, rect in self._codex_rects.items():
                if rect.collidepoint(pos):
                    self._codex_selected_type = type_key if self._codex_selected_type != type_key else None
                    return
        elif self._collection_tab == 2:
            for idx, rect in self._flower_rects.items():
                if rect.collidepoint(pos):
                    self._selected_flower_idx = idx if self._selected_flower_idx != idx else None
                    return
        elif self._collection_tab == 3:
            for type_key, rect in self._flower_codex_rects.items():
                if rect.collidepoint(pos):
                    self._flower_codex_selected_type = type_key if self._flower_codex_selected_type != type_key else None
                    return
        else:
            for bid, rect in self._mushroom_codex_rects.items():
                if rect.collidepoint(pos):
                    self._mushroom_codex_selected_bid = bid if self._mushroom_codex_selected_bid != bid else None
                    return

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
                self._my_rocks_scroll = max(0, min(self._max_my_rocks_scroll, self._my_rocks_scroll - dy))
            elif self._collection_tab == 1:
                self._codex_scroll = max(0, min(self._max_codex_scroll, self._codex_scroll - dy))
            elif self._collection_tab == 2:
                self._my_flowers_scroll = max(0, min(self._max_my_flowers_scroll, self._my_flowers_scroll - dy))
            elif self._collection_tab == 3:
                self._flower_codex_scroll = max(0, min(self._max_flower_codex_scroll, self._flower_codex_scroll - dy))
            else:
                self._mushroom_codex_scroll = max(0, min(self._max_mushroom_codex_scroll, self._mushroom_codex_scroll - dy))
        elif self.chest_open:
            mouse = pygame.mouse.get_pos()
            PW = 1140
            px = (SCREEN_W - PW) // 2
            if mouse[0] < px + PW // 2:
                self._chest_scroll = max(0, min(self._max_chest_scroll, self._chest_scroll - dy))
            else:
                self._player_chest_scroll = max(0, min(self._max_player_chest_scroll, self._player_chest_scroll - dy))

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

    def handle_npc_click(self, pos, player):
        from cities import RockQuestNPC, TradeNPC
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

    def handle_refinery_click(self, pos, player):
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
        for idx, rect in self._refine_rects.items():
            if rect.collidepoint(pos):
                self._refinery_selected_idx = idx
                return
        if self._refine_btn and self._refine_btn.collidepoint(pos):
            self._do_refine(player)

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
        for _ in range(recipe["output_count"]):
            player._add_item(recipe["output_id"])

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
        for _ in range(recipe["output_count"]):
            player._add_item(recipe["output_id"])

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

    # ------------------------------------------------------------------
    # HUD
    # ------------------------------------------------------------------

    def _draw_health(self, player):
        bw, bh = 180, 18
        x, y = 10, 10
        pygame.draw.rect(self.screen, (70, 10, 10), (x, y, bw, bh))
        hp_w = int(bw * player.health / MAX_HEALTH)
        r = 255 - int(200 * player.health / MAX_HEALTH)
        g = int(180 * player.health / MAX_HEALTH)
        pygame.draw.rect(self.screen, (r, g, 20), (x, y, hp_w, bh))
        pygame.draw.rect(self.screen, (220, 220, 220), (x, y, bw, bh), 1)
        txt = self.small.render(f"HP {player.health}/{MAX_HEALTH}", True, (255, 255, 255))
        self.screen.blit(txt, (x + 4, y + 2))

    def _draw_hunger(self, player):
        bw, bh = 180, 18
        x, y = 10, 34
        pygame.draw.rect(self.screen, (50, 35, 10), (x, y, bw, bh))
        hng_w = int(bw * player.hunger / 100.0)
        frac = player.hunger / 100.0
        if frac > 0.5:
            t = (frac - 0.5) * 2.0
            r, g = int(255 * (1.0 - t)), 200
        else:
            t = frac * 2.0
            r, g = 255, int(200 * t)
        pygame.draw.rect(self.screen, (r, g, 10), (x, y, hng_w, bh))
        pygame.draw.rect(self.screen, (200, 200, 200), (x, y, bw, bh), 1)
        txt = self.small.render(f"Food {int(player.hunger)}%", True, (255, 255, 255))
        self.screen.blit(txt, (x + 4, y + 2))

    def _draw_depth(self, player):
        depth = player.get_depth()
        txt = self.font.render(f"Depth: {depth} m", True, (230, 230, 230))
        self.screen.blit(txt, (SCREEN_W - txt.get_width() - 10, 10))

    def _draw_pick_level(self, player):
        ep = player.effective_pick_power
        tiers = [(6, "Obsidian Pick"), (5, "Ruby Pick"), (4, "Crystal Pick"),
                 (3, "Gold Pick"), (2, "Iron Pick"), (1.4, "Stone Pick")]
        label = next((name for thresh, name in tiers if ep >= thresh), "Wood Pick")
        txt = self.small.render(label, True, (200, 200, 150))
        self.screen.blit(txt, (SCREEN_W - txt.get_width() - 10, 32))

    def _draw_hotbar(self, player):
        slot_sz = 48
        gap = 4
        total_w = HOTBAR_SIZE * (slot_sz + gap) - gap
        start_x = (SCREEN_W - total_w) // 2
        y = SCREEN_H - slot_sz - 10
        self._hotbar_rects = []

        for i in range(HOTBAR_SIZE):
            x = start_x + i * (slot_sz + gap)
            self._hotbar_rects.append(pygame.Rect(x, y, slot_sz, slot_sz))
            selected = (i == player.selected_slot)
            pygame.draw.rect(self.screen, (60, 60, 60), (x, y, slot_sz, slot_sz))
            bdr = (220, 200, 50) if selected else (140, 140, 140)
            pygame.draw.rect(self.screen, bdr, (x, y, slot_sz, slot_sz), 3 if selected else 2)

            item_id = player.hotbar[i]
            if item_id and item_id in ITEMS:
                item = ITEMS[item_id]
                swatch = slot_sz - 14
                max_uses = item.get("max_uses")
                sw_h = (swatch - 2) if not max_uses else (swatch - 7)
                icon_sz = min(swatch, sw_h)
                icon = render_item_icon(item_id, item["color"], icon_sz)
                self.screen.blit(icon, (x + 5, y + 5))
                count = player.inventory.get(item_id, 0)
                ctxt = self.small.render(str(count), True, (255, 255, 255))
                self.screen.blit(ctxt, (x + slot_sz - ctxt.get_width() - 3, y + slot_sz - 15))
                if max_uses:
                    uses_left = player.hotbar_uses[i] or 0
                    frac = max(0.0, uses_left / max_uses)
                    bar_x, bar_y, bar_w = x + 5, y + 5 + sw_h + 2, swatch
                    pygame.draw.rect(self.screen, (40, 40, 40), (bar_x, bar_y, bar_w, 4))
                    fill_w = max(1, int(bar_w * frac))
                    gr = int(200 * frac)
                    rr = int(200 * (1 - frac))
                    pygame.draw.rect(self.screen, (rr, gr, 0), (bar_x, bar_y, fill_w, 4))
                if selected:
                    name_txt = self.small.render(item["name"], True, (200, 200, 200))
                    nx = (SCREEN_W - name_txt.get_width()) // 2
                    self.screen.blit(name_txt, (nx, y - 18))

    def _draw_mine_bar(self, player):
        if not player.mining_block or player.mine_progress <= 0:
            return
        bw, bh = 160, 14
        x = SCREEN_W // 2 - bw // 2
        y = SCREEN_H // 2 + 50
        pygame.draw.rect(self.screen, (30, 30, 30), (x, y, bw, bh))
        pygame.draw.rect(self.screen, (60, 210, 60), (x, y, int(bw * player.mine_progress), bh))
        pygame.draw.rect(self.screen, (200, 200, 200), (x, y, bw, bh), 1)
        txt = self.small.render("Mining...", True, (220, 220, 220))
        self.screen.blit(txt, (x + bw // 2 - txt.get_width() // 2, y - 16))

    def _draw_money(self, player):
        txt = self.font.render(f"$ {player.money}", True, (240, 210, 50))
        self.screen.blit(txt, (SCREEN_W - txt.get_width() - 10, 48))

    def _draw_hints(self, research, player):
        nearby_bed = player.get_nearby_bed()
        hints = [
            ("R: Research", self.research_open or (
                research and any(research.can_unlock(nid, player.inventory, player.money)
                                 for nid in research.nodes))),
            ("I: Inventory",  self.inventory_open),
            ("C: Craft",      self.crafting_open),
            ("G: Collection",  self.collection_open),
            ("E: Talk",       self.npc_open),
            ("E: Refinery",   self.refinery_open),
            ("E: Chest",      self.chest_open),
            ("E: Set Spawn",  nearby_bed is not None),
            ("`  Cheats",     self.cheat_open),
        ]
        y = 68
        for label, active in hints:
            color = (220, 200, 50) if active else (130, 130, 130)
            txt = self.small.render(label, True, color)
            self.screen.blit(txt, (SCREEN_W - txt.get_width() - 10, y))
            y += 16
        if player.spawn_x is not None:
            sp = self.small.render("* Bed spawn set", True, (100, 200, 100))
            self.screen.blit(sp, (SCREEN_W - sp.get_width() - 10, y + 4))
        if player.god_mode:
            god = self.small.render("GOD MODE", True, (255, 220, 50))
            self.screen.blit(god, (SCREEN_W - god.get_width() - 10, y + 20))

    # ------------------------------------------------------------------
    # NPC interaction panel
    # ------------------------------------------------------------------

    def _draw_npc_panel(self, player):
        from cities import RockQuestNPC, TradeNPC
        from rocks import RARITY_COLORS, ROCK_TYPES
        npc = self.active_npc

        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        self.screen.blit(overlay, (0, 0))

        from cities import RockQuestNPC as _RQN
        PW = 660
        PH = 490 if isinstance(npc, _RQN) else 460
        px = (SCREEN_W - PW) // 2
        py = (SCREEN_H - PH) // 2
        pygame.draw.rect(self.screen, (22, 22, 30), (px, py, PW, PH))
        pygame.draw.rect(self.screen, (120, 100, 60), (px, py, PW, PH), 2)

        hint = self.small.render("E or ESC to close", True, (100, 100, 110))
        self.screen.blit(hint, (px + PW - hint.get_width() - 8, py + 8))

        if isinstance(npc, RockQuestNPC):
            self._draw_quest_content(player, npc, px, py, PW, PH)
        elif isinstance(npc, TradeNPC):
            self._draw_trade_content(player, npc, px, py, PW, PH)

    def _draw_quest_content(self, player, npc, px, py, PW, PH):
        from cities import quest_display, quest_hint, RARITY_ORDER
        from rocks import RARITY_COLORS

        DIFF_LABELS = {0: "Novice", 1: "Journeyman", 2: "Expert"}
        diff_col    = {0: (120, 190, 120), 1: (190, 170, 80), 2: (210, 80, 80)}
        title_txt = f"ROCK COLLECTOR  [{DIFF_LABELS[npc.difficulty]}]"
        title = self.font.render(title_txt, True, diff_col[npc.difficulty])
        self.screen.blit(title, (px + PW // 2 - title.get_width() // 2, py + 10))

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

            can = npc.can_complete(player, quest_idx)
            bg  = (25, 40, 20) if can else (22, 22, 30)
            bdr = (60, 160, 60) if can else (70, 60, 80)
            pygame.draw.rect(self.screen, bg, row_rect)
            pygame.draw.rect(self.screen, bdr, row_rect, 2)

            iy = y + 10
            # Quest type badge
            kind_labels = {"single": "SPECIFIC", "any_rarity": "ANY RARITY",
                           "quantity": "BULK", "special": "SPECIAL TRAIT"}
            badge_col   = {"single": (120, 120, 180), "any_rarity": (100, 160, 200),
                           "quantity": (160, 120, 60), "special": (160, 80, 180)}
            badge = self.small.render(kind_labels.get(quest["kind"], "QUEST"), True,
                                      badge_col.get(quest["kind"], (150, 150, 150)))
            self.screen.blit(badge, (px + 22, iy))
            iy += 18

            # Quest description line — coloured by rarity if applicable
            desc = quest_display(quest)
            rarity_col = (220, 220, 220)
            if quest["kind"] == "single":
                rarity_col = RARITY_COLORS.get(quest["rarity"], rarity_col)
            elif quest["kind"] == "any_rarity":
                rarity_col = RARITY_COLORS.get(quest["min_rarity"], rarity_col)
            self.screen.blit(self.font.render(desc, True, rarity_col), (px + 22, iy))
            iy += 24

            # Hint line
            hint = quest_hint(quest)
            self.screen.blit(self.small.render(hint, True, (140, 150, 170)), (px + 22, iy))
            iy += 20

            # Match status
            matching = npc.find_matching_rocks(player, quest)
            needed   = quest.get("count", 1)
            if len(matching) >= needed:
                status = f"Ready!  ({len(matching)} matching in collection)"
                status_col = (80, 220, 80)
            else:
                status = f"Need {needed}  —  you have {len(matching)}"
                status_col = (180, 90, 90)
            self.screen.blit(self.small.render(status, True, status_col), (px + 22, iy))
            iy += 18

            # Reward + streak bonus preview
            streak_bonus = min(npc._streak, 2) * 25
            reward_str = f"Reward: {quest['reward']} gold"
            if streak_bonus:
                bonus_val = int(quest["reward"] * (1 + streak_bonus / 100)) - quest["reward"]
                reward_str += f"  (+{bonus_val} streak bonus)"
            self.screen.blit(self.font.render(reward_str, True, (240, 210, 50)), (px + 22, iy))

            # Hand-over button (right side of row)
            BW, BH = 170, 36
            bx2 = px + PW - BW - 20
            by2 = y + row_h // 2 - BH // 2
            btn_rect = pygame.Rect(bx2, by2, BW, BH)
            self._trade_rects[quest_idx] = btn_rect
            if len(matching) >= needed:
                b_bg, b_bdr, b_tc = (18, 90, 18), (45, 200, 45), (190, 255, 190)
            else:
                b_bg, b_bdr, b_tc = (30, 30, 36), (55, 55, 68), (70, 70, 82)
            pygame.draw.rect(self.screen, b_bg, btn_rect)
            pygame.draw.rect(self.screen, b_bdr, btn_rect, 2)
            bl = self.small.render("HAND OVER", True, b_tc)
            self.screen.blit(bl, (bx2 + BW // 2 - bl.get_width() // 2,
                                   by2 + BH // 2 - bl.get_height() // 2))

            y += row_h + 8

    def _draw_trade_content(self, player, npc, px, py, PW, PH):
        title = self.font.render("TRADER", True, (80, 210, 160))
        self.screen.blit(title, (px + PW // 2 - title.get_width() // 2, py + 10))

        self._trade_rects.clear()
        y = py + 52

        for i, (item_id, give_count, receive_gold) in enumerate(npc.trades):
            can = npc.can_trade(i, player)
            have = player.inventory.get(item_id, 0)
            item_name = ITEMS.get(item_id, {}).get("name", item_id)

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
                self.font.render(f"Receive: {receive_gold} gold", True, (240, 210, 50)),
                (px + 68, y + 32))

            lbl = self.font.render("TRADE", True, (190, 255, 190) if can else (70, 70, 82))
            self.screen.blit(lbl, (rect.right - lbl.get_width() - 10,
                                    y + row_h // 2 - lbl.get_height() // 2))
            y += row_h + 8

    # ------------------------------------------------------------------
    # Research overlay (4 columns)
    # ------------------------------------------------------------------

    def _draw_research(self, player, research):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("RESEARCH TREE", True, (255, 220, 50))
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("R to close  |  Click an available upgrade to unlock it",
                                 True, (150, 150, 150))
        self.screen.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, 26))

        n_cols = len(research.COLUMNS)
        CARD_W, CARD_H = 260, 92
        COL_GAP, ROW_GAP = 18, 7
        total_w = n_cols * CARD_W + (n_cols - 1) * COL_GAP
        col_x = [(SCREEN_W - total_w) // 2 + c * (CARD_W + COL_GAP) for c in range(n_cols)]
        header_y = 46

        for c, label in enumerate(research.COLUMNS):
            hdr = self.small.render(label, True, (190, 190, 190))
            self.screen.blit(hdr, (col_x[c], header_y))

        self._card_rects.clear()
        for col, row, node_id in research.layout:
            node = research.nodes[node_id]
            x = col_x[col]
            y = header_y + 18 + row * (CARD_H + ROW_GAP)
            rect = pygame.Rect(x, y, CARD_W, CARD_H)
            self._card_rects[node_id] = rect

            prereqs_ok = research.prereqs_met(node_id)
            can = research.can_unlock(node_id, player.inventory, player.money)

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

            pygame.draw.rect(self.screen, bg, rect)
            pygame.draw.rect(self.screen, border, rect, 2)
            self.screen.blit(self.font.render(node.name, True, (255, 255, 220)), (x + 6, y + 5))
            st_surf = self.small.render(status_txt, True, status_col)
            self.screen.blit(st_surf, (x + CARD_W - st_surf.get_width() - 6, y + 8))
            self.screen.blit(self.small.render(node.description, True, (150, 150, 150)), (x + 6, y + 27))

            if not node.unlocked:
                if not prereqs_ok:
                    blocked = [research.nodes[p].name for p in node.prerequisites
                               if not research.nodes[p].unlocked]
                    req_surf = self.small.render("Requires: " + ", ".join(blocked[:2]),
                                                 True, (160, 80, 80))
                    self.screen.blit(req_surf, (x + 6, y + 50))
                else:
                    cx2 = x + 6
                    for item_id, needed in node.cost.items():
                        have = player.inventory.get(item_id, 0)
                        iname = ITEMS.get(item_id, {}).get("name", item_id)
                        col_c = (70, 200, 70) if have >= needed else (210, 80, 80)
                        cs = self.small.render(f"{iname}: {have}/{needed}", True, col_c)
                        self.screen.blit(cs, (cx2, y + 50))
                        cx2 += cs.get_width() + 10
                    if node.money_cost > 0:
                        col_m = (70, 200, 70) if player.money >= node.money_cost else (210, 80, 80)
                        ms = self.small.render(f"Gold: {player.money}/{node.money_cost}", True, col_m)
                        self.screen.blit(ms, (cx2, y + 50))

            if row > 0 and prereqs_ok and not node.unlocked:
                mid_x = x + CARD_W // 2
                pygame.draw.line(self.screen, border, (mid_x, y - ROW_GAP), (mid_x, y), 1)

    # ------------------------------------------------------------------
    # Inventory overlay
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Crafting overlay (C key) — 3x3 grid left, equipment recipes right
    # ------------------------------------------------------------------

    def _draw_crafting(self, player, research):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        PW, PH = 1240, 570
        px = (SCREEN_W - PW) // 2
        py = (SCREEN_H - PH) // 2
        pygame.draw.rect(self.screen, (22, 22, 30), (px, py, PW, PH))
        pygame.draw.rect(self.screen, (80, 80, 105), (px, py, PW, PH), 2)

        title = self.font.render("CRAFTING", True, (220, 220, 100))
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, py + 6))
        hint_s = self.small.render(
            "Left-click cell: cycle item  |  Right-click: clear  |  C or ESC: close",
            True, (100, 100, 115))
        self.screen.blit(hint_s, (SCREEN_W // 2 - hint_s.get_width() // 2, py + 26))

        # ---- Left: 3x3 grid ----
        CELL, CGAP = 70, 6
        GW = 3 * CELL + 2 * CGAP
        gx, gy = px + 20, py + 50
        self._cell_rects.clear()

        for r in range(3):
            for c in range(3):
                cx = gx + c * (CELL + CGAP)
                cy = gy + r * (CELL + CGAP)
                item_id = self._craft_grid[r][c]
                rect = pygame.Rect(cx, cy, CELL, CELL)
                self._cell_rects[(r, c)] = rect
                if item_id and item_id in ITEMS:
                    item = ITEMS[item_id]
                    pygame.draw.rect(self.screen, (45, 50, 56), rect)
                    pygame.draw.rect(self.screen, (110, 110, 132), rect, 2)
                    sw = CELL - 16
                    icon = render_item_icon(item_id, item["color"], sw)
                    self.screen.blit(icon, (cx + 6, cy + 6))
                    ns = self.small.render(item["name"].split()[0], True, (190, 190, 190))
                    self.screen.blit(ns, (cx + CELL // 2 - ns.get_width() // 2, cy + CELL - 15))
                else:
                    pygame.draw.rect(self.screen, (28, 28, 36), rect)
                    pygame.draw.rect(self.screen, (52, 52, 66), rect, 1)
                    ps = self.small.render("+", True, (52, 52, 66))
                    self.screen.blit(ps, (cx + CELL // 2 - ps.get_width() // 2,
                                          cy + CELL // 2 - ps.get_height() // 2))

        arr = self.font.render("->", True, (110, 110, 110))
        self.screen.blit(arr, (gx + GW + 12, gy + GW // 2 - arr.get_height() // 2))

        OUT = 76
        ox, oy = gx + GW + 46, gy + (GW - OUT) // 2
        out_id, out_count = match_recipe(self._craft_grid)
        craftable = can_craft(self._craft_grid, player.inventory)

        if out_id and out_id in ITEMS:
            out_item = ITEMS[out_id]
            pygame.draw.rect(self.screen, (20, 50, 20) if craftable else (42, 28, 28), (ox, oy, OUT, OUT))
            pygame.draw.rect(self.screen, (55, 200, 55) if craftable else (140, 75, 75), (ox, oy, OUT, OUT), 2)
            sw = OUT - 14
            icon = render_item_icon(out_id, out_item["color"], sw)
            self.screen.blit(icon, (ox + 5, oy + 5))
            cnt_s = self.small.render(f"x{out_count}", True, (200, 200, 200))
            self.screen.blit(cnt_s, (ox + OUT - cnt_s.get_width() - 4, oy + OUT - 14))
        else:
            pygame.draw.rect(self.screen, (25, 25, 33), (ox, oy, OUT, OUT))
            pygame.draw.rect(self.screen, (52, 52, 66), (ox, oy, OUT, OUT), 1)
            qs = self.font.render("?", True, (55, 55, 70))
            self.screen.blit(qs, (ox + OUT // 2 - qs.get_width() // 2,
                                  oy + OUT // 2 - qs.get_height() // 2))

        self.screen.blit(self.small.render("Output", True, (85, 85, 105)),
                         (ox + OUT // 2 - self.small.size("Output")[0] // 2, oy + OUT + 4))

        BW, BH = 100, 32
        bx = ox + (OUT - BW) // 2
        by = oy + OUT + 22
        if craftable:
            bbg, bbdr, btxt = (18, 90, 18), (45, 190, 45), (190, 255, 190)
        else:
            bbg, bbdr, btxt = (30, 30, 36), (55, 55, 68), (70, 70, 82)
        self._craft_btn = pygame.Rect(bx, by, BW, BH)
        pygame.draw.rect(self.screen, bbg, self._craft_btn)
        pygame.draw.rect(self.screen, bbdr, self._craft_btn, 2)
        cl = self.font.render("CRAFT", True, btxt)
        self.screen.blit(cl, (bx + BW // 2 - cl.get_width() // 2,
                               by + BH // 2 - cl.get_height() // 2))

        info_x, info_y = ox + OUT + 12, gy
        if out_id:
            self.screen.blit(self.small.render("Materials:", True, (150, 150, 150)),
                             (info_x, info_y))
            info_y += 18
            for iid, needed in craft_costs(self._craft_grid).items():
                have = player.inventory.get(iid, 0)
                col = (65, 200, 65) if have >= needed else (210, 75, 75)
                ms = self.small.render(f"{ITEMS.get(iid,{}).get('name',iid)}: {have}/{needed}", True, col)
                self.screen.blit(ms, (info_x, info_y))
                info_y += 15
        elif any(self._craft_grid[r][c] for r in range(3) for c in range(3)):
            self.screen.blit(self.small.render("No recipe.", True, (130, 75, 75)),
                             (info_x, info_y))

        # Inventory strip below grid
        div_y = gy + GW + 14
        pygame.draw.line(self.screen, (58, 58, 72), (px + 10, div_y), (px + 490, div_y), 1)
        self.screen.blit(self.small.render("Inventory:", True, (100, 100, 120)), (gx, div_y + 5))
        MI, MIGAP = 44, 4
        items_held = sorted(
            [(iid, cnt) for iid, cnt in player.inventory.items() if cnt > 0],
            key=lambda t: ITEMS.get(t[0], {}).get("name", t[0]),
        )
        inv_cols = (490 - (gx - px)) // (MI + MIGAP)
        for idx, (iid, cnt) in enumerate(items_held):
            col = idx % inv_cols
            row = idx // inv_cols
            sx = gx + col * (MI + MIGAP)
            sy = div_y + 20 + row * (MI + MIGAP)
            itm = ITEMS.get(iid, {})
            pygame.draw.rect(self.screen, (30, 30, 38), (sx, sy, MI, MI))
            pygame.draw.rect(self.screen, (62, 62, 78), (sx, sy, MI, MI), 1)
            sw = MI - 10
            icon = render_item_icon(iid, itm.get("color", (80, 80, 80)), sw)
            self.screen.blit(icon, (sx + 4, sy + 4))
            cs = self.small.render(str(cnt), True, (200, 200, 200))
            self.screen.blit(cs, (sx + MI - cs.get_width() - 2, sy + MI - 13))

        # ---- Vertical divider ----
        div_vx = px + 500
        pygame.draw.line(self.screen, (65, 65, 85), (div_vx, py + 10), (div_vx, py + PH - 10), 1)

        # ---- Right: Recipe Book ----
        rb_hdr = self.small.render("Recipes  (click to fill grid)", True, (160, 150, 100))
        self.screen.blit(rb_hdr, (div_vx + 10, py + 10))

        MINI, MINIGAP = 13, 2
        MINIGW = 3 * MINI + 2 * MINIGAP
        RCARD_H = MINIGW + 10
        RCARD_W = PW - 510 - 10
        rx0 = div_vx + 10
        ry0 = py + 28

        RCARD_STEP = RCARD_H + 5
        panel_bottom = py + PH - 6
        visible_count = (panel_bottom - ry0) // RCARD_STEP
        self._max_recipe_scroll = max(0, len(RECIPES) - visible_count)
        self._recipe_scroll = max(0, min(self._max_recipe_scroll, self._recipe_scroll))

        # Scrollbar
        if self._max_recipe_scroll > 0:
            sb_x = px + PW - 10
            sb_h = panel_bottom - ry0
            sb_th = max(20, sb_h * visible_count // len(RECIPES))
            sb_top = ry0 + (sb_h - sb_th) * self._recipe_scroll // self._max_recipe_scroll
            pygame.draw.rect(self.screen, (35, 35, 48), (sb_x, ry0, 7, sb_h))
            pygame.draw.rect(self.screen, (100, 100, 140), (sb_x, sb_top, 7, sb_th))

        self._recipe_rects.clear()
        for ridx, recipe in enumerate(RECIPES):
            display_idx = ridx - self._recipe_scroll
            if display_idx < 0:
                continue
            ry = ry0 + display_idx * RCARD_STEP
            if ry + RCARD_H > panel_bottom:
                break
            rect = pygame.Rect(rx0, ry, RCARD_W, RCARD_H)
            self._recipe_rects[ridx] = rect

            out_id = recipe["output_id"]
            craftable_r = can_craft(recipe["pattern"], player.inventory)
            bg = (20, 45, 20) if craftable_r else (24, 24, 32)
            border = (50, 180, 50) if craftable_r else (52, 52, 68)
            pygame.draw.rect(self.screen, bg, rect)
            pygame.draw.rect(self.screen, border, rect, 1)

            # Mini 3x3 pattern
            for mr in range(3):
                for mc in range(3):
                    cell_item = recipe["pattern"][mr][mc]
                    mcx = rx0 + 4 + mc * (MINI + MINIGAP)
                    mcy = ry + 4 + mr * (MINI + MINIGAP)
                    if cell_item and cell_item in ITEMS:
                        pygame.draw.rect(self.screen, ITEMS[cell_item]["color"],
                                         (mcx, mcy, MINI, MINI))
                    else:
                        pygame.draw.rect(self.screen, (30, 30, 40), (mcx, mcy, MINI, MINI))
                    pygame.draw.rect(self.screen, (55, 55, 70), (mcx, mcy, MINI, MINI), 1)

            # Arrow
            arr_x = rx0 + 4 + MINIGW + 6
            arr_s = self.small.render("->", True, (100, 100, 100))
            self.screen.blit(arr_s, (arr_x, ry + RCARD_H // 2 - arr_s.get_height() // 2))

            # Output swatch
            sw = MINI * 2 + MINIGAP
            out_x = arr_x + arr_s.get_width() + 6
            out_y = ry + (RCARD_H - sw) // 2
            out_item = ITEMS.get(out_id, {})
            icon = render_item_icon(out_id, out_item.get("color", (80, 80, 80)), sw)
            self.screen.blit(icon, (out_x, out_y))

            # Name + cost summary
            name_x = out_x + sw + 8
            nm_s = self.small.render(recipe["name"], True, (220, 210, 170) if craftable_r else (140, 140, 150))
            self.screen.blit(nm_s, (name_x, ry + 4))
            costs = craft_costs(recipe["pattern"])
            cost_parts = []
            for iid, cnt in costs.items():
                have = player.inventory.get(iid, 0)
                col_c = (70, 200, 70) if have >= cnt else (190, 70, 70)
                cs = self.small.render(f"{ITEMS.get(iid,{}).get('name',iid)} {have}/{cnt}", True, col_c)
                self.screen.blit(cs, (name_x, ry + 4 + 14 * (len(cost_parts) + 1)))
                cost_parts.append(iid)


    # ------------------------------------------------------------------
    # Collection overlay (G key) — four tabs: My Rocks / Codex / My Flowers / Flower Codex
    # ------------------------------------------------------------------

    def _draw_collection(self, player):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        self.screen.blit(overlay, (0, 0))

        n_rock_disc = len(player.discovered_types)
        n_rock_total = len(ROCK_TYPE_ORDER)
        n_fl_disc = len(player.discovered_flower_types)
        n_fl_total = len(WILDFLOWER_TYPE_ORDER)
        n_mush_disc = len(player.discovered_mushroom_types)
        n_mush_total = len(_MUSHROOM_ORDER)

        is_flowers   = self._collection_tab in (2, 3)
        is_mushrooms = self._collection_tab == 4
        if is_mushrooms:
            title_text = "MUSHROOM CODEX"
            title_col  = (200, 230, 150)
        elif is_flowers:
            title_text = "WILDFLOWER COLLECTION"
            title_col  = (180, 255, 180)
        else:
            title_text = "ROCK COLLECTION"
            title_col  = (180, 220, 255)
        title = self.font.render(title_text, True, title_col)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 4))

        # Tab buttons
        self._tab_rects.clear()
        TAB_W, TAB_H = 160, 26
        tab_y = 24
        tab_labels = [
            f"MY ROCKS ({len(player.rocks)})",
            f"CODEX ({n_rock_disc}/{n_rock_total})",
            f"MY FLOWERS ({len(player.wildflowers)})",
            f"FLOWER CODEX ({n_fl_disc}/{n_fl_total})",
            f"MUSHROOMS ({n_mush_disc}/{n_mush_total})",
        ]
        total_tabs_w = len(tab_labels) * TAB_W + (len(tab_labels) - 1) * 6
        tab_x0 = SCREEN_W // 2 - total_tabs_w // 2
        for i, label in enumerate(tab_labels):
            tx = tab_x0 + i * (TAB_W + 6)
            rect = pygame.Rect(tx, tab_y, TAB_W, TAB_H)
            self._tab_rects[i] = rect
            active = (i == self._collection_tab)
            flower_tab = i in (2, 3)
            mush_tab   = i == 4
            if active:
                bg     = (38, 42, 18) if mush_tab else (40, 75, 45) if flower_tab else (45, 60, 80)
                border = (165, 150, 65) if mush_tab else (100, 210, 120) if flower_tab else (100, 160, 220)
            else:
                bg     = (22, 24, 10) if mush_tab else (25, 35, 27) if flower_tab else (25, 30, 40)
                border = (80, 72, 32) if mush_tab else (55, 90, 60) if flower_tab else (55, 65, 80)
            pygame.draw.rect(self.screen, bg, rect)
            pygame.draw.rect(self.screen, border, rect, 2)
            ls = self.small.render(label, True,
                                   (210, 200, 120) if (active and mush_tab)
                                   else (200, 240, 205) if (active and flower_tab)
                                   else (220, 230, 255) if active
                                   else (95, 86, 38) if mush_tab
                                   else (90, 130, 95) if flower_tab
                                   else (110, 120, 135))
            self.screen.blit(ls, (tx + TAB_W // 2 - ls.get_width() // 2,
                                   tab_y + TAB_H // 2 - ls.get_height() // 2))

        hint_text = ("G or ESC to close  |  Click a mushroom to inspect"
                     if is_mushrooms else
                     "G or ESC to close  |  Click a flower to inspect"
                     if is_flowers else
                     "G or ESC to close  |  Click a rock to inspect")
        hint = self.small.render(hint_text, True, (90, 95, 105))
        self.screen.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, tab_y + TAB_H + 2))

        if self._collection_tab == 0:
            self._draw_my_rocks(player)
        elif self._collection_tab == 1:
            self._draw_codex(player)
        elif self._collection_tab == 2:
            self._draw_my_flowers(player)
        elif self._collection_tab == 3:
            self._draw_flower_codex(player)
        else:
            self._draw_mushroom_codex(player)

    def _draw_my_rocks(self, player):
        if not player.rocks:
            msg = self.font.render("No rocks yet.  Mine Rock Deposits underground!", True, (80, 80, 90))
            self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2 - 10))
            return

        CELL, GAP, COLS = 82, 8, 8
        gx0 = (SCREEN_W - (COLS * CELL + (COLS - 1) * GAP)) // 2
        gy0 = 58

        detail_x = None
        if self._selected_rock_idx is not None and self._selected_rock_idx < len(player.rocks):
            detail_x = SCREEN_W - 340
            COLS = max(1, (detail_x - gx0 - 10) // (CELL + GAP))

        self._rock_rects.clear()
        for idx, rock in enumerate(player.rocks):
            col = idx % COLS
            row = idx // COLS
            x = gx0 + col * (CELL + GAP)
            y = gy0 + row * (CELL + GAP)
            if y + CELL > SCREEN_H - 8:
                break
            rect = pygame.Rect(x, y, CELL, CELL)
            self._rock_rects[idx] = rect

            selected = (idx == self._selected_rock_idx)
            rar_col = RARITY_COLORS[rock.rarity]
            pygame.draw.rect(self.screen, (45, 42, 60) if selected else (30, 30, 40), rect)
            pygame.draw.rect(self.screen, rar_col, rect, 3 if selected else 2)
            img = render_rock(rock, 58)
            self.screen.blit(img, (x + (CELL - 58) // 2, y + (CELL - 58) // 2 - 6))
            type_s = self.small.render(rock.base_type.replace("_", " "), True, (160, 160, 160))
            self.screen.blit(type_s, (x + CELL // 2 - type_s.get_width() // 2, y + CELL - 14))

        if detail_x is None:
            return

        rock = player.rocks[self._selected_rock_idx]
        dx, dy = detail_x, gy0
        dw, dh = SCREEN_W - dx - 8, SCREEN_H - gy0 - 10
        pygame.draw.rect(self.screen, (22, 22, 32), (dx, dy, dw, dh))
        pygame.draw.rect(self.screen, RARITY_COLORS[rock.rarity], (dx, dy, dw, dh), 2)
        img_big = render_rock(rock, 80)
        self.screen.blit(img_big, (dx + dw // 2 - 40, dy + 8))

        iy = [dy + 96]

        def dlabel(text, color=(220, 220, 200)):
            s = self.small.render(text, True, color)
            self.screen.blit(s, (dx + 8, iy[0]))
            iy[0] += 15

        dlabel(rock.base_type.replace("_", " ").title(), (240, 200, 100))
        dlabel(RARITY_LABEL[rock.rarity], RARITY_COLORS[rock.rarity])
        dlabel(f"Size: {rock.size.title()}")
        dlabel(f"Found at: {rock.depth_found}m depth")
        dlabel(f"Pattern: {rock.pattern}")
        iy[0] += 4

        def stat_bar(label, val, col=(80, 160, 220)):
            ls = self.small.render(label, True, (160, 160, 160))
            self.screen.blit(ls, (dx + 8, iy[0]))
            bx2 = dx + 80
            bw = dw - 90
            pygame.draw.rect(self.screen, (35, 35, 45), (bx2, iy[0] + 2, bw, 8))
            pygame.draw.rect(self.screen, col, (bx2, iy[0] + 2, int(bw * val), 8))
            vs = self.small.render(f"{val:.2f}", True, (180, 180, 180))
            self.screen.blit(vs, (bx2 + bw + 4, iy[0]))
            iy[0] += 16

        stat_bar("Hardness", rock.hardness / 10, (200, 100, 50))
        stat_bar("Luster",   rock.luster,         (100, 200, 220))
        stat_bar("Purity",   rock.purity,         (100, 220, 100))
        iy[0] += 4

        if rock.specials:
            dlabel("Specials:", (200, 180, 100))
            for sp in rock.specials:
                benefit, tradeoff = SPECIAL_DESCS.get(sp, ("", ""))
                dlabel(f"  {sp}", (220, 200, 80))
                dlabel(f"    + {benefit}", (80, 200, 80))
                dlabel(f"    - {tradeoff}", (200, 80, 80))
        else:
            dlabel("No specials.", (90, 90, 100))

        if rock.upgrades:
            iy[0] += 4
            dlabel("Upgrades:", (200, 200, 100))
            if "polished" in rock.upgrades:
                dlabel("  Polished  (Luster enhanced)", (80, 220, 220))
            if "fired" in rock.upgrades:
                dlabel("  Fired  (Purity enhanced)", (220, 160, 80))

    def _draw_codex(self, player):
        CELL, GAP, COLS = 82, 8, 6
        gx0 = (SCREEN_W - (COLS * CELL + (COLS - 1) * GAP)) // 2
        gy0 = 58

        detail_x = None
        if self._codex_selected_type is not None:
            detail_x = SCREEN_W - 340
            COLS = max(1, (detail_x - gx0 - 10) // (CELL + GAP))

        total_rows = (len(ROCK_TYPE_ORDER) + COLS - 1) // COLS
        visible_rows = (SCREEN_H - gy0 - 8 + GAP) // (CELL + GAP)
        self._max_codex_scroll = max(0, total_rows - visible_rows)
        self._codex_scroll = max(0, min(self._max_codex_scroll, self._codex_scroll))

        # Scrollbar
        if self._max_codex_scroll > 0:
            sb_x = gx0 + COLS * (CELL + GAP) - GAP + 8
            sb_h = SCREEN_H - gy0 - 8
            sb_th = max(20, sb_h * visible_rows // total_rows)
            sb_top = gy0 + (sb_h - sb_th) * self._codex_scroll // self._max_codex_scroll
            pygame.draw.rect(self.screen, (35, 35, 48), (sb_x, gy0, 7, sb_h))
            pygame.draw.rect(self.screen, (100, 100, 140), (sb_x, sb_top, 7, sb_th))

        self._codex_rects.clear()
        for idx, type_key in enumerate(ROCK_TYPE_ORDER):
            col = idx % COLS
            row = idx // COLS
            display_row = row - self._codex_scroll
            if display_row < 0:
                continue
            x = gx0 + col * (CELL + GAP)
            y = gy0 + display_row * (CELL + GAP)
            if y + CELL > SCREEN_H - 8:
                break
            rect = pygame.Rect(x, y, CELL, CELL)
            self._codex_rects[type_key] = rect

            discovered = type_key in player.discovered_types
            selected = (type_key == self._codex_selected_type)

            if discovered:
                img = render_codex_preview(type_key, 58)
                pygame.draw.rect(self.screen, (45, 42, 55) if selected else (28, 28, 38), rect)
                pygame.draw.rect(self.screen, (140, 160, 200) if selected else (70, 75, 95), rect,
                                 3 if selected else 2)
                self.screen.blit(img, (x + (CELL - 58) // 2, y + (CELL - 58) // 2 - 6))
                label = type_key.replace("_", " ")
            else:
                tdef = ROCK_TYPES[type_key]
                min_d = tdef["min_depth"]
                pygame.draw.rect(self.screen, (18, 18, 22) if selected else (14, 14, 18), rect)
                pygame.draw.rect(self.screen, (55, 55, 65) if selected else (35, 35, 42), rect,
                                 2 if selected else 1)
                qs = self.font.render("?", True, (55, 58, 68))
                self.screen.blit(qs, (x + CELL // 2 - qs.get_width() // 2,
                                      y + CELL // 2 - qs.get_height() // 2 - 6))
                label = f">{min_d}m"

            ls = self.small.render(label, True, (160, 165, 175) if discovered else (55, 58, 68))
            self.screen.blit(ls, (x + CELL // 2 - ls.get_width() // 2, y + CELL - 14))

        if detail_x is None:
            return

        type_key = self._codex_selected_type
        tdef = ROCK_TYPES[type_key]
        discovered = type_key in player.discovered_types

        dx, dy = detail_x, gy0
        dw, dh = SCREEN_W - dx - 8, SCREEN_H - gy0 - 10
        border_col = (100, 140, 200) if discovered else (55, 55, 70)
        pygame.draw.rect(self.screen, (20, 20, 30), (dx, dy, dw, dh))
        pygame.draw.rect(self.screen, border_col, (dx, dy, dw, dh), 2)

        iy = [dy + 8]

        def dlabel(text, color=(220, 220, 200)):
            s = self.small.render(text, True, color)
            self.screen.blit(s, (dx + 8, iy[0]))
            iy[0] += 15

        if discovered:
            img_big = render_codex_preview(type_key, 80)
            self.screen.blit(img_big, (dx + dw // 2 - 40, dy + 8))
            iy[0] = dy + 96
            dlabel(type_key.replace("_", " ").title(), (240, 210, 120))
            dlabel(f"Found from {tdef['min_depth']}m depth", (160, 180, 200))

            desc = ROCK_TYPE_DESCRIPTIONS.get(type_key, "")
            words = desc.split()
            line, lines = [], []
            for w in words:
                trial = " ".join(line + [w])
                if self.small.size(trial)[0] > dw - 18:
                    lines.append(" ".join(line))
                    line = [w]
                else:
                    line.append(w)
            if line:
                lines.append(" ".join(line))
            iy[0] += 4
            for ln in lines:
                dlabel(ln, (130, 135, 145))
            iy[0] += 6

            owned = [r for r in player.rocks if r.base_type == type_key]
            dlabel(f"In collection: {len(owned)}", (160, 210, 160))

            if owned:
                rarities = ["common", "uncommon", "rare", "epic", "legendary"]
                best = max(owned, key=lambda r: rarities.index(r.rarity))
                dlabel(f"Best rarity: {RARITY_LABEL[best.rarity]}",
                       RARITY_COLORS[best.rarity])
        else:
            iy[0] = dy + 30
            qs = self.font.render("???", True, (55, 60, 75))
            self.screen.blit(qs, (dx + dw // 2 - qs.get_width() // 2, dy + 8))
            dlabel("Not yet discovered.", (90, 95, 110))
            dlabel(f"Found below {tdef['min_depth']}m depth.", (120, 130, 150))

    # ------------------------------------------------------------------
    # Wildflower collection tabs
    # ------------------------------------------------------------------

    def _draw_my_flowers(self, player):
        if not player.wildflowers:
            msg = self.font.render("No wildflowers yet.  Pick them on the surface!", True, (80, 100, 80))
            self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2 - 10))
            return

        CELL, GAP, COLS = 82, 8, 8
        gx0 = (SCREEN_W - (COLS * CELL + (COLS - 1) * GAP)) // 2
        gy0 = 58

        detail_x = None
        if self._selected_flower_idx is not None and self._selected_flower_idx < len(player.wildflowers):
            detail_x = SCREEN_W - 340
            COLS = max(1, (detail_x - gx0 - 10) // (CELL + GAP))

        total_rows = (len(player.wildflowers) + COLS - 1) // COLS
        visible_rows = (SCREEN_H - gy0 - 8 + GAP) // (CELL + GAP)
        self._max_my_flowers_scroll = max(0, total_rows - visible_rows)
        self._my_flowers_scroll = max(0, min(self._max_my_flowers_scroll, self._my_flowers_scroll))

        self._flower_rects.clear()
        for idx, flower in enumerate(player.wildflowers):
            col = idx % COLS
            row = idx // COLS
            display_row = row - self._my_flowers_scroll
            if display_row < 0:
                continue
            x = gx0 + col * (CELL + GAP)
            y = gy0 + display_row * (CELL + GAP)
            if y + CELL > SCREEN_H - 8:
                break
            rect = pygame.Rect(x, y, CELL, CELL)
            self._flower_rects[idx] = rect

            selected = (idx == self._selected_flower_idx)
            rar_col = RARITY_COLORS[flower.rarity]
            pygame.draw.rect(self.screen, (35, 50, 35) if selected else (22, 35, 22), rect)
            pygame.draw.rect(self.screen, rar_col, rect, 3 if selected else 2)
            img = render_wildflower(flower, 58)
            self.screen.blit(img, (x + (CELL - 58) // 2, y + (CELL - 58) // 2 - 6))
            type_s = self.small.render(flower.flower_type.replace("_", " "), True, (140, 175, 140))
            self.screen.blit(type_s, (x + CELL // 2 - type_s.get_width() // 2, y + CELL - 14))

        if detail_x is None:
            return

        flower = player.wildflowers[self._selected_flower_idx]
        dx, dy = detail_x, gy0
        dw, dh = SCREEN_W - dx - 8, SCREEN_H - gy0 - 10
        pygame.draw.rect(self.screen, (15, 25, 15), (dx, dy, dw, dh))
        pygame.draw.rect(self.screen, RARITY_COLORS[flower.rarity], (dx, dy, dw, dh), 2)
        img_big = render_wildflower(flower, 80)
        self.screen.blit(img_big, (dx + dw // 2 - 40, dy + 8))

        iy = [dy + 96]

        def dlabel(text, color=(200, 230, 200)):
            s = self.small.render(text, True, color)
            self.screen.blit(s, (dx + 8, iy[0]))
            iy[0] += 15

        dlabel(flower.flower_type.replace("_", " ").title(), (200, 255, 160))
        dlabel(RARITY_LABEL[flower.rarity], RARITY_COLORS[flower.rarity])
        dlabel(f"Bloom: {flower.bloom_stage.title()}")
        dlabel(f"Pattern: {flower.petal_pattern.title()}  ({flower.petal_count} petals)")
        dlabel(f"Fragrance: {flower.fragrance:.2f}")
        dlabel(f"Vibrancy:  {flower.vibrancy:.2f}")
        dlabel(f"Biome: {flower.biodome_found.replace('_', ' ').title()}")
        if flower.specials:
            iy[0] += 4
            dlabel("Traits:", (180, 220, 180))
            for sp in flower.specials:
                dlabel(f"  {sp}", (150, 195, 155))

    def _draw_flower_codex(self, player):
        CELL, GAP, COLS = 82, 8, 6
        gx0 = (SCREEN_W - (COLS * CELL + (COLS - 1) * GAP)) // 2
        gy0 = 58

        detail_x = None
        if self._flower_codex_selected_type is not None:
            detail_x = SCREEN_W - 340
            COLS = max(1, (detail_x - gx0 - 10) // (CELL + GAP))

        total_rows = (len(WILDFLOWER_TYPE_ORDER) + COLS - 1) // COLS
        visible_rows = (SCREEN_H - gy0 - 8 + GAP) // (CELL + GAP)
        self._max_flower_codex_scroll = max(0, total_rows - visible_rows)
        self._flower_codex_scroll = max(0, min(self._max_flower_codex_scroll, self._flower_codex_scroll))

        if self._max_flower_codex_scroll > 0:
            sb_x = gx0 + COLS * (CELL + GAP) - GAP + 8
            sb_h = SCREEN_H - gy0 - 8
            sb_th = max(20, sb_h * visible_rows // total_rows)
            sb_top = gy0 + (sb_h - sb_th) * self._flower_codex_scroll // self._max_flower_codex_scroll
            pygame.draw.rect(self.screen, (20, 35, 20), (sb_x, gy0, 7, sb_h))
            pygame.draw.rect(self.screen, (80, 160, 90), (sb_x, sb_top, 7, sb_th))

        self._flower_codex_rects.clear()
        for idx, type_key in enumerate(WILDFLOWER_TYPE_ORDER):
            col = idx % COLS
            row = idx // COLS
            display_row = row - self._flower_codex_scroll
            if display_row < 0:
                continue
            x = gx0 + col * (CELL + GAP)
            y = gy0 + display_row * (CELL + GAP)
            if y + CELL > SCREEN_H - 8:
                break
            rect = pygame.Rect(x, y, CELL, CELL)
            self._flower_codex_rects[type_key] = rect

            discovered = type_key in player.discovered_flower_types
            selected = (type_key == self._flower_codex_selected_type)

            if discovered:
                img = get_flower_preview(type_key, 58)
                pygame.draw.rect(self.screen, (35, 50, 35) if selected else (20, 32, 20), rect)
                pygame.draw.rect(self.screen, (100, 190, 110) if selected else (55, 110, 65), rect,
                                 3 if selected else 2)
                self.screen.blit(img, (x + (CELL - 58) // 2, y + (CELL - 58) // 2 - 6))
                label = type_key.replace("_", " ")
            else:
                pygame.draw.rect(self.screen, (15, 22, 15) if selected else (12, 18, 12), rect)
                pygame.draw.rect(self.screen, (45, 70, 48) if selected else (28, 42, 30), rect,
                                 2 if selected else 1)
                qs = self.font.render("?", True, (40, 65, 42))
                self.screen.blit(qs, (x + CELL // 2 - qs.get_width() // 2,
                                      y + CELL // 2 - qs.get_height() // 2 - 6))
                label = "???"

            ls = self.small.render(label, True, (140, 185, 145) if discovered else (40, 65, 42))
            self.screen.blit(ls, (x + CELL // 2 - ls.get_width() // 2, y + CELL - 14))

        if detail_x is None:
            return

        type_key = self._flower_codex_selected_type
        tdef = WILDFLOWER_TYPES[type_key]
        discovered = type_key in player.discovered_flower_types

        dx, dy = detail_x, gy0
        dw, dh = SCREEN_W - dx - 8, SCREEN_H - gy0 - 10
        border_col = (90, 175, 100) if discovered else (40, 65, 42)
        pygame.draw.rect(self.screen, (14, 22, 14), (dx, dy, dw, dh))
        pygame.draw.rect(self.screen, border_col, (dx, dy, dw, dh), 2)

        iy = [dy + 8]

        def dlabel(text, color=(200, 230, 200)):
            s = self.small.render(text, True, color)
            self.screen.blit(s, (dx + 8, iy[0]))
            iy[0] += 15

        if discovered:
            img_big = get_flower_preview(type_key, 80)
            self.screen.blit(img_big, (dx + dw // 2 - 40, dy + 8))
            iy[0] = dy + 96
            dlabel(type_key.replace("_", " ").title(), (200, 255, 160))
            biodomes = [b for b, types in WILDFLOWER_BIODOME_AFFINITY.items() if type_key in types]
            dlabel("Biome: " + ", ".join(b.replace("_", " ").title() for b in biodomes),
                   (160, 205, 165))
            pool = tdef["rarity_pool"]
            counts = {r: pool.count(r) for r in dict.fromkeys(pool)}
            dlabel("Rarity: " + "  ".join(f"{r[0].upper()}×{c}" for r, c in counts.items()),
                   (180, 195, 180))
            owned = [f for f in player.wildflowers if f.flower_type == type_key]
            dlabel(f"In collection: {len(owned)}", (160, 210, 160))
            if owned:
                rarities = ["common", "uncommon", "rare", "epic", "legendary"]
                best = max(owned, key=lambda f: rarities.index(f.rarity))
                dlabel(f"Best rarity: {RARITY_LABEL[best.rarity]}", RARITY_COLORS[best.rarity])
        else:
            iy[0] = dy + 30
            qs = self.font.render("???", True, (42, 68, 44))
            self.screen.blit(qs, (dx + dw // 2 - qs.get_width() // 2, dy + 8))
            dlabel("Not yet discovered.", (75, 105, 78))
            dlabel("Find it on the surface.", (95, 130, 98))

    def _draw_mushroom_codex(self, player):
        CELL, GAP, COLS = 82, 8, 5
        gx0 = (SCREEN_W - (COLS * CELL + (COLS - 1) * GAP)) // 2
        gy0 = 58

        detail_x = None
        if self._mushroom_codex_selected_bid is not None:
            detail_x = SCREEN_W - 340
            COLS = max(1, (detail_x - gx0 - 10) // (CELL + GAP))

        total_rows   = (len(_MUSHROOM_ORDER) + COLS - 1) // COLS
        visible_rows = (SCREEN_H - gy0 - 8 + GAP) // (CELL + GAP)
        self._max_mushroom_codex_scroll = max(0, total_rows - visible_rows)
        self._mushroom_codex_scroll = max(0, min(self._max_mushroom_codex_scroll, self._mushroom_codex_scroll))

        if self._max_mushroom_codex_scroll > 0:
            sb_x  = gx0 + COLS * (CELL + GAP) - GAP + 8
            sb_h  = SCREEN_H - gy0 - 8
            sb_th = max(20, sb_h * visible_rows // total_rows)
            sb_top = gy0 + (sb_h - sb_th) * self._mushroom_codex_scroll // self._max_mushroom_codex_scroll
            pygame.draw.rect(self.screen, (22, 20, 10), (sb_x, gy0, 7, sb_h))
            pygame.draw.rect(self.screen, (140, 128, 55), (sb_x, sb_top, 7, sb_th))

        self._mushroom_codex_rects.clear()
        for idx, bid in enumerate(_MUSHROOM_ORDER):
            col = idx % COLS
            row = idx // COLS
            display_row = row - self._mushroom_codex_scroll
            if display_row < 0:
                continue
            x = gx0 + col * (CELL + GAP)
            y = gy0 + display_row * (CELL + GAP)
            if y + CELL > SCREEN_H - 8:
                break
            rect = pygame.Rect(x, y, CELL, CELL)
            self._mushroom_codex_rects[bid] = rect

            discovered = bid in player.discovered_mushroom_types
            selected   = (bid == self._mushroom_codex_selected_bid)

            if discovered:
                img = render_mushroom_preview(bid, 58)
                pygame.draw.rect(self.screen, (45, 40, 22) if selected else (28, 25, 14), rect)
                pygame.draw.rect(self.screen, (185, 168, 72) if selected else (100, 90, 40), rect,
                                 3 if selected else 2)
                self.screen.blit(img, (x + (CELL - 58) // 2, y + (CELL - 58) // 2 - 6))
                label = BLOCKS[bid]["name"]
            else:
                pygame.draw.rect(self.screen, (20, 18, 10) if selected else (14, 12, 8), rect)
                pygame.draw.rect(self.screen, (60, 54, 24) if selected else (35, 30, 14), rect,
                                 2 if selected else 1)
                qs = self.font.render("?", True, (52, 46, 20))
                self.screen.blit(qs, (x + CELL // 2 - qs.get_width() // 2,
                                      y + CELL // 2 - qs.get_height() // 2 - 6))
                label = "???"

            ls = self.small.render(label, True, (200, 180, 100) if discovered else (52, 46, 20))
            self.screen.blit(ls, (x + CELL // 2 - ls.get_width() // 2, y + CELL - 14))

        if detail_x is None:
            return

        bid        = self._mushroom_codex_selected_bid
        discovered = bid in player.discovered_mushroom_types
        dx, dy2    = detail_x, gy0
        dw         = SCREEN_W - dx - 8
        dh         = SCREEN_H - gy0 - 10
        border_col = (165, 148, 60) if discovered else (50, 44, 20)
        pygame.draw.rect(self.screen, (16, 14, 8), (dx, dy2, dw, dh))
        pygame.draw.rect(self.screen, border_col, (dx, dy2, dw, dh), 2)

        iy = [dy2 + 8]
        def dlabel(text, color=(210, 195, 140)):
            s = self.small.render(text, True, color)
            self.screen.blit(s, (dx + 8, iy[0]))
            iy[0] += 15

        if discovered:
            img_big = render_mushroom_preview(bid, 80)
            self.screen.blit(img_big, (dx + dw // 2 - 40, dy2 + 8))
            iy[0] = dy2 + 96
            dlabel(BLOCKS[bid]["name"], (235, 220, 130))
            drop      = BLOCKS[bid].get("drop", "")
            drop_col  = _MUSHROOM_DROP_COLOR.get(drop, (180, 160, 120))
            drop_name = drop.replace("_", " ").title()
            dlabel(f"Drop: {drop_name}", drop_col)
            dlabel(f"Biome: {_MUSHROOM_BIOME.get(bid, 'Any')}", (170, 195, 150))
            dlabel(f"Shape: {_MUSHROOM_SHAPES.get(bid, '').title()}", (155, 162, 178))
            count = player.mushrooms_found.get(bid, 0)
            dlabel(f"Collected: {count}", (160, 205, 160))
        else:
            iy[0] = dy2 + 30
            qs = self.font.render("???", True, (52, 46, 20))
            self.screen.blit(qs, (dx + dw // 2 - qs.get_width() // 2, dy2 + 8))
            dlabel("Not yet discovered.", (80, 72, 34))
            dlabel("Find it underground in caves.", (100, 90, 44))

    # ------------------------------------------------------------------
    # Refinery overlay (E key near equipment block)
    # ------------------------------------------------------------------

    def _draw_bakery(self, player):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("BAKERY", True, (220, 160, 80))
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close  |  Select a recipe and click BAKE",
                                 True, (120, 120, 130))
        self.screen.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, 26))

        # --- Left panel: recipe list ---
        LIST_X, LIST_Y = 30, 55
        LIST_W, ROW_H, GAP = 260, 58, 4
        ICON_SZ = 28
        LIST_BOTTOM = SCREEN_H - 10
        visible_count = (LIST_BOTTOM - LIST_Y) // (ROW_H + GAP)
        self._max_bakery_scroll = max(0, len(BAKERY_RECIPES) - visible_count)
        self._bakery_scroll = max(0, min(self._max_bakery_scroll, self._bakery_scroll))

        # Scrollbar
        if self._max_bakery_scroll > 0:
            sb_x = LIST_X + LIST_W + 4
            sb_h = LIST_BOTTOM - LIST_Y
            sb_th = max(20, sb_h * visible_count // len(BAKERY_RECIPES))
            sb_top = LIST_Y + (sb_h - sb_th) * self._bakery_scroll // self._max_bakery_scroll
            pygame.draw.rect(self.screen, (35, 25, 10), (sb_x, LIST_Y, 7, sb_h))
            pygame.draw.rect(self.screen, (160, 110, 50), (sb_x, sb_top, 7, sb_th))

        self._bakery_recipe_rects.clear()
        for i, recipe in enumerate(BAKERY_RECIPES):
            display_idx = i - self._bakery_scroll
            if display_idx < 0:
                continue
            ry = LIST_Y + display_idx * (ROW_H + GAP)
            if ry + ROW_H > LIST_BOTTOM:
                break
            can_bake_r = all(
                player.inventory.get(iid, 0) >= cnt
                for iid, cnt in recipe["ingredients"].items()
            )
            selected = (i == self._bakery_selected_recipe)
            if selected:
                bg     = (130, 85, 30) if can_bake_r else (75, 50, 50)
                border = (220, 160, 80)
            else:
                bg     = (50, 32, 10) if can_bake_r else (24, 24, 32)
                border = (180, 120, 50) if can_bake_r else (52, 52, 68)
            row_rect = pygame.Rect(LIST_X, ry, LIST_W, ROW_H)
            pygame.draw.rect(self.screen, bg, row_rect)
            pygame.draw.rect(self.screen, border, row_rect, 1)
            out_id   = recipe["output_id"]
            out_data = ITEMS.get(out_id, {})
            icon = render_item_icon(out_id, out_data.get("color", (80, 80, 80)), ICON_SZ)
            self.screen.blit(icon, (LIST_X + 4, ry + (ROW_H - ICON_SZ) // 2))
            name_col = out_data.get("color", (200, 200, 200)) if can_bake_r else (110, 110, 120)
            hunger   = out_data.get("hunger_restore", 0)
            label    = self.font.render(f"{recipe['name']}  +{hunger}%", True, name_col)
            self.screen.blit(label, (LIST_X + 4 + ICON_SZ + 6, ry + 5))
            iy = ry + 5 + 15
            for item_id, count in recipe["ingredients"].items():
                have = player.inventory.get(item_id, 0)
                item_name = ITEMS.get(item_id, {}).get("name", item_id)
                col = (120, 210, 100) if have >= count else (210, 80, 60)
                txt = self.small.render(f"{item_name}: {have}/{count}", True, col)
                self.screen.blit(txt, (LIST_X + 4 + ICON_SZ + 6, iy))
                iy += 12
            self._bakery_recipe_rects[i] = row_rect

        # --- Right panel: selected recipe detail ---
        recipe  = BAKERY_RECIPES[self._bakery_selected_recipe]
        DX = LIST_X + LIST_W + 30
        DY = LIST_Y
        detail_title = self.font.render(recipe["name"], True, (220, 180, 100))
        self.screen.blit(detail_title, (DX, DY))

        iy = DY + 30
        for item_id, count in recipe["ingredients"].items():
            have   = player.inventory.get(item_id, 0)
            needed = count
            item_name = ITEMS.get(item_id, {}).get("name", item_id)
            col = (180, 220, 100) if have >= needed else (220, 80, 60)
            txt = self.small.render(f"{item_name}: {have}/{needed}", True, col)
            self.screen.blit(txt, (DX, iy))
            iy += 20

        arrow = self.font.render("→", True, (180, 140, 60))
        self.screen.blit(arrow, (DX, iy + 4))
        out_data = ITEMS.get(recipe["output_id"], {})
        out_col  = out_data.get("color", (200, 200, 200))
        out_name = out_data.get("name", recipe["output_id"])
        out_lbl  = self.font.render(out_name, True, out_col)
        self.screen.blit(out_lbl, (DX + 24, iy + 4))

        # BAKE button
        can_bake = all(
            player.inventory.get(iid, 0) >= cnt
            for iid, cnt in recipe["ingredients"].items()
        )
        btn_col  = (160, 100, 40) if can_bake else (60, 50, 40)
        btn_rect = pygame.Rect(DX, iy + 40, 120, 34)
        pygame.draw.rect(self.screen, btn_col, btn_rect)
        pygame.draw.rect(self.screen, (220, 160, 80) if can_bake else (80, 70, 60), btn_rect, 2)
        btn_txt = self.font.render("BAKE", True,
                                   (255, 220, 120) if can_bake else (100, 90, 70))
        self.screen.blit(btn_txt, (btn_rect.centerx - btn_txt.get_width() // 2,
                                   btn_rect.centery - btn_txt.get_height() // 2))
        self._refine_btn = btn_rect

    def _draw_cooking_station(self, player, recipe_list, title_str, title_color,
                               selected_idx, recipe_rects_dict, selected_attr, block_id=None):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render(title_str, True, title_color)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close  |  Select a recipe and click COOK",
                                 True, (120, 120, 130))
        self.screen.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, 26))

        # --- Left panel: recipe list ---
        LIST_X, LIST_Y = 30, 55
        LIST_W, ROW_H, GAP = 270, 58, 4
        ICON_SZ = 28
        LIST_BOTTOM = SCREEN_H - 10
        visible_count = (LIST_BOTTOM - LIST_Y) // (ROW_H + GAP)
        max_scroll = max(0, len(recipe_list) - visible_count)
        scroll = self._cook_station_scroll.get(block_id, 0)
        scroll = max(0, min(max_scroll, scroll))
        if block_id is not None:
            self._cook_station_scroll[block_id] = scroll
            self._cook_station_max_scroll[block_id] = max_scroll

        if max_scroll > 0:
            sb_x = LIST_X + LIST_W + 4
            sb_h = LIST_BOTTOM - LIST_Y
            sb_th = max(20, sb_h * visible_count // len(recipe_list))
            sb_top = LIST_Y + (sb_h - sb_th) * scroll // max_scroll
            pygame.draw.rect(self.screen, (20, 35, 25), (sb_x, LIST_Y, 7, sb_h))
            pygame.draw.rect(self.screen, title_color, (sb_x, sb_top, 7, sb_th))

        recipe_rects_dict.clear()
        for i, recipe in enumerate(recipe_list):
            display_idx = i - scroll
            if display_idx < 0:
                continue
            ry = LIST_Y + display_idx * (ROW_H + GAP)
            if ry + ROW_H > LIST_BOTTOM:
                break
            can_cook_r = all(
                player.inventory.get(iid, 0) >= cnt
                for iid, cnt in recipe["ingredients"].items()
            )
            selected = (i == selected_idx)
            if selected:
                bg     = (60, 110, 80) if can_cook_r else (75, 45, 45)
                border = title_color
            else:
                bg     = (18, 48, 30) if can_cook_r else (24, 24, 32)
                border = (45, 140, 75) if can_cook_r else (52, 52, 68)
            row_rect = pygame.Rect(LIST_X, ry, LIST_W, ROW_H)
            pygame.draw.rect(self.screen, bg, row_rect)
            pygame.draw.rect(self.screen, border, row_rect, 1)
            out_id   = recipe["output_id"]
            out_data = ITEMS.get(out_id, {})
            icon = render_item_icon(out_id, out_data.get("color", (80, 80, 80)), ICON_SZ)
            self.screen.blit(icon, (LIST_X + 4, ry + (ROW_H - ICON_SZ) // 2))
            name_col  = out_data.get("color", (200, 200, 200)) if can_cook_r else (110, 110, 120)
            hunger    = out_data.get("hunger_restore", 0)
            label_str = f"{recipe['name']}  +{hunger}%" if hunger else recipe["name"]
            label = self.font.render(label_str, True, name_col)
            self.screen.blit(label, (LIST_X + 4 + ICON_SZ + 6, ry + 5))
            iy = ry + 5 + 15
            for item_id, count in recipe["ingredients"].items():
                have = player.inventory.get(item_id, 0)
                item_name = ITEMS.get(item_id, {}).get("name", item_id)
                col = (100, 200, 120) if have >= count else (200, 80, 60)
                txt = self.small.render(f"{item_name}: {have}/{count}", True, col)
                self.screen.blit(txt, (LIST_X + 4 + ICON_SZ + 6, iy))
                iy += 12
            recipe_rects_dict[i] = row_rect

        # --- Right panel: selected recipe detail ---
        recipe  = recipe_list[selected_idx]
        DX = LIST_X + LIST_W + 30
        DY = LIST_Y
        detail_title = self.font.render(recipe["name"], True, (220, 210, 170))
        self.screen.blit(detail_title, (DX, DY))

        iy = DY + 30
        for item_id, count in recipe["ingredients"].items():
            have      = player.inventory.get(item_id, 0)
            item_name = ITEMS.get(item_id, {}).get("name", item_id)
            col = (180, 220, 100) if have >= count else (220, 80, 60)
            txt = self.small.render(f"{item_name}: {have}/{count}", True, col)
            self.screen.blit(txt, (DX, iy))
            iy += 20

        arrow = self.font.render("→", True, (160, 160, 80))
        self.screen.blit(arrow, (DX, iy + 4))
        out_data = ITEMS.get(recipe["output_id"], {})
        out_col  = out_data.get("color", (200, 200, 200))
        out_name = out_data.get("name", recipe["output_id"])
        out_lbl  = self.font.render(out_name, True, out_col)
        self.screen.blit(out_lbl, (DX + 24, iy + 4))

        can_cook = all(
            player.inventory.get(iid, 0) >= cnt
            for iid, cnt in recipe["ingredients"].items()
        )
        btn_col  = (40, 100, 60) if can_cook else (40, 50, 40)
        btn_rect = pygame.Rect(DX, iy + 40, 120, 34)
        pygame.draw.rect(self.screen, btn_col, btn_rect)
        pygame.draw.rect(self.screen, title_color if can_cook else (60, 70, 60), btn_rect, 2)
        btn_txt = self.font.render("COOK", True,
                                   (200, 255, 180) if can_cook else (80, 100, 80))
        self.screen.blit(btn_txt, (btn_rect.centerx - btn_txt.get_width() // 2,
                                   btn_rect.centery - btn_txt.get_height() // 2))
        self._refine_btn = btn_rect

    def _draw_refinery(self, player):
        if self.refinery_block_id == BAKERY_BLOCK:
            self._draw_bakery(player)
            return
        if self.refinery_block_id == WOK_BLOCK:
            self._draw_cooking_station(player, WOK_RECIPES, "WOK",
                                       (220, 100, 40), self._wok_selected_recipe,
                                       self._wok_recipe_rects, "_wok_selected_recipe",
                                       block_id=WOK_BLOCK)
            return
        if self.refinery_block_id == STEAMER_BLOCK:
            self._draw_cooking_station(player, STEAMER_RECIPES, "STEAMER",
                                       (160, 200, 180), self._steamer_selected_recipe,
                                       self._steamer_recipe_rects, "_steamer_selected_recipe",
                                       block_id=STEAMER_BLOCK)
            return
        if self.refinery_block_id == NOODLE_POT_BLOCK:
            self._draw_cooking_station(player, NOODLE_POT_RECIPES, "NOODLE POT",
                                       (180, 140, 80), self._noodle_pot_selected_recipe,
                                       self._noodle_pot_recipe_rects, "_noodle_pot_selected_recipe",
                                       block_id=NOODLE_POT_BLOCK)
            return
        if self.refinery_block_id == BBQ_GRILL_BLOCK:
            self._draw_cooking_station(player, BBQ_GRILL_RECIPES, "BBQ GRILL",
                                       (210, 90, 30), self._bbq_grill_selected_recipe,
                                       self._bbq_grill_recipe_rects, "_bbq_grill_selected_recipe",
                                       block_id=BBQ_GRILL_BLOCK)
            return
        if self.refinery_block_id == CLAY_POT_BLOCK:
            self._draw_cooking_station(player, CLAY_POT_RECIPES, "CLAY POT",
                                       (175, 110, 65), self._clay_pot_selected_recipe,
                                       self._clay_pot_recipe_rects, "_clay_pot_selected_recipe",
                                       block_id=CLAY_POT_BLOCK)
            return
        equip_data = get_refinery_equipment().get(self.refinery_block_id)
        if equip_data is None:
            return

        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render(f"REFINERY -- {equip_data['name']}", True, (220, 180, 80))
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close  |  Select a rock then click REFINE",
                                 True, (120, 120, 130))
        self.screen.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, 26))
        desc = self.small.render(equip_data["description"], True, (160, 160, 160))
        self.screen.blit(desc, (SCREEN_W // 2 - desc.get_width() // 2, 42))

        list_x, list_y, list_w = 20, 60, SCREEN_W - 380
        CELL_H, GAP = 64, 6
        self._refine_rects.clear()

        if not player.rocks:
            msg = self.font.render("No rocks in collection.  Mine Rock Deposits!", True, (80, 80, 90))
            self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2))
        else:
            for row, (idx, rock) in enumerate(enumerate(player.rocks)):
                ry = list_y + row * (CELL_H + GAP)
                if ry + CELL_H > SCREEN_H - 60:
                    break
                rect = pygame.Rect(list_x, ry, list_w, CELL_H)
                self._refine_rects[idx] = rect
                selected = (idx == self._refinery_selected_idx)
                usable = equip_data["can_use"](rock)
                rar_col = RARITY_COLORS[rock.rarity]

                if selected:
                    bg, border = (40, 40, 60), rar_col
                elif usable:
                    bg, border = (25, 25, 35), (80, 80, 100)
                else:
                    bg, border = (18, 18, 22), (45, 45, 55)

                pygame.draw.rect(self.screen, bg, rect)
                pygame.draw.rect(self.screen, border, rect, 2)
                img = render_rock(rock, 48)
                self.screen.blit(img, (list_x + 6, ry + (CELL_H - 48) // 2))

                ix, iy = list_x + 62, ry + 8
                self.screen.blit(
                    self.small.render(rock.base_type.replace("_", " ").title(),
                                      True, (220, 200, 150)), (ix, iy))
                iy += 15
                self.screen.blit(
                    self.small.render(
                        f"{RARITY_LABEL[rock.rarity]} {rock.size}  |  "
                        f"Luster:{rock.luster:.2f}  Purity:{rock.purity:.2f}",
                        True, rar_col if usable else (80, 80, 80)), (ix, iy))
                iy += 14
                sp_text = ", ".join(rock.specials) if rock.specials else "no specials"
                self.screen.blit(
                    self.small.render(sp_text, True,
                                      (160, 140, 80) if usable else (60, 60, 60)), (ix, iy))
                iy += 14
                if rock.upgrades:
                    badge = "  ".join("Polished" if u == "polished" else "Fired" for u in rock.upgrades)
                    self.screen.blit(
                        self.small.render(badge, True, (80, 200, 200) if usable else (40, 100, 100)),
                        (ix, iy))

                if not usable:
                    bs = self.small.render("BLOCKED", True, (180, 60, 60))
                    self.screen.blit(bs, (rect.right - bs.get_width() - 8,
                                          ry + CELL_H // 2 - bs.get_height() // 2))

        rx, ry0, rw = SCREEN_W - 360, 60, 340
        pygame.draw.rect(self.screen, (22, 22, 32), (rx, ry0, rw, SCREEN_H - ry0 - 8))
        pygame.draw.rect(self.screen, (70, 70, 90), (rx, ry0, rw, SCREEN_H - ry0 - 8), 1)

        sel_idx = self._refinery_selected_idx
        sel_rock = (player.rocks[sel_idx]
                    if sel_idx is not None and sel_idx < len(player.rocks) else None)

        py = ry0 + 10
        is_upgrade = "upgrade_preview" in equip_data
        header = "Upgrade Effect" if is_upgrade else "Expected Output"
        self.screen.blit(self.font.render(header, True, (200, 200, 160)), (rx + 10, py))
        py += 28

        if sel_rock is not None:
            if equip_data["can_use"](sel_rock):
                if is_upgrade:
                    line = equip_data["upgrade_preview"](sel_rock)
                    self.screen.blit(self.small.render(line, True, (140, 220, 180)), (rx + 10, py))
                    py += 18
                    note = self.small.render("Rock stays in your collection.", True, (100, 160, 100))
                    self.screen.blit(note, (rx + 10, py))
                else:
                    for item_id, count in equip_data["refine"](sel_rock):
                        iname = ITEMS.get(item_id, {}).get("name", item_id)
                        icolor = ITEMS.get(item_id, {}).get("color", (128, 128, 128))
                        pygame.draw.rect(self.screen, icolor, (rx + 10, py + 2, 12, 12))
                        s = self.small.render(f"   {iname} x{count}", True, (200, 220, 180))
                        self.screen.blit(s, (rx + 10, py))
                        py += 18
            else:
                bs = self.small.render("Equipment cannot process this rock.", True, (180, 60, 60))
                self.screen.blit(bs, (rx + 10, py))
        else:
            tip = self.small.render("Select a rock from the list.", True, (100, 100, 110))
            self.screen.blit(tip, (rx + 10, py))

        BW, BH = 180, 44
        bx2 = rx + (rw - BW) // 2
        by = SCREEN_H - BH - 20
        can_refine = (sel_rock is not None and equip_data["can_use"](sel_rock))
        if can_refine:
            bbg, bbdr, btxt = (18, 90, 18), (45, 200, 45), (190, 255, 190)
        else:
            bbg, bbdr, btxt = (28, 28, 36), (55, 55, 68), (70, 70, 82)
        self._refine_btn = pygame.Rect(bx2, by, BW, BH)
        pygame.draw.rect(self.screen, bbg, self._refine_btn)
        pygame.draw.rect(self.screen, bbdr, self._refine_btn, 2)
        rl = self.font.render("REFINE", True, btxt)
        self.screen.blit(rl, (bx2 + BW // 2 - rl.get_width() // 2,
                               by + BH // 2 - rl.get_height() // 2))

    # ------------------------------------------------------------------
    # Automation interaction panel
    # ------------------------------------------------------------------

    _STATUS_COLOR = {
        "active":           (80, 220, 80),
        "halted_fuel":      (220, 140, 40),
        "halted_full":      (220, 220, 40),
        "halted_blocked":   (220, 60, 60),
        "halted_supports":  (80, 160, 220),
    }
    _STATUS_LABEL = {
        "active":           "Active",
        "halted_fuel":      "Out of Fuel",
        "halted_full":      "Storage Full",
        "halted_blocked":   "Blocked",
        "halted_supports":  "No Supports",
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
        PW, PH = 480, 430
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

        # --- Supports section ---
        sup_item_name = ITEMS.get(adef["support_item"], {}).get("name", adef["support_item"])
        next_support_in = adef["support_interval"] - auto._blocks_since_support
        sup_detail = self.small.render(
            f"Next support in {next_support_in} block(s)", True, (120, 130, 160)
        )
        self._draw_resource_row(
            "SUPPORTS", auto.supports, adef["supports_max"], sup_item_name,
            (80, 160, 220),
            "_auto_support1_btn", "_auto_support_all_btn",
            player.inventory.get(adef["support_item"], 0) > 0,
            py + 130, px, bar_w, py + 162,
        )
        self.screen.blit(sup_detail, (px + PW - sup_detail.get_width() - 14, py + 130))

        pygame.draw.line(self.screen, (70, 60, 90), (px + 10, py + 196), (px + PW - 10, py + 196))

        # --- Stored items section ---
        inv_count = auto.inv_count
        inv_label = self.small.render("STORED ITEMS", True, (200, 190, 230))
        self.screen.blit(inv_label, (px + 14, py + 202))
        count_label = self.small.render(f"{inv_count} / {adef['inv_limit']}", True, (160, 150, 200))
        self.screen.blit(count_label, (px + PW - count_label.get_width() - 14, py + 202))

        SW, SH, GAP = 44, 44, 6
        items_per_row = (PW - 28 + GAP) // (SW + GAP)
        ix0, iy0 = px + 14, py + 220
        for idx, (item_id, count) in enumerate(sorted(auto.stored.items())):
            col_i = idx % items_per_row
            row_i = idx // items_per_row
            sx_ = ix0 + col_i * (SW + GAP)
            sy_ = iy0 + row_i * (SH + GAP)
            if sy_ + SH > py + PH - 50:
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

        # Take All button
        TW, TH = 140, 28
        tx = px + PW - TW - 14
        ty = py + PH - TH - 10
        has_items = inv_count > 0
        t_col    = (30, 80, 30)   if has_items else (30, 30, 40)
        t_border = (60, 180, 60)  if has_items else (55, 55, 68)
        t_txt_col = (160, 255, 160) if has_items else (70, 70, 82)
        self._auto_take_btn = pygame.Rect(tx, ty, TW, TH)
        pygame.draw.rect(self.screen, t_col, self._auto_take_btn)
        pygame.draw.rect(self.screen, t_border, self._auto_take_btn, 1)
        take_t = self.small.render("TAKE ALL ITEMS", True, t_txt_col)
        self.screen.blit(take_t, (tx + TW // 2 - take_t.get_width() // 2,
                                   ty + TH // 2 - take_t.get_height() // 2))

        # Direction indicator
        dir_sym = "\u2192" if auto.direction == 1 else "\u2190"
        dir_t = self.small.render(f"Direction: {dir_sym}", True, (150, 140, 180))
        self.screen.blit(dir_t, (px + 14, py + PH - 20))

    def handle_automation_click(self, pos, player):
        auto = self.active_automation
        if auto is None:
            return
        if self._auto_deposit1_btn and self._auto_deposit1_btn.collidepoint(pos):
            auto.deposit_fuel(player, 1)
        elif self._auto_deposit_all_btn and self._auto_deposit_all_btn.collidepoint(pos):
            auto.deposit_fuel(player)
        elif self._auto_support1_btn and self._auto_support1_btn.collidepoint(pos):
            auto.deposit_supports(player, 1)
        elif self._auto_support_all_btn and self._auto_support_all_btn.collidepoint(pos):
            auto.deposit_supports(player)
        elif self._auto_take_btn and self._auto_take_btn.collidepoint(pos):
            auto.take_all(player)

    # ------------------------------------------------------------------
    # Death screen
    # ------------------------------------------------------------------

    def _draw_pause_menu(self):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        PW, PH = 360, 320
        px = (SCREEN_W - PW) // 2
        py = (SCREEN_H - PH) // 2
        pygame.draw.rect(self.screen, (12, 20, 60), (px, py, PW, PH), border_radius=12)
        pygame.draw.rect(self.screen, (55, 130, 255), (px, py, PW, PH), 2, border_radius=12)

        title = self._pause_font.render("PAUSED", True, (255, 255, 255))
        self.screen.blit(title, title.get_rect(center=(SCREEN_W // 2, py + 60)))

        BTN_W, BTN_H = 260, 52
        bx = SCREEN_W // 2 - BTN_W // 2
        btn_labels = [("resume", "RESUME"), ("save", "SAVE"), ("quit", "SAVE & QUIT")]
        btn_y_start = py + 120
        btn_gap = 66
        mx, my = pygame.mouse.get_pos()
        self._pause_btn_rects = {}
        for i, (key, label) in enumerate(btn_labels):
            rect = pygame.Rect(bx, btn_y_start + i * btn_gap, BTN_W, BTN_H)
            self._pause_btn_rects[key] = rect
            hovered = rect.collidepoint(mx, my)
            color = (40, 100, 240) if hovered else (20, 60, 160)
            pygame.draw.rect(self.screen, color, rect, border_radius=8)
            pygame.draw.rect(self.screen, (55, 130, 255), rect, 2, border_radius=8)
            lbl = self._pause_font2.render(label, True, (255, 255, 255))
            self.screen.blit(lbl, lbl.get_rect(center=rect.center))

    def handle_pause_click(self, pos):
        for key, rect in self._pause_btn_rects.items():
            if rect.collidepoint(pos):
                return key
        return None

    def _draw_death_screen(self, player):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))

        txt = self._death_font.render("YOU DIED", True, (220, 40, 40))
        self.screen.blit(txt, txt.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 - 70)))

        sub = self._death_font2.render("All items were dropped at your location.", True, (200, 180, 180))
        self.screen.blit(sub, sub.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2)))

        spawn_label = "Respawn at: Bed" if player.spawn_x is not None else "Respawn at: World Spawn"
        spawn_txt = self._death_font2.render(spawn_label, True, (150, 210, 150))
        self.screen.blit(spawn_txt, spawn_txt.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + 40)))

        key_txt = self._death_font2.render("Press SPACE or ENTER to respawn", True, (180, 180, 220))
        self.screen.blit(key_txt, key_txt.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + 90)))

    # ------------------------------------------------------------------
    # Cheat console
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # Chest overlay (E near chest block)
    # ------------------------------------------------------------------

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

    def _draw_cheat_console(self):
        W = SCREEN_W
        pygame.draw.rect(self.screen, (15, 14, 25), (0, 0, W, 40))
        pygame.draw.rect(self.screen, (60, 200, 80), (0, 0, W, 40), 1)

        cursor = "_" if int(pygame.time.get_ticks() / 500) % 2 == 0 else ""
        prompt = self._cheat_font.render("> " + self.cheat_text + cursor, True, (80, 255, 100))
        self.screen.blit(prompt, (10, 10))

        if self.cheat_message and self._cheat_msg_timer > 0:
            msg_col = (255, 80, 80) if self.cheat_message.startswith("!") else (200, 230, 100)
            msg = self._cheat_font.render(self.cheat_message.lstrip("!"), True, msg_col)
            self.screen.blit(msg, (W - msg.get_width() - 10, 10))
