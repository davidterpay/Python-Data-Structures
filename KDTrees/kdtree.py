import sys
sys.path.append('../')
from Binary_Tree.binarytree import BinarySearchTree
from kdtreenode import KDTreeNode
from functools import reduce

'''
Written by David Terpay
This is a KDTree class I wrote that includes some of the most important
functionality in CS as a whole. When I say that I am referencing range based
queries and finding nearest neighbors to a data point. I inherited the binary search
tree class I previously created since a KDTree is a type of BST. This allows for nearly
all of the functionality found the super class (including traversals, depth, breadth first
searches, etc.). Since KDTrees are harder than most data structures, I will link the extremely
helpful websites I found when I was building this class.

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
        if self.root:
            node = KDTreeNode(data, len(data))
            self.__insert(node, self.root, 0)
        else:
            self.root = KDTreeNode(data, 0)
            self.points.append(self.root)
        
    def __insert(self, newNode, node, dim):
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
        for data in lst:
            self.insert(data)

    def smallerDimValue(self, newNode, node, dim):
        '''
        Determines if Point a is smaller than Point b in a given dimension d.
        '''
        
        return node.getData()[dim] >= newNode.getData()[dim]

    def remove(self, data):
        if self.root:
            self.__remove(data, self.root, 0)
        
    def __remove(self, data, node, dim):
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
        return reduce(lambda x,y: x if x.getData()[dimension] <= y.getData()[dimension] else y, [node for node in args if node])

    def find(self, data):
        return self.__find(data, self.root, 0)
    
    def __find(self, data, node, dim):
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
        '''
        if lst:
            data = self.quickselect(lst)
            self.root = self.__buildTree(0, len(data) - 1, data, 0)
            self.points = data
        else:
            self.points = self.quickselect()
            self.root = self.__buildTree(0, len(self.points) - 1, self.points, 0)
        return list(map(KDTreeNode.getData, self.points))

    def __buildTree(self, left, right, lst, dim):
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
        print(node)
        print(lgn)
        print(linear)
        return self.euclideanDistance(linear, node) == self.euclideanDistance(lgn, node)

    def __len__(self):
        '''
        This returns the length of our kdtree. Allows for len() functionality.
        '''

        return len(self.points)
