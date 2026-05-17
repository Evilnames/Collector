"""Manuscript / book-binding system.

Pipeline:  flax_fiber + oak_gall + soot/dye  →  parchment + ink  →  scribed page
                                                                  (illumination grid)
                                                                       →  bound Manuscript

Manuscripts are decorative collectibles: stored per-player, displayed on Lecterns,
and shown in the encyclopedia. NPC-stocked variants are simple items
(`manuscript_common` / `manuscript_fine` / `manuscript_rare`) sold by the City
Scribe NPC and the Scriptorium outpost — they convert to a fresh Manuscript
when bought, attributed to the seller.
"""
import random
import hashlib
from dataclasses import dataclass, field


@dataclass
class Manuscript:
    uid: str
    origin_biome: str          # biome the flax grew in (drives parchment tone)
    parchment_variety: str     # "tan" | "cream" | "wheat" | "bone" | "rough"
    state: str                 # "raw_parchment" | "scribed" | "illuminated" | "bound"
    ink_key: str               # "ink_black" | "ink_crimson" | ...
    pigment_keys: list         # extra dye_extract keys used in illumination
    illumination_grid: list    # 8×12 grid of color indices (None for empty)
    penmanship: float          # 0.0–1.0  mini-game stroke accuracy
    illumination_quality: float# 0.0–1.0  derived from grid pattern
    page_condition: float      # 0.0–1.0  parchment base quality
    binding: str               # "stitched" | "leather" | "boards"
    content_category: str      # "lore" | "ledger" | "poem" | "map" | "treatise"
    title: str
    scribe_name: str           # "Player" or NPC name
    seed: int
    blend_components: list = field(default_factory=list)
    origin_kingdom: str = ""   # kingdom name where the parchment was pressed


# ── Biome → parchment profile ─────────────────────────────────────────────
# Flax grows in many biomes; the parchment takes on a different tint and
# baseline quality depending on origin.
BIOME_PARCHMENT_PROFILES = {
    "plains":      {"tone": (236, 220, 184), "variety": "cream",  "page_condition": 0.75, "smoothness": 0.80},
    "savanna":     {"tone": (228, 200, 152), "variety": "wheat",  "page_condition": 0.70, "smoothness": 0.65},
    "grassland":   {"tone": (240, 226, 194), "variety": "tan",    "page_condition": 0.72, "smoothness": 0.78},
    "river_delta": {"tone": (244, 232, 208), "variety": "bone",   "page_condition": 0.85, "smoothness": 0.90},
    "highlands":   {"tone": (222, 206, 176), "variety": "rough",  "page_condition": 0.65, "smoothness": 0.55},
    "wetland":     {"tone": (218, 208, 178), "variety": "rough",  "page_condition": 0.60, "smoothness": 0.50},
    "rolling_hills": {"tone": (236, 218, 180), "variety": "cream","page_condition": 0.72, "smoothness": 0.75},
    "boreal":      {"tone": (220, 206, 178), "variety": "tan",    "page_condition": 0.70, "smoothness": 0.70},
}

# ── Ink recipes ────────────────────────────────────────────────────────────
# Iron-gall ink is the base; coloured inks substitute a dye extract for the soot.
INK_RECIPES = {
    "ink_black":   {"label": "Iron Gall Ink", "dye": None,                  "tone": ( 28,  22,  18)},
    "ink_crimson": {"label": "Crimson Ink",   "dye": "dye_extract_crimson", "tone": (170,  38,  50)},
    "ink_cobalt":  {"label": "Cobalt Ink",    "dye": "dye_extract_cobalt",  "tone": ( 40,  70, 168)},
    "ink_verdant": {"label": "Verdant Ink",   "dye": "dye_extract_verdant", "tone": ( 60, 132,  70)},
    "ink_violet":  {"label": "Violet Ink",    "dye": "dye_extract_violet",  "tone": (110,  60, 160)},
    "ink_amber":   {"label": "Amber Ink",     "dye": "dye_extract_amber",   "tone": (200, 142,  50)},
    "ink_indigo":  {"label": "Indigo Ink",    "dye": "dye_extract_indigo",  "tone": ( 38,  50, 110)},
}

# ── Bindings ───────────────────────────────────────────────────────────────
BINDING_PROFILES = {
    "stitched": {"label": "Stitched",    "input_item": "thread",    "quality_bonus": 0.00},
    "leather":  {"label": "Leather",     "input_item": "leather",   "quality_bonus": 0.10},
    "boards":   {"label": "Wood Boards", "input_item": "oak_plank", "quality_bonus": 0.05},
}

# ── Content categories & titles ───────────────────────────────────────────
CONTENT_CATEGORIES = ["lore", "ledger", "poem", "map", "treatise"]

