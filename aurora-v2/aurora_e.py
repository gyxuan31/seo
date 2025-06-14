from utils import *

def aurora_e(input_graph, teleportation_vector, alpha=0.85, budget=1, max_iter=100, tol=1e-3):
    """
    implementation of AURORA-E algorithm
    :param input_graph: a networkx graph
    :param teleportation_vector: the teleportation vector
    :param alpha: damping factor
    :param budget: budget size
    :param max_iter: maximum number of iterations
    :return: the chosen influential edges
    """
    graph = deepcopy(input_graph)
    result = list()
    for i in range(budget):
        edge_max = find_max_influence_edge(graph, teleportation_vector, alpha=alpha, max_iter=max_iter, tol=tol)
        graph.remove_edge(edge_max[0], edge_max[1])
        result.append(edge_max)
    graph.add_weighted_edges_from(result)
    return result
