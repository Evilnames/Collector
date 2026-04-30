# CollectorBlocks

A 2D side-scrolling world of discovery built with Python and Pygame. Every world is historically generated — biomes, civilizations, trade routes, and ecosystems that feel like they existed long before you arrived. You are not building the world. You are uncovering it.

---

## The World

Each world is generated with history baked in. Cities have grown along rivers, military outposts guard mountain passes, and hermit monasteries hide in boreal forests. Trade has worn roads between settlements. Animals have migrated to the climates that suit them. Wildflowers seeded themselves across meadows over centuries. You arrive into all of it mid-story, and your job is to explore, document, and understand what was already here.

The terrain spans **23 distinct biomes** — from Mediterranean olive groves and East Asian bamboo coasts to arctic tundra, canyon badlands, dense jungle, and deep swamps. Each biome has its own geology, its own creatures, its own crops, its own flavors. A desert isn't just a reskinned forest. The rocks are different, the insects are different, the clay has a different mineral signature, and the spirits distilled here taste like nowhere else.

Underground, the world goes deep. Caves change character as you descend. Fossil beds from three geological eras — Paleozoic, Mesozoic, Cenozoic — wait in the dark. Crystal deposits, igneous intrusions, ferrous veins, and void-touched formations each have their own logic.

---

## Natural Wonders to Collect

### Birds — 246 Species
Songbirds, raptors, waders, seabirds, and forest specialists all occupy their own ranges. They flock, perch, and nest. If you stand still while a bird is nesting nearby, it may let you observe it close enough to log it. Build **bird feeders** and **nesting boxes** to draw species to you. Each species carries field notes on behavior and habitat.

### Fish — 242 Species
Lakes, rivers, coastal reefs, and ocean deeps each hold different fish. Your rod, your patience, and your biome determine what you pull up. A jungle river fishes nothing like a mountain stream. Catch rates shift with time of day and season.

### Insects — 305 Species
Butterflies, beetles, dragonflies, fireflies, moths, mantids, and more. Each has its own activity window — some emerge at dusk, some only in deep jungle, some only where specific flowers grow. Catching them requires timing and a bug net. A fully catalogued insect collection drives **crop pollination bonuses** across your farms.

### Wildflowers — 171 Species, ~684 Color Variations
Scattered across every biome surface in colors and forms specific to their climate. Some only bloom after rain. Some grow only at altitude. Press them, catalogue them, trade dried specimens with collectors in NPC cities.

### Rocks — 231 Types
From surface pebbles to deep-vein mineralites. Polish them at a rock tumbler, evaluate their luster, and trade with collector NPCs who seek specific regional varieties. Rock types follow biome geology — a desert surface yields nothing like a boreal riverbed.

### Gemstones — 87 Types
Raw gems must be cleaned and cut. Each gem type has its own depth range, optical effects, and possible cuts. Alexandrite shifts color under torchlight. Red Beryl forms only in igneous zones. Diamond requires a cutting mini-game with high failure risk but the highest trade value in the game.

### Fossils — 172 Types, 3 Geological Eras
Dig deep enough and the rock changes. Trilobites and Ammonites from the Paleozoic. Ichthyosaur teeth and ancient feathers from the Mesozoic. Mammoth molars and sabertooth fragments from the Cenozoic. Each fossil comes with provenance — depth found, biome, era — that affects its encyclopaedia entry and collector value.

### Seashells — 65 Species
Wash up on beaches and coastal shallows. Some are common, some appear only after storms, some require diving. A complete shell collection unlocks the Coastal Codex entry.

### Mushrooms
Underground and in forested biomes. Some are edible, some are alchemical components, some glow in the dark.

---

## Artisan Systems

Every craftable consumable system follows a full production pipeline, with biome-specific flavor profiles that make the output from a coastal Mediterranean vineyard taste nothing like a highland Celtic one.

### Wine — 12 Grape Profiles
Harvest grape varieties suited to your biome. Choose from **4 crush styles**, **4 yeast strains**, and **3 vessel types**. Age in cellars. Sell bottles to city merchants or drink for stat buffs that vary by vintage profile.

### Beer — 23 Biome Profiles
Grow hop vines, mash grain in a Brew Kettle, ferment in a Fermentation Vessel, and tap kegs in a Taproom. Output includes 18 distinct beer items, each with biome-specific flavor and buff characteristics.

### Tea — 8 Biome Profiles
Tea bushes grow in highland and tropical biomes. Wither leaves, control oxidation in Oxidation Zones, and cellar for depth. Add herbs from your herbalism collection to create blended teas with stacked buffs.

