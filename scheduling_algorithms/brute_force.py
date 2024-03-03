import numpy as np
from data_structures.graph import FullyConnectedGraph

class BruteForce:
    def __init__(self, worker_amount, task_amount):
        self.worker_amount = worker_amount
        self.task_amount = task_amount

    def run(self):
        worker_graph = FullyConnectedGraph(self.worker_amount)
        task_graph = FullyConnectedGraph(self.task_amount)

        task_subgraph = task_graph.get_adjacency_matrix(task_graph.get_nodes())

        worker_permutations = worker_graph.get_permutations(size=self.task_amount)
        # print("Total permutations: ", len(worker_permutations))
        # print(worker_permutations)

        worker_subgraph_netcost_dict = {}

        for worker_perm in worker_permutations:
            worker_subgraph = worker_graph.get_adjacency_matrix(worker_perm)
            # print("Worker subgraph")
            # print(worker_subgraph, "\n")

            # Element-wise Matrix Multiplication - Hadamard Product
            affinity_cost_subgraph = np.multiply(task_subgraph, worker_subgraph)
            # print("Affinity cost subgraph")
            # print(affinity_cost_subgraph, "\n")

            net_cost = np.sum(affinity_cost_subgraph)
            # print("Net cost of the Affinity cost subgraph")
            # print(net_cost, "\n")

            worker_subgraph_netcost_dict[worker_perm] = net_cost

        # print("Worker subgraph Net Costs: ")
        # print(worker_subgraph_netcost_dict)

        # Find the minimum value
        min_value = min(worker_subgraph_netcost_dict.values())
        # print("Lowest Net Cost: ", min_value)

        # Find all keys associated with the minimum value
        min_keys = [key for key, value in worker_subgraph_netcost_dict.items() if value == min_value]
        # print("Lowest Net Cost associated Worker subgraph permutation: ")
        # print(min_keys)

        return len(worker_permutations), min_value, min_keys