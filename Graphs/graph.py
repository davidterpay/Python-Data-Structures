from vertex import Vertex
from edge import Edge
import sys
sys.path.append('../')
from Linked_List import LinkedList

'''
Written by David Terpay
So far we have seen data structures that fall into two basic categories:
    1. Array Based (cache - optimized)
        - Stacks, Queues, Heaps, Hashing, Disjoint Sets, Uptrees
    2. List/pointer Based
        - Linked lists (single and double), Binary trees, KDTrees, BTrees,
            AVL Trees
Graphs on the other hand utilize these structures to solve algorithms that we had
previously. Graphs are a set of vertices and edges. Vertices can be thought of as 
nodes. The magnitude of the set of vertices is n; the magnitude of the set of edges
is m. This will be important once we dive into runtime analysis. Inicident edges are
the set of edges that are touching a vertex. The degree of a vertex is equal to the
magnitude of set of inicident edges for that vertex. Adjacent vertices is the set of 
vertices that are directly connected to a vertex (by an edge). A path is a sequence 
of vertices connected by edges. A cycle is a path with the same start and end vertex.
A simple graph is a graph with no self loops (or edges pointing to itself) and no 
multiedges (no two edges go from two of the same vertices). A subgraph g is the subset 
of vertices and edges from set of vertices and edges G. This means that every vertex 
in the subgraph is in the graphs set of vertices, every edge is in the set of edges. 
The minimum number of edges in  a connected graph is n - 1. In a graph that is not 
connected, 0. The maximum number of edges in a a simple graph is proportional to n^2. 
The sum of the degrees of all vertices is equal to 2m. A complete subgraph is a 
graph in which every vertex is adjacent to every other vertex. A connected subgraph 
is a graph that has a path between any two vertices. A connected component is a connected 
subgraph where no nodes are connected to the rest of the graph. An acyclic graph has 
no cycles. Finally, a spanning tree is a connected acyclic 
subgraph with minimal edge weight. Since there are several implementations 
of graphs, I will cover only a few of them here.

Implementation 1: Edge List
In an graph we need to store two different things: vertices and edges. The idea here
is to keep the all of the vertices in some sort of hash table to ensure O(1) search 
and insertion and to keep all of edges in some sort of list (usually a linked list). 
Problem here is that runtime can become a bit problematic when doing things such as 
removing vertices, finding adajcent vertices or incident edges. For example, removing 
from a hash table will require O(1) time but removing all edges from the list of edges 
will require O(m) time. As previously mentioned, m can be proportional
to n ^ 2 and at this point we are not satisified with removing in quadratic time.

Implementation 2: Adjacency Matrix
The idea here is to keep all of the vertices in a hash table, and to hold a large 
n x n matrix that will store an edge object or nothing. This will allow us to determine 
whether two vertices are adjacent in O(1) time, will allow us to find all incident edges 
in O(n) time, and will allow us to insert a new node inamortized O(n) time. However, since 
half of the matrix will not be used, we can have a significant amount of space overhead. 
In addition, constructing a graph with a bunch of vertices takes O(n ^ 2) time sicne each 
insertion is amortized O(n) time. When you remove a vertex from the matrix you can either 
leave the hole in the matrixor you can swap it with the last index copy in O(n) time.

Implementation 3: Adjacency List
This is by far the most scary to implement. In an adjacency list we store the vertices in 
a hash table. However, with each vertex, we also keep a linked list of pointers to the 
edges that contain that vertex. The edges are stored as a linked list but each edge 
points back to the position of the edge as stored in the linked list in the vertex hash 
table. In short, this allows us to create a graph with given set of vertices and edges in 
O(n) time. Additionally, insertion runs in O(1) time, remove runs in O(1) + O(deg(v)) which is 
bound by O(n), are adjacent runs in the minimum of the degrees of the two vertices in question. Finally,
incident edges runs in O(deg(v)) time.


THIS CLASS WILL IMPLEMENT AN ADJACENCY LIST
'''

