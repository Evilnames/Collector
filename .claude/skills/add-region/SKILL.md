---
name: add-region
description: Step-by-step guide for adding a new region type (biome group) to CollectorBlocks. Covers all name/tagline/heraldry pools in towns.py and the biome-to-group mapping.
---

# Add a New Region Type (Biome Group)

Regions are procedurally generated from data tables in [towns.py](../../../towns.py). A "region type" is a **biome group** — a named grouping of related biomes that share name pools, taglines, leader titles, and heraldry. All data lives in named dicts; no new classes or logic are needed.

---

## Step 1 — Map biomes to the new group

Find `_BIOME_GROUP` in [towns.py](../../../towns.py) and add every biome that belongs to this group:

```python
_BIOME_GROUP = {
    ...
    "volcanic":  "volcanic",   # new entries
    "lava_fields": "volcanic",
}
```

Biome keys must match the string IDs used in [biomes.py](../../../biomes.py).

---

## Step 2 — Add region names

Find `_REGION_NAMES_BY_GROUP` and add a list of thematic region names:

```python
_REGION_NAMES_BY_GROUP = {
    ...
    "volcanic": ["The Cinderpeak Dominion", "The Ashfall Reaches", "The Emberveil Territories"],
}
```

---

## Step 3 — Add town name parts

Find `_TOWN_NAMES_BY_GROUP` and add prefix/suffix pools for procedural town names:

```python
_TOWN_NAMES_BY_GROUP = {
    ...
    "volcanic": {
        "prefixes": ["Cinder", "Ember", "Ash", "Scorch", "Magma"],
        "suffixes": ["wick", "ford", "hold", "peak", "haven"],
    },
}
```

---

## Step 4 — Add taglines

Find `_TAGLINES_BY_GROUP` and add flavour lines displayed on the region map panel:

```python
_TAGLINES_BY_GROUP = {
    ...
    "volcanic": [
        "Forged in fire, tempered by ash.",
        "Where the earth still breathes.",
        "Heat shapes all things here.",
    ],
}
```

---

## Step 5 — Add heraldic charges

Find `_CHARGES_BY_GROUP` and add thematic symbols for the coat of arms generator:

```python
_CHARGES_BY_GROUP = {
    ...
    "volcanic": ["flame", "mountain", "anvil", "serpent", "sun"],
}
```

---

## Step 6 — Add leader titles

Find `_LEADER_TITLES` and add gendered title pairs for the region's ruler:

```python
_LEADER_TITLES = {
    ...
    "volcanic": ("Cinder Lord", "Cinder Lady"),
}
```

---

## Step 7 — Add leader greetings

Find `_LEADER_GREETINGS` and add opening dialogue lines for the palace LeaderNPC:

```python
_LEADER_GREETINGS = {
    ...
    "volcanic": [
        "The mountain speaks to those willing to listen.",
        "Ash falls on conqueror and conquered alike.",
    ],
}
```

---

## Step 8 — Add luxury specialties

Find `_LUXURY_SPECIALTY` and add what trade goods this region's towns tend to export:

```python
_LUXURY_SPECIALTY = {
    ...
    "volcanic": ["obsidian_slab", "coal", "iron_chunk"],
}
```

---

## Step 9 — Add need weights

Find `_NEED_WEIGHTS` and add the supply/demand weighting for this group. Copy an existing group as a baseline and adjust:

```python
_NEED_WEIGHTS = {
    ...
    "volcanic": {"food": 1.4, "tools": 0.8, "luxury": 0.6, "medicine": 1.0},
}
```

---

## Verification checklist

- [ ] All new biome keys in `_BIOME_GROUP` exist in [biomes.py](../../../biomes.py)
- [ ] Every dict (`_REGION_NAMES`, `_TOWN_NAMES`, `_TAGLINES`, `_CHARGES`, `_LEADER_TITLES`, `_LEADER_GREETINGS`, `_LUXURY_SPECIALTY`, `_NEED_WEIGHTS`) has an entry for the new group key
- [ ] Generate a new world — towns in the new biomes should have region-appropriate names and a coat of arms
- [ ] Palace leader NPC greets the player with one of the new lines
