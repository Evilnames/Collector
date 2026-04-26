# Gambling Table Mini-Game

A dice gambling mini-game played at a `GAMBLING_TABLE` block placed inside every inn. Player presses E to open the table. Pure gold economy — no inventory items involved.

---

## Game Flow

1. **Bet phase** — pick 10 / 25 / 50 / 100 gold. "Play" advances.
2. **Pick phase** — pick a number 2–12. Bots have already secretly picked.
3. **Roll phase** — 0.5 s animated dice (faces cycle randomly), then lock.
4. **Result phase** — all picks revealed, winner announced, gold updated. "Play Again" resets to bet; "Leave" closes.

**Winner logic**: `distance = |pick – roll|`. Lowest distance wins.
- Sole winner: net = +num_bots × bet
- Tie (N tied): pot split evenly (net = +(pot/N) – bet)
- Loser: net = -bet

**Bot picks**: weighted toward common 2d6 outcomes (`random.choices(range(2,13), weights=[1,2,3,4,5,6,5,4,3,2,1])[0]`) then ±1 noise clamped to [2,12]. 3 bots by default (named Aldric, Mira, Torvald, Sable).

---

## Files to Create / Modify

### `blocks.py`
- Add `GAMBLING_TABLE = 1177` after `POMEGRANATE_FRUIT_CLUSTER = 1176` (line 1221).
- Add to `BLOCKS` dict: `{"name": "Gambling Table", "hardness": float('inf'), "color": (20, 80, 40), "drop": None}`
- Add to `EQUIPMENT_BLOCKS` set.

### `renderer.py`
- Import `GAMBLING_TABLE`.
- Draw block: dark green felt (20,80,40), lighter center rect, 1px white border, two small dice squares with pip circles.

### `UI/gambling.py` — New file
`GamblingMixin` class. State variables initialized in `UI/__init__`:

| Variable | Type | Default |
|---|---|---|
| `gambling_open` | bool | False |
| `_gamble_phase` | str | "bet" |
| `_gamble_bet` | int | 10 |
| `_gamble_num_bots` | int | 3 |
| `_gamble_bot_picks` | list | [] |
| `_gamble_player_pick` | int? | None |
| `_gamble_roll_timer` | float | 0.0 |
| `_gamble_roll_result` | int? | None |
| `_gamble_die1` | int | 1 |
| `_gamble_die2` | int | 1 |
| `_gamble_result_msg` | str | "" |
| `_gamble_net_gold` | int | 0 |
| `_gamble_rects` | dict | {} |

**Methods:**
- `open_gambling_table(num_bots)` — resets state, sets `gambling_open = True`
- `_draw_gambling(player, dt)` — dark overlay, 560×420 felt panel, delegates to phase draw methods
- `_draw_gamble_bet(player)` — 4 bet buttons, Play/Close
- `_draw_gamble_pick(player)` — 11 number buttons (2–12), Roll/Close
- `_draw_gamble_rolling(player, dt)` — advance timer, animate dice, call `_compute_gamble_result` at 0.5s
- `_draw_gamble_result(player)` — dice, roll total, all picks by name, win/lose label, Play Again/Leave
- `_compute_gamble_result(player)` — compute distances, determine winner(s), update `player.money`
- `handle_gambling_click(pos, player)` — dispatch on phase + rect key
- `handle_gambling_keydown(key, player)` — ESC: pick→bet, else close

**Pip helper (module-level):**
```python
_PIP_POSITIONS = {
    1:[(3,3)], 2:[(1,1),(5,5)], 3:[(1,1),(3,3),(5,5)],
    4:[(1,1),(5,1),(1,5),(5,5)], 5:[(1,1),(5,1),(3,3),(1,5),(5,5)],
    6:[(1,1),(5,1),(1,3),(5,3),(1,5),(5,5)]
}
def _draw_die_face(surface, x, y, size, value):
    cell = size // 6
    pygame.draw.rect(surface, (235,235,235), (x,y,size,size), border_radius=4)
    pygame.draw.rect(surface, (50,50,50), (x,y,size,size), 1, border_radius=4)
    pip_r = max(2, size//12)
    for (px,py) in _PIP_POSITIONS[value]:
        pygame.draw.circle(surface, (30,30,30), (x+px*cell, y+py*cell), pip_r)
```

### `UI/__init__.py`
- `from .gambling import GamblingMixin`
- Add to `class UI(...)` inheritance.
- Initialize all state vars in `__init__()`.
- In `draw()`: `if self.gambling_open: self._draw_gambling(player, dt)`

### `main.py`
- `_close_all_ui()` (~line 525): add `ui.gambling_open = False`
- `_any_ui_open()` (~line 534): add `ui.gambling_open`
- Equipment dispatch (~line 1072, before final `else`):
  ```python
  elif equip == GAMBLING_TABLE:
      ui.open_gambling_table(3)
      ui.refinery_open = False
  ```
- KEYDOWN block: `if ui.gambling_open: ui.handle_gambling_keydown(event.key, player)`
- MOUSEBUTTONDOWN block: `elif ui.gambling_open: ui.handle_gambling_click(event.pos, player)`
- Import `GAMBLING_TABLE` with other block imports.

### `cities.py`
- Import `GAMBLING_TABLE`.
- In `_place_inn()` (line 3507), after the rug loop, place the table at the rightmost interior position:
  ```python
  table_x = left_x + width - 2
  if 0 <= sy < world.height:
      world.set_block(table_x, sy, GAMBLING_TABLE)
  ```
  Safe for all inn widths (minimum 4 → interior +1 to +2).

---

## Verification
1. Generate a new world; find a city with an inn.
2. Press E near the gambling table — panel opens in bet phase.
3. Select a bet, pick a number, watch dice animate and lock.
4. Confirm gold changes correctly for win / lose / tie.
5. ESC from pick → back to bet; ESC from bet/result → closes.
6. `_close_all_ui()` clears the panel and restores movement.
