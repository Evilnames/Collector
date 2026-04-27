"""SmithingMixin — Forge mini-game and Weapon Rack panel for CollectorBlocks."""

import math
import pygame
from constants import SCREEN_W, SCREEN_H
from weapons import (
    WEAPON_TYPES, MATERIAL_PROFILES, PART_TEMPLATES, ASSEMBLY_HANDLES,
    WEAPON_TYPE_ORDER, MATERIAL_ORDER,
    make_billet, calculate_part_quality, quality_tier, weapon_display_name,
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
_HOT_COL      = (255, 140,  40)
_WARM_COL     = (210,  70,  20)
_COLD_COL     = ( 90,  90, 100)

SMITH_COLS = 16
SMITH_ROWS = 10


# ── Helpers ───────────────────────────────────────────────────────────────────

def _draw_btn(surface, font, rect, label, enabled=True, hover=False):
    bg = _BTN_HL if (hover and enabled) else (_BTN_BG if enabled else _BTN_DISABLED)
    pygame.draw.rect(surface, bg, rect, border_radius=4)
    pygame.draw.rect(surface, _ACCENT if enabled else _DIM, rect, 1, border_radius=4)
    col = _ACCENT if enabled else _DIM
    txt = font.render(label, True, col)
    surface.blit(txt, txt.get_rect(center=rect.center))


def _temp_colour(t):
    """Map temperature 0–100 to an RGB glow colour."""
    if t >= 60:
        r = int(255)
        g = int(140 * (t - 60) / 40)
        b = 0
    elif t >= 30:
        r = int(210)
        g = int(70 * (t - 30) / 30)
        b = 0
    else:
        frac = t / 30.0
        r = int(90  + 120 * frac)
        g = int(90 * frac)
        b = int(100 * (1 - frac))
    return (min(255, r), min(255, g), min(255, b))


def _draw_temp_bar(surface, font, x, y, w, h, temp):
    """Draw a vertical temperature bar with glow colour."""
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
    pct = font.render(f"{label}: {int(q * 100)}%  {quality_tier(q)}", True, col)
    surface.blit(pct, (x, y + h + 3))


# ── Mixin ─────────────────────────────────────────────────────────────────────

class SmithingMixin:

    # ── Per-frame update (temperature drain) ─────────────────────────────────

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
            elif self._smith_phase in ("hammering",):
                # go back to heating (reheat)
                self._smith_phase = "heating"
            elif self._smith_phase == "quench":
                self._smith_phase = "hammering"
            elif self._smith_phase == "part_complete":
                self._smith_phase = "select"
            elif self._smith_phase == "assemble":
                self._smith_phase = "part_complete"
        elif key == pygame.K_RETURN:
            if self._smith_phase == "hammering":
                self._finish_hammering(player)
        elif key == pygame.K_SPACE:
            if self._smith_phase == "heating":
                self._smith_temperature = min(100.0, self._smith_temperature + 5.0)

    def handle_forge_keys(self, keys, dt, player):
        if self._smith_phase == "heating":
            if keys[pygame.K_SPACE]:
                self._smith_temperature = min(100.0, self._smith_temperature + 5.0 * dt)

    # ── Mouse drag update for hammering ──────────────────────────────────────

    def smith_update_drag(self, mouse_pos, mouse_buttons):
        if self._smith_phase != "hammering":
            return
        # Update hover cell
        self._smith_hover_cell = None
        for (r, c), rect in self._smith_cell_rects.items():
            if rect.collidepoint(mouse_pos):
                self._smith_hover_cell = (r, c)
                break
        # Drag hammering
        if mouse_buttons[0] and self._smith_hover_cell and self._smith_temperature >= 20.0:
            r, c = self._smith_hover_cell
            cell = self._smith_grid[r][c]
            if cell == "excess":
                self._smith_grid[r][c] = "removed"
                self._smith_drag_mode = "hammer"
            elif cell == "target":
                self._smith_grid[r][c] = "mistake"
                self._smith_mistakes += 1
                self._smith_drag_mode = "hammer"
        else:
            self._smith_drag_mode = None

    # ── Main draw dispatcher ──────────────────────────────────────────────────

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

        if self._smith_phase == "select":
            self._draw_smith_select(player)
        elif self._smith_phase == "heating":
            self._draw_smith_heating(player, dt)
        elif self._smith_phase == "hammering":
            self._draw_smith_hammering(player)
        elif self._smith_phase == "quench":
            self._draw_smith_quench(player)
        elif self._smith_phase == "part_complete":
            self._draw_smith_part_complete(player)
        elif self._smith_phase == "assemble":
            self._draw_smith_assemble(player)

    # ── Phase: Select ─────────────────────────────────────────────────────────

    def _draw_smith_select(self, player):
        cx, cy = SCREEN_W // 2, SCREEN_H // 2

        # Weapon type row
        type_lbl = self.font.render("Weapon Type", True, _ACCENT)
        self.screen.blit(type_lbl, (cx - type_lbl.get_width() // 2, cy - 140))

        btn_w, btn_h, gap = 110, 34, 10
        total_w = len(WEAPON_TYPE_ORDER) * btn_w + (len(WEAPON_TYPE_ORDER) - 1) * gap
        tx0 = cx - total_w // 2
        self._smith_type_rects = {}
        for i, wt in enumerate(WEAPON_TYPE_ORDER):
            r = pygame.Rect(tx0 + i * (btn_w + gap), cy - 100, btn_w, btn_h)
            self._smith_type_rects[wt] = r
            selected = (self._smith_type == wt)
            bg = _BTN_HL if selected else _BTN_BG
            pygame.draw.rect(self.screen, bg, r, border_radius=4)
            pygame.draw.rect(self.screen, _ACCENT if selected else _DIM, r, 1, border_radius=4)
            lbl = self.font.render(WEAPON_TYPES[wt]["name"], True, _ACCENT if selected else _DIM)
            self.screen.blit(lbl, lbl.get_rect(center=r.center))

        # Material row
        mat_lbl = self.font.render("Material", True, _ACCENT)
        self.screen.blit(mat_lbl, (cx - mat_lbl.get_width() // 2, cy - 48))

        total_mw = len(MATERIAL_ORDER) * btn_w + (len(MATERIAL_ORDER) - 1) * gap
        mx0 = cx - total_mw // 2
        self._smith_mat_rects = {}
        for i, mat in enumerate(MATERIAL_ORDER):
            r = pygame.Rect(mx0 + i * (btn_w + gap), cy - 14, btn_w, btn_h)
            self._smith_mat_rects[mat] = r
            selected = (self._smith_material == mat)
            col = MATERIAL_PROFILES[mat]["color"]
            bg  = tuple(min(255, c + 30) for c in col) if selected else _BTN_BG
            pygame.draw.rect(self.screen, bg, r, border_radius=4)
            pygame.draw.rect(self.screen, col if selected else _DIM, r, 1, border_radius=4)
            lbl = self.font.render(MATERIAL_PROFILES[mat]["name"], True, col if selected else _DIM)
            self.screen.blit(lbl, lbl.get_rect(center=r.center))

        # Show required ingot
        if self._smith_material:
            ingot_id  = MATERIAL_PROFILES[self._smith_material]["ingot_item"]
            inv_count = player.inventory.get(ingot_id, 0)
            coal_count = player.inventory.get("coal", 0)
            ingot_lbl = self.small.render(
                f"Requires: 1 {ingot_id.replace('_', ' ').title()}  (have {inv_count})  +  1 coal (have {coal_count})",
                True, _ACCENT if inv_count >= 1 and coal_count >= 1 else (200, 60, 40))
            self.screen.blit(ingot_lbl, (cx - ingot_lbl.get_width() // 2, cy + 30))

        # Lock info for gold/steel
        if self._smith_material == "gold":
            research = getattr(self, "_research", None)
            if research and not research.nodes.get("gold_smithing", None) or \
               (research and not research.nodes.get("gold_smithing").unlocked):
                lock_lbl = self.small.render("Requires: Gold Smithing research", True, (200, 80, 50))
                self.screen.blit(lock_lbl, (cx - lock_lbl.get_width() // 2, cy + 48))
        if self._smith_material == "steel":
            research = getattr(self, "_research", None)
            if research and not research.nodes.get("steel_forging", None) or \
               (research and not research.nodes.get("steel_forging").unlocked):
                lock_lbl = self.small.render("Requires: Steel Forging research", True, (200, 80, 50))
                self.screen.blit(lock_lbl, (cx - lock_lbl.get_width() // 2, cy + 48))

        # Begin Forging button
        can_start = (self._smith_type is not None and self._smith_material is not None and
                     player.inventory.get(MATERIAL_PROFILES[self._smith_material]["ingot_item"], 0) >= 1 and
                     player.inventory.get("coal", 0) >= 1)
        if self._smith_material in ("gold", "steel"):
            research = getattr(self, "_research", None)
            req = "gold_smithing" if self._smith_material == "gold" else "steel_forging"
            if research and not getattr(research.nodes.get(req), "unlocked", False):
                can_start = False

        btn_r = pygame.Rect(cx - 80, cy + 70, 160, 36)
        self._smith_begin_btn = btn_r
        _draw_btn(self.screen, self.font, btn_r, "Begin Forging", enabled=can_start,
                  hover=btn_r.collidepoint(pygame.mouse.get_pos()))

    # ── Phase: Heating ────────────────────────────────────────────────────────

    def _draw_smith_heating(self, player, dt):
        cx, cy = SCREEN_W // 2, SCREEN_H // 2

        # Flame animation using time
        t = pygame.time.get_ticks() / 1000.0
        for i in range(5):
            flicker = math.sin(t * 4 + i * 1.3) * 0.5 + 0.5
            fw = int(30 + flicker * 20)
            fh = int(60 + flicker * 30)
            fx = cx - 60 + i * 28 - fw // 2
            fy = cy - 20 - fh
            alpha = int(150 + 80 * flicker)
            col = (255, int(80 + 120 * flicker), 0)
            pygame.draw.ellipse(self.screen, col, (fx, fy, fw, fh))

        mat_col = MATERIAL_PROFILES.get(self._smith_material or "iron", {}).get("color", (160, 165, 175))
        pygame.draw.rect(self.screen, mat_col, (cx - 40, cy - 10, 80, 30))
        lbl = self.font.render("⬛ Metal Billet", True, mat_col)
        self.screen.blit(lbl, (cx - lbl.get_width() // 2, cy + 28))

        _draw_temp_bar(self.screen, self.small, cx + 60, cy - 80, 20, 100,
                       self._smith_temperature)

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

        mat     = self._smith_material or "iron"
        mat_col = MATERIAL_PROFILES[mat]["color"]
        glow    = MATERIAL_PROFILES[mat]["glow"]

        # Temperature glow tint on cells
        temp    = self._smith_temperature
        temp_col = _temp_colour(temp)

        available_h = SCREEN_H - 110
        available_w = SCREEN_W - 240
        cell_size   = min(available_w // SMITH_COLS, available_h // SMITH_ROWS)
        cell_size   = max(6, cell_size)
        grid_w = SMITH_COLS * cell_size
        grid_h = SMITH_ROWS * cell_size

        PANEL_W = 200
        PANEL_X = SCREEN_W - PANEL_W - 12
        gx = (PANEL_X - grid_w) // 2
        gx = max(10, gx)
        gy = 48

        # Draw grid
        for r in range(SMITH_ROWS):
            for c in range(SMITH_COLS):
                px = gx + c * cell_size
                py = gy + r * cell_size
                cr = pygame.Rect(px, py, cell_size, cell_size)
                state = self._smith_grid[r][c]
                target = self._smith_target[r][c]
                hover = (self._smith_hover_cell == (r, c))

                if state == "removed":
                    col = _CELL_REMOVED
                elif state == "mistake":
                    col = _CELL_MISTAKE
                elif state == "target":
                    # Blend metal color with temperature glow
                    blend = min(1.0, temp / 100.0) * 0.4
                    col = tuple(int(mat_col[i] * (1 - blend) + temp_col[i] * blend) for i in range(3))
                else:  # excess
                    col = _CELL_EXCESS

                if hover and temp >= 20.0 and state in ("excess", "target"):
                    col = tuple(min(255, c2 + 40) for c2 in col)

                pygame.draw.rect(self.screen, col, cr)

                # Draw faint target outline on excess cells
                if not target and state == "excess":
                    pygame.draw.rect(self.screen, (80, 85, 90), cr, 1)
                elif target and state == "target":
                    pygame.draw.rect(self.screen, tuple(min(255, v + 30) for v in col), cr, 1)
                elif target and state in ("excess", "removed", "mistake"):
                    # Show where target is
                    pygame.draw.rect(self.screen, (100, 140, 180), cr, 1)
                else:
                    pygame.draw.rect(self.screen, (50, 50, 55), cr, 1)

                self._smith_cell_rects[(r, c)] = cr

        # Outer grid border
        pygame.draw.rect(self.screen, mat_col, (gx - 2, gy - 2, grid_w + 4, grid_h + 4), 2)

        # ── Side panel ───────────────────────────────────────────────────────
        px2 = PANEL_X
        py2 = gy

        # Temperature bar
        _draw_temp_bar(self.screen, self.small, px2, py2, 22, 100, temp)
        py2 += 110

        # Mistake count
        mis_col = (200, 60, 40) if self._smith_mistakes > 0 else _DIM
        mis_lbl = self.small.render(f"Mistakes: {self._smith_mistakes}", True, mis_col)
        self.screen.blit(mis_lbl, (px2, py2))
        py2 += 20

        # Progress: cells removed
        total_excess = sum(1 for r in range(SMITH_ROWS) for c in range(SMITH_COLS)
                           if not self._smith_target[r][c])
        removed = sum(1 for r in range(SMITH_ROWS) for c in range(SMITH_COLS)
                      if self._smith_grid[r][c] == "removed")
        prog_lbl = self.small.render(f"Shaped: {removed}/{total_excess}", True, _ACCENT)
        self.screen.blit(prog_lbl, (px2, py2))
        py2 += 22

        # Temperature warning
        if temp < 30:
            warn = self.small.render("Too cold!", True, (200, 80, 50))
            self.screen.blit(warn, (px2, py2))
            py2 += 18

        # Reheat button (when cold)
        reheat_r = pygame.Rect(px2, py2 + 4, 120, 30)
        self._smith_reheat_btn = reheat_r
        _draw_btn(self.screen, self.small, reheat_r, "Reheat (1 coal)",
                  enabled=temp < 30 and player.inventory.get("coal", 0) >= 1,
                  hover=reheat_r.collidepoint(pygame.mouse.get_pos()))
        py2 += 42

        # Finish button (always available)
        finish_r = pygame.Rect(px2, py2, 120, 30)
        self._smith_finish_btn = finish_r
        _draw_btn(self.screen, self.small, finish_r, "Finish Part",
                  enabled=True, hover=finish_r.collidepoint(pygame.mouse.get_pos()))

        # Part info
        part_key = self._smith_current_part()
        part_lbl = self.font.render(
            f"{MATERIAL_PROFILES[mat]['name']} {part_key.replace('_', ' ').title()}",
            True, mat_col)
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

        water_desc = self.small.render("+0.05 quality bonus", True, (100, 200, 230))
        self.screen.blit(water_desc, (cx - 170, cy + 36))
        air_desc   = self.small.render("No bonus, but safer", True, _DIM)
        self.screen.blit(air_desc,   (cx + 20, cy + 36))

    # ── Phase: Part Complete ──────────────────────────────────────────────────

    def _draw_smith_part_complete(self, player):
        cx, cy = SCREEN_W // 2, SCREEN_H // 2

        lbl = self.font.render("Part Complete!", True, (100, 220, 100))
        self.screen.blit(lbl, (cx - lbl.get_width() // 2, cy - 130))

        if self._smith_part_quality:
            last_q = self._smith_part_quality[-1]
            _draw_quality_bar(self.screen, self.small, cx - 150, cy - 90, 300, 18, last_q)

        wtype = self._smith_type or "sword"
        parts = WEAPON_TYPES[wtype]["parts"]
        done  = len(self._smith_part_quality)
        progress_lbl = self.small.render(
            f"Parts forged: {done} / {len(parts)}", True, _ACCENT)
        self.screen.blit(progress_lbl, (cx - progress_lbl.get_width() // 2, cy - 50))

        # Pending parts list
        for i, part_key in enumerate(parts):
            mat = self._smith_material or "iron"
            if i < done:
                tier = quality_tier(self._smith_part_quality[i])
                col  = (100, 220, 100)
                text = f"  ✓ {mat.title()} {part_key.replace('_', ' ').title()}  [{tier}]"
            else:
                col  = _DIM
                text = f"  ○ {mat.title()} {part_key.replace('_', ' ').title()}"
            p_lbl = self.small.render(text, True, col)
            self.screen.blit(p_lbl, (cx - p_lbl.get_width() // 2, cy - 22 + i * 18))

        all_done = done >= len(parts)
        handle_id = ASSEMBLY_HANDLES.get(wtype, "")
        handle_count = player.inventory.get(handle_id, 0)

        # Next part or assemble
        next_r = pygame.Rect(cx - 90, cy + 60, 180, 36)
        asmb_r = pygame.Rect(cx - 90, cy + 106, 180, 36)
        self._smith_next_part_btn  = next_r if not all_done else None
        self._smith_assemble_btn   = asmb_r if all_done else None

        if not all_done:
            _draw_btn(self.screen, self.font, next_r, "Forge Next Part",
                      hover=next_r.collidepoint(pygame.mouse.get_pos()))
        else:
            h_lbl = self.small.render(
                f"Needs: {handle_id.replace('_', ' ').title()}  (have {handle_count})",
                True, _ACCENT if handle_count > 0 else (200, 60, 40))
            self.screen.blit(h_lbl, (cx - h_lbl.get_width() // 2, cy + 60))
            can_assemble = handle_count > 0
            _draw_btn(self.screen, self.font, asmb_r, "Assemble Weapon",
                      enabled=can_assemble,
                      hover=asmb_r.collidepoint(pygame.mouse.get_pos()))

    # ── Phase: Assemble ───────────────────────────────────────────────────────

    def _draw_smith_assemble(self, player):
        cx, cy = SCREEN_W // 2, SCREEN_H // 2

        avg_q = sum(self._smith_part_quality) / max(1, len(self._smith_part_quality))
        # Apply master_smithing bonus
        bonus = getattr(player, "smith_quality_bonus", 0.0)
        final_q = min(1.0, avg_q + bonus)
        tier    = quality_tier(final_q)

        lbl = self.font.render("Assemble Weapon?", True, _ACCENT)
        self.screen.blit(lbl, (cx - lbl.get_width() // 2, cy - 100))

        mat   = self._smith_material or "iron"
        wtype = self._smith_type or "sword"
        name  = f"{MATERIAL_PROFILES[mat]['name']} {WEAPON_TYPES[wtype]['name']}"
        n_lbl = self.font.render(name, True, MATERIAL_PROFILES[mat]["color"])
        self.screen.blit(n_lbl, (cx - n_lbl.get_width() // 2, cy - 68))

        _draw_quality_bar(self.screen, self.small, cx - 150, cy - 34, 300, 18, final_q,
                          label=f"Final Quality ({tier})")

        dmg = (WEAPON_TYPES[wtype]["base_damage"] *
               MATERIAL_PROFILES[mat]["damage_mult"] *
               (0.7 + final_q * 0.6))
        stats_lbl = self.small.render(
            f"Damage: {dmg:.1f}  Range: {WEAPON_TYPES[wtype]['attack_range']}  "
            f"Speed: {1.0 / WEAPON_TYPES[wtype]['cooldown']:.1f}/s",
            True, _ACCENT)
        self.screen.blit(stats_lbl, (cx - stats_lbl.get_width() // 2, cy + 10))

        handle_id = ASSEMBLY_HANDLES.get(wtype, "")
        h_lbl = self.small.render(
            f"Consumes: {handle_id.replace('_', ' ').title()} ×1",
            True, _DIM)
        self.screen.blit(h_lbl, (cx - h_lbl.get_width() // 2, cy + 30))

        confirm_r = pygame.Rect(cx - 90, cy + 60, 180, 36)
        cancel_r  = pygame.Rect(cx - 90, cy + 104, 180, 36)
        self._smith_confirm_btn = confirm_r
        self._smith_cancel_btn  = cancel_r
        _draw_btn(self.screen, self.font, confirm_r, "Assemble!",
                  hover=confirm_r.collidepoint(pygame.mouse.get_pos()))
        _draw_btn(self.screen, self.font, cancel_r, "Cancel",
                  hover=cancel_r.collidepoint(pygame.mouse.get_pos()))

    # ── Weapon Rack panel ────────────────────────────────────────────────────

    def _draw_weapon_rack(self, player):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("WEAPON RACK", True, _ACCENT)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))
        hint = self.small.render("ESC close", True, _DIM)
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 8))

        if not player.crafted_weapons:
            lbl = self.font.render("No weapons crafted yet.", True, _DIM)
            self.screen.blit(lbl, (SCREEN_W // 2 - lbl.get_width() // 2, SCREEN_H // 2))
            return

        ROW_H  = 56
        LIST_Y = 36
        LIST_X = 60
        self._rack_weapon_rects    = {}
        self._rack_equip_btn_rects = {}

        for i, w in enumerate(player.crafted_weapons):
            row_y = LIST_Y + i * ROW_H - self._rack_scroll
            if row_y + ROW_H < 0 or row_y > SCREEN_H:
                continue

            row_r = pygame.Rect(LIST_X, row_y, SCREEN_W - LIST_X * 2 - 140, ROW_H - 4)
            self._rack_weapon_rects[w.uid] = row_r

            equipped = (player.equipped_weapon_uid == w.uid)
            bg = (50, 40, 28) if equipped else (35, 30, 22)
            pygame.draw.rect(self.screen, bg, row_r, border_radius=4)
            pygame.draw.rect(self.screen, _ACCENT if equipped else _DIM, row_r, 1, border_radius=4)

            mat_col  = MATERIAL_PROFILES.get(w.material, {}).get("color", _ACCENT)
            name_lbl = self.font.render(weapon_display_name(w), True, mat_col)
            self.screen.blit(name_lbl, (row_r.x + 8, row_y + 4))

            tier_lbl = self.small.render(quality_tier(w.quality), True, mat_col)
            self.screen.blit(tier_lbl, (row_r.x + 8, row_y + 26))

            _draw_quality_bar(self.screen, self.small, row_r.x + 120, row_y + 28, 120, 10, w.quality, label="")

            btn_r = pygame.Rect(row_r.right + 8, row_y + 10, 110, 30)
            self._rack_equip_btn_rects[w.uid] = btn_r
            btn_lbl = "Unequip" if equipped else "Equip"
            _draw_btn(self.screen, self.small, btn_r, btn_lbl,
                      hover=btn_r.collidepoint(pygame.mouse.get_pos()))

        # Scroll hint
        if len(player.crafted_weapons) > 8:
            sc_lbl = self.small.render("Scroll to see more", True, _DIM)
            self.screen.blit(sc_lbl, (SCREEN_W // 2 - sc_lbl.get_width() // 2, SCREEN_H - 20))

    # ── HUD overlay (equipped weapon indicator) ───────────────────────────────

    def draw_smith_hud(self, player):
        if not player.equipped_weapon_uid:
            return
        weapon = next((w for w in player.crafted_weapons if w.uid == player.equipped_weapon_uid), None)
        if weapon is None:
            return
        mat_col = MATERIAL_PROFILES.get(weapon.material, {}).get("color", _ACCENT)
        name    = weapon_display_name(weapon)
        lbl     = self.small.render(f"⚔ {name}", True, mat_col)
        self.screen.blit(lbl, (8, SCREEN_H - lbl.get_height() - 26))

    # ── Click handlers ────────────────────────────────────────────────────────

    def _handle_forge_click(self, pos, player):
        phase = self._smith_phase
        if phase == "select":
            for wt, r in getattr(self, "_smith_type_rects", {}).items():
                if r.collidepoint(pos):
                    self._smith_type = wt
                    return
            for mat, r in getattr(self, "_smith_mat_rects", {}).items():
                if r.collidepoint(pos):
                    self._smith_material = mat
                    return
            if hasattr(self, "_smith_begin_btn") and self._smith_begin_btn.collidepoint(pos):
                self._start_heating(player)

        elif phase == "heating":
            if hasattr(self, "_smith_hammer_btn") and self._smith_hammer_btn.collidepoint(pos):
                if self._smith_temperature >= 80.0:
                    self._start_hammering()

        elif phase == "hammering":
            if hasattr(self, "_smith_finish_btn") and self._smith_finish_btn.collidepoint(pos):
                self._finish_hammering(player)
                return
            if hasattr(self, "_smith_reheat_btn") and self._smith_reheat_btn.collidepoint(pos):
                if self._smith_temperature < 30.0 and player.inventory.get("coal", 0) >= 1:
                    player.inventory["coal"] = player.inventory.get("coal", 0) - 1
                    self._smith_temperature = min(100.0, self._smith_temperature + 40.0)
                    self._smith_phase = "heating"
                    return
            # Grid clicks handled by smith_update_drag

        elif phase == "quench":
            if hasattr(self, "_smith_quench_water_btn") and self._smith_quench_water_btn.collidepoint(pos):
                self._apply_quench(0.05, player)
            elif hasattr(self, "_smith_quench_air_btn") and self._smith_quench_air_btn.collidepoint(pos):
                self._apply_quench(0.0, player)

        elif phase == "part_complete":
            if self._smith_next_part_btn and self._smith_next_part_btn.collidepoint(pos):
                self._smith_phase = "heating"
                self._smith_temperature = 0.0
                self._smith_grid = []
                self._smith_target = []
                self._smith_mistakes = 0
            elif self._smith_assemble_btn and self._smith_assemble_btn.collidepoint(pos):
                wtype = self._smith_type or "sword"
                handle_id = ASSEMBLY_HANDLES.get(wtype, "")
                if player.inventory.get(handle_id, 0) >= 1:
                    self._smith_phase = "assemble"

        elif phase == "assemble":
            if hasattr(self, "_smith_confirm_btn") and self._smith_confirm_btn.collidepoint(pos):
                self._do_assemble(player)
            elif hasattr(self, "_smith_cancel_btn") and self._smith_cancel_btn.collidepoint(pos):
                self._smith_phase = "part_complete"

    def _handle_weapon_rack_click(self, pos, player):
        if hasattr(self, "_rack_equip_btn_rects"):
            for uid, r in self._rack_equip_btn_rects.items():
                if r.collidepoint(pos):
                    if player.equipped_weapon_uid == uid:
                        player.equipped_weapon_uid = None
                    else:
                        player.equipped_weapon_uid = uid
                    return

    def handle_weapon_rack_scroll(self, delta):
        self._rack_scroll = max(0, self._rack_scroll - delta * 20)

    # ── Internal state transitions ────────────────────────────────────────────

    def _smith_current_part(self):
        wtype = self._smith_type or "sword"
        done  = len(self._smith_part_quality)
        parts = WEAPON_TYPES[wtype]["parts"]
        if done < len(parts):
            return parts[done]
        return parts[-1]

    def _start_heating(self, player):
        ingot_id = MATERIAL_PROFILES[self._smith_material]["ingot_item"]
        if player.inventory.get(ingot_id, 0) < 1:
            return
        if player.inventory.get("coal", 0) < 1:
            return
        player.inventory[ingot_id] = player.inventory.get(ingot_id, 0) - 1
        player.inventory["coal"]   = player.inventory.get("coal", 0) - 1
        # Start a fresh weapon if this is the first part
        if not self._smith_part_quality:
            self._smith_pending_uid = None
            new_w = player._weapon_gen.new_weapon(self._smith_type, self._smith_material)
            player.pending_parts[new_w.uid] = {}
            self._smith_pending_uid = new_w.uid
        self._smith_temperature = 0.0
        self._smith_phase = "heating"

    def _start_hammering(self):
        part_key = self._smith_current_part()
        self._smith_grid   = make_billet(part_key)
        self._smith_target = PART_TEMPLATES[part_key]
        self._smith_mistakes = 0
        self._smith_phase = "hammering"

    def _finish_hammering(self, player):
        q = calculate_part_quality(
            self._smith_grid, self._smith_target, self._smith_mistakes)
        self._smith_part_quality.append(round(q, 3))
        self._smith_phase = "quench"

    def _apply_quench(self, bonus, player):
        if self._smith_part_quality:
            q = min(1.0, self._smith_part_quality[-1] + bonus)
            self._smith_part_quality[-1] = round(q, 3)
        self._smith_phase = "part_complete"

    def _do_assemble(self, player):
        wtype  = self._smith_type or "sword"
        mat    = self._smith_material or "iron"
        handle = ASSEMBLY_HANDLES.get(wtype, "")
        if player.inventory.get(handle, 0) < 1:
            return

        # Consume handle
        player.inventory[handle] = player.inventory.get(handle, 0) - 1

        # Finalise weapon
        uid = self._smith_pending_uid
        weapon = None
        if uid:
            weapon = next((w for w in player.crafted_weapons if w.uid == uid), None)
        if weapon is None:
            # New weapon object
            weapon = player._weapon_gen.new_weapon(wtype, mat)

        weapon.parts_quality = list(self._smith_part_quality)
        avg = sum(weapon.parts_quality) / max(1, len(weapon.parts_quality))
        bonus = getattr(player, "smith_quality_bonus", 0.0)
        weapon.quality = round(min(1.0, avg + bonus), 3)

        if weapon not in player.crafted_weapons:
            player.crafted_weapons.append(weapon)

        # Clean up pending_parts entry
        if uid and uid in player.pending_parts:
            del player.pending_parts[uid]

        player.pending_notifications.append(
            ("Smithing", f"Forged: {weapon_display_name(weapon)}", None))

        # Reset state
        self._smith_phase       = "idle"
        self._smith_type        = None
        self._smith_material    = None
        self._smith_part_quality = []
        self._smith_pending_uid  = None
        self._smith_grid         = []
        self._smith_target       = []
        self._smith_mistakes     = 0
        self._smith_temperature  = 0.0
        self.refinery_open       = False

    # ═══════════════════════════════════════════════════════════════════════════
    # NPC PANEL METHODS
    # ═══════════════════════════════════════════════════════════════════════════

    # ── Weapon Armorer NPC panel ──────────────────────────────────────────────

    def _draw_weapon_armorer_content(self, player, npc, px, py, PW, PH):
        _GOLD = (210, 175,  60)
        _DIM2 = (130, 110,  70)

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

        sub = self.small.render("Select a weapon to sell:", True, _DIM2)
        self.screen.blit(sub, (px + 16, py + 38))

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
            pygame.draw.rect(self.screen, (28, 22,  8), row_r)
            pygame.draw.rect(self.screen, mat_col, row_r, 1)

            name_lbl = self.font.render(weapon_display_name(weapon), True, mat_col)
            self.screen.blit(name_lbl, (row_r.x + 10, ry + 6))

            tier = quality_tier(weapon.quality)
            q_lbl = self.small.render(f"{tier}  {int(weapon.quality * 100)}%  •  {weapon.material.title()}", True, _DIM2)
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
            uid = key.replace("_btn", "")
            value = npc.sell_weapon(uid, player)
            if value > 0:
                player.pending_notifications.append(
                    ("Sold", f"Weapon sold for {value}g", None))
            return

    # ── Quartermaster NPC panel ───────────────────────────────────────────────
    # Reuses _draw_trade_content — QuartermasterNPC has the same .trades / .can_trade /
    # .execute_trade / .boosted_gold interface as TradeNPC so no new draw method needed.

    # ── Garrison Commander NPC panel ──────────────────────────────────────────

    def _draw_garrison_commander_content(self, player, npc, px, py, PW, PH):
        _RED    = (200, 100,  70)
        _GOLD2  = (210, 175,  60)
        _DIM2   = (130, 110,  70)
        _GREEN  = (100, 200, 120)

        title = self.font.render("GARRISON COMMANDER", True, _RED)
        self.screen.blit(title, (px + PW // 2 - title.get_width() // 2, py + 10))

        hint = self.small.render("Deliver crafted weapons to earn gold.", True, _DIM2)
        self.screen.blit(hint, (px + PW // 2 - hint.get_width() // 2, py + 36))

        self._garrison_quest_rects = {}
        CARD_H, GAP = 130, 14
        weapons = getattr(player, "crafted_weapons", [])

        for qi, quest in enumerate(npc.quests):
            cy2 = py + 64 + qi * (CARD_H + GAP)
            card = pygame.Rect(px + 16, cy2, PW - 32, CARD_H)
            pygame.draw.rect(self.screen, (28, 22, 14), card)
            pygame.draw.rect(self.screen, _RED, card, 1, border_radius=4)

            wtype_str = quest["weapon_type"].title() if quest["weapon_type"] else "Any weapon type"
            q_label   = f"Bring {quest['count']}× {wtype_str}"
            q_lbl = self.font.render(q_label, True, _RED)
            self.screen.blit(q_lbl, (card.x + 10, cy2 + 8))

            tier_lbl = self.small.render(f"Minimum quality: {quest['min_tier']}", True, _DIM2)
            self.screen.blit(tier_lbl, (card.x + 10, cy2 + 34))

            matching = len(npc.matching_weapons(player, quest))
            have_col = _GREEN if matching >= quest["count"] else (200, 80, 50)
            have_lbl = self.small.render(f"You have: {matching} / {quest['count']} qualifying", True, have_col)
            self.screen.blit(have_lbl, (card.x + 10, cy2 + 54))

            reward_lbl = self.small.render(f"Reward: {quest['reward']}g", True, _GOLD2)
            self.screen.blit(reward_lbl, (card.x + 10, cy2 + 74))

            can = npc.can_complete(player, qi)
            btn_r = pygame.Rect(card.right - 130, cy2 + CARD_H - 44, 118, 32)
            self._garrison_quest_rects[qi] = btn_r
            bg = (55, 40, 20) if can else (30, 25, 18)
            bd = _GOLD2 if can else _DIM2
            pygame.draw.rect(self.screen, bg, btn_r, border_radius=4)
            pygame.draw.rect(self.screen, bd, btn_r, 1, border_radius=4)
            btn_lbl = self.small.render("Complete Quest", True, _GOLD2 if can else _DIM2)
            self.screen.blit(btn_lbl, btn_lbl.get_rect(center=btn_r.center))

    def _handle_garrison_commander_click(self, pos, player, npc):
        for qi, rect in getattr(self, "_garrison_quest_rects", {}).items():
            if rect.collidepoint(pos) and npc.can_complete(player, qi):
                reward = npc.quests[qi]["reward"]
                if npc.complete_quest(player, qi):
                    player.pending_notifications.append(
                        ("Quest", f"Weapons delivered! +{reward}g", None))
