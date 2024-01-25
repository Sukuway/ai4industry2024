import json
from stats import Stats
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import networkx as nx 
from itertools import combinations




abstract_nodes = ['A', 'B', 'C']
nodes = [1, 2, 3, 4, 5, 6, 7]
edges = [('A', 1), ('B', 2), ('B', 3), (1,5), (5,3)]


def make_graph(nodes, edges):
    g = nx.Graph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)
    return g

def edges_to_adjacency_list_undirected(abstract_nodes, nodes, edges):
    adjacency_list = {node: [] for node in abstract_nodes + nodes}

    for edge in edges:
        source, target = edge
        adjacency_list[source].append(target)
        adjacency_list[target].append(source)  

    return adjacency_list

def sub_graph(abstract_nodes, nodes, edges):
    keep_edges = [edge for edge in edges if (edge[0] in abstract_nodes)]
    keep_nodes = [edge[1] for edge in keep_edges]+[k for k in abstract_nodes]
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

def draw(G, color="red"):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=500, node_color=color, font_size=10)
    plt.show()

def get_neighbors_at_depth(abstract_nodes, adjacency_list, features, depth):
    visited = set()
    saved = set()

    def dfs(nodes, features):
        print(nodes)
        if len(nodes) > depth:
            return
        
        for neighbor in adjacency_list[nodes[-1]]:
            if (neighbor not in features) and (neighbor in abstract_nodes):
                return
            if neighbor not in visited:
                visited.add(neighbor)
                if  (neighbor in features) and (neighbor != nodes[0]):
                    for k in nodes:
                        if k not in features:
                            saved.add(k)
                dfs([k for k in nodes]+[neighbor], features)

    for feature in features:
        dfs([feature],features)
  
    return saved

def distance(a,b):
    return

def get_neighbors_at_distance(adjacency_list, features, dist):
    visited = set()
    saved = set()

    def dfs(nodes, features):
        total_dist = 0
        for i in range(1,len(nodes)-1):
            total_dist+=distance(i,i+1)

        if total_dist > dist:
            return
        
        for neighbor in adjacency_list[nodes[-1]]:
            if neighbor not in visited:
                visited.add(neighbor)
                if  (neighbor in features) and (neighbor != nodes[0]):
                    for k in nodes:
                        if k not in features:
                            saved.add(k)
                dfs([k for k in nodes]+[neighbor], features)

    for feature in features:
        dfs([feature],features)
  
    return saved





if __name__ == "__main__":

    stats = Stats(N=22500, folder='data')
    abstract_nodes = stats.unique_key_value_pairs()
    nodes = stats.nodes()
    idx_to_xy, xy_to_idx = stats.mapping_dictionaries(nodes)
    edges = stats.edges()

    abstract_nodes = list(abstract_nodes)
    formatted_nodes = [xy_to_idx[node] for node in nodes]
    formatted_edges = stats.edges_formatting(edges, xy_to_idx)
    distance_edges = stats.distance_edges(formatted_nodes, N=10)


    adgency_list = edges_to_adjacency_list_undirected(abstract_nodes,formatted_nodes,formatted_edges+distance_edges)
    print(get_neighbors_at_depth(abstract_nodes, adgency_list, abstract_nodes[:4], 15))


