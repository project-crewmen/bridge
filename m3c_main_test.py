from data_structures.graph import Graph
from crewmen.crewmen import Crewmen

if __name__ == "__main__":
    wm = Crewmen()

    worker_graph = Graph()
    worker_graph.create_random_graph(5)

    task_graph = Graph()
    task_graph.create_random_graph(3)

    print("Worker Graph: ")
    print(worker_graph.get_adjacency_matrix(worker_graph.get_nodes()), "\n")

    print("Task Graph: ")
    print(task_graph.get_adjacency_matrix(task_graph.get_nodes()), "\n")

    # affinity_costs = worker_graph.get_weighted_edge_list()
    # print("Affinity Costs: ", affinity_costs, "\n")

    # net_cost = wm.net_cost(affinity_costs)
    # print("Net Cost: ", net_cost, "\n")

    # affinity_cost_threshold = wm.affinity_cost_threshold(affinity_costs)
    # print("Affinity Cost Thresold: ", affinity_cost_threshold, "\n")

    # high_affinity_costs_set = wm.high_affinity_costs_set(affinity_costs, affinity_cost_threshold)
    # print("HACS: ", high_affinity_costs_set, "\n")

    # worker_graph.visualize_graph()