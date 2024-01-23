import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import networkx as nx 


nodes = ['A', 'B', 'C']
edges = [('A', 'C'), ('A', 'B'), ('B', 'C')]

def print_sub_graph(hypernodes, nodes, edges):
    keep_edges = [edge for edge in edges if (edge[0] in hypernodes) or (edge[1] in hypernodes)]
    keep
    return keep_nodes, keep_edges



G = nx.Graph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)


pos = nx.spring_layout(G)

nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_size=10)

plt.show()
