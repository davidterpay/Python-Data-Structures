import sys
sys.path.append('../')
from Linked_List import LinkedList

'''
This is my implementation of a stack. A stack is a first in - last out data structure.
Think of the stack as a stack of books. Once you put the first book down and place others on top,
you have to remove each of the books on top of the first book to get to the first book.
I used a doubly linked list as the the back end data structure to hold the data. 
To check out the implementation of the linked list, look at the Linked_List folder. I utilized a linked list
class that I previously created.
'''


class Stack():
    def __init__(self, head=None):
        '''
        A constructor for our stack.

        INPUT:
            head: Head of a chain of nodes (if applicable).
        OUTPUT:
            Stack

        We defined one class variables:
        stack = A linked list, that is composed of variables such as size, nodes, 
        and functionality that can be seen in the linked list folder. 
        The head variable can automatically be initialized from an 
        existing chain of nodes. Check out initializer() in the linked list class.
        '''

        self.stack = LinkedList.LinkedList(head)

    def push(self, data):
        '''
        This function will appened a new node onto our stack.
        INPUT:
            data = Data to be stored
        OUTPUT:
            Stack with new node on top

        Runtime : O(1) -- Push runs in constant time because all 
        we are doing is appending a new node to the front of our stack or our linked list. 
        This takes constant time.
        '''

        self.stack.addFront(data)

    def pop(self):
        '''
        This function will delete a node from our stack.
        INPUT: None
        OUTPUT:
            The data that will be deleted

        Runtime : O(1) -- Pop runs in constant time because all we are doing 
        is deleting a existing node from the front of our stack or our linked list. 
        This takes constant time.
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

        Runtime : O(1) -- isEmpty runs in constant time because all we are 
        doing is checking whether our length is 0. This is a instance variable 
        part of the linked list class. It does not take time to find the
        length of the linked list because we keep track of it through out 
        the lifecycle of the linked list.
        '''

        return self.stack.length == 0

    def size(self):
        '''
        This function will return the size of our stack.
        INPUT: None
        OUTPUT:
            The size of our stack

        Runtime : O(1) -- Size in constant time because all we are doing 
        is returning a variable from the linked list class. This is a instance 
        variable part of the linked list class. It does not take time to find 
        the length of the linked list because we keep track of it through out 
        the lifecycle of the linked list.
        '''

        return self.stack.length

    def peek(self):
        '''
        This function will return the first data point in our stack. 
        It does not return the node, rather just the
        data.
        INPUT: None
        OUTPUT:
            Data in the top node.

        Runtime : O(1) -- Peek runs in constant time because all we are doing 
        is returning the data held in the top most node aka the head.
        '''
        return None if self.isEmpty() else self.stack.head.getData()

    def __len__(self):
        '''
        This function will return the size of our stack. It allows us 
        to use len() on this class
        INPUT: None
        OUTPUT:
            The size of our stack

        Runtime : O(1) -- Size in constant time because all we are doing 
        is returning a variable from the linked list class. This is a instance 
        variable part of the linked list class. It does not take time to find the
        length of the linked list because we keep track of it through out 
        the lifecycle of the linked list.
        '''

        return len(self.stack)

    def __str__(self):
        '''
        This function will give us a string representation of our stack.
        INPUT: None
        OUTPUT:
            String representation of our stack

        Runtime : O(n) -- This runs in time proportional to n because we are
        iterating through every node in our linked list. This costs O(n) time.
        '''
        node = self.stack.head
        num = 1
        string = '\n\t------------ TOP ------------'
        while(node is not None):
            string += f"\nNode : {str(num)}" + f'\n{str(node)}'
            node = node.getNext()

            num += 1
        string += '\n\t----------- BOTTOM -----------\n'
        return string
