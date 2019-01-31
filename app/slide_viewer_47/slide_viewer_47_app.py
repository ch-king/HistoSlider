import sys

from PyQt5.QtGui import QPixmapCache
from PyQt5.QtWidgets import QApplication

from slide_viewer_47.common.slide_view_params import SlideViewParams
from slide_viewer_47.widgets.slide_viewer_main_window import SlideViewerMainWindow


def excepthook(excType, excValue, tracebackobj):
    print(excType, excValue, tracebackobj)


sys.excepthook = excepthook

if __name__ == "__main__":
    app = QApplication(sys.argv)
    cache_size_in_kb = 700 * 10 ** 3
    QPixmapCache.setCacheLimit(cache_size_in_kb)

    win = SlideViewerMainWindow()
    win.show()

    slide_path = "/home/anton/Downloads/CMU-1.tiff"
    slide_view_params = SlideViewParams(slide_path)
    win.slide_viewer.load(slide_view_params)

    sys.exit(app.exec_())
