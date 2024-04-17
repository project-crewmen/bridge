from crewmen.worker import Worker
from crewmen.task import Task
from crewmen.worker_graph import WorkerGraph
from crewmen.task_graph import TaskGraph
from crewmen.task_affinity_graph import TaskAffinityGraph
from crewmen.globaldeployment import GlobalDeployment
from crewmen.crewmen import Crewmen
from crewmen.affinity_cost import AffinityCost

from utils.crewmen_utils import  find_task, find_worker


class ExtendedBinPack:
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
        # print(previous_deployment)
        
        # Sort workers based on CPU availability
        total_cpu_availability = 0
        for w in self.workers:
            total_cpu_availability += w.cpu.cores - w.cpu.cores_used

        worker_cpu_aval = []
        for w in self.workers:
            worker_cpu_aval.append((w, (w.cpu.cores - w.cpu.cores_used)/total_cpu_availability))

        # sorted_workers = sorted(self.workers, key=lambda x: x.cpu.cores, reverse=True)
        sorted_worker_cpu_aval = sorted(worker_cpu_aval, key=lambda x: x[1], reverse=True)

        sorted_workers = []
        for item in sorted_worker_cpu_aval:
            sorted_workers.append(item[0])

        # Create a new deployment
        binpacked_deployment = GlobalDeployment(f"binpacked_deployment")
        binpacked_deployment.save_deployment(self.workers)
        # print("binpacked_deployment", binpacked_deployment)

        # Constructing Task Graph (Node: Task, Edge: Affinity)
        # task_graph = TaskGraph()
        # task_graph.initialize(self.tasks, self.worker_graph, self.task_affinity_graph)
        
        # gv1 = GraphVisulizer(task_graph.network.graph)
        # gv1.show()

        # Find the tasks with high affinites
        # Net Cost
        net_cost = wm.net_cost(self.task_affinity_graph.network.get_weighted_edge_list())
        # print("initial netcost:", net_cost)

        # Get Affinity Cost Threshold
        t = wm.affinity_cost_threshold(self.task_affinity_graph.network.get_weighted_edge_list())
        # print(t)

        # Calculate Hight Affinity Set
        has = wm.high_affinity_costs_set(self.task_affinity_graph.network.get_weighted_edge_list(), t)
        # print(has)

        unique_tasks = []

        for u, v, w in has:
            if u not in unique_tasks:
                unique_tasks.append(u)
            if v not in unique_tasks:
                unique_tasks.append(v)
       
        # print(unique_tasks)

        k = 0
        for candidate_worker in sorted_workers:
            if(k < len(unique_tasks)):
                for t in range(k, len(unique_tasks)):
                    colocatable_task = find_task(self.tasks, unique_tasks[t])

                    deployed_worker_id = binpacked_deployment.get_key_for_value(colocatable_task.id)                    
                    deployed_worker = find_worker(self.workers, deployed_worker_id)

                    if(candidate_worker.can_deploy_task(colocatable_task)):
                        # Colocate the task
                        deployed_worker.remove_task(colocatable_task)
                        candidate_worker.deploy_task(colocatable_task)
                        binpacked_deployment.colocate_deployment(colocatable_task.id, deployed_worker_id, candidate_worker.id)
                        k = t+1
                    else:
                        k = t
                        break
            else:
                break
            
        # print(binpacked_deployment)

        # Constructing Task Graph (Node: Task, Edge: Affinity)
        bp_task_graph = TaskGraph()
        bp_task_graph.initialize(self.tasks, self.worker_graph, self.task_affinity_graph)
        # print(bp_task_graph)


        # Crewmen Monitoring Functions
        net_cost = wm.net_cost(bp_task_graph.network.get_weighted_edge_list())
        # print("Net Cost: ", net_cost, "\n")

        total_colocations = binpacked_deployment.get_total_colocations(previous_deployment.deployment_map)

        return binpacked_deployment, net_cost, total_colocations