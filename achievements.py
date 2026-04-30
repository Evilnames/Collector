from dataclasses import dataclass


@dataclass
class Achievement:
    id: str
    name: str
    description: str
    category: str  # 'mushroom' | 'rock' | 'wildflower'
    required_items: list  # block_ids (int) for mushroom; type strings for rock/wildflower


# Mushroom block IDs mirror blocks.py constants (imported at runtime would cause circular deps)
_CAVE_MUSHROOM = 117; _EMBER_CAP = 118;   _PALE_GHOST = 119;   _GOLD_CHANTERELLE = 120
_COBALT_CAP    = 121; _MOSSY_CAP  = 122;  _VIOLET_CROWN = 123; _BLOOD_CAP = 124
_SULFUR_DOME   = 125; _IVORY_BELL = 126;  _ASH_BELL = 127;     _TEAL_BELL = 128
_RUST_SHELF    = 129; _COPPER_SHELF = 130;_OBSIDIAN_SHELF = 131;_COAL_PUFF = 132
_STONE_PUFF    = 133; _AMBER_PUFF = 134;  _SULFUR_TUFT = 135;  _HONEY_CLUSTER = 136
_CORAL_TUFT    = 137; _BONE_STALK = 138;  _MAGMA_CAP = 139;    _DEEP_INK = 140
_BIOLUME       = 141

