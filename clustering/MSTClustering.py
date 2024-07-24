import numpy as np
from mst_clustering import MSTClustering


class MSTClusteringWrapper:
    def __init__(self, dependencies):
        scaled_matrix = np.zeros((dependencies.n, dependencies.n), dtype=float)
        non_zero_mask = dependencies.matrix != 0
        scaled_matrix[non_zero_mask] = 1 / dependencies.matrix[non_zero_mask]

        model = MSTClustering(cutoff_scale=0.02, min_cluster_size=2)

        self.labels = model.fit_predict(scaled_matrix)
        self.clusters = set(self.labels)
