import math
import pygame
from constants import SCREEN_W, SCREEN_H
from pigments import (
    PIGMENT_TYPES, GRIND_STYLES, RAW_TO_PIGMENT, CALCINATION_MAP,
    PIGMENT_FAMILY_ORDER,
)

_BG      = ( 18,  14,  22)
_CELL_BG = ( 32,  26,  40)
_ACCENT  = (175, 140, 210)
_TITLE_C = (240, 232, 255)
_LABEL_C = (195, 175, 220)
_DIM_C   = ( 90,  78, 110)
_HINT_C  = (135, 115, 165)
_GREEN   = (100, 220, 110)
_YELLOW  = (220, 200,  80)
_RED     = (220,  80,  70)

_GRIND_TOTAL   = 8          # rhythm presses to finish
_GRIND_SPEED   = 1.8        # oscillator cycles per second
_HIT_WINDOW    = 0.18       # ±fraction of cycle to count as "good"


def _quality_color(q):
    if q >= 0.75:
        return _GREEN
    if q >= 0.45:
        return _YELLOW
    return _RED


def _consume_item(player, item_key, count=1):
    cur = player.inventory.get(item_key, 0)
    new = cur - count
    if new <= 0:
        player.inventory.pop(item_key, None)
    else:
        player.inventory[item_key] = new


def _raw_items_in_inventory(player):
    result = []
    for item_key, qty in player.inventory.items():
        if item_key in RAW_TO_PIGMENT and qty > 0:
            result.append((item_key, qty))
    return result


