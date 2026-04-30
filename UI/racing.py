import math
import random
import pygame
from Render.largeAnimal import draw_horse_traits
from Render.dogs import draw_dog_from_dict as _draw_dog_from_dict

_BET_OPTIONS = [10, 25, 50, 100, 250]

# Tack item stat boosts applied when building race field
_TACK_BOOSTS = {
    "tack_basic_saddle":    {"race_rating": 0.05},
    "tack_quality_saddle":  {"race_rating": 0.10},
    "tack_champion_saddle": {"race_rating": 0.15},
    "tack_lucky_horseshoe": {"reaction":    0.08},
    "tack_basic_collar":    {"race_rating": 0.05},
    "tack_quality_collar":  {"race_rating": 0.10},
    "tack_champion_collar": {"race_rating": 0.15},
    "tack_blinkers":        {"focus":       0.08},
}

# ---------- Racing style definitions ----------
_STYLE_COLORS = {
    "frontrunner": (255, 160,  60),
    "pacer":       (120, 200, 130),
    "closer":      (100, 160, 240),
    "wild":        (220,  80, 200),
}
_STYLE_LABELS = {
    "frontrunner": "Frontrunner",
    "pacer":       "Pacer",
    "closer":      "Closer",
    "wild":        "Wild Card",
}
_STYLE_DESC = {
    "frontrunner": "Bursts out of the gate hard. Leads early, but drains fast in the final stretch.",
    "pacer":       "Steady and consistent. Holds position without wild swings or sudden moves.",
    "closer":      "Slow start, saves energy. Comes alive in the final third when others tire.",
    "wild":        "Unpredictable. Prone to sudden surges that can win or blow the race entirely.",
}
_STYLE_TIP = {
    "frontrunner": "Bet frontrunners to win only if the field is weak — they need a clear lead.",
    "pacer":       "Pacers rarely collapse. Safe each-way bet, good in a close field.",
    "closer":      "Closers look slow early — don't panic. They finish strong when rivals fade.",
    "wild":        "Wild cards are a gamble within a gamble. High upside, high risk.",
}

# ---------- Commentary ----------
_COMMENTARY = {
    "start":         "And they're off!",
    "early_lead":    "{owner}'s {name} takes an early lead!",
    "fading":        "{name} is fading — stamina gone!",
    "pulling":       "{owner}'s {name} is pulling away!",
    "neck":          "They're neck and neck down the straight!",
    "closer_move":   "The closer is making a move — {name} surging!",
    "final":         "Final sprint! Everything on the line!",
    "finish":        "{owner}'s {name} wins the race!",
    "photo":         "Photo finish! They're almost inseparable!",
    "player_lead":   "Your horse is in the lead — hold on!",
    "player_trail":  "Come on — you need to close the gap!",
}

_RACE_DURATION   = 18.0
_SURGE_CHANCE    = 0.05
_SURGE_BOOST     = 0.18
_SURGE_DURATION  = 0.45
_STAMINA_DRAIN   = 18.0
_RACE_SPEED_SCALE = 0.055

# ---------- Dog racing style definitions ----------
_DOG_STYLE_COLORS = {
    "sprinter": (255, 130,  60),
    "pacer":    (120, 200, 130),
    "chaser":   ( 80, 180, 240),
    "surger":   (220,  80, 200),
}
_DOG_STYLE_LABELS = {
    "sprinter": "Sprinter",
    "pacer":    "Pacer",
    "chaser":   "Chaser",
    "surger":   "Surger",
}
_DOG_STYLE_DESC = {
    "sprinter": "Blazes out of the gate. Dominant early, fades hard if the race runs long.",
    "pacer":    "Steady and reliable. Keeps a consistent pace without wild swings.",
    "chaser":   "Slow starter. Prey drive kicks in when behind — comes alive mid-race.",
    "surger":   "Unpredictable bursts. High upside, high variance.",
}
_DOG_STYLE_TIP = {
    "sprinter": "Best against slow starters. Bet to win only — avoid if field is deep.",
    "pacer":    "Safe each-way bet. Rarely collapses, strong in tight competitive fields.",
    "chaser":   "Don't panic when they're behind early. Watch for the surge after halfway.",
    "surger":   "High risk, high reward. High prey_drive dogs surge far more often.",
}

_DOG_COMMENTARY_PLAYER_LEAD  = "Your dog is in the lead — hold on!"
_DOG_COMMENTARY_PLAYER_TRAIL = "Come on — you need to close the gap!"


def _dog_style_modifiers(d, race_progress, leader_pos):
    """Return (speed_mult, drain_mult) for a dog based on its style and race state."""
    style  = d.get("style", "pacer")
    sprint = d.get("sprint", 1.0)

    if style == "sprinter":
        if race_progress < 0.25:
            speed_mult = 1.15 + (sprint - 1.0) * 0.30
        elif race_progress < 0.65:
            speed_mult = 1.0
        else:
            speed_mult = 0.87
        drain_mult = 1.20 if race_progress < 0.50 else 1.05
    elif style == "chaser":
        if race_progress < 0.30:
            speed_mult = 0.87
        else:
            gap        = max(0.0, leader_pos - d.get("position", 0.0))
            prey_drive = d.get("prey_drive", 0.5)
            speed_mult = 1.0 + prey_drive * 0.18 * min(1.0, gap * 5)
        drain_mult = 0.90 if race_progress < 0.60 else 0.98
    elif style == "surger":
        speed_mult = 1.0
        drain_mult = 1.0
    else:  # pacer
        speed_mult = 1.0
        drain_mult = 0.93

    return speed_mult, drain_mult


def _style_modifiers(h, race_progress, dt):
    """Return (speed_mult, drain_mult) based on racing style and current progress."""
    style = h.get("style", "pacer")
    sm_frac = h["stamina"] / 100.0

    if style == "frontrunner":
        speed_mult = 1.12 if race_progress < 0.25 else (1.0 if race_progress < 0.65 else 0.90)
        drain_mult = 1.25 if race_progress < 0.50 else 1.05
    elif style == "closer":
        speed_mult = 0.88 if race_progress < 0.40 else (1.0 if race_progress < 0.70 else 1.15)
        drain_mult = 0.85 if race_progress < 0.60 else 0.95
    elif style == "wild":
        speed_mult = 1.0
        drain_mult = 1.0
        # Wild gets double surge chance (handled in tick_race separately)
    else:  # pacer
        speed_mult = 1.0
        drain_mult = 0.95

    return speed_mult, drain_mult


# _draw_dog_racer removed — replaced by _draw_dog_from_dict import above


