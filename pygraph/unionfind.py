

# Better name?
class UFNode():
    """Node structure include necessary information of algorithm."""
    def __init__(self):
        self.parent = self
        self.rank = 0
        self.count = 1 # The node itself.
    
    def reset(self):
        self.parent = self
        self.rank = 0
        self.count = 1
        return
    pass

def find(node: UFNode):
    """Find the root of given node."""
    # TODO: Find out does this approach iterate through
    #   every node in a chain?
    while node.parent != node:
        parent = node.parent
        # Find with "path halving".
        node.parent = parent.parent
        node = parent
    return node

def is_connected(a: UFNode, b: UFNode) -> bool:
    """Test are two nodes in the same set."""
    a = find(a)
    b = find(b)
    return a == b

def union(a: UFNode, b: UFNode) -> UFNode:
    """Unite a and b as same set."""
    # a and b are now the root of their kind.
    a = find(a)
    b = find(b)
    if a == b:
        return a
    if b.rank > a.rank:
        # swap them
        a, b = b, a
    a.count += b.count
    a.rank += 1
    b.parent = a
    return a