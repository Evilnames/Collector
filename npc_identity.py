"""NPC identity: procedural names, lineage blurbs, and family tree assignment.

All outputs are fully deterministic from (npc_uid, world_seed) — nothing is saved;
everything is re-derived on every world load.
"""
import random

# ---------------------------------------------------------------------------
# Name pools
# ---------------------------------------------------------------------------

_FIRST_NAMES_M = [
    "Aldric", "Bram", "Calder", "Dorin", "Edwyn", "Ferris", "Galen", "Hadwin",
    "Idris", "Jorin", "Kelvin", "Leofric", "Maren", "Norbert", "Oswin", "Perin",
    "Quell", "Rowan", "Soren", "Tavish", "Ulric", "Valdis", "Wulfric", "Xander",
    "Yoren", "Zedric", "Asher", "Beren", "Caspian", "Davin", "Eldric", "Falk",
    "Godwin", "Harwin", "Ingvar", "Jovan", "Kester", "Lorcan", "Merrick", "Nils",
    "Orin", "Piers", "Ragnor", "Sigurd", "Theron", "Uther", "Varyn", "Wendell",
    "Ximun", "Yvain", "Zareth", "Aldous", "Brennan", "Corwin", "Destan", "Emric",
    "Fenwick", "Gralen", "Hector", "Ilvar", "Jasper",
]

_FIRST_NAMES_F = [
    "Aelind", "Bera", "Catryn", "Dagna", "Edith", "Freyja", "Gilda", "Halla",
    "Ingrid", "Jorah", "Kestrel", "Lyra", "Marta", "Nessa", "Orla", "Petra",
    "Quill", "Runa", "Signe", "Thyra", "Ulla", "Vesna", "Wren", "Xara",
    "Ysolde", "Zara", "Aelith", "Brynn", "Calla", "Dagny", "Elara", "Fiona",
    "Greta", "Helga", "Ilona", "Jenna", "Kira", "Lena", "Mora", "Nora",
    "Odra", "Petal", "Ragna", "Sigrid", "Tilda", "Ursa", "Vala", "Wilda",
    "Xenia", "Yrsa", "Zelda", "Adela", "Birna", "Cynara", "Dorrit", "Emlyn",
    "Freya", "Gudrun", "Hesta", "Isra", "Jorunn",
]

_FAMILY_NAMES = [
    "Voss", "Strand", "Keld", "Maren", "Wulfson", "Aldwick", "Branmore", "Cairn",
    "Duskwood", "Elmhurst", "Fenwick", "Greystone", "Holloway", "Ironwood", "Juniper",
    "Kettlebrook", "Linden", "Moorfield", "Northgate", "Oakhaven", "Pinehurst",
    "Quarry", "Riverdale", "Stonebeck", "Thorn", "Underhill", "Valewood",
    "Whitmore", "Yarrow", "Zephyr", "Ashburn", "Birchwood", "Copperfield",
    "Dunmore", "Esterbrook", "Foxley", "Goodhart", "Harwick", "Ironbell",
    "Jasperhill", "Kingsford", "Larkmoor", "Mistwood", "Nettlebrook", "Oldfield",
    "Peregrine", "Quickwater", "Redmoor", "Saltwick", "Timberwall", "Upton",
    "Verdane", "Westfall", "Crossfield", "Dawnholm", "Emberton", "Frostholm",
    "Goldvein", "Harthway", "Ivywood", "Jackdaw", "Knollwood", "Larchwood",
    "Millford", "Nighthollow", "Osgate", "Pinecroft", "Ravenswood", "Siltmore",
    "Thornbury", "Underwood", "Vynewood", "Willowdale", "Yewbarrow", "Marshfield",
    "Ferndale", "Gravel", "Hartwick", "Irongate", "Jormdale", "Kelwick",
]

