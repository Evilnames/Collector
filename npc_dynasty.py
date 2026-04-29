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
    "inherited a household already accustomed to its own ways and spent twenty years finding the seams where their authority was and wasn't real",
    "produced exactly one document that has mattered more than everything else they did combined, and the document was never intended for public record",
    "was a gifted administrator who found diplomacy uncongenial and handled it anyway, which is reflected in the results",
    "refused, once, to do something the first generation had done without hesitation; whether this elevated the house or softened it depends on the account",
    "took in a distant relative who turned out to be both a genuine asset and a persistent complication for the remainder of their tenure",
    "settled a long-standing boundary dispute by the simple act of marrying across it, which solved one problem while creating at least two others",
    "was publicly humiliated once in a forum that mattered; the recovery was complete and methodical and the people responsible did not prosper",
    "spent a significant portion of their tenure managing a secret the first generation had left without instructions for; the effort aged them considerably",
    "was beloved by several people who never fully understood what they were actually doing, which is either a talent or a warning",
    "lived to ninety-one, which is the thing most people know about them; the governance was, on close study, considerably better than its reputation",
    "left the house with exactly as much as they found it, which sounds neutral and was, in context, a considerable achievement",
    "made enemies carefully and maintained them; by the end of their tenure the nature of those enmities had become a reliable map of the region's actual power",
    "oversaw the construction of three buildings and the collapse of two alliances; the buildings still stand",
    "spent their final decade publicly certain and privately reviewing every major decision they had ever made",
    "delegated heavily, chose well for twenty years, and then chose poorly once in a way that took the next generation ten years to untangle",
    "had a child who exceeded them in every measurable way, which was either the triumph of their governance or its most uncomfortable legacy",
    "was the generation in which the house found out what it actually believed, as distinct from what it had been claiming",
    "outlasted three rivals whose fall they had either arranged or anticipated; the fourth outlasted them",
    "never formally acknowledged the thing the family had done to acquire the seat, and had the opportunity to do so twice",
    "built a tradition of annual accounting that is still practised, still resented, and still the reason the house's finances have never collapsed",
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
    "The house is where it has been for three generations and is no longer certain whether this reflects strength or inertia.",
    "The current generation has everything the previous one built and a full understanding of what it cost; neither fact sits entirely comfortably.",
    "Something the house has been avoiding dealing with is becoming unavoidable; the question is no longer whether but when.",
    "The family is negotiating — with outside parties, with itself, with the past — and the outcomes of each negotiation are related in ways no one has fully mapped.",
    "The house's influence is diffuse in a way that makes it both hard to attack and hard to direct.",
    "The current head has been studying the house's history more carefully than any predecessor, which is either wisdom or anxiety, and possibly both.",
    "The house is in a moment of relative stability that its members are too experienced to fully trust.",
    "The region has changed enough that several of the house's traditional sources of authority no longer apply in the way they once did.",
    "The family is in the process of deciding what it is, now that the question of whether it survives has been settled.",
    "Something that functioned as an asset for two generations has recently become something more complicated.",
    "The house occupies a position that everyone acknowledges and that is increasingly difficult to define precisely.",
    "The current generation is the first to have grown up entirely within the house's established authority, which has shaped them in ways the older members find occasionally alarming.",
    "The house is maintaining three separate sets of relationships that would, if disclosed simultaneously, create a significant contradiction.",
    "There is a question circulating about the house's future that the family is answering differently in different rooms.",
    "The seat is secure, the finances are adequate, the alliances are holding, and the head of house is not sleeping well.",
    "The house has made peace with what it is, which is a different thing from being satisfied with it.",
    "Something the house did several generations ago is about to matter again for the first time in memory.",
    "The family is managing a period of transition that they are calling a period of stability, because that is what it requires them to call it.",
    "Everyone in the house knows what the problem is; not everyone agrees on whether it is the same problem.",
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
    "has concluded that the family's current public position is unsustainable and is trying to engineer a retreat that doesn't look like one",
    "wants to be the head who finally resolved the thing everyone before them only managed",
    "is trying to move the house's financial exposure from the people who currently hold it to people who are less likely to use it",
    "has identified the one change that would secure the house's position for two generations and cannot figure out how to make it without appearing to have known it was necessary",
    "is investigating whether an agreement made in the second generation is still binding, and is being careful not to alert anyone who might also want to know the answer",
    "wants to establish a formal peace with the rival house but cannot persuade the family that the cost is worth it, and is working around this",
    "is attempting to locate and destroy a specific document before someone else finds it; has not been successful and is becoming less subtle",
    "has an opinion about the house's succession that differs from the official position and is building the case to change it",
    "is quietly attempting to determine which of the house's current allies would remain loyal if its formal position were significantly weakened",
    "wants to step back from a specific set of obligations the house has carried since the founding without triggering a crisis",
    "is trying to understand what the founder actually did and whether the family would survive it becoming public, before deciding what to do about it",
    "has been reaching out to a regional power that the family has historically avoided, for reasons they haven't shared with anyone in the house",
    "believes the rivalry with the other house is preventing both families from achieving what either could manage alone, and is trying to prove this without making it political",
    "is working to place a specific person in a position of civic authority; the benefits to the house are not immediately obvious from the outside",
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
    "started when both families arrived in the region in the same season and have been competing for the same ground ever since without either fully acknowledging that this is what they are doing",
    "can be traced to a single piece of property that was surveyed once by each family's representative and came out a different size both times",
    "originates in a debt the {rival_family} owe the {own_family} that is not disputed in amount but is entirely disputed in whether it was ever intended to be repaid",
    "began when the {rival_family} hired away the {own_family}'s most capable household officer under circumstances that both sides describe as standard practice and neither regards as such",
    "traces to a council vote in which the {own_family} opposed the {rival_family}'s interests; the vote went the other way, but the opposition was remembered",
    "started with a piece of writing — a letter, or possibly a pamphlet — that attributed views to the {own_family} which they have never acknowledged holding",
    "stems from a wedding at which something was said by a member of one family to a member of the other; what was said has been described in at least four different ways since",
    "can be traced to a moment when the {own_family} was in serious difficulty and the {rival_family}, in a position to help, chose neutrality; the {rival_family} does not describe it as a choice",
    "originates in a judicial matter in which one family's representative made an argument that prevailed; the losing family believes the argument was dishonest and the records support this reading",
    "began when the {rival_family} expanded into a town the {own_family} had regarded, without formal documentation, as their territory",
    "traces to a commercial arrangement between the two houses that dissolved under circumstances both families describe as the other's fault",
    "started when a member of one house married a member of the other's household staff, which was framed as an insult by one family and a coincidence by the other",
    "originates in a period when both families were allied and one extended the other credit that was not repaid; the lender family considers this the foundation of the rivalry and the borrowing family considers it irrelevant",
    "can be traced to a specific night of negotiation that both families attended with different understandings of what was being negotiated",
]

