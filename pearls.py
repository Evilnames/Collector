import hashlib
import random
import pygame
from dataclasses import dataclass


@dataclass
class Pearl:
    uid: str
    color_name: str
    color: tuple
    luster: str         # "matte" | "satin" | "lustrous" | "iridescent"
    shape: str          # "round" | "oval" | "baroque" | "drop"
    size_mm: float
    rarity: str
    biome_found: str
    seed: int


PEARL_TYPES = {
    "white":    {"color": (240, 235, 220), "rarity_pool": ["common", "common", "uncommon"]},
    "cream":    {"color": (235, 220, 190), "rarity_pool": ["common", "uncommon"]},
    "pink":     {"color": (240, 200, 210), "rarity_pool": ["uncommon", "uncommon", "rare"]},
    "golden":   {"color": (235, 210, 130), "rarity_pool": ["uncommon", "rare"]},
    "black":    {"color": ( 50,  55,  70), "rarity_pool": ["rare", "rare", "epic"]},
    "blue":     {"color": (110, 145, 195), "rarity_pool": ["rare", "epic"]},
    "rainbow":  {"color": (200, 200, 235), "rarity_pool": ["epic", "legendary"]},
}

_LUSTER_POOL = ["matte", "satin", "lustrous", "lustrous", "iridescent"]
_SHAPE_POOL  = ["round", "round", "oval", "baroque", "drop"]


# Spawn weights per pearl color — higher = more common drop.
_PEARL_WEIGHTS = {
    "white":   12,
    "cream":   10,
    "pink":    6,
    "golden":  4,
    "black":   2,
    "blue":    2,
    "rainbow": 1,
}


class PearlGenerator:
    def __init__(self, world_seed: int):
        self._world_seed = world_seed

    def generate(self, bx: int, by: int, biome: str) -> "Pearl":
        seed = hash((self._world_seed, bx, by, "pearl")) & 0xFFFFFFFF
        rng = random.Random(seed)

        eligible = []
        for color_name, weight in _PEARL_WEIGHTS.items():
            eligible.extend([color_name] * weight)
        color_name = rng.choice(eligible)
        pdata = PEARL_TYPES[color_name]

        rarity = rng.choice(pdata["rarity_pool"])
        luster = rng.choice(_LUSTER_POOL)
        shape  = rng.choice(_SHAPE_POOL)
        size_mm = round(rng.uniform(4.0, 14.0), 1)

        uid = hashlib.md5(f"pearl_{seed}_{bx}_{by}".encode()).hexdigest()[:12]

        return Pearl(
            uid=uid,
            color_name=color_name,
            color=pdata["color"],
            luster=luster,
            shape=shape,
            size_mm=size_mm,
            rarity=rarity,
            biome_found=biome or "ocean",
            seed=seed,
        )


_pearl_surf_cache = {}


def render_pearl(pearl: "Pearl", cell_size: int = 58) -> pygame.Surface:
    cache_key = (pearl.uid, cell_size)
    if cache_key in _pearl_surf_cache:
        return _pearl_surf_cache[cache_key]
    surf = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)

    # Size scales with pearl size_mm relative to 4-14mm range.
    size_norm = (pearl.size_mm - 4.0) / 10.0
    radius = int(cell_size * 0.22 + size_norm * cell_size * 0.18)
    cx = cell_size // 2
    cy = cell_size // 2
    base = pearl.color

    if pearl.shape == "round":
        rect = (cx - radius, cy - radius, radius * 2, radius * 2)
    elif pearl.shape == "oval":
        rect = (cx - radius, cy - int(radius * 0.75), radius * 2, int(radius * 1.5))
    elif pearl.shape == "drop":
        rect = (cx - int(radius * 0.85), cy - radius, int(radius * 1.7), int(radius * 2.1))
    else:  # baroque
        rect = (cx - radius, cy - int(radius * 0.9), int(radius * 2.1), int(radius * 1.7))

    pygame.draw.ellipse(surf, base, rect)

    # Highlight
    hl_color = tuple(min(255, c + 60) for c in base)
    hl_rect = (rect[0] + rect[2] // 4, rect[1] + rect[3] // 5,
               max(2, rect[2] // 3), max(2, rect[3] // 4))
    pygame.draw.ellipse(surf, hl_color, hl_rect)

    if pearl.luster == "iridescent":
        # Faint rainbow ring
        ring_color = (200, 180, 230)
        pygame.draw.ellipse(surf, ring_color, rect, 1)

    _pearl_surf_cache[cache_key] = surf
    return surf
