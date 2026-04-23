import pygame
from constants import SCREEN_W, SCREEN_H
from ._data import (
    _MUSHROOM_ORDER, _MUSHROOM_BIOME, _MUSHROOM_DROP_COLOR,
    _MUSHROOM_SHAPES, _MUSHROOM_NAMES, SPECIAL_DESCS, RARITY_LABEL,
)
from .hud import HUDMixin
from .menus import MenusMixin
from .handlers import HandlersMixin
from .panels import PanelsMixin
from .crafting import CraftingMixin
from .coffee import CoffeeMixin
from .minigames import MinigamesMixin
from .collections import CollectionsMixin


class UI(
    HUDMixin, MenusMixin, HandlersMixin, PanelsMixin,
    CraftingMixin, CoffeeMixin, MinigamesMixin, CollectionsMixin,
):
    def __init__(self, screen):
        self.screen = screen
        pygame.font.init()
        self.font  = pygame.font.SysFont("consolas", 18)
        self.small = pygame.font.SysFont("consolas", 13)
        self.research_open           = False
        self.inventory_open          = False
        self.crafting_open           = False   # C: crafting panel
        self.collection_open         = False   # G: rock collection
        self.refinery_open           = False   # E near equipment block
        self.refinery_block_id       = None
        self._selected_rock_idx      = None
        self._refinery_selected_idx  = None
        self._card_rects    = {}
        self._inv_rects     = {}
        self._recipe_rects  = {}
        self._rock_rects    = {}
        self._refine_rects  = {}
        self._refine_btn    = None
        self._collection_tab       = 0   # 0=collection, 1=encyclopedia, 2=awards
        self._codex_selected_type  = None
        self._tab_rects            = {}
        self._codex_rects          = {}
        self._selected_flower_idx       = None
        self._flower_rects              = {}
        self._flower_codex_rects        = {}
        self._flower_codex_selected_type = None
        self._flower_codex_scroll       = 0
        self._my_flowers_scroll         = 0
        self._max_flower_codex_scroll   = 0
        self._max_my_flowers_scroll     = 0
        self._mushroom_codex_selected_bid = None
        self._mushroom_codex_rects        = {}
        self._mushroom_codex_scroll       = 0
        self._max_mushroom_codex_scroll   = 0
        self._selected_fossil_idx          = None
        self._fossil_rects                 = {}
        self._fossil_codex_selected_type   = None
        self._fossil_codex_rects           = {}
        self._fossil_codex_scroll          = 0
        self._max_fossil_codex_scroll      = 0
        self._my_fossils_scroll            = 0
        self._max_my_fossils_scroll        = 0
        # Gem collection
        self._selected_gem_idx             = None
        self._gem_rects                    = {}
        self._gem_codex_selected_type      = None
        self._gem_codex_rects              = {}
        self._gem_codex_scroll             = 0
        self._max_gem_codex_scroll         = 0
        self._my_gems_scroll               = 0
        self._max_my_gems_scroll           = 0
        # Unified collection view (new 3-tab layout)
        self._collection_filter       = "all"  # all/rocks/flowers/fossils/gems/mushrooms
        self._collection_filter_rects = {}
        self._encyclopedia_cat        = 0      # 0=rocks 1=flowers 2=mushrooms 3=fossils 4=gems
        self._encyclopedia_cat_rects  = {}
        self._unified_scroll          = 0
        self._max_unified_scroll      = 0
        self._unified_rects           = {}    # (cat, key) → rect
        self._unified_selected        = None  # (cat, key) or None
        # Gem cutter mini-game state
        self._gc_phase          = "select"  # select | show_seq | player_turn | reveal | choose_cut
        self._gc_gem_idx        = None
        self._gc_fault_pts      = []
        self._gc_seq_idx        = 0         # which point is currently highlighted in preview
        self._gc_seq_timer      = 0.0
        self._gc_seq_clicks     = []        # player's clicks so far
        self._gc_mistakes       = 0
        self._gc_fault_rects    = []        # list of pygame.Rect for clickable fault points
        self._gc_fault_lit      = -1        # index lit during preview (-1 = none)
        self._gc_reveal_timer   = 0.0
        self._gc_cut_rects      = {}        # cut_name → pygame.Rect
        self._gc_select_rects   = {}        # gem_idx → pygame.Rect
        self._craft_btn     = None
        self._craft_grid    = [[None] * 3 for _ in range(3)]
        self._cell_rects    = {}
        self._hotbar_rects  = []
        self._recipe_scroll     = 0
        self._codex_scroll      = 0
        self._my_rocks_scroll   = 0
        self._max_recipe_scroll = 0
        self._max_codex_scroll  = 0
        self._max_my_rocks_scroll = 0
        self._bakery_scroll         = 0
        self._max_bakery_scroll     = 0
        self._bakery_selected_recipe = 0
        self._bakery_recipe_rects    = {}
        self._wok_selected_recipe       = 0
        self._wok_recipe_rects          = {}
        self._steamer_selected_recipe   = 0
        self._steamer_recipe_rects      = {}
        self._noodle_pot_selected_recipe = 0
        self._noodle_pot_recipe_rects   = {}
        self._bbq_grill_selected_recipe  = 0
        self._bbq_grill_recipe_rects     = {}
        self._clay_pot_selected_recipe   = 0
        self._clay_pot_recipe_rects      = {}
        self._desert_forge_selected_recipe = 0
        self._desert_forge_recipe_rects    = {}
        self._cook_station_scroll        = {}
        self._cook_station_max_scroll    = {}
        self.npc_open   = False
        self.active_npc = None
        self._trade_rects = {}
        self._quest_btn   = None
        self.automation_open   = False
        self.active_automation = None
        self._auto_deposit1_btn    = None
        self._auto_deposit_all_btn = None
        self._auto_take_btn        = None
        self._auto_dir_btns        = {}
        self._auto_pickup_btn      = None
        self.farm_bot_open   = False
        self.active_farm_bot = None
        self._fb_deposit1_btn    = None
        self._fb_deposit_all_btn = None
        self._fb_seeds_btn       = None
        self._fb_get_seeds_btn   = None
        self._fb_take_btn        = None
        self._fb_pickup_btn      = None
        # Backhoe UI
        self.backhoe_open    = False
        self.active_backhoe  = None
        self._bh_deposit1_btn   = None
        self._bh_deposit_all_btn = None
        self._bh_take_btn       = None
        self._bh_ride_btn       = None
        self._bh_pickup_btn     = None
        # Chest UI
        self.chest_open       = False
        self.active_chest_inv = None   # direct reference to world.chest_data[(bx,by)]
        self.active_chest_pos = None   # (bx, by) for title display
        self._chest_rects     = {}     # item_id -> Rect  (chest side)
        self._player_for_chest_rects = {}  # item_id -> Rect  (player side)
        self._chest_scroll    = 0
        self._max_chest_scroll = 0
        self._player_chest_scroll = 0
        self._max_player_chest_scroll = 0
        # Cheat console
        self.cheat_open    = False
        self.cheat_text    = ""
        self.cheat_message = ""
        self._cheat_msg_timer = 0.0
        # Bird codex UI state
        self._bird_codex_scroll        = 0
        self._max_bird_codex_scroll    = 0
        # Fish codex UI state
        self._fish_codex_rects         = {}
        self._fish_codex_scroll        = 0
        self._max_fish_codex_scroll    = 0
        # Coffee codex UI state
        self._coffee_codex_scroll      = 0
        self._max_coffee_codex_scroll  = 0
        self._coffee_codex_selected    = None   # "biome_roast" string or None
        self._coffee_codex_rects       = {}
        # Roaster mini-game state
        self._roast_phase          = "select_bean"  # "select_bean" | "select_processing" | "roasting" | "result"
        self._roast_bean_idx       = None
        self._roast_time           = 0.0
        self._roast_total_time     = 30.0
        self._roast_temp           = 0.0
        self._roast_temp_vel       = 0.0
        self._roast_heat_held      = False
        self._roast_time_in_band   = 0.0
        self._roast_first_crack_hit  = False
        self._roast_second_crack_hit = False
        self._roast_penalties        = 0
        self._roast_event_flash      = None   # (text, color, timer) or None
        self._roast_stop_btn         = None
        self._roast_select_rects     = {}
        self._roast_result_done_btn  = None
        self._roast_proc_rects       = {}   # processing phase button rects
        # Blend station state
        self._blend_slots        = [None, None, None]  # bean indices or None
        self._blend_slot_rects   = []
        self._blend_list_rects   = {}  # bean_idx → Rect
        self._blend_btn          = None
        self._blend_result_bean  = None
        self._blend_phase        = "select"  # "select" | "result"
        self._blend_result_done_btn = None
        # Brew station state
        self._brew_bean_idx      = None
        self._brew_bean_rects    = {}  # bean_idx → Rect
        self._brew_method_rects  = {}  # method_key → Rect
        self._brew_btn           = None
        self._brew_water_quality = "soft"
        self._brew_grind_size    = "medium"
        self._brew_water_rects   = {}
        self._brew_grind_rects   = {}
        # Fossil prep table mini-game state
        self._fprep_phase      = "select"   # "select" | "prep" | "reveal"
        self._fprep_fossil     = None       # Fossil being prepared
        self._fprep_grid       = None       # 2D list of cell dicts
        self._fprep_n          = 0          # grid dimension
        self._fprep_tool       = "chisel"   # "chisel" | "brush"
        self._fprep_damage     = 0          # accumulated damage 0–100
        self._fprep_cell_hits  = None       # 2D list of hit counts
        self._fprep_cleared    = None       # 2D bool grid
        self._fprep_reveal_t   = 0.0        # reveal animation timer 0→1
        self._fprep_select_rects = {}       # fossil_idx → Rect
        self._fprep_grid_rect  = None       # Rect of whole grid area
        self._fprep_cell_size  = 44
        self._fprep_hover_cell = None       # (row, col) or None
        self._fprep_done_btn   = None
        self._fprep_chisel_btn = None
        self._fprep_brush_btn  = None
        # Fishing overlay fonts
        self._fish_bite_font = pygame.font.SysFont("Arial Black", 34, bold=True)
        # Toast notifications
        self._toasts = []
        self._toast_font = pygame.font.SysFont("consolas", 14)
        self._death_font  = pygame.font.SysFont("Arial Black", 72, bold=True)
        self._death_font2 = pygame.font.SysFont("Arial", 26)
        # Pause menu
        self.pause_open = False
        self._pause_btn_rects = {}
        self._pause_font  = pygame.font.SysFont("Arial Black", 56, bold=True)
        self._pause_font2 = pygame.font.SysFont("Arial Black", 30, bold=True)
        self._cheat_font  = pygame.font.SysFont("consolas", 20)
        # Drag-and-drop state for inventory → hotbar
        self._drag_item_id = None
        self._drag_pos     = (0, 0)
        self._inv_scroll     = 0
        self._max_inv_scroll = 0
        # Achievements (populated by main.py after save_mgr.load_achievements())
        self.achievements_data: dict  = {}   # {achievement_id: bool}
        self.global_collection: dict  = {}   # {category: set(item_id_str)}
        self._achievement_scroll     = 0
        self._max_achievement_scroll = 0
        # Animal registry / breeding screen
        self.breeding_open        = False
        self.world_ref            = None
        self._breed_tab           = 0          # 0=all 1=sheep 2=cow 3=chicken
        self._breed_tab_rects     = {}
        self._breed_list_rects    = {}         # uid -> Rect
        self._breed_selected_uid  = None
        self._breed_scroll        = 0
        self._max_breed_scroll    = 0
        # Bird observation mini-game overlay
        self._bird_obs_active    = False
        self._bird_obs_bird      = None
        self._bird_obs_timer     = 0.0   # 0.0 → 2.0 when complete
        self._bird_obs_failed    = False
        self._bird_obs_fail_timer = 0.0
        # Bird collection
        self._bird_journal_rects  = {}
        self._bird_journal_scroll = 0
        self._bird_codex_rects    = {}


    def draw(self, player, research=None, dt=0.0):
        if self._cheat_msg_timer > 0:
            self._cheat_msg_timer -= dt
        if player.dead:
            self._draw_death_screen(player)
            return
        self._draw_health(player)
        self._draw_hunger(player)
        self._draw_depth(player)
        self._draw_pick_level(player)
        self._draw_money(player)
        self._draw_mine_bar(player)
        self._draw_hints(research, player)
        if self.research_open and research:
            self._draw_research(player, research)
        if self.inventory_open:
            self._draw_inventory(player)
        if self.crafting_open:
            self._draw_crafting(player, research)
        if self.collection_open:
            self._draw_collection(player)
        if self.breeding_open:
            self._draw_breeding(player)
        if self.refinery_open and self.refinery_block_id is not None:
            self._draw_refinery(player, dt)
        if self.npc_open and self.active_npc is not None:
            self._draw_npc_panel(player)
        if self.automation_open and self.active_automation is not None:
            self._draw_automation_panel(player)
        if self.farm_bot_open and self.active_farm_bot is not None:
            self._draw_farm_bot_panel(player)
        if self.backhoe_open and self.active_backhoe is not None:
            self._draw_backhoe_panel(player)
        if self.chest_open and self.active_chest_inv is not None:
            self._draw_chest(player)
        if self.cheat_open:
            self._draw_cheat_console()
        if self.pause_open:
            self._draw_pause_menu()
        self._draw_hotbar(player)
        if getattr(player, 'bg_place_mode', False):
            self._draw_bg_mode_indicator()
        self._draw_coffee_buffs(player)
        self._drain_notifications(player)
        self._draw_toasts(dt)
        if self._drag_item_id is not None and self.inventory_open:
            self._draw_drag_item()

