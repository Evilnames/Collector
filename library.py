"""Library scoring + nearby-library bonus for the manuscript system.

A library is one or more Bookcase blocks placed within a small radius of the
player. Each filled shelf slot contributes raw points; the collection's
diversity (distinct content categories and biomes) multiplies the value.

The aggregate score is exposed to the player as `player.library_quality_bonus`,
which boosts penmanship and illumination floors when finalizing a manuscript
at a nearby Scribe's Desk — a thematic "studied in a well-stocked library"
buff.
"""
from manuscripts import quality_stars


# Player must be within this Manhattan radius (in tiles) of a bookcase for it
# to count toward the active library.
LIBRARY_RADIUS = 10

# Quality-bonus tuning: at maximum diversity + full shelves of high-quality
# manuscripts, the player's binding quality floor lifts by 30%.
MAX_QUALITY_BONUS = 0.30


def library_score(slots):
    """Compute a simple score for a list of (Manuscript | None) shelf slots."""
    filled = [m for m in slots if m is not None]
    categories = {m.content_category for m in filled if m.content_category}
    kingdoms   = {getattr(m, "origin_kingdom", "") for m in filled
                  if getattr(m, "origin_kingdom", "")}
    stars = [quality_stars(m) for m in filled]
    avg_stars = (sum(stars) / len(stars)) if stars else 0.0
    base = sum(stars) * 0.5
    diversity = len(categories) * 1.5 + len(kingdoms) * 0.5
    total = base + diversity
    # quality bonus 0–1 scaled to MAX_QUALITY_BONUS
    quality_bonus = min(MAX_QUALITY_BONUS, total / 40.0 * MAX_QUALITY_BONUS)
    return {
        "total":        total,
        "filled":       len(filled),
        "categories":   len(categories),
        "kingdoms":     len(kingdoms),
        "avg_stars":    avg_stars,
        "quality_bonus": quality_bonus,
    }


def aggregate_nearby_score(world, bx, by, radius=LIBRARY_RADIUS):
    """Combine all bookcases within `radius` tiles into a single score dict."""
    all_slots = []
    bookcases = getattr(world, "bookcase_contents", {}) or {}
    for (cx, cy), slots in bookcases.items():
        if abs(cx - bx) + abs(cy - by) <= radius:
            all_slots.extend(slots)
    return library_score(all_slots)


def update_player_library_bonus(player):
    """Recompute player.library_quality_bonus based on bookcases near the player.

    Should be called periodically (e.g. every few seconds) or when the player
    opens the Scribe's Desk so the bonus is fresh."""
    world = getattr(player, "world", None)
    if world is None:
        player.library_quality_bonus = 0.0
        player.library_score_summary = None
        return
    try:
        bx = int(player.x // 16)
        by = int(player.y // 16)
    except Exception:
        player.library_quality_bonus = 0.0
        player.library_score_summary = None
        return
    summary = aggregate_nearby_score(world, bx, by)
    player.library_quality_bonus = summary["quality_bonus"]
    player.library_score_summary = summary
