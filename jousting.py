"""Jousting bout state machine — live mounted joust against a knight.

Phases: lobby -> charge -> close -> impact -> result -> rest -> next pass.

A JoustBout owns its own state. The UI module (UI/jousting.py) draws the
phase-appropriate overlay and forwards input via handle_input(). main.py /
UI/handlers.py is responsible for opening a JoustBout when the player talks
to a tournament_grounds marshal.

Scoring (per pass):
  miss          → 0 pts
  shield_hit    → 1 pt
  clean_strike  → 3 pts
  unhorse       → 5 pts and the bout ends immediately

A tournament is a single-elimination bracket of 8 entrants. Three passes per
bout (or first unhorse).
"""

import random
from dataclasses import dataclass, field
from typing import Optional, List

import knightly_orders


# Phase constants
LOBBY   = "lobby"
CHARGE  = "charge"
CLOSE   = "close"
IMPACT  = "impact"
RESULT  = "result"
REST    = "rest"
DONE    = "done"

# Tuning
PASSES_PER_BOUT       = 3
CHARGE_DURATION       = 1.6   # seconds
CLOSE_DURATION        = 1.0
IMPACT_DURATION       = 0.6
REST_DURATION         = 1.4
RESULT_HOLD           = 2.4
BRACKET_SIZE          = 8

# Aim choices
AIM_HIGH = "high"
AIM_MID  = "mid"
AIM_LOW  = "low"
AIMS     = [AIM_HIGH, AIM_MID, AIM_LOW]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _equipped_lance(player):
    """Return the player's equipped Weapon if it is a lance, else None."""
    if not getattr(player, "equipped_weapon_uid", None):
        return None
    for w in player.crafted_weapons:
        if w.uid == player.equipped_weapon_uid and w.weapon_type == "lance":
            return w
    return None


def _lance_quality(player) -> float:
    lance = _equipped_lance(player)
    if not lance:
        return 0.4
    from weapons import effective_quality
    return effective_quality(lance)


def _horse_speed(player) -> float:
    h = getattr(player, "mounted_horse", None)
    if h is None:
        return 0.6
    return h.traits.get("speed_rating", 1.0) * h.traits.get("stamina_max", 1.0)


def _player_armor_def(player) -> int:
    return player.get_armor_defense() if hasattr(player, "get_armor_defense") else 0


def _barding_bonus(player) -> int:
    h = getattr(player, "mounted_horse", None)
    if h is None:
        return 0
    from horses import barding_defense
    return barding_defense(h)


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

@dataclass
class JoustOpponent:
    knight_id: int
    name:      str
    order_id:  int
    skill:     float
    score:     int = 0
    unhorsed:  bool = False


@dataclass
class JoustBout:
    opponent:        JoustOpponent
    pass_index:      int = 0
    player_score:    int = 0
    player_aim:      Optional[str] = None
    opponent_aim:    Optional[str] = None
    player_charge:   float = 0.0   # 0.0-1.0, how well player held the charge key
    phase:           str = LOBBY
    phase_timer:     float = 0.0
    last_outcome:    str = ""       # human-readable result of latest pass
    last_pts_player: int = 0
    last_pts_opp:    int = 0


@dataclass
class Tournament:
    bracket:        List[JoustOpponent]
    round_index:    int = 0
    current_bout:   Optional[JoustBout] = None
    player_active:  bool = True
    final_place:    int = 0   # 1 = champion, 2 = runner-up, 4 = semi, 8 = first round
    won_pennant_of: Optional[int] = None   # order_id whose pennant was awarded


# ---------------------------------------------------------------------------
# Bracket construction
# ---------------------------------------------------------------------------

