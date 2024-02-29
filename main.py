import numpy as np
from data_structures.graph import Graph, FullyConnectedGraph

# Example usage:
if __name__ == "__main__":
    worker_amount = 5
    task_amount = 3

    worker_graph = FullyConnectedGraph(worker_amount)
    task_graph = FullyConnectedGraph(task_amount)

    worker_subgraph_dict = {}

    combination_size = task_amount  # Change this to the desired combination size
    permutations = worker_graph.get_permutations(combination_size)
    for permutation in permutations:
        print("Worker Permutation: ", permutation)

        worker_subgraph = Graph()
        for node1 in permutation:
            for node2 in permutation:
                weight = 0
                if(node1 != node2):
                    weight = worker_graph.graph[node1][node2]['weight']
                    worker_subgraph.add_edge(node1, node2, weight)
        print("Worker\'s Subgraph Adjacency Matrix: ")
        print(worker_subgraph.get_adjacency_matrix(list(permutation)))
        print("")

        worker_subgraph_dict[permutation] = worker_subgraph.get_adjacency_matrix(list(permutation))

    print("Total permutations: ", len(permutations))
    # print(worker_subgraph_dict)

    # Get TaskGraph as an adjacency matric
    task_graph_adj_mat = task_graph.get_adjacency_matrix(list(task_graph.graph.nodes()))
    # print("Adjacency Matrix:")
    # print(task_graph_adj_mat)

    # Matrix multiplication
    worker_subgraph_netcost_dict = {}

    for perm, adj_mat in worker_subgraph_dict.items():
        res = np.dot(adj_mat, task_graph_adj_mat)
        netcost = np.sum(res)
        worker_subgraph_netcost_dict[perm] = netcost

    # print("Net Costs: ")
    # print(worker_subgraph_netcost_dict)

    # Find the minimum value
    min_value = min(worker_subgraph_netcost_dict.values())
    print("Lowest Net Cost: ", min_value)

    # Find all keys associated with the minimum value
    min_keys = [key for key, value in worker_subgraph_netcost_dict.items() if value == min_value]
    print("Lowest Net Cost associated Worker subgraph permutation: ")
    print(min_keys)