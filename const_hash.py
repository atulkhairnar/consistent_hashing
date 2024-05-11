import hashlib
from sortedcontainers import SortedList
import bisect

class HashRing:
    def __init__(self):
        self.nodes = SortedList()
        self.ring = {}
    
    def add_node(self, node):
        node_hash = hashlib.md5(node.encode()).hexdigest()
        if node_hash in self.nodes:
            print("Node is already added to ring.")
            return
        self.ring[node_hash] = node
        self.nodes.add(node_hash)

    def get_node(self, key):
        key_hash = hashlib.md5(key.encode()).hexdigest()
        position = bisect.bisect(self.nodes, key_hash) % len(self.nodes)
        return self.ring[self.nodes[position]]

    def remove_node(self, node):
        pass

if __name__ == "__main__":
    hr = HashRing()
    hr.add_node('a')
    hr.add_node('b')
    hr.add_node('c')
    for key in ('pune', 'kolkata', 'd', 'e', 'mumbai', 'chennai', 'nagpur', 'goa', 'kashmir', 'japan', 'maldives'):
        print(hr.get_node(key))