# Lineage profession lines used in blurbs
_PROFESSION_LINES = [
    "armourers",
    "farmers",
    "merchants",
    "fisherfolk",
    "stonecutters",
    "innkeepers",
    "healers",
    "scholars",
    "hunters",
    "herbalists",
    "brewers",
    "weavers",
    "miners",
    "millers",
    "potters",
    "shepherds",
    "vintners",
    "scribes",
    "carpenters",
    "chandlers",
    "tanners",
    "coopers",
    "blacksmiths",
    "bakers",
    "dyers",
    "wheelwrights",
    "ropemakers",
    "glassblowers",
    "charcoal burners",
    "drovers",
    "ferrymen",
    "apothecaries",
    "saddlers",
    "tilemakers",
    "saltworkers",
    "woodcutters",
    "beekeepers",
    "fullers",
    "clockmakers",
    "tax collectors",
    "road wardens",
    "river pilots",
    "gravediggers",
    "midwives",
    "ink-makers",
    "tollkeepers",
    "rat-catchers",
    "night watchmen",
]

# Optional birthplace adjectives for variety
_BIRTHPLACE_QUALIFIERS = [
    "in the old quarter of",
    "on the outskirts of",
    "in the heart of",
    "near the markets of",
    "at the edge of",
    "in the lower district of",
    "in the hills above",
    "along the waterfront of",
    "in the tanner's row of",
    "beneath the walls of",
    "in the poorest ward of",
    "near the guild houses of",
    "on a small holding outside",
    "in the merchant quarter of",
    "within the abbey grounds of",
    "in a farmstead two leagues from",
    "in the milling district of",
    "along the northern road out of",
    "",  # no qualifier — just "in {town}"
    "",
    "",
    "",
]

# Personal character traits
_PERSONAL_TRAITS = [
    "quick to anger but quick to forgive",
    "soft-spoken but sharp-eyed",
    "fiercely loyal to those they trust",
    "prone to long spells of melancholy",
    "cheerful even in hard times",
    "slow to trust strangers",
    "generous almost to a fault",
    "quietly ambitious",
    "deeply superstitious about small things",
    "sharper-witted than they appear",
    "rarely seen to smile, though not unkind",
    "known to keep their own counsel",
    "fond of long solitary walks at dusk",
    "unusually good at reading people",
    "respected for never breaking a promise",
    "given to sudden acts of unexpected generosity",
    "distrustful of anyone who smiles too easily",
    "prone to speaking their mind before thinking",
    "often the first to help and the last to ask for it",
    "known to hold a grudge longer than most",
    "prone to long silences that others find unsettling",
    "genuinely kind in a way that surprises people who first meet them",
    "restless in a way that has never fully resolved into anything",
    "fond of repeating the same three pieces of advice to anyone who listens",
    "careful with coin in a way that borders on miserly",
    "easy to underestimate until the moment it matters",
    "given to extreme opinions on minor subjects and silence on important ones",
    "known to remember everything and to choose carefully what they mention",
    "respected for plain speaking even when it costs them",
    "inclined to trust animals more readily than people",
    "prone to nervous energy that they channel into relentless work",
    "fond of their own company and unapologetic about it",
    "surprisingly tender-hearted beneath a brusque manner",
    "given to dark humour that not everyone finds amusing",
    "known to wake before dawn and be the last to leave at night",
    "deeply private in ways that are sometimes mistaken for coldness",
    "possessed of a temper that emerges rarely and spectacularly",
    "more observant than they let on, which has served them well",
    "inclined to finish what others start and say little about it",
    "known to take disagreements personally and disputes professionally, which is the wrong way round",
    "cautious by nature but capable of sudden and surprising boldness",
    "better at comforting others than at accepting comfort themselves",
    "given to strong opinions on food and absolutely no opinions on anything else",
    "prone to a dry wit that is either charming or insufferable depending on the recipient",
]

