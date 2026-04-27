"""Gladiator system — profiles, fight simulation, arena scheduling."""
import random
import uuid

# ---------------------------------------------------------------------------
# Arena animals — beasts that fight gladiators in beast-hunt bouts
# ---------------------------------------------------------------------------

# Each entry: (display_name, hp, attack, defense, agility, rarity, size_class, body_color)
# size_class: "small" | "medium" | "large" | "huge"
_ANIMAL_DEFS = {
    "rabbit":        ("Rabbit",        22,  8,  2,  9, "common",    "small",  (180, 155, 130)),
    "fox":           ("Fox",           38, 13,  3,  8, "common",    "small",  (195, 110,  45)),
    "wolf":          ("Wolf",          58, 22,  5,  7, "common",    "medium", (120, 115, 110)),
    "warthog":       ("Warthog",       68, 24,  7,  5, "common",    "medium", (130, 100,  75)),
    "boar":          ("Boar",          85, 28,  9,  5, "rare",      "large",  (100,  80,  60)),
    "elk":           ("Elk",           90, 26,  8,  5, "rare",      "large",  (165, 120,  70)),
    "bison":         ("Bison",        100, 26, 12,  3, "rare",      "large",  ( 90,  75,  55)),
    "crocodile":     ("Crocodile",     95, 32, 16,  2, "rare",      "large",  ( 75, 110,  60)),
    "bear":          ("Bear",         115, 36, 11,  3, "rare",      "huge",   (110,  80,  55)),
    "moose":         ("Moose",        108, 28, 13,  4, "rare",      "huge",   (130, 100,  65)),
    "mountain_lion": ("Mountain Lion",100, 38,  8,  8, "legendary", "large",  (180, 155, 110)),
    "tiger":         ("Tiger",        108, 42,  9,  9, "legendary", "huge",   (205, 130,  45)),
    "snow_leopard":  ("Snow Leopard",  95, 36,  8,  8, "legendary", "large",  (210, 205, 200)),
}

# Biome → list of animal_type keys, ordered by how common/likely they are
_BIOME_ANIMAL_POOLS = {
    "mediterranean": ["wolf", "boar", "bear", "crocodile"],
    "desert":        ["warthog", "crocodile", "wolf", "bison"],
    "temperate":     ["boar", "wolf", "bear", "elk", "fox"],
    "steppe":        ["wolf", "bison", "elk", "boar"],
    "jungle":        ["boar", "crocodile", "tiger"],
    "east_asian":    ["wolf", "boar", "tiger", "snow_leopard"],
    "coastal":       ["crocodile", "wolf", "boar"],
    "alpine":        ["bear", "elk", "wolf", "snow_leopard"],
    "silk_road":     ["wolf", "bison", "mountain_lion"],
}
_DEFAULT_ANIMAL_POOL = ["wolf", "boar", "bear"]

