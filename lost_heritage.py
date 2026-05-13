"""Lost Heritage — unique cultural artifacts generated from world history.

Each world generates a set of named LostArtifacts tied to its kingdoms and
dynasties. They appear as rare loot in ruins and underground chests, and are
tracked in the player's Heritage collection.
"""

import hashlib
import random
from dataclasses import dataclass, asdict


# ---------------------------------------------------------------------------
# Data class
# ---------------------------------------------------------------------------

@dataclass
class LostArtifact:
    uid: str
    category: str               # artwork / codex / relic / instrument / fragment
    #                             blueprint / idol / map / vessel
    name: str
    material: str
    condition: str              # pristine / intact / damaged / fragmentary / restored
    origin_kingdom: str
    origin_dynasty: str
    year_created: int
    year_lost: int              # -1 = unknown
    cause_of_loss: str
    description: str
    legend: str                 # non-empty only for legendary artifacts
    rarity: str                 # rare / epic / legendary
    value: int
    item_id: str
    location_hint: str

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> "LostArtifact":
        return LostArtifact(
            uid=d["uid"],
            category=d["category"],
            name=d["name"],
            material=d["material"],
            condition=d.get("condition", "intact"),
            origin_kingdom=d["origin_kingdom"],
            origin_dynasty=d["origin_dynasty"],
            year_created=d["year_created"],
            year_lost=d["year_lost"],
            cause_of_loss=d["cause_of_loss"],
            description=d["description"],
            legend=d.get("legend", ""),
            rarity=d["rarity"],
            value=d["value"],
            item_id=d["item_id"],
            location_hint=d["location_hint"],
        )


# ---------------------------------------------------------------------------
# Rarity
# ---------------------------------------------------------------------------

RARITY_COLORS = {
    "rare":      (120, 180, 255),
    "epic":      (180, 100, 255),
    "legendary": (255, 200,  60),
}

RARITY_VALUES = {
    "rare":      (180, 320),
    "epic":      (400, 650),
    "legendary": (800, 1400),
}


# ---------------------------------------------------------------------------
# Condition
# ---------------------------------------------------------------------------

_CONDITIONS = ["pristine", "intact", "intact", "damaged", "fragmentary", "restored"]

_CONDITION_VALUE_MOD = {
    "pristine":    1.45,
    "intact":      1.0,
    "damaged":     0.65,
    "fragmentary": 0.45,
    "restored":    0.80,
}

_CONDITION_SUFFIX = {
    "pristine":    "Remarkably well-preserved, it shows no signs of age.",
    "intact":      "It has survived the centuries largely intact.",
    "damaged":     "Though bearing clear signs of damage, it remains identifiable.",
    "fragmentary": "Only fragments remain, but enough to recognize its original form.",
    "restored":    "Later craftsmen worked to restore it, with mixed results.",
}


# ---------------------------------------------------------------------------
# Name patterns  (weighted via _NAME_PATTERN_WEIGHTS)
# ---------------------------------------------------------------------------

_NAME_PATTERNS = [
    lambda adj, noun, dyn, kin: f"The {adj} {noun} of {dyn}",
    lambda adj, noun, dyn, kin: f"The {noun} of {dyn}",
    lambda adj, noun, dyn, kin: f"{dyn}'s {adj} {noun}",
    lambda adj, noun, dyn, kin: f"The {adj} {noun} of {kin}",
    lambda adj, noun, dyn, kin: f"The {adj} {noun}, Pride of {dyn}",
    lambda adj, noun, dyn, kin: f"The Last {noun} of {dyn}",
    lambda adj, noun, dyn, kin: f"The {noun} of {kin}'s {adj} Age",
    lambda adj, noun, dyn, kin: f"The {adj} {noun}, Treasure of {kin}",
    lambda adj, noun, dyn, kin: f"The {noun} of the {adj} {kin}",
    lambda adj, noun, dyn, kin: f"{kin}'s {noun}",
    lambda adj, noun, dyn, kin: f"The {adj} {noun} from {kin}",
    lambda adj, noun, dyn, kin: f"The {noun} of {dyn}'s Founding",
    lambda adj, noun, dyn, kin: f"The {noun} of {kin}, {adj} and Forgotten",
    lambda adj, noun, dyn, kin: f"A {adj} {noun} of {dyn}",
]
_NAME_PATTERN_WEIGHTS = [5, 1, 2, 2, 2, 1, 1, 2, 2, 1, 1, 1, 1, 1]


