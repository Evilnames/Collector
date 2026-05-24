"""
UI/temple.py — TempleMixin for religious outposts.

Opened from the outpost flag menu when the active outpost is in
religion.RELIGIOUS_OUTPOST_TYPES. Shows the resident faith's identity,
the bishop, player standing, and action stubs.

Step 3 of the religion build: panel exists, displays state, and reserves
button slots. The actions themselves (donate / pilgrim / confess / accuse)
land in step 6 — buttons are intentionally inactive here so the UI is
finished before the action logic.
"""

import pygame
from constants import SCREEN_W, SCREEN_H

_BG       = (22, 20, 28)
_BORDER   = (175, 155, 110)
_TITLE_C  = (240, 220, 160)
_LABEL_C  = (200, 185, 140)
_DIM_C    = (110, 100, 75)
_WHITE    = (240, 240, 230)
_BAR_BG   = (52, 46, 38)

_PW = 520
_PH = 420


_ACTION_SLOTS = [
    ("Donate Relic",        "+standing  · costs a relic item"),
    ("Fund Pilgrimage",     "+piety, +standing  · 250g"),
    ("Confess",             "wash 1 scandal point  · free"),
    ("Endow Cathedral",     "+standing, rival faiths +scandal · 1500g"),
    ("Accuse Heresy",       "+zeal, scandals a House  · needs +10 standing"),
    ("Tithe Boycott",       "refuse — gain coin, lose standing"),
    ("Back Schismatic",     "+20 schism support  · 600g, schism only"),
    ("Sponsor Inquisition", "purge heresy regions  · 900g"),
]


