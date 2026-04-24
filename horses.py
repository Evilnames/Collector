import random
import uuid
import pygame
from constants import BLOCK_SIZE, GRAVITY, MAX_FALL, PLAYER_W, PLAYER_H, MINE_REACH, HOTBAR_SIZE
from animals import Animal, MUTATION_TYPES, MUTATION_CHANCE, MUTATION_INHERIT_ONE, MUTATION_INHERIT_BOTH

HORSE_MOVE_SPEED  = 1.4   # wander speed (px/frame)
HORSE_FLEE_SPEED  = 3.2   # flee speed when attacked
HORSE_FLEE_RADIUS = 5     # blocks — triggers flee on player approach (only when wild)

TEMPERAMENT_THRESHOLDS = {
    "calm":     5,
    "spirited": 9,
    "wild":     14,
}

TEMPERAMENT_BUCK_INTERVAL = {
    "calm":     1.8,
    "spirited": 1.2,
    "wild":     0.8,
}

TEMPERAMENT_BREAK_TIME = {
    "calm":  6.0,
    "spirited": 8.0,
    "wild":  10.0,
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
    "fungal":         [(105, 80, 55),   (130, 100, 72),  (80, 60, 40)],
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
    "alpine_mountain", "rocky_mountain", "tundra", "canyon",
}

STABLE_SEARCH_RADIUS = 6   # blocks from each horse to look for STABLE_BLOCK


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

        self.traits["speed_rating"]  = round(random.uniform(0.7, 1.3), 3)
        self.traits["stamina_max"]   = round(random.uniform(0.8, 1.2), 3)
        self.traits["temperament"]   = random.choices(
            ["calm", "spirited", "wild"], weights=[3, 4, 3]
        )[0]
        self.traits["coat_color"]    = random.choice(coat_options)
        self.traits["horseshoe_applied"] = False

        self.stamina    = 100.0
        self.rider      = None       # Player ref when mounted
        self._broken    = False      # True once horse-breaking minigame passed
        self._flee_timer = 0.0       # flee after being attacked

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
        if not (self.tamed and other.tamed):
            return None
        if not (self._stable_nearby(world) or other._stable_nearby(world)):
            return None

        offspring = Horse((self.x + other.x) / 2, (self.y + other.y) / 2, world)

        # Base genetics crossover (mirrors Animal._breed)
        cs_a = self.traits["color_shift"]
        cs_b = other.traits["color_shift"]
        offspring.traits["color_shift"] = tuple(
            max(-0.25, min(0.25, (cs_a[i] + cs_b[i]) / 2 + random.uniform(-0.03, 0.03)))
            for i in range(3)
        )
        sz = (self.traits["size"] + other.traits["size"]) / 2 + random.uniform(-0.02, 0.02)
        offspring.traits["size"] = max(0.85, min(1.15, sz))

        mut_a = self.traits.get("mutation")
        mut_b = other.traits.get("mutation")
        offspring_mutation = None
        if mut_a is not None and mut_a == mut_b:
            if random.random() < MUTATION_INHERIT_BOTH:
                offspring_mutation = mut_a
        elif mut_a is not None or mut_b is not None:
            source = mut_a if mut_a is not None else mut_b
            if random.random() < MUTATION_INHERIT_ONE:
                offspring_mutation = source
        if offspring_mutation is None and random.random() < MUTATION_CHANCE:
            offspring_mutation = random.choice(MUTATION_TYPES)
        offspring.traits["mutation"] = offspring_mutation

        # Horse-specific trait crossover
        sr = (self.traits["speed_rating"] + other.traits["speed_rating"]) / 2
        sr += random.uniform(-0.04, 0.04)
        offspring.traits["speed_rating"] = round(max(0.6, min(1.4, sr)), 3)

        sm = (self.traits["stamina_max"] + other.traits["stamina_max"]) / 2
        sm += random.uniform(-0.03, 0.03)
        offspring.traits["stamina_max"] = round(max(0.7, min(1.3, sm)), 3)

        order = ["calm", "spirited", "wild"]
        avg_idx = (order.index(self.traits["temperament"]) +
                   order.index(other.traits["temperament"])) / 2
        if getattr(player, "horse_breeding_mastery", False):
            avg_idx = max(0.0, avg_idx - 0.5)
        avg_idx += random.uniform(-0.5, 0.5)
        offspring.traits["temperament"] = order[max(0, min(2, round(avg_idx)))]

        # Coat blend with small noise
        ca, cb = self.traits["coat_color"], other.traits["coat_color"]
        blended = tuple(max(0, min(255, int((ca[i] + cb[i]) / 2) + random.randint(-8, 8)))
                        for i in range(3))
        offspring.traits["coat_color"] = blended

        offspring.traits["horseshoe_applied"] = False
        offspring.parent_a_uid = self.uid
        offspring.parent_b_uid = other.uid
        offspring.tamed  = True
        offspring._broken = True
        offspring._breed_cooldown = 9999.0

        cooldown = 900.0
        self._breed_cooldown  = cooldown
        other._breed_cooldown = cooldown

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

        # Keep breed cooldown high to prevent auto-breed
        if self._breed_cooldown < 9999.0:
            self._breed_cooldown = 9999.0

        # Rider drives position — skip all locomotion
        if self.rider is not None:
            return

        # Flee when attacked or player too close while wild
        if self._flee_timer > 0:
            self._flee_timer -= dt
            self.vx = self.facing * HORSE_FLEE_SPEED
            self.vy = min(self.vy + GRAVITY, MAX_FALL)
            self._move_x(self.vx)
            self._move_y(self.vy)
            return

        # Wild horse flees from nearby player
        if not self.tamed:
            player = getattr(self.world, '_player_ref', None)
            if player is not None:
                pdx = (player.x + PLAYER_W / 2) - (self.x + self.W / 2)
                pdy = (player.y + PLAYER_H / 2) - (self.y + self.H / 2)
                dist = ((pdx / BLOCK_SIZE) ** 2 + (pdy / BLOCK_SIZE) ** 2) ** 0.5
                if dist < HORSE_FLEE_RADIUS:
                    self.vx = (-1 if pdx > 0 else 1) * HORSE_FLEE_SPEED
                    self.facing = 1 if self.vx > 0 else -1
                    self.vy = min(self.vy + GRAVITY, MAX_FALL)
                    self._move_x(self.vx)
                    self._move_y(self.vy)
                    return

        # Tamed: follow player
        if self.tamed:
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

        self.vy = min(self.vy + GRAVITY, MAX_FALL)
        self._move_x(self.vx)
        self._move_y(self.vy)
