import numpy as np 

class node:
    #data - the feature data array created in data_collection.py
    #left_child/ right_child - binary tree children of current node
    #phish_val - the predicted classification, only useful for the leaf nodes
    #is_leaf - value is true if the node is a leaf node, false otherwise
    def __init__(self, data=None, left_child=None, right_child=None, phish_val=None, is_leaf=False):
        self.data = data
        self.left_child = left_child
        self.right_child = right_child
        self.phish_val = phish_val
        self.is_leaf = is_leaf


class decision_tree:
    def __init__(self, max_depth=100):
        self.max_depth = max_depth
        self.root = node()

    #Starts the process of building the tree, converts data to column stack and calls expand_tree
    def start_building(self, features):
        data = np.column_stack(features)
        self.root.data = data
        self.expand_tree(self.root)
    
    #Recursively builds the tree, passes in a node and checks if it will exceed max depth or 
    #if it is going to be a leaf node. Also handles splitting
    def expand_tree(self, current_node, depth=0):

    #Returns the feature in the data with the highest information gain, there will be the split
    def best_split(self, data):

    #Calculates information gain for each potential split (using entropy)
    def information_gain():

    #Calculates the entropy
    def entropy():

    #Splits the data based on results of best_split 
    def split_by_feature():

    #Returns true if all data at a node is in the same class (pure)
    def same_classification():
        
    #Uses input to predict classification based on the created tree
    def predict():

