"""
Render/blocks_victorian.py — Custom block art for Victorian & Craftsman home blocks.
Solid-color blocks are handled by the fallback in blockRenderHandler.py; only
blocks that need texture/pattern work are rendered here.
"""
import pygame
from blocks import BLOCKS
from constants import BLOCK_SIZE
from Render.block_helpers import _darken, _lighter

BS = BLOCK_SIZE

# Import all 250 Victorian block constants
from blocks import (
    FISH_SCALE_SHINGLE, FISH_SCALE_SHINGLE_DARK, FISH_SCALE_SHINGLE_BLUE,
    CLAPBOARD_SIDING, CLAPBOARD_SIDING_DARK, DROP_SIDING,
    BOARD_AND_BATTEN_SIDING, SHIPLAP_SIDING,
    PEBBLEDASH_RENDER, HALF_TIMBERING_PANEL, TERRACOTTA_CLADDING_TILE,
    FAIENCE_TILE_PANEL, PRESSED_METAL_PANEL, INCISED_RENDER_PANEL,
    ROUGHCAST_RENDER, PARGETING_PANEL, STUCCO_BAND,
    DECORATIVE_FRIEZE_PANEL, VERGEBOARD, DENTIL_MOULDING_STRIP,
    SLATE_ROOF_TILE, SLATE_ROOF_TILE_DARK, CLAY_ROOF_TILE, CLAY_ROOF_TILE_GREEN,
    IMBREX_ROOF_TILE, MANSARD_SLATE_PANEL,
    DECORATED_RIDGE_TILE, FINIAL_BLOCK, IRON_CRESTING_RAIL,
    JERKINHEAD_GABLE, TURRET_CAP_BLOCK, OCTAGONAL_TURRET_BLOCK,
    BAY_WINDOW_ROOF, DORMER_CHEEK, GABLED_DORMER_FRONT,
    PRESSED_BRICK, PRESSED_BRICK_BUFF, GAUGED_BRICK, RUBBED_BRICK,
    VITRIFIED_BRICK, POLYCHROME_BRICK_RED, POLYCHROME_BRICK_BLUE,
    POLYCHROME_BRICK_CREAM, TERRACOTTA_BLOCK, TERRACOTTA_PANEL,
    BUFF_TERRACOTTA, RUSTICATED_STONE, ASHLAR_STONE_BLOCK, ROCK_FACED_STONE,
    VERMICULATED_STONE, QUOIN_BLOCK, STRING_COURSE_BLOCK, PLINTH_BLOCK,
    ARCH_KEYSTONE_BLOCK, VOUSSOIR_BLOCK,
    TYMPANUM_PANEL, MEDALLION_BLOCK, CARTOUCHE_BLOCK, HERALDIC_PANEL,
    FLORENTINE_STONE,
    IONIC_COLUMN, DORIC_COLUMN, CORINTHIAN_COLUMN_SHAFT,
    COLUMN_CAPITAL, COLUMN_BASE, PILASTER_BLOCK, ENGAGED_COLUMN_BLOCK,
    FLUTED_PANEL, BRACKET_SUPPORT, KNEE_BRACE, CORBEL_BLOCK,
    MODILLION_BLOCK, CONSOLE_BRACKET, CANTILEVER_BEAM_END, EXPOSED_RAFTER_END,
    STAINED_GLASS_RED, STAINED_GLASS_BLUE, STAINED_GLASS_AMBER,
    STAINED_GLASS_GREEN, STAINED_GLASS_PURPLE, LEADED_LIGHT_PANEL,
    QUARRY_GLASS_PANEL, FROSTED_GLASS_PANEL, ETCHED_GLASS_PANEL,
    COLOURED_BORDER_GLASS,
    BAY_WINDOW_FRAME, ORIEL_WINDOW_FRAME, TRANSOM_WINDOW_FRAME,
    FANLIGHT_FRAME, GOTHIC_ARCH_WINDOW, ROUND_ARCH_WINDOW,
    PALLADIAN_WINDOW_FRAME, SASH_WINDOW_FRAME, CASEMENT_WINDOW_FRAME,
    VENETIAN_WINDOW_FRAME,
    PANELLED_DOOR_BLOCK, GLAZED_DOOR_BLOCK, DOUBLE_DOOR_BLOCK,
    DUTCH_DOOR_BLOCK, SLIDING_POCKET_DOOR_BLOCK,
    FANLIGHT_SURROUND, PILASTER_DOOR_SURROUND, HOOD_MOULDING,
    PORCH_ENTRY_STEPS, BOOT_SCRAPER_BLOCK, DOOR_KNOCKER_PLATE,
    LETTERBOX_PANEL, MARBLE_THRESHOLD, STORM_DOOR_BLOCK, SERVICE_DOOR_BLOCK,
    PORCH_COLUMN, ORNATE_PORCH_COLUMN, SPINDLE_RAIL, NEWEL_POST,
    BALUSTER_BLOCK, PORCH_BALUSTRADE, PORCH_CORNICE, VERANDA_BRACKET,
    PORCH_CEILING_BOARD, PORCH_FLOOR_BOARD, SCREEN_PORCH_PANEL,
    PORTE_COCHERE_BEAM, PERGOLA_POST, PERGOLA_BEAM, PERGOLA_SLAT,
    PORCH_SWING_BRACKET, WISTERIA_TRELLIS, LATTICE_PANEL,
    JIGSAW_TRIM_PANEL, GINGERBREAD_TRIM,
    WAINSCOT_PANEL_OAK, WAINSCOT_PANEL_DARK, BEADBOARD_PANEL,
    RAISED_PANEL_WALL, LINCRUSTA_PANEL, ANAGLYPTA_PANEL,
    DADO_RAIL, PICTURE_RAIL, CROWN_MOULDING, COVED_CORNICE,
    DENTIL_CORNICE, EGG_AND_DART_MOULDING, OVOLO_MOULDING,
    TALL_BASEBOARD, DARK_BASEBOARD, ARCHITRAVE,
    FLUTED_INTERIOR_PILASTER, SMOOTH_PLASTER_PANEL, PLASTER_CEILING_ROSE,
    COFFERED_CEILING_PANEL, EMBOSSED_TIN_CEILING_SILVER,
    EMBOSSED_TIN_CEILING_GOLD, SHIPLAP_INTERIOR, TONGUE_GROOVE_PLANK,
    WIDE_BOARD_PANELLING,
    ENCAUSTIC_FLOOR_TILE_RED, ENCAUSTIC_FLOOR_TILE_BLUE,
    ENCAUSTIC_FLOOR_TILE_GREEN, ENCAUSTIC_BORDER_TILE,
    GEOMETRIC_MOSAIC_FLOOR, PARQUET_FLOOR_HERRINGBONE,
    PARQUET_FLOOR_BASKET, PARQUET_FLOOR_STRIP,
    MARBLE_FLOOR_TILE, MARBLE_FLOOR_TILE_BLACK,
    TERRACOTTA_FLOOR_TILE, FLAGSTONE_FLOOR,
    HARDWOOD_STAIR_TREAD, PAINTED_STAIR_RISER, BRASS_STAIR_NOSING,
    OPEN_RISER_STAIR_STEP, LANDING_BOARD, BALCONY_DECK_BOARD,
    CELLAR_STONE_FLOOR, TILE_THRESHOLD_STRIP,
    FIREPLACE_MANTEL, FIREPLACE_SURROUND_TILE, FIREPLACE_OVERMANTEL,
    CAST_IRON_GRATE_FRONT, CAST_IRON_FIREBACK, HEARTH_TILE,
    INGLENOOK_SIDE_WALL, INGLENOOK_BENCH, OAK_BOOKCASE, PAINTED_BOOKCASE,
    WINDOW_SEAT_BOX, ALCOVE_SHELF, BUTLER_PANTRY_SHELF,
    CHINA_CABINET_BLOCK, BUILT_IN_WARDROBE_PANEL, HIGH_BACK_SETTLE,
    PLATE_RACK, DRESSER_BACK_PANEL, PANTRY_DOOR_BLOCK, DUMBWAITER_SHAFT_PANEL,
    WROUGHT_IRON_FENCE_PANEL, WROUGHT_IRON_GATE, BRICK_GARDEN_PIER,
    STONE_GARDEN_PIER, CAST_IRON_RAILING_PANEL, LOW_GARDEN_WALL,
    GARDEN_WALL_COPING, STONE_GARDEN_BALUSTRADE, STONE_GARDEN_STEPS,
    BATTERED_RETAINING_WALL, COAL_HOLE_COVER, AREA_STEPS_BLOCK,
    MOUNTING_BLOCK, GARDEN_URN_PEDESTAL, SUNDIAL_PEDESTAL,
    CARRIAGE_HOUSE_DOOR, STABLE_WALL_PANEL, CONSERVATORY_GLASS_PANEL,
    CONSERVATORY_IRON_FRAME, VICTORIAN_GREENHOUSE_FRAME,
    CLINKER_BRICK, RIVER_ROCK_BLOCK, RIVER_ROCK_COLUMN,
    COBBLESTONE_PIER, CRAFTSMAN_BEAM_END, CRAFTSMAN_FRIEZE_BOARD,
    CRAFTSMAN_BARGEBOARD, CRAFTSMAN_TRIM_STRIP, ARTS_AND_CRAFTS_TILE,
    PRAIRIE_GRID_GLASS, STRAP_HINGE_PANEL, CRAFTSMAN_COLUMN_CAP,
    TAPERED_PORCH_POST, SHED_DORMER_BLOCK,
    CHIMNEY_STACK_BLOCK, CHIMNEY_POT, CHIMNEY_CAP, FLAUNCHING_BLOCK,
    CAST_IRON_GUTTER, CAST_IRON_DOWNPIPE, HOPPER_HEAD_BLOCK,
    AIR_BRICK, DAMP_COURSE_BLOCK, BASEMENT_WINDOW_WELL,
    ICE_HOUSE_BLOCK, GARDEN_TOOL_STORE_PANEL, BELL_TOWER_BLOCK,
    SUMMERHOUSE_PANEL, GAZEBO_BEAM, GARDEN_PAVILION_POST,
    DOVECOTE_BLOCK, HA_HA_WALL_BLOCK, TOPIARY_FRAME, ROSE_ARCH_FRAME,
    COAL_CELLAR_BLOCK,
)


def _solid(bid):
    """Quick solid-color surface with 1px dark border."""
    base = BLOCKS[bid]["color"]
    s = pygame.Surface((BS, BS))
    s.fill(base)
    pygame.draw.rect(s, _darken(base), s.get_rect(), 1)
    return s


def _brick_pattern(base, mortar=(215, 208, 198), offset_rows=True):
    """Draw a brick wall pattern on a surface."""
    s = pygame.Surface((BS, BS))
    s.fill(mortar)
    dark = _darken(base, 20)
    bh = BS // 4          # brick height
    bw = BS // 2          # brick width
    for row in range(4):
        y = row * bh
        shift = bw // 2 if (offset_rows and row % 2 == 1) else 0
        for col in range(-1, 3):
            x = col * bw + shift
            pygame.draw.rect(s, base,  (x + 1, y + 1, bw - 2, bh - 2))
            pygame.draw.rect(s, dark,  (x + 1, y + 1, bw - 2, bh - 2), 1)
    return s


def _wood_plank_h(base, n_planks=4, groove_dark=30):
    """Horizontal wood planks."""
    s = pygame.Surface((BS, BS))
    ph = BS // n_planks
    for i in range(n_planks):
        c = _lighter(base, 8) if i % 2 == 0 else _darken(base, 8)
        pygame.draw.rect(s, c, (0, i * ph, BS, ph))
    for i in range(1, n_planks):
        pygame.draw.line(s, _darken(base, groove_dark), (0, i * ph), (BS, i * ph), 1)
    pygame.draw.rect(s, _darken(base, groove_dark), (0, 0, BS, BS), 1)
    return s


def _wood_plank_v(base, n_planks=4, groove_dark=30):
    """Vertical wood planks."""
    s = pygame.Surface((BS, BS))
    pw = BS // n_planks
    for i in range(n_planks):
        c = _lighter(base, 8) if i % 2 == 0 else _darken(base, 8)
        pygame.draw.rect(s, c, (i * pw, 0, pw, BS))
    for i in range(1, n_planks):
        pygame.draw.line(s, _darken(base, groove_dark), (i * pw, 0), (i * pw, BS), 1)
    pygame.draw.rect(s, _darken(base, groove_dark), (0, 0, BS, BS), 1)
    return s


