import pandas as pd
import numpy as np

# Define a TreeNode class to represent a node in the decision tree
class TreeNode:
    def __init__(self, feature=None, value=None, left=None, right=None, label=None):
        self.feature = feature
        self.value = value
        self.left = left
        self.right = right
        self.label = label

# The Gini impurity is found for the data set
def gini_impurity(data):
    species_counts = data['species'].value_counts()
    total_count = len(data)
    impurity = 1 - sum((count / total_count) ** 2 for count in species_counts)
    return impurity

# Split the data based on a feature and a value
def split_data(data, feature, value):
    left = data[data[feature] <= value]
    right = data[data[feature] > value]
    return left, right

# Find the best split for the data based on the lowest Gini impurity
def find_best_split(data):
    best_gini = float('inf')
    best_feature = None
    best_value = None

    for feature in data.columns[:-1]:
        for value in data[feature]:
            left, right = split_data(data, feature, value)
            if len(left) == 0 or len(right) == 0:
                continue
            gini_left = gini_impurity(left)
            gini_right = gini_impurity(right)
            weighted_gini = (len(left) * gini_left + len(right) * gini_right) / len(data)
            if weighted_gini < best_gini:
                best_gini = weighted_gini
                best_feature = feature
                best_value = value

    return best_feature, best_value

# Build the decision tree recursively
def build_tree(data, max_depth):
    if max_depth == 0 or len(data['species'].unique()) == 1:
        label = data['species'].mode().iloc[0]
        return TreeNode(label=label)
    
    feature, value = find_best_split(data)
    left_data, right_data = split_data(data, feature, value)

    if len(left_data) == 0 or len(right_data) == 0:
        label = data['species'].mode().iloc[0]
        return TreeNode(label=label)
    
    left = build_tree(left_data, max_depth - 1)
    right = build_tree(right_data, max_depth - 1)

    return TreeNode(feature=feature, value=value, left=left, right=right)

# Make a prediction for a single instance using the decision tree
def tree_predict(node, instance):
    if node.label is not None:
        return node.label
    
    if instance[node.feature] <= node.value:
        return tree_predict(node.left, instance)
    else:
        return tree_predict(node.right, instance)