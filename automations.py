import random
import pygame
from blocks import (BLOCKS, AIR, SUPPORT, IRON_SUPPORT, DIAMOND_SUPPORT,
                    MATURE_CROP_BLOCKS, MATURE_TO_YOUNG_CROP, YOUNG_CROP_BLOCKS,
                    GRASS, DIRT)
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


FARM_BOT_TYPES = {"farm_bot", "iron_farm_bot", "crystal_farm_bot"}

FARM_BOT_DEFS = {
    "farm_bot": {
        "name":          "Farm Bot",
        "fuel_item":     "coal",
        "fuel_tank":     60,
        "fuel_rate":     1 / 120.0,
        "scan_radius":   5,
        "scan_interval": 5.0,
        "inv_limit":     60,
        "w": 28, "h": 28,
        "color":         (80, 160, 60),
    },
    "iron_farm_bot": {
        "name":          "Iron Farm Bot",
        "fuel_item":     "iron_chunk",
        "fuel_tank":     40,
        "fuel_rate":     1 / 80.0,
        "scan_radius":   9,
        "scan_interval": 4.0,
        "inv_limit":     100,
        "w": 28, "h": 28,
        "color":         (160, 180, 160),
    },
    "crystal_farm_bot": {
        "name":          "Crystal Farm Bot",
        "fuel_item":     "crystal_shard",
        "fuel_tank":     20,
        "fuel_rate":     1 / 120.0,
        "scan_radius":   13,
        "scan_interval": 3.0,
        "inv_limit":     160,
        "w": 28, "h": 28,
        "color":         (100, 220, 200),
    },
}


def _darken(color, amount=30):
    return tuple(max(0, c - amount) for c in color)


