import math
import numpy as np

EPS = 10 ** (-10)


def orient(p1, p2, p3):
    valo = np.linalg.det([[p1.x, p1.y, 1], [p2.x, p2.y, 1], [p3.x, p3.y, 1]])
    if valo > EPS:
        return 1
    elif valo < -1*EPS:
        return -1
    else:
        return 0

class Point:
    origin = None
    max_X = -float('inf')

    def __init__(self, p: (float, float), pointIndex: int,
                 obstacleIndex:int):
        self.x = p[0]
        self.y = p[1]

        self.ind = pointIndex
        self.oind = obstacleIndex

        Point.max_X = max(Point.max_X, self.x)  # 10 % longer Broom ( int )

    def __repr__(self):
        return "Point()"

    def __str__(self):
        return str(self.x) +" "+ str(self.y) +" "+ str(self.ind)

    def update_origin(og):
        Point.origin = og

    def distance(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def dist_sqr(self):
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
             return self.dist_sqr() > other.dist_sqr()


class Line:
    cmpLine = None
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

        self.seenCount = False

    def updateCmpLine(line):
        Line.cmpLine = line

    def intersects_line(self, other):
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
        selfintersectionpoint = self.getIntersectionPoint(Line.cmpLine)
        otherIntersectionPoint = other.getIntersectionPoint(Line.cmpLine)
        porigin = Line.cmpLine.p1
        dist1 = math.sqrt((porigin.x - selfintersectionpoint[0])**2 + (porigin.y - selfintersectionpoint[1])**2)
        dist2 = math.sqrt((porigin.x - otherIntersectionPoint[0]) ** 2 + (porigin.y - otherIntersectionPoint[1]) ** 2)

        if abs(dist1-dist2) < EPS:
            p0 = Line.cmpLine.p1

            p1 = self.p1
            p2 = self.p2

            p3 = other.p1
            p4 = other.p2

            mainpoint = None
            if p1 == Line.cmpLine.p2:
                mainpoint = p1

                if p3==mainpoint:
                    o = orient(mainpoint,p2,p4)
                    if orient(mainpoint, p2, p0) == orient(mainpoint,p4,p0) < 0:
                        if o <0:
                            return True
                        else:
                            return False
                    else:
                        if o >0:
                            return True
                        else:
                            return False
                elif p4==mainpoint:
                    o = orient(mainpoint,p2,p3)
                    if orient(mainpoint, p2, p0) == orient(mainpoint,p3,p0) < 0:
                        if o <0:
                            return True
                        else:
                            return False
                    else:
                        if o >0:
                            return True
                        else:
                            return False
            elif p2 == Line.cmpLine.p2:
                mainpoint = p2
                if p3==mainpoint:
                    o = orient(mainpoint,p1,p4)
                    if orient(mainpoint, p1, p0) == orient(mainpoint, p4, p0) < 0:
                        if o < 0:
                            return True
                        else:
                            return False
                    else:
                        if o > 0:
                            return True
                        else:
                            return False
                elif p4==mainpoint:
                    o = orient(mainpoint,p1,p3)
                    if orient(mainpoint, p1, p0) == orient(mainpoint,p3,p0) < 0:
                        if o <0:
                            return True
                        else:
                            return False
                    else:
                        if o >0:
                            return True
                        else:
                            return False

        return dist1-dist2 > EPS

    def __repr__(self):
        return "Line()"

    def __str__(self):
        op = Line.cmpLine.p1
        sp = Line.cmpLine.getIntersectionPoint(self)

        dist = math.sqrt((op.x - sp[0])**2 + (op.y-sp[1])**2)

        return str(self.p1) +"     "+ str(self.p2) +"    "+ str(dist) + "  ("+str(op)+")"

    def __hash__(self):
        return hash((self.p1.ind, self.p2.ind))

    def update_sweep_len(self, new):
        self.sweepDistance = new

    def getIntersectionPoint(self, other):
        a = self.m
        b = self.b

        c = other.m
        d = other.b

        if abs(a-c) < EPS:
            x=self.p1.x
        else:
            x = (d-b)/(a-c)
        y = x*self.m + self.b

        return x,y


class Obstacle:
    def __init__(self, index):
        self.points = []  # list of Point objects
        self.edges = []  # list of Line objects
        self.ind = index
        self.pointIndices = set()
        self.minVertex = float('inf')

    def add_point(self, p):
        self.points.append(p)
        self.pointIndices.add(p.ind)
        if p.ind < self.minVertex:
            self.minVertex = p.ind

    def add_edge(self, e):
        self.edges.append(e)

    def get_incident_lines(self, vertex):
        retind = vertex.ind - self.minVertex

        return [self.edges[retind], self.edges[retind - 1]]

    def get_intersecting_edges(self, line):
        rettab = []

        for i in self.edges:
            if line.p1 == i.p1 or line.p1 == i.p2:
                continue
            if line.p2 == i.p1 or line.p2 == i.p2:
                continue
            if line.intersects_line(i):
                if line.p2.x == Point.max_X:
                    intersectionPoint = line.getIntersectionPoint(i)
                rettab.append(i)
        return rettab

    def same_line(self, point1: Point, point2: Point):  # Check if the point1 and point2 are lying on the same line
        if (point1.ind - self.minVertex + 1) % (len(self.points)) == (point2.ind - self.minVertex) or \
                (point2.ind - self.minVertex + 1) % (len(self.points)) == (point1.ind - self.minVertex):
            return True

        return False

    def isDiagonal(self, line: Line):
        a = (line.p1.x + line.p2.x)/2
        b = (line.p1.y + line.p2.y)/2
        p0 = Point((a,b),-1,-1)


        Ray = Line(p0,Point((10,p0.y),-1,-1))
        intersectCount = 0
        for i in self.edges:
            if Ray.intersects_line(i):
                intersectCount+=1

        return intersectCount%2==1