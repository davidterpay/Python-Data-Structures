from btreenode import BTreeNode
from datapair import DataPair
import sys
sys.path.append('../')
from Queues.Queue import Queue
'''
Written by David Terpay
This is a BTree class that I built. BTrees are a type of tree but are not a 
binary tree. BTrees are especially useful when you are storing data that needs
quick lookup times and when a hash table won't work. Many social media
companies use BTrees are their backend way to store profiles. The orders of the
BTrees can get into the hundred making lookup times run in logm(n) time where
m is the order of the tree. Below I listed all major properties of BTrees.

BTree properties: 
A BTree of order m is an m-way tree.
All keys within a node are ordered.
All leaves contain no more than m - 1 keys.
All internal nodes have exactly one more child than keys.
Root node can be a leaf or have [2, m] children (because the only way to add a node is to grow).
All non-root nodes have [ceiling(m/2), m] children.
All leaves are on the same level.
Order tells us how many keys can be in a node.
    # of keys = m - 1 
How big is a BTree going to get? 
    BTree is shorter than AVL:
        AVL has 2 children → h = log2(n).
        BTree has m children → h = logm(n).
2 ciel(m / 2) ^ h - 1 = minimum number of keys in a btree of height h and order m
m ^ (h + 1) - 1 = max number of keys in a btree of height h and order m
'''

class BTree():
    def __init__(self, order, root = None):
        '''
        We will keep track of the order and root of our btree
        '''

        self.order = order
        self.root = BTreeNode(self.order)

    def insert(self, key, value):
        '''
        Since we insert only at a leaf node, we must first find the correct leaf node
        by binary searching the children stored in the current node we are looking at.
        Once we find the child, we recurse to it, and then we insert the new datapair object
        through binary searching the index we need to insert and then inserting. We also have
        to check if our node is too large in which we then have to split it as given to use
        by the btree properties mentioned in the btree.py file.
        '''

        datapair = DataPair(key, value)
        self.__insert(self.root, datapair)
        if self.root.isFull():
            newRoot = BTreeNode(self.order)
            newRoot.children.append(self.root)
            self.split(newRoot, 0)
            self.root = newRoot

    def __insert(self, node, datapair):
        '''
        Since we insert only at a leaf node, we must first find the correct leaf node 
        by binary searching the children stored in the current node we are looking at.
        Once we find the child, we recurse to it, and then we insert the new datapair object 
        through binary searching the index we need to insert and then inserting. We also have
        to check if our node is too large in which we then have to split it as given to use
        by the btree properties mentioned in the btree.py file.
        INPUT:
            Node: Current node we are looking at
            datapair: New datapair object we are inserting
        OUTPUT:
            BTree with a new datapair object in a node.
        '''

        if node.isLeaf():
            node.insertDataPair(datapair)
        else:
            childIndex = node.binarySearch(0, len(node) - 1, datapair)
            self.__insert(node.children[childIndex], datapair)
            if node.children[childIndex].isFull():
                self.split(node, childIndex)

    def split(self, parent, childIndex):
        '''
        Insert a pointer into parent's children which will point to the
        new right node. The new right node is empty at this point.
        Insert the mid element from the child into its new position in the
        parent's elements. At this point the median is still in the child.
        Now we want to copy over the elements (and children) to the right
        of the child median into the new right node, and make sure the left
        node only has the elements (and children) to the left of the child
        median.
        '''

        #Child we are looking at
        child = parent.children[childIndex]

        #median of the childs array
        median = (len(child) - 1) // 2
        midChild = len(child) // 2
        #median element
        dataSplit = child.data[median]

        left = BTreeNode(self.order, child.data[0:median])
        right = BTreeNode(self.order, child.data[median + 1: len(child)])
        if not child.isLeaf():
            left.children = child.children[0 : midChild + 1]
            right.children = child.children[midChild + 1: len(child.children)]
        parent.data.insert(childIndex, dataSplit)
        parent.children[childIndex] = left
        if childIndex == len(parent) - 1:
            parent.children.append(right)
        else:
            parent.children.insert(childIndex + 1, right)

    def find(self, key):
        '''
        Find is quite simple. First we binary search the current node to see if our
        keys is in the node. If the key is in the node, return the value stored in 
        that DataPair object. Otherwise, we have to find the child we would visit with 
        the given key. Once we find the index of the child using binarysearch once again,
        we recurse into find once again and repeat the steps. However, if we are a leaf node, 
        and our key is not in the node, then it cannot possibly exist in our BTree so we
        simply return None. We use the helper function __find here.
        INPUT:
            key: Key that needs to be found
        OUTPUT:
            Value in our datapair object with the corresponding key.
        
        '''

        return self.__find(self.root, key)
    
    def __find(self, node, key):
        '''
        Find is quite simple. First we binary search the current node to see if our
        keys is in the node. If the key is in the node, return the value stored in
        that DataPair object. Otherwise, we have to find the child we would visit with
        the given key. Once we find the index of the child using binarysearch once again,
        we recurse into find once again and repeat the steps. However, if we are a leaf node,
        and our key is not in the node, then it cannot possibly exist in our BTree so we
        simply return None.
        INPUT:
            node: Current node we are looking at
            key: Key we are trying to find
        OUTPUT:
            Value stored in the datapair object with the given key (if it exists)
        '''

        found = node.find(key)
        if found != None:
            return node.data[found].getValue()
        else:
            if not node.isLeaf():
                childIndex = node.binarySearch(0, len(node) - 1, DataPair(key, 'value'))
                return self.__find(node.children[childIndex], key)
            else:
                return None

    def __str__(self):
        '''
        String representation of our BTree
        '''

        string = ''
        queue = Queue()
        queue.enque(self.root)
        queue.enque(1)
        while not queue.isEmpty():
            node = queue.deque()
            if not node.isLeaf():
                for child in node.children:
                    queue.enque(child)
                queue.enque(1)
            while node != 1:
                string += f'Data: {str([pair.key for pair in node.data])}' + '   '
                node = queue.deque()
            string += '\n\n'
        return string
