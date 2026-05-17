"""Knightly Orders — procedural per-region chivalric factions.

Each Region in the world gets 1-2 KnightlyOrders at worldgen. Orders own a
roster of named knights, a CoatOfArms (reuses heraldry.py), a motto, a
chivalric tradition (errant, templar, mercenary, ...), a chapter-house seat,
sworn vows, and a prestige score that rises as their members win tournaments.
Each knight holds a rank within the order (Squire -> Grandmaster).

Mirrors the lazy-seeding pattern used by guild_worldgen.seed_guilds: the public
entry point `seed_knightly_orders(world)` is idempotent and safe to call after
load.
"""

import random
from dataclasses import dataclass, field
from typing import Optional

import heraldry


# ---------------------------------------------------------------------------
# Registries — module-level singletons, just like GUILDS / OUTPOSTS
# ---------------------------------------------------------------------------

ORDERS: dict = {}        # order_id -> KnightlyOrder
KNIGHTS: dict = {}       # knight_id -> Knight
_NEXT_ORDER_ID  = 1
_NEXT_KNIGHT_ID = 1


# ---------------------------------------------------------------------------
# Per-biome-group name pools — a desert region produces different orders than
# a boreal one. Keep these short and evocative.
# ---------------------------------------------------------------------------

KNIGHTLY_ORDER_NAME_POOLS = {
    "forest":        ["Stag", "Oak", "Wolf", "Bear", "Briar", "Greenwood", "Antler"],
    "boreal":        ["Frost Wolf", "White Bear", "North Star", "Ice Hawk", "Hoarfrost", "Pine"],
    "jungle":        ["Jaguar", "Serpent", "Vine", "Sun Parrot", "Emerald Toad", "Canopy"],
    "tropical":      ["Coral", "Tide", "Palm", "Flame Bird", "Lagoon", "Salt Wind"],
    "mediterranean": ["Olive", "Falcon", "Galley", "Argent Sun", "Cypress", "Vermilion"],
    "coastal":       ["Anchor", "Gull", "Wave", "Pearl", "Driftwood", "Salt Star"],
    "desert":        ["Scorpion", "Dune", "Phoenix", "Crescent", "Sandstone",
                      "Black Sun", "Saffron Wind", "Quartz Star"],
    "steppe":        ["Stallion", "Comet", "Hawk", "Tall Grass", "Bronze Bow",
                      "Open Sky", "Iron Mare", "Nine Banners", "Wolf Moon"],
    "east_asian":    ["Cherry Blossom", "Crane", "Bamboo", "Lotus", "Tiger Claw",
                      "Jade", "Pine Wind", "Black Lacquer", "Mountain Mist"],
    "levant":        ["Cedar", "Lion", "Pomegranate", "Star of Dawn", "Saffron",
                      "Brass Gate", "Olive Crescent", "Date Palm"],
    "wasteland":     ["Black Vulture", "Ash", "Broken Crown", "Rust", "Cracked Bell"],
    "highlands":     ["Eagle", "Thistle", "Mountain", "Iron Stag", "Glen", "Tarn"],
    # New cultural groups
    "silk_road":     ["Caravan Hawk", "Sky Tug", "Salt Comet", "White Camel",
                      "Bronze Bow", "Nine Banners"],
    "arabia":        ["Crescent", "Saffron Wind", "Falcon", "Date Palm",
                      "Black Tent", "Empty Quarter"],
    "persia":        ["Winged Lion", "Sun-Disc", "Peacock", "Cedar Throne",
                      "Lapis Rose", "Iron Stallion", "Mithra's Flame"],
    "south_asian":   ["Tiger", "Lotus", "Vermilion Sun", "Sandalwood",
                      "Twin Moons", "Sandstone Lion", "Saffron Banner"],
    "yunnan":        ["Jade Pass", "Mist Crane", "Tea Tiger", "Bamboo Wind",
                      "River Dragon", "Stone Lantern"],
}
_DEFAULT_NAME_POOL = ["Lion", "Dragon", "Rose", "Sword", "Crown", "Tower"]

# Templates picked by tradition. {x} is filled from the biome pool above.
_NAME_TEMPLATES_BY_TRADITION = {
    "errant":       ["Order of the {x}", "Wandering {x}", "The {x} Errant"],
    "templar":      ["Sacred Order of the {x}", "Templars of the {x}", "Holy {x}"],
    "hospitaller":  ["Hospital of the {x}", "Almoners of the {x}", "Mercy of the {x}"],
    "cavalier":     ["Royal Order of the {x}", "King's {x}", "Crown {x}"],
    "mercenary":    ["The {x} Company", "Free Lances of the {x}", "{x} Free Sword"],
    "marcher":      ["Marchers of the {x}", "Wardens of the {x}", "{x} Border-Watch"],
    "magisterial":  ["Scholar-Knights of the {x}", "Conclave of the {x}", "Quill and {x}"],
    "berserker":    ["{x} Bloodsworn", "Howling {x}", "The {x} Wrath"],
    "horde":        ["{x} Horde", "Riders of the {x}", "Sons of the {x}",
                     "Tug of the {x}"],
    "cataphract":   ["{x} Cataphracts", "Iron Lances of the {x}",
                     "Sun-Court {x}"],
    "bushi":        ["Brotherhood of the {x}", "{x} Bushi",
                     "Vassals of the {x}", "House of the {x}"],
    "furusiyya":    ["Faris of the {x}", "{x} Mamluk",
                     "Riders of the {x} Crescent"],
    "rajput":       ["{x} Rajputs", "Sons of the {x}", "Garh of the {x}"],
}

KNIGHTLY_CHARGE_POOL = ["lance", "gauntlet", "helmet", "sword", "rose",
                        "lion", "dragon", "stag", "eagle", "cross"]


# ---------------------------------------------------------------------------
# Tradition profiles — drive almost every flavor decision for an order.
# ---------------------------------------------------------------------------

