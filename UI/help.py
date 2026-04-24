import pygame
from constants import SCREEN_W, SCREEN_H

_TOPICS = [
    "Distilling",
    "Wine Making",
    "Coffee Making",
    "Farming",
    "Crafting",
    "Mining",
    "Collecting",
    "Research",
]

_CONTENT = {
    "Distilling": [
        ("header",  "Distilling Spirits"),
        ("body",    "Each biome grows a different grain that produces a unique"),
        ("body",    "spirit type. Harvest mature grain plants to collect raw mash,"),
        ("body",    "then process it through three stations."),
        ("gap",),
        ("section", "STEP 1 — Grow & Harvest"),
        ("body",    "Plant grain seeds in a biome. Each biome yields a"),
        ("body",    "different grain and spirit variety:"),
        ("bullet",  "Tropical / Beach          →  Sugarcane  →  Rum"),
        ("bullet",  "Jungle / Savanna          →  Corn       →  Bourbon"),
        ("bullet",  "Wetland / Swamp           →  Botanical  →  Gin"),
        ("bullet",  "Alpine / Rocky Mountain   →  Pomace     →  Brandy"),
        ("bullet",  "Tundra / Boreal           →  Grain      →  Vodka"),
        ("bullet",  "Arid Steppe / Canyon / Rolling Hills  →  Grain  →  Whiskey"),
        ("body",    "Harvest fully-grown plants to receive raw mash items."),
        ("gap",),
        ("section", "STEP 2 — Copper Still  (Distillation)"),
        ("body",    "Place a Copper Still block and press E nearby to open it."),
        ("body",    "Select a raw mash from your inventory to load the still."),
        ("gap",),
        ("body",    "Mini-game: Hold SPACE to heat the still. Watch the"),
        ("body",    "temperature gauge rise. When the needle reaches the"),
        ("body",    "green zone, release SPACE to make the 'hearts cut'."),
        ("body",    "You must make 2 cuts total. Cutting inside the green"),
        ("body",    "zone raises cut quality and proof; cutting outside"),
        ("body",    "lowers them. Timing both cuts well gives the best result."),
        ("gap",),
        ("section", "STEP 3 — Barrel Room  (Aging)"),
        ("body",    "Place a Barrel Room block and press E to open it."),
        ("body",    "Select a distilled spirit, choose a barrel type and"),
        ("body",    "a maturation duration, then confirm to begin aging."),
        ("gap",),
        ("body",    "Barrel types shape the flavor notes:"),
        ("bullet",  "New Oak      — bold tannins, sawdust, fresh wood"),
        ("bullet",  "Charred Oak  — vanilla, caramel, sweet smoke"),
        ("bullet",  "Used Oak     — gentle oak, dried fruit, soft finish"),
        ("gap",),
        ("body",    "Duration options: Short, Medium, or Long."),
        ("body",    "Longer aging improves age quality but takes more time."),
        ("gap",),
        ("section", "STEP 4 — Bottling Station  (Bottle or Blend)"),
        ("body",    "Place a Bottling Station block and press E to open it."),
        ("body",    "Bottle a single aged spirit to add it to your collection,"),
        ("body",    "or blend up to 3 spirits together. A blend averages the"),
        ("body",    "attributes of all components and combines their flavor"),
        ("body",    "notes into a unique spirit of its own."),
        ("gap",),
        ("section", "QUALITY"),
        ("body",    "A spirit's final quality is determined by:"),
        ("bullet",  "Cut quality  — precision of the hearts cut in the Still"),
        ("bullet",  "Proof        — alcohol content (higher cut = higher proof)"),
        ("bullet",  "Age quality  — set by barrel type and duration"),
        ("bullet",  "Smoothness   — base attribute from the grain's biome"),
    ],
    "Wine Making": [
        ("header",  "Wine Making"),
        ("body",    "Each biome grows a grape variety with its own flavor profile."),
        ("body",    "Harvest mature grape vines to collect raw clusters, then"),
        ("body",    "process them through three stations."),
        ("gap",),
        ("section", "BIOME → GRAPE VARIETY"),
        ("bullet",  "Tropical           →  Sauvignon Blanc"),
        ("bullet",  "Jungle             →  Syrah"),
        ("bullet",  "Savanna            →  Tempranillo"),
        ("bullet",  "Wetland            →  Pinot Noir"),
        ("bullet",  "Arid Steppe        →  Grenache"),
        ("bullet",  "Canyon             →  Cabernet Sauvignon"),
        ("bullet",  "Beach              →  Riesling"),
        ("bullet",  "Tundra             →  Pinot Gris"),
        ("bullet",  "Swamp              →  Malbec"),
        ("bullet",  "Alpine Mountain    →  Chardonnay"),
        ("bullet",  "Rocky Mountain     →  Nebbiolo"),
        ("bullet",  "Rolling Hills      →  Merlot"),
        ("gap",),
        ("section", "STEP 1 — Grape Press  (Crush)"),
        ("body",    "Place a Grape Press block and press E to open it."),
        ("body",    "Select raw grapes, then choose a crush style:"),
        ("bullet",  "Whole Cluster    — stems in; adds tannin and earthiness"),
        ("bullet",  "Destemmed        — classic, balanced fruit"),
        ("bullet",  "Rosé Bleed       — brief skin contact; light, bright rosé"),
        ("bullet",  "Skin Fermented   — long skin contact; amber, textured"),
        ("gap",),
        ("body",    "Mini-game: Hold SPACE (or click PRESS) to build pressure."),
        ("body",    "Keep the gauge in the green zone as long as possible."),
        ("body",    "Two milestones fire automatically — Free-Run (~10 s) and"),
        ("body",    "Press-Wine (~22 s). Press ENTER or click STOP when done."),
        ("body",    "Over-pressing penalises quality; under-pressing wastes yield."),
        ("gap",),
        ("section", "STEP 2 — Fermentation Tank"),
        ("body",    "Place a Fermentation Tank block and press E to open it."),
        ("body",    "Select crushed grapes, then choose a yeast strain:"),
        ("bullet",  "Wild       — high complexity, lower alcohol, unpredictable"),
        ("bullet",  "Champagne  — clean, high-alcohol, biased to sparkling"),
        ("bullet",  "Bordeaux   — structured; builds body and tannin"),
        ("bullet",  "Burgundy   — elegant; aromatic lift, moderate body"),
        ("gap",),
        ("body",    "Mini-game: Hold SPACE to raise temperature, press N to add"),
        ("body",    "nutrients. Keep both in their target bands. Stop fermentation"),
        ("body",    "early for sweeter, lower-alcohol wine; let it run for drier,"),
        ("body",    "higher-alcohol results."),
        ("gap",),
        ("section", "STEP 3 — Wine Cellar  (Age, Blend & Bottle)"),
        ("body",    "Place a Wine Cellar block and press E to open it."),
        ("body",    "Three tabs are available:"),
        ("gap",),
        ("body",    "Age tab — select a fermented wine, choose a vessel:"),
        ("bullet",  "Oak Barrel   — adds body, spice, complexity"),
        ("bullet",  "Steel Tank   — preserves brightness and fruit"),
        ("bullet",  "Clay Amphora — earthy, mineral, gentle oxidation"),
        ("body",    "Then choose duration: Short (6 mo), Medium (2 yr), Long (5 yr)."),
        ("body",    "Longer aging adds complexity and quality."),
        ("gap",),
        ("body",    "Blend tab — combine up to 3 aged wines into one blend."),
        ("gap",),
        ("body",    "Bottle tab — choose serving temperature and glass style."),
        ("body",    "Serving temperature affects buff duration and quality:"),
        ("bullet",  "Chilled    — longer buff duration, small quality bonus"),
        ("bullet",  "Cellar     — balanced duration, best quality bonus"),
        ("bullet",  "Room Temp  — shorter duration, minimal bonus"),
        ("gap",),
        ("section", "WINE STYLES & BUFFS"),
        ("bullet",  "Red Wine     — warmth buff  (cold damage -50%)"),
        ("bullet",  "White Wine   — serenity buff  (hunger drain -60%)"),
        ("bullet",  "Rosé         — charm buff  (collect radius +75%)"),
        ("bullet",  "Sparkling    — vivacity buff  (jump +1, no fall damage)"),
        ("bullet",  "Dessert Wine — contemplation buff  (XP +25%)"),
    ],
    "Coffee Making": [
        ("header",  "Coffee Making"),
        ("body",    "Each biome grows a coffee variety with distinct flavor attributes."),
        ("body",    "Harvest mature coffee cherry plants to collect raw beans, then"),
        ("body",    "process them through the Roaster and Blend Station."),
        ("gap",),
        ("section", "BIOME → VARIETY"),
        ("bullet",  "Tropical / Beach / Alpine / Tundra / Rolling Hills  →  Arabica"),
        ("bullet",  "Savanna / Wetland / Swamp / Boreal                  →  Robusta"),
        ("bullet",  "Arid Steppe / Canyon / Rocky Mountain               →  Liberica"),
        ("gap",),
        ("section", "STEP 1 — Choose a Processing Method"),
        ("body",    "When opening raw beans in the Roaster, select a processing"),
        ("body",    "method before roasting. This shapes the base flavor:"),
        ("bullet",  "Washed   — clean, bright, acidity-forward; tea-like clarity"),
        ("bullet",  "Natural  — fruity, fermented, heavy sweetness"),
        ("bullet",  "Honey    — sweet and complex; apricot and nectarine notes"),
        ("gap",),
        ("section", "STEP 2 — Roaster  (Roasting Mini-game)"),
        ("body",    "Place a Roaster block and press E to open it."),
        ("body",    "Select a raw bean, choose processing, then begin the roast."),
        ("gap",),
        ("body",    "Mini-game: Hold SPACE to apply heat. Watch the temperature"),
        ("body",    "gauge. Roast level is determined by how long the bean stays"),
        ("body",    "in each temperature zone:"),
        ("bullet",  "Light   — bright, delicate, tea-like (stop early)"),
        ("bullet",  "Medium  — balanced, caramel, full flavour (hit first crack)"),
        ("bullet",  "Dark    — bold, smoky, low acidity (push past second crack)"),
        ("bullet",  "Charred — burnt and bitter (over-roasted)"),
        ("gap",),
        ("body",    "Hit First Crack for best quality; hold for Second Crack for"),
        ("body",    "dark roast. Release heat and stop to lock in your roast level."),
        ("gap",),
        ("section", "STEP 3 — Blend Station  (Optional)"),
        ("body",    "Place a Blend Station block and press E to open it."),
        ("body",    "Combine up to 3 roasted beans into a single blend. The blend"),
        ("body",    "averages the flavor attributes and combines flavor notes."),
        ("gap",),
        ("section", "STEP 4 — Brewing  (Brew Station)"),
        ("body",    "Place a Brew Station block and press E to open it."),
        ("body",    "Choose a brew method, grind size, and water quality:"),
        ("gap",),
        ("body",    "Brew methods:"),
        ("bullet",  "Drip         — focus buff  (amplifies sweetness & brightness)"),
        ("bullet",  "Espresso     — rush buff  (amplifies body & acidity)"),
        ("bullet",  "Pour Over    — clarity buff  (amplifies acidity & brightness)"),
        ("bullet",  "Cold Brew    — endurance buff  (amplifies sweetness & body)"),
        ("bullet",  "French Press — strength buff  (amplifies body & earthiness)"),
        ("gap",),
        ("body",    "Grind size affects extraction:"),
        ("bullet",  "Coarse  — longer, softer, smoother"),
        ("bullet",  "Medium  — balanced"),
        ("bullet",  "Fine    — fast, concentrated, bold"),
        ("gap",),
        ("body",    "Water quality:"),
        ("bullet",  "Soft     — highlights acidity and brightness"),
        ("bullet",  "Hard     — boosts body, mutes brightness"),
        ("bullet",  "Filtered — neutral, small quality bonus across the board"),
    ],
    "Farming": [
        ("header",  "Farming"),
        ("body",    "Grow crops by planting seeds on prepared soil."),
        ("gap",),
        ("section", "PLANTING"),
        ("body",    "Equip seeds in your hotbar and right-click on tilled"),
        ("body",    "soil to plant them. Crops grow automatically over time"),
        ("body",    "and must be harvested once fully grown."),
        ("gap",),
        ("section", "SOIL"),
        ("body",    "Use a hoe on dirt blocks to create tilled soil. Crops"),
        ("body",    "planted on fertile soil grow faster."),
        ("gap",),
        ("section", "FARM BOT"),
        ("body",    "Farm Bots automate planting and harvesting. Place one"),
        ("body",    "nearby and press E to configure seeds and fuel."),
    ],
    "Crafting": [
        ("header",  "Crafting"),
        ("body",    "Open the crafting panel with C. Place items into the"),
        ("body",    "3x3 grid and a matching recipe will appear on the right."),
        ("gap",),
        ("section", "EQUIPMENT"),
        ("body",    "Specialized blocks unlock additional recipes:"),
        ("bullet",  "Bakery            — baked goods and breads"),
        ("bullet",  "Wok               — stir-fry dishes"),
        ("bullet",  "Desert Forge      — metal tools and equipment"),
        ("bullet",  "Artisan Bench     — advanced crafted items"),
        ("bullet",  "Copper Still      — distilled spirits"),
        ("bullet",  "Barrel Room       — aged spirits"),
        ("bullet",  "Bottling Station  — bottled & blended spirits"),
        ("gap",),
        ("section", "RESEARCH LOCKS"),
        ("body",    "Some recipes are locked until researched. Open the"),
        ("body",    "Research tree with R to unlock new crafting options."),
    ],
    "Mining": [
        ("header",  "Mining"),
        ("body",    "Mine blocks with a pickaxe. Deeper layers contain"),
        ("body",    "rarer rocks, gems, and fossils."),
        ("gap",),
        ("section", "DEPTH"),
        ("body",    "The depth indicator in the HUD shows your current"),
        ("body",    "underground level. The deeper you go, the rarer the"),
        ("body",    "materials you will find."),
        ("gap",),
        ("section", "PICKAXES"),
        ("body",    "Better pickaxes mine faster and can break harder blocks."),
        ("body",    "Upgrade your tools at the Desert Forge."),
        ("gap",),
        ("section", "BACKHOE"),
        ("body",    "The Backhoe machine excavates large areas automatically."),
        ("body",    "Fuel it with oil barrels. Press E near it to mount or"),
        ("body",    "manage fuel. Use arrow keys to move the arm while riding."),
    ],
    "Collecting": [
        ("header",  "Collecting"),
        ("body",    "Open your collection panel with G. Items you pick up"),
        ("body",    "are automatically catalogued by category."),
        ("gap",),
        ("section", "CATEGORIES"),
        ("body",    "The collection tracks: rocks, wildflowers, fossils,"),
        ("body",    "gems, mushrooms, coffee, wine, and spirits."),
        ("body",    "Use the filter buttons at the top to sort by type."),
        ("gap",),
        ("section", "ENCYCLOPEDIA"),
        ("body",    "The Encyclopedia tab lists all known species and types"),
        ("body",    "in the world, including ones you haven't found yet."),
        ("body",    "Click an entry to see details and rarity information."),
        ("gap",),
        ("section", "AWARDS"),
        ("body",    "Complete collection milestones to earn awards and"),
        ("body",    "unlock special bonuses. Check the Awards tab in the"),
        ("body",    "collection panel to see your progress."),
    ],
    "Research": [
        ("header",  "Research"),
        ("body",    "Open the research tree with R. Spend research points"),
        ("body",    "to unlock nodes and gain new abilities and recipes."),
        ("gap",),
        ("section", "GAINING POINTS"),
        ("body",    "Research points are earned by collecting items, mining"),
        ("body",    "rare materials, and completing quests from NPCs."),
        ("gap",),
        ("section", "UNLOCKS"),
        ("body",    "Research unlocks crafting recipes, equipment upgrades,"),
        ("body",    "and world features. Plan your tree carefully — some"),
        ("body",    "advanced nodes require earlier nodes to be unlocked first."),
        ("gap",),
        ("section", "COLUMNS"),
        ("body",    "The tree is organized in columns by theme:"),
        ("bullet",  "Column 1  — Gathering & Tools"),
        ("bullet",  "Column 2  — Food & Cooking"),
        ("bullet",  "Column 3  — Mining & Geology"),
        ("bullet",  "Column 4  — Coffee & Wine"),
        ("bullet",  "Column 5  — Automation"),
        ("bullet",  "Column 6  — Distilling"),
    ],
}