_TITLE_POOLS = {
    "lore": (
        ["Hidden", "Forgotten", "Whispered", "Lost", "Elder", "Wandering"],
        ["Histories", "Tales", "Legends", "Annals", "Chronicles"],
    ),
    "ledger": (
        ["Merchant's", "Harbour", "Granary", "Royal", "Guild"],
        ["Ledger", "Accounts", "Reckoning", "Tally", "Register"],
    ),
    "poem": (
        ["Verses of", "Songs of", "Odes to", "Laments of", "Ballads of"],
        ["Spring", "the Sea", "the Crossing", "Distant Roads", "Old Names"],
    ),
    "map": (
        ["Surveyor's", "Mariner's", "Pilgrim's", "Cartographer's"],
        ["Map", "Atlas", "Charts", "Survey"],
    ),
    "treatise": (
        ["A Treatise on", "Notes on", "Observations of", "Studies in"],
        ["Husbandry", "Astronomy", "Stonework", "Herbs", "Glassmaking", "Coinage"],
    ),
}

BIOME_DISPLAY_NAMES = {
    "plains":        "Plains",
    "savanna":       "Savanna",
    "grassland":     "Grassland",
    "river_delta":   "River Delta",
    "highlands":     "Highlands",
    "wetland":       "Wetland",
    "rolling_hills": "Rolling Hills",
    "boreal":        "Boreal",
    "blend":         "Mixed",
}

UNKNOWN_KINGDOM = "Wildlands"  # fallback when no kingdom claims the location


def kingdom_for_world_x(world, bx: int) -> str:
    """Return the name of the kingdom whose territory contains block-x ``bx``.

    ``bx`` must be in block (tile) units, not pixels.  Falls back to
    ``UNKNOWN_KINGDOM`` when there is no plan, the position is out of bounds,
    or no kingdom claims that cell.
    """
    plan = getattr(world, "plan", None) if world is not None else None
    if plan is None:
        return UNKNOWN_KINGDOM
    cell = plan.cell_for_x(int(bx))
    if cell is None:
        return UNKNOWN_KINGDOM
    ci = cell.index
    for k in plan.kingdoms.values():
        if k.territory_lo <= ci < k.territory_hi:
            return k.name
    return UNKNOWN_KINGDOM


def all_kingdom_names(world) -> list:
    """Ordered list of kingdom names in the current world (for codex rows)."""
    plan = getattr(world, "plan", None) if world is not None else None
    if plan is None:
        return []
    return [k.name for k in sorted(plan.kingdoms.values(), key=lambda k: k.territory_lo)]


def _clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))


def generate_title(category: str, seed: int) -> str:
    rng = random.Random(seed ^ 0xB17B00)
    pre, post = _TITLE_POOLS.get(category, _TITLE_POOLS["lore"])
    return f"{rng.choice(pre)} {rng.choice(post)}"


def grid_quality(grid: list) -> float:
    """Score an illumination grid 0.0–1.0 from fill ratio + colour diversity + symmetry."""
    if not grid:
        return 0.0
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    if rows == 0 or cols == 0:
        return 0.0
    filled = 0
    colors = set()
    sym_match = 0
    sym_total = 0
    for r in range(rows):
        for c in range(cols):
            v = grid[r][c]
            if v is not None:
                filled += 1
                colors.add(v)
            # horizontal symmetry around mid-column
            mirror = grid[r][cols - 1 - c]
            sym_total += 1
            if v == mirror:
                sym_match += 1
    fill_ratio = filled / (rows * cols)
    diversity  = min(1.0, len(colors) / 5.0)
    symmetry   = sym_match / sym_total if sym_total else 0.0
    # Weighting: coverage 50%, variety 25%, symmetry 25%.
    return _clamp(fill_ratio * 0.5 + diversity * 0.25 + symmetry * 0.25)


def stroke_count(grid: list) -> int:
    """Count contiguous coloured strokes for a rough penmanship score."""
    if not grid:
        return 0
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    seen = [[False] * cols for _ in range(rows)]
    strokes = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] is None or seen[r][c]:
                continue
            strokes += 1
            stack = [(r, c)]
            target = grid[r][c]
            while stack:
                y, x = stack.pop()
                if y < 0 or y >= rows or x < 0 or x >= cols: continue
                if seen[y][x] or grid[y][x] != target: continue
                seen[y][x] = True
                stack.extend(((y+1, x), (y-1, x), (y, x+1), (y, x-1)))
    return strokes


