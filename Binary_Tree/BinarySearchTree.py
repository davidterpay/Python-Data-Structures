import sys
sys.path.append('../')
from Stack import Stack # Will be used in traversals
from Queue import Queue # Will be used in traversals
from Binary_Tree import TreeNode # Importing TreeNode class
'''
Written by David Terpay

This is a binary search tree class. It is made of of nodes that are defined in the TreeNode.py class.
In this class I will implement every type of traversal, search, removal, and even go over
some AVL tree properties. In addition, this class will display information describing the
type of tree that we have: full, perfect, complete, balanced. We will keep track of only 
the root of the tree, nothing else.
'''
#propertities
#   height
#       longest path
#   root
#   left right
#   perfect
#   full
#   complete
#   balanced
#   AVL properties ?
#       rebalancing
#   traversals
#       INORDER
#       PREORDER
#       POSTORDER
#       LEVELORDER
#   Searching
#       BFS
#       DFS
#   Removal
#       No child
#       one child
#       two child
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
        pass

    def remove(self, data):
        pass

    def find(self, data):
        pass

    def height(self, subRoot):
        pass

    def mirror(self):
        pass

    def inOrderTraverasl(self):
        pass

    def postOrderTraverasl(self):
        pass

    def preOrderTraversal(self):
        pass

    def levelOrderTraversal(self):
        pass

    def bfs(self):
        pass

    def dfs(self):
        pass

    def perfect(self):
        pass

    def full(self):
        pass

    def complete(self):
        pass

    def balanced(self):
        pass

    def sumDistance(self):
        pass
    
    def longestPath(self):
        pass
    
    def __len__(self):
        pass
    
    def __del__(self):
        pass
    
    def __str__(self):
        pass
