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

_REP_BAR_FULL = 80  # rep for a full bar width


def _rep_tier(rep):
    if rep >= 40:
        return "Honored", _GOLD
    if rep >= 20:
        return "Trusted", _GREEN
    if rep >= 1:
        return "Known", _YELLOW
    return "Stranger", _GREY


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

        content_top = cy + 42
        content_bot = cy + ch - 24
        content_h = content_bot - content_top

        pad_x = cx + 14
        COA_W, COA_H = 64, 80
        TEXT_X_OFF   = COA_W + 12
        TOWN_ROW_H   = 22
        HDR_H        = max(COA_H, 22 + 18 + 18)  # 80

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
            sub_s = self.small.render(
                f"{leader_str}  ·  {region.biome_group.title()}", True, _LABEL_C)
            screen.blit(sub_s, (text_x, ey + 22))

            if region.tagline:
                tg_s = self.small.render(region.tagline, True, _DIM_C)
                screen.blit(tg_s, (text_x, ey + 40))

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

                    # Luxury preference badges
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

    def handle_reputation_screen_scroll(self, dy):
        self._rep_scroll = max(0, min(
            getattr(self, '_rep_scroll', 0) + dy,
            getattr(self, '_rep_max_scroll', 0),
        ))
