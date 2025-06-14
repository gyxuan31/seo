from utils import *

def aurora_n(input_graph, e, alpha=0.85, budget=1, query=None, max_iter=100, tol=1e-3):
    """
    implementation of AURORA-N algorithm
    :param input_graph: a networkx graph
    :param e: the teleportation vector
    :param alpha: damping factor
    :param budget: budget size
    :param query: a list of query indices used for personalized setting
    :param max_iter: maximum number of iterations
    :return: the chosen influential nodes
    """
    graph = deepcopy(input_graph)
    result = list()
    for i in range(budget):
        v_max = find_max_influence_node(graph, e, result, alpha=alpha, query=query, max_iter=max_iter, tol=tol)
        edge_v = list(graph.edges(v_max, data='weight', default=1))
        graph.remove_edges_from(edge_v)
        result.append(v_max)
    return result
