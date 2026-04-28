"""SmithingMixin — Forge mini-game, Weapon Rack, Inspect, and Assembly Bench."""

import math
import pygame
from constants import SCREEN_W, SCREEN_H
from weapons import (
    WEAPON_TYPES, MATERIAL_PROFILES, PART_TEMPLATES, ASSEMBLY_HANDLES,
    WEAPON_TYPE_ORDER, MATERIAL_ORDER, WEAPON_STYLES, WEAPON_STYLE_ORDER,
    DECORATION_SLOTS, GEM_INLAY_ITEMS, GEM_RARITY_BONUS, SHELL_RARITY_BONUS,
    make_billet, calculate_part_quality, quality_tier,
    weapon_display_name, weapon_decoration_slots, effective_quality, weapon_damage,
    decoration_quality_bonus,
)

# ── Theme colours ──────────────────────────────────────────────────────────────
_ACCENT       = (220, 180, 100)
_DIM          = (140, 120,  90)
_BTN_BG       = ( 55,  45,  30)
_BTN_HL       = ( 80,  65,  40)
_BTN_DISABLED = ( 35,  30,  25)
_CELL_EXCESS  = (130, 135, 145)
_CELL_TARGET  = (175, 185, 200)
_CELL_REMOVED = ( 28,  22,  16)
_CELL_MISTAKE = (130,  30,  20)

SMITH_COLS = 16
SMITH_ROWS = 10


# ── Shared draw helpers ───────────────────────────────────────────────────────

def _draw_btn(surface, font, rect, label, enabled=True, hover=False):
    bg = _BTN_HL if (hover and enabled) else (_BTN_BG if enabled else _BTN_DISABLED)
    pygame.draw.rect(surface, bg, rect, border_radius=4)
    pygame.draw.rect(surface, _ACCENT if enabled else _DIM, rect, 1, border_radius=4)
    col = _ACCENT if enabled else _DIM
    txt = font.render(label, True, col)
    surface.blit(txt, txt.get_rect(center=rect.center))


def _temp_colour(t):
    if t >= 60:
        r, g, b = 255, int(140 * (t - 60) / 40), 0
    elif t >= 30:
        r, g, b = 210, int(70 * (t - 30) / 30), 0
    else:
        frac = t / 30.0
        r, g, b = int(90 + 120 * frac), int(90 * frac), int(100 * (1 - frac))
    return (min(255, r), min(255, g), min(255, b))


