import uuid
from collections import deque
import matplotlib.pyplot as plt
import networkx as nx
import heapq


# =========================
# Node + build tree from heap
# =========================
class Node:
    def __init__(self, key, color="#2b2b2b"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def build_heap_tree(heap_array):
    """Convert heap array (0-based) to a binary tree of Node objects."""
    if not heap_array:
        return None, {}

    nodes = [Node(v) for v in heap_array]
    id_to_node = {n.id: n for n in nodes}

    for i in range(len(nodes)):
        li = 2 * i + 1
        ri = 2 * i + 2
        if li < len(nodes):
            nodes[i].left = nodes[li]
        if ri < len(nodes):
            nodes[i].right = nodes[ri]

    return nodes[0], id_to_node


# =========================
# Build graph + fixed positions (same as task 4 idea)
# =========================
def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is None:
        return graph

    graph.add_node(node.id, color=node.color, label=node.val)

    if node.left:
        graph.add_edge(node.id, node.left.id)
        lx = x - 1 / 2 ** layer
        pos[node.left.id] = (lx, y - 1)
        add_edges(graph, node.left, pos, x=lx, y=y - 1, layer=layer + 1)

    if node.right:
        graph.add_edge(node.id, node.right.id)
        rx = x + 1 / 2 ** layer
        pos[node.right.id] = (rx, y - 1)
        add_edges(graph, node.right, pos, x=rx, y=y - 1, layer=layer + 1)

    return graph


def build_graph_and_pos(root):
    G = nx.DiGraph()
    pos = {root.id: (0, 0)}
    add_edges(G, root, pos)
    return G, pos


def draw_graph(G, pos, title):
    colors = [G.nodes[n]["color"] for n in G.nodes()]
    labels = {n: G.nodes[n]["label"] for n in G.nodes()}

    plt.clf()
    plt.title(title)
    nx.draw(G, pos=pos, labels=labels, arrows=False,
            node_size=2200, node_color=colors, font_size=10)
    plt.tight_layout()
    plt.pause(0.6)  # speed of animation (smaller = faster)


# =========================
# Color gradient: dark -> light (hex #RRGGBB)
# =========================
def lerp(a, b, t):
    return int(a + (b - a) * t)


def gradient_colors(n, start_hex="#102a43", end_hex="#e6f6ff"):
    """
    Generate n unique colors from dark -> light.
    """
    def hex_to_rgb(h):
        h = h.lstrip("#")
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

    def rgb_to_hex(r, g, b):
        return f"#{r:02x}{g:02x}{b:02x}"

    sr, sg, sb = hex_to_rgb(start_hex)
    er, eg, eb = hex_to_rgb(end_hex)

    if n <= 1:
        return [rgb_to_hex(sr, sg, sb)]

    cols = []
    for i in range(n):
        t = i / (n - 1)
        r = lerp(sr, er, t)
        g = lerp(sg, eg, t)
        b = lerp(sb, eb, t)
        cols.append(rgb_to_hex(r, g, b))
    return cols


# =========================
# Traversals (NO recursion)
# =========================
def dfs_stack_order(root):
    """DFS (preorder) using stack: root, left, right."""
    order = []
    stack = [root]

    while stack:
        node = stack.pop()
        order.append(node)

        # push right first so left processed first
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return order


def bfs_queue_order(root):
    """BFS using queue."""
    order = []
    q = deque([root])

    while q:
        node = q.popleft()
        order.append(node)
        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)

    return order


# =========================
# Animation
# =========================
def animate_traversal(root, traversal_name, order, id_to_node, G, pos):
    # reset node colors (dark)
    for node in id_to_node.values():
        node.color = "#2b2b2b"
        G.nodes[node.id]["color"] = node.color

    colors = gradient_colors(len(order), start_hex="#0b1f3a", end_hex="#cfefff")

    plt.figure(figsize=(10, 6))
    plt.ion()

    # initial state
    draw_graph(G, pos, f"{traversal_name}: start")

    for i, node in enumerate(order):
        node.color = colors[i]
        G.nodes[node.id]["color"] = node.color
        draw_graph(G, pos, f"{traversal_name}: step {i+1}/{len(order)} (visit {node.val})")

    plt.ioff()
    plt.show()


# =========================
# Main
# =========================
if __name__ == "__main__":
    # Example data -> heap -> tree
    data = [10, 3, 5, 2, 7, 1, 9, 8, 4, 6]
    heapq.heapify(data)  # min-heap array
    print("Heap array:", data)

    root, id_to_node = build_heap_tree(data)
    G, pos = build_graph_and_pos(root)

    # DFS (stack)
    dfs_order = dfs_stack_order(root)
    animate_traversal(root, "DFS (stack, depth-first)", dfs_order, id_to_node, G, pos)

    # BFS (queue)
    bfs_order = bfs_queue_order(root)
    animate_traversal(root, "BFS (queue, breadth-first)", bfs_order, id_to_node, G, pos)
