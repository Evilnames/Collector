# Player-Run Cities

## Overview

Players can establish and grow their own settlement by placing a **City Block** and attracting NPCs to fill roles in their economy. Cities require active management — feeding, paying, and assigning workers — and grow organically around the player's infrastructure.

---

## A. City Block

- A craftable block placed by the player to mark the city center.
- Defines a **city region** (e.g., ±80 tiles horizontally, full vertical range of the chunk column).
- Displays the city name, coat of arms, and population count when interacted with.
- Only one City Block per city. A player could theoretically establish multiple cities but each is independent.
- The City Block stores:
  - City name (player-set)
  - Coat of arms (player-designed, see Section F)
  - Treasury (coin balance for NPC wages)
  - Food reserve reference (scans chests in region)
  - Roster of claimed NPC beds and their occupants

---

## B. NPC Attraction

- Every **bed** placed within the city region has a daily chance to attract a wandering NPC.
- Attraction roll happens at dawn each in-game day.
- **Base attraction chance**: ~15% per empty bed per day.
- Modifiers:
  - +5% per chest of food available in the region
  - +10% if a Tavern/Inn building is present (future building type)
  - -5% per unemployed NPC already in city (overcrowding deterrent)
- When attracted, an NPC spawns near the City Block and "claims" that bed.
- Each NPC is procedurally generated with a name, appearance, and stat spread (see Section C).
- A notification alerts the player: *"A traveler has arrived in [City Name] and is seeking work."*

---

## C. NPC Hiring & Stats

### Hiring
- Attracted NPCs are **unhired** by default — they wander the city region and sleep in their bed.
- The player interacts with them to open a **Hire panel** showing:
  - Name, portrait, personality trait (hardworking / lazy / skilled / clumsy / etc.)
  - Stat spread (see below)
  - Requested daily wage (varies by stat quality)
- Player accepts or declines. Declined NPCs leave after 2 days.

### Stats
Each NPC rolls values (1–10) across six stats at generation:

| Stat | Relevant Jobs |
|------|--------------|
| **Strength** | Mining, Hauling |
| **Agility** | Farming, Taming |
| **Craft** | Crafting (future job type) |
| **Endurance** | All jobs (affects work hours/day) |
| **Intelligence** | Job efficiency bonuses |
| **Animal Affinity** | Taming jobs |

- Stats influence output rates and failure chances on their assigned job.
- NPCs can slowly gain stat XP over time from working their assigned role.

---

## D. Upkeep: Food & Wages

### Food
- Each NPC consumes **1 food item per day** from any chest within the city region.
- Food priority: cooked meals > raw food > crops (in that order).
- If no food is available for 2 consecutive days, the NPC becomes **disgruntled** (reduced output).
- After 3 days without food, the NPC **leaves the city**.

### Wages
- Each NPC has a daily coin wage stored in their hire record.
- Wages are paid automatically at dawn from the **City Block treasury**.
- Player deposits coins into the City Block to top up the treasury.
- If the treasury runs dry for 2 days, NPCs become disgruntled.
- After 3 unpaid days, NPCs leave.

### Disgruntled State
- Shown visually (slumped posture or visual indicator above head).
- Output rate drops by 50%.
- Player can speak to the NPC to see the complaint and resolve it.

---

## E. Jobs

NPCs are assigned a job via the City Block management panel or by interacting with the NPC directly.

---

### Farming Job
- NPC is assigned a **farm region** (player marks a rectangular area).
- Behavior loop:
  1. Till untilled soil in region.
  2. Plant seeds (pulled from assigned chest).
  3. Water crops if a water source is nearby.
  4. Harvest mature crops and deposit into assigned output chest.
- NPCs can move freely around the farm region — not stationary like automations.
- Agility stat affects harvest speed; Intelligence affects seed efficiency (fewer wasted).
- Multiple farm workers can share a region without conflict.

---

### Mining Job
- Player places a **Mining Post block** (new block) in or near a rock/ore deposit.
- NPC is assigned to a Mining Post.
- The Mining Post has configurable settings:
  - **Radius**: how far the miner digs (1–5 tiles from post, default 3).
  - **Target material**: all, ores only, stone only, specific block type.
  - **Depth limit**: max downward distance.
