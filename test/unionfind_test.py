import unittest

import pygraph

class TestUnionFind(unittest.TestCase):
    def test_basic(self):
        a = pygraph.UFNode()
        b = pygraph.UFNode()
        pygraph.union(a, b)
        self.assertTrue(pygraph.is_connected(a, b))
        return

    def test_complex(self):
        N_NODES = 1024
        
        nodes_a = [pygraph.UFNode() for _ in range(N_NODES)]
        nodes_b = [pygraph.UFNode() for _ in range(N_NODES)]
        root_a = nodes_a[0]
        root_b = nodes_b[0]

        for i, n in enumerate(nodes_a):
            pygraph.union(root_a, n)
            # Unite one node at a time.
            self.assertTrue(
                pygraph.is_connected(root_a, n)
            )
            # Ensure no other nodes are united.
            self.assertFalse(
                any(map(lambda n: pygraph.is_connected(root_a, n), nodes_a[i+1:]))
            )
        
        for n in nodes_b:
            pygraph.union(root_b, n)
        # Ensure nodes in 'nodes_b' are united.
        self.assertTrue(
            all(map(lambda n: pygraph.is_connected(root_b, n), nodes_b))
        )
        
        # Unite two sets.
        pygraph.union(root_a, root_b)
        # Ensure two sets are united.
        self.assertTrue(pygraph.is_connected(root_b, root_b))
        # Ensure each node are united against the opposite set.
        self.assertTrue(
            all(map(lambda n: pygraph.is_connected(root_a, n), nodes_b))
        )
        self.assertTrue(
            all(map(lambda n: pygraph.is_connected(root_b, n), nodes_a))
        )

        return
    pass
