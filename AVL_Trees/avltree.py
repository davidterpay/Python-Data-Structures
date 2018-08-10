import sys
sys.path.append('../')
from Binary_Tree.binarytree import BinarySearchTree
from Binary_Tree.treenode import TreeNode
import random

'''
Written by David Terpay
This will demonstrate some of the functionality we might see in a AVL Tree. This
will include rotations, insertions, and removals that keep the balance factor
of the entire tree within an absolute value of 1. This ensures that our runtime
of insertion, removal, and find are O(lg(n)). We will inherit the BST class that 
I previously created. You can check out the code and documentation in the Binary_Tree
folder in this repository.

ANY SORT OF RANGE OR ANY SORT OF NEAREST NEIGHBOR USE AVL
AVL trees are good for when you want range based searches and need to find the nearest 
neighbor. They however are not good for big data because we have to store all of the 
data in main memory (Btree is better in that case). Additionally, AVL trees are a
step up from arrays in terms of big - O but still are not ideal in the sense that
we should see a runtime of O(1) which can be found in hashing.

For more reference you can check out this website.
https://en.wikipedia.org/wiki/AVL_tree 
'''

class AVLTree(BinarySearchTree):
    def __init__(self, root = None):
        '''
        Since we are techincally a binary search tree, we will simply
        call and inherit the functionality of the BST class and overwrite
        some its functions such as insert, removal, etc. here.
        '''

        self.root = root

    def buildRandomTree(self, number, low, high):
        '''
        Builds a random tree with inputed high bound and low bound.
        '''

        self.insertPythonList(random.randint(low,high) for _ in range(number))

    def rebalance(self, node):
        '''
        This is a wrapper function that constanly rebalances our AVL tree.
        It checks if the height of the right subtree - left subtree is 
        greater than or equal to abs(2). If so it will call the correct rotation
        based on the side of imbalance and type of imbalance on that side. There
        are four different rotations
        
        1. leftRotation - This is when we have a stick on which is orientated towards
        the right. We have to turn this stick into a mountain.
        a.
        3
            \\
                5
                    \\
                        10
        
        b.
                5   
            //      \\
        3               10

        2. rightLeftRotation - This is when we have a elbow and we need to rotate it to the
        right and then left. We first turn it into a stick and then make it into a mountain
        a.
        3
            \\
                10
            //
            5
        
        b.
        3
            \\
                5
                    \\
                        10
        
        c.
                5   
            //      \\
        3               10

        3. rightRotation - This is when we have a stick which is orientated towards the left.
        We have to turn this stick into a mountain
        a.
                        10
                    //
                5
            //
        3

        b.
                5   
            //      \\
        3               10

        4. leftRightRotation - This is when we have a elbow and we need to rotate it to the
        left and then left. We first turn it into a stick and then make it into a mountain
        a.
                10
            //
        3
        \\
            5
        
        b.

                        10
                    //
                5
            //
        3
    
        c.
                5   
            //      \\
        3               10

        Runtime -- O(1) -- The runtime of rebalance is constant since all we are doing is changing
        pointers. NOTE: the runtime is also dependent on the height of the tree since we are calling
        balancefactor(). We could change the runtime by making the height a member of each node.
        '''

        heightBalance = self.balanceFactor(node)
        heightBalanceRight = self.balanceFactor(node.getRight()) if node.getRight() else 0
        heightBalanceLeft = self.balanceFactor(node.getLeft()) if node.getLeft() else 0
        if heightBalance >= 2:
            if heightBalanceRight == 1:
                self.leftRotation(node)
            else:
                self.rightLeftRotation(node)
        if heightBalance <= -2:
            if heightBalanceLeft == 1:
                self.leftRightRotation(node)
            else:
                self.rightRotation(node)

    def leftRotation(self, node):
        '''
        1. leftRotation - This is when we have a stick on which is orientated towards
        the right. We have to turn this stick into a mountain.
        a.
        3
            \\
                5
                    \\
                        10
        
        b.
                5   
            //      \\
        3               10
        '''

        right = node.getRight()
        if node == self.root:
            self.root = right
            right.setParent(None)
        else:
            parent = node.getParent()
            if parent.getRight() == node:
                parent.setRight(right)
            else:
                parent.setLeft(right)
            right.setParent(parent)
        node.setParent(right)
        node.setRight(right.getLeft())
        if right.getLeft():
            right.getLeft().setParent(node)
        right.setLeft(node)
    
    def leftRightRotation(self, node):
        '''
        4. leftRightRotation - This is when we have a elbow and we need to rotate it to the
        left and then left. We first turn it into a stick and then make it into a mountain
        a.
                10
            //
        3
        \\
            5
        
        b.

                        10
                    //
                5
            //
        3
    
        c.
                5   
            //      \\
        3               10
        '''

        left = node.getLeft()
        leftRight = left.getRight()
        left.setRight(leftRight.getLeft())
        if leftRight.getLeft():
            leftRight.getLeft().setParent(left)
        leftRight.setLeft(left)
        left.setParent(leftRight)
        leftRight.setParent(node)
        node.setLeft(leftRight)
        self.rightRotation(node)

    def rightRotation(self, node):
        '''
        3. rightRotation - This is when we have a stick which is orientated towards the left.
        We have to turn this stick into a mountain
        a.
                        10
                    //
                5
            //
        3

        b.
                5   
            //      \\
        3               10
        '''

        left = node.getLeft()
        if node == self.root:
            self.root = left
            left.setParent(None)
        else:
            parent = node.getParent()
            if parent.getRight() == node:
                parent.setRight(left)
            else:
                parent.setLeft(left)
            left.setParent(parent)
        node.setParent(left)
        node.setLeft(left.getRight())
        if left.getRight():
            left.getRight().setParent(node)
        left.setRight(node)

    def rightLeftRotation(self, node):
        '''
        2. rightLeftRotation - This is when we have a elbow and we need to rotate it to the
        right and then left. We first turn it into a stick and then make it into a mountain
        a.
        3
            \\
                10
            //
            5
        
        b.
        3
            \\
                5
                    \\
                        10
        
        c.
                5   
            //      \\
        3               10
        '''

        right = node.getRight()
        rightLeft = right.getLeft()
        right.setLeft(rightLeft.getRight())
        if rightLeft.getRight():
            rightLeft.getRight().setParent(right)
        node.setRight(rightLeft)
        rightLeft.setParent(node)
        rightLeft.setRight(right)
        right.setParent(rightLeft)
        self.leftRotation(node)

    def insert(self, data):
        '''
        This function will insert a node into our AVL tree. We overwrite 
        the existing insert function that can be found in the BST class. This
        function will not insert into our AVL tree if the data already exists
        in our tree. This insertion runs in O(lg(n)) time and is guaranteed to 
        allow search and removal to run in the lg(n) time. This function uses the
        helper function __insert().
        INPUT:
            data: Data that will be inserted into our list.
        OUTPUT:
            AVL tree with new node node in it
        
        Runtime -- O(lg(n)) -- This runs in time proportional to lg(n) 
        because our AVL tree automatically rebalances itself after each call to insert. 
        In other words, as we get deeper into the AVL tree, we keep track of the path 
        we take and once we insert into the tree we go back up the tree and check 
        for any imbalances. If any do exist, we automatically rebalance and fix the 
        tree to maintain a balance factor less than abs(2).
        '''

        if not self.root:
            self.root = TreeNode(data)
        else:
            self.__insert(data, self.root)
        
    def __insert(self, data, node):
        '''
        This function will insert a node into our AVL tree.  This
        function will not insert into our AVL tree if the data already exists
        in our tree. This insertion runs in O(lg(n)) time and is guaranteed to 
        allow search and removal to run in the lg(n) time. 
        INPUT:
            data: Data that will be inserted into our list.
            node: Node helps keep track of the path we take and allows us
                to get to a leaf node.
        OUTPUT:
            AVL tree with new node node in it
        
        Runtime -- O(lg(n)) -- This runs in time proportional to lg(n) because our AVL 
        tree automatically rebalances itself after each call to insert. In other words,
        as we get deeper into the AVL tree, we keep track of the path we take and once we
        insert into the tree we go back up the tree and check for any imbalances.
        If any do exist, we automatically rebalance and fix the tree to maintain a balance
        factor less than abs(2).
        '''

        if data == node.getData():
            return # no duplicates
        elif data > node.getData():
            if node.getRight():
                self.__insert(data, node.getRight())
            else:
                newNode = TreeNode(data)
                newNode.setParent(node)
                node.setRight(newNode)
        else:
            if node.getLeft():
                self.__insert(data, node.getLeft())
            else:
                newNode = TreeNode(data)
                newNode.setParent(node)
                node.setLeft(newNode)
        self.rebalance(node) # rebalacing the tree from leaf upwards if necessary
    
    def insertList(self, *args):
        '''
        This is a wrapper function that allows us to insert as many numbers
        into our AVL tree as we want

        Runtime -- O(nlg(n)) -- Since there are n data points and it takes lg(n) time
        to insert each it will take n * lg(n) time to insert all of the data points.
        '''

        for num in args:
            self.insert(num)
        
    def insertPythonList(self, lst):
        '''
        This is a wrapper function that allows us to insert a list of data
        into our AVL tree.

        Runtime -- O(nlg(n)) -- Since there are n data points and it takes lg(n) time
        to insert each it will take n * lg(n) time to insert all of the data points.
        '''

        for num in lst:
            self.insert(num)
    
    def remove(self, data):
        '''
        This function will remove a data point from a AVL tree given that it
        exists in the tree. Since our tree is guarateed to have a balance factor
        between -1 and 1, the removal will run in time proportional to lg(n). Once 
        we remove a node from the AVL tree we go back up the path we took and we rebalance
        if we need to. We use the __remove() helper function here.
        INPUT:
            data: Data to be removed
        OUTPUT:
            AVL tree that does not have the data point in it.
        
        Runtime -- O(lg(n)) -- Since our tree is fairly balanced, removal will run in 
        time proportional to lg(n).
        '''

        self.__remove(data, self.root)
    
    def __remove(self, data, node):
        '''
        This function will remove a data point from a AVL tree given that it
        exists in the tree. Since our tree is guarateed to have a balance factor
        between -1 and 1, the removal will run in time proportional to lg(n). Once 
        we remove a node from the AVL tree we go back up the path we took and we rebalance
        if we need to.
        INPUT:
            data: Data to be removed
            node: Node helps us keep track of the path we take and helps us get to the node
                we need to remove
        OUTPUT:
            AVL tree that does not have the data point in it.
        
        Runtime -- O(lg(n)) -- Since our tree is fairly balanced, removal will run in 
        time proportional to lg(n).
        '''

        if not node:
            return
        if node.getData() == data:
            parent = node.getParent()
            if node.getRight() and node.getLeft():  # two child removal
                self.twoChildRemoval(node)
            elif not node.getLeft() and node.getRight() or not node.getRight() and node.getLeft():  # one child removal
                self.oneChildRemoval(node)
            else:
                if parent:
                    if parent.getRight() == node:
                        parent.setRight(None)
                    else:
                        parent.setLeft(None)
                else:
                    self.root = None
        elif node.getData() > data:
            self.__remove(data, node.getLeft())
        else:
            self.__remove(data, node.getRight())
        self.rebalance(node)
    
    def twoChildRemoval(self, node):
        '''
        This is a helper function that will remove a node that has two children. What
        you are supposted to do is pretty much find the in order predecessor (which is
        simply the largest node in the left subtree) and replace it with the current 
        node and then delete the node.
        INPUT:
            node: Node that needs to be deleted
        OUTPUT:
            AVL tree with that data point removed
        '''

        parent = node.getParent()
        iop = self.findIOP(node.getLeft())
        node.getRight().setParent(iop)
        prevHead = iop.getParent()
        node.getLeft().setParent(iop)
        iop.setRight(node.getRight())
        if prevHead.getData() != node.getData():
            iop.getParent().setRight(iop.getLeft())
            if iop.getLeft():
                iop.getLeft().setParent(iop.getParent())
            iop.setLeft(node.getLeft())
        if not parent:
            self.root = iop
            iop.setParent(None)
        else:
            iop.setParent(parent)
            if parent.getLeft() and parent.getLeft().getData() == node.getData():
                parent.setLeft(iop)
            else:
                parent.setRight(iop)
    
    def oneChildRemoval(self, node):
        '''
        This is a helper function that will remove a node that has one child. What
        you are supposted to do is pretty much find the child that exists and swap it
        with the current node that will be deleted.
        INPUT:
            node: Node that needs to be deleted
        OUTPUT:
            AVL tree with that data point removed
        '''

        parent = node.getParent()
        right = node.getRight()
        left = node.getLeft()
        if parent:
            if parent.getRight() == node:
                if right:
                    parent.setRight(right)
                    right.setParent(parent)
                else:
                    parent.setRight(left)
                    left.setParent(parent)
            else:
                if right:
                    parent.setLeft(right)
                    right.setParent(parent)
                else:
                    parent.setLeft(left)
                    left.setParent(parent)
