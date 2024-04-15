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

    def add_edges(self, edge_list: list[(any, any, any)]):
        for x, y, w in edge_list:
            self.add_edge(x, y, w)

    def get_adjacency_matrix(self, nodeList):
        adjacency_matrix = nx.to_numpy_array(self.graph, nodelist=nodeList)
        return adjacency_matrix.tolist()
    
    def get_nodes(self):
        return self.graph.nodes()

    def get_edges(self):
        return self.graph.edges()
    
    def get_edge_weight(self, x, y):
        if self.graph.has_edge(x, y):
            return self.graph[x][y]['weight']
        else:
            return None
    
    # def get_adjacency_matrix(self, nodeList):
    #     return nx.to_numpy_array(self.graph, nodelist=nodeList)
    
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
    
    def get_weighted_edge_list_for_nodes(self, nodes):
        edges_with_weights = set()

        for node in nodes:
            for neighbor in self.graph.neighbors(node):
                # Ignore self-edges
                if neighbor == node:
                    continue
                # Check if the edge (neighbor, node) exists, if so, ignore it
                if (neighbor, node) in edges_with_weights:
                    continue
                
                weight = self.get_edge_weight(node, neighbor)
                if weight is not None:
                    edge = (node, neighbor)
                    edges_with_weights.add((edge[0], edge[1], weight))

        return list(edges_with_weights)
    
    def get_other_node(self, edge, node):
        if node == edge[0]:
            return edge[1]
        elif node == edge[1]:
            return edge[0]
        else:
            return None  # Node not found in the edge
    
    def select_least_degree_node_for_edge(self, edge):
        node1, node2, weight = edge
        degree1 = self.graph.degree(node1)
        degree2 = self.graph.degree(node2)
        
        if degree1 < degree2:
            return node1
        elif degree2 < degree1:
            return node2
        else:
            # If both nodes have the same degree, return a random node from the edge
            return random.choice((node1, node2))
    
    def get_disconnected_sets(self):
        colors = {}
        color = 0
        visited = set()
        node_colors_map = {}

        for node in self.graph.nodes():
            if node not in visited:
                color += 1
                nodes_in_component = self.dfs(node, color, visited, colors)
                node_colors_map[color] = nodes_in_component

        node_colors = [colors[node] for node in self.graph.nodes()]

        # Temporary visualization for testing
        # nx.draw(self.graph, with_labels=True, node_color=node_colors, cmap=plt.cm.tab10, node_size=500)
        # plt.show()

        return node_colors_map, node_colors

    def dfs(self, node, color, visited, colors):
        visited.add(node)
        colors[node] = color
        nodes_in_component = [node]

        for neighbor in self.graph.neighbors(node):
            if neighbor not in visited:
                nodes_in_component.extend(self.dfs(neighbor, color, visited, colors))

        return nodes_in_component
    
    def __str__(self):
        return str(self.get_adjacency_matrix(self.get_nodes()))