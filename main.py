from visibility import *
from util import get_added_elements
from dijkstra import dijkstra

# Drawing new map (obstacles, start and destiny points)
plot = Plot()
plot.draw()

# Get list of points and obstacles
points, obstacles = get_added_elements(plot)


# Get start and end points from points list
start_point = points[0]
end_point = points[-1]

# Create Visibility Graph
visible_graph, scenes_g = compute_graph(points, obstacles)
graph_plot = Plot(scenes=scenes_g)
graph_plot.draw()

# Find the shortest path
distance, parent, scenes = dijkstra(visible_graph, 0, len(points) - 1, True)
dijkstra_plot = Plot(scenes=scenes)
dijkstra_plot.draw()