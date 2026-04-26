"""
towns.py — Town and Region state, day-tick growth, supply logic.
Mirrors cities.py (geometry) but holds persistent town *identity*.
"""

import json
import random
from dataclasses import dataclass, field
from typing import Optional

import heraldry
from town_needs import (
    TOWN_CATEGORIES, BASE_NEED_AMOUNT, GOLD_PER_UNIT,
    REP_PER_NEED_FILLED, ITEM_TO_CATEGORY,
    LUXURY_CATEGORIES, BASE_NEED_AMOUNT_LUXURY, REP_PER_LUXURY_FILLED,
    LUXURY_VARIANT_POOLS, PREFERRED_BONUS_MULT,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DAYS_PER_TIER   = 5      # full-need days needed to tier up
REGION_SIZE     = 3      # towns per region

TIER_NAMES = ["Hamlet", "Village", "Town", "City"]

# ---------------------------------------------------------------------------
# Name pools
# ---------------------------------------------------------------------------

_PREFIXES = [
    "Ash", "Birch", "Cedar", "Dark", "Elder", "Fern", "Glen", "Hawk",
    "Iron", "Jade", "Kale", "Larch", "Moss", "North", "Oak", "Pine",
    "Red", "Stone", "Thorn", "Vale", "Willow",
    "Acacia", "Amber", "Baobab", "Copper", "Dawn", "Ebony", "Flint",
    "Ginkgo", "Gold", "Hibiscus", "Indigo", "Ivory", "Lotus",
    "Mahogany", "Neem", "Saffron", "Teak", "Umber",
]
_SUFFIXES = [
    "brook", "bury", "cliff", "dale", "field", "ford", "gate",
    "haven", "hold", "hurst", "keep", "moor", "reach", "ridge",
    "shire", "stead", "ton", "vale", "wick",
    "abad", "dhar", "ghat", "grad", "holm", "mar", "pur", "vara",
]
_BIOME_GROUP: dict[str, str] = {
    "temperate": "forest",    "boreal": "forest",
    "birch_forest": "forest", "redwood": "forest",
    "jungle": "jungle",       "tropical": "jungle",
    "wetland": "wetland",     "swamp": "wetland",
    "desert": "desert",
    "arid_steppe": "silk_road",   "savanna": "arabia",
    "rolling_hills": "levant",    "steep_hills": "persia",
    "alpine_mountain": "alpine", "tundra": "alpine",    "rocky_mountain": "alpine",
    "steppe": "steppe",       "wasteland": "steppe",
    "canyon": "yunnan",
    "beach": "coastal",
    "mediterranean": "mediterranean",
    "east_asian":    "east_asian",
    "south_asian":   "south_asian",
}
_DEFAULT_BIOME_GROUP = "highland"

_REGION_NAMES_BY_GROUP: dict[str, list[str]] = {
    "forest":   ["Ashenveil","Greywood","Brackenmoor","Fernhollow","Birchmore",
                 "Oldwood","Oakmere","Yewdale","Timbervast","Elmhurst",
                 "Kestrelwood","Lochvale","Embervast",
                 # Slavic / Nordic / East European / East Asian inflected
                 "Zelenmoor","Borova","Skovheim","Bjornveil","Shiromori",
                 "Cedrova","Rowanholm","Nyirveil","Dubglen","Lesnaya",
                 "Koivisto","Hvitskog","Brinyveld","Sekizan","Kasumiwood"],
    "jungle":   ["Fernwood","Deepcanopy","Mossveil","Rootmere","Greenhollow",
                 "Tanglemark","Ivywood","Verdantshire","Deepgrove","Thornveil",
                 "Jademark","Duskhollow",
                 # African / Amazonian / Southeast Asian inflected
                 "Rimbakar","Mbokawood","Varzmere","Tapajore","Savukadale",
                 "Hutanholm","Kalamark","Amazura","Kongomere","Kapokdale",
                 "Selvareach","Iguacuveil","Itaubamark","Ngiriwood"],
    "wetland":  ["Mirewood","Reedholm","Bogmere","Marshgate","Foghollow",
                 "Fenwick","Mistmere","Watershire","Deepfen","Mudvast",
                 "Vantmoor","Halvenmere",
                 # Nile / Mekong / Ganges / Amazon inflected
                 "Mekongate","Gangramere","Papyrusveil","Suddholm",
                 "Orinomere","Baikalmoor","Deltamere","Mahakamfen",
                 "Niloticfen","Chadmere","Pantanalvast","Irrawaddygate"],
    "desert":   ["Dunemark","Sandveil","Scorchfield","Emberreach","Ashrock",
                 "Goldsand","Ironstone","Copperveil","Drysward","Dustholm",
                 "Cinderfall","Umberveil",
                 # Arabian / Berber / Gobi / Atacama / Thar inflected
                 "Wadisand","Nefudmark","Ergsward","Kobiveil","Qarastone",
                 "Taklafeld","Atacamark","Nubiareach","Sahelveil","Khamseen",
                 "Hammadaveil","Tharstone","Regalmark","Namibvast","Karakumfeld"],
    "alpine":   ["Frostholm","Glaciergate","Snowpeak","Icevast","Coldspire",
                 "Stonecrown","Highwall","Wintermere","Icemark","Frostgate",
                 "Frostmere","Ironstead",
                 # Himalayan / Andean / Tibetan / Caucasus / Altai inflected
                 "Dhaurigate","Pachamark","Intihold","Simienkeep","Altaiholm",
                 "Cordilmark","Kiligate","Elbruzhold","Makalauveil","Tianpass",
                 "Kazbegvast","Potalagate","Huascaran","Illimanihold"],
    "steppe":   ["Dustmoor","Windreach","Flatstone","Plainsmere","Dryfield",
                 "Dustgate","Windholm","Greystone","Barrensward","Stonefield",
                 "Thornwall","Westbrook",
                 # Mongolian / Central Asian / Pontic / Ukrainian inflected
                 "Khangaireach","Tuulholm","Qyzylfield","Orkhonmere","Dobroplain",
                 "Tengrimark","Saraireach","Ponticgate","Uralfield","Stepnemark",
                 "Dzungarvast","Karakumplain","Targitaymere","Pechenegholm"],
    "coastal":  ["Saltmere","Tidehollow","Wavemark","Driftgate","Shellstone",
                 "Beachholm","Tidegate","Sandhollow","Coralveil","Foamreach",
                 "Northgate","Ardenvale",
                 # Polynesian / Caribbean / Swahili / Pacific inflected
                 "Atolmark","Moanagate","Kilwaveil","Malindisand","Caribshore",
                 "Tongaholm","Zanzimark","Kahuluiveil","Lagunareach","Swahishore",
                 "Marquesagate","Cibaomark","Javansea","Mandalayveil","Reefsward"],
    "highland": ["Peakshire","Ridgemere","Hillmark","Craghollow","Moorgate",
                 "Stoneback","Highmere","Cliffdale","Ridgeholm","Brokenstone",
                 "Quarrymere","Ossenfield",
                 # Ethiopian / Andean / Appalachian / Caucasus inflected
                 "Simienmark","Amharakeep","Punafield","Caucasmere","Colcaholm",
                 "Ozarkridge","Drakensmoor","Balemere","Altiplegate",
                 "Balochholm","Zagroskeep","Lesothomere","Appalacmark"],
    "mediterranean": ["Aurelia","Campania","Iberia","Baetica","Achaea","Attica",
                      "Laconia","Liguria","Etruria","Apulia","Dalmatia","Lusitania",
                      "Calabria","Bithynia","Hellas",
                      # North African / Levantine / Anatolian inflected
                      "Carthago","Leptis","Cyrene","Palmyra","Antioch",
                      "Kairouan","Almeria","Alcazara","Ephesia","Petra",
                      "Byblosia","Tingis","Sabrata","Caesarea"],
    "east_asian":    ["Longshan","Jadewater","Dragoncoast","Moonshore","Bamboohill",
                      "Crimsonriver","Cloudhaven","Silkdale","Lotusmere","Ivorygate",
                      "Cedarholm","Inkwater","Cherryreach",
                      "Longmen","Qinglong","Fenghuang","Zijincheng","Baihe",
                      "Sakuraholm","Fujimere","Tsukireach","Kirihaven","Momijivale",
                      "Goldencourt","Dragontower","Jadepalace","Redgate","Craneshore",
                      # Korean / Vietnamese / Tibetan / Thai inflected
                      "Hanraveil","Goryeomark","Champagate","Sukhothaivast",
                      "Pothalaholm","Dongsanmere","Baekdugate","Annamshore"],
    "arabia":        ["Sandsong","Oasismark","Palmshadow","Wellgate","Dunestar",
                      "Wadiveil","Hadhramark","Najdreach","Hejazshore","Qahtanhold",
                      "Yemengate","Incensevast","Frankholm","Myrrhmere","Maskatshore",
                      "Omayvast","Khalijmark","Beduinveil","Nabatamark","Dhofarreach"],
    "levant":        ["Cedargate","Phoenixshore","Tyreveil","Sidonmark","Jordanfold",
                      "Olivemere","Scriptvast","Purplecoast","Libanholm","Orontisreach",
                      "Palmyraveil","Aleppoveil","Caravanmark","Citadelmark","Byblosgate",
                      "Hamahold","Ugaritmark","Saltwaymark","Canaanveil","Ashkereach"],
    "persia":        ["Rosewater","Saffronvale","Azuregate","Shirazmark","Zagrosmere",
                      "Isfahanveil","Parsahold","Parthmark","Khorasangate","Farsveil",
                      "Ecbatanmark","Sogdmark","Mediamere","Elamreach","Sassanhold",
                      "Ctesivast","Bactraveil","Persepmark","Transoxmark","Hyrcmark"],
    "yunnan":        ["Jadegorge","Stoneforest","Cloudpeak","Copperveil","Dragonpool",
                      "Lotusshore","Flowerseamere","Mosscanyon","Peacockvale","Silversong",
                      "Erhaimark","Jinshajing","Cangmountain","Yuganghold","Lugumere",
                      "Dalireach","Lijianggate","Tengchongveil","Xishuanvast","Nujiangdeep"],
    "silk_road":     ["Jadegate","Oasisholm","Camelpass","Desertstar","Stonemural",
                      "Dunhuangmark","Loulanveil","Kashgarreach","Turpangate","Khotanford",
                      "Yumenpass","Gansuvast","Dunqiumark","Shazhougate","Luntaihold",
                      "Qiemofield","Ruoqiangveil","Yumenguan","Grottovast","Beaconfire"],
    "south_asian":   ["Devapura","Suryanagar","Nagarjuna","Chandramukhi","Krishnagar",
                      "Indravale","Gangashore","Vedaholm","Aryadale","Rajamere",
                      "Lotusfield","Saffrongate","Kalidevi",
                      # Dravidian / Sri Lankan / Bengali / Deccan inflected
                      "Vijayanagar","Kalindra","Dravida","Cherapura","Pandyashore",
                      "Kumaramere","Paravarholm","Somanagar","Cholarealm",
                      "Anuradhaveil","Magadhagate","Kanchipura","Sahyadrihold"],
}

_TAGLINES_BY_GROUP: dict[str, list[str]] = {
    "forest":   ["Known for fine timber and expert woodcraft",
                 "Famed for hunting and forest remedies",
                 "Renowned for deep-wood mushrooms and quiet wisdom",
                 "Known for charcoal burning and ironwood tools",
                 "Known for birch-bark canoe craft and forest river trading",
                 "Famed for resin tapping, pine-tar trade, and carved wooden shrines",
                 "Renowned for smoked game, wild berries, and bark-cloth weaving"],
    "jungle":   ["Rich in rare herbs and exotic birds",
                 "Known for ancient pottery and river trade",
                 "Famed for deep-canopy silks and rare dyes",
                 "Renowned for jungle honey and vine bridges",
                 "Known for cacao trading and bright feathered textiles",
                 "Renowned for rubber harvest and jungle waterway navigation",
                 "Famed for aromatic resin, blowpipe craft, and tree-shrine carvings"],
    "wetland":  ["Known for peat and medicinal reeds",
                 "Famed for river fish and wicker craft",
                 "Renowned for fog-glass and salt extraction",
                 "Known for eel smoking and marsh iron",
                 "Known for papyrus craft and delta grain storage",
                 "Famed for mangrove fishing, tidal salt works, and floating markets",
                 "Renowned for lotus cultivation and river-reed boat building"],
    "desert":   ["Known for spice trade and ancient sandstone ruins",
                 "Renowned for glasswork and long camel routes",
                 "Famed for precious gems and sun-dried goods",
                 "Known for date wine and nomadic law",
                 "Known for ancient aquifer engineering and star-map navigation",
                 "Famed for astronomy, sand-cast bronze, and fortress caravan cities",
                 "Renowned for rare frankincense, dye trade, and oasis hospitality"],
    "alpine":   ["Known for stonecutting and high-altitude sheep",
                 "Famed for fine wool and harsh winters",
                 "Renowned for mountain herbs and glacier ice trade",
                 "Known for goat cheese and fortress masonry",
                 "Known for yak butter trade and high-pass caravan routes",
                 "Famed for alpaca wool weaving and terraced mountainside farming",
                 "Renowned for mountain astronomy, snow-bridge engineering, and cold-smoke curing"],
    "steppe":   ["Known for horse trade and wind-dried meats",
                 "Famed for grassland grain and swift riders",
                 "Renowned for leather work and open-sky stargazing",
                 "Known for bone carving and dry-stone walls",
                 "Known for kumiss brewing and nomadic star navigation",
                 "Famed for felt-making, rapid horse courier networks, and iron stirrups",
                 "Renowned for composite bow craft and great kurgan burial rites"],
    "coastal":  ["Known for salt trade and deep-sea fishing",
                 "Famed for shipbuilding and coastal amber",
                 "Renowned for pearl diving and coral crafts",
                 "Known for smoked fish and tidal herb gardens",
                 "Known for outrigger canoe voyaging and open-ocean star navigation",
                 "Famed for coconut trade, coral stone architecture, and tapa cloth",
                 "Renowned for mangrove charcoal, dhow-building, and tidal fish traps"],
    "highland": ["Known for quarried stone and highland beef",
                 "Famed for ridge-road trade and sturdy ironwork",
                 "Renowned for moorland wool and carved stone",
                 "Known for high pasture cheese and cloudberry mead",
                 "Known for terraced farming, enset cultivation, and hilltop shrines",
                 "Famed for mountain honey, coffee cherry harvest, and weaving cooperatives",
                 "Renowned for dry-stone terracing, llama herding, and freeze-drying techniques"],
    "mediterranean": ["Known for olive oil, fine wine, and sun-baked marble",
                      "Famed for seafaring merchants and painted ceramics",
                      "Renowned for philosophers, poets, and open-air theatre",
                      "Known for terraced vineyards and ancient stone temples",
                      "Known for mosaic tilework, aromatic gardens, and ornate bath culture",
                      "Famed for purple dye trade, glassblowing, and cross-sea merchant fleets",
                      "Renowned for geometric mathematics, star catalogues, and monumental aqueducts"],
    "east_asian":    ["Known for fine silk, painted lacquer, and river trade",
                      "Famed for tea ceremonies and precise brushwork",
                      "Renowned for porcelain craft and mountain monasteries",
                      "Known for cherry blossom festivals and iron casting",
                      "Known for block printing, paper-making, and imperial canal networks",
                      "Famed for lacquerware, shadow-puppet theatre, and incense road trade",
                      "Renowned for bronze bells, kite festivals, and intricate garden design"],
    "arabia":        ["Known for frankincense roads, pearl diving, and camel caravans",
                      "Famed for date wine, Bedouin hospitality, and the incense trade",
                      "Renowned for star navigation across the Empty Quarter",
                      "Known for falcon hunting, tribal law, and ancient well-keeping",
                      "Famed for Nabataean rock-cut cities and desert caravan networks",
                      "Renowned for qahwa ceremony, tent weaving, and lunar calendar craft"],
    "levant":        ["Known for Phoenician purple dye, cedar trade, and sea-glass craft",
                      "Famed for the invented alphabet, merchant law, and deep harbour cities",
                      "Renowned for olive oil, coastal wine, and carved ivory work",
                      "Known for blown glass, coastal shipbuilding, and linen weaving",
                      "Famed for Silk Road crossroads hospitality and ancient scripture",
                      "Renowned for souk markets, aromatic resin, and mosaic tilework"],
    "persia":        ["Known for walled gardens, carpet weaving, and poetry tournaments",
                      "Famed for Achaemenid road networks, astronomy, and fire temples",
                      "Renowned for saffron trade, Sasanian silverwork, and wind-tower craft",
                      "Known for bridge engineering, ice-house cooling, and grape distillation",
                      "Famed for epic verse, royal hunting parks, and glazed tilework",
                      "Renowned for Silk Road commerce, miniature painting, and polo sport"],
    "yunnan":        ["Known for ancient tea trees and the Tea Horse Road caravans",
                      "Famed for marble quarrying, copper smelting, and bright festival dress",
                      "Renowned for peacock silk, wild mushrooms, and gorge-carved salt roads",
                      "Known for medicinal herbs gathered along the Three Parallel Rivers",
                      "Famed for minority craft traditions and highland flower markets",
                      "Renowned for ancient Naxi scrolls, carved jade, and terraced rice"],
    "silk_road":     ["Known for overland caravan trade between East and West",
                      "Famed for painted grottoes, jade cutting, and grape cultivation",
                      "Renowned for oasis hospitality and celestial navigation",
                      "Known for beacon-fire relay stations and imperial garrison posts",
                      "Famed for Sogdian merchants, Buddhist pilgrims, and Tang glazed pottery",
                      "Renowned for wind-dried melon, saffron silk, and ancient mural art"],
    "south_asian":   ["Known for spice roads, sacred rivers, and temple sculpture",
                      "Famed for fine cotton weaving and elaborate festivals",
                      "Renowned for elaborate stonework and aromatic cuisine",
                      "Known for monsoon rice paddies and gold craftsmanship",
                      "Known for stepwell engineering, indigo cultivation, and ivory carving",
                      "Famed for pepper and cardamom sea trade, classical dance, and bell-bronze work",
                      "Renowned for tank irrigation, silk weaving guilds, and carved cave monasteries"],
}

_CHARGES_BY_GROUP: dict[str, list[str]] = {
    "forest":   ["tree", "moon", "eagle", "wolf", "bear", "stag", "fox", "owl",
                 "raven", "arrow", "rose", "acorn", "oak_leaf", "none"],
    "jungle":   ["tree", "fleur", "eagle", "spear", "rose", "serpent",
                 "grapes", "thistle", "none"],
    "wetland":  ["anchor", "fish", "moon", "ship", "bell", "scales",
                 "swan", "frog", "none"],
    "desert":   ["sun", "sword", "star", "spear", "key", "eye",
                 "scorpion", "comet", "hourglass", "none"],
    "alpine":   ["crown", "tower", "cross", "castle", "hammer", "bear", "axe",
                 "snowflake", "mountain", "helmet", "anvil"],
    "steppe":   ["sword", "star", "eagle", "horse", "arrow", "axe",
                 "lance", "lightning", "bull", "none"],
    "coastal":  ["anchor", "fish", "cross", "castle", "ship", "key", "bell",
                 "dolphin", "waves", "trident", "cannon"],
    "highland": ["castle", "tower", "cross", "axe", "hammer", "lion", "wheat",
                 "portcullis", "gate", "buckler", "dagger", "boar", "none"],
    "mediterranean": ["sun", "olive", "ship", "amphora", "laurel", "eagle", "column",
                      "grapes", "fish", "trident", "key", "rose", "none"],
    "east_asian":    ["dragon", "crane", "lotus", "moon", "wave", "phoenix", "bamboo",
                      "mountain", "cloud", "star", "fish", "none"],
    "arabia":        ["camel", "crescent", "star", "palm", "sword",
                      "falcon", "eye", "hourglass", "none"],
    "levant":        ["cedar", "ship", "anchor", "fish", "amphora",
                      "key", "scroll", "waves", "dolphin", "none"],
    "persia":        ["lion", "sun", "star", "peacock", "crown",
                      "rose", "garden", "comet", "none"],
    "yunnan":        ["peacock", "camellia", "mountain", "jade", "phoenix",
                      "cloud", "dragon", "flower", "none"],
    "silk_road":     ["camel", "star", "moon", "sun", "key",
                      "sword", "eye", "comet", "hourglass", "none"],
    "south_asian":   ["lotus", "sun", "elephant", "peacock", "tiger", "wheel",
                      "star", "flower", "serpent", "none"],
}

_LEADER_TITLES: dict[str, tuple[str, str]] = {
    # (masculine, feminine) — randomly assigned at display time
    "forest":   ("Lord",     "Lady"),
    "jungle":   ("Chieftain","Chieftain"),
    "wetland":  ("Elder",    "Elder"),
    "desert":   ("Sultan",   "Sultana"),
    "alpine":   ("Jarl",     "Jarl"),
    "steppe":   ("Khan",     "Khatun"),
    "coastal":  ("Admiral",  "Admiral"),
    "highland":      ("Thane",     "Thane"),
    "mediterranean": ("Consul",    "Consul"),
    "east_asian":    ("Daimyo",    "Lady"),
    "arabia":        ("Emir",      "Emira"),
    "levant":        ("Malik",     "Malika"),
    "persia":        ("Satrap",    "Satrap"),
    "yunnan":        ("Tusi",      "Tusi"),
    "silk_road":     ("Prefect",   "Prefect"),
    "south_asian":   ("Raja",      "Rani"),
}

# ---------------------------------------------------------------------------
# Leader agendas
# ---------------------------------------------------------------------------
# Each region's leader rolls one of these agendas at world-gen. The agenda
# drives which contracts the leader prefers, what gifts curry favor, and
# (at high regional rep) a region-wide buff.
#
# Tags use the same vocabulary as town_needs categories where possible
# (food / wood / stone / metal / weapons / wine / coffee / spirits / pottery /
#  tea / herbs) plus a few region-specialty tags (gems / textiles / spices).

LEADER_AGENDAS: dict[str, dict] = {
    "martial": {
        "label":       "Martial",
        "description": "Hungers for arms, iron, and the spoils of the hunt.",
        "tags":        ("metal", "weapons"),
        "buff":        "martial_arsenal",
    },
    "mercantile": {
        "label":       "Mercantile",
        "description": "Sees worth in spices, gems, and well-traveled goods.",
        "tags":        ("gems", "spices", "pottery", "textiles"),
        "buff":        "mercantile_discount",
    },
    "scholarly": {
        "label":       "Scholarly",
        "description": "Collects books, fossils, and rare brews of leaf and stone.",
        "tags":        ("gems", "tea", "herbs"),
        "buff":        "scholarly_codex",
    },
    "pious": {
        "label":       "Pious",
        "description": "Honors the temple with herbs, candles, and sacred craft.",
        "tags":        ("herbs", "pottery", "wine"),
        "buff":        "pious_blessing",
    },
    "builder": {
        "label":       "Builder",
        "description": "Raises walls and roofs; insatiable for stone and timber.",
        "tags":        ("wood", "stone", "pottery"),
        "buff":        "builder_bonds",
    },
    "hedonist": {
        "label":       "Hedonist",
        "description": "Throws lavish feasts; demands wine, coffee, and rare spirits.",
        "tags":        ("wine", "coffee", "spirits", "food"),
        "buff":        "hedonist_indulgence",
    },
}

# Region specialties — what each biome group naturally produces (cheaper here)
# and what its leader pays a premium for (imports drive contract demand).
BIOME_GROUP_SPECIALTIES: dict[str, dict] = {
    "forest":         {"exports": ("wood", "herbs"),     "imports": ("metal", "spices", "wine")},
    "jungle":         {"exports": ("herbs", "textiles"), "imports": ("metal", "stone", "wine")},
    "wetland":        {"exports": ("herbs", "food"),     "imports": ("metal", "stone", "spirits")},
    "desert":         {"exports": ("gems", "spices"),    "imports": ("wood", "food", "wine")},
    "alpine":         {"exports": ("metal", "stone"),    "imports": ("food", "wine", "textiles")},
    "steppe":         {"exports": ("textiles", "food"),  "imports": ("wood", "metal", "wine")},
    "coastal":        {"exports": ("food", "pottery"),   "imports": ("wood", "metal", "spices")},
    "highland":       {"exports": ("stone", "herbs"),    "imports": ("food", "spices", "textiles")},
    "mediterranean":  {"exports": ("wine", "pottery"),   "imports": ("metal", "wood", "spices")},
    "east_asian":     {"exports": ("tea", "pottery"),    "imports": ("metal", "spices", "wine")},
    "arabia":         {"exports": ("spices", "coffee"),  "imports": ("wood", "metal", "wine")},
    "levant":         {"exports": ("spices", "wine"),    "imports": ("metal", "wood", "pottery")},
    "persia":         {"exports": ("textiles", "spices"),"imports": ("wood", "stone", "wine")},
    "yunnan":         {"exports": ("tea", "herbs"),      "imports": ("metal", "stone", "spirits")},
    "silk_road":      {"exports": ("textiles", "spices"),"imports": ("food", "wood", "metal")},
    "south_asian":    {"exports": ("spices", "tea"),     "imports": ("metal", "wood", "wine")},
}

# Pairwise agenda compatibility — yields a default relation. Lookups are
# symmetric (we try (a,b) then (b,a)). Any pair not listed defaults to neutral.
AGENDA_RELATIONS_RULES: dict[tuple[str, str], str] = {
    ("martial",    "martial"):    "rival",
    ("martial",    "mercantile"): "rival",
    ("martial",    "pious"):      "rival",
    ("martial",    "builder"):    "allied",
    ("mercantile", "mercantile"): "allied",
    ("mercantile", "builder"):    "allied",
    ("mercantile", "hedonist"):   "allied",
    ("mercantile", "scholarly"):  "allied",
    ("scholarly",  "scholarly"):  "allied",
    ("scholarly",  "pious"):      "allied",
    ("pious",      "pious"):      "allied",
    ("pious",      "hedonist"):   "rival",
    ("builder",    "builder"):    "allied",
    ("hedonist",   "hedonist"):   "allied",
    ("hedonist",   "martial"):    "rival",
}


def _agenda_relation(a: str, b: str) -> str:
    return (AGENDA_RELATIONS_RULES.get((a, b))
            or AGENDA_RELATIONS_RULES.get((b, a))
            or "neutral")


def pick_agenda(rng: random.Random) -> str:
    return rng.choice(list(LEADER_AGENDAS.keys()))


def agenda_label(agenda: str) -> str:
    return LEADER_AGENDAS.get(agenda, {}).get("label", "")


def agenda_description(agenda: str) -> str:
    return LEADER_AGENDAS.get(agenda, {}).get("description", "")


def agenda_tags(agenda: str) -> tuple:
    return LEADER_AGENDAS.get(agenda, {}).get("tags", ())


def region_buff(region) -> Optional[str]:
    if region is None:
        return None
    return LEADER_AGENDAS.get(region.agenda, {}).get("buff")


def region_specialty(region) -> dict:
    if region is None:
        return {"exports": (), "imports": ()}
    return BIOME_GROUP_SPECIALTIES.get(region.biome_group,
                                       BIOME_GROUP_SPECIALTIES["highland"])


def relation_between(rid_a: int, rid_b: int) -> str:
    region = REGIONS.get(rid_a)
    if region is None:
        return "neutral"
    return region.relations.get(rid_b, "neutral")


def allied_region_ids(region_id: int) -> list:
    region = REGIONS.get(region_id)
    if region is None:
        return []
    return [rid for rid, rel in region.relations.items() if rel == "allied"]


def rival_region_ids(region_id: int) -> list:
    region = REGIONS.get(region_id)
    if region is None:
        return []
    return [rid for rid, rel in region.relations.items() if rel == "rival"]


def compute_relations(seed: int = 0) -> None:
    """Fill REGIONS[*].relations using agenda compat + a small deterministic flip.

    Idempotent: clears existing relations first.
    """
    rids = sorted(REGIONS.keys())
    for rid in rids:
        REGIONS[rid].relations.clear()

    for i, ra_id in enumerate(rids):
        ra = REGIONS[ra_id]
        if not ra.agenda:
            continue
        for rb_id in rids[i + 1:]:
            rb = REGIONS[rb_id]
            if not rb.agenda:
                continue

            base = _agenda_relation(ra.agenda, rb.agenda)
            rng  = random.Random(seed ^ (ra_id * 7919) ^ (rb_id * 31337))
            roll = rng.random()
            rel  = base
            # A small flip chance keeps the map varied even when many regions share an agenda
            if base == "neutral":
                if   roll < 0.20: rel = "allied"
                elif roll < 0.30: rel = "rival"
            elif base == "allied" and roll < 0.10:
                rel = "neutral"
            elif base == "rival"  and roll < 0.10:
                rel = "neutral"

            if rel != "neutral":
                ra.relations[rb_id] = rel
                rb.relations[ra_id] = rel


_TOWN_NAMES_BY_GROUP: dict[str, tuple[list[str], list[str]]] = {
    # (prefixes, suffixes)
    "forest":   (["Ash","Birch","Oak","Elm","Larch","Elder","Fern","Moss","Pine","Willow",
                  "Bor","Dub","Zelen","Skog","Mori","Rowa","Cedro","Bjorn","Lind","Buka",
                  "Hvit","Sekin","Kasum","Nyir","Brin"],
                 ["brook","bury","dale","field","ford","haven","hurst","moor","stead","wick",
                  "ova","vik","mori","dal","grad","holm","les","berg"]),
    "jungle":   (["Vine","Deep","Root","Green","Fern","Jade","Moss","Thorn","Wild","Bough",
                  "Rimba","Kayu","Selva","Kongo","Kapok","Mboka","Itauba","Selu","Quech","Limon"],
                 ["grove","hollow","mere","fall","den","reach","wood","canopy","shade","run",
                  "kar","boka","ira","pur","veil","co","loma"]),
    "wetland":  (["Reed","Fog","Mud","Marsh","Mist","Fen","Bog","Moss","Grey","Ash",
                  "Delta","Papyr","Sudd","Nilew","Mekong","Ganga","Orin","Chad","Pant","Irra"],
                 ["fen","mere","marsh","hollow","mire","water","pool","haven","banks","drift",
                  "ghat","pan","khal","wadi","khor"]),
    "desert":   (["Dust","Sand","Ember","Copper","Gold","Iron","Salt","Bone","Sun","Dry",
                  "Wadi","Nefud","Gobi","Thar","Sahel","Nubia","Qara","Erg","Nafud","Karum"],
                 ["rock","post","well","pass","ridge","shard","dune","hold","gate","crossing",
                  "qum","abad","oaz","kum","sar"]),
    "alpine":   (["Snow","Frost","Stone","Peak","Ice","Cold","High","Grey","Fell","Crag",
                  "Dhaul","Intic","Pacha","Simien","Altai","Maka","Kazbek","Potal","Huasc","Tirich"],
                 ["hold","gate","wall","spire","pass","keep","ford","stead","cliff","crest",
                  "ri","la","dhar","apu","amba"]),
    "steppe":   (["Wind","Dust","Dry","Flat","Grey","Bare","Far","Wide","Gale","Drift",
                  "Khang","Tuul","Tengri","Orkhon","Qyzyl","Ulan","Dobro","Sarma","Dzung","Pech"],
                 ["ford","plain","field","crossing","reach","stand","drift","run","post","gap",
                  "gol","qum","bek","abad","grad"]),
    "coastal":  (["Salt","Tide","Wave","Shell","Drift","Crest","Foam","Gull","Cove","Sand",
                  "Moana","Atoll","Kilwa","Malindi","Carib","Tonga","Zanzi","Honu","Lagu","Marq"],
                 ["port","bay","cove","haven","shore","cliff","water","gate","drift","bank",
                  "toa","nui","reef","lagoon","atoll"]),
    "highland":      (["Peak","Crag","Moor","Ridge","Fell","Stone","Dark","High","Bleak","Cairn",
                       "Simien","Amhara","Puna","Colca","Ozark","Draken","Bale","Baloch","Zagros","Lesotho"],
                      ["top","rise","dale","shire","fell","moor","crag","side","head","ford",
                       "amba","pur","ridge","wold","spur"]),
    "mediterranean": (["Val","Serra","Monte","Villa","Porto","Costa","Agri","Ponte","Bella","Alto",
                       "Ksar","Ribat","Medina","Alcaz","Byblo","Palmyr","Caesa","Leptis","Cyrene","Tinge"],
                      ["nova","alta","bella","doro","mira","faro","vento","sole","mare","petra",
                       "zar","bey","abad","sar","qala"]),
    "east_asian":    (["Long","Jade","Dragon","Crane","Lotus","Bamboo","Golden","Moon","River","Cloud",
                       "Huang","Qing","Hong","Zi","Jin","Bai","Sakura","Fuji","Tsuki","Kiri","Haru",
                       "Hanra","Goryo","Champa","Sukho","Annam","Bagan","Dongas","Baekdu"],
                      ["zhou","jing","shan","hai","ming","dao","feng","yuan","shima","hama",
                       "men","guan","hu","jo","machi","zaki","mura","bao","gang","pu",
                       "seong","chon","dong","ho","ri"]),
    "arabia":        (["Wadi","Najd","Dhofar","Hejaz","Oman","Qatar","Hadr","Nabt","Rub","Khalij",
                       "Saba","Qahtan","Mayan","Hadhr","Incense","Palm","Falcon","Pearl","Dune","Well"],
                      ["abad","oasis","gate","ford","pass","shore","dune","spring","reach","hold",
                       "qala","sar","pur","wadi","bay"]),
    "levant":        (["Cedar","Olive","Purple","Tyrian","Sidon","Byblos","Jordan","Liban","Alep","Hama",
                       "Ugarit","Canaan","Ashker","Arvad","Byblian","Tyre","Phoenix","Salt","Glass","Script"],
                      ["gate","shore","mark","port","coast","way","ford","hold","veil","reach",
                       "abad","qala","souk","haven","bay"]),
    "persia":        (["Shir","Isfahan","Zagros","Fars","Khor","Mede","Elam","Sogd","Sasan","Parth",
                       "Achae","Ctesi","Bact","Hyrcan","Trans","Rose","Saffron","Azure","Garden","Fire"],
                      ["abad","stan","pur","gate","veil","mark","hold","mede","reach","shah",
                       "abad","qala","dez","sar","rud"]),
    "yunnan":        (["Stone","Jade","Cloud","Copper","Tea","Peacock","Cang","Erhai","Jinsha","Lugu",
                       "Yulong","Nujiang","Dali","Lijiang","Teng","Xian","Pu","Luo","Yong","Mengzi"],
                      ["gorge","peak","pool","vale","shore","shan","hai","he","yuan","pu",
                       "guan","zhai","dong","ba","jiang"]),
    "silk_road":     (["Dun","Kashgar","Khotan","Turpan","Lou","Yumen","Sha","Gansu","Luntai","Qiemo",
                       "Ruoqiang","Shan","Guan","An","Beacon","Jade","Camel","Oasis","Mural","Grotto"],
                      ["guan","hou","pass","cheng","abad","kum","qian","oasis","crossing","gate",
                       "fu","zhen","dun","kai","sar"]),
    "south_asian":   (["Deva","Naga","Surya","Chandra","Indra","Ganga","Arya","Raja","Kali","Veda",
                       "Vijaya","Chola","Pandya","Sahya","Magadh","Anura","Kanche","Dravid","Chaluk","Pallav"],
                      ["pura","ghat","nagar","tala","vati","shri","pur","mala","abad","devi",
                       "vatam","patti","uru","turai","mandal"]),
}

# Biome-specific need multipliers: (food, wood, stone, metal)
# Values > 1.0 mean higher demand; values < 1.0 mean lower demand
_NEED_WEIGHTS: dict[str, dict[str, float]] = {
    "forest":   {"food": 1.0, "wood": 0.6, "stone": 1.0, "metal": 1.2},
    "jungle":   {"food": 0.7, "wood": 0.7, "stone": 1.2, "metal": 1.0},
    "wetland":  {"food": 0.8, "wood": 1.0, "stone": 1.3, "metal": 1.0},
    "desert":   {"food": 1.5, "wood": 1.4, "stone": 0.7, "metal": 0.8},
    "alpine":   {"food": 1.2, "wood": 1.5, "stone": 0.7, "metal": 0.8},
    "steppe":   {"food": 0.9, "wood": 1.3, "stone": 1.1, "metal": 1.0},
    "coastal":  {"food": 0.8, "wood": 0.9, "stone": 1.2, "metal": 1.1},
    "highland":      {"food": 1.1, "wood": 1.1, "stone": 0.8, "metal": 0.9},
    "mediterranean": {"food": 0.9, "wood": 1.1, "stone": 0.7, "metal": 1.1},
    "east_asian":    {"food": 0.8, "wood": 0.9, "stone": 1.1, "metal": 1.2},
    "arabia":        {"food": 1.5, "wood": 1.6, "stone": 0.7, "metal": 0.9},
    "levant":        {"food": 0.9, "wood": 0.8, "stone": 0.9, "metal": 1.1},
    "persia":        {"food": 1.0, "wood": 1.1, "stone": 0.8, "metal": 1.0},
    "yunnan":        {"food": 1.1, "wood": 1.0, "stone": 0.9, "metal": 0.8},
    "silk_road":     {"food": 1.4, "wood": 1.5, "stone": 0.8, "metal": 0.9},
    "south_asian":   {"food": 0.7, "wood": 1.0, "stone": 0.8, "metal": 1.3},
}

# Luxury goods each biome group craves.
# Primary luxury is wanted by all tiers; secondary is unlocked at tier >= 1.
_LUXURY_SPECIALTY: dict[str, list[str]] = {
    "forest":   ["wine",    "herbs"],
    "jungle":   ["coffee",  "pottery"],
    "wetland":  ["tea",     "herbs"],
    "desert":   ["coffee",  "spirits"],
    "alpine":   ["spirits", "tea"],
    "steppe":   ["spirits", "herbs"],
    "coastal":  ["wine",    "tea"],
    "highland":      ["wine",    "pottery"],
    "mediterranean": ["wine",    "pottery"],
    "east_asian":    ["tea",     "pottery"],
    "arabia":        ["coffee",  "herbs"],
    "levant":        ["wine",    "pottery"],
    "persia":        ["wine",    "spirits"],
    "yunnan":        ["tea",     "herbs"],
    "silk_road":     ["wine",    "pottery"],
    "south_asian":   ["tea",     "herbs"],
}

_LEADER_GREETINGS: dict[str, list[str]] = {
    "forest":   ["The woods have many paths. Few lead here.",
                 "This kingdom grew from the trees. We honour that still.",
                 "Speak plainly. The forest rewards those who do.",
                 "The old trees remember every name spoken beneath them. Speak yours.",
                 "We trade in timber and silence. Which do you require?",
                 "Hunters, healers, and wanderers come here. Which are you?"],
    "jungle":   ["The canopy watches all who enter. State your purpose.",
                 "Few outsiders find their way this deep. You must have need.",
                 "The jungle gives and takes in equal measure. Remember that.",
                 "The river brought you here. The river will judge whether you leave.",
                 "We have no walls. The trees are our walls. Show them respect.",
                 "You carry the smell of open roads. Here we deal in roots and patience."],
    "wetland":  ["The marsh speaks to those who listen. What do you seek?",
                 "These fens have kept us hidden and kept us safe. Until now.",
                 "Outsiders rarely visit without a reason. What is yours?",
                 "The water knows every crossing. We know every stranger. Speak.",
                 "Fog hides much, but not intentions. What brings you into the mire?",
                 "We built this town on reeds and persistence. Your business?"],
    "desert":   ["The sands are unforgiving, stranger. Trade sustains us.",
                 "Water and shade are worth more here than gold. Almost.",
                 "You have crossed far to reach us. The desert respects that.",
                 "The stars guided you here. The stars do not lie. What do you carry?",
                 "We have survived where armies turned back. State your trade.",
                 "Every caravan that reaches us is a miracle. We honour them accordingly."],
    "alpine":   ["The mountain passes bring few visitors. State your purpose.",
                 "We do not waste words up here. The cold teaches that.",
                 "You've climbed high. The view is your reward. Now speak.",
                 "The summit does not care for flattery. Nor do we.",
                 "Thin air, thick walls, short patience. Make it quick.",
                 "Few roads lead here. That is by design. Why did you find one?"],
    "steppe":   ["You've ridden far. The plains teach patience.",
                 "Out here, trust is earned slowly. Talk is cheap.",
                 "The wind carries voices for miles on the steppe. Be careful.",
                 "A rider without purpose is just dust in the wind. What is yours?",
                 "We measure distance in days and honesty. How far have you come?",
                 "The horizon stretches in all directions. You chose to stop here. Why?"],
    "coastal":  ["Ha! A landlubber. Welcome to our harbour.",
                 "Every ship brings news. What do yours carry?",
                 "The tides wait for no one. Neither do we.",
                 "Salt, wind, and coin — that is this town's blood. What brings you?",
                 "We've seen stranger arrivals than you. Not many, but some.",
                 "The sea is generous and cruel. We understand both. Come in."],
    "highland":      ["You've climbed high to reach us. What do you want?",
                      "The moors have few secrets from those who live on them.",
                      "Blunt talk, sharp steel — that's the highland way.",
                      "The cloud sits low here most days. It keeps fools away. Most of them.",
                      "We have fed armies and outlasted kingdoms. Your business?",
                      "Stone endures. So do we. What do you need?"],
    "mediterranean": ["The sun shines on traders and philosophers alike. Which are you?",
                      "This city has stood a thousand years. A few more questions won't hurt it.",
                      "We debate everything here. But trade? That we decide quickly.",
                      "Our wine is older than your road. Sit and let us talk properly.",
                      "Every civilization has passed through here. We remember them all.",
                      "We do not rush. The sea has been patient with us. We extend that to guests."],
    "east_asian":    ["You arrive as the cherry blossoms fall. Auspicious, perhaps.",
                      "Patience and precision — we value both. Show us you have them.",
                      "The river carries many things downstream. What does it carry today?",
                      "The dragon sleeps in the mountain. Do not wake it without purpose.",
                      "The brush moves, the record stands. We are watching.",
                      "Honour flows downward from the throne. Remember that.",
                      "You are written into our records now. Choose your next words wisely.",
                      "The scholar and the merchant are equally welcome. Which are you?",
                      "Our gates have opened for ten thousand visitors. State your trade."],
    "arabia":        ["The desert tests all who cross it. You have passed. For now.",
                      "Coffee is offered before questions are asked. Sit.",
                      "We know every star by name. We know every stranger too.",
                      "The caravan road brought you here. The caravan road can take you back.",
                      "Hospitality is law in the desert. Do not mistake it for weakness.",
                      "My tribe has held this oasis for forty generations. Your business?"],
    "levant":        ["We built the first alphabet. Every word you say, you owe to us.",
                      "The purple dye of this coast is worth its weight in silver. Remember that.",
                      "Three roads meet here — sea, silk, and spice. We tax them all.",
                      "Our cedar ships have sailed every sea. What news do you bring from elsewhere?",
                      "The market does not close. The haggling never stops. Join us.",
                      "We have traded with every empire that rose and fell around us. Still trading."],
    "persia":        ["The garden is an image of paradise. You are welcome to walk in it.",
                      "A thousand years of empire built these roads. Use them respectfully.",
                      "The poet said: yesterday is gone, tomorrow uncertain — trade well today.",
                      "My satrap collects taxes, not insults. State your business clearly.",
                      "We invented the postal system. We know who you are already.",
                      "Fire remembers all things offered to it. What will you offer?"],
    "yunnan":        ["The gorges run deep here. So do loyalties. State your purpose.",
                      "Many roads meet in Yunnan — silk, salt, tea, and iron. Which brought you?",
                      "The Tea Horse Road has carried traders for centuries. Are you one?",
                      "Five peoples, five tongues, one plateau. You are a stranger to all of them.",
                      "The stone forest remembers every traveller who has passed. Remember that.",
                      "We answer to our own Tusi, not to distant thrones. Choose your words carefully."],
    "silk_road":     ["The beacons have not burned since the last war. Let us keep it that way.",
                      "Caravans come from east and west alike. We ask only that they trade fairly.",
                      "The jade gate stands because we guard it. What passes through, we decide.",
                      "Pilgrims, merchants, and soldiers all find rest here. Which are you?",
                      "The painted caves outside this city hold a thousand years of prayer. We hold the rest.",
                      "Dunhuang remembers every empire that used this road. We outlasted them all."],
    "south_asian":   ["The gods watch all who pass through these gates. State your purpose.",
                      "Every road leads here eventually. The spice route does not lie.",
                      "Honour the traditions of this place and you will be welcome.",
                      "We have welcomed pilgrims, merchants, and conquerors alike. Which are you?",
                      "The river feeds us and the monsoon tests us. We are patient people.",
                      "Our festivals are open to all. Our storehouses are not. State your trade."],
}

_HERALDIC_COLORS = [
    (180,  40,  40), (40,  80, 180), (50, 140,  50),
    (160, 140,  30), (130,  50, 160), (30, 130, 140),
    (180,  90,  30), (60,  60,  60),
]

_LEADER_FIRST = [
    # Northern European / fantasy baseline
    "Aldric", "Beatrix", "Calder", "Dorith", "Elowen", "Fenn",
    "Garet", "Hilda", "Islin", "Jorin", "Kessa", "Lorn",
    "Maren", "Nils", "Orla", "Pell", "Quen", "Reva",
    "Savan", "Tova", "Ulrik", "Vanna", "Wren",
    # Nordic / Scandinavian
    "Sigrid", "Bjorn", "Astrid", "Leif", "Freya", "Gunnar", "Ingrid",
    # Slavic / Eastern European
    "Mila", "Dmitri", "Katya", "Aleksei", "Zosia", "Vanya", "Bozena",
    # Arabic / Persian
    "Yasmin", "Tariq", "Leila", "Khalid", "Cyrus", "Roxana", "Omar",
    "Fatima", "Darius", "Zahra", "Shahin", "Nassim", "Soraya",
    # African (pan-regional)
    "Amara", "Kofi", "Zuri", "Adaeze", "Emeka", "Kwame", "Bakari",
    "Nia", "Chioma", "Seun", "Abebe", "Makena", "Oumar", "Ife",
    # East Asian
    "Lin", "Wei", "Hana", "Kenji", "Mei", "Jin", "Yuki", "Hiroshi",
    "Soo", "Baatar", "Temur", "Linh", "Thien", "Nari", "Joon",
    # South / Southeast Asian
    "Priya", "Arjun", "Anika", "Vikram", "Devi", "Meera", "Rajan",
    "Suthida", "Wayan", "Ayu", "Farid", "Siti", "Malai",
    # Latin / Iberian / Indigenous Americas
    "Isabella", "Diego", "Ximena", "Luisa", "Rodrigo", "Ines",
    "Kaya", "Tala", "Naira", "Tupac", "Ahanu", "Aponi",
    # Ottoman / Turkic / Central Asian
    "Aylin", "Murat", "Selene", "Turgen", "Aisha", "Bolat",
    # Greek / Hellenistic
    "Lyra", "Theron", "Clio", "Demetrios", "Kallistrate",
]
_LEADER_LAST = [
    # English-fantasy baseline
    "Ashveil", "Bram", "Coldwater", "Dusk", "Embershard",
    "Frost", "Gale", "Hollow", "Ironmoor", "Jarn",
    "Knell", "Loch", "Marsh", "Nettlefield", "Orn",
    "Pike", "Quill", "Reed", "Stonehaven", "Thorn",
    # Globally inspired fantasy surnames
    "Moonvale", "Ironbark", "Dawnfield", "Brightwater", "Starfall",
    "Nightshore", "Silverbrook", "Sunaveil", "Dragomir", "Vasquemoor",
    "Okamark", "Kimhaven", "Rashidholm", "Sundaraveil", "Osei",
    "Nakamere", "Silvamoor", "Bataarholm", "Tengrimark", "Chiomaveld",
    "Abebereach", "Kalindra", "Tuulholm", "Zanzimark", "Moanagate",
]


def _make_town_name(rng: random.Random, biome_group: str = _DEFAULT_BIOME_GROUP) -> str:
    if biome_group in _TOWN_NAMES_BY_GROUP:
        prefixes, suffixes = _TOWN_NAMES_BY_GROUP[biome_group]
    else:
        prefixes, suffixes = _PREFIXES, _SUFFIXES
    return rng.choice(prefixes) + rng.choice(suffixes)


def _biome_group_for(biodome: str) -> str:
    return _BIOME_GROUP.get(biodome, _DEFAULT_BIOME_GROUP)


def _make_region_name(rng: random.Random, used: set,
                      biome_group: str = _DEFAULT_BIOME_GROUP) -> str:
    source = _REGION_NAMES_BY_GROUP.get(biome_group,
                                        _REGION_NAMES_BY_GROUP[_DEFAULT_BIOME_GROUP])
    pool = [n for n in source if n not in used]
    if not pool:
        pool = source
    return rng.choice(pool)


def _make_tagline(rng: random.Random, biome_group: str) -> str:
    pool = _TAGLINES_BY_GROUP.get(biome_group, _TAGLINES_BY_GROUP[_DEFAULT_BIOME_GROUP])
    return rng.choice(pool)


def _make_leader_name(rng: random.Random) -> str:
    return f"{rng.choice(_LEADER_FIRST)} {rng.choice(_LEADER_LAST)}"


def leader_title_for(biome_group: str, rng: random.Random) -> str:
    """Return a biome-appropriate title (masc/fem chosen from rng)."""
    masc, fem = _LEADER_TITLES.get(biome_group, ("Lord", "Lady"))
    return rng.choice([masc, fem])


def leader_greeting_for(biome_group: str) -> str:
    """Return a random greeting line for a leader in this biome group."""
    import random as _random
    pool = _LEADER_GREETINGS.get(biome_group, _LEADER_GREETINGS["highland"])
    return _random.choice(pool)

# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class Town:
    town_id:          int
    region_id:        int
    is_capital:       bool
    center_bx:        int
    half_w:           int
    biome:            str
    name:             str
    leader_name:      Optional[str]
    tier:             int
    reputation:       int
    needs:            dict   # {"food": {"required": 200, "supplied": 50}, ...}
    growth_progress:  float  # 0..1; resets on tier up
    grown_buildings:  list   # [(offset, variant, width, height), ...]
    founded_day:      int
    size:             str    # "small"/"medium"/"large"

    def tier_name(self) -> str:
        return TIER_NAMES[min(self.tier, len(TIER_NAMES) - 1)]

    def all_needs_met(self) -> bool:
        return all(
            nd["supplied"] >= nd["required"]
            for nd in self.needs.values()
        )


@dataclass
class Region:
    region_id:       int
    name:            str
    capital_town_id: int
    member_town_ids: list
    leader_color:    tuple
    coat_of_arms:    Optional[heraldry.CoatOfArms] = None
    biome_group:     str = _DEFAULT_BIOME_GROUP
    tagline:         str = ""
    leader_title:    str = "Lord"
    agenda:          str = ""                                # leader personality (LEADER_AGENDAS key)
    relations:       dict = field(default_factory=dict)      # other_region_id → "allied" | "rival"
    # reputation is computed on read: sum of member town reps


# ---------------------------------------------------------------------------
# Registries
# ---------------------------------------------------------------------------

TOWNS:   dict[int, Town]   = {}
REGIONS: dict[int, Region] = {}

# ---------------------------------------------------------------------------
# Init
# ---------------------------------------------------------------------------

def _scan_bg_for_flags(world) -> list:
    """Scan in-memory bg chunks for TOWN_FLAG_BLOCK; return sorted list of bx values."""
    from blocks import TOWN_FLAG_BLOCK as _TFB
    from constants import CHUNK_W as _CW
    bxs = []
    for cx, chunk in world._bg_chunks.items():
        for by in range(len(chunk)):
            for lx in range(len(chunk[by])):
                if chunk[by][lx] == _TFB:
                    bxs.append(cx * _CW + lx)
    return sorted(bxs)


def init_towns(world) -> None:
    """Populate TOWNS and REGIONS from world.town_centers (set by generate_cities)."""
    TOWNS.clear()
    REGIONS.clear()

    # Try to load persisted data first
    if hasattr(world, '_save_mgr') and world._save_mgr is not None:
        rows = _load_from_db(world._save_mgr)
        if rows is not None:
            _fill_missing_coat_of_arms(world.seed)
            _restore_world_city_metadata(world)
            _respawn_leader_npcs(world)
            return

    centers = world.town_centers
    if not centers:
        # Old save: bg chunks are already loaded by _load_from; scan them for flags.
        centers = _scan_bg_for_flags(world)
        if not centers:
            return

    rng = random.Random(world.seed + 99999)
    used_names: set[str] = set()
    used_regions: set[str] = set()

    from cities import CITY_CONFIGS, _city_slot_metadata, CITY_SPACING
    city_sizes = getattr(world, 'city_sizes', [])
    slot_xs    = getattr(world, 'city_slot_xs', [])

    for town_id, center_bx in enumerate(centers):
        # Resolve slot_x: use stored value, or approximate from center_bx
        if town_id < len(slot_xs):
            slot_x = slot_xs[town_id]
        else:
            half   = CITY_SPACING // 2
            slot_x = round((center_bx - half) / CITY_SPACING) * CITY_SPACING + half

        meta   = _city_slot_metadata(slot_x)
        biome  = world.biodome_at(center_bx)
        name   = _make_town_name(rng, _biome_group_for(biome))
        used_names.add(name)

        size   = city_sizes[town_id] if town_id < len(city_sizes) else "medium"
        half_w = CITY_CONFIGS[size]["half_w"]

        TOWNS[town_id] = Town(
            town_id       = town_id,
            region_id     = meta["region_id"],
            is_capital    = meta["is_capital"],
            center_bx     = center_bx,
            half_w        = half_w,
            biome         = biome,
            name          = name,
            leader_name   = None,
            tier          = _starting_tier(size, meta["is_capital"]),
            reputation    = 0,
            needs         = {},
            growth_progress = 0.0,
            grown_buildings = [],
            founded_day   = 0,
            size          = size,
        )
        _assign_initial_needs(TOWNS[town_id])

    # Build regions — one deterministic RNG per region keyed by region_id
    region_ids = set(t.region_id for t in TOWNS.values())
    for rid in sorted(region_ids):
        members  = [t for t in TOWNS.values() if t.region_id == rid]
        capitals = [t for t in members if t.is_capital]
        capital  = capitals[0] if capitals else members[0]

        bg     = _biome_group_for(world.biodome_at(capital.center_bx))

        rng_r   = random.Random(world.seed + rid * 31337 + 88888)
        rname   = _make_region_name(rng_r, used_regions, bg)
        used_regions.add(rname)
        lcolor  = rng_r.choice(_HERALDIC_COLORS)
        lname   = _make_leader_name(rng_r)
        tagline = _make_tagline(rng_r, bg)
        title   = leader_title_for(bg, rng_r)
        capital.leader_name = lname

        coa = heraldry.generate(random.Random(), lcolor,
                                charge_pool=_CHARGES_BY_GROUP.get(bg))

        REGIONS[rid] = Region(
            region_id       = rid,
            name            = rname,
            capital_town_id = capital.town_id,
            member_town_ids = [t.town_id for t in members],
            leader_color    = lcolor,
            coat_of_arms    = coa,
            biome_group     = bg,
            tagline         = tagline,
            leader_title    = title,
            agenda          = pick_agenda(rng_r),
        )

    # Compute inter-region relations once all agendas are set
    compute_relations(world.seed)

    # Place castles + LeaderNPCs for each capital
    for town in TOWNS.values():
        if town.is_capital:
            _place_capital_structures(town, world)


def register_new_town(world, city_bx: int, city_size: str,
                      region_id: int = 0, is_capital: bool = False) -> None:
    """Register a dynamically-generated (chunk-streamed) city as a full Town."""
    from cities import CITY_CONFIGS
    town_id = max(TOWNS.keys()) + 1 if TOWNS else 0
    half_w  = CITY_CONFIGS[city_size]["half_w"]
    biome   = world.biodome_at(city_bx)
    rng     = random.Random(world.seed + city_bx * 7919)
    name    = _make_town_name(rng, _biome_group_for(biome))

    TOWNS[town_id] = Town(
        town_id         = town_id,
        region_id       = region_id,
        is_capital      = is_capital,
        center_bx       = city_bx,
        half_w          = half_w,
        biome           = biome,
        name            = name,
        leader_name     = None,
        tier            = _starting_tier(city_size, is_capital),
        reputation      = 0,
        needs           = {},
        growth_progress = 0.0,
        grown_buildings = [],
        founded_day     = 0,
        size            = city_size,
    )
    _assign_initial_needs(TOWNS[town_id])

    # Lazily create the Region if it doesn't exist yet
    if region_id not in REGIONS:
        bg      = _biome_group_for(world.biodome_at(city_bx))
        rng_r   = random.Random(world.seed + region_id * 31337 + 88888)
        used    = {r.name for r in REGIONS.values()}
        rname   = _make_region_name(rng_r, used, bg)
        lcolor  = rng_r.choice(_HERALDIC_COLORS)
        lname   = _make_leader_name(rng_r)
        tagline = _make_tagline(rng_r, bg)
        title   = leader_title_for(bg, rng_r)
        coa     = heraldry.generate(random.Random(), lcolor,
                                    charge_pool=_CHARGES_BY_GROUP.get(bg))
        REGIONS[region_id] = Region(
            region_id       = region_id,
            name            = rname,
            capital_town_id = town_id if is_capital else -1,
            member_town_ids = [],
            leader_color    = lcolor,
            coat_of_arms    = coa,
            biome_group     = bg,
            tagline         = tagline,
            leader_title    = title,
            agenda          = pick_agenda(rng_r),
        )
        if is_capital:
            TOWNS[town_id].leader_name = lname
        compute_relations(world.seed)
    else:
        if is_capital:
            # Claim the capital slot if no capital has arrived yet
            region = REGIONS[region_id]
            if region.capital_town_id == -1:
                rng_r = random.Random(world.seed + region_id * 31337 + 88888)
                _make_region_name(rng_r, set())   # advance rng past name
                rng_r.choice(_HERALDIC_COLORS)    # advance past color
                lname = _make_leader_name(rng_r)
                TOWNS[town_id].leader_name = lname
                region.capital_town_id = town_id
                # Update biome_group to the capital's biome — the region may have been
                # created by a non-capital city that arrived first with a different biome.
                region.biome_group = _biome_group_for(biome)

    REGIONS[region_id].member_town_ids.append(town_id)

    if is_capital:
        _place_capital_structures(TOWNS[town_id], world)


def _restore_world_city_metadata(world) -> None:
    """Populate world.town_centers/city_zones/etc. from loaded TOWNS after a DB load."""
    from cities import CITY_CONFIGS, CITY_SPACING
    half_spacing = CITY_SPACING // 2
    world.town_centers = []
    world.city_sizes   = []
    world.city_slot_xs = []
    world.city_zones   = []
    for town in sorted(TOWNS.values(), key=lambda t: t.town_id):
        bx     = town.center_bx
        size   = town.size
        half_w = CITY_CONFIGS.get(size, CITY_CONFIGS["medium"])["half_w"]
        slot_x = round((bx - half_spacing) / CITY_SPACING) * CITY_SPACING + half_spacing
        world.town_centers.append(bx)
        world.city_sizes.append(size)
        world.city_slot_xs.append(slot_x)
        world.city_zones.append((bx - half_w, bx + half_w))


def _palace_type_for(palace_left: int, world_seed: int) -> str:
    """Deterministic palace type for a capital at palace_left.  Same inputs → same type."""
    from cities import PALACE_TYPES
    return random.Random(palace_left ^ world_seed ^ 0xCAFEBABE).choice(PALACE_TYPES)


def _respawn_leader_npcs(world) -> None:
    """Re-create LeaderNPC entities for capital towns after loading from DB.
    Blocks are already in loaded chunks; only the entity needs to be spawned."""
    from cities import PALACE_NPC_OFFSET, LeaderNPC
    from constants import BLOCK_SIZE

    for town in TOWNS.values():
        if not town.is_capital:
            continue
        region = REGIONS.get(town.region_id)
        if region is None:
            continue
        palace_left = town.center_bx + town.half_w + 4
        sy = world.surface_y_at(palace_left)
        ptype = _palace_type_for(palace_left, world.seed)
        npc_offset = PALACE_NPC_OFFSET[ptype]
        npc_px = (palace_left + npc_offset) * BLOCK_SIZE
        npc_py = (sy - 3) * BLOCK_SIZE
        world.entities.append(
            LeaderNPC(npc_px, npc_py, world,
                      region_id   = region.region_id,
                      region_name = region.name,
                      leader_name = town.leader_name or "Leader",
                      leader_color= region.leader_color,
                      palace_type = ptype)
        )


def _place_capital_structures(town: Town, world) -> None:
    """Place a randomly-selected palace + LeaderNPC for a capital town."""
    from cities import (
        _place_castle, _populate_castle, _place_castle_garden,
        _place_mediterranean_palace,
        _place_east_asian_palace,
        _place_south_asian_palace,
        _place_italian_palazzo,
        _place_moorish_palace,
        _place_middle_eastern_palace,
        _place_norse_hall,
        _place_gothic_palace,
        _place_african_palace,
        _place_byzantine_palace,
        _place_tibetan_palace,
        _place_japanese_palace,
        _place_chinese_palace,
        _place_tang_palace,
        _place_song_palace,
        _place_han_palace,
        _place_east_african_palace,
        _place_mesoamerican_palace,
        _place_french_baroque_palace,
        _place_incan_palace,
        _place_persian_palace,
        PALACE_NPC_OFFSET,
        LeaderNPC,
    )
    from constants import BLOCK_SIZE

    region = REGIONS.get(town.region_id)
    palace_left = town.center_bx + town.half_w + 4
    sy = world.surface_y_at(palace_left)

    ptype = _palace_type_for(palace_left, world.seed)

    if ptype == "mediterranean":
        _place_mediterranean_palace(world, palace_left, sy)
    elif ptype == "east_asian":
        _place_east_asian_palace(world, palace_left, sy)
    elif ptype == "south_asian":
        _place_south_asian_palace(world, palace_left, sy)
    elif ptype == "italian":
        _place_italian_palazzo(world, palace_left, sy)
    elif ptype == "moorish":
        _place_moorish_palace(world, palace_left, sy)
    elif ptype == "middle_eastern":
        _place_middle_eastern_palace(world, palace_left, sy)
    elif ptype == "norse":
        _place_norse_hall(world, palace_left, sy)
    elif ptype == "gothic":
        _place_gothic_palace(world, palace_left, sy)
    elif ptype == "african":
        _place_african_palace(world, palace_left, sy)
    elif ptype == "byzantine":
        _place_byzantine_palace(world, palace_left, sy)
    elif ptype == "tibetan":
        _place_tibetan_palace(world, palace_left, sy)
    elif ptype == "japanese":
        _place_japanese_palace(world, palace_left, sy)
    elif ptype == "chinese":
        _place_chinese_palace(world, palace_left, sy)
    elif ptype == "tang_imperial":
        _place_tang_palace(world, palace_left, sy)
    elif ptype == "song_palace":
        _place_song_palace(world, palace_left, sy)
    elif ptype == "han_palace":
        _place_han_palace(world, palace_left, sy)
    elif ptype == "east_african":
        _place_east_african_palace(world, palace_left, sy)
    elif ptype == "mesoamerican":
        _place_mesoamerican_palace(world, palace_left, sy)
    elif ptype == "french_baroque":
        _place_french_baroque_palace(world, palace_left, sy)
    elif ptype == "incan":
        _place_incan_palace(world, palace_left, sy)
    elif ptype == "persian":
        _place_persian_palace(world, palace_left, sy)
    else:
        castle_w = _place_castle(world, palace_left, sy)
        castle_rng = random.Random(palace_left ^ (world.seed * 0x9E3779B9) ^ 0xBEEF1)
        _populate_castle(world, palace_left, sy, castle_rng)
        _place_castle_garden(world, palace_left + castle_w + 1, sy, castle_rng, town.biome)

    npc_offset = PALACE_NPC_OFFSET[ptype]

    if region is None:
        return
    npc_px = (palace_left + npc_offset) * BLOCK_SIZE
    npc_py = (sy - 3) * BLOCK_SIZE
    world.entities.append(
        LeaderNPC(npc_px, npc_py, world,
                  region_id   = region.region_id,
                  region_name = region.name,
                  leader_name = town.leader_name or "Leader",
                  leader_color= region.leader_color,
                  palace_type = ptype)
    )


def _coa_rng(world_seed: int, region_id: int, leader_color: tuple) -> random.Random:
    """Deterministic rng used only for back-filling missing COAs on old saves."""
    seed = (world_seed ^ (region_id * 0x9E3779B9) ^ hash(leader_color)) & 0x7FFFFFFF
    return random.Random(seed)


def _fill_missing_coat_of_arms(world_seed: int) -> None:
    """Regenerate coat_of_arms for any region that was loaded without one (old saves)."""
    for region in REGIONS.values():
        if region.coat_of_arms is None:
            region.coat_of_arms = heraldry.generate(
                _coa_rng(world_seed, region.region_id, region.leader_color),
                region.leader_color,
            )


def _starting_tier(size: str, is_capital: bool) -> int:
    base = {"small": 0, "medium": 1, "large": 2, "military": 1}.get(size, 0)
    return min(base + (1 if is_capital else 0), len(TIER_NAMES) - 1)


def _assign_initial_needs(town: Town) -> None:
    tier    = town.tier
    bg      = _biome_group_for(town.biome)
    weights = _NEED_WEIGHTS.get(bg, {})
    town.needs = {
        cat: {
            "required": max(1, round(BASE_NEED_AMOUNT[cat]
                                     * weights.get(cat, 1.0)
                                     * (tier + 1))),
            "supplied": 0,
        }
        for cat in TOWN_CATEGORIES
    }
    # Luxury specialty: primary always wanted; secondary unlocked at tier >= 1
    lux_rng  = random.Random(town.town_id * 1_234_567 + 42)
    luxuries = _LUXURY_SPECIALTY.get(bg, [])
    for i, lux in enumerate(luxuries):
        if i == 0 or tier >= 1 or town.is_capital:
            pool      = LUXURY_VARIANT_POOLS.get(lux, {})
            variants  = pool.get(bg) or pool.get("_default", [])
            preferred = lux_rng.choice(variants) if variants else None
            town.needs[lux] = {
                "required":  max(1, round(BASE_NEED_AMOUNT_LUXURY[lux] * (tier + 1))),
                "supplied":  0,
                "preferred": preferred,
            }
    # Military towns need weapons supplied (bows + arrows)
    if town.size == "military":
        from town_needs import BASE_NEED_AMOUNT_MILITARY
        town.needs["weapons"] = {
            "required":  max(1, BASE_NEED_AMOUNT_MILITARY["weapons"] * (tier + 1)),
            "supplied":  0,
            "preferred": "iron_arrow",
        }

# ---------------------------------------------------------------------------
# Supply
# ---------------------------------------------------------------------------

def supply_need(town: Town, player, category: str, amount: int) -> tuple[int, int]:
    """
    Deliver `amount` units of `category` from player to town.
    Returns (gold_earned, rep_earned).
    """
    if category not in town.needs:
        return 0, 0
    nd = town.needs[category]
    space = max(0, nd["required"] - nd["supplied"])
    can_supply = min(amount, space, player.count_items_in_category(category))
    if can_supply <= 0:
        return 0, 0

    # Count preferred-type items available before removal for gold bonus
    preferred = nd.get("preferred")
    pref_count = 0
    if preferred:
        pref_count = min(can_supply, sum(
            cnt for iid, cnt in player.inventory.items()
            if iid == preferred or iid.startswith(preferred + "_")
        ))

    removed = player.remove_items_in_category(category, can_supply)
    nd["supplied"] += removed

    base_rate = GOLD_PER_UNIT[category]
    gold = (round(pref_count * base_rate * PREFERRED_BONUS_MULT)
            + (removed - pref_count) * base_rate)
    player.money += gold

    rep = 0
    if nd["supplied"] >= nd["required"]:
        rep = REP_PER_LUXURY_FILLED if category in LUXURY_CATEGORIES else REP_PER_NEED_FILLED
        town.reputation += rep

    return gold, rep

# ---------------------------------------------------------------------------
# Day tick
# ---------------------------------------------------------------------------

def advance_day(world) -> None:
    """Called once per in-game day. Updates growth progress and triggers tier-ups."""
    for town in TOWNS.values():
        if not town.needs:
            continue
        if town.all_needs_met():
            # Builder leaders accelerate growth in their region once trust is earned.
            region = REGIONS.get(town.region_id)
            growth_mult = 1.0
            if region and region.agenda == "builder" and town.reputation >= 200:
                growth_mult = 1.5
            town.growth_progress += growth_mult / DAYS_PER_TIER
            if town.growth_progress >= 1.0:
                _tier_up(town, world)

    # Reset daily supply tracking (needs carry over; only supplied resets each tier-up)
    # Daily decay: partially supplied needs decay 10% of required each day they aren't met
    for town in TOWNS.values():
        for nd in town.needs.values():
            if nd["supplied"] < nd["required"]:
                decay = max(1, nd["required"] // 10)
                nd["supplied"] = max(0, nd["supplied"] - decay)


def _tier_up(town: Town, world) -> None:
    town.tier = min(town.tier + 1, 3)
    town.growth_progress = 0.0
    _assign_initial_needs(town)
    _grow_town_buildings(town, world)
    # Broadcast toast via world attribute (main.py reads it)
    if not hasattr(world, '_town_toasts'):
        world._town_toasts = []
    world._town_toasts.append(f"{town.name} grew to {town.tier_name()}!")

    # Re-evaluate capital for the region (it's locked at init, so just update leader)
    region = REGIONS.get(town.region_id)
    if region and town.is_capital:
        pass  # already capital

# ---------------------------------------------------------------------------
# Growth building placement
# ---------------------------------------------------------------------------

def _grow_town_buildings(town: Town, world) -> None:
    """Attempt to place the next growth slot building for the town."""
    from cities import CITY_CONFIGS, _place_house, _place_house_two_story, _place_tower, BUILDING_PALETTES
    import random as _r

    cfg = CITY_CONFIGS.get(town.size, CITY_CONFIGS["medium"])
    slots_key = f"growth_slots_tier{town.tier}"
    slots = cfg.get(slots_key, [])
    if not slots:
        return

    # Find the next unused slot
    used_offsets = {b[0] for b in town.grown_buildings}
    rng = _r.Random(world.seed + town.town_id * 31337 + town.tier * 997)

    from blocks import STONE as _STONE, AIR as _AIR
    # Growth buildings sit on the same floor as the city.
    city_sy = world.surface_y_at(town.center_bx)

    for offset, w_range, h_range, variants in slots:
        if offset in used_offsets:
            continue
        left_x = town.center_bx + offset
        sy     = city_sy
        width  = rng.randint(*w_range)
        height = rng.randint(*h_range)
        variant = rng.choice(variants)

        # Safety check — don't overwrite player-placed blocks
        if _slot_is_blocked(world, left_x, sy, width, height):
            continue

        # Flatten 3 blocks outside each outer wall so players approaching from
        # outside the city don't hit solid wall above the door opening.
        for ext_x in list(range(left_x - 3, left_x)) + list(range(left_x + width, left_x + width + 3)):
            if not (0 <= ext_x < world.width):
                continue
            if 0 <= sy < world.height:
                world.set_block(ext_x, sy, _STONE)
            for wy in range(sy - 6, sy):
                if 0 <= wy < world.height and world.get_block(ext_x, wy) != _AIR:
                    world.set_block(ext_x, wy, _AIR)

        wall_block, roof_block = rng.choice(BUILDING_PALETTES)
        if variant == "two_story":
            floor2_h = rng.randint(2, 3)
            _place_house_two_story(world, left_x, sy, width, height, floor2_h,
                                   wall_block, roof_block)
        elif variant == "tower":
            _place_tower(world, left_x, sy, width, height, wall_block, roof_block)
        else:
            _place_house(world, left_x, sy, width, height, wall_block, roof_block)

        town.grown_buildings.append((offset, variant, width, height))
        return  # one building per tier-up


def _slot_is_blocked(world, left_x: int, sy: int, width: int, height: int) -> bool:
    """Return True if the slot contains player-placed non-natural blocks."""
    from blocks import AIR, STONE, GRASS, DIRT, BEDROCK
    natural = {AIR, STONE, GRASS, DIRT, BEDROCK}
    for bx in range(left_x, left_x + width + 1):
        for by in range(sy - height - 1, sy):
            bid = world.get_block(bx, by)
            if bid not in natural:
                return True
    return False

# ---------------------------------------------------------------------------
# Lookup
# ---------------------------------------------------------------------------

def get_town_for_block(world, bx: int, by: int) -> Optional[Town]:
    """Return the Town whose footprint contains (bx, by), or None."""
    for town in TOWNS.values():
        if town.center_bx - town.half_w - 2 <= bx <= town.center_bx + town.half_w + 2:
            return town
    return None

# ---------------------------------------------------------------------------
# Serialization
# ---------------------------------------------------------------------------

def serialize_all() -> tuple[list[dict], list[dict]]:
    town_rows = []
    for t in TOWNS.values():
        town_rows.append({
            "town_id":         t.town_id,
            "region_id":       t.region_id,
            "is_capital":      int(t.is_capital),
            "center_bx":       t.center_bx,
            "half_w":          t.half_w,
            "biome":           t.biome,
            "name":            t.name,
            "leader_name":     t.leader_name or "",
            "tier":            t.tier,
            "reputation":      t.reputation,
            "growth_progress": t.growth_progress,
            "founded_day":     t.founded_day,
            "size":            t.size,
            "needs_json":      json.dumps(t.needs),
            "grown_buildings_json": json.dumps(t.grown_buildings),
        })
    region_rows = []
    for r in REGIONS.values():
        coa = r.coat_of_arms
        coa_json = json.dumps({
            "primary":   list(coa.primary),
            "secondary": list(coa.secondary),
            "metal":     list(coa.metal),
            "division":  coa.division,
            "ordinary":  coa.ordinary,
            "charge":    coa.charge,
            "motto":     coa.motto,
        }) if coa else "null"
        region_rows.append({
            "region_id":            r.region_id,
            "name":                 r.name,
            "capital_town_id":      r.capital_town_id,
            "member_town_ids_json": json.dumps(r.member_town_ids),
            "leader_color_json":    json.dumps(list(r.leader_color)),
            "coat_of_arms_json":    coa_json,
            "biome_group":          r.biome_group,
            "tagline":              r.tagline,
            "leader_title":         r.leader_title,
            "agenda":               r.agenda,
            "relations_json":       json.dumps({str(k): v for k, v in r.relations.items()}),
        })
    return town_rows, region_rows


def deserialize_all(town_rows: list[dict], region_rows: list[dict]) -> None:
    TOWNS.clear()
    REGIONS.clear()
    for row in town_rows:
        t = Town(
            town_id         = row["town_id"],
            region_id       = row["region_id"],
            is_capital      = bool(row["is_capital"]),
            center_bx       = row["center_bx"],
            half_w          = row["half_w"],
            biome           = row["biome"],
            name            = row["name"],
            leader_name     = row["leader_name"] or None,
            tier            = row["tier"],
            reputation      = row["reputation"],
            needs           = json.loads(row["needs_json"]),
            growth_progress = row["growth_progress"],
            grown_buildings = json.loads(row["grown_buildings_json"]),
            founded_day     = row["founded_day"],
            size            = row.get("size", "medium"),
        )
        TOWNS[t.town_id] = t
    for row in region_rows:
        lcolor = tuple(json.loads(row["leader_color_json"]))
        coa = None
        raw_coa = row.get("coat_of_arms_json")
        if raw_coa and raw_coa != "null":
            try:
                d = json.loads(raw_coa)
                coa = heraldry.CoatOfArms(
                    primary   = tuple(d["primary"]),
                    secondary = tuple(d["secondary"]),
                    metal     = tuple(d["metal"]),
                    division  = d["division"],
                    ordinary  = d["ordinary"],
                    charge    = d["charge"],
                    motto     = d["motto"],
                )
            except Exception:
                coa = None
        relations_raw = row.get("relations_json") or "{}"
        try:
            rel_d = json.loads(relations_raw) if relations_raw else {}
            relations = {int(k): v for k, v in rel_d.items()}
        except Exception:
            relations = {}
        r = Region(
            region_id       = row["region_id"],
            name            = row["name"],
            capital_town_id = row["capital_town_id"],
            member_town_ids = json.loads(row["member_town_ids_json"]),
            leader_color    = lcolor,
            coat_of_arms    = coa,
            biome_group     = row.get("biome_group") or _DEFAULT_BIOME_GROUP,
            tagline         = row.get("tagline") or "",
            leader_title    = row.get("leader_title") or "Lord",
            agenda          = row.get("agenda") or "",
            relations       = relations,
        )
        REGIONS[r.region_id] = r

    # Backfill agendas for old saves where this column is empty.
    # Recompute relations only when we actually filled agendas — otherwise
    # we'd overwrite the saved relation graph with a different one.
    needs_backfill = False
    for r in REGIONS.values():
        if not r.agenda:
            needs_backfill = True
            r.agenda = pick_agenda(random.Random(r.region_id * 31337 + 88888))
    if needs_backfill:
        compute_relations(seed=0)


def _load_from_db(save_mgr) -> Optional[bool]:
    """Try to load town/region data from DB. Returns True if data found, None if not."""
    try:
        import sqlite3
        with sqlite3.connect(save_mgr.db_path) as con:
            con.row_factory = sqlite3.Row
            towns_exist = con.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='towns'"
            ).fetchone()
            if not towns_exist:
                return None
            town_rows   = [dict(r) for r in con.execute("SELECT * FROM towns").fetchall()]
            region_rows = [dict(r) for r in con.execute("SELECT * FROM regions").fetchall()]
            if not town_rows:
                return None
            deserialize_all(town_rows, region_rows)
            return True
    except Exception:
        return None
