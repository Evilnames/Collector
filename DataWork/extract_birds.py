#!/usr/bin/env python3
"""Extract all bird species from birds.py into a CSV file."""

import csv
import os
import sys

# Path setup
COLLECTOR_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, COLLECTOR_DIR)

# Import birds module
import birds

# Collect all species from ALL_SPECIES list
rows = []
for cls in birds.ALL_SPECIES:
    row = {
        "Class": cls.__name__,
        "Species": cls.SPECIES,
        "Rarity": cls.RARITY,
        "Biomes": "; ".join(cls.BIOMES) if cls.BIOMES else "Any",
        "Is Flock": cls.IS_FLOCK,
        "Flock Size": f"{cls.FLOCK_SIZE_RANGE[0]}-{cls.FLOCK_SIZE_RANGE[1]}" if cls.IS_FLOCK else "N/A",
        "Altitude": f"{cls.ALTITUDE_BLOCKS[0]}-{cls.ALTITUDE_BLOCKS[1]} blocks",
        "Speed (px/s)": cls.SPEED,
        "Size": f"{cls.W}x{cls.H}",
        "Body Color": f"RGB({cls.BODY_COLOR[0]},{cls.BODY_COLOR[1]},{cls.BODY_COLOR[2]})",
        "Wing Color": f"RGB({cls.WING_COLOR[0]},{cls.WING_COLOR[1]},{cls.WING_COLOR[2]})",
        "Beak Color": f"RGB({cls.BEAK_COLOR[0]},{cls.BEAK_COLOR[1]},{cls.BEAK_COLOR[2]})",
        "Head Color": f"RGB({cls.HEAD_COLOR[0]},{cls.HEAD_COLOR[1]},{cls.HEAD_COLOR[2]})",
        "Accent Color": f"RGB({cls.ACCENT_COLOR[0]},{cls.ACCENT_COLOR[1]},{cls.ACCENT_COLOR[2]})",
        "Personality": cls.PERSONALITY,
        "Nocturnal": cls.NOCTURNAL,
    }
    rows.append(row)

# Write CSV
output_path = os.path.join(COLLECTOR_DIR, "birds_list.csv")
with open(output_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Exported {len(rows)} bird species to {output_path}")
