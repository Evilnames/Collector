import pygame
from blocks import BLOCKS
from constants import BLOCK_SIZE
from Render.block_helpers import _darken
from Render.blocks_terrain import build_terrain_surfs, build_ore_richness_surfs
from Render.blocks_wood import build_wood_surfs
from Render.blocks_crops import build_crop_surfs
from Render.blocks_crafting import build_crafting_surfs
from Render.blocks_decor import build_decor_surfs
from Render.blocks_structures import build_structure_surfs
from Render.logic_blocks import build_logic_surfs
from Render.ocean import build_ocean_surfs
from Render.pipe_blocks import build_pipe_surfs
from Render.blocks_bauhaus import build_bauhaus_surfs
from Render.blocks_victorian import build_victorian_surfs


def build_all_block_surfs():
    surfs = {}
    surfs.update(build_terrain_surfs())
    surfs.update(build_wood_surfs())
    surfs.update(build_crop_surfs())
    surfs.update(build_crafting_surfs())
    surfs.update(build_decor_surfs())
    surfs.update(build_structure_surfs())
    surfs.update(build_logic_surfs())
    surfs.update(build_ocean_surfs())
    surfs.update(build_pipe_surfs())
    surfs.update(build_bauhaus_surfs())
    surfs.update(build_victorian_surfs())

    # Fallback: generic solid-fill for any block with color not yet rendered
    for bid, bdata in BLOCKS.items():
        if bid not in surfs and bdata.get("color") is not None:
            s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
            s.fill(bdata["color"])
            pygame.draw.rect(s, _darken(bdata["color"]), s.get_rect(), 1)
            surfs[bid] = s

    return surfs
