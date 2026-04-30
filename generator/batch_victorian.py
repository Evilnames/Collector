#!/usr/bin/env python3
"""
batch_victorian.py — Add all 250 Victorian & Craftsman home blocks in one pass.

Usage:
    python generator/batch_victorian.py
    python generator/batch_victorian.py --dry-run
"""
import argparse
import re
import sys
from pathlib import Path

ROOT        = Path(__file__).parent.parent
BLOCKS_PY   = ROOT / "blocks.py"
ITEMS_PY    = ROOT / "items.py"
CRAFTING_PY = ROOT / "crafting.py"

IMPORT_INDENT = " " * 20
SET_INDENT    = " " * 20

# ── 250 Victorian / Craftsman blocks ──────────────────────────────────────────
# (name, R, G, B, hardness, recipe_ingredients)
# hardness: 1=soft decorative, 2=wood/plaster, 3=brick/stone, 4=dense masonry
BLOCKS_TO_ADD = [
    # ── Exterior Siding & Cladding ─────────────────────────────────────────────
    ("Fish Scale Shingle",          178,  90,  80,  2, {"plank": 4, "chisel": 1}),
    ("Fish Scale Shingle Dark",      80,  55,  55,  2, {"plank": 4, "dye_black": 1}),
    ("Fish Scale Shingle Blue",      75,  95, 120,  2, {"plank": 4, "dye_blue": 1}),
    ("Clapboard Siding",            235, 228, 210,  2, {"plank": 3}),
    ("Clapboard Siding Dark",       100,  75,  55,  2, {"plank": 3, "tar": 1}),
    ("Drop Siding",                 195, 175, 145,  2, {"plank": 3}),
    ("Board and Batten Siding",     140, 155, 120,  2, {"plank": 4, "nail": 2}),
    ("Shiplap Siding",              230, 225, 215,  2, {"plank": 4}),
    ("Pebbledash Render",           185, 180, 170,  3, {"stone_chip": 3, "sand": 2}),
    ("Half Timbering Panel",        210, 200, 185,  2, {"plank": 2, "lime_plaster": 2}),
    ("Terracotta Cladding Tile",    195, 105,  65,  3, {"clay_brick": 4}),
    ("Faience Tile Panel",           80, 165, 165,  3, {"clay_brick": 2, "dye_teal": 1}),
    ("Pressed Metal Panel",         160, 158, 155,  2, {"iron_ingot": 2}),
    ("Incised Render Panel",        210, 205, 195,  3, {"lime_plaster": 3, "chisel": 1}),
    ("Roughcast Render",            175, 172, 165,  3, {"stone_chip": 2, "sand": 2}),
    ("Pargeting Panel",             225, 220, 210,  3, {"lime_plaster": 4, "chisel": 1}),
    ("Stucco Band",                 235, 232, 225,  2, {"lime_plaster": 2, "sand": 1}),
    ("Decorative Frieze Panel",     225, 215, 200,  2, {"plank": 2, "chisel": 1}),
    ("Vergeboard",                   80,  55,  40,  2, {"plank": 3, "chisel": 1}),
    ("Dentil Moulding Strip",       235, 230, 220,  2, {"lime_plaster": 2, "chisel": 1}),

    # ── Roof & Gable ───────────────────────────────────────────────────────────
    ("Slate Roof Tile",             100, 105, 110,  3, {"stone_chip": 4}),
    ("Slate Roof Tile Dark",         60,  62,  68,  3, {"stone_chip": 4, "dye_black": 1}),
    ("Clay Roof Tile",              190,  95,  65,  3, {"clay_brick": 3}),
    ("Clay Roof Tile Green",         85, 120,  80,  3, {"clay_brick": 3, "dye_green": 1}),
    ("Imbrex Roof Tile",            170,  80,  55,  3, {"clay_brick": 3}),
    ("Mansard Slate Panel",          90,  92,  98,  3, {"stone_chip": 3}),
    ("Decorated Ridge Tile",        185,  90,  60,  3, {"clay_brick": 3, "chisel": 1}),
    ("Finial Block",                 70,  65,  80,  3, {"stone_chunk": 2, "chisel": 1}),
    ("Iron Cresting Rail",           45,  42,  40,  2, {"iron_ingot": 2, "coal": 1}),
    ("Jerkinhead Gable",            100, 105, 110,  3, {"stone_chip": 3, "plank": 1}),
    ("Turret Cap Block",             95, 105, 120,  3, {"stone_chip": 3}),
    ("Octagonal Turret Block",      140, 145, 155,  3, {"stone_chip": 4}),
    ("Bay Window Roof",             100, 105, 110,  3, {"stone_chip": 2, "plank": 2}),
    ("Dormer Cheek",                220, 215, 205,  2, {"plank": 2, "lime_plaster": 1}),
    ("Gabled Dormer Front",         220, 215, 200,  2, {"plank": 3, "chisel": 1}),

    # ── Brick & Masonry ────────────────────────────────────────────────────────
    ("Pressed Brick",               185,  78,  58,  3, {"clay_brick": 4}),
    ("Pressed Brick Buff",          210, 185, 140,  3, {"clay_brick": 4, "sand": 1}),
    ("Gauged Brick",                170,  70,  55,  3, {"clay_brick": 5, "chisel": 1}),
    ("Rubbed Brick",                210, 160, 145,  3, {"clay_brick": 4, "chisel": 1}),
    ("Vitrified Brick",              90,  95, 105,  4, {"clay_brick": 4, "coal": 2}),
    ("Polychrome Brick Red",        185,  78,  58,  3, {"clay_brick": 3, "dye_red": 1}),
    ("Polychrome Brick Blue",        80,  90, 130,  3, {"clay_brick": 3, "dye_blue": 1}),
    ("Polychrome Brick Cream",      220, 210, 190,  3, {"clay_brick": 3, "sand": 1}),
    ("Terracotta Block",            195, 105,  60,  3, {"clay_brick": 4}),
    ("Terracotta Panel",            190, 100,  55,  3, {"clay_brick": 3, "chisel": 1}),
    ("Buff Terracotta",             215, 185, 130,  3, {"clay_brick": 3, "sand": 1}),
    ("Rusticated Stone",            140, 135, 125,  4, {"stone_chunk": 3, "chisel": 1}),
    ("Ashlar Stone Block",          195, 190, 180,  4, {"stone_chunk": 3, "chisel": 1}),
    ("Rock Faced Stone",            130, 125, 115,  4, {"stone_chunk": 3}),
    ("Vermiculated Stone",          165, 160, 150,  4, {"stone_chunk": 3, "chisel": 2}),
    ("Quoin Block",                 200, 195, 185,  4, {"stone_chunk": 2, "chisel": 1}),
    ("String Course Block",         205, 200, 188,  3, {"stone_chunk": 2}),
    ("Plinth Block",                155, 150, 140,  4, {"stone_chunk": 3}),
    ("Arch Keystone Block",         210, 205, 195,  4, {"stone_chunk": 2, "chisel": 2}),
    ("Voussoir Block",              205, 200, 190,  4, {"stone_chunk": 2, "chisel": 1}),

    # ── Carved Stone Ornament ──────────────────────────────────────────────────
    ("Tympanum Panel",              215, 210, 200,  4, {"stone_chunk": 3, "chisel": 2}),
    ("Medallion Block",             225, 220, 210,  3, {"stone_chunk": 2, "chisel": 2}),
    ("Cartouche Block",             220, 210, 185,  3, {"stone_chunk": 2, "gold_ingot": 1, "chisel": 2}),
    ("Heraldic Panel",              210, 190, 165,  3, {"stone_chunk": 3, "chisel": 2}),
    ("Florentine Stone",            200, 195, 180,  4, {"stone_chunk": 4, "chisel": 2}),

    # ── Columns & Structural Ornament ─────────────────────────────────────────
    ("Ionic Column",                235, 232, 228,  4, {"stone_chunk": 4, "chisel": 2}),
    ("Doric Column",                230, 228, 225,  4, {"stone_chunk": 4, "chisel": 1}),
    ("Corinthian Column Shaft",     235, 230, 225,  4, {"stone_chunk": 4, "chisel": 3}),
    ("Column Capital",              240, 235, 228,  4, {"stone_chunk": 2, "chisel": 3}),
    ("Column Base",                 228, 225, 218,  4, {"stone_chunk": 2, "chisel": 1}),
    ("Pilaster Block",              230, 228, 222,  3, {"stone_chunk": 2, "chisel": 1}),
    ("Engaged Column Block",        232, 228, 222,  4, {"stone_chunk": 3, "chisel": 2}),
    ("Fluted Panel",                225, 222, 215,  3, {"stone_chunk": 2, "chisel": 2}),
    ("Bracket Support",             115,  85,  55,  2, {"plank": 2, "chisel": 1}),
    ("Knee Brace",                  100,  72,  45,  2, {"plank": 3}),
    ("Corbel Block",                155, 150, 140,  4, {"stone_chunk": 2, "chisel": 1}),
    ("Modillion Block",             235, 230, 220,  3, {"stone_chunk": 1, "chisel": 1}),
    ("Console Bracket",             225, 220, 210,  3, {"stone_chunk": 2, "chisel": 1}),
    ("Cantilever Beam End",         110,  82,  52,  2, {"plank": 2}),
    ("Exposed Rafter End",          150, 120,  80,  2, {"plank": 2}),

    # ── Windows & Glazing ─────────────────────────────────────────────────────
    ("Stained Glass Red",           200,  50,  45,  1, {"iron_ingot": 1, "dye_red": 2}),
    ("Stained Glass Blue",           40,  80, 190,  1, {"iron_ingot": 1, "dye_blue": 2}),
    ("Stained Glass Amber",         215, 155,  35,  1, {"iron_ingot": 1, "dye_yellow": 2}),
    ("Stained Glass Green",          50, 160,  80,  1, {"iron_ingot": 1, "dye_green": 2}),
    ("Stained Glass Purple",        120,  50, 175,  1, {"iron_ingot": 1, "dye_purple": 2}),
    ("Leaded Light Panel",          190, 200, 210,  1, {"iron_ingot": 1, "sand": 1}),
    ("Quarry Glass Panel",          195, 205, 210,  1, {"iron_ingot": 1, "sand": 1}),
    ("Frosted Glass Panel",         225, 228, 232,  1, {"sand": 2, "limestone": 1}),
    ("Etched Glass Panel",          210, 215, 220,  1, {"sand": 2, "chisel": 1}),
    ("Coloured Border Glass",       200, 185, 160,  1, {"sand": 2, "dye_yellow": 1}),
    ("Bay Window Frame",             65,  50,  38,  2, {"plank": 4}),
    ("Oriel Window Frame",           70,  55,  40,  2, {"plank": 4, "chisel": 1}),
    ("Transom Window Frame",         75,  60,  45,  2, {"plank": 2}),
    ("Fanlight Frame",               55,  52,  50,  2, {"iron_ingot": 2, "sand": 1}),
    ("Gothic Arch Window",           70,  55,  42,  2, {"plank": 3, "stone_chip": 1}),
    ("Round Arch Window",            68,  53,  40,  2, {"plank": 3}),
    ("Palladian Window Frame",       72,  57,  42,  2, {"plank": 4, "stone_chip": 1}),
    ("Sash Window Frame",           225, 222, 215,  2, {"plank": 3}),
    ("Casement Window Frame",        75,  60,  45,  2, {"plank": 3}),
    ("Venetian Window Frame",        80,  65,  48,  2, {"plank": 4, "chisel": 1}),

    # ── Doors & Entries ───────────────────────────────────────────────────────
    ("Panelled Door Block",          75,  52,  35,  2, {"plank": 4, "iron_ingot": 1}),
    ("Glazed Door Block",            80,  58,  38,  2, {"plank": 3, "sand": 1}),
    ("Double Door Block",            72,  50,  33,  2, {"plank": 6, "iron_ingot": 2}),
    ("Dutch Door Block",             95, 110,  75,  2, {"plank": 4, "iron_ingot": 1}),
    ("Sliding Pocket Door Block",    85,  65,  45,  2, {"plank": 4}),
    ("Fanlight Surround",           200, 195, 182,  3, {"stone_chunk": 2, "chisel": 1}),
    ("Pilaster Door Surround",      220, 215, 205,  3, {"stone_chunk": 3, "chisel": 1}),
    ("Hood Moulding",               195, 190, 182,  3, {"stone_chunk": 2, "chisel": 1}),
    ("Porch Entry Steps",           165, 160, 155,  4, {"stone_chunk": 4}),
    ("Boot Scraper Block",           55,  52,  50,  2, {"iron_ingot": 2}),
    ("Door Knocker Plate",          170, 140,  80,  2, {"copper_ingot": 2}),
    ("Letterbox Panel",             175, 145,  82,  2, {"copper_ingot": 1, "iron_ingot": 1}),
    ("Marble Threshold",            235, 232, 228,  4, {"stone_chunk": 2, "chisel": 1}),
    ("Storm Door Block",            180, 185, 190,  2, {"plank": 2, "iron_ingot": 1}),
    ("Service Door Block",           90,  75,  60,  2, {"plank": 3}),

    # ── Porches & Verandas ────────────────────────────────────────────────────
    ("Porch Column",                235, 232, 228,  2, {"plank": 3, "chisel": 1}),
    ("Ornate Porch Column",         238, 235, 230,  2, {"plank": 4, "chisel": 2}),
    ("Spindle Rail",                238, 235, 230,  2, {"plank": 3, "chisel": 1}),
    ("Newel Post",                   90,  68,  45,  2, {"plank": 3, "chisel": 1}),
    ("Baluster Block",              235, 232, 225,  2, {"plank": 2, "chisel": 1}),
    ("Porch Balustrade",            232, 230, 222,  2, {"plank": 4}),
    ("Porch Cornice",               232, 228, 218,  2, {"plank": 3, "chisel": 1}),
    ("Veranda Bracket",             238, 235, 228,  2, {"plank": 2, "chisel": 1}),
    ("Porch Ceiling Board",         185, 210, 215,  2, {"plank": 3}),
    ("Porch Floor Board",           115,  82,  52,  2, {"plank": 4}),
    ("Screen Porch Panel",          175, 180, 185,  2, {"iron_ingot": 2, "plank": 1}),
    ("Porte Cochere Beam",          100,  75,  48,  2, {"plank": 5}),
    ("Pergola Post",                 90,  70,  48,  2, {"plank": 3}),
    ("Pergola Beam",                 95,  73,  50,  2, {"plank": 4}),
    ("Pergola Slat",                100,  77,  52,  2, {"plank": 2}),
    ("Porch Swing Bracket",         110,  82,  55,  2, {"iron_ingot": 1, "plank": 2}),
    ("Wisteria Trellis",            230, 235, 230,  2, {"plank": 2}),
    ("Lattice Panel",               235, 232, 228,  2, {"plank": 2}),
    ("Jigsaw Trim Panel",           238, 232, 220,  2, {"plank": 2, "chisel": 1}),
    ("Gingerbread Trim",            235, 225, 208,  2, {"plank": 3, "chisel": 2}),

    # ── Interior Walls & Trim ─────────────────────────────────────────────────
    ("Wainscot Panel Oak",          155, 120,  75,  2, {"plank": 4}),
    ("Wainscot Panel Dark",          75,  52,  35,  2, {"plank": 4, "tar": 1}),
    ("Beadboard Panel",             235, 232, 225,  2, {"plank": 3}),
    ("Raised Panel Wall",           200, 175, 138,  2, {"plank": 4, "chisel": 1}),
    ("Lincrusta Panel",             228, 222, 210,  2, {"lime_plaster": 3, "chisel": 1}),
    ("Anaglypta Panel",             238, 235, 230,  2, {"lime_plaster": 2}),
    ("Dado Rail",                   235, 232, 222,  2, {"plank": 2, "chisel": 1}),
    ("Picture Rail",                230, 228, 218,  2, {"plank": 2}),
    ("Crown Moulding",              240, 238, 232,  2, {"plank": 2, "lime_plaster": 1, "chisel": 1}),
    ("Coved Cornice",               238, 235, 228,  2, {"lime_plaster": 3}),
    ("Dentil Cornice",              240, 237, 230,  2, {"lime_plaster": 3, "chisel": 1}),
    ("Egg and Dart Moulding",       238, 235, 228,  2, {"lime_plaster": 2, "chisel": 1}),
    ("Ovolo Moulding",              240, 238, 232,  2, {"plank": 1, "lime_plaster": 1}),
    ("Tall Baseboard",              238, 235, 228,  2, {"plank": 2}),
    ("Dark Baseboard",               82,  62,  42,  2, {"plank": 2, "tar": 1}),
    ("Architrave",                  238, 234, 226,  2, {"plank": 2, "chisel": 1}),
    ("Fluted Interior Pilaster",    232, 228, 220,  3, {"stone_chunk": 2, "chisel": 2}),
    ("Smooth Plaster Panel",        228, 225, 218,  2, {"lime_plaster": 3}),
    ("Plaster Ceiling Rose",        240, 238, 234,  2, {"lime_plaster": 3, "chisel": 1}),
    ("Coffered Ceiling Panel",      232, 228, 220,  2, {"plank": 3, "chisel": 1}),
    ("Embossed Tin Ceiling Silver", 185, 188, 192,  2, {"iron_ingot": 2}),
    ("Embossed Tin Ceiling Gold",   195, 175, 100,  2, {"iron_ingot": 1, "gold_ingot": 1}),
    ("Shiplap Interior",            232, 228, 220,  2, {"plank": 3}),
    ("Tongue Groove Plank",         185, 158, 118,  2, {"plank": 3}),
    ("Wide Board Panelling",        148, 118,  78,  2, {"plank": 4}),

    # ── Floors & Stairs ───────────────────────────────────────────────────────
    ("Encaustic Floor Tile Red",    185,  72,  55,  3, {"clay_brick": 3, "dye_red": 1}),
    ("Encaustic Floor Tile Blue",    68,  85, 148,  3, {"clay_brick": 3, "dye_blue": 1}),
    ("Encaustic Floor Tile Green",   72, 115,  72,  3, {"clay_brick": 3, "dye_green": 1}),
    ("Encaustic Border Tile",       165,  62,  50,  3, {"clay_brick": 4, "chisel": 1}),
    ("Geometric Mosaic Floor",      195, 185, 165,  3, {"stone_chip": 4, "chisel": 1}),
    ("Parquet Floor Herringbone",   140, 108,  68,  2, {"plank": 4, "chisel": 1}),
    ("Parquet Floor Basket",        148, 115,  72,  2, {"plank": 4, "chisel": 1}),
    ("Parquet Floor Strip",         135, 102,  65,  2, {"plank": 4}),
    ("Marble Floor Tile",           235, 232, 228,  4, {"stone_chunk": 3, "chisel": 1}),
    ("Marble Floor Tile Black",      42,  40,  45,  4, {"stone_chunk": 3, "dye_black": 1, "chisel": 1}),
    ("Terracotta Floor Tile",       188,  98,  62,  3, {"clay_brick": 3}),
    ("Flagstone Floor",             140, 135, 128,  3, {"stone_chunk": 3}),
    ("Hardwood Stair Tread",        115,  85,  52,  2, {"plank": 3}),
    ("Painted Stair Riser",         238, 235, 228,  2, {"plank": 2}),
    ("Brass Stair Nosing",          195, 165,  80,  2, {"copper_ingot": 1, "gold_ingot": 1}),
    ("Open Riser Stair Step",       120,  90,  58,  2, {"plank": 3}),
    ("Landing Board",               130,  98,  62,  2, {"plank": 4}),
    ("Balcony Deck Board",          115,  82,  52,  2, {"plank": 4}),
    ("Cellar Stone Floor",          115, 112, 108,  3, {"stone_chunk": 3}),
    ("Tile Threshold Strip",        178,  72,  55,  3, {"clay_brick": 2, "chisel": 1}),

    # ── Fireplaces & Built-ins ─────────────────────────────────────────────────
    ("Fireplace Mantel",            235, 232, 225,  2, {"plank": 4, "chisel": 2}),
    ("Fireplace Surround Tile",     210, 200, 185,  3, {"clay_brick": 4, "chisel": 1}),
    ("Fireplace Overmantel",        225, 210, 188,  2, {"plank": 4, "chisel": 2}),
    ("Cast Iron Grate Front",        45,  42,  40,  3, {"iron_ingot": 3}),
    ("Cast Iron Fireback",           48,  45,  43,  3, {"iron_ingot": 3, "chisel": 1}),
    ("Hearth Tile",                 190, 100,  60,  3, {"clay_brick": 3, "chisel": 1}),
    ("Inglenook Side Wall",         172, 140, 108,  2, {"stone_chunk": 2, "plank": 1}),
    ("Inglenook Bench",             120,  90,  60,  2, {"plank": 3}),
    ("Oak Bookcase",                 90,  65,  40,  2, {"plank": 5}),
    ("Painted Bookcase",            230, 228, 222,  2, {"plank": 5, "lime_plaster": 1}),
    ("Window Seat Box",             155, 125,  85,  2, {"plank": 4}),
    ("Alcove Shelf",                145, 115,  75,  2, {"plank": 3}),
    ("Butler Pantry Shelf",         180, 155, 118,  2, {"plank": 4}),
    ("China Cabinet Block",         100,  75,  50,  2, {"plank": 5, "sand": 1}),
    ("Built In Wardrobe Panel",     115,  88,  58,  2, {"plank": 5}),
    ("High Back Settle",             80,  58,  38,  2, {"plank": 4, "chisel": 1}),
    ("Plate Rack",                  158, 128,  88,  2, {"plank": 3, "iron_ingot": 1}),
    ("Dresser Back Panel",          185, 158, 120,  2, {"plank": 4}),
    ("Pantry Door Block",            88,  68,  48,  2, {"plank": 3}),
    ("Dumbwaiter Shaft Panel",       65,  55,  48,  3, {"plank": 2, "iron_ingot": 2}),

    # ── Garden & Exterior Features ────────────────────────────────────────────
    ("Wrought Iron Fence Panel",     45,  42,  40,  2, {"iron_ingot": 3, "coal": 1}),
    ("Wrought Iron Gate",            48,  44,  42,  2, {"iron_ingot": 4, "coal": 1}),
    ("Brick Garden Pier",           182,  80,  58,  3, {"clay_brick": 4}),
    ("Stone Garden Pier",           165, 160, 150,  4, {"stone_chunk": 4}),
    ("Cast Iron Railing Panel",      52,  50,  48,  3, {"iron_ingot": 3}),
    ("Low Garden Wall",             178,  82,  60,  3, {"clay_brick": 3}),
    ("Garden Wall Coping",          195, 190, 182,  3, {"stone_chunk": 2}),
    ("Stone Garden Balustrade",     185, 182, 175,  4, {"stone_chunk": 3, "chisel": 1}),
    ("Stone Garden Steps",          170, 165, 158,  4, {"stone_chunk": 4}),
    ("Battered Retaining Wall",     148, 142, 135,  4, {"stone_chunk": 4}),
    ("Coal Hole Cover",              52,  50,  48,  3, {"iron_ingot": 2}),
    ("Area Steps Block",            155, 152, 148,  4, {"stone_chunk": 3}),
    ("Mounting Block",              162, 158, 152,  4, {"stone_chunk": 3}),
    ("Garden Urn Pedestal",         185, 182, 175,  3, {"stone_chunk": 2, "chisel": 1}),
    ("Sundial Pedestal",            188, 185, 178,  3, {"stone_chunk": 2, "chisel": 1}),
    ("Carriage House Door",         105,  78,  52,  2, {"plank": 5, "iron_ingot": 1}),
    ("Stable Wall Panel",           182,  82,  60,  3, {"clay_brick": 4}),
    ("Conservatory Glass Panel",    200, 215, 225,  1, {"sand": 3, "iron_ingot": 1}),
    ("Conservatory Iron Frame",     180, 185, 188,  2, {"iron_ingot": 3}),
    ("Victorian Greenhouse Frame",  155, 168, 172,  2, {"iron_ingot": 4}),

    # ── Craftsman Specific ────────────────────────────────────────────────────
    ("Clinker Brick",                72,  55,  48,  3, {"clay_brick": 4, "coal": 1}),
    ("River Rock Block",            138, 130, 118,  3, {"stone_chunk": 3}),
    ("River Rock Column",           130, 122, 110,  3, {"stone_chunk": 4}),
    ("Cobblestone Pier",            118, 112, 105,  3, {"stone_chunk": 3}),
    ("Craftsman Beam End",          140, 108,  68,  2, {"plank": 3}),
    ("Craftsman Frieze Board",       78,  58,  40,  2, {"plank": 4, "tar": 1}),
    ("Craftsman Bargeboard",         82,  62,  42,  2, {"plank": 3}),
    ("Craftsman Trim Strip",         85,  65,  44,  2, {"plank": 2}),
    ("Arts and Crafts Tile",        158, 128,  85,  3, {"clay_brick": 3, "chisel": 1}),
    ("Prairie Grid Glass",          185, 200, 215,  1, {"sand": 2, "iron_ingot": 1}),
    ("Strap Hinge Panel",            65,  58,  52,  2, {"iron_ingot": 2, "plank": 1}),
    ("Craftsman Column Cap",        185, 180, 172,  3, {"stone_chunk": 2, "chisel": 1}),
    ("Tapered Porch Post",           95,  72,  48,  2, {"plank": 3}),
    ("Shed Dormer Block",           175, 172, 168,  3, {"plank": 3, "stone_chip": 1}),

    # ── Chimney & Utility ─────────────────────────────────────────────────────
    ("Chimney Stack Block",         175,  75,  55,  3, {"clay_brick": 5}),
    ("Chimney Pot",                 182,  82,  60,  3, {"clay_brick": 3, "chisel": 1}),
    ("Chimney Cap",                 188, 185, 178,  4, {"stone_chunk": 2}),
    ("Flaunching Block",            148, 142, 135,  3, {"stone_chunk": 2, "sand": 1}),
    ("Cast Iron Gutter",             52,  50,  48,  2, {"iron_ingot": 2}),
    ("Cast Iron Downpipe",           55,  52,  50,  2, {"iron_ingot": 2}),
    ("Hopper Head Block",            58,  55,  52,  2, {"iron_ingot": 2, "chisel": 1}),
    ("Air Brick",                   178,  78,  58,  3, {"clay_brick": 2}),
    ("Damp Course Block",           145, 140, 132,  3, {"stone_chunk": 2, "tar": 1}),
    ("Basement Window Well",         62,  60,  58,  2, {"iron_ingot": 3}),

    # ── Garden Structures ─────────────────────────────────────────────────────
    ("Ice House Block",             148, 152, 158,  4, {"stone_chunk": 4}),
    ("Garden Tool Store Panel",     148, 118,  78,  2, {"plank": 4}),
    ("Bell Tower Block",            182,  80,  58,  4, {"clay_brick": 5, "stone_chunk": 1}),
    ("Summerhouse Panel",           188, 182, 172,  2, {"plank": 4, "stone_chunk": 1}),
    ("Gazebo Beam",                 100,  78,  52,  2, {"plank": 4}),
    ("Garden Pavilion Post",        105,  82,  55,  2, {"plank": 3, "chisel": 1}),
    ("Dovecote Block",              205, 200, 192,  3, {"stone_chunk": 3, "lime_plaster": 1}),
    ("Ha Ha Wall Block",            148, 142, 135,  4, {"stone_chunk": 4}),
    ("Topiary Frame",               105, 138,  78,  2, {"iron_ingot": 2}),
    ("Rose Arch Frame",              72,  58,  45,  2, {"iron_ingot": 2, "plank": 1}),
    ("Coal Cellar Block",           118, 112, 108,  4, {"stone_chunk": 4, "coal": 1}),
]

