import sys
sys.path.append('../')
from Stacks import Stack # Will be used in traversals
from Queues import Queue # Will be used in traversals
import TreeNode # Importing TreeNode class
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
        This function will insert into our tree. If the root is none will simply make the new
        node the root. Otherwise we will call the helper function to recursively go thorugh 
        the tree until we hit a leaf where we will place our node. We do not place duplicates into
        our tree.
        INPUT:
            data = Data to be inserted into the tree
        OUTPUT:
            Tree with an additional node.

        Runtime -- O(h) -- This algorithm runs in O(h) because we have to get to a leaf node. Ideally,
        in terms of n this is a lg(n) time where the tree is either complete or perfect. But the runtime can
        be as bad as O(n) if we simply have a linked list.
        '''

        if self.root is None:
            self.root = TreeNode.TreeNode(data)
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
                newNode = TreeNode.TreeNode(data)
                newNode.setParent(node)
                node.setRight(newNode)
            else:
                self.__insertHelper(data, node.getRight())
        else:
            if node.getLeft() is None:
                newNode = TreeNode.TreeNode(data)
                newNode.setParent(node)
                node.setLeft(newNode)
            else:
                self.__insertHelper(data, node.getLeft())

    def find(self, data):
        '''
        This function is going to find a node based on inputed data. It will return the entire
        treenodee unless the data is not in the tree in which it will return None.
        INPUT:
            data = Data that we are trying to find
        OUTPUT:
            The treenode with the data or None

        Runtime -- O(h) -- This algorithm runs in O(h) because we have to get to a leaf node. Ideally,
        in terms of n this is a lg(n) time where the tree is either complete or perfect. But the runtime can
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
        multiple treenode objects at times. There is a much faster way to do this where you simply
        swap out the values and leave the pointers alone. I would say that my implementation is very
        similar to the implementation you might see with a language like C++ where reference varaibles, 
        pointers, etc. make the job much easier than python does.
        INPUT:
            data = Data to be removed from the tree
        OUTPUT:
            Tree without the treenode containing inputed data

        Runtime -- O(h) -- This algorithm runs in O(h) because we have to get to a leaf node possibly. Ideally,
        in terms of n this is a lg(n) time where the tree is either complete or perfect. But the runtime can
        be as bad as O(n) if we simply have a linked list.
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
            node.getLeft().setParent(iop)
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
                if parent.getLeft().getData() == node.getData():
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

    def height(self, subRoot):  # Work on this
        pass

    def mirror(self): # Work on this
        pass

    def inOrderTraverasl(self):  # Work on this
        pass

    def postOrderTraverasl(self):  # Work on this
        pass

    def preOrderTraversal(self):  # Work on this
        pass

    def levelOrderTraversal(self):  # Work on this
        pass

    def bfs(self):  # Work on this
        pass

    def dfs(self):  # Work on this
        pass

    def perfect(self):  # Work on this
        pass

    def full(self):  # Work on this
        pass

    def complete(self):  # Work on this
        pass

    def balanced(self):  # Work on this
        pass

    def properties(self):  # Work on this
        pass
    
    def sumDistance(self):  # Work on this
        pass
    
    def longestPath(self):  # Work on this
        pass
    
    def printPaths(self):  # Work on this
        pass
    
    def __len__(self):  # Work on this
        pass
    
    def __del__(self):  # Work on this
        pass
    
    def __str__(self):  # Work on this
        pass

bst = BinarySearchTree()
