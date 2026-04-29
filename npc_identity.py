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
    "Arvid", "Barek", "Cedd", "Dunstan", "Egon", "Falin", "Gerwick", "Halvard",
    "Ivar", "Jorvik", "Knut", "Luthric", "Mord", "Njal", "Odric", "Padraig",
    "Ranulf", "Steinn", "Tomas", "Ulf", "Vigmar", "Weland", "Yrjan", "Zoric",
    "Amund", "Birger", "Colm", "Drago", "Eadric", "Floki", "Gunnar", "Henric",
    "Iolo", "Joren", "Kaspar", "Leif", "Magnus", "Niklas", "Osvald", "Poul",
    "Ragnar", "Styrr", "Trygg", "Ulfar", "Vemund", "Wilmar", "Ymir", "Zahl",
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
    "Astrid", "Bergit", "Ciara", "Disa", "Eira", "Frid", "Gunhild", "Hlif",
    "Idun", "Jolnir", "Katla", "Lofn", "Maren", "Nerys", "Oda", "Pela",
    "Rannveig", "Solveig", "Thora", "Unnr", "Vigdis", "Wulfrun", "Ylva", "Zenna",
    "Arnora", "Bodil", "Ceridwen", "Drifa", "Embla", "Fenja", "Geirthrud", "Hertha",
    "Inga", "Jarnsaxa", "Kjerstin", "Lisbet", "Marta", "Nanna", "Osk", "Pela",
    "Ragnhild", "Sigrun", "Torunn", "Unn", "Valdis", "Winfred", "Yrsa", "Zilda",
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
    "Ashford", "Blackmere", "Coldwater", "Driftwood", "Eldenmoor", "Flintridge",
    "Grimshaw", "Halloway", "Inkstone", "Jolnwood", "Kindermere", "Lowfield",
    "Mudwick", "Nolwood", "Overdale", "Pemwick", "Rottenmere", "Southgate",
    "Tallbridge", "Ulverston", "Varwick", "Welborne", "Crosswick", "Yelwood",
    "Brakemore", "Coldmere", "Darkmoor", "Edgewood", "Fallowfield", "Grimwater",
    "Hillcroft", "Ironshire", "Knaveswell", "Littleford", "Mortwick", "Northmere",
    "Oldbridge", "Penhollow", "Rushwick", "Silverdale", "Tarwick", "Uphollow",
    "Vardenmere", "Wychwood", "Coldstone", "Dunwater", "Edgecroft", "Farwick",
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
    "known throughout the area as someone whose word is worth something",
    "rarely the first to speak in a room but often the last one people remember",
    "cheerful in a way that is entirely genuine and slightly suspicious to those who have seen more",
    "inclined to give second chances with a generosity that has been repaid perhaps half the time",
    "deeply uncomfortable with praise and inclined to deflect it until it becomes awkward",
    "known for going quiet rather than saying something they would regret",
    "possessed of opinions they keep to themselves until asked, then share entirely",
    "capable of lasting longer than anyone in a dispute of patience and equally capable of losing suddenly",
    "privately sentimental in ways that would embarrass them if stated aloud",
    "given to small routines they maintain with more rigour than strictly necessary",
    "the sort of person other people describe as 'solid' and who finds the word slightly deflating",
    "inclined toward fairness to a degree that occasionally baffles people who are used to something else",
    "more interested in what people do than what they say, and has adjusted their expectations accordingly",
    "known to hold the door and forget the birthday, which describes their priorities fairly well",
    "sharper in writing than in speech and aware of it",
    "rarely bored, which people notice without being entirely sure why",
    "the sort of person who finishes things; it is both a virtue and a tendency that causes friction",
    "possessed of a long memory for kindnesses and an equally long one for the other kind",
    "not easily moved by flattery, which is sometimes mistaken for coldness",
    "inclined to notice things that others overlook and say nothing about them until it matters",
    "given to a particular manner of helping that involves doing the thing rather than discussing it",
    "known to ask questions that seem simple and turn out not to be",
    "the sort of person who is always doing two things at once and rarely doing either badly",
    "given to opinions that arrive late and are often correct",
    "more patient with strangers than with people they know well, which is either a strength or a complaint depending on your position",
    "inclined to understate things in ways that take a moment to land",
    "the sort of person animals approach without being called",
    "known to be harder on themselves than on anyone else, which is not as reassuring as it sounds",
    "given to the sort of helpfulness that doesn't announce itself",
    "possessed of a particular talent for arriving at the moment something needs to be done",
    "more interested in how things work than in what they're called",
    "known to say what they mean and mean what they say, which is rarer than it should be",
    "inclined to ask for help less readily than they offer it",
    "quietly devoted to something — exactly what, they haven't explained",
    "given to unexpected silences in conversations, which some people find thoughtful and others find rude",
    "inclined to form strong attachments slowly and hold them firmly",
    "possessed of the particular confidence of someone who has been underestimated before and remembers it",
    "known to be more consistent in private than in public, which is unusual",
    "given to the kind of humour that doesn't announce itself as humour",
    "not easily rushed, which people either find steadying or maddening",
    "known to make good decisions under pressure and to spend too long on easy ones",
    "the sort of person who apologises once and means it",
    "inclined toward directness in ways that people who don't know them find surprising",
    "given to a specific kind of stubbornness that is indistinguishable from principle",
    "possessed of more inner life than their manner suggests",
    "known to remember the small things people say in passing, which can feel like a gift and occasionally like surveillance",
    "inclined to give advice only when asked, which makes people more likely to ask",
    "the sort of person who doesn't need to be liked but clearly prefers it",
    "given to long periods of quiet productivity that are only visible in their results",
    "known to take the long view on almost everything, including things that probably don't require it",
    "possessed of a genuinely generous spirit that people sometimes mistake for naivety until they have seen what it costs",
    "inclined to take problems apart carefully before deciding what to do about them",
    "the sort of person other people describe as steady, and who would find the word more flattering if they knew how rare it was",
    "given to occasional strong feelings about minor things that they immediately suppress",
    "known to leave situations better than they found them without making a point of it",
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
    "Spent a season digging drainage ditches for a landowner who paid late and poorly, and came away with a specific opinion about certain kinds of people that has never softened.",
    "Was present at the signing of a local trade agreement that later fell apart; knows which party broke it first and has never said publicly.",
    "Once acted as a go-between for two people who couldn't speak to each other directly; the arrangement resolved nothing and cost them a friendship.",
    "Took in a lodger for two winters who turned out to be interesting company and then, abruptly, gone.",
    "Found a purse full of coin once with no name on it; kept half, gave the other half to a family they knew was struggling, and still isn't sure which half they should have kept.",
    "Spent several months working for a family of considerable wealth and came away with specific views on how people of considerable wealth think.",
    "Agreed to testify on behalf of a neighbour in a property dispute and later discovered their account had been more useful to the opposing side.",
    "Survived a cart accident that killed the horse and left them with a limp that mostly went away.",
    "Once walked into a conversation that stopped the moment they entered the room, and has thought about it at odd intervals ever since.",
    "Spent a year corresponding with a relative in another town and only realised after the relative died how much those letters had mattered.",
    "Was offered a job they were not qualified for, accepted it, and managed by asking questions they perhaps should have known the answers to.",
    "Once talked someone out of a decision they regretted making, watched them make it anyway, and resolved to stop talking people out of things.",
    "Was chosen by lot for a civic duty they had no interest in and performed it more carefully than most people perform things they chose.",
    "Learned a skill from an old person who died before they could thank them properly.",
    "Got into a physical altercation once, won, and found it did not make them feel as good as expected.",
    "Took on work during a lean stretch that they were overqualified for and did it without complaint, which people still mention.",
    "Was the last to hear news of something that affected their family directly, and has not entirely forgiven the delay.",
    "Helped an elderly person with a legal matter without being asked; the matter resolved favourably, the thanks was excessive, and they remain quietly embarrassed by both.",
    "Spent a night lost in bad weather and arrived home the next morning and made exactly one change in how they lived.",
    "Was given advice they didn't ask for that turned out to be correct; thanked the person badly in the moment and has been trying to correct that ever since.",
    "Spent two months living off a kind of charity that wasn't called charity and has been very careful about how they extend the same to others since.",
    "Was part of a group that did something unwise together; everyone involved has a slightly different version of what happened.",
    "Watched a mentor's reputation collapse for reasons unrelated to their ability; it changed their understanding of what reputation is and isn't.",
    "Had a period of several years where things went wrong in sequence — not catastrophically, just consistently — and is still working out what it taught them.",
    "Helped dismantle a building that had stood for eighty years and found something hidden in the wall that they put back and told no one about.",
    "Once made a joke at the wrong moment that permanently altered how a room full of people thought of them; has been more careful since.",
    "Travelled to a city once that was larger than anything they had grown up expecting, and came back quieter.",
    "Covered for someone's absence once without being asked and without ever knowing what the absence was for; the person never acknowledged it, which was probably correct.",
    "Was in debt to a person they disliked and found the experience clarifying in ways that pure poverty had not been.",
    "Watched a business their family built for decades close in less than a year; has been studying avoidability ever since.",
    "Spent a winter in a place much colder than home with people much stranger than expected and came back with a kind of patience that wasn't there before.",
    "Was asked to evaluate something whose value they fundamentally misread; the person who asked never told them, which was either kindness or worse.",
    "Inherited a relationship with a creditor they didn't know about along with the rest of an estate; resolved it quietly over seven years.",
    "Once committed to a lie small enough to be forgivable and large enough that it was never practical to correct.",
    "Spent a season working as a messenger and developed a thorough understanding of what people will commit to writing versus what they will not.",
    "Was the only person present at an event with no stake in the outcome and found the experience of watching rather than competing unexpectedly interesting.",
    "Was the first in their family to do a particular thing, and only realised it afterwards.",
    "Spent a week in a town where they knew no one, for no particular reason, and found the anonymity unexpectedly pleasant.",
    "Was given a responsibility they didn't earn in the usual way, worked twice as hard because of it, and resented having to.",
    "Spent a winter as a toll-keeper on a mountain pass and came back with views on solitude that they have never fully unpacked.",
    "Was asked once to witness a document that, in hindsight, they should have read more carefully before signing.",
    "Caught in the middle of a neighbours' dispute years ago and handled it well enough that people still bring them other people's arguments.",
    "Was denied something they had worked toward for years; eventually stopped being angry about it and is still figuring out what replaced the anger.",
    "Spent six months keeping meticulous records of something no one else considered worth tracking; never explained why and the records still exist somewhere.",
    "Nursed a dying relative for eight months at some cost to their own situation, and has never spoken of it as a sacrifice.",
    "Once lied convincingly on behalf of someone who did not deserve the help, and has revised their position on both the lie and the person since.",
    "Made a friend on the road under unusual circumstances; they parted without exchanging names and neither has encountered the other since.",
    "Sold something irreplaceable during a hard year; recovered financially and has not recovered in the other sense.",
    "Was the only person in their family who stayed when the rest of them left, and has had years to work out whether that was loyalty or inertia.",
    "Spent a summer as a hired hand on a farm far from home; the farmer and their family are still the standard against which they measure hospitality.",
    "Was invited into a business arrangement they had serious reservations about, declined politely, and watched it succeed, which has complicated their confidence in their own judgment.",
    "Learned to read late in life from an unlikely teacher and has been quietly grateful ever since.",
    "Was cheated in a transaction once in a way that was entirely legal; the experience refined their understanding of both the law and the people who rely on it.",
    "Lost a close friend to a sudden illness and spent the following year doing everything that friend had put off, without being entirely conscious of why.",
    "Spent two seasons working a mine and came out with a deep and particular respect for underground silence.",
    "Was the subject of an unflattering but accurate piece of local gossip once; the experience improved them in ways the gossips certainly didn't intend.",
    "Helped a stranger locate a family member who had gone missing; they found them, and the reunion was complicated, and they have not volunteered for similar tasks since.",
    "Was offered a position of real responsibility very young, performed adequately, and has been cautious about authority ever since.",
    "Witnessed a moment of significant kindness between strangers once and has thought about it more than most of the things they have personally done.",
    "Left home under difficult circumstances, returned under better ones, and found the place smaller than they remembered in ways that had nothing to do with its actual size.",
]

