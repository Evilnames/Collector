"""Event templates and helpers for the history sim."""

import random


# Probability per kingdom per year for various roll-based events.
EVENT_RATES = {
    "war_declare":       0.025,   # martial bumps this 3x — kingdoms war more
    "found_settlement":  0.020,   # builder bumps this 3x
    "plague":            0.006,
    "famine":            0.008,
    "earthquake":        0.002,
    "abandon_decline":   0.012,   # cities decay/shrink under stress
    "city_shrink":       0.018,   # standalone shrink chance (per settlement/yr)

    # Political layer
    "alliance_form":     0.012,
    "alliance_break":    0.018,
    "revolt":            0.0018,  # per outlying settlement / yr (with distance scaling)
    "civil_war":         0.0035,  # per kingdom / yr (gated by tension)
    "kingdom_split":     0.45,    # P(split | civil war fires)
    "rebirth":           0.045,   # per orphan-cluster / yr — keep them coalescing
    "assassination":     0.003,
}


def text_shrink(settlement, new_tier):
    return f"{settlement.name} fell into decline; reduced to {new_tier}."

def text_kingdom_collapse(kingdom):
    return f"{kingdom.name} collapsed under the weight of its losses."

def text_alliance_form(a, b):
    return f"{a.name} and {b.name} sealed a formal alliance."

def text_alliance_break(a, b, reason: str):
    return f"The pact between {a.name} and {b.name} was broken — {reason}."

def text_revolt_independent(settlement, kingdom):
    return f"{settlement.name} cast off the banner of {kingdom.name} and declared itself free."

def text_revolt_defect(settlement, old_k, new_k):
    return f"{settlement.name} renounced {old_k.name} and swore fealty to {new_k.name}."

def text_civil_war(kingdom, faction_a, faction_b):
    return f"Civil war tore {kingdom.name} as {faction_a} rose against {faction_b}."

def text_kingdom_split(parent, breakaway, new_dynasty):
    return (f"{breakaway.name} broke away from {parent.name} under {new_dynasty}, "
            f"ending the war by drawing a new border.")

def text_kingdom_reborn(kingdom, settlement_count: int):
    return (f"{kingdom.name} was raised anew, uniting {settlement_count} "
            f"masterless settlements under one banner.")

def text_assassination(killer, victim, dynasty):
    return f"{killer.name} of {dynasty.house_name} struck down {victim.name} to seize the line."

def text_succession_war(winner_name, loser_name, dynasty):
    return (f"A war of succession in {dynasty.house_name} ended with {winner_name} "
            f"on the seat and {loser_name} cast out.")


def text_war_declare(attacker, defender):
    return f"{attacker.name} declared war on {defender.name}."

def text_sack(attacker, defender, settlement):
    return f"{attacker.name} sacked {settlement.name}; the city was ruined."

def text_annex(attacker, defender, settlement):
    return f"{attacker.name} annexed {settlement.name} from {defender.name}."

def text_defeat(victor, loser):
    return f"{loser.name} fell; territories absorbed by {victor.name}."

def text_found(kingdom, settlement, cell):
    return f"{kingdom.name} founded {settlement.name} in the {cell.biodome.replace('_',' ')}."

def text_grow(settlement, tier):
    return f"{settlement.name} grew into a {tier}."

def text_decline(settlement):
    return f"{settlement.name} declined and was abandoned."

def text_merge(big, small):
    return f"{big.name} absorbed {small.name}, forming a sprawling metropolis."

def text_plague(kingdom):
    return f"A plague swept {kingdom.name}, thinning its population."

def text_famine(kingdom):
    return f"Famine struck {kingdom.name}; many fled the land."

def text_earthquake(settlement):
    return f"An earthquake leveled {settlement.name}, leaving only ruins."

def text_extinction(dyn):
    return f"{dyn.house_name} ended; the line is broken."

def text_succession(person, dyn):
    return f"{person.name} of {dyn.house_name} took the seat."

def text_succession_crisis(person, dyn):
    return f"A bitter succession placed {person.name} at the head of {dyn.house_name}."

def text_birth(person, dyn):
    return f"{person.name} of {dyn.house_name} was born."

def text_marriage(a, b, dyn):
    return f"{a.name} of {dyn.house_name} wed {b.name}, sealing a bond."

def text_death(person, dyn):
    age = (person.died_year - person.born_year)
    e = f" {person.epithet}" if person.epithet else ""
    return f"{person.name}{e} of {dyn.house_name} died, aged {age}."
