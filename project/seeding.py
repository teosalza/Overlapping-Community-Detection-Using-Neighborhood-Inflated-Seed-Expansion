from networkx.algorithms.community import greedy_modularity_communities

def get_subgraphs_cluster(G):
    communities = greedy_modularity_communities(G)
    print("Number of communities with best modularity: "+str(len(communities)))
    communities_subgraphs = []
    for c in communities:
        communities_subgraphs.append(G.subgraph(c))
    return communities_subgraphs

def compute_distance_v_Ci(v,cluster,G_biconnected_core,sigma):
    links_Ci_Ci = cluster.number_of_edges() #number of intra-cluster links
    deg_Ci = sum(dict(G_biconnected_core.degree(cluster.nodes())).values())
    deg_V = G_biconnected_core.degree(v)
    links_v_Ci = cluster.degree(v)
    distance = -1*((2*links_v_Ci) /(deg_V*deg_Ci)) + links_Ci_Ci/(deg_Ci**2) + (sigma/deg_V) - (sigma/deg_Ci)
    return distance

def compute_graclus_center(clusters_list,G_biconnected_core):
    seed_dict = {}
    for (idx,cluster) in enumerate(clusters_list):
        distance_array = {}
        for n in cluster.nodes:
            distance = compute_distance_v_Ci(n,cluster,G_biconnected_core,1)
            distance_array[n] = distance
        seed_dict["C"+str(idx)] = min([(value,key) for key,value in distance_array.items()])[1]
    return seed_dict