def build_tournament(world, region_id: int, rng: random.Random) -> Tournament:
    """Pick 7 local knights weighted by their order prestige + skill."""
    candidates = []
    for o in knightly_orders.orders_for_region(region_id):
        for kid in o.member_ids:
            k = knightly_orders.knight(kid)
            if k is None:
                continue
            weight = max(0.1, o.prestige / 50.0 + k.skill)
            candidates.append((weight, k))
    # Fall back to every knight in the world if the region is empty
    if len(candidates) < 7:
        for k in knightly_orders.KNIGHTS.values():
            candidates.append((max(0.5, k.skill), k))
    rng.shuffle(candidates)
    picked = []
    seen = set()
    for w, k in sorted(candidates, key=lambda c: -c[0]):
        if k.knight_id in seen:
            continue
        seen.add(k.knight_id)
        picked.append(JoustOpponent(
            knight_id = k.knight_id,
            name      = k.name,
            order_id  = k.order_id,
            skill     = k.skill,
        ))
        if len(picked) >= BRACKET_SIZE - 1:
            break
    return Tournament(bracket=picked)


def next_opponent(t: Tournament) -> Optional[JoustOpponent]:
    """Pop one opponent per round; returns None when the bracket is exhausted."""
    if not t.player_active:
        return None
    if t.round_index >= len(t.bracket):
        return None
    opp = t.bracket[t.round_index]
    t.round_index += 1
    return opp


# ---------------------------------------------------------------------------
# Bout flow — call these from the UI
# ---------------------------------------------------------------------------

def start_bout(t: Tournament, opp: JoustOpponent) -> JoustBout:
    bout = JoustBout(opponent=opp)
    t.current_bout = bout
    return bout


def begin_pass(bout: JoustBout) -> None:
    bout.pass_index += 1
    bout.player_aim   = None
    bout.opponent_aim = None
    bout.player_charge = 0.0
    bout.phase       = CHARGE
    bout.phase_timer = CHARGE_DURATION


def tick(bout: JoustBout, dt: float, player) -> None:
    """Advance phase timers and run the AI side. Outcome is resolved in IMPACT."""
    if bout.phase == LOBBY or bout.phase == DONE:
        return
    bout.phase_timer -= dt
    if bout.phase_timer > 0:
        return
    # Phase rolled over
    if bout.phase == CHARGE:
        bout.phase = CLOSE
        bout.phase_timer = CLOSE_DURATION
        # AI picks aim — base skill weight blended with the opponent's tradition.
        base = [1, 2, 1] if bout.opponent.skill < 1.0 else [2, 2, 2]
        bias = knightly_orders.aim_bias_for_opponent(bout.opponent.knight_id)
        weights = [b + w for b, w in zip(base, bias)]
        bout.opponent_aim = random.choices(AIMS, weights=weights)[0]
    elif bout.phase == CLOSE:
        bout.phase = IMPACT
        bout.phase_timer = IMPACT_DURATION
        _resolve_impact(bout, player)
    elif bout.phase == IMPACT:
        bout.phase = RESULT
        bout.phase_timer = RESULT_HOLD
    elif bout.phase == RESULT:
        if (bout.pass_index >= PASSES_PER_BOUT
                or bout.opponent.unhorsed
                or getattr(player, "_jousting_unhorsed", False)):
            bout.phase = DONE
        else:
            bout.phase = REST
            bout.phase_timer = REST_DURATION
    elif bout.phase == REST:
        begin_pass(bout)


def handle_charge_input(bout: JoustBout, keys, pygame_mod) -> None:
    """Call from UI input loop while CHARGE phase is active.

    Player holds SPACE to keep speed up; we average the hold to a 0-1 score.
    """
    if bout.phase != CHARGE:
        return
    held = keys[pygame_mod.K_SPACE]
    # Linear blend toward 1.0 if held, toward 0.0 otherwise; tuned for the 1.6s window
    target = 1.0 if held else 0.0
    bout.player_charge = bout.player_charge * 0.85 + target * 0.15


def set_aim(bout: JoustBout, aim: str) -> None:
    if bout.phase == CLOSE and aim in AIMS:
        bout.player_aim = aim


# ---------------------------------------------------------------------------
# Impact resolution
# ---------------------------------------------------------------------------