# Third generation — what the grandchildren did with what was handed to them
_GEN3_ACTS = [
    "consolidated what the previous two generations had built and, in doing so, made it somewhat smaller and considerably more defensible",
    "spent the first decade undoing what their predecessor had done and the second decade wishing they hadn't",
    "produced the house's only genuine reformer — someone who improved things materially and was resented for it almost immediately",
    "was preoccupied with a personal obsession the family has never fully disclosed; the governance continued without them, more or less",
    "navigated a genuine crisis with enough competence that it left almost no mark on the public record, which is perhaps the highest form of the skill",
    "opened formal relations with the rival house for the first time, which half the family regarded as statesmanship and half as surrender",
    "lost the family's primary commercial interest to a competitor in a way that still has not been satisfactorily explained",
    "built a library, reformed the town charter, and was dead within the year; the reforms outlasted them and the library burned",
    "presided over the family's single greatest public embarrassment and managed, through some combination of patience and coin, to ensure it is now barely remembered",
    "was the first member of the house to marry outside the merchant and noble class, which was either a bold statement about values or a serious miscalculation, depending on the outcome",
    "extended the family's reach into two new towns through means the current generation prefers not to examine",
    "was the most beloved member of the lineage by the common people and the most troublesome to the family's actual interests, which is a combination that does not resolve easily",
    "governed for forty-three years and changed nothing deliberately, which is not the same as nothing changing",
    "spent twenty years building something the following generation dismantled in five; both decisions made sense at the time",
    "discovered the house's founding secret, said nothing, and carried the knowledge for the rest of a very long life",
    "was briefly a figure of regional significance before a series of private decisions reduced them to a merely local one",
    "attempted to legitimise the house's origins through a formal historical commission; the commission's findings were never published",
    "produced the one member of the lineage who could have been something remarkable under different circumstances; what circumstances those would have been is still debated",
    "handled everything calmly, left everything better than they found it, and is remembered with respect and very little feeling",
    "was the generation in which the family stopped believing its own mythology and had to decide what to do about that",
    "was the first member of the house to be born into power rather than to build toward it, which gave them a particular relationship to its value",
    "spent their tenure managing a rivalry they had inherited rather than acquired, and ended it with a settlement that neither party publicly celebrates",
    "had no interest in governance and governed anyway, out of obligation and stubbornness; the result was, by most measures, adequate",
    "oversaw the house's first significant act of public charity, which began as reputation management and became, over time, something that looked more like principle",
    "was the generation in which the family first encountered the thing that would eventually require them to choose who they actually were",
    "spent considerable effort maintaining a fiction the first two generations had established and passed the fiction intact to the fourth, along with its accumulated cost",
    "made a decision that was wrong in the way that only becomes clear in the following generation, which is the hardest kind to guard against",
    "was, by all accounts, a good person in a position that did not especially reward that",
    "built the house's reputation for a specific virtue and was genuinely the thing they appeared to be, which the family has been drawing on ever since",
    "governed through a period in which the region changed around them faster than any previous generation had experienced; adapted adequately and complained less than most would have",
    "was the first member of the lineage to refuse an instruction from an outside authority; the refusal cost something and established a precedent the house has needed twice since",
    "died with the house at its highest point of popular standing, which made them impossible to follow well",
    "was regarded in their lifetime as the house's greatest head; the subsequent generation's reassessment has been more complicated",
    "spent their tenure trying to discover whether the founding secret was true and died without a definitive answer, which may be the only outcome that could have preserved the family's peace",
]

# The house's enduring character — how it is broadly known across the region
_HOUSE_TRAITS = [
    "The house is known for producing capable administrators and undistinguished poets.",
    "They are regarded throughout the region as harder than they look and softer than they act.",
    "The family has a reputation for keeping their word in small things and their own counsel in large ones.",
    "They are known for throwing good feasts and conducting very private business.",
    "The house is regarded as fair by those who have dealt with them honestly and formidable by those who have not.",
    "They have a reputation for taking insults slowly and repaying them at interest.",
    "The family is known throughout the region as reliable allies and uncomfortable enemies.",
    "They are regarded as old money in the sense that they no longer feel the need to impress anyone.",
    "The house's reputation is for patience — they have outlasted rivals who were better-resourced, better-connected, and, in at least one case, better-looking.",
    "They are known for their hospitality and their memory, in approximately equal measure.",
    "The family is regarded as serious — people bring them problems they believe can actually be solved.",
    "They are known for speaking plainly, which is considered either refreshing or rude depending on who is on the receiving end.",
    "The house has a reputation for being difficult to surprise and very difficult to embarrass.",
    "They are regarded throughout the region as people who finish things, which is either admirable or alarming given what they have sometimes chosen to finish.",
    "The family is known for producing one genuinely exceptional person per generation and one genuinely difficult one.",
    "They have a reputation for being neither the most powerful house in the region nor the least consequential, which is perhaps exactly where they want to be.",
    "The house is known for its record-keeping, which is either a sign of administrative virtue or of accumulated leverage.",
    "They are regarded as a house that has seen enough of the region's history to be neither surprised nor impressed by most of it.",
    "The house is known for keeping its promises in the ways that matter and its silence in the ways that also matter.",
    "They are regarded throughout the region as a family that has been here long enough to be part of the landscape.",
    "The family has a reputation for producing people who are harder to read than they initially appear.",
    "They are known for a particular quality of attention — when the house is interested in something, people notice.",
    "The house is regarded as one of the few families in the region that can be trusted to be what they appear to be.",
    "They have a reputation for recovering from things that would have finished other families, which has generated both respect and a certain wariness.",
    "The family is known for outlasting fashions — in governance, in alliance, in opinion — which some read as wisdom and others as rigidity.",
    "They are regarded as a house that moves slowly by design; what they decide, they tend to do.",
    "The house is known for treating people who work for them well, which is either virtue or policy and has been both at different times.",
    "They have a reputation for never needing to raise their voice, which people who have seen what doesn't require the voice find informative.",
]

