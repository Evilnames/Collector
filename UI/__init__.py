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
from .wine import WineMixin
from .spirits import SpiritsMixin
from .beer import BeerMixin
from .minigames import MinigamesMixin
from .collections import CollectionsMixin
from .help import HelpMixin
from .horses_ui import HorseMixin
from .tea import TeaMixin
from .herbalism import HerbalismMixin
from .textiles import TextileMixin
from .cheese import CheeseMixin
from .jewelry import JewelryMixin
from .sculpture import SculptureMixin
from .tapestry import TapestryMixin
from .pottery import PotteryMixin
from .salt import SaltMixin
from .town_menu import TownMenuMixin
from .outpost_menu import OutpostMenuMixin
from .landmark_menu import LandmarkMenuMixin
from .city_block_menu import CityBlockMenuMixin
from .coat_of_arms import CoatOfArmsDesignerMixin
from .hire_panel import HirePanelMixin
from .job_panel import JobPanelMixin
from .reputation_screen import ReputationScreenMixin
from .dogs_ui import DogsMixin
from .weapons import SmithingMixin
from .gambling import GamblingMixin
from .racing import RacingMixin
from .arena import ArenaUIMixin
from .tea_house import TeaHouseMixin
from .dynasty_tree import DynastyTreeMixin


class UI(
    HUDMixin, MenusMixin, HandlersMixin, PanelsMixin,
    CraftingMixin, CoffeeMixin, WineMixin, TeaMixin, HerbalismMixin, SpiritsMixin, BeerMixin, MinigamesMixin, CollectionsMixin,
    HelpMixin, HorseMixin, DogsMixin, TextileMixin, CheeseMixin, JewelryMixin, SculptureMixin, TapestryMixin, PotteryMixin, SaltMixin,
    TownMenuMixin, OutpostMenuMixin, LandmarkMenuMixin, CityBlockMenuMixin, CoatOfArmsDesignerMixin, HirePanelMixin, JobPanelMixin, ReputationScreenMixin, SmithingMixin, GamblingMixin, RacingMixin, ArenaUIMixin, TeaHouseMixin,
    DynastyTreeMixin,
):
    def __init__(self, screen):
        self.screen = screen
        pygame.font.init()
        self.font  = pygame.font.SysFont("consolas", 18)
        self.small = pygame.font.SysFont("consolas", 13)
        self.research_open               = False
        self._research_selected_col      = 0
        self._research_cat_rects         = {}
        self._research_cat_scroll        = 0
        self._max_research_cat_scroll    = 0
        self._research_right_scroll      = 0
        self._max_research_right_scroll  = 0
        self.inventory_open          = False
        self.crafting_open           = False   # C: crafting panel
        self.collection_open         = False   # G: rock collection
        self.refinery_open           = False   # E near equipment block
        self.refinery_block_id       = None
        self.tea_house_open          = False   # E near TEA_HOUSE_BLOCK
        self.active_compost_bin_pos  = None   # (bx, by) when compost bin is open
        self._compost_deposit_btn    = None
        self._compost_collect_btn    = None
        self.active_coop_pos         = None   # (bx, by) when chicken coop is open
        self._coop_collect_btn       = None
        self.npc_inspect_open        = False   # I: NPC inspect overlay
        self.trade_block_open        = False
        self.active_trade_pos        = None   # (bx, by) of open trade block
        self._trade_goods_rects      = {}     # item_id -> Rect for stored goods grid
        self._trade_player_rects     = {}     # item_id -> Rect for player inventory section
        self._trade_horse_btn        = None
        self._trade_cart_btn         = None
        self._trade_city_btn         = None
        self._trade_thresh_minus     = None
        self._trade_thresh_plus      = None
        self._trade_dispatch_btn     = None
        self._trade_horse_idx        = 0      # selected index in tamed horse list
        self._trade_city_idx         = 0      # selected index in TOWNS list
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
        # Seashell collection
        self._shell_codex_selected         = None
        self._shell_codex_rects            = {}
        self._shell_codex_scroll           = 0
        self._max_shell_codex_scroll       = 0
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
        # Left-sidebar scroll (filter list / encyclopedia category list)
        self._collection_sidebar_scroll       = 0
        self._max_collection_sidebar_scroll   = 0
        self._encyclopedia_sidebar_scroll     = 0
        self._max_encyclopedia_sidebar_scroll = 0
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
        self._artisan_selected_recipe      = 0
        self._artisan_recipe_rects         = {}
        self._artisan_tab                  = 0
        self._artisan_search               = ""
        self._artisan_search_active        = False
        self._artisan_tab_rects            = []
        self._artisan_search_rect          = None
        self._artisan_view_all             = False
        self._artisan_view_all_btn         = None
        self._artisan_grid_rects           = {}
        self._artisan_grid_scroll          = 0
        self._bait_station_selected_recipe  = 0
        self._bait_station_recipe_rects     = {}
        self._fletching_selected_recipe     = 0
        self._fletching_recipe_rects        = {}
        self._smelter_selected_recipe       = 0
        self._smelter_recipe_rects          = {}
        self._glass_kiln_selected_recipe    = 0
        self._glass_kiln_recipe_rects       = {}
        self._garden_workshop_selected_recipe = 0
        self._garden_workshop_recipe_rects    = {}
        self._gw_view_all                     = False
        self._gw_view_all_btn                 = None
        self._gw_grid_rects                   = {}
        self._gw_grid_scroll                  = 0
        self._juicer_selected_recipe          = 0
        self._juicer_recipe_rects             = {}
        self._automation_selected_recipe      = 0
        self._automation_recipe_rects         = {}
        self._tanning_rack_selected_recipe    = 0
        self._tanning_rack_recipe_rects       = {}
        self._assembler_selected_recipe       = 0
        self._assembler_recipe_rects          = {}
        self._cook_station_scroll        = {}
        self._cook_station_max_scroll    = {}
        self.npc_open   = False
        self.active_npc = None
        self._trade_rects = {}
        self._quest_btn   = None
        # Town menu
        self.town_menu_open      = False
        self.town_chronicle_open = False
        self.active_town         = None
        self._town_supply_btns   = {}
        self._town_history_btn   = None
        # Outpost menu (diplomatic-only — kingdom & coat of arms)
        self.outpost_menu_open = False
        self.active_outpost    = None
        # Landmark menu (dedicated landmark info + activation screen)
        self.landmark_menu_open     = False
        self.active_landmark_region = None
        self.active_landmark_spec   = None
        # City Block menu (player-run cities)
        self.city_block_menu_open = False
        self.active_city_block    = None
        self._city_name_editing   = False
        self._city_name_draft     = ""
        self._city_name_rect      = None
        self._city_design_btn     = None
        # Coat of Arms designer
        self.coa_designer_open    = False
        self._coa_city            = None
        self._coa_division        = "plain"
        self._coa_ordinary        = "none"
        self._coa_charge          = "none"
        self._coa_primary         = (60, 100, 180)
        self._coa_secondary       = (200, 168, 72)
        self._coa_metal           = (200, 168, 72)
        self._coa_motto           = "Stand Firm"
        self._coa_charge_scroll   = 0
        self._coa_rects           = {}
        # Hire panel (settler NPCs)
        self.hire_panel_open      = False
        self.active_hire_npc      = None
        self.active_hire_city     = None
        self.active_hire_record   = None
        self._hire_accept_btn     = None
        self._hire_decline_btn    = None
        self._hire_assign_job_btn = None
        # Job assignment panel
        self.job_panel_open    = False
        self.active_job_record = None
        self.active_job_city   = None
        self._jp_job_type      = None
        self._jp_radius        = 3
        self._jp_target        = "all"
        self._jp_depth         = 20
        self._jp_src_bx        = ""
        self._jp_src_by        = ""
        self._jp_dst_bx        = ""
        self._jp_dst_by        = ""
        self._jp_active_field  = None
        self._jp_job_btns      = {}
        self._jp_radius_btns   = {}
        self._jp_target_btns   = {}
        self._jp_haul_fields   = {}
        self._jp_confirm       = None
        self._jp_cancel        = None
        # Reputation / kingdoms screen
        self.reputation_screen_open = False
        self._rep_scroll     = 0
        self._rep_max_scroll = 0
        self._rep_view          = "list"
        self._map_selected_rid  = None
        self._map_scroll        = 0
        self._map_node_rects    = {}
        self._rep_tab_rects     = {}
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
        # Garden UI
        self.garden_open             = False
        self.active_garden_flowers   = None  # direct reference to world.garden_data[(bx,by)]
        self.active_garden_pos       = None  # (bx, by)
        self._garden_flower_rects    = {}    # uid -> Rect (flowers placed on canvas)
        self._garden_canvas_rect     = None  # Rect of the open canvas area
        self._garden_col_rects       = {}    # uid -> Rect (collection panel)
        self._garden_col_scroll      = 0
        self._max_garden_col_scroll  = 0
        self._garden_drag_flower     = None  # Wildflower currently being dragged
        self._garden_drag_source     = None  # 'canvas' | 'collection'
        self._garden_drag_origin_pos = None  # (cx, cy) when dragged from canvas
        self._garden_drag_pos        = (0, 0)
        self._garden_view_all        = False
        self._garden_view_all_btn    = None
        self._garden_view_all_rects  = {}
        self._garden_view_all_scroll = 0
        # Wildflower display UI
        self.wildflower_display_open = False
        self.active_display_pos      = None  # (bx, by)
        self._display_player_rects   = {}    # uid -> Rect
        # Cheat console
        self.cheat_open    = False
        self.cheat_text    = ""
        self.cheat_message = ""
        self._cheat_msg_timer = 0.0
        # Help screen
        self.help_open          = False
        self._help_topic        = "Distilling"
        self._help_scroll         = 0
        self._help_max_scroll     = 0
        self._help_topic_rects    = {}
        self._help_topic_scroll   = 0
        self._help_topic_max_scroll = 0
        self._help_left_rect      = None
        # Guard sketches codex UI state
        self._guard_codex_scroll      = 0
        self._max_guard_codex_scroll  = 0
        self._guard_codex_rects       = {}
        # Bird codex UI state
        self._bird_codex_scroll        = 0
        self._max_bird_codex_scroll    = 0
        # Insect codex UI state
        self._insect_codex_scroll      = 0
        self._max_insect_codex_scroll  = 0
        self._insect_codex_rects       = {}
        # Food codex UI state
        self._food_codex_scroll        = 0
        self._max_food_codex_scroll    = 0
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
        self._roast_recording        = []   # [(time, temp), ...] curve recorded during roast
        self._roast_active_profile   = None # profile dict currently being followed
        self._roast_profile_match_time = 0.0
        self._roast_profile_rects    = {}
        self._roast_save_profile_btn = None
        self._roast_profile_name_entry = None  # None or str while typing name
        self._roast_profile_confirm_btn = None
        self._anaerobic_bean_idx     = None
        self._anaerobic_start_time   = None
        self._anaerobic_select_rects = {}
        self._anaerobic_action_btn   = None
        self._brew_herb_key          = None
        self._brew_herb_rects        = {}
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
        # ----- Wine codex UI state -----
        self._wine_codex_scroll      = 0
        self._max_wine_codex_scroll  = 0
        self._wine_codex_selected    = None   # "biome_style" or None
        self._wine_codex_rects       = {}
        # ----- Grape press mini-game state -----
        self._press_phase            = "select_grape"  # select_grape | select_style | pressing | result
        self._press_grape_idx        = None
        self._press_time             = 0.0
        self._press_total_time       = 30.0
        self._press_pressure         = 0.0
        self._press_held             = False
        self._press_time_green       = 0.0
        self._press_time_yellow      = 0.0
        self._press_over_penalty     = 0
        self._press_freerun_hit      = False
        self._press_wine_hit         = False
        self._press_event_flash      = None
        self._press_select_rects     = {}
        self._press_style_rects      = {}
        self._press_stop_btn         = None
        self._press_btn              = None
        self._press_result_done_btn  = None
        # ----- Fermentation mini-game state -----
        self._ferm_phase             = "select_must"  # select_must | select_yeast | fermenting | result
        self._ferm_must_idx          = None
        self._ferm_total_time        = 60.0
        self._ferm_time              = 0.0
        self._ferm_temp              = 0.45
        self._ferm_temp_vel          = 0.0
        self._ferm_temp_held         = False
        self._ferm_temp_band_time    = 0.0
        self._ferm_nutrient          = 0.5
        self._ferm_nut_held          = False
        self._ferm_nutrient_band_time = 0.0
        self._ferm_penalties         = 0
        self._ferm_primary_hit       = False
        self._ferm_malolactic_hit    = False
        self._ferm_finish_hit        = False
        self._ferm_event_flash       = None
        self._ferm_punch_hits        = 0
        self._ferm_punch_total       = 0
        self._ferm_next_punch_time   = 8.0
        self._ferm_punch_active_until = 0.0
        self._ferm_select_rects      = {}
        self._ferm_yeast_rects       = {}
        self._ferm_stop_btn          = None
        self._ferm_temp_btn          = None
        self._ferm_nut_btn           = None
        self._ferm_punch_btn         = None
        self._ferm_result_done_btn   = None
        # ----- Wine Cellar state (tabs: blend/age/bottle) -----
        self._cellar_tab             = "blend"
        self._cellar_tab_rects       = {}
        # Blend wine
        self._blend_wine_slots       = [None, None, None]
        self._blend_wine_slot_rects  = []
        self._blend_wine_list_rects  = {}
        self._blend_wine_btn         = None
        self._blend_wine_phase       = "select"
        self._blend_wine_result      = None
        self._blend_wine_done_btn    = None
        # Age wine
        self._age_wine_idx           = None
        self._age_wine_list_rects    = {}
        self._age_vessel             = "oak"
        self._age_duration           = "medium"
        self._age_vessel_rects       = {}
        self._age_duration_rects     = {}
        self._age_btn                = None
        # Wine aging mini-game
        self._age_phase              = "select"  # select | aging | result
        self._age_progress           = 0.0
        self._age_care_active        = False
        self._age_care_window        = 0.0
        self._age_care_prompt_timer  = 12.0
        self._age_care_bonus         = 0.0
        self._age_game_done          = False
        # Bottle wine
        self._bottle_wine_idx        = None
        self._bottle_wine_rects      = {}
        self._bottle_method          = None
        self._bottle_method_rects    = {}
        self._bottle_temp            = "cellar"
        self._bottle_temp_rects      = {}
        self._bottle_btn             = None
        # Wine bottling result
        self._bottle_wine_result_id  = None
        self._bottle_wine_result_g   = None
        # ----- Copper Still mini-game state -----
        self._still_phase            = "select_spirit"  # select_spirit | distilling | result
        self._still_spirit_idx       = None
        self._still_time             = 0.0
        self._still_temp             = 0.0
        self._still_temp_vel         = 0.0
        self._still_heat_held        = False
        self._still_heads_time       = 0.0
        self._still_hearts_time      = 0.0
        self._still_tails_time       = 0.0
        self._still_cut1_done        = False
        self._still_cut2_done        = False
        self._still_foreshots_hit    = False
        self._still_hearts_hit       = False
        self._still_feints_hit       = False
        self._still_event_flash      = None
        self._still_penalties        = 0
        self._still_cut1_btn         = None
        self._still_cut2_btn         = None
        self._still_finish_btn       = None
        self._still_select_rects     = {}
        self._still_result_spirit    = None
        self._still_result_done_btn  = None
        # ----- Barrel Room state -----
        self._barrel_spirit_idx      = None
        self._barrel_type_sel        = "charred_oak"
        self._barrel_duration_sel    = "medium"
        self._barrel_select_rects    = {}
        self._barrel_type_rects      = {}
        self._barrel_duration_rects  = {}
        self._barrel_age_btn         = None
        # Barrel Room aging mini-game
        self._barrel_phase           = "select"  # select | aging | result
        self._barrel_age_progress    = 0.0
        self._barrel_age_care_active = False
        self._barrel_age_care_window = 0.0
        self._barrel_age_care_timer  = 12.0
        self._barrel_age_care_bonus  = 0.0
        self._barrel_age_done        = False
        # ----- Bottling Station state -----
        self._bottle_phase           = "select"  # select | result
        self._bottle_single_idx      = None
        self._bottle_blend_slots     = []        # list of spirit indices (up to 3)
        self._bottle_select_rects    = {}
        self._bottle_single_btn      = None
        self._bottle_blend_btn       = None
        self._bottle_result_id       = None
        self._bottle_result_spirit   = None
        self._bottle_result_done_btn = None
        # ----- Spirits codex UI state -----
        self._spirits_codex_scroll      = 0
        self._max_spirits_codex_scroll  = 0
        self._spirits_codex_selected    = None
        self._spirits_codex_rects       = {}
        # ----- Brew Kettle state -----
        self._brew_phase          = "select_hop"  # select_hop | select_mash | brewing | result
        self._brew_beer_idx       = None
        self._brew_mash_sel       = None
        self._brew_hop_add        = "early"
        self._brew_temp           = 0.0
        self._brew_temp_vel       = 0.0
        self._brew_heat_held      = False
        self._brew_time           = 0.0
        self._brew_mash_set       = False
        self._brew_hop_set        = False
        self._brew_mash_quality   = 0.0
        self._brew_hop_quality    = 0.0
        self._brew_mash_zone_hit  = False
        self._brew_boil_zone_hit  = False
        self._brew_event_flash    = None
        self._brew_hop_rects      = {}
        self._brew_mash_rects     = {}
        self._brew_start_btn      = None
        self._brew_action_btn     = None
        self._brew_result_beer    = None
        self._brew_result_done_btn = None
        # ----- Fermentation Vessel state -----
        self._ferm_phase          = "select_beer"  # select_beer | select_yeast | fermenting | result
        self._ferm_beer_idx       = None
        self._ferm_yeast_sel      = None
        self._ferm_temp           = 0.15
        self._ferm_temp_vel       = 0.0
        self._ferm_cool_held      = False
        self._ferm_time           = 0.0
        self._ferm_duration       = 45.0
        self._ferm_time_in_optimal = 0.0
        self._ferm_rack_timer     = 10.0
        self._ferm_rack_active    = False
        self._ferm_rack_window    = 0.0
        self._ferm_rack_bonus     = 0.0
        self._ferm_penalties      = 0
        self._ferm_done           = False
        self._ferm_beer_rects     = {}
        self._ferm_yeast_rects    = {}
        self._ferm_start_btn      = None
        self._ferm_result_beer    = None
        self._ferm_result_done_btn = None
        # ----- Taproom state -----
        self._tap_phase           = "select"  # select | configure | conditioning | result
        self._tap_beer_idx        = None
        self._tap_vessel_sel      = None
        self._tap_duration_sel    = None
        self._tap_dry_hop         = False
        self._tap_cond_progress   = 0.0
        self._tap_cond_done       = False
        self._tap_dryhop_active   = False
        self._tap_dryhop_done     = False
        self._tap_dryhop_bonus    = 0.0
        self._tap_beer_rects      = {}
        self._tap_vessel_rects    = {}
        self._tap_duration_rects  = {}
        self._tap_dryhop_btn      = None
        self._tap_start_btn       = None
        self._tap_result_id       = None
        self._tap_result_beer_type = None
        self._tap_result_quality  = 0.0
        self._tap_result_notes    = []
        self._tap_result_done_btn = None
        # ----- Beer codex UI state -----
        self._beer_codex_scroll      = 0
        self._max_beer_codex_scroll  = 0
        self._beer_codex_selected    = None
        self._beer_codex_rects       = {}
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
        self._inv_tab           = 0      # 0=All 1=Seeds 2=Food 3=Tools
        self._inv_tab_rects     = {}
        self._inv_sort_count    = False  # False=alpha  True=by-count desc
        self._inv_sort_btn_rect = None
        self._inv_search        = ""
        self._inv_search_active = False
        self._inv_search_rect   = None
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
        self._breed_nb_rects      = {}         # uid -> no_breed toggle Rect
        self._breed_selected_uid  = None
        self._breed_scroll        = 0
        self._max_breed_scroll    = 0
        # Horse breaking mini-game overlay
        self._hb_active        = False
        self._hb_horse         = None
        self._hb_phase         = "intro"
        self._hb_intro_timer   = 2.5
        self._hb_balance       = 50.0
        self._hb_direction     = 1
        self._hb_buck_timer    = 0.0
        self._hb_buck_interval = 1.2
        self._hb_max_time      = 8.0
        self._hb_active_timer  = 0.0
        self._hb_result        = None
        self._hb_result_timer  = 0.0
        # Horse breeding panel
        self.horse_breeding_open      = False
        self.active_stable_pos        = None   # (bx, by) of the stable block
        self._hbr_horse_a             = None
        self._hbr_horse_b             = None
        self._hbr_breed_btn           = None
        self._hbr_close_btn           = None
        # Horse codex scroll
        self._horse_codex_scroll      = 0
        self._max_horse_codex_scroll  = 0
        # Dog UI state
        self.dog_view_open        = False
        self._dv_dog              = None
        self._dv_close_btn        = None
        self._dv_stay_btn         = None
        self.dog_breeding_open    = False
        self._dbr_dog_a           = None
        self._dbr_dog_b           = None
        self._dbr_breed_btn       = None
        self._dbr_close_btn       = None
        self.active_kennel_pos    = None
        self._dog_codex_scroll     = 0
        self._max_dog_codex_scroll = 0
        self._hunting_codex_scroll     = 0
        self._max_hunting_codex_scroll = 0
        # ----- Tea UI state -----
        self._wither_rack_slot_rects  = {}   # slot index -> Rect
        self._wither_leaf_rects       = {}   # leaf index -> Rect
        self._wither_method_rects     = {}   # method key -> Rect
        self._wither_pending_leaf_idx = None
        self._oxidation_phase        = "select_leaf"  # select_leaf|select_zone|ritual|result
        self._oxidation_leaf_idx     = None
        self._oxidation_time         = 0.0
        self._oxidation_total_time   = 25.0
        self._oxidation_level        = 0.0
        self._oxidation_quality      = 0.0
        self._oxidation_select_rects = {}
        self._oxidation_result_btn   = None
        self._oxidation_lock_btn     = None
        # ritual shared
        self._ox_target_zone         = None   # "white"|"yellow"|"green"|"oolong"|"black"|"puerh"
        self._ox_ritual_quality      = 0.0
        self._ox_zone_btn_rects      = {}
        self._ox_mouse_pos           = (0, 0)
        self._ox_mouse_down          = False
        # white
        self._white_warmth_score     = 0.0
        self._white_dew_pools        = []     # list of {pos, timer, hit}
        self._white_pocket_angle     = 0.0
        self._white_dew_timer        = 0.0
        self._white_dew_next         = 3.0
        # yellow
        self._yellow_wrapped         = False
        self._yellow_heat_arc        = 0.0
        self._yellow_wrap_time       = 0.0
        self._yellow_interval_log    = []     # last 8 interval durations
        self._yellow_rhythm_score    = 0.5
        self._yellow_overflow_time   = 0.0
        # green
        self._green_drag_last        = None
        self._green_drag_vel         = 0.0
        self._green_sectors          = [0.0] * 8
        self._green_enzyme           = 1.0
        self._green_still_timer      = 0.0
        # oolong
        self._oolong_sub             = "roll_1"  # roll_1|rest_1|roll_2|rest_2
        self._oolong_sub_timer       = 0.0
        self._oolong_angle_accum     = 0.0
        self._oolong_prev_angle      = None
        self._oolong_roll1_score     = 0.0
        self._oolong_roll2_score     = 0.0
        self._oolong_rest1_score     = 0.0
        self._oolong_rest2_score     = 0.0
        self._oolong_trail           = []
        self._oolong_rest_start_pos  = None
        # black
        self._black_crush_phase      = True
        self._black_crush_timer      = 0.0
        self._black_ox_timer         = 0.0
        self._black_cells            = [[0]*6 for _ in range(6)]
        self._black_cell_rects       = {}
        self._black_stop_btn         = None
        # puerh
        self._puerh_zone_dwell       = 0.0
        self._puerh_mold_time        = 0.0
        self._puerh_field_rect       = None
        self._tea_cellar_tab          = "brew"
        self._tea_cellar_leaf_idx     = None
        self._tea_cellar_select_rects = {}
        self._tea_cellar_age_rects    = {}
        self._tea_cellar_tab_rects    = {}
        self._tea_cellar_roast_rects  = {}
        self._tea_herbal_rects        = {}
        self._tea_codex_scroll        = 0
        self._max_tea_codex_scroll    = 0
        self._tea_codex_selected      = None
        self._tea_codex_rects         = {}
        self._roasting_phase        = "select_leaf"
        self._roasting_leaf_idx     = None
        self._roasting_select_rects = {}
        self._roasting_level_rects  = {}
        self._roasting_result_btn   = None
        # ----- Herbalism UI state -----
        self._research           = None   # set each frame in draw(); used by kiln/resonance
        self._drying_slot_rects  = {}   # slot index -> Rect
        self._drying_inv_rects   = {}   # src_key -> Rect
        self._dry_flower_btns    = {}
        self._mortar_slots       = [{} for _ in range(2)]
        self._mortar_slot_rects  = []
        self._mortar_active_slot = None
        self._mortar_grind_btn   = None
        self._mortar_inv_rects   = {}
        self._kiln_slots         = [{} for _ in range(4)]
        self._kiln_slot_rects    = []
        self._kiln_active_slot   = None
        self._kiln_brew_btn      = None
        self._kiln_result        = None
        self._kiln_result_btn    = None
        self._kiln_inv_rects     = {}
        self._kiln_inv_scroll    = 0
        self._res_slots          = [{} for _ in range(3)]
        self._res_slot_rects     = []
        self._res_active_slot    = None
        self._res_brew_btn       = None
        self._res_result         = None
        self._res_result_btn     = None
        self._res_inv_rects      = {}
        self._res_inv_scroll     = 0
        self._herb_codex_scroll      = 0
        self._max_herb_codex_scroll  = 0
        self._herb_codex_selected    = None
        self._herb_codex_rects       = {}
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
        # ----- Textile UI state -----
        self._spin_phase        = "select_fiber"
        self._spin_fiber_type   = "wool"
        self._spin_time         = 0.0
        self._spin_tension      = 0.0
        self._spin_quality      = 0.0
        self._spin_held         = False
        self._spin_fiber_rects  = {}
        self._spin_result_btn   = None
        self._dye_tab           = "extract"
        self._dye_tab_rects     = {}
        self._dye_flower_rects  = {}
        self._dye_flower_scroll = 0
        self._dye_thread_idx    = None
        self._dye_thread_rects  = {}
        self._dye_extract_rects = {}
        self._dye_selected_extract = None
        self._dye_result_btn    = None
        self._loom_phase        = "select_thread"
        self._loom_thread_idx   = None
        self._loom_texture      = "plain"
        self._loom_output_type  = "cloth"
        self._loom_thread_rects = {}
        self._loom_texture_rects= {}
        self._loom_output_rects = {}
        self._loom_grid_rects   = []
        self._loom_active_cell  = 0
        self._loom_cell_timer   = 1.2
        self._loom_pattern_score= 0.0
        self._loom_clicked_cells= set()
        self._loom_result_btn   = None
        self.wardrobe_open      = False
        self._wardrobe_slot_rects = {}
        self._wardrobe_item_rects = {}
        self._textile_codex_scroll   = 0
        self._textile_codex_selected = None
        self._textile_codex_rects    = {}
        # ----- Cheese UI state -----
        self._vat_phase          = "select_milk"
        self._vat_select_rects   = {}
        self._vat_current_cheese = None
        self._vat_result_cheese  = None
        self._vat_temp           = 0.0
        self._vat_temp_score     = 0.0
        self._vat_culture_added  = False
        self._vat_culture_score  = 0.0
        self._vat_culture_pulse  = 0.0
        self._vat_penalties      = 0.0
        self._vat_finish_timer   = 3.0
        self._vat_game_done      = False
        self._cp_phase          = "select_curd"
        self._cp_select_rects   = {}
        self._cp_type_rects     = {}
        self._cp_current_curd   = None
        self._cp_type           = "pressed"
        self._cp_pressure       = 0.0
        self._cp_score          = 0.0
        self._cp_timer          = 8.0
        self._cp_game_done      = False
        self._cp_result_cheese  = None
        self._cave_phase           = "select_wheel"
        self._cave_select_rects    = {}
        self._cave_duration_rects  = {}
        self._cave_current_wheel   = None
        self._cave_cycles          = 3
        self._cave_age_progress    = 0.0
        self._cave_care_bonus      = 0.0
        self._cave_care_prompt_timer = 5.0
        self._cave_care_active     = False
        self._cave_care_window     = 0.0
        self._cave_game_done       = False
        self._cave_result_item     = None
        self._cave_result_wheel    = None
        self._cheese_codex_scroll   = 0
        self._cheese_codex_selected = None
        self._cheese_codex_rects    = {}
        # ----- Jewelry UI state -----
        self._jw_phase            = "idle"
        self._jw_type             = None
        self._jw_slot_count       = 1
        self._jw_slots            = []
        self._jw_custom_name      = ""
        self._jw_gem_scroll       = 0
        self._jw_gem_rects        = {}
        self._jw_type_rects       = {}
        self._jw_slot_count_rects = {}
        self._jw_slot_rects       = []
        self._jw_drag_uid         = None
        self._jw_drag_kind        = None
        self._jw_drag_pos         = (0, 0)
        self._jw_detail_jewelry   = None
        self._jw_sell_rects       = {}
        self._jw_confirm_rect     = None
        self._jw_finish_rect      = None
        self._jw_craft_rect       = None
        self._jw_detail_close_rect= None
        self._jewelry_codex_scroll   = 0
        self._jewelry_codex_selected = None
        self._jewelry_codex_rects    = {}

        # Sculpture mini-game
        self._sculpt_phase          = "idle"
        self._sculpt_mineral        = None
        self._sculpt_count          = 0
        self._sculpt_grid           = []
        self._sculpt_undo_stack     = []
        self._sculpt_template       = None
        self._sculpt_cell_rects     = {}
        self._sculpt_template_rects = {}
        self._sculpt_mineral_rects  = {}
        self._sculpt_symmetry       = False   # mirror left↔right while carving
        self._sculpt_drag_mode      = None    # "carve" | "restore" | None
        self._sculpt_hover_cell     = None    # (ri, ci) | None

        # Tapestry mini-game
        self._tapestry_phase          = "idle"
        self._tapestry_thread         = None
        self._tapestry_count          = 0     # height in blocks (1–4)
        self._tapestry_width          = 1     # width in blocks (1–4)
        self._tapestry_grid           = []
        self._tapestry_undo_stack     = []
        self._tapestry_template       = None
        self._tapestry_cell_rects     = {}
        self._tapestry_template_rects = {}
        self._tapestry_thread_rects   = {}
        self._tapestry_symmetry       = False
        self._tapestry_drag_mode      = None   # "weave" | "unweave" | None
        self._tapestry_hover_cell     = None   # (ri, ci) | None

        # Pottery Wheel
        self._wheel_phase        = "select_clay"
        self._wheel_profile      = [3] * 12
        self._wheel_clay_budget  = 0
        self._wheel_clay_loaded  = 0
        self._wheel_spin_angle   = 0.0
        self._wheel_undo_stack   = []
        self._wheel_drag_row     = None
        self._wheel_row_rects    = {}
        self._wheel_clay_btn_rects = {}
        # Pottery Kiln
        self._kiln_tab           = "fire"
        self._kiln_phase         = "select_piece"
        self._kiln_firing_piece  = None
        self._kiln_firing_result_piece = None
        self._kiln_temp          = 0.0
        self._kiln_temp_vel      = 0.0
        self._kiln_time          = 0.0
        self._kiln_total_time    = 35.0
        self._kiln_heat_held     = False
        self._kiln_shock_penalties = 0.0
        self._kiln_time_in_green = 0.0
        self._kiln_event_flash   = None
        self._kiln_select_rects  = {}
        self._kiln_tab_rects     = {}
        # Glazing
        self._glaze_piece_idx    = None
        self._glaze_dust_key     = None
        self._glaze_piece_rects  = {}
        self._glaze_dust_rects   = {}

        # ----- Evaporation Pan mini-game state -----
        self._evap_phase              = "select_crystal"
        self._evap_current_crystal    = None
        self._evap_selected_method    = "solar"
        self._evap_time               = 0.0
        self._evap_temp               = 0.0
        self._evap_time_in_sweet      = 0.0
        self._evap_overheat_penalty   = 0
        self._evap_overheat_accum     = 0.0
        self._evap_crystallize_hit    = False
        self._evap_harvest_hit        = False
        self._evap_event_flash        = None
        self._evap_game_done          = False
        self._evap_result_crystal     = None
        self._evap_select_rects       = {}
        self._evap_method_rects       = {}
        # ----- Salt Grinder state -----
        self._grinder_phase           = "select_crystal"
        self._grinder_current_crystal = None
        self._grinder_select_rects    = {}
        self._grinder_grade_rects     = {}
        self._grinder_result_item     = None
        self._grinder_result_crystal  = None
        # ----- Salt codex UI state -----
        self._salt_codex_scroll       = 0
        self._max_salt_codex_scroll   = 0
        self._salt_codex_selected     = None
        self._salt_codex_rects        = {}

        # ----- Arena state -----
        self.arena_open              = False
        self._arena_phase            = "lobby"
        self._arena_bouts            = []
        self._arena_selected_bout    = 0
        self._arena_bet_fighter      = None
        self._arena_bet_amount       = 10
        self._arena_current_bout     = 0
        self._arena_round_idx        = 0
        self._arena_round_timer      = 0.0
        self._arena_crowd_favor      = 0.5
        self._arena_result_card      = None
        self._arena_gold_delta       = 0
        self._arena_rects            = {}
        self._arena_log_lines        = []
        self._gladiator_codex_scroll = 0

        # ----- Gambling Table state -----
        self.gambling_open        = False
        self._gamble_phase        = "bet"
        self._gamble_bet          = 10
        self._gamble_num_bots     = 3
        self._gamble_bot_names    = []
        self._gamble_bot_picks    = []
        self._gamble_player_pick  = None
        self._gamble_roll_timer   = 0.0
        self._gamble_roll_result  = None
        self._gamble_die1         = 1
        self._gamble_die2         = 1
        self._gamble_result_msg   = ""
        self._gamble_net_gold     = 0
        self._gamble_rects        = {}

        # ----- Horse Racing state -----
        self.racing_open              = False
        self.training_paddock_open    = False
        self._paddock_world           = None
        self._paddock_sel_animal      = "horse"
        self._paddock_sel_stat        = "speed"
        self._paddock_sel_duration    = 3
        self._paddock_rects           = {}
        self._race_phase              = "roster"
        self._race_bookkeeper         = None
        self._race_player_horse       = None
        self._race_horses             = []
        self._race_time               = 0.0
        self._race_bet_horse          = None
        self._race_bet_amount         = 10
        self._race_odds               = {}
        self._race_surges             = {}
        self._race_commentary         = None
        self._race_commentary_triggers = set()
        self._race_result_msg         = ""
        self._race_net_gold           = 0
        self._race_rects              = {}
        self._race_finished           = False
        self._race_placements         = []
        self._race_inspect_uid        = None

        # ----- Smithing / Forge mini-game state -----
        self._smith_phase        = "idle"   # idle|select|heating|hammering|quench|part_complete
        self._smith_tab          = "smith"  # "smith" | "craft"
        self._smith_style        = "classic"  # "classic" | "ornate" | "rugged"
        self._smith_type         = None     # weapon type key
        self._smith_material     = None     # material key
        self._smith_temperature  = 0.0     # 0–100
        self._smith_grid         = []       # 16×10 2D list of cell states
        self._smith_target       = []       # 16×10 bool (target shape)
        self._smith_cell_rects   = {}       # (r, c) → Rect
        self._smith_drag_mode    = None
        self._smith_hover_cell   = None
        self._smith_mistakes     = 0
        self._smith_part_quality = []       # [float] single element while smithing one part
        self._smith_pending_uid  = None     # legacy
        self._smith_type_rects   = {}
        self._smith_mat_rects    = {}
        self._smith_style_rects  = {}
        self._smith_tab_btns     = {}
        self._forge_craft_rects  = {}
        # Weapon rack panel
        self._rack_scroll        = 0
        self._rack_weapon_rects  = {}
        self._rack_equip_btn_rects = {}
        self._rack_inspect_btns  = {}
        # Assembly bench panel
        self._bench_scroll       = 0
        self._bench_assemble_btns = {}
        # Weapon inspect panel
        self._inspect_weapon_uid   = None
        self._inspect_picking_slot = None
        self._picker_type          = None
        self._inspect_add_btns     = {}
        self._inspect_remove_btns  = {}
        self._picker_item_rects    = {}
        self._picker_scroll        = 0
        # Weapon Armorer NPC panel
        self._armorer_sell_rects = {}
        self._armorer_scroll     = 0
        # Garrison Commander NPC panel
        self._garrison_quest_rects = {}

        # ----- Pipe layer UI state -----
        self.hopper_open            = False
        self.active_hopper_pos      = None
        self._hopper_rate_minus     = None
        self._hopper_rate_plus      = None
        self._hopper_close_btn      = None

        self.pipe_output_open       = False
        self.active_pipe_output_pos = None
        self._po_facing_btns        = {}
        self._po_close_btn          = None

        self.pipe_filter_open       = False
        self.active_pipe_filter_pos = None
        self._pf_item_rects         = {}
        self._pf_add_rects          = {}
        self._pf_scroll             = 0
        self._pf_close_btn          = None

        self.pipe_sorter_open       = False
        self.active_pipe_sorter_pos = None
        self._ps_item_rects         = {}
        self._ps_dir_rects          = {}
        self._ps_scroll             = 0
        self._ps_close_btn          = None

        # ----- Factory UI state -----
        self.factory_open           = False
        self.active_factory_pos     = None
        self._fac_input_rects       = {}   # slot_idx -> Rect
        self._fac_output_rects      = {}   # slot_idx -> Rect
        self._fac_count_btns        = {}   # (side, idx, sign) -> Rect
        self._fac_time_btns         = {}   # '+'/'-' -> Rect
        self._fac_pick_rects        = {}   # item_id -> Rect  (item picker)
        self._fac_picking           = None # (side, idx) or None
        self._fac_clear_rects       = {}   # slot_idx -> Rect per side
        self._fac_inv_scroll        = 0
        self._fac_cap_btns          = {}
        self._fac_close_btn         = None


    def open_hopper(self, world, pos):
        self.hopper_open       = True
        self.active_hopper_pos = pos

    def open_pipe_output(self, world, pos):
        self.pipe_output_open       = True
        self.active_pipe_output_pos = pos

    def open_pipe_filter(self, world, pos):
        self.pipe_filter_open       = True
        self.active_pipe_filter_pos = pos
        self._pf_scroll             = 0

    def open_pipe_sorter(self, world, pos):
        self.pipe_sorter_open       = True
        self.active_pipe_sorter_pos = pos
        self._ps_scroll             = 0

    def open_factory(self, world, pos):
        self.factory_open       = True
        self.active_factory_pos = pos
        self._fac_picking       = None
        self._fac_inv_scroll    = 0


    def draw(self, player, research=None, dt=0.0):
        self._research = research   # store so click handlers can access it
        if self._cheat_msg_timer > 0:
            self._cheat_msg_timer -= dt
        if player.dead:
            self._draw_death_screen(player)
            return
        self._draw_health(player)
        self._draw_hunger(player)
        self._draw_breath(player)
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
        if self.town_menu_open and self.active_town is not None:
            self._draw_town_menu(player)
            if self.town_chronicle_open:
                self._draw_city_chronicle(self.active_town)
        if getattr(self, "ruin_plaque_open", False):
            self._draw_ruin_plaque()
        if self.outpost_menu_open and self.active_outpost is not None:
            self._draw_outpost_menu(player)
        if self.landmark_menu_open and self.active_landmark_region is not None:
            self._draw_landmark_menu(player)
        if self.city_block_menu_open and self.active_city_block is not None:
            self._draw_city_block_menu(player)
        if self.coa_designer_open:
            self._draw_coat_of_arms_designer()
        if self.hire_panel_open and self.active_hire_record is not None:
            self._draw_hire_panel(player)
        if self.job_panel_open and self.active_job_record is not None:
            self._draw_job_panel()
        if self.reputation_screen_open:
            self._draw_reputation_screen(player)
        if self.automation_open and self.active_automation is not None:
            self._draw_automation_panel(player)
        if self.farm_bot_open and self.active_farm_bot is not None:
            self._draw_farm_bot_panel(player)
        if self.backhoe_open and self.active_backhoe is not None:
            self._draw_backhoe_panel(player)
        if self.trade_block_open and self.active_trade_pos is not None:
            self._draw_trade_block_panel(player)
        if self.chest_open and self.active_chest_inv is not None:
            self._draw_chest(player)
        if self.garden_open and self.active_garden_flowers is not None:
            self._draw_garden(player)
        if self.wildflower_display_open and self.active_display_pos is not None:
            self._draw_wildflower_display(player)
        if self.cheat_open:
            self._draw_cheat_console()
        if self.pause_open:
            self._draw_pause_menu()
        self._draw_hotbar(player)
        if self.help_open:
            self._draw_help()
        if getattr(player, 'bg_place_mode', False):
            self._draw_bg_mode_indicator()
        self._draw_shape_brush(player)
        self._draw_coffee_buffs(player)
        self._draw_wine_buffs(player)
        self._draw_tea_buffs(player)
        self._draw_herb_buffs(player)
        self._draw_salt_buffs(player)
        self._drain_notifications(player)
        self._draw_toasts(dt)
        if self._drag_item_id is not None and self.inventory_open:
            self._draw_drag_item()
        if self._hb_active:
            self._draw_horse_breaking_overlay(player)
        if self.horse_breeding_open:
            self._draw_horse_breeding_panel(player)
        self._draw_horse_stamina_hud(player)
        if self.dog_view_open:
            self._draw_dog_view_panel(player)
        if self.dog_breeding_open:
            self._draw_dog_breeding_panel(player)
        if self.tea_house_open:
            self._draw_tea_house(player, player.world, dt)
        if self.gambling_open:
            self._draw_gambling(player, dt)
        if self.arena_open:
            self._draw_arena(player, dt)
        if self.racing_open:
            self._draw_racing(player, dt)
        if getattr(self, "training_paddock_open", False):
            self._draw_training_paddock(player, dt)
        if self.wardrobe_open:
            self._draw_wardrobe(player)
        if self.hopper_open and self.active_hopper_pos is not None:
            self._draw_hopper(player, player.world)
        if self.pipe_output_open and self.active_pipe_output_pos is not None:
            self._draw_pipe_output(player, player.world)
        if self.pipe_filter_open and self.active_pipe_filter_pos is not None:
            self._draw_pipe_filter(player, player.world)
        if self.pipe_sorter_open and self.active_pipe_sorter_pos is not None:
            self._draw_pipe_sorter(player, player.world)
        if self.factory_open and self.active_factory_pos is not None:
            self._draw_factory(player, player.world)
        if self._jw_detail_jewelry is not None:
            self._draw_jewelry_detail(player)
        self.draw_smith_hud(player)
        # NPC inspect overlay — drawn on top of everything else
        if getattr(player, "inspecting_npc", None) is not None:
            if getattr(player, "dynasty_tree_open", False):
                self._draw_dynasty_tree(player, player.world)
            elif getattr(player, "dynasty_panel_open", False):
                self._draw_dynasty_chronicle(player, player.world)
            elif getattr(player, "fulfill_request_open", False):
                self._draw_npc_fulfill_request(player, player.world)
            elif getattr(player, "gift_panel_open", False):
                self._draw_npc_gift(player, player.world)
            else:
                self._draw_npc_inspect(player, player.world)

    def _render_stars(self, fnt, quality):
        """Return a Surface with 5 stars: bright gold filled, dim for empty."""
        n = round(max(0.0, min(1.0, quality)) * 5)
        star_w = fnt.render("★", True, (0, 0, 0)).get_width()
        h = fnt.get_height()
        surf = pygame.Surface((star_w * 5, h), pygame.SRCALPHA)
        for i in range(5):
            col = (220, 200, 80) if i < n else (60, 50, 25)
            s = fnt.render("★", True, col)
            surf.blit(s, (i * star_w, 0))
        return surf

