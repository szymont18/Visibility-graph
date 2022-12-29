from Graph import *
from graphicTool import *
from Obstacle import *
from util import *
import copy
from sortedcontainers import SortedList

import copy
from sortedcontainers import SortedList
import bisect


def visible(w, pw, obstacles, i, w_list, BroomT, visible_list):
    w_obstacle = obstacles[w.oind]

    if len(w_obstacle.getIntersectingEdges(pw)) != 0:  # Intersect the interior of the w_obstacle
        return False

    elif i == 0 or orient(pw.p1, pw.p2, w_list[i - 1]) != 0:
        # w is first vertex in sorted array or w(i-1) not on the segment pw

        if len(BroomT) > 0 and pw.intersectsLine(BroomT[0][1]):  # e exist and pw intersect e
            return False
        else:
            return True

    elif not visible_list[i - 1]:  # w(i-1) is not visible
        return False
    else:  # Search in BroomT for an edge e that intersect w(i - 1)w (not implemented yet)
        return True


def visibleVertices(point: Point, obstacles: list[Obstacle], graph: Graph, vertices: list[Point]):
    BroomT = SortedList()
    w_list = copy.deepcopy(vertices)

    if point.ind != 0:
        w_list.remove(vertices[0])

    if point.ind != vertices[-1].ind:
        w_list.remove(vertices[-1])

    w_list.remove(point)
    Point.updateOrigin(point)

    w_list = sorted(w_list)  # Sorting with angle, should be with dets
    half_line = Line(point, Point((Point.max_X, point.y), -3, -3))
    for obstacle in obstacles:
        edges = obstacle.getIntersectingEdges(half_line)

        for edge in edges:
            BroomT.add((edge.sweepDistance, edge))

    visible_found = [False for _ in range(len(w_list))]


    for i in range(len(w_list)):
        half_line = Line(point, w_list[i])

        if visible(w_list[i], half_line, obstacles, i, w_list, BroomT, visible_found):
            visible_found[i] = True
            graph.addEdge(point.ind, w_list[i].ind, point.distance(w_list[i]))  #Adding edges to the graph

        w_obstacle = obstacles[w_list[i].oind]
        temp = w_obstacle.getIncidentLines(w_list[i])

        for edge in temp:
            x = half_line.getLen()
            if edge.halfLineOrientation(half_line) == -1:  # lie on the clockwise side
                edge.updateSweepLen(x)
                BroomT.add((edge.sweepDistance, edge))
            else:  # lie on the COUNTERcloskwise side
                findAndRemove(BroomT, (edge.sweepDistance, edge))
                # BroomT.remove((edge.sweepDistance, edge))


def computeGraph(points: list[Point], obstacles: list[Obstacle]):
    graph = Graph()

    for k in range(len(points)):
        i = points[k]
        node = Node(i.ind, i)
        graph.addNode(node)

    for i in points:
        visibleVertices(i, obstacles, graph, points)

    return graph


def findAndRemove(T, val):  # TODO: Remove and implement a binary tree
    key = val[0]
    ed = val[1]

    index = bisect.bisect_left(T, val)

    for i in range(index, len(T)):
        if T[i][0] != key:
            return False
        elif ed == T[i][1]:
            del T[i]
            return True