def _draw_temp_bar(surface, font, x, y, w, h, temp):
    pygame.draw.rect(surface, (30, 25, 20), (x, y, w, h))
    filled_h = int(h * temp / 100.0)
    col = _temp_colour(temp)
    if filled_h > 0:
        pygame.draw.rect(surface, col, (x, y + h - filled_h, w, filled_h))
    pygame.draw.rect(surface, _DIM, (x, y, w, h), 1)
    label = font.render(f"{int(temp)}°", True, col)
    surface.blit(label, (x + w // 2 - label.get_width() // 2, y - 18))


def _draw_quality_bar(surface, font, x, y, w, h, q, label="Quality"):
    fill = int(w * q)
    col = (80, 200, 80) if q >= 0.65 else ((220, 180, 50) if q >= 0.40 else (200, 60, 40))
    pygame.draw.rect(surface, (30, 25, 20), (x, y, w, h))
    if fill > 0:
        pygame.draw.rect(surface, col, (x, y, fill, h))
    pygame.draw.rect(surface, _DIM, (x, y, w, h), 1)
    if label:
        pct = font.render(f"{label}: {int(q * 100)}%  {quality_tier(q)}", True, col)
        surface.blit(pct, (x, y + h + 3))


def _draw_section(surface, font, x, y, w, label, col=None):
    col = col or _DIM
    lbl = font.render(f"─── {label} ───", True, col)
    surface.blit(lbl, (x + w // 2 - lbl.get_width() // 2, y))
    return y + lbl.get_height() + 6


# ── Mixin ─────────────────────────────────────────────────────────────────────

class SmithingMixin:

    # ── Per-frame update ──────────────────────────────────────────────────────

    def smith_update(self, dt, player):
        if self._smith_phase == "hammering" and self._smith_temperature > 0:
            self._smith_temperature = max(0.0, self._smith_temperature - 1.5 * dt)

    # ── Key handlers ──────────────────────────────────────────────────────────

    def handle_forge_keydown(self, key, player):
        if key == pygame.K_ESCAPE:
            if self._smith_phase in ("select", "idle"):
                self.refinery_open = False
                self._smith_phase = "idle"
            elif self._smith_phase == "heating":
                self._smith_phase = "select"
            elif self._smith_phase == "hammering":
                self._smith_phase = "heating"
            elif self._smith_phase == "quench":
                self._smith_phase = "hammering"
            elif self._smith_phase == "part_complete":
                self._smith_phase = "select"
        elif key == pygame.K_RETURN:
            if self._smith_phase == "hammering":
                self._finish_hammering(player)
        elif key == pygame.K_SPACE:
            if self._smith_phase == "heating":
                self._smith_temperature = min(100.0, self._smith_temperature + 5.0)

    def handle_forge_keys(self, keys, dt, player):
        if self._smith_phase == "heating" and keys[pygame.K_SPACE]:
            self._smith_temperature = min(100.0, self._smith_temperature + 5.0 * dt)

    # ── Mouse drag update for hammering ──────────────────────────────────────

    def smith_update_drag(self, mouse_pos, mouse_buttons):
        if self._smith_phase != "hammering":
            return
        self._smith_hover_cell = None
        for (r, c), rect in self._smith_cell_rects.items():
            if rect.collidepoint(mouse_pos):
                self._smith_hover_cell = (r, c)
                break
        if mouse_buttons[0] and self._smith_hover_cell and self._smith_temperature >= 20.0:
            r, c = self._smith_hover_cell
            cell = self._smith_grid[r][c]
            if cell == "excess":
                self._smith_grid[r][c] = "removed"
            elif cell == "target":
                self._smith_grid[r][c] = "mistake"
                self._smith_mistakes += 1
        else:
            self._smith_drag_mode = None

    # ═══════════════════════════════════════════════════════════════════════════
    # FORGE
    # ═══════════════════════════════════════════════════════════════════════════

    def _draw_forge(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("FORGE", True, _ACCENT)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 4))
        hint = self.small.render("ESC back  ·  ENTER confirm", True, _DIM)
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        if self._smith_phase == "idle":
            self._smith_phase = "select"

        dispatch = {
            "select":       self._draw_smith_select,
            "heating":      lambda p: self._draw_smith_heating(p, dt),
            "hammering":    self._draw_smith_hammering,
            "quench":       self._draw_smith_quench,
            "part_complete": self._draw_smith_part_complete,
        }
        draw_fn = dispatch.get(self._smith_phase)
        if draw_fn:
            draw_fn(player)

    # ── Phase: Select ─────────────────────────────────────────────────────────

    def _draw_smith_select(self, player):
        cx, cy = SCREEN_W // 2, SCREEN_H // 2

        # ── Tabs ──────────────────────────────────────────────────────────────
        tab = getattr(self, "_smith_tab", "smith")
        tab_w, tab_h = 160, 30
        smith_tab_r = pygame.Rect(cx - tab_w - 8, cy - 190, tab_w, tab_h)
        craft_tab_r = pygame.Rect(cx + 8,          cy - 190, tab_w, tab_h)
        self._smith_tab_btns = {"smith": smith_tab_r, "craft": craft_tab_r}
        for tid, tr in self._smith_tab_btns.items():
            selected = (tab == tid)
            label = "Smith a Part" if tid == "smith" else "Craft Handles"
            bg = _BTN_HL if selected else _BTN_BG
            pygame.draw.rect(self.screen, bg, tr, border_radius=4)
            pygame.draw.rect(self.screen, _ACCENT if selected else _DIM, tr, 1, border_radius=4)
            lbl = self.font.render(label, True, _ACCENT if selected else _DIM)
            self.screen.blit(lbl, lbl.get_rect(center=tr.center))

        if tab == "craft":
            self._draw_forge_craft_tab(player)
            return

        # ── Weapon type ────────────────────────────────────────────────────
        type_lbl = self.font.render("Weapon Type", True, _ACCENT)
        self.screen.blit(type_lbl, (cx - type_lbl.get_width() // 2, cy - 148))

        btn_w, btn_h, gap = 110, 32, 8
        total_w = len(WEAPON_TYPE_ORDER) * btn_w + (len(WEAPON_TYPE_ORDER) - 1) * gap
        tx0 = cx - total_w // 2
        self._smith_type_rects = {}
        for i, wt in enumerate(WEAPON_TYPE_ORDER):
            r = pygame.Rect(tx0 + i * (btn_w + gap), cy - 112, btn_w, btn_h)
            self._smith_type_rects[wt] = r
            selected = (self._smith_type == wt)
            bg = _BTN_HL if selected else _BTN_BG
            pygame.draw.rect(self.screen, bg, r, border_radius=4)
            pygame.draw.rect(self.screen, _ACCENT if selected else _DIM, r, 1, border_radius=4)
            lbl = self.font.render(WEAPON_TYPES[wt]["name"], True, _ACCENT if selected else _DIM)
            self.screen.blit(lbl, lbl.get_rect(center=r.center))

        # ── Material ────────────────────────────────────────────────────────
        mat_lbl = self.font.render("Material", True, _ACCENT)
        self.screen.blit(mat_lbl, (cx - mat_lbl.get_width() // 2, cy - 60))

        total_mw = len(MATERIAL_ORDER) * btn_w + (len(MATERIAL_ORDER) - 1) * gap
        mx0 = cx - total_mw // 2
        self._smith_mat_rects = {}
        for i, mat in enumerate(MATERIAL_ORDER):
            r = pygame.Rect(mx0 + i * (btn_w + gap), cy - 26, btn_w, btn_h)
            self._smith_mat_rects[mat] = r
            selected = (self._smith_material == mat)
            col = MATERIAL_PROFILES[mat]["color"]
            bg  = tuple(min(255, c + 30) for c in col) if selected else _BTN_BG
            pygame.draw.rect(self.screen, bg, r, border_radius=4)
            pygame.draw.rect(self.screen, col if selected else _DIM, r, 1, border_radius=4)
            lbl = self.font.render(MATERIAL_PROFILES[mat]["name"], True, col if selected else _DIM)
            self.screen.blit(lbl, lbl.get_rect(center=r.center))

        # ── Style ────────────────────────────────────────────────────────────
        style_lbl = self.font.render("Style", True, _ACCENT)
        self.screen.blit(style_lbl, (cx - style_lbl.get_width() // 2, cy + 20))

        style_w = 130
        total_sw = len(WEAPON_STYLE_ORDER) * style_w + (len(WEAPON_STYLE_ORDER) - 1) * gap
        sx0 = cx - total_sw // 2
        self._smith_style_rects = {}
        for i, sid in enumerate(WEAPON_STYLE_ORDER):
            r = pygame.Rect(sx0 + i * (style_w + gap), cy + 44, style_w, btn_h)
            self._smith_style_rects[sid] = r
            selected = (getattr(self, "_smith_style", "classic") == sid)
            sdata = WEAPON_STYLES[sid]
            bg = _BTN_HL if selected else _BTN_BG
            pygame.draw.rect(self.screen, bg, r, border_radius=4)
            pygame.draw.rect(self.screen, _ACCENT if selected else _DIM, r, 1, border_radius=4)
            lbl = self.font.render(sdata["name"], True, _ACCENT if selected else _DIM)
            self.screen.blit(lbl, lbl.get_rect(center=r.center))

        # Style description
        cur_style = WEAPON_STYLES.get(getattr(self, "_smith_style", "classic"), WEAPON_STYLES["classic"])
        desc_lbl = self.small.render(cur_style["desc"], True, _DIM)
        self.screen.blit(desc_lbl, (cx - desc_lbl.get_width() // 2, cy + 84))

        # ── Ingot requirement ─────────────────────────────────────────────────
        if self._smith_material:
            ingot_id   = MATERIAL_PROFILES[self._smith_material]["ingot_item"]
            inv_count  = player.inventory.get(ingot_id, 0)
            coal_count = player.inventory.get("coal", 0)
            ok = inv_count >= 1 and coal_count >= 1
            req_lbl = self.small.render(
                f"Requires: 1 {ingot_id.replace('_', ' ').title()}  (have {inv_count})  +  1 coal (have {coal_count})",
                True, _ACCENT if ok else (200, 60, 40))
            self.screen.blit(req_lbl, (cx - req_lbl.get_width() // 2, cy + 104))

        for mat_key, req_node in (("gold", "gold_smithing"), ("steel", "steel_forging")):
            if self._smith_material == mat_key:
                research = getattr(self, "_research", None)
                if research and not getattr(research.nodes.get(req_node), "unlocked", False):
                    lock_lbl = self.small.render(
                        f"Requires: {req_node.replace('_', ' ').title()} research", True, (200, 80, 50))
                    self.screen.blit(lock_lbl, (cx - lock_lbl.get_width() // 2, cy + 120))

        # ── Begin Forging ─────────────────────────────────────────────────────
        can_start = (self._smith_type is not None and self._smith_material is not None and
                     player.inventory.get(MATERIAL_PROFILES.get(self._smith_material, {}).get("ingot_item", ""), 0) >= 1 and
                     player.inventory.get("coal", 0) >= 1)
        if self._smith_material in ("gold", "steel"):
            research = getattr(self, "_research", None)
            req = "gold_smithing" if self._smith_material == "gold" else "steel_forging"
            if research and not getattr(research.nodes.get(req), "unlocked", False):
                can_start = False

        btn_r = pygame.Rect(cx - 90, cy + 140, 180, 36)
        self._smith_begin_btn = btn_r
        _draw_btn(self.screen, self.font, btn_r, "Begin Forging", enabled=can_start,
                  hover=btn_r.collidepoint(pygame.mouse.get_pos()))

    # ── Forge craft tab (handles) ─────────────────────────────────────────────

    def _draw_forge_craft_tab(self, player):
        from crafting import SMITHING_FORGE_RECIPES
        cx, cy = SCREEN_W // 2, SCREEN_H // 2
        self._forge_craft_rects = {}
        COL_W, ROW_H, GAP = 300, 48, 8
        cols = 2
        total_w = cols * COL_W + (cols - 1) * GAP
        x0 = cx - total_w // 2
        y0 = cy - 130
        for i, recipe in enumerate(SMITHING_FORGE_RECIPES):
            col, row = i % cols, i // cols
            rx = x0 + col * (COL_W + GAP)
            ry = y0 + row * (ROW_H + GAP)
            r = pygame.Rect(rx, ry, COL_W, ROW_H)
            self._forge_craft_rects[i] = r
            can_craft = all(player.inventory.get(ing, 0) >= cnt
                            for ing, cnt in recipe["ingredients"].items())
            bg = _BTN_HL if can_craft else _BTN_BG
            pygame.draw.rect(self.screen, bg, r, border_radius=4)
            pygame.draw.rect(self.screen, _ACCENT if can_craft else _DIM, r, 1, border_radius=4)
            name_lbl = self.font.render(recipe["name"], True, _ACCENT if can_craft else _DIM)
            self.screen.blit(name_lbl, (rx + 8, ry + 5))
            ing_parts = [f"{ing.replace('_', ' ').title()} ×{cnt} ({player.inventory.get(ing, 0)})"
                         for ing, cnt in recipe["ingredients"].items()]
            ing_lbl = self.small.render("  ·  ".join(ing_parts), True, _ACCENT if can_craft else (100, 85, 65))
            self.screen.blit(ing_lbl, (rx + 8, ry + 26))

    # ── Phase: Heating ────────────────────────────────────────────────────────

    def _draw_smith_heating(self, player, dt):
        cx, cy = SCREEN_W // 2, SCREEN_H // 2
        t = pygame.time.get_ticks() / 1000.0
        for i in range(5):
            flicker = math.sin(t * 4 + i * 1.3) * 0.5 + 0.5
            fw, fh = int(30 + flicker * 20), int(60 + flicker * 30)
            fx = cx - 60 + i * 28 - fw // 2
            fy = cy - 20 - fh
            col = (255, int(80 + 120 * flicker), 0)
            pygame.draw.ellipse(self.screen, col, (fx, fy, fw, fh))

        mat_col = MATERIAL_PROFILES.get(self._smith_material or "iron", {}).get("color", (160, 165, 175))
        pygame.draw.rect(self.screen, mat_col, (cx - 40, cy - 10, 80, 30))
        lbl = self.font.render("⬛ Metal Billet", True, mat_col)
        self.screen.blit(lbl, (cx - lbl.get_width() // 2, cy + 28))
        _draw_temp_bar(self.screen, self.small, cx + 60, cy - 80, 20, 100, self._smith_temperature)
        hint = self.small.render("Hold SPACE to pump bellows · Need 80°+ to hammer", True, _DIM)
        self.screen.blit(hint, (cx - hint.get_width() // 2, cy + 68))
        coal_lbl = self.small.render(f"Coal: {player.inventory.get('coal', 0)}", True, _DIM)
        self.screen.blit(coal_lbl, (cx - coal_lbl.get_width() // 2, cy + 86))
        can_hammer = self._smith_temperature >= 80.0
        btn = pygame.Rect(cx - 90, cy + 110, 180, 34)
        self._smith_hammer_btn = btn
        _draw_btn(self.screen, self.font, btn, "Start Hammering", enabled=can_hammer,
                  hover=btn.collidepoint(pygame.mouse.get_pos()))

    # ── Phase: Hammering ──────────────────────────────────────────────────────

    def _draw_smith_hammering(self, player):
        self._smith_cell_rects.clear()
        mat, mat_col = self._smith_material or "iron", None
        mat_col = MATERIAL_PROFILES[mat]["color"]
        temp = self._smith_temperature
        temp_col = _temp_colour(temp)

        avail_h = SCREEN_H - 110
        avail_w = SCREEN_W - 240
        cs = max(6, min(avail_w // SMITH_COLS, avail_h // SMITH_ROWS))
        grid_w, grid_h = SMITH_COLS * cs, SMITH_ROWS * cs
        PANEL_W = 200
        PANEL_X = SCREEN_W - PANEL_W - 12
        gx = max(10, (PANEL_X - grid_w) // 2)
        gy = 48

        for r in range(SMITH_ROWS):
            for c in range(SMITH_COLS):
                cr = pygame.Rect(gx + c * cs, gy + r * cs, cs, cs)
                state  = self._smith_grid[r][c]
                target = self._smith_target[r][c]
                hover  = (self._smith_hover_cell == (r, c))
                if state == "removed":
                    col = _CELL_REMOVED
                elif state == "mistake":
                    col = _CELL_MISTAKE
                elif state == "target":
                    blend = min(1.0, temp / 100.0) * 0.4
                    col = tuple(int(mat_col[i] * (1 - blend) + temp_col[i] * blend) for i in range(3))
                else:
                    col = _CELL_EXCESS
                if hover and temp >= 20.0 and state in ("excess", "target"):
                    col = tuple(min(255, v + 40) for v in col)
                pygame.draw.rect(self.screen, col, cr)
                if not target and state == "excess":
                    pygame.draw.rect(self.screen, (80, 85, 90), cr, 1)
                elif target and state == "target":
                    pygame.draw.rect(self.screen, tuple(min(255, v + 30) for v in col), cr, 1)
                elif target and state in ("excess", "removed", "mistake"):
                    pygame.draw.rect(self.screen, (100, 140, 180), cr, 1)
                else:
                    pygame.draw.rect(self.screen, (50, 50, 55), cr, 1)
                self._smith_cell_rects[(r, c)] = cr

        pygame.draw.rect(self.screen, mat_col, (gx - 2, gy - 2, grid_w + 4, grid_h + 4), 2)

        px2, py2 = PANEL_X, gy
        _draw_temp_bar(self.screen, self.small, px2, py2, 22, 100, temp)
        py2 += 110
        mis_lbl = self.small.render(f"Mistakes: {self._smith_mistakes}", True,
                                    (200, 60, 40) if self._smith_mistakes else _DIM)
        self.screen.blit(mis_lbl, (px2, py2)); py2 += 20
        total_excess = sum(1 for r in range(SMITH_ROWS) for c in range(SMITH_COLS) if not self._smith_target[r][c])
        removed = sum(1 for r in range(SMITH_ROWS) for c in range(SMITH_COLS) if self._smith_grid[r][c] == "removed")
        self.screen.blit(self.small.render(f"Shaped: {removed}/{total_excess}", True, _ACCENT), (px2, py2)); py2 += 22
        if temp < 30:
            self.screen.blit(self.small.render("Too cold!", True, (200, 80, 50)), (px2, py2)); py2 += 18
        reheat_r = pygame.Rect(px2, py2 + 4, 120, 30)
        self._smith_reheat_btn = reheat_r
        _draw_btn(self.screen, self.small, reheat_r, "Reheat (1 coal)",
                  enabled=temp < 30 and player.inventory.get("coal", 0) >= 1,
                  hover=reheat_r.collidepoint(pygame.mouse.get_pos()))
        py2 += 42
        finish_r = pygame.Rect(px2, py2, 120, 30)
        self._smith_finish_btn = finish_r
        _draw_btn(self.screen, self.small, finish_r, "Finish Part",
                  hover=finish_r.collidepoint(pygame.mouse.get_pos()))
        part_key = self._smith_current_part()
        part_lbl = self.font.render(
            f"{MATERIAL_PROFILES[mat]['name']} {part_key.replace('_', ' ').title()}", True, mat_col)
        self.screen.blit(part_lbl, (gx, gy - 20))
        hint = self.small.render("Click to hammer cells  ·  ESC reheat  ·  ENTER finish", True, _DIM)
        self.screen.blit(hint, (gx, gy + grid_h + 8))

    # ── Phase: Quench ─────────────────────────────────────────────────────────

    def _draw_smith_quench(self, player):
        cx, cy = SCREEN_W // 2, SCREEN_H // 2
        lbl = self.font.render("Quench the Part", True, _ACCENT)
        self.screen.blit(lbl, (cx - lbl.get_width() // 2, cy - 80))
        desc = self.small.render("Choose how to cool the metal — affects final quality.", True, _DIM)
        self.screen.blit(desc, (cx - desc.get_width() // 2, cy - 52))
        w_btn = pygame.Rect(cx - 170, cy - 10, 150, 40)
        a_btn = pygame.Rect(cx + 20,  cy - 10, 150, 40)
        self._smith_quench_water_btn = w_btn
        self._smith_quench_air_btn   = a_btn
        _draw_btn(self.screen, self.font, w_btn, "Water Quench",
                  hover=w_btn.collidepoint(pygame.mouse.get_pos()))
        _draw_btn(self.screen, self.font, a_btn, "Air Cool",
                  hover=a_btn.collidepoint(pygame.mouse.get_pos()))
        self.screen.blit(self.small.render("+0.05 quality bonus", True, (100, 200, 230)), (cx - 170, cy + 36))
        self.screen.blit(self.small.render("No bonus, but safer", True, _DIM), (cx + 20, cy + 36))

    # ── Phase: Part Complete ──────────────────────────────────────────────────

    def _draw_smith_part_complete(self, player):
        cx, cy = SCREEN_W // 2, SCREEN_H // 2
        lbl = self.font.render("Part Complete!", True, (100, 220, 100))
        self.screen.blit(lbl, (cx - lbl.get_width() // 2, cy - 110))
        quality = self._smith_part_quality[-1] if self._smith_part_quality else 0.0
        _draw_quality_bar(self.screen, self.small, cx - 150, cy - 76, 300, 18, quality)
        wtype    = self._smith_type or "sword"
        mat      = self._smith_material or "iron"
        style_id = getattr(self, "_smith_style", "classic")
        part_key = WEAPON_TYPES[wtype]["parts"][0]
        mat_col  = MATERIAL_PROFILES[mat]["color"]
        style    = WEAPON_STYLES.get(style_id, WEAPON_STYLES["classic"])
        pname_lbl = self.font.render(
            f"{MATERIAL_PROFILES[mat]['name']} {style['name']} {part_key.replace('_', ' ').title()}",
            True, mat_col)
        self.screen.blit(pname_lbl, (cx - pname_lbl.get_width() // 2, cy - 38))
        hint = self.small.render("Take this part to the Assembly Bench to finish the weapon.", True, _DIM)
        self.screen.blit(hint, (cx - hint.get_width() // 2, cy - 6))
        take_r = pygame.Rect(cx - 100, cy + 30, 200, 38)
        self._smith_take_part_btn = take_r
        _draw_btn(self.screen, self.font, take_r, "Take Part",
                  hover=take_r.collidepoint(pygame.mouse.get_pos()))

    # ═══════════════════════════════════════════════════════════════════════════
    # ASSEMBLY BENCH
    # ═══════════════════════════════════════════════════════════════════════════

    def _draw_assembly_bench(self, player):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        self.screen.blit(overlay, (0, 0))
        title = self.font.render("ASSEMBLY BENCH", True, _ACCENT)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 4))
        self.screen.blit(self.small.render("ESC close", True, _DIM), (SCREEN_W - 80, 6))

        smithed = getattr(player, "smithed_parts", [])
        if not smithed:
            lbl = self.font.render("No smithed parts. Use the Forge to smith weapon parts.", True, _DIM)
            self.screen.blit(lbl, (SCREEN_W // 2 - lbl.get_width() // 2, SCREEN_H // 2))
            return

        ROW_H, ROW_GAP = 72, 6
        LIST_Y = 36
        scroll = getattr(self, "_bench_scroll", 0)
        self._bench_assemble_btns = {}

        for i, part in enumerate(smithed):
            row_y = LIST_Y + i * (ROW_H + ROW_GAP) - scroll
            if row_y + ROW_H < 0 or row_y > SCREEN_H:
                continue
            wtype, mat, part_key = part["weapon_type"], part["material"], part["part_key"]
            quality  = part["quality"]
            style_id = part.get("style", "classic")
            handle_id    = ASSEMBLY_HANDLES.get(wtype, "")
            handle_count = player.inventory.get(handle_id, 0)
            can_assemble = handle_count > 0
            mat_col = MATERIAL_PROFILES.get(mat, {}).get("color", _ACCENT)
            row_r   = pygame.Rect(40, row_y, SCREEN_W - 220, ROW_H)
            bg = (42, 32, 18) if can_assemble else (28, 22, 16)
            pygame.draw.rect(self.screen, bg, row_r, border_radius=4)
            pygame.draw.rect(self.screen, mat_col if can_assemble else _DIM, row_r, 1, border_radius=4)
            style_name = WEAPON_STYLES.get(style_id, WEAPON_STYLES["classic"])["name"]
            name_lbl = self.font.render(
                f"{MATERIAL_PROFILES[mat]['name']} {style_name} {part_key.replace('_', ' ').title()}",
                True, mat_col)
            self.screen.blit(name_lbl, (row_r.x + 10, row_y + 5))
            _draw_quality_bar(self.screen, self.small, row_r.x + 10, row_y + 30, 180, 10, quality, label="")
            tier_lbl = self.small.render(f"  {quality_tier(quality)}  {int(quality * 100)}%", True, mat_col)
            self.screen.blit(tier_lbl, (row_r.x + 194, row_y + 28))
            h_lbl = self.small.render(
                f"Needs: {handle_id.replace('_', ' ').title()}  (have {handle_count})",
                True, _ACCENT if can_assemble else (200, 60, 40))
            self.screen.blit(h_lbl, (row_r.x + 10, row_y + 50))
            btn_r = pygame.Rect(row_r.right + 10, row_y + (ROW_H - 34) // 2, 150, 34)
            self._bench_assemble_btns[i] = btn_r
            _draw_btn(self.screen, self.font, btn_r, "Assemble", enabled=can_assemble,
                      hover=btn_r.collidepoint(pygame.mouse.get_pos()))

        if len(smithed) * (ROW_H + ROW_GAP) > SCREEN_H - LIST_Y:
            self.screen.blit(self.small.render("Scroll to see more", True, _DIM),
                             (SCREEN_W // 2 - 50, SCREEN_H - 20))

    # ═══════════════════════════════════════════════════════════════════════════
    # WEAPON RACK
    # ═══════════════════════════════════════════════════════════════════════════

    def _draw_weapon_rack(self, player):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        self.screen.blit(overlay, (0, 0))
        title = self.font.render("WEAPON RACK", True, _ACCENT)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        self.screen.blit(self.small.render("ESC close", True, _DIM), (SCREEN_W - 80, 8))

        # If inspect panel is open, draw it on top
        if getattr(self, "_inspect_weapon_uid", None):
            self._draw_weapon_inspect(player)
            return

        if not player.crafted_weapons:
            lbl = self.font.render("No weapons crafted yet.", True, _DIM)
            self.screen.blit(lbl, (SCREEN_W // 2 - lbl.get_width() // 2, SCREEN_H // 2))
            return

        ROW_H  = 56
        LIST_Y = 36
        LIST_X = 60
        self._rack_weapon_rects    = {}
        self._rack_equip_btn_rects = {}
        self._rack_inspect_btns    = {}

        for i, w in enumerate(player.crafted_weapons):
            row_y = LIST_Y + i * ROW_H - self._rack_scroll
            if row_y + ROW_H < 0 or row_y > SCREEN_H:
                continue
            row_r = pygame.Rect(LIST_X, row_y, SCREEN_W - LIST_X * 2 - 260, ROW_H - 4)
            self._rack_weapon_rects[w.uid] = row_r
            equipped = (player.equipped_weapon_uid == w.uid)
            bg = (50, 40, 28) if equipped else (35, 30, 22)
            pygame.draw.rect(self.screen, bg, row_r, border_radius=4)
            pygame.draw.rect(self.screen, _ACCENT if equipped else _DIM, row_r, 1, border_radius=4)
            mat_col = MATERIAL_PROFILES.get(w.material, {}).get("color", _ACCENT)
            self.screen.blit(self.font.render(weapon_display_name(w), True, mat_col),
                             (row_r.x + 8, row_y + 4))
            tier = quality_tier(effective_quality(w))
            self.screen.blit(self.small.render(tier, True, mat_col), (row_r.x + 8, row_y + 26))
            _draw_quality_bar(self.screen, self.small, row_r.x + 120, row_y + 28, 120, 10,
                              effective_quality(w), label="")
            # Decoration dots
            if w.decorations:
                dx = row_r.x + 260
                for dec in w.decorations[:4]:
                    item_id = dec.get("item_id", "")
                    dot_col = GEM_INLAY_ITEMS.get(item_id, {}).get("color") or (180, 160, 120)
                    pygame.draw.circle(self.screen, dot_col, (dx, row_y + 26), 5)
                    dx += 14

            equip_r = pygame.Rect(row_r.right + 8, row_y + 4, 100, 26)
            insp_r  = pygame.Rect(row_r.right + 8, row_y + 34, 100, 18)
            self._rack_equip_btn_rects[w.uid] = equip_r
            self._rack_inspect_btns[w.uid]    = insp_r
            _draw_btn(self.screen, self.small, equip_r, "Unequip" if equipped else "Equip",
                      hover=equip_r.collidepoint(pygame.mouse.get_pos()))
            _draw_btn(self.screen, self.small, insp_r, "Inspect",
                      hover=insp_r.collidepoint(pygame.mouse.get_pos()))

        if len(player.crafted_weapons) > 8:
            self.screen.blit(self.small.render("Scroll to see more", True, _DIM),
                             (SCREEN_W // 2 - 50, SCREEN_H - 20))

    # ═══════════════════════════════════════════════════════════════════════════
    # WEAPON INSPECT PANEL
    # ═══════════════════════════════════════════════════════════════════════════

    def _draw_weapon_inspect(self, player):
        weapon = next((w for w in player.crafted_weapons
                       if w.uid == self._inspect_weapon_uid), None)
        if weapon is None:
            self._inspect_weapon_uid = None
            return

        # If picker is open, show it instead
        if getattr(self, "_inspect_picking_slot", None):
            self._draw_decoration_picker(player, weapon)
            return

        # ── Panel background ──────────────────────────────────────────────────
        PW, PH = 700, 520
        px = (SCREEN_W - PW) // 2
        py = (SCREEN_H - PH) // 2
        pygame.draw.rect(self.screen, (22, 16, 10), (px, py, PW, PH), border_radius=8)
        mat_col = MATERIAL_PROFILES.get(weapon.material, {}).get("color", _ACCENT)
        pygame.draw.rect(self.screen, mat_col, (px, py, PW, PH), 2, border_radius=8)
        pygame.draw.rect(self.screen, mat_col, (px, py, PW, 40), border_top_left_radius=8, border_top_right_radius=8)

        # Title bar
        title = self.font.render(weapon_display_name(weapon), True, (20, 12, 6))
        self.screen.blit(title, (px + PW // 2 - title.get_width() // 2, py + 8))
        close_r = pygame.Rect(px + PW - 36, py + 6, 28, 28)
        self._inspect_close_btn = close_r
        _draw_btn(self.screen, self.small, close_r, "✕",
                  hover=close_r.collidepoint(pygame.mouse.get_pos()))

        y = py + 50
        cx_p = px + PW // 2

        # ── Quality breakdown ─────────────────────────────────────────────────
        eq   = effective_quality(weapon)
        dec_bonus = decoration_quality_bonus(weapon)
        style_mod = WEAPON_STYLES.get(weapon.style, WEAPON_STYLES["classic"])["quality_mod"]

        _draw_quality_bar(self.screen, self.small, px + 20, y, PW - 40, 14, eq, label="")
        q_parts = [f"Base {int(weapon.quality * 100)}%"]
        if style_mod != 0:
            q_parts.append(f"Style {'+' if style_mod >= 0 else ''}{int(style_mod * 100)}%")
        if dec_bonus > 0:
            q_parts.append(f"Decorations +{int(dec_bonus * 100)}%")
        q_parts.append(f"→ Effective {int(eq * 100)}%  ({quality_tier(eq)})")
        q_str = self.small.render("  ".join(q_parts), True, mat_col)
        self.screen.blit(q_str, (px + 20, y + 18))
        y += 38

        # ── Combat stats ──────────────────────────────────────────────────────
        y = _draw_section(self.screen, self.small, px + 20, y, PW - 40, "Combat Stats", _ACCENT)
        wt = WEAPON_TYPES[weapon.weapon_type]
        dmg = weapon_damage(weapon)
        spd = 1.0 / wt["cooldown"]
        stats = (f"Damage: {dmg:.2f}     Range: {wt['attack_range']} block{'s' if wt['attack_range'] > 1 else ''}     "
                 f"Speed: {spd:.1f}/s     Cooldown: {wt['cooldown']:.2f}s")
        self.screen.blit(self.small.render(stats, True, _ACCENT), (px + 20, y))
        y += 20
        style_data = WEAPON_STYLES.get(weapon.style, WEAPON_STYLES["classic"])
        style_lbl = self.small.render(
            f"Style: {style_data['name']}  ·  {style_data['desc']}", True, _DIM)
        self.screen.blit(style_lbl, (px + 20, y))
        y += 26

        # ── Decorations ───────────────────────────────────────────────────────
        y = _draw_section(self.screen, self.small, px + 20, y, PW - 40, "Decorations", _ACCENT)
        dec_map = {d["slot"]: d for d in weapon.decorations}
        slots   = weapon_decoration_slots(weapon)
        self._inspect_add_btns    = {}
        self._inspect_remove_btns = {}

        for slot_key in slots:
            slot_data  = DECORATION_SLOTS.get(slot_key) or {"label": "Blade", "type": "gem"}
            slot_label = slot_data["label"]
            dec = dec_map.get(slot_key)

            # Slot label
            sl_lbl = self.small.render(f"[{slot_label}]", True, mat_col)
            self.screen.blit(sl_lbl, (px + 20, y))

            if dec:
                item_id  = dec.get("item_id", "")
                rarity   = dec.get("rarity", "common")
                gem_data = GEM_INLAY_ITEMS.get(item_id, {})
                if dec.get("type") == "gem" and gem_data:
                    dot_col  = gem_data["color"]
                    cut_str  = f"  ·  {dec['cut'].title()}" if dec.get("cut") else ""
                    bonus    = GEM_RARITY_BONUS.get(rarity, 0.01)
                    dec_name = f"{gem_data['name']} ({rarity.title()}){cut_str}  +{int(bonus * 100)}% quality"
                else:
                    dot_col  = (200, 180, 140)
                    dec_name = f"{dec.get('name', 'Shell')}  (+{int(SHELL_RARITY_BONUS.get(rarity, 0.01) * 100)}% quality)"
                pygame.draw.circle(self.screen, dot_col, (px + 110, y + 8), 6)
                dec_lbl = self.small.render(dec_name, True, (200, 200, 180))
                self.screen.blit(dec_lbl, (px + 124, y))
                rm_r = pygame.Rect(px + PW - 110, y - 2, 80, 22)
                self._inspect_remove_btns[slot_key] = rm_r
                _draw_btn(self.screen, self.small, rm_r, "Remove",
                          hover=rm_r.collidepoint(pygame.mouse.get_pos()))
            else:
                empty_lbl = self.small.render("Empty", True, _DIM)
                self.screen.blit(empty_lbl, (px + 110, y))
                type_label = "Gem" if slot_data["type"] == "gem" else "Shell"
                add_r = pygame.Rect(px + PW - 110, y - 2, 80, 22)
                self._inspect_add_btns[slot_key] = add_r
                _draw_btn(self.screen, self.small, add_r, f"Add {type_label}",
                          hover=add_r.collidepoint(pygame.mouse.get_pos()))
            y += 30

        # ── Rename ────────────────────────────────────────────────────────────
        y = max(y, py + PH - 60)
        self._inspect_rename_btn = pygame.Rect(px + 20, y, 120, 30)
        _draw_btn(self.screen, self.small, self._inspect_rename_btn, "Rename",
                  hover=self._inspect_rename_btn.collidepoint(pygame.mouse.get_pos()))

    # ── Decoration Picker ─────────────────────────────────────────────────────

    def _draw_decoration_picker(self, player, weapon):
        slot_key  = self._inspect_picking_slot
        slot_data = DECORATION_SLOTS.get(slot_key) or {"label": "Blade", "type": "gem"}
        is_gem    = slot_data["type"] == "gem"

        PW, PH = 560, 460
        px = (SCREEN_W - PW) // 2
        py = (SCREEN_H - PH) // 2
        pygame.draw.rect(self.screen, (18, 14, 8), (px, py, PW, PH), border_radius=8)
        mat_col = MATERIAL_PROFILES.get(weapon.material, {}).get("color", _ACCENT)
        pygame.draw.rect(self.screen, mat_col, (px, py, PW, PH), 2, border_radius=8)

        title = self.font.render(
            f"Choose {'Gem' if is_gem else 'Shell'} — {slot_data['label']} Slot", True, _ACCENT)
        self.screen.blit(title, (px + PW // 2 - title.get_width() // 2, py + 10))

        cancel_r = pygame.Rect(px + PW - 36, py + 8, 28, 28)
        self._picker_cancel_btn = cancel_r
        _draw_btn(self.screen, self.small, cancel_r, "✕",
                  hover=cancel_r.collidepoint(pygame.mouse.get_pos()))

        self._picker_item_rects = {}
        ROW_H = 40
        COLS   = 2
        COL_W  = (PW - 50) // COLS
        scroll = getattr(self, "_picker_scroll", 0)
        y0     = py + 50

        if is_gem:
            # Group player.gems by gem_type, tracking best rarity and total count
            gems = getattr(player, "gems", [])
            rarity_order = list(GEM_RARITY_BONUS.keys())  # common … legendary

            grouped: dict[str, dict] = {}
            for g in gems:
                if g.gem_type not in grouped:
                    grouped[g.gem_type] = {"count": 0, "best": g, "gem_type": g.gem_type}
                grouped[g.gem_type]["count"] += 1
                cur_best = grouped[g.gem_type]["best"]
                if rarity_order.index(g.rarity) > rarity_order.index(cur_best.rarity):
                    grouped[g.gem_type]["best"] = g

            if not grouped:
                no_lbl = self.font.render("No gems in collection yet.", True, _DIM)
                self.screen.blit(no_lbl, (px + PW // 2 - no_lbl.get_width() // 2, py + PH // 2))
            else:
                entries = sorted(grouped.values(),
                                 key=lambda e: rarity_order.index(e["best"].rarity), reverse=True)
                for i, entry in enumerate(entries):
                    col = i % COLS
                    row = i // COLS
                    rx  = px + 20 + col * (COL_W + 10)
                    ry  = y0 + row * (ROW_H + 6) - scroll
                    if ry + ROW_H < py + 44 or ry > py + PH - 10:
                        continue
                    r = pygame.Rect(rx, ry, COL_W, ROW_H)
                    self._picker_item_rects[entry["gem_type"]] = r

                    best     = entry["best"]
                    gem_data = GEM_INLAY_ITEMS.get(best.gem_type, {})
                    gem_col  = best.primary_color[:3]
                    bonus    = GEM_RARITY_BONUS.get(best.rarity, 0.01)

                    pygame.draw.rect(self.screen, _BTN_HL, r, border_radius=4)
                    pygame.draw.rect(self.screen, gem_col, r, 1, border_radius=4)
                    pygame.draw.circle(self.screen, gem_col, (r.x + 14, r.centery), 8)
                    name_lbl = self.small.render(gem_data.get("name", best.gem_type), True, gem_col)
                    self.screen.blit(name_lbl, (r.x + 28, r.y + 4))
                    detail = self.small.render(
                        f"{best.rarity.title()}  ·  +{int(bonus * 100)}%  ·  ×{entry['count']}",
                        True, _ACCENT)
                    self.screen.blit(detail, (r.x + 28, r.y + 22))
        else:
            # Shell picker — from player.seashells
            shells = getattr(player, "seashells", [])
            if not shells:
                no_lbl = self.font.render("No seashells in collection.", True, _DIM)
                self.screen.blit(no_lbl, (px + PW // 2 - no_lbl.get_width() // 2, py + PH // 2))
            else:
                rarity_order = list(SHELL_RARITY_BONUS.keys())
                seen: dict = {}
                for s in shells:
                    if s.species not in seen or (
                            rarity_order.index(s.rarity) > rarity_order.index(seen[s.species].rarity)):
                        seen[s.species] = s
                for i, (species, shell) in enumerate(list(seen.items())[:16]):
                    col = i % COLS
                    row = i // COLS
                    rx  = px + 20 + col * (COL_W + 10)
                    ry  = y0 + row * (ROW_H + 6) - scroll
                    if ry + ROW_H < py + 44 or ry > py + PH - 10:
                        continue
                    r = pygame.Rect(rx, ry, COL_W, ROW_H)
                    self._picker_item_rects[species] = r
                    shell_col = tuple(min(255, int(v * 1.1)) for v in shell.color[:3])
                    pygame.draw.rect(self.screen, _BTN_HL, r, border_radius=4)
                    pygame.draw.rect(self.screen, shell_col, r, 1, border_radius=4)
                    pygame.draw.circle(self.screen, shell_col, (r.x + 14, r.centery), 8)
                    name_lbl = self.small.render(species.replace("_", " ").title(), True, shell_col)
                    self.screen.blit(name_lbl, (r.x + 28, r.y + 4))
                    bonus = SHELL_RARITY_BONUS.get(shell.rarity, 0.01)
                    detail = self.small.render(
                        f"{shell.rarity.title()}  ·  +{int(bonus * 100)}%  ·  {shell.pattern}",
                        True, _ACCENT)
                    self.screen.blit(detail, (r.x + 28, r.y + 22))

    # ── HUD ───────────────────────────────────────────────────────────────────

    def draw_smith_hud(self, player):
        if not player.equipped_weapon_uid:
            return
        weapon = next((w for w in player.crafted_weapons if w.uid == player.equipped_weapon_uid), None)
        if weapon is None:
            return
        mat_col = MATERIAL_PROFILES.get(weapon.material, {}).get("color", _ACCENT)
        lbl = self.small.render(f"⚔ {weapon_display_name(weapon)}", True, mat_col)
        self.screen.blit(lbl, (8, SCREEN_H - lbl.get_height() - 26))

    # ═══════════════════════════════════════════════════════════════════════════
    # CLICK HANDLERS
    # ═══════════════════════════════════════════════════════════════════════════

    def _handle_forge_click(self, pos, player):
        phase = self._smith_phase
        if phase == "select":
            for tid, r in getattr(self, "_smith_tab_btns", {}).items():
                if r.collidepoint(pos):
                    self._smith_tab = tid
                    return
            tab = getattr(self, "_smith_tab", "smith")
            if tab == "craft":
                self._handle_forge_craft_click(pos, player)
                return
            for wt, r in getattr(self, "_smith_type_rects", {}).items():
                if r.collidepoint(pos):
                    self._smith_type = wt; return
            for mat, r in getattr(self, "_smith_mat_rects", {}).items():
                if r.collidepoint(pos):
                    self._smith_material = mat; return
            for sid, r in getattr(self, "_smith_style_rects", {}).items():
                if r.collidepoint(pos):
                    self._smith_style = sid; return
            if hasattr(self, "_smith_begin_btn") and self._smith_begin_btn.collidepoint(pos):
                self._start_heating(player)

        elif phase == "heating":
            if hasattr(self, "_smith_hammer_btn") and self._smith_hammer_btn.collidepoint(pos):
                if self._smith_temperature >= 80.0:
                    self._start_hammering()

        elif phase == "hammering":
            if hasattr(self, "_smith_finish_btn") and self._smith_finish_btn.collidepoint(pos):
                self._finish_hammering(player); return
            if hasattr(self, "_smith_reheat_btn") and self._smith_reheat_btn.collidepoint(pos):
                if self._smith_temperature < 30.0 and player.inventory.get("coal", 0) >= 1:
                    player.inventory["coal"] -= 1
                    self._smith_temperature = min(100.0, self._smith_temperature + 40.0)
                    self._smith_phase = "heating"; return

        elif phase == "quench":
            if hasattr(self, "_smith_quench_water_btn") and self._smith_quench_water_btn.collidepoint(pos):
                self._apply_quench(0.05, player)
            elif hasattr(self, "_smith_quench_air_btn") and self._smith_quench_air_btn.collidepoint(pos):
                self._apply_quench(0.0, player)

        elif phase == "part_complete":
            if hasattr(self, "_smith_take_part_btn") and self._smith_take_part_btn.collidepoint(pos):
                self._do_take_part(player)

    def _handle_forge_craft_click(self, pos, player):
        from crafting import SMITHING_FORGE_RECIPES
        for i, r in getattr(self, "_forge_craft_rects", {}).items():
            if not r.collidepoint(pos):
                continue
            recipe = SMITHING_FORGE_RECIPES[i]
            if not all(player.inventory.get(ing, 0) >= cnt for ing, cnt in recipe["ingredients"].items()):
                return
            for ing, cnt in recipe["ingredients"].items():
                player.inventory[ing] -= cnt
            out = recipe["output_id"]
            player.inventory[out] = player.inventory.get(out, 0) + recipe["output_count"]
            player.pending_notifications.append(("Forge", f"Crafted: {recipe['name']}", None))
            return

    def _handle_assembly_bench_click(self, pos, player):
        for i, rect in getattr(self, "_bench_assemble_btns", {}).items():
            if not rect.collidepoint(pos):
                continue
            smithed = getattr(player, "smithed_parts", [])
            if i >= len(smithed):
                return
            part      = smithed[i]
            wtype     = part["weapon_type"]
            mat       = part["material"]
            style_id  = part.get("style", "classic")
            handle_id = ASSEMBLY_HANDLES.get(wtype, "")
            if player.inventory.get(handle_id, 0) < 1:
                return
            player.inventory[handle_id] -= 1
            player.smithed_parts.pop(i)
            weapon = player._weapon_gen.new_weapon(wtype, mat, style=style_id)
            weapon.parts_quality = [part["quality"]]
            bonus = getattr(player, "smith_quality_bonus", 0.0)
            weapon.quality = round(min(1.0, part["quality"] + bonus), 3)
            player.crafted_weapons.append(weapon)
            player.pending_notifications.append(
                ("Smithing", f"Assembled: {weapon_display_name(weapon)}", None))
            return

    def _handle_weapon_rack_click(self, pos, player):
        # If inspect is open, route there
        if getattr(self, "_inspect_weapon_uid", None):
            self._handle_inspect_click(pos, player)
            return

        for uid, r in getattr(self, "_rack_equip_btn_rects", {}).items():
            if r.collidepoint(pos):
                player.equipped_weapon_uid = None if player.equipped_weapon_uid == uid else uid
                return
        for uid, r in getattr(self, "_rack_inspect_btns", {}).items():
            if r.collidepoint(pos):
                self._inspect_weapon_uid   = uid
                self._inspect_picking_slot = None
                return

    def _handle_inspect_click(self, pos, player):
        # If decoration picker is open
        if getattr(self, "_inspect_picking_slot", None):
            self._handle_picker_click(pos, player)
            return

        weapon = next((w for w in player.crafted_weapons
                       if w.uid == self._inspect_weapon_uid), None)
        if weapon is None:
            self._inspect_weapon_uid = None; return

        if hasattr(self, "_inspect_close_btn") and self._inspect_close_btn.collidepoint(pos):
            self._inspect_weapon_uid = None; return

        # Add decoration
        for slot_key, r in getattr(self, "_inspect_add_btns", {}).items():
            if r.collidepoint(pos):
                slot_data = DECORATION_SLOTS.get(slot_key) or {"type": "gem"}
                self._inspect_picking_slot = slot_key
                self._picker_type = slot_data["type"]
                return

        # Remove decoration
        for slot_key, r in getattr(self, "_inspect_remove_btns", {}).items():
            if r.collidepoint(pos):
                weapon.decorations = [d for d in weapon.decorations if d.get("slot") != slot_key]
                return

    def _handle_picker_click(self, pos, player):
        weapon = next((w for w in player.crafted_weapons
                       if w.uid == self._inspect_weapon_uid), None)
        slot_key = self._inspect_picking_slot

        if hasattr(self, "_picker_cancel_btn") and self._picker_cancel_btn.collidepoint(pos):
            self._inspect_picking_slot = None; return

        if weapon is None or slot_key is None:
            self._inspect_picking_slot = None; return

        slot_data = DECORATION_SLOTS.get(slot_key) or {"type": "gem"}

        for key, r in getattr(self, "_picker_item_rects", {}).items():
            if not r.collidepoint(pos):
                continue
            if slot_data["type"] == "gem":
                # Consume the best-rarity gem of this type from player.gems
                rarity_order = list(GEM_RARITY_BONUS.keys())
                gems = getattr(player, "gems", [])
                matching = [g for g in gems if g.gem_type == key]
                if not matching:
                    return
                # Pick highest-rarity gem
                gem = max(matching, key=lambda g: rarity_order.index(g.rarity))
                gems.remove(gem)
                gem_data = GEM_INLAY_ITEMS.get(key, {"name": key.replace("_", " ").title()})
                weapon.decorations = [d for d in weapon.decorations if d.get("slot") != slot_key]
                weapon.decorations.append({
                    "slot": slot_key, "item_id": key,
                    "name": f"{gem_data['name']} Inlay", "type": "gem",
                    "rarity": gem.rarity, "cut": gem.cut,
                })
            else:
                # Shell
                shells = getattr(player, "seashells", [])
                shell  = next((s for s in shells if s.species == key), None)
                if shell is None:
                    return
                shells.remove(shell)
                weapon.decorations = [d for d in weapon.decorations if d.get("slot") != slot_key]
                weapon.decorations.append({
                    "slot": slot_key, "item_id": shell.species,
                    "name": shell.species.replace("_", " ").title(),
                    "type": "shell", "rarity": shell.rarity,
                })
            self._inspect_picking_slot = None
            player.pending_notifications.append(
                ("Smithing", f"Decorated: {weapon_display_name(weapon)}", None))
            return

    def handle_weapon_rack_scroll(self, delta):
        self._rack_scroll = max(0, self._rack_scroll - delta * 20)

    def handle_bench_scroll(self, delta):
        self._bench_scroll = max(0, self._bench_scroll - delta * 20)

    # ═══════════════════════════════════════════════════════════════════════════
    # INTERNAL STATE TRANSITIONS
    # ═══════════════════════════════════════════════════════════════════════════

    def _smith_current_part(self):
        return WEAPON_TYPES[self._smith_type or "sword"]["parts"][0]

    def _start_heating(self, player):
        ingot_id = MATERIAL_PROFILES[self._smith_material]["ingot_item"]
        if player.inventory.get(ingot_id, 0) < 1 or player.inventory.get("coal", 0) < 1:
            return
        player.inventory[ingot_id] -= 1
        player.inventory["coal"]   -= 1
        self._smith_temperature = 0.0
        self._smith_phase       = "heating"

    def _start_hammering(self):
        part_key = self._smith_current_part()
        self._smith_grid    = make_billet(part_key)
        self._smith_target  = PART_TEMPLATES[part_key]
        self._smith_mistakes = 0
        self._smith_phase   = "hammering"

    def _finish_hammering(self, player):
        q = calculate_part_quality(self._smith_grid, self._smith_target, self._smith_mistakes)
        self._smith_part_quality = [round(q, 3)]
        self._smith_phase = "quench"

    def _apply_quench(self, bonus, player):
        if self._smith_part_quality:
            self._smith_part_quality[-1] = round(min(1.0, self._smith_part_quality[-1] + bonus), 3)
        self._smith_phase = "part_complete"

    def _do_take_part(self, player):
        wtype    = self._smith_type or "sword"
        mat      = self._smith_material or "iron"
        style_id = getattr(self, "_smith_style", "classic")
        part_key = WEAPON_TYPES[wtype]["parts"][0]
        quality  = self._smith_part_quality[-1] if self._smith_part_quality else 0.0
        player.smithed_parts.append({
            "weapon_type": wtype, "part_key": part_key,
            "material": mat, "style": style_id, "quality": round(quality, 3),
        })
        mat_name   = MATERIAL_PROFILES[mat]["name"]
        style_name = WEAPON_STYLES.get(style_id, WEAPON_STYLES["classic"])["name"]
        player.pending_notifications.append(
            ("Smithing", f"Forged: {mat_name} {style_name} {part_key.replace('_', ' ').title()}", None))
        self._smith_phase        = "idle"
        self._smith_type         = None
        self._smith_material     = None
        self._smith_part_quality = []
        self._smith_grid         = []
        self._smith_target       = []
        self._smith_mistakes     = 0
        self._smith_temperature  = 0.0
        self.refinery_open       = False

    # ═══════════════════════════════════════════════════════════════════════════
    # NPC PANELS
    # ═══════════════════════════════════════════════════════════════════════════

    def _draw_weapon_armorer_content(self, player, npc, px, py, PW, PH):
        _GOLD = (210, 175, 60)
        _DIM2 = (130, 110, 70)
        title = self.font.render("WEAPON ARMORER", True, _GOLD)
        self.screen.blit(title, (px + PW // 2 - title.get_width() // 2, py + 10))
        rep_bonus = npc.rep_bonus_pct() if hasattr(npc, "rep_bonus_pct") else 0
        if rep_bonus > 0:
            rb = self.small.render(f"+{rep_bonus}% rep bonus", True, (100, 200, 130))
            self.screen.blit(rb, (px + PW - rb.get_width() - 14, py + 10))
        if not getattr(player, "crafted_weapons", []):
            msg = self.small.render("You have no crafted weapons to sell.", True, _DIM2)
            self.screen.blit(msg, (px + PW // 2 - msg.get_width() // 2, py + PH // 2))
            return
        self.screen.blit(self.small.render("Select a weapon to sell:", True, _DIM2), (px + 16, py + 38))
        self._armorer_sell_rects = {}
        CELL_H, GAP = 54, 6
        scroll = getattr(self, "_armorer_scroll", 0)
        for i, weapon in enumerate(player.crafted_weapons):
            ry = py + 60 + i * (CELL_H + GAP) - scroll
            if ry + CELL_H < py + 56 or ry > py + PH - 20:
                continue
            row_r = pygame.Rect(px + 12, ry, PW - 104, CELL_H)
            self._armorer_sell_rects[weapon.uid] = row_r
            mat_col = MATERIAL_PROFILES.get(weapon.material, {}).get("color", _GOLD)
            pygame.draw.rect(self.screen, (28, 22, 8), row_r)
            pygame.draw.rect(self.screen, mat_col, row_r, 1)
            self.screen.blit(self.font.render(weapon_display_name(weapon), True, mat_col),
                             (row_r.x + 10, ry + 6))
            eq = effective_quality(weapon)
            q_lbl = self.small.render(
                f"{quality_tier(eq)}  {int(eq * 100)}%  •  {weapon.material.title()}", True, _DIM2)
            self.screen.blit(q_lbl, (row_r.x + 10, ry + 28))
            val   = npc.appraise(weapon, player)
            val_r = pygame.Rect(px + PW - 92, ry + 8, 76, CELL_H - 16)
            self._armorer_sell_rects[weapon.uid + "_btn"] = val_r
            pygame.draw.rect(self.screen, (45, 35, 10), val_r, border_radius=4)
            pygame.draw.rect(self.screen, _GOLD, val_r, 1, border_radius=4)
            val_lbl = self.font.render(f"{val}g", True, _GOLD)
            self.screen.blit(val_lbl, val_lbl.get_rect(center=val_r.center))

    def _handle_weapon_armorer_click(self, pos, player, npc):
        for key, rect in getattr(self, "_armorer_sell_rects", {}).items():
            if not rect.collidepoint(pos):
                continue
            uid   = key.replace("_btn", "")
            value = npc.sell_weapon(uid, player)
            if value > 0:
                player.pending_notifications.append(("Sold", f"Weapon sold for {value}g", None))
            return

    def _draw_garrison_commander_content(self, player, npc, px, py, PW, PH):
        _RED   = (200, 100, 70)
        _GOLD2 = (210, 175, 60)
        _DIM2  = (130, 110, 70)
        _GREEN = (100, 200, 120)
        title = self.font.render("GARRISON COMMANDER", True, _RED)
        self.screen.blit(title, (px + PW // 2 - title.get_width() // 2, py + 10))
        self.screen.blit(
            self.small.render("Deliver crafted weapons to earn gold.", True, _DIM2),
            (px + PW // 2 - 140, py + 36))
        self._garrison_quest_rects = {}
        CARD_H, GAP = 130, 14
        for qi, quest in enumerate(npc.quests):
            cy2  = py + 64 + qi * (CARD_H + GAP)
            card = pygame.Rect(px + 16, cy2, PW - 32, CARD_H)
            pygame.draw.rect(self.screen, (28, 22, 14), card)
            pygame.draw.rect(self.screen, _RED, card, 1, border_radius=4)
            wtype_str = quest["weapon_type"].title() if quest["weapon_type"] else "Any weapon type"
            self.screen.blit(self.font.render(f"Bring {quest['count']}× {wtype_str}", True, _RED),
                             (card.x + 10, cy2 + 8))
            self.screen.blit(self.small.render(f"Minimum quality: {quest['min_tier']}", True, _DIM2),
                             (card.x + 10, cy2 + 34))
            matching = len(npc.matching_weapons(player, quest))
            have_col = _GREEN if matching >= quest["count"] else (200, 80, 50)
            self.screen.blit(
                self.small.render(f"You have: {matching} / {quest['count']} qualifying", True, have_col),
                (card.x + 10, cy2 + 54))
            self.screen.blit(self.small.render(f"Reward: {quest['reward']}g", True, _GOLD2),
                             (card.x + 10, cy2 + 74))
            can   = npc.can_complete(player, qi)
            btn_r = pygame.Rect(card.right - 130, cy2 + CARD_H - 44, 118, 32)
            self._garrison_quest_rects[qi] = btn_r
            pygame.draw.rect(self.screen, (55, 40, 20) if can else (30, 25, 18), btn_r, border_radius=4)
            pygame.draw.rect(self.screen, _GOLD2 if can else _DIM2, btn_r, 1, border_radius=4)
            btn_lbl = self.small.render("Complete Quest", True, _GOLD2 if can else _DIM2)
            self.screen.blit(btn_lbl, btn_lbl.get_rect(center=btn_r.center))

    def _handle_garrison_commander_click(self, pos, player, npc):
        for qi, rect in getattr(self, "_garrison_quest_rects", {}).items():
            if rect.collidepoint(pos) and npc.can_complete(player, qi):
                reward = npc.quests[qi]["reward"]
                if npc.complete_quest(player, qi):
                    player.pending_notifications.append(
                        ("Quest", f"Weapons delivered! +{reward}g", None))
