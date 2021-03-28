from typing import (
    Hashable,
    Set,
    Mapping,
    List
)

from .graph import (
    Vertex,
    Edge,
    Graph,
    MinHeap,
)


# dijkstra:
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
# ---

# Finding shortest path using Dijkstra's algorithm.
def shortest_path(graph: Graph, src_id: Hashable, dst_id: Hashable):
    FAKE_INF = -1
    # Ensure no vertex is enqueued twice.
    # * `union-find` can add and check existence very fast, but cannot
    #   remove.
    visited: Set[Hashable] = set()
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
        # > Uncomment line below of want only the path to dst.
        # if u_id == dst_id: break
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