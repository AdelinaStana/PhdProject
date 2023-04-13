from mst_clustering import MSTClustering
import numpy as np

from clustering.ClusterEvaluator import ClusterEvaluator


class ClusteringAnalyzer:
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
        self.model.fit(self.data)
        self.labels = self.model.labels_
        self.nodes = {}
        for i in np.unique(self.labels):
            self.nodes[i] = set(np.where(self.labels == i)[0])

    def print_cluster_info(self):
        print("Labels: " + str(self.labels))
        print("Number of clusters: " + str(len(np.unique(self.labels))))
        for i, cluster_nodes in self.nodes.items():
            node_values = self.data[list(cluster_nodes)].astype(int)
            node_numbers = [node + 1 for node in cluster_nodes]
            print(f"Nodes associated with label {i}: {node_values.tolist()} (Node numbers: {node_numbers})")


c1 = ClusteringAnalyzer('data.csv', cutoff_scale=2)
c1.fit()
c2 = ClusteringAnalyzer('data.csv', cutoff_scale=1)
c2.fit()

eval = ClusterEvaluator()
print(eval.compute_mojo(c1.labels, c2.labels))
