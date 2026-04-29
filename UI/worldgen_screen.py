"""Animated worldgen screen — shows phases 1-4 of generation.

Flow:
  Phase 1 — geography sweeps in left-to-right (cell strip + elevation silhouette).
  Phase 2 — kingdom flags drop onto each capital with their heraldry color.
  Phase 3 — 500-year history plays through year-by-year; settlement dots
            appear / grow / explode into red Xs as chronicle events fire.
            SPACE pauses, 1/2/3/4 set 0.5x/1x/2x/4x playback.
  Phase 4 — final state shown; click the map to choose a spawn point,
            then click "Begin".

ENTER skips to the end. Returns the WorldPlan with optional spawn_world_x.
"""

import pygame

from constants import SCREEN_W, SCREEN_H
from worldgen import generate_world


# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------

_BIODOME_COLOR = {
    "temperate":       ( 70, 130,  60),
    "boreal":          ( 50, 100,  70),
    "birch_forest":    (140, 175, 110),
    "redwood":         ( 95,  70,  55),
    "jungle":          ( 30, 105,  50),
    "tropical":        ( 60, 150,  80),
    "wetland":         ( 80, 110,  90),
    "swamp":           ( 60,  80,  60),
    "savanna":         (175, 165,  90),
    "steppe":          (190, 180, 110),
    "arid_steppe":     (200, 175, 120),
    "wasteland":       (110,  95,  80),
    "alpine_mountain": (220, 225, 235),
    "rocky_mountain":  (140, 130, 125),
    "rolling_hills":   (140, 170,  95),
    "steep_hills":     (130, 150,  90),
    "desert":          (225, 200, 130),
    "tundra":          (210, 220, 230),
    "beach":           (230, 215, 165),
    "coastal":         (140, 175, 200),
    "ocean":           ( 35,  85, 145),
    "pacific_island":  (180, 200, 140),
    "canyon":          (170, 110,  80),
    "mediterranean":   (190, 175, 110),
    "east_asian":      (110, 140, 110),
    "south_asian":     (160, 140,  90),
}

_BG     = ( 18,  20,  28)
_FG     = (235, 235, 240)
_DIM    = (140, 140, 150)
_SKY    = ( 38,  44,  58)
_GROUND = ( 64,  56,  46)
_PANEL  = ( 28,  32,  40)


# ---------------------------------------------------------------------------
# Settlement state replay
# ---------------------------------------------------------------------------

