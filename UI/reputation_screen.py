import math
import pygame
import towns as towns_mod
import heraldry
from town_needs import LUXURY_CATEGORIES, CATEGORY_COLOR

_BG      = (24, 22, 18)
_BORDER  = (160, 130, 80)
_TITLE_C = (240, 220, 160)
_LABEL_C = (200, 185, 140)
_DIM_C   = (120, 110, 90)
_GREEN   = (90, 210, 100)
_YELLOW  = (220, 200, 70)
_GOLD    = (220, 175, 40)
_GREY    = (75, 70, 60)

_REP_BAR_FULL = 80
_MAP_PANEL_W  = 260

_BIOME_LUXURY = {
    "forest":        "wine",
    "jungle":        "coffee",
    "desert":        "spirits",
    "alpine":        "beer",
    "wetland":       "tea",
    "steppe":        "herbs",
    "coastal":       "spirits",
    "mediterranean": "wine",
    "east_asian":    "tea",
    "arabia":        "coffee",
    "levant":        "pottery",
    "persia":        "pottery",
    "silk_road":     "herbs",
    "yunnan":        "tea",
}


def _rep_tier(rep):
    if rep >= 40:
        return "Honored", _GOLD
    if rep >= 20:
        return "Trusted", _GREEN
    if rep >= 1:
        return "Known", _YELLOW
    return "Stranger", _GREY


def _region_luxury(region):
    cap = next(
        (towns_mod.TOWNS[tid] for tid in region.member_town_ids
         if tid in towns_mod.TOWNS and towns_mod.TOWNS[tid].is_capital),
        None,
    )
    if cap:
        for cat in LUXURY_CATEGORIES:
            if cat in cap.needs:
                return cat
    return _BIOME_LUXURY.get(region.biome_group, "")


def _draw_arch(surf, color, x1, x2, y, height, width=1):
    if abs(x2 - x1) < 4:
        return
    rect = pygame.Rect(min(x1, x2), y - height, abs(x2 - x1), height * 2)
    pygame.draw.arc(surf, color, rect, 0, math.pi, width)


