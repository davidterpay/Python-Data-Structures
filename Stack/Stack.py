from Linked_List import LinkedList
'''
This is my implementation of a stack. A stack is a first in - last out data structure.
Think of the stack as a stack of books. Once you put the first book down and place others on top,
you have to remove each of the books on top of the first book to get to the first book.

I used a linked list as the the back end data structure to hold the data. To check out the 
implementation of the linked list, look at the Linked List folder. I utilized the linked list
class that I previously created.
'''
class Stack(LinkedList.LinkedList):
    def __init__(self,head = None):  
        '''
        A constructor for our stack.

        INPUT: 
            head: Head of a chain of nodes (if applicable).
        OUTPUT: 
            Stack

        We defined one class variables:
        stack = A linked list, that is composed of variables such as size, nodes, and functionality that 
        can be seen if we check out the linked list folder. The head variable can automatically 
        initialize a stack from an existing chain of nodes. Check out initializer() in the linked list class.
        '''

        self.stack = super.__init__(head)
    
    def push(self, data):
        '''
        This function will appened a new node onto our stack.
        INPUT:
            data = Data to be stored
        OUTPUT:
            Stack with new node on top
        
        Runtime : O(1) -- Push runs in constant time because all we are doing is appending a new node
        to the front of our stack or our linked list. This takes constant time.
        
        '''

        self.stack.addFront(data)
    
    def pop(self):
        '''
        This function will delete a node from our stack.
        INPUT: None
        OUTPUT:
            The data that will be deleted
        
        Runtime : O(1) -- Pop runs in constant time because all we are doing is deleting a existing node
        from the front of our stack or our linked list. This takes constant time.
        '''

        topData = self.peek()
        self.stack.removeFront()
        return topData

    def isEmpty(self):
        '''
        This function will check if our stack is empty
        INPUT: None
        OUTPUT:
            True if empty. False if not empty
        
        Runtime : O(1) -- Pop runs in constant time because all we are doing is checking whether our length 
        is 0. This is a instance variable part of the linked list class. It does not take time to find the 
        length of the linked list because we keep track of it through out the lifecycle of the linked list.
        '''

        return len(self.stack) == 0
    
    def size(self):
        '''
        This function will return the size of our stack.
        INPUT: None
        OUTPUT:
            The size of our stack
        
        Runtime : O(1) -- Size in constant time because all we are doing is returning a variable from the linked
        list class. This is a instance variable part of the linked list class. It does not take time to find the 
        length of the linked list because we keep track of it through out the lifecycle of the linked list.
        '''

        return len(self.stack)

    def peek(self):
        '''
        This function will return the first data point in our stack. It does not return the node, rather just the
        data.
        INPUT: None
        OUTPUT:
            Data in the top node.
        
        Runtime : O(1) -- Peek runs in constant time because all we are doing is returning the data held in
        the top most node aka the head. 
        '''

        return self.stack.get(0)
