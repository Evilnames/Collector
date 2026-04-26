import pygame
from achievements import ACHIEVEMENTS, item_display_name, get_achievement_progress
from fish import (render_fish, FISH_TYPES, FISH_TYPE_ORDER, FISH_BIOME_GROUPS,
                  FISH_RARITY_COLORS, RARITY_LABEL as FISH_RARITY_LABEL)
from rocks import (render_rock, render_codex_preview, RARITY_COLORS,
                   ROCK_TYPE_ORDER, ROCK_TYPE_DESCRIPTIONS, ROCK_TYPES)
from wildflowers import (render_wildflower, get_flower_preview,
                         WILDFLOWER_TYPE_ORDER, WILDFLOWER_TYPES,
                         WILDFLOWER_BIODOME_AFFINITY)
from fossils import (render_fossil, render_fossil_codex_preview,
                     FOSSIL_TYPE_ORDER, FOSSIL_TYPES,
                     FOSSIL_SPECIAL_DESCS, FOSSIL_TYPE_DESCRIPTIONS, FOSSIL_AGE_COLORS)
from gemstones import (render_rough_gem, render_gem, render_gem_codex_preview,
                       GEM_TYPE_ORDER, GEM_TYPES, RARITY_COLORS as GEM_RARITY_COLORS,
                       GEM_TYPE_DESCRIPTIONS, GEM_CUT_DESCS)
from renderer import render_mushroom_preview
from blocks import BLOCKS
from coffee import (BIOME_DISPLAY_NAMES, ROAST_LEVEL_DESCS, ROAST_COLORS,
                    COFFEE_TYPE_ORDER)
from wine import (WINE_STYLE_DESCS, WINE_STYLE_COLORS, WINE_TYPE_ORDER,
                  WINE_STYLE_ORDER, VARIETY_DISPLAY_NAMES as WINE_VARIETY_NAMES,
                  BIOME_DISPLAY_NAMES as WINE_BIOME_NAMES)
from spirits import SPIRIT_TYPE_ORDER
from salt import SALT_TYPE_ORDER, BIOME_DISPLAY_NAMES as SALT_BIOME_NAMES, GRADES, OUTPUT_DESCS as SALT_OUTPUT_DESCS, OUTPUT_COLORS as SALT_OUTPUT_COLORS, _CODEX_BIOMES as SALT_CODEX_BIOMES
from constants import SCREEN_W, SCREEN_H
from ._data import (_MUSHROOM_ORDER, _MUSHROOM_BIOME, _MUSHROOM_DROP_COLOR,
                    _MUSHROOM_SHAPES, _MUSHROOM_NAMES, SPECIAL_DESCS, RARITY_LABEL)


