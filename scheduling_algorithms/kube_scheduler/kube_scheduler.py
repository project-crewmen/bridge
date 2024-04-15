import random

from crewmen.worker import Worker
from crewmen.task import Task
from crewmen.worker_graph import WorkerGraph
from crewmen.task_graph import TaskGraph
from crewmen.task_affinity_graph import TaskAffinityGraph
from crewmen.globaldeployment import GlobalDeployment
from crewmen.crewmen import Crewmen
from crewmen.affinity_cost import AffinityCost

from utils.crewmen_utils import  find_task, find_worker

def select_candidate_workers(workers: list[Worker], task: Task) -> list[Worker]:
    return workers

def score_workers(candidate_workers: list[Worker]) -> list[Worker]:
    return candidate_workers

def pick_worker(candidate_workers: list[Worker]) -> Worker:
    return random.choice(candidate_workers)


class KubeScheduler:
     def __init__(self, workers: list[Worker], tasks: list[Task], worker_graph: WorkerGraph, task_affinity_graph: TaskAffinityGraph):
        self.workers = workers
        self.tasks = tasks
        self.worker_graph = worker_graph
        self.task_affinity_graph = task_affinity_graph
     
     def run(self):
        wm = Crewmen()

        # Save previous deployment
        previous_deployment = GlobalDeployment(f"previous_deployment")
        previous_deployment.save_deployment(self.workers)
        # print("previous_deployment", previous_deployment)

        # Create a new deployment
        kube_sched_deployment = GlobalDeployment(f"kube_sched_deployment")
        kube_sched_deployment.save_deployment(self.workers)
        # print("kube_sched_deployment", kube_sched_deployment)

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

        # print(task_graph)

        # Net Cost
        net_cost = wm.net_cost(task_graph.network.get_weighted_edge_list())
        # print("initial netcost:", net_cost)

        # Get Affinity Cost Threshold
        t = wm.affinity_cost_threshold(task_graph.network.get_weighted_edge_list())
        # print(t)

        # Calculate Hight Affinity Costs Set
        hacs = wm.high_affinity_costs_set(task_graph.network.get_weighted_edge_list(), t)
        # print(hacs)


        # Get the Colocatable Tasks Set
        cts_ids = wm.get_colocatable_tasks_set(hacs)

        cts: list[Task] = []

        for cts_id in cts_ids:
            cts.append(find_task(self.tasks, cts_id))


        for colocatable_task in cts:
            deployed_worker_id = kube_sched_deployment.get_key_for_value(colocatable_task.id)                    
            deployed_worker = find_worker(self.workers, deployed_worker_id)
            
            """
            STEP 1 - Node Selection
            """
            candidate_workers = select_candidate_workers(self.workers, colocatable_task)

            """
            STEP 2 - Scoring and Prioritization
            """
            scored_workers = score_workers(candidate_workers)

            """
            STEP 3 - Pick a node
            """
            picked_worker = pick_worker(scored_workers)

            # Colocate the task
            deployed_worker.remove_task(colocatable_task)
            picked_worker.deploy_task(colocatable_task)
            kube_sched_deployment.colocate_deployment(colocatable_task.id, deployed_worker_id, picked_worker.id)

        # Constructing Task Graph (Node: Task, Edge: Affinity)
        kube_sched_task_graph = TaskGraph()

        for i in range(0, len(self.tasks)):
            for j in range(i, len(self.tasks)):
                if i != j:
                        # Find Tasks
                        x_task = find_task(self.tasks, f"t_{i}")
                        y_task = find_task(self.tasks, f"t_{j}")

                        # Find Affinity Cost
                        associated_affinity_cost =  AffinityCost(self.worker_graph, x_task, y_task, self.task_affinity_graph.network.get_edge_weight(x_task.id, y_task.id))

                        if x_task and y_task and associated_affinity_cost:
                            kube_sched_task_graph.add_affinity_cost(x_task, y_task, associated_affinity_cost)

        # print(kube_sched_task_graph)

        # Net Cost
        kube_sched_net_cost = wm.net_cost(kube_sched_task_graph.network.get_weighted_edge_list())
        # print(kube_sched_net_cost)

        total_colocations = kube_sched_deployment.get_total_colocations(previous_deployment.deployment_map)

        return kube_sched_deployment, kube_sched_net_cost, total_colocations