from stats import Stats

if __name__ == "__main__":
    stats = Stats('data')

    print(f'average degree : {stats.average_degree()}\n')

    print(f'common null keys : {stats.common_null_keys()}')