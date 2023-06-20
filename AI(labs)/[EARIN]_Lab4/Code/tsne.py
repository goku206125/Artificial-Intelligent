import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

# Recombine the data sets so that irises of the same species in both data sets are grouped together on the plot. Then,
# separate the 'species' column from the others.
def prepare_data_for_TSNE(train_data, test_data):
    recombined_data = pd.concat([train_data, test_data])
    X_vals = recombined_data.drop('species', axis=1).values
    Y_vals = train_data['species'].values

    return X_vals, Y_vals

# Use t-SNE to flatten the four dimensional data set into two dimensions
def perform_TSNE(X_vals, test_size_percent):
    total_data_size = len(X_vals)
    total_validation_size = total_data_size - round(test_size_percent * total_data_size)
    
    tsne = TSNE(n_components=2, random_state=42, perplexity = 20)
    X_tsne = tsne.fit_transform(X_vals)
    X_train_tsne = X_tsne[:total_validation_size]
    X_test_tsne = X_tsne[total_validation_size:]

    return X_train_tsne, X_test_tsne

# Plot points belonging to both data sets on the same graph
def plot_TSNE(X_train_tsne, X_test_tsne, Y_vals, test_data, trial, method):
    # Establish the color that will be associated with each species' data points
    colors = {'Iris-setosa': 'green', 'Iris-versicolor': 'darkorange', 'Iris-virginica': 'purple'}
    labels = list(colors.keys())

    plt.figure(figsize=(10, 6))
    plot_train_data(X_train_tsne, Y_vals, labels, colors)
    plot_test_data(X_test_tsne, test_data, colors)
    print_plot(trial, method)

# Plot points belonging to the training data set using solid colors
def plot_train_data(X_train_tsne, Y_vals, labels, colors):
    for species in labels:
        plt.scatter(X_train_tsne[Y_vals == species, 0], X_train_tsne[Y_vals == species, 1],
                    c=colors[species], label=species, s=50, alpha=0.6)

# Plot points belonging to the testing data set using two colors. The color on the inside is that of the predicted
# iris species, whereas the color on the outside is that of the correct species if the prediction was incorrect
# and black if the prediction was correct.
def plot_test_data(X_test_tsne, test_data, colors):
    for i, (_, row) in enumerate(test_data.iterrows()):
        actual = row['species']
        predicted = row['prediction']

        edge_color = colors[actual] if actual != predicted else 'black'
        plt.scatter(X_test_tsne[i, 0], X_test_tsne[i, 1], c=colors[predicted],
                    edgecolors=edge_color, linewidths=2.7, marker='o', s=55, alpha=0.8)

def print_plot(trial, method):
    plt.xlabel('t-SNE Component 1')
    plt.ylabel('t-SNE Component 2')
    plt.legend()
    plt.title(f'Iris Dataset t-SNE Visualization: Train Data vs. Test Data for {method} Method, Trial {trial + 1}')
    plt.show()