ORDER_TRADITIONS = {
    "errant": {
        "desc": "Roaming knights bound by personal honor, beholden to no crown.",
        "motto_pool": ["The road is my hall.", "Sworn to none, true to all.",
                       "Honor outlives the saddle."],
        "vow_pool": ["No hearth two nights running.",
                     "Refuse no honest duel.",
                     "Carry word for the wronged."],
        "patron_pool":   ["the Lone Rider", "Saint Aldric of the Long Road",
                          "the Hooded Pilgrim", "the Twin Moons"],
        "relic_pool":    ["Splintered Lance", "Mended Saddle", "Wayfarer's Spur",
                          "Hooded Sigil"],
        "doctrine_pool": ["Honor before lord", "The road provides",
                          "Wander, never settle"],
        "quirk_pool":    ["sleeps in the saddle", "speaks to no nobles",
                          "carries a stranger's letter",
                          "swears each oath in a new tongue"],
        "kit_weights":   {"lancer": 3, "champion": 2, "squire_elect": 2},
        "skill_bias":    0.00,
        "prestige_bias": -5,
        "aim_bias":      (1, 1, 1),
        "battle_cry":    "Honor and the road!",
        "pre_charge_ritual": "draws a single line in the dust with the lance-tip and salutes no one in particular",
    },
    "templar": {
        "desc": "A consecrated brotherhood that fights in the name of a chosen saint.",
        "motto_pool": ["Steel sanctified.", "By faith, by fire.",
                       "The saint's hand is our own."],
        "vow_pool": ["Daily prayer at dawn and dusk.",
                     "No coin shall enter the chapter house.",
                     "Bury every fallen foe with rites."],
        "patron_pool":   ["Saint Mira the Unburnt", "the Sevenfold Star",
                          "Saint Yorath of the Vigil", "the Pale Lamb"],
        "relic_pool":    ["Sanctified Cross", "Censer of the Vigil",
                          "Burning Hymn", "Saint's Knucklebone"],
        "doctrine_pool": ["Faith above flesh", "The saint commands the blade",
                          "Bear witness, then strike"],
        "quirk_pool":    ["fasts before every joust", "wears a hair shirt",
                          "blesses every horse before mounting",
                          "carries scripture beneath the gorget"],
        "kit_weights":   {"champion": 4, "lancer": 2, "squire_elect": 1},
        "skill_bias":    0.05,
        "prestige_bias": 15,
        "aim_bias":      (3, 2, 1),   # strike high — symbolic blow to the helm
        "battle_cry":    "Deus vult!",
        "pre_charge_ritual": "kneels for a silent paternoster, then crosses the lance with the chaplain's blessing",
    },
    "hospitaller": {
        "desc": "Knights who guard the sick and shelter pilgrims along hard roads.",
        "motto_pool": ["The wounded come first.", "Healing is also a sword.",
                       "We march so others may rest."],
        "vow_pool": ["Turn no traveler from the gate.",
                     "Strike only after the warning.",
                     "Tithe a tenth of every purse to the poor."],
        "patron_pool":   ["Saint Petra of the Almoner's Gate", "the Mended Hand",
                          "Saint Loren the Bandager", "the White Lily"],
        "relic_pool":    ["Almoner's Cup", "Pilgrim's Cloak", "Knotted Rope",
                          "Mortar and Pestle"],
        "doctrine_pool": ["Mercy first, then steel",
                          "No one falls untended",
                          "Tithe to the road"],
        "quirk_pool":    ["binds his own opponents' wounds",
                          "never strikes the first blow",
                          "rides a mule between bouts",
                          "kneels to no titled lord"],
        "kit_weights":   {"squire_elect": 3, "champion": 3, "lancer": 1},
        "skill_bias":    -0.05,
        "prestige_bias": 10,
        "aim_bias":      (1, 3, 2),   # body — clean unhorsings, not maiming
        "battle_cry":    "Mercy and the lily!",
        "pre_charge_ritual": "blesses a vial of oil for any opponent's wounds before lowering the lance",
    },
    "cavalier": {
        "desc": "Household knights of a regional crown — gilded, proud, well-funded.",
        "motto_pool": ["Crown before all.", "Loyalty, never coin.",
                       "We ride at the king's word."],
        "vow_pool": ["Wear the royal colors on every march.",
                     "Refuse no summons of the throne.",
                     "Never raise the lance against a sovereign."],
        "patron_pool":   ["the Gilded Stag", "King Eowin the Steadfast",
                          "the Argent Crown", "Queen Rhea of the Marches"],
        "relic_pool":    ["Coronation Cloak", "Royal Gauntlet",
                          "Banner of the First Lance", "Gilded Spur"],
        "doctrine_pool": ["The crown is our compass",
                          "Glory is the throne's tithe",
                          "Pageant is policy"],
        "quirk_pool":    ["wears three sashes at all times",
                          "refuses to ride without trumpets",
                          "polishes his greaves before every meal",
                          "addresses every squire as 'cousin'"],
        "kit_weights":   {"champion": 4, "lancer": 3, "squire_elect": 1},
        "skill_bias":    0.10,
        "prestige_bias": 25,
        "aim_bias":      (4, 2, 1),   # high — for the crowd
        "battle_cry":    "For the Crown and the Stag!",
        "pre_charge_ritual": "raises the royal pennant high, waits for the trumpets, then salutes the king's box",
    },
    "mercenary": {
        "desc": "Free companies who sell their lances by the season.",
        "motto_pool": ["Coin clears the field.", "Paid, but never bought.",
                       "Our contract is our creed."],
        "vow_pool": ["No campaign without contract.",
                     "Split every purse evenly.",
                     "Leave no comrade unburied or unpaid."],
        "patron_pool":   ["the Iron Purse", "Captain Vance the Untaxed",
                          "the Three Coins", "the Last Buyer"],
        "relic_pool":    ["Tally Ledger", "Iron Strongbox", "Severed Banner",
                          "Splintered Contract"],
        "doctrine_pool": ["The blade is the bill",
                          "No charity, no waste",
                          "Loyal to the season"],
        "quirk_pool":    ["counts coin between passes",
                          "names every horse for a debtor",
                          "renegotiates mid-march",
                          "always demands payment in advance"],
        "kit_weights":   {"lancer": 3, "champion": 3, "squire_elect": 1},
        "skill_bias":    0.05,
        "prestige_bias": -10,
        "aim_bias":      (1, 4, 2),   # body — efficient, no flourish
        "battle_cry":    "Steel and silver! No charity, no waste!",
        "pre_charge_ritual": "checks the contract one last time and tightens the pay-purse on the saddle",
    },
    "marcher": {
        "desc": "Border wardens hardened by frontier raids and long winters.",
        "motto_pool": ["Hold the line.", "The border is the bone.",
                       "Watch the dark, hold the dawn."],
        "vow_pool": ["Patrol the marches twice a moon.",
                     "Light the beacons at first alarm.",
                     "Take no captive that cannot ride."],
        "patron_pool":   ["the Watchful Eye", "Warden Drust the Unmoving",
                          "the Twin Beacons", "the Long Pass"],
        "relic_pool":    ["Beacon Iron", "Frontier Banner",
                          "Scarred Watch-Horn", "Boundary Stone"],
        "doctrine_pool": ["Hold the line, always",
                          "Vigilance is virtue",
                          "Trust no road after dusk"],
        "quirk_pool":    ["sleeps in armor by habit",
                          "lights a beacon at every camp",
                          "names her sword 'Watch'",
                          "never sits with his back to a gate"],
        "kit_weights":   {"lancer": 4, "champion": 2, "squire_elect": 2},
        "skill_bias":    0.05,
        "prestige_bias": 0,
        "aim_bias":      (1, 3, 3),   # body and low — break the saddle
        "battle_cry":    "Hold the line! Hold the dawn!",
        "pre_charge_ritual": "lights a small beacon-flame at the rail and salutes the watch-tower behind",
    },
    "magisterial": {
        "desc": "Scholar-knights who debate by day and drill by lamplight.",
        "motto_pool": ["Wisdom edges the blade.", "Read, then ride.",
                       "The library is the armory."],
        "vow_pool": ["Copy one page of scripture each week.",
                     "Speak truth, even to one's lord.",
                     "Settle disputes by argument before steel."],
        "patron_pool":   ["the Inkwell Saint", "Magister Hale of the Cloister",
                          "the Quill and Buckler", "the Twin Folios"],
        "relic_pool":    ["Annotated Codex", "Reading Stone",
                          "Quill of Wynhold", "Lamp of Long Nights"],
        "doctrine_pool": ["Think before charge",
                          "Every blow is a thesis",
                          "Knowledge of the tilt"],
        "quirk_pool":    ["recites poetry mid-charge",
                          "carries three books in the saddlebag",
                          "names every lance after a philosopher",
                          "argues judgments with the marshal"],
        "kit_weights":   {"squire_elect": 4, "champion": 2, "lancer": 1},
        "skill_bias":    -0.05,
        "prestige_bias": 5,
        "aim_bias":      (2, 3, 2),   # balanced; technical
        "battle_cry":    "Cogito, ergo lanceo!",
        "pre_charge_ritual": "consults the wind-stick angle and adjusts the lance grip by a finger-breadth",
    },
    "berserker": {
        "desc": "Battle-mad lancers who count scars instead of titles.",
        "motto_pool": ["Forward, always forward.", "First to charge, last to fall.",
                       "Pain is the only herald."],
        "vow_pool": ["Refuse no challenge once shouted.",
                     "Drink no water before a charge.",
                     "Bear every scar uncovered."],
        "patron_pool":   ["the Red Wolf", "Old Tavin Many-Scarred",
                          "the Howling Moon", "the Broken Antler"],
        "relic_pool":    ["Bloodied Helm", "Notched Tooth",
                          "Howl-Drum", "Splintered Rib of the Founder"],
        "doctrine_pool": ["Charge first, count after",
                          "Pain proves the man",
                          "No second wind, only the first"],
        "quirk_pool":    ["screams through the entire charge",
                          "removes the great-helm before impact",
                          "refuses to wear a gorget",
                          "drinks blood-wine before the lists"],
        "kit_weights":   {"lancer": 5, "champion": 2, "squire_elect": 1},
        "skill_bias":    0.00,
        "prestige_bias": -5,
        "aim_bias":      (3, 3, 1),   # high/mid — drama over precision
        "battle_cry":    "First to charge! Last to fall!",
        "pre_charge_ritual": "drinks blood-wine from the founder's horn and roars until the trumpets answer",
    },
    "horde": {
        "desc": "Steppe horse-archers bound by clan, not crown — fast, light, "
                "and pitiless in pursuit. The line bends, breaks, and folds "
                "back on you before you have read the wind.",
        "motto_pool": ["The sky is our roof.",
                       "We ride; the rest stay still.",
                       "Strike, then ride; ride, then strike.",
                       "The grass remembers every hoof.",
                       "Wherever the horse drinks, the clan camps.",
                       "An arrow loosed in flight is worth two on the ground."],
        "vow_pool": ["Never sleep beneath a stone roof.",
                     "Share every kill with the clan-fire.",
                     "Bury no rider without their horse.",
                     "Speak the names of seven ancestors before each ride.",
                     "Pour the first cup of kumis on the earth.",
                     "Strike no cousin save in formal duel.",
                     "Take no plunder the clan has not first divided."],
        "patron_pool":   ["the Eternal Sky", "the Iron Mare",
                          "Old Mother Tengri", "the Nine White Horses",
                          "the Wolf Beneath the Comet",
                          "Burqan Khaldun the Holy Mountain",
                          "the Black Sulde-Spirit",
                          "the Twin Comets of the Founding"],
        "relic_pool":    ["Ancestral Composite Bow", "Tasseled Tug-Banner",
                          "Silver Stirrup of the Founder",
                          "Felt of a Hundred Winters", "Mare's-Milk Drum",
                          "Nine-Tail Standard", "Birch-Bark Quiver",
                          "Salted Saddle of the First Ride"],
        "doctrine_pool": ["Speed before steel",
                          "Clan above khan",
                          "Strike the saddle, not the man",
                          "Feigned flight is also victory",
                          "The bow before the blade"],
        "quirk_pool":    ["speaks to every horse by name",
                          "never sleeps indoors",
                          "carries seven arrows for seven ancestors",
                          "drinks fermented mare's milk before a charge",
                          "refuses to dismount before nightfall",
                          "wears the tail of a wolf on the saddle",
                          "knots a hair from each warhorse into the bridle",
                          "navigates by Polaris even in daylight",
                          "speaks no name of the dead until the year is out"],
        "kit_weights":   {"lancer": 3, "squire_elect": 4, "champion": 1},
        "skill_bias":    0.05,
        "prestige_bias": 5,
        "aim_bias":      (1, 2, 4),   # low — strike the saddle, unhorse the mount
        "battle_cry":    "Uragsh! Uragsh!",
        "pre_charge_ritual": "raises the nine-tail standard and calls each rider's clan name in turn",
    },
    "cataphract": {
        "desc": "Mailed riders on mailed horses — the weight of a falling tower "
                "on the tip of a kontos. They do not skirmish; they break lines.",
        "motto_pool": ["The charge is our prayer.",
                       "Iron upon iron, until none stand.",
                       "We are the wall that moves.",
                       "The sun behind, the lance before.",
                       "We do not retreat — we reform.",
                       "Where the kontos points, the world bends."],
        "vow_pool": ["Never dismount before sunset.",
                     "Pray toward the rising sun each dawn.",
                     "Carry no blade lighter than your saddle.",
                     "Refuse no charge once the line is drawn.",
                     "Polish the scale before sleep, every night.",
                     "Take no enemy banner without saluting it first.",
                     "Speak the throne-name only on the battlefield."],
        "patron_pool":   ["the Sun-King Mithra", "the Winged Lion of Persepolis",
                          "Shapur the Unbroken", "the Gilded Peacock",
                          "the Throne of Flames",
                          "Anahita of the Bright Waters",
                          "the Sassanid Eagle", "the Burning Wheel of Cyrus"],
        "relic_pool":    ["Gilded Scale Hauberk", "Peacock Pennant",
                          "Kontos of the First Charge",
                          "Sun-Disc Chamfron", "Cedar-Throne Shard",
                          "Throne-Forged Klivanion", "Lion-Head Pommel",
                          "Annointed Stirrup of Persepolis"],
        "doctrine_pool": ["The weight of the charge decides all",
                          "Iron is our prayer-rope",
                          "The sun rises behind our line",
                          "Form, charge, reform — never break",
                          "Scale shields scale, lance answers lance"],
        "quirk_pool":    ["never speaks before sunrise",
                          "polishes scale by lamplight",
                          "names her warhorse for an emperor",
                          "wears two cloaks even in summer",
                          "refuses food off-horse",
                          "sleeps facing the rising sun",
                          "never sheathes the kontos in the same hour as drawing",
                          "salts the bridle each morning",
                          "speaks Greek and Pahlavi in alternating sentences"],
        "kit_weights":   {"champion": 5, "lancer": 4, "squire_elect": 1},
        "skill_bias":    0.08,
        "prestige_bias": 15,
        "aim_bias":      (4, 2, 1),   # crash high — break the helm
        "battle_cry":    "Mithra! The Sun-Wheel turns!",
        "pre_charge_ritual": "salutes the rising sun with kontos lowered, then locks the line shield to shield",
    },
    "bushi": {
        "desc": "Sworn retainers of a great house, bound by ancestral duty and "
                "the long blade. The lord's name is their first word at dawn "
                "and their last at the post.",
        "motto_pool": ["Duty above breath.",
                       "The blade does not boast.",
                       "Seven steps, then strike.",
                       "The cherry falls — so do we.",
                       "One cut. One word. One lord.",
                       "Bushido is the road, not the destination."],
        "vow_pool": ["Speak no idle words at the post.",
                     "Refuse no duel offered with respect.",
                     "Eat nothing the lord has not first tasted.",
                     "Practice the cut at every dawn.",
                     "Compose a death-poem before each campaign.",
                     "Sit lower than the lord, always.",
                     "Carry the wakizashi even in the bath-house."],
        "patron_pool":   ["the Mountain Wind", "Ancestor of the Long Sword",
                          "the Crane of the Eastern Pass",
                          "Lord of the Cherry Blossom",
                          "the Old Bushi Hayato",
                          "Hachiman, Kami of War",
                          "the Tiger of Echizen Province",
                          "the Pine-Wind of Mount Kōya"],
        "relic_pool":    ["Heirloom Katana", "Lacquered Helm of the Founder",
                          "Folded Banner of Seven Battles",
                          "Tea-Bowl of First Vassalage",
                          "Mon-Crested Naginata",
                          "Ancestral Mon-Banner",
                          "Sashimono of Seven Generations",
                          "Black-Lacquered Sageo Cord"],
        "doctrine_pool": ["Duty above breath",
                          "The cut is the word",
                          "Loyalty outlives the lord",
                          "One blade, one cut, one truth",
                          "Bear shame, never disgrace"],
        "quirk_pool":    ["bows to every blade before sheathing it",
                          "writes a death-poem each new moon",
                          "speaks no idle words for a full day",
                          "refuses food before duels",
                          "carries a comb beside the wakizashi",
                          "practices a single cut a thousand times before dawn",
                          "drinks tea in silence after a kill",
                          "refuses to remove his sandals at any meal",
                          "names every blade for an ancestor"],
        "kit_weights":   {"champion": 4, "lancer": 2, "squire_elect": 2},
        "skill_bias":    0.07,
        "prestige_bias": 20,
        "aim_bias":      (3, 3, 1),   # high/mid clean
        "battle_cry":    "Tenka, ware ni ari!",
        "pre_charge_ritual": "kneels for one breath, recites the lord's name, then rises to draw the long blade",
    },
    "furusiyya": {
        "desc": "Masters of horse, bow, and sabre — schooled in the art of war "
                "as both science and faith. The madrasa drills run from before "
                "dawn until the call to evening prayer.",
        "motto_pool": ["Skill is the truer steel.",
                       "The horse, the bow, the sword — and then the man.",
                       "We are trained as the sword is forged.",
                       "Three arts, one rider.",
                       "The crescent rises over the schooled hand.",
                       "Better one stroke perfected than a hundred attempted."],
        "vow_pool": ["Recite a verse before every charge.",
                     "Master the bow before the blade.",
                     "Tend your own horse — never leave it to a groom.",
                     "Refuse no traveler the cup.",
                     "Pray five times even on the march.",
                     "Tithe a share of every spoil to the school.",
                     "Pass the discipline to one student before death."],
        "patron_pool":   ["the Falcon Prince", "Sayyid of the Crescent",
                          "the Saffron-Gate Saint",
                          "the Mare of the First Charge",
                          "Khalid of the Long Lance",
                          "Ali of the Two-Pointed Sword",
                          "the Crescent over Damascus",
                          "Saladin's Shadow"],
        "relic_pool":    ["Damascened Sabre", "Crescent Pennant",
                          "Prayer-Rope of the Master",
                          "Saffron-Dyed Saddle-Cloth",
                          "Recurve of the Founder",
                          "Master's Lance of Twelve Notches",
                          "Astrolabe of the Cavalry-Madrasa",
                          "Mamluk Brand-Iron"],
        "doctrine_pool": ["Skill is the truer steel",
                          "Horse, bow, blade — in that order",
                          "The schooled hand strikes thrice",
                          "Mercy after, never during",
                          "Faith above the saddle, science within it"],
        "quirk_pool":    ["recites verse mid-charge",
                          "shoots the bow blindfolded once a moon",
                          "never raises voice to the squire",
                          "trains the horse before the sword each day",
                          "refuses gold from any non-soldier",
                          "studies the stars on every march",
                          "salts the lance-tip before tournaments",
                          "carries an astrolabe in the saddlebag",
                          "fasts on the day of every charge"],
        "kit_weights":   {"lancer": 3, "champion": 3, "squire_elect": 2},
        "skill_bias":    0.05,
        "prestige_bias": 10,
        "aim_bias":      (2, 3, 2),   # versatile
        "battle_cry":    "Allahu sayfuna! The Crescent rides!",
        "pre_charge_ritual": "recites a verse of the school's founder while running a thumb along the sabre's edge",
    },
    "rajput": {
        "desc": "Warrior caste sworn to glory — first into the breach, last out, "
                "and never in retreat. To turn the back is to lose the caste; "
                "to fall facing forward is to win it forever.",
        "motto_pool": ["Death before the back is turned.",
                       "The sun and the moon are our witnesses.",
                       "Glory is the only road home.",
                       "We are born to break the line.",
                       "Saffron above, vermilion within.",
                       "The Rana's word — once given — is iron."],
        "vow_pool": ["Never retreat from a drawn blade.",
                     "Touch the earth before each charge.",
                     "Honor every challenge from a peer.",
                     "Wear the vermilion only on the day of battle.",
                     "Speak the founder's lineage at every dawn.",
                     "Marry within the caste or not at all.",
                     "Take a wound rather than refuse hospitality."],
        "patron_pool":   ["Surya of the Burning Wheel",
                          "the Twin Tigers of the South",
                          "the Lotus Throne of Vijayagarh",
                          "Old Rana Hari the Unyielding",
                          "the Sun-and-Moon Banner",
                          "Durga of the Ten Arms",
                          "Hanuman the Unfallen",
                          "the Sandalwood Sage of Chittor"],
        "relic_pool":    ["Gold-Hilted Tulwar", "Vermilion Banner",
                          "Tiger-Claw Gauntlet",
                          "Lotus Seal of the First Rana",
                          "Sun-Disc Shield",
                          "Saffron Sash of the Last Charge",
                          "Khanda of the Founder",
                          "Rudraksha-Bead Rosary"],
        "doctrine_pool": ["No retreat, no surrender",
                          "Glory is the only road",
                          "The line breaks before we do",
                          "Death is the price of caste",
                          "Saffron at dawn, blood by noon"],
        "quirk_pool":    ["paints vermilion on the helm at dawn",
                          "refuses to sit in any chair lower than the lord",
                          "wears a turban no enemy has loosened",
                          "speaks only of the present war",
                          "carries a coil of saffron thread",
                          "ties a fresh marigold to the saddle every dawn",
                          "fasts the day after every kill",
                          "speaks the founder's name before each name they utter",
                          "sleeps with the tulwar across the chest"],
        "kit_weights":   {"champion": 4, "lancer": 3, "squire_elect": 1},
        "skill_bias":    0.07,
        "prestige_bias": 20,
        "aim_bias":      (3, 3, 2),   # aggressive
        "battle_cry":    "Jai Surya! Jai Rana!",
        "pre_charge_ritual": "paints a saffron stripe across the helm and touches the earth with both palms",
    },
}

