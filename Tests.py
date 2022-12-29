from dijkstra import *
'''
-----DIJKSTRA-----

G = Graph([(0, 0), (1, 1), (6, 1), (6, -1), (1, -1), (10, 5)])
G.addEdge(0, 1, 1)
G.addEdge(0, 3, 5)
G.addEdge(0, 4, 2)
G.addEdge(1, 2, 7)
G.addEdge(2, 5, 10)
G.addEdge(3, 4, 2)
G.addEdge(3, 5, 2)
s = 0
t = 5
d, p, scenes = dijkstra(G, 0, 5)
print(d)
plot = Plot(scenes=scenes)
plot.draw()


G = Graph([(0, 5), (1, 7), (3, -2), (4, 3), (10, 6)])
G.addEdge(0,1,5)
G.addEdge(0,2,5)
G.addEdge(0,3,1)
G.addEdge(1,2,6)
G.addEdge(1,4,7)
G.addEdge(2,4,4)
G.addEdge(3,4,1)
s = 0
t = 4
d,p,scenes = dijkstra(G,s,t)
plot = Plot(scenes=scenes)
plot.draw()
'''

'''
-----UTIL-----

from util import *

plot_test = Plot()
plot_test.draw()

point_list, obstacle_list = getAddedElements((0, 0), (1, 1), plot_test)

print("points_list", point_list)
print("obstacle_list", obstacle_list)
'''