def _build_year_states(plan):
    """For each year 0..history_years, return dict[sid] -> (state, tier).

    Cheap to build (single linear pass over chronicle); used to render the
    history-phase animation.
    """
    states = {}
    for s in plan.settlements.values():
        # Settlements founded mid-sim should appear at their founded_year.
        states[s.settlement_id] = ("alive" if s.founded_year == 0 else "absent",
                                   s.tier if s.founded_year == 0 else "hamlet",
                                   s.world_x, s.kingdom_id, s.is_capital)

    snapshots = []
    cursor = 0
    chronicle = plan.chronicle
    for year in range(plan.history_years + 1):
        # Apply all events at <= year that we haven't yet.
        while cursor < len(chronicle) and chronicle[cursor].year <= year:
            ev = chronicle[cursor]
            kind = ev.kind
            actors = ev.actors
            if kind == "found_settlement":
                sid = actors.get("settlement")
                s = plan.settlements.get(sid)
                if s is not None:
                    st = states[sid]
                    states[sid] = ("alive", "hamlet", s.world_x, s.kingdom_id, s.is_capital)
            elif kind in ("sack", "earthquake"):
                sid = actors.get("settlement")
                if sid in states:
                    cur = states[sid]
                    states[sid] = ("ruin", cur[1], cur[2], cur[3], cur[4])
            elif kind in ("abandon", "merge"):
                sid = actors.get("settlement") or actors.get("small")
                if sid in states:
                    cur = states[sid]
                    states[sid] = ("abandoned", cur[1], cur[2], cur[3], cur[4])
            elif kind == "grow_to_tier":
                sid = actors.get("settlement")
                s = plan.settlements.get(sid)
                if sid in states and s is not None:
                    cur = states[sid]
                    # tier increases monotonically; pull from final settlement record
                    states[sid] = (cur[0], s.tier, cur[2], cur[3], cur[4])
            elif kind == "shrink":
                sid = actors.get("settlement")
                if sid in states:
                    cur = states[sid]
                    # walk one tier down
                    tiers = ["hamlet", "village", "town", "city", "metropolis", "megalopolis"]
                    if cur[1] in tiers and tiers.index(cur[1]) > 0:
                        new_tier = tiers[tiers.index(cur[1]) - 1]
                        states[sid] = (cur[0], new_tier, cur[2], cur[3], cur[4])
            elif kind == "annex":
                sid = actors.get("settlement")
                attacker = actors.get("attacker")
                if sid in states and attacker is not None:
                    cur = states[sid]
                    states[sid] = (cur[0], cur[1], cur[2], attacker, cur[4])
            elif kind == "revolt_defect":
                sid = actors.get("settlement")
                new_k = actors.get("new_kingdom")
                if sid in states and new_k is not None:
                    cur = states[sid]
                    states[sid] = (cur[0], cur[1], cur[2], new_k, cur[4])
            elif kind == "revolt_independent":
                sid = actors.get("settlement")
                if sid in states:
                    cur = states[sid]
                    states[sid] = (cur[0], cur[1], cur[2], -1, cur[4])
            elif kind == "kingdom_split":
                breakaway_kid = actors.get("breakaway")
                # All settlements currently belonging to the breakaway kingdom
                # are moved to it in the post-sim state; pull from final record.
                if breakaway_kid is not None:
                    new_kingdom = plan.kingdoms.get(breakaway_kid)
                    if new_kingdom is not None:
                        for sid in new_kingdom.member_settlement_ids:
                            if sid in states:
                                cur = states[sid]
                                states[sid] = (cur[0], cur[1], cur[2], breakaway_kid, cur[4])
            elif kind == "kingdom_reborn":
                new_kid = actors.get("kingdom")
                if new_kid is not None:
                    new_kingdom = plan.kingdoms.get(new_kid)
                    if new_kingdom is not None:
                        for sid in new_kingdom.member_settlement_ids:
                            if sid in states:
                                cur = states[sid]
                                states[sid] = ("alive", cur[1], cur[2], new_kid, cur[4])
            cursor += 1
        snapshots.append({sid: tup for sid, tup in states.items()})
    return snapshots


# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------

def _sea_level_y(strip_rect):
    """Y at which the ocean surface sits within the silhouette area."""
    _, y0, _, h = strip_rect
    band_h = h // 4
    silhouette_h = h - band_h
    # Matches the terrain formula at e≈0.4 — typical coast elevation.
    return y0 + band_h + int(silhouette_h * (0.20 + 0.70 * (1 - 0.40)))


def _draw_strip(surface, plan, strip_rect, cells_visible: int):
    """Top half: biodome color band + elevation silhouette."""
    x0, y0, w, h = strip_rect
    band_h = h // 4
    silhouette_h = h - band_h
    span = plan.span
    cell_px = w / span
    sea_y = _sea_level_y(strip_rect)

    # Sky behind elevation silhouette.
    pygame.draw.rect(surface, _SKY, (x0, y0 + band_h, w, silhouette_h))

    for i in range(min(cells_visible, span)):
        c = plan.cells[i]
        cx = x0 + int(i * cell_px)
        cw = max(1, int((i + 1) * cell_px) - int(i * cell_px))

        # Biodome band.
        color = _BIODOME_COLOR.get(c.biodome, (120, 120, 120))
        pygame.draw.rect(surface, color, (cx, y0, cw, band_h))

        # Elevation silhouette under the band.
        e = c.elevation
        if c.biodome == "ocean":
            # Water sits at sea level — only the lower portion is blue,
            # the upper portion is sky.
            pygame.draw.rect(surface, _BIODOME_COLOR["ocean"],
                             (cx, sea_y, cw, y0 + h - sea_y))
        else:
            terrain_h = int(silhouette_h * (0.20 + 0.70 * (1 - e)))
            pygame.draw.rect(surface, _GROUND,
                             (cx, y0 + band_h + terrain_h, cw, silhouette_h - terrain_h))


