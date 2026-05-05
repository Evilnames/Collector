"""
Export all bird species from birds.py to a CSV file.
Reads class attributes directly from the module — no hardcoded lists.
"""
import csv
import inspect
import os
import sys

# 1. Resolve paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# 2. Ensure Collector/ is on sys.path so relative imports work
COLLECTOR_DIR = os.path.dirname(SCRIPT_DIR)
if COLLECTOR_DIR not in sys.path:
    sys.path.insert(0, COLLECTOR_DIR)

# 3. Import the birds module
import birds

# 4. Gather species — ALL_SPECIES is a list of class objects
species_list = birds.ALL_SPECIES

# 5. For each species, extract the class-level attributes we care about
rows = []
for cls in species_list:
    row = {
        "Class": cls.__name__,
        "Species": cls.SPECIES,
        "Rarity": cls.RARITY,
        "Biomes": "; ".join(cls.BIOMES) if cls.BIOMES else "Any",
        "Is Flock": cls.IS_FLOCK,
        "Flock Size": f"{cls.FLOCK_SIZE_RANGE[0]}-{cls.FLOCK_SIZE_RANGE[1]}" if cls.IS_FLOCK else "N/A",
        "Altitude (blocks)": f"{cls.ALTITUDE_BLOCKS[0]}-{cls.ALTITUDE_BLOCKS[1]}",
        "Speed (px/s)": cls.SPEED,
        "Width": cls.W,
        "Height": cls.H,
        "Body Color (RGB)": f"({cls.BODY_COLOR[0]}, {cls.BODY_COLOR[1]}, {cls.BODY_COLOR[2]})",
        "Wing Color (RGB)": f"({cls.WING_COLOR[0]}, {cls.WING_COLOR[1]}, {cls.WING_COLOR[2]})",
        "Beak Color (RGB)": f"({cls.BEAK_COLOR[0]}, {cls.BEAK_COLOR[1]}, {cls.BEAK_COLOR[2]})",
        "Head Color (RGB)": f"({cls.HEAD_COLOR[0]}, {cls.HEAD_COLOR[1]}, {cls.HEAD_COLOR[2]})",
        "Accent Color (RGB)": f"({cls.ACCENT_COLOR[0]}, {cls.ACCENT_COLOR[1]}, {cls.ACCENT_COLOR[2]})",
        "Personality": cls.PERSONALITY,
        "Nocturnal": cls.NOCTURNAL,
        "Is Ground Bird": getattr(cls, "IS_GROUND", False),
    }
    rows.append(row)

# 6. Write CSV
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "birds_export.csv")
if rows:
    fieldnames = list(rows[0].keys())
    with open(OUTPUT_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Exported {len(rows)} species to {OUTPUT_PATH}")
else:
    print("No species found in birds.ALL_SPECIES")