# Animal attack flavor text — maps animal type to attack strings
_ANIMAL_ATTACK_TEXT = {
    "rabbit":        ["{a} bolts at {d}!",  "{a} bites savagely!",       "A frantic lunge!"],
    "fox":           ["{a} darts at {d}!",  "{a} slashes and retreats!", "Cunning feint!"],
    "wolf":          ["{a} LUNGES at {d}!", "{a} snaps its jaws!",       "The wolf HOWLS and charges!"],
    "warthog":       ["{a} CHARGES {d}!",   "{a} gores with its tusks!", "A reckless rush!"],
    "boar":          ["{a} CHARGES {d}!",   "{a} slams its tusks in!",   "THUNDEROUS CHARGE!"],
    "elk":           ["{a} RAMS {d}!",      "{a} kicks out!",            "Antlers CRASH down!"],
    "bison":         ["{a} STAMPEDES {d}!", "{a} lowers its head!",      "The earth trembles!"],
    "crocodile":     ["{a} SNAPS at {d}!",  "{a} death-rolls!",          "CRUSHING JAWS!"],
    "bear":          ["{a} MAULS {d}!",     "{a} swipes its paw!",       "A DEVASTATING SWIPE!"],
    "moose":         ["{a} TRAMPLES {d}!",  "{a} headbutts!",            "Antlers GORE!"],
    "mountain_lion": ["{a} POUNCES {d}!",   "{a} rakes with its claws!", "LIGHTNING STRIKE!"],
    "tiger":         ["{a} POUNCES {d}!",   "{a} rakes and mauls!",      "THE CROWD SCREAMS!"],
    "snow_leopard":  ["{a} LEAPS at {d}!",  "{a} claws and bites!",      "IMPOSSIBLE SPEED!"],
}
_ANIMAL_DODGE_TEXT = {
    "rabbit":        "The rabbit zigzags!",
    "fox":           "The fox twists away!",
    "wolf":          "The wolf sidesteps!",
    "warthog":       "The warthog skids aside!",
    "boar":          "The boar deflects the blow!",
    "elk":           "The elk turns the blow!",
    "bison":         "The bison shrugs it off!",
    "crocodile":     "Thick hide absorbs the blow!",
    "bear":          "The bear shrugs off the hit!",
    "moose":         "The moose endures the blow!",
    "mountain_lion": "The lion rolls aside!",
    "tiger":         "The tiger vanishes — then reappears!",
    "snow_leopard":  "The leopard drifts like smoke!",
}

# Crowd reactions specific to beast fights
_BEAST_CROWD_LINES = [
    "The crowd SCREAMS!", "BLOOD AND GLORY!", "They chant the gladiator's name!",
    "The beast ROARS back!", "Rome demands more!", "A hush falls — then erupts!",
    "The arena shakes with noise!", "AVE! AVE! AVE!", "The mob is on its feet!",
]


class ArenaAnimal:
    """A beast that fights in the arena. Duck-types GladiatorProfile for simulation."""

    def __init__(self, animal_type: str):
        defn = _ANIMAL_DEFS.get(animal_type, _ANIMAL_DEFS["wolf"])
        self.uid          = f"animal_{animal_type}"
        self.animal_type  = animal_type
        self.name         = defn[0]
        self._hp          = defn[1]
        self._attack_val  = defn[2]
        self._defense_val = defn[3]
        self._agility_val = defn[4]
        self.rarity       = defn[5]
        self.size_class   = defn[6]
        self.body_color   = defn[7]
        self.wins   = 0
        self.losses = 0
        self.fame   = 0
        self.is_animal = True

    @property
    def max_hp(self):   return self._hp
    @property
    def attack(self):   return self._attack_val
    @property
    def defense(self):  return self._defense_val
    @property
    def agility(self):  return self._agility_val

    def to_dict(self):
        return {"animal_type": self.animal_type}

    @staticmethod
    def from_dict(d):
        return ArenaAnimal(d["animal_type"])


def generate_arena_animal(rng: random.Random, biome: str) -> ArenaAnimal:
    pool = _BIOME_ANIMAL_POOLS.get(biome, _DEFAULT_ANIMAL_POOL)
    # Weight toward rarer animals occasionally
    weights = [3 if _ANIMAL_DEFS[a][5] == "common" else
               2 if _ANIMAL_DEFS[a][5] == "rare"   else 1 for a in pool]
    animal_type = rng.choices(pool, weights=weights)[0]
    return ArenaAnimal(animal_type)

# ---------------------------------------------------------------------------
# Name pools (Roman-flavored + regional variants)
# ---------------------------------------------------------------------------