# A phrase or attitude attributed to the house across the region
_DYNASTY_SAYINGS = [
    "They are not known for mottos, which is itself a kind of statement.",
    "A saying attributed to their founder: 'Give them what they want. Wait.'",
    "The house is known for one principle: whatever was promised, was promised. No more, no less.",
    "A phrase associated with the family for generations: 'Early and quiet.'",
    "The house is credited with an observation that has circulated beyond it: 'A short memory is a liability you can see coming.'",
    "A phrase heard from members of the house: 'Which version did they hear?'",
    "The phrase most attributed to the current head: 'I'm not in a hurry to be wrong.'",
    "A saying associated with the family: 'We have time. We have always had time. This is not an accident.'",
    "A phrase heard in the household: 'Don't explain what they didn't ask. Don't omit what they'll find out.'",
    "The house is credited with an observation that has circulated beyond it: 'The person who keeps no records has decided to trust memory — and whoever controls the memory.'",
    "The only visible maxim associated with the house: patience, applied correctly, is indistinguishable from power.",
    "A phrase attributed to the second generation: 'We didn't build this to last a decade.'",
    "A phrase that outsiders associate with the family: 'We know. We have always known. We chose not to say.'",
    "The house is known for a toast offered at the end of serious meetings: to the second option.",
    "A saying attributed to the house: 'The rival is not the problem. The rival is the symptom.'",
    "Those who have negotiated with the family report a habit: they repeat what was just offered back in different words, and the new words are always slightly more specific.",
    "A phrase heard from members of the house: 'The next generation will have the luxury of forgetting this. We don't.'",
    "The house is associated with a quality of directness: they name things by their actual names, which other families find either refreshing or extremely uncomfortable.",
    "An expression used internally and occasionally overheard: 'It's not a problem yet. It will be.'",
    "A phrase attributed to the founder that the current generation disputes but has not stopped repeating: 'Every favour is a ledger entry.'",
]

_RIVALRY_INCIDENTS = [
    "{house_a} has seized a shipment bound for {house_b}'s territory. The cause is disputed.",
    "A representative of {house_b} was turned away at a market under {house_a}'s jurisdiction.",
    "{house_a} publicly challenged {house_b}'s claim to a border toll road. Neither side has backed down.",
    "Someone burned a supply cache near {house_b}'s frontier. {house_a} has issued a denial.",
    "{house_b} circulated a pamphlet attributing {house_a}'s recent prosperity to fraud.",
    "A caravan flying {house_a}'s colours was stopped and searched by guards loyal to {house_b}.",
    "A border magistrate has publicly sided with {house_b} in a property dispute against {house_a}.",
    "{house_a} hired away three of {house_b}'s most experienced traders within the same week.",
    "{house_b} has placed a competing merchant in a position {house_a} considered their own.",
    "Graffiti mocking {house_b}'s bloodline appeared in the capital. {house_a} issued a statement of ignorance.",
    "{house_a} called in a debt {house_b} claims was already settled. Neither will produce the original document.",
    "Two trade convoys from the rival houses collided at a crossroads. Official accounts of blame differ by source.",
    "A feast held by {house_b} extended no invitation to {house_a}. It was noticed.",
    "{house_a} accused {house_b}'s factor of bribery. The factor remains in post.",
    "A water channel dispute between the two houses has escalated to formal complaint.",
    "{house_b}'s guards turned back a travelling merchant who claimed {house_a}'s protection.",
    "Members of {house_a} were refused lodging in a town recently placed under {house_b}'s patronage.",
    "{house_b} has publicly backed a candidate for a civic post that {house_a} had quietly supported.",
    "{house_a} is said to have bribed a town official who was previously neutral between the houses.",
    "A fire at a {house_b} grain store has led to quiet accusations against {house_a}. Nothing has been proven.",
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
    "the house's most trusted long-term ally was, at the founding, placed there by an outside party; the arrangement has long since evolved into genuine loyalty, but the origin would create questions no one wants to answer",
    "the founding story the family tells omits a figure who was present at every critical moment and whose role, if acknowledged, would significantly complicate the narrative",
    "a member of the house provided information to an outside authority during a period of regional conflict that was used in ways the member had not fully anticipated; the affected parties never identified the source",
    "the house's primary civic foundation — the one its governance claims to derive from — was produced at the request of the family by someone who was paid to produce a specific conclusion",
    "an act of violence attributed to a third party three generations ago was carried out with the knowledge, if not the direction, of the house; the attribution has stood",
    "the house controls an asset it does not legally own; the documentation that would establish this has been misfiled in a way that has persisted for two generations",
    "a member of the third generation destroyed records that would have benefited a rival family in an active legal matter; the matter resolved against the rival partly as a result",
    "the house's name was acquired, not inherited; the family it replaced was real, and one member of that family is still alive and aware of what happened",
    "a promise made on behalf of the house by the first generation commits its successors to a course of action that two current members know about and neither has acted on",
    "a child of the house is living under someone else's identity elsewhere in the region; this was arranged by the family and was, at the time, presented as protection",
    "the house's origin story involves a figure it credits with founding the dynasty; that figure was not related to the current family and was, in effect, used as a front",
    "the civic record the family points to as evidence of its long tenure in the region was partially revised; the revision was minor in its factual content and significant in its implications",
    "a significant debt the house carried into the second generation was discharged under circumstances that the creditor's family, if they knew the full account, would contest",
    "the house knows the location of something that several other parties have been searching for, and has decided that knowing and not disclosing is the most advantageous position",
    "a member of the house has been in contact with its own rival house's disaffected heir for a period of years; what has been exchanged in those communications is known to no one else",
]


# ---------------------------------------------------------------------------
# History-aware selection — bias prose pools toward themes that actually
# happened in this dynasty's simulated 500-year history.
# ---------------------------------------------------------------------------

# Tag → keyword phrases. A pool entry containing any phrase picks up that tag.
_TAG_KEYWORDS = {
    "war":        ("war", "battle", "siege", "raid", "armed", "victory",
                   "soldier", "campaign", "conflict", "convoy", "ambush",
                   "border dispute", "violence"),
    "plague":     ("plague", "fever", "wasting", "illness", "outbreak",
                   "sick", "disease"),
    "famine":     ("famine", "drought", "starv", "hunger", "granary"),
    "disaster":   ("fire", "earthquake", "flood", "collapse", "ruin",
                   "destroyed"),
    "trade":      ("trade", "merchant", "coin", "monopoly", "salt road",
                   "broker", "commerce", "market", "caravan", "ledger",
                   "shipment"),
    "debt":       ("debt", "creditor", "borrow", "loan", "owed", "interest",
                   "ledger", "purse", "indebted"),
    "marriage":   ("marriage", "married", "wed", "betroth", "alliance",
                   "marry", "spouse"),
    "founding":   ("granary", "library", "market hall", "charter",
                   "founded", "built", "construction", "endowment",
                   "council", "civic"),
    "violence":   ("killed", "struck", "assassin", "ambush", "knife",
                   "blood", "removed", "dispatched", "deposed"),
    "revolt":     ("revolt", "uprising", "civil unrest", "deposed",
                   "rebellion", "civil war"),
    "succession": ("succession", "claimant", "heir", "disinherit", "seat",
                   "succeeded", "successor"),
    "secret":     ("secret", "concealed", "private", "undisclosed", "hidden",
                   "never disclosed", "never acknowledged", "off the record"),
    "rival":      ("rival", "feud", "rivalry", "opposed", "opponent"),
    "diplomacy":  ("treaty", "council", "diplomat", "negotiat", "envoy",
                   "broker", "intermediary"),
    "decline":    ("decline", "fell", "collapsed", "ruin", "exhausted",
                   "diminished", "dwindled"),
    "scandal":    ("scandal", "humiliat", "embarrass", "disgrace",
                   "compromised"),
}