# ---------------------------------------------------------------------------
# Word pools
# ---------------------------------------------------------------------------

_ADJECTIVES = [
    "Obsidian", "Golden", "Sunken", "Forgotten", "Blazing", "Crimson",
    "Ivory", "Azure", "Verdant", "Shattered", "Veiled", "Hallowed",
    "Rising", "Dying", "Gilded", "Iron", "Silver", "Haunted", "Ancient",
    "Eternal", "Radiant", "Crumbling", "Bloodstained", "Moonlit", "Ashen",
    "Sapphire", "Jade", "Amber", "Brazen", "Hollow", "Buried",
    "Weathered", "Carved", "Painted", "Sealed", "Crowned",
    "Fractured", "Sundered", "Pale", "Dark", "Bright", "Worn",
    "Twisted", "Bound", "Traced", "Lost", "Broken", "Named",
    "Holy", "Cursed", "Blessed", "Prized", "Forged", "Cast",
    "Gleaming", "Tarnished", "Ornate", "Heavy", "Delicate",
    "Nameless", "Inscribed", "Inlaid", "Chased", "Beaten",
    "Winged", "Thornbound", "Storied", "Twice-Lost",
]

_NOUNS = {
    "artwork": [
        "Portrait", "Triptych", "Mosaic", "Fresco", "Medallion",
        "Relief", "Mural", "Icon", "Bust", "Diptych",
        "Votive Panel", "Allegory", "Devotional", "Altarpiece", "Rendering",
        "Effigy", "Tableau", "Miniature", "Vignette", "Cartouche",
    ],
    "codex": [
        "Codex", "Compendium", "Chronicle", "Annals", "Atlas",
        "Grimoire", "Treatise", "Almanac", "Bestiary", "Lexicon",
        "Manifesto", "Tome", "Scroll", "Reckoning", "Survey",
        "Registry", "Discourse", "Commentary", "Psalter", "Epitome",
    ],
    "relic": [
        "Scepter", "Seal", "Signet", "Standard", "Helm",
        "Crown", "Chalice", "Blade", "Horn", "Reliquary",
        "Medallion", "Ring", "Banner", "Phylactery", "Pauldron",
        "Gorget", "Gauntlet", "Pendant", "Brooch", "Torque",
    ],
    "instrument": [
        "Lyre", "Harp", "Drum", "Horn", "Lute",
        "Rebec", "Dulcimer", "Zither", "Psaltery", "Flute",
        "Cittern", "Ocarina", "Sistrum", "Carnyx", "Gong",
        "Aulos", "Theorbo", "Rebab", "Kanun", "Salpinx",
    ],
    "fragment": [
        "Lintel", "Stele", "Keystone", "Capital", "Frieze",
        "Plaque", "Foundation Stone", "Cornerstone", "Tablet", "Inscription",
        "Tympanum", "Votive Stone", "Cartouche", "Column Drum", "Architrave",
        "Pediment", "Metope", "Spandrel", "Cornice", "Socle",
    ],
    "blueprint": [
        "Blueprint", "Survey", "Schema", "Diagram", "Plan",
        "Manual", "Treatise", "Pattern", "Schematic", "Record",
        "Register", "Inventory", "Ledger", "Elevation", "Cross-Section",
        "Specification", "Notation", "Draft", "Portfolio", "Projection",
    ],
    "idol": [
        "Idol", "Figurine", "Totem", "Effigy", "Votive",
        "Image", "Statuette", "Icon", "Graven Image", "God-Form",
        "Spirit-Figure", "Cult Object", "Devotional", "Face-Mask", "Warding Figure",
        "Temple Piece", "Offering Figure", "Talisman", "Fetish", "Apotropaic Figure",
    ],
    "map": [
        "Chart", "Survey", "Projection", "Rendering", "Itinerary",
        "Route Map", "Coastal Map", "Terrain Map", "Star Chart", "Portolan",
        "Schematic", "Wayfinder", "Bearing Chart", "Tracing", "Prospect",
        "Delineation", "Pictograph", "Trade Map", "Siege Map", "Survey Tablet",
    ],
    "vessel": [
        "Urn", "Amphora", "Krater", "Rhyton", "Pyxis",
        "Lekythos", "Oenochoe", "Hydria", "Pithos", "Larnax",
        "Canopic Jar", "Reliquary Chest", "Ceremonial Bowl", "Offering Cup", "Libation Vessel",
        "Ritual Flask", "Funerary Urn", "Painted Jar", "Footed Cup", "Beaker",
    ],
}

