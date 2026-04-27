import random
import pygame
from constants import SCREEN_W, SCREEN_H


class HorseMixin:
    """UI logic for horses: breaking minigame, breeding panel, stamina HUD."""

    # ------------------------------------------------------------------
    # Horse Breaking Minigame
    # ------------------------------------------------------------------

    def open_horse_breaking(self, horse):
        from horses import TEMPERAMENT_BUCK_INTERVAL, TEMPERAMENT_BREAK_TIME
        self._hb_active        = True
        self._hb_horse         = horse
        self._hb_phase         = "intro"
        self._hb_intro_timer   = 2.5
        self._hb_balance       = 50.0
        self._hb_direction     = random.choice([-1, 1])
        self._hb_buck_interval = TEMPERAMENT_BUCK_INTERVAL[horse.traits["temperament"]]
        self._hb_buck_timer    = self._hb_buck_interval
        self._hb_max_time      = TEMPERAMENT_BREAK_TIME[horse.traits["temperament"]]
        self._hb_active_timer  = 0.0
        self._hb_result        = None
        self._hb_result_timer  = 0.0

    def update_horse_breaking(self, keys, dt):
        """Tick the breaking minigame. Returns 'success', 'fail', or None."""
        if not self._hb_active:
            return None

        if self._hb_phase == "intro":
            self._hb_intro_timer -= dt
            if self._hb_intro_timer <= 0:
                self._hb_phase = "active"
            return None

        if self._hb_phase == "result":
            self._hb_result_timer -= dt
            if self._hb_result_timer <= 0:
                self._hb_active = False
                result = self._hb_result
                self._hb_result = None
                return result
            return None

        # --- Active phase ---
        self._hb_active_timer += dt

        # Player presses A or D to counter-balance
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self._hb_balance -= 22 * dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self._hb_balance += 22 * dt

        # Horse bucks every buck_interval seconds
        self._hb_buck_timer -= dt
        if self._hb_buck_timer <= 0:
            self._hb_direction = random.choice([-1, 1])
            self._hb_balance += self._hb_direction * 26
            # Bucks get faster as the ride progresses
            self._hb_buck_timer = max(0.3, self._hb_buck_interval - self._hb_active_timer * 0.06)

        # Mild drift toward center — not enough to save you if you're losing
        self._hb_balance += (50.0 - self._hb_balance) * 0.25 * dt

        # Clamp balance
        self._hb_balance = max(0.0, min(100.0, self._hb_balance))

        # Fall off if outside safe range
        if self._hb_balance < 15 or self._hb_balance > 85:
            self._hb_phase = "result"
            self._hb_result = "fail"
            self._hb_result_timer = 1.5
            return None

        # Success when surviving full duration
        if self._hb_active_timer >= self._hb_max_time:
            self._hb_phase = "result"
            self._hb_result = "success"
            self._hb_result_timer = 1.5
            return None

        return None

    def _draw_horse_breaking_overlay(self, player):
        # Full-screen dimmed backdrop
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        cx, cy = SCREEN_W // 2, SCREEN_H // 2

        horse = self._hb_horse
        temp  = horse.traits["temperament"] if horse else "spirited"
        temp_labels = {"calm": "CALM HORSE", "spirited": "SPIRITED HORSE", "wild": "WILD HORSE"}
        temp_colors = {"calm": (80, 200, 80), "spirited": (220, 180, 40), "wild": (220, 60, 60)}
        coat  = horse.traits.get("coat_color", (160, 115, 65)) if horse else (160, 115, 65)

        # Panel background
        pw, ph = 440, 240
        px, py = cx - pw // 2, cy - ph // 2
        pygame.draw.rect(self.screen, (30, 22, 14), (px, py, pw, ph), border_radius=10)
        pygame.draw.rect(self.screen, temp_colors.get(temp, (180, 180, 180)),
                         (px, py, pw, ph), 3, border_radius=10)

        # Title
        title_txt = self.font.render(temp_labels.get(temp, "HORSE"), True, temp_colors.get(temp, (180, 180, 180)))
        self.screen.blit(title_txt, (cx - title_txt.get_width() // 2, py + 12))

        # Coat swatch
        pygame.draw.rect(self.screen, coat, (px + 16, py + 46, 28, 28))
        pygame.draw.rect(self.screen, (200, 180, 140), (px + 16, py + 46, 28, 28), 2)

        if self._hb_phase == "intro":
            msg = self.font.render("HOLD ON TIGHT!", True, (240, 220, 160))
            sub = self.small.render("Press A / D to stay balanced", True, (180, 165, 130))
            countdown = self.font.render(f"Starting in {self._hb_intro_timer:.1f}s...", True, (200, 180, 120))
            self.screen.blit(msg, (cx - msg.get_width() // 2, cy - 20))
            self.screen.blit(sub, (cx - sub.get_width() // 2, cy + 12))
            self.screen.blit(countdown, (cx - countdown.get_width() // 2, cy + 38))
            return

        if self._hb_phase == "result":
            if self._hb_result == "success":
                msg = self.font.render("HORSE BROKEN!", True, (80, 220, 80))
                sub = self.small.render("The horse accepts you as its rider.", True, (150, 220, 150))
            else:
                msg = self.font.render("THROWN OFF!", True, (220, 80, 80))
                sub = self.small.render("The horse ran away. Try again.", True, (220, 150, 150))
            self.screen.blit(msg, (cx - msg.get_width() // 2, cy - 20))
            self.screen.blit(sub, (cx - sub.get_width() // 2, cy + 12))
            return

        # Active phase: draw balance bar
        bar_w, bar_h = 320, 20
        bar_x = cx - bar_w // 2
        bar_y = py + 90

        # Background bar
        pygame.draw.rect(self.screen, (50, 38, 24), (bar_x, bar_y, bar_w, bar_h))

        # Safe zone (center band)
        safe_w = int(bar_w * 0.70)   # [15%, 85%]
        safe_x = bar_x + int(bar_w * 0.15)
        pygame.draw.rect(self.screen, (40, 70, 40), (safe_x, bar_y, safe_w, bar_h))

        # Balance indicator
        ind_x = bar_x + int(self._hb_balance / 100 * bar_w)
        pygame.draw.rect(self.screen, (240, 200, 80),
                         (ind_x - 4, bar_y - 3, 8, bar_h + 6))

        # Danger zones highlight
        pygame.draw.rect(self.screen, (180, 50, 50), (bar_x, bar_y, int(bar_w * 0.15), bar_h))
        pygame.draw.rect(self.screen, (180, 50, 50),
                         (bar_x + int(bar_w * 0.85), bar_y, int(bar_w * 0.15) + 1, bar_h))

        pygame.draw.rect(self.screen, (160, 130, 80), (bar_x, bar_y, bar_w, bar_h), 2)

        bal_lbl = self.small.render("BALANCE", True, (180, 155, 110))
        self.screen.blit(bal_lbl, (bar_x, bar_y - 16))

        # Timer progress bar
        timer_w, timer_h = 320, 8
        timer_x = cx - timer_w // 2
        timer_y = bar_y + bar_h + 18
        pygame.draw.rect(self.screen, (35, 28, 18), (timer_x, timer_y, timer_w, timer_h))
        pct = min(1.0, self._hb_active_timer / self._hb_max_time)
        color = (100, 180, 100) if pct < 0.6 else (220, 180, 40) if pct < 0.85 else (80, 220, 80)
        pygame.draw.rect(self.screen, color, (timer_x, timer_y, int(timer_w * pct), timer_h))
        pygame.draw.rect(self.screen, (140, 110, 70), (timer_x, timer_y, timer_w, timer_h), 1)

        time_lbl = self.small.render(
            f"HOLD: {self._hb_active_timer:.1f} / {self._hb_max_time:.0f}s",
            True, (160, 135, 95)
        )
        self.screen.blit(time_lbl, (timer_x, timer_y + 12))

        # Direction hint
        hint = "← A" if self._hb_direction > 0 else "D →"
        hint_color = (220, 200, 100)
        ht = self.font.render(hint, True, hint_color)
        self.screen.blit(ht, (cx - ht.get_width() // 2, py + ph - 50))

    # ------------------------------------------------------------------
    # Breeding Panel
    # ------------------------------------------------------------------

    def open_horse_breeding(self, stable_pos, horse_a, horse_b):
        self.horse_breeding_open = True
        self.active_stable_pos   = stable_pos
        self._hbr_horse_a        = horse_a
        self._hbr_horse_b        = horse_b
        self._hbr_breed_btn      = None
        self._hbr_close_btn      = None

    def _draw_horse_breeding_panel(self, player):
        horse_a = self._hbr_horse_a
        horse_b = self._hbr_horse_b
        if horse_a is None or horse_b is None:
            self.horse_breeding_open = False
            return

        pw, ph = 500, 340
        px = SCREEN_W // 2 - pw // 2
        py = SCREEN_H // 2 - ph // 2

        pygame.draw.rect(self.screen, (28, 20, 12), (px, py, pw, ph), border_radius=8)
        pygame.draw.rect(self.screen, (160, 120, 60), (px, py, pw, ph), 3, border_radius=8)

        title = self.font.render("HORSE BREEDING", True, (215, 185, 110))
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, py + 10))

        # Close button
        close_r = pygame.Rect(px + pw - 30, py + 8, 22, 22)
        pygame.draw.rect(self.screen, (100, 50, 30), close_r, border_radius=4)
        ct = self.small.render("X", True, (240, 180, 100))
        self.screen.blit(ct, (close_r.centerx - ct.get_width() // 2,
                               close_r.centery - ct.get_height() // 2))
        self._hbr_close_btn = close_r

        # Draw two horse stat cards side by side
        card_w = 190
        left_x  = px + 14
        right_x = px + pw - 14 - card_w
        card_y  = py + 46

        self._draw_horse_stat_card(horse_a, left_x, card_y, card_w, 200, player)
        self._draw_horse_stat_card(horse_b, right_x, card_y, card_w, 200, player)

        # Predicted offspring stats (allele averages)
        off_sr = (horse_a.traits["speed_rating"] + horse_b.traits["speed_rating"]) / 2
        off_sm = (horse_a.traits["stamina_max"]  + horse_b.traits["stamina_max"])  / 2
        pred_y = card_y + 210
        pred_lbl = self.small.render(
            f"Offspring: SPD ~{off_sr:.2f}  STA ~{off_sm:.2f}  (±noise)",
            True, (185, 165, 110)
        )
        self.screen.blit(pred_lbl, (SCREEN_W // 2 - pred_lbl.get_width() // 2, pred_y))

        # Coat pattern allele odds
        geno_a = getattr(horse_a, 'genotype', {})
        geno_b = getattr(horse_b, 'genotype', {})
        pa_pair = geno_a.get("coat_pattern_gene", ["solid", "solid"])
        pb_pair = geno_b.get("coat_pattern_gene", ["solid", "solid"])
        all_combos = [a + "/" + b for a in pa_pair for b in pb_pair]
        from animals import COAT_PATTERN_ORDER, _expressed_categorical
        pattern_counts = {}
        for combo in all_combos:
            expressed = _expressed_categorical(combo.split("/"), COAT_PATTERN_ORDER)
            pattern_counts[expressed] = pattern_counts.get(expressed, 0) + 1
        pattern_parts = [f"{p}: {c * 25}%" for p, c in sorted(pattern_counts.items())]
        pat_lbl = self.small.render("Pattern odds: " + "  ".join(pattern_parts), True, (160, 140, 100))
        self.screen.blit(pat_lbl, (SCREEN_W // 2 - pat_lbl.get_width() // 2, pred_y + 16))

        # Mutation carrier check
        mut_a = geno_a.get("mutation", [None, None])
        mut_b = geno_b.get("mutation", [None, None])
        carrier_types = {a for a in mut_a + mut_b if a is not None}
        if carrier_types:
            for ct in carrier_types:
                combos_ct = [a == ct and b == ct for a in mut_a for b in mut_b]
                expr_pct = sum(combos_ct) * 25
                car_s = self.small.render(f"★ {ct} mutation: {expr_pct}% express, carriers possible",
                                           True, (220, 190, 70))
                pred_y += 16
                self.screen.blit(car_s, (SCREEN_W // 2 - car_s.get_width() // 2, pred_y + 16))

        if getattr(player, "horse_breeding_mastery", False):
            calm_lbl = self.small.render("Breeding Mastery: offspring temperament skews calmer",
                                          True, (100, 200, 100))
            self.screen.blit(calm_lbl, (SCREEN_W // 2 - calm_lbl.get_width() // 2, pred_y + 32))

        # Breed button — blocked if either horse has no_breed set
        cooldown_a = horse_a._breed_cooldown
        cooldown_b = horse_b._breed_cooldown
        no_breed_blocked = getattr(horse_a, 'no_breed', False) or getattr(horse_b, 'no_breed', False)
        on_cooldown = (cooldown_a < 9999 and cooldown_a > 0) or (cooldown_b < 9999 and cooldown_b > 0)
        blocked = on_cooldown or no_breed_blocked

        btn_w, btn_h = 160, 30
        btn_x = SCREEN_W // 2 - btn_w // 2
        btn_y = py + ph - 44
        btn_r = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
        btn_color = (80, 55, 25) if blocked else (130, 90, 35)
        pygame.draw.rect(self.screen, btn_color, btn_r, border_radius=6)
        pygame.draw.rect(self.screen, (180, 140, 70), btn_r, 2, border_radius=6)
        if no_breed_blocked:
            btn_txt = self.small.render("BREEDING DISABLED", True, (200, 80, 80))
        elif on_cooldown:
            cd = max(cooldown_a if cooldown_a < 9999 else 0,
                     cooldown_b if cooldown_b < 9999 else 0)
            btn_txt = self.small.render(f"COOLDOWN {int(cd)}s", True, (130, 105, 60))
        else:
            btn_txt = self.font.render("BREED", True, (240, 210, 130))
        self.screen.blit(btn_txt, (btn_r.centerx - btn_txt.get_width() // 2,
                                    btn_r.centery - btn_txt.get_height() // 2))
        self._hbr_breed_btn = None if blocked else btn_r

    def _draw_horse_stat_card(self, horse, cx, cy, cw, ch, player):
        traits = horse.traits
        coat   = traits.get("coat_color", (160, 115, 65))

        pygame.draw.rect(self.screen, (40, 30, 18), (cx, cy, cw, ch), border_radius=6)
        pygame.draw.rect(self.screen, (120, 90, 50), (cx, cy, cw, ch), 2, border_radius=6)

        # Coat swatch
        pygame.draw.rect(self.screen, coat, (cx + 6, cy + 6, 24, 24))
        pygame.draw.rect(self.screen, (180, 155, 115), (cx + 6, cy + 6, 24, 24), 1)

        # UID snippet
        uid_lbl = self.small.render(horse.uid[:8], True, (140, 120, 80))
        self.screen.blit(uid_lbl, (cx + 36, cy + 6))

        # Temperament badge
        temp = traits.get("temperament", "spirited")
        t_colors = {"calm": (80, 200, 80), "spirited": (220, 180, 40), "wild": (220, 60, 60)}
        t_lbl = self.small.render(temp.upper(), True, t_colors.get(temp, (180, 180, 180)))
        self.screen.blit(t_lbl, (cx + 36, cy + 20))

        # Mutation badge
        mut = traits.get("mutation")
        if mut:
            m_colors = {"golden": (220, 180, 30), "albino": (230, 225, 215),
                        "giant": (120, 180, 240), "miniature": (200, 140, 220)}
            m_lbl = self.small.render(mut.upper(), True, m_colors.get(mut, (200, 200, 200)))
            self.screen.blit(m_lbl, (cx + cw - m_lbl.get_width() - 6, cy + 6))

        # Speed bar
        sr = traits.get("speed_rating", 1.0)
        self._draw_stat_bar(cx + 6, cy + 42, cw - 12, 10, sr / 1.4, (80, 180, 255),
                            f"SPD {sr:.2f}")
        # Stamina bar
        sm = traits.get("stamina_max", 1.0)
        self._draw_stat_bar(cx + 6, cy + 62, cw - 12, 10, sm / 1.3, (80, 220, 120),
                            f"STA {sm:.2f}")

        # Tame status
        status = "TAMED" if horse.tamed else "WILD"
        s_color = (100, 220, 100) if horse.tamed else (220, 100, 100)
        s_lbl = self.small.render(status, True, s_color)
        self.screen.blit(s_lbl, (cx + 6, cy + 84))

        # Horseshoe indicator
        if traits.get("horseshoe_applied"):
            hs_lbl = self.small.render("SHOD", True, (200, 200, 180))
            self.screen.blit(hs_lbl, (cx + cw - hs_lbl.get_width() - 6, cy + 84))

        # Breed cooldown warning
        if 0 < horse._breed_cooldown < 9999:
            cd_lbl = self.small.render(f"CD {int(horse._breed_cooldown)}s", True, (200, 120, 60))
            self.screen.blit(cd_lbl, (cx + 6, cy + ch - 20))

    def _draw_stat_bar(self, bx, by, bw, bh, pct, color, label):
        pct = max(0.0, min(1.0, pct))
        pygame.draw.rect(self.screen, (35, 28, 18), (bx, by, bw, bh))
        pygame.draw.rect(self.screen, color, (bx, by, int(bw * pct), bh))
        pygame.draw.rect(self.screen, (100, 80, 50), (bx, by, bw, bh), 1)
        lbl = self.small.render(label, True, (180, 160, 110))
        self.screen.blit(lbl, (bx + bw + 4, by - 1))

    # ------------------------------------------------------------------
    # Stamina HUD (always visible when mounted)
    # ------------------------------------------------------------------

    def _draw_horse_stamina_hud(self, player):
        if getattr(player, "mounted_horse", None) is None:
            return
        horse = player.mounted_horse
        if horse is None:
            return

        BAR_W, BAR_H = 130, 12
        bx = SCREEN_W // 2 - BAR_W // 2
        by = SCREEN_H - 85

        # Background
        pygame.draw.rect(self.screen, (25, 18, 10), (bx - 2, by - 2, BAR_W + 4, BAR_H + 4))

        # Fill
        pct = horse.stamina / 100.0
        if pct > 0.5:
            bar_col = (80, 200, 80)
        elif pct > 0.2:
            bar_col = (220, 180, 40)
        else:
            bar_col = (220, 60, 40)

        # Flash red when exhausted
        cooldown = getattr(player, "_sprint_cooldown", 0.0)
        if cooldown > 0:
            import math
            flash = abs(math.sin(cooldown * 8))
            bar_col = tuple(int(c * flash) for c in (220, 60, 40))

        pygame.draw.rect(self.screen, bar_col, (bx, by, int(BAR_W * pct), BAR_H))
        pygame.draw.rect(self.screen, (140, 110, 60), (bx, by, BAR_W, BAR_H), 2)

        # Labels
        sta_lbl = self.small.render("STAMINA", True, (190, 165, 110))
        self.screen.blit(sta_lbl, (bx + BAR_W // 2 - sta_lbl.get_width() // 2, by - 14))

        sr = horse.traits.get("speed_rating", 1.0)
        spd_mult = 1.0 + sr
        if horse.traits.get("horseshoe_applied"):
            spd_mult *= 1.0 + getattr(player, "horse_shoe_bonus", 0.05)
        spd_lbl = self.small.render(f"SPD {spd_mult:.1f}x", True, (160, 200, 240))
        self.screen.blit(spd_lbl, (bx + BAR_W + 8, by))

        # [SPACE] sprint hint when stamina is available
        if horse.stamina > 10 and cooldown <= 0:
            hint = self.small.render("[SPACE] Sprint", True, (130, 115, 85))
            self.screen.blit(hint, (bx, by + BAR_H + 3))
