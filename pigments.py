import hashlib
import random as _rnd
from dataclasses import dataclass, field


@dataclass
class Pigment:
    uid: str
    pigment_key: str        # e.g. "ultramarine", "carmine"
    source_type: str        # "mineral" | "plant" | "earth" | "insect" | "animal" | "processed"
    origin_biome: str
    state: str              # "raw" | "ground" | "refined"
    color_family: str       # "blue" | "red" | "yellow" | "green" | "dark" | "earth"
    purity: float           # 0.0–1.0  saturation/richness of color
    opacity: float          # 0.0–1.0  covering power
    stability: float        # 0.0–1.0  lightfastness
    granularity: float      # 0.0–1.0  particle size (high = coarse)
    grind_quality: float    # 0.0–1.0  set by mill mini-game
    color_rgb: list         # [R, G, B]
    notes: list             # 2–3 descriptive strings
    seed: int
    blend_components: list = field(default_factory=list)

    def quality(self) -> float:
        return round(
            self.purity * 0.35 + self.opacity * 0.25 +
            self.stability * 0.25 + self.grind_quality * 0.15, 3
        )


PIGMENT_TYPES = {
    # ── BLUE ────────────────────────────────────────────────────────────
    "ultramarine": {
        "display": "Ultramarine",
        "family": "blue",
        "source_type": "mineral",
        "base_rgb": (20, 40, 165),
        "rarity": "rare",
        "biome_affinity": ["canyon", "rocky_mountain"],
        "base_attrs": {"purity": 0.75, "opacity": 0.85, "stability": 0.90, "granularity": 0.45},
        "notes_pool": ["Deep blue", "Warm undertone", "Dense coverage", "Lapis origin", "Prized since antiquity"],
    },
    "azurite": {
        "display": "Azurite",
        "family": "blue",
        "source_type": "mineral",
        "base_rgb": (50, 105, 195),
        "rarity": "uncommon",
        "biome_affinity": ["canyon", "desert"],
        "base_attrs": {"purity": 0.65, "opacity": 0.70, "stability": 0.65, "granularity": 0.55},
        "notes_pool": ["Bright cyan-blue", "Mineral origin", "Unstable over time", "Copper-based"],
    },
    "smalt": {
        "display": "Smalt",
        "family": "blue",
        "source_type": "mineral",
        "base_rgb": (45, 80, 175),
        "rarity": "uncommon",
        "biome_affinity": ["alpine_mountain"],
        "base_attrs": {"purity": 0.60, "opacity": 0.75, "stability": 0.70, "granularity": 0.65},
        "notes_pool": ["Cool blue", "Glassy texture", "Cobalt origin", "Coarse grind best"],
    },
    "indigo": {
        "display": "Indigo",
        "family": "blue",
        "source_type": "plant",
        "base_rgb": (55, 35, 130),
        "rarity": "common",
        "biome_affinity": ["tropical", "jungle"],
        "base_attrs": {"purity": 0.70, "opacity": 0.60, "stability": 0.80, "granularity": 0.35},
        "notes_pool": ["Deep violet-blue", "Vat dye", "Cloth affinity", "Tropical origin"],
    },
    "woad": {
        "display": "Woad",
        "family": "blue",
        "source_type": "plant",
        "base_rgb": (70, 90, 160),
        "rarity": "common",
        "biome_affinity": ["temperate", "rolling_hills"],
        "base_attrs": {"purity": 0.50, "opacity": 0.55, "stability": 0.70, "granularity": 0.30},
        "notes_pool": ["Muted blue", "Ancient dye", "Mild tone", "Pasture herb"],
    },
    "cerulean": {
        "display": "Cerulean Earth",
        "family": "blue",
        "source_type": "earth",
        "base_rgb": (95, 165, 215),
        "rarity": "uncommon",
        "biome_affinity": ["beach", "wetland"],
        "base_attrs": {"purity": 0.55, "opacity": 0.65, "stability": 0.75, "granularity": 0.50},
        "notes_pool": ["Sky blue", "Sandy undertone", "Coastal deposit", "Light opacity"],
    },
    # ── RED ─────────────────────────────────────────────────────────────
    "vermillion": {
        "display": "Vermillion",
        "family": "red",
        "source_type": "mineral",
        "base_rgb": (215, 40, 25),
        "rarity": "rare",
        "biome_affinity": ["canyon", "swamp"],
        "base_attrs": {"purity": 0.85, "opacity": 0.95, "stability": 0.80, "granularity": 0.40},
        "notes_pool": ["Pure scarlet", "Cinnabar origin", "Dense coverage", "Brilliant red"],
    },
    "madder_lake": {
        "display": "Madder Lake",
        "family": "red",
        "source_type": "plant",
        "base_rgb": (185, 50, 80),
        "rarity": "common",
        "biome_affinity": ["mediterranean", "temperate"],
        "base_attrs": {"purity": 0.65, "opacity": 0.60, "stability": 0.70, "granularity": 0.30},
        "notes_pool": ["Rose-red", "Root extract", "Warm hue", "Fugitive in light"],
    },
    "carmine": {
        "display": "Carmine",
        "family": "red",
        "source_type": "insect",
        "base_rgb": (165, 15, 50),
        "rarity": "rare",
        "biome_affinity": ["tropical", "savanna"],
        "base_attrs": {"purity": 0.90, "opacity": 0.80, "stability": 0.85, "granularity": 0.20},
        "notes_pool": ["Deep crimson", "Insect extract", "Intense saturation", "Lake pigment"],
    },
    "red_ochre": {
        "display": "Red Ochre",
        "family": "red",
        "source_type": "earth",
        "base_rgb": (185, 75, 40),
        "rarity": "common",
        "biome_affinity": ["savanna", "steppe"],
        "base_attrs": {"purity": 0.55, "opacity": 0.85, "stability": 0.95, "granularity": 0.60},
        "notes_pool": ["Warm earth red", "Iron oxide", "Durable", "Cave art origin"],
    },
    "kermes": {
        "display": "Kermes",
        "family": "red",
        "source_type": "insect",
        "base_rgb": (190, 35, 60),
        "rarity": "rare",
        "biome_affinity": ["mediterranean"],
        "base_attrs": {"purity": 0.80, "opacity": 0.75, "stability": 0.75, "granularity": 0.25},
        "notes_pool": ["Scarlet red", "Oak insect", "Medieval dye", "Warm crimson"],
    },
    "dragon_blood": {
        "display": "Dragon's Blood",
        "family": "red",
        "source_type": "plant",
        "base_rgb": (185, 20, 30),
        "rarity": "rare",
        "biome_affinity": ["tropical"],
        "base_attrs": {"purity": 0.80, "opacity": 0.70, "stability": 0.65, "granularity": 0.25},
        "notes_pool": ["Deep red resin", "Exotic origin", "Varnish quality", "Tropical tree"],
    },
    # ── YELLOW ──────────────────────────────────────────────────────────
    "orpiment": {
        "display": "Orpiment",
        "family": "yellow",
        "source_type": "mineral",
        "base_rgb": (225, 185, 20),
        "rarity": "uncommon",
        "biome_affinity": ["canyon", "wasteland"],
        "base_attrs": {"purity": 0.80, "opacity": 0.75, "stability": 0.50, "granularity": 0.45},
        "notes_pool": ["Bright gold-yellow", "Arsenic-based", "Toxic origin", "Vivid but unstable"],
    },
    "naples_yellow": {
        "display": "Naples Yellow",
        "family": "yellow",
        "source_type": "mineral",
        "base_rgb": (255, 215, 100),
        "rarity": "uncommon",
        "biome_affinity": ["desert", "rocky_mountain"],
        "base_attrs": {"purity": 0.70, "opacity": 0.85, "stability": 0.90, "granularity": 0.40},
        "notes_pool": ["Warm pale yellow", "Lead-antimony", "Dense coverage", "Opaque"],
    },
    "saffron": {
        "display": "Saffron Yellow",
        "family": "yellow",
        "source_type": "plant",
        "base_rgb": (255, 195, 15),
        "rarity": "rare",
        "biome_affinity": ["mediterranean", "east_asian"],
        "base_attrs": {"purity": 0.85, "opacity": 0.55, "stability": 0.60, "granularity": 0.15},
        "notes_pool": ["Pure gold-yellow", "Precious spice", "Transparent wash", "Luminous"],
    },
    "weld_yellow": {
        "display": "Weld Yellow",
        "family": "yellow",
        "source_type": "plant",
        "base_rgb": (210, 200, 60),
        "rarity": "common",
        "biome_affinity": ["rolling_hills", "steppe"],
        "base_attrs": {"purity": 0.60, "opacity": 0.50, "stability": 0.65, "granularity": 0.25},
        "notes_pool": ["Warm lime-yellow", "Lake dye", "Meadow herb", "Bright but fugitive"],
    },
    "gamboge": {
        "display": "Gamboge",
        "family": "yellow",
        "source_type": "plant",
        "base_rgb": (225, 160, 10),
        "rarity": "rare",
        "biome_affinity": ["jungle"],
        "base_attrs": {"purity": 0.85, "opacity": 0.65, "stability": 0.60, "granularity": 0.20},
        "notes_pool": ["Amber-yellow resin", "Jungle tree sap", "Transparent glaze", "Warm orange tint"],
    },
    "yellow_ochre": {
        "display": "Yellow Ochre",
        "family": "yellow",
        "source_type": "earth",
        "base_rgb": (195, 155, 45),
        "rarity": "common",
        "biome_affinity": ["arid_steppe", "savanna"],
        "base_attrs": {"purity": 0.55, "opacity": 0.90, "stability": 0.95, "granularity": 0.55},
        "notes_pool": ["Earthy gold", "Iron oxide", "Permanent", "Cave art origin"],
    },
    # ── GREEN ────────────────────────────────────────────────────────────
    "viridian": {
        "display": "Viridian",
        "family": "green",
        "source_type": "mineral",
        "base_rgb": (40, 155, 90),
        "rarity": "uncommon",
        "biome_affinity": ["jungle", "wetland"],
        "base_attrs": {"purity": 0.75, "opacity": 0.70, "stability": 0.85, "granularity": 0.40},
        "notes_pool": ["Pure cool green", "Malachite origin", "Transparent layers", "Vivid tone"],
    },
    "verdigris": {
        "display": "Verdigris",
        "family": "green",
        "source_type": "mineral",
        "base_rgb": (65, 165, 140),
        "rarity": "uncommon",
        "biome_affinity": ["rocky_mountain"],
        "base_attrs": {"purity": 0.65, "opacity": 0.65, "stability": 0.55, "granularity": 0.35},
        "notes_pool": ["Teal-green", "Copper patina", "Unstable in oil", "Brilliant but reactive"],
    },
    "terre_verte": {
        "display": "Terre Verte",
        "family": "green",
        "source_type": "earth",
        "base_rgb": (110, 145, 100),
        "rarity": "common",
        "biome_affinity": ["temperate", "rolling_hills"],
        "base_attrs": {"purity": 0.45, "opacity": 0.60, "stability": 0.90, "granularity": 0.50},
        "notes_pool": ["Muted olive green", "Earth mineral", "Fresco base", "Durable wash"],
    },
    "sap_green": {
        "display": "Sap Green",
        "family": "green",
        "source_type": "plant",
        "base_rgb": (75, 140, 65),
        "rarity": "common",
        "biome_affinity": ["temperate"],
        "base_attrs": {"purity": 0.60, "opacity": 0.50, "stability": 0.55, "granularity": 0.20},
        "notes_pool": ["Fresh leaf green", "Plant extract", "Transparent", "Fugitive over time"],
    },
    "emerald_green": {
        "display": "Emerald Green",
        "family": "green",
        "source_type": "mineral",
        "base_rgb": (10, 175, 80),
        "rarity": "rare",
        "biome_affinity": ["alpine_mountain"],
        "base_attrs": {"purity": 0.90, "opacity": 0.80, "stability": 0.75, "granularity": 0.30},
        "notes_pool": ["Brilliant emerald", "Chrome origin", "Vivid saturation", "Alpine mineral"],
    },
    "verona_green": {
        "display": "Verona Green",
        "family": "green",
        "source_type": "earth",
        "base_rgb": (100, 135, 90),
        "rarity": "uncommon",
        "biome_affinity": ["canyon", "rocky_mountain"],
        "base_attrs": {"purity": 0.50, "opacity": 0.70, "stability": 0.85, "granularity": 0.55},
        "notes_pool": ["Greyish green", "Stone deposit", "Muted tone", "Medieval use"],
    },
    # ── DARK ─────────────────────────────────────────────────────────────
    "bone_black": {
        "display": "Bone Black",
        "family": "dark",
        "source_type": "animal",
        "base_rgb": (25, 20, 30),
        "rarity": "common",
        "biome_affinity": [],
        "base_attrs": {"purity": 0.70, "opacity": 0.90, "stability": 0.95, "granularity": 0.45},
        "notes_pool": ["Deep charcoal black", "Calcined bone", "Warm undertone", "Dense ink"],
    },
    "ivory_black": {
        "display": "Ivory Black",
        "family": "dark",
        "source_type": "animal",
        "base_rgb": (30, 25, 25),
        "rarity": "uncommon",
        "biome_affinity": ["savanna", "jungle"],
        "base_attrs": {"purity": 0.80, "opacity": 0.85, "stability": 0.95, "granularity": 0.35},
        "notes_pool": ["Warm black", "Ivory char", "Smooth grind", "Rich depth"],
    },
    "sepia": {
        "display": "Sepia",
        "family": "dark",
        "source_type": "animal",
        "base_rgb": (85, 55, 35),
        "rarity": "uncommon",
        "biome_affinity": ["ocean", "beach"],
        "base_attrs": {"purity": 0.65, "opacity": 0.70, "stability": 0.80, "granularity": 0.20},
        "notes_pool": ["Warm brown-black", "Cuttlefish ink", "Smooth wash", "Sea origin"],
    },
    "carbon_black": {
        "display": "Carbon Black",
        "family": "dark",
        "source_type": "earth",
        "base_rgb": (20, 18, 20),
        "rarity": "common",
        "biome_affinity": [],
        "base_attrs": {"purity": 0.75, "opacity": 0.95, "stability": 0.95, "granularity": 0.30},
        "notes_pool": ["Pure black", "Coal origin", "Dense", "Neutral tone"],
    },
    "van_dyck_brown": {
        "display": "Van Dyck Brown",
        "family": "dark",
        "source_type": "earth",
        "base_rgb": (70, 40, 25),
        "rarity": "uncommon",
        "biome_affinity": ["swamp", "boreal"],
        "base_attrs": {"purity": 0.60, "opacity": 0.75, "stability": 0.80, "granularity": 0.45},
        "notes_pool": ["Dark warm brown", "Lignite deposit", "Rich shadow tone", "Peat origin"],
    },
    "umber": {
        "display": "Raw Umber",
        "family": "dark",
        "source_type": "earth",
        "base_rgb": (120, 85, 45),
        "rarity": "common",
        "biome_affinity": ["rocky_mountain", "canyon"],
        "base_attrs": {"purity": 0.55, "opacity": 0.85, "stability": 0.95, "granularity": 0.60},
        "notes_pool": ["Cool brown", "Manganese oxide", "Drying agent", "Old masters staple"],
    },
    # ── EARTH/WARM ───────────────────────────────────────────────────────
    "raw_sienna": {
        "display": "Raw Sienna",
        "family": "earth",
        "source_type": "earth",
        "base_rgb": (180, 120, 50),
        "rarity": "common",
        "biome_affinity": ["arid_steppe", "desert"],
        "base_attrs": {"purity": 0.55, "opacity": 0.80, "stability": 0.95, "granularity": 0.60},
        "notes_pool": ["Warm golden-brown", "Transparent base", "Iron-rich clay", "Tuscany earth"],
    },
    "burnt_sienna": {
        "display": "Burnt Sienna",
        "family": "earth",
        "source_type": "processed",
        "base_rgb": (165, 75, 35),
        "rarity": "uncommon",
        "biome_affinity": [],
        "base_attrs": {"purity": 0.70, "opacity": 0.80, "stability": 0.95, "granularity": 0.50},
        "notes_pool": ["Rich reddish-brown", "Calcined sienna", "Intense tone", "Warm shadow"],
    },
    "burnt_umber": {
        "display": "Burnt Umber",
        "family": "earth",
        "source_type": "processed",
        "base_rgb": (100, 55, 25),
        "rarity": "uncommon",
        "biome_affinity": [],
        "base_attrs": {"purity": 0.65, "opacity": 0.85, "stability": 0.95, "granularity": 0.50},
        "notes_pool": ["Dark warm brown", "Calcined umber", "Drying pigment", "Deep shadow"],
    },
    "tyrian_purple": {
        "display": "Tyrian Purple",
        "family": "earth",
        "source_type": "animal",
        "base_rgb": (100, 30, 90),
        "rarity": "legendary",
        "biome_affinity": ["ocean", "beach"],
        "base_attrs": {"purity": 0.95, "opacity": 0.80, "stability": 0.90, "granularity": 0.15},
        "notes_pool": ["Royal purple", "Murex snail", "Rarest pigment", "Imperial color"],
    },
    "lead_white": {
        "display": "Lead White",
        "family": "earth",
        "source_type": "mineral",
        "base_rgb": (240, 238, 232),
        "rarity": "uncommon",
        "biome_affinity": ["rocky_mountain"],
        "base_attrs": {"purity": 0.85, "opacity": 0.95, "stability": 0.85, "granularity": 0.30},
        "notes_pool": ["Warm bright white", "Lead-based", "Dense coverage", "Old masters white"],
    },
    "chalk_white": {
        "display": "Chalk White",
        "family": "earth",
        "source_type": "earth",
        "base_rgb": (245, 244, 238),
        "rarity": "common",
        "biome_affinity": ["beach", "tundra"],
        "base_attrs": {"purity": 0.65, "opacity": 0.75, "stability": 0.90, "granularity": 0.40},
        "notes_pool": ["Pure cool white", "Calcium carbonate", "Ground base", "Fresco ground"],
    },
    # ── BLUE (extended) ──────────────────────────────────────────────────
    "prussian_blue": {
        "display": "Prussian Blue",
        "family": "blue",
        "source_type": "mineral",
        "base_rgb": (15, 50, 130),
        "rarity": "uncommon",
        "biome_affinity": ["rocky_mountain", "boreal"],
        "base_attrs": {"purity": 0.80, "opacity": 0.90, "stability": 0.85, "granularity": 0.25},
        "notes_pool": ["Deep cool blue", "Iron-cyanide", "Dense tinting power", "Watercolour staple"],
    },
    "egyptian_blue": {
        "display": "Egyptian Blue",
        "family": "blue",
        "source_type": "mineral",
        "base_rgb": (35, 110, 175),
        "rarity": "rare",
        "biome_affinity": ["desert", "canyon"],
        "base_attrs": {"purity": 0.75, "opacity": 0.80, "stability": 0.95, "granularity": 0.50},
        "notes_pool": ["Ancient synthetic", "Copper-calcium silicate", "Turquoise blue", "Millennia-old formula"],
    },
    "cobalt_blue": {
        "display": "Cobalt Blue",
        "family": "blue",
        "source_type": "mineral",
        "base_rgb": (30, 75, 195),
        "rarity": "uncommon",
        "biome_affinity": ["alpine_mountain"],
        "base_attrs": {"purity": 0.85, "opacity": 0.75, "stability": 0.95, "granularity": 0.30},
        "notes_pool": ["Pure sky blue", "Cobalt aluminate", "Cool and clean", "Porcelain glaze origin"],
    },
    "maya_blue": {
        "display": "Maya Blue",
        "family": "blue",
        "source_type": "earth",
        "base_rgb": (55, 140, 195),
        "rarity": "rare",
        "biome_affinity": ["tropical", "jungle"],
        "base_attrs": {"purity": 0.70, "opacity": 0.65, "stability": 0.90, "granularity": 0.45},
        "notes_pool": ["Vivid turquoise-blue", "Clay-indigo composite", "Mesoamerican origin", "Remarkably durable"],
    },
    # ── RED (extended) ────────────────────────────────────────────────────
    "minium": {
        "display": "Minium",
        "family": "red",
        "source_type": "mineral",
        "base_rgb": (220, 70, 20),
        "rarity": "uncommon",
        "biome_affinity": ["rocky_mountain"],
        "base_attrs": {"purity": 0.75, "opacity": 0.90, "stability": 0.70, "granularity": 0.40},
        "notes_pool": ["Vivid orange-red", "Lead tetroxide", "Manuscript orange", "Toxic but brilliant"],
    },
    "rose_madder": {
        "display": "Rose Madder",
        "family": "red",
        "source_type": "processed",
        "base_rgb": (215, 90, 110),
        "rarity": "uncommon",
        "biome_affinity": [],
        "base_attrs": {"purity": 0.70, "opacity": 0.50, "stability": 0.60, "granularity": 0.20},
        "notes_pool": ["Pale cool rose", "Refined madder", "Transparent glaze", "Fugitive in light"],
    },
    "brazilwood_lake": {
        "display": "Brazilwood Lake",
        "family": "red",
        "source_type": "plant",
        "base_rgb": (175, 25, 55),
        "rarity": "rare",
        "biome_affinity": ["tropical", "jungle"],
        "base_attrs": {"purity": 0.75, "opacity": 0.60, "stability": 0.55, "granularity": 0.20},
        "notes_pool": ["Deep crimson lake", "Tropical hardwood", "Fugitive red", "Rich transparent wash"],
    },
    "realgar_red": {
        "display": "Realgar Red",
        "family": "red",
        "source_type": "mineral",
        "base_rgb": (200, 80, 20),
        "rarity": "uncommon",
        "biome_affinity": ["canyon", "wasteland"],
        "base_attrs": {"purity": 0.70, "opacity": 0.80, "stability": 0.50, "granularity": 0.50},
        "notes_pool": ["Orange-red", "Arsenic sulfide", "Unstable in air", "Pairs with orpiment"],
    },
    "lac_lake": {
        "display": "Lac Lake",
        "family": "red",
        "source_type": "insect",
        "base_rgb": (155, 20, 45),
        "rarity": "rare",
        "biome_affinity": ["tropical", "east_asian"],
        "base_attrs": {"purity": 0.85, "opacity": 0.65, "stability": 0.70, "granularity": 0.20},
        "notes_pool": ["Dark rich crimson", "Lac insect resin", "Shellac origin", "Asian dyestuff"],
    },
    # ── YELLOW (extended) ─────────────────────────────────────────────────
    "indian_yellow": {
        "display": "Indian Yellow",
        "family": "yellow",
        "source_type": "animal",
        "base_rgb": (240, 180, 20),
        "rarity": "rare",
        "biome_affinity": ["tropical", "east_asian"],
        "base_attrs": {"purity": 0.90, "opacity": 0.55, "stability": 0.65, "granularity": 0.15},
        "notes_pool": ["Luminous warm gold", "Animal extract", "Transparent wash", "Prized in miniatures"],
    },
    "massicot": {
        "display": "Massicot",
        "family": "yellow",
        "source_type": "mineral",
        "base_rgb": (240, 225, 120),
        "rarity": "uncommon",
        "biome_affinity": ["rocky_mountain", "desert"],
        "base_attrs": {"purity": 0.65, "opacity": 0.80, "stability": 0.75, "granularity": 0.35},
        "notes_pool": ["Pale straw yellow", "Lead monoxide", "Soft warm tone", "Medieval use"],
    },
    "stil_de_grain": {
        "display": "Stil de Grain",
        "family": "yellow",
        "source_type": "plant",
        "base_rgb": (205, 195, 50),
        "rarity": "uncommon",
        "biome_affinity": ["rolling_hills", "temperate"],
        "base_attrs": {"purity": 0.65, "opacity": 0.45, "stability": 0.55, "granularity": 0.20},
        "notes_pool": ["Green-yellow lake", "Buckthorn berries", "Transparent glaze", "Fugitive but beautiful"],
    },
    "chrome_yellow": {
        "display": "Chrome Yellow",
        "family": "yellow",
        "source_type": "mineral",
        "base_rgb": (255, 215, 10),
        "rarity": "uncommon",
        "biome_affinity": ["rocky_mountain"],
        "base_attrs": {"purity": 0.85, "opacity": 0.90, "stability": 0.80, "granularity": 0.30},
        "notes_pool": ["Brilliant lemon-yellow", "Lead chromate", "High coverage", "Van Gogh favourite"],
    },
    # ── GREEN (extended) ──────────────────────────────────────────────────
    "malachite_green": {
        "display": "Malachite Green",
        "family": "green",
        "source_type": "mineral",
        "base_rgb": (25, 140, 70),
        "rarity": "uncommon",
        "biome_affinity": ["jungle", "wetland"],
        "base_attrs": {"purity": 0.70, "opacity": 0.75, "stability": 0.70, "granularity": 0.55},
        "notes_pool": ["Warm bright green", "Ground malachite", "Ancient mineral", "Coarse texture"],
    },
    "schweinfurt_green": {
        "display": "Schweinfurt Green",
        "family": "green",
        "source_type": "mineral",
        "base_rgb": (0, 200, 90),
        "rarity": "rare",
        "biome_affinity": ["rocky_mountain"],
        "base_attrs": {"purity": 0.95, "opacity": 0.85, "stability": 0.60, "granularity": 0.30},
        "notes_pool": ["Vivid emerald", "Copper arsenite", "Highly toxic", "Brilliant but dangerous"],
    },
    "chromium_oxide_green": {
        "display": "Chromium Oxide",
        "family": "green",
        "source_type": "mineral",
        "base_rgb": (75, 130, 70),
        "rarity": "uncommon",
        "biome_affinity": ["alpine_mountain"],
        "base_attrs": {"purity": 0.65, "opacity": 0.85, "stability": 0.98, "granularity": 0.45},
        "notes_pool": ["Muted army green", "Chromium ore", "Extremely durable", "Opaque and solid"],
    },
    "brunswick_green": {
        "display": "Brunswick Green",
        "family": "green",
        "source_type": "earth",
        "base_rgb": (45, 100, 60),
        "rarity": "common",
        "biome_affinity": ["boreal", "temperate"],
        "base_attrs": {"purity": 0.50, "opacity": 0.75, "stability": 0.85, "granularity": 0.55},
        "notes_pool": ["Deep forest green", "Iron earth deposit", "Durable tone", "Dark shadow green"],
    },
    # ── DARK (extended) ───────────────────────────────────────────────────
    "lamp_black": {
        "display": "Lamp Black",
        "family": "dark",
        "source_type": "animal",
        "base_rgb": (18, 15, 18),
        "rarity": "common",
        "biome_affinity": [],
        "base_attrs": {"purity": 0.80, "opacity": 0.95, "stability": 0.95, "granularity": 0.15},
        "notes_pool": ["Finest black soot", "Oil lamp deposit", "Smooth and velvety", "Pure carbon"],
    },
    "vine_black": {
        "display": "Vine Black",
        "family": "dark",
        "source_type": "plant",
        "base_rgb": (22, 20, 28),
        "rarity": "common",
        "biome_affinity": ["temperate", "mediterranean"],
        "base_attrs": {"purity": 0.75, "opacity": 0.88, "stability": 0.90, "granularity": 0.25},
        "notes_pool": ["Cool blue-black", "Charred vine stems", "Ink quality", "Soft tone"],
    },
    "bistre": {
        "display": "Bistre",
        "family": "dark",
        "source_type": "animal",
        "base_rgb": (75, 50, 30),
        "rarity": "common",
        "biome_affinity": ["boreal", "temperate"],
        "base_attrs": {"purity": 0.55, "opacity": 0.65, "stability": 0.75, "granularity": 0.20},
        "notes_pool": ["Warm brown-black", "Wood soot extract", "Transparent wash", "Sketch medium"],
    },
    "mummy_brown": {
        "display": "Mummy Brown",
        "family": "dark",
        "source_type": "earth",
        "base_rgb": (55, 35, 20),
        "rarity": "rare",
        "biome_affinity": ["desert", "canyon"],
        "base_attrs": {"purity": 0.60, "opacity": 0.70, "stability": 0.80, "granularity": 0.30},
        "notes_pool": ["Ancient brown", "Bituminous earth", "Translucent depth", "Desert origin"],
    },
    # ── EARTH/WARM (extended) ─────────────────────────────────────────────
    "caput_mortuum": {
        "display": "Caput Mortuum",
        "family": "earth",
        "source_type": "mineral",
        "base_rgb": (100, 40, 70),
        "rarity": "uncommon",
        "biome_affinity": ["rocky_mountain", "canyon"],
        "base_attrs": {"purity": 0.65, "opacity": 0.85, "stability": 0.95, "granularity": 0.50},
        "notes_pool": ["Deep violet-brown", "Iron oxide calcinate", "Durable shadow", "Alchemist's waste"],
    },
    "terra_rosa": {
        "display": "Terra Rosa",
        "family": "earth",
        "source_type": "earth",
        "base_rgb": (175, 90, 85),
        "rarity": "common",
        "biome_affinity": ["mediterranean", "canyon"],
        "base_attrs": {"purity": 0.55, "opacity": 0.80, "stability": 0.95, "granularity": 0.55},
        "notes_pool": ["Cool rose-red earth", "Clay deposit", "Durable pink tone", "Mediterranean clay"],
    },
    "pozzuoli_red": {
        "display": "Pozzuoli Red",
        "family": "earth",
        "source_type": "earth",
        "base_rgb": (185, 95, 70),
        "rarity": "uncommon",
        "biome_affinity": ["any"],
        "base_attrs": {"purity": 0.60, "opacity": 0.80, "stability": 0.90, "granularity": 0.50},
        "notes_pool": ["Warm volcanic red", "Volcanic earth", "Ancient fresco use", "Pozzuoli deposit"],
    },
    "ochre_violet": {
        "display": "Ochre Violet",
        "family": "earth",
        "source_type": "earth",
        "base_rgb": (150, 100, 130),
        "rarity": "uncommon",
        "biome_affinity": ["steppe", "arid_steppe"],
        "base_attrs": {"purity": 0.55, "opacity": 0.75, "stability": 0.90, "granularity": 0.55},
        "notes_pool": ["Dusty violet-earth", "Manganese ochre", "Muted purple tone", "Steppe deposit"],
    },
}

