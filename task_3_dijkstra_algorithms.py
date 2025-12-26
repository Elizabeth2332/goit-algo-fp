import heapq
import math
import networkx as nx


# Create weighted graph
G = nx.DiGraph()

G.add_edge("A", "B", weight=4)
G.add_edge("A", "C", weight=2)
G.add_edge("C", "B", weight=1)
G.add_edge("B", "D", weight=5)
G.add_edge("C", "D", weight=8)
G.add_edge("D", "E", weight=6)
G.add_edge("B", "E", weight=10)


# Dijkstra using binary heap
def dijkstra_heap(graph, source, weight="weight"):
    dist = {node: math.inf for node in graph.nodes()}
    prev = {node: None for node in graph.nodes()}
    dist[source] = 0

    heap = [(0, source)]

    while heap:
        cur_dist, u = heapq.heappop(heap)

        if cur_dist > dist[u]:
            continue

        for v in graph.successors(u):
            w = graph[u][v][weight]
            new_dist = cur_dist + w

            if new_dist < dist[v]:
                dist[v] = new_dist
                prev[v] = u
                heapq.heappush(heap, (new_dist, v))

    return dist, prev


def reconstruct_path(prev, start, end):
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path if path[0] == start else None


# Run algorithm
start = "A"

distances, previous = dijkstra_heap(G, start)

print("Shortest distances from A:")
for node, d in distances.items():
    print(f"A → {node}: {d}")

print("\nPath A → E:")
