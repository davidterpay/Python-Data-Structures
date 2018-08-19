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
                newNode = KDTreeNode(data, (dim + 1) % self.dimensions)
                newNode.setParent(node)
                node.setLeft(newNode)
        else:
            if node.getRight():
                self.__insert(data, node.getRight(), (dim + 1) % self.dimensions)
            else:
                newNode = KDTreeNode(data, (dim + 1) % self.dimensions)
                node.setRight(newNode)
                newNode.setParent(node)

    def insertList(self, lst):
        for data in lst:
            self.insert(data)

    def smallerDimValue(self, data, node, dim):
        return node.getData()[dim] >= data[dim]

    def remove(self, data):
        if self.root:
            self.__remove(data, self.root, 0)
        
    def __remove(self, data, node, dim):
        if not node:
            return None
        if node.getData() == data:
            parent = node.getParent()
            if node.getRight(): # right child exists
                findMin = self.findMin(node.getRight(), (node.getDimDis() + 1) % self.dimensions, node.getDimDis())
                node.setData(findMin.getData())
                right = self.__remove(node.getData(), node.getRight(), (node.getDimDis() + 1) % self.dimensions)
                if right:
                    right.setParent(node)
                node.setRight(right)
            elif node.getLeft(): # left child exists
                findMin = self.findMin(node.getLeft(), (node.getDimDis() + 1) % self.dimensions, node.getDimDis())
                node.setData(findMin.getData())
                right = self.__remove(node.getData(), node.getLeft(), (node.getDimDis() + 1) % self.dimensions)
                if right:
                    right.setParent(node)
                node.setRight(right)
                node.setLeft(None)
            else: # zero child
                node = None
            if not parent:
                self.root = node
        elif node.getData()[dim] < data[dim]:
            node.setRight(self.__remove(data, node.getRight(), (dim + 1) % self.dimensions))
        else:
            node.setLeft(self.__remove(data, node.getLeft(), (dim + 1) % self.dimensions))   
        return node
    
    def findMin(self, node, cd = 0, dim = 0):
        if not node:
            return None
        elif cd == dim:
            if node.getLeft():
                return self.findMin(node.getLeft(), (cd + 1) % self.dimensions, dim)
            else:
                return node
        else:
            cd += 1 % self.dimensions
            return self.minimum(dim, node, self.findMin(node.getLeft(), cd, dim), self.findMin(node.getRight(), cd, dim))

    def minimum(self, dimension, *args):
        return reduce(lambda x,y: x if x.getData()[dimension] <= y.getData()[dimension] else y, [node for node in args if node])

    def find(self, data):
        return self.__find(data, self.root, 0)
    
    def __find(self, data, node, dim):
        if not node:
            return None
        if node.getData() == data:
            return node
        elif node.getData()[dim] < data[dim]:
            return self.__find(data, node.getRight(), (dim + 1) % self.dimensions)
        else:
            return self.__find(data, node.getLeft(), (dim + 1) % self.dimensions)

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
lst = [(0,10),(10,0),(-10,0),(-30,14),(-15,-30),(60,200),(50,730),(-100,-100),(-300,50)]
kdtree.insertList(lst)
print(kdtree)
print('\n\n\n')
kdtree.remove((0, 10))
print('\n\n\n')
print(kdtree)
print('\n\n\n')
print(kdtree.root)

