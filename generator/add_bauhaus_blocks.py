"""
One-shot script: adds all 100 Bauhaus/glass/artisan blocks to blocks.py,
items.py, and crafting.py. Run once from the project root.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent

# ── Block definitions ────────────────────────────────────────────────────────
# (constant_name, id, display_name, R, G, B, drop_item_id, hardness, comment)
BLOCKS = [
    # ── Bauhaus Glass (1284–1313) ─────────────────────────────────────────
    ("BAUHAUS_PLATE_GLASS",      1284, "Bauhaus Plate Glass",       218,233,245, "bauhaus_plate_glass",      2, "floor-to-ceiling frameless plate glass"),
    ("BAUHAUS_STRIP_WINDOW",     1285, "Strip Window",              215,230,242, "bauhaus_strip_window",     2, "horizontal band window; 3 panes, steel bars"),
    ("BAUHAUS_CORNER_GLASS",     1286, "Corner Glass Panel",        220,235,247, "bauhaus_corner_glass",     2, "90-degree glass corner unit"),
    ("BAUHAUS_CURTAIN_WALL",     1287, "Curtain Wall Unit",         210,228,240, "bauhaus_curtain_wall",     2, "steel-grid curtain wall panel 2x3"),
    ("BAUHAUS_GLASS_BRICK",      1288, "Glass Brick",               200,222,238, "bauhaus_glass_brick",      2, "solid cast glass brick; mortar-grid pattern"),
    ("BAUHAUS_FROSTED_STRIP",    1289, "Frosted Strip",             228,236,242, "bauhaus_frosted_strip",    2, "sandblasted horizontal-band frosted glass"),
    ("BAUHAUS_TINTED_STRIP",     1290, "Tinted Strip Window",        90,110,128, "bauhaus_tinted_strip",     2, "dark-tinted privacy strip window"),
    ("BAUHAUS_RED_PANEL",        1291, "Primary Red Panel",         200, 50, 40, "bauhaus_red_panel",        2, "Bauhaus primary red; opaque flat glass"),
    ("BAUHAUS_YELLOW_PANEL",     1292, "Primary Yellow Panel",      240,210, 30, "bauhaus_yellow_panel",     2, "Bauhaus primary yellow; opaque flat glass"),
    ("BAUHAUS_BLUE_PANEL",       1293, "Primary Blue Panel",         30, 80,180, "bauhaus_blue_panel",       2, "Bauhaus primary blue; opaque flat glass"),
    ("BAUHAUS_BLACK_GLASS",      1294, "Black Glass Panel",          22, 24, 28, "bauhaus_black_glass",      2, "near-black spandrel / shadow-box glass"),
    ("BAUHAUS_WHITE_GLASS",      1295, "Opaline White Glass",       242,245,248, "bauhaus_white_glass",      2, "opaline translucent white glass"),
    ("BAUHAUS_WIRE_GLASS",       1296, "Wire Glass",                195,215,230, "bauhaus_wire_glass",       2, "safety glass with embedded wire mesh"),
    ("BAUHAUS_CHANNEL_GLASS",    1297, "Channel Glass",             210,226,240, "bauhaus_channel_glass",    2, "U-profile channel glass; vertical ribs"),
    ("BAUHAUS_SANDBLAST_GLASS",  1298, "Sandblasted Glass",         225,232,238, "bauhaus_sandblast_glass",  2, "matte sandblasted surface; diffuse light"),
    ("BAUHAUS_ETCHED_GLASS",     1299, "Etched Glass",              222,234,244, "bauhaus_etched_glass",     2, "circle-in-square geometric etch"),
    ("BAUHAUS_DOUBLE_PANE",      1300, "Double Pane Unit",          214,230,242, "bauhaus_double_pane",      2, "insulated sealed double glazing"),
    ("BAUHAUS_GLASS_FLOOR",      1301, "Glass Floor Tile",          200,220,236, "bauhaus_glass_floor",      2, "structural glass floor panel"),
    ("BAUHAUS_CLERESTORY",       1302, "Clerestory Strip",          215,232,246, "bauhaus_clerestory",       2, "high-set clerestory window strip"),
    ("BAUHAUS_GREENHOUSE_PANE",  1303, "Greenhouse Pane",           200,228,210, "bauhaus_greenhouse_pane",  2, "thin greenhouse glass; greenish cast"),
    ("BAUHAUS_FRAMELESS_WALL",   1304, "Frameless Glass Wall",      220,236,248, "bauhaus_frameless_wall",   2, "structural frameless glass; no visible edge"),
    ("BAUHAUS_CANOPY_GLASS",     1305, "Glass Canopy",              205,228,244, "bauhaus_canopy_glass",     2, "sloped glass canopy / overhang panel"),
    ("BAUHAUS_SKYLIGHT",         1306, "Flat Skylight",             212,232,248, "bauhaus_skylight",         2, "flat steel-framed skylight with corner bolts"),
    ("BAUHAUS_JALOUSIE",         1307, "Jalousie Window",           210,228,240, "bauhaus_jalousie",         2, "louvered glass jalousie; 4 horizontal slats"),
    ("BAUHAUS_OPAQUE_GLASS",     1308, "Cast Opaque Glass",         175,200,218, "bauhaus_opaque_glass",     2, "dense poured-glass block; slight texture"),
    ("BAUHAUS_RIBBED_VERT",      1309, "Ribbed Vertical Glass",     212,230,244, "bauhaus_ribbed_vert",      2, "6 vertical ribs; alternating light/dark"),
    ("BAUHAUS_RIBBED_HORIZ",     1310, "Ribbed Horizontal Glass",   210,228,242, "bauhaus_ribbed_horiz",     2, "6 horizontal ribs; textured shower glass"),
    ("BAUHAUS_MIRROR_PANEL",     1311, "Mirror Panel",              185,200,215, "bauhaus_mirror_panel",     2, "polished flat mirror; no frame"),
    ("BAUHAUS_PRISM_GLASS",      1312, "Prism Glass",               215,232,246, "bauhaus_prism_glass",      2, "prismatic glass casting refraction bands"),
    ("BAUHAUS_SPANDREL",         1313, "Spandrel Panel",             50, 65, 80, "bauhaus_spandrel",         2, "opaque spandrel panel; hides floor slab"),
    # ── Steel & Metal Structural (1314–1338) ─────────────────────────────
    ("STEEL_I_BEAM",             1314, "Steel I-Beam",               75, 82, 88, "steel_i_beam",             2, "vertical steel I-section column"),
    ("STEEL_H_COLUMN",           1315, "Steel H-Column",             70, 78, 84, "steel_h_column",           2, "horizontal steel H-beam"),
    ("STEEL_ANGLE_BRACE",        1316, "Steel Angle Brace",          78, 85, 90, "steel_angle_brace",        2, "L-angle corner structural brace"),
    ("STEEL_MESH_PANEL",         1317, "Steel Mesh Panel",           82, 90, 96, "steel_mesh_panel",         2, "expanded steel mesh infill panel"),
    ("STEEL_GRATE_FLOOR",        1318, "Steel Grate Floor",          70, 80, 86, "steel_grate_floor",        2, "open-bar grate walkway floor"),
    ("STEEL_STAIR_TREAD",        1319, "Steel Stair Tread",          72, 80, 86, "steel_stair_tread",        2, "industrial checkered steel stair tread"),
    ("STEEL_RAILING_POST",       1320, "Steel Railing Post",         80, 88, 94, "steel_railing_post",       2, "tubular steel balcony railing post"),
    ("STEEL_CABLE_RAIL",         1321, "Cable Railing",              90, 98,104, "steel_cable_rail",         2, "tensioned cable railing; thin horizontal lines"),
    ("STEEL_PERFORATED",         1322, "Perforated Steel Panel",     78, 86, 92, "steel_perforated",         2, "punched-hole perforated steel cladding"),
    ("CORRUGATED_STEEL",         1323, "Corrugated Steel",           85, 92, 98, "corrugated_steel",         2, "corrugated metal wall/roof cladding"),
    ("ALUMINUM_CLADDING",        1324, "Brushed Aluminum",          168,172,178, "aluminum_cladding",        2, "smooth brushed-aluminum facade panel"),
    ("CHROME_TRIM",              1325, "Chrome Trim Strip",          195,200,208, "chrome_trim",              2, "polished chrome accent trim strip"),
    ("STEEL_DOOR_FRAME",         1326, "Steel Door Frame",           65, 72, 78, "steel_door_frame",         2, "bare steel door surround frame"),
    ("STEEL_WINDOW_FRAME",       1327, "Steel Window Frame",         68, 75, 80, "steel_window_frame",       2, "steel casement window frame"),
    ("STEEL_LOUVER",             1328, "Steel Louver Panel",         80, 88, 94, "steel_louver",             2, "horizontal steel louvred sunscreen"),
    ("STEEL_SOFFIT",             1329, "Steel Soffit Panel",         88, 94,100, "steel_soffit",             2, "steel underside/soffit cladding panel"),
    ("STEEL_FASCIA",             1330, "Steel Roof Fascia",          72, 80, 86, "steel_fascia",             2, "steel roof-edge fascia board"),
    ("STEEL_BALCONY_DECK",       1331, "Steel Balcony Deck",         75, 83, 89, "steel_balcony_deck",       2, "cantilevered steel balcony floor panel"),
    ("STEEL_SKYLIGHT_FRAME",     1332, "Skylight Frame",             70, 78, 84, "steel_skylight_frame",     2, "steel structural skylight surround"),
    ("ROUND_PIPE_COLUMN",        1333, "Round Pipe Column",          85, 92, 98, "round_pipe_column",        2, "exposed circular pipe column"),
    ("ROUND_PIPE_HORIZ",         1334, "Horizontal Pipe",            82, 90, 96, "round_pipe_horiz",         2, "exposed horizontal pipe / conduit run"),
    ("STEEL_GRID_CEILING",       1335, "Steel Grid Ceiling",         92, 98,104, "steel_grid_ceiling",       2, "suspended steel T-bar grid ceiling tile"),
    ("INDUSTRIAL_BRACKET",       1336, "Industrial Bracket",         68, 76, 82, "industrial_bracket",       2, "heavy-duty wall-mount steel bracket"),
    ("STEEL_THRESHOLD",          1337, "Steel Threshold",            80, 87, 93, "steel_threshold",          2, "steel floor transition threshold strip"),
    ("RIVETED_STEEL",            1338, "Riveted Steel Plate",        72, 79, 85, "riveted_steel",            2, "decorative riveted steel plate panel"),
    # ── Concrete Series (1339–1358) ──────────────────────────────────────
    ("BAUHAUS_CONCRETE_SMOOTH",  1339, "Smooth Concrete",           175,172,168, "bauhaus_concrete_smooth",  2, "fine-cast smooth poured concrete wall"),
    ("BAUHAUS_CONCRETE_BOARD",   1340, "Board-Form Concrete",       172,168,162, "bauhaus_concrete_board",   2, "board-formed concrete; subtle wood grain"),
    ("BAUHAUS_CONCRETE_POLISHED",1341, "Polished Concrete Floor",   182,180,176, "bauhaus_concrete_polished",2, "mirror-polished concrete floor slab"),
    ("BAUHAUS_CONCRETE_WHITE",   1342, "White Concrete",            225,222,218, "bauhaus_concrete_white",   2, "white Portland cement wall panel"),
    ("BAUHAUS_CONCRETE_CHARCOAL",1343, "Charcoal Concrete",          58, 58, 60, "bauhaus_concrete_charcoal",2, "dark charcoal pigmented concrete"),
    ("BAUHAUS_CONCRETE_WARM",    1344, "Buff Concrete",             192,185,170, "bauhaus_concrete_warm",    2, "warm buff / sandstone-tint concrete"),
    ("BAUHAUS_CONCRETE_PILLAR",  1345, "Concrete Pillar",           178,175,170, "bauhaus_concrete_pillar",  2, "round concrete column"),
    ("BAUHAUS_CONCRETE_CEILING", 1346, "Concrete Soffit",           168,165,162, "bauhaus_concrete_ceiling", 2, "flat exposed concrete ceiling panel"),
    ("BAUHAUS_CONCRETE_FASCIA",  1347, "Concrete Fascia",           180,177,173, "bauhaus_concrete_fascia",  2, "concrete roof-edge fascia"),
    ("BAUHAUS_CONCRETE_SCREEN",  1348, "Concrete Breeze Block",     175,172,168, "bauhaus_concrete_screen",  2, "open-grid decorative concrete screen"),
    ("BAUHAUS_CONCRETE_CURB",    1349, "Concrete Curb",             170,168,164, "bauhaus_concrete_curb",    2, "cast concrete curb / base trim"),
    ("BAUHAUS_CONCRETE_SILL",    1350, "Concrete Window Sill",      178,175,171, "bauhaus_concrete_sill",    2, "cast concrete window sill"),
    ("BAUHAUS_EXPOSED_AGGREGATE",1351, "Exposed Aggregate",         165,158,148, "bauhaus_exposed_aggregate",2, "exposed pebble-aggregate concrete surface"),
    ("BAUHAUS_POURED_FLOOR",     1352, "Poured Concrete Floor",     172,170,166, "bauhaus_poured_floor",     2, "seamless poured concrete floor"),
    ("BAUHAUS_PRECAST_PANEL",    1353, "Precast Concrete Panel",    178,174,170, "bauhaus_precast_panel",    2, "precast wall panel with seam lines"),
    ("BAUHAUS_CEILING_COFFER",   1354, "Coffered Concrete Ceiling", 168,166,162, "bauhaus_ceiling_coffer",   2, "grid-coffered concrete ceiling"),
    ("BAUHAUS_THIN_SHELL",       1355, "Thin-Shell Concrete",       180,177,173, "bauhaus_thin_shell",       2, "parabolic thin-shell concrete vault"),
    ("BAUHAUS_STAIR_TREAD",      1356, "Concrete Stair Tread",      170,168,164, "bauhaus_stair_tread",      2, "cast concrete stair tread"),
    ("BAUHAUS_HEARTH",           1357, "Concrete Hearth",           182,178,174, "bauhaus_hearth",           2, "polished concrete fireplace surround"),
    ("BAUHAUS_CONCRETE_MOSAIC",  1358, "Colored Aggregate Floor",   168,162,155, "bauhaus_concrete_mosaic",  2, "colored pebble-aggregate mosaic floor"),
    # ── Wood & Natural Trim (1359–1373) ──────────────────────────────────
    ("TEAK_SLAT_WALL",           1359, "Teak Slat Wall",            145, 95, 55, "teak_slat_wall",           2, "horizontal teak slat exterior cladding"),
    ("WALNUT_STRIP_FLOOR",       1360, "Walnut Strip Floor",         92, 62, 38, "walnut_strip_floor",       2, "narrow walnut strip hardwood floor"),
    ("BIRCH_VENEER_PANEL",       1361, "Birch Veneer Panel",        225,208,180, "birch_veneer_panel",       2, "light birch plywood veneer wall panel"),
    ("BAMBOO_CEILING_BATTEN",    1362, "Bamboo Ceiling Batten",     210,195,140, "bamboo_ceiling_batten",    2, "bamboo batten ceiling cladding"),
    ("CORK_TILE",                1363, "Natural Cork Tile",          195,162,110, "cork_tile",                2, "natural cork acoustic floor tile"),
    ("MAPLE_STRIP_FLOOR",        1364, "Maple Strip Floor",         215,185,138, "maple_strip_floor",        2, "light maple narrow-strip hardwood floor"),
    ("WHITEWASH_PLANK",          1365, "Whitewashed Plank",         232,228,220, "whitewash_plank",          2, "whitewashed pine cladding plank"),
    ("SMOKED_OAK_PANEL",         1366, "Smoked Oak Panel",           58, 48, 40, "smoked_oak_panel",         2, "ebonized / smoked oak wall panel"),
    ("ASH_VENEER",               1367, "Pale Ash Veneer",           212,200,180, "ash_veneer",               2, "pale ash wood veneer panel"),
    ("TEAK_DECK_BOARD",          1368, "Teak Deck Board",           148, 98, 58, "teak_deck_board",          2, "outdoor teak decking board"),
    ("WENGE_ACCENT",             1369, "Wenge Accent Strip",         38, 28, 22, "wenge_accent",             2, "very dark wenge accent trim strip"),
    ("ZEBRANO_PANEL",            1370, "Zebrano Veneer Panel",      188,162,110, "zebrano_panel",            2, "exotic zebrano wood; dramatic stripe grain"),
    ("RECLAIMED_PINE",           1371, "Reclaimed Pine Plank",      185,155,112, "reclaimed_pine",           2, "weathered reclaimed pine with knots"),
    ("REED_SCREEN_PANEL",        1372, "Reed Screen Panel",         195,178,132, "reed_screen_panel",        2, "natural reed / bamboo privacy screen"),
    ("HEMP_BOARD",               1373, "Hemp Composite Board",      180,168,135, "hemp_board",               2, "compressed hemp-fiber composite panel"),
    # ── Tile, Floor & Bauhaus Color (1374–1383) ──────────────────────────
    ("BLACK_CERAMIC_TILE",       1374, "Black Ceramic Tile",         28, 28, 30, "black_ceramic_tile",       2, "high-gloss black ceramic floor/wall tile"),
    ("WHITE_PORCELAIN_TILE",     1375, "White Porcelain Tile",      242,242,244, "white_porcelain_tile",     2, "high-gloss white porcelain tile"),
    ("BAUHAUS_MOSAIC_TILE",      1376, "Bauhaus Mosaic Tile",       200, 50, 40, "bauhaus_mosaic_tile",      2, "primary-color circle-triangle-square mosaic"),
    ("CHECKER_TILE",             1377, "Checkerboard Tile",         240,238,235, "checker_tile",             2, "classic black and white checkerboard"),
    ("BAUHAUS_TERRAZZO",         1378, "Bauhaus Terrazzo",          195,188,178, "bauhaus_terrazzo",         2, "terrazzo with glass chip aggregate"),
    ("BAUHAUS_RED_WALL",         1379, "Primary Red Wall",          198, 48, 38, "bauhaus_red_wall",         2, "matte Bauhaus primary red wall panel"),
    ("BAUHAUS_YELLOW_WALL",      1380, "Primary Yellow Wall",       238,208, 28, "bauhaus_yellow_wall",      2, "matte Bauhaus primary yellow wall panel"),
    ("BAUHAUS_BLUE_WALL",        1381, "Primary Blue Wall",          28, 78,178, "bauhaus_blue_wall",        2, "matte Bauhaus primary blue wall panel"),
    ("WHITE_STUCCO",             1382, "White Stucco",              238,236,232, "white_stucco",             2, "smooth white exterior stucco plaster"),
    ("LIME_PLASTER",             1383, "Lime Plaster",              228,222,210, "lime_plaster",             2, "off-white lime plaster interior wall"),
]


def patch_blocks_py():
    text = (ROOT / "blocks.py").read_text(encoding="utf-8")

    # 1. Insert ID constants after PIPE_SORTER_BLOCK line
    const_lines = "\n# ── Bauhaus Glass & Artisan Collection (1284–1383) ─────────────────────────\n"
    prev_cat = None
    cat_comments = {
        1284: "# — Bauhaus Glass —",
        1314: "# — Steel & Metal Structural —",
        1339: "# — Concrete —",
        1359: "# — Wood & Natural Trim —",
        1374: "# — Tile, Floor & Bauhaus Color —",
    }
    for row in BLOCKS:
        cname, bid, dname, r, g, b, drop, hard, comment = row
        if bid in cat_comments:
            const_lines += cat_comments[bid] + "\n"
        const_lines += f"{cname:<28} = {bid}  # {comment}\n"

    text = text.replace(
        "PIPE_SORTER_BLOCK  = 1283  # routes item types to configured exit directions\n",
        "PIPE_SORTER_BLOCK  = 1283  # routes item types to configured exit directions\n"
        + const_lines,
    )

    # 2. Insert BLOCKS dict entries after PIPE_SORTER_BLOCK entry
    dict_lines = "\n    # --- Bauhaus Glass & Artisan Collection ---\n"
    for row in BLOCKS:
        cname, bid, dname, r, g, b, drop, hard, comment = row
        dict_lines += (
            f"    {cname:<28}: "
            f'{{\"name\": \"{dname}\", \"hardness\": {hard}, '
            f'"color": ({r:3d}, {g:3d}, {b:3d}), \"drop\": \"{drop}\"}},\n'
        )

    text = text.replace(
        '    PIPE_SORTER_BLOCK:         {"name": "Pipe Sorter",',
        dict_lines + '    PIPE_SORTER_BLOCK:         {"name": "Pipe Sorter",',
    )

    (ROOT / "blocks.py").write_text(text, encoding="utf-8")
    print("blocks.py: patched")


def patch_items_py():
    text = (ROOT / "items.py").read_text(encoding="utf-8")

    # 1. Extend the from blocks import (...) statement
    import_addition = ",\n                    " + ",\n                    ".join(
        row[0] for row in BLOCKS
    )
    text = text.replace(
        "HOPPER_BLOCK, PIPE_OUTPUT_BLOCK, PIPE_FILTER_BLOCK, PIPE_SORTER_BLOCK)",
        "HOPPER_BLOCK, PIPE_OUTPUT_BLOCK, PIPE_FILTER_BLOCK, PIPE_SORTER_BLOCK"
        + import_addition + ")",
    )

    # 2. Insert ITEMS entries before the closing }
    items_lines = "\n    # --- Bauhaus Glass & Artisan Collection ---\n"
    for row in BLOCKS:
        cname, bid, dname, r, g, b, drop, hard, comment = row
        items_lines += (
            f"    \"{drop}\":{' ' * max(1, 28 - len(drop))}"
            f'{{\"name\": \"{dname}\", \"color\": ({r:3d}, {g:3d}, {b:3d}), \"place_block\": {cname}}},\n'
        )

    # Find last line before closing }
    text = text.rstrip()
    if text.endswith("}"):
        text = text[:-1] + items_lines + "}"
    else:
        raise RuntimeError("Could not find closing } in items.py")

    (ROOT / "items.py").write_text(text, encoding="utf-8")
    print("items.py: patched")


def patch_crafting_py():
    text = (ROOT / "crafting.py").read_text(encoding="utf-8")

    recipe_lines = "\n    # --- Bauhaus Glass & Artisan Collection ---\n"
    # Category-specific ingredient defaults
    glass_ids   = set(r[0] for r in BLOCKS if 1284 <= r[1] <= 1313)
    steel_ids   = set(r[0] for r in BLOCKS if 1314 <= r[1] <= 1338)
    concrete_ids= set(r[0] for r in BLOCKS if 1339 <= r[1] <= 1358)
    wood_ids    = set(r[0] for r in BLOCKS if 1359 <= r[1] <= 1373)
    tile_ids    = set(r[0] for r in BLOCKS if 1374 <= r[1] <= 1383)

    for row in BLOCKS:
        cname, bid, dname, r, g, b, drop, hard, comment = row
        if cname in glass_ids:
            ings = '{"clear_glass": 2, "iron_chunk": 1}'
        elif cname in steel_ids:
            ings = '{"iron_ingot": 3, "coal_chunk": 1}'
        elif cname in concrete_ids:
            ings = '{"stone_chip": 3, "gravel": 1}'
        elif cname in wood_ids:
            # pick appropriate plank based on color brightness
            brightness = r + g + b
            if brightness > 580:
                plank = "ash_plank"
            elif brightness > 450:
                plank = "oak_panel"
            elif brightness > 300:
                plank = "teak_plank"
            else:
                plank = "ebony_plank"
            ings = f'{{"{plank}": 4}}'
        else:  # tile / color
            ings = '{"stone_chip": 2, "sand": 1}'

        recipe_lines += (
            f'    {{"name": "{dname}", '
            f'"ingredients": {ings}, '
            f'"output_id": "{drop}", "output_count": 2}},\n'
        )

    # Insert before closing ] of ARTISAN_RECIPES
    # Find the last {"name": ... entry, then the ] after it
    idx = text.rfind('{"name": "Fur Vest"')
    closing = text.index("]", idx)
    text = text[:closing] + recipe_lines + text[closing:]

    (ROOT / "crafting.py").write_text(text, encoding="utf-8")
    print("crafting.py: patched")


if __name__ == "__main__":
    patch_blocks_py()
    patch_items_py()
    patch_crafting_py()
    print(f"\nDone — {len(BLOCKS)} blocks added (IDs {BLOCKS[0][1]}–{BLOCKS[-1][1]})")
    print("Next steps:")
    print("  1. Create Render/blocks_bauhaus.py with build_bauhaus_surfs()")
    print("  2. Add surfs.update(build_bauhaus_surfs()) to Render/blockRenderHandler.py")
