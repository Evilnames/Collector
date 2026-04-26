import random
import uuid
import pygame
from constants import BLOCK_SIZE, GRAVITY, JUMP_FORCE, MAX_FALL, PLAYER_W, PLAYER_H, MINE_REACH, HOTBAR_SIZE
from blocks import LADDER, WOOD_FENCE, IRON_FENCE, WATER

ANIMAL_MOVE_SPEED = 1.2
ANIMAL_CLIMB_SPEED = 1.5

MUTATION_TYPES = ["albino", "giant", "miniature", "golden"]

# Dominance order — index 0 = dominant, higher index = more recessive
COAT_PATTERN_ORDER  = ["solid", "dappled", "spotted", "blanket"]
LEG_MARKING_ORDER   = ["none", "socks", "stockings"]
WOOL_COLOR_ORDER    = ["white", "grey", "brown", "black"]
MANE_COLOR_ORDER    = ["match", "flaxen", "silver", "dark"]
FACE_MARKING_ORDER  = ["none", "star", "blaze", "stripe"]
HIDE_ORDER          = ["solid", "spotted", "belted", "piebald"]
GOAT_COLOR_ORDER    = ["tan", "white", "brown", "black"]
PLUMAGE_ORDER       = ["white", "yellow", "brown", "black"]
BIRTH_ORDER         = ["single", "twin"]    # twin fully recessive


def _expressed_categorical(allele_pair, order):
    """Return whichever allele is more dominant (lowest index in order list)."""
    a, b = allele_pair
    ai = order.index(a) if a in order else len(order)
    bi = order.index(b) if b in order else len(order)
    return order[min(ai, bi)]


