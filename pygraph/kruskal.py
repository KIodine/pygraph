from typing import (
    List,
)

from .graph import (
    Vertex,
    Edge,
    Graph,
)
from .minheap import (
    MinHeap,
)
from .unionfind import (
    UFNode,
    union,
    find,
    is_connected,
)


def edge_less(a: Edge, b: Edge) -> bool:
    return a.weight < b.weight

def min_span_tree(g: Graph) -> Graph:
    # Minimum spanning tree using Kruskal's algorithm.
    # Put all edges into minqueue
    # extract edges from queue
    # if two ends of edge is not connected, create an edge between them and
    # do connect them.
    # otherwise skip.
    g_out = Graph()
    edges = list(g.edges)
    edg: Edge = None
    minqueue = MinHeap(edge_less, arr=edges)
    while not minqueue.is_empty():
        edg = minqueue.extract_min()
        vert_a, vert_b = edg.vertices[0], edg.vertices[1]
        if not is_connected(vert_a.uf_node, vert_b.uf_node):
            union(vert_a.uf_node, vert_b.uf_node)
            g_out.AddVertex(vert_a.ident)
            g_out.AddVertex(vert_b.ident)
            g_out.AddEdge(vert_a.ident, vert_b.ident, edg.weight)
        pass
    for v in g.vertices.values():
        v.uf_node.reset()
    return g_out