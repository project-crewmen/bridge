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

class BruteForce:
    def __init__(self, workers: list[Worker], tasks: list[Task], worker_graph: WorkerGraph, task_affinity_graph: TaskAffinityGraph):
        self.workers = workers
        self.tasks = tasks
        self.worker_graph = worker_graph
        self.task_affinity_graph = task_affinity_graph

    def run(self):
        wm = Crewmen()

        # print(self.worker_graph.network.get_adjacency_matrix(self.worker_graph.network.get_nodes()))   
        # print(self.task_graph.network.get_adjacency_matrix(self.task_graph.network.get_nodes()))        

        # Deployments
        # @desc - calculate and store all posible ways of r amount of tasks can be deployed on n amount of workers - nPr
        worker_permutations = list(permutations(get_worker_ids(self.workers), len(self.workers)))
        # print(worker_permutations)

        # Record net costs for each worker permutation. Note that this map called "Worker Subgraph Netcost List"
        # Key: Specific deployment | Value: Net cost for that specific deployment
        worker_subgraph_netcost_list: Dict[str, float] = {}        
        
        d = 0
        for w_perm in worker_permutations:        
            # Clear workers for new deployments
            for w in self.workers:
                w.clear_deployments()

            # Deploying Tasks on Workers            
            deployment_map = GlobalDeployment(f"d_{d}")
            
            i = 0
            for w in w_perm:
                if i >= len(self.tasks):
                    i = 0
                    break

                # Locally on workers record the Task Deployment
                worker = find_worker(self.workers, w)
                worker.deploy_task(self.tasks[i])
                # Globally on crewmen record the Worker-Task Deployment
                deployment_map.record_deployment(worker.id, self.tasks[i].id)
                i += 1

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

            # Record the netcost
            worker_subgraph_netcost_list[f"d_{d}"] = net_cost

            # Record the deployment snapshot at Crewmen (Then later we can go through it and decide which deployment/deployments is/are the best)
            wm.add_to_deployments_map(f"d_{d}", deployment_map)
            d += 1
        
        minimum_worker_subgraph_netcosts_list = wm.get_minimum_worker_subgraph_netcosts_list(worker_subgraph_netcost_list)
        # print(minimum_worker_subgraph_netcosts_list)

        best_possible_worker_arrangements = wm.get_best_possible_worker_arrangements(minimum_worker_subgraph_netcosts_list)
        # print(best_possible_worker_arrangements)

        return len(worker_permutations), wm.get_deployments_for_keys(best_possible_worker_arrangements), minimum_worker_subgraph_netcosts_list[best_possible_worker_arrangements[0]]
   