def _resolve_impact(bout: JoustBout, player) -> None:
    if bout.player_aim is None:
        bout.player_aim = AIM_MID   # default if player didn't pick

    # Player offense / defense
    p_lance   = _lance_quality(player)
    p_speed   = _horse_speed(player)
    p_charge  = bout.player_charge
    p_defense = _player_armor_def(player) + _barding_bonus(player)

    # Opponent stats — synthetic from skill
    o_skill   = bout.opponent.skill
    o_speed   = 0.7 + o_skill * 0.5
    o_defense = 20 + int(o_skill * 12)
    o_aim     = bout.opponent_aim or AIM_MID

    # Player → opponent
    player_offense = p_lance * (0.6 + p_charge * 0.4) * (0.7 + p_speed * 0.4)
    aim_match_player = (bout.player_aim != o_aim)   # mismatched aim = harder dodge for opp
    p_outcome = _pass_outcome(player_offense, o_defense, aim_match_player)
    if p_outcome == "unhorse":
        bout.opponent.unhorsed = True
        bout.player_score += 5
        bout.last_pts_player = 5
        bout.last_outcome   = f"UNHORSED! You strike {bout.opponent.name} from the saddle."
        _consume_lance_if_shatter(player)
        return
    pts_p = {"miss": 0, "shield": 1, "clean": 3}[p_outcome]
    bout.player_score += pts_p
    bout.last_pts_player = pts_p

    # Opponent → player
    opp_offense = (0.5 + o_skill * 0.7) * (0.6 + o_speed * 0.4)
    aim_match_opp = (o_aim != bout.player_aim)
    o_outcome = _pass_outcome(opp_offense, p_defense, aim_match_opp)
    if o_outcome == "unhorse":
        setattr(player, "_jousting_unhorsed", True)
        bout.opponent.score += 5
        bout.last_pts_opp = 5
        bout.last_outcome = f"You are unhorsed by {bout.opponent.name}."
        _consume_lance_if_shatter(player)
        return
    pts_o = {"miss": 0, "shield": 1, "clean": 3}[o_outcome]
    bout.opponent.score += pts_o
    bout.last_pts_opp = pts_o
    bout.last_outcome = _describe_pass(p_outcome, o_outcome, bout.opponent.name)
    _consume_lance_if_shatter(player)


def _pass_outcome(offense: float, defense: int, aim_match: bool) -> str:
    """offense ~ 0.3 - 1.8; defense ~ 10-50. Returns miss/shield/clean/unhorse."""
    score = offense * 60 - defense * 0.4
    if aim_match:
        score += 8
    roll = random.uniform(-12, 12)
    final = score + roll
    if final >= 55:
        return "unhorse"
    if final >= 35:
        return "clean"
    if final >= 18:
        return "shield"
    return "miss"


def _describe_pass(player_out: str, opp_out: str, opp_name: str) -> str:
    bits = []
    if player_out == "clean":
        bits.append(f"Clean strike on {opp_name}.")
    elif player_out == "shield":
        bits.append("Glancing blow off the shield.")
    else:
        bits.append("You miss the mark.")
    if opp_out == "clean":
        bits.append("They land a clean strike on you.")
    elif opp_out == "shield":
        bits.append("Their lance taps your shield.")
    else:
        bits.append("They miss.")
    return " ".join(bits)


def _consume_lance_if_shatter(player) -> None:
    """Tournament lance heads shatter cleanly on every impact pass.

    We don't destroy the crafted lance (the shaft is reusable); we just consume
    one tournament_lance_head from inventory if the player carries any. Other
    lance materials don't shatter.
    """
    inv = getattr(player, "inventory", {})
    if inv.get("tournament_lance_head", 0) > 0:
        inv["tournament_lance_head"] -= 1
        if inv["tournament_lance_head"] <= 0:
            del inv["tournament_lance_head"]


# ---------------------------------------------------------------------------
# Round resolution + tournament rewards
# ---------------------------------------------------------------------------

