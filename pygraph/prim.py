import random
from typing import (
    Hashable,
)

from .graph import (
    Graph, Vertex, Edge
)
from .exceptions import (
    GraphException,
)
from .minheap import MinHeap
# implement minimum spanning tree using prim's algo.

# Prim's algorithm:
# randomly choose a vertex as start
# put edges of the vertex into min queue
# mark vertex as visited
# while not all vertex is visited:
#   extract min edge from queue
#   if the other side is not connected:
#       connect the other side
#       mark edge as visited
#       put the edges of other side into queue
# return new graph

def edge_less(e_a: Edge, e_b: Edge) -> bool:
    return e_a.weight < e_b.weight

def min_span_tree(g: Graph) -> Graph:
    """Minimum spanning tree using Prim's algorithm."""
    g_res = Graph()
    visited_vertices = set()
    visited_edges = set()
    minqueue = MinHeap(edge_less)
    
    v_start: Hashable = random.choice(list(g.vertices.keys()))
    visited_vertices.add(v_start)
    v = g.vertices[v_start]
    g_res.AddVertex(v_start)
    for edg in v.edges.values():
        if edg in visited_edges:
            continue
        #visited_edges.add(edg)
        minqueue.insert(edg)
    
    while len(g.vertices) > len(visited_vertices):
        edg: Edge = minqueue.extract_min()
        visited_edges.add(edg)
        
        v_src, v_dst = edg.vertices
        v_other: Vertex = None
        if v_src.ident in visited_vertices and v_dst.ident in visited_vertices:
            continue
        if not v_dst.ident in visited_vertices:
            v_other = v_dst #.ident
        if not v_src.ident in visited_vertices:
            v_other = v_src #.ident
            v_src, v_dst = v_dst, v_src
        if v_other is None:
            raise GraphException(
                "Assertion violated: both side of edge do not in any graph."
            )
        visited_vertices.add(v_other.ident)
        g_res.AddVertex(v_other.ident)
        g_res.AddEdge(v_src.ident, v_other.ident, edg.weight)
        for edge in v_other.edges.values():
            minqueue.insert(edge)
    assert len(g.vertices) == len(visited_vertices)
    
    return g_res