def _tags_for(text: str) -> set:
    t = text.lower()
    return {tag for tag, kws in _TAG_KEYWORDS.items() if any(k in t for k in kws)}


# Pre-compute tags once at module import. List of sets aligned with each pool.
_FOUNDER_ACT_TAGS    = [_tags_for(t) for t in _FOUNDER_ACTS]
_FOUNDER_LEGACY_TAGS = [_tags_for(t) for t in _FOUNDER_LEGACIES]
_GEN2_ACT_TAGS       = [_tags_for(t) for t in _GEN2_ACTS]
_GEN3_ACT_TAGS       = [_tags_for(t) for t in _GEN3_ACTS]
_HOUSE_TRAIT_TAGS    = [_tags_for(t) for t in _HOUSE_TRAITS]
_RIVALRY_CAUSE_TAGS  = [_tags_for(t) for t in _RIVALRY_CAUSES]
_DARK_SECRET_TAGS    = [_tags_for(t) for t in _DARK_SECRETS]


# Sim event kind → tag set. Multiple tags allowed.
_EVENT_KIND_TAGS = {
    "war_declare":        {"war", "rival"},
    "civil_war":          {"war", "revolt", "violence"},
    "sack":               {"war", "violence", "disaster"},
    "annex":              {"war", "rival"},
    "defeat_kingdom":     {"war", "decline"},
    "kingdom_collapse":   {"decline", "disaster"},
    "succession_war":     {"war", "succession", "violence"},
    "plague":             {"plague"},
    "famine":             {"famine"},
    "earthquake":         {"disaster"},
    "found_settlement":   {"founding"},
    "rebirth":            {"founding"},
    "alliance_form":      {"diplomacy", "marriage"},
    "alliance_break":     {"diplomacy", "scandal", "rival"},
    "revolt":             {"revolt", "violence"},
    "kingdom_split":      {"revolt", "decline"},
    "assassination":      {"violence", "secret", "succession"},
    "marriage":           {"marriage", "diplomacy"},
    "succession":         {"succession"},
    "succession_crisis":  {"succession", "violence", "scandal"},
    "extinction":         {"decline", "violence"},
    "birth":              set(),
    "death":              set(),
    "city_shrink":        {"decline"},
    "abandon_decline":    {"decline"},
    "merge":              {"founding"},
    "decline":            {"decline"},
}


def _gather_history_tags(world, region_id: int) -> dict:
    """Return tag → count derived from the kingdom + dynasty's real event log."""
    counts = {}
    plan = getattr(world, "plan", None) if world is not None else None
    if plan is None:
        return counts
    kingdom = plan.kingdoms.get(region_id)
    if kingdom is None:
        return counts
    events = list(plan.chronicle_for_kingdom(region_id))
    events += list(plan.chronicle_for_dynasty(kingdom.dynasty_id))
    for e in events:
        for tag in _EVENT_KIND_TAGS.get(e.kind, ()):
            counts[tag] = counts.get(tag, 0) + 1
    return counts


def _weighted_pick(rng: random.Random, pool: list, pool_tags: list,
                    history_tags: dict):
    """Pick a pool entry, biased toward entries whose tags match history."""
    if not history_tags:
        return rng.choice(pool)
    weights = []
    for tags in pool_tags:
        if not tags:
            weights.append(1.0)
            continue
        bias = sum(history_tags.get(t, 0) for t in tags)
        # Base 1.0 keeps untagged-but-relevant items reachable; bias multiplier
        # of 3 makes a single matching event triple the line's odds.
        weights.append(1.0 + 3.0 * bias)
    return rng.choices(pool, weights=weights, k=1)[0]


# ---------------------------------------------------------------------------
# Generation functions
# ---------------------------------------------------------------------------

def generate_chronicle(region_id: int, world_seed: int, dynasty_family: str,
                       rival_family: str | None = None,
                       town_names: list | None = None,
                       world=None) -> dict:
    """Return a full dynasty chronicle dict for one region's ruling house."""
    from npc_identity import _FIRST_NAMES_M, _FIRST_NAMES_F

    rng = random.Random(hash((region_id, world_seed, "chronicle")) & 0xFFFFFFFF)

    town = town_names[0] if town_names else "the region"

    # Tag counts derived from this dynasty's real simulated history. Empty
    # dict if no plan available — selection then falls back to uniform.
    history_tags = _gather_history_tags(world, region_id)

    founder_first   = rng.choice(_FIRST_NAMES_M + _FIRST_NAMES_F)
    founder_epithet = rng.choice(_FOUNDER_EPITHETS)
    founder_full    = f"{founder_first} {dynasty_family}, called \"{founder_epithet}\""

    act_template  = _weighted_pick(rng, _FOUNDER_ACTS, _FOUNDER_ACT_TAGS, history_tags)
    gender_word   = rng.choice(("himself", "herself"))
    founder_gender = "m" if gender_word == "himself" else "f"
    founder_act   = act_template.format(town=town, themselves=gender_word)
    founder_legacy = _weighted_pick(rng, _FOUNDER_LEGACIES, _FOUNDER_LEGACY_TAGS, history_tags)

    gen2         = _weighted_pick(rng, _GEN2_ACTS, _GEN2_ACT_TAGS, history_tags)
    gen3         = _weighted_pick(rng, _GEN3_ACTS, _GEN3_ACT_TAGS, history_tags)
    current_era  = rng.choice(_CURRENT_ERA_SITUATIONS)
    house_trait  = _weighted_pick(rng, _HOUSE_TRAITS, _HOUSE_TRAIT_TAGS, history_tags)
    house_saying = rng.choice(_DYNASTY_SAYINGS)
    dark_secret  = _weighted_pick(rng, _DARK_SECRETS, _DARK_SECRET_TAGS, history_tags)

    rivalry_text = None
    if rival_family:
        rival_fam = rival_family.replace("House ", "")
        template     = _weighted_pick(rng, _RIVALRY_CAUSES, _RIVALRY_CAUSE_TAGS, history_tags)
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
        "gen3":           gen3,
        "house_trait":    house_trait,
        "house_saying":   house_saying,
        "current_era":    current_era,
        "rivalry_text":   rivalry_text,
        "dark_secret":    dark_secret,
        # Raw fields used by the family tree generator:
        "_founder_first":   founder_first,
        "_founder_epithet": founder_epithet,
        "_founder_gender":  founder_gender,
    }


