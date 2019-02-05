from PyQt5.QtCore import (
    QPoint,
    Qt,
    QRect,
    QSize,
    QRectF,
    QMarginsF)
from PyQt5.QtGui import QWheelEvent, QMouseEvent, QTransform
from PyQt5.QtWidgets import (
    QGraphicsView,
    QRubberBand)

from openslide_viewer.SlideGraphicsScene import SlideGraphicsScene
from openslide_viewer.common.SlideHelper import SlideHelper
from openslide_viewer.common.SlideViewParams import SlideViewParams
from openslide_viewer.graphics.SlideGraphicsItemGroup import SlideGraphicsItemGroup
from ui import SlideViewerWidget


class SlideGraphicsView(QGraphicsView):
    def __init__(self, parent: SlideViewerWidget):
        super().__init__(parent)
        self.slide_viewer_widget = parent
        self.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.horizontalScrollBar().sliderMoved.connect(self.on_view_changed)
        self.verticalScrollBar().sliderMoved.connect(self.on_view_changed)

        self.scene = SlideGraphicsScene()
        self.setScene(self.scene)

        self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)

        self.mouse_press_view = None
        self.scale_initializer_deffered_function = None
        self.slide_view_params = None
        self.slide_helper = None

    """
    If you want to start view from some point at some level, specify <level> and <level_rect> params.
    level_rect : rect in dimensions of slide at level=level. If None - fits the whole size of slide
    """

    def load(self, slide_view_params: SlideViewParams, preffered_rects_count: int = 2000, zoom_step: float = 1.15):
        self.zoom_step = zoom_step
        self.slide_view_params = slide_view_params
        self.slide_helper = SlideHelper(slide_view_params.slide_path)

        self.slide_graphics = SlideGraphicsItemGroup(
            slide_view_params, preffered_rects_count
        )
        self.scene.clear()
        self.scene.addItem(self.slide_graphics)

        if self.slide_view_params.level == -1 or self.slide_view_params.level is None:
            self.slide_view_params.level = self.slide_helper.max_level

        self.slide_graphics.update_visible_level(self.slide_view_params.level)
        self.scene.setSceneRect(
            self.slide_helper.get_rect_for_level(self.slide_view_params.level)
        )

        def scale_initializer_deffered_function():
            self.resetTransform()
            # print("size when loading: ", self.view.viewport().size())
            if self.slide_view_params.level_rect:
                # self.view.fitInView(QRectF(*self.slide_view_params.level_rect), Qt.KeepAspectRatioByExpanding)
                self.fitInView(
                    QRectF(*self.slide_view_params.level_rect), Qt.KeepAspectRatio
                )
                # print("after fit: ", self.get_current_view_scene_rect())
            else:
                start_margins = QMarginsF(200, 200, 200, 200)
                start_image_rect_ = self.slide_helper.get_rect_for_level(
                    self.slide_view_params.level
                )
                self.fitInView(
                    start_image_rect_ + start_margins, Qt.KeepAspectRatio
                )

        self.scale_initializer_deffered_function = scale_initializer_deffered_function

    def showEvent(self, QShowEvent):
        """
        We need it deffered because fitInView logic depends on current viewport size. Expecting at this point widget is finally resized before being shown at first
        """
        if self.scale_initializer_deffered_function:
            # TODO labels start to occupy some space after view was already fitted, and labels will reduce size of viewport
            self.scale_initializer_deffered_function()
            self.on_view_changed()
            self.scale_initializer_deffered_function = None

    def mousePressEvent(self, event: QMouseEvent):
        if self.slide_helper is not None:
            if event.button() == Qt.MiddleButton:
                self.slide_graphics.update_grid_visibility(not self.slide_graphics.slide_view_params.grid_visible)
            elif event.button() == Qt.LeftButton:
                self.setDragMode(QGraphicsView.ScrollHandDrag)
            elif event.button() == Qt.RightButton:
                # self.setDragMode(QGraphicsView.RubberBandDrag)
                self.mouse_press_view = QPoint(event.pos())
                self.rubber_band.setGeometry(QRect(self.mouse_press_view, QSize()))
                self.rubber_band.show()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.slide_helper is not None:
            if event.button() == Qt.LeftButton:
                self.setDragMode(QGraphicsView.NoDrag)
            elif event.button() == Qt.RightButton:
                self.setDragMode(QGraphicsView.NoDrag)
                self.rubber_band.hide()
                pos_scene = self.mapToScene(self.rubber_band.pos())
                rect_scene = self.mapToScene(self.rubber_band.rect()).boundingRect()
                downsample = self.slide_helper.get_downsample_for_level(self.slide_view_params.level)
                selected_qrectf_0_level = QRectF(pos_scene * downsample, rect_scene.size() * downsample)
                self.slide_view_params.selected_rect_0_level = selected_qrectf_0_level.getRect()
                self.slide_graphics.update_selected_rect_0_level(self.slide_view_params.selected_rect_0_level)
                self.slide_viewer_widget.slide_info_widget.update_labels()
                self.scene.invalidate()
                self.mouse_press_view = None
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.slide_helper is not None:
            self.slide_viewer_widget.slide_info_widget.update_mouse_pos(self.mapToScene(event.pos()))
            if self.mouse_press_view:
                self.rubber_band.setGeometry(QRect(self.mouse_press_view, event.pos()).normalized())
        super().mouseMoveEvent(event)

    def wheelEvent(self, event: QWheelEvent):
        zoom_in = self.zoom_step
        zoom_out = 1 / zoom_in
        zoom = zoom_in if event.angleDelta().y() > 0 else zoom_out
        self.update_scale(event.pos(), zoom)

    def update_scale(self, mouse_pos: QPoint, zoom: float):
        old_mouse_pos_scene = self.mapToScene(mouse_pos)
        old_view_scene_rect = self.mapToScene(self.viewport().rect()).boundingRect()

        old_level = self.get_best_level_for_scale(self.get_current_view_scale())
        old_level_downsample = self.slide_helper.get_downsample_for_level(old_level)
        new_level = self.get_best_level_for_scale(self.get_current_view_scale() * zoom)
        new_level_downsample = self.slide_helper.get_downsample_for_level(new_level)

        level_scale_delta = 1 / (new_level_downsample / old_level_downsample)

        r = old_view_scene_rect.topLeft()
        m = old_mouse_pos_scene
        new_view_scene_rect_top_left = (m - (m - r) / zoom) * level_scale_delta
        new_view_scene_rect = QRectF(
            new_view_scene_rect_top_left,
            old_view_scene_rect.size() * level_scale_delta / zoom,
        )

        new_scale = (
            self.get_current_view_scale()
            * zoom
            * new_level_downsample
            / old_level_downsample
        )
        transform = (
            QTransform()
                .scale(new_scale, new_scale)
                .translate(-new_view_scene_rect.x(), -new_view_scene_rect.y())
        )

        new_rect = self.slide_helper.get_rect_for_level(new_level)
        self.scene.setSceneRect(new_rect)
        self.slide_view_params.level = new_level
        self.reset_view_transform()
        self.setTransform(transform, False)
        self.slide_graphics.update_visible_level(new_level)
        self.slide_viewer_widget.slide_info_widget.update_labels()

    def get_best_level_for_scale(self, scale: float):
        scene_width = self.scene.sceneRect().size().width()
        candidates = [0]
        for level in self.slide_helper.levels:
            w, h = self.slide_helper.get_level_size(level)
            if scene_width * scale <= w:
                candidates.append(level)
        best_level = max(candidates)
        return best_level

    def on_view_changed(self):
        if self.scale_initializer_deffered_function is None and self.slide_view_params:
            self.slide_view_params.level_rect = (
                self.get_current_view_scene_rect().getRect()
            )
        self.slide_viewer_widget.slide_info_widget.update_labels()

    def reset_view_transform(self):
        self.resetTransform()
        self.horizontalScrollBar().setValue(0)
        self.verticalScrollBar().setValue(0)

    def mouseDoubleClickEvent(self, event):
        point = self.mapToScene(event.pos())
        x = point.x()
        y = point.y()
        self.centerOn(x, y)
        super().mouseDoubleClickEvent(event)

    def get_current_view_scene_rect(self):
        return self.mapToScene(self.viewport().rect()).boundingRect()

    def get_current_view_scale(self):
        scale = self.transform().m11()
        return scale
