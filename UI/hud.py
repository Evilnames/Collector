import pygame
from constants import SCREEN_W, SCREEN_H, HOTBAR_SIZE, MAX_HEALTH, MAX_BREATH
from items import ITEMS
from item_icons import render_item_icon
from block_shapes import SHAPE_VARIANTS, draw_shape_preview

_MOISTURE_LABELS = {
    (0, 3): "dry / arid",
    (1, 4): "lightly watered",
    (2, 5): "moderate moisture",
    (3, 6): "well watered",
    (5, 8): "wet / flooded",
}

def _moisture_label(lo, hi):
    return _MOISTURE_LABELS.get((lo, hi), "wide tolerance")


class HUDMixin:

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
        if frac > 0.75:
            label, label_col = "Full",      (180, 255, 120)
        elif frac > 0.5:
            label, label_col = "Satisfied", (230, 255, 100)
        elif frac > 0.25:
            label, label_col = "Hungry",    (255, 180,  40)
        else:
            label, label_col = "Starving",  (255,  60,  40)
        txt = self.small.render(f"Hunger: {label}", True, label_col)
        self.screen.blit(txt, (x + 4, y + 2))

    def _draw_breath(self, player):
        if player.breath >= MAX_BREATH and not player._head_in_water():
            return
        bw, bh = 180, 18
        x, y = 10, 58
        pygame.draw.rect(self.screen, (10, 25, 50), (x, y, bw, bh))
        frac = max(0.0, player.breath / MAX_BREATH)
        br_w = int(bw * frac)
        r = int(60 + 40 * (1.0 - frac))
        g = int(180 * frac + 60)
        b = int(220 * frac + 30)
        pygame.draw.rect(self.screen, (r, g, b), (x, y, br_w, bh))
        pygame.draw.rect(self.screen, (200, 220, 240), (x, y, bw, bh), 1)
        if frac > 0.66:
            label, label_col = "Breath: Full",    (160, 230, 255)
        elif frac > 0.33:
            label, label_col = "Breath: Holding", (200, 220, 255)
        elif frac > 0.0:
            label, label_col = "Breath: Gasping", (255, 180,  80)
        else:
            label, label_col = "Drowning!",       (255,  60,  40)
        txt = self.small.render(label, True, label_col)
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
                    # Crop tooltip: show moisture preference for seed items
                    place_block = item.get("place_block")
                    if place_block is not None:
                        import soil as _soil
                        prefs = _soil.CROP_PREFERENCES.get(place_block)
                        if prefs is not None:
                            m_lo, m_hi = prefs["moisture"]
                            if place_block in player.known_crops:
                                hint = f"Moisture: {m_lo}-{m_hi}  Drain: {prefs['fertility_drain']}/harvest"
                            else:
                                hint = f"Likes: {_moisture_label(m_lo, m_hi)}"
                            is_premium = item.get("premium_seed", False)
                            hint_col = (255, 220, 100) if is_premium else (140, 210, 170)
                            hint_txt = self.small.render(hint, True, hint_col)
                            hx = (SCREEN_W - hint_txt.get_width()) // 2
                            self.screen.blit(hint_txt, (hx, y - 34))

    def _draw_bg_mode_indicator(self):
        slot_sz = 48
        y = SCREEN_H - slot_sz - 10
        txt = self.small.render("[ BG MODE ]", True, (120, 180, 255))
        x = (SCREEN_W - txt.get_width()) // 2
        self.screen.blit(txt, (x, y - txt.get_height() - 6))

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
        e_active = (self.npc_open or self.refinery_open or self.chest_open
                    or self.garden_open or nearby_bed is not None)
        research_glow = self.research_open or (
            research and any(research.can_unlock(nid, player.inventory, player.money)
                             for nid in research.nodes))
        wire_mode = getattr(player.world, "wire_mode", False) if hasattr(player, "world") else False
        pipe_mode = getattr(player.world, "pipe_mode", False) if hasattr(player, "world") else False
        hints = [
            ("R",  "Research",   research_glow),
            ("I",  "Inventory",  self.inventory_open),
            ("C",  "Craft",      self.crafting_open),
            ("G",  "Collection", self.collection_open),
            ("B",  "Animals",    self.breeding_open),
            ("E",  "Interact",   e_active),
            ("\\", "Wire Mode",  wire_mode),
            ("P",  "Pipe Mode",  pipe_mode),
            ("`",  "Cheats",     self.cheat_open),
        ]
        collapsed = getattr(self, "_hints_collapsed", False)

        panel_w   = 168
        title_h   = 22
        row_h     = 18
        pad_x     = 10
        body_h    = (len(hints) * row_h) + 10
        panel_h   = title_h + (0 if collapsed else body_h)
        panel_x   = SCREEN_W - panel_w - 8
        panel_y   = 64

        bg = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        bg.fill((18, 22, 30, 200))
        self.screen.blit(bg, (panel_x, panel_y))
        pygame.draw.rect(self.screen, (90, 110, 140),
                         (panel_x, panel_y, panel_w, panel_h), 1)

        # Title bar (clickable to collapse/expand)
        title_rect = pygame.Rect(panel_x, panel_y, panel_w, title_h)
        pygame.draw.rect(self.screen, (40, 55, 80), title_rect)
        pygame.draw.line(self.screen, (90, 110, 140),
                         (panel_x, panel_y + title_h),
                         (panel_x + panel_w, panel_y + title_h))
        self._hints_toggle_rect = title_rect
        chev = "▸" if collapsed else "▾"
        title_txt = self.small.render(f"{chev}  Controls", True, (220, 230, 245))
        self.screen.blit(title_txt, (panel_x + pad_x, panel_y + 4))

        if collapsed:
            return

        y = panel_y + title_h + 6
        key_col_x = panel_x + pad_x
        lbl_col_x = panel_x + pad_x + 22
        for key, label, active in hints:
            key_color   = (255, 220, 90)  if active else (170, 180, 200)
            label_color = (240, 230, 140) if active else (150, 155, 170)
            ktxt = self.small.render(key, True, key_color)
            ltxt = self.small.render(label, True, label_color)
            self.screen.blit(ktxt, (key_col_x, y))
            self.screen.blit(ltxt, (lbl_col_x, y))
            y += row_h

        flag_y = panel_y + panel_h + 4
        if player.spawn_x is not None:
            sp = self.small.render("* Bed spawn set", True, (120, 220, 130))
            self.screen.blit(sp, (SCREEN_W - sp.get_width() - 10, flag_y))
            flag_y += 16
        if player.god_mode:
            god = self.small.render("GOD MODE", True, (255, 220, 50))
            self.screen.blit(god, (SCREEN_W - god.get_width() - 10, flag_y))

    def _draw_shape_brush(self, player):
        """Bottom-right shape brush indicator: strip of 5 thumbnails + label."""
        from items import ITEMS as _ITEMS
        from blocks import BLOCKS as _BLOCKS

        # Determine current block colour for preview
        item_id = player.hotbar[player.selected_slot]
        block_color = (160, 168, 178)   # neutral steel-grey fallback
        if item_id and item_id in _ITEMS:
            place_block = _ITEMS[item_id].get("place_block")
            if place_block and place_block in _BLOCKS:
                bc = _BLOCKS[place_block].get("color")
                if bc:
                    block_color = bc
            else:
                block_color = _ITEMS[item_id].get("color", block_color)

        n_total = len(SHAPE_VARIANTS)
        cur = player.shape_idx % n_total
        cur_shape, cur_rot, cur_label = SHAPE_VARIANTS[cur]

        # Layout — 5 thumbnails centred on current
        thumb = 28
        gap = 3
        n_visible = 5
        panel_w = n_visible * (thumb + gap) - gap + 16
        panel_h = thumb + 36
        px = SCREEN_W - panel_w - 8
        slot_sz = 48
        py = SCREEN_H - slot_sz - 10 - panel_h - 6

        # Panel background
        bg = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        bg.fill((18, 22, 30, 200))
        self.screen.blit(bg, (px, py))
        pygame.draw.rect(self.screen, (80, 92, 108), (px, py, panel_w, panel_h), 1)

        # Label row
        label_surf = self.small.render(cur_label, True, (220, 228, 240))
        lx = px + (panel_w - label_surf.get_width()) // 2
        self.screen.blit(label_surf, (lx, py + 3))

        # Thumbnail row
        thumb_y = py + 18
        half = n_visible // 2
        for slot_i in range(n_visible):
            variant_i = (cur - half + slot_i) % n_total
            v_shape, v_rot, _ = SHAPE_VARIANTS[variant_i]
            cx = px + 8 + slot_i * (thumb + gap) + thumb // 2
            cy = thumb_y + thumb // 2
            draw_shape_preview(
                self.screen, v_shape, v_rot, block_color,
                cx, cy, thumb, highlight=(slot_i == half),
            )

        # Key hint
        hint = self.small.render("[Tab] cycle", True, (100, 108, 118))
        hx = px + (panel_w - hint.get_width()) // 2
        self.screen.blit(hint, (hx, py + panel_h - 13))

    def handle_hints_click(self, pos):
        rect = getattr(self, "_hints_toggle_rect", None)
        if rect is not None and rect.collidepoint(pos):
            self._hints_collapsed = not getattr(self, "_hints_collapsed", False)
            return True
        return False