def _draw_kingdom_flags(surface, plan, strip_rect, alpha_progress: float, kingdoms_visible: list):
    """Phase 2: drop a flag at each capital position with the kingdom's color."""
    x0, y0, w, h = strip_rect
    band_h = h // 4
    span = plan.span
    cell_px = w / span
    for k in kingdoms_visible:
        cap = plan.settlements.get(k.capital_settlement_id)
        if cap is None:
            continue
        col = tuple(k.color)
        # Convert capital world_x → cell_index → screen x
        idx = (cap.world_x - plan.world_min_x) / plan.cell_width
        sx = x0 + int(idx * cell_px)
        # Pole.
        pole_top = y0 - 18
        pygame.draw.line(surface, _FG, (sx, y0), (sx, pole_top), 2)
        # Flag triangle.
        pygame.draw.polygon(surface, col,
                            [(sx, pole_top), (sx + 12, pole_top + 6), (sx, pole_top + 12)])


def _draw_settlement_dots(surface, plan, strip_rect, year_state: dict, kingdom_colors: dict):
    """Phase 3: render every active settlement at its state, color = kingdom."""
    x0, y0, w, h = strip_rect
    band_h = h // 4
    span = plan.span
    cell_px = w / span
    y_dots = y0 + band_h - 5

    for sid, (state, tier, world_x, kingdom_id, is_cap) in year_state.items():
        if state == "absent":
            continue
        idx = (world_x - plan.world_min_x) / plan.cell_width
        sx = x0 + int(idx * cell_px)
        col = kingdom_colors.get(kingdom_id, (180, 180, 180))

        size = {"hamlet": 2, "village": 3, "town": 4,
                "city": 5, "metropolis": 6, "megalopolis": 7}.get(tier, 2)

        if state == "ruin":
            pygame.draw.line(surface, (180, 50, 50), (sx - 3, y_dots - 3), (sx + 3, y_dots + 3), 2)
            pygame.draw.line(surface, (180, 50, 50), (sx - 3, y_dots + 3), (sx + 3, y_dots - 3), 2)
        elif state == "abandoned":
            pygame.draw.circle(surface, (110, 110, 110), (sx, y_dots), size, 1)
        else:
            pygame.draw.rect(surface, col, (sx - size, y_dots - size, size * 2, size * 2))
            if is_cap:
                pygame.draw.rect(surface, _FG, (sx - size - 1, y_dots - size - 1,
                                                 size * 2 + 2, size * 2 + 2), 1)


def _draw_panel(surface, font_l, font_s, plan, phase: str, year: int,
                recent_events: list, kingdoms_visible: list):
    """Bottom panel: phase label + year ticker + last 3 chronicle lines + kingdom legend."""
    panel_y = SCREEN_H - 200
    pygame.draw.rect(surface, _PANEL, (0, panel_y, SCREEN_W, 200))
    pygame.draw.line(surface, _DIM, (0, panel_y), (SCREEN_W, panel_y), 1)

    # Phase label.
    lbl = font_l.render(phase, True, _FG)
    surface.blit(lbl, (24, panel_y + 16))

    # Year ticker upper-right.
    if year >= 0:
        yr = font_l.render(f"Year {year} / {plan.history_years}", True, _FG)
        surface.blit(yr, (SCREEN_W - yr.get_width() - 24, panel_y + 16))

    # Last 3 events.
    for i, ev in enumerate(recent_events[-3:]):
        line = f"Yr {ev.year} — {ev.text}"
        surf = font_s.render(line[:120], True, _DIM)
        surface.blit(surf, (24, panel_y + 64 + i * 22))

    # Kingdom legend (right side).
    lx = SCREEN_W - 280
    ly = panel_y + 64
    title = font_s.render("Kingdoms", True, _FG)
    surface.blit(title, (lx, ly))
    for i, k in enumerate(kingdoms_visible[:6]):
        row_y = ly + 22 + i * 18
        pygame.draw.rect(surface, tuple(k.color), (lx, row_y + 4, 12, 10))
        nm = font_s.render(k.name + (" (fallen)" if k.fallen_year != -1 else ""),
                           True, _DIM if k.fallen_year != -1 else _FG)
        surface.blit(nm, (lx + 18, row_y))


