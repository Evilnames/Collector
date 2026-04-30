"""World setup screen — configure world parameters before generation."""

import random
import pygame
from constants import SCREEN_W, SCREEN_H

_BG   = ( 18,  20,  28)
_FG   = (235, 235, 240)
_DIM  = (140, 140, 150)
_SEL  = ( 55, 110, 175)
_HOV  = ( 38,  70, 120)
_NORM = ( 38,  44,  58)

# ---------------------------------------------------------------------------
# Option definitions
# ---------------------------------------------------------------------------

_OPTIONS = [
    {
        "key": "size",
        "label": "World Size",
        "choices": ["small",   "medium",  "large",         "huge",          "epic"],
        "labels":  ["Small",   "Medium",  "Large",         "Huge",          "Epic"],
        "descs":   ["~6,400 blocks", "~16,000 blocks", "~25,600 blocks",
                    "~51,200 blocks", "~76,800 blocks"],
        "default": "large",
    },
    {
        "key": "history",
        "label": "History",
        "choices": ["young",               "standard",           "ancient"],
        "labels":  ["Young",               "Standard",           "Ancient"],
        "descs":   ["Less developed, more alive settlements",
                    "Balanced civilisations",
                    "Many ruins and fallen kingdoms"],
        "default": "standard",
    },
    {
        "key": "oceans",
        "label": "Oceans",
        "choices": ["sparse",                          "standard",          "abundant"],
        "labels":  ["Sparse",                          "Standard",          "Abundant"],
        "descs":   ["Mostly land — fewer sea crossings",
                    "Balanced land and sea",
                    "Many oceans — island chains and crossings"],
        "default": "standard",
    },
    {
        "key": "civilizations",
        "label": "Civilizations",
        "choices": ["isolated",           "standard",            "fragmented"],
        "labels":  ["Isolated",           "Standard",            "Fragmented"],
        "descs":   ["Few large kingdoms",
                    "Balanced kingdoms",
                    "Many small competing kingdoms"],
        "default": "standard",
    },
]

_SIZE_TO_SPAN    = {"small": 100, "medium": 250, "large": 400, "huge": 800, "epic": 1200}
_HISTORY_TO_YEARS = {"young": 200, "standard": 500, "ancient": 1000}
_OCEANS_TO_COUNT  = {"sparse": 1,  "standard": 2,   "abundant": 4}
_CIV_TO_KINGDOMS  = {"isolated": 0.8, "standard": 2.2, "fragmented": 4.5}


def _build_overrides(sel: dict) -> dict:
    oc = _OCEANS_TO_COUNT[sel["oceans"]]
    return {
        "world_span":                      _SIZE_TO_SPAN[sel["size"]],
        "history_years":                   _HISTORY_TO_YEARS[sel["history"]],
        "ocean_count_default":             oc,
        "ocean_count_variance":            1 if oc == 1 else 2,
        "starting_kingdoms_per_100_cells": _CIV_TO_KINGDOMS[sel["civilizations"]],
    }


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

_ROW_Y    = [148, 238, 328, 418]
_BTN_H    = 44
_LABEL_X  = 60
_BTN_X0   = 310
_BTN_GAP  = 10
_BIG_W    = 112   # 5-choice row
_STD_W    = 158   # 3-choice row


def _btn_rects(ri: int):
    opt = _OPTIONS[ri]
    n   = len(opt["choices"])
    bw  = _BIG_W if n == 5 else _STD_W
    y   = _ROW_Y[ri]
    return [pygame.Rect(_BTN_X0 + i * (bw + _BTN_GAP), y, bw, _BTN_H) for i in range(n)]


