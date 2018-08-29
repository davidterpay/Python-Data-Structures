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