from visibility import *
from util import getAddedElements
from dijkstra import dijkstra

# Drawing new map (obstacles, start and destiny points)
plot = Plot()
plot.draw()

# Get list of points and obstacles
points, obstacles = getAddedElements(plot)


# Get start and end points from points list
start_point = points[0]
end_point = points[-1]

# Create Visibility Graph
visible_graph = computeGraph(points, obstacles)

# Find the shortest path
distance, parent, scenes = dijkstra(visible_graph, 0, len(points) - 1, True)
dijkstra_plot = Plot(scenes=scenes)
dijkstra_plot.draw()