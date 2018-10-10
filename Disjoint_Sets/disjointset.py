import sys
sys.path.append('../')
from Disjoint_Sets import datanode
import random
'''
Written by David Terpay
Disjoint sets are a collection of sets that have a representative element within each set.
Disjoint sets are a huge part of graph theory and are vital to graphs' backend implementations.
Some of the functionality we see in a data structure such as this is makeset, find, and union.
In this implementation, I decided to union by size to ensure that the average runtime does not
get worse. In addition, this class will implement a path compression algorithm when calling find
to effectively make the height of the tree negligible. Disjoint sets are implemented using
arrays, but are visualized using uptrees.
For example:
We might have the collection of sets and representative elements as follows:
c = {0,1,2,3}, {4,5,6}, {7,8,9}

let the first element in each set be the representative element.
in that case

array = [-4,0,2,2,-3,4,5,-3,7,8]
NOTE: we store the negative of the size of each uptree in the representative element for a set.
would give us a structure like this
^   ^   ^
|   |   |
0   4   7
|   |   |
1   5   8
|   |   |
2   6   9
|
3
'''
class DisjointSet():
    def __init__(self, lst = None):
        '''
        We only need to keep track of the array in a disjoint set. Each element 
        can be mapped to an integer.
        '''
        self.array = []
        if lst:
            self.array = [datanode.DataNode(data) for data in lst]

    def insertelements(self, x):
        '''
        This function will insert x number of new items into our array.
        It automatically initializes the values store in each additional index
        to -1. This means that we are at the representative element.
        INPUT:
            x: New number of elements to be inserted into our disjoint set.
        OUTPUT:
            x addition items in our array.
        '''

        self.array.extend([datanode.DataNode(random.randint(-10,10)) for __ in range(x)])

    def union(self, set1, set2):
        '''
        When we union two sets, we first make sure that we have to root of 
        the sets. Once we have the root we check which set is more negative (since
        we are smart unioning by the size of each set). We also have to make sure
        we collect the new size of the set by adding the contents of the two sets 
        together. 
        INPUT:
            set1: First set
            set2: Second set
        OUTPUT:
            Smart unioned set.
        '''

        set1 = self.find(set1)
        set2 = self.find(set2)
        if set1 == set2:
            return
        newSize = self.array[set1].index + self.array[set2].index
        if self.array[set1].index <= self.array[set2].index:
            self.array[set2].index = set1
            self.array[set1].index = newSize
        else:
            self.array[set1].index = set2
            self.array[set2].index = newSize

    def find(self, position):
        '''
        Find is simple. If at our index we have a negative vlaue, then we
        are at the representative element. Otherwise, we have to search find
        again with the index stored at the current indexes value in our array.
        Additionally, when we are returning, we set the value of array[position] to 
        be the index. This helps significantly compress the path and allows 
        our runtime to be iterated log2() which is close enough to O(1) that we 
        can assume that our find function runs in O(1) time.
        INPUT:
            position: Position of the element in our disjoint set we are trying to 
                find the index of the representative element in our set.
        OUTPUT:
            Index of the representative element.
        '''

        if self.array[position].index < 0:
            return position
        index = self.find(self.array[position].index)
        self.array[position].index = index
        return index

    def size(self, index):
        '''
        This function will return the size of our uptree or set. First
        we find the index and then simply multiply by the -1 and return
        INPUT:
            index: index of the set we are looking at
        OUTPUT:
            size of the set or uptree
        '''

        return -1 * self.array[self.find(index)].index
    
    def upTree(self, index):
        '''
        This is a simple function that will show us the uptree for a 
        given index or set.
        INPUT:
            index: Index of the set we want
        OUTPUT:
            String uptree
        '''

        string = ''
        while self.array[index].index > -1:
            string = f'\n^\n|\n{self.array[index].data}' + string
            index = self.array[index].index
        string = f'\n^\n|\n{self.array[index].data}' + string
        return string

    def __str__(self):
        '''
        Overloading the str operator to give us a string representation of 
        our disjoint set. 
        '''

        return f'Size : {len(self)}\n\nArray : {[data.data for data in self.array]}'
    
    def __len__(self):
        '''
        Overloading the len operator to give us a length representation of 
        our disjoint set. 
        '''
        
        return len(self.array)