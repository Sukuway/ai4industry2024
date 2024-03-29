from GraphUtils import GraphUtils

if __name__ == "__main__":
    stats = GraphUtils(N=10000, folder='data')

    print(f'average degree : {stats.average_degree()}\n')

    abstract_nodes = stats.unique_key_value_pairs()
    print(f'abstract nodes : {len(abstract_nodes)}')

    nodes = stats.nodes()

    idx_to_xy, xy_to_idx = stats.mapping_dictionaries(nodes)
    formatted_nodes = [xy_to_idx[node] for node in nodes]
    print(f'nodes : {len(formatted_nodes)}')

    edges = stats.edges()

    formatted_edges = stats.edges_formatting(edges, xy_to_idx)
    print(f'edges : {len(formatted_edges)}')

    distance_edges = stats.distance_edges(formatted_nodes, idx_to_xy, N=20)
    print(f'distance edges : {len(distance_edges)}')

    drafted_features = stats.draft_features(formatted_nodes, 3, distance_edges, formatted_edges)
    print(f'drafted features : {drafted_features}')