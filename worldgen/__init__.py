"""Multi-pass world generator.

Public entry: ``generate_world(seed, span=None, year_callback=None)`` returns
a fully-baked ``WorldPlan`` ready for runtime consumption.

Phase order:
    1. Geography  — biome strip with streaking and coast logic.
    2. Kingdoms   — seed starting capitals + dynasties at attractive cells.
    3. History    — 500-year tick simulation; mutates kingdoms / settlements.
    4. Materialize— freeze state into the final WorldPlan artifact.
"""

from worldgen.config import WORLDGEN_CONFIG, resolve_span
from worldgen.geography import build_geography
from worldgen.kingdoms import seed_kingdoms
from worldgen.history.sim import simulate_history
from worldgen.history.economy import simulate_economy
from worldgen.materialize import build_plan
from worldgen.plan import WorldPlan
from lost_heritage import ArtifactGenerator


def generate_world(seed: int, span=None, year_callback=None,
                   config_overrides: dict = None) -> WorldPlan:
    """Run the full pipeline and return a WorldPlan.

    ``year_callback(year, kingdoms, settlements, dynasties, chronicle)`` is
    called once per simulated year (used by the worldgen viz screen).
    ``config_overrides`` keys are merged into WORLDGEN_CONFIG for this run only.
    """
    _saved = {}
    if config_overrides:
        for k, v in config_overrides.items():
            _saved[k] = WORLDGEN_CONFIG.get(k)
            WORLDGEN_CONFIG[k] = v
    try:
        if span is None:
            span = WORLDGEN_CONFIG["world_span"]
        span = resolve_span(span)

        cells = build_geography(seed, span)
        kingdoms, settlements, dynasties, next_ids = seed_kingdoms(cells, seed)
        chronicle = simulate_history(seed, cells, kingdoms, settlements, dynasties,
                                     next_ids, year_callback=year_callback)
        guild_histories = simulate_economy(
            seed, kingdoms, dynasties, settlements, cells,
            chronicle.to_list(), WORLDGEN_CONFIG["history_years"])
        plan = build_plan(seed, cells, kingdoms, settlements, dynasties, chronicle)
        plan.guild_histories = guild_histories
        plan.lost_artifacts = ArtifactGenerator().generate_for_world(plan)
        return plan
    finally:
        for k, v in _saved.items():
            if v is None:
                WORLDGEN_CONFIG.pop(k, None)
            else:
                WORLDGEN_CONFIG[k] = v


__all__ = ["generate_world", "WorldPlan", "WORLDGEN_CONFIG"]