ACHIEVEMENTS = [
    # ------------------------------------------------------------------ mushrooms
    Achievement(
        id="dome_dwellers",
        name="Dome Dwellers",
        description="Discover 5 classic cap mushrooms",
        category="mushroom",
        required_items=[_CAVE_MUSHROOM, _EMBER_CAP, _PALE_GHOST, _GOLD_CHANTERELLE, _COBALT_CAP],
    ),
    Achievement(
        id="vivid_caps",
        name="Vivid Caps",
        description="Discover 5 vivid and rare dome fungi",
        category="mushroom",
        required_items=[_MOSSY_CAP, _VIOLET_CROWN, _BLOOD_CAP, _SULFUR_DOME, _MAGMA_CAP],
    ),
    Achievement(
        id="bell_tower",
        name="Bell Tower",
        description="Discover the bell, stalk, and ink fungi",
        category="mushroom",
        required_items=[_IVORY_BELL, _ASH_BELL, _TEAL_BELL, _BONE_STALK, _DEEP_INK],
    ),
    Achievement(
        id="shelf_and_puff",
        name="Shelf & Puff",
        description="Discover shelf fungi and puffballs",
        category="mushroom",
        required_items=[_RUST_SHELF, _COPPER_SHELF, _OBSIDIAN_SHELF, _COAL_PUFF, _STONE_PUFF],
    ),
    Achievement(
        id="cluster_blooms",
        name="Cluster Blooms",
        description="Discover clusters and bioluminescent fungi",
        category="mushroom",
        required_items=[_AMBER_PUFF, _SULFUR_TUFT, _HONEY_CLUSTER, _CORAL_TUFT, _BIOLUME],
    ),

    # ------------------------------------------------------------------ rocks
    Achievement(
        id="surface_sampler",
        name="Surface Sampler",
        description="Collect 5 types of shallow-depth rocks",
        category="rock",
        required_items=["flint", "limestone", "sandstone", "slate", "chalk"],
    ),
    Achievement(
        id="earths_heart",
        name="Earth's Heart",
        description="Collect 5 foundational rock types",
        category="rock",
        required_items=["granite", "coal_gem", "basalt", "dolomite", "quartz"],
    ),
    Achievement(
        id="gem_hunter",
        name="Gem Hunter",
        description="Collect 5 mid-depth mineral specimens",
        category="rock",
        required_items=["amethyst", "citrine", "jasper", "pyrite", "tourmaline"],
    ),
    Achievement(
        id="deep_crystals",
        name="Deep Crystals",
        description="Collect 5 deep-formed crystals and minerals",
        category="rock",
        required_items=["malachite", "jade", "labradorite", "azurite", "rhodonite"],
    ),
    Achievement(
        id="legendary_stash",
        name="Legendary Stash",
        description="Collect 5 rare and legendary rocks",
        category="rock",
        required_items=["bloodstone", "moonstone", "voidite", "void_crystal", "meteorite"],
    ),

    # ------------------------------------------------------------------ wildflowers
    Achievement(
        id="meadow_bouquet",
        name="Meadow Bouquet",
        description="Find 5 common meadow wildflowers",
        category="wildflower",
        required_items=["daisy", "buttercup", "clover", "cornflower", "sunflower"],
    ),
    Achievement(
        id="forest_floor",
        name="Forest Floor",
        description="Find 5 woodland wildflowers",
        category="wildflower",
        required_items=["fireweed", "bluebell", "wood_anemone", "trillium", "lupine"],
    ),
    Achievement(
        id="wetland_wonders",
        name="Wetland Wonders",
        description="Find 5 wetland and cool-climate flowers",
        category="wildflower",
        required_items=["iris", "marsh_marigold", "water_lily", "arctic_poppy", "redwood_violet"],
    ),
    Achievement(
        id="exotic_paradise",
        name="Exotic Paradise",
        description="Find 5 exotic tropical flowers",
        category="wildflower",
        required_items=["orchid", "heliconia", "passion_flower", "hibiscus", "plumeria"],
    ),
    Achievement(
        id="rare_blooms",
        name="Rare Blooms",
        description="Find 5 rare and unusual wildflowers",
        category="wildflower",
        required_items=["bleeding_heart", "glowcap_bloom", "mycelium_lily", "desert_rose", "sand_lily"],
    ),

    # ------------------------------------------------------------------ fossils
    Achievement(
        id="ancient_seas",
        name="Ancient Seas",
        description="Discover 5 early Paleozoic fossils",
        category="fossil",
        required_items=["trilobite", "brachiopod", "crinoid", "coral_colony", "stromatolite"],
    ),
    Achievement(
        id="paleozoic_vault",
        name="Paleozoic Vault",
        description="Discover 5 mid-Paleozoic specimens",
        category="fossil",
        required_items=["nautiloid", "graptolite", "orthoceras", "spiriferid", "blastoid"],
    ),
    Achievement(
        id="mesozoic_garden",
        name="Mesozoic Garden",
        description="Discover 5 Mesozoic plant and sea fossils",
        category="fossil",
        required_items=["ammonite", "fern_frond", "pine_cone_fossil", "sea_lily", "cycad_frond"],
    ),
    Achievement(
        id="age_of_reptiles",
        name="Age of Reptiles",
        description="Discover 5 Mesozoic reptile fossils",
        category="fossil",
        required_items=["ichthyosaur_tooth", "mosasaur_scale", "pterosaur_bone", "plesiosaur_vertebra", "sauropod_scale"],
    ),
    Achievement(
        id="ice_age_relics",
        name="Ice Age Relics",
        description="Discover 5 Cenozoic megafauna fossils",
        category="fossil",
        required_items=["sabertooth", "mammoth_molar", "whale_bone", "dire_wolf_tooth", "elephant_ancestor_tusk"],
    ),

    # ------------------------------------------------------------------ completionist
    Achievement(
        id="fungal_master",
        name="Fungal Master",
        description="Discover all 25 species of cave fungi",
        category="mushroom",
        required_items=[117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141],
    ),
    Achievement(
        id="stone_sage",
        name="Stone Sage",
        description="Collect all 25 types of rocks and minerals",
        category="rock",
        required_items=["flint","limestone","sandstone","slate","chalk","granite","coal_gem","basalt","dolomite","quartz","amethyst","citrine","jasper","pyrite","tourmaline","malachite","jade","labradorite","azurite","rhodonite","bloodstone","moonstone","voidite","void_crystal","meteorite"],
    ),
    Achievement(
        id="botanical_sage",
        name="Botanical Sage",
        description="Discover all 25 species of wildflowers",
        category="wildflower",
        required_items=["daisy","buttercup","clover","cornflower","sunflower","fireweed","bluebell","wood_anemone","trillium","lupine","iris","marsh_marigold","water_lily","arctic_poppy","redwood_violet","orchid","heliconia","passion_flower","hibiscus","plumeria","bleeding_heart","glowcap_bloom","mycelium_lily","desert_rose","sand_lily"],
    ),
    Achievement(
        id="fossil_sage",
        name="Fossil Sage",
        description="Unearth all 25 featured fossil specimens",
        category="fossil",
        required_items=["trilobite","brachiopod","crinoid","coral_colony","stromatolite","nautiloid","graptolite","orthoceras","spiriferid","blastoid","ammonite","fern_frond","pine_cone_fossil","sea_lily","cycad_frond","ichthyosaur_tooth","mosasaur_scale","pterosaur_bone","plesiosaur_vertebra","sauropod_scale","sabertooth","mammoth_molar","whale_bone","dire_wolf_tooth","elephant_ancestor_tusk"],
    ),
    Achievement(
        id="age_of_giants",
        name="Age of Giants",
        description="Discover 5 colossal Cenozoic beasts",
        category="fossil",
        required_items=["giant_sloth_claw", "glyptodon_plate", "cave_bear_claw", "terror_bird_bone", "ancient_bird"],
    ),

    # ------------------------------------------------------------------ prestige / themed
    Achievement(
        id="cave_dwellers",
        name="Cave Dwellers",
        description="Discover 5 deep-cave mushroom species",
        category="mushroom",
        required_items=[_MAGMA_CAP, _BIOLUME, _DEEP_INK, _OBSIDIAN_SHELF, _BLOOD_CAP],
    ),
    Achievement(
        id="fire_and_stone",
        name="Fire & Stone",
        description="Collect 5 volcanic and igneous rocks",
        category="rock",
        required_items=["granite", "basalt", "coal_gem", "pyrite", "jasper"],
    ),
    Achievement(
        id="water_wanderers",
        name="Water Wanderers",
        description="Find 5 water-loving wildflowers",
        category="wildflower",
        required_items=["iris", "marsh_marigold", "water_lily", "bluebell", "wood_anemone"],
    ),
    Achievement(
        id="shape_shifters",
        name="Shape Shifters",
        description="Find one mushroom of each distinct shape",
        category="mushroom",
        required_items=[_CAVE_MUSHROOM, _IVORY_BELL, _RUST_SHELF, _COAL_PUFF, _SULFUR_TUFT],
    ),
    Achievement(
        id="chromatic_crystals",
        name="Chromatic Crystals",
        description="Collect 5 vibrant deep-formed minerals",
        category="rock",
        required_items=["amethyst", "azurite", "malachite", "labradorite", "jade"],
    ),

    # ------------------------------------------------------------------ fish
    Achievement(
        id="riverbank_trio",
        name="Riverbank Trio",
        description="Catch 3 common freshwater fish",
        category="fish",
        required_items=["minnow", "perch", "bluegill"],
    ),
    Achievement(
        id="lakewater_sampler",
        name="Lakewater Sampler",
        description="Catch 5 lake fish varieties",
        category="fish",
        required_items=["carp", "bass", "walleye", "crappie", "sunfish"],
    ),
    Achievement(
        id="trout_run",
        name="Trout Run",
        description="Catch 5 cold-water trout and salmon species",
        category="fish",
        required_items=["trout", "salmon", "brook_trout", "steelhead", "arctic_char"],
    ),
    Achievement(
        id="golden_catch",
        name="Golden Catch",
        description="Land the elusive golden koi",
        category="fish",
        required_items=["golden_koi"],
    ),
    Achievement(
        id="deep_lake_dwellers",
        name="Deep Lake Dwellers",
        description="Catch 4 deep-lake giants",
        category="fish",
        required_items=["sturgeon", "burbot", "lake_whitefish", "muskie"],
    ),
    Achievement(
        id="tropical_angler",
        name="Tropical Angler",
        description="Catch 5 exotic tropical fish",
        category="fish",
        required_items=["piranha", "arapaima", "tilapia", "cichlid", "tambaqui"],
    ),
    Achievement(
        id="master_angler",
        name="Master Angler",
        description="Catch 20 distinct fish species",
        category="fish",
        required_items=["minnow","perch","bass","carp","bluegill","walleye","crappie","sunfish",
                        "trout","salmon","pike","sturgeon","arctic_char","brook_trout","steelhead",
                        "piranha","tilapia","cichlid","roach","tench"],
    ),
    Achievement(
        id="complete_creel",
        name="Complete Creel",
        description="Catch every fish species in the world",
        category="fish",
        required_items=["minnow","perch","bass","carp","bluegill","walleye","golden_koi","crappie",
                        "sunfish","channel_catfish","smallmouth_bass","yellow_perch","muskie","roach",
                        "rudd","tench","trout","salmon","pike","sturgeon","arctic_char","lake_whitefish",
                        "burbot","brook_trout","steelhead","piranha","arapaima","electric_eel","tilapia",
                        "cichlid","tambaqui","catfish"],
    ),
    Achievement(
        id="pike_pursuit",
        name="The Lurkers",
        description="Catch 3 ambush-predator fish",
        category="fish",
        required_items=["pike", "muskie", "smallmouth_bass"],
    ),
    Achievement(
        id="panfish_sampler",
        name="Panfish Sampler",
        description="Catch 5 panfish species",
        category="fish",
        required_items=["bluegill", "crappie", "perch", "sunfish", "yellow_perch"],
    ),
    Achievement(
        id="apex_anglers",
        name="Apex Anglers",
        description="Land 5 of the most formidable fish in the world",
        category="fish",
        required_items=["arapaima", "sturgeon", "electric_eel", "muskie", "pike"],
    ),
    Achievement(
        id="electric_waters",
        name="Electric Waters",
        description="Catch the legendary electric eel",
        category="fish",
        required_items=["electric_eel"],
    ),
    Achievement(
        id="old_creek_fish",
        name="Old Creek Fish",
        description="Catch 5 classic European freshwater species",
        category="fish",
        required_items=["roach", "rudd", "tench", "yellow_perch", "channel_catfish"],
    ),

    # ------------------------------------------------------------------ gems
    Achievement(
        id="first_facet",
        name="First Facet",
        description="Cut 3 beginner gemstones",
        category="gem",
        required_items=["amber", "garnet", "rose_quartz"],
    ),
    Achievement(
        id="royal_gems",
        name="Royal Gems",
        description="Cut the 5 classic precious gemstones",
        category="gem",
        required_items=["ruby", "sapphire", "emerald", "diamond", "alexandrite"],
    ),
    Achievement(
        id="volcanic_facets",
        name="Volcanic Facets",
        description="Cut 5 volcanic and deep-origin gems",
        category="gem",
        required_items=["obsidian", "jet", "peridot", "spinel", "garnet"],
    ),
    Achievement(
        id="ultra_rare_gems",
        name="Ultra Rare",
        description="Cut 5 of the rarest gems on earth",
        category="gem",
        required_items=["taafeite", "grandidierite", "painite", "musgravite", "jeremejevite"],
    ),
    Achievement(
        id="earths_palette_cut",
        name="Earth's Palette",
        description="Cut 5 richly colored opaque gems",
        category="gem",
        required_items=["malachite", "turquoise", "lapis_lazuli", "azurite", "sodalite"],
    ),
    Achievement(
        id="optical_wonders",
        name="Optical Wonders",
        description="Cut 5 gems with extraordinary optical effects",
        category="gem",
        required_items=["opal", "labradorite", "moonstone", "tiger_eye", "alexandrite"],
    ),
    Achievement(
        id="gem_rainbow",
        name="Gem Rainbow",
        description="Cut gems spanning every color of the spectrum",
        category="gem",
        required_items=["amethyst", "citrine", "topaz", "emerald", "sapphire", "ruby", "garnet"],
    ),
    Achievement(
        id="gem_connoisseur",
        name="Gem Connoisseur",
        description="Cut 30 distinct types of gemstone",
        category="gem",
        required_items=["amber","garnet","spinel","peridot","tourmaline","alexandrite","emerald",
                        "ruby","sapphire","diamond","jet","obsidian","rose_quartz","amethyst",
                        "citrine","turquoise","malachite","moonstone","labradorite","topaz","opal",
                        "lapis_lazuli","tanzanite","tsavorite","fluorite","carnelian","agate","onyx",
                        "tiger_eye","aventurine"],
    ),
    Achievement(
        id="padparadscha_prize",
        name="Padparadscha Prize",
        description="Cut 5 corundum and spinel-family gems",
        category="gem",
        required_items=["padparadscha", "ruby", "sapphire", "spinel", "tourmaline"],
    ),
    Achievement(
        id="beryl_family",
        name="Beryl Family",
        description="Cut 5 members of the beryl mineral family",
        category="gem",
        required_items=["emerald", "red_beryl", "morganite", "hiddenite", "euclase"],
    ),
    Achievement(
        id="deep_gems",
        name="Deep Formation",
        description="Cut 5 gems formed under extreme pressure",
        category="gem",
        required_items=["tanzanite", "tsavorite", "paraiba", "kunzite", "morganite"],
    ),

    # ------------------------------------------------------------------ birds
    Achievement(
        id="first_sighting",
        name="First Sighting",
        description="Spot 3 common bird species",
        category="bird",
        required_items=["robin", "sparrow", "finch"],
    ),
    Achievement(
        id="birds_of_prey",
        name="Birds of Prey",
        description="Spot 5 raptor species",
        category="bird",
        required_items=["eagle", "owl", "condor", "vulture", "peregrine_falcon"],
    ),
    Achievement(
        id="coastal_calls",
        name="Coastal Calls",
        description="Spot 5 coastal and seabird species",
        category="bird",
        required_items=["pelican", "puffin", "albatross", "gannet", "cormorant"],
    ),
    Achievement(
        id="tropical_plumage",
        name="Tropical Plumage",
        description="Spot 5 dazzling tropical birds",
        category="bird",
        required_items=["parrot", "toucan", "flamingo", "macaw", "peacock"],
    ),
    Achievement(
        id="night_watchers",
        name="Night Watchers",
        description="Spot 4 nocturnal bird species",
        category="bird",
        required_items=["owl", "nightjar", "barn_owl", "snowy_owl"],
    ),
    Achievement(
        id="wading_birds",
        name="Wading Birds",
        description="Spot 5 wading bird species",
        category="bird",
        required_items=["heron", "stork", "ibis", "spoonbill", "flamingo"],
    ),
    Achievement(
        id="songbird_chorus",
        name="Songbird Chorus",
        description="Spot 5 melodious songbird species",
        category="bird",
        required_items=["robin", "cardinal", "finch", "mockingbird", "cedar_waxwing"],
    ),
    Achievement(
        id="world_birder",
        name="World Birder",
        description="Spot 40 distinct bird species",
        category="bird",
        required_items=["robin","blue_jay","eagle","pelican","parrot","sparrow","heron",
                        "hummingbird","owl","crow","flamingo","toucan","cardinal","puffin",
                        "vulture","roadrunner","peacock","kookaburra","sandpiper","kingfisher",
                        "woodpecker","finch","stork","macaw","pheasant","condor","snow_bunting",
                        "prairie_falcon","nightjar","ibis","albatross","raven","swallow","crane",
                        "spoonbill","peregrine_falcon","barn_owl","magpie","golden_oriole","hoopoe"],
    ),
    Achievement(
        id="falcon_league",
        name="Falcon League",
        description="Spot 5 falcon and hawk species",
        category="bird",
        required_items=["eagle", "prairie_falcon", "peregrine_falcon", "osprey", "merlin"],
    ),
    Achievement(
        id="penguin_parade",
        name="Penguin Parade",
        description="Spot 5 penguin species",
        category="bird",
        required_items=["emperor_penguin", "king_penguin", "gentoo_penguin", "macaroni_penguin", "rock_hopper_penguin"],
    ),
    Achievement(
        id="bird_of_paradise",
        name="Avian Wonders",
        description="Spot 5 of the world's most spectacular birds",
        category="bird",
        required_items=["peacock", "quetzal", "lyrebird", "golden_pheasant", "mandarin_duck"],
    ),

    # ------------------------------------------------------------------ insects
    Achievement(
        id="bug_catcher",
        name="Bug Catcher",
        description="Catch 5 common butterfly species",
        category="insect",
        required_items=["monarch", "swallowtail", "blue_morpho", "painted_lady", "cabbage_white"],
    ),
    Achievement(
        id="beetle_cabinet",
        name="Beetle Cabinet",
        description="Catch 5 beetle species",
        category="insect",
        required_items=["stag_beetle", "ladybug", "jewel_beetle", "dung_beetle", "atlas_beetle"],
    ),
    Achievement(
        id="jungle_wings",
        name="Jungle Wings",
        description="Catch 5 jungle butterfly species",
        category="insect",
        required_items=["blue_morpho", "birdwing", "rajahs_birdwing", "common_tiger", "jungle_sailor"],
    ),
    Achievement(
        id="desert_collectors",
        name="Desert Collectors",
        description="Catch 5 desert insect species",
        category="insect",
        required_items=["desert_swallowtail", "arizona_skipper", "desert_orange_tip", "desert_dotted_blue", "desert_blister_beetle"],
    ),
    Achievement(
        id="exotic_beetles",
        name="Exotic Beetles",
        description="Catch 5 spectacular exotic beetle species",
        category="insect",
        required_items=["atlas_beetle", "rainbow_stag", "sacred_scarab", "goliath_beetle", "hercules_beetle"],
    ),
    Achievement(
        id="european_wings",
        name="European Wings",
        description="Catch 5 European butterfly species",
        category="insect",
        required_items=["purple_emperor", "chalkhill_blue", "silver_washed_fritillary", "marbled_white", "orange_tip"],
    ),
    Achievement(
        id="entomologist",
        name="Entomologist",
        description="Catch 25 distinct insect species",
        category="insect",
        required_items=["monarch","swallowtail","blue_morpho","painted_lady","cabbage_white",
                        "birdwing","skipper","copper","stag_beetle","ladybug","jewel_beetle",
                        "dung_beetle","atlas_beetle","rainbow_stag","sacred_scarab","tiger_beetle",
                        "purple_emperor","chalkhill_blue","silver_washed_fritillary","orange_tip",
                        "desert_swallowtail","desert_blister_beetle","common_blue","red_admiral","white_admiral"],
    ),
    Achievement(
        id="butterfly_master",
        name="Butterfly Master",
        description="Catch 20 butterfly species",
        category="insect",
        required_items=["monarch","swallowtail","blue_morpho","painted_lady","cabbage_white",
                        "birdwing","skipper","copper","purple_emperor","chalkhill_blue",
                        "silver_washed_fritillary","marbled_white","orange_tip","common_blue",
                        "holly_blue","red_admiral","white_admiral","rajahs_birdwing",
                        "common_tiger","zebra_longwing"],
    ),
    Achievement(
        id="amazon_wings",
        name="Amazon Wings",
        description="Catch 5 South American butterfly species",
        category="insect",
        required_items=["zebra_longwing", "postman_butterfly", "eighty_eight", "jungle_sailor", "malachite_butterfly"],
    ),
    Achievement(
        id="north_american_wings",
        name="North American Wings",
        description="Catch 5 North American butterfly species",
        category="insect",
        required_items=["eastern_tiger_swallowtail", "great_spangled_fritillary", "painted_lady", "monarch", "copper"],
    ),
    Achievement(
        id="insect_apex",
        name="Insect Apex",
        description="Catch the largest and rarest insects in the world",
        category="insect",
        required_items=["goliath_beetle", "hercules_beetle", "atlas_beetle", "rajahs_birdwing", "birdwing"],
    ),
    Achievement(
        id="african_collection",
        name="African Collection",
        description="Catch 5 African butterfly and insect species",
        category="insect",
        required_items=["african_migrant", "african_swordtail", "blue_diadem", "great_eggfly", "tawny_coaster"],
    ),

    # ------------------------------------------------------------------ shells
    Achievement(
        id="beachcomber",
        name="Beachcomber",
        description="Find 5 common tidal shells",
        category="shell",
        required_items=["cowrie", "scallop", "clam", "limpet", "periwinkle"],
    ),
    Achievement(
        id="tidal_treasures",
        name="Tidal Treasures",
        description="Find 5 classic tidal shell varieties",
        category="shell",
        required_items=["cowrie", "cone", "scallop", "cockle", "whelk"],
    ),
    Achievement(
        id="reef_diver",
        name="Reef Diver",
        description="Find 5 deep reef shell species",
        category="shell",
        required_items=["oyster", "nautilus", "triton", "murex", "abalone"],
    ),
    Achievement(
        id="cowrie_crown",
        name="Cowrie Crown",
        description="Find 5 cowrie shell varieties",
        category="shell",
        required_items=["cowrie", "tiger_cowrie", "map_cowrie", "golden_cowrie", "chestnut_cowrie"],
    ),
    Achievement(
        id="snail_trail",
        name="Snail Trail",
        description="Find 5 gastropod shell varieties",
        category="shell",
        required_items=["moon_snail", "olive", "auger", "turritella", "nassa"],
    ),
    Achievement(
        id="rarest_shells",
        name="The Rarest Finds",
        description="Find 5 exceptionally rare shell specimens",
        category="shell",
        required_items=["slit_shell", "imperial_volute", "royal_volute", "baler_shell", "junonia"],
    ),
    Achievement(
        id="shell_artisan",
        name="Shell Artisan",
        description="Find 20 distinct shell species",
        category="shell",
        required_items=["cowrie","cone","scallop","clam","periwinkle","limpet","whelk",
                        "moon_snail","olive","auger","cockle","jingle_shell","blue_mussel",
                        "pelican_foot","oyster","abalone","murex","nautilus","triton","tiger_cowrie"],
    ),
    Achievement(
        id="shell_sage",
        name="Shell Sage",
        description="Find 30 tidal shell species",
        category="shell",
        required_items=["cowrie","cone","scallop","clam","periwinkle","limpet","whelk","sundial",
                        "top_shell","nerite","tellin","auger","cockle","moon_snail","olive",
                        "bubble_shell","horn_shell","ark_shell","jingle_shell","blue_mussel",
                        "coquina","keyhole_limpet","slipper_shell","nutmeg","pelican_foot",
                        "dove_shell","turban","cerith","violet_snail","nassa"],
    ),
    Achievement(
        id="volute_vault",
        name="Volute Vault",
        description="Find 5 volute and harp shell species",
        category="shell",
        required_items=["volute", "imperial_volute", "royal_volute", "baler_shell", "harp"],
    ),
    Achievement(
        id="tidal_pool",
        name="Tidal Pool",
        description="Find 5 tidal pool shell species",
        category="shell",
        required_items=["keyhole_limpet", "slipper_shell", "jingle_shell", "coquina", "pelican_foot"],
    ),
    Achievement(
        id="bivalve_collection",
        name="Bivalve Collection",
        description="Find 5 bivalve shell species",
        category="shell",
        required_items=["oyster", "clam", "scallop", "blue_mussel", "giant_clam"],
    ),

    # ------------------------------------------------------------------ coffee
    Achievement(
        id="highland_roast",
        name="Highland Roast",
        description="Roast coffee from 2 mountain biomes",
        category="coffee",
        required_items=["alpine_mountain_light", "rocky_mountain_light"],
    ),
    Achievement(
        id="dark_roast_explorer",
        name="Dark Roast Explorer",
        description="Roast 3 dark coffees from different biomes",
        category="coffee",
        required_items=["tropical_dark", "jungle_dark", "savanna_dark"],
    ),
    Achievement(
        id="light_roast_collection",
        name="Light Roast Collection",
        description="Roast light coffees from 4 different biomes",
        category="coffee",
        required_items=["tropical_light", "alpine_mountain_light", "rolling_hills_light", "jungle_light"],
    ),
    Achievement(
        id="coffee_connoisseur",
        name="Coffee Connoisseur",
        description="Roast coffee from 8 different biomes",
        category="coffee",
        required_items=["tropical_light","jungle_medium","alpine_mountain_light","rolling_hills_medium",
                        "arid_steppe_dark","canyon_dark","boreal_light","beach_medium"],
    ),

    # ------------------------------------------------------------------ wine
    Achievement(
        id="first_vintage",
        name="First Vintage",
        description="Produce wine using 2 different crush styles",
        category="wine",
        required_items=["rolling_hills_whole_cluster", "tropical_destemmed"],
    ),
    Achievement(
        id="winemaker_styles",
        name="Winemaker's Craft",
        description="Master all 4 crush styles from one biome",
        category="wine",
        required_items=["rolling_hills_whole_cluster", "rolling_hills_destemmed",
                        "rolling_hills_rose_bleed", "rolling_hills_skin_fermented"],
    ),
    Achievement(
        id="terroir_masters",
        name="Terroir Masters",
        description="Produce wine from 4 distinct mountain and hill biomes",
        category="wine",
        required_items=["rolling_hills_whole_cluster", "alpine_mountain_whole_cluster",
                        "rocky_mountain_whole_cluster", "canyon_skin_fermented"],
    ),
    Achievement(
        id="wine_collector",
        name="Wine Collector",
        description="Produce wine from 8 different biomes",
        category="wine",
        required_items=["rolling_hills_whole_cluster","alpine_mountain_whole_cluster",
                        "tropical_destemmed","jungle_destemmed","canyon_skin_fermented",
                        "arid_steppe_skin_fermented","beach_rose_bleed","tundra_whole_cluster"],
    ),

    # ------------------------------------------------------------------ tea
    Achievement(
        id="first_steep",
        name="First Steep",
        description="Process tea from 2 different biomes",
        category="tea",
        required_items=["alpine_mountain_white", "jungle_green"],
    ),
    Achievement(
        id="green_tea_path",
        name="Green Tea Path",
        description="Process green tea from 3 different biomes",
        category="tea",
        required_items=["jungle_green", "tropical_green", "rolling_hills_green"],
    ),
    Achievement(
        id="black_tea_master",
        name="Black Tea Master",
        description="Process black tea from 3 different biomes",
        category="tea",
        required_items=["alpine_mountain_black", "bamboo_forest_black", "rolling_hills_black"],
    ),
    Achievement(
        id="tea_connoisseur",
        name="Tea Connoisseur",
        description="Process 6 distinct tea types from different biomes",
        category="tea",
        required_items=["alpine_mountain_white","jungle_green","rolling_hills_oolong",
                        "bamboo_forest_hojicha","tropical_green","alpine_mountain_black"],
    ),
    Achievement(
        id="mountain_tea",
        name="Mountain Tea",
        description="Process 3 tea types from alpine mountain biomes",
        category="tea",
        required_items=["alpine_mountain_white", "alpine_mountain_green", "alpine_mountain_oolong"],
    ),

    # ------------------------------------------------------------------ beer
    Achievement(
        id="first_pint",
        name="First Pint",
        description="Condition beer from 2 different biomes",
        category="beer",
        required_items=["tropical_standard", "rolling_hills_standard"],
    ),
    Achievement(
        id="reserve_brewer",
        name="Reserve Brewer",
        description="Produce 3 reserve-quality beers from different biomes",
        category="beer",
        required_items=["tropical_reserve", "rolling_hills_reserve", "canyon_reserve"],
    ),
    Achievement(
        id="biome_brewery",
        name="Biome Brewery",
        description="Brew beer from 5 distinct biomes",
        category="beer",
        required_items=["tropical_standard","jungle_standard","canyon_standard",
                        "alpine_mountain_standard","rolling_hills_standard"],
    ),
    Achievement(
        id="beer_master",
        name="Beer Master",
        description="Brew fine or better beer from 8 different biomes",
        category="beer",
        required_items=["tropical_fine","jungle_fine","canyon_fine","alpine_mountain_fine",
                        "rolling_hills_fine","savanna_standard","beach_standard","arid_steppe_standard"],
    ),

    # ------------------------------------------------------------------ spirits
    Achievement(
        id="first_dram",
        name="First Dram",
        description="Distill spirits from 2 different biomes",
        category="spirit",
        required_items=["tropical_young", "rolling_hills_young"],
    ),
    Achievement(
        id="aged_collection",
        name="Aged Collection",
        description="Age spirits from 3 different mountain biomes",
        category="spirit",
        required_items=["alpine_mountain_aged", "canyon_aged", "rocky_mountain_aged"],
    ),
    Achievement(
        id="reserve_spirits",
        name="Reserve Spirits",
        description="Produce 3 reserve-quality spirits from different biomes",
        category="spirit",
        required_items=["tropical_reserve", "jungle_reserve", "rolling_hills_reserve"],
    ),
    Achievement(
        id="master_distiller",
        name="Master Distiller",
        description="Distill aged spirits from 8 different biomes",
        category="spirit",
        required_items=["tropical_aged","jungle_aged","alpine_mountain_aged","rocky_mountain_aged",
                        "canyon_aged","rolling_hills_aged","savanna_aged","tundra_aged"],
    ),

    # ------------------------------------------------------------------ mushroom extras
    Achievement(
        id="fiery_fungi",
        name="Fiery Fungi",
        description="Discover 5 hot-colored and volcanic fungi",
        category="mushroom",
        required_items=[_EMBER_CAP, _MAGMA_CAP, _BLOOD_CAP, _GOLD_CHANTERELLE, _AMBER_PUFF],
    ),
    Achievement(
        id="pale_harvest",
        name="Pale Harvest",
        description="Discover 4 pale and ghostly fungi",
        category="mushroom",
        required_items=[_PALE_GHOST, _IVORY_BELL, _STONE_PUFF, _BONE_STALK],
    ),
    Achievement(
        id="deep_shelf",
        name="Deep Shelf",
        description="Discover all 3 shelf fungus varieties",
        category="mushroom",
        required_items=[_RUST_SHELF, _COPPER_SHELF, _OBSIDIAN_SHELF],
    ),
    Achievement(
        id="glow_dark",
        name="Glow in the Dark",
        description="Discover 3 bioluminescent and phosphorescent fungi",
        category="mushroom",
        required_items=[_BIOLUME, _TEAL_BELL, _DEEP_INK],
    ),
    Achievement(
        id="tuft_master",
        name="Tuft Master",
        description="Discover 5 cluster and tuft fungi",
        category="mushroom",
        required_items=[_SULFUR_TUFT, _CORAL_TUFT, _HONEY_CLUSTER, _AMBER_PUFF, _COAL_PUFF],
    ),

    # ------------------------------------------------------------------ rock extras
    Achievement(
        id="sedimentary_set",
        name="Sedimentary Set",
        description="Collect 5 shallow sedimentary rocks",
        category="rock",
        required_items=["limestone", "sandstone", "chalk", "slate", "flint"],
    ),
    Achievement(
        id="crystal_rock_collection",
        name="Crystal Rock Collection",
        description="Collect 5 crystalline rock specimens",
        category="rock",
        required_items=["quartz", "citrine", "jade", "jasper", "dolomite"],
    ),
    Achievement(
        id="rare_specimens",
        name="Rare Specimens",
        description="Collect 5 exotic and otherworldly rock specimens",
        category="rock",
        required_items=["voidite", "void_crystal", "meteorite", "bloodstone", "moonstone"],
    ),
    Achievement(
        id="metallic_minerals",
        name="Metallic Minerals",
        description="Collect 5 metallic mineral specimens",
        category="rock",
        required_items=["pyrite", "tourmaline", "malachite", "azurite", "rhodonite"],
    ),
    Achievement(
        id="deep_minerals_rock",
        name="Deep Minerals",
        description="Collect 5 deep-formed mineral specimens",
        category="rock",
        required_items=["tourmaline", "rhodonite", "bloodstone", "moonstone", "jade"],
    ),

    # ------------------------------------------------------------------ wildflower extras
    Achievement(
        id="sun_lovers",
        name="Sun Lovers",
        description="Find 5 sun-loving wildflowers",
        category="wildflower",
        required_items=["daisy", "sunflower", "buttercup", "cornflower", "desert_rose"],
    ),
    Achievement(
        id="cold_blooms",
        name="Cold Blooms",
        description="Find 4 cold-climate wildflowers",
        category="wildflower",
        required_items=["arctic_poppy", "bluebell", "wood_anemone", "trillium"],
    ),
    Achievement(
        id="alien_flowers",
        name="Alien Flowers",
        description="Find 4 strange and otherworldly wildflowers",
        category="wildflower",
        required_items=["glowcap_bloom", "mycelium_lily", "bleeding_heart", "sand_lily"],
    ),
    Achievement(
        id="tropical_garden",
        name="Tropical Garden",
        description="Find 5 tropical wildflowers",
        category="wildflower",
        required_items=["orchid", "heliconia", "passion_flower", "hibiscus", "plumeria"],
    ),
    Achievement(
        id="desert_wildflowers",
        name="Desert Blooms",
        description="Find 4 desert and dry-land wildflowers",
        category="wildflower",
        required_items=["desert_rose", "sand_lily", "buttercup", "cornflower"],
    ),
    Achievement(
        id="bioluminescent_forest",
        name="Bioluminescent Forest",
        description="Find 4 rare glowing and deep-forest wildflowers",
        category="wildflower",
        required_items=["glowcap_bloom", "mycelium_lily", "redwood_violet", "fireweed"],
    ),

    # ------------------------------------------------------------------ fossil extras
    Achievement(
        id="coastal_fossils",
        name="Ancient Seas",
        description="Discover 5 marine invertebrate fossils",
        category="fossil",
        required_items=["trilobite", "nautiloid", "orthoceras", "ammonite", "crinoid"],
    ),
    Achievement(
        id="flora_fossils",
        name="Flora Fossils",
        description="Discover 5 ancient plant and sessile fossils",
        category="fossil",
        required_items=["fern_frond", "pine_cone_fossil", "cycad_frond", "crinoid", "coral_colony"],
    ),
    Achievement(
        id="micro_fossils",
        name="Micro Fossils",
        description="Discover 4 tiny and microscopic fossil specimens",
        category="fossil",
        required_items=["graptolite", "spiriferid", "blastoid", "stromatolite"],
    ),
    Achievement(
        id="apex_predators_fossils",
        name="Apex Predators",
        description="Discover 5 fossil remains of ancient apex predators",
        category="fossil",
        required_items=["sabertooth", "dire_wolf_tooth", "terror_bird_bone", "giant_sloth_claw", "cave_bear_claw"],
    ),
    Achievement(
        id="late_mesozoic_fossils",
        name="Late Mesozoic",
        description="Discover 5 Late Mesozoic marine reptile fossils",
        category="fossil",
        required_items=["ammonite", "ichthyosaur_tooth", "mosasaur_scale", "pterosaur_bone", "plesiosaur_vertebra"],
    ),

    # ------------------------------------------------------------------ hunting
    Achievement(
        id="first_kill",
        name="First Hunt",
        description="Hunt your first deer",
        category="hunt",
        required_items=["deer"],
    ),
    Achievement(
        id="small_game_hunter",
        name="Small Game Hunter",
        description="Hunt 5 small game species",
        category="hunt",
        required_items=["rabbit", "turkey", "duck", "pheasant", "goose"],
    ),
    Achievement(
        id="big_game_hunter",
        name="Big Game Hunter",
        description="Hunt 5 large game species",
        category="hunt",
        required_items=["deer", "elk", "moose", "bison", "boar"],
    ),
    Achievement(
        id="predator_hunter",
        name="Predator Hunter",
        description="Hunt 5 dangerous predator species",
        category="hunt",
        required_items=["wolf", "bear", "fox", "crocodile", "arctic_fox"],
    ),
    Achievement(
        id="master_of_the_wild",
        name="Master of the Wild",
        description="Hunt 12 different animal species",
        category="hunt",
        required_items=["deer","boar","rabbit","turkey","wolf","bear",
                        "duck","elk","fox","moose","pheasant","goose"],
    ),

    # ------------------------------------------------------------------ trophy room (all hunts)
    Achievement(
        id="trophy_room",
        name="Trophy Room",
        description="Collect a hunting trophy from every animal in the world",
        category="hunt",
        required_items=["deer","boar","rabbit","turkey","wolf","bear","duck","elk","bison",
                        "fox","arctic_fox","moose","bighorn","pheasant","warthog","musk_ox",
                        "crocodile","goose","hare","capybara"],
    ),

    # ------------------------------------------------------------------ horse racing
    Achievement(
        id="first_past_the_post",
        name="First Past the Post",
        description="Win a horse race",
        category="horse_racing",
        required_items=["winner"],
    ),

    # ------------------------------------------------------------------ dog racing
    Achievement(
        id="best_in_breed",
        name="Best in Breed",
        description="Win a dog race",
        category="dog_racing",
        required_items=["winner"],
    ),
]

