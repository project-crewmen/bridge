import uuid

class Link:
    def __init__(self, id = "t_" + uuid.uuid4().hex[:6], response_time: float = 0.1):
        # Meta Data
        self.id = id
        # Resource Requirements
        self.response_time = response_time

    def __str__(self):
        return f"{self.id}"
    
    def get_link_spec(self):
        return {
            "id": self.id,
            "response_time": self.response_time
        }