class Animal:
    def __init__(self, x, y, world, animal_id):
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.world = world
        self.on_ground = False
        self.facing = 1  # 1=right, -1=left
        self.animal_id = animal_id
        self._wander_timer = random.uniform(0.5, 3.0)
        self._wander_dir = random.choice([-1, 0, 0, 1])
        self._harvest_time = 0.0
        self.being_harvested = False

        # Genetics
        self.uid = str(uuid.uuid4())
        self.parent_a_uid = None
        self.parent_b_uid = None
        self.no_breed = False
        self.genotype = {}
        self.traits = {
            "color_shift": (
                random.uniform(-0.20, 0.20),
                random.uniform(-0.20, 0.20),
                random.uniform(-0.20, 0.20),
            ),
            "size": random.uniform(0.87, 1.13),
            "productivity": random.uniform(0.80, 1.20),
            "mutation": None,
        }
        self._init_base_genotype()

        # Health / death
        self.health = 3
        self.dead = False
        self._kill_timer = 0.0

        # Breeding
        self._breed_cooldown = random.uniform(300.0, 900.0)

        # Taming
        self.tamed = False
        self.tame_progress = 0

    # Subclasses define these as class attributes
    ANIMAL_W = 0
    ANIMAL_H = 0
    PREFERRED_FOODS = ()
    MEAT_DROP = ("raw_mutton", 1)

    @property
    def W(self):
        mut = self.traits.get("mutation")
        if mut == "giant":
            s = 1.4
        elif mut == "miniature":
            s = 0.6
        else:
            s = self.traits.get("size", 1.0)
        return int(self.ANIMAL_W * s)

    @property
    def H(self):
        mut = self.traits.get("mutation")
        if mut == "giant":
            s = 1.4
        elif mut == "miniature":
            s = 0.6
        else:
            s = self.traits.get("size", 1.0)
        return int(self.ANIMAL_H * s)

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.W, self.H)

    def _has_jump_clearance(self):
        left  = int(self.x // BLOCK_SIZE)
        right = int((self.x + self.W - 1) // BLOCK_SIZE)
        top   = int(self.y // BLOCK_SIZE)
        for bx in range(left, right + 1):
            if self.world.is_solid(bx, top - 1):
                return False
        return True

    def _move_x(self, dx):
        self.x += dx
        if self._collides():
            hit_fence = self._collides_with_fence()
            self.x -= dx
            self.vx = 0.0
            if self.on_ground and not hit_fence and self._has_jump_clearance():
                self.vy = JUMP_FORCE
            else:
                self._wander_dir = -self._wander_dir

    def _move_y(self, dy):
        self.y += dy
        if self._collides() or (dy > 0 and self._feet_in_water()):
            self.y -= dy
            self.vy = 0.0
            if dy > 0:
                self.on_ground = True
        else:
            if dy > 0:
                self.on_ground = False

    def _collides(self):
        left  = int(self.x // BLOCK_SIZE)
        right = int((self.x + self.W - 1) // BLOCK_SIZE)
        top   = int(self.y // BLOCK_SIZE)
        bot   = int((self.y + self.H - 1) // BLOCK_SIZE)
        for bx in range(left, right + 1):
            for by in range(top, bot + 1):
                if self.world.is_solid(bx, by):
                    return True
        return False

    def _collides_with_fence(self):
        left  = int(self.x // BLOCK_SIZE)
        right = int((self.x + self.W - 1) // BLOCK_SIZE)
        top   = int(self.y // BLOCK_SIZE)
        bot   = int((self.y + self.H - 1) // BLOCK_SIZE)
        for bx in range(left, right + 1):
            for by in range(top, bot + 1):
                bid = self.world.get_block(bx, by)
                if bid in (WOOD_FENCE, IRON_FENCE):
                    return True
        return False

    def _fence_in_direction(self, direction):
        self.x += direction
        result = self._collides_with_fence()
        self.x -= direction
        return result

    def _in_ladder(self):
        left  = int(self.x // BLOCK_SIZE)
        right = int((self.x + self.W - 1) // BLOCK_SIZE)
        top   = int(self.y // BLOCK_SIZE)
        bot   = int((self.y + self.H - 1) // BLOCK_SIZE)
        for bx in range(left, right + 1):
            for by in range(top, bot + 1):
                if self.world.get_block(bx, by) == LADDER:
                    return True
        return False

    def _feet_in_water(self):
        left = int(self.x // BLOCK_SIZE)
        right = int((self.x + self.W - 1) // BLOCK_SIZE)
        bot = int((self.y + self.H - 1) // BLOCK_SIZE)
        for bx in range(left, right + 1):
            if self.world.get_block(bx, bot) == WATER:
                return True
        return False

    def _in_water(self):
        left  = int(self.x // BLOCK_SIZE)
        right = int((self.x + self.W - 1) // BLOCK_SIZE)
        top   = int(self.y // BLOCK_SIZE)
        bot   = int((self.y + self.H - 1) // BLOCK_SIZE)
        for bx in range(left, right + 1):
            for by in range(top, bot + 1):
                if self.world.get_block(bx, by) == WATER:
                    return True
        return False

    def update(self, dt):
        if self.dead:
            return

        # Breeding cooldown
        self._breed_cooldown -= dt
        if (self._breed_cooldown <= 0
                and self.on_ground
                and not self.being_harvested
                and not self.no_breed):
            same = [e for e in self.world.entities
                    if type(e) is type(self) and not e.dead]
            if len(same) < 500:
                for other in same:
                    if other is self or other._breed_cooldown > 0 or other.no_breed:
                        continue
                    dx = (self.x + self.W / 2 - other.x - other.W / 2) / BLOCK_SIZE
                    dy = (self.y + self.H / 2 - other.y - other.H / 2) / BLOCK_SIZE
                    if (dx * dx + dy * dy) ** 0.5 <= 3.0:
                        self._breed(other, self.world)
                        break

        # Tamed: follow player instead of wandering
        if self.tamed:
            player = getattr(self.world, '_player_ref', None)
            if player is not None:
                pdx = (player.x + PLAYER_W / 2) - (self.x + self.W / 2)
                pdy = (player.y + PLAYER_H / 2) - (self.y + self.H / 2)
                dist = ((pdx / BLOCK_SIZE) ** 2 + (pdy / BLOCK_SIZE) ** 2) ** 0.5
                if dist > 2.5:
                    desired_dir = 1 if pdx > 0 else -1
                    if self._fence_in_direction(desired_dir):
                        self.vx = 0.0
                    else:
                        self.vx = ANIMAL_MOVE_SPEED * desired_dir
                else:
                    self.vx = 0.0
                if self.vx != 0:
                    self.facing = 1 if self.vx > 0 else -1
                if self._in_ladder():
                    if self.vx != 0:
                        self.vy = -ANIMAL_CLIMB_SPEED
                    else:
                        self.vy = 0
                elif self._in_water():
                    self.vy = min(self.vy + GRAVITY * 0.2, 2.5)
                    self.vx *= 0.8
                else:
                    self.vy = min(self.vy + GRAVITY, MAX_FALL)
                self._move_x(self.vx)
                self._move_y(self.vy)
                return  # skip wander

        # Normal wander
        self._wander_timer -= dt
        if self._wander_timer <= 0:
            self._wander_timer = random.uniform(1.5, 5.0)
            self._wander_dir = random.choice([-1, -1, 0, 0, 0, 1, 1])

        self.vx = self._wander_dir * ANIMAL_MOVE_SPEED
        if self.vx != 0:
            self.facing = 1 if self.vx > 0 else -1

        if self._in_ladder():
            if self.vx != 0:
                self.vy = -ANIMAL_CLIMB_SPEED
            else:
                self.vy = 0
        elif self._in_water():
            self.vy = min(self.vy + GRAVITY * 0.2, 2.5)
            self.vx *= 0.8
        else:
            self.vy = min(self.vy + GRAVITY, MAX_FALL)
        self._move_x(self.vx)
        self._move_y(self.vy)

    def _breed(self, other, world):
        cls = type(self)
        offspring = cls((self.x + other.x) / 2, (self.y + other.y) / 2, world)

        # Inherit allele-based genotype from both parents
        offspring._inherit_genotype(self, other)

        # color_shift stays blended (not allele-based)
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

        offspring.parent_a_uid = self.uid
        offspring.parent_b_uid = other.uid
        offspring.tamed = self.tamed and other.tamed
        offspring._breed_cooldown = 300.0 if offspring.traits.get("mutation") == "miniature" else 600.0
        self._breed_cooldown = 600.0
        other._breed_cooldown = 600.0
        world.entities.append(offspring)

        # Remove the most distant un-tamed animal of this type so the
        # population doesn't grow unboundedly and crowded areas stay playable.
        player = getattr(world, '_player_ref', None)
        if player is not None:
            pcx = player.x + PLAYER_W / 2
            pcy = player.y + PLAYER_H / 2
            candidates = [
                e for e in world.entities
                if type(e) is type(self) and not e.dead and not e.tamed
                and e is not offspring
            ]
            if candidates:
                farthest = max(
                    candidates,
                    key=lambda e: (e.x + e.W / 2 - pcx) ** 2 + (e.y + e.H / 2 - pcy) ** 2
                )
                farthest.dead = True

    # ------------------------------------------------------------------
    # Genetics helpers
    # ------------------------------------------------------------------

    def _init_base_genotype(self):
        """Set up base allele pairs from current trait values."""
        v = self.traits["size"]
        self.genotype["size_gene"] = [
            round(random.uniform(max(0.7, v - 0.1), min(1.3, v + 0.1)), 3),
            round(random.uniform(max(0.7, v - 0.1), min(1.3, v + 0.1)), 3),
        ]
        p = self.traits["productivity"]
        self.genotype["productivity_gene"] = [
            round(random.uniform(max(0.6, p - 0.15), min(1.4, p + 0.15)), 3),
            round(random.uniform(max(0.6, p - 0.15), min(1.4, p + 0.15)), 3),
        ]
        # Mutation gene: wild animals are rarely carriers (~5%)
        self.genotype["mutation"] = [None, None]
        if random.random() < 0.05:
            self.genotype["mutation"] = [None, random.choice(MUTATION_TYPES)]

    def _inherit_genotype(self, parent_a, parent_b):
        """Mendelian inheritance: pick one allele from each parent per gene."""
        for gene in parent_a.genotype:
            if gene not in parent_b.genotype:
                continue
            self.genotype[gene] = [
                random.choice(parent_a.genotype[gene]),
                random.choice(parent_b.genotype[gene]),
            ]
        # 3% chance one mutation allele spontaneously mutates
        if "mutation" in self.genotype and random.random() < 0.03:
            self.genotype["mutation"][random.randint(0, 1)] = random.choice(MUTATION_TYPES)
        self._apply_genotype_to_traits()

    def _apply_genotype_to_traits(self):
        """Sync expressed traits from genotype (phenotype computation)."""
        if "size_gene" in self.genotype:
            avg = (self.genotype["size_gene"][0] + self.genotype["size_gene"][1]) / 2
            self.traits["size"] = round(max(0.85, min(1.15, avg)), 3)
        if "productivity_gene" in self.genotype:
            avg = (self.genotype["productivity_gene"][0] + self.genotype["productivity_gene"][1]) / 2
            self.traits["productivity"] = round(max(0.7, min(1.3, avg)), 3)
        if "mutation" in self.genotype:
            a, b = self.genotype["mutation"]
            # Mutation only expresses when homozygous (both alleles match)
            self.traits["mutation"] = a if (a == b and a is not None) else None
        if self.traits.get("mutation") == "albino":
            self.traits["color_shift"] = (
                random.uniform(0.20, 0.25),
                random.uniform(0.20, 0.25),
                random.uniform(0.20, 0.25),
            )

    def _synthesize_genotype_from_traits(self):
        """Build genotype from saved traits — used when loading pre-genetics saves."""
        v = self.traits.get("size", 1.0)
        noise = random.uniform(-0.04, 0.04)
        self.genotype["size_gene"] = [round(max(0.7, v + noise), 3), round(max(0.7, v - noise), 3)]
        v = self.traits.get("productivity", 1.0)
        noise = random.uniform(-0.06, 0.06)
        self.genotype["productivity_gene"] = [round(max(0.6, v + noise), 3), round(max(0.6, v - noise), 3)]
        mut = self.traits.get("mutation")
        self.genotype["mutation"] = [mut, mut] if mut else [None, None]

    def in_range(self, player):
        acx = (self.x + self.W / 2) / BLOCK_SIZE
        acy = (self.y + self.H / 2) / BLOCK_SIZE
        pcx = (player.x + PLAYER_W / 2) / BLOCK_SIZE
        pcy = (player.y + PLAYER_H / 2) / BLOCK_SIZE
        return ((acx - pcx) ** 2 + (acy - pcy) ** 2) ** 0.5 <= MINE_REACH

    def try_harvest(self, player, dt):
        if self.dead:
            self.reset_harvest()
            return None
        tool = player.hotbar[player.selected_slot]
        if tool == "hunting_knife":
            self._kill_timer += dt
            self.being_harvested = True
            if self._kill_timer >= 0.5:
                self._kill_timer = 0.0
                self.health -= 1
                if self.health <= 0:
                    self.dead = True
                    self.reset_harvest()
                    item_id, base_count = self.MEAT_DROP
                    count = base_count + (1 if self.traits.get("mutation") == "giant" else 0)
                    return [(item_id, count)]
            return None
        return self._try_harvest_resource(player, dt)

    def _try_harvest_resource(self, player, dt):
        raise NotImplementedError

    def try_feed(self, player):
        if self.tamed:
            return False
        item_id = player.hotbar[player.selected_slot]
        if not item_id or item_id not in self.PREFERRED_FOODS:
            return False
        if player.inventory.get(item_id, 0) <= 0:
            return False
        player.inventory[item_id] -= 1
        if player.inventory[item_id] <= 0:
            del player.inventory[item_id]
            for i in range(HOTBAR_SIZE):
                if player.hotbar[i] == item_id:
                    player.hotbar[i] = None
                    break
        threshold = 2 if self.traits.get("mutation") == "albino" else 3
        self.tame_progress += 1
        if self.tame_progress >= threshold:
            self.tamed = True
        return True

    def reset_harvest(self):
        self._harvest_time = 0.0
        self._kill_timer = 0.0
        self.being_harvested = False


class Sheep(Animal):
    ANIMAL_W = 24
    ANIMAL_H = 18
    HARVEST_TIME = 1.5
    REGROW_TIME  = 30.0
    MILK_REFILL_TIME = 25.0
    MEAT_DROP = ("raw_mutton", 2)
    PREFERRED_FOODS = ("wheat", "carrot")

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "sheep")
        self.has_wool  = True
        self.has_milk  = True
        self._regrow_timer = 0.0
        self._milk_refill_timer = 0.0
        self._init_sheep_genotype()

    def _init_sheep_genotype(self):
        self.genotype["wool_color_gene"] = [
            random.choices(WOOL_COLOR_ORDER, weights=[55, 25, 15, 5])[0],
            random.choices(WOOL_COLOR_ORDER, weights=[55, 25, 15, 5])[0],
        ]
        self.genotype["fleece_gene"] = [
            round(random.uniform(0.8, 1.2), 3),
            round(random.uniform(0.8, 1.2), 3),
        ]
        # twin is fully recessive — rare in wild population
        self.genotype["birth_gene"] = [
            "single",
            "twin" if random.random() < 0.08 else "single",
        ]
        self._apply_genotype_to_traits()

    def _apply_genotype_to_traits(self):
        super()._apply_genotype_to_traits()
        if "wool_color_gene" in self.genotype:
            self.traits["wool_color"] = _expressed_categorical(
                self.genotype["wool_color_gene"], WOOL_COLOR_ORDER
            )
        if "fleece_gene" in self.genotype:
            avg = (self.genotype["fleece_gene"][0] + self.genotype["fleece_gene"][1]) / 2
            self.traits["fleece"] = round(max(0.7, min(1.3, avg)), 3)
        if "birth_gene" in self.genotype:
            self.traits["birth"] = _expressed_categorical(self.genotype["birth_gene"], BIRTH_ORDER)

    def _synthesize_genotype_from_traits(self):
        super()._synthesize_genotype_from_traits()
        wc = self.traits.get("wool_color", "white")
        self.genotype["wool_color_gene"] = [wc, wc]
        v = self.traits.get("fleece", self.traits.get("productivity", 1.0))
        noise = random.uniform(-0.04, 0.04)
        self.genotype["fleece_gene"] = [round(max(0.7, v + noise), 3), round(max(0.7, v - noise), 3)]
        b = self.traits.get("birth", "single")
        self.genotype["birth_gene"] = [b, b]

    def _breed(self, other, world):
        super()._breed(other, world)
        # Twin gene: when expressed, 60% chance of a second lamb
        offspring = next(
            (e for e in reversed(world.entities)
             if getattr(e, 'parent_a_uid', None) == self.uid and not e.dead),
            None
        )
        if offspring and offspring.traits.get("birth") == "twin" and random.random() < 0.6:
            twin = Sheep((self.x + other.x) / 2, (self.y + other.y) / 2, world)
            twin._inherit_genotype(self, other)
            cs_a = self.traits["color_shift"]
            cs_b = other.traits["color_shift"]
            twin.traits["color_shift"] = tuple(
                max(-0.25, min(0.25, (cs_a[i] + cs_b[i]) / 2 + random.uniform(-0.03, 0.03)))
                for i in range(3)
            )
            twin.parent_a_uid = self.uid
            twin.parent_b_uid = other.uid
            twin.tamed = self.tamed and other.tamed
            twin._breed_cooldown = 600.0
            world.entities.append(twin)

    def update(self, dt):
        super().update(dt)
        if self.dead:
            return
        if not self.has_wool:
            self._regrow_timer -= dt
            if self._regrow_timer <= 0:
                self.has_wool = True
        if not self.has_milk:
            self._milk_refill_timer -= dt
            if self._milk_refill_timer <= 0:
                self.has_milk = True

    def _try_harvest_resource(self, player, dt):
        tool = player.hotbar[player.selected_slot]
        if tool == "shears":
            if not self.has_wool:
                self.reset_harvest()
                return None
            self._harvest_time += dt
            self.being_harvested = True
            if self._harvest_time >= self.HARVEST_TIME:
                self.reset_harvest()
                self.has_wool = False
                self._regrow_timer = self.REGROW_TIME
                fleece = self.traits.get("fleece", self.traits.get("productivity", 1.0))
                mut    = self.traits.get("mutation")
                count  = max(1, round(random.randint(1, 3) * fleece))
                if mut == "giant":
                    count += 1
                drops = [("wool", count)]
                if mut == "golden":
                    drops.append(("golden_wool", 1))
                return drops
        elif tool == "bucket":
            if not self.has_milk:
                self.reset_harvest()
                return None
            self._harvest_time += dt
            self.being_harvested = True
            if self._harvest_time >= self.HARVEST_TIME:
                self.reset_harvest()
                self.has_milk = False
                self._milk_refill_timer = self.MILK_REFILL_TIME
                prod = self.traits.get("productivity", 1.0)
                mut  = self.traits.get("mutation")
                count = max(1, round(prod))
                if mut == "giant":
                    count += 1
                drops = [("sheep_milk", count)]
                if mut == "golden":
                    drops.append(("golden_milk", 1))
                return drops
        else:
            self.reset_harvest()
        return None


class Goat(Animal):
    ANIMAL_W = 22
    ANIMAL_H = 18
    HARVEST_TOOL = "bucket"
    HARVEST_TIME = 1.5
    REFILL_TIME  = 25.0
    MEAT_DROP    = ("raw_mutton", 1)
    PREFERRED_FOODS = ("wheat", "carrot")

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "goat")
        self.has_milk = True
        self._refill_timer = 0.0
        self._init_goat_genotype()

    def _init_goat_genotype(self):
        self.genotype["milk_richness_gene"] = [
            round(random.uniform(0.8, 1.2), 3),
            round(random.uniform(0.8, 1.2), 3),
        ]
        self.genotype["coat_color_gene"] = [
            random.choices(GOAT_COLOR_ORDER, weights=[50, 20, 20, 10])[0],
            random.choices(GOAT_COLOR_ORDER, weights=[50, 20, 20, 10])[0],
        ]
        self._apply_genotype_to_traits()

    def _apply_genotype_to_traits(self):
        super()._apply_genotype_to_traits()
        if "milk_richness_gene" in self.genotype:
            avg = (self.genotype["milk_richness_gene"][0] + self.genotype["milk_richness_gene"][1]) / 2
            self.traits["milk_richness"] = round(max(0.7, min(1.3, avg)), 3)
        if "coat_color_gene" in self.genotype:
            self.traits["coat_color"] = _expressed_categorical(self.genotype["coat_color_gene"], GOAT_COLOR_ORDER)

    def _synthesize_genotype_from_traits(self):
        super()._synthesize_genotype_from_traits()
        v = self.traits.get("milk_richness", self.traits.get("productivity", 1.0))
        noise = random.uniform(-0.04, 0.04)
        self.genotype["milk_richness_gene"] = [round(max(0.7, v + noise), 3), round(max(0.7, v - noise), 3)]
        cc = self.traits.get("coat_color", "tan")
        self.genotype["coat_color_gene"] = [cc, cc]

    def update(self, dt):
        super().update(dt)
        if self.dead:
            return
        if not self.has_milk:
            self._refill_timer -= dt
            if self._refill_timer <= 0:
                self.has_milk = True

    def _try_harvest_resource(self, player, dt):
        if not self.has_milk:
            self.reset_harvest()
            return None
        tool = player.hotbar[player.selected_slot]
        if tool != self.HARVEST_TOOL:
            self.reset_harvest()
            return None
        self._harvest_time += dt
        self.being_harvested = True
        if self._harvest_time >= self.HARVEST_TIME:
            self.reset_harvest()
            self.has_milk = False
            self._refill_timer = self.REFILL_TIME
            richness = self.traits.get("milk_richness", self.traits.get("productivity", 1.0))
            mut      = self.traits.get("mutation")
            count    = max(1, round(richness))
            if mut == "giant":
                count += 1
            drops = [("goat_milk", count)]
            if mut == "golden":
                drops.append(("golden_milk", 1))
            return drops
        return None


class Cow(Animal):
    ANIMAL_W = 30
    ANIMAL_H = 20
    HARVEST_TOOL = "bucket"
    HARVEST_TIME = 1.5
    REFILL_TIME = 20.0
    MEAT_DROP = ("raw_beef", 2)
    PREFERRED_FOODS = ("wheat", "apple")

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "cow")
        self.has_milk = True
        self._refill_timer = 0.0
        self._init_cow_genotype()

    def _init_cow_genotype(self):
        self.genotype["milk_richness_gene"] = [
            round(random.uniform(0.8, 1.2), 3),
            round(random.uniform(0.8, 1.2), 3),
        ]
        self.genotype["hide_gene"] = [
            random.choices(HIDE_ORDER, weights=[50, 30, 12, 8])[0],
            random.choices(HIDE_ORDER, weights=[50, 30, 12, 8])[0],
        ]
        self._apply_genotype_to_traits()

    def _apply_genotype_to_traits(self):
        super()._apply_genotype_to_traits()
        if "milk_richness_gene" in self.genotype:
            avg = (self.genotype["milk_richness_gene"][0] + self.genotype["milk_richness_gene"][1]) / 2
            self.traits["milk_richness"] = round(max(0.7, min(1.3, avg)), 3)
        if "hide_gene" in self.genotype:
            self.traits["hide"] = _expressed_categorical(self.genotype["hide_gene"], HIDE_ORDER)

    def _synthesize_genotype_from_traits(self):
        super()._synthesize_genotype_from_traits()
        v = self.traits.get("milk_richness", self.traits.get("productivity", 1.0))
        noise = random.uniform(-0.04, 0.04)
        self.genotype["milk_richness_gene"] = [round(max(0.7, v + noise), 3), round(max(0.7, v - noise), 3)]
        h = self.traits.get("hide", "solid")
        self.genotype["hide_gene"] = [h, h]

    def update(self, dt):
        super().update(dt)
        if self.dead:
            return
        if not self.has_milk:
            self._refill_timer -= dt
            if self._refill_timer <= 0:
                self.has_milk = True

    def _try_harvest_resource(self, player, dt):
        if not self.has_milk:
            self.reset_harvest()
            return None
        tool = player.hotbar[player.selected_slot]
        if tool != self.HARVEST_TOOL:
            self.reset_harvest()
            return None
        self._harvest_time += dt
        self.being_harvested = True
        if self._harvest_time >= self.HARVEST_TIME:
            self.reset_harvest()
            self.has_milk = False
            self._refill_timer = self.REFILL_TIME
            richness = self.traits.get("milk_richness", self.traits.get("productivity", 1.0))
            mut      = self.traits.get("mutation")
            count    = max(1, round(richness))
            if mut == "giant":
                count += 1
            drops = [("milk", count)]
            if mut == "golden":
                drops.append(("golden_milk", 1))
            return drops
        return None


class Chicken(Animal):
    ANIMAL_W = 18
    ANIMAL_H = 16
    HARVEST_TOOL = None  # collected empty-handed
    HARVEST_TIME = 1.0
    REFILL_TIME = 30.0
    MEAT_DROP = ("raw_chicken", 1)
    PREFERRED_FOODS = ("corn", "pea")

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "chicken")
        self.has_egg = True
        self._refill_timer = 0.0
        self._init_chicken_genotype()

    def _init_chicken_genotype(self):
        self.genotype["lay_rate_gene"] = [
            round(random.uniform(0.8, 1.2), 3),
            round(random.uniform(0.8, 1.2), 3),
        ]
        self.genotype["plumage_gene"] = [
            random.choices(PLUMAGE_ORDER, weights=[40, 25, 25, 10])[0],
            random.choices(PLUMAGE_ORDER, weights=[40, 25, 25, 10])[0],
        ]
        self._apply_genotype_to_traits()

    def _apply_genotype_to_traits(self):
        super()._apply_genotype_to_traits()
        if "lay_rate_gene" in self.genotype:
            avg = (self.genotype["lay_rate_gene"][0] + self.genotype["lay_rate_gene"][1]) / 2
            self.traits["lay_rate"] = round(max(0.7, min(1.3, avg)), 3)
        if "plumage_gene" in self.genotype:
            self.traits["plumage"] = _expressed_categorical(self.genotype["plumage_gene"], PLUMAGE_ORDER)

    def _synthesize_genotype_from_traits(self):
        super()._synthesize_genotype_from_traits()
        v = self.traits.get("lay_rate", self.traits.get("productivity", 1.0))
        noise = random.uniform(-0.04, 0.04)
        self.genotype["lay_rate_gene"] = [round(max(0.7, v + noise), 3), round(max(0.7, v - noise), 3)]
        p = self.traits.get("plumage", "white")
        self.genotype["plumage_gene"] = [p, p]

    def update(self, dt):
        super().update(dt)
        if self.dead:
            return
        if not self.has_egg:
            self._refill_timer -= dt
            if self._refill_timer <= 0:
                self.has_egg = True

    def _try_harvest_resource(self, player, dt):
        if not self.has_egg:
            self.reset_harvest()
            return None
        self._harvest_time += dt
        self.being_harvested = True
        if self._harvest_time >= self.HARVEST_TIME:
            self.reset_harvest()
            self.has_egg = False
            lay_rate = self.traits.get("lay_rate", 1.0)
            self._refill_timer = max(5.0, self.REFILL_TIME / lay_rate)
            prod  = self.traits.get("productivity", 1.0)
            mut   = self.traits.get("mutation")
            count = max(1, round(prod))
            if mut == "giant":
                count += 1
            drops = [("egg", count)]
            if mut == "golden":
                drops.append(("golden_egg", 1))
            return drops
        return None


BIG_CAT_FLEE_RADIUS = 7   # blocks
BIG_CAT_FLEE_SPEED  = 2.6


class BigCat(Animal):
    """Base class for rare, unhuntable big cats that flee from the player."""
    ANIMAL_W = 36
    ANIMAL_H = 20
    PREFERRED_FOODS = ()
    MEAT_DROP = (None, 0)

    def __init__(self, x, y, world, animal_id):
        super().__init__(x, y, world, animal_id)

    def try_harvest(self, player, dt):
        self.reset_harvest()
        return None

    def _try_harvest_resource(self, player, dt):
        return None

    def _breed(self, other, world):
        pass

    def update(self, dt):
        if self.dead:
            return

        player = getattr(self.world, '_player_ref', None)
        if player is not None:
            pdx = (player.x + PLAYER_W / 2) - (self.x + self.W / 2)
            pdy = (player.y + PLAYER_H / 2) - (self.y + self.H / 2)
            dist = ((pdx / BLOCK_SIZE) ** 2 + (pdy / BLOCK_SIZE) ** 2) ** 0.5
            if dist < BIG_CAT_FLEE_RADIUS:
                flee_dir = -1 if pdx > 0 else 1
                self.vx = flee_dir * BIG_CAT_FLEE_SPEED
                self.facing = 1 if self.vx > 0 else -1
                self.vy = min(self.vy + GRAVITY, MAX_FALL)
                self._move_x(self.vx)
                self._move_y(self.vy)
                return

        self._wander_timer -= dt
        if self._wander_timer <= 0:
            self._wander_timer = random.uniform(2.0, 8.0)
            self._wander_dir = random.choice([-1, -1, 0, 0, 0, 1, 1])

        self.vx = self._wander_dir * ANIMAL_MOVE_SPEED
        if self.vx != 0:
            self.facing = 1 if self.vx > 0 else -1

        self.vy = min(self.vy + GRAVITY, MAX_FALL)
        self._move_x(self.vx)
        self._move_y(self.vy)


class SnowLeopard(BigCat):
    ANIMAL_W = 36
    ANIMAL_H = 20

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "snow_leopard")


class MountainLion(BigCat):
    ANIMAL_W = 38
    ANIMAL_H = 22

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "mountain_lion")


# ---------------------------------------------------------------------------
# Huntable wildlife — flee from player, killed by arrows
# ---------------------------------------------------------------------------

HUNTABLE_FLEE_RADIUS = 9    # blocks
HUNTABLE_FLEE_SPEED  = 2.2


class HuntableAnimal(Animal):
    """Prey animal: flees the player and can only be killed by arrows."""

    def __init__(self, x, y, world, animal_id):
        super().__init__(x, y, world, animal_id)
        self._stunned_timer = 0.0
        self._barbed_timer  = 0.0

    def try_harvest(self, player, dt):
        self.reset_harvest()
        return None

    def _try_harvest_resource(self, player, dt):
        return None

    def _breed(self, other, world):
        pass

    def update(self, dt):
        if self.dead:
            return
        if self._stunned_timer > 0:
            self._stunned_timer -= dt
            self.vx = 0
            self.vy = min(self.vy + GRAVITY, MAX_FALL)
            self._move_y(self.vy)
            return
        player = getattr(self.world, '_player_ref', None)
        if self._barbed_timer > 0:
            self._barbed_timer -= dt
        if player is not None:
            pdx = (player.x + PLAYER_W / 2) - (self.x + self.W / 2)
            pdy = (player.y + PLAYER_H / 2) - (self.y + self.H / 2)
            dist = ((pdx / BLOCK_SIZE) ** 2 + (pdy / BLOCK_SIZE) ** 2) ** 0.5
            if dist < HUNTABLE_FLEE_RADIUS:
                flee_dir = -1 if pdx > 0 else 1
                flee_speed = HUNTABLE_FLEE_SPEED * (0.4 if self._barbed_timer > 0 else 1.0)
                self.vx = flee_dir * flee_speed
                self.facing = 1 if self.vx > 0 else -1
                self.vy = min(self.vy + GRAVITY, MAX_FALL)
                self._move_x(self.vx)
                self._move_y(self.vy)
                return
        self._wander_timer -= dt
        if self._wander_timer <= 0:
            self._wander_timer = random.uniform(2.0, 6.0)
            self._wander_dir = random.choice([-1, -1, 0, 0, 1, 1])
        self.vx = self._wander_dir * ANIMAL_MOVE_SPEED
        if self.vx != 0:
            self.facing = 1 if self.vx > 0 else -1
        self.vy = min(self.vy + GRAVITY, MAX_FALL)
        self._move_x(self.vx)
        self._move_y(self.vy)

    def on_arrow_hit(self, damage=1, poison=False, barb=False):
        """Deal arrow damage. Returns drop list when dead, else None."""
        self.health -= damage
        if poison:
            self._stunned_timer = 3.0
        if barb:
            self._barbed_timer = 5.0
        if self.health <= 0:
            self.dead = True
            return list(self.MEAT_DROP)
        return None


class Deer(HuntableAnimal):
    ANIMAL_W = 28
    ANIMAL_H = 22
    MEAT_DROP = [("raw_venison", 2), ("deer_hide", 1), ("bone", 1)]

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "deer")
        self.health = 3


class Boar(HuntableAnimal):
    ANIMAL_W = 26
    ANIMAL_H = 18
    MEAT_DROP = [("raw_boar_meat", 2), ("bone", 1)]

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "boar")
        self.health = 3


class Rabbit(HuntableAnimal):
    ANIMAL_W = 14
    ANIMAL_H = 12
    MEAT_DROP = [("raw_rabbit", 1), ("rabbit_pelt", 1)]

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "rabbit")
        self.health = 1


class Turkey(HuntableAnimal):
    ANIMAL_W = 20
    ANIMAL_H = 18
    MEAT_DROP = [("raw_turkey", 2), ("feather", 2)]

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "turkey")
        self.health = 2


DEER_BIOMES   = {"temperate", "boreal", "birch_forest", "rolling_hills", "redwood"}
BOAR_BIOMES   = {"temperate", "jungle", "swamp", "boreal", "redwood"}
RABBIT_BIOMES = {"temperate", "boreal", "tundra", "steppe", "rolling_hills", "steep_hills"}
TURKEY_BIOMES = {"temperate", "boreal", "birch_forest", "rolling_hills"}


class Wolf(HuntableAnimal):
    ANIMAL_W = 26
    ANIMAL_H = 18
    MEAT_DROP = [("wolf_pelt", 1), ("bone", 1)]

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "wolf")
        self.health = 2


class Bear(HuntableAnimal):
    ANIMAL_W = 34
    ANIMAL_H = 26
    MEAT_DROP = [("raw_bear_meat", 3), ("bear_pelt", 1), ("bone", 2)]

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "bear")
        self.health = 4


class Duck(HuntableAnimal):
    ANIMAL_W = 16
    ANIMAL_H = 12
    MEAT_DROP = [("raw_duck", 1), ("feather", 2)]

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "duck")
        self.health = 1


class Elk(HuntableAnimal):
    ANIMAL_W = 32
    ANIMAL_H = 26
    MEAT_DROP = [("raw_venison", 3), ("elk_antler", 1), ("bone", 1)]

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "elk")
        self.health = 3


class Bison(HuntableAnimal):
    ANIMAL_W = 36
    ANIMAL_H = 24
    MEAT_DROP = [("raw_bison_meat", 3), ("bison_hide", 1), ("bone", 1)]

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "bison")
        self.health = 3


class Fox(HuntableAnimal):
    ANIMAL_W = 20
    ANIMAL_H = 14
    MEAT_DROP = [("fox_pelt", 1), ("bone", 1)]

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "fox")
        self.health = 1


WOLF_BIOMES  = {"boreal", "tundra", "birch_forest", "redwood", "alpine_mountain"}
BEAR_BIOMES  = {"boreal", "redwood", "alpine_mountain", "rocky_mountain"}
DUCK_BIOMES  = {"wetland", "swamp", "temperate"}
ELK_BIOMES   = {"boreal", "tundra", "alpine_mountain", "rocky_mountain"}
BISON_BIOMES = {"steppe", "savanna", "arid_steppe", "rolling_hills"}
FOX_BIOMES   = {"temperate", "boreal", "rolling_hills", "birch_forest"}


class Moose(HuntableAnimal):
    ANIMAL_W = 36
    ANIMAL_H = 30
    MEAT_DROP = [("raw_venison", 4), ("moose_antler", 1), ("bone", 2)]

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "moose")
        self.health = 4


class Bighorn(HuntableAnimal):
    ANIMAL_W = 24
    ANIMAL_H = 20
    MEAT_DROP = [("raw_mutton", 2), ("bighorn_horn", 1), ("bone", 1)]

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "bighorn")
        self.health = 2


class Pheasant(HuntableAnimal):
    ANIMAL_W = 18
    ANIMAL_H = 14
    MEAT_DROP = [("raw_pheasant", 1), ("feather", 3)]

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "pheasant")
        self.health = 1


class Warthog(HuntableAnimal):
    ANIMAL_W = 24
    ANIMAL_H = 16
    MEAT_DROP = [("raw_boar_meat", 2), ("warthog_tusk", 1), ("bone", 1)]

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "warthog")
        self.health = 2


class MuskOx(HuntableAnimal):
    ANIMAL_W = 32
    ANIMAL_H = 22
    MEAT_DROP = [("raw_bison_meat", 3), ("musk_ox_hide", 1), ("bone", 1)]

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "musk_ox")
        self.health = 3


class Crocodile(HuntableAnimal):
    ANIMAL_W = 40
    ANIMAL_H = 14
    MEAT_DROP = [("raw_crocodile", 2), ("croc_hide", 1), ("bone", 1)]

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "crocodile")
        self.health = 3