class ManuscriptGenerator:
    """Builds raw parchments at the Scribe's Desk and seeds shop-stocked manuscripts."""

    def __init__(self, world_seed: int):
        self._world_seed = world_seed
        self._counter = 0

    def _next_uid(self, tag: str) -> tuple:
        self._counter += 1
        seed = (self._world_seed * 31 + self._counter * 7919) & 0xFFFFFFFF
        uid = hashlib.md5(f"{tag}_{seed}_{self._counter}".encode()).hexdigest()[:12]
        return uid, seed

    def generate_parchment(self, biodome: str, kingdom: str = UNKNOWN_KINGDOM) -> "Manuscript":
        uid, seed = self._next_uid("parchment")
        profile = BIOME_PARCHMENT_PROFILES.get(
            biodome, BIOME_PARCHMENT_PROFILES["plains"])
        rng = random.Random(seed)
        page_condition = _clamp(profile["page_condition"] + rng.gauss(0, 0.06))
        return Manuscript(
            uid=uid,
            origin_biome=biodome,
            parchment_variety=profile["variety"],
            state="raw_parchment",
            ink_key="",
            pigment_keys=[],
            illumination_grid=[[None] * 12 for _ in range(8)],
            penmanship=0.0,
            illumination_quality=0.0,
            page_condition=page_condition,
            binding="",
            content_category="",
            title="",
            scribe_name="",
            seed=seed,
            origin_kingdom=kingdom or UNKNOWN_KINGDOM,
        )

    def generate_shop_manuscript(self, tier: str, biome_hint: str = "plains",
                                 scribe_name: str = "Unknown Scribe",
                                 kingdom: str = UNKNOWN_KINGDOM) -> "Manuscript":
        """Build a finished Manuscript for shop-bought variants."""
        uid, seed = self._next_uid(f"shop_{tier}")
        rng = random.Random(seed)
        biome = biome_hint if biome_hint in BIOME_PARCHMENT_PROFILES else "plains"
        profile = BIOME_PARCHMENT_PROFILES[biome]
        category = rng.choice(CONTENT_CATEGORIES)
        ink_key = rng.choice(list(INK_RECIPES.keys()))
        tier_quality = {"common": 0.45, "fine": 0.70, "rare": 0.90}.get(tier, 0.5)

        # Build a simple decorative grid for shop manuscripts so the codex preview
        # has something to render even when the player didn't paint it.
        grid = [[None] * 12 for _ in range(8)]
        cells = max(6, int(96 * tier_quality * 0.4))
        for _ in range(cells):
            r, c = rng.randrange(8), rng.randrange(12)
            grid[r][c] = rng.randrange(min(5, max(1, int(tier_quality * 6))))
        pigments = list({f"dye_extract_{c}" for c in
                         ("crimson", "cobalt", "amber", "verdant", "indigo")
                         if rng.random() < tier_quality})

        binding = rng.choice(list(BINDING_PROFILES.keys()))
        title = generate_title(category, seed)
        return Manuscript(
            uid=uid,
            origin_biome=biome,
            parchment_variety=profile["variety"],
            state="bound",
            ink_key=ink_key,
            pigment_keys=pigments,
            illumination_grid=grid,
            penmanship=_clamp(tier_quality + rng.gauss(0, 0.05)),
            illumination_quality=grid_quality(grid),
            page_condition=_clamp(profile["page_condition"] + tier_quality * 0.15),
            binding=binding,
            content_category=category,
            title=title,
            scribe_name=scribe_name,
            seed=seed,
            origin_kingdom=kingdom or UNKNOWN_KINGDOM,
        )


def finalize_manuscript(parchment: "Manuscript", ink_key: str, pigment_keys: list,
                        grid: list, binding: str, category: str,
                        scribe_name: str = "You") -> "Manuscript":
    """Convert a raw parchment + player choices into a finished bound Manuscript."""
    binding_profile = BINDING_PROFILES.get(binding, BINDING_PROFILES["stitched"])
    illum_q = grid_quality(grid)
    strokes = stroke_count(grid)
    penmanship = _clamp(0.30 + min(1.0, strokes / 14.0) * 0.55 + illum_q * 0.20
                        + binding_profile["quality_bonus"])
    title = generate_title(category, parchment.seed)
    parchment.state = "bound"
    parchment.ink_key = ink_key
    parchment.pigment_keys = list(pigment_keys)
    parchment.illumination_grid = [row[:] for row in grid]
    parchment.illumination_quality = illum_q
    parchment.penmanship = penmanship
    parchment.binding = binding
    parchment.content_category = category
    parchment.title = title
    parchment.scribe_name = scribe_name
    return parchment


def quality_stars(manuscript: "Manuscript") -> int:
    """0–5 star rating used in the encyclopedia."""
    score = (manuscript.penmanship * 0.4
             + manuscript.illumination_quality * 0.4
             + manuscript.page_condition * 0.2)
    return max(1, min(5, int(round(score * 5))))
