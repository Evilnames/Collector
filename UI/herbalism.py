import pygame
from constants import SCREEN_W, SCREEN_H
from herbalism import (
    match_recipe, get_dried_item, can_press_flower, recipe_requires_research,
    DRYING_TABLE, DRYABLE_ITEMS, RECIPES, RECIPE_ORDER,
    POTION_DESCS, POTION_COLORS, TIER_LABELS, BUFF_DESCS,
    INGREDIENT_DISPLAY_NAMES, ALL_POTION_IDS,
    DRYING_RACK_SLOTS, DRY_DURATION_DAYS,
    match_mortar_recipe, MORTAR_RECIPES, MORTAR_COLORS, MORTAR_INGREDIENT_KEYS,
)
from world import CYCLE_DURATION

_ACCENT   = ( 70, 175, 140)
_DARK_BG  = ( 10,  28,  24)
_CELL_BG  = ( 15,  40,  32)
_TITLE_C  = (140, 235, 200)
_LABEL_C  = ( 90, 185, 145)
_DIM_C    = ( 40,  90,  72)
_HINT_C   = ( 70, 140, 110)

_TIER_COLORS = {
    "basic":  ( 90, 185, 145),
    "fine":   (160, 220, 180),
    "elixir": (220, 240, 255),
}


class HerbalismMixin:

    # ─────────────────────────────────────────────────────────────────────────
    # DRYING RACK
    # ─────────────────────────────────────────────────────────────────────────

    def _draw_drying_rack(self, player, dt=0.0):
        from items import ITEMS
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("DRYING RACK", True, _TITLE_C)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, _HINT_C)
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        slots = player.drying_rack_slots
        SLOT_W, SLOT_H = 130, 72
        GAP = 10
        total_w = DRYING_RACK_SLOTS * SLOT_W + (DRYING_RACK_SLOTS - 1) * GAP
        sx0 = (SCREEN_W - total_w) // 2
        sy0 = 34

        # ── Drying slots row ──────────────────────────────────────────────
        self._drying_slot_rects.clear()
        for i in range(DRYING_RACK_SLOTS):
            sx = sx0 + i * (SLOT_W + GAP)
            rect = pygame.Rect(sx, sy0, SLOT_W, SLOT_H)
            self._drying_slot_rects[i] = rect

            slot = slots[i] if i < len(slots) else None
            if slot is None:
                pygame.draw.rect(self.screen, _DARK_BG, rect)
                pygame.draw.rect(self.screen, _DIM_C, rect, 1)
                empty_s = self.small.render("Empty", True, _DIM_C)
                self.screen.blit(empty_s, (rect.centerx - empty_s.get_width() // 2,
                                           rect.centery - empty_s.get_height() // 2))
            else:
                done = slot["elapsed"] >= slot["duration"]
                bg   = (15, 50, 35) if not done else (10, 55, 20)
                brd  = (120, 220, 80) if done else _ACCENT
                pygame.draw.rect(self.screen, bg, rect)
                pygame.draw.rect(self.screen, brd, rect, 2 if done else 1)

                src_name = ITEMS.get(slot["src_key"], {}).get("name", slot["src_key"])
                out_name = ITEMS.get(slot["out_key"], {}).get("name", slot["out_key"])
                ns = self.small.render(src_name[:16], True, _TITLE_C)
                self.screen.blit(ns, (rect.x + 5, rect.y + 5))
                os2 = self.small.render(f"→ {out_name[:14]}", True, _LABEL_C)
                self.screen.blit(os2, (rect.x + 5, rect.y + 20))

                if done:
                    ready_s = self.font.render("READY", True, (120, 255, 90))
                    self.screen.blit(ready_s, (rect.centerx - ready_s.get_width() // 2,
                                               rect.y + 42))
                else:
                    # progress bar
                    frac = slot["elapsed"] / slot["duration"]
                    bar_x, bar_y = rect.x + 5, rect.y + 52
                    bar_w = SLOT_W - 10
                    pygame.draw.rect(self.screen, (20, 50, 35), (bar_x, bar_y, bar_w, 8))
                    pygame.draw.rect(self.screen, _ACCENT, (bar_x, bar_y, int(bar_w * frac), 8))
                    days_left = (slot["duration"] - slot["elapsed"]) / CYCLE_DURATION
                    time_s = self.small.render(f"{days_left:.1f}d", True, _HINT_C)
                    self.screen.blit(time_s, (rect.x + 5, rect.y + 42))

        bottom_y = sy0 + SLOT_H + 14
        split_x  = SCREEN_W // 2 - 10
        inv_w    = split_x - 8
        fl_w     = SCREEN_W - split_x - 18

        # ── Left bottom: inventory herbs to place ─────────────────────────
        pygame.draw.rect(self.screen, _DARK_BG, (8, bottom_y, inv_w, SCREEN_H - bottom_y - 8))
        pygame.draw.rect(self.screen, _DIM_C,   (8, bottom_y, inv_w, SCREEN_H - bottom_y - 8), 1)
        hdr = self.small.render("PLACE TO DRY  (click herb → fills next empty slot)", True, _LABEL_C)
        self.screen.blit(hdr, (16, bottom_y + 5))

        free_slots = sum(1 for i in range(DRYING_RACK_SLOTS)
                         if i >= len(slots) or slots[i] is None)
        avail_s = self.small.render(f"Free slots: {free_slots}/{DRYING_RACK_SLOTS}", True, _HINT_C)
        self.screen.blit(avail_s, (inv_w - avail_s.get_width() + 8, bottom_y + 5))

        self._drying_inv_rects.clear()
        ry = bottom_y + 24
        for src_key in DRYABLE_ITEMS:
            count = player.inventory.get(src_key, 0)
            if count <= 0:
                continue
            out_key  = DRYING_TABLE[src_key]
            src_name = ITEMS.get(src_key, {}).get("name", src_key)
            out_name = ITEMS.get(out_key, {}).get("name", out_key)
            btn = pygame.Rect(16, ry, inv_w - 16, 38)
            if ry + 38 > SCREEN_H - 10:
                break
            active = free_slots > 0
            self._drying_inv_rects[src_key] = btn
            pygame.draw.rect(self.screen, _CELL_BG if active else (10, 22, 18), btn)
            pygame.draw.rect(self.screen, _ACCENT if active else _DIM_C, btn, 1)
            top_s = self.small.render(f"{src_name}  ×{count}", True, _TITLE_C if active else _DIM_C)
            self.screen.blit(top_s, (btn.x + 6, btn.y + 3))
            bot_s = self.small.render(f"→ {out_name}", True, _LABEL_C if active else _DIM_C)
            self.screen.blit(bot_s, (btn.x + 6, btn.y + 19))
            ry += 44

        if not self._drying_inv_rects:
            msg = self.small.render("No dryable herbs in inventory.", True, _DIM_C)
            self.screen.blit(msg, (16, bottom_y + 30))

        # ── Right bottom: press wildflowers ──────────────────────────────
        rx0 = split_x + 10
        pygame.draw.rect(self.screen, _DARK_BG, (rx0, bottom_y, fl_w, SCREEN_H - bottom_y - 8))
        pygame.draw.rect(self.screen, _DIM_C,   (rx0, bottom_y, fl_w, SCREEN_H - bottom_y - 8), 1)
        hdr2 = self.small.render("PRESS WILDFLOWERS", True, _LABEL_C)
        self.screen.blit(hdr2, (rx0 + 8, bottom_y + 5))

        common_fl = [wf for wf in player.wildflowers if wf.rarity in ("common", "uncommon")]
        rare_fl   = [wf for wf in player.wildflowers if wf.rarity in ("rare", "epic", "legendary")]

        self._dry_flower_btns.clear()
        btn_y = bottom_y + 24
        for label, pool, out_key in [
            ("Press Common  ×" + str(len(common_fl)), common_fl, "pressed_flower"),
            ("Press Rare    ×" + str(len(rare_fl)),   rare_fl,   "pressed_rare_flower"),
        ]:
            btn_rect = pygame.Rect(rx0 + 8, btn_y, fl_w - 16, 46)
            active   = len(pool) > 0
            self._dry_flower_btns[out_key] = (btn_rect, pool)
            pygame.draw.rect(self.screen, _CELL_BG if active else (10, 22, 18), btn_rect)
            pygame.draw.rect(self.screen, _ACCENT if active else _DIM_C, btn_rect, 2 if active else 1)
            out_name = ITEMS.get(out_key, {}).get("name", out_key)
            ts = self.small.render(label, True, _TITLE_C if active else _DIM_C)
            self.screen.blit(ts, (btn_rect.x + 6, btn_rect.y + 5))
            bs = self.small.render(f"→ {out_name}", True, _LABEL_C if active else _DIM_C)
            self.screen.blit(bs, (btn_rect.x + 6, btn_rect.y + 24))
            btn_y += 56

        note = self.small.render("Pressing is instant. Consumes 1 wildflower.", True, _HINT_C)
        self.screen.blit(note, (rx0 + 8, btn_y + 6))

    def _handle_drying_rack_click(self, pos, player):
        from herbalism import DRYING_RACK_SLOTS, DRY_DURATION_DAYS
        slots = player.drying_rack_slots

        # Collect from ready slots
        for i, rect in self._drying_slot_rects.items():
            if rect.collidepoint(pos):
                if i < len(slots) and slots[i] is not None:
                    slot = slots[i]
                    if slot["elapsed"] >= slot["duration"]:
                        player._add_item(slot["out_key"])
                        slots[i] = None
                        # Trim trailing Nones
                        while slots and slots[-1] is None:
                            slots.pop()
                return

        # Place herb in next free slot
        for src_key, rect in self._drying_inv_rects.items():
            if rect.collidepoint(pos):
                if player.inventory.get(src_key, 0) <= 0:
                    return
                # Find first free slot index
                free_idx = None
                for i in range(DRYING_RACK_SLOTS):
                    val = slots[i] if i < len(slots) else None
                    if val is None:
                        free_idx = i
                        break
                if free_idx is None:
                    return  # all slots full
                # Extend list if needed
                while len(slots) <= free_idx:
                    slots.append(None)
                player.inventory[src_key] -= 1
                if player.inventory[src_key] <= 0:
                    del player.inventory[src_key]
                slots[free_idx] = {
                    "src_key":  src_key,
                    "out_key":  DRYING_TABLE[src_key],
                    "elapsed":  0.0,
                    "duration": DRY_DURATION_DAYS * CYCLE_DURATION,
                }
                return

        # Press wildflowers (instant)
        for out_key, (btn_rect, pool) in self._dry_flower_btns.items():
            if btn_rect.collidepoint(pos) and pool:
                player.wildflowers.remove(pool[0])
                player._add_item(out_key)
                return

    # ─────────────────────────────────────────────────────────────────────────
    # ALCHEMICAL KILN
    # ─────────────────────────────────────────────────────────────────────────

    def _draw_kiln(self, player, dt=0.0, research=None):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("ALCHEMICAL KILN", True, (220, 140, 80))
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, (140, 100, 50))
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        # Check research
        if research is not None and not (
            research.nodes.get("tincture_crafting") and
            research.nodes["tincture_crafting"].unlocked
        ):
            lock_msg = self.font.render("Requires: Tincture Crafting research", True, (180, 80, 40))
            self.screen.blit(lock_msg, (SCREEN_W // 2 - lock_msg.get_width() // 2, SCREEN_H // 2))
            return

        self._draw_station_ui(player, self._kiln_slots, self._kiln_slot_rects,
                              "_kiln_active_slot", self._kiln_inv_rects,
                              self._kiln_inv_scroll, "kiln", research,
                              brew_btn_attr="_kiln_brew_btn",
                              result_attr="_kiln_result",
                              result_btn_attr="_kiln_result_btn",
                              station_color=(200, 120, 40))

    def _handle_kiln_click(self, pos, player, research=None):
        self._handle_station_click(pos, player, self._kiln_slots, self._kiln_slot_rects,
                                   "_kiln_active_slot", self._kiln_inv_rects,
                                   "_kiln_brew_btn", "_kiln_result",
                                   "_kiln_result_btn", "kiln", research)

    # ─────────────────────────────────────────────────────────────────────────
    # RESONANCE CHAMBER
    # ─────────────────────────────────────────────────────────────────────────

    def _draw_resonance_chamber(self, player, dt=0.0, research=None):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("RESONANCE CHAMBER", True, (160, 120, 255))
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, (100, 75, 180))
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        if research is not None and not (
            research.nodes.get("resonance_mastery") and
            research.nodes["resonance_mastery"].unlocked
        ):
            lock_msg = self.font.render("Requires: Resonance Mastery research", True, (130, 80, 220))
            self.screen.blit(lock_msg, (SCREEN_W // 2 - lock_msg.get_width() // 2, SCREEN_H // 2))
            return

        self._draw_station_ui(player, self._res_slots, self._res_slot_rects,
                              "_res_active_slot", self._res_inv_rects,
                              self._res_inv_scroll, "resonance", research,
                              brew_btn_attr="_res_brew_btn",
                              result_attr="_res_result",
                              result_btn_attr="_res_result_btn",
                              station_color=(130, 90, 240))

    def _handle_resonance_click(self, pos, player, research=None):
        self._handle_station_click(pos, player, self._res_slots, self._res_slot_rects,
                                   "_res_active_slot", self._res_inv_rects,
                                   "_res_brew_btn", "_res_result",
                                   "_res_result_btn", "resonance", research)

    # ─────────────────────────────────────────────────────────────────────────
    # Shared station draw + click (used by both kiln and resonance)
    # ─────────────────────────────────────────────────────────────────────────

    def _draw_station_ui(self, player, slots, slot_rects, active_slot_attr,
                         inv_rects, inv_scroll, station, research,
                         brew_btn_attr, result_attr, result_btn_attr,
                         station_color):
        result = getattr(self, result_attr, None)

        if result is not None:
            self._draw_brew_result(player, result, result_btn_attr, station_color)
            return

        n_slots = len(slots)
        SLOT_W, SLOT_H, SLOT_GAP = 110, 90, 10
        total_slot_w = n_slots * SLOT_W + (n_slots - 1) * SLOT_GAP
        sx0 = (SCREEN_W - total_slot_w) // 2
        sy0 = 40

        # Draw ingredient slots
        del slot_rects[:]
        active_idx = getattr(self, active_slot_attr, None)
        for i, slot in enumerate(slots):
            sx = sx0 + i * (SLOT_W + SLOT_GAP)
            rect = pygame.Rect(sx, sy0, SLOT_W, SLOT_H)
            slot_rects.append(rect)
            is_active = (active_idx == i)
            bg  = (25, 45, 35) if not is_active else (35, 60, 48)
            brd = station_color if is_active else _DIM_C
            pygame.draw.rect(self.screen, bg, rect)
            pygame.draw.rect(self.screen, brd, rect, 3 if is_active else 1)

            if slot:
                item_key, count = slot.get("key"), slot.get("count", 1)
                from items import ITEMS
                item_name = ITEMS.get(item_key, {}).get("name", item_key)
                item_col  = ITEMS.get(item_key, {}).get("color", (180, 180, 180))
                ns = self.small.render(item_name[:14], True, item_col)
                self.screen.blit(ns, (sx + 6, sy0 + 8))
                cnt_s = self.font.render(f"×{count}", True, _TITLE_C)
                self.screen.blit(cnt_s, (sx + 6, sy0 + 36))
                # – button to reduce count
                minus_rect = pygame.Rect(sx + SLOT_W - 26, sy0 + 6, 20, 20)
                pygame.draw.rect(self.screen, (50, 20, 10), minus_rect)
                pygame.draw.rect(self.screen, (180, 80, 40), minus_rect, 1)
                ms = self.small.render("–", True, (220, 140, 80))
                self.screen.blit(ms, (minus_rect.centerx - ms.get_width() // 2,
                                      minus_rect.centery - ms.get_height() // 2))
                # + button to increase count
                plus_rect = pygame.Rect(sx + SLOT_W - 26, sy0 + 30, 20, 20)
                pygame.draw.rect(self.screen, (20, 50, 30), plus_rect)
                pygame.draw.rect(self.screen, (80, 180, 130), plus_rect, 1)
                ps = self.small.render("+", True, (140, 220, 160))
                self.screen.blit(ps, (plus_rect.centerx - ps.get_width() // 2,
                                      plus_rect.centery - ps.get_height() // 2))
            else:
                empty_s = self.small.render(f"Slot {i+1}", True, _DIM_C)
                self.screen.blit(empty_s, (sx + SLOT_W // 2 - empty_s.get_width() // 2,
                                            sy0 + SLOT_H // 2 - empty_s.get_height() // 2))
                if is_active:
                    pick_s = self.small.render("← pick item below", True, _LABEL_C)
                    self.screen.blit(pick_s, (sx + 4, sy0 + SLOT_H - 18))

        # Recipe match hint
        slot_dict = {s["key"]: s["count"] for s in slots if s and s.get("key")}
        matched = match_recipe(slot_dict, station)
        hint_y = sy0 + SLOT_H + 14
        if matched:
            from items import ITEMS
            m_name = ITEMS.get(matched, {}).get("name", matched)
            m_col  = POTION_COLORS.get(matched, _TITLE_C)
            match_s = self.font.render(f"✓  {m_name}", True, m_col)
            self.screen.blit(match_s, (SCREEN_W // 2 - match_s.get_width() // 2, hint_y))
        elif slot_dict:
            no_s = self.small.render("No matching recipe — will produce Mystery Flask", True, (160, 110, 60))
            self.screen.blit(no_s, (SCREEN_W // 2 - no_s.get_width() // 2, hint_y))

        # BREW button
        brew_rect = pygame.Rect(SCREEN_W // 2 - 80, hint_y + 28, 160, 36)
        has_items = bool(slot_dict)
        bc = (40, 90, 55) if has_items else (20, 45, 30)
        pygame.draw.rect(self.screen, bc, brew_rect)
        pygame.draw.rect(self.screen, _ACCENT if has_items else _DIM_C, brew_rect, 2)
        bl = self.font.render("BREW", True, _TITLE_C if has_items else _DIM_C)
        self.screen.blit(bl, (brew_rect.centerx - bl.get_width() // 2,
                               brew_rect.centery - bl.get_height() // 2))
        setattr(self, brew_btn_attr, brew_rect)

        # Inventory grid (ingredient picker)
        inv_y0 = hint_y + 76
        sub = self.small.render("Ingredients in inventory — click to add to selected slot:", True, _HINT_C)
        self.screen.blit(sub, (8, inv_y0))
        inv_y0 += 18

        HERB_KEYS = list(INGREDIENT_DISPLAY_NAMES.keys())
        inv_rects.clear()
        CELL_W, CELL_H, GAP, COLS = 180, 44, 6, 6
        gx0 = (SCREEN_W - (COLS * CELL_W + (COLS - 1) * GAP)) // 2
        col_i = 0
        row_i = 0
        for ikey in HERB_KEYS:
            count = player.inventory.get(ikey, 0)
            if count <= 0:
                continue
            cx = gx0 + col_i * (CELL_W + GAP)
            cy = inv_y0 + row_i * (CELL_H + GAP)
            if cy + CELL_H > SCREEN_H - 8:
                break
            rect = pygame.Rect(cx, cy, CELL_W, CELL_H)
            inv_rects[ikey] = rect
            from items import ITEMS
            item_col = ITEMS.get(ikey, {}).get("color", (160, 160, 160))
            pygame.draw.rect(self.screen, _CELL_BG, rect)
            pygame.draw.rect(self.screen, item_col, rect, 1)
            disp = INGREDIENT_DISPLAY_NAMES.get(ikey, ikey)
            ns = self.small.render(f"{disp}  ×{count}", True, item_col)
            self.screen.blit(ns, (cx + 6, cy + (CELL_H - ns.get_height()) // 2))
            col_i += 1
            if col_i >= COLS:
                col_i = 0
                row_i += 1

        # Known recipes panel (right side)
        self._draw_recipe_hints(player, station, research)

    def _draw_recipe_hints(self, player, station, research):
        rx0 = SCREEN_W - 260
        ry0 = 40
        rh  = SCREEN_H - 60
        pygame.draw.rect(self.screen, _DARK_BG, (rx0, ry0, 250, rh))
        pygame.draw.rect(self.screen, _DIM_C,   (rx0, ry0, 250, rh), 1)
        hdr = self.small.render("RECIPES", True, _LABEL_C)
        self.screen.blit(hdr, (rx0 + 8, ry0 + 4))
        iy = ry0 + 22
        for out_id, recipe in RECIPES.items():
            if recipe["station"] != station:
                continue
            if iy + 36 > ry0 + rh - 4:
                break
            disc = out_id in player.discovered_recipes
            tier_col = _TIER_COLORS.get(recipe["tier"], _LABEL_C)
            from items import ITEMS
            out_name = ITEMS.get(out_id, {}).get("name", out_id)
            if disc:
                ns = self.small.render(out_name, True, tier_col)
                self.screen.blit(ns, (rx0 + 8, iy))
                # ingredient list
                iy += 14
                for ing_key, ing_cnt in recipe["ingredients"].items():
                    ing_name = INGREDIENT_DISPLAY_NAMES.get(ing_key, ing_key)
                    is2 = self.small.render(f"  {ing_name} ×{ing_cnt}", True, _HINT_C)
                    self.screen.blit(is2, (rx0 + 8, iy))
                    iy += 12
                iy += 4
            else:
                qs = self.small.render("??? (undiscovered)", True, _DIM_C)
                self.screen.blit(qs, (rx0 + 8, iy))
                iy += 18

    def _draw_brew_result(self, player, out_id, result_btn_attr, station_color):
        from items import ITEMS
        cx, cy = SCREEN_W // 2, 80
        p_col   = POTION_COLORS.get(out_id, _ACCENT)
        pygame.draw.circle(self.screen, p_col, (cx, cy + 36), 36)
        pygame.draw.circle(self.screen,
                           (min(255, p_col[0]+50), min(255, p_col[1]+50), min(255, p_col[2]+50)),
                           (cx, cy + 36), 36, 3)

        out_name = ITEMS.get(out_id, {}).get("name", out_id)
        iy = cy + 86

        def rline(txt, col=_TITLE_C):
            nonlocal iy
            s = self.font.render(txt, True, col)
            self.screen.blit(s, (cx - s.get_width() // 2, iy))
            iy += 28

        rline(out_name, p_col)
        rline(POTION_DESCS.get(out_id, "Unknown effect"), _LABEL_C)
        recipe = RECIPES.get(out_id)
        if recipe:
            rline(f"[{TIER_LABELS.get(recipe['tier'], recipe['tier'])}]", _TIER_COLORS.get(recipe["tier"], _LABEL_C))
        if out_id == "mystery_flask":
            rline("Drink to identify", (180, 160, 120))

        done_rect = pygame.Rect(cx - 70, iy + 16, 140, 34)
        pygame.draw.rect(self.screen, _DARK_BG, done_rect)
        pygame.draw.rect(self.screen, _ACCENT, done_rect, 2)
        dl = self.font.render("DONE", True, _TITLE_C)
        self.screen.blit(dl, (done_rect.centerx - dl.get_width() // 2,
                               done_rect.centery - dl.get_height() // 2))
        setattr(self, result_btn_attr, done_rect)

    def _handle_station_click(self, pos, player, slots, slot_rects, active_slot_attr,
                               inv_rects, brew_btn_attr, result_attr, result_btn_attr,
                               station, research):
        result = getattr(self, result_attr, None)
        if result is not None:
            done_btn = getattr(self, result_btn_attr, None)
            if done_btn and done_btn.collidepoint(pos):
                setattr(self, result_attr, None)
                # Clear all slots
                for i in range(len(slots)):
                    slots[i] = {}
                setattr(self, active_slot_attr, None)
            return

        # Slot clicks
        for i, rect in enumerate(slot_rects):
            if rect.collidepoint(pos):
                setattr(self, active_slot_attr, i)
                return

        # – / + buttons inside filled slots
        SLOT_W, SLOT_H, SLOT_GAP = 110, 90, 10
        n_slots = len(slots)
        total_slot_w = n_slots * SLOT_W + (n_slots - 1) * SLOT_GAP
        sx0 = (SCREEN_W - total_slot_w) // 2
        sy0 = 40
        for i, slot in enumerate(slots):
            if not slot:
                continue
            sx = sx0 + i * (SLOT_W + SLOT_GAP)
            minus_rect = pygame.Rect(sx + SLOT_W - 26, sy0 + 6, 20, 20)
            plus_rect  = pygame.Rect(sx + SLOT_W - 26, sy0 + 30, 20, 20)
            if minus_rect.collidepoint(pos):
                slot["count"] = max(1, slot["count"] - 1)
                return
            if plus_rect.collidepoint(pos):
                have = player.inventory.get(slot["key"], 0)
                if slot["count"] < have:
                    slot["count"] += 1
                return

        # Brew button
        brew_btn = getattr(self, brew_btn_attr, None)
        if brew_btn and brew_btn.collidepoint(pos):
            slot_dict = {s["key"]: s["count"] for s in slots if s and s.get("key")}
            if not slot_dict:
                return
            # Check player has enough of each ingredient
            for ing_key, ing_cnt in slot_dict.items():
                if player.inventory.get(ing_key, 0) < ing_cnt:
                    return
            # Deduct ingredients
            for ing_key, ing_cnt in slot_dict.items():
                player.inventory[ing_key] -= ing_cnt
                if player.inventory[ing_key] <= 0:
                    del player.inventory[ing_key]
            # Match recipe — produce potion if match+research unlocked, else mystery_flask
            matched_id = match_recipe(slot_dict, station)
            if matched_id and recipe_requires_research(matched_id, research):
                out_id = matched_id
            else:
                out_id = "mystery_flask"
            player._add_item(out_id)
            player.discovered_recipes.add(out_id)
            setattr(self, result_attr, out_id)
            return

        # Inventory ingredient picker
        active_idx = getattr(self, active_slot_attr, None)
        if active_idx is not None:
            for ikey, rect in inv_rects.items():
                if rect.collidepoint(pos):
                    # Assign to active slot
                    slots[active_idx] = {"key": ikey, "count": 1}
                    setattr(self, active_slot_attr, None)
                    return

    # ─────────────────────────────────────────────────────────────────────────
    # MORTAR & PESTLE
    # ─────────────────────────────────────────────────────────────────────────

    _MC = (145, 135, 120)  # mortar stone colour

    def _draw_mortar(self, player, dt=0.0):
        from items import ITEMS
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("MORTAR & PESTLE", True, (200, 190, 170))
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close  |  No research required", True, (120, 110, 95))
        self.screen.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, 26))

        SLOT_W, SLOT_H, SLOT_GAP = 110, 90, 10
        total_slot_w = 2 * SLOT_W + SLOT_GAP
        sx0 = (SCREEN_W - total_slot_w) // 2
        sy0 = 50

        self._mortar_slot_rects.clear()
        active_idx = self._mortar_active_slot
        for i, slot in enumerate(self._mortar_slots):
            sx = sx0 + i * (SLOT_W + SLOT_GAP)
            rect = pygame.Rect(sx, sy0, SLOT_W, SLOT_H)
            self._mortar_slot_rects.append(rect)
            is_active = (active_idx == i)
            pygame.draw.rect(self.screen, (25, 23, 20) if not is_active else (40, 35, 28), rect)
            pygame.draw.rect(self.screen, self._MC if is_active else (60, 55, 50), rect, 3 if is_active else 1)
            if slot:
                item_key, count = slot.get("key"), slot.get("count", 1)
                item_name = ITEMS.get(item_key, {}).get("name", item_key)
                item_col  = ITEMS.get(item_key, {}).get("color", (180, 180, 180))
                ns = self.small.render(item_name[:14], True, item_col)
                self.screen.blit(ns, (sx + 6, sy0 + 8))
                cnt_s = self.font.render(f"×{count}", True, (220, 210, 195))
                self.screen.blit(cnt_s, (sx + 6, sy0 + 36))
                minus_rect = pygame.Rect(sx + SLOT_W - 26, sy0 + 6, 20, 20)
                plus_rect  = pygame.Rect(sx + SLOT_W - 26, sy0 + 30, 20, 20)
                pygame.draw.rect(self.screen, (50, 30, 20), minus_rect)
                pygame.draw.rect(self.screen, (160, 80, 40), minus_rect, 1)
                ms = self.small.render("–", True, (220, 140, 80))
                self.screen.blit(ms, (minus_rect.centerx - ms.get_width() // 2,
                                      minus_rect.centery - ms.get_height() // 2))
                pygame.draw.rect(self.screen, (20, 40, 25), plus_rect)
                pygame.draw.rect(self.screen, (80, 160, 100), plus_rect, 1)
                ps = self.small.render("+", True, (120, 200, 140))
                self.screen.blit(ps, (plus_rect.centerx - ps.get_width() // 2,
                                      plus_rect.centery - ps.get_height() // 2))
            else:
                empty_s = self.small.render(f"Slot {i + 1}", True, (60, 55, 50))
                self.screen.blit(empty_s, (sx + SLOT_W // 2 - empty_s.get_width() // 2,
                                            sy0 + SLOT_H // 2 - empty_s.get_height() // 2))
                if is_active:
                    pick_s = self.small.render("← pick herb below", True, (110, 100, 85))
                    self.screen.blit(pick_s, (sx + 4, sy0 + SLOT_H - 18))

        slot_dict = {s["key"]: s["count"] for s in self._mortar_slots if s and s.get("key")}
        matched = match_mortar_recipe(slot_dict)
        hint_y = sy0 + SLOT_H + 14
        if matched:
            m_name = ITEMS.get(matched, {}).get("name", matched)
            m_col  = MORTAR_COLORS.get(matched, (200, 190, 170))
            match_s = self.font.render(f"✓  {m_name}", True, m_col)
            self.screen.blit(match_s, (SCREEN_W // 2 - match_s.get_width() // 2, hint_y))
        elif slot_dict:
            no_s = self.small.render("No matching recipe", True, (140, 100, 60))
            self.screen.blit(no_s, (SCREEN_W // 2 - no_s.get_width() // 2, hint_y))

        grind_rect = pygame.Rect(SCREEN_W // 2 - 80, hint_y + 28, 160, 36)
        has_items = bool(slot_dict) and matched is not None
        bc = (40, 35, 25) if has_items else (20, 18, 14)
        pygame.draw.rect(self.screen, bc, grind_rect)
        pygame.draw.rect(self.screen, self._MC if has_items else (55, 50, 45), grind_rect, 2)
        gl = self.font.render("GRIND", True, (200, 190, 170) if has_items else (60, 55, 50))
        self.screen.blit(gl, (grind_rect.centerx - gl.get_width() // 2,
                               grind_rect.centery - gl.get_height() // 2))
        self._mortar_grind_btn = grind_rect

        inv_y0 = hint_y + 76
        sub = self.small.render("Herbs in inventory — click to add to selected slot:", True, (90, 85, 75))
        self.screen.blit(sub, (8, inv_y0))
        inv_y0 += 18
        self._mortar_inv_rects.clear()
        CELL_W, CELL_H, GAP, COLS = 180, 44, 6, 6
        gx0 = (SCREEN_W - (COLS * CELL_W + (COLS - 1) * GAP)) // 2
        col_i = row_i = 0
        for ikey in sorted(MORTAR_INGREDIENT_KEYS):
            count = player.inventory.get(ikey, 0)
            if count <= 0:
                continue
            cx = gx0 + col_i * (CELL_W + GAP)
            cy = inv_y0 + row_i * (CELL_H + GAP)
            if cy + CELL_H > SCREEN_H - 8:
                break
            rect = pygame.Rect(cx, cy, CELL_W, CELL_H)
            self._mortar_inv_rects[ikey] = rect
            item_col = ITEMS.get(ikey, {}).get("color", (160, 160, 160))
            pygame.draw.rect(self.screen, (15, 14, 12), rect)
            pygame.draw.rect(self.screen, item_col, rect, 1)
            disp = ITEMS.get(ikey, {}).get("name", ikey)
            ns = self.small.render(f"{disp}  ×{count}", True, item_col)
            self.screen.blit(ns, (cx + 6, cy + (CELL_H - ns.get_height()) // 2))
            col_i += 1
            if col_i >= COLS:
                col_i = 0
                row_i += 1

        # Known recipes panel (right side)
        rx0 = SCREEN_W - 260
        ry0 = 50
        rh  = SCREEN_H - 70
        pygame.draw.rect(self.screen, (12, 11, 9), (rx0, ry0, 250, rh))
        pygame.draw.rect(self.screen, (60, 55, 50), (rx0, ry0, 250, rh), 1)
        hdr = self.small.render("RECIPES", True, (110, 100, 85))
        self.screen.blit(hdr, (rx0 + 8, ry0 + 4))
        iy = ry0 + 22
        for recipe in MORTAR_RECIPES:
            if iy + 30 > ry0 + rh - 4:
                break
            out_name = ITEMS.get(recipe["output_id"], {}).get("name", recipe["output_id"])
            col = MORTAR_COLORS.get(recipe["output_id"], (180, 170, 155))
            ns = self.small.render(out_name, True, col)
            self.screen.blit(ns, (rx0 + 8, iy))
            iy += 14
            for ing_k, ing_v in recipe["ingredients"].items():
                ing_name = ITEMS.get(ing_k, {}).get("name", ing_k)
                is2 = self.small.render(f"  {ing_name} ×{ing_v}", True, (80, 75, 65))
                self.screen.blit(is2, (rx0 + 8, iy))
                iy += 12
            iy += 6

    def _handle_mortar_click(self, pos, player):
        # Slot selection
        for i, rect in enumerate(self._mortar_slot_rects):
            if rect.collidepoint(pos):
                self._mortar_active_slot = i
                return

        # +/− count buttons inside filled slots
        SLOT_W, SLOT_H, SLOT_GAP = 110, 90, 10
        sx0 = (SCREEN_W - (2 * SLOT_W + SLOT_GAP)) // 2
        sy0 = 50
        for i, slot in enumerate(self._mortar_slots):
            if not slot:
                continue
            sx = sx0 + i * (SLOT_W + SLOT_GAP)
            minus_rect = pygame.Rect(sx + SLOT_W - 26, sy0 + 6, 20, 20)
            plus_rect  = pygame.Rect(sx + SLOT_W - 26, sy0 + 30, 20, 20)
            if minus_rect.collidepoint(pos):
                slot["count"] = max(1, slot["count"] - 1)
                return
            if plus_rect.collidepoint(pos):
                have = player.inventory.get(slot["key"], 0)
                if slot["count"] < have:
                    slot["count"] += 1
                return

        # GRIND button
        if self._mortar_grind_btn and self._mortar_grind_btn.collidepoint(pos):
            slot_dict = {s["key"]: s["count"] for s in self._mortar_slots if s and s.get("key")}
            if not slot_dict:
                return
            matched_id = match_mortar_recipe(slot_dict)
            if matched_id is None:
                return
            for ing_key, ing_cnt in slot_dict.items():
                if player.inventory.get(ing_key, 0) < ing_cnt:
                    return
            for ing_key, ing_cnt in slot_dict.items():
                player.inventory[ing_key] -= ing_cnt
                if player.inventory[ing_key] <= 0:
                    del player.inventory[ing_key]
            player._add_item(matched_id)
            for i in range(len(self._mortar_slots)):
                self._mortar_slots[i] = {}
            self._mortar_active_slot = None
            return

        # Inventory herb picker
        if self._mortar_active_slot is not None:
            for ikey, rect in self._mortar_inv_rects.items():
                if rect.collidepoint(pos):
                    self._mortar_slots[self._mortar_active_slot] = {"key": ikey, "count": 1}
                    self._mortar_active_slot = None
                    return

    # ─────────────────────────────────────────────────────────────────────────
    # BUFF HUD
    # ─────────────────────────────────────────────────────────────────────────

    def _draw_herb_buffs(self, player):
        if not player.herb_buffs:
            return
        x = SCREEN_W - 200
        y = 330
        for buff, data in player.herb_buffs.items():
            dur   = data["duration"]
            label = BUFF_DESCS.get(buff, buff)
            ls    = self.small.render(f"⚗ {label}", True, _TITLE_C)
            self.screen.blit(ls, (x, y))
            bar_w, bar_h = 180, 6
            max_dur = 180.0
            fill = max(0, min(bar_w, int(bar_w * dur / max_dur)))
            pygame.draw.rect(self.screen, _DARK_BG, (x, y + 14, bar_w, bar_h))
            pygame.draw.rect(self.screen, _ACCENT,  (x, y + 14, fill,  bar_h))
            y += 26

    # ─────────────────────────────────────────────────────────────────────────
    # HERB CODEX (called from collections.py)
    # ─────────────────────────────────────────────────────────────────────────

    def _draw_herb_codex(self, player, gy0=58, gx_off=0):
        from items import ITEMS
        CELL_W, CELL_H, GAP = SCREEN_W - gx_off - 300, 68, 6
        CELL_W = max(300, CELL_W)
        detail_x = SCREEN_W - 290

        self._herb_codex_rects.clear()

        # Group by tier
        tiers = [("basic", "Basic Potions"), ("fine", "Fine Potions"), ("elixir", "Elixirs")]
        cy = gy0 - self._herb_codex_scroll
        total_h = 0
        visible_h = SCREEN_H - gy0 - 8

        for tier_key, tier_label in tiers:
            if cy + 22 > SCREEN_H - 8:
                break
            tier_col = _TIER_COLORS.get(tier_key, _LABEL_C)
            if cy >= gy0 - 22:
                hdr = self.font.render(tier_label.upper(), True, tier_col)
                self.screen.blit(hdr, (gx_off + 10, max(gy0, cy)))
            cy += 28
            total_h += 28

            for out_id in RECIPE_ORDER:
                recipe = RECIPES.get(out_id)
                if recipe is None or recipe["tier"] != tier_key:
                    continue
                disc = out_id in player.discovered_recipes
                rect = pygame.Rect(gx_off + 8, cy, CELL_W, CELL_H)
                self._herb_codex_rects[out_id] = rect
                total_h += CELL_H + GAP

                if cy + CELL_H < gy0:
                    cy += CELL_H + GAP
                    continue
                if cy > SCREEN_H - 8:
                    break

                p_col   = POTION_COLORS.get(out_id, _ACCENT)
                out_name = ITEMS.get(out_id, {}).get("name", out_id)
                sel     = (self._herb_codex_selected == out_id)

                if disc:
                    pygame.draw.rect(self.screen, _CELL_BG, rect)
                    pygame.draw.rect(self.screen, p_col, rect, 3 if sel else 1)
                    nm_s = self.font.render(out_name, True, p_col)
                    self.screen.blit(nm_s, (rect.x + 8, rect.y + 6))
                    desc_s = self.small.render(POTION_DESCS.get(out_id, ""), True, _LABEL_C)
                    self.screen.blit(desc_s, (rect.x + 8, rect.y + 30))
                    # ingredient summary
                    ing_parts = [f"{INGREDIENT_DISPLAY_NAMES.get(k,k)} ×{v}"
                                 for k, v in recipe["ingredients"].items()]
                    ing_s = self.small.render("  ".join(ing_parts), True, _HINT_C)
                    self.screen.blit(ing_s, (rect.x + 8, rect.y + 48))
                else:
                    pygame.draw.rect(self.screen, (8, 20, 16), rect)
                    pygame.draw.rect(self.screen, _DIM_C, rect, 1)
                    lock_s = self.small.render("???  Undiscovered", True, _DIM_C)
                    self.screen.blit(lock_s, (rect.x + 8, rect.y + (CELL_H - lock_s.get_height()) // 2))

                cy += CELL_H + GAP

        self._max_herb_codex_scroll = max(0, total_h - visible_h)

        # Detail panel
        if self._herb_codex_selected and self._herb_codex_selected in player.discovered_recipes:
            out_id  = self._herb_codex_selected
            recipe  = RECIPES.get(out_id, {})
            p_col   = POTION_COLORS.get(out_id, _ACCENT)
            pygame.draw.rect(self.screen, _DARK_BG, (detail_x, gy0, 280, 260))
            pygame.draw.rect(self.screen, p_col,    (detail_x, gy0, 280, 260), 2)
            iy = gy0 + 8
            def dline(txt, col=_TITLE_C):
                nonlocal iy
                s = self.small.render(txt, True, col)
                self.screen.blit(s, (detail_x + 10, iy))
                iy += 18
            out_name = ITEMS.get(out_id, {}).get("name", out_id)
            dline(out_name, p_col)
            dline(POTION_DESCS.get(out_id, ""), (180, 230, 200))
            dline(f"Tier: {TIER_LABELS.get(recipe.get('tier',''), '')}", _TIER_COLORS.get(recipe.get("tier","basic"), _LABEL_C))
            dline("Ingredients:", _LABEL_C)
            for ing_k, ing_v in recipe.get("ingredients", {}).items():
                dline(f"  {INGREDIENT_DISPLAY_NAMES.get(ing_k, ing_k)} ×{ing_v}", _TITLE_C)
            dline(f"Station: {recipe.get('station','').title()}", _HINT_C)
