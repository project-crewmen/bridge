import uuid

class Task:
    def __init__(self, id = "t_" + uuid.uuid4().hex[:6], cpu_required: int = 1, memory_required: int = 512, disk_required: int = 1024):
        # Meta Data
        self.id = id
        # Resource Requirements
        self.cpu_required = cpu_required
        self.memory_required = memory_required
        self.disk_required = disk_required

    def __str__(self):
        return f"{self.id}"
    
    def get_task_spec(self):
        return {
            "id": self.id,
            "cpu_required": self.cpu_required,
            "memory_required": self.memory_required,
            "disk_required": self.disk_required
        }
