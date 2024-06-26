import uuid

from crewmen.worker import Worker
# from crewmen.task import Task

from typing import Dict

class GlobalDeployment:
    def __init__(self, id = "d_" + uuid.uuid4().hex[:6],):
        # Meta Data
        self.id = id
        # Deployment
        self.deployment_map: Dict[str, list[str]] = {}

    def get_key_for_value(self, value):
        for key, values in self.deployment_map.items():
            if value in values:
                return key
        return None
    
    def save_deployment(self, workers: list[Worker]):
        for w in workers:
            t_ids = w.get_deployment_ids()
            for t in t_ids:
                self.record_deployment(w.id, t)

    def record_deployment(self, k: str, v: str):
        if k in self.deployment_map:
            self.deployment_map[k].append(v)
        else:
            self.deployment_map[k] = [v]

    def colocate_deployment(self, value, src_key, dest_key):
        if src_key in self.deployment_map:
            if value in self.deployment_map[src_key]:
                self.deployment_map[src_key].remove(value)
                self.deployment_map.setdefault(dest_key, []).append(value)
                return True  # Value moved successfully
        return False  # Either source key or value not found

    def get_display_text(self):
        return f"Deployment ID: {self.id} | Deployment Map: {self.deployment_map}"

    
    def get_global_deployment_spec(self):
        return self.deployment_map
    
    def get_total_colocations(self, comparing_deployment_map: Dict[str, list[str]]):
        total_changed_values = 0

        for key, values in self.deployment_map.items():
            for value in values:
                if value not in comparing_deployment_map[key]:
                    total_changed_values += 1

        return total_changed_values
    
    def __str__(self):
        return self.get_display_text()