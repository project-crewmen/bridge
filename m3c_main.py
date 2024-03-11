from data_structures.graph import Graph

if __name__ == "__main__":
    worker_graph = Graph()
    worker_graph.create_random_graph(5)

    print(worker_graph.get_adjacency_matrix(worker_graph.get_nodes()))