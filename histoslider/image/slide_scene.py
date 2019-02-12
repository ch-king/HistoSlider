from PyQt5.QtWidgets import QGraphicsScene


class SlideScene(QGraphicsScene):
    def __init__(self):
        QGraphicsScene.__init__(self)
        self.current_downsample = 1
        self.current_xywhds = (0, 0, 0, 0, 1)
        self.dirty = True

    def reset(self):
        # reset variables
        self.current_downsample = 1
        self.current_xywhds = (0, 0, 0, 0, 1)
        # remove the old pixelmap
        self.clear()
        self.dirty = True

    def paint_view(self, view, x: int, y: int, w: int, h: int, downsample: float):
        if ((x, y, w, h, downsample) == self.current_xywhds) and not self.dirty:
            return
        else:
            self.current_xywhds = (x, y, w, h, downsample)

        if self.current_downsample == downsample:
            # only update objects if downsample does not change
            # as when upon change of zoom the window changes as well
            for item in self.items():
                if hasattr(item, 'update_content'):
                    item.update_content(x, y, w, h, downsample)

        if self.current_downsample != downsample:
            view.scale(self.current_downsample / downsample, self.current_downsample / downsample)
            self.current_downsample = downsample

        self.dirty = False