### Coffee — 13 Biome Profiles
Tropical and subtropical biomes produce coffee cherries with wildly different flavor foundations — from bright citrus to deep chocolate to floral jasmine. Process, roast, grind. Serve at an outpost café or drink for exploration stamina buffs.

### Spirits — 13 Biome Profiles
A full grain-to-barrel pipeline. Still, barrel-age, and bottle spirits whose character is entirely determined by the biome's grain and water source. A Scottish highland whisky and a desert agave spirit are different systems sharing the same architecture.

### Cheese — Milk Source × Aging × Biome
Raise goats, cows, or sheep; collect milk; age in a cheese cave with temperature control. Texture, rind, and flavor shift with animal breed, aging time, and starter culture.

### Pottery — 8 Clay Biome Profiles
Each biome's clay has a mineral signature that affects fired color and texture notes. Throw pots, bowls, and vessels on a wheel mini-game. Trade with settlement merchants who prefer regional ceramic styles.

### Salt — Regional Crystal Varieties
Sea salt from coastal evaporation pans. Rock salt from underground veins. Each region's salt has a distinct flavor profile used in food recipes and as a standalone collector item.

### Textiles — Pattern × Dye × Weave
Raise sheep and process fleece, or harvest plant fibers. Combine dyes from biome flowers, weave patterns on a loom. Textiles feed the clothing economy of NPC cities.

### Herbalism — 15+ Potions and Elixirs
Harvest herb bushes, dry on a Drying Rack, combine in an Alchemist's setup. Recipe discovery is randomized each world — you find a recipe by experimentation or by trading with Herb Monastery outposts. Herbal additives can also be folded into tea for compound effects.

---

## Creatures and Breeding

### Farm Animals — 4 Species, 49 Total Breeds
- **Chickens** — 12 breeds
- **Goats** — 12 breeds
- **Sheep** — 12 breeds
- **Cows** — 13 breeds

Each breed has genetics: coat color, markings, size, milk yield, wool quality, temperament. Breed two animals and their offspring inherits a combination of both lineages, with rare mutations possible. Every animal's family history is tracked — you can trace your prize dairy cow back to the wild goat you first tamed in a mountain biome.

### Dogs — 30 Breeds, 18+ Genetic Attributes
Breed companion dogs with traits for speed, loyalty, herding instinct, and aesthetics. A dog follows you into the deep, alerts you to nearby threats, and can be trained to herd farm animals. The Cynology research column unlocks advanced genetics.

### Horses — Biome-Specific Breeds
Wild horses spawn by biome. Tame, breed, and race them. Racing is a full mini-game with betting and faction reputation stakes.

### Wildlife
Deer, boar, rabbit, and turkey populate the surface world and can be hunted with a bow for meat and hides. The hunting system has its own research column and a fletching table for crafting arrows.

---

## Blocks and Construction

Over **1,200 block IDs** span materials for every building purpose:

| Category | Examples |
|----------|---------|
| **Terrain** | Stone variants, soil types, sand, clay, glacial ice, volcanic rock |
| **Wood** | 10+ tree species: Oak, Birch, Redwood, Jungle, Bamboo, Palm, Breadfruit, and more |
| **Crops** | Dozens of crops with young and mature stages — wheat, rice, coffee cherry, grape, tea bush, hops, herbs, and more |
| **Crafting Stations** | Bakery, Wok, BBQ Grill, Clay Pot, Steamer, Noodle Pot, Juicer, Brew Kettle, Still, Loom, Pottery Wheel, Drying Rack, Forge, Gem Cutter, Fletching Table, and more |
| **Production** | Fermentation Vessel, Barrel Room, Bottling Station, Cheese Cave, Kiln |
| **Structural** | Stone brick, timber frame, plaster wall, clay tile, carved stone |
| **Decorative** | Carved sculpture blocks (3 styles), tapestry panels, display cases, lanterns |
| **Mechanical** | Wire, logic gates, elevator tracks, minecart rails |
| **Animal Infrastructure** | Kennel, nest box, bird feeder, stable |

Construction isn't just shelter — it's identity. A working winery needs its grape blocks, its crush station, its fermentation room, and its cellar. A functional monastery needs its drying rack, its herb gardens, and its alchemist's hearth. NPCs react to what you build near their settlements.

---

## Cities and Civilization

The world generates **10 city scales** from small villages to metropolitan centers, each populated with NPCs whose professions, inventory, and quest offerings are tied to the local biome and trade history. Cities grow over time if supplied with materials and food.

**40 outpost types** appear in the wilderness between cities, each with a specific trade specialty:

