---
name: add-npc
description: Step-by-step guide for adding a new NPC type to CollectorBlocks. Covers class definition, shop/quest setup, CITY_CONFIGS registration, and _build_single_city dispatch.
---

# Add a New NPC Type

NPCs are classes defined in [cities.py](../../../cities.py). Interactive (stationary) NPCs inherit from `NPC`; roaming NPCs inherit from `AmbientNPC`. After defining the class you register a string key in `CITY_CONFIGS` and add a dispatch case in `_build_single_city`.

---

## Step 1 — Choose a base class

| Base class | Use when |
|------------|----------|
| `NPC` | Stationary — has a shop, quest, or dialogue |
| `AmbientNPC` | Walks a patrol range, no interaction |

---

## Step 2 — Define the class

Add the new class in [cities.py](../../../cities.py) near the other NPC classes, before `CITY_CONFIGS`. Use an existing class of the same type as a reference.

### Shopkeeper example

```python
class TailorNPC(NPC):
    def __init__(self, world, bx, by, biodome, rng, difficulty=1):
        super().__init__(world, bx, by)
        self.animal_id  = "tailor"         # unique string, used in save/load
        self.name       = "Tailor"
        self.biodome    = biodome
        self.clothing   = _npc_clothing(biodome)
        self.difficulty = difficulty

        # Build shop inventory from a table defined below
        self.shop = _build_tailor_shop(rng, difficulty)

    def interact(self, player):
        # Return a shop UI descriptor — same pattern as MerchantNPC
        return {"type": "shop", "title": self.name, "items": self.shop}
```

### Quest-giver example

```python
class MapmakerNPC(NPC):
    def __init__(self, world, bx, by, biodome, rng, difficulty=1):
        super().__init__(world, bx, by)
        self.animal_id = "mapmaker"
        self.name      = "Mapmaker"
        self.biodome   = biodome
        self.clothing  = _npc_clothing(biodome)
        self.quest     = _build_mapmaker_quest(rng, difficulty)
        self.quest2    = _build_prestige_mapmaker_quest(rng, difficulty)

    def interact(self, player):
        return {"type": "quest", "quests": [self.quest, self.quest2]}
```

### Ambient NPC example

```python
class MerchantCaravanNPC(AmbientNPC):
    def __init__(self, world, bx, by, biodome, rng):
        super().__init__(world, bx, by, patrol_half=80)
        self.animal_id = "merchant_caravan"
        self.clothing  = _npc_clothing(biodome)
        self.speed     = 28
```

---

## Step 3 — Add shop/quest builder functions (if needed)

Define helper functions near the class. Follow the naming pattern `_build_<npc>_shop` or `_build_<npc>_quest`:

```python
TAILOR_SHOP_TABLE = [
    ("linen_shirt", 1, 12),   # (item_id, qty, price)
    ("wool_coat",   1, 28),
    ("leather_hat", 1, 18),
    ("silk_scarf",  1, 45),
]

def _build_tailor_shop(rng, difficulty):
    count  = 3 + min(difficulty, 2)
    items  = rng.sample(TAILOR_SHOP_TABLE, k=count)
    return [{"item": i, "qty": q, "price": p} for i, q, p in items]
```

---

## Step 4 — Register the NPC string in `CITY_CONFIGS`

Find the `"npc_types"` list for the city size(s) where this NPC should appear and add the new string:

```python
CITY_CONFIGS["large"]["npc_types"] = [
    "quest_rock", "blacksmith", "innkeeper", "merchant",
    "tailor",          # ← add here at the matching building slot index
    "shrine_keeper", "restaurant", "scholar", "trade",
]
```

The string must be added **at the same index** as the building in `"buildings"` that this NPC occupies. `len(npc_types)` must equal `len(buildings)` after the change.

---

## Step 5 — Add a dispatch case in `_build_single_city`

Find the block in `_build_single_city` in [cities.py](../../../cities.py) that maps `npc_type` strings to constructors (search for `"quest_rock"` or `"merchant"` to locate it). Add a new branch:

```python
elif npc_type == "tailor":
    npc = TailorNPC(world, bx, by, biodome, rng, difficulty)
    world.add_npc(npc)
```

For ambient NPCs, the dispatch is in the ambient NPC loop (search for `"villager"` or `"guard"`):

```python
elif amb_type == "merchant_caravan":
    npc = MerchantCaravanNPC(world, bx, by, biodome, rng)
    world.add_npc(npc)
```

---

## Reference

### `_npc_clothing(biodome)` palette keys

Clothing palettes are selected automatically based on biome. Pass the `biodome` string received in `__init__` and the function returns a `{"body", "leg", "skin", "trim", "hat"}` colour dict.

### Inherited NPC attributes worth setting

| Attribute | Default | Notes |
|-----------|---------|-------|
| `self.animal_id` | — | **Required.** Unique string; used in save/load. |
| `self.name` | `"NPC"` | Displayed in UI |
| `self.clothing` | `{}` | Use `_npc_clothing(biodome)` |
| `self.patrol_half` | `40` | `AmbientNPC` only — pixel radius |
| `self.speed` | `30` | Pixels/second |
| `self.is_ambient` | `True` for `AmbientNPC` | Affects night-time behaviour |

### Quest difficulty levels

| `difficulty` | Where used |
|-------------|-----------|
| `0` | Starter/tutorial quests |
| `1` | Normal town quests |
| `2` | Hard quests, royal court |
| `3` | Prestige/capital quests |

---

## Verification checklist

- [ ] `self.animal_id` is unique across all NPC classes
- [ ] `len(npc_types) == len(buildings)` in every `CITY_CONFIGS` entry you modified
- [ ] Dispatch case added in `_build_single_city` for the new string
- [ ] Shop table/quest builder defined if the NPC uses one
- [ ] Generate a city of the matching size — new NPC should appear in the expected building slot
- [ ] Interact with the NPC — shop/quest UI opens without errors
