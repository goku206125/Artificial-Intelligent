
import pandas as pd
import numpy as np
import time
import math
from sklearn.metrics import classification_report, confusion_matrix

from tsne import *
from knn import *
from decisiontree import *


def get_parameters():
    test_size_percent = get_float_input("Please enter the desired test size as a fraction (from 0.05 to 0.95):", 0.05, 0.95)
    neighbors_to_find = get_int_input("Please enter the number of neighbors to use in the KNN algorithm (from 1 to 149):", 1, 149)
    max_depth = get_int_input("Please enter the maximum depth of the decision tree algorithm (min 1):", 1)
    trials = get_int_input("Please enter the number of trials to run both algorithms for (min 1):", 1)
    return test_size_percent, neighbors_to_find, max_depth, trials


def get_int_input(prompt, minval = -math.inf, maxval = math.inf):
    while True:
        try:
            value = int(input(prompt))
            if (value < minval or value > maxval):
                print("Input is outside of specified range.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_float_input(prompt, minval = -math.inf, maxval = math.inf):
    while True:
        try:
            value = float(input(prompt))
            if (value < minval or value > maxval):
                print("Input is outside of specified range.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Split the dataset into training and testing sets
def train_test_split(data, test_size):
    data_copy = data.copy()
    test_data = data_copy.sample(frac=test_size)
    train_data = data_copy.drop(test_data.index)
    return train_data, test_data

# Load the dataset from the URL (so you don't need to have the file on your computer)
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
column_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']
data = pd.read_csv(url, header=None, names=column_names)

test_size_percent, neighbors_to_find, max_depth, trials = get_parameters()

time_elapsed = {'knn': 0, 'decisiontree': 0}
accuracy = 0

actual_values = pd.DataFrame()
predicted_values_knn = pd.DataFrame()
predicted_values_decisiontree = pd.DataFrame()

for trial in range(trials):
    # Randomly split the dataset into training and testing data sets according to the percentage provided
    train_data, test_data = train_test_split(data, test_size_percent)

    # Prepare the data for t-SNE
    X_vals, Y_vals = prepare_data_for_TSNE(train_data, test_data)

    # Perform t-SNE on the entire data set
    X_train_tsne, X_test_tsne = perform_TSNE(X_vals, test_size_percent)

    # Make predictions for the test data using K nearest neighbors method and measure the computation time
    start_time = time.time()
    test_data['prediction'] = [k_nearest_neighbors(train_data, row, neighbors_to_find) for _, row in test_data.iterrows()]
    stop_time = time.time()
    time_elapsed['knn'] += stop_time - start_time

    # Plot the t-SNE to show the results of the predictions
    plot_TSNE(X_train_tsne, X_test_tsne, Y_vals, test_data, trial, method = 'K Nearest Neighbors')

    actual_values = pd.concat([actual_values, pd.DataFrame(test_data['species'].values)])
    predicted_values_knn = pd.concat([predicted_values_knn, pd.DataFrame(test_data['prediction'].values)])
 
    start_time = time.time()

    # Train the decision tree
    tree = build_tree(train_data, max_depth)

    # Make predictions for the test data using the decision tree method and measure the computation time
    test_data['prediction'] = [tree_predict(tree, row) for _, row in test_data.iterrows()]
    stop_time = time.time()
    time_elapsed['decisiontree'] += stop_time - start_time

    # Plot the t-SNE to show the results of the predictions
    plot_TSNE(X_train_tsne, X_test_tsne, Y_vals, test_data, trial, method = 'Decision Tree')

    predicted_values_decisiontree = pd.concat([predicted_values_decisiontree, pd.DataFrame(test_data['prediction'].values)])



print(f"K nearest neighbors average computation time: {(time_elapsed['knn']/trials):.3f} seconds")

print("K nearest neighbors classification report:")
print(classification_report(actual_values, predicted_values_knn))

print("K nearest neighbors confusion matrix:")
print(confusion_matrix(actual_values, predicted_values_knn, normalize = 'true'))

print(f"\nDecision tree average computation time: {(time_elapsed['decisiontree']/trials):.3f} seconds")

print("Decision tree classification report:")
print(classification_report(actual_values, predicted_values_decisiontree))

print("Decision tree confusion matrix:")
print(confusion_matrix(actual_values, predicted_values_decisiontree, normalize = 'true'))








