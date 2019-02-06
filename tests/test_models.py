from histoslider.models.Acquisition2DData import Acquisition2DData
from histoslider.models.SlideData import SlideData
from histoslider.models.WorkspaceData import WorkspaceData


def test_models():
    workspace = WorkspaceData("My Workspace")
    slide = SlideData("Slide")
    slide2 = SlideData("Slide 2")

    acq = Acquisition2DData("a1")
    acq2 = Acquisition2DData("a2")

    slide.add_acquisition2d(acq)
    slide2.add_acquisition2d(acq2)

    workspace.add_slide(slide)
    workspace.add_slide(slide2)
    json = workspace.to_json()

    w2 = WorkspaceData.from_json(json)

    assert json == w2.to_json()


if __name__ == "__main__":
    test_models()
