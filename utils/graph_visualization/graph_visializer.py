import networkx as nx
import matplotlib.pyplot as plt

from data_structures.graph import Graph

class GraphVisulizer:
    def __init__(self, G: Graph, labels: list[any]=None, default_color='lightblue'):
        self.G = G
        self.labels = labels if labels is not None else {node: str(node) for node in self.G.nodes()}
        self.default_color = default_color
        # print(self.G)

    def show(self, colored_nodes=None, colored_edges=None, color='red'):
        pos = nx.circular_layout(self.G)  # Position nodes in a circular layout

        # Draw the graph without coloring the edges
        nx.draw(
            self.G, pos, with_labels=True, labels=self.labels, node_size=1000,
            node_color=self.default_color, font_size=12, font_weight='bold'
        )

        # Draw edge labels (optional)
        nx.draw_networkx_edge_labels(
            self.G, pos, edge_labels={(u, v): f"{self.G[u][v]['weight']}" for u, v in self.G.edges()}
        )

        # Color set node nodes
        if(colored_nodes):
            nx.draw_networkx_nodes(self.G, pos, node_color=colored_nodes, node_size=1000)

        # Color specific set of edges
        if(colored_edges):
            nx.draw_networkx_edges(self.G, pos, edgelist=colored_edges, edge_color=color)

        # Color associated nodes
        if(colored_edges):
            node_color = [color if node in sum(colored_edges, ()) else self.default_color for node in self.G.nodes()]
            nx.draw_networkx_nodes(self.G, pos, node_color=node_color, node_size=1000)

        # plt.title('Bidirectional Fully Connected Graph')
        plt.show()
