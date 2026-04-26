"""Dynasty chronicle generation — multi-generational history for ruling houses.

All output is deterministic from (region_id, world_seed). Nothing is saved.
"""
import random

# ---------------------------------------------------------------------------
# Data pools
# ---------------------------------------------------------------------------

_FOUNDER_EPITHETS = [
    "the Elder", "the Bold", "the Merchant", "the Builder", "the Silent",
    "the Fierce", "the Cunning", "Iron-Hand", "the Just", "the Wanderer",
    "Twice-Born", "the Schemer", "the Patient", "the Unyielding", "Stone-Face",
    "the Debtor", "the Fortunate", "the Stubborn", "Far-Sighted", "the Crooked",
    "the Unbowed", "the Quiet", "Bright-Eye", "the Steady", "the Bitter",
]

# {town} = first member town name; {themselves} = himself/herself
_FOUNDER_ACTS = [
    "drove out the previous ruling family during a period of civil unrest and took their seat by popular demand — though that demand was not entirely spontaneous",
    "acquired a monopoly on the region's salt roads through a combination of bribery, patience, and one well-timed marriage",
    "led the defence of {town} against a prolonged raiding season and extracted a permanent seat as the price of continued protection",
    "arranged a marriage between two feuding clans, positioning {themselves} at the head of the resulting alliance before either side fully understood what had happened",
    "uncovered widespread corruption within the old town council and leveraged it into authority that was not offered willingly",
    "funded the region's first permanent granary and declared the debt repaid in governance rather than coin",
    "arrived in the region as a wealthy outsider, spent two decades purchasing goodwill and obligations, and claimed the seat when no one was watching closely enough to stop it",
    "emerged as the unexpected survivor of a three-way succession dispute that left the other two claimants ruined",
    "engineered a trade agreement that ended a decade-long regional boycott and named themselves permanent broker as the fee",
    "led an expedition that located a resource the region now depends upon, and named access rights as their entire reward",
    "was simply the last credible figure standing after a decade of quiet political attrition wore every rival down",
    "purchased a failing minor title from an indebted predecessor and rebuilt it into something worth holding",
    "served as an intermediary in a border dispute and walked away with a seat at the table that was never explicitly offered",
    "leveraged a single act of well-timed generosity during a famine into a claim that the town recognised before it thought to question it",
]

_FOUNDER_LEGACIES = [
    "left the house wealthy and feared — several old families have not forgiven the methods, and they have long memories",
    "was loved by the common people and quietly despised by every merchant of standing in the region",
    "died before fully cementing their gains; the second generation inherited a half-finished empire and a great deal of unresolved goodwill",
    "established a code of conduct for the house that is still cited at councils and argued over at dinners",
    "left behind three children by two different partners and no written guidance on who should follow",
    "is remembered differently in each of the region's towns, which tells you something",
    "left the house in debt to a distant banking family whose patience has limits and whose interest compounds quarterly",
    "built something that has proven durable, though the cost of building it is still spoken of in lowered voices",
    "produced one exceptional heir and one who has been a persistent source of difficulty ever since",
    "is spoken of as a founder in public and as something more complicated after the second cup at any serious gathering",
    "died with everything in order and everyone wondering what they had missed",
    "left instructions so detailed and so contested that the family has been arguing about them ever since",
]

_GEN2_ACTS = [
    "expanded the house's reach by marrying into the merchant class of a neighbouring town — which satisfied no one and alarmed two factions that had previously been neutral",
    "nearly lost everything in a failed trade venture and spent a decade quietly rebuilding, telling no one how close it came",
    "came to open conflict with a rival family and prevailed — but the victory cost considerably more than anyone publicly acknowledges",
    "softened the house's feared reputation into something more diplomatic at the cost of a portion of the real leverage that reputation had carried",
    "entered into a pact with an outside power that the family has been quietly servicing ever since, under terms that have never been fully disclosed",
    "consolidated the house's position methodically and made three relationships that have never recovered as a side effect",
    "governed competently and without incident, which some regard as an achievement in itself and others regard as a missed opportunity",
    "presided as a figurehead while real decisions rested with an advisor whose influence is still debated; whether this was wisdom or weakness depends on who you ask",
    "oversaw a period of genuine prosperity that the current generation is still drawing on, which has obscured some decisions that deserved more scrutiny",
    "died young, officially of illness, at a time that was convenient for more than one party and has never been fully explained",
    "spent their tenure repairing the relationships the founder had used up, and left the house with better allies and less momentum",
    "made a series of decisions that individually appeared reasonable and collectively produced a situation their successors are still managing",
]