# Some traditions naturally fit certain regions. Soft bias — never a hard lock.
_TRADITION_BIAS_BY_GROUP = {
    "forest":        ["errant", "marcher", "hospitaller"],
    "boreal":        ["marcher", "berserker", "errant"],
    "jungle":        ["berserker", "errant", "hospitaller"],
    "tropical":      ["hospitaller", "cavalier", "mercenary"],
    "mediterranean": ["cavalier", "templar", "magisterial"],
    "coastal":       ["hospitaller", "mercenary", "errant"],
    "desert":        ["furusiyya", "templar", "marcher", "mercenary"],
    "steppe":        ["horde", "horde", "berserker", "mercenary"],
    "east_asian":    ["bushi", "bushi", "magisterial", "cavalier"],
    "levant":        ["furusiyya", "templar", "hospitaller", "cavalier"],
    "wasteland":     ["mercenary", "berserker", "horde", "marcher"],
    "highlands":     ["marcher", "errant", "berserker"],
    # New cultural groups
    "silk_road":     ["horde", "cataphract", "mercenary", "furusiyya"],
    "arabia":        ["furusiyya", "furusiyya", "marcher", "mercenary"],
    "persia":        ["cataphract", "cataphract", "magisterial", "cavalier"],
    "south_asian":   ["rajput", "rajput", "magisterial", "templar"],
    "yunnan":        ["bushi", "rajput", "horde", "magisterial"],
}


# ---------------------------------------------------------------------------
# Seat / chapter-house naming
# ---------------------------------------------------------------------------

_SEAT_TYPES_BY_TRADITION = {
    "errant":       ["Way-House", "Hostel", "Hedge-Hall"],
    "templar":      ["Chapter House", "Sanctum", "Holy Keep"],
    "hospitaller":  ["Almonry", "Pilgrim's Rest", "Brother-House"],
    "cavalier":     ["Royal Hall", "Court Keep", "King's Stable"],
    "mercenary":    ["Lance Camp", "Pay-Yard", "Free Hall"],
    "marcher":      ["Watch-Keep", "March-Tower", "Beacon Fort"],
    "magisterial":  ["Library Keep", "Scholar's Hall", "Inkwell Cloister"],
    "berserker":    ["Howl-Hall", "Bloody Keep", "Red Hearth"],
    "horde":        ["Ordu", "Felt-Tent Camp", "Tug-Hall", "Clan-Fire"],
    "cataphract":   ["Iron Stable", "Lion-Gate", "Sun Court", "Cedar Throne"],
    "bushi":        ["Dojo", "Cherry Keep", "Castle Hold", "Mon-House"],
    "furusiyya":    ["Madrasa", "Saddle-House", "Faris Court", "Crescent Hall"],
    "rajput":       ["Garh", "Mahal", "Tiger Fort", "Sun-Throne"],
}
_SEAT_LOCATIONS_BY_GROUP = {
    "forest":        ["Greenhollow", "Oakmere", "Briarfall", "Stagford"],
    "boreal":        ["Hoarfen", "Northwatch", "Whitepine", "Frostgate"],
    "jungle":        ["Vinehold", "Sunmaw", "Jade Falls", "Greenmaw"],
    "tropical":      ["Saltcove", "Palmreach", "Coralside", "Tideford"],
    "mediterranean": ["Olivara", "Cypressholm", "Vermilion", "Argent Bay"],
    "coastal":       ["Driftmouth", "Gullport", "Saltrun", "Pearlbridge"],
    "desert":        ["Sandstone", "Black Dune", "Crescent Hold", "Sunblight"],
    "steppe":        ["Tallgrass", "Brass Comet", "Stallion's Cross", "Long Sky",
                      "Nine-Banner Ford", "Wolf-Moon Plain"],
    "east_asian":    ["Jade Reach", "Crane Pass", "Bamboo Court", "Lotus Way",
                      "Black Lacquer Hold"],
    "levant":        ["Cedarfall", "Saffron Gate", "Pomegranate Hill", "Brass Reach"],
    "wasteland":     ["Rustmire", "Ashfen", "Cracked Bell", "Brokencrown"],
    "highlands":     ["Thistleburn", "Stagcrag", "Irongarth", "Tarnfoot"],
    # New cultural groups
    "silk_road":     ["Bukhara", "Samarkand", "Kashgar", "Khotan", "Salt-Caravan Ford"],
    "arabia":        ["Najd Wells", "Empty Quarter", "Crescent Oasis",
                      "Saffron Sands", "Black-Tent Plain"],
    "persia":        ["Persepolis", "Pasargadae", "Lion Gate", "Sun Court",
                      "Cedar Throne"],
    "south_asian":   ["Vijayagarh", "Sandalwood Hill", "Tiger Reach",
                      "Lotus Fort", "Vermilion Pass"],
    "yunnan":        ["Jade Pass", "Mist Gorge", "Tea Terrace",
                      "Crane Canyon", "Stone-Lantern Ridge"],
}
_DEFAULT_SEAT_LOCATIONS = ["Highgate", "Stonemarsh", "Greycross", "Foxhollow"]


# ---------------------------------------------------------------------------
# Knight ranks — exactly one Grandmaster per order, then a tapered hierarchy.
# ---------------------------------------------------------------------------

KNIGHT_RANKS = [
    # (rank_name, skill_floor, skill_ceiling)
    ("Squire",           0.70, 0.90),
    ("Knight-Errant",    0.85, 1.05),
    ("Knight-Banneret",  1.00, 1.20),
    ("Marshal",          1.10, 1.30),
    ("Grandmaster",      1.25, 1.40),
]

# Cultural rank labels — display-only. Canonical Knight.rank string stays
# European so existing save data and rank-roster code don't change. The codex
# and bracket UI calls cultural_rank_label(tradition, rank) at render time.
# Cultural ritual layer — kept separate from ORDER_TRADITIONS so editing one
# does not balloon the other. Every tradition has one entry. Codex UI calls
# the order_* helpers below to surface these.
TRADITION_RITUALS = {
    "errant": {
        "initiation_rite": "rides alone for a year and a day, returning with a token from a stranger's hearth",
        "funeral_rite":    "buried at a crossroads under a cairn, with the lance broken and split between the four roads",
        "festival":        "the Crossroads Moot — every fifth winter, errants gather to swap tales and trade horses",
        "fighting_school": "the Long Road — no formal style, only tested by mile and mile",
        "taboo":           "never accepting a lord's standing offer — even a friendly one",
        "salute":          "two fingers raised to the brow, palm outward — 'road well'",
    },
    "templar": {
        "initiation_rite": "all-night vigil before the chapter altar, ending with the chaplain's blessing at first light",
        "funeral_rite":    "buried in full plate beneath the chapter house, head pointing east",
        "festival":        "the Feast of the Founding Saint — three days of vigil, fasting, and a closing tournament",
        "fighting_school": "the Sevenfold Cut — a closed sword form passed only between brothers",
        "taboo":           "raising the lance against an unarmed pilgrim",
        "salute":          "right fist crossed over the heart — 'in the saint's name'",
    },
    "hospitaller": {
        "initiation_rite": "tends the sick at the chapter almonry for a full season before being given a lance",
        "funeral_rite":    "buried beside the road they last rode, marked by a stone lily",
        "festival":        "Almoner's Day — pilgrims are sheltered and fed for a week from the chapter's stores",
        "fighting_school": "the Mended Hand — defensive forms taught alongside binding wounds",
        "taboo":           "striking the first blow in any quarrel",
        "salute":          "open palm held to the heart — 'be well'",
    },
    "cavalier": {
        "initiation_rite": "the royal accolade — knighted by the king's own sword at the Coronation Feast",
        "funeral_rite":    "lies in state in the throne hall for three nights, then interred with full court honors",
        "festival":        "the King's Lists — annual grand tournament held on the sovereign's name-day",
        "fighting_school": "the Royal Tilt — courtly lance and sword forms refined in the king's stable",
        "taboo":           "ever riding under colors other than the crown's",
        "salute":          "a deep bow with the helm tucked in the crook of the arm — 'for the Crown'",
    },
    "mercenary": {
        "initiation_rite": "the contract-signing — drinking the captain's cup and marking the muster-ledger in blood",
        "funeral_rite":    "burned on the campaign-fire, ashes split among the surviving company",
        "festival":        "Pay-Day — the muster gathers, splits the season's purse, and re-signs the captains",
        "fighting_school": "the Free Lance — pragmatic mix of every form the company has captured a master from",
        "taboo":           "breaking a signed contract before its term, for any price",
        "salute":          "open hand pressed to the purse — 'paid and sworn'",
    },
    "marcher": {
        "initiation_rite": "stands one full moon at the border beacon before being given the warden's lance",
        "funeral_rite":    "raised on a beacon-cairn at the watch-line, lit one final time for the dead",
        "festival":        "Beacon Night — every watch-keep lights its fires the same midnight, end to end of the march",
        "fighting_school": "the Long Watch — patient pole forms tested against night raids",
        "taboo":           "abandoning the watch-post before the relief arrives",
        "salute":          "a single rap on the gauntlet against the helm — 'beacons hold'",
    },
    "magisterial": {
        "initiation_rite": "defends a thesis in arms before the conclave — a written argument followed by a sparring test",
        "funeral_rite":    "the body wrapped in the founder's scroll-case, buried under the library floor",
        "festival":        "the Lamp-Lit Conclave — three nights of debate, drilling, and reading by candlelight",
        "fighting_school": "the Argued Cut — every stroke must answer a stroke; the form is a dialectic",
        "taboo":           "striking before the opponent has finished speaking",
        "salute":          "two fingers tapped to a closed book at the belt — 'read, then ride'",
    },
    "berserker": {
        "initiation_rite": "fights the senior unarmored, in the chapter's red pit, until first blood is drawn either way",
        "funeral_rite":    "burned on a pyre of the dead's own broken weapons",
        "festival":        "the Howling — annual moonlit muster where new scars are counted and old ones renamed",
        "fighting_school": "the Red Charge — no parry, no retreat; every form is forward",
        "taboo":           "wearing a closed helm during a formal duel",
        "salute":          "fist struck against the breastplate twice — 'forward, always forward'",
    },
    "horde": {
        "initiation_rite": "the First Hunt — a three-day mounted hunt across the clan's range, returning with one trophy from each cardinal direction",
        "funeral_rite":    "sky-burial atop a ridge, the body laid on the felt of the founder, the horse loosed to run free",
        "festival":        "Naadam — three days of mounted archery, wrestling, and horse racing in the high summer grass",
        "fighting_school": "the Eagle-Wing — feigned flight, encircle, and arrow-storm before the lances close",
        "taboo":           "killing a foal of the clan-herd, even by accident",
        "salute":          "right hand swept from the horizon to the heart — 'sky above us'",
    },
    "cataphract": {
        "initiation_rite": "the Sun-Vigil — kept overnight on the chapter's eastern wall, lance in hand, until the first dawn light",
        "funeral_rite":    "cremated on a cedar pyre with the kontos laid crosswise, the ashes scattered to the east wind",
        "festival":        "Nowruz of Lances — spring tournament with the line drill performed as a public rite",
        "fighting_school": "the Iron Wall — locked shield-and-lance formation, advancing in step to a drum",
        "taboo":           "dismounting before sunset on any campaign day",
        "salute":          "kontos raised, then lowered to point at the sun — 'the Wheel turns'",
    },
    "bushi": {
        "initiation_rite": "genpuku — the squire's topknot is cut and the lord-given katana is bound to the obi for the first time",
        "funeral_rite":    "the body is washed, dressed in the white kimono, and interred with the wakizashi for the next world",
        "festival":        "Kabuto-Matsuri — the helms of past masters are aired in the dojo and the founder's cuts are demonstrated",
        "fighting_school": "Itto-Ryu — the one-cut school; every form ends in a single decisive stroke",
        "taboo":           "showing the back to an opponent who has not yet sheathed",
        "salute":          "a deep silent bow, hand resting on the saya — 'one cut, one word'",
    },
    "furusiyya": {
        "initiation_rite": "the Five Arts — must complete riding, archery, swordplay, polo, and recitation under examination of the master",
        "funeral_rite":    "buried before sunset facing the qibla, the sabre laid across the chest",
        "festival":        "the Crescent Games — open trials of lance, bow, and tabla-strike timed to the prayer hours",
        "fighting_school": "the Three-Art — horse, bow, and blade trained as one inseparable form",
        "taboo":           "letting another rider tend your own horse",
        "salute":          "right hand to brow, then to heart — 'peace and skill'",
    },
    "rajput": {
        "initiation_rite": "the Threshold Cut — the squire's brow is marked with vermilion and the founder's tulwar is touched to each shoulder",
        "funeral_rite":    "cremated on a pyre by the river, the tulwar broken across the knee and laid in the ash",
        "festival":        "Dussehra — the order's banner is paraded, the founder's tulwar polished, and trials of horse and lance are held",
        "fighting_school": "the Tulwar-and-Tear — circular cuts paired with footwork that never gives ground",
        "taboo":           "turning the back to a drawn blade — to do so is to lose the caste",
        "salute":          "right hand raised to the helm, palm forward — 'Jai Rana'",
    },
}


# Cultural Grandmaster title pairs that override the kingdom's leader_title
# when a noble is recruited into one of these traditions. Other roles still
# use the kingdom's title; only the head/grandmaster slot is overridden.
_GRANDMASTER_TITLE_BY_TRADITION = {
    "horde":       ("Khan",      "Khatun"),
    "cataphract":  ("Shah",      "Banou-Shah"),
    "bushi":       ("Shōgun",    "Shōgun"),
    "furusiyya":   ("Sultan",    "Sultana"),
    "rajput":      ("Maharana",  "Maharani"),
    "templar":     ("Grandmaster of the Order", "Grandmistress of the Order"),
    "berserker":   ("Wolf-Lord", "Wolf-Lady"),
}


_CULTURAL_RANK_LABELS = {
    "horde": {
        "Squire":          "Nokod",
        "Knight-Errant":   "Arban-Rider",
        "Knight-Banneret": "Mingghan-Captain",
        "Marshal":         "Bahadur",
        "Grandmaster":     "Khan",
    },
    "cataphract": {
        "Squire":          "Stratiotes",
        "Knight-Errant":   "Klibanophoros",
        "Knight-Banneret": "Spatharios",
        "Marshal":         "Strategos",
        "Grandmaster":     "Sun-Lord",
    },
    "bushi": {
        "Squire":          "Ashigaru",
        "Knight-Errant":   "Bushi",
        "Knight-Banneret": "Hatamoto",
        "Marshal":         "Karō",
        "Grandmaster":     "Shōgun",
    },
    "furusiyya": {
        "Squire":          "Ghulam",
        "Knight-Errant":   "Faris",
        "Knight-Banneret": "Amir",
        "Marshal":         "Atabeg",
        "Grandmaster":     "Sultan-Faris",
    },
    "rajput": {
        "Squire":          "Sevak",
        "Knight-Errant":   "Kshatriya",
        "Knight-Banneret": "Thakur",
        "Marshal":         "Senapati",
        "Grandmaster":     "Maharana",
    },
}


