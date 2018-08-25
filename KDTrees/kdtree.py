import sys
sys.path.append('../')
from Binary_Tree.binarytree import BinarySearchTree
from Binary_Tree.treenode import TreeNode
from kdtreenode import KDTreeNode
from functools import reduce

'''
Written by David Terpay
A k-d tree is a generalization of a Binary Search Tree that supports 
nearest neighbor search in higher numbers of dimensions — for example, 
with 2-D or 3-D points, instead of only 1-D keys. A 1-D-tree (a k-d tree 
with k=1) is simply a binary search tree.

This is a KDTree class I wrote that includes some of the most important
functionality in CS as a whole. When I say that I am referencing range 
based queries and finding nearest neighbors to a data point. I 
inherited the binary search tree class I previously created 
since a KDTree is a type of BST. This allows for nearly all of the 
functionality found the super class (including traversals, depth, breadth first
searches, etc.). Since KDTrees are harder than most data structures, I will 
link the extremely helpful websites I found when I was building this class.

https://courses.engr.illinois.edu/cs225/sp2018/mps/5/
https://en.wikipedia.org/wiki/K-d_tree
https://www.cs.cmu.edu/~ckingsf/bioinfo-lectures/kdtrees.pdf
http://www.cs.cornell.edu/courses/cs4780/2015fa/web/lecturenotes/lecturenote16.html
'''

