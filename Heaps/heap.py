import sys
sys.path.append('../')
# importing BinarySearchTree class and Treenode class for visualization
from Binary_Tree.binarytree import BinarySearchTree
from Binary_Tree.treenode import TreeNode
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
        '''
        We will keep track of four variables. Root which is the root of our tree.
        Array which will hold our data maintained in the heap. Size which 
        will keep track of many data points we have in our list. Capacity will
        tell us how many more nodes we can place in that level of our binary tree.
        '''

        self.tree = BinarySearchTree()
        self.array = [None]
        self.size = 0
        self.capacity = 1
    
    def insert(self, data):
        '''
        Insert will always insert at the very end of the heap in order to maintain
        a running time of O(1). Once we insert at the very end, we heapify up
        from the bottom. In addition, if the size is near the capacity, we
        grow the array (aka double it).
        INPUT:
            data: Data to be inserted
        OUTPUT:
            Heap with new data
        Runtime -- O(lg(n)) -- Since we are inserted at the very end, and since heapifyUp
        runs in time proptional to the height, we get a lg(n) running time.
        '''

        if self.size == self.capacity:
            self.growArray()
        if self.size == 0:
            self.array.append(data)
            self.size += 1
        else:
            self.size += 1
            self.array[self.size] = data
            self.heapifyUp(self.size)

    def buildTree(self):
        '''
        This function will help us build the binary tree attribute in this class.
        It will take the heap and map it onto a binary tree for an easy visualization of
        the heap. We use the __buildTree helper function here.
        INPUT: None
        OUTPUT:
            A binary tree visualization of a heap
        
        Runtime -- O(nlg(n)) -- Since there are n elements in our heap and inserting each
        element into the tree takes lg(n) time, our runtime is nlg(n).
        '''

        del self.tree
        self.tree = BinarySearchTree()
        lstData = [x for x in self.array if x]
        for data in lstData:
            if not self.tree.root:
                self.tree.root = TreeNode(data)
            else:
                self.__buildTree(self.tree.root,data)

    def __buildTree(self, node, data):
        '''
        This function will help us build the binary tree attribute in this class.
        It will take the heap and map it onto a binary tree for an easy visualization of
        the heap.
        INPUT:
            node: Current node we are recursing on
            data: Data to be inserted into the tree
        OUTPUT:
            A binary tree visualization of a heap
        
        Runtime -- O(nlg(n)) -- Since there are n elements in our heap and inserting each
        element into the tree takes lg(n) time, our runtime is nlg(n).
        '''

        if node is not None:
            if not node.getLeft():
                newNode = TreeNode(data)
                newNode.setParent(node)
                node.setLeft(newNode)
                return
            elif node.getLeft() and not node.getRight():
                newNode = TreeNode(data)
                newNode.setParent(node)
                node.setRight(newNode)
                return
            else:
                if self.tree.subRootIsPerfect(node):
                    while node.getLeft():
                        node = node.getLeft()
                    newNode = TreeNode(data)
                    newNode.setParent(node)
                    node.setLeft(newNode)
                    return
                elif self.tree.subRootIsPerfect(node.getLeft()) and self.tree.subRootIsComplete(node.getRight()):
                    self.__buildTree(node.getRight(), data)
                else:
                    self.__buildTree(node.getLeft(), data)           

    def heapifyUp(self, index):
        '''
        Heapify up rebalances or fixes the heap from the insertion 
        point up to the root if necessary. It checks the parent and 
        swaps if necessary.
        INPUT:
            index: Index that we are moving upwards with
        OUTPUT:
            Array that maintains the heap property

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
        Checks if the index is a leaf node.
        INPUT:
            index: Index that we are checking
        OUTPUT:
            True if leaf, false if not.
        '''

        return index * 2 > self.size

    def swap(self, low, upper):
        '''
        Swaps the data of the nodes in low and upper.
        INPUT:
            low: Lower index we want to swap.
            upper: Upper index we want to swap.
        OUTPUT:
            Array with data swapped
        '''

        first = self.array[low]
        self.array[low] = self.array[upper]
        self.array[upper] = first

    def growArray(self):
        '''
        Adds another level of our model tree copys the data.
        This runs in O(1) amortized time since we are doubling the array
        everytime we need to.
        INPUT: None
        OUTPUT:
            New array that is double the previous size without empty locations
            containing None.
        
        Runtime -- O(1)* -- Since we are doubling the size of our array everytime
        we reach the capacity, we effectively allow the algorithm to run in O(1) 
        amortized. 
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
        INPUT: None
        OUTPUT:
            Heap without min
        
        Runtime -- O(lg(n)) -- Since we might have to go through the entire tree, our runtime
        is proportional to the height which is lg(n).
        ''' 

        return self.__removeMin()

    def __removeMin(self):
        '''
        This automatically removes the min or max depending
        on whether it is a max or min prioirity heap. In this case, we have a min heap.
        INPUT: None
        OUTPUT:
            Heap without min
        
        Runtime -- O(lg(n)) -- Since we might have to go through the entire tree, our runtime
        is proportional to the height which is lg(n).
        '''

        min = self.array[1]
        self.array[1] = self.array[self.size]
        self.array[self.size] = None
        self.size -= 1
        self.heapifyDown()
        return min

    def isEmpty(self):
        '''
        Checks if heap is empty
        INPUT: None
        OUTPUT:
            True if empty, false if not.
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
        
        INPUT:
            lst: List of data
        OUTPUT:
            Heap
        
        Runtime -- O(n) -- Since we ignore the leaf nodes, half of our heap is partially sorted 
        and is a heap. We only have to call heapifydown on the parents of the leaves and work up.
        There is a proof of induction of this that can be found online.
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

    def heapSort(self, lst = None):
        '''
        In order to heap sort, first we build a heap using buildheap (this is
        if the list is new and inputed otherwise we keep the current list).
        Building the heap takes O(n) time. Second we remove min n times. Lastly,
        we reverse the array using index 0 as our start when we are returning 
        (this is so we do not return None).
        INPUT:
            lst: List of data if we want to input new data
        OUTPUT:
            Sorted list of data that will be a member of the class.
        
        Runtime -- O(nlg(n)) -- This runs in time proptional to nlg(n) because
        we call removeMin n times and it takes a max of lg(n) time to run it.
        The functions used here and there running times are below.

        buildheap -- O(n)
        removeMin -- O(nlg(n))
        reverse -- O(n)
        '''

        if lst:
            self.buildHeap(lst)
        prevSize = self.size
        for index in range(self.size, 0, -1):
            min = self.array[1]
            self.array[1] = self.array[index]
            self.array[index] = min
            self.size -= 1
            self.heapifyDown()
        self.size = prevSize
        for low in range(1,(self.size + 2) // 2):
            self.swap(low, (self.size + 1) - low)
        return self.array[1:self.size + 1]

    def leftChild(self, index):
        '''
        left child is 2 * index if rooted at 1 index.
        INPUT:
            index: Index our our data point in the array
        OUTPUT:
            The index of the leftChild.
        '''

        return index * 2
    
    def rightChild(self, index):
        '''
        right child is 2 index + 1 if rooted at 1 index.
        INPUT:
            index: Index our our data point in the array
        OUTPUT:
            The index of the rightChild.
        '''

        return index * 2 + 1
    
    def parent(self, index):
        '''
        parent is index // 2 if rooted at 1 index.
        INPUT:
            index: Index our our data point in the array
        OUTPUT:
            The index of the parent.
        '''

        return index // 2
    
    def __str__(self):
        '''
        This function helps us represent our heap in a string. It will show
        us the size, capacity, and the data in the array.
        INPUT: None
        OUTPUT:
            String representation of our (min)heap.
        '''

        string = 'Size is : ' + str(self.size) + '\nCapacity is : ' + str(self.capacity)
        string += '\nArray : ' + str(self.array)
        self.buildTree()
        string += '\n\n' + str(self.tree)
        return string
