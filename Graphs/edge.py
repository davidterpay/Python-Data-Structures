'''
Written by David Terpay
This is a class that will help structure our edges. Edges
contain a few data items
1. Two vertices
2. Key
3. Pointers to the position of the item in the linked list of 
    edges stored in the vertex edge list.
4. Visited which will allow us to keep track of the edges we visited
    when we are doing traversals
5. Discovery will allow us to label the edges as we are traversing the 
    graph.
'''
class Edge():
    def __init__(self, vertex1, vertex2, vertex1Pointer, vertex2Pointer, key):
        self.origin = vertex1
        self.v1Pointer = vertex1Pointer
        self.destination = vertex2
        self.v2Pointer = vertex2Pointer
        self.key = key
        self.visited = False
        self.discovery = False
        self.weight = 0
    
    def __lt__(self, other):
        return self.weight < other.weight
    
    def __gt__(self, other):
        return self.weight > other.weight

    def __str__(self):
        return str([str(self.origin), str(self.destination), f'Key: {self.key}', f'Visited: {self.visited}', f'Discovery: {self.discovery}', f'Weight: {self.weight}'])
    
