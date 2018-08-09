import sys
sys.path.append('../')
# importing BinarySearchTree class
# from Binary_Tree.binarytree import BinarySearchTree
import math
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


class Heap():
    def __init__(self):
        self.array = [None]
        self.size = 0
        self.capacity = 1
    
    def insert(self, data):
        if self.size == self.capacity:
            self.growArray()
        if self.size == 0:
            self.array.append(data)
            self.size += 1
        else:
            self.size += 1
            self.array[self.size] = data
            self.heapifyUp(self.size)

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
                self.swap(index, self.parent(index))
                self.heapifyUp(self.parent(index))

    def heapifyDown(self, index=1):
        '''
        We start at the root and build downward.

        Runtime -- O(lg(n)) -- We might have to go down to the very bottom of
        our tree.
        '''

        if not self.__isLeaf(index):
            minChildIndex = self.__minChild(index)
            if (self.array[index] > self.array[minChildIndex]):
                self.swap(index, minChildIndex)
                self.heapifyDown(minChildIndex)

    def __minChild(self, index):
        '''
        Used for heapifydown
        '''
        if self.rightChild(index) <= self.size:
            if self.array[self.rightChild(index)] < self.array[self.leftChild(index)]:
                return self.rightChild(index)
        return self.leftChild(index)

    def __isLeaf(self, index):
        '''
        checks if is a leaf
        '''
        return index * 2 > self.size

    def swap(self, low, upper):
        '''
        Swaps the data of the nodes in low and upper.
        '''
        first = self.array[low]
        self.array[low] = self.array[upper]
        self.array[upper] = first

    def growArray(self):
        '''
        Adds another level of our model tree copys the data.
        This runs in O(1) amortized time.
        '''
        
        self.capacity += int(pow(2, math.log2(self.capacity + 1)))
        newArray = [None for i in range((self.capacity))]
        newArray[0:self.size] = self.array
        self.array = newArray
    
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

    def __removeMin(self):
        '''
        This automatically removes the min or max depending
        on whether it is a max or min prioirity heap.
        '''
        min = self.array[1]
        self.array[1] = self.array[self.size]
        self.array[self.size] = None
        self.size -= 1
        self.heapifyDown()
        return min

    def isEmpty(self):
        '''
        checks if heap is empty
        '''
        return not self.array[1]

    def buildHeap(self, lst):
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
        self.array.extend(lst)
        self.size = len(lst)
        height = 0
        while pow(2, height + 1) - 1 < self.size:
            height += 1
        self.capacity = pow(2, height + 1) - 1
        self.array.extend([None] * (self.capacity - self.size))
        for index in range(self.parent(self.size),0,-1):
            self.heapifyDown(index)

    def heapSort(self, lst):
        '''
        first build the heap. second remove min n times. place min
        at the end. last step is reversing the array. using index 0
        as our start.
        in memory, stable sort.
        buildheap -- O(n) --
        removeMin -- O(nlg(n)) --
        reverse -- O(n) --
        '''
        self.buildHeap(lst)
        prevSize = self.size
        for __ in range(self.size):
            min = self.array[1]
            self.array[1] = self.array[self.size]
            self.array[self.size] = min
            self.size -= 1
            self.heapifyDown()
        for low in range(1,(prevSize + 1)//2):
            self.swap(low, prevSize - low)
        self.size = prevSize
        return self.array[1:self.size]

    def leftChild(self, index):
        '''
        left child is 2 * index if rooted at 1 index.
        '''
        return index * 2
    
    def rightChild(self, index):
        '''
        right child is 2 index + 1 if rooted at 1 index.
        '''
        return index * 2 + 1
    
    def parent(self, index):
        '''
        parent is index // 2 if rooted at 1 index.
        '''
        return index // 2
    
    def __str__(self):
        string = 'Size is : ' + str(self.size) + '\nCapacity is : ' + str(self.capacity)
        string += '\nArray : ' + str(self.array)
        return string

    

heap = Heap()
print(heap.heapSort([30, 20, 0, 8, 9, 7,23,4,19,1,-234,-1,-9043]))
