"""WorldPlan: the persisted artifact produced by the worldgen pipeline.

Single source of truth for terrain biome assignment, kingdom identity,
settlement placement (alive + ruined), dynasties, and the historical
chronicle. Runtime systems (world.py, towns.py, cities.py) read from this
instead of computing from seed.

Designed to be cheaply (de)serializable to JSON for SQLite storage.
"""

from dataclasses import dataclass, field, asdict
from typing import Any
import json
import gzip
import base64


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class BiomeCell:
    index: int                  # 0..span-1
    world_x: int                # center block x
    biome: str                  # deep biome (igneous/sedimentary/...)
    biodome: str                # surface biodome (temperate/desert/ocean/...)
    elevation_band: str         # lowland/hill/highland/peak
    elevation: float            # raw 0..1 (for terrain_mod blending)
    coastal: bool
    seed: int                   # deterministic per-cell rng seed
    drama: float = 1.0          # 0.3=flat plains .. 1.0=dramatic peaks


@dataclass
class Settlement:
    settlement_id: int
    kingdom_id: int             # current owner; -1 if ruined+independent
    original_kingdom_id: int    # who founded / first held
    name: str
    cell_index: int
    world_x: int                # center block (within cell, jittered)
    tier: str                   # hamlet/village/town/city/metropolis
    founded_year: int
    is_capital: bool
    dynasty_id: int             # current ruling dynasty; -1 if ruin
    state: str                  # alive / ruin / abandoned
    ruined_year: int = -1
    cause_of_ruin: str = ""     # event id reference
    history_event_ids: list = field(default_factory=list)


@dataclass
class Kingdom:
    kingdom_id: int
    name: str
    biome_group: str            # e.g. "forest", "desert" — for name/heraldry pools
    capital_settlement_id: int
    member_settlement_ids: list
    dynasty_id: int             # current ruling
    leader_title: tuple         # ("King", "Queen") etc.
    agenda: str                 # martial/mercantile/scholarly/pious/builder/hedonist
    heraldry: dict              # coat-of-arms blob from heraldry.py
    color: tuple                # (r, g, b) primary tincture for viz
    founded_year: int
    fallen_year: int = -1       # -1 if still alive
    relations: dict = field(default_factory=dict)   # other_kingdom_id -> "ally"/"rival"/"neutral"
    history_event_ids: list = field(default_factory=list)
    territory_lo: int = 0       # cell index: kingdom's western border
    territory_hi: int = 0       # cell index: kingdom's eastern border (exclusive)


@dataclass
class Person:
    person_id: int
    dynasty_id: int
    name: str
    born_year: int
    died_year: int = -1
    role: str = "scion"         # founder/head/heir/scion/spouse
    parent_ids: tuple = ()
    spouse_id: int = -1
    epithet: str = ""


@dataclass
class Dynasty:
    dynasty_id: int
    house_name: str             # "House Voss"
    founder_id: int
    head_id: int                # current head, or last head if extinct
    members: dict               # person_id -> Person
    extinct_year: int = -1
    history_event_ids: list = field(default_factory=list)


@dataclass
class Event:
    event_id: int
    year: int
    kind: str                   # event type id (war/sack/birth/plague/...)
    text: str                   # rendered chronicle line
    actors: dict = field(default_factory=dict)   # roles -> entity ids
    location_cell: int = -1


