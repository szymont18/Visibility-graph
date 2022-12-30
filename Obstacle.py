import math
import numpy as np

EPS = 10 ** (-10)


def det(a, b, c):
    return a.x * b.y + a.y * c.x + b.x * c.y - c.x * b.y - b.x * a.y - a.x * c.y


def orient(p1, p2, p3):
    valo = np.linalg.det([[p1.x, p1.y, 1], [p2.x, p2.y, 1], [p3.x, p3.y, 1]])
    # print(p1.x, p1.y, p2.ind, "   ", p2.x, p2.y, p2.ind, "   ", p3.x, p3.y, p3.ind, "   ", round(valo, 2))
    if valo > EPS:
        return 1
    elif valo < EPS:
        return -1
    else:
        return 0


def crossProd(l1, l2):
    v1 = (l1.p1.x - l1.p2.x, l1.p1.y - l1.p2.y)
    v2 = (l2.p1.x - l2.p2.x, l2.p1.y - l2.p2.y)

    return v1[0] * v2[1] - v1[1] * v2[0]


class Point:
    origin = None
    max_X = -float('inf')

    def __init__(self, p, pointIndex,
                 obstacleIndex):
        self.x = p[0]
        self.y = p[1]

        self.ind = pointIndex
        self.oind = obstacleIndex

        Point.max_X = max(Point.max_X, self.x)  # 10 % longer Broom ( int )

    def updateOrigin(og):
        Point.origin = og

    def distance(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def distSqr(self):
        return (self.x - Point.origin.x) ** 2 + (self.y - Point.origin.y) ** 2

    def findAngle(self):
        dx = self.x - Point.origin.x
        dy = self.y - Point.origin.y

        atan = math.atan2(dy, dx)

        if atan <= 0:
            return atan + 2 * math.pi
        else:
            return atan

    def __eq__(self, other):
        return self.ind == other.ind

    def __gt__(self, other):
        angle1 = self.findAngle()
        angle2 = other.findAngle()

        if angle1 > angle2:
            return False
        elif angle1 < angle2:
            return True
        else:
            return self.distSqr() < other.distSqr()


class Line:
    def __init__(self, p1, p2):  # p1 = Point a, p2 = Point b
        self.p1 = p1
        self.p2 = p2

        t1 = p1.x - p2.x

        if t1 < EPS and t1 > -1 * EPS:
            self.m = 0
        else:
            self.m = (p1.y - p2.y) / t1

        self.b = p1.y - self.m * p1.x

        if abs(self.m) < EPS:
            self.xIntercept = None
        else:
            self.xIntercept = -1 * self.b / self.m

        self.seenCount = 0
        self.sweepDistance = 0

    def halfLineOrientation(self, halfLine):
        hp2 = halfLine.p2

        if self.p1 == hp2:
            t = crossProd(halfLine, self)
            if t > 0:
                return 1  # cw
            else:
                return -1  # ccw
        else:
            t = crossProd(halfLine, Line(self.p2, self.p1))
            if t > 0:
                return 1  # cw
            else:
                return -1  # ccw

    def getLineValAtX(self, x):
        return self.m * x + self.b

    def intersectsLine(self, other):
        p1 = self.p1
        p2 = self.p2

        q1 = other.p1
        q2 = other.p2

        o1 = orient(p1, p2, q1)
        o2 = orient(p1, p2, q2)
        o3 = orient(q1, q2, p1)
        o4 = orient(q1, q2, p2)

        if (o1 != o2) and (o3 != o4) and o1 != 0 and o2 != 0 and o3 != 0 and o4 != 0:
            return True

        if (o1 == 0 or o2 == 0) and (o3 == 0 or o4 == 0) and (other.p1 == self.p2 or other.p2 == self.p2):
            return False
        return False

    def __eq__(self, other):
        return (self.p1.ind == other.p1.ind and self.p2.ind == other.p2.ind) or (
                self.p1.ind == other.p2.ind and self.p2.ind == other.p1.ind)

    def __gt__(self, other):
        return self.sweepDistance > other.sweepDistance

    def getLen(self):
        return (self.p2.x - self.p1.x) ** 2 + (self.p2.y - self.p1.y) ** 2

    def updateSweepLen(self, new):
        self.sweepDistance = new


class Obstacle:
    def __init__(self, index):
        self.points = []  # list of Point objects
        self.edges = []  # list of Line objects
        self.ind = index
        self.pointIndices = set()
        self.minVertex = float('inf')

    def addPoint(self, p):
        self.points.append(p)
        self.pointIndices.add(p.ind)
        if p.ind < self.minVertex:
            self.minVertex = p.ind

    def addEdge(self, e):
        self.edges.append(e)

    def getIncidentLines(self, vertex):
        retind = vertex.ind - self.minVertex

        return [self.edges[retind], self.edges[retind - 1]]

    def getIntersectingEdges(self, line):
        rettab = []

        for i in self.edges:
            if line.p1 == i.p1 or line.p1 == i.p2:
                continue
            if line.p2 == i.p1 or line.p2 == i.p2:
                continue
            if line.intersectsLine(i):
                if line.p2.x == Point.max_X:
                    line.sweepDistance = line.xIntercept
                rettab.append(i)
        return rettab

    def same_line(self, point1: Point, point2: Point):  # Check if the point1 and point2 are lying on the same line
        if (point1.ind - self.minVertex + 1) % (len(self.points)) == (point2.ind - self.minVertex) or \
                (point2.ind - self.minVertex + 1) % (len(self.points)) == (point1.ind - self.minVertex): return True

        return False
