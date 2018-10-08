'''
Written by: David Terpay
This is a class I built to help with abstracting data, all this will do is 
put the data in a class to allow operator overloading in the actual data's
class.
'''
class DataNode():
    def __init__(self, data):
        '''
        We will be keeping track of two things, the data and the index stored
        in the node. This helps keep track of the uptrees. Check the disjointset.py
        to see how this class is used
        '''
        
        self.data = data
        self.index = -1