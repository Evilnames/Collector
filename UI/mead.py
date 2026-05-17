import pygame
from constants import SCREEN_W, SCREEN_H
from mead import (
    MEAD_ADDITIVES, MEAD_STYLE_NAMES,
    YEAST_TYPES, BIOME_DISPLAY_NAMES, BUFF_DESCS, MEAD_BUFFS, _CODEX_BIOMES,
    apply_stir_result, apply_condition_result, get_bottle_output_id,
)

# Stir mini-game constants
_STIR_PHASE_TIMES   = (8.0, 12.0)   # seconds per phase (oxygenate, blend)
_STIR_TOTAL         = sum(_STIR_PHASE_TIMES)
_STIR_ZONES         = ((0.65, 0.85), (0.25, 0.45))  # good zone per phase
_STIR_OVER_ZONE     = 0.92
_SPEED_RISE         = 1.5    # per second while held
_SPEED_FALL         = (0.9, 1.8)  # per second when released (phase 0, phase 1)

# Conditioning constants
_COND_DURATION      = 22.0   # seconds to fill
_RACK_WINDOW        = (0.40, 0.65)
_RACK_BONUS         = 0.12

_TIER_COLORS = {
    "base":    (210, 155,  45),
    "fine":    (225, 170,  55),
    "reserve": (245, 195,  70),
}
_TIER_LABEL = {"base": "Base", "fine": "Fine", "reserve": "Reserve"}


