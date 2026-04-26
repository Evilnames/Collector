import pygame
from constants import SCREEN_W, SCREEN_H
from dogs import BREED_PROFILES, expressed_color_name, BASE_COLOR_ORDER, DILUTE_ORDER, WHITE_SPOTTING_ORDER, _expressed_categorical


class DogsMixin:

    def open_dog_view(self, dog):
        self.dog_view_open = True
        self._dv_dog = dog

    def open_dog_breeding(self, kennel_pos, dog_a, dog_b):
        self.dog_breeding_open = True
        self.active_kennel_pos = kennel_pos
        self._dbr_dog_a = dog_a
        self._dbr_dog_b = dog_b
        self._dbr_breed_btn  = None
        self._dbr_close_btn  = None

    # ── Shared helpers ────────────────────────────────────────────────────────

    def _draw_dog_stat_bar(self, label, value, lo, hi, x, y, bar_w, color):
        """Draw a labeled horizontal stat bar."""
        frac = (value - lo) / max(0.001, hi - lo)
        frac = max(0.0, min(1.0, frac))
        # Background
        pygame.draw.rect(self.screen, (40, 32, 20), (x + 90, y + 1, bar_w, 10))
        # Filled portion
        pygame.draw.rect(self.screen, color, (x + 90, y + 1, int(bar_w * frac), 10))
        # Label
        lbl = self.small.render(label[:10], True, (185, 165, 115))
        self.screen.blit(lbl, (x, y))
        # Value
        val_txt = self.small.render(f"{value:.2f}", True, (215, 195, 145))
        self.screen.blit(val_txt, (x + 90 + bar_w + 4, y))

    def _draw_ability_badge(self, x, y, label, active):
        """Draw a 90×24 ability badge."""
        bg = (55, 80, 45) if active else (35, 28, 18)
        border_col = (100, 175, 70) if active else (60, 50, 35)
        text_col   = (160, 230, 110) if active else (80, 65, 45)
        r = pygame.Rect(x, y, 90, 24)
        pygame.draw.rect(self.screen, bg, r, border_radius=4)
        pygame.draw.rect(self.screen, border_col, r, 1, border_radius=4)
        t = self.small.render(label, True, text_col)
        self.screen.blit(t, (r.centerx - t.get_width() // 2,
                              r.centery - t.get_height() // 2))

    def _draw_dog_portrait_box(self, dog, dx, dy, size=120):
        """Draw a dog portrait in a box at (dx, dy) of given size."""
        from Render.dogs import draw_dog_portrait
        draw_dog_portrait(self.screen, dx, dy, dog, size=size)

    # ── Dog View Panel ────────────────────────────────────────────────────────

    def _draw_dog_view_panel(self, player):
        dog = self._dv_dog
        if dog is None or dog.dead:
            self.dog_view_open = False
            return

        pw, ph = 680, 520
        px = SCREEN_W // 2 - pw // 2
        py = SCREEN_H // 2 - ph // 2
        traits = getattr(dog, "traits", {})

        # Panel background
        pygame.draw.rect(self.screen, (22, 16, 8), (px, py, pw, ph), border_radius=8)
        pygame.draw.rect(self.screen, (130, 100, 50), (px, py, pw, ph), 2, border_radius=8)

        # ── Title row ─────────────────────────────────────────────────────────
        dog_name  = traits.get("dog_name") or traits.get("uid", "")[:8]
        breed_str = traits.get("breed", "Mixed")
        gen_str   = f"Gen {traits.get('generation', 1)}"

        name_lbl  = self.font.render(dog_name, True, (230, 200, 140))
        breed_lbl = self.small.render(breed_str, True, (185, 155, 95))
        gen_lbl   = self.small.render(gen_str, True, (140, 120, 75))
        self.screen.blit(name_lbl,  (px + 16, py + 10))
        self.screen.blit(breed_lbl, (px + 16, py + 30))
        self.screen.blit(gen_lbl,   (px + pw - 80, py + 14))

        # Close button
        close_r = pygame.Rect(px + pw - 30, py + 8, 22, 22)
        pygame.draw.rect(self.screen, (100, 50, 30), close_r, border_radius=4)
        ct = self.small.render("X", True, (240, 180, 100))
        self.screen.blit(ct, (close_r.centerx - ct.get_width() // 2,
                               close_r.centery - ct.get_height() // 2))
        self._dv_close_btn = close_r

        # Stay/Follow toggle button
        stay_mode = getattr(dog, "stay_mode", False)
        stay_label = "STAY" if stay_mode else "FOLLOW"
        stay_col   = (60, 100, 50) if stay_mode else (50, 80, 120)
        stay_r = pygame.Rect(px + pw - 160, py + 8, 100, 24)
        pygame.draw.rect(self.screen, stay_col, stay_r, border_radius=4)
        pygame.draw.rect(self.screen, (100, 100, 80), stay_r, 1, border_radius=4)
        st = self.small.render(stay_label, True, (210, 225, 180))
        self.screen.blit(st, (stay_r.centerx - st.get_width() // 2,
                               stay_r.centery - st.get_height() // 2))
        self._dv_stay_btn = stay_r

        # ── Portrait ──────────────────────────────────────────────────────────
        portrait_size = 128
        self._draw_dog_portrait_box(dog, px + 14, py + 54, size=portrait_size)

        # ── Performance bars (right of portrait) ──────────────────────────────
        bar_x   = px + 158
        bar_w   = 240
        bar_y   = py + 56
        bar_gap = 20

        perf_bars = [
            ("SPEED",     "speed",       0.7, 1.3, (100, 190, 100)),
            ("ENDURANCE", "endurance",   0.7, 1.3, (80,  160, 220)),
            ("AGILITY",   "agility",     0.7, 1.3, (220, 180, 60)),
            ("STRENGTH",  "strength",    0.7, 1.3, (210, 100, 60)),
            ("NOSE",      "nose",        0.7, 1.3, (160, 100, 220)),
            ("ALERTNESS", "alertness",   0.7, 1.3, (220, 210, 80)),
        ]
        for i, (label, key, lo, hi, col) in enumerate(perf_bars):
            val = traits.get(key, 1.0)
            self._draw_dog_stat_bar(label, val, lo, hi, bar_x, bar_y + i * bar_gap, bar_w, col)

        # Temperament header line
        temp_y = bar_y + len(perf_bars) * bar_gap + 6
        temp_hdr = self.small.render("TEMPERAMENT", True, (180, 145, 70))
        self.screen.blit(temp_hdr, (bar_x, temp_y))
        pygame.draw.line(self.screen, (90, 70, 35),
                         (bar_x, temp_y + 13), (bar_x + bar_w + 55, temp_y + 13))

        temp_bars = [
            ("LOYALTY",      "loyalty",      0.0, 1.0, (100, 210, 140)),
            ("PLAYFULNESS",  "playfulness",  0.0, 1.0, (200, 170, 80)),
            ("STUBBORNNESS", "stubbornness", 0.0, 1.0, (200, 80,  80)),
            ("PREY DRIVE",   "prey_drive",   0.0, 1.0, (190, 130, 60)),
        ]
        temp_bar_y = temp_y + 18
        for i, (label, key, lo, hi, col) in enumerate(temp_bars):
            val = traits.get(key, 0.5)
            self._draw_dog_stat_bar(label, val, lo, hi, bar_x, temp_bar_y + i * bar_gap, bar_w, col)

        # ── Ability badges ────────────────────────────────────────────────────
        badge_y = py + 310
        abilities = [
            ("TRACK",  "has_tracking"),
            ("HERD",   "has_herding"),
            ("GUARD",  "has_guard"),
            ("FETCH",  "has_retrieve"),
        ]
        total_badge_w = 4 * 90 + 3 * 10
        badge_x = px + pw // 2 - total_badge_w // 2
        for j, (badge_label, trait_key) in enumerate(abilities):
            active = traits.get(trait_key, False)
            self._draw_ability_badge(badge_x + j * 100, badge_y, badge_label, active)

        # ── Visual traits (bottom-left) ────────────────────────────────────────
        vt_x = px + 14
        vt_y = py + 350
        pygame.draw.line(self.screen, (70, 55, 25), (vt_x, vt_y), (vt_x + 310, vt_y))
        vt_hdr = self.small.render("VISUAL TRAITS", True, (175, 148, 85))
        self.screen.blit(vt_hdr, (vt_x, vt_y + 4))

        coat_col  = traits.get("coat_color", (160, 100, 50))
        base_color   = traits.get("base_color", "yellow")
        dilute_exp   = traits.get("dilute_expressed", False)
        dilute_carry = traits.get("dilute_carrier", False)
        color_name   = expressed_color_name(base_color, dilute_exp)
        white_spot   = traits.get("white_spotting", "solid")
        eye_col_key  = traits.get("eye_color", "brown")
        from dogs import DOG_EYE_COLORS
        eye_rgb = DOG_EYE_COLORS.get(eye_col_key, (100, 60, 20))

        # Dilute carrier annotation
        if dilute_exp:
            dilute_str = "dilute/dilute (expressed)"
        elif dilute_carry:
            dilute_str = "carries dilute"
        else:
            dilute_str = "no dilute"

        vt_lines = [
            (f"Color: {color_name}", coat_col),
            (f"Genetics: {base_color} | {dilute_str}", None),
            (f"White: {white_spot}  Pattern: {traits.get('coat_pattern', '?')}", None),
            (f"Length: {traits.get('coat_length', '?')}  Type: {traits.get('coat_type', '?')}", None),
            (f"Ears: {traits.get('ear_type', '?')}  Tail: {traits.get('tail_type', '?')}", None),
            (f"Eyes: {eye_col_key}", eye_rgb),
            (f"Size: {traits.get('size_class', '?')}", None),
        ]
        line_h = 16
        for k, (text, swatch_col) in enumerate(vt_lines):
            t = self.small.render(text, True, (170, 148, 100))
            self.screen.blit(t, (vt_x, vt_y + 20 + k * line_h))
            if swatch_col:
                pygame.draw.rect(self.screen, swatch_col,
                                 (vt_x + t.get_width() + 6, vt_y + 23 + k * line_h, 10, 8))

        # ── Lineage (bottom-right) ─────────────────────────────────────────────
        lin_x = px + 360
        lin_y = py + 350
        pygame.draw.line(self.screen, (70, 55, 25), (lin_x, lin_y), (lin_x + 305, lin_y))
        lin_hdr = self.small.render("LINEAGE", True, (175, 148, 85))
        self.screen.blit(lin_hdr, (lin_x, lin_y + 4))

        pa_uid = getattr(dog, "parent_a_uid", None)
        pb_uid = getattr(dog, "parent_b_uid", None)
        gen = traits.get("generation", 1)

        if pa_uid is None and pb_uid is None:
            lin_txt = f"Wild-caught (Gen {gen})"
            t = self.small.render(lin_txt, True, (150, 130, 80))
            self.screen.blit(t, (lin_x, lin_y + 22))
        else:
            # Look up parent breeds from world entities
            world = getattr(self.screen, "_world_ref", None)
            entity_map = {}
            if world is not None:
                entity_map = {getattr(e, "uid", None): e for e in getattr(world, "entities", [])}
            def breed_of(uid):
                e = entity_map.get(uid)
                if e:
                    return e.traits.get("breed", "Unknown")
                return "Unknown"
            pa_breed = breed_of(pa_uid) if pa_uid else "Unknown"
            pb_breed = breed_of(pb_uid) if pb_uid else "Unknown"
            t1 = self.small.render(f"Parent A: {pa_breed}", True, (150, 130, 80))
            t2 = self.small.render(f"Parent B: {pb_breed}", True, (150, 130, 80))
            self.screen.blit(t1, (lin_x, lin_y + 22))
            self.screen.blit(t2, (lin_x, lin_y + 38))

    # ── Dog Breeding Panel ────────────────────────────────────────────────────

    def _draw_dog_breeding_panel(self, player):
        dog_a = self._dbr_dog_a
        dog_b = self._dbr_dog_b
        if dog_a is None or dog_b is None:
            self.dog_breeding_open = False
            return

        pw, ph = 580, 470
        px = SCREEN_W // 2 - pw // 2
        py = SCREEN_H // 2 - ph // 2

        pygame.draw.rect(self.screen, (22, 16, 8), (px, py, pw, ph), border_radius=8)
        pygame.draw.rect(self.screen, (120, 95, 50), (px, py, pw, ph), 2, border_radius=8)

        title = self.font.render("KENNEL BREEDING", True, (210, 180, 100))
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, py + 10))

        # Close button
        close_r = pygame.Rect(px + pw - 30, py + 8, 22, 22)
        pygame.draw.rect(self.screen, (100, 50, 30), close_r, border_radius=4)
        ct = self.small.render("X", True, (240, 180, 100))
        self.screen.blit(ct, (close_r.centerx - ct.get_width() // 2,
                               close_r.centery - ct.get_height() // 2))
        self._dbr_close_btn = close_r

        # Two stat cards
        card_w, card_h = 220, 245
        left_x  = px + 14
        right_x = px + pw - 14 - card_w
        card_y  = py + 44

        self._draw_dog_stat_card(dog_a, left_x, card_y, card_w, card_h, player)
        self._draw_dog_stat_card(dog_b, right_x, card_y, card_w, card_h, player)

        # Predictions
        pred_y = card_y + card_h + 8
        breed_a = dog_a.traits.get("breed", "Mixed")
        breed_b = dog_b.traits.get("breed", "Mixed")
        if breed_a == breed_b and "Mixed" not in breed_a:
            offspring_breed = breed_a
        else:
            a_s = breed_a.split()[0]
            b_s = breed_b.split()[0]
            offspring_breed = f"Mixed ({a_s}/{b_s})"

        perf_keys = ["speed", "endurance", "agility", "strength", "nose", "alertness"]
        avg_perf = {k: (dog_a.traits.get(k, 1.0) + dog_b.traits.get(k, 1.0)) / 2 for k in perf_keys}
        pred_line = "  ".join(f"{k[:3].upper()} ~{v:.2f}" for k, v in avg_perf.items())

        breed_lbl = self.small.render(f"Breed: {offspring_breed[:28]}", True, (180, 155, 90))
        pred_lbl  = self.small.render(pred_line, True, (150, 130, 75))
        self.screen.blit(breed_lbl, (px + pw // 2 - breed_lbl.get_width() // 2, pred_y))
        self.screen.blit(pred_lbl,  (px + pw // 2 - pred_lbl.get_width() // 2,  pred_y + 16))

        # Color outcome prediction
        col_y = pred_y + 34
        color_hdr = self.small.render("COLOR OUTCOMES:", True, (175, 150, 80))
        self.screen.blit(color_hdr, (px + 14, col_y))
        self._draw_color_outcome_row(dog_a, dog_b, px + 14, col_y + 14, pw - 28)

        # Ability inheritance odds
        ab_y = col_y + 52
        for j, ability in enumerate(("tracking", "herding", "guard", "retrieve")):
            gene = f"{ability}_gene"
            ga = getattr(dog_a, "genotype", {}).get(gene, [None, None])
            gb = getattr(dog_b, "genotype", {}).get(gene, [None, None])
            carriers_a = sum(1 for a in ga if a == ability)
            carriers_b = sum(1 for b in gb if b == ability)
            p = (carriers_a / 2) * (carriers_b / 2)
            col = (120, 200, 100) if p > 0 else (80, 65, 45)
            lbl = self.small.render(f"{ability.upper()[:5]}: {int(p*100)}%", True, col)
            self.screen.blit(lbl, (px + 20 + j * 138, ab_y))

        # Breed button
        cool_a = getattr(dog_a, "_breed_cooldown", 0)
        cool_b = getattr(dog_b, "_breed_cooldown", 0)
        can_breed = (cool_a <= 0 or cool_a >= 9990) and (cool_b <= 0 or cool_b >= 9990)
        breed_r = pygame.Rect(SCREEN_W // 2 - 80, py + ph - 48, 160, 30)
        btn_col = (55, 110, 55) if can_breed else (60, 45, 30)
        pygame.draw.rect(self.screen, btn_col, breed_r, border_radius=6)
        pygame.draw.rect(self.screen, (90, 80, 50), breed_r, 1, border_radius=6)

        if can_breed:
            bt = self.small.render("BREED", True, (160, 230, 120))
        else:
            max_cool = max(cool_a if cool_a < 9990 else 0,
                           cool_b if cool_b < 9990 else 0)
            bt = self.small.render(f"Cooldown {int(max_cool)}s", True, (150, 110, 60))
        self.screen.blit(bt, (breed_r.centerx - bt.get_width() // 2,
                               breed_r.centery - bt.get_height() // 2))
        self._dbr_breed_btn = breed_r if can_breed else None

    def _draw_dog_stat_card(self, dog, cx, cy, cw, ch, player):
        """Compact stat card for breeding panel."""
        traits = getattr(dog, "traits", {})
        pygame.draw.rect(self.screen, (32, 24, 14), (cx, cy, cw, ch), border_radius=6)
        pygame.draw.rect(self.screen, (90, 70, 40), (cx, cy, cw, ch), 1, border_radius=6)

        # Portrait
        portrait_size = 60
        self._draw_dog_portrait_box(dog, cx + 4, cy + 4, size=portrait_size)

        # UID + breed
        uid_str   = getattr(dog, "uid", "")[:8]
        breed_str = traits.get("breed", "Mixed")[:16]
        uid_lbl   = self.small.render(uid_str, True, (120, 100, 60))
        breed_lbl = self.small.render(breed_str, True, (175, 150, 90))
        self.screen.blit(uid_lbl,   (cx + 68, cy + 6))
        self.screen.blit(breed_lbl, (cx + 68, cy + 20))

        # 6 performance bars
        bar_y = cy + 68
        bar_w = cw - 12
        perf = [
            ("SPD", "speed",     0.7, 1.3, (100, 190, 100)),
            ("END", "endurance", 0.7, 1.3, (80, 160, 220)),
            ("AGI", "agility",   0.7, 1.3, (220, 180, 60)),
            ("STR", "strength",  0.7, 1.3, (210, 100, 60)),
            ("NOS", "nose",      0.7, 1.3, (160, 100, 220)),
            ("ALT", "alertness", 0.7, 1.3, (220, 210, 80)),
        ]
        for i, (label, key, lo, hi, col) in enumerate(perf):
            val  = traits.get(key, 1.0)
            frac = max(0, min(1, (val - lo) / (hi - lo)))
            bx = cx + 6
            by = bar_y + i * 18
            pygame.draw.rect(self.screen, (40, 32, 20), (bx + 30, by + 1, bar_w - 60, 10))
            pygame.draw.rect(self.screen, col,           (bx + 30, by + 1, int((bar_w - 60) * frac), 10))
            lt = self.small.render(label, True, (160, 140, 90))
            self.screen.blit(lt, (bx, by))
            vt = self.small.render(f"{val:.2f}", True, (185, 165, 105))
            self.screen.blit(vt, (bx + 30 + bar_w - 55, by))

        # Ability mini-badges
        ab_y = bar_y + len(perf) * 18 + 4
        ab_x = cx + 6
        for j, ability in enumerate(("tracking", "herding", "guard", "retrieve")):
            has = traits.get(f"has_{ability}", False)
            short = ability[:5].upper()
            ab_col = (70, 130, 60) if has else (40, 32, 20)
            tc     = (140, 220, 100) if has else (70, 58, 38)
            r = pygame.Rect(ab_x + j * 48, ab_y, 44, 16)
            pygame.draw.rect(self.screen, ab_col, r, border_radius=3)
            t = self.small.render(short, True, tc)
            self.screen.blit(t, (r.centerx - t.get_width() // 2,
                                  r.centery - t.get_height() // 2))

        # Cooldown warning
        cool = getattr(dog, "_breed_cooldown", 0)
        if 0 < cool < 9990:
            cw_txt = self.small.render(f"CD {int(cool)}s", True, (200, 120, 60))
            self.screen.blit(cw_txt, (cx + cw - cw_txt.get_width() - 4, cy + ch - 18))

    def _draw_color_outcome_row(self, dog_a, dog_b, x, y, row_w):
        """Show possible color outcomes for offspring with probability swatches."""
        from dogs import BASE_COLOR_ORDER, COLOR_RGB, expressed_color_name, _expressed_categorical
        geno_a = getattr(dog_a, "genotype", {})
        geno_b = getattr(dog_b, "genotype", {})

        base_a = geno_a.get("base_color_gene", ["yellow", "yellow"])
        base_b = geno_b.get("base_color_gene", ["yellow", "yellow"])
        dil_a  = geno_a.get("dilute_gene", ["full", "full"])
        dil_b  = geno_b.get("dilute_gene", ["full", "full"])

        # Enumerate the 4 possible offspring combinations (each parent contributes 1 allele)
        outcomes = {}
        for ba in base_a:
            for bb in base_b:
                expressed_base = _expressed_categorical([ba, bb], BASE_COLOR_ORDER)
                for da in dil_a:
                    for db in dil_b:
                        dilute_exp = (da == "dilute" and db == "dilute")
                        color_key = (expressed_base, dilute_exp)
                        outcomes[color_key] = outcomes.get(color_key, 0) + 1

        total = sum(outcomes.values())
        sorted_outcomes = sorted(outcomes.items(), key=lambda kv: -kv[1])

        swatch_w = min(120, row_w // max(1, len(sorted_outcomes)))
        for idx, ((b_color, dil_exp), count) in enumerate(sorted_outcomes[:5]):
            rgb = COLOR_RGB.get((b_color, "dilute" if dil_exp else "full"), (160, 100, 50))
            name = expressed_color_name(b_color, dil_exp)
            pct  = int(count / total * 100)
            sx = x + idx * (swatch_w + 4)
            # Color swatch
            pygame.draw.rect(self.screen, rgb, (sx, y, swatch_w - 2, 14))
            pygame.draw.rect(self.screen, (80, 65, 35), (sx, y, swatch_w - 2, 14), 1)
            # Label below
            lbl_col = (200, 175, 110) if pct >= 25 else (140, 120, 70)
            nl = self.small.render(f"{name[:12]} {pct}%", True, lbl_col)
            self.screen.blit(nl, (sx, y + 16))
