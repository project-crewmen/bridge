from crewmen.worker import Worker
from crewmen.task import Task
from crewmen.worker_graph import WorkerGraph
from crewmen.task_graph import TaskGraph
from crewmen.task_affinity_graph import TaskAffinityGraph
from crewmen.globaldeployment import GlobalDeployment
from crewmen.crewmen import Crewmen
from crewmen.affinity_cost import AffinityCost

from utils.crewmen_utils import  find_task

class EPVM:
     def __init__(self, workers: list[Worker], tasks: list[Task], worker_graph: WorkerGraph, task_affinity_graph: TaskAffinityGraph):
        self.workers = workers
        self.tasks = tasks
        self.worker_graph = worker_graph
        self.task_affinity_graph = task_affinity_graph
     
     def run(self):
        wm = Crewmen()

        # Save previous deployment
        previous_deployment = GlobalDeployment(f"previous_deployment")

        for w in self.workers:
            t_ids = w.get_deployment_ids()
            for t in t_ids:
                  previous_deployment.record_deployment(w.id, t)