from expansion import ConductanceStatistic 

def propagate_communities(expanded_community_list,G_detached_node_list,G_final):
    final_communities_list = []
    for c in expanded_community_list:
        current_communities = c.g1_nodes.copy()
        count = 0
        while count < len(G_detached_node_list):
            for i in range(len(G_detached_node_list)):
                if G_detached_node_list[i] in current_communities:
                    count += 1
                else:
                    neigh_list = G_final.neighbors(G_detached_node_list[i])
                    for el in neigh_list:
                        if el in current_communities: 
                            current_communities.append(G_detached_node_list[i])       
                            count = 0
                            break
                    count += 1
                # print(count)
        cc = ConductanceStatistic(current_communities,0,c.conductance_value,c.name)
        final_communities_list.append(cc)
    return final_communities_list