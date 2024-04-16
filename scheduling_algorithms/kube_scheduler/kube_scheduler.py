from crewmen.worker import Worker
from crewmen.task import Task
from crewmen.worker_graph import WorkerGraph
from crewmen.task_graph import TaskGraph
from crewmen.task_affinity_graph import TaskAffinityGraph
from crewmen.globaldeployment import GlobalDeployment
from crewmen.crewmen import Crewmen
from crewmen.affinity_cost import AffinityCost

from utils.crewmen_utils import  find_task, find_worker

def calculate_priority(worker: Worker, task: Task):
    # Calculate available resources on the node
    available_cpu = worker.cpu.cores - worker.cpu.cores_used
    available_memory = worker.memory.size - worker.memory.size_used

    # Calculate resource utilization ratio
    cpu_util_ratio = task.cpu_required / available_cpu
    memory_util_ratio = task.memory_required / available_memory

    # Priority calculation: lower utilization ratio indicates higher priority
    priority_score = 1 / (cpu_util_ratio + memory_util_ratio)

    return priority_score

def select_candidate_workers(workers: list[Worker], task: Task) -> list[Worker]:
    candidate_workers: list[Worker] = []

    for w in workers:
        if(w.can_deploy_task(task)):
            candidate_workers.append(w)

    return candidate_workers

def score_workers(candidate_workers: list[Worker], task: Task) -> list[Worker]:
    # Score workers based on resource availability
    scored_workers: list[(Worker, float)] = []
    for w in candidate_workers:
        scored_workers.append((w, calculate_priority(w, task)))

    
    return scored_workers

def pick_worker(scored_workers: list[(Worker, float)]) -> Worker:
    prioritized_workers = sorted(scored_workers, key=lambda x: x[1], reverse=True)

    # print(prioritized_workers)

    return prioritized_workers[0][0]


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
        task_graph.initialize(self.tasks, self.worker_graph, self.task_affinity_graph)
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
            scored_workers = score_workers(candidate_workers, colocatable_task)

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
        kube_sched_task_graph.initialize(self.tasks, self.worker_graph, self.task_affinity_graph)
        # print(kube_sched_task_graph)

        # Net Cost
        kube_sched_net_cost = wm.net_cost(kube_sched_task_graph.network.get_weighted_edge_list())
        # print(kube_sched_net_cost)

        total_colocations = kube_sched_deployment.get_total_colocations(previous_deployment.deployment_map)

        return kube_sched_deployment, kube_sched_net_cost, total_colocations