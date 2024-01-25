from Graph import Graph
import matplotlib.pyplot as plt
import networkx as nx 

def draw(G, color="red"):
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=500, node_color=color, font_size=10)
        plt.show()

if __name__ == "__main__":

    graph = Graph(100, "data")
    graph.init_nodes_and_edges(N=10)
    nxgraph, c = graph.make_graph()
    draw(nxgraph,c)
    