def cultural_rank_label(tradition: str, rank: str) -> str:
    """Map a canonical rank to a tradition-flavored label for display only."""
    labels = _CULTURAL_RANK_LABELS.get(tradition)
    if labels is None:
        return rank
    return labels.get(rank, rank)


def order_battle_cry(order_id: int) -> str:
    o = ORDERS.get(order_id)
    if not o:
        return ""
    return ORDER_TRADITIONS.get(o.tradition, {}).get("battle_cry", "")


def order_pre_charge_ritual(order_id: int) -> str:
    o = ORDERS.get(order_id)
    if not o:
        return ""
    return ORDER_TRADITIONS.get(o.tradition, {}).get("pre_charge_ritual", "")


def _ritual_field(order_id: int, key: str) -> str:
    o = ORDERS.get(order_id)
    if not o:
        return ""
    return TRADITION_RITUALS.get(o.tradition, {}).get(key, "")


def order_initiation_rite(order_id: int) -> str:
    return _ritual_field(order_id, "initiation_rite")


def order_funeral_rite(order_id: int) -> str:
    return _ritual_field(order_id, "funeral_rite")


def order_festival(order_id: int) -> str:
    return _ritual_field(order_id, "festival")


def order_fighting_school(order_id: int) -> str:
    return _ritual_field(order_id, "fighting_school")


def order_taboo(order_id: int) -> str:
    return _ritual_field(order_id, "taboo")


def order_salute(order_id: int) -> str:
    return _ritual_field(order_id, "salute")


# ---------------------------------------------------------------------------
# Tournament prize tables — return loot rolls keyed by the bested order's
# tradition. Called from jousting.award_rewards. Item ids are looked up in
# ITEMS at use time; the function returns the rolled list and the caller
# is responsible for adding to player.inventory.
# ---------------------------------------------------------------------------

_TRADITION_PRIZE_BOOK = {
    "errant":      ["book_errant_road_book"],
    "templar":     ["book_templar_rule", "sanctified_cross"],
    "hospitaller": ["book_hospitaller_almoners", "almoners_cup"],
    "cavalier":    ["book_cavalier_court_codex", "coronation_ribbon"],
    "mercenary":   ["book_mercenary_ledger", "ledger_pay_book"],
    "marcher":     ["book_marcher_watch_manual", "beacon_iron"],
    "magisterial": ["book_magisterial_summa", "book_lances_drill"],
    "berserker":   ["book_berserker_skald_saga", "founders_drinking_horn"],
    "horde":       ["book_horde_yasa", "nine_tail_standard",
                    "horsetail_charm", "naadam_medal"],
    "cataphract":  ["book_cataphract_strategikon", "sun_disc_chamfron",
                    "peacock_feather_crest", "klivanion_scale"],
    "bushi":       ["book_bushi_bushido", "mon_banner",
                    "tea_bowl_first_vassal", "death_poem_scroll"],
    "furusiyya":   ["book_furusiyya_treatise", "crescent_pennant_relic",
                    "madrasa_astrolabe", "faris_treatise"],
    "rajput":      ["book_rajput_charter", "vermilion_paint_pot",
                    "saffron_sash", "tiger_claw_gauntlet"],
}

_TRADITION_PRIZE_COIN = {
    "errant":      "coin_errant_token",
    "templar":     "coin_templar_silver",
    "hospitaller": "coin_hospitaller_lily",
    "cavalier":    "coin_cavalier_crown",
    "mercenary":   "coin_mercenary_denier",
    "marcher":     "coin_marcher_beacon",
    "magisterial": "coin_magisterial_quill",
    "berserker":   "coin_berserker_scar",
    "horde":       "coin_horde_tug",
    "cataphract":  "coin_cataphract_sun",
    "bushi":       "coin_bushi_mon",
    "furusiyya":   "coin_furusiyya_dinar",
    "rajput":      "coin_rajput_mohur",
}

_TRADITION_PRIZE_PENNANT = {
    "cavalier":    "pennant_kings_lists",
    "hospitaller": "pennant_almoner",
    "mercenary":   "pennant_pay_day",
    "marcher":     "pennant_beacon",
    "berserker":   "pennant_howling",
    "horde":       "pennant_naadam",
    "cataphract":  "pennant_nowruz",
    "bushi":       "pennant_mon",
    "furusiyya":   "pennant_crescent",
    "rajput":      "pennant_dussehra",
}

_SHARED_PODIUM_DROPS = [
    "trophy_first_pass_token", "broken_pennant", "victory_garland",
    "coin_champion_medallion", "coin_first_blood", "coin_chapter_double",
]
_SHARED_CHAMPION_DROPS = [
    "champion_chain", "rite_blade", "founders_drinking_horn",
    "order_charter", "knight_dossier",
]


def tournament_drops(order_id: int, place: int, rng) -> list:
    """Return [(item_id, count), ...] for a tournament finish.

    ``place``: 1 champion, 2 runner-up, 4 semi-final, 8 first-round knockout.
    """
    o = ORDERS.get(order_id)
    tradition = o.tradition if o else "errant"
    drops = []
    coin = _TRADITION_PRIZE_COIN.get(tradition)
    if coin and place <= 4:
        drops.append((coin, rng.randint(1, 2)))
    pennant = _TRADITION_PRIZE_PENNANT.get(tradition)
    if pennant and 1 < place <= 4:
        drops.append((pennant, 1))
    if place == 1:
        sig_pool = _TRADITION_PRIZE_BOOK.get(tradition, [])
        if sig_pool:
            drops.append((rng.choice(sig_pool), 1))
        drops.append((rng.choice(_SHARED_CHAMPION_DROPS), 1))
        if pennant:
            drops.append((pennant, 1))
    elif place <= 4:
        drops.append((rng.choice(_SHARED_PODIUM_DROPS), 1))
    return drops


def _rank_roster(rng: random.Random, n: int) -> list:
    """Pick a rank for each of n knights. Exactly one Grandmaster, then taper."""
    if n <= 0:
        return []
    ranks = ["Grandmaster"]
    pool = [("Marshal", 1), ("Knight-Banneret", 2), ("Knight-Errant", 3),
            ("Squire", 2)]
    flat = []
    for rank, weight in pool:
        flat.extend([rank] * weight)
    for _ in range(n - 1):
        ranks.append(rng.choice(flat))
    rng.shuffle(ranks)
    return ranks


def _skill_for_rank(rng: random.Random, rank: str, bias: float) -> float:
    for name, lo, hi in KNIGHT_RANKS:
        if name == rank:
            return round(rng.uniform(lo, hi) + bias, 3)
    return round(rng.uniform(0.85, 1.15) + bias, 3)


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class Knight:
    knight_id:        int
    name:             str
    order_id:         int
    personal_arms:    heraldry.CoatOfArms
    mount_breed:      str = "horse"
    kit:              str = "lancer"
    tournament_wins:  int = 0
    skill:            float = 1.0   # 0.7-1.4; weights AI in joust bouts
    rank:             str = "Knight-Errant"
    quirks:           list = field(default_factory=list)
    # Nobility — set when the knight is recruited from a kingdom's dynasty.
    is_noble:         bool = False
    noble_title:      str = ""
    dynasty_id:       int = -1
    person_id:        int = -1


@dataclass
class KnightlyOrder:
    order_id:           int
    name:               str
    motto:              str
    heraldry:           heraldry.CoatOfArms
    home_region:        int
    member_ids:         list = field(default_factory=list)
    founded_year:       int = 0
    prestige:           int = 20
    tradition:          str = "errant"
    seat:               str = ""
    vows:               list = field(default_factory=list)
    patron:             str = ""
    relic:              str = ""
    doctrine:           str = ""
    founding_chronicle: str = ""
    rival_id:           Optional[int] = None
    # Kingdom politics. region_id == kingdom_id in the plan-driven flow.
    # kingdom_alignment maps kingdom_id -> "sworn"|"rival"|"exiled"|"independent".
    kingdom_alignment:  dict = field(default_factory=dict)
    patron_dynasty_id:  Optional[int] = None
    # Worldgen-era ledger of notable moments. List[str], short prose lines like
    # "Year 142: Sir Carad slew the Bear-of-the-Marches at the Spring Lists."
    # Populated by _backdate_history at order creation so brand-new worlds
    # boot with centuries of chivalric backstory.
    historical_events:  list = field(default_factory=list)


# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------

def _pick_tradition(rng: random.Random, biome_group: str) -> str:
    biased = _TRADITION_BIAS_BY_GROUP.get(biome_group, [])
    # Weighted: biased traditions get extra rolls, all traditions still possible.
    bag = list(ORDER_TRADITIONS.keys()) + biased + biased
    return rng.choice(bag)


def _gen_order_name(rng: random.Random, biome_group: str, tradition: str) -> str:
    pool = KNIGHTLY_ORDER_NAME_POOLS.get(biome_group, _DEFAULT_NAME_POOL)
    templates = _NAME_TEMPLATES_BY_TRADITION.get(tradition,
                                                 ["Order of the {x}"])
    return rng.choice(templates).format(x=rng.choice(pool))


def _gen_seat_name(rng: random.Random, biome_group: str, tradition: str) -> str:
    seat_type = rng.choice(_SEAT_TYPES_BY_TRADITION.get(tradition, ["Chapter House"]))
    loc = rng.choice(_SEAT_LOCATIONS_BY_GROUP.get(biome_group, _DEFAULT_SEAT_LOCATIONS))
    return f"{seat_type} of {loc}"


def _gen_vows(rng: random.Random, tradition: str) -> list:
    pool = ORDER_TRADITIONS[tradition]["vow_pool"]
    n = rng.choice([1, 2, 2, 3])
    return rng.sample(pool, min(n, len(pool)))


def _pick_kit(rng: random.Random, tradition: str) -> str:
    weights = ORDER_TRADITIONS[tradition]["kit_weights"]
    kits = list(weights.keys())
    return rng.choices(kits, weights=list(weights.values()), k=1)[0]


# ---------------------------------------------------------------------------
# Founding chronicles — one-line procedural history.
# ---------------------------------------------------------------------------

_FOUNDING_OPENERS = [
    "Chartered after the {event}",
    "Sworn beneath the {landmark} of {place}",
    "Founded by {founder} in the wake of the {event}",
    "Raised on the {anniversary} day of the {event}",
    "Reformed from older orders after the {event}",
]
_FOUNDING_EVENTS = [
    "Long Winter", "Saffron Plague", "Battle of Greymoor",
    "Burning of Wynhold", "Twin Comet", "Crossing of the Marches",
    "Year Without Harvest", "Siege of Highgate",
]
_FOUNDING_LANDMARKS = ["oak", "watchstone", "broken arch", "iron bell",
                       "river-ford", "twin towers"]
_FOUNDING_ANNIVS    = ["seventh", "tenth", "first", "thirteenth", "fortieth"]


def _gen_founding_chronicle(rng: random.Random, biome_group: str,
                            founder_name: str) -> str:
    opener = rng.choice(_FOUNDING_OPENERS)
    place  = rng.choice(_SEAT_LOCATIONS_BY_GROUP.get(biome_group,
                                                     _DEFAULT_SEAT_LOCATIONS))
    return opener.format(
        event      = rng.choice(_FOUNDING_EVENTS),
        landmark   = rng.choice(_FOUNDING_LANDMARKS),
        place      = place,
        founder    = founder_name,
        anniversary= rng.choice(_FOUNDING_ANNIVS),
    ) + "."


def _gen_quirks(rng: random.Random, tradition: str) -> list:
    pool = ORDER_TRADITIONS[tradition]["quirk_pool"]
    n = rng.choice([0, 1, 1, 2])
    if n == 0 or not pool:
        return []
    return rng.sample(pool, min(n, len(pool)))


def aim_bias_for_opponent(knight_id: int) -> tuple:
    """Return (high, mid, low) weight bias for a knight's tradition.

    Used by jousting.tick when the AI picks its aim — gives each order a
    recognizable tilt-yard style.
    """
    k = KNIGHTS.get(knight_id)
    if not k:
        return (1, 1, 1)
    o = ORDERS.get(k.order_id)
    if not o:
        return (1, 1, 1)
    return ORDER_TRADITIONS.get(o.tradition,
                                ORDER_TRADITIONS["errant"])["aim_bias"]


def rival_of(order_id: int) -> Optional["KnightlyOrder"]:
    o = ORDERS.get(order_id)
    if o is None or o.rival_id is None:
        return None
    return ORDERS.get(o.rival_id)


# ---------------------------------------------------------------------------
# Kingdom alignment — orders take stances toward kingdoms, and recruit
# members from the ruling dynasty when the tradition allows.
# ---------------------------------------------------------------------------

# Per tradition: probability the home kingdom is "sworn" rather than
# "independent", and the chance of recruiting noble members at all.
_HOME_SWORN_PROB = {
    "cavalier":     0.95,
    "marcher":      0.90,
    "magisterial":  0.70,
    "templar":      0.55,
    "hospitaller":  0.20,
    "errant":       0.10,
    "mercenary":    0.05,
    "berserker":    0.10,
    # New traditions
    "horde":        0.60,   # clan loyalty, mixed crown loyalty
    "cataphract":   0.95,   # household cavalry of the crown
    "bushi":        0.95,   # vassal retainers
    "furusiyya":    0.70,   # often crown-trained but also independent schools
    "rajput":       0.92,   # sworn to the Rana
}
_NOBLE_RECRUIT_PROB = {
    "cavalier":     0.95,
    "magisterial":  0.60,
    "marcher":      0.55,
    "templar":      0.45,
    "hospitaller":  0.20,
    "errant":       0.10,
    "berserker":    0.10,
    "mercenary":    0.05,
    # New traditions
    "horde":        0.75,   # khans always have clan-blood riders
    "cataphract":   0.90,
    "bushi":        0.95,
    "furusiyya":    0.55,
    "rajput":       0.90,
}
# When the home is NOT sworn, some traditions are actively at odds with it.
_EXILED_PROB = {
    "berserker":    0.30,
    "errant":       0.15,
    "mercenary":    0.20,
    "horde":        0.25,   # exiled clans become rivals of the crown
    "furusiyya":    0.10,
}


