from data_structures.graph import Graph
from crewmen.task import Task

class TaskAffinityGraph:
    def __init__(self):
        self.network = Graph()
        self.tasks: list[Task] = []

    def add_task(self, task: Task):
        self.tasks.append(task)
        self.network.add_node(task.id)

    def add_affinity(self, x: Task, y: Task, weight: float):
        self.tasks.append(x)
        self.tasks.append(y)
        self.network.add_edge(x.id, y.id, weight=weight)

    def get_task_affinity_graph_spec(self):
        return self.network.get_adjacency_matrix(self.network.get_nodes())