_NAMES_ROMAN = [
    "Marcus", "Lucius", "Gaius", "Titus", "Quintus", "Sextus", "Decimus",
    "Brutus", "Cassius", "Crassus", "Corvus", "Maximus", "Remus", "Rufus",
    "Vibius", "Flavius", "Marius", "Livius", "Primus", "Regulus",
]
_NAMES_DESERT = [
    "Aziz", "Tariq", "Rashid", "Khalid", "Omar", "Samir", "Zaid",
    "Hadim", "Nasser", "Faris", "Jabir", "Karim", "Walid", "Yusuf",
]
_NAMES_EASTERN = [
    "Wei", "Jin", "Bo", "Shan", "Lei", "Dong", "Kwan", "Yong",
    "Hiroshi", "Ryu", "Ken", "Tatsu", "Isamu", "Akira", "Jiro",
]
_NAMES_STEPPE = [
    "Batu", "Kara", "Tengri", "Arslan", "Bolad", "Timur", "Yesugei",
    "Chagatai", "Kubilai", "Subedei", "Jochi", "Torbei",
]
_EPITHET_POOL = [
    "the Unbroken", "the Fierce", "Ironskin", "Bloodfist", "the Relentless",
    "of the Sand", "the Wolf", "the Bear", "the Hawk", "Stonehands",
    "the Merciless", "the Swift", "the Bold", "Scarface", "the Giant",
    "the Fox", "the Serpent", "the Lion", "Deathblow", "the Cruel",
]

_BIOME_NAMES = {
    "desert":        _NAMES_DESERT,
    "east_asian":    _NAMES_EASTERN,
    "steppe":        _NAMES_STEPPE,
    "silk_road":     _NAMES_STEPPE,
    "jungle":        _NAMES_ROMAN,
    "mediterranean": _NAMES_ROMAN,
}

# ---------------------------------------------------------------------------
# Appearance pools — reuse GuardNPC kit/helmet strings exactly
# ---------------------------------------------------------------------------

_GLADIATOR_KITS = [
    "swordsman", "spearman", "axeman", "macer", "halberdier", "lancer",
]
_GLADIATOR_HELMETS = ["pot", "kettle", "sallet", "plumed", "coif"]
_GLADIATOR_HELMET_FINISH = ["steel", "bronze", "burnished", "blackened"]

_RARITY_WEIGHTS = [70, 22, 8]   # common, rare, legendary
_RARITY_LABELS  = ["common", "rare", "legendary"]
_RARITY_STAT_BONUS = {"common": 0, "rare": 2, "legendary": 4}

# Color palettes by biome (armor / plate / trim)
_BIOME_COLORS = {
    "desert":        {"armor": (120, 95, 60), "plate": (180, 150, 80), "trim": (200, 130, 30)},
    "east_asian":    {"armor": (50, 55, 80),  "plate": (170, 50, 50),  "trim": (220, 180, 80)},
    "steppe":        {"armor": (75, 65, 50),  "plate": (130, 110, 70), "trim": (60, 100, 60)},
    "silk_road":     {"armor": (90, 70, 110), "plate": (160, 120, 60), "trim": (180, 60, 60)},
    "mediterranean": {"armor": (60, 60, 90),  "plate": (210, 200, 160),"trim": (140, 35, 35)},
    "jungle":        {"armor": (55, 85, 55),  "plate": (120, 100, 60), "trim": (30, 130, 80)},
}
_DEFAULT_COLORS = {"armor": (55, 55, 75), "plate": (155, 160, 165), "trim": (140, 35, 35)}


# ---------------------------------------------------------------------------
# GladiatorProfile
# ---------------------------------------------------------------------------

