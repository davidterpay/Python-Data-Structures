from datapair import DataPair
'''
Our BTree will be made up of BTreeNodes which contain a order, 
some data, and children. All of the data within the node will be sorted
and children will be sorted in such a way that we can quickly find the children
'''
class BTreeNode():
    def __init__(self, order, data = None, children = None):
        '''
        In our btreenode we will keep track of three things:
        the data, the children, and the order of our node.
        '''

        self.orderm = order
        self.data = data or []
        self.children = children or []
    
    def insert(self, key, value):
        '''
        Since the BTree must maintain data that is sorted within our nodes,
        we have to ensure that we insert into a tree in such a way that our data
        remains sorted. This function will simply create a new datapair object,
        with a given key and value, and will insert it into this node.
        We use __insertSorted as a helper function here.
        INPUT:
            key: Key we will look at when traversing through our btree node
            value: value we will store
        OUTPUT:
            New data member in our node.
        
        Runtime - O(lg(n)) - Since we are binary searching for the correct index to
        insert at, our runtime is proportional to lg(n).
        '''

        newDataPair = DataPair(key, value)
        if len(self) == 0:
            self.data.insert(0, newDataPair)
        else:
            self.__insertSorted(0, len(self.data) - 1, newDataPair)
    
    def insertList(self, lst):
        '''
        This function will allow user to input a list of datapair objects and 
        will sort them and initialize the data member of this node.
        INPUT:
            lst: List of DataPair objects
        OUTPUT:
            New node
        
        Runtime - O(nlg(n)) - Since mergesort takes O(nlg(n)) time our
        insert list will also run in that time.
        '''

        self.mergesort(lst)

    def mergesort(self, lst):
        '''
        Merge sort is a sorting algorithm that splits the list of numbers
        if half and then rebuilds the array upward. Once the size of each list
        is = 1, we know that the list is sorted. Next, we simply merge two sorted 
        lists and return the list. This is premise behind merge sort.
        INPUT:
            lst: List of data
        OUTPUT:
            Sorted list of data
        
        Runtime - O(nlg(n)) - Since it takes O(lg(n)) to divide the list and O(n) to
        rebuild our array, our algorithm takes a total of O(nlg(n)) time.
        '''

        self.data = self.__mergesort(lst)
    
    def __mergesort(self, lst):
        '''
        Merge sort is a sorting algorithm that splits the list of numbers
        if half and then rebuilds the array upward. Once the size of each list
        is = 1, we know that the list is sorted. Next, we simply merge two sorted
        lists and return the list. This is premise behind merge sort.
        '''

        if len(lst) == 1:
            return lst
        else:
            median = (len(lst)) // 2
            left = lst[0: median]
            right = lst[median: len(lst)]
            newLeft = self.__mergesort(left)
            newRight = self.__mergesort(right)
            return self.__merge(newLeft, newRight)

    def __merge(self, leftlist, rightlist):
        '''
        Helper function to merge leftlist and rightlist into
        one single list. It is assumed that the two lists are sorted.
        '''

        ctr = 0
        while len(rightlist) != 0:
            data = rightlist[0]
            if ctr > len(leftlist) - 1:
                leftlist.append(data)
                rightlist.pop(0)
            elif data < leftlist[ctr] or data == leftlist[ctr]:
                leftlist.insert(ctr, data)
                rightlist.pop(0)
            else:
                ctr += 1
        return leftlist       

    def __insertSorted(self, left, right, datapair):
        '''
        Helps binary search our treenode to find the correct index to 
        insert datapair into and then adds it into the node.
        INPUT:
            datapair: Datapair object we are looking to insert
            left: Left index
            right: Right index
        OUTPUT:
            New data member in our node.
        '''

        if left >= right:
            if datapair > self.data[left]:
                if right == len(self):
                    self.data.append(datapair)
                else:
                    self.data.insert(right + 1, datapair)
            else:
                self.data.insert(left, datapair)
        if left < right:
            median = (left + right) // 2
            if datapair < self.data[median]:
                self.__insertSorted(left, median - 1, datapair)
            elif datapair > self.data[median]:
                self.__insertSorted(median + 1, right, datapair)
            else:
                self.data.insert(median, datapair)
    
    def __str__(self):
        '''
        Overloading str to give us a string representation of our 
        btreenode.
        '''

        string = '-'*(10 * len(self)) + '\n\nData: | '
        for data in self.data:
            string += str(data.key) + ' | '
        string += '\n\nOrder: ' + str(self.orderm) + '\n\n'
        string += '-'*(10 * len(self))
        return string
    
    def __len__(self):
        '''
        Overloading the len() operator. Simply returns the length of our 
        data
        '''

        return len(self.data)

