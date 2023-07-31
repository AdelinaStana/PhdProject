from mst_clustering import MSTClustering
import numpy as np


class MSTCluster:
    def __init__(self, data_file, cutoff_scale=1, approximate=True):
        """
        cutoff_scale : minimum size of edges. All edges larger than cutoff_scale will be removed

        approximate: If True, then compute the approximate minimum spanning tree using
                n_neighbors nearest neighbors. If False, then compute the full O[N^2] edges
        """
        self.data = np.genfromtxt(data_file, delimiter=',')
        self.model = MSTClustering(cutoff_scale=cutoff_scale, approximate=approximate)
        self.labels = None
        self.nodes = None

    def fit(self):
        self.labels = self.model.fit_predict(self.data)
        self.nodes = {}
        for i in np.unique(self.labels):
            self.nodes[i] = set(np.where(self.labels == i)[0])

    def print_cluster_info(self):
        print("__________________________________________________\nMST Cluster")
        print("Number of clusters: " + str(len(np.unique(self.labels))))
        print("Labels: " + str(self.labels))

    def print_detailed_cluster_info(self):
        for i, cluster_nodes in self.nodes.items():
            node_values = self.data[list(cluster_nodes)].astype(int)
            node_numbers = [node + 1 for node in cluster_nodes]
            print(f"Nodes associated with label {i}: {node_values.tolist()} (Node numbers: {node_numbers})")

