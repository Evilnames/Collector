from constants import BLOCK_SIZE, PLAYER_W, PLAYER_H, MINE_REACH
from blocks import AIR as _AIR, WATER as _WATER

ROW_SPEED  = 160   # px/s manual cap for rowboat
SAIL_BASE  = 70    # px/s sailboat no-wind base
SAIL_WIND  = 55    # px/s added per unit of wind_strength
SAIL_CAP   = 260   # absolute max for sailboat


class Boat:
    W = BLOCK_SIZE * 2
    H = BLOCK_SIZE

    TYPE_ROW  = "rowboat"
    TYPE_SAIL = "sailboat"

    def __init__(self, x, y, boat_type):
        self.x         = float(x)
        self.y         = float(y)
        self.boat_type = boat_type
        self.vel_x     = 0.0
        self.rider     = None

    @classmethod
    def from_dict(cls, d):
        return cls(float(d["x"]), float(d["y"]), d["boat_type"])

    def to_dict(self):
        return {"x": self.x, "y": self.y, "boat_type": self.boat_type}

    def _sail_speed(self, world):
        wind_str = world._wind_strength if world._wind_active else 0.0
        wind_dir = world._wind_dir
        dir_match = 1.0 if (self.vel_x >= 0) == (wind_dir > 0) else 0.3
        return min(SAIL_CAP, SAIL_BASE + wind_str * SAIL_WIND * dir_match)

    def go(self, direction, world=None):
        if self.boat_type == self.TYPE_ROW:
            self.vel_x = ROW_SPEED * direction
        else:
            speed = self._sail_speed(world) if world else SAIL_BASE
            self.vel_x = speed * direction

    def stop(self):
        self.vel_x = 0.0

    def update(self, dt, world):
        if self.boat_type == self.TYPE_SAIL and self.vel_x != 0:
            target = self._sail_speed(world) * (1 if self.vel_x > 0 else -1)
            self.vel_x += (target - self.vel_x) * min(1.0, dt * 1.5)

        new_x = self.x + self.vel_x * dt
        if self.vel_x != 0 and world is not None:
            water_by = int((self.y + self.H) / BLOCK_SIZE)
            if self.vel_x > 0:
                lead_bx = int((new_x + self.W) / BLOCK_SIZE)
                if world.get_block(lead_bx, water_by) not in (_AIR, _WATER):
                    new_x = lead_bx * BLOCK_SIZE - self.W
                    self.vel_x = 0.0
            else:
                lead_bx = int(new_x / BLOCK_SIZE)
                if world.get_block(lead_bx, water_by) not in (_AIR, _WATER):
                    new_x = (lead_bx + 1) * BLOCK_SIZE
                    self.vel_x = 0.0
        self.x = new_x

        if self.rider is not None:
            self.rider.x = self.x + (self.W - PLAYER_W) // 2
            self.rider.y = self.y + (self.H - PLAYER_H) // 2

    def in_range(self, player):
        cx  = (self.x + self.W / 2) / BLOCK_SIZE
        cy  = (self.y + self.H / 2) / BLOCK_SIZE
        pcx = (player.x + PLAYER_W / 2) / BLOCK_SIZE
        pcy = (player.y + PLAYER_H / 2) / BLOCK_SIZE
        return ((cx - pcx) ** 2 + (cy - pcy) ** 2) ** 0.5 <= MINE_REACH