# Optional early-life detail added to the opening blurb
_CHILDHOOD_DETAILS = [
    "The eldest of several siblings.",
    "The youngest, and treated accordingly.",
    "One of twins; the other did not survive childhood.",
    "Orphaned young and raised by neighbours.",
    "Raised by a grandmother after their parents left for work elsewhere and did not return.",
    "A sickly child who grew into someone considerably more durable than expected.",
    "The only child of older parents who had long given up hoping.",
    "Sent away to a relative at seven and did not return home until grown.",
    "Grew up largely unsupervised, which had both advantages and costs.",
    "One of five; largely indistinguishable from the others until they weren't.",
    "Lost both parents to the same illness in the same winter.",
    "Raised in a household that moved often, for reasons that were never clearly explained.",
    "A quiet child who became a louder adult, or the reverse.",
    "The child of a marriage that everyone in town had opinions about.",
    "Grew up in the trade; could work a full day before most children their age knew what work was.",
    "Spent their childhood in a different region entirely and moved here as an adult.",
    "Raised alongside cousins in a large shared household; privacy was not a feature of early life.",
    "A serious child — never quite understood what the other children found so amusing.",
    "Lost a sibling young; the shape of that absence is still faintly visible if you know where to look.",
    "Grew up on the road with a family that never stayed anywhere long enough to call it home.",
    "Grew up watching their parents disagree about everything and learned to listen for what was said between the arguments.",
    "The child no one expected to survive infancy, which shaped how people treated them for years.",
    "One of several children all named after the same ancestor, which caused constant confusion and possibly still does.",
    "Grew up in a household that was never quite poor and never quite comfortable, which is a particular kind of education.",
    "The only child old enough to work during the years when the family needed it most.",
    "Grew up above the family's trade and knows exactly what it sounds like when business is good and when it isn't.",
    "Left school young when circumstances required it; the education was unfinished in ways they spent years correcting on their own.",
    "Raised in a household that moved once too often, and learned early to hold things loosely.",
    "Grew up in a family where things were said plainly; has since discovered this is not universal.",
    "The grandchild of the person who built what the family now runs.",
    "Grew up in the shadow of a more accomplished sibling, which is either a complaint or an explanation depending on the day.",
    "A wanted child after many years of hope, which meant growing up with certain expectations attached.",
    "The product of a second marriage, which put them at an angle to certain parts of the family.",
    "Spent their childhood in a place that no longer exists in its old form; the changes happened while they were away.",
    "Grew up in a household where money was treated as something that came and went, which turned out to be accurate.",
    "Was the child of a parent who was often away; filled the time with other things and is still filling it.",
    "Raised alongside the children of the family they worked for, which gave them two different understandings of the same world.",
    None,  # no detail — open bio with birth line directly
    None,
    None,
    None,
]

