import pygame
from constants import SCREEN_W, SCREEN_H
from beekeeping import BIOME_DISPLAY_NAMES, generate_flavor_notes, get_honey_item_id, get_quality_tier


class BeekeepingMixin:

    # ── Drawing ────────────────────────────────────────────────────────────

    def _draw_beehive(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("BEEHIVE", True, (240, 200, 60))
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, (140, 120, 60))
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        if self._hive_phase == "inspect":
            self._draw_hive_inspect(player)
        elif self._hive_phase == "spinning":
            self._draw_hive_spin(player, dt)
        elif self._hive_phase == "result":
            self._draw_hive_result(player)

    def _draw_hive_inspect(self, player):
        from blocks import BEEHIVE_BLOCK
        bx, by = self._hive_bx, self._hive_by
        progress = player.world._hive_progress.get((bx, by), 0.0)
        biodome   = player.world.get_biodome(bx)
        display   = BIOME_DISPLAY_NAMES.get(biodome, biodome.replace("_", " ").title())

        cx = SCREEN_W // 2

        # Hive icon circle
        pygame.draw.circle(self.screen, (210, 175, 60), (cx, 70), 32)
        pygame.draw.circle(self.screen, (240, 210, 90), (cx, 70), 32, 3)
        lbl = self.small.render(display, True, (255, 235, 150))
        self.screen.blit(lbl, (cx - lbl.get_width() // 2, 108))

        # Progress bar
        BAR_W, BAR_H = 340, 20
        bx0 = cx - BAR_W // 2
        by0 = 136
        pygame.draw.rect(self.screen, (40, 32, 10), (bx0, by0, BAR_W, BAR_H))
        pygame.draw.rect(self.screen, (160, 130, 40), (bx0, by0, BAR_W, BAR_H), 2)
        fill_col = (230, 185, 50) if progress >= 1.0 else (180, 145, 35)
        pygame.draw.rect(self.screen, fill_col, (bx0, by0, int(BAR_W * progress), BAR_H))
        prog_lbl = self.small.render("Ready!" if progress >= 1.0 else f"{progress:.0%} full", True,
                                     (255, 240, 160) if progress >= 1.0 else (200, 170, 80))
        self.screen.blit(prog_lbl, (cx - prog_lbl.get_width() // 2, by0 + 2))

        # Flower info
        fc = self._hive_flower_count
        fd = self._hive_flower_diversity
        flower_lbl = self.small.render(
            f"Nearby wildflower displays: {fc}  |  Flower types: {fd}", True, (200, 220, 160))
        self.screen.blit(flower_lbl, (cx - flower_lbl.get_width() // 2, 168))

        rate_lbl = self.small.render(
            "Production rate: " + ("fast" if fc >= 6 else "moderate" if fc >= 2 else "slow"), True,
            (170, 190, 130))
        self.screen.blit(rate_lbl, (cx - rate_lbl.get_width() // 2, 186))

        tip = self.small.render("Place wildflower displays nearby to boost production.", True, (140, 155, 110))
        self.screen.blit(tip, (cx - tip.get_width() // 2, 206))

        # Honeycomb in inventory
        hc_count = player.inventory.get("honeycomb_raw", 0)
        hc_lbl = self.small.render(f"Honeycomb in bag: {hc_count}", True, (230, 200, 110))
        self.screen.blit(hc_lbl, (cx - hc_lbl.get_width() // 2, 234))

        # Harvest button
        harvest_active = progress >= 1.0
        self._hive_harvest_btn = pygame.Rect(cx - 90, 268, 180, 36)
        hcol = (80, 60, 15) if not harvest_active else (170, 130, 25)
        pygame.draw.rect(self.screen, hcol, self._hive_harvest_btn)
        pygame.draw.rect(self.screen, (220, 175, 50) if harvest_active else (100, 80, 30), self._hive_harvest_btn, 2)
        hl = self.font.render("HARVEST HONEYCOMB", True, (255, 235, 130) if harvest_active else (120, 100, 50))
        self.screen.blit(hl, (self._hive_harvest_btn.centerx - hl.get_width() // 2,
                               self._hive_harvest_btn.centery - hl.get_height() // 2))

        # Extract button
        extract_active = hc_count >= 1
        self._hive_extract_btn = pygame.Rect(cx - 90, 316, 180, 36)
        ecol = (70, 50, 10) if not extract_active else (150, 110, 20)
        pygame.draw.rect(self.screen, ecol, self._hive_extract_btn)
        pygame.draw.rect(self.screen, (200, 160, 45) if extract_active else (90, 70, 25), self._hive_extract_btn, 2)
        el = self.font.render("EXTRACT HONEY", True, (240, 215, 110) if extract_active else (110, 90, 40))
        self.screen.blit(el, (self._hive_extract_btn.centerx - el.get_width() // 2,
                               self._hive_extract_btn.centery - el.get_height() // 2))

        hint_e = self.small.render("Extracts 1 honeycomb → honey + wax", True, (155, 135, 60))
        self.screen.blit(hint_e, (cx - hint_e.get_width() // 2, 358))

    def _draw_hive_spin(self, player, dt):
        # Physics update
        if self._hive_spin_held:
            self._hive_spin_speed = min(1.0, self._hive_spin_speed + 0.75 * dt)
        else:
            self._hive_spin_speed = max(0.0, self._hive_spin_speed - 0.40 * dt)

        sp = self._hive_spin_speed
        self._hive_spin_time += dt

        # Accumulate time in target zone
        if 0.30 <= sp <= 0.68:
            self._hive_spin_time_good += dt
        elif sp > 0.68:
            self._hive_spin_over_penalty = min(5, self._hive_spin_over_penalty + int(dt * 2))

        # Auto-finish after 20s
        if self._hive_spin_time >= 20.0:
            self._finish_extraction(player)
            return

        cx = SCREEN_W // 2

        # Speed gauge (horizontal)
        GAUGE_W, GAUGE_H = 400, 28
        gx0 = cx - GAUGE_W // 2
        gy0 = SCREEN_H // 2 - 60
        pygame.draw.rect(self.screen, (30, 22, 8), (gx0, gy0, GAUGE_W, GAUGE_H))
        pygame.draw.rect(self.screen, (110, 85, 30), (gx0, gy0, GAUGE_W, GAUGE_H), 2)

        # Zone colours
        lo_x = gx0 + int(GAUGE_W * 0.30)
        hi_x = gx0 + int(GAUGE_W * 0.68)
        ov_x = gx0 + int(GAUGE_W * 0.85)
        pygame.draw.rect(self.screen, (35, 80, 40), (lo_x, gy0, hi_x - lo_x, GAUGE_H))          # green
        pygame.draw.rect(self.screen, (95, 80, 30), (hi_x, gy0, ov_x - hi_x, GAUGE_H))           # yellow
        pygame.draw.rect(self.screen, (100, 28, 28), (ov_x, gy0, gx0 + GAUGE_W - ov_x, GAUGE_H)) # red

        # Needle
        nx = gx0 + int(GAUGE_W * sp)
        pygame.draw.rect(self.screen, (240, 210, 100), (nx - 4, gy0 - 4, 8, GAUGE_H + 8))

        zone_lbl = self.small.render("Slow   |   Optimal   |   Fast   |   Over", True, (180, 155, 70))
        self.screen.blit(zone_lbl, (gx0, gy0 - 20))
        spd_lbl = self.small.render(f"Speed: {sp:.0%}", True, (240, 215, 100))
        self.screen.blit(spd_lbl, (gx0, gy0 + GAUGE_H + 6))

        # Time progress
        TIME_Y = SCREEN_H - 60
        total = 20.0
        TIME_W = SCREEN_W - 200
        tx0 = cx - TIME_W // 2
        pygame.draw.rect(self.screen, (30, 22, 8), (tx0, TIME_Y, TIME_W, 16))
        pygame.draw.rect(self.screen, (110, 85, 30), (tx0, TIME_Y, TIME_W, 16), 2)
        pygame.draw.rect(self.screen, (200, 165, 50),
                         (tx0, TIME_Y, int(TIME_W * self._hive_spin_time / total), 16))
        tl = self.small.render(f"{self._hive_spin_time:.1f}s / {total:.0f}s", True, (200, 170, 70))
        self.screen.blit(tl, (cx - tl.get_width() // 2, TIME_Y + 18))

        inst = self.small.render("Hold SPACE / click SPIN to spin the extractor.  Press ENTER / click STOP to finish.", True, (170, 145, 60))
        self.screen.blit(inst, (cx - inst.get_width() // 2, TIME_Y - 30))

        stop_rect = pygame.Rect(SCREEN_W - 150, SCREEN_H - 56, 130, 32)
        pygame.draw.rect(self.screen, (60, 45, 10), stop_rect)
        pygame.draw.rect(self.screen, (190, 155, 40), stop_rect, 2)
        sl = self.font.render("STOP", True, (240, 210, 90))
        self.screen.blit(sl, (stop_rect.centerx - sl.get_width() // 2, stop_rect.centery - sl.get_height() // 2))
        self._hive_stop_btn = stop_rect

        spin_rect = pygame.Rect(SCREEN_W - 150, SCREEN_H - 96, 130, 32)
        scol = (130, 100, 25) if self._hive_spin_held else (80, 60, 12)
        pygame.draw.rect(self.screen, scol, spin_rect)
        pygame.draw.rect(self.screen, (220, 185, 60), spin_rect, 2)
        spnl = self.font.render("SPIN", True, (255, 235, 130))
        self.screen.blit(spnl, (spin_rect.centerx - spnl.get_width() // 2, spin_rect.centery - spnl.get_height() // 2))
        self._hive_spin_btn = spin_rect

    def _draw_hive_result(self, player):
        cx = SCREEN_W // 2
        jar = self._hive_result_jar
        if not jar:
            self._hive_phase = "inspect"
            return

        pygame.draw.circle(self.screen, (210, 165, 40), (cx, 90), 36)
        pygame.draw.circle(self.screen, (240, 200, 70), (cx, 90), 36, 3)

        iy = 142

        def rline(t, col=(230, 195, 80)):
            nonlocal iy
            s = self.font.render(t, True, col)
            self.screen.blit(s, (cx - s.get_width() // 2, iy))
            iy += 28

        def sline(t, col=(185, 155, 65)):
            nonlocal iy
            s = self.small.render(t, True, col)
            self.screen.blit(s, (cx - s.get_width() // 2, iy))
            iy += 18

        display = BIOME_DISPLAY_NAMES.get(jar.origin_biome, jar.origin_biome.replace("_", " ").title())
        tier = get_quality_tier(jar.quality)
        rline(f"{display} Honey  ({tier.title()})", (255, 240, 150))

        ss = self._render_stars(self.font, jar.quality)
        self.screen.blit(ss, (cx - ss.get_width() // 2, iy))
        iy += 28

        sline(f"Dominant flower: {jar.dominant_flower.replace('_', ' ').title()}")
        sline(f"Flower diversity: {jar.flower_diversity}")
        sline(f"Sweetness {jar.sweetness:.0%}  |  Floral {jar.floral:.0%}  |  Earthy {jar.earthiness:.0%}")
        if jar.flavor_notes:
            sline("Notes: " + ", ".join(jar.flavor_notes))
        iy += 8
        sline("→ Honey Jar added to collection", (180, 215, 140))
        sline("→ Beeswax added to bag", (180, 210, 150))

        done_rect = pygame.Rect(cx - 70, iy + 16, 140, 34)
        pygame.draw.rect(self.screen, (50, 38, 10), done_rect)
        pygame.draw.rect(self.screen, (200, 165, 45), done_rect, 2)
        dl = self.font.render("DONE", True, (240, 210, 90))
        self.screen.blit(dl, (done_rect.centerx - dl.get_width() // 2, done_rect.centery - dl.get_height() // 2))
        self._hive_done_btn = done_rect

    # ── Click handlers ─────────────────────────────────────────────────────

    def _handle_beehive_click(self, pos, player):
        if self._hive_phase == "inspect":
            if getattr(self, "_hive_harvest_btn", None) and self._hive_harvest_btn.collidepoint(pos):
                self._do_harvest(player)
            elif getattr(self, "_hive_extract_btn", None) and self._hive_extract_btn.collidepoint(pos):
                self._start_extraction(player)
        elif self._hive_phase == "spinning":
            if getattr(self, "_hive_stop_btn", None) and self._hive_stop_btn.collidepoint(pos):
                self._finish_extraction(player)
            elif getattr(self, "_hive_spin_btn", None) and self._hive_spin_btn.collidepoint(pos):
                self._hive_spin_held = True
        elif self._hive_phase == "result":
            if getattr(self, "_hive_done_btn", None) and self._hive_done_btn.collidepoint(pos):
                self._hive_phase = "inspect"
                self._hive_result_jar = None

    def _do_harvest(self, player):
        bx, by = self._hive_bx, self._hive_by
        progress = player.world._hive_progress.get((bx, by), 0.0)
        if progress < 1.0:
            return
        fd = self._hive_flower_diversity
        count = 1 + fd // 3
        for _ in range(count):
            player._add_item("honeycomb_raw")
        player.world._hive_progress[(bx, by)] = 0.0
        player.pending_notifications.append(("Beekeeping", "Honeycomb Harvested", None))

    def _start_extraction(self, player):
        if player.inventory.get("honeycomb_raw", 0) < 1:
            return
        self._hive_spin_speed = 0.0
        self._hive_spin_held = False
        self._hive_spin_time = 0.0
        self._hive_spin_time_good = 0.0
        self._hive_spin_over_penalty = 0
        self._hive_phase = "spinning"

    def _finish_extraction(self, player):
        total = max(1.0, self._hive_spin_time)
        quality = (self._hive_spin_time_good / total) - self._hive_spin_over_penalty * 0.12
        quality = max(0.0, min(1.0, quality))

        # Consume one honeycomb
        if player.inventory.get("honeycomb_raw", 0) >= 1:
            player.inventory["honeycomb_raw"] -= 1
            if player.inventory["honeycomb_raw"] == 0:
                del player.inventory["honeycomb_raw"]

        biodome = player.world.get_biodome(self._hive_bx)
        jar = player._honey_gen.generate(biodome, self._hive_flower_diversity)
        jar.quality = quality
        jar.flavor_notes = generate_flavor_notes(jar)
        player.honey_jars.append(jar)

        item_id = get_honey_item_id(quality)
        player._add_item(item_id)
        player._add_item("beeswax")

        tier = get_quality_tier(quality)
        player.discovered_honeys.add(f"{jar.origin_biome}_{tier}")
        player.pending_notifications.append(("Beekeeping", f"{item_id.replace('_', ' ').title()}", None))

        self._hive_result_jar = jar
        self._hive_phase = "result"

    def _open_beehive(self, bx, by, player):
        """Called when player opens a BEEHIVE_BLOCK. Scans nearby flowers."""
        from blocks import WILDFLOWER_DISPLAY_BLOCK
        self._hive_bx = bx
        self._hive_by = by
        self._hive_phase = "inspect"
        self._hive_result_jar = None

        flower_count = 0
        flower_set = set()
        for dx in range(-8, 9):
            for dy in range(-3, 4):
                if player.world._chunk_get(bx + dx, by + dy) == WILDFLOWER_DISPLAY_BLOCK:
                    flower_count += 1
                    key = (bx + dx, by + dy)
                    wf_data = player.world.wildflower_display_data.get(key)
                    if wf_data:
                        ftype = wf_data.get("flower_type", "")
                        if ftype:
                            flower_set.add(ftype)
        self._hive_flower_count = flower_count
        self._hive_flower_diversity = len(flower_set)

    # ── Key handlers ───────────────────────────────────────────────────────

    def handle_beehive_keydown(self, key, player):
        if self._hive_phase == "spinning":
            if key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self._finish_extraction(player)

    def handle_beehive_keys(self, keys, dt, player):
        if self._hive_phase == "spinning":
            self._hive_spin_held = bool(keys[pygame.K_SPACE])
