import random
import uuid
import pygame
from constants import BLOCK_SIZE, GRAVITY, MAX_FALL, PLAYER_W, PLAYER_H, MINE_REACH, HOTBAR_SIZE
from animals import (Animal, MUTATION_TYPES,
                     COAT_PATTERN_ORDER, LEG_MARKING_ORDER,
                     MANE_COLOR_ORDER, FACE_MARKING_ORDER,
                     _expressed_categorical)

HORSE_MOVE_SPEED  = 1.4   # wander speed (px/frame)
HORSE_FLEE_SPEED  = 3.2   # flee speed when attacked
HORSE_FLEE_RADIUS = 5     # blocks — triggers flee on player approach (only when wild)
HORSE_TRADE_SPEED = 5.0   # base trade-run speed (px/frame); scaled by speed_rating

TEMPERAMENT_THRESHOLDS = {
    "calm":     5,
    "spirited": 9,
    "wild":     14,
}

TEMPERAMENT_BUCK_INTERVAL = {
    "calm":     1.4,
    "spirited": 0.9,
    "wild":     0.55,
}

TEMPERAMENT_BREAK_TIME = {
    "calm":     10.0,
    "spirited": 16.0,
    "wild":     24.0,
}

# Coat color options keyed by biodome name (3 shades per biome)
BIOME_COAT_COLORS = {
    "temperate":      [(180, 120, 60),  (210, 165, 100), (90, 60, 35)],
    "boreal":         [(60, 45, 35),    (80, 58, 40),    (35, 28, 22)],
    "birch_forest":   [(195, 165, 115), (170, 138, 88),  (220, 195, 148)],
    "jungle":         [(100, 70, 40),   (140, 105, 70),  (75, 50, 28)],
    "wetland":        [(130, 105, 70),  (155, 125, 85),  (95, 75, 48)],
    "redwood":        [(80, 52, 30),    (110, 74, 45),   (55, 36, 20)],
    "tropical":       [(200, 170, 110), (175, 140, 80),  (225, 200, 145)],
    "savanna":        [(215, 200, 180), (190, 165, 140), (235, 220, 200)],
    "wasteland":      [(140, 120, 90),  (115, 95, 70),   (160, 142, 108)],
    "alpine_mountain":[(240, 238, 235), (220, 215, 210), (50, 45, 42)],
    "rocky_mountain": [(160, 145, 120), (135, 118, 92),  (185, 170, 148)],
    "rolling_hills":  [(220, 195, 150), (200, 175, 120), (170, 140, 90)],
    "steep_hills":    [(175, 148, 108), (150, 122, 82),  (200, 174, 136)],
    "steppe":         [(200, 168, 110), (175, 142, 88),  (225, 195, 138)],
    "arid_steppe":    [(210, 182, 130), (185, 155, 102), (235, 208, 160)],
    "desert":         [(225, 205, 165), (240, 220, 180), (210, 190, 145)],
    "tundra":         [(245, 242, 238), (230, 225, 218), (200, 195, 185)],
    "swamp":          [(110, 90, 58),   (85, 68, 40),    (135, 112, 78)],
    "beach":          [(200, 185, 150), (215, 200, 170), (175, 155, 115)],
    "canyon":         [(165, 115, 72),  (140, 92, 52),   (190, 140, 98)],
}
_FALLBACK_COAT = [(160, 115, 65), (190, 145, 90), (80, 55, 30)]

# Biomes where horses can spawn
HORSE_BIOMES = {
    "temperate", "boreal", "birch_forest", "rolling_hills", "steep_hills",
    "steppe", "arid_steppe", "savanna", "wasteland", "redwood",
    "rocky_mountain",
}

STABLE_SEARCH_RADIUS = 6   # blocks from each horse to look for STABLE_BLOCK
TROUGH_SEARCH_RADIUS = 5   # blocks from each horse to look for WATER_TROUGH
TROUGH_TAME_RATE     = 0.04  # tame progress per second when near a trough (wild only)