_MATERIALS = {
    "artwork": [
        "marble", "limestone", "oak panel", "ivory", "gilded wood",
        "bronze", "hammered gold", "silver leaf", "fired enamel", "polished obsidian",
        "painted ceramic", "hammered copper", "carved alabaster",
        "burnished terracotta", "lacquered cedar",
    ],
    "codex": [
        "vellum", "papyrus", "silk", "linen", "tanned hide",
        "birch bark", "hammered copper sheets", "wax tablets", "lambskin", "pressed reed",
        "palm leaf", "scraped parchment", "dyed cloth",
        "burnished tin tablets", "rolled bark",
    ],
    "relic": [
        "bronze", "iron", "gold", "silver", "obsidian",
        "jade", "ivory", "carved bone", "rock crystal", "electrum",
        "gilded iron", "blackened steel", "carved antler",
        "beaten copper", "nielloed silver",
    ],
    "instrument": [
        "rosewood", "ebony", "cedar", "birchwood", "bone",
        "ivory", "gilded bronze", "oak", "willow", "lacquered pine",
        "stretched hide", "hammered bronze", "inlaid sandalwood",
        "carved yew", "polished horn",
    ],
    "fragment": [
        "marble", "sandstone", "granite", "limestone", "basalt",
        "terracotta", "carved wood", "fired clay", "alabaster", "polished slate",
        "soapstone", "tuff", "travertine",
        "flint-dressed stone", "carved serpentine",
    ],
    "blueprint": [
        "vellum", "papyrus", "linen", "tanned hide", "silk",
        "bark paper", "hammered tin sheet", "pressed clay", "treated wood panel", "woven reed mat",
        "scraped bone", "dyed cotton", "incised stone slab",
        "oiled parchment", "compressed leaves",
    ],
    "idol": [
        "fired clay", "carved limestone", "bronze", "ivory", "obsidian",
        "polished bone", "gilded wood", "hammered copper", "alabaster", "painted terracotta",
        "carved antler", "rock crystal", "electrum", "blackwood", "jade",
    ],
    "map": [
        "vellum", "papyrus", "tanned hide", "linen", "silk",
        "birch bark", "hammered bronze sheet", "pressed clay tablet", "treated wood panel", "scraped parchment",
        "oiled cloth", "dyed reed mat", "incised stone", "woven silk", "palm leaf",
    ],
    "vessel": [
        "terracotta", "bronze", "silver", "gold", "alabaster",
        "painted ceramic", "obsidian", "hammered copper", "rock crystal", "faience",
        "carved soapstone", "gilded clay", "fired stoneware",
        "polished basalt", "enamelled bronze",
    ],
}

_CATEGORY_ITEM_IDS = {
    "artwork":    "lost_artwork",
    "codex":      "lost_codex",
    "relic":      "dynasty_relic",
    "instrument": "cultural_instrument",
    "fragment":   "sacred_fragment",
    "blueprint":  "architectural_plan",
    "idol":       "ancient_idol",
    "map":        "ancient_map",
    "vessel":     "antique_vessel",
}

_AGENDA_CATEGORIES = {
    "martial":    ["relic", "relic", "relic", "fragment", "blueprint", "idol"],
    "mercantile": ["codex", "codex", "codex", "blueprint", "artwork", "map", "vessel"],
    "scholarly":  ["codex", "codex", "codex", "blueprint", "instrument", "map"],
    "pious":      ["fragment", "fragment", "relic", "artwork", "instrument", "idol", "vessel"],
    "builder":    ["blueprint", "blueprint", "fragment", "fragment", "codex", "map"],
    "hedonist":   ["artwork", "artwork", "instrument", "instrument", "relic", "vessel"],
}

