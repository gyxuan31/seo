import networkx as nx
from copy import deepcopy


def get_max_node_index(path, start_id=0, spliter=None):
    """
    get maximum node index after alignment, align the first index to 1
    :param path: file path
    :param start_id: starting node index before alignment, either 1 or 0
    :param spliter: delimeter to split data
    :return: maximum node index after alignment
    """
    max_node = start_id
    datafile = open(path, "r")
    for line in datafile:
        n = max([int(node) + 1 - start_id for node in line.strip().split(spliter)[:2]])
        if n > max_node:
            max_node = n
    datafile.close()
    return max_node


def parse_edge(path, start_id=0, spliter=None):
    """
    edge list after alignment
    :param path: file path
    :param start_id: starting node index before alignment
    :param spliter: delimeter to split data
    :return: edge list after alignment
    """
    edge_list = list()
    datafile = open(path, "r")
    for line in datafile:
        e = line.strip().split(spliter)
        if len(e) == 2:
            edge = (int(e[0]) + 1 - start_id, int(e[1]) + 1 - start_id, 1)
        else:
            edge = (int(e[0]) + 1 - start_id, int(e[1]) + 1 - start_id, float(e[2]))
        edge_list.append(edge)
    datafile.close()
    return edge_list


def power_method_left(graph, vector, alpha=0.85, max_iter=100, tol=1e-3):
    """
    power method to calculate r = alpha * A * r + (1 - alpha) * vector
    :param graph: a networkx graph
    :param vector: teleportation vector, also used as initial starting vector
    :param alpha: damping factor
    :param max_iter: maximum number of iteration
    :param tol: tolerance
    :return: r
    """
    x = deepcopy(vector)
    for num_iter in range(max_iter):
        xlast = x
        x = dict.fromkeys(xlast.keys(), 0)
        for n in x:
            for nbr in graph[n]:
                x[n] += alpha * xlast[nbr] * graph[n][nbr]['weight']
            x[n] += (1.0 - alpha) * vector[n]
        err = sum([abs(x[n] - xlast[n]) for n in x])
        if err < tol:
            return x
    return x


def power_method_right(graph, vector, alpha=0.85, max_iter=100, tol=1e-3):
    """
    power method to calculate r' = alpha * r' * A + (1 - alpha) * vector'
    :param graph: a networkx graph
    :param vector: teleportation vector, also used as initial starting vector
    :param alpha: damping factor
    :param max_iter: maximum number of iteration
    :param tol: tolerance
    :return: r
    """
    x = deepcopy(vector)
    for num_iter in range(max_iter):
        xlast = x
        x = dict.fromkeys(xlast.keys(), 0)
        for n in x:
            for nbr in graph[n]:
                x[nbr] += alpha * xlast[n] * graph[n][nbr]['weight']
            x[n] += (1.0 - alpha) * vector[n]
        err = sum([abs(x[n] - xlast[n]) for n in x])
        if err < tol:
            return x
    return x


def power_method_right_with_scaling(graph, teleportation_vector, alpha=0.85, max_iter=100, tol=1e-3):
    """
    scaled ranking vector
    :param graph: a networkx graph
    :param teleportation_vector: teleportation vector
    :param alpha: damping factor
    :param max_iter: maximum number of iterations
    :param tol: tolerance
    :return: scaled ranking vector
    """
    r = power_method_right(graph, teleportation_vector, alpha=alpha, max_iter=max_iter, tol=tol)
    x = {k: 2 * alpha * v / (1 - alpha) for k, v in r.items()}
    return x


def find_max_influence_edge(graph, teleportation_vector, alpha=0.85, max_iter=100, tol=1e-3):
    """
    get edge with maximum influence
    :param graph: a networkx graph
    :param teleportation_vector: teleportation vector
    :param alpha: damping factor
    :param max_iter: maximum number of iterations
    :param tol: tolerance
    :return: edge with maximum gradient
    """
    directed = nx.is_directed(graph)
    max_grad = float('-inf')
    e_max = (-1, -1, -1)
    edges = set(graph.edges(data='weight', default=1))
    r = power_method_left(graph, teleportation_vector, alpha=alpha, max_iter=max_iter, tol=tol)
    x = power_method_right_with_scaling(graph, r, alpha=alpha, max_iter=max_iter, tol=tol)
    for e in edges:
        u = e[0]
        v = e[1]
        if directed:
            gradient = r[v] * x[u]
        else:
            gradient = r[u] * x[v] + r[v] * x[u]
            if u == v:
                gradient -= (r[v] * x[u])
        if gradient > max_grad:
            e_max = e
            max_grad = gradient
    return e_max


