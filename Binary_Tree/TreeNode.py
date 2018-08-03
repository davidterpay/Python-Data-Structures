
'''
Written by David Terpay

This class will be used to build our tree. This class will makeup the nodes
that we will find in our trees. We will include instance varaiables such as
data, parent, left, and right. These variables will all be encapsulated.
This is a matter of practice and not necessity. All else will be calculated 
in the BinaryTree.py file.
'''

class TreeNode():
    def __init__(self, data = None, parent = None, left = None, right = None):
        '''
        This is the constructor for our tree node. As mentioned earlier we will be
        keeping track of the parent, left child, right child, and data. This will create
        a instance of a treenode.
        INPUT:
            data = Data that we will store in our treenode.
            parent = The parent of this treenode.
            left = The left child of our treenode.
            right = The right child of our treenode.
        OUTPUT:
            A treenode instance.
        '''

        self.__parent = parent
        self.__left = left
        self.__right = right
        self.__data = data
    
    def getParent(self):
        '''
        Since our variables are encapsulated, this function will allow us to directly access the
        parent of our node.
        '''

        return self.__parent
    
    def setParent(self, parent):
        '''
        Since our variables are encapsulated, this function will allow us to directly change the
        parent of our node.
        '''

        self.__parent = parent
    
    def getLeft(self):
        '''
        Since our variables are encapsulated, this function will allow us to directly access the
        left child.
        '''

        return self.__left

    def setLeft(self, left):
        '''
        Since our variables are encapsulated, this function will allow us to directly change the
        left child.
        '''

        self.__left = left
    
    def getRight(self):
        '''
        Since our variables are encapsulated, this function will allow us to directly access the
        right child.
        '''

        return self.__right

    def setRight(self, right):
        '''
        Since our variables are encapsulated, this function will allow us to directly change the
        left child.
        '''

        self.__right = right
    
    def getData(self):
        '''
        Since our variables are encapsulated, this function will allow us to directly access the
        data.
        '''

        return self.__data

    def setData(self, data):
        '''
        Since our variables are encapsulated, this function will allow us to directly change the
        data.
        '''

        self.__data = data
    
    def __str__(self):
        '''
        This function will give us a string representation of our treenode. This will allow us to
        print each of the nodes if we want to print a tree.
        '''
        
        leftData = None
        rightData = None
        parentData = None
        if self.__parent:
            parentData = self.__parent.getData()
        if self.__left:
            leftData = self.__left.getData()
        if self.__right:
            rightData = self.__right.getData()
        string = '-----------------\n' + \
            f'   Data: {self.__data}\n  Parent: {parentData}\n\n  LC \tRC \n  {leftData}\t{rightData}\n'
        string += '-----------------\n'
        return string
