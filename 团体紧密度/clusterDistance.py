#coding:utf-8
import networkx as nx
import os
from collections import defaultdict
from collections import Counter
import pandas as pd
import time

dataDirectory = ''
dataNames = ['大数据.gexf','大连税务.gexf','2016贵州招投标结果.gexf']
dataPaths = [os.path.join(dataDirectory,name) for name in dataNames]
N = 20#平衡系数

class SimpleGraph:
    def __init__(self,graph):
        self.graph = graph
        self.nodes = graph.nodes(data=True)
        self.edges = self.del_extra_edges(graph.edges(data='weight'))
        self.types = self.get_types()
        self.nodeInfo = defaultdict()
        self.type2Nodes = defaultdict(list)
        self.sourceDict = defaultdict(dict)
        self.targetDict = defaultdict(dict)
        self.index_nodes()
        self.index_edges()


    def get_types(self):
        types=[]
        for n in self.nodes:
            types.append(n[1]['Modularity Class'])

        types = list(set(types))
        types.sort()
        return types

    def del_extra_edges(self,edges):
        newEdges=[]
        for e in edges:
            if e[0] > e[1]:
                newEdges.append((e[1],e[0],e[2]))
            elif e[0]<e[1]:
                newEdges.append(e)
        return newEdges

    def index_nodes(self):
        for key, value in self.nodes:
            self.nodeInfo[key] = value['Modularity Class']
            self.type2Nodes[value['Modularity Class']].append(key)
        return

    def index_edges(self):
        for (source, target, w) in self.edges:
            self.sourceDict[source][target] = (source, target, w)
            self.targetDict[target][source] = (source, target, w)
        return

    def neighbor_edges(self,nodeName):
        s1 = []
        s2 = []
        if nodeName in self.sourceDict:
            s1 = list(self.sourceDict[nodeName].items())
        if nodeName in self.targetDict:
            s2 = list(self.targetDict[nodeName].items())
        return s1 + s2

    def find_common_edges(self,type1,type2):
        t1 = self.type2Nodes[type1]
        t2 = self.type2Nodes[type2]
        commonEdges = []
        for t in t1:
            if t in self.sourceDict:
                for tt in t2:
                    if tt in self.sourceDict[t]:
                        commonEdges.append(self.sourceDict[t][tt])
                    elif tt in self.sourceDict:
                        if t in self.sourceDict[tt]:
                            commonEdges.append(self.sourceDict[tt][t])
        return commonEdges

    def cal_contrib(self,nodeName,typeName,edgeSet):
        weight = 0
        totWeight = 0
        for e in edgeSet:
            if e[1][2]:
                totWeight += e[1][2]
            sn = e[1][0]
            tn = e[1][1]
            if sn == nodeName:
                if self.nodeInfo[tn] == typeName:
                    if e[1][2]:
                        weight += e[1][2]
            else:
                if self.nodeInfo[sn] == typeName:
                    if e[1][2]:
                        weight += e[1][2]
        if totWeight == 0:
            return 0
        return weight / totWeight

    def clusterDistance(self,type1,type2):
        cluster1 = []
        cluster2 = []
        #建cluster可优化
        for node in self.nodes:
            if node[1]['Modularity Class'] == type1:
                cluster1.append(node)
            elif node[1]['Modularity Class'] == type2:
                cluster2.append(node)

        nodeDict = defaultdict(dict)
        for node in cluster1:
            edges1 = self.neighbor_edges(node[0])
            c11 = self.cal_contrib(node[0],type1,edges1)#对自身cluster贡献
            c12 = self.cal_contrib(node[0],type2,edges1)#对target cluster贡献
            nodeDict[node[0]]['c1'] = c11
            nodeDict[node[0]]['c2'] = c12

        for node in cluster2:
            edges2 = self.neighbor_edges(node[0])
            c21 = self.cal_contrib(node[0],type1,edges2)
            c22 = self.cal_contrib(node[0],type2,edges2)
            nodeDict[node[0]]['c1'] = c21
            nodeDict[node[0]]['c2'] = c22

        commonEdges = self.find_common_edges(type1,type2)

        dist = 0
        for e in commonEdges:
            if (nodeDict[e[0]]['c1'] and nodeDict[e[0]]['c2'] and nodeDict[e[1]]['c2'] and nodeDict[e[1]]['c1'] and e[2]):
                dist+=(nodeDict[e[0]]['c1']*nodeDict[e[0]]['c2']*nodeDict[e[1]]['c2']*nodeDict[e[1]]['c1']*e[2])*N
        return dist


begin = time.time()
k = 0
for path in dataPaths:
    data = pd.DataFrame()
    G = nx.read_gexf(path)
    graph = SimpleGraph(G)

    types1 = []
    types2 = []
    dists = []

    for i in range(len(graph.types)):
        for j in range(i+1,len(graph.types)):
            dist = graph.clusterDistance(graph.types[i],graph.types[j])
            # print('type {} type {} : {}'.format(types[i],types[j],dist))
            types1.append(graph.types[i])
            types2.append(graph.types[j])
            dists.append(dist)
    data = pd.DataFrame({'type1':types1,'type2':types2,'value':dists})
    data.to_csv(dataNames[k][:-5]+'.csv',index=False)
    k+=1
    end = time.time()
    print('running time:{}'.format(end-begin))

