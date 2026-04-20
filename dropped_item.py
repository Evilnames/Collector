from constants import BLOCK_SIZE, PLAYER_W, PLAYER_H

PICKUP_RADIUS_SQ = (BLOCK_SIZE * 1.5) ** 2
LIFETIME = 300.0  # 5 minutes


class DroppedItem:
    def __init__(self, x, y, item_id, count, lifetime=None):
        self.x = float(x)
        self.y = float(y)
        self.item_id = item_id
        self.count = count
        self._life = lifetime if lifetime is not None else LIFETIME

    def update(self, dt):
        self._life -= dt

    @property
    def expired(self):
        return self._life <= 0

    def in_range(self, player):
        dx = self.x - (player.x + PLAYER_W / 2)
        dy = self.y - (player.y + PLAYER_H / 2)
        return dx * dx + dy * dy <= PICKUP_RADIUS_SQ
