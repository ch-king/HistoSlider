from PyQt5.QtCore import QRectF, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QAction,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QSpinBox,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from slide_viewer.common.json_utils import to_json
from slide_viewer.common.level_builders import build_rects_and_color_alphas_for_grid
from slide_viewer.common.qt.my_spin_box import MySpinBox
from slide_viewer.common.screenshot_builders import build_screenshot_image
from slide_viewer.common.SlideViewParams import SlideViewParams
from slide_viewer.SlideViewer import SlideViewer
from ui.SlideViewerWidget_ui import Ui_SliderViewerWidget


class SlideViewerWidget(QWidget, Ui_SliderViewerWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)

        self.slide_viewer = SlideViewer(viewer_top_else_left=True)
        self.verticalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.slide_viewer)

    @property
    def toolbar(self) -> QToolBar:
        toolbar = QToolBar()

        set_grid_size_action = QAction(QIcon(":/icons/grid.png"), "Grid Size", self)
        set_grid_size_action.triggered.connect(self.set_grid_size)
        toolbar.addAction(set_grid_size_action)

        show_grid_action = QAction("Show Grid", self)
        show_grid_action.setCheckable(True)
        show_grid_action.triggered.connect(self.show_grid)
        toolbar.addAction(show_grid_action)

        go_to_action = QAction("Go To", self)
        go_to_action.triggered.connect(self.go_to)
        toolbar.addAction(go_to_action)

        take_screenshot_action = QAction("Take Screenshot", self)
        take_screenshot_action.triggered.connect(self.take_screenshot)
        toolbar.addAction(take_screenshot_action)

        print_items_action = QAction("Print Items", self)
        print_items_action.triggered.connect(self.print_items)
        toolbar.addAction(print_items_action)

        print_slide_view_params_action = QAction("Print Slide View Params", self)
        print_slide_view_params_action.triggered.connect(self.print_slide_view_params)
        toolbar.addAction(print_slide_view_params_action)

        return toolbar

    def set_grid_size(self):
        dialog = QDialog()
        dialog.setWindowTitle("Grid size")

        # grid_size = self.slide_viewer.slide_graphics.slide_view_params.grid_size_0_level
        # if not grid_size:
        grid_size = (224, 224)

        grid_w = QSpinBox()
        grid_w.setMaximum(2 ** 15)
        grid_w.setValue(grid_size[0])

        grid_h = QSpinBox()
        grid_h.setMaximum(2 ** 15)
        grid_h.setValue(grid_size[1])

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(grid_w)
        horizontal_layout.addWidget(grid_h)
        form_layout = QFormLayout()
        form_layout.addRow("grid width:", horizontal_layout)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog
        )
        main_layout.addWidget(button_box)
        dialog.setLayout(main_layout)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        res = dialog.exec()
        if res == QDialog.Accepted:
            rects, color_alphas = build_rects_and_color_alphas_for_grid(
                (grid_w.value(), grid_h.value()),
                self.slide_viewer.slide_helper.get_level_size(0),
            )
            self.slide_viewer.slide_graphics.update_grid_rects_0_level(
                rects, color_alphas
            )

    def show_grid(self, state: bool):
        self.slide_viewer.slide_graphics.update_grid_visibility(state)

    def go_to(self):
        dialog = QDialog()
        dialog.setWindowTitle("Go to")

        level = MySpinBox(1)
        x = MySpinBox(1000)
        y = MySpinBox(1000)
        width = MySpinBox(1000)
        height = MySpinBox(1000)

        form_layout = QFormLayout()
        form_layout.addRow("level:", level)
        form_layout.addRow("x:", x)
        form_layout.addRow("y:", y)
        form_layout.addRow("width:", width)
        form_layout.addRow("height:", height)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog
        )
        main_layout.addWidget(button_box)
        dialog.setLayout(main_layout)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        res = dialog.exec()
        if res == QDialog.Accepted:
            slide_path = self.slide_viewer.slide_helper.slide_path
            qrectf = QRectF(x.value(), y.value(), width.value(), height.value())
            self.slide_viewer.load(SlideViewParams(slide_path, level.value(), qrectf))

    def take_screenshot(self):
        dialog = QDialog()
        dialog.setWindowTitle("Screenshot")

        width = MySpinBox(1000)
        height = MySpinBox(1000)
        filepath = QLineEdit("screenshot_from_menu.jpg")

        form_layout = QFormLayout()
        form_layout.addRow("width:", width)
        form_layout.addRow("height:", height)
        form_layout.addRow("filepath:", filepath)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog
        )
        main_layout.addWidget(button_box)
        dialog.setLayout(main_layout)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        res = dialog.exec()
        if res == QDialog.Accepted:
            image = build_screenshot_image(
                self.slide_viewer.scene,
                QSize(width.value(), height.value()),
                self.slide_viewer.get_current_view_scene_rect(),
            )
            image.save(filepath.text())

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
