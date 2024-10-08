import numpy as np 

class node:
    #data - the feature data array created in data_collection.py
    #left_child/ right_child - binary tree children of current node
    #phish_val - the predicted classification, only useful for the leaf nodes
    #is_leaf - value is true if the node is a leaf node, false otherwise
    def init(self, data=None, left_child=None, right_child=None, phish_val=None, is_leaf=False):
        self.data = data
        self.left_child = left_child
        self.right_child = right_child
        self.phish_val = phish_val
        self.is_leaf = is_leaf


class decision_tree:


