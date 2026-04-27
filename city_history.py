"""City history chronicle generation — founding stories and local lore for each town.

All output is deterministic from (town_id, world_seed). Nothing is saved.
"""
import random

# ---------------------------------------------------------------------------
# Data pools
# ---------------------------------------------------------------------------

_FOUNDING_TYPES = [
    "a trade outpost established by a merchant family following a newly charted route",
    "a military garrison that was never formally decommissioned and simply became a town",
    "a refugee settlement that outlasted the crisis that created it",
    "a pilgrimage stopover that discovered it earned more from the travelers than from piety",
    "a seasonal market that gradually became permanent when the merchants stopped bothering to leave",
    "a farming community established by a land grant that most recipients considered punishment",
    "a river crossing that found itself indispensable before anyone had decided it was a settlement",
    "a lumber camp that grew faster than the trees it was clearing",
    "a fortified waystation on a road that was more dangerous than the destination it served",
    "a fishing camp that expanded inland when the catch proved insufficient and the soil did not",
    "a supply depot for an expedition that never returned, maintained by those left behind",
    "a garrison outpost that was abandoned by its original authority and claimed by its own people",
    "a clan settlement formed when two families in flight from different directions arrived at the same valley on the same winter",
    "a minor lordship granted to a creditor as partial payment of an unresolvable debt",
    "a mining camp established on a seam that ran out faster than the town built around it",
    "a monastery settlement whose lay community eventually outnumbered and outlasted the original monks",
    "a temporary shelter built ahead of a hard season that proved too useful to dismantle",
    "a toll point established at a natural choke in the road that the toll-takers eventually decided to defend rather than abandon",
    "a meeting ground between two peoples who found proximity less dangerous than the alternatives",
    "a healer's compound that grew outward when the sick who came to recover decided to stay",
]

# {town} = town name
_FOUNDING_ACTS = [
    "the family that built the first permanent structure refused to leave despite three different authorities telling them to, and by the time the fourth arrived, the matter was settled",
    "a single winter of exceptional cold forced a dozen traveling groups to share shelter at {town}, and when the thaw came, not all of them had anywhere better to go",
    "the road that {town} sits on was rerouted around a collapsed bridge, and the town that grew up at the detour never moved back",
    "the original founders disagreed about almost everything except the location, and spent the rest of their lives arguing in a place they had all, despite themselves, grown attached to",
    "a land survey that was supposed to mark the area as unsuitable for settlement contained errors that went uncorrected long enough for settlement to become a fact",
    "the first market at {town} ran three days over its scheduled length because no one wanted to be the first to pack up and concede the trade was done",
    "a crop failure in the surrounding area sent families to {town} in a single season, and the infrastructure built to support them outlasted the emergency",
    "the person who was supposed to lead the founding party died en route; the people who arrived anyway decided the destination was non-negotiable",
    "a garrison ordered to relocate refused on the grounds that they had already built the walls and did not see why they should do so again somewhere else",
    "the charter for {town} was signed by people who had not yet seen the location; those who eventually arrived found it less suitable than described and more difficult to abandon than expected",
    "the first permanent building at {town} was a debt-collection office, and the debtors who came to contest their obligations found it easier to settle nearby than to travel again",
    "the founders were looking for somewhere else entirely and settled for {town} only after determining that continuing the search was more expensive than accepting what they had found",
    "a natural spring that turned out to be less reliable than initially reported still drew enough people to form a town before its limitations became apparent",
    "the first autumn at {town} was mild enough that families who had intended to leave delayed until the roads became impassable, and by spring the concept of leaving had lost urgency",
    "a single act of hospitality during a difficult season generated an obligation that the recipients paid back over the following decades in labor, goods, and eventually permanent residence",
    "the settlement began as three separate camps that shared a well, and by the time they agreed on whose well it was, they had all become the same town",
    "the founders built at {town} because the location was already cleared, having been abandoned by a previous group whose reasons for leaving were not fully explained in anything they left behind",
    "a caravan that intended to pass through lost two wagons to a broken axle and a third to a marriage, and decided that the difficulty of continuing outweighed the inconvenience of staying",
    "the first year at {town} was successful enough that the founders sent for relatives; by the time the relatives arrived, the town was already larger than any of them had planned",
    "the founding document of {town} lists fourteen original settlers; local memory names thirty-one, which gives some sense of how history works in places that record their own",
]

