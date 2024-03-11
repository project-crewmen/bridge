import networkx as nx 
from itertools import permutations
import random
import matplotlib.pyplot as plt

class Graph:
    def __init__(self): 
        self.graph = nx.Graph()

    def create_random_graph(self, num_nodes):
        G = nx.Graph()
        nodes = range(num_nodes)
        G.add_nodes_from(nodes)
        for i in range(num_nodes):
            for j in range(i+1, num_nodes):
                weight = random.random()  # Generate a random weight between 0 and 1
                G.add_edge(i, j, weight= round(weight, 3))  # Add edge with random weight
        self.graph = G

    def add_node(self, x):
        self.graph.add_node(x)

    def add_edge(self, x, y, weight = 0):
        self.graph.add_edge(x, y, weight=weight)

    def get_adjacency_matrix(self, nodeList):
        return nx.to_numpy_array(self.graph, nodelist=nodeList)
    
    def get_nodes(self):
        return self.graph.nodes()

    def get_edges(self):
        return self.graph.edges()
    
    def get_edge_weight(self, x, y):
        if self.graph.has_edge(x, y):
            return self.graph[x][y]['weight']
        else:
            return None
    
    def get_adjacency_matrix(self, nodeList):
        return nx.to_numpy_array(self.graph, nodelist=nodeList)
    
    def get_permutations(self, size):
        nodes = list(self.graph.nodes())
        permutations_list = list(permutations(nodes, size))
        return permutations_list
    
    def visualize_graph(self):
        pos = nx.spring_layout(self.graph)  # Positions for all nodes
        nx.draw(self.graph, pos, with_labels=True, node_color='skyblue', node_size=500, font_size=10)  # Draw nodes with labels
        labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels)  # Draw edge labels
        plt.show()

    def get_weighted_edge_list(self):
        weighted_edge_list = []
        for edge in self.graph.edges(data=True):
            weighted_edge_list.append((edge[0], edge[1], edge[2]['weight']))
        return weighted_edge_list