@dataclass
class WorldPlan:
    seed: int
    span: int                   # number of cells
    cell_width: int             # blocks per cell
    history_years: int
    cells: list                 # list[BiomeCell]
    kingdoms: dict              # kingdom_id -> Kingdom
    settlements: dict           # settlement_id -> Settlement (alive + ruined)
    dynasties: dict             # dynasty_id -> Dynasty
    chronicle: list             # list[Event] in year order
    lost_artifacts: list = field(default_factory=list)   # list[LostArtifact dicts]

    # ----- coordinate helpers -----
    @property
    def world_min_x(self) -> int:
        return -(self.span * self.cell_width) // 2

    @property
    def world_max_x(self) -> int:
        return (self.span * self.cell_width) // 2

    def cell_for_x(self, x: int):
        idx = (x - self.world_min_x) // self.cell_width
        if idx < 0 or idx >= self.span:
            return None
        return self.cells[idx]

    def in_bounds(self, x: int) -> bool:
        return self.world_min_x <= x < self.world_max_x

    def settlements_in_chunk(self, cx: int, chunk_w: int):
        x0 = cx * chunk_w
        x1 = x0 + chunk_w
        out = []
        for s in self.settlements.values():
            if s.state == "alive" and x0 <= s.world_x < x1:
                out.append(s)
        return out

    def ruins_in_chunk(self, cx: int, chunk_w: int):
        x0 = cx * chunk_w
        x1 = x0 + chunk_w
        return [s for s in self.settlements.values()
                if s.state == "ruin" and x0 <= s.world_x < x1]

    def chronicle_for_settlement(self, settlement_id: int):
        s = self.settlements.get(settlement_id)
        if s is None:
            return []
        return [e for e in self.chronicle if e.event_id in s.history_event_ids]

    def chronicle_for_kingdom(self, kingdom_id: int):
        k = self.kingdoms.get(kingdom_id)
        if k is None:
            return []
        return [e for e in self.chronicle if e.event_id in k.history_event_ids]

    def chronicle_for_dynasty(self, dynasty_id: int):
        d = self.dynasties.get(dynasty_id)
        if d is None:
            return []
        return [e for e in self.chronicle if e.event_id in d.history_event_ids]

    # ----- serialization -----
    def to_blob(self) -> bytes:
        raw = json.dumps(_plan_to_dict(self), separators=(",", ":")).encode("utf-8")
        return gzip.compress(raw, compresslevel=6)

    @staticmethod
    def from_blob(blob: bytes) -> "WorldPlan":
        raw = gzip.decompress(blob)
        return _plan_from_dict(json.loads(raw.decode("utf-8")))


# ---------------------------------------------------------------------------
# Serialization helpers
# ---------------------------------------------------------------------------

def _plan_to_dict(p: WorldPlan) -> dict:
    return {
        "seed": p.seed,
        "span": p.span,
        "cell_width": p.cell_width,
        "history_years": p.history_years,
        "cells": [asdict(c) for c in p.cells],
        "kingdoms": {str(k): _kingdom_dict(v) for k, v in p.kingdoms.items()},
        "settlements": {str(k): asdict(v) for k, v in p.settlements.items()},
        "dynasties": {str(k): _dynasty_dict(v) for k, v in p.dynasties.items()},
        "chronicle": [asdict(e) for e in p.chronicle],
        "lost_artifacts": p.lost_artifacts,
    }


def _kingdom_dict(k: Kingdom) -> dict:
    d = asdict(k)
    d["leader_title"] = list(k.leader_title)
    d["color"] = list(k.color)
    d["relations"] = {str(kk): vv for kk, vv in k.relations.items()}
    return d


def _dynasty_dict(d: Dynasty) -> dict:
    return {
        "dynasty_id": d.dynasty_id,
        "house_name": d.house_name,
        "founder_id": d.founder_id,
        "head_id": d.head_id,
        "extinct_year": d.extinct_year,
        "history_event_ids": d.history_event_ids,
        "members": {str(pid): asdict(p) for pid, p in d.members.items()},
    }


def _plan_from_dict(d: dict) -> WorldPlan:
    cells = [BiomeCell(**c) for c in d["cells"]]
    settlements = {int(k): Settlement(**v) for k, v in d["settlements"].items()}
    kingdoms = {}
    for k, v in d["kingdoms"].items():
        v = dict(v)
        v["leader_title"] = tuple(v["leader_title"])
        v["color"] = tuple(v["color"])
        v["relations"] = {int(kk): vv for kk, vv in v.get("relations", {}).items()}
        kingdoms[int(k)] = Kingdom(**v)
    dynasties = {}
    for k, v in d["dynasties"].items():
        members = {int(pid): Person(**p) for pid, p in v["members"].items()}
        dynasties[int(k)] = Dynasty(
            dynasty_id=v["dynasty_id"],
            house_name=v["house_name"],
            founder_id=v["founder_id"],
            head_id=v["head_id"],
            extinct_year=v.get("extinct_year", -1),
            history_event_ids=v.get("history_event_ids", []),
            members=members,
        )
    chronicle = [Event(**e) for e in d["chronicle"]]
    return WorldPlan(
        seed=d["seed"],
        span=d["span"],
        cell_width=d["cell_width"],
        history_years=d["history_years"],
        cells=cells,
        kingdoms=kingdoms,
        settlements=settlements,
        dynasties=dynasties,
        chronicle=chronicle,
        lost_artifacts=d.get("lost_artifacts", []),
    )
