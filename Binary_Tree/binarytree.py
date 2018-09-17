import sys
sys.path.append('../')
from Stacks import Stack # Will be used in traversals; visit Stacks folder for docs
from Queues import Queue # Will be used in traversals; visit Queues folder for docs
from Binary_Tree import treenode # Importing TreeNode class
from Linked_List import LinkedList # Will be used in converting BST to linked list; visit Linked_List for code and docs
from functools import reduce # Used in longestPath
'''
Written by David Terpay

This is a binary search tree class. It is made of of nodes that are defined in the TreeNode.py class.
In this class I will implement every type of traversal, search, removal, and even go over
some AVL tree properties. In addition, this class will display information describing the
type of tree that we have: full, perfect, complete, balanced. We will keep track of only 
the root of the tree, nothing else.

I imported two classes other than the treenode class stack and queue. These are two classes
that I also wrote and can be found in the Stack and Queue folder on my github. These two classes
will particularly be helpful when we are doing traversals and searches.
'''

class BinarySearchTree():
    def __init__(self, root = None):
        '''
        This is the constructor for our binary tree. It will be a BST meaning that nodes 
        to the left will be smaller than the root and nodes to right will be larger than
        nodes on the left. As mentioned before, this class will only keep track of the root.
        INPUT:
            root = This will help us create a tree from an existing tree given the root.
        OUTPUT:
            A new instance of a binary search tree.
        '''

        self.root = root
    
    def insert(self, data):
        '''
        This function will insert into our tree. If the root is none will simply 
        make the new node the root. Otherwise we will call the helper function to 
        recursively go thorugh the tree until we hit a leaf where we will place 
        our node. We do not place duplicates into
        our tree.
        INPUT:
            data = Data to be inserted into the tree
        OUTPUT:
            Tree with an additional node.

        Runtime -- O(h) -- This algorithm runs in O(h) because we have to get 
        to a leaf node. Ideally, in terms of n this is a lg(n) time where the tree 
        is either complete or perfect. But the runtime can be as bad as O(n) 
        if we simply have a linked list.
        '''

        if self.root is None:
            self.root = treenode.TreeNode(data)
        else:
            self.__insertHelper(data, self.root)

    def __insertHelper(self, data, node):
        '''
        This function will insert into our tree. We will recursively go thorugh 
        the tree until we hit a leaf where we will place our node. We do not place duplicates into
        our tree.
        INPUT:
            data = Data to be inserted into the tree
            node = This parameter helps us keep track of where we are in our tree
        OUTPUT:
            Tree with an additional node.

        Runtime -- O(h) -- This algorithm runs in O(h) because we have to get to a leaf node. Ideally,
        in terms of n this is a lg(n) time where the tree is either complete or perfect. But the runtime can
        be as bad as O(n) if we simply have a linked list.
        '''

        if node.getData() == data: # We do not want duplicates
            return
        elif node.getData() < data:
            if node.getRight() is None:
                newNode = treenode.TreeNode(data)
                newNode.setParent(node)
                node.setRight(newNode)
            else:
                self.__insertHelper(data, node.getRight())
        else:
            if node.getLeft() is None:
                newNode = treenode.TreeNode(data)
                newNode.setParent(node)
                node.setLeft(newNode)
            else:
                self.__insertHelper(data, node.getLeft())

    def insertList(self,*args):
        '''
        Wrapper function that allows you to insert multiple data points at a time.
        INPUT:
            args = list of data points
        OUTPUT:
            BST with new nodes

        RUNTIME -- O(n) -- This function runs in O(n) because it at most takes O(n) time 
        to insert a node into a list but ideally is O(h) and there are n data points in the 
        list. So, O(n) + O(lg(n)) = O(n)
        '''

        for data in args:
            self.insert(data)

    def find(self, data):
        '''
        This function is going to find a node based on inputed data. 
        It will return the entire treenodee unless the data is not in 
        the tree in which it will return None.
        INPUT:
            data = Data that we are trying to find
        OUTPUT:
            The treenode with the data or None

        Runtime -- O(h) -- This algorithm runs in O(h) because we have 
        to get to a leaf node. Ideally, in terms of n this is a lg(n) time 
        where the tree is either complete or perfect. But the runtime can
        be as bad as O(n) if we simply have a linked list.
        '''

        if self.root.getData() == data:
            return self.root
        else:
            return self.__findHelper(data, self.root)
    
    def __findHelper(self, data, node):
        '''
        This function is going to find a node based on inputed data. It will return the entire
        treenodee unless the data is not in the tree in which it will return None.
        INPUT:
            data = Data that we are trying to find
            node = current node that we are checking, helps recursively find the node
        OUTPUT:
            The treenode with the data or None

        Runtime -- O(h) -- This algorithm runs in O(h) because we have to get to a leaf node. Ideally,
        in terms of n this is a lg(n) time where the tree is either complete or perfect. But the runtime can
        be as bad as O(n) if we simply have a linked list.
        '''

        if node == None or node.getData() == data:
            return node
        elif node.getData() < data:
            return self.__findHelper(data, node.getRight())
        else:
            return self.__findHelper(data, node.getLeft())

    def remove(self, data):
        '''
        Case one: 0 children
            We simply delete the node and make the parent point to None for that subtree
        Case two: 1 child
            We push that node up to the the current node and make the parent node point to 
            the left or right child.
        Case three: 2 children
            We find the inorder predecessor and we replace it with the current node.

        The reason the code for this is so extensive is because I take a very pointer based 
        take on remove. I try to move around nodes rather than the data inside of the node.
        This means that I have to constantly update the right, left, and parent pointers of
        multiple treenode objects at times. There is a much faster way to do this where you 
        simply swap out the values and leave the pointers alone. I would say that my 
        implementation is very similar to the implementation you might see with a language 
        like C++ where reference varaibles, pointers, etc. make the job much easier than 
        python does.
        INPUT:
            data = Data to be removed from the tree
        OUTPUT:
            Tree without the treenode containing inputed data

        Runtime -- O(h) -- This algorithm runs in O(h) because we have to get to a 
        leaf node possibly. Ideally, in terms of n this is a lg(n) time where the tree is 
        ither complete or perfect. But the runtime can be as bad as O(n) if we simply have a 
        linked list.
        '''
        
        node = self.find(data)
        if node is None:
            return
        parent = node.getParent()
        if not node.getLeft() and not node.getRight(): # no child removal
            if parent:
                if parent.getRight() == node:
                    parent.setRight(None)
                else:
                    parent.setLeft(None)
            else:
                self.root = None
        elif not node.getLeft() and node.getRight() or not node.getRight() and node.getLeft(): # one child removal
            right = node.getRight()
            left = node.getLeft()
            if parent:
                if parent.getRight() == node:
                    if right:
                        parent.setRight(right)
                        right.setParent(parent)
                    else:
                        parent.setRight(left)
                        left.setParent(parent)
                else:
                    if right:
                        parent.setLeft(right)
                        right.setParent(parent)
                    else:
                        parent.setLeft(left)
                        left.setParent(parent)
            else:
                if right:
                    right.setParent(None)
                    self.root = right
                else:
                    left.setParent(None)
                    self.root = left
        else: # two child removal
            iop = self.findIOP(node.getLeft())
            node.getRight().setParent(iop)
            prevHead = iop.getParent()
            node.getLeft().setParent(iop) #say we exclude this
            iop.setRight(node.getRight())
            if prevHead.getData() != node.getData():
                iop.getParent().setRight(iop.getLeft())
                if iop.getLeft():
                    iop.getLeft().setParent(iop.getParent())
                iop.setLeft(node.getLeft())
            if not parent:
                self.root = iop
                iop.setParent(None)
            else:
                iop.setParent(parent)
                if parent.getLeft() and parent.getLeft().getData() == node.getData():
                    parent.setLeft(iop)
                else:
                    parent.setRight(iop)

    def findIOP(self, node):
        '''
        This function is a helper function to remove. It finds the inorder predecessor.
        In other words it finds the largest data point in the left subtree. This will
        allow us to replace it in case we have a two child removal in remove.
        INPUT:
            node = node of left subtree that will be used to find the IOP.
        OUTPUT:
            IOP
        '''

        while(node.getRight()):
            node = node.getRight()
        return node

    def height(self):
        '''
        This function will return the height of our BST. It is a recursive 
        function that runs through all of the paths in our BST. This makes 
        our runtime rather slow at O(n). It uses the helper function _helper 
        which inputs a root that we will recurse on.
        INPUT: None
        OUTPUT:
            Height of BST
        
        Runtime -- O(n) -- Height runs in time proportional to n because we have 
        to visit all paths to determine which one is the longest.
        '''

        return self.heightHelper(self.root)

    def heightHelper(self, subRoot):
        '''
        This function will return the height of our BST from any given nodee. It is a recursive function 
        that runs through all of the paths in our BST. This makes our runtime rather slow at O(n). It will 
        return -1 if the node is none and otherwise it compares and takes the max height of the left and 
        right subtrees.

        INPUT:
            subRoot: Node that we will determine the longest path
        OUTPUT:
            Height of BST from given node
        
        Runtime -- O(n) -- Height runs in time proportional to n because we have to visit all paths to 
        determine which one is the longest.
        '''

        if subRoot == None:
            return -1
        return 1 + max(self.heightHelper(subRoot.getLeft()), self.heightHelper(subRoot.getRight()))

    def mirror(self):
        '''
        This is a wrapper function to __mirror. This function will do a complete mirror over 
        the center of our BST. All left subtrees will be swapped with right subtrees and right 
        subtrees will be swapped with left subtrees.
        INPUT: None
        OUTPUT:
            Mirrored BST
        
        Runtime -- O(n) -- Since we have to visit every node in our tree, the runtime is O(n).
        '''

        self.__mirror(self.root)
    
    def __mirror(self, root):
        '''
        This function will do a complete mirror over the center of our BST. All left subtrees
        will be swapped with right subtrees and right subtrees will be swapped with left subtrees.
        INPUT: 
            root = Node that we will be swapping children off.
        OUTPUT:
            Mirrored BST
        
        Runtime -- O(n) -- Since we have to visit every node in our tree, the runtime is O(n) because
        we have to visit every single node.
        '''
        
        if root is None:
            return
        right = root.getRight()
        left = root.getLeft()
        root.setLeft(right)
        root.setRight(left)
        self.__mirror(root.getLeft())
        self.__mirror(root.getRight())

    def inOrderTraverasl(self):
        '''
        This function will allow us to do an Inorder traversal. In other words we 
        follow the traversal of visiting left node, checking current, and visiting 
        right node - L curr R. We dive into the tree using this algorithm. This 
        algorithm will print out our data in order. We use the helper function 
        IOT to achieve all of this. We will return a list of our nodes.

        You can see more here: https://en.wikipedia.org/wiki/Tree_traversal

        INPUT: None
        OUTPUT:
            Inorder traversal of our BST.
        
        Runtime -- O(n) -- This function runs in O(n) because we have to visit 
        very single node.
        '''
        lst = []
        self.__IOT(self.root, lst)
        return lst
    
    def __IOT(self, subRoot, lst):
        '''
        This function will allow us to do an Inorder traversal. In other words we follow the 
        traversal of visiting left node, checking current, and visiting right node - L curr R. 
        We dive into the tree using this algorithm. This algorithm will print out our data in order.

        You can see more here: https://en.wikipedia.org/wiki/Tree_traversal
        
        INPUT: 
            subRoot = Root that we will be diving into
            lst = List that keeps track of our inorder traversal.
        OUTPUT:
            Inorder traversal of our BST.
        
        Runtime -- O(n) -- This function runs in O(n) because we have to visit every single node.
        '''

        if subRoot:
            self.__IOT(subRoot.getLeft(),lst)
            lst.append(subRoot)
            self.__IOT(subRoot.getRight(),lst)
    
    def postOrderTraverasl(self):
        '''
        This function will allow us to do an postorder traversal. In other words we follow the 
        traversal of visiting left node, visiting right node, and checking current - L R curr. 
        We dive into the tree using this algorithm. We use the helper function POT to achieve 
        all of this. We will return a list of our nodes.

        You can see more here: https://en.wikipedia.org/wiki/Tree_traversal

        INPUT: None
        OUTPUT:
            Postorder traversal of our BST.
        
        Runtime -- O(n) -- This function runs in O(n) because we have to visit 
        every single node.
        '''

        lst = []
        self.__POT(self.root,lst)
        return lst

    def __POT(self, subRoot, lst):
        '''
        This function will allow us to do an postorder traversal. In other words we follow the 
        traversal of visiting left node, visiting right node, and checking current - L R curr. 
        We dive into the tree using this algorithm. We use the helper function POT to achieve 
        all of this. We will return a list of our nodes.

        You can see more here: https://en.wikipedia.org/wiki/Tree_traversal

        INPUT: 
            subRoot = Root that we will be diving into
            lst = List that keeps track of our postorder traversal.
        OUTPUT:
            Postorder traversal of our BST.
        
        Runtime -- O(n) -- This function runs in O(n) because we have to visit every single node.
        '''

        if subRoot:
            self.__POT(subRoot.getLeft(),lst)
            self.__POT(subRoot.getRight(), lst)
            lst.append(subRoot)

    def preOrderTraversal(self):
        '''
        This function will allow us to do an preorder traversal. In other words we follow the 
        traversal of checking current, visiting left node, and visiting right node - curr L R. 
        We dive into the tree using this algorithm. We use the helper function __PRT to achieve 
        all of this. We will return a list of our nodes.

        You can see more here: https://en.wikipedia.org/wiki/Tree_traversal

        INPUT: None
        OUTPUT:
            Preorder traversal of our BST.
        
        Runtime -- O(n) -- This function runs in O(n) because we have to visit every 
        single node.
        '''

        lst = []
        self.__PRT(self.root, lst)
        return lst

    def __PRT(self, subRoot, lst):
        '''
        This function will allow us to do an preorder traversal. In other 
        words we follow the traversal of checking current, visiting left node, 
        and visiting right node - curr L R. We dive into the tree using 
        this algorithm. We use the helper function __PRT to achieve 
        all of this. We will return a list of our nodes.

        You can see more here: https://en.wikipedia.org/wiki/Tree_traversal

        INPUT: 
            subRoot = Root that we will be diving into
            lst = List that keeps track of our preorder traversal.
        OUTPUT:
            Preorder traversal of our BST.
        
        Runtime -- O(n) -- This function runs in O(n) because we have to visit 
        every single node.
        '''

        if subRoot:
            lst.append(subRoot)
            self.__PRT(subRoot.getLeft(), lst)
            self.__PRT(subRoot.getRight(), lst)

    def levelOrderTraversal(self):
        '''
        This function will allow us to do an level order traversal 
        (ie, from left to right, level by level). In other words we follow the traversal 
        of checking the nodes on each level of the tree. Here we finally use the queue class.
        

        You can see more here: https://en.wikipedia.org/wiki/Tree_traversal

        INPUT: None
        OUTPUT:
            Level order traversal of our BST.
        
        Runtime -- O(n) -- This function runs in O(n) because we have to 
        visit every single node.
        '''

        queue = Queue.Queue()
        lst = []
        queue.enque(self.root)
        while not queue.isEmpty():
            node = queue.deque()
            lst.append(node)
            if node.getLeft():
                queue.enque(node.getLeft())
            if node.getRight():
                queue.enque(node.getRight())
        return lst

    def bfs(self, data):
        '''
        This function will help us find an node given our elements are not entirely sorted 
        or our method of sorting the data is not exactly clear (we might have a heap). 
        This function will do a breadth first search which is similar to a level order 
        traversal in that we will search level by level.
        INPUT:
            data = Data to be searched for
        OUTPUT:
            Node containing the data given the data exists in the tree, otherwise None
        
        Runtime -- O(n) -- The runtime is proptional to the amount of data in our BST because 
        we might have to search every node before finding the correct node. 
        Average runtime is O(n).
        '''

        queue = Queue.Queue()
        queue.enque(self.root)
        while not queue.isEmpty():
            node = queue.deque()
            if node.getData() == data:
                return node
            if node.getLeft():
                queue.enque(node.getLeft())
            if node.getRight():
                queue.enque(node.getRight())
        return None

    def dfs(self, data):
        '''
        This function will help us find an node given our elements are not entirely 
        sorted or our method of sorting the data is not exactly clear (we might have 
        a heap). This function will do a depth first search which is similar to a 
        preorder traversal in that we will search Curr L R. This will allow us to 
        search as deep into our tree as quickly as possible. We use the
        stack class in this function. For documentation, go to the stacks folder 
        in the repository.
        INPUT:
            data = Data to be searched for
        OUTPUT:
            Node containing the data given the data exists in the tree, otherwise None
        
        Runtime -- O(n) -- The runtime is proptional to the amount of data in our BST 
        because we might have to search every node before finding the correct node. 
        Average runtime is O(n).
        '''

        stack = Stack.Stack()
        stack.push(self.root)
        while not stack.isEmpty():
            node = stack.pop()
            if data == node.getData():
                return node
            if node.getLeft():
                stack.push(node.getLeft())
            if node.getRight():
                stack.push(node.getRight())
        return None

    def perfect(self):
        '''
        A perfect tree is a tree that has two nodes and has every node on the same level
        for the last level. In other words, the last level has a full level. A perfect tree
        has only one struture for any given height. We use subRootIsPerfect in this function as a 
        helper function.
        INPUT: None
        OUTPUT:
            True if perfect; false if not perfect
        
        Runtime -- O(n) -- This function runs in time proportional to n because we have to 
        visit every node in our BST
        '''
        
        return self.subRootIsPerfect(self.root)

    def subRootIsPerfect(self,subRoot):
        '''
        A perfect tree is a tree that has two nodes and has every node on the same level
        for the last level. In other words, the last level has a full level. A perfect tree
        has only one struture for any given height.
        INPUT: 
            subRoot: Treenode that we recurse on
        OUTPUT:
            True if perfect; false if not perfect
        
        Runtime -- O(n) -- This function runs in time proportional to n because we 
        have to visit every node in our BST
        '''

        return self.numNodes(subRoot) == pow(2, self.heightHelper(subRoot) + 1) - 1 if subRoot else True

    def full(self):
        '''
        This function will tell us whether our tree is full. A tree is full if every node
        has exactly 2 or 0 children.
        INPUT: None
        OUTPUT:
            True if full; false if not full
        
        Runtime -- O(n) -- This function runs in time proportional to n because we 
        have to visit every node in our BST
        '''

        return self.subRootIsFull(self.root)
    
    def subRootIsFull(self, subRoot):
        '''
        This function will tell us whether our tree is full. A tree is full if every node
        has exactly 2 or 0 children.
        INPUT: 
            subRoot: Treenode that we recurse on.
        OUTPUT:
            True if full; false if not full
        
        Runtime -- O(n) -- This function runs in time proportional to n because we have 
        to visit every node in our BST
        '''

        if subRoot is None:
            return True
        elif subRoot.getLeft() and not subRoot.getRight():
            return False
        elif not subRoot.getLeft() and subRoot.getRight():
            return False
        else:
            return self.subRootIsFull(subRoot.getRight()) and self.subRootIsFull(subRoot.getLeft())

    def complete(self):
        '''
        A BST is complete if the BST is a perfect tree up until the last level 
        where all of the nodes are pushed to the left. This means that we have 
        two cases. Either the left subtree is a perfect tree and right subtree 
        is complete or the left subtree is complete and right subtree is perfect. 
        We use the helper function subRootIsComplete to check if our tree is complete or not.
        INPUT: None
        OUTPUT:
            True if complete. False if not.
        
        Runtime -- O(n) -- This function runs in time proportional to n because 
        we have to look at every single node and its children in this tree.
        '''

        return self.subRootIsComplete(self.root)
    
    def subRootIsComplete(self, subRoot):
        '''
        A BST is complete if the BST is a perfect tree up until the last level where all of
        the nodes are pushed to the left. This means that we have two cases. Either the
        left subtree is a perfect tree and right subtree is complete or the left subtree is
        complete and right subtree is perfect.
        INPUT: 
            subRoot: Treenode that we recurse on.
        OUTPUT:
            True if complete. False if not.

        Runtime - - O(n) - - This function runs in time proportional to n because 
        we have to look at every single node and its children in this tree.
        '''

        if subRoot:
            l = subRoot.getLeft()
            r = subRoot.getRight()
            if not r and not l:
                return True
            if r and not l:
                return False
            else:
                return self.subRootIsPerfect(l) and self.subRootIsComplete(r) or self.subRootIsComplete(l) and self.subRootIsPerfect(r)
        else:
            return True

    def balanced(self):
        '''
        This function will return true if our tree is balanced. In other words, 
        if the absolute difference in height between the left and right subtrees 
        is less than or equal to 1. We use balanceFactor to check the heightt of 
        the left and right subtrees. We will use this function when we inherit this
        class to make AVL trees.
        INPUT: None
        OUTPUT:
            True if balanced. False if not.

        Runtime -- O(n) -- This function runs in time proportional to n because we have 
        to find the height of the right and left subtrees. That requires O(n) time.
        '''

        return abs(self.balanceFactor(self.root)) <= 1

    def balanceFactor(self,subRoot):
        '''
        This function will return true the absolute difference in height 
        between the right and left subtrees is less than or equal to 1. We use 
        balanceFactor to check the height of the left and right subtrees. 
        We will use this function when we inherit this class to make AVL trees.
        INPUT: 
            subRoot = The subRoot whose height we will be checking
        OUTPUT:
            Returns the balance factor of that node

        Runtime -- O(n) -- This function runs in time proportional to n because 
        we have to find the height of the right and left subtrees. That requires O(n) time.
        '''

        return self.heightHelper(subRoot.getRight()) - self.heightHelper(subRoot.getLeft())

    def properties(self):
        '''
        This function will return a dictionary of every single property of our tree.
        INPUT: None
        OUTPUT:
            A dictionary of every single tree property.
        '''

        props = {'Nodes' : len(self)}
        props['Height'] = self.height()
        props['Longest Path'] = self.longestPath()
        props['Sum Distances'] = self.sumDistance()
        props['Perfect'] = self.perfect()
        props['Complete'] = self.complete()
        props['Full'] = self.full()
        props['Balanced'] = self.balanced()
        props['Balance Factor'] = self.balanceFactor(self.root)
        def dataify(node):
            return node.getData()
        props['Inorder Traversal'] = list(map(dataify, self.inOrderTraverasl()))
        props['Preorder Traversal'] = list(map(dataify, self.preOrderTraversal()))
        props['Postorder Traversal'] = list(map(dataify, self.postOrderTraverasl()))
        props['Level order Traversal'] = list(map(dataify, self.levelOrderTraversal()))
        return props

    def printProperties(self):
        '''
        This is a helper function to simply print all of the properties of our BST.
        INPUT: None
        OUTPUT:
            All properties printed.
        '''

        print('{')
        for key, value in self.properties().items():
            print(str(key) + ' : ' + str(value))
        print('}')

    def sumDistance(self):
        '''
        CS225 UIUC practice problem - 
        Each node in a tree has a distance from the root node - the depth of that
        node, or the number of edges along the path from that node to the root. This
        function returns the sum of the distances of all nodes to the root node (the
        sum of the depths of all the nodes). Your solution should take O(n) time,
        where n is the number of nodes in the tree.
        @return The sum of the distances of all nodes to the root
        This function uses the helper function of __sumdistance.
        INPUT: None
        OUTPUT:
            Sum of the distances in our tree from every node to our root.

        Runtime -- O(n) -- This runs in time proportional to n because we visit every node in
        our tree exactly once.
        '''

        sums = 0
        return self.__sumDistance(-1, self.root, sums)
    
    def __sumDistance(self,nodes, subRoot, sums):
        '''
        CS225 UIUC practice problem - 
        Each node in a tree has a distance from the root node - the depth of that
        node, or the number of edges along the path from that node to the root. This
        function returns the sum of the distances of all nodes to the root node (the
        sum of the depths of all the nodes). Your solution should take O(n) time,
        where n is the number of nodes in the tree.
        @return The sum of the distances of all nodes to the root
        INPUT: 
            nodes: This helps us keep track of the amount of nodes above the current node.
                this is particularly helpful when you add on nodes as you move down a tree.
            subRoot: The node that we are recursing on
            sums: We pass this varaible as a refernce throughout the entire run through of our function.
        OUTPUT:
            Sum of the distances in our tree from every node to our root.

        Runtime -- O(n) -- This runs in time proportional to n because we visit every node in
        our tree exactly once.
        '''

        sums += nodes + 1
        if subRoot:
            if subRoot.getLeft():
                sums = self.__sumDistance(nodes + 1, subRoot.getLeft(), sums)
            if subRoot.getRight():
                sums = self.__sumDistance(nodes + 1, subRoot.getRight(), sums)
        return sums

    def longestPath(self):
        '''
        This function will return the longest path from our root to any leaf node.
        This function uses printPaths and reduce in order to iterate through the list 
        of all paths in our BST. 
        ***There may be multiple longest paths***
        INPUT: None
        OUTPUT:
            Longest path in our BST

        Runtime -- O(n) -- Since print paths runs in O(n) time, and since we iterate 
        through the list returned by that function once, our total runtime is O(n).
        '''

        return reduce(lambda x,y: x if len(x) >= len(y) else y, self.printPaths())

    def bstToLinkedLst(self):
        '''
        This converts a binary search tree into a linked list. In order to achieve this we need
        to do a inorder traversal and then simply insert the list into our linked list.
        INPUT: None
        OUTPUT:
            Binary tree to a doubly linked list
        
        '''

        linked = LinkedList.LinkedList()
        lst = self.inOrderTraverasl()
        linked.insertList([node.getData() for node in lst])
        return linked

    def printPaths(self):
        '''
        Creates list of all the possible paths from the root of the tree to any leaf
        node and adds it to another list. Path is, all sequences starting at the root 
        node and continuing downwards, ending at a leaf node. Paths ending in a left 
        node should be added before paths ending in a node further to the right. 
        This uses the helper function __printPaths().
        INPUT: None
        OUTPUT:
            A list of all paths to leaf nodes from the root.
        
        Runtime -- O(n)  -- The runtime of this function is proportional to n because we have 
        to  go thorugh every single node in order to reach the leaf nodes in our tree.
        '''

        paths = []
        self.__printPaths(self.root,[],paths)
        return paths

    def __printPaths(self,subRoot, path, paths):
        '''
        Creates list of all the possible paths from the root of the tree to any leaf
        node and adds it to another list. Path is, all sequences starting at the 
        root node and continuing downwards, ending at a leaf node. Paths ending 
        in a left node should be added before paths ending in a node further to the right.
        INPUT:
            subRoot: Root that we will be recursing on
            path: The current path we are looking on
            paths: All of the paths in our BST
        OUTPUT:
            A list of all paths to leaf nodes from the root.
        
        Runtime -- O(n)  -- The runtime of this function is proportional 
        to n because we have to go thorugh every single node in order to reach 
        the leaf nodes in our tree.
        '''

        if not subRoot:
            return
        path.append(subRoot.getData())
        if not subRoot.getRight() and not subRoot.getLeft():
            paths.append(path)
        else:
            newPath = path.copy()
            self.__printPaths(subRoot.getLeft(), path, paths)
            self.__printPaths(subRoot.getRight(), newPath, paths)

    def numNodes(self,subRoot):
        '''
        This function will return the number of nodes we have in our BST.
        INPUT: None
        OUTPUT:
            Number of treenodes in our BST.

        Runtime -- O(n) -- This function runs in time proportional to n because we have to 
        visit every single node.
        '''

        if not subRoot:
            return 0
        return 1 + self.numNodes(subRoot.getRight()) + self.numNodes(subRoot.getLeft())
    
    def toString(self,node,depth):
        '''
        Helps us visualize the tree. Viewed horizontally.
        '''

        ret = ""
        if node.getRight():
            ret += self.toString(node.getRight(),depth + 1)
        ret += "\n\n" + ("     "*depth) + str(node.getData())
        if node.getLeft():
            ret += self.toString(node.getLeft(), depth + 1)
        return ret

    def clear(self, subRoot):
        '''
        This is a helper function to del(). We will recursively dive into the bottom of the
        tree and delete as we come back up.
        INPUT:
            subRoot: Root we are recursing on
        OUTPUT:
            Deleted tree
        
        '''

        if subRoot:
            l = subRoot.getLeft()
            r = subRoot.getRight()
            self.clear(l)
            self.clear(r)
            del subRoot
            
    def __len__(self):
        '''
        This function simply returns the length of our BST, allows for functionality using
        len(). It uses the numNodes helper function to determine the number of treenodes.
        For documentation look at that function.
        INPUT: None
        OUTPUT:
            Number of treenodes in our BST.
        '''

        return self.numNodes(self.root)
    
    def __del__(self):

        '''
        Deletes all memory associated with the creation of a BST.
        '''

        self.clear(self.root)
    
    def __str__(self, depth=0):
        '''
        Helps us visualize the tree. Viewed horizontally.
        '''

        return self.toString(self.root,0)
bst = BinarySearchTree()
bst.insert(10)
print(bst)