_CURRENT_ERA_SITUATIONS = [
    "The house holds its seat but feels the weight of two generations of accumulated obligations pressing against the present.",
    "The family is more respected than powerful, and some within it have begun to mistake the one for the other.",
    "A transition everyone can see coming has been delayed long enough that preparing for it and pretending it isn't happening have become indistinguishable.",
    "The current head controls the formal seat but not every room in which decisions are made.",
    "The house is owed more than it owes, which sounds advantageous until you try to collect.",
    "The family has outlasted several rivals and is now confronting the possibility that longevity may be masking a longer decline.",
    "A choice is approaching that the current generation has been circling for years; how it is made will define the house for the next two.",
]

# Per-ruler personal ambition (seeded per npc_uid, not per dynasty)
_PERSONAL_AMBITIONS = [
    "wants to restore the house to the reputation it held in the founder's generation, and is willing to cut corners to do it",
    "is quietly working to broker peace with the rival house — without the family's knowledge or approval",
    "seeks to expand the house's reach beyond the current region, which the rest of the family regards as equally admirable and alarming",
    "is more focused on a personal grievance than on the house's broader position, and is aware of the problem",
    "genuinely believes the seat should pass to someone better suited, but has not found a way to say it that doesn't sound like surrender",
    "wants to settle the old rivalry definitively and has concluded that sustained diplomacy is unlikely to accomplish this",
    "is quietly accumulating a private reserve against the possibility that the house falls, and framing this as prudence",
    "has been in correspondence with an outside power and has not disclosed the content of any of those letters",
    "is searching for the rumoured illegitimate line of the founding family, for reasons that have not been shared with anyone",
    "wants to be done with all of it and has not yet found an exit that preserves anything worth preserving",
    "is attempting to determine whether a particular story about the founder is true, and would strongly prefer the answer to be no",
    "is quietly preparing to name an unexpected successor, and takes some satisfaction in watching the wrong people position themselves",
    "is trying to renegotiate the terms of an old agreement that the house has never publicly acknowledged making",
    "has decided that one specific rival must be permanently removed from contention and is being methodical about how",
]

# {rival_family}, {own_family}, {town} all available; not all used in every entry
_RIVALRY_CAUSES = [
    "began with a betrothal agreed between the two houses that was broken off without explanation — the {rival_family} have neither accepted the official account nor allowed it to rest",
    "originates in a trade route that both families claim was theirs before the other arrived; the records have been read both ways by people paid to read them carefully",
    "traces to a parcel of land that changed hands under disputed terms two generations ago and has appreciated considerably in the time since",
    "stems from a debt that the {own_family} regard as settled and the {rival_family} do not, and the original documentation has not survived in a form that resolves the question",
    "began when the {rival_family}'s founder made a public statement about the {own_family} that was framed as an opinion and received as a declaration",
    "started with a fire in {town} that destroyed a building of considerable value; one family has consistently implied the other's involvement and has never produced evidence",
    "concerns a civic title that was never clearly established in law; both families hold documentation that supports their position and neither document is quite complete",
    "dates to an ambush on a trade convoy that the {own_family} attribute to agents of the {rival_family} — denied ever since, with a consistency that some find persuasive",
    "began when the {rival_family} provided shelter to an individual the {own_family} wanted returned, and have declined to discuss their reasons for doing so",
    "originated in a marriage alliance between the two houses that ended badly enough that both families now decline to specify exactly what happened",
    "dates to a civic appointment that one family believes was taken from them through the strategic misrepresentation of a third party",
    "started when one family provided testimony in a property dispute that the other family regarded as technically accurate and practically dishonest",
    "can be traced to a single evening of negotiation three generations ago at which something was said that was not written down but was not forgotten",
]

