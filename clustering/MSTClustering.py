import networkx as nx
import numpy as np


class MSTClustering:
    def __init__(self, dependencies):
        self.index_name_map = dependencies.index_name_map
        self.labels = np.array([0] * dependencies.n)

        G = nx.Graph()
        for edge in dependencies.array:
            G.add_edge(edge[0], edge[1], weight=edge[2])

        mst = nx.minimum_spanning_tree(G)

        cluster_id = 0
        for component in nx.connected_components(mst):
            for node in component:
                self.labels[node] = cluster_id
            cluster_id += 1

        self.clusters = set(self.labels)

    def print_clusters(self):
        print(f"MSTClustering - cluster count: {len(self.clusters)}")

        for cluster in self.clusters:
            count = 0
            print(f"Cluster {cluster}: ", end="")
            for i in range(0, len(self.labels)):
                if self.labels[i] == cluster:
                    print(self.index_name_map[i], end=", ")
                    count += 1
            print(f"total: {count}")