def _noble_title_for_role(role: str, leader_title: tuple,
                          tradition: str = "") -> str:
    """Map dynasty role + kingdom leader-title to a noble prefix.

    For traditions in _GRANDMASTER_TITLE_BY_TRADITION the head/founder roles
    override the kingdom title — a bushi order's head reads as 'Shōgun'
    regardless of the home region's leader_title.
    """
    head_male = leader_title[0] if leader_title else "King"
    override = _GRANDMASTER_TITLE_BY_TRADITION.get(tradition)
    if override and role in ("head", "founder"):
        head_male = override[0]
    if role == "head":
        return head_male
    if role == "founder":
        return f"Late {head_male}"
    if role == "spouse":
        return f"{head_male}-Consort"
    if role == "heir":
        return "Prince" if head_male in ("King", "Tsar", "Emperor", "Sultan",
                                          "Shah", "Maharana", "Shōgun") else "Heir"
    # scion / unknown
    return "Lord"


def _person_to_knight_name(person, leader_title: tuple, house_name: str,
                           tradition: str = "") -> tuple:
    """Return (full_name, noble_title) for a noble knight."""
    title = _noble_title_for_role(person.role, leader_title, tradition)
    epithet = f" {person.epithet}" if person.epithet else ""
    house_short = house_name.replace("House ", "")
    return (f"{title} {person.name} of {house_short}{epithet}", title)


def _rank_for_noble(rng: random.Random, role: str, tradition: str,
                    grandmaster_taken: bool) -> str:
    """Pick a rank for a noble recruit. Cavaliers crown their king."""
    if role == "head" and tradition == "cavalier" and not grandmaster_taken:
        return "Grandmaster"
    if role == "head" and tradition in ("templar", "marcher") and not grandmaster_taken:
        if rng.random() < 0.4:
            return "Grandmaster"
    if role in ("head", "founder"):
        return "Marshal"
    if role == "heir":
        return rng.choice(["Marshal", "Knight-Banneret"])
    if role == "spouse":
        return rng.choice(["Knight-Banneret", "Marshal"])
    # scion
    return rng.choice(["Knight-Banneret", "Knight-Errant", "Squire"])


def _recruit_noble(rng: random.Random, order: "KnightlyOrder", person,
                   leader_title: tuple, house_name: str, dynasty_id: int,
                   rank: str) -> "Knight":
    """Build a Knight tied to a real Person in a dynasty."""
    global _NEXT_KNIGHT_ID
    kid = _NEXT_KNIGHT_ID
    _NEXT_KNIGHT_ID += 1
    profile  = ORDER_TRADITIONS.get(order.tradition, ORDER_TRADITIONS["errant"])
    personal = heraldry.generate(rng, order.heraldry.primary,
                                 charge_pool=KNIGHTLY_CHARGE_POOL)
    full_name, title = _person_to_knight_name(person, leader_title, house_name,
                                              order.tradition)
    # Nobles get a small skill boost on top of rank (better training, gear).
    skill = _skill_for_rank(rng, rank, profile["skill_bias"] + 0.05)
    knight = Knight(
        knight_id     = kid,
        name          = full_name,
        order_id      = order.order_id,
        personal_arms = personal,
        kit           = _pick_kit(rng, order.tradition),
        skill         = skill,
        rank          = rank,
        quirks        = _gen_quirks(rng, order.tradition),
        is_noble      = True,
        noble_title   = title,
        dynasty_id    = dynasty_id,
        person_id     = person.person_id,
    )
    KNIGHTS[kid] = knight
    order.member_ids.append(kid)
    return knight