# Single-sentence life events added to the bio
_LIFE_EVENTS = [
    "Once travelled far on a merchant ship and has never quite settled since.",
    "Narrowly survived a flood that took the family farm in their youth.",
    "Studied under a travelling scholar for three summers before returning home.",
    "Worked as a road guard before finding their place here.",
    "Lost their first trade to bandits and built everything back from nothing.",
    "Once nursed a dying horse back to health and earned the whole town's respect for it.",
    "Raised by an aunt after their parents were taken by fever.",
    "Spent years wandering before this place finally felt like home.",
    "Served briefly at a noble's court and rarely speaks of what they saw there.",
    "Won a local contest long ago and still keeps the ribbon tucked away somewhere.",
    "Sent to live with distant relatives as a child and returned changed.",
    "Witnessed a fire that destroyed half the market and helped lead the rebuilding.",
    "Once found a stranger near death on the road and nursed them back without asking for anything.",
    "Trained as an apprentice under a well-regarded craftsman in another town.",
    "Narrowly avoided a serious debt years ago and has been careful with coin ever since.",
    "Crossed the region on foot as a young person on a dare and never regretted it.",
    "Survived a harsh winter that took three neighbours and shaped the rest of their outlook considerably.",
    "Apprenticed to the wrong master for four years and spent the next four unlearning what they were taught.",
    "Inherited a small piece of land that turned out to carry an old dispute attached to it.",
    "Once talked a desperate man down from a very bad decision and is not sure whether they did him a favour.",
    "Left a secure position abruptly under circumstances they decline to detail, and seem at peace with it.",
    "Spent two years in another town after a falling-out that has never been fully explained.",
    "Helped deliver twins during a blizzard once, and considers it the most useful thing they've ever done.",
    "Was wrongly accused of something minor years ago; the matter was resolved but not entirely forgotten.",
    "Watched their family's trade collapse slowly over a decade and learned more from it than they would have liked.",
    "Received an unexpected inheritance from a relative they barely knew, and still isn't sure what to make of it.",
    "Once kept a man's secret for years when revealing it would have benefited them considerably.",
    "Took in a stray dog that lived for eleven years and is quietly still not over its death.",
    "Survived a serious illness that left them changed in ways they find difficult to put into words.",
    "Worked two harvests for a family that wasn't theirs when their own was struggling, and never asked to be repaid.",
    "Crossed paths with someone important once and has wondered since what they knew that they didn't share.",
    "Paid for a young person's apprenticeship after noticing their situation and saying nothing about it afterwards.",
    "Was offered a chance to leave and build something different, and chose to stay, and does not entirely know why.",
    "Made a decision during a hard season that was correct and cost them a friendship they still miss.",
    "Spent three months recovering at a farmhouse owned by strangers, who became the closest thing to family they have.",
    "Witnessed something unsettling on the road once and has told the story carefully fewer times than they've thought about it.",
    "Carried a letter across the region for a dying man once; it was delivered, and whatever it contained changed hands quietly.",
    "Was offered a dishonest profit during a lean year and declined it, and has never fully stopped wondering if that was wisdom.",
    "Once spent a season working under a different name in a different town for reasons that seemed clearer at the time.",
    "Helped rebuild a bridge that collapsed during a storm and has taken quiet satisfaction in it every time they cross it.",
    "Kept a shop running alone for a year when their partner fell ill, and discovered something about themselves in the process.",
    "Fostered a child for two years while their family sorted itself out, and found the parting harder than anticipated.",
    "Turned down a marriage arrangement their parents considered advantageous and has never been given a full accounting of what was lost.",
    "Narrowly avoided being in the wrong place during a significant event; the margin was smaller than anyone knows.",
    "Found an old letter once that wasn't addressed to them and contains information that would complicate at least two people's lives.",
]