def _draw_skip_hint(surface, font_s, paused: bool, speed: float, in_history: bool):
    if in_history:
        state = "PAUSED" if paused else f"{speed:g}x"
        msg = f"SPACE pause  |  1/2/3/4 speed ({state})  |  ENTER skip"
    else:
        msg = "ENTER to skip"
    txt = font_s.render(msg, True, _DIM)
    surface.blit(txt, (SCREEN_W - txt.get_width() - 16, SCREEN_H - 26))


def _draw_spawn_hint(surface, font_s):
    txt = font_s.render("Click the map to choose your spawn point", True, (220, 200, 120))
    surface.blit(txt, (16, SCREEN_H - 26))


def _draw_spawn_marker(surface, plan, strip_rect, spawn_world_x):
    """Yellow diamond + flag pole at the chosen spawn position."""
    if spawn_world_x is None:
        return
    x0, y0, w, h = strip_rect
    band_h = h // 4
    cell_px = w / plan.span
    idx = (spawn_world_x - plan.world_min_x) / plan.cell_width
    sx = x0 + int(idx * cell_px)
    sy = y0 + band_h - 5
    pygame.draw.line(surface, (250, 220, 80), (sx, y0 - 32), (sx, sy), 2)
    pygame.draw.polygon(surface, (250, 220, 80),
                        [(sx, sy - 9), (sx + 7, sy), (sx, sy + 9), (sx - 7, sy)])
    pygame.draw.polygon(surface, _FG,
                        [(sx, sy - 9), (sx + 7, sy), (sx, sy + 9), (sx - 7, sy)], 1)


