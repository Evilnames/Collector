import pygame
import random

_PIP_POSITIONS = {
    1: [(3, 3)],
    2: [(1, 1), (5, 5)],
    3: [(1, 1), (3, 3), (5, 5)],
    4: [(1, 1), (5, 1), (1, 5), (5, 5)],
    5: [(1, 1), (5, 1), (3, 3), (1, 5), (5, 5)],
    6: [(1, 1), (5, 1), (1, 3), (5, 3), (1, 5), (5, 5)],
}

_BOT_NAMES = ["Aldric", "Mira", "Torvald", "Sable"]

_BET_OPTIONS = [10, 25, 50, 100]


def _draw_die_face(surface, x, y, size, value):
    cell = size // 6
    pygame.draw.rect(surface, (235, 235, 235), (x, y, size, size), border_radius=4)
    pygame.draw.rect(surface, (50, 50, 50), (x, y, size, size), 1, border_radius=4)
    pip_r = max(2, size // 12)
    for px, py in _PIP_POSITIONS[value]:
        pygame.draw.circle(surface, (30, 30, 30), (x + px * cell, y + py * cell), pip_r)


class GamblingMixin:

    def open_gambling_table(self, num_bots=3):
        self.gambling_open = True
        self._gamble_phase = "bet"
        self._gamble_bet = 10
        self._gamble_num_bots = min(num_bots, len(_BOT_NAMES))
        self._gamble_bot_names = _BOT_NAMES[:self._gamble_num_bots]
        self._gamble_bot_picks = []
        self._gamble_player_pick = None
        self._gamble_roll_timer = 0.0
        self._gamble_roll_result = None
        self._gamble_die1 = 1
        self._gamble_die2 = 1
        self._gamble_result_msg = ""
        self._gamble_net_gold = 0
        self._gamble_rects = {}

    def _draw_gambling(self, player, dt):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        sw, sh = self.screen.get_size()
        pw, ph = 560, 420
        px = (sw - pw) // 2
        py = (sh - ph) // 2

        # Felt panel
        pygame.draw.rect(self.screen, (20, 80, 40), (px, py, pw, ph), border_radius=8)
        pygame.draw.rect(self.screen, (255, 255, 255), (px, py, pw, ph), 1, border_radius=8)

        # Inner felt lighter rect
        pygame.draw.rect(self.screen, (28, 100, 52), (px + 12, py + 12, pw - 24, ph - 24), border_radius=6)

        title = self.font.render("Gambling Table", True, (230, 210, 140))
        self.screen.blit(title, (px + pw // 2 - title.get_width() // 2, py + 18))

        if self._gamble_phase == "bet":
            self._draw_gamble_bet(player, px, py, pw, ph)
        elif self._gamble_phase == "pick":
            self._draw_gamble_pick(player, px, py, pw, ph)
        elif self._gamble_phase == "rolling":
            self._draw_gamble_rolling(player, dt, px, py, pw, ph)
        elif self._gamble_phase == "result":
            self._draw_gamble_result(player, px, py, pw, ph)

    def _draw_gamble_bet(self, player, px, py, pw, ph):
        self._gamble_rects = {}
        font = self.font
        small = self.small

        gold_txt = font.render(f"Your gold: {player.money}", True, (230, 210, 140))
        self.screen.blit(gold_txt, (px + pw // 2 - gold_txt.get_width() // 2, py + 50))

        lbl = small.render("Choose your bet:", True, (200, 220, 180))
        self.screen.blit(lbl, (px + pw // 2 - lbl.get_width() // 2, py + 85))

        btn_w, btn_h = 100, 36
        total_w = len(_BET_OPTIONS) * btn_w + (len(_BET_OPTIONS) - 1) * 12
        bx_start = px + pw // 2 - total_w // 2
        by = py + 115

        for i, amt in enumerate(_BET_OPTIONS):
            bx = bx_start + i * (btn_w + 12)
            rect = pygame.Rect(bx, by, btn_w, btn_h)
            selected = (self._gamble_bet == amt)
            affordable = (player.money >= amt)
            bg = (50, 160, 80) if selected else ((40, 100, 60) if affordable else (60, 60, 60))
            pygame.draw.rect(self.screen, bg, rect, border_radius=5)
            pygame.draw.rect(self.screen, (200, 230, 180) if selected else (100, 160, 120), rect, 1, border_radius=5)
            lbl2 = self.font.render(f"{amt}g", True, (240, 230, 180) if affordable else (130, 130, 130))
            self.screen.blit(lbl2, (bx + btn_w // 2 - lbl2.get_width() // 2, by + btn_h // 2 - lbl2.get_height() // 2))
            self._gamble_rects[("bet", amt)] = rect

        # Bots info
        bots_txt = small.render(f"Opponents: {', '.join(self._gamble_bot_names)}", True, (170, 200, 160))
        self.screen.blit(bots_txt, (px + pw // 2 - bots_txt.get_width() // 2, py + 175))

        # Play button
        can_play = player.money >= self._gamble_bet
        play_rect = pygame.Rect(px + pw // 2 - 70, py + ph - 100, 140, 40)
        pygame.draw.rect(self.screen, (60, 140, 80) if can_play else (60, 60, 60), play_rect, border_radius=6)
        pygame.draw.rect(self.screen, (180, 220, 160), play_rect, 1, border_radius=6)
        play_lbl = self.font.render("Play", True, (240, 240, 200) if can_play else (130, 130, 130))
        self.screen.blit(play_lbl, (play_rect.centerx - play_lbl.get_width() // 2, play_rect.centery - play_lbl.get_height() // 2))
        self._gamble_rects["play"] = play_rect

        close_rect = pygame.Rect(px + pw // 2 - 50, py + ph - 48, 100, 32)
        pygame.draw.rect(self.screen, (80, 40, 40), close_rect, border_radius=5)
        pygame.draw.rect(self.screen, (180, 120, 120), close_rect, 1, border_radius=5)
        close_lbl = self.small.render("Leave", True, (220, 180, 180))
        self.screen.blit(close_lbl, (close_rect.centerx - close_lbl.get_width() // 2, close_rect.centery - close_lbl.get_height() // 2))
        self._gamble_rects["close"] = close_rect

    def _draw_gamble_pick(self, player, px, py, pw, ph):
        self._gamble_rects = {}
        small = self.small

        lbl = self.font.render(f"Bet: {self._gamble_bet}g — Pick a number (2–12):", True, (230, 210, 140))
        self.screen.blit(lbl, (px + pw // 2 - lbl.get_width() // 2, py + 50))

        nums = list(range(2, 13))
        btn_w, btn_h = 40, 40
        cols = 6
        row_gap = 48
        for i, n in enumerate(nums):
            col = i % cols
            row = i // cols
            bx = px + pw // 2 - (cols * (btn_w + 8)) // 2 + col * (btn_w + 8)
            by = py + 100 + row * row_gap
            rect = pygame.Rect(bx, by, btn_w, btn_h)
            sel = (self._gamble_player_pick == n)
            pygame.draw.rect(self.screen, (50, 150, 80) if sel else (30, 90, 50), rect, border_radius=5)
            pygame.draw.rect(self.screen, (180, 230, 160) if sel else (80, 140, 100), rect, 1, border_radius=5)
            num_lbl = self.font.render(str(n), True, (250, 240, 200))
            self.screen.blit(num_lbl, (rect.centerx - num_lbl.get_width() // 2, rect.centery - num_lbl.get_height() // 2))
            self._gamble_rects[("pick", n)] = rect

        # Show probability hint
        prob_hint = small.render("(7 is most likely on 2d6)", True, (150, 190, 150))
        self.screen.blit(prob_hint, (px + pw // 2 - prob_hint.get_width() // 2, py + 215))

        roll_rect = pygame.Rect(px + pw // 2 - 70, py + ph - 100, 140, 40)
        can_roll = self._gamble_player_pick is not None
        pygame.draw.rect(self.screen, (60, 140, 80) if can_roll else (50, 70, 55), roll_rect, border_radius=6)
        pygame.draw.rect(self.screen, (180, 220, 160), roll_rect, 1, border_radius=6)
        roll_lbl = self.font.render("Roll!", True, (240, 240, 200) if can_roll else (130, 130, 130))
        self.screen.blit(roll_lbl, (roll_rect.centerx - roll_lbl.get_width() // 2, roll_rect.centery - roll_lbl.get_height() // 2))
        self._gamble_rects["roll"] = roll_rect

        back_rect = pygame.Rect(px + pw // 2 - 50, py + ph - 48, 100, 32)
        pygame.draw.rect(self.screen, (80, 40, 40), back_rect, border_radius=5)
        pygame.draw.rect(self.screen, (180, 120, 120), back_rect, 1, border_radius=5)
        back_lbl = self.small.render("Back", True, (220, 180, 180))
        self.screen.blit(back_lbl, (back_rect.centerx - back_lbl.get_width() // 2, back_rect.centery - back_lbl.get_height() // 2))
        self._gamble_rects["back"] = back_rect

    def _draw_gamble_rolling(self, player, dt, px, py, pw, ph):
        self._gamble_roll_timer += dt
        # Animate dice
        if self._gamble_roll_timer < 0.5:
            self._gamble_die1 = random.randint(1, 6)
            self._gamble_die2 = random.randint(1, 6)
        elif self._gamble_roll_result is None:
            self._compute_gamble_result(player)

        die_size = 56
        total_dice_w = die_size * 2 + 20
        dx = px + pw // 2 - total_dice_w // 2
        dy = py + ph // 2 - die_size // 2 - 10

        _draw_die_face(self.screen, dx, dy, die_size, self._gamble_die1)
        _draw_die_face(self.screen, dx + die_size + 20, dy, die_size, self._gamble_die2)

        rolling_lbl = self.font.render("Rolling...", True, (230, 210, 140))
        self.screen.blit(rolling_lbl, (px + pw // 2 - rolling_lbl.get_width() // 2, py + 50))

        if self._gamble_roll_result is not None:
            total_lbl = self.font.render(f"= {self._gamble_roll_result}", True, (250, 240, 180))
            self.screen.blit(total_lbl, (px + pw // 2 - total_lbl.get_width() // 2, dy + die_size + 12))
            if self._gamble_roll_timer >= 0.9:
                self._gamble_phase = "result"

    def _compute_gamble_result(self, player):
        self._gamble_die1 = random.randint(1, 6)
        self._gamble_die2 = random.randint(1, 6)
        roll = self._gamble_die1 + self._gamble_die2
        self._gamble_roll_result = roll

        # Generate bot picks
        self._gamble_bot_picks = []
        for _ in self._gamble_bot_names:
            base = random.choices(range(2, 13), weights=[1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1])[0]
            noise = random.randint(-1, 1)
            self._gamble_bot_picks.append(max(2, min(12, base + noise)))

        player_dist = abs(self._gamble_player_pick - roll)
        bot_dists = [abs(p - roll) for p in self._gamble_bot_picks]
        all_dists = [player_dist] + bot_dists
        best = min(all_dists)

        winners = []
        if player_dist == best:
            winners.append("You")
        for i, d in enumerate(bot_dists):
            if d == best:
                winners.append(self._gamble_bot_names[i])

        pot = (self._gamble_num_bots + 1) * self._gamble_bet

        if "You" in winners and len(winners) == 1:
            net = self._gamble_num_bots * self._gamble_bet
            self._gamble_result_msg = f"You win! +{net}g"
            self._gamble_net_gold = net
        elif "You" in winners:
            share = pot // len(winners)
            net = share - self._gamble_bet
            sign = "+" if net >= 0 else ""
            self._gamble_result_msg = f"Tie! {sign}{net}g"
            self._gamble_net_gold = net
        else:
            self._gamble_result_msg = f"You lose! -{self._gamble_bet}g"
            self._gamble_net_gold = -self._gamble_bet

        player.money = max(0, player.money + self._gamble_net_gold)

    def _draw_gamble_result(self, player, px, py, pw, ph):
        self._gamble_rects = {}

        roll = self._gamble_roll_result
        die_size = 44
        dx = px + pw // 2 - (die_size * 2 + 20) // 2
        dy = py + 50

        _draw_die_face(self.screen, dx, dy, die_size, self._gamble_die1)
        _draw_die_face(self.screen, dx + die_size + 20, dy, die_size, self._gamble_die2)

        roll_lbl = self.font.render(f"Roll: {roll}", True, (250, 240, 180))
        self.screen.blit(roll_lbl, (px + pw // 2 - roll_lbl.get_width() // 2, dy + die_size + 6))

        # All picks
        y_offset = dy + die_size + 32
        you_txt = self.small.render(f"You picked: {self._gamble_player_pick}", True, (200, 230, 180))
        self.screen.blit(you_txt, (px + pw // 2 - you_txt.get_width() // 2, y_offset))
        y_offset += 22
        for name, pick in zip(self._gamble_bot_names, self._gamble_bot_picks):
            bot_txt = self.small.render(f"{name} picked: {pick}", True, (180, 210, 170))
            self.screen.blit(bot_txt, (px + pw // 2 - bot_txt.get_width() // 2, y_offset))
            y_offset += 20

        # Result message
        won = self._gamble_net_gold > 0
        tied_zero = self._gamble_net_gold == 0
        color = (120, 240, 120) if won else ((230, 230, 120) if tied_zero else (240, 100, 100))
        res_lbl = self.font.render(self._gamble_result_msg, True, color)
        self.screen.blit(res_lbl, (px + pw // 2 - res_lbl.get_width() // 2, y_offset + 8))

        gold_txt = self.small.render(f"Gold: {player.money}", True, (230, 210, 140))
        self.screen.blit(gold_txt, (px + pw // 2 - gold_txt.get_width() // 2, y_offset + 34))

        # Play Again
        again_rect = pygame.Rect(px + pw // 2 - 120, py + ph - 100, 110, 38)
        pygame.draw.rect(self.screen, (50, 130, 70), again_rect, border_radius=6)
        pygame.draw.rect(self.screen, (160, 220, 150), again_rect, 1, border_radius=6)
        again_lbl = self.font.render("Play Again", True, (240, 240, 200))
        self.screen.blit(again_lbl, (again_rect.centerx - again_lbl.get_width() // 2, again_rect.centery - again_lbl.get_height() // 2))
        self._gamble_rects["again"] = again_rect

        # Leave
        leave_rect = pygame.Rect(px + pw // 2 + 10, py + ph - 100, 110, 38)
        pygame.draw.rect(self.screen, (80, 40, 40), leave_rect, border_radius=6)
        pygame.draw.rect(self.screen, (180, 120, 120), leave_rect, 1, border_radius=6)
        leave_lbl = self.font.render("Leave", True, (230, 190, 190))
        self.screen.blit(leave_lbl, (leave_rect.centerx - leave_lbl.get_width() // 2, leave_rect.centery - leave_lbl.get_height() // 2))
        self._gamble_rects["leave"] = leave_rect

    def handle_gambling_click(self, pos, player):
        phase = self._gamble_phase
        for key, rect in self._gamble_rects.items():
            if not rect.collidepoint(pos):
                continue
            if phase == "bet":
                if isinstance(key, tuple) and key[0] == "bet":
                    amt = key[1]
                    if player.money >= amt:
                        self._gamble_bet = amt
                elif key == "play":
                    if player.money >= self._gamble_bet:
                        self._gamble_phase = "pick"
                        self._gamble_rects = {}
                elif key == "close":
                    self.gambling_open = False
            elif phase == "pick":
                if isinstance(key, tuple) and key[0] == "pick":
                    self._gamble_player_pick = key[1]
                elif key == "roll":
                    if self._gamble_player_pick is not None:
                        self._gamble_phase = "rolling"
                        self._gamble_roll_timer = 0.0
                        self._gamble_roll_result = None
                        self._gamble_rects = {}
                elif key == "back":
                    self._gamble_phase = "bet"
                    self._gamble_rects = {}
            elif phase == "result":
                if key == "again":
                    self._gamble_phase = "bet"
                    self._gamble_player_pick = None
                    self._gamble_roll_result = None
                    self._gamble_rects = {}
                elif key == "leave":
                    self.gambling_open = False
            break

    def handle_gambling_keydown(self, key, player):
        if key == pygame.K_ESCAPE:
            if self._gamble_phase == "pick":
                self._gamble_phase = "bet"
                self._gamble_rects = {}
            else:
                self.gambling_open = False