# Personal secrets revealed at Friendly tier
_PERSONAL_TENSIONS = [
    "owes a quiet debt to the local merchant guild that hasn't been repaid.",
    "harbours resentment toward a sibling who inherited more than their share.",
    "suspects a neighbour of stealing from them years ago but cannot prove it.",
    "once fled a town under circumstances they refuse to speak of.",
    "has been sending coin to family in another region without telling anyone here.",
    "quietly fears they aren't suited to the role they've been given.",
    "was passed over for a position they had worked years toward.",
    "carries guilt from a decision made during a hard winter, long ago.",
    "made a promise years back that they still haven't been able to keep.",
    "deeply disagrees with how the town is governed but says nothing publicly.",
    "is quietly estranged from a family member who moved far away.",
    "suspects someone they trust of hiding something from them.",
    "lost something precious years ago and has never fully made peace with it.",
    "borrowed more than they let on during a lean season and is still paying it back.",
    "turned down an offer years ago that they sometimes wonder about in quiet moments.",
    "is aware that a story about them circulating in town is not entirely false.",
    "carries a private conviction that they were responsible for something no one else has blamed them for.",
    "knows something about a local figure that would cause significant damage if it became known.",
    "has been contacted recently by someone from their past who they had hoped was gone for good.",
    "is concealing a health matter from everyone around them.",
    "has a child somewhere they have never met, and has made no move toward changing that.",
    "once gave false testimony in a minor matter to protect someone, and the weight of it has not diminished.",
    "is quietly moving assets in ways that would concern their household if discovered.",
    "suspects that a close relationship in their life was deliberately engineered for reasons they haven't worked out yet.",
    "holds a piece of information that would resolve a local dispute but releasing it would harm someone they owe a favour.",
    "has been shortchanging a supplier in small amounts for years and regards it as merely correcting an unfair arrangement.",
    "recently discovered that their family name is not entirely what they understood it to be.",
    "is carrying on a correspondence that their household would not approve of.",
    "was present at an event that was later misreported and has chosen not to correct the record.",
    "owes a significant favour to someone who has not yet named what they want for it.",
]

# Dynasty founding stories (one picked per dynasty/region)
_DYNASTY_ORIGINS = [
    "The house rose through a series of shrewd trade agreements three generations back.",
    "Founded by a celebrated soldier who was granted these lands after a regional conflict.",
    "Built their name on an early monopoly over grain and salt when the region was young.",
    "Came to prominence by mediating a long-running dispute between two feuding towns.",
    "Earned their standing as master builders who raised the first stone walls in the region.",
    "Rose from farming stock across two hard generations of accumulated land.",
    "Gained their seat through a strategic marriage that unified two rival bloodlines.",
    "A scholarly lineage that built influence by advising successive town councils.",
    "Built their fortune in the wool trade before moving into governance.",
    "Earned their position by leading the defence of the region during a period of raids.",
    "Granted authority by popular acclaim after restoring order during a famine.",
    "Grew powerful by controlling the region's main road and collecting passage agreements.",
    "Emerged from obscurity when a timely loan to the previous ruling family was never repaid.",
    "Built their name supplying provisions to the region's garrisons for three decades before acquiring formal authority.",
    "Rose to prominence by controlling the only reliable bridge in the region during a period of heavy flooding.",
    "Established through a series of carefully arranged marriages that absorbed three smaller families over two generations.",
    "Founded by a physician whose reputation for saving lives during a plague was converted into political standing.",
    "Grew from a minor clerical function into a governing authority when the original rulers died without heirs.",
    "Built their influence as arbiters in the region's commercial disputes, collecting fees and obligations along the way.",
    "Came to power by financing the rebuilding of a town after a major fire and naming the terms of reconstruction.",
]

# Current tensions within a dynasty (one picked per dynasty/region)
_DYNASTY_TENSIONS = [
    "The succession is quietly disputed — more than one heir believes the seat should be theirs.",
    "Rumours of mounting debt to a distant trading consortium have begun circulating.",
    "An old grievance with a neighbouring house has never fully been laid to rest.",
    "The head of house has grown reclusive in recent months, and allies are beginning to worry.",
    "A recent decision has divided the family — some believe it was a grave error.",
    "The house is quietly losing influence to a rising merchant family in the region.",
    "There is pressure from above to consolidate power, and not everyone agrees on how.",
    "A marriage alliance is being arranged; not all members of the house approve of the match.",
    "Someone within the house is said to be corresponding with an outside power.",
    "The region's reputation for stability is slipping, and the family is being blamed.",
    "An inheritance dispute from two generations ago has resurfaced and found new advocates.",
    "The house is divided over whether to align with a distant power or remain independent.",
    "The head of house is ageing and has refused to name a successor, which is beginning to affect everything.",
    "A trusted advisor has recently departed under circumstances the family describes as voluntary.",
    "A junior member of the house has begun building independent relationships the head has not sanctioned.",
    "The family's oldest ally in the region has signalled, without stating it plainly, that conditions have changed.",
    "A rumour regarding the legitimacy of the current head's claim has been circulating in the region's inns.",
    "The house controls less of the region's actual trade than its formal position would suggest.",
    "An external power has been quietly purchasing obligations throughout the region; the family has noticed.",
    "A document has surfaced that one branch of the family regards as binding and another regards as a forgery.",
    "The house has committed publicly to a course of action that a significant portion of the family believes is wrong.",
    "A member of the house has made a private enemy of someone with more reach than anyone anticipated.",
    "The family's ceremonial seat is contested by a rival with an argument that, on paper, is more compelling than expected.",
    "A son or daughter of the house is reportedly living under a different name elsewhere in the region.",
]