class CollectionsMixin:

    def _draw_collection(self, player):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        self.screen.blit(overlay, (0, 0))

        n_rock_disc   = len(player.discovered_types)
        n_rock_total  = len(ROCK_TYPE_ORDER)
        n_fl_disc     = len(player.discovered_flower_types)
        n_fl_total    = len(WILDFLOWER_TYPE_ORDER)
        n_mush_disc   = len(player.discovered_mushroom_types)
        n_mush_total  = len(_MUSHROOM_ORDER)
        n_fossil_disc = len(player.discovered_fossil_types)
        n_fossil_total = len(FOSSIL_TYPE_ORDER)
        n_gem_disc    = len(player.discovered_gem_types)
        n_gem_total   = len(GEM_TYPE_ORDER)
        n_ach_unlocked = sum(1 for v in self.achievements_data.values() if v)
        n_ach_total    = len(ACHIEVEMENTS)

        n_mush_owned = sum(1 for b in _MUSHROOM_ORDER if player.mushrooms_found.get(b, 0) > 0)
        n_fish_disc  = len(player.discovered_fish_species)
        n_fish_total = len(FISH_TYPE_ORDER)
        n_coffee_owned  = len(player.coffee_beans)
        n_wine_owned    = len(getattr(player, "wine_grapes", []))
        n_spirits_owned = len(getattr(player, "spirits", []))
        n_tea_owned     = len(getattr(player, "tea_leaves", []))
        from herbalism import ALL_POTION_IDS
        n_potions_owned = sum(player.inventory.get(k, 0) for k in ALL_POTION_IDS)
        n_textiles_owned = len(getattr(player, "textiles", []))
        n_cheese_owned   = len([c for c in getattr(player, "cheese_wheels", []) if c.state == "aged"])
        n_jewelry_owned    = len(getattr(player, "jewelry", []))
        n_sculptures_owned = len(getattr(player, "sculptures_created", []))
        n_tapestries_owned = len(getattr(player, "tapestries_created", []))
        n_pottery_owned    = len(getattr(player, "pottery_pieces", []))
        n_salt_owned       = len(getattr(player, "salt_crystals", []))
        n_dogs_tamed       = getattr(player, "dogs_tamed", 0)
        n_weapons_crafted  = len(getattr(player, "crafted_weapons", []))
        total_collected = (len(player.rocks) + len(player.wildflowers) +
                           len(player.fossils) + len(player.gems) + n_mush_owned +
                           n_coffee_owned + n_wine_owned + n_spirits_owned + n_tea_owned +
                           n_potions_owned + n_textiles_owned + n_cheese_owned + n_jewelry_owned +
                           n_sculptures_owned + n_tapestries_owned + n_pottery_owned + n_salt_owned +
                           n_dogs_tamed + n_weapons_crafted)

        # ---- 3 main tabs ----
        self._tab_rects.clear()
        TAB_H, TAB_GAP, tab_y = 26, 8, 24
        tab_defs = [
            (0, f"COLLECTION  ({total_collected})",           (38, 38, 55), (110, 110, 175), (50, 50, 72), (145, 145, 215), (200, 200, 255)),
            (1, "ENCYCLOPEDIA",                               (25, 45, 40), (72, 175, 152),  (14, 26, 23), (44, 105, 90),  (148, 228, 208)),
            (2, f"AWARDS  ({n_ach_unlocked}/{n_ach_total})", (45, 38, 10), (210, 178, 38),  (24, 20, 6),  (108, 88, 20),  (255, 215, 80)),
        ]
        TAB_W = min(240, (SCREEN_W - 20 - TAB_GAP * (len(tab_defs) - 1)) // len(tab_defs))
        total_tw = len(tab_defs) * TAB_W + (len(tab_defs) - 1) * TAB_GAP
        tx0 = SCREEN_W // 2 - total_tw // 2
        for tab_i, label, bg_a, brd_a, bg_i, brd_i, txt_a in tab_defs:
            tx = tx0 + tab_i * (TAB_W + TAB_GAP)
            rect = pygame.Rect(tx, tab_y, TAB_W, TAB_H)
            self._tab_rects[tab_i] = rect
            active = (tab_i == self._collection_tab)
            pygame.draw.rect(self.screen, bg_a if active else bg_i, rect)
            pygame.draw.rect(self.screen, brd_a if active else brd_i, rect, 2)
            txt_col = txt_a if active else brd_i
            ls = self.small.render(self._fit_label(label, TAB_W - 8), True, txt_col)
            self.screen.blit(ls, (tx + TAB_W // 2 - ls.get_width() // 2,
                                   tab_y + TAB_H // 2 - ls.get_height() // 2))

        # Title
        if self._collection_tab == 2:
            title_text, title_col = "AWARDS", (255, 215, 80)
        elif self._collection_tab == 1:
            enc_titles = ["ROCK CODEX", "FLOWER CODEX", "MUSHROOM CODEX", "FOSSIL CODEX", "GEM CODEX", "BIRD CODEX", "FISH CODEX", "COFFEE CODEX", "WINE CODEX", "SPIRITS CODEX", "INSECT CODEX", "FOOD CODEX", "HORSE CODEX", "TEA CODEX", "HERB CODEX", "TEXTILE CODEX", "CHEESE CODEX", "JEWELRY CODEX", "POTTERY CODEX", "SALT CODEX", "PAIRINGS CODEX", "DOG CODEX", "HUNTING LOG", "WEAPONS CODEX"]
            enc_cols   = [(180, 220, 255), (180, 255, 180), (220, 210, 140), (210, 185, 140), (180, 245, 225), (140, 210, 255), (120, 185, 240), (210, 145, 60), (220, 140, 160), (230, 170, 80), (140, 230, 150), (235, 175, 105), (210, 175, 100), (130, 215, 140), (140, 235, 200), (220, 160, 250), (245, 230, 160), (240, 205, 100), (210, 160, 110), (235, 232, 215), (225, 180, 255), (215, 180, 110), (220, 170, 100), (210, 195, 165)]
            title_text = enc_titles[self._encyclopedia_cat]
            title_col  = enc_cols[self._encyclopedia_cat]
        else:
            title_text = "COLLECTION"
            title_col  = (200, 200, 255)
        title_s = self.font.render(title_text, True, title_col)
        self.screen.blit(title_s, (SCREEN_W // 2 - title_s.get_width() // 2, 4))

        SUB_Y = tab_y + TAB_H + 4   # 54
        GY0   = SUB_Y

        # ---- Content ----
        SIDEBAR_W = 130
        if self._collection_tab == 0:
            # Left sidebar: filter list
            FILTER_DEFS = [
                ("all",       f"ALL ({total_collected})",          (55, 55, 75),  (130, 130, 180), (200, 200, 240)),
                ("rocks",     f"ROCKS ({len(player.rocks)})",      (42, 52, 70),  (95,  138, 198), (175, 208, 248)),
                ("flowers",   f"FLOWERS ({len(player.wildflowers)})",(32, 58, 35),(85,  178, 100), (168, 235, 178)),
                ("fossils",   f"FOSSILS ({len(player.fossils)})",  (50, 40, 20),  (168, 140, 72),  (215, 182, 112)),
                ("gems",      f"GEMS ({len(player.gems)})",        (22, 48, 45),  (72,  195, 170), (145, 235, 215)),
                ("mushrooms", f"MUSHROOMS ({n_mush_owned})",       (40, 36, 16),  (148, 132, 56),  (198, 182, 105)),
                ("coffee",    f"COFFEE ({n_coffee_owned})",        (40, 25, 10),  (140,  90,  35), (210, 150,  70)),
                ("wine",      f"WINE ({n_wine_owned})",            (40, 15, 22),  (175,  85, 110), (235, 155, 175)),
                ("spirits",   f"SPIRITS ({n_spirits_owned})",      (30, 22,  8),  (175, 115,  45), (230, 170,  80)),
                ("tea",       f"TEA ({n_tea_owned})",              (25, 45, 20),  ( 65, 160,  75), (130, 215, 140)),
                ("herbs",     f"POTIONS ({n_potions_owned})",      (10, 28, 24),  ( 70, 175, 140), (140, 235, 200)),
                ("textiles",  f"TEXTILES ({n_textiles_owned})",    (25, 12, 32),  (160,  90, 190), (220, 160, 250)),
                ("cheese",    f"CHEESE ({n_cheese_owned})",         (38, 30, 10),  (185, 155,  65), (245, 230, 160)),
                ("jewelry",    f"JEWELRY ({n_jewelry_owned})",        (28, 22,  8),  (180, 150,  60), (240, 205, 100)),
                ("sculptures", f"SCULPTURES ({n_sculptures_owned})", (35, 30, 22),  (190, 180, 155), (240, 230, 200)),
                ("tapestries", f"TAPESTRIES ({n_tapestries_owned})", (28, 20, 12),  (195, 165, 110), (245, 215, 165)),
                ("pottery",    f"POTTERY ({n_pottery_owned})",       (40, 25, 10),  (160, 110,  80), (210, 160, 110)),
                ("salt",       f"SALT ({n_salt_owned})",             (32, 30, 28),  (190, 185, 165), (235, 232, 215)),
                ("dogs",       f"DOGS ({n_dogs_tamed})",              (28, 20, 10),  (170, 130,  60), (215, 180, 110)),
                ("weapons",    f"WEAPONS ({n_weapons_crafted})",      (30, 22, 12),  (155, 140, 120), (210, 195, 165)),
            ]
            SB_X, SB_W, SB_BTN_H, SB_GAP = 4, SIDEBAR_W - 8, 26, 4
            self._collection_filter_rects.clear()
            total_sb_h = len(FILTER_DEFS) * (SB_BTN_H + SB_GAP)
            visible_sb_h = SCREEN_H - GY0 - 4
            self._max_collection_sidebar_scroll = max(0, total_sb_h - visible_sb_h)
            self._collection_sidebar_scroll = min(self._collection_sidebar_scroll,
                                                   self._max_collection_sidebar_scroll)
            sb_clip = pygame.Rect(0, GY0, SIDEBAR_W, visible_sb_h)
            self.screen.set_clip(sb_clip)
            for fi, (fkey, flabel, bg_d, brd_d, txt_d) in enumerate(FILTER_DEFS):
                by = GY0 + fi * (SB_BTN_H + SB_GAP) - self._collection_sidebar_scroll
                if by + SB_BTN_H <= GY0 or by >= GY0 + visible_sb_h:
                    continue
                frect = pygame.Rect(SB_X, by, SB_W, SB_BTN_H)
                self._collection_filter_rects[fkey] = frect.clip(sb_clip)
                is_active_f = (self._collection_filter == fkey)
                if is_active_f:
                    fb = (min(255, bg_d[0]+22), min(255, bg_d[1]+22), min(255, bg_d[2]+22))
                    fb_brd, fb_txt = brd_d, txt_d
                else:
                    fb = (bg_d[0]//2, bg_d[1]//2, bg_d[2]//2)
                    fb_brd = (brd_d[0]//2, brd_d[1]//2, brd_d[2]//2)
                    fb_txt = fb_brd
                pygame.draw.rect(self.screen, fb, frect)
                pygame.draw.rect(self.screen, fb_brd, frect, 2 if is_active_f else 1)
                fs = self.small.render(self._fit_label(flabel, SB_W - 6), True, fb_txt)
                self.screen.blit(fs, (SB_X + SB_W // 2 - fs.get_width() // 2,
                                       by + SB_BTN_H // 2 - fs.get_height() // 2))
            self.screen.set_clip(None)
            self._draw_sidebar_scroll_hint(GY0, visible_sb_h, SIDEBAR_W,
                                            self._collection_sidebar_scroll,
                                            self._max_collection_sidebar_scroll)
            self._draw_collection_unified(player, GY0, gx_off=SIDEBAR_W)
        elif self._collection_tab == 1:
            # Left sidebar: encyclopedia category list
            ENC_THEME = [
                ((42, 52, 70),  (95, 138, 198),  (175, 208, 248)),
                ((32, 58, 35),  (85, 178, 100),  (168, 235, 178)),
                ((40, 36, 16),  (148, 132, 56),  (198, 182, 105)),
                ((50, 40, 20),  (168, 140, 72),  (215, 182, 112)),
                ((22, 48, 45),  (72, 195, 170),  (145, 235, 215)),
                ((18, 40, 58),  (70, 150, 220),  (140, 210, 255)),
                ((18, 32, 50),  (55, 110, 185),  (120, 185, 240)),
                ((35, 22,  8),  (140,  90,  30), (210, 145,  60)),
                ((40, 18, 28),  (175,  90, 115), (235, 160, 180)),
                ((30, 22,  8),  (175, 115,  45), (230, 170,  80)),
                ((20, 40, 22),  (70,  170,  80), (140, 230, 150)),
                ((38, 24, 12),  (175, 105,  45), (235, 175, 105)),
                ((38, 28, 14),  (160, 120,  55), (210, 175, 100)),
                ((25, 45, 20),  ( 65, 160,  75), (130, 215, 140)),
                ((10, 28, 24),  ( 70, 175, 140), (140, 235, 200)),
                ((25, 12, 32),  (160,  90, 190), (220, 160, 250)),
                ((38, 30, 10),  (185, 155,  65), (245, 230, 160)),
                ((45, 20, 35),  (190, 100, 155), (250, 170, 220)),   # Jewelry
                ((40, 25, 10),  (160, 110,  80), (210, 160, 110)),   # Pottery
                ((32, 30, 28),  (190, 185, 165), (235, 232, 215)),   # Salt
                ((30, 18, 38),  (165, 110, 215), (225, 180, 255)),   # Pairings
                ((28, 20, 10),  (170, 130,  60), (215, 180, 110)),   # Dogs
                ((45, 35, 20),  (180, 120,  60), (220, 170, 100)),   # Hunting
                ((30, 22, 12),  (155, 140, 120), (210, 195, 165)),   # Weapons
            ]
            enc_labels = ["ROCKS", "FLOWERS", "MUSHROOMS", "FOSSILS", "GEMS",
                          "BIRDS", "FISH", "COFFEE", "WINE", "SPIRITS", "INSECTS", "FOOD", "HORSES", "TEA", "HERBS", "TEXTILES", "CHEESE", "JEWELRY", "POTTERY", "SALT", "PAIRINGS", "DOGS", "HUNTING", "WEAPONS"]
            SB_X, SB_W, SB_BTN_H, SB_GAP = 4, SIDEBAR_W - 8, 26, 4
            self._encyclopedia_cat_rects.clear()
            total_sb_h = len(enc_labels) * (SB_BTN_H + SB_GAP)
            visible_sb_h = SCREEN_H - GY0 - 4
            self._max_encyclopedia_sidebar_scroll = max(0, total_sb_h - visible_sb_h)
            self._encyclopedia_sidebar_scroll = min(self._encyclopedia_sidebar_scroll,
                                                     self._max_encyclopedia_sidebar_scroll)
            sb_clip = pygame.Rect(0, GY0, SIDEBAR_W, visible_sb_h)
            self.screen.set_clip(sb_clip)
            for cat_i, cat_label in enumerate(enc_labels):
                by = GY0 + cat_i * (SB_BTN_H + SB_GAP) - self._encyclopedia_sidebar_scroll
                if by + SB_BTN_H <= GY0 or by >= GY0 + visible_sb_h:
                    continue
                brect = pygame.Rect(SB_X, by, SB_W, SB_BTN_H)
                self._encyclopedia_cat_rects[cat_i] = brect.clip(sb_clip)
                bg_d, brd_d, txt_d = ENC_THEME[cat_i]
                is_active = (self._encyclopedia_cat == cat_i)
                if is_active:
                    eb = (min(255, bg_d[0]+22), min(255, bg_d[1]+22), min(255, bg_d[2]+22))
                    eb_brd, eb_txt = brd_d, txt_d
                else:
                    eb = (bg_d[0]//2, bg_d[1]//2, bg_d[2]//2)
                    eb_brd = (brd_d[0]//2, brd_d[1]//2, brd_d[2]//2)
                    eb_txt = eb_brd
                pygame.draw.rect(self.screen, eb, brect)
                pygame.draw.rect(self.screen, eb_brd, brect, 2 if is_active else 1)
                ls = self.small.render(cat_label, True, eb_txt)
                self.screen.blit(ls, (SB_X + SB_W // 2 - ls.get_width() // 2,
                                       by + SB_BTN_H // 2 - ls.get_height() // 2))
            self.screen.set_clip(None)
            self._draw_sidebar_scroll_hint(GY0, visible_sb_h, SIDEBAR_W,
                                            self._encyclopedia_sidebar_scroll,
                                            self._max_encyclopedia_sidebar_scroll)

            cat_draw = [
                self._draw_codex,
                self._draw_flower_codex,
                self._draw_mushroom_codex,
                self._draw_fossil_codex,
                self._draw_gem_codex,
                self._draw_bird_codex,
                self._draw_fish_codex,
                self._draw_coffee_codex,
                self._draw_wine_codex,
                self._draw_spirits_codex,
                self._draw_insect_codex,
                self._draw_food_codex,
                self._draw_horse_codex,
                self._draw_tea_codex,
                self._draw_herb_codex,
                self._draw_textile_codex,
                self._draw_cheese_codex,
                self._draw_jewelry_codex,
                self._draw_pottery_codex,
                self._draw_salt_codex,
                self._draw_pairings_codex,
                self._draw_dog_codex,
                self._draw_hunting_codex,
                self._draw_weapons_codex,
            ]
            if 0 <= self._encyclopedia_cat < len(cat_draw):
                cat_draw[self._encyclopedia_cat](player, gy0=GY0, gx_off=SIDEBAR_W)
        else:
            self._draw_achievements()

    def _draw_sidebar_scroll_hint(self, gy0, visible_h, sidebar_w, scroll, max_scroll):
        if max_scroll <= 0:
            return
        track_x = sidebar_w - 4
        track_w = 3
        total_h = visible_h + max_scroll
        thumb_h = max(20, int(visible_h * visible_h / total_h))
        thumb_y = gy0 + int((visible_h - thumb_h) * scroll / max_scroll)
        pygame.draw.rect(self.screen, (40, 40, 50), (track_x, gy0, track_w, visible_h))
        pygame.draw.rect(self.screen, (140, 140, 160), (track_x, thumb_y, track_w, thumb_h))

    def _fit_label(self, text, max_width):
        if self.small.size(text)[0] <= max_width:
            return text
        while text:
            text = text[:-1]
            if self.small.size(text + "...")[0] <= max_width:
                return text + "..."
        return "..."

    # ------------------------------------------------------------------
    # Unified collection tab
    # ------------------------------------------------------------------

    def _draw_collection_unified(self, player, gy0=80, gx_off=0):
        flt = self._collection_filter
        items = []
        if flt in ("all", "rocks"):
            items.extend(("rock", i) for i in range(len(player.rocks)))
        if flt in ("all", "flowers"):
            items.extend(("flower", i) for i in range(len(player.wildflowers)))
        if flt in ("all", "fossils"):
            items.extend(("fossil", i) for i in range(len(player.fossils)))
        if flt in ("all", "gems"):
            items.extend(("gem", i) for i in range(len(player.gems)))
        if flt in ("all", "mushrooms"):
            items.extend(("mushroom", bid) for bid in _MUSHROOM_ORDER
                         if player.mushrooms_found.get(bid, 0) > 0)
        if flt in ("all", "coffee"):
            items.extend(("coffee", i) for i in range(len(player.coffee_beans)))
        if flt in ("all", "wine"):
            items.extend(("wine", i) for i in range(len(getattr(player, "wine_grapes", []))))
        if flt in ("all", "spirits"):
            items.extend(("spirit", i) for i in range(len(getattr(player, "spirits", []))))
        if flt in ("all", "tea"):
            items.extend(("tea", i) for i in range(len(getattr(player, "tea_leaves", []))))
        if flt in ("all", "herbs"):
            from herbalism import ALL_POTION_IDS
            for pkey in ALL_POTION_IDS:
                for _ in range(player.inventory.get(pkey, 0)):
                    items.append(("herb", pkey))
        if flt in ("all", "textiles"):
            items.extend(("textile", i) for i in range(len(getattr(player, "textiles", []))))
        if flt in ("all", "jewelry"):
            items.extend(("jewelry", i) for i in range(len(getattr(player, "jewelry", []))))
        if flt in ("all", "sculptures"):
            items.extend(("sculpture", i) for i in range(len(getattr(player, "sculptures_created", []))))
        if flt in ("all", "tapestries"):
            items.extend(("tapestry", i) for i in range(len(getattr(player, "tapestries_created", []))))
        if flt in ("all", "pottery"):
            items.extend(("pottery", i) for i in range(len(getattr(player, "pottery_pieces", []))))
        if flt in ("all", "salt"):
            items.extend(("salt", i) for i in range(len(getattr(player, "salt_crystals", []))))
        if flt in ("all", "weapons"):
            items.extend(("weapon", i) for i in range(len(getattr(player, "crafted_weapons", []))))

        if not items:
            msg = self.font.render("Nothing collected yet!", True, (80, 80, 90))
            self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2))
            return

        CELL, GAP, COLS = 82, 8, 8
        content_w = SCREEN_W - gx_off
        gx0 = gx_off + (content_w - (COLS * CELL + (COLS - 1) * GAP)) // 2

        # Validate / clear selection if no longer in current filter
        if self._unified_selected is not None:
            sel_cat, sel_key = self._unified_selected
            still_valid = (sel_cat, sel_key) in items
            if not still_valid:
                self._unified_selected = None

        detail_x = None
        if self._unified_selected is not None:
            detail_x = SCREEN_W - 340
            COLS = max(1, (detail_x - gx0 - 10) // (CELL + GAP))

        total_rows   = (len(items) + COLS - 1) // COLS
        visible_rows = (SCREEN_H - gy0 - 8 + GAP) // (CELL + GAP)
        self._max_unified_scroll = max(0, total_rows - visible_rows)
        self._unified_scroll = max(0, min(self._max_unified_scroll, self._unified_scroll))

        if self._max_unified_scroll > 0:
            sb_x  = gx0 + COLS * (CELL + GAP) - GAP + 8
            sb_h  = SCREEN_H - gy0 - 8
            sb_th = max(20, sb_h * visible_rows // total_rows)
            sb_top = gy0 + (sb_h - sb_th) * self._unified_scroll // self._max_unified_scroll
            pygame.draw.rect(self.screen, (35, 35, 48), (sb_x, gy0, 7, sb_h))
            pygame.draw.rect(self.screen, (100, 100, 140), (sb_x, sb_top, 7, sb_th))

        self._unified_rects.clear()
        for pos_idx, (cat, key) in enumerate(items):
            col = pos_idx % COLS
            row = pos_idx // COLS
            display_row = row - self._unified_scroll
            if display_row < 0:
                continue
            x = gx0 + col * (CELL + GAP)
            y = gy0 + display_row * (CELL + GAP)
            if y + CELL > SCREEN_H - 8:
                break
            rect = pygame.Rect(x, y, CELL, CELL)
            self._unified_rects[(cat, key)] = rect

            selected = (self._unified_selected == (cat, key))

            if cat == "rock":
                it = player.rocks[key]
                rar_col = RARITY_COLORS[it.rarity]
                pygame.draw.rect(self.screen, (45, 42, 60) if selected else (30, 30, 40), rect)
                pygame.draw.rect(self.screen, rar_col, rect, 3 if selected else 2)
                img = render_rock(it, 58)
                label = it.base_type.replace("_", " ")
                label_col = (160, 160, 160)
            elif cat == "flower":
                it = player.wildflowers[key]
                rar_col = RARITY_COLORS[it.rarity]
                pygame.draw.rect(self.screen, (35, 50, 35) if selected else (22, 35, 22), rect)
                pygame.draw.rect(self.screen, rar_col, rect, 3 if selected else 2)
                img = render_wildflower(it, 58)
                label = it.flower_type.replace("_", " ")
                label_col = (140, 175, 140)
            elif cat == "fossil":
                it = player.fossils[key]
                rar_col = RARITY_COLORS[it.rarity]
                pygame.draw.rect(self.screen, (45, 40, 28) if selected else (30, 26, 18), rect)
                pygame.draw.rect(self.screen, rar_col, rect, 3 if selected else 2)
                img = render_fossil(it, 58)
                label = it.fossil_type.replace("_", " ")
                label_col = (175, 155, 115)
            elif cat == "gem":
                it = player.gems[key]
                rar_col = GEM_RARITY_COLORS.get(it.rarity, (120, 120, 120))
                pygame.draw.rect(self.screen, (28, 42, 40) if selected else (18, 28, 26), rect)
                pygame.draw.rect(self.screen, rar_col, rect, 3 if selected else 2)
                img = render_rough_gem(it, 58) if it.state == "rough" else render_gem(it, 58)
                label = ("rough " if it.state == "rough" else "") + it.gem_type.replace("_", " ")
                label_col = (120, 195, 175)
            elif cat == "bird":
                from birds import SPECIES_BY_ID
                obs  = player.birds_observed.get(key, {})
                sp_cls = SPECIES_BY_ID.get(key)
                rarity_bird_cols = {"common": (120, 170, 120), "uncommon": (100, 170, 220), "rare": (180, 120, 230)}
                rar_col = rarity_bird_cols.get(sp_cls.RARITY if sp_cls else "common", (120, 170, 120))
                pygame.draw.rect(self.screen, (18, 35, 50) if selected else (12, 24, 36), rect)
                pygame.draw.rect(self.screen, rar_col, rect, 3 if selected else 2)
                # Draw bird icon into a surface
                bird_icon = pygame.Surface((58, 58), pygame.SRCALPHA)
                bird_icon.fill((0, 0, 0, 0))
                if sp_cls:
                    bc = sp_cls.BODY_COLOR
                    wc = sp_cls.WING_COLOR
                    pygame.draw.ellipse(bird_icon, wc, (4, 22, 50, 20))
                    pygame.draw.ellipse(bird_icon, bc, (10, 24, 36, 16))
                    pygame.draw.circle(bird_icon, sp_cls.HEAD_COLOR, (44, 22), 8)
                    pygame.draw.rect(bird_icon, sp_cls.BEAK_COLOR, (50, 22, 8, 3))
                    pygame.draw.ellipse(bird_icon, sp_cls.ACCENT_COLOR, (14, 28, 24, 8))
                img = bird_icon
                label = key.replace("_", " ")
                label_col = (140, 200, 230)
                cnt_s = self.small.render(f"×{obs.get('count', 0)}", True, (180, 220, 240))
                self.screen.blit(cnt_s, (x + CELL - cnt_s.get_width() - 2, y + 2))
            elif cat == "fish":
                it = player.fish_caught[key]
                rar_col = FISH_RARITY_COLORS.get(it.rarity, (120, 120, 120))
                pygame.draw.rect(self.screen, (18, 30, 46) if selected else (10, 18, 28), rect)
                pygame.draw.rect(self.screen, rar_col, rect, 3 if selected else 2)
                img = render_fish(it, 58)
                label = FISH_TYPES.get(it.species, {}).get("name", it.species.replace("_", " ").title())
                label_col = (100, 165, 215)
            elif cat == "coffee":
                it = player.coffee_beans[key]
                roast_col = ROAST_COLORS.get(it.roast_level, (80, 50, 20))
                bg_col = (40, 25, 10) if selected else (25, 15, 5)
                pygame.draw.rect(self.screen, bg_col, rect)
                pygame.draw.rect(self.screen, roast_col, rect, 3 if selected else 2)
                img = pygame.Surface((58, 58), pygame.SRCALPHA)
                img.fill((0, 0, 0, 0))
                cx2, cy2 = 29, 29
                pygame.draw.ellipse(img, roast_col, (cx2 - 16, cy2 - 22, 32, 44))
                line_col = (max(0, roast_col[0] - 40), max(0, roast_col[1] - 40), max(0, roast_col[2] - 40))
                pygame.draw.line(img, line_col, (cx2, cy2 - 18), (cx2, cy2 + 18), 2)
                state_char = {"raw": "R", "roasted": "✓", "blended": "B"}.get(it.state, "?")
                sc_s = self.small.render(state_char, True, (220, 180, 100))
                img.blit(sc_s, (cx2 - sc_s.get_width() // 2, 2))
                label = BIOME_DISPLAY_NAMES.get(it.origin_biome, it.origin_biome)
                label_col = (210, 150, 70)
            elif cat == "wine":
                it = getattr(player, "wine_grapes", [])[key]
                style_col = WINE_STYLE_COLORS.get(it.style, (175, 90, 115))
                bg_col = (35, 12, 20) if selected else (22, 8, 14)
                pygame.draw.rect(self.screen, bg_col, rect)
                pygame.draw.rect(self.screen, style_col, rect, 3 if selected else 2)
                img = pygame.Surface((58, 58), pygame.SRCALPHA)
                img.fill((0, 0, 0, 0))
                for gx3, gy3 in [(20, 10), (34, 10), (14, 22), (28, 22), (42, 22), (20, 34), (34, 34)]:
                    pygame.draw.circle(img, style_col, (gx3, gy3), 7)
                pygame.draw.line(img, (120, 160, 80), (29, 40), (29, 54), 2)
                state_char = {"raw": "R", "crushed": "C", "fermented": "F", "aged": "A", "blended": "B"}.get(it.state, "?")
                sc_s = self.small.render(state_char, True, (240, 200, 210))
                img.blit(sc_s, (img.get_width() - sc_s.get_width() - 2, 2))
                label = WINE_VARIETY_NAMES.get(it.variety, it.variety.replace("_", " "))
                label_col = (230, 150, 170)
            elif cat == "spirit":
                from spirits import SPIRIT_TYPE_COLORS, BIOME_DISPLAY_NAMES as SBIOME
                it = getattr(player, "spirits", [])[key]
                sc3 = SPIRIT_TYPE_COLORS.get(it.spirit_type, (185, 140, 70))
                bg_col = (35, 24, 10) if selected else (22, 14, 5)
                pygame.draw.rect(self.screen, bg_col, rect)
                pygame.draw.rect(self.screen, sc3, rect, 3 if selected else 2)
                img = pygame.Surface((58, 58), pygame.SRCALPHA)
                img.fill((0, 0, 0, 0))
                pygame.draw.rect(img, sc3, (21, 24, 16, 28))
                pygame.draw.rect(img, sc3, (25, 14, 8, 13))
                pygame.draw.rect(img, (min(255, sc3[0] + 60), min(255, sc3[1] + 60), min(255, sc3[2] + 60)), (22, 26, 6, 6))
                state_char = {"raw": "R", "distilled": "D", "aged": "A", "blended": "B"}.get(it.state, "?")
                sc_s3 = self.small.render(state_char, True, (240, 215, 120))
                img.blit(sc_s3, (img.get_width() - sc_s3.get_width() - 2, 2))
                label = SBIOME.get(it.origin_biome, it.origin_biome)
                label_col = (215, 170, 80)
            elif cat == "herb":
                from herbalism import POTION_COLORS as _HCOL
                from items import ITEMS as _HITEMS
                p_col3 = _HCOL.get(key, (70, 175, 140))
                pygame.draw.rect(self.screen, (10, 28, 24) if selected else (8, 18, 15), rect)
                pygame.draw.rect(self.screen, p_col3, rect, 3 if selected else 2)
                img = pygame.Surface((58, 58), pygame.SRCALPHA)
                img.fill((0, 0, 0, 0))
                pygame.draw.circle(img, p_col3, (29, 34), 18)
                pygame.draw.rect(img, p_col3, (25, 8, 8, 16))
                pygame.draw.rect(img, (min(255, p_col3[0]+60), min(255, p_col3[1]+60), min(255, p_col3[2]+60)), (26, 28, 6, 8))
                label     = _HITEMS.get(key, {}).get("name", key)
                label_col = p_col3
            elif cat == "textile":
                from textiles import DYE_FAMILY_COLORS as _TDFC, DYE_FAMILY_DISPLAY as _TDFD
                it = getattr(player, "textiles", [])[key]
                dye_col = tuple(_TDFC.get(it.dye_family, _TDFC["natural"]))
                bg_col = (28, 16, 35) if selected else (18, 10, 22)
                pygame.draw.rect(self.screen, bg_col, rect)
                pygame.draw.rect(self.screen, dye_col, rect, 3 if selected else 2)
                img = pygame.Surface((58, 58), pygame.SRCALPHA)
                img.fill((0, 0, 0, 0))
                # Simple fabric swatch icon
                pygame.draw.rect(img, dye_col, (6, 6, 46, 46))
                pygame.draw.rect(img, (min(255, dye_col[0]+50), min(255, dye_col[1]+50), min(255, dye_col[2]+50)), (6, 6, 46, 46), 2)
                sc = {"thread": "T", "dyed": "D", "woven": "W"}.get(it.state, "?")
                sc_s = self.small.render(sc, True, (255, 255, 255))
                img.blit(sc_s, (img.get_width() - sc_s.get_width() - 2, 2))
                label = _TDFD.get(it.dye_family, it.dye_family)
                label_col = dye_col
            elif cat == "tea":
                from tea import TEA_TYPE_COLORS as _TTC, BIOME_DISPLAY_NAMES as _TBDN
                it = getattr(player, "tea_leaves", [])[key]
                tc3 = _TTC.get(it.tea_type, (65, 160, 75)) if it.tea_type else (65, 120, 55)
                bg_col = (18, 38, 18) if selected else (10, 24, 12)
                pygame.draw.rect(self.screen, bg_col, rect)
                pygame.draw.rect(self.screen, tc3, rect, 3 if selected else 2)
                img = pygame.Surface((58, 58), pygame.SRCALPHA)
                img.fill((0, 0, 0, 0))
                # Simple leaf icon
                pygame.draw.ellipse(img, tc3, (8, 12, 42, 34))
                pygame.draw.line(img, (min(255, tc3[0]+40), min(255, tc3[1]+40), min(255, tc3[2]+40)),
                                 (29, 14), (29, 44), 2)
                state_char = {"raw": "R", "withered": "W", "oxidized": "O", "brewed": "B", "blended": "X"}.get(it.state, "?")
                sc_s = self.small.render(state_char, True, (200, 240, 180))
                img.blit(sc_s, (img.get_width() - sc_s.get_width() - 2, 2))
                label = _TBDN.get(it.origin_biome, it.origin_biome)
                label_col = (130, 215, 140)
            elif cat == "jewelry":
                from jewelry import JEWELRY_TYPES as _JT, calculate_value
                piece = getattr(player, "jewelry", [])[key]
                jcol = (180, 150, 60)
                pygame.draw.rect(self.screen, (30, 24, 8) if selected else (20, 16, 6), rect)
                pygame.draw.rect(self.screen, jcol, rect, 3 if selected else 2)
                img = pygame.Surface((58, 58), pygame.SRCALPHA)
                img.fill((0, 0, 0, 0))
                # Draw a tiny jewelry silhouette in the icon
                jtype = piece.jewelry_type
                cx_i, cy_i = 29, 29
                if jtype == "ring":
                    pygame.draw.circle(img, jcol, (cx_i, cy_i), 18, 3)
                elif jtype == "crown":
                    pts = [(cx_i-18,cy_i+4),(cx_i-9,cy_i-10),(cx_i,cy_i-4),(cx_i+9,cy_i-10),(cx_i+18,cy_i+4)]
                    pygame.draw.lines(img, jcol, False, pts, 3)
                elif jtype == "pendant":
                    pygame.draw.polygon(img, jcol, [(cx_i,cy_i-14),(cx_i+12,cy_i),(cx_i,cy_i+14),(cx_i-12,cy_i)])
                elif jtype == "necklace":
                    import math
                    pygame.draw.arc(img, jcol, (cx_i-16,cy_i-16,32,32), 0, math.pi, 3)
                else:  # bracelet
                    pygame.draw.circle(img, jcol, (cx_i, cy_i), 16, 4)
                # Slot dots
                for si in range(min(piece.slot_count, 5)):
                    dot_x = 6 + si * 10
                    dot_col = (220, 190, 80) if (si < len(piece.slots) and piece.slots[si] is not None) else (70, 60, 28)
                    pygame.draw.circle(img, dot_col, (dot_x, 52), 4)
                label = piece.custom_name
                label_col = jcol
                if selected:
                    self._jw_detail_jewelry = piece
            elif cat == "sculpture":
                from sculpture import SCULPTABLE_MINERALS, MINERAL_COLORS
                sc = getattr(player, "sculptures_created", [])[key]
                sc_col = tuple(sc.color) if sc.color else (190, 180, 155)
                pygame.draw.rect(self.screen, (35, 30, 20) if selected else (22, 18, 12), rect)
                pygame.draw.rect(self.screen, sc_col, rect, 3 if selected else 2)
                # Tiny grid preview
                img = pygame.Surface((58, 58), pygame.SRCALPHA)
                img.fill((0, 0, 0, 0))
                rows = len(sc.grid)
                cw = max(1, 58 // 8)
                ch = max(1, 58 // rows)
                hi = tuple(min(255, c + 20) for c in sc_col)
                lo = tuple(max(0,   c - 25) for c in sc_col)
                for ri, row in enumerate(sc.grid):
                    for ci, filled in enumerate(row):
                        px2 = ci * cw
                        py2 = ri * ch
                        col2 = (hi if ci % 2 == 0 else lo) if filled else (18, 14, 10)
                        pygame.draw.rect(img, col2, (px2, py2, cw, ch))
                mineral_name = SCULPTABLE_MINERALS.get(sc.mineral, "Stone")
                label = f"{mineral_name} {sc.height}H"
                label_col = sc_col
            elif cat == "tapestry":
                from tapestry import WEAVABLE_THREADS
                tp = getattr(player, "tapestries_created", [])[key]
                tp_col = tuple(tp.color) if tp.color else (210, 195, 160)
                pygame.draw.rect(self.screen, (32, 24, 14) if selected else (20, 14, 8), rect)
                pygame.draw.rect(self.screen, tp_col, rect, 3 if selected else 2)
                img = pygame.Surface((58, 58), pygame.SRCALPHA)
                img.fill((0, 0, 0, 0))
                rows = len(tp.grid)
                cw = max(1, 58 // 16)
                ch = max(1, 58 // rows)
                hi = tuple(min(255, c + 22) for c in tp_col)
                lo = tuple(max(0,   c - 28) for c in tp_col)
                for ri, row in enumerate(tp.grid):
                    for ci, filled in enumerate(row):
                        px2 = ci * cw
                        py2 = ri * ch
                        col2 = (hi if ri % 2 == 0 else lo) if filled else (14, 10, 6)
                        pygame.draw.rect(img, col2, (px2, py2, cw, ch))
                thread_name = WEAVABLE_THREADS.get(tp.thread, "Thread")
                label = f"{thread_name} {tp.height}H"
                label_col = tp_col
            elif cat == "pottery":
                from pottery import CLAY_BIOME_PROFILES, GLAZE_TYPES
                piece = getattr(player, "pottery_pieces", [])[key]
                clay_col = (155, 105, 75)
                if piece.glaze_type and piece.glaze_type in GLAZE_TYPES:
                    gdata = GLAZE_TYPES[piece.glaze_type]
                    border_col = gdata["color"]
                else:
                    border_col = (160, 110, 80)
                pygame.draw.rect(self.screen, (40, 25, 10) if selected else (25, 15, 6), rect)
                pygame.draw.rect(self.screen, border_col, rect, 3 if selected else 2)
                img = pygame.Surface((58, 58), pygame.SRCALPHA)
                img.fill((0, 0, 0, 0))
                # Silhouette from profile
                if piece.profile:
                    prof = piece.profile
                    row_h = max(1, 50 // len(prof))
                    cx_i, ty = 29, 4
                    for ri, rad in enumerate(prof):
                        w = max(2, int(rad * 3.5))
                        pygame.draw.rect(img, clay_col, (cx_i - w, ty + ri * row_h, w * 2, row_h - 1))
                label = f"{piece.shape.title()} ({piece.firing_level[:3]})"
                label_col = (210, 160, 110)
            elif cat == "salt":
                it = getattr(player, "salt_crystals", [])[key]
                s_col = SALT_OUTPUT_COLORS.get(f"{it.refine_grade or 'coarse'}_salt", (235, 232, 215))
                pygame.draw.rect(self.screen, (35, 33, 30) if selected else (22, 20, 18), rect)
                pygame.draw.rect(self.screen, s_col, rect, 3 if selected else 2)
                img = pygame.Surface((58, 58), pygame.SRCALPHA)
                img.fill((0, 0, 0, 0))
                # Crystal polygon icon
                cx_i, cy_i = 29, 26
                pts = [(cx_i, cy_i-18), (cx_i+12, cy_i-6), (cx_i+10, cy_i+12),
                       (cx_i, cy_i+18), (cx_i-10, cy_i+12), (cx_i-12, cy_i-6)]
                pygame.draw.polygon(img, s_col, pts)
                pygame.draw.polygon(img, (255, 255, 255, 80), pts, 1)
                state_char = {"raw": "R", "dried": "D", "finished": "F"}.get(it.state, "?")
                sc_s = self.small.render(state_char, True, (200, 198, 190))
                img.blit(sc_s, (img.get_width() - sc_s.get_width() - 2, 2))
                label = SALT_BIOME_NAMES.get(it.origin_biome, it.origin_biome)
                label_col = (210, 205, 185)
            elif cat == "weapon":
                from weapons import MATERIAL_PROFILES, WEAPON_TYPES, quality_tier
                it     = getattr(player, "crafted_weapons", [])[key]
                mat_col = MATERIAL_PROFILES.get(it.material, {}).get("color", (180, 170, 155))
                pygame.draw.rect(self.screen, (30, 24, 16) if selected else (20, 16, 10), rect)
                pygame.draw.rect(self.screen, mat_col, rect, 3 if selected else 2)
                img = pygame.Surface((58, 58), pygame.SRCALPHA)
                img.fill((0, 0, 0, 0))
                # Simple sword icon: vertical blade + cross guard
                cx_i, cy_i = 29, 29
                pygame.draw.line(img, mat_col, (cx_i, 4), (cx_i, 44), 3)
                pygame.draw.line(img, mat_col, (cx_i - 10, 32), (cx_i + 10, 32), 3)
                pygame.draw.circle(img, mat_col, (cx_i, 50), 3)
                label = WEAPON_TYPES[it.weapon_type]["name"]
                label_col = mat_col
                tier_s = self.small.render(quality_tier(it.quality), True, mat_col)
                img.blit(tier_s, (2, 2))
            else:  # mushroom
                count = player.mushrooms_found.get(key, 0)
                pygame.draw.rect(self.screen, (40, 36, 20) if selected else (25, 22, 12), rect)
                pygame.draw.rect(self.screen, (175, 158, 68) if selected else (100, 88, 38), rect,
                                 3 if selected else 2)
                img = render_mushroom_preview(key, 58)
                label = _MUSHROOM_NAMES.get(key, BLOCKS[key]["name"])
                label_col = (195, 178, 108)
                if count > 1:
                    cnt_s = self.small.render(f"×{count}", True, (220, 200, 120))
                    self.screen.blit(cnt_s, (x + CELL - cnt_s.get_width() - 2, y + 2))

            self.screen.blit(img, (x + (CELL - 58) // 2, y + (CELL - 58) // 2 - 6))
            type_s = self.small.render(self._fit_label(label, CELL - 4), True, label_col)
            self.screen.blit(type_s, (x + CELL // 2 - type_s.get_width() // 2, y + CELL - 14))

        if detail_x is None:
            return

        sel_cat, sel_key = self._unified_selected
        dx, dy2 = detail_x, gy0
        dw = SCREEN_W - dx - 8
        dh = SCREEN_H - gy0 - 10
        iy = [dy2 + 96]

        def dlabel(text, color=(220, 220, 200)):
            s = self.small.render(text, True, color)
            self.screen.blit(s, (dx + 8, iy[0]))
            iy[0] += 15

        def stat_bar(label, val, bar_col, lbl_col=(160, 160, 160)):
            ls = self.small.render(label, True, lbl_col)
            self.screen.blit(ls, (dx + 8, iy[0]))
            bx2 = dx + 80
            bw = dw - 90
            pygame.draw.rect(self.screen, (35, 35, 45), (bx2, iy[0] + 2, bw, 8))
            pygame.draw.rect(self.screen, bar_col, (bx2, iy[0] + 2, int(bw * val), 8))
            vs = self.small.render(f"{val:.2f}", True, (180, 180, 180))
            self.screen.blit(vs, (bx2 + bw + 4, iy[0]))
            iy[0] += 16

        if sel_cat == "rock":
            rock = player.rocks[sel_key]
            pygame.draw.rect(self.screen, (22, 22, 32), (dx, dy2, dw, dh))
            pygame.draw.rect(self.screen, RARITY_COLORS[rock.rarity], (dx, dy2, dw, dh), 2)
            self.screen.blit(render_rock(rock, 80), (dx + dw // 2 - 40, dy2 + 8))
            dlabel(rock.base_type.replace("_", " ").title(), (240, 200, 100))
            dlabel(RARITY_LABEL[rock.rarity], RARITY_COLORS[rock.rarity])
            dlabel(f"Size: {rock.size.title()}")
            dlabel(f"Found at: {rock.depth_found}m depth")
            dlabel(f"Pattern: {rock.pattern}")
            iy[0] += 4
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

        elif sel_cat == "flower":
            flower = player.wildflowers[sel_key]
            pygame.draw.rect(self.screen, (15, 25, 15), (dx, dy2, dw, dh))
            pygame.draw.rect(self.screen, RARITY_COLORS[flower.rarity], (dx, dy2, dw, dh), 2)
            self.screen.blit(render_wildflower(flower, 80), (dx + dw // 2 - 40, dy2 + 8))
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

        elif sel_cat == "fossil":
            fossil = player.fossils[sel_key]
            pygame.draw.rect(self.screen, (22, 18, 12), (dx, dy2, dw, dh))
            pygame.draw.rect(self.screen, RARITY_COLORS[fossil.rarity], (dx, dy2, dw, dh), 2)
            self.screen.blit(render_fossil(fossil, 80), (dx + dw // 2 - 40, dy2 + 8))
            dlabel(fossil.fossil_type.replace("_", " ").title(), (235, 205, 130))
            dlabel(RARITY_LABEL[fossil.rarity], RARITY_COLORS[fossil.rarity])
            dlabel(f"Age: {fossil.age.title()}", FOSSIL_AGE_COLORS.get(fossil.age, (180, 160, 120)))
            dlabel(f"Size: {fossil.size.title()}")
            dlabel(f"Found at: {fossil.depth_found}m depth")
            dlabel(f"Pattern: {fossil.pattern.title()}")
            iy[0] += 4
            stat_bar("Clarity", fossil.clarity, (100, 180, 200), (160, 145, 110))
            stat_bar("Detail",  fossil.detail,  (180, 155, 80),  (160, 145, 110))
            iy[0] += 4
            if fossil.specials:
                dlabel("Traits:", (210, 185, 120))
                for sp in fossil.specials:
                    dlabel(f"  {sp.replace('_', ' ').title()}", (220, 195, 105))
                    dlabel(f"    {FOSSIL_SPECIAL_DESCS.get(sp, '')}", (145, 130, 90))
            else:
                dlabel("No special traits.", (90, 82, 60))

        elif sel_cat == "gem":
            gem = player.gems[sel_key]
            rar_col = GEM_RARITY_COLORS.get(gem.rarity, (120, 120, 120))
            pygame.draw.rect(self.screen, (14, 22, 20), (dx, dy2, dw, dh))
            pygame.draw.rect(self.screen, rar_col, (dx, dy2, dw, dh), 2)
            preview = render_rough_gem(gem, 100) if gem.state == "rough" else render_gem(gem, 100)
            self.screen.blit(preview, (dx + dw // 2 - 50, dy2 + 8))
            ty = dy2 + 116
            name_s = self.font.render(gem.gem_type.replace("_", " ").title(), True, rar_col)
            self.screen.blit(name_s, (dx + dw // 2 - name_s.get_width() // 2, ty)); ty += 22

            def grow(lbl, val, col=(155, 200, 185)):
                nonlocal ty
                l_s = self.small.render(f"{lbl}:", True, (80, 118, 108))
                v_s = self.small.render(str(val), True, col)
                self.screen.blit(l_s, (dx + 10, ty))
                self.screen.blit(v_s, (dx + dw - v_s.get_width() - 8, ty))
                ty += 17

            grow("Rarity", gem.rarity.title(), rar_col)
            grow("Size", gem.size.title())
            grow("State", gem.state.title(), (255, 200, 80) if gem.state == "rough" else (100, 220, 180))
            grow("Cut", GEM_CUT_DESCS.get(gem.cut, gem.cut).split(" —")[0])
            if gem.state == "cut":
                grow("Clarity", gem.clarity,
                     (255, 220, 80) if gem.clarity in ("FL", "VVS") else (155, 200, 185))
                grow("Inclusion", gem.inclusion.replace("_", " ").title())
                if gem.optical_effect != "none":
                    grow("Optical", gem.optical_effect.replace("_", " ").title(), (200, 160, 255))
            else:
                unk = self.small.render("Hidden until cut at Gem Cutter", True, (80, 100, 95))
                self.screen.blit(unk, (dx + dw // 2 - unk.get_width() // 2, ty)); ty += 17
            grow("Crystal", gem.crystal_system.title())
            grow("Depth", f"{gem.depth_found}m")

        elif sel_cat == "bird":
            from birds import SPECIES_BY_ID
            sp_cls  = SPECIES_BY_ID.get(sel_key)
            obs     = player.birds_observed.get(sel_key, {})
            rarity_bird_cols = {"common": (120, 170, 120), "uncommon": (100, 170, 220), "rare": (180, 120, 230)}
            rar_col = rarity_bird_cols.get(sp_cls.RARITY if sp_cls else "common", (120, 170, 120))
            pygame.draw.rect(self.screen, (10, 20, 32), (dx, dy2, dw, dh))
            pygame.draw.rect(self.screen, rar_col, (dx, dy2, dw, dh), 2)
            # Bird icon at large scale
            if sp_cls:
                bw2, bh2 = sp_cls.W * 4, sp_cls.H * 4
                bird_icon = pygame.Surface((bw2, bh2), pygame.SRCALPHA)
                bird_icon.fill((0, 0, 0, 0))
                pygame.draw.ellipse(bird_icon, sp_cls.WING_COLOR, (0, bh2 // 3, bw2, bh2 // 2))
                pygame.draw.ellipse(bird_icon, sp_cls.BODY_COLOR,
                                    (bw2 // 6, bh2 // 3, bw2 * 2 // 3, bh2 // 2))
                pygame.draw.circle(bird_icon, sp_cls.HEAD_COLOR,
                                   (bw2 - bw2 // 5, bh2 // 4), bh2 // 5)
                pygame.draw.ellipse(bird_icon, sp_cls.ACCENT_COLOR,
                                    (bw2 // 6, bh2 // 3 + bh2 // 8, bw2 // 2, bh2 // 5))
                self.screen.blit(bird_icon, (dx + dw // 2 - bw2 // 2, dy2 + 6))
            dlabel(sel_key.replace("_", " ").title(), (200, 230, 255))
            dlabel(sp_cls.RARITY.title() if sp_cls else "", rar_col)
            dlabel(f"Times observed: {obs.get('count', 0)}", (160, 220, 180))
            dlabel(f"First seen: {obs.get('biome', '?').replace('_', ' ').title()}", (140, 180, 210))
            if sp_cls and sp_cls.BIOMES:
                dlabel(f"Habitat: {', '.join(b.replace('_',' ').title() for b in sp_cls.BIOMES[:2])}", (140, 170, 140))
            else:
                dlabel("Habitat: Widespread", (140, 170, 140))
            dlabel("Flock species" if (sp_cls and sp_cls.IS_FLOCK) else "Solitary", (170, 185, 200))
        elif sel_cat == "fish":
            fish = player.fish_caught[sel_key]
            fdata = FISH_TYPES.get(fish.species, {})
            rar_col = FISH_RARITY_COLORS.get(fish.rarity, (120, 120, 180))
            pygame.draw.rect(self.screen, (10, 18, 28), (dx, dy2, dw, dh))
            pygame.draw.rect(self.screen, rar_col, (dx, dy2, dw, dh), 2)
            self.screen.blit(render_fish(fish, 80), (dx + dw // 2 - 40, dy2 + 6))
            dlabel(fdata.get("name", fish.species.replace("_", " ").title()), (200, 230, 255))
            dlabel(FISH_RARITY_LABEL.get(fish.rarity, fish.rarity.title()), rar_col)
            dlabel(f"Weight: {fish.weight_kg:.2f} kg", (160, 200, 230))
            dlabel(f"Length: {fish.length_cm} cm", (140, 185, 215))
            dlabel(f"Pattern: {fish.pattern.title()}", (140, 170, 200))
            dlabel(f"Habitat: {fish.habitat.title()}", (120, 165, 190))
            dlabel(f"Found in: {fish.biome_found.replace('_', ' ').title()}", (120, 155, 180))
            iy[0] += 4
            desc = fdata.get("description", "")
            if desc:
                # Word-wrap description to panel width
                words = desc.split()
                line = ""
                for w in words:
                    test = (line + " " + w).strip()
                    if self.small.size(test)[0] <= dw - 16:
                        line = test
                    else:
                        if line:
                            dlabel(line, (140, 150, 165))
                        line = w
                if line:
                    dlabel(line, (140, 150, 165))
        elif sel_cat == "coffee":
            bean = player.coffee_beans[sel_key]
            roast_col = ROAST_COLORS.get(bean.roast_level, (80, 50, 20))
            pygame.draw.rect(self.screen, (20, 12, 5), (dx, dy2, dw, dh))
            pygame.draw.rect(self.screen, roast_col, (dx, dy2, dw, dh), 2)
            # Draw bean preview
            bean_surf = pygame.Surface((80, 80), pygame.SRCALPHA)
            bean_surf.fill((0, 0, 0, 0))
            pygame.draw.ellipse(bean_surf, roast_col, (10, 5, 60, 70))
            lc = (max(0, roast_col[0] - 50), max(0, roast_col[1] - 50), max(0, roast_col[2] - 50))
            pygame.draw.line(bean_surf, lc, (40, 8), (40, 72), 3)
            self.screen.blit(bean_surf, (dx + dw // 2 - 40, dy2 + 6))
            dlabel(BIOME_DISPLAY_NAMES.get(bean.origin_biome, bean.origin_biome) + " " + bean.variety.title(), (220, 160, 80))
            dlabel(f"State: {bean.state.title()}", roast_col)
            dlabel(f"Roast: {ROAST_LEVEL_DESCS.get(bean.roast_level, bean.roast_level)}", roast_col)
            if bean.roast_quality > 0:
                stars = "★" * round(bean.roast_quality * 5)
                dlabel(f"Quality: {stars}", (220, 190, 60))
            if bean.flavor_notes:
                dlabel(f"Flavour Notes:", (180, 140, 80))
                for note in bean.flavor_notes:
                    dlabel(f"  • {note.title()}", (210, 175, 110))
            iy[0] += 4
            stat_bar("Acidity",   bean.acidity,   (180, 220, 80))
            stat_bar("Body",      bean.body,       (140, 90,  40))
            stat_bar("Sweetness", bean.sweetness,  (220, 180, 60))
            stat_bar("Earthiness",bean.earthiness, (130, 100, 50))
            stat_bar("Brightness",bean.brightness, (230, 200, 80))
        elif sel_cat == "wine":
            grape = getattr(player, "wine_grapes", [])[sel_key]
            style_col = WINE_STYLE_COLORS.get(grape.style, (175, 90, 115))
            pygame.draw.rect(self.screen, (18, 8, 14), (dx, dy2, dw, dh))
            pygame.draw.rect(self.screen, style_col, (dx, dy2, dw, dh), 2)
            grape_surf = pygame.Surface((80, 80), pygame.SRCALPHA)
            grape_surf.fill((0, 0, 0, 0))
            for gx4, gy4 in [(26, 12), (46, 12), (16, 28), (36, 28), (56, 28), (26, 44), (46, 44)]:
                pygame.draw.circle(grape_surf, style_col, (gx4, gy4), 10)
            pygame.draw.line(grape_surf, (100, 150, 70), (40, 56), (40, 74), 3)
            self.screen.blit(grape_surf, (dx + dw // 2 - 40, dy2 + 4))
            variety_name = WINE_VARIETY_NAMES.get(grape.variety, grape.variety.replace("_", " ").title())
            biome_name = WINE_BIOME_NAMES.get(grape.origin_biome, grape.origin_biome.replace("_", " ").title())
            dlabel(f"{biome_name} {variety_name}", (235, 165, 185))
            dlabel(f"State: {grape.state.title()}", style_col)
            if grape.style:
                dlabel(f"Style: {grape.style.title()}", style_col)
            if grape.crush_style:
                dlabel(f"Crush: {grape.crush_style.replace('_', ' ').title()}", (200, 160, 175))
            if grape.yeast:
                dlabel(f"Yeast: {grape.yeast.replace('_', ' ').title()}", (190, 155, 170))
            if grape.vessel:
                dlabel(f"Vessel: {grape.vessel.title()}", (185, 150, 165))
            if grape.press_quality > 0:
                stars = "★" * round(grape.press_quality * 5)
                dlabel(f"Press Quality: {stars}", (215, 175, 190))
            if grape.ferment_quality > 0:
                stars = "★" * round(grape.ferment_quality * 5)
                dlabel(f"Ferment Quality: {stars}", (215, 175, 190))
            if grape.flavor_notes:
                dlabel("Flavour Notes:", (195, 140, 155))
                for note in grape.flavor_notes:
                    dlabel(f"  • {note.title()}", (220, 170, 185))
            iy[0] += 4
            stat_bar("Sweetness", grape.sweetness,  (230, 175, 80))
            stat_bar("Acidity",   grape.acidity,    (180, 220, 80))
            stat_bar("Tannin",    grape.tannin,     (100,  60, 40))
            stat_bar("Body",      grape.body,       (140,  60, 80))
            stat_bar("Aromatics", grape.aromatics,  (200, 140, 220))
            if grape.alcohol > 0:
                stat_bar("Alcohol",   grape.alcohol,    (220, 100,  60))
            if grape.complexity > 0:
                stat_bar("Complexity",grape.complexity, (175, 130, 210))
        elif sel_cat == "spirit":
            from spirits import SPIRIT_TYPE_COLORS, SPIRIT_TYPE_DESCS, SPIRIT_BUFFS, BUFF_DESCS as SPIRIT_BUFF_DESCS
            from spirits import BIOME_DISPLAY_NAMES as SPIRIT_BIOME_NAMES
            spirit = getattr(player, "spirits", [])[sel_key]
            sc2 = SPIRIT_TYPE_COLORS.get(spirit.spirit_type, (185, 140, 70))
            pygame.draw.rect(self.screen, (18, 12, 5), (dx, dy2, dw, dh))
            pygame.draw.rect(self.screen, sc2, (dx, dy2, dw, dh), 2)
            # Draw simple bottle icon
            bot_surf = pygame.Surface((80, 80), pygame.SRCALPHA)
            bot_surf.fill((0, 0, 0, 0))
            pygame.draw.rect(bot_surf, sc2, (28, 30, 24, 42))
            pygame.draw.rect(bot_surf, sc2, (34, 18, 12, 16))
            pygame.draw.rect(bot_surf, (min(255, sc2[0] + 60), min(255, sc2[1] + 60), min(255, sc2[2] + 60)), (30, 32, 8, 8))
            self.screen.blit(bot_surf, (dx + dw // 2 - 40, dy2 + 4))
            bm3 = SPIRIT_BIOME_NAMES.get(spirit.origin_biome, spirit.origin_biome.replace("_", " ").title())
            dlabel(f"{bm3} {spirit.spirit_type.title()}", sc2)
            dlabel(f"State: {spirit.state.title()}", sc2)
            dlabel(SPIRIT_TYPE_DESCS.get(spirit.spirit_type, ""), (190, 165, 100))
            if spirit.grain_type:
                dlabel(f"Source: {spirit.grain_type.replace('_', ' ').title()}", (170, 145, 80))
            if spirit.barrel_type:
                dlabel(f"Barrel: {spirit.barrel_type.replace('_', ' ').title()}", (185, 150, 80))
            if spirit.age_duration:
                dlabel(f"Aged: {spirit.age_duration.title()}", (175, 140, 70))
            if spirit.cut_quality > 0:
                stars = "★" * round(spirit.cut_quality * 5)
                dlabel(f"Cut Quality: {stars}", (210, 175, 90))
            if spirit.age_quality > 0:
                stars = "★" * round(spirit.age_quality * 5)
                dlabel(f"Age Quality: {stars}", (220, 185, 100))
            buff_k = SPIRIT_BUFFS.get(spirit.spirit_type)
            if buff_k:
                dlabel(f"Buff: {SPIRIT_BUFF_DESCS.get(buff_k, buff_k)}", (130, 210, 130))
            if spirit.flavor_notes:
                dlabel("Notes:", (185, 155, 80))
                for note in spirit.flavor_notes:
                    dlabel(f"  • {note.title()}", (215, 180, 110))
            iy[0] += 4
            stat_bar("Grain Char.",  spirit.grain_character, (185, 155, 80))
            stat_bar("Sweetness",    spirit.sweetness,        (220, 180, 60))
            stat_bar("Spice",        spirit.spice,            (220, 120, 60))
            stat_bar("Smokiness",    spirit.smokiness,        (140, 130, 120))
            stat_bar("Smoothness",   spirit.smoothness,       (200, 200, 240))
        elif sel_cat == "tea":
            from tea import TEA_TYPE_COLORS as _TTC2, TEA_TYPE_DESCS, TEA_TYPE_BUFFS
            from tea import BUFF_DESCS as TEA_BUFF_DESCS, BIOME_DISPLAY_NAMES as _TBN2
            from tea import WITHER_METHODS, VARIETY_DISPLAY_NAMES, AGE_DURATIONS
            leaf = getattr(player, "tea_leaves", [])[sel_key]
            tc2 = _TTC2.get(leaf.tea_type, (65, 160, 75)) if leaf.tea_type else (65, 120, 55)
            pygame.draw.rect(self.screen, (10, 24, 12), (dx, dy2, dw, dh))
            pygame.draw.rect(self.screen, tc2, (dx, dy2, dw, dh), 2)
            # Leaf icon
            leaf_surf = pygame.Surface((80, 80), pygame.SRCALPHA)
            leaf_surf.fill((0, 0, 0, 0))
            pygame.draw.ellipse(leaf_surf, tc2, (8, 16, 64, 48))
            pygame.draw.line(leaf_surf, (min(255, tc2[0]+50), min(255, tc2[1]+50), min(255, tc2[2]+50)),
                             (40, 18), (40, 62), 2)
            self.screen.blit(leaf_surf, (dx + dw // 2 - 40, dy2 + 4))
            bm_leaf = _TBN2.get(leaf.origin_biome, leaf.origin_biome.replace("_", " ").title())
            var_leaf = VARIETY_DISPLAY_NAMES.get(leaf.variety, leaf.variety)
            dlabel(f"{bm_leaf} — {var_leaf}", tc2)
            dlabel(f"State: {leaf.state.title()}", tc2)
            if leaf.tea_type:
                dlabel(TEA_TYPE_DESCS.get(leaf.tea_type, leaf.tea_type), (180, 230, 160))
                buff_k = TEA_TYPE_BUFFS.get(leaf.tea_type)
                if buff_k:
                    dlabel(f"Buff: {TEA_BUFF_DESCS.get(buff_k, buff_k)}", (130, 215, 140))
            if leaf.wither_method:
                wm = WITHER_METHODS.get(leaf.wither_method, {})
                dlabel(f"Wither: {wm.get('label', leaf.wither_method)}", (190, 210, 160))
            if leaf.age_duration:
                ad = AGE_DURATIONS.get(leaf.age_duration, {})
                dlabel(f"Aged: {ad.get('label', leaf.age_duration)}", (175, 155, 70))
            if leaf.steep_quality > 0:
                stars = "★" * round(leaf.steep_quality * 5)
                dlabel(f"Quality: {stars}", (220, 200, 80))
            if leaf.flavor_notes:
                dlabel("Notes:", (160, 210, 130))
                for note in leaf.flavor_notes:
                    dlabel(f"  • {note.title()}", (190, 235, 170))
            iy[0] += 4
            stat_bar("Astringency", leaf.astringency, (180, 120,  60))
            stat_bar("Floral",      leaf.floral,      (220, 180, 230))
            stat_bar("Vegetal",     leaf.vegetal,     (120, 195,  90))
            stat_bar("Earthiness",  leaf.earthiness,  (140, 110,  70))
            stat_bar("Sweetness",   leaf.sweetness,   (210, 185,  80))
        elif sel_cat == "herb":
            from herbalism import POTION_COLORS as _PC2, POTION_DESCS as _PD2, RECIPES as _PR2
            from herbalism import TIER_LABELS, INGREDIENT_DISPLAY_NAMES
            from items import ITEMS as _HI2
            p_col4 = _PC2.get(sel_key, (70, 175, 140))
            pygame.draw.rect(self.screen, (10, 24, 20), (dx, dy2, dw, dh))
            pygame.draw.rect(self.screen, p_col4, (dx, dy2, dw, dh), 2)
            potion_surf = pygame.Surface((80, 80), pygame.SRCALPHA)
            potion_surf.fill((0, 0, 0, 0))
            pygame.draw.circle(potion_surf, p_col4, (40, 48), 26)
            pygame.draw.rect(potion_surf, p_col4, (34, 12, 12, 20))
            pygame.draw.circle(potion_surf, (min(255,p_col4[0]+60), min(255,p_col4[1]+60), min(255,p_col4[2]+60)), (40, 38), 8)
            self.screen.blit(potion_surf, (dx + dw // 2 - 40, dy2 + 4))
            p_name = _HI2.get(sel_key, {}).get("name", sel_key)
            dlabel(p_name, p_col4)
            dlabel(_PD2.get(sel_key, ""), (180, 230, 200))
            recipe4 = _PR2.get(sel_key)
            if recipe4:
                dlabel(f"Tier: {TIER_LABELS.get(recipe4['tier'], recipe4['tier'])}", (160, 210, 170))
                dlabel("Recipe:", (130, 185, 150))
                for ing_k, ing_v in recipe4["ingredients"].items():
                    dlabel(f"  {INGREDIENT_DISPLAY_NAMES.get(ing_k, ing_k)} ×{ing_v}", (140, 235, 200))
            qty = player.inventory.get(sel_key, 0)
            dlabel(f"In inventory: ×{qty}", (100, 160, 130))
        elif sel_cat == "textile":
            from textiles import DYE_FAMILY_COLORS as _TDFC2, DYE_FAMILY_DISPLAY as _TDFD2, OUTPUT_DISPLAY as _TOD2
            from textiles import GARMENT_BUFFS as _TGB2, GARMENT_BUFF_DESCS as _TGBD2, get_garment_bonus as _tgb_fn
            it = getattr(player, "textiles", [])[sel_key]
            dye_col2 = tuple(_TDFC2.get(it.dye_family, _TDFC2["natural"]))
            pygame.draw.rect(self.screen, (18, 10, 22), (dx, dy2, dw, dh))
            pygame.draw.rect(self.screen, dye_col2, (dx, dy2, dw, dh), 2)
            swatch = pygame.Surface((64, 64))
            swatch.fill(dye_col2)
            pygame.draw.rect(swatch, (0, 0, 0), (0, 0, 64, 64), 2)
            self.screen.blit(swatch, (dx + dw // 2 - 32, dy2 + 6))
            dlabel(_TOD2.get(it.output_type, it.output_type), dye_col2)
            dlabel(f"{it.fiber_type.title()} · {_TDFD2.get(it.dye_family,'Natural')}", (200, 180, 215))
            dlabel(f"Texture: {it.texture.title()}", (175, 155, 200))
            dlabel(f"State: {it.state.title()}", (150, 130, 175))
            dlabel(f"Quality: {it.quality:.0%}", (180, 235, 190))
            dlabel(f"Softness: {it.softness:.0%}  Luster: {it.luster:.0%}", (160, 215, 175))
            if it.state == "woven":
                dlabel(f"Pattern: {it.pattern_quality:.0%}", (160, 215, 175))
                stat = _TGB2.get(it.output_type)
                if stat:
                    bonus = _tgb_fn(it)
                    dlabel(_TGBD2[stat].format(bonus * 100), (120, 220, 140))
        elif sel_cat == "salt":
            it = getattr(player, "salt_crystals", [])[sel_key]
            s_col = SALT_OUTPUT_COLORS.get(f"{it.refine_grade or 'coarse'}_salt", (235, 232, 215))
            pygame.draw.rect(self.screen, (22, 20, 18), (dx, dy2, dw, dh))
            pygame.draw.rect(self.screen, s_col, (dx, dy2, dw, dh), 2)
            # Crystal icon
            cx_p, cy_p = dx + dw // 2, dy2 + 46
            pts = [(cx_p, cy_p-36), (cx_p+24, cy_p-12), (cx_p+20, cy_p+24),
                   (cx_p, cy_p+36), (cx_p-20, cy_p+24), (cx_p-24, cy_p-12)]
            pygame.draw.polygon(self.screen, s_col, pts)
            pygame.draw.polygon(self.screen, (255, 255, 255), pts, 2)
            dlabel(SALT_BIOME_NAMES.get(it.origin_biome, it.origin_biome) + " Salt", s_col)
            dlabel(f"Variety: {it.variety.title()}", (200, 195, 175))
            dlabel(f"State: {it.state.title()}", (180, 178, 160))
            if it.refine_grade:
                dlabel(f"Grade: {it.refine_grade.replace('_', ' ').title()}", s_col)
            if it.evap_method:
                dlabel(f"Evap: {it.evap_method.replace('_', ' ').title()}", (175, 170, 155))
            if it.flavor_notes:
                dlabel("Notes:", (190, 185, 160))
                for note in it.flavor_notes:
                    dlabel(f"  • {note.title()}", (210, 205, 185))
            iy[0] += 4
            stat_bar("Purity",    it.purity,    (235, 232, 215))
            stat_bar("Salinity",  it.salinity,  (140, 195, 215))
            stat_bar("Mineral",   it.mineral,   (175, 165, 130))
            stat_bar("Moisture",  it.moisture,  ( 90, 160, 200))
            stat_bar("Grain Size",it.grain_size,(200, 185, 145))
        elif sel_cat == "weapon":
            from weapons import MATERIAL_PROFILES, WEAPON_TYPES, quality_tier, weapon_damage, weapon_display_name
            it      = getattr(player, "crafted_weapons", [])[sel_key]
            mat_col = MATERIAL_PROFILES.get(it.material, {}).get("color", (180, 170, 155))
            pygame.draw.rect(self.screen, (18, 14, 10), (dx, dy2, dw, dh))
            pygame.draw.rect(self.screen, mat_col, (dx, dy2, dw, dh), 2)
            cx_p, cy_p = dx + dw // 2, dy2 + 46
            pygame.draw.line(self.screen, mat_col, (cx_p, dy2 + 8), (cx_p, dy2 + 84), 4)
            pygame.draw.line(self.screen, mat_col, (cx_p - 20, dy2 + 64), (cx_p + 20, dy2 + 64), 4)
            pygame.draw.circle(self.screen, mat_col, (cx_p, dy2 + 90), 5)
            dlabel(weapon_display_name(it), mat_col)
            dlabel(f"Type: {WEAPON_TYPES[it.weapon_type]['name']}", (200, 195, 185))
            dlabel(f"Material: {MATERIAL_PROFILES[it.material]['name']}", mat_col)
            dlabel(f"Quality: {quality_tier(it.quality)} ({int(it.quality * 100)}%)", mat_col)
            dlabel(f"Damage: {weapon_damage(it):.1f}", (220, 130, 80))
            dlabel(f"Range: {WEAPON_TYPES[it.weapon_type]['attack_range']} blocks", (160, 190, 220))
            dlabel(f"Attack speed: {1.0 / WEAPON_TYPES[it.weapon_type]['cooldown']:.1f}/s", (160, 190, 220))
            if it.parts_quality:
                dlabel("Part qualities:", (180, 175, 165))
                parts = WEAPON_TYPES[it.weapon_type]["parts"]
                for i, pq in enumerate(it.parts_quality):
                    pk = parts[i] if i < len(parts) else f"part {i+1}"
                    dlabel(f"  {pk.replace('_',' ').title()}: {int(pq*100)}%", mat_col)
        else:  # mushroom
            bid = sel_key
            pygame.draw.rect(self.screen, (16, 14, 8), (dx, dy2, dw, dh))
            pygame.draw.rect(self.screen, (165, 148, 60), (dx, dy2, dw, dh), 2)
            self.screen.blit(render_mushroom_preview(bid, 80), (dx + dw // 2 - 40, dy2 + 8))
            dlabel(BLOCKS[bid]["name"], (235, 220, 130))
            drop = BLOCKS[bid].get("drop") or ""
            dlabel(f"Drop: {drop.replace('_', ' ').title()}",
                   _MUSHROOM_DROP_COLOR.get(drop, (180, 160, 120)))
            dlabel(f"Biome: {_MUSHROOM_BIOME.get(bid, 'Any')}", (170, 195, 150))
            dlabel(f"Shape: {_MUSHROOM_SHAPES.get(bid, '').title()}", (155, 162, 178))
            dlabel(f"Collected: {player.mushrooms_found.get(bid, 0)}", (160, 205, 160))

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
            type_s = self.small.render(self._fit_label(rock.base_type.replace("_", " "), CELL - 4), True, (160, 160, 160))
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

    def _draw_codex(self, player, gy0=58, gx_off=0):
        CELL, GAP, COLS = 82, 8, 6
        gx0 = gx_off + (SCREEN_W - gx_off - (COLS * CELL + (COLS - 1) * GAP)) // 2

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

            ls = self.small.render(self._fit_label(label, CELL - 4), True, (160, 165, 175) if discovered else (55, 58, 68))
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
            type_s = self.small.render(self._fit_label(flower.flower_type.replace("_", " "), CELL - 4), True, (140, 175, 140))
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

    def _draw_flower_codex(self, player, gy0=58, gx_off=0):
        CELL, GAP, COLS = 82, 8, 6
        gx0 = gx_off + (SCREEN_W - gx_off - (COLS * CELL + (COLS - 1) * GAP)) // 2

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

            ls = self.small.render(self._fit_label(label, CELL - 4), True, (140, 185, 145) if discovered else (40, 65, 42))
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

    def _draw_mushroom_codex(self, player, gy0=58, gx_off=0):
        CELL, GAP, COLS = 82, 8, 5
        gx0 = gx_off + (SCREEN_W - gx_off - (COLS * CELL + (COLS - 1) * GAP)) // 2

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

            ls = self.small.render(self._fit_label(label, CELL - 4), True, (200, 180, 100) if discovered else (52, 46, 20))
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
    # Fossil collection tabs
    # ------------------------------------------------------------------

    def _draw_my_fossils(self, player):
        if not player.fossils:
            msg = self.font.render("No fossils yet.  Mine Fossil Deposits deep underground!", True, (90, 80, 65))
            self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2 - 10))
            return

        CELL, GAP, COLS = 82, 8, 8
        gx0 = (SCREEN_W - (COLS * CELL + (COLS - 1) * GAP)) // 2
        gy0 = 58

        detail_x = None
        if self._selected_fossil_idx is not None and self._selected_fossil_idx < len(player.fossils):
            detail_x = SCREEN_W - 340
            COLS = max(1, (detail_x - gx0 - 10) // (CELL + GAP))

        total_rows = (len(player.fossils) + COLS - 1) // COLS
        visible_rows = (SCREEN_H - gy0 - 8 + GAP) // (CELL + GAP)
        self._max_my_fossils_scroll = max(0, total_rows - visible_rows)
        self._my_fossils_scroll = max(0, min(self._max_my_fossils_scroll, self._my_fossils_scroll))

        self._fossil_rects.clear()
        for idx, fossil in enumerate(player.fossils):
            col = idx % COLS
            row = idx // COLS
            display_row = row - self._my_fossils_scroll
            if display_row < 0:
                continue
            x = gx0 + col * (CELL + GAP)
            y = gy0 + display_row * (CELL + GAP)
            if y + CELL > SCREEN_H - 8:
                break
            rect = pygame.Rect(x, y, CELL, CELL)
            self._fossil_rects[idx] = rect

            selected = (idx == self._selected_fossil_idx)
            rar_col = RARITY_COLORS[fossil.rarity] if fossil.prepared else (80, 72, 55)
            pygame.draw.rect(self.screen, (45, 40, 28) if selected else (30, 26, 18), rect)
            pygame.draw.rect(self.screen, rar_col, rect, 3 if selected else 2)
            img = render_fossil(fossil, 58)
            if not fossil.prepared:
                grey = img.copy()
                grey.fill((60, 52, 38, 210), special_flags=pygame.BLEND_RGBA_MULT)
                self.screen.blit(grey, (x + (CELL - 58) // 2, y + (CELL - 58) // 2 - 6))
                q_s = self.font.render("?", True, (140, 125, 90))
                self.screen.blit(q_s, (x + CELL // 2 - q_s.get_width() // 2,
                                       y + (CELL - 58) // 2 + 14))
            else:
                self.screen.blit(img, (x + (CELL - 58) // 2, y + (CELL - 58) // 2 - 6))
            label = fossil.fossil_type.replace("_", " ") if fossil.prepared else "unknown"
            type_s = self.small.render(self._fit_label(label, CELL - 4), True,
                                       (175, 155, 115) if fossil.prepared else (110, 98, 72))
            self.screen.blit(type_s, (x + CELL // 2 - type_s.get_width() // 2, y + CELL - 14))

        if detail_x is None:
            return

        fossil = player.fossils[self._selected_fossil_idx]
        dx, dy = detail_x, gy0
        dw, dh = SCREEN_W - dx - 8, SCREEN_H - gy0 - 10
        border_col = RARITY_COLORS[fossil.rarity] if fossil.prepared else (80, 72, 55)
        pygame.draw.rect(self.screen, (22, 18, 12), (dx, dy, dw, dh))
        pygame.draw.rect(self.screen, border_col, (dx, dy, dw, dh), 2)

        img_big = render_fossil(fossil, 80)
        if not fossil.prepared:
            grey_big = img_big.copy()
            grey_big.fill((60, 52, 38, 200), special_flags=pygame.BLEND_RGBA_MULT)
            self.screen.blit(grey_big, (dx + dw // 2 - 40, dy + 8))
            q_big = self.font.render("?", True, (160, 140, 100))
            self.screen.blit(q_big, (dx + dw // 2 - q_big.get_width() // 2, dy + 38))
        else:
            self.screen.blit(img_big, (dx + dw // 2 - 40, dy + 8))

        iy = [dy + 96]

        def dlabel(text, color=(215, 195, 155)):
            s = self.small.render(text, True, color)
            self.screen.blit(s, (dx + 8, iy[0]))
            iy[0] += 15

        if not fossil.prepared:
            dlabel("Unknown Fossil", (160, 145, 105))
            dlabel(f"Size: {fossil.size.title()}")
            dlabel(f"Found at: {fossil.depth_found}m depth")
            iy[0] += 8
            dlabel("Prepare at a Fossil Prep Table", (130, 160, 110))
            dlabel("to identify this specimen.", (100, 90, 68))
            return

        dlabel(fossil.fossil_type.replace("_", " ").title(), (235, 205, 130))
        dlabel(RARITY_LABEL[fossil.rarity], RARITY_COLORS[fossil.rarity])
        dlabel(f"Age: {fossil.age.title()}", FOSSIL_AGE_COLORS.get(fossil.age, (180, 160, 120)))
        dlabel(f"Size: {fossil.size.title()}")
        dlabel(f"Found at: {fossil.depth_found}m depth")
        dlabel(f"Pattern: {fossil.pattern.title()}")
        iy[0] += 4

        def stat_bar(label, val, col=(180, 150, 80)):
            ls = self.small.render(label, True, (160, 145, 110))
            self.screen.blit(ls, (dx + 8, iy[0]))
            bx2 = dx + 72
            bw = dw - 82
            pygame.draw.rect(self.screen, (35, 30, 20), (bx2, iy[0] + 2, bw, 8))
            pygame.draw.rect(self.screen, col, (bx2, iy[0] + 2, int(bw * val), 8))
            vs = self.small.render(f"{val:.2f}", True, (180, 160, 120))
            self.screen.blit(vs, (bx2 + bw + 4, iy[0]))
            iy[0] += 16

        stat_bar("Clarity", fossil.clarity, (100, 180, 200))
        stat_bar("Detail",  fossil.detail,  (180, 155, 80))
        iy[0] += 4

        if fossil.specials:
            dlabel("Traits:", (210, 185, 120))
            for sp in fossil.specials:
                desc = FOSSIL_SPECIAL_DESCS.get(sp, "")
                dlabel(f"  {sp.replace('_', ' ').title()}", (220, 195, 105))
                dlabel(f"    {desc}", (145, 130, 90))
        else:
            dlabel("No special traits.", (90, 82, 60))

    def _draw_fossil_codex(self, player, gy0=58, gx_off=0):
        CELL, GAP, COLS = 82, 8, 6
        gx0 = gx_off + (SCREEN_W - gx_off - (COLS * CELL + (COLS - 1) * GAP)) // 2

        detail_x = None
        if self._fossil_codex_selected_type is not None:
            detail_x = SCREEN_W - 340
            COLS = max(1, (detail_x - gx0 - 10) // (CELL + GAP))

        total_rows = (len(FOSSIL_TYPE_ORDER) + COLS - 1) // COLS
        visible_rows = (SCREEN_H - gy0 - 8 + GAP) // (CELL + GAP)
        self._max_fossil_codex_scroll = max(0, total_rows - visible_rows)
        self._fossil_codex_scroll = max(0, min(self._max_fossil_codex_scroll, self._fossil_codex_scroll))

        if self._max_fossil_codex_scroll > 0:
            sb_x = gx0 + COLS * (CELL + GAP) - GAP + 8
            sb_h = SCREEN_H - gy0 - 8
            sb_th = max(20, sb_h * visible_rows // total_rows)
            sb_top = gy0 + (sb_h - sb_th) * self._fossil_codex_scroll // self._max_fossil_codex_scroll
            pygame.draw.rect(self.screen, (28, 24, 14), (sb_x, gy0, 7, sb_h))
            pygame.draw.rect(self.screen, (160, 135, 72), (sb_x, sb_top, 7, sb_th))

        self._fossil_codex_rects.clear()
        for idx, type_key in enumerate(FOSSIL_TYPE_ORDER):
            col = idx % COLS
            row = idx // COLS
            display_row = row - self._fossil_codex_scroll
            if display_row < 0:
                continue
            x = gx0 + col * (CELL + GAP)
            y = gy0 + display_row * (CELL + GAP)
            if y + CELL > SCREEN_H - 8:
                break
            rect = pygame.Rect(x, y, CELL, CELL)
            self._fossil_codex_rects[type_key] = rect

            discovered = type_key in player.discovered_fossil_types
            selected = (type_key == self._fossil_codex_selected_type)

            if discovered:
                img = render_fossil_codex_preview(type_key, 58)
                pygame.draw.rect(self.screen, (48, 42, 28) if selected else (30, 26, 18), rect)
                pygame.draw.rect(self.screen, (185, 158, 82) if selected else (100, 84, 42), rect,
                                 3 if selected else 2)
                self.screen.blit(img, (x + (CELL - 58) // 2, y + (CELL - 58) // 2 - 6))
                label = type_key.replace("_", " ")
            else:
                tdef = FOSSIL_TYPES[type_key]
                min_d = tdef["min_depth"]
                pygame.draw.rect(self.screen, (20, 17, 10) if selected else (14, 12, 8), rect)
                pygame.draw.rect(self.screen, (62, 52, 26) if selected else (38, 32, 16), rect,
                                 2 if selected else 1)
                qs = self.font.render("?", True, (58, 48, 24))
                self.screen.blit(qs, (x + CELL // 2 - qs.get_width() // 2,
                                      y + CELL // 2 - qs.get_height() // 2 - 6))
                label = f">{min_d}m"

            ls = self.small.render(self._fit_label(label, CELL - 4), True, (185, 162, 108) if discovered else (58, 48, 24))
            self.screen.blit(ls, (x + CELL // 2 - ls.get_width() // 2, y + CELL - 14))

        if detail_x is None:
            return

        type_key = self._fossil_codex_selected_type
        tdef = FOSSIL_TYPES[type_key]
        discovered = type_key in player.discovered_fossil_types

        dx, dy = detail_x, gy0
        dw, dh = SCREEN_W - dx - 8, SCREEN_H - gy0 - 10
        border_col = (175, 148, 72) if discovered else (55, 46, 22)
        pygame.draw.rect(self.screen, (18, 15, 10), (dx, dy, dw, dh))
        pygame.draw.rect(self.screen, border_col, (dx, dy, dw, dh), 2)

        iy = [dy + 8]

        def dlabel(text, color=(215, 195, 155)):
            s = self.small.render(text, True, color)
            self.screen.blit(s, (dx + 8, iy[0]))
            iy[0] += 15

        if discovered:
            img_big = render_fossil_codex_preview(type_key, 80)
            self.screen.blit(img_big, (dx + dw // 2 - 40, dy + 8))
            iy[0] = dy + 96
            dlabel(type_key.replace("_", " ").title(), (235, 205, 130))
            dlabel(f"Era: {tdef['age'].title()}",
                   FOSSIL_AGE_COLORS.get(tdef["age"], (180, 160, 120)))
            dlabel(f"Found from {tdef['min_depth']}m depth", (155, 138, 100))

            desc = FOSSIL_TYPE_DESCRIPTIONS.get(type_key, "")
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
                dlabel(ln, (125, 112, 85))
            iy[0] += 6

            pool = tdef["rarity_pool"]
            counts = {r: pool.count(r) for r in dict.fromkeys(pool)}
            dlabel("Rarity: " + "  ".join(f"{r[0].upper()}×{c}" for r, c in counts.items()),
                   (175, 155, 105))
            owned = [f for f in player.fossils if f.fossil_type == type_key]
            dlabel(f"In collection: {len(owned)}", (155, 200, 155))
            if owned:
                rarities = ["common", "uncommon", "rare", "epic", "legendary"]
                best = max(owned, key=lambda f: rarities.index(f.rarity))
                dlabel(f"Best rarity: {RARITY_LABEL[best.rarity]}", RARITY_COLORS[best.rarity])
        else:
            iy[0] = dy + 30
            qs = self.font.render("???", True, (55, 46, 22))
            self.screen.blit(qs, (dx + dw // 2 - qs.get_width() // 2, dy + 8))
            dlabel("Not yet discovered.", (82, 70, 38))
            dlabel(f"Find it below {tdef['min_depth']}m depth.", (105, 90, 50))

    # ------------------------------------------------------------------
    # Achievements tab
    # ------------------------------------------------------------------

    _ACH_CATEGORY_COLORS = {
        "mushroom":   (170, 210, 110),
        "rock":       (160, 200, 240),
        "wildflower": (200, 240, 180),
        "fossil":     (220, 185, 110),
    }
    _ACH_CATEGORY_LABELS = {
        "mushroom":   "MUSHROOM",
        "rock":       "ROCK",
        "wildflower": "WILDFLOWER",
        "fossil":     "FOSSIL",
    }

    # ------------------------------------------------------------------
    # Gem collection tabs
    # ------------------------------------------------------------------

    def _draw_my_gems(self, player):
        if not player.gems:
            msg = self.font.render("No gems yet.  Mine Gem Deposits deep underground!", True, (70, 130, 115))
            self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2 - 10))
            hint = self.small.render("Approach the Gem Cutter block and press E to cut rough gems.", True, (60, 110, 98))
            self.screen.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, SCREEN_H // 2 + 14))
            return

        CELL, GAP, COLS = 82, 8, 8
        gx0 = (SCREEN_W - (COLS * CELL + (COLS - 1) * GAP)) // 2
        gy0 = 58

        detail_x = None
        if self._selected_gem_idx is not None and self._selected_gem_idx < len(player.gems):
            detail_x = SCREEN_W - 340
            COLS = max(1, (detail_x - gx0 - 10) // (CELL + GAP))

        total_rows = (len(player.gems) + COLS - 1) // COLS
        visible_rows = (SCREEN_H - gy0 - 8 + GAP) // (CELL + GAP)
        self._max_my_gems_scroll = max(0, total_rows - visible_rows)
        self._my_gems_scroll = max(0, min(self._max_my_gems_scroll, self._my_gems_scroll))

        self._gem_rects.clear()
        for idx, gem in enumerate(player.gems):
            col = idx % COLS
            row = idx // COLS
            display_row = row - self._my_gems_scroll
            if display_row < 0:
                continue
            x = gx0 + col * (CELL + GAP)
            y = gy0 + display_row * (CELL + GAP)
            if y + CELL > SCREEN_H - 8:
                break
            rect = pygame.Rect(x, y, CELL, CELL)
            self._gem_rects[idx] = rect

            selected = (idx == self._selected_gem_idx)
            rar_col = GEM_RARITY_COLORS.get(gem.rarity, (120, 120, 120))
            pygame.draw.rect(self.screen, (28, 42, 40) if selected else (18, 28, 26), rect)
            pygame.draw.rect(self.screen, rar_col, rect, 3 if selected else 2)

            if gem.state == "rough":
                img = render_rough_gem(gem, 58)
            else:
                img = render_gem(gem, 58)
            self.screen.blit(img, (x + (CELL - 58) // 2, y + (CELL - 58) // 2 - 6))

            label = gem.gem_type.replace("_", " ")
            if gem.state == "rough":
                label = "rough " + label
            type_s = self.small.render(self._fit_label(label, CELL - 4), True, (120, 195, 175))
            self.screen.blit(type_s, (x + CELL // 2 - type_s.get_width() // 2, y + CELL - 14))

        if detail_x is None:
            return

        gem = player.gems[self._selected_gem_idx]
        dx, dy = detail_x, gy0
        dw, dh = SCREEN_W - dx - 8, SCREEN_H - gy0 - 10
        pygame.draw.rect(self.screen, (14, 22, 20), (dx, dy, dw, dh))
        rar_col = GEM_RARITY_COLORS.get(gem.rarity, (120, 120, 120))
        pygame.draw.rect(self.screen, rar_col, (dx, dy, dw, dh), 2)

        # Render gem image
        preview_size = 100
        if gem.state == "rough":
            preview = render_rough_gem(gem, preview_size)
        else:
            preview = render_gem(gem, preview_size)
        self.screen.blit(preview, (dx + dw // 2 - preview_size // 2, dy + 8))

        ty = dy + preview_size + 16
        def detail_row(label, value, col=(155, 200, 185)):
            nonlocal ty
            lbl = self.small.render(f"{label}:", True, (80, 118, 108))
            val = self.small.render(str(value), True, col)
            self.screen.blit(lbl, (dx + 10, ty))
            self.screen.blit(val, (dx + dw - val.get_width() - 8, ty))
            ty += 17

        name = gem.gem_type.replace("_", " ").title()
        title_s = self.font.render(name, True, rar_col)
        self.screen.blit(title_s, (dx + dw // 2 - title_s.get_width() // 2, ty))
        ty += 22

        detail_row("Rarity", gem.rarity.title(), rar_col)
        detail_row("Size", gem.size.title())
        detail_row("State", gem.state.title(), (255, 200, 80) if gem.state == "rough" else (100, 220, 180))
        detail_row("Cut", GEM_CUT_DESCS.get(gem.cut, gem.cut).split(" —")[0])

        if gem.state == "cut":
            detail_row("Clarity", gem.clarity,
                       (255, 220, 80) if gem.clarity in ("FL", "VVS") else (155, 200, 185))
            detail_row("Inclusion", gem.inclusion.replace("_", " ").title())
            if gem.optical_effect != "none":
                detail_row("Optical", gem.optical_effect.replace("_", " ").title(), (200, 160, 255))
        else:
            ty += 4
            unknown = self.small.render("Hidden until cut at Gem Cutter", True, (80, 100, 95))
            self.screen.blit(unknown, (dx + dw // 2 - unknown.get_width() // 2, ty))
            ty += 17

        detail_row("Crystal", gem.crystal_system.title())
        detail_row("Depth", f"{gem.depth_found}m")

        ty += 6
        desc_text = GEM_TYPE_DESCRIPTIONS.get(gem.gem_type, "")
        words = desc_text.split()
        line, lines = [], []
        for w in words:
            test = " ".join(line + [w])
            if self.small.size(test)[0] > dw - 18:
                lines.append(" ".join(line))
                line = [w]
            else:
                line.append(w)
        if line:
            lines.append(" ".join(line))
        for l in lines[:4]:
            ls = self.small.render(l, True, (72, 100, 90))
            self.screen.blit(ls, (dx + 8, ty))
            ty += 15

    def _draw_gem_codex(self, player, gy0=58, gx_off=0):
        CELL, GAP, COLS = 82, 8, 10
        gx0 = gx_off + (SCREEN_W - gx_off - (COLS * CELL + (COLS - 1) * GAP)) // 2

        detail_x = None
        if self._gem_codex_selected_type is not None:
            detail_x = SCREEN_W - 340
            COLS = max(1, (detail_x - gx0 - 10) // (CELL + GAP))

        total_rows = (len(GEM_TYPE_ORDER) + COLS - 1) // COLS
        visible_rows = (SCREEN_H - gy0 - 8 + GAP) // (CELL + GAP)
        self._max_gem_codex_scroll = max(0, total_rows - visible_rows)
        self._gem_codex_scroll = max(0, min(self._max_gem_codex_scroll, self._gem_codex_scroll))

        self._gem_codex_rects.clear()
        for i, type_key in enumerate(GEM_TYPE_ORDER):
            col = i % COLS
            row = i // COLS
            display_row = row - self._gem_codex_scroll
            if display_row < 0:
                continue
            x = gx0 + col * (CELL + GAP)
            y = gy0 + display_row * (CELL + GAP)
            if y + CELL > SCREEN_H - 8:
                break
            rect = pygame.Rect(x, y, CELL, CELL)
            self._gem_codex_rects[type_key] = rect

            discovered = type_key in player.discovered_gem_types
            selected = (type_key == self._gem_codex_selected_type)

            if discovered:
                tdef = GEM_TYPES[type_key]
                sample_rarity = tdef["rarity_pool"][0]
                rar_col = GEM_RARITY_COLORS.get(sample_rarity, (120, 120, 120))
                pygame.draw.rect(self.screen, (28, 42, 40) if selected else (18, 28, 26), rect)
                pygame.draw.rect(self.screen, rar_col, rect, 3 if selected else 2)
                img = render_gem_codex_preview(type_key, 58)
                self.screen.blit(img, (x + (CELL - 58) // 2, y + (CELL - 58) // 2 - 6))
                name_s = self.small.render(self._fit_label(type_key.replace("_", " "), CELL - 4), True, (120, 195, 175))
            else:
                pygame.draw.rect(self.screen, (14, 18, 16), rect)
                pygame.draw.rect(self.screen, (40, 55, 50), rect, 2)
                q = self.font.render("?", True, (38, 55, 50))
                self.screen.blit(q, (x + CELL // 2 - q.get_width() // 2, y + CELL // 2 - q.get_height() // 2 - 8))
                name_s = self.small.render("???", True, (38, 55, 50))
            self.screen.blit(name_s, (x + CELL // 2 - name_s.get_width() // 2, y + CELL - 14))

        if detail_x is None:
            return

        type_key = self._gem_codex_selected_type
        discovered = type_key in player.discovered_gem_types
        dx, dy = detail_x, gy0
        dw, dh = SCREEN_W - dx - 8, SCREEN_H - gy0 - 10
        pygame.draw.rect(self.screen, (14, 22, 20), (dx, dy, dw, dh))

        if discovered:
            tdef = GEM_TYPES[type_key]
            sample_rarity = tdef["rarity_pool"][0]
            rar_col = GEM_RARITY_COLORS.get(sample_rarity, (120, 120, 120))
            pygame.draw.rect(self.screen, rar_col, (dx, dy, dw, dh), 2)

            preview = render_gem_codex_preview(type_key, 100)
            self.screen.blit(preview, (dx + dw // 2 - 50, dy + 8))

            ty = dy + 116
            name_s = self.font.render(type_key.replace("_", " ").title(), True, rar_col)
            self.screen.blit(name_s, (dx + dw // 2 - name_s.get_width() // 2, ty))
            ty += 24

            crys_s = self.small.render(f"Crystal system: {tdef['crystal_system'].title()}", True, (95, 145, 132))
            self.screen.blit(crys_s, (dx + 10, ty)); ty += 17
            depth_s = self.small.render(f"Found from depth: {tdef['min_depth']}m", True, (95, 145, 132))
            self.screen.blit(depth_s, (dx + 10, ty)); ty += 17
            cuts_s = self.small.render("Cuts: " + ", ".join(tdef["available_cuts"]), True, (95, 145, 132))
            self.screen.blit(cuts_s, (dx + 10, ty)); ty += 20

            desc_text = GEM_TYPE_DESCRIPTIONS.get(type_key, "")
            words = desc_text.split()
            line, lines = [], []
            for w in words:
                test = " ".join(line + [w])
                if self.small.size(test)[0] > dw - 18:
                    lines.append(" ".join(line))
                    line = [w]
                else:
                    line.append(w)
            if line:
                lines.append(" ".join(line))
            for l in lines[:5]:
                ls = self.small.render(l, True, (72, 108, 96))
                self.screen.blit(ls, (dx + 8, ty))
                ty += 15
        else:
            pygame.draw.rect(self.screen, (40, 55, 50), (dx, dy, dw, dh), 2)
            unk = self.font.render("Not Yet Discovered", True, (50, 75, 65))
            self.screen.blit(unk, (dx + dw // 2 - unk.get_width() // 2, dy + dh // 2 - 10))


    def _draw_bird_codex(self, player, gy0=58, gx_off=0):
        from birds import ALL_SPECIES
        RARITY_BIRD_COLS = {"common": (120, 170, 120), "uncommon": (100, 170, 220),
                            "rare": (180, 120, 230)}

        CELL, GAP, COLS = 120, 10, 6
        ROW_H = CELL + GAP
        gx0 = gx_off + (SCREEN_W - gx_off - (COLS * CELL + (COLS - 1) * GAP)) // 2
        visible_h = SCREEN_H - gy0 - 8

        num_rows = (len(ALL_SPECIES) + COLS - 1) // COLS
        total_h = num_rows * ROW_H
        self._max_bird_codex_scroll = max(0, total_h - visible_h)
        self._bird_codex_scroll = max(0, min(self._max_bird_codex_scroll, self._bird_codex_scroll))

        if self._max_bird_codex_scroll > 0:
            sb_x = gx0 + COLS * (CELL + GAP) - GAP + 8
            sb_th = max(20, visible_h * visible_h // total_h)
            sb_top = gy0 + (visible_h - sb_th) * self._bird_codex_scroll // self._max_bird_codex_scroll
            pygame.draw.rect(self.screen, (35, 35, 48), (sb_x, gy0, 7, visible_h))
            pygame.draw.rect(self.screen, (100, 100, 140), (sb_x, sb_top, 7, sb_th))

        self._bird_codex_rects.clear()
        for idx, sp_cls in enumerate(ALL_SPECIES):
            col = idx % COLS
            row = idx // COLS
            x = gx0 + col * (CELL + GAP)
            y = gy0 + row * ROW_H - self._bird_codex_scroll
            if y + CELL <= gy0 or y >= SCREEN_H - 8:
                continue
            rect = pygame.Rect(x, y, CELL, CELL)
            self._bird_codex_rects[sp_cls.SPECIES] = rect

            discovered = sp_cls.SPECIES in player.birds_observed
            obs = player.birds_observed.get(sp_cls.SPECIES, {})
            rar_col = RARITY_BIRD_COLS.get(sp_cls.RARITY, (150, 150, 150))

            # Background
            bg_col = (14, 28, 42) if discovered else (18, 18, 22)
            pygame.draw.rect(self.screen, bg_col, rect)
            pygame.draw.rect(self.screen, rar_col if discovered else (40, 40, 55), rect, 2)

            # Bird icon
            bw, bh = sp_cls.W * 3, sp_cls.H * 3
            bird_surf = pygame.Surface((bw, bh), pygame.SRCALPHA)
            bird_surf.fill((0, 0, 0, 0))
            if discovered:
                pygame.draw.ellipse(bird_surf, sp_cls.WING_COLOR, (0, bh // 3, bw, bh // 2))
                pygame.draw.ellipse(bird_surf, sp_cls.BODY_COLOR,
                                    (bw // 6, bh // 3, bw * 2 // 3, bh // 2))
                pygame.draw.circle(bird_surf, sp_cls.HEAD_COLOR,
                                   (bw - bw // 5, bh // 4), bh // 5)
                pygame.draw.ellipse(bird_surf, sp_cls.ACCENT_COLOR,
                                    (bw // 6, bh // 3 + bh // 8, bw // 2, bh // 5))
            else:
                # Silhouette
                pygame.draw.ellipse(bird_surf, (50, 50, 60), (0, bh // 3, bw, bh // 2))
                pygame.draw.ellipse(bird_surf, (40, 40, 50),
                                    (bw // 6, bh // 3, bw * 2 // 3, bh // 2))
                pygame.draw.circle(bird_surf, (50, 50, 60), (bw - bw // 5, bh // 4), bh // 5)
            self.screen.blit(bird_surf, (x + CELL // 2 - bw // 2, y + 6))

            # Name
            if discovered:
                name = sp_cls.SPECIES.replace("_", " ").title()
                name_col = (200, 225, 255)
            else:
                name = "???"
                name_col = (60, 60, 75)
            ns = self.small.render(self._fit_label(name, CELL - 6), True, name_col)
            self.screen.blit(ns, (x + CELL // 2 - ns.get_width() // 2, y + CELL - 28))

            # Rarity
            rs = self.small.render(sp_cls.RARITY.upper(), True,
                                    rar_col if discovered else (50, 50, 65))
            self.screen.blit(rs, (x + CELL // 2 - rs.get_width() // 2, y + CELL - 14))

            # Observation count badge
            if discovered:
                cnt = obs.get("count", 0)
                cb = self.small.render(f"×{cnt}", True, (180, 230, 200))
                self.screen.blit(cb, (x + CELL - cb.get_width() - 3, y + 3))

    # ------------------------------------------------------------------
    # Insect codex
    # ------------------------------------------------------------------

    def _draw_insect_codex(self, player, gy0=58, gx_off=0):
        from insects import ALL_INSECT_SPECIES
        RARITY_COLS = {"common": (120, 190, 120), "uncommon": (100, 200, 120),
                       "rare": (120, 210, 140)}

        CELL, GAP, COLS = 120, 10, 6
        ROW_H = CELL + GAP
        gx0 = gx_off + (SCREEN_W - gx_off - (COLS * CELL + (COLS - 1) * GAP)) // 2
        visible_h = SCREEN_H - gy0 - 8

        num_rows = (len(ALL_INSECT_SPECIES) + COLS - 1) // COLS
        total_h = num_rows * ROW_H
        self._max_insect_codex_scroll = max(0, total_h - visible_h)
        self._insect_codex_scroll = max(0, min(self._max_insect_codex_scroll,
                                               self._insect_codex_scroll))

        if self._max_insect_codex_scroll > 0:
            sb_x = gx0 + COLS * (CELL + GAP) - GAP + 8
            sb_th = max(20, visible_h * visible_h // total_h)
            sb_top = gy0 + (visible_h - sb_th) * self._insect_codex_scroll // self._max_insect_codex_scroll
            pygame.draw.rect(self.screen, (35, 35, 48), (sb_x, gy0, 7, visible_h))
            pygame.draw.rect(self.screen, (80, 140, 80), (sb_x, sb_top, 7, sb_th))

        self._insect_codex_rects.clear()
        for idx, sp_cls in enumerate(ALL_INSECT_SPECIES):
            col = idx % COLS
            row = idx // COLS
            x = gx0 + col * (CELL + GAP)
            y = gy0 + row * ROW_H - self._insect_codex_scroll
            if y + CELL <= gy0 or y >= SCREEN_H - 8:
                continue
            rect = pygame.Rect(x, y, CELL, CELL)
            self._insect_codex_rects[sp_cls.SPECIES] = rect

            discovered = sp_cls.SPECIES in getattr(player, "insects_observed", {})
            obs = getattr(player, "insects_observed", {}).get(sp_cls.SPECIES, {})
            rar_col = RARITY_COLS.get(sp_cls.RARITY, (150, 150, 150))

            bg_col = (14, 35, 18) if discovered else (18, 22, 18)
            pygame.draw.rect(self.screen, bg_col, rect)
            pygame.draw.rect(self.screen, rar_col if discovered else (40, 55, 40), rect, 2)

            # Insect icon (wing + body preview)
            iw, ih = sp_cls.W * 3, sp_cls.H * 3
            ins_surf = pygame.Surface((iw, ih), pygame.SRCALPHA)
            ins_surf.fill((0, 0, 0, 0))
            if discovered:
                wt = sp_cls.WING_TYPE
                wc = sp_cls.WING_COLOR
                bc = sp_cls.BODY_COLOR
                ac = sp_cls.ACCENT_COLOR
                if wt in ("butterfly", "moth"):
                    pygame.draw.ellipse(ins_surf, wc, (0, 0, iw // 2, ih))
                    pygame.draw.ellipse(ins_surf, wc, (iw // 2, 0, iw // 2, ih))
                    pygame.draw.ellipse(ins_surf, ac, (2, 2, iw // 2 - 3, ih - 4))
                    pygame.draw.ellipse(ins_surf, bc, (iw // 2 - 1, 1, 3, ih - 2))
                elif wt == "dragonfly":
                    pygame.draw.ellipse(ins_surf, wc, (0, 0, iw // 2, ih // 3))
                    pygame.draw.ellipse(ins_surf, wc, (iw // 2, 0, iw // 2, ih // 3))
                    pygame.draw.ellipse(ins_surf, bc, (2, ih // 4, iw - 4, ih // 2))
                    pygame.draw.ellipse(ins_surf, ac, (4, ih // 3, iw - 8, ih // 3))
                elif wt in ("beetle", "firefly"):
                    pygame.draw.ellipse(ins_surf, wc, (0, ih // 4, iw, ih // 2))
                    pygame.draw.ellipse(ins_surf, bc, (2, ih // 4 + 1, iw - 4, ih // 2 - 2))
                    pygame.draw.line(ins_surf, wc, (iw // 2, ih // 4 + 1), (iw // 2, ih // 4 + ih // 2 - 2))
                    if wt == "firefly":
                        pygame.draw.circle(ins_surf, ac, (iw - 3, ih // 2), 2)
                else:
                    pygame.draw.ellipse(ins_surf, wc, (0, 0, iw, ih))
                    pygame.draw.ellipse(ins_surf, bc, (iw // 4, 2, iw // 2, ih - 4))
            else:
                pygame.draw.ellipse(ins_surf, (50, 60, 50), (0, 0, iw, ih))
                pygame.draw.ellipse(ins_surf, (40, 50, 40), (iw // 4, 2, iw // 2, ih - 4))
            self.screen.blit(ins_surf, (x + CELL // 2 - iw // 2, y + 6))

            if discovered:
                name = sp_cls.SPECIES.replace("_", " ").title()
                name_col = (180, 240, 190)
            else:
                name = "???"
                name_col = (55, 70, 55)
            ns = self.small.render(self._fit_label(name, CELL - 6), True, name_col)
            self.screen.blit(ns, (x + CELL // 2 - ns.get_width() // 2, y + CELL - 28))

            rs = self.small.render(sp_cls.RARITY.upper(), True,
                                    rar_col if discovered else (50, 65, 50))
            self.screen.blit(rs, (x + CELL // 2 - rs.get_width() // 2, y + CELL - 14))

            if discovered:
                cnt = obs.get("count", 0)
                cb = self.small.render(f"×{cnt}", True, (150, 230, 160))
                self.screen.blit(cb, (x + CELL - cb.get_width() - 3, y + 3))
                cond = obs.get("best_condition")
                if cond == "perfect":
                    cs = self.small.render("★", True, (255, 230, 80))
                    self.screen.blit(cs, (x + 3, y + 3))
                morph = obs.get("morph")
                if morph:
                    ms = self.small.render(morph[:3].upper(), True, (210, 140, 255))
                    self.screen.blit(ms, (x + 3, y + CELL - 28))

    # ------------------------------------------------------------------
    # Fish codex
    # ------------------------------------------------------------------

    def _draw_fish_codex(self, player, gy0=58, gx_off=0):
        CELL, GAP, COLS = 74, 6, 9
        ROW_H    = CELL + GAP
        HDR_H    = 26
        gx0      = gx_off + (SCREEN_W - gx_off - (COLS * CELL + (COLS - 1) * GAP)) // 2
        visible_h = SCREEN_H - gy0 - 8

        # Build list of virtual rows: ("header", label) or ("fish", [species...])
        vrows = []
        for group_label, species_list in FISH_BIOME_GROUPS:
            vrows.append(("header", group_label))
            for i in range(0, len(species_list), COLS):
                vrows.append(("fish", species_list[i:i + COLS]))

        total_h = sum(HDR_H if r[0] == "header" else ROW_H for r in vrows)
        self._max_fish_codex_scroll = max(0, total_h - visible_h)
        self._fish_codex_scroll = max(0, min(self._max_fish_codex_scroll,
                                              self._fish_codex_scroll))

        if self._max_fish_codex_scroll > 0:
            sb_x  = gx0 + COLS * (CELL + GAP) - GAP + 8
            sb_th = max(20, visible_h * visible_h // total_h)
            sb_top = gy0 + (visible_h - sb_th) * self._fish_codex_scroll // self._max_fish_codex_scroll
            pygame.draw.rect(self.screen, (35, 35, 48), (sb_x, gy0, 7, visible_h))
            pygame.draw.rect(self.screen, (100, 100, 140), (sb_x, sb_top, 7, sb_th))

        self._fish_codex_rects.clear()
        cy = gy0 - self._fish_codex_scroll
        grid_w = COLS * CELL + (COLS - 1) * GAP

        for row in vrows:
            if row[0] == "header":
                if gy0 <= cy + HDR_H and cy < SCREEN_H - 8:
                    lbl = self.font.render(row[1].upper(), True, (140, 190, 255))
                    self.screen.blit(lbl, (gx0, cy + 4))
                    sep_y = cy + HDR_H - 3
                    pygame.draw.line(self.screen, (45, 65, 95),
                                     (gx0, sep_y), (gx0 + grid_w, sep_y), 1)
                cy += HDR_H
            else:
                if gy0 <= cy + ROW_H and cy < SCREEN_H - 8:
                    for col_idx, species in enumerate(row[1]):
                        x = gx0 + col_idx * (CELL + GAP)
                        y = cy
                        if y + CELL > SCREEN_H - 8:
                            continue
                        fdata = FISH_TYPES[species]
                        discovered = species in player.discovered_fish_species
                        rar_col = FISH_RARITY_COLORS.get(fdata["rarity_pool"][0], (120, 120, 120))
                        rect = pygame.Rect(x, y, CELL, CELL)
                        self._fish_codex_rects[species] = rect

                        if discovered:
                            preview = next(
                                (f for f in reversed(player.fish_caught)
                                 if f.species == species), None)
                            pygame.draw.rect(self.screen, (12, 22, 34), rect)
                            pygame.draw.rect(self.screen, rar_col, rect, 2)
                            if preview:
                                img = render_fish(preview, CELL - 12)
                                self.screen.blit(img, (x + 6, y + 3))
                            name_s = self.small.render(
                                self._fit_label(fdata["name"], CELL - 4), True, (120, 185, 240))
                        else:
                            pygame.draw.rect(self.screen, (14, 14, 20), rect)
                            pygame.draw.rect(self.screen, (35, 50, 65), rect, 1)
                            pygame.draw.ellipse(self.screen, (28, 42, 58),
                                                (x + 8, y + CELL // 2 - 10, CELL - 16, 20))
                            name_s = self.small.render("???", True, (50, 65, 80))

                        self.screen.blit(name_s,
                                         (x + CELL // 2 - name_s.get_width() // 2, y + CELL - 14))
                cy += ROW_H

    # ------------------------------------------------------------------
    # Food codex
    # ------------------------------------------------------------------

    def _draw_food_codex(self, player, gy0=58, gx_off=0):
        from crafting import (BAKERY_RECIPES, WOK_RECIPES, STEAMER_RECIPES,
                              NOODLE_POT_RECIPES, BBQ_GRILL_RECIPES, CLAY_POT_RECIPES,
                              JUICER_RECIPES)
        from items import ITEMS as _ITEMS

        SECTIONS = [
            ("Bakery",     BAKERY_RECIPES),
            ("Wok",        WOK_RECIPES),
            ("Steamer",    STEAMER_RECIPES),
            ("Noodle Pot", NOODLE_POT_RECIPES),
            ("BBQ Grill",  BBQ_GRILL_RECIPES),
            ("Clay Pot",   CLAY_POT_RECIPES),
            ("Juicer",     JUICER_RECIPES),
        ]

        discovered = getattr(player, "discovered_foods", set())
        cooked     = getattr(player, "foods_cooked", {})

        COLS = 5
        CELL_W, CELL_H, GAP = 148, 50, 6
        HEADER_H = 24
        total_w = COLS * CELL_W + (COLS - 1) * GAP
        gx0 = gx_off + (SCREEN_W - gx_off - total_w) // 2
        visible_h = SCREEN_H - gy0 - 8

        # Pre-calculate total content height for scrollbar
        total_h = 0
        for _, recipes in SECTIONS:
            total_h += HEADER_H + 6
            rows = (len(recipes) + COLS - 1) // COLS
            total_h += rows * (CELL_H + GAP)

        self._max_food_codex_scroll = max(0, total_h - visible_h)
        self._food_codex_scroll = max(0, min(self._max_food_codex_scroll, self._food_codex_scroll))

        if self._max_food_codex_scroll > 0:
            sb_x   = gx0 + total_w + 8
            sb_th  = max(20, visible_h * visible_h // total_h)
            sb_top = gy0 + (visible_h - sb_th) * self._food_codex_scroll // self._max_food_codex_scroll
            pygame.draw.rect(self.screen, (38, 28, 18), (sb_x, gy0, 7, visible_h))
            pygame.draw.rect(self.screen, (175, 105, 45), (sb_x, sb_top, 7, sb_th))

        y = gy0 - self._food_codex_scroll

        for station_name, recipes in SECTIONS:
            # Section header
            hy = y
            y += HEADER_H + 6
            if hy + HEADER_H > gy0 and hy < SCREEN_H - 8:
                hs = self.small.render(station_name.upper(), True, (235, 175, 105))
                self.screen.blit(hs, (gx0, hy + (HEADER_H - hs.get_height()) // 2))
                pygame.draw.line(self.screen, (100, 65, 30),
                                 (gx0 + hs.get_width() + 6, hy + HEADER_H // 2),
                                 (gx0 + total_w, hy + HEADER_H // 2), 1)

            num_rows = (len(recipes) + COLS - 1) // COLS
            for i, recipe in enumerate(recipes):
                col = i % COLS
                row = i // COLS
                cx = gx0 + col * (CELL_W + GAP)
                cy = y + row * (CELL_H + GAP)

                if cy + CELL_H <= gy0 or cy >= SCREEN_H - 8:
                    continue

                food_id     = recipe["output_id"]
                is_disc     = food_id in discovered
                item_data   = _ITEMS.get(food_id, {})
                item_color  = item_data.get("color", (130, 100, 70))

                rect = pygame.Rect(cx, cy, CELL_W, CELL_H)
                bg     = (42, 26, 12) if is_disc else (24, 20, 16)
                border = (item_color[0] // 2, item_color[1] // 2, item_color[2] // 2) if is_disc else (50, 40, 30)
                pygame.draw.rect(self.screen, bg, rect)
                pygame.draw.rect(self.screen, border, rect, 1)

                DOT_R = 5
                dot_col = item_color if is_disc else (55, 48, 42)
                pygame.draw.circle(self.screen, dot_col, (cx + 10, cy + CELL_H // 2), DOT_R)

                if is_disc:
                    name = item_data.get("name", food_id)
                    ns = self.small.render(self._fit_label(name, CELL_W - 32), True, (230, 195, 155))
                    self.screen.blit(ns, (cx + 20, cy + 7))

                    hunger = item_data.get("hunger_restore", 0)
                    rs = self.small.render(f"+{hunger}", True, (110, 195, 110))
                    self.screen.blit(rs, (cx + 20, cy + CELL_H - 18))

                    cnt = cooked.get(food_id, 0)
                    if cnt > 0:
                        cs = self.small.render(f"×{cnt}", True, (155, 135, 95))
                        self.screen.blit(cs, (cx + CELL_W - cs.get_width() - 5, cy + 7))
                else:
                    qs = self.small.render("???", True, (58, 50, 44))
                    self.screen.blit(qs, (cx + 20, cy + CELL_H // 2 - qs.get_height() // 2))

            y += num_rows * (CELL_H + GAP)

    # ------------------------------------------------------------------
    # Coffee codex
    # ------------------------------------------------------------------

    def _draw_coffee_codex(self, player, gy0=58, gx_off=0):
        BIOMES = ["tropical", "jungle", "savanna", "wetland", "arid_steppe", "canyon", "beach"]
        ROASTS = ["light", "medium", "dark", "charred", "green"]
        COLS   = len(ROASTS)
        CELL_W, CELL_H, GAP = 110, 68, 6
        HDR_H  = 22
        gx0    = gx_off + (SCREEN_W - gx_off - (COLS * CELL_W + (COLS - 1) * GAP)) // 2

        # Column header (roast names)
        hdr_y = gy0
        for ci, roast in enumerate(ROASTS):
            hx = gx0 + ci * (CELL_W + GAP)
            rc = ROAST_COLORS.get(roast, (100, 60, 20))
            lbl = self.small.render(roast.upper(), True, rc)
            self.screen.blit(lbl, (hx + CELL_W // 2 - lbl.get_width() // 2, hdr_y + 4))

        self._coffee_codex_rects.clear()
        cy = hdr_y + HDR_H
        for biome in BIOMES:
            # Biome row header
            bnm = BIOME_DISPLAY_NAMES.get(biome, biome)
            bl  = self.font.render(bnm.upper(), True, (200, 160, 80))
            self.screen.blit(bl, (gx0 - bl.get_width() - 8, cy + (CELL_H - bl.get_height()) // 2))
            for ci, roast in enumerate(ROASTS):
                hx = gx0 + ci * (CELL_W + GAP)
                key = f"{biome}_{roast}"
                discovered = key in player.discovered_coffee_origins
                rect = pygame.Rect(hx, cy, CELL_W, CELL_H)
                self._coffee_codex_rects[key] = rect
                rc = ROAST_COLORS.get(roast, (100, 60, 20))
                selected = (self._coffee_codex_selected == key)

                if discovered:
                    pygame.draw.rect(self.screen, (35, 22, 8), rect)
                    pygame.draw.rect(self.screen, rc, rect, 3 if selected else 1)
                    # Best quality for this origin+roast
                    best_q = max(
                        (b.roast_quality for b in player.coffee_beans
                         if b.origin_biome == biome and b.roast_level == roast), default=0.0)
                    stars = "★" * round(best_q * 5) if best_q > 0 else ""
                    name_s = self.small.render(ROAST_LEVEL_DESCS.get(roast, roast).split("—")[0].strip(), True, rc)
                    self.screen.blit(name_s, (hx + 4, cy + 4))
                    if stars:
                        qs = self.small.render(stars, True, (220, 190, 60))
                        self.screen.blit(qs, (hx + 4, cy + CELL_H - qs.get_height() - 4))
                else:
                    pygame.draw.rect(self.screen, (15, 9, 3), rect)
                    pygame.draw.rect(self.screen, (40, 25, 10), rect, 1)
                    lock = self.small.render("?", True, (50, 30, 10))
                    self.screen.blit(lock, (hx + CELL_W // 2 - lock.get_width() // 2,
                                            cy + CELL_H // 2 - lock.get_height() // 2))

            cy += CELL_H + GAP

        # Detail panel for selected
        if self._coffee_codex_selected:
            key = self._coffee_codex_selected
            if key in player.discovered_coffee_origins:
                biome, roast = key.rsplit("_", 1)
                beans_matching = [b for b in player.coffee_beans
                                  if b.origin_biome == biome and b.roast_level == roast]
                if beans_matching:
                    best = max(beans_matching, key=lambda b: b.roast_quality)
                    dx2 = gx0 + COLS * (CELL_W + GAP) + 10
                    dpw = SCREEN_W - dx2 - 8
                    pygame.draw.rect(self.screen, (25, 15, 5), (dx2, gy0, dpw, SCREEN_H - gy0 - 10))
                    pygame.draw.rect(self.screen, ROAST_COLORS.get(roast, (100, 60, 20)),
                                     (dx2, gy0, dpw, SCREEN_H - gy0 - 10), 2)
                    iy2 = gy0 + 8

                    def dline(txt, col=(210, 160, 80)):
                        nonlocal iy2
                        s = self.small.render(txt, True, col)
                        self.screen.blit(s, (dx2 + 6, iy2))
                        iy2 += 15

                    dline(f"{BIOME_DISPLAY_NAMES.get(biome, biome)} {best.variety.title()}", (220, 170, 90))
                    dline(ROAST_LEVEL_DESCS.get(roast, roast), ROAST_COLORS.get(roast, (180, 120, 60)))
                    stars = "★" * round(best.roast_quality * 5)
                    dline(f"Best quality: {stars}", (220, 190, 60))
                    dline(f"Flavour Notes:", (180, 140, 60))
                    for note in best.flavor_notes:
                        dline(f"  • {note.title()}", (210, 175, 100))

    def _draw_wine_codex(self, player, gy0=58, gx_off=0):
        BIOMES = ["tropical", "jungle", "savanna", "wetland", "arid_steppe", "canyon", "beach",
                  "tundra", "swamp", "alpine_mountain", "rocky_mountain", "rolling_hills"]
        STYLES = WINE_STYLE_ORDER
        COLS = len(STYLES)
        CELL_W, CELL_H, GAP = 110, 54, 6
        HDR_H = 22
        gx0 = gx_off + (SCREEN_W - gx_off - (COLS * CELL_W + (COLS - 1) * GAP)) // 2

        # Column header
        hdr_y = gy0
        for ci, style in enumerate(STYLES):
            hx = gx0 + ci * (CELL_W + GAP)
            col = WINE_STYLE_COLORS.get(style, (150, 80, 100))
            lbl = self.small.render(style.upper(), True, col)
            self.screen.blit(lbl, (hx + CELL_W // 2 - lbl.get_width() // 2, hdr_y + 4))

        self._wine_codex_rects.clear()
        cy = hdr_y + HDR_H - self._wine_codex_scroll
        for biome in BIOMES:
            bnm = WINE_BIOME_NAMES.get(biome, biome)
            bl = self.font.render(bnm.upper(), True, (210, 160, 180))
            self.screen.blit(bl, (gx0 - bl.get_width() - 8, cy + (CELL_H - bl.get_height()) // 2))
            for ci, style in enumerate(STYLES):
                hx = gx0 + ci * (CELL_W + GAP)
                key = f"{biome}_{style}"
                discovered = key in getattr(player, "discovered_wine_origins", set())
                rect = pygame.Rect(hx, cy, CELL_W, CELL_H)
                self._wine_codex_rects[key] = rect
                col = WINE_STYLE_COLORS.get(style, (150, 80, 100))
                selected = (self._wine_codex_selected == key)

                if discovered:
                    pygame.draw.rect(self.screen, (35, 18, 26), rect)
                    pygame.draw.rect(self.screen, col, rect, 3 if selected else 1)
                    best_q = max(
                        (g.ferment_quality for g in player.wine_grapes
                         if g.origin_biome == biome and g.style == style), default=0.0)
                    stars = "★" * round(best_q * 5) if best_q > 0 else ""
                    name_s = self.small.render(style.title(), True, col)
                    self.screen.blit(name_s, (hx + 4, cy + 4))
                    if stars:
                        qs = self.small.render(stars, True, (220, 190, 60))
                        self.screen.blit(qs, (hx + 4, cy + CELL_H - qs.get_height() - 4))
                else:
                    pygame.draw.rect(self.screen, (14, 8, 12), rect)
                    pygame.draw.rect(self.screen, (45, 22, 32), rect, 1)
                    lock = self.small.render("?", True, (60, 30, 40))
                    self.screen.blit(lock, (hx + CELL_W // 2 - lock.get_width() // 2,
                                            cy + CELL_H // 2 - lock.get_height() // 2))
            cy += CELL_H + GAP

        total_h = len(BIOMES) * (CELL_H + GAP) + HDR_H
        visible_h = SCREEN_H - gy0 - 10
        self._max_wine_codex_scroll = max(0, total_h - visible_h)

        # Detail panel for selected discovered entry
        if self._wine_codex_selected:
            key = self._wine_codex_selected
            if key in player.discovered_wine_origins:
                biome, style = key.rsplit("_", 1)
                matching = [g for g in player.wine_grapes
                            if g.origin_biome == biome and g.style == style]
                if matching:
                    best = max(matching, key=lambda g: g.ferment_quality)
                    dx2 = gx0 + COLS * (CELL_W + GAP) + 10
                    dpw = SCREEN_W - dx2 - 8
                    if dpw > 120:
                        col = WINE_STYLE_COLORS.get(style, (150, 80, 100))
                        pygame.draw.rect(self.screen, (20, 12, 18), (dx2, gy0, dpw, SCREEN_H - gy0 - 10))
                        pygame.draw.rect(self.screen, col, (dx2, gy0, dpw, SCREEN_H - gy0 - 10), 2)
                        iy2 = gy0 + 8

                        def dline(txt, c=(220, 170, 180)):
                            nonlocal iy2
                            s = self.small.render(txt, True, c)
                            self.screen.blit(s, (dx2 + 6, iy2))
                            iy2 += 15

                        dline(f"{WINE_BIOME_NAMES.get(biome, biome)} {WINE_VARIETY_NAMES.get(best.variety, best.variety)}", (230, 180, 200))
                        dline(WINE_STYLE_DESCS.get(style, style), col)
                        if best.vessel:
                            dline(f"Aged: {best.vessel.title()}", (190, 150, 170))
                        stars = "★" * round(best.ferment_quality * 5)
                        dline(f"Best quality: {stars}", (220, 190, 60))
                        dline(f"Alcohol: {best.alcohol:.0%}   Complexity: {best.complexity:.0%}", (190, 160, 170))
                        dline("Flavour Notes:", (190, 150, 170))
                        for note in best.flavor_notes:
                            dline(f"  • {note.title()}", (220, 180, 190))

    def _draw_achievements(self):
        CARD_W, CARD_H = 360, 118
        COLS            = 3
        COL_GAP         = 18
        ROW_GAP         = 14
        START_Y         = 58
        grid_w          = COLS * CARD_W + (COLS - 1) * COL_GAP
        START_X         = (SCREEN_W - grid_w) // 2

        # Separate into groups (mushroom, rock, wildflower) — display in row order
        all_achs = ACHIEVEMENTS  # imported at module level

        # Scrollable virtual canvas — calculate total height
        rows      = (len(all_achs) + COLS - 1) // COLS
        total_h   = rows * (CARD_H + ROW_GAP)
        visible_h = SCREEN_H - START_Y - 8
        self._max_achievement_scroll = max(0, total_h - visible_h)

        clip_rect = pygame.Rect(0, START_Y, SCREEN_W, visible_h)
        self.screen.set_clip(clip_rect)

        for idx, ach in enumerate(all_achs):
            col = idx % COLS
            row = idx // COLS
            cx  = START_X + col * (CARD_W + COL_GAP)
            cy  = START_Y + row * (CARD_H + ROW_GAP) - self._achievement_scroll

            if cy + CARD_H < START_Y or cy > SCREEN_H:
                continue

            unlocked  = self.achievements_data.get(ach.id, False)
            found, total = get_achievement_progress(ach, self.global_collection)
            cat_col   = self._ACH_CATEGORY_COLORS.get(ach.category, (200, 200, 200))

            # Card background
            if unlocked:
                bg_col     = (50, 44, 18)
                border_col = (200, 170, 40)
            else:
                bg_col     = (22, 22, 28)
                border_col = (55, 58, 70)
            card_surf = pygame.Surface((CARD_W, CARD_H), pygame.SRCALPHA)
            card_surf.fill((*bg_col, 230))
            pygame.draw.rect(card_surf, border_col, (0, 0, CARD_W, CARD_H), 2, border_radius=6)

            # Left accent stripe (category colour)
            pygame.draw.rect(card_surf, cat_col, (0, 0, 5, CARD_H), border_radius=3)

            # Category badge
            badge_lbl = self._ACH_CATEGORY_LABELS.get(ach.category, "")
            bs = self.small.render(badge_lbl, True, cat_col)
            card_surf.blit(bs, (12, 6))

            # UNLOCKED banner (top-right)
            if unlocked:
                ul_s = self.small.render("UNLOCKED", True, (255, 215, 80))
                card_surf.blit(ul_s, (CARD_W - ul_s.get_width() - 8, 6))

            # Achievement name
            name_s = self.font.render(ach.name, True, (255, 215, 80) if unlocked else (210, 210, 220))
            card_surf.blit(name_s, (12, 22))

            # Description
            desc_s = self.small.render(ach.description, True, (140, 140, 155))
            card_surf.blit(desc_s, (12, 44))

            # Progress bar (full width minus padding)
            bar_x, bar_y = 12, 62
            bar_w        = CARD_W - 24
            bar_h        = 8
            pygame.draw.rect(card_surf, (40, 40, 48), (bar_x, bar_y, bar_w, bar_h), border_radius=4)
            fill_w = int(bar_w * found / max(total, 1))
            bar_fill_col = (200, 170, 40) if unlocked else cat_col
            if fill_w > 0:
                pygame.draw.rect(card_surf, bar_fill_col,
                                 (bar_x, bar_y, fill_w, bar_h), border_radius=4)
            progress_lbl = f"{found}/{total}"
            ps = self.small.render(progress_lbl, True, (180, 180, 190))
            card_surf.blit(ps, (bar_x + bar_w - ps.get_width(), bar_y - ps.get_height() - 1))

            # Item checklist — 2 rows of 3 for ≤6 items; 1 row of 5 + overflow for larger
            large = len(ach.required_items) > 6
            items_per_row = 5 if large else 3
            label_max_w   = 55 if large else 90
            display_items = ach.required_items[:5] if large else ach.required_items
            overflow      = max(0, len(ach.required_items) - len(display_items))

            for i, req in enumerate(display_items):
                item_col_i = i % items_per_row
                item_row_i = i // items_per_row
                ix = 12 + item_col_i * (CARD_W // items_per_row - 4)
                iy = 76 + item_row_i * 17
                item_found = str(req) in self.global_collection.get(ach.category, set())
                tick  = "✓" if item_found else "–"
                t_col = (130, 210, 110) if item_found else (80, 80, 90)
                n_col = (190, 190, 200) if item_found else (80, 80, 90)
                tk_s  = self.small.render(tick, True, t_col)
                nm_s  = self.small.render(
                    self._fit_label(item_display_name(ach.category, req), label_max_w),
                    True, n_col,
                )
                card_surf.blit(tk_s, (ix, iy))
                card_surf.blit(nm_s, (ix + 12, iy))

            if overflow > 0:
                ov_s = self.small.render(f"…and {overflow} more", True, (80, 80, 90))
                card_surf.blit(ov_s, (12, 93))

            self.screen.blit(card_surf, (cx, cy))

        self.screen.set_clip(None)

    # ------------------------------------------------------------------
    # Horse Codex
    # ------------------------------------------------------------------

    def _draw_horse_codex(self, player, gy0=58, gx_off=0):
        from horses import BIOME_COAT_COLORS
        from constants import SCREEN_W, SCREEN_H

        content_x = gx_off
        content_w = SCREEN_W - content_x
        y = gy0 + 8

        title_col = (210, 175, 100)

        # ---- Left panel: stats ----
        left_w = content_w // 2 - 8
        lx = content_x + 6

        def stat_line(label, value_str, vy):
            lbl = self.small.render(label, True, (165, 145, 95))
            val = self.small.render(value_str, True, (230, 205, 140))
            self.screen.blit(lbl, (lx, vy))
            self.screen.blit(val, (lx + 120, vy))

        records = getattr(player, "horse_records", {})
        horses_tamed = getattr(player, "horses_tamed", 0)
        horses_bred  = getattr(player, "horses_bred", 0)
        best_spd = records.get("best_speed", 0.0)
        best_sta = records.get("best_stamina", 0.0)

        hdr = self.font.render("RECORDS", True, title_col)
        self.screen.blit(hdr, (lx, y))
        y2 = y + 22
        stat_line("Horses Tamed:", str(horses_tamed), y2);       y2 += 16
        stat_line("Horses Bred:",  str(horses_bred), y2);        y2 += 16
        stat_line("Best Speed:", f"{best_spd:.3f}" if best_spd else "—", y2); y2 += 16
        stat_line("Best Stamina:", f"{best_sta:.3f}" if best_sta else "—", y2); y2 += 16

        # Speed mult hint
        if best_spd:
            spd_mult = 1.0 + best_spd
            hint = self.small.render(f"  → {spd_mult:.2f}x move speed", True, (140, 175, 215))
            self.screen.blit(hint, (lx, y2));  y2 += 14

        y2 += 8
        hdr2 = self.font.render("HOW TO RIDE", True, title_col)
        self.screen.blit(hdr2, (lx, y2)); y2 += 20
        tips = [
            "• Tame with apples, carrots, wheat, sugar lumps",
            "• Use Horse Brush for faster taming (+2 progress)",
            "• Equip Saddle → Right-click tamed horse",
            "• First ride triggers the breaking minigame",
            "• Press SPACE to sprint (drains stamina)",
            "• Press E to dismount",
            "• Place Stable block to breed two tamed horses",
        ]
        for tip in tips:
            t = self.small.render(tip, True, (170, 152, 108))
            self.screen.blit(t, (lx, y2));  y2 += 14

        # ---- Right panel: biome coat grid ----
        disc = getattr(player, "discovered_coat_biomes", set())
        rx = content_x + left_w + 14
        ry = gy0 + 8

        hdr3 = self.font.render("COAT COLOURS", True, title_col)
        self.screen.blit(hdr3, (rx, ry)); ry += 22

        cell_w, cell_h = 56, 40
        cols_per_row   = max(1, (content_w - left_w - 20) // (cell_w + 6))

        biomes = list(BIOME_COAT_COLORS.keys())
        for idx, biome in enumerate(biomes):
            row = idx // cols_per_row
            col = idx % cols_per_row
            bx_ = rx + col * (cell_w + 6)
            by_ = ry + row * (cell_h + 6)

            found = biome in disc
            # Cell bg
            bg = (38, 30, 18) if found else (22, 18, 12)
            pygame.draw.rect(self.screen, bg, (bx_, by_, cell_w, cell_h), border_radius=4)
            border_c = (140, 110, 55) if found else (55, 45, 28)
            pygame.draw.rect(self.screen, border_c, (bx_, by_, cell_w, cell_h), 1, border_radius=4)

            if found:
                # Show the 3 coat swatches
                coats = BIOME_COAT_COLORS[biome]
                sw = (cell_w - 8) // 3
                for si, coat in enumerate(coats):
                    pygame.draw.rect(self.screen, coat,
                                     (bx_ + 4 + si * (sw + 1), by_ + 4, sw, 16))
                biome_short = biome.replace("_", " ").upper()[:8]
                bl = self.small.render(biome_short, True, (180, 158, 105))
                self.screen.blit(bl, (bx_ + cell_w // 2 - bl.get_width() // 2, by_ + 24))
            else:
                unk = self.small.render("???", True, (60, 50, 32))
                self.screen.blit(unk, (bx_ + cell_w // 2 - unk.get_width() // 2,
                                        by_ + cell_h // 2 - unk.get_height() // 2))

    def _draw_textile_codex(self, player, gy0=58, gx_off=130):
        from textiles import (DYE_FAMILY_COLORS, DYE_FAMILY_DISPLAY, OUTPUT_DISPLAY,
                               _FIBERS, _DYE_FAMILIES, _OUTPUT_TYPES, TOTAL_TEXTILE_TYPES)
        disc = getattr(player, "discovered_textiles", set())
        n_disc = len(disc)
        sub = self.small.render(
            f"{n_disc} / {TOTAL_TEXTILE_TYPES} textile combinations discovered", True, (180, 140, 210))
        self.screen.blit(sub, (gx_off + 8, gy0))

        CELL_W, CELL_H, GAP = 56, 42, 4
        COLS = len(_DYE_FAMILIES) + 1  # +1 for fiber label
        ROW_H = CELL_H + GAP
        content_w = SCREEN_W - gx_off
        grid_x = gx_off + (content_w - (COLS * (CELL_W + GAP))) // 2
        gy = gy0 + 22
        self._textile_codex_rects = {}

        for fi, ftype in enumerate(_FIBERS):
            row_y = gy + fi * len(_OUTPUT_TYPES) * ROW_H
            for oi, otype in enumerate(_OUTPUT_TYPES):
                cy = row_y + oi * ROW_H
                # Fiber+output label
                lbl_s = self.small.render(f"{ftype[:3].upper()}·{otype[:3].upper()}", True, (155, 135, 185))
                self.screen.blit(lbl_s, (grid_x, cy + CELL_H // 2 - lbl_s.get_height() // 2))
                for di, dye in enumerate(_DYE_FAMILIES):
                    cx = grid_x + (di + 1) * (CELL_W + GAP)
                    key = f"{ftype}_{dye}_{otype}"
                    discovered = key in disc
                    dye_col = tuple(DYE_FAMILY_COLORS[dye])
                    rect = pygame.Rect(cx, cy, CELL_W, CELL_H)
                    self._textile_codex_rects[key] = rect
                    if discovered:
                        pygame.draw.rect(self.screen, dye_col, rect)
                        pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)
                        if self._textile_codex_selected == key:
                            pygame.draw.rect(self.screen, (255, 255, 255), rect, 2)
                    else:
                        pygame.draw.rect(self.screen, (20, 12, 26), rect)
                        pygame.draw.rect(self.screen, (50, 35, 60), rect, 1)
                        unk = self.small.render("?", True, (55, 40, 65))
                        self.screen.blit(unk, (cx + CELL_W // 2 - unk.get_width() // 2,
                                               cy + CELL_H // 2 - unk.get_height() // 2))

        # Dye family column headers
        for di, dye in enumerate(_DYE_FAMILIES):
            hx = grid_x + (di + 1) * (CELL_W + GAP)
            dye_col = tuple(DYE_FAMILY_COLORS[dye])
            hs = self.small.render(DYE_FAMILY_DISPLAY[dye][:4].upper(), True, dye_col)
            self.screen.blit(hs, (hx + CELL_W // 2 - hs.get_width() // 2, gy0 + 8))

        # Detail panel for selected cell
        sel = self._textile_codex_selected
        if sel and sel in disc:
            parts = sel.split("_", 2)
            if len(parts) == 3:
                ftype, dye, otype = parts[0], parts[1], parts[2]
                dye_col = tuple(DYE_FAMILY_COLORS.get(dye, DYE_FAMILY_COLORS["natural"]))
                dpx = SCREEN_W - 230
                dpy = gy0 + 30
                dpw, dph = 220, 160
                pygame.draw.rect(self.screen, (22, 12, 30), (dpx, dpy, dpw, dph))
                pygame.draw.rect(self.screen, dye_col, (dpx, dpy, dpw, dph), 2)
                iy = dpy + 8

                def dline(txt, col=(220, 190, 250)):
                    nonlocal iy
                    s = self.small.render(txt, True, col)
                    self.screen.blit(s, (dpx + 8, iy))
                    iy += 18

                dline(OUTPUT_DISPLAY.get(otype, otype), dye_col)
                dline(f"{ftype.title()} · {DYE_FAMILY_DISPLAY.get(dye,'Natural')}", (200, 175, 220))
                dline("Discovered!", (120, 220, 140))

    def _draw_cheese_codex(self, player, gy0=58, gx_off=130):
        from cheese import _CODEX_BIOMES, BIOME_DISPLAY_NAMES, CHEESE_TYPE_DESCS, CHEESE_TYPE_COLORS
        disc = getattr(player, "discovered_cheese", set())

        _BG    = ( 38,  30,  10)
        _CELL  = ( 52,  42,  18)
        _TITLE = (245, 230, 160)
        _LABEL = (195, 170, 110)
        _DIM   = ( 90,  72,  40)

        gw = SCREEN_W - gx_off - 4
        cell_w, cell_h, gap = 120, 52, 6
        cols = max(1, gw // (cell_w + gap))

        cheese_types = list(CHEESE_TYPE_DESCS.keys())
        total = len(_CODEX_BIOMES) * len(cheese_types)
        disc_count = len(disc)

        # Header
        hl = self.small.render(f"Discovered: {disc_count} / {total}", True, _LABEL)
        self.screen.blit(hl, (gx_off + 8, gy0))

        # Grid: rows = biomes, cols = cheese types
        col_header_y = gy0 + 22
        for ci, ct in enumerate(cheese_types):
            hx = gx_off + 8 + ci * (cell_w + gap)
            col = CHEESE_TYPE_COLORS.get(ct, _CELL)
            hl2 = self.small.render(ct.replace("_", " ").title(), True, col)
            self.screen.blit(hl2, (hx, col_header_y))

        grid_y0 = col_header_y + 18
        self._cheese_codex_rects.clear()
        for ri, biome in enumerate(_CODEX_BIOMES):
            row_y = grid_y0 + ri * (cell_h + gap)
            # Row biome label
            bnm = BIOME_DISPLAY_NAMES.get(biome, biome)
            bl = self.small.render(bnm, True, _LABEL)
            self.screen.blit(bl, (gx_off, row_y + cell_h // 2 - bl.get_height() // 2))
            for ci, ct in enumerate(cheese_types):
                key = f"{biome}_{ct}"
                discovered = key in disc
                cx_ = gx_off + 8 + ci * (cell_w + gap)
                crect = pygame.Rect(cx_, row_y, cell_w, cell_h)
                self._cheese_codex_rects[key] = crect
                bg = _CELL if discovered else ( 28,  22,  10)
                pygame.draw.rect(self.screen, bg, crect)
                col = CHEESE_TYPE_COLORS.get(ct, _CELL)
                brd = col if discovered else _DIM
                pygame.draw.rect(self.screen, brd, crect, 2)
                if discovered:
                    ct_s = self.small.render(ct.replace("_", " ").title(), True, col)
                    self.screen.blit(ct_s, (cx_ + 4, row_y + 6))
                    b_s = self.small.render(bnm, True, _LABEL)
                    self.screen.blit(b_s, (cx_ + 4, row_y + 24))
                else:
                    unk = self.small.render("?", True, _DIM)
                    self.screen.blit(unk, (cx_ + cell_w // 2 - unk.get_width() // 2,
                                           row_y + cell_h // 2 - unk.get_height() // 2))

        # Detail panel for selected entry
        sel = self._cheese_codex_selected
        if sel and sel in disc:
            biome_, ct_ = sel.rsplit("_", 1)
            dpx = gx_off + cols * (cell_w + gap) + 12
            dpy = gy0 + 40
            dw, dh = 200, 120
            pygame.draw.rect(self.screen, _CELL, (dpx, dpy, dw, dh))
            col = CHEESE_TYPE_COLORS.get(ct_, _LABEL)
            pygame.draw.rect(self.screen, col, (dpx, dpy, dw, dh), 2)
            iy = dpy + 8

            def dline(txt, c=_LABEL):
                nonlocal iy
                s = self.small.render(txt, True, c)
                self.screen.blit(s, (dpx + 6, iy))
                iy += 16

            dline(ct_.replace("_", " ").title(), col)
            dline(BIOME_DISPLAY_NAMES.get(biome_, biome_), _TITLE)
            dline("Discovered!", (120, 220, 140))

    def _draw_jewelry_codex(self, player, gy0=58, gx_off=130):
        from jewelry import JEWELRY_TYPES, JEWELRY_TYPE_ORDER
        disc = getattr(player, "discovered_jewelry", set())
        n_disc = len(disc)

        _GOLD  = (220, 180, 60)
        _BG    = (22, 18, 8)
        _CELL  = (35, 28, 10)
        _LABEL = (195, 165, 80)

        sub = self.small.render(f"{n_disc} / {len(JEWELRY_TYPE_ORDER)} jewelry types crafted", True, _LABEL)
        self.screen.blit(sub, (gx_off + 8, gy0))

        CELL_W, CELL_H, GAP = 160, 110, 12
        gx0 = gx_off + 8
        gy  = gy0 + 22

        self._jewelry_codex_rects.clear()
        for ji, jkey in enumerate(JEWELRY_TYPE_ORDER):
            jdata = JEWELRY_TYPES[jkey]
            discovered = jkey in disc
            rx = gx0 + ji * (CELL_W + GAP)
            rect = pygame.Rect(rx, gy, CELL_W, CELL_H)
            self._jewelry_codex_rects[jkey] = rect
            selected = (self._jewelry_codex_selected == jkey)
            bg  = (50, 40, 14) if selected else _CELL
            bdr = _GOLD if selected else ((140, 115, 45) if discovered else (55, 45, 18))
            pygame.draw.rect(self.screen, bg, rect, border_radius=6)
            pygame.draw.rect(self.screen, bdr, rect, 2, border_radius=6)

            if discovered:
                nm = self.font.render(jdata["label"], True, _GOLD)
                self.screen.blit(nm, (rx + CELL_W // 2 - nm.get_width() // 2, gy + 10))
                self._draw_jw_icon(jkey, rx + CELL_W // 2, gy + 60, 22)
                slots_lbl = self.small.render(f"Up to {jdata['max_slots']} slots", True, _LABEL)
                self.screen.blit(slots_lbl, (rx + CELL_W // 2 - slots_lbl.get_width() // 2, gy + CELL_H - 20))
            else:
                unk = self.font.render("?", True, (70, 58, 25))
                self.screen.blit(unk, (rx + CELL_W // 2 - unk.get_width() // 2, gy + CELL_H // 2 - unk.get_height() // 2))

    def _draw_pottery_codex(self, player, gy0=58, gx_off=130):
        from pottery import CLAY_BIOME_PROFILES, BIOME_DISPLAY_NAMES, FIRING_LEVELS, GLAZE_TYPES
        _BG   = (30, 18, 8)
        _BDR  = (160, 110, 80)
        _CELL = (40, 25, 10)
        _TXT  = (210, 160, 110)
        _DIM  = (120, 85, 50)

        disc        = getattr(player, "discovered_pottery", set())
        all_biomes  = list(CLAY_BIOME_PROFILES.keys())
        fire_levels = FIRING_LEVELS[1:]  # skip "cracked"
        total       = len(all_biomes) * len(fire_levels)
        n_disc      = len(disc)

        sub = self.small.render(f"{n_disc} / {total} pottery types fired", True, _TXT)
        self.screen.blit(sub, (gx_off + 8, gy0))

        CELL_W, CELL_H, GAP = 120, 80, 10
        gx0 = gx_off + 8

        if not hasattr(self, '_pottery_codex_rects'):
            self._pottery_codex_rects = {}
        self._pottery_codex_rects.clear()

        for bi, biome in enumerate(all_biomes):
            # Column header
            bname = BIOME_DISPLAY_NAMES.get(biome, biome.title())
            bh = self.small.render(bname, True, _TXT)
            self.screen.blit(bh, (gx0 + bi * (CELL_W + GAP) + CELL_W // 2 - bh.get_width() // 2, gy0 + 18))
            for fi, level in enumerate(fire_levels):
                key = f"{biome}_{level}"
                rx  = gx0 + bi * (CELL_W + GAP)
                ry  = gy0 + 36 + fi * (CELL_H + GAP)
                rect = pygame.Rect(rx, ry, CELL_W, CELL_H)
                self._pottery_codex_rects[key] = rect
                found = key in disc

                bg  = (55, 35, 14) if found else _CELL
                bdr = _BDR if found else (70, 48, 28)
                pygame.draw.rect(self.screen, bg, rect, border_radius=4)
                pygame.draw.rect(self.screen, bdr, rect, 2, border_radius=4)

                if found:
                    lvl_lbl = self.small.render(level.title(), True, _TXT)
                    self.screen.blit(lvl_lbl, (rx + CELL_W // 2 - lvl_lbl.get_width() // 2, ry + 6))
                    # Mini vase silhouette
                    cx_c = rx + CELL_W // 2
                    profile = [3, 3, 5, 6, 6, 5, 4, 4, 5, 5, 4, 3]
                    row_h = 4
                    ty = ry + 24
                    for ri, rad in enumerate(profile):
                        w = rad * 3
                        pygame.draw.rect(self.screen, (160, 110, 80), (cx_c - w, ty + ri * row_h, w * 2, row_h - 1))
                else:
                    unk = self.font.render("?", True, (70, 48, 25))
                    self.screen.blit(unk, (rx + CELL_W // 2 - unk.get_width() // 2, ry + CELL_H // 2 - unk.get_height() // 2))

    def _draw_salt_codex(self, player, gy0=58, gx_off=130):
        disc = getattr(player, "discovered_salt_origins", set())

        _CELL  = (35, 33, 30)
        _TITLE = (235, 232, 215)
        _LABEL = (190, 185, 160)
        _DIM   = ( 85,  82,  75)

        total     = len(SALT_TYPE_ORDER)
        disc_count = len(disc)

        sub = self.small.render(f"Discovered: {disc_count} / {total}", True, _LABEL)
        self.screen.blit(sub, (gx_off + 8, gy0))

        cell_w, cell_h, gap = 115, 52, 6

        # Column headers (grades)
        col_hdr_y = gy0 + 22
        for ci, grade in enumerate(GRADES):
            hx = gx_off + 8 + ci * (cell_w + gap)
            col = SALT_OUTPUT_COLORS.get(f"{grade}_salt", _CELL)
            hl = self.small.render(grade.replace("_", " ").title(), True, col)
            self.screen.blit(hl, (hx, col_hdr_y))

        grid_y0 = col_hdr_y + 18
        self._salt_codex_rects.clear()
        for ri, biome in enumerate(SALT_CODEX_BIOMES):
            row_y = grid_y0 + ri * (cell_h + gap)
            bnm = SALT_BIOME_NAMES.get(biome, biome.replace("_", " ").title())
            bl = self.small.render(bnm, True, _LABEL)
            self.screen.blit(bl, (gx_off, row_y + cell_h // 2 - bl.get_height() // 2))
            for ci, grade in enumerate(GRADES):
                key = f"{biome}_{grade}"
                discovered = key in disc
                cx_ = gx_off + 8 + ci * (cell_w + gap)
                crect = pygame.Rect(cx_, row_y, cell_w, cell_h)
                self._salt_codex_rects[key] = crect
                col = SALT_OUTPUT_COLORS.get(f"{grade}_salt", _CELL)
                bg  = _CELL if discovered else (20, 18, 16)
                brd = col if discovered else _DIM
                pygame.draw.rect(self.screen, bg, crect)
                pygame.draw.rect(self.screen, brd, crect, 2)
                if discovered:
                    gn = self.small.render(grade.replace("_", " ").title(), True, col)
                    self.screen.blit(gn, (cx_ + 4, row_y + 6))
                    bn = self.small.render(bnm, True, _LABEL)
                    self.screen.blit(bn, (cx_ + 4, row_y + 24))
                else:
                    unk = self.small.render("?", True, _DIM)
                    self.screen.blit(unk, (cx_ + cell_w // 2 - unk.get_width() // 2,
                                           row_y + cell_h // 2 - unk.get_height() // 2))

        # Detail panel for selected entry
        sel = self._salt_codex_selected
        if sel and sel in disc:
            parts = sel.rsplit("_", 1)
            if len(parts) == 2:
                biome_, grade_ = parts[0], parts[1]
            else:
                biome_, grade_ = sel, ""
            dpx = gx_off + 8 + len(GRADES) * (cell_w + gap) + 12
            dpy = gy0 + 40
            dw2, dh2 = 200, 110
            col2 = SALT_OUTPUT_COLORS.get(f"{grade_}_salt", _LABEL)
            pygame.draw.rect(self.screen, _CELL, (dpx, dpy, dw2, dh2))
            pygame.draw.rect(self.screen, col2, (dpx, dpy, dw2, dh2), 2)
            iy2 = dpy + 8

            def dline(txt, c=_LABEL):
                nonlocal iy2
                s = self.small.render(txt, True, c)
                self.screen.blit(s, (dpx + 6, iy2))
                iy2 += 16

            dline(grade_.replace("_", " ").title(), col2)
            dline(SALT_BIOME_NAMES.get(biome_, biome_.replace("_", " ").title()), _TITLE)
            dline("Discovered!", (120, 220, 140))

    def _draw_pairings_codex(self, player, gy0=58, gx_off=130):
        from crossover import PAIRING_TABLE
        disc = getattr(player, "discovered_pairings", set())

        _BG       = (24, 18, 32)
        _TITLE    = (235, 220, 250)
        _LABEL    = (190, 175, 215)
        _DIM      = ( 95,  85, 110)
        _DISC_BRD = (185, 130, 230)
        _MULT     = (245, 200, 120)

        total = len(PAIRING_TABLE)
        sub = self.small.render(
            f"Discovered: {len(disc)} / {total}     Combine buffs from two systems for bonus duration.",
            True, _LABEL)
        self.screen.blit(sub, (gx_off + 8, gy0))

        row_y = gy0 + 26
        cell_w, cell_h, gap = 360, 46, 6

        for key, info in PAIRING_TABLE.items():
            discovered = info["name"] in disc
            rect = pygame.Rect(gx_off + 8, row_y, cell_w, cell_h)
            pygame.draw.rect(self.screen, _BG, rect)
            pygame.draw.rect(self.screen, _DISC_BRD if discovered else _DIM, rect, 2)
            if discovered:
                name_s = self.small.render(info["name"], True, _TITLE)
                self.screen.blit(name_s, (rect.x + 8, rect.y + 4))
                # Two systems → buff combo line
                parts = sorted(key, key=lambda t: t[0])
                combo = "  +  ".join(
                    f"{sys.title()}: {buff.replace('_', ' ').title()}"
                    for sys, buff in parts
                )
                combo_s = self.small.render(combo, True, _LABEL)
                self.screen.blit(combo_s, (rect.x + 8, rect.y + 22))
                mult_s = self.small.render(
                    f"x{info['duration_mult']:.2f}", True, _MULT)
                self.screen.blit(mult_s,
                    (rect.right - mult_s.get_width() - 8,
                     rect.y + cell_h // 2 - mult_s.get_height() // 2))
            else:
                q_s = self.small.render("???  +  ???", True, _DIM)
                self.screen.blit(q_s, (rect.x + 8, rect.y + cell_h // 2 - q_s.get_height() // 2))
            row_y += cell_h + gap
            if row_y > gy0 + 600:
                break  # avoid overflow on small screens

    def _draw_dog_codex(self, player, gy0=58, gx_off=130):
        from dogs import BREED_PROFILES
        from Render.dogs import draw_dog

        disc     = getattr(player, "discovered_dog_breeds", set())
        all_breeds = list(BREED_PROFILES.keys())
        total    = len(all_breeds)

        _BG    = (22, 16, 8)
        _TITLE = (215, 180, 110)
        _DIM   = (70, 55, 30)
        _DISC  = (180, 140, 65)

        sub = self.small.render(
            f"Discovered: {len(disc)} / {total}     Tame dogs to unlock their breed entry.",
            True, (170, 140, 80))
        self.screen.blit(sub, (gx_off + 8, gy0))

        cell_w, cell_h, gap_x, gap_y = 230, 80, 10, 8
        cols = max(1, (SCREEN_W - gx_off - 20) // (cell_w + gap_x))
        row_y = gy0 + 26

        for i, breed in enumerate(all_breeds):
            col_i  = i % cols
            row_i  = i // cols
            cx = gx_off + 8 + col_i * (cell_w + gap_x)
            cy = row_y + row_i * (cell_h + gap_y)

            discovered = breed in disc
            rect = pygame.Rect(cx, cy, cell_w, cell_h)
            pygame.draw.rect(self.screen, _BG, rect, border_radius=5)
            brd_col = _DISC if discovered else _DIM
            pygame.draw.rect(self.screen, brd_col, rect, 1, border_radius=5)

            if discovered:
                # Draw a small dog silhouette using breed coat color
                profile = BREED_PROFILES[breed]
                coat = profile.get("coat_colors", [(160, 100, 50)])[0]
                # Minimal stub dog object for rendering
                class _StubDog:
                    traits = {
                        "coat_color": coat,
                        "coat_pattern": "solid",
                        "coat_length": profile.get("coat_length", "short"),
                        "coat_type": "smooth",
                        "ear_type": profile.get("ear_type", "floppy"),
                        "tail_type": profile.get("tail_type", "long"),
                        "eye_color": "brown",
                        "size_class": profile.get("size_class", "medium"),
                    }
                    stay_mode = False
                    tamed = True
                    facing = 1
                draw_dog(self.screen, cx + 6, cy + 20, _StubDog(), scale=1.4, facing=1)

                name_s = self.small.render(breed, True, _TITLE)
                self.screen.blit(name_s, (cx + 56, cy + 6))
                biomes_str = ", ".join(sorted(profile["biomes"])[:3])
                bio_s = self.small.render(biomes_str[:28], True, (140, 115, 60))
                self.screen.blit(bio_s, (cx + 56, cy + 22))
                size_s = self.small.render(f"Size: {profile['size_class']}", True, (130, 105, 55))
                self.screen.blit(size_s, (cx + 56, cy + 38))
            else:
                q_s = self.small.render("???", True, _DIM)
                self.screen.blit(q_s, (cx + cell_w // 2 - q_s.get_width() // 2,
                                        cy + cell_h // 2 - q_s.get_height() // 2))

    def _draw_hunting_codex(self, player, gy0=58, gx_off=130):
        HUNTING_LOG_SPECIES = [
            ("bear",       "Bear",       "weight",        "lbs"),
            ("bighorn",    "Bighorn",    "horn_score",    "pts"),
            ("bison",      "Bison",      "weight",        "lbs"),
            ("boar",       "Boar",       "tusk_length",   "in"),
            ("crocodile",  "Crocodile",  "length",        "ft"),
            ("deer",       "Deer",       "antler_spread", "in"),
            ("duck",       "Duck",       "weight",        "lbs"),
            ("elk",        "Elk",        "antler_spread", "in"),
            ("fox",        "Fox",        "weight",        "lbs"),
            ("goose",      "Goose",      "weight",        "lbs"),
            ("hare",       "Hare",       "weight",        "lbs"),
            ("moose",      "Moose",      "antler_span",   "in"),
            ("musk_ox",    "Musk Ox",    "horn_spread",   "in"),
            ("pheasant",   "Pheasant",   "tail_length",   "in"),
            ("rabbit",     "Rabbit",     "weight",        "lbs"),
            ("turkey",     "Turkey",     "beard_length",  "in"),
            ("warthog",    "Warthog",    "tusk_length",   "in"),
            ("wolf",       "Wolf",       "weight",        "lbs"),
        ]

        STAT_LABELS = {
            "antler_spread": "Antler spread",
            "antler_span":   "Antler span",
            "tusk_length":   "Tusk length",
            "horn_score":    "Horn score",
            "horn_spread":   "Horn spread",
            "weight":        "Weight",
            "length":        "Body length",
            "tail_length":   "Tail length",
            "beard_length":  "Beard length",
        }

        _BG      = (28, 20, 10)
        _BORDER  = (100, 70, 35)
        _HUNTED  = (220, 170, 100)
        _DIM     = (80, 60, 35)
        _STAT    = (180, 140, 70)
        _COUNT   = (140, 105, 50)

        hunted    = getattr(player, "animals_hunted", {})
        trophies  = getattr(player, "hunt_trophies", {})
        total_killed = sum(hunted.values())

        sub = self.small.render(
            f"Total hunted: {total_killed}   —   Personal bests per species",
            True, _COUNT)
        self.screen.blit(sub, (gx_off + 8, gy0))

        ROW_H  = 36
        GAP    = 4
        col_w  = (SCREEN_W - gx_off - 24) // 2
        row_y  = gy0 + 24

        for i, (aid, label, stat_key, unit) in enumerate(HUNTING_LOG_SPECIES):
            col_i = i % 2
            row_i = i // 2
            cx = gx_off + 8 + col_i * (col_w + 8)
            cy = row_y + row_i * (ROW_H + GAP) - self._hunting_codex_scroll

            if cy + ROW_H < gy0 or cy > SCREEN_H:
                continue

            count = hunted.get(aid, 0)
            best  = trophies.get(aid, {}).get(stat_key, 0)

            rect = pygame.Rect(cx, cy, col_w, ROW_H)
            pygame.draw.rect(self.screen, _BG, rect, border_radius=4)
            brd = _HUNTED if count > 0 else _BORDER
            pygame.draw.rect(self.screen, brd, rect, 1, border_radius=4)

            name_col = _HUNTED if count > 0 else _DIM
            name_s = self.small.render(label, True, name_col)
            self.screen.blit(name_s, (cx + 8, cy + 4))

            count_s = self.small.render(f"×{count}", True, _COUNT)
            self.screen.blit(count_s, (cx + 8, cy + 18))

            if count > 0 and best > 0:
                stat_label = STAT_LABELS.get(stat_key, stat_key.replace("_", " ").title())
                stat_text  = f"Best {stat_label}: {best} {unit}"
                stat_s = self.small.render(stat_text, True, _STAT)
                self.screen.blit(stat_s, (cx + col_w // 2, cy + 4))

        rows = (len(HUNTING_LOG_SPECIES) + 1) // 2
        content_h = rows * (ROW_H + GAP) + 24
        visible_h = SCREEN_H - row_y
        self._max_hunting_codex_scroll = max(0, content_h - visible_h)

    # ------------------------------------------------------------------
    # Weapons codex
    # ------------------------------------------------------------------

    def _draw_weapons_codex(self, player, gy0=58, gx_off=0):
        from weapons import WEAPON_TYPES, MATERIAL_PROFILES, WEAPON_TYPE_ORDER, MATERIAL_ORDER, quality_tier
        ACCENT = (210, 195, 165)
        DIM    = (130, 120, 100)

        title = self.font.render("WEAPONS CODEX", True, ACCENT)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, gy0 + 4))

        crafted = getattr(player, "crafted_weapons", [])
        # Build lookup: (weapon_type, material) → best quality weapon
        best_by_key = {}
        for w in crafted:
            k = (w.weapon_type, w.material)
            if k not in best_by_key or w.quality > best_by_key[k].quality:
                best_by_key[k] = w

        CELL_W, CELL_H, GAP = 130, 44, 6
        total_w = len(MATERIAL_ORDER) * CELL_W + (len(MATERIAL_ORDER) - 1) * GAP
        gx0 = SCREEN_W // 2 - total_w // 2 + gx_off

        # Header row: material names
        for ci, mat in enumerate(MATERIAL_ORDER):
            col = MATERIAL_PROFILES[mat]["color"]
            x   = gx0 + ci * (CELL_W + GAP)
            lbl = self.font.render(MATERIAL_PROFILES[mat]["name"], True, col)
            self.screen.blit(lbl, (x + CELL_W // 2 - lbl.get_width() // 2, gy0 + 28))

        for ri, wtype in enumerate(WEAPON_TYPE_ORDER):
            row_y = gy0 + 52 + ri * (CELL_H + GAP)
            wt_lbl = self.small.render(WEAPON_TYPES[wtype]["name"], True, ACCENT)
            self.screen.blit(wt_lbl, (gx0 - wt_lbl.get_width() - 8, row_y + CELL_H // 2 - 6))

            for ci, mat in enumerate(MATERIAL_ORDER):
                col = MATERIAL_PROFILES[mat]["color"]
                x   = gx0 + ci * (CELL_W + GAP)
                r   = pygame.Rect(x, row_y, CELL_W, CELL_H)
                k   = (wtype, mat)
                best = best_by_key.get(k)
                discovered = best is not None

                bg = (28, 22, 14) if discovered else (18, 14, 10)
                bd = col if discovered else DIM
                pygame.draw.rect(self.screen, bg, r, border_radius=4)
                pygame.draw.rect(self.screen, bd, r, 1, border_radius=4)

                if discovered:
                    tier  = quality_tier(best.quality)
                    tier_lbl = self.small.render(tier, True, col)
                    self.screen.blit(tier_lbl, (x + CELL_W // 2 - tier_lbl.get_width() // 2,
                                                row_y + 6))
                    pct_lbl = self.small.render(f"{int(best.quality * 100)}%", True, col)
                    self.screen.blit(pct_lbl, (x + CELL_W // 2 - pct_lbl.get_width() // 2,
                                               row_y + 28))
                else:
                    unk = self.small.render("?", True, DIM)
                    self.screen.blit(unk, (x + CELL_W // 2 - unk.get_width() // 2,
                                          row_y + CELL_H // 2 - 8))

        total   = len(WEAPON_TYPE_ORDER) * len(MATERIAL_ORDER)
        disc    = len(best_by_key)
        summary = self.small.render(f"Crafted: {disc} / {total} combinations", True, DIM)
        self.screen.blit(summary, (SCREEN_W // 2 - summary.get_width() // 2, SCREEN_H - 24))
