import sys
sys.path.append('../')
from Linked_List import LinkedList # Used in backend adjacency list impl.
from Stacks import Stack # Used in DFS traversal
from Queues import Queue # Used in BFS traversal
from Disjoint_Sets import disjointset # Used in minimum spanning trees
from Heaps import heap # Used in minimum spanning trees
from Graphs.edge import Edge
from Graphs.vertex import Vertex

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
incident edges runs in O(deg(v)) time. If a graph is sparse, we should use an adjacency list.

If you have a sparse graph, you should probably stick to an adjacency list or an edge list.
However, if you have a dense graph, you really have to be looking at what functionality you will
be using to determine which backend implementation to use.


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
        self.connectedComponents = 0
        self.cycles = False

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
        When we are removing a vertex, we have to ensure that we are also
        removing all of the edges that belong to the vertex. We do so 
        by finding the edge object in the linked list of edges, and
        removing both of the pointers in the edge object (corresponding to
        the two vertices belonging to the edge).
        INPUT:
            v: Vertex that we will remove
        OUTPUT:
            Removed vertex from graph

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
        '''
        This function takes in a node and the linked list the node is a part of,
        and swaps the head of the linked list with the node. This allows us to
        remove in constant time. 
        INPUT:
            node: Node in the linked list we are removing
            lnkdlst: Linked List that the node belongs to
        OUTPUT:
            Node being removed from the linked list.
        '''

        if node != lnkdlst.head:
            lnkdlst.swap(lnkdlst.head, node)
        lnkdlst.removeFront()

    def removeEdge(self, v1,v2):
        '''
        This function will remove an edge that has two associated
        vertices, v1 and v2. We first find the vertex with the smaller degree,
        next we traverse through the linked list of edge pointers stored in the
        key. Once we do that we check whether the actual edge object has pointers
        pointing to v1 and v2. If so we simply remove, if not, we do nothing and 
        keep traversing the linked list.
        INPUT:
            v1: First vertex
            v2: Second vertex
        OUTPUT:
            Removed edge associated with v1 and v2
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
                return
            elif self.__checkVertices(v2, v1, data.v1, data.v2):
                vertex1 = data.v1Pointer
                vertex2 = data.v2Pointer
                self.__removeElem(linked.getData(), self.edges)
                self.__removeElem(vertex2, self.vertices[v1])
                self.__removeElem(vertex1, self.vertices[v2])
                return
            linked = linked.getNext()

    def __checkVertices(self, v1, v2, vertex1, vertex2):
        '''
        This will return true if we have a match of the two vertices in the linked list
        of edges and the two inputed vertices.
        INPUT:
            v1: First vertex we are checking
            v2: Second vertex we are checking
            vertex1: Pointer stored in the edge object
            vertex2: Other pointer stored in the edge object
        OUTPUT:
            True if we have a match.
        '''

        return (v1 == vertex1 and v2 == vertex2)

    def inicidentEdges(self, v):
        '''
        This function will return all of the edges touching a inputed 
        vertex.
        INPUT:
            v: Vertex we are finding all of the inicident edge for
        OUTPUT:
            List of incident edges to a given vertex
        
        Runtime
        Implementation 1: O(1) + O(m)
        Implementation 2: O(n)
        Implementation 3: O(1) + O(deg(v))
        '''

        edges = list(map(lambda data: data.getData(), self.vertices[v].toList()))
        return edges

    def areAdjacent(self, v1,v2):
        '''
        This function checks if two vertices, v1 and v2, are adjacent.
        We do so by finding the degree of the smaller vertex, and then traversing
        through the linked list of edge pointers stored in the key. We check the edge
        that the edge is pointing to and check whether the pointers stored inside the 
        actual edge object point to v1 and v2. If so we return true.
        INPUT:
            v1: First vertex
            v2: Second vertex
        OUTPUT:
            Returns data if adjacent; None otherwise
        Runtime
        Implementation 1: O(m)
        Implementation 2: O(1)
        Implementation 3: O(1) + O(min(deg(v1), deg(v2)))
        '''

        smaller = v1 if self.degree(v1) <= self.degree(v2) else v2
        linked = self.vertices[smaller].head
        while linked:
            data = linked.getData().getData()
            if self.__checkVertices(v1, v2, data.v1, data.v2) or self.__checkVertices(v2, v1, data.v1, data.v2):
                return data
            linked = linked.getNext()
        return None
    
    def adjacentVertices(self, v):
        '''
        This function will return all of the adjacent vertices around a given vertex
        v. This function will be helpful when we are doing BFS and DFS traversals 
        of the graph.
        INPUT:
            v: Vertex query
        OUTPUT:
            List of adjacent vertices
        '''

        edges = self.inicidentEdges(v)
        verts = []
        for e in edges:
            if e.v1 == v:
                verts.append(e.v2)
            else:
                verts.append(e.v1)
        return verts

    def degree(self, key):
        '''
        This function returns the length of the set of incident edges to a given
        vertex.
        '''
    
        return len(self.vertices[key])

    def numConnectedComponents(self):
        '''
        This is returning the number of connected components in our graph.
        All this means is that we might have a disjoint graph where some nodes
        do not have a path between them. We keep track of this when we call traversals
        DFS or BFS. Make sure to call the traversal before calling this function.
        '''

        return self.connectedComponents

    def cyclesExist(self):
        '''
        This function is checking whether we have cycles in our graph. A cycle just means
        that we have the same starting and ending point in a given path that we take 
        in a graph. We keep track of this when we run the traversals. Make sure to run
        the traversals before calling this function because otherwise you wil not 
        get the result you want.
        '''

        return self.cycles

    def initialize(self):
        '''
        This function will initialize our vertices
        and edges so that we can properly traverse the entire graph
        '''

        for v in self.vertices.keys():
            v.setVisited(False)
        for e in self.edges.toList():
            e.visited = False
            e.discovery = False

    def bfs(self):
        '''
        A breadth first search works very similarly to a BFS in a 
        binary tree. First we visit all of the children of a node before
        visiting any of the grandchildren. In order to properly do the traversal,
        we must first set all of the vertices as not visited and label all of
        the edges as not visited as well. Once we do that we simply do a BFS on every single
        node in our vertex list given that we have not yet visited the vertex.
        '''

        self.initialize()
        for v in self.vertices.keys():
            if not v.getVisited():
                self.connectedComponents += 1
                self.__bfs(v)
    
    def __bfs(self, v):
        '''
        Once we initialize everything (set everything to unexplored), we need a queue
        to help us visit the locations we need. The algorithm looks like this
        1. Enqueue the first vertex
        2. Report on it
        3. While !q.isempty():
            1. Dequeue
            2. Report
            3. Loop through the adjacent vertices
                - Update the edges, mark the vertex as visited (if not yet visited); enqueue
                - If visited, check if edge has been visited, if not mark the edge as a cross edge
                    which means we have a cycle
        
        A BFS will give us the shortest path in terms of number of edges. But it has to be from the starting
        point to a final point cant be two points in between. In addition, the discovery edges that are made by
        the DFS produce a spanning tree. A cross edge in BFS will only change the distance from the root 
        by a maximum of one.

        Remember, graph traversals can have any order we want. It all depends on the
        starting point. 
        Runtime - O(n + m) - This runtime is a little tricky to derive but I will try my best.
        Since we have to enqueue every single vertex onto the queue at least once, we get O(n). However,
        since we also have to visit every single adjacent vertex to a given vertex, which is equal to
        def(v), we get 2m. We get 2m, by summing up all of the degrees of all of the nodes which we visit.
        This finally gives us a runtime of O(n + 2m) = O(m + n). This is a very good run time because
        we have to visit every single node and edge in this version of a breadth first search (traversal).
        '''

        queue = Queue.Queue()
        v.setVisited(True)
        queue.enque(v)
        print(v)
        while not queue.isEmpty():
            vert = queue.deque()
            for adjvert in self.adjacentVertices(vert):
                edge = self.areAdjacent(adjvert, vert)
                if not adjvert.getVisited():
                    print(adjvert)
                    adjvert.setVisited(True)
                    edge.visited = True
                    edge.discovery = True
                    queue.enque(adjvert)
                elif not edge.visited:
                    self.cycles = True
                    edge.visited = True
                    edge.discovery = False
    
    def dfs(self):
        '''
        A depth first search works very similarly to a DFS in a 
        binary tree. We want to visit as deep into the graph as possible. In order 
        to properly do the traversal, we must first set all of the vertices as not visited 
        and label all of the edges as not visited as well. Once we do that 
        we simply do a DFS on every single node in our vertex list given that we have 
        not yet visited the vertex.
        '''

        self.initialize()
        for v in self.vertices.keys():
            if not v.getVisited():
                self.connectedComponents += 1
                self.__dfs(v)
    
    def __dfs(self,v):
        '''
        Once we initialize everything (set everything to unexplored), we need a stack
        to help us visit the locations we need. The algorithm looks like this
        1. push the first vertex
        2. Report on it
        3. While !stack.isempty():
            1. pop
            2. Report
            3. Loop through the adjacent vertices
                - Update the edges, mark the vertex as visited (if not yet visited); push
                - If visited, check if edge has been visited, if not mark the edge as a back edge
                    which means we have a cycle

        Remember, graph traversals can have any order we want. It all depends on the
        starting point. In addition, a traversal will automatically create a minimum spanning tree.

        Runtime - O(n + m) - This runtime is a little tricky to derive but I will try my best.
        Since we have to push every single vertex onto the queue at least once, we get O(n). However,
        since we also have to visit every single adjacent vertex to a given vertex, which is equal to
        def(v), we get 2m. We get 2m, by summing up all of the degrees of all of the nodes which we visit.
        This finally gives us a runtime of O(n + 2m) = O(m + n). This is a very good run time because
        we have to visit every single node and edge in this version of a breadth first search (traversal).
        '''

        v.setVisited(True)
        stack = Stack.Stack()
        stack.push(v)
        print(v)
        while not stack.isEmpty():
            vert = stack.pop()
            for adjvert in self.adjacentVertices(vert):
                e = self.areAdjacent(vert, adjvert)
                if not adjvert.getVisited():
                    print(adjvert)
                    adjvert.setVisited(True)
                    e.visited = True
                    e.discovery = True
                    stack.push(adjvert)
                elif not e.visited:
                    self.cycles = True
                    e.visited = True
                    e.discovery = False
    
    def mstKruskal(self):
        # sort the edges (using build heap)
        # place all vertices in seperate disjoint sets
        # for each edge:
            # if vertices in edge are in seperate sets, union and make the edge a discovery edge
            # else make the edge not discovery but visited
        # forest = disjointset.DisjointSet() # building a forest of disjoint sets to hold our vertices
        # forest.insertelements([v for v in self.vertices.keys()])
        forest = disjointset.DisjointSet(self.vertices.keys())
        edgeWeights = heap.Heap() #priority queue for our impl. of sorting edges.
        edgeWeights.buildHeap(self.edges.toList())
        minimumSpanningTree = Graph()
        while len(minimumSpanningTree.edges) < n - 1:
            


    def mstPrim(self):
        pass
    
    def dijkstra(self):
        pass

    def floydWarshall(self):
        pass

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
g.insertVertex('A')
g.insertVertex('B')
g.insertVertex('C')
g.insertVertex('D')
g.insertVertex('E')
g.insertVertex('F')
g.insertVertex('G')
g.insertVertex('H')
g.insertVertex('I')
keys = list(g.vertices.keys())
g.insertEdge(keys[0], keys[1],'key')
g.insertEdge(keys[0], keys[2], 'key')
g.insertEdge(keys[0], keys[3], 'key')
g.insertEdge(keys[1], keys[2], 'key')
g.insertEdge(keys[1], keys[4], 'key')
g.insertEdge(keys[4], keys[2], 'key')
g.insertEdge(keys[4], keys[6], 'key')
g.insertEdge(keys[7], keys[6], 'key')
g.insertEdge(keys[7], keys[3], 'key')
g.insertEdge(keys[2], keys[3], 'key')
g.insertEdge(keys[5], keys[3], 'key')
g.insertEdge(keys[2], keys[5], 'key')
g.insertEdge(keys[5], keys[6], 'key')
print(g)
