"""Year-tick simulation engine.

Mutates kingdoms / settlements / dynasties over N years; emits chronicle events.
Designed to run in <2s for span 400 with ~5 kingdoms over 500 years.

Public entry: ``simulate_history(...)`` — optionally yields each year via
``year_callback`` so the worldgen viz can paint the strip as the sim runs.
"""

import random

from worldgen.config import WORLDGEN_CONFIG
from worldgen.plan import Settlement, Dynasty, Person
from worldgen.history.chronicle import Chronicle
from worldgen.history.dynasty import age_dynasty, _NAMES, _EPITHETS
from worldgen.history import events as ev


_TIER_PROGRESSION = ["hamlet", "village", "town", "city", "metropolis", "megalopolis"]

# Years of protection a newly founded/reborn kingdom gets before war defeats,
# revolts, and hollowed-out collapses can kill it. Lets fledgling realms stand
# up rather than dying the same decade they're crowned.
_NEW_KINGDOM_GRACE = 30


def _in_grace(k, year: int) -> bool:
    return (year - k.founded_year) < _NEW_KINGDOM_GRACE


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _kingdom_strength(k, settlements: dict) -> float:
    alive = [settlements[sid] for sid in k.member_settlement_ids
             if settlements[sid].state == "alive"]
    if not alive:
        return 0.0
    score = 0.0
    for s in alive:
        score += {"hamlet": 1, "village": 2, "town": 4, "city": 7,
                  "metropolis": 12, "megalopolis": 18}.get(s.tier, 1)
    return score


def _living_kingdoms(kingdoms: dict, settlements: dict) -> list:
    return [k for k in kingdoms.values()
            if k.fallen_year == -1 and _kingdom_strength(k, settlements) > 0]


def _adjacent_enemy(k, kingdoms: dict, settlements: dict, rng) -> object:
    """Pick a kingdom geographically near k's territory."""
    own_cells = [settlements[sid].cell_index for sid in k.member_settlement_ids
                 if settlements[sid].state == "alive"]
    if not own_cells:
        return None
    own_lo, own_hi = min(own_cells), max(own_cells)
    best = []
    for other in _living_kingdoms(kingdoms, settlements):
        if other.kingdom_id == k.kingdom_id:
            continue
        ocells = [settlements[sid].cell_index for sid in other.member_settlement_ids
                  if settlements[sid].state == "alive"]
        if not ocells:
            continue
        gap = max(0, max(min(ocells) - own_hi, own_lo - max(ocells)))
        best.append((gap, other))
    if not best:
        return None
    best.sort(key=lambda t: t[0])
    return best[0][1] if rng.random() < 0.7 else rng.choice(best)[1]


# ---------------------------------------------------------------------------
# Settlement lifecycle
# ---------------------------------------------------------------------------

# Per-tier base growth chance (per year). Tapers sharply so the world isn't
# carpeted in metropolises — most settlements should plateau at hamlet/village,
# a few reach town, fewer reach city, and metropolis/megalopolis are landmarks.
_GROW_CHANCE = {
    "hamlet":     0.030,    # ~80% chance to reach village over 500 yr
    "village":    0.012,    # ~45% chance to reach town
    "town":       0.0035,   # ~17% chance to reach city
    "city":       0.0010,   # ~5% chance to reach metropolis
    "metropolis": 0.00025,  # ~1% chance to reach megalopolis
}


def _try_grow(s: Settlement, k, year: int, rng, chronicle, kingdoms, settlements, dynasties):
    if s.state != "alive":
        return
    cur = _TIER_PROGRESSION.index(s.tier)
    if cur >= len(_TIER_PROGRESSION) - 1:
        return
    growth_chance = _GROW_CHANCE.get(s.tier, 0.0)
    if k.agenda == "builder":
        growth_chance *= 1.8
    if k.agenda == "mercantile" and s.is_capital:
        growth_chance *= 1.5
    if rng.random() < growth_chance:
        s.tier = _TIER_PROGRESSION[cur + 1]
        dyn = dynasties.get(s.dynasty_id)
        chronicle.emit(year, "grow_to_tier", ev.text_grow(s, s.tier),
                       actors={"settlement": s.settlement_id},
                       location_cell=s.cell_index,
                       attach_to=[s, k, dyn])


