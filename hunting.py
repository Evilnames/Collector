from constants import BLOCK_SIZE, GRAVITY, MAX_FALL

ARROW_SPEED   = 9
ARROW_MAX_X   = 22 * BLOCK_SIZE   # horizontal range before despawn


class Arrow:
    W = 8
    H = 3

    def __init__(self, x, y, direction, world, damage=1,
                 speed=None, max_range=None, poison=False, extra_drops=False,
                 barb=False, color=None):
        self.x           = float(x)
        self.y           = float(y)
        self.vx          = direction * (speed or ARROW_SPEED)
        self.vy          = 0.0
        self.world       = world
        self.dead        = False
        self.damage      = damage
        self.poison      = poison
        self.extra_drops = extra_drops
        self.barb        = barb
        self.color       = color or (200, 170, 100)
        self._dist       = 0.0
        self._max_range  = max_range or ARROW_MAX_X

    def update(self):
        self.vy     = min(self.vy + GRAVITY * 0.18, MAX_FALL * 0.35)
        self.x     += self.vx
        self.y     += self.vy
        self._dist += abs(self.vx)
        if self._dist > self._max_range:
            self.dead = True
            return
        bx = int(self.x // BLOCK_SIZE)
        by = int(self.y // BLOCK_SIZE)
        if self.world.is_solid(bx, by):
            self.dead = True
