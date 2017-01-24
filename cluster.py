from collections import Counter, defaultdict
import matplotlib.pyplot as plt
from math import*
import numpy as np
from TwitterAPI import TwitterAPI
import pickle
import json
import operator
import networkx as nx

def print_num_friends(users):
    for k,v in users.items():
        print ('%s %d' %(str(k),len(users[k])))

def count_friends(users):
    count = Counter()
    for k,v in users.items():
        count.update(users[k])
    return count

def create_graphFN(users, friend_counts):
    edges = []
    common_friend = []
    sorted_counts = sorted(friend_counts.items(), key=lambda x: x[1], reverse=True)
    for items in sorted_counts:
        if(items[1] > 1):
            common_friend.append(items[0])
    graph = nx.Graph()

    for k in users:
        graph.add_node(k)
        for i in common_friend:
            if i in users[k]:
                graph.add_node(i)
                graph.add_edge(k,i)
    return graph

def draw_networkFN(graph, users, filename):
    screen_name=[]
    for k in users:
        screen_name.append(k)
    labels = {n : n if n in screen_name else '' for n in graph.nodes()}
    plt.figure(figsize=(15,15))
    nx.draw_networkx(graph,labels=labels,alpha=.5,width=.1 ,font_size =16, font_color = 'g',node_size=100)
    plt.savefig(filename, format = 'PNG')

def jaccard_similarity(x, y):
    d= set.union(*[set(x), set(y)])
    n = set.intersection(*[set(x), set(y)])
    return len(n)/float(len(d))

def create_graph(users):
    G=nx.Graph()
    #friends = []
    for x in users.keys():
        G.add_node(x)
    for key1 in users.keys():
        for key2 in users.keys():
            if key1 != key2:
                if(jaccard_similarity(set(users[key1]), set(users[key2])) > 0.005):
                    G.add_edge(key1, key2)
    return G

def find_best_edge(G0):
    eb_il = nx.edge_betweenness_centrality(G0).items()
    hbedge = list(sorted(eb_il, key=lambda x: x[1], reverse=True))[0][0]
    print(list(sorted(eb_il, key=lambda x: x[1], reverse=True))[0][0])
    return hbedge

def girvan_newman (G):
    if len(G.nodes()) == 1:
        return [G.nodes()]
    components =[c for c in nx.connected_component_subgraphs(G)]
    print("first",len(components))
    while len(components) <= 2:
        G.remove_edge(*find_best_edge(G))
        components = [c for c in nx.connected_component_subgraphs(G)]
    return components

def main():
    #load Data
    frnds = pickle.load(open('DataStore/NodeFriends.p', 'rb'))
    print_num_friends(frnds)
    Cfriends = count_friends(frnds)
    graph = create_graphFN(frnds, Cfriends)
    print('Graph has %s nodes and %s edges' % (len(graph.nodes()), len(graph.edges())))
    draw_networkFN(graph, frnds, 'DataStore/network.png')
    print('Network drawn to network.png')
    graph2 = create_graph(frnds)
    clusters =girvan_newman(graph2)
    #print('Graph after calculating similarity for users Graph has %s nodes and %s edges' % (len(graph2.nodes()), len(graph2.edges())))
    print('number of clusters : %d'%len(clusters))
    print('-------- Nodes per cluster --------- ')
    print('Cluster 1 : %d nodes \n%s\nCluster 2 : %d nodes\n%s\nCluster 3 : %d nodes\n%s' %
          (clusters[0].order(), clusters[0].nodes(), clusters[1].order(), clusters[1].nodes(), clusters[2].order(), clusters[2].nodes()))
    clusterResult={}
    clusterResult['numofCluster']=len(clusters)
    clusterResult['cluster1'] = clusters[0].order()
    clusterResult['cluster2'] = clusters[1].order()
    clusterResult['cluster3'] = clusters[2].order()
    pickle.dump(clusterResult, open( "DataStore/clusterResult.p", "wb" ))

if __name__ == '__main__':
    main()

