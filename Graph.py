class Node:
    def __init__(self, index: int, point: (float, float)):  # node index as int, point as pair (x,y)
        self.index = index
        self.point = point
        self.edges = {}  # dictionary of edges and their weights

    def add_edge(self, other: int, weight: float):
        if self.edges.get(other) is None:
            self.edges[other] = weight


class Graph:
    def __init__(self, v: list[(int, int)] = None):
        if v is not None:
            self.nodeList = [Node(i, (v[i][0], v[i][1])) for i in range(len(v))]
            self.node_coord = v  # coordinates of each node
        else:
            self.nodeList = []  # list of nodes
            self.node_coord = []  # coordinates of each node

        self.edges = {}  # dict of edges
        self.edges_coord = []  # coordinates of each edge. Example [(1,2), (2,3)] - edge between point (1, 2) and (2, 3)

    def addNode(self, n: Node):
        if n not in self.nodeList:
            self.nodeList.append(n)
            self.node_coord.append((n.point[0], n.point[1]))

    def addEdge(self, n1: int, n2: int, weight: float):
        if (n1, n2) not in self.edges and (n2, n1) not in self.edges:
            self.edges[(n1, n2)] = weight

            self.edges_coord.append([(self.nodeList[n1].point[0], self.nodeList[n1].point[1]),
                                     (self.nodeList[n2].point[0], self.nodeList[n2].point[1])])
            # Adding edge in Node class
            self.nodeList[n1].add_edge(n2, weight)
            self.nodeList[n2].add_edge(n1, weight)

    def __len__(self):
        return len(self.nodeList)



