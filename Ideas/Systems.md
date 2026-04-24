New Systems & Side Games — CollectorBlocks
Context
The game already has wine, coffee, farming, fishing, birding, rock/gem/fossil collecting, animal breeding, and 3-tier automation. The goal is to identify new systems that deepen the experience, create cross-system synergies, and follow the proven design patterns (dataclass lifecycle → mini-game → output tier → buff).

Tier 1 — High Fit, High Impact
1. Tea System
Why it fits: Mirrors coffee/wine exactly. Growers in biomes → harvest → process → blend → brew → buff.

Wild harvest: Tea plants spawn in tropical/jungle/alpine biomes (biome-specific cultivar names)
Farming option: Grow tea bushes on farm (slower yield, higher quality)
Processing: Wither → oxidize → dry. The oxidation level is the core choice:
Skip = green tea (bright, vegetal)
Partial = oolong (complex, floral)
Full = black tea (bold, malty)
Dark fermented = pu-erh (earthy, aged)
Herbal blends: Mix harvested tea with existing farm crops (chamomile, mint, ginger, lavender) — reuses farming output as ingredients
Mini-game: Oxidation timing (hold in green zone, similar to roasting). Second mini-game for loose-leaf vs pressed cake forming.
Aging: Pu-erh ages like wine (short/medium/long), gains complexity
Output: Brewed tea items (base/fine/aged) with calm/focus/endurance-style buffs distinct from coffee
Research column: Tea Cultivation → Processing Arts → Blending → Tea Ceremony (5 nodes)
Files to add/modify: tea.py, UI/tea.py, extend items.py, research.py, blocks.py


3. Beekeeping
Why it fits: Passive placement system (like bird feeders/baths) that creates synergies with existing systems — farming yield boost, wildflower bonus, and feeds directly into mead production.

Hive placement: Place bee boxes in world. Bees passively forage nearby flowers + farm crops
Biome honey: Honey type/flavor derived from surrounding wildflower biome
Tropical biome → passion fruit honey
Alpine → wildflower mountain honey
Wetland → clover honey
Synergy effects:
Crops within hive radius get +10–20% yield (pollination)
Wildflowers near hive respawn faster
Harvest: Collect honeycomb → extract honey + beeswax
Mead production: Honey + water → ferment (reuses wine fermentation pattern) → aged mead
Mead flavors inherit honey biome profile
Sparkling mead variant (like sparkling wine)
Beeswax uses: Candles (light source + ambient buff), wood polish (enhances tool durability), wax seals for wine bottles (cosmetic bonus)
Research: Apiary Basics → Honey Harvest → Pollination Arts → Master Apiarist (4 nodes)
Files: bees.py, UI/bees.py, extend blocks.py, items.py, farming integration

Tier 2 — New Dimensions
4. Herbalism & Alchemy
Why it fits: The Alchemical Kiln and Resonance Chamber already exist but appear underused. This system activates them as the heart of a potion-crafting branch that rewards deep collectors.

Ingredients: Dried mushrooms + pressed wildflowers + crop byproducts (roots, seeds, husks)
Drying rack block: Hang herbs to dry over time → dried ingredient items
Recipe discovery: Combine 2–4 ingredients in Alchemical Kiln → discover potions
Unknown combinations produce mystery flasks → player identifies through use
Successful combinations unlock recipe permanently
Resonance Chamber: Higher-tier transmutations — convert rare gem dust + dried herbs → powerful elixirs
Output: Potions with longer/stronger buffs than food (stamina, night vision, magnetism, dowsing for rare blocks)
Potion types: Health, speed, mining power, luck (better collectible rarity), charm (better trade prices)
Research: Herbalism Basics → Tincture Crafting → Alchemy → Resonance Mastery (4 nodes)
5. Insect Collecting
Why it fits: Mirrors birding — passive observation/collection, biome/season-specific, codex + achievements. Low implementation overhead, high flavor.

Tool: Bug net (craft from lumber + string)
Behavior: Insects flutter near flowers + bushes. Player must approach slowly (same spooked mechanic as birding)
Biome variety: 40+ species — butterflies (tropical), beetles (forest), fireflies (wetland/night), dragonflies (water adjacent)
Seasonal: Some species only active in spring/summer; fireflies only appear at night
Collection mechanic: Caught insects go in display cases (craftable furniture item)
Synergy: Insects near crops boost pollination (stacks with beehives)
Codex + achievements: Parallels bird achievement system
Files: insects.py, extend UI/collections.py, items.py
6. Pottery & Ceramics
Why it fits: Adds a crafting branch with both functional and decorative outputs. Clay is a natural underground resource. Functional items (pots that boost food effects) create reasons to invest.

Clay: Mine clay deposits in wetland/river biomes (new block type)
Pottery Wheel block: Shape clay → raw forms (bowls, vases, jugs, pots)
Kiln firing mini-game: Temperature control (similar to roasting) → determines final quality (cracked / intact / fine)
Glazing: Apply crushed gemstone dust for colored glazes → decorative rarity
Functional outputs:
Clay cooking pot → boosts food crafting yield (+1 serving)
Wine amphora → already referenced! (new vessel option with higher complexity gain)
Herb storage jar → extends dried ingredient shelf life
Water jug → portable water source for farming
Decorative: Vases, urns, display pieces for player base
Research: Clay Working → Kiln Mastery → Glaze Arts (3 nodes)
Tier 3 — Flavor & World-Building
7. Cartography System
Map fragments: Found in deep caves, gifted by city NPCs as rare quest rewards
Surveying: Stand at a location with a compass → map that biome section
Rare location markers: Treasure caches, rare ore veins, legendary creature dens
Map display: Parchment-style overlay showing explored regions + points of interest
Reward: Marked locations have boosted rare spawn rates
8. Stargazing
Telescope: Craftable from glass (gem dust) + iron
Night only: Active when world is dark
Constellations: 12 to discover, each tied to a month (seasonal rotation)
Rewards: Unlock cosmetic star chart items + rare meteorite spawn events
Lore tie-in: Meteorite rocks (already exist at deep depth) could have increased spawn rate after stargazing events
9. Textile / Fiber Arts
Inputs: Sheep wool (breeding already exists) + plant fibers (flax crop)
Spinning Wheel: Convert raw fiber → thread
Loom: Weave thread + natural dyes (from wildflower pigments) → cloth
Outputs: Rugs, tapestries (decorative blocks), clothing items with passive stat bonuses
Dye system: Each wildflower type produces a unique color — rewards completionist flower collecting
Cross-System Synergy Map
New System	Synergizes With
Tea	Farming (herbal crops), Coffee (shared brew station upgrades)
Distillery	Wine (pomace byproduct), Farming (grain crops)
Beekeeping	Farming (pollination boost), Wildflowers (honey flavor), Wine (mead)
Herbalism	Mushrooms, Wildflowers, Farming (crop byproducts), Alchemy Kiln
Insects	Birding (same codex pattern), Flowers, Beekeeping (pollination)
Pottery	Wine (amphora vessel), Farming (water jug), Food crafting
Textiles	Animal Breeding (wool), Wildflowers (dye), Crafting
Recommended Starting Point
Tea + Beekeeping as a pair — they share a research column space, are self-contained, and immediately create a synergy loop: bees boost wildflowers → wildflower honey → mead; farm crops + tea harvest → herbal blends. Both follow existing patterns closely so implementation risk is low.

Distillery as the next step — it deepens the wine/fermentation system players already invested in and adds a satisfying late-game prestige system (aged reserve spirits as high-value trade goods).