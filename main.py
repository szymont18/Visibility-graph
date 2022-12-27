from Graph import *
from graphicTool import *
from Obstacle import *
from util import *
import copy
from sortedcontainers import SortedList

import copy
from sortedcontainers import SortedList
import bisect


def visible(w, pw, obst, i, wlist, T, visibleList):
    wObstacle = obst[w.oind]

    if len(wObstacle.getIntersectingEdges(pw)) != 0:
        return False
    elif i == 0 or orient(pw.p1, pw.p2, wlist[i - 1]) != 0:
        if len(T) > 0 and pw.intersectsLine(T[0][1]):
            return False
        else:
            return True
    elif not visibleList[i - 1]:
        return False
    else:
        return True


def visibleVertices(p, obst, graph, vertices):
    T = SortedList()
    wlist = copy.deepcopy(vertices)

    if p.ind != 0:
        wlist.remove(vertices[0])

    if p.ind != vertices[-1].ind:
        wlist.remove(vertices[-1])
    wlist.remove(p)
    Point.updateOrigin(p)
    wlist = sorted(wlist)

    halfLine = Line(p, Point((100, p.y), -3, -3))
    for o in obst:
        lst = o.getIntersectingEdges(halfLine)
        for l in lst:
            T.add((l.sweepDistance, l))

    visibleFound = [False for _ in range(len(wlist))]
    for i in range(len(wlist)):
        halfLine = Line(p, wlist[i])
        if visible(wlist[i], halfLine, obst, i, wlist, T, visibleFound):
            visibleFound[i] = True
            graph.addEdge(p.ind, wlist[i].ind)
        obstacle = obst[wlist[i].oind]
        temp = obstacle.getIncidentLines(wlist[i])
        for edge in temp:
            x = halfLine.getLen()
            if edge.halfLineOrientation(halfLine) == -1:
                edge.updateSweepLen(x)
                T.add((edge.sweepDistance, edge))
            else:
                findAndRemove(T, (edge.sweepDistance, edge))


def computeGraph(st, end, points, obstacles):
    graph = Graph()

    for k in range(len(points)):
        i = points[k]
        node = Node(i.ind, i)
        graph.addNode(node)
    graph.addNode(Node(5, points[-1]))

    for i in points:
        visibleVertices(i, obstacles, graph, points)

    return graph

def findAndRemove(T, val): #TODO: Remove and implement a binary tree
    key = val[0]
    ed = val[1]

    index = T.bisect_left(T,key)

    for i in range(index, len(T)):
        if T[i][0] != key:
            return False
        elif ed == T[i][1]:
            del T[i]
            return True