_FOUNDING_LEGACIES = [
    "the original founders are remembered in the names of the main streets, though no one can agree which name belongs to whom",
    "the founding charter is still cited in property disputes, which suggests either that it was very well written or that nothing since has been clear enough to supersede it",
    "nothing from that period survives except the name and the habit of suspicious hospitality",
    "the founders left behind three competing accounts of why they came here, all of which have their adherents and none of which can be fully verified",
    "the founding families are largely gone, absorbed by marriage and departure; the town they built is considerably more durable than their lines",
    "there are no monuments to the founders, which some residents take as evidence of humility and others take as evidence of something else",
    "the original purpose of the settlement was abandoned within a generation, but the settlement itself proved more persistent than its reasons for existing",
    "the founding generation is remembered as having worked very hard; the following generations have been arguing ever since about what they actually built",
    "a fire in the record hall some decades after the founding destroyed most of the early documentation, which has allowed several competing versions of events to persist without resolution",
    "the founders wrote a great deal about their intentions and very little about their methods, which future residents have found characteristic",
    "the oldest building still standing dates from the third generation of settlement, which tells you something about the quality of the first two generations' construction",
    "the founding families established a tradition of annual gathering that continues today, though the reasons given for it have changed considerably over the years",
    "the founders are remembered more fondly than the contemporary record would support, which is a form of generosity that the town extends to itself",
    "the original land rights were never properly filed, a fact that became apparent and contentious about sixty years after it ceased to matter to the people involved",
    "a handful of founding-era tools and personal effects are kept in the hall of the local elder, who brings them out on ceremonial occasions and otherwise keeps them locked away",
]

_NOTABLE_FIGURE_FIRST_NAMES_M = [
    "Aldric", "Bram", "Corvus", "Destan", "Ewald", "Farren", "Guildric", "Harlen",
    "Idris", "Jarvik", "Keld", "Lorcan", "Maren", "Navar", "Oswin", "Pethric",
    "Quill", "Rothgar", "Sander", "Torvald",
]

_NOTABLE_FIGURE_FIRST_NAMES_F = [
    "Aldeth", "Brynn", "Caela", "Deva", "Enna", "Farya", "Gilda", "Hesta",
    "Ilse", "Jara", "Kessa", "Lira", "Marta", "Neva", "Odra", "Petra",
    "Quinna", "Reva", "Sela", "Thyra",
]

_NOTABLE_FIGURE_SURNAMES = [
    "Aldse", "Brac", "Corveth", "Dune", "Fell", "Graff", "Holt", "Irn",
    "Jeld", "Krath", "Lorn", "Meld", "Noss", "Ord", "Pelt", "Rast",
    "Selk", "Tark", "Ulf", "Veld",
]

_NOTABLE_FIGURE_EPITHETS = [
    "the Builder", "the Patient", "the Stubborn", "the Creditor", "the Architect",
    "the Necessary", "the Quiet", "the Unasked", "the Last", "the Accountant",
    "the Reluctant", "the Persistent", "Twice-Stayed", "the Ungrateful", "the Convenient",
    "the Remembered", "the Forgotten", "the Reasoned", "the Practical", "the Sufficient",
]

