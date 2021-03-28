import unittest

import pygraph

class TestMinimumSpanningTree(unittest.TestCase):
    def test_graph_fixed(self):
        g = pygraph.Graph()
        # --- vertices
        g.AddVertex('a')
        g.AddVertex('b')
        g.AddVertex('c')
        g.AddVertex('d')
        g.AddVertex('e')
        g.AddVertex('f')
        g.AddVertex('g')
        # --- edges
        g.AddEdge('a', 'b', 1)
        g.AddEdge('a', 'c', 8)
        g.AddEdge('a', 'e', 2)
        g.AddEdge('b', 'd', 6)
        g.AddEdge('c', 'd', 4)
        g.AddEdge('c', 'e', 3)
        g.AddEdge('d', 'f', 5)
        g.AddEdge('e', 'f', 9)
        g.AddEdge('e', 'g', 7)
        
        expected_g = pygraph.Graph()
        # --- vertices
        expected_g.AddVertex('a')
        expected_g.AddVertex('b')
        expected_g.AddVertex('c')
        expected_g.AddVertex('d')
        expected_g.AddVertex('e')
        expected_g.AddVertex('f')
        expected_g.AddVertex('g')
        # --- edges
        expected_g.AddEdge('a', 'b', 1)
        expected_g.AddEdge('a', 'e', 2)
        expected_g.AddEdge('c', 'e', 3)
        expected_g.AddEdge('c', 'd', 4)
        expected_g.AddEdge('d', 'f', 5)
        expected_g.AddEdge('e', 'g', 7)

        mst = pygraph.min_span_tree(g)
        # Do compare graph 'mst' and 'expected_g'
        self.assertEqual(expected_g, mst)

        return
    
    def test_auto_gen(self):
        g = pygraph.gen_graph(4096)
        mst = pygraph.min_span_tree(g)
        self.assertEqual(len(g.vertices), len(mst.vertices))
        self.assertEqual(len(mst.vertices) - 1, len(mst.edges))
        return
    pass