class GladiatorProfile:
    """All data for one gladiator; dict-serializable."""

    __slots__ = (
        "uid", "name", "origin_biome",
        "kit", "helmet", "helmet_finish", "emblem", "tint",
        "skin_tone", "shield_color", "boots", "clothing",
        "strength", "agility", "endurance",
        "fame", "wins", "losses", "rarity",
    )

    def __init__(self, uid, name, origin_biome,
                 kit, helmet, helmet_finish, emblem, tint,
                 skin_tone, shield_color, boots, clothing,
                 strength, agility, endurance,
                 fame=0, wins=0, losses=0, rarity="common"):
        self.uid            = uid
        self.name           = name
        self.origin_biome   = origin_biome
        self.kit            = kit
        self.helmet         = helmet
        self.helmet_finish  = helmet_finish
        self.emblem         = emblem
        self.tint           = tint
        self.skin_tone      = skin_tone
        self.shield_color   = shield_color
        self.boots          = boots
        self.clothing       = clothing
        self.strength       = strength
        self.agility        = agility
        self.endurance      = endurance
        self.fame           = fame
        self.wins           = wins
        self.losses         = losses
        self.rarity         = rarity

    # ---- derived stats ----

    @property
    def max_hp(self):
        return 80 + self.endurance * 8

    @property
    def attack(self):
        return self.strength * 3 + self.agility

    @property
    def defense(self):
        return self.endurance * 2 + self.agility // 2

    # ---- serialization ----

    def to_dict(self):
        return {
            "uid": self.uid, "name": self.name, "origin_biome": self.origin_biome,
            "kit": self.kit, "helmet": self.helmet, "helmet_finish": self.helmet_finish,
            "emblem": self.emblem, "tint": self.tint,
            "skin_tone": list(self.skin_tone), "shield_color": list(self.shield_color),
            "boots": list(self.boots), "clothing": {k: list(v) for k, v in self.clothing.items()},
            "strength": self.strength, "agility": self.agility, "endurance": self.endurance,
            "fame": self.fame, "wins": self.wins, "losses": self.losses, "rarity": self.rarity,
        }

    @staticmethod
    def from_dict(d):
        return GladiatorProfile(
            uid=d["uid"], name=d["name"], origin_biome=d["origin_biome"],
            kit=d["kit"], helmet=d["helmet"], helmet_finish=d["helmet_finish"],
            emblem=d.get("emblem", "none"), tint=d.get("tint", 0),
            skin_tone=tuple(d["skin_tone"]), shield_color=tuple(d["shield_color"]),
            boots=tuple(d["boots"]),
            clothing={k: tuple(v) for k, v in d["clothing"].items()},
            strength=d["strength"], agility=d["agility"], endurance=d["endurance"],
            fame=d.get("fame", 0), wins=d.get("wins", 0), losses=d.get("losses", 0),
            rarity=d.get("rarity", "common"),
        )

    # ---- fake NPC duck-typing for the renderer ----
    # draw_npc_guard expects .clothing, .kit, .helmet, etc as attrs — we have them.
    # Also needs ._bob_offset and .facing, which the caller sets temporarily.
    @property
    def _bob_offset(self):
        return 0

    @property
    def cape(self):
        return "none"

    @property
    def beard(self):
        return "none"

    @property
    def tabard(self):
        return "solid"

    @property
    def sash(self):
        return False


# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------

def generate_gladiator(rng: random.Random, biome: str = "temperate") -> GladiatorProfile:
    name_pool = _BIOME_NAMES.get(biome, _NAMES_ROMAN)
    first = rng.choice(name_pool)
    epithet = rng.choice(_EPITHET_POOL)
    name = f"{first} {epithet}"

    rarity = rng.choices(_RARITY_LABELS, weights=_RARITY_WEIGHTS)[0]
    bonus  = _RARITY_STAT_BONUS[rarity]
    base   = lambda lo, hi: rng.randint(lo, hi)

    strength  = min(10, base(2, 7) + bonus)
    agility   = min(10, base(2, 7) + bonus)
    endurance = min(10, base(2, 7) + bonus)
    fame      = rng.randint(0, 40) + bonus * 10

    kit     = rng.choice(_GLADIATOR_KITS)
    helmet  = rng.choice(_GLADIATOR_HELMETS)
    finish  = rng.choice(_GLADIATOR_HELMET_FINISH)
    emblems = ["none", "cross", "star", "circle", "chevron"]
    emblem  = rng.choice(emblems)
    tint    = rng.randint(-15, 15)

    pal = _BIOME_COLORS.get(biome, _DEFAULT_COLORS)
    skin_tones = [(245, 215, 175), (210, 175, 140), (180, 140, 100),
                  (150, 110, 70),  (110, 75, 45)]
    skin_tone   = rng.choice(skin_tones)
    shield_color = tuple(min(255, v + rng.randint(-20, 20)) for v in (140, 35, 35))
    boots       = (60, 45, 30)
    clothing    = {
        "armor": pal["armor"],
        "plate": pal["plate"],
        "trim":  pal["trim"],
        "skin":  skin_tone,
    }

    uid = str(uuid.uuid4())[:8]
    return GladiatorProfile(
        uid=uid, name=name, origin_biome=biome,
        kit=kit, helmet=helmet, helmet_finish=finish,
        emblem=emblem, tint=tint,
        skin_tone=skin_tone, shield_color=shield_color,
        boots=boots, clothing=clothing,
        strength=strength, agility=agility, endurance=endurance,
        fame=fame, rarity=rarity,
    )


