import math

class BruteForce:
    def __init__(self, worker_amount, task_amount):
        self.worker_amount = worker_amount
        self.task_amount = task_amount

    def run(self):

        worker_permutations_count = math.perm(self.worker_amount, self.task_amount)

        return worker_permutations_count, 0, 0