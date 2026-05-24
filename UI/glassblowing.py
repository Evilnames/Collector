"""Glassblowing UI mixin.

Two stations:

    Glass Blowing Bench (1732)
        - pick a sand variety from inventory
        - pick a target shape (bottle / vessel / pane)
        - run the puff mini-game (SPACE taps, target ≈ 6)
        - GlassPiece is created in "blown" state and appended to player.glass_items

    Annealing Oven (1733)
        - pick a "blown" piece
        - pick a cool rate (quick / standard / slow)
        - on success: grant the output item and mark discovered
        - on shatter (quick cool): grant glass_shards
"""

import pygame
from constants import SCREEN_W, SCREEN_H

from glassblowing import (
    SAND_BIOME_PROFILES, BIOME_DISPLAY_NAMES, VARIETY_DISPLAY,
    BLOW_SHAPES, ANNEAL_RATES, OUTPUT_DESCS, OUTPUT_COLORS, TYPE_ORDER,
    GlassblowingGenerator, GlassPiece,
    apply_blow, apply_anneal, get_output_item, discovered_key,
)


_PANEL_BG     = (18, 24, 30)
_PANEL_BORDER = (110, 160, 180)
_TEXT_MAIN    = (210, 235, 245)
_TEXT_DIM     = (110, 140, 155)
_BTN_BG       = (30, 50, 65)
_BTN_HOVER    = (60, 100, 130)
_FLAME        = (240, 150, 70)


# Helper: turn the four typed sand item ids into a uniform iterable.
def _sand_choices(player):
    """Yield (sand_biome, count) for each sand variety the player holds."""
    out = []
    for biome in SAND_BIOME_PROFILES.keys():
        n = player.inventory.get(f"sand_{biome}", 0)
        if n > 0:
            out.append((biome, n))
    return out


