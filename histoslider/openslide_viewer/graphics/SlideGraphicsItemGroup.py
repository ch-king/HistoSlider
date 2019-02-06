from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtWidgets import QGraphicsItemGroup

from histoslider.openslide_viewer.common.level_builders import (
    build_tiles_level,
    build_grid_level_from_rects,
)
from histoslider.openslide_viewer.common.SlideHelper import SlideHelper
from histoslider.openslide_viewer.common.SlideViewParams import SlideViewParams
from histoslider.openslide_viewer.graphics.LeveledGraphicsItemGroup import LeveledGraphicsItemGroup
from histoslider.openslide_viewer.graphics.SelectedRectGraphicsItem import SelectedRectGraphicsItem


class SlideGraphicsItemGroup(QGraphicsItemGroup):
    def __init__(self, slide_view_params: SlideViewParams, preffered_rects_count=2000):
        super().__init__()
        self.slide_view_params = slide_view_params
        self.slide_helper = SlideHelper(slide_view_params.slide_path)

        slide_w, slide_h = self.slide_helper.get_level_size(0)
        t = ((slide_w * slide_h) / preffered_rects_count) ** 0.5
        if t < 1000:
            t = 1000
        self.tile_size = (int(t), int(t))

        self.setAcceptedMouseButtons(Qt.NoButton)
        self.setAcceptHoverEvents(False)

        self.levels = self.slide_helper.levels

        self.leveled_graphics_group = LeveledGraphicsItemGroup(self.levels, self)
        self.leveled_graphics_selection = LeveledGraphicsItemGroup(self.levels, self)
        self.leveled_groups = [
            self.leveled_graphics_group,
            self.leveled_graphics_selection,
        ]

        self.graphics_grid = None

        self.init_tiles_levels()
        self.init_grid_levels()
        self.init_selected_rect_levels()
        self.update_visible_level(self.slide_view_params.level)

        # self.setFlag(QGraphicsItem.ItemHasNoContents, True)
        # self.setFlag(QGraphicsItem.ItemContainsChildrenInShape, True)
        # self.setFlag(QGraphicsItem.ItemHasNoContents, True)
        # self.setFlag(QGraphicsItem.ItemClipsToShape, True)
        # self.setFlag(QGraphicsItem.ItemClipsChildrenToShape, True)

    def boundingRect(self) -> QRectF:
        return self.leveled_graphics_group.boundingRect()

    def init_tiles_levels(self):
        for level in self.levels:
            tiles_level = build_tiles_level(level, self.tile_size, self.slide_helper)
            self.leveled_graphics_group.clear_level(level)
            self.leveled_graphics_group.add_item_to_level_group(level, tiles_level)

    def init_grid_levels(self):
        if self.slide_view_params.grid_rects_0_level:
            level = 0
            graphics_grid = build_grid_level_from_rects(
                level,
                self.slide_view_params.grid_rects_0_level,
                self.slide_view_params.grid_color_alphas_0_level,
                self.slide_helper,
            )
            graphics_grid.setZValue(10)
            graphics_grid.setVisible(self.slide_view_params.grid_visible)
            self.addToGroup(graphics_grid)
            self.graphics_grid = graphics_grid

    def init_selected_rect_levels(self):
        if self.slide_view_params.selected_rect_0_level:
            for level in self.levels:
                downsample = self.slide_helper.get_downsample_for_level(level)
                selected_qrectf_0_level = QRectF(
                    *self.slide_view_params.selected_rect_0_level
                )
                rect_for_level = QRectF(
                    selected_qrectf_0_level.topLeft() / downsample,
                    selected_qrectf_0_level.size() / downsample,
                )
                selected_graphics_rect = SelectedRectGraphicsItem(rect_for_level)
                selected_graphics_rect.setZValue(20)

                self.leveled_graphics_selection.clear_level(level)
                self.leveled_graphics_selection.add_item_to_level_group(
                    level, selected_graphics_rect
                )

    def update_visible_level(self, visible_level):
        if visible_level == None or visible_level == -1:
            visible_level = max(self.levels)
        for leveled_group in self.leveled_groups:
            leveled_group.update_visible_level(visible_level)
        self.slide_view_params.level = visible_level

        if self.graphics_grid:
            self.graphics_grid.update_downsample(
                self.slide_helper.get_downsample_for_level(visible_level)
            )

    def update_grid_rects_0_level(self, grid_rects_0_level, grid_color_alphas_0_level):
        self.slide_view_params.grid_rects_0_level = grid_rects_0_level
        self.slide_view_params.grid_color_alphas_0_level = grid_color_alphas_0_level
        self.init_grid_levels()

    def update_grid_visibility(self, grid_visible):
        self.slide_view_params.grid_visible = grid_visible
        if self.graphics_grid:
            self.graphics_grid.update_downsample(
                self.slide_helper.get_downsample_for_level(self.slide_view_params.level)
            )
            self.graphics_grid.setVisible(grid_visible)

    def update_selected_rect_0_level(self, selected_rect_0_level):
        self.slide_view_params.selected_rect_0_level = selected_rect_0_level
        self.init_selected_rect_levels()
