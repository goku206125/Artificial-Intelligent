import pandas as pd
import numpy as np
from math import sqrt
from collections import Counter


# Calculate the Euclidean distance between two vectors
def euclidean_distance(v1, v2):
    return sqrt(sum((v1 - v2) ** 2 for v1, v2 in zip(v1, v2)))

# Find the distances from the tested point to every point in the training data set. Then, from the closest k points,
# determine the species whose points appear the most number of times. In case of a tie, the species whose point is
# closest to the tested point is chosen as the prediction.
def k_nearest_neighbors(train_data, test_instance, k):
    distances = []
    for index, row in train_data.iterrows():
        dist = euclidean_distance(test_instance[:-1], row[:-1])
        distances.append((index, dist))

    distances.sort(key=lambda x: x[1])
    neighbors = [train_data.loc[d[0]] for d in distances[:k]]
    species_count = Counter(neighbor[-1] for neighbor in neighbors)

    return species_count.most_common(1)[0][0]