class GlassblowingMixin:

    # ── Glass Blowing Bench ──────────────────────────────────────────────────

    def _draw_blowing_bench(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("GLASS BLOWING BENCH", True, _TEXT_MAIN)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 8))
        hint = self.small.render("ESC to close", True, _TEXT_DIM)
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 8))

        # Left: sand variety selection
        self._glass_sand_rects = {}
        sx, sy = 60, 60
        self.screen.blit(self.font.render("SAND VARIETY", True, _TEXT_MAIN), (sx, sy))
        choices = _sand_choices(player)
        if not choices:
            msg = self.small.render("No typed sand. Mine SAND in desert / coast / volcanic / salt-flat biomes.", True, (210, 140, 100))
            self.screen.blit(msg, (sx, sy + 24))
        else:
            for i, (biome, n) in enumerate(choices):
                rect = pygame.Rect(sx, sy + 28 + i * 34, 220, 28)
                self._glass_sand_rects[biome] = rect
                bg = _BTN_HOVER if self.glass_sand_key == biome else _BTN_BG
                pygame.draw.rect(self.screen, bg, rect)
                pygame.draw.rect(self.screen, _PANEL_BORDER, rect, 1)
                txt = f"{BIOME_DISPLAY_NAMES[biome]}  ({n})"
                self.screen.blit(self.small.render(txt, True, _TEXT_MAIN), (rect.x + 6, rect.y + 7))
                sub = self.small.render(VARIETY_DISPLAY[SAND_BIOME_PROFILES[biome]["variety"]], True, _TEXT_DIM)
                self.screen.blit(sub, (rect.x + 130, rect.y + 7))

        # Middle: shape selection
        self._glass_shape_rects = {}
        mx, my = 320, 60
        self.screen.blit(self.font.render("TARGET SHAPE", True, _TEXT_MAIN), (mx, my))
        for i, (key, cfg) in enumerate(BLOW_SHAPES.items()):
            rect = pygame.Rect(mx, my + 28 + i * 60, 260, 54)
            self._glass_shape_rects[key] = rect
            bg = _BTN_HOVER if self.glass_shape_key == key else _BTN_BG
            pygame.draw.rect(self.screen, bg, rect)
            pygame.draw.rect(self.screen, _PANEL_BORDER, rect, 1)
            self.screen.blit(self.font.render(cfg["label"], True, _TEXT_MAIN), (rect.x + 8, rect.y + 6))
            self.screen.blit(self.small.render(cfg["desc"], True, _TEXT_DIM), (rect.x + 8, rect.y + 30))

        # Right: puff counter / blow control
        rx, ry = 620, 60
        self.screen.blit(self.font.render("BLOW", True, _TEXT_MAIN), (rx, ry))
        puff = self.glass_puff_count
        bar = pygame.Rect(rx, ry + 32, 280, 22)
        pygame.draw.rect(self.screen, (40, 40, 50), bar)
        pygame.draw.rect(self.screen, _PANEL_BORDER, bar, 1)
        # Target window 4–8 puffs; centre at 6.
        for p in range(12):
            cell = pygame.Rect(bar.x + 1 + p * 23, bar.y + 1, 22, 20)
            if p < puff:
                col = _FLAME if 4 <= puff <= 8 else (200, 90, 60) if puff > 8 else (130, 130, 140)
                pygame.draw.rect(self.screen, col, cell)
        self.screen.blit(self.small.render(f"Puffs: {puff}  (target 4–8)", True, _TEXT_MAIN), (rx, ry + 60))
        self.screen.blit(self.small.render("Press SPACE to puff", True, _TEXT_DIM),    (rx, ry + 78))
        self.screen.blit(self.small.render("Click FINISH to set the piece", True, _TEXT_DIM), (rx, ry + 96))

        self._glass_finish_rect = pygame.Rect(rx, ry + 130, 200, 34)
        ready = bool(self.glass_sand_key and self.glass_shape_key and puff > 0)
        bg = _BTN_HOVER if ready else (40, 40, 45)
        pygame.draw.rect(self.screen, bg, self._glass_finish_rect)
        pygame.draw.rect(self.screen, _PANEL_BORDER, self._glass_finish_rect, 1)
        self.screen.blit(self.font.render("FINISH BLOW", True, _TEXT_MAIN if ready else _TEXT_DIM),
                         (self._glass_finish_rect.x + 22, self._glass_finish_rect.y + 7))

        self._glass_reset_rect = pygame.Rect(rx, ry + 170, 200, 28)
        pygame.draw.rect(self.screen, _BTN_BG, self._glass_reset_rect)
        pygame.draw.rect(self.screen, _PANEL_BORDER, self._glass_reset_rect, 1)
        self.screen.blit(self.small.render("Reset (start over)", True, _TEXT_DIM), (self._glass_reset_rect.x + 20, self._glass_reset_rect.y + 7))

    def _handle_blowing_bench_click(self, pos, player):
        for biome, rect in getattr(self, "_glass_sand_rects", {}).items():
            if rect.collidepoint(pos):
                self.glass_sand_key = biome
                return
        for key, rect in getattr(self, "_glass_shape_rects", {}).items():
            if rect.collidepoint(pos):
                self.glass_shape_key = key
                return
        if getattr(self, "_glass_reset_rect", None) and self._glass_reset_rect.collidepoint(pos):
            self.glass_puff_count = 0
            return
        if getattr(self, "_glass_finish_rect", None) and self._glass_finish_rect.collidepoint(pos):
            self._commit_blow(player)
            return

    def handle_glass_keydown(self, key, player):
        if key == pygame.K_SPACE:
            self.glass_puff_count = min(12, self.glass_puff_count + 1)

    def _commit_blow(self, player):
        if not (self.glass_sand_key and self.glass_shape_key and self.glass_puff_count > 0):
            return
        sand_item = f"sand_{self.glass_sand_key}"
        if player.inventory.get(sand_item, 0) < 1:
            return
        # Consume one sand of that variety.
        player.inventory[sand_item] -= 1
        if player.inventory[sand_item] <= 0:
            player.inventory.pop(sand_item, None)
        # Create the GlassPiece and apply the blow result.
        piece = player._glass_gen.gather(self.glass_sand_key)
        apply_blow(piece, self.glass_shape_key, self.glass_puff_count)
        player.glass_items.append(piece)
        msg = "Glass burst!" if not piece.shape else f"Blown {BLOW_SHAPES[piece.shape]['label']}"
        player.pending_notifications.append(("Glassblowing", msg, None))
        self.glass_puff_count = 0

    # ── Annealing Oven ───────────────────────────────────────────────────────

    def _draw_annealing_oven(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("ANNEALING OVEN", True, _TEXT_MAIN)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 8))
        hint = self.small.render("ESC to close", True, _TEXT_DIM)
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 8))

        # Left: blown pieces awaiting anneal
        blown = [(i, p) for i, p in enumerate(player.glass_items) if p.state == "blown" and p.shape]
        self._glass_piece_rects = {}
        sx, sy = 60, 60
        self.screen.blit(self.font.render("BLOWN PIECES", True, _TEXT_MAIN), (sx, sy))
        if not blown:
            msg = self.small.render("Nothing to anneal. Blow a piece at the Blowing Bench first.", True, _TEXT_DIM)
            self.screen.blit(msg, (sx, sy + 24))
        else:
            for slot, (idx, p) in enumerate(blown[:10]):
                rect = pygame.Rect(sx, sy + 28 + slot * 36, 320, 30)
                self._glass_piece_rects[idx] = rect
                bg = _BTN_HOVER if self.glass_selected_idx == idx else _BTN_BG
                pygame.draw.rect(self.screen, bg, rect)
                pygame.draw.rect(self.screen, _PANEL_BORDER, rect, 1)
                label = (f"{BIOME_DISPLAY_NAMES[p.origin_biome]} {BLOW_SHAPES[p.shape]['label']}  "
                         f"clarity {int(p.clarity * 100)}  sym {int(p.symmetry * 100)}")
                self.screen.blit(self.small.render(label, True, _TEXT_MAIN), (rect.x + 6, rect.y + 8))

        # Right: cool-rate buttons
        self._glass_rate_rects = {}
        rx, ry = 420, 60
        self.screen.blit(self.font.render("COOL RATE", True, _TEXT_MAIN), (rx, ry))
        for i, (key, cfg) in enumerate(ANNEAL_RATES.items()):
            rect = pygame.Rect(rx, ry + 28 + i * 60, 300, 54)
            self._glass_rate_rects[key] = rect
            bg = _BTN_HOVER if self.glass_rate_key == key else _BTN_BG
            pygame.draw.rect(self.screen, bg, rect)
            pygame.draw.rect(self.screen, _PANEL_BORDER, rect, 1)
            self.screen.blit(self.font.render(cfg["label"], True, _TEXT_MAIN), (rect.x + 8, rect.y + 6))
            self.screen.blit(self.small.render(cfg["desc"], True, _TEXT_DIM), (rect.x + 8, rect.y + 30))

        # Confirm
        self._glass_anneal_btn = pygame.Rect(rx, ry + 240, 220, 36)
        ready = self.glass_selected_idx is not None and self.glass_rate_key
        bg = _BTN_HOVER if ready else (40, 40, 45)
        pygame.draw.rect(self.screen, bg, self._glass_anneal_btn)
        pygame.draw.rect(self.screen, _PANEL_BORDER, self._glass_anneal_btn, 1)
        self.screen.blit(self.font.render("ANNEAL", True, _TEXT_MAIN if ready else _TEXT_DIM),
                         (self._glass_anneal_btn.x + 80, self._glass_anneal_btn.y + 9))

    def _handle_annealing_oven_click(self, pos, player):
        for idx, rect in getattr(self, "_glass_piece_rects", {}).items():
            if rect.collidepoint(pos):
                self.glass_selected_idx = idx
                return
        for key, rect in getattr(self, "_glass_rate_rects", {}).items():
            if rect.collidepoint(pos):
                self.glass_rate_key = key
                return
        if getattr(self, "_glass_anneal_btn", None) and self._glass_anneal_btn.collidepoint(pos):
            self._commit_anneal(player)
            return

    # ── Codex (encyclopedia tab 40) ──────────────────────────────────────────

    def _draw_glass_codex(self, player, gy0=58, gx_off=130):
        import pygame as _pg
        disc = getattr(player, "discovered_glass", set())
        total = len(TYPE_ORDER)
        disc_count = len(disc)

        sub = self.small.render(f"Discovered: {disc_count} / {total}", True, _TEXT_DIM)
        self.screen.blit(sub, (gx_off + 8, gy0))

        biomes = list(SAND_BIOME_PROFILES.keys())   # 4
        shapes = list(BLOW_SHAPES.keys())           # 3
        cell_w, cell_h, gap = 130, 56, 6

        # Column headers (shapes)
        col_hdr_y = gy0 + 22
        for ci, shape in enumerate(shapes):
            hx = gx_off + 90 + ci * (cell_w + gap)
            col = OUTPUT_COLORS.get(shape, _TEXT_MAIN)
            self.screen.blit(self.small.render(BLOW_SHAPES[shape]["label"], True, col), (hx, col_hdr_y))

        grid_y0 = col_hdr_y + 20
        for ri, biome in enumerate(biomes):
            row_y = grid_y0 + ri * (cell_h + gap)
            bnm = BIOME_DISPLAY_NAMES.get(biome, biome.title())
            self.screen.blit(self.small.render(bnm, True, _TEXT_MAIN),
                             (gx_off + 4, row_y + cell_h // 2 - 7))
            for ci, shape in enumerate(shapes):
                key = f"{biome}_{shape}"
                discovered = key in disc
                cx = gx_off + 90 + ci * (cell_w + gap)
                crect = _pg.Rect(cx, row_y, cell_w, cell_h)
                col = OUTPUT_COLORS.get(shape, _TEXT_MAIN)
                bg  = (28, 36, 44) if discovered else (16, 20, 24)
                brd = col if discovered else (60, 70, 80)
                _pg.draw.rect(self.screen, bg, crect)
                _pg.draw.rect(self.screen, brd, crect, 2)
                if discovered:
                    self.screen.blit(self.small.render(VARIETY_DISPLAY[SAND_BIOME_PROFILES[biome]["variety"]], True, col), (cx + 6, row_y + 6))
                    self.screen.blit(self.small.render(BLOW_SHAPES[shape]["label"], True, _TEXT_MAIN), (cx + 6, row_y + 24))
                else:
                    unk = self.small.render("?", True, (60, 70, 80))
                    self.screen.blit(unk, (cx + cell_w // 2 - unk.get_width() // 2,
                                           row_y + cell_h // 2 - unk.get_height() // 2))

    def _commit_anneal(self, player):
        if self.glass_selected_idx is None or not self.glass_rate_key:
            return
        if self.glass_selected_idx >= len(player.glass_items):
            return
        piece = player.glass_items[self.glass_selected_idx]
        if piece.state != "blown" or not piece.shape:
            return
        survived = apply_anneal(piece, self.glass_rate_key)
        if not survived:
            piece.shape = ""
            player._add_item("glass_shards")
            player.pending_notifications.append(("Glassblowing", "Piece shattered while cooling!", None))
        else:
            out_id = get_output_item(piece)
            player._add_item(out_id)
            player.discovered_glass.add(discovered_key(piece))
            label = f"{BIOME_DISPLAY_NAMES[piece.origin_biome]} {BLOW_SHAPES[piece.shape]['label']}"
            player.pending_notifications.append(("Glassblowing", label, None))
        self.glass_selected_idx = None
        self.glass_rate_key     = None
