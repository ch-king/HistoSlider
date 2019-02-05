from PyQt5.QtCore import (
    QPoint,
    Qt,
    QEvent,
    QRect,
    QSize,
    QRectF,
    QMarginsF,
    QObject)
from PyQt5.QtGui import QWheelEvent, QMouseEvent, QTransform, QShowEvent
from PyQt5.QtWidgets import (
    QWidget,
    QGraphicsView,
    QVBoxLayout,
    QRubberBand)

from openslide_viewer.SlideGraphicsScene import SlideGraphicsScene
from openslide_viewer.SlideGraphicsView import SlideGraphicsView
from openslide_viewer.common.SlideHelper import SlideHelper
from openslide_viewer.common.SlideViewParams import SlideViewParams
from openslide_viewer.graphics.SlideGraphicsItemGroup import SlideGraphicsItemGroup
from ui import SlideViewerWidget
from ui.SlideInfoWidget import SlideInfoWidget


class SlideViewer(QWidget):
    # eventSignal = pyqtSignal(QEvent)

    def __init__(self, parent: SlideViewerWidget):
        super().__init__(parent)
        self.slide_viewer_widget = parent
        self.scene = SlideGraphicsScene(self)
        self.view = SlideGraphicsView(self.scene, self.on_view_changed)
        self.view.viewport().installEventFilter(self)

        self.rubber_band = QRubberBand(QRubberBand.Rectangle, self.view)
        self.mouse_press_view = None

        self.scale_initializer_deffered_function = None
        self.slide_view_params = None
        self.slide_helper = None

        layout = QVBoxLayout(self)
        layout.addWidget(self.view)
        self.setLayout(layout)

    """
    If you want to start view from some point at some level, specify <level> and <level_rect> params.
    level_rect : rect in dimensions of slide at level=level. If None - fits the whole size of slide
    """

    def load(
        self,
        slide_view_params: SlideViewParams,
        preffered_rects_count=2000,
        zoom_step=1.15,
    ):
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
            self.view.resetTransform()
            # print("size when loading: ", self.view.viewport().size())
            if self.slide_view_params.level_rect:
                # self.view.fitInView(QRectF(*self.slide_view_params.level_rect), Qt.KeepAspectRatioByExpanding)
                self.view.fitInView(
                    QRectF(*self.slide_view_params.level_rect), Qt.KeepAspectRatio
                )
                # print("after fit: ", self.get_current_view_scene_rect())
            else:
                start_margins = QMarginsF(200, 200, 200, 200)
                start_image_rect_ = self.slide_helper.get_rect_for_level(
                    self.slide_view_params.level
                )
                self.view.fitInView(
                    start_image_rect_ + start_margins, Qt.KeepAspectRatio
                )

        self.scale_initializer_deffered_function = scale_initializer_deffered_function

    def eventFilter(self, qobj: QObject, event: QEvent):
        # self.eventSignal.emit(event)
        event_processed = False
        # print("size when event: ", event, event.type(), self.view.viewport().size())
        if isinstance(event, QShowEvent):
            """
            we need it deffered because fitInView logic depends on current viewport size. Expecting at this point widget is finally resized before being shown at first
            """
            if self.scale_initializer_deffered_function:
                # TODO labels start to occupy some space after view was already fitted, and labels will reduce size of viewport
                self.scale_initializer_deffered_function()
                self.on_view_changed()
                self.scale_initializer_deffered_function = None
        elif isinstance(event, QWheelEvent):
            event_processed = self.process_viewport_wheel_event(event)
            # we handle wheel event to prevent GraphicsView interpret it as scrolling
        elif isinstance(event, QMouseEvent):
            event_processed = self.process_mouse_event(event)

        return event_processed

    def process_viewport_wheel_event(self, event: QWheelEvent):
        # print("size when wheeling: ", self.view.viewport().size())
        zoom_in = self.zoom_step
        zoom_out = 1 / zoom_in
        zoom = zoom_in if event.angleDelta().y() > 0 else zoom_out
        self.update_scale(event.pos(), zoom)
        event.accept()
        # self.on_view_changed()
        return True

    def process_mouse_event(self, event: QMouseEvent):
        if self.slide_helper is None:
            return False

        if event.button() == Qt.MiddleButton:
            if event.type() == QEvent.MouseButtonPress:
                self.slide_graphics.update_grid_visibility(
                    not self.slide_graphics.slide_view_params.grid_visible
                )
                return True
        elif event.button() == Qt.LeftButton:
            if event.type() == QEvent.MouseButtonPress:
                self.view.setDragMode(QGraphicsView.ScrollHandDrag)
                return False
            elif event.type() == QEvent.MouseButtonRelease:
                self.view.setDragMode(QGraphicsView.NoDrag)
                return False
        elif event.button() == Qt.RightButton:
            if event.type() == QEvent.MouseButtonPress:
                self.view.setDragMode(QGraphicsView.RubberBandDrag)
                self.mouse_press_view = QPoint(event.pos())
                self.rubber_band.setGeometry(QRect(self.mouse_press_view, QSize()))
                self.rubber_band.show()
                return True
            elif event.type() == QEvent.MouseButtonRelease:
                self.view.setDragMode(QGraphicsView.NoDrag)
                self.rubber_band.hide()
                self.remember_selected_rect_params()
                self.slide_graphics.update_selected_rect_0_level(
                    self.slide_view_params.selected_rect_0_level
                )
                self.slide_viewer_widget.slide_info_widget.update_labels()
                self.scene.invalidate()
                self.mouse_press_view = None
                return True
        elif event.type() == QEvent.MouseMove:
            self.slide_viewer_widget.slide_info_widget.update_mouse_pos(self.view.mapToScene(event.pos()))
            if self.mouse_press_view:
                self.rubber_band.setGeometry(
                    QRect(self.mouse_press_view, event.pos()).normalized()
                )
                return True

        return False

    def remember_selected_rect_params(self):
        pos_scene = self.view.mapToScene(self.rubber_band.pos())
        rect_scene = self.view.mapToScene(self.rubber_band.rect()).boundingRect()
        downsample = self.slide_helper.get_downsample_for_level(
            self.slide_view_params.level
        )
        selected_qrectf_0_level = QRectF(
            pos_scene * downsample, rect_scene.size() * downsample
        )
        self.slide_view_params.selected_rect_0_level = selected_qrectf_0_level.getRect()

    def update_scale(self, mouse_pos: QPoint, zoom: float):
        old_mouse_pos_scene = self.view.mapToScene(mouse_pos)
        old_view_scene_rect = self.view.mapToScene(
            self.view.viewport().rect()
        ).boundingRect()

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
        self.view.reset_view_transform()
        self.view.setTransform(transform, False)
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

    def get_current_view_scene_rect(self):
        return self.view.mapToScene(self.view.viewport().rect()).boundingRect()

    def get_current_view_scale(self):
        scale = self.view.transform().m11()
        return scale