# Codex grid order — 6 colour families × 6 types
PIGMENT_FAMILY_ORDER = ["blue", "red", "yellow", "green", "dark", "earth"]
PIGMENT_TYPE_ORDER = [
    k for fam in PIGMENT_FAMILY_ORDER
    for k, v in PIGMENT_TYPES.items() if v["family"] == fam
]

PIGMENT_DISPLAY_NAMES = {k: v["display"] for k, v in PIGMENT_TYPES.items()}

# Source groups for UI filtering
PIGMENT_SOURCE_GROUPS = {
    "mineral":   [k for k, v in PIGMENT_TYPES.items() if v["source_type"] == "mineral"],
    "plant":     [k for k, v in PIGMENT_TYPES.items() if v["source_type"] == "plant"],
    "earth":     [k for k, v in PIGMENT_TYPES.items() if v["source_type"] == "earth"],
    "insect":    [k for k, v in PIGMENT_TYPES.items() if v["source_type"] == "insect"],
    "animal":    [k for k, v in PIGMENT_TYPES.items() if v["source_type"] == "animal"],
    "processed": [k for k, v in PIGMENT_TYPES.items() if v["source_type"] == "processed"],
}

# Raw material → pigment key (used by Pigment Mill)
RAW_TO_PIGMENT = {
    "raw_lapis":       "ultramarine",
    "raw_azurite":     "azurite",
    "raw_cobalt_ore":  "smalt",
    "indigo_harvest":  "indigo",
    "woad_harvest":    "woad",
    "raw_cerulean":    "cerulean",
    "raw_cinnabar":    "vermillion",
    "madder_harvest":  "madder_lake",
    "raw_cochineal":   "carmine",
    "raw_ochre_red":   "red_ochre",
    "raw_kermes":      "kermes",
    "dragon_blood_harvest": "dragon_blood",
    "raw_realgar":     "orpiment",
    "raw_antimony":    "naples_yellow",
    "saffron_harvest": "saffron",
    "weld_harvest":    "weld_yellow",
    "gamboge_harvest": "gamboge",
    "raw_ochre":       "yellow_ochre",
    "raw_malachite":   "viridian",
    "raw_copper_ore":  "verdigris",
    "raw_terre_verte": "terre_verte",
    "raw_sap_plant":   "sap_green",
    "raw_chrome_ore":  "emerald_green",
    "raw_verona":      "verona_green",
    "raw_bone":        "bone_black",
    "raw_ivory":       "ivory_black",
    "raw_cuttlefish":  "sepia",
    "raw_coal_dust":   "carbon_black",
    "raw_lignite":     "van_dyck_brown",
    "raw_umber":       "umber",
    "raw_sienna":      "raw_sienna",
    "raw_murex":       "tyrian_purple",
    "raw_galena":           "lead_white",
    "raw_chalk":            "chalk_white",
    # ── Extended pigments ─────────────────────────────────────────────
    "raw_prussian":         "prussian_blue",
    "raw_egyptian_blue":    "egyptian_blue",
    "raw_cobalt_blue":      "cobalt_blue",
    "raw_palygorskite":     "maya_blue",
    "raw_minium":           "minium",
    "raw_brazilwood":       "brazilwood_lake",
    "raw_realgar_chunk":    "realgar_red",
    "raw_lac_insect":       "lac_lake",
    "raw_indian_yellow":    "indian_yellow",
    "raw_massicot":         "massicot",
    "raw_buckthorn":        "stil_de_grain",
    "raw_chromate":         "chrome_yellow",
    "raw_malachite_chunk":  "malachite_green",
    "raw_copper_arsenite":  "schweinfurt_green",
    "raw_chromium":         "chromium_oxide_green",
    "raw_brunswick_clay":   "brunswick_green",
    "raw_lamp_soot":        "lamp_black",
    "raw_vine_char":        "vine_black",
    "raw_wood_soot":        "bistre",
    "raw_asphaltum":        "mummy_brown",
    "raw_caput":            "caput_mortuum",
    "raw_terra_rosa":       "terra_rosa",
    "raw_volcanic_red":     "pozzuoli_red",
    "raw_violet_ochre":     "ochre_violet",
}

