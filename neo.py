from py2neo import Graph, Node, Relationship, NodeMatcher


def ConnectNeo4j(u='neo4j', p='myneo'):
    return Graph('http://47.100.93.63:7474/', username=u, password=p)


def CreateNode(graph, label, attrs):
    n = "_.name=" + "\'" + attrs['name'] + "\'"
    matcher = NodeMatcher(graph)
    value = matcher.match(label).where(n).first()
    if value is None:
        node = Node(label, **attrs)
        n = graph.create(node)
        return n
    return None


def MatchNode(graph, label, m_attrs):
    n = "_.name=" + "\'" + m_attrs['name'] + "\'"
    matcher = NodeMatcher(graph)
    value = matcher.match(label).where(n).first()
    return value


def CreateRelationship(graph, label1, attrs1, label2, attrs2, name):
    reValue1 = MatchNode(graph, label1, attrs1)
    reValue2 = MatchNode(graph, label2, attrs2)
    if reValue1 is None or reValue2 is None:
        return False
    m_r = Relationship(reValue1, name, reValue2)
    n = graph.create(m_r)
    return n


def MatchNodeById(m_graph, m_id):
    matcher = NodeMatcher(m_graph)
    re_value = matcher.get(m_id)
    return re_value


def MatchNodeByLabel(m_graph, m_label):
    matcher = NodeMatcher(m_graph)
    re_value = matcher.match(m_label)
    return re_value


def ClearGraph(g):
    g.run("match (n) detach delete n")
    return


def isAccountExist(g, acc):
    a = g.run("MATCH (n:user {" + "account:" + "\'{}\'".format(acc) + "}) RETURN n.account").data()
    if not a:
        return 0
    else:
        return 1


def isCoupleAccountPassword(g, acc, pas):
    a = g.run("MATCH (n:user {" + "account:" + "\'{}\'".format(acc) + "}) RETURN n.password").data()
    if not a:
        return 0
    else:
        if a[0]['n.password'] == pas:
            return 1
        else:
            return 0


def RegisterNeo4j(g, acc, pas):
    if isAccountExist(g, acc):
        return 0
    else:
        label = 'user'
        attrs = {"name": acc, "account": acc, "password": pas}
        CreateNode(g, label, attrs)
        return 1
