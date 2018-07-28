from Linked_List import LinkedList
'''
This is my implementation of a stack. A stack is a first in - last out data structure.
Think of the stack as a stack of books. Once you put the first book down and place others on top,
you have to remove each of the books on top of the first book to get to the first book.

I used a linked list as the the back end data structure to hold the data. To check out the 
implementation of the linked list, look at the Linked List folder. I utilized the linked list
class that I previously created.
'''
class Stack():
    def __init__(self):  # work on this
        self.stack = LinkedList.LinkedList()
    
    def push(self, data):  # work on this
        self.stack.addFront(data)
    
    def pop(self): # work on this
        pass

    def isEmpty(self):  # work on this
        pass
    
    def size(self):  # work on this
        pass

    def peek(self):  # work on this
        pass
