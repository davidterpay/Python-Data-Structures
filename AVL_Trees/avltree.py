import sys
sys.path.append('../')
from Binary_Tree.binarytree import BinarySearchTree
from Binary_Tree.treenode import TreeNode
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

        self.root = root

    def insertList(self, *args):
        '''

        '''

        for num in args:
            self.insert(num)
    
    def insert(self, data):
        '''
        '''

        if not self.root:
            self.root = TreeNode(data)
        else:
            self.__insert(data, self.root)
        
    def __insert(self, data, node):
        '''
        '''

        if data == node.getData():
            return # no duplicates
        elif data > node.getData():
            if node.getRight():
                self.__insert(data, node.getRight())
                # heightBalance = self.balanceFactor(node)
                # if heightBalance >= 2:
                #     if self.balanceFactor(node.getRight()) == 1:
                #         self.leftRotation(node)
                #     else:
                #         self.rightLeftRotation(node)
            else:
                newNode = TreeNode(data)
                newNode.setParent(node)
                node.setRight(newNode)
        else:
            if node.getLeft():
                self.__insert(data, node.getLeft())
                # heightBalance = self.balanceFactor(node)
                # if heightBalance <= -2:
                #     if self.balanceFactor(node.getLeft()) == -1:
                #         self.rightRotation(node)
                #     else:
                #         self.leftRightRotation(node)
            else:
                newNode = TreeNode(data)
                newNode.setParent(node)
                node.setLeft(newNode)
        self.rebalance(node)
    
    def remove(self, data):
        '''
        '''

        self.__remove(data, self.root)
    
    def twoChildRemoval(self, node):
        parent = node.getParent()
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
    
    def oneChildRemoval(self, node):
        parent = node.getParent()
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
    
    def __remove(self, data, node):
        '''
        '''
        if not node:
            return
        if node.getData() == data:
            parent = node.getParent()
            if node.getRight() and node.getLeft(): #two child removal
                self.twoChildRemoval(node)
            elif not node.getLeft() and node.getRight() or not node.getRight() and node.getLeft():# one child removal
                self.oneChildRemoval(node)
            else:
                if parent:
                    if parent.getRight() == node:
                        parent.setRight(None)
                    else:
                        parent.setLeft(None)
                else:
                    self.root = None
        elif node.getData() > data:
            self.__remove(data, node.getLeft())
        else:
            self.__remove(data, node.getRight())
        self.rebalance(node)
    
    def rebalance(self, node):
        heightBalance = self.balanceFactor(node)
        heightBalanceRight = self.balanceFactor(node.getRight()) if node.getRight() else 0
        heightBalanceLeft = self.balanceFactor(node.getLeft()) if node.getLeft() else 0
        if heightBalance >= 2:
            if heightBalanceRight == 1:
                self.leftRotation(node)
            else:
                self.rightLeftRotation(node)
        if heightBalance <= -2:
            if heightBalanceLeft == 1:
                self.leftRightRotation(node)
            else:
                self.rightRotation(node)

    def leftRotation(self, node):
        '''
        '''

        right = node.getRight()
        if node == self.root:
            self.root = right
            right.setParent(None)
        else:
            node.getParent().setRight(right)
            right.setParent(node.getParent())
        node.setParent(right)
        node.setRight(right.getLeft())
        right.setLeft(node)
    
    def leftRightRotation(self, node):
        '''
        '''

        left = node.getLeft()
        leftRight = left.getRight()


        left.setRight(leftRight.getLeft())
        leftRight.setLeft(left)
        left.setParent(leftRight)
        leftRight.setParent(node)
        node.setLeft(leftRight)
        self.rightRotation(node)

    
    def rightRotation(self, node):
        '''
        '''

        left = node.getLeft()
        if node == self.root:
            self.root = left
            left.setParent(None)
        else:
            parent = node.getParent()
            parent.setLeft(left)
            left.setParent(parent)
        node.setParent(left)
        node.setLeft(left.getRight())
        left.setRight(node)

    def rightLeftRotation(self, node):
        '''
        '''

        right = node.getRight()
        rightLeft = right.getLeft()
        right.setLeft(rightLeft.getRight())
        node.setRight(rightLeft)
        rightLeft.setParent(node)
        rightLeft.setRight(right)
        right.setParent(rightLeft)
        self.leftRotation(node)

avl = AVLTree()
avl.insertList(100,50,200,0,12,4,-234,-543,40)
print(avl)
print(avl.root.getRight().getLeft())