from crewmen.worker import Worker
from crewmen.task import Task
from crewmen.link import Link
from crewmen.affinity_cost import AffinityCost
from crewmen.worker_graph import WorkerGraph
from crewmen.task_graph import TaskGraph
from crewmen.globaldeployment import GlobalDeployment
from crewmen.crewmen import Crewmen

import random
from itertools import permutations
from typing import Dict

class BruteForce:
    def __init__(self, w_amt, t_amt):
        self.w_amt = w_amt
        self.t_amt = t_amt

    def run(self):
        wm = Crewmen()
    
        # @desc - We have to create Links, Workers individually. And then by considering workers as nodes and links as edges we can create a fully connected worker graph
        # For instance, for 3 workers we need 4 links. Note that, l0 is always the loopback link for each nodes
        
        # Number of Links Required
        # Since Worker Graph is a FullyConnectedGraph, for n nodes, there exists (n(n-1))/2 edges
        l_amt = (self.w_amt * (self.w_amt-1))//2

        test_links = [0.0, 0.1, 0.2, 0.05]

        # Populate Links Dictionary
        l_dict: Dict[str, Link] = {}
        l_dict[f"l_0"] = Link(response_time = 0.0000)
        for l in range(1, l_amt+1):
            # l_dict[f"l_{l}"] = Link(response_time = round(random.uniform(0, 1), 4))
            l_dict[f"l_{l}"] = Link(response_time = test_links[l])

        # print(', '.join([f"{k}: {v.response_time}" for k, v in l_dict.items()]))

        # Populate Workers Dictionary
        w_dict: Dict[str, Worker] = {}
        for w in range(0, self.w_amt):
            w_dict[f"w_{w}"] = Worker(f"w_{w}")

        # print(', '.join([f"{k}: {v}" for k, v in w_dict.items()]))

        # Constructing Fully Connected Worker Graph (Node: Worker, Edge: Link)
        worker_graph = WorkerGraph()

        w_dict_keys = list(w_dict.keys())
        k = 1
        for i in range(0, len(w_dict_keys)):
            for j in range(i, len(w_dict_keys)):
                if i == j:
                    worker_graph.add_link(w_dict[w_dict_keys[i]], w_dict[w_dict_keys[j]], l_dict["l_0"])
                else:
                    worker_graph.add_link(w_dict[w_dict_keys[i]], w_dict[w_dict_keys[j]], l_dict[f"l_{k}"])
                    k += 1


        print("Worker Graph: ")
        # print(worker_graph.network.get_nodes(), "\n")
        print(worker_graph.network.get_adjacency_matrix(worker_graph.network.get_nodes()), "\n")
        # print(worker_graph.network.get_weighted_edge_list(), "\n")
        

        # Populate Tasks Dictionary
        t_dict: Dict[str, Task] = {}
        for t in range(0, self.t_amt):
            t_dict[f"t_{t}"] = Task(f"t_{t}")

        print("Tasks: ")
        print(', '.join([f"{k}: {v}" for k, v in t_dict.items()]), "\n")

        # Deployments
        # @desc - calculate and store all posible ways of r amount of tasks can be deployed on n amount of workers - nPr
        worker_permutations = list(permutations(w_dict_keys, self.t_amt))
        # print(worker_permutations)

        # Record net costs for each worker permutation. Note that this map called "Worker Subgraph Netcost List"
        # Key: Specific deployment | Value: Net cost for that specific deployment
        worker_subgraph_netcost_list: Dict[str, float] = {}
        
        deployments_map: Dict[str, GlobalDeployment] = {}
        
        d = 0
        for w_perm in worker_permutations:        
            # Clear workers for new deployments
            for w in w_dict.values():
                w.clear_deployments()

            # Deploying Tasks on Workers            
            deployment_map = GlobalDeployment(f"d_{d}")
            
            i = 0
            for w in w_perm:
                # Locally on workers record the Task Deployment
                w_dict[w].deploy_task(t_dict[f"t_{i}"])
                # Globally on crewmen record the Worker-Task Deployment
                deployment_map.record_deployment(w_dict[w].id, t_dict[f"t_{i}"].id)
                i += 1
        
            # Constructing Task Graph (Node: Task, Edge: Affinity)
            task_graph = TaskGraph()

            test_affinities = [[0, 1.5], [1.5, 0]]

            t_dict_keys = list(t_dict.keys())
            for i in range(0, len(t_dict_keys)):
                for j in range(i, len(t_dict_keys)):
                    if i != j:
                        # task_graph.add_affinity_cost(t_dict[f"t_{i}"], t_dict[f"t_{j}"], AffinityCost(worker_graph, t_dict[f"t_{i}"], t_dict[f"t_{j}"], round(random.uniform(0, 1), 4)))
                        task_graph.add_affinity_cost(t_dict[f"t_{i}"], t_dict[f"t_{j}"], AffinityCost(worker_graph, t_dict[f"t_{i}"], t_dict[f"t_{j}"], test_affinities[i][j]))
            
            # print("\nTask Graph: ")
            # print(task_graph.network.get_nodes(), "\n")
            print(task_graph.network.get_adjacency_matrix(task_graph.network.get_nodes()), "\n")
            # print(task_graph.network.get_weighted_edge_list(), "\n")


            # Crewmen Monitoring Functions
            net_cost = wm.net_cost(task_graph.network.get_weighted_edge_list())
            # print("Net Cost: ", net_cost, "\n")

            # Record the netcost
            worker_subgraph_netcost_list[f"d_{d}"] = net_cost

            # Record the deployment snapshot at Crewmen (Then later we can go through it and decide which deployment/deployments is/are the best)
            wm.add_to_deployments_map(f"d_{d}", deployment_map)
            d += 1

        # print(deployments_map)
        print(worker_subgraph_netcost_list)
        
        minimum_worker_subgraph_netcosts_list = wm.get_minimum_worker_subgraph_netcosts_list(worker_subgraph_netcost_list)
        print(minimum_worker_subgraph_netcosts_list)

        best_possible_worker_arrangements = wm.get_best_possible_worker_arrangements(minimum_worker_subgraph_netcosts_list)
        print(best_possible_worker_arrangements)


        # print(f"--- Workers: {self.w_amt} | Tasks: {self.t_amt} ---")
        # print("Total number of permutations: ", len(worker_permutations))
        # print("Deployment Set (Least Net Cost): ")
        # print(get_deployments_for_keys(deployments_map, best_possible_worker_arrangements), "\n")


        return len(worker_permutations), wm.get_deployments_for_keys(best_possible_worker_arrangements), minimum_worker_subgraph_netcosts_list[best_possible_worker_arrangements[0]]
   