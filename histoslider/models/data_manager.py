from histoslider.models.workspace_model import WorkspaceModel


class DataManager:
    workspace_model = WorkspaceModel()

    @staticmethod
    def load_workspace(path: str):
        DataManager.workspace_model.beginResetModel()
        DataManager.workspace_model.load_workspace(path)
        DataManager.workspace_model.endResetModel()

    @staticmethod
    def save_workspace(path: str):
        DataManager.workspace_model.save_workspace(path)
