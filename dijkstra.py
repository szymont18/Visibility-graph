import queue
from Graph import *
from Visualiser import *


def dijkstra(G: Graph, s: int, t: int, visualise_flag: bool = True):
    '''
    Returns the value of the shortest path and the path between vertex s and t in graph G
    '''
    V = len(G)
    distance = [float('inf') for _ in range(V)]
    visited = [False for _ in range(V)]
    parent = [None for _ in range(V)]
    PQ = queue.PriorityQueue()
    visualiser = DijkstraVisualiser(G.node_coord, G.edges_coord)

    PQ.put((0, s))
    visited[s] = True
    distance[s] = 0

    if visualise_flag: visualiser.create_start_scene()

    while not PQ.empty():
        d, v = PQ.get()
        visited[v] = True
        if v == t: return distance[t], parent, visualiser.get_scenes()

        if visualise_flag:
            visualiser.create_scene(v, v)

        for u, weight in G.nodeList[v].edges.items():

            if visited[u]: continue

            if visualise_flag: visualiser.create_scene(v, u)

            if distance[u] > distance[v] + weight:
                distance[u] = distance[v] + weight
                parent[u] = v
                PQ.put((distance[u], u))

        if visualise_flag: visualiser.process_point(v)

    return distance[t], parent, visualiser.get_scenes

'''
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
'''

######################################################################

'''
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