class Horse(Animal):
    ANIMAL_W = 40
    ANIMAL_H = 26
    PREFERRED_FOODS = ("apple", "carrot", "wheat", "sugar_lump")
    MEAT_DROP = (None, 0)

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "horse")

        # Wipe any pending breed cooldown — horses only breed via stable
        self._breed_cooldown = 9999.0

        # Horse-specific traits
        bx = int(float(x) // BLOCK_SIZE)
        biodome = world.biodome_at(bx) if world is not None else "temperate"
        coat_options = BIOME_COAT_COLORS.get(biodome, _FALLBACK_COAT)

        self.traits["speed_rating"]      = round(random.uniform(0.7, 1.3), 3)
        self.traits["stamina_max"]       = round(random.uniform(0.8, 1.2), 3)
        self.traits["temperament"]       = random.choices(
            ["calm", "spirited", "wild"], weights=[3, 4, 3]
        )[0]
        self.traits["coat_color"]        = random.choice(coat_options)
        self.traits["horseshoe_applied"] = False
        self.traits["equipped_saddle"]   = None
        self.traits["equipped_horseshoe"]= None
        self.traits["training_bonuses"]  = {}

        self.stamina    = 100.0
        self.rider      = None       # Player ref when mounted
        self._broken    = False      # True once horse-breaking minigame passed
        self._flee_timer = 0.0       # flee after being attacked
        self._on_trade_run    = False  # True while horse is on an automated trade delivery
        self._trade_target_x  = None  # pixel x destination for current leg of the trip
        self._trade_stuck       = False  # True when horse hasn't made progress toward target
        self._trade_stuck_timer = 0.0    # accumulates dt between progress checks
        self._trade_last_x      = 0.0   # x at start of current check window

        self._init_horse_genotype()

    def _init_horse_genotype(self):
        sr = self.traits["speed_rating"]
        sm = self.traits["stamina_max"]
        self.genotype["speed_gene"]    = [sr, round(random.uniform(0.7, 1.3), 3)]
        self.genotype["stamina_gene"]  = [sm, round(random.uniform(0.8, 1.2), 3)]
        self.genotype["endurance_gene"]= [round(random.uniform(0.8, 1.2), 3),
                                          round(random.uniform(0.8, 1.2), 3)]
        self.genotype["gait_gene"]     = [round(random.uniform(0.8, 1.2), 3),
                                          round(random.uniform(0.8, 1.2), 3)]
        self.genotype["reaction_gene"] = [round(random.uniform(0.7, 1.3), 3),
                                          round(random.uniform(0.7, 1.3), 3)]
        self.genotype["agility_gene"]  = [round(random.uniform(0.7, 1.3), 3),
                                          round(random.uniform(0.7, 1.3), 3)]
        self.genotype["heart_gene"]    = [round(random.uniform(0.7, 1.3), 3),
                                          round(random.uniform(0.7, 1.3), 3)]
        self.genotype["coat_pattern_gene"] = [
            random.choices(COAT_PATTERN_ORDER, weights=[55, 25, 15, 5])[0],
            random.choices(COAT_PATTERN_ORDER, weights=[55, 25, 15, 5])[0],
        ]
        self.genotype["leg_marking_gene"] = [
            "none",
            random.choices(LEG_MARKING_ORDER, weights=[60, 25, 15])[0],
        ]
        self.genotype["mane_color_gene"] = [
            "match",
            random.choices(MANE_COLOR_ORDER, weights=[55, 25, 12, 8])[0],
        ]
        self.genotype["face_marking_gene"] = [
            "none",
            random.choices(FACE_MARKING_ORDER, weights=[50, 25, 15, 10])[0],
        ]
        self._apply_genotype_to_traits()

    def _apply_genotype_to_traits(self):
        super()._apply_genotype_to_traits()
        if "speed_gene" in self.genotype:
            avg = (self.genotype["speed_gene"][0] + self.genotype["speed_gene"][1]) / 2
            self.traits["speed_rating"] = round(max(0.6, min(1.4, avg)), 3)
        if "stamina_gene" in self.genotype:
            avg = (self.genotype["stamina_gene"][0] + self.genotype["stamina_gene"][1]) / 2
            self.traits["stamina_max"] = round(max(0.7, min(1.3, avg)), 3)
        if "endurance_gene" in self.genotype:
            avg = (self.genotype["endurance_gene"][0] + self.genotype["endurance_gene"][1]) / 2
            self.traits["endurance"] = round(max(0.7, min(1.3, avg)), 3)
        if "gait_gene" in self.genotype:
            avg = (self.genotype["gait_gene"][0] + self.genotype["gait_gene"][1]) / 2
            self.traits["gait"] = round(max(0.7, min(1.3, avg)), 3)
        if "reaction_gene" in self.genotype:
            avg = (self.genotype["reaction_gene"][0] + self.genotype["reaction_gene"][1]) / 2
            self.traits["reaction"] = round(max(0.7, min(1.3, avg)), 3)
        if "agility_gene" in self.genotype:
            avg = (self.genotype["agility_gene"][0] + self.genotype["agility_gene"][1]) / 2
            self.traits["agility"] = round(max(0.7, min(1.3, avg)), 3)
        if "heart_gene" in self.genotype:
            avg = (self.genotype["heart_gene"][0] + self.genotype["heart_gene"][1]) / 2
            self.traits["heart"] = round(max(0.7, min(1.3, avg)), 3)
        if "coat_pattern_gene" in self.genotype:
            self.traits["coat_pattern"] = _expressed_categorical(
                self.genotype["coat_pattern_gene"], COAT_PATTERN_ORDER
            )
        if "leg_marking_gene" in self.genotype:
            self.traits["leg_marking"] = _expressed_categorical(
                self.genotype["leg_marking_gene"], LEG_MARKING_ORDER
            )
        if "mane_color_gene" in self.genotype:
            self.traits["mane_color"] = _expressed_categorical(
                self.genotype["mane_color_gene"], MANE_COLOR_ORDER
            )
        if "face_marking_gene" in self.genotype:
            self.traits["face_marking"] = _expressed_categorical(
                self.genotype["face_marking_gene"], FACE_MARKING_ORDER
            )

    def _synthesize_genotype_from_traits(self):
        super()._synthesize_genotype_from_traits()
        for gene_key, trait_key, lo, hi in [
            ("speed_gene",    "speed_rating", 0.7, 1.3),
            ("stamina_gene",  "stamina_max",  0.8, 1.2),
            ("endurance_gene","endurance",    0.8, 1.2),
            ("gait_gene",     "gait",         0.8, 1.2),
            ("reaction_gene", "reaction",     0.7, 1.3),
            ("agility_gene",  "agility",      0.7, 1.3),
            ("heart_gene",    "heart",        0.7, 1.3),
        ]:
            v = self.traits.get(trait_key, 1.0)
            noise = random.uniform(-0.04, 0.04)
            self.genotype[gene_key] = [round(max(lo, v + noise), 3), round(max(lo, v - noise), 3)]
        cp = self.traits.get("coat_pattern", "solid")
        self.genotype["coat_pattern_gene"] = [cp, cp]
        lm = self.traits.get("leg_marking", "none")
        self.genotype["leg_marking_gene"] = ["none", lm]
        mc = self.traits.get("mane_color", "match")
        self.genotype["mane_color_gene"] = ["match", mc]
        fm = self.traits.get("face_marking", "none")
        self.genotype["face_marking_gene"] = ["none", fm]

    # ------------------------------------------------------------------
    # Race rating — single composite score for race difficulty / odds
    # ------------------------------------------------------------------

    @property
    def race_rating(self):
        sr = self.traits.get("speed_rating", 1.0)
        sm = self.traits.get("stamina_max",  1.0)
        en = self.traits.get("endurance",    1.0)
        gt = self.traits.get("gait",         1.0)
        raw = sr * 0.40 + sm * 0.25 + en * 0.20 + gt * 0.15
        return round(max(0.5, min(1.5, raw)), 3)

    # ------------------------------------------------------------------
    # Non-killable — flee instead
    # ------------------------------------------------------------------

    def try_harvest(self, player, dt):
        self._flee_timer = max(self._flee_timer, 4.0)
        self.reset_harvest()
        return None

    def _try_harvest_resource(self, player, dt):
        return None

    # ------------------------------------------------------------------
    # Taming
    # ------------------------------------------------------------------

    def try_feed(self, player):
        if self.tamed:
            return False
        item_id = player.hotbar[player.selected_slot]
        if not item_id:
            return False

        progress_gain = 0
        if item_id == "horse_brush":
            if player.inventory.get("horse_brush", 0) <= 0:
                return False
            # Consume one brush
            player.inventory["horse_brush"] -= 1
            if player.inventory["horse_brush"] <= 0:
                del player.inventory["horse_brush"]
                for i in range(HOTBAR_SIZE):
                    if player.hotbar[i] == "horse_brush":
                        player.hotbar[i] = None
                        break
            progress_gain = 2
        elif item_id in self.PREFERRED_FOODS:
            if player.inventory.get(item_id, 0) <= 0:
                return False
            player.inventory[item_id] -= 1
            if player.inventory[item_id] <= 0:
                del player.inventory[item_id]
                for i in range(HOTBAR_SIZE):
                    if player.hotbar[i] == item_id:
                        player.hotbar[i] = None
                        break
            # sugar_lump counts as 2
            progress_gain = 2 if item_id == "sugar_lump" else 1
        else:
            return False

        self.tame_progress += progress_gain
        threshold = TEMPERAMENT_THRESHOLDS[self.traits["temperament"]]
        threshold -= getattr(player, "horse_whisperer_bonus", 0)
        threshold = max(1, threshold)
        if self.tame_progress >= threshold:
            self.tamed = True
            player.horses_tamed = getattr(player, "horses_tamed", 0) + 1
            # Update codex records
            sr = self.traits["speed_rating"]
            sm = self.traits["stamina_max"]
            records = getattr(player, "horse_records", {})
            if sr > records.get("best_speed", 0.0):
                records["best_speed"] = sr
            if sm > records.get("best_stamina", 0.0):
                records["best_stamina"] = sm
            player.horse_records = records
            biodome = self.world.biodome_at(int(self.x // BLOCK_SIZE)) if self.world else "temperate"
            disc = getattr(player, "discovered_coat_biomes", set())
            disc.add(biodome)
            player.discovered_coat_biomes = disc
        return True

    # ------------------------------------------------------------------
    # Breeding — disabled for auto; called explicitly from stable UI
    # ------------------------------------------------------------------

    def _breed(self, other, world):
        # Block automatic proximity breeding from Animal.update()
        self._breed_cooldown = 9999.0
        return

    def breed_with(self, other, world, player):
        """Player-triggered breeding at a stable. Returns offspring or None."""
        if self.no_breed or other.no_breed:
            return None
        if self.traits.get("sex") == other.traits.get("sex"):
            return None
        if not (self.tamed and other.tamed):
            return None
        if not (self._stable_nearby(world) or other._stable_nearby(world)):
            return None

        offspring = Horse((self.x + other.x) / 2, (self.y + other.y) / 2, world)

        # Mendelian allele inheritance
        offspring._inherit_genotype(self, other)

        # color_shift blended (not allele-based)
        cs_a = self.traits["color_shift"]
        cs_b = other.traits["color_shift"]
        offspring.traits["color_shift"] = tuple(
            max(-0.25, min(0.25, (cs_a[i] + cs_b[i]) / 2 + random.uniform(-0.03, 0.03)))
            for i in range(3)
        )
        if offspring.traits.get("mutation") == "albino":
            offspring.traits["color_shift"] = (
                random.uniform(0.20, 0.25),
                random.uniform(0.20, 0.25),
                random.uniform(0.20, 0.25),
            )

        # Temperament: still index-blended since it has 3 discrete states
        order = ["calm", "spirited", "wild"]
        avg_idx = (order.index(self.traits["temperament"]) +
                   order.index(other.traits["temperament"])) / 2
        if getattr(player, "horse_breeding_mastery", False):
            avg_idx = max(0.0, avg_idx - 0.5)
        avg_idx += random.uniform(-0.5, 0.5)
        offspring.traits["temperament"] = order[max(0, min(2, round(avg_idx)))]

        # Coat color blended (RGB, not allele-based)
        ca, cb = self.traits["coat_color"], other.traits["coat_color"]
        offspring.traits["coat_color"] = tuple(
            max(0, min(255, int((ca[i] + cb[i]) / 2) + random.randint(-8, 8)))
            for i in range(3)
        )

        offspring.traits["horseshoe_applied"]  = False
        offspring.traits["equipped_saddle"]    = None
        offspring.traits["equipped_horseshoe"] = None
        offspring.traits["training_bonuses"]   = {}
        offspring.parent_a_uid = self.uid
        offspring.parent_b_uid = other.uid
        offspring.tamed  = True
        offspring._broken = True
        offspring._breed_cooldown = 9999.0

        self._breed_cooldown  = 900.0
        other._breed_cooldown = 900.0
        world.entities.append(offspring)

        if player:
            player.horses_bred = getattr(player, "horses_bred", 0) + 1
            sr2 = offspring.traits["speed_rating"]
            sm2 = offspring.traits["stamina_max"]
            records = getattr(player, "horse_records", {})
            if sr2 > records.get("best_speed", 0.0):
                records["best_speed"] = sr2
            if sm2 > records.get("best_stamina", 0.0):
                records["best_stamina"] = sm2
            player.horse_records = records

        return offspring

    def _stable_nearby(self, world):
        from blocks import STABLE_BLOCK
        cx = int((self.x + self.W / 2) // BLOCK_SIZE)
        cy = int((self.y + self.H / 2) // BLOCK_SIZE)
        for dx in range(-STABLE_SEARCH_RADIUS, STABLE_SEARCH_RADIUS + 1):
            for dy in range(-STABLE_SEARCH_RADIUS, STABLE_SEARCH_RADIUS + 1):
                if world.get_block(cx + dx, cy + dy) == STABLE_BLOCK:
                    return True
        return False

    def _trough_nearby(self, world):
        from blocks import WATER_TROUGH
        cx = int((self.x + self.W / 2) // BLOCK_SIZE)
        cy = int((self.y + self.H / 2) // BLOCK_SIZE)
        for dx in range(-TROUGH_SEARCH_RADIUS, TROUGH_SEARCH_RADIUS + 1):
            for dy in range(-TROUGH_SEARCH_RADIUS, TROUGH_SEARCH_RADIUS + 1):
                if world.get_block(cx + dx, cy + dy) == WATER_TROUGH:
                    return True
        return False

    # ------------------------------------------------------------------
    # Update — handles flee, mounted state, tame-follow, wander
    # ------------------------------------------------------------------

    def update(self, dt):
        if self.dead:
            return

        # Stamina regeneration when not mounted
        if self.rider is None:
            regen = 8.0 * self.traits.get("stamina_max", 1.0) * dt
            self.stamina = min(100.0, self.stamina + regen)
        # Endurance slows drain when sprinting (accessed in player.py via trait key)

        # Tick post-breed cooldown; 9999 means "not on cooldown" so leave it alone
        if self._breed_cooldown < 9999.0:
            self._breed_cooldown = max(0.0, self._breed_cooldown - dt)

        # Rider drives position — skip all locomotion
        if self.rider is not None:
            return

        # Trade run: move toward _trade_target_x, overriding all normal behaviour
        if self._on_trade_run and self._trade_target_x is not None:
            dx = self._trade_target_x - (self.x + self.W / 2)
            if abs(dx) > BLOCK_SIZE:
                speed = HORSE_TRADE_SPEED * self.traits.get("speed_rating", 1.0)
                self.vx = speed if dx > 0 else -speed
                self.facing = 1 if dx > 0 else -1
            else:
                self.vx = 0.0
            if self._in_water():
                self.vy = min(self.vy + GRAVITY * 0.2, 2.5)
                self.vx *= 0.8
            else:
                self.vy = min(self.vy + GRAVITY, MAX_FALL)
            self._move_x(self.vx)
            self._move_y(self.vy)

            # Stuck detection: check progress every 3 seconds when horse should be moving
            if abs(dx) > BLOCK_SIZE * 3:
                self._trade_stuck_timer += dt
                if self._trade_stuck_timer >= 3.0:
                    progress = abs(self.x - self._trade_last_x)
                    self._trade_stuck = progress < 4.0
                    self._trade_last_x = self.x
                    self._trade_stuck_timer = 0.0
            else:
                self._trade_stuck = False
                self._trade_stuck_timer = 0.0

            return

        # Flee when attacked or player too close while wild
        if self._flee_timer > 0:
            self._flee_timer -= dt
            self.vx = self.facing * HORSE_FLEE_SPEED
            if self._in_water():
                self.vy = min(self.vy + GRAVITY * 0.2, 2.5)
                self.vx *= 0.8
            else:
                self.vy = min(self.vy + GRAVITY, MAX_FALL)
            self._move_x(self.vx)
            self._move_y(self.vy)
            return

        # Passive taming from nearby water trough
        if not self.tamed and self._trough_nearby(self.world):
            self.tame_progress += TROUGH_TAME_RATE * dt
            threshold = TEMPERAMENT_THRESHOLDS[self.traits["temperament"]]
            if self.tame_progress >= threshold:
                self.tamed = True
                player = getattr(self.world, '_player_ref', None)
                if player is not None:
                    player.horses_tamed = getattr(player, "horses_tamed", 0) + 1

        # Wild horse flees from nearby player (not when penned in a fence)
        if not self.tamed and not self._near_fence():
            player = getattr(self.world, '_player_ref', None)
            if player is not None:
                pdx = (player.x + PLAYER_W / 2) - (self.x + self.W / 2)
                pdy = (player.y + PLAYER_H / 2) - (self.y + self.H / 2)
                dist = ((pdx / BLOCK_SIZE) ** 2 + (pdy / BLOCK_SIZE) ** 2) ** 0.5
                if dist < HORSE_FLEE_RADIUS:
                    self.vx = (-1 if pdx > 0 else 1) * HORSE_FLEE_SPEED
                    self.facing = 1 if self.vx > 0 else -1
                    if self._in_water():
                        self.vy = min(self.vy + GRAVITY * 0.2, 2.5)
                        self.vx *= 0.8
                    else:
                        self.vy = min(self.vy + GRAVITY, MAX_FALL)
                    self._move_x(self.vx)
                    self._move_y(self.vy)
                    return

        # Tamed: follow player (not when penned in a fence)
        if self.tamed and not self._near_fence():
            player = getattr(self.world, '_player_ref', None)
            if player is not None:
                pdx = (player.x + PLAYER_W / 2) - (self.x + self.W / 2)
                pdy = (player.y + PLAYER_H / 2) - (self.y + self.H / 2)
                dist = ((pdx / BLOCK_SIZE) ** 2 + (pdy / BLOCK_SIZE) ** 2) ** 0.5
                if dist > 3.0:
                    self.vx = HORSE_MOVE_SPEED * (1 if pdx > 0 else -1)
                    self.facing = 1 if self.vx > 0 else -1
                else:
                    self.vx = 0.0
                if self._in_water():
                    self.vy = min(self.vy + GRAVITY * 0.2, 2.5)
                    self.vx *= 0.8
                else:
                    self.vy = min(self.vy + GRAVITY, MAX_FALL)
                self._move_x(self.vx)
                self._move_y(self.vy)
                return

        # Wander
        self._wander_timer -= dt
        if self._wander_timer <= 0:
            self._wander_timer = random.uniform(2.0, 6.0)
            self._wander_dir = random.choice([-1, -1, 0, 0, 0, 1, 1])

        self.vx = self._wander_dir * HORSE_MOVE_SPEED
        if self.vx != 0:
            self.facing = 1 if self.vx > 0 else -1

        if self._in_water():
            self.vy = min(self.vy + GRAVITY * 0.2, 2.5)
            self.vx *= 0.8
        else:
            self.vy = min(self.vy + GRAVITY, MAX_FALL)
        self._move_x(self.vx)
        self._move_y(self.vy)


_HERD_VISUAL_GENES = {"coat_pattern_gene", "leg_marking_gene", "mane_color_gene", "face_marking_gene"}

def _blend_to_herd_template(horse, alpha):
    """Shift a herd member's float genes ~60% toward the alpha's, copy visual genes, and match coat color."""
    horse.traits["coat_color"] = alpha.traits["coat_color"]
    for gene_key, a_vals in alpha.genotype.items():
        if gene_key not in horse.genotype:
            continue
        d_vals = horse.genotype[gene_key]
        if gene_key in _HERD_VISUAL_GENES:
            horse.genotype[gene_key] = list(a_vals)
        elif isinstance(d_vals[0], float):
            horse.genotype[gene_key] = [
                round(0.6 * a + 0.4 * d, 3)
                for a, d in zip(a_vals, d_vals)
            ]
    horse._apply_genotype_to_traits()
    # coat_color is not derived from genotype — re-apply it after trait update
    horse.traits["coat_color"] = alpha.traits["coat_color"]
