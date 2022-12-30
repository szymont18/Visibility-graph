from Graph import *
from Obstacle import *
from graphicTool import *


def get_obstacle_from_linesCollection(lcol: LinesCollection, pointcount: int, obscount: int):
    lines = lcol.lines

    pts = []
    newobs = Obstacle(obscount)

    pointcount += 1
    p1 = Point(lines[0][0], pointcount, obscount)
    pointcount += 1
    p2 = Point(lines[0][1], pointcount, obscount)
    pts.append(p1)
    pts.append(p2)

    newobs.add_point(p1)
    newobs.add_point(p2)

    newobs.add_edge(Line(p1, p2))
    for i in range(1, len(lines) - 1):
        p1 = p2
        pointcount += 1
        p2 = Point(lines[i][1], pointcount, obscount)
        pts.append(p2)
        newobs.add_point(p2)
        newobs.add_edge(Line(p1, p2))
    newobs.add_edge(Line(p2, pts[0]))
    return newobs, pts, pointcount


def get_added_elements(plot1: Plot):
    obstList = []

    start_end = plot1.get_added_points()

    start = start_end[0].points[0]
    end = start_end[0].points[1]

    pointList = [Point(start, 0, -1)]

    plotLines = plot1.get_added_figure()
    pointCounter = 0
    obstacleCounter = 0

    for i in range(len(plotLines)):
        if plotLines[i].lines:  # I do not know why there are some empty LinesCollection
            res = get_obstacle_from_linesCollection(plotLines[i], pointCounter, obstacleCounter)
            obstacleCounter += 1
            pointCounter = res[2]
            obstList.append(res[0])
            pointList += res[1]

    end_obstacle = Obstacle(obstacleCounter)
    end_point = Point(end, pointCounter + 1, -2)

    end_obstacle.add_point(end_point)
    pointList.append(end_point)
    obstList.append(end_obstacle)

    return pointList, obstList
