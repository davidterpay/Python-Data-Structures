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
A simple graph is a graph with no self loops (or edges pointing to itself) and no multiedges
(no two edges go from two of the same vertices). A subgraph g is the subset of vertices and
edges from set of vertices and edges G. This means that every vertex in the subgraph is in 
the graphs set of vertices, every edge is in the set of edges. The minimum number of edges in 
a connected graph is n - 1. In a graph that is not connected, 0. The maximum number of edges
in a a simple graph is proportional to n^2. The sum of the degrees of all vertices 
is equal to 2m. A complete subgraph is a graph in which every vertex is adjacent to every other
vertex. A connected subgraph is a graph that has a path between any two vertices. A 
connected component is a connected subgraph where no nodes are connected to the rest
of the graph. An acyclic graph has no cycles. Finally, a spanning tree is a connected acyclic 
subgraph with minimal edge weight.
Since there are several implementations of graphs, I will cover only a few of them here.

Implementation 1: Edge List
In an graph we need to store two different things: vertices and edges. The idea here
is to keep the all of the vertices in some sort of hash table to ensure O(1) search and insertion
and to keep all of edges in some sort of list (usually a linked list). Problem here is that
runtime can become a bit problematic when doing things such as removing vertices, finding adajcent 
vertices or incident edges. For example, removing from a hash table will require O(1) time but removing
all edges from the list of edges will require O(m) time. As previously mentioned, m can be proportional
to n ^ 2 and at this point we are not satisified with removing in quadratic time.

Implementation 2: Adjacency Matrix
The idea here is to keep all of the vertices in a hash table, and to hold a large n x n matrix that will
store an edge object or nothing. This will allow us to determine whether two vertices are adjacent in O(1)
time, will allow us to find all incident edges in O(n) time, and will allow us to insert a new node in
amortized O(n) time. However, since half of the matrix will not be used, we can have a significant amount
of overhead. In addition, constructing a graph with a bunch of vertices takes O(n ^ 2) time sicne each insertion 
is amortized O(n) time. When you remove a vertex from the matrix you can either leave the hole in the matrix
or you can swap it with the last index copy in O(n) time.

Implementation 3: Adjacency List
'''
class Graph():
    def __init__(self, *args, **kwargs):
        '''
        Runtime
        Implementation 1: O(n)
        Implementation 2: O(n ^ 2)
        Implementation 3: O(1) ?
        '''
        pass
    def insertVertex(self, key):
        '''
        Runtime
        Implementation 1: O(1)
        Implementation 2: O(1) + O(n) amortized
        Implementation 3: O(1) ?
        '''
        pass
    def insertEdge(self, v1,v2,key):
        '''
        Runtime
        Implementation 1: O(1)
        Implementation 2: O(1)
        Implementation 3: O(1) ?
        '''
        pass
    def removeVertex(self, v):
        '''
        Runtime
        Implementation 1: O(1) + O(m)
        Implementation 2: O(1) + (n)
        Implementation 3: O(1)
        '''
        pass
    def removeEdge(self, v1,v2):
        '''
        Runtime
        Implementation 1: O(1)
        Implementation 2: O(1)
        Implementation 3: O(1)
        '''
        pass
    def inicidentEdges(self, v):
        '''
        Runtime
        Implementation 1: O(1) + O(m)
        Implementation 2: O(n)
        Implementation 3: O(1)
        '''
        pass
    def areAdjacent(self, v1,v2):
        '''
        Runtime
        Implementation 1: O(m) 
        Implementation 2: O(1)
        Implementation 3: O(1)
        '''
        pass