def _screen_x_to_world_x(plan, strip_rect, mx):
    x0, _, w, _ = strip_rect
    cell_px = w / plan.span
    idx = (mx - x0) / cell_px
    if idx < 0 or idx >= plan.span:
        return None
    return int(plan.world_min_x + idx * plan.cell_width + plan.cell_width // 2)


def _pick_spawn(plan, strip_rect, mx, my):
    """Convert click → world_x. Snap to nearest alive settlement if within ~24px.

    Returns None for clicks outside the strip or on ocean cells.
    """
    x0, y0, w, h = strip_rect
    if not (x0 <= mx < x0 + w and y0 <= my < y0 + h):
        return None
    raw = _screen_x_to_world_x(plan, strip_rect, mx)
    if raw is None:
        return None
    cell_px = w / plan.span
    best_sid = None
    best_dx = 24
    for s in plan.settlements.values():
        if s.state != "alive":
            continue
        idx = (s.world_x - plan.world_min_x) / plan.cell_width
        sx = x0 + int(idx * cell_px)
        d = abs(sx - mx)
        if d < best_dx:
            best_dx = d
            best_sid = s.settlement_id
    if best_sid is not None:
        return plan.settlements[best_sid].world_x
    cell = plan.cell_for_x(raw)
    if cell is not None and cell.biodome == "ocean":
        return None
    return raw


def _draw_begin_button(surface, font_l, btn_rect, hovered: bool):
    col = (60, 130, 70) if hovered else (45, 105, 55)
    pygame.draw.rect(surface, col, btn_rect, border_radius=6)
    pygame.draw.rect(surface, _FG, btn_rect, 2, border_radius=6)
    txt = font_l.render("Begin >", True, _FG)
    surface.blit(txt, (btn_rect.x + (btn_rect.w - txt.get_width()) // 2,
                       btn_rect.y + (btn_rect.h - txt.get_height()) // 2))


# ---------------------------------------------------------------------------
# Main entry
# ---------------------------------------------------------------------------

def show_worldgen(screen, seed: int, span=None):
    """Run the animated worldgen screen and return the finished WorldPlan.

    Generates the plan synchronously up front (~1s for span 400), then plays
    the four phases as an animation. Press SPACE/ENTER to skip to the Begin
    button at any time.
    """
    plan = generate_world(seed=seed, span=span)
    snapshots = _build_year_states(plan)

    font_l = pygame.font.SysFont("arial", 22, bold=True)
    font_s = pygame.font.SysFont("arial", 14)

    clock = pygame.time.Clock()
    strip_rect = (40, 60, SCREEN_W - 80, SCREEN_H - 280)

    # Per-phase pacing (seconds).
    PHASE1_S = 1.5     # geography sweep
    PHASE2_S = 1.0     # kingdom flags drop
    PHASE3_S = 5.0     # 500-year sim playback
    PHASE4_S = 0.5     # finalize flash

    elapsed = 0.0
    skip_to_done = False
    done = False
    paused = False
    speed = 1.0
    spawn_world_x = None
    btn_rect = pygame.Rect(SCREEN_W // 2 - 100, SCREEN_H - 70, 200, 44)

    kingdom_colors = {kid: tuple(k.color) for kid, k in plan.kingdoms.items()}

    total_s = PHASE1_S + PHASE2_S + PHASE3_S + PHASE4_S

    while not done:
        dt = clock.tick(60) / 1000.0
        in_history = PHASE1_S + PHASE2_S <= elapsed < PHASE1_S + PHASE2_S + PHASE3_S
        ready = elapsed >= total_s
        if not skip_to_done and not (paused and in_history):
            step = dt * (speed if in_history else 1.0)
            elapsed += step
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN:
                    skip_to_done = True
                    elapsed = total_s
                elif ev.key == pygame.K_SPACE and in_history:
                    paused = not paused
                elif ev.key == pygame.K_1:
                    speed = 0.5
                elif ev.key == pygame.K_2:
                    speed = 1.0
                elif ev.key == pygame.K_3:
                    speed = 2.0
                elif ev.key == pygame.K_4:
                    speed = 4.0
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mx, my = ev.pos
                if ready:
                    if btn_rect.collidepoint(mx, my):
                        done = True
                    else:
                        picked = _pick_spawn(plan, strip_rect, mx, my)
                        if picked is not None:
                            spawn_world_x = picked

        screen.fill(_BG)

        # Phase progress.
        if elapsed < PHASE1_S:
            phase = "Phase 1 — Geography"
            cells_visible = int(plan.span * (elapsed / PHASE1_S))
            _draw_strip(screen, plan, strip_rect, cells_visible)
            year_for_panel = -1
            recent = []
            kvis = []
        elif elapsed < PHASE1_S + PHASE2_S:
            phase = "Phase 2 — Kingdoms"
            _draw_strip(screen, plan, strip_rect, plan.span)
            kvis = list(plan.kingdoms.values())
            _draw_kingdom_flags(screen, plan, strip_rect,
                                (elapsed - PHASE1_S) / PHASE2_S, kvis)
            year_for_panel = -1
            recent = []
        elif elapsed < PHASE1_S + PHASE2_S + PHASE3_S:
            phase = "Phase 3 — History"
            _draw_strip(screen, plan, strip_rect, plan.span)
            kvis = list(plan.kingdoms.values())
            t_h = (elapsed - PHASE1_S - PHASE2_S) / PHASE3_S
            year = min(plan.history_years, int(t_h * plan.history_years))
            year_state = snapshots[year]
            _draw_settlement_dots(screen, plan, strip_rect, year_state, kingdom_colors)
            _draw_kingdom_flags(screen, plan, strip_rect, 1.0, kvis)
            recent = [e for e in plan.chronicle if e.year <= year][-3:]
            year_for_panel = year
        else:
            phase = "Ready" if elapsed >= PHASE1_S + PHASE2_S + PHASE3_S + PHASE4_S else "Phase 4 — Finalizing"
            _draw_strip(screen, plan, strip_rect, plan.span)
            year_state = snapshots[-1]
            kvis = list(plan.kingdoms.values())
            _draw_settlement_dots(screen, plan, strip_rect, year_state, kingdom_colors)
            _draw_kingdom_flags(screen, plan, strip_rect, 1.0, kvis)
            recent = plan.chronicle[-3:]
            year_for_panel = plan.history_years

        _draw_spawn_marker(screen, plan, strip_rect, spawn_world_x)
        _draw_panel(screen, font_l, font_s, plan, phase, year_for_panel, recent, kvis)
        _draw_skip_hint(screen, font_s, paused, speed, in_history)

        # Begin button only when ready.
        if ready:
            _draw_spawn_hint(screen, font_s)
            mx, my = pygame.mouse.get_pos()
            _draw_begin_button(screen, font_l, btn_rect, btn_rect.collidepoint(mx, my))

        pygame.display.flip()

    if spawn_world_x is not None:
        plan.spawn_world_x = spawn_world_x
    return plan
