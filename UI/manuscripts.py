"""Manuscripts UI mixin — Scribe's Desk station + Lectern reader.

Phases (state machine on `self._manu_phase`):
  parchment   : pick a raw parchment (or press a fresh one from flax_fiber)
  ink         : pick an ink the player owns; optionally toggle pigment accents
  illuminate  : 8×12 grid mini-game (tapestry-style colour placement)
  bind        : choose binding material + content category → finalize
"""
import pygame

from manuscripts import (
    INK_RECIPES, BINDING_PROFILES, CONTENT_CATEGORIES,
    BIOME_PARCHMENT_PROFILES, BIOME_DISPLAY_NAMES,
    finalize_manuscript, quality_stars, grid_quality,
    kingdom_for_world_x, UNKNOWN_KINGDOM,
)


_PIGMENT_KEYS = [
    "dye_extract_crimson", "dye_extract_cobalt", "dye_extract_amber",
    "dye_extract_verdant", "dye_extract_violet", "dye_extract_indigo",
    "dye_extract_rose",    "dye_extract_teal",
]
_PIGMENT_COLORS = {
    "dye_extract_crimson": (170,  38,  50),
    "dye_extract_cobalt":  ( 40,  70, 168),
    "dye_extract_amber":   (200, 142,  50),
    "dye_extract_verdant": ( 60, 132,  70),
    "dye_extract_violet":  (110,  60, 160),
    "dye_extract_indigo":  ( 38,  50, 110),
    "dye_extract_rose":    (215,  90, 110),
    "dye_extract_teal":    ( 40, 150, 150),
}

_GRID_ROWS = 8
_GRID_COLS = 12


def _inv_count(player, item_id):
    return getattr(player, "inventory", {}).get(item_id, 0) or 0


def _consume(player, item_id, n=1):
    inv = player.inventory
    if inv.get(item_id, 0) >= n:
        inv[item_id] -= n
        if inv[item_id] <= 0:
            del inv[item_id]
        return True
    return False


