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
    "the Lame", "the Creditor", "the Fox", "Long-Memory", "the Red",
    "the Grey", "the Widow-Maker", "Three-Times", "the Borrower", "the Knife",
    "the Gracious", "Soft-Spoken", "the Ledger", "Empty-Purse", "the Raven",
    "the Unlucky", "Four-Fingers", "the Architect", "the Reluctant", "the Twice-Married",
    "the Pale", "the Laughing", "the Slow", "Bone-Hand", "the Necessary",
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
    "financed the construction of {town}'s market hall and quietly wrote the charter in a way that anchored the family's authority for generations",
    "arrived as a refugee from a collapsed house elsewhere, rebuilt {themselves} methodically, and outlasted every person who had initially dismissed them",
    "won a disputed inheritance case that had divided the region for a decade, then used the resulting goodwill faster than anyone could think to object",
    "assembled a coalition of minor landholders against the previous authority, led the coalition to victory, and then declined to dissolve it",
    "gained the seat by offering to absorb the old ruling family's considerable debts in exchange for a formal transfer of title — a transaction widely described as generous",
    "was appointed as a temporary steward during a succession crisis and converted that appointment, by increments, into something permanent",
    "controlled the region's water rights at a critical moment of drought and exchanged them for a formal seat rather than coin",
    "built their claim on a single powerful relationship with an outside authority, sustained that relationship for thirty years, and never disclosed its terms",
    "accumulated enough small obligations across the region's merchant class that refusing their claim became more expensive than granting it",
    "came to power after the previous ruling family died in a fever outbreak, having been the only figure in {town} who had prepared for exactly that contingency",
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
    "died in disputed circumstances at a moment that was convenient for at least two parties; no formal inquiry was ever convened",
    "left the house with an excellent reputation and almost no actual money, which later generations have had to quietly reconcile",
    "is buried with more ceremony than most founders receive, which the current generation regards as somewhat ironic given what they know",
    "achieved a great deal and acknowledged none of it in writing, which has made the family's claims both unassailable and impossible to fully substantiate",
    "left a will that named someone no one expected, and that surprise has shaped the family's internal politics ever since",
    "is remembered as a visionary by those who benefited from the vision and as a tyrant by those who were in its way",
    "died leaving the succession clear, the finances sound, and one secret that the house has been protecting with considerable effort ever since",
    "established a tradition of one founding act and one founding concealment; the act is celebrated, the concealment is managed",
    "is credited publicly with building the region's prosperity and privately with having built it on ground that several original residents were removed from",
    "left the family a name that is genuinely respected, which is both an asset and a responsibility that some heirs have found easier to spend than maintain",
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
    "significantly expanded the family's landholdings through a sequence of purchases that were individually unremarkable and collectively alarming",
    "produced four children, named three of them heirs at different points, and died before clarifying which designation was final",
    "was widely regarded as less capable than the founder, spent their tenure proving otherwise in ways the public never fully credited, and died bitter",
    "reformed the house's governance in ways that increased accountability and reduced flexibility, which the current generation cannot decide whether to resent or revere",
    "pursued a feud with a neighbouring family for decades and prevailed, leaving the house both victorious and considerably smaller than it had been",
    "developed a drinking problem that everyone knew about and no one in the family has discussed in thirty years",
    "sold off a significant asset to resolve a crisis and spent the remainder of their tenure insisting it had not been necessary",
    "allied the house with a faction that subsequently lost its position; extracting the family from those commitments occupied the following generation entirely",
    "built a personal relationship with a distant authority that benefited the house for two generations and collapsed spectacularly in the third",
    "governed during the most peaceful and prosperous period the house has known, and is the least-discussed member of the lineage as a result",
    "was deposed briefly, restored after an arrangement that has never been disclosed, and ruled for another twenty years without acknowledging any of it",
    "left the house with a grudge against a specific family that has outlasted both its cause and its original principals, and is now simply inherited",
]

