import random
from constants import BLOCK_SIZE, GRAVITY, MAX_FALL

# ---------------------------------------------------------------------------
# Reputation helpers
# ---------------------------------------------------------------------------

def visitors_for_rep(rep):
    if rep >= 40:  return 4
    if rep >= 20:  return 3
    if rep >= 1:   return 2
    return 0


def _rep_tier_bonus(rep):
    if rep >= 40:  return 14
    if rep >= 20:  return 8
    if rep >= 1:   return 3
    return 0


# ---------------------------------------------------------------------------
# Tea item registry — all 21 brewed items, keyed by base tea type
# ---------------------------------------------------------------------------

TEA_ITEM_IDS = {
    "white":   ["white_tea",  "white_tea_fine",  "white_tea_aged"],
    "yellow":  ["yellow_tea", "yellow_tea_fine",  "yellow_tea_aged"],
    "green":   ["green_tea",  "green_tea_fine",   "green_tea_aged"],
    "oolong":  ["oolong_tea", "oolong_tea_fine",  "oolong_tea_aged"],
    "black":   ["black_tea",  "black_tea_fine",   "black_tea_aged"],
    "puerh":   ["puerh_tea",  "puerh_tea_fine",   "puerh_tea_aged"],
    "hojicha": ["hojicha",    "hojicha_fine",     "hojicha_aged"],
}

ALL_TEA_ITEM_IDS = {iid for items in TEA_ITEM_IDS.values() for iid in items}


def _quality_suffix(item_id):
    if item_id.endswith("_aged"):  return "aged"
    if item_id.endswith("_fine"):  return "fine"
    return "base"


def _base_type_from_item(item_id):
    for tea_type, ids in TEA_ITEM_IDS.items():
        if item_id in ids:
            return tea_type
    return None


# ---------------------------------------------------------------------------
# Tip calculation
# ---------------------------------------------------------------------------

def calculate_tip(visitor, tea_item_id, town_rep):
    base = 6 + _rep_tier_bonus(town_rep)
    served_type = _base_type_from_item(tea_item_id)
    type_match = 1.5 if served_type == visitor.preferred_type else 1.0
    qual = _quality_suffix(tea_item_id)
    quality_mult = 1.6 if qual == "aged" else (1.25 if qual == "fine" else 1.0)
    return max(1, int(base * type_match * quality_mult * visitor.mood))


# ---------------------------------------------------------------------------
# Name and preference pools per archetype
# ---------------------------------------------------------------------------

_ARCHETYPE_PREFS = {
    "farmer":   ["oolong", "puerh"],
    "guard":    ["black",  "hojicha"],
    "scholar":  ["green",  "white"],
    "elder":    ["white",  "puerh"],
    "merchant": ["oolong", "black"],
    "traveler": ["black",  "oolong"],
    "pilgrim":  ["green",  "white"],
    "villager": ["yellow", "hojicha"],
}

_ARCHETYPE_NAMES = {
    "farmer":   ["Aldric", "Berin", "Calla", "Darra", "Edwin", "Fern", "Gareth", "Hila",
                 "Iwan", "Jossa", "Keld", "Lira", "Maren", "Nold", "Orra", "Penn"],
    "guard":    ["Orlan", "Brek", "Cassia", "Dorn", "Elvar", "Fyra", "Gavon", "Helda",
                 "Ingrid", "Jorn", "Kavar", "Lexa", "Morroc", "Nessa", "Oswin", "Pala"],
    "scholar":  ["Aelindra", "Brant", "Cynara", "Delwin", "Erys", "Fenwick", "Galla", "Heln",
                 "Ivar", "Jessa", "Kyran", "Lysse", "Mirel", "Nevra", "Orin", "Prynn"],
    "elder":    ["Arvid", "Bessa", "Colm", "Dola", "Eadred", "Fala", "Gorm", "Hesta",
                 "Isen", "Jola", "Kira", "Loga", "Maga", "Nira", "Odda", "Palva"],
    "merchant": ["Aldous", "Brenna", "Carwin", "Deva", "Esmer", "Flass", "Goran", "Hetta",
                 "Ivo", "Jaret", "Korda", "Lyra", "Maldo", "Neven", "Oskar", "Petra"],
    "traveler": ["Arik", "Balla", "Cend", "Davan", "Elia", "Fors", "Gita", "Hadda",
                 "Irma", "Jarv", "Kessa", "Lorran", "Mika", "Nalla", "Ovar", "Pren"],
    "pilgrim":  ["Aelin", "Brath", "Coran", "Devla", "Ethor", "Finia", "Gael", "Havel",
                 "Ilven", "Jaron", "Keld", "Laran", "Mael", "Navar", "Oryn", "Paven"],
    "villager": ["Adda", "Bram", "Cessa", "Dola", "Eldra", "Finna", "Gorn", "Halla",
                 "Itta", "Jolda", "Kerra", "Lenna", "Minna", "Nella", "Osta", "Pella"],
}