> Wine Estate · Herb Monastery · Trapper Post · Boreal Distillery · Coffee Plantation · Jungle Herbalist · Tea House · Pottery Workshop · Spice Market · Textile Guild · Olive Press · Salt Works · Desert Glassworks · Canyon Forge · Alpine Monastery · Cheese Cave · Fungal Grove · Swamp Alchemist · Fishing Outpost · Coastal Saltworks · Nomad Camp · Craft Brewery · Hill Taproom · Spirit Distillery · Hillside Vineyard · Sculpture Atelier · Border Garrison · Highland Fortress · Desert Legion · Steppe Warcamp · Coastal Citadel · Timber Camp · Reed Weaver · Silk Pavilion · Incense Lodge · Glacier Camp · Bog Apothecary · Pearl Diving Camp · Canoe Trading Post · Mountain Lodge

Each outpost buys specific goods, sells region-exclusive materials, and gives quests tied to local expertise. Supplying a Herb Monastery with rare dried flowers yields different rewards than supplying it with healing potions.

---

## Player Cities

Place a **City Block** anywhere in the world to anchor your own settlement. The City Block is an unbreakable background block that defines the city center. Everything within **±80 blocks horizontally and ±50 blocks vertically** of it is your city region — the area where settlers work, buildings count toward city stats, and resources are managed.

### Getting Started

1. Craft a **City Block** item and place it (background layer) where you want your settlement.
2. Press **E** near it to open the City Block Menu.
3. Name your city, design a coat of arms, and deposit coins into the treasury.

### Settlers

Settlers arrive passively each in-game dawn. Arrival chance per bed in the city region:

> **Base 15%** + **5% per food chest** − **5% per unemployed settler**

Each settler is procedurally generated with a name, trait, and six stats (Strength, Agility, Craft, Endurance, Intelligence, Animal Affinity — each 1–10). Daily wage scales from **5–25 coins** based on total stats.

Settlers need both **food** and **wages** from the city treasury every day. Miss two days of either and they become disgruntled (50% work efficiency). Miss three days and they leave permanently.

### Jobs

Assign settlers jobs via the **Job Panel**. Each job draws on specific stats for throughput:

| Job | Stat | What It Does |
|-----|------|-------------|
| **Farming** | Agility | Harvests mature crops in the city region and replants |
| **Mining** | Strength | Extracts blocks from a configured Mining Post radius |
| **Hauling** | Agility + Strength | Moves items between two specified chests |
| **Taming** | Animal Affinity | Collects milk and eggs from livestock in the region |
| **Logging** | Strength | Fells trees in the city region and deposits lumber |
| **Cooking** | Craft | Converts raw meat and eggs into cooked meals |

Unemployed settlers don't work but still consume food and wages.

### City Block Menu

Open with **E** while within 3 blocks of the City Block.

- **Name** — Click to rename your city (28 character limit).
- **Coat of Arms** — Design button opens the heraldry editor. Choose a division, ordinary, charge, tinctures, metals, and a custom motto.
- **Treasury** — Deposit coins (+10 / +50 / +200 / All). The menu shows your daily wage drain and how many days of funds remain.
- **Settler Roster** — Lists up to 9 settlers with name, trait, job status, and wage. Color coded: green = employed, yellow = idle, red = disgruntled, dim = seeking work.

### Infrastructure Blocks

| Block | Purpose |
|-------|---------|
| **City Block** (1249) | Settlement anchor — defines the city center |
| **Mining Post** (1252) | Marks the work zone for Mining settlers |
| **Banner Block** (1253) | Displays your city coat of arms |

Beds and food chests placed within the city region contribute to settler attraction. More beds means more chances; more food chests boosts the arrival roll. Keep chests stocked and the treasury funded to grow your population steadily.

---

## Research — 24 Columns

Progress is gated behind a research tree organized into 24 disciplines:

> Mining Speed · Zone Access · Farming · Coffee · Birding · Winemaking · Distillation · Entomology · Horsemanship · Tea Cultivation · Herbalism · Textile Arts · Dairy Arts · Hunting · Jewelry Arts · Garden Arts · Masonry Arts · Ceramics · Cynology · Smithing Arts · Brewing · Salting Arts · Fishing · Logistics

Depth gates (shallow / mid / deep / core) gate research nodes — you cannot rush certain unlocks without first doing the work to descend.

---

## Items — Over 2,400

**2,415+ items** in the registry, covering:
- Raw materials from every system (ores, crops, animal products, herbs, shells, feathers, bones)
- Processed goods (wines, spirits, beers, teas, cheeses, textiles, pottery, salts)
- Food across 6 cuisine traditions: Bakery (142 recipes), Wok (56), BBQ Grill (76), Clay Pot (89), Steamer (26), Noodle Pot (26)
- Tools, weapons (10 types), and armor
- Collector display items and encyclopedia volumes

