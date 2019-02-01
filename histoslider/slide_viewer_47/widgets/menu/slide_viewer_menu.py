from slide_viewer_47.common.qt.my_menu import MyMenu
from slide_viewer_47.widgets.menu.on_load_slide_action import OnLoadSlideAction
from slide_viewer_47.widgets.menu.slide_viewer_view_menu import SlideViewerViewMenu
from slide_viewer_47.widgets.slide_viewer import SlideViewer


class SlideViewerMenu(MyMenu):
    def __init__(self, title, parent, slide_viewer: SlideViewer):
        super().__init__(title, parent)
        self.slide_viewer = slide_viewer
        self.load_action = OnLoadSlideAction("&load", self, slide_viewer)
        self.view_menu = SlideViewerViewMenu("&view", self, slide_viewer)
