import pickle

def main():
    collectResult = pickle.load(open('DataStore/collectResult.p', 'rb'))
    classifyResult = pickle.load(open('DataStore/classifyResult.p', 'rb'))
    clusterResult = pickle.load(open('DataStore/clusterResult.p', 'rb'))
    sFile = open('DataStore/summary.txt', 'w')
    print("Total number of user collected: %d\n"%collectResult['totalUser'])
    sFile.write("Total number of user collected %d\n"%collectResult['totalUser'])
    print("Total Number of messages collected: %d\n"%classifyResult['total'])
    sFile.write("Total Number of messages collected: %d\n"%classifyResult['total'])
    print("Number of communities discovered: %d\n"%clusterResult['numofCluster'])
    sFile.write("Number of communities discovered: %d\n"%clusterResult['numofCluster'])
    print("Cluster 1 : %d nodes \nCluster 2 : %d nodes \nCluster 3 : %d nodes\n\n" %
          (clusterResult['cluster1'], clusterResult['cluster2'], clusterResult['cluster3']))
    sFile.write("print('Cluster 1 : %d nodes \nCluster 2 : %d nodes \nCluster 3 : %d nodes\n" %
            (clusterResult['cluster1'], clusterResult['cluster2'], clusterResult['cluster3']))
    avg = (clusterResult['cluster1']+clusterResult['cluster2']+clusterResult['cluster3'])/float(clusterResult['numofCluster'])
    print("Average number of users per community: %d\n"%avg)
    sFile.write("Average number of users per community: %d\n"%avg)
    print("Number of instance found from Positive Class : %d\n"%classifyResult['positive'])
    sFile.write("Number of instance found from Positive Class : %d\n"%classifyResult['positive'])
    print("Number of instance found from Positive Class : %d\n"%classifyResult['negative'])
    sFile.write("Number of instance found from Positive Class : %d\n"%classifyResult['negative'])
    print("------------Positive Tweet------------")
    sFile.write("------------Positive Tweet------------")
    print("%s"%classifyResult['posTweet'])
    sFile.write("%s"%classifyResult['posTweet'])
    print("------------Negative Tweet------------")
    sFile.write("------------Negative Tweet------------")
    print("%s"%classifyResult['negTweet'])
    sFile.write("%s"%classifyResult['negTweet'])
    sFile.close()


if __name__ == '__main__':
    main()