class MeadMixin:

    # ── Open helpers ─────────────────────────────────────────────────────────

    def _open_mead_vat(self, bx, by, player):
        self.refinery_open    = True
        self.refinery_block_id = self._mead_vat_bid()
        self._mead_vat_phase  = "select_honey"
        self._mead_honey_sel  = None
        self._mead_add_sel    = "none"
        self._mead_yeast_sel  = "wine"
        self._mead_stir_speed = 0.0
        self._mead_stir_held  = False
        self._mead_stir_phase = 0
        self._mead_stir_elapsed = 0.0
        self._mead_stir_good    = 0.0
        self._mead_batch_wip  = None
        self._mead_result_item = None

    def _open_mead_cellar(self, bx, by, player):
        self.refinery_open     = True
        self.refinery_block_id = self._mead_cellar_bid()
        self._mead_cellar_phase = "select"
        self._mead_cellar_idx   = 0
        self._mead_cond_prog    = 0.0
        self._mead_rack_bonus   = 0.0
        self._mead_racked       = False
        self._mead_result_item  = None

    @staticmethod
    def _mead_vat_bid():
        from blocks import MEAD_VAT_BLOCK
        return MEAD_VAT_BLOCK

    @staticmethod
    def _mead_cellar_bid():
        from blocks import MEAD_CELLAR_BLOCK
        return MEAD_CELLAR_BLOCK

    # ── Top-level draw ────────────────────────────────────────────────────────

    def _draw_mead_vat(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("MEAD VAT", True, (225, 175, 60))
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, (140, 120, 60))
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        phase = self._mead_vat_phase
        if phase == "select_honey":
            self._draw_mead_select_honey(player)
        elif phase == "select_additive":
            self._draw_mead_select_additive(player)
        elif phase == "select_yeast":
            self._draw_mead_select_yeast(player)
        elif phase == "stirring":
            self._draw_mead_stir(player, dt)
        elif phase == "result":
            self._draw_mead_vat_result(player)

    def _draw_mead_cellar(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("MEAD CELLAR", True, (200, 155, 55))
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, (130, 110, 55))
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        phase = self._mead_cellar_phase
        if phase == "select":
            self._draw_mead_cellar_select(player)
        elif phase == "conditioning":
            self._draw_mead_conditioning(player, dt)
        elif phase == "result":
            self._draw_mead_cellar_result(player)

    # ── Vat phases ────────────────────────────────────────────────────────────

    def _draw_mead_select_honey(self, player):
        cx = SCREEN_W // 2
        lbl = self.font.render("SELECT HONEY QUALITY", True, (220, 195, 100))
        self.screen.blit(lbl, (cx - lbl.get_width() // 2, 48))
        sub = self.small.render("Higher quality honey produces richer mead.", True, (160, 140, 90))
        self.screen.blit(sub, (cx - sub.get_width() // 2, 74))

        honey_options = [
            ("base",    "honey_jar",         "Honey Jar",          (235, 165, 30)),
            ("fine",    "honey_jar_fine",     "Honey Jar (Fine)",   (245, 180, 40)),
            ("artisan", "honey_jar_artisan",  "Honey Jar (Artisan)",(255, 200, 55)),
        ]
        self._mead_honey_btns = {}
        bw, bh, gap = 220, 60, 18
        total_w = len(honey_options) * bw + (len(honey_options) - 1) * gap
        x0 = cx - total_w // 2
        y0 = 120
        for tier, item_id, label, col in honey_options:
            count = player.inventory.get(item_id, 0)
            has   = count > 0
            rect  = pygame.Rect(x0, y0, bw, bh)
            bg    = (50, 38, 12) if has else (28, 22, 8)
            pygame.draw.rect(self.screen, bg, rect, border_radius=6)
            border = col if has else (80, 65, 30)
            pygame.draw.rect(self.screen, border, rect, 2, border_radius=6)
            name_s = self.small.render(label, True, col if has else (100, 85, 45))
            self.screen.blit(name_s, (rect.centerx - name_s.get_width() // 2, rect.y + 8))
            cnt_s = self.small.render(f"x{count} in inventory", True,
                                      (180, 155, 70) if has else (80, 70, 35))
            self.screen.blit(cnt_s, (rect.centerx - cnt_s.get_width() // 2, rect.y + 30))
            if has:
                self._mead_honey_btns[tier] = (rect, item_id)
            x0 += bw + gap

        note = self.small.render("Click a honey tier to continue →", True, (130, 115, 60))
        self.screen.blit(note, (cx - note.get_width() // 2, y0 + bh + 20))

    def _draw_mead_select_additive(self, player):
        cx = SCREEN_W // 2
        lbl = self.font.render("SELECT ADDITIVE", True, (220, 195, 100))
        self.screen.blit(lbl, (cx - lbl.get_width() // 2, 48))
        sub = self.small.render("Optional — each additive creates a distinct mead style.", True, (160, 140, 90))
        self.screen.blit(sub, (cx - sub.get_width() // 2, 74))

        additive_order = ["none", "pepper", "saffron", "red_wine", "wheat_beer"]
        self._mead_add_btns = {}
        bw, bh, gap = 185, 72, 12
        total_w = len(additive_order) * bw + (len(additive_order) - 1) * gap
        x0 = cx - total_w // 2
        y0 = 110
        for key in additive_order:
            add   = MEAD_ADDITIVES[key]
            item  = add["item"]
            has   = (item is None) or (player.inventory.get(item, 0) > 0)
            rect  = pygame.Rect(x0, y0, bw, bh)
            sel   = (key == self._mead_add_sel)
            bg    = (52, 40, 14) if sel else ((42, 32, 10) if has else (22, 18, 6))
            pygame.draw.rect(self.screen, bg, rect, border_radius=6)
            border = (230, 185, 60) if sel else ((150, 120, 50) if has else (60, 50, 25))
            pygame.draw.rect(self.screen, border, rect, 2, border_radius=6)
            name_s = self.small.render(MEAD_STYLE_NAMES[key], True,
                                       (240, 210, 100) if sel else ((200, 170, 75) if has else (90, 75, 35)))
            self.screen.blit(name_s, (rect.centerx - name_s.get_width() // 2, rect.y + 6))
            desc_s = self.small.render(add["label"], True, (150, 130, 65) if has else (65, 55, 25))
            self.screen.blit(desc_s, (rect.centerx - desc_s.get_width() // 2, rect.y + 26))
            if item:
                cnt = player.inventory.get(item, 0)
                req_s = self.small.render(f"Needs: {item} ({cnt})", True,
                                          (160, 140, 60) if has else (100, 80, 30))
                self.screen.blit(req_s, (rect.centerx - req_s.get_width() // 2, rect.y + 48))
            if has:
                self._mead_add_btns[key] = rect
            x0 += bw + gap

        y_btns = y0 + bh + 24
        self._mead_add_confirm_btn = pygame.Rect(cx - 100, y_btns, 200, 36)
        pygame.draw.rect(self.screen, (55, 44, 14), self._mead_add_confirm_btn, border_radius=5)
        pygame.draw.rect(self.screen, (210, 170, 55), self._mead_add_confirm_btn, 2, border_radius=5)
        lbl2 = self.small.render("CONFIRM →", True, (230, 195, 80))
        self.screen.blit(lbl2, (self._mead_add_confirm_btn.centerx - lbl2.get_width() // 2,
                                  self._mead_add_confirm_btn.centery - lbl2.get_height() // 2))

    def _draw_mead_select_yeast(self, player):
        cx = SCREEN_W // 2
        lbl = self.font.render("SELECT YEAST", True, (220, 195, 100))
        self.screen.blit(lbl, (cx - lbl.get_width() // 2, 48))

        yeast_order = ["wild", "wine", "champagne", "bread"]
        self._mead_yeast_btns = {}
        bw, bh, gap = 210, 80, 14
        total_w = len(yeast_order) * bw + (len(yeast_order) - 1) * gap
        x0 = cx - total_w // 2
        y0 = 110
        for key in yeast_order:
            y = YEAST_TYPES[key]
            rect  = pygame.Rect(x0, y0, bw, bh)
            sel   = (key == self._mead_yeast_sel)
            bg    = (50, 40, 12) if sel else (30, 24, 8)
            pygame.draw.rect(self.screen, bg, rect, border_radius=6)
            border = (225, 180, 55) if sel else (120, 100, 40)
            pygame.draw.rect(self.screen, border, rect, 2, border_radius=6)
            name_s = self.small.render(y["label"], True, (240, 210, 90) if sel else (190, 160, 65))
            self.screen.blit(name_s, (rect.centerx - name_s.get_width() // 2, rect.y + 8))
            desc_s = self.small.render(y["desc"], True, (155, 130, 55))
            self.screen.blit(desc_s, (rect.centerx - desc_s.get_width() // 2, rect.y + 30))
            var_s = self.small.render(f"Quality variance: {y['quality_variance']:.0%}", True, (130, 110, 45))
            self.screen.blit(var_s, (rect.centerx - var_s.get_width() // 2, rect.y + 52))
            self._mead_yeast_btns[key] = rect
            x0 += bw + gap

        y_btn = y0 + bh + 24
        self._mead_yeast_start_btn = pygame.Rect(cx - 110, y_btn, 220, 40)
        pygame.draw.rect(self.screen, (55, 44, 14), self._mead_yeast_start_btn, border_radius=5)
        pygame.draw.rect(self.screen, (215, 175, 55), self._mead_yeast_start_btn, 2, border_radius=5)
        go_s = self.small.render("START STIRRING →", True, (235, 200, 80))
        self.screen.blit(go_s, (self._mead_yeast_start_btn.centerx - go_s.get_width() // 2,
                                  self._mead_yeast_start_btn.centery - go_s.get_height() // 2))

    def _draw_mead_stir(self, player, dt):
        cx = SCREEN_W // 2
        phase_names = ["OXYGENATE", "BLEND"]
        ph = self._mead_stir_phase
        elapsed = self._mead_stir_elapsed

        phase_lbl = self.font.render(phase_names[ph], True, (230, 200, 80))
        self.screen.blit(phase_lbl, (cx - phase_lbl.get_width() // 2, 44))

        time_left = _STIR_PHASE_TIMES[ph] - (elapsed - sum(_STIR_PHASE_TIMES[:ph]))
        tl_s = self.small.render(f"{max(0.0, time_left):.1f}s remaining", True, (160, 140, 65))
        self.screen.blit(tl_s, (cx - tl_s.get_width() // 2, 76))

        # Speed gauge
        GAU_W, GAU_H = 500, 32
        gx = cx - GAU_W // 2
        gy = 120
        pygame.draw.rect(self.screen, (30, 24, 8), (gx, gy, GAU_W, GAU_H))
        lo, hi = _STIR_ZONES[ph]
        green_x = gx + int(lo * GAU_W)
        green_w = int((hi - lo) * GAU_W)
        pygame.draw.rect(self.screen, (30, 90, 30), (green_x, gy, green_w, GAU_H))
        over_x = gx + int(_STIR_OVER_ZONE * GAU_W)
        pygame.draw.rect(self.screen, (80, 25, 25), (over_x, gy, GAU_W - (over_x - gx), GAU_H))
        pygame.draw.rect(self.screen, (140, 115, 50), (gx, gy, GAU_W, GAU_H), 2)

        needle_x = gx + int(self._mead_stir_speed * GAU_W)
        pygame.draw.line(self.screen, (255, 230, 80), (needle_x, gy - 4), (needle_x, gy + GAU_H + 4), 3)

        zone_lbl = self.small.render("OPTIMAL ZONE", True, (80, 200, 80))
        self.screen.blit(zone_lbl, (green_x + green_w // 2 - zone_lbl.get_width() // 2, gy + GAU_H + 6))
        over_lbl = self.small.render("OVER-SPIN", True, (200, 80, 80))
        self.screen.blit(over_lbl, (over_x + (GAU_W - (over_x - gx)) // 2 - over_lbl.get_width() // 2, gy + GAU_H + 6))

        # Quality bar
        quality = self._mead_stir_good / _STIR_TOTAL if _STIR_TOTAL > 0 else 0.0
        qb_w, qb_h = 340, 16
        qbx = cx - qb_w // 2
        qby = gy + GAU_H + 36
        pygame.draw.rect(self.screen, (28, 22, 6), (qbx, qby, qb_w, qb_h))
        pygame.draw.rect(self.screen, (140, 115, 45), (qbx, qby, qb_w, qb_h), 2)
        q_fill_col = (200, 185, 50) if quality < 0.55 else ((140, 195, 80) if quality < 0.80 else (80, 220, 100))
        pygame.draw.rect(self.screen, q_fill_col, (qbx, qby, int(qb_w * quality), qb_h))
        q_lbl = self.small.render(f"Quality {quality:.0%}", True, (200, 180, 70))
        self.screen.blit(q_lbl, (cx - q_lbl.get_width() // 2, qby + qb_h + 6))

        inst = ["Hold SPACE to stir faster", "Keep the needle in the green zone",
                "Phase 2: ease off for a gentle blend"]
        for i, line in enumerate(inst):
            s = self.small.render(line, True, (130, 115, 55))
            self.screen.blit(s, (cx - s.get_width() // 2, qby + qb_h + 28 + i * 18))

        # Overall timer bar
        total_prog = elapsed / _STIR_TOTAL
        tb_w, tb_h = 500, 8
        tbx = cx - tb_w // 2
        tby = gy - 20
        pygame.draw.rect(self.screen, (22, 18, 6), (tbx, tby, tb_w, tb_h))
        pygame.draw.rect(self.screen, (110, 90, 35), (tbx, tby, int(tb_w * min(1.0, total_prog)), tb_h))

    def _draw_mead_vat_result(self, player):
        cx = SCREEN_W // 2
        batch = self._mead_batch_wip
        if batch is None:
            return
        lbl = self.font.render("MUST PREPARED", True, (225, 195, 75))
        self.screen.blit(lbl, (cx - lbl.get_width() // 2, 44))

        style = MEAD_STYLE_NAMES.get(batch.additive, "Mead")
        bio   = BIOME_DISPLAY_NAMES.get(batch.origin_biome, batch.origin_biome)
        tier  = batch.honey_tier.title()
        lines = [
            f"Style: {style}",
            f"Biome: {bio}  •  Honey: {tier}",
            f"Yeast: {YEAST_TYPES[batch.yeast_type]['label']}",
            f"Ferment quality: {batch.ferment_quality:.0%}",
            "",
            "The must is now fermenting.",
            "Take it to the Mead Cellar to condition and bottle.",
        ]
        y = 90
        for line in lines:
            s = self.small.render(line, True, (185, 160, 70))
            self.screen.blit(s, (cx - s.get_width() // 2, y))
            y += 22

        self._mead_vat_done_btn = pygame.Rect(cx - 90, y + 12, 180, 36)
        pygame.draw.rect(self.screen, (50, 40, 12), self._mead_vat_done_btn, border_radius=5)
        pygame.draw.rect(self.screen, (210, 170, 55), self._mead_vat_done_btn, 2, border_radius=5)
        d_s = self.small.render("DONE", True, (230, 195, 75))
        self.screen.blit(d_s, (self._mead_vat_done_btn.centerx - d_s.get_width() // 2,
                                  self._mead_vat_done_btn.centery - d_s.get_height() // 2))

    # ── Cellar phases ─────────────────────────────────────────────────────────

    def _draw_mead_cellar_select(self, player):
        cx = SCREEN_W // 2
        fermenting = [b for b in player.mead_batches if b.state == "fermenting"]
        lbl = self.font.render("SELECT BATCH TO CONDITION", True, (200, 160, 55))
        self.screen.blit(lbl, (cx - lbl.get_width() // 2, 44))

        if not fermenting:
            msg = self.small.render("No fermenting batches.  Use the Mead Vat first.", True, (150, 130, 60))
            self.screen.blit(msg, (cx - msg.get_width() // 2, SCREEN_H // 2))
            return

        self._mead_cellar_batch_btns = {}
        bw, bh, gap = 280, 60, 10
        total_h = len(fermenting) * bh + (len(fermenting) - 1) * gap
        y0 = max(80, SCREEN_H // 2 - total_h // 2)
        for i, batch in enumerate(fermenting):
            rect = pygame.Rect(cx - bw // 2, y0 + i * (bh + gap), bw, bh)
            sel  = (i == self._mead_cellar_idx)
            pygame.draw.rect(self.screen, (48, 36, 10) if sel else (28, 22, 7), rect, border_radius=5)
            pygame.draw.rect(self.screen, (210, 165, 50) if sel else (110, 90, 35), rect, 2, border_radius=5)
            style = MEAD_STYLE_NAMES.get(batch.additive, "Mead")
            bio   = BIOME_DISPLAY_NAMES.get(batch.origin_biome, batch.origin_biome)
            n_s = self.small.render(f"{style}  —  {bio}", True, (230, 195, 80) if sel else (175, 150, 60))
            self.screen.blit(n_s, (rect.x + 10, rect.y + 8))
            q_s = self.small.render(f"Ferment quality: {batch.ferment_quality:.0%}  •  Honey: {batch.honey_tier.title()}",
                                    True, (155, 135, 55))
            self.screen.blit(q_s, (rect.x + 10, rect.y + 32))
            self._mead_cellar_batch_btns[i] = rect

        start_btn_rect = pygame.Rect(cx - 100, y0 + len(fermenting) * (bh + gap) + 16, 200, 36)
        self._mead_cellar_start_btn = start_btn_rect
        pygame.draw.rect(self.screen, (50, 40, 12), start_btn_rect, border_radius=5)
        pygame.draw.rect(self.screen, (210, 168, 52), start_btn_rect, 2, border_radius=5)
        go = self.small.render("CONDITION →", True, (230, 195, 75))
        self.screen.blit(go, (start_btn_rect.centerx - go.get_width() // 2,
                               start_btn_rect.centery - go.get_height() // 2))

    def _draw_mead_conditioning(self, player, dt):
        self._mead_cond_prog = min(1.0, self._mead_cond_prog + dt / _COND_DURATION)

        cx = SCREEN_W // 2
        fermenting = [b for b in player.mead_batches if b.state == "fermenting"]
        if not fermenting or self._mead_cellar_idx >= len(fermenting):
            self._mead_cellar_phase = "select"
            return
        batch = fermenting[self._mead_cellar_idx]

        lbl = self.font.render("CONDITIONING", True, (200, 160, 55))
        self.screen.blit(lbl, (cx - lbl.get_width() // 2, 44))

        style = MEAD_STYLE_NAMES.get(batch.additive, "Mead")
        bio   = BIOME_DISPLAY_NAMES.get(batch.origin_biome, batch.origin_biome)
        info = self.small.render(f"{style}  •  {bio}  •  Honey: {batch.honey_tier.title()}", True, (175, 150, 65))
        self.screen.blit(info, (cx - info.get_width() // 2, 76))

        # Progress bar
        BAR_W, BAR_H = 420, 28
        bx0, by0 = cx - BAR_W // 2, 110
        pygame.draw.rect(self.screen, (28, 22, 7), (bx0, by0, BAR_W, BAR_H))
        pygame.draw.rect(self.screen, (120, 95, 38), (bx0, by0, BAR_W, BAR_H), 2)
        fill_col = (215, 170, 55) if self._mead_cond_prog < 1.0 else (80, 210, 90)
        pygame.draw.rect(self.screen, fill_col, (bx0, by0, int(BAR_W * self._mead_cond_prog), BAR_H))
        pct_s = self.small.render(f"Conditioning {self._mead_cond_prog:.0%}" if self._mead_cond_prog < 1.0 else "Ready to bottle!", True, (210, 185, 75))
        self.screen.blit(pct_s, (cx - pct_s.get_width() // 2, by0 + BAR_H + 6))

        self._mead_rack_btn = None
        self._mead_bottle_btn = None
        y_act = by0 + BAR_H + 40

        # Rack button
        in_window = _RACK_WINDOW[0] <= self._mead_cond_prog <= _RACK_WINDOW[1]
        if in_window and not self._mead_racked:
            self._mead_rack_btn = pygame.Rect(cx - 90, y_act, 180, 34)
            pygame.draw.rect(self.screen, (38, 52, 20), self._mead_rack_btn, border_radius=5)
            pygame.draw.rect(self.screen, (130, 190, 70), self._mead_rack_btn, 2, border_radius=5)
            rack_s = self.small.render("RACK  (+clarity)", True, (150, 215, 85))
            self.screen.blit(rack_s, (self._mead_rack_btn.centerx - rack_s.get_width() // 2,
                                       self._mead_rack_btn.centery - rack_s.get_height() // 2))
            y_act += 50
        elif self._mead_racked:
            racked_s = self.small.render("✓ Racked", True, (100, 190, 70))
            self.screen.blit(racked_s, (cx - racked_s.get_width() // 2, y_act))
            y_act += 26

        # Bottle button
        if self._mead_cond_prog >= 1.0:
            self._mead_bottle_btn = pygame.Rect(cx - 90, y_act, 180, 36)
            pygame.draw.rect(self.screen, (50, 40, 12), self._mead_bottle_btn, border_radius=5)
            pygame.draw.rect(self.screen, (215, 172, 55), self._mead_bottle_btn, 2, border_radius=5)
            bot_s = self.small.render("BOTTLE →", True, (235, 200, 80))
            self.screen.blit(bot_s, (self._mead_bottle_btn.centerx - bot_s.get_width() // 2,
                                      self._mead_bottle_btn.centery - bot_s.get_height() // 2))

        # Instructions
        inst_lines = [
            "Wait for conditioning to complete.",
            "Rack between 40–65% for improved clarity.",
        ]
        for i, line in enumerate(inst_lines):
            s = self.small.render(line, True, (120, 105, 48))
            self.screen.blit(s, (cx - s.get_width() // 2, y_act + 60 + i * 20))

    def _draw_mead_cellar_result(self, player):
        cx = SCREEN_W // 2
        item_id = self._mead_result_item
        lbl = self.font.render("MEAD BOTTLED", True, (225, 190, 70))
        self.screen.blit(lbl, (cx - lbl.get_width() // 2, 44))

        tier_map = {"mead": "base", "mead_fine": "fine", "mead_reserve": "reserve"}
        tier = tier_map.get(item_id, "base")
        col  = _TIER_COLORS.get(tier, (210, 155, 45))

        lines = [
            f"Produced: {_TIER_LABEL.get(tier, 'Base')} Mead",
            f"Item: {item_id.replace('_', ' ').title()}",
        ]
        if item_id in MEAD_BUFFS:
            lines.append("")
            lines.append("Buffs when consumed:")
            for buff_key in MEAD_BUFFS[item_id]:
                lines.append(f"  • {BUFF_DESCS.get(buff_key, buff_key)}")
        y = 90
        for line in lines:
            s = self.small.render(line, True, col if line else (100, 85, 40))
            self.screen.blit(s, (cx - s.get_width() // 2, y))
            y += 22

        self._mead_cellar_done_btn = pygame.Rect(cx - 80, y + 16, 160, 36)
        pygame.draw.rect(self.screen, (50, 40, 12), self._mead_cellar_done_btn, border_radius=5)
        pygame.draw.rect(self.screen, (210, 170, 52), self._mead_cellar_done_btn, 2, border_radius=5)
        d_s = self.small.render("DONE", True, (230, 195, 75))
        self.screen.blit(d_s, (self._mead_cellar_done_btn.centerx - d_s.get_width() // 2,
                                  self._mead_cellar_done_btn.centery - d_s.get_height() // 2))

    # ── Stir physics ──────────────────────────────────────────────────────────

    def _update_mead_stir(self, dt, player=None):
        if self._mead_vat_phase != "stirring":
            return

        self._mead_stir_elapsed += dt
        ph = self._mead_stir_phase

        # Advance phase
        if ph == 0 and self._mead_stir_elapsed >= _STIR_PHASE_TIMES[0]:
            self._mead_stir_phase = 1
            ph = 1

        # Speed physics
        if self._mead_stir_held:
            self._mead_stir_speed = min(1.0, self._mead_stir_speed + _SPEED_RISE * dt)
        else:
            fall = _SPEED_FALL[ph]
            self._mead_stir_speed = max(0.0, self._mead_stir_speed - fall * dt)

        # Score good time
        lo, hi = _STIR_ZONES[ph]
        if lo <= self._mead_stir_speed <= hi:
            self._mead_stir_good += dt

        # End of game
        if self._mead_stir_elapsed >= _STIR_TOTAL:
            stir_q = self._mead_stir_good / _STIR_TOTAL
            if self._mead_batch_wip is not None:
                apply_stir_result(self._mead_batch_wip, stir_q)
                if player is not None:
                    player.mead_batches.append(self._mead_batch_wip)
            self._mead_vat_phase = "result"

    # ── Click handlers ────────────────────────────────────────────────────────

    def _handle_mead_vat_click(self, pos, player):
        phase = self._mead_vat_phase

        if phase == "select_honey":
            for tier, (rect, item_id) in getattr(self, "_mead_honey_btns", {}).items():
                if rect.collidepoint(pos):
                    self._mead_honey_sel = tier
                    self._mead_vat_phase = "select_additive"
                    return

        elif phase == "select_additive":
            for key, rect in getattr(self, "_mead_add_btns", {}).items():
                if rect.collidepoint(pos):
                    self._mead_add_sel = key
            if hasattr(self, "_mead_add_confirm_btn") and self._mead_add_confirm_btn.collidepoint(pos):
                self._mead_vat_phase = "select_yeast"

        elif phase == "select_yeast":
            for key, rect in getattr(self, "_mead_yeast_btns", {}).items():
                if rect.collidepoint(pos):
                    self._mead_yeast_sel = key
            if hasattr(self, "_mead_yeast_start_btn") and self._mead_yeast_start_btn.collidepoint(pos):
                self._start_mead_stir(player)

        elif phase == "result":
            if hasattr(self, "_mead_vat_done_btn") and self._mead_vat_done_btn.collidepoint(pos):
                self.refinery_open = False

    def _start_mead_stir(self, player):
        tier     = self._mead_honey_sel or "base"
        additive = self._mead_add_sel
        yeast    = self._mead_yeast_sel

        # Consume inputs from inventory
        honey_item_map = {"base": "honey_jar", "fine": "honey_jar_fine", "artisan": "honey_jar_artisan"}
        honey_item = honey_item_map[tier]
        if player.inventory.get(honey_item, 0) < 1:
            return
        player.inventory[honey_item] = player.inventory.get(honey_item, 0) - 1
        if player.inventory[honey_item] == 0:
            del player.inventory[honey_item]

        add_item = MEAD_ADDITIVES[additive]["item"]
        if add_item and player.inventory.get(add_item, 0) < 1:
            return
        if add_item:
            player.inventory[add_item] = player.inventory.get(add_item, 0) - 1
            if player.inventory[add_item] == 0:
                del player.inventory[add_item]

        biodome = player.world.get_biodome(0)
        self._mead_batch_wip = player._mead_gen.generate(biodome, tier, additive, yeast)
        self._mead_stir_elapsed = 0.0
        self._mead_stir_good    = 0.0
        self._mead_stir_phase   = 0
        self._mead_stir_speed   = 0.0
        self._mead_stir_held    = False
        self._mead_vat_phase    = "stirring"

    def _handle_mead_cellar_click(self, pos, player):
        phase = self._mead_cellar_phase

        if phase == "select":
            for i, rect in getattr(self, "_mead_cellar_batch_btns", {}).items():
                if rect.collidepoint(pos):
                    self._mead_cellar_idx = i
            if hasattr(self, "_mead_cellar_start_btn") and self._mead_cellar_start_btn.collidepoint(pos):
                fermenting = [b for b in player.mead_batches if b.state == "fermenting"]
                if fermenting:
                    self._mead_cond_prog  = 0.0
                    self._mead_rack_bonus = 0.0
                    self._mead_racked     = False
                    self._mead_cellar_phase = "conditioning"

        elif phase == "conditioning":
            if self._mead_rack_btn and self._mead_rack_btn.collidepoint(pos) and not self._mead_racked:
                self._mead_rack_bonus = _RACK_BONUS
                self._mead_racked     = True
            if self._mead_bottle_btn and self._mead_bottle_btn.collidepoint(pos) and self._mead_cond_prog >= 1.0:
                self._finish_mead_bottling(player)

        elif phase == "result":
            if hasattr(self, "_mead_cellar_done_btn") and self._mead_cellar_done_btn.collidepoint(pos):
                self.refinery_open = False

    def _finish_mead_bottling(self, player):
        fermenting = [b for b in player.mead_batches if b.state == "fermenting"]
        if not fermenting or self._mead_cellar_idx >= len(fermenting):
            return
        batch = fermenting[self._mead_cellar_idx]
        apply_condition_result(batch, self._mead_rack_bonus)
        item_id = get_bottle_output_id(batch)
        player._add_item(item_id)
        player.discovered_meads.add(
            f"{batch.origin_biome}_{'reserve' if batch.ferment_quality >= 0.80 else 'fine' if batch.ferment_quality >= 0.55 else 'base'}"
        )
        self._mead_result_item = item_id
        self._mead_cellar_phase = "result"

    # ── Key handlers ──────────────────────────────────────────────────────────

    def handle_mead_vat_keydown(self, key, player):
        pass  # SPACE handled via held-key polling

    def handle_mead_vat_keys(self, keys, dt, player):
        if self._mead_vat_phase != "stirring":
            return
        import pygame as _pg
        self._mead_stir_held = keys[_pg.K_SPACE]
        self._update_mead_stir(dt, player)

    # ── Codex ─────────────────────────────────────────────────────────────────

    def _draw_mead_codex(self, player, gy0=58, gx_off=0):
        import pygame
        cx = SCREEN_W // 2

        TIERS  = ["base", "fine", "reserve"]
        TIER_LABELS = ["Base", "Fine", "Reserve"]
        CELL_W, CELL_H, GAP = 100, 52, 6
        ROW_H  = CELL_H + GAP
        BIOMES = _CODEX_BIOMES
        COLS   = len(TIERS)
        grid_w = COLS * CELL_W + (COLS - 1) * GAP
        grid_x = cx - grid_w // 2 - 60
        grid_y = gy0 + 30

        # Column headers
        for ci, tl in enumerate(TIER_LABELS):
            hx = grid_x + ci * (CELL_W + GAP) + CELL_W // 2
            hs = self.small.render(tl, True, _TIER_COLORS.get(TIERS[ci], (200, 170, 55)))
            self.screen.blit(hs, (hx - hs.get_width() // 2, gy0 + 8))

        self._mead_codex_rects = {}
        for ri, biome in enumerate(BIOMES):
            bio_name = BIOME_DISPLAY_NAMES.get(biome, biome)
            by = grid_y + ri * ROW_H
            row_lbl = self.small.render(bio_name, True, (165, 145, 65))
            self.screen.blit(row_lbl, (grid_x - row_lbl.get_width() - 8, by + CELL_H // 2 - row_lbl.get_height() // 2))

            for ci, tier in enumerate(TIERS):
                cell_x = grid_x + ci * (CELL_W + GAP)
                key    = f"{biome}_{tier}"
                found  = key in player.discovered_meads
                rect   = pygame.Rect(cell_x, by, CELL_W, CELL_H)

                bg_col = (42, 32, 8) if found else (20, 16, 5)
                pygame.draw.rect(self.screen, bg_col, rect, border_radius=4)
                brd_col = _TIER_COLORS.get(tier, (180, 140, 50)) if found else (55, 45, 20)
                pygame.draw.rect(self.screen, brd_col, rect, 1, border_radius=4)

                if found:
                    tier_s = self.small.render(tier.title(), True, _TIER_COLORS.get(tier, (210, 170, 60)))
                    self.screen.blit(tier_s, (rect.centerx - tier_s.get_width() // 2, rect.y + 6))
                    bio_s = self.small.render(bio_name[:12], True, (150, 130, 55))
                    self.screen.blit(bio_s, (rect.centerx - bio_s.get_width() // 2, rect.y + 26))
                else:
                    q_s = self.small.render("?", True, (65, 55, 25))
                    self.screen.blit(q_s, (rect.centerx - q_s.get_width() // 2, rect.centery - q_s.get_height() // 2))

                if rect.collidepoint(pygame.mouse.get_pos()):
                    self._mead_codex_selected = (biome, tier)
                self._mead_codex_rects[(biome, tier)] = rect

        # Detail panel
        sel = getattr(self, "_mead_codex_selected", None)
        px = grid_x + grid_w + 30
        py = gy0 + 8
        pw, ph_h = 260, 320
        pygame.draw.rect(self.screen, (22, 18, 6), (px, py, pw, ph_h), border_radius=6)
        pygame.draw.rect(self.screen, (100, 80, 30), (px, py, pw, ph_h), 1, border_radius=6)
        if sel:
            biome, tier = sel
            key = f"{biome}_{tier}"
            found = key in player.discovered_meads
            bio_name = BIOME_DISPLAY_NAMES.get(biome, biome)
            title_s = self.small.render(f"{bio_name} Mead ({tier.title()})", True,
                                         _TIER_COLORS.get(tier, (210, 170, 55)))
            self.screen.blit(title_s, (px + pw // 2 - title_s.get_width() // 2, py + 10))
            if found:
                buffs = MEAD_BUFFS.get(f"mead{'_' + tier if tier != 'base' else ''}", {})
                ty = py + 38
                for bk, bv in buffs.items():
                    bs = self.small.render(f"• {BUFF_DESCS.get(bk, bk)}", True, (155, 210, 100))
                    self.screen.blit(bs, (px + 12, ty))
                    ty += 18
                    dur_s = self.small.render(f"  Duration: {bv['duration']:.0f}s", True, (115, 150, 75))
                    self.screen.blit(dur_s, (px + 12, ty))
                    ty += 20
            else:
                undis = self.small.render("Not yet discovered.", True, (90, 78, 35))
                self.screen.blit(undis, (px + pw // 2 - undis.get_width() // 2, py + 50))
        else:
            hint_s = self.small.render("Hover a cell to inspect.", True, (90, 78, 35))
            self.screen.blit(hint_s, (px + pw // 2 - hint_s.get_width() // 2, py + ph_h // 2))
