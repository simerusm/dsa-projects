import heapq

# Sample graph
# vertex1 = [(vertex2, weight), ...]
graph = {
    "a": [("d", 5)],
    "b": [("a", 6), ("e", 3)],
    "c": [("a", 14)],
    "d": [("c", 12), ("e", 5), ("f", 7)],
    "e": [("a", 2), ("f", 20)],
    "f": [("h", 15)],
    "g": [("d", 9)],
    "h": []
}

def dijkstra(graph: dict[str, list[Tuple[str, int]], start: str):
    # shortest known distance from start to each node
    dist = {v: float("inf") for v in graph}
    dist[start] = 0

    # previous node on shortest path
    prev = {v: None for v in graph}

    # min-heap of (distance, vertex)
    pq = [(0, start)]

    while pq:
        curr_dist, u = heapq.heappop(pq)

        # stale entry check
        if curr_dist > dist[u]:
            continue

        # relax all outgoing edges from u
        for v, weight in graph[u]:
            new_dist = curr_dist + weight

            if new_dist < dist[v]:
                dist[v] = new_dist
                prev[v] = u
                heapq.heappush(pq, (new_dist, v))

    return dist, prev
