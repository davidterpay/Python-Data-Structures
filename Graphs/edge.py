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
        self.v1 = vertex1
        self.v1Pointer = vertex1Pointer
        self.v2 = vertex2
        self.v2Pointer = vertex2Pointer
        self.key = key
        self.visited = False
        self.discovery = False

    def __str__(self):
        return str([str(self.v1),str(self.v2),f'Key: {self.key}'])
    
