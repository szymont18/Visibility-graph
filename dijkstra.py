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

    visualiser = DijkstraVisualiser(G.node_coord, G.edges_coord, t)

    PQ.put((0, s))
    visited[s] = True
    distance[s] = 0

    if visualise_flag: visualiser.create_start_scene()

    while not PQ.empty():
        d, v = PQ.get()
        visited[v] = True

        if visualise_flag:
            visualiser.create_scene(v, v)

        if v == t:
            if visualise_flag:
                visualiser.create_end_scene(parent, s, t)
            return distance[t], parent, visualiser.get_scenes()

        for u, weight in G.nodeList[v].edges.items():

            if visited[u]: continue

            if visualise_flag: visualiser.create_scene(v, u)

            if distance[u] > distance[v] + weight:
                distance[u] = distance[v] + weight
                parent[u] = v
                PQ.put((distance[u], u))

        if visualise_flag: visualiser.process_point(v)

    return distance[t], parent, visualiser.get_scenes()