def generate_ruler_ambition(npc_uid: str, world_seed: int) -> str:
    rng = random.Random(hash((npc_uid, world_seed, "ambition")) & 0xFFFFFFFF)
    return rng.choice(_PERSONAL_AMBITIONS)


# ---------------------------------------------------------------------------
# Family tree (500 years, deterministic, not saved)
# ---------------------------------------------------------------------------

_SIBLING_FATES = [
    "married into a merchant house in a neighbouring region and was rarely seen at home thereafter",
    "took holy orders and is mentioned in family records only at funerals",
    "managed the family's western estates competently and without notice",
    "died in a hunting accident at thirty-one — formally an accident",
    "served as the house's diplomatic envoy for nearly two decades",
    "married the rival house and the family did not discuss them again",
    "fell into a debt scandal that the family quietly absorbed",
    "lived in {town} all their life and was, by all accounts, content",
    "vanished from records after thirty; rumours about where vary",
    "served as steward to two consecutive heads and was widely trusted",
    "drowned in the spring floods at twenty-six",
    "was a noted patron of regional craftsmanship in their later years",
    "made one disastrous investment and was managed carefully ever after",
    "left for distant campaigns and returned briefly twice in forty years",
    "took the family's seat on the regional council without ambition",
    "married well and had the good sense to keep their opinions short",
    "was the family's most respected face in {town}'s civic life",
    "developed a reputation for plain speaking the head of house found useful",
    "died young of a fever — the family record gives no further detail",
    "was set up with a modest estate and never asked for more",
    "spent their life in correspondence with scholars across the region",
    "was widely loved and held no formal position by their own choice",
    "managed the family's accounts for thirty-eight years without an error",
    "fought a duel of consequence and was kept indoors for a year afterward",
    "established the family's library, which is still consulted",
    "married three times and outlived all three spouses",
    "left a will that surprised the family and changed nothing legally",
    "ran the household for an aging head and quietly governed for years",
    "departed for the capital at twenty and returned only to be buried",
    "was the head's most reliable confidant and the only one trusted with the ledger",
]

_DEATH_CAUSES = [
    "a fever in late winter",
    "old age, peacefully",
    "a fall from horseback",
    "complications from a long illness",
    "a hunting accident",
    "the wasting illness that took several of their generation",
    "circumstances the family declined to specify",
    "drowning during the spring floods",
    "a heart attack at table",
    "wounds taken in a border skirmish",
    "old age, surrounded by the household",
    "an illness contracted on a journey",
    "complications following a routine procedure",
    "a stroke in their sixty-third year",
    "an accident the family chose not to investigate further",
]


def _extract_real_lineage(world, region_id: int) -> dict | None:
    """Walk the real Dynasty.members chain and return the chronological
    succession line: founder → each successive head, plus siblings and
    spouses keyed by person_id. Returns None when no plan is available.
    """
    plan = getattr(world, "plan", None) if world is not None else None
    if plan is None:
        return None
    kingdom = plan.kingdoms.get(region_id)
    if kingdom is None:
        return None
    dyn = plan.dynasties.get(kingdom.dynasty_id)
    if dyn is None or not dyn.members:
        return None

    members = dyn.members  # person_id -> Person
    # The reigning succession: walk parent_ids. Founder has role="founder".
    founder = next((p for p in members.values() if p.role == "founder"), None)
    if founder is None:
        founder = min(members.values(), key=lambda p: p.born_year)

    # Build a parent → children index for quick walking and sibling lookup
    children_of = {}
    for p in members.values():
        for par_id in p.parent_ids:
            children_of.setdefault(par_id, []).append(p)

    # Walk forward through the line: at each step pick the child of the
    # current head who themselves became a head (role in {head}). If there's
    # a tie, pick the eldest by born_year for stability.
    chain  = [founder]
    cur    = founder
    safety = 0
    while safety < 40:
        safety += 1
        candidates = [c for c in children_of.get(cur.person_id, [])
                      if c.role in ("head", "heir")]
        # 'heir' may flag the next ruler before they took the seat. Prefer 'head'.
        next_heads = [c for c in candidates if c.role == "head"]
        pick_pool = next_heads or candidates
        if not pick_pool:
            break
        nxt = min(pick_pool, key=lambda p: p.born_year)
        chain.append(nxt)
        cur = nxt

    spouse_of = {}
    siblings_of_head = {}
    for h in chain:
        if h.spouse_id != -1 and h.spouse_id in members:
            spouse_of[h.person_id] = members[h.spouse_id]
        # Siblings = children of h's parent who aren't h and aren't a spouse role
        if h.parent_ids:
            par_id = h.parent_ids[0]
            sibs = [c for c in children_of.get(par_id, [])
                    if c.person_id != h.person_id and c.role != "spouse"]
            siblings_of_head[h.person_id] = sibs

    return {
        "history_years": plan.history_years,
        "chain":         chain,
        "spouse_of":     spouse_of,
        "siblings_of":   siblings_of_head,
        "extinct_year":  dyn.extinct_year,
    }


def _gather_other_houses(world, own_region_id: int, world_seed: int) -> list:
    """Return [(family_name, region_id), ...] for every other ruling house.

    Falls back to a synthetic pool if no plan is available so spouses still
    get a family name in standalone tests.
    """
    from npc_identity import _FAMILY_NAMES
    out = []
    plan = getattr(world, "plan", None) if world is not None else None
    if plan is not None:
        for rid in plan.kingdoms.keys():
            if rid == own_region_id:
                continue
            fam = _dynasty_name_for_region(rid, world_seed).replace("House ", "")
            out.append((fam, rid))
    if not out:
        # Fallback: synthesize a handful of houses so the tree still has
        # cross-house marriages (used by isolated tests / pre-plan worlds).
        rng = random.Random(hash((own_region_id, world_seed, "fallback")) & 0xFFFFFFFF)
        pool = [f for f in _FAMILY_NAMES if f != ""]
        rng.shuffle(pool)
        out = [(f, -1) for f in pool[:8]]
    return out


def _kingdom_relations_for_region(world, region_id: int) -> dict:
    """Return {other_rid: 'ally'|'rival'|'neutral'} for this kingdom, if available."""
    plan = getattr(world, "plan", None) if world is not None else None
    if plan is None:
        return {}
    k = plan.kingdoms.get(region_id)
    if k is None:
        return {}
    return dict(getattr(k, "relations", {}))


