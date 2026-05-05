#!/usr/bin/env python3
"""Extract unique bird species from the eBird/Clements World Bird List.

Scans BirdList.csv for rows where Column 5 (category) == 'species',
then saves the distinct English names (Column 6) to NewBirdList.csv.
"""

import csv
import os

BASE = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(BASE, "BirdList.csv")
OUTPUT = os.path.join(BASE, "NewBirdList.csv")

def main():
    seen = set()
    species = []

    # BirdList.csv uses both commas and the first row is a credit line — skip non-species rows
    with open(INPUT, encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 6:
                continue
            category = row[4].strip().lower()  # Column 5
            english_name = row[5].strip()        # Column 6
            if category == "species" and english_name:
                # Also skip rows that are just category names (no English name for families, etc.)
                if english_name not in seen:
                    seen.add(english_name)
                    species.append(english_name)

    # Write output
    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["English Name", "Scientific Name", "Family"])
        for name in species:
            writer.writerow([name, "", ""])

    print(f"Extracted {len(species)} unique species -> {OUTPUT}")


if __name__ == "__main__":
    main()
