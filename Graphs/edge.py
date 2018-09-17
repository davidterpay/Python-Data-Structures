'''
Written by David Terpay
This is a class that will help structure our edges. Edges
contain a few data items
1. Two vertices
2. Key
3. Pointers to the position of the item in the linked list of 
    edges stored in the vertex edge list.
'''
class Edge():
    def __init__(self, vertex1, vertex2, key):
        self.v1 = vertex1
        self.v2 = vertex2
        self.key = key
    def __str__(self):
        return str([str(self.v1),str(self.v2),f'Key: {self.key}'])
    