def _draw_rival_dashes(surf, color, x1, x2, y, depth=18):
    dx = x2 - x1
    dist = abs(dx)
    if dist < 4:
        return
    steps = max(1, dist // 11)
    for i in range(steps):
        t0 = i / steps
        t1 = (i + 0.55) / steps
        px0 = int(x1 + dx * t0)
        px1 = int(x1 + dx * t1)
        py  = y + int(math.sin(t0 * math.pi) * depth)
        pygame.draw.line(surf, color, (px0, py), (px1, py), 1)


class ReputationScreenMixin:

    def _draw_reputation_screen(self, player):
        screen = self.screen
        sw, sh = screen.get_size()

        visited = getattr(player, 'visited_town_ids', set())

        visible = []
        for region in sorted(towns_mod.REGIONS.values(), key=lambda r: r.region_id):
            vt = [towns_mod.TOWNS[tid] for tid in region.member_town_ids
                  if tid in towns_mod.TOWNS and tid in visited]
            if vt:
                visible.append((region, vt))

        surf = pygame.Surface((sw, sh), pygame.SRCALPHA)
        surf.fill((0, 0, 0, 175))
        screen.blit(surf, (0, 0))

        cw, ch = 860, min(sh - 80, 580)
        cx = (sw - cw) // 2
        cy = (sh - ch) // 2

        pygame.draw.rect(screen, _BG, (cx, cy, cw, ch))
        pygame.draw.rect(screen, _BORDER, (cx, cy, cw, ch), 2)

        ts = self.font.render("KINGDOMS  &  STANDING", True, _TITLE_C)
        screen.blit(ts, (cx + (cw - ts.get_width()) // 2, cy + 10))
        pygame.draw.line(screen, _BORDER, (cx + 16, cy + 34), (cx + cw - 16, cy + 34), 1)

        hs = self.small.render("K  or  ESC  to close", True, _DIM_C)
        screen.blit(hs, (cx + (cw - hs.get_width()) // 2, cy + ch - 18))

        # ── LIST / MAP toggle buttons ────────────────────────────────────────
        view = getattr(self, '_rep_view', 'list')
        btn_w, btn_h = 52, 20
        btn_y = cy + 40
        btn_gap = 6
        total_btn_w = btn_w * 2 + btn_gap
        btn_list_x = cx + cw - total_btn_w - 18
        btn_map_x  = btn_list_x + btn_w + btn_gap

        tab_rects = {}
        for label, bx, key in [("LIST", btn_list_x, "list"), ("MAP", btn_map_x, "map")]:
            r = pygame.Rect(bx, btn_y, btn_w, btn_h)
            tab_rects[key] = r
            active = (view == key)
            bg_col  = (45, 42, 32) if active else (30, 28, 22)
            brd_col = _GOLD if active else _GREY
            pygame.draw.rect(screen, bg_col, r)
            pygame.draw.rect(screen, brd_col, r, 1)
            ls = self.small.render(label, True, _TITLE_C if active else _DIM_C)
            screen.blit(ls, (bx + (btn_w - ls.get_width()) // 2, btn_y + (btn_h - ls.get_height()) // 2))
        self._rep_tab_rects = tab_rects

        content_top = cy + 66
        content_bot = cy + ch - 24
        content_h   = content_bot - content_top

        if view == 'map':
            all_regions = sorted(towns_mod.REGIONS.values(), key=lambda r: r.region_id)
            visited_rids = {
                region.region_id for region, _ in visible
            }
            self._draw_kingdom_map(
                screen, cx, cy, cw, ch,
                content_top, content_bot,
                all_regions, visited_rids, player,
            )
            return

        # ── LIST VIEW (unchanged) ────────────────────────────────────────────
        pad_x = cx + 14
        COA_W, COA_H = 64, 80
        TEXT_X_OFF   = COA_W + 12
        TOWN_ROW_H   = 22
        HDR_H        = max(COA_H, 22 + 18 + 18)

        def _entry_h(n_towns):
            return 8 + HDR_H + 8 + n_towns * TOWN_ROW_H + 14

        total_h = sum(_entry_h(len(vt)) for _, vt in visible) if visible else 0
        self._rep_max_scroll = max(0, total_h - content_h)
        scroll = max(0, min(getattr(self, '_rep_scroll', 0), self._rep_max_scroll))
        self._rep_scroll = scroll

        clip = pygame.Rect(cx, content_top, cw, content_h)
        old_clip = screen.get_clip()
        screen.set_clip(clip)

        y = content_top - scroll
        text_x = pad_x + TEXT_X_OFF

        for region, vt in visible:
            eh = _entry_h(len(vt))
            if y + eh < content_top:
                y += eh
                continue
            if y > content_bot:
                break

            ey = y + 8

            if region.coat_of_arms:
                heraldry.draw(screen, pad_x, ey, COA_W, COA_H, region.coat_of_arms)
            else:
                pygame.draw.rect(screen, (50, 45, 38), (pad_x, ey, COA_W, COA_H))

            rn_s = self.font.render(region.name.upper(), True, _TITLE_C)
            screen.blit(rn_s, (text_x, ey))

            cap = next(
                (towns_mod.TOWNS[tid] for tid in region.member_town_ids
                 if tid in towns_mod.TOWNS and towns_mod.TOWNS[tid].is_capital),
                None
            )
            leader_str = (f"{region.leader_title} {cap.leader_name}"
                          if cap and cap.leader_name else region.leader_title)
            ag_label   = towns_mod.agenda_label(region.agenda) if region.agenda else ""
            sub_parts  = [leader_str]
            if ag_label:
                sub_parts.append(ag_label)
            sub_parts.append(region.biome_group.title())
            sub_s = self.small.render("  ·  ".join(sub_parts), True, _LABEL_C)
            screen.blit(sub_s, (text_x, ey + 22))

            if region.tagline:
                tg_s = self.small.render(region.tagline, True, _DIM_C)
                screen.blit(tg_s, (text_x, ey + 40))

            allies = [towns_mod.REGIONS[rid].name
                      for rid in towns_mod.allied_region_ids(region.region_id)
                      if rid in towns_mod.REGIONS]
            rivals = [towns_mod.REGIONS[rid].name
                      for rid in towns_mod.rival_region_ids(region.region_id)
                      if rid in towns_mod.REGIONS]
            rel_parts = []
            if allies:
                rel_parts.append(("✦ Allied: " + ", ".join(allies), (130, 200, 130)))
            if rivals:
                rel_parts.append(("⚔ Rival: " + ", ".join(rivals), (210, 110, 80)))
            rel_x = text_x
            for txt, col in rel_parts:
                rs = self.small.render(txt, True, col)
                screen.blit(rs, (rel_x, ey + 58))
                rel_x += rs.get_width() + 14

            # Supply market chips — only shows non-baseline tags
            if region.supply:
                chips = []
                for tag, s in sorted(region.supply.items()):
                    if s >= 1.20:
                        chips.append((f"{tag}↑", (130, 175, 230)))
                    elif s <= 0.75:
                        chips.append((f"{tag}↓", (230, 120, 80)))
                if chips:
                    x_off = text_x
                    prefix_s = self.small.render("Market: ", True, (140, 130, 100))
                    screen.blit(prefix_s, (x_off, ey + 76))
                    x_off += prefix_s.get_width()
                    for chip_text, chip_col in chips[:5]:
                        cs = self.small.render(chip_text + "  ", True, chip_col)
                        screen.blit(cs, (x_off, ey + 76))
                        x_off += cs.get_width()

            reg_rep = sum(t.reputation for t in vt)
            tier_label, tier_col = _rep_tier(reg_rep)
            badge_s = self.small.render(f"{tier_label}  {reg_rep} rep", True, tier_col)
            screen.blit(badge_s, (cx + cw - badge_s.get_width() - 22, ey + 2))

            town_y = ey + HDR_H + 8
            for town in vt:
                if content_top - 30 < town_y < content_bot + 5:
                    _, tc = _rep_tier(town.reputation)
                    tn_s = self.small.render(
                        f"{town.name}  ({town.tier_name()})", True, _LABEL_C)
                    screen.blit(tn_s, (text_x, town_y))

                    bx = text_x + 190
                    by = town_y + 3
                    bw, bh = 120, 10
                    fill = int(bw * min(town.reputation / _REP_BAR_FULL, 1.0))
                    pygame.draw.rect(screen, (40, 38, 30), (bx, by, bw, bh))
                    if fill > 0:
                        pygame.draw.rect(screen, tc, (bx, by, fill, bh))
                    pygame.draw.rect(screen, _BORDER, (bx, by, bw, bh), 1)

                    rn_surf = self.small.render(str(town.reputation), True, tc)
                    screen.blit(rn_surf, (bx + bw + 6, town_y))

                    badge_x = bx + bw + 42
                    for cat, nd in town.needs.items():
                        if cat not in LUXURY_CATEGORIES:
                            continue
                        preferred = nd.get("preferred")
                        if not preferred:
                            continue
                        pref_name = preferred.replace("_", " ").title()
                        col = CATEGORY_COLOR[cat]
                        dim_col = tuple(max(0, c - 60) for c in col)
                        bs = self.small.render(pref_name, True, col)
                        pad = 4
                        badge_w = bs.get_width() + pad * 2
                        badge_h = 14
                        badge_y = town_y + (TOWN_ROW_H - badge_h) // 2
                        pygame.draw.rect(screen, dim_col,  (badge_x, badge_y, badge_w, badge_h))
                        pygame.draw.rect(screen, col,      (badge_x, badge_y, badge_w, badge_h), 1)
                        screen.blit(bs, (badge_x + pad, badge_y + 1))
                        badge_x += badge_w + 5

                town_y += TOWN_ROW_H

            div_y = y + eh - 7
            if content_top < div_y < content_bot:
                pygame.draw.line(screen, (55, 50, 42),
                                 (pad_x, div_y), (cx + cw - 22, div_y), 1)

            y += eh

        if not visible:
            ns = self.font.render("No kingdoms visited yet.", True, _DIM_C)
            screen.blit(ns, (cx + (cw - ns.get_width()) // 2,
                             content_top + content_h // 2 - 10))

        screen.set_clip(old_clip)

        if self._rep_max_scroll > 0:
            sb_x = cx + cw - 12
            sb_h = content_h
            thumb_h = max(28, int(sb_h * content_h / total_h))
            thumb_y = content_top + int((sb_h - thumb_h) * scroll / self._rep_max_scroll)
            pygame.draw.rect(screen, (38, 35, 28), (sb_x, content_top, 8, sb_h))
            pygame.draw.rect(screen, _BORDER, (sb_x, thumb_y, 8, thumb_h))

    # ── MAP VIEW ─────────────────────────────────────────────────────────────

    def _draw_kingdom_map(self, screen, cx, cy, cw, ch,
                          content_top, content_bot,
                          all_regions, visited_rids, player):
        content_h = content_bot - content_top
        map_area_w = cw - _MAP_PANEL_W - 20   # left portion for the track
        map_clip   = pygame.Rect(cx, content_top, map_area_w, content_h)
        panel_x    = cx + map_area_w + 8
        panel_w    = cw - map_area_w - 16

        # Vertical divider
        div_x = cx + map_area_w + 4
        pygame.draw.line(screen, (55, 50, 42),
                         (div_x, content_top), (div_x, content_bot), 1)

        N = len(all_regions)
        if N == 0:
            ns = self.font.render("No kingdoms exist.", True, _DIM_C)
            screen.blit(ns, (cx + (map_area_w - ns.get_width()) // 2,
                             content_top + content_h // 2 - 10))
            self._draw_map_detail(screen, panel_x, content_top, panel_w, content_h, None, [])
            return

        NODE_R   = 18
        SPACING  = max(60, min(110, (map_area_w - NODE_R * 2 - 20) // max(1, N - 1)))
        total_track_w = SPACING * (N - 1) if N > 1 else 0

        scroll       = getattr(self, '_map_scroll', 0)
        max_scroll   = max(0, total_track_w - (map_area_w - NODE_R * 2 - 20))
        self._map_scroll = min(scroll, max_scroll)
        scroll = self._map_scroll

        track_x0 = cx + NODE_R + 10 - scroll
        track_y  = content_top + content_h // 2

        # Compute node centres
        node_xs = [track_x0 + i * SPACING for i in range(N)]

        old_clip = screen.get_clip()
        screen.set_clip(map_clip)

        # Draw track line
        pygame.draw.line(screen, (60, 55, 45),
                         (track_x0, track_y),
                         (track_x0 + total_track_w, track_y), 2)

        # Build rid → index map for arc drawing
        rid_to_idx = {r.region_id: i for i, r in enumerate(all_regions)}

        # Allied arcs above the track
        drawn_ally_pairs = set()
        for i, region in enumerate(all_regions):
            for ally_rid in towns_mod.allied_region_ids(region.region_id):
                pair = tuple(sorted((region.region_id, ally_rid)))
                if pair in drawn_ally_pairs:
                    continue
                drawn_ally_pairs.add(pair)
                j = rid_to_idx.get(ally_rid)
                if j is None:
                    continue
                x1, x2 = node_xs[i], node_xs[j]
                dist = abs(x2 - x1)
                arc_h = max(20, min(50, dist // 3))
                _draw_arch(screen, (120, 180, 100, 180), x1, x2, track_y, arc_h, 1)

        # Rival arcs below the track
        drawn_rival_pairs = set()
        for i, region in enumerate(all_regions):
            for rival_rid in towns_mod.rival_region_ids(region.region_id):
                pair = tuple(sorted((region.region_id, rival_rid)))
                if pair in drawn_rival_pairs:
                    continue
                drawn_rival_pairs.add(pair)
                j = rid_to_idx.get(rival_rid)
                if j is None:
                    continue
                x1, x2 = node_xs[i], node_xs[j]
                _draw_rival_dashes(screen, (200, 80, 60), x1, x2, track_y, depth=22)

        # Draw nodes
        node_rects = {}
        selected_rid = getattr(self, '_map_selected_rid', None)
        for i, region in enumerate(all_regions):
            nx = node_xs[i]
            visited = region.region_id in visited_rids
            rid = region.region_id

            # Node circle
            if visited:
                col = region.leader_color
                # Slightly brighten leader color
                col = tuple(min(255, int(c * 1.1 + 20)) for c in col)
            else:
                col = (50, 48, 42)

            selected = (rid == selected_rid)
            if selected:
                pygame.draw.circle(screen, _GOLD, (nx, track_y), NODE_R + 4, 2)
            pygame.draw.circle(screen, col, (nx, track_y), NODE_R)
            pygame.draw.circle(screen, _BORDER if visited else (70, 65, 55),
                               (nx, track_y), NODE_R, 1)

            # Luxury label above node
            if visited:
                lux = _region_luxury(region)
                if lux:
                    lux_col = CATEGORY_COLOR.get(lux, _DIM_C)
                    ls = self.small.render(lux, True, lux_col)
                    screen.blit(ls, (nx - ls.get_width() // 2, track_y - NODE_R - 18))

            # Region name below node
            name_str = region.name if visited else "???"
            name_col = _LABEL_C if visited else (60, 58, 50)
            ns = self.small.render(name_str, True, name_col)
            screen.blit(ns, (nx - ns.get_width() // 2, track_y + NODE_R + 4))

            # Dynasty tier badge below name
            if visited:
                all_town_reps = [
                    towns_mod.TOWNS[tid].reputation
                    for tid in region.member_town_ids
                    if tid in towns_mod.TOWNS
                ]
                reg_rep = sum(all_town_reps)
                tier_label, tier_col = _rep_tier(reg_rep)
                ts = self.small.render(tier_label, True, tier_col)
                screen.blit(ts, (nx - ts.get_width() // 2, track_y + NODE_R + 18))

            # Store hit rect (unclipped coords for click detection)
            node_rects[rid] = pygame.Rect(nx - NODE_R, track_y - NODE_R,
                                          NODE_R * 2, NODE_R * 2)

        self._map_node_rects = node_rects

        # Scroll indicator
        if max_scroll > 0:
            sb_y = content_bot - 6
            bar_w = map_area_w - 20
            thumb_w = max(24, int(bar_w * (map_area_w / (total_track_w + map_area_w))))
            thumb_x = cx + 10 + int((bar_w - thumb_w) * scroll / max_scroll)
            pygame.draw.rect(screen, (38, 35, 28), (cx + 10, sb_y, bar_w, 4))
            pygame.draw.rect(screen, _BORDER, (thumb_x, sb_y, thumb_w, 4))

        screen.set_clip(old_clip)

        # Detail panel
        selected_region = (towns_mod.REGIONS.get(selected_rid)
                           if selected_rid is not None else None)
        if selected_region is not None:
            visited_towns = [
                towns_mod.TOWNS[tid] for tid in selected_region.member_town_ids
                if tid in towns_mod.TOWNS and tid in getattr(player, 'visited_town_ids', set())
            ]
        else:
            visited_towns = []
        self._draw_map_detail(screen, panel_x, content_top, panel_w, content_h,
                              selected_region, visited_towns)

    def _draw_map_detail(self, screen, px, py, pw, ph, region, visited_towns):
        if region is None:
            hint = self.small.render("Select a kingdom", True, _DIM_C)
            screen.blit(hint, (px + (pw - hint.get_width()) // 2, py + ph // 2 - 8))
            return

        visited = len(visited_towns) > 0
        y = py + 8
        line_h = 18

        # Region name
        ns = self.font.render(region.name.upper(), True, _TITLE_C if visited else _DIM_C)
        screen.blit(ns, (px, y))
        y += 22

        # Leader
        cap = next(
            (towns_mod.TOWNS[tid] for tid in region.member_town_ids
             if tid in towns_mod.TOWNS and towns_mod.TOWNS[tid].is_capital),
            None,
        )
        if cap and cap.leader_name:
            ls = self.small.render(f"{region.leader_title} {cap.leader_name}", True, _LABEL_C)
            screen.blit(ls, (px, y))
            y += line_h

        # Biome · wealth · danger
        sub = f"{region.biome_group.title()}  ·  {region.wealth.title()}  ·  {region.danger.title()}"
        ss = self.small.render(sub, True, _DIM_C)
        screen.blit(ss, (px, y))
        y += line_h

        # Agenda
        ag_label = towns_mod.agenda_label(region.agenda) if region.agenda else ""
        if ag_label:
            ags = self.small.render(ag_label, True, _DIM_C)
            screen.blit(ags, (px, y))
            y += line_h

        # Tagline
        if region.tagline:
            tgs = self.small.render(region.tagline, True, (90, 85, 70))
            screen.blit(tgs, (px, y))
            y += line_h

        y += 4
        pygame.draw.line(screen, (55, 50, 42), (px, y), (px + pw - 8, y), 1)
        y += 6

        # Luxury badge
        lux = _region_luxury(region)
        if lux:
            lux_col = CATEGORY_COLOR.get(lux, _DIM_C)
            lux_bg  = tuple(max(0, c - 60) for c in lux_col)
            label   = lux.title()
            bs = self.small.render(label, True, lux_col)
            bpad = 4
            bw = bs.get_width() + bpad * 2
            bh = 16
            pygame.draw.rect(screen, lux_bg, (px, y, bw, bh))
            pygame.draw.rect(screen, lux_col, (px, y, bw, bh), 1)
            screen.blit(bs, (px + bpad, y + 1))
            y += bh + 6

        # Relations
        allies = [towns_mod.REGIONS[rid].name
                  for rid in towns_mod.allied_region_ids(region.region_id)
                  if rid in towns_mod.REGIONS]
        rivals = [towns_mod.REGIONS[rid].name
                  for rid in towns_mod.rival_region_ids(region.region_id)
                  if rid in towns_mod.REGIONS]
        if allies:
            als = self.small.render("✦ " + ", ".join(allies), True, (130, 200, 130))
            screen.blit(als, (px, y))
            y += line_h
        if rivals:
            rvs = self.small.render("⚔ " + ", ".join(rivals), True, (210, 110, 80))
            screen.blit(rvs, (px, y))
            y += line_h

        y += 4
        pygame.draw.line(screen, (55, 50, 42), (px, y), (px + pw - 8, y), 1)
        y += 8

        if not visited:
            ns2 = self.small.render("Not yet visited", True, _DIM_C)
            screen.blit(ns2, (px, y))
            return

        # Supply market — only when there's something non-baseline to show
        if region.supply:
            supply_chips = []
            for tag, s in sorted(region.supply.items()):
                if s >= 1.20:
                    supply_chips.append((f"{tag}↑", (130, 175, 230)))
                elif s <= 0.75:
                    supply_chips.append((f"{tag}↓", (230, 120, 80)))
            if supply_chips:
                mkt_s = self.small.render("Market", True, _DIM_C)
                screen.blit(mkt_s, (px, y))
                y += line_h
                x_off = px
                for chip_text, chip_col in supply_chips[:4]:
                    cs = self.small.render(chip_text + "  ", True, chip_col)
                    screen.blit(cs, (x_off, y))
                    x_off += cs.get_width()
                y += line_h + 4

        # Towns
        th = self.small.render("Towns", True, _LABEL_C)
        screen.blit(th, (px, y))
        y += line_h + 2

        TOWN_ROW_H = 22
        for town in visited_towns:
            if y + TOWN_ROW_H > py + ph - 8:
                break
            _, tc = _rep_tier(town.reputation)
            tn_s = self.small.render(town.name, True, _LABEL_C)
            screen.blit(tn_s, (px, y))

            bx = px + 90
            by = y + 4
            bw, bh = 80, 10
            fill = int(bw * min(town.reputation / _REP_BAR_FULL, 1.0))
            pygame.draw.rect(screen, (40, 38, 30), (bx, by, bw, bh))
            if fill > 0:
                pygame.draw.rect(screen, tc, (bx, by, fill, bh))
            pygame.draw.rect(screen, _BORDER, (bx, by, bw, bh), 1)

            rep_s = self.small.render(str(town.reputation), True, tc)
            screen.blit(rep_s, (bx + bw + 4, y))

            y += TOWN_ROW_H

    # ── INPUT ─────────────────────────────────────────────────────────────────

    def handle_reputation_screen_click(self, pos):
        tab_rects = getattr(self, '_rep_tab_rects', {})
        for key, rect in tab_rects.items():
            if rect.collidepoint(pos):
                self._rep_view = key
                return

        if getattr(self, '_rep_view', 'list') != 'map':
            return

        node_rects = getattr(self, '_map_node_rects', {})
        for rid, rect in node_rects.items():
            if rect.collidepoint(pos):
                if getattr(self, '_map_selected_rid', None) == rid:
                    self._map_selected_rid = None  # deselect on second click
                else:
                    self._map_selected_rid = rid
                return

    def handle_reputation_screen_scroll(self, dy):
        self._rep_scroll = max(0, min(
            getattr(self, '_rep_scroll', 0) + dy,
            getattr(self, '_rep_max_scroll', 0),
        ))
