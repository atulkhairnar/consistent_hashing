import hashlib
from sortedcontainers import SortedList
import bisect

class HashRing:
    def __init__(self):
        self.nodes = SortedList()
        self.ring = {}
        
    
    @staticmethod
    def get_hash(key):
        # generate md5 hash of any key string
        return hashlib.md5(key.encode()).hexdigest()

    def add_node(self, node):
        '''
        Add node to hashring
        '''
        node_hash = HashRing.get_hash(node)
        if node_hash in self.nodes:
            print("Node is already added to ring.")
            return
        self.ring[node_hash] = node
        self.nodes.add(node_hash)

    def get_node(self, key):
        '''
        Given the key find the node to which it should belong to. 
        '''
        # if no host added to ring, return -1
        if not self.nodes:
            return -1
        key_hash = HashRing.get_hash(key)
        position = bisect.bisect(self.nodes, key_hash) % len(self.nodes)
        return self.ring[self.nodes[position]]

    def remove_node(self, node):
        '''
        If any node x is to be removed, return the node to which keys from x relocated to
        '''
        node_hash = HashRing.get_hash(node)
        
        # return -1 if node does not exist on the ring
        if node_hash not in self.nodes:
            print("Node {} not found in the ring".format(node))
            return -1
        # if only one host is remaining, raise warning
        if len(self.nodes) == 1:
            print("There is only one host present in the ring. Keys can't be relocated")
            return -1

        index = bisect.bisect(self.nodes, node_hash) % len(self.nodes)
        next_node_name = self.ring[self.nodes[index]]
        # remove nodes from nodelist and ring dict
        self.nodes.remove(node_hash)
        del self.ring[node_hash]
        # returns the next hosts for data migration
        return next_node_name
        


if __name__ == "__main__":
    hr = HashRing()
    for node in 'abcd':
        hr.add_node(node)
    for key in ('pune', 'kolkata', 'd', 'e', 'mumbai', 'chennai', 'nagpur', 'goa', 'kashmir', 'japan', 'maldives'):
        print(hr.get_node(key))
    for node in ('d', 'a'):
        print(hr.remove_node(node))
