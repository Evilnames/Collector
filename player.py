import random
import pygame
from automations import Automation, AUTOMATION_DEFS, FarmBot, FARM_BOT_DEFS, FARM_BOT_TYPES
from blocks import (BLOCKS, AIR, ROCK_DEPOSIT, WILDFLOWER_PATCH, FOSSIL_DEPOSIT, CAVE_MUSHROOMS, EQUIPMENT_BLOCKS, LADDER, SUPPORT, WATER,
                    WOOD_DOOR_CLOSED, WOOD_DOOR_OPEN, IRON_DOOR_CLOSED, IRON_DOOR_OPEN,
                    ALL_SUPPORTS, SAPLING, GRASS, DIRT, ALL_LOGS, ALL_LEAVES,
                    YOUNG_CROP_BLOCKS, MATURE_CROP_BLOCKS, BUSH_BLOCKS,
                    STRAWBERRY_BUSH, WHEAT_BUSH,
                    CARROT_BUSH, TOMATO_BUSH, CORN_BUSH, PUMPKIN_BUSH, APPLE_BUSH,
                    RICE_BUSH, GINGER_BUSH, BOK_CHOY_BUSH, GARLIC_BUSH,
                    SCALLION_BUSH, CHILI_BUSH,
                    PEPPER_BUSH, ONION_BUSH, POTATO_BUSH, EGGPLANT_BUSH, CABBAGE_BUSH,
                    STRAWBERRY_CROP_MATURE, WHEAT_CROP_MATURE,
                    CARROT_CROP_MATURE, TOMATO_CROP_MATURE, CORN_CROP_MATURE,
                    PUMPKIN_CROP_MATURE, APPLE_CROP_MATURE,
                    RICE_CROP_MATURE, GINGER_CROP_MATURE,
                    BOK_CHOY_CROP_MATURE, GARLIC_CROP_MATURE,
                    SCALLION_CROP_MATURE, CHILI_CROP_MATURE,
                    PEPPER_CROP_MATURE, ONION_CROP_MATURE, POTATO_CROP_MATURE,
                    EGGPLANT_CROP_MATURE, CABBAGE_CROP_MATURE,
                    PERENNIAL_CROP_MATURE, MATURE_TO_YOUNG_CROP, CHEST_BLOCK)
from items import ITEMS
from rocks import RockGenerator, Rock
from wildflowers import WildflowerGenerator, Wildflower
from fossils import FossilGenerator, Fossil
from constants import (
    BLOCK_SIZE, PLAYER_W, PLAYER_H,
    GRAVITY, JUMP_FORCE, MOVE_SPEED, MAX_FALL,
    MINE_REACH, MAX_HEALTH, HOTBAR_SIZE,
    ROCK_DETECT_RANGE,
)


