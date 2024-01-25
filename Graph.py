from stats import Stats
import matplotlib.pyplot as plt
import networkx as nx 

class Graph():
    def __init__(self, N: int, folder: str):
        self.N = N
        self.folder = folder

    def init_nodes_and_edges(self, N=3):
        self.stats = Stats(N=self.N, folder=self.folder)

        abstract_nodes = self.stats.unique_key_value_pairs()
        nodes = self.stats.nodes()

        self.idx_to_xy, self.xy_to_idx = self.stats.mapping_dictionaries(nodes)

        edges = self.stats.edges()

        self.abstract_nodes: list = list(abstract_nodes)
        self.nodes: list = [self.xy_to_idx[node] for node in nodes]

        self.edges: list = self.stats.edges_formatting(edges, self.xy_to_idx)
        self.distance_edges: list = self.stats.distance_edges(self.nodes, self.idx_to_xy, N)

    def get_all_nodes(self) -> list:
        return self.nodes + self.abstract_nodes
    
    def get_all_edges(self) -> list:
        return self.edges + self.distance_edges

    def make_graph(self) -> nx.Graph:
        g = nx.Graph()
        g.add_nodes_from(self.get_all_nodes())
        g.add_edges_from(self.get_all_edges())
        return g

    def edges_to_adjacency_list_undirected(self):
        adjacency_list = {node: [] for node in self.get_all_nodes()}

        for edge in self.get_all_edges():
            source, target = edge
            adjacency_list[source].append(target)
            adjacency_list[target].append(source)  

        return adjacency_list

    def sub_graph(self, abstract_nodes):
        keep_edges = [edge for edge in self.get_all_edges() if (edge[0] in abstract_nodes)]
        keep_nodes = [edge[1] for edge in keep_edges]+[k for k in abstract_nodes]
        return keep_nodes, keep_edges

    def test_connected(self):
        g: nx.Graph = self.make_graph()
        return nx.is_connected(g)

    """def fully_connected(abstract_nodes, nodes, edges):
        unconnected = []
        connected = []
        for i,j in combinations(abstract_nodes, 2):
            keep_nodes, keep_edges = sub_graph([i,j], nodes, edges)
            if test_connected(keep_nodes, keep_edges):
                connected.append((i,j))
            else :
                unconnected.append((i,j))
        return unconnected, connected"""


    def get_neighbors_at_depth(self, adjacency_list, features, depth):
        visited = set()
        saved = set()

        def dfs(nodes, features):
            print(nodes)
            if len(nodes) > depth:
                return
            
            for neighbor in adjacency_list[nodes[-1]]:
                if (neighbor not in features) and (neighbor in self.abstract_nodes):
                    return
                elif neighbor not in visited:
                    visited.add(neighbor)
                    if  (neighbor in features) and (neighbor != nodes[0]):
                        for k in nodes:
                            if k not in features:
                                saved.add(k)
                    dfs([k for k in nodes]+[neighbor], features)

        for feature in features:
            visited.add(feature)
            dfs([feature],features)
    
        return saved


    def get_neighbors_at_distance(self, adjacency_list, features, dist):
        visited = set()
        saved = set()
        
        def dfs(nodes, total_dist):

            print(nodes, total_dist)
            
            if (len(nodes) > 2) and (nodes[-2] != str and nodes[-1] != str):
 
                    coord1 = self.idx_to_xy[nodes[-2]]
                    coord2 = self.idx_to_xy[nodes[-1]]
                    total_dist+=self.stats._haversine_distance(coord1, coord2)


            if total_dist > dist:
                return
            
            for neighbor in adjacency_list[nodes[-1]]:
                if (neighbor not in features) and (neighbor in self.abstract_nodes):
                    return
                elif neighbor not in visited:
                    visited.add(neighbor)
                    if  (neighbor in features) and (neighbor != nodes[0]):
                        for k in nodes:
                            if k not in features:
                                saved.add(k)
                    dfs([k for k in nodes]+[neighbor], total_dist)

        for feature in features:
            visited.add(feature)
            dfs([feature],0)
    
        return saved


