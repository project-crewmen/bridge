from crewmen.worker import Worker
from crewmen.task import Task
from crewmen.link import Link
from crewmen.affinity_cost import AffinityCost
from crewmen.worker_graph import WorkerGraph
from crewmen.task_graph import TaskGraph
from crewmen.crewmen import Crewmen

import random
from itertools import permutations
from typing import Dict

def record_deployment(dict, k, v):
    if k in dict:
        dict[k].append(v)
    else:
        dict[k] = [v]

if __name__ == "__main__":
    wm = Crewmen()
 
    for w_amt in range(3, 4):
        # @desc - We have to create Links, Workers individually. And then by considering workers as nodes and links as edges we can create a fully connected worker graph
        # For instance, for 3 workers we need 4 links. Note that, l0 is always the loopback link for each nodes
        # l0 = Link(response_time=0.0)
        # l1 = Link(response_time=0.01)
        # l2 = Link(response_time=0.02)
        # l3 = Link(response_time=0.03)

        # Then workers can be created
        # w1 = Worker("w_1")
        # w2 = Worker("w_2")
        # w3 = Worker("w_3")
        
        # Finally by placing (edge, weight) pairs, we can create a fully connected worker graph
        # worker_graph.add_link(w1, w1, l0)
        # worker_graph.add_link(w2, w2, l0)
        # worker_graph.add_link(w3, w3, l0)
        # worker_graph.add_link(w1, w2, l1)
        # worker_graph.add_link(w1, w3, l2)
        # worker_graph.add_link(w2, w3, l3)
        
        # Number of Links Required
        # Since Worker Graph is a FullyConnectedGraph, for n nodes, there exists (n(n-1))/2 edges
        l_amt = (w_amt * (w_amt-1))//2

        # Populate Links Dictionary
        l_dict: Dict[str, Link] = {}
        l_dict[f"l_0"] = Link(response_time = 0.0000)
        for l in range(1, l_amt+1):
            l_dict[f"l_{l}"] = Link(response_time = round(random.uniform(0, 1), 4))

        # print(', '.join([f"{k}: {v.response_time}" for k, v in l_dict.items()]))

        # Populate Workers Dictionary
        w_dict: Dict[str, Worker] = {}
        for w in range(0, w_amt):
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
        # print(worker_graph.network.get_adjacency_matrix(worker_graph.network.get_nodes()), "\n")
        print(worker_graph.network.get_weighted_edge_list(), "\n")

        for t_amt in range(2, w_amt+1):
            # Populate Tasks Dictionary
            t_dict: Dict[str, Task] = {}
            for t in range(0, t_amt):
                t_dict[f"t_{t}"] = Task(f"t_{t}")

            print(', '.join([f"{k}: {v}" for k, v in t_dict.items()]))

            # Deployments
            # @desc - calculate and store all posible ways of r amount of tasks can be deployed on n amount of workers - nPr
            worker_permutations = list(permutations(w_dict_keys, t_amt))
            print(worker_permutations)

            
            # Deploying Tasks on Workers
            deployment_map: Dict[str, list[str]] = {}
            
            # For now, each task depoly on exactly 1 worker
            for i in range(0, len(t_dict)):
                w_dict[f"w_{i}"].deploy_task(t_dict[f"t_{i}"])
                record_deployment(deployment_map, w_dict[f"w_{i}"].id, t_dict[f"t_{i}"].id)

            print("Deployments: ")
            print(deployment_map)


            # Constructing Task Graph (Node: Task, Edge: Affinity)
            task_graph = TaskGraph()

            t_dict_keys = list(t_dict.keys())
            for i in range(0, len(t_dict_keys)):
                for j in range(i, len(t_dict_keys)):
                    if i != j:
                        task_graph.add_affinity_cost(t_dict[f"t_{i}"], t_dict[f"t_{j}"], AffinityCost(worker_graph, t_dict[f"t_{i}"], t_dict[f"t_{j}"], round(random.uniform(0, 1), 4)))
            
            print("\nTask Graph: ")
            # print(task_graph.network.get_nodes(), "\n")
            # print(task_graph.network.get_adjacency_matrix(task_graph.network.get_nodes()), "\n")
            print(task_graph.network.get_weighted_edge_list(), "\n")


            # Crewmen Monitoring Functions
            net_cost = wm.net_cost(task_graph.network.get_weighted_edge_list())
            print("Net Cost: ", net_cost, "\n")
   