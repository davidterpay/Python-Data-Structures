'''
DESCRIPTION:
This is a simple doubly Linked List class written by David Terpay. I implemented
the most simlpe data structure ADT. Test cases and other practice problems will
be written in a different file (probably main).
'''

class Node:
        '''
        We have our node class. This class will allow for basic functionality.
        I specifically made the variables private so that I could encapsulate them.
        Setters and Getters are in place.
        '''

        def __init__(self, data=None, next=None, prev=None):
            '''
            Initializer that inputs data, next, and prev. These are all initized to none at first
            INPUT:
            data = entering the data we might be storing
            next = a pointer of sorts to the next node in the list
            prev = a pointer of sorts to the previous node in the list
            '''
            self.__data = data
            self.__next = next
            self.__prev = prev

        def getData(self):
            '''
            Return the encapsulated data
            '''
            return self.__data

        def setData(self, data):
            '''
            Set the encapsulated data to something new
            '''
            self.__data = data

        def getNext(self):
            '''
            Get the encapsulated next
            '''
            return self.__next

        def setNext(self, next):
            '''
            Set the encapsulated next to something new
            '''
            self.__next = next

        def getPrev(self):
            '''
            Get the encapsulated prev
            '''
            return self.__prev

        def setPrev(self, prev):
            '''
            Set the encapsulated prev to something new
            '''
            self.__prev = prev

        def __str__(self):
            '''
            Returns the string representation of the node instance
            '''
            nextData = None
            prevData = None
            if self.getNext() is not None:
                nextData = self.getNext().getData()
            if self.getPrev() is not None:
                prevData = self.getPrev().getData()
            box = '\n----------------------------------------------------'
            data = f"\nThis Node has the following attributes: \n\tdata: {self.getData()} \n\tnext data: {nextData} \n\tprev data: {prevData}"
            return box + data + box