class Goose(HuntableAnimal):
    ANIMAL_W = 18
    ANIMAL_H = 16
    MEAT_DROP = [("raw_goose", 1), ("feather", 2)]

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "goose")
        self.health = 1


class Hare(HuntableAnimal):
    ANIMAL_W = 16
    ANIMAL_H = 14
    MEAT_DROP = [("raw_rabbit", 1), ("rabbit_pelt", 1)]
    # Hares flee faster than rabbits
    def update(self, dt):
        if self.dead:
            return
        player = getattr(self.world, '_player_ref', None)
        if player is not None:
            pdx = (player.x + PLAYER_W / 2) - (self.x + self.W / 2)
            pdy = (player.y + PLAYER_H / 2) - (self.y + self.H / 2)
            dist = ((pdx / BLOCK_SIZE) ** 2 + (pdy / BLOCK_SIZE) ** 2) ** 0.5
            if dist < HUNTABLE_FLEE_RADIUS + 3:
                flee_dir = -1 if pdx > 0 else 1
                self.vx = flee_dir * (HUNTABLE_FLEE_SPEED + 1.2)
                self.facing = 1 if self.vx > 0 else -1
                self.vy = min(self.vy + GRAVITY, MAX_FALL)
                self._move_x(self.vx)
                self._move_y(self.vy)
                return
        self._wander_timer -= dt
        if self._wander_timer <= 0:
            self._wander_timer = random.uniform(1.0, 4.0)
            self._wander_dir = random.choice([-1, -1, 0, 1, 1])
        self.vx = self._wander_dir * (ANIMAL_MOVE_SPEED + 0.5)
        if self.vx != 0:
            self.facing = 1 if self.vx > 0 else -1
        self.vy = min(self.vy + GRAVITY, MAX_FALL)
        self._move_x(self.vx)
        self._move_y(self.vy)

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "hare")
        self.health = 1


MOOSE_BIOMES    = {"boreal", "wetland", "steep_hills", "redwood"}
BIGHORN_BIOMES  = {"rocky_mountain", "alpine_mountain", "canyon", "steep_hills"}
PHEASANT_BIOMES = {"temperate", "birch_forest", "rolling_hills", "boreal"}
WARTHOG_BIOMES  = {"savanna", "arid_steppe", "steppe", "wasteland"}
MUSK_OX_BIOMES  = {"tundra", "alpine_mountain"}
CROC_BIOMES     = {"swamp", "wetland", "jungle", "tropical"}
GOOSE_BIOMES    = {"wetland", "temperate", "swamp"}
HARE_BIOMES     = {"steppe", "tundra", "arid_steppe", "wasteland"}
