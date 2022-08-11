import numpy as np
import operator
import networkx as nx


class ConductanceStatistic:
    def __init__(self,g1_nodes,g2_nodes,conductance_value,name):
        self.name = name
        self.g1_nodes = g1_nodes
        self.g2_nodes = g2_nodes
        self.conductance_value = conductance_value
    

def get_low_conductance_set(Gb_copy,val,alpha,epsilon):
    restart_node =  list(Gb_copy.neighbors(val))+[val] 

    Xv = np.zeros(max(list(Gb_copy.nodes)))
    Rv = np.zeros(max(list(Gb_copy.nodes)))
    for el in restart_node:
        # n_neighbors = len(list(Gb_copy.neighbors(el)))
        Rv[el-1] = 1 / len(restart_node)

    finish_count = 0
    count = 0   
    isRunning = True

    #computation code
    while isRunning:
        node = list(Gb_copy.nodes)[count]
        while Rv[node-1] > len(list(Gb_copy.neighbors(node)))*epsilon:
            finish_count = 0
            Xv[node-1] = Xv[node-1] + (1-alpha)*Rv[node-1]
            for el in Gb_copy.neighbors(node):
                Rv[el-1] = Rv[el-1] + alpha*Rv[node-1]/(2*len(list(Gb_copy.neighbors(node))))
            Rv[node-1] = alpha*Rv[node-1]/2
            
        else:
            finish_count += 1

        if finish_count == len(list(Gb_copy.nodes)): break
        if count == len(list(Gb_copy.nodes))-1: count = 0
        count += 1
    
    return Xv

def order_by_descending(Xv, Gb_copy):
    #ordering by descending 
    descending_graph_ordering = {}
    for (idx,el) in enumerate(Xv):
        if(Gb_copy.has_node(idx + 1)):
            descending_graph_ordering[idx+1] = el / len(list(Gb_copy.neighbors(idx+1)))
            
    descending_graph_ordering = dict( sorted(descending_graph_ordering.items(), key=operator.itemgetter(1),reverse=True))
    return descending_graph_ordering

def get_minimum_conductance(descending_graph_ordering,Gb_core_copy,name):
    #Filter and get only 90% of total nodes
    maximun_nodes_iterations = int(len(descending_graph_ordering)*90/100)
    #calculate conductance
    current_set = []
    conductace_values = []
    conductance_list_set = []
    count_iteration = 0
    for (key,val) in descending_graph_ordering.items():
        if(count_iteration <= maximun_nodes_iterations):
            G2 = Gb_core_copy.copy()
            current_set.append(key) 
            conductance_value = nx.conductance(G2,current_set)
            conductace_values.append(conductance_value)

            G2.remove_nodes_from(current_set)
            cond = ConductanceStatistic(current_set.copy(), list(G2.nodes).copy(),conductance_value,name)
            conductance_list_set.append(cond)
            count_iteration += 1

    #Calculate conductance min
    cond_min = ConductanceStatistic(0,0,1,name)
    for el in conductance_list_set:
        if(el.conductance_value < cond_min.conductance_value):
            cond_min = el

    return cond_min, conductace_values