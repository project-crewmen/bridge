from crewmen.crewmen import Crewmen
from crewmen.worker_graph import WorkerGraph
from crewmen.worker import Worker
from crewmen.task import Task

class AffinityCost:
    def __init__(self, worker_graph: WorkerGraph, t1: Task, t2: Task, affinity: float):
        self.worker_graph = worker_graph
        self.t1 = t1
        self.t2 = t2
        self.affinity = affinity
        self.wm = Crewmen()

    def get_affinity_cost(self):
        t1_deployed_worker = None 
        t2_deployed_worker = None 

        for w in self.worker_graph.workers:
            if self.t1 in w.deployments:
                t1_deployed_worker = w
            if self.t2 in w.deployments:
                t2_deployed_worker = w
        
        if t1_deployed_worker is None or t2_deployed_worker is None:            
            return None 

        ac = self.wm.affinity_cost(
            self.affinity,
            self.worker_graph.network.get_edge_weight(t1_deployed_worker.id, t2_deployed_worker.id),
            1.0
        )

        return ac