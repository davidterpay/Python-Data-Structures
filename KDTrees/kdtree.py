import sys
sys.path.append('../')
from Binary_Tree.binarytree import BinarySearchTree
from kdtreenode import KDTreeNode
from functools import reduce

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
            self.root = KDTreeNode(data, 0)
        
    def __insert(self, data, node, dim):
        if self.smallerDimValue(data, node, dim):
            if node.getLeft():
                self.__insert(data, node.getLeft(), (dim + 1) % self.dimensions)
            else:
                newNode = KDTreeNode(data, dim)
                newNode.setParent(node)
                node.setLeft(newNode)
        else:
            if node.getRight():
                self.__insert(data, node.getRight(), (dim + 1) % self.dimensions)
            else:
                newNode = KDTreeNode(data, dim)
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
    
    def findMin(self, node, currentDimension, dim):
        if not node:
            return None
        elif currentDimension == dim:
            if node.getLeft():
                self.findMin(node.getLeft(), (currentDimension + 1) % self.dimensions, dim)
            else:
                return node
        else:
            cd = (currentDimension + 1) % self.dimensions
            return self.minimum(dim, node, self.findMin(node.getLeft(), cd, dim), self.findMin(node.getRight(), cd, dim))

    def minimum(self, dimension, *args):
        lst = [x for x in args if x]
        return lst[0] if len(lst) == 1 else reduce(lambda x,y: x if x[dimension] < y[dimension] else y, lst)

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
print('\n\n\n')
print(kdtree.root.getRight())
