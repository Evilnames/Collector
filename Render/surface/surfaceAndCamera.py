import pygame
from constants import BLOCK_SIZE, SCREEN_W, SCREEN_H, PLAYER_W, PLAYER_H


def _darken(color, amount=25):
    return tuple(max(0, c - amount) for c in color)


def build_bg_darken_surf():
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    s.fill((0, 0, 0, 110))
    return s


def build_bg_block_surfs(block_surfs, bg_darken_surf):
    darken = bg_darken_surf
    result = {}
    for bid, surf in block_surfs.items():
        baked = surf.copy().convert_alpha()
        baked.blit(darken, (0, 0))
        result[bid] = baked
    return result


def build_cave_wall_surf():
    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    s.fill((55, 47, 40))
    pygame.draw.rect(s, (45, 38, 32), (0, 0, BLOCK_SIZE, BLOCK_SIZE), 1)
    return s


def build_tilled_soil_surfs():
    variants = [
        {"base": (150, 108, 62), "groove": (58, 38, 22)},
        {"base": ( 88,  58, 28), "groove": (36, 22, 12)},
    ]
    surfs = []
    for v in variants:
        s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        s.fill(v["base"])
        for gy in (8, 16, 24):
            pygame.draw.line(s, v["groove"], (2, gy), (BLOCK_SIZE - 2, gy), 2)
        pygame.draw.rect(s, _darken(v["base"], 40), s.get_rect(), 1)
        surfs.append(s)
    return surfs


def update_camera(cam_x, cam_y, player, world):
    target_x = player.x - SCREEN_W // 2 + PLAYER_W // 2
    target_y = player.y - SCREEN_H // 2 + PLAYER_H // 2
    cam_x += (target_x - cam_x) * 0.12
    cam_y += (target_y - cam_y) * 0.12
    max_cy = world.height * BLOCK_SIZE - SCREEN_H
    cam_y = max(0.0, min(cam_y, float(max_cy)))
    return cam_x, cam_y
