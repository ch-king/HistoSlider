from histoslider.models import SlideData
from histoslider.models.BaseData import BaseData


class WorkspaceData(BaseData):
    def __init__(self, name: str):
        super().__init__(name)
        self.path: str = None

    def add_slide(self, slide: SlideData):
        self._add_child(slide)

    def delete_slide(self, slide: SlideData):
        self._delete_child(slide)

    def find_child(self, name: str):
        child = self.children[name]
        return child
