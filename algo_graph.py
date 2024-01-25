from Graph import Graph
from map import generate_map

if __name__ == "__main__":

    G = Graph(22500, "data")
    G.init_nodes_and_edges(N=10)

    adgency_list = G.edges_to_adjacency_list_undirected()
    features = G.stats.draft_features(G.nodes, 3, G.distance_edges, G.edges)
    print(features)
    #points = G.get_neighbors_at_distance(adgency_list, features, 20)
    points = G.get_neighbors_at_depth(adgency_list, features, 10)
    points = [G.idx_to_xy[i] for i in points]
    print(points)
    generate_map(points)