assert len(BLOCKS_TO_ADD) == 250, f"Expected 250 blocks, got {len(BLOCKS_TO_ADD)}"

# ── Name helpers ──────────────────────────────────────────────────────────────
def to_const(name):
    return re.sub(r"\W+", "_", name.strip()).upper().strip("_")

def to_id(name):
    return re.sub(r"\W+", "_", name.strip()).lower().strip("_")

def fmt_color(r, g, b):
    return f"({r:3d}, {g:3d}, {b:3d})"

# ── Brace / bracket helpers ───────────────────────────────────────────────────
def _find_matching(text, open_pos, open_ch, close_ch):
    depth = 0
    for i in range(open_pos, len(text)):
        if text[i] == open_ch:
            depth += 1
        elif text[i] == close_ch:
            depth -= 1
            if depth == 0:
                return i
    raise ValueError(f"No matching {close_ch!r} found")

def _dict_close(text, dict_name):
    m = re.search(rf"^{re.escape(dict_name)} *= *\{{", text, re.MULTILINE)
    if not m:
        raise ValueError(f"Cannot find '{dict_name} = {{' in file")
    return _find_matching(text, m.end() - 1, "{", "}")

def _list_close(text, list_name):
    m = re.search(rf"^{re.escape(list_name)} *= *\[", text, re.MULTILINE)
    if not m:
        raise ValueError(f"Cannot find '{list_name} = [' in file")
    return _find_matching(text, m.end() - 1, "[", "]")

