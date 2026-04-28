import pygame
from constants import BLOCK_SIZE


def draw_boats(screen, boats, cam_x, cam_y, font, player=None, world=None):
    for boat in boats:
        sx = int(boat.x - cam_x)
        sy = int(boat.y - cam_y)
        W, H = boat.W, boat.H

        HULL     = (120, 75, 35)
        HULL_DRK = (70, 45, 20)
        HULL_LGT = (165, 110, 55)

        hull_pts = [
            (sx + 4, sy),
            (sx + W - 4, sy),
            (sx + W, sy + H),
            (sx, sy + H),
        ]
        pygame.draw.polygon(screen, HULL, hull_pts)
        pygame.draw.polygon(screen, HULL_DRK, hull_pts, 2)
        pygame.draw.line(screen, HULL_LGT, (sx + 8, sy + 5), (sx + W - 8, sy + 5), 1)

        if boat.boat_type == "rowboat":
            pygame.draw.rect(screen, HULL_DRK, (sx - 5, sy + H // 2 - 2, 7, 4))
            pygame.draw.rect(screen, HULL_DRK, (sx + W - 2, sy + H // 2 - 2, 7, 4))
        else:
            mast_x   = sx + W // 2
            mast_top = sy - H * 2
            pygame.draw.line(screen, HULL_DRK, (mast_x, sy + H // 4), (mast_x, mast_top), 2)

            wind_str = (world._wind_strength if world._wind_active else 0.0) if world else 0.0
            wind_dir = world._wind_dir if world else 1
            tilt     = int(wind_str * 7 * wind_dir)
            sail_pts = [
                (mast_x, mast_top),
                (mast_x + tilt + wind_dir * 14, sy - H // 2),
                (mast_x, sy + H // 4),
            ]
            pygame.draw.polygon(screen, (240, 235, 210), sail_pts)
            pygame.draw.polygon(screen, (190, 180, 155), sail_pts, 1)

        if player is not None and boat.in_range(player):
            if player.riding_boat is boat:
                hint = "[A/D] Steer  [E] Exit" if boat.boat_type == "sailboat" else "[A/D] Row  [E] Exit"
            else:
                hint = "[E] Board"
            txt = font.render(hint, True, (200, 230, 255))
            screen.blit(txt, (sx + W // 2 - txt.get_width() // 2, sy - 18))
