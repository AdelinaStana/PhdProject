import networkx as nx
import numpy as np
from collections import OrderedDict

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
        print(f"\n\n\nMSTClustering - cluster count: {len(self.clusters)}")

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
            print("Distribution: ", end="")
            # print packages distribution
            sorted_dict = OrderedDict(sorted(packages_dict.items(), key=lambda item: item[1], reverse=True))
            for item in sorted_dict.items():
                print(f"{item[0]} - {item[1]} [{round((item[1]*100)/count, 1)}%]", end=", ")
