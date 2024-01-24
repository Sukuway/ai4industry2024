from stats import Stats

if __name__ == "__main__":
    stats = Stats('data')

    print(f'average degree : {stats.average_degree()}\n')

    unique_key_value = stats.unique_key_value_pairs()
    print(f'abstract nodes : {len(unique_key_value)}')

    nodes = stats.nodes()
    print(f'nodes : {len(nodes)}')

    edges = stats.edges()
    print(f'edges : {len(edges)}')

    idx_to_xy, xy_to_idx = stats.mapping_dictionaries(nodes)
    formatted_nodes = [xy_to_idx[node] for node in nodes]

    formatted_edges = stats.edges_formatting(edges, xy_to_idx)
    print(f'formatted edges : {formatted_edges[:10]}')