import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(3, 4)
G.add_edge(4, 1)

edge_labels = {(1, 2): 'A', (2, 3): 'B', (3, 4): 'C', (4, 1): 'D'}

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

plt.show()