def resolve_bout(bout: JoustBout, t: Tournament, player) -> bool:
    """Mark winner of the current bout. Returns True if the player advanced."""
    if getattr(player, "_jousting_unhorsed", False):
        player._jousting_unhorsed = False
        t.player_active = False
        return False
    if bout.opponent.unhorsed or bout.player_score > bout.opponent.score:
        knightly_orders.record_tournament_win(bout.opponent.knight_id, prestige_delta=0)
        # Rivalry: if the opponent's order is a sworn enemy of the player's,
        # add a prestige bonus and tag the bout outcome.
        sworn = getattr(player, "order_id", 0)
        opp_oid = bout.opponent.order_id
        if sworn and knightly_orders.is_rival_pair(sworn, opp_oid):
            player.order_prestige = getattr(player, "order_prestige", 0) + 5
            bout.last_outcome += " (rival order felled — +5 prestige)"
        return True
    if bout.player_score == bout.opponent.score:
        # tiebreaker by lance quality
        if _lance_quality(player) >= bout.opponent.skill * 0.7:
            return True
        t.player_active = False
        return False
    t.player_active = False
    return False


def award_rewards(t: Tournament, player) -> dict:
    """Compute final placement, gold, and trophy. Mutates player inventory + money.

    Returns a summary dict the UI can show.
    """
    rounds_won = max(0, t.round_index - (0 if t.player_active else 1))
    place = max(1, BRACKET_SIZE >> max(0, rounds_won)) if rounds_won < 3 else 1
    if t.player_active and rounds_won >= 3:
        place = 1

    reward_table = {1: 600, 2: 300, 4: 150, 8: 50}
    gold = reward_table.get(place, 25)
    player.money = getattr(player, "money", 0) + gold

    summary = {"place": place, "gold": gold, "pennant_order": None,
               "loot_drops": []}

    # Tradition-flavored loot rolls — keyed by the order the player just bested.
    # For non-champion placements, the "current bout" is the bout where the
    # player was knocked out, so the loot reads as a souvenir from the foe
    # that put them out of the lists.
    if t.current_bout is not None:
        bested_order_id = t.current_bout.opponent.order_id
        loot = knightly_orders.tournament_drops(bested_order_id, place, random)
        if loot:
            inv = getattr(player, "inventory", {})
            for item_id, count in loot:
                inv[item_id] = inv.get(item_id, 0) + count
            player.inventory = inv
            summary["loot_drops"] = loot

    # Champion gets a pennant of the order they bested in the final
    if place == 1 and t.current_bout is not None:
        order_id = t.current_bout.opponent.order_id
        inv = getattr(player, "inventory", {})
        inv["tournament_pennant"] = inv.get("tournament_pennant", 0) + 1
        player.inventory = inv
        t.won_pennant_of = order_id
        summary["pennant_order"] = order_id
        # Mark the player as riding under this order's colors — any barding
        # with uses_heraldry=True will trim with the order's primary tincture.
        player.champion_order_id = order_id
        record = getattr(player, "tournament_record", {"wins": 0, "podium": 0, "entries": 0})
        record["wins"] += 1
        record["podium"] += 1
        record["entries"] += 1
        player.tournament_record = record
        player.order_joust_wins = getattr(player, "order_joust_wins", 0) + 1
        # If the player is sworn to the order whose pennant they just won,
        # the order's chapter house grants bonus prestige at the next visit.
        # Otherwise winning under any pennant still nudges order standing.
        sworn = getattr(player, "order_id", 0)
        if sworn:
            bonus = 5 if sworn == order_id else 2
            player.order_prestige = getattr(player, "order_prestige", 0) + bonus
            summary["order_prestige_gain"] = bonus
    elif place <= 4:
        record = getattr(player, "tournament_record", {"wins": 0, "podium": 0, "entries": 0})
        record["podium"] += 1
        record["entries"] += 1
        player.tournament_record = record
    else:
        record = getattr(player, "tournament_record", {"wins": 0, "podium": 0, "entries": 0})
        record["entries"] += 1
        player.tournament_record = record

    t.final_place = place
    return summary
