'''
BTree properties: 
A BTree of order m is an m-way tree.
All keys within a node are ordered.
All leaves contain no more than m - 1 keys.
All internal nodes have exactly one more child than keys.
Root node can be a leaf or have [2, m] children (because the only way to add a node is to grow).
All non-root nodes have [ceiling(m/2), m] children.
All leaves are on the same level.

Order tells us how many keys can be in a node.
    # of keys = m - 1 
How big is a BTree going to get? 
    BTreeis shorter than AVL:
        AVL has 2 children → h = log2(n).
        BTree has m children → h = logm(n).

2 ciel(m / 2) ^ h - 1 = minimum number of keys in a btree of height h and order m
m ^ (h + 1) - 1 = max number of keys in a btree of height h and order m
'''