# ---------------------------------------------------------------------------
# Identity generation
# ---------------------------------------------------------------------------

def generate_identity(npc_uid: str, town_id: int, _role: str, world_seed: int) -> dict:
    """Return a stable identity dict for one NPC.

    Keys: first_name, family_name, gender, display_name, blurb, bio, personal_tension
    """
    rng = random.Random(hash((npc_uid, world_seed, "identity")) & 0xFFFFFFFF)

    gender = rng.choice(("m", "f"))
    first_name = rng.choice(_FIRST_NAMES_M if gender == "m" else _FIRST_NAMES_F)
    family_name = rng.choice(_FAMILY_NAMES)

    qualifier = rng.choice(_BIRTHPLACE_QUALIFIERS)
    profession = rng.choice(_PROFESSION_LINES)

    from towns import TOWNS
    town_name = TOWNS[town_id].name if town_id in TOWNS else "the region"
    if qualifier:
        location_phrase = f"{qualifier} {town_name}"
    else:
        location_phrase = f"in {town_name}"

    blurb = f"Born {location_phrase}, from a line of {profession}."

    pronoun  = "He" if gender == "m" else "She"
    event    = rng.choice(_LIFE_EVENTS)
    trait    = rng.choice(_PERSONAL_TRAITS)
    bio      = f"{blurb} {event} {pronoun} is {trait}."
    tension  = rng.choice(_PERSONAL_TENSIONS)

    return {
        "first_name":        first_name,
        "family_name":       family_name,
        "gender":            gender,
        "display_name":      f"{first_name} {family_name}",
        "blurb":             blurb,
        "bio":               bio,
        "personal_tension":  tension,
    }


# ---------------------------------------------------------------------------
# Family tree assignment
# ---------------------------------------------------------------------------

# NPC type strings considered "adult" (can be paired as spouses / siblings)
_ADULT_TYPES = {
    "npc_villager", "npc_farmer", "npc_elder", "npc_beggar", "npc_noble",
    "npc_pilgrim", "npc_drunkard", "npc_quest", "npc_merchant", "npc_blacksmith",
    "npc_innkeeper", "npc_scholar", "npc_jewelry", "npc_shrine", "npc_trade",
    "npc_restaurant", "npc_doctor", "npc_coffee", "npc_wine", "npc_guard",
    "npc_musician", "npc_town_crier", "npc_weapon_armorer", "npc_quartermaster",
    "npc_garrison_commander",
}
_CHILD_TYPE = "npc_child"

# NPC types considered rulers (can be assigned to a cross-town dynasty)
_RULER_TYPES = {"npc_noble", "npc_elder"}

_DYNASTY_ROLES = ["head", "heir", "heir", "cousin", "cousin", "cousin"]


