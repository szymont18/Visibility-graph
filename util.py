from Graph import *
from Obstacle import *
from graphicTool import *


def getObstacleFromLinesCollection(lcol, pointcount, obscount):
    lines = lcol.lines

    pts = []
    newobs = Obstacle(obscount)

    pointcount += 1
    p1 = Point(lines[0][0], pointcount, obscount)
    pointcount += 1
    p2 = Point(lines[0][1], pointcount, obscount)
    pts.append(p1)
    pts.append(p2)

    newobs.addPoint(p1)
    newobs.addPoint(p2)

    newobs.addEdge(Line(p1, p2))
    for i in range(1, len(lines) - 1):
        p1 = p2
        pointcount += 1
        p2 = Point(lines[i][1], pointcount, obscount)
        pts.append(p2)
        newobs.addPoint(p2)
        newobs.addEdge(Line(p1, p2))
    newobs.addEdge(Line(p2, pts[0]))
    return newobs, pts, pointcount


def getAddedElements(plot1):
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
            res = getObstacleFromLinesCollection(plotLines[i], pointCounter, obstacleCounter)
            obstacleCounter += 1
            pointCounter = res[2]
            obstList.append(res[0])
            pointList += res[1]
    pointList.append(Point(end, pointCounter + 1, -2))
    return pointList, obstList
