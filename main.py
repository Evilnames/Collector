import sys
import time
import random
import json
from pathlib import Path
import pygame
from world import World
from player import Player
from renderer import Renderer
from UI import UI
from research import ResearchTree
from constants import SCREEN_W, SCREEN_H, FPS, BLOCK_SIZE
from automations import Automation, AUTOMATION_DEFS, AUTOMATION_ITEM, FARM_BOT_ITEM, Backhoe
from constants import PLAYER_W
from save_manager import SaveManager
from blocks import GEM_CUTTER_BLOCK, ROASTER_BLOCK, GRAPE_PRESS_BLOCK, FERMENTATION_BLOCK, COMPOST_BIN_BLOCK, STILL_BLOCK, STABLE_BLOCK, KENNEL_BLOCK, OXIDATION_STATION_BLOCK, SPINNING_WHEEL_BLOCK, LOOM_BLOCK, DAIRY_VAT_BLOCK, AGING_CAVE_BLOCK, FLETCHING_TABLE_BLOCK, ELEVATOR_STOP_BLOCK, WILDFLOWER_DISPLAY_BLOCK, WINE_CELLAR_BLOCK, BARREL_ROOM_BLOCK, TRADE_BLOCK, BREW_KETTLE_BLOCK, FERM_VESSEL_BLOCK, TAPROOM_BLOCK, CHICKEN_COOP_BLOCK, GAMBLING_TABLE, BET_COUNTER, TEA_HOUSE_BLOCK, TRAINING_PADDOCK_BLOCK, BEEHIVE_BLOCK, MEAD_VAT_BLOCK, MEAD_CELLAR_BLOCK, SALTING_RACK_BLOCK, CURING_CELLAR_BLOCK, BOOKCASE_BLOCK, FALCONER_PERCH, MEWS_BLOCK, FEED_TROUGH_BLOCK
from elevators import ElevatorCar
from minecarts import Minecart

SETTINGS_PATH = Path(__file__).parent / "settings.json"