- Behavior loop:
  1. NPC mines blocks in the configured region, working outward from the post.
  2. Deposits resources into the nearest chest or an assigned output chest.
  3. When the region is exhausted, NPC idles at the post.
- Strength stat affects mining speed; Endurance affects how many hours per day they mine.
- Player must relocate the Mining Post or reassign the miner when a vein runs out.

---

### Hauling Job
- NPC is assigned a **source chest** and a **destination chest**.
- Configurable filters: move all items, move only a specific item type, move up to N items.
- Behavior loop:
  1. Walk to source chest, pick up items matching the filter.
  2. Walk to destination chest, deposit items.
  3. Repeat on a cooldown (faster with higher Agility + Strength).
- Useful for moving farm output to a storage vault, or ore to a smelter chest.
- Multiple haulers can share source/destination without conflict.

---

### Taming Job
- NPC is assigned an **animal pen region**.
- Behavior loop:
  1. Tends animals in the pen (feeds them from assigned feed chest, reduces disease chance).
  2. Milks cows/goats when ready and deposits milk into assigned output chest.
  3. Collects eggs from chickens (future).
  4. Shears sheep (future).
- Animal Affinity stat directly improves milk yield and reduces animal stress.
- Agility affects tending speed.
- A single Tamer can manage up to (5 + Animal Affinity) animals efficiently.

---

### Job Assignment Rules
- An NPC can only hold **one job at a time**.
- Jobs can be reassigned freely from the City Block panel.
- Unassigned hired NPCs wander the city region and consume food/wages without producing.

---

## F. Coat of Arms Designer

Accessed through the City Block interaction menu under **"City Identity"**.

### Components
- **Shield shape**: 5–8 options (heater, roundel, lozenge, kite, etc.)
- **Background**: solid color or simple pattern (stripes, quarters, diagonal)
- **Charge** (symbol on the shield): ~30 options drawn from game's existing icon set
  - Animals: wolf, eagle, horse, fish, bear, boar, stag
  - Tools: hammer, pickaxe, bow, sword, anvil
  - Nature: tree, wheat, mountain, wave, sun, moon
  - Heraldic: crown, star, cross, fleur-de-lis, chevron
- **Colors**: full color picker for background, pattern, and charge
- **City Banner**: the coat of arms is displayed on a banner block that can be crafted and placed anywhere

### Usage
- Displayed on the City Block panel header.
- Shown in NPC "hometown" references.
- Printable on **Banner blocks** placed decoratively in the city.
- Future: used in diplomacy or trade if inter-city systems are added.

---

## Data & Implementation Notes

### New Blocks Needed
- `CITY_BLOCK` — the city anchor/management block
- `MINING_POST_BLOCK` — assigns a miner's work zone
- `BANNER_BLOCK` — displays the coat of arms

### New UI Panels Needed
- **City Overview panel** — population, treasury, food status, job roster
- **Hire NPC panel** — stats, wage, accept/decline
- **Job Assignment panel** — per-NPC job config with region/chest pickers
- **Coat of Arms designer** — shield, charge, color selectors

### Save Data
City data stored per City Block instance:
```
{
  name: str,
  coat_of_arms: { shape, bg_color, pattern, charge, charge_color },
  treasury: int,
  npcs: [ { id, bed_pos, job, job_config, stats, wage, days_unpaid, days_unfed } ]
}
```

### NPC Behavior Loop (per dawn tick)
1. Check food availability → consume or increment `days_unfed`
2. Check treasury → pay wage or increment `days_unpaid`
3. If `days_unfed >= 3` or `days_unpaid >= 3` → NPC leaves
4. If either >= 2 → set disgruntled flag
5. Execute job action for the day

### Attraction Roll (per dawn tick, per empty bed)
1. Count food chests, unemployed NPCs in region
2. Compute attraction chance
3. Roll — on success, generate NPC and spawn near City Block

---

## Open Questions / Future Extensions
- **City upgrades**: unlock more bed slots or job types by building specific structures.
- **NPC relationships**: NPCs that like each other work better near each other.
- **Inter-city trade**: two player cities (or player + NPC city) can set up hauler trade routes.
- **Raids / defense**: hostile mobs target city NPCs; players build walls and hire guards.
- **NPC morale system**: festivals, decorations, and amenities boost happiness and output.
