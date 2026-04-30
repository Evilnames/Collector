import pygame
import hashlib
from constants import SCREEN_W, SCREEN_H
from jewelry import JEWELRY_TYPES, JEWELRY_TYPE_ORDER, calculate_value

_GOLD = (220, 180, 60)
_DARK = (18, 14, 8)
_BG   = (28, 22, 12)


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def _gem_color(gem):
    return gem.primary_color


def _rock_color(rock):
    return rock.primary_color


def _item_label(kind, obj):
    if kind == "gem":
        return f"{obj.gem_type.replace('_',' ').title()} ({obj.rarity[:3].upper()})"
    if kind == "pearl":
        return f"{obj.color_name.title()} Pearl ({obj.rarity[:3].upper()})"
    return f"{obj.base_type.replace('_',' ').title()} ({obj.rarity[:3].upper()})"


def _item_color(kind, obj):
    if kind == "gem":
        return _gem_color(obj)
    if kind == "pearl":
        return obj.color
    return _rock_color(obj)


# ---------------------------------------------------------------------------
# Jewelry shape helpers
# ---------------------------------------------------------------------------

def _slot_positions(jtype, n, cx, cy, radius=80):
    """Return list of (x, y) pixel centres for n slots arranged around the piece."""
    import math
    if jtype == "ring":
        # Arc of a circle
        angles = [math.pi * 0.75 + i * (math.pi * 1.5 / max(n - 1, 1)) for i in range(n)]
        return [(int(cx + radius * 0.8 * math.cos(a)), int(cy + radius * 0.8 * math.sin(a))) for a in angles]
    if jtype == "necklace":
        # Gentle arc across the top
        spread = min(160, n * 45)
        angles = [math.pi + math.radians(180 - spread // 2 + i * spread // max(n - 1, 1)) for i in range(n)]
        return [(int(cx + (radius + 10) * math.cos(a)), int(cy + (radius + 10) * math.sin(a))) for a in angles]
    if jtype == "bracelet":
        angles = [2 * math.pi * i / n for i in range(n)]
        return [(int(cx + radius * 0.7 * math.cos(a)), int(cy + radius * 0.7 * math.sin(a))) for a in angles]
    if jtype == "pendant":
        # Stacked vertically
        step = 50
        return [(cx, cy - (n - 1) * step // 2 + i * step) for i in range(n)]
    if jtype == "crown":
        # Spread horizontally
        total_w = (n - 1) * 60
        return [(cx - total_w // 2 + i * 60, cy - 20) for i in range(n)]
    return [(cx + i * 50, cy) for i in range(n)]


# ---------------------------------------------------------------------------
# JewelryMixin
# ---------------------------------------------------------------------------

class JewelryMixin:

    # ------------------------------------------------------------------ #
    #  Workbench: main draw dispatcher                                    #
    # ------------------------------------------------------------------ #

    def _draw_jewelry_workbench(self, player, dt=0.0):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 215))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render("JEWELRY WORKBENCH", True, _GOLD)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 6))

        hint = self.small.render("ESC to close", True, (100, 85, 45))
        self.screen.blit(hint, (SCREEN_W - hint.get_width() - 8, 6))

        phase = self._jw_phase
        if phase in ("idle", "type_select"):
            self._draw_jw_type_select(player)
        elif phase == "slot_select":
            self._draw_jw_slot_select(player)
        elif phase == "design":
            self._draw_jw_design(player)
        elif phase == "name_confirm":
            self._draw_jw_name_confirm(player)

        # Draw drag ghost on top
        if self._jw_drag_uid is not None:
            self._draw_jw_drag_ghost(player)

    # ------------------------------------------------------------------ #
    #  Phase 1 — type select                                              #
    # ------------------------------------------------------------------ #

    def _draw_jw_type_select(self, player):
        sub = self.small.render("Choose what to make:", True, (180, 150, 70))
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 34))

        CARD_W, CARD_H, GAP = 190, 130, 18
        total_w = len(JEWELRY_TYPES) * CARD_W + (len(JEWELRY_TYPES) - 1) * GAP
        gx0 = (SCREEN_W - total_w) // 2
        cy = SCREEN_H // 2 - CARD_H // 2

        self._jw_type_rects.clear()
        for i, (jkey, jdata) in enumerate(JEWELRY_TYPES.items()):
            rx = gx0 + i * (CARD_W + GAP)
            rect = pygame.Rect(rx, cy, CARD_W, CARD_H)
            self._jw_type_rects[jkey] = rect
            hov = rect.collidepoint(pygame.mouse.get_pos())
            bg  = (45, 35, 15) if hov else (30, 22, 8)
            bdr = _GOLD if hov else (140, 110, 40)
            pygame.draw.rect(self.screen, bg, rect, border_radius=6)
            pygame.draw.rect(self.screen, bdr, rect, 2, border_radius=6)

            lbl = self.font.render(jdata["label"], True, _GOLD if hov else (200, 160, 60))
            self.screen.blit(lbl, (rx + CARD_W // 2 - lbl.get_width() // 2, cy + 16))
            slots_txt = self.small.render(f"Up to {jdata['max_slots']} gem slots", True, (150, 130, 70))
            self.screen.blit(slots_txt, (rx + CARD_W // 2 - slots_txt.get_width() // 2, cy + 50))
            val_txt = self.small.render(f"Base value: {jdata['base_value']}g", True, (130, 115, 55))
            self.screen.blit(val_txt, (rx + CARD_W // 2 - val_txt.get_width() // 2, cy + 72))

            # Little icon shape
            self._draw_jw_icon(jkey, rx + CARD_W // 2, cy + CARD_H - 24, 10)

    # ------------------------------------------------------------------ #
    #  Phase 2 — slot count                                               #
    # ------------------------------------------------------------------ #

    def _draw_jw_slot_select(self, player):
        jtype = self._jw_type
        jdata = JEWELRY_TYPES[jtype]
        sub = self.small.render(f"How many gem slots for your {jdata['label']}?", True, (180, 150, 70))
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 34))

        MAX = jdata["max_slots"]
        BTN_W, BTN_H, GAP = 80, 80, 16
        total_w = MAX * BTN_W + (MAX - 1) * GAP
        gx0 = (SCREEN_W - total_w) // 2
        cy = SCREEN_H // 2 - BTN_H // 2

        self._jw_slot_count_rects.clear()
        for n in range(1, MAX + 1):
            rx = gx0 + (n - 1) * (BTN_W + GAP)
            rect = pygame.Rect(rx, cy, BTN_W, BTN_H)
            self._jw_slot_count_rects[n] = rect
            selected = (n == self._jw_slot_count)
            bg  = (55, 42, 14) if selected else (30, 22, 8)
            bdr = _GOLD if selected else (120, 95, 35)
            pygame.draw.rect(self.screen, bg, rect, border_radius=6)
            pygame.draw.rect(self.screen, bdr, rect, 2, border_radius=6)
            num = self.font.render(str(n), True, _GOLD if selected else (180, 145, 55))
            self.screen.blit(num, (rx + BTN_W // 2 - num.get_width() // 2, cy + 12))
            s_lbl = self.small.render("slot" if n == 1 else "slots", True, (140, 115, 50))
            self.screen.blit(s_lbl, (rx + BTN_W // 2 - s_lbl.get_width() // 2, cy + 46))

        # Confirm button
        conf_rect = pygame.Rect(SCREEN_W // 2 - 90, cy + BTN_H + 30, 180, 44)
        self._jw_confirm_rect = conf_rect
        pygame.draw.rect(self.screen, (45, 35, 12), conf_rect, border_radius=6)
        pygame.draw.rect(self.screen, _GOLD, conf_rect, 2, border_radius=6)
        conf_lbl = self.font.render("Next →", True, _GOLD)
        self.screen.blit(conf_lbl, (conf_rect.centerx - conf_lbl.get_width() // 2,
                                    conf_rect.centery - conf_lbl.get_height() // 2))

    # ------------------------------------------------------------------ #
    #  Phase 3 — design (drag-and-drop)                                   #
    # ------------------------------------------------------------------ #

    def _draw_jw_design(self, player):
        # Left panel: gem + rock picker
        PANEL_W = 310
        PANEL_H = SCREEN_H - 80
        px = 20
        py = 50
        pygame.draw.rect(self.screen, (25, 20, 10), (px, py, PANEL_W, PANEL_H))
        pygame.draw.rect(self.screen, (120, 95, 35), (px, py, PANEL_W, PANEL_H), 1)

        lbl = self.small.render("Your Gems, Rocks & Pearls  (drag to slots →)", True, (170, 140, 55))
        self.screen.blit(lbl, (px + 8, py + 6))

        # Build combined list excluding already-slotted uids
        slotted_uids = {s["uid"] for s in self._jw_slots if s is not None}
        items = [(g.uid, "gem", g) for g in player.gems if g.uid not in slotted_uids]
        items += [(r.uid, "rock", r) for r in player.rocks if r.uid not in slotted_uids]
        items += [(p.uid, "pearl", p) for p in getattr(player, "pearls", []) if p.uid not in slotted_uids]

        CELL_W, CELL_H, GAP, COLS = 140, 40, 4, 2
        visible_h = PANEL_H - 30
        max_rows = (visible_h + GAP) // (CELL_H + GAP)
        max_visible = max_rows * COLS

        scroll = max(0, min(self._jw_gem_scroll, max(0, (len(items) - max_visible + COLS - 1) // COLS)))
        self._jw_gem_scroll = scroll
        start = scroll * COLS

        self._jw_gem_rects.clear()
        for li, (uid, kind, obj) in enumerate(items[start:start + max_visible]):
            col_i = li % COLS
            row_i = li // COLS
            rx = px + 6 + col_i * (CELL_W + GAP)
            ry = py + 26 + row_i * (CELL_H + GAP)
            rect = pygame.Rect(rx, ry, CELL_W, CELL_H)
            self._jw_gem_rects[uid] = (rect, kind, obj)
            dragging = (self._jw_drag_uid == uid)
            bg = (50, 40, 18) if dragging else (35, 28, 10)
            bdr = _item_color(kind, obj)
            pygame.draw.rect(self.screen, bg, rect, border_radius=3)
            pygame.draw.rect(self.screen, bdr, rect, 1, border_radius=3)
            # Color dot
            pygame.draw.circle(self.screen, bdr, (rx + 14, ry + CELL_H // 2), 7)
            nm = self.small.render(_item_label(kind, obj), True, (200, 175, 100))
            self.screen.blit(nm, (rx + 26, ry + 4))
            kind_lbl = self.small.render(kind, True, (130, 110, 60))
            self.screen.blit(kind_lbl, (rx + 26, ry + 20))

        # Scroll arrows
        if scroll > 0:
            up_rect = pygame.Rect(px + PANEL_W - 24, py + 28, 18, 18)
            pygame.draw.rect(self.screen, (60, 50, 20), up_rect, border_radius=3)
            self.screen.blit(self.small.render("▲", True, _GOLD), (up_rect.x + 2, up_rect.y + 1))
        if start + max_visible < len(items):
            dn_rect = pygame.Rect(px + PANEL_W - 24, py + PANEL_H - 28, 18, 18)
            pygame.draw.rect(self.screen, (60, 50, 20), dn_rect, border_radius=3)
            self.screen.blit(self.small.render("▼", True, _GOLD), (dn_rect.x + 2, dn_rect.y + 1))

        # Right panel: jewelry canvas
        cx = (SCREEN_W + PANEL_W + 40) // 2
        cy_center = SCREEN_H // 2
        jtype = self._jw_type
        n = self._jw_slot_count

        positions = _slot_positions(jtype, n, cx, cy_center)
        SLOT_R = 26

        # Draw piece silhouette
        self._draw_jw_silhouette(jtype, cx, cy_center, 90)

        self._jw_slot_rects = []
        for si, (sx, sy) in enumerate(positions):
            slot_data = self._jw_slots[si] if si < len(self._jw_slots) else None
            filled = slot_data is not None
            color = _item_color(slot_data["kind"], self._get_jw_obj(slot_data, player)) if filled else (80, 65, 28)
            border = color if filled else (130, 100, 35)
            pygame.draw.circle(self.screen, (30, 24, 10) if not filled else color, (sx, sy), SLOT_R)
            pygame.draw.circle(self.screen, border, (sx, sy), SLOT_R, 2)
            slot_rect = pygame.Rect(sx - SLOT_R, sy - SLOT_R, SLOT_R * 2, SLOT_R * 2)
            self._jw_slot_rects.append(slot_rect)
            num_lbl = self.small.render(str(si + 1), True, (180, 150, 60))
            self.screen.blit(num_lbl, (sx - num_lbl.get_width() // 2, sy - num_lbl.get_height() // 2))
            if filled:
                nm = self.small.render(slot_data["uid"][:6], True, (240, 220, 150))
                self.screen.blit(nm, (sx - nm.get_width() // 2, sy + SLOT_R + 3))

        # Finish button (enabled if ≥ 1 slot filled)
        filled_count = sum(1 for s in self._jw_slots if s is not None)
        finish_rect = pygame.Rect(cx - 90, SCREEN_H - 60, 180, 40)
        self._jw_finish_rect = finish_rect
        enabled = filled_count >= 1
        bdr = _GOLD if enabled else (80, 65, 25)
        bg  = (50, 38, 12) if enabled else (28, 22, 8)
        pygame.draw.rect(self.screen, bg, finish_rect, border_radius=6)
        pygame.draw.rect(self.screen, bdr, finish_rect, 2, border_radius=6)
        f_lbl = self.font.render("Finish →", True, bdr)
        self.screen.blit(f_lbl, (finish_rect.centerx - f_lbl.get_width() // 2,
                                 finish_rect.centery - f_lbl.get_height() // 2))

        hint = self.small.render("Drag gems/rocks/pearls into slots  •  click a filled slot to clear it", True, (110, 90, 40))
        self.screen.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, SCREEN_H - 18))

    # ------------------------------------------------------------------ #
    #  Phase 4 — name + confirm                                           #
    # ------------------------------------------------------------------ #

    def _draw_jw_name_confirm(self, player):
        from jewelry import JEWELRY_TYPES as JT, calculate_value, Jewelry, make_uid
        jtype = self._jw_type
        jdata = JT[jtype]

        title2 = self.font.render("Name Your Creation", True, _GOLD)
        self.screen.blit(title2, (SCREEN_W // 2 - title2.get_width() // 2, 34))

        # Text input box
        inp_rect = pygame.Rect(SCREEN_W // 2 - 240, SCREEN_H // 2 - 130, 480, 44)
        pygame.draw.rect(self.screen, (20, 16, 6), inp_rect)
        pygame.draw.rect(self.screen, _GOLD, inp_rect, 2)
        name_txt = self.font.render(self._jw_custom_name + "|", True, (240, 210, 120))
        self.screen.blit(name_txt, (inp_rect.x + 10, inp_rect.y + 10))
        if not self._jw_custom_name:
            ph = self.small.render(f"Enter a name for your {jdata['label']}…", True, (100, 85, 40))
            self.screen.blit(ph, (inp_rect.x + 10, inp_rect.y + 14))

        # Preview
        cx = SCREEN_W // 2
        cy = SCREEN_H // 2 + 30
        self._draw_jw_silhouette(jtype, cx, cy, 70)
        positions = _slot_positions(jtype, self._jw_slot_count, cx, cy, radius=60)
        for si, (sx, sy) in enumerate(positions):
            slot_data = self._jw_slots[si] if si < len(self._jw_slots) else None
            color = _item_color(slot_data["kind"], self._get_jw_obj(slot_data, player)) if slot_data else (80, 65, 28)
            pygame.draw.circle(self.screen, color, (sx, sy), 18)
            pygame.draw.circle(self.screen, (220, 190, 80), (sx, sy), 18, 2)

        # Dummy jewelry for value estimate
        name = self._jw_custom_name or jdata["label"]
        dummy = type("J", (), {"uid": "x", "jewelry_type": jtype, "slot_count": self._jw_slot_count,
                                "slots": self._jw_slots, "custom_name": name, "seed": 0})()
        val = calculate_value(dummy, player, master_jeweler=getattr(player, "master_jeweler", False))

        val_txt = self.small.render(f"Estimated merchant value: {val} gold", True, (180, 155, 60))
        self.screen.blit(val_txt, (SCREEN_W // 2 - val_txt.get_width() // 2, SCREEN_H - 100))

        craft_rect = pygame.Rect(SCREEN_W // 2 - 100, SCREEN_H - 68, 200, 44)
        self._jw_craft_rect = craft_rect
        pygame.draw.rect(self.screen, (45, 35, 10), craft_rect, border_radius=6)
        pygame.draw.rect(self.screen, _GOLD, craft_rect, 2, border_radius=6)
        c_lbl = self.font.render("Craft Jewelry", True, _GOLD)
        self.screen.blit(c_lbl, (craft_rect.centerx - c_lbl.get_width() // 2,
                                 craft_rect.centery - c_lbl.get_height() // 2))

    # ------------------------------------------------------------------ #
    #  Drag ghost                                                         #
    # ------------------------------------------------------------------ #

    def _draw_jw_drag_ghost(self, player):
        uid = self._jw_drag_uid
        kind = self._jw_drag_kind
        mx, my = self._jw_drag_pos
        obj = self._get_jw_obj({"uid": uid, "kind": kind}, player)
        if obj is None:
            return
        color = _item_color(kind, obj)
        pygame.draw.circle(self.screen, color, (mx, my), 20, 0)
        pygame.draw.circle(self.screen, (240, 220, 120), (mx, my), 20, 2)
        nm = self.small.render(_item_label(kind, obj), True, (240, 220, 120))
        self.screen.blit(nm, (mx + 24, my - 8))

    # ------------------------------------------------------------------ #
    #  Detail viewer                                                      #
    # ------------------------------------------------------------------ #

    def _draw_jewelry_detail(self, player, jewelry=None):
        j = jewelry or self._jw_detail_jewelry
        if j is None:
            return
        PW, PH = 520, 400
        px = (SCREEN_W - PW) // 2
        py = (SCREEN_H - PH) // 2
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        pygame.draw.rect(self.screen, (22, 18, 8), (px, py, PW, PH))
        pygame.draw.rect(self.screen, _GOLD, (px, py, PW, PH), 2)

        title = self.font.render(j.custom_name, True, _GOLD)
        self.screen.blit(title, (px + PW // 2 - title.get_width() // 2, py + 10))
        type_lbl = self.small.render(JEWELRY_TYPES[j.jewelry_type]["label"], True, (160, 130, 55))
        self.screen.blit(type_lbl, (px + PW // 2 - type_lbl.get_width() // 2, py + 34))

        cx = px + PW // 2
        cy = py + PH // 2
        self._draw_jw_silhouette(j.jewelry_type, cx, cy, 70)
        positions = _slot_positions(j.jewelry_type, j.slot_count, cx, cy, radius=60)
        for si, (sx, sy) in enumerate(positions):
            slot_data = j.slots[si] if si < len(j.slots) else None
            obj = self._get_jw_obj(slot_data, player) if slot_data else None
            color = _item_color(slot_data["kind"], obj) if obj else (80, 65, 28)
            pygame.draw.circle(self.screen, color, (sx, sy), 20)
            pygame.draw.circle(self.screen, (220, 190, 80), (sx, sy), 20, 2)
            if obj:
                nm = self.small.render(_item_label(slot_data["kind"], obj), True, (230, 205, 110))
                self.screen.blit(nm, (sx - nm.get_width() // 2, sy + 24))

        val = calculate_value(j, player, master_jeweler=getattr(player, "master_jeweler", False))
        val_lbl = self.small.render(f"Value: {val} gold", True, (170, 145, 55))
        self.screen.blit(val_lbl, (px + PW // 2 - val_lbl.get_width() // 2, py + PH - 44))

        close_rect = pygame.Rect(px + PW - 90, py + PH - 36, 80, 28)
        self._jw_detail_close_rect = close_rect
        pygame.draw.rect(self.screen, (40, 30, 10), close_rect, border_radius=4)
        pygame.draw.rect(self.screen, (160, 130, 50), close_rect, 1, border_radius=4)
        cl = self.small.render("Close", True, (200, 165, 60))
        self.screen.blit(cl, (close_rect.centerx - cl.get_width() // 2, close_rect.centery - cl.get_height() // 2))

    # ------------------------------------------------------------------ #
    #  NPC sell panel                                                     #
    # ------------------------------------------------------------------ #

    def _draw_jewelry_merchant_content(self, player, npc, px, py, PW, PH):
        title = self.font.render("JEWELRY MERCHANT", True, _GOLD)
        self.screen.blit(title, (px + PW // 2 - title.get_width() // 2, py + 10))

        self._jw_sell_rects = {}
        CELL_H, GAP = 52, 6
        ry = py + 38

        # ---- Jewelry section ----
        has_jewelry = bool(player.jewelry)
        sub = self.small.render("Jewelry" if has_jewelry else "No jewelry to sell", True, (160, 135, 55))
        self.screen.blit(sub, (px + 16, ry))
        ry += 20

        for piece in player.jewelry:
            if ry + CELL_H > py + PH - 60:
                break
            rect = pygame.Rect(px + 12, ry, PW - 100, CELL_H)
            self._jw_sell_rects[piece.uid] = rect
            pygame.draw.rect(self.screen, (28, 22, 8), rect)
            pygame.draw.rect(self.screen, (140, 110, 40), rect, 1)
            nm = self.font.render(piece.custom_name, True, _GOLD)
            self.screen.blit(nm, (rect.x + 10, ry + 8))
            type_lbl = self.small.render(
                JEWELRY_TYPES[piece.jewelry_type]["label"] + f"  •  {piece.slot_count} slots",
                True, (140, 115, 50))
            self.screen.blit(type_lbl, (rect.x + 10, ry + 28))
            val = npc.appraise(piece, player)
            val_lbl = self.font.render(f"{val}g", True, (200, 175, 60))
            sell_rect = pygame.Rect(px + PW - 82, ry + 8, 68, CELL_H - 16)
            self._jw_sell_rects[piece.uid + "_btn"] = sell_rect
            pygame.draw.rect(self.screen, (45, 35, 10), sell_rect, border_radius=4)
            pygame.draw.rect(self.screen, _GOLD, sell_rect, 1, border_radius=4)
            self.screen.blit(val_lbl, (sell_rect.centerx - val_lbl.get_width() // 2,
                                       sell_rect.centery - val_lbl.get_height() // 2))
            ry += CELL_H + GAP

        # ---- Pearls section ----
        pearls = getattr(player, "pearls", [])
        ry += 6
        if ry + 20 < py + PH - 20:
            pearl_hdr = self.small.render(
                "Loose Pearls" if pearls else "No loose pearls",
                True, (180, 175, 210))
            self.screen.blit(pearl_hdr, (px + 16, ry))
            ry += 20

        PEARL_H = 34
        for pearl in pearls:
            if ry + PEARL_H > py + PH - 10:
                break
            rect = pygame.Rect(px + 12, ry, PW - 100, PEARL_H)
            pygame.draw.rect(self.screen, (22, 20, 32), rect)
            pygame.draw.rect(self.screen, pearl.color, rect, 1)
            # Color dot
            pygame.draw.circle(self.screen, pearl.color, (rect.x + 16, rect.centery), 7)
            lbl_txt = f"{pearl.color_name.title()} Pearl  •  {pearl.shape}  •  {pearl.size_mm}mm"
            lbl = self.small.render(lbl_txt, True, (210, 205, 230))
            self.screen.blit(lbl, (rect.x + 30, ry + 4))
            rar = self.small.render(pearl.rarity, True, (160, 155, 190))
            self.screen.blit(rar, (rect.x + 30, ry + 20))
            val = npc.pearl_offer(pearl)
            val_lbl = self.small.render(f"{val}g", True, (200, 175, 60))
            sell_rect = pygame.Rect(px + PW - 82, ry + 4, 68, PEARL_H - 8)
            self._jw_sell_rects["pearl_" + pearl.uid + "_btn"] = sell_rect
            pygame.draw.rect(self.screen, (35, 28, 50), sell_rect, border_radius=4)
            pygame.draw.rect(self.screen, (180, 170, 220), sell_rect, 1, border_radius=4)
            self.screen.blit(val_lbl, (sell_rect.centerx - val_lbl.get_width() // 2,
                                       sell_rect.centery - val_lbl.get_height() // 2))
            ry += PEARL_H + GAP

    # ------------------------------------------------------------------ #
    #  Click handlers                                                     #
    # ------------------------------------------------------------------ #

    def _handle_jewelry_workbench_click(self, pos, player):
        phase = self._jw_phase
        if phase in ("idle", "type_select"):
            for jkey, rect in self._jw_type_rects.items():
                if rect.collidepoint(pos):
                    self._jw_type = jkey
                    self._jw_slot_count = 1
                    self._jw_phase = "slot_select"
                    return
        elif phase == "slot_select":
            for n, rect in self._jw_slot_count_rects.items():
                if rect.collidepoint(pos):
                    self._jw_slot_count = n
                    return
            if hasattr(self, "_jw_confirm_rect") and self._jw_confirm_rect.collidepoint(pos):
                self._jw_slots = [None] * self._jw_slot_count
                self._jw_phase = "design"
                return
        elif phase == "design":
            # Click on a filled slot → clear it
            for si, slot_rect in enumerate(self._jw_slot_rects):
                if slot_rect.collidepoint(pos):
                    if si < len(self._jw_slots) and self._jw_slots[si] is not None:
                        self._jw_slots[si] = None
                        return
            # Click on finish
            if hasattr(self, "_jw_finish_rect") and self._jw_finish_rect.collidepoint(pos):
                if any(s is not None for s in self._jw_slots):
                    self._jw_custom_name = ""
                    self._jw_phase = "name_confirm"
                    return
            # Click on a gem/rock to start drag
            for uid, (rect, kind, obj) in self._jw_gem_rects.items():
                if rect.collidepoint(pos):
                    self._jw_drag_uid = uid
                    self._jw_drag_kind = kind
                    self._jw_drag_pos = pos
                    return
        elif phase == "name_confirm":
            if hasattr(self, "_jw_craft_rect") and self._jw_craft_rect.collidepoint(pos):
                self._do_craft_jewelry(player)
                return

    def _handle_jewelry_drop(self, pos, player):
        uid = self._jw_drag_uid
        kind = self._jw_drag_kind
        self._jw_drag_uid = None
        self._jw_drag_kind = None
        if uid is None:
            return
        for si, slot_rect in enumerate(self._jw_slot_rects):
            if slot_rect.collidepoint(pos):
                if si < len(self._jw_slots) and self._jw_slots[si] is None:
                    self._jw_slots[si] = {"uid": uid, "kind": kind}
                return

    def handle_jewelry_keydown(self, key, unicode_char, player):
        if self._jw_phase != "name_confirm":
            return
        if key == pygame.K_BACKSPACE:
            self._jw_custom_name = self._jw_custom_name[:-1]
        elif key == pygame.K_RETURN:
            if self._jw_custom_name.strip():
                self._do_craft_jewelry(player)
        elif unicode_char and unicode_char.isprintable() and len(self._jw_custom_name) < 32:
            self._jw_custom_name += unicode_char

    def handle_jewelry_merchant_click(self, pos, player, npc):
        if not hasattr(self, "_jw_sell_rects"):
            return
        for uid, rect in self._jw_sell_rects.items():
            if rect.collidepoint(pos) and uid.endswith("_btn"):
                base_uid = uid[:-4]
                if base_uid.startswith("pearl_"):
                    pearl_uid = base_uid[len("pearl_"):]
                    value = npc.sell_pearl(pearl_uid, player)
                    if value:
                        player.pending_notifications.append(
                            ("Pearl Sold", f"+{value}g", None))
                else:
                    npc.sell_piece(base_uid, player)
                return

    def handle_jewelry_detail_click(self, pos):
        if self._jw_detail_jewelry is None:
            return
        if hasattr(self, "_jw_detail_close_rect") and self._jw_detail_close_rect.collidepoint(pos):
            self._jw_detail_jewelry = None

    # ------------------------------------------------------------------ #
    #  Craft finalization                                                 #
    # ------------------------------------------------------------------ #

    def _do_craft_jewelry(self, player):
        import time
        from jewelry import Jewelry, make_uid
        name = self._jw_custom_name.strip() or JEWELRY_TYPES[self._jw_type]["label"]
        seed = int(time.time() * 1000) & 0xFFFFFFFF
        uid = make_uid(seed, len(player.jewelry))
        piece = Jewelry(
            uid=uid,
            jewelry_type=self._jw_type,
            slot_count=self._jw_slot_count,
            slots=[s for s in self._jw_slots],
            custom_name=name,
            seed=seed,
        )

        # Remove consumed gems/rocks/pearls from player collections
        gem_uids   = {s["uid"] for s in self._jw_slots if s and s["kind"] == "gem"}
        rock_uids  = {s["uid"] for s in self._jw_slots if s and s["kind"] == "rock"}
        pearl_uids = {s["uid"] for s in self._jw_slots if s and s["kind"] == "pearl"}
        player.gems  = [g for g in player.gems  if g.uid not in gem_uids]
        player.rocks = [r for r in player.rocks if r.uid not in rock_uids]
        if hasattr(player, "pearls"):
            player.pearls = [p for p in player.pearls if p.uid not in pearl_uids]

        player.jewelry.append(piece)
        player.discovered_jewelry.add(self._jw_type)
        player.pending_notifications.append(("Jewelry", f"{name} crafted!", None))

        # Reset workbench state
        self._jw_phase = "idle"
        self._jw_type = None
        self._jw_slots = []
        self._jw_custom_name = ""

    # ------------------------------------------------------------------ #
    #  Drawing utilities                                                  #
    # ------------------------------------------------------------------ #

    def _get_jw_obj(self, slot_data, player):
        if slot_data is None:
            return None
        uid = slot_data["uid"]
        if slot_data["kind"] == "gem":
            return next((g for g in player.gems if g.uid == uid), None)
        if slot_data["kind"] == "pearl":
            return next((p for p in getattr(player, "pearls", []) if p.uid == uid), None)
        return next((r for r in player.rocks if r.uid == uid), None)

    def _draw_jw_icon(self, jtype, cx, cy, size):
        """Draw a tiny iconic shape for a jewelry type."""
        if jtype == "ring":
            pygame.draw.circle(self.screen, _GOLD, (cx, cy), size, 2)
        elif jtype == "necklace":
            pygame.draw.arc(self.screen, _GOLD, (cx - size, cy - size, size * 2, size * 2),
                            0, 3.14, 2)
        elif jtype == "bracelet":
            pygame.draw.circle(self.screen, _GOLD, (cx, cy), size, 3)
        elif jtype == "pendant":
            pygame.draw.polygon(self.screen, _GOLD, [(cx, cy - size), (cx + size, cy), (cx, cy + size), (cx - size, cy)])
        elif jtype == "crown":
            pts = [(cx - size, cy), (cx - size // 2, cy - size), (cx, cy - size // 2),
                   (cx + size // 2, cy - size), (cx + size, cy)]
            pygame.draw.lines(self.screen, _GOLD, False, pts, 2)

    def _draw_jw_silhouette(self, jtype, cx, cy, size):
        """Draw a faint background silhouette of the jewelry type."""
        col = (55, 44, 16)
        if jtype == "ring":
            pygame.draw.circle(self.screen, col, (cx, cy), size, 6)
        elif jtype == "necklace":
            pygame.draw.arc(self.screen, col, (cx - size, cy - size, size * 2, size * 2),
                            0, 3.14, 6)
        elif jtype == "bracelet":
            pygame.draw.circle(self.screen, col, (cx, cy), size, 8)
        elif jtype == "pendant":
            pts = [(cx, cy - size), (cx + size // 2, cy), (cx, cy + size // 2), (cx - size // 2, cy)]
            pygame.draw.polygon(self.screen, col, pts)
        elif jtype == "crown":
            pts = [(cx - size, cy + size // 4), (cx - size // 2, cy - size // 2),
                   (cx, cy), (cx + size // 2, cy - size // 2), (cx + size, cy + size // 4)]
            pygame.draw.lines(self.screen, col, False, pts, 8)