# Map achievement_id -> Achievement for fast lookup
ACHIEVEMENT_BY_ID = {a.id: a for a in ACHIEVEMENTS}

# Display names for mushroom block_ids (mirrors _MUSHROOM_NAMES in ui.py)
MUSHROOM_DISPLAY_NAMES = {
    _CAVE_MUSHROOM: "Cave Mushroom",   _EMBER_CAP: "Ember Cap",
    _PALE_GHOST: "Pale Ghost",         _GOLD_CHANTERELLE: "Gold Chanterelle",
    _COBALT_CAP: "Cobalt Cap",         _MOSSY_CAP: "Mossy Cap",
    _VIOLET_CROWN: "Violet Crown",     _BLOOD_CAP: "Blood Cap",
    _SULFUR_DOME: "Sulfur Dome",       _IVORY_BELL: "Ivory Bell",
    _ASH_BELL: "Ash Bell",             _TEAL_BELL: "Teal Bell",
    _RUST_SHELF: "Rust Shelf",         _COPPER_SHELF: "Copper Shelf",
    _OBSIDIAN_SHELF: "Obsidian Shelf", _COAL_PUFF: "Coal Puff",
    _STONE_PUFF: "Stone Puff",         _AMBER_PUFF: "Amber Puff",
    _SULFUR_TUFT: "Sulfur Tuft",       _HONEY_CLUSTER: "Honey Cluster",
    _CORAL_TUFT: "Coral Tuft",         _BONE_STALK: "Bone Stalk",
    _MAGMA_CAP: "Magma Cap",           _DEEP_INK: "Deep Ink",
    _BIOLUME: "Biolume",
}


def item_display_name(category: str, item) -> str:
    """Return a human-readable name for an achievement item."""
    if category == "mushroom":
        return MUSHROOM_DISPLAY_NAMES.get(item, str(item))
    return str(item).replace("_", " ").title()


def get_achievement_progress(ach: Achievement, global_collection: dict) -> tuple[int, int]:
    """Return (found_count, total_count) for an achievement given the global collection."""
    cat_items = global_collection.get(ach.category, set())
    found = sum(1 for r in ach.required_items if str(r) in cat_items)
    return found, len(ach.required_items)
