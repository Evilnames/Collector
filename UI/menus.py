import pygame
from ._data import _MUSHROOM_NAMES
from constants import SCREEN_W, SCREEN_H


class MenusMixin:

    _RARITY_COLORS = {
        "common":    (140, 140, 140),
        "uncommon":  (50,  180,  50),
        "rare":      (60,  100, 220),
        "epic":      (150,  50, 220),
        "legendary": (240, 180,   0),
    }

    def _draw_pause_menu(self):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        PW, PH = 360, 320
        px = (SCREEN_W - PW) // 2
        py = (SCREEN_H - PH) // 2
        pygame.draw.rect(self.screen, (12, 20, 60), (px, py, PW, PH), border_radius=12)
        pygame.draw.rect(self.screen, (55, 130, 255), (px, py, PW, PH), 2, border_radius=12)

        title = self._pause_font.render("PAUSED", True, (255, 255, 255))
        self.screen.blit(title, title.get_rect(center=(SCREEN_W // 2, py + 60)))

        BTN_W, BTN_H = 260, 52
        bx = SCREEN_W // 2 - BTN_W // 2
        btn_labels = [("resume", "RESUME"), ("save", "SAVE"), ("quit", "SAVE & QUIT")]
        btn_y_start = py + 120
        btn_gap = 66
        mx, my = pygame.mouse.get_pos()
        self._pause_btn_rects = {}
        for i, (key, label) in enumerate(btn_labels):
            rect = pygame.Rect(bx, btn_y_start + i * btn_gap, BTN_W, BTN_H)
            self._pause_btn_rects[key] = rect
            hovered = rect.collidepoint(mx, my)
            color = (40, 100, 240) if hovered else (20, 60, 160)
            pygame.draw.rect(self.screen, color, rect, border_radius=8)
            pygame.draw.rect(self.screen, (55, 130, 255), rect, 2, border_radius=8)
            lbl = self._pause_font2.render(label, True, (255, 255, 255))
            self.screen.blit(lbl, lbl.get_rect(center=rect.center))

    def handle_pause_click(self, pos):
        for key, rect in self._pause_btn_rects.items():
            if rect.collidepoint(pos):
                return key
        return None

    def _draw_death_screen(self, player):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))

        txt = self._death_font.render("YOU DIED", True, (220, 40, 40))
        self.screen.blit(txt, txt.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 - 70)))

        sub = self._death_font2.render("All items were dropped at your location.", True, (200, 180, 180))
        self.screen.blit(sub, sub.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2)))

        spawn_label = "Respawn at: Bed" if player.spawn_x is not None else "Respawn at: World Spawn"
        spawn_txt = self._death_font2.render(spawn_label, True, (150, 210, 150))
        self.screen.blit(spawn_txt, spawn_txt.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + 40)))

        key_txt = self._death_font2.render("Press SPACE or ENTER to respawn", True, (180, 180, 220))
        self.screen.blit(key_txt, key_txt.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + 90)))

    def _draw_cheat_console(self):
        W = SCREEN_W
        pygame.draw.rect(self.screen, (15, 14, 25), (0, 0, W, 40))
        pygame.draw.rect(self.screen, (60, 200, 80), (0, 0, W, 40), 1)

        cursor = "_" if int(pygame.time.get_ticks() / 500) % 2 == 0 else ""
        prompt = self._cheat_font.render("> " + self.cheat_text + cursor, True, (80, 255, 100))
        self.screen.blit(prompt, (10, 10))

        if self.cheat_message and self._cheat_msg_timer > 0:
            msg_col = (255, 80, 80) if self.cheat_message.startswith("!") else (200, 230, 100)
            msg = self._cheat_font.render(self.cheat_message.lstrip("!"), True, msg_col)
            self.screen.blit(msg, (W - msg.get_width() - 10, 10))

    def _drain_notifications(self, player):
        while getattr(player, "pending_notifications", None):
            category, name_or_bid, rarity = player.pending_notifications.pop(0)
            if category == "Mushroom":
                display = _MUSHROOM_NAMES.get(name_or_bid, "Mushroom")
                color = (200, 170, 110)
            elif category == "Bird":
                display = name_or_bid
                rarity_bird_cols = {"common": (120, 190, 120), "uncommon": (100, 170, 220), "rare": (180, 120, 230)}
                color = rarity_bird_cols.get(rarity, (140, 210, 255))
            elif category == "Achievement":
                display = name_or_bid
                color = (255, 215, 80)
            else:
                display = name_or_bid
                color = self._RARITY_COLORS.get(rarity, (200, 200, 200))
            duration = 5.0 if category == "Achievement" else 3.5
            if len(self._toasts) < 6:
                self._toasts.append({
                    "category": category,
                    "name": display,
                    "color": color,
                    "timer": duration,
                    "total": duration,
                })

    def _draw_toasts(self, dt):
        self._toasts = [t for t in self._toasts if t["timer"] > 0]
        if not self._toasts:
            return

        tw, th = 200, 44
        margin = 12
        gap = 5

        for i, toast in enumerate(self._toasts):
            toast["timer"] -= dt
            remaining = toast["timer"]
            elapsed = toast["total"] - remaining
            if elapsed < 0.15:
                alpha = int(255 * elapsed / 0.15)
            elif remaining < 0.5:
                alpha = int(255 * max(0.0, remaining) / 0.5)
            else:
                alpha = 255

            x = SCREEN_W - tw - margin
            y = SCREEN_H - margin - th - i * (th + gap)

            surf = pygame.Surface((tw, th), pygame.SRCALPHA)
            surf.fill((18, 18, 18, int(210 * alpha / 255)))

            rc = toast["color"]
            pygame.draw.rect(surf, (*rc, alpha), (0, 0, 4, th))

            cat_surf = self._toast_font.render(toast["category"], True, (160, 160, 160))
            cat_surf.set_alpha(alpha)
            surf.blit(cat_surf, (10, 4))

            name_surf = self._toast_font.render(toast["name"], True, rc)
            name_surf.set_alpha(alpha)
            surf.blit(name_surf, (10, 22))

            self.screen.blit(surf, (x, y))
