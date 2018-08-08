import sys
sys.path.append('../')
# importing BinarySearchTree class
from Binary_Tree.binarytree import BinarySearchTree
'''
Written by David Terpay
This class will demonstrate some of the functionality of a (min)heap. 
The heap I will build is going to be a min heap where the 
smallest data point is on top and the tree nodes value's 
increases as you move down the tree. I utilize the binarytree
class from Binary_Tree to build the heap. You can check 
out the code and documentation in the Binary_Tree folder in 
this repository.

Heap is a complete binary tree. Root node is smallest node.
Parent is always smaller than all decendents. A heap is a 
recusive structure. We store the tree in an array. The tree
is just how we think about this data structure. Since our tree
is always complete there is an easy way to map the tree onto
a array. Adds and removes elements (when all we want to do
is remove the minimum element) in amortized O(1) time.
'''


class Heap(BinarySearchTree):
    def __init__(self):
        self.root = None
        self.array = [None, None]
        self.size = 0
        self.capacity = 0
    
    def insert(self, data):
        if self.size == self.capacity:
            self.growArray()
        self.size += 1
        self.array[self.size] = data
        self.heapifyUp(self.size)
    
    def remove(self):
        '''
        This automatically removes the min or max depending
        on whether it is a max or min prioirity heap. We have to
        insert at the beginning or end to have O(1) runtime. Insert
        into a heap, we insert at the end. We remove from the end
        by first removing the root, and then replacing the root with
        the last element in our array. Then we call heapify down.
        ''' 
        return self.__removeMin()

    def isEmpty(self):
        '''
        checks if heap is empty
        '''
        pass
        
    def heapifyUp(self, index):
        '''
        Heapify up rebalances or fixes the heap from the insertion 
        point up to the root if necessary. It checks the parent and 
        swaps if necessary.

        Runtime -- O(lg(n)) -- Because we might have to go up to
        the entire height of the tree.
        '''
        if index > 1:
            if (self.array[index] < self.array[self.parent(index)]):
                self.swap(self.array[index], self.array[self.parent(index)])
                self.heapifyUp(self.parent(index))

    
    def heapifyDown(self, index = 1):
        '''
        We start at the root and build downward.

        Runtime -- O(lg(n)) -- We might have to go down to the very bottom of
        our tree.
        '''
        if not self.__isLeaf(index):
            minChildIndex = self.__minChild(index)
            if (self.array[index] > self.array[minChildIndex]):
                self.swap(index,minChildIndex)
                self.heapifyDown(minChildIndex)

    def swap(self, low, upper):
        '''
        Swaps the data of the nodes in low and upper.
        '''
        pass

    def buildHeap(self):
        '''
        Builds a heap from an existing list of data.
        Option 1: sort the array --> O(nlg(n)) if using mergesort, etc.
        Option 2: Call heapify up after every insert into our new list.
            O(nlg(n)) runtime because we have to insert n elements and
            lg(n) time to insert into our list
        Option 3: Call heapifydown. assumes that right and left subtrees 
            are heaps just might swap one element. The leaf nodes are already
            heaps so we have to simply call heapifydown on the parents of the
            leaf nodes and work our way up. Half of our array is already a heap.
            We have to heapifydown on half of our array.
        '''
        pass

    def __minChild(self,index):
        '''
        Used for heapifydown
        '''
        pass

    def __isLeaf(self, index):
        '''
        checks if is a leaf
        '''
        pass

    def growArray(self):
        '''
        Doubles the size of curr array and copys the data.
        This runs in O(1) amortized time.
        '''
        pass

    def __removeMin(self):
        '''
        This automatically removes the min or max depending
        on whether it is a max or min prioirity heap.
        '''
        min = self.array[1]
        self.array[1] = self.array[self.size]
        self.size -= 1
        self.heapifyDown()
        return min
    
    def leftChild(self):
        '''
        left child is 2 * index if rooted at 1 index.
        '''
        pass
    
    def rightChild(self):
        '''
        right child is 2 index + 1 if rooted at 1 index.
        '''
        pass
    
    def parent(self, index):
        '''
        parent is index // 2 if rooted at 1 index.
        '''
        pass
    

