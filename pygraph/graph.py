from typing import (
    List,
    Set,
    Mapping,
    Hashable,
    Callable
)

from .minheap import (
    MinHeap,
)
from .unionfind import UFNode
from .exceptions import (
    GraphException,
)


class Vertex():
    def __init__(self, ident: Hashable):
        # TODO: Add a `uf_node` member and implement `union-find` data struct.
        self.uf_node = UFNode() # for kruskal's algorithm.
        self.ident = ident
        self.edges = dict() # Mapping[Hashable, Edge] 
        return
    
    def __str__(self) -> str:
        s = "<Vertex [{}]>".format(
            ", ".join(
                (f"{ident}: {edge}" for ident, edge in self.edges.items())
            )
        )
        return s
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            raise GraphException(
                "Cannot compare type {} with {}".format(type(self), type(other))
            )
        v_other: Vertex = other
        if self.ident != v_other.ident:
            return False
        if self.edges.keys() != v_other.edges.keys():
            #print("no equal links")
            return False
        for ident, edge in self.edges.items():
            edge_other = v_other.edges[ident]
            if edge.weight != edge_other.weight:
                #print("no equal weight")
                return False
        return True
    pass


class Edge():
    def __init__(self, src: Vertex, dst: Vertex, weight: int):
        self.weight = weight
        self.vertices = [src, dst] # List[Vertex]
        return
    
    def __str__(self) -> str:
        s = f"<Edge @ 0x{id(self):016X}, weight={self.weight}>"
        return s
    pass


class Graph():
    """Undirected graph."""
    def __init__(self):
        self.vertices: Mapping[Hashable, Vertex] = dict() # Mapping[int, Vertex]
        self.edges = set()
        return
    
    def __str__(self) -> str:
        adjs = "\n".join(
            (f"    {ident}: {v}" for ident, v in self.vertices.items())
        )
        s = (
            f"<Graph @ 0x{id(self):016X},"
            f" {len(self.vertices)} vertices, {len(self.edges)} edges,"
            f" relations:\n{adjs}\n>"
        )
        return s

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            raise GraphException(f"Cannot compare type {type(self)} and {type(other)}.")
        # Compare each edge of vertices, if they have the same
        # destination and weight, they are the same.
        g_other: Graph = other
        if self.vertices.keys() != g_other.vertices.keys():
            return False
        for ident, v in self.vertices.items():
            if v != g_other.vertices[ident]:
                return False
        return True

    @classmethod
    def FromSpec(cls, spec: str):
        return

    # FIXME: Determine the correct behavior of adding an existed ident?
    def AddVertex(self, ident: Hashable) -> Vertex:
        if ident in self.vertices.keys():
            return
        self.vertices[ident] = Vertex(ident)
        return
    
    def AddEdge(self, src: Hashable, dst: Hashable, weight: int) -> Edge:
        va, vb = self.vertices[src], self.vertices[dst]
        edg = Edge(va, vb, weight)
        va.edges[dst] = edg
        vb.edges[src] = edg
        self.edges.add(edg)
        return
    pass

# > Do we just need to visit all vertices once? why?
#   If so, `union-find` can be very useful.
# using Dijkstra's algorithm.
def shortest_path(graph: Graph, src_id: Hashable, dst_id: Hashable):
    FAKE_INF = -1
    # Ensure no vertex is enqueued twice.
    # * `union-find` can add and check existence very fast, but cannot
    #   remove.
    visited: Set[Hashable] = set()
    # map[VertexID]struct{int, VertexID}
    distances: Mapping[Hashable, List[int, Hashable]] = dict()
    def dist_less_than(v_a: Hashable, v_b: Hashable) -> bool:
        d_a, d_b = distances[v_a][0], distances[v_b][0]
        if d_a == FAKE_INF and d_b == FAKE_INF:
            raise Exception("Can't compare psuedo `inf`(-1)s.")
        if d_a == FAKE_INF:
            return False
        if d_b == FAKE_INF:
            return True
        return d_a < d_b
    minqueue = MinHeap(dist_less_than)
    
    for v in graph.vertices.values():
        distances[v.ident] = [FAKE_INF, None]
    distances[src_id] = [0, src_id]
    
    minqueue.insert(src_id)
    visited.add(src_id)
    while not minqueue.is_empty():
        u_id: Hashable = minqueue.extract_min()
        # if u_id == dst_id: break
        # > If we just need a shortest path to a certain point, can we just
        #   break once we reach the point/vertex? Is the path at that time
        #   guarenteed to be the shortest path?
        u_dist, _ = distances[u_id]
        u: Vertex = graph.vertices[u_id]
        for v_id, edge in u.edges.items():
            v_dist = u_dist + edge.weight
            assert v_dist >= 0
            # If new distance less than old distance, do "relax".
            if distances[v_id][0] < 0 or v_dist < distances[v_id][0]:
                distances[v_id] = [v_dist, u_id]
                if not v_id in visited:
                    minqueue.insert(v_id)
                    visited.add(v_id)
                pass
            pass
        pass
    return distances

# dijkstra:
    # --- Done init
    # distances: Mapping[VertexID, int]
    # -- or Mapping[VertexID, Tuple[int, VertexID]], the second for 
    #    `source` vertex.
    # queue: Minqueue[VertexID]
    # > Put nodes into queue on its first update, avoiding finding them
    #   in heap array.
    # ---
    # init `distances` with ids and -1(as inf)
    # init distances[src] with 0
    # put src into queue
    # mark src as visited
    # while queue is not empty:
    #   u = minqueue.extract
    #   for v in u:
    #       d_u = distances[u.ident]
    #       --- do "relax"
    #       d_v = distances[u] + u.edges[v.ident].weight
    #       if d_v < distances[v]:
    #           distances[v] = d_v
    #           if not v_id in visited:
    #               minqueue.insert(v)
    #               visited.add(v_id)
