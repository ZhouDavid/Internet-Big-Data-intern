#coding:utf-8
import networkx as nx
import os

dataDirectory = os.path.join('..','..','..','data','cluster')
dataNames = ['大连税务.gexf']
dataPaths = [os.path.join(dataDirectory,name) for name in dataNames]
for path in dataPaths:
    graph = nx.read_gexf('大数据.gexf')
    
    pass