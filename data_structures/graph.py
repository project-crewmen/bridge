import networkx as nx 
from itertools import combinations, permutations
import numpy as np

class Graph:
    def __init__(self): 
        self.graph = nx.Graph()

    def add_edge(self, x, y, weight = 0):
        self.graph.add_edge(x, y, weight=weight)

    def get_adjacency_matrix(self, nodeList):
        return nx.to_numpy_array(self.graph, nodelist=nodeList)
    

class FullyConnectedGraph:    
    def __init__(self, num_nodes): 
        self.num_nodes = num_nodes
        self.graph = self.create_fully_connected_graph()
        
    def create_fully_connected_graph(self):
        G = nx.Graph()
        nodes = range(self.num_nodes)
        G.add_nodes_from(nodes)
        for i in range(self.num_nodes):
            for j in range(i+1, self.num_nodes):
                # weight = random.random()  # Generate a random weight between 0 and 1
                weight = i + j
                G.add_edge(i, j, weight=weight)  # Add edge with random weight
        return G
    
    def get_adjacency_matrix(self, nodeList):
        return nx.to_numpy_array(self.graph, nodelist=nodeList)
    
    def get_combinations(self, size):
        nodes = list(self.graph.nodes())
        combinations_list = list(combinations(nodes, size))
        return combinations_list
    
    def get_permutations(self, size):
        nodes = list(self.graph.nodes())
        permutations_list = list(permutations(nodes, size))
        return permutations_list