class KDTree(BinarySearchTree):
    def __init__(self, dimensions):
        '''
        This is a constructor that will give us a default, basic 
        KDTree. It will not create a nice sorted and relatively
        balanced KDtree. In order to get that, construct a KDTree, 
        and then simply insert a list into createBalancedTree() function.
        This will sort the list in multidimensional space using quickselect, 
        and will recursively construct your tree from your list which will
        be an attribute of the object --> points. There are three variables
        we will keep track of
            root = Will allow us to maintain our tree structure. We inherited
                the Binary Search Tree class as well as all of its useful 
                properties.
            
            points = A sorted list of points (if we called createBalancedTree),
                otherwise unsorted list.
            
            dimensions = The number of dimensions our data is in
        '''

        super().__init__()
        self.points = []
        self.dimensions = dimensions

    def insert(self, data):
        '''
        When we are inserting in a kdtree, we compare the values
        at a certain dimension and move left if the new data is smaller
        and right otherwise. Once we hit a node that does not have a right child
        or left child (depending on our data point value's) we insert there.
        INPUT:
            data: Data to be inserted.
        OUTPUT:
            A new node in our KDTree.

        Runtimee - O(h) - Our runtime is bounded by the height of our tree.
        if our tree is created by using the helper function createBalancedTree()
        then our runtime is going to be bounded by O(lg(n)) because our tree will be
        fairly balanced. However, without using this helpuer function our runtime can be
        as bad O(n) when our KDTree has a bery linked list like structure.
        '''

        if self.root:
            node = KDTreeNode(data, len(data))
            self.__insert(node, self.root, 0)
        else:
            self.root = KDTreeNode(data, 0)
            self.points.append(self.root)
        
    def __insert(self, newNode, node, dim):
        '''
        This is a helper function to insert.
        INPUT:
            newNode: New node to be inserted
            node: Current node we are recursing on
            dim: Dimension we are looking at
        OUTPUT:
            A new node in our KDTree.
        '''

        if self.smallerDimValue(newNode, node, dim):
            if node.getLeft():
                self.__insert(newNode, node.getLeft(), (dim + 1) % self.dimensions)
            else:
                newNode.setDimDis((dim + 1) % self.dimensions)
                newNode.setParent(node)
                node.setLeft(newNode)
                self.points.append(newNode)
        else:
            if node.getRight():
                self.__insert(newNode, node.getRight(), (dim + 1) % self.dimensions)
            else:
                newNode.setDimDis((dim + 1) % self.dimensions)
                node.setRight(newNode)
                newNode.setParent(node)
                self.points.append(newNode)

    def insertList(self, lst):
        '''
        This is a wrapper function that allows us to insert a list of nodes
        into our kdtree
        INPUT:
            lst: List of data we want to insert
        OUTPUT:
            KDTree we more nodes
        '''

        for data in lst:
            self.insert(data)

    def smallerDimValue(self, a, b, d):
        '''
        Determines if Point a is smaller than Point b in a given dimension d.
        INPUT:
            a: Point a
            b: Point B
            d: Dimesion d
        OUTPUT:
            True if a is smaller than b in a given dimension d. Else false
        '''
        
        return a.getData()[d] <= b.getData()[d]

    def remove(self, data):
        '''
        As stated by geeks for geeks
        1) If current node contains the point to be deleted
            If node to be deleted is a leaf node, simply delete it 
            (Same as BST Delete)
            If node to be deleted has right child as not NULL 
            (Different from BST)
                Find minimum of current node’s dimension in right subtree.
                Replace the node with above found minimum and 
                recursively delete minimum in right subtree.
            Else If node to be deleted has left child 
                as not NULL (Different from BST)
                Find minimum of current node’s dimension in left subtree.
                Replace the node with above found minimum and 
                recursively delete minimum in left subtree.
                Make new left subtree as right child of current node.
        2) If current doesn’t contain the point to be deleted
            If node to be deleted is smaller than current node on current dimension, 
            recur for left subtree.
            Else recur for right subtree.
        INPUT:
            data: Data to be removed
            node: Current we are looking at
            dim: Dimension
        OUTPUT:
            Removed node
        '''

        if self.root:
            self.__remove(data, self.root, 0)
        
    def __remove(self, data, node, dim):
        '''
        This is a helper function to remove. Read remove
        for more documentation on how to remove.
        '''

        if not node:
            return None
        if node.getData() == data:
            self.points.remove(node)
            parent = node.getParent()
            if node.getRight(): # right child exists
                findMin = self.findMin(node.getRight(), (node.getDimDis() + 1) % self.dimensions, node.getDimDis())
                node.setData(findMin.getData())
                right = self.__remove(node.getData(), node.getRight(), (node.getDimDis() + 1) % self.dimensions)
                if right:
                    right.setParent(node)
                node.setRight(right)
                self.points.append(node)
            elif node.getLeft(): # left child exists
                findMin = self.findMin(node.getLeft(), (node.getDimDis() + 1) % self.dimensions, node.getDimDis())
                node.setData(findMin.getData())
                right = self.__remove(node.getData(), node.getLeft(), (node.getDimDis() + 1) % self.dimensions)
                if right:
                    right.setParent(node)
                node.setRight(right)
                node.setLeft(None)
                self.points.append(node)
            else: # zero child
                node = None
            if not parent:
                self.root = node
        elif node.getData()[dim] < data[dim]:
            node.setRight(self.__remove(data, node.getRight(), (dim + 1) % self.dimensions))
        else:
            node.setLeft(self.__remove(data, node.getLeft(), (dim + 1) % self.dimensions))   
        return node
    
    def findMin(self, node, cd = 0, dim = 0):
        '''
        This is a helper function to remove that finds the smallest node
        value for a given dimension. It returns that node so that we can properly
        remove a tree node from our KDTree. 
        First we check if our dimension is equal to the dimension we need.
            if so then we check if there is a left child and recurse that way
            otherwise we return the node
        Second if our dimension is not equal, we have to return the minimum of the right, left
            and current node.

        Runtime - O(h) - Our runtime is really bounded by our height so we have to be
        careful how we build our tree (aka use createaBalancedTree).
        '''

        if not node:
            return None
        elif cd == dim:
            if node.getLeft():
                return self.findMin(node.getLeft(), (cd + 1) % self.dimensions, dim)
            else:
                return node
        else:
            cd += 1 % self.dimensions
            return self.minimum(dim, node, self.findMin(node.getLeft(), cd, dim), self.findMin(node.getRight(), cd, dim))

    def minimum(self, dimension, *args):
        '''
        This function is a helper function to remove that takes a list 
        of nodes and returns the node containing the smallest value 
        in a certain dimension.
        INPUT:
            dimension: Dimension we are looking at
            args: List of data
        OUTPUT:
            Node with the smallest value in a certain dimension.
        
        Runtime - O(n) - We have to traverse the entire list
        '''

        return reduce(lambda x,y: x if self.smallerDimValue(x,y,dimension) else y, [node for node in args if node])

    def find(self, data):
        '''
        At each level, we compare
        the data value's in that dimension vs. the node value's in that
        dimension and recurse accordingly.
        INPUT:
            data: Data we are trying to find
        OUTPUT:
            The node if it exists in the tree, otherwise none.
        
        Runtime - O(lg(n)) - If our tree is created using the createBalancedTree()
        function, then our search is more or less bounded by the height of our tree.
        However, if we randomly insert, we could end up getting a long linked list.
        In this case, runtime is more along the lines of O(n). However, average runtime
        is far better than that so we say a O(lg(n)) is appropriate.
        '''

        return self.__find(data, self.root, 0)
    
    def __find(self, data, node, dim):
        '''
        This is a helper function that helps us recurse through our
        k-dimensional tree to find our data. At each level, we compare
        the data value's in that dimension vs. the node value's in that
        dimension and recurse accordingly.
        INPUT:
            data: Data we are trying to find
            node: Current node we are recursing on
            dim: Dimension discriminator
        OUTPUT:
            The node if it exists in the tree, otherwise none.
        
        Runtime - O(lg(n)) - If our tree is created using the createBalancedTree()
        function, then our search is more or less bounded by the height of our tree.
        However, if we randomly insert, we could end up getting a long linked list.
        In this case, runtime is more along the lines of O(n). However, average runtime
        is far better than that so we say a O(lg(n)) is appropriate.
        '''

        if not node:
            return None
        if node.getData() == data:
            return node
        elif node.getData()[dim] < data[dim]:
            return self.__find(data, node.getRight(), (dim + 1) % self.dimensions)
        else:
            return self.__find(data, node.getLeft(), (dim + 1) % self.dimensions)

    def createBalancedTree(self, lst = None):
        '''
        KD-trees are created recursively; at any stage of the 
        construction, the median value in the current dimension 
        is selected and a node is created based on it. Then, all 
        the elements in the current subtree are divided up into 
        elements which are less than the median, or greater than the 
        median, and then the subtrees are created recursively. The 
        children pick the median in the next dimension, and repeat 
        until the entire set of inputs has been processed. Successive 
        levels of the tree split on increasing dimensions, modulo the 
        total number: a 3D tree will have levels split by dimension 0, 
        1, 2, 0, 1, 2, etc.
        INPUT:
            lst: List of data
        OUTPUT:
            List of data in sorted order
        '''

        if lst:
            data = self.quickselect(lst)
            self.root = self.__buildTree(0, len(data) - 1, data, 0)
            self.points = data
        else:
            self.points = self.quickselect()
            self.root = self.__buildTree(0, len(self.points) - 1, self.points, 0)
        return list(map(KDTreeNode.getData, self.points))

    def createLeafTree(self, lst = None):
        '''
        This is a function that will create a tree in which all
        of our data is stored in the leaf nodes. We will do so
        by first sorting our list of points, and then creating
        TreeNodes with only the splitting value within the node.
        When we reach the leaf nodes, we simply will add the kdtree
        nodes where ever necessary. MAKE SURE THE POINTS ARE
        SORTED BEFORE CALLING THIS OR ELSE THE FUNCTION WILL NOT WORK
        INPUT: None
        OUTPUT:
            Leaf Tree
        '''

        self.points = self.quickselect()
        self.root = self.__medianSplit(0, len(self) - 1, 0)
        self.__medianInsert(self.root, 0, len(self) - 1)
        return self.root
    
    def __medianInsert(self, node, left, right):
        '''
        This is a helper function to insert the actual KDTree nodes
        into our KDTree. It splits the points array and recursively inserts 
        each node where the in order predecessor would be placed. This
        effectively allows us to place our node in the correct location.
        INPUT:
            node: Current node we are recursing on. This variable helps keep
                track of where the data should be placed. So in short, we 
                have node and all we have to do is find this nodes IOP and
                insert there.
            left: Left index we are recursing on
            right: Right index we are recursing on
        OUTPUT:
            KDTree with all of its leaf nodes containing the actual data.
            All internal nodes are treeNodes while leaf nodes are specifically
            KDTreeNodes (Since they hold data of multiple dimensions).
        
        Runtime - O(nlg(n)) - Since there are n elements and since it takes
        approximately O(h) time to insert each node, our total runtime is 
        O(nlg(n)).
        '''

        if left <= right:
            median = (left + right + 1) // 2
            medianDataPoint = self.points[median]
            medianDataPoint.setRight(None)
            medianDataPoint.setLeft(None)
            medianDataPoint.setRight(None)
            self.__insertInorderPredecessor(node, medianDataPoint)
            self.__medianInsert(node.getLeft(), left, median - 1)
            self.__medianInsert(node.getRight(), median + 1, right)

    def __insertInorderPredecessor(self, node, data):
        '''
        This function will correctly insert our data into the variable 
        node's IOP
        INPUT:
            node: Node we are looking to find IOP of
            data: Data to be inserted
        OUTPUT:
            New node in KDTree.
        '''

        if node.getLeft():
            positionInsert = node.getLeft()
            while positionInsert.getRight():
                positionInsert = positionInsert.getRight()
            positionInsert.setRight(data)
            data.setParent(positionInsert)
        else:
            node.setLeft(data)
            data.setParent(node)

    def __medianSplit(self, left, right, dim):
        '''
        This function will build us a KDTree filled with TreeNodes
        (NOTE: these are not KDTreeNodes because they only carry 1-d data).
        It will build us all of our splitting points at each dimensions so that
        when we insert our actual data we will simply find the IOP of the node
        and insert the data there.
        INPUT:
            left: Left index we are recursing on
            right: Right index we are recursing on
            dim: Dimension we are looking at
        OUTPUT:
            KDTree with treenodes containing 1-d data that helps us create a tree
            where we can insert all data at the leaf nodes.
        '''

        if left > right:
            return
        median = (left + right + 1) // 2
        data = self.points[median].getData()[dim]
        root = TreeNode(data)
        left = self.__medianSplit(left, median - 1, (dim + 1) % self.dimensions)
        if left:
            left.setParent(root)
        right = self.__medianSplit(median + 1, right, (dim + 1) % self.dimensions)
        if right:
            left.setParent(root)
        root.setRight(right)
        root.setLeft(left)
        return root

    def __buildTree(self, left, right, lst, dim):
        '''
        Create a subroot based on the median of our points list and 
        then recurse on the indices between a though m−1 for its left subtree, 
        and m+1 through b  for its right subtree, using splitting 
        dimension (d+1) mod k.
        INPUT:
            left: Left most index we are splitting on
            right: Right most index we are splitting on
            lst: Lst of points
            dim: Dimension
        OUTPUT:
            Root of the new tree
        
        Runtime - O(n) - Since we have to recurse for every element in our list
        our runtime is bounded by the amount of data we have in it.
        '''

        if left > right:
            return
        median = (left + right + 1) // 2
        root = lst[median]
        root.setDimDis(dim)
        right = self.__buildTree(median + 1, right, lst, (dim + 1) % self.dimensions)
        if right:
            right.setParent(root)
        left = self.__buildTree(left, median - 1, lst, (dim + 1) % self.dimensions)
        if left:
            left.setParent(root)
        root.setRight(right)
        root.setLeft(left)
        return root

    def __sort(self, lst, left, right, dim):
        '''
        This helper function will sort the array using the 
        quickselect algorithm. We recursively sort the left and
        right sides of the array to give us a faster runtime than
        soemthing like bubblesort.
        INPUT:
            lst: List of data
            left: Left index we are sorting
            right: Right index we are sorting
            dim: Dimension we are sorting at
        OUTPUT:
            Sorted list of points in k-dimensions
        '''

        if left < right:
            median = (left + right + 1) // 2
            # We need pivot to correctly put median in the middle
            # So that we can properly sort the other dimensions and halves
            self.pivot(lst, left, right, median, dim)
            # Recursively sorting the right and left sides on the array
            self.__sort(lst, left, median - 1, (dim + 1) % self.dimensions)
            self.__sort(lst, median + 1, right, (dim + 1) % self.dimensions)
            return lst

    def pivot(self, lst, left, right, median, dim):
        '''
        This function will allow us to put the median in the correct 
        location in our array.
        INPUT:
            lst: List of data
            left: Left position of what we are traversing
            right: Right position of what we are traversing
            median: The median we are trying to put in correct place
            dim: Dimension we are sorting at
        OUTPUT:
            The median of the array will be correct.
        '''

        # We check if the partition is greater than or equal to median. If
        # so then we have to recur on the proper side.
        pivot = self.partition(left, right, lst, dim)
        if pivot != median:
            if pivot < median:
                self.pivot(lst, pivot + 1, right, median, dim)
            elif pivot > median:
                self.pivot(lst, left, pivot - 1, median,  dim)
        
    def partition(self, left, right, lst, dim):
        '''
        Partition is a helper function to quicksort that 
        checks the the final position in the array and finds all
        of the elements that are smaller to put them to the left. 
        Finally at the end, we swap the place of the final position
        or the very right element and put it in right after all of 
        the smallest elements. This means that all of the elements
        that are smaller than the right most element will be to the 
        left and all the larger elements will be to the right. This gives
        us a partially sorted array where the k-th position is
        in the correct place
        INPUT:
            left: The left position of the array we are partitioning
            right: The right position of the array we are partitioning
            lst: List of data
            dim: Dimension we are looking at
        OUTPUT:
            Partially sorted data where k-th element is in the correct place.
        
        Runtime - O(n) - Since we traverse the entire array, our runtime is O(n).
        '''

        low = left - 1
        for x in range(left, right):
            if self.smallerDimValue(lst[x], lst[right], dim):
                low += 1
                temp = lst[low]
                lst[low] = lst[x]
                lst[x] = temp
        low += 1
        temp = lst[right]
        lst[right] = lst[low]
        lst[low] = temp
        return low

    def quickselect(self, lst = None):
        '''
        Quickselect is a selection algorithm to find the 
        k-th smallest element in an unordered list. We use quickselect to
        sort and order our multidimensional data.
        For an understanding of how quickselect works, check out these websites
        https://www.geeksforgeeks.org/quickselect-algorithm/
        https://en.wikipedia.org/wiki/Quickselect
        INPUT:
            lst = lst to be sorted
        OUTPUT:
            Sorted list of k - dimensional data
        
        Runtime - O(nlg(n)) - Since the quickselect algorithm is very similar to 
        quicksort, and since we divide our problem in half every single time we
        try to find the median value to place in sorted order, our algorithm runs in time
        proportional to nlg(n). However, the runtime can be as poor as O(n^2).
        '''

        if lst:
            data = [KDTreeNode(value, 0) for value in lst]
            return self.__sort(data, 0, len(data) - 1, 0)
        else:
            return self.__sort(self.points, 0, len(self.points) - 1, 0)

    def shouldReplace(self, target, currBest, potential):
        '''
        Determines if a Point is closer to the target Point than another 
        reference Point. Takes three points: target, currentBest, and potential, 
        and returns whether or not potential is closer to target than currentBest.
        We are using Euclidean distance to compare k-dimensional points.
        INPUT:
            target = Query point
            currBest = Current best point
            potential = The potential new closest point
        OUTPUT:
            True if new point is closer, false if it is not
        '''

        potentialDistance = self.euclideanDistance(target, potential)
        currentDistance = self.euclideanDistance(target, currBest)
        return potentialDistance < currentDistance

    def euclideanDistance(self, first, second):
        '''
        This function will give us the euclidean distance between
        two points
        INPUT:
            first = first point
            second = second point
        OUTPUT:
            euclidean distance between the two points
        '''

        distance = 0
        for index, data in enumerate(first.getData()):
            distance += pow(data - second.getData()[index], 2)
        return pow(distance, 1/2)
    
    def splitPlaneDistance(self, target, current, currBest):
        '''
        This is a helper function to find nearest neighbor that 
        checks the current points distance from the spliting dimensions plane
        and returns true if it is smaller than the current radius of 
        the circle within which our point can exist. This function allows us to make
        sure we do not traverse through subtreees that could not possibly contain the 
        nearest neighbor hence dramatically increasing the average runtime of our 
        algorithm.
        INPUT:
            target = Query point
            current = Current (or parent node) which we are checking
            currBest = The current best node which will give us the radius we need
        OUTPUT:
            True if current points distance from the splitting plane is less
            than the current radius; false otherwise
        
        '''
        euclideanDistance = self.euclideanDistance(target,currBest)
        dimension = current.getDimDis()
        return euclideanDistance >= abs(target.getData()[dimension] - current.getData()[dimension])
    
    def findNearestNeighbor(self, target):
        '''
        The findNearestNeighbor() search is done in two steps: a 
        search to find the smallest hyperrectangle that contains 
        the target element, and then a back traversal to see if any 
        other hyperrectangle could contain a closer point, which may 
        be a point with smaller distance or a point with equal distance, 
        but a "smaller" point (as defined by operator< in the point class). 
        In the first step, you must recursively traverse down the tree, at each 
        level choosing the subtree which represents the region containing the 
        search element (another place to save some duplicate code?). When you 
        reach the lowest bounding hyperrectangle, then the corresponding node 
        is effectively the "current best" neighbor.However, it may be the case 
        that a better match exists outside of the containing hyperrectangle. 
        At then end of first step of the search, we start traversing back 
        up the kdtree to the parent node. The current best distance defines a 
        radius which contains the nearest neighbor. During the back-traversal 
        (i.e., stepping out of the recursive calls), you must first check if 
        the distance to the parent node is less than the current radius. If so, 
        then that distance now defines the radius, and we replace the "current best" 
        match. Next, it is necessary to check to see if the current splitting 
        plane's distance from search node is within the current radius. If so, then 
        the opposite subtree could contain a closer node, and must also be searched recursively.
        During the back-traversal, it is important to only check the subtrees that 
        are within the current radius, or else the efficiency of the kdtree is lost. If 
        the distance from the search node to the splitting plane is greater than the current 
        radius, then there cannot possibly be a better nearest neighbor in the subtree, 
        so the subtree can be skipped entirely.
        You can assume that findNearestNeighbor will only be called on a valid kd-tree.
        We use the __findNearNeighbor() helper function here.
        INPUT:
            target = The data point we are trying to find a match for
        OUTPUT:
            Node closet to the target point
        
        Runtime - O(lg(n)) - Since we are splitting the tree and HOPEFULLY 
        reecursing only one side of the tree, we are bounded by the height of 
        the tree which is ~ lg(n) ~ if we are creating a semi-balanced tree. However,
        there are many variables that go into the theoretical runtime. Because of that,
        we can get a runtime as bad as O(n) which is no better than running through all 
        of the points and finding a minimum that way. Average runtime is far better than
        O(n) however, and because of that it makes this algorithm very valuable once you are
        searching for a nearest neighbor in data bases that contain billions of data points.
        '''

        query = KDTreeNode(target, 0)
        return self.__findNearestNeighbor(0, query, self.root, self.root)

    def __findNearestNeighbor(self, dim, target, currBest, current):
        '''
        The first step is to check if we are a leaf node. If so, return the node.
        We can traverse through the tree and find the leaf node we want
        NOTE: If the child doesn't exist, we leave it be and do not recur
        Here we check if the current node is better than the childrens nodes we visited
        above. If so, we change the currentbest to current.
        Finally we check whether we need to visit the subtrees that are opposite
        We determine whether we visit based on the distance of the parent node's
        distance to the planes splitting dimensions line. I will link a demonstration
        to lessen the confusion. If we are less than the euclidean distance, then we
        have to visit the side of the tree that we did not recur on.
        INPUT:
            dim = Dimension we are currently splitting on
            target = The query point we are attempting to find a nearest neighbor for
            currBest = Used to store the current best (closest) node
            current = The current node we are recurring on
        OUTPUT:
            Node closet to the target point
        '''

        if not current.getLeft() and not current.getRight():
            if self.shouldReplace(target,currBest,current):
                return current
            else:
                return currBest
        finalValue = currBest
        visitedLeft = False # variable that tells us which child we visit
        if self.smallerDimValue(current, target, dim) and current.getRight():
            finalValue = self.__findNearestNeighbor((dim + 1) % self.dimensions, target, current, current.getRight())
        if self.smallerDimValue(target, current, dim) and current.getLeft():
            visitedLeft = True
            finalValue = self.__findNearestNeighbor((dim + 1) % self.dimensions,target, current, current.getLeft())
        if self.shouldReplace(target, finalValue, current):
            finalValue = current
        if self.splitPlaneDistance(target, current, finalValue):
            if visitedLeft and current.getRight():
                oppositetree = self.__findNearestNeighbor((dim + 1) % self.dimensions, target, finalValue, current.getRight())
                if self.shouldReplace(target, finalValue, oppositetree):
                    finalValue = oppositetree
            if not visitedLeft and current.getLeft():
                oppositetree = self.__findNearestNeighbor((dim + 1) % self.dimensions, target, finalValue, current.getLeft())
                if self.shouldReplace(target, finalValue, oppositetree):
                    finalValue = oppositetree
        return finalValue
    
    def linearTestNN(self, target):
        '''
        This function will allow us to compare the runtimes between running a find
        nearest neighbor search and linealy searching through our list to find 
        the minimum distance neighbor.
        INPUT:
            target = Query point
        OUTPUT:
            Node that is closest to the target
        
        Runtime - O(n) - This runs in O(n) because we have to check every single 
        element in our array (using this algorithm). An algorithm such as findnearestneighbor
        cuts down subtrees that cannot possibly contain a closer point so its runtime 
        is much faster on a average case.
        '''

        node = KDTreeNode(target, 0)
        minimum = self.points[0]
        for data in self.points:
            if self.euclideanDistance(node, minimum) > self.euclideanDistance(node, data):
                minimum = data
        return minimum
    
    def verifyNearest(self, target):
        '''
        This is a testing function I created to make sure that 
        both linear and findNearestNeighbor return nodes that are the same distance away from
        the target point. I had to implement this because we might not get the same point 
        but the distances should be the exact same.
        INPUT:
            target = Query point
        OUTPUT:
            True if the two algorithms result's are same distance apart from the target.
        '''

        linear = self.linearTestNN(target)
        lgn = self.findNearestNeighbor(target)
        node = KDTreeNode(target, 0)
        return self.euclideanDistance(linear, node) == self.euclideanDistance(lgn, node)

    def __len__(self):
        '''
        This returns the length of our kdtree. Allows for len() functionality.
        '''

        return len(self.points)

from random import randint
kdtree = KDTree(5)
def createPoint(dim):
    return [randint(-100,100) for x in range(dim)]


# lstData = [(3, 2),	(5, 8),	(6, 1),	(4, 4),	(9, 0),	(1, 1),	(2, 2),	(8, 7)]
lstData = [createPoint(5) for x in range(51)]
kdtree.createBalancedTree(lstData)
kdtree.createLeafTree()
print(kdtree)