class PigmentMixin:

    # ─── top-level draw dispatcher ────────────────────────────────────────────

    def _draw_pigment_mill(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("PIGMENT MILL", True, _TITLE_C)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, _HINT_C)
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        if self._pigment_phase == "select_raw":
            self._draw_pigment_select_raw(player)
        elif self._pigment_phase == "select_grind":
            self._draw_pigment_select_grind(player)
        elif self._pigment_phase == "grinding":
            self._draw_pigment_grinding(player, dt)
        elif self._pigment_phase == "calcinate":
            self._draw_pigment_calcinate(player)
        elif self._pigment_phase == "result":
            self._draw_pigment_result(player)

    # ─── phase: select raw material ───────────────────────────────────────────

    def _draw_pigment_select_raw(self, player):
        self._pigment_raw_rects.clear()
        raw_slots = _raw_items_in_inventory(player)
        if not raw_slots:
            msg = self.font.render("No raw materials! Mine rocks, harvest crops, or collect earth deposits.", True, _LABEL_C)
            self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2))
            return

        sub = self.small.render("Select a raw material to grind:", True, _LABEL_C)
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 32))

        CELL_W, CELL_H, GAP, COLS = 220, 68, 10, 4
        gx0 = (SCREEN_W - (COLS * CELL_W + (COLS - 1) * GAP)) // 2
        for li, (item_key, qty) in enumerate(raw_slots[:16]):
            col_i, row_i = li % COLS, li // COLS
            rx = gx0 + col_i * (CELL_W + GAP)
            ry = 55 + row_i * (CELL_H + GAP)
            rect = pygame.Rect(rx, ry, CELL_W, CELL_H)
            self._pigment_raw_rects[item_key] = rect
            pygame.draw.rect(self.screen, _CELL_BG, rect)
            pygame.draw.rect(self.screen, _ACCENT, rect, 2)

            pig_key = RAW_TO_PIGMENT.get(item_key, item_key)
            pig_data = PIGMENT_TYPES.get(pig_key, {})
            base_rgb = pig_data.get("base_rgb", (160, 140, 180))

            # Color swatch strip on left
            swatch = pygame.Rect(rx + 4, ry + 4, 14, CELL_H - 8)
            pygame.draw.rect(self.screen, base_rgb, swatch)

            from items import ITEMS
            nm_str = ITEMS.get(item_key, {}).get("name", item_key.replace("_", " ").title())
            nm = self.small.render(nm_str, True, _TITLE_C)
            self.screen.blit(nm, (rx + 24, ry + 8))

            pig_nm = pig_data.get("display", pig_key.replace("_", " ").title())
            pn = self.small.render(f"→ {pig_nm}", True, _LABEL_C)
            self.screen.blit(pn, (rx + 24, ry + 26))

            fam = pig_data.get("family", "")
            fl = self.small.render(fam.title(), True, _DIM_C)
            self.screen.blit(fl, (rx + 24, ry + 44))

            qt = self.small.render(f"×{qty}", True, _HINT_C)
            self.screen.blit(qt, (rx + CELL_W - qt.get_width() - 8, ry + 8))

            # Calcination badge
            if pig_key in CALCINATION_MAP:
                badge = self.small.render("⟳ calc", True, _YELLOW)
                self.screen.blit(badge, (rx + CELL_W - badge.get_width() - 8, ry + 44))

    # ─── phase: select grind style ────────────────────────────────────────────

    def _draw_pigment_select_grind(self, player):
        self._pigment_grind_rects.clear()
        sub = self.small.render("Choose a grind style:", True, _LABEL_C)
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 32))

        pig_key = RAW_TO_PIGMENT.get(self._pigment_selected_raw, "")
        pig_data = PIGMENT_TYPES.get(pig_key, {})
        pig_nm = pig_data.get("display", pig_key.replace("_", " ").title())
        nm_lbl = self.font.render(pig_nm, True, tuple(pig_data.get("base_rgb", (180, 160, 210))))
        self.screen.blit(nm_lbl, (SCREEN_W // 2 - nm_lbl.get_width() // 2, 52))

        BTN_W, BTN_H, BTN_GAP = 240, 120, 16
        total_w = len(GRIND_STYLES) * BTN_W + (len(GRIND_STYLES) - 1) * BTN_GAP
        gx0 = (SCREEN_W - total_w) // 2
        for pi, (sk, sd) in enumerate(GRIND_STYLES.items()):
            px = gx0 + pi * (BTN_W + BTN_GAP)
            py = SCREEN_H // 2 - BTN_H // 2
            prect = pygame.Rect(px, py, BTN_W, BTN_H)
            self._pigment_grind_rects[sk] = prect
            pygame.draw.rect(self.screen, _CELL_BG, prect)
            pygame.draw.rect(self.screen, _ACCENT, prect, 2)
            lbl = self.font.render(sd["label"], True, _TITLE_C)
            self.screen.blit(lbl, (px + BTN_W // 2 - lbl.get_width() // 2, py + 12))

            # Modifiers
            for di, (attr, delta) in enumerate([
                ("Granularity", sd["granularity"]),
                ("Purity", sd.get("purity", 0.0)),
            ]):
                sign = "+" if delta >= 0 else ""
                col = _GREEN if delta > 0 else _RED if delta < 0 else _DIM_C
                dl = self.small.render(f"{attr}: {sign}{int(delta * 100)}%", True, col)
                self.screen.blit(dl, (px + BTN_W // 2 - dl.get_width() // 2, py + 50 + di * 20))

            mult = sd["grind_quality_mult"]
            ml = self.small.render(f"Skill mult: ×{mult:.2f}", True, _HINT_C)
            self.screen.blit(ml, (px + BTN_W // 2 - ml.get_width() // 2, py + 94))

        # Calcination option
        if pig_key in CALCINATION_MAP:
            calc_y = SCREEN_H // 2 + BTN_H // 2 + 30
            calc_rect = pygame.Rect(SCREEN_W // 2 - 140, calc_y, 280, 44)
            self._pigment_calc_rect = calc_rect
            pygame.draw.rect(self.screen, _CELL_BG, calc_rect)
            pygame.draw.rect(self.screen, _YELLOW, calc_rect, 2)
            out_key = CALCINATION_MAP[pig_key]
            out_nm = PIGMENT_TYPES.get(out_key, {}).get("display", out_key.replace("_", " ").title())
            cl = self.small.render(f"Calcinate → {out_nm} (no mini-game)", True, _YELLOW)
            self.screen.blit(cl, (SCREEN_W // 2 - cl.get_width() // 2, calc_y + 12))
        else:
            self._pigment_calc_rect = None

    # ─── phase: rhythm grinding mini-game ─────────────────────────────────────

    def _draw_pigment_grinding(self, player, dt):
        self._pigment_grind_pos = (self._pigment_grind_pos + dt * _GRIND_SPEED) % 1.0

        cx, cy = SCREEN_W // 2, SCREEN_H // 2

        pig_key = RAW_TO_PIGMENT.get(self._pigment_selected_raw, "")
        pig_data = PIGMENT_TYPES.get(pig_key, {})
        pig_nm = pig_data.get("display", pig_key.replace("_", " ").title())
        base_rgb = pig_data.get("base_rgb", (180, 160, 210))

        # Title
        nl = self.font.render(f"Grinding: {pig_nm}", True, tuple(base_rgb))
        self.screen.blit(nl, (cx - nl.get_width() // 2, 32))

        # Oscillator bar
        bar_w = 400
        bar_x = cx - bar_w // 2
        bar_y = cy - 60
        pygame.draw.rect(self.screen, _CELL_BG, (bar_x, bar_y, bar_w, 28))

        # Sweet zone (centre ±HIT_WINDOW)
        hz_w = int(bar_w * _HIT_WINDOW * 2)
        hz_x = cx - hz_w // 2
        pygame.draw.rect(self.screen, (60, 140, 70), (hz_x, bar_y, hz_w, 28))

        # Oscillating cursor
        osc = math.sin(self._pigment_grind_pos * 2 * math.pi)
        cursor_x = int(cx + osc * (bar_w // 2 - 8))
        pygame.draw.rect(self.screen, _TITLE_C, (cursor_x - 4, bar_y - 4, 8, 36))
        pygame.draw.rect(self.screen, _ACCENT, (bar_x, bar_y, bar_w, 28), 2)

        # Hit feedback (flash last hit quality)
        if self._pigment_last_hit is not None:
            flash_col = _GREEN if self._pigment_last_hit >= 0.7 else _YELLOW if self._pigment_last_hit >= 0.3 else _RED
            fl = self.font.render("GRIND!", True, flash_col)
            self.screen.blit(fl, (cx - fl.get_width() // 2, bar_y - 42))
            self._pigment_last_hit_timer -= dt
            if self._pigment_last_hit_timer <= 0:
                self._pigment_last_hit = None

        # Progress dots
        hits_done = len(self._pigment_grind_hits)
        for di in range(_GRIND_TOTAL):
            dx = cx - (_GRIND_TOTAL * 20) // 2 + di * 20 + 10
            col = _GREEN if di < hits_done else _DIM_C
            pygame.draw.circle(self.screen, col, (dx, cy + 20), 7)

        # Controls
        kl = self.small.render(f"Press SPACE when cursor is in the green zone  ({hits_done}/{_GRIND_TOTAL})", True, _HINT_C)
        self.screen.blit(kl, (cx - kl.get_width() // 2, cy + 50))

        style_nm = GRIND_STYLES.get(self._pigment_selected_grind, {}).get("label", "")
        sl = self.small.render(style_nm, True, _LABEL_C)
        self.screen.blit(sl, (cx - sl.get_width() // 2, cy + 72))

    # ─── phase: calcination (instant) ─────────────────────────────────────────

    def _draw_pigment_calcinate(self, player):
        cx = SCREEN_W // 2
        pig_key = RAW_TO_PIGMENT.get(self._pigment_selected_raw, "")
        out_key = CALCINATION_MAP.get(pig_key, pig_key)
        pig_nm = PIGMENT_TYPES.get(out_key, {}).get("display", out_key.replace("_", " ").title())
        base_rgb = PIGMENT_TYPES.get(out_key, {}).get("base_rgb", (180, 160, 210))

        msg = self.font.render("Calcination Complete!", True, _TITLE_C)
        self.screen.blit(msg, (cx - msg.get_width() // 2, SCREEN_H // 2 - 70))
        nm_l = self.font.render(pig_nm, True, tuple(base_rgb))
        self.screen.blit(nm_l, (cx - nm_l.get_width() // 2, SCREEN_H // 2 - 28))
        note = self.small.render("A refined pigment has been added to your inventory.", True, _LABEL_C)
        self.screen.blit(note, (cx - note.get_width() // 2, SCREEN_H // 2 + 14))
        ok = self.small.render("Click anywhere to continue", True, _DIM_C)
        self.screen.blit(ok, (cx - ok.get_width() // 2, SCREEN_H // 2 + 44))

    # ─── phase: result ────────────────────────────────────────────────────────

    def _draw_pigment_result(self, player):
        pig = self._pigment_result
        if pig is None:
            return
        cx = SCREEN_W // 2
        pig_data = PIGMENT_TYPES.get(pig.pigment_key, {})
        pig_nm = pig_data.get("display", pig.pigment_key.replace("_", " ").title())
        base_rgb = tuple(pig.color_rgb) if pig.color_rgb else (180, 160, 210)

        msg = self.font.render("Pigment Refined!", True, _TITLE_C)
        self.screen.blit(msg, (cx - msg.get_width() // 2, SCREEN_H // 2 - 110))

        # Color swatch
        swatch_rect = pygame.Rect(cx - 30, SCREEN_H // 2 - 80, 60, 40)
        pygame.draw.rect(self.screen, base_rgb, swatch_rect)
        pygame.draw.rect(self.screen, _ACCENT, swatch_rect, 2)

        nm_l = self.font.render(pig_nm, True, base_rgb)
        self.screen.blit(nm_l, (cx - nm_l.get_width() // 2, SCREEN_H // 2 - 30))

        q = pig.quality()
        q_col = _quality_color(q)
        ql = self.font.render(f"Quality: {int(q * 100)}%", True, q_col)
        self.screen.blit(ql, (cx - ql.get_width() // 2, SCREEN_H // 2 + 8))

        # Attribute breakdown
        attrs = [
            ("Purity",       pig.purity),
            ("Opacity",      pig.opacity),
            ("Stability",    pig.stability),
            ("Grind",        pig.grind_quality),
        ]
        for ai, (lbl, val) in enumerate(attrs):
            ax = cx - 160 + ai * 82
            ay = SCREEN_H // 2 + 40
            bar_h = int(val * 40)
            pygame.draw.rect(self.screen, _CELL_BG, (ax, ay, 14, 40))
            pygame.draw.rect(self.screen, _quality_color(val), (ax, ay + 40 - bar_h, 14, bar_h))
            ll = self.small.render(lbl, True, _DIM_C)
            self.screen.blit(ll, (ax + 7 - ll.get_width() // 2, ay + 44))

        if pig.notes:
            notes_str = ", ".join(pig.notes[:3])
            fn = self.small.render(notes_str, True, _HINT_C)
            self.screen.blit(fn, (cx - fn.get_width() // 2, SCREEN_H // 2 + 100))

        ok = self.small.render("Click anywhere to grind another", True, _DIM_C)
        self.screen.blit(ok, (cx - ok.get_width() // 2, SCREEN_H // 2 + 124))

    # ─── click handler ────────────────────────────────────────────────────────

    def _handle_pigment_mill_click(self, pos, player):
        if self._pigment_phase == "select_raw":
            for item_key, rect in self._pigment_raw_rects.items():
                if rect.collidepoint(pos):
                    self._pigment_selected_raw = item_key
                    self._pigment_phase = "select_grind"
                    self._pigment_calc_rect = None
                    return
        elif self._pigment_phase == "select_grind":
            if self._pigment_calc_rect and self._pigment_calc_rect.collidepoint(pos):
                self._do_pigment_calcinate(player)
                return
            for sk, rect in self._pigment_grind_rects.items():
                if rect.collidepoint(pos):
                    self._pigment_selected_grind = sk
                    self._pigment_phase = "grinding"
                    self._pigment_grind_pos = 0.0
                    self._pigment_grind_hits = []
                    self._pigment_last_hit = None
                    self._pigment_last_hit_timer = 0.0
                    return
        elif self._pigment_phase in ("result", "calcinate"):
            self._pigment_phase = "select_raw"
            self._pigment_result = None

    # ─── key handlers ─────────────────────────────────────────────────────────

    def handle_pigment_keydown(self, key, player):
        if key == pygame.K_ESCAPE:
            if self._pigment_phase in ("select_grind", "grinding"):
                self._pigment_phase = "select_raw"
                self._pigment_grind_hits = []
            elif self._pigment_phase in ("result", "calcinate"):
                self._pigment_phase = "select_raw"
                self._pigment_result = None
            else:
                self.refinery_open = False
        elif key == pygame.K_SPACE and self._pigment_phase == "grinding":
            self._do_grind_hit(player)

    def handle_pigment_keys(self, keys, dt, player):
        pass  # SPACE handled via keydown

    # ─── internal helpers ─────────────────────────────────────────────────────

    def _do_grind_hit(self, player):
        osc = math.sin(self._pigment_grind_pos * 2 * math.pi)
        accuracy = max(0.0, 1.0 - abs(osc) / _HIT_WINDOW) if abs(osc) <= _HIT_WINDOW else 0.0
        self._pigment_grind_hits.append(accuracy)
        self._pigment_last_hit = accuracy
        self._pigment_last_hit_timer = 0.8

        if len(self._pigment_grind_hits) >= _GRIND_TOTAL:
            self._finish_grinding(player)

    def _finish_grinding(self, player):
        raw_key = self._pigment_selected_raw
        pig_key = RAW_TO_PIGMENT.get(raw_key, raw_key)
        style = GRIND_STYLES.get(self._pigment_selected_grind, GRIND_STYLES["standard"])
        avg_acc = sum(self._pigment_grind_hits) / max(1, len(self._pigment_grind_hits))
        grind_quality = min(1.0, avg_acc * style["grind_quality_mult"])

        origin_biome = getattr(player.world, "get_biodome", lambda x: "unknown")(
            int(player.x // 16)
        )
        pig = player._pigment_gen.generate(pig_key, origin_biome)
        # Apply grind quality and style modifiers
        pig.grind_quality = round(grind_quality, 3)
        pig.purity = round(max(0.0, min(1.0, pig.purity + style.get("purity", 0.0))), 3)
        pig.granularity = round(max(0.0, min(1.0, pig.granularity + style.get("granularity", 0.0))), 3)
        pig.state = "ground"
        player.pigments.append(pig)
        player.discovered_pigments.add(pig_key)
        _consume_item(player, raw_key)
        player._add_item(f"pigment_{pig_key}")

        self._pigment_result = pig
        self._pigment_phase = "result"

    def _do_pigment_calcinate(self, player):
        raw_key = self._pigment_selected_raw
        pig_key = RAW_TO_PIGMENT.get(raw_key, raw_key)
        out_key = CALCINATION_MAP.get(pig_key, pig_key)

        origin_biome = getattr(player.world, "get_biodome", lambda x: "unknown")(
            int(player.x // 16)
        )
        # Generate a base pigment as the "source", then calcinate it
        source_pig = player._pigment_gen.generate(pig_key, origin_biome)
        pig = player._pigment_gen.generate_processed(source_pig, out_key)
        player.pigments.append(pig)
        player.discovered_pigments.add(out_key)
        _consume_item(player, raw_key)
        player._add_item(f"pigment_{out_key}")

        self._pigment_phase = "calcinate"
