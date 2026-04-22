import random
import pygame
from blocks import BLOCKS, AIR, SUPPORT, IRON_SUPPORT, DIAMOND_SUPPORT
from constants import BLOCK_SIZE, WORLD_MAX_X, WORLD_H, MINE_REACH, PLAYER_W, PLAYER_H

AUTOMATION_DEFS = {
    "coal_miner": {
        "name":             "Coal Miner",
        "fuel_item":        "coal",
        "fuel_tank":        20,
        "fuel_rate":        1 / 40.0,
        "mine_time":        3.0,
        "max_hardness":     3,
        "inv_limit":        30,
        "support_item":     "support_item",
        "support_block":    SUPPORT,
        "support_interval": 4,    # place a support every 4 blocks traveled
        "supports_max":     10,
        "w": 20, "h": 20,
        "color":            (110, 90, 70),
    },
    "iron_miner": {
        "name":             "Iron Miner",
        "fuel_item":        "iron_chunk",
        "fuel_tank":        10,
        "fuel_rate":        1 / 64.0,
        "mine_time":        1.5,
        "max_hardness":     6,
        "inv_limit":        50,
        "support_item":     "iron_support_item",
        "support_block":    IRON_SUPPORT,
        "support_interval": 10,   # iron support covers 5-block radius
        "supports_max":     5,
        "w": 20, "h": 20,
        "color":            (160, 170, 180),
    },
    "crystal_miner": {
        "name":             "Crystal Miner",
        "fuel_item":        "crystal_shard",
        "fuel_tank":        5,
        "fuel_rate":        1 / 96.0,
        "mine_time":        0.5,
        "max_hardness":     9,
        "inv_limit":        80,
        "support_item":     "diamond_support_item",
        "support_block":    DIAMOND_SUPPORT,
        "support_interval": 20,   # diamond support covers 10-block radius
        "supports_max":     3,
        "w": 20, "h": 20,
        "color":            (80, 200, 220),
    },
}


def _darken(color, amount=30):
    return tuple(max(0, c - amount) for c in color)


