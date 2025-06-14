from utils import *


def aurora_s(input_graph, e, alpha=0.85, budget=2, max_iter=100, tol=1e-3):
    """
    implementation of AURORA-S algorithm
    :param input_graph: a networkx graph
    :param e: the teleportation vector
    :param alpha: damping factor
    :param budget: budget size
    :param max_iter: maximum number of iterations
    :return: the chosen influential subgraph
    """
    graph = deepcopy(input_graph)
    directed = nx.is_directed(graph)
    result = set()

    while len(result) != budget:
        max_grad = float('-inf')
        edge_max = (-1, -1, -1)
        edges = list(graph.edges(data='weight', default=1))

        r = power_method_left(graph, e, alpha=alpha, max_iter=max_iter, tol=tol)
        x = power_method_right_with_scaling(graph, r, alpha=alpha, max_iter=max_iter, tol=tol)

        for edge in edges:
            u = edge[0]
            v = edge[1]
            if (u in result) and (v in result):
                continue
            if directed:
                grad = x[u] * r[v]
            else:
                grad = x[u] * r[v] + x[v] * r[u]
            if grad > max_grad:
                edge_max = edge
                max_grad = grad
        u = edge_max[0]
        v = edge_max[1]

        if len(result) + 2 <= budget:
            result.add(u)
            result.add(v)
        else:
            u_grad = calculate_node_influence(graph, u, r, x)
            v_grad = calculate_node_influence(graph, v, r, x)
            if u_grad >= v_grad:
                if u not in result:
                    result.add(u)
                else:
                    result.add(v)
            else:
                if v not in result:
                    result.add(v)
                else:
                    result.add(u)

        edges_to_remove = list(graph.subgraph(list(result)).edges(data='weight', default=1))
        graph.remove_edges_from(edges_to_remove)

    result = list(result)
    return result
