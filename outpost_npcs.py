from cities import NPC, AmbientNPC, _CLOTHING_PALETTES
import outposts

# ---------------------------------------------------------------------------
# Unique clothing palettes per outpost type
# Falls through to _CLOTHING_PALETTES for shared keys (mediterranean, desert, etc.)
# ---------------------------------------------------------------------------

OUTPOST_CLOTHING = {
    "winemaker": {
        "body": (120, 60, 80), "leg": (70, 45, 35), "skin": (220, 180, 125),
        "trim": (160, 110, 50), "hat": (180, 140, 60),
        "armor": (100, 70, 30), "plate": (150, 110, 55),
    },
    "monk": {
        "body": (100, 95, 80), "leg": (90, 85, 70), "skin": (230, 195, 150),
        "trim": (60, 55, 45), "hat": (115, 108, 90),
        "armor": (70, 65, 55), "plate": (120, 115, 100),
    },
    "trapper": {
        "body": (85, 65, 50), "leg": (70, 55, 40), "skin": (240, 200, 155),
        "trim": (130, 95, 55), "hat": (105, 80, 50),
        "armor": (75, 60, 40), "plate": (120, 95, 60),
    },
    "distiller": {
        "body": (50, 55, 70), "leg": (60, 50, 40), "skin": (230, 190, 145),
        "trim": (140, 115, 60), "hat": (80, 75, 60),
        "armor": (45, 50, 65), "plate": (100, 110, 130),
    },
    "plantation_worker": {
        "body": (55, 130, 95), "leg": (80, 60, 40), "skin": (160, 110, 65),
        "trim": (180, 155, 55), "hat": (200, 175, 80),
        "armor": (40, 95, 70), "plate": (70, 120, 90),
    },
    "jungle_healer": {
        "body": (40, 115, 75), "leg": (65, 50, 30), "skin": (145, 95, 55),
        "trim": (195, 165, 45), "hat": (170, 145, 40),
        "armor": (30, 90, 60), "plate": (60, 120, 80),
    },
    "tea_master": {
        "body": (55, 80, 120), "leg": (45, 60, 95), "skin": (240, 205, 165),
        "trim": (20, 20, 30), "hat": (75, 70, 40),
        "armor": (40, 55, 85), "plate": (80, 100, 135),
    },
    "potter": {
        "body": (145, 100, 65), "leg": (120, 85, 55), "skin": (210, 170, 120),
        "trim": (80, 60, 40), "hat": (160, 130, 80),
        "armor": (110, 80, 50), "plate": (160, 130, 90),
    },
    "saltworker": {
        "body": (200, 200, 185), "leg": (185, 180, 160), "skin": (210, 170, 120),
        "trim": (100, 130, 155), "hat": (215, 210, 190),
        "armor": (155, 155, 145), "plate": (200, 195, 185),
    },
    "blacksmith": {
        "body": (55, 50, 55), "leg": (45, 42, 45), "skin": (210, 170, 115),
        "trim": (140, 100, 50), "hat": (70, 65, 60),
        "armor": (50, 45, 50), "plate": (90, 90, 100),
    },
    "fungi_keeper": {
        "body": (95, 120, 80), "leg": (70, 85, 60), "skin": (180, 145, 100),
        "trim": (130, 155, 90), "hat": (105, 130, 75),
        "armor": (75, 100, 65), "plate": (120, 145, 100),
    },
    "alchemist": {
        "body": (75, 55, 105), "leg": (60, 45, 85), "skin": (190, 155, 110),
        "trim": (160, 130, 50), "hat": (90, 70, 120),
        "armor": (60, 45, 90), "plate": (110, 90, 145),
    },
    "coastal": {
        "body": (80, 120, 160), "leg": (200, 190, 155), "skin": (215, 175, 120),
        "trim": (45, 75, 110), "hat": (195, 178, 120),
        "armor": (55, 90, 125), "plate": (90, 130, 165),
    },
    "steppe_nomad": {
        "body": (165, 90, 40), "leg": (135, 95, 50), "skin": (195, 155, 100),
        "trim": (125, 35, 30), "hat": (190, 145, 55),
        "armor": (120, 70, 30), "plate": (175, 130, 55),
    },
    "artisan": {
        "body": (110, 105, 95), "leg": (90, 85, 75), "skin": (220, 180, 130),
        "trim": (145, 120, 70), "hat": (130, 125, 110),
        "armor": (85, 80, 70), "plate": (140, 135, 125),
    },
    "weaver": {
        "body": (180, 80, 130), "leg": (155, 130, 100), "skin": (195, 155, 100),
        "trim": (220, 195, 60), "hat": (195, 155, 185),
        "armor": (145, 60, 105), "plate": (195, 150, 175),
    },
    "lumberjack": {
        "body": (155, 50, 45), "leg": (75, 55, 35), "skin": (220, 175, 125),
        "trim": (90, 60, 35), "hat": (110, 75, 45),
        "armor": (80, 55, 35), "plate": (135, 95, 55),
    },
    "silk_master": {
        "body": (200, 165, 100), "leg": (140, 95, 55), "skin": (225, 185, 140),
        "trim": (140, 60, 110), "hat": (210, 175, 110),
        "armor": (170, 130, 70), "plate": (215, 180, 120),
    },
    # --- Military outpost palettes ---
    "soldier": {
        "body": (80, 90, 75), "leg": (65, 75, 60), "skin": (210, 170, 120),
        "trim": (50, 55, 45), "hat": (70, 78, 65),
        "armor": (100, 110, 90), "plate": (130, 140, 120),
    },
    "fortress_guard": {
        "body": (55, 55, 65), "leg": (45, 45, 55), "skin": (210, 175, 130),
        "trim": (150, 45, 40), "hat": (60, 60, 70),
        "armor": (85, 90, 105), "plate": (115, 118, 130),
    },
    "legion": {
        "body": (175, 145, 90), "leg": (160, 130, 80), "skin": (200, 155, 100),
        "trim": (180, 140, 40), "hat": (165, 140, 75),
        "armor": (135, 110, 65), "plate": (185, 155, 80),
    },
    "warlord": {
        "body": (130, 55, 45), "leg": (110, 75, 50), "skin": (190, 148, 95),
        "trim": (80, 40, 30), "hat": (120, 50, 42),
        "armor": (95, 45, 35), "plate": (155, 90, 65),
    },
    "naval_guard": {
        "body": (45, 65, 120), "leg": (40, 55, 100), "skin": (215, 175, 125),
        "trim": (190, 190, 200), "hat": (35, 50, 95),
        "armor": (55, 80, 140), "plate": (100, 115, 160),
    },
    "polynesian": {
        # Tapa bark-cloth, warm Pacific brown skin
        "body": (210, 130, 60), "leg": (240, 210, 150), "skin": (175, 130, 80),
        "trim": (90, 55, 25), "hat": (225, 180, 80),
        "armor": (130, 100, 50), "plate": (200, 165, 90),
    },
    # Shared cultural keys — delegate to cities' palettes
    "mediterranean": None,
    "desert":        None,
    "alpine":        None,
    "south_asian":   None,
    "east_asian":    None,
}