def _try_shrink(s: Settlement, k, year: int, rng, chronicle, kingdoms, settlements, dynasties):
    """Cities drop a tier under stress: weak kingdom, recent disaster, generic decline."""
    if s.state != "alive":
        return
    cur = _TIER_PROGRESSION.index(s.tier)
    if cur == 0:
        # Hamlet: tiny chance to be abandoned outright.
        if rng.random() < 0.0015:
            s.state = "abandoned"
            s.ruined_year = year
            s.cause_of_ruin = "decline"
            dyn = dynasties.get(s.dynasty_id)
            chronicle.emit(year, "abandon", ev.text_decline(s),
                           actors={"settlement": s.settlement_id},
                           location_cell=s.cell_index, attach_to=[s, k, dyn])
        return
    shrink_chance = ev.EVENT_RATES["city_shrink"]
    # Weak kingdoms shrink more.
    strength = _kingdom_strength(k, settlements)
    if strength < 8:
        shrink_chance *= 2.5
    # Capital is sturdier.
    if s.is_capital:
        shrink_chance *= 0.4
    if rng.random() < shrink_chance:
        new_tier = _TIER_PROGRESSION[cur - 1]
        s.tier = new_tier
        dyn = dynasties.get(s.dynasty_id)
        chronicle.emit(year, "shrink", ev.text_shrink(s, new_tier),
                       actors={"settlement": s.settlement_id},
                       location_cell=s.cell_index, attach_to=[s, k, dyn])


def _try_merge(k, year: int, rng, chronicle, settlements, dynasties):
    """Big city absorbs adjacent same-kingdom settlement."""
    members = [settlements[sid] for sid in k.member_settlement_ids
               if settlements[sid].state == "alive"]
    bigs = [s for s in members if s.tier in ("city", "metropolis", "megalopolis")]
    smalls = [s for s in members if s.tier in ("hamlet", "village", "town")]
    if not bigs or not smalls:
        return
    if rng.random() > 0.005:
        return
    big = rng.choice(bigs)
    near = sorted(smalls, key=lambda s: abs(s.cell_index - big.cell_index))[0]
    if abs(near.cell_index - big.cell_index) > 3:
        return
    near.state = "abandoned"
    if big.tier == "city":
        big.tier = "metropolis"
    elif big.tier == "metropolis":
        big.tier = "megalopolis"
    dyn = dynasties.get(big.dynasty_id)
    chronicle.emit(year, "merge", ev.text_merge(big, near),
                   actors={"big": big.settlement_id, "small": near.settlement_id},
                   location_cell=big.cell_index, attach_to=[big, near, k, dyn])


# ---------------------------------------------------------------------------
# Founding
# ---------------------------------------------------------------------------

