import pygame
import soil as _soil

from blocks import (BLOCKS, AIR, STONE, WATER, GRAVEL, SNOW, SAND,
                    YOUNG_CROP_BLOCKS, MATURE_CROP_BLOCKS, TILLED_SOIL,
                    ALL_LOGS, ALL_LEAVES)
from constants import BLOCK_SIZE, SCREEN_W, SCREEN_H, CHUNK_W, WORLD_H

_MM_W      = 180
_MM_H      = 120
_MM_MARGIN = 8


# ------------------------------------------------------------------
# E1 — Indicators
# ------------------------------------------------------------------

def draw_mining_indicator(screen, cam_x, cam_y, mine_overlay, player):
    if not player.mining_block or player.mine_progress <= 0:
        return
    bx, by = player.mining_block
    sx = bx * BLOCK_SIZE - int(cam_x)
    sy = by * BLOCK_SIZE - int(cam_y)
    alpha = int(200 * player.mine_progress)
    mine_overlay.fill((0, 0, 0, alpha))
    screen.blit(mine_overlay, (sx, sy))
    pygame.draw.rect(screen, (255, 255, 255), (sx, sy, BLOCK_SIZE, BLOCK_SIZE), 2)


def draw_place_indicator(renderer, player):
    if not player.place_target:
        return
    _, block_id = player._selected_place_block()
    if block_id is None:
        return
    bx, by = player.place_target
    sx = bx * BLOCK_SIZE - int(renderer.cam_x)
    sy = by * BLOCK_SIZE - int(renderer.cam_y)
    color = BLOCKS.get(block_id, {}).get("color")
    bg_mode = getattr(player, 'bg_place_mode', False)
    if bg_mode:
        ghost_color = (max(0, color[0] - 30), max(0, color[1] - 10), min(255, color[2] + 60)) if color else (60, 80, 180)
        key = ("bg", ghost_color)
        if renderer._ghost_color_key != key:
            renderer._ghost_color_key = key
            renderer._ghost_surf.fill((0, 0, 0, 0))
            renderer._ghost_surf.fill((*ghost_color, 100))
        renderer.screen.blit(renderer._ghost_surf, (sx, sy))
        pygame.draw.rect(renderer.screen, (100, 160, 255), (sx, sy, BLOCK_SIZE, BLOCK_SIZE), 2)
    else:
        if color:
            if renderer._ghost_color_key != color:
                renderer._ghost_color_key = color
                renderer._ghost_surf.fill((0, 0, 0, 0))
                renderer._ghost_surf.fill((*color, 120))
            renderer.screen.blit(renderer._ghost_surf, (sx, sy))
        pygame.draw.rect(renderer.screen, (255, 255, 255), (sx, sy, BLOCK_SIZE, BLOCK_SIZE), 2)


# ------------------------------------------------------------------
# E2 — Floating texts & dropped items
# ------------------------------------------------------------------

def add_float_text(floating_texts, world_x, world_y, text, color):
    floating_texts.append({
        "x": float(world_x), "y": float(world_y),
        "text": text, "color": color, "life": 2.0, "vy": -40.0,
    })


def tick_float_texts(floating_texts, dt):
    for ft in floating_texts:
        ft["y"] += ft["vy"] * dt
        ft["life"] -= dt
    return [ft for ft in floating_texts if ft["life"] > 0]


