from histoslider.models.WorkspaceData import WorkspaceData


class DataManager:
    workspace = WorkspaceData("Workspace")

    @staticmethod
    def load_workspace(path: str):
        with open(path, 'r') as file:
            workspace = WorkspaceData.from_json(file.read())
        workspace.path = path
        DataManager.workspace = workspace
        return workspace

    @staticmethod
    def save_workspace(path: str):
        DataManager.workspace.path = path
        with open(path, 'w') as file:
            file.write(WorkspaceData.to_json(DataManager.workspace))