---

## Automation and Machinery

### Mining Machines — 3 Tiers

Point a miner in a direction and it digs indefinitely, collecting drops into its internal inventory. Each tier cuts through harder rock, carries more, and refuels on a different resource.

| Machine | Fuel | Max Hardness | Inventory |
|---------|------|-------------|-----------|
| Coal Miner | Coal | 3 (stone, soft ore) | 30 slots |
| Iron Miner | Iron Chunks | 6 (deep ore, granite) | 50 slots |
| Crystal Miner | Crystal Shards | 9 (all blocks) | 80 slots |

Miners halt automatically when fuel runs out, inventory fills, or they hit an indestructible block. Connect a logic wire — the miner reads it as an enable pin. No power on the wire means the miner stops. Power restored, it resumes. Chain this with a Deposit Trigger to build a full stop-fill-dump-resume cycle without any player input.

### Farm Bots — 3 Tiers

A Farm Bot scans a radius around itself each tick, harvesting mature crops and replanting from its seed inventory automatically. Higher tiers do more.

| Bot | Fuel | Scan Radius | Special |
|-----|------|------------|---------|
| Farm Bot | Coal | 5 blocks | Harvest + replant |
| Iron Farm Bot | Iron Chunks | 9 blocks | + internal water tank, auto-irrigates dry soil |
| Crystal Farm Bot | Crystal Shards | 13 blocks | + water tank + compost slot + auto-tills dirt/grass |

The Crystal Farm Bot converts raw dirt and grass into tilled soil, waters it, applies compost when fertility drops, and cycles seeds it harvests back into its own seed slot. A fully stocked Crystal Farm Bot left running is a closed agricultural loop.

### Backhoe

A player-operated heavy excavator that runs on oil barrels. The arm has 4-block reach and can be aimed in any direction. Dig speed is 7 blocks per second regardless of hardness (up to its cap), making it the fastest excavation tool in the game. Carries 40 slots of ore. Park it at a shaft entrance, fuel it, and carve out rooms or tunnels at a fraction of the hand time.

### Minecarts and Elevators

Lay rail networks by hand. Minecarts follow the track and carry ore between your mine face and surface depots. Elevators handle vertical shafts — set car stops at each level and ride between them.

---

## Logic System

A full programmable wire network. Wires carry a binary signal (powered / unpowered). Any machine adjacent to a powered wire runs; adjacent to an unpowered wire on an otherwise wired circuit, it halts. The logic system evaluates in phases — sources seed power, BFS propagates through wire, gates resolve, then outputs switch state.

### Signal Sources

| Block | Behavior |
|-------|---------|
| **Lever / Switch** | Manual on/off toggle, omnidirectional output |
| **Pressure Plate** | HIGH when player or any entity stands on it |
| **Day Sensor** | HIGH during daylight hours |
| **Night Sensor** | HIGH during nighttime |
| **Water Sensor** | HIGH when water is adjacent to it |
| **Crop Sensor** | HIGH when a mature crop is directly below it |
| **Fish Trap Sensor** | HIGH when the fish trap it watches has accumulated catches |
| **Pulse Generator** | Oscillates on/off at a configurable period (default 2 s) |
| **Observer** | Emits a 2-tick pulse whenever the block it faces changes ID |

### Logic Gates

| Gate | Behavior |
|------|---------|
| **AND Gate** | Output HIGH only when all inputs are HIGH |
| **OR Gate** | Output HIGH when any input is HIGH |
| **NOT Gate** | Output HIGH when its input is LOW (inverts signal) |
| **Repeater** | Delays signal propagation by a configurable time (default 0.5 s); also cleans up long-distance signal |

### Memory and State

| Block | Behavior |
|-------|---------|
| **RS Latch** | Set input latches it ON; Reset input latches it OFF. Holds state with no power input. |
| **T Flip-Flop** | Toggles output on every rising edge of its input — converts a pulse into a sustained toggle |
| **Counter** | Counts rising edges on its input; output goes HIGH when count reaches threshold; a Reset wire zeroes it |
| **Comparator** | Reads the fill level of an adjacent chest (0–8 scale); output goes HIGH when fill ≥ threshold |
| **Sequencer** | Advances through 4 output channels (Right → Down → Left → Up) on each rising input edge |

### Outputs

