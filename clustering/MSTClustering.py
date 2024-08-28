import math

import numpy as np
from mst_clustering import MSTClustering
import networkx as nx


def invert_weights(graph, threshold=None):
    new_graph = nx.Graph()
    for u, v, d in graph.edges(data=True):
        if d['weight'] != 0:
            w = 1 / d['weight']
            if threshold is None or w < threshold:
                new_graph.add_edge(u, v, weight=w)
    return new_graph


class MSTClusteringWrapper:
    # def __init__(self, dependencies):
    #     scaled_matrix = np.zeros((dependencies.n, dependencies.n), dtype=float)
    #     for i in range(0, dependencies.n):
    #         for j in range(0, dependencies.n):
    #             if dependencies.matrix[i][j] != 0:
    #                 scaled_matrix[i][j] = 1 / dependencies.matrix[i][j]
    #
    #     non_zero_mask = dependencies.matrix != 0
    #     non_zero_values = scaled_matrix[non_zero_mask]
    #     max_non_zero = np.median(non_zero_values)
    #
    #     model = MSTClustering(cutoff_scale=1, min_cluster_size=2)
    #
    #     self.labels = model.fit_predict(scaled_matrix)
    #     self.clusters = set(self.labels)

    """
        The clusters are formed by the nodes that are still connected by edges from the
        minimum spanning tree. When applying ZMST for software
        clustering, in our approach, the initial weighted graph results
        from the dependency structure matrix. Since the dependency
        structure matrix describes a directed graph, we first transform
        it into an undirected graph by assigning to every edge the
        weight resulting as the average between the two directed
        dependencies. The threshold value used for edge elimination
        can be set as a parameter of the algorithm - in our approach we
        specify the value in a percentual manner (an edge is considered
        too long if its weight is smaller than the certain percent of the
        average weight of all edges in the graph).
    """
    def __init__(self, dependencies):
        graph = invert_weights(dependencies.graph)

        mst = nx.minimum_spanning_tree(graph)

        sorted_edges = sorted(mst.edges(data=True), key=lambda x: x[2]['weight'])

        average_weight = sum(data['weight'] for _, _, data in mst.edges(data=True)) / mst.number_of_edges()

        threshold = average_weight * 3.5

        edges_to_remove = [(u, v) for u, v, data in sorted_edges if data['weight'] > threshold]

        mst.remove_edges_from(edges_to_remove)

        self.labels = np.array([-1] * dependencies.n)
        cluster_id = 0
        for component in nx.connected_components(mst):
            for node in component:
                self.labels[dependencies.name_index_map[node]] = cluster_id
            cluster_id += 1

        if -1 in self.labels:
            print("ups")

        self.clusters = set(self.labels)

    def calculate_nr_edges_to_remove(self, mst, n):
        max_entities_per_cluster = 25

        num_clusters_needed = math.ceil(n / max_entities_per_cluster)
        existing_clusters = len(list(nx.connected_components(mst)))
        num_edges_to_remove = max(0, num_clusters_needed - existing_clusters)

        return num_edges_to_remove


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