class Automation:
    def __init__(self, x, y, auto_type, direction=1):
        self.x = float(x)
        self.y = float(y)
        self.auto_type = auto_type
        self.direction = direction  # 1 = right, -1 = left
        self._def = AUTOMATION_DEFS[auto_type]

        self.fuel = 0.0
        self.supports = 0
        self.stored = {}

        self._state = "moving"
        self._halt_reason = ""
        self._mine_timer = 0.0
        self._mining_block_id = 0
        # Counts blocks traveled since last support was placed
        self._blocks_since_support = 0

    # ------------------------------------------------------------------ props
    @property
    def W(self):
        return self._def["w"]

    @property
    def H(self):
        return self._def["h"]

    @property
    def inv_count(self):
        return sum(self.stored.values())

    @property
    def status(self):
        if self._state != "halted":
            return "active"
        return {
            "fuel":        "halted_fuel",
            "full":        "halted_full",
            "blocked":     "halted_blocked",
            "no_supports": "halted_supports",
        }.get(self._halt_reason, "active")

    # ------------------------------------------------------------------ logic
    def _halt(self, reason):
        self._state = "halted"
        self._halt_reason = reason

    def _target_block(self):
        bx = int(self.x // BLOCK_SIZE) + self.direction
        by = int(self.y // BLOCK_SIZE)
        return bx, by

    def _place_support_if_needed(self, world):
        """
        Place a support at the automation's current block if the interval is reached.
        Returns False and halts if supports are required but unavailable.
        """
        adef = self._def
        if self._blocks_since_support < adef["support_interval"]:
            return True  # not time yet
        if self.supports <= 0:
            self._halt("no_supports")
            return False
        cbx = int(self.x // BLOCK_SIZE)
        cby = int(self.y // BLOCK_SIZE)
        if world.get_block(cbx, cby) == AIR:
            world.set_block(cbx, cby, adef["support_block"])
        self.supports -= 1
        self._blocks_since_support = 0
        return True

    def update(self, dt, world):
        adef = self._def

        # --- Halted: check if conditions have cleared ---
        if self._state == "halted":
            if self._halt_reason == "fuel" and self.fuel > 0:
                self._state = "moving"
                self._halt_reason = ""
            elif self._halt_reason == "full" and self.inv_count < adef["inv_limit"]:
                self._state = "moving"
                self._halt_reason = ""
            elif self._halt_reason == "no_supports" and self.supports > 0:
                self._state = "moving"
                self._halt_reason = ""
            elif self._halt_reason == "blocked":
                tbx, tby = self._target_block()
                if abs(tbx) < WORLD_MAX_X and 0 <= tby < WORLD_H:
                    bid = world.get_block(tbx, tby)
                    h = BLOCKS[bid]["hardness"]
                    if bid == AIR or (h != float("inf") and h <= adef["max_hardness"]):
                        self._state = "moving"
                        self._halt_reason = ""
            return  # no fuel consumed while halted

        # --- Consume fuel ---
        self.fuel = max(0.0, self.fuel - adef["fuel_rate"] * dt)
        if self.fuel == 0.0:
            self._halt("fuel")
            return

        # --- Check inventory capacity ---
        if self.inv_count >= adef["inv_limit"]:
            self._halt("full")
            return

        tbx, tby = self._target_block()

        # --- World edge ---
        if not (abs(tbx) < WORLD_MAX_X and 0 <= tby < WORLD_H):
            self._halt("blocked")
            return

        block_id = world.get_block(tbx, tby)

        # --- MOVING state ---
        if self._state == "moving":
            # Before moving, place a support at current position if interval reached
            if not self._place_support_if_needed(world):
                return  # halted for no_supports

            if block_id == AIR:
                self.x += self.direction * BLOCK_SIZE
                self._blocks_since_support += 1
                return

            h = BLOCKS[block_id]["hardness"]
            if h == float("inf") or h > adef["max_hardness"]:
                self._halt("blocked")
                return
            # Start mining
            self._state = "mining"
            self._mine_timer = 0.0
            self._mining_block_id = block_id
            return

        # --- MINING state ---
        if self._state == "mining":
            # If block changed externally (player mined it), resume moving
            if world.get_block(tbx, tby) != self._mining_block_id:
                self._state = "moving"
                self._mine_timer = 0.0
                return

            self._mine_timer += dt
            if self._mine_timer >= adef["mine_time"]:
                drop = BLOCKS[self._mining_block_id].get("drop")
                if drop:
                    chance = BLOCKS[self._mining_block_id].get("drop_chance", 1.0)
                    if random.random() < chance:
                        self.stored[drop] = self.stored.get(drop, 0) + 1
                world.set_block(tbx, tby, AIR)
                self.x += self.direction * BLOCK_SIZE
                self._blocks_since_support += 1
                self._state = "moving"
                self._mine_timer = 0.0

    # ------------------------------------------------------------------ interaction
    def deposit_fuel(self, player, amount=None):
        adef = self._def
        fuel_item = adef["fuel_item"]
        available = player.inventory.get(fuel_item, 0)
        if available <= 0:
            return
        space = adef["fuel_tank"] - self.fuel
        if space <= 0:
            return
        if amount is None:
            amount = available
        to_add = min(amount, available, int(space) if space == int(space) else int(space) + 1)
        to_add = min(to_add, int(space)) if space == int(space) else min(to_add, int(space) + 1)
        to_add = max(1, min(to_add, available)) if space > 0 else 0
        to_add = min(to_add, int(space) + (1 if space % 1 > 0 else 0))
        to_add = min(to_add, available)
        if to_add <= 0:
            return
        self.fuel = min(adef["fuel_tank"], self.fuel + to_add)
        player.inventory[fuel_item] = player.inventory.get(fuel_item, 0) - to_add
        if player.inventory[fuel_item] <= 0:
            player.inventory.pop(fuel_item, None)

    def deposit_supports(self, player, amount=None):
        adef = self._def
        sup_item = adef["support_item"]
        available = player.inventory.get(sup_item, 0)
        if available <= 0:
            return
        space = adef["supports_max"] - self.supports
        if space <= 0:
            return
        to_add = min(available, space) if amount is None else min(amount, available, space)
        if to_add <= 0:
            return
        self.supports += to_add
        player.inventory[sup_item] = player.inventory.get(sup_item, 0) - to_add
        if player.inventory[sup_item] <= 0:
            player.inventory.pop(sup_item, None)

    def take_all(self, player):
        for item_id, count in self.stored.items():
            for _ in range(count):
                player._add_item(item_id)
        self.stored.clear()

    def in_range(self, player):
        acx = (self.x + self.W / 2) / BLOCK_SIZE
        acy = (self.y + self.H / 2) / BLOCK_SIZE
        pcx = (player.x + PLAYER_W / 2) / BLOCK_SIZE
        pcy = (player.y + PLAYER_H / 2) / BLOCK_SIZE
        return ((acx - pcx) ** 2 + (acy - pcy) ** 2) ** 0.5 <= MINE_REACH

    # ------------------------------------------------------------------ rendering
    def draw(self, surface, cam_x, cam_y):
        sx = int(self.x - cam_x)
        sy = int(self.y - cam_y)
        W, H = self.W, self.H
        color = self._def["color"]
        dark = _darken(color)

        # Body
        pygame.draw.rect(surface, color, (sx, sy, W, H))
        pygame.draw.rect(surface, dark, (sx, sy, W, H), 2)

        # Direction arrow (triangle)
        mid_y = sy + H // 2
        if self.direction == 1:
            pts = [(sx + W - 5, mid_y), (sx + W - 11, mid_y - 4), (sx + W - 11, mid_y + 4)]
        else:
            pts = [(sx + 5, mid_y), (sx + 11, mid_y - 4), (sx + 11, mid_y + 4)]
        pygame.draw.polygon(surface, (255, 255, 255), pts)

        # Fuel bar (above, 4px tall — orange)
        bar_w = W
        frac_fuel = self.fuel / self._def["fuel_tank"] if self._def["fuel_tank"] > 0 else 0
        pygame.draw.rect(surface, (30, 30, 30), (sx, sy - 6, bar_w, 4))
        pygame.draw.rect(surface, (220, 160, 40), (sx, sy - 6, int(bar_w * frac_fuel), 4))

        # Support bar (above fuel bar, 3px tall — blue)
        frac_sup = self.supports / self._def["supports_max"] if self._def["supports_max"] > 0 else 0
        pygame.draw.rect(surface, (20, 20, 40), (sx, sy - 11, bar_w, 3))
        pygame.draw.rect(surface, (80, 160, 220), (sx, sy - 11, int(bar_w * frac_sup), 3))

        # Mining progress bar (below, 3px, only while mining)
        if self._state == "mining":
            prog = self._mine_timer / self._def["mine_time"]
            pygame.draw.rect(surface, (30, 30, 30), (sx, sy + H + 1, W, 3))
            pygame.draw.rect(surface, (80, 200, 80), (sx, sy + H + 1, int(W * prog), 3))

        # Halted overlay (semi-transparent red tint)
        if self._state == "halted":
            halt_surf = pygame.Surface((W, H), pygame.SRCALPHA)
            halt_surf.fill((180, 30, 30, 100))
            surface.blit(halt_surf, (sx, sy))