class HelpMixin:

    def _draw_help(self):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        self.screen.blit(overlay, (0, 0))

        panel = pygame.Rect(20, 20, SCREEN_W - 40, SCREEN_H - 40)
        pygame.draw.rect(self.screen, (18, 18, 28), panel)
        pygame.draw.rect(self.screen, (80, 80, 130), panel, 2)

        title_surf = self.font.render("HELP", True, (200, 200, 255))
        self.screen.blit(title_surf, (panel.centerx - title_surf.get_width() // 2, panel.y + 8))
        hint = self.small.render("ESC to close", True, (100, 100, 150))
        self.screen.blit(hint, (panel.right - hint.get_width() - 10, panel.y + 10))

        CONTENT_Y = panel.y + 34
        LEFT_W = 190

        # Left topic panel
        left_rect = pygame.Rect(panel.x + 8, CONTENT_Y, LEFT_W, panel.bottom - CONTENT_Y - 8)
        pygame.draw.rect(self.screen, (12, 12, 22), left_rect)
        pygame.draw.rect(self.screen, (50, 50, 80), left_rect, 1)

        self._help_topic_rects.clear()
        ty = left_rect.y + 10
        for topic in _TOPICS:
            btn = pygame.Rect(left_rect.x + 4, ty, left_rect.width - 8, 28)
            self._help_topic_rects[topic] = btn
            selected = (self._help_topic == topic)
            if selected:
                pygame.draw.rect(self.screen, (40, 40, 80), btn)
                pygame.draw.rect(self.screen, (100, 100, 190), btn, 1)
            label_col = (220, 220, 255) if selected else (150, 150, 190)
            label = self.small.render(topic, True, label_col)
            self.screen.blit(label, (btn.x + 10, btn.y + 7))
            ty += 34

        # Right content panel
        right_x = panel.x + LEFT_W + 16
        right_w = panel.right - right_x - 8
        right_rect = pygame.Rect(right_x, CONTENT_Y, right_w, panel.bottom - CONTENT_Y - 8)
        pygame.draw.rect(self.screen, (12, 12, 22), right_rect)
        pygame.draw.rect(self.screen, (50, 50, 80), right_rect, 1)

        content = _CONTENT.get(self._help_topic, [])
        LINE_H = 17

        # Measure total content height
        total_h = 0
        for entry in content:
            if entry[0] == "header":
                total_h += 28
            elif entry[0] == "section":
                total_h += 24
            elif entry[0] == "gap":
                total_h += 10
            else:
                total_h += LINE_H

        visible_h = right_rect.height - 16
        self._help_max_scroll = max(0, total_h - visible_h)
        self._help_scroll = max(0, min(self._help_max_scroll, self._help_scroll))

        SB_W = 10
        content_w = right_w - SB_W - 4 if self._help_max_scroll > 0 else right_w - 4

        clip = pygame.Rect(right_rect.x + 1, right_rect.y + 1, right_rect.width - 2, right_rect.height - 2)
        old_clip = self.screen.get_clip()
        self.screen.set_clip(clip)

        cx = right_rect.x + 12
        y = right_rect.y + 8 - self._help_scroll

        for entry in content:
            kind = entry[0]
            if kind == "header":
                surf = self.font.render(entry[1], True, (200, 200, 255))
                self.screen.blit(surf, (cx, y))
                y += 28
            elif kind == "section":
                surf = self.small.render(entry[1], True, (140, 200, 140))
                self.screen.blit(surf, (cx, y))
                pygame.draw.line(self.screen, (70, 110, 70),
                                 (cx, y + 15), (right_rect.x + content_w, y + 15), 1)
                y += 24
            elif kind == "bullet":
                surf = self.small.render("  •  " + entry[1], True, (185, 185, 210))
                self.screen.blit(surf, (cx + 8, y))
                y += LINE_H
            elif kind == "body":
                text = entry[1] if len(entry) > 1 else ""
                if text:
                    surf = self.small.render(text, True, (185, 185, 210))
                    self.screen.blit(surf, (cx, y))
                y += LINE_H
            elif kind == "gap":
                y += 10

        self.screen.set_clip(old_clip)

        # Scrollbar
        if self._help_max_scroll > 0:
            sb_x = right_rect.right - SB_W - 2
            sb_track_h = right_rect.height - 4
            thumb_h = max(20, int(sb_track_h * visible_h / max(total_h, 1)))
            thumb_y = right_rect.y + 2 + int(
                (sb_track_h - thumb_h) * self._help_scroll / self._help_max_scroll
            )
            pygame.draw.rect(self.screen, (30, 30, 50),
                             (sb_x, right_rect.y + 2, SB_W, sb_track_h))
            pygame.draw.rect(self.screen, (90, 90, 140),
                             (sb_x, thumb_y, SB_W, thumb_h))

    def handle_help_click(self, pos):
        for topic, rect in self._help_topic_rects.items():
            if rect.collidepoint(pos):
                self._help_topic = topic
                self._help_scroll = 0
                return
