import unittest

import pygraph


class TestShortestPath(unittest.TestCase):
    def test_graph_a(self):
        g = pygraph.Graph()
        expected = {
            'a': [0, 'a'],
            'b': [2, 'a'],
            'c': [3, 'b'],
            'd': [6, 'a'],
            'e': [8, 'd']
        }
        # --- vertices
        g.AddVertex("a")
        g.AddVertex("b")
        g.AddVertex("c")
        g.AddVertex("d")
        g.AddVertex("e")
        # --- edges
        g.AddEdge("a", "b", 2)
        g.AddEdge("a", "c", 13)
        g.AddEdge("b", "c", 1)
        g.AddEdge("d", "a", 6)
        g.AddEdge("d", "e", 2)
        
        res = pygraph.shortest_path(g, "a", "c")
        
        self.assertEqual(res, expected)
        return
    
    def test_graph_b(self):
        g = pygraph.Graph()
        expected = {
            'a': [0, 'a'],
            'b': [10, 'f'],
            'c': [5, 'f'],
            'd': [24, 'e'],
            'e': [11, 'c'],
            'f': [3, 'a'],
            'g': [16, 'c']
        }
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

        res = pygraph.shortest_path(g, "a", "g")

        self.assertEqual(res, expected)
        return
    
    def test_random_graph(self):
        FAKE_INF = -1
        N_VERTICES = 8192
        
        g   = pygraph.gen_graph(N_VERTICES)
        res = pygraph.shortest_path(g, "0000", "0001")
        
        self.assertEqual(len(res), len(g.vertices))
        # Ensure all nodes got updated.
        self.assertTrue(
            all(
                map(lambda tp: tp[0] != FAKE_INF and not tp[1] is None, res)
            )
        )
        return
    pass
