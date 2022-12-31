from graphicTool import *
from Graph import *
from Obstacle import *
import copy


class DijkstraVisualiser:
    def __init__(self, points: list[(int, int)], edges: list[[(int, int), (int, int)]], destiny: int):
        self.points = points
        self.edges = edges
        self.processed_points = []
        self.scenes = []
        self.destiny = points[destiny]

    def create_start_scene(self):
        self.scenes.append(Scene([PointsCollection(self.points),
                                  PointsCollection([self.destiny], color='purple')],
                        [LinesCollection(self.edges)]))

    def process_point(self, p: int):
        self.processed_points.append(self.points[p])

    def create_scene(self, start_point: int, end_point: int):

        self.scenes.append(Scene([PointsCollection(self.points),
                                  PointsCollection([self.destiny], color='purple'),
               PointsCollection([self.points[start_point]], color='orange'),
               PointsCollection([self.points[end_point]], color='lime'),
                PointsCollection(self.processed_points.copy(), color='black')],
              [LinesCollection(self.edges),
               LinesCollection([[self.points[start_point], self.points[end_point]]], color='red')]))

    def create_end_scene(self, parent: list[int], s:int, t:int):
        parent_lines = []
        parent_points = []
        while t != s:
            parent_points.append(self.points[t])
            parent_lines.append([self.points[t], self.points[parent[t]]])
            t = parent[t]

        parent_points.append(self.points[s])

        self.scenes.append(Scene([PointsCollection(self.points, color='grey'),
                                  PointsCollection(parent_points, color='black')],
                                 [LinesCollection(self.edges, color='grey'),
                                  LinesCollection(parent_lines, color='red')]))

    def get_scenes(self):
        return self.scenes


class VisibilityVisualiser:

    def __init__(self, lines: list[Line], points: list[Point],
                 start_point: Point, end_point: Point, x:float):
        self.lines = [[(line.p1.x, line.p1.y), (line.p2.x, line.p2.y)] for line in lines]

        self.points = [(point.x, point.y) for point in points]
        self.start_point = (start_point.x, start_point.y)
        self.end_point = (end_point.x, end_point.y)
        self.broom_X = x
        self.scenes = []
        self.visible_vert = [[] for i in range(len(points) + 2)]

    def create_start_scene(self):
        self.scenes.append(Scene([PointsCollection(self.points),
                                  PointsCollection([self.start_point], color='purple'),
                                  PointsCollection([self.end_point], color='purple')],
                                 [LinesCollection(self.lines)]))

    def get_scenes(self):
        return self.scenes

    def create_broom_scene(self, broom: Line):
        first_point = (broom.p1.x, broom.p1.y)
        second_point = (self.broom_X, broom.p2.y)
        broom_line = [[first_point, second_point]]

        self.broom_line = broom_line

        self.scenes.append(Scene([PointsCollection(self.points, color='grey'),
                                  PointsCollection([first_point], color='orange')],
                                 [LinesCollection(self.lines, color='grey'),
                                  LinesCollection(broom_line, color='red')]))

    def intersecting_scene(self, intersecting_lines: list[Line]):
        lines = [[(line.p1.x, line.p1.y), (line.p2.x, line.p2.y)] for line in intersecting_lines]
        self.scenes.append(Scene([PointsCollection(self.points, color='grey'),
                                  PointsCollection([(self.broom_line[0][0][0], self.broom_line[0][0][1])], color='orange')],
                                 [LinesCollection(self.lines, color='grey'),
                                  LinesCollection(self.broom_line, color='red'),
                                  LinesCollection(lines)]))

    def change_broom_scene(self, broom: Line, lines: list[Line], visible_flag: bool):
        first_point = (broom.p1.x, broom.p1.y)
        second_point = (broom.p2.x, broom.p2.y)
        broom_line = [[first_point, second_point]]
        lines = [[(line.p1.x, line.p1.y), (line.p2.x, line.p2.y)] for line in lines]

        self.broom_line = broom_line

        self.scenes.append(Scene([PointsCollection(self.points, color='grey'),
                                  PointsCollection([first_point],color='orange'),
                                  PointsCollection([second_point], color='lime'),
                                  PointsCollection(self.visible_vert[broom.p1.ind].copy(), color='green')],
                                 [LinesCollection(self.lines, color='grey'),
                                  LinesCollection(self.broom_line, color='red'),
                                  LinesCollection(lines)]))

        if visible_flag:
            self.visible_vert[broom.p1.ind].append(second_point)
            self.scenes.append(Scene([PointsCollection(self.points, color='grey'),
                                      PointsCollection([first_point], color='orange'),
                                      PointsCollection([second_point], color='lime'),
                                      PointsCollection(self.visible_vert[broom.p1.ind].copy(), color='green')],
                                     [LinesCollection(self.lines, color='grey'),
                                      LinesCollection(self.broom_line, color='red'),
                                      LinesCollection(lines)]))

        elif first_point in self.visible_vert[broom.p2.ind]:
            self.visible_vert[broom.p1.ind].append(second_point)
            self.scenes.append(Scene([PointsCollection(self.points, color='grey'),
                                      PointsCollection([first_point], color='orange'),
                                      PointsCollection([second_point], color='lime'),
                                      PointsCollection(self.visible_vert[broom.p1.ind].copy(), color='green')],
                                     [LinesCollection(self.lines, color='grey'),
                                      LinesCollection(self.broom_line, color='red'),
                                      LinesCollection(lines)]))

        else:
            self.scenes.append(Scene([PointsCollection(self.points, color='grey'),
                                      PointsCollection([first_point], color='orange'),
                                      PointsCollection([second_point], color='lime'),
                                      PointsCollection(self.visible_vert[broom.p1.ind].copy(), color='green'),
                                      PointsCollection([second_point], color='red')],
                                     [LinesCollection(self.lines, color='grey'),
                                      LinesCollection(self.broom_line, color='red'),
                                      LinesCollection(lines)]))

    def graph_connection_scene(self, point: Point):
        edges = [[(self.visible_vert[point.ind][i][0],self.visible_vert[point.ind][i][1]),
                  (point.x, point.y)] for i in range(len(self.visible_vert[point.ind]))]

        self.scenes.append(Scene([PointsCollection(self.points, color='grey'),
                                  PointsCollection([(point.x, point.y)], color='orange'),
                                  PointsCollection(self.visible_vert[point.ind].copy(), color='green')],
                                 [LinesCollection(self.lines, color='grey'),
                                  LinesCollection(edges, color='green')]))










