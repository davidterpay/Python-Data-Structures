import sys
sys.path.append('../')
from Binary_Tree.binarytree import BinarySearchTree
from Binary_Tree.treenode import TreeNode

class KDTree(BinarySearchTree):
    def __init__(self, dimensions):
        '''
        '''
        self.root = None
        self.dimensions = dimensions

    def insert(self, data):
        if self.root:
            self.__insert(data, self.root, 0)
        else:
            self.root = TreeNode(data)
        
    def __insert(self, data, node, dim):
        if self.smallerDimValue(data, node, dim):
            if node.getLeft():
                self.__insert(data, node.getLeft(), (dim + 1) % self.dimensions)
            else:
                newNode = TreeNode(data)
                newNode.setParent(node)
                node.setLeft(newNode)
        else:
            if node.getRight():
                self.__insert(data, node.getRight(), (dim + 1) % self.dimensions)
            else:
                newNode = TreeNode(data)
                node.setRight(newNode)
                newNode.setParent(node)

    def insertList(self, lst):
        for data in lst:
            self.insert(data)

    def smallerDimValue(self, data, node, dim):
        return node.getData()[dim] >= data[dim]

    def remove(self, data):
        if self.root:
            self.__remove(data)
        
    def __remove(self, data):
        pass

    def find(self, data):
        return self.__find(data)
    
    def __find(self, data):
        pass

    def createBalancedTree(self):
        pass

    def sort(self):
        pass

    def quicksort(self):
        pass

    def shouldReplace(self):
        pass

    def euclideanDistance(self):
        pass
    
    def findNearestNeighbor(self):
        pass

from random import randint
kdtree = KDTree(2)
lst = [(randint(-10, 10),randint(-10,10)) for x in range(3)]
kdtree.insertList(lst)
print(kdtree)
