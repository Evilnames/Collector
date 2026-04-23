import random
import uuid
import pygame
from constants import BLOCK_SIZE, GRAVITY, JUMP_FORCE, MAX_FALL, PLAYER_W, PLAYER_H, MINE_REACH, HOTBAR_SIZE
from blocks import LADDER, WOOD_FENCE, IRON_FENCE

ANIMAL_MOVE_SPEED = 1.2
ANIMAL_CLIMB_SPEED = 1.5


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
        self.traits = {
            "color_shift": (
                random.uniform(-0.20, 0.20),
                random.uniform(-0.20, 0.20),
                random.uniform(-0.20, 0.20),
            ),
            "size": random.uniform(0.87, 1.13),
        }

        # Health / death
        self.health = 3
        self.dead = False
        self._kill_timer = 0.0

        # Breeding
        self._breed_cooldown = random.uniform(60.0, 180.0)

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
        return int(self.ANIMAL_W * self.traits.get("size", 1.0))

    @property
    def H(self):
        return int(self.ANIMAL_H * self.traits.get("size", 1.0))

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.W, self.H)

    def _move_x(self, dx):
        self.x += dx
        if self._collides():
            hit_fence = self._collides_with_fence()
            self.x -= dx
            self.vx = 0.0
            if self.on_ground and not hit_fence:
                self.vy = JUMP_FORCE
            else:
                self._wander_dir = -self._wander_dir

    def _move_y(self, dy):
        self.y += dy
        if self._collides():
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

    def update(self, dt):
        if self.dead:
            return

        # Breeding cooldown
        self._breed_cooldown -= dt
        if (self._breed_cooldown <= 0
                and self.on_ground
                and not self.being_harvested):
            same = [e for e in self.world.entities
                    if type(e) is type(self) and not e.dead]
            if len(same) < 500:
                for other in same:
                    if other is self or other._breed_cooldown > 0:
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
        else:
            self.vy = min(self.vy + GRAVITY, MAX_FALL)
        self._move_x(self.vx)
        self._move_y(self.vy)

    def _breed(self, other, world):
        cls = type(self)
        offspring = cls((self.x + other.x) / 2, (self.y + other.y) / 2, world)
        cs_a = self.traits["color_shift"]
        cs_b = other.traits["color_shift"]
        offspring.traits["color_shift"] = tuple(
            max(-0.25, min(0.25,
                (cs_a[i] + cs_b[i]) / 2 + random.uniform(-0.03, 0.03)))
            for i in range(3)
        )
        sz = (self.traits["size"] + other.traits["size"]) / 2 + random.uniform(-0.02, 0.02)
        offspring.traits["size"] = max(0.85, min(1.15, sz))
        offspring.parent_a_uid = self.uid
        offspring.parent_b_uid = other.uid
        offspring.tamed = True
        offspring._breed_cooldown = 120.0
        self._breed_cooldown = 120.0
        other._breed_cooldown = 120.0
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
                    item_id, count = self.MEAT_DROP
                    return (item_id, count)
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
        self.tame_progress += 1
        if self.tame_progress >= 3:
            self.tamed = True
        return True

    def reset_harvest(self):
        self._harvest_time = 0.0
        self._kill_timer = 0.0
        self.being_harvested = False


class Sheep(Animal):
    ANIMAL_W = 24
    ANIMAL_H = 18
    HARVEST_TOOL = "shears"
    HARVEST_TIME = 1.5
    REGROW_TIME = 30.0
    MEAT_DROP = ("raw_mutton", 2)
    PREFERRED_FOODS = ("wheat", "carrot")

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "sheep")
        self.has_wool = True
        self._regrow_timer = 0.0

    def update(self, dt):
        super().update(dt)
        if self.dead:
            return
        if not self.has_wool:
            self._regrow_timer -= dt
            if self._regrow_timer <= 0:
                self.has_wool = True

    def _try_harvest_resource(self, player, dt):
        if not self.has_wool:
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
            self.has_wool = False
            self._regrow_timer = self.REGROW_TIME
            return ("wool", random.randint(1, 3))
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
            return ("milk", 1)
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
            self._refill_timer = self.REFILL_TIME
            return ("egg", 1)
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
