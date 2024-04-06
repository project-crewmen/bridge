from crewmen.worker import Worker
from crewmen.task import Task
from crewmen.worker_graph import WorkerGraph
from crewmen.task_graph import TaskGraph
from crewmen.task_affinity_graph import TaskAffinityGraph
from crewmen.globaldeployment import GlobalDeployment
from crewmen.crewmen import Crewmen
from crewmen.affinity_cost import AffinityCost

from utils.crewmen_utils import get_worker_ids, find_worker, find_task, find_link

from itertools import permutations
from typing import Dict

class BinPack:
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
            previous_deployment.record_deployment(w.id, t_ids)

        # print(previous_deployment)

        # Clear previous deployment
        for w in self.workers:
            w.clear_deployments()

        cleared_deployment = GlobalDeployment(f"cleared_deployment")

        for w in self.workers:
            t_ids = w.get_deployment_ids()
            cleared_deployment.record_deployment(w.id, t_ids)

        # print(cleared_deployment)

        # Get the first worker and deploy tasks as much as possible, then move to next worker, and continue + Record the new deployment
        binpacked_deployment = GlobalDeployment(f"binpacked_deployment")

        k = 0
        for candidate_worker in self.workers:
            if(k < len(self.tasks)-1):
                for t in range(k, len(self.tasks)):
                    deploying_task = self.tasks[t]
                    if(candidate_worker.can_deploy_task(deploying_task)):
                        candidate_worker.deploy_task(deploying_task)
                        binpacked_deployment.record_deployment(candidate_worker.id, deploying_task.id)
                        k = t
                    else:
                        k = t
                        break
            else:
                break
            
        # print(binpacked_deployment)

        # Constructing Task Graph (Node: Task, Edge: Affinity)
        task_graph = TaskGraph()

        for i in range(0, len(self.tasks)):
            for j in range(i, len(self.tasks)):
                if i != j:
                    # Find Tasks
                    x_task = find_task(self.tasks, f"t_{i}")
                    y_task = find_task(self.tasks, f"t_{j}")

                    # Find Affinity Cost
                    associated_affinity_cost =  AffinityCost(self.worker_graph, x_task, y_task, self.task_affinity_graph.network.get_edge_weight(x_task.id, y_task.id))

                    if x_task and y_task and associated_affinity_cost:
                        task_graph.add_affinity_cost(x_task, y_task, associated_affinity_cost)


        # Crewmen Monitoring Functions
        net_cost = wm.net_cost(task_graph.network.get_weighted_edge_list())
        # print("Net Cost: ", net_cost, "\n")

        return binpacked_deployment, net_cost