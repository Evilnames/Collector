import math
import random
import pygame
from constants import SCREEN_W, SCREEN_H
from tea import (
    apply_wither, apply_oxidation, apply_aging, apply_herbal_blend, apply_roasting,
    get_brew_item_id, make_blend,
    WITHER_METHODS, WITHER_RACK_SLOTS,
    TEA_TYPE_DESCS, TEA_TYPE_COLORS, TEA_TYPE_BUFFS,
    BUFF_DESCS, BIOME_DISPLAY_NAMES, VARIETY_DISPLAY_NAMES,
    HERBAL_ADDITIVES, AGE_DURATIONS, ROASTING_LEVELS, _CODEX_BIOMES, _CODEX_TEA_TYPES,
)
from world import CYCLE_DURATION
from dataclasses import asdict


_ACCENT   = ( 65, 160,  75)
_DARK_BG  = ( 12,  28,  14)
_CELL_BG  = ( 18,  38,  20)
_TITLE_C  = (140, 215, 130)
_LABEL_C  = (100, 175,  90)
_DIM_C    = ( 55,  90,  50)
_HINT_C   = ( 80, 130,  70)


class TeaMixin:

    # ─────────────────────────────────────────────────────────────────────────
    # WITHERING RACK
    # ─────────────────────────────────────────────────────────────────────────

    def _draw_withering_rack(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("WITHERING RACK", True, _TITLE_C)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, _HINT_C)
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        slots = player.withering_rack_slots
        SLOT_W, SLOT_H = 160, 76
        GAP = 12
        total_w = WITHER_RACK_SLOTS * SLOT_W + (WITHER_RACK_SLOTS - 1) * GAP
        sx0 = (SCREEN_W - total_w) // 2
        sy0 = 34

        # ── Withering slots row ───────────────────────────────────────────
        self._wither_rack_slot_rects.clear()
        for i in range(WITHER_RACK_SLOTS):
            sx = sx0 + i * (SLOT_W + GAP)
            rect = pygame.Rect(sx, sy0, SLOT_W, SLOT_H)
            self._wither_rack_slot_rects[i] = rect

            slot = slots[i] if i < len(slots) else None
            if slot is None:
                pygame.draw.rect(self.screen, _DARK_BG, rect)
                pygame.draw.rect(self.screen, _DIM_C, rect, 1)
                es = self.small.render("Empty", True, _DIM_C)
                self.screen.blit(es, (rect.centerx - es.get_width() // 2,
                                      rect.centery - es.get_height() // 2))
            else:
                done = slot["elapsed"] >= slot["duration"]
                bg   = (14, 44, 18) if not done else (10, 52, 16)
                brd  = (100, 220, 80) if done else _ACCENT
                pygame.draw.rect(self.screen, bg, rect)
                pygame.draw.rect(self.screen, brd, rect, 2 if done else 1)

                ld   = slot["leaf_data"]
                biome_name = BIOME_DISPLAY_NAMES.get(ld["origin_biome"], ld["origin_biome"])
                var_name   = VARIETY_DISPLAY_NAMES.get(ld["variety"], ld["variety"])
                nm_s = self.small.render((biome_name + " " + var_name)[:22], True, _TITLE_C)
                self.screen.blit(nm_s, (rect.x + 5, rect.y + 4))
                wm_s = self.small.render(WITHER_METHODS[slot["method"]]["label"], True, _LABEL_C)
                self.screen.blit(wm_s, (rect.x + 5, rect.y + 20))

                if done:
                    ready_s = self.font.render("READY", True, (100, 255, 80))
                    self.screen.blit(ready_s, (rect.centerx - ready_s.get_width() // 2,
                                               rect.y + 46))
                else:
                    frac = slot["elapsed"] / slot["duration"]
                    bar_x, bar_y = rect.x + 5, rect.y + 56
                    bar_w = SLOT_W - 10
                    pygame.draw.rect(self.screen, (18, 42, 18), (bar_x, bar_y, bar_w, 8))
                    pygame.draw.rect(self.screen, _ACCENT, (bar_x, bar_y, int(bar_w * frac), 8))
                    days_left = (slot["duration"] - slot["elapsed"]) / CYCLE_DURATION
                    ts = self.small.render(f"{days_left:.1f}d", True, _HINT_C)
                    self.screen.blit(ts, (rect.x + 5, rect.y + 42))

        bottom_y  = sy0 + SLOT_H + 14
        leaf_col_w = (SCREEN_W - 20) * 2 // 3
        meth_col_x = leaf_col_w + 20
        meth_col_w = SCREEN_W - meth_col_x - 10

        # ── Bottom-left: raw leaves to place ─────────────────────────────
        pygame.draw.rect(self.screen, _DARK_BG, (8, bottom_y, leaf_col_w, SCREEN_H - bottom_y - 8))
        pygame.draw.rect(self.screen, _DIM_C,   (8, bottom_y, leaf_col_w, SCREEN_H - bottom_y - 8), 1)
        free_slots = sum(1 for i in range(WITHER_RACK_SLOTS)
                         if i >= len(slots) or slots[i] is None)
        hdr = self.small.render(
            f"RAW LEAVES — click to select  (free slots: {free_slots}/{WITHER_RACK_SLOTS})",
            True, _LABEL_C)
        self.screen.blit(hdr, (16, bottom_y + 5))

        self._wither_leaf_rects.clear()
        raw = [(i, x) for i, x in enumerate(player.tea_leaves) if x.state == "raw"]
        CELL_W, CELL_H, GAP2, COLS = 200, 52, 6, max(1, leaf_col_w // 207)
        gx0 = 16
        for li, (bi, leaf) in enumerate(raw[:20]):
            col_i = li % COLS
            row_i = li // COLS
            rx = gx0 + col_i * (CELL_W + GAP2)
            ry = bottom_y + 24 + row_i * (CELL_H + GAP2)
            if ry + CELL_H > SCREEN_H - 10:
                break
            rect = pygame.Rect(rx, ry, CELL_W, CELL_H)
            self._wither_leaf_rects[bi] = rect
            sel = (self._wither_pending_leaf_idx == bi)
            nm = BIOME_DISPLAY_NAMES.get(leaf.origin_biome, leaf.origin_biome)
            vr = VARIETY_DISPLAY_NAMES.get(leaf.variety, leaf.variety)
            pygame.draw.rect(self.screen, (30, 60, 30) if sel else _CELL_BG, rect)
            pygame.draw.rect(self.screen, (120, 220, 100) if sel else _ACCENT, rect,
                             2 if sel else 1)
            ns = self.small.render((nm + " " + vr)[:24], True, _TITLE_C)
            self.screen.blit(ns, (rx + 5, ry + 6))
            rs = self.small.render("Raw — click to select", True, _HINT_C)
            self.screen.blit(rs, (rx + 5, ry + 24))

        if not raw:
            msg = self.font.render("No raw tea leaves! Harvest ripe Tea Plants.", True, _DIM_C)
            self.screen.blit(msg, (16, bottom_y + 30))

        # ── Bottom-right: method picker (shown when leaf is selected) ─────
        pygame.draw.rect(self.screen, _DARK_BG, (meth_col_x, bottom_y, meth_col_w, SCREEN_H - bottom_y - 8))
        pygame.draw.rect(self.screen, _DIM_C,   (meth_col_x, bottom_y, meth_col_w, SCREEN_H - bottom_y - 8), 1)

        if self._wither_pending_leaf_idx is not None and free_slots > 0:
            mhdr = self.small.render("Choose method:", True, _LABEL_C)
            self.screen.blit(mhdr, (meth_col_x + 8, bottom_y + 5))
            self._wither_method_rects.clear()
            for mi, (wkey, wdata) in enumerate(WITHER_METHODS.items()):
                mrect = pygame.Rect(meth_col_x + 8, bottom_y + 24 + mi * 68,
                                    meth_col_w - 16, 60)
                self._wither_method_rects[wkey] = mrect
                pygame.draw.rect(self.screen, _CELL_BG, mrect)
                pygame.draw.rect(self.screen, _ACCENT, mrect, 2)
                lbl = self.font.render(wdata["label"], True, _TITLE_C)
                self.screen.blit(lbl, (mrect.x + 8, mrect.y + 4))
                desc = wdata["desc"].split(".")[0]
                ds   = self.small.render(desc[:36], True, _LABEL_C)
                self.screen.blit(ds, (mrect.x + 8, mrect.y + 24))
                dur_s = self.small.render(f"{wdata['days']}d", True, _HINT_C)
                self.screen.blit(dur_s, (mrect.x + 8, mrect.y + 42))
        elif free_slots == 0:
            full_s = self.small.render("All slots in use.", True, _DIM_C)
            self.screen.blit(full_s, (meth_col_x + 8, bottom_y + 30))
        else:
            sel_s = self.small.render("Select a leaf first.", True, _DIM_C)
            self.screen.blit(sel_s, (meth_col_x + 8, bottom_y + 30))

    def _handle_withering_rack_click(self, pos, player):
        from tea import TeaLeaf, WITHER_RACK_SLOTS
        slots = player.withering_rack_slots

        # Collect from ready slots
        for i, rect in self._wither_rack_slot_rects.items():
            if rect.collidepoint(pos):
                if i < len(slots) and slots[i] is not None:
                    slot = slots[i]
                    if slot["elapsed"] >= slot["duration"]:
                        leaf = TeaLeaf(**slot["leaf_data"])
                        apply_wither(leaf, slot["method"])
                        player.tea_leaves.append(leaf)
                        slots[i] = None
                        while slots and slots[-1] is None:
                            slots.pop()
                return

        # Select a raw leaf
        for bi, rect in self._wither_leaf_rects.items():
            if rect.collidepoint(pos):
                self._wither_pending_leaf_idx = bi
                self._wither_method_rects.clear()
                return

        # Choose method for selected leaf
        if self._wither_pending_leaf_idx is not None:
            free_slots = sum(1 for i in range(WITHER_RACK_SLOTS)
                             if i >= len(slots) or slots[i] is None)
            if free_slots == 0:
                return
            for wkey, rect in self._wither_method_rects.items():
                if rect.collidepoint(pos):
                    bi = self._wither_pending_leaf_idx
                    if bi >= len(player.tea_leaves) or player.tea_leaves[bi].state != "raw":
                        self._wither_pending_leaf_idx = None
                        return
                    leaf = player.tea_leaves.pop(bi)
                    # Find first free slot
                    free_idx = next(
                        (i for i in range(WITHER_RACK_SLOTS)
                         if i >= len(slots) or slots[i] is None),
                        None)
                    if free_idx is None:
                        player.tea_leaves.insert(bi, leaf)
                        return
                    while len(slots) <= free_idx:
                        slots.append(None)
                    slots[free_idx] = {
                        "leaf_data": asdict(leaf),
                        "method":   wkey,
                        "elapsed":  0.0,
                        "duration": WITHER_METHODS[wkey]["days"] * CYCLE_DURATION,
                    }
                    self._wither_pending_leaf_idx = None
                    return

    # ─────────────────────────────────────────────────────────────────────────
    # OXIDATION STATION
    # ─────────────────────────────────────────────────────────────────────────

    _OX_ZONES = [
        ("white",  0.00, 0.08,  (205, 200, 180), "White"),
        ("yellow", 0.08, 0.18,  (190, 170,  70), "Yellow"),
        ("green",  0.18, 0.28,  ( 50, 140,  50), "Green"),
        ("oolong", 0.28, 0.75,  (160, 130,  40), "Oolong"),
        ("black",  0.75, 0.93,  ( 55,  25,  10), "Black"),
        ("puerh",  0.93, 1.00,  ( 35,  20,   8), "Pu-erh"),
    ]
    _RITUAL_NAMES = {
        "white":  "Withering Fan",
        "yellow": "Swaddling Rhythm",
        "green":  "Sha Qing Pan",
        "oolong": "Rolling Table",
        "black":  "CTC Rolling Press",
        "puerh":  "Wo Dui Pile",
    }
    _RITUAL_INSTRUCTIONS = {
        "white":  "Hover over the warm air pocket. Avoid the blue dew pools.",
        "yellow": "Click anywhere to wrap/unwrap — match the metronome rhythm.",
        "green":  "Hold and drag in circles to stir the leaves. Don't stop!",
        "oolong": "Trace circles during ROLL. Hold perfectly still during REST.",
        "black":  "Hold and drag over cells to crush them, then click STOP at the right moment.",
        "puerh":  "Keep the crosshair inside the glowing fermentation zone.",
    }

    def _draw_oxidation_station(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("OXIDATION STATION", True, _TITLE_C)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, _HINT_C)
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        if self._oxidation_phase == "select_leaf":
            self._draw_ox_select_leaf(player)
        elif self._oxidation_phase == "select_zone":
            self._draw_ox_select_zone()
        elif self._oxidation_phase == "ritual":
            self._draw_ox_ritual(player, dt)
        elif self._oxidation_phase == "result":
            self._draw_ox_result(player)

    # ── leaf selection ────────────────────────────────────────────────────────

    def _draw_ox_select_leaf(self, player):
        self._oxidation_select_rects.clear()
        withered = [(i, x) for i, x in enumerate(player.tea_leaves) if x.state == "withered"]
        if not withered:
            msg = self.font.render("No withered leaves! Use the Withering Rack first.", True, _LABEL_C)
            self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2))
            return
        sub = self.small.render("Select a withered leaf to oxidize:", True, _LABEL_C)
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 32))
        CELL_W, CELL_H, GAP, COLS = 200, 56, 8, 5
        gx0 = (SCREEN_W - (COLS * CELL_W + (COLS - 1) * GAP)) // 2
        for li, (bi, leaf) in enumerate(withered[:20]):
            col_i, row_i = li % COLS, li // COLS
            rx = gx0 + col_i * (CELL_W + GAP)
            ry = 55 + row_i * (CELL_H + GAP)
            rect = pygame.Rect(rx, ry, CELL_W, CELL_H)
            self._oxidation_select_rects[bi] = rect
            pygame.draw.rect(self.screen, _CELL_BG, rect)
            pygame.draw.rect(self.screen, _ACCENT, rect, 2)
            nm = BIOME_DISPLAY_NAMES.get(leaf.origin_biome, leaf.origin_biome)
            wm = WITHER_METHODS.get(leaf.wither_method, {}).get("label", leaf.wither_method)
            ns = self.small.render(nm + " — " + wm, True, _TITLE_C)
            self.screen.blit(ns, (rx + 6, ry + 8))
            h2 = self.small.render("Click to oxidize", True, _HINT_C)
            self.screen.blit(h2, (rx + 6, ry + 26))

    # ── zone selection ────────────────────────────────────────────────────────

    def _draw_ox_select_zone(self):
        sub = self.font.render("What tea are you making?", True, _TITLE_C)
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 32))
        self._ox_zone_btn_rects.clear()
        BTN_W, BTN_H, GAP = 180, 130, 16
        total_w = 3 * BTN_W + 2 * GAP
        gx0 = (SCREEN_W - total_w) // 2
        zone_descs = {
            "white":  "Barely touched.\nDelicate, floral.",
            "yellow": "Gently swaddled.\nMellow, smooth.",
            "green":  "Pan-fired to stop\noxidation. Fresh.",
            "oolong": "Rolled & rested.\nComplex, floral.",
            "black":  "Fully rolled &\noxidized. Bold.",
            "puerh":  "Pile-fermented.\nEarthy, deep.",
        }
        for i, (key, lo, hi, col, label) in enumerate(self._OX_ZONES):
            row, col_i = divmod(i, 3)
            rx = gx0 + col_i * (BTN_W + GAP)
            ry = 80 + row * (BTN_H + GAP)
            rect = pygame.Rect(rx, ry, BTN_W, BTN_H)
            self._ox_zone_btn_rects[key] = rect
            pygame.draw.rect(self.screen, _CELL_BG, rect)
            pygame.draw.rect(self.screen, col, rect, 3)
            lbl = self.font.render(label, True, col)
            self.screen.blit(lbl, (rect.centerx - lbl.get_width() // 2, ry + 8))
            ritual_lbl = self.small.render(self._RITUAL_NAMES[key], True, _LABEL_C)
            self.screen.blit(ritual_lbl, (rect.centerx - ritual_lbl.get_width() // 2, ry + 32))
            ox_lbl = self.small.render(f"{lo:.0%}–{hi:.0%} oxidation", True, _HINT_C)
            self.screen.blit(ox_lbl, (rect.centerx - ox_lbl.get_width() // 2, ry + 50))
            for di, dl in enumerate(zone_descs[key].split("\n")):
                ds = self.small.render(dl, True, _DIM_C)
                self.screen.blit(ds, (rect.centerx - ds.get_width() // 2, ry + 74 + di * 16))

    # ── ritual frame ──────────────────────────────────────────────────────────

    def _draw_ox_ritual(self, player, dt):
        self._oxidation_time = min(self._oxidation_total_time, self._oxidation_time + dt)

        # Zone bar (horizontal) just below title
        self._draw_ox_zone_bar()

        zone = self._ox_target_zone
        RITUAL_TOP = 56
        if zone == "white":
            self._update_draw_white(dt, RITUAL_TOP)
        elif zone == "yellow":
            self._update_draw_yellow(dt, RITUAL_TOP)
        elif zone == "green":
            self._update_draw_green(dt, RITUAL_TOP)
        elif zone == "oolong":
            self._update_draw_oolong(dt, RITUAL_TOP)
        elif zone == "black":
            self._update_draw_black(dt, RITUAL_TOP)
        elif zone == "puerh":
            self._update_draw_puerh(dt, RITUAL_TOP)

        if self._oxidation_time >= self._oxidation_total_time:
            self._finish_oxidation(player)
            return

        # HUD: ritual name, instruction, quality stars, time bar, lock button
        ritual_name = self._RITUAL_NAMES.get(zone, "")
        rn = self.small.render(ritual_name.upper(), True, _LABEL_C)
        self.screen.blit(rn, (SCREEN_W // 2 - rn.get_width() // 2, 28))

        HUD_Y = SCREEN_H - 90
        inst = self.small.render(self._RITUAL_INSTRUCTIONS.get(zone, ""), True, _HINT_C)
        self.screen.blit(inst, (SCREEN_W // 2 - inst.get_width() // 2, HUD_Y - 36))

        qs = self._render_stars(self.small, self._ox_ritual_quality)
        self.screen.blit(qs, (20, HUD_Y - 18))

        time_left = self._oxidation_total_time - self._oxidation_time
        ts = self.small.render(f"{time_left:.1f}s", True, _LABEL_C)
        self.screen.blit(ts, (20, HUD_Y))

        TIME_W = SCREEN_W - 200
        pygame.draw.rect(self.screen, _DARK_BG, (20, HUD_Y + 18, TIME_W, 12))
        prog = 1.0 - self._oxidation_time / self._oxidation_total_time
        pygame.draw.rect(self.screen, _ACCENT, (20, HUD_Y + 18, int(TIME_W * prog), 12))

        lock_rect = pygame.Rect(SCREEN_W - 150, HUD_Y, 130, 34)
        pygame.draw.rect(self.screen, (30, 80, 35), lock_rect)
        pygame.draw.rect(self.screen, _ACCENT, lock_rect, 2)
        ll = self.font.render("FINISH", True, _TITLE_C)
        self.screen.blit(ll, (lock_rect.centerx - ll.get_width() // 2,
                               lock_rect.centery - ll.get_height() // 2))
        self._oxidation_lock_btn = lock_rect

    def _draw_ox_zone_bar(self):
        BAR_X, BAR_Y, BAR_W, BAR_H = 20, 28, SCREEN_W - 40, 20
        pygame.draw.rect(self.screen, _DARK_BG, (BAR_X, BAR_Y, BAR_W, BAR_H))
        for key, lo, hi, col, label in self._OX_ZONES:
            seg_x = BAR_X + int(BAR_W * lo)
            seg_w = max(1, int(BAR_W * (hi - lo)))
            pygame.draw.rect(self.screen, col, (seg_x, BAR_Y, seg_w, BAR_H))
            ls = self.small.render(label, True, (200, 200, 200))
            if seg_w > ls.get_width() + 4:
                self.screen.blit(ls, (seg_x + seg_w // 2 - ls.get_width() // 2,
                                      BAR_Y + BAR_H // 2 - ls.get_height() // 2))
        pygame.draw.rect(self.screen, _DIM_C, (BAR_X, BAR_Y, BAR_W, BAR_H), 1)
        # Cursor dot
        cx = BAR_X + int(BAR_W * self._oxidation_level)
        pygame.draw.polygon(self.screen, (255, 255, 80),
                             [(cx, BAR_Y + BAR_H + 6), (cx - 5, BAR_Y + BAR_H),
                              (cx + 5, BAR_Y + BAR_H)])

    # ── result screen ─────────────────────────────────────────────────────────

    def _draw_ox_result(self, player):
        leaf = player.tea_leaves[self._oxidation_leaf_idx]
        tea_col = TEA_TYPE_COLORS.get(leaf.tea_type, _ACCENT)
        cx, cy = SCREEN_W // 2, 80
        pygame.draw.circle(self.screen, tea_col, (cx, cy + 40), 36)
        pygame.draw.circle(self.screen,
                           (min(255, tea_col[0] + 40), min(255, tea_col[1] + 40),
                            min(255, tea_col[2] + 40)), (cx, cy + 40), 36, 3)
        iy = cy + 95
        def rline(txt, col=_TITLE_C):
            nonlocal iy
            s = self.font.render(txt, True, col)
            self.screen.blit(s, (cx - s.get_width() // 2, iy))
            iy += 28
        rline(BIOME_DISPLAY_NAMES.get(leaf.origin_biome, leaf.origin_biome) + " " +
              VARIETY_DISPLAY_NAMES.get(leaf.variety, leaf.variety))
        rline(TEA_TYPE_DESCS.get(leaf.tea_type, leaf.tea_type), tea_col)
        ss = self._render_stars(self.font, leaf.steep_quality)
        self.screen.blit(ss, (cx - ss.get_width() // 2, iy))
        iy += 28
        rline(f"Oxidation: {leaf.oxidation:.0%}", _LABEL_C)
        if leaf.flavor_notes:
            rline("Flavour Notes:", (160, 200, 130))
            for note in leaf.flavor_notes:
                rline(f"  • {note.title()}", _TITLE_C)
        done_rect = pygame.Rect(cx - 70, iy + 20, 140, 34)
        pygame.draw.rect(self.screen, _DARK_BG, done_rect)
        pygame.draw.rect(self.screen, _ACCENT, done_rect, 2)
        dl = self.font.render("DONE", True, _TITLE_C)
        self.screen.blit(dl, (done_rect.centerx - dl.get_width() // 2,
                               done_rect.centery - dl.get_height() // 2))
        self._oxidation_result_btn = done_rect

    # ── ritual: WHITE — Withering Fan ─────────────────────────────────────────

    def _update_draw_white(self, dt, top_y):
        CX, CY = SCREEN_W // 2, top_y + 170
        TW, TH = 500, 200

        # Update air pocket (sine path)
        self._white_pocket_angle += dt * 0.6
        px = CX + int(math.cos(self._white_pocket_angle) * (TW // 2 - 40))
        py = CY + int(math.sin(self._white_pocket_angle * 0.7) * (TH // 2 - 20))

        # Update dew pools
        self._white_dew_timer += dt
        if self._white_dew_timer >= self._white_dew_next and len(self._white_dew_pools) < 3:
            margin = 40
            dpx = random.randint(CX - TW // 2 + margin, CX + TW // 2 - margin)
            dpy = random.randint(CY - TH // 2 + margin, CY + TH // 2 - margin)
            self._white_dew_pools.append({"pos": (dpx, dpy), "timer": 0.0, "hit": False})
            self._white_dew_timer = 0.0
            self._white_dew_next  = random.uniform(4.0, 8.0)
        for pool in self._white_dew_pools:
            pool["timer"] += dt
        self._white_dew_pools = [p for p in self._white_dew_pools if p["timer"] < 3.5]

        # Mouse interaction
        mx, my = self._ox_mouse_pos
        pocket_dist = math.hypot(mx - px, my - py)
        in_pocket = pocket_dist < 55
        if in_pocket:
            self._white_warmth_score = min(1.0, self._white_warmth_score + dt * 0.07)
        else:
            self._white_warmth_score = max(0.0, self._white_warmth_score - dt * 0.015)

        dew_hits = 0
        for pool in self._white_dew_pools:
            d = math.hypot(mx - pool["pos"][0], my - pool["pos"][1])
            if d < 22:
                pool["hit"] = True
                dew_hits += 1

        if dew_hits > 0:
            self._oxidation_level = min(0.08, self._oxidation_level + 0.003 * dt * dew_hits * 60)
        else:
            self._oxidation_level += 0.0001 * dt * 60
        self._oxidation_level = max(0.0, min(0.08, self._oxidation_level))

        dew_hit_count = sum(1 for p in self._white_dew_pools if p["hit"])
        dew_penalty = min(0.8, dew_hit_count * 0.25)
        self._ox_ritual_quality = self._white_warmth_score * max(0.0, 1.0 - dew_penalty)

        # Draw tray
        tray_rect = pygame.Rect(CX - TW // 2, CY - TH // 2, TW, TH)
        pygame.draw.rect(self.screen, (50, 40, 25), tray_rect)
        pygame.draw.rect(self.screen, (90, 75, 50), tray_rect, 2)
        # Leaf dots
        for seed in range(20):
            lx = CX - TW // 2 + 20 + (seed * 47 % (TW - 40))
            ly = CY - TH // 2 + 15 + (seed * 31 % (TH - 30))
            g = int(120 + self._oxidation_level * 200)
            pygame.draw.circle(self.screen, (60, g, 40), (lx, ly), 5)
        # Air pocket
        pocket_alpha = int(40 + 30 * math.sin(self._white_pocket_angle * 3))
        pygame.draw.ellipse(self.screen, (200, 200, 180),
                            (px - 55, py - 35, 110, 70), 2)
        if in_pocket:
            pygame.draw.ellipse(self.screen, (220, 220, 190),
                                (px - 55, py - 35, 110, 70))
        air_lbl = self.small.render("warm air", True, (160, 160, 130))
        self.screen.blit(air_lbl, (px - air_lbl.get_width() // 2, py - 10))
        # Dew pools
        for pool in self._white_dew_pools:
            dpx, dpy = pool["pos"]
            fade = max(0, 1.0 - pool["timer"] / 3.5)
            col = (80, 120, 200) if not pool["hit"] else (200, 80, 80)
            pygame.draw.circle(self.screen, col, (dpx, dpy), 22, 2)
            dl = self.small.render("dew", True, col)
            self.screen.blit(dl, (dpx - dl.get_width() // 2, dpy - 7))
        # Warmth bar
        ws = self.small.render("Warmth:", True, _LABEL_C)
        self.screen.blit(ws, (CX - TW // 2, CY + TH // 2 + 14))
        pygame.draw.rect(self.screen, _DARK_BG, (CX - TW // 2 + 65, CY + TH // 2 + 14, 200, 12))
        pygame.draw.rect(self.screen, (220, 200, 100),
                         (CX - TW // 2 + 65, CY + TH // 2 + 14, int(200 * self._white_warmth_score), 12))

    # ── ritual: YELLOW — Swaddling Rhythm ─────────────────────────────────────

    def _update_draw_yellow(self, dt, top_y):
        CX, CY = SCREEN_W // 2, top_y + 190
        IDEAL_PERIOD = 3.0

        # Metronome: bounces 0→1→0 with period IDEAL_PERIOD
        metronome_phase = (self._oxidation_time % IDEAL_PERIOD) / IDEAL_PERIOD
        metro_x = CX - 120 + int(240 * metronome_phase)

        # Heat arc logic
        if self._yellow_wrapped:
            self._yellow_heat_arc = min(1.0, self._yellow_heat_arc + dt * 0.18)
        else:
            self._yellow_heat_arc = max(0.0, self._yellow_heat_arc - dt * 0.12)
        self._yellow_wrap_time += dt

        # Oxidation
        if self._yellow_wrapped:
            overflow = max(0.0, self._yellow_heat_arc - 0.85)
            ox_rate = 0.0025 + overflow * 0.025
            self._oxidation_level = min(0.18, self._oxidation_level + ox_rate * dt * 60)
        else:
            self._oxidation_level = max(0.08, self._oxidation_level + 0.0001 * dt * 60)

        # Rhythm quality from interval log
        if self._yellow_interval_log:
            scores = [max(0.0, 1.0 - abs(iv - IDEAL_PERIOD) / IDEAL_PERIOD)
                      for iv in self._yellow_interval_log[-8:]]
            self._yellow_rhythm_score = sum(scores) / len(scores)
        overflow_fraction = min(1.0, sum(1 for iv in self._yellow_interval_log[-8:]
                                         if iv > IDEAL_PERIOD * 2.0) / max(1, len(self._yellow_interval_log[-8:])))
        self._ox_ritual_quality = self._yellow_rhythm_score * (1.0 - overflow_fraction * 0.5)

        # Draw bundle
        bundle_r = 38 + (4 if self._yellow_wrapped else 0)
        bundle_col = (210, 185, 100) if self._yellow_wrapped else (180, 160, 80)
        pygame.draw.circle(self.screen, bundle_col, (CX, CY), bundle_r)
        pygame.draw.circle(self.screen, (230, 210, 130), (CX, CY), bundle_r, 3)
        state_lbl = self.font.render("WRAPPED" if self._yellow_wrapped else "UNWRAPPED",
                                     True, (220, 200, 100))
        self.screen.blit(state_lbl, (CX - state_lbl.get_width() // 2, CY - 10))

        # Steam particles when wrapped
        if self._yellow_wrapped:
            for i in range(4):
                sx = CX + random.randint(-20, 20)
                sy = CY - bundle_r - random.randint(5, 25)
                pygame.draw.line(self.screen, (200, 200, 200), (sx, sy), (sx + 2, sy - 8), 1)

        # Heat arc
        arc_r = bundle_r + 18
        arc_col = (255, 160, 40) if self._yellow_heat_arc > 0.85 else (200, 130, 40)
        pygame.draw.arc(self.screen, arc_col,
                        (CX - arc_r, CY - arc_r, arc_r * 2, arc_r * 2),
                        0, self._yellow_heat_arc * math.pi * 2, 8)
        heat_lbl = self.small.render(f"Heat: {self._yellow_heat_arc:.0%}", True, arc_col)
        self.screen.blit(heat_lbl, (CX - heat_lbl.get_width() // 2, CY + arc_r + 6))
        if self._yellow_heat_arc > 0.85:
            ovf = self.small.render("TOO HOT!", True, (255, 80, 40))
            self.screen.blit(ovf, (CX - ovf.get_width() // 2, CY - arc_r - 20))

        # Metronome
        pygame.draw.line(self.screen, _DIM_C, (CX - 120, CY + 90), (CX + 120, CY + 90), 2)
        wrap_lbl = self.small.render("WRAP", True, _LABEL_C)
        unwrap_lbl = self.small.render("UNWRAP", True, _LABEL_C)
        self.screen.blit(wrap_lbl, (CX - 120, CY + 76))
        self.screen.blit(unwrap_lbl, (CX + 120 - unwrap_lbl.get_width(), CY + 76))
        pygame.draw.circle(self.screen, (220, 200, 80), (metro_x, CY + 90), 7)

        # Interval log bar
        log_y = CY + 108
        log_lbl = self.small.render("Rhythm:", True, _LABEL_C)
        self.screen.blit(log_lbl, (CX - 160, log_y))
        for bi, iv in enumerate(self._yellow_interval_log[-8:]):
            score = max(0.0, 1.0 - abs(iv - IDEAL_PERIOD) / IDEAL_PERIOD)
            col = (int(200 * (1 - score)), int(180 * score), 40)
            pygame.draw.rect(self.screen, col, (CX - 100 + bi * 26, log_y, 22, 14))

        click_hint = self.small.render("Click to wrap / unwrap", True, _HINT_C)
        self.screen.blit(click_hint, (CX - click_hint.get_width() // 2, CY + 130))

    # ── ritual: GREEN — Sha Qing Pan ──────────────────────────────────────────

    def _update_draw_green(self, dt, top_y):
        CX, CY = SCREEN_W // 2, top_y + 210
        WOK_R = 130

        mx, my = self._ox_mouse_pos
        in_wok = math.hypot(mx - CX, my - CY) < WOK_R - 10

        # Velocity tracking
        if self._green_drag_last is not None and self._ox_mouse_down and in_wok:
            ddx = mx - self._green_drag_last[0]
            ddy = my - self._green_drag_last[1]
            speed = math.hypot(ddx, ddy) / max(dt, 0.001)
            self._green_drag_vel = min(600.0, speed)
            self._green_still_timer = 0.0
            if speed > 30:
                angle = math.atan2(my - CY, mx - CX)
                sector = int((angle + math.pi) / (math.pi / 4)) % 8
                self._green_sectors[sector] = min(1.0, self._green_sectors[sector] + dt * 1.5)
        else:
            self._green_drag_vel = max(0.0, self._green_drag_vel - 300 * dt)
            self._green_still_timer += dt

        self._green_drag_last = (mx, my)

        # Decay sector heat slowly
        for i in range(8):
            self._green_sectors[i] = max(0.0, self._green_sectors[i] - dt * 0.08)

        # Enzyme activity: drops when dragging fast, recovers when still
        if self._green_drag_vel > 80 and in_wok and self._ox_mouse_down:
            self._green_enzyme = max(0.0, self._green_enzyme - dt * 0.9)
        else:
            self._green_enzyme = min(1.0, self._green_enzyme + dt * 0.35)

        # Oxidation rises with enzyme activity
        self._oxidation_level = min(0.28, self._oxidation_level + self._green_enzyme * 0.003 * dt * 60)
        self._oxidation_level = max(0.18, self._oxidation_level)

        mean_heat = sum(self._green_sectors) / 8.0
        self._ox_ritual_quality = mean_heat * (1.0 - self._green_enzyme)

        # Draw wok
        pygame.draw.circle(self.screen, (35, 30, 25), (CX, CY), WOK_R)
        pygame.draw.circle(self.screen, (80, 65, 50), (CX, CY), WOK_R, 4)

        # Sector arcs
        for i in range(8):
            angle_start = i * math.pi / 4 - math.pi
            angle_end   = angle_start + math.pi / 4
            heat = self._green_sectors[i]
            arc_col = (int(20 + heat * 200), int(60 + heat * 120), int(10 + heat * 20))
            inner_r, outer_r = 30, WOK_R - 8
            arc_rect = (CX - outer_r, CY - outer_r, outer_r * 2, outer_r * 2)
            if heat > 0.05:
                pygame.draw.arc(self.screen, arc_col, arc_rect,
                                angle_start, angle_end, outer_r - inner_r)

        # Leaf dots inside wok
        for seed in range(25):
            ang = seed * 2.5
            r = 20 + (seed * 37 % 90)
            lx = CX + int(math.cos(ang) * r)
            ly = CY + int(math.sin(ang) * r)
            g = max(60, int(180 - self._green_enzyme * 120))
            pygame.draw.circle(self.screen, (50, g, 30), (lx, ly), 4)

        # Enzyme bar
        ebar_y = CY + WOK_R + 14
        el = self.small.render("Enzyme Activity:", True, _LABEL_C)
        self.screen.blit(el, (CX - 180, ebar_y))
        ebar_col = (int(self._green_enzyme * 220), int((1 - self._green_enzyme) * 200), 30)
        pygame.draw.rect(self.screen, _DARK_BG, (CX - 5, ebar_y, 180, 12))
        pygame.draw.rect(self.screen, ebar_col,
                         (CX - 5, ebar_y, int(180 * self._green_enzyme), 12))
        if self._green_still_timer > 0.8:
            stop_lbl = self.font.render("STIRRING STOPPED!", True, (255, 80, 40))
            self.screen.blit(stop_lbl, (CX - stop_lbl.get_width() // 2, CY - WOK_R - 28))

        drag_hint = self.small.render("Hold mouse button & drag inside the wok", True, _HINT_C)
        self.screen.blit(drag_hint, (CX - drag_hint.get_width() // 2, ebar_y + 20))

    # ── ritual: OOLONG — Rolling Table ────────────────────────────────────────

    def _update_draw_oolong(self, dt, top_y):
        CX, CY = SCREEN_W // 2, top_y + 200
        GUIDE_R = 80

        self._oolong_sub_timer += dt
        durations = {"roll_1": 9.0, "rest_1": 5.0, "roll_2": 9.0, "rest_2": 2.0}
        cur_dur = durations.get(self._oolong_sub, 9.0)

        # Phase transitions
        phase_order = ["roll_1", "rest_1", "roll_2", "rest_2"]
        if self._oolong_sub_timer >= cur_dur:
            idx = phase_order.index(self._oolong_sub)
            if idx + 1 < len(phase_order):
                # Save score for completed phase
                if self._oolong_sub == "roll_1":
                    self._oolong_roll1_score = min(1.0, self._oolong_angle_accum / (math.pi * 8))
                    self._oxidation_level = min(0.52, self._oxidation_level + 0.10)
                elif self._oolong_sub == "rest_1":
                    self._oolong_rest1_score = self._oolong_rest_score_current()
                elif self._oolong_sub == "roll_2":
                    self._oolong_roll2_score = min(1.0, self._oolong_angle_accum / (math.pi * 8))
                    self._oxidation_level = min(0.74, self._oxidation_level + 0.10)
                elif self._oolong_sub == "rest_2":
                    self._oolong_rest2_score = self._oolong_rest_score_current()
                self._oolong_sub = phase_order[idx + 1]
                self._oolong_sub_timer = 0.0
                self._oolong_angle_accum = 0.0
                self._oolong_prev_angle = None
                self._oolong_trail.clear()
                if self._oolong_sub in ("rest_1", "rest_2"):
                    self._oolong_rest_start_pos = self._ox_mouse_pos

        is_roll = self._oolong_sub in ("roll_1", "roll_2")
        is_rest = self._oolong_sub in ("rest_1", "rest_2")

        mx, my = self._ox_mouse_pos

        if is_roll and self._ox_mouse_down:
            # Track circular motion by accumulating angle change
            dx, dy = mx - CX, my - CY
            if math.hypot(dx, dy) > 15:
                angle = math.atan2(dy, dx)
                if self._oolong_prev_angle is not None:
                    delta = angle - self._oolong_prev_angle
                    if delta > math.pi:
                        delta -= 2 * math.pi
                    elif delta < -math.pi:
                        delta += 2 * math.pi
                    self._oolong_angle_accum += abs(delta)
                self._oolong_prev_angle = angle
                self._oolong_trail.append((mx, my))
                if len(self._oolong_trail) > 40:
                    self._oolong_trail.pop(0)

        # Quality
        r1 = self._oolong_roll1_score
        r2 = self._oolong_roll2_score if self._oolong_sub not in ("roll_1", "rest_1") \
             else min(1.0, self._oolong_angle_accum / (math.pi * 8))
        rs1 = self._oolong_rest1_score
        rs2 = self._oolong_rest2_score if self._oolong_sub == "rest_2" \
              else self._oolong_rest_score_current()
        self._ox_ritual_quality = (r1 + r2) / 2 * (rs1 + rs2) / 2

        # Draw bundle
        pygame.draw.circle(self.screen, (80, 65, 40), (CX, CY), 36)
        pygame.draw.circle(self.screen, (120, 95, 55), (CX, CY), 36, 3)
        if is_roll:
            pygame.draw.circle(self.screen, _DIM_C, (CX, CY), GUIDE_R, 1)
        # Trail
        if len(self._oolong_trail) > 1:
            for ti in range(1, len(self._oolong_trail)):
                alpha = ti / len(self._oolong_trail)
                col = (int(80 * alpha), int(160 * alpha), int(80 * alpha))
                pygame.draw.line(self.screen, col,
                                 self._oolong_trail[ti - 1], self._oolong_trail[ti], 2)

        # Phase label + progress
        phase_names = {
            "roll_1": "ROLL  (1/2)", "rest_1": "REST  (1/2)",
            "roll_2": "ROLL  (2/2)", "rest_2": "REST  (2/2)",
        }
        phase_col = (100, 200, 100) if is_roll else (200, 180, 80)
        pl = self.font.render(phase_names.get(self._oolong_sub, ""), True, phase_col)
        self.screen.blit(pl, (CX - pl.get_width() // 2, top_y + 80))
        frac = self._oolong_sub_timer / cur_dur
        pygame.draw.rect(self.screen, _DARK_BG, (CX - 150, top_y + 104, 300, 8))
        pygame.draw.rect(self.screen, phase_col, (CX - 150, top_y + 104, int(300 * frac), 8))

        if is_roll:
            loops_done = self._oolong_angle_accum / (math.pi * 2)
            ll = self.small.render(f"Loops: {loops_done:.1f}", True, _LABEL_C)
            self.screen.blit(ll, (CX - ll.get_width() // 2, CY + 50))
            drag_hint = self.small.render("Hold mouse & trace circles", True, _HINT_C)
            self.screen.blit(drag_hint, (CX - drag_hint.get_width() // 2, CY + 70))
        else:
            still_score = self._oolong_rest_score_current()
            sl = self.small.render(f"Stillness: {still_score:.0%}", True, _LABEL_C)
            self.screen.blit(sl, (CX - sl.get_width() // 2, CY + 50))
            pygame.draw.circle(self.screen, (80, 140, 80), (CX, CY), 28, 2)
            rest_hint = self.small.render("Hold the mouse still", True, _HINT_C)
            self.screen.blit(rest_hint, (CX - rest_hint.get_width() // 2, CY + 70))

    def _oolong_rest_score_current(self):
        if self._oolong_rest_start_pos is None:
            return 1.0
        mx, my = self._ox_mouse_pos
        sx, sy = self._oolong_rest_start_pos
        moved = math.hypot(mx - sx, my - sy)
        return max(0.0, 1.0 - moved / 40.0)

    # ── ritual: BLACK — CTC Rolling Press ─────────────────────────────────────

    def _update_draw_black(self, dt, top_y):
        GRID_X = SCREEN_W // 2 - 114
        GRID_Y = top_y + 70
        CELL_SZ = 38

        # Build cell rects once
        if not self._black_cell_rects:
            for row in range(6):
                for col in range(6):
                    rx = GRID_X + col * CELL_SZ
                    ry = GRID_Y + row * CELL_SZ
                    self._black_cell_rects[(row, col)] = pygame.Rect(rx, ry, CELL_SZ - 2, CELL_SZ - 2)

        if self._black_crush_phase:
            self._black_crush_timer += dt
            if self._black_crush_timer >= 15.0:
                self._black_crush_phase = False

            # Drag crushing
            if self._ox_mouse_down:
                for (row, col), rect in self._black_cell_rects.items():
                    if rect.collidepoint(self._ox_mouse_pos):
                        if self._black_cells[row][col] < 2:
                            self._black_cells[row][col] += 1

        else:
            self._black_ox_timer += dt
            # Crushed cells oxidize
            crushed = sum(1 for r in self._black_cells for c in r if c == 2)
            ox_rate = 0.002 + crushed * 0.0001
            self._oxidation_level = min(0.93, self._oxidation_level + ox_rate * dt * 60)
            if self._oxidation_level >= 0.93:
                self._oxidation_level = 0.93

        crushed_total = sum(1 for r in self._black_cells for c in r if c == 2)
        crush_ratio = crushed_total / 36.0
        lo_z, hi_z = 0.75, 0.93
        zone_center = (lo_z + hi_z) / 2
        zone_centrality = max(0.0, 1.0 - abs(self._oxidation_level - zone_center) / (0.09 + 1e-6))
        self._ox_ritual_quality = crush_ratio * 0.6 + zone_centrality * 0.4

        # Draw grid
        cell_colors = [
            (30, 90, 30),    # intact
            (60, 45, 20),    # cracked
            (15, 10, 8),     # crushed
        ]
        for (row, col), rect in self._black_cell_rects.items():
            state = self._black_cells[row][col]
            bg = cell_colors[state]
            # During oxidation phase, darken crushed cells with time
            if not self._black_crush_phase and state == 2:
                t_frac = min(1.0, self._black_ox_timer / 10.0)
                ox_shift = int(t_frac * 50)
                bg = (max(0, bg[0] - ox_shift), max(0, bg[1] - ox_shift), max(0, bg[2] - ox_shift))
            pygame.draw.rect(self.screen, bg, rect)
            if state == 0:
                pygame.draw.line(self.screen, (60, 110, 50),
                                 (rect.centerx, rect.top + 3), (rect.centerx, rect.bottom - 3), 1)
                pygame.draw.rect(self.screen, (50, 80, 45), rect, 1)
            elif state == 1:
                pygame.draw.line(self.screen, (100, 75, 30),
                                 (rect.left + 3, rect.top + 3), (rect.right - 3, rect.bottom - 3), 2)
                pygame.draw.rect(self.screen, (80, 60, 30), rect, 1)
            else:
                pygame.draw.rect(self.screen, (35, 25, 15), rect, 1)

        # Status labels
        phase_y = GRID_Y + 6 * CELL_SZ + 12
        if self._black_crush_phase:
            time_left = max(0, 15.0 - self._black_crush_timer)
            cl = self.font.render(f"CRUSH  —  {crushed_total}/36 cells  —  {time_left:.0f}s left",
                                  True, _TITLE_C)
            self.screen.blit(cl, (SCREEN_W // 2 - cl.get_width() // 2, phase_y))
            drag_hint = self.small.render("Hold and drag over the grid", True, _HINT_C)
            self.screen.blit(drag_hint, (SCREEN_W // 2 - drag_hint.get_width() // 2, phase_y + 22))
        else:
            ox_t_left = max(0, 10.0 - self._black_ox_timer)
            ol = self.font.render(f"OXIDIZING  —  {self._oxidation_level:.0%}  —  {ox_t_left:.0f}s",
                                  True, (180, 80, 40))
            self.screen.blit(ol, (SCREEN_W // 2 - ol.get_width() // 2, phase_y))
            stop_rect = pygame.Rect(SCREEN_W // 2 - 70, phase_y + 26, 140, 32)
            pygame.draw.rect(self.screen, (60, 20, 10), stop_rect)
            pygame.draw.rect(self.screen, (200, 80, 40), stop_rect, 2)
            sl = self.font.render("STOP", True, (255, 200, 120))
            self.screen.blit(sl, (stop_rect.centerx - sl.get_width() // 2,
                                  stop_rect.centery - sl.get_height() // 2))
            self._black_stop_btn = stop_rect

    # ── ritual: PU-ERH — Wo Dui Pile ──────────────────────────────────────────

    def _update_draw_puerh(self, dt, top_y):
        FIELD_W, FIELD_H = 280, 280
        FIELD_X = SCREEN_W // 2 - FIELD_W // 2
        FIELD_Y = top_y + 60
        self._puerh_field_rect = pygame.Rect(FIELD_X, FIELD_Y, FIELD_W, FIELD_H)

        mx, my = self._ox_mouse_pos
        if self._puerh_field_rect.collidepoint(mx, my):
            aeration = (mx - FIELD_X) / FIELD_W
            moisture  = (my - FIELD_Y) / FIELD_H
        else:
            aeration = 0.5
            moisture  = 0.5

        # Check zones
        ECX, ECY, ERX, ERY = 0.52, 0.52, 0.24, 0.20
        in_zone = ((aeration - ECX) / ERX) ** 2 + ((moisture - ECY) / ERY) ** 2 <= 1.0
        in_mold  = aeration > 0.76 and moisture > 0.76

        if in_zone:
            self._puerh_zone_dwell += dt
            self._oxidation_level = min(1.0, self._oxidation_level + 0.005 * dt * 60)
        elif in_mold:
            self._puerh_mold_time += dt
            self._oxidation_level = min(1.0, self._oxidation_level + 0.003 * dt * 60)
        else:
            self._oxidation_level = min(1.0, self._oxidation_level + 0.0005 * dt * 60)
        self._oxidation_level = max(0.93, self._oxidation_level)

        dwell_frac = self._puerh_zone_dwell / self._oxidation_total_time
        mold_penalty = min(0.8, self._puerh_mold_time * 0.12)
        self._ox_ritual_quality = dwell_frac * (1.0 - mold_penalty)

        # Draw field
        pygame.draw.rect(self.screen, (25, 18, 10), self._puerh_field_rect)
        pygame.draw.rect(self.screen, _DIM_C, self._puerh_field_rect, 1)

        # Zones (colored regions)
        stall_rect = pygame.Rect(FIELD_X, FIELD_Y, int(FIELD_W * 0.3), int(FIELD_H * 0.4))
        pygame.draw.rect(self.screen, (25, 35, 60), stall_rect)
        sl = self.small.render("stall", True, (60, 90, 140))
        self.screen.blit(sl, (FIELD_X + 4, FIELD_Y + 4))

        mold_x = FIELD_X + int(FIELD_W * 0.76)
        mold_y = FIELD_Y + int(FIELD_H * 0.76)
        mold_w = FIELD_W - int(FIELD_W * 0.76)
        mold_h = FIELD_H - int(FIELD_H * 0.76)
        pygame.draw.rect(self.screen, (50, 20, 20),
                         (mold_x, mold_y, mold_w, mold_h))
        ml = self.small.render("mold!", True, (200, 60, 60))
        self.screen.blit(ml, (mold_x + 4, mold_y + 4))

        # Ideal ellipse
        ell_cx = FIELD_X + int(ECX * FIELD_W)
        ell_cy = FIELD_Y + int(ECY * FIELD_H)
        ell_rx = int(ERX * FIELD_W)
        ell_ry = int(ERY * FIELD_H)
        col = (120, 180, 80) if in_zone else (60, 100, 40)
        pygame.draw.ellipse(self.screen, col,
                            (ell_cx - ell_rx, ell_cy - ell_ry, ell_rx * 2, ell_ry * 2), 3)
        if in_zone:
            pygame.draw.ellipse(self.screen, (40, 60, 20),
                                (ell_cx - ell_rx, ell_cy - ell_ry, ell_rx * 2, ell_ry * 2))

        # Axis labels
        ax_l = self.small.render("← compact", True, _DIM_C)
        ax_r = self.small.render("open →",   True, _DIM_C)
        ax_t = self.small.render("dry ↑",    True, _DIM_C)
        ax_b = self.small.render("↓ wet",    True, _DIM_C)
        self.screen.blit(ax_l, (FIELD_X + 2, FIELD_Y + FIELD_H + 4))
        self.screen.blit(ax_r, (FIELD_X + FIELD_W - ax_r.get_width() - 2, FIELD_Y + FIELD_H + 4))
        self.screen.blit(ax_t, (FIELD_X - ax_t.get_width() - 4, FIELD_Y + 2))
        self.screen.blit(ax_b, (FIELD_X - ax_b.get_width() - 4, FIELD_Y + FIELD_H - 16))

        # Crosshair
        if self._puerh_field_rect.collidepoint(mx, my):
            cross_col = (200, 220, 100) if in_zone else (180, 100, 80)
            pygame.draw.line(self.screen, cross_col, (mx - 10, my), (mx + 10, my), 2)
            pygame.draw.line(self.screen, cross_col, (mx, my - 10), (mx, my + 10), 2)

        # Mold warning
        if self._puerh_mold_time > 0:
            mw = self.small.render(f"Mold: {self._puerh_mold_time:.1f}s!", True, (220, 80, 60))
            self.screen.blit(mw, (FIELD_X + FIELD_W + 8, FIELD_Y))

        # Dwell bar
        dw = self.small.render("Ideal time:", True, _LABEL_C)
        self.screen.blit(dw, (FIELD_X, FIELD_Y + FIELD_H + 22))
        pygame.draw.rect(self.screen, _DARK_BG, (FIELD_X + 90, FIELD_Y + FIELD_H + 22, 180, 10))
        pygame.draw.rect(self.screen, (100, 180, 60),
                         (FIELD_X + 90, FIELD_Y + FIELD_H + 22, int(180 * dwell_frac), 10))

    # ── click / key / mouse handlers ──────────────────────────────────────────

    def _handle_oxidation_station_click(self, pos, player):
        if self._oxidation_phase == "select_leaf":
            for bi, rect in self._oxidation_select_rects.items():
                if rect.collidepoint(pos):
                    if player.tea_leaves[bi].state == "withered":
                        self._oxidation_leaf_idx = bi
                        self._oxidation_phase    = "select_zone"
                    return

        elif self._oxidation_phase == "select_zone":
            for key, rect in self._ox_zone_btn_rects.items():
                if rect.collidepoint(pos):
                    self._start_ritual(key)
                    return

        elif self._oxidation_phase == "ritual":
            zone = self._ox_target_zone
            if zone == "yellow":
                # Toggle wrap/unwrap on any click
                prev_time = self._yellow_wrap_time
                if prev_time > 0.4:
                    self._yellow_interval_log.append(prev_time)
                self._yellow_wrapped   = not self._yellow_wrapped
                self._yellow_wrap_time = 0.0
                return
            if zone == "black" and not self._black_crush_phase:
                if self._black_stop_btn and self._black_stop_btn.collidepoint(pos):
                    self._finish_oxidation(player)
                    return
            if self._oxidation_lock_btn and self._oxidation_lock_btn.collidepoint(pos):
                self._finish_oxidation(player)
                return

        elif self._oxidation_phase == "result":
            if self._oxidation_result_btn and self._oxidation_result_btn.collidepoint(pos):
                self._oxidation_phase    = "select_leaf"
                self._oxidation_leaf_idx = None

    def _start_ritual(self, zone_key):
        from tea import OXIDATION_ZONES
        lo, hi = OXIDATION_ZONES[zone_key]
        self._ox_target_zone       = zone_key
        self._oxidation_level      = (lo + hi) / 2
        self._oxidation_time       = 0.0
        self._ox_ritual_quality    = 0.0
        self._oxidation_phase      = "ritual"
        # white
        self._white_warmth_score   = 0.0
        self._white_dew_pools      = []
        self._white_pocket_angle   = 0.0
        self._white_dew_timer      = 0.0
        self._white_dew_next       = 3.0
        # yellow
        self._yellow_wrapped       = False
        self._yellow_heat_arc      = 0.2
        self._yellow_wrap_time     = 0.0
        self._yellow_interval_log  = []
        self._yellow_rhythm_score  = 0.5
        # green
        self._green_drag_last      = None
        self._green_drag_vel       = 0.0
        self._green_sectors        = [0.0] * 8
        self._green_enzyme         = 1.0
        self._green_still_timer    = 0.0
        # oolong
        self._oolong_sub           = "roll_1"
        self._oolong_sub_timer     = 0.0
        self._oolong_angle_accum   = 0.0
        self._oolong_prev_angle    = None
        self._oolong_roll1_score   = 0.0
        self._oolong_roll2_score   = 0.0
        self._oolong_rest1_score   = 1.0
        self._oolong_rest2_score   = 1.0
        self._oolong_trail         = []
        self._oolong_rest_start_pos = None
        # black
        self._black_crush_phase    = True
        self._black_crush_timer    = 0.0
        self._black_ox_timer       = 0.0
        self._black_cells          = [[0]*6 for _ in range(6)]
        self._black_cell_rects     = {}
        self._black_stop_btn       = None
        # puerh
        self._puerh_zone_dwell     = 0.0
        self._puerh_mold_time      = 0.0

    def handle_oxidation_mouse_motion(self, pos):
        self._ox_mouse_pos = pos

    def handle_oxidation_mouse_down(self, pos, player):
        self._ox_mouse_pos  = pos
        self._ox_mouse_down = True
        self._handle_oxidation_station_click(pos, player)

    def handle_oxidation_mouse_up(self, pos):
        self._ox_mouse_pos  = pos
        self._ox_mouse_down = False

    def handle_oxidation_keydown(self, key, player):
        import pygame as _pg
        if key == _pg.K_RETURN:
            if self._oxidation_phase == "ritual":
                self._finish_oxidation(player)
            elif self._oxidation_phase == "result":
                self._oxidation_phase    = "select_leaf"
                self._oxidation_leaf_idx = None

    def handle_oxidation_keys(self, keys, dt, player):
        # No per-frame key polling needed in the new system
        pass

    def _finish_oxidation(self, player):
        from tea import tea_type_from_oxidation, OXIDATION_ZONES
        leaf   = player.tea_leaves[self._oxidation_leaf_idx]
        ox     = self._oxidation_level
        t_type = tea_type_from_oxidation(ox)
        lo, hi = OXIDATION_ZONES[t_type]
        center = (lo + hi) / 2.0
        half   = (hi - lo) / 2.0 + 1e-6
        centrality  = max(0.0, 1.0 - abs(ox - center) / half)
        ritual_q    = max(0.0, min(1.0, self._ox_ritual_quality))
        quality     = 0.5 * centrality + 0.5 * ritual_q
        if t_type == self._ox_target_zone:
            quality = min(1.0, quality * 1.15)
        apply_oxidation(leaf, ox, quality)
        player.discovered_tea_origins.add(f"{leaf.origin_biome}_{leaf.tea_type}")
        self._oxidation_phase = "result"

    # ─────────────────────────────────────────────────────────────────────────
    # TEA CELLAR
    # ─────────────────────────────────────────────────────────────────────────

    def _draw_tea_cellar(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("TEA CELLAR", True, _TITLE_C)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, _HINT_C)
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        # Tab bar
        tabs     = [("brew", "Brew"), ("blend", "Blend"), ("age", "Age (Pu-erh)"), ("roast", "Roast")]
        tab_w    = 180
        tab_x    = SCREEN_W // 2 - (len(tabs) * tab_w) // 2
        self._tea_cellar_tab_rects = {}
        for ti, (tkey, tlbl) in enumerate(tabs):
            trect = pygame.Rect(tab_x + ti * tab_w, 30, tab_w - 4, 26)
            self._tea_cellar_tab_rects[tkey] = trect
            active = (self._tea_cellar_tab == tkey)
            pygame.draw.rect(self.screen, (_ACCENT if active else _DARK_BG), trect)
            pygame.draw.rect(self.screen, _ACCENT, trect, 1)
            ts = self.small.render(tlbl, True, (255, 255, 255) if active else _LABEL_C)
            self.screen.blit(ts, (trect.centerx - ts.get_width() // 2,
                                  trect.centery - ts.get_height() // 2))

        if self._tea_cellar_tab == "brew":
            self._draw_tea_cellar_brew(player)
        elif self._tea_cellar_tab == "blend":
            self._draw_tea_cellar_blend(player)
        elif self._tea_cellar_tab == "age":
            self._draw_tea_cellar_age(player)
        elif self._tea_cellar_tab == "roast":
            self._draw_tea_cellar_roast(player)

    def _draw_tea_cellar_brew(self, player):
        self._tea_cellar_select_rects.clear()
        oxidized = [(i, x) for i, x in enumerate(player.tea_leaves)
                    if x.state in ("oxidized", "blended")]
        if not oxidized:
            msg = self.font.render("No processed leaves! Use the Oxidation Station first.", True, _LABEL_C)
            self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2))
            return
        sub = self.small.render("Select a leaf to brew into tea:", True, _LABEL_C)
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 62))
        CELL_W, CELL_H, GAP, COLS = 220, 66, 8, 5
        gx0 = (SCREEN_W - (COLS * CELL_W + (COLS - 1) * GAP)) // 2
        for li, (bi, leaf) in enumerate(oxidized[:20]):
            col_i, row_i = li % COLS, li // COLS
            rx = gx0 + col_i * (CELL_W + GAP)
            ry = 82 + row_i * (CELL_H + GAP)
            rect = pygame.Rect(rx, ry, CELL_W, CELL_H)
            self._tea_cellar_select_rects[bi] = rect
            tea_col = TEA_TYPE_COLORS.get(leaf.tea_type, _ACCENT)
            pygame.draw.rect(self.screen, _CELL_BG, rect)
            pygame.draw.rect(self.screen, tea_col, rect, 2)
            nm = BIOME_DISPLAY_NAMES.get(leaf.origin_biome, leaf.origin_biome)
            ns = self.small.render(nm + " — " + leaf.tea_type.title(), True, tea_col)
            self.screen.blit(ns, (rx + 6, ry + 6))
            ss = self._render_stars(self.small, leaf.steep_quality)
            self.screen.blit(ss, (rx + 6, ry + 24))
            out_id = get_brew_item_id(leaf)
            from items import ITEMS
            out_name = ITEMS.get(out_id, {}).get("name", out_id)
            os = self.small.render("→ " + out_name, True, _HINT_C)
            self.screen.blit(os, (rx + 6, ry + 42))

    def _draw_tea_cellar_blend(self, player):
        self._tea_cellar_select_rects.clear()
        oxidized = [(i, x) for i, x in enumerate(player.tea_leaves)
                    if x.state in ("oxidized", "blended") and x.tea_type]
        if not oxidized:
            msg = self.font.render("No processed leaves to blend.", True, _LABEL_C)
            self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2 - 20))
            return
        sub = self.small.render("Select a leaf to add herbal blends:", True, _LABEL_C)
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 62))
        CELL_W, CELL_H, GAP, COLS = 220, 56, 8, 5
        gx0 = (SCREEN_W - (COLS * CELL_W + (COLS - 1) * GAP)) // 2
        for li, (bi, leaf) in enumerate(oxidized[:15]):
            col_i, row_i = li % COLS, li // COLS
            rx = gx0 + col_i * (CELL_W + GAP)
            ry = 82 + row_i * (CELL_H + GAP)
            rect = pygame.Rect(rx, ry, CELL_W, CELL_H)
            self._tea_cellar_select_rects[bi] = rect
            tea_col = TEA_TYPE_COLORS.get(leaf.tea_type, _ACCENT)
            pygame.draw.rect(self.screen, _CELL_BG, rect)
            pygame.draw.rect(self.screen, tea_col, rect, 2)
            nm  = BIOME_DISPLAY_NAMES.get(leaf.origin_biome, leaf.origin_biome)
            ns  = self.small.render(nm + " " + leaf.tea_type.title(), True, tea_col)
            self.screen.blit(ns, (rx + 6, ry + 6))
            adds = ", ".join(HERBAL_ADDITIVES.get(k, {}).get("label", k) for k in leaf.herbal_additions)
            if adds:
                as_ = self.small.render("+ " + adds, True, (180, 210, 140))
                self.screen.blit(as_, (rx + 6, ry + 24))

        # Show available additives on the right
        if self._tea_cellar_leaf_idx is not None and \
           0 <= self._tea_cellar_leaf_idx < len(player.tea_leaves):
            leaf = player.tea_leaves[self._tea_cellar_leaf_idx]
            rx0 = SCREEN_W - 280
            ry0 = 82
            pygame.draw.rect(self.screen, _DARK_BG, (rx0, ry0, 260, 200))
            pygame.draw.rect(self.screen, _ACCENT, (rx0, ry0, 260, 200), 2)
            hdr = self.small.render("Add Herbals (from inventory):", True, _LABEL_C)
            self.screen.blit(hdr, (rx0 + 8, ry0 + 6))
            self._tea_herbal_rects = {}
            for hi, (hkey, hdata) in enumerate(HERBAL_ADDITIVES.items()):
                have = player.inventory.get(hkey, 0)
                if have <= 0:
                    continue
                hrect = pygame.Rect(rx0 + 8, ry0 + 30 + hi * 34, 244, 28)
                self._tea_herbal_rects[hkey] = hrect
                already = hkey in leaf.herbal_additions
                pygame.draw.rect(self.screen, (30, 60, 30) if not already else (50, 90, 50), hrect)
                pygame.draw.rect(self.screen, _ACCENT, hrect, 1)
                lbl_s = self.small.render(
                    hdata["label"] + (f"  (x{have})" if not already else "  ✓"), True,
                    _TITLE_C if not already else (180, 220, 140))
                self.screen.blit(lbl_s, (hrect.x + 6, hrect.centery - lbl_s.get_height() // 2))

    def _draw_tea_cellar_age(self, player):
        self._tea_cellar_select_rects.clear()
        puerh = [(i, x) for i, x in enumerate(player.tea_leaves)
                 if x.state == "oxidized" and x.tea_type == "puerh"]
        if not puerh:
            msg = self.font.render("No oxidized Pu-erh leaves! Only Pu-erh can be aged.", True, _LABEL_C)
            self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2 - 20))
            return
        sub = self.small.render("Select a Pu-erh leaf to age:", True, _LABEL_C)
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 62))
        CELL_W, CELL_H, GAP, COLS = 220, 56, 8, 4
        gx0 = (SCREEN_W - (COLS * CELL_W + (COLS - 1) * GAP)) // 2
        for li, (bi, leaf) in enumerate(puerh[:12]):
            col_i, row_i = li % COLS, li // COLS
            rx = gx0 + col_i * (CELL_W + GAP)
            ry = 82 + row_i * (CELL_H + GAP)
            rect = pygame.Rect(rx, ry, CELL_W, CELL_H)
            self._tea_cellar_select_rects[bi] = rect
            tea_col = TEA_TYPE_COLORS.get("puerh", _ACCENT)
            pygame.draw.rect(self.screen, _CELL_BG, rect)
            pygame.draw.rect(self.screen, tea_col, rect, 2)
            nm  = BIOME_DISPLAY_NAMES.get(leaf.origin_biome, leaf.origin_biome)
            ns  = self.small.render(nm, True, tea_col)
            self.screen.blit(ns, (rx + 6, ry + 8))
            ss = self._render_stars(self.small, leaf.steep_quality)
            self.screen.blit(ss, (rx + 6, ry + 26))

        if self._tea_cellar_leaf_idx is not None and \
           0 <= self._tea_cellar_leaf_idx < len(player.tea_leaves):
            leaf = player.tea_leaves[self._tea_cellar_leaf_idx]
            rx0 = SCREEN_W - 300
            ry0 = 82
            pygame.draw.rect(self.screen, _DARK_BG, (rx0, ry0, 280, 220))
            pygame.draw.rect(self.screen, TEA_TYPE_COLORS.get("puerh", _ACCENT), (rx0, ry0, 280, 220), 2)
            hdr = self.small.render("Choose aging duration:", True, _LABEL_C)
            self.screen.blit(hdr, (rx0 + 8, ry0 + 6))
            self._tea_cellar_age_rects.clear()
            for ai, (akey, adata) in enumerate(AGE_DURATIONS.items()):
                arect = pygame.Rect(rx0 + 8, ry0 + 32 + ai * 52, 264, 44)
                self._tea_cellar_age_rects[akey] = arect
                pygame.draw.rect(self.screen, (30, 22, 10), arect)
                pygame.draw.rect(self.screen, (130, 90, 40), arect, 2)
                al  = self.font.render(adata["label"], True, (200, 160, 80))
                self.screen.blit(al, (arect.x + 10, arect.y + 6))
                qm  = self.small.render(f"Quality ×{adata['quality_mult']:.2f}  +{adata['complexity_delta']:.0%} complexity",
                                         True, _HINT_C)
                self.screen.blit(qm, (arect.x + 10, arect.y + 26))

    def _handle_tea_cellar_click(self, pos, player):
        # Tab clicks
        if hasattr(self, "_tea_cellar_tab_rects"):
            for tkey, trect in self._tea_cellar_tab_rects.items():
                if trect.collidepoint(pos):
                    self._tea_cellar_tab      = tkey
                    self._tea_cellar_leaf_idx = None
                    return

        if self._tea_cellar_tab == "brew":
            for bi, rect in self._tea_cellar_select_rects.items():
                if rect.collidepoint(pos):
                    leaf = player.tea_leaves[bi]
                    out_id = get_brew_item_id(leaf)
                    player._add_item(out_id)
                    player.tea_leaves.pop(bi)
                    return

        elif self._tea_cellar_tab == "blend":
            for bi, rect in self._tea_cellar_select_rects.items():
                if rect.collidepoint(pos):
                    self._tea_cellar_leaf_idx = bi
                    return
            if hasattr(self, "_tea_herbal_rects") and self._tea_cellar_leaf_idx is not None:
                leaf = player.tea_leaves[self._tea_cellar_leaf_idx]
                for hkey, hrect in self._tea_herbal_rects.items():
                    if hrect.collidepoint(pos) and hkey not in leaf.herbal_additions:
                        if player.inventory.get(hkey, 0) > 0:
                            apply_herbal_blend(leaf, [hkey])
                            player.inventory[hkey] = player.inventory[hkey] - 1
                            if player.inventory[hkey] <= 0:
                                del player.inventory[hkey]
                            return

        elif self._tea_cellar_tab == "age":
            for bi, rect in self._tea_cellar_select_rects.items():
                if rect.collidepoint(pos):
                    self._tea_cellar_leaf_idx = bi
                    return
            if self._tea_cellar_leaf_idx is not None:
                leaf = player.tea_leaves[self._tea_cellar_leaf_idx]
                for akey, arect in self._tea_cellar_age_rects.items():
                    if arect.collidepoint(pos):
                        apply_aging(leaf, akey)
                        self._tea_cellar_leaf_idx = None
                        return

        elif self._tea_cellar_tab == "roast":
            for bi, rect in self._tea_cellar_select_rects.items():
                if rect.collidepoint(pos):
                    self._tea_cellar_leaf_idx = bi
                    return
            if self._tea_cellar_leaf_idx is not None:
                leaf = player.tea_leaves[self._tea_cellar_leaf_idx]
                for rkey, rrect in self._tea_cellar_roast_rects.items():
                    if rrect.collidepoint(pos):
                        apply_roasting(leaf, rkey)
                        player.discovered_tea_origins.add(f"{leaf.origin_biome}_hojicha")
                        self._tea_cellar_leaf_idx = None
                        return

    def _draw_tea_cellar_roast(self, player):
        self._tea_cellar_select_rects.clear()
        roastable = [(i, x) for i, x in enumerate(player.tea_leaves)
                     if x.state == "oxidized" and x.tea_type in ("green", "oolong", "white", "yellow")]
        if not roastable:
            msg = self.font.render("No roastable leaves! Use oxidized Green, White, Yellow, or Oolong.", True, _LABEL_C)
            self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2 - 20))
            return
        sub = self.small.render("Select a leaf to roast into Hojicha:", True, _LABEL_C)
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 62))
        CELL_W, CELL_H, GAP, COLS = 220, 56, 8, 4
        gx0 = (SCREEN_W - (COLS * CELL_W + (COLS - 1) * GAP)) // 2
        for li, (bi, leaf) in enumerate(roastable[:12]):
            col_i, row_i = li % COLS, li // COLS
            rx = gx0 + col_i * (CELL_W + GAP)
            ry = 82 + row_i * (CELL_H + GAP)
            rect = pygame.Rect(rx, ry, CELL_W, CELL_H)
            self._tea_cellar_select_rects[bi] = rect
            tea_col = TEA_TYPE_COLORS.get(leaf.tea_type, _ACCENT)
            pygame.draw.rect(self.screen, _CELL_BG, rect)
            pygame.draw.rect(self.screen, tea_col, rect, 2)
            nm  = BIOME_DISPLAY_NAMES.get(leaf.origin_biome, leaf.origin_biome)
            ns  = self.small.render(nm + " — " + leaf.tea_type.title(), True, tea_col)
            self.screen.blit(ns, (rx + 6, ry + 8))
            ss = self._render_stars(self.small, leaf.steep_quality)
            self.screen.blit(ss, (rx + 6, ry + 26))

        if self._tea_cellar_leaf_idx is not None and \
           0 <= self._tea_cellar_leaf_idx < len(player.tea_leaves):
            leaf = player.tea_leaves[self._tea_cellar_leaf_idx]
            rx0 = SCREEN_W - 300
            ry0 = 82
            pygame.draw.rect(self.screen, _DARK_BG, (rx0, ry0, 280, 240))
            pygame.draw.rect(self.screen, TEA_TYPE_COLORS.get("hojicha", _ACCENT), (rx0, ry0, 280, 240), 2)
            hdr = self.small.render("Choose roast level:", True, _LABEL_C)
            self.screen.blit(hdr, (rx0 + 8, ry0 + 6))
            self._tea_cellar_roast_rects.clear()
            for ri, (rkey, rdata) in enumerate(ROASTING_LEVELS.items()):
                rrect = pygame.Rect(rx0 + 8, ry0 + 32 + ri * 62, 264, 54)
                self._tea_cellar_roast_rects[rkey] = rrect
                pygame.draw.rect(self.screen, (35, 20, 10), rrect)
                pygame.draw.rect(self.screen, TEA_TYPE_COLORS.get("hojicha", _ACCENT), rrect, 2)
                rl  = self.font.render(rdata["label"], True, (200, 140, 70))
                self.screen.blit(rl, (rrect.x + 10, rrect.y + 6))
                desc_lines = rdata["desc"].split(". ")
                for di, dl in enumerate(desc_lines[:1]):
                    ds = self.small.render(dl, True, _HINT_C)
                    self.screen.blit(ds, (rrect.x + 10, rrect.y + 28))
                qm = self.small.render(f"Quality ×{rdata['quality_mult']:.2f}  +{rdata['complexity_bonus']:.0%} complexity",
                                       True, _DIM_C)
                self.screen.blit(qm, (rrect.x + 10, rrect.y + 40))

    # ─────────────────────────────────────────────────────────────────────────
    # ROASTING KILN (standalone block)
    # ─────────────────────────────────────────────────────────────────────────

    def _draw_roasting_kiln(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("ROASTING KILN", True, (200, 140, 70))
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC to close", True, _HINT_C)
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        if self._roasting_phase == "select_leaf":
            self._roasting_select_rects.clear()
            roastable = [(i, x) for i, x in enumerate(player.tea_leaves)
                         if x.state == "oxidized" and x.tea_type in ("green", "oolong", "white", "yellow")]
            if not roastable:
                msg = self.font.render("No roastable leaves! Use oxidized Green, White, Yellow, or Oolong.", True, _LABEL_C)
                self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2))
                return
            sub = self.small.render("Select a leaf to roast into Hojicha:", True, _LABEL_C)
            self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 32))
            CELL_W, CELL_H, GAP, COLS = 200, 56, 8, 5
            gx0 = (SCREEN_W - (COLS * CELL_W + (COLS - 1) * GAP)) // 2
            for li, (bi, leaf) in enumerate(roastable[:20]):
                col_i, row_i = li % COLS, li // COLS
                rx = gx0 + col_i * (CELL_W + GAP)
                ry = 55 + row_i * (CELL_H + GAP)
                rect = pygame.Rect(rx, ry, CELL_W, CELL_H)
                self._roasting_select_rects[bi] = rect
                tea_col = TEA_TYPE_COLORS.get(leaf.tea_type, _ACCENT)
                pygame.draw.rect(self.screen, _CELL_BG, rect)
                pygame.draw.rect(self.screen, tea_col, rect, 2)
                nm = BIOME_DISPLAY_NAMES.get(leaf.origin_biome, leaf.origin_biome)
                ns = self.small.render(nm + " — " + leaf.tea_type.title(), True, tea_col)
                self.screen.blit(ns, (rx + 6, ry + 8))
                ss = self._render_stars(self.small, leaf.steep_quality)
                self.screen.blit(ss, (rx + 6, ry + 26))

        elif self._roasting_phase == "select_level":
            sub = self.small.render("Choose a roast level:", True, _LABEL_C)
            self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 32))
            self._roasting_level_rects.clear()
            BTN_W, BTN_H, BTN_GAP = 280, 120, 20
            total_w = len(ROASTING_LEVELS) * BTN_W + (len(ROASTING_LEVELS) - 1) * BTN_GAP
            gx0 = (SCREEN_W - total_w) // 2
            for ri, (rkey, rdata) in enumerate(ROASTING_LEVELS.items()):
                px = gx0 + ri * (BTN_W + BTN_GAP)
                py = SCREEN_H // 2 - BTN_H // 2
                prect = pygame.Rect(px, py, BTN_W, BTN_H)
                self._roasting_level_rects[rkey] = prect
                pygame.draw.rect(self.screen, (30, 18, 8), prect)
                pygame.draw.rect(self.screen, (160, 90, 35), prect, 2)
                lbl = self.font.render(rdata["label"], True, (210, 150, 80))
                self.screen.blit(lbl, (px + BTN_W // 2 - lbl.get_width() // 2, py + 10))
                desc_lines = rdata["desc"].split(". ")
                for di, dl in enumerate(desc_lines[:2]):
                    ds = self.small.render(dl, True, _LABEL_C)
                    self.screen.blit(ds, (px + 8, py + 40 + di * 16))
                qm = self.small.render(f"Quality ×{rdata['quality_mult']:.2f}  +{rdata['complexity_bonus']:.0%} complexity",
                                       True, _HINT_C)
                self.screen.blit(qm, (px + 8, py + 90))

        elif self._roasting_phase == "result":
            leaf = player.tea_leaves[self._roasting_leaf_idx]
            hojicha_col = TEA_TYPE_COLORS.get("hojicha", _ACCENT)
            cx, cy = SCREEN_W // 2, 80
            pygame.draw.circle(self.screen, hojicha_col, (cx, cy + 40), 36)
            pygame.draw.circle(self.screen, (min(255, hojicha_col[0] + 40),
                                              min(255, hojicha_col[1] + 40),
                                              min(255, hojicha_col[2] + 40)),
                                (cx, cy + 40), 36, 3)

            iy = cy + 95
            def rline(txt, col=_TITLE_C):
                nonlocal iy
                s = self.font.render(txt, True, col)
                self.screen.blit(s, (cx - s.get_width() // 2, iy))
                iy += 28

            rline(BIOME_DISPLAY_NAMES.get(leaf.origin_biome, leaf.origin_biome) + " " +
                  VARIETY_DISPLAY_NAMES.get(leaf.variety, leaf.variety))
            rline(TEA_TYPE_DESCS.get("hojicha", "Hojicha"), hojicha_col)
            rline(f"Roast: {ROASTING_LEVELS.get(leaf.roasting_level, {}).get('label', leaf.roasting_level)}", (200, 140, 70))
            ss = self._render_stars(self.font, leaf.steep_quality)
            self.screen.blit(ss, (cx - ss.get_width() // 2, iy))
            iy += 28
            if leaf.flavor_notes:
                rline("Flavour Notes:", (160, 200, 130))
                for note in leaf.flavor_notes:
                    rline(f"  • {note.title()}", _TITLE_C)

            done_rect = pygame.Rect(cx - 70, iy + 20, 140, 34)
            pygame.draw.rect(self.screen, _DARK_BG, done_rect)
            pygame.draw.rect(self.screen, (160, 90, 35), done_rect, 2)
            dl = self.font.render("DONE", True, _TITLE_C)
            self.screen.blit(dl, (done_rect.centerx - dl.get_width() // 2,
                                  done_rect.centery - dl.get_height() // 2))
            self._roasting_result_btn = done_rect

    def _handle_roasting_kiln_click(self, pos, player):
        if self._roasting_phase == "select_leaf":
            for bi, rect in self._roasting_select_rects.items():
                if rect.collidepoint(pos):
                    if player.tea_leaves[bi].state == "oxidized":
                        self._roasting_leaf_idx = bi
                        self._roasting_phase    = "select_level"
                    return
        elif self._roasting_phase == "select_level":
            for rkey, rect in self._roasting_level_rects.items():
                if rect.collidepoint(pos):
                    leaf = player.tea_leaves[self._roasting_leaf_idx]
                    apply_roasting(leaf, rkey)
                    player.discovered_tea_origins.add(f"{leaf.origin_biome}_hojicha")
                    self._roasting_phase = "result"
                    return
        elif self._roasting_phase == "result":
            if self._roasting_result_btn and self._roasting_result_btn.collidepoint(pos):
                self._roasting_phase    = "select_leaf"
                self._roasting_leaf_idx = None

    # ─────────────────────────────────────────────────────────────────────────
    # BUFF HUD
    # ─────────────────────────────────────────────────────────────────────────

    def _draw_tea_buffs(self, player):
        if not player.tea_buffs:
            return
        x = SCREEN_W - 200
        y = 260
        for buff, data in player.tea_buffs.items():
            dur    = data["duration"]
            label  = BUFF_DESCS.get(buff, buff)
            lbl_s  = self.small.render(f"☕ {label}", True, _TITLE_C)
            self.screen.blit(lbl_s, (x, y))
            bar_w  = 180
            bar_h  = 6
            max_dur = 225.0
            fill    = max(0, min(bar_w, int(bar_w * dur / max_dur)))
            pygame.draw.rect(self.screen, _DARK_BG, (x, y + 14, bar_w, bar_h))
            pygame.draw.rect(self.screen, _ACCENT,   (x, y + 14, fill,  bar_h))
            y += 26

    # ─────────────────────────────────────────────────────────────────────────
    # CODEX (called from collections.py)
    # ─────────────────────────────────────────────────────────────────────────

    def _draw_tea_codex(self, player, gy0=58, gx_off=0):
        TEA_TYPES = _CODEX_TEA_TYPES
        BIOMES    = _CODEX_BIOMES
        COLS      = len(TEA_TYPES)
        CELL_W, CELL_H, GAP = 96, 64, 4
        HDR_H     = 22
        gx0 = gx_off + (SCREEN_W - gx_off - (COLS * CELL_W + (COLS - 1) * GAP)) // 2

        # Column headers
        hdr_y = gy0
        for ci, t_type in enumerate(TEA_TYPES):
            hx    = gx0 + ci * (CELL_W + GAP)
            tc    = TEA_TYPE_COLORS.get(t_type, _ACCENT)
            lbl   = self.small.render(t_type.upper(), True, tc)
            self.screen.blit(lbl, (hx + CELL_W // 2 - lbl.get_width() // 2, hdr_y + 4))

        self._tea_codex_rects.clear()
        cy = hdr_y + HDR_H - self._tea_codex_scroll

        total_h   = len(BIOMES) * (CELL_H + GAP) + HDR_H
        visible_h = SCREEN_H - gy0 - 10
        self._max_tea_codex_scroll = max(0, total_h - visible_h)

        for biome in BIOMES:
            bnm = BIOME_DISPLAY_NAMES.get(biome, biome)
            bl  = self.font.render(bnm.upper(), True, (140, 200, 120))
            self.screen.blit(bl, (gx0 - bl.get_width() - 8, cy + (CELL_H - bl.get_height()) // 2))

            for ci, t_type in enumerate(TEA_TYPES):
                hx   = gx0 + ci * (CELL_W + GAP)
                key  = f"{biome}_{t_type}"
                disc = key in player.discovered_tea_origins
                rect = pygame.Rect(hx, cy, CELL_W, CELL_H)
                self._tea_codex_rects[key] = rect
                tc   = TEA_TYPE_COLORS.get(t_type, _ACCENT)
                sel  = (self._tea_codex_selected == key)

                if disc:
                    pygame.draw.rect(self.screen, _CELL_BG, rect)
                    pygame.draw.rect(self.screen, tc, rect, 3 if sel else 1)
                    # Best quality for this origin+type
                    best_q = max(
                        (x.steep_quality for x in player.tea_leaves
                         if x.origin_biome == biome and x.tea_type == t_type), default=0.0)
                    stars = "★" * round(best_q * 5) if best_q > 0 else "★"
                    nm_s  = self.small.render(
                        BIOME_DISPLAY_NAMES.get(biome, biome), True, tc)
                    ss_s  = self.small.render(stars, True, (220, 200, 80))
                    self.screen.blit(nm_s, (hx + 4, cy + 6))
                    self.screen.blit(ss_s, (hx + 4, cy + 26))
                    if sel:
                        buff_key = TEA_TYPE_BUFFS.get(t_type, "")
                        buff_desc = BUFF_DESCS.get(buff_key, "")
                        bs = self.small.render(buff_desc, True, (180, 230, 160))
                        self.screen.blit(bs, (hx + 4, cy + 44))
                else:
                    pygame.draw.rect(self.screen, (10, 20, 10), rect)
                    pygame.draw.rect(self.screen, _DIM_C, rect, 1)
                    lock = self.small.render("?", True, (30, 55, 30))
                    self.screen.blit(lock, (hx + CELL_W // 2 - lock.get_width() // 2,
                                            cy + CELL_H // 2 - lock.get_height() // 2))

            cy += CELL_H + GAP

        # Detail panel for selected discovered entry
        if self._tea_codex_selected:
            key = self._tea_codex_selected
            if key in player.discovered_tea_origins:
                parts   = key.rsplit("_", 1)
                if len(parts) == 2:
                    biome, t_type = parts
                    tc  = TEA_TYPE_COLORS.get(t_type, _ACCENT)
                    px0 = SCREEN_W - 300
                    py0 = gy0
                    pygame.draw.rect(self.screen, _DARK_BG, (px0, py0, 290, 260))
                    pygame.draw.rect(self.screen, tc, (px0, py0, 290, 260), 2)

                    iy = py0 + 10
                    def dline(txt, col=_TITLE_C):
                        nonlocal iy
                        s = self.small.render(txt, True, col)
                        self.screen.blit(s, (px0 + 10, iy))
                        iy += 18

                    dline(BIOME_DISPLAY_NAMES.get(biome, biome) + " — " + t_type.title(), tc)
                    dline(TEA_TYPE_DESCS.get(t_type, t_type), (180, 215, 160))
                    buff_key = TEA_TYPE_BUFFS.get(t_type, "")
                    dline("Buff: " + BUFF_DESCS.get(buff_key, ""), (160, 210, 140))
                    best_leaves = [x for x in player.tea_leaves
                                   if x.origin_biome == biome and x.tea_type == t_type]
                    if best_leaves:
                        best = max(best_leaves, key=lambda x: x.steep_quality)
                        dline(f"Best Quality: {'★' * round(best.steep_quality * 5)}", (220, 200, 80))
                        if best.flavor_notes:
                            dline("Notes:", _LABEL_C)
                            for note in best.flavor_notes[:3]:
                                dline(f"  • {note.title()}", _TITLE_C)
