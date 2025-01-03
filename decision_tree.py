import numpy as np 
from data_processing import EXPECTED_FEATURES, NUM_COLORS

class node:
    #data - the feature data array created in data_collection.py (length of EXPECTED_FEATURES)
    #left_child/ right_child - binary tree children of current node
    #phish_val - the predicted classification, only useful for the leaf nodes
    #is_leaf - value is true if the node is a leaf node, false otherwise
    #depth - keeps track of current node depth in the tree, compares against max_depth
    #split_val - the value of the feature the children split at, used for prediction
    #feature - what feature is being used to split the node children, used for prediction
    def __init__(self, data=None, left_child=None, right_child=None, phish_val=None, is_leaf=False, depth=None, split_val=None, feature=None):
        self.data = data
        self.left_child = left_child
        self.right_child = right_child
        self.phish_val = phish_val
        self.is_leaf = is_leaf
        self.depth = depth
        self.split_val = split_val
        self.feature = feature

class decision_tree:
    def __init__(self, max_depth=9, min_data_split=7):
        self.max_depth = max_depth
        self.min_data_split  = min_data_split
        self.root = node(depth=0)
    

    #Starts the process of building the tree, converts data to column stack and calls expand_tree (recursive)
    def start_building(self, features):
        self.root.data = features
        self.expand_tree(self.root)

    
    #Recursively builds the tree, passes in a node and checks if it will exceed max depth, if the data is  
    #of the same classification, or if it is too small. Then it is going to be a leaf node.
    def expand_tree(self, current_node):
        #If the data is empty, mark it as empty and create a leaf node
        if len(current_node.data) == 0:
            current_node.is_leaf = True
            current_node.phish_val = -1
            return 
        
        #Check to see if a leaf node condition (depth, min_samples, or same class) has been reached
        if current_node.depth >= self.max_depth or self.same_classification(current_node.data) or len(current_node.data) < self.min_data_split:
            current_node.is_leaf = True
            current_node.phish_val = np.round(np.mean(current_node.data[:, -1])) 
            print(f"Created a leaf: phish_val: {current_node.phish_val}, depth: {current_node.depth}, feature: {current_node.feature}")
            return
        
        #Early leaf creation if there is a high or low phish ratio after a split 
        num_phish = np.sum(current_node.data[:,-1] == 0)
        phish_ratio = num_phish / len(current_node.data)

        if phish_ratio < 0.2:
            current_node.is_leaf = True
            current_node.phish_val = 1 
            return 
        
        if phish_ratio > 0.8:
            current_node.is_leaf = True
            current_node.phish_val = 0 
            return 

        best_feature_column, best_split_value = self.best_split(current_node.data)
        
        if(best_feature_column == None or best_split_value == None):
            print("No more good splits found, creating a leaf...")
            current_node.is_leaf = True
            current_node.phish_val = np.round(np.mean(current_node.data[:, -1]))
            return

        left_data, right_data = self.split_by_feature(current_node.data, best_feature_column, best_split_value)

        current_node.split_val = best_split_value
        current_node.feature = best_feature_column
        current_node.left_child = node(left_data, depth=current_node.depth+1)
        current_node.right_child = node(right_data, depth=current_node.depth+1)
        
        self.expand_tree(current_node.left_child)
        self.expand_tree(current_node.right_child)


    #Returns the feature in the data with the highest information gain, there will be the split
    def best_split(self, data):
        num_features = EXPECTED_FEATURES - 1  #ignoring the phish_val
        
        #Only need to calculate parent entropy once for each split 
        parent_entropy = self.entropy(data)
        print(f"Parent entropy: {parent_entropy}")

        #If entropy is 0 that means the data is of the same classification, so no more splitting needed
        if(parent_entropy == 0):
            return None, None

        best_info_gain = 0.0
        best_feature_column = None
        best_split_value = None
        found_brand_split = False

        for feature in range(NUM_COLORS, num_features):
            if np.any(data[:, feature] == 1):
                    info_gain = self.information_gain(data, feature, 0, parent_entropy) * 7.0 #I want *good* brand splits to happen before color ones
                    if info_gain > best_info_gain:
                        found_brand_split = True
                        best_info_gain = info_gain
                        best_feature_column = feature
                        best_split_value = 0

        if found_brand_split is False: 
            for feature in range(NUM_COLORS):
                feature_vals_padded = np.unique(data[:, feature])
                #Ignore padded colors
                feature_vals = feature_vals_padded[feature_vals_padded != 0.0] 
                split_points = np.percentile(feature_vals, [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 99])
                if len(split_points) > 1:
                    for split_val in split_points:
                        info_gain = self.information_gain(data, feature, split_val, parent_entropy)
                        if feature == 0:
                            info_gain *= 2.0
                        if info_gain > best_info_gain:
                            best_info_gain = info_gain
                            best_feature_column = feature
                            best_split_value = split_val

        print(f"best feature: {best_feature_column}, best split_val: {best_split_value}, best info_gain: {best_info_gain}")
        return best_feature_column, best_split_value
        

    #Calculates information gain for each potential split 
    #<https://en.wikipedia.org/wiki/Information_gain_(decision_tree)>
    def information_gain(self, data, feature_column, split_value, parent_entropy):
        left_child, right_child = self.split_by_feature(data, feature_column, split_value)
        
        if len(left_child) < self.min_data_split or len(right_child) < self.min_data_split:
            return 0

        left_weight = len(left_child) / len(data)
        right_weight = len(right_child) / len(data)

        left_child_entropy = self.entropy(left_child)
        right_child_entropy = self.entropy(right_child)
        weighted_child_entropy = (left_weight * left_child_entropy + right_weight * right_child_entropy) 
    
        gain = parent_entropy - weighted_child_entropy
        balance = 1 - abs(left_child_entropy - right_child_entropy)
        
        if feature_column >= NUM_COLORS:
            #If split creates a right child that is very "pure"
            if right_child_entropy < 0.1 or left_child_entropy < 0.1:
                return gain * 2.5
            return gain * 1.5

        return gain * (balance ** 2)

    
    #Calculates the binary entropy using phish_val (phish_val is either 0 or 1) 
    #<https://en.wikipedia.org/wiki/Binary_entropy_function>
    def entropy(self, data):
        if len(data) == 0:
            return 0

        phish_vals = data[:, -1]
        p = np.mean(phish_vals)
        
        #If the probability is 1 or 0 then the phish_vals are of the same classification 
        if p < 0.1 or p > 0.9:
            return 0

        return -p * np.log2(p) - (1 - p) * np.log2(1 - p)  
    
        
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


    #Returns true if all data at a node is in the same class/phish_val (pure)
    def same_classification(self, data):
        phish_vals = data[:, -1]
        unique_vals = np.unique(phish_vals)
        return len(unique_vals) == 1

        
    #Uses input to predict classification based on the created tree
    #Returns array of predictions based on data
    def predict(self, data):
        predictions = []
        for features in data:
            phish_prediction = self.predict_traverse(features, self.root)
            predictions.append(phish_prediction)
        return np.array(predictions)

    
    #Recursive tree traversal function, used for classification of data (phish_val)
    def predict_traverse(self, features, current_node):
        if current_node.is_leaf:
            if current_node.phish_val == -1:
                print(f"Traversed to an empty node at depth {current_node.depth}")
                return 0
            return current_node.phish_val 
        
        #If the data being split on it a padded value, go the route with the larger sample of data (only for colors)
        if current_node.feature < (NUM_COLORS) and features[current_node.feature] == 0.0:
            if len(current_node.left_child.data) > len(current_node.right_child.data):
                return self.predict_traverse(features, current_node.left_child)
            else:
                return self.predict_traverse(features, current_node.right_child) 

        if features[current_node.feature] <= current_node.split_val:
            return self.predict_traverse(features, current_node.left_child)
        else:
            return self.predict_traverse(features, current_node.right_child)