# Biome-group preferred materials (50% chance to apply when category matches)
_BIOME_MATERIAL_BIAS = {
    "forest":   {"relic": "carved antler", "fragment": "carved wood", "idol": "carved antler"},
    "desert":   {"fragment": "sandstone", "relic": "alabaster", "vessel": "alabaster", "idol": "carved limestone"},
    "tundra":   {"relic": "carved bone", "instrument": "polished horn", "idol": "carved antler"},
    "tropical": {"codex": "palm leaf", "blueprint": "palm leaf", "vessel": "faience"},
    "volcanic": {"relic": "obsidian", "fragment": "basalt", "artwork": "polished obsidian", "idol": "obsidian"},
    "coastal":  {"vessel": "painted ceramic", "map": "hammered bronze sheet", "codex": "pressed reed"},
}


# ---------------------------------------------------------------------------
# Description assembly
# ---------------------------------------------------------------------------

_CREATION_PHRASES = [
    "Commissioned during the height of {kingdom}'s power,",
    "Crafted in the capital of {kingdom} by an unknown artisan,",
    "Forged under the patronage of {dynasty},",
    "Created as a gift between rival courts,",
    "Produced in the royal workshops of {kingdom},",
    "Said to have been made for the founders of {dynasty},",
    "Presented at the treaty signing between {kingdom} and its neighbors,",
    "Built to commemorate a great victory over {kingdom}'s enemies,",
    "Assembled across three generations of {dynasty}'s craftsmen,",
    "Recorded as a treasure of {kingdom} in its own annals,",
    "Made for the coronation of a {kingdom} ruler,",
    "Crafted as a devotional offering by artisans of {dynasty},",
    "Produced when {kingdom} was at the height of its craft traditions,",
]

_CREATION_PERSON_PHRASES = [
    "Made for {person} of {dynasty},",
    "Commissioned personally by {person}, who ruled {kingdom},",
    "Said to have been a prized possession of {person},",
    "Crafted as a gift for {person}, founder of {dynasty},",
    "Created at the command of {person} and kept in the {kingdom} treasury,",
    "Recorded in the chronicles as belonging to {person} of {kingdom},",
]

_CREATION_EVENT_PHRASES = [
    "In year {year}, {event_brief}. Among the things created in this period was",
    "Following the events of year {year} — when {event_brief} —",
    "Made to commemorate the events of year {year}, when {event_brief},",
]

_MIDDLES = [
    "this {material} {noun} was considered one of the era's great treasures.",
    "this {material} {noun} was kept in the {dynasty} treasury for generations.",
    "this {material} {noun} was regarded as a symbol of {dynasty}'s authority.",
    "this {material} {noun} was said to be without equal in the known world.",
    "this {material} {noun} was among the finest works produced by that civilization.",
    "this {material} {noun} passed through many hands before it was lost.",
    "this {material} {noun} was displayed in the great hall of {kingdom}'s capital.",
]

_LOSS_PHRASES = {
    "sacked":     "It was lost when the city was sacked and its treasures scattered.",
    "plague":     "Its whereabouts became unknown after the plague emptied the city.",
    "earthquake": "The earthquake that destroyed the settlement buried it beneath rubble.",
    "decline":    "As the settlement declined, it passed from memory along with its owners.",
    "war":        "It disappeared during the wars that tore the region apart.",
    "fire":       "The fire that consumed the settlement likely scattered or destroyed it.",
    "flood":      "The floods that struck the settlement may have swept it away.",
    "":           "Its fate is unrecorded.",
}

_TAIL_PHRASES = [
    "Scholars have long debated where it came to rest.",
    "Some say it was taken by merchants traveling east; others believe it was buried with the ruling family.",
    "No complete record of its final resting place survives.",
    "Rumors persist that it was hidden before the fall, waiting to be rediscovered.",
    "The {dynasty} seal on its surface is the only proof of its origin.",
    "If recovered, it would be considered one of the finest surviving pieces from that era.",
    "Its recovery would be a significant historical event.",
    "Fragments of a song survive which describe it, though the melody has been forgotten.",
    "No inventory from the period lists its whereabouts after the fall.",
    "Some accounts mention it passing through a trader's hands, though the trail ends there.",
    "It is mentioned only once in the surviving records, and the entry is incomplete.",
    "Later chroniclers noted its absence without explanation.",
]