class Graph():
    def __init__(self):
        '''
        Our graph will keep track of a set of vertices and a linked list of edges as
        mentioned in the description of an adjacency list.

        Runtime
        Implementation 1: O(n)
        Implementation 2: O(n ^ 2)
        Implementation 3: O(n)
        '''

        self.vertices = {}
        self.edges = LinkedList.LinkedList()

    def insertVertex(self, key):
        '''
        Here all we do is create a new vertex object with the key parameter and insert it
        into our set of vertices. The reason we use a set is because it is implemented
        using a hashtable and allows us to have constant lookups.
        INPUT:
            key: Key or data we want to insert
        OUTPUT:
            Inserted vertex into our graph

        Runtime
        Implementation 1: O(1)
        Implementation 2: O(1) + O(n) amortized
        Implementation 3: O(1) ?
        '''

        vert = Vertex(key)
        self.vertices[vert] = LinkedList.LinkedList()

    def insertEdge(self, v1,v2,key):
        '''
        The idea here is to create a new edge and append an empty node
        to the linked list stored in the key of the vertices. Once you add
        a new node, you make the edge point back to the exact location of each of
        the vertices; likewise, we make the data within the node stored in the 
        linked list of inicident edges point directly to the edge as stored
        in the linked list of edges.
        INPUT:
            v1: Vertex 1 that will have a new edge
            v2: Vertex 2 that will have a new edge
            key: Key that will be stored in the edge
        OUTPUT:
            New edge
        
        Runtime
        Implementation 1: O(1)
        Implementation 2: O(1)
        Implementation 3: O(1)
        '''

        self.vertices[v1].addFront(None)
        self.vertices[v2].addFront(None)
        self.edges.addFront(None)
        edge1 = Edge(v1, v2, self.vertices[v1].head, self.vertices[v2].head, key)
        self.vertices[v1].head.setData(self.edges.head)
        self.vertices[v2].head.setData(self.edges.head)
        self.edges.head.setData(edge1)
        
    def removeVertex(self, v):
        '''
        Runtime
        Implementation 1: O(1) + O(m)
        Implementation 2: O(1) + (n)
        Implementation 3: O(1) + O(deg(v))
        '''

        while self.vertices[v].head:
            data = self.vertices[v].head.getData().getData()
            vertex1 = data.v1Pointer
            vertex2 = data.v2Pointer
            self.__removeElem(self.vertices[v].head.getData(), self.edges)
            self.__removeElem(vertex1, self.vertices[data.v1])
            self.__removeElem(vertex2, self.vertices[data.v2])
        self.vertices.pop(v)
            
    def __removeElem(self, node, lnkdlst):
        if node != lnkdlst.head:
            lnkdlst.swap(lnkdlst.head, node)
        lnkdlst.removeFront()

    def removeEdge(self, v1,v2):
        '''
        Runtime
        Implementation 1: O(1)
        Implementation 2: O(1)
        Implementation 3: O(1) + O(min(deg(v1),deg(v2)))
        '''
        smaller = v2 if self.degree(v1) >= self.degree(v2) else v1
        linked = self.vertices[smaller].head
        while linked:
            data = linked.getData().getData()
            if self.__checkVertices(v1, v2, data.v1, data.v2):
                vertex1 = data.v1Pointer
                vertex2 = data.v2Pointer
                self.__removeElem(linked.getData(), self.edges)
                self.__removeElem(vertex1, self.vertices[v1])
                self.__removeElem(vertex2, self.vertices[v2])
            elif self.__checkVertices(v2, v1, data.v1, data.v2):
                vertex1 = data.v1Pointer
                vertex2 = data.v2Pointer
                self.__removeElem(linked.getData(), self.edges)
                self.__removeElem(vertex2, self.vertices[v1])
                self.__removeElem(vertex1, self.vertices[v2])
            linked = linked.getNext()
        

    def __checkVertices(self, v1, v2, vertex1, vertex2):
        return (v1 == vertex1 and v2 == vertex2)

    def inicidentEdges(self, v):
        '''
        Runtime
        Implementation 1: O(1) + O(m)
        Implementation 2: O(n)
        Implementation 3: O(1) + O(deg(v))
        '''

        edges = list(map(lambda data: data.getData(), self.vertices[v].toList()))
        return edges

    def areAdjacent(self, v1,v2):
        '''
        Runtime
        Implementation 1: O(m)
        Implementation 2: O(1)
        Implementation 3: O(1) + O(min(deg(v1), deg(v2)))
        '''
        pass
    
    def degree(self, key):
        '''
        This function returns the length of the set of incident edges to a given
        vertex.
        '''
    
        return len(self.vertices[key])

    def __str__(self):
        '''
        String representation of our Graph
        '''

        string = ''
        for key, value in self.vertices.items():
            edgestring = ''
            edges = value.head
            if not edges:
                edgestring = '[]'
            while edges:
                edgestring += str(edges.getData().getData())
                edges = edges.getNext()
                if edges:
                    edgestring += ', '
            string += f'{key}\nEdges: {edgestring}\n\n'
        return string

g = Graph()
g.insertVertex(10)
g.insertVertex(30)
g.insertVertex(50)
keys = list(g.vertices.keys())
g.insertEdge(keys[0], keys[1], 'removal')
g.insertEdge(keys[2], keys[1], 'suppp')
print(g)
g.removeEdge(keys[0],keys[1])
print('\n\n')
print(g)
