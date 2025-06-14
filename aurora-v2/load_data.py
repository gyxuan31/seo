import os
from utils import *


def grqc():
    path = os.path.join("Test1.txt")
    #path = os.path.join("GrQc.txt")
    graph = nx.Graph()

    nnodes = get_max_node_index(path, start_id=1)
    node_list = list(range(1, nnodes+1))
    graph.add_nodes_from(node_list)

    edge_list = parse_edge(path, start_id=1)
    graph.add_weighted_edges_from(edge_list)

    return graph
