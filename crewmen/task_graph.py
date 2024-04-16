from data_structures.graph import Graph
from crewmen.task import Task
from crewmen.worker_graph import WorkerGraph
from crewmen.affinity_cost import AffinityCost
from crewmen.task_affinity_graph import TaskAffinityGraph

from utils.crewmen_utils import find_task

class TaskGraph:
    def __init__(self):
        self.network = Graph()
        self.tasks: list[Task] = []

    def initialize(self, tasks: list[Task], worker_graph: WorkerGraph, task_affinity_graph: TaskAffinityGraph):
        for i in range(0, len(tasks)):
            for j in range(i, len(tasks)):
                if i != j:
                        # Find Tasks
                        x_task = find_task(tasks, f"t_{i}")
                        y_task = find_task(tasks, f"t_{j}")

                        # Find Affinity Cost
                        associated_affinity_cost =  AffinityCost(worker_graph, x_task, y_task, task_affinity_graph.network.get_edge_weight(x_task.id, y_task.id))

                        if x_task and y_task and associated_affinity_cost:
                            self.add_affinity_cost(x_task, y_task, associated_affinity_cost)


    def add_task(self, task: Task):
        self.tasks.append(task)
        self.network.add_node(task.id)

    def add_affinity_cost(self, x: Task, y: Task, weight: AffinityCost):
        self.tasks.append(x)
        self.tasks.append(y)
        self.network.add_edge(x.id, y.id, weight=weight.get_affinity_cost())

    def __str__(self):
        return str(self.network.get_adjacency_matrix(self.network.get_nodes()))