import numpy as np
import networkx as nx


class MSTClustering:
    def __init__(self, dependencies):
        G = nx.from_numpy_array(dependencies.matrix)

        mst = nx.minimum_spanning_tree(G)
        mst_dense = nx.to_numpy_array(mst)

        # Use a percentile to set the threshold for edge removal
        percentile = 5
        non_zero_values = mst_dense[mst_dense > 0]
        if len(non_zero_values) > 0:
            threshold = np.percentile(non_zero_values, percentile)
        mst_dense[mst_dense <= threshold] = 0

        G_thresh = nx.from_numpy_array(mst_dense)

        connected_components = list(nx.connected_components(G_thresh))

        self.labels = np.zeros(nx.number_of_nodes(G), dtype=int)
        for label, component in enumerate(connected_components):
            for node in component:
                self.labels[node] = label

        self.clusters = {}
        for i, label in enumerate(self.labels):
            if label not in self.clusters:
                self.clusters[label] = []
            self.clusters[label].append(i)
