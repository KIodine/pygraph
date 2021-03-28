import unittest

import pygraph


class TestGraphBasic(unittest.TestCase):
    def test_linking(self):
        g = pygraph.Graph()
        g.AddVertex("a")
        g.AddVertex("b")
        g.AddEdge("a", "b", 10)
        vert_a = g.vertices["a"]
        vert_b = g.vertices["b"]
        self.assertTrue(vert_a.edges["b"] == vert_b.edges["a"])
        return
    
    def test_graph_equal(self):
        g_a = pygraph.Graph()
        g_b = pygraph.Graph()
        # setup 'g_a'
        g_a.AddVertex('a')
        g_a.AddVertex('b')
        g_a.AddEdge('a', 'b', 3)
        # setup 'g_b'
        g_b.AddVertex('a')
        g_b.AddVertex('b')
        g_b.AddEdge('a', 'b', 3)
        self.assertEqual(g_a, g_b)

        with self.assertRaises(pygraph.GraphException):
            _ = g_a == True

        g_b.AddVertex('c')
        g_b.AddEdge('b', 'c', 3)
        self.assertNotEqual(g_a, g_b)

        g_a.AddVertex('c')
        self.assertNotEqual(g_a, g_b)

        g_a.AddEdge('b', 'c', 4)
        self.assertNotEqual(g_a, g_b)

        return

    # def test_graph_copy(self):
    pass
