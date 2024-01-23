from stats import Stats

if __name__ == "__main__":
    stats = Stats('data')

    print(f'average degree : {stats.average_degree()}\n')

    unique_key_value = stats.unique_key_value_pairs()
    print(f'abstract nodes : {len(unique_key_value)}')

    nodes = stats.nodes()
    print(f'nodes : {len(nodes)}')

    connexions = stats.connexions()
    print(f'edges : {len(connexions)}')
    print(connexions[0])