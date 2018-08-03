from Linked_List import Node
'''
DESCRIPTION:
This is a simple doubly Linked List class written by David Terpay. I implemented
the most simple data structure ADT with easy to difficult ranging functionality. 
Test cases and other practice problems will be written in a different file (probably main).

I choose problems from Stanford's "Linked List Problems" by Nick Parlante 
(http://cslibrary.stanford.edu/105/LinkedListProblems.pdf). While 
his solutions are written in C, I figured a translation to python would be handy.
I would like to note that not every function found there is found in this PDF. 
I choose based on interesting the questions were to me. I built more functionality 
off a few of them such as the reverse() function in which you can now input a 
lower bound and upper bound and our reverse function will reverse solely in that interval. 
In addition to this, I also took some problems from UIUC's CS225 Data Structures 
and Algorithms. You can check out that awesome class here (https://courses.engr.illinois.edu/cs225/sp2018/).
'''


class LinkedList:
    '''
    DESCRIPTION:
    We have our linked list class. I use a node class that was defined outside this class.
    See node.py for documentation on the Node class.
    '''

    '''
    On to the functionality of the linked list class
    '''

    def __init__(self, head = None):
        '''
        A constructor for our linked list class.

        INPUT: 
            head: Head of a chain of nodes (if applicable).
        OUTPUT: 
            linked list

        We defined three class variables:
        head = The start of the linked list
        tail = The end of the linked list
        length = The length of the linked list
        '''

        if head is not None:
            self.head = head
            self.tail = None
            self.length = 0
            self.initialize()
        else:
            self.head = None
            self.tail = None
            self.length = 0

    def initialize(self):
        '''
        Wrapper function to the constructor that will help create 
        a linked list from an existing chain of nodes.

        INPUT: None
        OUTPUT: 
            Linked List with head, tail and length reinitialized
        
        Runtime : O(n) -- This runs in time proportional to n because we are 
        iterating through every single node until we hit None. n is proportional to
        the amount of data
        '''

        node = self.head
        while node.getNext() is not None:
            node = node.getNext()
            self.length += 1
        self.tail = node
        self.length += 1

    def addFront(self, data):
        '''
        Adding a node to the front of our list.
        Case 1: There are no nodes
            Insert and make head and tail.
        Case 2: There is one+ node
            Insert and make head.

        INPUT: 
            data: Data that we want to our linked list
        OUTPUT: 
            A linked list with a new appended head.

        Runtime : O(1) -- This runs in constant time because we are 
        simply changing a few pointers.
        '''

        node = Node.Node(data)
        if self.head is None:
            node.setNext(None)
            node.setPrev(None)
            self.head = self.tail = node
        else:
            node.setNext(self.head)
            self.head.setPrev(node)
            self.head = node
        self.length += 1
    
    def stack(self,*args):
        '''
        Wrapper function that allows you to input as many numbers as you want
        into this func and add it to the linked list. Appends each number
        to the front. This acts as a stack in terms of first in - last out where last 
        refers to the tail of the list. This function is similar to the queue function.

        INPUT: 
            args: tuple or list of many data points to be inserted into a linked list.
        OUTPUT: 
            Stacked Linked list
        
        Runtime : O(n) -- This runs in time proportional to n because we are 
        iterating through every single node in our list. n is proportional to
        the amount of data that is in args
        '''

        for number in args:
            self.addFront(number)

    def addBack(self, data):
        '''
        Adding a node to the back of our list.
        Case 1: There are no nodes
            Insert and make head and tail.
        Case 2: There is one+ node 
            Insert and make tail.

        INPUT: 
            data: Data that we want to add to our linked list
        OUTPUT: 
            A linked list with a new appended tail.
        '''
        
        if self.head is None:
            self.addFront(data)
        else:
            node = Node.Node(data)
            node.setPrev(self.tail)
            node.setNext(None)
            self.tail.setNext(node)
            self.tail = node
            self.length += 1

    def insertNth(self, n, data):
        '''
        Allows you to insert a node into linked list at an 
        index that you choose. This is zero indexed.

        INPUT: 
            n: position that we want to insert the node at
            data: Data that we want to 
        OUTPUT: 
            A linked list with a newly inserted node
        '''

        if n <= 0:
            self.addFront(data)
        elif n >= self.length - 1:
            self.addBack(data)
        else:
            prev = self.get(n - 1)
            next = prev.getNext()
            newNode = Node.Node(data)
            newNode.setPrev(prev)
            newNode.setNext(next)
            if next is not None:
                next.setPrev(newNode)
            prev.setNext(newNode)
    
    def insertSorted(self, data):
        '''
        This function will insert our new node into sorted order.
        *** This assumes that our linked list is sorted ***

        INPUT: 
            data: Data that we want to 
        OUTPUT: 
            A linked list with a newly inserted node.
        
        Runtime : O(n) -- This runs in time proportional to n because we are 
        iterating through our list until we find the correct position to insert.
        Worst case is O(n) which means we have to insert at the very back, while 
        best case is O(1) which means we simply insert at the front.
        '''

        for index in range(self.length):
            if self.get(index).getData() > data:
                self.insertNth(index, data)
                return
        self.addBack(data)

    def queue(self, *args):
        '''
        Wrapper function that allows you to input as many numbers as you want
        into this func and add it to the linked list. Appends each number to 
        the back. Acts as a first in - first out in respect with the head of 
        our linked list being the first node.

        INPUT: 
            args: tuple or list of many data points to be inserted into a linked list.
        OUTPUT: 
            Queued Linked list
        
        Runtime : O(n) -- This runs in time proportional to n because we are 
        iterating through every single node in our list. n is proportional to
        the amount of data that is in args
        '''

        for number in args:
            self.addBack(number)
    
    def removeFront(self):
        '''
        Removing a node from the front of a linked list.
        Case 1: No nodes exist
            Do nothing
        Case 2: There is one node
            Delete the single node and decrement the length
        Case 3: Multiple nodes
            Delete head and set new head to be head->next

        INPUT: None
        OUTPUT: 
            Linked list with one less node and a new head

        Runtime : O(1) -- This runs in constant time because we are 
        simply changing a few pointers.
        '''

        if self.head is None:
            return
        elif self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            nextNode = self.head.getNext()
            nextNode.setPrev(None)
            self.head = nextNode
        self.length -= 1

    def removeBack(self):
        '''
        Removing a node from the front of a linked list.
        Case 1: No nodes exist
            Do nothing
        Case 2: There is one node
            Delete the single node and decrement the length
        Case 3: Multiple nodes
            Delete tail and set new tail to be tail->prev
        
        INPUT: None
        OUTPUT: 
            Linked list with one less node and a new tail

        Runtime : O(1) -- This runs in constant time because we are 
        simply changing a few pointers.
        '''

        if self.head is None or self.head == self.tail:
            self.removeFront()
        else:
            prevNode = self.tail.getPrev()
            prevNode.setNext(None)
            self.tail = prevNode
            self.length -= 1

    def insertList(self,lst):
        '''
        This adds functionality to make a list into a linked list.
        INPUT:
            lst: List of nodes
        OUTPUT:
            Linked list with nodes in order of the list.

        '''
        
        for node in lst:
            self.addFront(node)

    def get(self, index):
        '''
        Return a certain node based on a inputed index
        INPUT:
            index = Index of the position of the node that we want
        OUTPUT:
            The node in that index or None

        Runtime : O(n) -- This runs in time proportional to n because we are 
        iterating through our list until we find the correct position to collect.
        Worst case is O(n) which means we have to collect at the very back, while 
        best case is O(1) which means we simply collect at the front.
        '''

        position = 0
        node = self.head
        while(node is not None and position != index):
            node = node.getNext()
            position += 1
        return node

    def count(self,data):
        '''
        Counts the number of times a given int occurs in a list
        INPUT: None
        OUTPUT:
            Number of occurances

        Runtime : O(n) -- This runs in time proportional to n because we are 
        iterating through our list to tally up how many occurances we see.
        '''

        count = 0
        node = self.head
        while node is not None:
            if node.getData() == data:
                count += 1
            node = node.getNext()
        return count

    def reverse(self,low, upper):
        '''
        This function will reverse a linked list based on inputed indices. It 
        does take in two parameters. Yes it takes care of 
        reversing both the next and previous pointers since it is doubly linked.
        INPUT: 
            low: lower bound of the list
            upper: upper bound of the list
        OUTPUT: 
            Reverses this instance of the linked list between the two indices
        
        Runtime : O(n) -- This runs in time proportional to n because we are 
        utilizing our get function to collect the nodes in the range (low to high).
        We cannot get around the our runtime to a smaller one because searching 
        for a node in a linked list costs O(n) time. Runtime might be slightly better 
        if the range is smaller but on the average case it will not change.
        '''

        if self.head == self.tail or self.head is None or low == upper:
            return
        else:
            if upper > self.length - 1:
                upper = self.length - 1
            if low < 0:
                low = 0
            previousStart = self.get(low).getPrev()
            endNext = self.get(upper).getNext()
            prev = self.get(low).getPrev()
            curr = self.get(low)
            high = self.get(upper)
            temp = curr.getNext()
            curr.setNext(endNext)
            curr.setPrev(temp)
            if endNext is not None:
                endNext.setPrev(curr)
            if upper == self.length - 1:
                self.tail = curr
            prev = curr
            curr = temp
            while(curr != high):
                temp = curr.getNext()
                curr.setNext(prev)
                curr.setPrev(temp)
                prev = curr
                curr = temp
            curr.setNext(prev)
            curr.setPrev(previousStart)
            if previousStart is not None:
                previousStart.setNext(curr)
            if low == 0:
                self.head = curr
            
    def reverseList(self):
        '''
        This is a wrapper for the reverse function that will simply
        reverse an entire linked list. This function uses the reverse function
        INPUT: 
            low: lower bound of the list
            upper: upper bound of the list
        OUTPUT: 
            Reverses this instance of the linked list between the two indices
        
        Runtime : O(n) -- This runs in time proportional to n because we are 
        utilizing our get function to collect the nodes in the range (low to high).
        We cannot get around the our runtime to a smaller one because searching 
        for a node in a linked list costs O(n) time.
        '''

        self.reverse(0,self.length - 1)

    def reverseNth(self, n):
        '''
        Reverses blocks of length n in the current List.
        INPUT: 
            n: The length of the block
            upper: upper bound of the list
        OUTPUT: 
            Reverses blocks of length n in the list
        
        Runtime : O(n ^ 2) -- This runs in time proportional to n ^ 2 because we are 
        utilizing our get function to collect the nodes in the range (low to high).
        We cannot get around the our runtime to a smaller one because searching 
        for a node in a linked list costs O(n) time. The runtime might vary depending
        on the block length but as a whole it runs on worst case O(n ^ 2) due to the fact
        that we iterate through every item in the range and the calls we make to the
        reverse function which runs in O(n).
        '''

        if n >= self.length:
            self.reverse(0,self.length - 1)
        else:
            for index in range(0,self.length, n):
                if index < self.length - 1:
                    self.reverse(index, index + n - 1)
    
    def waterfall(self):
        '''
        Modifies the List using the waterfall algorithm.
        Every other node (starting from the second one) is removed from the List, 
        but appended at the back, becoming the new tail. 
        This continues until the next thing to be removed is either the 
        tail (not necessarily the original tail!) or NULL. You may NOT allocate new ListNodes. 
        Note that since the tail should be continuously updated, some nodes will be moved more than once.
        INPUT: None
        OUTPUT: 
            Modified linked list as given by the rules of the waterfall algorithm
        
        Runtime : O(n) -- This runs in time proportional to n because we are 
        iterating through every node in our linked list. This costs O(n) time.
        '''

        if self.head == self.tail or self.head == None:
            return
        else:
            curr = self.head.getNext()
            prev = self.head
            while(curr is not self.tail):
                next = curr.getNext()
                prev.setNext(next)
                if next is not None:
                    next.setPrev(prev)
                curr.setNext(None)
                self.tail.setNext(curr)
                curr.setPrev(self.tail)
                self.tail = curr
                prev = next
                curr = next.getNext()

    def deleteDups(self):
        '''
        This function will pretty much delete duplicates in our
        linked list. I think the naive way of approaching this 
        problem would be to iterate through the list twice. However,
        since this is a linked list, Im not sure whether using a
        set would have a much better runtime. Either way, I am going 
        to use a set because I think it is more intuitive and more applicable
        for normal lists.
        INPUT: None
        OUTPUT: 
            Linked list with no duplicate ints, strings, etc.
        
        Runtime : O(n) -- This runs in time proportional to n because we are 
        iterating through every node in our linked list. This costs O(n) time.
        '''

        newSet = set(self.toList())
        dictionary = {key: False for key in newSet}
        self.length = len(newSet)
        current = self.head
        while current is not None:
            data = current.getData()
            if dictionary[data]: # This means we have already seen this point
                next = current.getNext()
                prev = current.getPrev()
                if prev is not None:
                    prev.setNext(next)
                if next is not None:
                    next.setPrev(prev)
            else:
                dictionary[data] = True

            if current.getNext() is None:
                self.tail = current

            current = current.getNext()

    def mergesort(self, other):
        '''
        Merge Sort — Algorithm Details

        Merge Sort is a recursive sorting algorithm that behaves as follows:

        Base Case: A list of length 1 is sorted. Return.
        Recursive Case:
        Split the current list into two smaller, more manageable parts
        Sort the two halves (this should be a recursive call)
        Merge the two sorted halves back together into a single list
        In other words, Merge Sort operates on the principle of breaking 
        the problem into smaller and smaller pieces, and merging the sorted, 
        smaller lists together to finally end up at a completely sorted list.

        I guess the implementation of mergesort is dependent on how you 
        write the linked list class. In my case, I have to pass in self 
        when initially calling mergesort so that our function has a list
        to work with. This function or any of the helper functions does not
        allocate any new nodes. We do create a few pointers by creating new lists,
        but these new lists are using the same nodes that were used previously. 
        Although python does not have a way to check memory allocation (that i am
        aware of), these functions could be translated to languages such as 
        C++ and be tested under valgrind for leaks.
        INPUT: 
            other: This is a pointer to the head of a linked list
        OUTPUT: 
            Sorted linked list using mergesort
        
        Runtime : O(nlg(n)) -- This runs in time proportional to nlg(n) it takes lg(n) time 
        to split the entire linked list into two halves until the length is 1, and it takes
        n time to merge together all of the lists back together. Although mergesort does
        allocate some new list pointers, it does not allocate new nodes. This is due to the 
        way I implemented split and merge (which are seen below).
        '''

        if other.length == 1:
            return
        else:
            mid = other.length // 2
            right = other.split(mid)
            left = other
            self.mergesort(left)
            self.mergesort(right)
            self.merge(right)
   
    def split(self, splitPoint):
        '''
        This function will take in the current instances list and 
        split it based on the splitPoint. It returns a new list but does not
        allocate new nodes. The new list returned points to the second half of the
        new split list. The current instance will still maintain the first half. This is
        important to note otherwise mergesort might appear to be confusing.
        This does change the length of our current list as well as
        the pointers to the head and the tail.
        INPUT:
            splitPoint: The index where we want to split the list.
        OUTPUT: 
            Second half of the split linked list.
        
        Runtime : O(n) -- This runs in time proportional to n because we are 
        iterating through every node (possibly) in our linked list. This costs O(n) time.
        runtime could be better if the splitPoint is early on.
        '''

        if splitPoint >= self.length:
            return
        else:
            node = self.get(splitPoint - 1)
            next = node.getNext()
            next.setPrev(None)
            node.setNext(None)
            self.tail = node
            self.length = splitPoint
            newLst = LinkedList(next)
            return newLst

    def merge(self, other):
        '''
        Helper function to merge two sorted and independent sequences of linked memory.
        The result should be a single sequence that is itself sorted.
        This function SHOULD NOT create ANY new List objects.
        This function does not allocate new memory or create new nodes. This function merges on
        to the callers list.
        INPUT:
            other: The other linked list we want to merge with this instance of our list.
        OUTPUT: 
            A linked list merged with other in sorted order.
        
        Runtime : O(n) -- This runs in time proportional to n because we are 
        iterating through every node (possibly) in our linked list and in 
        the other linked list. This costs O(n) time.
        '''

        firstLst = self.head
        secondLst = other.head
        while secondLst is not None:
            data = secondLst.getData()
            if firstLst.getData() > data:
                if firstLst == self.head:
                    temp = secondLst.getNext()
                    secondLst.setNext(firstLst)
                    secondLst.setPrev(None)
                    firstLst.setPrev(secondLst)
                    self.head = secondLst
                    secondLst = temp
                else:
                    temp = secondLst.getNext()
                    secondLst.setPrev(firstLst.getPrev())
                    secondLst.setNext(firstLst)
                    firstLst.getPrev().setNext(secondLst)
                    firstLst.setPrev(secondLst)
                    secondLst = temp
                self.length += 1
            else:
                if firstLst == self.tail:
                    temp = secondLst.getNext()
                    firstLst.setNext(secondLst)
                    secondLst.setPrev(firstLst)
                    secondLst.setNext(None)
                    self.tail = secondLst
                    secondLst = temp
                    self.length += 1
                else:
                    firstLst = firstLst.getNext()
        del other

    def bubblesort(self):
        '''
        This algorithm checks the next node whether its data is larger than the current node.
        If the data in the current node is larger, then it swaps them. It does this process
        until it hits the end of our list at which point we know that the largest 
        data point has to be at the end of our linked list. Therefore we can now simply
        search the length of the linked list - 1 until we get to a length of 1 at which point 
        we know we have a sorted list because an element of length one is sorted. This algorithm
        runs in O(n^2) and takes up O(1) space since we do not use addition space.
        INPUT: None
        OUTPUT: 
            Sorted linked list using the bubblesort algorithm
        
        Runtime : O(n ^ 2) -- This runs in time proportional to n ^ 2 because we are 
        iterating through every node in our linked list and in each iteration of a node we
        go through the linked list for every node (aka double for loop). It costs O(n) time 
        to go through node in our list, but since we go through the linked list for every node it
        becomes O(n ^ 2).
        '''

        if self.head is None or self.length == 1:
            return
        elif self.head.getData() > self.tail.getData() and self.length == 2:
                self.swap(self.head, self.tail)
        else:
            bubblelength = self.length
            for _ in range(self.length - 1):
                current = next = self.get(0)
                for __ in range(bubblelength - 1):
                    next = current.getNext()
                    if current.getData() > next.getData():
                        self.swap(current,next)
                    else:
                        current = next
                bubblelength -= 1

    def swap(self,prev,next):
        '''
        This is a helper function for bubblesort and mergesort.
        I would like to note that this function only deals with nodes
        that are right next to each other. This will not correctly swap 
        nodes that are not sequential.
        INPUT:
            prev: The previous node which will be swapped with next
            next: The next node which will be swapped with prev
        OUTPUT: 
            The linked list will swap the two nodes
        
        Runtime : O(1) -- This runs in constant time because we are 
        simply changing a few pointers.
        '''

        if prev == self.head:
            self.head = next
        if next == self.tail:
            self.tail = prev
        if prev.getPrev() is not None:
            prev.getPrev().setNext(next)
        if next.getNext() is not None:
            next.getNext().setPrev(prev)
        prev.setNext(next.getNext())
        next.setPrev(prev.getPrev())
        prev.setPrev(next)
        next.setNext(prev)
    
    def toList(self):
        '''
        This function converts our linked list into a python list. Extracts only
        the data from each node.
        INPUT: None
        OUTPUT: 
            List of all of our data
        
        Runtime : O(n) -- This runs in time proportional to n because we are 
        iterating through every node in our linked list. This costs O(n) time.
        '''

        lst = []
        node = self.head
        while(node is not None):
            lst.append(node.getData())
            node = node.getNext()
        return lst

    def __del__(self):
        '''
        This function will remove all of the nodes in our linked list.
        INPUT: None
        OUTPUT: 
            deletes our linked list and all memory attached with it
        
        Runtime : O(n) -- This runs in time proportional to n because we are 
        iterating through every node in our linked list. This costs O(n) time.
        '''

        while(self.head is not None):
            self.removeFront()
    
    def __len__(self):
        '''
        Returns the length of the linked list
        INPUT: None
        OUTPUT: 
            Length of our linked list
        
        Runtime : O(1) -- This runs in constant time because we are simply returning an
        attribute to of this class
        '''

        return self.length
    
    def __str__(self):
        '''
        This function will give us a string representation of our linked list.
        INPUT: None
        OUTPUT: 
            String representation of our linked list
        
        Runtime : O(n) -- This runs in time proportional to n because we are 
        iterating through every node in our linked list. This costs O(n) time.
        '''

        node = self.head
        num = 1
        string = ''
        while(node is not None):
            string += f"\nNode : {str(num)}" + f'\n{str(node)}'
            node = node.getNext()
            if node is not None:
                string += '\n\tn | \t^ p\n\te | \t| r\n\tx | \t| e\n\tt V \t| v\n'
            num += 1
        return string