def assign_ruling_dynasties(world, world_seed: int) -> None:
    """Link nobles and elders across each region into a shared ruling dynasty.

    Must be called after all cities for the world are built.

    Sets on each ruler NPC:
        dynasty_id    (int)        — region_id
        dynasty_name  (str)        — e.g. "House Voss"
        dynasty_role  (str)        — "head" | "heir" | "cousin"
        dynasty_kin   (list[dict]) — [{display_name, town_name, dynasty_role}, ...]
    """
    from towns import REGIONS, TOWNS

    # Group ruler entities by town_id (nobles/elders) and by region_id (leaders)
    rulers_by_town:    dict = {}
    leaders_by_region: dict = {}
    for entity in world.entities:
        aid = getattr(entity, "animal_id", "")
        if aid in _RULER_TYPES:
            tid = getattr(entity, "town_id", None)
            if tid is not None:
                rulers_by_town.setdefault(tid, []).append(entity)
        elif aid == "npc_leader":
            rid = getattr(entity, "region_id", None)
            if rid is not None:
                leaders_by_region.setdefault(rid, []).append(entity)

    # Pre-compute rival house names keyed by region_id for cross-reference
    def _rival_house_name(rid):
        rng_r = random.Random(hash((rid, world_seed, "dynasty")) & 0xFFFFFFFF)
        return f"House {rng_r.choice(_FAMILY_NAMES)}"

    for region_id, region in REGIONS.items():
        rng = random.Random(hash((region_id, world_seed, "dynasty")) & 0xFFFFFFFF)
        dynasty_family  = rng.choice(_FAMILY_NAMES)
        dynasty_name    = f"House {dynasty_family}"
        dynasty_origin  = rng.choice(_DYNASTY_ORIGINS)
        dynasty_tension = rng.choice(_DYNASTY_TENSIONS)

        # Find rival house (first rival region in relations)
        dynasty_rival           = None
        dynasty_rival_region_id = None
        for other_rid, rel in getattr(region, "relations", {}).items():
            if rel == "rival" and other_rid in REGIONS:
                dynasty_rival           = _rival_house_name(other_rid)
                dynasty_rival_region_id = other_rid
                break

        # Gather all rulers in this region as (npc, town_id) pairs
        region_rulers = []
        for tid in region.member_town_ids:
            for npc in rulers_by_town.get(tid, []):
                region_rulers.append((npc, tid))

        region_leaders = leaders_by_region.get(region_id, [])

        if not region_rulers and not region_leaders:
            continue

        rng.shuffle(region_rulers)

        # Assign dynasty roles (head → heirs → cousins)
        roles = [_DYNASTY_ROLES[min(i, len(_DYNASTY_ROLES) - 1)]
                 for i in range(len(region_rulers))]

        # Generate the full multi-generational chronicle for this dynasty
        import npc_dynasty as _dyn
        town_names = [TOWNS[tid].name for tid in region.member_town_ids if tid in TOWNS]
        chronicle  = _dyn.generate_chronicle(
            region_id, world_seed, dynasty_family,
            rival_family=dynasty_rival,
            town_names=town_names,
        )

        # Apply dynasty data to each noble/elder ruler
        for (npc, _tid), role in zip(region_rulers, roles):
            npc.dynasty_id              = region_id
            npc.dynasty_name            = dynasty_name
            npc.dynasty_role            = role
            npc.dynasty_history         = dynasty_origin
            npc.dynasty_tension         = dynasty_tension
            npc.dynasty_rival           = dynasty_rival
            npc.dynasty_rival_region_id = dynasty_rival_region_id
            npc.dynasty_chronicle = chronicle
            npc.dynasty_ambition  = _dyn.generate_ruler_ambition(
                getattr(npc, "npc_uid", str(id(npc))), world_seed
            )
            if hasattr(npc, "identity") and npc.identity:
                npc.identity["family_name"] = dynasty_family
                npc.identity["display_name"] = (
                    f"{npc.identity['first_name']} {dynasty_family}"
                )

        # Build kin list for each noble/elder ruler
        for (npc, _tid), _role in zip(region_rulers, roles):
            kin = []
            for (other, other_tid), other_role in zip(region_rulers, roles):
                if other is npc:
                    continue
                town_name  = TOWNS[other_tid].name if other_tid in TOWNS else "Unknown"
                other_name = (other.identity.get("display_name", "?")
                              if hasattr(other, "identity") and other.identity else "?")
                kin.append({
                    "display_name": other_name,
                    "town_name":    town_name,
                    "dynasty_role": other_role,
                })
            npc.dynasty_kin = kin

        # Stamp dynasty data onto LeaderNPCs (capital city leaders) for this region
        noble_kin = [
            {"display_name": (n.identity.get("display_name", "?")
                              if hasattr(n, "identity") and n.identity else "?"),
             "town_name":    TOWNS[tid].name if tid in TOWNS else "Unknown",
             "dynasty_role": role}
            for (n, tid), role in zip(region_rulers, roles)
        ]
        for leader in region_leaders:
            leader.dynasty_id              = region_id
            leader.dynasty_name            = dynasty_name
            leader.dynasty_role            = "head"
            leader.dynasty_history         = dynasty_origin
            leader.dynasty_tension         = dynasty_tension
            leader.dynasty_rival           = dynasty_rival
            leader.dynasty_rival_region_id = dynasty_rival_region_id
            leader.dynasty_chronicle       = chronicle
            leader.dynasty_ambition        = _dyn.generate_ruler_ambition(
                getattr(leader, "npc_uid", str(id(leader))), world_seed
            )
            leader.dynasty_kin = noble_kin


