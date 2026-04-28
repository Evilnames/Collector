---
name: add-seashell
description: Step-by-step guide for adding a new seashell species to CollectorBlocks. Covers SHELL_TYPES entry, SHELL_TYPE_ORDER, and SHELL_TYPE_DESCRIPTIONS registration.
---

# Add a New Seashell Species

Seashells are dictionary-based collectibles defined in [seashells.py](../../../seashells.py). Each species is an entry in `SHELL_TYPES`. Individual collected shells are generated as `Seashell` dataclass instances by `SeashellGenerator` when the player mines a `SEASHELL_BLOCK`.

There are two depth zones: **tidal** (y 45–60, free access) and **reef** (y 60–95, requires diving helmet). Species only generate in their assigned zone.

---

## Step 1 — Add an entry to SHELL_TYPES

Add a new key to `SHELL_TYPES` in [seashells.py](../../../seashells.py). Group it near species of the same `depth_zone` and similar rarity for readability.

```python
"sundial": {
    "depth_zone":  "tidal",
    "rarity_pool": ["uncommon", "rare", "rare"],
    "color_pool":  [(210, 195, 155), (195, 178, 135), (225, 210, 170)],
    "patterns":    ["spiral", "ribbed", "spiral"],
    "size_range":  (2.0, 6.0),
    "shape":       "spiral",
},
```

**depth_zone**: `"tidal"` or `"reef"`. Controls which zone SEASHELL_BLOCKs can yield this species.

**rarity_pool**: repeated entries increase probability — e.g. `["uncommon", "rare", "rare"]` = 1/3 uncommon, 2/3 rare.

**color_pool**: list of RGB tuples; one is picked at generation time.

**patterns**: list drawn randomly; repeat a pattern to weight it higher. Each pattern affects how `render_seashell` draws the surface detail.

**size_range**: `(min_cm, max_cm)` — cosmetic only, shown in the detail panel.

**shape**: controls the silhouette drawn by `render_seashell`. Pick the closest match from the shapes table below.

---

## Step 2 — Add to SHELL_TYPE_ORDER

Find `SHELL_TYPE_ORDER` in [seashells.py](../../../seashells.py) and insert the key. Keep tidal species first, reef species after, and sort roughly by rarity (common → epic) within each zone:

```python
SHELL_TYPE_ORDER = [
    # Tidal
    "cowrie", "clam", "periwinkle", "scallop", "limpet", "cone", "sundial", "whelk",
    # Reef
    "oyster", "turritella", "abalone", "murex", "volute", "triton", "nautilus", "marginella",
]
```

This list drives the Seashell Codex grid order — tidal entries appear first, reef below.

---

## Step 3 — Add a description to SHELL_TYPE_DESCRIPTIONS

Add a one-sentence natural-history blurb to `SHELL_TYPE_DESCRIPTIONS` in [seashells.py](../../../seashells.py). Shown in both the detail panel and the Codex:

```python
SHELL_TYPE_DESCRIPTIONS = {
    ...
    "sundial": "A flat spiral shell with radiating ribs, named for its resemblance to a sun dial face.",
    ...
}
```

---

## Reference

### depth_zone

| Zone | Block y range | Access |
|------|--------------|--------|
| `"tidal"` | 45–60 | Free |
| `"reef"` | 60–95 | Diving Helmet required |

### shape → render behaviour

| Shape | Visual | Good for |
|-------|--------|---------|
| `"oval"` | Rounded ellipse with optional spots/bands/iridescent overlay | Cowries, clams, abalones, volutes |
| `"cone"` | Triangle silhouette with horizontal band lines | Cone snails, limpets, turritella |
| `"spiral"` | Outward Archimedean spiral stroke | Periwinkles, whelks, murex, triton |
| `"fan"` | Radiating ribs from a central hinge point | Scallops, fan shells |
| `"coiled"` | Concentric filled circles with a banded overlay | Nautilus, ammonite-like forms |

### patterns

| Pattern | Effect |
|---------|--------|
| `"spotted"` | Scattered dark circles on oval shapes |
| `"banded"` | Vertical color bands on oval; cross-line on coiled |
| `"solid"` | Base color only, no overlay |
| `"ribbed"` | Horizontal lines on cone; radial lines on fan |
| `"spiral"` | Spiral line strokes (enhances spiral shape) |
| `"layered"` | Growth-ring lines across oval shapes |
| `"iridescent"` | Semi-transparent cyan shimmer patch on oval |
| `"spined"` | Branching spine lines (spiral shape only) |
| `"coiled"` | Tight concentric rings (coiled shape only) |

### rarity_pool weights

| Rarity | Typical use |
|--------|-------------|
| `"common"` | Abundant tidal species |
| `"uncommon"` | Slightly rarer tidal or basic reef |
| `"rare"` | Deeper reef, harder to find |
| `"epic"` | Reef showpieces (nautilus, marginella) |
| `"legendary"` | Reserved for future deep-zone expansion |

---

## Verification checklist

- [ ] Dict key is unique in `SHELL_TYPES`
- [ ] `depth_zone` is `"tidal"` or `"reef"`
- [ ] Key is inserted in `SHELL_TYPE_ORDER` in the correct zone group
- [ ] Description added to `SHELL_TYPE_DESCRIPTIONS`
- [ ] In-game: swim to the correct zone depth, mine a `SEASHELL_BLOCK` — species should appear in the Collection and Seashell Codex