def _resolve_clothing(key: str) -> dict:
    local = OUTPOST_CLOTHING.get(key)
    if local is not None:
        return local
    return _CLOTHING_PALETTES.get(key, _CLOTHING_PALETTES["temperate"])


def _all_needs_met(op: outposts.Outpost) -> bool:
    return all(nd["supplied"] >= nd["required"] for nd in op.needs.values())


# ---------------------------------------------------------------------------
# NPC class
# ---------------------------------------------------------------------------

class OutpostKeeperNPC(NPC):
    """Stationary keeper for any outpost type. Handles buy/sell/needs."""

    def __init__(self, x, y, world, outpost_id: int, outpost_type: str):
        super().__init__(x, y, world, "npc_outpost_keeper")
        self.outpost_id   = outpost_id
        self.outpost_type = outpost_type
        otype             = outposts.OUTPOST_TYPES[outpost_type]
        self.clothing     = _resolve_clothing(otype["clothing_key"])
        self.display_name = otype["display_name"]
        self.sells        = otype["sells"]   # [(item_id, base_cost)]
        self.buys         = otype["buys"]    # [(item_id, base_pay, max_qty)]

    # ------------------------------------------------------------------
    # Price helpers
    # ------------------------------------------------------------------

    def _op(self) -> outposts.Outpost | None:
        return outposts.OUTPOSTS.get(self.outpost_id)

    def needs_met(self) -> bool:
        op = self._op()
        return op is None or _all_needs_met(op)

    def sell_cost(self, idx: int) -> int:
        _, base = self.sells[idx]
        mult = 1.0 if self.needs_met() else 1.25
        return max(1, round(base * mult))

    def buy_pay(self, idx: int) -> int:
        _, base, _ = self.buys[idx]
        mult = 1.15 if self.needs_met() else 0.85
        return max(1, round(base * mult))

    # ------------------------------------------------------------------
    # Buy from keeper
    # ------------------------------------------------------------------

    def can_afford(self, idx: int, player) -> bool:
        return player.money >= self.sell_cost(idx)

    def in_stock(self, idx: int) -> bool:
        op = self._op()
        if op is None:
            return True
        item_id = self.sells[idx][0]
        return op.stock.get(item_id, 0) > 0

    def execute_purchase(self, idx: int, player) -> bool:
        if not self.can_afford(idx, player) or not self.in_stock(idx):
            return False
        item_id, _ = self.sells[idx]
        player.money -= self.sell_cost(idx)
        player._add_item(item_id)
        op = self._op()
        if op:
            op.stock[item_id] = max(0, op.stock.get(item_id, 0) - 1)
        return True

    # ------------------------------------------------------------------
    # Sell to keeper
    # ------------------------------------------------------------------

    def can_sell_to(self, idx: int, player) -> bool:
        item_id, _, _ = self.buys[idx]
        return player.inventory.get(item_id, 0) >= 1

    def execute_sell(self, idx: int, player) -> bool:
        item_id, _, max_qty = self.buys[idx]
        qty = min(player.inventory.get(item_id, 0), max_qty)
        if qty < 1:
            return False
        player.inventory[item_id] = player.inventory.get(item_id, 0) - qty
        if player.inventory[item_id] <= 0:
            del player.inventory[item_id]
            for i in range(len(player.hotbar)):
                if player.hotbar[i] == item_id:
                    player.hotbar[i] = None
        player.money += self.buy_pay(idx) * qty
        # Credit supplied for this item if it's in outpost needs
        op = self._op()
        if op and item_id in op.needs:
            op.needs[item_id]["supplied"] = min(
                op.needs[item_id]["supplied"] + qty,
                op.needs[item_id]["required"],
            )
            op.last_resupply_day = getattr(self.world, "day_count", 0)
        return True

    # ------------------------------------------------------------------
    # Supply delivery (meets outpost needs, small gold token reward)
    # ------------------------------------------------------------------

    def supply_items(self) -> list[tuple[str, int, int]]:
        """Returns [(item_id, still_needed, small_gold_per_unit)] for each unmet need."""
        op = self._op()
        if op is None:
            return []
        from items import ITEMS
        result = []
        for item_id, nd in op.needs.items():
            still = nd["required"] - nd["supplied"]
            if still > 0:
                # Token reward: ~20% of a typical trade value
                base_val = ITEMS.get(item_id, {}).get("_supply_value", 2)
                result.append((item_id, still, max(1, base_val)))
        return result

    def can_supply(self, item_id: str, player) -> bool:
        return player.inventory.get(item_id, 0) >= 1

    def execute_supply(self, item_id: str, player) -> bool:
        op = self._op()
        if op is None or item_id not in op.needs:
            return False
        nd = op.needs[item_id]
        still_needed = nd["required"] - nd["supplied"]
        qty = min(player.inventory.get(item_id, 0), still_needed)
        if qty < 1:
            return False
        player.inventory[item_id] = player.inventory.get(item_id, 0) - qty
        if player.inventory[item_id] <= 0:
            del player.inventory[item_id]
            for i in range(len(player.hotbar)):
                if player.hotbar[i] == item_id:
                    player.hotbar[i] = None
        nd["supplied"] = min(nd["supplied"] + qty, nd["required"])
        op.last_resupply_day = getattr(self.world, "day_count", 0)
        # Small token reward per unit delivered
        _SUPPLY_PAY = {"lumber": 2, "coal": 3, "iron_chunk": 4, "stone_chip": 1,
                       "coarse_salt": 2, "gold_nugget": 8}
        pay = _SUPPLY_PAY.get(item_id, 2) * qty
        player.money += pay
        return True

    # ------------------------------------------------------------------
    # Status text for UI
    # ------------------------------------------------------------------

    def needs_status_lines(self) -> list[str]:
        op = self._op()
        if op is None:
            return ["Well-stocked. Best prices available."]
        missing = []
        for item_id, nd in op.needs.items():
            if nd["supplied"] < nd["required"]:
                still = nd["required"] - nd["supplied"]
                from items import ITEMS
                name = ITEMS.get(item_id, {}).get("name", item_id)
                missing.append(f"Needs {still}x {name}")
        if not missing:
            return ["Well-stocked. Best prices available."]
        return missing

    def stock_line(self, idx: int) -> str:
        op = self._op()
        item_id = self.sells[idx][0]
        if op is None:
            return ""
        qty = op.stock.get(item_id, 0)
        return f"In stock: {qty}"


# ---------------------------------------------------------------------------
# Military soldier NPCs — ambient patrols for military outpost types
# ---------------------------------------------------------------------------

_OUTPOST_ARMOR_TYPE = {
    "border_garrison":   "mail",
    "highland_fortress": "plate",
    "desert_legion":     "lorica",
    "steppe_warcamp":    "leather",
    "coastal_citadel":   "naval",
}


class MilitarySoldierNPC(AmbientNPC):
    """Ambient guard that patrols a military outpost. Drawn with outpost-specific armor."""
    is_ambient = True

    def __init__(self, x, y, world, outpost_type: str, clothing: dict, patrol_half: int = 30):
        super().__init__(x, y, world, "npc_soldier", patrol_half=patrol_half)
        self.armor_type  = _OUTPOST_ARMOR_TYPE.get(outpost_type, "mail")
        self.clothing    = clothing
        self._walk_speed = 18.0
        self._pause_max  = 4.5
