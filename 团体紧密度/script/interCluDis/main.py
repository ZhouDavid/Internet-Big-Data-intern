#coding:utf-8
import networkx as nx
import os
from collections import defaultdict
from collections import Counter
import pandas as pd


dataDirectory = os.path.join('..','..','..','data','cluster')
dataNames = ['大数据.gexf']#,'大连税务.gexf','2016贵州招投标结果.gexf'
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

def cal_contrib(nodeName,typeName,edgeSet,nodeInfo):
    weight = 0
    totWeight = 0
    for e in edgeSet:
        totWeight+=e[1][2]
        sn = e[1][0]
        tn = e[1][1]
        if sn == nodeName:
            if nodeInfo[tn] == typeName:
                weight+=e[1][2]
        else:
            if nodeInfo[sn] == typeName:
                weight+=e[1][2]

    if totWeight == 0:
        return 0
    return weight/totWeight

def index_for_nodes(nodes):
    result=defaultdict()
    for key,value in nodes:
        result[key] = value['Modularity Class']
    return result

def index_for_edges(edges):
    sourceDict = defaultdict(dict)
    targetDict = defaultdict(dict)
    for (source,target,w) in edges:
        sourceDict[source][target] = (source,target,w)
        #targetDict[target][source] = (source,target,w)
    return sourceDict,targetDict

def type2node_name(nodes):
    d = defaultdict(list)
    for node in nodes:
        d[node[1]['Modularity Class']].append(node[0])
    return d


def del_self_edge(edges):
    newEdges = []
    for e in edges:
        if not e[0] == e[1]:
            if e[2]:
                newEdges.append(e)
    return newEdges

def clusterDistance(G,type1,type2):
    nodes = G.nodes(data=True)
    edges = G.edges(data='weight')
    edges = del_self_edge(edges)
    #对nodes 和edges进行预处理，建索引
    nodeInfo = index_for_nodes(nodes)
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
        c11 = cal_contrib(node[0],type1,edges1,nodeInfo)#对自身cluster贡献
        c12 = cal_contrib(node[0],type2,edges1,nodeInfo)#对target cluster贡献
        nodeDict[node[0]]['c1'] = c11
        nodeDict[node[0]]['c2'] = c12

    for node in cluster2:
        edges2 = find_node_edges(node[0],sourceEdgeDict,targetEdgeDict)
        c21 = cal_contrib(node[0],type1,edges2,nodeInfo)
        c22 = cal_contrib(node[0],type2,edges2,nodeInfo)
        nodeDict[node[0]]['c1'] = c21
        nodeDict[node[0]]['c2'] = c22

    commonEdges = find_common_edges(type1,type2,sourceEdgeDict,type2nodeDict)

    dist = 0
    for e in commonEdges:
        dist+= (nodeDict[e[0]]['c1']*nodeDict[e[1]]['c2']*e[2])
    return dist

def has_double_edge(edges):
    nodeNames=[]
    newEdges = []
    for e in edges:
        nodeNames.append(e[0])
        nodeNames.append(e[1])
    nodeNames = list(set(nodeNames))

    i = 0
    nodeNameDict={}
    for n in nodeNames:
        nodeNameDict[n] = i
        i+=1

    for e in edges:
        if nodeNameDict[e[0]]<nodeNameDict[e[1]]:
            newEdges.append(e)
        elif nodeNameDict[e[0]]>nodeNameDict[e[1]]:
            newEdges.append((e[1],e[0],e[2]))
        else:
            tmp = e
            print('here')
    l1 = len(list(set(newEdges)))
    l2 = len(newEdges)
    if not len(list(set(newEdges)))==len(newEdges):
        l1 = len(list(set(newEdges)))
        l2=len(newEdges)
        print('fuck you ')

k = 0
for path in dataPaths:
    data = pd.DataFrame()
    graph = nx.read_gexf(path)
    #获取一共有多少个类
    nodes = graph.nodes(data=True)
    types = []
    for node in nodes:
        types.append(node[1]['Modularity Class'])

    types = list(set(types))
    types1 = []
    types2 = []
    dists = []
    #重边检测
    #has_double_edge(graph.edges(data='weight'))

    print(clusterDistance(graph,0,8))
    # for i in range(len(types)):
    #     for j in range(i+1,len(types)):
    #         dist = clusterDistance(graph,types[i],types[j])
    #         print('type {} type {} : {}'.format(types[i],types[j],dist))
    #         # types1.append(types[i])
    #         # types2.append(types[j])
            # dists.append(dist)
    # data = pd.DataFrame({'type1':types1,'type2':types2,'value':dists})
    # data.to_csv(dataNames[k]+'.csv',index=False)
    k+=1