_LEGENDARY_LEGENDS = [
    "It was said to bring victory to any army that marched beneath its symbol.",
    "Accounts claim it was used in the founding rites of the dynasty itself.",
    "Those who carried it were said to speak with uncanny authority over others.",
    "It was believed to protect its city from plague and famine while kept intact.",
    "According to the chronicles, those who consulted it claimed it was never wrong.",
    "The dynasty's enemies feared its presence above all other treasures of the realm.",
    "It is said that the dynasty's long rule was tied to its continued safekeeping.",
    "Legends claim its sound could calm any crowd, or incite any army to fury.",
    "It was said to glow faintly in the presence of underground water or hidden passages.",
    "Those who studied it claimed it revealed routes no other map had ever shown.",
    "It is said that the dynasty's fall began the very night it was separated from them.",
    "Some claimed it was older than the kingdom itself — a relic of a forgotten age.",
    "The chronicle records that three wars were fought over possession of it.",
    "It is said that no ruler who kept it close ever died in battle.",
]

_LOCATION_HINTS = [
    "Somewhere beneath the ruins of the old capital",
    "Buried in the eastern settlements",
    "Lost in the western reaches of the former kingdom",
    "Hidden deep underground, near an old settlement",
    "Scattered with other treasures across a forgotten ruin",
    "Entombed with its last owner in a collapsed building",
    "Dispersed when the capital fell — pieces in several ruins",
    "Rumored to be beneath a river-crossing settlement",
    "Said to be sealed in a vault beneath the old treasury",
    "Possibly carried east by fleeing refugees from the fall",
    "Believed to be in the deepest level of an old ruin",
    "Last recorded in the capital; its movements after that are unknown",
    "Some say it was buried in a secret chamber during the siege",
    "Accounts place it near the kingdom's borders at the time of the fall",
]


def _notable_person_name(dynasty) -> str:
    if dynasty is None:
        return ""
    for pid in (dynasty.founder_id, dynasty.head_id):
        person = dynasty.members.get(pid)
        if person is not None:
            if person.epithet:
                return f"{person.name} the {person.epithet}"
            return person.name
    return ""


def _build_description(rng, material, noun, kingdom_name, dynasty_name,
                        cause_of_ruin, notable_person, key_event, condition) -> str:
    use_person = bool(notable_person) and rng.random() < 0.40
    use_event  = bool(key_event)      and rng.random() < 0.35

    if use_person:
        opening = rng.choice(_CREATION_PERSON_PHRASES).format(
            person=notable_person, dynasty=dynasty_name, kingdom=kingdom_name)
    elif use_event:
        brief    = key_event.text.rstrip(".")
        opening  = rng.choice(_CREATION_EVENT_PHRASES).format(
            year=key_event.year, event_brief=brief.lower())
    else:
        opening = rng.choice(_CREATION_PHRASES).format(
            kingdom=kingdom_name, dynasty=dynasty_name)

    middle = rng.choice(_MIDDLES).format(
        material=material, noun=noun.lower(),
        dynasty=dynasty_name, kingdom=kingdom_name)
    loss   = _LOSS_PHRASES.get(cause_of_ruin, _LOSS_PHRASES[""])
    tail   = rng.choice(_TAIL_PHRASES).format(dynasty=dynasty_name)
    cond   = _CONDITION_SUFFIX[condition]

    return f"{opening} {middle} {loss} {tail} {cond}"


def _build_cause_of_loss(cause_of_ruin, settlement_name, kingdom_name) -> str:
    if cause_of_ruin == "sacked":
        return f"lost in the sacking of {settlement_name}"
    if cause_of_ruin == "plague":
        return f"abandoned during the plague that emptied {settlement_name}"
    if cause_of_ruin == "earthquake":
        return f"buried when {settlement_name} was destroyed by earthquake"
    if cause_of_ruin == "decline":
        return f"forgotten as {settlement_name} was abandoned"
    if cause_of_ruin == "war":
        return f"lost during the wars that destroyed {settlement_name}"
    if cause_of_ruin == "fire":
        return f"lost when fire consumed {settlement_name}"
    return f"lost with the fall of {kingdom_name}"


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------