# Pigments that can be calcined (heated) to produce a different pigment
CALCINATION_MAP = {
    "raw_sienna":   "burnt_sienna",
    "umber":        "burnt_umber",
    "madder_lake":  "rose_madder",
}

# Processing options for the mill
GRIND_STYLES = {
    "coarse": {
        "label": "Coarse Grind",
        "desc": "Quick rough grind. Lower purity, coarser texture.",
        "granularity": +0.30,
        "purity": -0.05,
        "grind_quality_mult": 0.80,
    },
    "standard": {
        "label": "Standard Grind",
        "desc": "Balanced grind. Good all-around result.",
        "granularity": 0.00,
        "purity": 0.00,
        "grind_quality_mult": 1.00,
    },
    "fine": {
        "label": "Fine Grind",
        "desc": "Slow fine grind. Higher purity, smoother texture.",
        "granularity": -0.25,
        "purity": +0.10,
        "grind_quality_mult": 1.20,
    },
}

GRIND_STYLE_ORDER = ["coarse", "standard", "fine"]


class PigmentGenerator:
    def __init__(self, world_seed: int):
        self._world_seed = world_seed
        self._counter = 0

    def generate(self, pigment_key: str, origin_biome: str) -> Pigment:
        self._counter += 1
        seed = (self._world_seed * 31 + self._counter * 7919) & 0xFFFFFFFF
        uid = hashlib.md5(f"pigment_{seed}_{self._counter}".encode()).hexdigest()[:12]
        rng = _rnd.Random(seed)

        ptype = PIGMENT_TYPES.get(pigment_key, PIGMENT_TYPES["yellow_ochre"])
        base = ptype["base_attrs"]

        def _jitter(v):
            return max(0.0, min(1.0, v + rng.gauss(0, 0.06)))

        purity = _jitter(base["purity"])
        opacity = _jitter(base["opacity"])
        stability = _jitter(base["stability"])
        granularity = _jitter(base["granularity"])

        # Color varies slightly with purity
        br, bg, bb = ptype["base_rgb"]
        variance = int((purity - 0.5) * 30)
        color_rgb = [
            max(0, min(255, br + rng.randint(-8, 8) + variance)),
            max(0, min(255, bg + rng.randint(-8, 8) + variance)),
            max(0, min(255, bb + rng.randint(-8, 8) + variance)),
        ]

        pool = ptype["notes_pool"]
        notes = rng.sample(pool, min(2, len(pool)))

        return Pigment(
            uid=uid,
            pigment_key=pigment_key,
            source_type=ptype["source_type"],
            origin_biome=origin_biome,
            state="raw",
            color_family=ptype["family"],
            purity=round(purity, 3),
            opacity=round(opacity, 3),
            stability=round(stability, 3),
            granularity=round(granularity, 3),
            grind_quality=0.0,
            color_rgb=color_rgb,
            notes=notes,
            seed=seed,
        )

    def generate_processed(self, source: Pigment, new_key: str) -> Pigment:
        """Create a calcined/processed variant from an existing pigment."""
        self._counter += 1
        seed = (self._world_seed * 53 + self._counter * 6143) & 0xFFFFFFFF
        uid = hashlib.md5(f"pigment_proc_{seed}_{self._counter}".encode()).hexdigest()[:12]
        rng = _rnd.Random(seed)

        ptype = PIGMENT_TYPES[new_key]
        base = ptype["base_attrs"]

        def _jitter(v, boost=0.05):
            return max(0.0, min(1.0, v + rng.gauss(boost, 0.04)))

        # Calcination improves purity and opacity slightly
        br, bg, bb = ptype["base_rgb"]
        color_rgb = [
            max(0, min(255, br + rng.randint(-5, 5))),
            max(0, min(255, bg + rng.randint(-5, 5))),
            max(0, min(255, bb + rng.randint(-5, 5))),
        ]
        pool = ptype["notes_pool"]
        notes = rng.sample(pool, min(2, len(pool)))

        return Pigment(
            uid=uid,
            pigment_key=new_key,
            source_type="processed",
            origin_biome=source.origin_biome,
            state="refined",
            color_family=ptype["family"],
            purity=round(_jitter(base["purity"], 0.08), 3),
            opacity=round(_jitter(base["opacity"], 0.05), 3),
            stability=round(_jitter(base["stability"], 0.0), 3),
            granularity=round(max(0.0, source.granularity - 0.10), 3),
            grind_quality=round(min(1.0, source.grind_quality + 0.10), 3),
            color_rgb=color_rgb,
            notes=notes,
            seed=seed,
        )
