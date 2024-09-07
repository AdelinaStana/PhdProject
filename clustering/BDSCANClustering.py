from scipy import sparse
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import MinMaxScaler
import numpy as np


class DBSCANClustering:
    def __init__(self, dependencies):
        weights = np.array(dependencies.matrix)

        distance_matrix = np.full(weights.shape, 1e10)
        non_zero_weights = weights != 0
        distance_matrix[non_zero_weights] = 1 / weights[non_zero_weights]
        matrix = sparse.csr_matrix(distance_matrix)

        dense_matrix = matrix.toarray()

        dbscan = DBSCAN(eps=0.5, min_samples=4, metric='precomputed')
        self.labels = dbscan.fit_predict(dense_matrix)
        self.clusters = set(self.labels)