_DARK_SECRETS = [
    "the founder's claim to the seat was not as clean as the formal record suggests — there was a prior claimant, and their departure from the matter was not entirely voluntary",
    "the house carries a substantial undisclosed liability to a creditor who has chosen, so far, not to press it; what they expect in return has never been stated",
    "a member of the second generation produced an heir outside of any recognised arrangement; that heir is alive somewhere in the region and has never been acknowledged",
    "the official account of the previous head's death does not accord with what the household staff who were present remember; those individuals have since been quietly dispersed",
    "the family has been providing quiet access to its regional influence to an outside commercial interest for a number of years, which conflicts with several of its stated positions",
    "a treaty signed in private commits the house to a position that directly contradicts what it advocates in public on a matter currently under discussion",
    "one of the current heirs was not born to the parent the family records name; the discrepancy, if established, would materially affect the succession",
    "a systematic irregularity in the management of civic funds has been concealed beneath careful accounting for two generations; the accumulated sum is not trivial",
    "a member of the family provided material assistance to the rival house during a period of active conflict; this was never formally acknowledged or sanctioned",
    "the asset the house's reputation rests upon most heavily was acquired through a transaction the family would not voluntarily describe in detail",
]


# ---------------------------------------------------------------------------
# Generation functions
# ---------------------------------------------------------------------------

def generate_chronicle(region_id: int, world_seed: int, dynasty_family: str,
                       rival_family: str | None = None,
                       town_names: list | None = None) -> dict:
    """Return a full dynasty chronicle dict for one region's ruling house."""
    from npc_identity import _FIRST_NAMES_M, _FIRST_NAMES_F

    rng = random.Random(hash((region_id, world_seed, "chronicle")) & 0xFFFFFFFF)

    town = town_names[0] if town_names else "the region"

    founder_first   = rng.choice(_FIRST_NAMES_M + _FIRST_NAMES_F)
    founder_epithet = rng.choice(_FOUNDER_EPITHETS)
    founder_full    = f"{founder_first} {dynasty_family}, called \"{founder_epithet}\""

    act_template  = rng.choice(_FOUNDER_ACTS)
    gender_word   = rng.choice(("himself", "herself"))
    founder_act   = act_template.format(town=town, themselves=gender_word)
    founder_legacy = rng.choice(_FOUNDER_LEGACIES)

    gen2         = rng.choice(_GEN2_ACTS)
    current_era  = rng.choice(_CURRENT_ERA_SITUATIONS)
    dark_secret  = rng.choice(_DARK_SECRETS)

    rivalry_text = None
    if rival_family:
        rival_fam = rival_family.replace("House ", "")
        template     = rng.choice(_RIVALRY_CAUSES)
        rivalry_text = template.format(
            rival_family=rival_fam,
            own_family=dynasty_family,
            town=town,
        )

    return {
        "founder_full":   founder_full,
        "founder_act":    founder_act,
        "founder_legacy": founder_legacy,
        "gen2":           gen2,
        "current_era":    current_era,
        "rivalry_text":   rivalry_text,
        "dark_secret":    dark_secret,
    }


def generate_ruler_ambition(npc_uid: str, world_seed: int) -> str:
    rng = random.Random(hash((npc_uid, world_seed, "ambition")) & 0xFFFFFFFF)
    return rng.choice(_PERSONAL_AMBITIONS)


# ---------------------------------------------------------------------------
# Dynasty Favor system
# ---------------------------------------------------------------------------

FAVOR_TIERS = [
    {"min":  70, "name": "Champion", "color": (220, 190,  80),
     "perk": "10% off all purchases in dynasty towns. Rival house members are hostile on sight. Dynasty Quest unlocks."},
    {"min":  45, "name": "Favored",  "color": (140, 200, 120),
     "perk": "5% off all purchases in dynasty towns. Request rewards are enhanced."},
    {"min":  20, "name": "Known",    "color": (170, 160, 130),
     "perk": "Request rewards from this house are enhanced by 50 gold."},
    {"min": -999,"name": "Unknown",  "color": (100,  95, 105),
     "perk": None},
]

# Quest specs — system attr on player, count, readable label
_DYNASTY_QUEST_SPECS = [
    {"attr": "fish_caught",    "count": 5, "label": "rare fish from the region's waters"},
    {"attr": "gemstones",      "count": 3, "label": "fine gemstones for the treasury"},
    {"attr": "wine_bottles",   "count": 4, "label": "bottles of vintage wine for a state occasion"},
    {"attr": "fossils",        "count": 4, "label": "significant fossil specimens for the archive"},
    {"attr": "cheeses",        "count": 6, "label": "aged cheeses for a feast"},
    {"attr": "teas",           "count": 6, "label": "fine teas for the household supply"},
    {"attr": "birds_caught",   "count": 4, "label": "rare bird specimens for the collection"},
    {"attr": "insects_caught", "count": 5, "label": "rare insect specimens for the naturalist's archive"},
    {"attr": "rocks",          "count": 4, "label": "notable rock specimens for the gallery"},
    {"attr": "textiles",       "count": 5, "label": "bolts of fine cloth for the household"},
]


