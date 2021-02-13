from typing import (
    List,
    Set,
    Mapping,
    Hashable,
    Callable
)

class MinHeap():
    INIT_SIZE = 32
    def __init__(
            self, less_than: Callable[[object, object], bool], *,
            arr: List[object]=None
        ):
        self.less_than = less_than
        self.arr: List = None
        if arr is None:
            self.arr: List[object] = [None for _ in range(self.INIT_SIZE)]
            self.count = 0
        else:
            self.arr = arr
            self.count = len(self.arr)
            # Then do heapify
        self.cap = len(self.arr)
        return
    # TODO: heapify, sift_up, sift_down, extract_min, insert
    def is_empty(self) -> bool:
        return self.count == 0
    
    def sift_up(self, idx: int):
        arr = self.arr
        while idx > 0:
            parent = (idx + 1) >> 1
            if self.less_than(arr[idx], arr[parent - 1]):
                parent -= 1
                tmp         = arr[idx]
                arr[idx]    = arr[parent]
                arr[parent] = tmp
                parent += 1
            idx = parent - 1
        return
    
    def sift_down(self, idx: int):
        bound = self.count #len(self.arr)
        max_idx = (bound >> 1) - 1
        arr = self.arr
        while idx <= max_idx:
            idx += 1
            i_l, i_r = idx << 1, (idx << 1) + 1
            idx -= 1
            swp = idx
            if i_l <= bound and self.less_than(arr[i_l - 1], arr[idx]):
                swp = i_l
            if i_r <= bound and self.less_than(arr[i_r - 1], arr[idx]) \
                and self.less_than(arr[i_r], arr[i_l]):
                swp = i_r
            if swp == idx:
                break
            swp -= 1
            tmp      = arr[idx]
            arr[idx] = arr[swp]
            arr[swp] = tmp
            idx = swp
        return
    
    def min_heapify(self):
        #arr = self.arr
        max_idx = (self.count >> 1) - 1 #(len(arr) >> 1) - 1
        for i in range(max_idx, -1, -1):
            self.sift_down(i)
        return
    
    def extract_min(self) -> object:
        if self.count <= 0:
            return None
        arr = self.arr
        res = arr[0]
        arr[0] = arr[self.count - 1]
        self.count -= 1
        #print(self.count, self.arr)
        self.sift_down(0)
        return res
    
    def insert(self, obj: object):
        idx = self.count
        self.count += 1
        if self.count > self.cap:
            self.arr.extend((None for i in range(len(self.arr))))
            self.cap = len(self.arr)
        self.arr[idx] = obj
        self.sift_up(idx)
        return
    pass


class Vertex():
    def __init__(self, ident: Hashable):
        # TODO: Add a `uf_node` member and implement `union-find` data struct.
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

    @classmethod
    def FromSpec(cls, spec: str):
        return

    def AddVertex(self, ident: Hashable) -> Vertex:
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
        #           minqueue.insert(v)
        #           visited.add(v_id)

if __name__ == '__main__':
    # --- test 2
    g = Graph()
    # TODO: add a `FromSpec` class method.
    # Auto generate graph for testing? Must ensure:
    #   - No self-linking
    #   - No repeated edges
    # --- vertices
    g.AddVertex("a")
    g.AddVertex("b")
    g.AddVertex("c")
    g.AddVertex("d")
    g.AddVertex("e")
    g.AddVertex("f")
    g.AddVertex("g")
    # --- edges
    g.AddEdge("a", "b", 32)
    g.AddEdge("a", "f", 3)
    g.AddEdge("b", "e", 12)
    g.AddEdge("b", "c", 21)
    g.AddEdge("b", "f", 7)
    g.AddEdge("c", "e", 6)
    g.AddEdge("c", "f", 2)
    g.AddEdge("c", "g", 11)
    g.AddEdge("d", "e", 13)
    g.AddEdge("d", "g", 9)

    res = shortest_path(g, "a", "g")
    print(res)