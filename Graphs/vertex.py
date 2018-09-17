import sys
sys.path.append('../')
from Linked_List import LinkedList
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
        # self.__edges = LinkedList.LinkedList(listEdge)
    
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
    
    # def addEdge(self, data):
    #     '''
    #     Adding an edge to the linked list of edges. Remember this stores a pointer
    #     to the actual object as seen in the linked list of edges in the graph class.
    #     '''

    #     self.__edges.addFront(data)
    
    # def degree(self):
    #     '''
    #     Returns the magnitude of the set of incident edges.
    #     '''

    #     return len(self.__edges)
    
    def __str__(self):
        string = f'Data: {self.__data}'
        return string