def generate_family_tree(region_id: int, world_seed: int, chronicle: dict,
                          dynasty_family: str, town_names: list | None = None,
                          rival_family: str | None = None,
                          rival_region_id: int | None = None,
                          world=None) -> dict:
    """Build a 500-year deterministic family tree for the dynasty.

    Spouses are drawn from other ruling houses across the world's kingdoms,
    so each generation shows real cross-house marriages — sometimes with the
    rival house (an attempt at peace), sometimes with allies, sometimes with
    distant neutrals. Years are negative integers counting back from the
    present (year 0 = current head's lifetime). Nothing is saved.
    """
    from npc_identity import _FIRST_NAMES_M, _FIRST_NAMES_F

    rng  = random.Random(hash((region_id, world_seed, "tree")) & 0xFFFFFFFF)
    town = town_names[0] if town_names else "the region"

    other_houses = _gather_other_houses(world, region_id, world_seed)
    relations    = _kingdom_relations_for_region(world, region_id)
    rival_clean  = rival_family.replace("House ", "") if rival_family else None

    # Pull the real simulated head chain — these become the actual rulers
    # in the tree (real names, epithets, birth/death years), so the chronicle
    # events and the family tree reference the same people.
    real_lin = _extract_real_lineage(world, region_id)

    def _pick_spouse_house():
        """Return (family_name, kind) where kind ∈ {'rival','ally','foreign','common'}."""
        r = rng.random()
        if rival_clean and r < 0.18:
            return (rival_clean, "rival")
        if other_houses and r < 0.88:
            fam, rid = rng.choice(other_houses)
            kind = "foreign"
            if rid in relations:
                rel = relations[rid]
                if rel == "ally":
                    kind = "ally"
                elif rel == "rival":
                    kind = "rival"
            return (fam, kind)
        return (None, "common")

    GEN_COUNT      = 20
    YEARS_SPAN     = 500
    YEARS_PER_GEN  = YEARS_SPAN // GEN_COUNT  # 25
    BASE_YEAR      = -YEARS_SPAN              # founder reign starts here

    people  = []
    next_id = [0]

    def _new(**fields):
        p = {
            "id":           next_id[0],
            "gen":          0,
            "parent_id":    None,
            "spouse_id":    None,
            "gender":       "m",
            "first":        "?",
            "epithet":      None,
            "born":         None,
            "died":         None,
            "ruled_from":   None,
            "ruled_to":     None,
            "is_ruler":     False,
            "is_main_line": False,
            "deed":         None,
            "death_cause":  None,
            "house":        None,   # surname; None = born to this dynasty (uses dynasty_family)
            "match_kind":   None,   # for married-in spouses: rival/ally/foreign/common
        }
        p.update(fields)
        next_id[0] += 1
        people.append(p)
        return p

    def _name_for(gender):
        pool = _FIRST_NAMES_M if gender == "m" else _FIRST_NAMES_F
        return rng.choice(pool)

    # Convert a simulated year (0 = founding, history_years = present) into
    # the tree's year coord (0 = present, negative = past). When no real
    # lineage is available, the procedural BASE_YEAR scheme is used instead.
    def _sim_to_tree(sim_year):
        if real_lin is None or sim_year < 0:
            return None
        return sim_year - real_lin["history_years"]

    real_chain = real_lin["chain"] if real_lin else []
    real_chain = real_chain[:GEN_COUNT]

    def _real_head(gen_idx):
        return real_chain[gen_idx] if gen_idx < len(real_chain) else None

    def _apply_real_to_ruler(person_dict, real_person):
        """Overwrite procedural fields with the real Person's identity + dates."""
        if real_person is None:
            return
        person_dict["first"] = real_person.name or person_dict["first"]
        if real_person.epithet:
            person_dict["epithet"] = real_person.epithet
        b = _sim_to_tree(real_person.born_year)
        d = _sim_to_tree(real_person.died_year) if real_person.died_year != -1 else None
        if b is not None: person_dict["born"] = b
        person_dict["died"] = d  # None means still living
        # Reign window: from coming-of-age to death (or present)
        if person_dict.get("born") is not None:
            person_dict["ruled_from"] = max(person_dict["born"] + 18,
                                             person_dict.get("ruled_from") or person_dict["born"] + 18)
        person_dict["ruled_to"] = d

    # ---- Founder + spouse ----
    f_first   = chronicle.get("_founder_first") or _name_for("m")
    f_gender  = chronicle.get("_founder_gender", "m")
    f_epithet = chronicle.get("_founder_epithet")

    f_born = BASE_YEAR - rng.randint(28, 38)
    f_died = BASE_YEAR + rng.randint(20, 35)
    founder = _new(
        gen=0, gender=f_gender, first=f_first, epithet=f_epithet,
        born=f_born, died=f_died,
        ruled_from=BASE_YEAR, ruled_to=f_died,
        is_ruler=True, is_main_line=True,
        deed=(chronicle.get("founder_act", "").strip().capitalize() + ". "
              + chronicle.get("founder_legacy", "").strip().capitalize() + "."),
        death_cause=rng.choice(_DEATH_CAUSES),
    )
    real_founder = _real_head(0)
    _apply_real_to_ruler(founder, real_founder)

    sp_g  = "f" if f_gender == "m" else "m"
    sp_house, sp_kind = _pick_spouse_house()
    sp_first = _name_for(sp_g)
    sp_born  = (founder["born"] or f_born) + rng.randint(-3, 5)
    sp_died  = (founder["died"] + rng.randint(-15, 20)) if founder["died"] is not None else None
    # Use the real spouse's first name + dates if the sim recorded one.
    if real_founder is not None and real_lin:
        rsp = real_lin["spouse_of"].get(real_founder.person_id)
        if rsp is not None:
            sp_first = rsp.name or sp_first
            b = _sim_to_tree(rsp.born_year)
            d = _sim_to_tree(rsp.died_year) if rsp.died_year != -1 else None
            if b is not None: sp_born = b
            sp_died = d
    f_sp  = _new(
        gen=0, gender=sp_g, first=sp_first,
        born=sp_born, died=sp_died,
        spouse_id=founder["id"],
        house=sp_house,
        match_kind=sp_kind,
    )
    founder["spouse_id"] = f_sp["id"]
    if sp_died is not None:
        f_sp["death_cause"] = rng.choice(_DEATH_CAUSES)

    prev_ruler = founder

    # ---- Subsequent generations ----
    # If real heads end before GEN_COUNT, keep generating procedural ones so
    # the tree always reaches the present. If the last real head is still
    # alive, the chain *is* the present — stop there.
    real_ends_alive = bool(real_chain and real_chain[-1].died_year == -1)
    if real_ends_alive:
        GEN_LIMIT = len(real_chain)
    else:
        GEN_LIMIT = max(GEN_COUNT, len(real_chain))
    last_gen = GEN_LIMIT - 1
    for gen in range(1, GEN_LIMIT):
        rhead = _real_head(gen)
        n_children = rng.randint(2, 4)
        children   = []
        target_b   = prev_ruler["born"] + YEARS_PER_GEN
        for ci in range(n_children):
            c_g = "m" if rng.random() < 0.55 else "f"
            children.append(_new(
                gen=gen, parent_id=prev_ruler["id"], gender=c_g,
                first=_name_for(c_g),
                born=target_b + rng.randint(-4, 4) + ci * 2,
            ))

        # Choose heir — eldest by default, occasionally a younger sibling
        heir_idx = 0
        if n_children >= 2 and rng.random() < 0.18:
            heir_idx = rng.randint(1, n_children - 1)
        heir = children[heir_idx]
        heir["is_ruler"]     = True
        heir["is_main_line"] = True

        reign_start = max(prev_ruler["ruled_to"] + rng.randint(-2, 2),
                          heir["born"] + 18)

        is_current = (gen == last_gen)
        if is_current:
            heir["died"]       = None
            heir["ruled_to"]   = None
            heir["ruled_from"] = reign_start
        else:
            age_at_death = rng.randint(50, 82)
            heir["died"]       = heir["born"] + age_at_death
            heir["ruled_from"] = reign_start
            heir["ruled_to"]   = heir["died"]
            heir["death_cause"] = rng.choice(_DEATH_CAUSES)

        if rng.random() < 0.45:
            heir["epithet"] = rng.choice(_FOUNDER_EPITHETS)

        # Splice real ruler identity + dates onto this heir, if available
        _apply_real_to_ruler(heir, rhead)

        # Weave in chronicle prose at the right generations
        if gen == 1:
            heir["deed"] = chronicle.get("gen2", "").strip().capitalize() + "."
        elif gen == 2:
            heir["deed"] = chronicle.get("gen3", "").strip().capitalize() + "."
        elif is_current:
            parts = []
            if chronicle.get("current_era"): parts.append(chronicle["current_era"].strip())
            if chronicle.get("house_saying"): parts.append(chronicle["house_saying"].strip())
            heir["deed"] = " ".join(parts) if parts else rng.choice(_GEN3_ACTS)
        else:
            pool = _GEN2_ACTS + _GEN3_ACTS
            heir["deed"] = rng.choice(pool).capitalize() + "."

        # Heir's spouse — drawn from another house when possible. If the sim
        # recorded a real spouse for this head, use their name and dates.
        h_sp_g     = "f" if heir["gender"] == "m" else "m"
        h_sp_first = _name_for(h_sp_g)
        h_sp_born  = heir["born"] + rng.randint(-3, 5)
        h_sp_died  = None if (is_current or heir["died"] is None) \
                          else (heir["died"] + rng.randint(-15, 20))
        if rhead is not None and real_lin:
            rsp = real_lin["spouse_of"].get(rhead.person_id)
            if rsp is not None:
                h_sp_first = rsp.name or h_sp_first
                b = _sim_to_tree(rsp.born_year)
                d = _sim_to_tree(rsp.died_year) if rsp.died_year != -1 else None
                if b is not None: h_sp_born = b
                h_sp_died = d
        h_sp_house, h_sp_kind = _pick_spouse_house()
        h_sp = _new(
            gen=gen, gender=h_sp_g, first=h_sp_first,
            born=h_sp_born, died=h_sp_died,
            spouse_id=heir["id"],
            house=h_sp_house,
            match_kind=h_sp_kind,
        )
        if h_sp_died is not None:
            h_sp["death_cause"] = rng.choice(_DEATH_CAUSES)
        heir["spouse_id"] = h_sp["id"]

        # Sibling fates
        for sib in children:
            if sib is heir:
                continue
            sib_age = rng.randint(20, 80)
            still_alive = is_current and rng.random() < 0.4
            if not still_alive:
                sib["died"]        = sib["born"] + sib_age
                sib["death_cause"] = rng.choice(_DEATH_CAUSES)
            sib["deed"] = rng.choice(_SIBLING_FATES).format(town=town)
            # If the fate involves marriage, attach a real house — siblings
            # who marry out adopt that house's name.
            if "married" in sib["deed"]:
                sib_h, sib_k = _pick_spouse_house()
                if sib_h:
                    sib["house"]      = sib_h
                    sib["match_kind"] = sib_k
                    sib["deed"]       = f"{sib['deed']} (House {sib_h})."

        prev_ruler = heir

    return {
        "people":          people,
        "founder_id":      founder["id"],
        "current_head_id": prev_ruler["id"],
        "house_name":      f"House {dynasty_family}",
    }


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


