'''
Written by David Terpay
Disjoint sets are a collection of sets that have a representative element within each set.
Disjoint sets are a huge part of graph theory and are vital to graphs' backend implementations.
Some of the functionality we see in a data structure such as this is makeset, find, and union.
In this implementation, I decided to union by size to ensure that the average runtime does not
get worse. In addition, this class will implement a path compression algorithm when calling find
to effectively make the height of the tree negligible. Disjoint sets are implemented using
arrays, but are visualized at uptrees.
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
    def __init__(self, lst):
        '''
        We only need to keep track of the array in a disjoint set. Each element 
        can be mapped to an integer.
        '''

        self.array = lst
    
    
