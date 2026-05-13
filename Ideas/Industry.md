Ready for review
Select text to add comments on the plan
Industrial Scaling — From Solo Miner to Production Empire
Context
The game currently peaks at Crystal Miners + Crystal Farm Bots + settler city management. That's powerful but still feels like assisted manual play — you're still the bottleneck between extraction, processing, and sale. The goal is a second act where the player builds interconnected systems that run passively, so the joy shifts from "doing things" to "watching the machine work."

Player target: Mostly passive / Factorio-style — set up infrastructure, then check in to top off fuel and adjust routes.

Four Pillars (implement in this order — each feeds the next)
Pillar 1: Processing Chain
What it adds: Factory machines that auto-convert raw materials without the player standing at a crafting bench.

New blocks (in blocks.py + items.py):

CRUSHER — ore → ore concentrate (2:1 ratio)
SMELTER — ore/concentrate → metal bar
ALLOY_FURNACE — bar + fuel → alloy (steel, bronze, etc.)
PIPE (3 tiers: wood/iron/crystal) — routes items between machines and chests
PIPE_SORTER — reads item type, routes to left/right output
How it works:

Each factory block has an input slot (chest-like), output slot, fuel slot, and progress bar
Every game tick, if fueled and input available, it processes one batch
Pipes connect block-to-block or block-to-chest; items physically move at pipe tier speed
The player draws the layout; automation handles throughput
Wire system already exists — factories halt when adjacent wire is present but unpowered (same pattern as miners in automations.py)
Progression arc:

Early: place a Smelter, hand-fill it, pick up bars manually — faster than the forge
Mid: Crusher → Smelter → chest, all piped. Iron flows hands-free
Late: branching sorter networks. Crystal ore → crystal branch, iron ore → iron branch, all feeding into a shared output chest room
Key files: blocks.py, items.py, automations.py (reuse miner tick pattern), world.py (entity tick registration), Render/blocks_crafting.py (draw functions), UI/crafting.py (factory UI panel), crafting.py (recipes for factory blocks themselves)

Pillar 2: Depth Engine
What it adds: Vertical shaft infrastructure that turns deep zones into a facility, not an expedition.

New blocks:

ORE_LIFT — vertical pipe; moves items upward one block per tick against gravity
FUEL_LINE — vertical pipe; moves fuel items downward
DEEP_STATION — coordinator block (placed at shaft bottom); owns a large fuel reservoir, coordinates up to 4 adjacent Crystal Miners, routes their output into the trunk Ore Lift
How it works:

Player digs a vertical shaft, lines it with Ore Lift segments, places Deep Station at depth
Deep Station draws fuel from Fuel Line above (player tops off surface chest)
Miners adjacent to the Deep Station output into it; it feeds the Ore Lift
Ore Lift delivers ore to a surface chest the player never has to descend for
Multiple Deep Stations at different depth tiers (mid ~40, deep ~100, core ~160) each connect to the same shaft
Progression arc:

Early: single Ore Lift reduces "visit the miner" trips to "check the surface chest"
Mid: Deep Station + Fuel Line — player only touches the surface fuel chest every few in-game days
Late: 3-level shaft with a Deep Station per level; surface looks like a pit head, ore streams upward constantly
Research gates: The existing depth gate nodes (~40/100/160) in research.py naturally unlock each Deep Station tier — no new research columns needed, just add the factory unlock to existing nodes.

Key files: blocks.py, items.py, automations.py (Deep Station tick logic, mirrors FarmBot coordinator pattern), world.py, Render/blocks_crafting.py

Pillar 3: Settler Specialization
What it adds: Settlers accumulate job XP → Foreman tier → behavioral upgrades. Guild Hall building amplifies a whole job type passively.

Changes to existing settler records (player_cities.py):

Add job_xp: int and job_tier: int (0=basic, 1=senior, 2=foreman) to settler dict
Each _job_* function awards XP per action (harvest, ore mined, item hauled)
Tier thresholds: 100 XP → Senior, 300 XP → Foreman
Foreman perks by job (behavioral changes, not stat %):