def find_max_influence_node(graph, teleportation_vector, result, alpha=0.85, query=None, max_iter=100, tol=1e-3):
    """
    get node with maximum influence
    :param graph: a networkx graph
    :param teleportation_vector: teleportation vector
    :param result: already selected nodes
    :param alpha: damping factor
    :param query: list of query nodes
    :param max_iter: maximum number of iterations
    :param tol: tolerance
    :return: node with maximum gradient
    """
    directed = nx.is_directed(graph)
    max_grad = float('-inf')
    v_max = -1
    if query is not None:
        personalized = True
    else:
        personalized = False
    nodeset = set(graph.nodes())
    r = power_method_left(graph, teleportation_vector, alpha=alpha, max_iter=max_iter, tol=tol)
    x = power_method_right_with_scaling(graph, r, alpha=alpha, max_iter=max_iter, tol=tol)
    for v in nodeset:
        if personalized and (v in query):
            continue
        if v in result:
            continue
        if directed:
            e_v = list(graph.in_edges(v, data='weight', default=1)) + list(graph.out_edges(v, data='weight', default=1))
            grad = sum([r[j] * x[i] for (i, j, w) in e_v])
        else:
            grad = 0
            e_v = set(graph.edges(v, data='weight', default=1))
            for (i, j, w) in e_v:
                grad += (r[i] * x[j] + r[j] * x[i])
                if i == j:
                    grad -= (r[j] * x[j])
        if grad > max_grad:
            v_max = v
            max_grad = grad
    return v_max


def calculate_node_influence(graph, u, r, x):
    """
    calculate the influence of node u
    :param graph: a networkx graph
    :param u: node u
    :param r: ranking vector
    :param x: scaled vector
    :return: influence of node u
    """
    directed = nx.is_directed(graph)
    if directed:
        e_list = list(graph.in_edges(u, data='weight', default=1)) + list(graph.out_edges(u, data='weight', default=1))
        lst = [x[e[0]] * r[e[1]] for e in e_list]
        gradient = sum(lst)
    else:
        gradient = 0
        for i in graph[u]:
            gradient += (x[u] * r[i] + x[i] * r[u])
            if i == u:
                gradient -= (x[u] * r[i])
    return gradient


def norm(v):
    """
    for evaluation purpose
    :param v: ranking vector
    :return: norm
    """
    v = [val for key, val in v.items()]
    v_sum = sum(v)
    v = [(val / v_sum) ** 2 for val in v]
    return sum(v).real


def evaluate(input_graph, lst, teleportation_vector, r, alpha=0.85, element='edge', max_iter=100, tol=1e-3):
    """
    evaluation
    :param input_graph: a networkx graph
    :param lst: list of selected edges/nodes, or the list of nodes in induced-subgraph
    :param teleportation_vector: teleportation vector
    :param r: ranking vector before elements removal
    :param alpha: damping factor
    :param element: edge, node, or subgraph
    :param max_iter: maximum number of iterations
    :param tol: tolerance
    :return: value for evaluation metric
    """
    graph = deepcopy(input_graph)
    directed = nx.is_directed(graph)
    r_change = list()
    if element == 'edge':
        graph.remove_edges_from(lst)
        r_change = power_method_left(graph, teleportation_vector, alpha=alpha, max_iter=max_iter, tol=tol)
    if element == 'node':
        if directed:
            edge_vertices = list(graph.out_edges(lst, data='weight', default=1)) + list(graph.in_edges(lst, data='weight', default=1))
        else:
            edge_vertices = list(graph.edges(lst, data='weight', default=1))
        graph.remove_edges_from(edge_vertices)
        r_change = power_method_left(graph, teleportation_vector, alpha=alpha, max_iter=max_iter, tol=tol)
    if element == 'subgraph':
        subgraph = nx.subgraph(graph, lst)
        if directed:
            edge_subgraph = list(subgraph.out_edges(data='weight', default=1)) + list(subgraph.in_edges(data='weight', default=1))
        else:
            edge_subgraph = list(subgraph.edges(data='weight', default=1))
        graph.remove_edges_from(edge_subgraph)
        r_change = power_method_left(graph, teleportation_vector, alpha=alpha, max_iter=max_iter, tol=tol)
    change = abs(norm(r) - norm(r_change))
    return change
