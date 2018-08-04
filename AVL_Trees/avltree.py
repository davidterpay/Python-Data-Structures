import sys
sys.path.append('../')
from Binary_Tree.binarytree import BinarySearchTree
'''
Written by David Terpay
This will demonstrate some of the functionality we might see in a AVL Tree. This
will include rotations, insertions, and removals that keep the balance factor
of the entire tree within an absolute value of 1. This ensures that our runtime
of insertion, removal, and find are O(lg(n)). We will inherit the BST class that 
I previously created. You can check out the code and documentation in the Binary_Tree
folder in this repository.
'''

class AVLTree(BinarySearchTree):
    def __init__(self, root = None):
        '''
        Since we are techincally a binary search tree, we will simply
        call and inherit the functionality of the BST class and overwrite
        some its functions such as insert, removal, etc. here.
        '''

        super.__init__(root)
    
    def rebalance(self, node):
        pass
    
    def insert(self, data):
        pass
    
    def remove(self, data):
        pass
    
    def leftRotation(self, node):
        pass
    
    def leftRightRotation(self, node):
        pass
    
    def rightRotation(self, node):
        pass

    def rightLeftRotation(self, node):
        pass 