def _draw_row(surf, font_l, font_s, ri: int, selected: str, hover_ci: int):
    opt   = _OPTIONS[ri]
    y     = _ROW_Y[ri]
    rects = _btn_rects(ri)
    n     = len(opt["choices"])
    bw    = _BIG_W if n == 5 else _STD_W

    # Row label
    lbl = font_l.render(opt["label"], True, _FG)
    surf.blit(lbl, (_LABEL_X, y + (_BTN_H - lbl.get_height()) // 2))

    # Buttons
    for ci, (rect, choice, label) in enumerate(zip(rects, opt["choices"], opt["labels"])):
        col = _SEL if choice == selected else (_HOV if ci == hover_ci else _NORM)
        bdr = _FG  if choice == selected else _DIM
        pygame.draw.rect(surf, col, rect, border_radius=6)
        pygame.draw.rect(surf, bdr, rect, 1, border_radius=6)
        t = font_s.render(label, True, _FG)
        surf.blit(t, (rect.x + (rect.w - t.get_width()) // 2,
                      rect.y + (rect.h - t.get_height()) // 2))

    # Description of current selection (right of buttons)
    sel_ci = opt["choices"].index(selected)
    desc   = opt["descs"][sel_ci]
    end_x  = _BTN_X0 + n * bw + (n - 1) * _BTN_GAP + 18
    d = font_s.render(desc, True, _DIM)
    surf.blit(d, (end_x, y + (_BTN_H - d.get_height()) // 2))


# ---------------------------------------------------------------------------
# Main entry
# ---------------------------------------------------------------------------

def show_world_setup(screen, seed: int):
    """Display world setup choices and return (config_overrides, seed)."""
    font_l = pygame.font.SysFont("arial", 22, bold=True)
    font_s = pygame.font.SysFont("arial", 14)
    clock  = pygame.time.Clock()

    selections = {opt["key"]: opt["default"] for opt in _OPTIONS}

    seed_y      = 508
    reroll_rect = pygame.Rect(_BTN_X0, seed_y, 110, 36)
    begin_rect  = pygame.Rect(SCREEN_W // 2 - 120, SCREEN_H - 78, 240, 50)

    done = False
    while not done:
        mx, my = pygame.mouse.get_pos()
        clock.tick(60)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN:
                done = True
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                for ri, opt in enumerate(_OPTIONS):
                    for ci, (rect, choice) in enumerate(zip(_btn_rects(ri), opt["choices"])):
                        if rect.collidepoint(mx, my):
                            selections[opt["key"]] = choice
                if reroll_rect.collidepoint(mx, my):
                    seed = random.randint(0, 2**31 - 1)
                if begin_rect.collidepoint(mx, my):
                    done = True

        screen.fill(_BG)

        # Title
        title = font_l.render("New World", True, _FG)
        screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 48))
        sub = font_s.render("Configure your world before generation begins", True, _DIM)
        screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 80))
        pygame.draw.line(screen, _DIM, (60, 112), (SCREEN_W - 60, 112), 1)

        # Option rows
        for ri, opt in enumerate(_OPTIONS):
            hover_ci = next(
                (ci for ci, r in enumerate(_btn_rects(ri)) if r.collidepoint(mx, my)),
                -1,
            )
            _draw_row(screen, font_l, font_s, ri, selections[opt["key"]], hover_ci)

        # Divider before seed
        pygame.draw.line(screen, _DIM, (60, seed_y - 18), (SCREEN_W - 60, seed_y - 18), 1)

        # Seed row
        sl = font_l.render("Seed", True, _FG)
        screen.blit(sl, (_LABEL_X, seed_y + (36 - sl.get_height()) // 2))
        sv = font_s.render(str(seed), True, _DIM)
        screen.blit(sv, (_BTN_X0 + 128, seed_y + (36 - sv.get_height()) // 2))
        rcol = _HOV if reroll_rect.collidepoint(mx, my) else _NORM
        pygame.draw.rect(screen, rcol, reroll_rect, border_radius=6)
        pygame.draw.rect(screen, _DIM, reroll_rect, 1, border_radius=6)
        rt = font_s.render("Reroll", True, _FG)
        screen.blit(rt, (reroll_rect.x + (reroll_rect.w - rt.get_width()) // 2,
                         reroll_rect.y + (reroll_rect.h - rt.get_height()) // 2))

        # Begin button
        bcol = (60, 130, 70) if begin_rect.collidepoint(mx, my) else (45, 105, 55)
        pygame.draw.rect(screen, bcol, begin_rect, border_radius=6)
        pygame.draw.rect(screen, _FG, begin_rect, 2, border_radius=6)
        bt = font_l.render("Generate World  →", True, _FG)
        screen.blit(bt, (begin_rect.x + (begin_rect.w - bt.get_width()) // 2,
                         begin_rect.y + (begin_rect.h - bt.get_height()) // 2))

        hint = font_s.render("ENTER to begin with defaults", True, _DIM)
        screen.blit(hint, (SCREEN_W - hint.get_width() - 16, SCREEN_H - 22))

        pygame.display.flip()

    return _build_overrides(selections), seed
