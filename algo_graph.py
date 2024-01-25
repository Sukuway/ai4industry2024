import json
from stats import Stats
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import networkx as nx 
from itertools import combinations
from Graph import Graph


if __name__ == "__main__":

    G = Graph(22500, "data")
    G.init_nodes_and_edges(N=10)

    adgency_list = G.edges_to_adjacency_list_undirected()
    print(G.get_neighbors_at_depth(adgency_list, G.abstract_nodes[:4], 20))