def assign_families(npcs: list, town_id: int, world_seed: int) -> None:
    """Group NPCs in a city into family units.

    Sets on each NPC:
        family_id    (str)  — "{town_id}_{family_index}"
        family_role  (str)  — "parent" | "child" | "elder" | "singleton"
        spouse_uid   (str|None)
        parent_uids  (list[str])
        sibling_uids (list[str])
    """
    rng = random.Random(hash((town_id, world_seed, "families")) & 0xFFFFFFFF)

    adults   = [n for n in npcs if getattr(n, "animal_id", "") in _ADULT_TYPES
                                 and getattr(n, "animal_id", "") != "npc_elder"]
    elders   = [n for n in npcs if getattr(n, "animal_id", "") == "npc_elder"]
    children = [n for n in npcs if getattr(n, "animal_id", "") == _CHILD_TYPE]

    # Initialise family fields on every NPC
    for npc in npcs:
        npc.family_id    = None
        npc.family_role  = "singleton"
        npc.spouse_uid   = None
        npc.parent_uids  = []
        npc.sibling_uids = []

    rng.shuffle(adults)
    rng.shuffle(elders)
    rng.shuffle(children)

    family_index = 0

    # Pair adults into couples; assign 0–3 children to each pair
    while len(adults) >= 2:
        fid = f"{town_id}_{family_index}"
        family_index += 1

        parent_a = adults.pop()
        parent_b = adults.pop()

        parent_a.family_id   = fid
        parent_b.family_id   = fid
        parent_a.family_role = "parent"
        parent_b.family_role = "parent"
        parent_a.spouse_uid  = parent_b.npc_uid
        parent_b.spouse_uid  = parent_a.npc_uid

        # Share the same family_name — use the first parent's family name
        if hasattr(parent_b, "identity") and hasattr(parent_a, "identity"):
            parent_b.identity["family_name"] = parent_a.identity["family_name"]
            parent_b.identity["display_name"] = (
                f"{parent_b.identity['first_name']} {parent_a.identity['family_name']}"
            )

        # Assign children
        num_kids = rng.randint(0, min(3, len(children)))
        family_children = [children.pop() for _ in range(num_kids)]

        for kid in family_children:
            kid.family_id    = fid
            kid.family_role  = "child"
            kid.parent_uids  = [parent_a.npc_uid, parent_b.npc_uid]
            if hasattr(kid, "identity") and hasattr(parent_a, "identity"):
                kid.identity["family_name"] = parent_a.identity["family_name"]
                kid.identity["display_name"] = (
                    f"{kid.identity['first_name']} {parent_a.identity['family_name']}"
                )

        sib_uids = [k.npc_uid for k in family_children]
        for kid in family_children:
            kid.sibling_uids = [u for u in sib_uids if u != kid.npc_uid]

    # Remaining single adults become singletons (already initialised)

    # Assign elders to existing families as extended family, or give them their own
    for elder in elders:
        if family_index > 0 and rng.random() < 0.7:
            # Join a random existing family
            fid = f"{town_id}_{rng.randint(0, family_index - 1)}"
            elder.family_id   = fid
            elder.family_role = "elder"
            # Find that family's members and link as siblings (loose)
            for npc in npcs:
                if npc.family_id == fid and npc is not elder:
                    elder.sibling_uids.append(npc.npc_uid)
                    break
        else:
            elder.family_id   = f"{town_id}_{family_index}"
            elder.family_role = "elder"
            family_index += 1

    # Remaining unparented children become singletons
    for kid in children:
        kid.family_id   = f"{town_id}_{family_index}"
        kid.family_role = "child"
        family_index += 1