# ---------------------------------------------------------------------------
# Rivalry Tension system
# ---------------------------------------------------------------------------

TENSION_LEVELS = [
    (0, "Calm",    (140, 200, 140)),
    (1, "Tense",   (220, 190,  80)),
    (2, "Hostile", (210, 120,  60)),
    (3, "Feud",    (200,  60,  60)),
]


def _rivalry_key(rid_a: int, rid_b: int) -> str:
    return f"{min(rid_a, rid_b)}_{max(rid_a, rid_b)}"


def _dynasty_name_for_region(rid: int, world_seed: int) -> str:
    from npc_identity import _FAMILY_NAMES
    rng = random.Random(hash((rid, world_seed, "dynasty")) & 0xFFFFFFFF)
    return f"House {rng.choice(_FAMILY_NAMES)}"


def tension_level(player, key: str) -> int:
    return getattr(player, "rivalry_tension", {}).get(key, 0)


def tension_label(player, key: str) -> tuple:
    lvl = tension_level(player, key)
    return TENSION_LEVELS[lvl][1], TENSION_LEVELS[lvl][2]


def _escalate_tension(player, key: str) -> None:
    t = getattr(player, "rivalry_tension", {})
    t[key] = min(3, t.get(key, 0) + 1)
    player.rivalry_tension = t


def _calm_tension(player, key: str) -> None:
    t = getattr(player, "rivalry_tension", {})
    t[key] = max(0, t.get(key, 0) - 1)
    player.rivalry_tension = t


def _apply_region_rel_delta(player, region_id: int, delta: int, world) -> None:
    """Apply relationship delta to all nobles/elders in a region, then re-check milestones."""
    for entity in world.entities:
        if (getattr(entity, "dynasty_id", None) == region_id
                and getattr(entity, "animal_id", "") in {"npc_noble", "npc_elder"}):
            uid = getattr(entity, "npc_uid", None)
            if uid:
                old = player.npc_relationships.get(uid, 0)
                player.npc_relationships[uid] = max(-100, min(100, old + delta))
                check_dynasty_milestones(player, entity, world)


def _make_incident_quest(rid: int, house_name: str, rng) -> dict:
    spec = rng.choice(_DYNASTY_QUEST_SPECS).copy()
    spec["count"]       = rng.randint(1, 2)
    spec["reward_gold"] = 200 + rng.randint(0, 4) * 50
    spec["region_id"]   = rid
    spec["house_name"]  = house_name
    return spec


