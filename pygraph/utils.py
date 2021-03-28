import random
import math

from .graph import (
    Graph,
    Vertex,
)


EDGES_LO = 1
EDGES_HI = 8
WEIGHT_LO = 1
WEIGHT_HI = 15


def gen_graph(
        n_vertices: int, *,
        edges_low: int=EDGES_LO, edges_high: int=EDGES_HI,
        weight_low: int=WEIGHT_LO, weight_high: int=WEIGHT_HI
    ) -> Graph:
    assert edges_low > 0 and edges_high >= edges_low
    assert weight_low > 0 and weight_high >= weight_low
    g = Graph()
    n_digit = math.ceil(math.log10(n_vertices))
    vertex_ids = [
        f"{i:0{n_digit}d}" for i in range(n_vertices)
    ]
    for v_id in vertex_ids:
        g.AddVertex(v_id)
    for v_id, vertex in g.vertices.items():
        # Choose vertices to link.
        rng_ids = {
            random.choice(vertex_ids)
            for _ in range(random.randint(edges_low, edges_high))
        }
        # Ensure vertices are not self-linked.
        rng_ids.discard(v_id)
        for r_id in rng_ids:
            # Ensure vertices are not doubly-linked.
            if r_id in vertex.edges.keys():
                continue
            g.AddEdge(v_id, r_id, random.randint(weight_low, weight_high))
        pass
    return g