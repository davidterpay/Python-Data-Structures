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
            node = KDTreeNode(data, len(data))
            self.__insert(node, self.root, 0)
        else:
            self.root = KDTreeNode(data, 0)
        
    def __insert(self, newNode, node, dim):
        if self.smallerDimValue(newNode, node, dim):
            if node.getLeft():
                self.__insert(newNode, node.getLeft(), (dim + 1) % self.dimensions)
            else:
                newNode.setDimDis((dim + 1) % self.dimensions)
                newNode.setParent(node)
                node.setLeft(newNode)
        else:
            if node.getRight():
                self.__insert(newNode, node.getRight(), (dim + 1) % self.dimensions)
            else:
                newNode.setDimDis((dim + 1) % self.dimensions)
                node.setRight(newNode)
                newNode.setParent(node)

    def insertList(self, lst):
        for data in lst:
            self.insert(data)

    def smallerDimValue(self, newNode, node, dim):
        return node.getData()[dim] >= newNode.getData()[dim]

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

    def createBalancedTree(self, lst):
        data = self.quickselect(lst)
        self.root = self.__buildTree(0, len(data) - 1, data, 0)
        return list(map(KDTreeNode.getData, data))

    def __buildTree(self, left, right, lst, dim):
        if left > right:
            return
        median = (left + right) // 2
        root = lst[median]
        root.setDimDis(dim)
        right = self.__buildTree(median + 1, right, lst, (dim + 1) % self.dimensions)
        if right:
            right.setParent(root)
        left = self.__buildTree(left, median - 1, lst, (dim + 1) % self.dimensions)
        if left:
            left.setParent(root)
        root.setRight(right)
        root.setLeft(left)
        return root

    def __sort(self, lst, left, right, dim):
        if left < right:
            median = (left + right) // 2
            # We need pivot to correctly put median in the middle
            # So that we can properly sort the other dimensions and halves
            self.pivot(lst, left, right, median, dim)
            # Recursively sorting the right and left sides on the array
            self.__sort(lst, left, median - 1, (dim + 1) % self.dimensions)
            self.__sort(lst, median + 1, right, (dim + 1) % self.dimensions)
            return lst

    def pivot(self, lst, left, right, median, dim):
        # We check if the partition is greater than or equal to median. If
        # so then we have to recur on the proper side.
        pivot = self.partition(left, right, lst, dim)
        if pivot != median:
            if pivot < median:
                self.pivot(lst, pivot + 1, right, median, dim)
            elif pivot > median:
                self.pivot(lst, left, pivot - 1, median,  dim)
        
    def partition(self, left, right, lst, dim):
        low = left - 1
        for x in range(left, right):
            if self.smallerDimValue(lst[x], lst[right], dim):
                low += 1
                temp = lst[low]
                lst[low] = lst[x]
                lst[x] = temp
        low += 1
        temp = lst[right]
        lst[right] = lst[low]
        lst[low] = temp
        return low

    def quickselect(self, lst):
        data = [KDTreeNode(value, 0) for value in lst]
        return self.__sort(data, 0, len(data) - 1, 0)

    def shouldReplace(self, target, currBest, potential):
        potentialDistance = self.euclideanDistance(target, potential)
        currentDistance = self.euclideanDistance(target, currBest)
        return True if potentialDistance <= currentDistance else False

    def euclideanDistance(self, first, second):
        distance = 0
        for index, data in enumerate(first.getData()):
            distance += pow(data - second.getData()[index], 2)
        return pow(distance, 1/2)
    
    def findNearestNeighbor(self):
        pass

from random import randint
kdtree = KDTree(2)
lstData = [(3, 2), (4, 4), (5, 8), (6, 1), (9, 0), (1, 1), (2, 2), (8, 7)]
print(kdtree.createBalancedTree(lstData))
print(kdtree)
print(kdtree.root.getRight().getRight().getRight())
