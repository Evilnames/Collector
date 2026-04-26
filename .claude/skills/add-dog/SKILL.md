---
name: add-dog
description: Step-by-step guide for adding a new dog breed to CollectorBlocks. Covers BREED_PROFILES entry, DOG_BIOME_MAP registration (auto-derived), and optional Render/dogs.py tweaks.
---

# Add a New Dog Breed

Dog breeds are data-driven entries in [dogs.py](../../../dogs.py). There is no class to subclass — everything is driven by the `BREED_PROFILES` dict. `DOG_BIOME_MAP` is **automatically derived** from each breed's `"biomes"` set at module load time.

---

## Step 1 — Add an entry to `BREED_PROFILES`

Open [dogs.py](../../../dogs.py) and add a new key to the `BREED_PROFILES` dict. Use an existing breed (e.g., `"Labrador"` or `"Border Collie"`) as a template.

```python
"Akita": {
    # ── Biomes where wild Akitas spawn ──────────────────────────────
    "biomes": {"boreal", "alpine_mountain", "rocky_mountain"},

    # ── Physical size class ─────────────────────────────────────────
    # Options: "toy" | "small" | "medium" | "large" | "giant"
    "size_class": "large",

    # ── Float gene ranges (lo, hi) — each allele drawn from uniform(lo, hi) ──
    # Performance genes:  speed / endurance / agility / strength     range 0.7–1.3
    # Sensory genes:      nose / alertness                            range 0.7–1.3
    # Temperament genes:  loyalty / playfulness / stubbornness / prey_drive   range 0.0–1.0
    "genes": {
        "speed_gene":        (0.9, 1.2),
        "endurance_gene":    (1.0, 1.2),
        "agility_gene":      (0.9, 1.1),
        "strength_gene":     (1.1, 1.3),   # high strength
        "nose_gene":         (0.8, 1.1),
        "alertness_gene":    (1.0, 1.3),   # high alertness → natural guard
        "loyalty_gene":      (0.8, 1.0),
        "playfulness_gene":  (0.4, 0.7),
        "stubbornness_gene": (0.5, 0.8),   # moderately stubborn
        "prey_drive_gene":   (0.7, 1.0),
    },

    # ── Ability carrier probabilities (0.0–1.0 per allele) ──────────
    # Abilities: "tracking" | "herding" | "guard" | "retrieve"
    # An ability only *expresses* when both alleles match (recessive).
    # Carrier probability here is per-allele in wild dogs.
    "abilities": {"guard": 0.55},

    # ── Coat colour palette (list of RGB tuples) ────────────────────
    # One is chosen at random for each spawned dog.
    "coat_colors": [(220, 200, 160), (80, 65, 45), (240, 230, 210)],

    # ── Coat pattern weights parallel to DOG_COAT_PATTERN_ORDER ──────
    # Order: [solid, spotted, merle, brindle, saddle, ticked]
    "coat_pattern_weights": [60, 0, 0, 0, 40, 0],

    # ── Physical defaults ────────────────────────────────────────────
    "ear_type":   "erect",    # "erect" | "semi-erect" | "floppy"
    "tail_type":  "curled",   # "long" | "curled" | "short" | "bob"
    "coat_length":"short",    # "short" | "medium" | "long"

    # ── Coat type weights parallel to DOG_COAT_TYPE_ORDER ─────────────
    # Order: [smooth, wavy, curly, wire]
    "coat_type_weights": [80, 20, 0, 0],
},
```

That's all that's required. `DOG_BIOME_MAP` is rebuilt automatically when the module loads.

---

## Step 2 — Update `_boost_pure_breed` (optional)

If you want the `pure_breeding` research bonus to boost this breed's signature trait, add a line to the `char_trait` dict in [dogs.py](../../../dogs.py):

```python
def _boost_pure_breed(offspring, breed):
    char_trait = {
        ...
        "Akita": "strength",   # +0.05 to strength for pure Akita offspring
        ...
    }.get(breed)
```

---

## Step 3 — Renderer (optional, no action needed for basic breeds)

[Render/dogs.py](../../../Render/dogs.py) draws all dogs generically using their trait dict. No per-breed draw function is needed. However if you want a distinctive silhouette or marking you can add an `if breed == "Akita":` branch inside `draw_dog()` after the standard anatomy is drawn.

---

## Verification checklist

- [ ] Start a new world (or explore a new biome) — Akitas should spawn in `boreal`, `alpine_mountain`, `rocky_mountain`
- [ ] Wild Akita flees until tamed — feed bone/meat until collar consumed
- [ ] Tamed Akita follows player; G-key toggles STAY
- [ ] Right-click tamed Akita with empty hand → view panel shows breed "Akita"
- [ ] Breed two Akitas at kennel → offspring breed = "Akita" (pure)
- [ ] Breed Akita + Husky → offspring breed = "Mixed (Akita/Husky)"
- [ ] Dog codex (Encyclopedia → DOGS) shows Akita entry after taming one
