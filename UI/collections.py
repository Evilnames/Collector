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
        n_coffee_owned = len(player.coffee_beans)
        total_collected = (len(player.rocks) + len(player.wildflowers) +
                           len(player.fossils) + len(player.gems) + n_mush_owned + n_coffee_owned)

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
            enc_titles = ["ROCK CODEX", "FLOWER CODEX", "MUSHROOM CODEX", "FOSSIL CODEX", "GEM CODEX", "BIRD CODEX", "FISH CODEX", "COFFEE CODEX"]
            enc_cols   = [(180, 220, 255), (180, 255, 180), (220, 210, 140), (210, 185, 140), (180, 245, 225), (140, 210, 255), (120, 185, 240), (210, 145, 60)]
            title_text = enc_titles[self._encyclopedia_cat]
            title_col  = enc_cols[self._encyclopedia_cat]
        else:
            title_text = "COLLECTION"
            title_col  = (200, 200, 255)
        title_s = self.font.render(title_text, True, title_col)
        self.screen.blit(title_s, (SCREEN_W // 2 - title_s.get_width() // 2, 4))

        SUB_Y = tab_y + TAB_H + 4   # 54
        SUB_H = 20
        GY0   = SUB_Y + SUB_H + 6   # 80

        # ---- Sub-button row ----
        if self._collection_tab == 0:
            # Filter buttons for the unified collection
            self._collection_filter_rects.clear()
            filter_defs = [
                ("all",       f"ALL ({total_collected})"),
                ("rocks",     f"ROCKS ({len(player.rocks)})"),
                ("flowers",   f"FLOWERS ({len(player.wildflowers)})"),
                ("fossils",   f"FOSSILS ({len(player.fossils)})"),
                ("gems",      f"GEMS ({len(player.gems)})"),
                ("mushrooms", f"MUSHROOMS ({n_mush_owned})"),
                ("coffee",    f"COFFEE ({n_coffee_owned})"),
            ]
            FILTER_THEME = {
                "all":       ((55, 55, 75),  (130, 130, 180), (200, 200, 240)),
                "rocks":     ((42, 52, 70),  (95,  138, 198), (175, 208, 248)),
                "flowers":   ((32, 58, 35),  (85,  178, 100), (168, 235, 178)),
                "fossils":   ((50, 40, 20),  (168, 140, 72),  (215, 182, 112)),
                "gems":      ((22, 48, 45),  (72,  195, 170), (145, 235, 215)),
                "mushrooms": ((40, 36, 16),  (148, 132, 56),  (198, 182, 105)),
                "coffee":    ((40, 25, 10),  (140,  90,  35), (210, 150,  70)),
            }
            fGAP = 6
            fW = min(148, (SCREEN_W - 20 - fGAP * (len(filter_defs) - 1)) // len(filter_defs))
            total_fw = len(filter_defs) * fW + (len(filter_defs) - 1) * fGAP
            fx0 = SCREEN_W // 2 - total_fw // 2
            for fi, (fkey, flabel) in enumerate(filter_defs):
                fx = fx0 + fi * (fW + fGAP)
                frect = pygame.Rect(fx, SUB_Y, fW, SUB_H)
                self._collection_filter_rects[fkey] = frect
                bg_d, brd_d, txt_d = FILTER_THEME[fkey]
                is_active_f = (self._collection_filter == fkey)
                if is_active_f:
                    fb = (min(255, bg_d[0] + 22), min(255, bg_d[1] + 22), min(255, bg_d[2] + 22))
                    fb_brd, fb_txt = brd_d, txt_d
                else:
                    fb = (bg_d[0] // 2, bg_d[1] // 2, bg_d[2] // 2)
                    fb_brd = (brd_d[0] // 2, brd_d[1] // 2, brd_d[2] // 2)
                    fb_txt = fb_brd
                pygame.draw.rect(self.screen, fb, frect)
                pygame.draw.rect(self.screen, fb_brd, frect, 2 if is_active_f else 1)
                fs = self.small.render(self._fit_label(flabel, fW - 6), True, fb_txt)
                self.screen.blit(fs, (fx + fW // 2 - fs.get_width() // 2,
                                       SUB_Y + SUB_H // 2 - fs.get_height() // 2))

        elif self._collection_tab == 1:
            # Encyclopedia sub-category buttons
            self._encyclopedia_cat_rects.clear()
            n_bird_disc  = len(player.birds_observed)
            n_bird_total = 85
            n_coffee_disc  = len(player.discovered_coffee_origins)
            n_coffee_total = len(COFFEE_TYPE_ORDER)
            enc_defs = [
                (0, f"ROCKS ({n_rock_disc}/{n_rock_total})"),
                (1, f"FLOWERS ({n_fl_disc}/{n_fl_total})"),
                (2, f"MUSHROOMS ({n_mush_disc}/{n_mush_total})"),
                (3, f"FOSSILS ({n_fossil_disc}/{n_fossil_total})"),
                (4, f"GEMS ({n_gem_disc}/{n_gem_total})"),
                (5, f"BIRDS ({n_bird_disc}/{n_bird_total})"),
                (6, f"FISH ({n_fish_disc}/{n_fish_total})"),
                (7, f"COFFEE ({n_coffee_disc}/{n_coffee_total})"),
            ]
            ENC_THEME = [
                ((42, 52, 70),  (95, 138, 198),  (175, 208, 248)),
                ((32, 58, 35),  (85, 178, 100),  (168, 235, 178)),
                ((40, 36, 16),  (148, 132, 56),  (198, 182, 105)),
                ((50, 40, 20),  (168, 140, 72),  (215, 182, 112)),
                ((22, 48, 45),  (72, 195, 170),  (145, 235, 215)),
                ((18, 40, 58),  (70, 150, 220),  (140, 210, 255)),
                ((18, 32, 50),  (55, 110, 185),  (120, 185, 240)),
                ((35, 22,  8),  (140,  90,  30), (210, 145,  60)),
            ]
            eGAP = 6
            eW = min(190, (SCREEN_W - 20 - eGAP * (len(enc_defs) - 1)) // len(enc_defs))
            total_ew = len(enc_defs) * eW + (len(enc_defs) - 1) * eGAP
            ex0 = SCREEN_W // 2 - total_ew // 2
            for ei, (cat_i, cat_label) in enumerate(enc_defs):
                ex = ex0 + ei * (eW + eGAP)
                erect = pygame.Rect(ex, SUB_Y, eW, SUB_H)
                self._encyclopedia_cat_rects[cat_i] = erect
                bg_d, brd_d, txt_d = ENC_THEME[cat_i]
                is_active_e = (self._encyclopedia_cat == cat_i)
                if is_active_e:
                    eb = (min(255, bg_d[0] + 22), min(255, bg_d[1] + 22), min(255, bg_d[2] + 22))
                    eb_brd, eb_txt = brd_d, txt_d
                else:
                    eb = (bg_d[0] // 2, bg_d[1] // 2, bg_d[2] // 2)
                    eb_brd = (brd_d[0] // 2, brd_d[1] // 2, brd_d[2] // 2)
                    eb_txt = eb_brd
                pygame.draw.rect(self.screen, eb, erect)
                pygame.draw.rect(self.screen, eb_brd, erect, 2 if is_active_e else 1)
                es = self.small.render(self._fit_label(cat_label, eW - 6), True, eb_txt)
                self.screen.blit(es, (ex + eW // 2 - es.get_width() // 2,
                                       SUB_Y + SUB_H // 2 - es.get_height() // 2))

        # ---- Content ----
        if self._collection_tab == 0:
            self._draw_collection_unified(player, GY0)
        elif self._collection_tab == 1:
            cat_draw = [
                self._draw_codex,
                self._draw_flower_codex,
                self._draw_mushroom_codex,
                self._draw_fossil_codex,
                self._draw_gem_codex,
                self._draw_bird_codex,
                self._draw_fish_codex,
                self._draw_coffee_codex,
            ]
            if 0 <= self._encyclopedia_cat < len(cat_draw):
                cat_draw[self._encyclopedia_cat](player, gy0=GY0)
        else:
            self._draw_achievements()

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

    def _draw_collection_unified(self, player, gy0=80):
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

        if not items:
            msg = self.font.render("Nothing collected yet!", True, (80, 80, 90))
            self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2))
            return

        CELL, GAP, COLS = 82, 8, 8
        gx0 = (SCREEN_W - (COLS * CELL + (COLS - 1) * GAP)) // 2

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
                # Draw a simple coffee bean icon
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
        else:  # mushroom
            bid = sel_key
            pygame.draw.rect(self.screen, (16, 14, 8), (dx, dy2, dw, dh))
            pygame.draw.rect(self.screen, (165, 148, 60), (dx, dy2, dw, dh), 2)
            self.screen.blit(render_mushroom_preview(bid, 80), (dx + dw // 2 - 40, dy2 + 8))
            dlabel(BLOCKS[bid]["name"], (235, 220, 130))
            drop = BLOCKS[bid].get("drop", "")
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

    def _draw_codex(self, player, gy0=58):
        CELL, GAP, COLS = 82, 8, 6
        gx0 = (SCREEN_W - (COLS * CELL + (COLS - 1) * GAP)) // 2

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

    def _draw_flower_codex(self, player, gy0=58):
        CELL, GAP, COLS = 82, 8, 6
        gx0 = (SCREEN_W - (COLS * CELL + (COLS - 1) * GAP)) // 2

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

    def _draw_mushroom_codex(self, player, gy0=58):
        CELL, GAP, COLS = 82, 8, 5
        gx0 = (SCREEN_W - (COLS * CELL + (COLS - 1) * GAP)) // 2

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

    def _draw_fossil_codex(self, player, gy0=58):
        CELL, GAP, COLS = 82, 8, 6
        gx0 = (SCREEN_W - (COLS * CELL + (COLS - 1) * GAP)) // 2

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

    def _draw_gem_codex(self, player, gy0=58):
        CELL, GAP, COLS = 82, 8, 10
        gx0 = (SCREEN_W - (COLS * CELL + (COLS - 1) * GAP)) // 2

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


    def _draw_bird_codex(self, player, gy0=58):
        from birds import ALL_SPECIES
        RARITY_BIRD_COLS = {"common": (120, 170, 120), "uncommon": (100, 170, 220),
                            "rare": (180, 120, 230)}

        CELL, GAP, COLS = 120, 10, 6
        ROW_H = CELL + GAP
        gx0 = (SCREEN_W - (COLS * CELL + (COLS - 1) * GAP)) // 2
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
    # Fish codex
    # ------------------------------------------------------------------

    def _draw_fish_codex(self, player, gy0=58):
        CELL, GAP, COLS = 74, 6, 9
        ROW_H    = CELL + GAP
        HDR_H    = 26
        gx0      = (SCREEN_W - (COLS * CELL + (COLS - 1) * GAP)) // 2
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
    # Coffee codex
    # ------------------------------------------------------------------

    def _draw_coffee_codex(self, player, gy0=58):
        BIOMES = ["tropical", "jungle", "savanna", "wetland", "arid_steppe", "canyon", "beach"]
        ROASTS = ["light", "medium", "dark", "charred", "green"]
        COLS   = len(ROASTS)
        CELL_W, CELL_H, GAP = 110, 68, 6
        HDR_H  = 22
        gx0    = (SCREEN_W - (COLS * CELL_W + (COLS - 1) * GAP)) // 2

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
            self.screen.blit(bl, (10, cy + (CELL_H - bl.get_height()) // 2))
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