class RacingMixin:

    # ------------------------------------------------------------------
    # Open / close
    # ------------------------------------------------------------------

    def open_racing(self, bookkeeper_npc, player):
        self.racing_open              = True
        self._race_phase              = "choose"
        self._race_mode               = "horse"   # "horse" | "dog"
        self._race_bookkeeper         = bookkeeper_npc
        self._race_player_horse       = self._find_player_horse(player)
        self._race_player_dog         = self._find_player_dog(player)
        self._race_horses             = []
        self._race_time               = 0.0
        self._race_bet_horse          = None
        self._race_bet_amount         = _BET_OPTIONS[0]
        self._race_commentary         = None
        self._race_result_msg         = ""
        self._race_net_gold           = 0
        self._race_rects              = {}
        self._race_finished           = False
        self._race_placements         = []
        self._race_commentary_triggers = set()
        self._race_inspect_uid        = None
        self._circuit_reg_tier        = 1
        self._circuit_reg_mode        = "horse"
        self._circuit_leg_active      = False
        self._race_steeplechase       = False  # Flat or Steeplechase toggle
        self._race_jump_flashes       = {}     # {racer_uid: flash_timer} for stumble visual

    def _find_player_horse(self, player):
        from horses import Horse as _Horse
        world = getattr(player, "world", None)
        if world is None:
            return None
        for ent in world.entities:
            if isinstance(ent, _Horse) and ent.tamed and not ent.dead and ent.rider is None:
                return ent
        return None

    def _find_player_dog(self, player):
        from dogs import Dog as _Dog
        world = getattr(player, "world", None)
        if world is None:
            return None
        px = getattr(player, "x", 0)
        py = getattr(player, "y", 0)
        for ent in world.entities:
            if isinstance(ent, _Dog) and ent.tamed and not ent.dead and not ent.stay_mode:
                dx = abs(getattr(ent, "x", 0) - px)
                dy = abs(getattr(ent, "y", 0) - py)
                if dx < 512 and dy < 512:
                    return ent
        return None

    def _resolve_owner_names(self, npc_horses, player):
        """Overwrite placeholder owner names with real NPC names from nearby entities."""
        world  = getattr(player, "world", None)
        if world is None:
            return
        bkp = self._race_bookkeeper
        bkp_x = getattr(bkp, "x", 0)

        from cities import NPC as _NPC
        nearby_names = []
        for ent in world.entities:
            if isinstance(ent, _NPC) and not isinstance(ent, type(bkp)):
                dx = abs(getattr(ent, "x", 0) - bkp_x)
                if dx < 60 * 32:   # 60 blocks radius
                    nm = getattr(ent, "name", None)
                    if nm and nm not in nearby_names:
                        nearby_names.append(nm)

        # Assign a unique nearby NPC name to each horse where possible
        used = set()
        for h in npc_horses:
            for nm in nearby_names:
                if nm not in used:
                    h["owner"] = nm.split()[0] if " " in nm else nm  # first name only
                    used.add(nm)
                    break

    def _build_race_field(self, player):
        npc    = self._race_bookkeeper
        horses = []

        ph = self._race_player_horse
        if ph is not None:
            pt = ph.traits
            _saddle_b = _TACK_BOOSTS.get(pt.get("equipped_saddle"), {})
            _shoe_b   = _TACK_BOOSTS.get(pt.get("equipped_horseshoe"), {})
            _tb       = pt.get("training_bonuses", {})
            _rr = min(1.5, ph.race_rating + _saddle_b.get("race_rating", 0) + _tb.get("speed", 0) * 0.40)
            horses.append({
                "uid":          getattr(ph, "uid", "player"),
                "name":         getattr(ph, "name", "Your Horse"),
                "owner":        "You",
                "race_rating":  _rr,
                "stamina":      100.0,
                "stamina_max":  pt.get("stamina_max", 1.0),
                "endurance":    min(1.3, pt.get("endurance", 1.0) + _tb.get("endurance", 0)),
                "reaction":     min(1.3, pt.get("reaction", 1.0) + _shoe_b.get("reaction", 0) + _tb.get("reaction", 0)),
                "agility":      min(1.3, pt.get("agility", 1.0) + _tb.get("agility", 0)),
                "heart":        pt.get("heart", 1.0),
                "coat_color":   pt.get("coat_color", (160, 120, 60)),
                "coat_pattern": pt.get("coat_pattern", "solid"),
                "leg_marking":  pt.get("leg_marking", "none"),
                "mane_color":   pt.get("mane_color", "match"),
                "face_marking": pt.get("face_marking", "none"),
                "temperament":  pt.get("temperament", "spirited"),
                "color_shift":  pt.get("color_shift", (0, 0, 0)),
                "size":         pt.get("size", 1.0),
                "style":        "pacer",   # player's horse has no preset style
                "wins":         getattr(player, "races_won", 0),
                "races":        getattr(player, "races_entered", 0),
                "is_player":    True,
                "position":     0.0,
                "place":        0,
                "surge_timer":  0.0,
                "finished":     False,
                "jumps_cleared": [False, False, False],
            })

        npc_horse_defs = npc._npc_horses if npc else []
        self._resolve_owner_names(npc_horse_defs, player)

        for h in npc_horse_defs:
            horses.append({
                "uid":          h["name"],
                "name":         h["name"],
                "owner":        h.get("owner", "Local"),
                "race_rating":  h["race_rating"],
                "stamina":      100.0,
                "stamina_max":  h.get("stamina_max", 1.0),
                "endurance":    h.get("endurance", 1.0),
                "reaction":     h.get("reaction", 1.0),
                "agility":      h.get("agility", 1.0),
                "heart":        h.get("heart", 1.0),
                "coat_color":   h.get("coat_color", (140, 100, 60)),
                "coat_pattern": h.get("coat_pattern", "solid"),
                "leg_marking":  h.get("leg_marking", "none"),
                "mane_color":   h.get("mane_color", "match"),
                "face_marking": h.get("face_marking", "none"),
                "temperament":  h.get("temperament", "spirited"),
                "color_shift":  (0, 0, 0),
                "size":         1.0,
                "style":        h.get("style", "pacer"),
                "wins":         h.get("wins", 0),
                "races":        h.get("races", 0),
                "is_player":    False,
                "position":     0.0,
                "place":        0,
                "surge_timer":  0.0,
                "finished":     False,
                "jumps_cleared": [False, False, False],
            })

        ratings = [h["race_rating"] for h in horses]
        avg = sum(ratings) / max(len(ratings), 1)
        for h in horses:
            ratio = avg / max(h["race_rating"], 0.01)
            h["odds"] = round(max(1.1, min(8.0, ratio * 1.6)), 1)

        return horses

    # ------------------------------------------------------------------
    # Main draw dispatcher
    # ------------------------------------------------------------------

    def _draw_racing(self, player, dt):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))

        sw, sh = self.screen.get_size()
        pw, ph = 740, 500
        px = (sw - pw) // 2
        py = (sh - ph) // 2

        pygame.draw.rect(self.screen, (50, 38, 24), (px, py, pw, ph), border_radius=8)
        pygame.draw.rect(self.screen, (195, 165, 100), (px, py, pw, ph), 1, border_radius=8)
        pygame.draw.rect(self.screen, (66, 50, 32), (px + 10, py + 10, pw - 20, ph - 20), border_radius=6)

        mode = getattr(self, "_race_mode", "horse")
        title_str = "Dog Racing" if mode == "dog" else "Horse Racing"
        title = self.font.render(title_str, True, (230, 205, 130))
        self.screen.blit(title, (px + pw // 2 - title.get_width() // 2, py + 13))

        phase = self._race_phase
        if phase == "choose":
            self._draw_race_choose(player, px, py, pw, ph)
        elif phase == "tack_shop":
            self._draw_tack_shop(player, px, py, pw, ph)
        elif phase == "circuit_menu":
            self._draw_circuit_menu(player, px, py, pw, ph)
        elif phase == "circuit_legs":
            self._draw_circuit_legs(player, px, py, pw, ph)
        elif phase == "circuit_result":
            self._draw_circuit_result(player, px, py, pw, ph)
        elif phase == "roster":
            if mode == "dog":
                self._draw_dog_race_roster(player, px, py, pw, ph)
            else:
                self._draw_race_roster(player, px, py, pw, ph)
        elif phase == "inspect":
            if mode == "dog":
                self._draw_dog_race_inspect(player, px, py, pw, ph)
            else:
                self._draw_race_inspect(player, px, py, pw, ph)
        elif phase == "bet":
            if mode == "dog":
                self._draw_dog_race_bet(player, px, py, pw, ph)
            else:
                self._draw_race_bet(player, px, py, pw, ph)
        elif phase == "gate":
            self._draw_race_gate(player, dt, px, py, pw, ph)
        elif phase == "racing":
            self._draw_race_racing(player, dt, px, py, pw, ph)
        elif phase == "photo_finish":
            self._draw_race_photo_finish(player, dt, px, py, pw, ph)
        elif phase == "result":
            self._draw_race_result(player, px, py, pw, ph)

    # ------------------------------------------------------------------
    # Phase: roster — field overview
    # ------------------------------------------------------------------

    def _draw_race_roster(self, player, px, py, pw, ph):
        self._race_rects = {}
        npc = self._race_bookkeeper
        if not self._race_horses:
            self._race_horses = self._build_race_field(player)

        fee     = npc.entry_fee(player) if npc else 50
        champ   = npc.is_champion_ring() if npc else False
        ring_lbl = self.small.render(
            ("Champion Ring" if champ else "Racing Ring") + f"  —  Entry fee: {fee}g",
            True, (200, 175, 110))
        self.screen.blit(ring_lbl, (px + pw // 2 - ring_lbl.get_width() // 2, py + 38))

        # Steeplechase toggle
        sc = getattr(self, "_race_steeplechase", False)
        for tog_lbl, tog_val, tog_x in [("Flat Race", False, px + pw // 2 - 115), ("Steeplechase", True, px + pw // 2 + 5)]:
            tr = pygame.Rect(tog_x, py + 54, 110, 22)
            sel = (sc == tog_val)
            pygame.draw.rect(self.screen, (55, 130, 60) if sel else (40, 40, 40), tr, border_radius=3)
            pygame.draw.rect(self.screen, (180, 230, 150) if sel else (70, 70, 70), tr, 1, border_radius=3)
            tt = self.small.render(tog_lbl, True, (230, 225, 200))
            self.screen.blit(tt, (tr.centerx - tt.get_width() // 2, tr.centery - tt.get_height() // 2))
            self._race_rects[("steeplechase_toggle", tog_val)] = tr

        # Column headers
        hdr_y = py + 82
        headers = [("Horse & Owner", px + 50), ("Style", px + 295),
                   ("Form", px + 430), ("Odds", px + 530), ("Speed", px + 610)]
        for txt, cx in headers:
            ht = self.small.render(txt, True, (160, 140, 80))
            self.screen.blit(ht, (cx, hdr_y))

        # Divider
        pygame.draw.line(self.screen, (130, 100, 50),
                         (px + 25, hdr_y + 14), (px + pw - 25, hdr_y + 14), 1)

        # Horse rows
        row_h = 38
        for i, h in enumerate(self._race_horses):
            ry       = hdr_y + 18 + i * row_h
            selected = (self._race_inspect_uid == h["uid"])

            # Row highlight
            if selected:
                pygame.draw.rect(self.screen, (75, 60, 38), (px + 25, ry, pw - 50, row_h - 2), border_radius=3)
                pygame.draw.rect(self.screen, (200, 160, 80), (px + 25, ry, pw - 50, row_h - 2), 1, border_radius=3)

            # Coat swatch
            pygame.draw.rect(self.screen, h["coat_color"], (px + 30, ry + 8, 14, 14), border_radius=3)
            if h.get("is_player"):
                pygame.draw.rect(self.screen, (255, 230, 100), (px + 30, ry + 8, 14, 14), 2, border_radius=3)

            # Horse name
            name_col = (255, 235, 130) if h.get("is_player") else (215, 200, 170)
            nt = self.small.render(h["name"], True, name_col)
            self.screen.blit(nt, (px + 50, ry + 2))

            # Owner name in dim text below
            owner_col = (140, 120, 80) if not h.get("is_player") else (160, 200, 140)
            ot = self.small.render(f"owned by {h['owner']}", True, owner_col)
            self.screen.blit(ot, (px + 50, ry + 18))

            # Style badge
            style = h.get("style", "pacer")
            sc    = _STYLE_COLORS.get(style, (160, 160, 160))
            sl    = _STYLE_LABELS.get(style, style.title())
            badge_surf = self.small.render(sl, True, sc)
            self.screen.blit(badge_surf, (px + 295, ry + 10))

            # Form record (W / R)
            wins  = h.get("wins", 0)
            races = h.get("races", 0)
            if races > 0:
                form_str  = f"{wins}W / {races}R"
                win_rate  = wins / races
                form_col  = (100, 230, 100) if win_rate >= 0.5 else \
                            ((230, 210, 80) if win_rate >= 0.25 else (200, 100, 80))
            else:
                form_str = "Debut"
                form_col = (180, 160, 120)
            ft = self.small.render(form_str, True, form_col)
            self.screen.blit(ft, (px + 430, ry + 10))

            # Odds
            ot2 = self.small.render(f"{h['odds']}x", True, (220, 190, 100))
            self.screen.blit(ot2, (px + 530, ry + 10))

            # Speed bar (race_rating)
            spd_bar_x = px + 610
            spd       = h["race_rating"]
            bar_w     = int((spd - 0.5) / 1.0 * 70)
            bar_col   = (100, 200, 100) if h.get("is_player") else (150, 180, 130)
            pygame.draw.rect(self.screen, (45, 38, 25), (spd_bar_x, ry + 10, 70, 10), border_radius=2)
            pygame.draw.rect(self.screen, bar_col, (spd_bar_x, ry + 10, bar_w, 10), border_radius=2)

            # Click rect for whole row
            row_rect = pygame.Rect(px + 25, ry, pw - 50, row_h - 2)
            self._race_rects[("inspect", h["uid"])] = row_rect

        # Hint line
        hint = self.small.render("Click a horse to inspect  •  ESC to leave", True, (120, 105, 70))
        self.screen.blit(hint, (px + pw // 2 - hint.get_width() // 2, py + ph - 108))

        # Buttons
        has_horse  = self._race_player_horse is not None
        has_field  = any(not h.get("is_player") for h in self._race_horses)
        can_enter  = has_horse and has_field and player.money >= fee

        spectating = not has_horse  # no horse = spectator mode
        enter_label = "Watch Race" if spectating else "Enter Race"
        enter_rect = pygame.Rect(px + pw // 2 - 130, py + ph - 80, 120, 36)
        ec = (55, 140, 55) if (can_enter or spectating) else (50, 50, 50)
        pygame.draw.rect(self.screen, ec, enter_rect, border_radius=5)
        pygame.draw.rect(self.screen, (180, 230, 150) if (can_enter or spectating) else (90, 90, 90), enter_rect, 1, border_radius=5)
        el = self.font.render(enter_label, True, (240, 240, 210) if (can_enter or spectating) else (120, 120, 120))
        self.screen.blit(el, (enter_rect.centerx - el.get_width() // 2, enter_rect.centery - el.get_height() // 2))
        self._race_rects["enter"] = enter_rect

        if not has_horse and not spectating:
            nh = self.small.render("(Bring a tamed horse)", True, (170, 120, 80))
            self.screen.blit(nh, (px + pw // 2 - nh.get_width() // 2, py + ph - 38))
        elif not has_field:
            nh = self.small.render("(No other horses entered)", True, (170, 120, 80))
            self.screen.blit(nh, (px + pw // 2 - nh.get_width() // 2, py + ph - 38))

        close_rect = pygame.Rect(px + pw // 2 + 10, py + ph - 80, 120, 36)
        pygame.draw.rect(self.screen, (80, 40, 40), close_rect, border_radius=5)
        pygame.draw.rect(self.screen, (180, 120, 120), close_rect, 1, border_radius=5)
        cl = self.font.render("Leave", True, (230, 190, 190))
        self.screen.blit(cl, (close_rect.centerx - cl.get_width() // 2, close_rect.centery - cl.get_height() // 2))
        self._race_rects["close"] = close_rect

    # ------------------------------------------------------------------
    # Phase: inspect — per-horse detail view
    # ------------------------------------------------------------------

    def _draw_race_inspect(self, player, px, py, pw, ph):
        self._race_rects = {}
        h = next((x for x in self._race_horses if x["uid"] == self._race_inspect_uid), None)
        if h is None:
            self._race_phase = "roster"
            return

        npc     = self._race_bookkeeper
        favored = self._race_is_favored(player)

        # Header
        pygame.draw.rect(self.screen, h["coat_color"],
                         (px + pw // 2 - 20, py + 42, 40, 20), border_radius=4)
        name_t = self.font.render(h["name"], True, (230, 215, 170))
        self.screen.blit(name_t, (px + pw // 2 - name_t.get_width() // 2, py + 42))

        owner_t = self.small.render(f"Owned by  {h['owner']}", True, (170, 150, 100))
        self.screen.blit(owner_t, (px + pw // 2 - owner_t.get_width() // 2, py + 64))

        # Style block
        style    = h.get("style", "pacer")
        sc       = _STYLE_COLORS.get(style, (160, 160, 160))
        sl       = _STYLE_LABELS.get(style, style.title())
        desc     = _STYLE_DESC.get(style, "")
        tip      = _STYLE_TIP.get(style, "")

        style_lbl = self.font.render(f"Racing style:  {sl}", True, sc)
        self.screen.blit(style_lbl, (px + 40, py + 96))

        # Wrap style description
        words = desc.split()
        line, lines = "", []
        for w in words:
            if self.small.size(line + w)[0] < pw - 90:
                line += w + " "
            else:
                lines.append(line.strip())
                line = w + " "
        if line:
            lines.append(line.strip())
        for j, ln in enumerate(lines):
            dt_surf = self.small.render(ln, True, (175, 160, 125))
            self.screen.blit(dt_surf, (px + 40, py + 118 + j * 16))

        # Divider
        pygame.draw.line(self.screen, (100, 80, 45),
                         (px + 40, py + 165), (px + pw - 40, py + 165), 1)

        # Stat grid — shown fully if player's horse or favored
        stat_y = py + 175
        stats = [
            ("Race Rating",  h["race_rating"]),
            ("Stamina",      h["stamina_max"]  if (h.get("is_player") or favored) else None),
            ("Endurance",    h["endurance"]    if (h.get("is_player") or favored) else None),
            ("Reaction",     h["reaction"]     if (h.get("is_player") or favored) else None),
            ("Heart",        h["heart"]        if (h.get("is_player") or favored) else None),
        ]
        col_x = [px + 40, px + 220, px + 410, px + 590]
        for k, (label, val) in enumerate(stats):
            cx  = col_x[k % 4]
            row = stat_y + (k // 4) * 50
            pygame.draw.rect(self.screen, (40, 32, 20), (cx, row, 155, 40), border_radius=3)
            pygame.draw.rect(self.screen, (100, 80, 45), (cx, row, 155, 40), 1, border_radius=3)
            lbl_s = self.small.render(label, True, (150, 135, 95))
            self.screen.blit(lbl_s, (cx + 6, row + 4))
            if val is not None:
                bar_w = int((val - 0.5) / 1.0 * 130)
                bar_col = (120, 210, 120) if val > 1.0 else (170, 150, 90) if val > 0.85 else (200, 100, 80)
                pygame.draw.rect(self.screen, (30, 24, 15), (cx + 6, row + 24, 130, 8), border_radius=2)
                pygame.draw.rect(self.screen, bar_col, (cx + 6, row + 24, bar_w, 8), border_radius=2)
                num_s = self.small.render(f"{val:.2f}", True, bar_col)
                self.screen.blit(num_s, (cx + 118, row + 22))
            else:
                unk_s = self.small.render("??? (Get Favored)", True, (110, 95, 65))
                self.screen.blit(unk_s, (cx + 6, row + 22))

        # Form
        wins  = h.get("wins", 0)
        races = h.get("races", 0)
        form_y = stat_y + 60
        if races > 0:
            win_rate = wins / races
            form_col = (100, 230, 100) if win_rate >= 0.5 else \
                       ((230, 210, 80) if win_rate >= 0.25 else (200, 100, 80))
            form_s = self.small.render(f"Career record:  {wins} wins from {races} races", True, form_col)
        else:
            form_s = self.small.render("Career record:  First race — no history", True, (160, 145, 100))
        self.screen.blit(form_s, (px + 40, form_y))

        # Bookkeeper tip
        tip_y = form_y + 24
        pygame.draw.line(self.screen, (100, 80, 45),
                         (px + 40, tip_y - 4), (px + pw - 40, tip_y - 4), 1)
        tip_hdr = self.small.render("Bookkeeper's tip:", True, (180, 155, 90))
        self.screen.blit(tip_hdr, (px + 40, tip_y + 2))
        tip_words = tip.split()
        tline, tlines = "", []
        for w in tip_words:
            if self.small.size(tline + w)[0] < pw - 90:
                tline += w + " "
            else:
                tlines.append(tline.strip())
                tline = w + " "
        if tline:
            tlines.append(tline.strip())
        for j, ln in enumerate(tlines):
            ts = self.small.render(ln, True, (200, 180, 130))
            self.screen.blit(ts, (px + 40, tip_y + 18 + j * 15))

        # Buttons
        back_rect = pygame.Rect(px + pw // 2 - 130, py + ph - 64, 120, 36)
        pygame.draw.rect(self.screen, (55, 44, 28), back_rect, border_radius=5)
        pygame.draw.rect(self.screen, (160, 130, 70), back_rect, 1, border_radius=5)
        bl = self.font.render("< Back", True, (215, 195, 140))
        self.screen.blit(bl, (back_rect.centerx - bl.get_width() // 2, back_rect.centery - bl.get_height() // 2))
        self._race_rects["back_from_inspect"] = back_rect

        npc_entry = npc
        fee = npc_entry.entry_fee(player) if npc_entry else 50
        has_horse = self._race_player_horse is not None
        has_field = any(not h.get("is_player") for h in self._race_horses)
        can_enter = has_horse and has_field and player.money >= fee

        enter_rect = pygame.Rect(px + pw // 2 + 10, py + ph - 64, 120, 36)
        ec = (55, 140, 55) if can_enter else (50, 50, 50)
        pygame.draw.rect(self.screen, ec, enter_rect, border_radius=5)
        pygame.draw.rect(self.screen, (180, 230, 150) if can_enter else (90, 90, 90), enter_rect, 1, border_radius=5)
        el = self.font.render("Enter Race", True, (240, 240, 210) if can_enter else (120, 120, 120))
        self.screen.blit(el, (enter_rect.centerx - el.get_width() // 2, enter_rect.centery - el.get_height() // 2))
        self._race_rects["enter"] = enter_rect

    def _race_is_favored(self, player):
        npc = self._race_bookkeeper
        if npc is None:
            return False
        region = getattr(npc, "_region_id", None)
        if region is None:
            return False
        return region in getattr(player, "favored_dynasty_regions", set()) \
            or region in getattr(player, "champion_dynasty_regions", set())

    # ------------------------------------------------------------------
    # Phase: bet — choose horse + wager
    # ------------------------------------------------------------------

    def _draw_race_bet(self, player, px, py, pw, ph):
        self._race_rects = {}
        lbl = self.font.render("Place your bet — who wins the race?", True, (230, 205, 130))
        self.screen.blit(lbl, (px + pw // 2 - lbl.get_width() // 2, py + 42))

        gold_t = self.small.render(f"Gold: {player.money}", True, (200, 175, 100))
        self.screen.blit(gold_t, (px + pw // 2 - gold_t.get_width() // 2, py + 64))

        row_h = 36
        hy    = py + 92
        for i, h in enumerate(self._race_horses):
            ry       = hy + i * row_h
            selected = (self._race_bet_horse == h["uid"])
            bg     = (55, 90, 45) if selected else (38, 50, 30)
            border = (160, 230, 140) if selected else (80, 110, 68)
            rect   = pygame.Rect(px + 30, ry, pw - 60, row_h - 4)
            pygame.draw.rect(self.screen, bg, rect, border_radius=4)
            pygame.draw.rect(self.screen, border, rect, 1, border_radius=4)

            # Coat swatch
            pygame.draw.rect(self.screen, h["coat_color"], (rect.x + 6, ry + 10, 12, 12), border_radius=3)

            # Name + style tag
            nc = (255, 235, 130) if h.get("is_player") else (215, 200, 170)
            nt = self.small.render(h["name"], True, nc)
            self.screen.blit(nt, (rect.x + 24, ry + 2))

            style  = h.get("style", "pacer")
            sc     = _STYLE_COLORS.get(style, (160, 160, 160))
            sl     = _STYLE_LABELS.get(style, style.title())
            st_s   = self.small.render(f"[{sl}]", True, sc)
            self.screen.blit(st_s, (rect.x + 24, ry + 18))

            # Owner
            ot = self.small.render(f"{h['owner']}", True, (140, 120, 80))
            self.screen.blit(ot, (rect.x + 130, ry + 18))

            # Odds
            odds_t = self.small.render(f"{h['odds']}x payout", True, (210, 185, 100))
            self.screen.blit(odds_t, (rect.right - odds_t.get_width() - 10, ry + 10))

            self._race_rects[("pick_horse", h["uid"])] = rect

        # Bet amount
        bet_y = hy + len(self._race_horses) * row_h + 12
        bl2 = self.small.render("Bet amount:", True, (160, 145, 90))
        self.screen.blit(bl2, (px + 30, bet_y))
        btn_w, btn_h = 82, 30
        for j, amt in enumerate(_BET_OPTIONS):
            bx    = px + 30 + j * (btn_w + 8)
            brect = pygame.Rect(bx, bet_y + 20, btn_w, btn_h)
            sel   = (self._race_bet_amount == amt)
            aff   = (player.money >= amt)
            bc    = (55, 140, 70) if sel else ((38, 85, 50) if aff else (45, 45, 45))
            pygame.draw.rect(self.screen, bc, brect, border_radius=4)
            pygame.draw.rect(self.screen, (180, 230, 160) if sel else (85, 120, 85), brect, 1, border_radius=4)
            at = self.small.render(f"{amt}g", True, (240, 230, 180) if aff else (110, 110, 110))
            self.screen.blit(at, (brect.centerx - at.get_width() // 2, brect.centery - at.get_height() // 2))
            self._race_rects[("bet_amt", amt)] = brect

        can_go = (self._race_bet_horse is not None) and (player.money >= self._race_bet_amount)
        go_rect = pygame.Rect(px + pw // 2 - 70, py + ph - 80, 140, 38)
        pygame.draw.rect(self.screen, (55, 150, 55) if can_go else (45, 45, 45), go_rect, border_radius=5)
        pygame.draw.rect(self.screen, (180, 240, 150), go_rect, 1, border_radius=5)
        go_t = self.font.render("To the Gates!", True, (245, 240, 210) if can_go else (120, 120, 120))
        self.screen.blit(go_t, (go_rect.centerx - go_t.get_width() // 2, go_rect.centery - go_t.get_height() // 2))
        self._race_rects["go"] = go_rect

        back_rect = pygame.Rect(px + pw // 2 - 50, py + ph - 38, 100, 26)
        pygame.draw.rect(self.screen, (65, 32, 32), back_rect, border_radius=4)
        pygame.draw.rect(self.screen, (150, 100, 100), back_rect, 1, border_radius=4)
        bk_t = self.small.render("Back", True, (200, 165, 165))
        self.screen.blit(bk_t, (back_rect.centerx - bk_t.get_width() // 2, back_rect.centery - bk_t.get_height() // 2))
        self._race_rects["back"] = back_rect

    # ------------------------------------------------------------------
    # Phase: gate — countdown
    # ------------------------------------------------------------------

    def _draw_race_gate(self, player, dt, px, py, pw, ph):
        self._race_time += dt
        t = self._race_time

        if t < 3.0:
            count = 3 - int(t)
            size  = max(1, int(80 - (t % 1.0) * 30))
            cs    = pygame.font.Font(None, size * 2).render(str(count), True, (255, 220, 80))
            self.screen.blit(cs, (px + pw // 2 - cs.get_width() // 2,
                                  py + ph // 2 - cs.get_height() // 2))
        else:
            gs = self.font.render("GO!", True, (100, 255, 100))
            self.screen.blit(gs, (px + pw // 2 - gs.get_width() // 2,
                                  py + ph // 2 - gs.get_height() // 2))
            if t >= 3.6:
                self._race_time  = 0.0
                self._race_phase = "racing"
                self._race_commentary = (_COMMENTARY["start"], 2.5)

        # Show the full field in starting order (sorted by race_rating desc)
        sorted_field = sorted(self._race_horses, key=lambda x: x["race_rating"], reverse=True)
        sl_y = py + 80
        for i, h in enumerate(sorted_field):
            style  = h.get("style", "pacer")
            sc_col = _STYLE_COLORS.get(style, (160, 160, 160))
            sl_lbl = _STYLE_LABELS.get(style, "")
            name_c = (255, 235, 130) if h.get("is_player") else (200, 185, 155)
            ns = self.small.render(f"#{i+1}  {h['name']}  ({h['owner']})", True, name_c)
            ss = self.small.render(f"[{sl_lbl}]  {h['odds']}x", True, sc_col)
            self.screen.blit(ns, (px + 60, sl_y + i * 22))
            self.screen.blit(ss, (px + pw - 200, sl_y + i * 22))

        hint = self.small.render("The gates are opening...", True, (155, 135, 85))
        self.screen.blit(hint, (px + pw // 2 - hint.get_width() // 2, py + ph - 50))

    # ------------------------------------------------------------------
    # Phase: racing — animated race
    # ------------------------------------------------------------------

    def _draw_race_racing(self, player, dt, px, py, pw, ph):
        if not self._race_finished:
            if getattr(self, "_race_mode", "horse") == "dog":
                self._tick_dog_race(dt, player)
            else:
                self._tick_race(dt, player)

        # Track area (left 3/4 of panel)
        track_x = px + 20
        track_w = pw - 190   # leave right column for standings
        track_h = len(self._race_horses) * 52 + 20
        track_y = py + 50
        pygame.draw.rect(self.screen, (38, 28, 15), (track_x, track_y, track_w, track_h), border_radius=4)
        pygame.draw.rect(self.screen, (130, 100, 50), (track_x, track_y, track_w, track_h), 1, border_radius=4)

        # Finish line checkered flag
        fl_x = track_x + track_w - 28
        for seg in range(0, track_h, 8):
            col = (255, 255, 255) if (seg // 8) % 2 == 0 else (10, 10, 10)
            pygame.draw.rect(self.screen, col, (fl_x, track_y + seg, 6, min(8, track_h - seg)))

        # Steeplechase hurdles
        if getattr(self, "_race_steeplechase", False):
            for jump_frac in [0.25, 0.55, 0.85]:
                hx = track_x + 10 + int(jump_frac * (track_w - 80))
                pygame.draw.rect(self.screen, (220, 200, 150), (hx - 2, track_y, 4, track_h))
                pygame.draw.rect(self.screen, (160, 100, 40), (hx - 4, track_y, 8, 6))
            # Flash "!" for stumbles
            flashes = getattr(self, "_race_jump_flashes", {})
            for h in self._race_horses:
                if h["uid"] in flashes and flashes[h["uid"]] > 0:
                    hx_pos = track_x + 10 + int(h["position"] * (track_w - 80))
                    hy_pos = track_y + 14 + self._race_horses.index(h) * 52
                    ft = self.font.render("!", True, (255, 80, 60))
                    self.screen.blit(ft, (hx_pos + 2, hy_pos - 20))
                    flashes[h["uid"]] -= 0.016

        # Sort horses by current position for standings
        sorted_h = sorted(self._race_horses, key=lambda x: x["position"], reverse=True)

        _HORSE_W, _HORSE_H = 40, 26
        for i, h in enumerate(self._race_horses):
            hy  = track_y + 14 + i * 52
            hx  = track_x + 10 + int(h["position"] * (track_w - 80))

            is_leading = (h is sorted_h[0])

            # Lead glow
            if is_leading:
                pulse    = (math.sin(pygame.time.get_ticks() * 0.01) + 1) * 0.5
                glow_r   = int(18 + 7 * pulse)
                glow_s   = pygame.Surface((glow_r * 4, glow_r * 4), pygame.SRCALPHA)
                gc       = h["coat_color"]
                pygame.draw.circle(glow_s, (gc[0], gc[1], gc[2], 55),
                                   (glow_r * 2, glow_r * 2), glow_r * 2)
                self.screen.blit(glow_s, (hx + 20 - glow_r * 2, hy + 13 - glow_r * 2))

            # Player horse highlight border
            if h.get("is_player"):
                pygame.draw.rect(self.screen, (255, 230, 80),
                                 (hx - 2, hy - 6, _HORSE_W + 4, _HORSE_H + 10), 1,
                                 border_radius=2)

            # Racer sprite — dog or horse
            if getattr(self, "_race_mode", "horse") == "dog":
                _draw_dog_from_dict(self.screen, hx, hy + 4, h, scale=0.5, facing=1)
            else:
                draw_horse_traits(self.screen, hx, hy, h, W=_HORSE_W, H=_HORSE_H, facing=1)

            # Surge spark (in front of nose)
            if h["surge_timer"] > 0:
                nose_x = hx + _HORSE_W + 10
                pygame.draw.circle(self.screen, (255, 240, 100), (nose_x, hy + 9), 4)
                pygame.draw.circle(self.screen, (255, 190, 50),  (nose_x, hy + 9), 2)

            # Name label
            label = h["name"] if h.get("is_player") else f"{h['name']} ({h['owner']})"
            nc    = (255, 235, 130) if h.get("is_player") else (185, 170, 135)
            nl    = self.small.render(label, True, nc)
            self.screen.blit(nl, (hx, hy - 14))

            # Stamina bar
            sm_frac = max(0.0, h["stamina"] / 100.0)
            sm_col  = (90, 220, 90) if sm_frac > 0.5 else \
                      ((220, 200, 55) if sm_frac > 0.25 else (215, 75, 75))
            pygame.draw.rect(self.screen, (35, 28, 18), (hx, hy + 28, 60, 5), border_radius=2)
            pygame.draw.rect(self.screen, sm_col, (hx, hy + 28, int(sm_frac * 60), 5), border_radius=2)

        # ---- Standings sidebar (right column) ----
        sb_x  = px + pw - 165
        sb_y  = track_y
        sb_hdr = self.small.render("Standings", True, (170, 150, 90))
        self.screen.blit(sb_hdr, (sb_x, sb_y))
        place_cols = [(220, 175, 40), (185, 185, 195), (185, 115, 60)]
        for rank, h in enumerate(sorted_h):
            ry2   = sb_y + 18 + rank * 26
            pc    = place_cols[rank] if rank < 3 else (155, 140, 115)
            rk_t  = self.small.render(f"#{rank+1}", True, pc)
            self.screen.blit(rk_t, (sb_x, ry2))
            nm_c  = (255, 235, 130) if h.get("is_player") else (195, 180, 150)
            nm_t  = self.small.render(h["name"][:10], True, nm_c)
            self.screen.blit(nm_t, (sb_x + 26, ry2))
            # Style indicator dot
            if getattr(self, "_race_mode", "horse") == "dog":
                sdot_c = _DOG_STYLE_COLORS.get(h.get("style", "pacer"), (160, 160, 160))
            else:
                sdot_c = _STYLE_COLORS.get(h.get("style", "pacer"), (160, 160, 160))
            pygame.draw.circle(self.screen, sdot_c, (sb_x + 140, ry2 + 6), 4)

        # Commentary
        if self._race_commentary:
            msg, fade = self._race_commentary
            alpha  = min(255, int(fade * 255 / 2.0))
            c_surf = self.font.render(msg, True, (255, 220, 80))
            c_surf.set_alpha(alpha)
            self.screen.blit(c_surf, (px + pw // 2 - 90 - c_surf.get_width() // 2,
                                      py + ph - 80))
            self._race_commentary = (msg, fade - 0.016) if fade > 0.0 else None

        # Progress bar + timer
        prog  = min(1.0, self._race_time / _RACE_DURATION)
        bar_y = py + ph - 48
        pygame.draw.rect(self.screen, (35, 28, 18), (px + 20, bar_y, track_w, 10), border_radius=3)
        pygame.draw.rect(self.screen, (130, 175, 110), (px + 20, bar_y, int(prog * track_w), 10), border_radius=3)
        tt    = self.small.render(f"{max(0.0, _RACE_DURATION - self._race_time):.1f}s", True, (160, 145, 95))
        self.screen.blit(tt, (track_x + track_w - tt.get_width(), bar_y - 14))

    def _tick_race(self, dt, player):
        self._race_time += dt
        horses        = self._race_horses
        place_counter = [0]
        progress      = self._race_time / _RACE_DURATION

        for h in horses:
            if h["finished"]:
                continue

            sm_frac  = h["stamina"] / 100.0
            base     = h["race_rating"] * 0.80
            sm_bonus = 0.20 * sm_frac

            # Reaction boost (early race)
            react_mult = 1.0
            if progress < 0.20:
                react_mult = 0.85 + h["reaction"] * 0.15

            # Heart boost (low stamina)
            heart_mult = 1.0
            if sm_frac < 0.30:
                heart_mult = 0.75 + h["heart"] * 0.25

            # Racing style modifiers
            style_spd, style_drain = _style_modifiers(h, progress, dt)

            # Surge
            h["surge_timer"] = max(0.0, h["surge_timer"] - dt)
            surge_mult = 1.0
            if h["surge_timer"] > 0:
                surge_mult = 1.0 + _SURGE_BOOST
            else:
                # Wild cards surge twice as often
                chance = _SURGE_CHANCE * (2.0 if h.get("style") == "wild" else 1.0)
                if random.random() < chance * dt:
                    h["surge_timer"] = _SURGE_DURATION * (1.5 if h.get("style") == "wild" else 1.0)
                    surge_mult = 1.0 + _SURGE_BOOST

            speed = (base + sm_bonus) * react_mult * heart_mult * style_spd * surge_mult
            h["position"] = min(1.0, h["position"] + speed * _RACE_SPEED_SCALE * dt)

            drain = _STAMINA_DRAIN * dt * style_drain / max(0.5, h["endurance"] * (0.7 + h["agility"] * 0.3))
            h["stamina"] = max(0.0, h["stamina"] - drain)

            # Steeplechase jump checks
            if getattr(self, "_race_steeplechase", False):
                for jump_idx, jump_prog in enumerate([0.25, 0.55, 0.85]):
                    if not h["jumps_cleared"][jump_idx] and h["position"] >= jump_prog:
                        h["jumps_cleared"][jump_idx] = True
                        agility = h.get("agility", 1.0)
                        if random.random() > agility * 0.70:
                            h["position"] = max(0.0, h["position"] - 0.04)
                            h["stamina"]  = max(0.0, h["stamina"]  - 18.0)
                            self._race_jump_flashes[h["uid"]] = 0.6

            if h["position"] >= 1.0:
                h["finished"] = True
                place_counter[0] += 1
                h["place"] = place_counter[0]
                self._race_placements.append(h)

        # Commentary triggers
        sorted_h = sorted(horses, key=lambda x: x["position"], reverse=True)

        def _cmt(key, **kw):
            self._race_commentary = (_COMMENTARY[key].format(**kw), 2.5)
            self._race_commentary_triggers.add(key)

        leader = sorted_h[0]
        triggers = self._race_commentary_triggers

        if "start" not in triggers and progress < 0.06 and self._race_commentary is None:
            _cmt("start")

        if "early_lead" not in triggers and progress > 0.25:
            triggers.add("early_lead")
            gap = leader["position"] - (sorted_h[1]["position"] if len(sorted_h) > 1 else 0)
            if gap > 0.08:
                _cmt("early_lead", name=leader["name"], owner=leader["owner"])

        if "mid" not in triggers and progress > 0.50:
            triggers.add("mid")
            gap_top = leader["position"] - (sorted_h[1]["position"] if len(sorted_h) > 1 else 0)
            if leader["stamina"] < 35 and leader.get("style") != "closer":
                _cmt("fading", name=leader["name"], owner=leader["owner"])
            elif gap_top > 0.12:
                _cmt("pulling", name=leader["name"], owner=leader["owner"])
            else:
                closers_near = [h for h in sorted_h[:3] if h.get("style") == "closer"]
                if closers_near and closers_near[0]["position"] > sorted_h[0]["position"] * 0.92:
                    _cmt("closer_move", name=closers_near[0]["name"], owner=closers_near[0]["owner"])
                else:
                    _cmt("neck", name="", owner="")

        if "player_check" not in triggers and progress > 0.60:
            ph_rank = next((r for r, h in enumerate(sorted_h) if h.get("is_player")), None)
            if ph_rank is not None:
                if ph_rank == 0:
                    self._race_commentary = (_COMMENTARY["player_lead"], 2.0)
                elif ph_rank >= len(sorted_h) - 1:
                    self._race_commentary = (_COMMENTARY["player_trail"], 2.0)
            triggers.add("player_check")

        if "final" not in triggers and progress > 0.85:
            _cmt("final", name="", owner="")

        # End condition
        if self._race_placements or self._race_time >= _RACE_DURATION:
            unfinished = sorted([h for h in horses if not h["finished"]],
                                key=lambda x: x["position"], reverse=True)
            for h in unfinished:
                h["finished"] = True
                h["position"] = min(1.0, h["position"])
                place_counter[0] += 1
                h["place"] = place_counter[0]
                self._race_placements.append(h)

            self._race_finished = True
            winner = self._race_placements[0] if self._race_placements else sorted_h[0]

            if (len(self._race_placements) >= 2 and
                    abs(self._race_placements[0]["position"] - self._race_placements[1]["position"]) < 0.02):
                self._race_phase = "photo_finish"
                self._race_time  = 0.0
                self._race_commentary = (_COMMENTARY["photo"], 3.0)
            else:
                self._race_phase = "result"
                self._race_commentary = (
                    _COMMENTARY["finish"].format(name=winner["name"], owner=winner["owner"]), 3.0)
                if getattr(self, "_circuit_leg_active", False):
                    self._apply_circuit_leg_result(winner, player)
                else:
                    self._apply_race_result(winner, player)

            # Update session win records for NPC horses
            npc = self._race_bookkeeper
            if npc:
                for h in self._race_placements:
                    for hdef in npc._npc_horses:
                        if hdef["name"] == h["uid"]:
                            hdef["races"] = hdef.get("races", 0) + 1
                            if h["place"] == 1:
                                hdef["wins"] = hdef.get("wins", 0) + 1


    # ------------------------------------------------------------------
    # Phase: photo finish
    # ------------------------------------------------------------------

    def _draw_race_photo_finish(self, player, dt, px, py, pw, ph):
        self._race_time += dt
        t = self._race_time

        winner = self._race_placements[0] if self._race_placements else None
        runner = self._race_placements[1] if len(self._race_placements) > 1 else None

        lbl = self.font.render("PHOTO FINISH!", True, (255, 230, 60))
        self.screen.blit(lbl, (px + pw // 2 - lbl.get_width() // 2, py + 55))

        if winner:
            w1 = self.font.render(f"Winner: {winner['name']}", True, (120, 255, 120))
            self.screen.blit(w1, (px + pw // 2 - w1.get_width() // 2, py + 100))
            w2 = self.small.render(f"owned by  {winner['owner']}", True, (140, 210, 140))
            self.screen.blit(w2, (px + pw // 2 - w2.get_width() // 2, py + 122))
        if runner:
            r1 = self.small.render(f"2nd:  {runner['name']}  ({runner['owner']})", True, (185, 185, 195))
            self.screen.blit(r1, (px + pw // 2 - r1.get_width() // 2, py + 148))

        # Dramatic reveal of the two horses
        if winner:
            scale = min(1.0, t / 0.6)
            w_size = int(80 * scale)
            if w_size > 4:
                pygame.draw.ellipse(self.screen, winner["coat_color"],
                                    (px + pw // 2 - 100 - w_size // 2, py + 190, w_size, int(w_size * 0.6)))
        if runner:
            scale2 = min(1.0, max(0.0, (t - 0.3) / 0.6))
            r_size = int(70 * scale2)
            if r_size > 4:
                pygame.draw.ellipse(self.screen, runner["coat_color"],
                                    (px + pw // 2 + 20, py + 190, r_size, int(r_size * 0.6)))

        if t >= 2.5:
            if winner:
                if getattr(self, "_circuit_leg_active", False):
                    self._apply_circuit_leg_result(winner, player)
                elif getattr(self, "_race_mode", "horse") == "dog":
                    self._apply_dog_race_result(winner, player)
                else:
                    self._apply_race_result(winner, player)
            self._race_phase = "result"
            self._race_time  = 0.0

    # ------------------------------------------------------------------
    # Phase: result
    # ------------------------------------------------------------------

    def _draw_race_result(self, player, px, py, pw, ph):
        self._race_rects = {}

        title = self.font.render("Race Results", True, (230, 205, 130))
        self.screen.blit(title, (px + pw // 2 - title.get_width() // 2, py + 42))

        place_labels = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th"]
        place_colors = [(220, 175, 40), (185, 185, 195), (185, 115, 60),
                        (155, 138, 118), (138, 128, 108), (125, 115, 98), (115, 105, 90), (105, 96, 82)]
        for i, h in enumerate(self._race_placements[:8]):
            ry   = py + 74 + i * 30
            pc   = place_colors[i] if i < len(place_colors) else (150, 140, 120)
            style = h.get("style", "pacer")
            if getattr(self, "_race_mode", "horse") == "dog":
                sc = _DOG_STYLE_COLORS.get(style, (160, 160, 160))
            else:
                sc = _STYLE_COLORS.get(style, (160, 160, 160))

            # Place badge
            pl_t = self.small.render(f"{place_labels[i]}", True, pc)
            self.screen.blit(pl_t, (px + 40, ry))

            # Horse name + owner
            nm_c  = (255, 235, 130) if h.get("is_player") else (215, 200, 170)
            nm_t  = self.small.render(f"{h['name']}  ({h['owner']})", True, nm_c)
            self.screen.blit(nm_t, (px + 90, ry))

            # Style tag
            if getattr(self, "_race_mode", "horse") == "dog":
                sl_lbl = _DOG_STYLE_LABELS.get(style, style.title())
            else:
                sl_lbl = _STYLE_LABELS.get(style, style.title())
            st_t = self.small.render(f"[{sl_lbl}]", True, sc)
            self.screen.blit(st_t, (px + 360, ry))

            # "You" marker
            if h.get("is_player"):
                you_t = self.small.render("◀ You", True, (255, 235, 100))
                self.screen.blit(you_t, (px + 520, ry))

        # Result message
        col   = (100, 240, 110) if self._race_net_gold > 0 else \
                ((235, 95, 95) if self._race_net_gold < 0 else (215, 215, 110))
        res_t = self.font.render(self._race_result_msg, True, col)
        self.screen.blit(res_t, (px + pw // 2 - res_t.get_width() // 2, py + ph - 120))

        gold_t = self.small.render(f"Gold: {player.money}", True, (205, 182, 108))
        self.screen.blit(gold_t, (px + pw // 2 - gold_t.get_width() // 2, py + ph - 96))

        again_rect = pygame.Rect(px + pw // 2 - 135, py + ph - 68, 125, 36)
        pygame.draw.rect(self.screen, (45, 125, 55), again_rect, border_radius=5)
        pygame.draw.rect(self.screen, (155, 225, 145), again_rect, 1, border_radius=5)
        ag_t = self.font.render("Race Again", True, (240, 240, 210))
        self.screen.blit(ag_t, (again_rect.centerx - ag_t.get_width() // 2, again_rect.centery - ag_t.get_height() // 2))
        self._race_rects["again"] = again_rect

        leave_rect = pygame.Rect(px + pw // 2 + 10, py + ph - 68, 125, 36)
        pygame.draw.rect(self.screen, (78, 38, 38), leave_rect, border_radius=5)
        pygame.draw.rect(self.screen, (175, 115, 115), leave_rect, 1, border_radius=5)
        lv_t = self.font.render("Leave", True, (228, 188, 188))
        self.screen.blit(lv_t, (leave_rect.centerx - lv_t.get_width() // 2, leave_rect.centery - lv_t.get_height() // 2))
        self._race_rects["leave"] = leave_rect

    # ------------------------------------------------------------------
    # Apply race result
    # ------------------------------------------------------------------

    def _apply_race_result(self, winner, player):
        if player is None:
            return
        npc           = self._race_bookkeeper
        bet_horse_uid = self._race_bet_horse
        bet_amount    = self._race_bet_amount

        won_bet = winner and (winner["uid"] == bet_horse_uid)
        if won_bet:
            odds   = next((h["odds"] for h in self._race_horses if h["uid"] == bet_horse_uid), 2.0)
            payout = int(bet_amount * odds)
            self._race_net_gold = payout - bet_amount
            player.money += payout
            self._race_result_msg = f"You won! +{payout}g (bet on {winner['name']})"
        else:
            self._race_net_gold = -bet_amount
            bet_name = next((h["name"] for h in self._race_horses if h["uid"] == bet_horse_uid), "your pick")
            self._race_result_msg = f"{winner['name']} won. {bet_name} lost. -{bet_amount}g"

        player_place = None
        for h in self._race_placements:
            if h.get("is_player"):
                player_place = h["place"]
                break

        ph = self._race_player_horse
        if ph is not None and player_place is not None:
            uid = getattr(ph, "uid", "player")
            if uid not in player.horse_pbs or player_place < player.horse_pbs.get(uid, 99):
                player.horse_pbs[uid] = player_place

        if player_place is not None and player_place <= 3:
            if player_place == 1:
                player.races_won = getattr(player, "races_won", 0) + 1
                player.gold_won_racing = getattr(player, "gold_won_racing", 0) + max(0, self._race_net_gold)
                player._add_item("racing_trophy_1st")
            elif player_place == 2:
                player._add_item("racing_trophy_2nd")
            elif player_place == 3:
                player._add_item("racing_trophy_3rd")

            if npc:
                try:
                    from npc_dynasty import apply_racing_result as _dynasty_race
                    _dynasty_race(player, npc, player_place)
                except Exception:
                    pass

    # ------------------------------------------------------------------
    # Dog racing: field builder
    # ------------------------------------------------------------------

    def _build_dog_race_field(self, player):
        npc  = self._race_bookkeeper
        dogs = []

        pd = self._race_player_dog
        if pd is not None:
            pt    = pd.traits
            breed = pt.get("breed", "Unknown")
            name  = pt.get("dog_name") or breed
            _col_b = _TACK_BOOSTS.get(pt.get("equipped_collar"), {})
            _bli_b = _TACK_BOOSTS.get(pt.get("equipped_blinkers"), {})
            _tb    = pt.get("training_bonuses", {})
            _rr    = min(1.5, pd.race_rating + _col_b.get("race_rating", 0) + _tb.get("speed", 0) * 0.40)
            dogs.append({
                "uid":        getattr(pd, "uid", "player_dog"),
                "name":       name,
                "breed":      breed,
                "owner":      "You",
                "race_rating": _rr,
                "stamina":    100.0,
                "stamina_max": pt.get("endurance", 1.0),
                "endurance":   min(1.3, pt.get("endurance", 1.0) + _tb.get("endurance", 0)),
                "agility":     min(1.3, pt.get("agility", 1.0) + _tb.get("agility", 0)),
                "alertness":   min(1.3, pt.get("alertness", 1.0) + _tb.get("alertness", 0)),
                "prey_drive":  pt.get("prey_drive", 0.5),
                "sprint":      min(1.3, pt.get("sprint", 1.0) + _tb.get("sprint", 0)),
                "focus":       min(1.3, pt.get("focus", 1.0) + _bli_b.get("focus", 0) + _tb.get("focus", 0)),
                "coat_color":  pt.get("coat_color", (160, 100, 50)),
                "style":       pt.get("race_style", "pacer"),
                "wins":        getattr(player, "dog_races_won", 0),
                "races":       getattr(player, "dog_races_entered", 0),
                "is_player":   True,
                "position":    0.0,
                "place":       0,
                "surge_timer": 0.0,
                "finished":    False,
            })

        npc_dog_defs = npc._npc_dogs if npc else []
        self._resolve_owner_names(npc_dog_defs, player)

        for d in npc_dog_defs:
            dogs.append({
                "uid":        d["name"],
                "name":       d["name"],
                "breed":      d.get("breed", "Mixed"),
                "owner":      d.get("owner", "Local"),
                "race_rating": d["race_rating"],
                "stamina":    100.0,
                "stamina_max": d.get("endurance", 1.0),
                "endurance":   d.get("endurance", 1.0),
                "agility":     d.get("agility", 1.0),
                "alertness":   d.get("alertness", 1.0),
                "prey_drive":  d.get("prey_drive", 0.5),
                "sprint":      d.get("sprint", 1.0),
                "focus":       d.get("focus", 1.0),
                "coat_color":  d.get("coat_color", (140, 90, 40)),
                "style":       d.get("style", "pacer"),
                "wins":        d.get("wins", 0),
                "races":       d.get("races", 0),
                "is_player":   False,
                "position":    0.0,
                "place":       0,
                "surge_timer": 0.0,
                "finished":    False,
            })

        ratings = [d["race_rating"] for d in dogs]
        avg = sum(ratings) / max(len(ratings), 1)
        for d in dogs:
            ratio = avg / max(d["race_rating"], 0.01)
            d["odds"] = round(max(1.1, min(8.0, ratio * 1.6)), 1)

        return dogs

    # ------------------------------------------------------------------
    # Dog racing: roster
    # ------------------------------------------------------------------

    def _draw_dog_race_roster(self, player, px, py, pw, ph):
        self._race_rects = {}
        npc = self._race_bookkeeper
        if not self._race_horses:
            self._race_horses = self._build_dog_race_field(player)

        fee   = npc.entry_fee(player) if npc else 50
        champ = npc.is_champion_ring() if npc else False
        ring_lbl = self.small.render(
            ("Champion Ring" if champ else "Racing Ring") + f"  —  Dog Entry: {fee}g",
            True, (200, 175, 110))
        self.screen.blit(ring_lbl, (px + pw // 2 - ring_lbl.get_width() // 2, py + 38))

        # Steeplechase toggle (shared state with horse roster)
        sc = getattr(self, "_race_steeplechase", False)
        for tog_lbl, tog_val, tog_x in [("Flat Race", False, px + pw // 2 - 115), ("Steeplechase", True, px + pw // 2 + 5)]:
            tr = pygame.Rect(tog_x, py + 54, 110, 22)
            sel = (sc == tog_val)
            pygame.draw.rect(self.screen, (55, 130, 60) if sel else (40, 40, 40), tr, border_radius=3)
            pygame.draw.rect(self.screen, (180, 230, 150) if sel else (70, 70, 70), tr, 1, border_radius=3)
            tt = self.small.render(tog_lbl, True, (230, 225, 200))
            self.screen.blit(tt, (tr.centerx - tt.get_width() // 2, tr.centery - tt.get_height() // 2))
            self._race_rects[("steeplechase_toggle", tog_val)] = tr

        headers = [("Dog & Owner", px + 50), ("Breed", px + 240),
                   ("Style", px + 370), ("Form", px + 490), ("Speed", px + 610)]
        hdr_y = py + 82
        for txt, cx in headers:
            ht = self.small.render(txt, True, (160, 140, 80))
            self.screen.blit(ht, (cx, hdr_y))

        row_h = 42
        list_y = py + 82
        for i, d in enumerate(self._race_horses):
            ry    = list_y + i * row_h
            rect  = pygame.Rect(px + 30, ry, pw - 60, row_h - 4)
            bg    = (58, 45, 28) if d.get("is_player") else (50, 38, 23)
            pygame.draw.rect(self.screen, bg, rect, border_radius=4)
            if d.get("is_player"):
                pygame.draw.rect(self.screen, (200, 170, 80), rect, 1, border_radius=4)

            # Coat swatch
            pygame.draw.rect(self.screen, d["coat_color"], (rect.x + 6, ry + 14, 10, 10), border_radius=2)

            # Name
            nc = (255, 235, 130) if d.get("is_player") else (215, 200, 170)
            nt = self.small.render(d["name"], True, nc)
            self.screen.blit(nt, (rect.x + 22, ry + 5))
            ot = self.small.render(d["owner"], True, (140, 120, 80))
            self.screen.blit(ot, (rect.x + 22, ry + 21))

            # Breed
            bt = self.small.render(d.get("breed", ""), True, (160, 145, 110))
            self.screen.blit(bt, (px + 240, ry + 13))

            # Style tag
            style  = d.get("style", "pacer")
            sc     = _DOG_STYLE_COLORS.get(style, (160, 160, 160))
            sl_lbl = _DOG_STYLE_LABELS.get(style, style.title())
            st_s   = self.small.render(f"[{sl_lbl}]", True, sc)
            self.screen.blit(st_s, (px + 370, ry + 13))

            # Form W/R
            form_t = self.small.render(f"{d['wins']}/{d['races']}", True, (170, 155, 110))
            self.screen.blit(form_t, (px + 490, ry + 13))

            # Speed bar
            bar_w  = int(d["race_rating"] * 60)
            pygame.draw.rect(self.screen, (40, 32, 20),    (px + 610, ry + 15, 60, 8), border_radius=2)
            pygame.draw.rect(self.screen, (110, 195, 125), (px + 610, ry + 15, bar_w, 8), border_radius=2)

            # Inspect rect
            self._race_rects[("inspect", d["uid"])] = rect

        # Enter / close buttons
        max_ry = list_y + len(self._race_horses) * row_h + 8
        has_dog = self._race_player_dog is not None
        can_afford = player.money >= fee
        can_enter  = has_dog and can_afford
        enter_col  = (45, 125, 55) if can_enter else (45, 45, 45)
        enter_rect = pygame.Rect(px + pw // 2 - 130, max(py + ph - 80, max_ry), 120, 36)
        pygame.draw.rect(self.screen, enter_col, enter_rect, border_radius=5)
        pygame.draw.rect(self.screen, (155, 225, 145), enter_rect, 1, border_radius=5)
        en_t = self.font.render("Enter Race", True, (240, 240, 210) if can_enter else (120, 120, 120))
        self.screen.blit(en_t, (enter_rect.centerx - en_t.get_width() // 2, enter_rect.centery - en_t.get_height() // 2))
        self._race_rects["enter"] = enter_rect

        if not has_dog:
            hint = self.small.render("Bring a tamed dog (not on stay) to enter.", True, (195, 135, 80))
            self.screen.blit(hint, (px + pw // 2 - hint.get_width() // 2, enter_rect.bottom + 6))

        close_rect = pygame.Rect(px + pw // 2 + 10, enter_rect.y, 120, 36)
        pygame.draw.rect(self.screen, (78, 38, 38), close_rect, border_radius=5)
        pygame.draw.rect(self.screen, (175, 115, 115), close_rect, 1, border_radius=5)
        cl_t = self.font.render("Leave", True, (228, 188, 188))
        self.screen.blit(cl_t, (close_rect.centerx - cl_t.get_width() // 2, close_rect.centery - cl_t.get_height() // 2))
        self._race_rects["close"] = close_rect

    # ------------------------------------------------------------------
    # Dog racing: inspect
    # ------------------------------------------------------------------

    def _draw_dog_race_inspect(self, player, px, py, pw, ph):
        self._race_rects = {}
        uid = self._race_inspect_uid
        dog = next((d for d in self._race_horses if d["uid"] == uid), None)
        if not dog:
            self._race_phase = "roster"
            return

        style  = dog.get("style", "pacer")
        sc     = _DOG_STYLE_COLORS.get(style, (160, 160, 160))
        sl_lbl = _DOG_STYLE_LABELS.get(style, style.title())

        # Header
        nc   = (255, 235, 130) if dog.get("is_player") else (215, 200, 170)
        nm_t = self.font.render(dog["name"], True, nc)
        self.screen.blit(nm_t, (px + 60, py + 44))
        br_t = self.small.render(f"{dog.get('breed','')}  ·  owned by {dog['owner']}", True, (155, 135, 90))
        self.screen.blit(br_t, (px + 60, py + 68))
        st_t = self.font.render(f"[{sl_lbl}]", True, sc)
        self.screen.blit(st_t, (px + pw - 200, py + 52))

        # Style description
        desc_t = self.small.render(_DOG_STYLE_DESC.get(style, ""), True, (175, 160, 120))
        self.screen.blit(desc_t, (px + 60, py + 92))
        tip_t  = self.small.render(_DOG_STYLE_TIP.get(style, ""), True, (140, 130, 95))
        self.screen.blit(tip_t, (px + 60, py + 110))

        # Stat bars
        def _bar(label, value, y, lo=0.7, hi=1.3):
            lb_t = self.small.render(label, True, (160, 145, 105))
            self.screen.blit(lb_t, (px + 60, y))
            frac = max(0.0, min(1.0, (value - lo) / (hi - lo)))
            bx   = px + 165
            pygame.draw.rect(self.screen, (40, 32, 20), (bx, y + 2, 120, 10), border_radius=3)
            col  = (90, 200, 100) if frac > 0.6 else ((210, 195, 55) if frac > 0.35 else (205, 75, 75))
            pygame.draw.rect(self.screen, col, (bx, y + 2, int(frac * 120), 10), border_radius=3)
            vt   = self.small.render(f"{value:.2f}", True, (200, 185, 145))
            self.screen.blit(vt, (bx + 128, y))

        sy = py + 136
        _bar("Speed",      dog["race_rating"], sy);      sy += 22
        _bar("Endurance",  dog["endurance"],   sy);      sy += 22
        _bar("Agility",    dog["agility"],     sy);      sy += 22
        _bar("Alertness",  dog["alertness"],   sy);      sy += 22
        _bar("Prey Drive", dog["prey_drive"],  sy, 0, 1); sy += 22
        _bar("Sprint",     dog["sprint"],      sy);      sy += 22
        _bar("Focus",      dog["focus"],       sy);      sy += 22

        # Career record
        form_t = self.small.render(f"Career: {dog['wins']}W / {dog['races']}R    Odds: {dog['odds']}x payout",
                                   True, (170, 155, 110))
        self.screen.blit(form_t, (px + 60, sy + 8))

        # Buttons
        npc = self._race_bookkeeper
        fee = npc.entry_fee(player) if npc else 50
        has_dog   = self._race_player_dog is not None
        can_enter = has_dog and player.money >= fee

        enter_rect = pygame.Rect(px + pw // 2 - 140, py + ph - 72, 120, 36)
        ec = (45, 125, 55) if can_enter else (45, 45, 45)
        pygame.draw.rect(self.screen, ec, enter_rect, border_radius=5)
        pygame.draw.rect(self.screen, (155, 225, 145), enter_rect, 1, border_radius=5)
        en_t = self.font.render("Enter Race", True, (240, 240, 210) if can_enter else (120, 120, 120))
        self.screen.blit(en_t, (enter_rect.centerx - en_t.get_width() // 2, enter_rect.centery - en_t.get_height() // 2))
        self._race_rects["enter"] = enter_rect

        back_rect = pygame.Rect(px + pw // 2 + 10, py + ph - 72, 120, 36)
        pygame.draw.rect(self.screen, (65, 32, 32), back_rect, border_radius=5)
        pygame.draw.rect(self.screen, (150, 100, 100), back_rect, 1, border_radius=5)
        bk_t = self.font.render("Back", True, (200, 165, 165))
        self.screen.blit(bk_t, (back_rect.centerx - bk_t.get_width() // 2, back_rect.centery - bk_t.get_height() // 2))
        self._race_rects["back_from_inspect"] = back_rect

    # ------------------------------------------------------------------
    # Dog racing: bet
    # ------------------------------------------------------------------

    def _draw_dog_race_bet(self, player, px, py, pw, ph):
        self._race_rects = {}
        bl = self.font.render("Pick a dog to bet on:", True, (210, 185, 120))
        self.screen.blit(bl, (px + pw // 2 - bl.get_width() // 2, py + 44))

        hy     = py + 76
        row_h  = 42
        for d in self._race_horses:
            ry   = hy
            sel  = (self._race_bet_horse == d["uid"])
            rect = pygame.Rect(px + 40, ry, pw - 80, row_h - 4)
            bg   = (60, 110, 65) if sel else ((58, 45, 28) if d.get("is_player") else (50, 38, 23))
            pygame.draw.rect(self.screen, bg, rect, border_radius=4)
            pygame.draw.rect(self.screen, (180, 230, 160) if sel else (90, 80, 55), rect, 1, border_radius=4)

            pygame.draw.rect(self.screen, d["coat_color"], (rect.x + 6, ry + 15, 10, 10), border_radius=2)

            nc   = (255, 235, 130) if d.get("is_player") else (215, 200, 170)
            nt   = self.small.render(d["name"], True, nc)
            self.screen.blit(nt, (rect.x + 24, ry + 2))
            bt   = self.small.render(d.get("breed", ""), True, (160, 145, 110))
            self.screen.blit(bt, (rect.x + 24, ry + 18))

            style  = d.get("style", "pacer")
            sc     = _DOG_STYLE_COLORS.get(style, (160, 160, 160))
            sl_lbl = _DOG_STYLE_LABELS.get(style, style.title())
            st_s   = self.small.render(f"[{sl_lbl}]", True, sc)
            self.screen.blit(st_s, (rect.x + 160, ry + 10))

            ot = self.small.render(f"{d['owner']}", True, (140, 120, 80))
            self.screen.blit(ot, (rect.x + 290, ry + 10))

            odds_t = self.small.render(f"{d['odds']}x payout", True, (210, 185, 100))
            self.screen.blit(odds_t, (rect.right - odds_t.get_width() - 10, ry + 10))

            self._race_rects[("pick_horse", d["uid"])] = rect
            hy += row_h

        # Bet amount
        bet_y = hy + 10
        bl2   = self.small.render("Bet amount:", True, (160, 145, 90))
        self.screen.blit(bl2, (px + 30, bet_y))
        btn_w, btn_h = 82, 30
        for j, amt in enumerate(_BET_OPTIONS):
            bx    = px + 30 + j * (btn_w + 8)
            brect = pygame.Rect(bx, bet_y + 20, btn_w, btn_h)
            sel   = (self._race_bet_amount == amt)
            aff   = (player.money >= amt)
            bc    = (55, 140, 70) if sel else ((38, 85, 50) if aff else (45, 45, 45))
            pygame.draw.rect(self.screen, bc, brect, border_radius=4)
            pygame.draw.rect(self.screen, (180, 230, 160) if sel else (85, 120, 85), brect, 1, border_radius=4)
            at = self.small.render(f"{amt}g", True, (240, 230, 180) if aff else (110, 110, 110))
            self.screen.blit(at, (brect.centerx - at.get_width() // 2, brect.centery - at.get_height() // 2))
            self._race_rects[("bet_amt", amt)] = brect

        can_go  = (self._race_bet_horse is not None) and (player.money >= self._race_bet_amount)
        go_rect = pygame.Rect(px + pw // 2 - 70, py + ph - 80, 140, 38)
        pygame.draw.rect(self.screen, (55, 150, 55) if can_go else (45, 45, 45), go_rect, border_radius=5)
        pygame.draw.rect(self.screen, (180, 240, 150), go_rect, 1, border_radius=5)
        go_t = self.font.render("To the Gates!", True, (245, 240, 210) if can_go else (120, 120, 120))
        self.screen.blit(go_t, (go_rect.centerx - go_t.get_width() // 2, go_rect.centery - go_t.get_height() // 2))
        self._race_rects["go"] = go_rect

        back_rect = pygame.Rect(px + pw // 2 - 50, py + ph - 38, 100, 26)
        pygame.draw.rect(self.screen, (65, 32, 32), back_rect, border_radius=4)
        pygame.draw.rect(self.screen, (150, 100, 100), back_rect, 1, border_radius=4)
        bk_t = self.small.render("Back", True, (200, 165, 165))
        self.screen.blit(bk_t, (back_rect.centerx - bk_t.get_width() // 2, back_rect.centery - bk_t.get_height() // 2))
        self._race_rects["back"] = back_rect

    # ------------------------------------------------------------------
    # Dog racing: simulation tick
    # ------------------------------------------------------------------

    def _tick_dog_race(self, dt, player):
        self._race_time += dt
        dogs          = self._race_horses
        place_counter = [0]
        progress      = self._race_time / _RACE_DURATION

        sorted_d  = sorted(dogs, key=lambda x: x["position"], reverse=True)
        leader_pos = sorted_d[0]["position"] if sorted_d else 0.0

        for d in dogs:
            if d["finished"]:
                continue

            sm_frac = d["stamina"] / 100.0
            base    = d["race_rating"] * 0.78
            sm_bonus = 0.22 * sm_frac

            # Alertness = start reaction
            alert_mult = 1.0
            if progress < 0.20:
                alert_mult = 0.85 + d.get("alertness", 1.0) * 0.15

            # Prey drive = late-race drive when tired
            drive_mult = 1.0
            if sm_frac < 0.30:
                drive_mult = 0.75 + d.get("prey_drive", 0.5) * 0.25

            style_spd, style_drain = _dog_style_modifiers(d, progress, leader_pos)

            # Focus wobble — high focus = steadier line
            focus  = d.get("focus", 1.0)
            wobble = random.uniform(-0.015, 0.015) * (1.3 / max(0.7, focus))

            # Surge system
            d["surge_timer"] = max(0.0, d["surge_timer"] - dt)
            surge_mult = 1.0
            if d["surge_timer"] > 0:
                surge_mult = 1.0 + _SURGE_BOOST
            else:
                prey_drive = d.get("prey_drive", 0.5)
                if d.get("style") == "surger":
                    chance = 0.05 + prey_drive * 0.06
                else:
                    chance = _SURGE_CHANCE * 0.6
                if random.random() < chance * dt:
                    d["surge_timer"] = _SURGE_DURATION
                    surge_mult = 1.0 + _SURGE_BOOST

            speed = max(0.0, (base + sm_bonus + wobble) * alert_mult * drive_mult * style_spd * surge_mult)
            d["position"] = min(1.0, d["position"] + speed * _RACE_SPEED_SCALE * dt)

            drain = _STAMINA_DRAIN * dt * style_drain / max(0.5, d["endurance"] * (0.7 + d["agility"] * 0.3))
            d["stamina"] = max(0.0, d["stamina"] - drain)

            # Steeplechase jump checks
            if getattr(self, "_race_steeplechase", False):
                for jump_idx, jump_prog in enumerate([0.25, 0.55, 0.85]):
                    if not d["jumps_cleared"][jump_idx] and d["position"] >= jump_prog:
                        d["jumps_cleared"][jump_idx] = True
                        agility = d.get("agility", 1.0)
                        if random.random() > agility * 0.70:
                            d["position"] = max(0.0, d["position"] - 0.04)
                            d["stamina"]  = max(0.0, d["stamina"]  - 18.0)
                            self._race_jump_flashes[d["uid"]] = 0.6

            if d["position"] >= 1.0:
                d["finished"] = True
                place_counter[0] += 1
                d["place"] = place_counter[0]
                self._race_placements.append(d)

        # Commentary
        sorted_d = sorted(dogs, key=lambda x: x["position"], reverse=True)

        def _cmt(key, **kw):
            msg = _COMMENTARY.get(key, "")
            if not msg:
                return
            self._race_commentary = (msg.format(**kw), 2.5)
            self._race_commentary_triggers.add(key)

        leader   = sorted_d[0] if sorted_d else None
        triggers = self._race_commentary_triggers

        if leader and "start" not in triggers and progress < 0.06:
            _cmt("start")
        if leader and "early_lead" not in triggers and progress > 0.25:
            triggers.add("early_lead")
            gap = leader["position"] - (sorted_d[1]["position"] if len(sorted_d) > 1 else 0)
            if gap > 0.08:
                _cmt("early_lead", name=leader["name"], owner=leader["owner"])
        if "mid" not in triggers and progress > 0.50:
            triggers.add("mid")
            if leader and leader["stamina"] < 35 and leader.get("style") != "chaser":
                _cmt("fading", name=leader["name"], owner=leader["owner"])
            else:
                _cmt("neck", name="", owner="")
        if "player_check" not in triggers and progress > 0.60:
            ph_rank = next((r for r, d in enumerate(sorted_d) if d.get("is_player")), None)
            if ph_rank is not None:
                if ph_rank == 0:
                    self._race_commentary = (_DOG_COMMENTARY_PLAYER_LEAD, 2.0)
                elif ph_rank >= len(sorted_d) - 1:
                    self._race_commentary = (_DOG_COMMENTARY_PLAYER_TRAIL, 2.0)
            triggers.add("player_check")
        if "final" not in triggers and progress > 0.85:
            _cmt("final", name="", owner="")

        # End condition
        if self._race_placements or self._race_time >= _RACE_DURATION:
            unfinished = sorted([d for d in dogs if not d["finished"]],
                                key=lambda x: x["position"], reverse=True)
            for d in unfinished:
                d["finished"] = True
                d["position"] = min(1.0, d["position"])
                place_counter[0] += 1
                d["place"] = place_counter[0]
                self._race_placements.append(d)

            self._race_finished = True
            winner = self._race_placements[0] if self._race_placements else sorted_d[0]

            if (len(self._race_placements) >= 2 and
                    abs(self._race_placements[0]["position"] - self._race_placements[1]["position"]) < 0.02):
                self._race_phase = "photo_finish"
                self._race_time  = 0.0
                self._race_commentary = (_COMMENTARY["photo"], 3.0)
            else:
                self._race_phase = "result"
                self._race_commentary = (
                    _COMMENTARY["finish"].format(name=winner["name"], owner=winner["owner"]), 3.0)
                if getattr(self, "_circuit_leg_active", False):
                    self._apply_circuit_leg_result(winner, player)
                else:
                    self._apply_dog_race_result(winner, player)

            npc = self._race_bookkeeper
            if npc:
                for d in self._race_placements:
                    for ddef in npc._npc_dogs:
                        if ddef["name"] == d["uid"]:
                            ddef["races"] = ddef.get("races", 0) + 1
                            if d["place"] == 1:
                                ddef["wins"] = ddef.get("wins", 0) + 1

    # ------------------------------------------------------------------
    # Dog racing: apply result
    # ------------------------------------------------------------------

    def _apply_dog_race_result(self, winner, player):
        if player is None:
            return
        bet_horse_uid = self._race_bet_horse
        bet_amount    = self._race_bet_amount

        won_bet = winner and (winner["uid"] == bet_horse_uid)
        if won_bet:
            odds   = next((d["odds"] for d in self._race_horses if d["uid"] == bet_horse_uid), 2.0)
            payout = int(bet_amount * odds)
            self._race_net_gold = payout - bet_amount
            player.money += payout
            self._race_result_msg = f"You won! +{payout}g (bet on {winner['name']})"
        else:
            self._race_net_gold = -bet_amount
            bet_name = next((d["name"] for d in self._race_horses if d["uid"] == bet_horse_uid), "your pick")
            self._race_result_msg = f"{winner['name']} won. {bet_name} lost. -{bet_amount}g"

        player_place = None
        for d in self._race_placements:
            if d.get("is_player"):
                player_place = d["place"]
                break

        pd = self._race_player_dog
        if pd is not None and player_place is not None:
            uid = getattr(pd, "uid", "player_dog")
            pbs = getattr(player, "dog_race_pbs", {})
            if uid not in pbs or player_place < pbs.get(uid, 99):
                pbs[uid] = player_place
                player.dog_race_pbs = pbs

        if player_place is not None:
            player.dog_races_entered = getattr(player, "dog_races_entered", 0) + 1
            if player_place == 1:
                player.dog_races_won = getattr(player, "dog_races_won", 0) + 1
                player.gold_won_dog_racing = getattr(player, "gold_won_dog_racing", 0) + max(0, self._race_net_gold)
                player._add_item("dog_racing_trophy_1st")
            elif player_place == 2:
                player._add_item("dog_racing_trophy_2nd")
            elif player_place == 3:
                player._add_item("dog_racing_trophy_3rd")

    # ------------------------------------------------------------------
    # Circuit: constants helpers
    # ------------------------------------------------------------------

    _CIRCUIT_TIERS = {
        1: {"name": "Local Circuit",            "stops": 3, "entry_fee": 100,  "prize": 1500,  "req": 0},
        2: {"name": "Regional Circuit",         "stops": 4, "entry_fee": 300,  "prize": 5000,  "req": 1},
        3: {"name": "National Circuit",         "stops": 5, "entry_fee": 800,  "prize": 15000, "req": 2},
        4: {"name": "International Grand Prix", "stops": 6, "entry_fee": 2000, "prize": 50000, "req": 3},
    }
    _CIRCUIT_TIER_KEY = {1:"local", 2:"regional", 3:"national", 4:"international"}
    _POINTS_TABLE = {1:10, 2:8, 3:6, 4:5, 5:4, 6:3, 7:2, 8:1}

    def _circuit_at_current_leg(self, player):
        """Return True if this bookkeeper's city matches the active circuit's current leg."""
        ac = getattr(player, "active_circuit", None)
        if not ac or ac["current_leg"] >= len(ac["legs"]):
            return False
        leg      = ac["legs"][ac["current_leg"]]
        bkp      = self._race_bookkeeper
        if bkp is None:
            return False
        from constants import BLOCK_SIZE as _BS
        bkp_bx = int(getattr(bkp, "x", 0) // _BS)
        return abs(bkp_bx - leg["center_bx"]) <= 60

    def _circuit_leg_total_cost(self, player):
        ac = getattr(player, "active_circuit", None)
        return ac["entry_fee_per_leg"] if ac else 0

    # ------------------------------------------------------------------
    # Circuit: menu screen
    # ------------------------------------------------------------------

    def _draw_circuit_menu(self, player, px, py, pw, ph):
        self._race_rects = {}
        ac         = getattr(player, "active_circuit", None)
        by_tier    = getattr(player, "circuits_completed_by_tier", {1:0,2:0,3:0,4:0})
        tier_key   = self._CIRCUIT_TIER_KEY

        if ac is None:
            # --- Registration view ---
            hdr = self.font.render("Circuit Racing", True, (230, 205, 130))
            self.screen.blit(hdr, (px + pw // 2 - hdr.get_width() // 2, py + 42))
            sub = self.small.render("Register for a multi-city racing series.", True, (160, 145, 100))
            self.screen.blit(sub, (px + pw // 2 - sub.get_width() // 2, py + 66))

            # Mode toggle
            mode = getattr(self, "_circuit_reg_mode", "horse")
            tog_y = py + 90
            for m, lbl, cx in [("horse", "Horse", px + pw // 2 - 80), ("dog", "Dog", px + pw // 2 + 10)]:
                tr = pygame.Rect(cx, tog_y, 70, 24)
                sel = (mode == m)
                pygame.draw.rect(self.screen, (55, 130, 60) if sel else (45, 45, 45), tr, border_radius=4)
                pygame.draw.rect(self.screen, (180, 230, 150) if sel else (80, 80, 80), tr, 1, border_radius=4)
                tt = self.small.render(lbl, True, (230, 230, 200))
                self.screen.blit(tt, (tr.centerx - tt.get_width() // 2, tr.centery - tt.get_height() // 2))
                self._race_rects[("circuit_mode_toggle", m)] = tr

            # Tier buttons
            tier_y = py + 126
            for tier, cfg in self._CIRCUIT_TIERS.items():
                completed = by_tier.get(tier, by_tier.get(str(tier), 0))
                required  = cfg["req"]
                tier_total= sum(by_tier.get(t, by_tier.get(str(t), 0)) for t in range(1, tier))
                unlocked  = (tier == 1) or (tier_total >= required)
                selected  = (getattr(self, "_circuit_reg_tier", 1) == tier)

                r = pygame.Rect(px + 30, tier_y, pw - 60, 48)
                bg = (65, 50, 30) if selected else ((45, 38, 26) if unlocked else (30, 28, 26))
                pygame.draw.rect(self.screen, bg, r, border_radius=5)
                pygame.draw.rect(self.screen, (200, 165, 80) if selected else ((110, 90, 55) if unlocked else (55, 52, 48)),
                                 r, 1, border_radius=5)

                tier_col = (230, 200, 130) if unlocked else (90, 85, 75)
                nt = self.font.render(cfg["name"], True, tier_col)
                self.screen.blit(nt, (r.x + 14, tier_y + 6))
                details = f"{cfg['stops']} stops · {cfg['entry_fee']}g/leg · Prize: {cfg['prize']:,}g"
                if not unlocked:
                    details = f"LOCKED — complete {required} lower circuit(s) first"
                dt = self.small.render(details, True, (155, 138, 100) if unlocked else (80, 75, 65))
                self.screen.blit(dt, (r.x + 14, tier_y + 28))
                if completed:
                    ct = self.small.render(f"×{completed} completed", True, (120, 200, 120))
                    self.screen.blit(ct, (r.right - ct.get_width() - 12, tier_y + 16))
                if unlocked:
                    self._race_rects[("circuit_tier_select", tier)] = r

                tier_y += 56

            # Register button
            sel_tier  = getattr(self, "_circuit_reg_tier", 1)
            sel_cfg   = self._CIRCUIT_TIERS[sel_tier]
            sel_total = sel_cfg["entry_fee"] * sel_cfg["stops"]
            can_reg   = player.money >= sel_total
            reg_rect  = pygame.Rect(px + pw // 2 - 110, py + ph - 72, 220, 42)
            rc = (50, 130, 55) if can_reg else (40, 40, 40)
            pygame.draw.rect(self.screen, rc, reg_rect, border_radius=6)
            pygame.draw.rect(self.screen, (180, 240, 150), reg_rect, 1, border_radius=6)
            reg_lbl = f"Register  ({sel_total:,}g total)"
            rt = self.font.render(reg_lbl, True, (245, 240, 210) if can_reg else (110, 110, 110))
            self.screen.blit(rt, (reg_rect.centerx - rt.get_width() // 2, reg_rect.centery - rt.get_height() // 2))
            self._race_rects["circuit_register"] = reg_rect

        else:
            # --- Active circuit view ---
            hdr = self.font.render(ac["name"], True, (230, 205, 130))
            self.screen.blit(hdr, (px + pw // 2 - hdr.get_width() // 2, py + 42))
            mode_t = self.small.render(f"{ac['mode'].title()} Circuit  ·  {ac['entry_fee_per_leg']}g per leg", True, (160, 145, 100))
            self.screen.blit(mode_t, (px + pw // 2 - mode_t.get_width() // 2, py + 66))

            # Points so far
            total_pts = sum(lg["points"] for lg in ac["legs"])
            max_pts   = sum(self._POINTS_TABLE.get(1, 10) for _ in ac["legs"])
            pts_t = self.font.render(f"Points: {total_pts} / {max_pts}", True, (210, 195, 120))
            self.screen.blit(pts_t, (px + pw // 2 - pts_t.get_width() // 2, py + 90))

            # Current leg info
            cur   = ac["current_leg"]
            legs  = ac["legs"]
            if cur < len(legs):
                leg = legs[cur]
                leg_t = self.font.render(f"Next: Leg {cur+1} at {leg['city_name']}", True, (200, 185, 130))
                self.screen.blit(leg_t, (px + pw // 2 - leg_t.get_width() // 2, py + 118))
                from constants import BLOCK_SIZE as _BS
                bkp = self._race_bookkeeper
                bkp_bx = int(getattr(bkp, "x", 0) // _BS) if bkp else 0
                dist_bk = abs(bkp_bx - leg["center_bx"])
                if dist_bk > 60:
                    dist_t = self.small.render(f"Travel ~{dist_bk} blocks to reach this city", True, (175, 145, 90))
                    self.screen.blit(dist_t, (px + pw // 2 - dist_t.get_width() // 2, py + 142))

            # Buttons row
            btn_y = py + ph - 82
            at_leg = self._circuit_at_current_leg(player)
            fee    = ac["entry_fee_per_leg"]
            can_race = at_leg and player.money >= fee

            race_rect = pygame.Rect(px + 40, btn_y, 160, 40)
            rc2 = (50, 130, 55) if can_race else (38, 38, 38)
            pygame.draw.rect(self.screen, rc2, race_rect, border_radius=5)
            pygame.draw.rect(self.screen, (180, 240, 150), race_rect, 1, border_radius=5)
            rl = self.font.render(f"Race Leg {cur+1}  ({fee}g)", True, (245,240,210) if can_race else (100,100,100))
            self.screen.blit(rl, (race_rect.centerx - rl.get_width() // 2, race_rect.centery - rl.get_height() // 2))
            self._race_rects["circuit_race_leg"] = race_rect

            legs_rect = pygame.Rect(px + 220, btn_y, 130, 40)
            pygame.draw.rect(self.screen, (50, 55, 90), legs_rect, border_radius=5)
            pygame.draw.rect(self.screen, (140, 155, 210), legs_rect, 1, border_radius=5)
            lgt = self.font.render("View Legs", True, (210, 215, 240))
            self.screen.blit(lgt, (legs_rect.centerx - lgt.get_width() // 2, legs_rect.centery - lgt.get_height() // 2))
            self._race_rects["circuit_view_legs"] = legs_rect

            aband_rect = pygame.Rect(px + 370, btn_y, 120, 40)
            pygame.draw.rect(self.screen, (90, 35, 35), aband_rect, border_radius=5)
            pygame.draw.rect(self.screen, (180, 100, 100), aband_rect, 1, border_radius=5)
            at = self.small.render("Abandon", True, (220, 165, 165))
            self.screen.blit(at, (aband_rect.centerx - at.get_width() // 2, aband_rect.centery - at.get_height() // 2))
            self._race_rects["circuit_abandon"] = aband_rect

        # Back button
        back_rect = pygame.Rect(px + pw - 110, py + ph - 40, 100, 30)
        pygame.draw.rect(self.screen, (65, 32, 32), back_rect, border_radius=4)
        pygame.draw.rect(self.screen, (150, 100, 100), back_rect, 1, border_radius=4)
        bk_t = self.small.render("Back", True, (200, 165, 165))
        self.screen.blit(bk_t, (back_rect.centerx - bk_t.get_width() // 2, back_rect.centery - bk_t.get_height() // 2))
        self._race_rects["back_to_choose"] = back_rect

    # ------------------------------------------------------------------
    # Circuit: legs list screen
    # ------------------------------------------------------------------

    def _draw_circuit_legs(self, player, px, py, pw, ph):
        self._race_rects = {}
        ac = getattr(player, "active_circuit", None)
        if not ac:
            self._race_phase = "circuit_menu"
            return

        hdr = self.font.render(ac["name"] + " — Route", True, (230, 205, 130))
        self.screen.blit(hdr, (px + pw // 2 - hdr.get_width() // 2, py + 42))

        from constants import BLOCK_SIZE as _BS
        bkp    = self._race_bookkeeper
        bkp_bx = int(getattr(bkp, "x", 0) // _BS) if bkp else 0

        leg_y = py + 76
        for i, leg in enumerate(ac["legs"]):
            done    = leg["completed"]
            current = (i == ac["current_leg"] and not done)
            r = pygame.Rect(px + 30, leg_y, pw - 60, 40)
            bg = (50, 70, 40) if done else ((60, 50, 28) if current else (40, 36, 24))
            pygame.draw.rect(self.screen, bg, r, border_radius=4)
            pygame.draw.rect(self.screen, (140, 200, 110) if done else ((200, 175, 80) if current else (80, 72, 50)),
                             r, 1, border_radius=4)

            # Status icon
            icon = "✓" if done else ("▶" if current else "·")
            ic = (140, 210, 120) if done else ((240, 215, 90) if current else (120, 110, 80))
            it = self.font.render(icon, True, ic)
            self.screen.blit(it, (r.x + 10, leg_y + 9))

            # City name + leg number
            nc = (230, 220, 180) if (done or current) else (160, 148, 115)
            nt = self.font.render(f"Leg {i+1}: {leg['city_name']}", True, nc)
            self.screen.blit(nt, (r.x + 38, leg_y + 8))

            # Distance (if upcoming)
            if not done:
                dist = abs(bkp_bx - leg["center_bx"])
                dt = self.small.render(f"~{dist} blocks away", True, (140, 128, 88))
                self.screen.blit(dt, (r.right - dt.get_width() - 10, leg_y + 13))
            else:
                # Placement + points
                place_labels = ["—","1st","2nd","3rd","4th","5th","6th","7th","8th"]
                place_idx = min(leg["placement"] or 0, len(place_labels) - 1)
                pt = self.small.render(f"{place_labels[place_idx]}  +{leg['points']}pts", True, (160, 200, 140))
                self.screen.blit(pt, (r.right - pt.get_width() - 10, leg_y + 13))

            leg_y += 48

        # Points summary
        total_pts = sum(lg["points"] for lg in ac["legs"])
        max_pts   = len(ac["legs"]) * 10
        ps = self.font.render(f"Total: {total_pts} / {max_pts} points", True, (200, 190, 130))
        self.screen.blit(ps, (px + pw // 2 - ps.get_width() // 2, leg_y + 8))

        back_rect = pygame.Rect(px + pw // 2 - 55, py + ph - 46, 110, 34)
        pygame.draw.rect(self.screen, (65, 32, 32), back_rect, border_radius=5)
        pygame.draw.rect(self.screen, (150, 100, 100), back_rect, 1, border_radius=5)
        bk_t = self.font.render("Back", True, (200, 165, 165))
        self.screen.blit(bk_t, (back_rect.centerx - bk_t.get_width() // 2, back_rect.centery - bk_t.get_height() // 2))
        self._race_rects["back_to_circuit_menu"] = back_rect

    # ------------------------------------------------------------------
    # Circuit: leg result application
    # ------------------------------------------------------------------

    def _apply_circuit_leg_result(self, winner, player):
        if player is None:
            return
        ac = getattr(player, "active_circuit", None)
        if not ac:
            return

        cur_leg_idx = ac["current_leg"]
        leg         = ac["legs"][cur_leg_idx]

        # Find player placement
        player_place = None
        for h in self._race_placements:
            if h.get("is_player"):
                player_place = h["place"]
                break

        leg["completed"] = True
        leg["placement"] = player_place
        leg["points"]    = self._POINTS_TABLE.get(player_place, 0) if player_place else 0

        # Betting payout (same as regular race)
        bet_uid = self._race_bet_horse
        bet_amt = self._race_bet_amount
        won_bet = winner and (winner["uid"] == bet_uid)
        if won_bet:
            odds   = next((h["odds"] for h in self._race_horses if h["uid"] == bet_uid), 2.0)
            payout = int(bet_amt * odds)
            self._race_net_gold = payout - bet_amt
            player.money += payout
        else:
            self._race_net_gold = -bet_amt

        ac["current_leg"] += 1

        if ac["current_leg"] >= len(ac["legs"]):
            # Circuit complete — go to result phase
            self._race_phase = "circuit_result"
            self._circuit_leg_active = False
        else:
            self._race_phase = "result"
            next_leg = ac["legs"][ac["current_leg"]]
            self._race_result_msg = (
                f"Leg {cur_leg_idx+1} done! +{leg['points']}pts  "
                f"→ Next: {next_leg['city_name']}"
            )

    # ------------------------------------------------------------------
    # Circuit: final result screen
    # ------------------------------------------------------------------

    def _draw_circuit_result(self, player, px, py, pw, ph):
        self._race_rects = {}
        ac = getattr(player, "active_circuit", None)
        if not ac:
            self._race_phase = "choose"
            return

        total_pts = sum(lg["points"] for lg in ac["legs"])
        max_pts   = len(ac["legs"]) * 10
        pct = total_pts / max_pts if max_pts else 0

        tier     = ac["tier"]
        tier_key = self._CIRCUIT_TIER_KEY.get(tier, "local")

        if pct >= 0.85:
            grade, trophy_id, grade_col = "Gold", f"circuit_trophy_{tier_key}_gold", (255, 215, 0)
            prize = ac["grand_prize_gold"]
        elif pct >= 0.65:
            grade, trophy_id, grade_col = "Silver", f"circuit_trophy_{tier_key}_silver", (210, 210, 220)
            prize = int(ac["grand_prize_gold"] * 0.6)
        elif pct >= 0.40:
            grade, trophy_id, grade_col = "Bronze", f"circuit_trophy_{tier_key}_bronze", (195, 130, 65)
            prize = int(ac["grand_prize_gold"] * 0.25)
        else:
            grade, trophy_id, grade_col = "Participation", None, (130, 120, 100)
            prize = 0

        # Apply prizes (only once — check flag)
        if not ac.get("_prizes_applied"):
            ac["_prizes_applied"] = True
            if prize:
                player.money += prize
            if trophy_id:
                player._add_item(trophy_id)
            # Record completion
            cbt = getattr(player, "circuits_completed_by_tier", {1:0,2:0,3:0,4:0})
            cbt[tier] = cbt.get(tier, 0) + 1
            player.circuits_completed_by_tier = cbt
            completed = getattr(player, "completed_circuits", [])
            completed.append({
                "name": ac["name"], "tier": tier, "grade": grade,
                "points": total_pts, "max_points": max_pts, "prize": prize,
            })
            player.completed_circuits = completed

        hdr = self.font.render("Circuit Complete!", True, (230, 205, 130))
        self.screen.blit(hdr, (px + pw // 2 - hdr.get_width() // 2, py + 42))

        name_t = self.font.render(ac["name"], True, (200, 185, 140))
        self.screen.blit(name_t, (px + pw // 2 - name_t.get_width() // 2, py + 66))

        grade_t = self.font.render(grade + " Finish", True, grade_col)
        self.screen.blit(grade_t, (px + pw // 2 - grade_t.get_width() // 2, py + 96))

        pts_t = self.small.render(f"{total_pts} points out of {max_pts}", True, (185, 175, 130))
        self.screen.blit(pts_t, (px + pw // 2 - pts_t.get_width() // 2, py + 122))

        # Leg breakdown
        leg_y = py + 150
        place_labels = ["—","1st","2nd","3rd","4th","5th","6th","7th","8th"]
        for i, leg in enumerate(ac["legs"]):
            pl = min(leg.get("placement") or 0, len(place_labels)-1)
            row = f"Leg {i+1} · {leg['city_name'][:18]:<18}  {place_labels[pl]}  +{leg['points']}pts"
            rt = self.small.render(row, True, (165, 152, 115))
            self.screen.blit(rt, (px + 60, leg_y))
            leg_y += 20

        if prize:
            prize_t = self.font.render(f"+{prize:,}g prize money!", True, (130, 230, 110))
            self.screen.blit(prize_t, (px + pw // 2 - prize_t.get_width() // 2, leg_y + 10))

        # Clear active circuit and close buttons
        done_rect = pygame.Rect(px + pw // 2 - 55, py + ph - 58, 110, 38)
        pygame.draw.rect(self.screen, (45, 125, 55), done_rect, border_radius=5)
        pygame.draw.rect(self.screen, (155, 225, 145), done_rect, 1, border_radius=5)
        dn_t = self.font.render("Done", True, (240, 240, 210))
        self.screen.blit(dn_t, (done_rect.centerx - dn_t.get_width() // 2, done_rect.centery - dn_t.get_height() // 2))
        self._race_rects["circuit_done"] = done_rect

    # ------------------------------------------------------------------
    # Choose mode screen
    # ------------------------------------------------------------------

    def _draw_race_choose(self, player, px, py, pw, ph):
        self._race_rects = {}

        lbl = self.font.render("Welcome to the Racing Ring", True, (220, 200, 130))
        self.screen.blit(lbl, (px + pw // 2 - lbl.get_width() // 2, py + 60))
        sub = self.small.render("Choose your race type:", True, (170, 155, 110))
        self.screen.blit(sub, (px + pw // 2 - sub.get_width() // 2, py + 88))

        has_horse = self._race_player_horse is not None
        has_dog   = self._race_player_dog is not None

        btn_w, btn_h = 185, 70
        gap    = 20
        row_y  = py + 120
        total_w = btn_w * 3 + gap * 2
        bx = px + pw // 2 - total_w // 2

        def _btn(rect, enabled, label, sub_label, base_col, border_col):
            bg = base_col if enabled else (40, 40, 40)
            bc = border_col if enabled else (70, 70, 70)
            pygame.draw.rect(self.screen, bg, rect, border_radius=6)
            pygame.draw.rect(self.screen, bc, rect, 1, border_radius=6)
            lt = self.font.render(label, True, (240, 230, 200) if enabled else (100, 100, 100))
            self.screen.blit(lt, (rect.centerx - lt.get_width() // 2, rect.y + 14))
            if sub_label:
                st = self.small.render(sub_label, True, (170, 150, 110) if enabled else (80, 80, 80))
                self.screen.blit(st, (rect.centerx - st.get_width() // 2, rect.y + 40))

        # Horse Racing
        horse_rect = pygame.Rect(bx, row_y, btn_w, btn_h)
        horse_sub = "Tamed horse needed" if not has_horse else "Enter a horse race"
        _btn(horse_rect, has_horse, "Horse Racing", horse_sub, (45, 100, 60), (180, 230, 150))
        self._race_rects["horse_mode"] = horse_rect

        # Dog Racing
        dog_rect = pygame.Rect(bx + btn_w + gap, row_y, btn_w, btn_h)
        dog_sub = "Following dog needed" if not has_dog else "Enter a dog race"
        _btn(dog_rect, has_dog, "Dog Racing", dog_sub, (60, 90, 140), (150, 185, 230))
        self._race_rects["dog_mode"] = dog_rect

        # Circuit Racing
        circ_rect = pygame.Rect(bx + (btn_w + gap) * 2, row_y, btn_w, btn_h)
        ac = getattr(player, "active_circuit", None)
        circ_sub = f"Leg {ac['current_leg']+1}/{len(ac['legs'])}" if ac else "Multi-city series"
        _btn(circ_rect, True, "Circuit Racing", circ_sub, (100, 65, 140), (185, 145, 230))
        self._race_rects["circuit_mode"] = circ_rect

        # Recent circuit completions badge
        by_tier = getattr(player, "circuits_completed_by_tier", {})
        tier_names = {1:"Local", 2:"Regional", 3:"National", 4:"Intl"}
        badges = [f"{tier_names[t]}×{n}" for t, n in sorted(by_tier.items()) if n > 0]
        if badges:
            badge_t = self.small.render("Completed: " + "  ".join(badges), True, (185, 165, 100))
            self.screen.blit(badge_t, (px + pw // 2 - badge_t.get_width() // 2, row_y + btn_h + 14))

        # Watch & Bet (spectator) button + Tack Shop button
        row2_y = row_y + btn_h + 32
        watch_rect = pygame.Rect(px + pw // 2 - 175, row2_y, 160, 38)
        _btn(watch_rect, True, "Watch & Bet", "No horse/dog needed", (70, 55, 90), (165, 135, 200))
        self._race_rects["spectator_mode"] = watch_rect

        tack_rect = pygame.Rect(px + pw // 2 + 15, row2_y, 160, 38)
        _btn(tack_rect, True, "Tack Shop", "Equip gear for races", (75, 55, 35), (180, 140, 80))
        self._race_rects["tack_shop_mode"] = tack_rect

        close_rect = pygame.Rect(px + pw // 2 - 55, py + ph - 52, 110, 34)
        pygame.draw.rect(self.screen, (78, 38, 38), close_rect, border_radius=5)
        pygame.draw.rect(self.screen, (175, 115, 115), close_rect, 1, border_radius=5)
        cl_t = self.font.render("Leave", True, (228, 188, 188))
        self.screen.blit(cl_t, (close_rect.centerx - cl_t.get_width() // 2, close_rect.centery - cl_t.get_height() // 2))
        self._race_rects["close"] = close_rect

    # ------------------------------------------------------------------
    # Spectator mode field builder
    # ------------------------------------------------------------------

    def _build_spectator_field(self, player):
        """Build an NPC-only field (no player horse/dog)."""
        mode = getattr(self, "_race_mode", "horse")
        npc  = self._race_bookkeeper
        entries = []
        npc_defs = (npc._npc_horses if mode == "horse" else npc._npc_dogs) if npc else []
        self._resolve_owner_names(list(npc_defs), player)
        for h in npc_defs:
            if mode == "horse":
                entries.append({
                    "uid": h["name"], "name": h["name"], "owner": h.get("owner","Local"),
                    "race_rating": h["race_rating"], "stamina": 100.0,
                    "stamina_max": h.get("stamina_max",1.0), "endurance": h.get("endurance",1.0),
                    "reaction": h.get("reaction",1.0), "agility": h.get("agility",1.0),
                    "heart": h.get("heart",1.0), "coat_color": h.get("coat_color",(140,100,60)),
                    "coat_pattern": h.get("coat_pattern","solid"), "leg_marking": h.get("leg_marking","none"),
                    "mane_color": h.get("mane_color","match"), "face_marking": h.get("face_marking","none"),
                    "temperament": h.get("temperament","spirited"), "color_shift": (0,0,0), "size": 1.0,
                    "style": h.get("style","pacer"), "wins": h.get("wins",0), "races": h.get("races",0),
                    "is_player": False, "position": 0.0, "place": 0, "surge_timer": 0.0, "finished": False,
                    "jumps_cleared": [False, False, False],
                })
            else:
                entries.append({
                    "uid": h["name"], "name": h["name"], "breed": h.get("breed","Mixed"),
                    "owner": h.get("owner","Local"), "race_rating": h["race_rating"], "stamina": 100.0,
                    "stamina_max": h.get("endurance",1.0), "endurance": h.get("endurance",1.0),
                    "agility": h.get("agility",1.0), "alertness": h.get("alertness",1.0),
                    "prey_drive": h.get("prey_drive",0.5), "sprint": h.get("sprint",1.0), "focus": h.get("focus",1.0),
                    "coat_color": h.get("coat_color",(140,90,40)),
                    "coat_pattern": h.get("coat_pattern","solid"), "white_spotting": h.get("white_spotting","solid"),
                    "coat_length": h.get("coat_length","short"), "coat_type": h.get("coat_type","smooth"),
                    "ear_type": h.get("ear_type","floppy"), "tail_type": h.get("tail_type","long"),
                    "eye_color": h.get("eye_color","brown"), "size_class": h.get("size_class","medium"),
                    "style": h.get("style","pacer"), "wins": h.get("wins",0), "races": h.get("races",0),
                    "is_player": False, "position": 0.0, "place": 0, "surge_timer": 0.0, "finished": False,
                    "jumps_cleared": [False, False, False],
                })
        ratings = [e["race_rating"] for e in entries]
        avg = sum(ratings) / max(len(ratings), 1)
        for e in entries:
            ratio = avg / max(e["race_rating"], 0.01)
            e["odds"] = round(max(1.1, min(8.0, ratio * 1.6)), 1)
        return entries

    # ------------------------------------------------------------------
    # Tack shop draw
    # ------------------------------------------------------------------

    def _draw_tack_shop(self, player, px, py, pw, ph):
        self._race_rects = {}
        hdr = self.font.render("Tack Shop", True, (230, 200, 130))
        self.screen.blit(hdr, (px + pw // 2 - hdr.get_width() // 2, py + 42))

        npc = self._race_bookkeeper
        shop = npc.tack_shop if npc else []

        # Current equipment display
        horse = self._race_player_horse
        dog   = self._race_player_dog
        eq_y  = py + 68
        if horse:
            hn = getattr(horse, "name", "Horse")
            saddle = horse.traits.get("equipped_saddle") or "None"
            shoe   = horse.traits.get("equipped_horseshoe") or "None"
            ht = self.small.render(f"Horse ({hn}):  Saddle: {saddle}  ·  Horseshoe: {shoe}", True, (180, 165, 115))
            self.screen.blit(ht, (px + 30, eq_y))
            eq_y += 18
        if dog:
            dn = dog.traits.get("dog_name") or dog.traits.get("breed", "Dog")
            col  = dog.traits.get("equipped_collar") or "None"
            bli  = dog.traits.get("equipped_blinkers") or "None"
            dt = self.small.render(f"Dog ({dn}):  Collar: {col}  ·  Blinkers: {bli}", True, (180, 165, 115))
            self.screen.blit(dt, (px + 30, eq_y))
            eq_y += 18

        # Shop items
        from items import ITEMS as _ITEMS
        row_y = eq_y + 10
        for (item_id, cost, display, _, _b) in shop:
            info = _ITEMS.get(item_id, {})
            tack_type = info.get("tack_type", "")
            boost = _TACK_BOOSTS.get(item_id, {})
            boost_str = "  ".join(f"+{v} {k.replace('_',' ')}" for k, v in boost.items())
            is_horse = tack_type.startswith("horse")
            is_dog   = tack_type.startswith("dog")
            can_buy  = player.money >= cost

            r = pygame.Rect(px + 30, row_y, pw - 60, 34)
            pygame.draw.rect(self.screen, (46, 36, 22), r, border_radius=4)
            pygame.draw.rect(self.screen, (110, 88, 50), r, 1, border_radius=4)

            col_c = (200, 185, 140)
            name_t = self.small.render(display, True, col_c)
            self.screen.blit(name_t, (r.x + 10, row_y + 9))
            boost_t = self.small.render(boost_str, True, (130, 200, 130))
            self.screen.blit(boost_t, (r.x + 170, row_y + 9))
            cost_t = self.small.render(f"{cost}g", True, (210, 190, 130) if can_buy else (110, 100, 80))
            self.screen.blit(cost_t, (r.x + 370, row_y + 9))

            if is_horse and horse and can_buy:
                btn = pygame.Rect(r.right - 130, row_y + 5, 125, 24)
                pygame.draw.rect(self.screen, (55, 110, 60), btn, border_radius=3)
                pygame.draw.rect(self.screen, (155, 220, 145), btn, 1, border_radius=3)
                bt = self.small.render("Equip on Horse", True, (235, 235, 210))
                self.screen.blit(bt, (btn.centerx - bt.get_width() // 2, btn.centery - bt.get_height() // 2))
                self._race_rects[("tack_buy_horse", item_id, cost)] = btn
            elif is_dog and dog and can_buy:
                btn = pygame.Rect(r.right - 125, row_y + 5, 120, 24)
                pygame.draw.rect(self.screen, (55, 80, 130), btn, border_radius=3)
                pygame.draw.rect(self.screen, (140, 165, 220), btn, 1, border_radius=3)
                bt = self.small.render("Equip on Dog", True, (235, 235, 210))
                self.screen.blit(bt, (btn.centerx - bt.get_width() // 2, btn.centery - bt.get_height() // 2))
                self._race_rects[("tack_buy_dog", item_id, cost)] = btn

            row_y += 40

        gold_t = self.small.render(f"Gold: {player.money}g", True, (200, 185, 120))
        self.screen.blit(gold_t, (px + 30, py + ph - 48))

        back_rect = pygame.Rect(px + pw - 115, py + ph - 46, 105, 34)
        pygame.draw.rect(self.screen, (65, 32, 32), back_rect, border_radius=5)
        pygame.draw.rect(self.screen, (150, 100, 100), back_rect, 1, border_radius=5)
        bk_t = self.font.render("Back", True, (200, 165, 165))
        self.screen.blit(bk_t, (back_rect.centerx - bk_t.get_width() // 2, back_rect.centery - bk_t.get_height() // 2))
        self._race_rects["back_to_choose"] = back_rect

    # ------------------------------------------------------------------
    # Training paddock — open / draw / click
    # ------------------------------------------------------------------

    def open_training_paddock(self, player, world):
        self.training_paddock_open = True
        self._paddock_world        = world
        self._paddock_sel_animal   = "horse"
        self._paddock_sel_stat     = "speed"
        self._paddock_sel_duration = 3
        self._paddock_rects        = {}

    def _draw_training_paddock(self, player, dt):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))

        sw, sh = self.screen.get_size()
        pw, ph = 660, 460
        px = (sw - pw) // 2
        py = (sh - ph) // 2

        pygame.draw.rect(self.screen, (38, 28, 16), (px, py, pw, ph), border_radius=8)
        pygame.draw.rect(self.screen, (155, 120, 60), (px, py, pw, ph), 1, border_radius=8)

        hdr = self.font.render("Training Paddock", True, (230, 200, 130))
        self.screen.blit(hdr, (px + pw // 2 - hdr.get_width() // 2, py + 14))

        self._paddock_rects = {}
        world  = self._paddock_world
        horse  = self._find_player_horse(player) if world else None
        dog    = self._find_player_dog(player) if world else None
        sel_an = getattr(self, "_paddock_sel_animal", "horse")
        sel_st = getattr(self, "_paddock_sel_stat", "speed")
        sel_du = getattr(self, "_paddock_sel_duration", 3)

        # Animal selector
        an_y = py + 50
        for an_lbl, an_val in [("Horse", "horse"), ("Dog", "dog")]:
            has = (horse is not None) if an_val == "horse" else (dog is not None)
            ar  = pygame.Rect(px + 30 + (an_val == "dog") * 160, an_y, 150, 30)
            sel = (sel_an == an_val)
            pygame.draw.rect(self.screen, (55, 130, 60) if (sel and has) else ((40,40,40) if not has else (42,38,28)), ar, border_radius=4)
            pygame.draw.rect(self.screen, (180, 230, 150) if (sel and has) else (70,70,70), ar, 1, border_radius=4)
            at = self.font.render(an_lbl, True, (235, 230, 210) if has else (100, 100, 100))
            self.screen.blit(at, (ar.centerx - at.get_width() // 2, ar.centery - at.get_height() // 2))
            if has:
                self._paddock_rects[("animal", an_val)] = ar

        # Show current animal info
        target = horse if sel_an == "horse" else dog
        an_y2 = an_y + 38
        if target:
            an_name = (getattr(target, "name", None) or
                       target.traits.get("dog_name") or
                       target.traits.get("breed", "Unknown"))
            tb = target.traits.get("training_bonuses", {})
            info_t = self.small.render(
                f"{an_name}  ·  Training bonuses: " +
                ("  ".join(f"{k.title()} +{v:.3f}" for k, v in tb.items()) or "None"),
                True, (175, 160, 115))
            self.screen.blit(info_t, (px + 30, an_y2))

        # Stat selector
        st_y = an_y2 + 30
        stats = ["speed", "endurance", "agility", "alertness"] if sel_an == "dog" else ["speed", "endurance", "agility", "reaction"]
        for i, stat in enumerate(stats):
            sr = pygame.Rect(px + 30 + i * 148, st_y, 140, 28)
            sel2 = (sel_st == stat)
            pygame.draw.rect(self.screen, (55, 90, 130) if sel2 else (38, 35, 26), sr, border_radius=4)
            pygame.draw.rect(self.screen, (140, 175, 220) if sel2 else (70, 65, 50), sr, 1, border_radius=4)
            st_t = self.small.render(stat.title(), True, (225, 220, 200))
            self.screen.blit(st_t, (sr.centerx - st_t.get_width() // 2, sr.centery - st_t.get_height() // 2))
            self._paddock_rects[("stat", stat)] = sr

        # Duration selector
        _DURATIONS = [(1, 50, 0.02), (3, 120, 0.05), (7, 250, 0.10)]
        dur_y = st_y + 42
        dur_lbl = self.small.render("Training duration:", True, (160, 145, 105))
        self.screen.blit(dur_lbl, (px + 30, dur_y))
        for i, (days, cost, boost) in enumerate(_DURATIONS):
            dr = pygame.Rect(px + 30 + i * 195, dur_y + 22, 185, 34)
            sel3 = (sel_du == days)
            can  = player.money >= cost
            pygame.draw.rect(self.screen, (70, 50, 28) if sel3 else ((40,40,40) if not can else (38,35,26)), dr, border_radius=4)
            pygame.draw.rect(self.screen, (200, 170, 90) if sel3 else ((70,70,70) if not can else (90,80,55)), dr, 1, border_radius=4)
            dl = self.small.render(f"{days} day{'s' if days>1 else ''}  ·  {cost}g  ·  +{boost:.0%}", True,
                                   (230, 220, 185) if can else (100, 100, 100))
            self.screen.blit(dl, (dr.centerx - dl.get_width() // 2, dr.centery - dl.get_height() // 2))
            if can:
                self._paddock_rects[("duration", days, cost, boost)] = dr

        # Active sessions
        sess = getattr(player, "training_sessions", [])
        sess_y = dur_y + 68
        sess_hdr = self.small.render("Active sessions:", True, (160, 145, 105))
        self.screen.blit(sess_hdr, (px + 30, sess_y))
        for i, s in enumerate(sess[:4]):
            sl = self.small.render(
                f"{s['stat'].title()}  ({s['days_remaining']}d left)  ·  {s.get('animal_type','').title()} uid:{s['uid'][:6]}",
                True, (175, 165, 130))
            self.screen.blit(sl, (px + 30, sess_y + 18 + i * 18))

        # Cap notice
        cap_t = self.small.render("Max bonus: +0.15 per stat", True, (130, 120, 90))
        self.screen.blit(cap_t, (px + pw - cap_t.get_width() - 20, py + ph - 54))

        # Start Training button
        can_start = (target is not None and player.money >= dict(zip(
            [d for d,_,_ in _DURATIONS], [c for _,c,_ in _DURATIONS])).get(sel_du, 999))
        start_rect = pygame.Rect(px + pw // 2 - 90, py + ph - 52, 180, 38)
        pygame.draw.rect(self.screen, (50, 130, 55) if can_start else (40, 40, 40), start_rect, border_radius=5)
        pygame.draw.rect(self.screen, (165, 235, 155), start_rect, 1, border_radius=5)
        st2 = self.font.render("Start Training", True, (245, 240, 215) if can_start else (110, 110, 110))
        self.screen.blit(st2, (start_rect.centerx - st2.get_width() // 2, start_rect.centery - st2.get_height() // 2))
        self._paddock_rects["start"] = start_rect

        # Close button
        cl_rect = pygame.Rect(px + pw - 108, py + ph - 42, 100, 30)
        pygame.draw.rect(self.screen, (65, 32, 32), cl_rect, border_radius=4)
        pygame.draw.rect(self.screen, (150, 100, 100), cl_rect, 1, border_radius=4)
        clt = self.small.render("Close", True, (200, 165, 165))
        self.screen.blit(clt, (cl_rect.centerx - clt.get_width() // 2, cl_rect.centery - clt.get_height() // 2))
        self._paddock_rects["close"] = cl_rect

    def handle_training_paddock_click(self, pos, player, world):
        _DURATIONS = {1: (50, 0.02), 3: (120, 0.05), 7: (250, 0.10)}
        horse = self._find_player_horse(player)
        dog   = self._find_player_dog(player)
        for key, rect in self._paddock_rects.items():
            if not rect.collidepoint(pos):
                continue
            if isinstance(key, tuple):
                if key[0] == "animal":
                    self._paddock_sel_animal = key[1]
                elif key[0] == "stat":
                    self._paddock_sel_stat = key[1]
                elif key[0] == "duration":
                    self._paddock_sel_duration = key[1]
            elif key == "start":
                sel_an = getattr(self, "_paddock_sel_animal", "horse")
                sel_st = getattr(self, "_paddock_sel_stat", "speed")
                sel_du = getattr(self, "_paddock_sel_duration", 3)
                target = horse if sel_an == "horse" else dog
                dur_cfg = _DURATIONS.get(sel_du)
                if target and dur_cfg:
                    cost, boost_per_day = dur_cfg
                    if player.money >= cost:
                        player.money -= cost
                        sessions = getattr(player, "training_sessions", [])
                        sessions.append({
                            "uid":          getattr(target, "uid", "?"),
                            "animal_type":  sel_an,
                            "stat":         sel_st,
                            "days_remaining": sel_du,
                            "days_total":   sel_du,
                            "boost_per_day": boost_per_day / sel_du,
                        })
                        player.training_sessions = sessions
                        player.pending_notifications.append(
                            ("Training", f"Training started! {sel_st.title()} training for {sel_du} day(s).", None)
                        )
            elif key == "close":
                self.training_paddock_open = False
            break

    # ------------------------------------------------------------------
    # Input handlers
    # ------------------------------------------------------------------

    def handle_racing_click(self, pos, player):
        phase = self._race_phase
        mode  = getattr(self, "_race_mode", "horse")
        for key, rect in self._race_rects.items():
            if not rect.collidepoint(pos):
                continue
            if phase == "choose":
                if key == "horse_mode" and self._race_player_horse is not None:
                    self._race_mode  = "horse"
                    self._race_phase = "roster"
                    self._race_horses = []
                elif key == "dog_mode" and self._race_player_dog is not None:
                    self._race_mode  = "dog"
                    self._race_phase = "roster"
                    self._race_horses = []
                elif key == "circuit_mode":
                    self._race_phase = "circuit_menu"
                elif key == "spectator_mode":
                    self._race_mode  = getattr(self, "_race_mode", "horse")
                    self._race_phase = "roster"
                    self._race_horses = self._build_spectator_field(player)
                elif key == "tack_shop_mode":
                    self._race_phase = "tack_shop"
                elif key == "close":
                    self.racing_open = False
            elif phase == "tack_shop":
                if isinstance(key, tuple):
                    if key[0] == "tack_buy_horse":
                        item_id, cost = key[1], key[2]
                        horse = self._race_player_horse
                        if horse and player.money >= cost:
                            from items import ITEMS as _ITEMS
                            info = _ITEMS.get(item_id, {})
                            tack_type = info.get("tack_type", "")
                            player.money -= cost
                            slot = "equipped_saddle" if "saddle" in tack_type else "equipped_horseshoe"
                            old = horse.traits.get(slot)
                            if old:
                                player._add_item(old)
                            horse.traits[slot] = item_id
                    elif key[0] == "tack_buy_dog":
                        item_id, cost = key[1], key[2]
                        dog = self._race_player_dog
                        if dog and player.money >= cost:
                            from items import ITEMS as _ITEMS
                            info = _ITEMS.get(item_id, {})
                            tack_type = info.get("tack_type", "")
                            player.money -= cost
                            slot = "equipped_collar" if "collar" in tack_type else "equipped_blinkers"
                            old = dog.traits.get(slot)
                            if old:
                                player._add_item(old)
                            dog.traits[slot] = item_id
                elif key == "back_to_choose":
                    self._race_phase = "choose"
            elif phase == "circuit_menu":
                if isinstance(key, tuple):
                    if key[0] == "circuit_tier_select":
                        self._circuit_reg_tier = key[1]
                    elif key[0] == "circuit_mode_toggle":
                        self._circuit_reg_mode = key[1]
                elif key == "circuit_register":
                    npc    = self._race_bookkeeper
                    world  = getattr(player, "world", None)
                    tier   = getattr(self, "_circuit_reg_tier", 1)
                    cfg    = self._CIRCUIT_TIERS[tier]
                    total  = cfg["entry_fee"] * cfg["stops"]
                    mode   = getattr(self, "_circuit_reg_mode", "horse")
                    by_tier = getattr(player, "circuits_completed_by_tier", {1:0,2:0,3:0,4:0})
                    tier_total = sum(by_tier.get(t, by_tier.get(str(t), 0)) for t in range(1, tier))
                    unlocked = (tier == 1) or (tier_total >= cfg["req"])
                    if unlocked and player.money >= total and npc and world:
                        player.money -= total
                        player.active_circuit = npc._generate_circuit(
                            tier, mode, player.x, world)
                elif key == "circuit_race_leg":
                    ac  = getattr(player, "active_circuit", None)
                    fee = ac["entry_fee_per_leg"] if ac else 0
                    if ac and self._circuit_at_current_leg(player) and player.money >= fee:
                        player.money -= fee
                        leg = ac["legs"][ac["current_leg"]]
                        self._race_mode   = ac["mode"]
                        self._race_horses = []
                        self._circuit_leg_active = True
                        # Build field: circuit NPC field + player racer
                        if ac["mode"] == "horse":
                            ph = self._find_player_horse(player)
                            self._race_player_horse = ph
                            npc_field = leg["npc_field"]
                            # Rebuild with player horse + leg NPC field directly
                            horses = self._build_race_field(player)
                            # Replace NPC entries with the circuit leg's field
                            player_entry = next((h for h in horses if h.get("is_player")), None)
                            self._race_horses = []
                            if player_entry:
                                self._race_horses.append(player_entry)
                            for h in npc_field:
                                self._race_horses.append({
                                    "uid": h["name"], "name": h["name"], "owner": h.get("owner","Local"),
                                    "race_rating": h["race_rating"], "stamina": 100.0,
                                    "stamina_max": h.get("stamina_max", 1.0), "endurance": h.get("endurance", 1.0),
                                    "reaction": h.get("reaction", 1.0), "agility": h.get("agility", 1.0),
                                    "heart": h.get("heart", 1.0), "coat_color": h.get("coat_color", (140,100,60)),
                                    "coat_pattern": h.get("coat_pattern","solid"), "leg_marking": h.get("leg_marking","none"),
                                    "mane_color": h.get("mane_color","match"), "face_marking": h.get("face_marking","none"),
                                    "temperament": h.get("temperament","spirited"), "color_shift": (0,0,0), "size": 1.0,
                                    "style": h.get("style","pacer"), "wins": h.get("wins",0), "races": h.get("races",0),
                                    "is_player": False, "position": 0.0, "place": 0, "surge_timer": 0.0, "finished": False,
                                })
                        else:
                            pd = self._find_player_dog(player)
                            self._race_player_dog = pd
                            npc_field = leg["npc_field"]
                            player_entry = self._build_dog_race_field(player)
                            p_dog = next((d for d in player_entry if d.get("is_player")), None)
                            self._race_horses = []
                            if p_dog:
                                self._race_horses.append(p_dog)
                            for d in npc_field:
                                self._race_horses.append({
                                    "uid": d["name"], "name": d["name"], "breed": d.get("breed","Mixed"),
                                    "owner": d.get("owner","Local"), "race_rating": d["race_rating"],
                                    "stamina": 100.0, "stamina_max": d.get("endurance",1.0),
                                    "endurance": d.get("endurance",1.0), "agility": d.get("agility",1.0),
                                    "alertness": d.get("alertness",1.0), "prey_drive": d.get("prey_drive",0.5),
                                    "sprint": d.get("sprint",1.0), "focus": d.get("focus",1.0),
                                    "coat_color": d.get("coat_color",(140,90,40)),
                                    "coat_pattern": d.get("coat_pattern","solid"),
                                    "white_spotting": d.get("white_spotting","solid"),
                                    "coat_length": d.get("coat_length","short"),
                                    "coat_type": d.get("coat_type","smooth"),
                                    "ear_type": d.get("ear_type","floppy"),
                                    "tail_type": d.get("tail_type","long"),
                                    "eye_color": d.get("eye_color","brown"),
                                    "size_class": d.get("size_class","medium"),
                                    "style": d.get("style","pacer"), "wins": d.get("wins",0), "races": d.get("races",0),
                                    "is_player": False, "position": 0.0, "place": 0, "surge_timer": 0.0, "finished": False,
                                })
                        # Calculate odds
                        ratings = [h["race_rating"] for h in self._race_horses]
                        avg = sum(ratings) / max(len(ratings), 1)
                        for h in self._race_horses:
                            ratio = avg / max(h["race_rating"], 0.01)
                            h["odds"] = round(max(1.1, min(8.0, ratio * 1.6)), 1)
                        self._race_phase = "bet"
                        self._race_time  = 0.0
                        self._race_finished  = False
                        self._race_placements = []
                        self._race_commentary_triggers = set()
                        self._race_bet_horse = None
                        self._race_bet_amount = _BET_OPTIONS[0]
                elif key == "circuit_view_legs":
                    self._race_phase = "circuit_legs"
                elif key == "circuit_abandon":
                    player.active_circuit = None
                    self._circuit_leg_active = False
                elif key == "back_to_choose":
                    self._race_phase = "choose"
            elif phase == "circuit_legs":
                if key == "back_to_circuit_menu":
                    self._race_phase = "circuit_menu"
            elif phase == "circuit_result":
                if key == "circuit_done":
                    player.active_circuit = None
                    self._circuit_leg_active = False
                    self._race_phase = "choose"
            elif phase == "roster":
                if isinstance(key, tuple) and key[0] == "steeplechase_toggle":
                    self._race_steeplechase = key[1]
                    self._race_horses = []   # rebuild field on toggle
                elif isinstance(key, tuple) and key[0] == "inspect":
                    self._race_inspect_uid = key[1]
                    self._race_phase = "inspect"
                elif key == "enter":
                    npc = self._race_bookkeeper
                    fee = npc.entry_fee(player) if npc else 50
                    has_field = any(not h.get("is_player") for h in self._race_horses)
                    if mode == "dog":
                        racer_ready = self._race_player_dog is not None
                    else:
                        racer_ready = self._race_player_horse is not None
                    # Spectator mode: skip racer check, go straight to bet
                    spectating = (not racer_ready and has_field)
                    if spectating:
                        self._race_phase = "bet"
                    elif racer_ready and has_field and player.money >= fee:
                        player.money -= fee
                        if mode == "dog":
                            self._race_horses = self._build_dog_race_field(player)
                        else:
                            player.races_entered = getattr(player, "races_entered", 0) + 1
                            self._race_horses = self._build_race_field(player)
                        self._race_phase = "bet"
                elif key == "close":
                    self.racing_open = False
            elif phase == "inspect":
                if key == "back_from_inspect":
                    self._race_phase = "roster"
                elif key == "enter":
                    npc = self._race_bookkeeper
                    fee = npc.entry_fee(player) if npc else 50
                    has_field = any(not h.get("is_player") for h in self._race_horses)
                    if mode == "dog":
                        racer_ready = self._race_player_dog is not None
                    else:
                        racer_ready = self._race_player_horse is not None
                    if racer_ready and has_field and player.money >= fee:
                        player.money -= fee
                        if mode == "dog":
                            self._race_horses = self._build_dog_race_field(player)
                        else:
                            player.races_entered = getattr(player, "races_entered", 0) + 1
                            self._race_horses = self._build_race_field(player)
                        self._race_phase = "bet"
            elif phase == "bet":
                if isinstance(key, tuple):
                    if key[0] == "pick_horse":
                        self._race_bet_horse = key[1]
                    elif key[0] == "bet_amt":
                        if player.money >= key[1]:
                            self._race_bet_amount = key[1]
                elif key == "go":
                    if self._race_bet_horse and player.money >= self._race_bet_amount:
                        player.money -= self._race_bet_amount
                        self._race_phase = "gate"
                        self._race_time  = 0.0
                        self._race_finished  = False
                        self._race_placements = []
                        self._race_commentary_triggers = set()
                elif key == "back":
                    self._race_phase = "roster"
            elif phase == "result":
                if key == "again":
                    if getattr(self, "_circuit_leg_active", False):
                        self._circuit_leg_active = False
                        self._race_phase = "circuit_menu"
                    else:
                        self._race_phase = "choose"
                    self._race_horses   = []
                    self._race_bet_horse = None
                    self._race_placements = []
                    self._race_result_msg = ""
                    self._race_inspect_uid = None
                    self._race_player_horse = self._find_player_horse(player)
                    self._race_player_dog   = self._find_player_dog(player)
                elif key == "leave":
                    self._circuit_leg_active = False
                    self.racing_open = False
            break

    def handle_racing_keydown(self, key, player):
        if key == pygame.K_ESCAPE:
            phase = self._race_phase
            if phase == "choose":
                self.racing_open = False
            elif phase == "inspect":
                self._race_phase = "roster"
            elif phase == "roster":
                self._race_phase = "choose"
            elif phase == "result":
                if getattr(self, "_circuit_leg_active", False):
                    self._circuit_leg_active = False
                    self._race_phase = "circuit_menu"
                else:
                    self.racing_open = False
            elif phase == "bet":
                if getattr(self, "_circuit_leg_active", False):
                    self._race_phase = "circuit_menu"
                else:
                    self._race_phase = "roster"
            elif phase == "tack_shop":
                self._race_phase = "choose"
            elif phase == "circuit_menu":
                self._race_phase = "choose"
            elif phase == "circuit_legs":
                self._race_phase = "circuit_menu"
            elif phase == "circuit_result":
                player.active_circuit = None
                self._circuit_leg_active = False
                self._race_phase = "choose"
