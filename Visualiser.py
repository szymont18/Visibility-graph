from graphicTool import *
from Graph import *
import copy


class DijkstraVisualiser:
    def __init__(self, points: list[(int, int)], edges: list[[(int, int), (int, int)]]):
        self.points = points
        self.edges = edges
        self.processed_points = []
        self.scenes = []

    def create_start_scene(self):
        self.scenes.append(Scene([PointsCollection(self.points)],
                        [LinesCollection(self.edges)]))

    def process_point(self, p: int):
        self.processed_points.append(self.points[p])

    def create_scene(self, start_point: int, end_point: int):

        self.scenes.append(Scene([PointsCollection(self.points),
               PointsCollection([self.points[start_point]], color='orange'),
               PointsCollection([self.points[end_point]], color='lime'),
                PointsCollection(self.processed_points.copy(), color='black')],
              [LinesCollection(self.edges),
               LinesCollection([[self.points[start_point], self.points[end_point]]], color='red')]))

    def get_scenes(self):
        return self.scenes