# Clothing palette per archetype: [skin, shirt, pants, boot]
_ARCHETYPE_PALETTE = {
    "farmer":   [(220, 185, 145), (160, 115,  55), (100,  75,  40), ( 80,  60,  35)],
    "guard":    [(200, 170, 135), ( 70,  80,  95), ( 55,  65,  80), ( 45,  50,  60)],
    "scholar":  [(230, 200, 165), (145, 125, 175), (100,  85, 130), ( 70,  60,  90)],
    "elder":    [(200, 175, 150), (185, 170, 145), (140, 128, 108), ( 90,  82,  70)],
    "merchant": [(215, 180, 140), (130,  90,  40), ( 90,  65,  30), ( 70,  50,  25)],
    "traveler": [(195, 165, 130), (100, 110,  90), ( 75,  82,  65), ( 55,  60,  50)],
    "pilgrim":  [(225, 195, 160), (210, 205, 195), (180, 175, 165), (120, 118, 112)],
    "villager": [(218, 188, 148), (170, 130,  85), (115,  88,  55), ( 85,  65,  42)],
}

# Tea preference hint shown in UI
_PREF_HINTS = {
    "white":   "Prefers delicate, light tea",
    "yellow":  "Enjoys mellow, golden tea",
    "green":   "Favours fresh, grassy tea",
    "oolong":  "Likes complex, floral-earthy tea",
    "black":   "Wants bold, robust tea",
    "puerh":   "Seeks deep, earthy tea",
    "hojicha": "Craves warm, roasted tea",
}

# ---------------------------------------------------------------------------
# Conversation pools
# ---------------------------------------------------------------------------

