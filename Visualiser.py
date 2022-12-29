from graphicTool import *
from Graph import *
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

    def __init__(self, lines: list[[(float, float), (float, float)]], points: list[(float, float)],
                 start_point: (int, int), end_point: (int, int)):
        self.lines = lines
        self.points = points
        self.start_point = start_point
        self.end_point = end_point
