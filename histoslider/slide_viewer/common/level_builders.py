from PySide2.QtWidgets import QGraphicsItemGroup

from slide_viewer.common.SlideHelper import SlideHelper
from slide_viewer.common.utils import slice_rect, slice_rect2
from slide_viewer.graphics.GridGraphicsItem import GridGraphicsItem
from slide_viewer.graphics.TileGraphicsItem import TileGraphicsItem


def build_tiles_level(level, tile_size, slide_helper: SlideHelper):
    level_size = slide_helper.get_level_size(level)
    tiles_rects = slice_rect(level_size, tile_size)
    tiles_graphics_group = QGraphicsItemGroup()
    downsample = slide_helper.get_downsample_for_level(level)
    for tile_rect in tiles_rects:
        item = TileGraphicsItem(tile_rect, slide_helper.slide_path, level, downsample)
        item.moveBy(tile_rect[0], tile_rect[1])
        tiles_graphics_group.addToGroup(item)

    return tiles_graphics_group


def build_rects_and_color_alphas_for_grid(
    grid_size_0_level, level_size_0, slice_func=slice_rect2
):
    rect_size = grid_size_0_level[0], grid_size_0_level[1]
    rects = slice_func(level_size_0, rect_size, rect_size)
    # colors = [(0, 255, 0, random.randint(0, 128)) for i in range(len(rects))]
    # colors = [(0, 255, 0, 0) for i in range(len(rects))]
    color_alphas = [0 for i in range(len(rects))]
    return rects, color_alphas


# def build_grid_level(level, grid_size_0_level, slide_helper: SlideHelper):
#     level_size = slide_helper.get_level_size(level)
#     level_downsample = slide_helper.get_downsample_for_level(level)
#     rect_size = grid_size_0_level[0] / level_downsample, grid_size_0_level[1] / level_downsample
#     rects = slice_rect(level_size, rect_size)

# colors = [(0, 255, 0, random.randint(0, 128)) for i in range(len(rects))]
# color_alphas=[random.randint(0, 128) for i in range(len(rects))]
# graphics_grid = GraphicsGrid(rects,
#                              colors,
#                              [0, 0, *level_size],
#                              color_alphas)
# return graphics_grid


def build_grid_level_from_rects(
    level, rects_0_level, intensities, slide_helper: SlideHelper
):
    level_size = slide_helper.get_level_size(level)
    level_downsample = slide_helper.get_downsample_for_level(level)
    rects = [
        (
            rect_0_level[0] / level_downsample,
            rect_0_level[1] / level_downsample,
            rect_0_level[2] / level_downsample,
            rect_0_level[3] / level_downsample,
        )
        for rect_0_level in rects_0_level
    ]
    graphics_grid = GridGraphicsItem(rects, intensities, [0, 0, *level_size])
    return graphics_grid
