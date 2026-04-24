import pygame
from constants import SCREEN_W, SCREEN_H
from herbalism import (
    match_recipe, get_dried_item, can_press_flower, recipe_requires_research,
    DRYING_TABLE, DRYABLE_ITEMS, RECIPES, RECIPE_ORDER,
    POTION_DESCS, POTION_COLORS, TIER_LABELS, BUFF_DESCS,
    INGREDIENT_DISPLAY_NAMES, ALL_POTION_IDS,
)

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
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("DRYING RACK", True, _TITLE_C)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, _HINT_C)
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        half_w = SCREEN_W // 2 - 10

        # ── Left: dry inventory items ─────────────────────────────────────
        pygame.draw.rect(self.screen, _DARK_BG, (8, 36, half_w, SCREEN_H - 48))
        pygame.draw.rect(self.screen, _DIM_C,   (8, 36, half_w, SCREEN_H - 48), 1)
        hdr = self.small.render("DRY FROM INVENTORY", True, _LABEL_C)
        self.screen.blit(hdr, (8 + 8, 42))

        self._dry_select_rects.clear()
        ry = 64
        for src_key in DRYABLE_ITEMS:
            count = player.inventory.get(src_key, 0)
            if count <= 0:
                continue
            out_key = DRYING_TABLE[src_key]
            from items import ITEMS
            src_name = ITEMS.get(src_key, {}).get("name", src_key)
            out_name = ITEMS.get(out_key, {}).get("name", out_key)
            btn_rect = pygame.Rect(16, ry, half_w - 16, 44)
            self._dry_select_rects[src_key] = btn_rect
            pygame.draw.rect(self.screen, _CELL_BG, btn_rect)
            pygame.draw.rect(self.screen, _ACCENT, btn_rect, 2)
            top_s = self.font.render(f"{src_name}  ×{count}", True, _TITLE_C)
            self.screen.blit(top_s, (btn_rect.x + 8, btn_rect.y + 4))
            bot_s = self.small.render(f"→  {out_name}", True, _LABEL_C)
            self.screen.blit(bot_s, (btn_rect.x + 8, btn_rect.y + 24))
            ry += 52

        if ry == 64:
            msg = self.font.render("No dryable items in inventory.", True, _LABEL_C)
            self.screen.blit(msg, (16, SCREEN_H // 2 - 10))

        # ── Right: press wildflowers ──────────────────────────────────────
        rx0 = SCREEN_W // 2 + 10
        pygame.draw.rect(self.screen, _DARK_BG, (rx0, 36, half_w - 10, SCREEN_H - 48))
        pygame.draw.rect(self.screen, _DIM_C,   (rx0, 36, half_w - 10, SCREEN_H - 48), 1)
        hdr2 = self.small.render("PRESS WILDFLOWERS", True, _LABEL_C)
        self.screen.blit(hdr2, (rx0 + 8, 42))

        common_fl  = [wf for wf in player.wildflowers if wf.rarity in ("common", "uncommon")]
        rare_fl    = [wf for wf in player.wildflowers if wf.rarity in ("rare", "epic", "legendary")]

        self._dry_flower_btns.clear()
        btn_y = 64
        for label, pool, out_key in [
            ("Press Common Flowers", common_fl, "pressed_flower"),
            ("Press Rare Flowers",   rare_fl,   "pressed_rare_flower"),
        ]:
            count = len(pool)
            btn_rect = pygame.Rect(rx0 + 8, btn_y, half_w - 26, 54)
            active   = count > 0
            self._dry_flower_btns[out_key] = (btn_rect, pool)
            bg_col = _CELL_BG if active else (12, 22, 18)
            brd    = _ACCENT if active else _DIM_C
            pygame.draw.rect(self.screen, bg_col, btn_rect)
            pygame.draw.rect(self.screen, brd, btn_rect, 2)
            top_s = self.font.render(f"{label}  ×{count}", True, _TITLE_C if active else _DIM_C)
            self.screen.blit(top_s, (btn_rect.x + 8, btn_rect.y + 6))
            from items import ITEMS
            out_name = ITEMS.get(out_key, {}).get("name", out_key)
            bot_s = self.small.render(f"→  {out_name}", True, _LABEL_C if active else _DIM_C)
            self.screen.blit(bot_s, (btn_rect.x + 8, btn_rect.y + 30))
            btn_y += 64

        note = self.small.render("Pressing consumes 1 wildflower from your collection.", True, _HINT_C)
        self.screen.blit(note, (rx0 + 8, btn_y + 12))

    def _handle_drying_rack_click(self, pos, player):
        for src_key, rect in self._dry_select_rects.items():
            if rect.collidepoint(pos):
                if player.inventory.get(src_key, 0) > 0:
                    out_key = DRYING_TABLE[src_key]
                    player.inventory[src_key] -= 1
                    if player.inventory[src_key] <= 0:
                        del player.inventory[src_key]
                    player._add_item(out_key)
                return
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
