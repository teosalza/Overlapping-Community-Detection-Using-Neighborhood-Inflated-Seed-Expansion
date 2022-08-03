def filter_detached_graph(G,G_biconnected_core):
    for n in G_biconnected_core.nodes:
        G.remove_node(n)
    return G

def filtered_graph(G):
    node_list = []
    for e in G.nodes:
        neigh_list = list(G.neighbors(e))
        if  len(neigh_list) == 1:
            neigh = neigh_list[0]
            node_list.append([e,neigh])
    if len(node_list) != 0:
        for n in node_list:
            if(G.has_edge(n[0],n[1])):
                G.remove_edge(n[0],n[1])
        return filtered_graph(G)
    return G