class TempleMixin:

    def open_temple(self, outpost=None, faith_id=None):
        """Open from either a religious outpost OR a direct faith id (used by
        in-city shrine keepers and bishop NPCs)."""
        self.temple_open            = True
        self.active_temple_op       = outpost
        self.active_temple_faith_id = faith_id
        self._temple_result_msg     = ""

    def close_temple(self):
        self.temple_open            = False
        self.active_temple_op       = None
        self.active_temple_faith_id = None
        self._temple_result_msg     = ""

    def _resolve_temple_faith(self):
        """Return (op_or_none, region_or_none, faith_or_none). Routes through
        religion.faith_for_outpost so heretic_hideouts pick a schismatic /
        heretical faith instead of the regional primary."""
        import religion as rel
        op = getattr(self, "active_temple_op", None)
        if op is not None:
            try:
                from outposts import region_for_outpost
                region = region_for_outpost(op)
            except Exception:
                region = None
            faith = rel.faith_for_outpost(op)
            return (op, region, faith)
        fid = getattr(self, "active_temple_faith_id", None)
        if fid is not None:
            return (None, None, rel.FAITH_STATES.get(fid))
        return (None, None, None)

    def _draw_temple(self, player):
        try:
            import religion as rel
        except Exception:
            return

        op, region, faith = self._resolve_temple_faith()
        if op is None and faith is None:
            return
        clergy = rel.CLERGY.get(region.region_id) if region else None
        try:
            from outposts import OUTPOST_TYPES
        except Exception:
            OUTPOST_TYPES = {}

        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        self.screen.blit(overlay, (0, 0))

        px = (SCREEN_W - _PW) // 2
        py = (SCREEN_H - _PH) // 2

        pygame.draw.rect(self.screen, _BG,     (px, py, _PW, _PH))
        pygame.draw.rect(self.screen, _BORDER, (px, py, _PW, _PH), 2)

        if op is not None:
            cfg = OUTPOST_TYPES.get(op.outpost_type, {})
            type_label = cfg.get("display_name",
                                 op.outpost_type.replace("_", " ").title())
            heading = f"{op.name} — {type_label}"
        elif faith is not None:
            heading = f"{faith.name} — Sanctuary"
        else:
            heading = "Sanctuary"
        title = self.font.render(heading, True, _TITLE_C)
        self.screen.blit(title, (px + 18, py + 14))

        pygame.draw.line(self.screen, _BORDER,
                         (px + 12, py + 42), (px + _PW - 12, py + 42))

        if faith is None:
            msg = self.small.render(
                "No clergy is in residence. The doors are bolted.",
                True, _DIM_C)
            self.screen.blit(msg, (px + 18, py + 60))
            self._draw_temple_close_hint(px, py)
            return

        self._draw_temple_faith_card(faith, clergy, op, px + 18, py + 56)
        self._draw_temple_actions(player, faith, op,
                                  px + 18, py + 210, _PW - 36)
        self._draw_temple_close_hint(px, py)

    # ------------------------------------------------------------------
    def _draw_temple_faith_card(self, faith, clergy, op, x, y):
        import religion as rel

        profile  = rel.doctrine_profile(faith.doctrine)
        tint     = profile.get("tint", (180, 170, 150))
        epithet  = profile.get("epithet", "")

        # Faith name + epithet
        nm = self.font.render(faith.name, True, _TITLE_C)
        self.screen.blit(nm, (x, y))
        ep = self.small.render(f"{faith.doctrine.title()}  —  {epithet}",
                               True, tint)
        self.screen.blit(ep, (x, y + 22))

        # Head + bishop (bishop only shown when we have regional clergy)
        head_line = self.small.render(
            f"{faith.head_title}: {faith.head_name}", True, _LABEL_C)
        self.screen.blit(head_line, (x, y + 44))
        if clergy is not None:
            bishop_line = self.small.render(
                f"{clergy.bishop_title} in residence: {clergy.bishop_name}",
                True, _LABEL_C)
            self.screen.blit(bishop_line, (x, y + 60))

        # Stat bars — piety, orthodoxy, zeal, scandal
        bars = [
            ("Piety",     faith.piety,     (200, 195, 120)),
            ("Orthodoxy", faith.orthodoxy, (155, 175, 200)),
            ("Zeal",      faith.zeal,      (200, 110,  95)),
            ("Scandal",   faith.scandal,   (175,  90, 100)),
        ]
        bar_y = y + 82
        for i, (lbl, val, col) in enumerate(bars):
            row_y = bar_y + i * 16
            ls = self.small.render(lbl, True, _DIM_C)
            self.screen.blit(ls, (x, row_y))
            bx = x + 80
            bw = 200
            pygame.draw.rect(self.screen, _BAR_BG, (bx, row_y + 2, bw, 9))
            fw = int(bw * max(0, min(100, val)) / 100)
            pygame.draw.rect(self.screen, col, (bx, row_y + 2, fw, 9))
            vs = self.small.render(str(int(val)), True, _LABEL_C)
            self.screen.blit(vs, (bx + bw + 8, row_y))

        # Player standing
        standing = rel.get_standing(faith.faith_id)
        tier_lbl, tier_col = rel.standing_tier(standing)
        st_lbl = self.small.render("Your Standing:", True, _DIM_C)
        self.screen.blit(st_lbl, (x + 300, y + 82))
        st_val = self.font.render(f"{tier_lbl} ({standing:+d})",
                                  True, tier_col)
        self.screen.blit(st_val, (x + 300, y + 98))

        rec = rel.PLAYER_STANDING.get(faith.faith_id)
        if rec:
            pm_lbl = self.small.render(
                f"Pilgrim marks: {rec.pilgrim_marks}", True, _DIM_C)
            self.screen.blit(pm_lbl, (x + 300, y + 124))
            rd_lbl = self.small.render(
                f"Relics donated: {rec.relics_donated}", True, _DIM_C)
            self.screen.blit(rd_lbl, (x + 300, y + 140))

    # ------------------------------------------------------------------
    def _draw_temple_actions(self, player, faith, op, x, y, w):
        """Two-column grid of action stubs. All inactive in step 3 — the
        action logic ships in step 6. Buttons are still rendered so the
        UI shape is finished and reviewable now."""
        self._temple_action_rects = {}
        hdr = self.small.render("Sanctuary Actions", True, _LABEL_C)
        self.screen.blit(hdr, (x, y))
        pygame.draw.line(self.screen, _BORDER,
                         (x, y + 16), (x + w, y + 16))

        col_w = (w - 12) // 2
        btn_h = 42
        for i, (label, sub) in enumerate(_ACTION_SLOTS):
            row = i // 2
            col = i % 2
            bx = x + col * (col_w + 12)
            by = y + 24 + row * (btn_h + 6)
            pygame.draw.rect(self.screen, (52, 46, 50),
                             (bx, by, col_w, btn_h), border_radius=4)
            pygame.draw.rect(self.screen, (78, 70, 64),
                             (bx, by, col_w, btn_h), 1, border_radius=4)
            ls = self.small.render(label, True, _LABEL_C)
            self.screen.blit(ls, (bx + 10, by + 4))
            ss = self.small.render(sub, True, _DIM_C)
            self.screen.blit(ss, (bx + 10, by + 22))
            # Stash for click handling once actions ship
            self._temple_action_rects[label] = pygame.Rect(
                bx, by, col_w, btn_h)

        # Result toast (set by handle_temple_click)
        msg = getattr(self, "_temple_result_msg", "")
        if msg:
            ts = self.small.render(msg, True, (240, 220, 150))
            self.screen.blit(ts, (x, y + 24 + 3 * (btn_h + 6) + 6))

    # ------------------------------------------------------------------
    def _draw_temple_close_hint(self, px, py):
        hint = self.small.render("[E] or [ESC] to close", True, _DIM_C)
        self.screen.blit(hint, (px + 18, py + _PH - 22))

    # ------------------------------------------------------------------
    def handle_temple_click(self, pos, player) -> bool:
        """Dispatch a click to the religion.action_* handler for whichever
        button was hit. Returns True if any button consumed the click."""
        for label, rect in getattr(self, "_temple_action_rects", {}).items():
            if not rect.collidepoint(pos):
                continue
            self._invoke_temple_action(label, player)
            return True
        return False

    def _invoke_temple_action(self, label, player):
        import religion as rel
        _, _, faith = self._resolve_temple_faith()
        if faith is None:
            self._temple_result_msg = "No faith in residence."
            return

        handler = rel.TEMPLE_ACTION_HANDLERS.get(label)
        if handler is None:
            return

        day = getattr(player.world, "day_count", 0) if getattr(
            player, "world", None) else 0
        ok, msg, cost = handler(player, faith, day)
        # cost > 0 → player pays; cost < 0 → player is paid
        if ok and cost != 0:
            player.money = max(0, getattr(player, "money", 0) - cost)
        self._temple_result_msg = msg
