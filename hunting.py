from constants import BLOCK_SIZE, GRAVITY, MAX_FALL

ARROW_SPEED   = 9
ARROW_MAX_X   = 22 * BLOCK_SIZE   # horizontal range before despawn


class Arrow:
    W = 8
    H = 3

    def __init__(self, x, y, direction, world, damage=1):
        self.x        = float(x)
        self.y        = float(y)
        self.vx       = direction * ARROW_SPEED
        self.vy       = 0.0
        self.world    = world
        self.dead     = False
        self.damage   = damage
        self._dist    = 0.0

    def update(self):
        self.vy     = min(self.vy + GRAVITY * 0.18, MAX_FALL * 0.35)
        self.x     += self.vx
        self.y     += self.vy
        self._dist += abs(self.vx)
        if self._dist > ARROW_MAX_X:
            self.dead = True
            return
        bx = int(self.x // BLOCK_SIZE)
        by = int(self.y // BLOCK_SIZE)
        if self.world.is_solid(bx, by):
            self.dead = True
