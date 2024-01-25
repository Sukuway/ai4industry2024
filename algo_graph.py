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
    #points = G.get_neighbors_at_distance(adgency_list, G.abstract_nodes[:4], 20)
    points = G.get_neighbors_at_depth(adgency_list, G.abstract_nodes[:4], 10)
    points = [G.idx_to_xy[i] for i in points]
    print(points)

