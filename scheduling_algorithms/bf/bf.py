from crewmen.worker import Worker
from crewmen.task import Task
from crewmen.worker_graph import WorkerGraph
from crewmen.task_graph import TaskGraph
from crewmen.globaldeployment import GlobalDeployment
from crewmen.crewmen import Crewmen

from utils.crewmen_utils import get_worker_ids, find_worker

from itertools import permutations
from typing import Dict

class BruteForce:
    def __init__(self, workers: list[Worker], tasks: list[Task], worker_graph: WorkerGraph, task_graph: TaskGraph):
        self.workers = workers
        self.tasks = tasks
        self.worker_graph = worker_graph
        self.task_graph = task_graph

    def run(self):
        wm = Crewmen()        

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


            # Crewmen Monitoring Functions
            net_cost = wm.net_cost(self.task_graph.network.get_weighted_edge_list())
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
   