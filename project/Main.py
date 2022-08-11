import pandas as pd
import numpy as np
import networkx as nx
from math import e
from utils import load_data
from statistics import mean
from filtering import filter_detached_graph, filtered_graph 
from seeding import get_subgraphs_cluster, compute_graclus_center
from expansion import get_low_conductance_set,order_by_descending,get_minimum_conductance
from propagation import propagate_communities
import mlflow
import os,getopt,sys
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

def main(argv):
    dataset_name="network_1000_7327"
    # path ="..\datasets\\network_100\\network_1000_7327.lfi"
    path ="..\datasets\\facebook\\0.edges"
    # path ="..\datasets\\facebook\\3980.edges"
    # path ="..\datasets\\HepPh\\ca-HepPh.mtx"
    # path ="..\datasets\\myspace\\soc-myspace.edges"

    alpha = 0.9
    epsilon = 10**-6
    try:
        opts, args = getopt.getopt(argv,"hi:d:a:e:",["ifile=","dfile=","afile=","efile="])
    except getopt.GetoptError:
        print("Usage: Main.py -i <inputfile> -d <datasetname> -a <alpha> -e <epsilon>")
        sys.exit(2)

    if len(opts) == 0:
        print("Usage: Main.py -i <inputfile> -d <datasetname> -a <alpha> -e <epsilon>")
        sys.exit()

    for opt, arg in opts:
        if opt == '-h':
            print("Usage Main.py -i <inputfile> -d <datasetname> -a <alpha> -e <epsilon>")
            sys.exit()
        elif opt in ("-i", "--ifile"):
            path = arg
        elif opt in ("-d", "--dfile"):
            dataset_name = arg
        elif opt in ("-a", "--afile"):
            alpha = float(arg)
        elif opt in ("-e", "--efile"):
            epsilon = float(arg)
        

    with mlflow.start_run() as run:
        #Loading and generating graph----------------------------------------------------
        print("-(Start) Generating graph")
        input_edges, num_nodes = load_data(path)
        G = nx.read_edgelist(path,create_using=nx.Graph(), nodetype = int)
        for n in G.nodes:
            G.nodes[n]["visited"] = False

        print("-(End) Generated graph")


        #Dataset descritpion-------------------------------------------------------------
        max_degree = max([e[1] for e in G.degree])
        avg_degree = '{0:.3g}'.format(mean([e[1] for e in G.degree]))
        avg_clustering_coefficient = '{0:.4g}'.format(nx.average_clustering(G))

        dt_description = pd.DataFrame({
            "name":[dataset_name],
            "No. vertices":[G.number_of_nodes()],
            "No. edges":[G.number_of_edges()],
            "Max. deg":[max_degree],
            "Avg. deg":[avg_degree],
            "Avg. CC":[avg_clustering_coefficient]})

        print("-----")
        print(dt_description)
        print("-----")


        #Filtering phase------------------------------------------------------------------
            #Filtering the graph, removing the  whiskers from the biconnected core
        print("-(Start) Filtering phase")
        print("     Generating biconnected core")
        G2 = G.copy()
        G_filtered = filtered_graph(G2)
        G_biconnected_core = G_filtered.subgraph(max(nx.connected_components(G_filtered), key=len)).copy()

        print("     Generating detached graph")
        G_detached = filter_detached_graph(G.copy(),G_biconnected_core)

        print("-----")
        print("G statistics before filtering:")
        print("     -"+nx.info(G))
        print("G_biconnected statistics after filtering:")
        print("     -"+nx.info(G_biconnected_core))

        perc_no_verticles = '{0:.3g}'.format(len(G_biconnected_core.nodes)/len(G.nodes)*100)
        perc_no_edges = '{0:.3g}'.format(len(G_biconnected_core.edges)/len(G.edges)*100)
        max_comp_detach =  0 if len(list(G.nodes)) == len(list(G_biconnected_core)) else len(max(nx.connected_components(G_detached), key=len))
        perc_max_comp_detach ='{0:.3g}'.format(max_comp_detach / len(G.nodes) * 100) 

        bc_description = pd.DataFrame({
            "No. of vertices (%)":[str(len(G_biconnected_core.nodes))+'('+str(perc_no_verticles)+')'],
            "No. of edges (%)":[str(len(G_biconnected_core.edges))+'('+str(perc_no_edges)+')'],
            "No. components detached":[len(G_detached.nodes)],
            "Size of the LCC (%)":[str(max_comp_detach)+"("+str(perc_max_comp_detach)+")"]})
        print(bc_description)
        print("-----")
        print("-(End) Filtering phase")

        #Seeding phase--------------------------------------------------------------------
        print("-(Start) Seeding phase")
        print("     Calculating best clusters")
        #Exhaustive non-overlapping clusters on G_biconnected_core
        communities_subgraphs_clusters = get_subgraphs_cluster(G_biconnected_core)
        #Get seed list computing the Graclus center algorithm
        print("     Compute graculus center")
        seed_dict_gc = compute_graclus_center(communities_subgraphs_clusters,G_biconnected_core)
        #Get seed list computing the Spread Hubs
        print("-(End) Seeding phase")

        #Seeding exapansion phase--------------------------------------------------------
        print("-(Start) Expansion phase")

        
        expanded_community_list = []
        G_bicon_expansion = G_biconnected_core.copy()
        for key,val in seed_dict_gc.items():
            Xv = get_low_conductance_set(G_bicon_expansion,val,alpha,epsilon)
            descending_graph_ordering = order_by_descending(Xv,G_bicon_expansion)
            cond_min, conductance_values = get_minimum_conductance(descending_graph_ordering,G_bicon_expansion,key)
            expanded_community_list.append(cond_min)
        print("-(End) Expansion phase")

        #Propagation phase-------------------------------------------------------------
        print("-(Start) Propagation phase")
        G_final = G.copy()
        final_community_list = propagate_communities(expanded_community_list,list(G_detached.nodes),G_final)
        for el in final_community_list:
            print(" Final Community result:")
            print("    ",el.name, " - ",len(el.g1_nodes))
        print("-(End) Propagation phase")
        return


if __name__ == "__main__":
    main(sys.argv[1:])