| Block | Powered State | Unpowered State |
|-------|-------------|----------------|
| **Dam Block** | Open — water flows through | Closed — water blocked |
| **Pump** | Active — moves water | Inactive |
| **Iron Gate** | Open | Closed |
| **Powered Lantern** | Lit | Dark |
| **Alarm Bell** | Ringing | Silent |
| **Deposit Trigger** | Rising edge dumps nearby bot inventories into an adjacent chest | — |

The **Deposit Trigger** is the keystone of any automated mining loop. On a rising edge (not while continuously powered — only on the transition LOW→HIGH), it finds every miner and farm bot within 3 blocks and forces their stored inventory into the nearest adjacent chest. Wire a Pulse Generator into a Deposit Trigger next to a chest and your bots empty themselves on a timer without you ever touching them.

### Example Circuits

**Auto-harvest loop:** Crop Sensor → Deposit Trigger. When the crop below the sensor matures, the sensor goes HIGH, the Deposit Trigger fires, and the farm bot dumps its load into the chest. The sensor drops LOW when the crop is harvested and replanted. Cycle repeats.

**Chest overflow gate:** Comparator (threshold 7) on a chest → NOT Gate → Iron Miner enable pin. When the chest is nearly full, the NOT Gate drops LOW, halting the miner. When items are removed and fill drops below threshold, the NOT Gate goes HIGH and mining resumes.

**Day/night lighting:** Day Sensor → NOT Gate → Powered Lanterns. Lanterns light up at dusk and switch off at dawn automatically.

**4-stage sequencer:** Pulse Generator → Sequencer → 4 separate output channels. Each channel can feed a different machine or gate. Rotate through four actions on a timed cycle.

**Latch memory:** Use an RS Latch when you want something to stay ON after a brief trigger pulse (like a fish trap filling) without needing continuous power from the sensor.

---

## Pipe System

A physical item transport network. Items move through pipes from Hoppers (source) to Output Blocks (sink). The system path-finds automatically using BFS — you place the pipes, connect the endpoints, and items route themselves.

### Pipe Tiers

| Pipe | Item | Speed |
|------|------|-------|
| Wooden Pipe | `pipe` | 1× |
| Iron Pipe | `pipe_iron` | 3× |
| Crystal Pipe | `pipe_crystal` | 8× |

Speed determines how many tiles an item advances per routing tick (every 0.5 s). Mix tiers in a single network — items inherit the speed of whichever tile they're currently on.

### Pipe Devices

| Block | Function |
|-------|---------|
| **Hopper** | Pulls 1 item per tick from the container directly above it into the pipe network |
| **Pipe Output** | Deposits items into the container directly below (or in its facing direction) |
| **Filter** | Items not on its whitelist are blocked and buffered; whitelisted items pass through |
| **Sorter** | Routes specific item IDs to specific directions — split a mixed stream into sorted outputs |

### How Routing Works

When a Hopper pulls an item, the system runs a BFS across all connected pipe tiles to find the nearest reachable Output Block. The item is launched along that path. If a Filter blocks it mid-route, the item buffers at the tile before the filter and waits for re-routing. If an Output Block's destination container is full, the item buffers at the output and retries next tick.

This means the network is self-healing — remove a pipe tile and in-transit items strand at their last valid position, then re-route once the network is repaired.

### Wire Integration

Hoppers and Output Blocks obey the logic wire enable pin. An unpowered wire adjacent to a Hopper stops it from pulling. An unpowered wire adjacent to an Output Block stops it from depositing. This lets you gate entire production pipelines with a single logic signal — pause a pipe output when a downstream chest is full (via Comparator), or stop a hopper when a machine is offline.

### What Pipes Connect

Pipes can pull from and deposit into: **Chests**, **Mining Automations** (miner stored inventory), **Farm Bots** (stored harvest), and **Factories**. A Crystal Miner next to a Hopper with a Crystal Pipe network feeding into sorted chests is a fully hands-off deep mining operation.

---

## Transport Infrastructure

- **Minecarts** — follow hand-laid rail networks, carry ore between mine face and depot
- **Elevators** — vertical shaft transport with configurable stops per level

---

## Getting Started

**Requirements:** Python 3.10+, Pygame

```bash
pip install pygame
python main.py
```

The game launches fullscreen. Press **F11** to toggle windowed mode.

---

## Controls

| Key | Action |
|-----|--------|
| A / D | Move left / right |
| Space | Jump |
| Left click | Mine / interact |
| Right click | Place block |
| 1–8 | Hotbar slot |
| Scroll | Cycle hotbar |
| E | Inventory |
| R | Research tree |
| T | Automations panel |
| Esc | Close / pause |
| F11 | Toggle fullscreen |
