import uuid

# from crewmen.worker import Worker
# from crewmen.task import Task

from typing import Dict

class GlobalDeployment:
    def __init__(self, id = "d_" + uuid.uuid4().hex[:6],):
        # Meta Data
        self.id = id
        # Deployment
        self.deployment_map: Dict[str, list[str]] = {}

    def record_deployment(self, k: str, v: str):
        if k in self.deployment_map:
            self.deployment_map[k].append(v)
        else:
            self.deployment_map[k] = [v]

    def get_display_text(self):
        return f"Deployment ID: {self.id} | Deployment Map: {self.deployment_map}"

    def __str__(self):
        return self.get_display_text()
    
    def get_global_deployment_spec(self):
        return self.deployment_map