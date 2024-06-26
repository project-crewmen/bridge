from crewmen.worker import Worker
from crewmen.task import Task
from crewmen.worker_graph import WorkerGraph
from crewmen.task_graph import TaskGraph
from crewmen.task_affinity_graph import TaskAffinityGraph
from crewmen.globaldeployment import GlobalDeployment
from crewmen.crewmen import Crewmen

from utils.crewmen_utils import  find_task, find_worker


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
        previous_deployment.save_deployment(self.workers)
        # print(previous_deployment)
       
        
        # Sort workers based on CPU availability
        sorted_workers = sorted(self.workers, key=lambda x: x.cpu.cores - x.cpu.cores_used, reverse=True)

        # Create a new deployment
        binpacked_deployment = GlobalDeployment(f"binpacked_deployment")
        binpacked_deployment.save_deployment(self.workers)
        # print("binpacked_deployment", binpacked_deployment)

        # gv1 = GraphVisulizer(self.task_affinity_graph.network.graph)
        # gv1.show()

        # Find the tasks with high affinites
        # Net Cost
        net_cost = wm.net_cost(self.task_affinity_graph.network.get_weighted_edge_list())
        # print("initial netcost:", net_cost)

        task_affinity_list = self.task_affinity_graph.network.get_weighted_edge_list()
        sorted_task_affinity_list = sorted(task_affinity_list, key=lambda x: x[2], reverse=True)

        unique_tasks = []
        for u, v, w in sorted_task_affinity_list:
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

                    if(candidate_worker.can_deploy_task(colocatable_task) and (colocatable_task not in candidate_worker.deployments)):
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