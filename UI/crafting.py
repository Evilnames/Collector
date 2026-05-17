import pygame
from items import ITEMS
from item_icons import render_item_icon
from crafting import (RECIPES, BAKERY_RECIPES, WOK_RECIPES, STEAMER_RECIPES, NOODLE_POT_RECIPES,
                      BBQ_GRILL_RECIPES, CLAY_POT_RECIPES, FORGE_RECIPES, ARTISAN_RECIPES,
                      BAIT_STATION_RECIPES, FLETCHING_RECIPES, SMELTER_RECIPES, GLASS_KILN_RECIPES,
                      GARDEN_WORKSHOP_RECIPES, JUICER_RECIPES, AUTOMATION_RECIPES,
                      TANNING_RACK_RECIPES,
                      ARTISAN_TABS, ARTISAN_RECIPE_TAB,
                      RECIPE_GROUPS, RECIPE_GROUPS_ORDER,
                      match_recipe, craft_costs, can_craft,
                      RESEARCH_LOCKED_RECIPES, is_research_locked, can_craft_with_research)
from rocks import get_refinery_equipment, RARITY_COLORS
from constants import SCREEN_W, SCREEN_H
from ._data import RARITY_LABEL


class CraftingMixin:

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
        res_locked = is_research_locked(out_id, research) if out_id else False
        craftable = can_craft_with_research(self._craft_grid, player.inventory, research)

        if out_id and out_id in ITEMS:
            out_item = ITEMS[out_id]
            if res_locked:
                bg_col, br_col = (45, 20, 20), (160, 60, 60)
            elif craftable:
                bg_col, br_col = (20, 50, 20), (55, 200, 55)
            else:
                bg_col, br_col = (42, 28, 28), (140, 75, 75)
            pygame.draw.rect(self.screen, bg_col, (ox, oy, OUT, OUT))
            pygame.draw.rect(self.screen, br_col, (ox, oy, OUT, OUT), 2)
            sw = OUT - 14
            icon = render_item_icon(out_id, out_item["color"], sw)
            self.screen.blit(icon, (ox + 5, oy + 5))
            cnt_s = self.small.render(f"x{out_count}", True, (200, 200, 200))
            self.screen.blit(cnt_s, (ox + OUT - cnt_s.get_width() - 4, oy + OUT - 14))
            if res_locked:
                lock_s = self.small.render("LOCKED", True, (210, 80, 80))
                self.screen.blit(lock_s, (ox + OUT // 2 - lock_s.get_width() // 2, oy + 2))
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
            if res_locked:
                req_node_id = RESEARCH_LOCKED_RECIPES.get(out_id, "")
                req_node = research.nodes.get(req_node_id) if research else None
                req_name = req_node.name if req_node else req_node_id
                ls = self.small.render(f"Needs research: {req_name}", True, (210, 100, 100))
                self.screen.blit(ls, (info_x, info_y))
                info_y += 18
            self.screen.blit(self.small.render("Materials:", True, (150, 150, 150)),
                             (info_x, info_y))
            info_y += 18
            costs = list(craft_costs(self._craft_grid).items())
            ing_x = info_x
            for j, (iid, needed) in enumerate(costs):
                have = player.inventory.get(iid, 0)
                col = (65, 200, 65) if have >= needed else (210, 75, 75)
                ms = self.small.render(f"{ITEMS.get(iid,{}).get('name',iid)} {have}/{needed}", True, col)
                self.screen.blit(ms, (ing_x, info_y))
                ing_x += ms.get_width()
                if j < len(costs) - 1:
                    sep = self.small.render(" | ", True, (80, 90, 80))
                    self.screen.blit(sep, (ing_x, info_y))
                    ing_x += sep.get_width()
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
        SEARCH_H = 22
        SEARCH_Y = py + 28
        ry0 = SEARCH_Y + SEARCH_H + 4
        RCARD_STEP = RCARD_H + 5
        HEADER_STEP = 20
        panel_bottom = py + PH - 6

        # Search box + Craftable toggle on the same row
        BTN_W, BTN_GAP = 90, 6
        search_w = RCARD_W - BTN_W - BTN_GAP
        search_rect = pygame.Rect(rx0, SEARCH_Y, search_w, SEARCH_H)
        self._craft_search_rect = search_rect
        pygame.draw.rect(self.screen,
                         (38, 38, 52) if self._craft_search_active else (28, 28, 38),
                         search_rect)
        pygame.draw.rect(self.screen,
                         (140, 130, 80) if self._craft_search_active else (65, 65, 85),
                         search_rect, 1)
        disp = self._craft_search if self._craft_search else "Search recipes..."
        stxt = self.small.render(disp, True,
                                 (210, 200, 160) if self._craft_search else (80, 80, 100))
        self.screen.blit(stxt, (rx0 + 6, SEARCH_Y + SEARCH_H // 2 - stxt.get_height() // 2))
        if self._craft_search_active:
            cur_x = rx0 + 6 + stxt.get_width() + 1
            pygame.draw.line(self.screen, (200, 190, 120),
                             (cur_x, SEARCH_Y + 4), (cur_x, SEARCH_Y + SEARCH_H - 4))

        btn_x = rx0 + search_w + BTN_GAP
        btn_rect = pygame.Rect(btn_x, SEARCH_Y, BTN_W, SEARCH_H)
        self._craft_craftable_btn = btn_rect
        if self._craft_show_craftable:
            btn_bg, btn_br, btn_tc = (20, 70, 20), (55, 190, 55), (140, 240, 140)
        else:
            btn_bg, btn_br, btn_tc = (28, 28, 38), (65, 65, 85), (110, 110, 130)
        pygame.draw.rect(self.screen, btn_bg, btn_rect)
        pygame.draw.rect(self.screen, btn_br, btn_rect, 1)
        bl = self.small.render("Craftable", True, btn_tc)
        self.screen.blit(bl, (btn_x + BTN_W // 2 - bl.get_width() // 2,
                               SEARCH_Y + SEARCH_H // 2 - bl.get_height() // 2))

        # Build grouped display list (filtered by search and craftable toggle)
        query = self._craft_search.lower()
        only_craftable = self._craft_show_craftable

        def _recipe_passes(ridx):
            r = RECIPES[ridx]
            if query and query not in r["name"].lower():
                return False
            if only_craftable and not can_craft(r["pattern"], player.inventory):
                return False
            return True

        rid_by_output = {r["output_id"]: i for i, r in enumerate(RECIPES)}
        display_list = []
        seen = set()
        for group_name in RECIPE_GROUPS_ORDER:
            group_items = [rid_by_output[oid] for oid in RECIPE_GROUPS.get(group_name, [])
                           if oid in rid_by_output and _recipe_passes(rid_by_output[oid])]
            if group_items:
                display_list.append(("header", group_name))
                for ridx in group_items:
                    display_list.append(("recipe", ridx))
                    seen.add(ridx)
        ungrouped = [i for i in range(len(RECIPES))
                     if i not in seen and _recipe_passes(i)]
        if ungrouped:
            display_list.append(("header", "Other"))
            for ridx in ungrouped:
                display_list.append(("recipe", ridx))

        # Pixel-based scroll
        total_h = sum(HEADER_STEP if e[0] == "header" else RCARD_STEP for e in display_list)
        visible_h = panel_bottom - ry0
        self._max_recipe_scroll = max(0, total_h - visible_h)
        self._recipe_scroll = max(0, min(self._max_recipe_scroll, self._recipe_scroll))

        # Scrollbar
        if self._max_recipe_scroll > 0:
            sb_x = px + PW - 10
            sb_h = panel_bottom - ry0
            sb_th = max(20, sb_h * visible_h // total_h)
            sb_top = ry0 + (sb_h - sb_th) * self._recipe_scroll // self._max_recipe_scroll
            pygame.draw.rect(self.screen, (35, 35, 48), (sb_x, ry0, 7, sb_h))
            pygame.draw.rect(self.screen, (100, 100, 140), (sb_x, sb_top, 7, sb_th))

        self._recipe_rects.clear()
        cur_y = ry0 - self._recipe_scroll
        panel_clip = pygame.Rect(rx0, ry0, RCARD_W + 12, panel_bottom - ry0)
        old_panel_clip = self.screen.get_clip()
        self.screen.set_clip(panel_clip)

        for entry in display_list:
            is_header = entry[0] == "header"
            step = HEADER_STEP if is_header else RCARD_STEP
            item_h = HEADER_STEP if is_header else RCARD_H
            ry = cur_y
            cur_y += step

            if ry + item_h <= ry0:
                continue
            if ry >= panel_bottom:
                break

            if is_header:
                _, group_name = entry
                line_y = ry + HEADER_STEP // 2
                pygame.draw.line(self.screen, (65, 60, 42),
                                 (rx0, line_y), (rx0 + RCARD_W - 10, line_y), 1)
                lbl = self.small.render(group_name.upper(), True, (155, 140, 85))
                lbg_x, lbg_y = rx0 + 4, ry + (HEADER_STEP - lbl.get_height()) // 2
                pygame.draw.rect(self.screen, (22, 22, 30),
                                 (lbg_x - 2, lbg_y - 1, lbl.get_width() + 6, lbl.get_height() + 2))
                self.screen.blit(lbl, (lbg_x, lbg_y))
            else:
                _, ridx = entry
                recipe = RECIPES[ridx]
                rect = pygame.Rect(rx0, ry, RCARD_W, RCARD_H)
                self._recipe_rects[ridx] = rect

                out_id = recipe["output_id"]
                locked_r = is_research_locked(out_id, research)
                craftable_r = (not locked_r) and can_craft(recipe["pattern"], player.inventory)
                if locked_r:
                    bg = (38, 18, 18)
                    border = (130, 50, 50)
                elif craftable_r:
                    bg = (20, 45, 20)
                    border = (50, 180, 50)
                else:
                    bg = (24, 24, 32)
                    border = (52, 52, 68)
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

                # Name + cost (clipped to card bounds)
                old_clip = self.screen.get_clip()
                self.screen.set_clip(rect)
                name_x = out_x + sw + 8
                if locked_r:
                    req_nid = RESEARCH_LOCKED_RECIPES.get(out_id, "")
                    req_node = research.nodes.get(req_nid) if research else None
                    lk_s = self.small.render(
                        f"[R] {req_node.name if req_node else req_nid}", True, (160, 65, 65))
                    self.screen.blit(lk_s, (name_x, ry + 4 + 14))
                    nm_col = (180, 80, 80)
                else:
                    nm_col = (220, 210, 170) if craftable_r else (140, 140, 150)
                nm_s = self.small.render(recipe["name"], True, nm_col)
                self.screen.blit(nm_s, (name_x, ry + 4))
                if not locked_r:
                    costs = craft_costs(recipe["pattern"])
                    for line_i, (iid, cnt) in enumerate(costs.items()):
                        have = player.inventory.get(iid, 0)
                        col_c = (70, 200, 70) if have >= cnt else (190, 70, 70)
                        cs = self.small.render(
                            f"{ITEMS.get(iid, {}).get('name', iid)} {have}/{cnt}", True, col_c)
                        self.screen.blit(cs, (name_x, ry + 4 + 14 * (line_i + 1)))
                self.screen.set_clip(old_clip)

        self.screen.set_clip(old_panel_clip)

    def _draw_bakery(self, player):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("BAKERY", True, (220, 160, 80))
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close  |  Select a recipe and click BAKE",
                                 True, (120, 120, 130))
        self.screen.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, 26))

        # Craftable toggle (top-right)
        CB_W, CB_H = 90, 22
        cb_rect = pygame.Rect(SCREEN_W - CB_W - 16, 6, CB_W, CB_H)
        self._bakery_craftable_btn = cb_rect
        if self._bakery_show_craftable:
            cb_bg, cb_br, cb_tc = (20, 70, 20), (55, 190, 55), (140, 240, 140)
        else:
            cb_bg, cb_br, cb_tc = (25, 25, 35), (65, 65, 85), (110, 110, 130)
        pygame.draw.rect(self.screen, cb_bg, cb_rect)
        pygame.draw.rect(self.screen, cb_br, cb_rect, 1)
        cb_lbl = self.small.render("Craftable", True, cb_tc)
        self.screen.blit(cb_lbl, (cb_rect.centerx - cb_lbl.get_width() // 2,
                                   cb_rect.centery - cb_lbl.get_height() // 2))

        # --- Left panel: recipe list ---
        LIST_X, LIST_Y = 30, 55
        LIST_W, ROW_H, GAP = 260, 58, 4
        ICON_SZ = 28
        LIST_BOTTOM = SCREEN_H - 10
        visible_count = (LIST_BOTTOM - LIST_Y) // (ROW_H + GAP)

        bakery_indexed = [
            (i, r) for i, r in enumerate(BAKERY_RECIPES)
            if not self._bakery_show_craftable
            or all(player.inventory.get(iid, 0) >= cnt for iid, cnt in r["ingredients"].items())
        ]
        self._max_bakery_scroll = max(0, len(bakery_indexed) - visible_count)
        self._bakery_scroll = max(0, min(self._max_bakery_scroll, self._bakery_scroll))

        # Scrollbar
        if self._max_bakery_scroll > 0:
            sb_x = LIST_X + LIST_W + 4
            sb_h = LIST_BOTTOM - LIST_Y
            sb_th = max(20, sb_h * visible_count // len(bakery_indexed))
            sb_top = LIST_Y + (sb_h - sb_th) * self._bakery_scroll // self._max_bakery_scroll
            pygame.draw.rect(self.screen, (35, 25, 10), (sb_x, LIST_Y, 7, sb_h))
            pygame.draw.rect(self.screen, (160, 110, 50), (sb_x, sb_top, 7, sb_th))

        self._bakery_recipe_rects.clear()
        for slot, (i, recipe) in enumerate(bakery_indexed):
            display_idx = slot - self._bakery_scroll
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
            ing_x = LIST_X + 4 + ICON_SZ + 6
            ing_y = ry + 5 + 15
            for j, (item_id, count) in enumerate(recipe["ingredients"].items()):
                have = player.inventory.get(item_id, 0)
                item_name = ITEMS.get(item_id, {}).get("name", item_id)
                col = (120, 210, 100) if have >= count else (210, 80, 60)
                seg = self.small.render(f"{item_name} {have}/{count}", True, col)
                self.screen.blit(seg, (ing_x, ing_y))
                ing_x += seg.get_width()
                if j < len(recipe["ingredients"]) - 1:
                    sep = self.small.render(" | ", True, (100, 100, 110))
                    self.screen.blit(sep, (ing_x, ing_y))
                    ing_x += sep.get_width()
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

        nut_y = self._draw_food_nutrition(DX, iy + 34, out_data, accent=(220, 160, 80))
        btn_top = max(iy + 40, nut_y + 6)

        # BAKE button
        can_bake = all(
            player.inventory.get(iid, 0) >= cnt
            for iid, cnt in recipe["ingredients"].items()
        )
        btn_col  = (160, 100, 40) if can_bake else (60, 50, 40)
        btn_rect = pygame.Rect(DX, btn_top, 120, 34)
        pygame.draw.rect(self.screen, btn_col, btn_rect)
        pygame.draw.rect(self.screen, (220, 160, 80) if can_bake else (80, 70, 60), btn_rect, 2)
        btn_txt = self.font.render("BAKE", True,
                                   (255, 220, 120) if can_bake else (100, 90, 70))
        self.screen.blit(btn_txt, (btn_rect.centerx - btn_txt.get_width() // 2,
                                   btn_rect.centery - btn_txt.get_height() // 2))
        self._refine_btn = btn_rect

    def _draw_food_nutrition(self, x, y, item_data, accent=(180, 140, 60)):
        """Draw a nutrition breakdown for a food output. Returns the y after the panel."""
        if not item_data.get("edible"):
            return y
        hunger   = item_data.get("hunger_restore", 0)
        protein  = item_data.get("protein_factor", 0.0)
        fiber    = item_data.get("fiber_factor",   0.0)
        vitamins = item_data.get("vitamin_factor", 0.0)
        sugar    = item_data.get("sugar_factor",   0.0)

        hdr = self.small.render("Nutrition", True, accent)
        self.screen.blit(hdr, (x, y))
        y += 16

        self._draw_nutrition_bar_simple(x, y, hunger / 100.0, (110, 195, 110),
                                        f"Hunger   +{hunger}")
        y += 18
        self._draw_nutrition_bar_simple(x, y, protein,  (210, 120,  80), f"Protein  {protein:.2f}")
        y += 18
        self._draw_nutrition_bar_simple(x, y, fiber,    ( 80, 175,  90), f"Fiber    {fiber:.2f}")
        y += 18
        self._draw_nutrition_bar_simple(x, y, vitamins, ( 90, 180, 220), f"Vitamins {vitamins:.2f}")
        y += 18
        self._draw_nutrition_bar_simple(x, y, sugar,    (235, 200,  60), f"Sugar    {sugar:.2f}")
        y += 18
        return y

    def _draw_nutrition_bar_simple(self, x, y, value, color, label):
        SEGS, SEG_W, SEG_H, SEG_GAP = 10, 12, 8, 2
        filled = round(max(0.0, min(1.0, value)) * SEGS)
        label_s = self.small.render(label, True, (185, 160, 120))
        self.screen.blit(label_s, (x, y))
        bx = x + 110
        for i in range(SEGS):
            col = color if i < filled else (45, 35, 25)
            pygame.draw.rect(self.screen, col, (bx + i * (SEG_W + SEG_GAP), y, SEG_W, SEG_H))

    def _draw_cooking_station(self, player, recipe_list, title_str, title_color,
                               selected_idx, recipe_rects_dict, block_id=None,
                               action_label="COOK", show_block_grid=False):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render(title_str, True, title_color)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render(f"ESC to close  |  Select a recipe and click {action_label}",
                                 True, (120, 120, 130))
        self.screen.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, 26))

        # Craftable toggle (top-right, always shown)
        only_craftable = self._cook_station_craftable.get(block_id, False)
        CB_W, CB_H = 90, 22
        cb_x = SCREEN_W - CB_W - 16
        cb_y = 6
        if show_block_grid:
            cb_y = 34   # shift down so it doesn't overlap the VIEW ALL button
        cb_rect = pygame.Rect(cb_x, cb_y, CB_W, CB_H)
        self._cook_station_craftable_btn = cb_rect
        if only_craftable:
            cb_bg, cb_br, cb_tc = (20, 70, 20), (55, 190, 55), (140, 240, 140)
        else:
            cb_bg, cb_br, cb_tc = (25, 25, 35), (65, 65, 85), (110, 110, 130)
        pygame.draw.rect(self.screen, cb_bg, cb_rect)
        pygame.draw.rect(self.screen, cb_br, cb_rect, 1)
        cb_lbl = self.small.render("Craftable", True, cb_tc)
        self.screen.blit(cb_lbl, (cb_x + CB_W // 2 - cb_lbl.get_width() // 2,
                                   cb_y + CB_H // 2 - cb_lbl.get_height() // 2))

        if show_block_grid:
            vab_label = "VIEW RECIPES" if self._gw_view_all else "VIEW ALL BLOCKS"
            vab_s = self.small.render(vab_label, True, title_color)
            vab_rect = pygame.Rect(SCREEN_W - vab_s.get_width() - 28, 10,
                                   vab_s.get_width() + 16, 22)
            pygame.draw.rect(self.screen, (40, 55, 30) if self._gw_view_all else (25, 35, 15), vab_rect)
            pygame.draw.rect(self.screen, title_color, vab_rect, 1)
            self.screen.blit(vab_s, (vab_rect.x + 8, vab_rect.y + 3))
            self._gw_view_all_btn = vab_rect

            if self._gw_view_all:
                sorted_recipes = sorted(enumerate(recipe_list), key=lambda x: x[1]["name"])
                LIST_X  = 30
                LIST_Y  = 55
                LIST_BOTTOM = SCREEN_H - 10
                CELL    = 88
                GRID_W  = SCREEN_W - LIST_X - 16
                cols    = max(1, GRID_W // CELL)
                total_rows = max(1, (len(sorted_recipes) + cols - 1) // cols)
                vis_rows   = max(1, (LIST_BOTTOM - LIST_Y) // CELL)
                max_gs     = max(0, total_rows - vis_rows)
                self._gw_grid_scroll = max(0, min(max_gs, self._gw_grid_scroll))
                row_off = self._gw_grid_scroll

                if max_gs > 0:
                    sb_x  = LIST_X + cols * CELL + 2
                    sb_h  = LIST_BOTTOM - LIST_Y
                    sb_th = max(20, sb_h * vis_rows // total_rows)
                    sb_top = LIST_Y + (sb_h - sb_th) * row_off // max_gs
                    pygame.draw.rect(self.screen, (20, 35, 25), (sb_x, LIST_Y, 7, sb_h))
                    pygame.draw.rect(self.screen, title_color, (sb_x, sb_top, 7, sb_th))

                self._gw_grid_rects.clear()
                block_surfs = getattr(self, "_block_surfs", None)
                for slot, (i, recipe) in enumerate(sorted_recipes):
                    c = slot % cols
                    r = slot // cols - row_off
                    if r < 0:
                        continue
                    cx = LIST_X + c * CELL
                    cy = LIST_Y + r * CELL
                    if cy + CELL > LIST_BOTTOM:
                        break
                    can_cook_r = all(player.inventory.get(iid, 0) >= cnt
                                     for iid, cnt in recipe["ingredients"].items())
                    selected = (i == selected_idx)
                    bg = ((60, 110, 80) if can_cook_r else (75, 45, 45)) if selected \
                        else ((18, 48, 30) if can_cook_r else (24, 24, 32))
                    border = title_color if selected \
                        else ((45, 140, 75) if can_cook_r else (52, 52, 68))
                    cell_rect = pygame.Rect(cx + 2, cy + 2, CELL - 4, CELL - 4)
                    pygame.draw.rect(self.screen, bg, cell_rect)
                    pygame.draw.rect(self.screen, border, cell_rect, 1)
                    out_id      = recipe["output_id"]
                    out_data    = ITEMS.get(out_id, {})
                    place_block = out_data.get("place_block")
                    raw_surf    = block_surfs.get(place_block) if block_surfs and place_block else None
                    if raw_surf:
                        icon = pygame.transform.scale(raw_surf, (52, 52))
                    else:
                        icon = render_item_icon(out_id, out_data.get("color", (80, 80, 80)), 52)
                    self.screen.blit(icon, (cx + CELL // 2 - 26, cy + 6))
                    name_col = out_data.get("color", (200, 200, 200)) if can_cook_r else (110, 110, 120)
                    short = recipe["name"] if len(recipe["name"]) <= 11 else recipe["name"][:10] + "…"
                    ns = self.small.render(short, True, name_col)
                    self.screen.blit(ns, (cx + CELL // 2 - ns.get_width() // 2, cy + 62))
                    self._gw_grid_rects[i] = cell_rect
                return

        # --- Left panel: recipe list ---
        LIST_X, LIST_Y = 30, 55
        LIST_W, ROW_H, GAP = 270, 58, 4
        ICON_SZ = 28
        LIST_BOTTOM = SCREEN_H - 10
        visible_count = (LIST_BOTTOM - LIST_Y) // (ROW_H + GAP)

        all_sorted = sorted(enumerate(recipe_list), key=lambda x: x[1]["name"])
        if only_craftable:
            sorted_recipes = [(i, r) for i, r in all_sorted
                              if all(player.inventory.get(iid, 0) >= cnt
                                     for iid, cnt in r["ingredients"].items())]
        else:
            sorted_recipes = all_sorted

        max_scroll = max(0, len(sorted_recipes) - visible_count)
        scroll = self._cook_station_scroll.get(block_id, 0)
        scroll = max(0, min(max_scroll, scroll))
        if block_id is not None:
            self._cook_station_scroll[block_id] = scroll
            self._cook_station_max_scroll[block_id] = max_scroll

        if max_scroll > 0:
            sb_x = LIST_X + LIST_W + 4
            sb_h = LIST_BOTTOM - LIST_Y
            sb_th = max(20, sb_h * visible_count // len(sorted_recipes))
            sb_top = LIST_Y + (sb_h - sb_th) * scroll // max_scroll
            pygame.draw.rect(self.screen, (20, 35, 25), (sb_x, LIST_Y, 7, sb_h))
            pygame.draw.rect(self.screen, title_color, (sb_x, sb_top, 7, sb_th))

        recipe_rects_dict.clear()
        for slot, (i, recipe) in enumerate(sorted_recipes):
            display_idx = slot - scroll
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
            ing_x = LIST_X + 4 + ICON_SZ + 6
            ing_y = ry + 5 + 15
            for j, (item_id, count) in enumerate(recipe["ingredients"].items()):
                have = player.inventory.get(item_id, 0)
                item_name = ITEMS.get(item_id, {}).get("name", item_id)
                col = (100, 200, 120) if have >= count else (200, 80, 60)
                seg = self.small.render(f"{item_name} {have}/{count}", True, col)
                self.screen.blit(seg, (ing_x, ing_y))
                ing_x += seg.get_width()
                if j < len(recipe["ingredients"]) - 1:
                    sep = self.small.render(" | ", True, (80, 90, 80))
                    self.screen.blit(sep, (ing_x, ing_y))
                    ing_x += sep.get_width()
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

        nut_y = self._draw_food_nutrition(DX, iy + 34, out_data, accent=title_color)
        btn_top = max(iy + 40, nut_y + 6)

        can_cook = all(
            player.inventory.get(iid, 0) >= cnt
            for iid, cnt in recipe["ingredients"].items()
        )
        btn_col  = (40, 100, 60) if can_cook else (40, 50, 40)
        btn_rect = pygame.Rect(DX, btn_top, 120, 34)
        pygame.draw.rect(self.screen, btn_col, btn_rect)
        pygame.draw.rect(self.screen, title_color if can_cook else (60, 70, 60), btn_rect, 2)
        btn_txt = self.font.render(action_label, True,
                                   (200, 255, 180) if can_cook else (80, 100, 80))
        self.screen.blit(btn_txt, (btn_rect.centerx - btn_txt.get_width() // 2,
                                   btn_rect.centery - btn_txt.get_height() // 2))
        self._refine_btn = btn_rect

        # Block preview: show the actual in-world tile when the output is placeable
        place_block = out_data.get("place_block")
        block_surfs = getattr(self, '_block_surfs', None)
        if place_block is not None and block_surfs is not None:
            surf = block_surfs.get(place_block)
            if surf is not None:
                PREVIEW_SZ = 96
                preview = pygame.transform.scale(surf, (PREVIEW_SZ, PREVIEW_SZ))
                px = DX
                py = btn_rect.bottom + 16
                lbl = self.small.render("In-world:", True, (110, 110, 110))
                self.screen.blit(lbl, (px, py))
                self.screen.blit(preview, (px, py + 14))
                pygame.draw.rect(self.screen, (70, 70, 70), (px, py + 14, PREVIEW_SZ, PREVIEW_SZ), 1)

    def _draw_artisan_bench(self, player):
        from blocks import ARTISAN_BENCH_BLOCK
        TITLE_COLOR = (210, 180, 130)

        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("ARTISAN BENCH", True, TITLE_COLOR)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close  |  Select a recipe and click CRAFT",
                                 True, (120, 120, 130))
        self.screen.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, 26))

        # View All Blocks toggle button (top-right)
        vab_label = "VIEW RECIPES" if self._artisan_view_all else "VIEW ALL BLOCKS"
        vab_s = self.small.render(vab_label, True, TITLE_COLOR)
        vab_rect = pygame.Rect(SCREEN_W - vab_s.get_width() - 28, 10, vab_s.get_width() + 16, 22)
        pygame.draw.rect(self.screen, (60, 48, 24) if self._artisan_view_all else (35, 28, 14), vab_rect)
        pygame.draw.rect(self.screen, TITLE_COLOR, vab_rect, 1)
        self.screen.blit(vab_s, (vab_rect.x + 8, vab_rect.y + 3))
        self._artisan_view_all_btn = vab_rect

        LIST_X, LIST_W = 30, 290
        TAB_H, TAB_GAP = 22, 2
        n_tabs = len(ARTISAN_TABS)
        tab_w  = (LIST_W - TAB_GAP * (n_tabs - 1)) // n_tabs

        # --- Tabs ---
        self._artisan_tab_rects = []
        for i, label in enumerate(ARTISAN_TABS):
            tx       = LIST_X + i * (tab_w + TAB_GAP)
            active   = (i == self._artisan_tab)
            tab_rect = pygame.Rect(tx, 46, tab_w, TAB_H)
            pygame.draw.rect(self.screen, (70, 55, 30) if active else (25, 20, 12), tab_rect)
            pygame.draw.rect(self.screen, TITLE_COLOR if active else (80, 70, 50), tab_rect, 1)
            lbl = self.small.render(label, True, TITLE_COLOR if active else (140, 120, 90))
            self.screen.blit(lbl, (tab_rect.centerx - lbl.get_width() // 2,
                                   tab_rect.centery - lbl.get_height() // 2))
            self._artisan_tab_rects.append(tab_rect)

        # --- Search box + Craftable toggle ---
        SEARCH_Y = 46 + TAB_H + 4
        SEARCH_H = 22
        CB_W, CB_GAP = 90, 6
        search_w = LIST_W - CB_W - CB_GAP
        search_rect = pygame.Rect(LIST_X, SEARCH_Y, search_w, SEARCH_H)
        self._artisan_search_rect = search_rect
        pygame.draw.rect(self.screen,
                         (45, 38, 22) if self._artisan_search_active else (30, 25, 15),
                         search_rect)
        pygame.draw.rect(self.screen,
                         TITLE_COLOR if self._artisan_search_active else (80, 70, 50),
                         search_rect, 1)
        display_str = self._artisan_search if self._artisan_search else "Search..."
        stxt = self.small.render(display_str, True,
                                 (200, 185, 150) if self._artisan_search else (90, 80, 60))
        self.screen.blit(stxt, (LIST_X + 6, SEARCH_Y + SEARCH_H // 2 - stxt.get_height() // 2))
        if self._artisan_search_active:
            cur_x = LIST_X + 6 + stxt.get_width() + 1
            pygame.draw.line(self.screen, TITLE_COLOR,
                             (cur_x, SEARCH_Y + 4), (cur_x, SEARCH_Y + SEARCH_H - 4))

        cb_x = LIST_X + search_w + CB_GAP
        cb_rect = pygame.Rect(cb_x, SEARCH_Y, CB_W, SEARCH_H)
        self._artisan_craftable_btn = cb_rect
        if self._artisan_show_craftable:
            cb_bg, cb_br, cb_tc = (20, 70, 20), (55, 190, 55), (140, 240, 140)
        else:
            cb_bg, cb_br, cb_tc = (30, 25, 15), (80, 70, 50), (110, 110, 130)
        pygame.draw.rect(self.screen, cb_bg, cb_rect)
        pygame.draw.rect(self.screen, cb_br, cb_rect, 1)
        cb_lbl = self.small.render("Craftable", True, cb_tc)
        self.screen.blit(cb_lbl, (cb_x + CB_W // 2 - cb_lbl.get_width() // 2,
                                   SEARCH_Y + SEARCH_H // 2 - cb_lbl.get_height() // 2))

        # --- Filter recipes ---
        query   = self._artisan_search.lower()
        tab_idx = self._artisan_tab
        filtered = sorted(
            [(fi, r) for fi, r in enumerate(ARTISAN_RECIPES)
             if (tab_idx == 0 or ARTISAN_RECIPE_TAB[fi] == tab_idx)
             and (not query or query in r["name"].lower())
             and (not self._artisan_show_craftable
                  or all(player.inventory.get(iid, 0) >= cnt
                         for iid, cnt in r["ingredients"].items()))],
            key=lambda x: x[1]["name"]
        )

        # Auto-reset selection when it falls outside the filtered view
        sel_idx = self._artisan_selected_recipe
        if filtered and sel_idx not in {fi for fi, _ in filtered}:
            self._artisan_selected_recipe = filtered[0][0]
            sel_idx = self._artisan_selected_recipe

        # --- Recipe list or grid ---
        LIST_Y      = SEARCH_Y + SEARCH_H + 6
        LIST_BOTTOM = SCREEN_H - 10

        if self._artisan_view_all:
            # ── Grid view: all filtered recipes as icon tiles ──
            CELL        = 88
            GRID_X      = LIST_X
            GRID_W      = SCREEN_W - LIST_X - 16
            cols        = max(1, GRID_W // CELL)
            total_rows  = max(1, (len(filtered) + cols - 1) // cols)
            vis_rows    = max(1, (LIST_BOTTOM - LIST_Y) // CELL)
            max_gs      = max(0, total_rows - vis_rows)
            self._artisan_grid_scroll = max(0, min(max_gs, self._artisan_grid_scroll))
            row_off     = self._artisan_grid_scroll

            if max_gs > 0:
                sb_x  = GRID_X + cols * CELL + 2
                sb_h  = LIST_BOTTOM - LIST_Y
                sb_th = max(20, sb_h * vis_rows // total_rows)
                sb_top = LIST_Y + (sb_h - sb_th) * row_off // max_gs
                pygame.draw.rect(self.screen, (20, 35, 25), (sb_x, LIST_Y, 7, sb_h))
                pygame.draw.rect(self.screen, TITLE_COLOR,  (sb_x, sb_top, 7, sb_th))

            self._artisan_grid_rects.clear()
            if not filtered:
                msg = self.small.render("No results", True, (100, 90, 70))
                self.screen.blit(msg, (GRID_X + 10, LIST_Y + 10))
            for slot, (fi, recipe) in enumerate(filtered):
                c   = slot % cols
                r   = slot // cols - row_off
                if r < 0:
                    continue
                cx  = GRID_X + c * CELL
                cy  = LIST_Y + r * CELL
                if cy + CELL > LIST_BOTTOM:
                    break
                can_cook_r = all(player.inventory.get(iid, 0) >= cnt
                                 for iid, cnt in recipe["ingredients"].items())
                selected   = (fi == sel_idx)
                bg = ((60, 110, 80) if can_cook_r else (75, 45, 45)) if selected \
                    else ((18, 48, 30) if can_cook_r else (24, 24, 32))
                border = TITLE_COLOR if selected \
                    else ((45, 140, 75) if can_cook_r else (52, 52, 68))
                cell_rect = pygame.Rect(cx + 2, cy + 2, CELL - 4, CELL - 4)
                pygame.draw.rect(self.screen, bg, cell_rect)
                pygame.draw.rect(self.screen, border, cell_rect, 1)
                out_id      = recipe["output_id"]
                out_data    = ITEMS.get(out_id, {})
                block_surfs = getattr(self, "_block_surfs", None)
                place_block = out_data.get("place_block")
                raw_surf    = block_surfs.get(place_block) if block_surfs and place_block else None
                if raw_surf:
                    icon = pygame.transform.scale(raw_surf, (52, 52))
                else:
                    icon = render_item_icon(out_id, out_data.get("color", (80, 80, 80)), 52)
                self.screen.blit(icon, (cx + CELL // 2 - 26, cy + 6))
                name_col = out_data.get("color", (200, 200, 200)) if can_cook_r else (110, 110, 120)
                short = recipe["name"] if len(recipe["name"]) <= 11 else recipe["name"][:10] + "…"
                ns = self.small.render(short, True, name_col)
                self.screen.blit(ns, (cx + CELL // 2 - ns.get_width() // 2, cy + 62))
                self._artisan_grid_rects[fi] = cell_rect
        else:
            # ── Normal list view ──
            ROW_H, GAP, ICON_SZ = 58, 4, 28
            visible_count = max(1, (LIST_BOTTOM - LIST_Y) // (ROW_H + GAP))
            max_scroll    = max(0, len(filtered) - visible_count)
            bid           = ARTISAN_BENCH_BLOCK
            scroll        = max(0, min(max_scroll, self._cook_station_scroll.get(bid, 0)))
            self._cook_station_scroll[bid]     = scroll
            self._cook_station_max_scroll[bid] = max_scroll

            if max_scroll > 0:
                sb_x   = LIST_X + LIST_W + 4
                sb_h   = LIST_BOTTOM - LIST_Y
                sb_th  = max(20, sb_h * visible_count // len(filtered))
                sb_top = LIST_Y + (sb_h - sb_th) * scroll // max_scroll
                pygame.draw.rect(self.screen, (20, 35, 25), (sb_x, LIST_Y, 7, sb_h))
                pygame.draw.rect(self.screen, TITLE_COLOR,  (sb_x, sb_top, 7, sb_th))

            self._artisan_recipe_rects.clear()
            if not filtered:
                msg = self.small.render("No results", True, (100, 90, 70))
                self.screen.blit(msg, (LIST_X + 10, LIST_Y + 10))
            for slot, (fi, recipe) in enumerate(filtered):
                display_slot = slot - scroll
                if display_slot < 0:
                    continue
                ry = LIST_Y + display_slot * (ROW_H + GAP)
                if ry + ROW_H > LIST_BOTTOM:
                    break
                can_cook_r = all(player.inventory.get(iid, 0) >= cnt
                                 for iid, cnt in recipe["ingredients"].items())
                selected   = (fi == sel_idx)
                bg = ((60, 110, 80) if can_cook_r else (75, 45, 45)) if selected \
                    else ((18, 48, 30) if can_cook_r else (24, 24, 32))
                border = TITLE_COLOR if selected \
                    else ((45, 140, 75) if can_cook_r else (52, 52, 68))
                row_rect = pygame.Rect(LIST_X, ry, LIST_W, ROW_H)
                pygame.draw.rect(self.screen, bg, row_rect)
                pygame.draw.rect(self.screen, border, row_rect, 1)
                out_id   = recipe["output_id"]
                out_data = ITEMS.get(out_id, {})
                icon = render_item_icon(out_id, out_data.get("color", (80, 80, 80)), ICON_SZ)
                self.screen.blit(icon, (LIST_X + 4, ry + (ROW_H - ICON_SZ) // 2))
                name_col = out_data.get("color", (200, 200, 200)) if can_cook_r else (110, 110, 120)
                self.screen.blit(self.font.render(recipe["name"], True, name_col),
                                 (LIST_X + 4 + ICON_SZ + 6, ry + 5))
                ing_x, ing_y = LIST_X + 4 + ICON_SZ + 6, ry + 20
                for j, (item_id, count) in enumerate(recipe["ingredients"].items()):
                    have = player.inventory.get(item_id, 0)
                    col  = (100, 200, 120) if have >= count else (200, 80, 60)
                    seg  = self.small.render(
                        f"{ITEMS.get(item_id, {}).get('name', item_id)} {have}/{count}", True, col)
                    self.screen.blit(seg, (ing_x, ing_y))
                    ing_x += seg.get_width()
                    if j < len(recipe["ingredients"]) - 1:
                        sep = self.small.render(" | ", True, (80, 90, 80))
                        self.screen.blit(sep, (ing_x, ing_y))
                        ing_x += sep.get_width()
                self._artisan_recipe_rects[fi] = row_rect

        if self._artisan_view_all:
            return

        # --- Right panel: selected recipe detail ---
        recipe   = ARTISAN_RECIPES[sel_idx] if filtered else ARTISAN_RECIPES[0]
        DX, DY   = LIST_X + LIST_W + 30, 55
        self.screen.blit(self.font.render(recipe["name"], True, (220, 210, 170)), (DX, DY))
        iy = DY + 30
        for item_id, count in recipe["ingredients"].items():
            have = player.inventory.get(item_id, 0)
            col  = (180, 220, 100) if have >= count else (220, 80, 60)
            self.screen.blit(
                self.small.render(
                    f"{ITEMS.get(item_id, {}).get('name', item_id)}: {have}/{count}", True, col),
                (DX, iy))
            iy += 20
        self.screen.blit(self.font.render("→", True, (160, 160, 80)), (DX, iy + 4))
        out_data = ITEMS.get(recipe["output_id"], {})
        self.screen.blit(
            self.font.render(out_data.get("name", recipe["output_id"]), True,
                             out_data.get("color", (200, 200, 200))),
            (DX + 24, iy + 4))
        nut_y   = self._draw_food_nutrition(DX, iy + 34, out_data, accent=TITLE_COLOR)
        btn_top = max(iy + 40, nut_y + 6)
        can_cook = all(player.inventory.get(iid, 0) >= cnt
                       for iid, cnt in recipe["ingredients"].items())
        btn_rect = pygame.Rect(DX, btn_top, 120, 34)
        pygame.draw.rect(self.screen, (40, 100, 60) if can_cook else (40, 50, 40), btn_rect)
        pygame.draw.rect(self.screen, TITLE_COLOR if can_cook else (60, 70, 60), btn_rect, 2)
        btn_txt = self.font.render("CRAFT", True, (200, 255, 180) if can_cook else (80, 100, 80))
        self.screen.blit(btn_txt, (btn_rect.centerx - btn_txt.get_width() // 2,
                                   btn_rect.centery - btn_txt.get_height() // 2))
        self._refine_btn = btn_rect

        place_block = out_data.get("place_block")
        block_surfs = getattr(self, "_block_surfs", None)
        if place_block and block_surfs:
            surf = block_surfs.get(place_block)
            if surf:
                PREVIEW_SZ = 96
                preview    = pygame.transform.scale(surf, (PREVIEW_SZ, PREVIEW_SZ))
                px, py     = DX, btn_rect.bottom + 16
                self.screen.blit(self.small.render("In-world:", True, (110, 110, 110)), (px, py))
                self.screen.blit(preview, (px, py + 14))
                pygame.draw.rect(self.screen, (70, 70, 70),
                                 (px, py + 14, PREVIEW_SZ, PREVIEW_SZ), 1)

    def _draw_refinery(self, player, dt=0.0):
        from blocks import (FOSSIL_TABLE_BLOCK, ROASTER_BLOCK, BLEND_STATION_BLOCK,
                            BREW_STATION_BLOCK, GEM_CUTTER_BLOCK, BAKERY_BLOCK,
                            WOK_BLOCK, STEAMER_BLOCK, NOODLE_POT_BLOCK,
                            BBQ_GRILL_BLOCK, CLAY_POT_BLOCK, DESERT_FORGE_BLOCK,
                            ARTISAN_BENCH_BLOCK,
                            GRAPE_PRESS_BLOCK, FERMENTATION_BLOCK, WINE_CELLAR_BLOCK,
                            STILL_BLOCK, BARREL_ROOM_BLOCK, BOTTLING_BLOCK,
                            BREW_KETTLE_BLOCK, FERM_VESSEL_BLOCK, TAPROOM_BLOCK,
                            COMPOST_BIN_BLOCK,
                            WITHERING_RACK_BLOCK, OXIDATION_STATION_BLOCK, TEA_CELLAR_BLOCK, ROASTING_KILN_BLOCK,
                            DRYING_RACK_BLOCK, KILN_BLOCK, RESONANCE_BLOCK, MORTAR_BLOCK,
                            BAIT_STATION_BLOCK,
                            SPINNING_WHEEL_BLOCK, DYE_VAT_BLOCK, LOOM_BLOCK,
                            DAIRY_VAT_BLOCK, CHEESE_PRESS_BLOCK, AGING_CAVE_BLOCK,
                            FLETCHING_TABLE_BLOCK, SMELTER_BLOCK, ANAEROBIC_TANK_BLOCK,
                            GLASS_KILN_BLOCK, GARDEN_WORKSHOP_BLOCK,
                            JEWELRY_WORKBENCH_BLOCK, JUICER_BLOCK,
                            AUTOMATION_BENCH_BLOCK, WEAPON_ASSEMBLER_BLOCK)
        from blocks import TANNING_RACK_BLOCK
        if self.refinery_block_id == TANNING_RACK_BLOCK:
            self._draw_cooking_station(player, TANNING_RACK_RECIPES, "TANNING RACK",
                                       (145, 105, 60), self._tanning_rack_selected_recipe,
                                       self._tanning_rack_recipe_rects,
                                       block_id=TANNING_RACK_BLOCK,
                                       action_label="TAN")
            return
        if self.refinery_block_id == JEWELRY_WORKBENCH_BLOCK:
            self._draw_jewelry_workbench(player, dt)
            return
        if self.refinery_block_id == FOSSIL_TABLE_BLOCK:
            self._draw_fossil_table(player, dt)
            return
        if self.refinery_block_id == ROASTER_BLOCK:
            self._draw_roaster(player, dt)
            return
        from blocks import SCRIBES_DESK_BLOCK, LECTERN_BLOCK, BOOKCASE_BLOCK
        if self.refinery_block_id == SCRIBES_DESK_BLOCK:
            self._draw_scribes_desk(player, dt)
            return
        if self.refinery_block_id == LECTERN_BLOCK:
            self._draw_lectern(player, dt)
            return
        if self.refinery_block_id == BOOKCASE_BLOCK:
            self._draw_bookcase(player, dt)
            return
        if self.refinery_block_id == BLEND_STATION_BLOCK:
            self._draw_blend_station(player)
            return
        if self.refinery_block_id == BREW_STATION_BLOCK:
            self._draw_brew_station(player)
            return
        if self.refinery_block_id == GRAPE_PRESS_BLOCK:
            self._draw_grape_press(player, dt)
            return
        if self.refinery_block_id == FERMENTATION_BLOCK:
            self._draw_fermenter(player, dt)
            return
        if self.refinery_block_id == WINE_CELLAR_BLOCK:
            self._draw_wine_cellar(player, dt)
            return
        if self.refinery_block_id == STILL_BLOCK:
            self._draw_still(player, dt)
            return
        if self.refinery_block_id == BARREL_ROOM_BLOCK:
            self._draw_barrel_room(player, dt)
            return
        if self.refinery_block_id == BOTTLING_BLOCK:
            self._draw_bottling_station(player, dt)
            return
        if self.refinery_block_id == BREW_KETTLE_BLOCK:
            self._draw_brew_kettle(player, dt)
            return
        if self.refinery_block_id == FERM_VESSEL_BLOCK:
            self._draw_ferm_vessel(player, dt)
            return
        if self.refinery_block_id == TAPROOM_BLOCK:
            self._draw_taproom(player, dt)
            return
        from blocks import FALCONER_PERCH, MEWS_BLOCK
        if self.refinery_block_id in (FALCONER_PERCH, MEWS_BLOCK):
            self.update_falconry(dt, player)
            self.tick_raptor_cooldowns(dt, player)
            self._draw_falconer_perch(player)
            if getattr(self, "falconry_capture_open", False):
                self._draw_falconry_capture(player)
            return
        if self.refinery_block_id == WITHERING_RACK_BLOCK:
            self._draw_withering_rack(player, dt)
            return
        if self.refinery_block_id == OXIDATION_STATION_BLOCK:
            self._draw_oxidation_station(player, dt)
            return
        if self.refinery_block_id == TEA_CELLAR_BLOCK:
            self._draw_tea_cellar(player, dt)
            return
        if self.refinery_block_id == ROASTING_KILN_BLOCK:
            self._draw_roasting_kiln(player, dt)
            return
        if self.refinery_block_id == DRYING_RACK_BLOCK:
            self._draw_drying_rack(player, dt)
            return
        if self.refinery_block_id == MORTAR_BLOCK:
            self._draw_mortar(player, dt)
            return
        if self.refinery_block_id == KILN_BLOCK:
            self._draw_kiln(player, dt, getattr(self, "_research", None))
            return
        if self.refinery_block_id == RESONANCE_BLOCK:
            self._draw_resonance_chamber(player, dt, getattr(self, "_research", None))
            return
        if self.refinery_block_id == SPINNING_WHEEL_BLOCK:
            self._draw_spinning_wheel(player, dt)
            return
        if self.refinery_block_id == DYE_VAT_BLOCK:
            self._draw_dye_vat(player, dt)
            return
        if self.refinery_block_id == LOOM_BLOCK:
            self._draw_loom(player, dt)
            return
        if self.refinery_block_id == DAIRY_VAT_BLOCK:
            self._draw_dairy_vat(player, dt)
            return
        if self.refinery_block_id == CHEESE_PRESS_BLOCK:
            self._draw_cheese_press(player, dt)
            return
        if self.refinery_block_id == AGING_CAVE_BLOCK:
            self._draw_aging_cave(player, dt)
            return
        if self.refinery_block_id == GEM_CUTTER_BLOCK:
            self._draw_gem_cutter(player, dt)
            return
        if self.refinery_block_id == BAKERY_BLOCK:
            self._draw_bakery(player)
            return
        if self.refinery_block_id == WOK_BLOCK:
            self._draw_cooking_station(player, WOK_RECIPES, "WOK",
                                       (220, 100, 40), self._wok_selected_recipe,
                                       self._wok_recipe_rects,
                                       block_id=WOK_BLOCK)
            return
        if self.refinery_block_id == STEAMER_BLOCK:
            self._draw_cooking_station(player, STEAMER_RECIPES, "STEAMER",
                                       (160, 200, 180), self._steamer_selected_recipe,
                                       self._steamer_recipe_rects,
                                       block_id=STEAMER_BLOCK)
            return
        if self.refinery_block_id == NOODLE_POT_BLOCK:
            self._draw_cooking_station(player, NOODLE_POT_RECIPES, "NOODLE POT",
                                       (180, 140, 80), self._noodle_pot_selected_recipe,
                                       self._noodle_pot_recipe_rects,
                                       block_id=NOODLE_POT_BLOCK)
            return
        if self.refinery_block_id == BBQ_GRILL_BLOCK:
            self._draw_cooking_station(player, BBQ_GRILL_RECIPES, "BBQ GRILL",
                                       (210, 90, 30), self._bbq_grill_selected_recipe,
                                       self._bbq_grill_recipe_rects,
                                       block_id=BBQ_GRILL_BLOCK)
            return
        if self.refinery_block_id == CLAY_POT_BLOCK:
            self._draw_cooking_station(player, CLAY_POT_RECIPES, "CLAY POT",
                                       (175, 110, 65), self._clay_pot_selected_recipe,
                                       self._clay_pot_recipe_rects,
                                       block_id=CLAY_POT_BLOCK)
            return
        if self.refinery_block_id == DESERT_FORGE_BLOCK:
            self._draw_cooking_station(player, FORGE_RECIPES, "DESERT FORGE",
                                       (175, 95, 40), self._desert_forge_selected_recipe,
                                       self._desert_forge_recipe_rects,
                                       block_id=DESERT_FORGE_BLOCK)
            return
        if self.refinery_block_id == ARTISAN_BENCH_BLOCK:
            self._draw_artisan_bench(player)
            return
        if self.refinery_block_id == BAIT_STATION_BLOCK:
            self._draw_cooking_station(player, BAIT_STATION_RECIPES, "BAIT STATION",
                                       (100, 70, 40), self._bait_station_selected_recipe,
                                       self._bait_station_recipe_rects,
                                       block_id=BAIT_STATION_BLOCK,
                                       action_label="CRAFT")
            return
        if self.refinery_block_id == FLETCHING_TABLE_BLOCK:
            self._draw_cooking_station(player, FLETCHING_RECIPES, "FLETCHING TABLE",
                                       (139, 110, 75), self._fletching_selected_recipe,
                                       self._fletching_recipe_rects,
                                       block_id=FLETCHING_TABLE_BLOCK,
                                       action_label="CRAFT")
            return
        if self.refinery_block_id == WEAPON_ASSEMBLER_BLOCK:
            self._draw_assembly_bench(player)
            return
        if self.refinery_block_id == SMELTER_BLOCK:
            self._draw_cooking_station(player, SMELTER_RECIPES, "SMELTER",
                                       (160, 80, 50), self._smelter_selected_recipe,
                                       self._smelter_recipe_rects,
                                       block_id=SMELTER_BLOCK,
                                       action_label="SMELT")
            return
        if self.refinery_block_id == ANAEROBIC_TANK_BLOCK:
            self._draw_anaerobic_tank(player, dt)
            return
        if self.refinery_block_id == GLASS_KILN_BLOCK:
            self._draw_cooking_station(player, GLASS_KILN_RECIPES, "GLASS KILN",
                                       (180, 220, 240), self._glass_kiln_selected_recipe,
                                       self._glass_kiln_recipe_rects,
                                       block_id=GLASS_KILN_BLOCK,
                                       action_label="SMELT")
            return
        if self.refinery_block_id == GARDEN_WORKSHOP_BLOCK:
            self._draw_cooking_station(player, GARDEN_WORKSHOP_RECIPES, "GARDEN WORKSHOP",
                                       (100, 155, 80), self._garden_workshop_selected_recipe,
                                       self._garden_workshop_recipe_rects,
                                       block_id=GARDEN_WORKSHOP_BLOCK,
                                       action_label="CRAFT", show_block_grid=True)
            return
        if self.refinery_block_id == JUICER_BLOCK:
            self._draw_cooking_station(player, JUICER_RECIPES, "JUICER",
                                       (220, 160, 60), self._juicer_selected_recipe,
                                       self._juicer_recipe_rects,
                                       block_id=JUICER_BLOCK,
                                       action_label="JUICE")
            return
        if self.refinery_block_id == AUTOMATION_BENCH_BLOCK:
            self._draw_cooking_station(player, AUTOMATION_RECIPES, "AUTOMATION BENCH",
                                       (70, 90, 110), self._automation_selected_recipe,
                                       self._automation_recipe_rects,
                                       block_id=AUTOMATION_BENCH_BLOCK,
                                       action_label="CRAFT")
            return
        if self.refinery_block_id == COMPOST_BIN_BLOCK:
            self._draw_compost_bin(player)
            return
        from blocks import CHICKEN_COOP_BLOCK
        if self.refinery_block_id == CHICKEN_COOP_BLOCK:
            self._draw_chicken_coop(player)
            return
        from blocks import FORGE_BLOCK, WEAPON_RACK_BLOCK
        if self.refinery_block_id == FORGE_BLOCK:
            self._draw_forge(player, dt)
            return
        if self.refinery_block_id == WEAPON_RACK_BLOCK:
            self._draw_weapon_rack(player)
            return
        from blocks import SCULPTORS_BENCH, TAPESTRY_FRAME_BLOCK
        if self.refinery_block_id == SCULPTORS_BENCH:
            self._draw_sculptor_bench(player, dt)
            return
        if self.refinery_block_id == TAPESTRY_FRAME_BLOCK:
            self._draw_tapestry_frame(player, dt)
            return
        from blocks import POTTERY_WHEEL_BLOCK, POTTERY_KILN_BLOCK, EVAPORATION_PAN_BLOCK, SALT_GRINDER_BLOCK
        if self.refinery_block_id == POTTERY_WHEEL_BLOCK:
            self._draw_pottery_wheel(player, dt)
            return
        if self.refinery_block_id == POTTERY_KILN_BLOCK:
            self._draw_pottery_kiln(player, dt)
            return
        if self.refinery_block_id == EVAPORATION_PAN_BLOCK:
            self._draw_evap_pan(player, dt)
            return
        if self.refinery_block_id == SALT_GRINDER_BLOCK:
            self._draw_salt_grinder(player, dt)
            return
        from blocks import PIGMENT_MILL_BLOCK
        if self.refinery_block_id == PIGMENT_MILL_BLOCK:
            self._draw_pigment_mill(player, dt)
            return
        from blocks import BEEHIVE_BLOCK as _BHB_DRAW
        if self.refinery_block_id == _BHB_DRAW:
            self._draw_beehive(player, dt)
            return
        from blocks import MEAD_VAT_BLOCK as _MVB, MEAD_CELLAR_BLOCK as _MCB
        if self.refinery_block_id == _MVB:
            self._draw_mead_vat(player, dt)
            return
        if self.refinery_block_id == _MCB:
            self._draw_mead_cellar(player, dt)
            return
        from blocks import SALTING_RACK_BLOCK as _SRB, CURING_CELLAR_BLOCK as _CCB
        if self.refinery_block_id == _SRB:
            self._draw_salting_rack(player, dt)
            return
        if self.refinery_block_id == _CCB:
            self._draw_curing_cellar(player, dt)
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
                from rocks import render_rock
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
    # Compost Bin panel
    # ------------------------------------------------------------------

    def _draw_compost_bin(self, player):
        import soil as _soil
        from item_icons import render_item_icon
        from items import ITEMS as _ITEMS
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        self.screen.blit(overlay, (0, 0))

        PW, PH = 480, 320
        px = (SCREEN_W - PW) // 2
        py = (SCREEN_H - PH) // 2
        pygame.draw.rect(self.screen, (50, 36, 20), (px, py, PW, PH))
        pygame.draw.rect(self.screen, (130, 90, 50), (px, py, PW, PH), 2)

        title = self.font.render("COMPOST BIN", True, (200, 160, 80))
        self.screen.blit(title, (px + PW // 2 - title.get_width() // 2, py + 8))

        hint = self.small.render(
            "Click an organic item in hotbar then [Deposit]  |  ESC to close",
            True, (130, 110, 70))
        self.screen.blit(hint, (px + PW // 2 - hint.get_width() // 2, py + 30))

        bin_pos = self.active_compost_bin_pos
        bin_data = (player.world.compost_bin_data.setdefault(
            bin_pos, {"input": {}, "progress": 0.0, "output": 0, "output_rich": 0})
            if bin_pos else {"input": {}, "progress": 0.0, "output": 0, "output_rich": 0})

        # --- Input inventory ---
        ix, iy = px + 16, py + 60
        input_label = self.small.render("Input (organic items):", True, (180, 155, 110))
        self.screen.blit(input_label, (ix, iy))
        iy += 18
        if bin_data["input"]:
            for item_id, count in list(bin_data["input"].items()):
                item_def = _ITEMS.get(item_id, {})
                icon = render_item_icon(item_id, item_def.get("color", (180, 180, 180)), 24)
                self.screen.blit(icon, (ix, iy))
                lbl = self.small.render(f"{item_def.get('name', item_id)} x{count}", True, (200, 190, 160))
                self.screen.blit(lbl, (ix + 28, iy + 4))
                iy += 28
        else:
            empty = self.small.render("(empty)", True, (100, 90, 70))
            self.screen.blit(empty, (ix, iy))
            iy += 20

        # --- Progress bar ---
        bar_y = py + 185
        progress = bin_data["progress"]
        total_items = sum(bin_data["input"].values())
        bar_w = PW - 32
        is_active = total_items >= _soil.COMPOST_INPUT_PER_OUTPUT
        filled = int(bar_w * progress / _soil.COMPOST_OUTPUT_THRESHOLD)
        pygame.draw.rect(self.screen, (40, 28, 14), (px + 16, bar_y, bar_w, 16))
        if filled > 0:
            bar_color = (100, 160, 60) if is_active else (80, 80, 60)
            pygame.draw.rect(self.screen, bar_color, (px + 16, bar_y, filled, 16))
        pygame.draw.rect(self.screen, (110, 85, 45), (px + 16, bar_y, bar_w, 16), 1)
        if is_active:
            prog_text = f"Composting: {int(progress)}/{int(_soil.COMPOST_OUTPUT_THRESHOLD)}"
            prog_color = (180, 200, 140)
        else:
            need = _soil.COMPOST_INPUT_PER_OUTPUT - total_items
            prog_text = f"Idle — deposit {need} more item{'s' if need != 1 else ''} to begin"
            prog_color = (160, 120, 80)
        prog_lbl = self.small.render(prog_text, True, prog_color)
        self.screen.blit(prog_lbl, (px + 16, bar_y - 18))

        # --- Output ---
        out_count = bin_data["output"]
        out_rich  = bin_data.get("output_rich", 0)
        out_lbl = self.font.render(f"Compost ready: {out_count}", True, (140, 200, 80) if out_count > 0 else (80, 80, 60))
        self.screen.blit(out_lbl, (px + 16, bar_y + 24))
        if out_rich > 0:
            rich_lbl = self.font.render(f"Rich Compost ready: {out_rich}", True, (180, 220, 80))
            self.screen.blit(rich_lbl, (px + 16, bar_y + 44))

        # --- Buttons ---
        btn_y = py + PH - 48
        deposit_enabled = False
        sel = player.hotbar[player.selected_slot]
        if sel and _ITEMS.get(sel, {}).get("fertilize_tool") is None:
            if sel in _soil.ORGANIC_ITEM_IDS and player.inventory.get(sel, 0) > 0:
                deposit_enabled = True

        dep_col = (40, 90, 40) if deposit_enabled else (28, 28, 36)
        dep_bdr = (80, 180, 80) if deposit_enabled else (55, 55, 68)
        self._compost_deposit_btn = pygame.Rect(px + 16, btn_y, 140, 32)
        pygame.draw.rect(self.screen, dep_col, self._compost_deposit_btn)
        pygame.draw.rect(self.screen, dep_bdr, self._compost_deposit_btn, 2)
        dep_txt = self.font.render("Deposit", True, (200, 240, 200) if deposit_enabled else (70, 70, 82))
        self.screen.blit(dep_txt, (self._compost_deposit_btn.centerx - dep_txt.get_width() // 2,
                                   self._compost_deposit_btn.centery - dep_txt.get_height() // 2))

        collect_any = out_count > 0 or out_rich > 0
        col_col = (40, 90, 40) if collect_any else (28, 28, 36)
        col_bdr = (80, 180, 80) if collect_any else (55, 55, 68)
        self._compost_collect_btn = pygame.Rect(px + 168, btn_y, 140, 32)
        pygame.draw.rect(self.screen, col_col, self._compost_collect_btn)
        pygame.draw.rect(self.screen, col_bdr, self._compost_collect_btn, 2)
        col_txt = self.font.render("Collect", True, (200, 240, 200) if collect_any else (70, 70, 82))
        self.screen.blit(col_txt, (self._compost_collect_btn.centerx - col_txt.get_width() // 2,
                                   self._compost_collect_btn.centery - col_txt.get_height() // 2))

    def _draw_chicken_coop(self, player):
        from animals import Chicken as _Chicken
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        self.screen.blit(overlay, (0, 0))

        PW, PH = 400, 260
        px = (SCREEN_W - PW) // 2
        py = (SCREEN_H - PH) // 2
        pygame.draw.rect(self.screen, (48, 34, 18), (px, py, PW, PH))
        pygame.draw.rect(self.screen, (165, 125, 60), (px, py, PW, PH), 2)

        title = self.font.render("CHICKEN COOP", True, (220, 185, 90))
        self.screen.blit(title, (px + PW // 2 - title.get_width() // 2, py + 8))

        # Count contributing hens
        hens = [e for e in player.world.entities
                if isinstance(e, _Chicken) and not e.dead
                and e.traits.get("sex") == "female"]
        hen_lbl = self.small.render(
            f"Contributing hens: {len(hens)}" if hens else "No hens found — tame female chickens to fill this coop",
            True, (180, 160, 100) if hens else (160, 90, 60))
        self.screen.blit(hen_lbl, (px + 16, py + 34))

        coop_pos = self.active_coop_pos
        coop_data = (player.world.chicken_coop_data.setdefault(
            coop_pos, {"eggs": 0, "progress": 0.0})
            if coop_pos else {"eggs": 0, "progress": 0.0})

        # Progress bar (toward next egg)
        bar_y = py + 80
        bar_w = PW - 32
        progress = coop_data["progress"]
        filled = int(bar_w * min(progress, 1.0))
        pygame.draw.rect(self.screen, (36, 24, 12), (px + 16, bar_y, bar_w, 14))
        if filled > 0 and hens:
            pygame.draw.rect(self.screen, (200, 170, 60), (px + 16, bar_y, filled, 14))
        pygame.draw.rect(self.screen, (120, 90, 40), (px + 16, bar_y, bar_w, 14), 1)
        bar_lbl = self.small.render("Next egg progress", True, (150, 130, 80))
        self.screen.blit(bar_lbl, (px + 16, bar_y - 16))

        # Egg count display
        egg_count = coop_data["eggs"]
        egg_color = (230, 200, 80) if egg_count > 0 else (80, 70, 50)
        egg_lbl = self.font.render(f"Eggs ready: {egg_count} / {player.world._COOP_MAX_EGGS}", True, egg_color)
        self.screen.blit(egg_lbl, (px + 16, bar_y + 26))

        hint = self.small.render("ESC to close", True, (100, 90, 60))
        self.screen.blit(hint, (px + PW // 2 - hint.get_width() // 2, py + PH - 22))

        # Collect button
        btn_y = py + PH - 52
        can_collect = egg_count > 0
        btn_col = (50, 100, 40) if can_collect else (28, 28, 36)
        btn_bdr = (100, 200, 80) if can_collect else (55, 55, 68)
        self._coop_collect_btn = pygame.Rect(px + PW // 2 - 70, btn_y, 140, 32)
        pygame.draw.rect(self.screen, btn_col, self._coop_collect_btn)
        pygame.draw.rect(self.screen, btn_bdr, self._coop_collect_btn, 2)
        btn_txt = self.font.render("Collect Eggs", True, (200, 240, 180) if can_collect else (70, 70, 82))
        self.screen.blit(btn_txt, (self._coop_collect_btn.centerx - btn_txt.get_width() // 2,
                                   self._coop_collect_btn.centery - btn_txt.get_height() // 2))
