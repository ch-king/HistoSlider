from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QAction,
    QDialog,
    QMessageBox,
    QToolBar,
    QWidget,
)

from histoslider.openslide_viewer.SlideGraphicsView import SlideGraphicsView
from histoslider.openslide_viewer.common.SlideViewParams import SlideViewParams
from histoslider.openslide_viewer.common.json_utils import to_json
from histoslider.openslide_viewer.common.level_builders import build_rects_and_color_alphas_for_grid
from histoslider.openslide_viewer.common.screenshot_builders import build_screenshot_image
from histoslider.ui.GoToDialog import GoToDialog
from histoslider.ui.GridSizeDialog import GridSizeDialog
from histoslider.ui.ScreenshotDialog import ScreenshotDialog
from histoslider.ui.SlideInfoWidget import SlideInfoWidget
from histoslider.ui.SlideViewerWidget_ui import Ui_SliderViewerWidget


class SlideViewerWidget(QWidget, Ui_SliderViewerWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)

        self.slide_viewer = SlideGraphicsView(self)
        self.slide_info_widget = SlideInfoWidget(self.slide_viewer)

        self.verticalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.slide_viewer)
        self.verticalLayout.addWidget(self.slide_info_widget)

    @property
    def toolbar(self) -> QToolBar:
        toolbar = QToolBar()

        set_grid_size_action = QAction("Grid size", self)
        set_grid_size_action.triggered.connect(self.set_grid_size)
        toolbar.addAction(set_grid_size_action)

        show_grid_action = QAction(QIcon(":/icons/grid.png"), "Show Grid", self)
        show_grid_action.setCheckable(True)
        show_grid_action.triggered.connect(self.show_grid)
        toolbar.addAction(show_grid_action)

        go_to_action = QAction("Go To", self)
        go_to_action.triggered.connect(self.go_to)
        toolbar.addAction(go_to_action)

        take_screenshot_action = QAction("Take screenshot", self)
        take_screenshot_action.triggered.connect(self.take_screenshot)
        toolbar.addAction(take_screenshot_action)

        print_items_action = QAction("Print items", self)
        print_items_action.triggered.connect(self.print_items)
        toolbar.addAction(print_items_action)

        print_slide_view_params_action = QAction("Print slide params", self)
        print_slide_view_params_action.triggered.connect(self.print_slide_view_params)
        toolbar.addAction(print_slide_view_params_action)

        return toolbar

    def set_grid_size(self):
        dialog = GridSizeDialog()
        res = dialog.exec()
        if res == QDialog.Accepted:
            rects, color_alphas = build_rects_and_color_alphas_for_grid(
                dialog.get_size(),
                self.slide_viewer.slide_helper.get_level_size(0)
            )
            self.slide_viewer.slide_graphics.update_grid_rects_0_level(rects, color_alphas)

    def show_grid(self, state: bool):
        self.slide_viewer.slide_graphics.update_grid_visibility(state)

    def go_to(self):
        dialog = GoToDialog()
        res = dialog.exec()
        if res == QDialog.Accepted:
            slide_path = self.slide_viewer.slide_helper.slide_path
            self.slide_viewer.load(SlideViewParams(slide_path, dialog.get_level(), dialog.get_rect()))

    def take_screenshot(self):
        dialog = ScreenshotDialog()
        res = dialog.exec()
        if res == QDialog.Accepted:
            image = build_screenshot_image(
                self.slide_viewer.scene,
                dialog.get_size(),
                self.slide_viewer.get_current_view_scene_rect(),
            )
            image.save(dialog.get_filepath())

    def print_items(self):
        items = self.slide_viewer.scene.items(
            self.slide_viewer.get_current_view_scene_rect()
        )
        print(items)
        QMessageBox.information(None, "Items", str(items))

    def print_slide_view_params(self):
        str_ = to_json(self.slide_viewer.slide_view_params)
        print(str_)
        QMessageBox.information(None, "SlideViewParams", str_)
