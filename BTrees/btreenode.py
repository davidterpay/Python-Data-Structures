'''
Need a key: value data structure, need to store the data struc and 
the children of each of the nodes
'''
class BTreeNode():
    def __init__(self, data = None, children = None):
        self.data = data
        self.children = None