class Automation:
    def __init__(self, x, y, auto_type, direction=(1, 0)):
        self.x = float(x)
        self.y = float(y)
        self.auto_type = auto_type
        self.direction = direction  # (dx, dy): (1,0)=right, (-1,0)=left, (0,-1)=up, (0,1)=down
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
        dx, dy = self.direction
        bx = int(self.x // BLOCK_SIZE) + dx
        by = int(self.y // BLOCK_SIZE) + dy
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
                dx, dy = self.direction
                self.x += dx * BLOCK_SIZE
                self.y += dy * BLOCK_SIZE
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
                dx, dy = self.direction
                self.x += dx * BLOCK_SIZE
                self.y += dy * BLOCK_SIZE
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
        dx, dy = self.direction
        cx, cy = sx + W // 2, sy + H // 2
        if (dx, dy) == (1, 0):
            pts = [(sx + W - 5, cy), (sx + W - 11, cy - 4), (sx + W - 11, cy + 4)]
        elif (dx, dy) == (-1, 0):
            pts = [(sx + 5, cy), (sx + 11, cy - 4), (sx + 11, cy + 4)]
        elif (dx, dy) == (0, -1):
            pts = [(cx, sy + 5), (cx - 4, sy + 11), (cx + 4, sy + 11)]
        else:
            pts = [(cx, sy + H - 5), (cx - 4, sy + H - 11), (cx + 4, sy + H - 11)]
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


class FarmBot:
    def __init__(self, x, y, bot_type, fuel=0.0, seeds=None, stored=None, state="active"):
        self.x = float(x)
        self.y = float(y)
        self.bot_type = bot_type
        self._def = FARM_BOT_DEFS[bot_type]
        self.fuel = float(fuel)
        self.seeds = seeds or {}
        self.stored = stored or {}
        self._state = state
        self._halt_reason = ""
        self._scan_timer = 0.0
        self._mature_to_seed = None

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
        return {"fuel": "halted_fuel", "full": "halted_full"}.get(self._halt_reason, "active")

    def _get_mature_to_seed(self):
        if self._mature_to_seed is None:
            from items import ITEMS
            young_to_seed = {idata["place_block"]: iid
                             for iid, idata in ITEMS.items()
                             if idata.get("place_block") in YOUNG_CROP_BLOCKS}
            self._mature_to_seed = {
                mature: young_to_seed.get(young)
                for mature, young in MATURE_TO_YOUNG_CROP.items()
            }
        return self._mature_to_seed

    def update(self, dt, world):
        adef = self._def
        if self._state == "halted":
            if self._halt_reason == "fuel" and self.fuel > 0:
                self._state = "active"
                self._halt_reason = ""
            elif self._halt_reason == "full" and self.inv_count < adef["inv_limit"]:
                self._state = "active"
                self._halt_reason = ""
            return
        self.fuel = max(0.0, self.fuel - adef["fuel_rate"] * dt)
        if self.fuel == 0.0:
            self._state = "halted"
            self._halt_reason = "fuel"
            return
        self._scan_timer += dt
        if self._scan_timer >= adef["scan_interval"]:
            self._scan_timer = 0.0
            self._scan_and_tend(world)

    def _scan_and_tend(self, world):
        adef = self._def
        if self.inv_count >= adef["inv_limit"]:
            self._state = "halted"
            self._halt_reason = "full"
            return
        # Auto-cycle: any seed items that landed in stored produce get moved to seeds slot
        from items import ITEMS
        for item_id in list(self.stored.keys()):
            if ITEMS.get(item_id, {}).get("place_block") in YOUNG_CROP_BLOCKS:
                self.seeds[item_id] = self.seeds.get(item_id, 0) + self.stored.pop(item_id)
        cx = int((self.x + self.W / 2) // BLOCK_SIZE)
        cy = int((self.y + self.H / 2) // BLOCK_SIZE)
        r = adef["scan_radius"]
        mature_to_seed = self._get_mature_to_seed()
        for bx in range(cx - r, cx + r + 1):
            for by in range(cy - r, cy + r + 1):
                if self.inv_count >= adef["inv_limit"]:
                    return
                bid = world.get_block(bx, by)
                if bid in MATURE_CROP_BLOCKS:
                    self._harvest(world, bx, by, bid, mature_to_seed)
                elif bid == AIR and self.seeds and world.get_block(bx, by + 1) in (GRASS, DIRT):
                    self._plant(world, bx, by)

    def _plant(self, world, bx, by):
        from items import ITEMS
        for seed_id, count in list(self.seeds.items()):
            if count > 0:
                world.set_block(bx, by, ITEMS[seed_id]["place_block"])
                self.seeds[seed_id] -= 1
                if self.seeds[seed_id] <= 0:
                    del self.seeds[seed_id]
                return

    def _harvest(self, world, bx, by, block_id, mature_to_seed):
        drop = BLOCKS[block_id].get("drop")
        if drop:
            if random.random() < BLOCKS[block_id].get("drop_chance", 1.0):
                self.stored[drop] = self.stored.get(drop, 0) + 1
        seed_drop = mature_to_seed.get(block_id)
        if seed_drop:
            count = random.randint(1, 2)
            self.stored[seed_drop] = self.stored.get(seed_drop, 0) + count
        world.set_block(bx, by, AIR)
        if world.get_block(bx, by + 1) not in (GRASS, DIRT):
            return
        seed_id = mature_to_seed.get(block_id)
        # Prefer exact seed match, fall back to any available seed
        if seed_id and self.seeds.get(seed_id, 0) > 0:
            world.set_block(bx, by, MATURE_TO_YOUNG_CROP[block_id])
            self.seeds[seed_id] -= 1
            if self.seeds[seed_id] <= 0:
                del self.seeds[seed_id]
        elif self.seeds:
            self._plant(world, bx, by)

    def deposit_fuel(self, player, amount=None):
        adef = self._def
        fi = adef["fuel_item"]
        have = player.inventory.get(fi, 0)
        if have <= 0 or self.fuel >= adef["fuel_tank"]:
            return
        space = adef["fuel_tank"] - self.fuel
        n = min(have, int(space) + (1 if space % 1 else 0))
        if amount is not None:
            n = min(n, amount)
        if n <= 0:
            return
        self.fuel = min(adef["fuel_tank"], self.fuel + n)
        player.inventory[fi] = have - n
        if player.inventory[fi] <= 0:
            del player.inventory[fi]

    def deposit_seeds(self, player, seed_id, amount=None):
        have = player.inventory.get(seed_id, 0)
        if have <= 0:
            return
        n = have if amount is None else min(amount, have)
        if n <= 0:
            return
        self.seeds[seed_id] = self.seeds.get(seed_id, 0) + n
        player.inventory[seed_id] = have - n
        if player.inventory[seed_id] <= 0:
            del player.inventory[seed_id]

    def deposit_all_seeds(self, player):
        from items import ITEMS
        seed_ids = [iid for iid, idata in ITEMS.items()
                    if idata.get("place_block") in YOUNG_CROP_BLOCKS
                    and player.inventory.get(iid, 0) > 0]
        for seed_id in seed_ids:
            self.deposit_seeds(player, seed_id)

    def get_seeds(self, player):
        for seed_id, count in list(self.seeds.items()):
            for _ in range(count):
                player._add_item(seed_id)
        self.seeds.clear()

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

    def draw(self, surface, cam_x, cam_y):
        sx = int(self.x - cam_x)
        sy = int(self.y - cam_y)
        W, H = self.W, self.H
        color = self._def["color"]
        dark = _darken(color)

        pygame.draw.rect(surface, color, (sx, sy, W, H))
        pygame.draw.rect(surface, dark, (sx, sy, W, H), 2)

        # Leaf icon
        cx, cy_ = sx + W // 2, sy + H // 2
        leaf_pts = [(cx, cy_ - 5), (cx - 4, cy_ + 3), (cx + 4, cy_ + 3)]
        pygame.draw.polygon(surface, (40, 100, 40), leaf_pts)

        # Fuel bar
        bar_w = W
        frac_fuel = self.fuel / self._def["fuel_tank"] if self._def["fuel_tank"] > 0 else 0
        pygame.draw.rect(surface, (30, 30, 30), (sx, sy - 6, bar_w, 4))
        pygame.draw.rect(surface, (220, 160, 40), (sx, sy - 6, int(bar_w * frac_fuel), 4))

        if self._state == "halted":
            halt_surf = pygame.Surface((W, H), pygame.SRCALPHA)
            halt_surf.fill((180, 30, 30, 100))
            surface.blit(halt_surf, (sx, sy))
