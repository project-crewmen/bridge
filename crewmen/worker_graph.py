from data_structures.graph import Graph
from crewmen.worker import Worker
from crewmen.link import Link

class WorkerGraph:
    def __init__(self):
        self.network = Graph()
        self.workers: list[Worker] = []

    def add_worker(self, worker: Worker):
        self.workers.append(worker)
        self.network.add_node(worker.id)

    def add_link(self, x: Worker, y: Worker, weight: Link):
        self.workers.append(x)
        self.workers.append(y)
        self.network.add_edge(x.id, y.id, weight=weight.response_time)

    def get_worker_graph_spec(self):
        return self.network.get_adjacency_matrix(self.network.get_nodes())
    
    def __str__(self):
        return str(self.network.get_adjacency_matrix(self.network.get_nodes()))
