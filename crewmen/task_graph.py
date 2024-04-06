from data_structures.graph import Graph
from crewmen.task import Task
from crewmen.affinity_cost import AffinityCost

class TaskGraph:
    def __init__(self):
        self.network = Graph()
        self.tasks: list[Task] = []

    def add_task(self, task: Task):
        self.tasks.append(task)
        self.network.add_node(task.id)

    def add_affinity_cost(self, x: Task, y: Task, weight: AffinityCost):
        self.tasks.append(x)
        self.tasks.append(y)
        self.network.add_edge(x.id, y.id, weight=weight.get_affinity_cost())

    def __str__(self):
        return str(self.network.get_adjacency_matrix(self.network.get_nodes()))