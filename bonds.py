"""Guild-issued bonds.

Each active guild auto-issues one bond every 30 in-game days. Bonds have a
fixed face value, a weekly coupon, and a 30-day maturity. The player buys
bonds from the float; coupons + principal flow back from the guild treasury.

Default behavior: if the guild lacks treasury when a coupon or principal is
due, the bond is marked "defaulted" and the player loses the principal (the
loss is the implicit price of the higher fixed yield vs. equity).
"""

from collections import deque
from dataclasses import dataclass, field
from typing import Optional

from guilds import GUILDS

BOND_FACE_VALUE      = 100
BOND_COUPON_RATE     = 0.015   # 1.5% per week of face value
BOND_MATURITY_DAYS   = 30
BOND_ISSUE_INTERVAL  = 30      # one new bond per active guild every 30 days
BOND_TREASURY_FLOOR  = 50      # guild needs at least this much before issuing


@dataclass
class Bond:
    bond_id:        int
    issuer_guild_id: str
    face_value:     int
    coupon_rate:    float
    issued_day:     int
    maturity_day:   int
    owner_id:       str = "float"    # "float" until sold; "player" after purchase
    coupons_paid:   int = 0
    state:          str = "active"   # active | matured | defaulted


BONDS: dict = {}
_NEXT_ID = [1]


def reset_bonds() -> None:
    BONDS.clear()
    _NEXT_ID[0] = 1


def issue_periodic_bonds(day: int) -> list:
    """Each active guild that hasn't issued a bond in BOND_ISSUE_INTERVAL days
    creates a fresh unsold bond in the float."""
    issued = []
    for g in GUILDS.values():
        if g.state != "active" or g.treasury < BOND_TREASURY_FLOOR:
            continue
        recent = [b for b in BONDS.values()
                  if b.issuer_guild_id == g.guild_id
                  and (day - b.issued_day) < BOND_ISSUE_INTERVAL]
        if recent:
            continue
        bond = Bond(
            bond_id        = _NEXT_ID[0],
            issuer_guild_id = g.guild_id,
            face_value     = BOND_FACE_VALUE,
            coupon_rate    = BOND_COUPON_RATE,
            issued_day     = day,
            maturity_day   = day + BOND_MATURITY_DAYS,
        )
        _NEXT_ID[0] += 1
        BONDS[bond.bond_id] = bond
        issued.append(bond)
    return issued


def buy_bond(bond_id: int, player) -> tuple[bool, int, str]:
    b = BONDS.get(bond_id)
    if b is None or b.state != "active" or b.owner_id != "float":
        return False, 0, "Bond not available."
    cost = b.face_value
    if getattr(player, "money", 0) < cost:
        return False, 0, f"Need {cost}g."
    player.money -= cost
    b.owner_id = "player"
    g = GUILDS.get(b.issuer_guild_id)
    if g is not None:
        g.treasury += cost
    return True, cost, f"Bought 1× {g.name if g else 'guild'} bond at face {cost}g."


def weekly_coupons(day: int, player) -> None:
    """Pay coupons on all active player-held bonds. Default on missed payments."""
    for b in list(BONDS.values()):
        if b.state != "active" or b.owner_id != "player":
            continue
        if (day - b.issued_day) <= 0 or ((day - b.issued_day) % 7) != 0:
            continue
        coupon = int(round(b.face_value * b.coupon_rate))
        g = GUILDS.get(b.issuer_guild_id)
        if g is None or g.state != "active" or g.treasury < coupon:
            b.state = "defaulted"
            continue
        g.treasury -= coupon
        player.money = getattr(player, "money", 0) + coupon
        b.coupons_paid += 1


def daily_maturity_check(day: int, player) -> None:
    """When a bond reaches maturity, return principal to the player."""
    for b in list(BONDS.values()):
        if b.state != "active":
            continue
        if day < b.maturity_day:
            continue
        g = GUILDS.get(b.issuer_guild_id)
        if b.owner_id != "player":
            # Unowned bond expires worthless.
            b.state = "matured"
            del BONDS[b.bond_id]
            continue
        if g is None or g.state != "active" or g.treasury < b.face_value:
            b.state = "defaulted"
            continue
        g.treasury -= b.face_value
        player.money = getattr(player, "money", 0) + b.face_value
        b.state = "matured"
        del BONDS[b.bond_id]


def player_bonds() -> list:
    return [b for b in BONDS.values() if b.owner_id == "player"]


def float_bonds() -> list:
    return [b for b in BONDS.values() if b.owner_id == "float" and b.state == "active"]
