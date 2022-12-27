class Node:
    def __init__(self, index, point):  # node index as int, point as pair (x,y)
        self.index = index
        self.point = point


class Graph:
    def __init__(self):
        self.nodeList = []  # list of nodes
        self.edges = []  # list of edges as (n1, n2) -> graph contains edge from node n1 to n2

    def addNode(self, n):
        if n not in self.nodeList:
            self.nodeList.append(n)
            self.edges.append([])

    def addEdge(self, n1, n2):
        if (n1, n2) not in self.edges and (n2, n1) not in self.edges:
            self.edges[n1].append(n2)

