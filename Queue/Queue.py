import sys
sys.path.append('../')
from Linked_List import LinkedList

'''
This is my implementation of a queue. A queue is a first in - first out data structure.
Think of the queue as a line at Starbucks. The first person to get in line is the first person to get served; The last
person in line is the last to be served. I used a doubly linked list as the the back end data structure to hold the data. 
To check out the implementation of the linked list, look at the Linked_List folder. I utilized a linked list
class that I previously created.
'''

class Queue():
    def __init__(self, head = None):
        '''
        A constructor for our queue.
        INPUT:
            head: Head of a chain of nodes (if applicable).
        OUTPUT:
            Queue
            
        We defined one class variables:
        queue = A linked list, that is composed of variables such as size, nodes, and functionality that
        can be seen in the linked list folder. The queue can automatically be initialized from an existing 
        chain of nodes. Check out initializer() in the linked list class.
        '''

        self.queue = LinkedList.LinkedList(head)

    def enque(self, data):
        '''
        This function will appened a new node onto our queue. It appends it to the end of our stack
        INPUT:
            data = Data to be stored
        OUTPUT:
            queue with new node at the end
        Runtime : O(1) -- Enque runs in constant time because all we are doing is appending a new node
        to the back of our stack or our linked list. This takes constant time because we are using a doubly 
        linked list as our linked list.
        '''

        self.queue.addBack(data)

    def deque(self):
        '''
        This function will delete a node from the front of our queue.
        INPUT: None
        OUTPUT:
            The data that will be deleted
        Runtime : O(1) -- deque runs in constant time because all we are doing is deleting a existing node
        from the front of our queue or our linked list. This takes constant time.
        '''

        data = self.queue.head.getData()
        self.queue.removeFront()
        return data

    def size(self):
        '''
        This function will return the size of our queue.
        INPUT: None
        OUTPUT:
            The size of our queue
        Runtime : O(1) -- Size in constant time because all we are doing is returning a variable from the linked
        list class. This is a instance variable part of the linked list class. It does not take time to find the
        length of the linked list because we keep track of it through out the lifecycle of the linked list.
        '''

        return self.queue.length

    def isEmpty(self):
        '''
        This function will check if our queue is empty
        INPUT: None
        OUTPUT:
            True if empty. False if not empty
        Runtime : O(1) -- isEmpty runs in constant time because all we are doing is checking whether our length
        is 0. This is a instance variable part of the linked list class. It does not take time to find the
        length of the linked list because we keep track of it through out the lifecycle of the linked list.
        '''

        return self.queue.length == 0

    def peek(self):
        '''
        This function will return the first data point in our queue. It does not return the node, rather just the
        data. It also does not remove the node from the list.
        INPUT: None
        OUTPUT:
            Data in the first node.
        Runtime : O(1) -- Peek runs in constant time because all we are doing is returning the data held in
        the first most node aka the head.
        '''

        return None if self.queue.head is None else self.queue.head.getData()

    def __len__(self):
        '''
        This function will return the size of our queue. It uses the
        len() from the linked list class.
        INPUT: None
        OUTPUT:
            The size of our queue
        Runtime : O(1) -- Size in constant time because all we are doing is returning a instance variable from the linked
        list class. This is a instance variable part of the linked list class. It does not take time to find the
        length of the linked list because we keep track of it through out the lifecycle of the linked list.
        '''

        return len(self.queue)

    def __str__(self):
        '''
        This function will give us a string representation of our queue.
        INPUT: None
        OUTPUT:
            String representation of our queue
        Runtime : O(n) -- This runs in time proportional to n because we are
        iterating through every node in our linked list. This costs O(n) time.
        '''

        node = self.queue.head
        num = 1
        string = '\n\t------------ FRONT ------------'
        while(node is not None):
            string += f"\nNode : {str(num)}" + f'\n{str(node)}'
            node = node.getNext()

            num += 1
        string += '\n\t----------- BACK -----------\n'
        return string
