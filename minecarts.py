from constants import BLOCK_SIZE, PLAYER_W, PLAYER_H, MINE_REACH


MINECART_SPEED = 200  # pixels/second


class Minecart:
    W = BLOCK_SIZE
    H = BLOCK_SIZE

    def __init__(self, track_by, stop_bx):
        self.track_by = track_by        # block row of the track
        self.cart_x   = float(stop_bx * BLOCK_SIZE)
        self.target_x = self.cart_x
        self.vel_x    = 0.0             # positive = right, negative = left
        self.state    = "idle"          # "idle" | "moving" | "calling"
        self.rider    = None

    @classmethod
    def from_dict(cls, d):
        cart = cls(d["track_by"], d["stop_bx"])
        cart.cart_x   = float(d["cart_bx"] * BLOCK_SIZE)
        cart.target_x = cart.cart_x
        return cart

    def get_stops(self, world):
        from blocks import MINE_TRACK_BLOCK, MINE_TRACK_STOP_BLOCK
        _track = {MINE_TRACK_BLOCK, MINE_TRACK_STOP_BLOCK}
        cart_bx = int(self.cart_x // BLOCK_SIZE)

        left = cart_bx
        while left > 0 and world.get_block(left - 1, self.track_by) in _track:
            left -= 1
        right = cart_bx
        while right < world.width - 1 and world.get_block(right + 1, self.track_by) in _track:
            right += 1

        return [bx for bx in range(left, right + 1)
                if world.get_block(bx, self.track_by) == MINE_TRACK_STOP_BLOCK]

    def call(self, target_bx):
        self.target_x = float(target_bx * BLOCK_SIZE)
        self.state    = "calling"
        self.vel_x    = MINECART_SPEED if self.target_x >= self.cart_x else -MINECART_SPEED

    def go(self, direction):
        """Start free-moving in direction: +1 = right, -1 = left."""
        self.vel_x = MINECART_SPEED * direction
        self.state = "moving"

    def stop(self):
        self.vel_x    = 0.0
        self.state    = "idle"
        self.target_x = self.cart_x

    def update(self, dt, world):
        from blocks import MINE_TRACK_BLOCK, MINE_TRACK_STOP_BLOCK
        _track = {MINE_TRACK_BLOCK, MINE_TRACK_STOP_BLOCK}

        if self.state == "calling":
            delta = abs(self.vel_x) * dt
            diff  = self.target_x - self.cart_x
            if abs(diff) <= delta:
                self.cart_x = self.target_x
                self.stop()
            else:
                self.cart_x += self.vel_x * dt

        elif self.state == "moving":
            new_x   = self.cart_x + self.vel_x * dt
            # Check the leading edge of the cart stays on track
            if self.vel_x > 0:
                lead_bx = int((new_x + self.W - 1) // BLOCK_SIZE)
            else:
                lead_bx = int(new_x // BLOCK_SIZE)
            if world.get_block(lead_bx, self.track_by) not in _track:
                self.stop()
            else:
                self.cart_x = new_x

        if self.rider is not None:
            self.rider.x = self.cart_x + (self.W - PLAYER_W) // 2
            self.rider.y = float(self.track_by * BLOCK_SIZE) + (self.H - PLAYER_H) // 2

    @property
    def cart_y(self):
        return self.track_by * BLOCK_SIZE

    def in_range(self, player):
        cx  = self.cart_x / BLOCK_SIZE + 0.5
        cy  = self.track_by - 0.5
        pcx = (player.x + PLAYER_W / 2) / BLOCK_SIZE
        pcy = (player.y + PLAYER_H / 2) / BLOCK_SIZE
        return ((cx - pcx) ** 2 + (cy - pcy) ** 2) ** 0.5 <= MINE_REACH
