import uuid

class Task:
    def __init__(self, id = "t_" + uuid.uuid4().hex[:6]):
        # Meta Data
        self.id = id
        # Resource Requirements
        self.cpu_required = 1
        self.memory_required = 512
        self.disk_required = 1024

    def __str__(self):
        return f"{self.id}"
