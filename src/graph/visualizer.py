import osmnx as ox
import matplotlib.pyplot as plt

def plot_route(G, route_nodes):
    fig, ax = ox.plot_graph_route(G, route_nodes, route_linewidth=3, node_size=0, bgcolor='white')
    plt.show()