# ---------------------------------------------------------------------------
# Fight simulation
# ---------------------------------------------------------------------------

_CRIT_LABELS   = ["DEVASTATING BLOW", "PERFECT STRIKE", "BRUTAL HIT", "CRUSHING FORCE"]
_DODGE_LABELS  = ["PERFECT DODGE", "NIMBLE ESCAPE", "NEAR MISS", "SWIFT PARRY"]
_NORMAL_LABELS = ["strikes", "hits", "lands a blow on", "hammers", "slashes at"]


def _animal_attack_label(animal, defender_name, rng, is_crit, damage):
    if damage == 0:
        return _ANIMAL_DODGE_TEXT.get(animal.animal_type, f"The {animal.name} misses!")
    texts = _ANIMAL_ATTACK_TEXT.get(animal.animal_type, ["{a} attacks {d}!"])
    tmpl = rng.choice(texts)
    label = tmpl.format(a=animal.name, d=defender_name.split()[0])
    if is_crit:
        label = label.rstrip("!") + "!!"
    return label


def _gladiator_attack_label(attacker, defender, rng, is_crit, damage):
    if is_crit and damage > 0:
        return rng.choice(_CRIT_LABELS)
    if damage == 0:
        return rng.choice(_DODGE_LABELS)
    aname = attacker.name.split()[0]
    dname = (defender.name if not getattr(defender, "is_animal", False)
             else defender.name)
    return f"{aname} {rng.choice(_NORMAL_LABELS)} {dname}"


def _make_round_event(round_num, attacker, defender, damage, is_crit,
                      hp1_after, hp2_after, is_g1_attacking, rng):
    a_is_animal = getattr(attacker, "is_animal", False)
    if a_is_animal:
        label = _animal_attack_label(attacker, defender.name, rng, is_crit, damage)
    else:
        label = _gladiator_attack_label(attacker, defender, rng, is_crit, damage)
    return {
        "round":           round_num,
        "attacker":        attacker.name,
        "defender":        defender.name,
        "damage":          damage,
        "crit":            is_crit,
        "hp1_after":       hp1_after,
        "hp2_after":       hp2_after,
        "label":           label,
        "is_g1_attacking": is_g1_attacking,
        "attacker_is_animal": a_is_animal,
    }