Mining Foreman: oversees one adjacent junior miner settler; combined output counts as 2× speed
Farming Foreman: rotates crop types each season (not locked to one configured crop)
Hauling Foreman: can be assigned to a Caravan (Pillar 4) — increases carry capacity
Cook Foreman: unlocks multi-ingredient meal recipes (satisfies town food needs list, not just city settlers)
Logging Foreman: auto-replants saplings (currently logging only chops)
Taming Foreman: produces artisan goods (aged cheese, fine wool) in addition to milk/eggs
Guild Hall:

New building type in player_cities.py build options
Requires: 1 Foreman of job type + building materials
Effect: all settlers of that job type in the city gain +20% efficiency passively
Attracts new settlers who arrive pre-assigned to that job (start at Senior tier)
One Guild Hall per job type max (6 max per city)
Progression arc:

Early: notice high-strength settlers mine faster — start assigning deliberately
Mid: first Foreman emerges; player moves them to the bottleneck job
Late: full Guild Hall set for a specialized city (Mining City vs Farming City feel distinct)
Key files: player_cities.py (settler records, _job_* functions, _daily_city_tick), cities.py (NPC building definitions for Guild Hall), UI/panels.py (settler detail panel — show XP/tier)

Pillar 4: Trade Network
What it adds: Automated caravan routes between city ↔ outposts ↔ towns. Passive daily profit from production output.

New items: WAGON (craftable, requires horse + wagon kit) — a rideable item that becomes the caravan vehicle

New system: caravans (new file caravans.py):

CARAVAN_ROUTES: list[dict] — each route: {name, stops: [loc_id, ...], carry: {item_id: max_qty}, return_carry: {item_id: max_qty}, days_until_return, settler_id}
Route tick runs in _daily_city_tick: decrement timer; on arrival, sell what destination wants from carry manifest, buy what's configured in return_carry, deposit coin to city treasury
Player assigns a Hauling Foreman settler to a route → carry capacity +50%
CARAVAN_LEDGER UI panel: list of active routes, last profit, days until return
Route configuration: Player places a Caravan Post block at their city, opens UI, selects destination (from known outposts/towns on minimap), sets carry manifest and return manifest. The Wagon "departs" (disappears from city, timer starts). On return it reappears and auto-deposits.

Outpost needs integration: Each outpost already has a needs list in outposts.py. Caravan checks that list for what to bring; checks buys list for what to buy back. No manual configuration needed beyond "route to this outpost."

Town supply contracts: Once a town reaches City tier, the player can establish a Supply Contract: daily caravan fulfills the town's needs list in exchange for town_growth_contribution (speeds up tier-up beyond the current 5-day-per-tier rate).

Progression arc:

Early: player manually trades at outposts. Realizes the friction. Crafts first Wagon.
Mid: 3-4 routes running. Ledger shows passive daily coin. Processing Chain output now routes via caravan automatically.
Late: Caravan Guild building (like Guild Hall) lets player manage 8+ routes from a map overlay. Supply contracts with 2-3 towns means the player's city is feeding the whole region.
Key files: new caravans.py, player_cities.py (hook _daily_city_tick to call caravan tick), outposts.py (read needs/buys for caravan AI), towns.py (supply contract hooks), blocks.py + items.py (Wagon, Caravan Post), UI/panels.py or new UI/caravans.py (Ledger panel)

Implementation Order
Processing Chain — foundational; defines the factory-block pattern other pillars reuse
Depth Engine — extends existing miner pattern; ore now flows to surface automatically
Settler Specialization — extends existing settler system; Foreman roles enable Pillar 4
Trade Network — cap-stone; requires working production (Pillar 1+2) and Hauling Foreman (Pillar 3)
Verification
Place Smelter, load iron chunks, watch bars appear in adjacent chest without touching it
Build a Crusher → Smelter → pipe → chest chain; mine iron ore, confirm bars reach the chest hands-free
Dig to depth 40, place Ore Lift + Coal Miner, confirm ore appears in surface chest
Hire 5 settlers, assign all to Mining, wait 10 in-game days, confirm one reaches Senior tier
Establish a caravan route to any outpost with a needs list, wait one in-game day, confirm coin deposited to treasury
Build a Mining Guild Hall, confirm new settlers arrive pre-assigned to Mining job