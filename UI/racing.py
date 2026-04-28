import math
import random
import pygame
from Render.largeAnimal import draw_horse_traits

_BET_OPTIONS = [10, 25, 50, 100, 250]

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


class RacingMixin:

    # ------------------------------------------------------------------
    # Open / close
    # ------------------------------------------------------------------

    def open_racing(self, bookkeeper_npc, player):
        self.racing_open              = True
        self._race_phase              = "roster"
        self._race_bookkeeper         = bookkeeper_npc
        self._race_player_horse       = self._find_player_horse(player)
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
        self._race_inspect_uid        = None   # uid of horse selected for detail view

    def _find_player_horse(self, player):
        from horses import Horse as _Horse
        world = getattr(player, "world", None)
        if world is None:
            return None
        for ent in world.entities:
            if isinstance(ent, _Horse) and ent.tamed and not ent.dead and ent.rider is None:
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
            horses.append({
                "uid":          getattr(ph, "uid", "player"),
                "name":         getattr(ph, "name", "Your Horse"),
                "owner":        "You",
                "race_rating":  ph.race_rating,
                "stamina":      100.0,
                "stamina_max":  pt.get("stamina_max", 1.0),
                "endurance":    pt.get("endurance", 1.0),
                "reaction":     pt.get("reaction", 1.0),
                "agility":      pt.get("agility", 1.0),
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

        title = self.font.render("Horse Racing", True, (230, 205, 130))
        self.screen.blit(title, (px + pw // 2 - title.get_width() // 2, py + 13))

        phase = self._race_phase
        if phase == "roster":
            self._draw_race_roster(player, px, py, pw, ph)
        elif phase == "inspect":
            self._draw_race_inspect(player, px, py, pw, ph)
        elif phase == "bet":
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
        self.screen.blit(ring_lbl, (px + pw // 2 - ring_lbl.get_width() // 2, py + 40))

        # Column headers
        hdr_y = py + 62
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

        enter_rect = pygame.Rect(px + pw // 2 - 130, py + ph - 80, 120, 36)
        ec = (55, 140, 55) if can_enter else (50, 50, 50)
        pygame.draw.rect(self.screen, ec, enter_rect, border_radius=5)
        pygame.draw.rect(self.screen, (180, 230, 150) if can_enter else (90, 90, 90), enter_rect, 1, border_radius=5)
        el = self.font.render("Enter Race", True, (240, 240, 210) if can_enter else (120, 120, 120))
        self.screen.blit(el, (enter_rect.centerx - el.get_width() // 2, enter_rect.centery - el.get_height() // 2))
        self._race_rects["enter"] = enter_rect

        if not has_horse:
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

            # Actual horse sprite
            draw_horse_traits(self.screen, hx, hy, h, W=_HORSE_W, H=_HORSE_H, facing=1)

            # Surge spark (in front of horse nose)
            if h["surge_timer"] > 0:
                nose_x = hx + _HORSE_W + 10
                pygame.draw.circle(self.screen, (255, 240, 100), (nose_x, hy + 9), 4)
                pygame.draw.circle(self.screen, (255, 190, 50),  (nose_x, hy + 9), 2)

            # Name label (horse + owner condensed)
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
            sc   = _STYLE_COLORS.get(style, (160, 160, 160))

            # Place badge
            pl_t = self.small.render(f"{place_labels[i]}", True, pc)
            self.screen.blit(pl_t, (px + 40, ry))

            # Horse name + owner
            nm_c  = (255, 235, 130) if h.get("is_player") else (215, 200, 170)
            nm_t  = self.small.render(f"{h['name']}  ({h['owner']})", True, nm_c)
            self.screen.blit(nm_t, (px + 90, ry))

            # Style tag
            st_t = self.small.render(f"[{_STYLE_LABELS.get(style, '')}]", True, sc)
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
    # Input handlers
    # ------------------------------------------------------------------

    def handle_racing_click(self, pos, player):
        phase = self._race_phase
        for key, rect in self._race_rects.items():
            if not rect.collidepoint(pos):
                continue
            if phase == "roster":
                if isinstance(key, tuple) and key[0] == "inspect":
                    self._race_inspect_uid = key[1]
                    self._race_phase = "inspect"
                elif key == "enter":
                    npc = self._race_bookkeeper
                    fee = npc.entry_fee(player) if npc else 50
                    has_field = any(not h.get("is_player") for h in self._race_horses)
                    if self._race_player_horse is not None and has_field and player.money >= fee:
                        player.money -= fee
                        player.races_entered = getattr(player, "races_entered", 0) + 1
                        self._race_horses = self._build_race_field(player)
                        self._race_phase  = "bet"
                elif key == "close":
                    self.racing_open = False
            elif phase == "inspect":
                if key == "back_from_inspect":
                    self._race_phase = "roster"
                elif key == "enter":
                    npc = self._race_bookkeeper
                    fee = npc.entry_fee(player) if npc else 50
                    has_field = any(not h.get("is_player") for h in self._race_horses)
                    if self._race_player_horse is not None and has_field and player.money >= fee:
                        player.money -= fee
                        player.races_entered = getattr(player, "races_entered", 0) + 1
                        self._race_horses = self._build_race_field(player)
                        self._race_phase  = "bet"
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
                    self._race_phase    = "roster"
                    self._race_horses   = []
                    self._race_bet_horse = None
                    self._race_placements = []
                    self._race_result_msg = ""
                    self._race_inspect_uid = None
                elif key == "leave":
                    self.racing_open = False
            break

    def handle_racing_keydown(self, key, player):
        if key == pygame.K_ESCAPE:
            phase = self._race_phase
            if phase == "inspect":
                self._race_phase = "roster"
            elif phase in ("roster", "result"):
                self.racing_open = False
            elif phase == "bet":
                self._race_phase = "roster"
