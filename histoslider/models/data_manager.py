from histoslider.models.tree_model import TreeModel
from histoslider.models.workspace_data import WorkspaceData


class DataManager:
    workspace = WorkspaceData("Workspace")
    tree_model = TreeModel(workspace)

    @staticmethod
    def load_workspace(path: str):
        with open(path, 'r') as file:
            workspace = WorkspaceData.from_json(file.read())
        workspace.path = path
        DataManager.workspace = workspace
        DataManager.tree_model = TreeModel(DataManager.workspace)
        return workspace

    @staticmethod
    def save_workspace(path: str):
        DataManager.workspace.path = path
        with open(path, 'w') as file:
            file.write(WorkspaceData.to_json(DataManager.workspace))