def draw_float_texts(screen, cam_x, cam_y, floating_texts, font):
    for ft in floating_texts:
        sx = int(ft["x"] - cam_x)
        sy = int(ft["y"] - cam_y)
        alpha = min(255, int(255 * ft["life"]))
        surf = font.render(ft["text"], True, ft["color"])
        surf.set_alpha(alpha)
        screen.blit(surf, (sx - surf.get_width() // 2, sy))


def draw_dropped_items(screen, cam_x, cam_y, dropped_items, font):
    from items import ITEMS
    for item in dropped_items:
        sx = int(item.x - cam_x)
        sy = int(item.y - cam_y)
        if not (-20 <= sx <= SCREEN_W + 20 and -20 <= sy <= SCREEN_H + 20):
            continue
        col = ITEMS.get(item.item_id, {}).get("color", (200, 200, 200))
        pygame.draw.rect(screen, col, (sx - 8, sy - 8, 16, 16))
        pygame.draw.rect(screen, (255, 255, 255), (sx - 8, sy - 8, 16, 16), 1)
        if item.count > 1:
            txt = font.render(str(item.count), True, (255, 255, 255))
            screen.blit(txt, (sx - txt.get_width() // 2, sy - txt.get_height() // 2))


# ------------------------------------------------------------------
# E3 — Weather & world overlays
# ------------------------------------------------------------------

def draw_farm_sense(screen, cam_x, cam_y, player, world, font):
    tb = player.target_block
    if tb is None:
        return
    bx, by = tb
    block_id = world.get_block(bx, by)
    sx = bx * BLOCK_SIZE - int(cam_x)
    sy = by * BLOCK_SIZE - int(cam_y)
    if block_id in MATURE_CROP_BLOCKS:
        pygame.draw.rect(screen, (255, 210, 0), (sx - 1, sy - 1, BLOCK_SIZE + 2, BLOCK_SIZE + 2), 3)
        label = font.render("Ready!", True, (255, 210, 0))
        screen.blit(label, (sx, sy - label.get_height() - 2))
        return
    if block_id in YOUNG_CROP_BLOCKS:
        pygame.draw.rect(screen, (140, 140, 140), (sx - 1, sy - 1, BLOCK_SIZE + 2, BLOCK_SIZE + 2), 2)
        moisture  = world._soil_moisture.get((bx, by + 1), 0)
        fertility = world._soil_fertility.get((bx, by + 1), world.max_fertility)
        progress  = world._crop_progress.get((bx, by), 0)
        text = f"M:{moisture}/{_soil.MAX_MOISTURE}  F:{fertility}/{world.max_fertility}  {progress}%"
        label = font.render(text, True, (210, 210, 120))
        screen.blit(label, (sx, sy - label.get_height() - 2))
        return
    if block_id == TILLED_SOIL:
        moisture  = world._soil_moisture.get((bx, by), 0)
        fertility = world._soil_fertility.get((bx, by), world.max_fertility)
        m_color = (120, 180, 220) if moisture >= 4 else (200, 170, 110)
        pygame.draw.rect(screen, m_color, (sx - 1, sy - 1, BLOCK_SIZE + 2, BLOCK_SIZE + 2), 2)
        label = font.render(
            f"M:{moisture}/{_soil.MAX_MOISTURE}  F:{fertility}/{world.max_fertility}",
            True, m_color)
        screen.blit(label, (sx, sy - label.get_height() - 2))


_LOGIC_HELP = None

def _build_logic_help():
    from blocks import (
        SWITCH_BLOCK_OFF, SWITCH_BLOCK_ON,
        LATCH_BLOCK_OFF, LATCH_BLOCK_ON,
        PRESSURE_PLATE_OFF, PRESSURE_PLATE_ON,
        DAY_SENSOR_BLOCK, NIGHT_SENSOR_BLOCK,
        WATER_SENSOR_BLOCK, CROP_SENSOR_BLOCK,
        AND_GATE_BLOCK, OR_GATE_BLOCK, NOT_GATE_BLOCK,
        REPEATER_BLOCK, PULSE_GEN_BLOCK,
        RS_LATCH_Q0, RS_LATCH_Q1,
        T_FLIPFLOP_BLOCK, COUNTER_BLOCK,
        COMPARATOR_BLOCK, OBSERVER_BLOCK, SEQUENCER_BLOCK,
        DAM_BLOCK_CLOSED, DAM_BLOCK_OPEN,
        PUMP_BLOCK_OFF, PUMP_BLOCK_ON,
        IRON_GATE_BLOCK_CLOSED, IRON_GATE_BLOCK_OPEN,
        POWERED_LANTERN_OFF, POWERED_LANTERN_ON,
        ALARM_BELL_OFF, ALARM_BELL_ON,
        DEPOSIT_TRIGGER_BLOCK,
    )
    return {
        SWITCH_BLOCK_OFF:          ("Switch", "E: toggle on/off"),
        SWITCH_BLOCK_ON:           ("Switch", "E: toggle on/off"),
        LATCH_BLOCK_OFF:           ("Toggle Latch", "E: toggle on/off"),
        LATCH_BLOCK_ON:            ("Toggle Latch", "E: toggle on/off"),
        PRESSURE_PLATE_OFF:        ("Pressure Plate", "Activates when stood on"),
        PRESSURE_PLATE_ON:         ("Pressure Plate", "Activates when stood on"),
        DAY_SENSOR_BLOCK:          ("Day Sensor", "ON during daytime  |  Right-click: switch to Night"),
        NIGHT_SENSOR_BLOCK:        ("Night Sensor", "ON during nighttime  |  Right-click: switch to Day"),
        WATER_SENSOR_BLOCK:        ("Water Sensor", "ON when adjacent tile contains water"),
        CROP_SENSOR_BLOCK:         ("Crop Sensor", "ON when crop directly below is mature"),
        AND_GATE_BLOCK:            ("AND Gate", "ON when ALL inputs powered  |  Right-click: rotate"),
        OR_GATE_BLOCK:             ("OR Gate", "ON when ANY input powered  |  Right-click: rotate"),
        NOT_GATE_BLOCK:            ("NOT Gate", "ON when input is OFF  |  Right-click: rotate"),
        REPEATER_BLOCK:            ("Repeater", "Delays signal  |  Right-click: cycle delay (0.25→0.5→1→2→4s)"),
        PULSE_GEN_BLOCK:           ("Pulse Generator", "Toggles on a timer  |  Right-click: cycle period"),
        RS_LATCH_Q0:               ("RS Latch (off)", "S sets ON, R resets OFF  |  Right-click: rotate"),
        RS_LATCH_Q1:               ("RS Latch (on)",  "S sets ON, R resets OFF  |  Right-click: rotate"),
        T_FLIPFLOP_BLOCK:          ("T-Flip-Flop", "Toggles on rising edge  |  Right-click: manual toggle"),
        COUNTER_BLOCK:             ("Counter", "Counts pulses; outputs when count ≥ threshold  |  Right-click: cycle threshold"),
        COMPARATOR_BLOCK:          ("Comparator", "ON when adjacent chest fill ≥ threshold  |  Right-click: cycle threshold"),
        OBSERVER_BLOCK:            ("Observer", "Pulses when watched block changes  |  Right-click: rotate"),
        SEQUENCER_BLOCK:           ("Sequencer", "Steps through 4 outputs on each pulse  |  Right-click: advance step"),
        DAM_BLOCK_CLOSED:          ("Dam", "Opens when powered by wire"),
        DAM_BLOCK_OPEN:            ("Dam (open)", "Opens when powered by wire"),
        PUMP_BLOCK_OFF:            ("Pump", "Pumps water when powered by wire"),
        PUMP_BLOCK_ON:             ("Pump (on)", "Pumps water when powered by wire"),
        IRON_GATE_BLOCK_CLOSED:    ("Iron Gate", "Opens when powered by wire"),
        IRON_GATE_BLOCK_OPEN:      ("Iron Gate (open)", "Opens when powered by wire"),
        POWERED_LANTERN_OFF:       ("Powered Lantern", "Lights up when powered by wire"),
        POWERED_LANTERN_ON:        ("Powered Lantern (on)", "Lights up when powered by wire"),
        ALARM_BELL_OFF:            ("Alarm Bell", "Rings when powered by wire"),
        ALARM_BELL_ON:             ("Alarm Bell (ringing)", "Rings when powered by wire"),
        DEPOSIT_TRIGGER_BLOCK:     ("Deposit Trigger", "Rising edge: nearby bots dump inventory into adjacent chest"),
    }


def draw_logic_help(screen, cam_x, cam_y, player, world, font):
    global _LOGIC_HELP
    if _LOGIC_HELP is None:
        _LOGIC_HELP = _build_logic_help()
    tb = player.target_block
    if tb is None:
        return
    bx, by = tb
    block_id = world.get_block(bx, by)
    entry = _LOGIC_HELP.get(block_id)
    if entry is None:
        return
    name, desc = entry
    gs = world.logic_state.get((bx, by), {})

    lines = [name]
    # Append live state detail where useful
    if block_id in _LOGIC_HELP:
        from blocks import (COUNTER_BLOCK, COMPARATOR_BLOCK,
                            REPEATER_BLOCK, PULSE_GEN_BLOCK, SEQUENCER_BLOCK)
        if block_id == COUNTER_BLOCK:
            count = gs.get("count", 0)
            threshold = gs.get("threshold", 4)
            lines.append(f"Count: {count} / {threshold}")
        elif block_id == COMPARATOR_BLOCK:
            fill = gs.get("fill_level", 0)
            threshold = gs.get("threshold", 4)
            lines.append(f"Fill: {fill} / {threshold}")
        elif block_id == REPEATER_BLOCK:
            lines.append(f"Delay: {gs.get('delay', 0.5)}s")
        elif block_id == PULSE_GEN_BLOCK:
            lines.append(f"Period: {gs.get('period', 2.0)}s")
        elif block_id == SEQUENCER_BLOCK:
            step_names = ["Right", "Down", "Left", "Up"]
            lines.append(f"Step: {step_names[gs.get('step', 0) % 4]}")
    lines.append(desc)

    sx = bx * BLOCK_SIZE - int(cam_x)
    sy = by * BLOCK_SIZE - int(cam_y)
    line_h = font.get_height() + 2
    box_w = max(font.size(l)[0] for l in lines) + 12
    box_h = line_h * len(lines) + 8
    bx_screen = max(2, min(SCREEN_W - box_w - 2, sx))
    by_screen = max(2, sy - box_h - 4)

    bg = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
    bg.fill((10, 10, 18, 200))
    screen.blit(bg, (bx_screen, by_screen))
    pygame.draw.rect(screen, (80, 80, 120), (bx_screen, by_screen, box_w, box_h), 1)

    for i, line in enumerate(lines):
        col = (200, 200, 255) if i == 0 else ((160, 210, 180) if i < len(lines) - 1 else (130, 130, 160))
        surf = font.render(line, True, col)
        screen.blit(surf, (bx_screen + 6, by_screen + 4 + i * line_h))


def draw_water_overlay(screen, water_overlay_surf, player):
    if player._head_in_water():
        screen.blit(water_overlay_surf, (0, 0))


def draw_rain(screen, cam_x, world):
    if not world._rain_active:
        return
    surf = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    # Grey atmospheric wash — desaturates the sky slightly
    surf.fill((72, 82, 100, 28))
    # Denser, more visible streaks
    streak_color = (160, 190, 230, 145)
    cx_off   = int(cam_x) % 12
    time_off = (pygame.time.get_ticks() // 22) % SCREEN_H
    for sx in range(-cx_off, SCREEN_W, 12):
        seed_val = (sx + int(cam_x) // 12) & 0xFFFF
        start_y  = (seed_val * 137 % SCREEN_H + time_off) % SCREEN_H
        length   = 10 + (seed_val * 53 % 14)
        pygame.draw.line(surf, streak_color, (sx, start_y), (sx - 2, start_y + length), 1)
    screen.blit(surf, (0, 0))


# ------------------------------------------------------------------
# E4 — Minimap
# ------------------------------------------------------------------

def build_mm_color_table():
    from blocks import (GRASS, DIRT, OBSIDIAN, BEDROCK, GATE_MID, GATE_DEEP, GATE_CORE,
                        HOUSE_WALL, HOUSE_ROOF,
                        HOUSE_WALL_STONE, HOUSE_ROOF_STONE,
                        HOUSE_WALL_BRICK, HOUSE_ROOF_BRICK,
                        HOUSE_WALL_DARK, HOUSE_ROOF_DARK,
                        RESTAURANT_WALL, RESTAURANT_AWNING,
                        POLISHED_GRANITE, POLISHED_MARBLE, SLATE_TILE,
                        TERRACOTTA_BLOCK, MOSSY_BRICK, CREAM_BRICK,
                        CHARCOAL_PLANK, WALNUT_PLANK, OAK_PANEL, BAMBOO_PANEL,
                        OBSIDIAN_TILE, COBBLESTONE, LAPIS_BRICK, BASALT_COLUMN,
                        LIMESTONE_BLOCK, COPPER_TILE, TEAK_PLANK,
                        DRIFTWOOD_PLANK, CEDAR_PANEL, JADE_PANEL,
                        ROSE_QUARTZ_BLOCK, GILDED_BRICK, AMETHYST_BLOCK,
                        AMBER_TILE, IVORY_BRICK, EBONY_PLANK,
                        MAHOGANY_PLANK, ASH_PLANK, FROSTED_GLASS, CRIMSON_BRICK,
                        TERRACOTTA_SHINGLE, THATCH_ROOF, VERDIGRIS_COPPER,
                        SILVER_PANEL, GOLD_LEAF_TRIM,
                        STAINED_GLASS_RED, STAINED_GLASS_BLUE, STAINED_GLASS_GREEN,
                        QUARTZ_PILLAR, ONYX_INLAY,
                        WHITE_PLASTER_WALL, CARVED_PLASTER, MUQARNAS_BLOCK,
                        MASHRABIYA, ZELLIGE_TILE, ARABESQUE_PANEL,
                        ADOBE_BRICK, SPANISH_ROOF_TILE, WROUGHT_IRON_GRILLE,
                        TALAVERA_TILE, SALTILLO_TILE,
                        COBALT_DOOR_CLOSED, COBALT_DOOR_OPEN,
                        CRIMSON_CEDAR_DOOR_CLOSED, CRIMSON_CEDAR_DOOR_OPEN,
                        TEAL_DOOR_CLOSED, TEAL_DOOR_OPEN,
                        SAFFRON_DOOR_CLOSED, SAFFRON_DOOR_OPEN,
                        STUDDED_OAK_DOOR_CLOSED, STUDDED_OAK_DOOR_OPEN,
                        VERMILION_DOOR_CLOSED, VERMILION_DOOR_OPEN,
                        SHOJI_DOOR_CLOSED, SHOJI_DOOR_OPEN,
                        GILDED_DOOR_CLOSED, GILDED_DOOR_OPEN,
                        BRONZE_DOOR_CLOSED, BRONZE_DOOR_OPEN,
                        SWAHILI_DOOR_CLOSED, SWAHILI_DOOR_OPEN,
                        SANDALWOOD_DOOR_CLOSED, SANDALWOOD_DOOR_OPEN,
                        STONE_SLAB_DOOR_CLOSED, STONE_SLAB_DOOR_OPEN,
                        HALF_TIMBER_WALL, ASHLAR_BLOCK, GOTHIC_TRACERY, FLUTED_COLUMN,
                        CORNICE_BLOCK, ROSE_WINDOW, HERRINGBONE_BRICK, BAROQUE_TRIM,
                        TUDOR_BEAM, VENETIAN_FLOOR, FLEMISH_BRICK, PILASTER,
                        DENTIL_TRIM, WATTLE_DAUB, NORDIC_PLANK, MANSARD_SLATE,
                        ROMAN_MOSAIC, SETT_STONE, ROMANESQUE_ARCH, DARK_SLATE_ROOF,
                        KEYSTONE, PLINTH_BLOCK, IRON_LANTERN, SANDSTONE_ASHLAR,
                        GARGOYLE_BLOCK, LIGHT_TRAP_BLOCK,
                        OGEE_ARCH, RUSTICATED_STONE, CHEVRON_STONE, TRIGLYPH_PANEL,
                        MARBLE_INLAY, BRICK_NOGGING, CRENELLATION, FAN_VAULT,
                        PORTCULLIS_BLOCK, ARROW_LOOP, MACHICOLATION, DRAWBRIDGE_PLANK,
                        ROUND_TOWER_WALL, CURTAIN_WALL, CORBEL_COURSE, TOWER_CAP,
                        GREAT_HALL_FLOOR, DUNGEON_WALL, CASTLE_FIREPLACE, HERALDIC_PANEL,
                        WALL_WALK_FLOOR, CASTLE_GATE_ARCH, DRAWBRIDGE_CHAIN, DUNGEON_GRATE,
                        MOAT_STONE, CHAPEL_STONE, MURDER_HOLE, GARDEROBE_CHUTE,
                        ACANTHUS_PANEL, PEBBLE_DASH, ENCAUSTIC_TILE, CHEQUERBOARD_MARBLE,
                        WROUGHT_IRON_BALUSTRADE, OPUS_INCERTUM, GROTESQUE_FRIEZE,
                        BARREL_VAULT, POINTED_ARCH, ENGLISH_BOND, RELIEF_PANEL,
                        DIAGONAL_TILE,
                        TAPESTRY_BLOCK, WOVEN_RUG, CELTIC_KNOTWORK, BYZANTINE_MOSAIC,
                        JAPANESE_SHOJI, OTTOMAN_TILE, LEADLIGHT_WINDOW, TUDOR_ROSE,
                        GREEK_KEY, VENETIAN_PLASTER, SCOTTISH_RUBBLE, ART_NOUVEAU_PANEL,
                        DUTCH_GABLE, STRIPED_ARCH, TIMBER_TRUSS, HEARTH_STONE,
                        LINEN_FOLD, PARQUET_FLOOR, COFFERED_CEILING, OPUS_SIGNINUM,
                        GLAZED_ROOF_TILE, LATTICE_SCREEN, MOON_GATE, PAINTED_BEAM,
                        DOUGONG, CERAMIC_PLANTER, STONE_LANTERN, LACQUER_PANEL,
                        PAPER_LANTERN, DRAGON_TILE, HAN_BRICK, PAVILION_FLOOR,
                        BAMBOO_SCREEN, CLOUD_MOTIF, COIN_TILE, BLUE_WHITE_TILE,
                        GARDEN_ROCK, STEPPED_WALL, PAGODA_EAVE, CINNABAR_WALL,
                        WHITEWASHED_WALL, MONASTERY_ROOF, MANI_STONE, PRAYER_FLAG_BLOCK,
                        MUGHAL_ARCH, PIETRA_DURA, EGYPTIAN_FRIEZE, SANDSTONE_COLUMN,
                        AZTEC_SUNSTONE, MAYA_RELIEF, VIKING_CARVING, RUNE_STONE,
                        PERSIAN_IWAN, KILIM_TILE, AFRICAN_MUD_BRICK, KENTE_PANEL,
                        WAT_FINIAL, KHMER_STONE, HANJI_SCREEN, DANCHEONG,
                        ART_DECO_PANEL, OBSIDIAN_CUT, OTTOMAN_ARCH, LOTUS_CAPITAL,
                        AZULEJO_TILE, MANUELINE_PANEL, TORII_PANEL, INCA_ASHLAR,
                        RUSSIAN_KOKOSHNIK, ONION_DOME_TILE, GEORGIAN_FANLIGHT, PALLADIAN_WINDOW,
                        STAVE_PLANK, IONIC_CAPITAL, MOORISH_STAR_TILE, CRAFTSMAN_PANEL,
                        BRUTALIST_PANEL, METOPE, ARMENIAN_KHACHKAR, BENIN_RELIEF,
                        MAORI_CARVING, MUGHAL_JALI, PERSIAN_TILE, SWISS_CHALET,
                        ANDEAN_TEXTILE, BAROQUE_ORNAMENT, POLYNESIAN_CARVED,
                        MOORISH_COLUMN, PORTUGUESE_CORK,
                        SPINNING_WHEEL_BLOCK, DYE_VAT_BLOCK, LOOM_BLOCK,
                        TEXTILE_RUG_NATURAL, TEXTILE_RUG_GOLDEN, TEXTILE_RUG_CRIMSON,
                        TEXTILE_RUG_ROSE, TEXTILE_RUG_COBALT, TEXTILE_RUG_VIOLET,
                        TEXTILE_RUG_VERDANT, TEXTILE_RUG_AMBER, TEXTILE_RUG_IVORY,
                        TEXTILE_TAPESTRY_NATURAL, TEXTILE_TAPESTRY_GOLDEN,
                        TEXTILE_TAPESTRY_CRIMSON, TEXTILE_TAPESTRY_ROSE,
                        TEXTILE_TAPESTRY_COBALT, TEXTILE_TAPESTRY_VIOLET,
                        TEXTILE_TAPESTRY_VERDANT, TEXTILE_TAPESTRY_AMBER,
                        TEXTILE_TAPESTRY_IVORY,
                        GLASS_KILN_BLOCK,
                        CLEAR_GLASS, STAINED_GLASS_GOLDEN, STAINED_GLASS_CRIMSON,
                        STAINED_GLASS_ROSE, STAINED_GLASS_COBALT, STAINED_GLASS_VIOLET,
                        STAINED_GLASS_VERDANT, STAINED_GLASS_AMBER, STAINED_GLASS_IVORY,
                        CATHEDRAL_WINDOW, MOSAIC_GLASS, SMOKED_GLASS,
                        RIBBED_GLASS, HAMMERED_GLASS, CRACKLED_GLASS,
                        OCULUS_WINDOW, LANCET_WINDOW, DIAMOND_PANE,
                        SEA_GLASS, MIRROR_GLASS, IRIDESCENT_GLASS,
                        SUNSET_GLASS, OBSIDIAN_GLASS, CRYSTAL_GLASS,
                        POTTERY_WHEEL_BLOCK, POTTERY_KILN_BLOCK,
                        CALCADA_PORTUGUESA, AZULEJO_GEOMETRIC, PAINTED_TILE_BORDER,
                        SPANISH_MAJOLICA, AZULEJO_STAIR,
                        PORTUGUESE_PINK_MARBLE, SPANISH_HEX_TILE, MUDEJAR_STAR_TILE,
                        ALBARRADA_PANEL, SGRAFFITO_WALL, TRENCADIS_PANEL,
                        AZULEJO_NAVY, AZULEJO_MANGANESE, PLATERESQUE_PANEL, AZULEJO_CORNICE,
                        TALAVERA_FOUNTAIN, BARCELONA_TILE, MOORISH_ARCHWAY_TILE,
                        PORTUGUESE_CHIMNEY, BARCELOS_TILE, REJA_PANEL,
                        ORANGE_TREE_PLANTER, WAVE_COBBLE, AZULEJO_FACADE_PANEL,
                        MUDEJAR_BRICK, PORTUGUESE_BENCH, SPANISH_PATIO_FLOOR,
                        ARABIC_ROOF_TILE, MOORISH_COLUMN_TILE, ESTREMOZ_MARBLE,
                        MEZQUITA_ARCH, MIHRAB_TILE, MEDINA_AZAHARA_STONE, CORDOBA_COLUMN,
                        ORANGE_COURT_FLOOR, CORDOBAN_LEATHER, UMAYYAD_MULTILOBED,
                        GOLD_TESSERA_PANEL, UMAYYAD_DOME_RIB, KUFIC_PANEL,
                        PATIO_FLOWER_WALL, CORDOBAN_PATIO_TILE, STAR_VAULT_PANEL,
                        ANDALUSIAN_FOUNTAIN, NASRID_HONEYCOMB,
                        CRACKED_STONE, STALACTITE, STALAGMITE, CAVE_MOSS,
                        )
    TERRAIN_IDS = (
        {AIR, GRASS, DIRT, STONE, OBSIDIAN, BEDROCK, WATER, GRAVEL,
         GATE_MID, GATE_DEEP, GATE_CORE,
         CRACKED_STONE, STALACTITE, STALAGMITE, CAVE_MOSS,
         HOUSE_WALL, HOUSE_ROOF,
         HOUSE_WALL_STONE, HOUSE_ROOF_STONE,
         HOUSE_WALL_BRICK, HOUSE_ROOF_BRICK,
         HOUSE_WALL_DARK, HOUSE_ROOF_DARK,
         RESTAURANT_WALL, RESTAURANT_AWNING,
         POLISHED_GRANITE, POLISHED_MARBLE, SLATE_TILE,
         TERRACOTTA_BLOCK, MOSSY_BRICK, CREAM_BRICK,
         CHARCOAL_PLANK, WALNUT_PLANK, OAK_PANEL, BAMBOO_PANEL,
         OBSIDIAN_TILE, COBBLESTONE, LAPIS_BRICK, BASALT_COLUMN,
         LIMESTONE_BLOCK, COPPER_TILE, TEAK_PLANK,
         DRIFTWOOD_PLANK, CEDAR_PANEL, JADE_PANEL,
         ROSE_QUARTZ_BLOCK, GILDED_BRICK, AMETHYST_BLOCK,
         AMBER_TILE, IVORY_BRICK, EBONY_PLANK,
         MAHOGANY_PLANK, ASH_PLANK, FROSTED_GLASS, CRIMSON_BRICK,
         TERRACOTTA_SHINGLE, THATCH_ROOF, VERDIGRIS_COPPER,
         SILVER_PANEL, GOLD_LEAF_TRIM,
         STAINED_GLASS_RED, STAINED_GLASS_BLUE, STAINED_GLASS_GREEN,
         QUARTZ_PILLAR, ONYX_INLAY,
         WHITE_PLASTER_WALL, CARVED_PLASTER, MUQARNAS_BLOCK,
         MASHRABIYA, ZELLIGE_TILE, ARABESQUE_PANEL,
         ADOBE_BRICK, SPANISH_ROOF_TILE, WROUGHT_IRON_GRILLE,
         TALAVERA_TILE, SALTILLO_TILE,
         COBALT_DOOR_CLOSED, COBALT_DOOR_OPEN,
         CRIMSON_CEDAR_DOOR_CLOSED, CRIMSON_CEDAR_DOOR_OPEN,
         TEAL_DOOR_CLOSED, TEAL_DOOR_OPEN,
         SAFFRON_DOOR_CLOSED, SAFFRON_DOOR_OPEN,
         STUDDED_OAK_DOOR_CLOSED, STUDDED_OAK_DOOR_OPEN,
         VERMILION_DOOR_CLOSED, VERMILION_DOOR_OPEN,
         SHOJI_DOOR_CLOSED, SHOJI_DOOR_OPEN,
         GILDED_DOOR_CLOSED, GILDED_DOOR_OPEN,
         BRONZE_DOOR_CLOSED, BRONZE_DOOR_OPEN,
         SWAHILI_DOOR_CLOSED, SWAHILI_DOOR_OPEN,
         SANDALWOOD_DOOR_CLOSED, SANDALWOOD_DOOR_OPEN,
         STONE_SLAB_DOOR_CLOSED, STONE_SLAB_DOOR_OPEN,
         HALF_TIMBER_WALL, ASHLAR_BLOCK, GOTHIC_TRACERY, FLUTED_COLUMN,
         CORNICE_BLOCK, ROSE_WINDOW, HERRINGBONE_BRICK, BAROQUE_TRIM,
         TUDOR_BEAM, VENETIAN_FLOOR, FLEMISH_BRICK, PILASTER,
         DENTIL_TRIM, WATTLE_DAUB, NORDIC_PLANK, MANSARD_SLATE,
         ROMAN_MOSAIC, SETT_STONE, ROMANESQUE_ARCH, DARK_SLATE_ROOF,
         KEYSTONE, PLINTH_BLOCK, IRON_LANTERN, SANDSTONE_ASHLAR,
         GARGOYLE_BLOCK, LIGHT_TRAP_BLOCK,
         OGEE_ARCH, RUSTICATED_STONE, CHEVRON_STONE, TRIGLYPH_PANEL,
         MARBLE_INLAY, BRICK_NOGGING, CRENELLATION, FAN_VAULT,
         PORTCULLIS_BLOCK, ARROW_LOOP, MACHICOLATION, DRAWBRIDGE_PLANK,
         ROUND_TOWER_WALL, CURTAIN_WALL, CORBEL_COURSE, TOWER_CAP,
         GREAT_HALL_FLOOR, DUNGEON_WALL, CASTLE_FIREPLACE, HERALDIC_PANEL,
         WALL_WALK_FLOOR, CASTLE_GATE_ARCH, DRAWBRIDGE_CHAIN, DUNGEON_GRATE,
         MOAT_STONE, CHAPEL_STONE, MURDER_HOLE, GARDEROBE_CHUTE,
         ACANTHUS_PANEL, PEBBLE_DASH, ENCAUSTIC_TILE, CHEQUERBOARD_MARBLE,
         WROUGHT_IRON_BALUSTRADE, OPUS_INCERTUM, GROTESQUE_FRIEZE,
         BARREL_VAULT, POINTED_ARCH, ENGLISH_BOND, RELIEF_PANEL,
         DIAGONAL_TILE,
         TAPESTRY_BLOCK, WOVEN_RUG, CELTIC_KNOTWORK, BYZANTINE_MOSAIC,
         JAPANESE_SHOJI, OTTOMAN_TILE, LEADLIGHT_WINDOW, TUDOR_ROSE,
         GREEK_KEY, VENETIAN_PLASTER, SCOTTISH_RUBBLE, ART_NOUVEAU_PANEL,
         DUTCH_GABLE, STRIPED_ARCH, TIMBER_TRUSS, HEARTH_STONE,
         LINEN_FOLD, PARQUET_FLOOR, COFFERED_CEILING, OPUS_SIGNINUM,
         GLAZED_ROOF_TILE, LATTICE_SCREEN, MOON_GATE, PAINTED_BEAM,
         DOUGONG, CERAMIC_PLANTER, STONE_LANTERN, LACQUER_PANEL,
         PAPER_LANTERN, DRAGON_TILE, HAN_BRICK, PAVILION_FLOOR,
         BAMBOO_SCREEN, CLOUD_MOTIF, COIN_TILE, BLUE_WHITE_TILE,
         GARDEN_ROCK, STEPPED_WALL, PAGODA_EAVE, CINNABAR_WALL,
         WHITEWASHED_WALL, MONASTERY_ROOF, MANI_STONE, PRAYER_FLAG_BLOCK,
         MUGHAL_ARCH, PIETRA_DURA, EGYPTIAN_FRIEZE, SANDSTONE_COLUMN,
         AZTEC_SUNSTONE, MAYA_RELIEF, VIKING_CARVING, RUNE_STONE,
         PERSIAN_IWAN, KILIM_TILE, AFRICAN_MUD_BRICK, KENTE_PANEL,
         WAT_FINIAL, KHMER_STONE, HANJI_SCREEN, DANCHEONG,
         ART_DECO_PANEL, OBSIDIAN_CUT, OTTOMAN_ARCH, LOTUS_CAPITAL,
         AZULEJO_TILE, MANUELINE_PANEL, TORII_PANEL, INCA_ASHLAR,
         RUSSIAN_KOKOSHNIK, ONION_DOME_TILE, GEORGIAN_FANLIGHT, PALLADIAN_WINDOW,
         STAVE_PLANK, IONIC_CAPITAL, MOORISH_STAR_TILE, CRAFTSMAN_PANEL,
         BRUTALIST_PANEL, METOPE, ARMENIAN_KHACHKAR, BENIN_RELIEF,
         MAORI_CARVING, MUGHAL_JALI, PERSIAN_TILE, SWISS_CHALET,
         ANDEAN_TEXTILE, BAROQUE_ORNAMENT, POLYNESIAN_CARVED,
         MOORISH_COLUMN, PORTUGUESE_CORK,
         SPINNING_WHEEL_BLOCK, DYE_VAT_BLOCK, LOOM_BLOCK,
         TEXTILE_RUG_NATURAL, TEXTILE_RUG_GOLDEN, TEXTILE_RUG_CRIMSON,
         TEXTILE_RUG_ROSE, TEXTILE_RUG_COBALT, TEXTILE_RUG_VIOLET,
         TEXTILE_RUG_VERDANT, TEXTILE_RUG_AMBER, TEXTILE_RUG_IVORY,
         TEXTILE_TAPESTRY_NATURAL, TEXTILE_TAPESTRY_GOLDEN, TEXTILE_TAPESTRY_CRIMSON,
         TEXTILE_TAPESTRY_ROSE, TEXTILE_TAPESTRY_COBALT, TEXTILE_TAPESTRY_VIOLET,
         TEXTILE_TAPESTRY_VERDANT, TEXTILE_TAPESTRY_AMBER, TEXTILE_TAPESTRY_IVORY,
         GLASS_KILN_BLOCK,
         CLEAR_GLASS, STAINED_GLASS_GOLDEN, STAINED_GLASS_CRIMSON,
         STAINED_GLASS_ROSE, STAINED_GLASS_COBALT, STAINED_GLASS_VIOLET,
         STAINED_GLASS_VERDANT, STAINED_GLASS_AMBER, STAINED_GLASS_IVORY,
         CATHEDRAL_WINDOW, MOSAIC_GLASS, SMOKED_GLASS,
         RIBBED_GLASS, HAMMERED_GLASS, CRACKLED_GLASS,
         OCULUS_WINDOW, LANCET_WINDOW, DIAMOND_PANE,
         SEA_GLASS, MIRROR_GLASS, IRIDESCENT_GLASS,
         SUNSET_GLASS, OBSIDIAN_GLASS, CRYSTAL_GLASS,
         POTTERY_WHEEL_BLOCK, POTTERY_KILN_BLOCK,
         CALCADA_PORTUGUESA, AZULEJO_GEOMETRIC, PAINTED_TILE_BORDER,
         SPANISH_MAJOLICA, AZULEJO_STAIR,
         PORTUGUESE_PINK_MARBLE, SPANISH_HEX_TILE, MUDEJAR_STAR_TILE,
         ALBARRADA_PANEL, SGRAFFITO_WALL, TRENCADIS_PANEL,
         AZULEJO_NAVY, AZULEJO_MANGANESE, PLATERESQUE_PANEL, AZULEJO_CORNICE,
         TALAVERA_FOUNTAIN, BARCELONA_TILE, MOORISH_ARCHWAY_TILE,
         PORTUGUESE_CHIMNEY, BARCELOS_TILE, REJA_PANEL,
         ORANGE_TREE_PLANTER, WAVE_COBBLE, AZULEJO_FACADE_PANEL,
         MUDEJAR_BRICK, PORTUGUESE_BENCH, SPANISH_PATIO_FLOOR,
         ARABIC_ROOF_TILE, MOORISH_COLUMN_TILE, ESTREMOZ_MARBLE,
         MEZQUITA_ARCH, MIHRAB_TILE, MEDINA_AZAHARA_STONE, CORDOBA_COLUMN,
         ORANGE_COURT_FLOOR, CORDOBAN_LEATHER, UMAYYAD_MULTILOBED,
         GOLD_TESSERA_PANEL, UMAYYAD_DOME_RIB, KUFIC_PANEL,
         PATIO_FLOWER_WALL, CORDOBAN_PATIO_TILE, STAR_VAULT_PANEL,
         ANDALUSIAN_FOUNTAIN, NASRID_HONEYCOMB,
         SNOW, SAND}
        | ALL_LOGS | ALL_LEAVES
    )
    stone_col = BLOCKS[STONE]["color"]
    table = [(30, 28, 38)] * 512
    for bid, bdata in BLOCKS.items():
        if 0 <= bid < 512:
            if bid in TERRAIN_IDS:
                col = bdata.get("color")
                table[bid] = col if col else stone_col
            else:
                table[bid] = stone_col
    return table


def rebuild_minimap(renderer, world):
    if not world._chunks:
        renderer._minimap_surf = None
        return
    cxs = sorted(world._chunks.keys())
    min_cx, max_cx = cxs[0], cxs[-1]
    raw_w = (max_cx - min_cx + 1) * CHUNK_W
    raw_h = WORLD_H
    renderer._mm_min_bx = min_cx * CHUNK_W
    renderer._mm_span_bx = raw_w
    raw = pygame.Surface((raw_w, raw_h))
    ctable = renderer._mm_ctable
    mapped = [raw.map_rgb(*ctable[i]) for i in range(len(ctable))]
    pa = pygame.PixelArray(raw)
    mask = len(ctable) - 1
    for cx in cxs:
        chunk = world._chunks[cx]
        base_x = (cx - min_cx) * CHUNK_W
        for lx in range(CHUNK_W):
            for y in range(raw_h):
                pa[base_x + lx][y] = mapped[chunk[y][lx] & mask]
    del pa
    renderer._minimap_surf = pygame.transform.scale(raw, (_MM_W, _MM_H))


def draw_minimap(renderer, world, player, dt):
    if not renderer.minimap_visible:
        return
    renderer._minimap_timer -= dt
    if renderer._minimap_surf is None or renderer._minimap_timer <= 0:
        rebuild_minimap(renderer, world)
        renderer._minimap_timer = 3.0
    if renderer._minimap_surf is None:
        return

    mx = SCREEN_W - _MM_W - _MM_MARGIN
    my = SCREEN_H - _MM_H - 58 - _MM_MARGIN

    pygame.draw.rect(renderer.screen, (12, 10, 18), (mx - 4, my - 4, _MM_W + 8, _MM_H + 8))
    renderer.screen.blit(renderer._minimap_surf, (mx, my))
    pygame.draw.rect(renderer.screen, (65, 65, 75), (mx - 4, my - 4, _MM_W + 8, _MM_H + 8), 1)

    mm_off  = getattr(renderer, '_mm_min_bx', 0)
    mm_span = max(1, getattr(renderer, '_mm_span_bx', 1))
    h = world.height

    vx = int((renderer.cam_x / BLOCK_SIZE - mm_off) / mm_span * _MM_W)
    vy = int(renderer.cam_y / BLOCK_SIZE * _MM_H / h)
    vw = max(2, int(SCREEN_W / BLOCK_SIZE / mm_span * _MM_W))
    vh = max(2, int(SCREEN_H / BLOCK_SIZE * _MM_H / h))
    vx = max(0, min(_MM_W - 1, vx))
    vy = max(0, min(_MM_H - 1, vy))
    pygame.draw.rect(renderer.screen, (220, 215, 50), (mx + vx, my + vy, vw, vh), 1)

    px_map = int((player.x / BLOCK_SIZE - mm_off) / mm_span * _MM_W)
    py_map = int(player.y / BLOCK_SIZE * _MM_H / h)
    px_map = max(1, min(_MM_W - 2, px_map))
    py_map = max(1, min(_MM_H - 2, py_map))
    pygame.draw.rect(renderer.screen, (255, 255, 255), (mx + px_map - 1, my + py_map - 1, 3, 3))