VISITOR_CONVERSATIONS = {
    "farmer": {
        "life": [
            ["Aldric wraps both hands around the cup.",
             '"This time of year the soil gets cold before you do.',
             ' Had to replant the east row twice this season."',
             "He sips slowly. \"Still. Harvest came through.\""],
            ["The farmer stares into the cup for a moment.",
             '"My grandfather always said good tea meant the day was worth finishing."',
             " Never thought much about it until now.",
             " Suppose he was right."],
            ["She tilts the cup, watching the colour.",
             '"We had rain for eight days straight.',
             ' Lost the barley.',
             ' Kept the rye. Could have been worse."'],
            ["He exhales through his nose.",
             '"My boy wants to leave for the city.',
             " I can't blame him. It's quieter here than it used to be.",
             " But the land's still good.\""],
        ],
        "philosophy": [
            ['"You can\'t rush a field any more than you can rush a cup of tea."',
             " Both need the right conditions and then they do it themselves."],
            ['"A bad harvest teaches you more than a good one.',
             " The good ones you just accept.",
             ' The bad ones you carry home and think about.\"'],
        ],
    },
    "guard": {
        "life": [
            ["Orlan sets the cup down and exhales slowly.",
             '"The eastern gate gets cold before dawn.',
             " I never minded. It was quiet.",
             ' Nobody makes trouble that early."'],
            ["The guard turns the cup in his hands.",
             '"Had a long watch last night.',
             " Nothing happened, which is how it should be.",
             ' People forget that nothing happening is the point."'],
            ["She takes a careful sip.",
             '"We moved the patrol line last week.',
             " Closer to the river. Took some adjusting.",
             ' You get used to a route. Then it changes."'],
            ["He looks out past you.",
             '"I\'ve been at the gate for eleven years.',
             " Seen the town triple in size.",
             ' Sometimes I wonder if I\'m guarding the same place."'],
        ],
        "philosophy": [
            ['"You learn more standing still than moving.',
             " Took me years to believe that.",
             ' Now it\'s just obvious."'],
            ['"Most problems resolve themselves if you let them.',
             ' The ones that don\'t — those are the ones that matter."'],
        ],
    },
    "scholar": {
        "life": [
            ["The scholar holds the cup near her face, breathing it in.",
             '"Green tea is a manuscript — everything worth knowing is already there.',
             " You just need to learn how to read it.",
             ' Or so I tell my students."'],
            ["He opens a small notebook, then puts it away.",
             '"I was cataloguing herb varieties this morning.',
             " There's a valerian growing near the north wall that shouldn't be there.",
             ' It suggests the soil profile is unusual."'],
            ["She traces the rim of the cup thoughtfully.",
             '"I\'ve been reading about the old roads.',
             " They used to run much further east than anyone thinks.",
             ' The maps are all wrong, of course."'],
            ["The scholar nods, as if confirming something to himself.",
             '"A well-made tea has more information in it than most books.',
             " Soil, climate, the hand of the maker.",
             ' You just have to know what to taste."'],
        ],
        "philosophy": [
            ['"The best questions are the ones you can\'t answer yet.',
             " They teach patience.",
             ' The ones you can answer are just exercise."'],
            ['"Understanding is not the same as knowledge.',
             " I\'ve spent thirty years collecting the second",
             ' and am still waiting for the first."'],
        ],
    },
    "elder": {
        "life": [
            ["The elder wraps the cup in both palms.",
             '"I used to drink black tea every morning.',
             " Now I prefer white.",
             ' I think that says something about me, though I\'m not sure what."'],
            ["She closes her eyes for a moment after the first sip.",
             '"My husband planted a tea bush forty years ago.',
             " It\'s still growing.",
             ' He isn\'t. But the tea is."'],
            ["He speaks slowly, as if each word costs something.",
             '"When I was young I thought experience would make things clearer.',
             " It hasn\'t.",
             ' But it has made them quieter."'],
            ["The elder looks at the tea for a long time before speaking.",
             '"My granddaughter asked me what I regret.',
             " I told her: the hurrying.",
             ' She didn\'t understand. She will."'],
        ],
        "philosophy": [
            ['"Time is the ingredient that can\'t be added later.',
             ' You either let a thing age or you don\'t."'],
            ['"The young want answers.',
             " The old want the right questions.",
             ' The wise ones learn this is the same thing."'],
        ],
    },
    "merchant": {
        "life": [
            ["The merchant assesses the tea the way she assesses everything.",
             '"Fair quality.',
             " Better than the eastern road stops.",
             ' I\'ve been drinking bad tea for three weeks."'],
            ["He pulls out a ledger, then decides against it.",
             '"I crossed the pass twice this season.',
             " Second time was worse.",
             ' But the price at the other end was better, so."'],
            ["She holds the cup at arm\'s length briefly, then drinks.",
             '"I used to sell tea, actually.',
             " Years ago.",
             ' Never thought I\'d miss it until I stopped."'],
            ["The merchant leans back.",
             '"Everything has its price and its season.',
             " Tea, wool, reputation.",
             ' The trick is knowing which season you\'re in."'],
        ],
        "philosophy": [
            ['"A fair price is one both sides would agree to twice.',
             " Most prices don\'t qualify.",
             ' Good tea comes close."'],
            ['"I\'ve learned that the best deals are the ones neither side regrets.',
             " They\'re also the rarest.",
             ' Treasure them."'],
        ],
    },
    "traveler": {
        "life": [
            ["The traveler stretches her shoulders before drinking.",
             '"I\'ve had tea in five different cities this year.',
             " This is the first one that tasted like someone made it on purpose.",
             ' Most people just pour water."'],
            ["He drops his pack by the door.",
             '"Three days on the coastal road.',
             " Sleeping rough.",
             ' A cup of tea makes a bed out of any floor."'],
            ["She wraps both hands around the warmth.",
             '"I don\'t stay anywhere long.',
             " But I always remember where the tea was good.",
             ' It\'s how I know where I\'ve been."'],
            ["The traveler looks out as if checking the road.",
             '"I\'m heading north eventually.',
             " Everyone says don\'t go in winter.",
             ' I\'ve been going where they say don\'t for years."'],
        ],
        "philosophy": [
            ['"A road shows you what\'s out there.',
             " Tea shows you where you are.",
             ' Both are necessary."'],
            ['"The mistake most people make is thinking arrival is the point.',
             " The road is the point.",
             ' You just need somewhere to go."'],
        ],
    },
    "pilgrim": {
        "life": [
            ["The pilgrim folds her hands around the cup.",
             '"I\'ve been walking since the last new moon.',
             " I don\'t know if I\'ll find what I\'m looking for.",
             ' But I think the looking is part of it."'],
            ["He drinks quietly, then speaks.",
             '"The shrine I visited last week was empty.',
             " No keeper, no offerings.",
             ' Just stone and light.',
             ' It was enough."'],
            ["She looks at the steam rising from the cup.",
             '"I used to live in one place.',
             " Had a house, a garden.",
             ' I gave it up.',
             ' I don\'t miss it the way I thought I would."'],
            ["The pilgrim is quiet a long time.",
             '"Every road leads somewhere.',
             " Even the ones that end in water.",
             ' Especially those."'],
        ],
        "philosophy": [
            ['"The purpose of a journey isn\'t to arrive.',
             " It\'s to become the kind of person",
             ' who no longer needs to leave."'],
            ['"Stillness isn\'t the absence of movement.',
             " It\'s the presence of acceptance.",
             ' I\'m still learning that."'],
        ],
    },
    "villager": {
        "life": [
            ["The villager settles in with the comfortable ease of someone with nowhere to be.",
             '"My neighbour built a second floor last month.',
             " Now she can see into my garden.",
             ' I planted taller hedges.',
             ' She hasn\'t said anything yet."'],
            ["She sips and sighs.",
             '"The baker raised his prices again.',
             " Third time this year.",
             ' Everyone complains.',
             ' Nobody stops buying. Himself included."'],
            ["He looks comfortable.",
             '"I had a good day.',
             " Found what I was looking for at the market.",
             ' Didn\'t have to argue about the price.',
             ' That basically never happens."'],
            ["The villager looks up at the ceiling.",
             '"My cat knocked over a jar of honey this morning.',
             " She didn\'t look sorry.",
             ' I\'ve stopped expecting her to."'],
        ],
        "philosophy": [
            ['"The small things are the big things.',
             " You just don\'t know it until they\'re gone.",
             ' Good tea. A warm fire. Somebody who knows your name."'],
            ['"Contentment isn\'t the same as giving up.',
             " I spent a long time confusing them.",
             ' It\'s more like... arriving."'],
        ],
    },
}


