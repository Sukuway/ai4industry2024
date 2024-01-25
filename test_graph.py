from Graph import Graph

if __name__ == "__main__":

    G = Graph(100, "data")
    G.init_nodes_and_edges(N=10)
    G.draw(G.make_graph())
    