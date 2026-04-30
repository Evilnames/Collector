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

When the hand work is done, machines take over:
- **FarmBot** — automated crop planting and harvesting, configurable per plot
- **Backhoe** — excavates tunnels and deposits ore to a chest
- **Minecarts** — ore transport across rail networks you lay by hand
- **Elevators** — vertical travel through deep mine shafts
- **Logic Gates + Wire** — programmable automation circuits for device control
- **Automations** require oil. Oil is finite. Plan accordingly.

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
