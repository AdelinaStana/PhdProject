import numpy as np
from mst_clustering import MSTClustering
import networkx as nx


def invert_weights(graph, threshold):
    new_graph = nx.Graph()
    for u, v, d in graph.edges(data=True):
        if d['weight'] != 0:
            w = 1 / d['weight']
            if w < threshold:
                new_graph.add_edge(u, v, weight=w)
    return new_graph


class MSTClusteringWrapper:
    # def __init__(self, dependencies):
    #     scaled_matrix = np.zeros((dependencies.n, dependencies.n), dtype=float)
    #     non_zero_mask = dependencies.matrix != 0
    #     scaled_matrix[non_zero_mask] = 1 / dependencies.matrix[non_zero_mask]
    #
    #     non_zero_values = scaled_matrix[non_zero_mask]
    #     max_non_zero = np.max(non_zero_values)
    #
    #     model = MSTClustering(cutoff_scale=max_non_zero)
    #
    #     self.labels = model.fit_predict(scaled_matrix)
    #     self.clusters = set(self.labels)

    def __init__(self, dependencies):
        self.index_name_map = dependencies.index_name_map
        self.labels = np.array([-1] * dependencies.n)

        scaled_matrix = np.zeros((dependencies.n, dependencies.n), dtype=float)
        non_zero_mask = dependencies.matrix != 0
        scaled_matrix[non_zero_mask] = 1 / dependencies.matrix[non_zero_mask]

        non_zero_values = scaled_matrix[non_zero_mask]
        cutoff = np.max(non_zero_values)

        scaled_graph = invert_weights(dependencies.graph, cutoff)
        mst = nx.minimum_spanning_tree(scaled_graph, algorithm='prim')

        cluster_id = 0
        for component in nx.connected_components(mst):
            for node in component:
                self.labels[dependencies.name_index_map[node]] = cluster_id
            cluster_id += 1

        self.clusters = set(self.labels)

    def print_clusters(self):
        print(f"\nMST Clustering - cluster count: {len(self.clusters)}")

        for cluster in self.clusters:
            packages_dict = {}
            count = 0
            print(f"\n\nCluster {cluster}: ", end="")
            for i in range(0, len(self.labels)):
                if self.labels[i] == cluster:
                    full_name = self.index_name_map[i]
                    print(full_name, end=", ")
                    count += 1

                    # count packages distribution
                    packages = full_name.split(".")[:-1]
                    for package in packages:
                        if package in packages_dict.keys():
                            packages_dict[package] += 1
                        else:
                            packages_dict[package] = 1

            print(f"\nTotal: {count}")