# Present-day observation closing the bio
_CURRENT_NOTES = [
    "These days they keep mostly to themselves, which suits them.",
    "They seem settled here, or close enough to it that the difference doesn't show.",
    "Lately they have been quieter than usual, and people who know them have noticed.",
    "They have been asking questions about something recently, without saying what.",
    "People describe them as reliable, which is the kind of reputation that takes years to build and seconds to lose.",
    "There is something they are working toward, though they haven't named it to anyone.",
    "They have lived here long enough that most people have stopped wondering where they came from.",
    "Something seems to be weighing on them lately, though they haven't said what.",
    "They are well-regarded here, in the specific way that comes from never having given anyone a reason not to be.",
    "They have fewer friends than acquaintances, and seem comfortable with the distinction.",
    "There is a restlessness to them lately that people who have known them for years say wasn't always there.",
    "They are in the middle of something — exactly what, they are not yet saying.",
    "People come to them with problems, which suggests something about how they are perceived.",
    "They seem to be enjoying a period of relative peace, which they are approaching with appropriate caution.",
    "They know more people here than they let on, and fewer of them well than they would like.",
    "There is a project they have been mentioning for years without making much visible progress on.",
    "They have the particular air of someone who has made their peace with where they ended up.",
    "Something happened recently that shifted their thinking; what it was, they haven't shared.",
    "They are the sort of person others describe as 'good to have around,' which is a different thing from popular.",
    "They have been here long enough to watch things change and have a lot of quiet opinions about how.",
    "There is a letter they have been meaning to write for several years.",
    "They are content, which is something not everyone arrives at.",
    "People trust them without entirely being able to say why, which is perhaps the best kind of trust.",
    "Lately they seem to be watching something without quite looking at it directly.",
    "They have roots here now, or the nearest thing to it.",
    "People describe them as someone who was here before things got complicated, which is accurate.",
    "They have more history in this place than most people walking its streets.",
    "They are in the middle of something, though what exactly isn't clear from the outside.",
    "Something is different about them lately — not worse, exactly, just different.",
    "They seem to be waiting, though it is not obvious for what.",
    "The years have suited them, on balance.",
    "They seem like someone who has recently made a decision and is still deciding if it was right.",
    "People who have known them for years say they haven't changed much, which is probably a compliment.",
    "They have the air of someone who has been through things and is no longer particularly alarmed by most of what comes up.",
    "There is something they are not saying, which is true of most people but somehow more obvious with them.",
    "They seem comfortable here, which may be the most honest thing that can be said.",
    "People go to them with things, which tells you something.",
    "They have been making a specific kind of effort lately that people around them have noticed without fully naming.",
    "The town seems to have grown around them in a way that has left them more central than they intended.",
    "There is a quality of calm about them that suggests something has been resolved, though they haven't said what.",
    "They seem to have arrived at something, though what exactly remains their own business.",
    "People treat them as someone who has earned the right to be direct, which either means they have or they've been getting away with it long enough that it amounts to the same thing.",
    "There is a plan somewhere behind the eyes; it may be modest, or it may not be.",
    "They have lived here long enough to be part of what makes the place what it is.",
    "Something shifted for them some months back; they haven't named it but the change is visible to people who pay attention.",
    "They seem, in an unshowy way, to be doing all right.",
    "People remember what they were like before certain things happened and are quietly rooting for them.",
    "They carry their history quietly enough that it takes time to see how much of it there is.",
    "They are the kind of person a town accumulates and doesn't notice it has until they aren't there.",
    "There is a particular satisfaction about them lately that suggests something is going right.",
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
    "is quietly preparing to leave, and has not told anyone.",
    "has recently said something in anger that they cannot take back and have not apologised for.",
    "is protecting someone else's secret at some ongoing cost to their own reputation.",
    "has been avoiding a conversation for months that is only becoming more necessary.",
    "recently found out something about their own past that changes how they understand several years of their life.",
    "is the only person who knows where something important is, and hasn't decided what to do with that.",
    "has a private agreement with someone in town that would look very different from the outside.",
    "borrowed something years ago that has never been returned and both parties have tacitly agreed not to mention.",
    "was once asked to do something they refused; they are no longer certain they made the right call.",
    "has been quietly accumulating something — money, information, goodwill — without explaining the purpose.",
    "carries a resentment they have never voiced toward someone they see regularly.",
    "did something years ago that they believe no one witnessed, and which they think about more than they expected.",
    "has been offered something that requires them to act against someone they like, and has not yet decided.",
    "suspects they are being watched, without having identified who or why.",
    "knows about an arrangement in town that is not entirely above board and has concluded that knowing is sufficient involvement.",
    "has been keeping a record of something for years and hasn't decided what to do with it.",
    "made a promise to someone who is dead that would complicate their life considerably if honoured.",
    "is aware that someone has the wrong impression of them and hasn't corrected it because the wrong impression is more convenient.",
    "has been receiving messages from someone whose identity they have not shared with anyone.",
    "is quietly in conflict with someone they appear to be on good terms with.",
    "borrowed a sum long ago that has never been spoken of by either party; the original lender has since died.",
    "has been changing their mind about something they said publicly years ago and isn't sure how to handle the gap.",
    "is quietly trying to undo something they did, without it becoming apparent that they are doing so.",
    "carries a specific guilt about the last conversation they had with someone who is no longer alive.",
    "has been approached to do something they haven't refused yet.",
    "knows a person in town is not who they say they are and has decided this is not their problem.",
    "has a plan they haven't told anyone about.",
    "is living at a level of comfort that is slightly better than the truth about their finances would support.",
    "recently found out they were excluded from something they should have been part of.",
    "is quietly angry about something that happened years ago and hasn't finished deciding what, if anything, to do about it.",
    "has been sleeping poorly, which people who know them have noticed.",
    "was once close to someone who is now an enemy of theirs and is unsure which of them is responsible.",
    "is waiting for something to either resolve itself or require a decision.",
    "has been offered something valuable by someone whose motives they don't understand.",
    "knows where a thing is that other people have been looking for.",
    "agreed to something in a difficult moment that they would not agree to now.",
    "has been lying about something so minor and for so long that correcting it has become more complicated than the original lie.",
    "is quietly preparing to leave, and has not told anyone.",
    "recently said something in anger that they cannot take back and have not apologised for.",
    "is protecting someone else's secret at some ongoing cost to their own reputation.",
    "has been avoiding a conversation for months that is only becoming more necessary.",
    "recently found out something about their own past that changes how they understand several years of their life.",
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


# Sentence templates for the opening birth line — {location} and {profession} are filled in
_BIRTH_TEMPLATES = [
    "Born {location}, from a line of {profession}.",
    "Grew up {location}, in a family of {profession}.",
    "Raised {location} — {profession}, like the rest of the family before them.",
    "Came from {location}, with generations of {profession} behind them.",
    "Spent their early years {location}, in a household of {profession}.",
    "From {location}, and from {profession} on both sides.",
    "Their people have been {profession} as long as anyone can remember; they themselves were born {location}.",
    "The trade of {profession} was in the family long before they arrived, {location}.",
    "Born into a household of {profession}, {location}.",
    "Came into the world {location}, the latest in a long line of {profession}.",
    "A family of {profession}, {location} — that is where they come from.",
    "{profession_cap} — that was the trade they were born into, {location}.",
    "The {profession} trade was all anyone in the family had ever done; they were born {location}.",
    "Came up {location}, surrounded by {profession} and unlikely to be anything else.",
    "Everything in the family ran toward {profession}; they were born {location} and learned early.",
]

# Optional vivid specific detail added to the bio (roughly 35% of NPCs)
_NOTABLE_DETAILS = [
    "They keep a small carved figure on their worktable that they have never explained.",
    "They are never without a particular knife that is too good to be a working tool and too worn to be an ornament.",
    "They always sit with their back to the wall, which people attribute to different things.",
    "They have a habit of repeating the last word of a sentence they are thinking over.",
    "They keep their accounts in a personal shorthand that no one else can read.",
    "They are known for a specific gesture they make when they are about to say no.",
    "They have never been seen to write anything down, which either means an excellent memory or something else.",
    "They keep a piece of cloth in their pocket that may once have been something; they have never said what.",
    "They have a scar they explain differently on different occasions, which people have started to find amusing.",
    "They wear a ring that has been too small for their finger for years and have made no apparent move to resolve this.",
    "They have a piece of someone else's handwriting tacked above their door that no one has asked about in years.",
    "They always know what time it is without looking; people have tested this and stopped testing it.",
    "They are known to say goodbye once, quickly, and to find extended partings extremely difficult.",
    "They keep a specific corner of their space meticulously ordered and the rest exactly as it falls.",
    "They are the only person in their trade who uses a left-handed grip, which is technically incorrect and apparently unimportant.",
    "They have lived in the same building long enough that they navigate it without light, which occasionally unsettles visitors.",
    "They are known for bringing food to meetings, unprompted and without explanation.",
    "They have a specific piece of music they hum when working that they are entirely unaware of humming.",
    "They keep a calendar with specific dates circled; no one has been invited to ask about the circled dates.",
    "They are known to send word when they hear that someone's circumstances have changed, which requires keeping track of a great many people's circumstances.",
    "They have never spoken ill of someone who wasn't in the room, which people mention when asked what they're like.",
    "They own a coat so old that replacing it would require them to admit how long they have been wearing it.",
    "They are inexplicably good at gauging weather, which people in agricultural trades have noticed.",
    "They have a particular way of listening — head tilted, hands still — that makes people say more than they intended.",
    "They are known to leave a small useful gift when they stay somewhere, always anonymous.",
    "They are one of the few people in the area who can read well and who do not seem to consider this a credential.",
    "They have a specific place they go when they need to think; people have stopped following them there.",
    "They always refill a cup before they refill their own, which is either courtesy or habit and may be both.",
    "They have a name for a tool that they use privately and, occasionally, out loud by accident.",
    "They carry a list of something — names, debts, tasks — that they consult when no one is looking.",
]

# ---------------------------------------------------------------------------
# Identity generation
# ---------------------------------------------------------------------------

def generate_identity(npc_uid: str, town_id: int, _role: str, world_seed: int) -> dict:
    """Return a stable identity dict for one NPC.

    Keys: first_name, family_name, gender, display_name, blurb, bio, personal_tension
    """
    rng = random.Random(hash((npc_uid, world_seed, "identity")) & 0xFFFFFFFF)

    gender     = rng.choice(("m", "f"))
    first_name = rng.choice(_FIRST_NAMES_M if gender == "m" else _FIRST_NAMES_F)
    family_name = rng.choice(_FAMILY_NAMES)

    qualifier  = rng.choice(_BIRTHPLACE_QUALIFIERS)
    profession = rng.choice(_PROFESSION_LINES)

    from towns import TOWNS
    town_name = TOWNS[town_id].name if town_id in TOWNS else "the region"
    location_phrase = f"{qualifier} {town_name}" if qualifier else f"in {town_name}"

    birth_template = rng.choice(_BIRTH_TEMPLATES)
    birth_line = birth_template.format(
        location=location_phrase,
        profession=profession,
        profession_cap=profession.capitalize(),
    )

    # Optional childhood detail appended to the birth line
    childhood = rng.choice(_CHILDHOOD_DETAILS)
    blurb = f"{birth_line} {childhood}" if childhood else birth_line

    pronoun = "He" if gender == "m" else "She"

    # One or two life events (roughly 50/50)
    events = rng.sample(_LIFE_EVENTS, k=2) if rng.random() < 0.5 else [rng.choice(_LIFE_EVENTS)]
    events_text = " ".join(events)

    trait        = rng.choice(_PERSONAL_TRAITS)
    current_note = rng.choice(_CURRENT_NOTES)
    tension      = rng.choice(_PERSONAL_TENSIONS)

    # Optional vivid detail (~35% of NPCs)
    detail_text = f" {rng.choice(_NOTABLE_DETAILS)}" if rng.random() < 0.35 else ""

    bio = f"{blurb} {events_text} {pronoun} is {trait}.{detail_text} {current_note}"

    return {
        "first_name":       first_name,
        "family_name":      family_name,
        "gender":           gender,
        "display_name":     f"{first_name} {family_name}",
        "blurb":            blurb,
        "bio":              bio,
        "personal_tension": tension,
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


def _inject_plan_dynasty_chronicle(chronicle: dict, world, region_id: int) -> None:
    """Layer the simulated 500-year chronicle onto the dynasty chronicle dict.

    Adds (or replaces):
        kingdom_summary  — one-line "founded in year N; fallen in year M".
        dynasty_arc      — counts of births/deaths/marriages/successions.
        kingdom_events   — list of "Yr N — text" lines for the kingdom.
        dynasty_events   — list of "Yr N — text" lines for the dynasty.
        current_era      — derived from latest significant event.
    """
    plan = world.plan
    kingdom = plan.kingdoms.get(region_id)
    if kingdom is None:
        return
    dyn = plan.dynasties.get(kingdom.dynasty_id)
    if dyn is None:
        return

    if kingdom.fallen_year != -1:
        chronicle["kingdom_summary"] = (
            f"{kingdom.name} stood for {kingdom.fallen_year - kingdom.founded_year} years "
            f"before falling in year {kingdom.fallen_year}."
        )
    else:
        chronicle["kingdom_summary"] = (
            f"{kingdom.name} has endured {plan.history_years - kingdom.founded_year} years."
        )

    k_events = plan.chronicle_for_kingdom(region_id)
    d_events = plan.chronicle_for_dynasty(kingdom.dynasty_id)

    chronicle["kingdom_events"] = [f"Yr {e.year} — {e.text}" for e in k_events]
    chronicle["dynasty_events"] = [f"Yr {e.year} — {e.text}" for e in d_events]

    births = sum(1 for e in d_events if e.kind == "birth")
    deaths = sum(1 for e in d_events if e.kind == "death")
    marriages = sum(1 for e in d_events if e.kind == "marriage")
    successions = sum(1 for e in d_events if e.kind in ("succession", "succession_crisis"))
    crises = sum(1 for e in d_events if e.kind == "succession_crisis")
    extinct = " The line ended in turmoil." if dyn.extinct_year != -1 else ""
    chronicle["dynasty_arc"] = (
        f"Across {plan.history_years} years: {births} births, {marriages} unions, "
        f"{deaths} deaths, {successions} successions ({crises} contested).{extinct}"
    )

    significant = [e for e in k_events
                   if e.kind in ("sack", "annex", "merge", "kingdom_collapse",
                                 "defeat_kingdom", "earthquake", "plague",
                                 "famine", "found_settlement", "extinction",
                                 "succession_crisis")]
    if significant:
        latest = significant[-1]
        chronicle["current_era"] = (
            f"In recent memory: {latest.text} (year {latest.year})."
        )


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
            world=world,
        )
        # Inject the actual 500-year sim chronicle for this kingdom + dynasty.
        if getattr(world, "plan", None) is not None:
            _inject_plan_dynasty_chronicle(chronicle, world, region_id)

        # Compute court visual attributes for this region
        from cities import PALACE_TYPES
        capital = TOWNS.get(region.capital_town_id)
        court_palace_type = ""
        if capital:
            palace_left = capital.center_bx + capital.half_w + 4
            court_palace_type = random.Random(
                palace_left ^ world_seed ^ 0xCAFEBABE
            ).choice(PALACE_TYPES)

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
            npc.leader_color = region.leader_color
            npc.palace_type  = court_palace_type
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
