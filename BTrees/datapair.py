'''
This is a simple data structure that holds a key and value.
We will use this data structure to make up the backend way we 
hold the data in our BTree.
'''
class DataPair():
    def __init__(self, key = None, value = None):
        '''
        A fancy key-value pair will make up our data in the BTree.
        INPUT:
            key: Key
            value: Value
        OUTPUT:
            DataPair
        '''

        self.key = key
        self.__value = value

    def setKey(self, key):
        '''
        Setter to set the key in our DataPair object.
        '''
        self.key = key

    def getValue(self):
        '''
        Getter to retrieve the value in our DataPair object.
        '''

        return self.__value

    def setValue(self, value):
        '''
        Setter to set the value in our DataPair object.
        '''
        
        self.__value = value

    def __lt__(self, other):
        '''
        We are overloading the less than operator to allow for less
        code and more accesibility
        INPUT:
            other: Other node we are comparing
        OUTPUT:
            True if this instance's key is smaller than other
        '''

        return self.key < other.key

    def __gt__(self, other):
        '''
        We are overloading the greater than operator to allow for less
        code and more accesibility
        INPUT:
            other: Other node we are comparing
        OUTPUT:
            True if this instance's key is greater than other
        '''

        return self.key > other.key

    def __eq__(self, other):
        '''
        We are overloading the equal to operator to allow for less
        code and more accesibility
        INPUT:
            other: Other node we are comparing
        OUTPUT:
            True if this instance's key is equal to other
        '''

        return self.key == other.key
    
    def __str__(self):
        '''
        String representation of our DataPair
        '''

        string = '---------\n\nKey: ' + str(self.key) + '\n\nValue: ' + str(self.__value) + '\n\n' + '---------'
        return string
