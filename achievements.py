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
