"""Dynasty mutation: age members, marry, birth heirs, succession on death."""

import random
from worldgen.plan import Person, Dynasty


_NAMES = ["Aerin","Brom","Cale","Doria","Edra","Falk","Garin","Hesta",
          "Iven","Jora","Kael","Lira","Marek","Nyssa","Olen","Pira",
          "Quill","Rhys","Sera","Toren","Ulva","Vesh","Wren","Yara",
          "Zane","Anora","Bren","Caen","Drya","Elar"]
_EPITHETS = ["the Just","the Fierce","the Wise","the Quiet","the Iron",
             "the Patient","the Bold","the Restless","the Bright","the Grim"]


def age_dynasty(dyn: Dynasty, year: int, rng: random.Random,
                next_person_id: list, on_event):
    """Run one tick: age, deaths, births, succession. Calls on_event(kind, person, ...)."""
    if dyn.extinct_year != -1:
        return
    head = dyn.members.get(dyn.head_id)
    if head is None:
        dyn.extinct_year = year
        return

    # Roll death for head if old enough.
    if head.died_year == -1:
        age = year - head.born_year
        death_chance = max(0.0, (age - 55) / 30.0) * 0.20
        if age > 80:
            death_chance = 0.5
        if rng.random() < death_chance:
            head.died_year = year
            on_event("death", head)
            _try_succession(dyn, year, rng, on_event)

    # Birth roll: head + spouse may produce an heir.
    if head.died_year == -1 and head.spouse_id != -1:
        if rng.random() < 0.06:
            child = Person(
                person_id=next_person_id[0],
                dynasty_id=dyn.dynasty_id,
                name=rng.choice(_NAMES),
                born_year=year,
                role="scion",
                parent_ids=(head.person_id, head.spouse_id),
            )
            next_person_id[0] += 1
            dyn.members[child.person_id] = child
            on_event("birth", child)

    # Pair up unmarried adults (head only, for cheap sim).
    if head.died_year == -1 and head.spouse_id == -1:
        if year - head.born_year > 18 and rng.random() < 0.25:
            spouse = Person(
                person_id=next_person_id[0],
                dynasty_id=dyn.dynasty_id,
                name=rng.choice(_NAMES),
                born_year=year - rng.randint(18, 30),
                role="spouse",
            )
            next_person_id[0] += 1
            spouse.spouse_id = head.person_id
            head.spouse_id = spouse.person_id
            dyn.members[spouse.person_id] = spouse
            on_event("marriage", head, spouse=spouse)


def _try_succession(dyn: Dynasty, year: int, rng: random.Random, on_event):
    living_kids = [p for p in dyn.members.values()
                   if p.died_year == -1 and p.role in ("scion", "heir")
                   and year - p.born_year >= 14]
    if not living_kids:
        # Try any living member.
        living = [p for p in dyn.members.values() if p.died_year == -1]
        if not living:
            dyn.extinct_year = year
            on_event("extinction", None)
            return
        chosen = rng.choice(living)
    else:
        chosen = max(living_kids, key=lambda p: -p.born_year)  # eldest
    if not chosen.epithet:
        chosen.epithet = rng.choice(_EPITHETS)
    chosen.role = "head"
    dyn.head_id = chosen.person_id
    if len(living_kids) > 1:
        on_event("succession_crisis", chosen)
    else:
        on_event("succession", chosen)