def _align_with_kingdoms(rng: random.Random, order: "KnightlyOrder",
                         plan, roster_size: int) -> int:
    """Set kingdom_alignment, recruit noble members, return # nobles recruited.

    `plan` must be a worldgen.plan.WorldPlan (or None — falls back to a
    plan-less default where alignment is set but no nobles are recruited).
    """
    tradition = order.tradition
    home_kid  = order.home_region

    # ---- Set alignment toward the home kingdom ----
    home_sworn = rng.random() < _HOME_SWORN_PROB.get(tradition, 0.5)
    if home_sworn:
        order.kingdom_alignment[home_kid] = "sworn"
    else:
        if rng.random() < _EXILED_PROB.get(tradition, 0.0):
            order.kingdom_alignment[home_kid] = "exiled"
        else:
            order.kingdom_alignment[home_kid] = "independent"

    # ---- Propagate kingdom-vs-kingdom relations into alignment ----
    if plan is not None:
        home = plan.kingdoms.get(home_kid)
        if home is not None:
            for other_kid, rel in home.relations.items():
                if other_kid == home_kid:
                    continue
                # Sworn orders inherit their home's enemies and friends.
                if order.kingdom_alignment[home_kid] == "sworn":
                    if rel == "rival":
                        order.kingdom_alignment[other_kid] = "rival"
                    elif rel == "ally":
                        order.kingdom_alignment[other_kid] = "sworn"
                # Exiled orders flip: feud with home, friendly with home's rivals.
                elif order.kingdom_alignment[home_kid] == "exiled" and rel == "rival":
                    order.kingdom_alignment[other_kid] = "sworn"

    if plan is None:
        return 0

    # ---- Noble recruitment ----
    home = plan.kingdoms.get(home_kid)
    if home is None:
        return 0
    if rng.random() >= _NOBLE_RECRUIT_PROB.get(tradition, 0.1):
        return 0

    # Pick recruit dynasty: usually the home dynasty; an exiled order
    # may instead pull from a rival kingdom's dynasty.
    recruit_kid = home_kid
    if order.kingdom_alignment.get(home_kid) == "exiled":
        rivals = [kid for kid, rel in home.relations.items() if rel == "rival"
                  and kid in plan.kingdoms]
        if rivals:
            recruit_kid = rng.choice(rivals)

    recruit_kingdom = plan.kingdoms.get(recruit_kid)
    if recruit_kingdom is None:
        return 0
    dynasty = plan.dynasties.get(recruit_kingdom.dynasty_id)
    if dynasty is None or not dynasty.members:
        return 0

    order.patron_dynasty_id = dynasty.dynasty_id

    living = [p for p in dynasty.members.values() if p.died_year == -1]
    if not living:
        return 0

    # Decide how many nobles to take. Cap at half the roster.
    max_n = max(1, roster_size // 2)
    if tradition == "cavalier":
        n = rng.randint(1, min(max_n, len(living)))
    else:
        n = 1

    grandmaster_taken = False
    nobles = []
    # Prefer the head first (king), then heir, then others.
    living.sort(key=lambda p: {"head": 0, "heir": 1, "spouse": 2,
                               "scion": 3, "founder": 4}.get(p.role, 5))
    for person in living[:n]:
        rank = _rank_for_noble(rng, person.role, tradition, grandmaster_taken)
        if rank == "Grandmaster":
            grandmaster_taken = True
        _recruit_noble(rng, order, person,
                       recruit_kingdom.leader_title,
                       dynasty.house_name,
                       dynasty.dynasty_id,
                       rank)
        nobles.append(person)
    return len(nobles)


# ---------------------------------------------------------------------------
# Lookups for alignment
# ---------------------------------------------------------------------------

def aligned_kingdoms(order_id: int, status: str = "sworn") -> list:
    o = ORDERS.get(order_id)
    if not o:
        return []
    return [kid for kid, s in o.kingdom_alignment.items() if s == status]


def alignment_with(order_id: int, kingdom_id: int) -> str:
    o = ORDERS.get(order_id)
    if not o:
        return "independent"
    return o.kingdom_alignment.get(kingdom_id, "independent")


_KNIGHT_FIRSTS = ["Aldric", "Beren", "Cedric", "Drust", "Eowin",
                  "Hale", "Iven", "Joren", "Kael", "Loren",
                  "Mira", "Nessa", "Orla", "Petra", "Rhea",
                  "Tavin", "Ulric", "Vance", "Wren", "Yorath"]
_KNIGHT_EPITHETS = ["of Ashvale", "the Bold", "of Wynhold",
                    "the Quick", "of Stormridge", "the Steadfast",
                    "the Tall", "of Greymoor", "the Younger",
                    "of Highgate", "the Stern", "of Thornmere"]


def _gen_knight_name(rng: random.Random) -> str:
    return f"Sir {rng.choice(_KNIGHT_FIRSTS)} {rng.choice(_KNIGHT_EPITHETS)}"


def _new_order(rng: random.Random, region, founded_year: int) -> KnightlyOrder:
    global _NEXT_ORDER_ID
    oid = _NEXT_ORDER_ID
    _NEXT_ORDER_ID += 1
    biome_group = getattr(region, "biome_group", "forest")
    tradition   = _pick_tradition(rng, biome_group)
    profile     = ORDER_TRADITIONS[tradition]
    primary     = region.leader_color if region else (140, 60, 60)
    coa         = heraldry.generate(rng, primary, charge_pool=KNIGHTLY_CHARGE_POOL)
    motto       = rng.choice(profile["motto_pool"])
    founder_first = rng.choice(_KNIGHT_FIRSTS)
    order = KnightlyOrder(
        order_id           = oid,
        name               = _gen_order_name(rng, biome_group, tradition),
        motto              = motto,
        heraldry           = coa,
        home_region        = getattr(region, "region_id", 0),
        founded_year       = founded_year,
        prestige           = max(5, min(100, rng.randint(15, 45) + profile["prestige_bias"])),
        tradition          = tradition,
        seat               = _gen_seat_name(rng, biome_group, tradition),
        vows               = _gen_vows(rng, tradition),
        patron             = rng.choice(profile["patron_pool"]),
        relic              = "the " + rng.choice(profile["relic_pool"]),
        doctrine           = rng.choice(profile["doctrine_pool"]),
        founding_chronicle = _gen_founding_chronicle(rng, biome_group,
                                                     f"Sir {founder_first}"),
    )
    # Centuries of backstory — generate after the order exists so we can
    # reference its tradition/seat/founder in the prose.
    order.historical_events = _generate_historical_events(
        rng, order, founded_year, current_year=max(founded_year + 1, founded_year + 50))
    # Prestige rises with age and quiet victories.
    order.prestige = min(100, order.prestige + min(40, len(order.historical_events) * 3))
    ORDERS[oid] = order
    return order


_EVENT_TEMPLATES = [
    "Year {y}: Sir {n} won the {place} Lists, taking three lances unhorsed.",
    "Year {y}: a schism over the doctrine of {doctrine} split the order; the dissenters were exiled.",
    "Year {y}: {n} of the {seat_short} earned the rank of Marshal in the field.",
    "Year {y}: the order rode against a brigand-king at the {place} fords; few returned.",
    "Year {y}: a Grandmaster fell to fever; succession was contested for a season.",
    "Year {y}: the {relic_short} was carried to the {place} sanctum and never moved again.",
    "Year {y}: a royal wedding feast saw the order's banner raised above the dais.",
    "Year {y}: dishonor — Sir {n} was unhorsed at the king's joust and stripped of spurs.",
    "Year {y}: a plague took the senior knights; the roster shrank for a generation.",
    "Year {y}: a rival order's Grandmaster was slain in a duel of honor under the {place} oak.",
    "Year {y}: the order was granted lands east of {place} by the crown.",
    "Year {y}: a sworn vow of {vow} was added to the chapter rolls after the {place} campaign.",
    "Year {y}: Sir {n} was hailed Champion of the Lists for three seasons running.",
    "Year {y}: a contested election left the order leaderless until midwinter.",
    "Year {y}: the order took up arms against a heretic preacher at {place}.",
]


def _generate_historical_events(rng: random.Random, order: KnightlyOrder,
                                founded_year: int, current_year: int) -> list:
    """Walk forward from founded_year picking sparse notable events. Returns
    a list of short prose lines suitable for the chapter-house wall."""
    span = max(10, current_year - founded_year)
    n_events = rng.randint(3, 6) + min(4, span // 60)
    events = []
    seat_short = order.seat.split(" ")[-1] if order.seat else "chapter"
    relic_short = order.relic.replace("the ", "")
    vow = (order.vows[0] if order.vows else "valor")
    place_pool = ["Spring", "Autumn", "Winter", "Solstice", "Royal", "Marcher",
                  "Border", "Crown", "Cathedral", "Harbor"]
    used_years = set()
    for _ in range(n_events):
        for _try in range(8):
            y = founded_year + rng.randint(1, span)
            if y not in used_years:
                used_years.add(y)
                break
        tmpl = rng.choice(_EVENT_TEMPLATES)
        line = tmpl.format(
            y           = y,
            n           = rng.choice(_KNIGHT_FIRSTS),
            place       = rng.choice(place_pool),
            doctrine    = order.doctrine or "the vow",
            seat_short  = seat_short,
            relic_short = relic_short,
            vow         = vow,
        )
        events.append((y, line))
    events.sort(key=lambda t: t[0])
    return [line for _, line in events]


def _new_knight(rng: random.Random, order: KnightlyOrder, rank: str) -> Knight:
    global _NEXT_KNIGHT_ID
    kid = _NEXT_KNIGHT_ID
    _NEXT_KNIGHT_ID += 1
    profile  = ORDER_TRADITIONS.get(order.tradition, ORDER_TRADITIONS["errant"])
    personal = heraldry.generate(rng, order.heraldry.primary,
                                 charge_pool=KNIGHTLY_CHARGE_POOL)
    knight = Knight(
        knight_id     = kid,
        name          = _gen_knight_name(rng),
        order_id      = order.order_id,
        personal_arms = personal,
        kit           = _pick_kit(rng, order.tradition),
        skill         = _skill_for_rank(rng, rank, profile["skill_bias"]),
        rank          = rank,
        quirks        = _gen_quirks(rng, order.tradition),
    )
    KNIGHTS[kid] = knight
    order.member_ids.append(kid)
    return knight


# ---------------------------------------------------------------------------
# Public entry — idempotent. Mirrors guild_worldgen.seed_guilds.
# ---------------------------------------------------------------------------

def seed_knightly_orders(world) -> None:
    """Charter 1-2 orders per region if none exist. Safe to call on every load."""
    try:
        from towns import REGIONS
    except Exception:
        return
    if not REGIONS:
        return
    seed = getattr(world, "world_seed", 0) or 0
    game_year = getattr(world, "day", 0) // 365
    plan = getattr(world, "plan", None)
    # Historical sim length (e.g. 500). Orders were chartered somewhere in
    # those centuries, not on day one of the player's game — so we backdate.
    history_years = getattr(plan, "history_years", 0) if plan else 0
    sim_current_year = max(history_years, 1)
    for region in REGIONS.values():
        if any(o.home_region == region.region_id for o in ORDERS.values()):
            continue
        rng = random.Random((seed * 7919) ^ (region.region_id * 104729) ^ 0xCAFEF00D)
        n_orders = rng.choice([1, 1, 2])
        new_orders = []
        for _ in range(n_orders):
            # Backdate founding into the historical era. If we have a plan,
            # roll a year in [50, history_years - 30]; otherwise fall back
            # to the live game year.
            if history_years > 80:
                founded = rng.randint(50, history_years - 30)
            else:
                founded = game_year
            order = _new_order(rng, region, founded)
            # Regenerate events using the proper sim_current_year horizon now
            # that we have it (the _new_order default used a tight window).
            order.historical_events = _generate_historical_events(
                rng, order, founded, sim_current_year)
            order.prestige = min(100, order.prestige
                                 + min(40, len(order.historical_events) * 3))
            new_orders.append(order)
            roster_size = rng.randint(3, 6)
            # First: try to recruit nobles from the plan. They consume roster
            # slots; the rest is filled with procedural knights.
            n_nobles = _align_with_kingdoms(rng, order, plan, roster_size)
            remaining = roster_size - n_nobles
            if remaining > 0:
                # If a noble is already Grandmaster, the rest are non-Grandmaster.
                has_gm = any(KNIGHTS[kid].rank == "Grandmaster"
                             for kid in order.member_ids if kid in KNIGHTS)
                ranks = _rank_roster(rng, remaining)
                if has_gm:
                    ranks = ["Marshal" if r == "Grandmaster" else r for r in ranks]
                for rank in ranks:
                    _new_knight(rng, order, rank)
        # If a region chartered two orders, pair them as rivals.
        if len(new_orders) == 2:
            new_orders[0].rival_id = new_orders[1].order_id
            new_orders[1].rival_id = new_orders[0].order_id
        elif len(new_orders) == 1:
            # Pair with a random already-existing order from a *neighboring*
            # region (deterministic via rng). Optional — may stay solo.
            others = [o for o in ORDERS.values()
                      if o.home_region != region.region_id
                      and o.rival_id is None]
            if others and rng.random() < 0.55:
                partner = rng.choice(others)
                new_orders[0].rival_id = partner.order_id
                partner.rival_id        = new_orders[0].order_id


# ---------------------------------------------------------------------------
# Lookups
# ---------------------------------------------------------------------------

def orders_for_region(region_id: int) -> list:
    return [o for o in ORDERS.values() if o.home_region == region_id]


def orders_patronized_by(dynasty_id: int) -> list:
    """Orders that recruited their founding chapter from this plan-dynasty."""
    return [o for o in ORDERS.values() if o.patron_dynasty_id == dynasty_id]


def knights_from_dynasty(dynasty_id: int) -> list:
    """All knights (across orders) whose noble line is this plan-dynasty."""
    return [k for k in KNIGHTS.values() if k.dynasty_id == dynasty_id]


def knight(knight_id: int) -> Optional[Knight]:
    return KNIGHTS.get(knight_id)


def order(order_id: int) -> Optional[KnightlyOrder]:
    return ORDERS.get(order_id)


def tradition_desc(tradition: str) -> str:
    return ORDER_TRADITIONS.get(tradition, {}).get("desc", "")


def record_tournament_win(knight_id: int, prestige_delta: int = 1) -> None:
    k = KNIGHTS.get(knight_id)
    if not k:
        return
    k.tournament_wins += 1
    o = ORDERS.get(k.order_id)
    if o:
        o.prestige = min(100, o.prestige + prestige_delta)


def reset_registries() -> None:
    """Wipe in-memory state (used by save_manager.new_world / load)."""
    global _NEXT_ORDER_ID, _NEXT_KNIGHT_ID
    ORDERS.clear()
    KNIGHTS.clear()
    _NEXT_ORDER_ID = 1
    _NEXT_KNIGHT_ID = 1


# ---------------------------------------------------------------------------
# Player Membership — petition / quests / promotion
# ---------------------------------------------------------------------------

# Prestige thresholds for ranking up. Squire starts at 0 prestige; player
# is promoted to the next rank when prestige passes the threshold.
RANK_THRESHOLDS = [0, 10, 30, 70, 150]   # Squire / Errant / Banneret / Marshal / Grandmaster
RANK_NAMES      = [r[0] for r in KNIGHT_RANKS]

# Tradition-flavored quest templates. Each entry:
#   kind:     short tag used by UI flavor text
#   summary:  text shown on the quest board ({n} filled below)
#   item_id:  item the player must deliver (or None for kill/joust quests)
#   count:    number of items
#   prestige: prestige reward
#   gold:     gold reward
# Quest template fields:
#   tier:     0..4 — min player rank index to take it (Squire=0 ... Grandmaster=4)
#   kind:     short tag used for UI flavor
#   summary:  text shown on the quest board ({n} filled at roll-time)
#   item_id:  item the player must deliver (or None for joust_win quests)
#   count:    number of items required
#   prestige: prestige reward
#   gold:     gold reward
ORDER_QUEST_POOLS = {
    "errant": [
        {"tier": 0, "kind": "wayfarer", "summary": "Carry {n} sealed letters to the next chapter — proof you've walked the long road.",
         "item_id": "parchment", "count": 6, "prestige": 4, "gold": 25},
        {"tier": 0, "kind": "wayfarer", "summary": "Stitch the road-banner: bring {n} bolts of wool.",
         "item_id": "wool", "count": 4, "prestige": 4, "gold": 20},
        {"tier": 1, "kind": "duel",     "summary": "Win {n} tournament bouts under no pennant — honor outlives the saddle.",
         "item_id": None, "count": 2, "prestige": 8, "gold": 50, "kill_kind": "joust_win"},
        {"tier": 2, "kind": "wayfarer", "summary": "Bring {n} fine manuscripts gathered from chapters along the road.",
         "item_id": "manuscript_fine", "count": 2, "prestige": 14, "gold": 90},
        {"tier": 3, "kind": "duel",     "summary": "The Long Ride: win {n} bouts on the open circuit.",
         "item_id": None, "count": 4, "prestige": 22, "gold": 140, "kill_kind": "joust_win"},
    ],
    "templar": [
        {"tier": 0, "kind": "alms",   "summary": "Tithe {n} loaves of bread to the almonry.",
         "item_id": "bread", "count": 8, "prestige": 4, "gold": 20},
        {"tier": 0, "kind": "vigil",  "summary": "Bring {n} torches for the chapter altar's all-night vigil.",
         "item_id": "torch", "count": 12, "prestige": 4, "gold": 18},
        {"tier": 1, "kind": "relic",  "summary": "Recover {n} sanctified manuscripts for the chapter altar.",
         "item_id": "manuscript_fine", "count": 2, "prestige": 9, "gold": 70},
        {"tier": 2, "kind": "relic",  "summary": "Bring {n} rare manuscripts said to bear the saint's hand.",
         "item_id": "manuscript_rare", "count": 1, "prestige": 16, "gold": 140},
        {"tier": 3, "kind": "duel",   "summary": "Win {n} bouts in the saint's name — strike high, like the Sevenfold Cut.",
         "item_id": None, "count": 3, "prestige": 22, "gold": 120, "kill_kind": "joust_win"},
    ],
    "hospitaller": [
        {"tier": 0, "kind": "alms",   "summary": "Tithe {n} medicinal herbs to the chapter almonry.",
         "item_id": "dried_chamomile", "count": 6, "prestige": 4, "gold": 25},
        {"tier": 0, "kind": "alms",   "summary": "Bring {n} loaves to feed the pilgrims.",
         "item_id": "bread", "count": 10, "prestige": 5, "gold": 25},
        {"tier": 1, "kind": "mercy",  "summary": "Pack {n} bolts of linen for binding pilgrim wounds.",
         "item_id": "linen", "count": 4, "prestige": 8, "gold": 45},
        {"tier": 2, "kind": "mercy",  "summary": "Bring {n} fine manuscripts of medicine to the chapter library.",
         "item_id": "manuscript_fine", "count": 2, "prestige": 14, "gold": 100},
        {"tier": 3, "kind": "alms",   "summary": "Tithe {n} rare mushrooms for the apothecary's stores.",
         "item_id": "rare_mushroom", "count": 8, "prestige": 20, "gold": 160},
    ],
    "cavalier": [
        {"tier": 0, "kind": "tribute", "summary": "Bring {n} tournament pennants to the Crown's hall.",
         "item_id": "tournament_pennant", "count": 2, "prestige": 6, "gold": 50},
        {"tier": 1, "kind": "duel",    "summary": "Win {n} tournament bouts for the King's colors.",
         "item_id": None, "count": 1, "prestige": 8, "gold": 60, "kill_kind": "joust_win"},
        {"tier": 2, "kind": "tribute", "summary": "Deliver {n} sets of jousting plate to the royal armory.",
         "item_id": "armor_jousting_chestplate", "count": 2, "prestige": 14, "gold": 200},
        {"tier": 3, "kind": "duel",    "summary": "The King's Lists: win {n} bouts to be named Crown's Champion.",
         "item_id": None, "count": 4, "prestige": 24, "gold": 180, "kill_kind": "joust_win"},
        {"tier": 1, "kind": "tribute", "summary": "Bring {n} bolts of silk for the King's mantle.",
         "item_id": "silk", "count": 3, "prestige": 9, "gold": 75},
    ],
    "mercenary": [
        {"tier": 0, "kind": "bounty",  "summary": "Bring {n} iron chunks to the muster — pay is by the pound.",
         "item_id": "iron_chunk", "count": 16, "prestige": 4, "gold": 35},
        {"tier": 0, "kind": "bounty",  "summary": "Captain wants {n} rabbit pelts for the company quartermaster.",
         "item_id": "rabbit_pelt", "count": 6, "prestige": 4, "gold": 50},
        {"tier": 1, "kind": "bounty",  "summary": "Deliver {n} bear pelts — the captain pays by the hide.",
         "item_id": "bear_pelt", "count": 2, "prestige": 8, "gold": 110},
        {"tier": 2, "kind": "duel",    "summary": "Re-sign with blood: win {n} bouts to prove the contract still holds.",
         "item_id": None, "count": 2, "prestige": 14, "gold": 120, "kill_kind": "joust_win"},
        {"tier": 3, "kind": "bounty",  "summary": "Big purse: bring {n} sets of jousting plate stripped from the field.",
         "item_id": "armor_jousting_chestplate", "count": 2, "prestige": 20, "gold": 260},
    ],
    "marcher": [
        {"tier": 0, "kind": "warding", "summary": "Bring {n} torches to the beacon-line — a watch must never go dark.",
         "item_id": "torch", "count": 12, "prestige": 4, "gold": 25},
        {"tier": 1, "kind": "warding", "summary": "Recover {n} wolf pelts from the borderlands.",
         "item_id": "wolf_pelt", "count": 3, "prestige": 8, "gold": 60},
        {"tier": 2, "kind": "warding", "summary": "Bring {n} bear pelts — the watch-line will be lined with their hides.",
         "item_id": "bear_pelt", "count": 3, "prestige": 14, "gold": 120},
        {"tier": 3, "kind": "duel",    "summary": "Win {n} bouts in defense of the march.",
         "item_id": None, "count": 3, "prestige": 20, "gold": 110, "kill_kind": "joust_win"},
    ],
    "magisterial": [
        {"tier": 0, "kind": "study",   "summary": "Copy out {n} manuscripts for the conclave library.",
         "item_id": "manuscript_common", "count": 3, "prestige": 5, "gold": 40},
        {"tier": 0, "kind": "study",   "summary": "Bring {n} parchments for the scholar-knights.",
         "item_id": "parchment_fine", "count": 6, "prestige": 4, "gold": 30},
        {"tier": 1, "kind": "study",   "summary": "Submit {n} fine manuscripts as a defended thesis.",
         "item_id": "manuscript_fine", "count": 2, "prestige": 10, "gold": 80},
        {"tier": 2, "kind": "study",   "summary": "The Argued Cut: win {n} bouts answering stroke for stroke.",
         "item_id": None, "count": 2, "prestige": 14, "gold": 100, "kill_kind": "joust_win"},
        {"tier": 3, "kind": "study",   "summary": "Bring {n} rare manuscripts — the Lamp-Lit Conclave requires them.",
         "item_id": "manuscript_rare", "count": 2, "prestige": 22, "gold": 220},
    ],
    "berserker": [
        {"tier": 0, "kind": "trophy",  "summary": "Bring {n} wolf pelts — fresh, from your own kill.",
         "item_id": "wolf_pelt", "count": 3, "prestige": 5, "gold": 40},
        {"tier": 1, "kind": "trophy",  "summary": "Bring {n} bear pelts torn down with axe and tooth.",
         "item_id": "bear_pelt", "count": 3, "prestige": 9, "gold": 90},
        {"tier": 2, "kind": "duel",    "summary": "Win {n} bouts on the red pit — no parry, no retreat.",
         "item_id": None, "count": 2, "prestige": 14, "gold": 80, "kill_kind": "joust_win"},
        {"tier": 3, "kind": "trophy",  "summary": "The Howling: bring {n} bear pelts AND win {n2} bouts (back-to-back tasks).",
         "item_id": "bear_pelt", "count": 5, "prestige": 24, "gold": 180},
    ],
    "horde": [
        {"tier": 0, "kind": "raid",    "summary": "Bring {n} bows back from the steppe-rider's hunt.",
         "item_id": "bow", "count": 2, "prestige": 5, "gold": 35},
        {"tier": 1, "kind": "raid",    "summary": "Bring {n} horse hides for the clan-felt.",
         "item_id": "horse_pelt", "count": 2, "prestige": 9, "gold": 80},
        {"tier": 2, "kind": "raid",    "summary": "The Eagle-Wing drill: win {n} mounted bouts.",
         "item_id": None, "count": 2, "prestige": 13, "gold": 90, "kill_kind": "joust_win"},
        {"tier": 3, "kind": "raid",    "summary": "Bring {n} horse hides for the Khan's great yurt.",
         "item_id": "horse_pelt", "count": 5, "prestige": 22, "gold": 200},
    ],
    "cataphract": [
        {"tier": 0, "kind": "tribute", "summary": "Bring {n} iron lances for the line drill.",
         "item_id": "lance_shaft", "count": 5, "prestige": 5, "gold": 45},
        {"tier": 1, "kind": "tribute", "summary": "Deliver {n} jousting plates to the chapter armory.",
         "item_id": "armor_jousting_chestplate", "count": 1, "prestige": 9, "gold": 90},
        {"tier": 2, "kind": "duel",    "summary": "Hold the Iron Wall: win {n} bouts without breaking line.",
         "item_id": None, "count": 3, "prestige": 16, "gold": 110, "kill_kind": "joust_win"},
        {"tier": 3, "kind": "tribute", "summary": "Bring {n} sets of full jousting plate for the eastern wall garrison.",
         "item_id": "armor_jousting_chestplate", "count": 3, "prestige": 24, "gold": 280},
    ],
    "bushi": [
        {"tier": 0, "kind": "tribute", "summary": "Bring {n} silk bolts for the lord's banner.",
         "item_id": "silk", "count": 4, "prestige": 5, "gold": 50},
        {"tier": 1, "kind": "duel",    "summary": "Win {n} bouts in the lord's name — one cut, one word.",
         "item_id": None, "count": 1, "prestige": 9, "gold": 60, "kill_kind": "joust_win"},
        {"tier": 2, "kind": "tribute", "summary": "Deliver {n} rare manuscripts of the founder's school.",
         "item_id": "manuscript_rare", "count": 1, "prestige": 14, "gold": 150},
        {"tier": 3, "kind": "duel",    "summary": "Itto-Ryu: end {n} bouts each in a single decisive stroke.",
         "item_id": None, "count": 3, "prestige": 22, "gold": 140, "kill_kind": "joust_win"},
    ],
    "furusiyya": [
        {"tier": 0, "kind": "study",   "summary": "Bring {n} bows for the Three-Art drill.",
         "item_id": "bow", "count": 2, "prestige": 5, "gold": 40},
        {"tier": 1, "kind": "tribute", "summary": "Deliver {n} sabres for the master's inspection.",
         "item_id": "sword", "count": 2, "prestige": 9, "gold": 75},
        {"tier": 2, "kind": "duel",    "summary": "The Crescent Games: win {n} mounted bouts at the prayer hours.",
         "item_id": None, "count": 2, "prestige": 14, "gold": 100, "kill_kind": "joust_win"},
        {"tier": 3, "kind": "tribute", "summary": "Bring {n} sets of jousting plate and {n2} sabres for the Sultan's review.",
         "item_id": "armor_jousting_chestplate", "count": 2, "prestige": 22, "gold": 240},
    ],
    "rajput": [
        {"tier": 0, "kind": "tribute", "summary": "Bring {n} tulwars polished and oiled for the founder's hall.",
         "item_id": "sword", "count": 2, "prestige": 5, "gold": 50},
        {"tier": 1, "kind": "raid",    "summary": "Bring {n} bear pelts — a Rajput's mark.",
         "item_id": "bear_pelt", "count": 2, "prestige": 10, "gold": 95},
        {"tier": 2, "kind": "duel",    "summary": "The Tulwar-and-Tear: win {n} bouts giving no ground.",
         "item_id": None, "count": 2, "prestige": 15, "gold": 120, "kill_kind": "joust_win"},
        {"tier": 3, "kind": "tribute", "summary": "Dussehra parade: deliver {n} silk bolts for the founder's banner.",
         "item_id": "silk", "count": 6, "prestige": 22, "gold": 220},
    ],
}
_DEFAULT_QUESTS = ORDER_QUEST_POOLS["errant"]


# Promotion ceremony flavor — keyed by tradition, indexed by rank promoted TO.
# Surfaced when the player crosses a rank threshold at quest turn-in.
PROMOTION_CEREMONY = {
    "errant":      ["girded with a road-stained spur at a crossroads cairn",
                    "named Knight-Errant under the open sky",
                    "given a banneret stitched from four hearths' wool",
                    "raised to Marshal of the Road — no hall, only horizon",
                    "named Grandmaster of the Wandering Order"],
    "templar":     ["robed in the white surcoat at first light",
                    "knighted after an all-night vigil before the altar",
                    "given the banneret blessed by the chaplain",
                    "named Marshal of the Vigil",
                    "made Grandmaster — the saint's hand upon yours"],
    "hospitaller": ["bound with the white sash of the almonry",
                    "knighted before the chapter's wounded",
                    "given the banneret of the Mended Hand",
                    "named Marshal of the Almonry",
                    "raised to Grandmaster of Mercy"],
    "cavalier":    ["dubbed by the King's own sword at court",
                    "knighted at the Coronation Feast",
                    "given the royal banneret at the King's Lists",
                    "named Marshal of the Crown",
                    "raised to Royal Grandmaster"],
    "mercenary":   ["signed into the ledger in blood",
                    "given a free lance and the captain's cup",
                    "named a banneret — your name on the muster-roll",
                    "raised to Marshal — half the season's purse is yours",
                    "made Captain of Captains"],
    "marcher":     ["given the warden's lance at the border beacon",
                    "named Knight of the March — beacons lit for you",
                    "given the banneret of the watch-line",
                    "raised to Marshal of the March",
                    "made Grandmaster — every beacon yours to command"],
    "magisterial": ["sworn after a thesis in arms before the conclave",
                    "named Knight of the Argued Cut",
                    "given the banneret of the founder's scroll-case",
                    "raised to Marshal of the Conclave",
                    "made Grandmaster — the library bears your name"],
    "berserker":   ["scarred and named at the red pit",
                    "knighted with first-blood drawn against the senior",
                    "given the banneret torn from the last foe",
                    "raised to Wolf-Marshal",
                    "made Wolf-Lord — the Howling moon is yours"],
    "horde":       ["given the felt-tunic of the clan-rider",
                    "named Arban-Rider after the First Hunt",
                    "raised to Mingghan-Captain at Naadam",
                    "named Bahadur — Khan-in-waiting",
                    "raised to Khan over felt and arrow"],
    "cataphract":  ["given the kontos at the eastern wall",
                    "knighted in the Sun-Vigil",
                    "raised to Strator at Nowruz of Lances",
                    "named Marshal of the Iron Wall",
                    "made Shah of the Sun-Court"],
    "bushi":       ["topknot cut and katana bound at genpuku",
                    "named retainer of the lord — the dojo bows",
                    "raised to Mounted Bushi",
                    "named Marshal of the Itto-Ryu",
                    "raised to Shōgun of the school"],
    "furusiyya":   ["named after the Five Arts examination",
                    "given the sabre and the master's nod",
                    "raised to Faris of the chapter",
                    "named Mamluk of the Crescent",
                    "made Sultan of the Riding Schools"],
    "rajput":      ["marked at the brow with vermilion and tulwar",
                    "named Kshatri of the Threshold Cut",
                    "raised to Garh-Sirdar — keeper of the founder's tulwar",
                    "named Maharana-in-waiting",
                    "raised to Maharana of the Order"],
}


def promotion_ceremony_line(tradition: str, new_rank_idx: int) -> str:
    pool = PROMOTION_CEREMONY.get(tradition, PROMOTION_CEREMONY["errant"])
    idx = max(0, min(new_rank_idx, len(pool) - 1))
    return pool[idx]


def order_for_town(town_id: int, bx: Optional[int] = None):
    """Return the KnightlyOrder seated in (or aligned with) the town nearest
    to the chapter house. Always returns *some* order if the world has any
    regions (or charters one on demand) — chapter houses are never empty.

    - `town_id` is the NPC's identity-track town id (used only for the rng
      seed so the choice is stable across reloads).
    - `bx` is the chapter house's world-x. When provided, the town is
      resolved by *position* (nearest TOWN to bx), matching how outposts
      used to resolve their region. Falling back to TOWNS.get(town_id)
      handles callers that don't pass bx.
    """
    rng = random.Random(town_id * 7331 + 17)
    try:
        from towns import TOWNS, REGIONS
    except Exception:
        TOWNS, REGIONS = {}, {}

    town = None
    if bx is not None and TOWNS:
        town = min(TOWNS.values(), key=lambda t: abs(t.center_bx - bx))
    if town is None:
        town = TOWNS.get(town_id)

    if town is not None:
        local = orders_for_region(town.region_id)
        if local:
            return rng.choice(local)
        region = REGIONS.get(town.region_id)
        if region is not None:
            # Lazy-seed: charter one order for this region so the chapter
            # house has someone seated. Uses the town_id as part of the
            # rng seed so a region newly hosting a chapter house gets a
            # stable, region-flavored order.
            order = _lazy_seed_order(region, rng)
            if order is not None:
                return order

    if ORDERS:
        return rng.choice(list(ORDERS.values()))
    return None


def _lazy_seed_order(region, rng: random.Random):
    """Charter a single order for a region on demand (used by order_for_town
    when worldgen didn't seed one for this region). Mirrors the per-region
    block of seed_knightly_orders but trimmed: one order, small roster,
    no rival pairing (the regular seed pass handles that on next load).
    """
    try:
        founded = rng.randint(50, 470)
        order = _new_order(rng, region, founded)
        order.historical_events = _generate_historical_events(
            rng, order, founded, current_year=500)
        order.prestige = min(100, order.prestige
                             + min(40, len(order.historical_events) * 3))
        # Small roster so the order feels populated (Grandmaster + a few).
        for rank in _rank_roster(rng, rng.randint(3, 5)):
            _new_knight(rng, order, rank)
        return order
    except Exception:
        return None


def roll_order_quest(order_id: int, day: int, rank_idx: int = 0,
                     refresh: int = 0) -> Optional[dict]:
    """Roll a quest template for an order on a given day.

    Filters by tier: a quest of tier T is offered only if rank_idx >= T,
    OR T == rank_idx + 1 (a 'reach' quest one rank above you, picked
    occasionally to give a stretch goal). `refresh` shifts the seed so
    rerolls produce a different roll on the same day.
    """
    o = ORDERS.get(order_id)
    if o is None:
        return None
    pool = ORDER_QUEST_POOLS.get(o.tradition, _DEFAULT_QUESTS)
    eligible = [q for q in pool if q.get("tier", 0) <= rank_idx + 1]
    if not eligible:
        eligible = pool
    rng = random.Random(order_id * 9973 + day * 31 + refresh * 1019)
    tmpl = rng.choice(eligible)
    q = dict(tmpl)
    q["order_id"]   = order_id
    q["day_rolled"] = day
    q["refresh"]    = refresh
    q["summary"]    = tmpl["summary"].format(n=tmpl["count"],
                                              n2=tmpl["count"] // 2 or 1)
    return q


def player_rank_idx(prestige: int) -> int:
    """Rank index by prestige alone (the cap your trials are racing toward)."""
    idx = 0
    for i, threshold in enumerate(RANK_THRESHOLDS):
        if prestige >= threshold:
            idx = i
    return idx


def player_effective_rank_idx(player) -> int:
    """Actual rank — capped by the highest passed trial.

    Each rank above Squire requires a passed trial. The player's
    `passed_trials` counter (stored under order_quests_done is too noisy,
    so we track separately via player.order_passed_trials) gates the
    label. Falls back gracefully if missing.
    """
    by_prestige = player_rank_idx(getattr(player, "order_prestige", 0))
    passed = int(getattr(player, "order_passed_trials", 0))
    # passed=0 → max rank Squire (0); passed=N → max rank N.
    return min(by_prestige, passed)


def player_rank_label(order_id: int, prestige: int, rank_idx: int = None) -> str:
    """If rank_idx is provided, use it (e.g. effective rank); else fall back
    to prestige-only idx for back-compat with older callers."""
    if rank_idx is None:
        rank_idx = player_rank_idx(prestige)
    rank_idx = max(0, min(rank_idx, len(RANK_NAMES) - 1))
    rank = RANK_NAMES[rank_idx]
    o = ORDERS.get(order_id)
    if o is None:
        return rank
    return cultural_rank_label(o.tradition, rank)


def next_rank_threshold(prestige: int) -> Optional[int]:
    idx = player_rank_idx(prestige)
    if idx + 1 >= len(RANK_THRESHOLDS):
        return None
    return RANK_THRESHOLDS[idx + 1]


# ---------------------------------------------------------------------------
# Rank-up reward grants.
#
# When a player passes a trial and rises in rank within their order, the
# chapter house grants a curated bundle of items appropriate to that new
# rank — induction kit at Knight-Errant, full chapter livery at Banneret,
# command insignia at Marshal, founder relics + royal regalia at Grandmaster.
#
# Each rank's grant has two parts:
#   UNIVERSAL_RANK_REWARDS[rank] — every order grants these.
#   TRADITION_RANK_REWARDS[trad][rank] — extra tradition-flavored items.
# Rank 0 (Squire) is the starting rank — no grant. The lists below cover
# ranks 1..4.
# ---------------------------------------------------------------------------

UNIVERSAL_RANK_REWARDS = {
    # Knight-Errant — induction, basic gear
    1: [
        "livery_squire_sash", "seal_squire_brand",
        "training_pell_post", "training_wooden_sword", "training_wooden_lance",
        "training_riding_pad", "training_ankle_weights", "training_dust_ring",
        "training_form_chart", "training_quintain",
        "book_initiation_rite", "document_oath_letter", "seal_oath_wax", "oath_ring",
        "pilgrims_cloak_token", "document_safe_conduct",
        "drink_chapter_ale", "feast_chapter_pie",
        "field_water_skin", "field_horse_brush", "field_scribes_kit",
        "medicine_blood_stop", "medicine_chapter_balm",
        "map_chapter_holdings",
    ],
    # Knight-Banneret — full chapter member
    2: [
        "livery_chapter_surcoat",
        "document_knight_pass", "document_chapter_dispatch",
        "seal_chapter_wax",
        "book_chapter_chronicle", "book_blade_forms", "book_horse_lore",
        "field_chapter_brazier", "field_chapter_cookpot", "field_farriers_kit",
        "medicine_burn_salve", "medicine_pain_powder", "medicine_splint_kit",
        "feast_beacon_porridge", "drink_beacon_grog",
        "chronicle_great_tilts",
        "map_tournament_circuit", "map_march_borders",
        "ledger_armory", "ledger_horse_tally",
        "instrument_chapter_horn",
    ],
    # Marshal — leadership
    3: [
        "livery_marshal_sash",
        "seal_marshal", "document_field_dispatch", "document_quartering_order",
        "document_summons",
        "book_oath_register", "book_funeral_rite", "book_festival_calendar",
        "standard_pay_pole", "standard_march_beacon", "standard_royal_pennon",
        "field_armorers_anvil", "field_chapter_chest", "field_grinding_stone",
        "field_marching_tent",
        "medicine_eye_drops", "medicine_recovery_tonic", "medicine_herbalist_chest",
        "chronicle_rivalries",
        "feast_pay_day_stew", "feast_lamplit_cake",
        "drink_lamplit_mead", "drink_pay_day_grog",
        "instrument_war_drum",
        "chapter_keys", "order_ledger", "order_charter",
        "shrine_portable",
        "trophy_broken_helm", "trophy_dented_gauntlet", "trophy_severed_plume",
    ],
    # Grandmaster — founder relics + royal regalia
    4: [
        "livery_grandmaster_collar", "livery_royal_mantle",
        "seal_grandmaster", "seal_treaty",
        "document_treaty_inter", "document_writ_of_pardon", "document_writ_of_truce",
        "document_writ_of_war", "document_charter_renewal", "document_ransom_demand",
        "document_excommunication", "document_recantation",
        "standard_red_hearth", "standard_quill_and_lance",
        "chronicle_founder",
        "founders_broken_lance", "founders_helm", "founders_signet",
        "dynasty_first_lance", "dynasty_founders_boots", "dynasty_founders_gloves",
        "dynasty_founders_tooth",
        "saints_knucklebone", "royal_gauntlet_keepsake",
        "trophy_grandmaster_glove", "trophy_captured_pennant", "trophy_horsetail_taken",
        "vassal_seal",
        "reliquary_brass_box", "reliquary_cedar_chest",
        "reliquary_glass_phial", "reliquary_lacquer_case",
        "ledger_tithe_book",
        "drink_blood_wine", "drink_coronation_wine", "drink_pilgrim_water",
        "drink_soma_ceremonial",
        "feast_coronation_roast", "feast_pilgrim_bread", "feast_howling_haunch",
        "censer_of_vigil", "incense_chapter",
    ],
}

TRADITION_RANK_REWARDS = {
    "errant": {
        1: ["livery_warden_cloak"],
        2: ["standard_errant_bough", "book_errant_road_book"],
        3: ["map_pilgrim_routes"],
        4: [],
    },
    "templar": {
        1: ["prayer_beads_rosary", "blessing_water_dawn"],
        2: ["standard_templar_cross", "book_templar_rule"],
        3: ["blessing_oil_chrism"],
        4: ["blessing_oil_saint", "blessing_water_holy"],
    },
    "hospitaller": {
        1: ["livery_pilgrim_robe", "blessing_oil_rose"],
        2: ["standard_hospitaller_lily"],
        3: [],
        4: [],
    },
    "cavalier": {
        1: ["book_cavalier_court_codex"],
        2: [],
        3: ["dynasty_herald_tabard", "dynasty_parade_lance"],
        4: ["dynasty_coronation_robe", "dynasty_state_robe"],
    },
    "mercenary": {
        1: ["livery_lances_tabard"],
        2: [],
        3: [],
        4: ["livery_red_war_paint"],
    },
    "marcher": {
        1: ["livery_warden_cloak"],
        2: [],
        3: [],
        4: [],
    },
    "magisterial": {
        1: ["livery_scholar_stole"],
        2: [],
        3: [],
        4: [],
    },
    "samurai": {
        1: ["prayer_beads_juzu"],
        2: ["shrine_obo"],
        3: [],
        4: ["yari_lance_head"],
    },
    "ghazi": {
        1: ["prayer_beads_misbaha"],
        2: [],
        3: ["rumh_lance_head"],
        4: ["shamshir_blade"],
    },
    "rajput": {
        1: [],
        2: [],
        3: ["kund_lance_head"],
        4: [],
    },
    "horde": {
        1: [],
        2: [],
        3: ["ban-pou_lance_head", "dao_blade"],
        4: [],
    },
}


def grant_rank_rewards(player, tradition: str, new_rank: int) -> list:
    """Add rank-appropriate items to player.inventory.

    Returns the list of (item_id, count) granted so the UI can flash them.
    new_rank is the rank the player has just been raised to (1..4).
    """
    inv = getattr(player, "inventory", None)
    if inv is None:
        return []
    grants = []
    universal = UNIVERSAL_RANK_REWARDS.get(new_rank, [])
    tradition_extra = TRADITION_RANK_REWARDS.get(tradition, {}).get(new_rank, [])
    for item_id in list(universal) + list(tradition_extra):
        inv[item_id] = inv.get(item_id, 0) + 1
        grants.append((item_id, 1))
    return grants


# ---------------------------------------------------------------------------
# Quartermaster shop — items the chapter house quartermaster will sell back
# to members who missed them on rank-up or want duplicates. Gated by player
# rank: a Marshal can browse Squire/Errant/Banneret/Marshal stock; only a
# Grandmaster can buy from the Grandmaster shelf.
#
# Prices roughly: rank-1 commons = 8-20g, rank-2 = 25-60g, rank-3 = 80-150g,
# rank-4 founder relics = 250-500g.
# ---------------------------------------------------------------------------

QUARTERMASTER_OFFERS = {
    # Rank 1 stock — induction kit + duplicates of trial-room basics
    1: [
        ("livery_squire_sash", 10),
        ("training_pell_post", 8),
        ("training_wooden_sword", 8),
        ("training_wooden_lance", 12),
        ("training_riding_pad", 10),
        ("training_quintain", 15),
        ("training_ankle_weights", 8),
        ("training_dust_ring", 10),
        ("training_form_chart", 6),
        ("book_initiation_rite", 14),
        ("document_oath_letter", 8),
        ("seal_oath_wax", 6),
        ("oath_ring", 18),
        ("pilgrims_cloak_token", 12),
        ("document_safe_conduct", 10),
        ("field_water_skin", 6),
        ("field_horse_brush", 8),
        ("field_scribes_kit", 14),
        ("medicine_blood_stop", 10),
        ("medicine_chapter_balm", 12),
        ("drink_chapter_ale", 6),
        ("feast_chapter_pie", 10),
        ("map_chapter_holdings", 15),
        ("seal_squire_brand", 8),
    ],
    # Rank 2 stock — chapter livery, mid-tier docs & gear
    2: [
        ("livery_chapter_surcoat", 60),
        ("document_knight_pass", 28),
        ("document_chapter_dispatch", 22),
        ("seal_chapter_wax", 18),
        ("book_chapter_chronicle", 32),
        ("book_blade_forms", 36),
        ("book_horse_lore", 30),
        ("field_chapter_brazier", 28),
        ("field_chapter_cookpot", 24),
        ("field_farriers_kit", 30),
        ("medicine_burn_salve", 28),
        ("medicine_pain_powder", 26),
        ("medicine_splint_kit", 32),
        ("feast_beacon_porridge", 22),
        ("drink_beacon_grog", 18),
        ("chronicle_great_tilts", 40),
        ("map_tournament_circuit", 36),
        ("map_march_borders", 32),
        ("ledger_armory", 28),
        ("ledger_horse_tally", 26),
        ("instrument_chapter_horn", 45),
    ],
    # Rank 3 stock — command insignia
    3: [
        ("livery_marshal_sash", 110),
        ("seal_marshal", 95),
        ("document_field_dispatch", 80),
        ("document_quartering_order", 85),
        ("document_summons", 90),
        ("book_oath_register", 95),
        ("book_funeral_rite", 100),
        ("book_festival_calendar", 90),
        ("standard_pay_pole", 120),
        ("standard_march_beacon", 130),
        ("standard_royal_pennon", 140),
        ("field_armorers_anvil", 100),
        ("field_chapter_chest", 90),
        ("field_grinding_stone", 85),
        ("field_marching_tent", 110),
        ("medicine_eye_drops", 95),
        ("medicine_recovery_tonic", 100),
        ("medicine_herbalist_chest", 130),
        ("chronicle_rivalries", 110),
        ("feast_pay_day_stew", 80),
        ("feast_lamplit_cake", 90),
        ("drink_lamplit_mead", 85),
        ("drink_pay_day_grog", 80),
        ("instrument_war_drum", 130),
        ("chapter_keys", 95),
        ("order_ledger", 110),
        ("order_charter", 140),
        ("shrine_portable", 120),
        ("seal_rivalry_token", 90),
    ],
    # Rank 4 stock — founder relics & royal regalia (very expensive)
    4: [
        ("livery_grandmaster_collar", 380),
        ("livery_royal_mantle", 420),
        ("seal_grandmaster", 300),
        ("seal_treaty", 280),
        ("document_treaty_inter", 250),
        ("document_writ_of_pardon", 280),
        ("document_writ_of_truce", 270),
        ("document_writ_of_war", 320),
        ("document_charter_renewal", 240),
        ("document_ransom_demand", 220),
        ("document_excommunication", 290),
        ("document_recantation", 240),
        ("standard_red_hearth", 360),
        ("standard_quill_and_lance", 340),
        ("chronicle_founder", 380),
        ("founders_broken_lance", 420),
        ("founders_helm", 480),
        ("founders_signet", 500),
        ("saints_knucklebone", 360),
        ("royal_gauntlet_keepsake", 340),
        ("trophy_grandmaster_glove", 320),
        ("trophy_captured_pennant", 280),
        ("trophy_horsetail_taken", 270),
        ("vassal_seal", 300),
        ("reliquary_brass_box", 320),
        ("reliquary_cedar_chest", 340),
        ("reliquary_glass_phial", 280),
        ("reliquary_lacquer_case", 360),
        ("ledger_tithe_book", 260),
        ("drink_blood_wine", 220),
        ("drink_coronation_wine", 240),
        ("drink_pilgrim_water", 200),
        ("drink_soma_ceremonial", 260),
        ("feast_coronation_roast", 240),
        ("feast_pilgrim_bread", 200),
        ("feast_howling_haunch", 220),
        ("censer_of_vigil", 280),
        ("incense_chapter", 220),
    ],
}


def quartermaster_offers_for_rank(rank_idx: int) -> list:
    """Return [(item_id, price, min_rank)] for everything the player can buy.

    Offers from lower ranks are unlocked too — a Marshal sees Squire–Marshal
    stock. Items already in `min_rank` order so the UI groups easily.
    """
    out = []
    for r in range(1, min(rank_idx, 4) + 1):
        for item_id, price in QUARTERMASTER_OFFERS.get(r, []):
            out.append((item_id, price, r))
    return out


def quartermaster_buy(player, item_id: str, price: int) -> bool:
    """Charge the player and grant one of the item. Returns False if can't afford."""
    money = int(getattr(player, "money", 0))
    if money < price:
        return False
    inv = getattr(player, "inventory", None)
    if inv is None:
        return False
    player.money = money - price
    inv[item_id] = inv.get(item_id, 0) + 1
    return True


# ---------------------------------------------------------------------------
# Standing labels — narrative texture on top of raw prestige.
# ---------------------------------------------------------------------------

STANDING_TIERS = [
    (0,    "Initiate"),
    (10,   "Sworn"),
    (30,   "Bonded"),
    (70,   "Honored"),
    (150,  "Exalted"),
    (250,  "Storied"),
]


def standing_label(prestige: int) -> str:
    label = STANDING_TIERS[0][1]
    for floor, name in STANDING_TIERS:
        if prestige >= floor:
            label = name
    return label


# ---------------------------------------------------------------------------
# Vows — chosen at petition. Each held vow gives +1 prestige per quest
# turn-in. Vow text is drawn from the order's own vow list plus the
# tradition vow_pool. Picking 2 of 4 is the typical flow.
# ---------------------------------------------------------------------------

VOW_PRESTIGE_BONUS = 1   # per vow held, added to every quest turn-in


def candidate_vows_for_order(order_id: int, k: int = 4) -> list:
    """Return up to k vow strings the player can choose from at petition.

    Mixes the order's own vows with extras from the tradition pool so the
    player sees real choices, not just the auto-rolled set on the order.
    """
    o = ORDERS.get(order_id)
    if o is None:
        return []
    seen = set()
    out = []
    for v in (o.vows or []):
        if v not in seen:
            out.append(v)
            seen.add(v)
    pool = ORDER_TRADITIONS.get(o.tradition, {}).get("vow_pool", [])
    for v in pool:
        if v not in seen and len(out) < k:
            out.append(v)
            seen.add(v)
    return out[:k]


def vow_prestige_bonus(player_vows) -> int:
    if not player_vows:
        return 0
    return VOW_PRESTIGE_BONUS * len(player_vows)


# ---------------------------------------------------------------------------
# Rank Trials — every rank-up requires both prestige AND a specific trial.
# Trials surface the existing tradition ritual layer as gameplay.
# ---------------------------------------------------------------------------

# Trial requirement kinds:
#   joust_win:      win N tournament bouts after the trial is opened
#   joust_pennant:  win N bouts under THIS order's pennant
#   tribute:        deliver N of item_id
# Trials are keyed by destination rank (1..4). Rank 0 (Squire) is automatic.
# Each entry: (label, kind, count, item_id_or_none, flavor)
RANK_TRIALS = {
    1: ("Trial of the Initiate", "tribute", 1, "tournament_pennant",
        "Bring a single tournament pennant to the seat — proof you've stood in the lists."),
    2: ("Trial of the Lance",    "joust_win", 1, None,
        "Win a single tournament bout after the trial is opened."),
    3: ("Trial of the Marshal",  "joust_win", 3, None,
        "Win three tournament bouts to prove your sword is the order's own."),
    4: ("Trial of the Grandmaster", "joust_pennant", 1, None,
        "Win a tournament under this order's pennant. Nothing less."),
}


def rank_trial_for(prestige_threshold_met_rank_idx: int):
    """Return the trial tuple required for the given destination rank, or None."""
    return RANK_TRIALS.get(prestige_threshold_met_rank_idx)


# ---------------------------------------------------------------------------
# Rivalry — tournaments and orders fan an old grudge.
# ---------------------------------------------------------------------------

def is_rival_pair(order_id_a: int, order_id_b: int) -> bool:
    if not order_id_a or not order_id_b or order_id_a == order_id_b:
        return False
    a = ORDERS.get(order_id_a)
    b = ORDERS.get(order_id_b)
    if a and a.rival_id == order_id_b:
        return True
    if b and b.rival_id == order_id_a:
        return True
    return False