def _fire_incident(world, player, rid_a: int, rid_b: int, key: str,
                   day_count: int, rng) -> None:
    world_seed   = getattr(world, "seed", 0)
    house_a_name = _dynasty_name_for_region(rid_a, world_seed)
    house_b_name = _dynasty_name_for_region(rid_b, world_seed)

    template     = rng.choice(_RIVALRY_INCIDENTS)
    incident_text = template.format(house_a=house_a_name, house_b=house_b_name)

    player.pending_notifications.append(("Rivalry", incident_text, "uncommon"))
    player.rivalry_last_incident[key] = day_count

    rng_q = random.Random(hash((key, day_count, "iq")) & 0xFFFFFFFF)
    player.incident_quests_active[key] = {
        "side_a":       _make_incident_quest(rid_a, house_a_name, rng_q),
        "side_b":       _make_incident_quest(rid_b, house_b_name, rng_q),
        "incident_text": incident_text,
        "posted_day":   day_count,
        "expires_day":  day_count + 10,
    }


def tick_rivalry_incidents(world, player, day_count: int) -> None:
    from towns import REGIONS, rival_region_ids

    if not hasattr(player, "rivalry_tension"):         player.rivalry_tension        = {}
    if not hasattr(player, "rivalry_last_incident"):   player.rivalry_last_incident  = {}
    if not hasattr(player, "incident_quests_active"):  player.incident_quests_active = {}
    if not hasattr(player, "rivalry_dormant_until"):   player.rivalry_dormant_until  = {}

    seen = set()
    for region_id in list(REGIONS.keys()):
        for rival_rid in rival_region_ids(region_id):
            key = _rivalry_key(region_id, rival_rid)
            if key in seen:
                continue
            seen.add(key)

            # Check existing quest expiry
            iq = player.incident_quests_active.get(key)
            if iq and day_count > iq["expires_day"]:
                del player.incident_quests_active[key]
                _escalate_tension(player, key)

            # Skip dormant rivalries
            if day_count < player.rivalry_dormant_until.get(key, 0):
                continue

            # Fire on ~15-day interval with small jitter
            last = player.rivalry_last_incident.get(key, -99)
            rng  = random.Random(hash((key, day_count // 15)) & 0xFFFFFFFF)
            if day_count - last < 15 + rng.randint(0, 4):
                continue

            _fire_incident(world, player, region_id, rival_rid, key, day_count, rng)


def fulfill_incident_quest(player, side: str, key: str, world) -> tuple:
    """Complete one side of an incident quest. Returns (rel_delta, gold)."""
    iq = getattr(player, "incident_quests_active", {}).pop(key, None)
    if not iq:
        return 0, 0

    quest       = iq[side]
    other_side  = "side_b" if side == "side_a" else "side_a"
    other_quest = iq[other_side]

    gold = quest["reward_gold"]
    player.money += gold

    _apply_region_rel_delta(player, quest["region_id"],       +15, world)
    _apply_region_rel_delta(player, other_quest["region_id"], -8,  world)
    _calm_tension(player, key)

    house_name = quest["house_name"]
    player.pending_notifications.append(
        ("Rivalry", f"You aided {house_name}. Their gratitude is noted.", "rare")
    )
    return 15, gold


# ---------------------------------------------------------------------------
# Broker Peace
# ---------------------------------------------------------------------------

def can_broker_peace(player, rid_a: int, rid_b: int, world) -> bool:
    champ         = getattr(player, "champion_dynasty_regions", set())
    fav           = getattr(player, "favored_dynasty_regions",  set())
    key           = _rivalry_key(rid_a, rid_b)
    dormant_until = getattr(player, "rivalry_dormant_until", {}).get(key, 0)
    current_day   = getattr(world, "day_count", 0)
    return (
        rid_a in fav and rid_b in fav
        and (rid_a in champ or rid_b in champ)
        and current_day >= dormant_until
        and tension_level(player, key) >= 1
    )


def generate_peace_quest(rid_a: int, rid_b: int, world_seed: int) -> dict:
    rng  = random.Random(hash((rid_a, rid_b, world_seed, "peace")) & 0xFFFFFFFF)
    spec = rng.choice(_DYNASTY_QUEST_SPECS).copy()
    spec["count"]       = rng.randint(5, 8)
    spec["reward_gold"] = 800 + rng.randint(0, 4) * 100
    spec["rid_a"]       = rid_a
    spec["rid_b"]       = rid_b
    return spec


def fulfill_peace_quest(player, rid_a: int, rid_b: int, world) -> int:
    key  = _rivalry_key(rid_a, rid_b)
    quest = generate_peace_quest(rid_a, rid_b, getattr(world, "seed", 0))
    gold  = quest["reward_gold"]
    player.money += gold

    if not hasattr(player, "rivalry_tension"):      player.rivalry_tension      = {}
    if not hasattr(player, "rivalry_dormant_until"): player.rivalry_dormant_until = {}

    player.rivalry_tension[key]      = 0
    player.rivalry_dormant_until[key] = getattr(world, "day_count", 0) + 60

    _apply_region_rel_delta(player, rid_a, +10, world)
    _apply_region_rel_delta(player, rid_b, +10, world)

    player.pending_notifications.append(
        ("Rivalry", "Peace brokered. Both houses acknowledge your intervention.", "epic")
    )
    return gold


def apply_racing_result(player, bookkeeper_npc, player_place: int) -> None:
    """Award dynasty favor for horse racing placement. player_place is 1-based (1 = winner)."""
    region_id = getattr(bookkeeper_npc, "_region_id", None)
    world     = getattr(player, "world", None)
    if region_id is None or world is None:
        return

    if player_place == 1:
        favor_delta = 10
        msg = f"Your horse's victory impresses the local nobility!"
    elif player_place == 2:
        favor_delta = 6
        msg = "A strong showing — the local houses take notice."
    elif player_place == 3:
        favor_delta = 3
        msg = "Respectable placement in the race."
    else:
        return  # No dynasty gain for 4th+

    _apply_region_rel_delta(player, region_id, favor_delta, world)

    prestige = getattr(player, "racing_prestige", {})
    prestige[str(region_id)] = prestige.get(str(region_id), 0) + (1 if player_place == 1 else 0)
    player.racing_prestige = prestige

    # Check rival regions — winning can also affect rivalry dynamics
    rival_regions = getattr(player, "rival_dynasty_regions", set())
    for ent in getattr(world, "entities", []):
        rival_rid = getattr(ent, "_region_id", None)
        if rival_rid is not None and rival_rid != region_id and rival_rid in rival_regions:
            _apply_region_rel_delta(player, rival_rid, -4, world)
            break

    check_dynasty_milestones(player, bookkeeper_npc, world)

    if hasattr(player, "pending_notifications"):
        player.pending_notifications.append(("Racing", msg, "uncommon" if player_place == 1 else "common"))