class Player:
    def __init__(self, world):
        self.world = world
        sx = 0
        sy = world.surface_y_at(sx)
        self.x = float(sx * BLOCK_SIZE + (BLOCK_SIZE - PLAYER_W) // 2)
        self.y = float((sy - 2) * BLOCK_SIZE)
        self.vx = 0.0
        self.vy = 0.0
        self.on_ground = False
        self.facing = 1          # 1 = right, -1 = left
        self.health = MAX_HEALTH
        self.pick_power = 1
        self.inventory = {}
        self.hotbar = [None] * HOTBAR_SIZE
        self.hotbar_uses = [None] * HOTBAR_SIZE
        self.selected_slot = 0
        self.money = 0
        # Rock collection
        self.rocks = []
        self.discovered_types = set()
        self.rock_detect_range = ROCK_DETECT_RANGE
        self._rock_gen = RockGenerator(world.seed)
        # Wildflower collection
        self.wildflowers = []
        self.discovered_flower_types = set()
        self._flower_gen = WildflowerGenerator(world.seed)
        # Mushroom collection
        self.mushrooms_found = {}        # block_id -> count
        self.discovered_mushroom_types = set()
        # Fossil collection
        self.fossils = []
        self.discovered_fossil_types = set()
        self._fossil_gen = FossilGenerator(world.seed)
        self.pending_notifications = []   # (category, name_or_bid, rarity)
        self.known_recipes = set()
        # Water state
        self._drowning_timer = 0.0
        # Hunger
        self.hunger             = 100.0
        self._hunger_drain_rate = 100.0 / 600.0  # 100% over 10 minutes
        self._eat_cooldown      = 0.0
        # Spawn / death
        self.spawn_x = None
        self.spawn_y = None
        self.dead = False
        self.god_mode = False
        # Mining state
        self.mining_block = None  # (bx, by) or None
        self.mine_progress = 0.0
        self._mine_time = 0.0
        self._mine_total = 0.0
        # Placement state
        self.place_target = None  # (bx, by) ghost shown by renderer
        # Farm sense: block under mouse (for crop readiness display)
        self.target_block = None

    def apply_save(self, d):
        self.x, self.y = d["x"], d["y"]
        self.vx, self.vy = d["vx"], d["vy"]
        self.facing = d["facing"]
        self.health, self.hunger = d["health"], d["hunger"]
        self.pick_power, self.money = d["pick_power"], d["money"]
        self.selected_slot = d["selected_slot"]
        self.inventory = d["inventory"]
        self.hotbar = d["hotbar"]
        self.hotbar_uses = d["hotbar_uses"]
        self.known_recipes = set(d["known_recipes"])
        self.rocks = [Rock(**r) for r in d["rocks"]]
        self.wildflowers = [Wildflower(**wf) for wf in d["wildflowers"]]
        self.fossils = [Fossil(**f) for f in d.get("fossils", [])]
        self.discovered_types = set(d["discovered_types"])
        self.discovered_flower_types = set(d["discovered_flower_types"])
        self.discovered_fossil_types = set(d.get("discovered_fossil_types", []))
        self.mushrooms_found = {int(k): v for k, v in d["mushrooms_found"].items()}
        self.discovered_mushroom_types = set(int(x) for x in d["discovered_mushroom_types"])
        self.spawn_x = d.get("spawn_x")
        self.spawn_y = d.get("spawn_y")

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------

    def handle_input(self, keys, mouse_buttons, mouse_world_pos, dt):
        self.vx = 0.0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vx = -MOVE_SPEED
            self.facing = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vx = MOVE_SPEED
            self.facing = 1

        if self._in_ladder():
            if keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]:
                self.vy = -4   # climb up
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.vy = 2    # climb down
            else:
                self.vy = 0    # hold position
        elif self._in_water():
            if keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]:
                self.vy = -3   # swim up
            self.vx *= 0.55    # water drag on horizontal movement
        elif (keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.on_ground:
            self.vy = JUMP_FORCE
            self.on_ground = False

        mining = False
        harvest_target = None

        # Keyboard mining: Z key digs in the direction you're facing.
        # Z + W = dig up, Z + S = dig down.
        if keys[pygame.K_z]:
            mining = True
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                bx = int((self.x + PLAYER_W / 2) // BLOCK_SIZE)
                by = int(self.y // BLOCK_SIZE) - 1
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                bx = int((self.x + PLAYER_W / 2) // BLOCK_SIZE)
                by = int((self.y + PLAYER_H - 1) // BLOCK_SIZE) + 1
            else:
                by = int((self.y + PLAYER_H / 2) // BLOCK_SIZE)
                if self.facing == 1:
                    bx = int((self.x + PLAYER_W - 1) // BLOCK_SIZE) + 1
                else:
                    bx = int(self.x // BLOCK_SIZE) - 1
            self._mine_at(bx, by, dt)

        # Mouse mining: left-click, but only on the facing side.
        elif mouse_buttons[0]:
            mining = True
            mx, my = mouse_world_pos
            pcx = self.x + PLAYER_W / 2

            # Try animal interaction first
            harvest_target = self._find_animal_at(mx, my)
            if harvest_target is not None:
                result = harvest_target.try_harvest(self, dt)
                if result is not None:
                    item_id, count = result
                    for _ in range(count):
                        self._add_item(item_id)
                    self._consume_tool_use()
                self._reset_mine()
            else:
                # Normal block mining (facing-side check)
                if self.facing == 1 and mx < pcx - BLOCK_SIZE * 0.5:
                    self._reset_mine()
                elif self.facing == -1 and mx > pcx + BLOCK_SIZE * 0.5:
                    self._reset_mine()
                else:
                    bx = int(mx // BLOCK_SIZE)
                    by = int(my // BLOCK_SIZE)
                    cx = pcx / BLOCK_SIZE
                    cy = (self.y + PLAYER_H / 2) / BLOCK_SIZE
                    if ((bx - cx) ** 2 + (by - cy) ** 2) ** 0.5 > MINE_REACH:
                        self._reset_mine()
                    else:
                        self._mine_at(bx, by, dt)
        if not mining:
            self._reset_mine()

        # Track mouse target for farm sense display
        self.target_block = None
        mx, my = mouse_world_pos
        tbx = int(mx // BLOCK_SIZE)
        tby = int(my // BLOCK_SIZE)
        pcx = self.x + PLAYER_W / 2
        if ((tbx - pcx / BLOCK_SIZE) ** 2 + (tby - (self.y + PLAYER_H / 2) / BLOCK_SIZE) ** 2) ** 0.5 <= MINE_REACH:
            self.target_block = (tbx, tby)

        # Reset harvest state for animals not currently targeted
        for entity in getattr(self.world, 'entities', []):
            if entity is not harvest_target:
                entity.reset_harvest()

        # Block placement: right-click = mouse target, Ctrl = block in facing direction
        placing = mouse_buttons[2] or keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]
        if placing:
            if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                # Ctrl: place in facing direction
                by = int((self.y + PLAYER_H / 2) // BLOCK_SIZE)
                if self.facing == 1:
                    bx = int((self.x + PLAYER_W - 1) // BLOCK_SIZE) + 1
                else:
                    bx = int(self.x // BLOCK_SIZE) - 1
                self.place_target = (bx, by)
                self._try_place(bx, by)
            else:
                # Right-click: place at cursor
                mx, my = mouse_world_pos
                bx = int(mx // BLOCK_SIZE)
                by = int(my // BLOCK_SIZE)
                cx = (self.x + PLAYER_W / 2) / BLOCK_SIZE
                cy = (self.y + PLAYER_H / 2) / BLOCK_SIZE
                if ((bx - cx) ** 2 + (by - cy) ** 2) ** 0.5 <= MINE_REACH:
                    self.place_target = (bx, by)
                    self._try_place(bx, by)
                else:
                    self.place_target = None
        else:
            self.place_target = None

    def _find_animal_at(self, mx, my):
        for entity in getattr(self.world, 'entities', []):
            if entity.rect.collidepoint(mx, my) and entity.in_range(self):
                return entity
        return None

    def _reset_mine(self):
        self.mining_block = None
        self.mine_progress = 0.0
        self._mine_time = 0.0

    def _has_line_of_sight(self, target_bx, target_by):
        px = (self.x + PLAYER_W / 2) / BLOCK_SIZE
        py = (self.y + PLAYER_H / 2) / BLOCK_SIZE
        dx = (target_bx + 0.5) - px
        dy = (target_by + 0.5) - py
        dist = (dx * dx + dy * dy) ** 0.5
        if dist == 0:
            return True
        step = 0.35
        sx, sy = dx / dist * step, dy / dist * step
        cx, cy = px + sx, py + sy
        for _ in range(int(dist / step)):
            ibx, iby = int(cx), int(cy)
            if ibx == target_bx and iby == target_by:
                return True
            if self.world.is_solid(ibx, iby):
                return False
            cx += sx
            cy += sy
        return True

    def _mine_at(self, bx, by, dt):
        block_id = self.world.get_block(bx, by)
        if block_id == AIR:
            self._reset_mine()
            return
        if block_id in YOUNG_CROP_BLOCKS:
            self._reset_mine()
            return

        hardness = BLOCKS[block_id]["hardness"]
        if hardness == float('inf'):
            return

        if self.mining_block != (bx, by):
            self.mining_block = (bx, by)
            self._mine_time = 0.0
            self._mine_total = hardness / self._mining_power_for(block_id)

        self._mine_time += dt
        self.mine_progress = min(1.0, self._mine_time / self._mine_total)

        if self.mine_progress >= 1.0:
            if block_id == ROCK_DEPOSIT:
                rock = self._rock_gen.generate(bx, by, self.get_depth(), self.world.get_biome(bx))
                self.rocks.append(rock)
                self.discovered_types.add(rock.base_type)
                self.pending_notifications.append(
                    ("Rock", rock.base_type.replace("_", " ").title(), rock.rarity))
            elif block_id == WILDFLOWER_PATCH:
                flower = self._flower_gen.generate(bx, by, self.world.get_biodome(bx))
                self.wildflowers.append(flower)
                self.discovered_flower_types.add(flower.flower_type)
                self.pending_notifications.append(
                    ("Wildflower", flower.flower_type.replace("_", " ").title(), flower.rarity))
            elif block_id == FOSSIL_DEPOSIT:
                fossil = self._fossil_gen.generate(bx, by, self.get_depth(), self.world.get_biome(bx))
                self.fossils.append(fossil)
                self.discovered_fossil_types.add(fossil.fossil_type)
                self.pending_notifications.append(
                    ("Fossil", fossil.fossil_type.replace("_", " ").title(), fossil.rarity))
            elif block_id in CAVE_MUSHROOMS:
                self.mushrooms_found[block_id] = self.mushrooms_found.get(block_id, 0) + 1
                self.discovered_mushroom_types.add(block_id)
                self.pending_notifications.append(("Mushroom", block_id, None))
            else:
                block_data = BLOCKS[block_id]
                drop = block_data["drop"]
                if drop:
                    chance = block_data.get("drop_chance", 1.0)
                    if random.random() < chance:
                        self._add_item(drop)
                if block_id == CHEST_BLOCK:
                    for item_id, count in self.world.chest_data.pop((bx, by), {}).items():
                        if count > 0:
                            self._add_item(item_id, count)
                # Mature crops also drop seeds back
                if block_id == STRAWBERRY_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("strawberry_seed")
                elif block_id == WHEAT_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("wheat_seed")
                elif block_id == CARROT_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("carrot_seed")
                elif block_id == TOMATO_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("tomato_seed")
                elif block_id == CORN_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("corn_seed")
                elif block_id == PUMPKIN_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("pumpkin_seed")
                elif block_id == APPLE_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("apple_seed")
                elif block_id == RICE_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("rice_seed")
                elif block_id == GINGER_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("ginger_seed")
                elif block_id == BOK_CHOY_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("bok_choy_seed")
                elif block_id == GARLIC_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("garlic_seed")
                elif block_id == SCALLION_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("scallion_seed")
                elif block_id == CHILI_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("chili_seed")
                elif block_id == PEPPER_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("pepper_seed")
                elif block_id == ONION_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("onion_seed")
                elif block_id == POTATO_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("potato_seed")
                elif block_id == EGGPLANT_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("eggplant_seed")
                elif block_id == CABBAGE_CROP_MATURE:
                    for _ in range(random.randint(1, 2)):
                        self._add_item("cabbage_seed")
                # Bushes: small chance of food directly
                elif block_id == STRAWBERRY_BUSH and random.random() < 0.25:
                    self._add_item("strawberry")
                elif block_id == WHEAT_BUSH and random.random() < 0.20:
                    self._add_item("wheat")
                elif block_id == CARROT_BUSH and random.random() < 0.30:
                    self._add_item("carrot")
                elif block_id == TOMATO_BUSH and random.random() < 0.25:
                    self._add_item("tomato")
                elif block_id == CORN_BUSH and random.random() < 0.20:
                    self._add_item("corn")
                elif block_id == PUMPKIN_BUSH and random.random() < 0.15:
                    self._add_item("pumpkin")
                elif block_id == APPLE_BUSH and random.random() < 0.30:
                    self._add_item("apple")
                elif block_id == RICE_BUSH and random.random() < 0.25:
                    self._add_item("rice")
                elif block_id == GINGER_BUSH and random.random() < 0.20:
                    self._add_item("ginger")
                elif block_id == BOK_CHOY_BUSH and random.random() < 0.30:
                    self._add_item("bok_choy")
                elif block_id == GARLIC_BUSH and random.random() < 0.20:
                    self._add_item("garlic")
                elif block_id == SCALLION_BUSH and random.random() < 0.30:
                    self._add_item("scallion")
                elif block_id == CHILI_BUSH and random.random() < 0.25:
                    self._add_item("chili")
                elif block_id == PEPPER_BUSH and random.random() < 0.25:
                    self._add_item("pepper")
                elif block_id == ONION_BUSH and random.random() < 0.20:
                    self._add_item("onion")
                elif block_id == POTATO_BUSH and random.random() < 0.20:
                    self._add_item("potato")
                elif block_id == EGGPLANT_BUSH and random.random() < 0.25:
                    self._add_item("eggplant")
                elif block_id == CABBAGE_BUSH and random.random() < 0.30:
                    self._add_item("cabbage")
            if block_id in PERENNIAL_CROP_MATURE and random.random() > 0.33:
                self.world.set_block(bx, by, MATURE_TO_YOUNG_CROP[block_id])
            else:
                self.world.set_block(bx, by, AIR)
            self._consume_tool_use()
            self._reset_mine()

    def _selected_place_block(self):
        """Returns (item_id, block_id) for the selected hotbar slot, or (None, None)."""
        item_id = self.hotbar[self.selected_slot]
        if item_id is None:
            return None, None
        block_id = ITEMS.get(item_id, {}).get("place_block")
        if block_id is None:
            return None, None
        if self.inventory.get(item_id, 0) <= 0:
            return None, None
        return item_id, block_id

    def _try_place(self, bx, by):
        current = self.world.get_block(bx, by)
        if current == WOOD_DOOR_CLOSED:
            self.world.set_block(bx, by, WOOD_DOOR_OPEN); return
        if current == WOOD_DOOR_OPEN:
            self.world.set_block(bx, by, WOOD_DOOR_CLOSED); return
        if current == IRON_DOOR_CLOSED:
            self.world.set_block(bx, by, IRON_DOOR_OPEN); return
        if current == IRON_DOOR_OPEN:
            self.world.set_block(bx, by, IRON_DOOR_CLOSED); return
        item_id = self.hotbar[self.selected_slot]
        if item_id is None:
            return
        item_data = ITEMS.get(item_id, {})
        if item_data.get("edible", False):
            self._try_eat()
            return
        spawn_type = item_data.get("spawn_automation")
        if spawn_type:
            if self.inventory.get(item_id, 0) <= 0:
                return
            if spawn_type in FARM_BOT_TYPES:
                adef = FARM_BOT_DEFS[spawn_type]
                ax = bx * BLOCK_SIZE + (BLOCK_SIZE - adef["w"]) // 2
                ay = by * BLOCK_SIZE + (BLOCK_SIZE - adef["h"]) // 2
                self.world.farm_bots.append(FarmBot(ax, ay, spawn_type))
            else:
                adef = AUTOMATION_DEFS[spawn_type]
                ax = bx * BLOCK_SIZE + (BLOCK_SIZE - adef["w"]) // 2
                ay = by * BLOCK_SIZE + (BLOCK_SIZE - adef["h"]) // 2
                pcx = int((self.x + PLAYER_W / 2) // BLOCK_SIZE)
                pcy = int((self.y + PLAYER_H / 2) // BLOCK_SIZE)
                ddx, ddy = bx - pcx, by - pcy
                if abs(ddx) >= abs(ddy):
                    spawn_dir = (1 if ddx >= 0 else -1, 0)
                else:
                    spawn_dir = (0, 1 if ddy >= 0 else -1)
                self.world.automations.append(Automation(ax, ay, spawn_type, spawn_dir))
            self.inventory[item_id] -= 1
            if self.inventory[item_id] <= 0:
                del self.inventory[item_id]
                for i in range(HOTBAR_SIZE):
                    if self.hotbar[i] == item_id:
                        self.hotbar[i] = None
                        break
            return
        block_id = item_data.get("place_block")
        if block_id is None:
            return
        if self.inventory.get(item_id, 0) <= 0:
            return
        if self.world.get_block(bx, by) != AIR:
            return
        # Seeds must be planted on grass or dirt
        if block_id in YOUNG_CROP_BLOCKS:
            if self.world.get_block(bx, by + 1) not in (GRASS, DIRT):
                return
        # Don't place inside the player (passable blocks are exempt)
        passable = {LADDER, SAPLING} | ALL_SUPPORTS | BUSH_BLOCKS | YOUNG_CROP_BLOCKS
        if block_id not in passable:
            block_px = pygame.Rect(bx * BLOCK_SIZE, by * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            if block_px.colliderect(self.rect):
                return
        self.world.set_block(bx, by, block_id)
        self.inventory[item_id] -= 1
        if self.inventory[item_id] <= 0:
            del self.inventory[item_id]
            for i in range(HOTBAR_SIZE):
                if self.hotbar[i] == item_id:
                    self.hotbar[i] = None

    def _consume_tool_use(self):
        """Decrement uses for a consumable tool in the selected hotbar slot."""
        slot = self.selected_slot
        item_id = self.hotbar[slot]
        if item_id is None:
            return
        max_uses = ITEMS.get(item_id, {}).get("max_uses")
        if max_uses is None:
            return
        uses = self.hotbar_uses[slot]
        if uses is None:
            return
        uses -= 1
        if uses <= 0:
            self.inventory[item_id] = self.inventory.get(item_id, 1) - 1
            if self.inventory.get(item_id, 0) <= 0:
                self.inventory.pop(item_id, None)
                self.hotbar[slot] = None
                self.hotbar_uses[slot] = None
            else:
                self.hotbar_uses[slot] = max_uses
        else:
            self.hotbar_uses[slot] = uses

    def _add_item(self, item_id, count=1):
        self.inventory[item_id] = self.inventory.get(item_id, 0) + count
        if item_id not in self.hotbar:
            for i in range(HOTBAR_SIZE):
                if self.hotbar[i] is None:
                    self.hotbar[i] = item_id
                    max_uses = ITEMS.get(item_id, {}).get("max_uses")
                    if max_uses is not None:
                        self.hotbar_uses[i] = max_uses
                    break

    def collect_all_items(self):
        drops = {k: v for k, v in self.inventory.items() if v > 0}
        self.inventory = {}
        self.hotbar = [None] * HOTBAR_SIZE
        self.hotbar_uses = [None] * HOTBAR_SIZE
        return drops

    def respawn(self):
        if self.spawn_x is not None and self.spawn_y is not None:
            self.x = float(self.spawn_x)
            self.y = float(self.spawn_y)
        else:
            sx = 0
            sy = self.world.surface_y_at(sx)
            self.x = float(sx * BLOCK_SIZE + (BLOCK_SIZE - PLAYER_W) // 2)
            self.y = float((sy - 2) * BLOCK_SIZE)
        self.vx = 0.0
        self.vy = 0.0
        self.health = MAX_HEALTH
        self.hunger = 100.0
        self.dead = False
        self._drowning_timer = 0.0

    def get_nearby_bed(self):
        from blocks import BED
        cx = int((self.x + PLAYER_W / 2) // BLOCK_SIZE)
        cy = int((self.y + PLAYER_H / 2) // BLOCK_SIZE)
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                if self.world.get_block(cx + dx, cy + dy) == BED:
                    return (cx + dx, cy + dy)
        return None

    def set_spawn(self, bx, by):
        self.spawn_x = float(bx * BLOCK_SIZE + (BLOCK_SIZE - PLAYER_W) // 2)
        self.spawn_y = float((by - 1) * BLOCK_SIZE)

    def _try_eat(self):
        if self._eat_cooldown > 0:
            return False
        item_id = self.hotbar[self.selected_slot]
        if item_id is None:
            return False
        item_data = ITEMS.get(item_id, {})
        if not item_data.get("edible", False):
            return False
        if self.inventory.get(item_id, 0) <= 0:
            return False
        self.hunger = min(100.0, self.hunger + item_data.get("hunger_restore", 0))
        self._eat_cooldown = 0.5
        self.inventory[item_id] -= 1
        if self.inventory[item_id] <= 0:
            del self.inventory[item_id]
            for i in range(HOTBAR_SIZE):
                if self.hotbar[i] == item_id:
                    self.hotbar[i] = None
        return True

    # ------------------------------------------------------------------
    # Physics
    # ------------------------------------------------------------------

    def update(self, dt):
        in_water = self._in_water()
        if self._in_ladder():
            self.vy = min(self.vy, 2)  # suppress gravity; allow slow drift but not free-fall
        elif in_water:
            # Buoyancy: reduced gravity and terminal velocity while submerged
            self.vy = min(self.vy + GRAVITY * 0.25, 2.5)
        else:
            self.vy = min(self.vy + GRAVITY, MAX_FALL)
        self._move_x(self.vx)
        prev_vy = self.vy
        landed = self._move_y(self.vy)
        if not self.god_mode:
            # Fall damage only applies outside water
            if landed and prev_vy > 10 and not in_water:
                dmg = int((prev_vy - 10) * 5)
                self.health = max(0, self.health - dmg)
            # Drowning: after 5 s with head submerged, 5 HP/s damage
            if self._head_in_water():
                self._drowning_timer += dt
                if self._drowning_timer > 5.0:
                    self.health = max(0, self.health - 5 * dt)
            else:
                self._drowning_timer = max(0.0, self._drowning_timer - dt * 2)
        else:
            self._drowning_timer = 0.0
            self.health = MAX_HEALTH
            self.hunger = 100.0
        # Hunger drain and starvation damage
        if self._eat_cooldown > 0:
            self._eat_cooldown -= dt
        if not self.god_mode:
            self.hunger = max(0.0, self.hunger - self._hunger_drain_rate * dt)
            if self.hunger == 0.0:
                self.health = max(0, self.health - 3 * dt)
        # Death detection
        if not self.dead and self.health <= 0:
            self.dead = True

    def _move_x(self, dx):
        if dx == 0:
            return
        self.x += dx
        if self._collides():
            self.x -= dx
            self.vx = 0.0

    def _move_y(self, dy):
        if dy == 0:
            return False
        self.y += dy
        if self._collides():
            self.y -= dy
            hit_floor = dy > 0
            if hit_floor:
                self.on_ground = True
            self.vy = 0.0
            return hit_floor
        else:
            if dy > 0:
                self.on_ground = False
            return False

    def _in_ladder(self):
        left  = int(self.x // BLOCK_SIZE)
        right = int((self.x + PLAYER_W - 1) // BLOCK_SIZE)
        top   = int(self.y // BLOCK_SIZE)
        bot   = int((self.y + PLAYER_H - 1) // BLOCK_SIZE)
        for bx in range(left, right + 1):
            for by in range(top, bot + 1):
                if self.world.get_block(bx, by) == LADDER:
                    return True
        return False

    def _in_water(self):
        left  = int(self.x // BLOCK_SIZE)
        right = int((self.x + PLAYER_W - 1) // BLOCK_SIZE)
        top   = int(self.y // BLOCK_SIZE)
        bot   = int((self.y + PLAYER_H - 1) // BLOCK_SIZE)
        for bx in range(left, right + 1):
            for by in range(top, bot + 1):
                if self.world.get_block(bx, by) == WATER:
                    return True
        return False

    def _head_in_water(self):
        left  = int(self.x // BLOCK_SIZE)
        right = int((self.x + PLAYER_W - 1) // BLOCK_SIZE)
        head_y = int(self.y // BLOCK_SIZE)
        for bx in range(left, right + 1):
            if self.world.get_block(bx, head_y) == WATER:
                return True
        return False

    def _collides(self):
        left  = int(self.x // BLOCK_SIZE)
        right = int((self.x + PLAYER_W - 1) // BLOCK_SIZE)
        top   = int(self.y // BLOCK_SIZE)
        bot   = int((self.y + PLAYER_H - 1) // BLOCK_SIZE)
        for bx in range(left, right + 1):
            for by in range(top, bot + 1):
                if self.world.is_solid(bx, by):
                    return True
        return False

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def get_nearby_equipment(self):
        """Return the block_id of an equipment block within 2 blocks of the player, or None."""
        cx = int((self.x + PLAYER_W / 2) // BLOCK_SIZE)
        cy = int((self.y + PLAYER_H / 2) // BLOCK_SIZE)
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                bid = self.world.get_block(cx + dx, cy + dy)
                if bid in EQUIPMENT_BLOCKS:
                    return bid
        return None

    def get_nearby_chest(self):
        """Return (bx, by) of a chest block within 2 blocks of the player, or None."""
        cx = int((self.x + PLAYER_W / 2) // BLOCK_SIZE)
        cy = int((self.y + PLAYER_H / 2) // BLOCK_SIZE)
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                if self.world.get_block(cx + dx, cy + dy) == CHEST_BLOCK:
                    return (cx + dx, cy + dy)
        return None

    def get_depth(self):
        block_y = int(self.y // BLOCK_SIZE)
        surface_y = self.world.surface_y_at(int(self.x // BLOCK_SIZE))
        return max(0, block_y - surface_y)

    @property
    def effective_pick_power(self):
        item_id = self.hotbar[self.selected_slot]
        tool_power = ITEMS.get(item_id, {}).get("pick_power", 0) if item_id else 0
        return max(self.pick_power, tool_power)

    @property
    def effective_axe_power(self):
        item_id = self.hotbar[self.selected_slot]
        tool_power = ITEMS.get(item_id, {}).get("axe_power", 0) if item_id else 0
        return max(self.pick_power, tool_power)

    def _mining_power_for(self, block_id):
        if block_id in ALL_LOGS or block_id in ALL_LEAVES:
            return max(self.effective_pick_power, self.effective_axe_power)
        return self.effective_pick_power

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), PLAYER_W, PLAYER_H)

    @property
    def center_px(self):
        return (int(self.x + PLAYER_W // 2), int(self.y + PLAYER_H // 2))
