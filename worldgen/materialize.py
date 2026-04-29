"""Phase 4: convert post-sim state into a finalized WorldPlan."""

from worldgen.plan import WorldPlan
from worldgen.config import WORLDGEN_CONFIG


def build_plan(seed: int, cells: list, kingdoms: dict, settlements: dict,
               dynasties: dict, chronicle) -> WorldPlan:
    cfg = WORLDGEN_CONFIG
    return WorldPlan(
        seed=seed,
        span=len(cells),
        cell_width=cfg["cell_block_width"],
        history_years=cfg["history_years"],
        cells=cells,
        kingdoms=kingdoms,
        settlements=settlements,
        dynasties=dynasties,
        chronicle=chronicle.to_list(),
    )
