import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import networkx as nx 
from itertools import combinations


abstract_nodes = ['A', 'B', 'C']
nodes = [1, 2, 3]
edges = [('A', 1), ('B', 2), ('B', 3)]


def make_graph(nodes, edges):
    g = nx.Graph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)
    return g



def sub_graph(abstract_nodes, nodes, edges):
    keep_edges = [edge for edge in edges if (edge[0] in abstract_nodes)]
    keep_nodes = [edge[1] for edge in keep_edges]+abstract_nodes
    return keep_nodes, keep_edges

def test_connected(nodes, edges):
    g = nx.Graph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)
    return nx.is_connected(g)

def fully_connected(abstract_nodes, nodes, edges):
    unconnected = []
    connected = []
    for i,j in combinations(abstract_nodes, 2):
        keep_nodes, keep_edges = sub_graph([i,j], nodes, edges)
        if test_connected(keep_nodes, keep_edges):
            connected.append((i,j))
        else :
            unconnected.append((i,j))
    return unconnected, connected



def test():

    commu = nx.community.louvain_communities(make_graph(nodes+abstract_nodes, edges))
    print(commu)
    unco, co = fully_connected(abstract_nodes, nodes, edges)
    print(len(unco), len(co))


    # sub_nodes, sub_edges = sub_graph(abstract_nodes, nodes, edges)

    # G = nx.Graph()

    # G.add_nodes_from(sub_nodes)
    # G.add_edges_from(sub_edges)

    # print(nx.is_connected(G))

    # pos = nx.spring_layout(G)

    # nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=100, node_color='skyblue', font_size=10)

    # plt.show()
    return

test()