_CURRENT_ERA_SITUATIONS = [
    "The house holds its seat but feels the weight of two generations of accumulated obligations pressing against the present.",
    "The family is more respected than powerful, and some within it have begun to mistake the one for the other.",
    "A transition everyone can see coming has been delayed long enough that preparing for it and pretending it isn't happening have become indistinguishable.",
    "The current head controls the formal seat but not every room in which decisions are made.",
    "The house is owed more than it owes, which sounds advantageous until you try to collect.",
    "The family has outlasted several rivals and is now confronting the possibility that longevity may be masking a longer decline.",
    "A choice is approaching that the current generation has been circling for years; how it is made will define the house for the next two.",
    "The house is in a period of consolidation that some members read as strength and others read as contraction.",
    "An external pressure is being managed quietly, and the amount of effort that management requires has begun to show.",
    "The family occupies a position of formal authority and practical uncertainty simultaneously, which is more common than it appears in the histories.",
    "The house is more financially exposed than its public standing suggests; closing that gap has become the primary private concern.",
    "The current head has been in place long enough to outlive the context that shaped their early decisions, and has not fully adjusted.",
    "The family is operating on assumptions inherited from the previous generation that may no longer be accurate.",
    "The house is at its highest point of formal influence and lowest point of internal agreement in living memory.",
    "An alliance that sustained the family for two generations has been quietly fraying; no one has acknowledged this publicly.",
    "The house has been governing effectively but has done so by deferring several structural problems that are now due.",
    "The region is changing around the family faster than the family is changing to meet it.",
    "The current generation is the most capable the house has fielded in decades and is also the most divided.",
    "The house's public reputation significantly exceeds what an honest internal accounting would support.",
    "The family is in a position where maintaining appearances has become nearly as expensive as the actual governance.",
    "Everyone watching the house from outside believes it is stable; everyone watching it from inside is less certain.",
    "The house controls the seat, manages the territory adequately, and is quietly waiting for something it cannot name to resolve itself.",
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
    "intends to reform the house's finances before anyone outside the family discovers how compromised they are",
    "is working to identify which of the family's current allies is the informant they have long suspected exists",
    "has a specific vision for the region that the family does not share and has been implementing it incrementally without announcement",
    "is attempting to locate a document that, if destroyed, would resolve a problem the house has carried for forty years",
    "wants to arrange a marriage alliance that would effectively merge two houses; has not yet decided whether to ask permission",
    "is investigating the circumstances of a predecessor's death, not from grief but because the answer changes the balance of several current relationships",
    "is building a case for a formal claim that the family abandoned two generations ago, slowly and without informing anyone",
    "has concluded that one of the heirs apparent is unsuitable and is arranging circumstances accordingly rather than stating it",
    "is negotiating, privately, with the rival house — not for peace but for a partition arrangement that would benefit both families at the region's expense",
    "wants, above everything else, to be remembered well, and is making decisions based on how they will read in fifty years rather than how they function now",
    "has accepted that the house is in decline and is focused entirely on ensuring the decline is managed rather than reversed",
    "is trying to engineer a confrontation with the rival family that ends permanently, and will not specify what permanently means",
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
    "began when the {own_family} publicly supported a claimant the {rival_family} opposed; the claimant lost, and the support was not forgotten",
    "traces to a trade consortium that both families attempted to control simultaneously; the resulting dispute was never formally resolved, merely suspended",
    "originated when a member of the {rival_family} was passed over for an appointment that went to a member of the {own_family}, in circumstances that remain disputed",
    "stems from the {own_family} blocking a territorial expansion the {rival_family} had spent a decade preparing; the {rival_family} did not regard this as a business matter",
    "began when a trusted employee of one house was found to have been simultaneously employed by the other, and both families claim to have been the deceived party",
    "originated in competing claims to the same water source that both families' founders believed they had secured exclusively",
    "started when the {rival_family} refused to support the {own_family} during a period of serious difficulty, which the {own_family} have described as a betrayal ever since",
    "traces to a hunting incident two generations ago that one family describes as an accident and the other does not",
    "began when one family's merchant ships undercut the other's in the region's main market by a margin that the affected family regarded as impossible without inside information",
    "originated in a charitable endowment that both families claim credit for establishing and each believes the other has been drawing benefit from without acknowledgement",
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
    "the house's founding charter contains a clause that was deliberately omitted from all subsequent copies distributed to other parties",
    "a confession made by the second-generation head — regarding the founder's methods — was sealed and has been in the possession of a single trusted family for thirty years",
    "an entire branch of the family was formally disinherited two generations ago; the grounds were stated as misconduct, but the actual reason was that they knew something",
    "the family's most important current ally was, two generations ago, directly harmed by the house's actions; the current relationship is built on the assumption that this is forgotten",
    "a significant portion of the family's early land acquisition was funded by an outside party whose identity was never disclosed and whose share of the arrangement has never been honoured",
    "the current head's predecessor did not die of the illness recorded; the family has maintained a consistent account for decades without any member publicly deviating from it",
    "a child born to the founding line was placed with another family under a different name; that family still lives in the region and does not know what they are carrying",
    "the house's relationship with the regional faith is more transactional than it appears; a series of favours exchanged over two generations has never been acknowledged by either party",
    "a private arrangement with the rival house exists — made during a period of mutual crisis — that would, if disclosed, invalidate the entire public framing of their current relationship",
    "the house's most celebrated civic act was, in fact, remediation for a harm they caused and have never acknowledged; the story that replaced it is the one that has survived",
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
