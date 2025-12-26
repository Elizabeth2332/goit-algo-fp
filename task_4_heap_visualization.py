import uuid
import heapq
import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)

        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)

        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)

    return graph


def draw_tree(tree_root, title="Binary Heap Visualization"):
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    add_edges(tree, tree_root, pos)

    colors = [node[1]["color"] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]["label"] for node in tree.nodes(data=True)}

    plt.figure(figsize=(10, 6))
    plt.title(title)
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2200, node_color=colors)
    plt.show()


# Build a binary heap tree from an array (heap) and visualize it
def build_heap_tree(heap_array):
    """
    Convert a binary heap stored as an array into a binary tree of Node objects.
    heap_array: list (e.g., result of heapq.heapify)
    Returns: root Node or None
    """
    if not heap_array:
        return None

    nodes = [Node(value) for value in heap_array]

    for i in range(len(nodes)):
        left_i = 2 * i + 1
        right_i = 2 * i + 2

        if left_i < len(nodes):
            nodes[i].left = nodes[left_i]
        if right_i < len(nodes):
            nodes[i].right = nodes[right_i]

    return nodes[0]


if __name__ == "__main__":
    # Example: build a MIN-HEAP using heapq and visualize it
    data = [10, 3, 5, 2, 7, 1, 9, 8, 4, 6]

    heapq.heapify(data)  # now 'data' is a valid min-heap array
    print("Heap array:", data)

    root = build_heap_tree(data)
    draw_tree(root, title="Min-Heap (array -> tree)")
