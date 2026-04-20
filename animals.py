import random
import pygame
from constants import BLOCK_SIZE, GRAVITY, MAX_FALL, PLAYER_W, PLAYER_H, MINE_REACH

ANIMAL_MOVE_SPEED = 1.2


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

    # Subclasses define these as class attributes
    ANIMAL_W = 0
    ANIMAL_H = 0

    @property
    def W(self):
        return self.ANIMAL_W

    @property
    def H(self):
        return self.ANIMAL_H

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.W, self.H)

    def _move_x(self, dx):
        self.x += dx
        if self._collides():
            self.x -= dx
            self.vx = 0.0
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

    def update(self, dt):
        self._wander_timer -= dt
        if self._wander_timer <= 0:
            self._wander_timer = random.uniform(1.5, 5.0)
            self._wander_dir = random.choice([-1, -1, 0, 0, 0, 1, 1])

        self.vx = self._wander_dir * ANIMAL_MOVE_SPEED
        if self.vx != 0:
            self.facing = 1 if self.vx > 0 else -1

        self.vy = min(self.vy + GRAVITY, MAX_FALL)
        self._move_x(self.vx)
        self._move_y(self.vy)

    def in_range(self, player):
        acx = (self.x + self.W / 2) / BLOCK_SIZE
        acy = (self.y + self.H / 2) / BLOCK_SIZE
        pcx = (player.x + PLAYER_W / 2) / BLOCK_SIZE
        pcy = (player.y + PLAYER_H / 2) / BLOCK_SIZE
        return ((acx - pcx) ** 2 + (acy - pcy) ** 2) ** 0.5 <= MINE_REACH

    def try_harvest(self, player, dt):
        raise NotImplementedError

    def reset_harvest(self):
        self._harvest_time = 0.0
        self.being_harvested = False


class Sheep(Animal):
    ANIMAL_W = 24
    ANIMAL_H = 18
    HARVEST_TOOL = "shears"
    HARVEST_TIME = 1.5
    REGROW_TIME = 30.0

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "sheep")
        self.has_wool = True
        self._regrow_timer = 0.0

    def update(self, dt):
        super().update(dt)
        if not self.has_wool:
            self._regrow_timer -= dt
            if self._regrow_timer <= 0:
                self.has_wool = True

    def try_harvest(self, player, dt):
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

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "cow")
        self.has_milk = True
        self._refill_timer = 0.0

    def update(self, dt):
        super().update(dt)
        if not self.has_milk:
            self._refill_timer -= dt
            if self._refill_timer <= 0:
                self.has_milk = True

    def try_harvest(self, player, dt):
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

    def __init__(self, x, y, world):
        super().__init__(x, y, world, "chicken")
        self.has_egg = True
        self._refill_timer = 0.0

    def update(self, dt):
        super().update(dt)
        if not self.has_egg:
            self._refill_timer -= dt
            if self._refill_timer <= 0:
                self.has_egg = True

    def try_harvest(self, player, dt):
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