def _nearby_light_trap(world, player):
    """Return (bx, by) of a light trap block within 2 blocks of the player, or None."""
    from blocks import LIGHT_TRAP_BLOCK as _LTB
    px = int(player.x // BLOCK_SIZE)
    py = int(player.y // BLOCK_SIZE)
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            bx, by = px + dx, py + dy
            if world.get_block(bx, by) == _LTB:
                return (bx, by)
    return None


def _nearby_guild_hall(world, player):
    """Return (bx, by, guild_id) of the nearest Guild Hall within 3 blocks, or None.

    `guild_id` is None if the Hall predates the per-guild registry (older save).
    """
    from blocks import GUILD_HALL_VARIANTS as _GHV
    from guild_worldgen import guild_at_hall
    px = int(player.x // BLOCK_SIZE)
    py = int(player.y // BLOCK_SIZE)
    for dy in range(-3, 4):
        for dx in range(-3, 4):
            bx, by = px + dx, py + dy
            if world.get_block(bx, by) in _GHV:
                return (bx, by, guild_at_hall(bx, by))
    return None


def _nearby_animal_trap(world, player):
    """Return (bx, by) of an animal trap block within 2 blocks of the player, or None."""
    from blocks import ANIMAL_TRAP_BLOCK as _ATB
    px = int(player.x // BLOCK_SIZE)
    py = int(player.y // BLOCK_SIZE)
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            bx, by = px + dx, py + dy
            if world.get_block(bx, by) == _ATB:
                return (bx, by)
    return None


def _nearby_fish_trap(world, player):
    """Return (bx, by) of any fish trap block within 2 blocks of the player, or None."""
    from blocks import FISH_TRAP_BLOCKS as _FTBS
    px = int(player.x // BLOCK_SIZE)
    py = int(player.y // BLOCK_SIZE)
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            bx, by = px + dx, py + dy
            if world.get_block(bx, by) in _FTBS:
                return (bx, by)
    return None


def _insect_morph_at(ins, world_seed):
    """Return morph name if this insect's position seeds a color morph, else None."""
    if not ins.HAS_MORPH:
        return None
    import random as _rnd
    rng = _rnd.Random(world_seed ^ int(ins._spawn_x * 7919) ^ int(ins._spawn_y * 3571))
    if rng.random() < 0.15:
        return rng.choice(ins.MORPH_VARIANTS)
    return None


# Items dropped into inventory when the player successfully observes a species.
INSECT_DROP_TABLE = {
    "silk_moth":          "silk_thread",
    "honeybee":           "beeswax",
    "carpenter_bee":      "beeswax",
    "tundra_bumblebee":   "beeswax",
    "arctic_bumblebee":   "beeswax",
    "common_firefly":     "bioluminescent_gel",
    "blue_firefly":       "bioluminescent_gel",
    "golden_firefly":     "bioluminescent_gel",
    "asian_firefly":      "bioluminescent_gel",
    "tropical_firefly":   "bioluminescent_gel",
    "marsh_firefly":      "bioluminescent_gel",
    "wetland_glowfly":    "bioluminescent_gel",
    "swamp_lantern":      "bioluminescent_gel",
    "giant_hornet":       "venom_sac",
    "asian_giant_hornet": "venom_sac",
    "european_hornet":    "venom_sac",
    "atlas_moth":         "moth_dust",
    "comet_moth":         "moth_dust",
    "bogong_moth":        "moth_dust",
    "cochineal_scale":    "raw_cochineal",
    "kermes_scale":       "raw_kermes",
    "murex_snail":        "raw_murex",
}


def _update_reptiles(reptiles, player, dt, block_size):
    """Update all reptiles; return (species_id, biome) if one is discovered, else None."""
    from reptiles import OBS_DURATION, OBS_SPEED_THRESH
    discovered = None
    for rep in reptiles:
        rep.update(dt)
        if rep.state in ("fleeing", "hidden"):
            rep._obs_timer = 0.0
            continue
        dx_b = abs(player.x - rep.x) / block_size
        dy_b = abs(player.y - rep.y) / block_size
        if dx_b < rep.OBS_RADIUS and dy_b < rep.OBS_RADIUS * 0.6:
            if abs(player.vx) < OBS_SPEED_THRESH:
                rep._obs_timer += dt
                if rep._obs_timer >= OBS_DURATION and discovered is None:
                    biome = ""
                    if hasattr(rep, 'world') and rep.world is not None:
                        biome = rep.world.biodome_at(int(rep.x // block_size))
                    rep._obs_timer = 0.0
                    rep.flee()
                    discovered = (rep.SPECIES, biome)
            else:
                rep._obs_timer = 0.0
        else:
            rep._obs_timer = 0.0
    return discovered


def _load_settings():
    try:
        if SETTINGS_PATH.exists():
            return json.loads(SETTINGS_PATH.read_text())
    except Exception:
        pass
    return {"fullscreen": True, "debug": False}


def _save_settings(settings):
    try:
        SETTINGS_PATH.write_text(json.dumps(settings, indent=2))
    except Exception:
        pass


def _apply_display_mode(settings):
    if settings.get("fullscreen", True):
        flags = pygame.FULLSCREEN | pygame.SCALED
    else:
        flags = 0
    return pygame.display.set_mode((SCREEN_W, SCREEN_H), flags)


def _show_splash(screen):
    W, H = screen.get_size()
    clock = pygame.time.Clock()

    BLACK        = (0,   0,   0)
    BLUE_DARK    = (10,  50, 180)
    BLUE_MID     = (25,  90, 220)
    BLUE_LIGHT   = (55, 130, 255)
    BLUE_SHINE   = (90, 160, 255)
    WHITE        = (255, 255, 255)

    try:
        font_title = pygame.font.SysFont("Arial Black", 128, bold=True)
    except Exception:
        font_title = pygame.font.SysFont(None, 140, bold=True)

    # Pre-render title text
    title_txt = font_title.render("Collector", True, WHITE)

    oval_w, oval_h = 560, 230
    ox = W // 2 - oval_w // 2
    oy = H // 2 - oval_h // 2

    # Build the static splash surface (drawn at full opacity, faded via alpha overlay)
    splash = pygame.Surface((W, H))
    splash.fill(BLACK)

    # Gradient oval: 6 concentric ellipses, darkest edge → brightest center
    gradient_steps = [
        (0,   0,   oval_w,     oval_h,     BLUE_DARK),
        (10,  6,   oval_w-20,  oval_h-12,  BLUE_MID),
        (22,  12,  oval_w-44,  oval_h-24,  BLUE_MID),
        (50,  26,  oval_w-100, oval_h-52,  BLUE_LIGHT),
        (80,  40,  oval_w-160, oval_h-80,  BLUE_LIGHT),
        (110, 54,  oval_w-220, oval_h-108, BLUE_SHINE),
    ]
    for dx, dy, ew, eh, col in gradient_steps:
        if ew > 0 and eh > 0:
            pygame.draw.ellipse(splash, col, (ox + dx, oy + dy, ew, eh))

    # Oval border — thin dark ring
    pygame.draw.ellipse(splash, (0, 30, 120), (ox, oy, oval_w, oval_h), 4)

    # "Collector" text centered on the oval
    title_rect = title_txt.get_rect(center=(W // 2, H // 2))
    splash.blit(title_txt, title_rect)

    # Scanline overlay (every other row half-transparent black)
    scan = pygame.Surface((W, H), pygame.SRCALPHA)
    for row in range(0, H, 2):
        pygame.draw.line(scan, (0, 0, 0, 55), (0, row), (W, row))

    # Timing
    FADE_IN  = 0.35   # seconds
    HOLD     = 1.8
    FADE_OUT = 0.45
    total    = FADE_IN + HOLD + FADE_OUT
    elapsed  = 0.0

    fade_surf = pygame.Surface((W, H))
    fade_surf.fill(BLACK)

    while elapsed < total:
        dt = clock.tick(60) / 1000.0
        elapsed += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return  # skip

        # Alpha: 0 → 255 → 255 → 0
        if elapsed < FADE_IN:
            alpha = int(255 * (elapsed / FADE_IN))
        elif elapsed < FADE_IN + HOLD:
            alpha = 255
        else:
            alpha = int(255 * (1.0 - (elapsed - FADE_IN - HOLD) / FADE_OUT))
        alpha = max(0, min(255, alpha))

        screen.fill(BLACK)
        screen.blit(splash, (0, 0))
        screen.blit(scan, (0, 0))

        # Fade overlay: invert alpha (255 = black covering everything, 0 = fully visible)
        fade_surf.set_alpha(255 - alpha)
        screen.blit(fade_surf, (0, 0))

        pygame.display.flip()


def _show_settings_screen(screen, settings):
    """Settings screen with fullscreen toggle. Returns (screen, settings)."""
    clock = pygame.time.Clock()

    BLACK      = (0,   0,   0)
    BLUE_DARK  = (10,  50, 180)
    BLUE_LIGHT = (55, 130, 255)
    WHITE      = (255, 255, 255)
    BTN_HOVER  = (40, 100, 240)
    BTN_NORMAL = (20,  60, 160)
    GREEN_ON   = (20, 140,  50)
    GREEN_HOV  = (30, 180,  70)

    try:
        font_title = pygame.font.SysFont("Arial Black", 72, bold=True)
        font_btn   = pygame.font.SysFont("Arial Black", 36, bold=True)
    except Exception:
        font_title = pygame.font.SysFont(None, 80, bold=True)
        font_btn   = pygame.font.SysFont(None, 42, bold=True)

    btn_w, btn_h = 320, 62

    def _make_rects(w, h):
        bx = w // 2 - btn_w // 2
        gap = btn_h + 20
        base = h // 2 - (gap * 3) // 2
        return (
            pygame.Rect(bx, base,           btn_w, btn_h),
            pygame.Rect(bx, base + gap,     btn_w, btn_h),
            pygame.Rect(bx, base + gap * 2, btn_w, btn_h),
            pygame.Rect(bx, base + gap * 3, btn_w, btn_h),
        )

    def draw_button(surf, rect, label, hovered, active=False):
        if active:
            col = GREEN_HOV if hovered else GREEN_ON
        elif hovered:
            col = BTN_HOVER
        else:
            col = BTN_NORMAL
        pygame.draw.rect(surf, col, rect, border_radius=10)
        pygame.draw.rect(surf, BLUE_LIGHT, rect, 2, border_radius=10)
        lbl = font_btn.render(label, True, WHITE)
        surf.blit(lbl, lbl.get_rect(center=rect.center))

    W, H = screen.get_size()
    rect_fs, rect_ores, rect_debug, rect_back = _make_rects(W, H)

    while True:
        mx, my = pygame.mouse.get_pos()
        hover_fs    = rect_fs.collidepoint(mx, my)
        hover_ores  = rect_ores.collidepoint(mx, my)
        hover_debug = rect_debug.collidepoint(mx, my)
        hover_back  = rect_back.collidepoint(mx, my)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return screen, settings
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if rect_fs.collidepoint(mx, my):
                    settings["fullscreen"] = not settings.get("fullscreen", True)
                    _save_settings(settings)
                    screen = _apply_display_mode(settings)
                    W, H = screen.get_size()
                    rect_fs, rect_ores, rect_debug, rect_back = _make_rects(W, H)
                if rect_ores.collidepoint(mx, my):
                    settings["show_all_resources"] = not settings.get("show_all_resources", True)
                    _save_settings(settings)
                if rect_debug.collidepoint(mx, my):
                    settings["debug"] = not settings.get("debug", False)
                    _save_settings(settings)
                if rect_back.collidepoint(mx, my):
                    return screen, settings

        screen.fill(BLACK)
        title = font_title.render("Settings", True, WHITE)
        screen.blit(title, title.get_rect(center=(W // 2, H // 4)))
        fs_on    = settings.get("fullscreen", True)
        ores_on  = settings.get("show_all_resources", True)
        debug_on = settings.get("debug", False)
        draw_button(screen, rect_fs,    "Fullscreen: ON"   if fs_on    else "Fullscreen: OFF",   hover_fs,    active=fs_on)
        draw_button(screen, rect_ores,  "Show Ores: ON"    if ores_on  else "Show Ores: OFF",    hover_ores,  active=ores_on)
        draw_button(screen, rect_debug, "Debug Mode: ON"   if debug_on else "Debug Mode: OFF",   hover_debug, active=debug_on)
        draw_button(screen, rect_back,  "Back", hover_back)
        pygame.display.flip()
        clock.tick(60)


def _show_main_menu(screen, has_save, settings):
    """Returns ('new'|'load', screen, settings). Blocks until the player clicks a button."""
    from UI.menu_scene import MenuScene

    W, H = screen.get_size()
    clock = pygame.time.Clock()

    CREAM = (248, 243, 228)
    SAGE  = (172, 210, 158)
    GRAY  = (155, 148, 130)

    # --- Fonts (prefer elegant serifs) ---
    def _sfont(names, size, italic=False):
        for name in names:
            try:
                f = pygame.font.SysFont(name, size, bold=False, italic=italic)
                if f:
                    return f
            except Exception:
                pass
        return pygame.font.SysFont(None, size)

    font_title    = _sfont(["Georgia", "Palatino Linotype", "Book Antiqua", "Times New Roman"], 94)
    font_subtitle = _sfont(["Georgia", "Palatino Linotype", "Book Antiqua", "Times New Roman"], 24, italic=True)
    font_btn      = _sfont(["Georgia", "Palatino Linotype", "Arial", "Times New Roman"], 30)

    # Pre-render title with soft drop-shadow
    title_surf   = font_title.render("Collector", True, CREAM)
    title_shadow = font_title.render("Collector", True, (0, 0, 0))

    # Subtitle — letter-spaced "DISCOVER NATURE"
    _SUB = "DISCOVER  NATURE"
    _CHAR_GAP = 5
    char_surfs = [font_subtitle.render(ch, True, SAGE) for ch in _SUB]
    sub_total_w = sum(s.get_width() for s in char_surfs) + _CHAR_GAP * (len(_SUB) - 1)

    # --- Button layout ---
    btn_w, btn_h = 256, 52
    btn_gap = btn_h + 16
    btn_x   = W // 2 - btn_w // 2
    btn_base_y = int(H * 0.54)

    rect_new      = pygame.Rect(btn_x, btn_base_y,               btn_w, btn_h)
    rect_load     = pygame.Rect(btn_x, btn_base_y + btn_gap,     btn_w, btn_h)
    rect_settings = pygame.Rect(btn_x, btn_base_y + btn_gap * 2, btn_w, btn_h)
    rect_quit     = pygame.Rect(btn_x, btn_base_y + btn_gap * 3, btn_w, btn_h)

    _BTN_BG  = (12, 20, 12, 172)
    _BTN_HOV = (28, 45, 24, 210)
    _BTN_DIM = (18, 18, 14, 100)

    def draw_button(surf, rect, label, hovered, enabled):
        bg = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        if not enabled:
            bg.fill(_BTN_DIM)
            border_col = (255, 255, 255, 14)
            text_col   = GRAY
        elif hovered:
            bg.fill(_BTN_HOV)
            border_col = (255, 255, 255, 55)
            text_col   = CREAM
        else:
            bg.fill(_BTN_BG)
            border_col = (255, 255, 255, 22)
            text_col   = CREAM
        pygame.draw.rect(bg, border_col, bg.get_rect(), 1, border_radius=8)
        surf.blit(bg, rect.topleft)
        lbl = font_btn.render(label, True, text_col)
        surf.blit(lbl, lbl.get_rect(center=rect.center))

    scene = MenuScene(W, H)

    # Fade-in from black
    fade_alpha = 255
    fade_surf = pygame.Surface((W, H))
    fade_surf.fill((0, 0, 0))

    while True:
        dt = min(clock.tick(60) / 1000.0, 0.05)

        mx, my = pygame.mouse.get_pos()
        hover_new      = rect_new.collidepoint(mx, my)
        hover_load     = rect_load.collidepoint(mx, my) and has_save
        hover_settings = rect_settings.collidepoint(mx, my)
        hover_quit     = rect_quit.collidepoint(mx, my)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if rect_new.collidepoint(mx, my):
                    return "new", screen, settings
                if has_save and rect_load.collidepoint(mx, my):
                    return "load", screen, settings
                if rect_settings.collidepoint(mx, my):
                    screen, settings = _show_settings_screen(screen, settings)
                    W, H = screen.get_size()
                if rect_quit.collidepoint(mx, my):
                    pygame.quit()
                    sys.exit()

        scene.update(dt)
        scene.draw(screen)

        # Title
        title_y = int(H * 0.215)
        screen.blit(title_shadow, title_shadow.get_rect(center=(W // 2 + 2, title_y + 3)))
        screen.blit(title_surf,   title_surf.get_rect(center=(W // 2,       title_y)))

        # Subtitle — letter by letter for spacing
        sub_y = title_y + title_surf.get_height() + 2
        cx = W // 2 - sub_total_w // 2
        for cs in char_surfs:
            screen.blit(cs, (cx, sub_y))
            cx += cs.get_width() + _CHAR_GAP

        # Buttons
        draw_button(screen, rect_new,      "New Game",  hover_new,      True)
        draw_button(screen, rect_load,     "Load Game", hover_load,     has_save)
        draw_button(screen, rect_settings, "Settings",  hover_settings, True)
        draw_button(screen, rect_quit,     "Quit",      hover_quit,     True)

        # Fade-in overlay
        if fade_alpha > 0:
            fade_alpha = max(0, fade_alpha - int(255 * dt * 2.2))
            fade_surf.set_alpha(fade_alpha)
            screen.blit(fade_surf, (0, 0))

        pygame.display.flip()


def _run_with_loading_screen(screen, label, task_fn):
    """Show a loading frame, then run task_fn on the main thread."""
    W, H = screen.get_size()

    try:
        font = pygame.font.SysFont("Arial Black", 42, bold=True)
    except Exception:
        font = pygame.font.SysFont(None, 48, bold=True)

    screen.fill((0, 0, 0))
    lbl = font.render(label + "...", True, (255, 255, 255))
    screen.blit(lbl, lbl.get_rect(center=(W // 2, H // 2)))
    pygame.display.flip()
    pygame.event.pump()

    return task_fn()


def _t(label, t0):
    print(f"  {label}: {(time.perf_counter() - t0)*1000:.0f}ms")
    return time.perf_counter()


def main():
    t0 = time.perf_counter()
    print("[startup]")

    pygame.init()
    t0 = _t("pygame.init", t0)

    settings = _load_settings()
    screen = _apply_display_mode(settings)
    pygame.display.set_caption("CollectorBlocks")
    clock = pygame.time.Clock()
    t0 = _t("display init", t0)

    save_mgr = SaveManager()
    t0 = _t("SaveManager", t0)

    choice, screen, settings = _show_main_menu(screen, save_mgr.has_save(), settings)
    t0 = _t("menu choice: " + choice, t0)

    renderer = Renderer(screen)
    renderer.show_all_resources = settings.get("show_all_resources", True)
    t0 = _t("Renderer", t0)

    ui = UI(screen)
    ui._block_surfs = renderer._block_surfs
    t0 = _t("UI", t0)

    # Load global achievement state (persists across all games)
    ui.achievements_data, ui.global_collection = save_mgr.load_achievements()
    t0 = _t("load_achievements", t0)

    research = ResearchTree()
    t0 = _t("ResearchTree", t0)

    overrides = {}
    if choice == "load":
        def _do_load():
            global t0
            t0 = time.perf_counter()
            data = save_mgr.load()
            t0 = _t("  save_mgr.load", t0)
            w = World(seed=data["seed"], preloaded=data,
                      save_mgr=save_mgr, player_x=data["player"]["x"])
            import npc_identity as _npc_id
            _npc_id.assign_ruling_dynasties(w, data["seed"])
            t0 = _t("  World(preloaded)", t0)
            p = Player(w)
            t0 = _t("  Player", t0)
            p.apply_save(data["player"])
            t0 = _t("  player.apply_save", t0)
            # Resolve sculpture uid pointers now that Sculpture objects are loaded
            if hasattr(w, "_pending_sculpture_positions"):
                uid_map = {sc.uid: sc for sc in p.sculptures_created}
                for pos, val in w._pending_sculpture_positions.items():
                    if isinstance(val, dict) and "root" in val:
                        w.sculpture_data[pos] = {"root": val["root"]}
                    elif val in uid_map:
                        w.sculpture_data[pos] = uid_map[val]
                del w._pending_sculpture_positions
            # Resolve tapestry uid pointers
            if hasattr(w, "_pending_tapestry_positions"):
                tp_uid_map = {tp.uid: tp for tp in p.tapestries_created}
                for pos, val in w._pending_tapestry_positions.items():
                    if isinstance(val, dict) and "root" in val:
                        w.tapestry_data[pos] = {"root": val["root"]}
                    elif val in tp_uid_map:
                        w.tapestry_data[pos] = tp_uid_map[val]
                del w._pending_tapestry_positions
            import logic as _logic
            _logic.evaluate_full_network(w)
            return w, p, data["research"]
        world, player, research_data = _run_with_loading_screen(screen, "Loading", _do_load)
        research.apply_save(research_data)
        research.apply_bonuses(player, world)
        t0 = _t("research.apply_save", t0)
    else:
        seed = random.SystemRandom().randint(0, 2**31 - 1)
        # Animated worldgen: shows phases 1-4 (geography → kingdoms → 500-year
        # history → finalize) and returns the baked WorldPlan for the new World.
        from UI.world_setup import show_world_setup
        from UI.worldgen_screen import show_worldgen
        save_mgr.new_game()
        overrides, seed = show_world_setup(screen, seed)
        plan = show_worldgen(screen, seed, config_overrides=overrides)
        def _do_gen():
            global t0
            t0 = time.perf_counter()
            w = World(seed=seed, save_mgr=save_mgr, world_plan=plan)
            t0 = _t("  World(new)", t0)
            p = Player(w)
            t0 = _t("  Player", t0)
            return w, p
        world, player = _run_with_loading_screen(screen, "Building World", _do_gen)
        if settings.get("debug", False):
            for node in research.nodes.values():
                node.apply(player, world)
            research.apply_bonuses(player, world)

    if settings.get("debug", False) or (choice == "new" and overrides.get("exploration_mode", False)):
        player.no_hunger = True

    t0 = _t("total after choice", t0)

    world._player_ref = player
    world.debug = settings.get("debug", False)
    ui.world_ref = world

    renderer.cam_x = player.x - SCREEN_W // 2
    renderer.cam_y = player.y - SCREEN_H // 2

    def _close_all_ui():
        ui.pause_open = False
        ui.help_open = False
        ui.research_open = ui.inventory_open = ui.crafting_open = False
        ui._inv_search = ""
        ui._inv_search_active = False
        ui._craft_search = ""
        ui._craft_search_active = False
        ui._craft_show_craftable = False
        ui._bakery_show_craftable = False
        ui._artisan_show_craftable = False
        ui._cook_station_craftable.clear()
        ui.collection_open = ui.refinery_open = ui.npc_open = False
        ui.breeding_open = False
        ui.reputation_screen_open = False
        ui.automation_open = False
        ui.active_automation = None
        ui.farm_bot_open = False
        ui.active_farm_bot = None
        ui.backhoe_open = False
        ui.active_backhoe = None
        if hasattr(ui, 'equipment_crafting_open'):
            ui.equipment_crafting_open = False
        ui.active_npc = None
        ui._drag_item_id = None
        ui.chest_open = False
        ui.active_chest_inv = None
        ui.active_chest_pos = None
        ui.garden_open = False
        ui.active_garden_flowers = None
        ui.active_garden_pos = None
        ui._garden_drag_flower = None
        ui._garden_drag_source = None
        ui.wildflower_display_open = False
        ui.active_display_pos = None
        ui.wardrobe_open = False
        ui._jw_phase = "idle"
        ui._jw_drag_uid = None
        ui._sculpt_phase = "idle"
        ui.town_menu_open = False
        ui.active_town = None
        ui.outpost_menu_open = False
        ui.active_outpost = None
        ui.landmark_menu_open = False
        ui.active_landmark_region = None
        ui.active_landmark_spec = None
        ui.city_block_menu_open = False
        ui.active_city_block = None
        ui.coa_designer_open = False
        ui._coa_city = None
        ui.hire_panel_open = False
        ui.active_hire_npc = None
        ui.job_panel_open  = False
        ui.active_job_record = None
        ui.trade_block_open = False
        ui.active_trade_pos = None
        player.inspecting_npc = None
        player.gift_panel_open = False
        player.fulfill_request_open = False
        player.dynasty_panel_open = False
        player.dynasty_tree_open = False
        ui.gambling_open = False
        ui.racing_open = False
        ui.arena_open = False
        ui.bazaar_open = False
        ui.training_paddock_open = False
        ui.tea_house_open = False
        ui.ruin_plaque_open = False
        ui.ruin_plaque_info = None
        ui.hopper_open = False
        ui.pipe_output_open = False
        ui.pipe_filter_open = False
        ui.pipe_sorter_open = False
        ui.factory_open = False

    def _any_ui_open():
        return any([ui.pause_open, ui.help_open, ui.research_open, ui.inventory_open, ui.crafting_open,
                    ui.collection_open, ui.refinery_open, ui.npc_open,
                    ui.automation_open, ui.farm_bot_open, ui.chest_open,
                    ui.backhoe_open, ui.breeding_open, ui.garden_open, ui.wildflower_display_open,
                    ui.horse_breeding_open, ui._hb_active, ui.wardrobe_open,
                    ui.town_menu_open, ui.outpost_menu_open, ui.landmark_menu_open, ui.city_block_menu_open, ui.coa_designer_open, ui.hire_panel_open, ui.job_panel_open, ui.reputation_screen_open, ui.trade_block_open,
                    ui.dog_view_open, ui.dog_breeding_open, ui.gambling_open, ui.racing_open, ui.arena_open, ui.bazaar_open, ui.tea_house_open, getattr(ui, "training_paddock_open", False),
                    getattr(ui, "ruin_plaque_open", False),
                    getattr(ui, "hopper_open", False), getattr(ui, "pipe_output_open", False),
                    getattr(ui, "pipe_filter_open", False), getattr(ui, "pipe_sorter_open", False),
                    getattr(ui, "factory_open", False),
                    getattr(player, "inspecting_npc", None) is not None])

    def _find_nearby_npc(world, player):
        from cities import NPC
        for entity in world.entities:
            if isinstance(entity, NPC) and entity.in_range(player):
                if getattr(entity, 'is_ambient', False):
                    continue
                return entity
        return None

    def _find_any_nearby_npc(world, player):
        """Like _find_nearby_npc but also returns ambient NPCs (for inspect)."""
        from cities import NPC
        for entity in world.entities:
            if isinstance(entity, NPC) and entity.in_range(player):
                return entity
        return None

    def _execute_cheat(cmd, player, world):
        parts = cmd.strip().split()
        if not parts:
            return ""
        verb = parts[0].lower()
        if verb == "heal":
            player.health = 100
            player.hunger = 100.0
            return "Healed!"
        if verb == "god":
            player.god_mode = not player.god_mode
            return f"God mode: {'ON' if player.god_mode else 'OFF'}"
        if verb == "give":
            if len(parts) < 2:
                return "!Usage: give <item_id> [count]"
            from items import ITEMS
            item_id = parts[1]
            if item_id not in ITEMS:
                return f"!Unknown item: {item_id}"
            count = int(parts[2]) if len(parts) >= 3 else 1
            player._add_item(item_id, count)
            return f"Gave {count}x {item_id}"
        if verb == "money":
            if len(parts) < 2:
                return "!Usage: money <amount>"
            player.money += int(parts[1])
            return f"Money: {player.money}"
        if verb == "tp":
            if len(parts) < 3:
                return "!Usage: tp <block_x> <block_y>"
            from constants import BLOCK_SIZE, PLAYER_W, PLAYER_H
            bx, by = int(parts[1]), int(parts[2])
            player.x = float(bx * BLOCK_SIZE)
            player.y = float(by * BLOCK_SIZE)
            player.vx = player.vy = 0.0
            return f"Teleported to {bx},{by}"
        if verb == "kill":
            player.health = 0
            return "RIP"
        return f"!Unknown command: {verb}"

    def _save_and_notify(w, p, res):
        if p.mounted_machine is not None:
            bh = p.mounted_machine
            bh.take_all(p)
            p.mounted_machine = None
        newly = save_mgr.save(w, p, res)
        ui.achievements_data, ui.global_collection = save_mgr.load_achievements()
        for ach in newly:
            p.pending_notifications.append(("Achievement", ach.name, None))

    _fps_font = pygame.font.SysFont("consolas", 16)
    _fps_smooth = 60.0
    _fps_last = -1
    fps_surf = _fps_font.render("FPS: 60", True, (255, 255, 255))
    _biome_surf = None
    _biome_last = ""

    autosave_timer = 0.0
    AUTOSAVE_INTERVAL = 60.0

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                # Cheat console input intercepts all keys while open
                if ui.cheat_open:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKQUOTE:
                        ui.cheat_open = False
                        ui.cheat_text = ""
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        result = _execute_cheat(ui.cheat_text, player, world)
                        ui.cheat_message = result
                        ui.cheat_text = ""
                        ui._cheat_msg_timer = 3.0
                    elif event.key == pygame.K_BACKSPACE:
                        ui.cheat_text = ui.cheat_text[:-1]
                    else:
                        ch = event.unicode
                        if ch and ch.isprintable():
                            ui.cheat_text += ch
                    continue  # don't process other keys while console open

                # Inventory search bar intercepts all keys while active
                if ui.inventory_open and ui._inv_search_active:
                    ui.handle_inventory_search_key(event)
                    continue

                # Crafting screen search bar intercepts all keys while active
                if ui.crafting_open and ui._craft_search_active:
                    ui.handle_craft_search_key(event)
                    continue

                # Artisan bench search bar intercepts all keys while active
                if ui.refinery_open and ui._artisan_search_active:
                    ui.handle_artisan_search_key(event)
                    continue

                # Death screen: only SPACE/ENTER to respawn
                if player.dead:
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER):
                        player.respawn()
                        _close_all_ui()
                    continue

                # Elevator floor navigation while riding
                if player.riding_elevator is not None and not _any_ui_open():
                    car = player.riding_elevator
                    if event.key in (pygame.K_w, pygame.K_UP):
                        stops = car.get_stops(world)
                        if stops:
                            car_by = int(round(car.car_y / BLOCK_SIZE))
                            idx = min(range(len(stops)), key=lambda i: abs(stops[i] - car_by))
                            if idx > 0:
                                car.call(stops[idx - 1], world)
                        continue
                    elif event.key in (pygame.K_s, pygame.K_DOWN):
                        stops = car.get_stops(world)
                        if stops:
                            car_by = int(round(car.car_y / BLOCK_SIZE))
                            idx = min(range(len(stops)), key=lambda i: abs(stops[i] - car_by))
                            if idx < len(stops) - 1:
                                car.call(stops[idx + 1], world)
                        continue

                # Boat steering controls while riding
                if player.riding_boat is not None and not _any_ui_open():
                    boat = player.riding_boat
                    if event.key in (pygame.K_a, pygame.K_LEFT):
                        boat.go(-1, world)
                        continue
                    elif event.key in (pygame.K_d, pygame.K_RIGHT):
                        boat.go(1, world)
                        continue
                    elif event.key in (pygame.K_s, pygame.K_DOWN):
                        boat.stop()
                        continue

                # Minecart direction controls while riding
                if player.riding_minecart is not None and not _any_ui_open():
                    cart = player.riding_minecart
                    if event.key in (pygame.K_a, pygame.K_LEFT):
                        cart.go(-1)
                        continue
                    elif event.key in (pygame.K_d, pygame.K_RIGHT):
                        cart.go(1)
                        continue
                    elif event.key in (pygame.K_s, pygame.K_DOWN):
                        cart.stop()
                        continue

                # Roaster: ENTER to stop roasting
                if ui.refinery_open and ui.refinery_block_id == ROASTER_BLOCK:
                    ui.handle_roaster_keydown(event.key, player)

                # Grape Press: ENTER to finish pressing
                if ui.refinery_open and ui.refinery_block_id == GRAPE_PRESS_BLOCK:
                    ui.handle_press_keydown(event.key, player)

                # Beehive: ENTER / SPACE keydown
                if ui.refinery_open and ui.refinery_block_id == BEEHIVE_BLOCK:
                    ui.handle_beehive_keydown(event.key, player)
                # Mead Vat: SPACE keydown
                if ui.refinery_open and ui.refinery_block_id == MEAD_VAT_BLOCK:
                    ui.handle_mead_vat_keydown(event.key, player)

                # Fermentation Tank: P punchdown, ENTER to finish
                if ui.refinery_open and ui.refinery_block_id == FERMENTATION_BLOCK:
                    ui.handle_fermenter_keydown(event.key, player)

                # Copper Still: ENTER to make cuts
                if ui.refinery_open and ui.refinery_block_id == STILL_BLOCK:
                    ui.handle_still_keydown(event.key, player)

                # Oxidation Station: ENTER to lock oxidation level
                if ui.refinery_open and ui.refinery_block_id == OXIDATION_STATION_BLOCK:
                    ui.handle_oxidation_keydown(event.key, player)

                # Spinning Wheel: SPACE for tension, ESC to close
                if ui.refinery_open and ui.refinery_block_id == SPINNING_WHEEL_BLOCK:
                    ui.handle_spinning_wheel_keydown(event.key, player)

                # Loom: ESC to close
                if ui.refinery_open and ui.refinery_block_id == LOOM_BLOCK:
                    ui.handle_loom_keydown(event.key, player)

                # Dairy Vat: SPACE to add culture
                if ui.refinery_open and ui.refinery_block_id == DAIRY_VAT_BLOCK:
                    ui.handle_dairy_vat_keydown(event.key, player)

                # Aging Cave: C to care for wheel
                if ui.refinery_open and ui.refinery_block_id == AGING_CAVE_BLOCK:
                    ui.handle_aging_cave_keydown(event.key, player)

                # Wine Cellar aging: W to swirl
                if ui.refinery_open and ui.refinery_block_id == WINE_CELLAR_BLOCK:
                    ui.handle_wine_age_keydown(event.key)

                # Barrel Room aging: W to sample
                if ui.refinery_open and ui.refinery_block_id == BARREL_ROOM_BLOCK:
                    ui.handle_barrel_age_keydown(event.key)

                # Brew Kettle: ENTER to set mash / add hops / finish
                if ui.refinery_open and ui.refinery_block_id == BREW_KETTLE_BLOCK:
                    ui.handle_brew_keydown(event.key, player)

                # Fermentation Vessel: W to rack; SPACE held to cool
                if ui.refinery_open and ui.refinery_block_id == FERM_VESSEL_BLOCK:
                    ui.handle_ferm_keydown(event.key, player)

                # Taproom: W to dry-hop during conditioning
                if ui.refinery_open and ui.refinery_block_id == TAPROOM_BLOCK:
                    ui.handle_tap_keydown(event.key, player)

                # Jewelry Workbench: text input for name phase
                if ui.refinery_open and ui._jw_phase == "name_confirm":
                    ui.handle_jewelry_keydown(event.key, getattr(event, "unicode", ""), player)

                # City Block: text input for city name editing
                if ui.city_block_menu_open and ui._city_name_editing:
                    ui.handle_city_block_keydown(event.key, getattr(event, "unicode", ""), player)

                # Job panel: text input for hauling config
                if ui.job_panel_open:
                    ui.handle_job_panel_keydown(event.key, getattr(event, "unicode", ""))

                # Sculptor's Bench: Z=undo, ENTER=confirm, ESC=back
                from blocks import SCULPTORS_BENCH as _SCULPTORS_BENCH
                if ui.refinery_open and ui.refinery_block_id == _SCULPTORS_BENCH:
                    ui.handle_sculptor_keydown(event.key, player)
                # Tapestry Frame: Z=undo, ENTER=confirm, ESC=back
                from blocks import TAPESTRY_FRAME_BLOCK as _TAPESTRY_FRAME
                if ui.refinery_open and ui.refinery_block_id == _TAPESTRY_FRAME:
                    ui.handle_tapestry_keydown(event.key, player)

                # Pottery Wheel / Kiln: Z=undo, ENTER=confirm, SPACE=heat, ESC=back
                from blocks import POTTERY_WHEEL_BLOCK as _PWB, POTTERY_KILN_BLOCK as _PKB
                if ui.refinery_open and ui.refinery_block_id in (_PWB, _PKB):
                    ui.handle_pottery_keydown(event.key, player)

                from blocks import EVAPORATION_PAN_BLOCK as _EVAP_PAN
                if ui.refinery_open and ui.refinery_block_id == _EVAP_PAN:
                    ui.handle_evap_pan_keydown(event.key, player)

                # Forge: SPACE=bellows, ENTER=finish part, ESC=back/close
                from blocks import FORGE_BLOCK as _FORGE_BLOCK
                if ui.refinery_open and ui.refinery_block_id == _FORGE_BLOCK:
                    ui.handle_forge_keydown(event.key, player)

                # Pigment Mill: SPACE=grind hit, ENTER=confirm, ESC=back
                from blocks import PIGMENT_MILL_BLOCK as _PIGMENT_MILL
                if ui.refinery_open and ui.refinery_block_id == _PIGMENT_MILL:
                    ui.handle_pigment_keydown(event.key, player)

                # Gambling Table: ESC navigates phases or closes
                if ui.gambling_open:
                    ui.handle_gambling_keydown(event.key, player)

                # Horse Racing: ESC navigates phases or closes
                if ui.racing_open:
                    ui.handle_racing_keydown(event.key, player)
                if getattr(ui, "training_paddock_open", False) and event.key == pygame.K_ESCAPE:
                    ui.training_paddock_open = False

                # Arena: ESC skips to result or closes
                if ui.arena_open:
                    ui.handle_arena_keydown(event.key, player)

                # Jousting: arrow keys pick aim during CLOSE phase, ESC exits
                if getattr(ui, "jousting_open", False):
                    if event.key == pygame.K_ESCAPE:
                        ui.close_jousting()
                    else:
                        ui.handle_jousting_key(event, player)

                # Bazaar: ESC skips resolve or closes
                if ui.bazaar_open:
                    ui.handle_bazaar_keydown(event.key, player)

                # Stock Exchange: ESC closes, TAB switches tabs, text input for charter name
                if getattr(ui, "stock_exchange_open", False):
                    ui.handle_stock_exchange_keydown(event.key, player,
                                                    unicode=getattr(event, "unicode", ""))

                # Milking mini-game: SPACE pulls the currently lit teat
                if event.key == pygame.K_SPACE and not _any_ui_open():
                    from animals import Cow as _Cow
                    for _ent in world.entities:
                        if isinstance(_ent, _Cow) and _ent._milking is not None:
                            _ent.handle_milking_press()
                            break

                # Weapon Rack: ESC closes inspect/picker layers before closing rack
                from blocks import WEAPON_RACK_BLOCK as _WEAPON_RACK_BLOCK
                if ui.refinery_open and ui.refinery_block_id == _WEAPON_RACK_BLOCK:
                    if event.key == pygame.K_ESCAPE:
                        if getattr(ui, "_inspect_picking_slot", None):
                            ui._inspect_picking_slot = None
                        elif getattr(ui, "_inspect_weapon_uid", None):
                            ui._inspect_weapon_uid = None
                        else:
                            ui.refinery_open = False

                # Wardrobe toggle (T = Textiles/Tailoring)
                if event.key == pygame.K_t:
                    if ui.wardrobe_open:
                        ui.wardrobe_open = False
                    elif not _any_ui_open():
                        ui.wardrobe_open = True
                if event.key == pygame.K_ESCAPE and ui.wardrobe_open:
                    ui.wardrobe_open = False

                if event.key == pygame.K_h and ui.town_menu_open:
                    ui.town_chronicle_open = not ui.town_chronicle_open

                if event.key == pygame.K_ESCAPE:
                    if ui.coa_designer_open:
                        ui.close_coat_of_arms_designer()
                    elif getattr(ui, "ruin_plaque_open", False):
                        ui.ruin_plaque_open = False
                        ui.ruin_plaque_info = None
                    elif getattr(player, "dynasty_tree_open", False):
                        player.dynasty_tree_open = False
                    elif ui.town_chronicle_open:
                        ui.town_chronicle_open = False
                    elif ui.job_panel_open:
                        ui.close_job_panel()
                    elif player.fishing_state in ("casting", "biting", "reeling"):
                        player.fishing_state = None
                        player._fishing_biome = None
                        player._fishing_is_hotspot = False
                        player._fishing_pending_fish = None
                    elif ui.pause_open:
                        ui.pause_open = False
                    elif _any_ui_open():
                        _close_all_ui()
                    else:
                        ui.pause_open = True

                # Backhoe UI: SPACE mounts the machine
                if event.key == pygame.K_SPACE and ui.backhoe_open and ui.active_backhoe is not None:
                    bh = ui.active_backhoe
                    ui.close_backhoe()
                    player.mounted_machine = bh
                    player.x = bh.x + (bh.W - PLAYER_W) / 2
                    player.y = bh.y

                # Backhoe arm movement while mounted (arrow keys)
                if player.mounted_machine is not None and not _any_ui_open():
                    bh = player.mounted_machine
                    _arm_r_sq = Backhoe.ARM_REACH ** 2
                    _candidate = None
                    if event.key == pygame.K_LEFT:
                        _candidate = (bh.arm_dx - 1, bh.arm_dy)
                    elif event.key == pygame.K_RIGHT:
                        _candidate = (bh.arm_dx + 1, bh.arm_dy)
                    elif event.key == pygame.K_UP:
                        _candidate = (bh.arm_dx, bh.arm_dy - 1)
                    elif event.key == pygame.K_DOWN:
                        _candidate = (bh.arm_dx, bh.arm_dy + 1)
                    if _candidate is not None and _candidate[0] ** 2 + _candidate[1] ** 2 <= _arm_r_sq:
                        if _candidate != (0, 0):
                            bh.arm_dx, bh.arm_dy = _candidate

                if event.key == pygame.K_BACKQUOTE:
                    ui.cheat_open = True
                    ui.cheat_text = ""

                if event.key == pygame.K_s and (event.mod & pygame.KMOD_CTRL):
                    _save_and_notify(world, player, research)
                    print("Game saved.")

                if event.key == pygame.K_r:
                    ui.research_open = not ui.research_open
                    ui.inventory_open = ui.crafting_open = False
                    ui.equipment_crafting_open = ui.collection_open = ui.refinery_open = False
                    ui._inv_search = ""; ui._inv_search_active = False

                if event.key == pygame.K_i:
                    ui.inventory_open = not ui.inventory_open
                    ui.research_open = ui.crafting_open = False
                    ui.equipment_crafting_open = ui.collection_open = ui.refinery_open = False
                    if not ui.inventory_open:
                        ui._inv_search = ""
                        ui._inv_search_active = False

                if event.key == pygame.K_c:
                    ui.crafting_open = not ui.crafting_open
                    ui.research_open = ui.inventory_open = False
                    ui.equipment_crafting_open = ui.collection_open = ui.refinery_open = False
                    ui._inv_search = ""; ui._inv_search_active = False
                    if not ui.crafting_open:
                        ui._craft_search = ""; ui._craft_search_active = False
                        ui._craft_show_craftable = False

                if event.key == pygame.K_g:
                    ui.collection_open = not ui.collection_open
                    ui.research_open = ui.inventory_open = ui.crafting_open = False
                    ui.equipment_crafting_open = ui.refinery_open = ui.breeding_open = False
                    ui._inv_search = ""; ui._inv_search_active = False

                if event.key == pygame.K_b:
                    ui.breeding_open = not ui.breeding_open
                    ui.research_open = ui.inventory_open = ui.crafting_open = False
                    ui.equipment_crafting_open = ui.collection_open = ui.refinery_open = False
                    ui._inv_search = ""; ui._inv_search_active = False

                if event.key == pygame.K_k:
                    ui.reputation_screen_open = not ui.reputation_screen_open
                    if ui.reputation_screen_open:
                        ui.research_open = ui.inventory_open = ui.crafting_open = False
                        ui.collection_open = ui.refinery_open = ui.breeding_open = False
                        ui._inv_search = ""; ui._inv_search_active = False

                if event.key == pygame.K_h:
                    ui.help_open = not ui.help_open
                    if ui.help_open:
                        ui.research_open = ui.inventory_open = ui.crafting_open = False
                        ui.collection_open = ui.refinery_open = ui.breeding_open = False
                        ui._inv_search = ""; ui._inv_search_active = False

                if event.key == pygame.K_F9:
                    if research.nodes.get("stock_exchange_access") and research.nodes["stock_exchange_access"].unlocked:
                        if ui.stock_exchange_open:
                            ui.stock_exchange_open = False
                        else:
                            ui.open_stock_exchange(research)
                            ui.research_open = ui.inventory_open = ui.crafting_open = False
                            ui.collection_open = ui.refinery_open = ui.breeding_open = False

                if event.key == pygame.K_i:
                    nearby_any = _find_any_nearby_npc(world, player)
                    if nearby_any is not None:
                        from cities import LandmarkNPC as _LandmarkNPC_i
                        if isinstance(nearby_any, _LandmarkNPC_i):
                            pass  # landmark interaction is handled via E on the flag
                        elif getattr(player, "inspecting_npc", None) is nearby_any:
                            player.inspecting_npc = None
                            player.gift_panel_open = False
                            player.fulfill_request_open = False
                        else:
                            _close_all_ui()
                            player.inspecting_npc = nearby_any
                            player.gift_panel_open = False
                            player.fulfill_request_open = False
                            ui._inspect_panel_scroll = 0
                            # Rival dynasty first-meeting penalty
                            _uid = getattr(nearby_any, "npc_uid", None)
                            if _uid and _uid not in player.npc_relationships:
                                _rid = getattr(nearby_any, "dynasty_id", None)
                                if _rid in getattr(player, "rival_dynasty_regions", set()):
                                    player.npc_relationships[_uid] = -20
                                else:
                                    player.npc_relationships[_uid] = 0
                            import npc_preferences as _npc_prefs
                            _npc_prefs.maybe_generate_request(
                                player, nearby_any, getattr(world, "day_count", 0)
                            )

                if event.key == pygame.K_e:
                    # Dismount minecart if currently riding
                    if player.riding_minecart is not None:
                        cart = player.riding_minecart
                        cart.stop()
                        cart.rider = None
                        player.x = cart.cart_x + Minecart.W + 4
                        player.y = float(cart.track_by * BLOCK_SIZE)
                        player.riding_minecart = None
                        continue

                    # Dismount boat if currently riding
                    if player.riding_boat is not None:
                        boat = player.riding_boat
                        boat.stop()
                        boat.rider = None
                        player.x = boat.x + boat.W + 4
                        player.y = boat.y
                        player.riding_boat = None
                        continue

                    # Dismount elevator if currently riding
                    if player.riding_elevator is not None:
                        car = player.riding_elevator
                        car.rider = None
                        player.x = car.shaft_x * BLOCK_SIZE + ElevatorCar.W + 4
                        player.riding_elevator = None
                        continue

                    # Dismount horse if currently riding
                    if player.mounted_horse is not None:
                        horse = player.mounted_horse
                        horse.rider = None
                        player.x = horse.x + horse.W + 4
                        player.y = horse.y
                        player.mounted_horse = None
                        continue

                    # Guild Hall — open Stock Exchange focused on that hall's guild
                    hall = _nearby_guild_hall(world, player)
                    if hall is not None:
                        if ui.stock_exchange_open:
                            ui.stock_exchange_open = False
                        else:
                            ui.open_stock_exchange(research, focus_guild_id=hall[2])
                            ui.research_open = ui.inventory_open = ui.crafting_open = False
                            ui.collection_open = ui.refinery_open = ui.breeding_open = False
                        continue

                    # Dismount backhoe if currently riding
                    if player.mounted_machine is not None:
                        bh = player.mounted_machine
                        bh.take_all(player)
                        player.x = bh.x + bh.W + 4
                        player.y = bh.y
                        player.mounted_machine = None
                        # Then open the backhoe UI so player can manage fuel
                        _close_all_ui()
                        ui.open_backhoe(bh)
                        continue

                    nearby_boat = next(
                        (b for b in world.boats if b.in_range(player) and b.rider is None), None
                    )
                    nearby_auto = next(
                        (a for a in world.automations if a.in_range(player)), None
                    )
                    nearby_fb = next(
                        (fb for fb in world.farm_bots if fb.in_range(player)), None
                    )
                    nearby_bh = next(
                        (bh for bh in world.backhoes if bh.in_range(player)), None
                    )
                    nearby_flag = player.get_nearby_town_flag()
                    nearby_outpost_flag = player.get_nearby_outpost_flag()
                    nearby_landmark_flag = player.get_nearby_landmark_flag()
                    nearby_city_block = player.get_nearby_city_block()
                    nearby_npc = _find_nearby_npc(world, player)
                    nearby_bed = player.get_nearby_bed()
                    nearby_elev_stop = player.get_nearby_elevator_stop()
                    nearby_track_stop = player.get_nearby_mine_track_stop()
                    if nearby_auto is not None:
                        if ui.automation_open and ui.active_automation is nearby_auto:
                            ui.automation_open = False
                            ui.active_automation = None
                        else:
                            _close_all_ui()
                            ui.automation_open = True
                            ui.active_automation = nearby_auto
                    elif nearby_fb is not None:
                        if ui.farm_bot_open and ui.active_farm_bot is nearby_fb:
                            ui.farm_bot_open = False
                            ui.active_farm_bot = None
                        else:
                            _close_all_ui()
                            ui.farm_bot_open = True
                            ui.active_farm_bot = nearby_fb
                    elif nearby_bh is not None:
                        if ui.backhoe_open and ui.active_backhoe is nearby_bh:
                            ui.close_backhoe()
                        else:
                            _close_all_ui()
                            ui.open_backhoe(nearby_bh)
                    elif nearby_city_block is not None:
                        from player_cities import get_city_at
                        city = get_city_at(*nearby_city_block)
                        if city is not None:
                            if ui.city_block_menu_open and ui.active_city_block is city:
                                ui.close_city_block_menu()
                            else:
                                _close_all_ui()
                                ui.open_city_block_menu(city)
                    elif nearby_outpost_flag is not None:
                        from outposts import get_outpost_for_block
                        op = get_outpost_for_block(*nearby_outpost_flag)
                        if op is None:
                            print(f"[WARNING] Outpost flag at {nearby_outpost_flag}: "
                                  f"OUTPOSTS registry is empty — something broke during load.")
                        elif ui.outpost_menu_open and ui.active_outpost is op:
                            ui.close_outpost_menu()
                        else:
                            _close_all_ui()
                            ui.open_outpost_menu(op)
                    elif nearby_landmark_flag is not None:
                        from landmarks import apply_effect, landmark_for
                        from towns import REGIONS, TOWNS
                        lbx, lby = nearby_landmark_flag
                        _reg = None
                        if TOWNS:
                            _nearest_t = min(TOWNS.values(),
                                             key=lambda t: abs(t.center_bx - lbx))
                            if _nearest_t.region_id in REGIONS:
                                _reg = REGIONS[_nearest_t.region_id]
                        if _reg is None:
                            print(f"[WARNING] Landmark flag at ({lbx},{lby}) has no "
                                  f"matching region. Nearest town center: "
                                  f"{_nearest_t.center_bx if TOWNS else 'none'}. "
                                  f"E-key will not work.")
                        if _reg:
                            if ui.landmark_menu_open and ui.active_landmark_region is _reg:
                                # Second E: fire the effect
                                ok, title, detail = apply_effect(
                                    player, _reg, getattr(world, "day_count", 0),
                                    debug=settings.get("debug", False))
                                if not hasattr(world, "_town_toasts"):
                                    world._town_toasts = []
                                msg = title if not detail else f"{title} — {detail}"
                                world._town_toasts.append(msg)
                                ui.close_landmark_menu()
                                if getattr(world, "pending_arena_open", None) is not None:
                                    _close_all_ui()
                                    ui.open_arena(world.pending_arena_open)
                                    world.pending_arena_open = None
                                if getattr(world, "pending_bazaar_open", None) is not None:
                                    _close_all_ui()
                                    lots, fence_wants, rivals = world.pending_bazaar_open
                                    ui.open_bazaar(lots, fence_wants, rivals)
                                    world.pending_bazaar_open = None
                            else:
                                # First E: open the info screen
                                _close_all_ui()
                                _spec = landmark_for(
                                    _reg.agenda,
                                    getattr(_reg, "biome_group", ""))
                                ui.open_landmark_menu(_reg, _spec)
                    elif nearby_npc is not None:
                        from cities import LeaderNPC, LandmarkNPC
                        from settler_npcs import SettlerNPC as _SettlerNPC
                        if isinstance(nearby_npc, LandmarkNPC):
                            pass  # handled via nearby_landmark_flag above
                        elif isinstance(nearby_npc, _SettlerNPC):
                            # Any settler (hired or not) → hire/status panel
                            from player_cities import PLAYER_CITIES
                            _city = next((c for c in PLAYER_CITIES.values()
                                          if c.bx == nearby_npc.settler_city_bx), None)
                            _rec  = next((r for r in (_city.npcs if _city else [])
                                          if r["id"] == nearby_npc.settler_id), None)
                            if _city and _rec:
                                if ui.hire_panel_open and ui.active_hire_npc is nearby_npc:
                                    ui.close_hire_panel()
                                else:
                                    _close_all_ui()
                                    ui.open_hire_panel(nearby_npc, _city, _rec)
                        elif ui.npc_open and ui.active_npc is nearby_npc:
                            ui.npc_open = False
                            ui.active_npc = None
                        else:
                            _close_all_ui()
                            if not nearby_npc.is_open(world.time_of_day):
                                player.pending_notifications.append(
                                    ("Shop", "Closed — come back at dawn", None))
                            else:
                                ui.npc_open = True
                                ui.active_npc = nearby_npc
                            if isinstance(nearby_npc, LeaderNPC):
                                from towns import REGIONS
                                region = REGIONS.get(nearby_npc.region_id)
                                if region is not None:
                                    player.visited_town_ids.add(region.capital_town_id)
                    elif nearby_flag is not None:
                        from towns import get_town_for_block
                        town = get_town_for_block(world, *nearby_flag)
                        if town is not None:
                            if ui.town_menu_open and ui.active_town is town:
                                ui.close_town_menu()
                            else:
                                _close_all_ui()
                                ui.open_town_menu(town, player)
                    elif nearby_boat is not None:
                        nearby_boat.rider = player
                        player.riding_boat = nearby_boat
                    elif nearby_bed is not None:
                        player.set_spawn(*nearby_bed)
                        print("Spawn point set to bed.")
                    elif nearby_elev_stop is not None:
                        bx, by = nearby_elev_stop
                        car = next((c for c in world.elevator_cars if c.shaft_x == bx), None)
                        if car is not None:
                            car_by = int(round(car.car_y / BLOCK_SIZE))
                            if car.state == "idle" and car_by == by and car.rider is None:
                                car.rider = player
                                player.riding_elevator = car
                            elif (car.state != "moving" or car_by != by) and car.rider is None:
                                car.call(by, world)
                    elif nearby_track_stop is not None:
                        bx, by = nearby_track_stop
                        _track_carts = [c for c in world.minecarts if c.track_by == by]
                        cart = min(_track_carts, key=lambda c: abs(c.cart_x - bx * BLOCK_SIZE), default=None)
                        if cart is not None:
                            cart_bx = int(round(cart.cart_x / BLOCK_SIZE))
                            if cart.state == "idle" and cart_bx == bx and cart.rider is None:
                                cart.rider = player
                                player.riding_minecart = cart
                            else:
                                cart.call(bx)
                    else:
                        ui.npc_open = False
                        ui.active_npc = None
                        nearby_chest = player.get_nearby_chest()
                        nearby_garden = player.get_nearby_garden()
                        nearby_wf_display = player.get_nearby_wildflower_display()
                        nearby_pottery_display = player.get_nearby_pottery_display()
                        nearby_ruin_marker = player.get_nearby_ruin_marker()
                        if nearby_ruin_marker is not None:
                            from ruins import lookup_marker_info
                            info = lookup_marker_info(world, *nearby_ruin_marker)
                            if info is not None:
                                if ui.ruin_plaque_open:
                                    ui.ruin_plaque_open = False
                                    ui.ruin_plaque_info = None
                                else:
                                    _close_all_ui()
                                    ui.ruin_plaque_open = True
                                    ui.ruin_plaque_info = info
                        elif nearby_chest is not None:
                            if ui.chest_open and ui.active_chest_pos == nearby_chest:
                                ui.chest_open = False
                                ui.active_chest_inv = None
                                ui.active_chest_pos = None
                            else:
                                _close_all_ui()
                                bx, by = nearby_chest
                                ui.active_chest_inv = world.chest_data.setdefault((bx, by), {})
                                ui.active_chest_pos = nearby_chest
                                ui.chest_open = True
                        elif nearby_garden is not None:
                            if ui.garden_open and ui.active_garden_pos == nearby_garden:
                                ui.garden_open = False
                                ui.active_garden_flowers = None
                                ui.active_garden_pos = None
                            else:
                                _close_all_ui()
                                bx, by = nearby_garden
                                ui.active_garden_flowers = world.garden_data.setdefault((bx, by), [])
                                ui.active_garden_pos = nearby_garden
                                ui.garden_open = True
                        elif nearby_wf_display is not None:
                            if ui.wildflower_display_open and ui.active_display_pos == nearby_wf_display:
                                ui.wildflower_display_open = False
                                ui.active_display_pos = None
                            else:
                                _close_all_ui()
                                ui.active_display_pos = nearby_wf_display
                                ui.wildflower_display_open = True
                        elif nearby_pottery_display is not None:
                            bx, by = nearby_pottery_display
                            existing = world.pottery_display_data.get((bx, by))
                            if existing is not None:
                                # Remove piece from pedestal, return vase item
                                from pottery import get_output_item
                                world.pottery_display_data.pop((bx, by))
                                player._add_item(get_output_item(existing))
                                player.pending_notifications.append(("Pottery", f"{existing.shape.title()} removed from display", None))
                            elif player.unplaced_vases:
                                piece = player.unplaced_vases.pop()
                                world.pottery_display_data[(bx, by)] = piece
                                player.pending_notifications.append(("Pottery", f"{piece.firing_level.title()} {piece.clay_biome.title()} vase displayed", None))
                            else:
                                player.pending_notifications.append(("Pottery", "No vases available to display", None))
                        else:
                            _at_pos = _nearby_animal_trap(world, player)
                            if _at_pos is not None:
                                trap = world.animal_traps.get(_at_pos)
                                if trap and trap["accumulated"]:
                                    for _item_id, _count in trap["accumulated"]:
                                        player.inventory[_item_id] = player.inventory.get(_item_id, 0) + _count
                                        player.pending_notifications.append(
                                            ("Trap", _item_id.replace("_", " ").title(), None))
                                    trap["accumulated"].clear()
                                else:
                                    quality = world.trap_quality_label(_at_pos[0])
                                    player.pending_notifications.append(
                                        ("Animal Trap", f"Nothing caught yet  •  {quality}", None))
                            _ft_pos = _nearby_fish_trap(world, player) if _at_pos is None else None
                            if _ft_pos is not None:
                                _ft = world.fish_traps.get(_ft_pos)
                                if _ft is not None:
                                    _ft_names    = {"wicker": "Wicker Fish Trap", "iron": "Iron Fish Trap",
                                                    "reinforced": "Reinforced Fish Trap", "steel": "Steel Cage Trap"}
                                    _ft_label    = _ft_names.get(_ft["type"], "Fish Trap")
                                    _ft_caps_tbl = {"wicker": (10, 20), "iron": (20, 40),
                                                    "reinforced": (30, 60), "steel": (50, 80)}
                                    _ft_cap, _ft_bait_cap = _ft_caps_tbl.get(_ft["type"], (10, 20))
                                    _gave_fish   = False
                                    if _ft["accumulated"]:
                                        for _fid, _fc in _ft["accumulated"]:
                                            player.inventory[_fid] = player.inventory.get(_fid, 0) + _fc
                                            player.pending_notifications.append(
                                                (_ft_label, _fid.replace("_", " ").title(), None))
                                        _ft["accumulated"].clear()
                                        _gave_fish = True
                                    _worms = player.inventory.get("worm_bait", 0)
                                    if _worms > 0 and _ft["bait"] < _ft_bait_cap:
                                        _deposit = min(_worms, _ft_bait_cap - _ft["bait"])
                                        _ft["bait"] += _deposit
                                        player.inventory["worm_bait"] = _worms - _deposit
                                        if player.inventory["worm_bait"] == 0:
                                            del player.inventory["worm_bait"]
                                        player.pending_notifications.append(
                                            (_ft_label, f"Loaded {_deposit} worm bait  •  {_ft['bait']}/{_ft_bait_cap}", None))
                                    elif not _gave_fish:
                                        from blocks import WATER as _FTW
                                        _bx2, _by2 = _ft_pos
                                        _has_water = any(world.get_block(_bx2+_dx, _by2+_dy) == _FTW
                                                         for _dx, _dy in ((0,1),(0,-1),(1,0),(-1,0)))
                                        _total_fish = sum(c for _, c in _ft["accumulated"])
                                        _status = "needs water nearby" if not _has_water else f"bait: {_ft['bait']}  •  caught: {_total_fish}/{_ft_cap}"
                                        player.pending_notifications.append(
                                            (_ft_label, _status, None))
                            _lt_pos = _nearby_light_trap(world, player) if _at_pos is None and _ft_pos is None else None
                            if _lt_pos is not None:
                                trap = world.light_traps.get(_lt_pos)
                                if trap and trap["accumulated"]:
                                    biome = world.biodome_at(int(player.x // BLOCK_SIZE))
                                    for _sp in trap["accumulated"]:
                                        obs = player.insects_observed.get(_sp)
                                        if obs is None:
                                            player.insects_observed[_sp] = {"count": 1, "biome": biome,
                                                                             "best_condition": "good", "morph": None}
                                        else:
                                            obs["count"] += 1
                                        player.discovered_insect_types.add(_sp)
                                        player.pending_notifications.append(
                                            ("Insect", _sp.replace("_", " ").title(), None))
                                    trap["accumulated"].clear()
                                else:
                                    player.pending_notifications.append(
                                        ("Light Trap", "No insects gathered yet", None))
                            _switch_toggled = False
                            if _at_pos is None and _lt_pos is None:
                                from blocks import SWITCH_BLOCK_OFF, SWITCH_BLOCK_ON, LATCH_BLOCK_OFF, LATCH_BLOCK_ON
                                import logic as _logic
                                _sw_pos = player.get_nearby_equipment_pos(SWITCH_BLOCK_OFF) or \
                                          player.get_nearby_equipment_pos(SWITCH_BLOCK_ON)
                                _lt2_pos = player.get_nearby_equipment_pos(LATCH_BLOCK_OFF) or \
                                           player.get_nearby_equipment_pos(LATCH_BLOCK_ON)
                                if _sw_pos is not None:
                                    sbx, sby = _sw_pos
                                    sbid = world.get_block(sbx, sby)
                                    world.set_block(sbx, sby, SWITCH_BLOCK_ON if sbid == SWITCH_BLOCK_OFF else SWITCH_BLOCK_OFF)
                                    _logic.evaluate_full_network(world)
                                    _switch_toggled = True
                                elif _lt2_pos is not None:
                                    lbx, lby = _lt2_pos
                                    lbid = world.get_block(lbx, lby)
                                    world.set_block(lbx, lby, LATCH_BLOCK_ON if lbid == LATCH_BLOCK_OFF else LATCH_BLOCK_OFF)
                                    _logic.evaluate_full_network(world)
                                    _switch_toggled = True
                            equip = None if (_at_pos is not None or _lt_pos is not None or _switch_toggled) else player.get_nearby_equipment()
                            if equip is not None:
                                ui.refinery_open = True
                                ui.refinery_block_id = equip
                                ui.research_open = ui.inventory_open = ui.crafting_open = False
                                ui._inv_search = ""; ui._inv_search_active = False
                                ui.equipment_crafting_open = ui.collection_open = False
                                if equip == TRADE_BLOCK:
                                    trade_pos = player.get_nearby_equipment_pos(TRADE_BLOCK)
                                    if trade_pos is not None:
                                        world.trade_block_data.setdefault(trade_pos, {
                                            "horse_uid": None, "has_cart": False,
                                            "linked_town_id": None, "inventory": {},
                                            "threshold": 10, "state": "idle", "ticks_left": 0.0,
                                        })
                                        ui.active_trade_pos = trade_pos
                                        ui.trade_block_open = True
                                        ui.refinery_open = False
                                elif equip == COMPOST_BIN_BLOCK:
                                    ui.active_compost_bin_pos = player.get_nearby_equipment_pos(COMPOST_BIN_BLOCK)
                                elif equip in (FALCONER_PERCH, MEWS_BLOCK):
                                    perch_pos = player.get_nearby_equipment_pos(equip)
                                    ui.open_falconer_perch(perch_pos, player)
                                elif equip == BOOKCASE_BLOCK:
                                    ui.active_bookcase_pos = player.get_nearby_equipment_pos(BOOKCASE_BLOCK)
                                    if ui.active_bookcase_pos is not None:
                                        world.bookcase_contents.setdefault(ui.active_bookcase_pos, [None] * 6)
                                elif equip == STABLE_BLOCK:
                                    # Find two nearby tamed horses to populate the breeding panel
                                    from horses import Horse as _Horse
                                    tamed_horses = [
                                        e for e in world.entities
                                        if isinstance(e, _Horse) and e.tamed and not e.dead
                                        and e._stable_nearby(world)
                                    ]
                                    if len(tamed_horses) >= 2:
                                        stable_pos = player.get_nearby_equipment_pos(STABLE_BLOCK)
                                        ui.open_horse_breeding(stable_pos, tamed_horses[0], tamed_horses[1])
                                    ui.refinery_open = False
                                elif equip == KENNEL_BLOCK:
                                    from dogs import Dog as _Dog
                                    tamed_dogs = [
                                        e for e in world.entities
                                        if isinstance(e, _Dog) and e.tamed and not e.dead
                                        and e._kennel_nearby(world)
                                    ]
                                    if len(tamed_dogs) >= 2:
                                        kennel_pos = player.get_nearby_equipment_pos(KENNEL_BLOCK)
                                        ui.open_dog_breeding(kennel_pos, tamed_dogs[0], tamed_dogs[1])
                                    ui.refinery_open = False
                                elif equip == CHICKEN_COOP_BLOCK:
                                    ui.active_coop_pos = player.get_nearby_equipment_pos(CHICKEN_COOP_BLOCK)
                                elif equip == FEED_TROUGH_BLOCK:
                                    trough_pos = player.get_nearby_equipment_pos(FEED_TROUGH_BLOCK)
                                    if trough_pos is not None:
                                        held = player.hotbar[player.selected_slot]
                                        _FEED_UNITS = {"wheat": 1, "carrot": 1, "hay_bale": 4}
                                        units = _FEED_UNITS.get(held, 0)
                                        if units and player.inventory.get(held, 0) > 0:
                                            data = world.feed_trough_data.setdefault(
                                                trough_pos, {"contents": 0, "progress": 0.0})
                                            if data["contents"] + units <= 16:
                                                player.inventory[held] -= 1
                                                if player.inventory[held] <= 0:
                                                    del player.inventory[held]
                                                    for _i in range(len(player.hotbar)):
                                                        if player.hotbar[_i] == held:
                                                            player.hotbar[_i] = None
                                                            break
                                                data["contents"] += units
                                elif equip == TEA_HOUSE_BLOCK:
                                    _close_all_ui()
                                    ui.open_tea_house()
                                elif equip == GAMBLING_TABLE:
                                    _close_all_ui()
                                    ui.open_gambling_table(3)
                                elif equip == BET_COUNTER:
                                    from cities import RacingBookkeeperNPC as _RBN
                                    _bkp = None
                                    for _ent in world.entities:
                                        if isinstance(_ent, _RBN):
                                            _ex = abs(_ent.x - player.x)
                                            if _ex < 16 * 32:
                                                _bkp = _ent
                                                break
                                    _close_all_ui()
                                    ui.open_racing(_bkp, player)
                                elif equip == TRAINING_PADDOCK_BLOCK:
                                    _close_all_ui()
                                    ui.open_training_paddock(player, world)
                                elif equip == BEEHIVE_BLOCK:
                                    _hive_pos = player.get_nearby_equipment_pos(BEEHIVE_BLOCK)
                                    if _hive_pos is not None:
                                        ui._open_beehive(_hive_pos[0], _hive_pos[1], player)
                                elif equip == MEAD_VAT_BLOCK:
                                    _mv_pos = player.get_nearby_equipment_pos(MEAD_VAT_BLOCK)
                                    if _mv_pos is not None:
                                        ui._open_mead_vat(_mv_pos[0], _mv_pos[1], player)
                                elif equip == MEAD_CELLAR_BLOCK:
                                    _mc_pos = player.get_nearby_equipment_pos(MEAD_CELLAR_BLOCK)
                                    if _mc_pos is not None:
                                        ui._open_mead_cellar(_mc_pos[0], _mc_pos[1], player)
                                elif equip == SALTING_RACK_BLOCK:
                                    _sr_pos = player.get_nearby_equipment_pos(SALTING_RACK_BLOCK)
                                    if _sr_pos is not None:
                                        ui._open_salting_rack(_sr_pos[0], _sr_pos[1], player)
                                elif equip == CURING_CELLAR_BLOCK:
                                    _cc_pos = player.get_nearby_equipment_pos(CURING_CELLAR_BLOCK)
                                    if _cc_pos is not None:
                                        ui._open_curing_cellar(_cc_pos[0], _cc_pos[1], player)
                                else:
                                    from blocks import (HOPPER_BLOCK as _HOP2,
                                                        PIPE_OUTPUT_BLOCK as _PO2,
                                                        PIPE_FILTER_BLOCK as _PF2,
                                                        PIPE_SORTER_BLOCK as _PS2,
                                                        FACTORY_BLOCK as _FAC2)
                                    equip_pos = player.get_nearby_equipment_pos(equip)
                                    if equip == _HOP2:
                                        _close_all_ui()
                                        ui.open_hopper(world, equip_pos)
                                    elif equip == _PO2:
                                        _close_all_ui()
                                        ui.open_pipe_output(world, equip_pos)
                                    elif equip == _PF2:
                                        _close_all_ui()
                                        ui.open_pipe_filter(world, equip_pos)
                                    elif equip == _PS2:
                                        _close_all_ui()
                                        ui.open_pipe_sorter(world, equip_pos)
                                    elif equip == _FAC2:
                                        _close_all_ui()
                                        ui.open_factory(world, equip_pos)
                                    else:
                                        ui.active_compost_bin_pos = None
                            else:
                                ui.refinery_open = False

                if event.key == pygame.K_BACKSLASH:
                    world.toggle_wire_mode()

                if event.key == pygame.K_p and not _any_ui_open():
                    world.toggle_pipe_mode()

                if event.key == pygame.K_g and not _any_ui_open():
                    # Toggle stay/follow for all tamed dogs within 8 blocks
                    from dogs import Dog as _Dog
                    for _dog in world.entities:
                        if isinstance(_dog, _Dog) and _dog.tamed and not _dog.dead:
                            if _dog.in_range_stay_toggle(player, radius=8):
                                _dog.stay_mode = not _dog.stay_mode

                if event.key == pygame.K_q and not _any_ui_open():
                    # Deconstruct nearby idle elevator car
                    nearby_car = next(
                        (c for c in world.elevator_cars if c.in_range(player) and c.state == "idle" and c.rider is None),
                        None,
                    )
                    if nearby_car is not None:
                        world.elevator_cars.remove(nearby_car)
                        player._add_item("elevator_car")

                if event.key == pygame.K_m:
                    renderer.minimap_visible = not renderer.minimap_visible

                if event.key == pygame.K_f and not _any_ui_open() and not player.dead:
                    player.on_fish_press()

                # Hotbar number keys 1–8
                for i in range(8):
                    if event.key == getattr(pygame, f"K_{i + 1}", None):
                        player.selected_slot = i

                # Shape brush cycling (Tab = next shape)
                if event.key == pygame.K_TAB and not _any_ui_open():
                    from block_shapes import SHAPE_VARIANTS as _SV
                    player.shape_idx = (player.shape_idx + 1) % len(_SV)

            if event.type == pygame.MOUSEWHEEL:
                if not player.dead and not ui.cheat_open:
                    if ui.coa_designer_open:
                        ui.handle_coa_scroll(event.y)
                    elif ui.reputation_screen_open:
                        if getattr(ui, '_rep_view', 'list') == 'map':
                            ui._map_scroll = max(0, getattr(ui, '_map_scroll', 0) - event.y * 20)
                        else:
                            ui.handle_reputation_screen_scroll(-event.y * 20)
                    elif ui.help_open:
                        mx, my = pygame.mouse.get_pos()
                        left_rect = getattr(ui, '_help_left_rect', None)
                        if left_rect and left_rect.collidepoint(mx, my):
                            ui._help_topic_scroll = max(0, min(ui._help_topic_max_scroll,
                                                               ui._help_topic_scroll - event.y * 20))
                        else:
                            ui._help_scroll = max(0, min(ui._help_max_scroll,
                                                         ui._help_scroll - event.y * 20))
                    elif ui.wildflower_display_open:
                        max_s = max(0, len(player.wildflowers) - 6)
                        ui._display_scroll = max(0, min(max_s, getattr(ui, '_display_scroll', 0) - event.y))
                    elif ui.research_open or ui.inventory_open or ui.crafting_open or ui.collection_open or ui.refinery_open or ui.chest_open or ui.breeding_open or ui.garden_open or ui.horse_breeding_open or ui.dog_breeding_open or ui.dog_view_open:
                        ui.handle_scroll(event.y)
                    elif getattr(player, 'dynasty_tree_open', False):
                        _max = getattr(ui, '_tree_max_scroll', 0)
                        ui._tree_scroll = max(0, min(_max,
                            getattr(ui, '_tree_scroll', 0) - event.y * 30))
                    elif getattr(player, 'dynasty_panel_open', False):
                        _max = getattr(ui, '_chronicle_max_scroll', 0)
                        ui._chronicle_scroll = max(0, min(_max,
                            getattr(ui, '_chronicle_scroll', 0) - event.y * 20))
                    elif ui.active_npc is not None:
                        from cities import CoinDealerNPC, ChapterMasterNPC
                        from coin_npcs import (MoneyChangerNPC, CoinAppraiserNPC,
                                                CoinCollectorNPC)
                        if isinstance(ui.active_npc, CoinDealerNPC):
                            tab = getattr(ui, "_coin_dealer_tab", "buy")
                            if tab == "buy":
                                ui._coin_dealer_scroll = max(0,
                                    getattr(ui, "_coin_dealer_scroll", 0) - event.y)
                            else:
                                ui._coin_dealer_sell_scroll = max(0,
                                    getattr(ui, "_coin_dealer_sell_scroll", 0) - event.y)
                        elif isinstance(ui.active_npc, MoneyChangerNPC):
                            ui._money_changer_scroll = max(0,
                                getattr(ui, "_money_changer_scroll", 0) - event.y)
                        elif isinstance(ui.active_npc, CoinAppraiserNPC):
                            ui._appraiser_scroll = max(0,
                                getattr(ui, "_appraiser_scroll", 0) - event.y)
                        elif isinstance(ui.active_npc, CoinCollectorNPC):
                            ui._collector_scroll = max(0,
                                getattr(ui, "_collector_scroll", 0) - event.y)
                        elif (isinstance(ui.active_npc, ChapterMasterNPC)
                              and getattr(ui, "_ch_tab", "quests") == "shop"):
                            ui._ch_shop_scroll = max(0,
                                getattr(ui, "_ch_shop_scroll", 0) - event.y)
                    elif (player.inspecting_npc is not None
                          and not getattr(player, 'dynasty_panel_open', False)):
                        _max = getattr(ui, '_inspect_scroll_max', 0)
                        ui._inspect_panel_scroll = max(0, min(_max,
                            getattr(ui, '_inspect_panel_scroll', 0) - event.y * 20))
                    elif not _any_ui_open():
                        player.selected_slot = (player.selected_slot - event.y) % 8

            if event.type == pygame.MOUSEMOTION:
                if ui.inventory_open:
                    ui.handle_inventory_drag(event.pos)
                if ui._jw_drag_uid is not None:
                    ui._jw_drag_pos = event.pos
                if ui.garden_open:
                    ui.handle_garden_mousemotion(event.pos)
                if ui.refinery_open and ui.refinery_block_id == OXIDATION_STATION_BLOCK:
                    ui.handle_oxidation_mouse_motion(event.pos)

            if event.type == pygame.MOUSEBUTTONUP:
                if ui.inventory_open:
                    ui.handle_inventory_release(event.pos, player)
                if ui._jw_drag_uid is not None:
                    ui._handle_jewelry_drop(event.pos, player)
                if ui.garden_open:
                    ui.handle_garden_mouseup(event.pos, player)
                if ui.refinery_open and ui.refinery_block_id == OXIDATION_STATION_BLOCK:
                    ui.handle_oxidation_mouse_up(event.pos)
                if ui.refinery_open and ui.refinery_block_id == SALTING_RACK_BLOCK:
                    ui.handle_salting_rack_mouseup(player)
                # Bow / spear gun — release to fire (only when no UI is open)
                if event.button == 1 and not player.dead and not _any_ui_open():
                    player.release_aim_shot(
                        event.pos[0], event.pos[1],
                        renderer.cam_x, renderer.cam_y)
                # End sculpt drag on any mouse release
                if getattr(ui, '_sculpt_drag_mode', None) is not None:
                    ui._sculpt_drag_mode = None
                # End pottery wheel drag
                if getattr(ui, '_wheel_drag_row', None) is not None:
                    ui._wheel_drag_row = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player.dead or ui.cheat_open:
                    pass
                elif event.button == 1 and ui.handle_hints_click(event.pos):
                    pass
                elif ui.help_open:
                    ui.handle_help_click(event.pos)
                elif ui.pause_open:
                    action = ui.handle_pause_click(event.pos)
                    if action == "resume":
                        ui.pause_open = False
                    elif action == "save":
                        _save_and_notify(world, player, research)
                        print("Game saved.")
                    elif action == "quit":
                        _save_and_notify(world, player, research)
                        running = False
                elif ui.automation_open:
                    action = ui.handle_automation_click(event.pos, player)
                    if action == "pickup":
                        auto = ui.active_automation
                        auto.take_all(player)
                        fuel_back = int(auto.fuel)
                        if fuel_back > 0:
                            fuel_item = AUTOMATION_DEFS[auto.auto_type]["fuel_item"]
                            for _ in range(fuel_back):
                                player._add_item(fuel_item)
                        world.automations.remove(auto)
                        item_id = AUTOMATION_ITEM.get(auto.auto_type)
                        if item_id:
                            player._add_item(item_id)
                        ui.automation_open = False
                        ui.active_automation = None
                elif ui.farm_bot_open:
                    result = ui.handle_farm_bot_click(event.pos, player)
                    if result == "pickup":
                        fb = ui.active_farm_bot
                        fb.take_all(player)
                        fb.get_seeds(player)
                        fuel_back = int(fb.fuel)
                        if fuel_back > 0:
                            fuel_item = fb._def["fuel_item"]
                            for _ in range(fuel_back):
                                player._add_item(fuel_item)
                        world.farm_bots.remove(fb)
                        item_id = FARM_BOT_ITEM.get(fb.bot_type)
                        if item_id:
                            player._add_item(item_id)
                        ui.farm_bot_open = False
                        ui.active_farm_bot = None
                elif ui.backhoe_open:
                    result = ui.handle_backhoe_click(event.pos, player)
                    if result == "ride":
                        bh = ui.active_backhoe
                        ui.close_backhoe()
                        player.mounted_machine = bh
                        player.x = bh.x + (bh.W - PLAYER_W) / 2
                        player.y = bh.y
                    elif result == "pickup":
                        bh = ui.active_backhoe
                        bh.take_all(player)
                        fuel_back = int(bh.fuel)
                        for _ in range(fuel_back):
                            player._add_item("oil_barrel")
                        world.backhoes.remove(bh)
                        player._add_item("backhoe_item")
                        ui.close_backhoe()
                elif ui.town_menu_open:
                    ui.handle_town_menu_click(event.pos, player)
                elif ui.coa_designer_open:
                    ui.handle_coa_click(event.pos)
                elif ui.city_block_menu_open:
                    ui.handle_city_block_click(event.pos, player)
                elif ui.job_panel_open:
                    ui.handle_job_panel_click(event.pos, player)
                elif ui.hire_panel_open:
                    ui.handle_hire_panel_click(event.pos, player)
                elif ui.reputation_screen_open:
                    ui.handle_reputation_screen_click(event.pos)
                elif ui.outpost_menu_open:
                    ui.handle_sommelier_click(event.pos, player)
                elif getattr(player, "inspecting_npc", None) is not None:
                    ui.handle_inspect_click(event.pos, player, world)
                elif ui.npc_open:
                    ui.handle_npc_click(event.pos, player)
                elif ui.research_open:
                    ui.handle_research_click(event.pos, player, world, research)
                elif ui.inventory_open:
                    ui.handle_inventory_click(event.pos, player, event.button)
                elif ui.crafting_open:
                    ui.handle_crafting_click(event.pos, player, event.button, research,
                                             debug=settings.get("debug", False))
                elif ui.collection_open:
                    ui.handle_collection_click(event.pos, player)
                elif ui.breeding_open:
                    ui.handle_breeding_click(event.pos, player)
                elif ui.refinery_open:
                    if ui.refinery_block_id == GEM_CUTTER_BLOCK:
                        ui.handle_gem_cutter_click(event.pos, player)
                    else:
                        ui.handle_refinery_click(event.pos, player, debug=settings.get("debug", False))
                        # Roaster heat button also responds to mouse down
                        if ui.refinery_block_id == ROASTER_BLOCK:
                            if hasattr(ui, '_roast_heat_btn') and ui._roast_heat_btn and ui._roast_heat_btn.collidepoint(event.pos):
                                ui._roast_heat_held = True
                        if ui.refinery_block_id == GRAPE_PRESS_BLOCK:
                            if getattr(ui, '_press_btn', None) and ui._press_btn.collidepoint(event.pos):
                                ui._press_held = True
                        if ui.refinery_block_id == FERMENTATION_BLOCK:
                            if getattr(ui, '_ferm_temp_btn', None) and ui._ferm_temp_btn.collidepoint(event.pos):
                                ui._ferm_temp_held = True
                            if getattr(ui, '_ferm_nut_btn', None) and ui._ferm_nut_btn.collidepoint(event.pos):
                                ui._ferm_nut_held = True
                elif ui.horse_breeding_open:
                    ui.handle_horse_breeding_click(event.pos, player, world)
                elif ui.dog_breeding_open:
                    ui.handle_kennel_breeding_click(event.pos, player, world)
                elif ui.dog_view_open:
                    ui.handle_dog_view_click(event.pos, player)
                elif ui.tea_house_open:
                    ui.handle_tea_house_click(event.pos, player, world)
                elif ui.gambling_open:
                    ui.handle_gambling_click(event.pos, player)
                elif ui.racing_open:
                    ui.handle_racing_click(event.pos, player)
                elif getattr(ui, "training_paddock_open", False):
                    ui.handle_training_paddock_click(event.pos, player, world)
                elif ui.arena_open:
                    ui.handle_arena_click(event.pos, player)
                elif getattr(ui, "jousting_open", False):
                    ui.handle_jousting_click(*event.pos, player)
                elif ui.bazaar_open:
                    ui.handle_bazaar_click(event.pos, player)
                elif getattr(ui, "stock_exchange_open", False):
                    ui.handle_stock_exchange_click(event.pos, player)
                elif ui.wardrobe_open:
                    ui.handle_wardrobe_click(event.pos, player)
                elif ui.trade_block_open:
                    ui.handle_trade_block_click(event.pos, player, world, event.button)
                elif ui.chest_open:
                    ui.handle_chest_click(event.pos, player, event.button)
                elif getattr(ui, "hopper_open", False):
                    ui.handle_hopper_click(event.pos, world)
                elif getattr(ui, "pipe_output_open", False):
                    ui.handle_pipe_output_click(event.pos, world)
                elif getattr(ui, "pipe_filter_open", False):
                    ui.handle_pipe_filter_click(event.pos, player, world)
                elif getattr(ui, "pipe_sorter_open", False):
                    ui.handle_pipe_sorter_click(event.pos, player, world)
                elif getattr(ui, "factory_open", False):
                    ui.handle_factory_click(event.pos, player, world, event.button)
                elif ui.garden_open:
                    ui.handle_garden_mousedown(event.pos, player)
                elif ui.wildflower_display_open:
                    ui.handle_wildflower_display_click(event.pos, player)
                else:
                    # Left-click on any NPC opens inspect panel
                    if event.button == 1 and not player.dead:
                        mx, my = event.pos
                        from cities import NPC as _NPC
                        _clicked_npc = None
                        for _ent in world.entities:
                            if not isinstance(_ent, _NPC):
                                continue
                            _nsx = int(_ent.x - renderer.cam_x)
                            _nsy = int(_ent.y - renderer.cam_y)
                            if pygame.Rect(_nsx - 4, _nsy - 4, _ent.NPC_W + 8, _ent.NPC_H + 8).collidepoint(mx, my):
                                _clicked_npc = _ent
                                break
                        if _clicked_npc is not None:
                            from cities import LandmarkNPC as _LandmarkNPC_c
                            if isinstance(_clicked_npc, _LandmarkNPC_c):
                                pass  # landmark interaction is via E on the flag
                            elif getattr(player, "inspecting_npc", None) is _clicked_npc:
                                player.inspecting_npc = None
                                player.gift_panel_open = False
                                player.fulfill_request_open = False
                            else:
                                _close_all_ui()
                                player.inspecting_npc = _clicked_npc
                                player.gift_panel_open = False
                                player.fulfill_request_open = False
                                ui._inspect_panel_scroll = 0
                                _uid = getattr(_clicked_npc, "npc_uid", None)
                                if _uid and _uid not in player.npc_relationships:
                                    _rid = getattr(_clicked_npc, "dynasty_id", None)
                                    if _rid in getattr(player, "rival_dynasty_regions", set()):
                                        player.npc_relationships[_uid] = -20
                                    else:
                                        player.npc_relationships[_uid] = 0
                                import npc_preferences as _npc_prefs
                                _npc_prefs.maybe_generate_request(
                                    player, _clicked_npc, getattr(world, "day_count", 0)
                                )
                    # Check for bird clicks before falling through to hotbar/world
                    if event.button == 1 and not ui._bird_obs_active:
                        _bino_held = player.hotbar[player.selected_slot] == "binoculars"
                        mx, my = event.pos
                        for bird in world.birds:
                            bsx = int(bird.x - renderer.cam_x)
                            bsy = int(bird.y - renderer.cam_y)
                            if pygame.Rect(bsx - 4, bsy - 4, bird.W + 8, bird.H + 8).collidepoint(mx, my):
                                _settled = (bird.state in ("perching", "stopped", "landing")
                                            or getattr(bird, 'IS_GROUND', False))
                                if _bino_held or _settled:
                                    ui.open_bird_observation(bird)
                                break
                    # Check for insect clicks (requires bug_net equipped)
                    held = player.hotbar[player.selected_slot]
                    if event.button == 1 and held == "bug_net":
                        mx, my = event.pos
                        _night_a = renderer._sky_night_alpha(world.time_of_day)
                        from world import DAY_DURATION as _DAY_DUR
                        _tod = world.time_of_day
                        _is_dawn = _tod < 60.0
                        _is_dusk = _DAY_DUR - 60.0 <= _tod < _DAY_DUR
                        for ins in world.insects:
                            if ins.spooked:
                                continue
                            if ins.NIGHT_ONLY and _night_a < 30:
                                continue
                            if ins.DAWN_ONLY and not _is_dawn:
                                continue
                            if ins.DUSK_ONLY and not _is_dusk:
                                continue
                            isx = int(ins.x - renderer.cam_x)
                            isy = int(ins.y - renderer.cam_y)
                            pad = 14 if ins.WING_TYPE == "firefly" else 4
                            if pygame.Rect(isx - pad, isy - pad, ins.W + pad * 2, ins.H + pad * 2).collidepoint(mx, my):
                                sp = ins.SPECIES
                                biome = world.biodome_at(int(ins.x // BLOCK_SIZE))
                                morph = _insect_morph_at(ins, world.seed)
                                existing = player.insects_observed.get(sp)
                                if existing is None:
                                    player.insects_observed[sp] = {"count": 1, "biome": biome,
                                                                    "best_condition": "perfect", "morph": morph}
                                else:
                                    existing["count"] += 1
                                    if morph and not existing.get("morph"):
                                        existing["morph"] = morph
                                player.discovered_insect_types.add(sp)
                                player.pending_notifications.append(
                                    ("Insect", sp.replace("_", " ").title(), ins.RARITY))
                                drop = INSECT_DROP_TABLE.get(sp)
                                if drop:
                                    player.inventory[drop] = player.inventory.get(drop, 0) + 1
                                ins.spook()
                                break
                    # Bow / spear gun — hold left-click to aim, release to fire
                    if event.button == 1 and not player.dead:
                        player.start_aim("bow") or player.start_aim("spear")
                    # Melee attack — left-click with weapon equipped (no UI open)
                    if event.button == 1 and not player.dead and player.equipped_weapon_uid and not _any_ui_open():
                        from animals import HuntableAnimal
                        from constants import PLAYER_H
                        px_c = int(player.x + PLAYER_W / 2)
                        py_c = int(player.y + PLAYER_H / 2)
                        melee_rect = pygame.Rect(px_c - 48, py_c - 32, 96, 64)
                        for entity in world.entities:
                            if isinstance(entity, HuntableAnimal) and not entity.dead:
                                if melee_rect.colliderect(entity.rect):
                                    drops = player.try_melee_attack(entity)
                                    if drops is not None:
                                        animal_id = entity.animal_id
                                        player.animals_hunted[animal_id] = player.animals_hunted.get(animal_id, 0) + 1
                                        player.pending_notifications.append(
                                            ("Hunting", f"{animal_id.title()} struck", None))
                                        if drops:
                                            for item_id, count in drops:
                                                player._add_item(item_id, count)
                                    break
                    # Landmark flag right-click: show landmark info toast
                    if event.button == 3:
                        from blocks import LANDMARK_FLAG_BLOCK as _LFB
                        from landmarks import landmark_for
                        from towns import REGIONS, TOWNS
                        mx_w = event.pos[0] + renderer.cam_x
                        my_w = event.pos[1] + renderer.cam_y
                        _lbx = int(mx_w // BLOCK_SIZE)
                        _lby = int(my_w // BLOCK_SIZE)
                        if world.get_bg_block(_lbx, _lby) == _LFB or world.get_bg_block(_lbx, _lby + 1) == _LFB:
                            for _twn in TOWNS.values():
                                if abs(_twn.center_bx - _lbx) < 20:
                                    _reg = REGIONS.get(_twn.region_id)
                                    if _reg and _reg.agenda:
                                        _spec = landmark_for(_reg.agenda, getattr(_reg, "biome_group", ""))
                                        if not hasattr(world, "_town_toasts"):
                                            world._town_toasts = []
                                        world._town_toasts.append(
                                            f"{_spec['name']} — {_spec['tagline']}")
                                    break
                    # Logic block right-click: rotate gates / toggle sensor mode / cycle pulse period
                    if event.button == 3 and not _any_ui_open():
                        from blocks import (LOGIC_ROTATEABLE_BLOCKS as _LRB,
                                            DAY_SENSOR_BLOCK as _DSB, NIGHT_SENSOR_BLOCK as _NSB,
                                            PULSE_GEN_BLOCK as _PGBR)
                        import logic as _logicr
                        _rx_w = event.pos[0] + renderer.cam_x
                        _ry_w = event.pos[1] + renderer.cam_y
                        _rbx = int(_rx_w // BLOCK_SIZE)
                        _rby = int(_ry_w // BLOCK_SIZE)
                        _rbid = world.get_block(_rbx, _rby)
                        if _rbid in _LRB:
                            _gs = world.logic_state.get((_rbx, _rby), {})
                            _gs["facing"] = _logicr._rotate_facing(_gs.get("facing", "right"))
                            world.logic_state[(_rbx, _rby)] = _gs
                            _logicr.evaluate_full_network(world)
                        elif _rbid == _DSB:
                            world.set_block(_rbx, _rby, _NSB)
                            _logicr.evaluate_full_network(world)
                        elif _rbid == _NSB:
                            world.set_block(_rbx, _rby, _DSB)
                            _logicr.evaluate_full_network(world)
                        elif _rbid == _PGBR:
                            _pgs = world.logic_state.get((_rbx, _rby), {})
                            _periods = [0.25, 0.5, 1.0, 2.0, 4.0, 8.0]
                            _cur = _pgs.get("period", 2.0)
                            try:
                                _pidx = _periods.index(_cur)
                            except ValueError:
                                _pidx = 3
                            _pgs["period"] = _periods[(_pidx + 1) % len(_periods)]
                            world.logic_state[(_rbx, _rby)] = _pgs
                        # Repeater right-click: cycle delay
                        from blocks import (REPEATER_BLOCK as _RPTBR,
                                            COUNTER_BLOCK as _CTRBR,
                                            COMPARATOR_BLOCK as _CMPBR,
                                            SEQUENCER_BLOCK as _SEQBR,
                                            T_FLIPFLOP_BLOCK as _TFFBR)
                        if _rbid == _RPTBR:
                            _rgs = world.logic_state.get((_rbx, _rby), {})
                            _delays = [0.25, 0.5, 1.0, 2.0, 4.0]
                            _dcur = _rgs.get("delay", 0.5)
                            try:
                                _didx = _delays.index(_dcur)
                            except ValueError:
                                _didx = 1
                            _rgs["delay"] = _delays[(_didx + 1) % len(_delays)]
                            world.logic_state[(_rbx, _rby)] = _rgs
                        # Counter right-click: cycle threshold 2-3-4-5-6-8-10-12-16
                        elif _rbid == _CTRBR:
                            _cgs = world.logic_state.get((_rbx, _rby), {})
                            _thresholds = [2, 3, 4, 5, 6, 8, 10, 12, 16]
                            _ct = _cgs.get("threshold", 4)
                            try:
                                _cidx = _thresholds.index(_ct)
                            except ValueError:
                                _cidx = 2
                            _cgs["threshold"] = _thresholds[(_cidx + 1) % len(_thresholds)]
                            world.logic_state[(_rbx, _rby)] = _cgs
                            _logicr.evaluate_full_network(world)
                        # Comparator right-click: cycle threshold 1-8
                        elif _rbid == _CMPBR:
                            _mpgs = world.logic_state.get((_rbx, _rby), {})
                            _mpgs["threshold"] = (_mpgs.get("threshold", 4) % 8) + 1
                            world.logic_state[(_rbx, _rby)] = _mpgs
                            _logicr.evaluate_full_network(world)
                        # Sequencer right-click: manually advance step
                        elif _rbid == _SEQBR:
                            _sgs = world.logic_state.get((_rbx, _rby), {})
                            _sgs["step"] = (_sgs.get("step", 0) + 1) % 4
                            world.logic_state[(_rbx, _rby)] = _sgs
                            _logicr.evaluate_full_network(world)
                        # T-Flip-Flop right-click: manual toggle
                        elif _rbid == _TFFBR:
                            _tgs = world.logic_state.get((_rbx, _rby), {})
                            _tgs["q"] = not _tgs.get("q", False)
                            world.logic_state[(_rbx, _rby)] = _tgs
                            _logicr.evaluate_full_network(world)
                        # Player Sensor right-click: cycle detection radius 3→5→8→12
                        from blocks import PLAYER_SENSOR_BLOCK as _PLRSNS_R
                        if _rbid == _PLRSNS_R:
                            _psgs = world.logic_state.get((_rbx, _rby), {})
                            _radii = [3, 5, 8, 12]
                            _cur_r = _psgs.get("radius", 5)
                            try:
                                _ridx = _radii.index(_cur_r)
                            except ValueError:
                                _ridx = 1
                            _psgs["radius"] = _radii[(_ridx + 1) % len(_radii)]
                            world.logic_state[(_rbx, _rby)] = _psgs
                        # Pipe Buffer right-click: cycle release rate 1→2→4→8 ticks
                        from blocks import PIPE_BUFFER_BLOCK as _PBFR
                        if _rbid == _PBFR:
                            _pbcfg = world.pipe_state.get((_rbx, _rby), {})
                            _rates = [1, 2, 4, 8]
                            _cur_rate = _pbcfg.get("rate", 2)
                            try:
                                _prdx = _rates.index(_cur_rate)
                            except ValueError:
                                _prdx = 1
                            _pbcfg["rate"] = _rates[(_prdx + 1) % len(_rates)]
                            world.pipe_state[(_rbx, _rby)] = _pbcfg
                    # Sculptor right-click: restore stone in carve phase
                    if event.button == 3 and ui.refinery_open:
                        from blocks import SCULPTORS_BENCH as _SCULPTORS_BENCH_R
                        if ui.refinery_block_id == _SCULPTORS_BENCH_R and ui._sculpt_phase == "carve":
                            ui._handle_sculptor_bench_click(event.pos, player, right=True)
                    # Tapestry Frame right-click: remove thread in weave phase
                    if event.button == 3 and ui.refinery_open:
                        from blocks import TAPESTRY_FRAME_BLOCK as _TAPESTRY_FRAME_R
                        if ui.refinery_block_id == _TAPESTRY_FRAME_R and ui._tapestry_phase == "weave":
                            ui._handle_tapestry_frame_click(event.pos, player, right=True)
                    ui.handle_hotbar_click(event.pos, player)

        keys = pygame.key.get_pressed()
        mouse_btns = pygame.mouse.get_pressed()
        mouse_scr_pos = pygame.mouse.get_pos()
        mouse_world = (
            mouse_scr_pos[0] + renderer.cam_x,
            mouse_scr_pos[1] + renderer.cam_y,
        )

        # Jousting: poll SPACE during the CHARGE phase
        if getattr(ui, "jousting_open", False):
            ui.update_jousting_input(keys, player)

        # Roaster: poll SPACE for heat
        if ui.refinery_open and ui.refinery_block_id == ROASTER_BLOCK:
            ui.handle_roaster_keys(keys)
        # Grape Press: poll SPACE for pressure
        if ui.refinery_open and ui.refinery_block_id == GRAPE_PRESS_BLOCK:
            ui.handle_press_keys(keys)
        # Fermentation Tank: poll SPACE (temp) + N (nutrient)
        if ui.refinery_open and ui.refinery_block_id == FERMENTATION_BLOCK:
            ui.handle_fermenter_keys(keys)
        # Copper Still: poll SPACE for heat
        if ui.refinery_open and ui.refinery_block_id == STILL_BLOCK:
            ui.handle_still_keys(keys)
        # Brew Kettle: poll SPACE for heat
        if ui.refinery_open and ui.refinery_block_id == BREW_KETTLE_BLOCK:
            ui.handle_brew_keys(keys)
        # Fermentation Vessel: poll SPACE to cool
        if ui.refinery_open and ui.refinery_block_id == FERM_VESSEL_BLOCK:
            ui.handle_ferm_keys(keys)
        # Oxidation Station: poll SPACE to slow oxidation
        if ui.refinery_open and ui.refinery_block_id == OXIDATION_STATION_BLOCK:
            ui.handle_oxidation_keys(keys, dt, player)
        # Spinning Wheel: poll SPACE for fiber tension
        if ui.refinery_open and ui.refinery_block_id == SPINNING_WHEEL_BLOCK:
            ui.handle_spinning_wheel_keys(keys, dt, player)
        # Beehive: poll SPACE for spin extraction
        if ui.refinery_open and ui.refinery_block_id == BEEHIVE_BLOCK:
            ui.handle_beehive_keys(keys, dt, player)
        # Mead Vat: poll SPACE for stirring mini-game
        if ui.refinery_open and ui.refinery_block_id == MEAD_VAT_BLOCK:
            ui.handle_mead_vat_keys(keys, dt, player)
        # Salting Rack: poll mouse held for zone filling
        if ui.refinery_open and ui.refinery_block_id == SALTING_RACK_BLOCK:
            ui.handle_charcuterie_keys(keys, dt, player)
        # Pigment Mill: poll SPACE for grind rhythm
        from blocks import PIGMENT_MILL_BLOCK as _PIGMENT_MILL_PF
        if ui.refinery_open and ui.refinery_block_id == _PIGMENT_MILL_PF:
            ui.handle_pigment_keys(keys, dt, player)

        # Sculptor's Bench: per-frame drag painting + hover tracking
        if ui.refinery_open and getattr(ui, '_sculpt_phase', 'idle') == 'carve':
            from blocks import SCULPTORS_BENCH as _SCULPTORS_BENCH_PF
            if ui.refinery_block_id == _SCULPTORS_BENCH_PF:
                ui._sculpt_update_drag(mouse_scr_pos, mouse_btns)
        # Tapestry Frame: per-frame drag weaving + hover tracking
        if ui.refinery_open and getattr(ui, '_tapestry_phase', 'idle') == 'weave':
            from blocks import TAPESTRY_FRAME_BLOCK as _TAPESTRY_FRAME_PF
            if ui.refinery_block_id == _TAPESTRY_FRAME_PF:
                ui._tapestry_update_drag(mouse_scr_pos, mouse_btns)

        # Pottery: per-frame held key (SPACE for kiln heat) + wheel drag
        from blocks import POTTERY_WHEEL_BLOCK as _PWB_PF, POTTERY_KILN_BLOCK as _PKB_PF
        if ui.refinery_open and ui.refinery_block_id in (_PWB_PF, _PKB_PF):
            ui.handle_pottery_keys(keys, dt, player)

        # Evaporation pan: per-frame held key (SPACE for heat)
        from blocks import EVAPORATION_PAN_BLOCK as _EVAP_PF
        if ui.refinery_open and ui.refinery_block_id == _EVAP_PF:
            ui.handle_evap_pan_keys(keys, dt, player)
        if ui.refinery_open and ui.refinery_block_id == _PWB_PF and ui._wheel_phase == "shaping":
            ui._handle_pottery_wheel_drag(mouse_scr_pos, mouse_btns)

        # Forge: per-frame held key (SPACE for bellows) + hammer drag + temperature drain
        from blocks import FORGE_BLOCK as _FORGE_PF
        if ui.refinery_open and ui.refinery_block_id == _FORGE_PF:
            ui.handle_forge_keys(keys, dt, player)
            ui.smith_update_drag(mouse_scr_pos, mouse_btns)
        ui.smith_update(dt, player)

        if ui.pause_open:
            renderer.draw_world(world, player)
            renderer.draw_player(player)
            renderer.draw_dropped_items(world.dropped_items)
            renderer.draw_entities(world.entities)
            renderer.draw_tea_house_visitors(world.tea_house_visitors)
            renderer.draw_arrows(world.arrows)
            renderer.draw_nests(world.nests)
            renderer.draw_birds(world.birds)
            renderer.draw_insects(world.insects, world.time_of_day)
            renderer.draw_reptiles(world.reptiles)
            renderer.draw_live_fish(world.live_fish)
            renderer.draw_spears(world.spears)
            renderer.draw_aim_preview(player, mouse_scr_pos)
            renderer.draw_automations(world.automations)
            renderer.draw_farm_bots(world.farm_bots)
            renderer.draw_backhoes(world.backhoes, player)
            renderer.draw_elevator_cars(world.elevator_cars)
            renderer.draw_minecarts(world.minecarts)
            renderer.draw_boats(world.boats, player, world)
            ui.draw(player, research, dt)
            pygame.display.flip()
            continue

        if player.dead:
            # Freeze game while dead; just do minimal updates
            renderer.draw_world(world, player)
            renderer.draw_player(player)
            renderer.draw_dropped_items(world.dropped_items)
            ui.draw(player, research, dt)
            renderer.draw_minimap(world, player, dt)
            pygame.display.flip()
            continue

        # Backhoe mounted controls
        _BACKHOE_SPEED = 2
        if player.mounted_machine is not None and not _any_ui_open() and not ui.cheat_open:
            bh = player.mounted_machine
            if keys[pygame.K_a]:
                bh.move(-_BACKHOE_SPEED, world)
            if keys[pygame.K_d]:
                bh.move(_BACKHOE_SPEED, world)
            if keys[pygame.K_z]:
                bh.dig(dt, world)
            bh.apply_gravity(world)
            player.x = bh.x + (bh.W - PLAYER_W) / 2
            player.y = bh.y

        # Pending horse break minigame trigger
        if getattr(player, '_pending_horse_break', None) is not None:
            ui.open_horse_breaking(player._pending_horse_break)
            player._pending_horse_break = None

        # Pending dog view panel trigger
        if getattr(player, '_pending_dog_view', None) is not None:
            ui.open_dog_view(player._pending_dog_view)
            player._pending_dog_view = None

        # Pending falconry capture trigger
        if getattr(player, '_pending_raptor_capture', None) is not None:
            species_key, biome, src = player._pending_raptor_capture
            player._pending_raptor_capture = None
            # Open the perch panel implicitly so capture UI has a container
            ui.refinery_open = True
            ui.refinery_block_id = FALCONER_PERCH
            if not hasattr(ui, "_fy_selected_uid"):
                ui.open_falconer_perch(None, player)
            ui.open_falconry_capture(species_key, biome, src)

        # Horse breaking minigame tick
        if ui._hb_active:
            result = ui.update_horse_breaking(keys, dt)
            if result == "success":
                horse = ui._hb_horse
                horse._broken = True
                player.mounted_horse = horse
                horse.rider = player
                ui._hb_horse = None
            elif result == "fail":
                if ui._hb_horse is not None:
                    ui._hb_horse._flee_timer = 5.0
                    ui._hb_horse = None

        if not _any_ui_open() and not ui.cheat_open:
            player.handle_input(keys, mouse_btns, mouse_world, dt)
        else:
            player.vx = 0.0
        player.update(dt)
        player.update_aim(dt)
        for wx, wy, text, color in player.pending_harvest_floats:
            renderer.add_float_text(wx, wy, text, color)
        player.pending_harvest_floats.clear()
        world.update_loaded_chunks(player.x)
        if player.dead:
            drops = player.collect_all_items()
            world.spawn_drops(player.x + 10, player.y + 14, drops)

        for entity in world.entities:
            entity.update(dt)
        world._player_ref = player

        # Arrow projectile update + collision
        if world.arrows:
            from animals import HuntableAnimal
            import pygame as _pg
            for arrow in world.arrows:
                if arrow.dead:
                    continue
                arrow.update()
                arrow_rect = _pg.Rect(int(arrow.x), int(arrow.y), arrow.W, arrow.H)
                for entity in world.entities:
                    if isinstance(entity, HuntableAnimal) and not entity.dead:
                        if arrow_rect.colliderect(entity.rect):
                            drops = entity.on_arrow_hit(arrow.damage, poison=arrow.poison, barb=arrow.barb)
                            arrow.dead = True
                            if drops:
                                if arrow.extra_drops:
                                    drops = [(iid, cnt + 1) for iid, cnt in drops]
                                if getattr(player, "master_hunter", False):
                                    drops[0] = (drops[0][0], drops[0][1] + 1)
                                for item_id, count in drops:
                                    player._add_item(item_id, count)
                                animal_id = entity.animal_id
                                player.animals_hunted[animal_id] = player.animals_hunted.get(animal_id, 0) + 1
                                player.pending_notifications.append(
                                    ("Hunting", f"{animal_id.title()} hunted", None))
                                prev = player.hunt_trophies.get(animal_id, {})
                                new_record = False
                                for stat, val in entity.stats.items():
                                    if val > prev.get(stat, 0):
                                        player.hunt_trophies.setdefault(animal_id, {})[stat] = val
                                        if prev.get(stat, 0) > 0:
                                            new_record = True
                                if new_record:
                                    player.pending_notifications.append(
                                        ("Hunting", f"New record! {animal_id.replace('_', ' ').title()}", None))
                            break
            world.arrows = [a for a in world.arrows if not a.dead]

        for bird in world.birds:
            bird.update(dt)
        for ins in world.insects:
            ins.update(dt)
        _reptile_discover = _update_reptiles(world.reptiles, player, dt, BLOCK_SIZE)
        if _reptile_discover:
            _sp, _biome = _reptile_discover
            _existing = player.reptiles_observed.get(_sp)
            if _existing is None:
                player.reptiles_observed[_sp] = {"count": 1, "biome": _biome}
            else:
                _existing["count"] += 1
            player.discovered_reptile_types.add(_sp)
            from reptiles import ALL_REPTILE_SPECIES as _ALL_REPT
            _rept_cls = next((c for c in _ALL_REPT if c.SPECIES == _sp), None)
            _rarity = _rept_cls.RARITY if _rept_cls else "common"
            player.pending_notifications.append(
                ("Reptile", _sp.replace("_", " ").title(), _rarity))
        for lf in world.live_fish:
            lf.update(dt)
        world.live_fish = [lf for lf in world.live_fish if not lf.dead]

        # Spear projectile update + collision with live fish
        if world.spears:
            import pygame as _pg
            for spear in world.spears:
                if spear.dead:
                    continue
                spear.update()
                spear_rect = _pg.Rect(int(spear.x), int(spear.y), spear.W, spear.H)
                for lf in world.live_fish:
                    if lf.dead:
                        continue
                    if spear_rect.colliderect(lf.rect):
                        from fish import FishGenerator
                        if not hasattr(world, "_speared_fish_gen"):
                            world._speared_fish_gen = FishGenerator(world.seed)
                        from constants import BLOCK_SIZE as _LF_BS
                        bx_f = int(lf.x // _LF_BS)
                        by_f = int(lf.y // _LF_BS)
                        caught = world._speared_fish_gen.generate(
                            bx_f, by_f, lf.biome,
                            ocean_zone=lf.ocean_zone,
                        )
                        # Override species with the entity's species so the spear
                        # actually catches the fish you aimed at.
                        caught.species = lf.species
                        caught.rarity = lf.rarity
                        player.fish_caught.append(caught)
                        player.discovered_fish_species.add(lf.species)
                        player._add_item("fish")
                        prev = player.fish_bests.get(caught.species)
                        if prev is None or caught.weight_kg > prev["weight_kg"]:
                            player.fish_bests[caught.species] = {"weight_kg": caught.weight_kg, "length_cm": caught.length_cm}
                        player.pending_notifications.append(
                            ("Speared", lf.species.replace("_", " ").title(), lf.rarity))
                        lf.dead = True
                        spear.dead = True
                        break
            world.spears = [s for s in world.spears if not s.dead]
        # Bird observation mini-game tick
        if ui._bird_obs_active and ui._bird_obs_bird is not None:
            bird = ui._bird_obs_bird
            _bino_held = player.hotbar[player.selected_slot] == "binoculars"
            player_moving = abs(player.vx) > 0.5
            bird_escaped = bird.state in ("flying", "taking_off", "fleeing") and not _bino_held
            if bird_escaped:
                if not ui._bird_obs_failed:
                    ui._bird_obs_failed = True
                    ui._bird_obs_fail_timer = 1.5
                    ui._bird_obs_timer = 0.0
            elif not player_moving:
                ui._bird_obs_timer += dt
            if ui._bird_obs_timer >= 2.0:
                sp = bird.SPECIES
                biome = world.biodome_at(int(bird.x // BLOCK_SIZE))
                player.birds_observed.setdefault(sp, {"count": 0, "biome": biome})
                player.birds_observed[sp]["count"] += 1
                player.discovered_bird_types.add(sp)
                player.pending_notifications.append(
                    ("Bird", sp.replace("_", " ").title(), bird.RARITY))
                bird.spook()
                ui._bird_obs_active = False
                ui._bird_obs_bird = None
        if ui._bird_obs_failed:
            ui._bird_obs_fail_timer -= dt
            if ui._bird_obs_fail_timer <= 0:
                ui._bird_obs_active = False
                ui._bird_obs_failed = False
                ui._bird_obs_bird = None
        for car in world.elevator_cars:
            car.update(dt, world, player)
        for cart in world.minecarts:
            cart.update(dt, world)
        for boat in world.boats:
            boat.update(dt, world)
        for automation in world.automations:
            automation.update(dt, world)
        for farm_bot in world.farm_bots:
            farm_bot.update(dt, world)
        for bh in world.backhoes:
            if player.mounted_machine is not bh:
                bh.apply_gravity(world)
        world.update_time(dt)
        world.update_water(dt, player)
        world.update_flood_erosion(dt)
        world.update_soil(dt)
        world.update_compost_bins(dt)
        world.update_chicken_coops(dt)
        world.update_grass_regrowth(dt)
        world.update_trade_blocks(dt, player)
        world.update_tea_house_visitors(dt, player)
        import logic as _ltm
        _ltm.logic_tick(world, dt, player)
        import pipes as _pipes
        _pipes.pipe_tick(world, dt)
        import factory as _factory_mod
        _factory_mod.factory_tick(world, dt)
        world.update_irrigation(dt)
        world.update_saplings(dt)
        world.update_crops(dt)
        world.tick_hives(dt)
        world.update_fruit_trees(dt)
        world.update_leaves(dt, player)
        world.update_dropped_items(dt, player)
        world.update_clouds(player.x, dt)

        autosave_timer += dt
        if autosave_timer >= AUTOSAVE_INTERVAL:
            autosave_timer = 0.0
            print("[Autosave] Saving game...")
            _save_and_notify(world, player, research)

        renderer.update_camera(player, world)

        renderer.draw_world(world, player)
        renderer.draw_player(player)
        renderer.draw_entities(world.entities)
        renderer.draw_tea_house_visitors(world.tea_house_visitors)
        renderer.draw_arrows(world.arrows)
        renderer.draw_nests(world.nests)
        renderer.draw_birds(world.birds)
        renderer.draw_insects(world.insects)
        renderer.draw_reptiles(world.reptiles)
        renderer.draw_live_fish(world.live_fish)
        renderer.draw_spears(world.spears)
        renderer.draw_aim_preview(player, mouse_scr_pos)
        renderer.draw_automations(world.automations)
        renderer.draw_farm_bots(world.farm_bots)
        renderer.draw_backhoes(world.backhoes, player)
        renderer.draw_elevator_cars(world.elevator_cars, player)
        renderer.draw_minecarts(world.minecarts, player)
        renderer.draw_boats(world.boats, player, world)
        renderer.draw_dropped_items(world.dropped_items)
        renderer.draw_farm_sense(player, world)
        renderer.draw_logic_help(player, world)
        renderer.draw_mining_indicator(player)
        renderer.draw_place_indicator(player)
        renderer.draw_water_overlay(player)
        renderer.draw_heat_shimmer(world, dt)
        renderer.draw_rain(world)
        renderer.draw_rain_particles(world, dt)
        renderer.draw_snow_particles(world, dt)
        renderer.draw_dust_particles(world, dt)
        renderer.draw_wind_particles(world, dt)
        renderer.draw_embers(world, dt)
        renderer.draw_biome_overlay(world, dt)
        renderer.tick_float_texts(dt)
        renderer.draw_float_texts()
        renderer.draw_lighting(player, world, player.get_depth(), world.time_of_day)
        ui.draw(player, research, dt)
        renderer.draw_wire_hud(world)
        renderer.draw_pipe_hud(world)
        # Drain town tier-up toasts
        if hasattr(world, '_town_toasts') and world._town_toasts:
            for msg in world._town_toasts:
                player.pending_notifications.append(("Town", msg, None))
            world._town_toasts.clear()
        # Drain city settler arrival toasts
        if hasattr(world, '_city_toasts') and world._city_toasts:
            for msg in world._city_toasts:
                player.pending_notifications.append(("City", msg, None))
            world._city_toasts.clear()
        # Rivalry incident tick
        import npc_dynasty as _dyn_mod
        _dyn_mod.tick_rivalry_incidents(world, player, world.day_count)
        if ui._bird_obs_active:
            ui._draw_bird_observation_overlay(player)
        ui.draw_fishing_overlay(player, dt)
        renderer.draw_minimap(world, player, dt)

        if dt > 0:
            _fps_smooth += (1.0 / dt - _fps_smooth) * 0.1
        _fps_int = int(_fps_smooth)
        if _fps_int != _fps_last:
            fps_surf = _fps_font.render(f"FPS: {_fps_int}", True, (255, 255, 255))
            _fps_last = _fps_int
        screen.blit(fps_surf, (8, SCREEN_H - fps_surf.get_height() - 8))

        if settings.get("debug", False):
            _cur_biome = world.biodome_at(int(player.x // BLOCK_SIZE))
            if _cur_biome != _biome_last:
                _biome_surf = _fps_font.render(f"Biome: {_cur_biome}", True, (255, 255, 255))
                _biome_last = _cur_biome
            if _biome_surf:
                screen.blit(_biome_surf, (8, SCREEN_H - fps_surf.get_height() - _biome_surf.get_height() - 12))

        pygame.display.flip()

    print("Auto-saving...")
    save_mgr.save(world, player, research)  # on exit: skip notifications, just save
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