def _set_close(text, set_name):
    m = re.search(rf"^{re.escape(set_name)}\b[^{{]*\{{", text, re.MULTILINE | re.DOTALL)
    if not m:
        raise ValueError(f"Cannot find set {set_name!r}")
    return _find_matching(text, m.end() - 1, "{", "}")

def _import_close(text):
    m = re.search(r"^from blocks import \(", text, re.MULTILINE)
    if not m:
        return -1
    return _find_matching(text, m.end() - 1, "(", ")")

def next_block_id(text):
    ids = [int(v) for v in re.findall(r"^[A-Z][A-Z_0-9]* *= *(\d+)", text, re.MULTILINE)]
    return max(ids) + 1

# ── Apply all mutations ───────────────────────────────────────────────────────
def apply(dry_run=False):
    blocks_text   = BLOCKS_PY.read_text(encoding="utf-8")
    items_text    = ITEMS_PY.read_text(encoding="utf-8")
    crafting_text = CRAFTING_PY.read_text(encoding="utf-8")

    bid = next_block_id(blocks_text)
    print(f"Starting from block ID {bid}")

    all_consts = []

    for name, r, g, b, hardness, recipe in BLOCKS_TO_ADD:
        const   = to_const(name)
        item_id = to_id(name)
        color   = fmt_color(r, g, b)
        drop_s  = f'"{item_id}"'

        # ── blocks.py: ID constant ─────────────────────────────────────────
        insert_pos = blocks_text.find("\nBLOCKS = {")
        if insert_pos == -1:
            raise ValueError("Cannot find 'BLOCKS = {' in blocks.py")
        line = f"\n{const:<36} = {bid}  # {name.lower()}"
        blocks_text = blocks_text[:insert_pos] + line + blocks_text[insert_pos:]

        # ── blocks.py: BLOCKS dict entry ───────────────────────────────────
        pad    = max(1, 26 - len(const))
        entry  = f'    {const}:{" " * pad}{{"name": "{name}", "hardness": {hardness}, "color": {color}, "drop": {drop_s}}},\n'
        close  = _dict_close(blocks_text, "BLOCKS")
        blocks_text = blocks_text[:close] + entry + blocks_text[close:]

        # ── items.py: item entry ───────────────────────────────────────────
        IMPORT_IND = " " * 20
        pad_i  = max(1, 26 - len(item_id) - 2)
        ientry = f'    "{item_id}":{" " * pad_i}{{"name": "{name}", "color": {color}, "place_block": {const}}},\n'
        iclose = _dict_close(items_text, "ITEMS")
        items_text = items_text[:iclose] + ientry + items_text[iclose:]

        # ── items.py: extend blocks import ────────────────────────────────
        imp_close = _import_close(items_text)
        if imp_close != -1:
            items_text = items_text[:imp_close] + f",\n{IMPORT_IND}{const}" + items_text[imp_close:]

        # ── crafting.py: ARTISAN_RECIPES placeholder ──────────────────────
        ing_str = ", ".join(f'"{k}": {v}' for k, v in recipe.items())
        rentry  = f'    {{"name": "{name}", "ingredients": {{{ing_str}}}, "output_id": "{item_id}", "output_count": 2}},\n'
        rclose  = _list_close(crafting_text, "ARTISAN_RECIPES")
        crafting_text = crafting_text[:rclose] + rentry + crafting_text[rclose:]

        all_consts.append(const)
        print(f"  [{bid:4d}] {const}")
        bid += 1

    if dry_run:
        print(f"\nDry run — {len(BLOCKS_TO_ADD)} blocks planned, nothing written.")
        return

    BLOCKS_PY.write_text(blocks_text, encoding="utf-8")
    ITEMS_PY.write_text(items_text, encoding="utf-8")
    CRAFTING_PY.write_text(crafting_text, encoding="utf-8")

    print(f"\nWritten: blocks.py, items.py, crafting.py")
    print(f"Added {len(BLOCKS_TO_ADD)} blocks (IDs {bid - len(BLOCKS_TO_ADD)}–{bid - 1})")
    print("\nStill needs manual work:")
    print("  Render/blocks_victorian.py — create custom art module")
    print("  Render/blockRenderHandler.py — register new module")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    apply(dry_run=args.dry_run)
