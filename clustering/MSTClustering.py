from scipy.sparse.csgraph import minimum_spanning_tree, connected_components
import numpy as np


class MSTClustering:
    def __init__(self, dependencies):
        mst = minimum_spanning_tree(dependencies.matrix)
        mst_dense = mst.toarray()

        non_zero_values = dependencies.matrix[dependencies.matrix > 0]
        if len(non_zero_values) > 0:
            threshold = np.min(non_zero_values)

        mst_dense[mst_dense <= threshold] = 0
        # find threshold based on cluster output

        _, self.labels = connected_components(mst_dense, directed=True)

        self.clusters = {}
        for i, label in enumerate(self.labels):
            if label not in self.clusters:
                self.clusters[label] = []
            self.clusters[label].append(i)

