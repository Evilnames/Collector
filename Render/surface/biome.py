import pygame
from blocks import BLOCKS, STONE, RESOURCE_BLOCKS
from constants import BLOCK_SIZE
from biomes import BIOME_STONE_COLORS


def _darken(color, amount=25):
    return tuple(max(0, c - amount) for c in color)


def build_water_surfs():
    surfs = []
    for level in range(1, 9):
        h = max(4, level * BLOCK_SIZE // 8)
        s = pygame.Surface((BLOCK_SIZE, h), pygame.SRCALPHA)
        alpha = 110 + level * 7
        s.fill((40, 110, 220, alpha))
        shimmer = pygame.Surface((BLOCK_SIZE, 2), pygame.SRCALPHA)
        shimmer.fill((100, 180, 255, 55))
        for ry in range(3, h - 1, 9):
            s.blit(shimmer, (0, ry))
        surfs.append(s)
    return surfs


def build_resource_hint_surfs():
    stone_col = BLOCKS[STONE]["color"]
    hints = {}
    for bid in RESOURCE_BLOCKS:
        res_col  = BLOCKS[bid]["color"]
        hint_col = tuple(int(stone_col[i] * 0.8 + res_col[i] * 0.2) for i in range(3))
        s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        s.fill(hint_col)
        pygame.draw.rect(s, _darken(hint_col), s.get_rect(), 1)
        hints[bid] = s
    return hints


def build_biome_resource_hint_surfs():
    result = {}
    for biome, stone_col in BIOME_STONE_COLORS.items():
        hints = {}
        for bid in RESOURCE_BLOCKS:
            res_col  = BLOCKS[bid]["color"]
            hint_col = tuple(int(stone_col[i] * 0.8 + res_col[i] * 0.2) for i in range(3))
            s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
            s.fill(hint_col)
            pygame.draw.rect(s, _darken(hint_col), s.get_rect(), 1)
            hints[bid] = s
        result[biome] = hints
    return result


def build_biome_stone_surfs():
    surfs = {}
    for biome, color in BIOME_STONE_COLORS.items():
        s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        s.fill(color)
        pygame.draw.rect(s, _darken(color), s.get_rect(), 1)
        surfs[biome] = s
    return surfs
