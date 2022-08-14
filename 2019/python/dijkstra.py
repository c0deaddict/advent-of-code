# https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Pseudocode
def dijkstra(graph, source):
    dist = {source: 0}
    prev = {}
    queue = set(graph.keys())

    while queue:
        u = min(queue, key=lambda v: dist[v] if v in dist else float("inf"))
        queue.remove(u)

        for (v, d) in graph[u].items():
            if v not in queue or u not in dist:
                continue
            alt = dist[u] + d
            if v not in dist or alt < dist[v]:
                dist[v] = alt
                prev[v] = u

    return dist, prev


def dijkstra_path(source, v, prev):
    path = []
    while True:
        v = prev[v]
        if v == source:
            return path
        path.append(v)
