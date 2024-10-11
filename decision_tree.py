import numpy as np 
import math

class node:
    #data - the feature data array created in data_collection.py
    #left_child/ right_child - binary tree children of current node
    #phish_val - the predicted classification, only useful for the leaf nodes
    #is_leaf - value is true if the node is a leaf node, false otherwise
    def __init__(self, data=None, left_child=None, right_child=None, phish_val=None, is_leaf=False, depth=None):
        self.data = data
        self.left_child = left_child
        self.right_child = right_child
        self.phish_val = phish_val
        self.is_leaf = is_leaf
        self.depth = depth


class decision_tree:
    def __init__(self, max_depth=100):
        self.max_depth = max_depth
        self.root = node()
        self.depth = 1

    #------------------------------------------------------------------------------------------------------#

    #Starts the process of building the tree, converts data to column stack and calls expand_tree (recursive)
    def start_building(self, features):
        data = np.column_stack(features)
        self.root.data = data
        self.expand_tree(self.root, self.depth)

    #------------------------------------------------------------------------------------------------------#
    
    #Recursively builds the tree, passes in a node and checks if it will exceed max depth or 
    #if it is going to be a leaf node. Also handles splitting
    def expand_tree(self, current_node, depth=0):
        if depth >= self.max_depth or self.same_classification(current_node.data)
            current_node.is_leaf = True
            
            #TODO:Assign current_node.phish_val here
         
        #TODO:Determine best_split and create child nodes

        #TODO:Call expand_tree on the new child nodes

    #------------------------------------------------------------------------------------------------------#

    #Returns the feature in the data with the highest information gain, there will be the split
    def best_split(self, data):
        best_info_gain = -math.inf
        best_feature_column = None
        best_split_value = None
        num_features = 16 #15 RBG values and one brand val

        #Only need to calculate parent entropy once for each split 
        parent_entropy = self.entropy(data)

        #Determines what feature is going to be best to split on
        for feature in range(num_features):
            feature_vals = np.unique(data[:, feature])

            #NOTETOSELF: might want to change to different feature_vals to iterate through if causing problems

            for split_value in feature_vals:
                info_gain = self.information_gain(data, feature_vals, split_value, parent_entropy)
                if info_gain > best_info_gain:
                    best_info_gain = info_gain
                    best_feature_column = feature_vals
                    best_split_value = split_value
        
        return best_feature_column, best_split_value

    #------------------------------------------------------------------------------------------------------#

    #Calculates information gain for each potential split 
    #<https://en.wikipedia.org/wiki/Information_gain_(decision_tree)>
    def information_gain(self, data, feature_column, split_value, parent_entropy):
        left_child, right_child = self.split_by_feature(data, feature_column, split_value)

        if len(left_child) == 0 or len(right_child) == 0:
            return 0

        left_child_entropy = self.entropy(left_child)
        right_child_entropy = self.entropy(right_child)
        average_child_entropy = (left_child_entropy + right_child_entropy) / 2 #NOTETOSELF: May want to switch to weighted average

        return parent_entropy - average_child_entropy
         

    #------------------------------------------------------------------------------------------------------#

    #Calculates the binary entropy using phish_val (either 0 or 1) 
    #<https://en.wikipedia.org/wiki/Binary_entropy_function>
    def entropy(self, data):
        phish_vals = data[:, -1]
        p = np.mean(phish_vals)
        
        #If the probability is 1 or 0 then the phish_vals are of the same classification
        if p == 1 or p == 0:
            return 0

        return -p * np.log2(p) - (1 - p) * np.log2(1 - p)
    
    #------------------------------------------------------------------------------------------------------#
        
    #Splits the data based on the feature and split value 
    def split_by_feature(self, data, feature_column, split_value):
        left_data = []
        right_data = []

        for row in data:
            if row[feature_column] <= split_value:
                left_data.append(row)
            else:
                right_data.append(row)
        
        return np.array(left_data), np.array(right_data)


    #------------------------------------------------------------------------------------------------------#

    #Returns true if all data at a node is in the same class/phish_val (pure)
    def same_classification(self, data):
        phish_vals = data[:, -1]
        unique_vals = np.unique(phish_vals)
        return len(unique_vals) == 1

    #------------------------------------------------------------------------------------------------------#
        
    #Uses input to predict classification based on the created tree
    def predict():