# {town} = town name, {themselves} = himself/herself/themselves
_NOTABLE_FIGURE_ACTS = [
    "rebuilt {town}'s market hall after the fire at {themselves}' own expense, then spent fifteen years recovering the cost through preferential stall fees — a transaction locals describe as philanthropic",
    "negotiated an end to a prolonged dispute between {town} and its nearest neighbor by conceding almost everything, then reacquired it quietly over the following decade",
    "served as mayor of {town} for an implausible thirty-one years by the simple method of never agreeing on a successor",
    "financed the construction of {town}'s granary on the condition that {themselves}' family maintained administrative control of it in perpetuity, a condition that was agreed to in writing and has been contested in spirit ever since",
    "arrived in {town} with nothing and left it with half of it, which the town's historians describe either as industry or as acquisition depending on which family they belong to",
    "kept {town} solvent during a decade of poor harvests through a series of loan arrangements whose full terms remain unclear to everyone except the creditor",
    "served as the primary intermediary in two generations of land disputes, managing to profit from each resolution in ways that were technically within the terms agreed",
    "established the road connecting {town} to the regional trade route, then charged modest fees for its use for the rest of {themselves}' natural life and arranged for {themselves}' heirs to continue",
    "is credited with saving {town} from abandonment after a hard year by personally traveling to recruit new settlers, though the terms {themselves} offered those settlers are no longer discussed in public",
    "proposed and oversaw the construction of {town}'s current walls, which are considered overbuilt by every military mind who has looked at them and irreplaceable by every resident who has not",
    "resolved a water rights dispute that had divided {town} for a generation, by the method of purchasing the disputed source outright and then charging both parties the same rate",
    "organized the first formal market at {town} at a time when doing so required a permit that {themselves} had not technically obtained",
    "donated the land for {town}'s central square on the condition that it bear no name at all, a condition that has been observed and resented in roughly equal measure",
    "established a lending library whose collection {themselves} had acquired through a series of purchases, gifts, and transactions that the original owners would have described differently",
    "is remembered for having said, on the occasion of {town}'s first formal census, that the number was wrong and that {themselves} knew it because {themselves} had miscounted {themselves}",
    "arranged a marriage alliance between {town}'s two most contentious merchant families, then spent the remainder of {themselves}' life as the only person either side would speak to",
    "wrote {town}'s first set of municipal regulations in language so ambiguous that every subsequent generation has found in it exactly the authority they were looking for",
    "is the only figure from {town}'s early history whose portrait was painted, stored, lost, recovered, and eventually hung in the hall by people who were no longer certain the portrait was of the right person",
    "organized the repair of {town}'s bridge after the flood, collecting contributions from residents who later discovered that the final cost had been lower than the amount collected, though the difference has never been formally accounted for",
    "served three separate terms as town elder at intervals that suggest either great commitment or an inability to remain retired",
]