def get_conversation(archetype, town_rep):
    pool = VISITOR_CONVERSATIONS.get(archetype, {})
    use_philosophy = town_rep >= 20 and random.random() < 0.3 and pool.get("philosophy")
    topic = "philosophy" if use_philosophy else "life"
    lines = pool.get(topic, [["They sip the tea in silence."]])
    return random.choice(lines)


# ---------------------------------------------------------------------------
# TeaHouseVisitorNPC
# ---------------------------------------------------------------------------

class TeaHouseVisitorNPC:
    NPC_W = 20
    NPC_H = 28
    _WALK_SPEED = 32.0

    def __init__(self, x, y, world, archetype, rng=None):
        self.x = float(x)
        self.y = float(y)
        self.vy = 0.0
        self.on_ground = False
        self.world = world
        self.archetype = archetype
        rng = rng or random.Random()
        name_pool = _ARCHETYPE_NAMES.get(archetype, _ARCHETYPE_NAMES["villager"])
        self.display_name = rng.choice(name_pool)
        prefs = _ARCHETYPE_PREFS.get(archetype, ["black"])
        self.preferred_type = rng.choice(prefs)
        self.mood = round(rng.uniform(0.85, 1.15), 2)
        self.palette = _ARCHETYPE_PALETTE.get(archetype, _ARCHETYPE_PALETTE["villager"])
        self.facing = 1
        self.state = "walking"   # walking | waiting | served
        self._served_timer = 0.0
        self._bob_timer = 0.0
        self._bob_offset = 0.0
        self._snap_to_surface()

    def _snap_to_surface(self):
        for _ in range(60):
            if not self._collides():
                break
            self.y -= BLOCK_SIZE

    def _collides(self):
        left  = int(self.x // BLOCK_SIZE)
        right = int((self.x + self.NPC_W - 1) // BLOCK_SIZE)
        top   = int(self.y // BLOCK_SIZE)
        bot   = int((self.y + self.NPC_H - 1) // BLOCK_SIZE)
        for bx in range(left, right + 1):
            for by in range(top, bot + 1):
                if self.world.is_solid(bx, by):
                    return True
        return False

    def update(self, dt, tea_house_pos):
        # Gravity
        self.vy = min(self.vy + GRAVITY, MAX_FALL)
        self.y += self.vy
        if self._collides():
            self.y -= self.vy
            self.vy = 0.0
            self.on_ground = True
        else:
            self.on_ground = False

        self._bob_timer += dt
        self._bob_offset = 0.0

        if self.state == "walking" and tea_house_pos is not None:
            target_x = tea_house_pos[0] * BLOCK_SIZE
            dx = target_x - self.x
            dist = abs(dx)
            if dist <= BLOCK_SIZE * 3:
                self.state = "waiting"
                self._bob_offset = 0.0
            else:
                self.facing = 1 if dx > 0 else -1
                old_x = self.x
                self.x += self._WALK_SPEED * dt * self.facing
                if self._collides():
                    self.x = old_x
                self._bob_offset = (self._bob_timer * 2.2 % (2 * 3.14159)) * 1.5

        elif self.state == "waiting":
            self._bob_offset = 0.0

        elif self.state == "served":
            self._served_timer += dt
            self.facing = -1
            old_x = self.x
            self.x -= self._WALK_SPEED * dt
            if self._collides():
                self.x = old_x

    @property
    def pref_hint(self):
        return _PREF_HINTS.get(self.preferred_type, "")

    @property
    def done(self):
        return self.state == "served" and self._served_timer > 5.0


# ---------------------------------------------------------------------------
# Visitor spawning
# ---------------------------------------------------------------------------

_ARCHETYPES = list(_ARCHETYPE_PREFS.keys())


def spawn_visitor(world, tea_house_pos):
    """Create a TeaHouseVisitorNPC near a city and set it walking toward tea_house_pos."""
    from towns import TOWNS
    centers = getattr(world, "town_centers", [])
    if not centers:
        return None
    rng = random.Random()
    city_x = rng.choice(centers) * BLOCK_SIZE
    spawn_x = city_x + rng.randint(-6, 6) * BLOCK_SIZE
    spawn_y = float(getattr(world, "surface_y_at", lambda bx: 60)(int(spawn_x // BLOCK_SIZE)) * BLOCK_SIZE)
    archetype = rng.choice(_ARCHETYPES)
    return TeaHouseVisitorNPC(spawn_x, spawn_y, world, archetype, rng)
