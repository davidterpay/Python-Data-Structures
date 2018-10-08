import sys
sys.path.append('../')
from Linked_List import LinkedList
import math
'''
Written by David Terpay
This is a class that will represent our vertex. 
Our vertex will hold two things:
    1. Data/key
    2. Linked list of pointers to edges
'''
class Vertex():
    def __init__(self, data, listEdge = None):
        '''
        Our vertex stores the data and a linked list of edges
        '''

        self.__data = data
        self.predecessor = None
        self.weight = math.inf
        self.__visited = False
    
    def setVisited(self, var):
        '''
        Setter for encapsulated data
        '''

        self.__visited = var
    
    def getVisited(self):
        '''
        Getter for encapsulated data
        '''

        return self.__visited

    def getData(self):
        '''
        Getter for encapsulated data
        '''
        
        return self.__data
    
    def setData(self, data):
        '''
        Setter for encapsulated data
        '''

        return self.__data
    
    def __lt__(self, other):
        return self.weight < other.weight

    def __gt__(self, other):
        return self.weight > other.weight

    def __str__(self):
        string = f'Data: {self.__data}'
        return string
