"""Arena UI — gladiator spectator experience, betting, and card collecting."""
import pygame
import random

from gladiators import (simulate_fight, GladiatorProfile,
                        _BOUT_TYPE_LABEL, _BOUT_TYPE_COLOR,
                        _BEAST_CROWD_LINES, _ANIMAL_DEFS)

_BET_OPTIONS    = [10, 25, 50, 100]
_PANEL_BG       = (35, 28, 18)
_PANEL_STONE    = (55, 45, 30)
_PANEL_GOLD     = (200, 165, 60)
_PANEL_SAND     = (180, 150, 95)
_CROWD_CHEER    = ["The crowd erupts!", "ROME DEMANDS BLOOD!", "They roar his name!",
                   "A mighty cheer!", "The mob goes wild!", "Ave, gladiator!"]
_CROWD_BEAST    = _BEAST_CROWD_LINES

_RARITY_COLORS  = {"common": (180, 180, 180), "rare": (120, 180, 255), "legendary": (255, 215, 60)}
_RARITY_BG      = {"common": (40, 40, 50), "rare": (25, 35, 65), "legendary": (55, 45, 10)}


class _FacingProxy:
    """Duck-type wrapper so a GladiatorProfile can be passed to draw_npc_guard."""
    def __init__(self, gladiator: GladiatorProfile, facing: int):
        self._g     = gladiator
        self.facing = facing

    def __getattr__(self, name):
        return getattr(self._g, name)


def _draw_hp_bar(screen, x, y, w, h, current, maximum, color):
    ratio = max(0.0, current / maximum) if maximum > 0 else 0.0
    pygame.draw.rect(screen, (50, 20, 20), (x, y, w, h))
    pygame.draw.rect(screen, color, (x, y, int(w * ratio), h))
    pygame.draw.rect(screen, (120, 100, 80), (x, y, w, h), 1)


