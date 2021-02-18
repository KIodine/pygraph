import unittest

from pygraph.prim import min_span_tree
import pygraph


class TestPrimMST(unittest.TestCase):
    def test_fixed(self):
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
        
        mst_prim = min_span_tree(g)
        mst_kruskal = pygraph.min_span_tree(g)
        #print(mst)
        self.assertEqual(expected_g, mst_prim)
        self.assertEqual(mst_kruskal, mst_prim)
        
        return
    
    def test_fixed_2(self):
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
        g.AddEdge('a', 'b', 12)
        g.AddEdge('a', 'c', 8)
        g.AddEdge('a', 'd', 13)
        g.AddEdge('b', 'c', 21)
        g.AddEdge('b', 'e', 32)
        g.AddEdge('b', 'f', 7)
        g.AddEdge('c', 'f', 2)
        g.AddEdge('d', 'g', 9)

        g_expected = pygraph.Graph()
        # --- vertices
        g_expected.AddVertex('a')
        g_expected.AddVertex('b')
        g_expected.AddVertex('c')
        g_expected.AddVertex('d')
        g_expected.AddVertex('e')
        g_expected.AddVertex('f')
        g_expected.AddVertex('g')
        # --- edges
        g_expected.AddEdge('a', 'c', 8)
        g_expected.AddEdge('a', 'd', 13)
        g_expected.AddEdge('b', 'e', 32)
        g_expected.AddEdge('b', 'f', 7)
        g_expected.AddEdge('c', 'f', 2)
        g_expected.AddEdge('d', 'g', 9)

        mst_prim = min_span_tree(g)
        mst_kruskal = pygraph.min_span_tree(g)
        
        self.assertEqual(mst_prim, g_expected)
        self.assertEqual(mst_prim, mst_kruskal)

        return

    def test_auto_gen(self):
        g = pygraph.gen_graph(4096)
        mst_kruskal = pygraph.min_span_tree(g)
        mst_prim = min_span_tree(g)
        
        self.assertEqual(len(g.vertices), len(mst_kruskal.vertices))
        self.assertEqual(len(mst_kruskal.vertices) - 1, len(mst_kruskal.edges))

        self.assertEqual(len(g.vertices), len(mst_prim.vertices))
        self.assertEqual(len(mst_prim.vertices) - 1, len(mst_prim.edges))
        
        prim_sum = 0
        for v in mst_prim.vertices.values():
            for e in v.edges.values():
                prim_sum += e.weight
            pass

        kruskal_sum = 0
        for v in mst_kruskal.vertices.values():
            for e in v.edges.values():
                kruskal_sum += e.weight
            pass
        
        # The graph might be slighly different with edges have the same weight,
        # but the sum of weight must be the same.
        self.assertEqual(kruskal_sum, prim_sum)
        
        return
    pass

