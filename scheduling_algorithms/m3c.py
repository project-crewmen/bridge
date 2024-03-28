from crewmen.worker import Worker
from crewmen.task import Task
from crewmen.link import Link
from crewmen.affinity_cost import AffinityCost
from crewmen.worker_graph import WorkerGraph
from crewmen.task_graph import TaskGraph
from crewmen.crewmen import Crewmen

from typing import Dict

def record_deployment(dict, k, v):
    if k in dict:
        dict[k].append(v)
    else:
        dict[k] = [v]

def get_deployments_for_keys(deployments_map: Dict[str, Dict[str, list[str]]], keys: list[str]) -> list[Dict[str, list[str]]]:
    return [deployments_map[key] for key in keys if key in deployments_map]


class M3C:
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

        test_links = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5]

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


        # Deploying Tasks on Workers
        deployment_map: Dict[str, list[str]] = {}

        w_dict[f"w_0"].deploy_task(t_dict[f"t_0"])
        record_deployment(deployment_map, w_dict[f"w_0"].id, t_dict[f"t_0"].id)
        w_dict[f"w_1"].deploy_task(t_dict[f"t_1"])
        record_deployment(deployment_map, w_dict[f"w_1"].id, t_dict[f"t_1"].id)
        w_dict[f"w_2"].deploy_task(t_dict[f"t_2"])
        record_deployment(deployment_map, w_dict[f"w_1"].id, t_dict[f"t_1"].id)
        w_dict[f"w_3"].deploy_task(t_dict[f"t_3"])
        record_deployment(deployment_map, w_dict[f"w_1"].id, t_dict[f"t_1"].id)
        w_dict[f"w_4"].deploy_task(t_dict[f"t_4"])
        record_deployment(deployment_map, w_dict[f"w_1"].id, t_dict[f"t_1"].id)

        # Constructing Task Graph (Node: Task, Edge: Affinity)
        task_graph = TaskGraph()

        test_affinities = [
            [0, 1, 2, 3, 4],
            [1, 0, 5, 6, 7],
            [2, 5, 0, 8, 9],
            [3, 6, 8, 0, 10],
            [4, 7, 9, 10, 0],
        ]

        t_dict_keys = list(t_dict.keys())
        for i in range(0, len(t_dict_keys)):
            for j in range(i, len(t_dict_keys)):
                if i != j:
                    # task_graph.add_affinity_cost(t_dict[f"t_{i}"], t_dict[f"t_{j}"], AffinityCost(worker_graph, t_dict[f"t_{i}"], t_dict[f"t_{j}"], round(random.uniform(0, 1), 4)))
                    task_graph.add_affinity_cost(t_dict[f"t_{i}"], t_dict[f"t_{j}"], AffinityCost(worker_graph, t_dict[f"t_{i}"], t_dict[f"t_{j}"], test_affinities[i][j]))

        print("\nTask Graph: ")
        # print(task_graph.network.get_nodes(), "\n")
        print(task_graph.network.get_adjacency_matrix(task_graph.network.get_nodes()), "\n")
        # print(task_graph.network.get_weighted_edge_list(), "\n")