def _try_found(k, year, rng, chronicle, kingdoms, settlements, cells, next_settlement_id):
    """Builder-leaning kingdoms expand by founding new settlements on free cells."""
    rate = ev.EVENT_RATES["found_settlement"]
    if k.agenda == "builder":
        rate *= 3.0
    if rng.random() > rate:
        return
    own_cells = [settlements[sid].cell_index for sid in k.member_settlement_ids
                 if settlements[sid].state == "alive"]
    if not own_cells:
        return
    span = len(cells)
    cap_idx = own_cells[len(own_cells) // 2]
    # Stay inside the kingdom's territory and keep the same wide minimum
    # separation as initial seeding. Settlements stay clearly part of one
    # kingdom and never crowd into a neighbor's land.
    SETTLEMENT_MIN_SEP = WORLDGEN_CONFIG.get("settlement_min_separation_cells", 14)
    terr_lo = getattr(k, "territory_lo", 0)
    terr_hi = getattr(k, "territory_hi", span)
    occupied = {s.cell_index for s in settlements.values() if s.state == "alive"}
    def _too_close(cidx):
        return any(abs(cidx - oc) < SETTLEMENT_MIN_SEP for oc in occupied)
    candidates = []
    for delta in range(SETTLEMENT_MIN_SEP, max(SETTLEMENT_MIN_SEP + 1, (terr_hi - terr_lo) // 2 + 1)):
        for cidx in (cap_idx - delta, cap_idx + delta):
            if (terr_lo <= cidx < terr_hi
                    and not _cell_occupied(cidx, settlements)
                    and not _too_close(cidx)
                    and cells[cidx].biodome != "ocean"):
                candidates.append(cidx)
        if candidates:
            break
    if not candidates:
        return
    cidx = rng.choice(candidates)
    cell = cells[cidx]
    sid = next_settlement_id[0]; next_settlement_id[0] += 1
    name = _gen_settlement_name(rng)
    cell_w = WORLDGEN_CONFIG["cell_block_width"]
    settlements[sid] = Settlement(
        settlement_id=sid,
        kingdom_id=k.kingdom_id,
        original_kingdom_id=k.kingdom_id,
        name=name,
        cell_index=cidx,
        world_x=cell.world_x + rng.randint(-cell_w // 4, cell_w // 4),
        tier="hamlet",
        founded_year=year,
        is_capital=False,
        dynasty_id=k.dynasty_id,
        state="alive",
    )
    k.member_settlement_ids.append(sid)
    chronicle.emit(year, "found_settlement",
                   ev.text_found(k, settlements[sid], cell),
                   actors={"kingdom": k.kingdom_id, "settlement": sid},
                   location_cell=cidx, attach_to=[settlements[sid], k])


def _cell_occupied(cell_idx: int, settlements: dict) -> bool:
    return any(s.cell_index == cell_idx and s.state == "alive"
               for s in settlements.values())


def _gen_settlement_name(rng):
    syl_a = ["Bel","Cor","Dra","Esk","Far","Gal","Hek","Ire","Jor","Kel",
             "Lor","Mor","Nor","Ovel","Pyr","Quill","Rev","Sar","Tal","Ulm"]
    syl_b = ["mar","ford","wyn","stead","reach","mere","gate","vale",
             "thorn","keep","run","hold","brook","crest"]
    return rng.choice(syl_a) + rng.choice(syl_b)


# ---------------------------------------------------------------------------
# War / disasters
# ---------------------------------------------------------------------------

def _try_war(k, year, rng, chronicle, kingdoms, settlements, dynasties):
    rate = ev.EVENT_RATES["war_declare"]
    if k.agenda == "martial":
        rate *= 3.0
    if rng.random() > rate:
        return
    enemy = _adjacent_enemy(k, kingdoms, settlements, rng)
    if enemy is None:
        return
    chronicle.emit(year, "declare_war", ev.text_war_declare(k, enemy),
                   actors={"attacker": k.kingdom_id, "defender": enemy.kingdom_id},
                   attach_to=[k, enemy])
    k.relations[enemy.kingdom_id] = "rival"
    enemy.relations[k.kingdom_id] = "rival"

    # Resolve a battle outcome: strength + dice.
    s_atk = _kingdom_strength(k, settlements) + rng.uniform(0, 5)
    s_def = _kingdom_strength(enemy, settlements) + rng.uniform(0, 5)
    if s_atk > s_def:
        # Attacker takes a defender settlement. Capitals are tougher targets;
        # prefer non-capital. Annex more often than sack so the world keeps
        # alive cities to inhabit.
        targets = [settlements[sid] for sid in enemy.member_settlement_ids
                   if settlements[sid].state == "alive"]
        if targets:
            non_caps = [t for t in targets if not t.is_capital]
            tgt = rng.choice(non_caps) if non_caps else rng.choice(targets)
            if rng.random() < 0.25 and not tgt.is_capital:
                _sack_settlement(tgt, k, enemy, year, rng, chronicle, kingdoms, settlements, dynasties)
            else:
                _annex_settlement(tgt, k, enemy, year, chronicle, kingdoms, settlements, dynasties)
            # Check defender collapse.
            if _kingdom_strength(enemy, settlements) <= 0 and not _in_grace(enemy, year):
                enemy.fallen_year = year
                chronicle.emit(year, "defeat_kingdom",
                               ev.text_defeat(k, enemy),
                               actors={"victor": k.kingdom_id, "loser": enemy.kingdom_id},
                               attach_to=[k, enemy])


def _sack_settlement(s, attacker, defender, year, rng, chronicle, kingdoms, settlements, dynasties):
    s.state = "ruin"
    s.ruined_year = year
    dyn = dynasties.get(s.dynasty_id)
    chronicle.emit(year, "sack",
                   ev.text_sack(attacker, defender, s),
                   actors={"attacker": attacker.kingdom_id,
                           "defender": defender.kingdom_id,
                           "settlement": s.settlement_id},
                   location_cell=s.cell_index, attach_to=[s, attacker, defender, dyn])
    s.cause_of_ruin = "sacked"
    if s.is_capital:
        # Capital lost — try to relocate to the largest surviving member.
        survivors = [settlements[sid] for sid in defender.member_settlement_ids
                     if settlements[sid].state == "alive"]
        if survivors:
            new_cap = max(survivors, key=lambda x: _TIER_PROGRESSION.index(x.tier))
            new_cap.is_capital = True
            defender.capital_settlement_id = new_cap.settlement_id


def _annex_settlement(s, attacker, defender, year, chronicle, kingdoms, settlements, dynasties):
    if s.settlement_id in defender.member_settlement_ids:
        defender.member_settlement_ids.remove(s.settlement_id)
    s.kingdom_id = attacker.kingdom_id
    s.dynasty_id = attacker.dynasty_id
    attacker.member_settlement_ids.append(s.settlement_id)
    dyn = dynasties.get(s.dynasty_id)
    chronicle.emit(year, "annex",
                   ev.text_annex(attacker, defender, s),
                   actors={"attacker": attacker.kingdom_id,
                           "defender": defender.kingdom_id,
                           "settlement": s.settlement_id},
                   location_cell=s.cell_index, attach_to=[s, attacker, defender, dyn])


def _try_disaster(k, year, rng, chronicle, settlements, dynasties):
    if rng.random() < ev.EVENT_RATES["plague"]:
        chronicle.emit(year, "plague", ev.text_plague(k),
                       actors={"kingdom": k.kingdom_id}, attach_to=[k])
        # 30% chance one settlement abandons due to plague.
        if rng.random() < 0.3:
            members = [settlements[sid] for sid in k.member_settlement_ids
                       if settlements[sid].state == "alive" and not settlements[sid].is_capital]
            if members:
                s = rng.choice(members)
                s.state = "abandoned"
                s.ruined_year = year
                s.cause_of_ruin = "plague"
                chronicle.emit(year, "abandon", ev.text_decline(s),
                               actors={"settlement": s.settlement_id},
                               location_cell=s.cell_index, attach_to=[s, k])

    if rng.random() < ev.EVENT_RATES["famine"]:
        chronicle.emit(year, "famine", ev.text_famine(k),
                       actors={"kingdom": k.kingdom_id}, attach_to=[k])

    if rng.random() < ev.EVENT_RATES["earthquake"]:
        members = [settlements[sid] for sid in k.member_settlement_ids
                   if settlements[sid].state == "alive"]
        if members:
            s = rng.choice(members)
            s.state = "ruin"
            s.ruined_year = year
            s.cause_of_ruin = "earthquake"
            dyn = dynasties.get(s.dynasty_id)
            chronicle.emit(year, "earthquake", ev.text_earthquake(s),
                           actors={"settlement": s.settlement_id},
                           location_cell=s.cell_index, attach_to=[s, k, dyn])
            if s.is_capital:
                survivors = [settlements[sid] for sid in k.member_settlement_ids
                             if settlements[sid].state == "alive"]
                if survivors:
                    new_cap = max(survivors,
                                  key=lambda x: _TIER_PROGRESSION.index(x.tier))
                    new_cap.is_capital = True
                    k.capital_settlement_id = new_cap.settlement_id


# ---------------------------------------------------------------------------
# Political events: alliances, revolts, civil war, kingdom split, rebirth
# ---------------------------------------------------------------------------

def _try_alliance(k, year, rng, chronicle, kingdoms, settlements):
    """Two kingdoms with shared interests sign a formal alliance."""
    if rng.random() > ev.EVENT_RATES["alliance_form"]:
        return
    candidates = [other for other in _living_kingdoms(kingdoms, settlements)
                  if other.kingdom_id != k.kingdom_id
                  and k.relations.get(other.kingdom_id) == "neutral"]
    if not candidates:
        return
    # Mercantile/scholarly/pious agendas seek alliances; martial/hedonist rarely.
    affinity = {"mercantile": 1.4, "scholarly": 1.2, "pious": 1.3,
                "builder": 1.0, "martial": 0.4, "hedonist": 0.7}
    weighted = []
    for o in candidates:
        w = affinity.get(k.agenda, 1.0) * affinity.get(o.agenda, 1.0)
        if k.biome_group == o.biome_group:
            w *= 1.3   # cultural kinship
        weighted.append((w, o))
    total = sum(w for w, _ in weighted)
    pick = rng.random() * total
    acc = 0.0
    chosen = weighted[0][1]
    for w, o in weighted:
        acc += w
        if acc >= pick:
            chosen = o
            break
    k.relations[chosen.kingdom_id] = "ally"
    chosen.relations[k.kingdom_id] = "ally"
    chronicle.emit(year, "alliance_form", ev.text_alliance_form(k, chosen),
                   actors={"a": k.kingdom_id, "b": chosen.kingdom_id},
                   attach_to=[k, chosen])


def _try_break_alliance(k, year, rng, chronicle, kingdoms):
    """Existing alliances drift; some snap. Reasons attached to the chronicle line."""
    allies = [oid for oid, rel in k.relations.items() if rel == "ally"]
    if not allies:
        return
    if rng.random() > ev.EVENT_RATES["alliance_break"]:
        return
    other_id = rng.choice(allies)
    other = kingdoms.get(other_id)
    if other is None or other.fallen_year != -1:
        return
    reasons = ["a trade dispute soured both courts",
               "a marriage was withdrawn at the last hour",
               "a shared border was contested by lesser lords",
               "a tribute went unpaid for three winters",
               "an heir was insulted at a feast",
               "a dynastic claim was made and refused"]
    reason = rng.choice(reasons)
    k.relations[other_id] = "rival"
    other.relations[k.kingdom_id] = "rival"
    chronicle.emit(year, "alliance_break", ev.text_alliance_break(k, other, reason),
                   actors={"a": k.kingdom_id, "b": other_id},
                   attach_to=[k, other])


def _try_revolt(k, year, rng, chronicle, kingdoms, settlements, dynasties):
    """An outlying town rebels — either declares independence or defects to a neighbor."""
    if _in_grace(k, year):
        return
    members = [settlements[sid] for sid in k.member_settlement_ids
               if settlements[sid].state == "alive" and not settlements[sid].is_capital]
    if not members:
        return
    capital = settlements.get(k.capital_settlement_id)
    if capital is None:
        return
    # Outlying = far from capital, lower tier.
    candidates = []
    for s in members:
        dist = abs(s.cell_index - capital.cell_index)
        # Distance scaling caps at 2.0x so very wide kingdoms don't auto-shed.
        dist_mult = min(2.0, 1.0 + dist / 20.0)
        p = ev.EVENT_RATES["revolt"] * dist_mult
        if _kingdom_strength(k, settlements) < 6:
            p *= 1.5
        if k.agenda in ("martial", "hedonist"):
            p *= 1.3
        candidates.append((p, s))
    for p, s in candidates:
        if rng.random() >= p:
            continue
        # Decide outcome: independence or defection.
        neighbors = [other for other in _living_kingdoms(kingdoms, settlements)
                     if other.kingdom_id != k.kingdom_id]
        nearest = None
        if neighbors:
            nearest = min(neighbors, key=lambda o:
                abs(o.territory_lo + o.territory_hi - 2 * s.cell_index))
        defect = (nearest is not None
                  and (k.relations.get(nearest.kingdom_id) == "rival" or rng.random() < 0.45))
        if defect and nearest is not None:
            k.member_settlement_ids.remove(s.settlement_id)
            s.kingdom_id = nearest.kingdom_id
            s.dynasty_id = nearest.dynasty_id
            nearest.member_settlement_ids.append(s.settlement_id)
            chronicle.emit(year, "revolt_defect",
                           ev.text_revolt_defect(s, k, nearest),
                           actors={"settlement": s.settlement_id,
                                   "old_kingdom": k.kingdom_id,
                                   "new_kingdom": nearest.kingdom_id},
                           location_cell=s.cell_index,
                           attach_to=[s, k, nearest])
            return  # one revolt per kingdom-tick
        # Independence: orphan the settlement (kingdom_id stays so chronicle
        # can trace origin, but mark a special flag via cause field).
        k.member_settlement_ids.remove(s.settlement_id)
        s.kingdom_id = -1     # masterless
        chronicle.emit(year, "revolt_independent",
                       ev.text_revolt_independent(s, k),
                       actors={"settlement": s.settlement_id,
                               "old_kingdom": k.kingdom_id},
                       location_cell=s.cell_index,
                       attach_to=[s, k])
        return


def _try_civil_war(k, year, rng, chronicle, kingdoms, settlements, dynasties,
                   next_dynasty_id, next_person_id):
    """Civil war can split a kingdom into two. Triggered by tension + size."""
    members = [settlements[sid] for sid in k.member_settlement_ids
               if settlements[sid].state == "alive"]
    if len(members) < 4:
        return  # too small to fracture
    rate = ev.EVENT_RATES["civil_war"]
    # Recent succession crises raise tension.
    recent_window = 30
    crisis_recent = any(e.year > year - recent_window
                        and e.kind in ("succession_crisis", "extinction")
                        and e.actors.get("dynasty") == k.dynasty_id
                        for e in chronicle.events)
    if crisis_recent:
        rate *= 4.0
    # Hedonist/martial agendas more likely to fracture; pious least.
    if k.agenda in ("hedonist", "martial"):
        rate *= 1.5
    if k.agenda == "pious":
        rate *= 0.5
    if rng.random() >= rate:
        return
    # Pick a faction leader (a sibling/heir) and a side of the kingdom to keep.
    # Faction names from agenda/dynasty.
    capital = settlements.get(k.capital_settlement_id)
    if capital is None:
        return
    dyn = dynasties.get(k.dynasty_id)
    if dyn is None:
        return
    house = dyn.house_name
    rebel_faction = f"the {rng.choice(['Younger','Outer','Border','Lower'])} branch of {house}"
    loyal_faction = f"the {rng.choice(['Elder','Inner','Crown','High'])} branch of {house}"
    chronicle.emit(year, "civil_war",
                   ev.text_civil_war(k, rebel_faction, loyal_faction),
                   actors={"kingdom": k.kingdom_id, "dynasty": k.dynasty_id},
                   attach_to=[k, dyn])
    # Decide: split (40% by default) or one side wins (no split, just chronicle weight).
    if rng.random() >= ev.EVENT_RATES["kingdom_split"]:
        return
    _split_kingdom(k, year, rng, chronicle, kingdoms, settlements, dynasties,
                   next_dynasty_id, next_person_id, rebel_faction)


def _split_kingdom(parent, year, rng, chronicle, kingdoms, settlements, dynasties,
                   next_dynasty_id, next_person_id, rebel_label: str):
    """Eastern (or western) half of parent kingdom breaks off into a new kingdom
    with a cadet dynasty branch."""
    members = sorted(
        [settlements[sid] for sid in parent.member_settlement_ids
         if settlements[sid].state == "alive"],
        key=lambda s: s.cell_index)
    if len(members) < 4:
        return
    capital = settlements.get(parent.capital_settlement_id)
    if capital is None:
        return
    # Pick split axis: settlements on the side OPPOSITE the capital break off.
    cap_x = capital.cell_index
    east = [s for s in members if s.cell_index > cap_x]
    west = [s for s in members if s.cell_index < cap_x]
    breakaway_side = east if len(east) >= len(west) else west
    if len(breakaway_side) < 2:
        return

    # New dynasty: cadet branch.
    parent_dyn = dynasties.get(parent.dynasty_id)
    if parent_dyn is None:
        return
    cadet_pid = next_person_id[0]; next_person_id[0] += 1
    cadet_did = next_dynasty_id[0]; next_dynasty_id[0] += 1
    cadet_founder = Person(
        person_id=cadet_pid,
        dynasty_id=cadet_did,
        name=rng.choice(["Voren","Kara","Mirek","Shara","Tael","Yssa","Branor","Pell"]),
        born_year=year - rng.randint(20, 35),
        role="founder",
        epithet="the Breaker" if rng.random() < 0.5 else "the Free-Hand",
    )
    parent_house = parent_dyn.house_name
    base = parent_house.replace("House ", "") if parent_house.startswith("House ") else parent_house
    cadet_house = f"House {base}-{rng.choice(['Vael','Mor','Sar','Wyn','Drak','Ren'])}"
    cadet_dyn = Dynasty(
        dynasty_id=cadet_did,
        house_name=cadet_house,
        founder_id=cadet_founder.person_id,
        head_id=cadet_founder.person_id,
        members={cadet_founder.person_id: cadet_founder},
    )
    dynasties[cadet_did] = cadet_dyn

    # New kingdom from the breakaway side.
    new_kid = max(kingdoms.keys()) + 1
    # Heraldry: same primary tincture, different charge to mark schism.
    heraldry_clone = dict(parent.heraldry)
    heraldry_clone["charge"] = rng.choice(["sword","crown","star","eye","none","tower"])
    # Name: cadet variant of parent.
    breakaway_name = parent.name + " " + rng.choice(["Free State","Marches","Reach","Holdings"])
    # Pick a new capital from the breakaway side: largest tier, fall back to first.
    new_capital = max(breakaway_side,
                      key=lambda s: _TIER_PROGRESSION.index(s.tier))
    # Compute new territories: split parent's territory at the boundary.
    boundary = (min(s.cell_index for s in breakaway_side) +
                max(s.cell_index for s in breakaway_side)) // 2
    if breakaway_side is east:
        new_lo, new_hi = boundary - 1, parent.territory_hi
        parent.territory_hi = boundary - 1
    else:
        new_lo, new_hi = parent.territory_lo, boundary + 1
        parent.territory_lo = boundary + 1

    new_kingdom = type(parent)(
        kingdom_id=new_kid,
        name=breakaway_name,
        biome_group=parent.biome_group,
        capital_settlement_id=new_capital.settlement_id,
        member_settlement_ids=[s.settlement_id for s in breakaway_side],
        dynasty_id=cadet_did,
        leader_title=parent.leader_title,
        agenda=rng.choice(list({"martial","mercantile","scholarly","pious","builder","hedonist"} - {parent.agenda})),
        heraldry=heraldry_clone,
        color=parent.color,
        founded_year=year,
        territory_lo=new_lo,
        territory_hi=new_hi,
    )
    # Wire relations: parent <-> new are bitter rivals.
    for kid_other, rel in parent.relations.items():
        new_kingdom.relations[kid_other] = rel if rel != "ally" else "neutral"
    new_kingdom.relations[parent.kingdom_id] = "rival"
    parent.relations[new_kid] = "rival"
    for other in kingdoms.values():
        if other.kingdom_id == parent.kingdom_id:
            continue
        other.relations[new_kid] = other.relations.get(parent.kingdom_id, "neutral")
    kingdoms[new_kid] = new_kingdom

    # Move settlements over.
    for s in breakaway_side:
        parent.member_settlement_ids.remove(s.settlement_id)
        s.kingdom_id = new_kid
        s.dynasty_id = cadet_did
        s.original_kingdom_id = new_kid
        if s is new_capital:
            s.is_capital = True
        else:
            s.is_capital = False

    chronicle.emit(year, "kingdom_split",
                   ev.text_kingdom_split(parent, new_kingdom, cadet_house, rebel_label),
                   actors={"parent": parent.kingdom_id, "breakaway": new_kid,
                           "cadet_dynasty": cadet_did},
                   attach_to=[parent, new_kingdom, parent_dyn, cadet_dyn])


def _try_kingdom_reborn(year, rng, chronicle, kingdoms, settlements, dynasties,
                        cells, next_dynasty_id, next_person_id):
    """Three or more masterless settlements (kingdom_id=-1) cluster together
    and someone declares a new kingdom over them."""
    orphans = [s for s in settlements.values()
               if s.state == "alive" and s.kingdom_id == -1]
    if len(orphans) < 2:
        return
    if rng.random() >= ev.EVENT_RATES["rebirth"]:
        return
    # Pick a centroid orphan with at least 1 other orphan within ~12 cells.
    rng.shuffle(orphans)
    cluster = None
    for seed_s in orphans:
        nearby = [s for s in orphans if abs(s.cell_index - seed_s.cell_index) <= 12]
        if len(nearby) >= 2:
            cluster = nearby
            break
    if cluster is None:
        return
    # New dynasty + kingdom. Promote the chosen capital so the fledgling
    # realm starts above the "weak kingdom" thresholds.
    cap = max(cluster, key=lambda s: _TIER_PROGRESSION.index(s.tier))
    if _TIER_PROGRESSION.index(cap.tier) < _TIER_PROGRESSION.index("village"):
        cap.tier = "village"
    dyn_id = next_dynasty_id[0]; next_dynasty_id[0] += 1
    pid = next_person_id[0]; next_person_id[0] += 1
    founder = Person(
        person_id=pid, dynasty_id=dyn_id,
        name=rng.choice(["Halvin","Talra","Ovenor","Selin","Dremar","Ysra"]),
        born_year=year - rng.randint(25, 40),
        role="founder",
        epithet=rng.choice(["the Unifier","the Crowned-Late","the Common-Born","the Free-Risen"]),
    )
    house = "House " + rng.choice(["Verren","Halmar","Tarsil","Brennar","Ostrik","Wyldun"])
    new_dyn = Dynasty(dynasty_id=dyn_id, house_name=house,
                      founder_id=founder.person_id, head_id=founder.person_id,
                      members={founder.person_id: founder})
    dynasties[dyn_id] = new_dyn
    new_kid = max(kingdoms.keys()) + 1
    name_root = rng.choice(["Free", "United", "Crown", "Reborn", "New"])
    biome_group = "highland"
    territory_cells = [s.cell_index for s in cluster]
    new_kingdom = type(next(iter(kingdoms.values())))(
        kingdom_id=new_kid,
        name=f"{name_root} {cap.name}",
        biome_group=biome_group,
        capital_settlement_id=cap.settlement_id,
        member_settlement_ids=[s.settlement_id for s in cluster],
        dynasty_id=dyn_id,
        leader_title=("Steward","Steward"),
        agenda=rng.choice(["builder","mercantile","scholarly"]),
        heraldry={"primary":[140,140,140],"secondary":[60,60,60],"metal":[210,210,210],
                  "division":"plain","ordinary":"none","charge":"crown","motto":"Reborn"},
        color=(140,140,140),
        founded_year=year,
        territory_lo=min(territory_cells) - 4,
        territory_hi=max(territory_cells) + 4,
    )
    for kid_other in kingdoms:
        new_kingdom.relations[kid_other] = "neutral"
    for k in kingdoms.values():
        k.relations[new_kid] = "neutral"
    kingdoms[new_kid] = new_kingdom
    for s in cluster:
        s.kingdom_id = new_kid
        s.dynasty_id = dyn_id
        if s is cap:
            s.is_capital = True
    chronicle.emit(year, "kingdom_reborn",
                   ev.text_kingdom_reborn(new_kingdom, len(cluster)),
                   actors={"kingdom": new_kid, "dynasty": dyn_id},
                   attach_to=[new_kingdom, new_dyn])


def _try_assassination(dyn, year, rng, chronicle):
    """During a contested succession, an heir may eliminate a sibling."""
    if rng.random() >= ev.EVENT_RATES["assassination"]:
        return
    living_heirs = [p for p in dyn.members.values()
                    if p.died_year == -1 and p.role in ("scion", "heir")
                    and year - p.born_year >= 14]
    if len(living_heirs) < 2:
        return
    living_heirs.sort(key=lambda p: p.born_year)
    killer = living_heirs[0]
    victim = living_heirs[1]
    victim.died_year = year
    killer.epithet = "the Blood-Hand"
    chronicle.emit(year, "assassination",
                   ev.text_assassination(killer, victim, dyn),
                   actors={"killer": killer.person_id, "victim": victim.person_id,
                           "dynasty": dyn.dynasty_id},
                   attach_to=[dyn])


# ---------------------------------------------------------------------------
# Public entry
# ---------------------------------------------------------------------------

def simulate_history(seed: int, cells: list, kingdoms: dict, settlements: dict,
                     dynasties: dict, next_ids: tuple, years: int = None,
                     year_callback=None) -> Chronicle:
    cfg = WORLDGEN_CONFIG
    years = years or cfg["history_years"]
    chronicle = Chronicle()
    rng = random.Random(seed ^ 0x4157_0712)

    next_person_id, next_dynasty_id, next_settlement_id = next_ids
    next_person_id = [next_person_id]
    next_dynasty_id = [next_dynasty_id]
    next_settlement_id = [next_settlement_id]

    for year in range(1, years + 1):
        # Dynasty tick.
        for dyn in list(dynasties.values()):
            def _dyn_event(kind, person, **kw):
                if kind == "death":
                    chronicle.emit(year, "death", ev.text_death(person, dyn),
                                   actors={"person": person.person_id, "dynasty": dyn.dynasty_id},
                                   attach_to=[dyn])
                elif kind == "birth":
                    chronicle.emit(year, "birth", ev.text_birth(person, dyn),
                                   actors={"person": person.person_id, "dynasty": dyn.dynasty_id},
                                   attach_to=[dyn])
                elif kind == "marriage":
                    spouse = kw["spouse"]
                    chronicle.emit(year, "marriage",
                                   ev.text_marriage(person, spouse, dyn),
                                   actors={"a": person.person_id, "b": spouse.person_id,
                                           "dynasty": dyn.dynasty_id},
                                   attach_to=[dyn])
                elif kind == "succession":
                    chronicle.emit(year, "succession",
                                   ev.text_succession(person, dyn),
                                   actors={"person": person.person_id, "dynasty": dyn.dynasty_id},
                                   attach_to=[dyn])
                elif kind == "succession_crisis":
                    chronicle.emit(year, "succession_crisis",
                                   ev.text_succession_crisis(person, dyn),
                                   actors={"person": person.person_id, "dynasty": dyn.dynasty_id},
                                   attach_to=[dyn])
                elif kind == "extinction":
                    chronicle.emit(year, "extinction", ev.text_extinction(dyn),
                                   actors={"dynasty": dyn.dynasty_id}, attach_to=[dyn])
                    # If dynasty was ruling, mark kingdom fallen.
                    for k in kingdoms.values():
                        if k.dynasty_id == dyn.dynasty_id and k.fallen_year == -1:
                            k.fallen_year = year
                            chronicle.emit(year, "kingdom_collapse",
                                           f"{k.name} collapsed without heir.",
                                           actors={"kingdom": k.kingdom_id},
                                           attach_to=[k])
            age_dynasty(dyn, year, rng, next_person_id, _dyn_event)

        # Settlement / kingdom ticks.
        for k in list(kingdoms.values()):
            if k.fallen_year != -1:
                continue
            for sid in list(k.member_settlement_ids):
                _try_grow(settlements[sid], k, year, rng, chronicle,
                          kingdoms, settlements, dynasties)
                _try_shrink(settlements[sid], k, year, rng, chronicle,
                            kingdoms, settlements, dynasties)
            _try_merge(k, year, rng, chronicle, settlements, dynasties)
            _try_found(k, year, rng, chronicle, kingdoms, settlements,
                       cells, next_settlement_id)
            _try_war(k, year, rng, chronicle, kingdoms, settlements, dynasties)
            _try_disaster(k, year, rng, chronicle, settlements, dynasties)
            _try_alliance(k, year, rng, chronicle, kingdoms, settlements)
            _try_break_alliance(k, year, rng, chronicle, kingdoms)
            _try_revolt(k, year, rng, chronicle, kingdoms, settlements, dynasties)
            _try_civil_war(k, year, rng, chronicle, kingdoms, settlements, dynasties,
                           next_dynasty_id, next_person_id)
            # Weak kingdoms collapse on their own — but only if hollowed-out
            # (no capital alive, or one settlement left). A wounded but
            # functioning kingdom can recover.
            if year > 30 and not _in_grace(k, year):
                alive_members = [settlements[sid] for sid in k.member_settlement_ids
                                 if settlements[sid].state == "alive"]
                cap_alive = (k.capital_settlement_id is not None
                             and k.capital_settlement_id in settlements
                             and settlements[k.capital_settlement_id].state == "alive")
                hollowed = (not cap_alive) or len(alive_members) <= 1
                if hollowed and rng.random() < 0.06:
                    k.fallen_year = year
                    chronicle.emit(year, "kingdom_collapse",
                                   ev.text_kingdom_collapse(k),
                                   actors={"kingdom": k.kingdom_id},
                                   attach_to=[k])
                    # Surviving members go independent (orphans available for rebirth).
                    for s in alive_members:
                        s.is_capital = False
                        s.kingdom_id = -1

        # Cross-kingdom: orphan settlements may coalesce into a new realm.
        _try_kingdom_reborn(year, rng, chronicle, kingdoms, settlements, dynasties,
                            cells, next_dynasty_id, next_person_id)
        # Assassinations during contested succession (any dynasty).
        for dyn in list(dynasties.values()):
            if dyn.extinct_year == -1:
                _try_assassination(dyn, year, rng, chronicle)

        if year_callback is not None:
            year_callback(year, kingdoms, settlements, dynasties, chronicle)

    return chronicle