_NOTABLE_EVENTS = [
    "a siege that lasted four months and was broken not by relief but by the besiegers running out of provisions first — a victory the town celebrates annually with a meal conspicuously lacking in variety",
    "a fire that took the old market district and was later found to have started in a building whose owner had recently been in dispute with the mayor, a coincidence that was investigated and found inconclusive",
    "a flood that reshaped the lower quarter of town and deposited a stratum of silt that the residents found, on examination, to contain materials that did not originate locally",
    "a plague season that killed a third of the population and produced, in its aftermath, a tradition of exceptionally thorough record-keeping that persists to this day",
    "a year of exceptional harvest that funded the construction of half the permanent buildings still standing, and produced a period of optimism that subsequent years spent some decades correcting",
    "the arrival of a delegation from a distant authority who demanded taxes on goods the town had not known were taxable; the negotiation that followed lasted three years and ended with an agreement that both sides claimed as a victory",
    "a winter cold enough that the river froze solid for six weeks, which was unprecedented in living memory and produced, among those who survived it, an unusually pragmatic approach to preparation",
    "the discovery, during the digging of a new well, of a buried foundation from a settlement older than anyone had records for, which was excavated with interest, studied without conclusion, and eventually built over",
    "a trade route collapse that removed the majority of the town's economic purpose in a single season and prompted a decade of reinvention that the town is still completing",
    "a visit from a traveling dignitary whose identity was disputed both before and after the fact, but whose brief stay generated gifts, promises, and obligations that shaped the town's politics for a generation",
    "a rebellion that lasted eleven days, ended in a negotiated settlement, and is described by the current administration as a civic dialogue and by the participants' descendants as something more emphatic",
    "a drought of three years that emptied half the farms and filled the town with people who had nowhere else to go, permanently altering its character from agricultural to something less easily categorized",
    "a period of rapid growth following the opening of a new road that lasted eight years and produced more buildings than residents, a surplus that took a generation to absorb",
    "a collapse of the main bridge that isolated the town for a season, during which it discovered both its capacity for self-sufficiency and several things about its neighbors that it had not previously known",
    "a dispute over market rights that escalated from a disagreement between two families into a civic argument that involved every household, the regional authority, and a mediator from elsewhere who resolved it by siding with no one",
    "a season of unusual animal behavior that the town interpreted variously as omen, disease, or weather-related disturbance, and that has been cited ever since as evidence for whatever the citing party already believed",
    "an unexplained period of prosperity in which the town's coffers doubled without any corresponding event that anyone has been able to identify, which the cautious describe as a mystery and the optimistic describe as earned",
    "a generation of mayors whose collective tenure was characterized by neither achievement nor scandal, which the town's historians have found surprisingly difficult to write about",
    "the arrival of a skilled craftsperson whose technique was unknown in the region and who taught it freely, then left without explanation, and whose name no one thought to record until it was too late",
    "a night on which all the lights in town went out simultaneously for reasons that were never established, which was subsequently remembered very differently by everyone who experienced it",
]

_CURRENT_ERA = [
    "the town is quieter than it was a generation ago, and the older families prefer it that way",
    "the town is growing faster than it has infrastructure to support, and this is creating arguments that have not yet found their resolutions",
    "the town has a reputation for producing reliable goods and unreliable accounts of itself, both of which it has maintained with consistency",
    "the town is at a point where it has become large enough to develop factions but not quite large enough to need to manage them formally",
    "the town is known throughout the region primarily for a product it considers secondary and a reputation it considers incomplete",
    "the town is managed with the kind of competent efficiency that makes for very little worth recording and very stable conditions for those within it",
    "the town has been in a slow transition for about a decade and has not yet determined what it is transitioning into",
    "the town's character has shifted from what it was founded as to something its founders would not have predicted, which it considers neither a loss nor a gain",
    "the town is in a period of consolidation following a decade of rapid change, which most residents have found more comfortable than the change itself",
    "the town is generally regarded by outsiders as smaller than it feels to those who live in it, a gap in perception that the residents find characteristically frustrating",
    "the town has more history than it has historians, and so most of what happened here is remembered in forms that are more durable than accurate",
    "the town operates with a degree of self-sufficiency that it has maintained through periods when the regional authority was more or less interested in it, and regards this as a virtue",
    "the town is currently navigating a question about its future direction that it has been navigating, in various forms, for about thirty years",
    "the town produces exactly one thing that it is known for regionally, is slightly embarrassed by the fame, and has built a small secondary industry around providing it to visitors",
    "the town is at peace with itself in ways that are legible to its residents and invisible to anyone who has not lived here long enough to understand what the current arrangements represent",
]

