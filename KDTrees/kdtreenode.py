import sys
sys.path.append('../')
from Binary_Tree.treenode import TreeNode
class KDTreeNode(TreeNode):
    def __init__(self, data, dim):
        super().__init__(data)
        self.__dimensionDiscriminator = dim
    
    def getDimDis(self):
        return self.__dimensionDiscriminator
    
    def setDimDis(self, data):
        self.__dimensionDiscriminator = data
    
    def __str__(self):
        '''
        This function will give us a string representation of our treenode. 
        This will allow us to print each of the nodes if we want to print a tree.
        '''

        string = super().__str__()
        string += f'\nDimension Discriminator: {self.__dimensionDiscriminator}'
        return string