class ArtifactGenerator:

    def generate_for_world(self, plan) -> list:
        """Return a list of LostArtifact dicts for all kingdoms in the plan."""
        artifacts = []
        counter   = 0

        for kingdom in plan.kingdoms.values():
            dynasty       = plan.dynasties.get(kingdom.dynasty_id)
            dynasty_name  = dynasty.house_name if dynasty else "an unknown house"
            notable_person = _notable_person_name(dynasty)

            ruins = [s for s in plan.settlements.values()
                     if s.original_kingdom_id == kingdom.kingdom_id
                     and s.state in ("ruin", "abandoned")]

            k_event_ids = set(kingdom.history_event_ids)
            k_events    = [e for e in plan.chronicle
                           if e.event_id in k_event_ids
                           and e.kind in ("war", "sack", "plague", "earthquake",
                                          "famine", "founding", "treaty", "fire", "flood")]

            rng  = random.Random((kingdom.kingdom_id * 9973 + plan.seed) & 0xFFFF_FFFF)
            n    = rng.randint(2, 3) if kingdom.fallen_year == -1 else rng.randint(3, 6)
            pool = _AGENDA_CATEGORIES.get(kingdom.agenda, _AGENDA_CATEGORIES["builder"])
            bias = _BIOME_MATERIAL_BIAS.get(kingdom.biome_group, {})

            for _ in range(n):
                category  = rng.choice(pool)
                noun      = rng.choice(_NOUNS[category])
                adj       = rng.choice(_ADJECTIVES)
                mat_pool  = _MATERIALS[category]

                biome_mat = bias.get(category)
                if biome_mat and rng.random() < 0.5 and biome_mat in mat_pool:
                    material = biome_mat
                else:
                    material = rng.choice(mat_pool)

                pattern_fn = rng.choices(_NAME_PATTERNS, weights=_NAME_PATTERN_WEIGHTS, k=1)[0]
                name       = pattern_fn(adj, noun, dynasty_name, kingdom.name)

                ruin           = rng.choice(ruins) if ruins else None
                cause_of_ruin  = ruin.cause_of_ruin if ruin else ""
                settlement_name = ruin.name if ruin else kingdom.name

                year_created = rng.randint(
                    kingdom.founded_year,
                    kingdom.fallen_year if kingdom.fallen_year != -1 else plan.history_years)
                year_lost = ruin.ruined_year if ruin and ruin.ruined_year > 0 else -1

                condition = rng.choice(_CONDITIONS)

                roll   = rng.random()
                rarity = "legendary" if roll < 0.12 else "epic" if roll < 0.45 else "rare"

                lo, hi    = RARITY_VALUES[rarity]
                base_val  = rng.randint(lo, hi)
                value     = int(base_val * _CONDITION_VALUE_MOD[condition])

                uid_src = f"{plan.seed}_{kingdom.kingdom_id}_{counter}_{name}"
                uid     = hashlib.md5(uid_src.encode()).hexdigest()[:12]
                counter += 1

                key_event     = rng.choice(k_events) if k_events else None
                cause_of_loss = _build_cause_of_loss(cause_of_ruin, settlement_name, kingdom.name)
                description   = _build_description(
                    rng, material, noun, kingdom.name, dynasty_name,
                    cause_of_ruin, notable_person, key_event, condition)
                legend        = rng.choice(_LEGENDARY_LEGENDS) if rarity == "legendary" else ""
                location_hint = rng.choice(_LOCATION_HINTS)

                artifact = LostArtifact(
                    uid=uid, category=category, name=name, material=material,
                    condition=condition, origin_kingdom=kingdom.name,
                    origin_dynasty=dynasty_name, year_created=year_created,
                    year_lost=year_lost, cause_of_loss=cause_of_loss,
                    description=description, legend=legend, rarity=rarity,
                    value=value, item_id=_CATEGORY_ITEM_IDS[category],
                    location_hint=location_hint,
                )
                artifacts.append(artifact.to_dict())

        return artifacts
