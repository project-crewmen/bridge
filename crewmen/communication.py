import uuid

class Communication:
    def __init__(self, x_task, y_task, message_passed, data_exchanged):
        # Meta Data
        self.x_task = x_task
        self.y_task = y_task
        self.message_passed = message_passed
        self.data_exchanged = data_exchanged