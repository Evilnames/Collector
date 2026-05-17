"""New coin-trading NPCs.

Kept separate from cities.py to avoid further bloat. Each NPC class subclasses
NPC and follows the CoinDealerNPC pattern (panel + execute_* methods).
"""
import random
from cities import NPC, _npc_clothing
from coins import (
    coin_price, coin_melt_price, coin_metal, attempt_provenance,
    attempt_regrade, appraise_fee, regrade_fee,
    generate_auction_lots, derive_npc_coin_interest, npc_coin_offer,
    coin_matches_interest,
)


# ---------------------------------------------------------------------------
# Auctioneer — weekly rotating high-rarity lots with simulated AI bidding
# ---------------------------------------------------------------------------

class AuctioneerNPC(NPC):
    """Runs a weekly auction. Player places bids; AI bidders raise until ai_max."""
    SHOP_HOURS = True

    def __init__(self, x, y, world, rng, biodome="temperate"):
        super().__init__(x, y, world, "npc_merchant")
        self.clothing = _npc_clothing(biodome)
        self.clothing["body"] = (90, 55, 120)   # auction purple
        self.clothing["trim"] = (200, 165, 45)
        self.display_name = "Auctioneer"
        self._auction_seed = rng.randint(0, 0x7FFFFFFF)
        self._last_week    = -1
        self._lots: list   = []

    def _current_week(self) -> int:
        return int(getattr(self.world, "day", 0)) // 7

    def _ensure_lots(self, player):
        week = self._current_week()
        if week == self._last_week:
            return
        gen = getattr(player, "_coin_gen", None)
        if gen is None:
            return
        self._lots     = generate_auction_lots(gen, week, self._auction_seed, lot_count=3)
        self._last_week = week

    def min_next_bid(self, idx: int) -> int:
        lot = self._lots[idx]
        if lot["leader"] == "player":
            return lot["current_bid"]      # already winning
        return lot["current_bid"] + max(1, lot["current_bid"] // 12)

    def can_bid(self, idx: int, player) -> bool:
        if not (0 <= idx < len(self._lots)):
            return False
        lot = self._lots[idx]
        if lot["leader"] == "player":
            return False
        return player.money >= self.min_next_bid(idx)

    def place_bid(self, idx: int, player) -> str:
        """Player bids the minimum. Each AI bidder responds: they re-raise if
        their ai_max permits, otherwise they fold. Returns a status string."""
        if not self.can_bid(idx, player):
            return "cannot_bid"
        lot = self._lots[idx]
        bid = self.min_next_bid(idx)
        if player.money < bid:
            return "no_gold"
        # Player takes the lead at `bid`
        lot["current_bid"] = bid
        lot["leader"]      = "player"
        # AI rivals try to overbid until their ai_max is exceeded
        rng = random.Random(self._auction_seed ^ idx ^ lot["current_bid"])
        rivals_left = lot["ai_bidders"]
        while rivals_left > 0:
            raise_amt = lot["current_bid"] + rng.randint(2, max(3, lot["current_bid"] // 10))
            if raise_amt <= lot["ai_max"] and rng.random() < 0.75:
                lot["current_bid"] = raise_amt
                lot["leader"]      = "house"
                rivals_left -= 1
            else:
                break
        return "leader_player" if lot["leader"] == "player" else "outbid"

    def claim(self, idx: int, player) -> bool:
        """Claim a lot the player is winning — pays current_bid, takes the coin."""
        if not (0 <= idx < len(self._lots)):
            return False
        lot = self._lots[idx]
        if lot["leader"] != "player":
            return False
        price = lot["current_bid"]
        if player.money < price:
            return False
        coin = lot["coin"]
        player.money -= price
        player.coins.append(coin)
        player.discovered_coin_types.add(coin.coin_type_id)
        if hasattr(player, "_check_coin_set_complete"):
            player._check_coin_set_complete(coin.civilization_name)
        player.pending_notifications.append(("Auction Won", coin.display_name, coin.rarity))
        self._lots.pop(idx)
        return True


# ---------------------------------------------------------------------------
# Money-Changer — buys & sells coins at flat bullion (melt) price
# ---------------------------------------------------------------------------

class MoneyChangerNPC(NPC):
    """Pays based purely on metal weight (a bullion floor for any coin)."""
    SHOP_HOURS = True

    def __init__(self, x, y, world, rng, biodome="temperate"):
        super().__init__(x, y, world, "npc_merchant")
        self.clothing = _npc_clothing(biodome)
        self.clothing["body"] = (160, 130, 60)
        self.clothing["trim"] = (200, 200, 215)
        self.display_name = "Money-Changer"

    def buy_price(self, coin) -> int:
        return coin_melt_price(coin)

    def sell_price(self, coin) -> int:
        # Sells back at a small markup over melt — never a deal for collectors,
        # but lets you pull a common coin out of bullion if needed.
        return max(1, int(coin_melt_price(coin) * 1.25))

    def execute_sell(self, coin_idx: int, player) -> bool:
        """Player sells a coin from their collection at the melt price."""
        if not (0 <= coin_idx < len(player.coins)):
            return False
        coin  = player.coins.pop(coin_idx)
        price = self.buy_price(coin)
        player.money += price
        player.pending_notifications.append(
            ("Melted", f"+{price}g  {coin.denomination_label}", "common"))
        return True


# ---------------------------------------------------------------------------
# Coin Appraiser — paid identification of provenance / re-grading
# ---------------------------------------------------------------------------

class CoinAppraiserNPC(NPC):
    """Pay a fee to attempt provenance research, or to regrade a coin's condition."""
    SHOP_HOURS = True

    def __init__(self, x, y, world, rng, biodome="temperate"):
        super().__init__(x, y, world, "npc_scholar")
        self.clothing = _npc_clothing(biodome)
        self.clothing["body"] = (70, 95, 130)
        self.clothing["trim"] = (200, 175, 60)
        self.display_name = "Coin Appraiser"
        self._seed = rng.randint(0, 0x7FFFFFFF)
        self._regrade_attempts: dict = {}  # coin.uid → count (max 1)

    def appraise_cost(self, coin) -> int:
        return appraise_fee(coin)

    def regrade_cost(self, coin) -> int:
        return regrade_fee(coin)

    def can_appraise(self, coin, player) -> bool:
        return (not coin.provenance) and player.money >= self.appraise_cost(coin)

    def can_regrade(self, coin, player) -> bool:
        used = self._regrade_attempts.get(coin.uid, 0)
        return used < 1 and player.money >= self.regrade_cost(coin)

    def execute_appraise(self, coin_idx: int, player) -> str:
        if not (0 <= coin_idx < len(player.coins)):
            return "bad_idx"
        coin = player.coins[coin_idx]
        if not self.can_appraise(coin, player):
            return "cannot"
        player.money -= self.appraise_cost(coin)
        rng = random.Random(self._seed ^ (coin.seed or 0) ^ 0xAAAA)
        if attempt_provenance(coin, rng):
            player.pending_notifications.append(
                ("Provenance Found", coin.denomination_label, coin.rarity))
            return "found"
        player.pending_notifications.append(
            ("No Provenance", "Records were inconclusive.", "common"))
        return "nothing"

    def execute_regrade(self, coin_idx: int, player) -> str:
        if not (0 <= coin_idx < len(player.coins)):
            return "bad_idx"
        coin = player.coins[coin_idx]
        if not self.can_regrade(coin, player):
            return "cannot"
        player.money -= self.regrade_cost(coin)
        self._regrade_attempts[coin.uid] = 1
        rng = random.Random(self._seed ^ (coin.seed or 0) ^ 0xBBBB)
        result = attempt_regrade(coin, rng)
        if result == "upgraded":
            player.pending_notifications.append(
                ("Coin Upgraded", f"{coin.denomination_label} → {coin.condition.title()}",
                 coin.rarity))
        elif result == "damaged":
            player.pending_notifications.append(
                ("Coin Damaged", f"{coin.denomination_label} → {coin.condition.title()}",
                 "common"))
        else:
            player.pending_notifications.append(
                ("Regrade Unchanged", coin.denomination_label, "common"))
        return result


# ---------------------------------------------------------------------------
# Coin Collector — generic NPC that pays a premium for one type they fancy
# ---------------------------------------------------------------------------

class CoinCollectorNPC(NPC):
    """An enthusiast who pays premium for a specific kind of coin (set per spawn).
    Stock has no items — pure buyer."""
    SHOP_HOURS = True

    def __init__(self, x, y, world, rng, biodome="temperate"):
        super().__init__(x, y, world, "npc_villager")
        self.clothing = _npc_clothing(biodome)
        self.clothing["body"] = (120, 95, 60)
        self.display_name = "Coin Collector"
        self._spawn_seed = rng.randint(0, 0x7FFFFFFF)
        self._interest: dict | None = None
        # Daily budget so they can't be drained instantly
        self._budget       = 250
        self._last_day     = -1

    def _ensure_interest(self, player):
        if self._interest is not None:
            return
        gen = getattr(player, "_coin_gen", None)
        # Force an interest if none rolled (collectors always want *something*)
        for salt in range(8):
            interest = derive_npc_coin_interest(self._spawn_seed ^ (salt * 911), gen)
            if interest:
                self._interest = interest
                return
        # Last-resort fallback
        self._interest = {"kind": "metal", "value": "silver",
                          "label": "Silver coins", "premium": 1.3}

    def _refresh_budget(self):
        day = int(getattr(self.world, "day", 0))
        if day != self._last_day:
            self._last_day = day
            self._budget   = 250 + (day % 7) * 25

    def offer_for(self, coin) -> int:
        if not self._interest:
            return 0
        return npc_coin_offer(coin, self._interest)

    def can_buy(self, coin) -> bool:
        self._refresh_budget()
        offer = self.offer_for(coin)
        return offer > 0 and self._budget >= offer

    def execute_sell(self, coin_idx: int, player) -> bool:
        """Player sells a matching coin to this collector at the premium offer."""
        if not (0 <= coin_idx < len(player.coins)):
            return False
        coin  = player.coins[coin_idx]
        if not self.can_buy(coin):
            return False
        price = self.offer_for(coin)
        player.coins.pop(coin_idx)
        player.money += price
        self._budget -= price
        player.pending_notifications.append(
            ("Collector Pleased", f"+{price}g  {coin.denomination_label}", coin.rarity))
        return True