_LOCAL_LEGENDS = [
    "there is a house at the edge of town that has been locked for forty years; the family that owns it lives elsewhere and has declined every offer to purchase it, without explanation",
    "the old well in the center square runs deeper than any survey has found the water table to be, a discrepancy that the surveyors have noted and the residents have simply accepted",
    "a set of coins found beneath the foundations of the original hall bore dates that could not be reconciled with any calendar the local scholars recognized, and were eventually lost before the question could be resolved",
    "there is a path through the woods south of town that the locals avoid after dark, not because of any specific incident they can name, but because the habit of avoiding it is older than anyone who currently holds it",
    "every decade or so, a traveler arrives asking about a place that sounds like this town but cannot be quite matched to it; they always leave disappointed, and none of them have ever explained clearly what they were looking for",
    "the town's founding document contains a clause about a specific parcel of land that does not correspond to any location anyone has been able to identify, despite two formal attempts to do so",
    "three generations of children have reported hearing music on still nights from the direction of the old mill, which has not been operational in living memory",
    "the town hall has a locked room on the second floor that no current official has a key to; the door is solid and the room, on the available evidence, contains something",
    "a map found during renovation of the old inn showed a different arrangement of the town than any historical record supports, depicting structures that either predate all documentation or were never built",
    "there is an annual tradition in the town of leaving a small offering at the crossroads east of the main gate; no one currently living can explain its origin, but no one has stopped doing it",
    "a single tree in the center of town was planted by the founders and is considerably older than the species usually lives; the town's botanists have no explanation that satisfies the town's historians",
    "the town's records contain a gap of eleven years in the middle of its history during which, by all documentation, nothing happened — a claim that everyone who knows anything about the town finds implausible",
    "there is a name carved into the stone of the oldest building that does not appear in any founding record, tax roll, or burial register; whoever it was has been removed from the town's memory entirely except for this one mark",
    "every resident can describe a smell they sometimes encounter in the lower quarter of town — always the same smell, always brief, always in the same general area — and no one has found a source",
    "the town's dogs consistently refuse to enter one particular alley, which is otherwise unremarkable; the town has stopped trying to determine why and begun simply routing deliveries around it",
    "a letter was found in the walls during a renovation, addressed to a recipient who could not be identified and containing instructions for a task that could not be interpreted; it is kept in the hall and brought out when visitors ask about the town's history",
    "the founding records list a thirteenth founder who appears nowhere in the following documentation — no land grants, no marriages, no death record — as if they arrived, signed, and then ceased to exist",
    "there is a story about a buried fortune somewhere in the old district that is old enough to predate the current layout, specific enough to suggest a real source, and has produced nothing in four attempts to find it",
    "the town has a tradition of painting a specific symbol above doorways that residents cannot explain the meaning of but agree it would be bad luck to stop doing",
    "somewhere in the attic of the hall are the records of a civic proceeding whose subject was sealed by unanimous vote and whose participants all declined to speak of it afterward",
]

# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------

def generate_city_chronicle(town_id: int, town_name: str, biome: str, world_seed: int) -> dict:
    """Return a deterministic narrative chronicle for the given town."""
    rng = random.Random(f"{town_id}:{world_seed}:city_history")

    founding_type   = rng.choice(_FOUNDING_TYPES)
    founding_act    = rng.choice(_FOUNDING_ACTS).replace("{town}", town_name)
    founding_legacy = rng.choice(_FOUNDING_LEGACIES)

    # Notable historical figure
    is_female = rng.random() < 0.5
    if is_female:
        first = rng.choice(_NOTABLE_FIGURE_FIRST_NAMES_F)
        themselves = "herself"
    else:
        first = rng.choice(_NOTABLE_FIGURE_FIRST_NAMES_M)
        themselves = "himself"
    surname  = rng.choice(_NOTABLE_FIGURE_SURNAMES)
    epithet  = rng.choice(_NOTABLE_FIGURE_EPITHETS)
    figure_full = f"{first} {surname}, called '{epithet}'"
    figure_act  = (rng.choice(_NOTABLE_FIGURE_ACTS)
                   .replace("{town}", town_name)
                   .replace("{themselves}", themselves))

    notable_event = rng.choice(_NOTABLE_EVENTS)
    current_era   = rng.choice(_CURRENT_ERA)
    local_legend  = rng.choice(_LOCAL_LEGENDS)

    return {
        "founding_type":   founding_type,
        "founding_act":    founding_act,
        "founding_legacy": founding_legacy,
        "figure_full":     figure_full,
        "figure_act":      figure_act,
        "notable_event":   notable_event,
        "current_era":     current_era,
        "local_legend":    local_legend,
    }
