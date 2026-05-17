"""Falconry UI mixin.

Adds the Falconer's Perch panel (list of tamed raptors, detail card with
training/hunt buttons) and the capture mini-game shown when the player
right-clicks a wild raptor while wielding a Falconer's Gauntlet.

Panel layout (740 × 540):
    Left column   – list of tamed raptors (160 wide)
    Right column  – selected raptor portrait + stat bars + action buttons
                    and an inline training/hunt mini-game when active.
"""

import random
import pygame
from constants import SCREEN_W, SCREEN_H
from falconry import (
    RAPTOR_SPECIES, TRAINING_DRILLS, QUARRY, QUARRY_ORDER,
    apply_training, hunt_outcome, apply_hunt, feed_raptor,
    raptor_quality_stars, species_rating, capture_success_chance,
)


_BAR_COLORS = {
    "speed":        (200, 110,  60),
    "strength":     (180,  90,  90),
    "intelligence": (140, 165, 220),
    "endurance":    (130, 175,  85),
    "boldness":     (220, 175,  90),
    "vision":       (190, 145, 220),
}


class FalconryMixin:
    # ──────────────────────────────────────────────────────────────────────────
    # Public entry: open the perch panel
    # ──────────────────────────────────────────────────────────────────────────
    def open_falconer_perch(self, pos, player):
        self.falconry_open = True
        self.active_perch_pos = pos
        self._fy_selected_uid = None
        self._fy_state = "idle"          # "idle" | "training" | "hunting" | "capture"
        self._fy_drill = None
        self._fy_quarry = None
        self._fy_timer = 0.0
        self._fy_marker = 0.0
        self._fy_marker_dir = 1
        self._fy_result_msg = ""
        self._fy_result_color = (210, 200, 160)
        self._fy_btn_rects = {}
        self._fy_list_rects = {}

    def open_falconry_capture(self, species_key, biome, source_bird=None):
        """Triggered from main.py when player right-clicks a wild raptor while
        wielding the falconer_gauntlet."""
        self.falconry_capture_open = True
        self._fy_capture_species = species_key
        self._fy_capture_biome = biome or ""
        self._fy_capture_source = source_bird
        self._fy_state = "capture"
        self._fy_marker = 0.0
        self._fy_marker_dir = 1
        self._fy_result_msg = ""
        self._fy_btn_rects = {}

    # ──────────────────────────────────────────────────────────────────────────
    # Per-frame update (called by main.py while panel is open)
    # ──────────────────────────────────────────────────────────────────────────
    def update_falconry(self, dt, player):
        if self._fy_state in ("training", "hunting", "capture"):
            self._fy_timer += dt
            # Marker bounces in a 0..1 range
            self._fy_marker += self._fy_marker_dir * dt * 1.4
            if self._fy_marker >= 1.0:
                self._fy_marker = 1.0
                self._fy_marker_dir = -1
            elif self._fy_marker <= 0.0:
                self._fy_marker = 0.0
                self._fy_marker_dir = 1

    # ──────────────────────────────────────────────────────────────────────────
    # Drawing
    # ──────────────────────────────────────────────────────────────────────────
    def _draw_falconer_perch(self, player):
        pw, ph = 740, 540
        px = SCREEN_W // 2 - pw // 2
        py = SCREEN_H // 2 - ph // 2
        pygame.draw.rect(self.screen, (24, 18, 10), (px, py, pw, ph), border_radius=8)
        pygame.draw.rect(self.screen, (140, 100,  50), (px, py, pw, ph), 2, border_radius=8)

        title = self.large.render("Falconer's Perch", True, (240, 200, 130))
        self.screen.blit(title, (px + 18, py + 12))

        close_r = pygame.Rect(px + pw - 32, py + 10, 22, 22)
        pygame.draw.rect(self.screen, (110, 50, 30), close_r, border_radius=4)
        ct = self.small.render("X", True, (240, 180, 100))
        self.screen.blit(ct, (close_r.centerx - ct.get_width() // 2,
                              close_r.centery - ct.get_height() // 2))
        self._fy_btn_rects["close"] = close_r

        # Left column — raptor list
        list_x = px + 14
        list_y = py + 50
        list_w = 200
        list_h = ph - 70
        pygame.draw.rect(self.screen, (16, 12, 6), (list_x, list_y, list_w, list_h), border_radius=4)
        pygame.draw.rect(self.screen, (90, 70, 40), (list_x, list_y, list_w, list_h), 1, border_radius=4)

        self._fy_list_rects.clear()
        if not player.tamed_raptors:
            t = self.small.render("No tamed raptors yet.", True, (160, 140,  95))
            self.screen.blit(t, (list_x + 12, list_y + 14))
            t2 = self.small.render("Carry a gauntlet and",  True, (130, 115,  80))
            t3 = self.small.render("right-click a wild raptor", True, (130, 115,  80))
            self.screen.blit(t2, (list_x + 12, list_y + 36))
            self.screen.blit(t3, (list_x + 12, list_y + 52))
        else:
            for i, r in enumerate(player.tamed_raptors):
                row_y = list_y + 6 + i * 36
                if row_y + 32 > list_y + list_h:
                    break
                row = pygame.Rect(list_x + 4, row_y, list_w - 8, 32)
                selected = (r.uid == self._fy_selected_uid)
                pygame.draw.rect(self.screen,
                                 (60, 45, 25) if selected else (32, 24, 14),
                                 row, border_radius=3)
                pygame.draw.rect(self.screen,
                                 (180, 140,  70) if selected else (75, 60, 35),
                                 row, 1, border_radius=3)
                sp = RAPTOR_SPECIES.get(r.species, {})
                col = sp.get("color", (200, 180, 140))
                pygame.draw.circle(self.screen, col,
                                   (row.x + 14, row.centery), 8)
                nm = self.small.render(r.name[:14], True, (230, 200, 140))
                sn = self.small.render(sp.get("name", r.species)[:18], True, (160, 140,  95))
                self.screen.blit(nm, (row.x + 30, row.y + 2))
                self.screen.blit(sn, (row.x + 30, row.y + 16))
                self._fy_list_rects[r.uid] = row

        # Right column — selected detail
        det_x = list_x + list_w + 14
        det_y = list_y
        det_w = pw - (det_x - px) - 14
        det_h = list_h
        pygame.draw.rect(self.screen, (16, 12, 6), (det_x, det_y, det_w, det_h), border_radius=4)
        pygame.draw.rect(self.screen, (90, 70, 40), (det_x, det_y, det_w, det_h), 1, border_radius=4)

        r = self._selected_raptor(player)
        if r is None:
            self._draw_wild_raptor_list(player, det_x, det_y, det_w, det_h)
            return

        self._draw_raptor_detail(player, r, det_x, det_y, det_w, det_h)

    def _scan_wild_raptors(self, player, radius_blocks=40):
        """Find Bird entities near the player whose class maps to a raptor species."""
        from falconry import BIRD_CLASS_TO_RAPTOR
        from constants import BLOCK_SIZE
        results = []
        try:
            entities = player.world.entities
        except Exception:
            return results
        px, py = player.x, player.y
        r2 = (radius_blocks * BLOCK_SIZE) ** 2
        for e in entities:
            species_key = BIRD_CLASS_TO_RAPTOR.get(type(e).__name__)
            if not species_key:
                continue
            if (getattr(e, "x", 0) - px) ** 2 + (getattr(e, "y", 0) - py) ** 2 > r2:
                continue
            results.append((species_key, e))
        return results

    def _draw_wild_raptor_list(self, player, x, y, w, h):
        wilds = self._scan_wild_raptors(player)
        t = self.font.render("Wild Raptors Nearby", True, (240, 210, 150))
        self.screen.blit(t, (x + 14, y + 12))
        hint = self.small.render(
            "Have a Falconer's Gauntlet equipped, then click to attempt capture.",
            True, (170, 150, 100))
        self.screen.blit(hint, (x + 14, y + 36))

        if not wilds:
            n = self.small.render("(no raptors within 40 blocks)", True, (130, 115,  80))
            self.screen.blit(n, (x + 14, y + 60))
            return

        seen = []
        for i, (species_key, bird) in enumerate(wilds[:8]):
            row_y = y + 64 + i * 32
            row = pygame.Rect(x + 14, row_y, w - 28, 28)
            held = player.hotbar[player.selected_slot]
            ok = held == "falconer_gauntlet"
            pygame.draw.rect(self.screen,
                             (60, 50, 28) if ok else (32, 24, 14),
                             row, border_radius=3)
            pygame.draw.rect(self.screen,
                             (180, 140,  70) if ok else (75, 60, 35),
                             row, 1, border_radius=3)
            sp = RAPTOR_SPECIES[species_key]
            pygame.draw.circle(self.screen, sp["color"], (row.x + 16, row.centery), 8)
            label = self.small.render(
                f"{sp['name']}    (tier {sp['tier']}, ~{int(capture_success_chance(species_key)*100)}%)",
                True, (235, 205, 145) if ok else (140, 120,  85))
            self.screen.blit(label, (row.x + 32, row.centery - 8))
            self._fy_btn_rects[f"wild_{i}"] = row
            seen.append((species_key, bird))
        self._fy_wild_list = seen

    def _selected_raptor(self, player):
        for r in player.tamed_raptors:
            if r.uid == self._fy_selected_uid:
                return r
        return None

    def _draw_raptor_detail(self, player, r, x, y, w, h):
        sp = RAPTOR_SPECIES.get(r.species, {})
        # Header
        nm = self.font.render(r.name, True, (240, 210, 150))
        species_name = sp.get("name", r.species)
        sn = self.small.render(species_name, True, (175, 150, 100))
        self.screen.blit(nm, (x + 14, y + 10))
        self.screen.blit(sn, (x + 14, y + 32))

        stars = raptor_quality_stars(r)
        tier  = species_rating(r.species)
        tier_t = self.small.render(
            f"Tier {tier}    {'★' * stars}{'·' * (5 - stars)}",
            True, (215, 185, 110))
        self.screen.blit(tier_t, (x + w - 160, y + 10))

        # Status row
        status_t = self.small.render(
            f"Hunts: {r.hunts_completed}    State: {r.state}    Cooldown: {r.cooldown:0.1f}s",
            True, (165, 145, 100))
        self.screen.blit(status_t, (x + 14, y + 52))

        # Stat bars
        bar_x = x + 14
        bar_y = y + 80
        bar_w = w - 28
        for i, key in enumerate(("speed", "strength", "intelligence",
                                 "endurance", "boldness", "vision")):
            self._draw_falcon_bar(key, getattr(r, key),
                                  bar_x, bar_y + i * 22, bar_w)

        # Bond / hunger / condition
        meta_y = bar_y + 6 * 22 + 4
        self._draw_falcon_meta_bar("Bond",      r.bond,     bar_x, meta_y,      bar_w, ( 90, 200, 200))
        self._draw_falcon_meta_bar("Condition", r.condition, bar_x, meta_y + 18, bar_w, (120, 200, 110))
        self._draw_falcon_meta_bar("Hunger",    r.hunger,    bar_x, meta_y + 36, bar_w, (210, 130,  90))

        # Action buttons or mini-game
        act_y = meta_y + 64
        if self._fy_state == "idle":
            self._draw_falconry_actions(player, r, x, act_y, w)
        elif self._fy_state == "training":
            self._draw_minigame_panel(x, act_y, w, label=f"Training: {TRAINING_DRILLS[self._fy_drill]['label']}")
        elif self._fy_state == "hunting":
            self._draw_minigame_panel(x, act_y, w, label=f"Hunt: {QUARRY[self._fy_quarry]['label']}")

        # Result line
        if self._fy_result_msg:
            t = self.small.render(self._fy_result_msg, True, self._fy_result_color)
            self.screen.blit(t, (x + 14, y + h - 22))

    def _draw_falcon_bar(self, key, value, x, y, w):
        col = _BAR_COLORS.get(key, (200, 180, 140))
        lbl = self.small.render(key.capitalize()[:12], True, (165, 145, 100))
        self.screen.blit(lbl, (x, y))
        pygame.draw.rect(self.screen, (40, 30, 18), (x + 110, y + 2, w - 160, 10))
        pygame.draw.rect(self.screen, col,             (x + 110, y + 2,
                         int((w - 160) * max(0.0, min(1.0, value))), 10))
        v = self.small.render(f"{value:.2f}", True, (215, 195, 145))
        self.screen.blit(v, (x + w - 42, y))

    def _draw_falcon_meta_bar(self, label, value, x, y, w, col):
        lbl = self.small.render(label, True, (165, 145, 100))
        self.screen.blit(lbl, (x, y))
        pygame.draw.rect(self.screen, (40, 30, 18), (x + 110, y + 2, w - 160, 10))
        pygame.draw.rect(self.screen, col,             (x + 110, y + 2,
                         int((w - 160) * max(0.0, min(1.0, value))), 10))
        v = self.small.render(f"{value:.2f}", True, (215, 195, 145))
        self.screen.blit(v, (x + w - 42, y))

    # ── Buttons (idle state) ─────────────────────────────────────────────────
    def _draw_falconry_actions(self, player, r, x, y, w):
        btn_h = 24
        # Feed button
        feed_r = pygame.Rect(x + 14, y, 120, btn_h)
        food_qty = player.inventory.get("raptor_food", 0)
        pygame.draw.rect(self.screen, (60, 90, 50) if food_qty > 0 else (50, 40, 30),
                         feed_r, border_radius=4)
        pygame.draw.rect(self.screen, (120, 160,  80), feed_r, 1, border_radius=4)
        ft = self.small.render(f"Feed  ({food_qty})", True, (220, 235, 175))
        self.screen.blit(ft, (feed_r.centerx - ft.get_width() // 2,
                              feed_r.centery - ft.get_height() // 2))
        self._fy_btn_rects["feed"] = feed_r

        # Training drill buttons (2 rows of 3)
        labels = self.small.render("Training drills:", True, (175, 150, 100))
        self.screen.blit(labels, (x + 14, y + 32))
        keys = list(TRAINING_DRILLS.keys())
        for i, drill_key in enumerate(keys):
            row, col = divmod(i, 3)
            bx = x + 14 + col * 175
            by = y + 50 + row * 28
            br = pygame.Rect(bx, by, 165, 22)
            drill = TRAINING_DRILLS[drill_key]
            have = player.inventory.get("raptor_food", 0)
            ok = have >= drill["food_cost"] and r.cooldown <= 0
            pygame.draw.rect(self.screen, (60, 70, 90) if ok else (50, 40, 30),
                             br, border_radius=3)
            pygame.draw.rect(self.screen, (130, 150, 200) if ok else (90, 75, 50),
                             br, 1, border_radius=3)
            t = self.small.render(f"{drill['label']}  -{drill['food_cost']}", True,
                                  (210, 220, 240) if ok else (130, 115, 80))
            self.screen.blit(t, (br.centerx - t.get_width() // 2,
                                 br.centery - t.get_height() // 2))
            self._fy_btn_rects[f"drill_{drill_key}"] = br

        # Hunt button row
        hl = self.small.render("Hunt quarry:", True, (175, 150, 100))
        self.screen.blit(hl, (x + 14, y + 110))
        biome = self._current_biome(player)
        quarry_keys = [q for q in QUARRY_ORDER if biome in QUARRY[q]["biomes"]]
        if not quarry_keys:
            quarry_keys = QUARRY_ORDER[:4]
        for i, qkey in enumerate(quarry_keys[:6]):
            row, col = divmod(i, 3)
            bx = x + 14 + col * 175
            by = y + 128 + row * 28
            br = pygame.Rect(bx, by, 165, 22)
            q = QUARRY[qkey]
            ok = (r.strength >= q["strength_req"] * 0.6
                  and r.condition >= 0.20
                  and r.hunger <= 0.85
                  and r.cooldown <= 0)
            pygame.draw.rect(self.screen, (80, 60, 30) if ok else (50, 40, 30),
                             br, border_radius=3)
            pygame.draw.rect(self.screen, (200, 160, 90) if ok else (90, 75, 50),
                             br, 1, border_radius=3)
            t = self.small.render(q['label'], True,
                                  (240, 215, 160) if ok else (130, 115, 80))
            self.screen.blit(t, (br.centerx - t.get_width() // 2,
                                 br.centery - t.get_height() // 2))
            self._fy_btn_rects[f"hunt_{qkey}"] = br

    def _draw_minigame_panel(self, x, y, w, label):
        """Bouncing marker mini-game. Click STOP when marker is in the green zone."""
        lbl = self.small.render(label + "  —  click STOP when the marker is in the bright zone", True, (215, 195, 145))
        self.screen.blit(lbl, (x + 14, y))
        # Track
        track_x = x + 14
        track_y = y + 28
        track_w = w - 28
        pygame.draw.rect(self.screen, (40, 30, 18), (track_x, track_y, track_w, 18))
        # Green zone in the middle 35..65%
        gz_x = track_x + int(track_w * 0.35)
        gz_w = int(track_w * 0.30)
        pygame.draw.rect(self.screen, (60, 130, 60), (gz_x, track_y, gz_w, 18))
        # Marker
        mx = track_x + int(track_w * self._fy_marker) - 3
        pygame.draw.rect(self.screen, (240, 220, 130), (mx, track_y - 4, 6, 26))

        stop_r = pygame.Rect(x + w // 2 - 60, y + 60, 120, 28)
        pygame.draw.rect(self.screen, (160, 90, 40), stop_r, border_radius=4)
        pygame.draw.rect(self.screen, (220, 160, 80), stop_r, 1, border_radius=4)
        st = self.small.render("STOP", True, (250, 230, 180))
        self.screen.blit(st, (stop_r.centerx - st.get_width() // 2,
                              stop_r.centery - st.get_height() // 2))
        self._fy_btn_rects["stop"] = stop_r

    # ──────────────────────────────────────────────────────────────────────────
    # Capture mini-game (separate small overlay)
    # ──────────────────────────────────────────────────────────────────────────
    def _draw_falconry_capture(self, player):
        pw, ph = 420, 240
        px = SCREEN_W // 2 - pw // 2
        py = SCREEN_H // 2 - ph // 2
        pygame.draw.rect(self.screen, (24, 18, 10), (px, py, pw, ph), border_radius=8)
        pygame.draw.rect(self.screen, (140, 100,  50), (px, py, pw, ph), 2, border_radius=8)

        sp = RAPTOR_SPECIES.get(self._fy_capture_species, {})
        title = self.font.render(f"Capture: {sp.get('name', self._fy_capture_species)}", True, (240, 210, 150))
        self.screen.blit(title, (px + 18, py + 12))

        chance = capture_success_chance(self._fy_capture_species)
        info = self.small.render(f"Tier {species_rating(self._fy_capture_species)}    Base chance {chance*100:.0f}%",
                                 True, (175, 150, 100))
        self.screen.blit(info, (px + 18, py + 38))

        # Marker track
        track_x = px + 20
        track_y = py + 80
        track_w = pw - 40
        pygame.draw.rect(self.screen, (40, 30, 18), (track_x, track_y, track_w, 18))
        gz_x = track_x + int(track_w * 0.40)
        gz_w = int(track_w * 0.20)
        pygame.draw.rect(self.screen, (60, 130, 60), (gz_x, track_y, gz_w, 18))
        mx = track_x + int(track_w * self._fy_marker) - 3
        pygame.draw.rect(self.screen, (240, 220, 130), (mx, track_y - 4, 6, 26))

        stop_r = pygame.Rect(px + pw // 2 - 60, py + 130, 120, 28)
        pygame.draw.rect(self.screen, (160, 90, 40), stop_r, border_radius=4)
        st = self.small.render("RELEASE", True, (250, 230, 180))
        self.screen.blit(st, (stop_r.centerx - st.get_width() // 2,
                              stop_r.centery - st.get_height() // 2))
        self._fy_btn_rects["capture_stop"] = stop_r

        cancel_r = pygame.Rect(px + pw - 80, py + ph - 36, 64, 24)
        pygame.draw.rect(self.screen, (80, 50, 30), cancel_r, border_radius=4)
        ct = self.small.render("Cancel", True, (220, 190, 140))
        self.screen.blit(ct, (cancel_r.centerx - ct.get_width() // 2,
                              cancel_r.centery - ct.get_height() // 2))
        self._fy_btn_rects["capture_cancel"] = cancel_r

        if self._fy_result_msg:
            t = self.small.render(self._fy_result_msg, True, self._fy_result_color)
            self.screen.blit(t, (px + 18, py + ph - 36))

    # ──────────────────────────────────────────────────────────────────────────
    # Click handling
    # ──────────────────────────────────────────────────────────────────────────
    def handle_falconer_perch_click(self, pos, player):
        if self._fy_btn_rects.get("close") and self._fy_btn_rects["close"].collidepoint(pos):
            self.falconry_open = False
            return

        # Raptor list
        for uid, rect in self._fy_list_rects.items():
            if rect.collidepoint(pos):
                self._fy_selected_uid = uid
                self._fy_state = "idle"
                self._fy_result_msg = ""
                return

        # Wild raptor capture rows (when no raptor is selected)
        if self._selected_raptor(player) is None:
            for k, br in list(self._fy_btn_rects.items()):
                if not k.startswith("wild_"):
                    continue
                if br.collidepoint(pos):
                    idx = int(k[len("wild_"):])
                    wild_list = getattr(self, "_fy_wild_list", [])
                    if idx >= len(wild_list):
                        return
                    species_key, bird = wild_list[idx]
                    held = player.hotbar[player.selected_slot]
                    if held != "falconer_gauntlet":
                        self._fy_result_msg = "Equip the Falconer's Gauntlet first."
                        self._fy_result_color = (220, 140, 100)
                        return
                    try:
                        from constants import BLOCK_SIZE
                        biome = player.world.get_biodome(int(bird.x // BLOCK_SIZE))
                    except Exception:
                        biome = ""
                    self.open_falconry_capture(species_key, biome, bird)
                    return

        r = self._selected_raptor(player)
        if r is None:
            return

        if self._fy_state == "idle":
            # Feed
            if self._fy_btn_rects.get("feed") and self._fy_btn_rects["feed"].collidepoint(pos):
                if player.inventory.get("raptor_food", 0) > 0:
                    player.inventory["raptor_food"] -= 1
                    if player.inventory["raptor_food"] <= 0:
                        del player.inventory["raptor_food"]
                    feed_raptor(r, 1)
                    self._fy_result_msg = f"{r.name} fed."
                    self._fy_result_color = (180, 220, 150)
                return
            # Drill buttons
            for k, br in list(self._fy_btn_rects.items()):
                if not k.startswith("drill_"):
                    continue
                if br.collidepoint(pos):
                    drill_key = k[len("drill_"):]
                    drill = TRAINING_DRILLS[drill_key]
                    if player.inventory.get("raptor_food", 0) < drill["food_cost"]:
                        self._fy_result_msg = "Not enough raptor food."
                        self._fy_result_color = (220, 140, 100)
                        return
                    if r.cooldown > 0:
                        self._fy_result_msg = f"{r.name} is resting."
                        self._fy_result_color = (220, 140, 100)
                        return
                    self._begin_minigame("training", drill_key)
                    return
            # Hunt buttons
            for k, br in list(self._fy_btn_rects.items()):
                if not k.startswith("hunt_"):
                    continue
                if br.collidepoint(pos):
                    qkey = k[len("hunt_"):]
                    q = QUARRY[qkey]
                    if r.strength < q["strength_req"] * 0.6:
                        self._fy_result_msg = f"{r.name} cannot take a {q['label'].lower()}."
                        self._fy_result_color = (220, 140, 100)
                        return
                    if r.condition < 0.20 or r.hunger > 0.85 or r.cooldown > 0:
                        self._fy_result_msg = f"{r.name} is not ready to hunt."
                        self._fy_result_color = (220, 140, 100)
                        return
                    self._begin_minigame("hunting", qkey)
                    return
        elif self._fy_state in ("training", "hunting"):
            if self._fy_btn_rects.get("stop") and self._fy_btn_rects["stop"].collidepoint(pos):
                self._resolve_minigame(player, r)

    def handle_falconry_capture_click(self, pos, player):
        if self._fy_btn_rects.get("capture_cancel") and self._fy_btn_rects["capture_cancel"].collidepoint(pos):
            self.falconry_capture_open = False
            self._fy_state = "idle"
            return
        if self._fy_btn_rects.get("capture_stop") and self._fy_btn_rects["capture_stop"].collidepoint(pos):
            self._resolve_capture(player)

    # ──────────────────────────────────────────────────────────────────────────
    # Mini-game flow
    # ──────────────────────────────────────────────────────────────────────────
    def _begin_minigame(self, kind, key):
        self._fy_state = kind
        if kind == "training":
            self._fy_drill = key
            self._fy_quarry = None
        else:
            self._fy_drill = None
            self._fy_quarry = key
        self._fy_marker = 0.0
        self._fy_marker_dir = 1
        self._fy_timer = 0.0
        self._fy_result_msg = ""

    def _resolve_minigame(self, player, r):
        # Marker position quality: 1.0 dead-centre, fading toward edges
        dist = abs(self._fy_marker - 0.5)
        perf = max(0.0, 1.0 - dist * 2.5)
        if self._fy_state == "training":
            drill = TRAINING_DRILLS[self._fy_drill]
            # Deduct food
            player.inventory["raptor_food"] = player.inventory.get("raptor_food", 0) - drill["food_cost"]
            if player.inventory["raptor_food"] <= 0:
                del player.inventory["raptor_food"]
            before = getattr(r, drill["stat"])
            apply_training(r, self._fy_drill, perf)
            after = getattr(r, drill["stat"])
            self._fy_result_msg = f"{drill['label']}: {drill['stat']} {before:.2f} → {after:.2f}"
            self._fy_result_color = (180, 220, 150) if perf > 0.4 else (220, 200, 130)
        elif self._fy_state == "hunting":
            outcome = hunt_outcome(r, self._fy_quarry, random.Random())
            # Performance influences result slightly: better stop = better drops
            if perf > 0.8 and outcome["success"]:
                outcome["drops"].append(("feather", 2))
            apply_hunt(r, outcome)
            for item_id, count in outcome.get("drops", []):
                player.inventory[item_id] = player.inventory.get(item_id, 0) + count
            self._fy_result_msg = outcome["msg"]
            self._fy_result_color = (180, 220, 150) if outcome["success"] else (220, 140, 100)
            if outcome["success"]:
                player.raptor_records["best_hunts"] = max(player.raptor_records.get("best_hunts", 0), r.hunts_completed)
                player.raptor_records["best_bond"] = max(player.raptor_records.get("best_bond", 0.0), r.bond)
        self._fy_state = "idle"

    def _resolve_capture(self, player):
        species = self._fy_capture_species
        biome = self._fy_capture_biome
        dist = abs(self._fy_marker - 0.5)
        perf = max(0.0, 1.0 - dist * 4.0)   # tighter zone than training
        base = capture_success_chance(species)
        chance = max(0.05, min(0.98, base * (0.6 + perf * 0.8)))
        rng = random.Random()
        if rng.random() < chance:
            from falconry import make_raptor
            player._raptor_counter = getattr(player, "_raptor_counter", 0) + 1
            r = make_raptor(species, biome, player.world.seed, player._raptor_counter)
            player.tamed_raptors.append(r)
            player.discovered_raptor_species.add(species)
            # Remove the wild bird from the world so it doesn't double-exist
            src = getattr(self, "_fy_capture_source", None)
            if src is not None and src in player.world.entities:
                player.world.entities.remove(src)
            self._fy_result_msg = f"Captured {r.name} ({RAPTOR_SPECIES[species]['name']})."
            self._fy_result_color = (180, 220, 150)
            self.falconry_capture_open = False
            self._fy_state = "idle"
        else:
            self._fy_result_msg = "The bird escapes — try again."
            self._fy_result_color = (220, 140, 100)

    # ──────────────────────────────────────────────────────────────────────────
    # Helpers
    # ──────────────────────────────────────────────────────────────────────────
    def _current_biome(self, player):
        """Best-effort biome lookup for the player's position."""
        try:
            bx = int(player.x)
            return player.world.get_biodome(bx)
        except Exception:
            return ""

    # ──────────────────────────────────────────────────────────────────────────
    # Codex
    # ──────────────────────────────────────────────────────────────────────────
    def _draw_falconry_codex(self, player, gy0=58, gx_off=0):
        from constants import SCREEN_W, SCREEN_H
        from falconry import SPECIES_ORDER, RAPTOR_SPECIES, raptor_quality_stars
        x0 = gx_off + 14
        y0 = gy0 + 12
        grid_w = SCREEN_W - x0 - 320
        cell_w, cell_h = 168, 60
        cols = max(1, grid_w // (cell_w + 8))
        self._falconry_codex_rects = {}
        # Aggregate best stars per species
        best = {}
        for r in player.tamed_raptors:
            best[r.species] = max(best.get(r.species, 0), raptor_quality_stars(r))

        for i, key in enumerate(SPECIES_ORDER):
            sp = RAPTOR_SPECIES[key]
            row, col = divmod(i, cols)
            cx = x0 + col * (cell_w + 8)
            cy = y0 + row * (cell_h + 8)
            r = pygame.Rect(cx, cy, cell_w, cell_h)
            discovered = key in player.discovered_raptor_species
            bg = (40, 30, 16) if discovered else (22, 18, 10)
            border = (180, 140, 70) if discovered else (60, 50, 30)
            pygame.draw.rect(self.screen, bg, r, border_radius=4)
            pygame.draw.rect(self.screen, border, r, 1, border_radius=4)
            # Plumage swatch
            pygame.draw.circle(self.screen, sp["color"] if discovered else (60, 55, 45),
                               (r.x + 16, r.centery), 10)
            name = sp["name"] if discovered else "?????"
            ns = self.small.render(name, True,
                                   (235, 205, 145) if discovered else (90, 75, 55))
            self.screen.blit(ns, (r.x + 32, r.y + 6))
            tier_t = self.small.render(f"Tier {sp['tier']}", True,
                                       (175, 150, 100) if discovered else (75, 65, 45))
            self.screen.blit(tier_t, (r.x + 32, r.y + 24))
            if discovered:
                stars = best.get(key, 0)
                star_t = self.small.render("★" * stars + "·" * (5 - stars),
                                           True, (230, 200, 90))
                self.screen.blit(star_t, (r.x + 32, r.y + 40))
            self._falconry_codex_rects[key] = r

        # Right panel: summary
        info_x = SCREEN_W - 300
        info_y = y0
        pygame.draw.rect(self.screen, (22, 18, 10), (info_x, info_y, 290, 380), border_radius=6)
        pygame.draw.rect(self.screen, (140, 100, 50), (info_x, info_y, 290, 380), 1, border_radius=6)

        ttl = self.font.render("Falconry Log", True, (240, 210, 150))
        self.screen.blit(ttl, (info_x + 14, info_y + 8))

        lines = [
            f"Species discovered: {len(player.discovered_raptor_species)} / {len(SPECIES_ORDER)}",
            f"Tamed raptors:      {len(player.tamed_raptors)}",
            f"Total hunts won:    {sum(r.hunts_completed for r in player.tamed_raptors)}",
            f"Best bond:          {max((r.bond for r in player.tamed_raptors), default=0.0):.2f}",
        ]
        for i, ln in enumerate(lines):
            t = self.small.render(ln, True, (200, 175, 120))
            self.screen.blit(t, (info_x + 16, info_y + 40 + i * 18))

    # ──────────────────────────────────────────────────────────────────────────
    # Cooldown tick (called each frame from main.py)
    # ──────────────────────────────────────────────────────────────────────────
    def tick_raptor_cooldowns(self, dt, player):
        for r in getattr(player, "tamed_raptors", []):
            if r.cooldown > 0:
                r.cooldown = max(0.0, r.cooldown - dt)
                if r.cooldown <= 0 and r.state == "resting":
                    r.state = "perched"
            # Slow hunger drift while perched
            r.hunger = min(1.0, r.hunger + dt * 0.002)
