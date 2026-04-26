# Region Expansion — Diplomacy, Economy, Landmarks

## Context

Regions in CollectorBlocks today are richly *flavored* but thinly *played*. The `Region` dataclass ([towns.py:856-869](../towns.py#L856-L869)) carries `name`, `biome_group`, `tagline`, `leader_title`, `agenda`, `relations`, `coat_of_arms` — all driven by 9 data tables in [towns.py](../towns.py) and a clean `add-region` workflow ([.claude/skills/add-region/SKILL.md](../.claude/skills/add-region/SKILL.md)).

Where regions move gameplay today (and only here):

- Trade contract weighting ([cities.py:1776-1815](../cities.py#L1776-L1815))
- Shop specialty scoring + agenda-match shop size bump ([cities.py:1420-1450](../cities.py#L1420-L1450))
- High-rep buffs: mercantile stock, pious blessings, builder bonds ([towns.py:1343-1389](../towns.py#L1343-L1389))
- LeaderNPC greeting text ([towns.py:628](../towns.py#L628))
- Allied/rival relations ([towns.py:479-512](../towns.py#L479-L512)) — *computed but only used for quarter-strength reputation share*

Goal: take regions from "named flavor" to "felt geography" by wiring three independent vectors that each give regions a measurable identity — diplomatic (A), economic (C), physical (D).

## Sequencing

Land in this order so each phase de-risks the next:

1. **A — Relations** (no schema, instantly visible)
2. **C — Wealth/Danger** (one schema bump; informs D's calibration)
3. **D — Capital landmarks** (uses C's wealth for spawn quality)

---

## Vector A — Make `relations` matter

`compute_relations()` already builds a real diplomacy graph that no system reads. Wire it into existing systems rather than building new ones.

The player's "diplomatic anchor" = the region with the highest aggregate reputation (sum of member-town `reputation`). Add a helper `anchor_region_id()` in [towns.py](../towns.py) that returns this. No player-side state needed since rep already lives on Towns.

### A1 — Allied/rival pricing in shops

Bake the relation multiplier into `_rep_discount` ([cities.py:1366](../cities.py#L1366)) so it propagates through every existing buy path (Merchant, Blacksmith, Scholar, Tavern, Garrison, Shrine):

- Anchor region allied to shop's region → ×0.90
- Anchor region rival to shop's region → ×1.10
- Same region or no anchor → ×1.00

Use `relation_between(anchor_id, npc_region_id)` ([towns.py:458](../towns.py#L458)).

### A2 — Rival contract refusals

In `_pick_contract_for_region` ([cities.py:1776](../cities.py#L1776)), if the requesting region is rival to the player's anchor, return `None` 50% of the time. `LeaderNPC.__init__` and `_new_contract` ([cities.py:1820-1835](../cities.py#L1820-L1835)) skip `None` results, so rival capitals end up with shorter contract lists.

### A3 — Reputation cascade

Where reputation is awarded:
- `execute_contract` already shares ¼ rep to allies ([cities.py:1860-1871](../cities.py#L1860-L1871)). Extend this same pattern to rival regions: −10% rep there.
- `supply_need_with_player_items` ([towns.py:1326](../towns.py#L1326)) only updates the source town today. Add the same allied/rival cascade so casual supply-filling also moves regional politics.

Use `allied_region_ids()` / `rival_region_ids()` ([towns.py:465-476](../towns.py#L465-L476)).

### A4 — Surface diplomacy in UI

The leader info card ([UI/panels.py:924-950](../UI/panels.py#L924-L950)) already shows agenda. Add two lines below the agenda chip:

- "Allied: [comma-separated region names]" (green tint)
- "Rival: [comma-separated region names]" (red tint)

Truncate to 2-3 names with "…" if long.

---

## Vector C — Wealth + danger fields

Add two derived axes to the `Region` dataclass to give regions an economic and physical identity beyond agenda.

### C1 — Schema

Extend `Region` ([towns.py:856-869](../towns.py#L856-L869)):

```python
wealth: str = "modest"   # "poor" | "modest" | "rich"
danger: str = "calm"     # "calm" | "rough" | "wild"
```

Derive deterministically in `init_towns()` ([towns.py:896](../towns.py#L896)) using a per-region seeded `random.Random(world.seed ^ region_id)`:

| Agenda | Wealth bias |
|---|---|
| mercantile, builder | rich-skewed |
| pious, scholarly | modest-skewed |
| martial, hedonist | even split |

| Biome group | Danger bias |
|---|---|
| steppe, jungle, desert, wasteland | wild-skewed |
| mediterranean, coastal, levant | calm-skewed |
| everything else | rough-skewed |

### C2 — Wealth effects

- **Shop stock**: rich +1, poor −1 stock slot at [cities.py:1444-1472](../cities.py#L1444-L1472).
- **Contract reward**: rich ×1.25, poor ×0.8 in [cities.py:1776-1815](../cities.py#L1776-L1815).
- **Growth pace**: rich towns hit growth thresholds 25% faster, poor 25% slower in [towns.py:1334-1346](../towns.py#L1334-L1346).

### C3 — Danger effects

- **Enemy spawn rate**: in [world.py](../world.py) spawn loop, multiply spawn chance by region.danger tier (calm 0.7, rough 1.0, wild 1.5) when player is in that region's biome belt.
- **Wild loot**: gate one rare drop tier behind "wild" regions only — pick a high-tier ore drop or rare insect/fish variant; check region.danger inside the drop roll.

### C4 — Persistence

- Bump `SAVE_VERSION` in [save_manager.py](../save_manager.py).
- Persist `wealth` and `danger` in the regions row.
- Old saves: re-derive on load using the same seeded function (idempotent, so no migration script needed).

### C5 — UI surface

[UI/panels.py:924-950](../UI/panels.py#L924-L950) — show "Wealth: Rich" and "Danger: Wild" on the leader card, color-coded.

### C6 — Update `add-region` skill

Extend [.claude/skills/add-region/SKILL.md](../.claude/skills/add-region/SKILL.md) with a step describing the biome-group bias tables for wealth/danger so future region authors can tune them.

---

## Vector D — Capital landmarks per agenda

Each capital hosts one structure tied to its leader's `agenda`, making capitals visibly distinct.

| Agenda | Landmark | Effect (one trip per in-game day) |
|---|---|---|
| martial | Arena | Wave-defense mini-event → rep + gold |
| mercantile | Grand Bazaar | +1 rare slot in every shop in region |
| scholarly | Archive | Reveals 1 random recipe codex page |
| pious | Great Shrine | Persistent blessing while inside this region |
| builder | Stoneworks | −20% on block-pack purchases for the day |
| hedonist | Pleasure Garden | +stat buffs for 1 in-game day |

### D1 — Data table

New module [landmarks.py](../landmarks.py) (keeps towns.py from growing further per CLAUDE.md file-size guidance). Each entry: `agenda` key, `name`, `block_offsets` (small footprint, ~5×5), `npc_factory`, `interact_fn`. Mirrors how `PALACE_TYPES` works in palaces.

### D2 — Placement

Capitals already place a palace. Mirror that scaffolding in [cities.py](../cities.py) to place the landmark at a second slot near the palace. Use `region.wealth` from Vector C to pick a "grand" vs "modest" sprite variant — gives wealth a visible payoff.

### D3 — Renderer

Add draw routines in [renderer.py](../renderer.py) for each landmark block. Six new block IDs (next free per memory: 1072+ — verify in `workflow_add_block.md` memory before allocating). Use `_rng = _rnd.Random(N)` per the renderer-random feedback memory, **never** `_rnd.seed()`.

### D4 — Interaction

One NPC per landmark, simple menu choice → effect. Reuse existing town NPC framework patterns from [outpost_npcs.py](../outpost_npcs.py). No new UI panel needed.

### D5 — Save

Landmark blocks save with the world like any other static structure. NPC state (one-per-day cooldown) is persisted on Region: add `landmark_used_day: int` field.

---

## Critical files

- [towns.py](../towns.py) — Region dataclass, init_towns, relation helpers, growth code, supply cascade
- [cities.py](../cities.py) — shop pricing (`_rep_discount`), contract gen, capital placement
- [UI/panels.py](../UI/panels.py) — leader info card
- [save_manager.py](../save_manager.py) — SAVE_VERSION bump for C
- [renderer.py](../renderer.py) — landmark sprites
- [world.py](../world.py) — enemy spawn rate hook for C3
- **New** [landmarks.py](../landmarks.py) — landmark data + interactions
- [.claude/skills/add-region/SKILL.md](../.claude/skills/add-region/SKILL.md) — extend with wealth/danger biases

## Verification

Each vector ships independently — verify before moving to the next.

**Vector A**

- Generate a world; open ≥3 leader cards — each shows Allies and Rivals.
- With anchor in region R₁, buy from a shop in allied R₂ → −10%; in rival R₃ → +10%.
- Provoke a rival contract list — confirm visibly fewer contracts than from a neutral region.
- Earn rep at one town and watch allied regions also gain rep; rivals drop slightly.

**Vector C**

- Load an *old* save and confirm wealth/danger appear without crashes (re-derived from seed).
- Spawn into a "rich" region — confirm shops have +1 slot, contracts pay more, growth bar fills faster.
- Spawn into a "wild" region — confirm enemies appear ~50% more often, the gated rare drop appears.
- Leader card shows the new fields.

**Vector D**

- Visit each agenda type's capital and confirm the matching landmark exists with correct sprite.
- Trigger each effect once and confirm the daily cooldown gates a second use.
- Confirm "rich" capitals show the grand variant.
- Save/reload and confirm cooldown state and structures persist.
