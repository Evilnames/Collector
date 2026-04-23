import pygame
from constants import SCREEN_W, SCREEN_H, HOTBAR_SIZE, MAX_HEALTH
from items import ITEMS
from item_icons import render_item_icon


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
        hints = [
            ("R: Research", self.research_open or (
                research and any(research.can_unlock(nid, player.inventory, player.money)
                                 for nid in research.nodes))),
            ("I: Inventory",  self.inventory_open),
            ("C: Craft",      self.crafting_open),
            ("G: Collection",  self.collection_open),
            ("B: Animals",     self.breeding_open),
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