def simulate_fight(g1, g2, rng: random.Random) -> list:
    """Return a list of round-event dicts. g1/g2 may be GladiatorProfile or ArenaAnimal."""
    hp1 = g1.max_hp
    hp2 = g2.max_hp
    rounds = []

    for round_num in range(1, 14):
        if hp1 <= 0 or hp2 <= 0:
            break

        # Higher agility attacks first; tie goes to g1
        if g2.agility > g1.agility:
            attacker, defender = g2, g1
            is_g1_attacking = False
        else:
            attacker, defender = g1, g2
            is_g1_attacking = True

        raw      = rng.randint(0, attacker.attack)
        is_crit  = rng.random() < 0.18
        if is_crit:
            raw = int(raw * 1.5)
        damage = max(0, raw - defender.defense // 2)

        if is_g1_attacking:
            hp2 = max(0, hp2 - damage)
        else:
            hp1 = max(0, hp1 - damage)

        rounds.append(_make_round_event(
            round_num, attacker, defender, damage, is_crit,
            hp1, hp2, is_g1_attacking, rng))

        if hp1 <= 0 or hp2 <= 0:
            break

        # Retaliation swing
        if is_g1_attacking:
            atk2, def2 = g2, g1
            g2_swings = True
        else:
            atk2, def2 = g1, g2
            g2_swings = False

        raw2     = rng.randint(0, atk2.attack)
        is_crit2 = rng.random() < 0.18
        if is_crit2:
            raw2 = int(raw2 * 1.5)
        damage2 = max(0, raw2 - def2.defense // 2)

        if g2_swings:
            hp1 = max(0, hp1 - damage2)
        else:
            hp2 = max(0, hp2 - damage2)

        rounds.append(_make_round_event(
            round_num, atk2, def2, damage2, is_crit2,
            hp1, hp2, not g2_swings, rng))

    winner = g1 if hp1 > 0 else g2
    loser  = g2 if hp1 > 0 else g1
    winner.wins  += 1
    if not getattr(winner, "is_animal", False):
        winner.fame = min(100, winner.fame + (15 if getattr(loser, "is_animal", False) else 10))
    loser.losses += 1
    if not getattr(loser, "is_animal", False):
        loser.fame = max(0, loser.fame - 3)

    return rounds


# ---------------------------------------------------------------------------
# Arena scheduling
# ---------------------------------------------------------------------------

class Bout:
    """One fight on the card — either a duel or beast hunt."""
    __slots__ = ("g1", "g2", "bout_type", "round_log", "winner_uid")

    # bout_type: "duel" | "beast_hunt" | "champion"
    def __init__(self, g1, g2, bout_type="duel"):
        self.g1         = g1
        self.g2         = g2
        self.bout_type  = bout_type
        self.round_log  = []
        self.winner_uid = None


_BOUT_TYPE_LABEL = {
    "duel":       "DUEL",
    "beast_hunt": "BEAST HUNT",
    "champion":   "CHAMPION BOUT",
}
_BOUT_TYPE_COLOR = {
    "duel":       (140, 180, 230),
    "beast_hunt": (210, 110,  60),
    "champion":   (215, 185,  55),
}


def generate_arena_week(region_seed: int, day_count: int,
                        biome: str = "temperate") -> list:
    """Return list of 3 Bouts with mixed types (deterministic per week)."""
    week = day_count // 7
    rng  = random.Random(region_seed ^ (week * 0x9e3779b9))

    bouts = []

    # Bout 0: always beast hunt — dramatic opener
    g_opener = generate_gladiator(rng, biome)
    animal   = generate_arena_animal(rng, biome)
    bouts.append(Bout(g_opener, animal, "beast_hunt"))

    # Bout 1: classic duel
    g1 = generate_gladiator(rng, biome)
    g2 = generate_gladiator(rng, biome)
    bouts.append(Bout(g1, g2, "duel"))

    # Bout 2: champion duel or second beast hunt (33% beast)
    if rng.random() < 0.33:
        g_champ  = generate_gladiator(rng, biome)
        animal2  = generate_arena_animal(rng, biome)
        bouts.append(Bout(g_champ, animal2, "beast_hunt"))
    else:
        # Champion bout: higher-stat fighters
        gc1 = generate_gladiator(rng, biome)
        gc2 = generate_gladiator(rng, biome)
        # Boost stats to feel like seasoned fighters
        for g in (gc1, gc2):
            g.strength  = min(10, g.strength  + 2)
            g.agility   = min(10, g.agility   + 2)
            g.endurance = min(10, g.endurance + 2)
            g.fame      = min(100, g.fame + 30)
            g.wins     += rng.randint(3, 12)
        bouts.append(Bout(gc1, gc2, "champion"))

    return bouts


def is_games_day(region_seed: int, day_count: int) -> bool:
    """True if today is a scheduled games day for this arena."""
    interval = 3 + (region_seed % 3)   # 3, 4, or 5 day cycle
    offset   = region_seed % interval
    return (day_count + offset) % interval == 0


def days_until_games(region_seed: int, day_count: int) -> int:
    """How many days until the next games day."""
    interval = 3 + (region_seed % 3)
    offset   = region_seed % interval
    for d in range(1, interval + 1):
        if (day_count + d + offset) % interval == 0:
            return d
    return interval
