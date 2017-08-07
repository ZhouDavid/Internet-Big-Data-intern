#coding:utf-8
import networkx as nx
import os
from collections import defaultdict

dataDirectory = os.path.join('..','..','..','data','cluster')
dataNames = ['大数据.gexf']
dataPaths = [os.path.join(dataDirectory,name) for name in dataNames]

def find_common_edges(type1,type2,edgeDict):
    edgeDict[type1]
    edgeDict[type2]

def find_node_edges(nodeName,edgeSet):
    edges = []
    for e in edgeSet:
        pass
    return None

def cal_contrib(typeName,edgeSet):
    pass

def index_for_nodes(nodes):
    result=defaultdict(dict)
    for key,value in nodes:
        result[key] = value
    return result

def index_for_edges(edges):
    result = defaultdict(list)
    for (source,target,w) in edges:
        result[source].append((source,target,w))
    return result

def clusterDistance(G,type1,type2):
    nodes = G.nodes(data=True)
    edges = G.edges(data='weight')
    #对nodes 和edges进行预处理，建索引
    nodeDict = index_for_nodes(nodes)
    edgeDict = index_for_edges(edges)

    cluster1 = []
    cluster2 = []
    for node in nodes:
        if node[2]['Modularity Class'] == type1:
            cluster1.append(node)
        elif node[2]['Modularity Class'] == type2:
            cluster2.append(node)

    for node in cluster1:
        edges1 = find_node_edges(node[0],edges)
        c11 = cal_contrib(type1,edges1)#对自身cluster贡献
        c12 = cal_contrib(type2,edges1)#对target cluster贡献
    for node in cluster2:
        edges2 = find_node_edges(node[0],edges)
        c21 = cal_contrib(type1,edges2)
        c22 = cal_contrib(type2,edges2)

    commonEdges = find_common_edges(type1,type2,edges)
    dist = 0
    for e in commonEdges:
        dist+= nodeDict[e[0]]['c1']*nodeDict[e[1]]*e[2]
    print(dist)
    pass









for path in dataPaths:
    graph = nx.read_gexf(path)
    clusterDistance(graph,1,2)
