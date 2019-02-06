from PyQt5.QtCore import QPointF
from PyQt5.QtWidgets import QWidget

from histoslider.openslide_viewer.common.utils import point_to_str
from histoslider.ui.SlideInfoWidget_ui import Ui_SlideInfoWidget


class SlideInfoWidget(QWidget, Ui_SlideInfoWidget):
    def __init__(self, slide_viewer):
        QWidget.__init__(self, slide_viewer)
        self.setupUi(self)
        self.slide_viewer = slide_viewer

    def update_labels(self):
        self.setUpdatesEnabled(False)
        level_downsample = self.slide_viewer.slide_helper.get_downsample_for_level(
            self.slide_viewer.slide_view_params.level
        )
        level_size = self.slide_viewer.slide_helper.get_level_size(self.slide_viewer.slide_view_params.level)

        self.levelDownsampleLabel.setText(
            "Level, Downsample: {}, {:.0f}".format(self.slide_viewer.slide_view_params.level, level_downsample)
        )
        self.levelSizeLabel.setText("Level Size: ({}, {})".format(*level_size))
        self.viewSceneLabel.setText(
            "View Scene: ({:.0f},{:.0f},{:.0f},{:.0f})".format(
                *self.slide_viewer.get_current_view_scene_rect().getRect()
            )
        )
        if self.slide_viewer.slide_view_params.selected_rect_0_level:
            self.selectedAreaLabel.setText(
                "Selected Area (0-level): ({:.0f},{:.0f},{:.0f},{:.0f})".format(
                    *self.slide_viewer.slide_view_params.selected_rect_0_level
                )
            )
        self.setUpdatesEnabled(True)

    def update_mouse_pos(self, text: QPointF):
        self.mouseSceneLabel.setText("Mouse Scene: " + point_to_str(text))
