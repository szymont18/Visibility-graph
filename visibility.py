from sortedcontainers import SortedList, SortedSet
from Visualiser import *
import copy




def searchForIntersection(T : SortedList,broom : Line):
    for i in T:
        if broom.intersects_line(i):
            return True
    return False


def visible(w: Point, pw: Line, obstacles: list[Obstacle], i: int, w_list: list[Point], BroomT: SortedList,
            visible_list: list[bool]):
    w_obstacle = obstacles[w.oind]

    if w.oind == pw.p1.oind:
        if w_obstacle.same_line(pw.p1, pw.p2):
            return True

    if w.oind == pw.p1.oind:
        if w_obstacle.isDiagonal(pw): # Diagonal Check
            return False

    if len(w_obstacle.get_intersecting_edges(pw)) != 0:# Intersect the interior of the w_obstacle
        return False

    elif i == 0 or orient(pw.p1, pw.p2, w_list[i - 1]) != 0:
        # w is first vertex in sorted array or w(i-1) not on the segment pw

        if len(BroomT) > 0 and pw.intersects_line(BroomT[0]): # e exist and pw intersect e
            return False
        else:
            return True

    elif not visible_list[i - 1]:  # w(i-1) is not visible
        return False
    else:  # Search in BroomT for an edge e that intersect w(i - 1)w
        if searchForIntersection(BroomT, pw):
            return True
        else:
            return False

def visible_vertices(point: Point, obstacles: list[Obstacle], graph: Graph, vertices: list[Point],
                     visualiser: VisibilityVisualiser):

    BroomT = SortedSet()
    w_list = copy.deepcopy(vertices)
    if point.ind != 0:
        w_list.remove(vertices[0])

    w_list.remove(point)
    Point.update_origin(point)

    w_list = sorted(w_list)
    half_line = Line(point, Point((Point.max_X, point.y), -3, -3))
    Line.updateCmpLine(half_line)

    if visualiser is not None:
        visualiser.create_broom_scene(half_line)

    for obstacle in obstacles:
        edges = obstacle.get_intersecting_edges(half_line)

        for edge in edges:
            edge.seenCount= True
            BroomT.add(edge)

    if visualiser is not None:
        lines = [it for it in BroomT]
        visualiser.intersecting_scene(lines)


    visible_found = [False for _ in range(len(w_list))]

    for i in range(len(w_list)):
        half_line = Line(point, w_list[i])
        Line.updateCmpLine(half_line)

        if visible(w_list[i], half_line, obstacles, i, w_list, BroomT, visible_found):

            if visualiser is not None:
                lines = [it for it in BroomT]
                visualiser.change_broom_scene(half_line, lines, True)

            visible_found[i] = True
            graph.add_edge(point.ind, w_list[i].ind, point.distance(w_list[i]))  #Adding edges to the graph


        elif visualiser is not None:
            lines = [it for it in BroomT]
            visualiser.change_broom_scene(half_line, lines, False)


        if w_list[i].ind == vertices[-1].ind: continue

        w_obstacle = obstacles[w_list[i].oind]
        temp = w_obstacle.get_incident_lines(w_list[i])

        if temp[0].seenCount == False and temp[1].seenCount == True: #prioritise removing over adding
            temp[0], temp[1] = temp[1], temp[0]

        for edge in temp:
            if edge.seenCount == True:  # lie on the COUNTERclockwise side
                edge.seenCount = False
                BroomT.discard(edge)
            elif edge.seenCount == False and edge != half_line:  # lie on the clockwise side
                edge.seenCount = True
                BroomT.add(edge)

    if visualiser is not None:
        visualiser.graph_connection_scene(point)

    for edge in BroomT:
        edge.seenCount = False
    BroomT.clear()


def compute_graph(points: list[Point], obstacles: list[Obstacle], vis_flag=True):
    graph = Graph()

    visualiser = None

    if vis_flag:
        lines = [line for obstacle in obstacles for line in obstacle.edges]  # Do not tests
        visualiser = VisibilityVisualiser(lines, points, points[0], points[-1], Point.max_X)

        visualiser.create_start_scene()

    for k in range(len(points)):
        i = points[k]
        node = Node(i.ind, i)
        graph.add_node(node)

    for i in points:
        visible_vertices(i, obstacles, graph, points, visualiser)

    scenes = []
    if vis_flag:
        scenes = visualiser.get_scenes()

    return graph, scenes
