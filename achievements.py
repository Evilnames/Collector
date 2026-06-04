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

    # ============================================================ NEW BATCH (+50)

    # -------- mushroom (5)
    Achievement(
        id="crimson_caps",
        name="Crimson Caps",
        description="Discover the 3 red-hot cap fungi",
        category="mushroom",
        required_items=[_BLOOD_CAP, _MAGMA_CAP, _EMBER_CAP],
    ),
    Achievement(
        id="bell_devotee",
        name="Bell Devotee",
        description="Discover every bell mushroom variety",
        category="mushroom",
        required_items=[_IVORY_BELL, _ASH_BELL, _TEAL_BELL],
    ),
    Achievement(
        id="puffball_brigade",
        name="Puffball Brigade",
        description="Discover all 4 puffball fungi",
        category="mushroom",
        required_items=[_COAL_PUFF, _STONE_PUFF, _AMBER_PUFF, _COBALT_CAP],
    ),
    Achievement(
        id="forager_first_basket",
        name="Forager's First Basket",
        description="Discover any 3 edible-looking mushrooms",
        category="mushroom",
        required_items=[_CAVE_MUSHROOM, _GOLD_CHANTERELLE, _HONEY_CLUSTER],
    ),
    Achievement(
        id="dark_dome_finds",
        name="Dark Dome Finds",
        description="Discover 4 fungi exclusive to the deepest caves",
        category="mushroom",
        required_items=[_DEEP_INK, _MAGMA_CAP, _OBSIDIAN_SHELF, _BIOLUME],
    ),

    # -------- rock (5)
    Achievement(
        id="pebble_path",
        name="Pebble Path",
        description="Collect 3 of the most common shore rocks",
        category="rock",
        required_items=["flint", "chalk", "slate"],
    ),
    Achievement(
        id="mountain_collector",
        name="Mountain Collector",
        description="Collect 5 rocks born of mountain pressure",
        category="rock",
        required_items=["granite", "basalt", "quartz", "dolomite", "pyrite"],
    ),
    Achievement(
        id="painters_palette",
        name="Painter's Palette",
        description="Collect 4 vividly pigmented mineral rocks",
        category="rock",
        required_items=["jasper", "malachite", "azurite", "tourmaline"],
    ),
    Achievement(
        id="moonlit_finds",
        name="Moonlit Finds",
        description="Collect 3 rocks that shimmer in low light",
        category="rock",
        required_items=["moonstone", "labradorite", "bloodstone"],
    ),
    Achievement(
        id="from_the_void",
        name="From the Void",
        description="Collect 3 otherworldly rock specimens",
        category="rock",
        required_items=["voidite", "void_crystal", "meteorite"],
    ),

    # -------- wildflower (5)
    Achievement(
        id="white_petals",
        name="White Petals",
        description="Find 4 white-flowering wildflowers",
        category="wildflower",
        required_items=["daisy", "water_lily", "arctic_poppy", "sand_lily"],
    ),
    Achievement(
        id="blue_meadow",
        name="Blue Meadow",
        description="Find 4 blue-petaled wildflowers",
        category="wildflower",
        required_items=["cornflower", "bluebell", "iris", "lupine"],
    ),
    Achievement(
        id="red_garden",
        name="Red Garden",
        description="Find 4 red-flowered wildflowers",
        category="wildflower",
        required_items=["hibiscus", "bleeding_heart", "fireweed", "passion_flower"],
    ),
    Achievement(
        id="yellow_field",
        name="Yellow Field",
        description="Find 4 yellow-flowered wildflowers",
        category="wildflower",
        required_items=["sunflower", "buttercup", "marsh_marigold", "plumeria"],
    ),
    Achievement(
        id="spring_walk",
        name="Spring Walk",
        description="Find 5 wildflowers that bloom in early spring",
        category="wildflower",
        required_items=["daisy", "buttercup", "clover", "bluebell", "trillium"],
    ),

    # -------- fossil (5)
    Achievement(
        id="shelled_pasts",
        name="Shelled Pasts",
        description="Unearth 4 ancient shelled invertebrates",
        category="fossil",
        required_items=["ammonite", "nautiloid", "orthoceras", "spiriferid"],
    ),
    Achievement(
        id="plant_imprints",
        name="Plant Imprints",
        description="Unearth 3 ancient plant fossils",
        category="fossil",
        required_items=["fern_frond", "cycad_frond", "pine_cone_fossil"],
    ),
    Achievement(
        id="great_lizards",
        name="Great Lizards",
        description="Unearth 5 fossil traces of giant reptiles",
        category="fossil",
        required_items=["sauropod_scale", "pterosaur_bone", "plesiosaur_vertebra", "ichthyosaur_tooth", "mosasaur_scale"],
    ),
    Achievement(
        id="megafauna_bones",
        name="Megafauna Bones",
        description="Unearth 4 ice age megafauna fossils",
        category="fossil",
        required_items=["mammoth_molar", "elephant_ancestor_tusk", "whale_bone", "giant_sloth_claw"],
    ),
    Achievement(
        id="microscopic_giants",
        name="Microscopic Giants",
        description="Unearth 4 small-yet-ancient invertebrate fossils",
        category="fossil",
        required_items=["trilobite", "brachiopod", "graptolite", "blastoid"],
    ),

    # -------- gem (5)
    Achievement(
        id="crystal_starter",
        name="Crystal Starter",
        description="Cut 4 entry-level gemstones",
        category="gem",
        required_items=["amber", "garnet", "rose_quartz", "amethyst"],
    ),
    Achievement(
        id="crown_jewels",
        name="Crown Jewels",
        description="Cut the 4 most prized gemstones",
        category="gem",
        required_items=["ruby", "sapphire", "emerald", "diamond"],
    ),
    Achievement(
        id="quartz_family_gem",
        name="Quartz Family",
        description="Cut 4 members of the quartz family",
        category="gem",
        required_items=["rose_quartz", "amethyst", "citrine", "tiger_eye"],
    ),
    Achievement(
        id="fire_gem_set",
        name="Fire Gems",
        description="Cut 5 fiery-hued gemstones",
        category="gem",
        required_items=["garnet", "ruby", "padparadscha", "spinel", "carnelian"],
    ),
    Achievement(
        id="cool_crystals",
        name="Cool Crystals",
        description="Cut 5 cool-hued rare gemstones",
        category="gem",
        required_items=["tanzanite", "paraiba", "kunzite", "tsavorite", "peridot"],
    ),

    # -------- fish (5)
    Achievement(
        id="cold_stream",
        name="Cold Stream",
        description="Catch 4 cold-stream fish",
        category="fish",
        required_items=["trout", "salmon", "brook_trout", "arctic_char"],
    ),
    Achievement(
        id="bottom_feeders",
        name="Bottom Feeders",
        description="Catch 4 bottom-dwelling fish",
        category="fish",
        required_items=["catfish", "channel_catfish", "carp", "burbot"],
    ),
    Achievement(
        id="river_giants",
        name="River Giants",
        description="Catch 4 enormous river fish",
        category="fish",
        required_items=["sturgeon", "arapaima", "pike", "muskie"],
    ),
    Achievement(
        id="small_fry",
        name="Small Fry",
        description="Catch 4 of the smallest freshwater fish",
        category="fish",
        required_items=["minnow", "roach", "rudd", "tench"],
    ),
    Achievement(
        id="bass_brigade",
        name="Bass Brigade",
        description="Catch 4 bass and perch species",
        category="fish",
        required_items=["bass", "smallmouth_bass", "yellow_perch", "perch"],
    ),

    # -------- bird (5)
    Achievement(
        id="backyard_birder",
        name="Backyard Birder",
        description="Spot 5 familiar garden birds",
        category="bird",
        required_items=["robin", "sparrow", "blue_jay", "cardinal", "finch"],
    ),
    Achievement(
        id="shoreline_watch",
        name="Shoreline Watch",
        description="Spot 5 coastal birds along the shore",
        category="bird",
        required_items=["pelican", "gannet", "sandpiper", "cormorant", "puffin"],
    ),
    Achievement(
        id="great_raptors",
        name="Great Raptors",
        description="Spot 3 of the most majestic raptors",
        category="bird",
        required_items=["eagle", "condor", "vulture"],
    ),
    Achievement(
        id="rainbow_birds",
        name="Rainbow Birds",
        description="Spot 4 brilliantly colored birds",
        category="bird",
        required_items=["parrot", "macaw", "toucan", "golden_oriole"],
    ),
    Achievement(
        id="frozen_flyers",
        name="Frozen Flyers",
        description="Spot 4 birds adapted to the cold",
        category="bird",
        required_items=["snowy_owl", "snow_bunting", "emperor_penguin", "king_penguin"],
    ),

    # -------- insect (5)
    Achievement(
        id="blue_wings",
        name="Blue Wings",
        description="Catch 4 blue butterfly species",
        category="insect",
        required_items=["blue_morpho", "common_blue", "chalkhill_blue", "holly_blue"],
    ),
    Achievement(
        id="garden_visitors",
        name="Garden Visitors",
        description="Catch 4 butterflies that frequent gardens",
        category="insect",
        required_items=["monarch", "painted_lady", "copper", "swallowtail"],
    ),
    Achievement(
        id="armored_critters",
        name="Armored Critters",
        description="Catch 5 beetle species",
        category="insect",
        required_items=["stag_beetle", "ladybug", "jewel_beetle", "sacred_scarab", "tiger_beetle"],
    ),
    Achievement(
        id="titan_beetles",
        name="Titan Beetles",
        description="Catch 4 of the largest beetles in the world",
        category="insect",
        required_items=["atlas_beetle", "goliath_beetle", "hercules_beetle", "rainbow_stag"],
    ),
    Achievement(
        id="admirals_and_emperors",
        name="Admirals & Emperors",
        description="Catch 4 regal butterfly species",
        category="insect",
        required_items=["red_admiral", "white_admiral", "purple_emperor", "marbled_white"],
    ),

    # -------- shell (5)
    Achievement(
        id="cowrie_curator",
        name="Cowrie Curator",
        description="Find 4 cowrie shell varieties",
        category="shell",
        required_items=["cowrie", "tiger_cowrie", "golden_cowrie", "map_cowrie"],
    ),
    Achievement(
        id="spiral_seekers",
        name="Spiral Seekers",
        description="Find 5 spiral-shelled mollusks",
        category="shell",
        required_items=["nautilus", "triton", "turritella", "auger", "cerith"],
    ),
    Achievement(
        id="bivalve_basket",
        name="Bivalve Basket",
        description="Find 4 common bivalves",
        category="shell",
        required_items=["clam", "oyster", "scallop", "blue_mussel"],
    ),
    Achievement(
        id="rare_carrier",
        name="Rare Carrier",
        description="Find 5 famously rare shells",
        category="shell",
        required_items=["junonia", "baler_shell", "imperial_volute", "royal_volute", "harp"],
    ),
    Achievement(
        id="first_seashells",
        name="First Seashells",
        description="Find 4 starter beach shells",
        category="shell",
        required_items=["cowrie", "clam", "scallop", "limpet"],
    ),

    # -------- coffee / wine / tea / beer / spirits (5)
    Achievement(
        id="coffee_continental",
        name="Coffee Continental",
        description="Roast coffee from 4 continents' worth of biomes",
        category="coffee",
        required_items=["tropical_light", "jungle_medium", "alpine_mountain_light", "beach_medium"],
    ),
    Achievement(
        id="estate_vintner",
        name="Estate Vintner",
        description="Produce wine from 4 distinct terroirs",
        category="wine",
        required_items=["rolling_hills_whole_cluster", "tropical_destemmed", "jungle_destemmed", "canyon_skin_fermented"],
    ),
    Achievement(
        id="tea_garden_tour",
        name="Tea Garden Tour",
        description="Process 4 teas spanning warm and cool biomes",
        category="tea",
        required_items=["jungle_green", "tropical_green", "alpine_mountain_white", "alpine_mountain_oolong"],
    ),
    Achievement(
        id="craft_brewer",
        name="Craft Brewer",
        description="Brew standard beer from 4 different biomes",
        category="beer",
        required_items=["tropical_standard", "canyon_standard", "beach_standard", "jungle_standard"],
    ),
    Achievement(
        id="cellar_run",
        name="Cellar Run",
        description="Age spirits across 4 mountainous biomes",
        category="spirit",
        required_items=["jungle_aged", "alpine_mountain_aged", "canyon_aged", "rocky_mountain_aged"],
    ),

    # ============================================================ NEW BATCH (+50)

    # -------- mushroom (5)
    Achievement(
        id="mossy_growth",
        name="Mossy Growth",
        description="Discover 3 vividly tinted cap mushrooms",
        category="mushroom",
        required_items=[_MOSSY_CAP, _COBALT_CAP, _VIOLET_CROWN],
    ),
    Achievement(
        id="sulfur_set",
        name="Sulfur Set",
        description="Discover both sulfur-yellow fungi",
        category="mushroom",
        required_items=[_SULFUR_DOME, _SULFUR_TUFT],
    ),
    Achievement(
        id="coral_and_bone",
        name="Coral & Bone",
        description="Discover 3 strangely-shaped cave fungi",
        category="mushroom",
        required_items=[_CORAL_TUFT, _BONE_STALK, _BIOLUME],
    ),
    Achievement(
        id="earthbound_caps",
        name="Earthbound Caps",
        description="Discover 3 shallow-cave cap mushrooms",
        category="mushroom",
        required_items=[_CAVE_MUSHROOM, _GOLD_CHANTERELLE, _MOSSY_CAP],
    ),
    Achievement(
        id="fungal_apprentice",
        name="Fungal Apprentice",
        description="Discover 10 mushroom species",
        category="mushroom",
        required_items=[_CAVE_MUSHROOM, _EMBER_CAP, _GOLD_CHANTERELLE, _MOSSY_CAP, _IVORY_BELL,
                        _RUST_SHELF, _COAL_PUFF, _AMBER_PUFF, _HONEY_CLUSTER, _BIOLUME],
    ),

    # -------- rock (5)
    Achievement(
        id="shoreline_rocks",
        name="Shoreline Rocks",
        description="Collect 4 stones found near coastlines",
        category="rock",
        required_items=["flint", "limestone", "sandstone", "chalk"],
    ),
    Achievement(
        id="green_minerals",
        name="Green Minerals",
        description="Collect 3 green-tinted minerals",
        category="rock",
        required_items=["jade", "malachite", "tourmaline"],
    ),
    Achievement(
        id="red_rocks",
        name="Red Rocks",
        description="Collect 3 red-banded rock specimens",
        category="rock",
        required_items=["bloodstone", "jasper", "rhodonite"],
    ),
    Achievement(
        id="apprentice_geologist",
        name="Apprentice Geologist",
        description="Collect 10 rock types",
        category="rock",
        required_items=["flint", "limestone", "sandstone", "slate", "chalk",
                        "granite", "coal_gem", "basalt", "dolomite", "quartz"],
    ),
    Achievement(
        id="underdark_specimens",
        name="Underdark Specimens",
        description="Collect 4 stones formed under heat or impact",
        category="rock",
        required_items=["voidite", "void_crystal", "meteorite", "basalt"],
    ),

    # -------- wildflower (5)
    Achievement(
        id="purple_flowers",
        name="Purple Flowers",
        description="Find 4 purple-petaled wildflowers",
        category="wildflower",
        required_items=["lupine", "iris", "orchid", "passion_flower"],
    ),
    Achievement(
        id="exotic_quartet",
        name="Exotic Quartet",
        description="Find 4 exotic tropical wildflowers",
        category="wildflower",
        required_items=["heliconia", "plumeria", "hibiscus", "orchid"],
    ),
    Achievement(
        id="cave_garden",
        name="Cave Garden",
        description="Find 3 wildflowers that thrive without sunlight",
        category="wildflower",
        required_items=["glowcap_bloom", "mycelium_lily", "redwood_violet"],
    ),
    Achievement(
        id="botanical_apprentice",
        name="Botanical Apprentice",
        description="Discover 10 wildflower species",
        category="wildflower",
        required_items=["daisy", "buttercup", "clover", "cornflower", "sunflower",
                        "fireweed", "bluebell", "iris", "water_lily", "orchid"],
    ),
    Achievement(
        id="tundra_walk",
        name="Tundra Walk",
        description="Find 3 flowers that bloom in cold soil",
        category="wildflower",
        required_items=["arctic_poppy", "fireweed", "marsh_marigold"],
    ),

    # -------- fossil (5)
    Achievement(
        id="coral_seabed",
        name="Coral Seabed",
        description="Unearth 4 fossils from ancient reef floors",
        category="fossil",
        required_items=["coral_colony", "sea_lily", "stromatolite", "crinoid"],
    ),
    Achievement(
        id="molluscan_remains",
        name="Molluscan Remains",
        description="Unearth 4 cephalopod and brachiopod fossils",
        category="fossil",
        required_items=["ammonite", "nautiloid", "orthoceras", "brachiopod"],
    ),
    Achievement(
        id="paleontologist_apprentice",
        name="Paleontologist Apprentice",
        description="Unearth 10 fossil specimens",
        category="fossil",
        required_items=["trilobite", "brachiopod", "crinoid", "coral_colony", "ammonite",
                        "fern_frond", "sabertooth", "mammoth_molar", "whale_bone", "ichthyosaur_tooth"],
    ),
    Achievement(
        id="ocean_predators",
        name="Ocean Predators",
        description="Unearth 3 marine reptile predator fossils",
        category="fossil",
        required_items=["mosasaur_scale", "ichthyosaur_tooth", "plesiosaur_vertebra"],
    ),
    Achievement(
        id="ice_age_mammals",
        name="Ice Age Mammals",
        description="Unearth 4 mammalian fossils from the last ice age",
        category="fossil",
        required_items=["sabertooth", "dire_wolf_tooth", "mammoth_molar", "cave_bear_claw"],
    ),

    # -------- gem (5)
    Achievement(
        id="emerald_path",
        name="Emerald Path",
        description="Cut 3 members of the green-beryl gem family",
        category="gem",
        required_items=["emerald", "morganite", "hiddenite"],
    ),
    Achievement(
        id="red_gems",
        name="Red Gems",
        description="Cut 5 red-hued gemstones",
        category="gem",
        required_items=["ruby", "garnet", "padparadscha", "red_beryl", "carnelian"],
    ),
    Achievement(
        id="blue_gems",
        name="Blue Gems",
        description="Cut 5 blue-hued gemstones",
        category="gem",
        required_items=["sapphire", "tanzanite", "paraiba", "lapis_lazuli", "sodalite"],
    ),
    Achievement(
        id="carbon_gems",
        name="Carbon Gems",
        description="Cut 4 dark or carbon-rich gemstones",
        category="gem",
        required_items=["diamond", "jet", "obsidian", "onyx"],
    ),
    Achievement(
        id="jewelry_starter",
        name="Jeweler's Starter Tray",
        description="Cut 10 introductory gemstones",
        category="gem",
        required_items=["amber", "garnet", "rose_quartz", "amethyst", "citrine",
                        "topaz", "peridot", "turquoise", "opal", "carnelian"],
    ),

    # -------- fish (5)
    Achievement(
        id="spawning_run",
        name="Spawning Run",
        description="Catch 4 fish during a spawning run",
        category="fish",
        required_items=["salmon", "trout", "steelhead", "brook_trout"],
    ),
    Achievement(
        id="silver_scales",
        name="Silver Scales",
        description="Catch 3 silver-flanked predator fish",
        category="fish",
        required_items=["perch", "walleye", "pike"],
    ),
    Achievement(
        id="amazonian",
        name="Amazonian",
        description="Catch 4 Amazon-river fish",
        category="fish",
        required_items=["arapaima", "piranha", "tambaqui", "electric_eel"],
    ),
    Achievement(
        id="catch_dozen",
        name="A Dozen Fish",
        description="Catch 12 fish species",
        category="fish",
        required_items=["minnow", "perch", "bass", "carp", "bluegill", "walleye",
                        "crappie", "sunfish", "trout", "salmon", "pike", "catfish"],
    ),
    Achievement(
        id="river_basics",
        name="River Basics",
        description="Catch the 4 most common river fish",
        category="fish",
        required_items=["bluegill", "perch", "bass", "carp"],
    ),

    # -------- bird (5)
    Achievement(
        id="owl_house",
        name="Owl House",
        description="Spot all 3 owl species",
        category="bird",
        required_items=["owl", "barn_owl", "snowy_owl"],
    ),
    Achievement(
        id="corvid_council",
        name="Corvid Council",
        description="Spot 4 corvid species",
        category="bird",
        required_items=["crow", "raven", "magpie", "blue_jay"],
    ),
    Achievement(
        id="forest_birds",
        name="Forest Birds",
        description="Spot 4 woodland species",
        category="bird",
        required_items=["woodpecker", "kingfisher", "cedar_waxwing", "mockingbird"],
    ),
    Achievement(
        id="plumage_pageant",
        name="Plumage Pageant",
        description="Spot 4 of the most flamboyantly plumed birds",
        category="bird",
        required_items=["golden_pheasant", "peacock", "mandarin_duck", "quetzal"],
    ),
    Achievement(
        id="open_air_flocks",
        name="Open Air Flocks",
        description="Spot 5 birds of fields and open skies",
        category="bird",
        required_items=["sparrow", "finch", "hummingbird", "swallow", "kookaburra"],
    ),

    # -------- insect (5)
    Achievement(
        id="orange_wings",
        name="Orange Wings",
        description="Catch 4 orange-winged butterflies",
        category="insect",
        required_items=["monarch", "painted_lady", "copper", "orange_tip"],
    ),
    Achievement(
        id="fritillary_set",
        name="Fritillary Set",
        description="Catch 3 fritillaries and kin",
        category="insect",
        required_items=["silver_washed_fritillary", "great_spangled_fritillary", "copper"],
    ),
    Achievement(
        id="amazon_jungle_bugs",
        name="Amazon Jungle Bugs",
        description="Catch 5 stunning Amazonian butterflies",
        category="insect",
        required_items=["blue_morpho", "zebra_longwing", "postman_butterfly", "malachite_butterfly", "eighty_eight"],
    ),
    Achievement(
        id="catch_ten_bugs",
        name="Catch Ten",
        description="Catch 10 insect species",
        category="insect",
        required_items=["monarch", "swallowtail", "blue_morpho", "painted_lady", "cabbage_white",
                        "ladybug", "stag_beetle", "copper", "red_admiral", "orange_tip"],
    ),
    Achievement(
        id="white_wings",
        name="White Wings",
        description="Catch 4 white-winged butterflies",
        category="insect",
        required_items=["cabbage_white", "white_admiral", "marbled_white", "orange_tip"],
    ),

    # -------- shell (5)
    Achievement(
        id="tropical_shells",
        name="Tropical Shells",
        description="Find 4 warm-water shell specimens",
        category="shell",
        required_items=["tiger_cowrie", "golden_cowrie", "junonia", "harp"],
    ),
    Achievement(
        id="tiny_shells",
        name="Tiny Shells",
        description="Find 4 small intertidal shells",
        category="shell",
        required_items=["periwinkle", "limpet", "top_shell", "nerite"],
    ),
    Achievement(
        id="mussel_collection",
        name="Mussel Collection",
        description="Find 5 mussel and clinging-bivalve shells",
        category="shell",
        required_items=["blue_mussel", "clam", "oyster", "ark_shell", "jingle_shell"],
    ),
    Achievement(
        id="snail_shells",
        name="Snail Shells",
        description="Find 5 sea-snail shell varieties",
        category="shell",
        required_items=["moon_snail", "olive", "auger", "nassa", "violet_snail"],
    ),
    Achievement(
        id="shell_apprentice",
        name="Shell Apprentice",
        description="Find 10 shells along the shore",
        category="shell",
        required_items=["cowrie", "scallop", "clam", "limpet", "whelk",
                        "moon_snail", "cockle", "auger", "blue_mussel", "oyster"],
    ),

    # -------- hunt (5)
    Achievement(
        id="antlered_collection",
        name="Antlered Collection",
        description="Hunt 4 antlered or horned species",
        category="hunt",
        required_items=["deer", "elk", "moose", "bighorn"],
    ),
    Achievement(
        id="arctic_hunts",
        name="Arctic Hunts",
        description="Hunt 3 species adapted to the far north",
        category="hunt",
        required_items=["arctic_fox", "musk_ox", "moose"],
    ),
    Achievement(
        id="canine_hunts",
        name="Canine Hunts",
        description="Hunt the 3 wild canines",
        category="hunt",
        required_items=["wolf", "fox", "arctic_fox"],
    ),
    Achievement(
        id="tropical_hunts",
        name="Tropical Hunts",
        description="Hunt 3 species of hot climates",
        category="hunt",
        required_items=["crocodile", "warthog", "capybara"],
    ),
    Achievement(
        id="bovine_hunts",
        name="Bovine Hunts",
        description="Hunt both wild bovines",
        category="hunt",
        required_items=["bison", "musk_ox"],
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
