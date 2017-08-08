#coding:utf-8
import networkx as nx
import os
from collections import defaultdict

dataDirectory = os.path.join('..','..','..','data','cluster')
dataNames = ['大数据.gexf']
dataPaths = [os.path.join(dataDirectory,name) for name in dataNames]

def find_common_edges(type1,type2,edgeSourceDict,type2nodeDict):
    t1 = type2nodeDict[type1]
    t2 = type2nodeDict[type2]
    commonEdges = []
    for t in t1:
        if t in edgeSourceDict:
            for tt in t2:
                if tt in edgeSourceDict[t]:
                    commonEdges.append(edgeSourceDict[t][tt])
                elif tt in edgeSourceDict:
                    if t in edgeSourceDict[tt]:
                        commonEdges.append(edgeSourceDict[tt][t])
    return commonEdges


def find_node_edges(nodeName,edgeSourceDict,edgeTargetDict):
    s1=s2=[]
    if nodeName in edgeSourceDict:
        s1 = list(edgeSourceDict[nodeName].items())
    if nodeName in edgeTargetDict:
        s2 = list(edgeTargetDict[nodeName].items())
    return s1+s2

def cal_contrib(typeName,edgeSet,edgeSourceDict,targetEdgeDict):
    weight = 0
    totWeight = 0
    for e in edgeSet:
        totWeight+=e[1][2]
        sn = e[1][0]
        tn = e[1][1]
        if edgeSourceDict[sn]==typeName:
            weight+=e[1][2]
        elif targetEdgeDict[tn] == typeName:
            weight+=e[1][2]

    return weight/totWeight

def index_for_nodes(nodes):
    result=defaultdict(dict)
    for key,value in nodes:
        result[key] = value
    return result

def index_for_edges(edges):
    sourceDict = defaultdict(dict)
    targetDict = defaultdict(dict)
    for (source,target,w) in edges:
        sourceDict[source][target] = (source,target,w)
        targetDict[target][source] = (source,target,w)
    return sourceDict,targetDict

def type2node_name(nodes):
    d = defaultdict(list)
    for node in nodes:
        d[node[1]['Modularity Class']].append(node[0])
    return d



def clusterDistance(G,type1,type2):
    nodes = G.nodes(data=True)
    edges = G.edges(data='weight')
    #对nodes 和edges进行预处理，建索引
    #nodeDict = index_for_nodes(nodes)
    nodeDict = defaultdict(dict)
    sourceEdgeDict,targetEdgeDict = index_for_edges(edges)
    type2nodeDict = type2node_name(nodes)

    cluster1 = []
    cluster2 = []
    #建cluster可优化
    for node in nodes:
        if node[1]['Modularity Class'] == type1:
            cluster1.append(node)
        elif node[1]['Modularity Class'] == type2:
            cluster2.append(node)

    for node in cluster1:
        edges1 = find_node_edges(node[0],sourceEdgeDict,targetEdgeDict)
        c11 = cal_contrib(type1,edges1,sourceEdgeDict,targetEdgeDict)#对自身cluster贡献
        c12 = cal_contrib(type2,edges1,sourceEdgeDict,targetEdgeDict)#对target cluster贡献
        nodeDict[node[0]]['c1'] = c11
        nodeDict[node[0]]['c2'] = c12

    for node in cluster2:
        edges2 = find_node_edges(node[0],sourceEdgeDict,targetEdgeDict)
        c21 = cal_contrib(type1,edges2,sourceEdgeDict,targetEdgeDict)
        c22 = cal_contrib(type2,edges2,sourceEdgeDict,targetEdgeDict)
        nodeDict[node[0]]['c1'] = c21
        nodeDict[node[0]]['c2'] = c22

    commonEdges = find_common_edges(type1,type2,sourceEdgeDict,type2nodeDict)

    dist = 0
    for e in commonEdges:
        dist+= nodeDict[e[0]]['c1']*nodeDict[e[1]]['c2']*e[2]
    pass

for path in dataPaths:
    graph = nx.read_gexf(path)
    clusterDistance(graph,1,2)
