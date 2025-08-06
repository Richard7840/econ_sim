class ProjectInstance:
    def __init__(self, project_id: str, target: str = None):
        self.project_id = project_id
        self.current_cp = 0
        self.target = target
