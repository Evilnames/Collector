"""Jousting UI — lobby, bracket, live bout overlay, results.

Pattern mirrors UI/arena.py: a mixin attached to the main UI class. The
mixin owns its phase state on `self._jousting_*` attributes and is opened
from a tournament_grounds marshal interaction (see UI/handlers.py).
"""

import pygame

import jousting
import knightly_orders
import heraldry


_PANEL_BG    = (28, 22, 36)
_PANEL_STONE = (45, 38, 56)
_PANEL_GOLD  = (210, 180, 90)
_PANEL_LIGHT = (210, 205, 220)
_BAR_BG      = (60, 40, 40)
_BAR_FILL    = (220, 200, 120)


class JoustingMixin:

    # -----------------------------------------------------------------------
    # Open / close
    # -----------------------------------------------------------------------

    def open_jousting(self, player, world, region_id, rng):
        self.jousting_open      = True
        self._jousting_phase    = "lobby"         # lobby | bracket | bout | rest | finished
        self._jousting_world    = world
        self._jousting_region   = region_id
        self._jousting_t        = jousting.build_tournament(world, region_id, rng)
        self._jousting_bout     = None
        self._jousting_rects    = {}
        self._jousting_result   = None
        self._jousting_message  = ""
        player._jousting_unhorsed = False

    def close_jousting(self):
        self.jousting_open = False

    # -----------------------------------------------------------------------
    # Draw dispatcher
    # -----------------------------------------------------------------------

    def _draw_jousting(self, player, dt):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))

        sw, sh = self.screen.get_size()
        pw, ph = 720, 560
        px = (sw - pw) // 2
        py = (sh - ph) // 2
        pygame.draw.rect(self.screen, _PANEL_BG, (px, py, pw, ph), border_radius=6)
        pygame.draw.rect(self.screen, _PANEL_GOLD, (px, py, pw, ph), 2, border_radius=6)
        pygame.draw.rect(self.screen, _PANEL_STONE, (px + 10, py + 10, pw - 20, ph - 20), border_radius=4)
        title = self.font.render("TOURNAMENT GROUNDS", True, _PANEL_GOLD)
        self.screen.blit(title, (px + pw // 2 - title.get_width() // 2, py + 18))

        if self._jousting_phase == "lobby":
            self._draw_jousting_lobby(player, px, py, pw, ph)
        elif self._jousting_phase == "bout":
            self._draw_jousting_bout(player, dt, px, py, pw, ph)
        elif self._jousting_phase == "rest":
            self._draw_jousting_rest(player, px, py, pw, ph)
        elif self._jousting_phase == "finished":
            self._draw_jousting_finished(player, px, py, pw, ph)

    # -----------------------------------------------------------------------
    # Lobby — show bracket + sign-up button
    # -----------------------------------------------------------------------

    def _draw_jousting_lobby(self, player, px, py, pw, ph):
        self._jousting_rects = {}
        font, small = self.font, self.small
        t = self._jousting_t

        msg = small.render(
            "A field of seven knights has signed the lists. Three passes per bout, "
            "single elimination.",
            True, _PANEL_LIGHT)
        self.screen.blit(msg, (px + 30, py + 60))

        y = py + 95
        for i, opp in enumerate(t.bracket):
            order = knightly_orders.order(opp.order_id)
            order_name = order.name if order else "Unaffiliated"
            tinct = order.heraldry.primary if order else (140, 60, 60)
            pygame.draw.rect(self.screen, tinct, (px + 30, y, 14, 14))
            k = knightly_orders.knight(opp.knight_id)
            raw_rank = (k.rank if k else "Knight")
            tradition = order.tradition if order else ""
            rank = knightly_orders.cultural_rank_label(tradition, raw_rank)
            line = f"{opp.name}, {rank}  —  {order_name}  (skill {opp.skill:.2f})"
            self.screen.blit(small.render(line, True, _PANEL_LIGHT), (px + 52, y - 1))
            y += 16
            # Cultural salute on entry, then a quirk line if present.
            salute = knightly_orders.order_salute(opp.order_id)
            if salute:
                stxt = small.render(f"   ⟶ {salute}", True, (180, 175, 130))
                self.screen.blit(stxt, (px + 52, y - 1))
                y += 14
            if k and k.quirks:
                qtxt = small.render(f"   — {k.quirks[0]}", True, (165, 150, 110))
                self.screen.blit(qtxt, (px + 52, y - 1))
                y += 14
            else:
                y += 2

        # Equipment check
        lance = jousting._equipped_lance(player)
        horse = getattr(player, "mounted_horse", None)
        ok = lance is not None and horse is not None
        warn = []
        if lance is None:
            warn.append("Equip a lance.")
        if horse is None:
            warn.append("Be mounted on a horse.")
        warn_y = py + ph - 100
        if warn:
            text = small.render("  •  ".join(warn), True, (220, 140, 110))
            self.screen.blit(text, (px + 30, warn_y))

        # Buttons
        btn_w, btn_h = 180, 38
        btn_x = px + pw // 2 - btn_w // 2
        btn_y = py + ph - 60
        col = (90, 130, 70) if ok else (70, 70, 80)
        pygame.draw.rect(self.screen, col, (btn_x, btn_y, btn_w, btn_h), border_radius=5)
        label = font.render("Sign Up & Joust" if ok else "Not Ready", True, _PANEL_LIGHT)
        self.screen.blit(label, (btn_x + btn_w // 2 - label.get_width() // 2,
                                 btn_y + btn_h // 2 - label.get_height() // 2))
        if ok:
            self._jousting_rects["sign_up"] = pygame.Rect(btn_x, btn_y, btn_w, btn_h)

        cancel = pygame.Rect(px + pw - 110, py + 16, 90, 26)
        pygame.draw.rect(self.screen, (90, 60, 60), cancel, border_radius=4)
        self.screen.blit(small.render("Leave", True, _PANEL_LIGHT),
                         (cancel.centerx - 20, cancel.centery - 8))
        self._jousting_rects["cancel"] = cancel

    # -----------------------------------------------------------------------
    # Bout — show charge bar / aim picker / impact result
    # -----------------------------------------------------------------------

    def _draw_jousting_bout(self, player, dt, px, py, pw, ph):
        self._jousting_rects = {}
        font, small = self.font, self.small
        bout = self._jousting_bout
        opp  = bout.opponent

        # Tick the bout sim
        jousting.tick(bout, dt, player)

        # Header — opponent + score
        head = font.render(f"vs. {opp.name}", True, _PANEL_GOLD)
        self.screen.blit(head, (px + 30, py + 55))
        score = small.render(f"Pass {bout.pass_index}/{jousting.PASSES_PER_BOUT}    "
                             f"You {bout.player_score}  —  {opp.score} Them",
                             True, _PANEL_LIGHT)
        self.screen.blit(score, (px + 30, py + 80))

        # Tilt-yard schematic
        yard_y = py + 200
        pygame.draw.rect(self.screen, (90, 70, 50), (px + 30, yard_y, pw - 60, 90))
        pygame.draw.rect(self.screen, (140, 120, 90),
                         (px + 30, yard_y + 42, pw - 60, 6))   # central rail

        # Rider positions move toward the center during CHARGE/CLOSE
        progress = 1.0
        if bout.phase == jousting.CHARGE:
            progress = 1.0 - (bout.phase_timer / jousting.CHARGE_DURATION)
        elif bout.phase == jousting.CLOSE:
            progress = 1.0
        elif bout.phase == jousting.IMPACT:
            progress = 1.0
        else:
            progress = 0.0
        player_x = int(px + 50 + (pw - 140) * 0.5 * progress)
        opp_x    = int(px + pw - 60 - (pw - 140) * 0.5 * progress)
        pygame.draw.rect(self.screen, (200, 200, 220), (player_x, yard_y + 30, 14, 24))   # player
        pygame.draw.rect(self.screen, opp_color(opp), (opp_x - 14, yard_y + 30, 14, 24))  # opp

        # Phase-specific UI
        if bout.phase == jousting.CHARGE:
            cap = small.render("CHARGE — hold SPACE to keep your horse at full gallop.",
                               True, _PANEL_LIGHT)
            self.screen.blit(cap, (px + 30, py + 120))
            self._draw_bar(px + 30, py + 150, pw - 60, 18, bout.player_charge)
            # Opponent's battle cry as they thunder down the lists.
            cry = knightly_orders.order_battle_cry(opp.order_id)
            if cry:
                cs = small.render(f"{opp.name}: “{cry}”", True, (220, 170, 130))
                self.screen.blit(cs, (px + 30, py + 175))

        elif bout.phase == jousting.CLOSE:
            cap = small.render("CLOSE — pick your aim: [↑] high  [→] mid  [↓] low",
                               True, _PANEL_LIGHT)
            self.screen.blit(cap, (px + 30, py + 120))
            for i, aim in enumerate(jousting.AIMS):
                rect = pygame.Rect(px + 30 + i * 110, py + 145, 100, 30)
                col = (140, 130, 80) if bout.player_aim == aim else (70, 60, 80)
                pygame.draw.rect(self.screen, col, rect, border_radius=4)
                self.screen.blit(small.render(aim.upper(), True, _PANEL_LIGHT),
                                 (rect.centerx - 18, rect.centery - 8))
                self._jousting_rects[f"aim_{aim}"] = rect

        elif bout.phase == jousting.IMPACT or bout.phase == jousting.RESULT:
            cap = small.render("IMPACT!", True, (250, 220, 120))
            self.screen.blit(cap, (px + 30, py + 120))
            outcome = small.render(bout.last_outcome, True, _PANEL_LIGHT)
            self.screen.blit(outcome, (px + 30, py + 145))
            pts = small.render(f"+{bout.last_pts_player} you   +{bout.last_pts_opp} them",
                               True, _PANEL_GOLD)
            self.screen.blit(pts, (px + 30, py + 170))

        elif bout.phase == jousting.REST:
            cap = small.render("Resetting at the ends of the tilt-yard…",
                               True, _PANEL_LIGHT)
            self.screen.blit(cap, (px + 30, py + 120))

        elif bout.phase == jousting.DONE:
            # Resolve bout, advance bracket, or finish tournament
            advanced = jousting.resolve_bout(bout, self._jousting_t, player)
            if advanced and self._jousting_t.player_active:
                next_opp = jousting.next_opponent(self._jousting_t)
                if next_opp is None:
                    self._jousting_finalize(player)
                else:
                    self._jousting_phase = "rest"
                    self._jousting_message = (
                        f"Advance! Next opponent: {next_opp.name}.")
                    self._jousting_t.current_bout = None
                    self._jousting_pending_opp = next_opp
            else:
                self._jousting_finalize(player)

    def _jousting_finalize(self, player):
        self._jousting_phase = "finished"
        self._jousting_result = jousting.award_rewards(self._jousting_t, player)

    # -----------------------------------------------------------------------
    # Rest between bouts
    # -----------------------------------------------------------------------

    def _draw_jousting_rest(self, player, px, py, pw, ph):
        self._jousting_rects = {}
        small = self.small
        self.screen.blit(small.render(self._jousting_message, True, _PANEL_LIGHT),
                         (px + 30, py + 100))
        btn = pygame.Rect(px + pw // 2 - 90, py + ph - 70, 180, 40)
        pygame.draw.rect(self.screen, (90, 130, 70), btn, border_radius=5)
        self.screen.blit(self.font.render("Ready", True, _PANEL_LIGHT),
                         (btn.centerx - 30, btn.centery - 10))
        self._jousting_rects["next_bout"] = btn

    # -----------------------------------------------------------------------
    # Final results
    # -----------------------------------------------------------------------

    def _draw_jousting_finished(self, player, px, py, pw, ph):
        self._jousting_rects = {}
        font, small = self.font, self.small
        res = self._jousting_result or {}
        place = res.get("place", 8)
        title = {1: "CHAMPION OF THE LISTS",
                 2: "Runner-Up",
                 4: "Semi-Finalist",
                 8: "First-Round Knockout"}.get(place, "Out of the Bracket")
        self.screen.blit(font.render(title, True, _PANEL_GOLD), (px + 30, py + 70))
        self.screen.blit(small.render(f"Purse: {res.get('gold', 0)} gold",
                                      True, _PANEL_LIGHT), (px + 30, py + 110))
        if res.get("pennant_order") is not None:
            order = knightly_orders.order(res["pennant_order"])
            if order:
                self.screen.blit(small.render(
                    f"You take a pennant of the {order.name}.",
                    True, _PANEL_LIGHT), (px + 30, py + 135))

        # List tradition-flavored loot drops alongside the purse.
        loot = res.get("loot_drops", [])
        if loot:
            try:
                from items import ITEMS
            except Exception:
                ITEMS = {}
            self.screen.blit(small.render("Spoils taken from the lists:",
                                          True, _PANEL_GOLD),
                             (px + 30, py + 160))
            row_y = py + 180
            for item_id, count in loot:
                spec = ITEMS.get(item_id, {})
                label = spec.get("name", item_id)
                pip = spec.get("color", (200, 200, 200))
                pygame.draw.rect(self.screen, pip, (px + 32, row_y, 10, 10))
                txt = f"  ×{count}  {label}" if count > 1 else f"  {label}"
                self.screen.blit(small.render(txt, True, _PANEL_LIGHT),
                                 (px + 48, row_y - 2))
                row_y += 18

        btn = pygame.Rect(px + pw // 2 - 60, py + ph - 60, 120, 36)
        pygame.draw.rect(self.screen, (90, 90, 130), btn, border_radius=5)
        self.screen.blit(font.render("Done", True, _PANEL_LIGHT),
                         (btn.centerx - 24, btn.centery - 10))
        self._jousting_rects["done"] = btn

    # -----------------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------------

    def _draw_bar(self, x, y, w, h, value):
        pygame.draw.rect(self.screen, _BAR_BG, (x, y, w, h), border_radius=3)
        pygame.draw.rect(self.screen, _BAR_FILL,
                         (x, y, int(w * max(0.0, min(1.0, value))), h), border_radius=3)

    # -----------------------------------------------------------------------
    # Input
    # -----------------------------------------------------------------------

    def handle_jousting_click(self, mx, my, player):
        rects = self._jousting_rects
        if "cancel" in rects and rects["cancel"].collidepoint(mx, my):
            self.close_jousting()
            return
        if "sign_up" in rects and rects["sign_up"].collidepoint(mx, my):
            opp = jousting.next_opponent(self._jousting_t)
            if opp is None:
                self.close_jousting()
                return
            self._jousting_bout = jousting.start_bout(self._jousting_t, opp)
            jousting.begin_pass(self._jousting_bout)
            self._jousting_phase = "bout"
            return
        if "next_bout" in rects and rects["next_bout"].collidepoint(mx, my):
            opp = getattr(self, "_jousting_pending_opp", None)
            if opp is None:
                self._jousting_finalize(player)
                return
            self._jousting_bout = jousting.start_bout(self._jousting_t, opp)
            jousting.begin_pass(self._jousting_bout)
            self._jousting_phase = "bout"
            return
        if "done" in rects and rects["done"].collidepoint(mx, my):
            self.close_jousting()
            return
        for aim in jousting.AIMS:
            key = f"aim_{aim}"
            if key in rects and rects[key].collidepoint(mx, my):
                jousting.set_aim(self._jousting_bout, aim)
                return

    def handle_jousting_key(self, event, player):
        if self._jousting_phase != "bout":
            return
        bout = self._jousting_bout
        if bout is None or bout.phase != jousting.CLOSE:
            return
        if event.key == pygame.K_UP:
            jousting.set_aim(bout, jousting.AIM_HIGH)
        elif event.key == pygame.K_RIGHT:
            jousting.set_aim(bout, jousting.AIM_MID)
        elif event.key == pygame.K_DOWN:
            jousting.set_aim(bout, jousting.AIM_LOW)

    def update_jousting_input(self, keys, player):
        if self._jousting_phase != "bout":
            return
        if self._jousting_bout is None:
            return
        jousting.handle_charge_input(self._jousting_bout, keys, pygame)


    # -----------------------------------------------------------------------
    # Encyclopedia tab: Chivalry — list discovered orders + tournament record
    # -----------------------------------------------------------------------

    def _draw_chivalry_codex(self, player, gy0=58, gx_off=0):
        from constants import SCREEN_W, SCREEN_H
        x0 = gx_off + 14
        y0 = gy0 + 12

        # Resolve kingdom names from the world plan when available.
        plan = getattr(getattr(player, "world", None), "plan", None)
        def kingdom_name(kid):
            if plan is not None:
                k = plan.kingdoms.get(kid)
                if k:
                    return k.name
            try:
                from towns import REGIONS
                r = REGIONS.get(kid)
                if r:
                    return r.name
            except Exception:
                pass
            return f"Kingdom {kid}"

        orders = list(knightly_orders.ORDERS.values())
        cell_w, cell_h = 360, 396
        grid_w = SCREEN_W - x0 - 320
        cols = max(1, grid_w // (cell_w + 8))
        for i, order in enumerate(orders):
            row, col = divmod(i, cols)
            cx = x0 + col * (cell_w + 8)
            cy = y0 + row * (cell_h + 8)
            r = pygame.Rect(cx, cy, cell_w, cell_h)
            pygame.draw.rect(self.screen, (28, 22, 14), r, border_radius=4)
            pygame.draw.rect(self.screen, (175, 140, 70), r, 1, border_radius=4)
            heraldry.draw(self.screen, cx + 6, cy + 8, 30, 38, order.heraldry)
            tx = cx + 44
            ns = self.small.render(order.name, True, (235, 210, 150))
            self.screen.blit(ns, (tx, cy + 6))
            trad = (order.tradition or "errant").replace("_", " ").title()
            ts = self.small.render(f"{trad} tradition", True, (210, 175, 110))
            self.screen.blit(ts, (tx, cy + 22))
            seat = order.seat or "—"
            ss = self.small.render(f"Seat: {seat}", True, (175, 155, 110))
            self.screen.blit(ss, (tx, cy + 38))
            ms = self.small.render(f"“{order.motto}”", True, (170, 150, 105))
            self.screen.blit(ms, (cx + 8, cy + 58))

            yc = cy + 78
            line_h = 16
            details = []
            if order.doctrine:
                details.append(("Doctrine", order.doctrine, (200, 180, 130)))
            if order.patron:
                details.append(("Patron", order.patron, (200, 180, 130)))
            if order.relic:
                details.append(("Relic", order.relic, (200, 180, 130)))
            if order.vows:
                details.append(("Vow", order.vows[0], (190, 165, 110)))
            rival = knightly_orders.rival_of(order.order_id)
            if rival:
                details.append(("Rival order", rival.name, (215, 130, 110)))
            # Kingdom alignment summary.
            sworn = knightly_orders.aligned_kingdoms(order.order_id, "sworn")
            feuds = knightly_orders.aligned_kingdoms(order.order_id, "rival")
            exiled = knightly_orders.aligned_kingdoms(order.order_id, "exiled")
            if sworn:
                names = ", ".join(kingdom_name(k) for k in sworn[:3])
                details.append(("Sworn to", names, (180, 215, 155)))
            if feuds:
                names = ", ".join(kingdom_name(k) for k in feuds[:3])
                details.append(("At feud with", names, (220, 130, 110)))
            if exiled:
                names = ", ".join(kingdom_name(k) for k in exiled[:3])
                details.append(("Exiled from", names, (210, 120, 100)))
            for label, val, col_rgb in details:
                txt = self.small.render(f"{label}: {val}", True, col_rgb)
                self.screen.blit(txt, (cx + 8, yc))
                yc += line_h

            wins = sum(knightly_orders.KNIGHTS[kid].tournament_wins
                       for kid in order.member_ids
                       if kid in knightly_orders.KNIGHTS)
            stats = self.small.render(
                f"Members {len(order.member_ids)} · Prestige {order.prestige} · Wins {wins}",
                True, (200, 175, 120))
            self.screen.blit(stats, (cx + 8, yc))
            yc += line_h
            # Grandmaster line — use the cultural label for the rank prefix.
            gm = next((knightly_orders.KNIGHTS[kid] for kid in order.member_ids
                       if kid in knightly_orders.KNIGHTS
                       and knightly_orders.KNIGHTS[kid].rank == "Grandmaster"),
                      None)
            if gm:
                col_gm = (245, 210, 110) if gm.is_noble else (215, 190, 130)
                gm_title = knightly_orders.cultural_rank_label(
                    order.tradition, "Grandmaster")
                gms = self.small.render(
                    f"{gm_title}: {gm.name}", True, col_gm)
                self.screen.blit(gms, (cx + 8, yc))
                yc += line_h
            # Battle cry — short, evocative, drawn from ORDER_TRADITIONS.
            cry = knightly_orders.order_battle_cry(order.order_id)
            if cry:
                cs = self.small.render(f"Cry: “{cry}”", True, (220, 170, 130))
                self.screen.blit(cs, (cx + 8, yc))
                yc += line_h
            # Pre-charge ritual line.
            ritual = knightly_orders.order_pre_charge_ritual(order.order_id)
            if ritual:
                rs = self.small.render(f"Ritual: {ritual}", True, (175, 160, 120))
                self.screen.blit(rs, (cx + 8, yc))
                yc += line_h
            # Cultural depth — initiation, school, festival, taboo.
            extras = [
                ("Initiation",
                 knightly_orders.order_initiation_rite(order.order_id),
                 (185, 170, 130)),
                ("School",
                 knightly_orders.order_fighting_school(order.order_id),
                 (175, 195, 165)),
                ("Festival",
                 knightly_orders.order_festival(order.order_id),
                 (200, 175, 130)),
                ("Taboo",
                 knightly_orders.order_taboo(order.order_id),
                 (220, 145, 130)),
            ]
            for label, val, col_rgb in extras:
                if not val:
                    continue
                # Truncate to fit the card width; tradition strings can be long.
                shown = val if len(val) < 60 else val[:57] + "…"
                t = self.small.render(f"{label}: {shown}", True, col_rgb)
                self.screen.blit(t, (cx + 8, yc))
                yc += line_h
            # Noble count — flag royal entanglement.
            nobles = [knightly_orders.KNIGHTS[kid]
                      for kid in order.member_ids
                      if kid in knightly_orders.KNIGHTS
                      and knightly_orders.KNIGHTS[kid].is_noble]
            if nobles:
                line = f"Nobles in roster: {len(nobles)}"
                if order.patron_dynasty_id is not None and plan is not None:
                    dyn = plan.dynasties.get(order.patron_dynasty_id)
                    if dyn:
                        line += f"  —  {dyn.house_name}"
                ns = self.small.render(line, True, (220, 195, 145))
                self.screen.blit(ns, (cx + 8, yc))
                yc += line_h
            if order.founding_chronicle:
                fc = self.small.render(order.founding_chronicle,
                                       True, (160, 145, 110))
                self.screen.blit(fc, (cx + 8, yc))
                yc += line_h
            # Centuries-deep chivalric ledger — last few notable moments.
            events = getattr(order, "historical_events", []) or []
            if events:
                yc += 4
                title_s = self.small.render(
                    f"Annals (founded yr {order.founded_year}):",
                    True, (210, 180, 130))
                self.screen.blit(title_s, (cx + 8, yc))
                yc += line_h
                for line in events[-4:]:
                    shown = line if len(line) < 72 else line[:69] + "…"
                    es = self.small.render(shown, True, (170, 155, 120))
                    self.screen.blit(es, (cx + 8, yc))
                    yc += line_h

        # Right panel: player tournament record
        info_x = SCREEN_W - 300
        info_y = y0
        pygame.draw.rect(self.screen, (22, 18, 10), (info_x, info_y, 290, 240), border_radius=6)
        pygame.draw.rect(self.screen, (175, 140, 70), (info_x, info_y, 290, 240), 1, border_radius=6)
        ttl = self.font.render("Your Lists Record", True, (240, 210, 150))
        self.screen.blit(ttl, (info_x + 14, info_y + 8))
        rec = getattr(player, "tournament_record", {"wins": 0, "podium": 0, "entries": 0})
        pennants = getattr(player, "inventory", {}).get("tournament_pennant", 0)
        lines = [
            f"Tournaments entered: {rec.get('entries', 0)}",
            f"Podium finishes:     {rec.get('podium', 0)}",
            f"Championships:       {rec.get('wins', 0)}",
            f"Pennants taken:      {pennants}",
        ]
        for i, ln in enumerate(lines):
            t = self.small.render(ln, True, (200, 175, 120))
            self.screen.blit(t, (info_x + 16, info_y + 40 + i * 18))


def opp_color(opp):
    order = knightly_orders.order(opp.order_id)
    if order:
        return order.heraldry.primary
    return (170, 60, 60)
