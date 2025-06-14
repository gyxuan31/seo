# -*- coding: utf-8 -*-
from scipy.sparse.linalg import eigs
import load_data as data
from utils import *
from aurora_e import *
from aurora_n import *
from aurora_s import *
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    G = data.grqc()  # input graph
    query = None  # a list of indices for query node, if global, set it to None
    k = 2  # budget size
    np.random.seed(100)
    plt.rcParams['font.sans-serif'] = ['Kaitt', 'SimHei']

    max_iter = 50  # maximum number of iteration
    tol = 1e-3  # tolerance for error check in power method

    print("k =", k)
    N = G.number_of_nodes()
    A = nx.to_scipy_sparse_matrix(G, dtype='float', format='csc')
    eigval, _ = eigs(A, k=1)
    alpha = 0.5 / abs(eigval[0])
    alpha = alpha.real

    if query is None:
        start_vector = dict.fromkeys(G, 1.0 / N)
    else:
        start_vector = dict.fromkeys(G, 0.0)
        length = len(query)
        for i in query:
            start_vector[i] = 1.0 / length

    r = power_method_left(G, start_vector, alpha=alpha)
    print(r)

    options = {
    'node_color': 'black',  # 节点颜色
    'node_size': 1,  # 节点大小
    'width': 0.1,  # 边粗
    'alpha': 0.7,  # 节点颜色透明度
    'linewidths': 0.1,  # 节点边缘线粗细
    'edge_color': 'black',  # 边颜色
    # 'font_size': 1,  # 节点上标签的字体大小
    # 'font_color': 'white'  # 节点上标签字的颜色
    }
    # pos = nx.random_layout(G, seed=100)
    pos = nx.layout.spring_layout(G)

    # # 绘制原始数据集图形
    # nx.draw_networkx(G, **options,pos=pos,font_size=1, font_color='white')
    # plt.title('Airline数据集的网络拓扑图')
    # plt.show()


    edges = aurora_e(G, start_vector, alpha=alpha, budget=k, max_iter=max_iter, tol=tol)
    print(edges)
    goodness = evaluate(G, edges, start_vector, r, alpha=alpha, element='edge')
    print("最具影响力的边:", goodness)

    nodes = aurora_n(G, start_vector, alpha=alpha, budget=k, query=query, max_iter=max_iter, tol=tol)
    print(nodes)
    goodness = evaluate(G, nodes, start_vector, r, alpha=alpha, element='node')
    print("最具影响力的节点:", goodness)

    subgraph = aurora_s(G, start_vector, alpha=alpha, budget=k, max_iter=max_iter, tol=tol)
    print(subgraph)
    goodness = evaluate(G, subgraph, start_vector, r, alpha=alpha, element='subgraph')
    print("最具影响力的子图构成:", goodness)


    # 绘制最具影响力的节点和边
    edges2 = [(x, y) for (x, y, z) in edges]
    # 标定特定的节点
    node_colors = ['red' if node in nodes else 'black' for node in G.nodes()]
    node_size = [ 20 if node in nodes else 1 for node in G.nodes()]
    edge_colors = [ '#4472C4' if edge in edges2 else 'black' for edge in G.edges()]
    edge_width = [ 2 if edge in edges2 else 0.1 for edge in G.edges()]
    nx.draw_networkx(G, with_labels=False, pos=pos,
                     node_size= node_size,  # 节点大小
                     width = edge_width,  # 边粗
                     alpha = 0.7,  # 节点颜色透明度
                     linewidths = 0.1,  # 节点边缘线粗细
                     node_color=node_colors, 
                     edge_color=edge_colors
                     )
    G.remove_edges_from(nx.selfloop_edges(G))
    nx.draw_networkx_edges(G,pos,edgelist=edges2,width=3,edge_color='#4472C4',alpha=0.7)
    plt.title(f'当k={k}时影响程度最高的k个节点和k条边',fontsize = 16)
    ax = plt.gca()
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color('black')
        spine.set_linewidth(1.5)
    plt.show()

    #绘制最具影响力的子图
    subgraphlist = G.subgraph(subgraph)
    # 绘制整个图形
    nx.draw_networkx(G, **options,pos=pos,font_size=1, font_color='white')
    nx.draw_networkx(subgraphlist, pos, with_labels=False, 
            node_color='#A9D18E', node_size=15,
            width = 2,
            edge_color = '#A9D18E',
            alpha = 0.7)
    # 调整轴的边界线样式，添加外框黑线
    ax = plt.gca()
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color('black')
        spine.set_linewidth(1.5)

    plt.title(f'当k={k}时影响程度最高的由k个节点构成的子图', fontsize = 16)
    plt.show()