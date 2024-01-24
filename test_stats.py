from stats import Stats

if __name__ == "__main__":
    stats = Stats('data')

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
