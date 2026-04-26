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
from blocks import GEM_CUTTER_BLOCK, ROASTER_BLOCK, GRAPE_PRESS_BLOCK, FERMENTATION_BLOCK, COMPOST_BIN_BLOCK, STILL_BLOCK, STABLE_BLOCK, KENNEL_BLOCK, OXIDATION_STATION_BLOCK, SPINNING_WHEEL_BLOCK, LOOM_BLOCK, DAIRY_VAT_BLOCK, AGING_CAVE_BLOCK, FLETCHING_TABLE_BLOCK, ELEVATOR_STOP_BLOCK, WILDFLOWER_DISPLAY_BLOCK, WINE_CELLAR_BLOCK, BARREL_ROOM_BLOCK, TRADE_BLOCK
from elevators import ElevatorCar
from minecarts import Minecart

SETTINGS_PATH = Path(__file__).parent / "settings.json"


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
    flags = pygame.FULLSCREEN if settings.get("fullscreen", True) else 0
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
    """Returns ('new'|'load', screen). Blocks until the player clicks a button."""
    W, H = screen.get_size()
    clock = pygame.time.Clock()

    BLACK      = (0,   0,   0)
    BLUE_DARK  = (10,  50, 180)
    BLUE_MID   = (25,  90, 220)
    BLUE_LIGHT = (55, 130, 255)
    BLUE_SHINE = (90, 160, 255)
    WHITE      = (255, 255, 255)
    GRAY       = (120, 120, 140)
    BTN_HOVER  = (40, 100, 240)
    BTN_NORMAL = (20,  60, 160)
    BTN_DIM    = (30,  30,  60)

    try:
        font_title = pygame.font.SysFont("Arial Black", 96, bold=True)
        font_btn   = pygame.font.SysFont("Arial Black", 38, bold=True)
    except Exception:
        font_title = pygame.font.SysFont(None, 110, bold=True)
        font_btn   = pygame.font.SysFont(None, 44, bold=True)

    title_txt = font_title.render("Collector", True, WHITE)

    # Title oval
    oval_w, oval_h = 480, 180
    ox = W // 2 - oval_w // 2
    oy = H // 4 - oval_h // 2
    gradient_steps = [
        (0,   0,   oval_w,     oval_h,     BLUE_DARK),
        (8,   5,   oval_w-16,  oval_h-10,  BLUE_MID),
        (20,  10,  oval_w-40,  oval_h-20,  BLUE_MID),
        (45,  22,  oval_w-90,  oval_h-44,  BLUE_LIGHT),
        (75,  36,  oval_w-150, oval_h-72,  BLUE_SHINE),
    ]

    # Button layout
    btn_w, btn_h = 280, 62
    btn_gap = 24
    btn_x = W // 2 - btn_w // 2
    btn_new_y = H // 2 + 20
    btn_load_y = btn_new_y + btn_h + btn_gap
    btn_settings_y = btn_load_y + btn_h + btn_gap

    rect_new      = pygame.Rect(btn_x, btn_new_y,      btn_w, btn_h)
    rect_load     = pygame.Rect(btn_x, btn_load_y,     btn_w, btn_h)
    rect_settings = pygame.Rect(btn_x, btn_settings_y, btn_w, btn_h)

    def draw_button(surf, rect, label, hovered, enabled):
        if not enabled:
            col = BTN_DIM
            text_col = GRAY
        elif hovered:
            col = BTN_HOVER
            text_col = WHITE
        else:
            col = BTN_NORMAL
            text_col = WHITE
        pygame.draw.rect(surf, col, rect, border_radius=10)
        pygame.draw.rect(surf, BLUE_LIGHT if (hovered and enabled) else BLUE_DARK, rect, 2, border_radius=10)
        lbl = font_btn.render(label, True, text_col)
        lbl_rect = lbl.get_rect(center=rect.center)
        surf.blit(lbl, lbl_rect)

    while True:
        mx, my = pygame.mouse.get_pos()
        hover_new      = rect_new.collidepoint(mx, my)
        hover_load     = rect_load.collidepoint(mx, my) and has_save
        hover_settings = rect_settings.collidepoint(mx, my)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if rect_new.collidepoint(mx, my):
                    return "new", screen
                if has_save and rect_load.collidepoint(mx, my):
                    return "load", screen
                if rect_settings.collidepoint(mx, my):
                    screen, settings = _show_settings_screen(screen, settings)
                    W, H = screen.get_size()

        screen.fill(BLACK)

        # Draw title oval
        for dx, dy, ew, eh, col in gradient_steps:
            if ew > 0 and eh > 0:
                pygame.draw.ellipse(screen, col, (ox + dx, oy + dy, ew, eh))
        pygame.draw.ellipse(screen, (0, 30, 120), (ox, oy, oval_w, oval_h), 3)
        tr = title_txt.get_rect(center=(W // 2, oy + oval_h // 2))
        screen.blit(title_txt, tr)

        draw_button(screen, rect_new,      "New Game",  hover_new,      True)
        draw_button(screen, rect_load,     "Load Game", hover_load,     has_save)
        draw_button(screen, rect_settings, "Settings",  hover_settings, True)

        pygame.display.flip()
        clock.tick(60)


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

    _show_splash(screen)
    t0 = _t("splash", t0)

    save_mgr = SaveManager()
    t0 = _t("SaveManager", t0)

    choice, screen = _show_main_menu(screen, save_mgr.has_save(), settings)
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

    if choice == "load":
        def _do_load():
            global t0
            t0 = time.perf_counter()
            data = save_mgr.load()
            t0 = _t("  save_mgr.load", t0)
            w = World(seed=data["seed"], preloaded=data,
                      save_mgr=save_mgr, player_x=data["player"]["x"])
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
            return w, p, data["research"]
        world, player, research_data = _run_with_loading_screen(screen, "Loading", _do_load)
        research.apply_save(research_data)
        research.apply_bonuses(player, world)
        t0 = _t("research.apply_save", t0)
    else:
        seed = random.randint(0, 2**31 - 1)
        def _do_gen():
            global t0
            t0 = time.perf_counter()
            save_mgr.new_game()
            w = World(seed=seed, save_mgr=save_mgr)
            t0 = _t("  World(new)", t0)
            p = Player(w)
            t0 = _t("  Player", t0)
            return w, p
        world, player = _run_with_loading_screen(screen, "Generating World", _do_gen)
        if settings.get("debug", False):
            for node in research.nodes.values():
                node.apply(player, world)
            research.apply_bonuses(player, world)

    if settings.get("debug", False):
        player.no_hunger = True

    t0 = _t("total after choice", t0)

    world._player_ref = player
    ui.world_ref = world

    renderer.cam_x = player.x - SCREEN_W // 2
    renderer.cam_y = player.y - SCREEN_H // 2

    def _close_all_ui():
        ui.pause_open = False
        ui.help_open = False
        ui.research_open = ui.inventory_open = ui.crafting_open = False
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
        ui.wildflower_display_open = False
        ui.active_display_pos = None
        ui.wardrobe_open = False
        ui._jw_phase = "idle"
        ui._jw_drag_uid = None
        ui._sculpt_phase = "idle"
        ui.town_menu_open = False
        ui.active_town = None
        ui.trade_block_open = False
        ui.active_trade_pos = None

    def _any_ui_open():
        return any([ui.pause_open, ui.help_open, ui.research_open, ui.inventory_open, ui.crafting_open,
                    ui.collection_open, ui.refinery_open, ui.npc_open,
                    ui.automation_open, ui.farm_bot_open, ui.chest_open,
                    ui.backhoe_open, ui.breeding_open, ui.garden_open, ui.wildflower_display_open,
                    ui.horse_breeding_open, ui._hb_active, ui.wardrobe_open,
                    ui.town_menu_open, ui.reputation_screen_open, ui.trade_block_open,
                    ui.dog_view_open, ui.dog_breeding_open])

    def _find_nearby_npc(world, player):
        from cities import NPC
        for entity in world.entities:
            if isinstance(entity, NPC) and entity.in_range(player):
                if getattr(entity, 'is_ambient', False):
                    continue
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

                # Jewelry Workbench: text input for name phase
                if ui.refinery_open and ui._jw_phase == "name_confirm":
                    ui.handle_jewelry_keydown(event.key, getattr(event, "unicode", ""), player)

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

                # Wardrobe toggle (T = Textiles/Tailoring)
                if event.key == pygame.K_t:
                    if ui.wardrobe_open:
                        ui.wardrobe_open = False
                    elif not _any_ui_open():
                        ui.wardrobe_open = True
                if event.key == pygame.K_ESCAPE and ui.wardrobe_open:
                    ui.wardrobe_open = False

                if event.key == pygame.K_ESCAPE:
                    if player.fishing_state in ("casting", "biting"):
                        player.fishing_state = None
                        player._fishing_biome = None
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

                if event.key == pygame.K_i:
                    ui.inventory_open = not ui.inventory_open
                    ui.research_open = ui.crafting_open = False
                    ui.equipment_crafting_open = ui.collection_open = ui.refinery_open = False

                if event.key == pygame.K_c:
                    ui.crafting_open = not ui.crafting_open
                    ui.research_open = ui.inventory_open = False
                    ui.equipment_crafting_open = ui.collection_open = ui.refinery_open = False

                if event.key == pygame.K_g:
                    ui.collection_open = not ui.collection_open
                    ui.research_open = ui.inventory_open = ui.crafting_open = False
                    ui.equipment_crafting_open = ui.refinery_open = ui.breeding_open = False

                if event.key == pygame.K_b:
                    ui.breeding_open = not ui.breeding_open
                    ui.research_open = ui.inventory_open = ui.crafting_open = False
                    ui.equipment_crafting_open = ui.collection_open = ui.refinery_open = False

                if event.key == pygame.K_k:
                    ui.reputation_screen_open = not ui.reputation_screen_open
                    if ui.reputation_screen_open:
                        ui.research_open = ui.inventory_open = ui.crafting_open = False
                        ui.collection_open = ui.refinery_open = ui.breeding_open = False

                if event.key == pygame.K_h:
                    ui.help_open = not ui.help_open
                    if ui.help_open:
                        ui.research_open = ui.inventory_open = ui.crafting_open = False
                        ui.collection_open = ui.refinery_open = ui.breeding_open = False

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
                    elif nearby_npc is not None:
                        if ui.npc_open and ui.active_npc is nearby_npc:
                            ui.npc_open = False
                            ui.active_npc = None
                        else:
                            _close_all_ui()
                            ui.npc_open = True
                            ui.active_npc = nearby_npc
                    elif nearby_flag is not None:
                        from towns import get_town_for_block
                        town = get_town_for_block(world, *nearby_flag)
                        if town is not None:
                            if ui.town_menu_open and ui.active_town is town:
                                ui.close_town_menu()
                            else:
                                _close_all_ui()
                                ui.open_town_menu(town, player)
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
                        cart = next((c for c in world.minecarts if c.track_by == by), None)
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
                        if nearby_chest is not None:
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
                            equip = player.get_nearby_equipment()
                            if equip is not None:
                                ui.refinery_open = True
                                ui.refinery_block_id = equip
                                ui.research_open = ui.inventory_open = ui.crafting_open = False
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
                                else:
                                    ui.active_compost_bin_pos = None
                            else:
                                ui.refinery_open = False

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

            if event.type == pygame.MOUSEWHEEL:
                if not player.dead and not ui.cheat_open:
                    if ui.reputation_screen_open:
                        ui.handle_reputation_screen_scroll(-event.y * 20)
                    elif ui.help_open:
                        ui._help_scroll = max(0, min(ui._help_max_scroll, ui._help_scroll - event.y * 20))
                    elif ui.wildflower_display_open:
                        max_s = max(0, len(player.wildflowers) - 6)
                        ui._display_scroll = max(0, min(max_s, getattr(ui, '_display_scroll', 0) - event.y))
                    elif ui.research_open or ui.inventory_open or ui.crafting_open or ui.collection_open or ui.refinery_open or ui.chest_open or ui.breeding_open or ui.garden_open or ui.horse_breeding_open or ui.dog_breeding_open or ui.dog_view_open:
                        ui.handle_scroll(event.y)
                    elif not _any_ui_open():
                        player.selected_slot = (player.selected_slot - event.y) % 8

            if event.type == pygame.MOUSEMOTION:
                if ui.inventory_open:
                    ui.handle_inventory_drag(event.pos)
                if ui._jw_drag_uid is not None:
                    ui._jw_drag_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                if ui.inventory_open:
                    ui.handle_inventory_release(event.pos, player)
                if ui._jw_drag_uid is not None:
                    ui._handle_jewelry_drop(event.pos, player)
                # End sculpt drag on any mouse release
                if getattr(ui, '_sculpt_drag_mode', None) is not None:
                    ui._sculpt_drag_mode = None
                # End pottery wheel drag
                if getattr(ui, '_wheel_drag_row', None) is not None:
                    ui._wheel_drag_row = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player.dead or ui.cheat_open:
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
                elif ui.npc_open:
                    ui.handle_npc_click(event.pos, player)
                elif ui.research_open:
                    ui.handle_research_click(event.pos, player, world, research)
                elif ui.inventory_open:
                    ui.handle_inventory_click(event.pos, player)
                elif ui.crafting_open:
                    ui.handle_crafting_click(event.pos, player, event.button, research)
                elif ui.collection_open:
                    ui.handle_collection_click(event.pos, player)
                elif ui.breeding_open:
                    ui.handle_breeding_click(event.pos, player)
                elif ui.refinery_open:
                    if ui.refinery_block_id == GEM_CUTTER_BLOCK:
                        ui.handle_gem_cutter_click(event.pos, player)
                    else:
                        ui.handle_refinery_click(event.pos, player)
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
                elif ui.wardrobe_open:
                    ui.handle_wardrobe_click(event.pos, player)
                elif ui.trade_block_open:
                    ui.handle_trade_block_click(event.pos, player, world, event.button)
                elif ui.chest_open:
                    ui.handle_chest_click(event.pos, player, event.button)
                elif ui.garden_open:
                    ui.handle_garden_click(event.pos, player)
                elif ui.wildflower_display_open:
                    ui.handle_wildflower_display_click(event.pos, player)
                else:
                    # Check for bird clicks before falling through to hotbar/world
                    if event.button == 1 and not ui._bird_obs_active:
                        mx, my = event.pos
                        for bird in world.birds:
                            bsx = int(bird.x - renderer.cam_x)
                            bsy = int(bird.y - renderer.cam_y)
                            if pygame.Rect(bsx - 4, bsy - 4, bird.W + 8, bird.H + 8).collidepoint(mx, my):
                                ui.open_bird_observation(bird)
                                break
                    # Check for insect clicks (requires bug_net equipped)
                    held = player.hotbar[player.selected_slot]
                    if (event.button == 1 and not ui._insect_obs_active
                            and held == "bug_net"):
                        mx, my = event.pos
                        _night_a = renderer._sky_night_alpha(world.time_of_day)
                        for ins in world.insects:
                            if ins.spooked:
                                continue
                            if ins.NIGHT_ONLY and _night_a < 30:
                                continue
                            isx = int(ins.x - renderer.cam_x)
                            isy = int(ins.y - renderer.cam_y)
                            if pygame.Rect(isx - 4, isy - 4, ins.W + 8, ins.H + 8).collidepoint(mx, my):
                                ui.open_insect_observation(ins)
                                break
                    # Bow firing — left-click with bow equipped fires an arrow
                    if event.button == 1 and not player.dead:
                        player.fire_arrow()
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
        # Oxidation Station: poll SPACE to slow oxidation
        if ui.refinery_open and ui.refinery_block_id == OXIDATION_STATION_BLOCK:
            ui.handle_oxidation_keys(keys, dt, player)
        # Spinning Wheel: poll SPACE for fiber tension
        if ui.refinery_open and ui.refinery_block_id == SPINNING_WHEEL_BLOCK:
            ui.handle_spinning_wheel_keys(keys, dt, player)

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

        if ui.pause_open:
            renderer.draw_world(world, player)
            renderer.draw_player(player)
            renderer.draw_dropped_items(world.dropped_items)
            renderer.draw_entities(world.entities)
            renderer.draw_arrows(world.arrows)
            renderer.draw_nests(world.nests)
            renderer.draw_birds(world.birds)
            renderer.draw_insects(world.insects, world.time_of_day)
            renderer.draw_automations(world.automations)
            renderer.draw_farm_bots(world.farm_bots)
            renderer.draw_backhoes(world.backhoes, player)
            renderer.draw_elevator_cars(world.elevator_cars)
            renderer.draw_minecarts(world.minecarts)
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

        # Horse mounted physics
        if player.mounted_horse is not None and not _any_ui_open() and not ui.cheat_open:
            horse = player.mounted_horse
            from constants import GRAVITY, MAX_FALL
            horse.vy = min(horse.vy + GRAVITY, MAX_FALL)
            horse._move_x(horse.vx)
            horse._move_y(horse.vy)
            player.on_ground = horse.on_ground

        # Pending horse break minigame trigger
        if getattr(player, '_pending_horse_break', None) is not None:
            ui.open_horse_breaking(player._pending_horse_break)
            player._pending_horse_break = None

        # Pending dog view panel trigger
        if getattr(player, '_pending_dog_view', None) is not None:
            ui.open_dog_view(player._pending_dog_view)
            player._pending_dog_view = None

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
        player.update(dt)
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
        # Prune off-screen spooked insects
        world.insects = [i for i in world.insects
                         if not i.spooked or abs(i.x - player.x) < 2000]
        # Bird observation mini-game tick
        if ui._bird_obs_active and ui._bird_obs_bird is not None:
            bird = ui._bird_obs_bird
            player_moving = abs(player.vx) > 0.5
            if bird.state in ("flying", "taking_off"):
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
        # Insect catch mini-game tick
        if ui._insect_obs_active and ui._insect_obs_insect is not None:
            ins = ui._insect_obs_insect
            player_moving = abs(player.vx) > 0.5
            if ins.spooked:
                if not ui._insect_obs_failed:
                    ui._insect_obs_failed = True
                    ui._insect_obs_fail_timer = 1.5
                    ui._insect_obs_timer = 0.0
            elif not player_moving:
                ui._insect_obs_timer += dt
            if ui._insect_obs_timer >= 1.5:
                sp = ins.SPECIES
                biome = world.biodome_at(int(ins.x // BLOCK_SIZE))
                player.insects_observed.setdefault(sp, {"count": 0, "biome": biome})
                player.insects_observed[sp]["count"] += 1
                player.discovered_insect_types.add(sp)
                player.pending_notifications.append(
                    ("Insect", sp.replace("_", " ").title(), ins.RARITY))
                ins.spook()
                ui._insect_obs_active = False
                ui._insect_obs_insect = None
        if ui._insect_obs_failed:
            ui._insect_obs_fail_timer -= dt
            if ui._insect_obs_fail_timer <= 0:
                ui._insect_obs_active = False
                ui._insect_obs_failed = False
                ui._insect_obs_insect = None
        for car in world.elevator_cars:
            car.update(dt, world, player)
        for cart in world.minecarts:
            cart.update(dt, world)
        for automation in world.automations:
            automation.update(dt, world)
        for farm_bot in world.farm_bots:
            farm_bot.update(dt, world)
        for bh in world.backhoes:
            if player.mounted_machine is not bh:
                bh.apply_gravity(world)
        world.update_time(dt)
        world.update_water(dt, player)
        world.update_soil(dt)
        world.update_compost_bins(dt)
        world.update_trade_blocks(dt, player)
        world.update_saplings(dt)
        world.update_crops(dt)
        world.update_leaves(dt, player)
        world.update_dropped_items(dt, player)

        autosave_timer += dt
        if autosave_timer >= AUTOSAVE_INTERVAL:
            autosave_timer = 0.0
            print("[Autosave] Saving game...")
            _save_and_notify(world, player, research)

        renderer.update_camera(player, world)

        renderer.draw_world(world, player)
        renderer.draw_player(player)
        renderer.draw_entities(world.entities)
        renderer.draw_arrows(world.arrows)
        renderer.draw_nests(world.nests)
        renderer.draw_birds(world.birds)
        renderer.draw_insects(world.insects)
        renderer.draw_automations(world.automations)
        renderer.draw_farm_bots(world.farm_bots)
        renderer.draw_backhoes(world.backhoes, player)
        renderer.draw_elevator_cars(world.elevator_cars, player)
        renderer.draw_minecarts(world.minecarts, player)
        renderer.draw_dropped_items(world.dropped_items)
        renderer.draw_farm_sense(player, world)
        renderer.draw_mining_indicator(player)
        renderer.draw_place_indicator(player)
        renderer.draw_water_overlay(player)
        renderer.draw_rain(world)
        renderer.tick_float_texts(dt)
        renderer.draw_float_texts()
        renderer.draw_lighting(player, world, player.get_depth(), world.time_of_day)
        ui.draw(player, research, dt)
        # Drain town tier-up toasts
        if hasattr(world, '_town_toasts') and world._town_toasts:
            for msg in world._town_toasts:
                player.pending_notifications.append(("Town", msg, None))
            world._town_toasts.clear()
        if ui._bird_obs_active:
            ui._draw_bird_observation_overlay(player)
        if ui._insect_obs_active:
            ui._draw_insect_observation_overlay(player)
        ui.draw_fishing_overlay(player, dt)
        renderer.draw_minimap(world, player, dt)

        if dt > 0:
            _fps_smooth += (1.0 / dt - _fps_smooth) * 0.1
        _fps_int = int(_fps_smooth)
        if _fps_int != _fps_last:
            fps_surf = _fps_font.render(f"FPS: {_fps_int}", True, (255, 255, 255))
            _fps_last = _fps_int
        screen.blit(fps_surf, (8, SCREEN_H - fps_surf.get_height() - 8))

        pygame.display.flip()

    print("Auto-saving...")
    save_mgr.save(world, player, research)  # on exit: skip notifications, just save
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
