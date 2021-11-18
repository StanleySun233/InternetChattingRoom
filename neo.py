from py2neo import Graph, Node, Relationship, NodeMatcher
import Neo_Fun as NeoFun
import json
import io
import sys
import urllib.request


def CheckPassword(account, password):
    print(1)


graph = NeoFun.ConnectNeo4j()
# NeoFun.ClearGraph(graph)
labe1 = 'user'
attrs1 = {"name": 'test1', "account": 'test1', "password": '020506'}
attrs3 = {"name": '浦发银行', "code": '60000'}
# labe2 = 'SecuritiesExchange'
# attrs2 = {"name": '上海证券交易所'}
NeoFun.CreateNode(graph, labe1, attrs1)
# m_r_name = "证券交易"
# reValue = NeoFun.CreateRelationship(graph, labe1, attrs1, labe2, attrs2, m_r_name,graph)
print(NeoFun.isAccountExist(graph, 'test2'))
