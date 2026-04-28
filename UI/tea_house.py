import pygame
from constants import SCREEN_W, SCREEN_H
from tea_house import (
    calculate_tip, get_conversation, ALL_TEA_ITEM_IDS, _base_type_from_item,
)
from items import ITEMS

_BG       = ( 18,  22,  18)
_PANEL    = ( 26,  32,  26)
_BORDER   = ( 75, 115,  65)
_TITLE_C  = (160, 220, 140)
_LABEL_C  = (120, 175, 100)
_DIM_C    = ( 60,  90,  50)
_HINT_C   = ( 80, 120,  70)
_SEL_BG   = ( 38,  58,  30)
_SEL_BORD = (110, 180,  80)
_TIP_C    = (220, 200,  80)
_CONV_C   = (210, 210, 195)
_WHITE    = (240, 240, 230)
_CLOSE_C  = (160,  70,  55)


class TeaHouseMixin:

    def open_tea_house(self):
        self.tea_house_open = True
        self._th_phase = "serve"   # "serve" | "result"
        self._th_selected_visitor = None
        self._th_selected_tea = None
        self._th_result = None
        self._th_visitor_rects = []
        self._th_tea_rects = {}
        self._th_serve_btn = None
        self._th_close_btn = None

    def _draw_tea_house(self, player, world, dt=0.0):
        from towns import TOWNS

        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        PW, PH = 700, 430
        px = (SCREEN_W - PW) // 2
        py = (SCREEN_H - PH) // 2

        pygame.draw.rect(self.screen, _BG,     (px, py, PW, PH), border_radius=6)
        pygame.draw.rect(self.screen, _BORDER, (px, py, PW, PH), 2, border_radius=6)

        title = self.font.render("TEA HOUSE", True, _TITLE_C)
        self.screen.blit(title, (px + PW // 2 - title.get_width() // 2, py + 8))

        hint = self.small.render("ESC to close", True, _HINT_C)
        self.screen.blit(hint, (px + PW - hint.get_width() - 8, py + 10))

        if self._th_phase == "result":
            self._draw_th_result(px, py, PW, PH)
            return

        # Divider
        mid_x = px + 310
        pygame.draw.line(self.screen, _BORDER, (mid_x, py + 36), (mid_x, py + PH - 12), 1)

        self._draw_th_visitors(px, py, PW, PH, world, player)
        self._draw_th_teas(px, py, PW, PH, mid_x, player)
        self._draw_th_serve_btn(px, py, PW, PH, player, world)

    def _draw_th_visitors(self, px, py, PW, PH, world, player):
        lx = px + 12
        self._th_visitor_rects.clear()

        lbl = self.small.render("WAITING VISITORS", True, _LABEL_C)
        self.screen.blit(lbl, (lx, py + 40))

        waiting = [v for v in getattr(world, "tea_house_visitors", []) if v.state == "waiting"]

        if not waiting:
            msg = self.small.render("No visitors yet — build reputation nearby.", True, _DIM_C)
            self.screen.blit(msg, (lx, py + 64))
            return

        ROW_H = 66
        for i, visitor in enumerate(waiting[:4]):
            ry = py + 56 + i * (ROW_H + 6)
            rw = 286
            is_sel = self._th_selected_visitor == i
            bg = _SEL_BG if is_sel else _PANEL
            bord = _SEL_BORD if is_sel else _BORDER
            rect = pygame.Rect(lx, ry, rw, ROW_H)
            pygame.draw.rect(self.screen, bg, rect, border_radius=4)
            pygame.draw.rect(self.screen, bord, rect, 1, border_radius=4)
            self._th_visitor_rects.append(rect)

            name_surf = self.font.render(visitor.display_name, True, _WHITE)
            self.screen.blit(name_surf, (lx + 8, ry + 6))

            arch_surf = self.small.render(visitor.archetype.capitalize(), True, _LABEL_C)
            self.screen.blit(arch_surf, (lx + 8, ry + 26))

            hint_surf = self.small.render(visitor.pref_hint, True, _DIM_C)
            self.screen.blit(hint_surf, (lx + 8, ry + 42))

            if is_sel and self._th_selected_tea:
                tip_val = calculate_tip(visitor, self._th_selected_tea, _nearest_rep(world, player))
                tip_surf = self.small.render(f"~{tip_val} coins", True, _TIP_C)
                self.screen.blit(tip_surf, (lx + rw - tip_surf.get_width() - 8, ry + 6))

    def _draw_th_teas(self, px, py, PW, PH, mid_x, player):
        rx = mid_x + 12
        self._th_tea_rects.clear()

        lbl = self.small.render("YOUR BREWED TEAS", True, _LABEL_C)
        self.screen.blit(lbl, (rx, py + 40))

        teas = [(iid, cnt) for iid, cnt in player.inventory.items()
                if iid in ALL_TEA_ITEM_IDS and cnt > 0]

        if not teas:
            msg = self.small.render("No brewed tea in inventory.", True, _DIM_C)
            self.screen.blit(msg, (rx, py + 64))
            return

        ROW_H = 38
        rw = PW - (mid_x - px) - 24
        for i, (iid, cnt) in enumerate(teas[:8]):
            ry = py + 56 + i * (ROW_H + 4)
            is_sel = self._th_selected_tea == iid
            bg = _SEL_BG if is_sel else _PANEL
            bord = _SEL_BORD if is_sel else _BORDER
            rect = pygame.Rect(rx, ry, rw, ROW_H)
            pygame.draw.rect(self.screen, bg, rect, border_radius=4)
            pygame.draw.rect(self.screen, bord, rect, 1, border_radius=4)
            self._th_tea_rects[iid] = rect

            item_name = ITEMS.get(iid, {}).get("name", iid)
            name_surf = self.small.render(item_name, True, _WHITE)
            self.screen.blit(name_surf, (rx + 8, ry + ROW_H // 2 - name_surf.get_height() // 2))

            cnt_surf = self.small.render(f"×{cnt}", True, _DIM_C)
            self.screen.blit(cnt_surf, (rx + rw - cnt_surf.get_width() - 8,
                                        ry + ROW_H // 2 - cnt_surf.get_height() // 2))

    def _draw_th_serve_btn(self, px, py, PW, PH, player, world):
        can_serve = (self._th_selected_visitor is not None and
                     self._th_selected_tea is not None)

        bw, bh = 160, 36
        bx = px + PW // 2 - bw // 2
        by = py + PH - bh - 12
        col = _SEL_BORD if can_serve else _DIM_C
        pygame.draw.rect(self.screen, _PANEL, (bx, by, bw, bh), border_radius=4)
        pygame.draw.rect(self.screen, col, (bx, by, bw, bh), 2, border_radius=4)
        lbl = self.font.render("Serve Tea", True, col)
        self.screen.blit(lbl, (bx + bw // 2 - lbl.get_width() // 2,
                                by + bh // 2 - lbl.get_height() // 2))
        self._th_serve_btn = pygame.Rect(bx, by, bw, bh)

    def _draw_th_result(self, px, py, PW, PH):
        r = self._th_result
        if not r:
            return

        name_surf = self.font.render(r["name"], True, _TITLE_C)
        self.screen.blit(name_surf, (px + PW // 2 - name_surf.get_width() // 2, py + 44))

        y = py + 84
        for line in r["conversation"]:
            lsurf = self.small.render(line, True, _CONV_C)
            self.screen.blit(lsurf, (px + 28, y))
            y += lsurf.get_height() + 4

        y += 16
        tip_lbl = self.font.render(f"{r['name']} tips you {r['tip']} coins.", True, _TIP_C)
        self.screen.blit(tip_lbl, (px + PW // 2 - tip_lbl.get_width() // 2, y))

        bw, bh = 160, 36
        bx = px + PW // 2 - bw // 2
        by = py + PH - bh - 16
        pygame.draw.rect(self.screen, _PANEL, (bx, by, bw, bh), border_radius=4)
        pygame.draw.rect(self.screen, _SEL_BORD, (bx, by, bw, bh), 2, border_radius=4)
        lbl = self.font.render("Continue", True, _SEL_BORD)
        self.screen.blit(lbl, (bx + bw // 2 - lbl.get_width() // 2,
                                by + bh // 2 - lbl.get_height() // 2))
        self._th_serve_btn = pygame.Rect(bx, by, bw, bh)

    def handle_tea_house_click(self, pos, player, world):
        if self._th_phase == "result":
            if self._th_serve_btn and self._th_serve_btn.collidepoint(pos):
                self._th_phase = "serve"
                self._th_result = None
                self._th_selected_visitor = None
                self._th_selected_tea = None
            return

        for i, rect in enumerate(self._th_visitor_rects):
            if rect.collidepoint(pos):
                self._th_selected_visitor = i
                return

        for iid, rect in self._th_tea_rects.items():
            if rect.collidepoint(pos):
                self._th_selected_tea = iid
                return

        if (self._th_serve_btn and self._th_serve_btn.collidepoint(pos) and
                self._th_selected_visitor is not None and self._th_selected_tea is not None):
            self._do_serve(player, world)

    def _do_serve(self, player, world):
        waiting = [v for v in getattr(world, "tea_house_visitors", []) if v.state == "waiting"]
        if self._th_selected_visitor >= len(waiting):
            return
        visitor = waiting[self._th_selected_visitor]

        iid = self._th_selected_tea
        if player.inventory.get(iid, 0) <= 0:
            return

        player.inventory[iid] -= 1
        if player.inventory[iid] == 0:
            del player.inventory[iid]
            # Remove from hotbar if present
            for slot_i, slot_item in enumerate(player.hotbar):
                if slot_item == iid:
                    player.hotbar[slot_i] = None
                    player.hotbar_uses[slot_i] = None
                    break

        rep = _nearest_rep(world, player)
        tip = calculate_tip(visitor, iid, rep)
        player.money += tip

        conversation = get_conversation(visitor.archetype, rep)

        visitor.state = "served"

        self._th_result = {
            "name": visitor.display_name,
            "conversation": conversation,
            "tip": tip,
        }
        self._th_phase = "result"


def _nearest_rep(world, player=None):
    from towns import TOWNS
    from constants import BLOCK_SIZE
    centers = getattr(world, "town_centers", [])
    if not centers:
        return 0
    if player is not None and getattr(player, "tea_house_pos", None):
        ref_bx = player.tea_house_pos[0]
    else:
        ref_bx = centers[0]
    tid = min(range(len(centers)), key=lambda i: abs(centers[i] - ref_bx))
    town = TOWNS.get(tid)
    return town.reputation if town else 0