def favor_tier(favor: int) -> dict:
    for tier in FAVOR_TIERS:
        if favor >= tier["min"]:
            return tier
    return FAVOR_TIERS[-1]


def calculate_dynasty_favor(player, region_id: int, world) -> int:
    """Average relationship score across all nobles and elders in the dynasty's region."""
    scores = []
    for entity in world.entities:
        if (getattr(entity, "dynasty_id", None) == region_id
                and getattr(entity, "animal_id", "") in {"npc_noble", "npc_elder"}):
            uid = getattr(entity, "npc_uid", None)
            if uid:
                scores.append(player.npc_relationships.get(uid, 0))
    return int(sum(scores) / len(scores)) if scores else 0


def generate_dynasty_quest(region_id: int, world_seed: int) -> dict:
    rng = random.Random(hash((region_id, world_seed, "dynasty_quest")) & 0xFFFFFFFF)
    spec = rng.choice(_DYNASTY_QUEST_SPECS).copy()
    spec["gold"] = 400 + rng.randint(0, 4) * 100
    return spec


def check_dynasty_milestones(player, npc, world) -> None:
    """Check if dynasty favor has crossed a tier. Trigger perks and notifications."""
    region_id = getattr(npc, "dynasty_id", None)
    if region_id is None:
        return

    favor     = calculate_dynasty_favor(player, region_id, world)
    tier      = favor_tier(favor)
    tier_name = tier["name"]

    reached = getattr(player, "dynasty_tiers_reached", {})
    _TIER_ORDER = ["Unknown", "Known", "Favored", "Champion"]
    prev = reached.get(region_id, "Unknown")
    if _TIER_ORDER.index(tier_name) <= _TIER_ORDER.index(prev):
        return

    # Record new tier
    if not hasattr(player, "dynasty_tiers_reached"):
        player.dynasty_tiers_reached = {}
    player.dynasty_tiers_reached[region_id] = tier_name

    dynasty_name = getattr(npc, "dynasty_name", "the house")

    if tier_name == "Known":
        if not hasattr(player, "known_dynasty_regions"):
            player.known_dynasty_regions = set()
        player.known_dynasty_regions.add(region_id)
        player.pending_notifications.append(
            ("Dynasty", f"{dynasty_name} now knows your name. Request rewards are enhanced.", "uncommon")
        )

    elif tier_name == "Favored":
        if not hasattr(player, "favored_dynasty_regions"):
            player.favored_dynasty_regions = set()
        player.favored_dynasty_regions.add(region_id)
        if not hasattr(player, "known_dynasty_regions"):
            player.known_dynasty_regions = set()
        player.known_dynasty_regions.add(region_id)
        player.pending_notifications.append(
            ("Dynasty", f"You are Favored by {dynasty_name}. Merchants in their towns offer 5% better prices.", "rare")
        )

    elif tier_name == "Champion":
        if not hasattr(player, "champion_dynasty_regions"):
            player.champion_dynasty_regions = set()
        player.champion_dynasty_regions.add(region_id)
        if not hasattr(player, "favored_dynasty_regions"):
            player.favored_dynasty_regions = set()
        player.favored_dynasty_regions.add(region_id)
        if not hasattr(player, "known_dynasty_regions"):
            player.known_dynasty_regions = set()
        player.known_dynasty_regions.add(region_id)

        # Title
        if not hasattr(player, "dynasty_titles"):
            player.dynasty_titles = []
        title = f"Champion of {dynasty_name}"
        if title not in player.dynasty_titles:
            player.dynasty_titles.append(title)

        player.pending_notifications.append(
            ("Dynasty", f"You are Champion of {dynasty_name}! A dynasty quest is now available.", "epic")
        )

        # Rival lockout
        rival_region_id = getattr(npc, "dynasty_rival_region_id", None)
        if rival_region_id is not None:
            if not hasattr(player, "rival_dynasty_regions"):
                player.rival_dynasty_regions = set()
            player.rival_dynasty_regions.add(rival_region_id)
            rival_name = getattr(npc, "dynasty_rival", "their rival house")
            player.pending_notifications.append(
                ("Dynasty", f"Warning: {rival_name} now regards you as an enemy.", "rare")
            )
