from constants import BLOCK_SIZE, PLAYER_W, PLAYER_H, MINE_REACH


ELEVATOR_SPEED = 200  # pixels/second — much faster than walking (MOVE_SPEED * 60 ≈ 240 max)


class ElevatorCar:
    W = BLOCK_SIZE
    H = BLOCK_SIZE * 2

    def __init__(self, shaft_x, stop_by):
        self.shaft_x = shaft_x      # block column of the cable/stop shaft
        self.car_y = float(stop_by * BLOCK_SIZE)
        self.target_y = self.car_y
        self.state = "idle"         # "idle" | "moving"
        self.rider = None           # Player ref while boarded, else None

    @classmethod
    def from_dict(cls, d):
        car = cls(d["shaft_x"], d["stop_by"])
        car.car_y = float(d["car_by"] * BLOCK_SIZE)
        car.target_y = car.car_y
        return car

    def get_stops(self, world):
        from blocks import ELEVATOR_STOP_BLOCK, ELEVATOR_CABLE_BLOCK
        _elev = {ELEVATOR_STOP_BLOCK, ELEVATOR_CABLE_BLOCK}
        car_by = int(self.car_y // BLOCK_SIZE)

        # Walk up and down to find the contiguous run of elevator blocks
        top = car_by
        while top > 0 and world.get_block(self.shaft_x, top - 1) in _elev:
            top -= 1
        bot = car_by
        while bot < world.height - 1 and world.get_block(self.shaft_x, bot + 1) in _elev:
            bot += 1

        return [by for by in range(top, bot + 1)
                if world.get_block(self.shaft_x, by) == ELEVATOR_STOP_BLOCK]

    def _path_clear(self, from_by, to_by, world):
        from blocks import ELEVATOR_STOP_BLOCK, ELEVATOR_CABLE_BLOCK
        _elev = {ELEVATOR_STOP_BLOCK, ELEVATOR_CABLE_BLOCK}
        step = 1 if to_by >= from_by else -1
        for by in range(from_by, to_by + step, step):
            if world.get_block(self.shaft_x, by) not in _elev:
                return False
        return True

    def call(self, target_by, world):
        car_by = int(round(self.car_y / BLOCK_SIZE))
        if not self._path_clear(car_by, target_by, world):
            return
        self.target_y = float(target_by * BLOCK_SIZE)
        self.state = "moving"

    def update(self, dt, world, player):
        if self.state == "moving":
            delta = ELEVATOR_SPEED * dt
            diff = self.target_y - self.car_y
            if abs(diff) <= delta:
                self.car_y = self.target_y
                self.state = "idle"
            else:
                self.car_y += delta if diff > 0 else -delta

        if self.rider is not None:
            self.rider.x = float(self.shaft_x * BLOCK_SIZE + (self.W - PLAYER_W) // 2)
            self.rider.y = self.car_y + (self.H - PLAYER_H) // 2

    def in_range(self, player):
        cx = self.shaft_x + 0.5
        cy = self.car_y / BLOCK_SIZE + 1.0
        pcx = (player.x + PLAYER_W / 2) / BLOCK_SIZE
        pcy = (player.y + PLAYER_H / 2) / BLOCK_SIZE
        return ((cx - pcx) ** 2 + (cy - pcy) ** 2) ** 0.5 <= MINE_REACH
