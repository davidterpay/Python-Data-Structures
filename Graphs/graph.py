from edge import Edge
from vertex import Vertex
import sys
sys.path.append('../')
from Linked_List import LinkedList # Used in backend adjacency list impl.
from Stacks import Stack # Used in DFS traversal
from Queues import Queue # Used in BFS traversal
from Disjoint_Sets import disjointset # Used in minimum spanning trees
from Heaps import heap # Used in minimum spanning trees
import math

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


NOTE: THIS CLASS WILL IMPLEMENT AN ADJACENCY LIST
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
    
    def __createdVertexInsertion(self, v):
        '''
        This is a helper function to simply inserted a given vertex into a 
        hash table of existing vertices
        INPUT:
            v: Vertex that we are inserting
        OUTPUT:
            Graph with a new given vertex
        '''

        self.vertices[v] = LinkedList.LinkedList()

    def insertEdge(self, origin, destination, key, weight = 0):
        '''
        The idea here is to create a new edge and append an empty node
        to the linked list stored in the key of the vertices. Once you add
        a new node, you make the edge point back to the exact location of each of
        the vertices; likewise, we make the data within the node stored in the 
        linked list of inicident edges point directly to the edge as stored
        in the linked list of edges.
        INPUT:
            origin: Vertex 1 that will have a new edge
            destination: Vertex 2 that will have a new edge
            key: Key that will be stored in the edge
        OUTPUT:
            New edge
        
        Runtime
        Implementation 1: O(1)
        Implementation 2: O(1)
        Implementation 3: O(1)
        '''

        self.vertices[origin].addFront(None)
        self.vertices[destination].addFront(None)
        self.edges.addFront(None)
        edge1 = Edge(origin, destination, self.vertices[origin].head, self.vertices[destination].head, key)
        self.vertices[origin].head.setData(self.edges.head)
        self.vertices[destination].head.setData(self.edges.head)
        edge1.weight = weight
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
            self.__removeElem(vertex1, self.vertices[data.origin])
            self.__removeElem(vertex2, self.vertices[data.destination])
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

    def removeEdge(self, origin,destination):
        '''
        This function will remove an edge that has two associated
        vertices, origin and destination. We first find the vertex with the smaller degree,
        next we traverse through the linked list of edge pointers stored in the
        key. Once we do that we check whether the actual edge object has pointers
        pointing to origin and destination. If so we simply remove, if not, we do nothing and 
        keep traversing the linked list.
        INPUT:
            origin: First vertex
            destination: Second vertex
        OUTPUT:
            Removed edge associated with origin and destination
        Runtime
        Implementation 1: O(1)
        Implementation 2: O(1)
        Implementation 3: O(1) + O(min(deg(origin),deg(destination)))
        '''

        smaller = destination if self.degree(origin) >= self.degree(destination) else origin
        linked = self.vertices[smaller].head
        while linked:
            data = linked.getData().getData()
            if self.__checkVertices(origin, destination, data.origin, data.destination):
                vertex1 = data.v1Pointer
                vertex2 = data.v2Pointer
                self.__removeElem(linked.getData(), self.edges)
                self.__removeElem(vertex1, self.vertices[origin])
                self.__removeElem(vertex2, self.vertices[destination])
                return
            elif self.__checkVertices(destination, origin, data.origin, data.destination):
                vertex1 = data.v1Pointer
                vertex2 = data.v2Pointer
                self.__removeElem(linked.getData(), self.edges)
                self.__removeElem(vertex2, self.vertices[origin])
                self.__removeElem(vertex1, self.vertices[destination])
                return
            linked = linked.getNext()

    def __checkVertices(self, origin, destination, vertex1, vertex2):
        '''
        This will return true if we have a match of the two vertices in the linked list
        of edges and the two inputed vertices.
        INPUT:
            origin: First vertex we are checking
            destination: Second vertex we are checking
            vertex1: Pointer stored in the edge object
            vertex2: Other pointer stored in the edge object
        OUTPUT:
            True if we have a match.
        '''

        return (origin == vertex1 and destination == vertex2)

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

    def areAdjacent(self, origin,destination):
        '''
        This function checks if two vertices, origin and destination, are adjacent.
        We do so by finding the degree of the smaller vertex, and then traversing
        through the linked list of edge pointers stored in the key. We check the edge
        that the edge is pointing to and check whether the pointers stored inside the 
        actual edge object point to origin and destination. If so we return true.
        INPUT:
            origin: First vertex
            destination: Second vertex
        OUTPUT:
            Returns data if adjacent; None otherwise
        Runtime
        Implementation 1: O(m)
        Implementation 2: O(1)
        Implementation 3: O(1) + O(min(deg(origin), deg(destination)))
        '''

        smaller = origin if self.degree(origin) <= self.degree(destination) else destination
        linked = self.vertices[smaller].head
        while linked:
            data = linked.getData().getData()
            if self.__checkVertices(origin, destination, data.origin, data.destination) or self.__checkVertices(destination, origin, data.origin, data.destination):
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
            if e.origin == v:
                verts.append(e.destination)
            else:
                verts.append(e.origin)
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
        '''
        Before we talk about the algorithm, lets touch base on what a MST exactly is once again. A
        minimum spanning tree (MST) is a graph that is minimally connected. This means that we 
        have created a path between any two nodes in our graph, have no cycles, and have a minimum
        total weight. In order to build a MST using Kruskal's algorithm, we first put each vertex in 
        a seperate set in a disjoint set. The purpose we do this is to check whether two vertices have
        the same representative element. If they do, that means they are part of some minimum spanning 
        tree for that labeled set. Next, we place all of the edges in a heap and build a minheap based
        on the edge weights. This will allow for us to properly remove each edge and to have the
        edges in correct order in linear time (build heap runs in O(n) time). Finally, we create a new
        graph which will be the minimum spanning tree.
        Once we do all of this we follow this algorithm:
        # while edges < n - 1:
            # for each edge:
                # if vertices in edge are in seperate sets, union and make the edge a discovery edge
                # else make the edge not discovery but visited
        
        Runtime - O(n + mlg(n)) - Since it takes O(n) time to build the disjoint set, O(m) time to 
        build a minheap(partially sorted), O(m) time to loop through the while loop since we might have
        to visit every edge, and finally O(lg(m)) = o(lg(n)) time to remove from a heap, we get a total runtime
        of O(n + mlg(n)). The runtime of implementing this algorithm using a sorted array is the same runtime.
        However, a minheap allows you to update edge weights with less of a cost and works better with a dense 
        graph.
        '''

        minimumSpanningTree = Graph()
        forest = disjointset.DisjointSet(self.vertices.keys())
        edgeWeights = heap.Heap() # priority queue for our impl. of sorting edges.
        edgeWeights.buildHeap(self.edges.toList())

        while len(minimumSpanningTree.edges) < (len(self.vertices.keys()) - 1):
            edge = edgeWeights.remove()
            index1 = index2 = 0
            # Room for optimization

            for index, value in enumerate(forest.array):
                if value.data == edge.origin:
                    index1 = index
                elif value.data == edge.destination:
                    index2 = index

            if forest.find(index1) != forest.find(index2):
                forest.union(index1, index2)
                if not edge.origin in minimumSpanningTree.vertices.keys():
                    minimumSpanningTree.__createdVertexInsertion(edge.origin)
                if not edge.destination in minimumSpanningTree.vertices.keys():
                    minimumSpanningTree.__createdVertexInsertion(edge.destination)

                minimumSpanningTree.insertEdge(edge.origin, edge.destination, edge.key, edge.weight)

        return minimumSpanningTree

    def mstPrim(self, v):
        '''
        Before we talk about the algorithm, lets touch base on what a MST exactly is once again. A
        minimum spanning tree (MST) is a graph that is minimally connected. This means that we 
        have created a path between any two nodes in our graph, have no cycles, and have a minimum
        total weight. In order to build a MST using Prim's algorithm, we first give each vertex a weight
        and a predecessor. Once we do this, we set the predecessor and weight in each vertex to be
        none and +inf respectively. In Prim's algorithm, we need to have a starting vertex. We set the
        weight of the starting vertex to 0. We then build a minheap to hold all of our vertices. We
        also create a new graph object that will end up being our MST. Finally, here we start our 
        algorithm. 
        for each vertex in vertices:
            min = queue.remove()
            if predecessor:
                Mst.addedge(vertex,predecessor)
            for neighbor of vertex not in new graph:
                if current_weight > weight_of_edge_connecting_vertex_neighbor:
                    neighbor.weight = weight_of_edge_connecting_vertex_neighbor
                    neighbor.predecessor = vertex

        Runtime - O(n + mlg(n)) - We know that 'initializing' each of the vertices takes O(n) time.
        Next, building a minHeap takes O(n) time. Once we enter the for loop and traverse all of the 
        vertices, we have an outer runtime of O(n). On the inside of the for loop, we remove from
        the minheap which takes O(lg(n)) time since we might have to heapify down.
        So that small portion gives us a runtime of nlg(n). The other portion inside
        of the for loop runs in time proportional to mlg(n) since we visit m edges, and 
        building the heap again takes lg(n) time. Once we add these up, we get a total
        runtime of O(mlg(n) + nlg(n)). Other implementations will get you better runtimes depending on
        what you want from the graph and the type of graph you are expecting. Using a adjacency list and
        minheap, we get this runtime. Using a adjacency matrix and a heap we also get the same runtime.
        However, if we swapped the heap for an unsorted array, we get a runtime of O(n^2) for both
        implementations of a graph. The best way to truely improve the runtime is to use a fibonacci heap,
        this would reduce total runtime to O(nlg(n) + m).
        '''

        for v in self.vertices.keys():
            v.predecessor = None
            v.weight = math.inf

        v.weight = 0
        priorityQueue = heap.Heap()
        priorityQueue.buildHeap(self.vertices.keys())
        minimumSpanningTree = Graph()

        for __ in range(len(self.vertices)):
            e = priorityQueue.remove()
            minimumSpanningTree.__createdVertexInsertion(e)
            if e.predecessor:
                key = self.areAdjacent(e, e.predecessor).key
                minimumSpanningTree.insertEdge(e, e.predecessor, key, e.weight)
            for neighbor in self.adjacentVertices(e):
                if not neighbor in minimumSpanningTree.vertices.keys():
                    weight = self.areAdjacent(neighbor, e).weight
                    if weight < neighbor.weight:
                        neighbor.weight = weight
                        neighbor.predecessor = e
                        priorityQueue.buildHeap()
        return minimumSpanningTree
    
    def dijkstra(self, start):
        '''
        Dijkstra's algorithm builds off of Prim's algorithm. The objective of Dijkstra's algorithm is
        to find the shortest path between a starting node and a destination node. However, at
        the end of running Dijkstra's algorithm, we find that we have the shortest path to 
        every other single vertex in our graph. When I am throwing around the word shortest path, I am
        referencing the smallest total edge weight path. Dijkstra's algorithm only changes one thing
        from Prim's algorithm: instead of updating the weight to be edge weight, we total up 
        the total distance or edge weight we have seen so far and add it to the vertex's weight. 
        Dijkstra's algorithm is very useful because it handles both directed and undirected graphs. In
        addition, Dijkstra's algorithm accounts will make the correct call when deciding between
        many small weighted edges and one large weighted edge. One downside of Dijkstra's algorithm
        is that it cannot handle neight weight cycles. Finally, if we are trying to find the path
        from start to finish, we start with the destination node and work backwards using each 
        node's predecessor.

        INPUT:
            start: Starting node we are finding
        OUTPUT:
            Shortest path to every single vertex in our graph from the starting point
        
        Runtime - O(n + mlg(n)) - We know that 'initializing' each of the vertices takes O(n) time.
        Next, building a minHeap takes O(n) time. Once we enter the for loop and traverse all of the 
        vertices, we have an outer runtime of O(n). On the inside of the for loop, we remove from
        the minheap which takes O(lg(n)) time since we might have to heapify down.
        So that small portion gives us a runtime of nlg(n). The other portion inside
        of the for loop runs in time proportional to mlg(n) since we visit m edges, and 
        building the heap again takes lg(n) time. Once we add these up, we get a total
        runtime of O(mlg(n) + nlg(n)). Other implementations will get you better runtimes depending on
        what you want from the graph and the type of graph you are expecting. Using a adjacency list and
        minheap, we get this runtime. Using a adjacency matrix and a heap we also get the same runtime.
        However, if we swapped the heap for an unsorted array, we get a runtime of O(n^2) for both
        implementations of a graph. The best way to truely improve the runtime is to use a fibonacci heap,
        this would reduce total runtime to O(nlg(n) + m).
        '''

        for v in self.vertices.keys():
            v.weight = math.inf
            v.predecessor = None
        v.weight = 0
        priorityQueue = heap.Heap() # heap to store our vertices
        priorityQueue.buildHeap(self.vertices.keys())
        sssp = Graph() # Single source shortest path (Dijkstras)
        for __ in range(len(self.vertices.keys())):
            vert = priorityQueue.remove()
            sssp.__createdVertexInsertion(vert)
            if vert.predecessor:
                e = self.areAdjacent(vert.predecessor, vert)
                key = e.key
                weight = e.weight
                sssp.insertEdge(vert.predecessor, vert, key, weight)
            # Can add additional code to account for directed graphs.
            for adjvert in self.adjacentVertices(vert):
                if adjvert not in sssp.vertices.keys():
                    existing_weight = self.areAdjacent(adjvert, vert).weight + vert.weight
                    if existing_weight < adjvert.weight:
                        adjvert.weight = existing_weight
                        adjvert.predecessor = vert
                        priorityQueue.buildHeap()
        return sssp

    def floydWarshall(self):
        '''
        Since Dijkstra's algorithm cannot account for negative edge weights, we need
        an alternative algorithm that will run properly if we do need negative edge weights.
        This algorithm is known as the Floyd Warshall Algorithm. The premise behind it is
        to assign each of the edges between each vertice +inf to start off. Once we find 
        a path that is shorter, we change the edge weight to the correct weight.
        Since this algorithm does require a adjacency matrix implementation if we want to use
        dynamic programming, we cannot implment it here. However, I will give a run through
        of the algorithm that we would use. This algorithm will give us the shortest path
        between any two vertices. Unlike Dijkstra's, we will have every single shortest path.
        Floyd Warshall's algo checks whether the inclusion of certain eedges is better than the existing
        path. It ignores adding an edge that already exists in our edge inputs. This helps us avoid 
        cycles and self loops. After the first w for loop, we know that all paths are optimal with
        the addition of k. Floyd Warshall's algorithm is a dynamic programming algo.

        Runtime - O(n ^ 3) - Since we do have to visit every single vertex, our runtime is O(n * n * n).
        At first glance this runtime might seem bad since we have not focused on any algorithm whose
        runtime is worse than ~ O(n ^2), the beauty of Floyd Warshall is the fact that it will
        give us the shortest path between all vertices. 
        '''

        # 1. Label each self edge to be 0
        # 2. Lavel non-existent edges to be +inf
        # 3. Label all other edges with the corresponding edges weights
        # Once we do that we move onto 3 nest for loops
        # for (u : g):
        #   for (v : g):
        #       for (w : g):
        #           if matrix[u,v] > d[u,w] + d[w,u]:
        #               d[u,v] = d[u,w] + d[w,v]
    
    def sumWeights(self):
        '''
        This is a helper function that sums the weights of all the edges in our 
        graph.
        INPUT:
            none
        OUTPUT:
            Sum of all the weights of all the edges
        Runtime - O(m) - Since we have to sum up all of the edges, our algorithm runs 
        in time proportional to O(m).
        '''

        minHeap = heap.Heap()
        minHeap.buildHeap(self.edges.toList())
        minSum = 0
        while not minHeap.isEmpty():
            minSum += minHeap.remove().weight
        return minSum

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