class ManuscriptMixin:
    # ── Top-level ────────────────────────────────────────────────────────
    def _draw_scribes_desk(self, player, dt=0.0):
        self._manu_rects = {}
        screen = self.screen
        sw, sh = screen.get_size()
        pygame.draw.rect(screen, (40, 32, 24), (0, 0, sw, sh))
        pygame.draw.rect(screen, (90, 70, 50), (0, 0, sw, 38))
        title = self.font.render("Scribe's Desk", True, (245, 230, 200))
        screen.blit(title, (12, 8))
        bc = pygame.Rect(sw - 110, 6, 100, 26)
        pygame.draw.rect(screen, (140, 70, 60), bc)
        screen.blit(self.small.render("Close", True, (255, 255, 255)), (bc.x + 28, bc.y + 6))
        self._manu_rects["close"] = bc

        phase = getattr(self, "_manu_phase", "parchment")
        # phase tabs
        tabs = [("Parchment", "parchment"),
                ("Ink",       "ink"),
                ("Illuminate","illuminate"),
                ("Bind",      "bind")]
        x = 12
        for label, key in tabs:
            r = pygame.Rect(x, 46, 110, 26)
            active = (key == phase)
            pygame.draw.rect(screen, (130, 95, 55) if active else (75, 60, 45), r)
            screen.blit(self.small.render(label, True, (255, 245, 220)), (r.x + 8, r.y + 6))
            self._manu_rects[f"phase_{key}"] = r
            x += 118

        if phase == "parchment":
            self._draw_manu_parchment(player)
        elif phase == "ink":
            self._draw_manu_ink(player)
        elif phase == "illuminate":
            self._draw_manu_illuminate(player)
        elif phase == "bind":
            self._draw_manu_bind(player)

    def _handle_scribes_desk_click(self, pos, player, right=False):
        rects = getattr(self, "_manu_rects", {})
        if rects.get("close") and rects["close"].collidepoint(pos):
            self.refinery_open = False
            self.refinery_block_id = None
            return
        for key in ("parchment", "ink", "illuminate", "bind"):
            r = rects.get(f"phase_{key}")
            if r and r.collidepoint(pos):
                self._manu_phase = key
                return
        phase = getattr(self, "_manu_phase", "parchment")
        if phase == "parchment":
            self._click_manu_parchment(pos, player)
        elif phase == "ink":
            self._click_manu_ink(pos, player, right)
        elif phase == "illuminate":
            self._click_manu_illuminate(pos, player, right)
        elif phase == "bind":
            self._click_manu_bind(pos, player)

    # ── Phase 1: Parchment ──────────────────────────────────────────────
    def _draw_manu_parchment(self, player):
        screen = self.screen
        sw, sh = screen.get_size()
        info = ("Press parchment from 3 flax fibers (uses your current biome's character) "
                "or pick an existing raw parchment.")
        screen.blit(self.small.render(info, True, (220, 210, 180)), (16, 86))

        # Press button
        press_btn = pygame.Rect(16, 116, 220, 36)
        can_press = _inv_count(player, "flax_fiber") >= 3
        pygame.draw.rect(screen, (110, 80, 50) if can_press else (60, 55, 50), press_btn)
        label = f"Press Parchment  (flax × 3 : {_inv_count(player, 'flax_fiber')})"
        screen.blit(self.small.render(label, True, (255, 250, 225)), (press_btn.x + 10, press_btn.y + 10))
        self._manu_rects["press_parchment"] = press_btn

        y = 170
        screen.blit(self.font.render("Raw Parchments", True, (245, 230, 200)), (16, y))
        y += 28
        for i, p in enumerate(getattr(player, "raw_parchments", [])):
            r = pygame.Rect(16, y, sw - 32, 32)
            sel = (getattr(self, "_manu_selected", None) is p)
            pygame.draw.rect(screen, (95, 80, 60) if sel else (60, 50, 40), r)
            tone = BIOME_PARCHMENT_PROFILES.get(p.origin_biome, {}).get("tone", (220, 200, 170))
            pygame.draw.rect(screen, tone, (r.x + 4, r.y + 4, 24, 24))
            kingdom = p.origin_kingdom or UNKNOWN_KINGDOM
            text = f"#{i+1}  {kingdom} {p.parchment_variety}  cond {p.page_condition:.2f}"
            screen.blit(self.small.render(text, True, (240, 230, 210)), (r.x + 40, r.y + 8))
            self._manu_rects[f"parchment_{i}"] = (r, p)
            y += 36
            if y > sh - 40:
                break

    def _click_manu_parchment(self, pos, player):
        rects = self._manu_rects
        if rects.get("press_parchment") and rects["press_parchment"].collidepoint(pos):
            if _consume(player, "flax_fiber", 3):
                biome = self._player_current_biome(player)
                kingdom = kingdom_for_world_x(getattr(player, "world", None), int(player.x) // 16)
                parchment = player._manuscript_gen.generate_parchment(biome, kingdom)
                player.raw_parchments.append(parchment)
                player.pending_notifications.append(("Scribe", "Pressed Parchment", None))
            return
        for k, v in list(rects.items()):
            if k.startswith("parchment_") and isinstance(v, tuple):
                r, p = v
                if r.collidepoint(pos):
                    self._manu_selected = p
                    self._manu_phase = "ink"
                    self._manu_grid = [row[:] for row in p.illumination_grid]
                    return

    def _player_current_biome(self, player):
        try:
            bx = int(player.x // 16)
            biome = player.world.get_biodome(bx)
        except Exception:
            biome = "plains"
        return biome if biome in BIOME_PARCHMENT_PROFILES else "plains"

    # ── Phase 2: Ink ────────────────────────────────────────────────────
    def _draw_manu_ink(self, player):
        screen = self.screen
        if getattr(self, "_manu_selected", None) is None:
            screen.blit(self.small.render("Pick a parchment first.", True, (240, 200, 180)), (16, 96))
            return
        screen.blit(self.font.render("Choose Ink", True, (245, 230, 200)), (16, 90))
        y = 124
        for ink_key, info in INK_RECIPES.items():
            owned = _inv_count(player, ink_key)
            r = pygame.Rect(16, y, 340, 30)
            sel = (getattr(self, "_manu_ink", "") == ink_key)
            pygame.draw.rect(screen, (95, 80, 60) if sel else (60, 50, 40), r)
            pygame.draw.rect(screen, info["tone"], (r.x + 4, r.y + 4, 22, 22))
            text = f"{info['label']}  (×{owned})"
            screen.blit(self.small.render(text, True, (240, 230, 210)), (r.x + 32, r.y + 7))
            self._manu_rects[f"ink_{ink_key}"] = r
            y += 34

        # Pigment accents (right side)
        screen.blit(self.font.render("Pigment Accents (right-click to toggle)", True, (245, 230, 200)), (380, 90))
        y2 = 124
        selected = getattr(self, "_manu_pigments", set())
        for pk in _PIGMENT_KEYS:
            owned = _inv_count(player, pk)
            r = pygame.Rect(380, y2, 340, 26)
            on = pk in selected
            pygame.draw.rect(screen, (95, 80, 60) if on else (60, 50, 40), r)
            pygame.draw.rect(screen, _PIGMENT_COLORS.get(pk, (180, 180, 180)),
                             (r.x + 4, r.y + 4, 18, 18))
            screen.blit(self.small.render(f"{pk.replace('dye_extract_','').title()}  (×{owned})",
                                            True, (240, 230, 210)), (r.x + 30, r.y + 5))
            self._manu_rects[f"pig_{pk}"] = r
            y2 += 30

        # Continue
        cont = pygame.Rect(16, 480, 200, 32)
        pygame.draw.rect(screen, (90, 130, 80), cont)
        screen.blit(self.small.render("Continue → Illuminate", True, (255, 255, 255)),
                    (cont.x + 18, cont.y + 8))
        self._manu_rects["ink_continue"] = cont

    def _click_manu_ink(self, pos, player, right=False):
        rects = self._manu_rects
        if rects.get("ink_continue") and rects["ink_continue"].collidepoint(pos):
            if getattr(self, "_manu_ink", "") and _inv_count(player, self._manu_ink) >= 1:
                self._manu_phase = "illuminate"
            return
        for ink_key in INK_RECIPES:
            r = rects.get(f"ink_{ink_key}")
            if r and r.collidepoint(pos):
                if _inv_count(player, ink_key) >= 1:
                    self._manu_ink = ink_key
                return
        for pk in _PIGMENT_KEYS:
            r = rects.get(f"pig_{pk}")
            if r and r.collidepoint(pos):
                pigs = getattr(self, "_manu_pigments", None)
                if pigs is None:
                    pigs = set()
                    self._manu_pigments = pigs
                if pk in pigs:
                    pigs.discard(pk)
                elif _inv_count(player, pk) >= 1:
                    pigs.add(pk)
                return

    # ── Phase 3: Illuminate ─────────────────────────────────────────────
    def _draw_manu_illuminate(self, player):
        screen = self.screen
        sw, sh = screen.get_size()
        screen.blit(self.font.render("Illumination Grid", True, (245, 230, 200)), (16, 86))
        screen.blit(self.small.render("Click a cell to paint; right-click erases. Symmetry, coverage and variety raise quality.",
                                       True, (220, 210, 180)), (16, 116))

        ink_key = getattr(self, "_manu_ink", "ink_black")
        ink_color = INK_RECIPES.get(ink_key, INK_RECIPES["ink_black"])["tone"]
        palette = [(0, ink_color)]
        for i, pk in enumerate(sorted(getattr(self, "_manu_pigments", set()))):
            palette.append((i + 1, _PIGMENT_COLORS.get(pk, (200, 200, 200))))

        # Palette buttons
        px = 16
        py = 144
        for idx, (cid, col) in enumerate(palette):
            r = pygame.Rect(px, py, 36, 36)
            sel = (getattr(self, "_manu_active_color", 0) == cid)
            pygame.draw.rect(screen, (240, 235, 220) if sel else (60, 50, 40), r, 2)
            pygame.draw.rect(screen, col, (r.x + 4, r.y + 4, r.w - 8, r.h - 8))
            self._manu_rects[f"pal_{cid}"] = r
            px += 44

        # Grid
        if getattr(self, "_manu_grid", None) is None:
            self._manu_grid = [[None] * _GRID_COLS for _ in range(_GRID_ROWS)]
        grid = self._manu_grid
        cell = 38
        gx = 16
        gy = 200
        for r in range(_GRID_ROWS):
            for c in range(_GRID_COLS):
                rect = pygame.Rect(gx + c * cell, gy + r * cell, cell - 2, cell - 2)
                pygame.draw.rect(screen, (75, 60, 45), rect)
                v = grid[r][c]
                if v is not None:
                    if v < len(palette):
                        pygame.draw.rect(screen, palette[v][1],
                                         (rect.x + 4, rect.y + 4, rect.w - 8, rect.h - 8))
        self._manu_rects["grid_origin"] = (gx, gy, cell)

        # Stats + continue
        q = grid_quality(grid)
        screen.blit(self.small.render(f"Quality preview: {q*100:.0f}%", True, (245, 230, 200)),
                    (gx + _GRID_COLS * cell + 24, gy))
        cont = pygame.Rect(gx + _GRID_COLS * cell + 24, gy + 40, 200, 32)
        pygame.draw.rect(screen, (90, 130, 80), cont)
        screen.blit(self.small.render("Continue → Bind", True, (255, 255, 255)),
                    (cont.x + 32, cont.y + 8))
        self._manu_rects["illuminate_continue"] = cont

        clear = pygame.Rect(gx + _GRID_COLS * cell + 24, gy + 80, 200, 28)
        pygame.draw.rect(screen, (110, 60, 60), clear)
        screen.blit(self.small.render("Clear Grid", True, (255, 255, 255)),
                    (clear.x + 60, clear.y + 6))
        self._manu_rects["grid_clear"] = clear

    def _click_manu_illuminate(self, pos, player, right=False):
        rects = self._manu_rects
        if rects.get("illuminate_continue") and rects["illuminate_continue"].collidepoint(pos) and not right:
            self._manu_phase = "bind"
            return
        if rects.get("grid_clear") and rects["grid_clear"].collidepoint(pos) and not right:
            self._manu_grid = [[None] * _GRID_COLS for _ in range(_GRID_ROWS)]
            return
        for k, r in list(rects.items()):
            if k.startswith("pal_") and isinstance(r, pygame.Rect) and r.collidepoint(pos) and not right:
                self._manu_active_color = int(k.split("_", 1)[1])
                return
        origin = rects.get("grid_origin")
        if not origin:
            return
        gx, gy, cell = origin
        c = (pos[0] - gx) // cell
        r = (pos[1] - gy) // cell
        if 0 <= r < _GRID_ROWS and 0 <= c < _GRID_COLS:
            if right:
                self._manu_grid[r][c] = None
            else:
                self._manu_grid[r][c] = getattr(self, "_manu_active_color", 0)

    # ── Phase 4: Bind ───────────────────────────────────────────────────
    def _draw_manu_bind(self, player):
        screen = self.screen
        if getattr(self, "_manu_selected", None) is None:
            screen.blit(self.small.render("Pick a parchment first.", True, (240, 200, 180)), (16, 96))
            return
        screen.blit(self.font.render("Bind & Title", True, (245, 230, 200)), (16, 86))
        y = 124
        for bk, info in BINDING_PROFILES.items():
            owned = _inv_count(player, info["input_item"])
            r = pygame.Rect(16, y, 360, 30)
            sel = (getattr(self, "_manu_binding", "") == bk)
            pygame.draw.rect(screen, (95, 80, 60) if sel else (60, 50, 40), r)
            txt = f"{info['label']}  ({info['input_item']} ×1, have {owned})"
            screen.blit(self.small.render(txt, True, (240, 230, 210)), (r.x + 12, r.y + 7))
            self._manu_rects[f"bind_{bk}"] = r
            y += 34

        screen.blit(self.font.render("Content", True, (245, 230, 200)), (420, 90))
        y2 = 124
        for cat in CONTENT_CATEGORIES:
            r = pygame.Rect(420, y2, 220, 30)
            sel = (getattr(self, "_manu_category", "") == cat)
            pygame.draw.rect(screen, (95, 80, 60) if sel else (60, 50, 40), r)
            screen.blit(self.small.render(cat.title(), True, (240, 230, 210)), (r.x + 12, r.y + 7))
            self._manu_rects[f"cat_{cat}"] = r
            y2 += 34

        # Library bonus readout
        from library import update_player_library_bonus
        update_player_library_bonus(player)
        bonus = getattr(player, "library_quality_bonus", 0.0) or 0.0
        if bonus > 0:
            summary = getattr(player, "library_score_summary", None) or {}
            txt = (f"Library nearby — score {summary.get('total', 0):.1f}, "
                   f"quality floor +{int(bonus * 100)}%")
            screen.blit(self.small.render(txt, True, (180, 220, 200)), (16, 372))

        fin = pygame.Rect(16, 400, 260, 36)
        ok = (getattr(self, "_manu_binding", "") and getattr(self, "_manu_category", ""))
        pygame.draw.rect(screen, (90, 130, 80) if ok else (60, 55, 50), fin)
        screen.blit(self.small.render("Bind Manuscript", True, (255, 255, 255)), (fin.x + 70, fin.y + 10))
        self._manu_rects["finalize"] = fin

    def _click_manu_bind(self, pos, player):
        rects = self._manu_rects
        if rects.get("finalize") and rects["finalize"].collidepoint(pos):
            self._finalize_manuscript(player)
            return
        for bk in BINDING_PROFILES:
            r = rects.get(f"bind_{bk}")
            if r and r.collidepoint(pos):
                if _inv_count(player, BINDING_PROFILES[bk]["input_item"]) >= 1:
                    self._manu_binding = bk
                return
        for cat in CONTENT_CATEGORIES:
            r = rects.get(f"cat_{cat}")
            if r and r.collidepoint(pos):
                self._manu_category = cat
                return

    def _finalize_manuscript(self, player):
        parchment = getattr(self, "_manu_selected", None)
        binding = getattr(self, "_manu_binding", "")
        category = getattr(self, "_manu_category", "")
        ink_key = getattr(self, "_manu_ink", "")
        if not parchment or not binding or not category or not ink_key:
            return
        if not _consume(player, ink_key, 1):
            return
        if not _consume(player, BINDING_PROFILES[binding]["input_item"], 1):
            return
        grid = getattr(self, "_manu_grid", None) or [[None]*_GRID_COLS for _ in range(_GRID_ROWS)]
        pigments = list(getattr(self, "_manu_pigments", set()))
        # Refresh library bonus before binding so a well-stocked library lifts quality.
        from library import update_player_library_bonus
        update_player_library_bonus(player)
        manuscript = finalize_manuscript(parchment, ink_key, pigments, grid, binding, category,
                                         scribe_name="You")
        # Apply library quality bonus: lift penmanship and illumination floors.
        bonus = getattr(player, "library_quality_bonus", 0.0) or 0.0
        if bonus > 0:
            manuscript.penmanship = min(1.0, manuscript.penmanship + bonus * (1.0 - manuscript.penmanship))
            manuscript.illumination_quality = min(1.0, manuscript.illumination_quality + bonus * (1.0 - manuscript.illumination_quality))
        if parchment in player.raw_parchments:
            player.raw_parchments.remove(parchment)
        player.manuscripts.append(manuscript)
        player.discovered_manuscripts.add(f"{manuscript.origin_kingdom}_{manuscript.content_category}")
        player.pending_notifications.append(("Manuscript", manuscript.title, None))
        # reset state
        self._manu_selected = None
        self._manu_binding = ""
        self._manu_category = ""
        self._manu_phase = "parchment"

    # ── Lectern reader ──────────────────────────────────────────────────
    def _draw_lectern(self, player, dt=0.0):
        self._lectern_rects = {}
        screen = self.screen
        sw, sh = screen.get_size()
        pygame.draw.rect(screen, (40, 32, 24), (0, 0, sw, sh))
        screen.blit(self.font.render("Lectern — Your Manuscripts", True, (245, 230, 200)), (12, 12))
        bc = pygame.Rect(sw - 110, 6, 100, 26)
        pygame.draw.rect(screen, (140, 70, 60), bc)
        screen.blit(self.small.render("Close", True, (255, 255, 255)), (bc.x + 28, bc.y + 6))
        self._lectern_rects["close"] = bc

        y = 56
        if not player.manuscripts:
            screen.blit(self.small.render("No manuscripts yet — bind one at a Scribe's Desk.",
                                            True, (210, 200, 180)), (16, y))
            return
        sel = getattr(self, "_lectern_selected", None)
        for i, m in enumerate(player.manuscripts):
            r = pygame.Rect(16, y, 340, 32)
            on = (sel == i)
            pygame.draw.rect(screen, (95, 80, 60) if on else (60, 50, 40), r)
            stars = quality_stars(m)
            screen.blit(self.small.render(f"{m.title}  ★{stars}", True, (240, 230, 210)),
                        (r.x + 10, r.y + 7))
            self._lectern_rects[f"manu_{i}"] = r
            y += 36
            if y > sh - 40:
                break
        # Detail panel
        if sel is not None and 0 <= sel < len(player.manuscripts):
            self._draw_manuscript_detail(player.manuscripts[sel], 380, 56)

    def _draw_manuscript_detail(self, m, x, y):
        screen = self.screen
        screen.blit(self.font.render(m.title, True, (245, 230, 200)), (x, y))
        kingdom = m.origin_kingdom or UNKNOWN_KINGDOM
        meta = f"{kingdom} · {m.parchment_variety} · {m.content_category.title()}"
        screen.blit(self.small.render(meta, True, (210, 200, 180)), (x, y + 28))
        screen.blit(self.small.render(f"Scribe: {m.scribe_name}", True, (210, 200, 180)), (x, y + 46))
        screen.blit(self.small.render(f"Ink: {INK_RECIPES.get(m.ink_key, {}).get('label', '—')}",
                                       True, (210, 200, 180)), (x, y + 64))
        screen.blit(self.small.render(f"Binding: {BINDING_PROFILES.get(m.binding, {}).get('label', '—')}",
                                       True, (210, 200, 180)), (x, y + 82))
        screen.blit(self.small.render(f"Penmanship {m.penmanship:.2f}   Illumination {m.illumination_quality:.2f}",
                                       True, (210, 200, 180)), (x, y + 100))
        # Mini preview of the grid
        cell = 14
        gx, gy = x, y + 130
        for r in range(_GRID_ROWS):
            for c in range(_GRID_COLS):
                rect = pygame.Rect(gx + c * cell, gy + r * cell, cell - 1, cell - 1)
                pygame.draw.rect(screen, (75, 60, 45), rect)
                v = m.illumination_grid[r][c] if r < len(m.illumination_grid) and c < len(m.illumination_grid[0]) else None
                if v is not None:
                    if v == 0:
                        col = INK_RECIPES.get(m.ink_key, INK_RECIPES["ink_black"])["tone"]
                    else:
                        idx = v - 1
                        col = (200, 200, 200)
                        if 0 <= idx < len(m.pigment_keys):
                            col = _PIGMENT_COLORS.get(m.pigment_keys[idx], col)
                    pygame.draw.rect(screen, col, (rect.x + 2, rect.y + 2, rect.w - 4, rect.h - 4))

    # ── Bookcase ────────────────────────────────────────────────────────
    def _draw_bookcase(self, player, dt=0.0):
        from library import library_score
        self._bookcase_rects = {}
        screen = self.screen
        sw, sh = screen.get_size()
        pos = getattr(self, "active_bookcase_pos", None)
        slots = player.world.bookcase_contents.get(pos, [None] * 6) if pos else [None] * 6
        pygame.draw.rect(screen, (38, 28, 20), (0, 0, sw, sh))
        pygame.draw.rect(screen, (90, 65, 40), (0, 0, sw, 38))
        screen.blit(self.font.render("Bookcase", True, (245, 230, 200)), (12, 8))
        bc = pygame.Rect(sw - 110, 6, 100, 26)
        pygame.draw.rect(screen, (140, 70, 60), bc)
        screen.blit(self.small.render("Close", True, (255, 255, 255)), (bc.x + 28, bc.y + 6))
        self._bookcase_rects["close"] = bc

        # Library score
        score = library_score(slots)
        score_txt = (f"Library Score: {score['total']:.1f}   "
                     f"Categories: {score['categories']} / 5   "
                     f"Kingdoms: {score['kingdoms']}   "
                     f"Avg Stars: {score['avg_stars']:.1f}")
        screen.blit(self.small.render(score_txt, True, (220, 200, 170)), (12, 46))
        bonus_txt = f"Nearby Bonus → +{int(score['quality_bonus']*100)}% scribing quality"
        screen.blit(self.small.render(bonus_txt, True, (200, 180, 230)), (12, 64))

        # Left side: 6 shelf slots
        screen.blit(self.font.render("Shelves", True, (245, 230, 200)), (16, 92))
        slot_y = 122
        for i in range(6):
            r = pygame.Rect(16, slot_y, 360, 38)
            sel = (getattr(self, "_bookcase_sel_slot", None) == i)
            pygame.draw.rect(screen, (95, 80, 60) if sel else (60, 50, 40), r)
            m = slots[i] if i < len(slots) else None
            if m is not None:
                from manuscripts import INK_RECIPES, quality_stars
                spine = INK_RECIPES.get(m.ink_key, INK_RECIPES["ink_black"])["tone"]
                pygame.draw.rect(screen, spine, (r.x + 6, r.y + 6, 12, 26))
                stars = quality_stars(m)
                txt = f"{m.title}  ★{stars}  ({m.content_category.title()})"
                screen.blit(self.small.render(txt, True, (240, 230, 210)), (r.x + 28, r.y + 12))
            else:
                screen.blit(self.small.render(f"Slot {i + 1}: empty",
                                              True, (140, 130, 115)), (r.x + 16, r.y + 12))
            self._bookcase_rects[f"slot_{i}"] = r
            slot_y += 44

        # Right side: player manuscripts (loose)
        screen.blit(self.font.render("Your Manuscripts", True, (245, 230, 200)), (400, 92))
        screen.blit(self.small.render("(click to place into selected slot; click filled slot to withdraw)",
                                       True, (180, 170, 150)), (400, 116))
        y2 = 138
        for i, m in enumerate(player.manuscripts):
            r = pygame.Rect(400, y2, 360, 30)
            pygame.draw.rect(screen, (60, 50, 40), r)
            from manuscripts import INK_RECIPES, quality_stars
            spine = INK_RECIPES.get(m.ink_key, INK_RECIPES["ink_black"])["tone"]
            pygame.draw.rect(screen, spine, (r.x + 6, r.y + 4, 10, 22))
            stars = quality_stars(m)
            txt = f"{m.title}  ★{stars}  · {m.content_category.title()}"
            screen.blit(self.small.render(txt, True, (240, 230, 210)), (r.x + 24, r.y + 8))
            self._bookcase_rects[f"manu_{i}"] = r
            y2 += 34
            if y2 > sh - 40:
                break

    def _handle_bookcase_click(self, pos_xy, player, right=False):
        rects = getattr(self, "_bookcase_rects", {})
        if rects.get("close") and rects["close"].collidepoint(pos_xy):
            self.refinery_open = False
            self.refinery_block_id = None
            self.active_bookcase_pos = None
            self._bookcase_sel_slot = None
            return
        bc_pos = getattr(self, "active_bookcase_pos", None)
        if bc_pos is None:
            return
        slots = player.world.bookcase_contents.setdefault(bc_pos, [None] * 6)
        # Slot clicks
        for i in range(6):
            r = rects.get(f"slot_{i}")
            if r and r.collidepoint(pos_xy):
                if slots[i] is not None:
                    # Withdraw
                    player.manuscripts.append(slots[i])
                    slots[i] = None
                    self._bookcase_sel_slot = None
                else:
                    self._bookcase_sel_slot = i
                return
        # Manuscript-list clicks
        for i, m in enumerate(player.manuscripts):
            r = rects.get(f"manu_{i}")
            if r and r.collidepoint(pos_xy):
                # Place into selected empty slot, or first empty slot
                target = self._bookcase_sel_slot
                if target is None or slots[target] is not None:
                    target = next((idx for idx, v in enumerate(slots) if v is None), None)
                if target is not None:
                    slots[target] = m
                    player.manuscripts.pop(i)
                    self._bookcase_sel_slot = None
                return

    def _handle_lectern_click(self, pos, player, right=False):
        rects = getattr(self, "_lectern_rects", {})
        if rects.get("close") and rects["close"].collidepoint(pos):
            self.refinery_open = False
            self.refinery_block_id = None
            return
        for k, r in rects.items():
            if k.startswith("manu_") and r.collidepoint(pos):
                self._lectern_selected = int(k.split("_", 1)[1])
                return