def _stained_glass(glass_color, lead=(30, 28, 30)):
    """Stained glass with diamond leading pattern."""
    s = pygame.Surface((BS, BS))
    s.fill(glass_color)
    # diagonal leading lines
    pygame.draw.line(s, lead, (0, BS // 2), (BS // 2, 0), 2)
    pygame.draw.line(s, lead, (BS // 2, 0), (BS, BS // 2), 2)
    pygame.draw.line(s, lead, (BS, BS // 2), (BS // 2, BS), 2)
    pygame.draw.line(s, lead, (BS // 2, BS), (0, BS // 2), 2)
    # center cross
    pygame.draw.line(s, lead, (BS // 2, 0), (BS // 2, BS), 1)
    pygame.draw.line(s, lead, (0, BS // 2), (BS, BS // 2), 1)
    # bright highlight in each quadrant
    hi = _lighter(glass_color, 50)
    pygame.draw.circle(s, hi, (BS // 4, BS // 4), 3)
    pygame.draw.circle(s, hi, (3 * BS // 4, BS // 4), 3)
    pygame.draw.circle(s, hi, (BS // 4, 3 * BS // 4), 3)
    pygame.draw.circle(s, hi, (3 * BS // 4, 3 * BS // 4), 3)
    pygame.draw.rect(s, lead, (0, 0, BS, BS), 1)
    return s


def _leaded_grid(base, lead=(55, 52, 50), cell=8):
    """Square leaded light grid."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    for x in range(0, BS, cell):
        pygame.draw.line(s, lead, (x, 0), (x, BS), 1)
    for y in range(0, BS, cell):
        pygame.draw.line(s, lead, (0, y), (BS, y), 1)
    pygame.draw.rect(s, lead, (0, 0, BS, BS), 1)
    return s


def _diamond_leaded(base, lead=(55, 52, 50)):
    """Diamond pane (quarry) leaded glass."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    d = BS // 3
    for row in range(-1, 4):
        for col in range(-1, 4):
            cx = col * d + (d // 2 if row % 2 else 0)
            cy = row * d
            pts = [(cx, cy + d // 2), (cx + d // 2, cy),
                   (cx, cy - d // 2), (cx - d // 2, cy)]
            pygame.draw.polygon(s, lead, pts, 1)
    pygame.draw.rect(s, lead, (0, 0, BS, BS), 1)
    return s


def _encaustic_tile(primary, secondary, cream=(230, 220, 200)):
    """Victorian encaustic tile with cross-in-square pattern."""
    s = pygame.Surface((BS, BS))
    s.fill(cream)
    h = BS // 2
    # four corner squares
    for cx, cy in [(0, 0), (h, 0), (0, h), (h, h)]:
        col = primary if (cx + cy) // h % 2 == 0 else secondary
        pygame.draw.rect(s, col, (cx + 2, cy + 2, h - 4, h - 4))
    # center diamond
    mid = BS // 2
    d = BS // 5
    pts = [(mid, mid - d), (mid + d, mid), (mid, mid + d), (mid - d, mid)]
    pygame.draw.polygon(s, cream, pts)
    pygame.draw.polygon(s, _darken(primary, 30), pts, 1)
    # grid lines
    pygame.draw.line(s, _darken(cream, 40), (0, h), (BS, h), 1)
    pygame.draw.line(s, _darken(cream, 40), (h, 0), (h, BS), 1)
    pygame.draw.rect(s, _darken(cream, 40), (0, 0, BS, BS), 1)
    return s


def _herringbone(base):
    """Herringbone parquet floor pattern."""
    s = pygame.Surface((BS, BS))
    s.fill(_darken(base, 20))
    w, h = BS // 4, BS // 8
    dark = _darken(base, 30)
    light = _lighter(base, 15)
    for row in range(-1, BS // h + 2):
        for col in range(-1, BS // w + 2):
            x = col * w + (row % 2) * (w // 2)
            y = row * h
            c = light if (row + col) % 2 == 0 else base
            # alternating horizontal/vertical strips
            if row % 2 == 0:
                pygame.draw.rect(s, c, (x, y, w - 1, h - 1))
            else:
                pygame.draw.rect(s, c, (x, y, h - 1, w - 1))
            pygame.draw.rect(s, dark, (x, y, w - 1, h - 1), 1) if row % 2 == 0 \
                else pygame.draw.rect(s, dark, (x, y, h - 1, w - 1), 1)
    pygame.draw.rect(s, _darken(base, 40), (0, 0, BS, BS), 1)
    return s


def _beadboard(base):
    """Narrow vertical bead paneling."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    bead_w = 4
    dark  = _darken(base, 35)
    hi    = _lighter(base, 35)
    for x in range(0, BS, bead_w):
        pygame.draw.line(s, dark, (x, 0), (x, BS), 1)
        pygame.draw.line(s, hi,   (x + 1, 0), (x + 1, BS), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _raised_panel(base):
    """Interior raised-field wall panel."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 40)
    m = 4
    # outer bevel
    pygame.draw.lines(s, dark, False, [(0, BS-1), (0, 0), (BS-1, 0)], 2)
    pygame.draw.lines(s, hi,   False, [(1, BS-1), (BS-1, BS-1), (BS-1, 1)], 2)
    # inner raised field
    inner = (m+2, m+2, BS - 2*m - 4, BS - 2*m - 4)
    pygame.draw.rect(s, _lighter(base, 12), inner)
    pygame.draw.lines(s, hi,   False,
                      [(m, BS-m), (m, m), (BS-m, m)], 1)
    pygame.draw.lines(s, dark, False,
                      [(m+1, BS-m), (BS-m, BS-m), (BS-m, m+1)], 1)
    return s


def _fish_scale(base, rows=3):
    """Fish-scale / scallop shingle pattern."""
    s = pygame.Surface((BS, BS))
    s.fill(_darken(base, 15))
    dark  = _darken(base, 35)
    hi    = _lighter(base, 25)
    rh    = BS // rows
    w     = BS // 2
    for row in range(rows):
        y = row * rh
        shift = w // 2 if row % 2 else 0
        for col in range(-1, 3):
            cx = col * w + w // 2 + shift
            # filled arc (half-ellipse = scale)
            rect = pygame.Rect(cx - w // 2, y, w, rh * 2)
            pygame.draw.ellipse(s, base, rect)
            pygame.draw.arc(s, dark, rect, 0, 3.14159, 1)
            pygame.draw.arc(s, hi,   rect, 3.14159, 6.28318, 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _wrought_iron_fence(base=(45, 42, 40)):
    """Vertical iron fence pickets with pointed tops."""
    s = pygame.Surface((BS, BS))
    s.fill((110, 130, 90))   # grass backing (transparent in use)
    dark = _darken(base, 15)
    hi   = _lighter(base, 25)
    # top and bottom rails
    pygame.draw.rect(s, base, (0, 4, BS, 4))
    pygame.draw.rect(s, base, (0, BS - 8, BS, 4))
    # pickets
    for x in range(2, BS, 6):
        pygame.draw.rect(s, base, (x, 8, 3, BS - 12))
        # spear tip
        pts = [(x + 1, 2), (x, 8), (x + 3, 8)]
        pygame.draw.polygon(s, hi, pts)
        pygame.draw.polygon(s, dark, pts, 1)
    return s


def _lattice(base=(235, 232, 228)):
    """Diamond lattice panel."""
    s = pygame.Surface((BS, BS))
    s.fill(_lighter(base, 20))
    dark = _darken(base, 40)
    step = 8
    for i in range(-BS, BS * 2, step):
        pygame.draw.line(s, dark, (i, 0), (i + BS, BS), 1)
        pygame.draw.line(s, dark, (i + BS, 0), (i, BS), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _mosaic(colors):
    """Small geometric tessellated mosaic."""
    s = pygame.Surface((BS, BS))
    cell = 4
    for row in range(BS // cell):
        for col in range(BS // cell):
            c = colors[(row + col) % len(colors)]
            c2 = _darken(c, 15) if (row + col) % 3 == 0 else c
            pygame.draw.rect(s, c2, (col * cell, row * cell, cell - 1, cell - 1))
    pygame.draw.rect(s, _darken(colors[0], 50), (0, 0, BS, BS), 1)
    return s


def _column_shaft(base, fluted=False):
    """Cylindrical column shaft."""
    s = pygame.Surface((BS, BS))
    s.fill((0, 0, 0, 0) if hasattr(s, 'set_alpha') else base)
    s.fill(base)
    dark  = _darken(base, 40)
    hi    = _lighter(base, 50)
    # main shaft
    shaft_x = BS // 4
    shaft_w = BS // 2
    pygame.draw.rect(s, base, (shaft_x, 0, shaft_w, BS))
    # shading for cylindrical look
    pygame.draw.line(s, hi,   (shaft_x + 2, 0), (shaft_x + 2, BS), 2)
    pygame.draw.line(s, dark, (shaft_x + shaft_w - 3, 0), (shaft_x + shaft_w - 3, BS), 2)
    if fluted:
        for fx in range(shaft_x + 2, shaft_x + shaft_w - 2, 4):
            pygame.draw.line(s, _darken(base, 20), (fx, 0), (fx, BS), 1)
    pygame.draw.rect(s, dark, (shaft_x, 0, shaft_w, BS), 1)
    return s


def _tin_ceiling(base, emboss_color=None):
    """Embossed tin ceiling tile with repeating square pattern."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    ec  = emboss_color or _lighter(base, 30)
    dark = _darken(base, 30)
    cell = BS // 4
    for row in range(4):
        for col in range(4):
            x, y = col * cell, row * cell
            # raised square inset
            pygame.draw.rect(s, ec, (x + 2, y + 2, cell - 4, cell - 4))
            pygame.draw.lines(s, _lighter(ec, 20), False,
                              [(x+2, y+cell-2), (x+2, y+2), (x+cell-2, y+2)], 1)
            pygame.draw.lines(s, dark, False,
                              [(x+2, y+cell-2), (x+cell-2, y+cell-2), (x+cell-2, y+2)], 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _cofferred(base):
    """Coffered ceiling grid panel."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 45)
    hi   = _lighter(base, 35)
    m = 6
    # recessed field
    field = (m, m, BS - 2 * m, BS - 2 * m)
    pygame.draw.rect(s, _darken(base, 15), field)
    # bevel edges of coffering
    pygame.draw.lines(s, dark, False, [(m, BS-m), (m, m), (BS-m, m)], 2)
    pygame.draw.lines(s, hi,   False, [(m, BS-m), (BS-m, BS-m), (BS-m, m)], 2)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _marble(base, veins=3):
    """Marble floor tile with diagonal veins."""
    import random as _r
    _r.seed(hash(base))
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 50)
    for _ in range(veins):
        x1 = _r.randint(0, BS)
        y1 = _r.randint(0, BS // 2)
        x2 = x1 + _r.randint(-BS // 2, BS // 2)
        y2 = y1 + _r.randint(BS // 3, BS)
        pygame.draw.line(s, dark, (x1, y1), (x2, y2), 1)
    pygame.draw.rect(s, _darken(base, 30), (0, 0, BS, BS), 1)
    return s


def _slate_tile(base):
    """Slate roof courses."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 30)
    hi   = _lighter(base, 20)
    course_h = BS // 5
    for i in range(5):
        y = i * course_h
        shift = (BS // 4) if i % 2 else 0
        # course overlap shadow
        pygame.draw.line(s, dark, (0, y), (BS, y), 1)
        pygame.draw.line(s, hi,   (0, y + 1), (BS, y + 1), 1)
        # vertical joint
        jx = (BS // 2 + shift) % BS
        pygame.draw.line(s, dark, (jx, y), (jx, y + course_h), 1)
    pygame.draw.rect(s, _darken(base, 20), (0, 0, BS, BS), 1)
    return s


def _clay_tile(base):
    """Overlapping clay/pantile courses."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 20)
    th = BS // 4  # tile height
    for row in range(4):
        y = row * th
        shift = BS // 4 if row % 2 else 0
        for col in range(-1, 3):
            tx = col * (BS // 2) + shift
            # curved pantile shape using ellipses
            r = pygame.Rect(tx, y, BS // 2, th + 2)
            pygame.draw.arc(s, _lighter(base, 15), r, 0, 3.14159, th // 2)
            pygame.draw.arc(s, dark, r, 3.14159, 6.28318, 2)
        pygame.draw.line(s, dark, (0, y), (BS, y), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _door_panel(base, n_panels=6, glazed=False):
    """Panelled door face."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 30)
    pw = BS - 8
    ph = (BS - 8) // n_panels - 2
    for i in range(n_panels):
        y = 4 + i * (ph + 2)
        if glazed and i < n_panels // 2:
            # upper glazing
            glass_c = (190, 210, 220)
            pygame.draw.rect(s, glass_c, (4, y, pw, ph))
            pygame.draw.line(s, dark, (4 + pw // 2, y), (4 + pw // 2, y + ph), 1)
        else:
            inner = (6, y + 2, pw - 4, ph - 4)
            pygame.draw.rect(s, _lighter(base, 10), inner)
        pygame.draw.lines(s, hi,   False,
                          [(4, y + ph), (4, y), (4 + pw, y)], 1)
        pygame.draw.lines(s, dark, False,
                          [(4, y + ph), (4 + pw, y + ph), (4 + pw, y)], 1)
    # door frame
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 2)
    return s


def _window_frame(base, arch=None):
    """Window frame with glazing bar grid."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    glass = (185, 210, 225)
    dark  = _darken(base, 40)
    m = 3
    # glazing area
    if arch == "pointed":
        pts = [(m, BS // 2), (BS // 2, m), (BS - m, BS // 2), (BS - m, BS - m), (m, BS - m)]
        pygame.draw.polygon(s, glass, pts)
    elif arch == "round":
        pygame.draw.rect(s, glass, (m, BS // 3, BS - 2 * m, BS - BS // 3 - m))
        pygame.draw.ellipse(s, glass, (m, m, BS - 2 * m, BS * 2 // 3))
    else:
        pygame.draw.rect(s, glass, (m, m, BS - 2 * m, BS - 2 * m))
    # glazing bars
    pygame.draw.line(s, dark, (BS // 2, m), (BS // 2, BS - m), 1)
    pygame.draw.line(s, dark, (m, BS // 2), (BS - m, BS // 2), 1)
    # frame border
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 2)
    return s


def _iron_railing(base=(52, 50, 48)):
    """Ornate cast iron railing with scroll tops."""
    s = pygame.Surface((BS, BS))
    s.fill((115, 140, 80))  # hedge/garden backdrop (tinted bg)
    dark = _darken(base, 15)
    hi   = _lighter(base, 25)
    # rails
    pygame.draw.rect(s, base, (0, 3, BS, 3))
    pygame.draw.rect(s, base, (0, BS - 6, BS, 3))
    for x in range(2, BS, 7):
        # picket
        pygame.draw.rect(s, base, (x, 6, 3, BS - 10))
        # scroll top circle
        pygame.draw.circle(s, hi, (x + 1, 5), 2)
        pygame.draw.circle(s, dark, (x + 1, 5), 2, 1)
    return s


def _porch_column_art(base):
    """White turned porch column with capital & base."""
    s = pygame.Surface((BS, BS))
    s.fill((0, 0, 0, 0) if hasattr(s, 'set_alpha') else (200, 220, 200))
    s.fill(base)
    dark = _darken(base, 35)
    hi   = _lighter(base, 40)
    cx = BS // 2
    # base block
    pygame.draw.rect(s, _darken(base, 20), (BS // 4 - 2, BS - 6, BS // 2 + 4, 6))
    # shaft
    pygame.draw.rect(s, base, (cx - 5, 6, 10, BS - 12))
    pygame.draw.line(s, hi,   (cx - 3, 6), (cx - 3, BS - 6), 1)
    pygame.draw.line(s, dark, (cx + 3, 6), (cx + 3, BS - 6), 1)
    # capital block
    pygame.draw.rect(s, _darken(base, 15), (BS // 4 - 2, 0, BS // 2 + 4, 6))
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _spindle_rail(base):
    """Turned spindle rail section."""
    s = pygame.Surface((BS, BS))
    s.fill(_lighter(base, 20))
    dark = _darken(base, 40)
    hi   = _lighter(base, 50)
    # top and bottom rail
    pygame.draw.rect(s, _darken(base, 20), (0, 0, BS, 4))
    pygame.draw.rect(s, _darken(base, 20), (0, BS - 4, BS, 4))
    # spindles
    for x in range(3, BS, 8):
        mid = BS // 2
        # turned profile: narrow at top/bottom, wide at center
        pygame.draw.rect(s, base, (x, 4, 3, BS - 8))
        pygame.draw.ellipse(s, hi, (x - 1, mid - 4, 5, 8))
        pygame.draw.ellipse(s, dark, (x - 1, mid - 4, 5, 8), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _porch_floor(base):
    """Hardwood porch floor planks with subtle grain."""
    s = pygame.Surface((BS, BS))
    ph = BS // 5
    for i in range(5):
        c = _lighter(base, 6) if i % 2 == 0 else _darken(base, 6)
        pygame.draw.rect(s, c, (0, i * ph, BS, ph - 1))
        # grain line
        pygame.draw.line(s, _darken(c, 20), (0, i * ph + ph // 2),
                         (BS, i * ph + ph // 2), 1)
    pygame.draw.rect(s, _darken(base, 35), (0, 0, BS, BS), 1)
    return s


def _river_rock(base):
    """Rounded river stone wall."""
    import random as _r
    _r.seed(hash(base) ^ 12345)
    s = pygame.Surface((BS, BS))
    s.fill(_darken(base, 25))
    for _ in range(12):
        rx = _r.randint(2, BS - 8)
        ry = _r.randint(2, BS - 6)
        rw = _r.randint(6, 12)
        rh = _r.randint(4, 8)
        c = _r.choice([_lighter(base, 20), base, _darken(base, 20)])
        pygame.draw.ellipse(s, c, (rx, ry, rw, rh))
        pygame.draw.ellipse(s, _darken(c, 25), (rx, ry, rw, rh), 1)
    pygame.draw.rect(s, _darken(base, 40), (0, 0, BS, BS), 1)
    return s


def _flagstone(base):
    """Irregular flagstone floor."""
    s = pygame.Surface((BS, BS))
    s.fill(_darken(base, 30))
    mortar = _darken(base, 40)
    stones = [
        (1, 1, BS // 2 - 2, BS // 2 - 1),
        (BS // 2 + 1, 1, BS // 2 - 2, BS // 3 - 1),
        (BS // 2 + 1, BS // 3 + 1, BS // 2 - 2, BS // 2 - 1),
        (1, BS // 2 + 1, BS // 3 - 1, BS // 2 - 2),
        (BS // 3 + 1, BS // 2 + 1, BS - BS // 3 - 2, BS // 2 - 2),
    ]
    for rect in stones:
        c = _lighter(base, 8) if stones.index(rect) % 2 == 0 else base
        pygame.draw.rect(s, c, rect)
        pygame.draw.rect(s, mortar, rect, 1)
    pygame.draw.rect(s, mortar, (0, 0, BS, BS), 1)
    return s


def _gingerbread(base):
    """Elaborate scrollwork trim with pierced cutouts."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 45)
    hi   = _lighter(base, 35)
    # horizontal board
    pygame.draw.rect(s, _darken(base, 10), (0, 0, BS, BS // 3))
    # scrollwork arches along bottom
    arch_w = BS // 4
    for i in range(4):
        cx = i * arch_w + arch_w // 2
        rect = pygame.Rect(cx - arch_w // 2 + 1, BS // 3, arch_w - 2, arch_w)
        pygame.draw.arc(s, dark, rect, 0, 3.14159, 2)
        # circle cutout
        pygame.draw.circle(s, hi, (cx, BS // 3 + arch_w // 3), 3)
        pygame.draw.circle(s, dark, (cx, BS // 3 + arch_w // 3), 3, 1)
    # drop pendants
    for i in range(4):
        px = i * arch_w + arch_w // 2
        py = BS - 4
        pygame.draw.circle(s, _darken(base, 20), (px, py), 3)
        pygame.draw.circle(s, dark, (px, py), 3, 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _prairie_glass(base):
    """Prairie-style geometric grid glass (Frank Lloyd Wright influence)."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    lead = (50, 48, 45)
    # outer border
    pygame.draw.rect(s, lead, (0, 0, BS, BS), 2)
    # inner geometric grid: 3x3 cells
    cell = BS // 4
    for i in range(1, 4):
        pygame.draw.line(s, lead, (i * cell, 0), (i * cell, BS), 1)
        pygame.draw.line(s, lead, (0, i * cell), (BS, i * cell), 1)
    # center accent square
    m = BS // 3
    pygame.draw.rect(s, _darken(base, 20), (m, m, BS - 2 * m, BS - 2 * m), 2)
    return s


def _chimney_stack(base):
    """Brick chimney stack pattern (staggered courses, compact)."""
    s = _brick_pattern(base, mortar=(195, 185, 175))
    # smoke-darkened top edge
    top_col = _darken(base, 45)
    pygame.draw.rect(s, top_col, (0, 0, BS, 4))
    return s


def _conservatory_glass(base):
    """Curved conservatory glass panel with iron frame."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    frame = (80, 90, 95)
    # curved bar pattern
    for x in range(0, BS + 1, BS // 4):
        pygame.draw.line(s, frame, (x, 0), (x, BS), 2)
    # arc at top
    pygame.draw.arc(s, frame, (0, 0, BS, BS), 0, 3.14159, 2)
    pygame.draw.rect(s, frame, (0, 0, BS, BS), 2)
    return s


def _rusticated_stone(base):
    """Deeply channeled rusticated stone blocks."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark   = _darken(base, 50)
    groove = _darken(base, 70)
    hi     = _lighter(base, 20)
    # horizontal channels
    for y in range(0, BS, BS // 3):
        pygame.draw.rect(s, groove, (0, y, BS, 2))
        pygame.draw.rect(s, hi,    (0, y + 2, BS, 1))
    # vertical joint midway
    pygame.draw.rect(s, groove, (BS // 2, 0, 2, BS))
    # rough face texture
    pygame.draw.rect(s, dark, (2, 4, 8, 6))
    pygame.draw.rect(s, dark, (16, 10, 6, 8))
    pygame.draw.rect(s, dark, (8, 18, 10, 5))
    pygame.draw.rect(s, dark, (20, 22, 7, 5))
    pygame.draw.rect(s, _darken(base, 30), (0, 0, BS, BS), 1)
    return s


def _ashlar_stone(base):
    """Smooth ashlar stone with fine drafted margins."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 35)
    hi   = _lighter(base, 20)
    # coursed horizontal joints
    course_h = BS // 3
    for y in range(0, BS, course_h):
        pygame.draw.line(s, dark, (0, y), (BS, y), 1)
    # drafted margin on each block
    m = 2
    for row in range(3):
        y0 = row * course_h
        mid_y = y0 + course_h // 2
        w2 = BS if row % 2 == 0 else BS // 2
        for bx in range(0, BS, w2):
            pygame.draw.rect(s, _darken(base, 15), (bx + m, y0 + m, w2 - 2*m, course_h - 2*m))
            pygame.draw.rect(s, dark, (bx + m, y0 + m, w2 - 2*m, course_h - 2*m), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


# ── Main builder ───────────────────────────────────────────────────────────────

def build_victorian_surfs():
    surfs = {}

    def _add(bid, surf):
        surfs[bid] = surf

    # ── Exterior Siding ────────────────────────────────────────────────────────
    for bid in (FISH_SCALE_SHINGLE, FISH_SCALE_SHINGLE_DARK, FISH_SCALE_SHINGLE_BLUE):
        _add(bid, _fish_scale(BLOCKS[bid]["color"]))
    for bid in (CLAPBOARD_SIDING, CLAPBOARD_SIDING_DARK, DROP_SIDING, SHIPLAP_SIDING,
                SHIPLAP_INTERIOR):
        _add(bid, _wood_plank_h(BLOCKS[bid]["color"], n_planks=5))
    for bid in (BOARD_AND_BATTEN_SIDING,):
        _add(bid, _wood_plank_v(BLOCKS[bid]["color"], n_planks=5))
    _add(HALF_TIMBERING_PANEL, _raised_panel(BLOCKS[HALF_TIMBERING_PANEL]["color"]))
    _add(PEBBLEDASH_RENDER,    _river_rock(BLOCKS[PEBBLEDASH_RENDER]["color"]))
    _add(ROUGHCAST_RENDER,     _river_rock(BLOCKS[ROUGHCAST_RENDER]["color"]))

    # ── Roof ──────────────────────────────────────────────────────────────────
    for bid in (SLATE_ROOF_TILE, SLATE_ROOF_TILE_DARK, MANSARD_SLATE_PANEL,
                JERKINHEAD_GABLE, BAY_WINDOW_ROOF, TURRET_CAP_BLOCK,
                OCTAGONAL_TURRET_BLOCK, SHED_DORMER_BLOCK):
        _add(bid, _slate_tile(BLOCKS[bid]["color"]))
    for bid in (CLAY_ROOF_TILE, CLAY_ROOF_TILE_GREEN, IMBREX_ROOF_TILE,
                DECORATED_RIDGE_TILE, CHIMNEY_POT):
        _add(bid, _clay_tile(BLOCKS[bid]["color"]))

    # ── Brick & Masonry ───────────────────────────────────────────────────────
    for bid in (PRESSED_BRICK, PRESSED_BRICK_BUFF, GAUGED_BRICK, RUBBED_BRICK,
                VITRIFIED_BRICK, POLYCHROME_BRICK_RED, POLYCHROME_BRICK_BLUE,
                POLYCHROME_BRICK_CREAM, CHIMNEY_STACK_BLOCK, BRICK_GARDEN_PIER,
                STABLE_WALL_PANEL, LOW_GARDEN_WALL, BELL_TOWER_BLOCK, CLINKER_BRICK,
                AIR_BRICK):
        _add(bid, _brick_pattern(BLOCKS[bid]["color"]))
    _add(CHIMNEY_STACK_BLOCK, _chimney_stack(BLOCKS[CHIMNEY_STACK_BLOCK]["color"]))
    for bid in (RUSTICATED_STONE,):
        _add(bid, _rusticated_stone(BLOCKS[bid]["color"]))
    for bid in (ASHLAR_STONE_BLOCK, VOUSSOIR_BLOCK, QUOIN_BLOCK, PLINTH_BLOCK,
                STRING_COURSE_BLOCK):
        _add(bid, _ashlar_stone(BLOCKS[bid]["color"]))
    for bid in (ROCK_FACED_STONE, FLORENTINE_STONE, VERMICULATED_STONE):
        _add(bid, _rusticated_stone(BLOCKS[bid]["color"]))

    # ── Columns ───────────────────────────────────────────────────────────────
    for bid in (IONIC_COLUMN, CORINTHIAN_COLUMN_SHAFT):
        _add(bid, _column_shaft(BLOCKS[bid]["color"], fluted=True))
    for bid in (DORIC_COLUMN, ENGAGED_COLUMN_BLOCK, PILASTER_BLOCK, FLUTED_PANEL,
                FLUTED_INTERIOR_PILASTER):
        _add(bid, _column_shaft(BLOCKS[bid]["color"], fluted=False))
    _add(PORCH_COLUMN,       _porch_column_art(BLOCKS[PORCH_COLUMN]["color"]))
    _add(ORNATE_PORCH_COLUMN, _porch_column_art(BLOCKS[ORNATE_PORCH_COLUMN]["color"]))
    _add(TAPERED_PORCH_POST,  _porch_column_art(BLOCKS[TAPERED_PORCH_POST]["color"]))
    _add(RIVER_ROCK_COLUMN,   _river_rock(BLOCKS[RIVER_ROCK_COLUMN]["color"]))
    _add(COBBLESTONE_PIER,    _river_rock(BLOCKS[COBBLESTONE_PIER]["color"]))

    # ── Stained Glass ─────────────────────────────────────────────────────────
    _add(STAINED_GLASS_RED,    _stained_glass(BLOCKS[STAINED_GLASS_RED]["color"]))
    _add(STAINED_GLASS_BLUE,   _stained_glass(BLOCKS[STAINED_GLASS_BLUE]["color"]))
    _add(STAINED_GLASS_AMBER,  _stained_glass(BLOCKS[STAINED_GLASS_AMBER]["color"]))
    _add(STAINED_GLASS_GREEN,  _stained_glass(BLOCKS[STAINED_GLASS_GREEN]["color"]))
    _add(STAINED_GLASS_PURPLE, _stained_glass(BLOCKS[STAINED_GLASS_PURPLE]["color"]))
    _add(LEADED_LIGHT_PANEL,   _leaded_grid(BLOCKS[LEADED_LIGHT_PANEL]["color"]))
    _add(QUARRY_GLASS_PANEL,   _diamond_leaded(BLOCKS[QUARRY_GLASS_PANEL]["color"]))
    _add(FROSTED_GLASS_PANEL,  _leaded_grid(BLOCKS[FROSTED_GLASS_PANEL]["color"], cell=6))
    _add(ETCHED_GLASS_PANEL,   _leaded_grid(BLOCKS[ETCHED_GLASS_PANEL]["color"], cell=10))
    _add(COLOURED_BORDER_GLASS, _leaded_grid(BLOCKS[COLOURED_BORDER_GLASS]["color"]))
    _add(PRAIRIE_GRID_GLASS,    _prairie_glass(BLOCKS[PRAIRIE_GRID_GLASS]["color"]))
    _add(CONSERVATORY_GLASS_PANEL, _conservatory_glass(BLOCKS[CONSERVATORY_GLASS_PANEL]["color"]))

    # ── Windows ───────────────────────────────────────────────────────────────
    for bid in (SASH_WINDOW_FRAME, CASEMENT_WINDOW_FRAME, TRANSOM_WINDOW_FRAME,
                PALLADIAN_WINDOW_FRAME, BAY_WINDOW_FRAME, ORIEL_WINDOW_FRAME,
                VENETIAN_WINDOW_FRAME):
        _add(bid, _window_frame(BLOCKS[bid]["color"]))
    _add(GOTHIC_ARCH_WINDOW, _window_frame(BLOCKS[GOTHIC_ARCH_WINDOW]["color"], arch="pointed"))
    _add(ROUND_ARCH_WINDOW,  _window_frame(BLOCKS[ROUND_ARCH_WINDOW]["color"],  arch="round"))
    _add(FANLIGHT_FRAME,     _window_frame(BLOCKS[FANLIGHT_FRAME]["color"],     arch="round"))

    # ── Doors ─────────────────────────────────────────────────────────────────
    _add(PANELLED_DOOR_BLOCK,     _door_panel(BLOCKS[PANELLED_DOOR_BLOCK]["color"], n_panels=6))
    _add(GLAZED_DOOR_BLOCK,       _door_panel(BLOCKS[GLAZED_DOOR_BLOCK]["color"], n_panels=4, glazed=True))
    _add(DOUBLE_DOOR_BLOCK,       _door_panel(BLOCKS[DOUBLE_DOOR_BLOCK]["color"], n_panels=4))
    _add(DUTCH_DOOR_BLOCK,        _door_panel(BLOCKS[DUTCH_DOOR_BLOCK]["color"], n_panels=3))
    _add(SLIDING_POCKET_DOOR_BLOCK, _door_panel(BLOCKS[SLIDING_POCKET_DOOR_BLOCK]["color"], n_panels=3))
    _add(SERVICE_DOOR_BLOCK,      _door_panel(BLOCKS[SERVICE_DOOR_BLOCK]["color"], n_panels=4))
    _add(PANTRY_DOOR_BLOCK,       _door_panel(BLOCKS[PANTRY_DOOR_BLOCK]["color"], n_panels=4))
    _add(CARRIAGE_HOUSE_DOOR,     _door_panel(BLOCKS[CARRIAGE_HOUSE_DOOR]["color"], n_panels=3))
    _add(STORM_DOOR_BLOCK,        _window_frame(BLOCKS[STORM_DOOR_BLOCK]["color"]))

    # ── Porch & Trim ──────────────────────────────────────────────────────────
    _add(SPINDLE_RAIL,         _spindle_rail(BLOCKS[SPINDLE_RAIL]["color"]))
    _add(PORCH_BALUSTRADE,     _spindle_rail(BLOCKS[PORCH_BALUSTRADE]["color"]))
    _add(BALUSTER_BLOCK,       _spindle_rail(BLOCKS[BALUSTER_BLOCK]["color"]))
    _add(LATTICE_PANEL,        _lattice(BLOCKS[LATTICE_PANEL]["color"]))
    _add(WISTERIA_TRELLIS,     _lattice(BLOCKS[WISTERIA_TRELLIS]["color"]))
    _add(GINGERBREAD_TRIM,     _gingerbread(BLOCKS[GINGERBREAD_TRIM]["color"]))
    _add(JIGSAW_TRIM_PANEL,    _gingerbread(BLOCKS[JIGSAW_TRIM_PANEL]["color"]))
    _add(PORCH_FLOOR_BOARD,    _porch_floor(BLOCKS[PORCH_FLOOR_BOARD]["color"]))
    _add(BALCONY_DECK_BOARD,   _porch_floor(BLOCKS[BALCONY_DECK_BOARD]["color"]))
    _add(PORCH_CEILING_BOARD,  _wood_plank_v(BLOCKS[PORCH_CEILING_BOARD]["color"], n_planks=6))

    # ── Interior Wall & Trim ──────────────────────────────────────────────────
    _add(BEADBOARD_PANEL,      _beadboard(BLOCKS[BEADBOARD_PANEL]["color"]))
    _add(WAINSCOT_PANEL_OAK,   _raised_panel(BLOCKS[WAINSCOT_PANEL_OAK]["color"]))
    _add(WAINSCOT_PANEL_DARK,  _raised_panel(BLOCKS[WAINSCOT_PANEL_DARK]["color"]))
    _add(RAISED_PANEL_WALL,    _raised_panel(BLOCKS[RAISED_PANEL_WALL]["color"]))
    for bid in (TONGUE_GROOVE_PLANK, WIDE_BOARD_PANELLING):
        _add(bid, _wood_plank_v(BLOCKS[bid]["color"], n_planks=4))
    _add(COFFERED_CEILING_PANEL,       _cofferred(BLOCKS[COFFERED_CEILING_PANEL]["color"]))
    _add(EMBOSSED_TIN_CEILING_SILVER,  _tin_ceiling(BLOCKS[EMBOSSED_TIN_CEILING_SILVER]["color"]))
    _add(EMBOSSED_TIN_CEILING_GOLD,    _tin_ceiling(BLOCKS[EMBOSSED_TIN_CEILING_GOLD]["color"], (220, 200, 120)))
    for bid in (OAK_BOOKCASE, BUTLER_PANTRY_SHELF, DRESSER_BACK_PANEL,
                CRAFTSMAN_FRIEZE_BOARD, CRAFTSMAN_BARGEBOARD):
        _add(bid, _wood_plank_v(BLOCKS[bid]["color"], n_planks=5))

    # ── Floors ────────────────────────────────────────────────────────────────
    _add(ENCAUSTIC_FLOOR_TILE_RED,   _encaustic_tile(BLOCKS[ENCAUSTIC_FLOOR_TILE_RED]["color"],   (230, 220, 200)))
    _add(ENCAUSTIC_FLOOR_TILE_BLUE,  _encaustic_tile(BLOCKS[ENCAUSTIC_FLOOR_TILE_BLUE]["color"],  (230, 220, 200)))
    _add(ENCAUSTIC_FLOOR_TILE_GREEN, _encaustic_tile(BLOCKS[ENCAUSTIC_FLOOR_TILE_GREEN]["color"], (230, 220, 200)))
    _add(ENCAUSTIC_BORDER_TILE,      _encaustic_tile(BLOCKS[ENCAUSTIC_BORDER_TILE]["color"],      (180, 60, 48)))
    _add(GEOMETRIC_MOSAIC_FLOOR,     _mosaic([(185, 75, 55), (230, 220, 200), (68, 85, 148), (230, 220, 200)]))
    _add(PARQUET_FLOOR_HERRINGBONE,  _herringbone(BLOCKS[PARQUET_FLOOR_HERRINGBONE]["color"]))
    for bid in (PARQUET_FLOOR_BASKET, PARQUET_FLOOR_STRIP, HARDWOOD_STAIR_TREAD,
                LANDING_BOARD, OPEN_RISER_STAIR_STEP):
        _add(bid, _wood_plank_h(BLOCKS[bid]["color"], n_planks=4))
    _add(MARBLE_FLOOR_TILE,       _marble(BLOCKS[MARBLE_FLOOR_TILE]["color"]))
    _add(MARBLE_FLOOR_TILE_BLACK, _marble(BLOCKS[MARBLE_FLOOR_TILE_BLACK]["color"], veins=2))
    _add(MARBLE_THRESHOLD,        _marble(BLOCKS[MARBLE_THRESHOLD]["color"]))
    _add(FLAGSTONE_FLOOR,         _flagstone(BLOCKS[FLAGSTONE_FLOOR]["color"]))
    _add(CELLAR_STONE_FLOOR,      _flagstone(BLOCKS[CELLAR_STONE_FLOOR]["color"]))

    # ── Garden Iron ───────────────────────────────────────────────────────────
    _add(WROUGHT_IRON_FENCE_PANEL, _wrought_iron_fence(BLOCKS[WROUGHT_IRON_FENCE_PANEL]["color"]))
    _add(WROUGHT_IRON_GATE,        _wrought_iron_fence(BLOCKS[WROUGHT_IRON_GATE]["color"]))
    _add(CAST_IRON_RAILING_PANEL,  _iron_railing(BLOCKS[CAST_IRON_RAILING_PANEL]["color"]))
    _add(TOPIARY_FRAME,            _iron_railing(BLOCKS[TOPIARY_FRAME]["color"]))
    _add(ROSE_ARCH_FRAME,          _iron_railing(BLOCKS[ROSE_ARCH_FRAME]["color"]))

    # ── Masonry Garden ────────────────────────────────────────────────────────
    for bid in (GARDEN_WALL_COPING, STONE_GARDEN_BALUSTRADE, STONE_GARDEN_STEPS,
                BATTERED_RETAINING_WALL, AREA_STEPS_BLOCK, MOUNTING_BLOCK,
                PORCH_ENTRY_STEPS, STONE_GARDEN_PIER):
        _add(bid, _ashlar_stone(BLOCKS[bid]["color"]))
    _add(RIVER_ROCK_BLOCK, _river_rock(BLOCKS[RIVER_ROCK_BLOCK]["color"]))
    _add(ARTS_AND_CRAFTS_TILE, _encaustic_tile(BLOCKS[ARTS_AND_CRAFTS_TILE]["color"], (120, 95, 65)))

    # ── Previously fallback-only blocks ───────────────────────────────────────

    # Terracotta tiles
    for bid in (TERRACOTTA_CLADDING_TILE, TERRACOTTA_BLOCK, TERRACOTTA_PANEL,
                BUFF_TERRACOTTA, TERRACOTTA_FLOOR_TILE, HEARTH_TILE):
        _add(bid, _terracotta_tile(BLOCKS[bid]["color"]))
    _add(FAIENCE_TILE_PANEL, _faience_tile(BLOCKS[FAIENCE_TILE_PANEL]["color"]))
    _add(TILE_THRESHOLD_STRIP, _terracotta_tile(BLOCKS[TILE_THRESHOLD_STRIP]["color"]))

    # Metal & pressed surfaces
    _add(PRESSED_METAL_PANEL,  _embossed_metal(BLOCKS[PRESSED_METAL_PANEL]["color"]))
    _add(IRON_CRESTING_RAIL,   _cresting_rail(BLOCKS[IRON_CRESTING_RAIL]["color"]))
    _add(CAST_IRON_GRATE_FRONT, _iron_grate(BLOCKS[CAST_IRON_GRATE_FRONT]["color"]))
    _add(CAST_IRON_FIREBACK,    _iron_fireback(BLOCKS[CAST_IRON_FIREBACK]["color"]))
    _add(CAST_IRON_GUTTER,      _half_round_gutter(BLOCKS[CAST_IRON_GUTTER]["color"]))
    _add(CAST_IRON_DOWNPIPE,    _round_pipe(BLOCKS[CAST_IRON_DOWNPIPE]["color"]))
    _add(HOPPER_HEAD_BLOCK,     _hopper_head(BLOCKS[HOPPER_HEAD_BLOCK]["color"]))
    _add(COAL_HOLE_COVER,       _coal_hole(BLOCKS[COAL_HOLE_COVER]["color"]))
    _add(BOOT_SCRAPER_BLOCK,    _boot_scraper(BLOCKS[BOOT_SCRAPER_BLOCK]["color"]))
    _add(DOOR_KNOCKER_PLATE,    _door_knocker(BLOCKS[DOOR_KNOCKER_PLATE]["color"]))
    _add(LETTERBOX_PANEL,       _letterbox(BLOCKS[LETTERBOX_PANEL]["color"]))
    _add(STRAP_HINGE_PANEL,     _strap_hinge(BLOCKS[STRAP_HINGE_PANEL]["color"]))
    _add(BASEMENT_WINDOW_WELL,  _window_well(BLOCKS[BASEMENT_WINDOW_WELL]["color"]))
    _add(DAMP_COURSE_BLOCK,     _damp_course(BLOCKS[DAMP_COURSE_BLOCK]["color"]))
    _add(CONSERVATORY_IRON_FRAME, _iron_conservatory_frame(BLOCKS[CONSERVATORY_IRON_FRAME]["color"]))
    _add(VICTORIAN_GREENHOUSE_FRAME, _iron_conservatory_frame(BLOCKS[VICTORIAN_GREENHOUSE_FRAME]["color"]))

    # Plaster & render panels
    _add(INCISED_RENDER_PANEL,  _incised_render(BLOCKS[INCISED_RENDER_PANEL]["color"]))
    _add(PARGETING_PANEL,       _pargeting(BLOCKS[PARGETING_PANEL]["color"]))
    _add(STUCCO_BAND,           _stucco_band(BLOCKS[STUCCO_BAND]["color"]))
    _add(LINCRUSTA_PANEL,       _lincrusta(BLOCKS[LINCRUSTA_PANEL]["color"]))
    _add(ANAGLYPTA_PANEL,       _anaglypta(BLOCKS[ANAGLYPTA_PANEL]["color"]))
    _add(SMOOTH_PLASTER_PANEL,  _smooth_plaster(BLOCKS[SMOOTH_PLASTER_PANEL]["color"]))
    _add(PLASTER_CEILING_ROSE,  _ceiling_rose(BLOCKS[PLASTER_CEILING_ROSE]["color"]))
    _add(COVED_CORNICE,         _coved_cornice_art(BLOCKS[COVED_CORNICE]["color"]))
    _add(FLAUNCHING_BLOCK,      _flaunching(BLOCKS[FLAUNCHING_BLOCK]["color"]))
    _add(DOVECOTE_BLOCK,        _smooth_plaster(BLOCKS[DOVECOTE_BLOCK]["color"]))

    # Decorative wood trim & mouldings
    _add(VERGEBOARD,            _vergeboard_art(BLOCKS[VERGEBOARD]["color"]))
    _add(DECORATIVE_FRIEZE_PANEL, _frieze_panel(BLOCKS[DECORATIVE_FRIEZE_PANEL]["color"]))
    _add(DENTIL_MOULDING_STRIP, _dentil_strip(BLOCKS[DENTIL_MOULDING_STRIP]["color"]))
    _add(DENTIL_CORNICE,        _dentil_strip(BLOCKS[DENTIL_CORNICE]["color"]))
    _add(EGG_AND_DART_MOULDING, _egg_dart(BLOCKS[EGG_AND_DART_MOULDING]["color"]))
    _add(OVOLO_MOULDING,        _ovolo_moulding(BLOCKS[OVOLO_MOULDING]["color"]))
    _add(CROWN_MOULDING,        _crown_moulding(BLOCKS[CROWN_MOULDING]["color"]))
    _add(DADO_RAIL,             _dado_rail_art(BLOCKS[DADO_RAIL]["color"]))
    _add(PICTURE_RAIL,          _picture_rail_art(BLOCKS[PICTURE_RAIL]["color"]))
    _add(TALL_BASEBOARD,        _baseboard_art(BLOCKS[TALL_BASEBOARD]["color"]))
    _add(DARK_BASEBOARD,        _baseboard_art(BLOCKS[DARK_BASEBOARD]["color"]))
    _add(ARCHITRAVE,            _architrave_art(BLOCKS[ARCHITRAVE]["color"]))
    _add(DORMER_CHEEK,          _rendered_wall(BLOCKS[DORMER_CHEEK]["color"]))
    _add(GABLED_DORMER_FRONT,   _vergeboard_art(BLOCKS[GABLED_DORMER_FRONT]["color"]))

    # Carved stone ornament
    _add(ARCH_KEYSTONE_BLOCK,   _keystone(BLOCKS[ARCH_KEYSTONE_BLOCK]["color"]))
    _add(TYMPANUM_PANEL,        _tympanum(BLOCKS[TYMPANUM_PANEL]["color"]))
    _add(MEDALLION_BLOCK,       _medallion(BLOCKS[MEDALLION_BLOCK]["color"]))
    _add(CARTOUCHE_BLOCK,       _cartouche(BLOCKS[CARTOUCHE_BLOCK]["color"]))
    _add(HERALDIC_PANEL,        _heraldic(BLOCKS[HERALDIC_PANEL]["color"]))
    _add(FINIAL_BLOCK,          _finial(BLOCKS[FINIAL_BLOCK]["color"]))
    _add(CORBEL_BLOCK,          _corbel(BLOCKS[CORBEL_BLOCK]["color"]))
    _add(MODILLION_BLOCK,       _modillion(BLOCKS[MODILLION_BLOCK]["color"]))
    _add(CONSOLE_BRACKET,       _console(BLOCKS[CONSOLE_BRACKET]["color"]))
    _add(COLUMN_CAPITAL,        _column_capital(BLOCKS[COLUMN_CAPITAL]["color"]))
    _add(COLUMN_BASE,           _column_base_art(BLOCKS[COLUMN_BASE]["color"]))
    _add(CRAFTSMAN_COLUMN_CAP,  _column_capital(BLOCKS[CRAFTSMAN_COLUMN_CAP]["color"]))
    _add(FANLIGHT_SURROUND,     _fanlight_surround_art(BLOCKS[FANLIGHT_SURROUND]["color"]))
    _add(PILASTER_DOOR_SURROUND, _pilaster_surround(BLOCKS[PILASTER_DOOR_SURROUND]["color"]))
    _add(HOOD_MOULDING,         _hood_moulding_art(BLOCKS[HOOD_MOULDING]["color"]))
    _add(CHIMNEY_CAP,           _keystone(BLOCKS[CHIMNEY_CAP]["color"]))

    # Wood brackets & beams
    _add(BRACKET_SUPPORT,       _bracket(BLOCKS[BRACKET_SUPPORT]["color"]))
    _add(KNEE_BRACE,            _knee_brace_art(BLOCKS[KNEE_BRACE]["color"]))
    _add(CANTILEVER_BEAM_END,   _beam_end(BLOCKS[CANTILEVER_BEAM_END]["color"]))
    _add(EXPOSED_RAFTER_END,    _beam_end(BLOCKS[EXPOSED_RAFTER_END]["color"]))
    _add(CRAFTSMAN_BEAM_END,    _beam_end(BLOCKS[CRAFTSMAN_BEAM_END]["color"]))
    _add(CRAFTSMAN_TRIM_STRIP,  _trim_strip(BLOCKS[CRAFTSMAN_TRIM_STRIP]["color"]))
    _add(PERGOLA_POST,          _pergola_post_art(BLOCKS[PERGOLA_POST]["color"]))
    _add(PERGOLA_BEAM,          _wood_plank_h(BLOCKS[PERGOLA_BEAM]["color"], n_planks=3))
    _add(PERGOLA_SLAT,          _wood_plank_h(BLOCKS[PERGOLA_SLAT]["color"], n_planks=6))
    _add(PORTE_COCHERE_BEAM,    _wood_plank_h(BLOCKS[PORTE_COCHERE_BEAM]["color"], n_planks=3))
    _add(PORCH_SWING_BRACKET,   _bracket(BLOCKS[PORCH_SWING_BRACKET]["color"]))
    _add(GAZEBO_BEAM,           _wood_plank_h(BLOCKS[GAZEBO_BEAM]["color"], n_planks=3))
    _add(GARDEN_PAVILION_POST,  _pergola_post_art(BLOCKS[GARDEN_PAVILION_POST]["color"]))

    # Newel & stair
    _add(NEWEL_POST,            _newel_post_art(BLOCKS[NEWEL_POST]["color"]))
    _add(PORCH_CORNICE,         _crown_moulding(BLOCKS[PORCH_CORNICE]["color"]))
    _add(VERANDA_BRACKET,       _bracket(BLOCKS[VERANDA_BRACKET]["color"]))
    _add(SCREEN_PORCH_PANEL,    _screen_panel(BLOCKS[SCREEN_PORCH_PANEL]["color"]))
    _add(PAINTED_STAIR_RISER,   _stair_riser(BLOCKS[PAINTED_STAIR_RISER]["color"]))
    _add(BRASS_STAIR_NOSING,    _stair_nosing(BLOCKS[BRASS_STAIR_NOSING]["color"]))

    # Fireplace elements
    _add(FIREPLACE_MANTEL,      _mantelpiece(BLOCKS[FIREPLACE_MANTEL]["color"]))
    _add(FIREPLACE_SURROUND_TILE, _fireplace_surround(BLOCKS[FIREPLACE_SURROUND_TILE]["color"]))
    _add(FIREPLACE_OVERMANTEL,  _overmantel(BLOCKS[FIREPLACE_OVERMANTEL]["color"]))
    _add(INGLENOOK_SIDE_WALL,   _inglenook_wall(BLOCKS[INGLENOOK_SIDE_WALL]["color"]))
    _add(INGLENOOK_BENCH,       _bench_art(BLOCKS[INGLENOOK_BENCH]["color"]))

    # Built-in furniture
    _add(PAINTED_BOOKCASE,      _bookcase_art(BLOCKS[PAINTED_BOOKCASE]["color"]))
    _add(WINDOW_SEAT_BOX,       _window_seat(BLOCKS[WINDOW_SEAT_BOX]["color"]))
    _add(ALCOVE_SHELF,          _shelf_art(BLOCKS[ALCOVE_SHELF]["color"]))
    _add(CHINA_CABINET_BLOCK,   _cabinet_art(BLOCKS[CHINA_CABINET_BLOCK]["color"]))
    _add(BUILT_IN_WARDROBE_PANEL, _wardrobe_art(BLOCKS[BUILT_IN_WARDROBE_PANEL]["color"]))
    _add(HIGH_BACK_SETTLE,      _settle_art(BLOCKS[HIGH_BACK_SETTLE]["color"]))
    _add(PLATE_RACK,            _plate_rack_art(BLOCKS[PLATE_RACK]["color"]))
    _add(DUMBWAITER_SHAFT_PANEL, _dumbwaiter(BLOCKS[DUMBWAITER_SHAFT_PANEL]["color"]))

    # Garden structures & utility
    _add(GARDEN_URN_PEDESTAL,   _urn_pedestal(BLOCKS[GARDEN_URN_PEDESTAL]["color"]))
    _add(SUNDIAL_PEDESTAL,      _sundial_pedestal(BLOCKS[SUNDIAL_PEDESTAL]["color"]))
    _add(ICE_HOUSE_BLOCK,       _ashlar_stone(BLOCKS[ICE_HOUSE_BLOCK]["color"]))
    _add(GARDEN_TOOL_STORE_PANEL, _wood_plank_v(BLOCKS[GARDEN_TOOL_STORE_PANEL]["color"], n_planks=4))
    _add(SUMMERHOUSE_PANEL,     _rendered_wall(BLOCKS[SUMMERHOUSE_PANEL]["color"]))
    _add(HA_HA_WALL_BLOCK,      _battered_wall(BLOCKS[HA_HA_WALL_BLOCK]["color"]))
    _add(COAL_CELLAR_BLOCK,     _coal_cellar(BLOCKS[COAL_CELLAR_BLOCK]["color"]))

    return surfs


# ── Drawing helpers for the 103 previously-fallback blocks ────────────────────

def _terracotta_tile(base):
    """Smooth fired terracotta with subtle glaze sheen."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    hi   = _lighter(base, 28)
    dark = _darken(base, 28)
    # diagonal glaze highlight top-left
    pygame.draw.line(s, hi, (2, 2), (BS - 8, 2), 1)
    pygame.draw.line(s, hi, (2, 3), (2, BS - 8), 1)
    # subtle shadow bottom-right
    pygame.draw.line(s, dark, (BS - 2, 4), (BS - 2, BS - 2), 1)
    pygame.draw.line(s, dark, (4, BS - 2), (BS - 2, BS - 2), 1)
    # thin grout line border
    pygame.draw.rect(s, _darken(base, 40), (0, 0, BS, BS), 2)
    return s


def _faience_tile(base):
    """Glazed faience tile with geometric border motif."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    hi   = _lighter(base, 40)
    dark = _darken(base, 35)
    cream = (235, 228, 210)
    m = 4
    # outer tile border
    pygame.draw.rect(s, cream, (0, 0, BS, BS), m)
    # inner field
    inner = (m, m, BS - 2*m, BS - 2*m)
    pygame.draw.rect(s, base, inner)
    # octagonal inset
    d = 5
    cx, cy = BS // 2, BS // 2
    pts = [(cx, m+d), (BS-m-d, m), (BS-m, m+d),
           (BS-m, BS-m-d), (BS-m-d, BS-m), (m+d, BS-m),
           (m, BS-m-d), (m, m+d), (m+d, m)]
    pygame.draw.polygon(s, cream, pts, 1)
    # center dot
    pygame.draw.circle(s, hi, (cx, cy), 3)
    pygame.draw.circle(s, dark, (cx, cy), 3, 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _embossed_metal(base):
    """Pressed/stamped metal panel with regular embossed grid."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    hi   = _lighter(base, 35)
    dark = _darken(base, 30)
    cell = BS // 4
    for row in range(4):
        for col in range(4):
            x, y = col * cell, row * cell
            # raised diamond in each cell
            cx, cy = x + cell // 2, y + cell // 2
            r = cell // 3
            pts = [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)]
            pygame.draw.polygon(s, hi, pts)
            pygame.draw.polygon(s, dark, pts, 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _cresting_rail(base):
    """Decorative iron ridge cresting with repeating spearhead finials."""
    s = pygame.Surface((BS, BS))
    s.fill(_lighter(base, 60))   # sky/roof backdrop
    dark = _darken(base, 20)
    hi   = _lighter(base, 30)
    # horizontal rail
    pygame.draw.rect(s, base, (0, BS // 2, BS, 4))
    pygame.draw.rect(s, hi,   (0, BS // 2, BS, 1))
    # finials
    for x in range(2, BS, 8):
        h = BS // 2 - 4
        pygame.draw.rect(s, base, (x, h, 3, BS // 2 - h))
        # spear tip
        pts = [(x + 1, h - 6), (x, h), (x + 3, h)]
        pygame.draw.polygon(s, hi,   pts)
        pygame.draw.polygon(s, dark, pts, 1)
        # scroll circle
        pygame.draw.circle(s, hi,   (x + 1, h + 3), 2)
        pygame.draw.circle(s, dark, (x + 1, h + 3), 2, 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _iron_grate(base):
    """Cast iron fireplace grate front with bar pattern."""
    s = pygame.Surface((BS, BS))
    s.fill(_darken(base, 40))   # dark firebox
    hi = _lighter(base, 25)
    # horizontal grate bars
    for y in range(4, BS - 4, 4):
        pygame.draw.rect(s, base, (2, y, BS - 4, 2))
        pygame.draw.line(s, hi, (2, y), (BS - 4, y), 1)
    # vertical side rails
    pygame.draw.rect(s, base, (0, 0, 3, BS))
    pygame.draw.rect(s, base, (BS - 3, 0, 3, BS))
    # frame
    pygame.draw.rect(s, base, (0, 0, BS, BS), 2)
    return s


def _iron_fireback(base):
    """Decorative cast iron fireback with relief panel."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 30)
    hi   = _lighter(base, 20)
    # outer border
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 2)
    # arched top relief
    arc_r = pygame.Rect(4, 3, BS - 8, BS // 2)
    pygame.draw.arc(s, hi, arc_r, 0, 3.14159, 2)
    # stylised urn / vase shape
    cx = BS // 2
    pygame.draw.ellipse(s, hi, (cx - 5, BS // 4, 10, 8))   # urn top
    pygame.draw.rect(s, hi, (cx - 3, BS // 4 + 6, 6, 8))   # urn body
    pygame.draw.ellipse(s, hi, (cx - 6, BS // 4 + 12, 12, 5))  # urn base
    # rosette dots
    for px, py in [(8, 8), (BS - 8, 8), (8, BS - 8), (BS - 8, BS - 8)]:
        pygame.draw.circle(s, hi, (px, py), 3)
        pygame.draw.circle(s, dark, (px, py), 3, 1)
    return s


def _half_round_gutter(base):
    """Cast iron half-round gutter profile viewed face-on."""
    s = pygame.Surface((BS, BS))
    s.fill(_lighter(base, 50))  # wall/sky backdrop
    dark = _darken(base, 25)
    hi   = _lighter(base, 25)
    # gutter profile - horizontal half-pipe
    y0 = BS // 3
    pygame.draw.rect(s, base, (0, y0, BS, BS // 3))
    pygame.draw.arc(s, _darken(base, 40), (0, y0, BS, BS // 3), 3.14159, 6.28318, BS // 6)
    pygame.draw.line(s, hi,   (0, y0), (BS, y0), 2)
    pygame.draw.line(s, dark, (0, y0 + BS // 3), (BS, y0 + BS // 3), 2)
    # bracket screws
    for x in (BS // 4, 3 * BS // 4):
        pygame.draw.circle(s, dark, (x, y0 + BS // 6), 2)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _round_pipe(base):
    """Vertical circular cast iron downpipe."""
    s = pygame.Surface((BS, BS))
    s.fill(_lighter(base, 55))
    dark = _darken(base, 30)
    hi   = _lighter(base, 35)
    cx   = BS // 2
    r    = BS // 5
    # pipe barrel
    pygame.draw.rect(s, base, (cx - r, 0, r * 2, BS))
    # cylindrical shading
    pygame.draw.line(s, hi,   (cx - r + 2, 0), (cx - r + 2, BS), 2)
    pygame.draw.line(s, dark, (cx + r - 3, 0), (cx + r - 3, BS), 2)
    # collar rings
    for y in (BS // 4, BS // 2, 3 * BS // 4):
        pygame.draw.rect(s, dark, (cx - r - 1, y - 2, r * 2 + 2, 4))
        pygame.draw.line(s, hi, (cx - r, y - 1), (cx + r, y - 1), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _hopper_head(base):
    """Bell/hopper-shaped downpipe head."""
    s = pygame.Surface((BS, BS))
    s.fill(_lighter(base, 55))
    dark = _darken(base, 30)
    hi   = _lighter(base, 30)
    # funnel shape
    pts = [(4, 0), (BS - 4, 0), (BS // 2 + 4, BS // 2), (BS // 2 + 4, BS),
           (BS // 2 - 4, BS), (BS // 2 - 4, BS // 2)]
    pygame.draw.polygon(s, base, pts)
    pygame.draw.polygon(s, dark, pts, 1)
    # top opening highlight
    pygame.draw.line(s, hi, (4, 2), (BS - 4, 2), 1)
    # cast rivet dots
    for px in (6, BS - 6):
        pygame.draw.circle(s, dark, (px, 4), 2)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _coal_hole(base):
    """Decorative cast iron coal hole cover with radiating pattern."""
    s = pygame.Surface((BS, BS))
    s.fill(_darken(base, 10))
    hi   = _lighter(base, 30)
    dark = _darken(base, 35)
    cx, cy = BS // 2, BS // 2
    # circular cover
    pygame.draw.circle(s, base,  (cx, cy), BS // 2 - 2)
    pygame.draw.circle(s, dark,  (cx, cy), BS // 2 - 2, 2)
    # radiating spokes
    import math
    for i in range(8):
        a = i * math.pi / 4
        x2 = int(cx + (BS // 2 - 5) * math.cos(a))
        y2 = int(cy + (BS // 2 - 5) * math.sin(a))
        pygame.draw.line(s, hi, (cx, cy), (x2, y2), 1)
    # center hub
    pygame.draw.circle(s, dark, (cx, cy), 4)
    pygame.draw.circle(s, hi,   (cx, cy), 3)
    return s


def _boot_scraper(base):
    """Wrought iron boot scraper with crossbar."""
    s = pygame.Surface((BS, BS))
    s.fill((130, 148, 100))  # stone step backdrop
    dark = _darken(base, 20)
    hi   = _lighter(base, 25)
    # two vertical posts
    pygame.draw.rect(s, base, (4, BS // 2, 4, BS // 2 - 2))
    pygame.draw.rect(s, base, (BS - 8, BS // 2, 4, BS // 2 - 2))
    # scraper bar
    pygame.draw.rect(s, base, (4, BS // 2 - 2, BS - 8, 4))
    pygame.draw.line(s, hi, (4, BS // 2 - 2), (BS - 8, BS // 2 - 2), 1)
    pygame.draw.line(s, dark, (4, BS // 2 + 2), (BS - 8, BS // 2 + 2), 1)
    # scroll tops
    for x in (5, BS - 7):
        pygame.draw.circle(s, hi, (x + 1, BS // 2 - 5), 3)
        pygame.draw.circle(s, dark, (x + 1, BS // 2 - 5), 3, 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _door_knocker(base):
    """Brass door knocker plate with ring."""
    s = pygame.Surface((BS, BS))
    s.fill((80, 58, 38))   # dark door backdrop
    dark = _darken(base, 35)
    hi   = _lighter(base, 45)
    cx, cy = BS // 2, BS // 2
    # backplate
    pygame.draw.rect(s, base, (cx - 6, 4, 12, BS - 8), border_radius=3)
    pygame.draw.rect(s, dark, (cx - 6, 4, 12, BS - 8), 1, border_radius=3)
    # knocker ring
    pygame.draw.circle(s, base, (cx, cy), 6, 2)
    pygame.draw.circle(s, hi,   (cx - 2, cy - 2), 2)
    # pivot boss
    pygame.draw.circle(s, dark, (cx, 8), 3)
    pygame.draw.circle(s, hi,   (cx, 8), 2)
    return s


def _letterbox(base):
    """Brass letterbox plate with slot."""
    s = pygame.Surface((BS, BS))
    s.fill((80, 58, 38))   # door backdrop
    dark = _darken(base, 35)
    hi   = _lighter(base, 40)
    cy   = BS // 2
    # plate
    pygame.draw.rect(s, base, (2, cy - 6, BS - 4, 12), border_radius=2)
    pygame.draw.rect(s, dark, (2, cy - 6, BS - 4, 12), 1, border_radius=2)
    # slot
    pygame.draw.rect(s, _darken(base, 60), (5, cy - 2, BS - 10, 4))
    # highlight
    pygame.draw.line(s, hi, (3, cy - 5), (BS - 3, cy - 5), 1)
    # corner screws
    for px in (5, BS - 5):
        pygame.draw.circle(s, dark, (px, cy), 2)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _strap_hinge(base):
    """Decorative strap hinge face plate on door panel."""
    s = pygame.Surface((BS, BS))
    s.fill((80, 58, 38))   # door backdrop
    dark = _darken(base, 30)
    hi   = _lighter(base, 30)
    # horizontal strap
    pygame.draw.rect(s, base, (0, BS // 2 - 3, BS, 6))
    pygame.draw.line(s, hi,   (0, BS // 2 - 3), (BS, BS // 2 - 3), 1)
    pygame.draw.line(s, dark, (0, BS // 2 + 3), (BS, BS // 2 + 3), 1)
    # rivet dots
    for x in range(4, BS - 2, 6):
        pygame.draw.circle(s, hi,   (x, BS // 2), 2)
        pygame.draw.circle(s, dark, (x, BS // 2), 2, 1)
    # knuckle barrel at left
    pygame.draw.rect(s, _lighter(base, 20), (0, BS // 2 - 5, 8, 10), border_radius=4)
    pygame.draw.rect(s, dark, (0, BS // 2 - 5, 8, 10), 1, border_radius=4)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _window_well(base):
    """Curved metal basement window well."""
    s = pygame.Surface((BS, BS))
    s.fill((110, 95, 80))   # earth/wall backdrop
    dark = _darken(base, 30)
    hi   = _lighter(base, 25)
    # corrugated metal arcs
    for y in range(0, BS, BS // 6):
        pygame.draw.arc(s, base, (2, y, BS - 4, BS // 3), 0, 3.14159, 3)
        pygame.draw.arc(s, hi,   (2, y, BS - 4, BS // 3), 0, 3.14159, 1)
    # side flanges
    pygame.draw.rect(s, base, (0, 0, 3, BS))
    pygame.draw.rect(s, base, (BS - 3, 0, 3, BS))
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _damp_course(base):
    """Bitumen damp proof course layer between stone courses."""
    s = pygame.Surface((BS, BS))
    s.fill(_darken(base, 15))
    hi   = _lighter(base, 15)
    dark = _darken(base, 45)
    # stone courses above/below
    course = BS // 3
    pygame.draw.rect(s, base, (0, 0, BS, course - 2))
    pygame.draw.rect(s, base, (0, BS - course + 2, BS, course - 2))
    # damp course band — black bitumen stripe
    pygame.draw.rect(s, (28, 25, 22), (0, course - 2, BS, 4))
    # slight texture in dpc band
    for x in range(0, BS, 4):
        pygame.draw.line(s, (45, 40, 38), (x, course - 2), (x, course + 2), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _iron_conservatory_frame(base):
    """Ornate cast iron conservatory frame with glazing bars."""
    s = pygame.Surface((BS, BS))
    s.fill((170, 210, 220))  # glass/sky fill
    dark = _darken(base, 25)
    hi   = _lighter(base, 30)
    # main vertical bars
    for x in range(0, BS + 1, BS // 4):
        pygame.draw.rect(s, base, (x - 1, 0, 3, BS))
        pygame.draw.line(s, hi, (x, 0), (x, BS), 1)
    # horizontal glazing bars
    for y in range(0, BS + 1, BS // 4):
        pygame.draw.rect(s, base, (0, y - 1, BS, 3))
        pygame.draw.line(s, hi, (0, y), (BS, y), 1)
    # decorative arch at top
    pygame.draw.arc(s, base, (2, 1, BS - 4, BS // 2), 0, 3.14159, 3)
    pygame.draw.arc(s, hi,   (2, 1, BS - 4, BS // 2), 0, 3.14159, 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 2)
    return s


def _incised_render(base):
    """Render with scored geometric incised lines."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 45)
    hi   = _lighter(base, 20)
    cell = BS // 4
    # scored grid
    for i in range(1, 4):
        pygame.draw.line(s, dark, (i * cell, 0), (i * cell, BS), 1)
        pygame.draw.line(s, hi,   (i * cell + 1, 0), (i * cell + 1, BS), 1)
        pygame.draw.line(s, dark, (0, i * cell), (BS, i * cell), 1)
        pygame.draw.line(s, hi,   (0, i * cell + 1), (BS, i * cell + 1), 1)
    # diagonal score in each cell
    for row in range(4):
        for col in range(4):
            if (row + col) % 2 == 0:
                cx, cy = col * cell + cell // 2, row * cell + cell // 2
                pygame.draw.line(s, dark, (cx - 3, cy - 3), (cx + 3, cy + 3), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _pargeting(base):
    """Ornate moulded plaster exterior decoration."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 40)
    cx, cy = BS // 2, BS // 2
    # stylised foliage relief
    # stem
    pygame.draw.line(s, dark, (cx, BS - 2), (cx, 4), 1)
    # leaf sprays
    for sign in (-1, 1):
        for r_x, r_y in [(sign * 6, BS * 3 // 4), (sign * 8, BS // 2), (sign * 5, BS // 4)]:
            pts = [(cx, r_y), (cx + r_x, r_y - 4), (cx + r_x, r_y + 4)]
            pygame.draw.polygon(s, hi, pts)
            pygame.draw.polygon(s, dark, pts, 1)
    # top flower
    pygame.draw.circle(s, hi,   (cx, 5), 4)
    pygame.draw.circle(s, dark, (cx, 5), 4, 1)
    for a_x, a_y in [(-4, 0), (4, 0), (0, -4), (0, 4)]:
        pygame.draw.circle(s, hi, (cx + a_x, 5 + a_y), 2)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _stucco_band(base):
    """Smooth stucco horizontal band with pencil-line joints."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 30)
    hi   = _lighter(base, 30)
    # top shadow line
    pygame.draw.line(s, dark, (0, 0), (BS, 0), 2)
    # bottom highlight
    pygame.draw.line(s, hi,   (0, BS - 2), (BS, BS - 2), 1)
    # faint pencil-scored quoin lines
    for x in range(0, BS, BS // 2):
        pygame.draw.line(s, dark, (x, 2), (x, BS - 2), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _lincrusta(base):
    """Embossed Lincrusta wall covering — repeating scroll motif."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    hi   = _lighter(base, 35)
    dark = _darken(base, 30)
    # four-cell repeating acanthus/scroll
    cell = BS // 2
    for row in range(2):
        for col in range(2):
            x0, y0 = col * cell + 2, row * cell + 2
            cx, cy  = x0 + cell // 2 - 2, y0 + cell // 2 - 2
            # outer oval
            pygame.draw.ellipse(s, hi,   (x0, y0, cell - 4, cell - 4))
            pygame.draw.ellipse(s, dark, (x0, y0, cell - 4, cell - 4), 1)
            # inner curl
            pygame.draw.ellipse(s, base, (x0 + 3, y0 + 3, cell - 10, cell - 10))
            pygame.draw.ellipse(s, dark, (x0 + 3, y0 + 3, cell - 10, cell - 10), 1)
            # leaf tendrils
            pygame.draw.line(s, dark, (cx, y0), (cx, y0 + cell - 4), 1)
            pygame.draw.line(s, dark, (x0, cy), (x0 + cell - 4, cy), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _anaglypta(base):
    """Anaglypta textured relief wallcovering — diagonal diamond grid."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    hi   = _lighter(base, 40)
    dark = _darken(base, 30)
    d    = BS // 5
    for row in range(-1, BS // d + 2):
        for col in range(-1, BS // d + 2):
            cx = col * d + (d // 2 if row % 2 else 0)
            cy = row * d
            pts = [(cx, cy + d // 2), (cx + d // 2, cy),
                   (cx, cy - d // 2), (cx - d // 2, cy)]
            pygame.draw.polygon(s, hi,   pts)
            pygame.draw.polygon(s, dark, pts, 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _smooth_plaster(base):
    """Smooth interior lime plaster with a slight texture."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    # very faint float marks
    import random as _r
    _r.seed(hash(base) ^ 77)
    hi   = _lighter(base, 12)
    dark = _darken(base, 12)
    for _ in range(6):
        x1 = _r.randint(0, BS - 4)
        y1 = _r.randint(0, BS - 2)
        pygame.draw.line(s, hi if _r.random() > 0.5 else dark,
                         (x1, y1), (x1 + _r.randint(3, 8), y1), 1)
    pygame.draw.rect(s, _darken(base, 25), (0, 0, BS, BS), 1)
    return s


def _ceiling_rose(base):
    """Ornate plaster ceiling rose with concentric rings."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    cx, cy = BS // 2, BS // 2
    dark = _darken(base, 40)
    hi   = _lighter(base, 45)
    # concentric rings
    for r, col in [(BS // 2 - 1, dark), (BS // 2 - 3, hi),
                   (BS // 3, dark),      (BS // 3 - 2, hi),
                   (BS // 5, dark),      (4, hi)]:
        pygame.draw.circle(s, col, (cx, cy), r, 1)
    # petal details
    import math
    for i in range(8):
        a = i * math.pi / 4
        px = int(cx + (BS // 3 - 4) * math.cos(a))
        py = int(cy + (BS // 3 - 4) * math.sin(a))
        pygame.draw.circle(s, hi,   (px, py), 2)
        pygame.draw.circle(s, dark, (px, py), 2, 1)
    # center boss
    pygame.draw.circle(s, dark, (cx, cy), 3)
    pygame.draw.circle(s, hi,   (cx, cy), 2)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _coved_cornice_art(base):
    """Curved coved plaster cornice profile."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 40)
    # cove curve — filled arc
    pygame.draw.arc(s, dark, (0, -BS // 2, BS * 2, BS), 0, 3.14159 / 2, BS // 3)
    pygame.draw.arc(s, hi,   (0, -BS // 2, BS * 2, BS), 0, 3.14159 / 2, 2)
    # horizontal shelf top
    pygame.draw.rect(s, _lighter(base, 10), (0, 0, BS, 4))
    # vertical wall bottom
    pygame.draw.rect(s, _lighter(base, 5), (0, BS - 4, BS, 4))
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _flaunching(base):
    """Cement flaunching around chimney — sloped grey bead."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 25)
    # sloped surface lines
    for i in range(0, BS, 4):
        pygame.draw.line(s, _darken(base, 10 + i), (0, i), (BS - i, 0), 1)
    # edge profile
    pygame.draw.polygon(s, _darken(base, 20),
                        [(0, BS), (BS, 0), (BS, BS // 4), (BS // 4, BS)], 0)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _vergeboard_art(base):
    """Decorative bargeboards with carved scrollwork cutouts."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 45)
    hi   = _lighter(base, 35)
    # main board body
    pygame.draw.rect(s, _darken(base, 10), (0, 0, BS, BS // 3))
    # cutout arches along bottom edge
    arch_w = BS // 3
    for i in range(3):
        cx = i * arch_w + arch_w // 2
        r = pygame.Rect(cx - arch_w // 2 + 1, BS // 3, arch_w - 2, arch_w // 2 * 2)
        pygame.draw.arc(s, dark, r, 0, 3.14159, 2)
        pygame.draw.arc(s, hi,   r, 0, 3.14159, 1)
    # carved circles
    for i in range(3):
        cx = i * arch_w + arch_w // 2
        pygame.draw.circle(s, dark, (cx, BS // 6), 4, 1)
        pygame.draw.circle(s, hi,   (cx, BS // 6), 3)
    # drop pendants
    for i in range(3):
        px = i * arch_w + arch_w // 2
        pygame.draw.circle(s, _darken(base, 25), (px, BS - 5), 4)
        pygame.draw.circle(s, dark, (px, BS - 5), 4, 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _frieze_panel(base):
    """Decorative carved frieze panel with repeating anthemion motif."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 35)
    # background band
    pygame.draw.rect(s, _darken(base, 8), (0, BS // 4, BS, BS // 2))
    # anthemion fan motif repeated
    for i in range(2):
        cx = i * BS // 2 + BS // 4
        cy = BS // 2
        for r_ang in range(5):
            import math
            a = math.pi * (r_ang / 4 - 0.5)
            x2 = int(cx + 8 * math.cos(a))
            y2 = int(cy - 8 * math.sin(a))
            pygame.draw.line(s, hi,   (cx, cy), (x2, y2), 1)
            pygame.draw.circle(s, hi,   (x2, y2), 2)
            pygame.draw.circle(s, dark, (x2, y2), 2, 1)
        pygame.draw.circle(s, dark, (cx, cy), 3)
        pygame.draw.circle(s, hi,   (cx, cy), 2)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _dentil_strip(base):
    """Repeating dentil (tooth) moulding strip."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark  = _darken(base, 45)
    hi    = _lighter(base, 35)
    tooth_w, tooth_gap, tooth_h = 4, 2, BS // 2
    y0    = (BS - tooth_h) // 2
    # cornice bed above
    pygame.draw.rect(s, _darken(base, 10), (0, 0, BS, y0))
    pygame.draw.line(s, dark, (0, y0), (BS, y0), 1)
    # dentils
    x = 1
    while x < BS:
        pygame.draw.rect(s, _lighter(base, 5), (x, y0, tooth_w, tooth_h))
        pygame.draw.lines(s, hi,   False,
                          [(x, y0 + tooth_h), (x, y0), (x + tooth_w, y0)], 1)
        pygame.draw.lines(s, dark, False,
                          [(x, y0 + tooth_h), (x + tooth_w, y0 + tooth_h), (x + tooth_w, y0)], 1)
        x += tooth_w + tooth_gap
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _egg_dart(base):
    """Classical egg-and-dart moulding strip."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 40)
    cy   = BS // 2
    mh   = BS // 3
    # bed
    pygame.draw.rect(s, _darken(base, 8), (0, 0, BS, cy - mh // 2))
    # alternating egg (oval) and dart (arrow) motifs
    cell = BS // 4
    for i in range(4):
        cx = i * cell + cell // 2
        if i % 2 == 0:
            # egg oval
            pygame.draw.ellipse(s, hi,   (cx - cell // 3, cy - mh // 2, cell * 2 // 3, mh))
            pygame.draw.ellipse(s, dark, (cx - cell // 3, cy - mh // 2, cell * 2 // 3, mh), 1)
            # shadow at base
            pygame.draw.ellipse(s, dark, (cx - cell // 3 + 1, cy + mh // 4, cell * 2 // 3 - 2, mh // 4))
        else:
            # dart / arrow
            pts = [(cx, cy - mh // 2 - 2), (cx - 3, cy + mh // 2), (cx + 3, cy + mh // 2)]
            pygame.draw.polygon(s, dark, pts)
            pygame.draw.polygon(s, hi,   pts, 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _ovolo_moulding(base):
    """Quarter-round ovolo moulding profile."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 45)
    # quarter-circle profile fill
    pygame.draw.circle(s, _darken(base, 10), (0, BS), BS - 2)
    # highlight arc
    pygame.draw.arc(s, hi, (-BS // 2, BS // 2, BS, BS), 0, 3.14159 / 2, 3)
    # shadow arc
    pygame.draw.arc(s, dark, (-BS // 4, BS // 4, BS, BS), 0, 3.14159 / 2, 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _crown_moulding(base):
    """Stepped crown moulding profile."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 45)
    # stacked profiles from top
    layers = [
        (0, 0, BS, 5, 0),      # flat fascia
        (2, 5, BS - 4, 6, 10), # ovolo
        (4, 11, BS - 8, 4, 5), # fillet
        (2, 15, BS - 4, 8, 8), # cavetto cove
        (0, 23, BS, 4, 0),     # flat soffit
    ]
    for x0, y0, w, h, shade in layers:
        c = _darken(base, shade) if shade else base
        pygame.draw.rect(s, c, (x0, y0, w, h))
        pygame.draw.line(s, hi,   (x0, y0), (x0 + w, y0), 1)
        pygame.draw.line(s, dark, (x0, y0 + h), (x0 + w, y0 + h), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _dado_rail_art(base):
    """Dado rail (chair rail) horizontal moulding."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 40)
    cy = BS // 2
    rh = BS // 4
    # wall above
    pygame.draw.rect(s, _lighter(base, 5), (0, 0, BS, cy - rh // 2))
    # rail profile
    pygame.draw.rect(s, _darken(base, 5), (0, cy - rh // 2, BS, rh))
    pygame.draw.line(s, hi,   (0, cy - rh // 2), (BS, cy - rh // 2), 2)
    pygame.draw.line(s, dark, (0, cy + rh // 2), (BS, cy + rh // 2), 2)
    # wall below
    pygame.draw.rect(s, _darken(base, 8), (0, cy + rh // 2, BS, BS - (cy + rh // 2)))
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _picture_rail_art(base):
    """Picture rail — narrow moulding near ceiling top."""
    s = pygame.Surface((BS, BS))
    s.fill(_lighter(base, 8))   # wall
    dark = _darken(base, 40)
    hi   = _lighter(base, 40)
    rh = 6
    y0 = 4
    pygame.draw.rect(s, base, (0, y0, BS, rh))
    pygame.draw.line(s, hi,   (0, y0), (BS, y0), 1)
    pygame.draw.line(s, dark, (0, y0 + rh), (BS, y0 + rh), 1)
    # picture hook detail
    cx = BS // 2
    pygame.draw.circle(s, dark, (cx, y0 + rh // 2), 2)
    pygame.draw.circle(s, hi,   (cx, y0 + rh // 2 - 1), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _baseboard_art(base):
    """Tall skirting/baseboard moulding with flat face and ogee cap."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 40)
    # flat face
    pygame.draw.rect(s, _lighter(base, 5), (2, BS // 4, BS - 4, BS * 2 // 3))
    # cap moulding top
    pygame.draw.rect(s, _darken(base, 5), (0, BS // 4 - 3, BS, 5))
    pygame.draw.line(s, hi,   (0, BS // 4 - 3), (BS, BS // 4 - 3), 1)
    pygame.draw.line(s, dark, (0, BS // 4 + 2), (BS, BS // 4 + 2), 1)
    # toe (plinth)
    pygame.draw.rect(s, _darken(base, 10), (0, BS - 5, BS, 5))
    pygame.draw.line(s, hi, (0, BS - 5), (BS, BS - 5), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _architrave_art(base):
    """Door/window architrave — rebated moulding surround."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 40)
    # outer flat
    pygame.draw.rect(s, _darken(base, 5), (0, 0, BS, BS))
    # back band inner rebate (shadow at door edge)
    pygame.draw.rect(s, _darken(base, 15), (BS - 5, 0, 5, BS))
    pygame.draw.line(s, dark, (BS - 5, 0), (BS - 5, BS), 1)
    # ogee profile lines
    for y in range(0, BS, BS // 4):
        pygame.draw.line(s, hi,   (0, y), (BS - 6, y), 1)
        pygame.draw.line(s, dark, (0, y + 1), (BS - 6, y + 1), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _rendered_wall(base):
    """Smooth rendered wall (stucco/plaster exterior)."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    hi   = _lighter(base, 18)
    dark = _darken(base, 18)
    # very faint scored horizontal quoin lines
    for y in range(0, BS, BS // 4):
        pygame.draw.line(s, dark, (0, y), (BS, y), 1)
        pygame.draw.line(s, hi,   (0, y + 1), (BS, y + 1), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _keystone(base):
    """Arch keystone — trapezoid wedge block."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 30)
    # trapezoid shape wider at bottom
    pts = [(BS // 4, 0), (3 * BS // 4, 0),
           (BS - 2, BS - 1), (2, BS - 1)]
    pygame.draw.polygon(s, _lighter(base, 8), pts)
    pygame.draw.polygon(s, dark, pts, 1)
    # drafted margin lines
    pygame.draw.lines(s, hi, False,
                      [(BS // 4 + 2, 2), (BS // 4, 0), (2, BS - 1)], 1)
    pygame.draw.lines(s, dark, False,
                      [(3 * BS // 4 - 2, 2), (3 * BS // 4, 0), (BS - 2, BS - 1)], 1)
    # boss line
    cy = BS // 2
    pygame.draw.line(s, hi, (BS // 4 + 2, cy), (3 * BS // 4 - 2, cy), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _tympanum(base):
    """Triangular tympanum panel — pediment infill with relief."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 35)
    # triangular field
    pts = [(0, BS - 1), (BS // 2, 2), (BS - 1, BS - 1)]
    pygame.draw.polygon(s, _lighter(base, 8), pts)
    pygame.draw.polygon(s, dark, pts, 1)
    # inner fan / shell relief
    cx, cy = BS // 2, BS // 2 + 4
    import math
    for i in range(7):
        a = math.pi * i / 6
        r = BS // 4
        x2 = int(cx + r * math.cos(a))
        y2 = int(cy - r * abs(math.sin(a)))
        pygame.draw.line(s, hi, (cx, cy), (x2, y2), 1)
    pygame.draw.circle(s, dark, (cx, cy), 3)
    pygame.draw.circle(s, hi,   (cx, cy), 2)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _medallion(base):
    """Circular stone medallion with relief decoration."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    cx, cy = BS // 2, BS // 2
    dark = _darken(base, 40)
    hi   = _lighter(base, 45)
    # outer ring
    pygame.draw.circle(s, _darken(base, 10), (cx, cy), BS // 2 - 1)
    pygame.draw.circle(s, dark, (cx, cy), BS // 2 - 1, 2)
    pygame.draw.circle(s, hi,   (cx, cy), BS // 2 - 3, 1)
    # inner rosette
    pygame.draw.circle(s, _lighter(base, 12), (cx, cy), BS // 3)
    pygame.draw.circle(s, dark, (cx, cy), BS // 3, 1)
    # petal ring
    import math
    for i in range(8):
        a = i * math.pi / 4
        px = int(cx + (BS // 3 - 2) * math.cos(a))
        py = int(cy + (BS // 3 - 2) * math.sin(a))
        pygame.draw.circle(s, hi, (px, py), 2)
    pygame.draw.circle(s, dark, (cx, cy), 3)
    pygame.draw.circle(s, hi,   (cx, cy), 2)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _cartouche(base):
    """Ornate cartouche frame with scrolled ends."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 40)
    cy = BS // 2
    # rolled ends
    for ex in (3, BS - 7):
        pygame.draw.ellipse(s, _lighter(base, 10), (ex, cy - 8, 8, 16))
        pygame.draw.ellipse(s, dark, (ex, cy - 8, 8, 16), 1)
        pygame.draw.ellipse(s, hi,   (ex + 1, cy - 6, 5, 12), 1)
    # central panel
    pygame.draw.rect(s, _lighter(base, 8), (10, cy - 8, BS - 20, 16))
    pygame.draw.rect(s, dark, (10, cy - 8, BS - 20, 16), 1)
    # inscription lines
    for y in (cy - 3, cy + 2):
        pygame.draw.line(s, dark, (13, y), (BS - 13, y), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _heraldic(base):
    """Heraldic shield panel."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark  = _darken(base, 40)
    hi    = _lighter(base, 35)
    gold  = (185, 152, 72)
    # shield outline
    pts = [(4, 2), (BS - 4, 2), (BS - 4, BS * 2 // 3),
           (BS // 2, BS - 3), (4, BS * 2 // 3)]
    pygame.draw.polygon(s, _darker_by(base, 5), pts)
    pygame.draw.polygon(s, dark, pts, 2)
    # horizontal division
    cy = BS * 2 // 5
    pygame.draw.line(s, dark, (4, cy), (BS - 4, cy), 1)
    # chief (top) field
    pygame.draw.polygon(s, gold, [(4, 2), (BS - 4, 2), (BS - 4, cy), (4, cy)])
    pygame.draw.polygon(s, dark, [(4, 2), (BS - 4, 2), (BS - 4, cy), (4, cy)], 1)
    # center charge (simple circle device)
    pygame.draw.circle(s, hi,   (BS // 2, (cy + BS * 2 // 3) // 2), 5)
    pygame.draw.circle(s, dark, (BS // 2, (cy + BS * 2 // 3) // 2), 5, 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _darker_by(base, amount):
    return tuple(max(0, c - amount) for c in base)


def _finial(base):
    """Pointed spire finial block."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 45)
    cx   = BS // 2
    # tapered spire
    pts = [(cx, 0), (cx + BS // 4, BS), (cx - BS // 4, BS)]
    pygame.draw.polygon(s, _lighter(base, 8), pts)
    pygame.draw.polygon(s, dark, pts, 1)
    # shaft ring
    pygame.draw.rect(s, _darken(base, 20), (cx - BS // 5, BS * 2 // 3, BS // 5 * 2, 6))
    pygame.draw.line(s, hi, (cx - BS // 5, BS * 2 // 3), (cx + BS // 5, BS * 2 // 3), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _corbel(base):
    """Projecting corbel bracket — stepped stone support."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 30)
    # stepped corbel profile
    steps = [(0, BS // 3, BS // 3, BS * 2 // 3),
             (BS // 3, BS // 6, BS // 3 * 2, BS * 5 // 6),
             (BS // 3 * 2, 0, BS // 3, BS)]
    for x0, y0, w, h in steps:
        pygame.draw.rect(s, _lighter(base, 5), (x0, y0, w, h))
        pygame.draw.lines(s, hi, False, [(x0, y0 + h), (x0, y0), (x0 + w, y0)], 1)
        pygame.draw.lines(s, dark, False, [(x0, y0 + h), (x0 + w, y0 + h), (x0 + w, y0)], 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _modillion(base):
    """Small S-scroll modillion bracket."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 40)
    # scroll body
    pygame.draw.arc(s, base,  (2, 2, BS - 8, BS // 2), 0, 3.14159, BS // 4)
    pygame.draw.arc(s, base,  (4, BS // 2, BS - 8, BS // 2 - 2), 3.14159, 6.28318, BS // 4)
    pygame.draw.arc(s, hi,    (2, 2, BS - 8, BS // 2), 0, 3.14159, 1)
    pygame.draw.arc(s, dark,  (4, BS // 2, BS - 8, BS // 2 - 2), 3.14159, 6.28318, 1)
    # flat bed plate on top
    pygame.draw.rect(s, _darken(base, 8), (0, 0, BS, 5))
    pygame.draw.line(s, hi, (0, 1), (BS, 1), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _console(base):
    """Console (S-curve) bracket."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 35)
    # top wide part
    pygame.draw.rect(s, _lighter(base, 5), (2, 2, BS - 4, BS // 3))
    # S-curve
    pygame.draw.arc(s, base, (0, BS // 3 - BS // 4, BS, BS // 2), 0, 3.14159, BS // 5)
    pygame.draw.arc(s, base, (2, BS // 2, BS - 4, BS // 2), 3.14159, 6.28318, BS // 5)
    # highlight/shadow
    pygame.draw.arc(s, hi,   (0, BS // 3 - BS // 4, BS, BS // 2), 0, 3.14159, 1)
    pygame.draw.arc(s, dark, (2, BS // 2, BS - 4, BS // 2), 3.14159, 6.28318, 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _column_capital(base):
    """Classical column capital — volute/abacus block."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 40)
    # abacus (top flat slab)
    pygame.draw.rect(s, _darken(base, 5), (0, 0, BS, BS // 4))
    pygame.draw.line(s, hi,   (0, 0), (BS, 0), 1)
    pygame.draw.line(s, dark, (0, BS // 4), (BS, BS // 4), 1)
    # echinus (egg-shape bulge)
    pygame.draw.ellipse(s, _lighter(base, 8), (2, BS // 4, BS - 4, BS // 3))
    pygame.draw.ellipse(s, dark, (2, BS // 4, BS - 4, BS // 3), 1)
    # volute scrolls on sides
    for ex in (2, BS - 6):
        pygame.draw.ellipse(s, hi, (ex, BS // 4, 6, 8))
        pygame.draw.ellipse(s, dark, (ex, BS // 4, 6, 8), 1)
    # neck / astragal
    pygame.draw.rect(s, _darken(base, 12), (2, BS * 3 // 5, BS - 4, 3))
    pygame.draw.line(s, hi, (2, BS * 3 // 5), (BS - 2, BS * 3 // 5), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _column_base_art(base):
    """Attic column base — torus / scotiae / plinth."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 40)
    # plinth (bottom flat)
    pygame.draw.rect(s, _darken(base, 5), (0, BS - BS // 4, BS, BS // 4))
    pygame.draw.line(s, hi, (0, BS - BS // 4), (BS, BS - BS // 4), 1)
    # lower torus
    pygame.draw.ellipse(s, _lighter(base, 5), (2, BS - BS // 4 - BS // 6, BS - 4, BS // 6))
    pygame.draw.ellipse(s, dark, (2, BS - BS // 4 - BS // 6, BS - 4, BS // 6), 1)
    # scotiae hollow
    pygame.draw.ellipse(s, _darken(base, 15), (4, BS // 2, BS - 8, BS // 5))
    pygame.draw.ellipse(s, dark, (4, BS // 2, BS - 8, BS // 5), 1)
    # upper torus
    pygame.draw.ellipse(s, _lighter(base, 8), (2, BS // 3, BS - 4, BS // 6))
    pygame.draw.ellipse(s, dark, (2, BS // 3, BS - 4, BS // 6), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _fanlight_surround_art(base):
    """Semicircular fanlight door surround with pilaster sides."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 35)
    # side pilasters
    pygame.draw.rect(s, _darken(base, 8), (0, 0, 5, BS))
    pygame.draw.rect(s, _darken(base, 8), (BS - 5, 0, 5, BS))
    pygame.draw.line(s, hi, (2, 0), (2, BS), 1)
    pygame.draw.line(s, hi, (BS - 3, 0), (BS - 3, BS), 1)
    # arch soffit
    pygame.draw.arc(s, _darken(base, 5), (4, 2, BS - 8, BS - 6), 0, 3.14159, 4)
    pygame.draw.arc(s, hi,   (5, 3, BS - 10, BS - 8), 0, 3.14159, 1)
    pygame.draw.arc(s, dark, (4, 2, BS - 8, BS - 6), 0, 3.14159, 1)
    # keystone
    pygame.draw.rect(s, _lighter(base, 12), (BS // 2 - 3, 2, 6, 8))
    pygame.draw.rect(s, dark, (BS // 2 - 3, 2, 6, 8), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _pilaster_surround(base):
    """Door surround with flanking pilasters and entablature."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 35)
    # entablature header
    pygame.draw.rect(s, _darken(base, 8), (0, 0, BS, BS // 4))
    pygame.draw.line(s, hi,   (0, 1), (BS, 1), 1)
    pygame.draw.line(s, dark, (0, BS // 4), (BS, BS // 4), 2)
    # left pilaster
    pygame.draw.rect(s, _darken(base, 5), (0, BS // 4, BS // 5, BS * 3 // 4))
    pygame.draw.line(s, hi, (2, BS // 4), (2, BS), 1)
    pygame.draw.line(s, dark, (BS // 5, BS // 4), (BS // 5, BS), 1)
    # right pilaster
    pygame.draw.rect(s, _darken(base, 5), (BS - BS // 5, BS // 4, BS // 5, BS * 3 // 4))
    pygame.draw.line(s, hi, (BS - BS // 5 + 1, BS // 4), (BS - BS // 5 + 1, BS), 1)
    pygame.draw.line(s, dark, (BS - 1, BS // 4), (BS - 1, BS), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _hood_moulding_art(base):
    """Drip-stone hood moulding over window/door."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 35)
    # projecting hood label
    pygame.draw.rect(s, _darken(base, 8), (0, 0, BS, BS // 3))
    # soffit undercut (shadow)
    pygame.draw.rect(s, _darken(base, 30), (0, BS // 3, BS, 3))
    # angled kneelers at ends
    pygame.draw.polygon(s, _darken(base, 12),
                        [(0, BS // 3), (BS // 5, 0), (0, 0)])
    pygame.draw.polygon(s, _darken(base, 12),
                        [(BS, BS // 3), (BS - BS // 5, 0), (BS, 0)])
    pygame.draw.line(s, hi, (0, 1), (BS, 1), 1)
    pygame.draw.line(s, dark, (0, BS // 3 + 3), (BS, BS // 3 + 3), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _bracket(base):
    """Angled decorative support bracket — right-triangle profile."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 35)
    # right-angle bracket body
    pts = [(0, 0), (BS - 1, 0), (0, BS - 1)]
    pygame.draw.polygon(s, _lighter(base, 8), pts)
    pygame.draw.polygon(s, dark, pts, 1)
    # profile lines
    pygame.draw.line(s, hi,   (0, 0), (BS - 1, 0), 1)
    pygame.draw.line(s, hi,   (0, 0), (0, BS - 1), 1)
    pygame.draw.line(s, dark, (0, BS - 1), (BS - 1, 0), 2)
    # scroll detail
    pygame.draw.circle(s, hi,   (BS // 4, BS // 4), 4)
    pygame.draw.circle(s, dark, (BS // 4, BS // 4), 4, 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _knee_brace_art(base):
    """Craftsman knee brace — angled timber strut."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 30)
    # thick diagonal timber
    pygame.draw.line(s, _lighter(base, 5), (0, BS - 1), (BS - 1, 0), 6)
    pygame.draw.line(s, hi,   (1, BS - 2), (BS - 2, 1), 1)
    pygame.draw.line(s, dark, (3, BS - 1), (BS - 1, 3), 1)
    # end notch cuts
    pygame.draw.rect(s, dark, (0, BS - 6, 5, 6))
    pygame.draw.rect(s, dark, (BS - 5, 0, 5, 6))
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _beam_end(base):
    """Exposed rafter or cantilever beam end grain view."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 30)
    # beam cross-section with concentric growth ring lines
    m = 3
    pygame.draw.rect(s, _lighter(base, 5), (m, m, BS - 2*m, BS - 2*m))
    for i in range(3, min(BS // 2 - 2, 10)):
        pygame.draw.rect(s, _darken(base, i * 3), (m + i, m + i, BS - 2*(m+i), BS - 2*(m+i)), 1)
    # medullary ray lines
    cx, cy = BS // 2, BS // 2
    for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
        pygame.draw.line(s, dark, (cx, cy), (cx + dx * BS // 2, cy + dy * BS // 2), 1)
    pygame.draw.rect(s, dark, (m, m, BS - 2*m, BS - 2*m), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _trim_strip(base):
    """Simple square-profiled Craftsman trim strip."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 35)
    # flat face with bevel edges
    pygame.draw.rect(s, _lighter(base, 5), (2, 2, BS - 4, BS - 4))
    pygame.draw.lines(s, hi,   False, [(2, BS - 2), (2, 2), (BS - 2, 2)], 1)
    pygame.draw.lines(s, dark, False, [(2, BS - 2), (BS - 2, BS - 2), (BS - 2, 2)], 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _pergola_post_art(base):
    """Square Craftsman pergola post with chamfered corners."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 35)
    cx = BS // 2
    w  = BS // 3
    # shaft
    pygame.draw.rect(s, _lighter(base, 5), (cx - w, 0, w * 2, BS))
    # chamfer bevel lines
    pygame.draw.line(s, hi,   (cx - w + 1, 0), (cx - w + 1, BS), 1)
    pygame.draw.line(s, dark, (cx + w - 2, 0), (cx + w - 2, BS), 1)
    pygame.draw.rect(s, dark, (cx - w, 0, w * 2, BS), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _newel_post_art(base):
    """Ornate turned newel post with finial cap."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 40)
    cx = BS // 2
    # base block
    pygame.draw.rect(s, _darken(base, 12), (cx - 6, BS - 7, 12, 7))
    # turned shaft
    for y, w2 in [(BS - 7, 6), (BS * 3 // 5, 5), (BS // 2, 4),
                  (BS * 2 // 5, 5), (BS // 4, 6), (BS // 8, 5)]:
        pygame.draw.rect(s, base, (cx - w2, y - 5, w2 * 2, 5))
        pygame.draw.line(s, hi,   (cx - w2 + 1, y - 4), (cx - w2 + 1, y), 1)
        pygame.draw.line(s, dark, (cx + w2 - 2, y - 4), (cx + w2 - 2, y), 1)
    # sphere cap finial
    pygame.draw.circle(s, _lighter(base, 8), (cx, BS // 8), 5)
    pygame.draw.circle(s, dark, (cx, BS // 8), 5, 1)
    pygame.draw.circle(s, hi, (cx - 1, BS // 8 - 1), 2)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _screen_panel(base):
    """Wire mesh screen panel in wooden frame."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    wire = _darken(base, 35)
    # frame
    pygame.draw.rect(s, _darken(base, 15), (0, 0, BS, BS), 3)
    # wire mesh grid
    for x in range(5, BS - 4, 3):
        pygame.draw.line(s, wire, (x, 3), (x, BS - 3), 1)
    for y in range(5, BS - 4, 3):
        pygame.draw.line(s, wire, (3, y), (BS - 3, y), 1)
    pygame.draw.rect(s, _darken(base, 40), (0, 0, BS, BS), 1)
    return s


def _stair_riser(base):
    """Painted vertical stair riser — plain with moulded base edge."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 30)
    hi   = _lighter(base, 35)
    # slight raised panel
    pygame.draw.rect(s, _lighter(base, 5), (3, 3, BS - 6, BS - 6))
    pygame.draw.lines(s, hi,   False, [(3, BS - 3), (3, 3), (BS - 3, 3)], 1)
    pygame.draw.lines(s, dark, False, [(3, BS - 3), (BS - 3, BS - 3), (BS - 3, 3)], 1)
    # nosing shadow at top
    pygame.draw.rect(s, dark, (0, 0, BS, 2))
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _stair_nosing(base):
    """Brass/metal stair nosing strip."""
    s = pygame.Surface((BS, BS))
    s.fill((140, 108, 68))   # wood tread
    dark = _darken(base, 30)
    hi   = _lighter(base, 45)
    # nosing bar at top edge
    pygame.draw.rect(s, base, (0, 0, BS, 6))
    pygame.draw.line(s, hi,   (0, 1), (BS, 1), 1)
    pygame.draw.line(s, dark, (0, 5), (BS, 5), 1)
    # anti-slip grooves
    for x in range(3, BS - 2, 4):
        pygame.draw.line(s, dark, (x, 2), (x, 4), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _mantelpiece(base):
    """Ornate painted wooden fireplace mantelpiece."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 45)
    # shelf top
    pygame.draw.rect(s, _darken(base, 5), (0, 0, BS, BS // 5))
    pygame.draw.line(s, hi, (0, 1), (BS, 1), 1)
    # frieze
    pygame.draw.rect(s, _lighter(base, 3), (2, BS // 5, BS - 4, BS // 4))
    # carved swag motif on frieze
    cx = BS // 2
    pygame.draw.arc(s, dark, (cx - 8, BS // 5 + 2, 16, 10), 3.14159, 6.28318, 1)
    pygame.draw.arc(s, hi,   (cx - 7, BS // 5 + 3, 14, 8),  3.14159, 6.28318, 1)
    # pilaster columns either side
    for px in (2, BS - 5):
        pygame.draw.rect(s, _darken(base, 8), (px, BS // 5, 4, BS * 3 // 5))
        pygame.draw.line(s, hi, (px + 1, BS // 5), (px + 1, BS * 4 // 5), 1)
    # base plinth
    pygame.draw.rect(s, _darken(base, 12), (0, BS * 4 // 5, BS, BS // 5))
    pygame.draw.line(s, hi, (0, BS * 4 // 5), (BS, BS * 4 // 5), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _fireplace_surround(base):
    """Tiled fireplace surround with decorative tile set."""
    s = pygame.Surface((BS, BS))
    s.fill(_darken(base, 20))
    tile_c = base
    dark   = _darken(base, 40)
    hi     = _lighter(base, 40)
    cell   = BS // 4
    for row in range(4):
        for col in range(4):
            # alternating painted/plain tiles
            c = _lighter(base, 25) if (row + col) % 2 == 0 else base
            x, y = col * cell + 1, row * cell + 1
            pygame.draw.rect(s, c, (x, y, cell - 2, cell - 2))
            # simple painted motif on alternate tiles
            if (row + col) % 2 == 0:
                cx, cy = x + (cell - 2) // 2, y + (cell - 2) // 2
                pygame.draw.circle(s, _darken(base, 30), (cx, cy), (cell - 2) // 3)
                pygame.draw.circle(s, hi, (cx, cy), (cell - 2) // 3, 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _overmantel(base):
    """Elaborate overmantel mirror frame above fireplace."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 40)
    gold = (188, 155, 72)
    # outer frame
    pygame.draw.rect(s, gold, (0, 0, BS, BS), 3)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    # mirror field
    pygame.draw.rect(s, (185, 205, 215), (3, 3, BS - 6, BS - 6))
    # bevelled inner edge
    pygame.draw.lines(s, hi,   False, [(3, BS - 3), (3, 3), (BS - 3, 3)], 1)
    pygame.draw.lines(s, dark, False, [(3, BS - 3), (BS - 3, BS - 3), (BS - 3, 3)], 1)
    # top pediment detail
    pygame.draw.rect(s, gold, (BS // 4, 3, BS // 2, 5))
    # corner rosettes
    for px, py in [(3, 3), (BS - 5, 3), (3, BS - 5), (BS - 5, BS - 5)]:
        pygame.draw.circle(s, gold, (px + 1, py + 1), 3)
        pygame.draw.circle(s, dark, (px + 1, py + 1), 3, 1)
    return s


def _inglenook_wall(base):
    """Inglenook nook side wall — rough plaster over stone."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark  = _darken(base, 30)
    hi    = _lighter(base, 20)
    stone = _darken(base, 45)
    # rough plaster surface
    import random as _r
    _r.seed(hash(base) ^ 55555)
    for _ in range(10):
        x1, y1 = _r.randint(0, BS - 4), _r.randint(0, BS - 2)
        pygame.draw.line(s, dark if _r.random() > 0.5 else hi,
                         (x1, y1), (x1 + _r.randint(2, 6), y1 + _r.randint(-1, 1)), 1)
    # exposed stone course at base
    pygame.draw.rect(s, stone, (0, BS - 8, BS, 8))
    for sx in range(0, BS, BS // 3):
        pygame.draw.rect(s, _darken(stone, 20), (sx, BS - 8, 1, 8))
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _bench_art(base):
    """Built-in wooden settle/bench seat."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 30)
    # seat top
    pygame.draw.rect(s, _darker_by(base, 8), (0, BS // 3, BS, 5))
    pygame.draw.line(s, hi,   (0, BS // 3), (BS, BS // 3), 1)
    pygame.draw.line(s, dark, (0, BS // 3 + 4), (BS, BS // 3 + 4), 1)
    # plank lines on seat
    for x in range(0, BS, BS // 4):
        pygame.draw.line(s, dark, (x, BS // 3), (x, BS // 3 + 5), 1)
    # base/apron board
    pygame.draw.rect(s, _darken(base, 10), (2, BS // 3 + 5, BS - 4, BS * 2 // 3 - 5))
    # leg outlines at sides
    for lx in (2, BS - 5):
        pygame.draw.rect(s, _darken(base, 15), (lx, BS // 3 + 5, 4, BS * 2 // 3 - 5))
        pygame.draw.line(s, hi, (lx + 1, BS // 3 + 5), (lx + 1, BS - 1), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _bookcase_art(base):
    """Painted built-in bookcase with shelves and books."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 35)
    book_cols = [(185, 72, 55), (55, 90, 165), (62, 118, 62),
                 (190, 155, 45), (130, 55, 130)]
    # shelves
    shelf_h = BS // 5
    for shelf in range(4):
        y0 = shelf * shelf_h
        pygame.draw.rect(s, _darken(base, 8), (0, y0 + shelf_h - 3, BS, 3))
        # books on shelf
        bx = 1
        bi = 0
        while bx < BS - 3:
            bw = 3 + bi % 3
            bc = book_cols[(bi + shelf) % len(book_cols)]
            pygame.draw.rect(s, bc, (bx, y0 + 1, bw, shelf_h - 4))
            pygame.draw.line(s, _darken(bc, 30), (bx, y0 + 1), (bx, y0 + shelf_h - 3), 1)
            bx += bw + 1
            bi += 1
    # frame rails
    pygame.draw.rect(s, _darken(base, 5), (0, 0, 3, BS))
    pygame.draw.rect(s, _darken(base, 5), (BS - 3, 0, 3, BS))
    pygame.draw.line(s, hi, (1, 0), (1, BS), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _window_seat(base):
    """Built-in window seat box with hinged lid panel."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 35)
    # box body
    pygame.draw.rect(s, _darker_by(base, 8), (2, BS // 3, BS - 4, BS * 2 // 3 - 2))
    # lid panel
    pygame.draw.rect(s, _lighter(base, 5), (2, BS // 4, BS - 4, BS // 10))
    pygame.draw.line(s, hi,   (2, BS // 4), (BS - 2, BS // 4), 1)
    pygame.draw.line(s, dark, (2, BS // 4 + BS // 10), (BS - 2, BS // 4 + BS // 10), 1)
    # hinge hardware
    for hx in (BS // 3, 2 * BS // 3):
        pygame.draw.rect(s, (140, 115, 55), (hx - 2, BS // 4 - 1, 4, 4))
        pygame.draw.rect(s, dark, (hx - 2, BS // 4 - 1, 4, 4), 1)
    # cushion / seat top
    pygame.draw.rect(s, (175, 128, 148), (2, BS // 5, BS - 4, BS // 10))
    pygame.draw.rect(s, dark, (2, BS // 5, BS - 4, BS // 10), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _shelf_art(base):
    """Built-in alcove shelf with moulded front edge."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 35)
    # three shelves
    for i in range(3):
        y = i * (BS // 3)
        pygame.draw.rect(s, _darker_by(base, 5), (0, y + BS // 3 - 4, BS, 5))
        pygame.draw.line(s, hi, (0, y + BS // 3 - 4), (BS, y + BS // 3 - 4), 1)
        pygame.draw.line(s, dark, (0, y + BS // 3), (BS, y + BS // 3), 1)
    # side wall brackets
    for sx in (2, BS - 4):
        pygame.draw.rect(s, _darken(base, 10), (sx, 0, 3, BS))
        pygame.draw.line(s, hi, (sx + 1, 0), (sx + 1, BS), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _cabinet_art(base):
    """China cabinet/display case with glazed upper doors."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 35)
    glass = (185, 208, 218)
    # upper glazed section
    pygame.draw.rect(s, glass, (2, 2, BS - 4, BS // 2 - 2))
    # glazing bar cross
    pygame.draw.line(s, dark, (BS // 2, 2), (BS // 2, BS // 2 - 2), 1)
    pygame.draw.line(s, dark, (2, BS // 4), (BS - 2, BS // 4), 1)
    pygame.draw.rect(s, dark, (2, 2, BS - 4, BS // 2 - 2), 1)
    # lower solid doors
    for i in range(2):
        x0 = 2 + i * (BS // 2 - 2)
        pygame.draw.rect(s, _darker_by(base, 8),
                         (x0, BS // 2, (BS // 2 - 3), BS // 2 - 2))
        pygame.draw.rect(s, dark, (x0, BS // 2, (BS // 2 - 3), BS // 2 - 2), 1)
        # knob
        pygame.draw.circle(s, (160, 130, 65), (x0 + (BS // 2 - 3) - 4, BS * 3 // 4), 2)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _wardrobe_art(base):
    """Built-in fitted wardrobe panel with double door."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 35)
    # two door panels
    for i in range(2):
        x0 = 1 + i * (BS // 2)
        dw = BS // 2 - 2
        pygame.draw.rect(s, _darker_by(base, 5), (x0, 1, dw, BS - 2))
        # door panel recess
        inner = (x0 + 3, 4, dw - 6, BS - 10)
        pygame.draw.rect(s, _lighter(base, 8), inner)
        pygame.draw.lines(s, hi,   False,
                          [(x0 + 3, BS - 6), (x0 + 3, 4), (x0 + dw - 3, 4)], 1)
        pygame.draw.lines(s, dark, False,
                          [(x0 + 3, BS - 6), (x0 + dw - 3, BS - 6), (x0 + dw - 3, 4)], 1)
        # door knob
        kx = x0 + dw - 6 if i == 0 else x0 + 5
        pygame.draw.circle(s, (150, 120, 62), (kx, BS // 2), 2)
        pygame.draw.circle(s, dark, (kx, BS // 2), 2, 1)
    # centre gap
    pygame.draw.rect(s, dark, (BS // 2 - 1, 0, 2, BS))
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _settle_art(base):
    """High-back wooden settle with panelled back."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 30)
    # high back panels
    for i in range(2):
        px = 2 + i * (BS // 2 - 1)
        pygame.draw.rect(s, _lighter(base, 5), (px, 2, BS // 2 - 3, BS * 2 // 3))
        inner = (px + 2, 4, BS // 2 - 7, BS * 2 // 3 - 6)
        pygame.draw.rect(s, _darker_by(base, 5), inner)
        pygame.draw.lines(s, hi,   False,
                          [(px + 2, inner[1] + inner[3]), (px + 2, inner[1]), (inner[0] + inner[2], inner[1])], 1)
        pygame.draw.lines(s, dark, False,
                          [(px + 2, inner[1] + inner[3]), (inner[0] + inner[2], inner[1] + inner[3]), (inner[0] + inner[2], inner[1])], 1)
    # seat
    pygame.draw.rect(s, _darken(base, 10), (2, BS * 2 // 3, BS - 4, 5))
    pygame.draw.line(s, hi, (2, BS * 2 // 3), (BS - 2, BS * 2 // 3), 1)
    # legs
    for lx in (3, BS - 6):
        pygame.draw.rect(s, _darken(base, 12), (lx, BS * 2 // 3 + 5, 4, BS // 3 - 5))
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _plate_rack_art(base):
    """Wall-mounted plate rack with display slots."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 30)
    # back board
    pygame.draw.rect(s, _darken(base, 8), (0, 0, BS, BS))
    # horizontal rails
    for y in (BS // 5, BS // 5 * 2, BS // 5 * 3, BS // 5 * 4):
        pygame.draw.rect(s, _lighter(base, 10), (2, y - 2, BS - 4, 4))
        pygame.draw.line(s, hi, (2, y - 2), (BS - 2, y - 2), 1)
        pygame.draw.line(s, dark, (2, y + 2), (BS - 2, y + 2), 1)
    # plates in slots (simple ovals)
    plate_col = (235, 225, 210)
    for i in range(3):
        px = 4 + i * (BS // 3)
        pygame.draw.ellipse(s, plate_col, (px, BS // 5 - 6, BS // 3 - 4, 10))
        pygame.draw.ellipse(s, dark, (px, BS // 5 - 6, BS // 3 - 4, 10), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _dumbwaiter(base):
    """Dumbwaiter service shaft panel with track guides."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 25)
    # shaft surround
    pygame.draw.rect(s, _darken(base, 15), (0, 0, BS, BS))
    # vertical guide rails
    rail_col = (90, 80, 72)
    for rx in (BS // 4, 3 * BS // 4):
        pygame.draw.rect(s, rail_col, (rx - 2, 0, 4, BS))
        pygame.draw.line(s, hi, (rx - 1, 0), (rx - 1, BS), 1)
    # shelf/platform crossbar
    pygame.draw.rect(s, (125, 105, 82), (BS // 4 + 2, BS // 2 - 3, BS // 2 - 4, 6))
    pygame.draw.line(s, hi, (BS // 4 + 2, BS // 2 - 3), (3 * BS // 4 - 2, BS // 2 - 3), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _urn_pedestal(base):
    """Stone garden urn pedestal with moulded neck."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 35)
    cx = BS // 2
    # plinth base
    pygame.draw.rect(s, _darken(base, 10), (0, BS - 6, BS, 6))
    pygame.draw.line(s, hi, (0, BS - 6), (BS, BS - 6), 1)
    # tapered shaft
    for y in range(BS - 6, 6, -4):
        w = int(BS // 3 + (BS // 2 - BS // 3) * (BS - 6 - y) / (BS - 12))
        c = _lighter(base, 5) if y % 8 == 0 else base
        pygame.draw.rect(s, c, (cx - w, y - 4, w * 2, 4))
    # cap moulding
    pygame.draw.rect(s, _darken(base, 5), (cx - BS // 3, 2, BS // 3 * 2, 5))
    pygame.draw.line(s, hi, (cx - BS // 3, 2), (cx + BS // 3, 2), 1)
    # highlight edge lines
    pygame.draw.line(s, hi,   (cx - BS // 3 + 2, 6), (cx - BS // 5, BS - 7), 1)
    pygame.draw.line(s, dark, (cx + BS // 3 - 3, 6), (cx + BS // 5, BS - 7), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _sundial_pedestal(base):
    """Stone sundial column pedestal with carved panel."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 35)
    cx   = BS // 2
    # plinth
    pygame.draw.rect(s, _darken(base, 8), (0, BS - 5, BS, 5))
    # square column shaft
    pygame.draw.rect(s, _lighter(base, 5), (cx - BS // 4, 5, BS // 2, BS - 10))
    # carved panel on shaft
    inner = (cx - BS // 5, 8, BS // 5 * 2, BS // 3)
    pygame.draw.rect(s, _darker_by(base, 10), inner)
    pygame.draw.lines(s, hi,   False,
                      [(inner[0], inner[1] + inner[3]), (inner[0], inner[1]), (inner[0] + inner[2], inner[1])], 1)
    pygame.draw.lines(s, dark, False,
                      [(inner[0], inner[1] + inner[3]), (inner[0] + inner[2], inner[1] + inner[3]), (inner[0] + inner[2], inner[1])], 1)
    # cap
    pygame.draw.rect(s, _darken(base, 5), (cx - BS // 4 - 2, 2, BS // 2 + 4, 4))
    pygame.draw.line(s, hi, (cx - BS // 4 - 2, 2), (cx + BS // 4 + 2, 2), 1)
    # side face shading
    pygame.draw.line(s, dark, (cx + BS // 4 - 1, 5), (cx + BS // 4 - 1, BS - 5), 1)
    pygame.draw.line(s, hi,   (cx - BS // 4 + 1, 5), (cx - BS // 4 + 1, BS - 5), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _battered_wall(base):
    """Battered (sloped face) retaining wall — rough coursed stone."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 20)
    # battered courses — shifted left at each level
    course_h = BS // 5
    for row in range(5):
        slope = row * 2
        y     = row * course_h
        pygame.draw.line(s, dark, (0, y), (BS, y), 1)
        pygame.draw.line(s, hi,   (0, y + 1), (BS, y + 1), 1)
        # joint at mid-brick (offset per row)
        jx = (BS // 2 + slope) % BS
        pygame.draw.line(s, dark, (jx, y), (jx, y + course_h), 1)
    # rough stone face texture
    import random as _r
    _r.seed(hash(base) ^ 99)
    for _ in range(8):
        rx = _r.randint(2, BS - 5)
        ry = _r.randint(2, BS - 4)
        pygame.draw.rect(s, _darken(base, 25), (rx, ry, _r.randint(2, 6), _r.randint(1, 3)))
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s


def _coal_cellar(base):
    """Coal cellar block — rough stone with coal-black fill."""
    s = pygame.Surface((BS, BS))
    s.fill(base)
    dark = _darken(base, 40)
    hi   = _lighter(base, 18)
    # stone surround
    pygame.draw.rect(s, _darken(base, 12), (0, 0, BS, BS))
    pygame.draw.rect(s, _lighter(base, 5), (3, 3, BS - 6, BS - 6))
    # dark coal opening
    pygame.draw.rect(s, (28, 25, 22), (5, 5, BS - 10, BS - 10))
    # coal lumps
    coal_lo = (45, 42, 40)
    coal_hi = (65, 60, 58)
    for cx, cy, r in [(8, 10, 3), (15, 8, 2), (10, 16, 2), (18, 15, 3), (14, 22, 2)]:
        pygame.draw.circle(s, coal_lo, (cx, cy), r)
        pygame.draw.circle(s, coal_hi, (cx - 1, cy - 1), max(1, r - 1))
    # stone mortar border
    pygame.draw.rect(s, dark, (3, 3, BS - 6, BS - 6), 1)
    pygame.draw.rect(s, dark, (0, 0, BS, BS), 1)
    return s