class ArenaUIMixin:

    def open_arena(self, bouts):
        self.arena_open         = True
        self._arena_phase       = "lobby"
        self._arena_bouts       = bouts
        self._arena_selected_bout = 0
        self._arena_bet_fighter = None   # 0 = g1, 1 = g2
        self._arena_bet_amount  = 10
        self._arena_current_bout = 0
        self._arena_round_idx   = 0
        self._arena_round_timer = 0.0
        self._arena_crowd_favor = 0.5
        self._arena_result_card = None  # GladiatorProfile or None
        self._arena_gold_delta  = 0
        self._arena_rects       = {}
        self._arena_log_lines   = []    # recent event strings for watch phase

    # -----------------------------------------------------------------------
    # Top-level dispatcher
    # -----------------------------------------------------------------------

    def _draw_arena(self, player, dt):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        sw, sh = self.screen.get_size()
        pw, ph = 680, 480
        px = (sw - pw) // 2
        py = (sh - ph) // 2

        # Stone panel
        pygame.draw.rect(self.screen, _PANEL_BG, (px, py, pw, ph), border_radius=6)
        pygame.draw.rect(self.screen, (80, 65, 40), (px, py, pw, ph), 2, border_radius=6)
        pygame.draw.rect(self.screen, _PANEL_STONE, (px + 10, py + 10, pw - 20, ph - 20), border_radius=4)

        # Title strip
        title_strip = pygame.Rect(px + 10, py + 10, pw - 20, 30)
        pygame.draw.rect(self.screen, (60, 45, 20), title_strip, border_radius=4)
        title = self.font.render("THE ARENA", True, _PANEL_GOLD)
        self.screen.blit(title, (px + pw // 2 - title.get_width() // 2, py + 16))

        if self._arena_phase == "lobby":
            self._draw_arena_lobby(player, px, py, pw, ph)
        elif self._arena_phase == "watch":
            self._draw_arena_watch(player, dt, px, py, pw, ph)
        elif self._arena_phase == "result":
            self._draw_arena_result(player, px, py, pw, ph)

    # -----------------------------------------------------------------------
    # Lobby phase
    # -----------------------------------------------------------------------

    def _draw_arena_lobby(self, player, px, py, pw, ph):
        self._arena_rects = {}
        font, small = self.font, self.small
        content_y = py + 50
        left_w  = 280
        right_w = pw - left_w - 30
        left_x  = px + 14
        right_x = px + left_w + 20

        # ---- Left: bout list ----
        header = small.render("TODAY'S BOUTS", True, _PANEL_SAND)
        self.screen.blit(header, (left_x, content_y))

        for i, bout in enumerate(self._arena_bouts):
            by = content_y + 22 + i * 88
            card_rect = pygame.Rect(left_x, by, left_w - 8, 82)
            selected  = (self._arena_selected_bout == i)
            bg = (65, 52, 28) if selected else (45, 36, 20)
            brd = _BOUT_TYPE_COLOR.get(bout.bout_type, (90, 75, 45)) if selected else (90, 75, 45)
            pygame.draw.rect(self.screen, bg, card_rect, border_radius=4)
            pygame.draw.rect(self.screen, brd, card_rect, 1 if not selected else 2, border_radius=4)
            self._arena_rects[("bout", i)] = card_rect

            # Bout type badge
            badge_col = _BOUT_TYPE_COLOR.get(bout.bout_type, (150, 150, 150))
            badge_txt = small.render(_BOUT_TYPE_LABEL.get(bout.bout_type, ""), True, badge_col)
            self.screen.blit(badge_txt, (left_x + left_w // 2 - 4 - badge_txt.get_width() // 2, by + 66))

            g2_is_animal = getattr(bout.g2, "is_animal", False)

            # Left fighter
            self._draw_gladiator_mini(self.screen, bout.g1, left_x + 8, by + 8, 1)
            g1_lbl = small.render(bout.g1.name.split()[0], True, (230, 210, 170))
            self.screen.blit(g1_lbl, (left_x + 36, by + 6))
            rar1 = small.render(bout.g1.rarity, True, _RARITY_COLORS.get(bout.g1.rarity, (200, 200, 200)))
            self.screen.blit(rar1, (left_x + 36, by + 20))
            fame1 = small.render(f"Fame {bout.g1.fame}", True, (170, 155, 110))
            self.screen.blit(fame1, (left_x + 36, by + 34))
            rec1 = small.render(f"{bout.g1.wins}W/{bout.g1.losses}L", True, (140, 140, 120))
            self.screen.blit(rec1, (left_x + 36, by + 48))

            # VS label
            vs_col = _BOUT_TYPE_COLOR.get(bout.bout_type, (220, 180, 80))
            vs = font.render("VS", True, vs_col)
            self.screen.blit(vs, (left_x + left_w // 2 - 14, by + 22))

            # Right: animal or second gladiator
            if g2_is_animal:
                self._draw_beast_portrait(self.screen, bout.g2,
                                          left_x + left_w - 50, by + 8)
                a2_lbl = small.render(bout.g2.name, True, (220, 185, 140))
                self.screen.blit(a2_lbl, (left_x + left_w - 8 - a2_lbl.get_width() - 6, by + 6))
                a2_rar = small.render(bout.g2.rarity, True, _RARITY_COLORS.get(bout.g2.rarity, (200, 200, 200)))
                self.screen.blit(a2_rar, (left_x + left_w - 8 - a2_rar.get_width() - 6, by + 20))
                a2_sz  = small.render(bout.g2.size_class.upper(), True, (160, 130, 90))
                self.screen.blit(a2_sz,  (left_x + left_w - 8 - a2_sz.get_width() - 6, by + 34))
                a2_hp  = small.render(f"HP {bout.g2.max_hp}", True, (130, 195, 130))
                self.screen.blit(a2_hp,  (left_x + left_w - 8 - a2_hp.get_width() - 6, by + 48))
            else:
                self._draw_gladiator_mini(self.screen, bout.g2, left_x + left_w - 8 - 28, by + 8, -1)
                g2_lbl = small.render(bout.g2.name.split()[0], True, (230, 210, 170))
                self.screen.blit(g2_lbl, (left_x + left_w - 8 - g2_lbl.get_width() - 36, by + 6))
                rar2 = small.render(bout.g2.rarity, True, _RARITY_COLORS.get(bout.g2.rarity, (200, 200, 200)))
                self.screen.blit(rar2, (left_x + left_w - 8 - rar2.get_width() - 36, by + 20))
                fame2 = small.render(f"Fame {bout.g2.fame}", True, (170, 155, 110))
                self.screen.blit(fame2, (left_x + left_w - 8 - fame2.get_width() - 36, by + 34))
                rec2 = small.render(f"{bout.g2.wins}W/{bout.g2.losses}L", True, (140, 140, 120))
                self.screen.blit(rec2, (left_x + left_w - 8 - rec2.get_width() - 36, by + 48))

        # ---- Right: bet panel for selected bout ----
        bout = self._arena_bouts[self._arena_selected_bout]
        pygame.draw.rect(self.screen, (42, 33, 15), (right_x, content_y, right_w, ph - 70), border_radius=4)
        pygame.draw.rect(self.screen, (90, 75, 45), (right_x, content_y, right_w, ph - 70), 1, border_radius=4)

        bet_title = font.render("PLACE YOUR BET", True, _PANEL_GOLD)
        self.screen.blit(bet_title, (right_x + right_w // 2 - bet_title.get_width() // 2, content_y + 8))

        # Fighter pick buttons — adapt for beast bouts
        pick_y = content_y + 38
        g2_is_animal = getattr(bout.g2, "is_animal", False)
        fighters = (bout.g1, bout.g2)
        for fi, g in enumerate(fighters):
            fx = right_x + 8 + fi * (right_w // 2 - 4)
            fw = right_w // 2 - 12
            frect = pygame.Rect(fx, pick_y, fw, 60)
            sel = (self._arena_bet_fighter == fi)
            fbg  = (70, 55, 20) if sel else (48, 38, 18)
            fbrd = (200, 170, 70) if sel else (90, 75, 45)
            pygame.draw.rect(self.screen, fbg, frect, border_radius=4)
            pygame.draw.rect(self.screen, fbrd, frect, 1, border_radius=4)
            self._arena_rects[("pick_fighter", fi)] = frect

            is_animal = getattr(g, "is_animal", False)
            if is_animal:
                self._draw_beast_portrait(self.screen, g, fx + 4, pick_y + 8)
                fname  = small.render(g.name, True, (220, 185, 140))
                fstats = small.render(f"ATK {g.attack}  DEF {g.defense}", True, (170, 155, 110))
                fhp    = small.render(f"HP {g.max_hp}  {g.size_class.upper()}", True, (130, 200, 130))
                frar   = small.render(g.rarity.upper(), True, _RARITY_COLORS.get(g.rarity, (200, 200, 200)))
                self.screen.blit(fname,  (fx + 38, pick_y + 4))
                self.screen.blit(frar,   (fx + 38, pick_y + 18))
                self.screen.blit(fstats, (fx + 38, pick_y + 32))
                self.screen.blit(fhp,    (fx + 38, pick_y + 46))
            else:
                self._draw_gladiator_mini(self.screen, g, fx + 4, pick_y + 8, 1 if fi == 0 else -1)
                fname  = small.render(g.name.split()[0], True, (230, 210, 170))
                fstats = small.render(f"S{g.strength} A{g.agility} E{g.endurance}", True, (170, 155, 110))
                fhp    = small.render(f"HP {g.max_hp}", True, (130, 200, 130))
                self.screen.blit(fname,  (fx + 32, pick_y + 6))
                self.screen.blit(fstats, (fx + 32, pick_y + 22))
                self.screen.blit(fhp,    (fx + 32, pick_y + 38))

        # Bet amount buttons
        bet_label = small.render("Wager:", True, _PANEL_SAND)
        self.screen.blit(bet_label, (right_x + 8, pick_y + 72))

        bw, bh, bgap = 54, 28, 6
        for bi, amt in enumerate(_BET_OPTIONS):
            bx = right_x + 8 + bi * (bw + bgap)
            brect = pygame.Rect(bx, pick_y + 90, bw, bh)
            affordable = player.money >= amt
            sel = (self._arena_bet_amount == amt)
            bbg = (70, 55, 20) if sel else ((45, 38, 18) if affordable else (35, 30, 25))
            bbrd = (200, 170, 70) if sel else ((90, 75, 45) if affordable else (60, 55, 45))
            pygame.draw.rect(self.screen, bbg, brect, border_radius=4)
            pygame.draw.rect(self.screen, bbrd, brect, 1, border_radius=4)
            blbl = small.render(f"{amt}g", True, (230, 210, 170) if affordable else (100, 90, 70))
            self.screen.blit(blbl, (brect.centerx - blbl.get_width() // 2, brect.centery - blbl.get_height() // 2))
            self._arena_rects[("bet_amt", amt)] = brect

        gold_txt = small.render(f"Your gold: {player.money}", True, (200, 175, 100))
        self.screen.blit(gold_txt, (right_x + 8, pick_y + 128))

        # Watch button
        watch_rect = pygame.Rect(right_x + 8, py + ph - 100, right_w - 16, 38)
        can_watch  = True
        wbg = (80, 55, 15) if can_watch else (50, 45, 30)
        pygame.draw.rect(self.screen, wbg, watch_rect, border_radius=5)
        pygame.draw.rect(self.screen, (200, 165, 60), watch_rect, 1, border_radius=5)
        wlbl = font.render("WATCH THE GAMES", True, (240, 220, 150) if can_watch else (130, 120, 90))
        self.screen.blit(wlbl, (watch_rect.centerx - wlbl.get_width() // 2, watch_rect.centery - wlbl.get_height() // 2))
        self._arena_rects["watch"] = watch_rect

        # Leave button
        leave_rect = pygame.Rect(right_x + 8, py + ph - 52, right_w - 16, 32)
        pygame.draw.rect(self.screen, (60, 30, 20), leave_rect, border_radius=4)
        pygame.draw.rect(self.screen, (150, 100, 80), leave_rect, 1, border_radius=4)
        llbl = small.render("Leave", True, (210, 170, 150))
        self.screen.blit(llbl, (leave_rect.centerx - llbl.get_width() // 2, leave_rect.centery - llbl.get_height() // 2))
        self._arena_rects["leave"] = leave_rect

        # Sponsor stub
        sponsor_rect = pygame.Rect(left_x, py + ph - 52, left_w - 8, 32)
        pygame.draw.rect(self.screen, (35, 30, 20), sponsor_rect, border_radius=4)
        pygame.draw.rect(self.screen, (70, 60, 40), sponsor_rect, 1, border_radius=4)
        slbl = small.render("Sponsor a Gladiator (coming soon)", True, (100, 90, 65))
        self.screen.blit(slbl, (sponsor_rect.centerx - slbl.get_width() // 2, sponsor_rect.centery - slbl.get_height() // 2))

    # -----------------------------------------------------------------------
    # Watch phase
    # -----------------------------------------------------------------------

    def _draw_arena_watch(self, player, dt, px, py, pw, ph):
        self._arena_rects = {}
        font, small = self.font, self.small

        bout     = self._arena_bouts[self._arena_current_bout]
        g1, g2   = bout.g1, bout.g2

        # Simulate on first entry if not yet done
        if not bout.round_log:
            rng = random.Random()
            bout.round_log  = simulate_fight(g1, g2, rng)
            bout.winner_uid = g1.uid if bout.round_log and bout.round_log[-1]["hp1_after"] > 0 else g2.uid

        rounds = bout.round_log
        content_y = py + 50

        # ---- Crowd favor bar ----
        if rounds and self._arena_round_idx < len(rounds):
            ev = rounds[self._arena_round_idx]
            target_favor = ev["hp1_after"] / (g1.max_hp) if (g1.max_hp + g2.max_hp) > 0 else 0.5
            self._arena_crowd_favor += (target_favor - self._arena_crowd_favor) * 0.15
        favor = self._arena_crowd_favor
        fbar_x, fbar_y, fbar_w, fbar_h = px + 120, content_y, pw - 240, 14
        pygame.draw.rect(self.screen, (120, 30, 30), (fbar_x, fbar_y, int(fbar_w * (1 - favor)), fbar_h))
        pygame.draw.rect(self.screen, (30, 80, 30),  (fbar_x + int(fbar_w * (1 - favor)), fbar_y, int(fbar_w * favor), fbar_h))
        pygame.draw.rect(self.screen, (120, 100, 60), (fbar_x, fbar_y, fbar_w, fbar_h), 1)
        crowd_lbl = small.render("CROWD FAVOR", True, (160, 140, 90))
        self.screen.blit(crowd_lbl, (fbar_x + fbar_w // 2 - crowd_lbl.get_width() // 2, fbar_y + 18))

        # ---- HP bars ----
        if rounds and self._arena_round_idx < len(rounds):
            ev   = rounds[self._arena_round_idx]
            hp1  = ev["hp1_after"]
            hp2  = ev["hp2_after"]
        else:
            hp1 = g1.max_hp if not rounds else rounds[-1]["hp1_after"]
            hp2 = g2.max_hp if not rounds else rounds[-1]["hp2_after"]

        bar_y   = content_y + 38
        bar_h_s = 12
        _draw_hp_bar(self.screen, px + 14,       bar_y, 200, bar_h_s, hp1, g1.max_hp, (80, 180, 80))
        _draw_hp_bar(self.screen, px + pw - 214, bar_y, 200, bar_h_s, hp2, g2.max_hp, (80, 180, 80))

        g1_name = small.render(g1.name, True, (220, 200, 150))
        g2_name = small.render(g2.name, True, (220, 200, 150))
        self.screen.blit(g1_name, (px + 14, bar_y - 16))
        self.screen.blit(g2_name, (px + pw - 14 - g2_name.get_width(), bar_y - 16))

        hp1_txt = small.render(f"{hp1}/{g1.max_hp}", True, (130, 200, 130))
        hp2_txt = small.render(f"{hp2}/{g2.max_hp}", True, (130, 200, 130))
        self.screen.blit(hp1_txt, (px + 14, bar_y + 14))
        self.screen.blit(hp2_txt, (px + pw - 14 - hp2_txt.get_width(), bar_y + 14))

        # ---- Gladiator sprites / beast portraits ----
        sprite_y = bar_y + 32
        scale = 2
        g1_sx = px + 80
        g2_sx = px + pw - 80 - 20 * scale

        self._draw_gladiator_mini(self.screen, g1, g1_sx, sprite_y, 1, scale=scale)

        g2_is_animal = getattr(g2, "is_animal", False)
        if g2_is_animal:
            self._draw_beast_portrait(self.screen, g2, g2_sx, sprite_y, scale=scale)
        else:
            self._draw_gladiator_mini(self.screen, g2, g2_sx, sprite_y, -1, scale=scale)

        # Bout type label between fighters
        btype_lbl = font.render(_BOUT_TYPE_LABEL.get(bout.bout_type, ""), True,
                                _BOUT_TYPE_COLOR.get(bout.bout_type, _PANEL_GOLD))
        self.screen.blit(btype_lbl, (px + pw // 2 - btype_lbl.get_width() // 2, sprite_y - 2))

        # Round label below bout type
        rnd_num = rounds[min(self._arena_round_idx, len(rounds) - 1)]["round"] if rounds else 1
        rnd_lbl = small.render(f"Round {rnd_num}", True, (170, 155, 110))
        self.screen.blit(rnd_lbl, (px + pw // 2 - rnd_lbl.get_width() // 2, sprite_y + 18))

        # ---- Event log (last 4 lines) ----
        log_y = sprite_y + 80
        log_box = pygame.Rect(px + 14, log_y, pw - 28, 96)
        pygame.draw.rect(self.screen, (28, 22, 12), log_box, border_radius=4)
        pygame.draw.rect(self.screen, (80, 65, 40), log_box, 1, border_radius=4)
        lines_to_show = self._arena_log_lines[-4:]
        for li, line in enumerate(lines_to_show):
            age   = len(lines_to_show) - 1 - li
            alpha = max(160, 255 - age * 28)
            col   = (alpha, int(alpha * 0.9), int(alpha * 0.6))
            ls    = small.render(line, True, col)
            self.screen.blit(ls, (log_box.x + 8, log_box.y + 8 + li * 20))

        # ---- Advance animation ----
        self._arena_round_timer += dt
        round_speed = 0.7
        if self._arena_round_timer >= round_speed and self._arena_round_idx < len(rounds) - 1:
            self._arena_round_timer = 0.0
            self._arena_round_idx  += 1
            ev = rounds[self._arena_round_idx]
            line = self._format_round_line(ev, g1, g2)
            self._arena_log_lines.append(line)
        elif self._arena_round_idx == 0 and rounds:
            ev   = rounds[0]
            line = self._format_round_line(ev, g1, g2)
            if not self._arena_log_lines:
                self._arena_log_lines.append(line)
        elif self._arena_round_timer >= round_speed and self._arena_round_idx >= len(rounds) - 1:
            self._arena_phase = "result"
            self._arena_round_timer = 0.0
            self._resolve_arena_result(player)

        # Skip button
        skip_rect = pygame.Rect(px + pw - 110, py + ph - 50, 96, 30)
        pygame.draw.rect(self.screen, (55, 42, 20), skip_rect, border_radius=4)
        pygame.draw.rect(self.screen, (120, 100, 60), skip_rect, 1, border_radius=4)
        sk = small.render("SKIP", True, (190, 165, 100))
        self.screen.blit(sk, (skip_rect.centerx - sk.get_width() // 2, skip_rect.centery - sk.get_height() // 2))
        self._arena_rects["skip"] = skip_rect

    def _format_round_line(self, ev, g1, g2):
        label = ev["label"]
        dmg   = ev["damage"]
        if ev.get("attacker_is_animal", False):
            # Animal attacks already have full flavor text
            dmg_tag = f" (-{dmg})" if dmg > 0 else ""
            return f"  {label}{dmg_tag}"
        if ev["crit"] and dmg > 0:
            return f"  {label}! ({dmg} dmg)"
        elif dmg == 0:
            return f"  {label}!"
        else:
            return f"  {label} for {dmg} dmg"

    # -----------------------------------------------------------------------
    # Result phase
    # -----------------------------------------------------------------------

    def _resolve_arena_result(self, player):
        bout      = self._arena_bouts[self._arena_current_bout]
        winner_uid = bout.winner_uid
        winner = bout.g1 if bout.g1.uid == winner_uid else bout.g2
        is_beast_bout = getattr(bout.g2, "is_animal", False)

        # Payout: champion bouts pay 3:1, beast hunts pay 2.5:1, duels pay 2:1
        payout_mult = {"champion": 3, "beast_hunt": 2, "duel": 2}.get(bout.bout_type, 2)

        gold_delta = 0
        if self._arena_bet_fighter is not None and self._arena_bet_amount > 0:
            picked_g = bout.g1 if self._arena_bet_fighter == 0 else bout.g2
            if picked_g.uid == winner_uid:
                gold_delta = self._arena_bet_amount * payout_mult
                player.money = max(0, player.money + gold_delta)
            else:
                gold_delta = -self._arena_bet_amount
                player.money = max(0, player.money + gold_delta)
        self._arena_gold_delta = gold_delta

        # Card drop logic:
        # - Beast hunt won by gladiator → 50% chance of gladiator card
        # - Duel/champion → 40% chance of winner card (only gladiators)
        # - Beast wins → no card
        self._arena_result_card = None
        picked_g = None
        if self._arena_bet_fighter is not None:
            picked_g = bout.g1 if self._arena_bet_fighter == 0 else bout.g2
        if not getattr(winner, "is_animal", False) and picked_g and picked_g.uid == winner_uid:
            drop_chance = 0.50 if is_beast_bout else 0.40
            if random.random() < drop_chance:
                self._arena_result_card = winner
                cards = getattr(player, "gladiator_cards", [])
                if not any(c.get("uid") == winner.uid for c in cards):
                    cards.append(winner.to_dict())
                    player.gladiator_cards = cards

    def _draw_arena_result(self, player, px, py, pw, ph):
        self._arena_rects = {}
        font, small = self.font, self.small

        bout     = self._arena_bouts[self._arena_current_bout]
        winner   = bout.g1 if bout.winner_uid == bout.g1.uid else bout.g2
        loser    = bout.g2 if bout.winner_uid == bout.g1.uid else bout.g1

        content_y = py + 50

        # Winner banner
        winner_is_animal = getattr(winner, "is_animal", False)
        win_text = (f"THE {winner.name.upper()} WINS!"
                    if winner_is_animal else f"{winner.name.split()[0]} WINS!")
        win_col  = (210, 100, 50) if winner_is_animal else _PANEL_GOLD
        win_lbl  = font.render(win_text, True, win_col)
        self.screen.blit(win_lbl, (px + pw // 2 - win_lbl.get_width() // 2, content_y))

        # Sprites
        sprite_y = content_y + 34
        if winner_is_animal:
            self._draw_beast_portrait(self.screen, winner, px + pw // 2 - 28, sprite_y, scale=2)
        else:
            self._draw_gladiator_mini(self.screen, winner, px + pw // 2 - 24, sprite_y, 1, scale=2)

        # Crowd cheer — beast fights use wilder lines
        cheer_pool = _CROWD_BEAST if bout.bout_type == "beast_hunt" else _CROWD_CHEER
        cheer_col  = (220, 150, 70) if bout.bout_type == "beast_hunt" else _PANEL_SAND
        cheer = random.choice(cheer_pool)
        cheer_s = small.render(cheer, True, cheer_col)
        self.screen.blit(cheer_s, (px + pw // 2 - cheer_s.get_width() // 2, sprite_y + 56))

        # Gold result
        result_y = sprite_y + 80
        if self._arena_gold_delta > 0:
            gold_msg = f"You won your bet! +{self._arena_gold_delta}g"
            gold_col = (120, 230, 120)
        elif self._arena_gold_delta < 0:
            gold_msg = f"You lost your bet. {self._arena_gold_delta}g"
            gold_col = (230, 100, 100)
        else:
            gold_msg = "No bet placed."
            gold_col = (180, 170, 140)
        gold_s = font.render(gold_msg, True, gold_col)
        self.screen.blit(gold_s, (px + pw // 2 - gold_s.get_width() // 2, result_y))

        # Card drop
        card_y = result_y + 32
        if self._arena_result_card is not None:
            card = self._arena_result_card
            card_box = pygame.Rect(px + pw // 2 - 130, card_y, 260, 60)
            rar_bg = _RARITY_BG.get(card.rarity, (40, 40, 50))
            pygame.draw.rect(self.screen, rar_bg, card_box, border_radius=5)
            pygame.draw.rect(self.screen, _RARITY_COLORS.get(card.rarity, (180, 180, 180)), card_box, 1, border_radius=5)
            card_header = small.render("GLADIATOR CARD OBTAINED!", True, _RARITY_COLORS.get(card.rarity, (200, 200, 200)))
            self.screen.blit(card_header, (card_box.centerx - card_header.get_width() // 2, card_y + 6))
            card_name = font.render(card.name, True, (240, 220, 160))
            self.screen.blit(card_name, (card_box.centerx - card_name.get_width() // 2, card_y + 26))
            card_rar = small.render(card.rarity.upper(), True, _RARITY_COLORS.get(card.rarity, (180, 180, 180)))
            self.screen.blit(card_rar, (card_box.centerx - card_rar.get_width() // 2, card_y + 44))
            card_y += 68

        # Buttons
        btn_y = py + ph - 58
        more_bouts = self._arena_current_bout < len(self._arena_bouts) - 1
        if more_bouts:
            next_rect = pygame.Rect(px + pw // 2 - 130, btn_y, 120, 38)
            pygame.draw.rect(self.screen, (60, 48, 18), next_rect, border_radius=5)
            pygame.draw.rect(self.screen, _PANEL_GOLD, next_rect, 1, border_radius=5)
            nlbl = font.render("Next Bout", True, (240, 220, 150))
            self.screen.blit(nlbl, (next_rect.centerx - nlbl.get_width() // 2, next_rect.centery - nlbl.get_height() // 2))
            self._arena_rects["next"] = next_rect

        leave_rect = pygame.Rect(px + pw // 2 + 10 if more_bouts else px + pw // 2 - 60, btn_y, 120, 38)
        pygame.draw.rect(self.screen, (60, 30, 20), leave_rect, border_radius=5)
        pygame.draw.rect(self.screen, (150, 100, 80), leave_rect, 1, border_radius=5)
        llbl = font.render("Leave", True, (220, 180, 160))
        self.screen.blit(llbl, (leave_rect.centerx - llbl.get_width() // 2, leave_rect.centery - llbl.get_height() // 2))
        self._arena_rects["leave"] = leave_rect

    # -----------------------------------------------------------------------
    # Gladiator codex (collection tab)
    # -----------------------------------------------------------------------

    def _draw_gladiator_codex(self, player, gy0=58, gx_off=0):
        font, small = self.font, self.small
        cards_raw = getattr(player, "gladiator_cards", [])
        cards = []
        for d in cards_raw:
            try:
                cards.append(GladiatorProfile.from_dict(d))
            except Exception:
                pass

        sw = self.screen.get_width()
        if not cards:
            no_msg = font.render("No gladiator cards yet. Attend the arena!", True, (140, 130, 100))
            self.screen.blit(no_msg, (sw // 2 - no_msg.get_width() // 2, gy0 + 40))
            return

        CARD_W, CARD_H, GAP = 160, 190, 10
        cols = max(1, (sw - gx_off - 10) // (CARD_W + GAP))
        scroll = getattr(self, "_gladiator_codex_scroll", 0)

        for ci, card in enumerate(cards):
            col = ci % cols
            row = ci // cols
            cx  = gx_off + 8 + col * (CARD_W + GAP)
            cy  = gy0 + 4 + row * (CARD_H + GAP) - scroll
            if cy + CARD_H < gy0 or cy > self.screen.get_height():
                continue

            rar_bg  = _RARITY_BG.get(card.rarity, (40, 40, 50))
            rar_brd = _RARITY_COLORS.get(card.rarity, (180, 180, 180))
            crect   = pygame.Rect(cx, cy, CARD_W, CARD_H)
            pygame.draw.rect(self.screen, rar_bg, crect, border_radius=5)
            pygame.draw.rect(self.screen, rar_brd, crect, 1, border_radius=5)

            # Sprite centered in top half
            self._draw_gladiator_mini(self.screen, card, cx + CARD_W // 2 - 10, cy + 10, 1)

            # Name
            name_s = small.render(card.name, True, (230, 210, 165))
            if name_s.get_width() > CARD_W - 6:
                name_s = small.render(card.name.split()[0], True, (230, 210, 165))
            self.screen.blit(name_s, (cx + CARD_W // 2 - name_s.get_width() // 2, cy + 38))

            rar_s = small.render(card.rarity.upper(), True, rar_brd)
            self.screen.blit(rar_s, (cx + CARD_W // 2 - rar_s.get_width() // 2, cy + 54))

            # Stats
            stats_lines = [
                f"STR {card.strength}  AGI {card.agility}  END {card.endurance}",
                f"HP {card.max_hp}  ATK {card.attack}  DEF {card.defense}",
                f"Fame: {card.fame}",
                f"Record: {card.wins}W / {card.losses}L",
                f"Origin: {card.origin_biome}",
            ]
            for si, sl in enumerate(stats_lines):
                ss = small.render(sl, True, (180, 165, 130))
                self.screen.blit(ss, (cx + CARD_W // 2 - ss.get_width() // 2, cy + 72 + si * 18))

        total_rows = (len(cards) + cols - 1) // cols
        total_h    = total_rows * (CARD_H + GAP)
        visible_h  = self.screen.get_height() - gy0
        max_scroll = max(0, total_h - visible_h)
        self._gladiator_codex_scroll = min(scroll, max_scroll)

    # -----------------------------------------------------------------------
    # Sprite helpers
    # -----------------------------------------------------------------------

    def _draw_beast_portrait(self, surface, animal, x, y, scale=1):
        """Draw a stylized beast silhouette based on size class and color."""
        col    = animal.body_color
        dark   = tuple(max(0, v - 35) for v in col)
        rar    = animal.rarity
        glow   = _RARITY_COLORS.get(rar, (180, 180, 180))
        sc     = scale

        # Size-class shapes (all drawn at scale 1, then scaled)
        sz = animal.size_class
        # Bounding box per size_class at scale=1: (w, h)
        dims = {"small": (16, 12), "medium": (24, 16), "large": (32, 20), "huge": (40, 24)}
        bw, bh = dims.get(sz, (24, 16))
        bw, bh = bw * sc, bh * sc

        # Body ellipse
        pygame.draw.ellipse(surface, col, (x, y + bh // 3, bw, bh * 2 // 3))
        # Head (sphere-ish on right side)
        hw = max(6, bw // 4) * sc // sc
        pygame.draw.ellipse(surface, col, (x + bw - hw, y, hw, hw + 2))
        # Eye dot
        pygame.draw.circle(surface, (240, 50, 50), (x + bw - hw // 3, y + hw // 3), max(1, sc))
        # Rarity glow border
        if rar in ("rare", "legendary"):
            pygame.draw.ellipse(surface, glow, (x - 1, y + bh // 3 - 1, bw + 2, bh * 2 // 3 + 2), 1)
        # Legs (simple lines)
        leg_col = dark
        n_legs = 4
        for li in range(n_legs):
            lx = x + int(bw * (0.15 + li * 0.22))
            pygame.draw.rect(surface, leg_col, (lx, y + bh - 2, max(2, sc * 2), max(4, bh // 3)))

    def _draw_gladiator_mini(self, surface, gladiator, x, y, facing, scale=1):
        try:
            from Render.Guardsystem import draw_npc_guard
            proxy = _FacingProxy(gladiator, facing)
            if scale == 1:
                draw_npc_guard(surface, x, y, proxy)
            else:
                tmp = pygame.Surface((20 * scale + 4, 32 * scale + 4), pygame.SRCALPHA)
                draw_npc_guard(tmp, 2, 6, proxy)
                scaled = pygame.transform.scale(tmp, (tmp.get_width() * scale // scale,
                                                       tmp.get_height() * scale // scale))
                # Draw at 2× by scaling a small temporary surface
                tiny = pygame.Surface((24, 38), pygame.SRCALPHA)
                draw_npc_guard(tiny, 2, 6, proxy)
                big  = pygame.transform.scale(tiny, (24 * scale, 38 * scale))
                surface.blit(big, (x, y))
                return
        except Exception:
            pass

    # -----------------------------------------------------------------------
    # Input handlers
    # -----------------------------------------------------------------------

    def handle_arena_click(self, pos, player):
        phase = self._arena_phase
        for key, rect in self._arena_rects.items():
            if not rect.collidepoint(pos):
                continue

            if phase == "lobby":
                if isinstance(key, tuple) and key[0] == "bout":
                    self._arena_selected_bout = key[1]
                elif isinstance(key, tuple) and key[0] == "pick_fighter":
                    self._arena_bet_fighter = key[1]
                elif isinstance(key, tuple) and key[0] == "bet_amt":
                    if player.money >= key[1]:
                        self._arena_bet_amount = key[1]
                elif key == "watch":
                    self._start_arena_watch(player)
                elif key == "leave":
                    self.arena_open = False

            elif phase == "watch":
                if key == "skip":
                    self._skip_to_result(player)

            elif phase == "result":
                if key == "next":
                    self._arena_current_bout += 1
                    self._arena_bet_fighter  = None
                    self._arena_round_idx    = 0
                    self._arena_round_timer  = 0.0
                    self._arena_log_lines    = []
                    self._arena_crowd_favor  = 0.5
                    self._arena_phase        = "lobby"
                elif key == "leave":
                    self.arena_open = False
            break

    def _start_arena_watch(self, player):
        if self._arena_bet_fighter is not None and self._arena_bet_amount > 0:
            if player.money >= self._arena_bet_amount:
                player.money -= self._arena_bet_amount
            else:
                self._arena_bet_fighter = None
        self._arena_current_bout = self._arena_selected_bout
        self._arena_round_idx   = 0
        self._arena_round_timer = 0.0
        self._arena_log_lines   = []
        self._arena_crowd_favor = 0.5
        self._arena_gold_delta  = 0
        self._arena_result_card = None
        self._arena_phase       = "watch"

    def _skip_to_result(self, player):
        bout = self._arena_bouts[self._arena_current_bout]
        if not bout.round_log:
            rng = random.Random()
            bout.round_log  = simulate_fight(bout.g1, bout.g2, rng)
            bout.winner_uid = bout.g1.uid if bout.round_log and bout.round_log[-1]["hp1_after"] > 0 else bout.g2.uid
        self._arena_round_idx = len(bout.round_log) - 1
        self._resolve_arena_result(player)
        self._arena_phase = "result"

    def handle_arena_keydown(self, key, player):
        if key == pygame.K_ESCAPE:
            if self._arena_phase == "watch":
                self._skip_to_result(player)
                self._arena_phase = "result"
            else:
                self.arena_open = False
